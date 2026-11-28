#!/usr/bin/env python3
"""Extend retro/facts/OKE.json with 2010-2013 (filings accepted 2009-12-01 to 2013-12-31), asserting that every earlier fact is
unchanged. Same discipline as gen_oke.py: each raw figure is read from its own labelled row of a named table (the row text is kept in
the fact and written to the verbatim checklist) or from the sentence that holds it (asserted present word for word), every rate, margin
and change is computed, and every quote is asserted present in its own filing. Only filings accepted on or before 2013-12-31 are read.
The downloads (keep them outside the repo, e.g. the session scratchpad):

    python3 retro/tools/edgar.py index 1039684 <dir>
    python3 retro/tools/edgar.py fetch 1039684 <dir> --from 2009-10-01 --to 2013-12-31 --forms 8-K 8-K/A 10-K 10-K/A 10-Q

    python3 -I retro/generators/oke/gen_oke_1013.py --filings <dir> [--facts-in <2008-2009 sheet>] [--out retro/facts/OKE.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_oke_1013.json

--facts-in is the 2008-2009 sheet gen_oke.py writes (default: retro/facts/OKE.json, which must then hold 2008-2009 only).
What the batch reads and decides is in retro/README.md, "OKE 2010-2013".
"""
import argparse
import copy
import datetime as dt
import glob
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
_ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("--filings", required=True)
_ap.add_argument("--facts-in")
_ap.add_argument("--out")
_ap.add_argument("--checklist")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402

ET = ZoneInfo("America/New_York")
START, CUT = "2010-01-01", "2013-12-31"
CIK = 1039684
ROWS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("OKE")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
old = json.load(open(A.facts_in or os.path.join(REPO, "retro", "facts", "OKE.json"), encoding="utf-8"))
assert all(s["published"] <= "2009-12-31" for s in old["sources"].values()), "--facts-in must be the 2008-2009 sheet"
f = copy.deepcopy(old)
CHECK = {}
TEXT = {}
norm = lambda s: re.sub(r"\s+", " ", s).strip()


def path(acc, pat):
    hits = glob.glob(os.path.join(SP, "*", acc, pat))
    assert len(hits) == 1, (acc, pat, hits)
    return hits[0]


def lines(p):
    if p not in TEXT:
        TEXT[p] = open(p, encoding="utf-8", errors="replace").read().splitlines()
    return TEXT[p]


def joined(p):
    return norm(" ".join(lines(p)))


def quote(p, s):
    """A sentence or fragment, word for word in its filing (whitespace collapsed); added to the checklist."""
    assert norm(s) in joined(p), (os.path.basename(p), s[:120])
    CHECK.setdefault(p, []).append(s)
    return s


def num(t):
    t = t.replace(",", "").replace("$", "").strip()
    if t in ("—", "--", "–", "-", ""):
        return 0.0
    neg = t.startswith("(") and t.endswith(")")
    return -float(t.strip("()")) if neg else float(t)


NUMCELL = re.compile(r"^\(?-?[\d,]+(\.\d+)?\)?$|^[—–-]$")


def row(p, label, anchor=None, after=None, n=None, nth=0):
    """The nth row (from 0) of a converted HTML filing whose first cell matches `label`, at or after the first line matching `anchor`
    (and then `after`), whose other cells are numbers; returns (numbers, the row's text). The row goes to the checklist."""
    ls = lines(p)
    i = 0
    for a in [x for x in (anchor, after) if x]:
        i = next(k for k in range(i, len(ls)) if re.search(a, ls[k]))
    seen = 0
    for k in range(i, len(ls)):
        cells = [c.strip() for c in ls[k].split("|")]
        if re.fullmatch(label, cells[0]) and len(cells) > 1 and all(NUMCELL.match(c) for c in cells[1:] if c):
            vals = [num(c) for c in cells[1:] if c]
            if n is None or len(vals) == n:
                if seen == nth:
                    CHECK.setdefault(p, []).append(ls[k])
                    return vals, ls[k]
                seen += 1
    raise AssertionError((os.path.basename(p), label, anchor, after))


def pub(acc):
    """The date a filing counts from (the acceptance-time rule): EDGAR's UTC time in ET; at or after 16:00, the next trading day."""
    r = ROWS[acc]
    t = dt.datetime.fromisoformat(r[1].replace("Z", "+00:00")).astimezone(ET)
    day = t.date().isoformat()
    if (t.hour, t.minute) >= (16, 0):
        day = min(d for d in TDAYS if d > day)
    if (t.hour, t.minute) < (9, 30):
        when = f"accepted {t:%Y-%m-%d %H:%M} ET, before the open"
    elif (t.hour, t.minute) < (16, 0):
        when = f"accepted {t:%Y-%m-%d %H:%M} ET, during the session"
    else:
        when = f"accepted {t:%Y-%m-%d %H:%M} ET, after the close: counts from {day}"
    assert START <= day <= CUT or acc == "0001039684-09-000075", (acc, day)
    return day, when


SOURCES = {}
NEXT_ID = [max(int(k[2:]) for k in old["sources"]) + 1]


def src(acc, title, supports):
    sid = f"OK{NEXT_ID[0]}"
    NEXT_ID[0] += 1
    day, when = pub(acc)
    SOURCES[sid] = {"published": day, "filed": when, "title": title,
                    "url": f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc.replace('-', '')}/{acc}.txt", "supports": supports}
    return sid


pct1 = lambda a, b: round((b / a - 1) * 100 + 0.0, 1)
g1 = lambda a, b: round((b / a - 1) * 100 + 0.0, 1) if a > 0 else round((b - a) / abs(a) * 100 + 0.0, 1)   # over a loss's |value| (CAT)
m2 = lambda a, b: round(a / b * 100 + 0.0, 2)

# ── the 10-Ks: the FY2009-FY2012 vintages; the FY2009 10-K/A re-files two certifications only (no vintage) ───────────────────────────
K = {"F2009": "0000909281-10-000030", "F2010": "0001039684-11-000029", "F2011": "0001039684-12-000027", "F2012": "0001039684-13-000024"}
DK = {k: path(a, "10-K__*.rows.txt") for k, a in K.items()}
quote(path("0001039684-10-000025", "10-K_A__*.rows.txt"), "The purpose of this Amendment No. 1 to our Annual Report on Form 10-K for "
      "the year ended December 31, 2009, is to re-file Exhibits 31.1 and 31.2 to reference the proper periodic report in paragraph 1 of "
      "the certifications.")
