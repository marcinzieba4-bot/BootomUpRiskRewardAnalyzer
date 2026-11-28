#!/usr/bin/env python3
"""Generate retro/facts/LYB.json (2012-02-10 to 2026-11-20) from LyondellBasell Industries N.V.'s own filings (edgar.py's rows).

Every raw figure is read from its own labelled row (the row is kept for the verbatim checklist), every rate, margin, tax rate
and rule-T value is computed, every quoted sentence is asserted present in its own filing. Only filings accepted on or before
2026-11-22 are read. The downloads (keep them outside the repository):

    python3 retro/tools/edgar.py index 1489393 <dir>
    python3 retro/tools/edgar.py fetch 1489393 <dir> --from 2010-04-01 --to 2026-11-27 --forms 10-K 10-Q 8-K 8-K/A 10-12B 10-12B/A

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
CUT = "2026-11-22"
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
# the FY2010 revisions (the 8-K of 2011-06-22's guarantor note; the 8-K/A of 2011-08-15's Revisions I and II; the 8-K of 2011-10-21's
# MD&A) change the Predecessor's January-April 2010 reorganization items, taxes and balance sheet only: every figure the FY2010 vintage
# gives a model is identical in the revised statements, so they add nothing (asserted here; rule T takes 2010 from the Q4 2011 release)
F10R = doc("0000950123-11-077060", "EX-99.1__")
quote(doc("0000950123-11-077060", "8-K_A__"), "This Form 8-K/A updates the Current Report on Form 8-K of LyondellBasell Industries N.V. (the “Company”) filed on June 22, 2011")
_r = line_no(F10R, "Dilutive potential shares")
assert row(F10R, "Dilutive potential shares", _r, _r + 1)[1] == sh10
_r = line_no(F10R, "Net cash provided by (used in) operating activities")
assert row(F10R, "Net cash provided by (used in) operating activities", _r, _r + 1)[1][0] == ocf10[0]
_r = line_no(F10R, "Expenditures for property, plant and equipment")
assert row(F10R, "Expenditures for property, plant and equipment", _r, _r + 1)[1][0] == capex10[0]
_r = line_no(F10R, "Customers | 5,993")
assert row(F10R, "Customers", _r, _r + 1)[1] == cust10
_r = line_no(F10R, "Operating income (loss) | 2,254")
assert row(F10R, "Operating income (loss)", _r, _r + 1)[1] == [2254, 690, 317, -5928]
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

# ══ 2014-2017: the Q4 2013 to Q3 2017 releases, the FY2013-FY2016 10-Ks, the dividends and repurchase authorities to 2017-12-31 ══
# (added for retro/README.md, "LYB 2014-2017"; everything above is unchanged, so the 2012-2013 facts regenerate byte for byte).
# The releases' tables are renumbered from Q1 2014 (Table 7 the segment reconciliation, Table 10 the income statement, Table 11 the
# charges), so these are found by their titles, not their numbers; the segment names are matched with their dashes normalized.
REL2 = {"Q4 2013": "0001193125-14-029894", "Q1 2014": "0001193125-14-165167", "Q2 2014": "0001193125-14-279747",
        "Q3 2014": "0001193125-14-380926", "Q4 2014": "0001193125-15-030610", "Q1 2015": "0001193125-15-145163",
        "Q2 2015": "0001193125-15-264845", "Q3 2015": "0001193125-15-351254", "Q4 2015": "0001193125-16-446746",
        "Q1 2016": "0001193125-16-551100", "Q2 2016": "0001193125-16-663276", "Q3 2016": "0001193125-16-754456",
        "Q4 2016": "0001193125-17-029768", "Q1 2017": "0001193125-17-145129", "Q2 2017": "0001193125-17-239266",
        "Q3 2017": "0001193125-17-321949", "Q4 2017": "0001193125-18-029923"}   # Q4 2017: added for "LYB 2018-2021"
SID2 = {q: f"LB{40 + i}" for i, q in enumerate(REL2)}
FREL2 = {q: doc(a, "EX-99.1__") for q, a in REL2.items()}
TOTALS = ("Total", "YTD", "AnnualImpact", "Impact")
dnorm = lambda s: re.sub(r"\s*[-–—]\s*", "-", s)
nofoot = lambda s: re.sub(r"(\s*\([a-z](, [a-z])*\))+$|\d$", "", s.strip()).strip()   # '..operations(b)', '(a, b)', '(a) (b)', 'LCM1'


def title_line(path, title):
    hits = [i for i, x in enumerate(lines(path)) if re.match(r"Table \d+\s*[-–—]\s*" + re.escape(title), x)]
    assert len(hits) == 1, (path, title, hits)
    return hits[0]


def row2(path, label, start, stop):
    """The unique row in lines[start:stop] whose first cell, footnote marks dropped and dashes normalized, is `label`."""
    L = lines(path)[start:stop]
    hits = [x for x in L if "|" in x and dnorm(nofoot(x.split(" |")[0])) == dnorm(label)]
    assert len(hits) == 1, (path, label, len(hits), hits[:3], start, stop)
    CHECK.setdefault(path, []).append(hits[0])
    return hits[0], [num(t) for t in cells(hits[0]) if t]


def qtable(path, title):
    """(start, stop, columns) of a quarterly table (a year row, then a header of Q1 .. Q4, Total/YTD/AnnualImpact, Q1 ..)."""
    i0 = title_line(path, title)
    L = lines(path)
    stop = next((i for i in range(i0 + 1, len(L)) if re.match(r"Table \d+\s*[-–—]", L[i])), len(L))
    yi = next(i for i in range(i0, i0 + 6) if re.fullmatch(r"20\d\d \| 20\d\d", L[i]))
    years = [int(y) for y in L[yi].split(" | ")]
    hi = next(i for i in range(yi, yi + 4) if L[i].startswith(("(Millions of U.S. dollars)", "Millions of U.S. dollars")))
    labels = [c.strip() for c in L[hi].split("|")[1:]]
    k = next(j for j, lb in enumerate(labels) if lb in TOTALS) + 1
    cols = [(years[0], lb) for lb in labels[:k]] + [(years[1], lb) for lb in labels[k:]]
    return hi, stop, cols


def qval(path, title, label, year, col, section=None):
    hi, stop, cols = qtable(path, title)
    if col == "TOTAL":
        col = next(c for y, c in cols if y == year and c in TOTALS)
    start = hi
    if section:
        start = line_no(path, section[0], 0, hi)
        stop = line_no(path, section[1], 0, start)
    _, v = row2(path, label, start, stop)
    assert len(v) == len(cols), (path, title, label, v, cols)
    return v[cols.index((year, col))]


def t1b(path):
    """Table 1 (Earnings Summary): its first block only (the 'Excluding LCM Impact' block below it is the company's adjusted view);
    cells are the quarter, the previous quarter, the year-ago quarter, then the year to date (this year, last year)."""
    i0 = title_line(path, "Earnings Summary")
    L = lines(path)
    i1 = next(i for i in range(i0, i0 + 30) if L[i].startswith(("Excluding LCM", "(a) |")))
    _, rev = row2(path, "Sales and other operating revenues", i0, i1)
    shl = next(x for x in ("Diluted share count (millions)", "Diluted share count (weighted average in millions)")   # Q4 2017: the latter
               if any("|" in y and dnorm(nofoot(y.split(" |")[0])) == x for y in lines(path)[i0:i1]))
    _, sh = row2(path, shl, i0, i1)
    hdr = [i for i in range(i0, i1) if L[i].startswith("Diluted earnings per share (U.S. dollars):")]
    assert len(hdr) == 1, (path, hdr)
    _, eps = row2(path, "Income from continuing operations", hdr[0], hdr[0] + 4)
    _, ebitda = row2(path, "EBITDA", i0, i1)
    return rev, eps, sh, ebitda


INC, SEGT = "Unaudited Income Statement Information", "Reconciliation of Segment Information to Consolidated Financial Information"
PRETAX2 = ("Income from continuing operations before income taxes", "Income before taxes")
OPA2 = "Olefins & Polyolefins-Americas"


def pretax2(path, year, col):
    for lab in PRETAX2:
        try:
            return qval(path, INC, lab, year, col)
        except AssertionError:
            pass
    raise AssertionError((path, "pre-tax", year, col))


ORDER2 = list(REL2)
for qi, (qq, acc) in enumerate(REL2.items()):
    q, fy = int(qq[1]), int(qq[3:])
    f = FREL2[qq]
    rev, eps, sh, ebitda = t1b(f)
    qc = f"Q{q}"
    oi, oi_p = qval(f, INC, "Operating income", fy, qc), qval(f, INC, "Operating income", fy - 1, qc)
    pti, pti_p = pretax2(f, fy, qc), pretax2(f, fy - 1, qc)
    assert rev[0] == qval(f, INC, "Sales and other operating revenues", fy, qc), qq
    assert rev[2] == qval(f, INC, "Sales and other operating revenues", fy - 1, qc), qq
    opa, opa_p = (qval(f, SEGT, OPA2, fy, qc, section=SEG_SECTION), qval(f, SEGT, OPA2, fy - 1, qc, section=SEG_SECTION))
    ind, ind_p = (qval(f, SEGT, IND, fy, qc, section=SEG_SECTION), qval(f, SEGT, IND, fy - 1, qc, section=SEG_SECTION))
    pub, filed = published(acc)
    title = f"LyondellBasell Industries N.V. {qq} results (8-K, Exhibit 99.1)"
    sid = source(SID2[qq], acc, title, f, "the quarter's Table 1 (revenues, diluted EPS from continuing operations, diluted shares), "
                 "the segment reconciliation (segment operating income) and the income statement table, each with the year-ago quarter "
                 "as this release shows it")
    raw = dict(rev_m=rev[0], rev_prior_m=rev[2], oi_m=oi, oi_prior_m=oi_p, pti_m=pti, pti_prior_m=pti_p, eps_q=eps[0], eps_q_prior=eps[2],
               dil_sh_m=sh[0], opa_m=opa, opa_prior_m=opa_p, ind_m=ind, ind_prior_m=ind_p, ebitda_m=ebitda[0])
    rel_day = dt.date.fromisoformat(FILINGS[acc][1][:10])
    nq = ORDER2[qi + 1] if qi + 1 < len(ORDER2) else "Q1 2018"
    basis = "diluted from continuing operations"
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
        pti_y = pretax2(f, fy, "TOTAL")
        tax_y = qval(f, INC, "Provision for (benefit from) income taxes" if fy == 2017 else "Provision for income taxes", fy, "TOTAL")
        ni_att = qval(f, INC, "Net income attributable to the Company shareholders", fy, "TOTAL")
        assert rev[3] == qval(f, INC, "Sales and other operating revenues", fy, "TOTAL"), qq
        if fy == 2013:      # the Q4 2013 release's charges table has the layout of Table 1 (the year in its fourth cell)
            i2 = title_line(f, "Charges (Benefits) Included in Net Income")
            lab2, items = "After-tax effect of net charges (credits)", row2(f, "After-tax effect of net charges (credits)", i2, i2 + 20)[1][3]
            ttl = "Charges (Benefits) Included in Net Income"
        else:
            ttl = "Charges (Benefits) Included in Income from Continuing Operations"
            lab2 = "After-tax effect of net charges (benefits)"
            items = qval(f, ttl, lab2, fy, "TOTAL")
        prev_rev = rev[4]
        kind = "charges" if items >= 0 else "benefits"
        test_note = (f"the release's '{ttl}' table: '{lab2}' of {usd_m(items)} for the year (every item that table lists, charges net "
                     "of benefits, recurring ones such as the lower of cost or market inventory adjustments included where listed) against "
                     "net income attributable "
                     f"to the Company of {usd_m(ni_att)}: kept at GAAP; the net is a charge, so the mirror test does not arise")
        if kind == "benefits":     # FY2017 (U.S. tax reform): the mirror of the AAPL FY2002 test (retro/README.md, "LYB 2018-2021")
            test_note = (f"the release's '{ttl}' table: '{lab2}' of {usd_m(items)} for the year (every item that table lists, the "
                         "U.S. tax reform benefit among them), a net benefit, against net income attributable to the Company of "
                         f"{usd_m(ni_att)}: the mirror test (the benefit against the income without it, {usd_m(ni_att + items)}) is not "
                         "met, so the year is kept at GAAP")
        dist = (-items > ni_att + items) if kind == "benefits" else (items > ni_att)
        a = dict(fy=fy, fy_label=f"FY{fy % 100}", eps_normalized=eps[3], excluded_note=None, revenue_usd_b=round(rev[3] / 1000, 3),
                 diluted_shares_m=sh[3],
                 normalization_note=f"FY{fy % 100} ${eps[3]:.2f} {basis} from the {qq} release ({pub}) until the 10-K",
                 op_margin=mg(pti_y, rev[3]),
                 op_margin_note=f"FY{fy % 100} income before income taxes {usd_m(pti_y)} / revenues {usd_m(rev[3])} ({qq} release)",
                 sales_growth=pct(prev_rev, rev[3]),
                 check_pretax_margin=mg(pti_y, rev[3]),
                 check_pretax_note=f"FY{fy % 100} income before income taxes / revenues ({qq} release)",
                 tax_rate=round(tax_y / pti_y, 3), tax_note=f"FY{fy % 100} effective rate: provision for income taxes {usd_m(tax_y)} on {usd_m(pti_y)}",
                 one_off_test=dict(items_after_tax_m=items, income_attributable_m=ni_att, distorted=dist, kind=kind, note=test_note))
        p["fy_actual"] = a
    prints.append(p)

# the releases' company figures excluding the lower of cost or market adjustments (Table 1's 'Excluding LCM Impact' block, from Q4 2014)
# remove an item that recurs in nine of the twelve quarters from Q3 2014 to Q2 2017, so they are not figures excluding only one-offs
# (the NKE FY2007, AVGO, PFE and V rule, as for the 2011-2013 adjusted EPS); GAAP stands. Asserted here, shown in the README only.
for qq in ("Q4 2014", "Q4 2015", "Q4 2016"):
    quote(FREL2[qq], "Excluding LCM Impact:")

# ── the FY2013-FY2016 10-Ks ──
K13, K14, K15, K16 = "0001193125-14-060399", "0000950123-15-003039", "0001193125-16-465311", "0001193125-17-047661"
F13, F14, F15, F16 = doc(K13, "10-K__"), doc(K14, "10-K__"), doc(K15, "10-K__"), doc(K16, "10-K__")
CYCQ = "Our business operations are subject to the cyclical and volatile nature of the supply-demand balance in the chemical and refining industries."
GHGQ = ("Compliance with these or other changes in laws, regulations and obligations that create a GHG emissions trading scheme or GHG "
        "reduction policies generally could significantly increase our costs or reduce demand for products we produce.")


def tenk(path, acc, sid, fy, title):
    """One 10-K vintage's figures: Item 6 (five years of revenues and diluted EPS from continuing operations, the two 2010 periods where
    shown), the EPS note's diluted shares (three years), the statement of income's pre-tax income and tax, the cash flow statement's
    dividends and repurchases, the segment note's revenues from customers (this year and last), and its own words."""
    i0, i1 = sel(path)
    _, rv = row(path, "Sales and other operating revenues", i0, i1)
    _e = line_no(path, "Earnings per share from continuing operations:", 0, i0)
    _, ep = row(path, "Diluted", _e, _e + 3)
    _, ocf = row(path, "Operating activities", i0, i1 + 20)
    _, capex = row(path, "Expenditures for property, plant and equipment", i0, i1 + 20)
    hdr = next(x for x in lines(path)[i0:i0 + 8] if x.startswith("In millions of dollars, except per share data"))
    yrs = [int(c) for c in cells(hdr)]
    e = line_no(path, "Potential dilutive shares")
    _, shr = row(path, "Potential dilutive shares", e, e + 1)
    st = line_no(path, "CONSOLIDATED STATEMENTS OF INCOME")
    _, pt = row(path, "Income from continuing operations before income taxes", st, st + 40)
    _, tx = row(path, "Provision for income taxes", st, st + 40)
    cf = line_no(path, "Cash flows from financing activities:")
    _, rep = row(path, "Repurchases of Company ordinary shares", cf, cf + 4)
    _, dvp = row(path, "Dividends paid", cf, cf + 4)
    s24 = line_no(path, f"Year Ended December 31, {fy}", 0, line_no(path, "Potential dilutive shares"))
    _, cust = row(path, "Customers", s24, s24 + 4)
    s24p = line_no(path, f"Year Ended December 31, {fy - 1}", 0, s24)
    _, custp = row(path, "Customers", s24p, s24p + 4)
    assert cust[6] == rv[0] and custp[6] == rv[1], (fy, cust, custp, rv)
    m = re.search(r"Refining\. Our Refining segment refines[^•]*?\.(?= •|$)", norm(" ".join(lines(path))))
    refq = quote(path, m.group(0))
    source(sid, acc, title, path,
           f"FY{fy} annual history: the selected financial data (revenues and diluted EPS from continuing operations, five years), the "
           "EPS note's diluted shares, the statements of income and cash flows, the segment note (revenues from customers), the "
           "dividend increase and the risk factors (cyclicality, greenhouse gas regulation) and Item 1's segment description")
    return dict(rv=dict(zip(yrs, rv)), ep=dict(zip(yrs, ep)), ocf=ocf[0], capex=capex[0], sh={fy: shr[0], fy - 1: shr[2], fy - 2: shr[4]},
                pt=pt[0], tx=tx[0], rep=rep[0], dvp=dvp[0], cust=cust, custp=custp, why=quote(path, CYCQ), ghg=quote(path, GHGQ),
                refq=refq, pub=SRC[sid]["published"])


