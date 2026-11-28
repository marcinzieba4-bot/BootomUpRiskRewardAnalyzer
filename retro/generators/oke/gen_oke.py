#!/usr/bin/env python3
"""Generate retro/facts/OKE.json (2008-2009) from ONEOK, Inc.'s own filings (edgar.py's converted documents).

Every raw figure is read from its own filing: in the HTML filings (FY2002 10-K on) from its labelled row of a named table (the row
text is kept in the fact and written to the verbatim checklist); in the plain-text filings (FY1998-FY2001 10-Ks) it is typed once with
the snippet of the filing that holds it, and the script asserts the snippet is there (whitespace, table rules, '|' and '$' flattened on
both sides) and that the typed figures are consecutive numbers in it. Every rate, margin, change and rule-T value is computed, never
typed; every quoted sentence is asserted present in its own filing word for word and written to the verbatim checklist
(retro/tools/verbatim.py). Only filings accepted on or before 2009-12-31 are read. The downloads (keep them outside the repo, e.g. in
the session scratchpad):

    python3 retro/tools/edgar.py index 1039684 <dir>
    python3 retro/tools/edgar.py fetch 1039684 <dir> --from 1998-09-01 --to 2006-12-31 --forms 10-K 10-K405 10-K/A
    python3 retro/tools/edgar.py fetch 1039684 <dir> --from 2007-01-01 --to 2010-01-21 --forms 8-K 8-K/A 10-K 10-K/A 10-Q

    python3 -I retro/generators/oke/gen_oke.py --filings <dir> [--out retro/facts/OKE.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_oke.json
"""
import argparse
import datetime as dt
import glob
import json
import math
import os
import re
import sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
_ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("--filings", required=True)
_ap.add_argument("--out")
_ap.add_argument("--checklist")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402

ET = ZoneInfo("America/New_York")
CUT = "2009-12-31"
CIK = 1039684
ROWS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("OKE")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
CHECK = {}


def path(acc, pat):
    hits = glob.glob(os.path.join(SP, "*", acc, pat))
    assert len(hits) == 1, (acc, pat, hits)
    return hits[0]


TEXT = {}


def flat(s):
    s = s.replace("|", " ").replace("$", " ")
    s = re.sub(r"\.{3,}", " ", s)
    s = re.sub(r"</?(S|C|TABLE|CAPTION|PAGE)>", " ", s)
    s = " ".join(t for t in s.split() if not re.fullmatch(r"[-=_]{3,}", t))
    return s


def text(p):
    if p not in TEXT:
        with open(p, encoding="utf-8" if p.endswith(".rows.txt") else "latin-1", errors="replace") as fh:
            raw = fh.read()
        TEXT[p] = (re.sub(r"\s+", " ", raw), flat(raw), raw.splitlines())
    return TEXT[p]


def quote(p, s):
    """A sentence or fragment, word for word in its filing (whitespace collapsed); added to the checklist."""
    assert re.sub(r"\s+", " ", s) in text(p)[0], (p, s[:120])
    CHECK.setdefault(p, []).append(s)
    return s


def num(t):
    t = t.replace(",", "").replace("$", "").strip()
    if t in ("—", "--", "–", "-", ""):
        return 0.0
    neg = t.startswith("(") and t.endswith(")")
    return -float(t.strip("()")) if neg else float(t)


def S(p, snippet, *toks):
    """The snippet is in the filing p (flattened), and the typed figures are consecutive numbers in it; returns them."""
    f = flat(snippet)
    assert f in text(p)[1], (os.path.basename(p), snippet[:140])
    words = f.split()
    n = len(toks)
    assert any(words[i:i + n] == list(toks) for i in range(len(words) - n + 1)), (snippet[:100], toks)
    CHECK.setdefault(p, [])
    return [num(t) for t in toks]


NUMCELL = re.compile(r"^\(?-?[\d,]+(\.\d+)?\)?$|^[—–-]$")


def row(p, label, anchor=None, after=None, n=None):
    """The first row of a converted HTML filing whose label matches `label` (a regex on the first cell), at or after the first line
    matching `anchor` (and then `after`), whose other cells are numbers; returns (numbers, the row's text). The row goes to the
    checklist."""
    lines = text(p)[2]
    i = 0
    for a in [x for x in (anchor, after) if x]:
        i = next(k for k in range(i, len(lines)) if re.search(a, lines[k]))
    for k in range(i, len(lines)):
        cells = [c.strip() for c in lines[k].split("|")]
        if re.fullmatch(label, cells[0]) and len(cells) > 1 and all(NUMCELL.match(c) for c in cells[1:] if c):
            vals = [num(c) for c in cells[1:] if c]
            if n is None or len(vals) == n:
                CHECK.setdefault(p, []).append(lines[k])
                return vals, lines[k]
    raise AssertionError((os.path.basename(p), label, anchor, after))


def pub(acc):
    """The date a filing counts from (the acceptance-time rule): EDGAR's UTC time in ET; at or after 16:00, the next trading day;
    a time of exactly 00:00 ET (EDGAR gives the date only) counts as before the open."""
    r = ROWS[acc]
    t = dt.datetime.fromisoformat(r[1].replace("Z", "+00:00")).astimezone(ET)
    day = t.date().isoformat()
    if (t.hour, t.minute) >= (16, 0):
        day = min(d for d in TDAYS if d > day)
    if (t.hour, t.minute) == (0, 0):
        when = f"filed {r[0]} (EDGAR gives the date only; counted as before the open)"
    elif (t.hour, t.minute) < (9, 30):
        when = f"accepted {t:%Y-%m-%d %H:%M} ET, before the open"
    elif (t.hour, t.minute) < (16, 0):
        when = f"accepted {t:%Y-%m-%d %H:%M} ET, during the session"
    else:
        when = f"accepted {t:%Y-%m-%d %H:%M} ET, after the close: counts from {day}"
    assert day <= CUT
    return day, when


SOURCES = {}


def src(sid, acc, title, supports, date_only=False):
    day, when = pub(acc)
    if date_only:                      # before 2002 EDGAR records the filing date only
        day, when = ROWS[acc][0], f"filed {ROWS[acc][0]} (EDGAR gives the filing date only)"
    SOURCES[sid] = {"published": day, "filed": when, "title": title,
                    "url": f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc.replace('-', '')}/{acc}.txt", "supports": supports}
    return sid


pct = lambda a, b: round((b / a - 1) * 100 + 0.0, 2)
pct1 = lambda a, b: round((b / a - 1) * 100 + 0.0, 1)
g1 = lambda a, b: round((b / a - 1) * 100 + 0.0, 1) if a > 0 else round((b - a) / abs(a) * 100 + 0.0, 1)   # over a loss's |value| (CAT)
g2 = lambda a, b: round((b / a - 1) * 100 + 0.0, 2) if a > 0 else round((b - a) / abs(a) * 100 + 0.0, 2)

# ── sources: the decade's 10-Ks (rule T), the history vintages, the releases, the guidance and dividend 8-Ks ─────────────────────
F1998 = src("OK1", "0000950134-98-007714", "ONEOK FY1998 10-K405 (fiscal year ended August 31, 1998)",
            "rule T: fiscal 1997 against fiscal 1996 (revenues, net margin, operating income and pre-tax income from the statement of "
            "income)", True)