quote(path("0001039684-10-000025", "10-K_A__*.rows.txt"), "this Amendment No. 1 does not change any previously reported financial "
      "results")

# ── the 2012 two-for-one split (a stock dividend; NYSE trading on the post-split basis from 2012-06-04, Yahoo's split date) ──
SPLIT_ACC = "0001039684-12-000059"
SPLIT_Q = quote(path(SPLIT_ACC, "8-K__*.rows.txt"), "On June 1, 2012, we completed our previously announced two-for-one split of our "
                "common stock. The two-for-one split was accomplished by a distribution on June 1, 2012, of one share of ONEOK common stock "
                "for each share outstanding and held by holders of record on May 24, 2012. ONEOK shares began trading on a post-split basis "
                "on the New York Stock Exchange beginning at the opening of trading on June 4, 2012.")
quote(path("0001039684-12-000017", "EX-99.1__*.rows.txt"), "ONEOK, Inc. (NYSE: OKE) today announced that its board of directors has "
      "authorized a two-for-one split of ONEOK common stock, subject to shareholder approval")

# the Q3 2009 release (OK21, in the 2008-2009 sheet): its nine-month columns give the Q4 2009 pre-tax income as the year less nine months
Q309 = path("0001039684-09-000075", "EX-99.1__*.rows.txt")
assert old["sources"]["OK21"]["url"].endswith("0001039684-09-000075.txt")

# ── sources, in date order ───────────────────────────────────────────────────────────────────────────────────────────────────────
S_G0122 = src("0000909281-10-000010", "ONEOK 8-K: 2010 earnings guidance; 2009 earnings guidance updated (Items 2.02, 7.01)",
              "the FY2009 EPS guide ($2.85-2.89 a diluted share) and the FY2010 net income guide")
S_D44 = src("0000909281-10-000012", "ONEOK 8-K: quarterly dividend of $0.44 (Item 8.01)", "the quarterly dividend rate, $0.44 a share")
S_R409 = src("0000909281-10-000023", "ONEOK Q4 2009 results (8-K exhibit 99.1; the earnings tables are not filed)",
             "Q4 2009: the Distribution segment's operating income (the release's text)")
S_K09 = src(K["F2009"], "ONEOK FY2009 10-K", "history vintage FY2009; Q4 2009's revenues, net margin, operating income and diluted EPS "
            "(quarterly financial data) and the year's pre-tax income and diluted shares; the 'why'")
plan = [("print", "Q1 2010", 2010, 1, "0000909281-10-000058", "Apr 28"),
        ("div", "0000909281-10-000108", 0.46),
        ("print", "Q2 2010", 2010, 2, "0000909281-10-000122", "Aug 3"),
        ("guide8k", "0001039684-10-000015", "ONEOK 8-K: 2010 earnings guidance updated (Item 7.01)"),
        ("div", "0001039684-10-000035", 0.48),
        ("print", "Q3 2010", 2010, 3, "0001039684-10-000039", "Nov 2"),
        ("guide8k", "0001039684-11-000006", "ONEOK 8-K: 2011 earnings guidance; 2010 outlook (Items 2.02, 7.01)"),
        ("div", "0001039684-11-000012", 0.52),
        ("print", "Q4 2010", 2010, 4, "0001039684-11-000024", "Feb 21"),
        ("k", "F2010"),
        ("print", "Q1 2011", 2011, 1, "0001039684-11-000053", "May 3"),
        ("div", "0001039684-11-000083", 0.56),
        ("print", "Q2 2011", 2011, 2, "0001039684-11-000090", "Aug 2"),
        ("guide8k", "0001039684-11-000111", "ONEOK 8-K: next-year financial guidance; the current-year range restated (Item 7.01)"),
        ("print", "Q3 2011", 2011, 3, "0001039684-11-000120", "Nov 1"),
        ("guide8k_div", "0001039684-12-000008", "ONEOK 8-K: quarterly dividend of $0.61; 2011 net income outlook (Items 2.02, 7.01, 8.01)",
         0.61),
        ("print", "Q4 2011", 2011, 4, "0001039684-12-000022", "Feb 20"),
        ("k", "F2011"),
        ("print", "Q1 2012", 2012, 1, "0001039684-12-000040", "May 1"),
        ("split",),
        ("div", "0001039684-12-000074", 0.33),
        ("print", "Q2 2012", 2012, 2, "0001039684-12-000077", "Jul 31"),
        ("guide8k", "0001039684-12-000097", "ONEOK 8-K: next-year financial guidance; the current-year range restated (Item 7.01)"),
        ("print", "Q3 2012", 2012, 3, "0001039684-12-000104", "Oct 30"),
        ("div", "0001039684-13-000006", 0.36),
        ("print", "Q4 2012", 2012, 4, "0001039684-13-000018", "Feb 25"),
        ("k", "F2012"),
        ("print", "Q1 2013", 2013, 1, "0001039684-13-000040", "Apr 30"),
        ("guide8k", "0001039684-13-000056", "ONEOK 8-K: energy services wind down; 2013 net income guidance updated (Items 2.05, 7.01)"),
        ("div", "0001039684-13-000076", 0.38),
        ("print", "Q2 2013", 2013, 2, "0001039684-13-000078", "Jul 30"),
        ("print", "Q3 2013", 2013, 3, "0001039684-13-000097", "Nov 5")]
SID_PRINT, SID_8K, SID_DIV, SID_K = {}, {}, {}, {"F2009": S_K09}
S_SPLIT = None
for step in plan:
    if step[0] == "print":
        _, q, fy, n, acc, rel = step
        SID_PRINT[q] = src(acc, f"ONEOK {q} results (8-K exhibit 99.1)",
                           f"{q}: revenues, net margin, operating income, income before income taxes, diluted EPS, diluted shares and the "
                           "Distribution segment's operating income; the EPS guide where the release gives one")
    elif step[0] in ("guide8k", "guide8k_div"):
        SID_8K[step[1]] = src(step[1], step[2], "the EPS guide (net income guidance) it states")
        if step[0] == "guide8k_div":
            SID_DIV[step[1]] = SID_8K[step[1]]
    elif step[0] == "div":
        SID_DIV[step[1]] = src(step[1], f"ONEOK 8-K: quarterly dividend of ${step[2]:.2f} (Item 8.01)",
                               f"the quarterly dividend rate, ${step[2]:.2f} a share")
    elif step[0] == "k":
        SID_K[step[1]] = src(K[step[1]], f"ONEOK {step[1].replace('F', 'FY')} 10-K", f"history vintage {step[1].replace('F', 'FY')}; the 'why'")
    elif step[0] == "split":
        S_SPLIT = src(SPLIT_ACC, "ONEOK 8-K: two-for-one stock split completed (Items 7.01, 8.01)",
                      "the 2012 two-for-one split: distribution on June 1, 2012, post-split trading from June 4, 2012")