T13 = tenk(F13, K13, "LB4", 2013, "LyondellBasell Industries N.V. FY2013 10-K")
T14 = tenk(F14, K14, "LB5", 2014, "LyondellBasell Industries N.V. FY2014 10-K")
T15 = tenk(F15, K15, "LB6", 2015, "LyondellBasell Industries N.V. FY2015 10-K")
T16 = tenk(F16, K16, "LB7", 2016, "LyondellBasell Industries N.V. FY2016 10-K")
# Item 6 of the FY2013 and FY2014 10-Ks shows 2010 as its two periods (columns of the same year): their sum is the combined year the
# FY2012 10-K's MD&A printed, which stays the 2010 revenue (the latest filing that prints the combined year)
for path in (F13, F14):
    i0, i1 = sel(path)
    _, rv = row(path, "Sales and other operating revenues", i0, i1)
    hdr = next(x for x in lines(path)[i0:i0 + 8] if x.startswith("In millions of dollars, except per share data"))
    yrs = [int(c) for c in cells(hdr)]
    assert sum(v for y, v in zip(yrs, rv) if y == 2010) == 38939, path
assert T13["rv"][2009] == rev12[4] and T13["ep"][2011] == 4.32 and T13["ep"][2012] == 4.96
assert [T13["ep"][2013], T14["ep"][2014], T15["ep"][2015], T16["ep"][2016]] == [6.76, 8.00, 9.60, 9.15]
DIVQ = {2013: quote(F13, "We increased our interim dividends in 2013 from $0.40 to $0.60;"),
        2014: quote(F14, "We increased our interim dividends in 2014 from $0.60 to $0.70;"),
        2015: quote(F15, "We increased our interim dividend in 2015 from $0.70 to $0.78;"),
        2016: quote(F16, "We increased our interim dividend from $0.78 to $0.85 in May 2016;")}
DIVR = {2013: 0.60, 2014: 0.70, 2015: 0.78, 2016: 0.85}


def vintage(prev, t, fy, sid):
    """The next vintage: each year from the latest filing that reports it, the ten fiscal years to the latest one."""
    rv = {k: v for k, v in prev["revenue_usd_b"].items()}
    rs = dict(prev["revenue_sources"])
    for y, v in t["rv"].items():
        if y == 2010:
            continue                                  # the two periods; the combined year stays (asserted above)
        rv[str(y)], rs[str(y)] = v / 1000, sid
    keep = [str(y) for y in range(fy - 9, fy + 1)]
    rv = {y: rv[y] for y in keep if y in rv}
    rs = {y: rs[y] for y in rv}
    eps = dict(prev["eps_normalized"])
    eps.update({str(y): v for y, v in t["ep"].items() if y >= 2011})
    sh = dict(prev["diluted_shares_m"])
    sh.update({str(y): v for y, v in t["sh"].items()})
    srcs = [sid] + [s for s in dict.fromkeys(rs.values()) if s != sid]
    return dict(base, published=t["pub"], sources=srcs, fy_label=f"FY{fy % 100}", fiscal_year_ends={str(fy): f"{fy}-12-31"},
                eps_normalized=eps, eps_excluded={"2010": EXCL10},
                revenue_usd_b=rv, revenue_sources=rs,
                revenue_note=(f"{min(int(y) for y, s in rs.items() if s == sid)}-{fy} from the FY{fy} 10-K (continuing operations), "
                              "2010 the FY2012 10-K's combined periods ($38,939M; the later 10-Ks show its two periods, which sum to it), "
                              "earlier years from the latest earlier 10-K that reports them (2006-2007 with Berre, a seam); the ten "
                              "fiscal years to the latest one"),
                diluted_shares_m=sh,
                shares_note="diluted weighted-average shares of the EPS note (2010: the Successor's May 1 to December 31)",
                **FYM(fy, t["pt"], t["tx"], t["rv"][fy], t["rv"][fy - 1], f"FY{fy} 10-K"),
                dividend_annual=round(DIVR[fy] * 4, 2),
                dividend_note=f"${DIVR[fy]:.2f} a quarter, the interim dividend of {fy} (FY{fy} 10-K: '{DIVQ[fy]}')",
                fcf_b=round((t["ocf"] + t["capex"]) / 1000, 3), fcf_label=f"FY{fy % 100}",
                fcf_note=f"net cash provided by operating activities {usd_m(t['ocf'])} less capital expenditures {usd_m(-t['capex'])} (FY{fy} 10-K)",
                cash_return_text=(f"{usd_m(-t['dvp'])} of dividends paid and {usd_m(-t['rep'])} of share repurchases in FY{fy % 100}"
                                  if t["rep"] else f"{usd_m(-t['dvp'])} of dividends paid in FY{fy % 100}, no share repurchases"),
                groups=seg_groups(t["cust"], t["custp"], SEGN12), groups_basis=f"FY{fy % 100} segment revenues from customers (FY{fy} 10-K)",
                why=f"Risk factor (FY{fy} 10-K): {t['why']}" + THEMES,
                refining_quote=t["refq"], transition_quote=t["ghg"], tenk_label=f"FY{fy} 10-K")


V4 = vintage(V3, T13, 2013, "LB4")
V5 = vintage(V4, T14, 2014, "LB5")
V6 = vintage(V5, T15, 2015, "LB6")
V7 = vintage(V6, T16, 2016, "LB7")
assert "2006" in V6["revenue_usd_b"] and "2006" not in V7["revenue_usd_b"]