F1999 = src("OK2", "0000950134-99-010556", "ONEOK FY1999 10-K405 (fiscal year ended August 31, 1999)",
            "rule T: fiscal 1998 against fiscal 1997 (statement of income; the Distribution segment's operating income)", True)
F2000 = src("OK3", "0000930661-01-000672", "ONEOK FY2000 10-K (year ended December 31, 2000; the transition period of September-"
            "December 1999)", "rule T: fiscal 1999 against fiscal 1998 (statement of income; the Distribution segment)", True)
F2001 = src("OK4", "0000930661-02-000717", "ONEOK FY2001 10-K405", "rule T: calendar 2000 against fiscal 1999 (statement of income; "
            "the Distribution segment); 2001's listed items (the OCC ruling and the Enron bankruptcy)", True)
F2002 = src("OK5", "0000930661-03-000949", "ONEOK FY2002 10-K", "rule T: 2001 against 2000 (statement of income; the Distribution "
            "segment)")
F2003 = src("OK6", "0001193125-04-033606", "ONEOK FY2003 10-K", "rule T: 2002 against 2001 (statement of income; the Distribution "
            "segment)")
F2004 = src("OK7", "0001193125-05-044590", "ONEOK FY2004 10-K", "rule T: 2003 against 2002 (statement of income; the Distribution "
            "segment); FY2002 diluted shares")
F2005 = src("OK8", "0001193125-06-051266", "ONEOK FY2005 10-K", "rule T: 2004 against 2003 (statement of income; the Distribution "
            "segment); FY2001 EPS from continuing operations (excluded) and FY2003 diluted shares")
F2006 = src("OK9", "0001193125-07-042960", "ONEOK FY2006 10-K", "history vintage FY2006; rule T: 2005 and 2006 against the year "
            "before; the company's EPS excluding the 2005 and 2006 gains on sale; the 'why'")
F2007 = src("OK10", "0001193125-08-040037", "ONEOK FY2007 10-K", "history vintage FY2007; the 'why'")
F2008 = src("OK11", "0001039684-09-000010", "ONEOK FY2008 10-K", "history vintage FY2008; the 'why'")
D = {k: path(a, p) for k, a, p in [
    ("F1998", "0000950134-98-007714", "10-K405__1"), ("F1999", "0000950134-99-010556", "10-K405__1"),
    ("F2000", "0000930661-01-000672", "10-K__0001.txt"), ("F2001", "0000930661-02-000717", "10-K405__d10k405.txt"),
    ("F2002", "0000930661-03-000949", "10-K__d10k.rows.txt"), ("F2003", "0001193125-04-033606", "10-K__d10k.rows.txt"),
    ("F2004", "0001193125-05-044590", "10-K__d10k.rows.txt"), ("F2005", "0001193125-06-051266", "10-K__d10k.rows.txt"),
    ("F2006", "0001193125-07-042960", "10-K__d10k.rows.txt"), ("F2007", "0001193125-08-040037", "10-K__d10k.rows.txt"),
    ("F2008", "0001039684-09-000010", "10-K__form_10-k.rows.txt")]}
SID = {"F1998": F1998, "F1999": F1999, "F2000": F2000, "F2001": F2001, "F2002": F2002, "F2003": F2003, "F2004": F2004,
       "F2005": F2005, "F2006": F2006, "F2007": F2007, "F2008": F2008}
# the FY2006 10-K/A of 2007-05-25 only corrects an exhibit's signature date (adds nothing)
quote(path("0001193125-07-123574", "10-K_A__d10ka.rows.txt"), "The purpose of this Amendment No. 1 to our Annual Report on Form 10-K "
      "for the year ended December 31, 2006, is to amend Exhibit 32.2 to correct the signature date from February 28, 2006 to February "
      "28, 2007.")

# ── rule T over 1997-2006 (the decade of the vintage public on 2008-01-04): each change from the latest filing published by then
# whose statement of income (or Distribution segment table) tabulates both years, as tabulated (seams in, as published). Fiscal
# 1996-1999 ended August 31; the four-month transition period to December 31, 1999 is not a fiscal year, so calendar 2000 is set
# against fiscal 1999 as the FY2001 10-K places them side by side (the BKR transition rule) ──
RT = {"nm": {"unit": 1, "lower_is_better": False, "values": {}, "raw": {}},
      "dist": {"unit": 1, "lower_is_better": False, "values": {}, "raw": {}},
      "revenue": {"unit": 1, "lower_is_better": False, "values": {}, "raw": {}},
      "op_margin": {"unit": 10, "lower_is_better": False, "values": {}, "raw": {}},
      "pretax_margin": {"unit": 10, "lower_is_better": False, "values": {}, "raw": {}}}


def rt_year(y, f, rev, nm, oi, pti, how, rows):
    """One year's rule-T values from (prior, current) pairs in thousands of dollars."""
    RT["revenue"]["raw"][str(y)] = {"source": SID[f], "revenue_k": rev, "rows": rows}
    RT["revenue"]["values"][str(y)] = pct(*rev)
    RT["nm"]["raw"][str(y)] = {"source": SID[f], "net_margin_k": nm, "rows": rows}
    RT["nm"]["values"][str(y)] = pct(*nm)
    RT["op_margin"]["raw"][str(y)] = {"source": SID[f], "oi_k": oi, "revenue_k": rev, "rows": rows}
    RT["op_margin"]["values"][str(y)] = round((oi[1] / rev[1] - oi[0] / rev[0]) * 10000 + 0.0, 1)
    RT["pretax_margin"]["raw"][str(y)] = {"source": SID[f], "pti_k": pti, "revenue_k": rev, "how": how, "rows": rows}
    RT["pretax_margin"]["values"][str(y)] = round((pti[1] / rev[1] - pti[0] / rev[0]) * 10000 + 0.0, 1)


def rt_dist(y, f, pair, rows):
    RT["dist"]["raw"][str(y)] = {"source": SID[f], "dist_oi_k": pair, "rows": rows}
    RT["dist"]["values"][str(y)] = g2(*pair)