srt_src = sorted(SOURCES.items(), key=lambda kv: (kv[1]["published"], int(kv[0][2:])))
assert [k for k, _ in srt_src] == sorted(SOURCES, key=lambda k: int(k[2:])), "source ids must follow publication order"

# ── history vintages: each year from the latest filing that reports it; the ten fiscal years to the latest one ─────────────────────
V8 = old["history_vintages"][-1]                     # the FY2008 vintage (2008-2009 sheet)
assert V8["fy_label"] == "FY08"
ST = r"^CONSOLIDATED STATEMENTS OF INCOME$"
I6 = r"^ITEM 6\.( \|)? SELECTED FINANCIAL DATA$"
SPUB = {**{k: v["published"] for k, v in old["sources"].items()}, **{k: v["published"] for k, v in SOURCES.items()}}


def item6_eps(fk):
    p = DK[fk]
    if fk in ("F2011", "F2012"):         # continuing operations under its own heading (the retail marketing business discontinued)
        return row(p, r"Diluted", I6, r"^Earnings per share - continuing operations$")
    if fk == "F2010":
        return row(p, r"Diluted earnings per share", I6)
    return row(p, r"Diluted earnings per share - continuing operations", I6)


def stmt(fk, label, n=3, after=None):
    return row(DK[fk], label, ST, after, n=n)


def why(fk, lead, extra):
    lo = joined(DK[fk]).lower()
    # DURABLE needs the company not to call its own business cyclical (the MU rule): the only use of the word is the billing cycle
    assert lo.count("cyclical") == lo.count("invoiced on a cyclical basis"), (fk, "a 10-K that calls the business cyclical")
    q = [quote(DK[fk], lead), quote(DK[fk], "Our cash flow depends heavily on the earnings and distributions of ONEOK Partners."),
         quote(DK[fk], extra)]
    label = fk.replace("F", "FY")
    return " ".join(f"'{x}'" for x in q) + (f" (the {label} 10-K's own words; it calls no business of the company cyclical, the word "
                                            "appearing only in its billing cycle, so DURABLE, the MU rule)")


def groups(fk):
    """Segment sales to unaffiliated customers (ONEOK Partners, Distribution, Energy Services), the last year and the one before."""
    out = []
    for l in lines(DK[fk]):
        if l.startswith("Sales to unaffiliated customers |"):
            cells = [num(c) for c in l.split("|")[1:] if c.strip()]
            if len(cells) == 5:
                out.append(cells)
                CHECK.setdefault(DK[fk], []).append(l)
        if len(out) == 2:
            break
    (cur, pri) = out
    return [[n, round(cur[i] / 1e6, 3), pct1(pri[i], cur[i])] for i, n in enumerate(["ONEOK Partners", "Distribution", "Energy Services"])]


def vintage(fk, fy, eps, rev, sh, lead, extra, div_q, div_sentence, restate_note):
    """eps / rev / sh: {year: (value, source id)}; the per-year sources give each year's publication date (on_basis)."""
    st = {"rev": stmt(fk, r"Revenues")[0], "oi": stmt(fk, r"Operating income")[0], "pti": stmt(fk, r"Income before income taxes")[0],
          "tax": [abs(x) for x in stmt(fk, r"Income taxes( \(Note [A-Z]\))?")[0]]}
    cf = r"^CONSOLIDATED STATEMENTS OF CASH FLOWS( \||$)"
    cfo = row(DK[fk], r"Cash provided by operating activities", cf, n=3)[0]
    cx = [abs(x) for x in row(DK[fk], r"Capital expenditures \(less allowance for equity funds used during construction\)", cf, n=3)[0]]
    rp = [abs(x) for x in row(DK[fk], r"Repurchase of common stock", cf, n=3)[0]]
    sid = SID_K[fk]
    years = sorted(eps)
    assert years == list(range(years[0], fy + 1)) and len(years) <= 10, (fk, years)
    first = years[0]
    v = {
        "published": SPUB[sid], "sources": sorted({sid} | {s for _, s in eps.values()} | {s for _, s in rev.values()}
                                                 | {s for _, s in sh.values()}, key=lambda s: -int(s[2:])),
        "company": "ONEOK, Inc.", "exchange": "NYSE", "symbol": "OKE",
        "business_line": V8["business_line"],
        "fy_label": f"FY{fy % 100:02d}", "fiscal_year_ends": {str(y): f"{y}-12-31" for y in years},
        "eps_normalized": {str(y): eps[y][0] for y in years}, "eps_sources": {str(y): eps[y][1] for y in years},
        "eps_published": {str(y): SPUB[eps[y][1]] for y in years},
        "eps_excluded": {}, "eps_first_excluded": V8["eps_first_excluded"] if first == 2002 else {},
        "revenue_usd_b": {str(y): round(rev[y][0] / 1e6, 6) if rev[y][1] in SOURCES else rev[y][0] for y in years},
        "revenue_sources": {str(y): rev[y][1] for y in years},
        "diluted_shares_m": {str(y): round(sh[y][0] / 1000, 3) if sh[y][1] in SOURCES else sh[y][0] for y in years},
        "shares_sources": {str(y): sh[y][1] for y in years},
        "shares_published": {str(y): SPUB[sh[y][1]] for y in years},
        "shares_note": "diluted average shares of common stock, millions (each statement of income)",
        "normalization": V8["normalization"] + "; " + restate_note,
        "pe_window_start": f"{first}-01-01",
        "prev_fy_op_margin": m2(st["oi"][0], st["rev"][0]),
        "prev_fy_op_margin_note": (f"FY{fy % 100:02d} operating income ${st['oi'][0] / 1000:,.1f}M / revenues ${st['rev'][0] / 1000:,.1f}M "
                                   f"(FY{fy} 10-K), the operating margin"),
        "check_pretax_margin": m2(st["pti"][0], st["rev"][0]),
        "check_pretax_note": (f"FY{fy % 100:02d} income before income taxes ${st['pti'][0] / 1000:,.1f}M / revenues ${st['rev'][0] / 1000:,.1f}M "
                              f"(FY{fy} 10-K); before the noncontrolling interests (ONEOK Partners' other unitholders), so the check "
                              "overstates ONEOK's own EPS"),
        "tax_rate": round(st["tax"][0] / st["pti"][0], 4),
        "tax_note": (f"FY{fy % 100:02d} income taxes ${st['tax'][0] / 1000:,.1f}M / income before income taxes ${st['pti'][0] / 1000:,.1f}M "
                     f"(FY{fy} 10-K)"),
        "prev_fy_sales_growth": pct1(st["rev"][1], st["rev"][0]),
        "dividend_annual": round(div_q * 4, 2),
        "dividend_note": f"${div_q:.2f} a quarter, ${div_q * 4:.2f} a year: '{quote(DK[fk], div_sentence)}' (FY{fy} 10-K)",
        "fcf_label": f"FY{fy % 100:02d}", "fcf_b": round((cfo[0] - cx[0]) / 1e6, 3),
        "fcf_note": (f"cash provided by operating activities ${cfo[0] / 1000:,.1f}M less capital expenditures ${cx[0] / 1000:,.1f}M "
                     f"(FY{fy} 10-K, consolidated, ONEOK Partners' included)"),
        "cash_return_text": f"repurchases of common stock ${rp[0] / 1000:,.1f}M in {fy} (FY{fy} 10-K's statement of cash flows)",
        "groups": groups(fk), "groups_basis": f"FY{fy % 100:02d} segment sales to unaffiliated customers (FY{fy} 10-K segment note; "
                                              "eliminations and Other left out)",
        "margin_signal_name": "Pre-tax margin change",
        "kind": "DURABLE", "kind_text": V8["kind_text"],
        "why": why(fk, lead, extra),
    }
    return v


