#!/usr/bin/env python3
"""Generate retro/facts/LYB.json (2012-02-10 to 2013-12-31) from LyondellBasell Industries N.V.'s own filings (edgar.py's rows).

Every raw figure is read from its own labelled row (the row is kept for the verbatim checklist), every rate, margin, tax rate
and rule-T value is computed, every quoted sentence is asserted present in its own filing. Only filings accepted on or before
2013-12-31 are read. The downloads (keep them outside the repository):

    python3 retro/tools/edgar.py index 1489393 <dir>
    python3 retro/tools/edgar.py fetch 1489393 <dir> --from 2010-04-01 --to 2014-03-31 --forms 10-K 10-Q 8-K 8-K/A 10-12B 10-12B/A

Run:
    python3 -I retro/generators/lyb/gen_lyb.py --filings <dir> [--out retro/facts/LYB.json] [--checklist <dir>/checklist_lyb.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_lyb.json
"""
import argparse
import datetime as dt
import json
import math
import os
import re
import sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))       # retro/generators/lyb -> the repository
_ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("--filings", required=True, help="folder edgar.py wrote (allrows.json, tenk/, tenq/, eightk/); keep it outside the repo")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/LYB.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_lyb.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402  (the repo's own tool: trading days from the Yahoo cache)

ET = ZoneInfo("America/New_York")
CUT = "2013-12-31"
CIK = 1489393
FILINGS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("LYB")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
CHECK = {}          # verbatim checklist: file -> strings


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def doc(acc, prefix):
    for sub in ("tenk", "tenq", "eightk"):
        d = os.path.join(SP, sub, acc)
        if os.path.isdir(d):
            hits = sorted(f for f in os.listdir(d) if f.startswith(prefix) and f.endswith(".rows.txt"))
            assert len(hits) == 1, (acc, prefix, hits)
            return os.path.join(d, hits[0])
    raise AssertionError(acc)


TEXT = {}


def lines(path):
    if path not in TEXT:
        with open(path, encoding="utf-8", errors="replace") as fh:
            TEXT[path] = [norm(x) for x in fh.read().split("\n")]
    return TEXT[path]


def quote(path, s):
    """Assert a sentence or fragment is in its filing, word for word; add it to the checklist."""
    full = norm(" ".join(lines(path)))
    assert norm(s) in full, (path, s[:120])
    CHECK.setdefault(path, []).append(s)
    return s


def num(tok):
    t = tok.strip().replace("$", "").replace(",", "").strip()
    if t in ("—", "-", "–", "- -", ""):
        return 0.0
    if t == "N/A":
        return None
    neg = t.startswith("(") and t.endswith(")")
    v = float(t.strip("()%"))
    return -v if neg else v


def cells(r):
    """A row's value cells: '($ | 151)' (a dollar sign in its own cell) joined back to '(151)'."""
    r = re.sub(r"\(\s*\$\s*\|\s*", "(", r)
    r = re.sub(r"\|\s*\$\s*\|", "|", r)
    return [t.strip() for t in r.split("|")[1:]]


def row(path, label, start=0, stop=None, exact=True):
    """The unique row in lines[start:stop] whose first cell is `label`; returns (row, numeric values)."""
    L = lines(path)[start:stop]
    dash = lambda t: t.replace("—", "-")          # the Q3 2011 release prints its segment names with em dashes
    hits = [x for x in L if (dash(x.split(" |")[0].strip()) == label if exact else x.startswith(label)) and "|" in x]
    assert len(hits) == 1, (path, label, len(hits), hits[:3], start, stop)
    r = hits[0]
    vals = [num(t) for t in cells(r) if t]
    CHECK.setdefault(path, []).append(r)
    return r, vals


def line_no(path, startswith, nth=0, start=0):
    idx = [i for i, x in enumerate(lines(path)) if i >= start and x.startswith(startswith)]
    return idx[nth]


def next_tday(d):
    return min(x for x in TDAYS if x > d)


def published(acc):
    """Publication date from EDGAR's acceptance time (UTC -> ET); at or after the 16:00 ET close, the next trading day."""
    r = FILINGS[acc]
    t = dt.datetime.fromisoformat(r[1].replace("Z", "+00:00")).astimezone(ET)
    d = t.date().isoformat()
    hm = t.strftime("%H:%M")
    if hm >= "16:00":
        return next_tday(d), f"accepted {d} {hm} ET (after the close), so dated the next trading day"
    if d not in TDAYS:
        return next_tday(d), f"accepted {d} {hm} ET (not a trading day), so dated the next trading day"
    if hm < "09:30":
        return d, f"accepted {d} {hm} ET (before the open)"
    return d, f"accepted {d} {hm} ET (during market hours)"


URL = lambda acc, fn: f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc.replace('-', '')}/{fn}"
SRC = {}


def source(sid, acc, title, path, supports):
    p, filed = published(acc)
    assert p <= CUT, (sid, p)
    fn = os.path.basename(path).split("__", 1)[1].replace(".rows.txt", ".htm")
    SRC[sid] = dict(published=p, filed=filed, title=title, url=URL(acc, fn), supports=supports)
    return sid


usd_m = lambda v: f"${v:,.0f}M" if v >= 0 else f"$({-v:,.0f})M"     # a loss in parentheses, as the filings print it
pct = lambda a, b: round((b / a - 1) * 100, 1) if a > 0 else round((b - a) / abs(a) * 100, 1) if a < 0 else None
mg = lambda x, rev: round(x / rev * 100 + 0.0, 2)