# fiscal 1997 (FY1998 10-K405): the utility-format statement prints no operating income or pre-tax line; operating income is revenues
# less cost of gas, operations and maintenance, depreciation and general taxes (income taxes sit among its operating expenses), pre-tax
# income is net income plus income taxes, net margin is revenues less cost of gas. No Distribution segment before the FY1999 10-K
# (the FY1998 10-K reports a "Regulated" segment), so the Distribution signal's rule T starts with fiscal 1998
_r = S(D["F1998"], "Total Operating Revenues 1,835,402 1,161,927 1,224,345", "1,835,402", "1,161,927", "1,224,345")
_c = S(D["F1998"], "Cost of gas 1,220,009 725,960 807,694", "1,220,009", "725,960", "807,694")
_o = S(D["F1998"], "Operations and maintenance 277,068 210,852 201,644", "277,068", "210,852", "201,644")
_d = S(D["F1998"], "Depreciation, depletion, and amortization 101,653 74,509 72,868 General taxes", "101,653", "74,509", "72,868")
_g = S(D["F1998"], "General taxes 33,217 22,491 21,489", "33,217", "22,491", "21,489")
_t = S(D["F1998"], "Income taxes 66,585 34,839 33,037", "66,585", "34,839", "33,037")
_n = S(D["F1998"], "Net Income 101,795 59,268 52,836", "101,795", "59,268", "52,836")
oi97 = [_r[i] - _c[i] - _o[i] - _d[i] - _g[i] for i in (2, 1)]
rt_year(1997, "F1998", [_r[2], _r[1]], [_r[2] - _c[2], _r[1] - _c[1]], oi97, [_n[2] + _t[2], _n[1] + _t[1]],
        "net income plus income taxes (the statement prints no pre-tax line); operating income and net margin computed from its lines",
        ["Total Operating Revenues 1,835,402 1,161,927 1,224,345", "Cost of gas 1,220,009 725,960 807,694",
         "Operations and maintenance 277,068 210,852 201,644", "Depreciation, depletion, and amortization 101,653 74,509 72,868",
         "General taxes 33,217 22,491 21,489", "Income taxes 66,585 34,839 33,037", "Net Income 101,795 59,268 52,836"])
assert oi97[1] == 128115, "fiscal 1997 operating income as the FY1999 10-K prints it"
# fiscal 1998 (FY1999 10-K405)
_r = S(D["F1999"], "Operating Revenues $ 1,842,810 $ 1,820,758 $ 1,161,927", "1,842,810", "1,820,758", "1,161,927")
_m = S(D["F1999"], "Net Revenues 686,786 600,749 435,967", "686,786", "600,749", "435,967")
_oi = S(D["F1999"], "Operating Income 219,583 188,811 128,115", "219,583", "188,811", "128,115")
_t = S(D["F1999"], "Income Taxes 67,056 66,585 34,839", "67,056", "66,585", "34,839")
_n = S(D["F1999"], "Net Income 106,357 101,795 59,268", "106,357", "101,795", "59,268")
rt_year(1998, "F1999", [_r[2], _r[1]], [_m[2], _m[1]], [_oi[2], _oi[1]], [_n[2] + _t[2], _n[1] + _t[1]],
        "net income plus income taxes (the statement prints no pre-tax line)",
        ["Operating Revenues $ 1,842,810 $ 1,820,758 $ 1,161,927", "Net Revenues 686,786 600,749 435,967",
         "Operating Income 219,583 188,811 128,115", "Income Taxes 67,056 66,585 34,839", "Net Income 106,357 101,795 59,268"])
_ds = S(D["F1999"], "Net revenues 404,384 378,376 225,252 Operating costs 230,868 208,513 116,325 Depreciation, depletion, and "
        "amortization 75,443 66,214 42,980 Operating Income $ 98,073 $ 103,649 $ 65,947", "98,073", "103,649", "65,947")
rt_dist(1998, "F1999", [_ds[2], _ds[1]], ["Distribution: Operating Income $ 98,073 $ 103,649 $ 65,947"])
# fiscal 1999 (FY2000 10-K: columns 2000, the four months to December 1999, fiscal 1999, fiscal 1998)
_r = S(D["F2000"], "OPERATING REVENUES (NOTE A) $6,642,858 $ 806,478 $1,838,949 $1,820,758", "1,838,949", "1,820,758")
_m = S(D["F2000"], "Net Revenues 797,132 218,797 625,471 545,639", "625,471", "545,639")
_oi = S(D["F2000"], "Operating Income 333,933 83,568 215,722 188,811", "215,722", "188,811")
_t = S(D["F2000"], "Income taxes 90,286 22,737 67,056 66,585", "67,056", "66,585")
_n = S(D["F2000"], "Income before cumulative effect of a change in 143,492 35,344 106,357 101,795", "106,357", "101,795")
rt_year(1999, "F2000", [_r[1], _r[0]], [_m[1], _m[0]], [_oi[1], _oi[0]], [_n[1] + _t[1], _n[0] + _t[0]],
        "income before the cumulative effect plus income taxes (the statement prints no pre-tax line)",
        ["OPERATING REVENUES (NOTE A) $6,642,858 $ 806,478 $1,838,949 $1,820,758", "Net Revenues 797,132 218,797 625,471 545,639",
         "Operating Income 333,933 83,568 215,722 188,811", "Income taxes 90,286 22,737 67,056 66,585",
         "Income before cumulative effect of a change in 143,492 35,344 106,357 101,795"])
_ds = S(D["F2000"], "Operating income $ 97,931 $ 98,073 $ 103,649 OPERATING RESULTS - Gross margin on gas sales decreased in 2000",
        "97,931", "98,073", "103,649")
rt_dist(1999, "F2000", [_ds[2], _ds[1]], ["Distribution: Operating income $ 97,931 $ 98,073 $ 103,649"])
# calendar 2000 against fiscal 1999 (FY2001 10-K405: columns 2001, 2000, the four months to December 1999, fiscal 1999)
_r = S(D["F2001"], "Operating Revenues (Note A) $ 6,803,146 $ 6,642,858 $ 806,478 $ 1,838,949", "6,803,146", "6,642,858", "806,478",
       "1,838,949")
_m = S(D["F2001"], "Net Revenues 908,785 797,132 218,797 625,471", "908,785", "797,132", "218,797", "625,471")
_oi = S(D["F2001"], "Operating Income 295,232 333,933 83,568 215,722", "295,232", "333,933", "83,568", "215,722")
_t = S(D["F2001"], "Income taxes 52,234 90,286 22,737 67,056", "52,234", "90,286", "22,737", "67,056")
_n = S(D["F2001"], "accounting principle 103,716 143,492 35,344 106,357", "103,716", "143,492", "35,344", "106,357")
rt_year(2000, "F2001", [_r[3], _r[1]], [_m[3], _m[1]], [_oi[3], _oi[1]], [_n[3] + _t[3], _n[1] + _t[1]],
        "income before the cumulative effect plus income taxes (the statement prints no pre-tax line); calendar 2000 against fiscal "
        "1999, the transition period between them left out",
        ["Operating Revenues (Note A) $ 6,803,146 $ 6,642,858 $ 806,478 $ 1,838,949", "Net Revenues 908,785 797,132 218,797 625,471",
         "Operating Income 295,232 333,933 83,568 215,722", "Income taxes 52,234 90,286 22,737 67,056",
         "Income before cumulative effect of a change in accounting principle 103,716 143,492 35,344 106,357"])
_ds = S(D["F2001"], "Operating income $ 54,097 $ 97,931 $ 98,073", "54,097", "97,931", "98,073")
quote(D["F2001"], "The Distribution segment provides natural gas\ndistribution services in Oklahoma and Kansas.")
rt_dist(2000, "F2001", [_ds[2], _ds[1]], ["Distribution: Operating income $ 54,097 $ 97,931 $ 98,073"])


