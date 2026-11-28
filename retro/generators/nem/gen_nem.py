#!/usr/bin/env python3
"""Generate retro/facts/NEM.json (2008-2009) from Newmont Mining Corporation's own filings (edgar.py's converted documents).

Every raw figure is typed once with the snippet of its own filing that holds it: the script asserts the snippet is in that
filing (whitespace, table rules, dot leaders, '|' and '$' flattened on both sides) and that the typed figures are consecutive
numbers in it. Every rate, margin, change and rule-T value is computed, never typed; every quoted sentence is asserted present
in its own filing word for word and written to the verbatim checklist (retro/tools/verbatim.py). Only filings accepted on or
before 2009-12-31 are read. The downloads (keep them outside the repo, e.g. in the session scratchpad):

    python3 retro/tools/edgar.py index 1164727 <dir>
    python3 retro/tools/edgar.py fetch 1164727 <dir> --from 2002-01-01 --to 2006-10-01 --forms 10-K 10-K/A 10-K405
    python3 retro/tools/edgar.py fetch 1164727 <dir> --from 2006-10-01 --to 2010-03-01 --forms 8-K 8-K/A 10-K 10-K/A
    python3 retro/tools/edgar.py index 71824 <old>         # the pre-2002 Newmont Mining Corporation (now Newmont USA Limited)
    python3 retro/tools/edgar.py fetch 71824 <old> --from 1997-01-01 --to 2001-12-31 --forms 10-K 10-K405 10-K405/A

    python3 -I retro/generators/nem/gen_nem.py --filings <dir> --old <old> [--out retro/facts/NEM.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_nem.json
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
_ap.add_argument("--old", required=True, help="the folder for CIK 71824 (the FY1997-FY2000 10-Ks)")
_ap.add_argument("--out")
_ap.add_argument("--checklist")
A = _ap.parse_args()
SP, OLD = os.path.abspath(A.filings), os.path.abspath(A.old)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402

ET = ZoneInfo("America/New_York")
CUT = "2009-12-31"
ROWS = {}
for d in (SP, OLD):
    for r in json.load(open(os.path.join(d, "allrows.json"))):
        ROWS[r[3]] = r
chart = retro_tool.chart("NEM")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
CHECK = {}


def path(acc, pat):
    hits = [p for base in (SP, OLD) for p in glob.glob(os.path.join(base, "*", acc, pat))]
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
        TEXT[p] = (re.sub(r"\s+", " ", raw), flat(raw))
    return TEXT[p]


def quote(p, s):
    """A sentence or fragment, word for word in its filing (whitespace collapsed); added to the checklist."""
    assert re.sub(r"\s+", " ", s) in text(p)[0], (p, s[:120])
    CHECK.setdefault(p, []).append(s)
    return s


def num(t):
    t = t.replace(",", "")
    if t in ("—", "--", "–"):
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


def src(sid, acc, cik, title, supports, date_only=False):
    day, when = pub(acc)
    if date_only:                      # before 2002-2003 EDGAR records the filing date only
        day, when = ROWS[acc][0], f"filed {ROWS[acc][0]} (EDGAR gives the filing date only)"
    SOURCES[sid] = {"published": day, "filed": when, "title": title,
                    "url": f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace('-', '')}/{acc}.txt", "supports": supports}
    return sid


pct = lambda a, b: round((b / a - 1) * 100 + 0.0, 2)
pct1 = lambda a, b: round((b / a - 1) * 100 + 0.0, 1)

# ── sources: the decade's 10-Ks (rule T), the history vintages, the releases and the outlook 8-Ks ─────────────────────────────
OLDCIK, CIK = 71824, 1164727
F1998 = src("NM1", "0000950134-99-002280", OLDCIK, "Newmont Mining Corporation FY1998 10-K405 (Exhibit 13, the 1998 annual report)",
            "rule T: 1997 against 1996 (equity production and total cash cost per equity ounce; sales and pre-tax income)", True)
F1999 = src("NM2", "0000927356-00-000580", OLDCIK, "Newmont Mining Corporation FY1999 10-K405 (Exhibit 13, the 1999 annual report)",
            "rule T: 1998 against 1997 (equity production and total cash cost per equity ounce)", True)
F1999A = src("NM3", "0000950130-00-006251", OLDCIK, "Newmont Mining Corporation FY1999 10-K405/A (Amendment No. 2: consolidating statements)",
             "rule T: 1998 against 1997 (sales and pre-tax income, the consolidated column)", True)
F2000 = src("NM4", "0000927356-01-000391", OLDCIK, "Newmont Mining Corporation FY2000 10-K405 (Item 6; the supplemental consolidated "
            "results with Battle Mountain, pages NM-1 on)", "rule T: 1997 against 1996 (sales, Item 6); 1999 against 1998 (equity ounces "
            "sold, total cash cost, sales and pre-tax income, supplemental)", True)
F2001A = src("NM5", "0000930661-03-001112", CIK, "Newmont FY2001 10-K/A (Amendment No. 1, the restated 2001 report)",
             "rule T: 1998 against 1997 (sales, Item 6); 2000 against 1999 (equity ounces sold, total cash cost, sales and pre-tax income)")
F2002A = src("NM6", "0001193125-03-066826", CIK, "Newmont FY2002 10-K/A (Amendment No. 1)",
             "rule T: 1999 against 1998 (sales, Item 6); 2001 against 2000 (equity ounces sold, costs applicable to sales per ounce, sales "
             "and pre-tax income)")
F2003 = src("NM7", "0001193125-04-042223", CIK, "Newmont FY2003 10-K", "rule T: 2000 against 1999 (revenues, Item 6)")
F2003A = src("NM8", "0001193125-04-126163", CIK, "Newmont FY2003 10-K/A (Amendment No. 1: Items 7 and 8 re-filed)",
             "rule T: 2002 against 2001 (equity ounces sold, total cash cost per equity ounce, sales and pre-tax income)")
F2004 = src("NM9", "0001193125-05-050868", CIK, "Newmont FY2004 10-K", "rule T: 2001 against 2000 (revenues, Item 6); 2003 against 2002 "
            "(equity ounces sold, costs applicable to sales per ounce, sales and pre-tax income); FY2002 diluted shares")
F2005A = src("NM10", "0001193125-06-216043", CIK, "Newmont FY2005 10-K/A (Amendment No. 1)", "rule T: 2002 against 2001 (revenues, Item 6); "
             "2004 against 2003 (consolidated ounces sold, costs applicable to sales per ounce, sales and pre-tax income); FY2001 a loss; "
             "FY2003 diluted shares")
F2006 = src("NM11", "0001193125-07-038537", CIK, "Newmont FY2006 10-K", "history: 2002-2003 diluted EPS from continuing operations and "
            "revenues; rule T: 2003 and 2004 revenue changes, 2005 and 2006 ounce and cost changes; the 'why'")
R2006 = src("NM12", "0001193125-07-218594", CIK, "Newmont 8-K: updated FY2006 consolidated financial statements (Merchant Banking "
            "discontinued)", "history vintage FY2006 (2004-2006 from continuing operations without Merchant Banking); rule T: 2005 "
            "and 2006 revenue and pre-tax margin changes")
F2007 = src("NM13", "0001193125-08-035169", CIK, "Newmont FY2007 10-K", "history vintage FY2007; the 'why'")
F2008 = src("NM14", "0000950134-09-003236", CIK, "Newmont FY2008 10-K", "history vintage FY2008; the 'why'")
R2008 = src("NM15", "0000950123-09-043136", CIK, "Newmont 8-K: FY2008 Items 6-8 recast (FSP APB 14-1, FAS 160, Kori Kollo and the "
            "2009 segments)", "history vintage FY2008 as recast (from 2009-09-15)")
D = {k: path(a, p) for k, a, p in [
    ("F1998", "0000950134-99-002280", "EX-13__10"), ("F1999", "0000927356-00-000580", "EX-13__4"),
    ("F1999A", "0000950130-00-006251", "10-K405_A__0001.txt"), ("F2000", "0000927356-01-000391", "10-K405__0001.txt"),
    ("F2001A", "0000930661-03-001112", "10-K_A__d10ka.rows.txt"), ("F2002A", "0001193125-03-066826", "10-K_A__d10ka.rows.txt"),
    ("F2003", "0001193125-04-042223", "10-K__d10k.rows.txt"), ("F2003A", "0001193125-04-126163", "10-K_A__d10ka.rows.txt"),
    ("F2004", "0001193125-05-050868", "10-K__d10k.rows.txt"), ("F2005A", "0001193125-06-216043", "10-K_A__d10ka.rows.txt"),
    ("F2006", "0001193125-07-038537", "10-K__d10k.rows.txt"), ("R2006", "0001193125-07-218594", "EX-99.1__dex991.rows.txt"),
    ("F2007", "0001193125-08-035169", "10-K__d10k.rows.txt"), ("F2008", "0000950134-09-003236", "10-K__d65086e10vk.rows.txt"),
    ("R2008", "0000950123-09-043136", "EX-99.1__c90174exv99w1.rows.txt")]}
SID = {"F1998": F1998, "F1999": F1999, "F1999A": F1999A, "F2000": F2000, "F2001A": F2001A, "F2002A": F2002A, "F2003": F2003,
       "F2003A": F2003A, "F2004": F2004, "F2005A": F2005A, "F2006": F2006, "R2006": R2006}

# ── rule T over 1997-2006 (the decade of the vintage public on 2008-01-04): each change from the latest filing published by then
# that tabulates both years, as tabulated (seams in, as published) ──
RT = {"oz": {"unit": 1, "lower_is_better": False, "values": {}, "raw": {}},
      "cas": {"unit": 1, "lower_is_better": True, "values": {}, "raw": {}},
      "revenue": {"unit": 1, "lower_is_better": False, "values": {}, "raw": {}},
      "eps": {"unit": 1, "lower_is_better": False, "values": {}, "raw": {}},
      "margin": {"unit": 10, "lower_is_better": False, "values": {}, "raw": {}}}


def rt_vol(y, f, snip, toks_oz, toks_cost, line_oz, line_cost, snip_cost=None):
    """Ounces and the per-ounce cost of year y against y-1 (each list is (prior, current) in the filing's own order given)."""
    o = S(D[f], snip, *toks_oz)
    c = S(D[f], snip_cost or snip, *toks_cost)
    po, co = o[toks_oz.index(line_oz[0])], o[toks_oz.index(line_oz[1])]
    pc, cc = c[toks_cost.index(line_cost[0])], c[toks_cost.index(line_cost[1])]
    RT["oz"]["raw"][str(y)] = {"source": SID[f], "oz_k": [po, co], "rows": [snip]}
    RT["oz"]["values"][str(y)] = pct(po, co)
    RT["cas"]["raw"][str(y)] = {"source": SID[f], "cost": [pc, cc], "rows": [snip_cost or snip]}
    RT["cas"]["values"][str(y)] = pct(pc, cc)


# 1997: the FY1998 annual report's equity production and total cash cost per equity ounce (no ounces-sold line)
rt_vol(1997, "F1998", "Total/Weighted average 4,070.7 3,956.8 3,104.1 $ 183 $ 187 $ 218",
       ("4,070.7", "3,956.8", "3,104.1"), ("183", "187", "218"), ("3,104.1", "3,956.8"), ("218", "187"))
rt_vol(1998, "F1999", "Total/Weighted average 4,175.5 4,070.7 3,956.8 $ 175 $ 183 $ 187",
       ("4,175.5", "4,070.7", "3,956.8"), ("175", "183", "187"), ("3,956.8", "4,070.7"), ("187", "183"))
rt_vol(1999, "F2000", "Total/Weighted average.............. 5,727.8 4,946.2 4,954.3 $170 $173 $179",
       ("5,727.8", "4,946.2", "4,954.3"), ("170", "173", "179"), ("4,954.3", "4,946.2"), ("179", "173"))
rt_vol(2000, "F2001A", "Total/Weighted average(1) | 5,466.1 | 5,763.7 | 4,946.2 | 184 | 170 | 173",
       ("5,466.1", "5,763.7", "4,946.2"), ("184", "170", "173"), ("4,946.2", "5,763.7"), ("173", "170"))
rt_vol(2001, "F2002A", "Equity Ounces Sold (000) | 255.8 | 222.0 | 251.4 | 380.7 | 341.5 | 354.2 | 6,971.4 | 5,171.0 | 5,585.3",
       ("6,971.4", "5,171.0", "5,585.3"), ("192", "187", "173"), ("5,585.3", "5,171.0"), ("173", "187"),
       "Total costs applicable to sales | 133 | 137 | 130 | 178 | 145 | 135 | 192 | 187 | 173")
rt_vol(2002, "F2003A", "Newmont Total/Weighted-Average | 7,383.6 | 7,631.7 | 5,466.1 | 203 | 189 | 184",
       ("7,383.6", "7,631.7", "5,466.1"), ("203", "189", "184"), ("5,466.1", "7,631.7"), ("184", "189"))
rt_vol(2003, "F2004", "Equity ounces sold (000) | 6,988.4 | 7,383.6 | 7,631.7",
       ("6,988.4", "7,383.6", "7,631.7"), ("233", "205", "192"), ("7,631.7", "7,383.6"), ("192", "205"),
       "Total cash costs | 231 | 203 | 189 Reclamation/accretion expense and other | 2 | 2 | 3 "
       "Total costs applicable to sales | 233 | 205 | 192")
rt_vol(2004, "F2005A", "Total/Weighted-Average | 8,552.0 | 8,828.9 | 8,377.4 | 236 | 216 | 195 | 60 | 60 | 58",
       ("8,552.0", "8,828.9", "8,377.4"), ("236", "216", "195"), ("8,377.4", "8,828.9"), ("195", "216"))
for y, pair_oz, pair_c in ((2005, ("8,618.8", "8,429.3"), ("218", "237")), (2006, ("8,429.3", "7,361.2"), ("237", "304"))):
    rt_vol(y, "F2006", "Total/Weighted-Average | 7,361.2 | 8,429.3 | 8,618.8 | 304 | 237 | 218 | 73 | 60 | 60",
           ("7,361.2", "8,429.3", "8,618.8"), ("304", "237", "218"), pair_oz, pair_c)


def rt_rev(y, f, snip, toks, prior, cur):
    v = S(D[f], snip, *toks)
    a, b = v[toks.index(prior)], v[toks.index(cur)]
    RT["revenue"]["raw"][str(y)] = {"source": SID[f], "revenue_m": [a, b], "rows": [snip]}
    RT["revenue"]["values"][str(y)] = pct(a, b)


rt_rev(1997, "F2000", "Sales........................ $1,554.9 $1,398.9 $1,453.9 $1,572.8 $1,105.7",
       ("1,554.9", "1,398.9", "1,453.9", "1,572.8", "1,105.7"), "1,105.7", "1,572.8")
rt_rev(1998, "F2001A", "Sales | 1,666.1 | 1,819.0 | 1,627.1 | 1,730.5 | 1,917.7", ("1,666.1", "1,819.0", "1,627.1", "1,730.5", "1,917.7"),
       "1,917.7", "1,730.5")
rt_rev(1999, "F2002A", "Sales | 2,622.2 | 1,666.1 | 1,819.0 | 1,627.1 | 1,730.5", ("2,622.2", "1,666.1", "1,819.0", "1,627.1", "1,730.5"),
       "1,730.5", "1,627.1")
rt_rev(2000, "F2003", "Revenues | 3,214.1 | 2,657.9 | 1,666.7 | 1,819.6 | 1,627.9", ("3,214.1", "2,657.9", "1,666.7", "1,819.6", "1,627.9"),
       "1,627.9", "1,819.6")
rt_rev(2001, "F2004", "Revenues | 4,524.2 | 3,157.8 | 2,622.2 | 1,666.1 | 1,819.0", ("4,524.2", "3,157.8", "2,622.2", "1,666.1", "1,819.0"),
       "1,819.0", "1,666.1")
rt_rev(2002, "F2005A", "Revenues | 4,406 | 4,411 | 3,059 | 2,541 | 1,642", ("4,406", "4,411", "3,059", "2,541", "1,642"), "1,642", "2,541")
for y, a, b in ((2003, "2,458", "2,980"), (2004, "2,980", "4,326")):
    rt_rev(y, "F2006", "Revenues | 4,987 | 4,352 | 4,326 | 2,980 | 2,458", ("4,987", "4,352", "4,326", "2,980", "2,458"), a, b)
for y, a, b in ((2005, "4,326", "4,352"), (2006, "4,352", "4,987")):
    rt_rev(y, "R2006", "Sales - copper, net | 671 | 672 | 786 4,987 | 4,352 | 4,326", ("4,987", "4,352", "4,326"), a, b)


def rt_margin(y, f, sales, pretax):
    """Pre-tax margin change of year y: income before income taxes (minority interest and equity income outside it) on the sales
    lines (gold and base metals or copper; royalties, gains and other income left out), (prior, current) from one filing.
    sales: [(snippet, tokens, prior_tok, cur_tok), ...] summed; pretax: (snippet, tokens, prior_tok, cur_tok)."""
    rv = [0.0, 0.0]
    rows = []
    for snip, toks, a, b in sales:
        v = S(D[f], snip, *toks)
        rv[0] += v[toks.index(a)] if a is not None else 0.0
        rv[1] += v[toks.index(b)]
        rows.append(snip)
    snip, toks, a, b = pretax
    v = S(D[f], snip, *toks)
    pt = [v[toks.index(a)], v[toks.index(b)]]
    rows.append(snip)
    RT["margin"]["raw"][str(y)] = {"source": SID[f], "pretax_m": pt, "sales_m": [round(x, 3) for x in rv], "rows": rows}
    RT["margin"]["values"][str(y)] = round((pt[1] / rv[1] - pt[0] / rv[0]) * 10000 + 0.0, 1)


rt_margin(1997, "F1998", [("Sales $ 1,453,856 $ 1,572,757 $ 1,105,666", ("1,453,856", "1,572,757", "1,105,666"), "1,105,666", "1,572,757")],
          ("accounting principle (461,885) 131,915 39,066", ("(461,885)", "131,915", "39,066"), "39,066", "131,915"))
_s98 = S(D["F1999A"], "1998 Sales and other income Sales.................. $ -- $ 483.0 $ 970.9 $ -- $1,453.9", "1,453.9")
_s97 = S(D["F1999A"], "1997 Sales and other income Sales.................. $ -- $ 609.6 $ 963.1 $ -- $1,572.7", "1,572.7")
_p98 = S(D["F1999A"], "cumulative effect of a change in accounting principle.............. -- (166.0) (295.9) -- (461.9)", "(461.9)")
_p97 = S(D["F1999A"], "Pre-tax income before minority interest and equity income.......... -- 3.1 128.8 -- 131.9", "131.9")
RT["margin"]["raw"]["1998"] = {"source": F1999A, "pretax_m": [_p97[0], _p98[0]], "sales_m": [_s97[0], _s98[0]],
                               "rows": ["Sales $ -- $ 483.0 $ 970.9 $ -- $1,453.9 (1998)", "Sales $ -- $ 609.6 $ 963.1 $ -- $1,572.7 (1997)",
                                        "Pre-tax loss ... (461.9) (1998)", "Pre-tax income ... 131.9 (1997)"]}
RT["margin"]["values"]["1998"] = round((_p98[0] / _s98[0] - _p97[0] / _s97[0]) * 10000 + 0.0, 1)
rt_margin(1999, "F2000", [("Sales.................................... $1,809,450 $1,627,083 $1,730,479",
                           ("1,809,450", "1,627,083", "1,730,479"), "1,730,479", "1,627,083")],
          ("principles................................ 19,997 59,530 (591,014)", ("19,997", "59,530", "(591,014)"), "(591,014)", "59,530"))
rt_margin(2000, "F2001A", [("Sales | 1,666,108 | 1,819,005 | 1,627,083", ("1,666,108", "1,819,005", "1,627,083"), "1,627,083", "1,819,005")],
          ("Pre-tax income (loss) before minority interest, equity income (loss) and cumulative effect of a change in accounting "
           "principle | (63,051) | 38,918 | 35,122", ("(63,051)", "38,918", "35,122"), "35,122", "38,918"))
rt_margin(2001, "F2002A", [("Sales—gold | 2,566,833 | 1,666,108 | 1,819,005", ("2,566,833", "1,666,108", "1,819,005"), "1,819,005", "1,666,108"),
                           ("Sales—base metals, net | 55,321 | — | —", ("55,321", "—", "—"), "—", "—")],
          ("Pre-tax income (loss) before minority interest, equity income (loss) of affiliates and cumulative effect of a change in "
           "accounting principle | 216,326 | (63,051) | 38,918", ("216,326", "(63,051)", "38,918"), "38,918", "(63,051)"))
rt_margin(2002, "F2003A", [("Sales—gold | 3,082,936 | 2,566,833 | 1,666,108", ("3,082,936", "2,566,833", "1,666,108"), "1,666,108", "2,566,833"),
                           ("Sales—base metals, net | 74,820 | 55,321 | —", ("74,820", "55,321", "—"), "—", "55,321")],
          ("cumulative effect of a change in accounting principle | 925,386 | 216,326 | (63,051)", ("925,386", "216,326", "(63,051)"),
           "(63,051)", "216,326"))
rt_margin(2003, "F2004", [("Sales—gold, net | 3,653,563 | 3,082,936 | 2,566,833", ("3,653,563", "3,082,936", "2,566,833"), "2,566,833", "3,082,936"),
                          ("Sales—base metals, net | 870,622 | 74,820 | 55,321", ("870,622", "74,820", "55,321"), "55,321", "74,820")],
          ("cumulative effect of a change in accounting principle | 1,099,005 | 925,386 | 216,326", ("1,099,005", "925,386", "216,326"),
           "216,326", "925,386"))
rt_margin(2004, "F2005A", [("Sales—gold, net | 3,734 | 3,625 | 3,059", ("3,734", "3,625", "3,059"), "3,059", "3,625"),
                           ("Sales—copper, net | 672 | 786 | —", ("672", "786", "—"), "—", "786")],
          ("Income from continuing operations before income tax, minority interest and equity income (loss) of affiliates | 1,064 | "
           "1,111 | 931", ("1,064", "1,111", "931"), "931", "1,111"))
for y, a, b in ((2005, "1,068", "915"), (2006, "915", "1,231")):
    ga, gb = {"1,068": "3,540", "915": "3,680", "1,231": "4,316"}[a], {"915": "3,680", "1,231": "4,316"}[b]
    ca, cb = {"1,068": "786", "915": "672"}[a], {"915": "672", "1,231": "671"}[b]
    rt_margin(y, "R2006", [("Sales - gold, net | 4,316 | 3,680 | 3,540", ("4,316", "3,680", "3,540"), ga, gb),
                           ("Sales - copper, net | 671 | 672 | 786", ("671", "672", "786"), ca, cb)],
              ("Income from continuing operations before income tax, minority interest and equity income of affiliates | 1,231 | "
               "915 | 1,068", ("1,231", "915", "1,068"), a, b))

# ── history vintages: each year from the latest filing that reports it ───────────────────────────────────────────────────────
WHY_Q = ["One of the most significant risks is fluctuation in the prices of gold and copper, which are affected by numerous factors "
         "beyond our control.", "A Substantial or Extended Decline in Gold or Copper Prices Would Have a Material Adverse Effect on Newmont"]


def why(f, lead):
    for w in ("cyclical",):                       # DURABLE needs the company not to call its own business cyclical (the MU rule)
        assert w not in text(D[f])[0].lower(), (f, w)
    q = [quote(D[f], lead)] + [quote(D[f], s) for s in WHY_Q]
    label = {"F2006": "FY2006", "F2007": "FY2007", "F2008": "FY2008"}[f]
    return " ".join(f"'{x}'" for x in q) + (f" (the {label} 10-K's own words; it does not call the business cyclical, so DURABLE, "
                                            "the MU rule)")


# FY2006 history as the 8-K of 2007-10-16 recasts it (Merchant Banking discontinued): 2004-2006 from it, 2002-2003 from the FY2006 10-K
e06 = S(D["R2006"], "Income from continuing operations per common share, diluted | 1.18 | 0.60 | 0.91", "1.18", "0.60", "0.91")
e0603 = S(D["F2006"], "Diluted income (loss) per common share: From continuing operations | 1.86 | 0.80 | 0.92 | 1.15 | 0.29",
          "1.86", "0.80", "0.92", "1.15", "0.29")
r06 = S(D["R2006"], "Sales - copper, net | 671 | 672 | 786 4,987 | 4,352 | 4,326", "4,987", "4,352", "4,326")
r0603 = S(D["F2006"], "Revenues | 4,987 | 4,352 | 4,326 | 2,980 | 2,458", "4,987", "4,352", "4,326", "2,980", "2,458")
sh06 = S(D["R2006"], "Diluted weighted-average common shares outstanding | 452 | 449 | 447", "452", "449", "447")
sh03 = S(D["F2005A"], "Diluted weighted-average common shares outstanding | 449 | 447 | 414", "449", "447", "414")
sh02 = S(D["F2004"], "Diluted weighted-average common shares outstanding | 446,511 | 413,723 | 372,975", "446,511", "413,723", "372,975")
e01 = S(D["F2005A"], "Diluted income (loss) per common share: From continuing operations | 0.83 | 1.01 | 1.23 | 0.38 | (0.27)",
        "0.83", "1.01", "1.23", "0.38", "(0.27)")
g06 = S(D["R2006"], "Sales - gold, net | 4,316 | 3,680 | 3,540", "4,316", "3,680", "3,540")
c06 = S(D["R2006"], "Sales - copper, net | 671 | 672 | 786", "671", "672", "786")
pt06 = S(D["R2006"], "Income from continuing operations before income tax, minority interest and equity income of affiliates | 1,231 | "
         "915 | 1,068", "1,231", "915", "1,068")
tx06 = S(D["R2006"], "Income tax expense (Note 7) | (337) | (270) | (327)", "(337)", "(270)", "(327)")
cf06 = S(D["R2006"], "Net cash provided from continuing operations | 1,133 | 1,182 | 1,449", "1,133", "1,182", "1,449")
cx06 = S(D["R2006"], "Additions to property, plant and mine development | (1,545) | (1,216) | (669)", "(1,545)", "(1,216)", "(669)")
ca06 = S(D["R2006"], "Cash and cash equivalents | 1,166 | 1,082", "1,166", "1,082")
oz06 = S(D["F2006"], "Consolidated gold ounces sold (thousands)(1) | 7,361 | 8,429 | 8,619", "7,361", "8,429", "8,619")
cs06 = S(D["F2006"], "Costs applicable to sales(3) Gold (per ounce) | 304 | 237 | 218", "304", "237", "218")

FIRST_EXCL = {"2001": "a loss: $(0.27) a diluted share from continuing operations (FY2005 10-K/A), as were 1998-2000 ($(3.26), $(0.62) and "
              "$(0.45) before the cumulative effect, the FY2002-FY2004 10-Ks); a loss year that is not the latest takes the years before it "
              "(the PFE 2003, CMCSA 2003 and MU FY2003 rule), so the history starts with FY2002 and the P/E window on 2002-01-01, the day "
              "after FY2001 ended (the window holds the old Newmont's January-February 2002 days, before the Normandy and Franco-Nevada "
              "acquisitions, priced on FY2002's EPS)"}
NORM = ("GAAP diluted EPS from continuing operations before the cumulative effect of accounting changes, each year from the latest filing "
        "that reports it; Newmont publishes no EPS excluding one-offs for 2002-2006, whose listed items are small fractions of their "
        "income (2002: an after-tax $38.3M derivative loss, a $30.7M Lihir gain, $2.4M of write-downs and $10.2M of tax benefits against "
        "$146.6M, the FY2002 10-K/A)")
DIV_NOTE = "$0.10 a quarter, $0.40 a year (each 10-K's dividends declared per common share)"
V = []
V.append({
    "published": SOURCES[R2006]["published"], "sources": [R2006, F2006, F2005A, F2004], "company": "Newmont Mining Corporation",
    "exchange": "NYSE", "business_line": "gold producer, with copper from Batu Hijau (Indonesia)", "fy_label": "FY06",
    "eps_normalized": {"2002": e0603[4], "2003": e0603[3], "2004": e06[2], "2005": e06[1], "2006": e06[0]},
    "eps_sources": {"2002": F2006, "2003": F2006, "2004": R2006, "2005": R2006, "2006": R2006},
    "eps_excluded": {}, "eps_first_excluded": FIRST_EXCL,
    "revenue_usd_b": {"2002": r0603[4] / 1000, "2003": r0603[3] / 1000, "2004": r06[2] / 1000, "2005": r06[1] / 1000, "2006": r06[0] / 1000},
    "revenue_sources": {"2002": F2006, "2003": F2006, "2004": R2006, "2005": R2006, "2006": R2006},
    "diluted_shares_m": {"2002": round(sh02[2] / 1000, 3), "2003": sh03[2], "2004": sh06[2], "2005": sh06[1], "2006": sh06[0]},
    "shares_sources": {"2002": F2004, "2003": F2005A, "2004": R2006, "2005": R2006, "2006": R2006},
    "normalization": NORM + "; 2004-2006 as the 8-K of 2007-10-16 recasts them without Merchant Banking, 2002-2003 from the FY2006 10-K "
                     "(with it: a seam, as published)",
    "pe_window_start": "2002-01-01",
    "prev_fy_margin": round(pt06[0] / r06[0] * 100, 2), "prev_fy_margin_note": "FY06 income from continuing operations before income tax, "
    f"minority interest and equity income ${pt06[0]:,.0f}M / revenues ${r06[0]:,.0f}M (8-K of 2007-10-16)",
    "tax_rate": round(-tx06[0] / pt06[0], 4), "tax_note": f"FY06 income tax expense ${-tx06[0]:,.0f}M / pre-tax ${pt06[0]:,.0f}M (8-K of 2007-10-16)",
    "prev_fy_sales_growth": pct1(r06[1], r06[0]),
    "prev_fy_oz_k": oz06[0], "prev_fy_oz_pct": pct1(oz06[1], oz06[0]), "prev_fy_cas": cs06[0],
    "prev_fy_cas_pct": pct1(cs06[1], cs06[0]), "franchise_source": "FY2006 10-K",
    "dividend_annual": 0.40, "dividend_note": DIV_NOTE + ": FY2006 10-K",
    "cash_b": ca06[0] / 1000, "fcf_b": round((cf06[0] + cx06[0]) / 1000, 3), "fcf_label": "FY06",
    "fcf_note": f"net cash provided from continuing operations ${cf06[0]:,.0f}M less additions to property, plant and mine development "
                f"${-cx06[0]:,.0f}M (8-K of 2007-10-16)",
    "cash_return_text": "dividend $0.10 a quarter; no repurchase program in the FY2006 10-K",
    "groups": [["Gold", g06[0] / 1000, pct1(g06[1], g06[0])], ["Copper", c06[0] / 1000, pct1(c06[1], c06[0])]],
    "groups_basis": "FY06 sales by metal, net (8-K of 2007-10-16)", "margin_signal_name": "Pre-tax margin change",
    "kind": "DURABLE", "why": why("F2006", "Newmont is one of the world’s largest gold producers and is the only gold company included in the "
                                  "S&P 500 Index."),
})
V[-1]["eps_first_excluded"]["2001"] += f" [FY2005 10-K/A row: diluted from continuing operations 2005-2001 {e01}]"

# FY2007 10-K: 2003-2007 from it (FY2007 excluded: a loss with listed one-offs larger than the year's income, no figure without them)
e07 = S(D["F2007"], "Diluted (loss) income per common share: From continuing operations | (2.13) | 1.25 | 0.62 | 0.93 | 0.94",
        "(2.13)", "1.25", "0.62", "0.93", "0.94")
r07 = S(D["F2007"], "Revenues | 5,526 | 4,882 | 4,265 | 4,222 | 2,792", "5,526", "4,882", "4,265", "4,222", "2,792")
sh07 = S(D["F2007"], "Diluted weighted-average common shares outstanding | 452 | 452 | 449", "452", "452", "449")
g07 = S(D["F2007"], "Sales - gold, net | 4,305 | 4,211 | 3,593", "4,305", "4,211", "3,593")
pt07 = S(D["F2007"], "(Loss) income from continuing operations before income tax, minority interest and equity income of affiliates | "
         "(352) | 1,250 | 924", "(352)", "1,250", "924")
ca07 = S(D["F2007"], "Cash and cash equivalents | 1,231 | 1,166", "1,231", "1,166")
oz07 = S(D["F2007"], "Consolidated gold ounces sold (thousands)(1) | 6,184 | 7,186 | 8,237", "6,184", "7,186", "8,237")
cs07 = S(D["F2007"], "Costs applicable to sales(3) Gold (per ounce) | 406 | 303 | 235", "406", "303", "235")
tx07 = quote(D["F2007"], "Income tax expense was $200 in 2007, compared to $326 and $270 in 2006 and 2005, respectively.")
cfq07 = quote(D["F2007"], "Net cash provided from continuing operations was $525, $1,129 and $1,169 for 2007, 2006 and 2005, respectively")
cxq07 = quote(D["F2007"], "Additions to property, plant and mine development were $1,670, $1,537 and $1,204 for continuing operations in "
              "2007, 2006 and 2005, respectively.")
EXCL07 = ("a loss with no figure excluding only its one-offs: $(2.13) a diluted share from continuing operations (FY2007 10-K); the Q4 "
          "2007 release lists $1,544M of after-tax charges in continuing operations ('Write-down of Exploration goodwill' $1,122M, "
          "'Loss on settlement of gold contracts' $358M, marketable securities $39M, the Batu Hijau minority loan $25M) against its "
          "$963M loss, but publishes no per-share figure without them; excluded as the latest year (the NKE FY2018 and XOM FY2020 rule), "
          "its own days leave the P/E window, and it stays a gap")
for s in ("Write-down of Exploration goodwill", "Loss on settlement of gold contracts"):
    quote(path("0001144204-08-011007", "EX-99.1__*ex99-1.txt"), s)
_c07 = S(path("0001144204-08-011007", "EX-99.1__*ex99-1.txt"),
         "Write-down of Exploration goodwill $(1,122) $ -- $(1,122) $ -- Loss on settlement of gold contracts $ -- $ -- $ (358) $ (23) "
         "Write-down of marketable securities $ (39) $ -- $ (39) $ -- Batu Hijau minority loan repayment $ -- $ -- $ (25) $ --",
         "(1,122)", "--", "(1,122)", "--")
assert 1122 + 358 + 39 + 25 > 963 + 0, "the listed charges exceed the loss's distance to zero: no year without them is a loss"
V.append({**{k: V[0][k] for k in ("company", "exchange", "business_line", "pe_window_start", "margin_signal_name", "kind")},
    "published": SOURCES[F2007]["published"], "sources": [F2007, F2006, R2006, F2005A, F2004], "fy_label": "FY07",
    "eps_normalized": {"2002": e0603[4], "2003": e07[4], "2004": e07[3], "2005": e07[2], "2006": e07[1]},
    "eps_sources": {"2002": F2006, "2003": F2007, "2004": F2007, "2005": F2007, "2006": F2007},
    "eps_excluded": {"2007": EXCL07}, "eps_first_excluded": V[0]["eps_first_excluded"],
    "revenue_usd_b": {"2002": r0603[4] / 1000, "2003": r07[4] / 1000, "2004": r07[3] / 1000, "2005": r07[2] / 1000, "2006": r07[1] / 1000,
                      "2007": r07[0] / 1000},
    "revenue_sources": {"2002": F2006, **{y: F2007 for y in ("2003", "2004", "2005", "2006", "2007")}},
    "diluted_shares_m": {"2002": round(sh02[2] / 1000, 3), "2003": sh03[2], "2004": sh06[2], "2005": sh07[2], "2006": sh07[1], "2007": sh07[0]},
    "shares_sources": {"2002": F2004, "2003": F2005A, "2004": R2006, "2005": F2007, "2006": F2007, "2007": F2007},
    "normalization": NORM + "; 2003-2007 from the FY2007 10-K (Merchant Banking and Pajingo discontinued), 2002 from the FY2006 10-K "
                     "(a seam, as published)",
    "prev_fy_margin": round(pt07[0] / r07[0] * 100, 2), "prev_fy_margin_note": "FY07 loss from continuing operations before income tax, "
    f"minority interest and equity income ${pt07[0]:,.0f}M / revenues ${r07[0]:,.0f}M (FY2007 10-K)",
    "tax_rate": round(200 / pt07[0], 4), "tax_note": "FY07 income tax expense $200M on a pre-tax loss of $352M (FY2007 10-K: '" + tx07 + "')",
    "prev_fy_sales_growth": pct1(r07[1], r07[0]),
    "prev_fy_oz_k": oz07[0], "prev_fy_oz_pct": pct1(oz07[1], oz07[0]), "prev_fy_cas": cs07[0],
    "prev_fy_cas_pct": pct1(cs07[1], cs07[0]), "franchise_source": "FY2007 10-K",
    "dividend_annual": 0.40, "dividend_note": DIV_NOTE + ": FY2007 10-K",
    "cash_b": ca07[0] / 1000, "fcf_b": round((525 - 1670) / 1000, 3), "fcf_label": "FY07",
    "fcf_note": "net cash provided from continuing operations $525M (after the $578M settlement of the price-capped forward sales "
                "contracts) less additions to property, plant and mine development $1,670M (FY2007 10-K: '" + cfq07 + "'; '" + cxq07 + "')",
    "cash_return_text": "dividend $0.10 a quarter; no repurchase program in the FY2007 10-K",
    "groups": [["Gold", g07[0] / 1000, pct1(g07[1], g07[0])], ["Copper", round((r07[0] - g07[0]) / 1000, 3),
                                                                     pct1(r07[1] - g07[1], r07[0] - g07[0])]],
    "groups_basis": "FY07 sales by metal, net (FY2007 10-K; copper as revenues less gold)",
    "why": why("F2007", "Newmont is one of the world’s largest gold producers and is the only gold company included in the S&P 500 Index, "
                        "Fortune 500 and in the Dow Jones Sustainability Index-World."),
})

# FY2008 10-K: 2004-2008 from it; the FY2008 10-K/A of 2009-06-08 only corrects the audit report's date (adds nothing)
quote(path("0000950123-09-012276", "10-K_A__*.rows.txt"), "to correct a typographical error in the date of the Audit Report from "
      "February 18, 2008 to February 18, 2009.")
e08 = S(D["F2008"], "Diluted income (loss) per common share: From continuing operations | 1.82 | (2.13) | 1.25 | 0.62 | 0.93",
        "1.82", "(2.13)", "1.25", "0.62", "0.93")
r08 = S(D["F2008"], "Revenues | 6,199 | 5,526 | 4,882 | 4,265 | 4,222", "6,199", "5,526", "4,882", "4,265", "4,222")
sh08 = S(D["F2008"], "Diluted weighted-average common shares outstanding | 455 | 452 | 452", "455", "452", "452")
g08 = S(D["F2008"], "Sales — gold, net | 5,447 | 4,305 | 4,211", "5,447", "4,305", "4,211")
pt08 = S(D["F2008"], "Income (loss) from continuing operations before income tax, minority interest and equity (loss) income of "
         "affiliates | 1,276 | (352) | 1,250", "1,276", "(352)", "1,250")
tx08 = S(D["F2008"], "Income tax expense (Note 8) | (113) | (200) | (326)", "(113)", "(200)", "(326)")
ca08 = S(D["F2008"], "Cash and cash equivalents | 435 | 1,231", "435", "1,231")
oz08 = S(D["F2008"], "Consolidated gold ounces sold (thousands)(1) | 6,255 | 6,184 | 7,186", "6,255", "6,184", "7,186")
cs08 = S(D["F2008"], "Costs applicable to sales(3) Gold (per ounce) | 440 | 389 | 288", "440", "389", "288")
cfq08 = quote(D["F2008"], "Net cash provided from continuing operations was $1,403, $525 and $1,129 for 2008, 2007 and 2006, respectively")
cxq08 = quote(D["F2008"], "Additions to property, plant and mine development were $1,875, $1,672 and $1,537 for continuing operations in "
              "2008, 2007 and 2006, respectively.")
EXCL07_8 = EXCL07.replace("(FY2007 10-K)", "(FY2008 10-K)")
V.append({**{k: V[0][k] for k in ("company", "exchange", "business_line", "pe_window_start", "margin_signal_name", "kind")},
    "published": SOURCES[F2008]["published"], "sources": [F2008, F2007, F2006, R2006, F2005A, F2004], "fy_label": "FY08",
    "eps_normalized": {"2002": e0603[4], "2003": e07[4], "2004": e08[4], "2005": e08[3], "2006": e08[2], "2008": e08[0]},
    "eps_sources": {"2002": F2006, "2003": F2007, **{y: F2008 for y in ("2004", "2005", "2006", "2008")}},
    "eps_excluded": {"2007": EXCL07_8}, "eps_first_excluded": V[0]["eps_first_excluded"],
    "revenue_usd_b": {"2002": r0603[4] / 1000, "2003": r07[4] / 1000, "2004": r08[4] / 1000, "2005": r08[3] / 1000, "2006": r08[2] / 1000,
                      "2007": r08[1] / 1000, "2008": r08[0] / 1000},
    "revenue_sources": {"2002": F2006, "2003": F2007, **{y: F2008 for y in ("2004", "2005", "2006", "2007", "2008")}},
    "diluted_shares_m": {"2002": round(sh02[2] / 1000, 3), "2003": sh03[2], "2004": sh06[2], "2005": sh07[2], "2006": sh08[2],
                         "2007": sh08[1], "2008": sh08[0]},
    "shares_sources": {"2002": F2004, "2003": F2005A, "2004": R2006, "2005": F2007, "2006": F2008, "2007": F2008, "2008": F2008},
    "normalization": NORM + "; 2004-2008 from the FY2008 10-K, 2003 from the FY2007 10-K, 2002 from the FY2006 10-K (seams, as "
                     "published); FY2008 at GAAP $1.82: the Q4 2008 release's adjusted net income ($1.99) also removes items that recur "
                     "in every period it tabulates ('Legacy closure obligations', write-downs of marketable securities), so GAAP stands "
                     "(the PEP 2008 core rule)",
    "prev_fy_margin": round(pt08[0] / r08[0] * 100, 2), "prev_fy_margin_note": "FY08 income from continuing operations before income tax, "
    f"minority interest and equity income ${pt08[0]:,.0f}M / revenues ${r08[0]:,.0f}M (FY2008 10-K)",
    "tax_rate": round(-tx08[0] / pt08[0], 4), "tax_note": f"FY08 income tax expense ${-tx08[0]:,.0f}M / pre-tax ${pt08[0]:,.0f}M (FY2008 10-K)",
    "prev_fy_sales_growth": pct1(r08[1], r08[0]),
    "prev_fy_oz_k": oz08[0], "prev_fy_oz_pct": pct1(oz08[1], oz08[0]), "prev_fy_cas": cs08[0],
    "prev_fy_cas_pct": pct1(cs08[1], cs08[0]), "franchise_source": "FY2008 10-K",
    "dividend_annual": 0.40, "dividend_note": DIV_NOTE + ": FY2008 10-K",
    "cash_b": ca08[0] / 1000, "fcf_b": round((1403 - 1875) / 1000, 3), "fcf_label": "FY08",
    "fcf_note": "net cash provided from continuing operations $1,403M less additions to property, plant and mine development $1,875M "
                "(FY2008 10-K: '" + cfq08 + "'; '" + cxq08 + "')",
    "cash_return_text": "dividend $0.10 a quarter; no repurchase program in the FY2008 10-K",
    "groups": [["Gold", g08[0] / 1000, pct1(g08[1], g08[0])], ["Copper", round((r08[0] - g08[0]) / 1000, 3),
                                                                     pct1(r08[1] - g08[1], r08[0] - g08[0])]],
    "groups_basis": "FY08 sales by metal, net (FY2008 10-K; copper as revenues less gold)",
    "why": why("F2008", "Newmont is one of the world’s largest gold producers and is the only gold company included in the S&P 500 Index "
                        "and Fortune 500, and was the first gold company included in the Dow Jones Sustainability Index-World."),
})

# the 8-K of 2009-09-15 recasting the FY2008 10-K (FSP APB 14-1, FAS 160, Kori Kollo discontinued): a vintage of its own (the MU and
# MSFT recast rule); 2004-2008 from it
quote(path("0000950123-09-043136", "8-K__*.rows.txt"), "However, it is also required to be applied retrospectively to all periods presented.")
e09 = S(D["R2008"], "Diluted: Continuing operations | 1.80 | (2.18) | 1.19 | 0.60 | 0.94", "1.80", "(2.18)", "1.19", "0.60", "0.94")
r09 = S(D["R2008"], "Revenues | 6,124 | 5,465 | 4,805 | 4,221 | 4,212", "6,124", "5,465", "4,805", "4,221", "4,212")
sh09 = S(D["R2008"], "Diluted weighted-average common shares outstanding | 455 | 452 | 452", "455", "452", "452")
g09 = S(D["R2008"], "Sales — gold, net | 5,372 | 4,244 | 4,134", "5,372", "4,244", "4,134")
pt09 = S(D["R2008"], "Income (loss) from continuing operations before income tax expense and other items | 1,252 | (389) | 1,212",
         "1,252", "(389)", "1,212")
tx09 = S(D["R2008"], "Income tax expense (Note 8) | (100) | (190) | (314)", "(100)", "(190)", "(314)")
ca09 = S(D["R2008"], "Cash and cash equivalents | 435 | 1,230", "435", "1,230")
oz09 = S(D["R2008"], "Consolidated gold ounces sold (thousands)(1) | 6,170 | 6,097 | 7,057", "6,170", "6,097", "7,057")
cs09 = S(D["R2008"], "Costs applicable to sales(3) Gold (per ounce) | 436 | 390 | 290", "436", "390", "290")
cfq09 = quote(D["R2008"], "Net cash provided from continuing operations was $1,397, $528 and $1,099 for 2008, 2007 and 2006, respectively")
cxq09 = quote(D["R2008"], "Additions to property, plant and mine development were $1,870, $1,669 and $1,536 for continuing operations in "
              "2008, 2007 and 2006, respectively.")
V.append({**{k: V[2][k] for k in ("company", "exchange", "business_line", "pe_window_start", "margin_signal_name", "kind", "why",
                                   "dividend_annual", "cash_return_text")},
    "published": SOURCES[R2008]["published"], "sources": [R2008, F2007, F2006, R2006, F2005A, F2004], "fy_label": "FY08",
    "eps_normalized": {"2002": e0603[4], "2003": e07[4], "2004": e09[4], "2005": e09[3], "2006": e09[2], "2008": e09[0]},
    "eps_sources": {"2002": F2006, "2003": F2007, **{y: R2008 for y in ("2004", "2005", "2006", "2008")}},
    "eps_excluded": {"2007": EXCL07.replace("$(2.13) a diluted share from continuing operations (FY2007 10-K)",
                                            "$(2.18) a diluted share from continuing operations (the 8-K of 2009-09-15)")},
    "eps_first_excluded": V[0]["eps_first_excluded"],
    "revenue_usd_b": {"2002": r0603[4] / 1000, "2003": r07[4] / 1000, "2004": r09[4] / 1000, "2005": r09[3] / 1000, "2006": r09[2] / 1000,
                      "2007": r09[1] / 1000, "2008": r09[0] / 1000},
    "revenue_sources": {"2002": F2006, "2003": F2007, **{y: R2008 for y in ("2004", "2005", "2006", "2007", "2008")}},
    "diluted_shares_m": {"2002": round(sh02[2] / 1000, 3), "2003": sh03[2], "2004": sh06[2], "2005": sh07[2], "2006": sh09[2],
                         "2007": sh09[1], "2008": sh09[0]},
    "shares_sources": {"2002": F2004, "2003": F2005A, "2004": R2006, "2005": F2007, "2006": R2008, "2007": R2008, "2008": R2008},
    "normalization": NORM + "; 2004-2008 as the 8-K of 2009-09-15 recasts them (FSP APB 14-1 and FAS 160 applied retrospectively, Kori "
                     "Kollo discontinued; EPS attributable to Newmont stockholders), 2003 from the FY2007 10-K, 2002 from the FY2006 10-K "
                     "(seams, as published); FY2008 at GAAP (the adjusted figure also removes recurring items, the PEP 2008 core rule)",
    "prev_fy_margin": round(pt09[0] / r09[0] * 100, 2), "prev_fy_margin_note": "FY08 income from continuing operations before income tax "
    f"expense and other items ${pt09[0]:,.0f}M / revenues ${r09[0]:,.0f}M (8-K of 2009-09-15)",
    "tax_rate": round(-tx09[0] / pt09[0], 4), "tax_note": f"FY08 income tax expense ${-tx09[0]:,.0f}M / pre-tax ${pt09[0]:,.0f}M (8-K of 2009-09-15)",
    "prev_fy_sales_growth": pct1(r09[1], r09[0]),
    "prev_fy_oz_k": oz09[0], "prev_fy_oz_pct": pct1(oz09[1], oz09[0]), "prev_fy_cas": cs09[0],
    "prev_fy_cas_pct": pct1(cs09[1], cs09[0]), "franchise_source": "8-K of 2009-09-15",
    "dividend_note": DIV_NOTE + ": FY2008 10-K",
    "cash_b": ca09[0] / 1000, "fcf_b": round((1397 - 1870) / 1000, 3), "fcf_label": "FY08",
    "fcf_note": "net cash provided from continuing operations $1,397M less additions to property, plant and mine development $1,870M "
                "(8-K of 2009-09-15: '" + cfq09 + "'; '" + cxq09 + "')",
    "groups": [["Gold", g09[0] / 1000, pct1(g09[1], g09[0])], ["Copper", round((r09[0] - g09[0]) / 1000, 3),
                                                                     pct1(r09[1] - g09[1], r09[0] - g09[0])]],
    "groups_basis": "FY08 sales by metal, net (8-K of 2009-09-15; copper as revenues less gold)",
})

# EPS rule T on the history of the vintage public on 2008-01-04 (the FY2006 recast): changes between consecutive years in it
h0 = V[0]["eps_normalized"]
for y in range(2003, 2007):
    a, b = h0[str(y - 1)], h0[str(y)]
    RT["eps"]["raw"][str(y)] = {"source": R2006 if y >= 2005 else F2006, "eps": [a, b]}
    RT["eps"]["values"][str(y)] = pct(a, b)

# ── the quarterly prints: the earnings releases (8-K exhibit 99.1), each figure against the year-ago quarter as the release shows it ──
PR = []
NEXT = {1: "Q2 print (late July)", 2: "Q3 print (late October)", 3: "Q4 and full-year print with the 10-K (February)",
        4: "Q1 print (late April)"}


def prt(sid, acc, pat, quarter, fy, q, release, spec, adj=None, outlook_note=None):
    p = path(acc, pat)
    day, when = pub(acc)
    SOURCES[sid] = {"published": day, "filed": when, "title": f"Newmont {quarter} results (8-K exhibit 99.1)",
                    "url": f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc.replace('-', '')}/{acc}.txt",
                    "supports": f"{quarter}: revenues, consolidated gold ounces sold, costs applicable to sales per ounce, pre-tax income, "
                                "diluted EPS from continuing operations, cash and debt"}
    v = {k: S(p, s, *t) for k, (s, t) in spec.items()}
    rev, rev0 = v["rev"][-2], v["rev"][-1]
    pt, pt0 = v["pt"]
    oz, oz0 = v["oz"][-2], v["oz"][-1]
    cas, cas0 = v["cas"]
    e, e0 = v["eps"]
    m, m0 = pt / rev * 100, pt0 / rev0 * 100
    g = lambda a, b: round((b / a - 1) * 100 + 0.0, 1) if a > 0 else round((b - a) / abs(a) * 100 + 0.0, 1)
    d = {"quarter": quarter, "fy": fy, "q": q, "published": day, "release": release,
         "release_time": when, "source": sid,
         "raw": {"rev_m": rev, "rev_prior_m": rev0, "pretax_m": pt, "pretax_prior_m": pt0, "oz_k": oz, "oz_prior_k": oz0,
                 "cas": cas, "cas_prior": cas0},
         "rows": {k: s for k, (s, t) in spec.items()},
         "sales_b": round(rev / 1000, 3), "sales_pct": pct1(rev0, rev), "oz_pct": pct1(oz0, oz),
         "cas_pct": pct1(cas0, cas), "pretax_margin": round(m + 0.0, 2), "pretax_margin_prior": round(m0 + 0.0, 2),
         "margin_bp": round((m - m0) * 100 + 0.0, 1), "eps_q": e, "eps_q_prior": e0, "eps_pct": g(e0, e),
         "diluted_shares_m": v["sh"][0], "cash_b": round(v["cash"][0] / 1000, 3),
         "debt_note": f"debt ${v['ltd'][0] + v['cur'][0]:,.0f}M (long-term ${v['ltd'][0]:,.0f}M and current portion ${v['cur'][0]:,.0f}M)",
         "rev_note": f"revenues ${rev:,.0f}M vs ${rev0:,.0f}M a year earlier",
         "oz_note": f"consolidated gold ounces sold {oz:,.0f}K vs {oz0:,.0f}K",
         "cas_note": f"costs applicable to sales ${cas:,.0f} an ounce of gold vs ${cas0:,.0f}",
         "eps_note": None,
         "adj_note": adj, "next_print": NEXT[q]}
    fmt = lambda x: f"${x:.2f}" if x >= 0 else f"$({-x:.2f})"
    d["eps_note"] = f"GAAP diluted EPS from continuing operations {fmt(e)} vs {fmt(e0)}" + (
        "; growth over the year-ago loss's absolute value (the CAT rule)" if e0 < 0 else "")
    if adj:
        d["adj_note"] = quote(p, adj) if not adj.startswith("(") else adj
    if outlook_note:
        d["outlook_note"] = outlook_note
    PR.append(d)