# carried years from the FY2008 vintage, with their own sources
c_eps = {int(y): (v, V8["eps_sources"][y]) for y, v in V8["eps_normalized"].items()}
c_rev = {int(y): (v, V8["revenue_sources"][y]) for y, v in V8["revenue_usd_b"].items()}
c_sh = {int(y): (v, V8["shares_sources"][y]) for y, v in V8["diluted_shares_m"].items()}
LEAD = "We are a diversified energy company and successor to the company founded in 1906 known as Oklahoma Natural Gas Company."
X1 = "The volatility of natural gas, crude oil and NGL prices could adversely affect ONEOK Partners’ cash flow."
X2 = "The volatility of natural gas, crude oil and NGL prices could affect adversely ONEOK Partners’ cash flow."
V = []
# FY2009 10-K: 2005-2009 EPS from Item 6 (2005 and 2006 stay at the company's figures without the gains on sale), 2007-2009 statements
e, _ = item6_eps("F2009")
assert e == [2.87, 2.95, 2.79, 2.68, 3.73], e
r, _ = stmt("F2009", r"Revenues")
s, _ = stmt("F2009", r"Diluted", after=r"(?i)^Average shares")
eps09 = {**c_eps, 2007: (e[2], S_K09), 2008: (e[1], S_K09), 2009: (e[0], S_K09)}
rev09 = {**c_rev, 2007: (r[2], S_K09), 2008: (r[1], S_K09), 2009: (r[0], S_K09)}
sh09 = {**c_sh, 2007: (s[2], S_K09), 2008: (s[1], S_K09), 2009: (s[0], S_K09)}
V.append(vintage("F2009", 2009, eps09, rev09, sh09, LEAD, X1, 0.44, "In January 2010, we declared a dividend of $0.44 per share ($1.76 "
                 "per share on an annualized basis) for the fourth quarter of 2009", "2007-2009 from the FY2009 10-K, GAAP (no year's listed "
                 "items approach its income: 2009's gain on sale of assets $4.8M)"))
# FY2010 10-K: 2006-2010 EPS from Item 6, 2008-2010 statements
e, _ = item6_eps("F2010")
assert e == [3.10, 2.87, 2.95, 2.79, 2.68], e
r, _ = stmt("F2010", r"Revenues")
s, _ = stmt("F2010", r"Diluted", after=r"(?i)^Average shares")
S10 = SID_K["F2010"]
eps10 = {**eps09, 2007: (e[3], S10), 2008: (e[2], S10), 2009: (e[1], S10), 2010: (e[0], S10)}
rev10 = {**rev09, 2008: (r[2], S10), 2009: (r[1], S10), 2010: (r[0], S10)}
sh10 = {**sh09, 2008: (s[2], S10), 2009: (s[1], S10), 2010: (s[0], S10)}
X10 = quote(DK["F2010"], "Additionally, 2010 results for ONEOK Partners’ natural gas liquids business include the gain on the sale of a "
            "49-percent ownership interest in Overland Pass Pipeline Company.")
V.append(vintage("F2010", 2010, eps10, rev10, sh10, LEAD, X1, 0.52, "In January 2011, we declared a dividend of $0.52 per share ($2.08 "
                 "per share on an annualized basis) for the fourth quarter of 2010", "2010 from the FY2010 10-K at GAAP $3.10: its one listed "
                 "item, the $16.3M gain on the sale of a 49-percent interest in Overland Pass Pipeline Company (4 cents a share, the Q4 2010 "
                 "release), is far under half the year's income, and no filing publishes EPS without it"))
# FY2011 10-K: EPS from continuing operations, 2007-2011 restated for the retail marketing business (discontinued, sold 2012-02-01);
# 2009-2011 statements restated likewise; 2003-2006 as earlier filings report them (a seam, as published)
e, _ = item6_eps("F2011")
assert e == [3.34, 3.09, 2.80, 2.91, 2.74], e
r, _ = stmt("F2011", r"Revenues")
s, _ = stmt("F2011", r"Diluted", after=r"(?i)^Average shares")
S11 = SID_K["F2011"]
eps11 = {**eps10, 2007: (e[4], S11), 2008: (e[3], S11), 2009: (e[2], S11), 2010: (e[1], S11), 2011: (e[0], S11)}
rev11 = {**rev10, 2009: (r[2], S11), 2010: (r[1], S11), 2011: (r[0], S11)}
sh11 = {**sh10, 2009: (s[2], S11), 2010: (s[1], S11), 2011: (s[0], S11)}
X11 = quote(DK["F2011"], "Earnings per share - continuing operations")
V.append(vintage("F2011", 2011, eps11, rev11, sh11, LEAD, X2, 0.61, "In January 2012, we declared a dividend of $0.61 per share ($2.44 "
                 "per share on an annualized basis) for the fourth quarter of 2011", "2007-2011 from the FY2011 10-K's Item 6, 'Earnings per "
                 "share - continuing operations' (the retail natural gas marketing business, sold to Constellation Energy on February 1, 2012, "
                 "in discontinued operations), and 2009-2011 revenues restated likewise; 2002-2006 as their own filings report them (a seam, "
                 "as published); GAAP (no listed item near the year's income)"))
