#!/usr/bin/env python3
"""Generate retro/facts/SCHW.json (2008-2009) from The Charles Schwab Corporation's own filings (edgar.py's converted rows).

Every raw figure is read from its own row by label (the row is kept), every rate is computed, every quoted sentence is
asserted present in its own filing, and a verbatim checklist is written for retro/tools/verbatim.py. Only filings accepted
on or before 2009-12-31 are read. Run (the downloads: edgar.py index 316709 <dir>; edgar.py fetch 316709 <dir> --from 2001-01-01 --to 2013-12-31 --forms 10-K 10-K/A;
edgar.py fetch 316709 <dir> --from 2006-10-01 --to 2013-12-31 --forms 8-K 8-K/A 10-Q 10-Q/A):

    python3 -I retro/generators/schw/gen_schw.py --filings <dir> [--out retro/facts/SCHW.json] [--checklist <dir>/checklist_schw.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_schw.json
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
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))       # retro/generators/schw -> the repository
_ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("--filings", required=True, help="folder edgar.py wrote (allrows.json, tenk/, tenq/, eightk/); keep it outside the repo")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/SCHW.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_schw.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402  (the repo's own tool: trading days from the Yahoo cache)

ET = ZoneInfo("America/New_York")
CUT = "2009-12-31"
FILINGS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("SCHW")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
CHECK = {}          # verbatim checklist: file -> strings


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def doc(acc, name):
    d = os.path.join(SP, "tenk" if os.path.isdir(os.path.join(SP, "tenk", acc)) else
                     "tenq" if os.path.isdir(os.path.join(SP, "tenq", acc)) else "eightk", acc)
    p = os.path.join(d, name)
    assert os.path.exists(p), p
    return p


TEXT = {}


def lines(path):
    if path not in TEXT:
        with open(path, encoding="utf-8" if path.endswith(".rows.txt") else "latin-1", errors="replace") as fh:
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
    if t in ("—", "-", "–", ""):
        return 0.0
    neg = t.startswith("(") and t.endswith(")")
    t = t.strip("()%")
    v = float(t)
    return -v if neg else v


def row(path, label, start=0, stop=None, n=None, text=False):
    """The unique row in lines[start:stop] that starts with `label` (after whitespace collapse); returns (row, values) where
    values are the last n numeric cells (rows files split by '|', text files by whitespace with '$' dropped)."""
    L = lines(path)[start:stop]
    hits = [x for x in L if x.startswith(label) and (not text or re.match(r"[\s$]*[\d(.—-]", x[len(label):]))]
    assert len(hits) == 1, (path, label, len(hits), hits[:3])
    r = hits[0]
    if text:
        rest = r[len(label):].replace("$", " ")
        toks = [t for t in rest.split() if re.fullmatch(r"\(?[\d,]*\.?\d+\)?%?|—|-", t)]
    else:
        toks = [t.strip() for t in r.split("|")[1:]]
    def safe(t):
        try:
            return num(t)
        except ValueError:
            return None
    vals = [safe(t) for t in toks]
    out = vals[-n:] if n else vals
    assert None not in out, (path, label, r)
    CHECK.setdefault(path, []).append(r)
    return r, out


def sel_bounds(path):
    """(start, stop) of a 10-K's selected financial data table: its title to the next 'Item 7.' line."""
    i0 = line_no(path, "Selected Financial and Operating Data")
    i1 = min(i for i, x in enumerate(lines(path)) if i > i0 and x.startswith("Item 7. |"))
    return i0, i1


def overview_bounds(path):
    """(start, stop) of the MD&A overview's client activity table: the 'Item 7.' line to the first metric bullet."""
    i0 = sel_bounds(path)[1]
    i1 = min(i for i, x in enumerate(lines(path)) if i > i0 and x.startswith("• | Net new client assets"))
    return i0, i1


def line_no(path, startswith, nth=0):
    idx = [i for i, x in enumerate(lines(path)) if x.startswith(startswith)]
    return idx[nth]


def next_tday(d):
    return min(x for x in TDAYS if x > d)


def published(acc):
    """Publication date from EDGAR's acceptance time (UTC -> ET); after the 16:00 ET close, the next trading day."""
    r = FILINGS[acc]
    t = dt.datetime.fromisoformat(r[1].replace("Z", "+00:00")).astimezone(ET)
    d = t.date().isoformat()
    assert d <= CUT, acc
    if r[1].endswith("T05:00:00.000Z") or r[1].endswith("T04:00:00.000Z"):     # EDGAR gives the date only
        return d, f"accepted {d} (EDGAR gives the date only; treated as before the open)"
    hm = t.strftime("%H:%M")
    if hm >= "16:00":
        return next_tday(d), f"accepted {d} {hm} ET (after the close), so dated the next trading day"
    if hm < "09:30":
        return d, f"accepted {d} {hm} ET (before the open)"
    return d, f"accepted {d} {hm} ET (during market hours)"


URL = lambda acc, fn: f"https://www.sec.gov/Archives/edgar/data/316709/{acc.replace('-', '')}/{fn}"
SRC = {}


def source(i, acc, title, fn, supports):
    p, filed = published(acc)
    SRC[f"SCHW{i}"] = dict(published=p, filed=filed, title=title, url=URL(acc, fn), supports=supports)
    return f"SCHW{i}"


# ── filings ─────────────────────────────────────────────────────────────────────
K00, K01, K02, K03, K04, K05 = ("0000316709-01-000010", "0000316709-02-000008", "0000316709-03-000009", "0000316709-04-000006",
                                "0000316709-05-000006", "0001193125-06-039674")
K06, K07, K08 = "0001193125-07-039782", "0001193125-08-039024", "0001193125-09-037420"
Q306_10Q, Q208_10Q = "0001193125-06-224755", "0001193125-08-169989"
REL = {"Q4 2006": "0001193125-07-007667", "Q1 2007": "0001193125-07-082863", "Q2 2007": "0001193125-07-156354",
       "Q3 2007": "0001193125-07-218478", "Q4 2007": "0001193125-08-007343", "Q1 2008": "0001193125-08-081657",
       "Q2 2008": "0001193125-08-152020", "Q3 2008": "0001193125-08-210863", "Q4 2008": "0001193125-09-007447",
       "Q1 2009": "0001193125-09-079519", "Q2 2009": "0001193125-09-150031", "Q3 2009": "0001193125-09-208410"}