SP_ = lambda s, *t: (s, t)
prt("NM16", "0001144204-07-039821", "EX-99.1__*.rows.txt", "Q2 2007", 2007, 2, "Aug 2", {
    "rev": SP_("Sales - copper, net | 340 | 202 | 553 | 339 1,302 | 1,293 | 2,558 | 2,425", "1,302", "1,293"),
    "pt": SP_("(Loss) income from continuing operations before income tax, minority interest and equity income of affiliates | (331) | "
              "377 | (195) | 702", "(331)", "377"),
    "eps": SP_("Diluted: (Loss) income from continuing operations | (0.90) | 0.29 | (0.82) | 0.71", "(0.90)", "0.29"),
    "sh": SP_("Diluted weighted-average common shares outstanding | 454 | 452 | 453 | 451", "454"),
    "oz": SP_("Consolidated gold sales (000 ounces) (1) | 1,448 | 1,843 | 3,053 | 3,652", "1,448", "1,843"),
    "cas": SP_("Costs applicable to sales ($/ounce) | 433 | 299 | 427 | 287", "433", "299"),
    "cash": SP_("Cash and cash equivalents | 668 | 1,166", "668"), "cur": SP_("Current portion of long-term debt | 161 | 159", "161"),
    "ltd": SP_("Long-term debt | 2,493 | 1,752", "2,493")})