# ── filings ─────────────────────────────────────────────────────────────────────
K10, K11, K12 = "0000950123-11-026580", "0001193125-12-088192", "0001193125-13-051488"     # FY2010, FY2011, FY2012 10-Ks
F10, F11, F12 = doc(K10, "10-K__"), doc(K11, "10-K__"), doc(K12, "10-K__")
REL = {"Q3 2011": "0000950123-11-092763", "Q4 2011": "0001193125-12-051218", "Q1 2012": "0001193125-12-194555",
       "Q2 2012": "0001193125-12-318363", "Q3 2012": "0001193125-12-436640", "Q4 2012": "0001193125-13-033597",
       "Q1 2013": "0001193125-13-175901", "Q2 2013": "0001193125-13-303773", "Q3 2013": "0001193125-13-414776"}
FREL = {q: doc(a, "EX-99.1__") for q, a in REL.items()}
Q311_10Q, Q212_10Q = "0000950123-11-094007", "0001193125-12-318803"
DIV_8K = "0001193125-13-236119"

# ── release tables ──────────────────────────────────────────────────────────────


def table_cols(path, title, nth=0):
    """(start, stop, columns) of a release table: columns are (year, label) for each value cell, from its year and header rows."""
    i0 = line_no(path, title, nth)
    L = lines(path)
    stop = next((i for i in range(i0 + 1, len(L)) if L[i].startswith("Table ")), len(L))
    yi = next(i for i in range(i0, i0 + 6) if re.fullmatch(r"20\d\d( \| 20\d\d)?", L[i]))
    years = [int(y) for y in L[yi].split(" | ")]
    hi = next(i for i in range(yi, yi + 4) if L[i].startswith("(Millions of U.S. dollars)"))
    labels = [c.strip() for c in L[hi].split("|")[1:]]
    if len(years) == 1:
        cols = [(years[0], lb) for lb in labels]
    else:
        k = next(j for j, lb in enumerate(labels) if lb in ("Total", "YTD")) + 1
        cols = [(years[0], lb) for lb in labels[:k]] + [(years[1], lb) for lb in labels[k:]]
    return hi, stop, cols


def tval(path, title, label, year, col, nth=None, section=None, exact=True):
    """A value from a release table by its row label and its (year, column) header; tables of one year are searched in order."""
    tries = [nth] if nth is not None else [0, 1]
    for n in tries:
        try:
            hi, stop, cols = table_cols(path, title, n)
        except (IndexError, StopIteration):
            continue
        if (year, col) not in cols:
            continue
        start = hi
        if section:
            start = line_no(path, section[0], 0, hi)
            stop = line_no(path, section[1], 0, start)
        _, v = row(path, label, start, stop, exact)
        assert len(v) == len(cols), (path, title, label, v, cols)
        return v[cols.index((year, col))]
    raise AssertionError((path, title, label, year, col))


def t1(path):
    """Table 1 (Earnings Summary): revenues, diluted EPS (continuing operations where reported), diluted shares; the cells are the
    quarter, the previous quarter, the year-ago quarter, then year-to-date."""
    i0 = line_no(path, "Table 1 ")
    i1 = i0 + 22
    _, rev = row(path, "Sales and other operating revenues", i0, i1)
    _, sh = row(path, "Diluted share count (millions)", i0, i1)
    L = lines(path)
    hdr = [i for i in range(i0, i1) if L[i].startswith("Diluted earnings per share (U.S. dollars):")]
    if hdr:            # from Q2 2012: the per-share rows follow a header; continuing operations is the second of them
        _, eps = row(path, "Income from continuing operations", hdr[0], hdr[0] + 4)
        basis = "diluted from continuing operations"
    else:
        lab = next(x.split(" |")[0] for x in L[i0:i1] if x.startswith("Diluted earnings"))
        _, eps = row(path, lab, i0, i1)
        basis = "diluted (no discontinued operations in the release)"
    _, ebitda = row(path, "EBITDA(c)" if any(x.startswith("EBITDA(c) |") for x in L[i0:i1]) else
                    "EBITDA(b)" if any(x.startswith("EBITDA(b) |") for x in L[i0:i1]) else
                    "EBITDA(c)(d)" if any(x.startswith("EBITDA(c)(d) |") for x in L[i0:i1]) else "EBITDA(d)", i0, i1)
    return rev, eps, sh, basis, ebitda


PRETAX = ("Income (loss) before taxes", "Income before taxes")


def pretax(path, year, col):
    for lab in PRETAX:
        try:
            return tval(path, "Table 11", lab, year, col)
        except AssertionError:
            pass
    raise AssertionError((path, "pre-tax", year, col))


SEG_SECTION = ("Operating income (loss):", "Depreciation and amortization:")
OPA, IND = "Olefins & Polyolefins - Americas", "Intermediates & Derivatives"