TENQ = {"Q1 2007": "0001193125-07-105767", "Q2 2007": "0001193125-07-173544", "Q3 2007": "0001193125-07-238225",
        "Q1 2008": "0001193125-08-107521", "Q2 2008": "0001193125-08-169989", "Q3 2008": "0001193125-08-227611",
        "Q1 2009": "0001193125-09-103594", "Q2 2009": "0001193125-09-167020", "Q3 2009": "0001193125-09-224395"}
F00 = doc(K00, "EX-13.1__0005.txt")
F01 = doc(K01, "EX-13.1__exh13_1.txt")
F02 = doc(K02, "EX-13__exh13_1.txt")
F03 = doc(K03, "EX-13__exh13_1.txt")
F04 = doc(K04, "10-K__body.txt")
F05 = doc(K05, "10-K__d10k.rows.txt")
F06, F07, F08 = (doc(K06, "10-K__d10k.rows.txt"), doc(K07, "10-K__d10k.rows.txt"), doc(K08, "10-K__d10k.rows.txt"))
FREL = {q: doc(a, "EX-99.1__dex991.rows.txt") for q, a in REL.items()}

S = {}
S["K00"] = source(1, K00, "The Charles Schwab Corporation FY2000 10-K (annual report, exhibit 13.1)", "0005.txt",
                  "selected financial and operating data 1996-2000 (restated for the U.S. Trust merger): the 1996-1997 rule-T changes")
S["K01"] = source(2, K01, "The Charles Schwab Corporation FY2001 10-K (annual report, exhibit 13.1)", "exh13_1.txt",
                  "selected financial and operating data 1997-2001: the 1997-1998 rule-T changes")
S["K02"] = source(3, K02, "The Charles Schwab Corporation FY2002 10-K (annual report, exhibit 13)", "exh13_1.txt",
                  "selected financial and operating data 1998-2002 and the reconciliation of adjusted operating income: the "
                  "1998-1999 rule-T changes and the items that make FY2002 a distorted year")
S["K03"] = source(4, K03, "The Charles Schwab Corporation FY2003 10-K (annual report, exhibit 13)", "exh13_1.txt",
                  "selected financial and operating data 1999-2003: the 1999-2000 rule-T changes and the 2000-2002 trades")
S["K04"] = source(5, K04, "The Charles Schwab Corporation FY2004 10-K", "body.txt",
                  "selected financial and operating data 2000-2004 and the 2002-2004 client activity metrics: the 2000-2001 "
                  "rule-T changes and the 2002-2003 trades")
S["K05"] = source(6, K05, "The Charles Schwab Corporation FY2005 10-K", "d10k.htm",
                  "selected financial and operating data 2001-2005 and the 2003-2005 client activity metrics: the 2001-2002 "
                  "rule-T changes, the 2002-2004 client assets and the 2003-2004 trades")
S["Q306Q"] = source(7, Q306_10Q, "The Charles Schwab Corporation Q3 2006 10-Q", "d10q.htm",
                    "the quarterly dividend raised to $.05 a share (October 19, 2006)")
S["Q4 2006"] = source(8, REL["Q4 2006"], "Schwab Q4 2006 earnings release (8-K exhibit 99.1)", "dex991.htm",
                      "Q4 2006 statement of income, financial and operating highlights, client assets and trades")
S["K06"] = source(9, K06, "The Charles Schwab Corporation FY2006 10-K", "d10k.htm",
                  "selected financial and operating data 2002-2006 (continuing operations, U.S. Trust discontinued), the 2004-2006 "
                  "client activity metrics and the 2004-2006 statements of income: the FY06 history vintage; the 2002-2006 "
                  "rule-T changes; Items 1, 1A and 5")
S["Q1 2007"] = source(10, REL["Q1 2007"], "Schwab Q1 2007 earnings release (8-K exhibit 99.1)", "dex991.htm",
                      "Q1 2007 statement of income, financial and operating highlights, client assets and trades")
S["Q2 2007"] = source(11, REL["Q2 2007"], "Schwab Q2 2007 earnings release (8-K exhibit 99.1)", "dex991.htm",
                      "Q2 2007 statement of income, financial and operating highlights, client assets and trades")
S["Q3 2007"] = source(12, REL["Q3 2007"], "Schwab Q3 2007 earnings release (8-K exhibit 99.1)", "dex991.htm",
                      "Q3 2007 statement of income, financial and operating highlights, client assets and trades")
S["Q4 2007"] = source(13, REL["Q4 2007"], "Schwab Q4 2007 earnings release (8-K exhibit 99.1)", "dex991.htm",
                      "Q4 2007 and FY2007 statement of income, financial and operating highlights, client assets and trades")
S["K07"] = source(14, K07, "The Charles Schwab Corporation FY2007 10-K", "d10k.htm",
                  "selected financial and operating data 2003-2007, the 2005-2007 client activity metrics and the 2005-2007 "
                  "statements of income: the FY07 history vintage; Items 1, 1A and 5")
S["Q1 2008"] = source(15, REL["Q1 2008"], "Schwab Q1 2008 earnings release (8-K exhibit 99.1)", "dex991.htm",
                      "Q1 2008 statement of income, financial and operating highlights, client assets and trades")
S["Q2 2008"] = source(16, REL["Q2 2008"], "Schwab Q2 2008 earnings release (8-K exhibit 99.1)", "dex991.htm",
                      "Q2 2008 statement of income, financial and operating highlights, client assets and trades")
S["Q208Q"] = source(17, Q208_10Q, "The Charles Schwab Corporation Q2 2008 10-Q", "d10q.htm",
                    "the quarterly dividend raised to $.06 a share (July 22, 2008)")
S["Q3 2008"] = source(18, REL["Q3 2008"], "Schwab Q3 2008 earnings release (8-K exhibit 99.1)", "dex991.htm",
                      "Q3 2008 statement of income, financial and operating highlights, client assets and trades")
S["Q4 2008"] = source(19, REL["Q4 2008"], "Schwab Q4 2008 earnings release (8-K exhibit 99.1)", "dex991.htm",
                      "Q4 2008 and FY2008 statement of income, financial and operating highlights, client assets and trades")