prt("NM17", "0001144204-07-057272", "EX-99.1__*.rows.txt", "Q3 2007", 2007, 3, "Oct 31", {
    "rev": SP_("Sales- copper, net | 547 | 93 | 1,100 | 432 1,646 | 1,102 | 4,204 | 3,527", "1,646", "1,102"),
    "pt": SP_("Income from continuing operations before income tax, minority interest and equity income (loss) of affiliates | 607 | 199 "
              "| 412 | 901", "607", "199"),
    "eps": SP_("Diluted: Income (loss) from continuing operations | 0.72 | 0.09 | (0.10) | 0.81", "0.72", "0.09"),
    "sh": SP_("Diluted weighted-average common shares outstanding | 453 | 452 | 453 | 451", "453"),
    "oz": SP_("Consolidated gold sales (000 ounces) (1) | 1,614 | 1,698 | 4,667 | 5,350", "1,614", "1,698"),
    "cas": SP_("Costs applicable to sales ($/ounce) (3) | 388 | 318 | 414 | 297", "388", "318"),
    "cash": SP_("Cash and cash equivalents | 1,053 | 1,166", "1,053"), "cur": SP_("Current portion of long-term debt | 288 | 159", "288"),
    "ltd": SP_("Long-term debt | 2,745 | 1,752", "2,745")})