def rt_html(y, f, anchor, rev_labels, nm_label, pti_label, cols, how, tax_label=None, inc_label=None, dist_anchor=None):
    """Year y against y-1 from an HTML 10-K's statement of income (cols: the (prior, current) column indexes)."""
    p = D[f]
    rows, rv = [], None
    for lab in rev_labels:                         # revenues: the total row, or the sum of the revenue lines the statement prints
        v, t = row(p, lab, anchor)
        rows.append(t)
        rv = v if rv is None else [a + b for a, b in zip(rv, v)]
    nm, t = row(p, nm_label, anchor)
    rows.append(t)
    oi, t = row(p, r"Operating Income", anchor)
    rows.append(t)
    if pti_label:
        pti, t = row(p, pti_label, anchor)
        rows.append(t)
    else:                                          # no pre-tax line: income from continuing operations plus income taxes
        inc, t1 = row(p, inc_label, anchor)
        tax, t2 = row(p, tax_label, anchor)
        rows += [t1, t2]
        pti = [a + b for a, b in zip(inc, tax)]
    a, b = cols
    rt_year(y, f, [rv[a], rv[b]], [nm[a], nm[b]], [oi[a], oi[b]], [pti[a], pti[b]], how, rows)


ST = r"^CONSOLIDATED STATEMENTS OF INCOME$"
rt_html(2001, "F2002", ST, [r"Operating revenues, excluding energy trading revenues", r"Energy trading revenues, net"],
        r"Net Revenues", None, (2, 1), "income from continuing operations plus income taxes (the statement prints no pre-tax line); "
        "revenues the two revenue lines summed", tax_label=r"Income taxes", inc_label=r"Income from continuing operations")
rt_html(2002, "F2003", ST, [r"Operating revenues, excluding energy trading revenues", r"Energy trading revenues, net"],
        r"Net Revenues", r"Income before Income Taxes", (2, 1), "income before income taxes; revenues the two revenue lines summed")
rt_html(2003, "F2004", ST, [r"Total Revenues"], r"Net Margin", r"Income before Income Taxes", (2, 1), "income before income taxes")
rt_html(2004, "F2005", ST, [r"Total Revenues"], r"Net Margin", r"Income before Income Taxes", (2, 1), "income before income taxes")
for y, cols in ((2005, (2, 1)), (2006, (1, 0))):
    rt_html(y, "F2006", ST, [r"Total Revenues"], r"Net Margin", r"Income before Minority Interests and Income Taxes", cols,
            "income before minority interests and income taxes")
# the Distribution segment's operating income, from each 10-K's Distribution table (2001-2006)
DA = r"selected financial and operating information for (our|the) Distribution segment"
for y, f, anchor, n_cols, cols in ((2001, "F2002", DA, 3, (2, 1)),
                                   (2002, "F2003", DA, 3, (2, 1)),
                                   (2003, "F2004", DA, 3, (2, 1)),
                                   (2004, "F2005", DA, 3, (2, 1)),
                                   (2005, "F2006", DA, 3, (2, 1)),
                                   (2006, "F2006", DA, 3, (1, 0))):
    v, t = row(D[f], r"Operating income", anchor, n=n_cols)
    rt_dist(y, f, [v[cols[0]], v[cols[1]]], [t])

# ── history vintages: each year from the latest filing that reports it ───────────────────────────────────────────────────────
I6 = r"^ITEM 6\.( \|)? SELECTED FINANCIAL DATA$"


def item6_eps(f):
    v, t = row(D[f], r"Diluted earnings per share - continuing operations", I6)
    return v, t


def why(f, lead, extra=()):
    lo = text(D[f])[0].lower()
    # DURABLE needs the company not to call its own business cyclical (the MU rule): the only use of the word is the billing cycle
    assert lo.count("cyclical") == lo.count("invoiced on a cyclical basis"), (f, "a 10-K that calls the business cyclical")
    q = [quote(D[f], lead), quote(D[f], "Our cash flow depends heavily on the earnings and distributions of ONEOK Partners.")] + [
        quote(D[f], s) for s in extra]
    label = {"F2006": "FY2006", "F2007": "FY2007", "F2008": "FY2008"}[f]
    return " ".join(f"'{x}'" for x in q) + (f" (the {label} 10-K's own words; it calls no business of the company cyclical, the word "
                                            "appearing only in its billing cycle, so DURABLE, the MU rule)")


# EPS 2002-2006 (FY2006 10-K, Item 6: diluted EPS from continuing operations) and the company's figures without the gains on sale
e06, e06t = item6_eps("F2006")
assert e06 == [2.68, 3.73, 2.13, 2.05, 1.26], e06
X0605 = quote(D["F2006"], "Excluding the gain on sale of a 20 percent partnership interest in Northern Border Pipeline in 2006 and excluding "
              "the 2005 gain on sale of our Texas gathering and processing assets, EPS from continuing operations decreased to $2.40 in "
              "2006, compared with $2.53 in 2005.")
ADJ = {"2005": 2.53, "2006": 2.40}
ADJ_NOTE = ("2005 and 2006 at the company's EPS from continuing operations excluding only the gains on sale ($2.53 without the $264.2M "
            "pre-tax gain on the Texas gathering and processing assets, GAAP $3.73; $2.40 without ONEOK's share of the gain on the 20 "
            "percent interest in Northern Border Pipeline, GAAP $2.68), from the FY2006 10-K in every vintage that holds them (the ACN rule: "
            "'" + X0605 + "')")
# FY2001: the AAPL FY2002 test on the latest filing that reports the year (the FY2005 10-K: $0.36 from continuing operations, income
# from continuing operations $43.5M) against the FY2001 10-K's two listed items, $34.6M and $37.4M of operating income
e05, e05t = item6_eps("F2005")
assert e05[-1] == 0.36, e05
inc05, inc05t = row(D["F2005"], r"Income from continuing operations", I6)
assert inc05[-1] == 43.5, inc05
I01 = quote(D["F2001"], "The impact of the OCC ruling related to the\nrecovery of gas costs from the 2000/2001 winter reduced operating income by\n"
            "$34.6 million and the impact of the Enron bankruptcy reduced operating income\nby $37.4 million in 2001.")
assert 34.6 + 37.4 > inc05[-1], "the listed items exceed the year's income from continuing operations"
FIRST_EXCL = {"2001": (f"the AAPL FY2002 test: $0.36 a diluted share from continuing operations and income from continuing operations of "
                       f"${inc05[-1]:.1f}M (FY2005 10-K, the latest filing that reports the year, the production segment discontinued), "
                       "against the FY2001 10-K's two listed items, $72.0M together ('" + I01.replace("\n", " ") + "'), so reported EPS "
                       "is under half the year's EPS without them ($0.36 against $0.36 + $72.0M / 99.7M diluted shares = $1.08), and no "
                       "filing publishes a figure excluding only them; a distorted year that is not the latest takes the years before it "
                       "(the ACN FY02 and AAPL FY2002 rule), so the history starts with FY2002 and the P/E window on 2002-01-01, which also "
                       "leaves out fiscal 1997-1999 (years to August 31) and the four-month transition period to December 31, 1999")}