S["K08"] = source(20, K08, "The Charles Schwab Corporation FY2008 10-K", "d10k.htm",
                  "selected financial and operating data 2004-2008, the 2006-2008 client activity metrics and the 2006-2008 "
                  "statements of income: the FY08 history vintage; Items 1, 1A and 5")
S["Q1 2009"] = source(21, REL["Q1 2009"], "Schwab Q1 2009 earnings release (8-K exhibit 99.1)", "dex991.htm",
                      "Q1 2009 statement of income, financial and operating highlights, client assets and trades")
S["Q2 2009"] = source(22, REL["Q2 2009"], "Schwab Q2 2009 earnings release (8-K exhibit 99.1)", "dex991.htm",
                      "Q2 2009 statement of income, financial and operating highlights, client assets and trades")
S["Q3 2009"] = source(23, REL["Q3 2009"], "Schwab Q3 2009 earnings release (8-K exhibit 99.1)", "dex991.htm",
                      "Q3 2009 statement of income, financial and operating highlights, client assets and trades")
for k, v in S.items():
    pass

r1 = lambda x: round(x + 0.0, 1)
r2 = lambda x: round(x + 0.0, 2)
pct = lambda a, b: (b / a - 1) * 100

# ── rule T over the decade of the FY2006 10-K (1997-2006), each change from the latest 10-K published by 2008-01-04 that reports
#    both years ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
SEL = {}     # (filing) -> {measure: (row, {year: value})}


def sel_text(path, years, specs):
    """Selected data of a text-format annual report: label -> values for `years` (most recent first, as printed)."""
    out = {}
    i0 = [i for i, x in enumerate(lines(path)) if x.startswith("Selected Financial and Operating Data")][-1]
    for key, label in specs.items():
        r, v = row(path, label, start=i0, stop=i0 + 110, n=len(years), text=True)
        out[key] = (r, dict(zip(years, v)))
    return out


def sel_rows(path, years, specs, start=0, stop=None):
    out = {}
    for key, label in specs.items():
        r, v = row(path, label, start=start, stop=stop, n=len(years))
        out[key] = (r, dict(zip(years, v)))
    return out


SPEC_OLD = {"revenue": "Revenues ", "expense": "Expenses excluding interest ", "client_assets": "Client assets (in billions) ",
            "dart": "Daily average revenue trades ", "margin": "Pre-tax profit margin "}
s00 = sel_text(F00, [2000, 1999, 1998, 1997, 1996], SPEC_OLD)
s01 = sel_text(F01, [2001, 2000, 1999, 1998, 1997], {**SPEC_OLD, "margin": "Pre-tax profit margin - reported "})
s02 = sel_text(F02, [2002, 2001, 2000, 1999, 1998], {**SPEC_OLD, "margin": "Pre-tax profit margin - reported "})
s03 = sel_text(F03, [2003, 2002, 2001, 2000, 1999], {**SPEC_OLD, "revenue": "Revenues (1) ",
                                                     "expense": "Expenses excluding interest (1) ",
                                                     "dart": "Daily average revenue trades (8) ",
                                                     "margin": "Pre-tax profit margin - reported "})
s04 = sel_text(F04, [2004, 2003, 2002, 2001, 2000], {"revenue": "Revenues (1) ", "expense": "Expenses excluding interest (1) ",
                                                     "client_assets": "Client assets (in billions) ", "margin": "Pre-tax profit margin (1) "})
# the FY2004 10-K's client activity metrics (2004, 2003, 2002): its trades table (two lines: label, then figures)
L04 = lines(F04)
i04 = [i for i, x in enumerate(L04) if x == "Daily average revenue trades"]
assert len(i04) == 2, i04
r04_dart = L04[i04[1] + 1]
assert r04_dart.startswith("(in thousands) (1)"), r04_dart
d04 = [num(t) for t in r04_dart.split()[-3:]]
assert d04 == [156.4, 140.8, 134.1], d04
CHECK.setdefault(F04, []).append("Daily average revenue trades " + r04_dart)
s04["dart"] = ("Daily average revenue trades " + r04_dart, dict(zip([2004, 2003, 2002], d04)))
s05 = sel_rows(F05, [2005, 2004, 2003, 2002, 2001], {"revenue": "Revenues |", "expense": "Expenses excluding interest |",
                                                     "client_assets": "Client assets (in billions) |",
                                                     "margin": "Pre-tax profit margin from continuing operations |"},
               *sel_bounds(F05))
r05d, v05d = row(F05, "Daily average revenue trades (in thousands) |", *overview_bounds(F05), n=3)
s05["dart"] = (r05d, dict(zip([2005, 2004, 2003], v05d)))
s06 = sel_rows(F06, [2006, 2005, 2004, 2003, 2002], {"revenue": "Net revenues |", "expense": "Expenses excluding interest |",
                                                     "margin": "Pre-tax profit margin from continuing operations |"}, *sel_bounds(F06))
r06c, v06c = row(F06, "Client assets (in billions, at year end) |", *overview_bounds(F06), n=3)
s06["client_assets"] = (r06c, dict(zip([2006, 2005, 2004], v06c)))
r06d, v06d = row(F06, "Daily average revenue trades (in thousands) |", *overview_bounds(F06), n=3)
s06["dart"] = (r06d, dict(zip([2006, 2005, 2004], v06d)))
SEL = {"K00": s00, "K01": s01, "K02": s02, "K03": s03, "K04": s04, "K05": s05, "K06": s06}
ORDER = ["K00", "K01", "K02", "K03", "K04", "K05", "K06"]          # by publication date, all before 2008-01-04


def latest_pair(measure, y):
    """The latest 10-K published by 2008-01-04 that reports both y-1 and y for a measure."""
    for k in reversed(ORDER):
        m = SEL[k].get(measure)
        if m and y in m[1] and y - 1 in m[1]:
            return k, m
    raise AssertionError((measure, y))


RULE_T_KEYS = {"revenue": (1, False), "client_assets": (1, False), "expense_gap": (1, True), "dart": (1, False),
               "pretax_margin": (10, False)}
MEAS = {"revenue": "net revenue growth, % ('Revenues' to the FY2004 10-K, 'Net revenues' after)",
        "client_assets": "client assets growth, %, year end against year end",
        "expense_gap": "growth of expenses excluding interest less net revenue growth, pp",
        "dart": "daily average revenue trades growth, %",
        "pretax_margin": "change in the pre-tax profit margin, bp, as each 10-K prints the margin"}