# FY2012 10-K: per-share figures on the post-split basis (2008-2012 from Item 6); 2003-2007 from earlier filings, before the split
# (on_basis halves them); the ten fiscal years to the latest one, so FY2002 and the FY2001 note leave
e, _ = item6_eps("F2012")
assert e == [1.64, 1.67, 1.55, 1.40, 1.45], e
r, _ = stmt("F2012", r"Revenues")
s, _ = stmt("F2012", r"Diluted", after=r"(?i)^Average shares")
S12 = SID_K["F2012"]
eps12 = {**eps11, 2008: (e[4], S12), 2009: (e[3], S12), 2010: (e[2], S12), 2011: (e[1], S12), 2012: (e[0], S12)}
rev12 = {**rev11, 2010: (r[2], S12), 2011: (r[1], S12), 2012: (r[0], S12)}
sh12 = {**sh11, 2010: (s[2], S12), 2011: (s[1], S12), 2012: (s[0], S12)}
for d in (eps12, rev12, sh12):
    del d[2002]
X12 = quote(DK["F2012"], "We also recognized an expense of $10.3 million related to the impairment of our goodwill in the first quarter "
            "2012.")
V.append(vintage("F2012", 2012, eps12, rev12, sh12, "We are a diversified energy company and successor to the company founded in 1906 "
                 "as Oklahoma Natural Gas Company.", X2, 0.36, "In January 2013, we declared a dividend of $0.36 per share ($1.44 per share "
                 "on an annualized basis)", "2008-2012 from the FY2012 10-K's Item 6 on the post-split basis; 2012 at GAAP (its listed items, "
                 "the $10.3M goodwill impairment and the $13.5M after-tax gain on the retail marketing sale, are far under its income); the "
                 "ten fiscal years to the latest one, so FY2002 and the FY2001 note leave the history and the window starts with 2003"))
for v in V:
    assert all(v["eps_published"][y] <= v["published"] for y in v["eps_normalized"])
# the split's basis: every per-share fact published before 2012-06-04 is pre-split; the FY2012 10-K is post-split
assert V[-1]["eps_published"]["2007"] < "2012-06-04" <= V[-1]["published"]

# ── the prints ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
NEXT = {1: "Q2 print (early August)", 2: "Q3 print (early November)", 3: "Q4 and full-year print, with the 10-K (late February)",
        4: "Q1 print (late April or early May)"}
PR = []


def fmt_e(x):
    return f"${x:.2f}" if x >= 0 else f"$({-x:.2f})"


def fm(x):
    return f"${x:,.1f}M" if x >= 0 else f"$({-x:,.1f})M"


def finish(d, cash_k, pti_label_note):
    r = d["raw"]
    d.update({"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": g1(r["rev_prior_m"], r["rev_m"]),
              "nm_pct": g1(r["nm_prior_m"], r["nm_m"]), "dist_pct": g1(r["dist_prior_m"], r["dist_m"]),
              "opm": m2(r["oi_m"], r["rev_m"]), "opm_bp": round((m2(r["oi_m"], r["rev_m"]) - m2(r["oi_prior_m"], r["rev_prior_m"])) * 100, 1),
              "ptm": m2(r["pti_m"], r["rev_m"]), "ptm_bp": round((m2(r["pti_m"], r["rev_m"]) - m2(r["pti_prior_m"], r["rev_prior_m"])) * 100, 1),
              "eps_q": r["eps_q"], "eps_q_prior": r["eps_q_prior"], "diluted_shares_m": r["dil_sh_m"],
              "sales_note": f"revenues ${r['rev_m']:,.1f}M vs ${r['rev_prior_m']:,.1f}M a year earlier",
              "nm_note": f"net margin ${r['nm_m']:,.1f}M vs ${r['nm_prior_m']:,.1f}M",
              "dist_note": (f"Distribution operating income {fm(r['dist_m'])} vs {fm(r['dist_prior_m'])}"
                            + ("; growth over the year-ago loss's absolute value (the CAT rule)" if r["dist_prior_m"] < 0 else "")),
              "margin_note": f"operating income ${r['oi_m']:,.1f}M, income before income taxes ${r['pti_m']:,.1f}M{pti_label_note}",
              "eps_note": f"diluted {fmt_e(r['eps_q'])} vs {fmt_e(r['eps_q_prior'])}",
              "cash_note": f"cash and cash equivalents ${cash_k / 1000:,.1f}M at the quarter's end (consolidated)",
              "next_print": NEXT[d["q"]]})
    PR.append(d)


# Q4 2009: the release files no earnings tables (it links to them on the website, unused), so the quarter comes from the FY2009 10-K's
# quarterly financial data (revenues, net margin, operating income, diluted EPS), its pre-tax income as the year less the nine months
# of the Q3 2009 release, its diluted shares as the year's (no quarterly count is filed), and the Distribution segment from the
# release's text (the NEM 'source_10k' encoding)
p4, pk = path("0000909281-10-000023", "EX-99.1__*.rows.txt"), DK["F2009"]
quote(p4, "View earnings tables (link)")
QD = r"^S\. QUARTERLY FINANCIAL DATA \(UNAUDITED\)$"
rq9, t1 = row(pk, r"Total revenues", QD)
rq8, t2 = row(pk, r"Total revenues", QD, r"^Year Ended December 31, 2008")
nq9, t3 = row(pk, r"Net margin", QD)
nq8, t4 = row(pk, r"Net margin", QD, r"^Year Ended December 31, 2008")
oq9, t5 = row(pk, r"Operating income", QD)
oq8, t6 = row(pk, r"Operating income", QD, r"^Year Ended December 31, 2008")
eq9, t7 = row(pk, r"Diluted", QD)
eq8, t8 = row(pk, r"Diluted", QD, r"^Year Ended December 31, 2008")
pty, t9 = stmt("F2009", r"Income before income taxes")
pt9m, t10 = row(Q309, r"Income before income taxes", r"^CONSOLIDATED STATEMENTS OF INCOME$")
shy, t11 = stmt("F2009", r"Diluted", after=r"(?i)^Average shares")
cash, t12 = row(pk, r"Cash and cash equivalents", r"^CONSOLIDATED BALANCE SHEETS$")
DQ = quote(p4, "The distribution segment reported operating income of $79.5 million in the fourth quarter 2009, compared with $71.2 "
               "million in the fourth quarter 2008.")