NORM = ("diluted EPS from continuing operations (before the 2003 cumulative effect of accounting changes), each year from the latest filing "
        "that reports it; " + ADJ_NOTE + "; no other year has listed items near its income (2002: gains of $7.6M, $1.5M and $1.9M and a "
                                         "$5.0M settlement accrual against $151.0M, the FY2002 10-K); GAAP otherwise")


def stmt(f, label, n=3):
    return row(D[f], label, ST, n=n)


r06, _ = stmt("F2006", r"Total Revenues")
r05, _ = stmt("F2005", r"Total Revenues")
r04, _ = stmt("F2004", r"Total Revenues")
sh06, _ = stmt("F2006", r"Diluted", 3)
sh05, _ = row(D["F2005"], r"Diluted", ST, after=r"^Average Shares of Common Stock", n=3)
sh04, _ = row(D["F2004"], r"Diluted", ST, after=r"^Average Shares of Common Stock", n=3)
sh06, _ = row(D["F2006"], r"Diluted", ST, after=r"^Average Shares of Common Stock", n=3)


def vintage_stats(f, fy):
    """The last year's statement figures for a vintage (thousands of dollars)."""
    rv, _ = stmt(f, r"Total Revenues|Revenues")
    oi, _ = stmt(f, r"Operating Income")
    pti, _ = stmt(f, r"Income before Minority Interests and Income Taxes")
    tax, _ = stmt(f, r"Income taxes( \(Note L\))?")
    cfo, _ = row(D[f], r"Cash Provided by (\(Used in\) )?Operating Activities", r"^CONSOLIDATED STATEMENTS OF CASH FLOWS$", n=3)
    cx, _ = row(D[f], r"Capital expenditures( \(less allowance for equity funds used during construction\))?",
                r"^CONSOLIDATED STATEMENTS OF CASH FLOWS$", n=3)
    rp, _ = row(D[f], r"Repurchase of common stock", r"^CONSOLIDATED STATEMENTS OF CASH FLOWS$", n=3)
    seg_a = r"^Sales to unaffiliated customers"
    return {"rev": rv, "oi": oi, "pti": pti, "tax": [abs(x) for x in tax], "cfo": cfo, "capex": [abs(x) for x in cx],
            "repurchase": [abs(x) for x in rp]}


def groups(f, nlab):
    """Segment sales to unaffiliated customers (ONEOK Partners, Distribution, Energy Services), the last year and the one before, from
    the segment note (the first two 'Sales to unaffiliated customers' rows after the note's heading)."""
    lines = text(D[f])[2]
    k0 = max(i for i, l in enumerate(lines) if re.match(r"^(M\.|Note M|NOTE M)?.*SEGMENTS", l) and "Note M" not in l) if False else None
    out = []
    for k, l in enumerate(lines):
        if l.startswith("Sales to unaffiliated customers |"):
            cells = [num(c) for c in l.split("|")[1:] if c.strip()]
            if len(cells) == nlab:
                out.append((cells, l))
                CHECK.setdefault(D[f], []).append(l)
        if len(out) == 2:
            break
    (cur, t1), (pri, t2) = out
    names = ["ONEOK Partners", "Distribution", "Energy Services"]
    return [[n, round(cur[i] / 1e6, 3), pct1(pri[i], cur[i])] for i, n in enumerate(names)]


def vintage(f, fy, eps, eps_src, rev, rev_src, sh, sh_src, extra_why, lead, div_q, div_note, groups_basis):
    st = vintage_stats(f, fy)
    m = lambda a, b: round(a / b * 100 + 0.0, 2)
    return {
        "published": SOURCES[SID[f]]["published"], "sources": sorted({SID[f]} | set(eps_src.values()) | set(rev_src.values())
                                                                  | set(sh_src.values()), key=lambda s: -int(s[2:])),
        "company": "ONEOK, Inc.", "exchange": "NYSE", "symbol": "OKE",
        "business_line": ("natural gas distribution (Oklahoma, Kansas, Texas) and energy services; the general partner of ONEOK Partners, "
                          "L.P. (NYSE: OKS), consolidated"),
        "fy_label": f"FY{fy % 100:02d}", "fiscal_year_ends": {str(y): f"{y}-12-31" for y in eps},
        "eps_normalized": {str(y): v for y, v in sorted(eps.items())}, "eps_sources": {str(y): s for y, s in sorted(eps_src.items())},
        "eps_excluded": {}, "eps_first_excluded": FIRST_EXCL,
        "revenue_usd_b": {str(y): round(v / 1e6, 6) for y, v in sorted(rev.items())},
        "revenue_sources": {str(y): s for y, s in sorted(rev_src.items())},
        "diluted_shares_m": {str(y): round(v / 1000, 3) for y, v in sorted(sh.items())},
        "shares_sources": {str(y): s for y, s in sorted(sh_src.items())},
        "shares_note": "diluted average shares of common stock, millions (each statement of income)",
        "normalization": NORM, "pe_window_start": "2002-01-01",
        "prev_fy_op_margin": m(st["oi"][0], st["rev"][0]),
        "prev_fy_op_margin_note": (f"FY{fy % 100:02d} operating income ${st['oi'][0] / 1000:,.1f}M / revenues ${st['rev'][0] / 1000:,.1f}M "
                                   f"(FY{fy} 10-K), the operating margin"),
        "check_pretax_margin": m(st["pti"][0], st["rev"][0]),
        "check_pretax_note": (f"FY{fy % 100:02d} income before minority interests and income taxes ${st['pti'][0] / 1000:,.1f}M / revenues "
                              f"${st['rev'][0] / 1000:,.1f}M (FY{fy} 10-K); before the minority interests (ONEOK Partners' other "
                              "unitholders), so the check overstates ONEOK's own EPS"),
        "tax_rate": round(st["tax"][0] / st["pti"][0], 4),
        "tax_note": (f"FY{fy % 100:02d} income taxes ${st['tax'][0] / 1000:,.1f}M / income before minority interests and income taxes "
                     f"${st['pti'][0] / 1000:,.1f}M (FY{fy} 10-K)"),
        "prev_fy_sales_growth": pct1(st["rev"][1], st["rev"][0]),
        "dividend_annual": round(div_q * 4, 2), "dividend_note": div_note,
        "fcf_label": f"FY{fy % 100:02d}", "fcf_b": round((st["cfo"][0] - st["capex"][0]) / 1e6, 3),
        "fcf_note": (f"cash provided by operating activities ${st['cfo'][0] / 1000:,.1f}M less capital expenditures "
                     f"${st['capex'][0] / 1000:,.1f}M (FY{fy} 10-K, consolidated, ONEOK Partners' included)"),
        "cash_return_text": (f"repurchases of common stock ${st['repurchase'][0] / 1000:,.1f}M in {fy} (FY{fy} 10-K's statement of cash "
                             "flows)"),
        "groups": groups(f, 5), "groups_basis": groups_basis,
        "margin_signal_name": "Pre-tax margin change",
        "kind": "DURABLE", "kind_text": "A gas distributor and the general partner of a midstream partnership",
        "why": why(f, lead, extra_why),
    }