# ── dividends: each declared interim rate from the first filing that states it (the Q4 2013 to Q2 2017 releases) ──
DIV2 = [("Q4 2013", 0.60, "Increased interim dividend by 20 percent to $0.60 per share"),
        ("Q1 2014", 0.70, "the Supervisory Board approved a 10 cent per share increase of the quarterly interim dividend to $0.70 per share"),
        ("Q2 2015", 0.78, "Increased the interim quarterly dividend by 11 percent to 78 cents per share"),
        ("Q2 2016", 0.85, "Increased second quarter 2016 interim dividend by 9% to $0.85 per share"),
        ("Q2 2017", 0.90, "Increased second quarter 2017 dividend by 6% to $0.90 per share")]
for qq, rate, s in DIV2:
    dividends.append(dict(published=SRC[SID2[qq]]["published"], source=SID2[qq], quarterly=rate,
                          note=f"${rate:.2f} a quarter, the interim dividend increase announced in the {qq} release",
                          quote=quote(FREL2[qq], s)))

# ── repurchase authorities: each annual meeting's approval (Item 5.07), display only (the share counts carry their effect) ──
BB2 = [("LB31", "0001193125-14-151137", "2014"), ("LB32", "0001193125-15-183388", "2015"), ("LB33", "0001193125-16-591840", "2016"),
       ("LB34", "0001193125-17-189202", "2017")]
buybacks2 = []
for sid, acc, yr in BB2:
    fb = doc(acc, "8-K__")
    source(sid, acc, f"LyondellBasell Industries N.V. 8-K (Item 5.07: the {yr} annual meeting)", fb,
           "the shareholders' approval of the authority to repurchase up to 10% of the shares")
    buybacks2.append(dict(published=SRC[sid]["published"], source=sid,
                          quote=quote(fb, "The approval of the authority of the Management Board, acting with the approval of the "
                                          "Supervisory Board, to repurchase up to 10% of the Company’s shares was approved"),
                          note="display only: the diluted share counts carry its effect",
                          text=f"the {yr} annual meeting's authority to repurchase up to 10% of the shares"))

# ══ 2018-2021: the Q1 2018 to Q3 2021 releases, the FY2017-FY2020 10-Ks, the dividends and repurchase authorities to 2021-12-31 ══
# (added for retro/README.md, "LYB 2018-2021"; everything above is unchanged but Q4 2017, the last release in the 2014-2017 layout, which
# joins REL2, so the 2012-2017 facts regenerate byte for byte). From Q1 2018 the releases drop the income statement and charges tables:
# Table 1 gives revenues, net income, diluted EPS (on net income) and diluted shares; the EBITDA reconciliation gives income from continuing
# operations and the provision for income taxes (their sum is the pre-tax income); segment operating income is in the segment overview
# tables (Q1-Q2 2018; from Q2 2021 in Exhibit 99.2) or the segment reconciliation (Q3 2018 to Q1 2021), whose 'Continuing Operations'
# row is the consolidated operating income. Where the release prints no consolidated operating income (Q1 and Q2 2018, Q2 and Q3 2021),
# it comes from the quarter's 10-Q, accepted the same day during the session ('oi_source'), with the year-ago quarter as that 10-Q shows it.
REL3 = {"Q1 2018": ("0001193125-18-136586", "0001193125-18-137643"), "Q2 2018": ("0001489393-18-000008", "0001489393-18-000012"),
        "Q3 2018": ("0001489393-18-000017", None), "Q4 2018": ("0001489393-19-000003", None),
        "Q1 2019": ("0001489393-19-000020", None), "Q2 2019": ("0001489393-19-000042", None),
        "Q3 2019": ("0001489393-19-000064", None), "Q4 2019": ("0001489393-20-000004", None),
        "Q1 2020": ("0001489393-20-000027", None), "Q2 2020": ("0001489393-20-000048", None),
        "Q3 2020": ("0001489393-20-000064", None), "Q4 2020": ("0001489393-21-000003", None),
        "Q1 2021": ("0001489393-21-000012", None), "Q2 2021": ("0001489393-21-000037", "0001489393-21-000039"),
        "Q3 2021": ("0001489393-21-000044", "0001489393-21-000046")}
SID3 = {q: f"LB{60 + i}" for i, q in enumerate(REL3)}
QSID = {"Q1 2018": "LB80", "Q2 2018": "LB81", "Q2 2021": "LB82", "Q3 2021": "LB83"}
FREL3 = {q: doc(a, "EX-99__" if q == "Q4 2018" else "EX-99.1__") for q, (a, _) in REL3.items()}
FSEG3 = {q: doc(a, "EX-99.2__") for q, (a, _) in REL3.items() if q in ("Q2 2021", "Q3 2021")}   # the business results exhibit
YEARROW = re.compile(r"20\d\d( \| 20\d\d)?")


def table_at(path, title, exact=False):
    """(start, stop) of the table whose title line is 'Table N - <title>' (exactly, when `exact`); stop at the next table."""
    L = lines(path)
    pat = re.compile(r"Table \d+\s*[-–—]\s*" + re.escape(title) + (r"\s*$" if exact else ""))
    hits = [i for i, x in enumerate(L) if pat.match(x)]
    assert len(hits) == 1, (path, title, hits)
    i0 = hits[0]
    stop = next((i for i in range(i0 + 1, len(L)) if re.match(r"Table \d+\s*[-–—]", L[i])), len(L))
    return i0, stop


def five(path, title, label, start=None, stop=None):
    """A row of a table laid out as the quarter, the previous quarter, the year-ago quarter (then year to date, this year and last)."""
    i0, i1 = table_at(path, title) if start is None else (start, stop)
    _, v = row2(path, label, i0, i1)
    assert len(v) in (3, 5), (path, title, label, v)
    return v


def first_label(path, i0, i1, labels):
    have = [x for x in labels if any("|" in y and dnorm(nofoot(y.split(" |")[0])) == dnorm(x) for y in lines(path)[i0:i1])]
    assert len(have) == 1, (path, labels, have)
    return have[0]


def earnings3(path):
    """Table 1 (Earnings Summary), its first block (the 'Excluding LCM' block below it is the company's adjusted view)."""
    i0, i1 = table_at(path, "Earnings Summary")
    i1 = next((i for i in range(i0, i1) if lines(path)[i].startswith(("Excluding", "(a)"))), i1)
    rev = five(path, None, "Sales and other operating revenues", i0, i1)
    ni = five(path, None, "Net income", i0, i1)
    eps = five(path, None, first_label(path, i0, i1, ("Diluted earnings per share", "Diluted earnings per share (U.S. dollars)")), i0, i1)
    sh = five(path, None, first_label(path, i0, i1, ("Weighted average diluted share count",
                                                    "Weighted average diluted share count (millions)")), i0, i1)
    eb = five(path, None, "EBITDA", i0, i1)
    return rev, ni, eps, sh, eb


def recon_block(path):
    """The EBITDA reconciliation's first block: (start, stop, columns or None for the five-column layout)."""
    L = lines(path)
    i0, i1 = table_at(path, "Reconciliation of Net Income to EBITDA")
    yi = next((i for i in range(i0 + 1, i0 + 4) if YEARROW.fullmatch(L[i])), None)
    if yi is None:                                        # Q2 and Q3 2021: Three Months Ended | Six (Nine) Months Ended
        return i0, i1, None
    years = [int(y) for y in L[yi].split(" | ")]
    hi = yi + 1
    labels = [c.strip() for c in L[hi].split("|")[1:]]
    k = next(j for j, lb in enumerate(labels) if lb in TOTALS) + 1
    cols = [(years[0], lb) for lb in labels[:k]] + [(years[1], lb) for lb in labels[k:]]
    stop = next((i for i in range(hi + 1, i1) if YEARROW.fullmatch(L[i])), i1)    # Q3 2018: a 2016 block follows
    return hi, stop, cols


def recon_val(path, label, year, col):
    hi, stop, cols = recon_block(path)
    alts = {"Provision for (benefit from) income taxes": ("Provision for (benefit from) income taxes", "Provision for income taxes")}
    lab = first_label(path, hi, stop, alts.get(label, (label,)))           # Q1 2020: 'Provision for income taxes'
    _, v = row2(path, lab, hi, stop)
    if cols is None:                                      # col: 0 the quarter, 2 the year-ago quarter
        assert len(v) == 5, (path, label, v)
        return v[col]
    if col == "TOTAL":
        col = next(c for y, c in cols if y == year and c in TOTALS)
    assert len(v) == len(cols), (path, label, v, cols)
    return v[cols.index((year, col))]


def pretax3(path, fy, q, prior=False):
    """Income from continuing operations plus the provision for (benefit from) income taxes, from the EBITDA reconciliation."""
    _, _, cols = recon_block(path)
    y, c = (fy - 1 if prior else fy), (f"Q{q}" if q else "TOTAL")
    if cols is None:
        c = 2 if prior else 0
    inc = recon_val(path, "Income from continuing operations", y, c)
    tax = recon_val(path, "Provision for (benefit from) income taxes", y, c)
    return inc + tax, tax


SEGREC = "Reconciliation of Segment Information to Consolidated Financial Information"


def seg3(qq, path, label):
    """A segment's (or the consolidated, label 'Continuing Operations') operating income this quarter and the year-ago quarter."""
    q, fy = int(qq[1]), int(qq[3:])
    if qq in ("Q1 2018", "Q2 2018"):                      # the segment overview tables (no segment reconciliation)
        t = {OPA2: "O&P-Americas Financial Overview", IND: "I&D Financial Overview"}[label]
        L = lines(path)
        i0 = next(i for i, x in enumerate(L) if re.match(r"Table \d+\s*[-–—]\s*" + t.replace("-", "[-–—]"), x))
        i1 = next(i for i in range(i0 + 1, len(L)) if re.match(r"Table \d+\s*[-–—]", L[i]))
        v = five(path, None, "Operating income", i0, i1)
        return v[0], v[2]
    if qq in FSEG3:                                       # Q2 and Q3 2021: Exhibit 99.2's segment overview tables
        f2 = FSEG3[qq]
        t = {OPA2: "O&P-Americas Financial Overview", IND: "I&D Financial Overview"}[label]
        v = five(f2, t, "Operating income")
        return v[0], v[2]
    i0, i1 = table_at(path, SEGREC, exact=True)
    L = lines(path)
    yi = next(i for i in range(i0 + 1, i0 + 4) if YEARROW.fullmatch(L[i]))
    years = [int(y) for y in L[yi].split(" | ")]
    labels = [c.strip() for c in L[yi + 1].split("|")[1:]]
    k = next(j for j, lb in enumerate(labels) if lb in TOTALS) + 1
    cols = [(years[0], lb) for lb in labels[:k]] + [(years[1], lb) for lb in labels[k:]]
    s0 = line_no(path, "Operating income (loss):", 0, i0)
    s1 = line_no(path, "Depreciation and amortization:", 0, s0)
    assert s1 < i1
    if label == "Continuing Operations":                  # 'Continuing operations' from Q1 2019
        label = first_label(path, s0, s1, ("Continuing Operations", "Continuing operations"))
    _, v = row2(path, label, s0, s1)
    assert len(v) == len(cols), (qq, label, v, cols)
    return v[cols.index((fy, f"Q{q}"))], v[cols.index((fy - 1, f"Q{q}"))]


def tenq_oi(acc, rev_now, rev_prior):
    """The 10-Q's statement of income: operating income for the quarter and the year-ago quarter (revenues checked against the release)."""
    f = doc(acc, "10-Q__")
    st = line_no(f, "CONSOLIDATED STATEMENTS OF INCOME")
    r0 = line_no(f, "Sales and other operating revenues", 0, st)
    _, oi = row(f, "Operating income", st, st + 30)
    # the revenues total: the first row after the revenue lines whose first two values are the release's (customers + related parties)
    tot = next(x for x in lines(f)[r0:r0 + 6] if "|" in x and re.fullmatch(r"[\d,| ]+", x)
               and [num(t) for t in x.split("|")][:2] == [rev_now, rev_prior])      # the unlabelled total row
    CHECK.setdefault(f, []).append(tot)
    return f, oi[0], oi[1]