rule_t = {}
for key, (unit, lower) in RULE_T_KEYS.items():
    vals, raw = {}, {}
    for y in range(1997, 2007):
        if key == "expense_gap":
            k, m = latest_pair("revenue", y)
            k2, e = latest_pair("expense", y)
            assert k == k2, (y, k, k2)
            rv, ex = (m[1][y - 1], m[1][y]), (e[1][y - 1], e[1][y])
            raw[str(y)] = dict(source=S[k], revenue_m=list(rv), expense_m=list(ex), rows=[m[0], e[0]])
            vals[str(y)] = round(pct(*ex) - pct(*rv) + 0.0, 2)
        elif key == "pretax_margin":
            k, m = latest_pair("margin", y)
            mg = (m[1][y - 1], m[1][y])
            raw[str(y)] = dict(source=S[k], margin_pct=list(mg), rows=[m[0]])
            vals[str(y)] = round((mg[1] - mg[0]) * 100 + 0.0, 1)
        else:
            k, m = latest_pair(key, y)
            v = (m[1][y - 1], m[1][y])
            raw[str(y)] = dict(source=S[k], **{("revenue_m" if key == "revenue" else "client_assets_b" if key == "client_assets"
                                                 else "dart_k"): list(v)}, rows=[m[0]])
            vals[str(y)] = round(pct(*v) + 0.0, 2)
    v = sorted(vals.values())
    n = len(v)
    med = v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
    worst, best = (v[-1], v[0]) if lower else (v[0], v[-1])
    rr = lambda x: math.floor(x / unit + 0.5) * unit
    th = dict(zip(("BEAR", "BASE", "BULL", "XBULL"), (rr(worst + (worst - med)), rr(worst), rr(med), rr(best))))
    rule_t[key] = dict(measure=MEAS[key] + " (each pair of years from the latest 10-K published by 2008-01-04 that reports both)",
                       unit=unit, lower_is_better=lower, values=vals, thresholds=th, raw=raw)

# ── history vintages ────────────────────────────────────────────────────────────────────────────────────────────────────
ITEM1 = ("engages, through its subsidiaries (collectively referred to as the Company, and primarily located in San Francisco except "
         "as indicated), in securities brokerage, banking, and related financial services.")
DEV = "Developments in the business, economic, and geopolitical environment could negatively impact the Company’s business."
COMP06 = ("There has been aggressive price competition in the Company’s industry, which may continue in the future.")
COMP07 = "The Company’s industry is characterized by aggressive price competition."
LIST = "CSC’s common stock is listed on The Nasdaq Stock Market under the ticker symbol SCHW."
for f in (F06, F07, F08):
    quote(f, ITEM1)
    quote(f, DEV)
    quote(f, LIST)
quote(F06, COMP06)
quote(F07, COMP07)
quote(F08, COMP07)
for f in (F06, F07, F08):
    assert "cyclic" not in " ".join(lines(f)).lower(), f          # no 10-K calls the business cyclical
DUR = ("DURABLE, risk 2: the 10-K ties results to markets, rates and investor engagement and names price competition, a cycle and "
       "a competitive field, and does not call its own business cyclical (the JPM, LOW and SHW reading); no theme in "
       "taxonomy_eras.json is live for a securities broker and bank on these dates (OFFSHORE is scoped to IT services), so the "
       "watch list is empty and these words stay here (the PEP obesity rule)")
X02 = ("a distorted year (the AAPL FY2002 test): the items the FY2002 10-K excludes from adjusted operating income (restructuring "
       "charges of $373M, goodwill and other impairment charges of $61M and merger- and acquisition-related charges of $27M, less a "
       "$22M extraordinary gain: $287M after tax) exceed the year's $117M income from continuing operations as the FY2006 10-K "
       "restates it ($0.09 a share); the adjusted figure is in dollars on the earlier basis (U.S. Trust in, no per-share figure), so "
       "none excludes them on the continuing-operations basis; FY2001 ($0.05, with $208M of excluded items after tax) precedes it, "
       "and the history and the P/E window start with FY2003 (the JPM FY2002 rule)")
r02x, v02x = row(F02, "Total excluded items, after tax ", n=3, text=True)
assert v02x == [-287, -208, -131], v02x
for lab, want in (("Restructuring charges (3) ", -373), ("Goodwill and other impairment charges (5) ", -61),
                  ("Merger- and acquisition-related charges (6) ", -27), ("Extraordinary gain (1) ", 22)):
    r_, v_ = row(F02, lab, text=True, n=None)
    assert v_[0] == want, (lab, v_)


def vintage(fk, f, years, published_src, label, prev_ca, prev_nna, groups, groups_basis, extra_eps=None):
    """A 10-K's five-year selected data (most recent first) as a history vintage."""
    b = sel_bounds(f)
    re_, ve = row(f, "Income from continuing operations per share — diluted |", *b, n=5)
    rr_, vr = row(f, "Net revenues |", *b, n=5)
    rs_, vs = row(f, "Weighted-average common shares outstanding — diluted |", *b, n=5)
    eps = {str(y): v for y, v in zip(years, ve) if y >= 2003}
    rev = {str(y): round(v / 1000, 3) for y, v in zip(years, vr) if y >= 2003}
    sh = {str(y): v for y, v in zip(years, vs) if y >= 2003}
    srcs = {str(y): published_src for y in eps}
    if extra_eps:
        for y, (e, r_, s_, src) in extra_eps.items():
            eps[str(y)], rev[str(y)], sh[str(y)], srcs[str(y)] = e, r_, s_, src
    eps = dict(sorted(eps.items())); rev = dict(sorted(rev.items())); sh = dict(sorted(sh.items())); srcs = dict(sorted(srcs.items()))
    # the last year's statement of income: pre-tax income, taxes, components
    i0 = [i for i, x in enumerate(lines(f)) if x.startswith("Asset management and administration fees |") and len(x.split("|")) == 4][0]
    ri, vi = row(f, "Income from continuing operations before taxes on income |", n=3, start=i0, stop=i0 + 30)
    rt, vt = row(f, "Taxes on income |", n=3, start=i0, stop=i0 + 30)
    pre, tax = vi[0], -vt[0]
    ly = years[0]
    yr_rev = vr[0]
    m = r2(pre / yr_rev * 100)
    return dict(rows=[re_, rr_, rs_, ri, rt], eps=eps, rev=rev, sh=sh, srcs=srcs, pre=pre, tax=tax, margin=m,
                sales_growth=r1(pct(vr[1], vr[0])), ly=ly)