prt("NM18", "0001144204-08-011007", "EX-99.1__*ex99-1.txt", "Q4 2007", 2007, 4, "Feb 21", {
    "rev": SP_("Sales- copper, net 121 239 1,221 671 1,410 1,424 5,526 4,882", "1,410", "1,424"),
    "pt": SP_("affiliates (785) 330 (352) 1,250", "(785)", "330"),
    "eps": SP_("Diluted: (Loss) income from continuing operations $ (2.06) $ 0.38 $ (2.13) $ 1.25", "(2.06)", "0.38"),
    "sh": SP_("Diluted weighted-average common shares outstanding 452 452 452 452", "452"),
    "oz": SP_("Consolidated gold sales (000 ounces) (1) 1,648 1,954 6,184 7,186", "1,648", "1,954"),
    "cas": SP_("Costs applicable to sales ($/ounce) ((3)) $ 384 $ 324 $ 406 $ 303", "384", "324"),
    "cash": SP_("Cash and cash equivalents $ 1,231 $ 1,166", "1,231"), "cur": SP_("Current portion of long-term debt $ 255 $ 159", "255"),
    "ltd": SP_("Long-term debt 2,683 1,752", "2,683")},
    adj="(none: the release lists after-tax items in a table and publishes no adjusted figure)")