ORDER3 = list(REL3)
for qi, (qq, (acc, qacc)) in enumerate(REL3.items()):
    q, fy = int(qq[1]), int(qq[3:])
    f = FREL3[qq]
    rev, ni, eps, sh, ebitda = earnings3(f)
    opa, opa_p = seg3(qq, f, OPA2)
    ind, ind_p = seg3(qq, f, IND)
    pti, tx_q = pretax3(f, fy, q)
    pti_p, tx_p = pretax3(f, fy, q, prior=True)
    pub, filed = published(acc)
    sid = source(SID3[qq], acc, f"LyondellBasell Industries N.V. {qq} results (8-K, Exhibit 99.1" + (" and 99.2)" if qq in FSEG3 else ")"), f,
                 "the quarter's Table 1 (revenues, net income, diluted EPS, diluted shares), the segment operating income ("
                 + ("the segment overview tables" if qq in ("Q1 2018", "Q2 2018") else "Exhibit 99.2's segment overview tables"
                    if qq in FSEG3 else "the segment reconciliation, with the consolidated operating income") + ") and the EBITDA "
                 "reconciliation (income from continuing operations and the provision for income taxes), each with the year-ago quarter "
                 "as this release shows it")
    oi_src = None
    if qacc:
        fq, oi, oi_p = tenq_oi(qacc, rev[0], rev[2])
        oi_src = source(QSID[qq], qacc, f"LyondellBasell Industries N.V. {qq} 10-Q", fq,
                        "the statement of income's operating income for the quarter and the year-ago quarter (the release prints none)")
        assert SRC[oi_src]["published"] == pub, (qq, "the 10-Q is public on the release's date", SRC[oi_src]["published"], pub)
    else:
        oi, oi_p = seg3(qq, f, "Continuing Operations")
    raw = dict(rev_m=rev[0], rev_prior_m=rev[2], oi_m=oi, oi_prior_m=oi_p, pti_m=pti, pti_prior_m=pti_p, eps_q=eps[0], eps_q_prior=eps[2],
               dil_sh_m=sh[0], opa_m=opa, opa_prior_m=opa_p, ind_m=ind, ind_prior_m=ind_p, ebitda_m=ebitda[0])
    rel_day = dt.date.fromisoformat(FILINGS[acc][1][:10])
    nq = ORDER3[qi + 1] if qi + 1 < len(ORDER3) else "Q4 2021"
    basis = "diluted on net income (the release prints no continuing-operations figure)"
    seg_from = (" (O&P–Americas recast without the compounding business that moved to Advanced Polymer Solutions, as this release shows "
                "the year-ago quarter)" if qq == "Q3 2018" else "")
    p = dict(quarter=qq, fy=fy, q=q, published=pub, source=sid, release=f"{rel_day.strftime('%b')} {rel_day.day}",
             release_time=f"8-K {filed}", period_end=f"{fy}-{QDATE[q]}", raw=raw,
             sales_b=round(rev[0] / 1000, 3), sales_pct=pct(rev[2], rev[0]),
             opm=mg(oi, rev[0]), opm_bp=round((mg(oi, rev[0]) - mg(oi_p, rev[2])) * 100, 1),
             ptm=mg(pti, rev[0]), ptm_bp=round((mg(pti, rev[0]) - mg(pti_p, rev[2])) * 100, 1),
             eps_q=eps[0], eps_q_prior=eps[2], diluted_shares_m=sh[0],
             opa_pct=pct(opa_p, opa), ind_pct=pct(ind_p, ind),
             seg_note=f"O&P–Americas operating income {usd_m(opa)} vs {usd_m(opa_p)}, Intermediates & Derivatives {usd_m(ind)} vs "
                      f"{usd_m(ind_p)}{seg_from}",
             sales_note=f"sales and other operating revenues {usd_m(rev[0])} vs {usd_m(rev[2])}",
             margin_note=(f"operating income {usd_m(oi)} vs {usd_m(oi_p)}" + (f" ({qq} 10-Q)" if oi_src else "") +
                          f"; income before income taxes: income from continuing operations {usd_m(pti - tx_q)} plus the provision "
                          f"for income taxes {usd_m(tx_q)}, against {usd_m(pti_p - tx_p)} plus {usd_m(tx_p)}"),
             eps_note=f"GAAP, {basis}, {'$%.2f' % eps[0] if eps[0] >= 0 else '$(%.2f)' % -eps[0]} against "
             f"{'$%.2f' % eps[2] if eps[2] >= 0 else '$(%.2f)' % -eps[2]} a year earlier",
             cash_note=f"EBITDA {usd_m(ebitda[0])} (non-GAAP, display only)",
             next_print=f"the {nq} release")
    if oi_src:
        p["oi_source"] = oi_src
    prints.append(p)

# ── the full years (Q4 2018, Q4 2019, Q4 2020): Table 1's year column, the EBITDA reconciliation's year, the one-offs the release lists
# after tax (its footnotes and text), summed with their signs: charges net of benefits; LCM included where listed, as in 2014-2017 ──
ONEOFF3 = {
    2018: [("Q4 2018", "The third and fourth quarters of 2018 include after-tax charges for transaction and integration costs associated "
                       "with the acquisition of A. Schulman of $42 million and $15 million, respectively.", +1, None),
           ("Q4 2018", "The second quarter of 2018 includes a $346 million non-cash benefit from the release of unrecognized tax benefits and "
                       "associated accrued interest.", -1, None)],
    2019: [("Q4 2019", "In the third quarter of 2018, fourth quarter of 2018, first quarter of 2019, second quarter of 2019, third quarter "
                       "of 2019 and fourth quarter of 2019 are after-tax charges of $42 million, $15 million, $12 million, $15 million, "
                       "$33 million and $29 million, respectively, for acquisition-related transaction and integration costs associated "
                       "with our acquisition of A. Schulman.", +1, slice(2, 6)),
           ("Q4 2019", "The second quarter of 2018 and third quarter of 2019 includes a non-cash benefit of $346 million and $85 million, "
                       "respectively, from the previously unrecognized tax benefits and release of associated accrued interest.", -1, slice(1, 2))],
    2020: [("Q4 2020", "LCM and Impairment charges reduced full year 2020 net income by $457 million, or $1.37 per share.", +1, None),
           ("Q4 2020", "During 2020, costs for integration and restructuring impacted net income by $33 million or $0.10 per share.", +1, None)],
}
for p in prints:
    if p["quarter"] not in ("Q4 2018", "Q4 2019", "Q4 2020"):
        continue
    qq, fy, f = p["quarter"], p["fy"], FREL3[p["quarter"]]
    rev, ni, eps, sh, _ = earnings3(f)
    pti_y, tax_y = pretax3(f, fy, None)
    inc_y = pti_y - tax_y
    comp = f"income from continuing operations {usd_m(inc_y)} plus the provision for income taxes {usd_m(tax_y)}"
    parts = []
    for _, s, sign, sl in ONEOFF3[fy]:
        quote(f, s)
        amts = [float(a.replace(",", "")) for a in re.findall(r"\$([\d,]+) million", s)]
        amts = amts[sl] if sl else amts
        parts.append((sign * sum(amts), s))
    items = sum(v for v, _ in parts)
    kind = "charges" if items >= 0 else "benefits"
    dist = (-items > ni[3] + items) if kind == "benefits" else (items > ni[3])
    assert not dist, (qq, "a distorted year needs its encoding first")
    listed = "; ".join(f"'{s}'" for _, s in parts)
    test_note = (f"the after-tax items the {qq} release lists for the year ({listed}), charges net of benefits: "
                 f"{usd_m(items)}, against net income of {usd_m(ni[3])}: " +
                 ("kept at GAAP; the net is a charge, so the mirror test does not arise" if kind == "charges" else
                  f"a net benefit; the mirror test (the benefit against the income without it, {usd_m(ni[3] + items)}) is not met, so "
                  "the year is kept at GAAP"))
    p["fy_actual"] = dict(
        fy=fy, fy_label=f"FY{fy % 100}", eps_normalized=eps[3], excluded_note=None, revenue_usd_b=round(rev[3] / 1000, 3),
        diluted_shares_m=sh[3],
        normalization_note=f"FY{fy % 100} ${eps[3]:.2f} diluted on net income (the {qq} release prints no continuing-operations "
                           f"figure) from the {qq} release ({p['published']}) until the 10-K",
        op_margin=mg(pti_y, rev[3]),
        op_margin_note=f"FY{fy % 100} income before income taxes ({comp}) / revenues {usd_m(rev[3])} ({qq} release)",
        sales_growth=pct(rev[4], rev[3]), check_pretax_margin=mg(pti_y, rev[3]),
        check_pretax_note=f"FY{fy % 100} income before income taxes / revenues ({qq} release)",
        tax_rate=round(tax_y / pti_y, 3),
        tax_note=f"FY{fy % 100} effective rate: the provision for income taxes on income before income taxes ({comp})",
        one_off_test=dict(items_after_tax_m=items, income_attributable_m=ni[3], distorted=dist, kind=kind, note=test_note))
# the Q4 2020 release's 'Excluding LCM and Impairment' EPS also removes the LCM adjustments, which recur (as in 2014-2017): GAAP stands
quote(FREL3["Q4 2020"], "Net income excluding LCM and impairment")

# ── the FY2017-FY2020 10-Ks ──
K17, K18, K19, K20 = "0001193125-18-054181", "0001489393-19-000011", "0001489393-20-000009", "0001489393-21-000007"
F17, F18, F19, F20 = doc(K17, "10-K__"), doc(K18, "10-K__"), doc(K19, "10-K__"), doc(K20, "10-K__")
SEGN18 = SEGN12[:3] + ["Advanced Polymer Solutions"] + SEGN12[3:]
GHGQ20 = ("additional regulations and legislation are likely to be forthcoming at the U.S. federal or state level that could result in "
          "increased operating costs for compliance, or required acquisition or trading of emission allowances. Additionally, demand for "
          "the products we produce may be reduced.")
CLOUDQ = {2018: "Customer’s Accounting for Implementation Costs Incurred in a Cloud Computing Arrangement That is a Service Contract"}


def sel3(path):
    """Item 6's table: the 'Item 6' heading followed within eight lines by the table's header (FY2019 on: no '|' in the heading)."""
    L = lines(path)
    hits = [i for i, x in enumerate(L) if x.lower().startswith("item 6.") and "selected financial data" in x.lower()
            and any(y.startswith("In millions of dollars, except per share data") for y in L[i:i + 8])]
    assert len(hits) == 1, (path, hits)
    return hits[0], hits[0] + 60