def income_rows(f, labels, start_label="Asset management and administration fees |"):
    """The 10-K's statement of income component rows (three years, most recent first): the first table that starts with the
    asset management line and has exactly three numbers."""
    L = lines(f)
    out = {}
    idx = [i for i, x in enumerate(L) if x.startswith(start_label) and len(x.split("|")) == 4]
    assert idx, f
    i0 = idx[0]
    for lab in labels:
        hits = [L[j] for j in range(i0, i0 + 12) if L[j].startswith(lab + " |") and len(L[j].split("|")) == 4]
        assert len(hits) == 1, (f, lab, hits)
        CHECK.setdefault(f, []).append(hits[0])
        out[lab] = (hits[0], [num(t) for t in hits[0].split("|")[1:]])
    return out


def build_vintage(fk, f, years, fy_label, extra_eps=None):
    v = vintage(fk, f, years, S[fk], fy_label, None, None, None, None, extra_eps)
    comp = income_rows(f, ["Asset management and administration fees", "Net interest revenue", "Trading revenue", "Other"])
    groups = [[n, round(c[1][0] / 1000, 3), r1(pct(c[1][1], c[1][0])) if c[1][1] else None] for n, c in comp.items()]
    groups = [[("Asset management and administration fees" if n.startswith("Asset") else n), a, g] for n, a, g in groups]
    tot = round(sum(g[1] for g in groups), 3)
    assert abs(tot - v["rev"][str(v["ly"])]) < 0.0015, (tot, v["rev"])
    b = overview_bounds(f)
    rca, vca = row(f, "Client assets (in billions, at year end) |", *b, n=3)
    rnn, vnn = row(f, "Net new client assets (in billions)", *b, n=3)
    return v, groups, (rca, vca), (rnn, vnn), comp


v06, g06, ca06, nn06, c06 = build_vintage("K06", F06, [2006, 2005, 2004, 2003, 2002], "FY06")
v07, g07, ca07, nn07, c07 = build_vintage("K07", F07, [2007, 2006, 2005, 2004, 2003], "FY07")
v08, g08, ca08, nn08, c08 = build_vintage("K08", F08, [2008, 2007, 2006, 2005, 2004], "FY08",
                                          extra_eps={2003: (v07["eps"]["2003"], v07["rev"]["2003"], v07["sh"]["2003"], S["K07"])})
assert v06["eps"] == {"2003": 0.29, "2004": 0.26, "2005": 0.48, "2006": 0.69}, v06["eps"]
assert v07["eps"]["2007"] == 0.92 and v08["eps"]["2008"] == 1.06
# every year a later 10-K reports equals the earlier vintage's figure (EPS, revenue, diluted shares)
for a, b in ((v06, v07), (v07, v08)):
    for y in set(a["eps"]) & set(b["eps"]):
        assert (a["eps"][y], a["rev"][y], a["sh"][y]) == (b["eps"][y], b["rev"][y], b["sh"][y]), (y,)
# the FY2002 continuing-operations figures the distorted-year test uses (FY2006 10-K)
r06i, v06i = row(F06, "Income from continuing operations before extraordinary gain |", *sel_bounds(F06), n=5)
assert v06i[-1] == 117, v06i
r06e = row(F06, "Income from continuing operations per share — diluted |", *sel_bounds(F06), n=5)
assert r06e[1][-1] == 0.09
r05i, v05i = row(F05, "Income from continuing operations per share — diluted |", *sel_bounds(F05), n=5)
assert v05i[-1] == 0.05, v05i

# the two recast 8-Ks change no figure the history uses (each adds nothing): the 2007-07-17 segment recast of the FY2006 10-K
# and the 2009-06-01 recast of the FY2008 10-K for the segment change and FSP EITF 03-6-1 (continuing-operations EPS unchanged)
F8K07 = doc("0001193125-07-156327", "EX-99.1__dex991.rows.txt")
F8K09 = doc("0001193125-09-122011", "EX-99.1__dex991.rows.txt")
assert row(F8K07, "Total net revenues | 19% | 4,309 | 3,619 |", n=3)[1] == [4309, 3619, 3416]
assert row(F8K07, "Income from continuing operations | 41% | 891 |", n=3)[1] == [891, 634, 350]
b9 = (line_no(F8K09, "Net revenues | 11% |"), line_no(F8K09, "Net revenues | 11% |") + 12)
assert row(F8K09, "Net revenues | 11% |", n=5)[1] == [5150, 4994, 4309, 3619, 3416]
assert row(F8K09, "Income from continuing operations per share — diluted (2) |", *b9, n=5)[1] == [1.06, 0.92, 0.69, 0.48, 0.26]
assert row(F8K09, "Weighted-average common shares outstanding — diluted |", *b9, n=5)[1] == [1157, 1222, 1286, 1308, 1365]
quote(doc("0001193125-09-122011", "8-K__d8k.rows.txt"), "The adoption of this FSP did not change any of the previously reported EPS data in the Company’s Annual Report on "
             "Form 10-K for the year ended December 31, 2008, except for the years ended December 31, 2007 and 2006")

WHY06 = (f"'The Charles Schwab Corporation (CSC) ... {ITEM1}' '{DEV}' '{COMP06}' (FY2006 10-K); {DUR}")
WHY07 = (f"'The Charles Schwab Corporation (CSC) ... {ITEM1}' '{DEV}' '{COMP07}' (FY2007 10-K); {DUR}")
WHY08 = (f"'The Charles Schwab Corporation (CSC) ... {ITEM1}' '{DEV}' '{COMP07}' (FY2008 10-K); {DUR}")
NORM = ("diluted EPS from continuing operations (U.S. Trust discontinued: {ust}), each year from the latest filing "
        "that reports it, GAAP: no filing on the continuing-operations basis publishes a figure excluding one-offs, and no year from "
        "FY2003 meets the AAPL FY2002 test (FY2004's $186M of restructuring charges before tax, the largest, against $350M of income "
        "from continuing operations); FY02 is excluded")