prt("NM19", "0001144204-08-023947", "EX-99.1__*ex99-1.txt", "Q1 2008", 2008, 1, "Apr 24", {
    "rev": SP_("Sales- copper, net 432 213 1,943 1,224", "1,943", "1,224"),
    "pt": SP_("minority interest and equity loss of affiliates 796 140", "796", "140"),
    "eps": SP_("Diluted: Income from continuing operations $ 0.80 $ 0.09", "0.80", "0.09"),
    "sh": SP_("Diluted weighted-average common shares outstanding 457 452", "457"),
    "oz": SP_("Golden Giant -- 3 44 49 1,621 1,557", "1,621", "1,557"),
    "cas": SP_("Average $ 396 $ 404", "396", "404"),
    "cash": SP_("Cash and cash equivalents $ 1,014 $ 1,231", "1,014"), "cur": SP_("Current portion of long-term debt $ 261 $ 255", "261"),
    "ltd": SP_("Long-term debt 2,886 2,683", "2,886")},
    adj="resulting in Adjusted Net income(1) of approximately $386 million ($0.85 per share)")
prt("NM20", "0001144204-08-041572", "EX-99.1__*ex99-1.txt", "Q2 2008", 2008, 2, "Jul 24", {
    "rev": SP_("Sales - copper, net 183 340 615 553 1,522 1,276 3,465 2,500", "1,522", "1,276"),
    "pt": SP_("of affiliates 310 (322) 1,106 (182)", "310", "(322)"),
    "eps": SP_("Diluted: Income (loss) from continuing operations $ 0.61 $ (0.89) $ 1.41 $ (0.80)", "0.61", "(0.89)"),
    "sh": SP_("Diluted weighted-average common shares outstanding 456 451 457 451", "456"),
    "oz": SP_("Golden Giant -- 9 -- 12 46 54 90 103 1,504 1,408 3,125 2,965", "1,504", "1,408"),
    "cas": SP_("Average $ 440 $ 417 $ 417 $ 410", "440", "417"),
    "cash": SP_("Cash and cash equivalents $ 1,036 $ 1,231", "1,036"), "cur": SP_("Current portion of long-term debt $ 261 $ 255", "261"),
    "ltd": SP_("Long-term debt 3,085 2,683", "3,085")},
    adj="NEWMONT'S SECOND QUARTER ADJUSTED NET INCOME(1) RISES TO $230 MILLION ($0.51 PER SHARE)")