def tenk3(path, acc, sid, fy, title, ghg):
    """As tenk(), for the FY2017-FY2020 10-Ks: 'Dividends paid - common stock' from FY2018, six segments from FY2018 (Advanced Polymer
    Solutions), and the vintage's own greenhouse gas sentence."""
    i0, i1 = sel3(path)
    _, rv = row(path, "Sales and other operating revenues", i0, i1)
    _e = line_no(path, "Earnings per share from continuing operations:", 0, i0)
    _, ep = row(path, "Diluted", _e, _e + 3)
    _, ocf = row(path, "Operating activities", i0, i1 + 20)
    _, capex = row(path, "Expenditures for property, plant and equipment", i0, i1 + 20)
    hdr = next(x for x in lines(path)[i0:i0 + 8] if x.startswith("In millions of dollars, except per share data"))
    yrs = [int(c) for c in cells(hdr)]
    e = line_no(path, "Potential dilutive shares")
    _, shr = row(path, "Potential dilutive shares", e, e + 1)
    st = line_no(path, "CONSOLIDATED STATEMENTS OF INCOME")
    _, pt = row(path, "Income from continuing operations before income taxes", st, st + 40)
    _, tx = row(path, first_label(path, st, st + 40, ("Provision for income taxes", "Provision for (benefit from) income taxes",
                                                    "(Benefit from) provision for income taxes")), st, st + 40)   # FY2020: the latter
    cf = line_no(path, "Cash flows from financing activities:")
    _, rep = row(path, "Repurchases of Company ordinary shares", cf, cf + 4)
    _, dvp = row(path, first_label(path, cf, cf + 4, ("Dividends paid", "Dividends paid - common stock")), cf, cf + 4)
    s24 = line_no(path, f"Year Ended December 31, {fy}", 0, line_no(path, "Potential dilutive shares"))
    _, cust = row(path, "Customers", s24, s24 + 6)
    s24p = line_no(path, f"Year Ended December 31, {fy - 1}", 0, s24)
    _, custp = row(path, "Customers", s24p, s24p + 6)
    nseg = 5 if fy == 2017 else 6
    assert len(cust) == nseg + 2 and cust[-1] == rv[0] and custp[-1] == rv[1], (fy, cust, custp, rv)
    m = re.search(r"Refining\. Our Refining segment refines[^•]*?\.(?= •|$)", norm(" ".join(lines(path))))
    refq = quote(path, m.group(0))
    source(sid, acc, title, path,
           f"FY{fy} annual history: the selected financial data (revenues and diluted EPS from continuing operations, five years), the "
           "EPS note's diluted shares, the statements of income and cash flows, the segment note (revenues from customers), the "
           "dividend line and the risk factors (cyclicality, greenhouse gas regulation) and Item 1's segment description")
    return dict(rv=dict(zip(yrs, rv)), ep=dict(zip(yrs, ep)), ocf=ocf[0], capex=capex[0], sh={fy: shr[0], fy - 1: shr[2], fy - 2: shr[4]},
                pt=pt[0], tx=tx[0], rep=rep[0], dvp=dvp[0], cust=cust, custp=custp, why=quote(path, CYCQ), ghg=quote(path, ghg),
                refq=refq, pub=SRC[sid]["published"], nseg=nseg)


T17 = tenk3(F17, K17, "LB100", 2017, "LyondellBasell Industries N.V. FY2017 10-K", GHGQ)
T18 = tenk3(F18, K18, "LB101", 2018, "LyondellBasell Industries N.V. FY2018 10-K", GHGQ)
T19 = tenk3(F19, K19, "LB102", 2019, "LyondellBasell Industries N.V. FY2019 10-K", GHGQ)
T20 = tenk3(F20, K20, "LB103", 2020, "LyondellBasell Industries N.V. FY2020 10-K", GHGQ20)
assert [T17["ep"][2017], T18["ep"][2018], T19["ep"][2019], T20["ep"][2020]] == [12.28, 12.03, 9.60, 4.25]
DIVQ.update({2017: quote(F17, "Increased quarterly dividend from $0.85 to $0.90 in May 2017;"),
             2018: quote(F18, "Increase in quarterly dividend from $0.90 to $1.00 in February 2018."),
             2019: quote(F19, "Increased quarterly dividend from $1.00 per share to $1.05 per share in the second quarter;"),
             2020: quote(F20, "December | 1.05 | 352 | November 30, 2020")})
DIVR.update({2017: 0.90, 2018: 1.00, 2019: 1.05, 2020: 1.05})
CLOUD3 = {}
for fy, path in ((2018, F18), (2019, F19), (2020, F20)):
    # each of these 10-Ks names cloud once, in an accounting standard's title (ASU 2018-15): quoted, text only (the SCHW `cloud_words`)
    assert sum("cloud" in x.lower() for x in lines(path)) == 1, fy
    CLOUD3[fy] = quote(path, CLOUDQ[2018])
for path in (F17, F18, F19, F20):        # no 10-K of the range names electric vehicles, e-commerce, streaming or crypto
    low = norm(" ".join(lines(path))).lower()
    assert not any(w in low for w in ("electric vehicle", "e-commerce", "streaming", "crypto")), path


def vintage3(prev, t, fy, sid):
    """vintage() for FY2017-FY2020: six segments from FY2018, the business line with Advanced Polymer Solutions, the cloud words."""
    v = vintage(prev, t, fy, sid)
    if t["nseg"] == 6:
        v.update(groups=[[n, round(c / 1000, 3), pct(pc, c)] for n, c, pc in zip(SEGN18, t["cust"][:6], t["custp"][:6])],
                 business_line="Olefins and polyolefins, intermediates and derivatives, advanced polymer solutions, refining, technology")
    if fy in CLOUD3:
        v["cloud_quote"] = CLOUD3[fy]
    keep = [str(y) for y in range(fy - 9, fy + 1)]          # the ten fiscal years to the latest one (the 2010 count leaves with FY2020)
    v["diluted_shares_m"] = {y: n for y, n in v["diluted_shares_m"].items() if y in keep}
    rs = v["revenue_sources"]
    v["revenue_note"] = (f"{min(int(y) for y, s in rs.items() if s == sid)}-{fy} from the FY{fy} 10-K (continuing operations)"
                         + ("; 2010 the FY2012 10-K's combined periods ($38,939M; the later 10-Ks show its two periods, which sum to it)"
                            if "2010" in rs else "")
                         + "; earlier years from the latest earlier 10-K that reports them; the ten fiscal years to the latest one")
    if "2010" not in v["diluted_shares_m"]:
        v["shares_note"] = "diluted weighted-average shares of the EPS note; the ten fiscal years to the latest one"
    if fy == 2020:                                            # no increase in 2020: the rate of the 10-K's dividend table
        v["dividend_note"] = f"$1.05 a quarter, the interim dividend of 2020 (FY2020 10-K, the dividend table's December row: '{DIVQ[2020]}')"
    return v


V8 = vintage3(V7, T17, 2017, "LB100")
V9 = vintage3(V8, T18, 2018, "LB101")
V10 = vintage3(V9, T19, 2019, "LB102")
V11 = vintage3(V10, T20, 2020, "LB103")
assert "2007" not in V8["revenue_usd_b"] and "2008" in V8["revenue_usd_b"] and "2010" in V10["revenue_usd_b"] and "2010" not in V11["revenue_usd_b"]

# ── dividends: each declared interim rate from the first filing that states it ──
DIV3 = [("Q1 2018", 1.00, "Dividend increased by 11% to $1.00 per share"),
        ("Q2 2019", 1.05, "Increased our quarterly dividend to $1.05 per share, the eleventh increase over the past 8 years"),
        ("Q2 2021", 1.13, "Increased quarterly dividend by 7.6 percent to $1.13 per share reflecting confidence in dividend sustainability "
                          "through cycles")]
for qq, rate, s in DIV3:
    dividends.append(dict(published=SRC[SID3[qq]]["published"], source=SID3[qq], quarterly=rate,
                          note=f"${rate:.2f} a quarter, the interim dividend increase announced in the {qq} release",
                          quote=quote(FREL3[qq], s)))

# ── repurchase authorities (display only, the share counts carry their effect) ──
BB3 = [("LB84", "0001193125-18-183600", "8-K__", "the 2018 annual meeting",
        "The approval of the authority of the Management Board or the Board, as applicable, to repurchase up to 10% of the Company’s "
        "issued share capital until December 1, 2019 was approved", "the 2018 annual meeting's authority to repurchase up to 10% of the shares"),
       ("LB85", "0001489393-19-000034", "8-K__", "the 2019 annual meeting",
        "The authorization of the Board to repurchase up to 10% of the Company’s outstanding shares, at prices ranging from the nominal "
        "value of the shares up to 110% of the market price for the shares, until November 30, 2020 was approved",
        "the 2019 annual meeting's authority to repurchase up to 10% of the shares"),
       ("LB86", "0001489393-19-000037", "EX-99.1__", "the June 2019 announcement",
        "In addition, we intend to expedite our share repurchase program, which currently allows for the repurchase of up to 37 million of "
        "our outstanding shares.", "the intent to expedite the share repurchase program (up to 37 million shares)"),
       ("LB87", "0001489393-19-000050", "8-K__", "the September 2019 extraordinary general meeting",
        "the Company’s shareholders approved a new share repurchase program authorizing the Company to repurchase up to 10% of the "
        "Company’s outstanding shares as of the date of the Extraordinary General Meeting, or approximately 33.3 million shares, over the "
        "next 18 months", "the September 2019 meeting's program to repurchase up to 10% of the shares (about 33.3 million)"),
       ("LB88", "0001489393-20-000037", "8-K__", "the 2020 annual meeting",
        "the Company’s shareholders approved a new share repurchase program authorizing the Company to repurchase up to 10% of the "
        "Company’s issued share capital as of the date of the Annual Meeting, or approximately 34.0 million shares, over the next 18 months",
        "the 2020 annual meeting's program to repurchase up to 10% of the shares (about 34.0 million)"),
       ("LB89", "0001489393-21-000019", "8-K__", "the 2021 annual meeting",
        "the Company’s shareholders approved a new share repurchase program authorizing the Company to repurchase up to 10% of the "
        "Company’s issued share capital as of the date of the Annual Meeting, or 34,004,563 shares, until November 28, 2022",
        "the 2021 annual meeting's program to repurchase up to 10% of the shares (34,004,563)")]
for sid, acc, pre, what, s, text in BB3:
    fb = doc(acc, pre)
    source(sid, acc, f"LyondellBasell Industries N.V. 8-K ({what})", fb, "the share repurchase authority")
    buybacks2.append(dict(published=SRC[sid]["published"], source=sid, quote=quote(fb, s),
                          note="display only: the diluted share counts carry its effect", text=text))

# ── adds nothing (asserted present, quoted in the README): the preliminary Q1 2020 8-K gives a net income and EBITDA range only, and
# the capital expenditure outlook; no filing of 2018-2021 guides revenue, EPS or a margin in numbers ──
FPRE = doc("0001104659-20-046638", "EX-99.1__")
quote(FPRE, "First quarter 2020 net income is expected to be in the range of $110 million to $180 million.")
for qq in REL3:
    quote(FREL3[qq], "OUTLOOK")