def vint(fk, f, v, groups, ca, nn, fy_label, why, extra_note=""):
    ly = v["ly"]
    return dict(
        published=SRC[S[fk]]["published"], sources=[S[fk]] + ([S["K07"]] if fk == "K08" else []), fy_label=fy_label,
        kind="DURABLE", why=why, eps_normalized=v["eps"], eps_sources=v["srcs"], eps_excluded={},
        eps_first_excluded={"2002": X02}, revenue_usd_b=v["rev"], revenue_sources=v["srcs"], diluted_shares_m=v["sh"],
        shares_sources=v["srcs"], margin_signal_name="Pre-tax margin change",
        prev_fy_op_margin=v["margin"],
        prev_fy_op_margin_note=f"{fy_label} income from continuing operations before taxes on income ${v['pre']:,.0f}M / net revenues "
                               f"${v['rev'][str(ly)] * 1000:,.0f}M",
        prev_fy_pretax_margin=v["margin"],
        prev_fy_pretax_margin_note=f"{fy_label} income from continuing operations before taxes on income ${v['pre']:,.0f}M / net "
                                   f"revenues ${v['rev'][str(ly)] * 1000:,.0f}M",
        prev_fy_sales_growth=v["sales_growth"],
        prev_fy_client_assets_b=ca[1][0], prev_fy_client_assets_growth=r1(pct(ca[1][1], ca[1][0])), prev_fy_nna_b=nn[1][0],
        tax_rate=round(v["tax"] / v["pre"], 4), tax_note=f"{fy_label} taxes on income ${v['tax']:,.0f}M on pre-tax ${v['pre']:,.0f}M",
        dividend_annual=None, dividend_note=None,
        business_line="securities brokerage, banking and related financial services: retail brokerage and banking, services for "
                      "independent investment advisors" + (", corporate and retirement services" if fk != "K06" else "")
                      + " (" + {"K06": "two segments", "K07": "three segments", "K08": "three segments"}[fk] + ")",
        groups=groups, groups_basis=f"{fy_label} net revenues by component (asset management and administration fees, net interest "
                                    f"revenue, trading revenue, other; {fy_label} growth)",
        company="The Charles Schwab Corporation", exchange="Nasdaq", pe_window_start="2003-01-01",
        fiscal_year="year ended December 31,", rows=v["rows"] + [ca[0], nn[0]],
        normalization=NORM.format(ust=("the agreement to sell it to Bank of America of November 19, 2006" if fk == "K06" else
                                       "sold on July 1, 2007")) + extra_note)


V = [vint("K06", F06, v06, g06, ca06, nn06, "FY06", WHY06),
     vint("K07", F07, v07, g07, ca07, nn07, "FY07", WHY07),
     vint("K08", F08, v08, g08, ca08, nn08, "FY08", WHY08,
          "; FY03 from the FY2007 10-K (the FY2008 10-K's selected data starts with 2004)")]