dq = [float(x) for x in re.findall(r"\$([\d.]+) million", DQ)]
EQ = quote(p4, "Fourth-quarter 2009 net income attributable to ONEOK was $93.4 million, or 87 cents per diluted share, compared with "
               "$68.2 million, or 65 cents per diluted share, in the same period in 2008.")
assert (eq9[3], eq8[3]) == (0.87, 0.65)
d = {"quarter": "Q4 2009", "fy": 2009, "q": 4, "published": max(SPUB[S_R409], SPUB[S_K09]), "source": S_R409, "source_10k": S_K09,
     "sources_extra": ["OK21"], "release": "Feb 22", "release_time": SOURCES[S_R409]["filed"] + "; the FY2009 10-K "
                                                                                      + SOURCES[S_K09]["filed"],
     "raw": {"rev_m": rq9[3] / 1000, "rev_prior_m": rq8[3] / 1000, "nm_m": nq9[3] / 1000, "nm_prior_m": nq8[3] / 1000,
             "oi_m": oq9[3] / 1000, "oi_prior_m": oq8[3] / 1000, "pti_m": (pty[0] - pt9m[2]) / 1000, "pti_prior_m": (pty[1] - pt9m[3]) / 1000,
             "dist_m": dq[0], "dist_prior_m": dq[1], "eps_q": eq9[3], "eps_q_prior": eq8[3], "dil_sh_m": round(shy[0] / 1000, 3)},
     "rows": {"revenues": [t1, t2], "net_margin": [t3, t4], "operating_income": [t5, t6], "eps": [t7, t8], "pretax_year": t9,
              "pretax_nine_months": t10, "shares_year": t11, "cash": t12, "distribution": DQ, "eps_release": EQ},
     "source_title": "ONEOK Q4 2009: the FY2009 10-K's quarterly financial data and statements (the release files no tables)"}
assert SPUB[S_R409] == SPUB[S_K09], "the release and the 10-K count from the same day"
finish(d, cash[0], "; the quarter from the FY2009 10-K (the release files no earnings tables): pre-tax income the year less the nine "
                   "months of the Q3 2009 release, diluted shares the year's")
d["sales_note"] += " (the FY2009 10-K's quarterly financial data)"


def prt(q, fy, n, acc, rel):
    sid = SID_PRINT[q]
    p = path(acc, "EX-99.1__*.rows.txt")
    rv, t_rv = row(p, r"Revenues", ST)
    nm, t_nm = row(p, r"Net margin", ST)
    oi, t_oi = row(p, r"Operating income", ST)
    pti, t_pt = row(p, r"Income before income taxes", ST)
    try:
        eps, t_e = row(p, r"Net earnings per share, diluted", ST)
    except AssertionError:                      # from Q4 2011: continuing operations under 'Diluted earnings per share:'
        eps, t_e = row(p, r"Income from continuing operations", ST, r"^Diluted earnings per share:?$")
    sh, t_s = row(p, r"Diluted", ST, r"(?i)^Average shares")
    ds, t_d = row(p, r"Operating income( \(loss\))?", r"(?i)INFORMATION AT A GLANCE", r"(?i)^(Natural Gas )?Distribution$")
    cash, t_c = row(p, r"Cash and cash equivalents", r"^CONSOLIDATED BALANCE SHEETS$")
    d = {"quarter": q, "fy": fy, "q": n, "published": SPUB[sid], "source": sid, "release": rel, "release_time": SOURCES[sid]["filed"],
         "raw": {"rev_m": rv[0] / 1000, "rev_prior_m": rv[1] / 1000, "nm_m": nm[0] / 1000, "nm_prior_m": nm[1] / 1000,
                 "oi_m": oi[0] / 1000, "oi_prior_m": oi[1] / 1000, "pti_m": pti[0] / 1000, "pti_prior_m": pti[1] / 1000,
                 "dist_m": ds[0], "dist_prior_m": ds[1], "eps_q": eps[0], "eps_q_prior": eps[1], "dil_sh_m": round(sh[0] / 1000, 3)},
         "rows": {"revenues": t_rv, "net_margin": t_nm, "operating_income": t_oi, "pretax": t_pt, "eps": t_e, "shares": t_s,
                  "distribution": t_d, "cash": t_c},
         "source_title": SOURCES[sid]["title"]}
    finish(d, cash[0], "")
    if "continuing" in t_e:
        d["eps_note"] += " from continuing operations (the retail marketing business discontinued from the Q4 2011 release)"
    if d["published"] >= "2012-06-04":
        assert sh[0] > 200000, (q, "a post-split print reports post-split shares")


for step in plan:
    if step[0] == "print":
        prt(*step[1:])
# each Q4 print came a trading day or less before its 10-K, and no weekly date falls between them
for q, fk in (("Q4 2010", "F2010"), ("Q4 2011", "F2011"), ("Q4 2012", "F2012")):
    p = next(x for x in PR if x["quarter"] == q)
    k = SPUB[SID_K[fk]]
    assert p["published"] < k and [d for d in TDAYS if p["published"] < d <= k] == [k], (q, "the 10-K comes the next trading day")
assert [p["published"] for p in PR] == sorted(p["published"] for p in PR)

# ── EPS guides: ONEOK's GAAP net income guidance for the year (from 2010 a dollar range, before it a per-share range) ───────────────
EG = []


def eguide(fy, sid, acc, doc, s, lo, hi, unit):
    cands = sorted(glob.glob(os.path.join(SP, "*", acc, "EX-99*.rows.txt")) + glob.glob(os.path.join(SP, "*", acc, "8-K__*.rows.txt")))
    hits = [c for c in cands if norm(s) in joined(c)]
    assert hits, (doc, s[:80])
    qt = quote(hits[0], s)
    g = {"fy": fy, "published": SPUB[sid], "source": sid, "doc": doc, "quote": qt}
    if unit == "share":
        assert f"${lo:.2f} to ${hi:.2f}" in qt, (doc, lo, hi)
        g["eps_guide"] = [lo, hi]
    elif unit == "words":
        g["words"] = True
    else:
        assert f"${lo:.0f} million to ${hi:.0f} million" in qt, (doc, lo, hi)
        g["ni_guide_m"] = [lo, hi]
        # the per-share figure: net income over the diluted shares of the latest print public on the guide's date (its own release's
        # where it is in one; the KMI rule, OKE's guides having no per-share figure from 2010)
        shp = [p for p in PR if p["published"] <= g["published"]] or [x for x in old["prints"] if x["published"] <= g["published"]]
        g["shares_print"] = shp[-1]["quarter"]
    EG.append(g)