# ══ 2022-2026: the Q4 2021 to Q3 2026 releases, the FY2021-FY2025 10-Ks, the dividends and repurchase authorities to 2026-11-22 ══
# (added for retro/README.md, "LYB 2022-2026"; everything above is unchanged, so the 2012-2021 facts regenerate byte for byte).
# From Q4 2021 every release is Exhibit 99.1 (Table 1, the earnings summary; Table 2, the EBITDA reconciliation) and Exhibit 99.2 (the
# segment overview tables, operating income by segment); no release prints the consolidated operating income. For Q1-Q3 it comes from
# the quarter's 10-Q, accepted the same Friday during the session ('oi_source', the 2018-2021 encoding); the fourth quarter has no 10-Q
# and no filing prints a fourth-quarter operating income, so a Q4 print's operating margin is n/r (None). From Q1 2025 the EBITDA
# reconciliation starts from net income (the refining business discontinued, its results an identified item), so the pre-tax income comes
# from the 10-Q for Q1-Q3 and is n/r for Q4 2025. Items 6 of the FY2021-FY2025 10-Ks are 'Reserved': each vintage takes three years from
# its own statements and earlier years from the latest earlier vintage, the ten fiscal years to the latest one.
REL4 = {"Q4 2021": ("0001489393-22-000003", None), "Q1 2022": ("0001489393-22-000018", "0001489393-22-000020"),
        "Q2 2022": ("0001489393-22-000035", "0001489393-22-000037"), "Q3 2022": ("0001489393-22-000043", "0001489393-22-000046"),
        "Q4 2022": ("0001489393-23-000002", None), "Q1 2023": ("0001489393-23-000023", "0001489393-23-000025"),
        "Q2 2023": ("0001489393-23-000036", "0001489393-23-000037"), "Q3 2023": ("0001489393-23-000040", "0001489393-23-000043"),
        "Q4 2023": ("0001489393-24-000005", None), "Q1 2024": ("0001489393-24-000018", "0001489393-24-000020"),
        "Q2 2024": ("0001489393-24-000035", "0001489393-24-000037"), "Q3 2024": ("0001489393-24-000040", "0001489393-24-000046"),
        "Q4 2024": ("0001489393-25-000004", None), "Q1 2025": ("0001489393-25-000021", "0001489393-25-000022"),
        "Q2 2025": ("0001489393-25-000038", "0001489393-25-000041"), "Q3 2025": ("0001489393-25-000054", "0001489393-25-000056"),
        "Q4 2025": ("0001489393-26-000003", None), "Q1 2026": ("0001489393-26-000025", "0001489393-26-000028"),
        "Q2 2026": ("0001489393-26-000057", "0001489393-26-000061"), "Q3 2026": ("0001489393-26-000067", "0001489393-26-000070")}
SID4 = {q: f"LB{120 + i}" for i, q in enumerate(REL4)}
QSID4 = {q: f"LB{140 + i}" for i, q in enumerate(q for q, (_, b) in REL4.items() if b)}
FREL4 = {q: doc(a, "EX-99.1__") for q, (a, _) in REL4.items()}
FSEG4 = {q: doc(a, "EX-99.2__") for q, (a, _) in REL4.items()}
DISC25 = ("Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025")          # releases whose year-ago quarter is restated without the refining business
quote(FREL4["Q1 2025"], "In February 2025, we ceased business operations at our Houston refinery. Accordingly, our refining business, "
                        "previously disclosed as the Refining segment, is reported as a discontinued operation. The related operating "
                        "results of our refining business are reported as discontinued operations for all periods presented.")
# the 8-K/A of 2024-11-01 (accepted 15:04 ET, the release's day) re-files Exhibit 99.2 of Q3 2024 to correct one word of its text
# ("438 million shares" to "438 thousand shares"): every figure is the same, so it adds nothing (asserted)
_a, _b = lines(FSEG4["Q3 2024"]), lines(doc("0001489393-24-000043", "EX-99.2__"))
assert len(_a) == len(_b) and [i for i, (x, y) in enumerate(zip(_a, _b)) if x != y] == [65] and "438 thousand shares" in _b[65]


def earnings4(path):
    """Table 1 (Earnings Summary), its first block (the 'Excluding Identified Items' block below it is the company's adjusted view)."""
    i0, i1 = table_at(path, "Earnings Summary")
    L = lines(path)
    i1 = next((i for i in range(i0 + 1, i1) if L[i].startswith(("Excluding", "(a)", "(1)"))), i1)
    rev = five(path, None, "Sales and other operating revenues", i0, i1)
    ni = five(path, None, first_label(path, i0, i1, ("Net income", "Net income (loss)", "Net (loss) income")), i0, i1)
    eps = five(path, None, first_label(path, i0, i1, ("Diluted earnings per share", "Diluted earnings (loss) per share",
                                                    "Diluted (loss) earnings per share")), i0, i1)
    sh = five(path, None, "Weighted average diluted share count", i0, i1)
    eb = five(path, None, "EBITDA", i0, i1)
    return rev, ni, eps, sh, eb


def recon4(path):
    """Table 2, the reconciliation of net income to EBITDA: income from continuing operations and the provision for income taxes
    (None where the table starts from net income, from Q1 2025), and the net income excluding identified items."""
    L = lines(path)
    i0 = [i for i, x in enumerate(L) if re.match(r"Table 2\s*[-–—]\s*Reconciliation", x)]
    assert len(i0) == 1, path
    i0 = i0[0]
    i1 = next(i for i in range(i0 + 1, len(L)) if re.match(r"Table \d+\s*[-–—]", L[i]))
    lab = lambda x: dnorm(nofoot(x.split(" |")[0]))
    inc = [i for i in range(i0, i1) if "|" in L[i] and lab(L[i]) in ("Income from continuing operations", "(Loss) income from "
                                                                   "continuing operations", "Income (loss) from continuing operations")]
    excl = next(i for i in range(i0, i1) if "|" in L[i] and lab(L[i]).startswith("Net income") and "excluding" in lab(L[i]))
    _, ex = row2(path, lab(L[excl]), excl, excl + 1)
    if not inc:
        return None, None, ex
    assert len(inc) == 1, (path, inc)
    _, iv = row2(path, lab(L[inc[0]]), inc[0], inc[0] + 1)
    t = next(i for i in range(inc[0] + 1, inc[0] + 3) if "|" in L[i] and "income taxes" in lab(L[i]))
    _, tv = row2(path, lab(L[t]), t, t + 1)
    return iv, tv, ex


def seg4(qq, label):
    """A segment's operating income row in Exhibit 99.2's segment overview table (the quarter, the previous quarter, the year-ago quarter,
    then the year to date; Q3 2026: the quarter, the previous quarter, then the nine months, with no year-ago quarter)."""
    f2 = FSEG4[qq]
    t = {OPA2: "O&P-Americas Financial Overview", IND: "I&D Financial Overview"}[label]
    i0, i1 = table_at(f2, t)
    lab = first_label(f2, i0, i1, ("Operating income", "Operating income (loss)", "Operating (loss) income"))
    _, v = row2(f2, lab, i0, i1)
    return v


def tenq4(acc, rev_now, rev_prior):
    """The 10-Q's statement of income: operating income and income from continuing operations before income taxes, the quarter and the
    year-ago quarter (the revenues total checked against the release's)."""
    f = doc(acc, "10-Q__")
    st = next(i for i, x in enumerate(lines(f)) if x in ("CONSOLIDATED STATEMENTS OF INCOME", "CONSOLIDATED STATEMENTS OF INCOME (LOSS)",
                                                          "CONSOLIDATED STATEMENTS OF (LOSS) INCOME"))
    r0 = line_no(f, "Sales and other operating revenues", 0, st)
    tot = next(x for x in lines(f)[r0:r0 + 6] if "|" in x and re.fullmatch(r"[\d,| ]+", x)
               and [num(t) for t in x.split("|")][:2] == [rev_now, rev_prior])
    CHECK.setdefault(f, []).append(tot)
    _, oi = row2(f, first_label(f, st, st + 30, ("Operating income", "Operating income (loss)", "Operating (loss) income")), st, st + 30)
    _, pt = row2(f, first_label(f, st, st + 30, ("Income from continuing operations before income taxes",
                                                 "Income (loss) from continuing operations before income taxes",
                                                 "(Loss) income from continuing operations before income taxes")), st, st + 30)
    return f, oi[0], oi[1], pt[0], pt[1]


usd_e = lambda e: f"${e:.2f}" if e >= 0 else f"$({-e:.2f})"      # a loss per share in parentheses, as the filings print it
ORDER4 = list(REL4)
q4_note = ("operating income: not in the release (its segment tables give segment operating income only) and the fourth quarter has no "
           "10-Q, so the operating margin is n/r")