# ── prints ──────────────────────────────────────────────────────────────────────────────────────────────────────────────
Q_END = {1: "March", 2: "June", 3: "September", 4: "December"}
PE = {1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"}
NOTES = {
    "Q3 2008": [("EPS from continuing operations of $.26,", None),
                ("We also faced revenue headwinds this quarter due to the recognition of $73 million in pre-tax charges relating to "
                 "losses on two corporate debt securities that were affected by market turmoil.", None)],
    "Q4 2008": [("The company’s fourth quarter results include $25 million in pre-tax severance charges.", None),
                ("we are proceeding with our previously announced effort to reduce expenses significantly, with the current "
                 "expectation of identifying and implementing cuts totaling 7 to 8% of our 2008 total spending.", None)],
    "Q1 2009": [("The company’s first quarter results include a $26 million pre-tax gain relating to the repurchase of certain "
                 "outstanding company debt, $14 million in pre-tax net impairment losses on certain mortgage-backed securities, and "
                 "$59 million in pre-tax charges for severance and other costs relating to its previously announced expense "
                 "reduction measures.", None)],
    "Q2 2009": [("The company’s second quarter results include $40 million in pre-tax charges relating to its previously announced "
                 "expense reduction measures and a $16 million FDIC special industry assessment.", None),
                ("our commitment to reduce 2009 expenses by 7 to 8% of the 2008 total is on track.", None)],
    "Q3 2009": [("credit-related charges recognized during the quarter totaled $11 million.", None),
                ("money market fund fee waivers increased to $78 million as anticipated, resulting in a 24% decline.", None)],
}
NOTE_TXT = {
    "Q3 2008": "the quarter's EPS includes $.04 of charges on two corporate debt securities ($73M before tax; the 7.01 8-K of "
               "2008-09-29 estimated them), with no figure excluding them, so it stays GAAP (the ACN rule for a one-off with no "
               "published figure without it)",
    "Q4 2008": "$25M of severance charges in the quarter, GAAP; the release's expense goal (cuts of 7 to 8% of 2008's total spending) "
               "is a cost component, not a revenue, EPS or margin guide, so method r2 has no input for it (the JPM and MSFT segment "
               "reading)",
    "Q1 2009": "a $26M debt repurchase gain, $14M of impairment losses and $59M of expense-reduction charges in the quarter, GAAP",
    "Q2 2009": "$40M of expense-reduction charges and a $16M FDIC special assessment in the quarter, GAAP; the 2009 expense goal "
               "restated ('on track'), no field",
    "Q3 2009": "$11M of credit-related impairment charges and $78M of money market fund fee waivers in the quarter, as published",
}


def section(f, title, nth=0):
    return line_no(f, title, nth)


prints = []
order = list(REL)
for qi, q in enumerate(order):
    f = FREL[q]
    qn, fy = int(q[1]), int(q[3:])
    h0 = section(f, "Financial and Operating Highlights")
    c0 = [i for i, x in enumerate(lines(f)) if x.startswith("Growth in Client Assets and Accounts")]
    c0 = c0[-1]
    rr, vr = row(f, "Total net revenues |", start=h0, stop=c0, n=5)
    re_, ve = row(f, "Total expenses excluding interest |", start=h0, stop=c0, n=5)
    pre_lab = "Income before taxes on income |" if q == "Q3 2009" else "Income from continuing operations before taxes on income |"
    rp, vp = row(f, pre_lab, start=h0, stop=c0, n=5)
    rd, vd = row(f, "Revenue trades (", start=h0, stop=c0, n=5)
    rsh, vsh = [(x, None) for x in [None]][0]
    shl = [x for x in lines(f)[h0:c0] if x.startswith("Weighted-average common shares outstanding")]
    assert len(shl) == 1, (q, shl)
    rsh = shl[0]
    vsh = [num(t) for t in rsh.split("|")[1:][-5:]]
    CHECK.setdefault(f, []).append(rsh)
    rc, vc = row(f, "Total client assets |", start=c0, stop=c0 + 40, n=5)
    nnl = [x for x in lines(f)[c0:c0 + 45] if re.match(r"(Total net new (client )?assets|Net new client assets) ", x)]
    assert len(nnl) == 1, (q, nnl)
    rn = nnl[0]
    vn = [num(t) for t in rn.split("|")[1:][-5:]]
    CHECK.setdefault(f, []).append(rn)
    # diluted EPS from continuing operations, the statement of income (quarter, year-ago quarter)
    hl = [x for x in lines(f)[h0:c0] if x.startswith("Diluted earnings per share from continuing operations |")]
    e0 = [i for i, x in enumerate(lines(f)) if re.match(r"Earnings Per Share [—–-] Diluted$", x)]
    if hl:              # the highlights table: the quarter and the year-ago quarter (fifth column)
        re2, ve2 = row(f, "Diluted earnings per share from continuing operations |", start=h0, stop=c0, n=5)
        eps_q, eps_q0 = ve2[0], ve2[4]
    else:               # the statement of income: diluted EPS, income from continuing operations (quarter, year-ago quarter)
        assert e0, q
        re2, ve2 = row(f, "Income from continuing operations |", start=e0[0], stop=e0[0] + 3)
        eps_q, eps_q0 = ve2[0], ve2[1]
    if e0:              # cross-check against the statement where it prints the continuing-operations line
        st = [x for x in lines(f)[e0[0]:e0[0] + 3] if x.startswith("Income from continuing operations |")]
        if st:
            sv = [num(t) for t in st[0].split("|")[1:]]
            assert sv[:2] == [eps_q, eps_q0], (q, sv, eps_q, eps_q0)
    # the 10-Q (for Q1-Q3) reports the same quarter: revenue, expenses, pre-tax income, trades, client assets
    if q in TENQ:
        fq = [os.path.join(SP, "tenq", TENQ[q], x) for x in os.listdir(os.path.join(SP, "tenq", TENQ[q]))
              if x.startswith("10-Q__") and x.endswith(".rows.txt")][0]
        Lq = lines(fq)
        def qrow(lab):
            h = [x for x in Lq if x.startswith(lab)]
            return [num(t) for t in h[0].split("|")[1:3]]
        assert qrow("Total net revenues |")[:2] == [vr[0], vr[4]], (q, "10-Q revenue")
        assert qrow("Total expenses excluding interest |")[:2] == [ve[0], ve[4]], (q, "10-Q expenses")
        pq = qrow("Income from continuing operations before taxes on income |") if any(
            x.startswith("Income from continuing operations before taxes on income |") for x in Lq) else qrow(
            "Income before taxes on income |")
        assert pq[:2] == [vp[0], vp[4]], (q, "10-Q pre-tax")
        assert qrow("Daily average revenue trades (in thousands) (1) |")[:2] == [vd[0], vd[4]], (q, "10-Q trades")
        assert qrow("Client assets (in billions, at quarter end) |")[:2] == [vc[0], vc[4]], (q, "10-Q client assets")
    raw = dict(revenue_m=vr[0], revenue_prior_m=vr[4], revenue_prev_q_m=vr[1], expense_m=ve[0], expense_prior_m=ve[4],
               pretax_m=vp[0], pretax_prior_m=vp[4], client_assets_b=vc[0], client_assets_prior_b=vc[4], dart_k=vd[0],
               dart_prior_k=vd[4], nna_b=vn[0])
    pm, pm0 = raw["pretax_m"] / raw["revenue_m"] * 100, raw["pretax_prior_m"] / raw["revenue_prior_m"] * 100
    d = dict(sales_pct=r1(pct(vr[4], vr[0])), seq_pct=r1(pct(vr[1], vr[0])), pretax_margin=r2(pm), pretax_margin_bp=r1((pm - pm0) * 100),
             expense_pct=r1(pct(ve[4], ve[0])), expense_gap_pp=r1(pct(ve[4], ve[0]) - pct(vr[4], vr[0])),
             ca_pct=r1(pct(vc[4], vc[0])), dart_pct=r1(pct(vd[4], vd[0])))
    pub = SRC[S[q]]["published"]
    filed = SRC[S[q]]["filed"]
    nxt = f"Q{qn % 4 + 1} {fy + (1 if qn == 4 else 0)} print (the quarter ends in {Q_END[qn % 4 + 1]})"
    rel_date = dt.date.fromisoformat(pub)
    note = NOTE_TXT.get(q, "")
    for s_, _ in NOTES.get(q, []):
        quote(f, s_)
    if NOTES.get(q):
        note += " (" + " ".join(f"'{s_}'" for s_, _ in NOTES[q]) + ")"
    p = dict(quarter=q, fy=fy, q=qn, published=pub, source=S[q], release=f"{rel_date:%b} {rel_date.day}",
             release_time=f"8-K {filed}; no filing states the release time", period_end=f"{fy}-{PE[qn]}", raw=raw,
             rows=dict(rev=rr, exp=re_, pre=rp, dart=rd, ca=rc, nna=rn, eps=re2, shares=rsh),
             sales_b=round(vr[0] / 1000, 3), ca_b=vc[0], dart_k=vd[0], nna_b=vn[0], **d, eps_q=eps_q, eps_q_prior=eps_q0,
             diluted_shares_m=vsh[0],
             sales_note=f"net revenues ${vr[0]:,.0f}M vs ${vr[4]:,.0f}M a year earlier, ${vr[1]:,.0f}M the quarter before",
             client_note=f"client assets ${vc[0]:,.1f}B vs ${vc[4]:,.1f}B a year earlier; net new client assets ${vn[0]:,.1f}B in the "
                         f"quarter; daily average revenue trades {vd[0]:,.1f}K vs {vd[4]:,.1f}K",
             eps_note=f"diluted EPS from continuing operations ${eps_q:.2f} vs ${eps_q0:.2f}, GAAP",
             shares_note=f"diluted shares {vsh[0]:,.0f}M; expenses excluding interest ${ve[0]:,.0f}M vs ${ve[4]:,.0f}M",
             next_print=nxt, note=note)
    if qn == 4:
        # full-year actuals from the statement of income's twelve-month columns
        s0 = [i for i, x in enumerate(lines(f)) if x.startswith("Consolidated Statements of Income")][0]
        rfr, vfr = row(f, "Total net revenues |", start=s0, stop=h0)
        rfp, vfp = row(f, "Income from continuing operations before taxes on income |", start=s0, stop=h0)
        rft, vft = row(f, "Taxes on income |", start=s0, stop=h0)
        rfs = [x for x in lines(f)[s0:h0] if re.match(r"Weighted-Average Common Shares Outstanding [—–-] Diluted", x)]
        assert len(rfs) == 1
        vfs = [num(t) for t in rfs[0].split("|")[1:][-4:]]
        CHECK.setdefault(f, []).append(rfs[0])
        est = [x for x in lines(f)[e0[0]:e0[0] + 3] if x.startswith("Income from continuing operations |")]
        assert len(est) == 1, q
        CHECK.setdefault(f, []).append(est[0])
        ve3 = [num(t) for t in est[0].split("|")[1:]]
        rev_y, pre_y, tax_y, sh_y, eps_y = vfr[2], vfp[2], -vft[2], vfs[2], ve3[2]
        ly = {2006: 0.69, 2007: 0.92, 2008: 1.06}[fy]
        assert eps_y == ly, (q, eps_y)
        m = r2(pre_y / rev_y * 100)
        p["fy_actual"] = dict(
            fy=fy, fy_label=f"FY{fy % 100:02d}", eps_normalized=eps_y, revenue_usd_b=round(rev_y / 1000, 3), diluted_shares_m=sh_y,
            normalization_note=f"FY{fy % 100:02d} ${eps_y:.2f}, diluted EPS from continuing operations, GAAP ({q} release)",
            op_margin=m, op_margin_note=f"FY{fy % 100:02d} income from continuing operations before taxes on income ${pre_y:,.0f}M / "
                                        f"net revenues ${rev_y:,.0f}M ({q} release)",
            pretax_margin=m, pretax_margin_note=f"FY{fy % 100:02d} income from continuing operations before taxes on income "
                                                f"${pre_y:,.0f}M / net revenues ${rev_y:,.0f}M ({q} release)",
            sales_growth=r1(pct(vfr[3], vfr[2])), client_assets_b=vc[0], client_assets_growth=d["ca_pct"],
            tax_rate=round(tax_y / pre_y, 4), tax_note=f"FY{fy % 100:02d} taxes on income ${tax_y:,.0f}M on pre-tax ${pre_y:,.0f}M",
            rows=[rfr, rfp, rft, rfs[0], est[0]])
    prints.append(p)

# ── dividends: the latest declared quarterly rate, each from the first filing that states it ─────────────────────────────
FQ306 = doc(Q306_10Q, "10-Q__d10q.rows.txt")
FQ208 = doc(Q208_10Q, "10-Q__d10q.rows.txt")
D1 = "On October 19, 2006, the Board of Directors increased the quarterly cash dividend from $.03 to $.05 per share"
D2 = "on July 22, 2008, the Board of Directors increased the quarterly cash dividend from $.05 per share to $.06 per share"
quote(FQ306, D1)
quote(FQ208, D2)
dividends = [dict(published=SRC[S["Q306Q"]]["published"], quarterly=0.05, source=S["Q306Q"], note=f"$0.05 a quarter: '{D1}' (Q3 2006 10-Q)"),
             dict(published=SRC[S["Q208Q"]]["published"], quarterly=0.06, source=S["Q208Q"], note=f"$0.06 a quarter: '{D2}' (Q2 2008 10-Q)")]

facts = dict(
    _doc=("Point-in-time fact sheet for SCHW retrospectives (retro/build_schw.py), generated from The Charles Schwab Corporation's own "
          "filings: every raw figure is read from the row it appears in (kept in 'rows'), checked against its filing, and every "
          "growth rate, margin, gap and rule-T value is computed from those figures. Every value carries a source with its "
          "publication date (EDGAR acceptance time, ET; a filing accepted after the 16:00 ET close is dated the next trading day). "
          "Decisions: retro/README.md, 'SCHW'."),
    ticker="SCHW", sources=SRC, history_vintages=V, prints=prints, guides=[], dividends=dividends, events=[], company_names=[],
    splits=[], listings=[], rule_t=rule_t,
    fiscal_calendar=dict(rule="the calendar year", quote=quote(F06, "Results for the years ended December 31, 2006, 2005, and 2004 are shown in the following table:"),
                         source=S["K06"]),
    price_basis=("Yahoo's SCHW series is the common stock of the registrant (CIK 316709), listed on The Nasdaq Stock Market on every "
                 "date (each 10-K's Item 5). Its splits (the last on 2000-05-31) precede every date in the P/E window (2003-01-01 on), "
                 "so every price the models use is the close as traded; the 2007 special dividend of $1.00 is not a split and the "
                 "series is not adjusted for it."))
out = A.out or os.path.join(REPO, "retro", "facts", "SCHW.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(facts, fh, ensure_ascii=False, indent=1)
with open(A.checklist or os.path.join(SP, "checklist_schw.json"), "w", encoding="utf-8") as fh:
    json.dump(CHECK, fh, ensure_ascii=False, indent=1)
print(out, len(prints), "prints;", sum(len(v) for v in CHECK.values()), "checklist strings")
for k, v in rule_t.items():
    print(k, v["values"], v["thresholds"])
for p in prints:
    print(p["quarter"], p["published"], p["sales_pct"], p["ca_pct"], p["expense_gap_pp"], p["dart_pct"], p["pretax_margin_bp"], p["eps_q"])
for s, v in SRC.items():
    print(s, v["published"], v["filed"], v["title"])