prt("NM21", "0001144204-08-059873", "EX-99.1__*.rows.txt", "Q3 2008", 2008, 3, "Oct 29", {
    "rev": SP_("Sales - copper, net | 90 | 547 | 705 | 1,100 1,392 | 1,616 | 4,857 | 4,116", "1,392", "1,616"),
    "pt": SP_("Income from continuing operations before income tax, minority interest and equity loss of affiliates | 212 | 615 | 1,318 "
              "| 433", "212", "615"),
    "eps": SP_("Diluted: Income (loss) from continuing operations | 0.39 | 0.73 | 1.80 | (0.07)", "0.39", "0.73"),
    "sh": SP_("Diluted weighted-average common shares outstanding | 455 | 453 | 456 | 451", "455"),
    "oz": SP_("45 | 39 | 135 | 142 1,508 | 1,570 | 4,633 | 4,536", "1,508", "1,570"),
    "cas": SP_("Average | 480 | 374 | 438 | 398", "480", "374"),
    "cash": SP_("Cash and cash equivalents | 854 | 1,231", "854"), "cur": SP_("Current portion of long-term debt | 142 | 255", "142"),
    "ltd": SP_("Long-term debt | 3,355 | 2,683", "3,355")})
prt("NM22", "0001144204-09-009779", "EX-99.1__*.rows.txt", "Q4 2008", 2008, 4, "Feb 19", {
    "rev": SP_("Sales - copper, net | 47 | 121 | 752 | 1,221 1,342 | 1,410 | 6,199 | 5,526", "1,342", "1,410"),
    "pt": SP_("(Loss) income from continuing operations before income tax,minority interest and equity income (loss) of affiliates | "
              "(42) | (785) | 1,276 | (352)", "(42)", "(785)"),
    "eps": SP_("Diluted: Income (loss) from continuing operations | 0.02 | (2.06) | 1.82 | (2.13)", "0.02", "(2.06)"),
    "sh": SP_("Diluted weighted-average common shares outstanding | 455 | 452 | 455 | 452", "455"),
    "oz": SP_("45 | 43 | 180 | 185 1,622 | 1,648 | 6,255 | 6,184", "1,622", "1,648"),
    "cas": SP_("Average | 448 | 366 | 440 | 389", "448", "366"),
    "cash": SP_("Cash and cash equivalents | 435 | 1,231", "435"), "cur": SP_("Current portion of long-term debt | 169 | 255", "169"),
    "ltd": SP_("Long-term debt | 3,373 | 2,683", "3,373")},
    adj="50% increase in adjusted net income(1) at $905 million ($1.99 per share)")