V = []
V.append(vintage("F2006", 2006,
                 {2002: e06[4], 2003: e06[3], 2004: e06[2], 2005: ADJ["2005"], 2006: ADJ["2006"]},
                 {y: F2006 for y in range(2002, 2007)},
                 {2002: r04[2], 2003: r05[2], 2004: r06[2], 2005: r06[1], 2006: r06[0]},
                 {2002: F2004, 2003: F2005, 2004: F2006, 2005: F2006, 2006: F2006},
                 {2002: sh04[2], 2003: sh05[2], 2004: sh06[2], 2005: sh06[1], 2006: sh06[0]},
                 {2002: F2004, 2003: F2005, 2004: F2006, 2005: F2006, 2006: F2006},
                 ["Our nonregulated businesses have a higher level of risk than our regulated businesses."],
                 "We purchase, transport, store and distribute natural gas.",
                 0.34, "$0.34 a quarter, $1.36 a year: '" + quote(D["F2006"], "A quarterly dividend of $0.34 per share was declared in "
                                                                     "January 2007, payable in the first quarter of 2007.") + "' (FY2006 10-K)",
                 "FY06 segment sales to unaffiliated customers (FY2006 10-K segment note; eliminations and Other left out)"))
# FY2007 10-K: 2005-2007 from its statements; 2003-2007 EPS from its Item 6 (2005 and 2006 at the company's figures)
e07, _ = item6_eps("F2007")
assert e07 == [2.79, 2.68, 3.73, 2.13, 2.05], e07
r07, _ = stmt("F2007", r"Total Revenues")
sh07, _ = row(D["F2007"], r"Diluted", ST, after=r"^Average Shares of Common Stock", n=3)
V.append(vintage("F2007", 2007,
                 {2002: e06[4], 2003: e07[4], 2004: e07[3], 2005: ADJ["2005"], 2006: ADJ["2006"], 2007: e07[0]},
                 {2002: F2006, 2003: F2007, 2004: F2007, 2005: F2006, 2006: F2006, 2007: F2007},
                 {2002: r04[2], 2003: r05[2], 2004: r06[2], 2005: r07[2], 2006: r07[1], 2007: r07[0]},
                 {2002: F2004, 2003: F2005, 2004: F2006, 2005: F2007, 2006: F2007, 2007: F2007},
                 {2002: sh04[2], 2003: sh05[2], 2004: sh06[2], 2005: sh07[2], 2006: sh07[1], 2007: sh07[0]},
                 {2002: F2004, 2003: F2005, 2004: F2006, 2005: F2007, 2006: F2007, 2007: F2007},
                 ["The volatility of natural gas, crude oil and NGL prices could adversely affect ONEOK Partners’ cash flow."],
                 "We purchase, transport, store and distribute natural gas.",
                 0.38, "$0.38 a quarter, $1.52 a year: '" + quote(D["F2007"], "We declared a quarterly dividend of $0.38 per share ($1.52 "
                                                                     "per share on an annualized basis) in January 2008") + "' (FY2007 10-K)",
                 "FY07 segment sales to unaffiliated customers (FY2007 10-K segment note; eliminations and Other left out)"))
# FY2008 10-K: 2006-2008 from its statements; 2004-2008 EPS from its Item 6
e08, _ = item6_eps("F2008")
assert e08 == [2.95, 2.79, 2.68, 3.73, 2.13], e08
r08, _ = stmt("F2008", r"Revenues")
sh08, _ = row(D["F2008"], r"Diluted", ST, after=r"^Average Shares of Common Stock", n=3)
V.append(vintage("F2008", 2008,
                 {2002: e06[4], 2003: e07[4], 2004: e08[4], 2005: ADJ["2005"], 2006: ADJ["2006"], 2007: e08[1], 2008: e08[0]},
                 {2002: F2006, 2003: F2007, 2004: F2008, 2005: F2006, 2006: F2006, 2007: F2008, 2008: F2008},
                 {2002: r04[2], 2003: r05[2], 2004: r06[2], 2005: r07[2], 2006: r08[2], 2007: r08[1], 2008: r08[0]},
                 {2002: F2004, 2003: F2005, 2004: F2006, 2005: F2007, 2006: F2008, 2007: F2008, 2008: F2008},
                 {2002: sh04[2], 2003: sh05[2], 2004: sh06[2], 2005: sh07[2], 2006: sh08[2], 2007: sh08[1], 2008: sh08[0]},
                 {2002: F2004, 2003: F2005, 2004: F2006, 2005: F2007, 2006: F2008, 2007: F2008, 2008: F2008},
                 ["The volatility of natural gas, crude oil and NGL prices could adversely affect ONEOK Partners’ cash flow."],
                 "We are a diversified energy company and successor to the company founded in 1906 known as Oklahoma Natural Gas Company.",
                 0.40, "$0.40 a quarter, $1.60 a year: '" + quote(D["F2008"], "In January 2009, we declared a dividend of $0.40 per share "
                                                                     "($1.60 per share on an annualized basis) for the fourth quarter of "
                                                                     "2008") + "' (FY2008 10-K)",
                 "FY08 segment sales to unaffiliated customers (FY2008 10-K segment note; eliminations and Other left out)"))
for v in V:
    assert len(v["eps_normalized"]) <= 10 and min(v["eps_normalized"]) == "2002"

# EPS rule T is not a signal of this engine (the signals are net margin, Distribution operating income, revenue and two margins)

# ── the quarterly prints: the earnings releases (8-K exhibit 99.1), each figure against the year-ago quarter as the release shows it ──
PR = []
NEXT = {1: "Q2 print (early August)", 2: "Q3 print (early November)", 3: "Q4 and full-year print, with the 10-K (late February)",
        4: "Q1 print (late April or early May)"}
REL_ST = r"^CONSOLIDATED STATEMENTS OF INCOME$"