for qi, (qq, (acc, qacc)) in enumerate(REL4.items()):
    q, fy = int(qq[1]), int(qq[3:])
    f = FREL4[qq]
    rev, ni, eps, sh, ebitda = earnings4(f)
    opa_v, ind_v = seg4(qq, OPA2), seg4(qq, IND)
    seg_from = ""
    if len(opa_v) == 4:                     # Q3 2026: no year-ago column; the year-ago quarter as the Q3 2025 release printed it
        assert qq == "Q3 2026" and len(ind_v) == 4
        y = next(p for p in prints if p["quarter"] == "Q3 2025")
        ya_o, ya_i = seg4("Q3 2025", OPA2), seg4("Q3 2025", IND)
        assert (opa_v[3], ind_v[3]) == (ya_o[3], ya_i[3]), "the nine months of 2025 as the Q3 2025 release printed them (no recast)"
        opa, opa_p, ind, ind_p = opa_v[0], y["raw"]["opa_m"], ind_v[0], y["raw"]["ind_m"]
        seg_from = (" (this release's segment tables print no third quarter 2025 column: the year-ago quarter is the Q3 2025 release's, "
                    "whose nine months of 2025 this release repeats unchanged)")
    else:
        opa, opa_p, ind, ind_p = opa_v[0], opa_v[2], ind_v[0], ind_v[2]
    inc, tax, excl = recon4(f)
    pub, filed = published(acc)
    sid = source(SID4[qq], acc, f"LyondellBasell Industries N.V. {qq} results (8-K, Exhibits 99.1 and 99.2)", f,
                 "the quarter's Table 1 (revenues, net income, diluted EPS, diluted shares), the EBITDA reconciliation (income from "
                 "continuing operations and the provision for income taxes, where printed; the net income excluding identified items) and "
                 "Exhibit 99.2's segment overview tables (segment operating income), each with the year-ago quarter as this release shows it")
    oi_src, oi, oi_p, pti, pti_p = None, None, None, None, None
    if inc is not None:
        pti, pti_p = inc[0] + tax[0], inc[2] + tax[2]
        pt_note = (f"income before income taxes: income from continuing operations {usd_m(inc[0])} plus the provision for income taxes "
                   f"{usd_m(tax[0])}, against {usd_m(inc[2])} plus {usd_m(tax[2])}")
    if qacc:
        fq, oi, oi_p, qpt, qpt_p = tenq4(qacc, rev[0], rev[2])
        oi_src = source(QSID4[qq], qacc, f"LyondellBasell Industries N.V. {qq} 10-Q", fq,
                        "the statement of income's operating income and income from continuing operations before income taxes for the "
                        "quarter and the year-ago quarter (the release prints no operating income)")
        assert SRC[oi_src]["published"] == pub, (qq, "the 10-Q is public on the release's date", SRC[oi_src]["published"], pub)
        if inc is not None:
            assert (qpt, qpt_p) == (pti, pti_p), (qq, "the release's pre-tax components and the 10-Q's pre-tax income agree")
        else:
            pti, pti_p = qpt, qpt_p
            pt_note = f"income from continuing operations before income taxes {usd_m(pti)} vs {usd_m(pti_p)} ({qq} 10-Q)"
    elif inc is None:
        pt_note = ("income before income taxes: not in the release (from Q1 2025 its EBITDA reconciliation starts from net income, the "
                   "discontinued refining business among the identified items) and the fourth quarter has no 10-Q, so the pre-tax margin is n/r")
    raw = dict(rev_m=rev[0], rev_prior_m=rev[2], oi_m=oi, oi_prior_m=oi_p, pti_m=pti, pti_prior_m=pti_p, eps_q=eps[0], eps_q_prior=eps[2],
               dil_sh_m=sh[0], opa_m=opa, opa_prior_m=opa_p, ind_m=ind, ind_prior_m=ind_p, ebitda_m=ebitda[0])
    rel_day = dt.date.fromisoformat(FILINGS[acc][1][:10])
    nq = ORDER4[qi + 1] if qi + 1 < len(ORDER4) else "Q4 2026"
    m_ = lambda x, r: None if x is None else mg(x, r)
    bp_ = lambda a, ra, b, rb: None if a is None else round((mg(a, ra) - mg(b, rb)) * 100, 1)
    p = dict(quarter=qq, fy=fy, q=q, published=pub, source=sid, release=f"{rel_day.strftime('%b')} {rel_day.day}",
             release_time=f"8-K {filed}", period_end=f"{fy}-{QDATE[q]}", raw=raw,
             sales_b=round(rev[0] / 1000, 3), sales_pct=pct(rev[2], rev[0]),
             opm=m_(oi, rev[0]), opm_bp=bp_(oi, rev[0], oi_p, rev[2]),
             ptm=m_(pti, rev[0]), ptm_bp=bp_(pti, rev[0], pti_p, rev[2]),
             eps_q=eps[0], eps_q_prior=eps[2], diluted_shares_m=sh[0],
             opa_pct=pct(opa_p, opa), ind_pct=pct(ind_p, ind),
             seg_note=f"O&P–Americas operating income {usd_m(opa)} vs {usd_m(opa_p)}, Intermediates & Derivatives {usd_m(ind)} vs "
                      f"{usd_m(ind_p)}{seg_from}",
             sales_note=f"sales and other operating revenues {usd_m(rev[0])} vs {usd_m(rev[2])}" + (
                 " (the year-ago quarter without the refining business, a discontinued operation, as this release shows it)"
                 if qq in DISC25 else ""),
             margin_note=((f"operating income {usd_m(oi)} vs {usd_m(oi_p)} ({qq} 10-Q)" if qacc else q4_note) + "; " + pt_note),
             eps_note=f"GAAP, diluted on net income (the release prints no continuing-operations figure), "
                      f"{'$%.2f' % eps[0] if eps[0] >= 0 else '$(%.2f)' % -eps[0]} against "
                      f"{'$%.2f' % eps[2] if eps[2] >= 0 else '$(%.2f)' % -eps[2]} a year earlier",
             cash_note=f"EBITDA {usd_m(ebitda[0])} (non-GAAP, display only)",
             next_print=f"the {nq} release")
    if oi_src:
        p["oi_source"] = oi_src
    if q == 4:
        # the full year: Table 1's year column; the one-off test on Table 2's identified items after tax for the year (net income
        # excluding identified items less net income: every item the table lists, charges net of benefits, as for 2014-2017's table)
        items = round(excl[3] - ni[3], 1)
        kind = "charges" if items >= 0 else "benefits"
        dist = (-items > ni[3] + items) if kind == "benefits" else (items > ni[3])
        loss = eps[3] <= 0
        lab_ex = next(x.split(" |")[0] for x in lines(f) if x.startswith("Net income") and "excluding" in x)
        if loss:
            test_note = (f"the release's Table 2: '{nofoot(lab_ex)}' of {usd_m(excl[3])} against net income (loss) of {usd_m(ni[3])}, "
                         f"identified items of {usd_m(items)} after tax: the year is a loss, so it is excluded whatever the test")
        else:
            test_note = (f"the release's Table 2: '{nofoot(lab_ex)}' of {usd_m(excl[3])} against net income of {usd_m(ni[3])}, "
                         f"identified items of {usd_m(items)} after tax (every item the table lists, charges net of benefits): kept at "
                         "GAAP; the net is a charge, so the mirror test does not arise")
        a = dict(fy=fy, fy_label=f"FY{fy % 100}", eps_normalized=None if loss else eps[3],
                 excluded_note=(f"{usd_e(eps[3])} a diluted share on net income for FY{fy % 100} (the {qq} release): a loss, so the year has no P/E and is "
                                "excluded as the latest year, its days out of the window (the MU FY2003 and NEM FY2007 rule)") if loss else None,
                 eps_gaap=eps[3], revenue_usd_b=round(rev[3] / 1000, 3), diluted_shares_m=sh[3],
                 normalization_note=(f"FY{fy % 100} ${eps[3]:.2f} diluted on net income (the {qq} release prints no continuing-operations "
                                     f"figure) from the {qq} release ({pub}) until the 10-K") if not loss else
                                    f"FY{fy % 100} excluded (a loss) from the {qq} release ({pub}) until the 10-K",
                 sales_growth=pct(rev[4], rev[3]),
                 one_off_test=dict(items_after_tax_m=items, income_attributable_m=ni[3], distorted=dist, kind=kind, note=test_note))
        if inc is not None:
            pti_y = inc[3] + tax[3]
            comp = f"income from continuing operations {usd_m(inc[3])} plus the provision for income taxes {usd_m(tax[3])}"
            a.update(op_margin=mg(pti_y, rev[3]),
                     op_margin_note=f"FY{fy % 100} income before income taxes ({comp}) / revenues {usd_m(rev[3])} ({qq} release)",
                     check_pretax_margin=mg(pti_y, rev[3]), check_pretax_note=f"FY{fy % 100} income before income taxes / revenues ({qq} release)",
                     tax_rate=round(tax[3] / pti_y, 3),
                     tax_note=f"FY{fy % 100} effective rate: the provision for income taxes on income before income taxes ({comp})")
        else:                                   # Q4 2025: no pre-tax income in the release; the vintage's last year's margin stands
            a.update(op_margin=None, op_margin_note=None, check_pretax_margin=None, check_pretax_note=None, tax_rate=None, tax_note=None)
        p["fy_actual"] = a
    prints.append(p)
# the company's EPS excluding identified items removes the LCM adjustments and the asset write-downs 'in excess of $10 million in aggregate
# for the period', which recur (impairments or write-downs in each year of 2021-2025): not a figure excluding only one-offs; GAAP stands
quote(FREL4["Q2 2025"], "“Identified items” include adjustments for lower of cost or market (\"LCM\"), gain on sale of business, asset "
                        "write-downs in excess of $10 million in aggregate for the period")
# the 2027 targets of the 2023 Capital Markets Day (Q1 2023 release) are mid-cycle aspirations on 2013-2022 average margins, no guide
quote(FREL4["Q1 2023"], "Launched new strategy targeting net income(b) of $6.3 billion and $10 billion of normalized EBITDA(a)(b) by 2027")
quote(FREL4["Q1 2023"], "(b) Reflects a 2022 year-end asset portfolio with 2013-2022 historical average margins and operating rates and "
                        "the company's strategic initiatives.")
for qq in REL4:
    quote(FREL4[qq], "OUTLOOK")

# ── the FY2021-FY2025 10-Ks (Item 6 reserved: three years from the statements) ──
K21, K22, K23, K24, K25 = ("0001489393-22-000009", "0001489393-23-000006", "0001489393-24-000012", "0001489393-25-000008",
                           "0001489393-26-000012")
F21, F22, F23, F24, F25 = (doc(k, "10-K__") for k in (K21, K22, K23, K24, K25))
CYCQ24 = "Our business operations are subject to the cyclical and volatile nature of the supply-demand balance in the chemical industry."
GHGQ22 = ("Additional regulations could be forthcoming at the U.S. federal or state level that could result in increased operating costs "
          "for compliance, required acquisition or trading of emission allowances, or compliance costs associated with additional regulatory "
          "frameworks for a range of potential carbon reduction projects, including carbon capture, use, and sequestration projects. "
          "Additionally, demand for the products we produce may be reduced.")
GHGQ24 = ("several state governments have promulgated regulations directed at GHG emissions reductions from certain types of facilities, and "
          "additional regulations could be forthcoming, that could result in increased operating costs for compliance, required acquisition "
          "or trading of emission allowances, or other costs.", "Additionally, demand for the products we produce may be reduced.")
AIQ = "In addition, the complex and dynamic regulatory environment surrounding artificial intelligence (“AI”), including generative AI, subjects us to a variety of risks."
REFX = "Accordingly, our refining business, previously disclosed as the Refining segment, is reported as a discontinued operation."
SEGN25 = SEGN18[:4] + SEGN18[5:]
DIVQ4 = {2021: "December | 1.13 | 376 | November 29, 2021", 2022: "December - Quarterly dividend | 1.19 | 386 | November 28, 2022",
         2023: "December - Quarterly dividend | 1.25 | 406 | November 27, 2023", 2024: "December | 1.34 | 437 | December 2, 2024",
         2025: ("In February 2026, we declared a quarterly dividend of $0.69 per share, representing a $0.68 per share reduction from our "
                "fourth quarter 2025 dividend.")}
DIVR4 = {2021: 1.13, 2022: 1.19, 2023: 1.25, 2024: 1.34, 2025: 0.69}


def tenk4(path, acc, sid, fy, title):
    """One FY2021-FY2025 10-K vintage: the statement of income's three years (revenues, pre-tax income, tax), the EPS note's diluted EPS
    from continuing operations and diluted shares (three years), the cash flow statement, the segment note's revenues from customers
    (this year and last), and its own words (cyclicality, greenhouse gas regulation, refining, AI)."""
    L = lines(path)
    st = line_no(path, "CONSOLIDATED STATEMENTS OF INCOME")
    yrs = [int(c) for c in cells(next(x for x in L[st:st + 4] if x.startswith("Millions of dollars, except earnings")))]
    r0 = line_no(path, "Related parties", 0, st)
    tot = L[r0 + 1]
    assert re.fullmatch(r"[\d,| ]+", tot), (fy, tot)
    rv = [num(t) for t in tot.split("|")]
    CHECK.setdefault(path, []).append(tot)
    _, pt = row2(path, first_label(path, st, st + 40, ("Income from continuing operations before income taxes",
                                                      "Income (loss) from continuing operations before income taxes")), st, st + 40)
    _, tx = row2(path, first_label(path, st, st + 40, ("Provision for income taxes", "Provision for (benefit from) income taxes",
                                                      "(Benefit from) provision for income taxes")), st, st + 40)
    e = line_no(path, "Potential dilutive shares")
    _, shr = row(path, "Potential dilutive shares", e, e + 1)
    _, epr = row(path, "Diluted", e, e + 4)
    assert len(shr) == 6 and len(epr) == 6, (fy, shr, epr)
    cfo = line_no(path, "Net cash provided by operating activities |")
    _, ocf = row(path, "Net cash provided by operating activities", cfo, cfo + 1)
    _, capex = row(path, "Expenditures for property, plant and equipment", cfo, cfo + 4)
    cf = line_no(path, "Cash flows from financing activities:")
    _, rep = row(path, "Repurchases of Company ordinary shares", cf, cf + 4)
    _, dvp = row(path, "Dividends paid - common stock", cf, cf + 4)
    s24 = line_no(path, f"Year Ended December 31, {fy}", 0, e)
    _, cust = row(path, "Customers", s24, s24 + 6)
    s24p = line_no(path, f"Year Ended December 31, {fy - 1}", 0, s24)
    _, custp = row(path, "Customers", s24p, s24p + 6)
    nseg = 5 if fy == 2025 else 6
    assert len(cust) == nseg + 2 and cust[-1] == rv[0] and custp[-1] == rv[1], (fy, cust, custp, rv)
    full = norm(" ".join(L))
    low = full.lower()
    assert not any(w in low for w in ("electric vehicle", "e-commerce", "streaming", "crypto", "cloud", "glp-1", "obesity")), fy
    assert "automotive" in low, fy
    ai = quote(path, AIQ) if fy >= 2024 else None
    if fy < 2024:
        assert "artificial intelligence" not in low and "generative" not in low, fy
    m = re.search(r"Refining\. Our Refining segment refines[^•]*?\.(?= •|$)", full)
    if fy <= 2024:
        refq = quote(path, m.group(0))
        why = quote(path, CYCQ if fy <= 2023 else CYCQ24)
        ghg = (quote(path, GHGQ20) if fy == 2021 else quote(path, GHGQ22) if fy <= 2023 else
               " … ".join(quote(path, s) for s in GHGQ24))
        refx = None
    else:                                    # FY2025: the refining business is a discontinued operation; no greenhouse gas demand words
        assert m is None and "demand for the products we produce may be reduced" not in full
        refq, ghg, refx, why = None, None, quote(path, REFX), quote(path, CYCQ24)
    source(sid, acc, title, path,
           f"FY{fy} annual history (Item 6 reserved): the statement of income (revenues, income before income taxes and the provision, "
           "three years), the EPS note's diluted EPS from continuing operations and diluted shares, the cash flow statement, the segment "
           "note (revenues from customers), the dividend table and the risk factors (cyclicality, greenhouse gas regulation, AI) and "
           "Item 1's segment description")
    return dict(rv=dict(zip(yrs, rv)), ep=dict(zip(yrs, epr[0::2])), ocf=ocf[0], capex=capex[0], sh=dict(zip(yrs, shr[0::2])),
                pt=pt[0], tx=tx[0], rep=rep[0], dvp=dvp[0], cust=cust, custp=custp, why=why, ghg=ghg, refq=refq, refx=refx, ai=ai,
                pub=SRC[sid]["published"], nseg=nseg)