G0122 = "0000909281-10-000010"
eguide(2009, S_G0122, G0122, "8-K of 2010-01-25", "ONEOK expects its 2009 results to be in the range of $2.85 to $2.89 per diluted share",
       2.85, 2.89, "share")
eguide(2010, S_G0122, G0122, "8-K of 2010-01-25", "Our 2010 net income is expected to be in the range of $300 million to $335 million.",
       300, 335, "m")
P = SID_PRINT
eguide(2010, P["Q1 2010"], "0000909281-10-000058", "Q1 2010 release", "ONEOK also reaffirmed its 2010 net income guidance, announced on "
       "Jan. 19, 2010, in the range of $300 million to $335 million.", 300, 335, "m")
eguide(2010, P["Q2 2010"], "0000909281-10-000122", "Q2 2010 release", "ONEOK also reaffirmed its 2010 net income guidance in the range of "
       "$300 million to $335 million.", 300, 335, "m")
eguide(2010, SID_8K["0001039684-10-000015"], "0001039684-10-000015", "8-K of 2010-10-05", "Our 2010 net income is expected to be in the "
       "range of $320 million to $335 million, compared with our previous range of $300 million to $335 million provided on January 19, "
       "2010.", 320, 335, "m")
eguide(2010, P["Q3 2010"], "0001039684-10-000039", "Q3 2010 release", "ONEOK reaffirmed its 2010 net income guidance that was updated on "
       "Sept. 30, 2010, to be in the range of $320 million to $335 million", 320, 335, "m")
G0121 = "0001039684-11-000006"
eguide(2010, SID_8K[G0121], G0121, "8-K of 2011-01-21", "ONEOK also announced that its 2010 net income is expected to be at the high end of "
       "the earnings guidance range of $320 million to $335 million", None, None, "words")
eguide(2011, SID_8K[G0121], G0121, "8-K of 2011-01-21", "ONEOK’s 2011 net income is expected to be in the range of $325 million to $360 "
       "million", 325, 360, "m")
eguide(2011, P["Q1 2011"], "0001039684-11-000053", "Q1 2011 release", "ONEOK also reaffirmed its 2011 net income guidance, announced on "
       "Jan. 18, 2011, in the range of $325 million to $360 million.", 325, 360, "m")
eguide(2011, P["Q2 2011"], "0001039684-11-000090", "Q2 2011 release", "ONEOK also updated its 2011 net income guidance to the range of $325 "
       "million to $345 million compared with the previous guidance of $325 million to $360 million.", 325, 345, "m")
G0928 = "0001039684-11-000111"
eguide(2011, SID_8K[G0928], G0928, "8-K of 2011-09-29", "its current 2011 guidance range of $325 million to $345 million", 325, 345, "m")
eguide(2012, SID_8K[G0928], G0928, "8-K of 2011-09-29", "ONEOK’s 2012 net income is expected to be in the range of $355 million to $400 "
       "million", 355, 400, "m")
eguide(2011, P["Q3 2011"], "0001039684-11-000120", "Q3 2011 release", "ONEOK also increased its 2011 net income guidance to the range of "
       "$345 million to $365 million", 345, 365, "m")
G0120 = "0001039684-12-000008"
eguide(2011, SID_8K[G0120], G0120, "8-K of 2012-01-23", "ONEOK expects its 2011 net income to be in a range of $355 million to $365 million",
       355, 365, "m")
eguide(2012, P["Q4 2011"], "0001039684-12-000022", "Q4 2011 release", "ONEOK also increased its 2012 net income guidance to the range of "
       "$360 million to $410 million", 360, 410, "m")
eguide(2012, P["Q1 2012"], "0001039684-12-000040", "Q1 2012 release", "ONEOK reaffirmed its 2012 net income guidance range of $360 million "
       "to $410 million, provided on Feb. 20, 2012.", 360, 410, "m")
eguide(2012, P["Q2 2012"], "0001039684-12-000077", "Q2 2012 release", "ONEOK updated its 2012 net income guidance range to $345 million to "
       "$375 million, compared with the previous range of $360 million to $410 million.", 345, 375, "m")
G0924 = "0001039684-12-000097"
eguide(2012, SID_8K[G0924], G0924, "8-K of 2012-09-25", "its current 2012 guidance range of $345 million to $375 million", 345, 375, "m")
eguide(2013, SID_8K[G0924], G0924, "8-K of 2012-09-25", "ONEOK's 2013 net income is expected to be in the range of $405 million to $455 "
       "million", 405, 455, "m")
eguide(2012, P["Q3 2012"], "0001039684-12-000104", "Q3 2012 release", "ONEOK affirmed its 2012 net income guidance range of $345 million to "
       "$375 million.", 345, 375, "m")
eguide(2013, P["Q4 2012"], "0001039684-13-000018", "Q4 2012 release", "ONEOK reduced its 2013 net income guidance range to $350 million to "
       "$400 million, compared with the previous guidance range of $405 million to $455 million announced on Sept. 24, 2012.", 350, 400, "m")
eguide(2013, P["Q1 2013"], "0001039684-13-000040", "Q1 2013 release", "ONEOK reaffirmed its 2013 net income guidance range of $350 million "
       "to $400 million, provided on Feb. 25, 2013.", 350, 400, "m")
G0611 = "0001039684-13-000056"
eguide(2013, SID_8K[G0611], G0611, "8-K of 2013-06-12", "The updated 2013 net income guidance is expected to be in the range of $235 million "
       "to $285 million, compared with its previously announced net income guidance range of $350 million to $400 million.", 235, 285, "m")
quote(path(G0611, "EX-99.1__*.rows.txt"), "ONEOK's updated 2013 net income guidance now reflects the expected one-time charges and "
      "operating losses in the energy services segment.")
eguide(2013, P["Q2 2013"], "0001039684-13-000078", "Q2 2013 release", "ONEOK affirmed its 2013 net income guidance range of $235 million to "
       "$285 million announced on June 10, 2013.", 235, 285, "m")
eguide(2013, P["Q3 2013"], "0001039684-13-000097", "Q3 2013 release", "ONEOK also updated its 2013 net income guidance range to $245 "
       "million to $275 million, compared with the previous guidance range of $235 million to $285 million", 245, 275, "m")