def prt(sid, acc, quarter, fy, q, release):
    p = path(acc, "EX-99.1__*.rows.txt")
    day, when = pub(acc)
    SOURCES[sid] = {"published": day, "filed": when, "title": f"ONEOK {quarter} results (8-K exhibit 99.1)",
                    "url": f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc.replace('-', '')}/{acc}.txt",
                    "supports": f"{quarter}: revenues, net margin, operating income, income before income taxes, diluted EPS, diluted "
                                "shares and the Distribution segment's operating income"}
    rv, t_rv = row(p, r"Total Revenues|Revenues", REL_ST)
    nm, t_nm = row(p, r"Net [Mm]argin", REL_ST)
    oi, t_oi = row(p, r"Operating [Ii]ncome", REL_ST)
    pti, t_pt = row(p, r"Income before (Minority Interests and )?[Ii]ncome [Tt]axes", REL_ST)
    eps, t_e = row(p, r"Net [Ee]arnings [Pp]er [Ss]hare, [Dd]iluted", REL_ST)
    sh, t_s = row(p, r"Diluted", REL_ST, after=r"(?i)^Average Shares of Common Stock")
    ds, t_d = row(p, r"Operating income( \(loss\))?", r"(?i)^(ONEOK, Inc\. and Subsidiaries )?INFORMATION AT A GLANCE$|^INFORMATION AT A GLANCE",
                  r"^Distribution$")
    cash, t_c = row(p, r"Cash and cash equivalents", r"^CONSOLIDATED BALANCE SHEETS$")
    mg = lambda x, r: round(x / r * 100 + 0.0, 2)
    fmt = lambda x: f"${x:.2f}" if x >= 0 else f"$({-x:.2f})"
    fm = lambda x: f"${x:,.1f}M" if x >= 0 else f"$({-x:,.1f})M"
    d = {"quarter": quarter, "fy": fy, "q": q, "published": day, "source": sid, "release": release, "release_time": when,
         "raw": {"rev_m": rv[0] / 1000, "rev_prior_m": rv[1] / 1000, "nm_m": nm[0] / 1000, "nm_prior_m": nm[1] / 1000,
                 "oi_m": oi[0] / 1000, "oi_prior_m": oi[1] / 1000, "pti_m": pti[0] / 1000, "pti_prior_m": pti[1] / 1000,
                 "dist_m": ds[0], "dist_prior_m": ds[1], "eps_q": eps[0], "eps_q_prior": eps[1], "dil_sh_m": round(sh[0] / 1000, 3)},
         "rows": {"revenues": t_rv, "net_margin": t_nm, "operating_income": t_oi, "pretax": t_pt, "eps": t_e, "shares": t_s,
                  "distribution": t_d, "cash": t_c}}
    r = d["raw"]
    d.update({"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": g1(r["rev_prior_m"], r["rev_m"]),
              "nm_pct": g1(r["nm_prior_m"], r["nm_m"]), "dist_pct": g1(r["dist_prior_m"], r["dist_m"]),
              "opm": mg(r["oi_m"], r["rev_m"]), "opm_bp": round((mg(r["oi_m"], r["rev_m"]) - mg(r["oi_prior_m"], r["rev_prior_m"])) * 100, 1),
              "ptm": mg(r["pti_m"], r["rev_m"]),
              "ptm_bp": round((mg(r["pti_m"], r["rev_m"]) - mg(r["pti_prior_m"], r["rev_prior_m"])) * 100, 1),
              "eps_q": r["eps_q"], "eps_q_prior": r["eps_q_prior"], "diluted_shares_m": r["dil_sh_m"],
              "sales_note": f"revenues ${r['rev_m']:,.1f}M vs ${r['rev_prior_m']:,.1f}M a year earlier",
              "nm_note": f"net margin ${r['nm_m']:,.1f}M vs ${r['nm_prior_m']:,.1f}M",
              "dist_note": (f"Distribution operating income {fm(r['dist_m'])} vs {fm(r['dist_prior_m'])}"
                            + ("; growth over the year-ago loss's absolute value (the CAT rule)" if r["dist_prior_m"] < 0 else "")),
              "margin_note": (f"operating income ${r['oi_m']:,.1f}M, income before minority interests and income taxes ${r['pti_m']:,.1f}M"
                              if "Minority" in t_pt else
                              f"operating income ${r['oi_m']:,.1f}M, income before income taxes ${r['pti_m']:,.1f}M (noncontrolling "
                              "interests deducted after taxes from 2009, FAS 160)"),
              "eps_note": f"diluted {fmt(r['eps_q'])} vs {fmt(r['eps_q_prior'])}",
              "cash_note": f"cash and cash equivalents ${cash[0] / 1000:,.1f}M at the quarter's end (consolidated)",
              "next_print": NEXT[q], "source_title": SOURCES[sid]["title"]})
    PR.append(d)


prt("OK12", "0001193125-07-168403", "Q2 2007", 2007, 2, "Aug 1")
prt("OK13", "0001193125-07-231343", "Q3 2007", 2007, 3, "Oct 31")
prt("OK14", "0001193125-08-037684", "Q4 2007", 2007, 4, "Feb 25")
prt("OK15", "0001193125-08-097560", "Q1 2008", 2008, 1, "Apr 30")
prt("OK16", "0001193125-08-166768", "Q2 2008", 2008, 2, "Aug 5")
prt("OK17", "0001193125-08-226207", "Q3 2008", 2008, 3, "Nov 5")
prt("OK18", "0001039684-09-000008", "Q4 2008", 2008, 4, "Feb 23")
prt("OK19", "0001039684-09-000018", "Q1 2009", 2009, 1, "Apr 29")
prt("OK20", "0001039684-09-000048", "Q2 2009", 2009, 2, "Aug 4")
prt("OK21", "0001039684-09-000075", "Q3 2009", 2009, 3, "Nov 3")
# each Q4 print came a day or two before its 10-K, and no weekly date falls between them (the builder asserts the vintage is public)
for q, f in (("Q4 2007", "F2007"), ("Q4 2008", "F2008")):
    p = next(x for x in PR if x["quarter"] == q)
    assert p["published"] < SOURCES[SID[f]]["published"], q
    days = [d for d in TDAYS if p["published"] < d < SOURCES[SID[f]]["published"]]
    assert not days, (q, "a trading day between the Q4 print and its 10-K")

# ── EPS guides: ONEOK's 'net income guidance' per diluted share (GAAP), a range for each fiscal year, from the releases and the
# guidance 8-Ks (Item 7.01); current-FY EPS is the latest range's midpoint (method r2's guide rule) ──
EG = []


def eguide(fy, sid, acc, doc, s, lo, hi, title=None):
    day, when = pub(acc)
    if sid not in SOURCES:
        SOURCES[sid] = {"published": day, "filed": when, "title": title,
                        "url": f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc.replace('-', '')}/{acc}.txt",
                        "supports": f"the FY{fy} EPS guide (net income guidance per diluted share)"}
    cands = sorted(glob.glob(os.path.join(SP, "*", acc, "EX-99*.rows.txt")) + glob.glob(os.path.join(SP, "*", acc, "8-K__*.rows.txt")))
    hits = [c for c in cands if re.sub(r"\s+", " ", s) in text(c)[0]]
    assert hits, (doc, s[:80])
    qt = quote(hits[0], s)
    assert f"${lo:.2f} to ${hi:.2f}" in qt, (doc, lo, hi)
    EG.append({"fy": fy, "published": day, "source": sid, "doc": doc, "eps_guide": [lo, hi], "quote": qt})


eguide(2007, "OK12", "0001193125-07-168403", "Q2 2007 release", "The company also reaffirmed its previous 2007 earnings guidance, but "
       "narrowed the range to $2.50 to $2.70 per diluted share", 2.50, 2.70)
eguide(2007, "OK22", "0001181431-07-057683", "8-K of 2007-09-17", "ONEOK, Inc. (NYSE: OKE) today reaffirmed its previous 2007 earnings "
       "guidance in the range of $2.50 to $2.70 per diluted share", 2.50, 2.70, "ONEOK 8-K: 2007 earnings guidance reaffirmed (Item 7.01)")
eguide(2007, "OK13", "0001193125-07-231343", "Q3 2007 release", "The company also increased its previous 2007 earnings guidance to a "
       "range of $2.62 to $2.72 per diluted share", 2.62, 2.72)