prt("NM23", "0001144204-09-023022", "EX-99.1__*.rows.txt", "Q1 2009", 2009, 1, "Apr 30", {
    "rev": SP_("Sales - copper, net | 161 | 432 1,552 | 1,943", "1,552", "1,943"),
    "pt": SP_("Income from continuing operations before income tax expense and other items | 387 | 788", "387", "788"),
    "eps": SP_("Diluted: Continuing operations | 0.40 | 0.79", "0.40", "0.79"),
    "sh": SP_("Diluted weighted-average common shares outstanding | 473 | 457", "473"),
    "oz": SP_("Ahafo | 144 | 105 1,534 | 1,621", "1,534", "1,621"),
    "cas": SP_("Average | 435 | 396", "435", "396"),
    "cash": SP_("Cash and cash equivalents | 1,451 | 435", "1,451"), "cur": SP_("Current portion of long-term debt | 223 | 169", "223"),
    "ltd": SP_("Long-term debt | 2,749 | 3,072", "2,749")})
prt("NM24", "0001144204-09-038371", "EX-99.1__*.rows.txt", "Q2 2009", 2009, 2, "Jul 23", {
    "rev": SP_("Sales - copper, net | 229 | 183 | 390 | 615 1,602 | 1,503 | 3,138 | 3,428", "1,602", "1,503"),
    "pt": SP_("Income from continuing operations before income tax (expense) benefit and other items | 459 | 295 | 846 | 1,078", "459", "295"),
    "eps": SP_("Diluted: Continuing operations | 0.35 | 0.59 | 0.75 | 1.37", "0.35", "0.59"),
    "sh": SP_("Diluted weighted-average common shares outstanding | 491 | 456 | 484 | 457", "491"),
    "oz": SP_("Ahafo (2) | 132 | 134 | 276 | 239 1,502 | 1,483 | 3,019 | 3,084", "1,502", "1,483"),
    "cas": SP_("Average | 423 | 439 | 427 | 416", "423", "439"),
    "cash": SP_("Cash and cash equivalents | 544 | 435", "544"), "cur": SP_("Current portion of long-term debt | 221 | 165", "221"),
    "ltd": SP_("Long-term debt | 2,810 | 3,072", "2,810")})