T21 = tenk4(F21, K21, "LB110", 2021, "LyondellBasell Industries N.V. FY2021 10-K")
T22 = tenk4(F22, K22, "LB111", 2022, "LyondellBasell Industries N.V. FY2022 10-K")
T23 = tenk4(F23, K23, "LB112", 2023, "LyondellBasell Industries N.V. FY2023 10-K")
T24 = tenk4(F24, K24, "LB113", 2024, "LyondellBasell Industries N.V. FY2024 10-K")
T25 = tenk4(F25, K25, "LB114", 2025, "LyondellBasell Industries N.V. FY2025 10-K")
assert [T21["ep"][2021], T22["ep"][2022], T23["ep"][2023], T24["ep"][2024], T25["ep"][2025]] == [16.77, 11.83, 6.48, 4.14, -2.48]
assert (T25["ep"][2024], T25["ep"][2023], T25["rv"][2023]) == (4.39, 5.68, 33336)          # restated without the refining business
for fy, path in ((2021, F21), (2022, F22), (2023, F23), (2024, F24), (2025, F25)):
    DIVQ[fy] = quote(path, DIVQ4[fy])
    DIVR[fy] = DIVR4[fy]
# the 8-Ks of 2023-03-07 (a summary of 2020-2022 on the segment structure effective January 1, 2023) and 2023-05-12 (the FY2022 10-K's
# Items recast for that structure) recast segments only: the revenues, EPS and shares a model reads are the FY2022 10-K's (asserted), and
# the segment bridge is display only, so they add nothing (the UNH 2011-05-23 segment recast precedent)
FR23 = doc("0001489393-23-000008", "EX-99.1__")
quote(FR23, "Based on Segment Structure Effective as of January 1, 2023")
assert row(FR23, "Total sales and other operating revenues", 0)[1] == [T22["rv"][2020], T22["rv"][2021], T22["rv"][2022]]
FR23b = doc("0001489393-23-000028", "EX-99.1__")
_e = line_no(FR23b, "Potential dilutive shares")
assert row(FR23b, "Potential dilutive shares", _e, _e + 1)[1][0::2] == [T22["sh"][y] for y in (2022, 2021, 2020)]
assert row(FR23b, "Diluted", _e, _e + 4)[1][0::2] == [T22["ep"][y] for y in (2022, 2021, 2020)]


def vintage4(prev, t, fy, sid):
    """The FY2021-FY2025 vintages: three years from the 10-K's statements, earlier years from the latest earlier vintage, the ten fiscal
    years to the latest one (EPS and shares included, so 2010 and 2011 leave); a loss year is excluded."""
    tt = dict(t, ep={y: v for y, v in t["ep"].items() if v > 0})
    v = vintage(prev, tt, fy, sid)
    keep = [str(y) for y in range(fy - 9, fy + 1)]
    v["eps_normalized"] = {y: e for y, e in v["eps_normalized"].items() if y in keep}
    v["eps_excluded"] = {str(y): (f"{usd_e(e)} a diluted share from continuing operations for FY{y % 100} (FY{fy} 10-K): a loss, so "
                                  "the year has no P/E and is excluded, its days out of the window (the MU FY2003 and NEM FY2007 rule)")
                         for y, e in t["ep"].items() if e <= 0}
    v["diluted_shares_m"] = {y: n for y, n in v["diluted_shares_m"].items() if y in keep}
    segs = SEGN18 if t["nseg"] == 6 else SEGN25
    v.update(groups=[[n, round(c / 1000, 3), pct(pc, c)] for n, c, pc in zip(segs, t["cust"][:t["nseg"]], t["custp"][:t["nseg"]])],
             business_line=("Olefins and polyolefins, intermediates and derivatives, advanced polymer solutions, refining, technology"
                            if t["nseg"] == 6 else "Olefins and polyolefins, intermediates and derivatives, advanced polymer solutions, technology"),
             shares_note="diluted weighted-average shares of the EPS note; the ten fiscal years to the latest one",
             tenk_scan=True)
    first = min(int(y) for y, s in v["revenue_sources"].items() if s == sid)
    v["revenue_note"] = (f"{first}-{fy} from the FY{fy} 10-K's statement of income (Item 6 reserved)"
                         + (", from continuing operations without the refining business (discontinued in 2025); earlier years with it, as "
                            "the earlier 10-Ks report them (a seam)" if fy == 2025 else "") +
                         "; earlier years from the latest earlier 10-K that reports them; the ten fiscal years to the latest one")
    v["dividend_note"] = (f"${DIVR[fy]:.2f} a quarter, the interim dividend of {fy} (FY{fy} 10-K, the dividend table's December row: "
                          f"'{DIVQ[fy]}')" if fy < 2025 else f"$0.69 a quarter, the interim dividend declared in February 2026 (FY2025 10-K: '{DIVQ[fy]}')")
    for k in ("refining_quote", "transition_quote", "cloud_quote"):
        v.pop(k, None)
    if t["refq"]:
        v.update(refining_quote=t["refq"], transition_quote=t["ghg"])
    else:
        v["refining_exit_quote"] = t["refx"]
    if t["ai"]:
        v["ai_quote"] = t["ai"]
    return v


V12 = vintage4(V11, T21, 2021, "LB110")
V13 = vintage4(V12, T22, 2022, "LB111")
V14 = vintage4(V13, T23, 2023, "LB112")
V15 = vintage4(V14, T24, 2024, "LB113")
V16 = vintage4(V15, T25, 2025, "LB114")
assert sorted(V16["eps_normalized"]) == [str(y) for y in range(2016, 2025)] and list(V16["eps_excluded"]) == ["2025"]
assert "2011" not in V12["eps_normalized"] and "2012" in V12["eps_normalized"] and min(V16["revenue_usd_b"]) == "2016"

# ── dividends: each declared interim rate from the first filing that states it ──
DIV4 = [("Q2 2022", "10-Q", 1.19, "Dividends - common stock ($1.19 per share)"),
        ("Q2 2023", "release", 1.25, "Increased quarterly dividend by 5% to $1.25 per share"),
        ("Q2 2024", "release", 1.34, "Increased quarterly dividend by 7% to $1.34 per share"),
        ("Q2 2025", "10-Q", 1.37, "Dividends - common stock ($1.37 per share)"),
        ("FY2025", "10-K", 0.69, DIVQ4[2025])]
for qq, kind_, rate, s in DIV4:
    if kind_ == "10-K":
        sid, path = "LB114", F25
    elif kind_ == "10-Q":
        sid, path = QSID4[qq], doc(REL4[qq][1], "10-Q__")
    else:
        sid, path = SID4[qq], FREL4[qq]
    dividends.append(dict(published=SRC[sid]["published"], source=sid, quarterly=rate,
                          note=f"${rate:.2f} a quarter, the interim dividend rate first stated in the {qq} {kind_}",
                          quote=quote(path, s)))

# ── repurchase authorities: each annual meeting's program (display only, the share counts carry their effect) ──
BB4 = [("LB160", "0001489393-22-000028", "2022", "34,026,947 shares, until November 27, 2023"),
       ("LB161", "0001489393-23-000032", "2023", "34,042,250 shares, until November 19, 2024"),
       ("LB162", "0001489393-24-000025", "2024", "34,042,250 shares, until November 24, 2025"),
       ("LB163", "0001489393-25-000028", "2025", "34,042,250 shares, until November 23, 2026"),
       ("LB164", "0001489393-26-000034", "2026", "34,042,250 shares, until November 22, 2027")]
for sid, acc, yr, tail in BB4:
    fb = doc(acc, "8-K__")
    source(sid, acc, f"LyondellBasell Industries N.V. 8-K (the {yr} annual meeting)", fb, "the share repurchase authority")
    buybacks2.append(dict(published=SRC[sid]["published"], source=sid,
                          quote=quote(fb, "the Company’s shareholders approved a new share repurchase program authorizing the Company to "
                                          "repurchase up to 10% of the Company’s issued share capital as of the date of the Annual Meeting, "
                                          f"or {tail}"),
                          note="display only: the diluted share counts carry its effect",
                          text=f"the {yr} annual meeting's program to repurchase up to 10% of the shares ({tail.split(' shares')[0]})"))

facts = dict(
    _doc=("LyondellBasell Industries N.V. (NYSE: LYB), point-in-time facts for retro/build_lyb.py. Every value carries its source and "
          "the source's publication date (EDGAR acceptance time; at or after the 16:00 ET close it counts from the next trading day). "
          "Generated by retro/generators/lyb/gen_lyb.py from the filings' converted rows: each figure is read from its labelled row, "
          "the row is asserted present in its own filing, and every rate, margin, tax rate and rule-T value is computed."),
    ticker="LYB", sources=dict(sorted(SRC.items(), key=lambda kv: (kv[1]["published"], kv[0]))), listing=listing, distributions=[],
    history_vintages=[V1, V2, V3, V4, V5, V6, V7, V8, V9, V10, V11, V12, V13, V14, V15, V16], prints=prints, guides=[], dividends=dividends, events=[], company_names=[],
    buyback_programs=[dict(published=SRC["LB30"]["published"], source="LB30", quote=BUYBACK_Q,
                           note="display only: the diluted share counts carry its effect",
                           text="a share repurchase program for up to 10% of the shares from May 2013")] + buybacks2,
    rule_t=rule_t)

out = A.out or os.path.join(REPO, "retro", "facts", "LYB.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(facts, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_lyb.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump({k: sorted(set(v)) for k, v in CHECK.items()}, fh, indent=1, ensure_ascii=False)
print(f"wrote {out}: {len(prints)} prints, {len(facts["history_vintages"])} vintages, {len(dividends)} dividends; checklist {ck} "
      f"({sum(len(set(v)) for v in CHECK.values())} strings)")
for k, e in rule_t.items():
    print(f"  rule T {k}: {e['values']} -> {e['thresholds']}")
for p in prints:
    bp = lambda v: "n/r" if v is None else f"{v:+.0f}bp"
    print(f"  {p['quarter']} {p['published']} rev {p['sales_pct']:+.1f}% opm {bp(p['opm_bp'])} ptm {bp(p['ptm_bp'])} "
          f"O&P-A {p['opa_pct']} I&D {p['ind_pct']} eps {p['eps_q']} vs {p['eps_q_prior']} sh {p['diluted_shares_m']} | {p['release_time']}")