eguide(2007, "OK23", "0001193125-08-004466", "8-K of 2008-01-10", "ONEOK also increased its net income guidance for 2007 to $2.75 to "
       "$2.79 per diluted share", 2.75, 2.79, "ONEOK 8-K: 2008 net income guidance; 2007 guidance increased (Item 7.01)")
eguide(2008, "OK23", "0001193125-08-004466", "8-K of 2008-01-10", "ONEOK’s net income guidance for 2008 is in the range of $2.75 to "
       "$3.15 per diluted share.", 2.75, 3.15)
eguide(2008, "OK15", "0001193125-08-097560", "Q1 2008 release", "ONEOK also reaffirmed its 2008 net income guidance, announced on Jan. "
       "8, 2008, in the range of $2.75 to $3.15 per diluted share.", 2.75, 3.15)
eguide(2008, "OK16", "0001193125-08-166768", "Q2 2008 release", "ONEOK raised its 2008 net income guidance to the range of $2.90 to "
       "$3.10 per diluted share from the range of $2.75 to $3.15 per diluted share.", 2.90, 3.10)
eguide(2008, "OK17", "0001193125-08-226207", "Q3 2008 release", "The company also affirmed its 2008 net income guidance, but narrowed "
       "the range to $2.95 to $3.05 per diluted share", 2.95, 3.05)
eguide(2008, "OK24", "0000909281-09-000011", "8-K of 2009-02-09", "We also affirmed our net income guidance for 2008 of $2.95 to $3.05 "
       "per diluted share.", 2.95, 3.05, "ONEOK 8-K: 2009 net income guidance; 2008 guidance affirmed (Item 7.01)")
eguide(2009, "OK24", "0000909281-09-000011", "8-K of 2009-02-09", "Our 2009 net income guidance is estimated to be in the range of "
       "$2.25 to $2.75 per diluted share.", 2.25, 2.75)
eguide(2009, "OK19", "0001039684-09-000018", "Q1 2009 release", "ONEOK also reaffirmed its 2009 earnings per share guidance, announced "
       "on Feb. 5, 2009, in the range of $2.25 to $2.75 per diluted share.", 2.25, 2.75)
eguide(2009, "OK20", "0001039684-09-000048", "Q2 2009 release", "ONEOK also updated its 2009 earnings per share guidance to the range "
       "of $2.40 to $2.70 per diluted share from its previous range of $2.25 to $2.75 per diluted share", 2.40, 2.70)
eguide(2009, "OK21", "0001039684-09-000075", "Q3 2009 release", "The company also increased its 2009 net income guidance to the range "
       "of $2.65 to $2.85 per diluted share", 2.65, 2.85)
EG.sort(key=lambda g: (g["published"], g["fy"]))

# ── dividends: each rate change from the first filing that states it as declared ──
DV = []


def div(sid, acc, s, quarterly):
    day, when = pub(acc)
    SOURCES[sid] = {"published": day, "filed": when, "title": f"ONEOK 8-K: quarterly dividend of ${quarterly:.2f} (Item 8.01)",
                    "url": f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc.replace('-', '')}/{acc}.txt",
                    "supports": f"the quarterly dividend rate, ${quarterly:.2f} a share"}
    qt = quote(path(acc, "8-K__*.rows.txt"), s)
    DV.append({"published": day, "quarterly": quarterly, "source": sid,
               "note": f"${quarterly:.2f} a quarter, ${quarterly * 4:.2f} a year: '{qt}' ({SOURCES[sid]['title'].split(':')[0]} of {day})"})


div("OK25", "0001181431-07-046762", "On July 19, 2007, we announced an increase in our second quarter 2007 dividend to 36 cents per share "
    "of common stock.", 0.36)
div("OK26", "0001181431-08-004496", "On January 17, 2008, we announced an increase in the fourth quarter 2007 dividend paid on our "
    "common stock to 38 cents per share of common stock.", 0.38)
div("OK27", "0001181431-08-043642", "On July 17, 2008, we announced an increase in our quarterly dividend to 40 cents per share from 38 "
    "cents per share of common stock", 0.40)
div("OK28", "0001039684-09-000045", "On July 16, 2009, our board of directors declared a second-quarter 2009 dividend of 42 cents per "
    "share of common stock", 0.42)

# ── the listing (display): NYSE: OKE on every date ──
LST = [{"symbol": "OKE", "exchange": "NYSE", "published": SOURCES["OK12"]["published"], "effective": "1997-11-26", "source": "OK12",
        "note": quote(path("0001193125-07-168403", "EX-99.1__*.rows.txt"), "ONEOK, Inc. (NYSE: OKE)")}]
quote(D["F2006"], "Common stock, par value of $0.01 | New York Stock Exchange")


def rule_t_thresholds(k):
    unit, lower = RT[k]["unit"], RT[k]["lower_is_better"]
    v = sorted(RT[k]["values"].values())
    n = len(v)
    med = v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
    worst, best = (v[-1], v[0]) if lower else (v[0], v[-1])
    r = lambda x: math.floor(x / unit + 0.5) * unit
    return dict(zip(("BEAR", "BASE", "BULL", "XBULL"), (r(worst + (worst - med)), r(worst), r(med), r(best))))


for k in RT:
    RT[k]["thresholds"] = rule_t_thresholds(k)
facts = {
    "_doc": "Point-in-time fact sheet for OKE retrospectives (retro/build_oke.py): ONEOK, Inc. (NYSE: OKE). Generated by "
            "retro/generators/oke/gen_oke.py from the filings; every value carries a source and its publication date (the acceptance-time "
            "rule). Read retro/README.md, 'OKE', before editing.",
    "ticker": "OKE", "sources": dict(sorted(SOURCES.items(), key=lambda kv: int(kv[0][2:]))), "history_vintages": V, "prints": PR,
    "guides": [], "eps_guides": EG, "dividends": DV, "events": [], "company_names": [], "listings": LST, "rule_t": RT,
    "price_basis": ("Yahoo OKE, split-adjusted to today's shares: its 2:1 of 2001-06-12 precedes the P/E window (2002-01-01 on); its 2:1 "
                    "of 2012-06-04 and its 11422:10000 factor of 2014-02-03 (the ONE Gas separation, a distribution, not a split) follow "
                    "every built date, so the builder multiplies Yahoo's close by both, which gives the close as traded; the builder "
                    "refuses dates from 2012-06-04 until they are encoded"),
}
assert all(s["published"] <= CUT for s in SOURCES.values())
out = A.out or os.path.join(REPO, "retro", "facts", "OKE.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(facts, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_oke.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump({k: v for k, v in CHECK.items() if v}, fh, ensure_ascii=False, indent=1)
print(f"{out}: {len(V)} vintages, {len(PR)} prints, {len(EG)} EPS guides, {len(DV)} dividends, {len(SOURCES)} sources; "
      f"{sum(len(v) for v in CHECK.values())} quotes in {ck}")
for k in RT:
    print(k, RT[k]["values"], RT[k]["thresholds"])
for p in PR:
    print(p["quarter"], p["published"], p["sales_pct"], p["nm_pct"], p["dist_pct"], p["opm_bp"], p["ptm_bp"], p["eps_q"], p["eps_q_prior"])