prt("NM25", "0001144204-09-055214", "EX-99.1__*.rows.txt", "Q3 2009", 2009, 3, "Oct 29", {
    "rev": SP_("Sales - copper, net | 396 | 90 | 786 | 705 2,049 | 1,371 | 5,187 | 4,799", "2,049", "1,371"),
    "pt": SP_("Income from continuing operations before income tax and other items | 904 | 222 | 1,750 | 1,300", "904", "222"),
    "eps": SP_("Diluted: Continuing operations | 0.79 | 0.40 | 1.54 | 1.77", "0.79", "0.40"),
    "sh": SP_("Diluted weighted-average common shares outstanding | 491 | 455 | 486 | 456", "491"),
    "oz": SP_("Ahafo (2) | 136 | 141 | 412 | 380 1,715 | 1,485 | 4,734 | 4,569", "1,715", "1,485"),
    "cas": SP_("Average | 404 | 467 | 419 | 433", "404", "467"),
    "cash": SP_("Cash and cash equivalents | 3,022 | 435", "3,022"), "cur": SP_("Current portion of long-term debt | 225 | 165", "225"),
    "ltd": SP_("Long-term debt | 4,698 | 3,072", "4,698")})
for p in PR:
    p["release_time"] = SOURCES[p["source"]]["filed"]

# ── outlooks: equity gold sales and costs applicable to sales per ounce (volumes and unit costs) and the cost components of the Q4
# 2007 table; method r2 has no volume input and none for cost components (the XOM production and MSFT segment rules): display only ──
UNUSED = ("a volume and unit-cost outlook: method r2 has no input for a production guide (the XOM rule) or for cost components (the MSFT "
          "segment rule), so no field; no filing guides revenue, EPS or a margin")
G = []


def guide(fy, sid, acc, pat, title, s, unused=UNUSED):
    day, when = pub(acc)
    if sid not in SOURCES:
        SOURCES[sid] = {"published": day, "filed": when, "title": title,
                        "url": f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc.replace('-', '')}/{acc}.txt",
                        "supports": "a display-only outlook (guide line)"}
    G.append({"fy": fy, "published": day, "source": sid, "doc": title, "display": quote(path(acc, pat), s), "unused": unused})


RX = "EX-99.1__*.rows.txt"
guide(2007, "NM16", "0001144204-07-039821", RX, "Q2 2007 release", "we continue to expect gold sales of between 5.2 and 5.6 million "
      "equity ounces at costs applicable to sales of between $375 and $400 an ounce for the year.")
guide(2007, "NM17", "0001144204-07-057272", RX, "Q3 2007 release", "we are narrowing our outlook for equity gold sales to between 5.2 and "
      "5.4 million ounces at costs applicable to sales of between $400 and $430 per ounce for 2007.")
guide(2008, "NM26", "0001144204-08-006646", "EX-99.1__*ex99-1.txt", "8-K of 2008-02-07 (2007 operating and reserve results, 2008 outlook)",
      "We expect our 2008 gold sales performance to be comparable with our 2007 results, with equity gold sales expected to be between "
      "5.1 and 5.4 million ounces at costs applicable to sales of between $425 and $450 per ounce.")
guide(2008, "NM18", "0001144204-08-011007", "EX-99.1__*ex99-1.txt", "Q4 2007 release (2008 financial outlook)",
      "Depreciation, depletion & amortization $725 - $775 Exploration $220 - $230 Advanced projects, research and development "
      "$120 - $180 General and administrative $140 - $150 Interest expense, net $110 - $120 Effective tax rate 30% - 34%",
      "cost components and a tax rate (the MSFT segment rule): no field; the equity gold sales outlook of the 8-K of 2008-02-07 stands "
      "in words only; no filing guides revenue, EPS or a margin")
guide(2008, "NM19", "0001144204-08-023947", "EX-99.1__*ex99-1.txt", "Q1 2008 release", "The Company's 2008 annual equity gold sales "
      "guidance remains unchanged between 5.1 and 5.4 million ounces at costs applicable to sales of between $425 and $450 per ounce.")
guide(2008, "NM20", "0001144204-08-041572", "EX-99.1__*ex99-1.txt", "Q2 2008 release", "The Company is maintaining its initial 2008 annual "
      "equity gold sales guidance at between 5.1 and 5.4 million ounces and its initial costs applicable to sales guidance of between "
      "$425 and $450 per ounce.")
guide(2008, "NM21", "0001144204-08-059873", RX, "Q3 2008 release", "The Company is maintaining its initial 2008 annual equity gold sales "
      "guidance at between 5.1 and 5.4 million ounces")
guide(2009, "NM27", "0001144204-09-003674", RX, "8-K of 2009-01-27 (2008 operating results, 2009 outlook)", "The Company expects higher "
      "equity gold sales of between 5.2 and 5.5 million ounces at lower costs applicable to sales of between $400 and $440 per ounce in 2009.")
guide(2009, "NM22", "0001144204-09-009779", RX, "Q4 2008 release", "Equity gold sales in 2009 are expected to increase to between 5.2 and "
      "5.5 million ounces at lower costs applicable to sales of between $400 and $440 per ounce")
guide(2009, "NM23", "0001144204-09-023022", RX, "Q1 2009 release", "The Company is maintaining its previously announced 2009 equity gold "
      "sales outlook of between 5.2 and 5.5 million ounces at costs applicable to sales of between $400 and $440 per ounce")
guide(2009, "NM24", "0001144204-09-038371", RX, "Q2 2009 release", "With a revised 2009 equity gold sales outlook of 5.2 to 5.4 million "
      "ounces, the Company’s outlook for 2009 costs applicable to sales remains unchanged at between $400 and $440 per ounce.")
guide(2009, "NM25", "0001144204-09-055214", RX, "Q3 2009 release", "the Company estimates its outlook for 2009 equity gold sales to be "
      "approximately 5.2 million ounces, at the lower end of its previously estimated range.")

# ── the listing (display): NYSE: NEM on every date ──
LST = [{"symbol": "NEM", "exchange": "NYSE", "published": SOURCES[F2006]["published"], "effective": "2002-02-13", "source": F2006,
        "note": quote(D["F2006"], "Newmont’s common stock is listed and principally traded on the New York Stock Exchange (under the "
                                  "symbol “NEM”)")}]


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
for p in PR:
    p["source_title"] = SOURCES[p["source"]]["title"]
facts = {
    "_doc": "Point-in-time fact sheet for NEM retrospectives (retro/build_nem.py): Newmont Mining Corporation (NYSE: NEM). Generated by "
            "retro/generators/nem/gen_nem.py from the filings; every value carries a source and its publication date (the acceptance-time "
            "rule). Read retro/README.md, 'NEM', before editing.",
    "ticker": "NEM", "sources": dict(sorted(SOURCES.items(), key=lambda kv: int(kv[0][2:]))), "history_vintages": V, "prints": PR,
    "guides": G, "eps_guides": [], "dividends": [], "events": [], "company_names": [], "splits": [], "listings": LST,
    "distributions": [], "rule_t": RT,
    "price_basis": "Yahoo NEM: no split since 1994, so the close is the price as traded on every date from the P/E window's start "
                   "(2002-01-01)",
}
assert all(s["published"] <= CUT for s in SOURCES.values())
out = A.out or os.path.join(REPO, "retro", "facts", "NEM.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(facts, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_nem.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump({k: v for k, v in CHECK.items() if v}, fh, ensure_ascii=False, indent=1)
print(f"{out}: {len(V)} vintages, {len(PR)} prints, {len(G)} guides, {len(SOURCES)} sources; "
      f"{sum(len(v) for v in CHECK.values())} quotes in {ck}")
for k in RT:
    print(k, RT[k]["values"], RT[k]["thresholds"])