EG.sort(key=lambda g: (g["published"], g["fy"]))
for g in EG:                                     # the doc label carries the date the fact counts from
    if g["doc"].startswith("8-K of"):
        assert g["doc"] == f"8-K of {g['published']}", (g["doc"], g["published"])
# the 2013-12-02 8-K (2014 guidance; ONE Gas' 2014 net income) states no 2013 range: the FY2014 guides are current only from the Q4 2013
# print, after the range
assert "2013 net income" not in joined(path("0001039684-13-000108", "EX-99.1__*.rows.txt")).replace("2013 net income guidance", "")

# ── dividends: each rate change from the first filing that states it as declared ──
DV = []
DIVQ = {"0000909281-10-000012": ("On January 20, 2010, our board of directors declared a fourth-quarter 2009 dividend of 44 cents per share "
                                 "of common stock", 0.44, S_D44),
        "0000909281-10-000108": ("announced an increase in our quarterly dividend to 46 cents per share of common stock from 44 cents per "
                                 "share", 0.46, None),
        "0001039684-10-000035": ("announced an increase in our quarterly dividend to 48 cents per share of common stock from 46 cents per "
                                 "share", 0.48, None),
        "0001039684-11-000012": ("announced an increase in our quarterly dividend to 52 cents per share of common stock from 48 cents per "
                                 "share", 0.52, None),
        "0001039684-11-000083": ("On July 20, 2011, we announced a second-quarter 2011 dividend of 56 cents per share of common stock", 0.56,
                                 None),
        "0001039684-12-000008": ("On January 18, 2012, our board of directors approved a dividend of 61 cents per share of common stock "
                                 "effective for the fourth quarter 2011", 0.61, None),
        "0001039684-12-000074": ("On July 25, 2012, we announced that our board of directors approved a second-quarter 2012 dividend of 33 "
                                 "cents per share of common stock", 0.33, None),
        "0001039684-13-000006": ("On January 16, 2013, we announced that our board of directors approved a cash dividend of 36 cents per "
                                 "share of common stock", 0.36, None),
        "0001039684-13-000076": ("On July 24, 2013, we announced that our board of directors approved a cash dividend of 38 cents per share "
                                 "of common stock", 0.38, None)}
for acc, (s, qd, sid) in DIVQ.items():
    sid = sid or SID_DIV[acc]
    qt = quote(path(acc, "8-K__*.rows.txt"), s)
    DV.append({"published": SPUB[sid], "quarterly": qd, "source": sid,
               "note": f"${qd:.2f} a quarter, ${qd * 4:.2f} a year: '{qt}' (ONEOK 8-K of {SPUB[sid]})"})
# unchanged rates (read by their text): 2011-04-20 ($0.52), 2011-10-27 and its 8-K/A of 2011-10-31 ($0.56), 2012-04-23 ($0.61),
# 2012-10-25 ($0.33), 2013-04-19 ($0.36), 2013-10-24 ($0.38)
for acc, c in (("0001039684-11-000045", 52), ("0001039684-11-000115", 56), ("0001039684-12-000038", 61), ("0001039684-12-000101", 33),
               ("0001039684-13-000035", 36), ("0001039684-13-000094", 38)):
    assert f"dividend of {c} cents per share" in joined(path(acc, "8-K__*.rows.txt")), acc
DV.sort(key=lambda x: x["published"])

# ── the split record (the shared on_basis helper restates every per-share fact published before it) ──
SPLITS = [{"effective": "2012-06-04", "ratio": 2.0, "source": S_SPLIT,
           "note": (f"'{SPLIT_Q}' ({S_SPLIT}); Yahoo's split date is 2012-06-04, the first trading day on the new basis. Per-share figures "
                    "published before 2012-06-04 are halved and share counts doubled (on_basis); the Q2 2012 release and later filings "
                    "report on the new basis ('split-adjusted')")}]
assert SPUB[S_SPLIT] > "2012-06-04" and not [d for d in TDAYS if "2012-06-04" <= d < SPUB[S_SPLIT] and
                                               dt.date.fromisoformat(d).weekday() == 4], "no weekly date before the split's source"

# ── assemble ──
for k in ("history_vintages", "prints", "eps_guides", "dividends"):
    assert all(x["published"] <= "2009-12-31" for x in f[k]), k
f["sources"] = {**old["sources"], **dict(sorted(SOURCES.items(), key=lambda kv: int(kv[0][2:])))}
f["history_vintages"] = old["history_vintages"] + V
f["prints"] = old["prints"] + PR
f["eps_guides"] = old["eps_guides"] + EG
f["dividends"] = old["dividends"] + DV
f["splits"] = SPLITS
f["price_basis"] = ("Yahoo OKE, split-adjusted to today's shares: its 2:1 of 2001-06-12 precedes the P/E window (2002-01-01 on) and every "
                    "per-share fact; its 2:1 of 2012-06-04 is the 'splits' record (before it the builder multiplies Yahoo's close by 2, after "
                    "it the per-share facts published before it are halved, on_basis); its 11422:10000 factor of 2014-02-03 (the ONE Gas "
                    "separation, a distribution, not a split) follows every built date, so the builder multiplies Yahoo's close by it, which "
                    "gives the close as traded; the builder refuses dates from 2014-02-03 until it is encoded")
f["_doc"] = old["_doc"].replace("Generated by retro/generators/oke/gen_oke.py", "Generated by retro/generators/oke/gen_oke.py (2008-2009) "
                                "and gen_oke_1013.py (2010-2013)")
assert all(s["published"] <= CUT for s in f["sources"].values())
for k in ("rule_t", "listings", "company_names", "events", "guides"):
    assert f[k] == old[k], k
out = A.out or os.path.join(REPO, "retro", "facts", "OKE.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(f, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_oke_1013.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump({k: v for k, v in CHECK.items() if v}, fh, ensure_ascii=False, indent=1)
print(f"{out}: +{len(V)} vintages, +{len(PR)} prints, +{len(EG)} EPS guides, +{len(DV)} dividends, +{len(SOURCES)} sources; "
      f"{sum(len(v) for v in CHECK.values())} quotes in {ck}")
for p in PR:
    print(p["quarter"], p["published"], p["sales_pct"], p["nm_pct"], p["dist_pct"], p["opm_bp"], p["ptm_bp"], p["eps_q"], p["eps_q_prior"],
          p["diluted_shares_m"])
for g in EG:
    print(g["fy"], g["published"], g["doc"], g.get("eps_guide") or g.get("ni_guide_m") or "words", g.get("shares_print"))