# ── prints ──────────────────────────────────────────────────────────────────────
QDATE = {1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"}
prints, sources_rel = [], {}
SID = {"Q3 2011": "LB10", "Q4 2011": "LB11", "Q1 2012": "LB12", "Q2 2012": "LB13", "Q3 2012": "LB14", "Q4 2012": "LB15",
       "Q1 2013": "LB16", "Q2 2013": "LB17", "Q3 2013": "LB18"}
ORDER = list(REL)
for qi, (qq, acc) in enumerate(REL.items()):
    q, fy = int(qq[1]), int(qq[3:])
    f = FREL[qq]
    rev, eps, sh, basis, ebitda = t1(f)
    qc = f"Q{q}"
    oi, oi_p = tval(f, "Table 11", "Operating income", fy, qc), tval(f, "Table 11", "Operating income", fy - 1, qc)
    pti, pti_p = pretax(f, fy, qc), pretax(f, fy - 1, qc)
    # the year-ago quarter's revenues from the same release's Table 1 (its third cell), checked against its Table 11
    assert rev[2] == tval(f, "Table 11", "Sales and other operating revenues", fy - 1, qc), qq
    assert rev[0] == tval(f, "Table 11", "Sales and other operating revenues", fy, qc), qq
    opa, opa_p = (tval(f, "Table 8", OPA, fy, qc, section=SEG_SECTION), tval(f, "Table 8", OPA, fy - 1, qc, section=SEG_SECTION))
    ind, ind_p = (tval(f, "Table 8", IND, fy, qc, section=SEG_SECTION), tval(f, "Table 8", IND, fy - 1, qc, section=SEG_SECTION))
    pub, filed = published(acc)
    title = f"LyondellBasell Industries N.V. {qq} results (8-K, Exhibit 99.1)"
    sid = source(SID[qq], acc, title, f, "the quarter's Table 1 (revenues, diluted EPS, diluted shares), Table 8 (segment operating "
                 "income) and Table 11 (statement of income), each with the year-ago quarter as this release shows it")
    raw = dict(rev_m=rev[0], rev_prior_m=rev[2], oi_m=oi, oi_prior_m=oi_p, pti_m=pti, pti_prior_m=pti_p, eps_q=eps[0], eps_q_prior=eps[2],
               dil_sh_m=sh[0], opa_m=opa, opa_prior_m=opa_p, ind_m=ind, ind_prior_m=ind_p, ebitda_m=ebitda[0])
    rel_day = dt.date.fromisoformat(FILINGS[acc][1][:10])
    nq = ORDER[qi + 1] if qi + 1 < len(ORDER) else "Q4 2013"
    p = dict(quarter=qq, fy=fy, q=q, published=pub, source=sid, release=f"{rel_day.strftime('%b')} {rel_day.day}",
             release_time=f"8-K {filed}", period_end=f"{fy}-{QDATE[q]}", raw=raw,
             sales_b=round(rev[0] / 1000, 3), sales_pct=pct(rev[2], rev[0]),
             opm=mg(oi, rev[0]), opm_bp=round((mg(oi, rev[0]) - mg(oi_p, rev[2])) * 100, 1),
             ptm=mg(pti, rev[0]), ptm_bp=round((mg(pti, rev[0]) - mg(pti_p, rev[2])) * 100, 1),
             eps_q=eps[0], eps_q_prior=eps[2], diluted_shares_m=sh[0],
             opa_pct=pct(opa_p, opa), ind_pct=pct(ind_p, ind),
             seg_note=f"O&P–Americas operating income {usd_m(opa)} vs {usd_m(opa_p)}, Intermediates & Derivatives {usd_m(ind)} vs {usd_m(ind_p)}",
             sales_note=f"sales and other operating revenues {usd_m(rev[0])} vs {usd_m(rev[2])}",
             margin_note=f"operating income {usd_m(oi)} vs {usd_m(oi_p)}; income before income taxes {usd_m(pti)} vs {usd_m(pti_p)}",
             eps_note=f"GAAP, {basis}, {'$%.2f' % eps[0] if eps[0] >= 0 else '$(%.2f)' % -eps[0]} against "
             f"{'$%.2f' % eps[2] if eps[2] >= 0 else '$(%.2f)' % -eps[2]} a year earlier",
             cash_note=f"EBITDA {usd_m(ebitda[0])} (non-GAAP, display only)",
             next_print=f"the {nq} release")
    if q == 4:
        # the full year: Table 1's year column (its fourth cell), Table 11's year column, Table 2's after-tax one-offs
        ycol = next(c for y, c in table_cols(f, "Table 11", 0)[2] if y == fy and c in ("Total", "YTD"))
        pti_y = pretax(f, fy, ycol)
        tax_lab = ("Provision for (benefit from) income taxes")
        tax_y = tval(f, "Table 11", tax_lab, fy, ycol)
        ni_att = tval(f, "Table 11", "Net income (loss) attributable to the Company", fy, ycol, exact=False)
        i2 = line_no(f, "Table 2 ")
        lab2 = next(x.split(" |")[0] for x in lines(f)[i2:i2 + 40] if x.startswith("After-tax effect of net charges"))
        _, t2 = row(f, lab2, i2, i2 + 40)
        items = t2[3]
        prev_rev = rev[4]
        a = dict(fy=fy, fy_label=f"FY{fy % 100}", eps_normalized=eps[3], excluded_note=None, revenue_usd_b=round(rev[3] / 1000, 3),
                 diluted_shares_m=sh[3],
                 normalization_note=f"FY{fy % 100} ${eps[3]:.2f} {basis} from the {qq} release ({pub}) until the 10-K",
                 op_margin=mg(pti_y, rev[3]),
                 op_margin_note=f"FY{fy % 100} income before income taxes {usd_m(pti_y)} / revenues {usd_m(rev[3])} ({qq} release)",
                 sales_growth=pct(prev_rev, rev[3]),
                 check_pretax_margin=mg(pti_y, rev[3]),
                 check_pretax_note=f"FY{fy % 100} income before income taxes / revenues ({qq} release)",
                 tax_rate=round(tax_y / pti_y, 3), tax_note=f"FY{fy % 100} effective rate: provision for income taxes {usd_m(tax_y)} on {usd_m(pti_y)}",
                 one_off_test=dict(items_after_tax_m=items, income_attributable_m=ni_att, distorted=items > ni_att, kind="charges",
                                   note=(f"the release's Table 2 '{lab2}' of {usd_m(items)} for the year (every item that table lists, "
                                         "charges net of benefits, recurring ones such as the warrants' mark to market included) against "
                                         f"net income attributable to the Company of {usd_m(ni_att)}: kept at GAAP; the net is a charge, "
                                         "so the mirror test does not arise")))
        p["fy_actual"] = a
    prints.append(p)

# the Q2 2012 release moves the Berre refinery to discontinued operations and republishes 2011 on that basis: FY2011's EPS from
# continuing operations and its revenues are restated from that release until a later 10-K (the LMT and CB print-level 'restates')
f = FREL["Q2 2012"]
quote(f, "Berre refinery moved to discontinued operations; business segments have been realigned by moving Oxyfuels to "
         "Intermediates and Derivatives")
r11 = tval(f, "Table 11", "Sales and other operating revenues", 2011, "Total")
i9 = line_no(f, "Table 9 ")
_, e9 = row(f, "Diluted earnings per share – continuing operations", i9, i9 + 60)
assert len(e9) == 8, e9
next(p for p in prints if p["quarter"] == "Q2 2012")["restates"] = {
    "2011": dict(eps_normalized=e9[4], revenue_usd_b=round(r11 / 1000, 3),
                 note=f"FY11 restated by the Q2 2012 release (the Berre refinery in discontinued operations): diluted EPS from continuing "
                      f"operations ${e9[4]:.2f} (Table 9), revenues {usd_m(r11)} (Table 11)")}

# ── history vintages ────────────────────────────────────────────────────────────


def sel(path):
    i0 = [i for i, x in enumerate(lines(path)) if x.lower().startswith("item 6. | selected financial data")][-1]
    return i0, i0 + 60


def mdna_rev(path, sentence):
    quote(path, sentence)
    return sentence


i0, i1 = sel(F10)
_, rev10 = row(F10, "Sales and other operating revenues", i0, i1)        # May-Dec 2010, Jan-Apr 2010, 2009, 2008, 2007, 2006
_, sh10 = row(F10, "Dilutive potential shares", line_no(F10, "Dilutive potential shares"), line_no(F10, "Dilutive potential shares") + 1)
_, ocf10 = row(F10, "Operating activities", i0, i1 + 30)
_, capex10 = row(F10, "Expenditures for property, plant and equipment", i0, i1 + 30)
c10 = quote(F10, "Revenues — We had revenues of $41,151 million in 2010, $30,828 million in 2009 and $50,706 million in 2008.")
quote(F10, "References in the following discussion to results for the year ended December 31, 2010 are to the combined Successor "
           "and Predecessor periods unless otherwise specifically described as Successor or Predecessor.")
quote(F10, "Management believes that combining the Successor and Predecessor periods for the year ended December 31, 2010, which is "
           "a non-GAAP presentation, provides a more meaningful comparison")
assert rev10[0] + rev10[1] == 41151
s24 = line_no(F10, "May 1 through December 31, 2010:")
_, cust10 = row(F10, "Customers", s24, s24 + 4)
WHY10 = quote(F10, "Our businesses are highly cyclical, in addition to experiencing some less significant seasonal effects.")
SEGN = ["Olefins & Polyolefins–Americas", "Olefins & Polyolefins–Europe, Asia, International", "Intermediates & Derivatives",
        "Refining & Oxyfuels", "Technology"]
LISTQ = quote(F10, "Our shares have traded on the New York Stock Exchange, under the symbol “LYB,” since October 14, 2010.")
ISSUEQ = quote(F10, "Our capital was issued effective April 30, 2010 in connection with our emergence from bankruptcy proceedings.")
quote(F10, "We have not yet paid any dividends on our shares.")
source("LB1", K10, "LyondellBasell Industries N.V. FY2010 10-K", F10,
       "the selected financial data (revenues 2006-2009 and the two 2010 periods), the MD&A's combined 2010 revenues and operating "
       "income, the statements of income (2008-2010), the segment note, the EPS note (May-December 2010), Item 5 (the listing, no "
       "dividends yet) and the risk factors")

i0, i1 = sel(F11)
_, rev11 = row(F11, "Sales and other operating revenues", i0, i1)        # 2011, May-Dec 2010, Jan-Apr 2010, 2009, 2008, 2007
_e = line_no(F11, "Earnings per share from continuing operations:", 0, i0)
_, eps11 = row(F11, "Diluted", _e, _e + 3)
_, oi11s = row(F11, "Operating income (loss)(b)", i0, i1)
_, ocf11 = row(F11, "Operating activities", i0, i1 + 20)
_, capex11 = row(F11, "Expenditures for property, plant and equipment", i0, i1 + 20)
quote(F11, "Revenues—We had revenues of $51,035 million in 2011, $41,151 million in 2010 and $30,828 million in 2009.")
quote(F11, "Operating Income—The Company had operating income of $3,998 million, $2,944 million and $317 million in 2011, 2010 and "
           "2009, respectively.")
e11 = line_no(F11, "Potential dilutive shares")
_, sh11 = row(F11, "Potential dilutive shares", e11, e11 + 1)
s24 = line_no(F11, "Year Ended December 31, 2011", 1)
_, cust11 = row(F11, "Customers", s24, s24 + 4)
_, div11 = row(F11, "Dividends paid", line_no(F11, "Net cash provided by (used in) operating activities"),
               line_no(F11, "Net cash provided by (used in) operating activities") + 30)
WHY11 = quote(F11, "Our businesses are highly cyclical, in addition to experiencing some less significant seasonal effects.")
DIV25 = quote(F11, "The Company paid interim dividends of $0.20 per share on September 7, 2011 and $0.25 per share on December 16, 2011.")
quote(F11, "The Company paid a special dividend of $4.50 per share on December 16, 2011.")
source("LB2", K11, "LyondellBasell Industries N.V. FY2011 10-K", F11,
       "FY2011 annual history: the selected financial data (revenues 2007-2011, diluted EPS 2011), the MD&A's combined 2010 revenues, "
       "the EPS note's diluted shares (2011, May-December 2010), the cash flow statement, the segment note (2011 revenues from "
       "customers), the dividends paid and the risk factors")

i0, i1 = sel(F12)
_, rev12 = row(F12, "Sales and other operating revenues", i0, i1)        # 2012, 2011, May-Dec 2010, Jan-Apr 2010, 2009, 2008
_e = line_no(F12, "Earnings per share from continuing operations:", 0, i0)
_, eps12 = row(F12, "Diluted", _e, _e + 3)
_, ocf12 = row(F12, "Operating activities", i0, i1 + 20)
_, capex12 = row(F12, "Expenditures for property, plant and equipment", i0, i1 + 20)
quote(F12, "Revenues—We had revenues of $45,352 million in 2012, $48,183 million in 2011 and $38,939 million in 2010.")
assert rev12[2] + rev12[3] == 38939
e12 = line_no(F12, "Potential dilutive shares")
_, sh12 = row(F12, "Potential dilutive shares", e12, e12 + 1)
s24 = line_no(F12, "Year EndedDecember 31, 2012")
_, cust12 = row(F12, "Customers", s24, s24 + 4)
s24b = line_no(F12, "Year EndedDecember 31, 2011")
_, cust12p = row(F12, "Customers", s24b, s24b + 4)
_, div12 = row(F12, "Dividends paid", line_no(F12, "Net cash provided by (used in) operating activities"),
               line_no(F12, "Net cash provided by (used in) operating activities") + 30)
WHY12 = quote(F12, "Our businesses’ results are impacted by seasonal effects and are highly cyclical.")
source("LB3", K12, "LyondellBasell Industries N.V. FY2012 10-K", F12,
       "FY2012 annual history: the selected financial data (revenues 2008-2012 from continuing operations, diluted EPS from "
       "continuing operations 2011-2012), the MD&A's combined 2010 revenues, the EPS note's diluted shares, the cash flow "
       "statement, the segment note (2011-2012 revenues from customers) and the risk factors")



def year_margins(path, pretax_label):
    """A 10-K's own year: pre-tax margin, tax rate and revenue growth from its statement of income (the vintage's last year)."""
    st = line_no(path, "CONSOLIDATED STATEMENTS OF INCOME")
    _, pt = row(path, pretax_label, st, st + 40)
    _, tx = row(path, "Provision for (benefit from) income taxes", st, st + 40)
    return pt[0], tx[0]


pt11, tx11 = year_margins(F11, "Income (loss) before income taxes")
pt12, tx12 = year_margins(F12, "Income from continuing operations before income taxes")
FYM = lambda fy, pt, tx, rv, prv, src: dict(
    prev_fy_op_margin=mg(pt, rv), prev_fy_op_margin_note=f"FY{fy % 100} income before income taxes {usd_m(pt)} / revenues {usd_m(rv)} ({src})",
    prev_fy_sales_growth=pct(prv, rv), check_pretax_margin=mg(pt, rv),
    check_pretax_note=f"FY{fy % 100} income before income taxes / revenues ({src})",
    tax_rate=round(tx / pt, 3), tax_note=f"FY{fy % 100} effective rate: provision for income taxes {usd_m(tx)} on {usd_m(pt)} ({src})")
THEMES = "; no theme in taxonomy_eras.json is live for a chemicals and refining company on this date"
NORM = ("diluted EPS from continuing operations, GAAP, each year from the latest filing that reports it (a release that republishes "
        "a year on a new basis restates it until the next 10-K); 2010 is two periods (the Predecessor to April 30, the Successor from "
        "May 1, after fresh-start accounting), with EPS for the Successor's eight months only, and is not a year of EPS")
EXCL10 = ("$2.67 a diluted share from continuing operations for May 1 to December 31, 2010 (FY2010 10-K: the Successor period after "
          "the emergence from bankruptcy), not a year; the Predecessor's January-April 2010 has no EPS")
base = dict(company="LyondellBasell Industries N.V.", exchange="NYSE", symbol="LYB", pe_window_start="2010-04-30",
            kind="CYCLICAL", kind_text="A cyclical commodity chemicals and refining company",
            business_line="Olefins and polyolefins, intermediates and derivatives, refining, technology",
            margin_signal_name="Pre-tax margin change", normalization=NORM)
seg_groups = lambda c, prior, names: [[n, round(v / 1000, 3), (pct(pv, v) if prior else None)]
                                      for n, v, pv in zip(names, c[:5], (prior or [None] * 5)[:5])]
V1 = dict(base, published=SRC["LB1"]["published"], sources=["LB1"], fy_label="FY10", fiscal_year_ends={"2010": "2010-12-31"},
          eps_normalized={}, eps_excluded={"2010": EXCL10},
          revenue_usd_b={"2006": rev10[5] / 1000, "2007": rev10[4] / 1000, "2008": rev10[3] / 1000, "2009": rev10[2] / 1000,
                         "2010": 41.151},
          revenue_sources={y: "LB1" for y in ("2006", "2007", "2008", "2009", "2010")},
          revenue_note="2010: the MD&A's combined Successor and Predecessor periods ($41,151M, its 'non-GAAP presentation'); "
                       "2006-2007: the Predecessor (2006 without Lyondell Chemical, 2007 with it from December 21)",
          diluted_shares_m={"2010": sh10[0]},
          shares_note="diluted weighted-average shares of the EPS note (2010: the Successor's May 1 to December 31); none before the emergence",
          prev_fy_op_margin=None, prev_fy_op_margin_note=None, prev_fy_sales_growth=None, check_pretax_margin=None,
          check_pretax_note=None, tax_rate=None, tax_note=None,
          dividend_annual=0.0, dividend_note="no dividend paid yet (FY2010 10-K: 'We have not yet paid any dividends on our shares.')",
          fcf_b=round((ocf10[0] + capex10[0]) / 1000, 3), fcf_label="May-Dec 2010",
          fcf_note=f"the Successor's net cash from operating activities {usd_m(ocf10[0])} less capital expenditures {usd_m(-capex10[0])} (FY2010 10-K)",
          cash_return_text="no dividends or share repurchases in 2010",
          groups=seg_groups(cust10, None, SEGN), groups_basis="May-Dec 2010 segment revenues from customers (FY2010 10-K, the Successor)",
          why=f"Risk factor (FY2010 10-K): {WHY10}" + THEMES)
assert abs(V1["revenue_usd_b"]["2008"] - 50.706) < 1e-9 and abs(V1["revenue_usd_b"]["2006"] - 13.175) < 1e-9
V2 = dict(base, published=SRC["LB2"]["published"], sources=["LB2", "LB1"], fy_label="FY11", fiscal_year_ends={"2011": "2011-12-31"},
          eps_normalized={"2011": eps11[0]}, eps_excluded={"2010": EXCL10},
          revenue_usd_b={"2006": rev10[5] / 1000, "2007": rev11[5] / 1000, "2008": rev11[4] / 1000, "2009": rev11[3] / 1000,
                         "2010": 41.151, "2011": rev11[0] / 1000},
          revenue_sources={"2006": "LB1", **{y: "LB2" for y in ("2007", "2008", "2009", "2010", "2011")}},
          revenue_note="2010: the MD&A's combined Successor and Predecessor periods ($41,151M); 2006 from the FY2010 10-K",
          diluted_shares_m={"2010": sh11[1], "2011": sh11[0]},
          shares_note="diluted weighted-average shares of the EPS note (2010: the Successor's May 1 to December 31)",
          **FYM(2011, pt11, tx11, rev11[0], 41151, "FY2011 10-K"),
          dividend_annual=0.25 * 4, dividend_note="$0.25 a quarter, the interim dividend paid December 16, 2011 (FY2011 10-K)",
          fcf_b=round((ocf11[0] + capex11[0]) / 1000, 3), fcf_label="FY11",
          fcf_note=f"net cash provided by operating activities {usd_m(ocf11[0])} less capital expenditures {usd_m(-capex11[0])} (FY2011 10-K)",
          cash_return_text=f"{usd_m(-div11[0])} of dividends paid in FY11 (with the $4.50 special dividend), no share repurchases",
          groups=seg_groups(cust11, None, SEGN), groups_basis="FY11 segment revenues from customers (FY2011 10-K)",
          why=f"Risk factor (FY2011 10-K): {WHY11}" + THEMES)
SEGN12 = SEGN[:3] + ["Refining"] + SEGN[4:]
V3 = dict(base, published=SRC["LB3"]["published"], sources=["LB3", "LB2", "LB1"], fy_label="FY12", fiscal_year_ends={"2012": "2012-12-31"},
          eps_normalized={"2011": eps12[1], "2012": eps12[0]}, eps_excluded={"2010": EXCL10},
          revenue_usd_b={"2006": rev10[5] / 1000, "2007": rev11[5] / 1000, "2008": rev12[5] / 1000, "2009": rev12[4] / 1000,
                         "2010": 38.939, "2011": rev12[1] / 1000, "2012": rev12[0] / 1000},
          revenue_sources={"2006": "LB1", "2007": "LB2", **{y: "LB3" for y in ("2008", "2009", "2010", "2011", "2012")}},
          revenue_note=("2008-2012 from continuing operations (the Berre refinery out), 2010 the MD&A's combined periods ($38,939M); "
                        "2006-2007 as the FY2010 and FY2011 10-Ks report them, with Berre (a seam)"),
          diluted_shares_m={"2010": sh12[4], "2011": sh12[2], "2012": sh12[0]},
          shares_note="diluted weighted-average shares of the EPS note (2010: the Successor's May 1 to December 31)",
          **FYM(2012, pt12, tx12, rev12[0], rev12[1], "FY2012 10-K"),
          dividend_annual=0.40 * 4, dividend_note="$0.40 a quarter, the interim dividend of 2012 (FY2012 10-K)",
          fcf_b=round((ocf12[0] + capex12[0]) / 1000, 3), fcf_label="FY12",
          fcf_note=f"net cash provided by operating activities {usd_m(ocf12[0])} less capital expenditures {usd_m(-capex12[0])} (FY2012 10-K)",
          cash_return_text=f"{usd_m(-div12[0])} of dividends paid in FY12 (with the $2.75 special dividend), no share repurchases",
          groups=seg_groups(cust12, cust12p, SEGN12), groups_basis="FY12 segment revenues from customers (FY2012 10-K)",
          why=f"Risk factor (FY2012 10-K): {WHY12}" + THEMES)
quote(F12, "We increased our interim dividend from $0.25 to $0.40 in the second quarter 2012;")
assert eps12[:2] == [4.96, 4.32] and sh12[0] == 577

# ── dividends: each declared interim rate from the first filing that states it (special dividends are not a rate) ──
F311Q, F212Q, FD8K = doc(Q311_10Q, "10-Q__"), doc(Q212_10Q, "10-Q__"), doc(DIV_8K, "8-K__")
source("LB20", Q311_10Q, "LyondellBasell Industries N.V. Q3 2011 10-Q", F311Q, "the dividend note: the $0.20 interim dividend of August 2011")
source("LB21", Q212_10Q, "LyondellBasell Industries N.V. Q2 2012 10-Q", F212Q, "the dividend note: the $0.40 interim dividend of May 2012")
source("LB30", DIV_8K, "LyondellBasell Industries N.V. 8-K (Items 5.07 and 8.01: the 2013 annual meeting)", FD8K,
       "the $0.50 interim dividend authorized for June 2013 and the share repurchase program of up to 10% of the shares")
dividends = [
    dict(published=SRC["LB20"]["published"], source="LB20", quarterly=0.20,
         note="$0.20 a quarter, the interim dividend of August 2011 (Q3 2011 10-Q)",
         quote=quote(F311Q, "In the first nine months of 2011, we paid cash dividends totaling $171 million, including dividends of $0.20 "
                            "and $0.10 per share of common stock, respectively, to shareholders of record on August 17, 2011 and May 5, 2011.")),
    dict(published=SRC["LB2"]["published"], source="LB2", quarterly=0.25,
         note="$0.25 a quarter, the interim dividend paid December 16, 2011 (FY2011 10-K)", quote=DIV25),
    dict(published=SRC["LB21"]["published"], source="LB21", quarterly=0.40,
         note="$0.40 a quarter, the interim dividend of June 2012 (Q2 2012 10-Q)",
         quote=quote(F212Q, "Dividend distribution—In June 2012, we paid a dividend to all shareholders of record as of May 11, 2012 of "
                            "$0.40 per share, for an aggregate of $230 million.")),
    dict(published=SRC["LB30"]["published"], source="LB30", quarterly=0.50,
         note="$0.50 a quarter, the interim dividend authorized for June 2013 (8-K of the 2013 annual meeting)",
         quote=quote(FD8K, "The dividend of $0.50 per share represents a 25% increase over the Company’s first quarter interim dividend")),
]
BUYBACK_Q = quote(FD8K, "Also on May 22, 2013, the Company announced that the Supervisory Board has approved a share repurchase program "
                        "for up to 10% of the Company’s outstanding shares")

# ── rule T: the annual year-on-year changes the filings public on the first date (2012-02-10) report: the FY2010 10-K (2006-2009,
# the 2010 periods, the MD&A's combined 2010) and the Q4 2011 release (2011, and 2010 combined as its tables print it) ──
fq4 = FREL["Q4 2011"]
seg08 = line_no(F10, "Segment operating income (loss)", 0, line_no(F10, "Customers | 13,193"))   # the segment note's 2008 table
_, s08 = row(F10, "Segment operating income (loss)", seg08, seg08 + 1)
# segment operating income 2009 and 2008 from the MD&A's segment tables (the two 2010 periods, 2009, 2008)
mda_opa = line_no(F10, "Operating income (loss) | 1,043 | 320 | 169 | (1,355)")
_, opa_mda = row(F10, "Operating income (loss)", mda_opa, mda_opa + 1)
mda_ind = line_no(F10, "Operating income (loss) | 512 | 157 | 250 | (1,915)")
_, ind_mda = row(F10, "Operating income (loss)", mda_ind, mda_ind + 1)
assert opa_mda[3] == s08[0] and ind_mda[3] == s08[2], (opa_mda, ind_mda, s08)
opa10c = tval(fq4, "Table 8", OPA, 2010, "YTD", section=SEG_SECTION)
ind10c = tval(fq4, "Table 8", IND, 2010, "YTD", section=SEG_SECTION)
opa11 = tval(fq4, "Table 8", OPA, 2011, "YTD", section=SEG_SECTION)
ind11 = tval(fq4, "Table 8", IND, 2011, "YTD", section=SEG_SECTION)
assert opa10c == opa_mda[0] + opa_mda[1] and ind10c == ind_mda[0] + ind_mda[1]
st = line_no(F10, "CONSOLIDATED STATEMENTS OF INCOME")
_, oi_st = row(F10, "Operating income (loss)", st, st + 30)
_, pti_st = row(F10, "Income (loss) from continuing operations before income taxes", st, st + 30)
rev11c, rev10c = tval(fq4, "Table 11", "Sales and other operating revenues", 2011, "YTD"), tval(fq4, "Table 11", "Sales and other operating revenues", 2010, "YTD")
oi11c, oi10c = tval(fq4, "Table 11", "Operating income", 2011, "YTD"), tval(fq4, "Table 11", "Operating income", 2010, "YTD")
pti11c, pti10c = pretax(fq4, 2011, "YTD"), pretax(fq4, 2010, "YTD")
assert (rev10c, oi10c) == (41151, 2944) and oi10c == oi_st[0] + oi_st[1]
REV = {2006: rev10[5], 2007: rev10[4], 2008: rev10[3], 2009: rev10[2], 2010: rev10c, 2011: rev11c}
OPM = {2008: mg(oi_st[3], rev10[3]), 2009: mg(oi_st[2], rev10[2]), 2010: mg(oi10c, rev10c), 2011: mg(oi11c, rev11c)}
PTM = {2008: mg(pti_st[3], rev10[3]), 2009: mg(pti_st[2], rev10[2]), 2010: mg(pti10c, rev10c), 2011: mg(pti11c, rev11c)}
SEG_OPA = {2008: opa_mda[3], 2009: opa_mda[2], 2010: opa10c, 2011: opa11}
SEG_IND = {2008: ind_mda[3], 2009: ind_mda[2], 2010: ind10c, 2011: ind11}
src_of = lambda y: "LB11" if y >= 2010 else "LB1"


def growth_vals(series):
    """Year-on-year growth between consecutive years; a change from a loss year is no growth rate and leaves rule T (the KMI rule)."""
    return {str(y): round((series[y] / series[y - 1] - 1) * 100, 1) for y in sorted(series) if y - 1 in series and series[y - 1] > 0}


def rule_t_entry(values, unit, note=None):
    v = sorted(values.values())
    n = len(v)
    med = v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
    worst, best = v[0], v[-1]
    r = lambda x: math.floor(x / unit + 0.5) * unit
    e = dict(values=values, sources={y: src_of(int(y)) for y in values}, unit=unit, lower_is_better=False,
             thresholds=dict(zip(("BEAR", "BASE", "BULL", "XBULL"), (r(worst + (worst - med)), r(worst), r(med), r(best)))))
    if note:
        e["note"] = note
    return e


rule_t = {
    "opa": rule_t_entry(growth_vals(SEG_OPA), 1, "2009 against 2008's loss (goodwill impairments, FY2010 10-K: $(1,355)M) is no growth "
                                                 "rate; 2010 is the combined periods as the Q4 2011 release prints them"),
    "ind": rule_t_entry(growth_vals(SEG_IND), 1, "2009 against 2008's loss (goodwill impairments, FY2010 10-K: $(1,915)M) is no growth rate"),
    "revenue": rule_t_entry(growth_vals(REV), 1, "2006-2007: the Predecessor (Basell; Lyondell Chemical from December 21, 2007)"),
    "op_margin": rule_t_entry({str(y): round((OPM[y] - OPM[y - 1]) * 100, 1) for y in sorted(OPM) if y - 1 in OPM}, 10),
    "pretax_margin": rule_t_entry({str(y): round((PTM[y] - PTM[y - 1]) * 100, 1) for y in sorted(PTM) if y - 1 in PTM}, 10,
                                  "income from continuing operations before income taxes on revenues, reorganization items in, as "
                                  "reported (2010's $7,365M combined: the discharge of liabilities and fresh-start accounting)"),
}
quote(fq4, "Comparisons with the prior quarter, fourth quarter 2010 and full year 2010 are available in the following table.")

listing = dict(first_trading_day="2010-04-30", exchange="NYSE", symbol="LYB", published=SRC["LB1"]["published"], source="LB1",
               note=("LyondellBasell Industries N.V.'s shares were issued on April 30, 2010, at the emergence from bankruptcy, quoted on the "
                     "Pink Sheets to October 13, 2010 and listed on the NYSE as LYB from October 14, 2010 (FY2010 10-K, Item 5: "
                     f"'{ISSUEQ}' '{LISTQ}'); the P/E exists only from the first day (the listing rule of method r2). Yahoo's LYB series "
                     "starts on 2010-04-28, two days before the capital was issued: those two points are left out"))

facts = dict(
    _doc=("LyondellBasell Industries N.V. (NYSE: LYB), point-in-time facts for retro/build_lyb.py. Every value carries its source and "
          "the source's publication date (EDGAR acceptance time; at or after the 16:00 ET close it counts from the next trading day). "
          "Generated by retro/generators/lyb/gen_lyb.py from the filings' converted rows: each figure is read from its labelled row, "
          "the row is asserted present in its own filing, and every rate, margin, tax rate and rule-T value is computed."),
    ticker="LYB", sources=dict(sorted(SRC.items(), key=lambda kv: (kv[1]["published"], kv[0]))), listing=listing, distributions=[],
    history_vintages=[V1, V2, V3], prints=prints, guides=[], dividends=dividends, events=[], company_names=[],
    buyback_programs=[dict(published=SRC["LB30"]["published"], source="LB30", quote=BUYBACK_Q,
                           note="display only: the diluted share counts carry its effect",
                           text="a share repurchase program for up to 10% of the shares from May 2013")],
    rule_t=rule_t)

out = A.out or os.path.join(REPO, "retro", "facts", "LYB.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(facts, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_lyb.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump({k: sorted(set(v)) for k, v in CHECK.items()}, fh, indent=1, ensure_ascii=False)
print(f"wrote {out}: {len(prints)} prints, 3 vintages, {len(dividends)} dividends; checklist {ck} "
      f"({sum(len(set(v)) for v in CHECK.values())} strings)")
for k, e in rule_t.items():
    print(f"  rule T {k}: {e['values']} -> {e['thresholds']}")
for p in prints:
    print(f"  {p['quarter']} {p['published']} rev {p['sales_pct']:+.1f}% opm {p['opm_bp']:+.0f}bp ptm {p['ptm_bp']:+.0f}bp "
          f"O&P-A {p['opa_pct']} I&D {p['ind_pct']} eps {p['eps_q']} vs {p['eps_q_prior']} sh {p['diluted_shares_m']} | {p['release_time']}")
