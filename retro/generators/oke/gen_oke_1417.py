#!/usr/bin/env python3
"""Extend retro/facts/OKE.json with 2014-2017 (filings accepted 2013-12-01 to 2017-12-31), asserting that every earlier fact is
unchanged. Same discipline as gen_oke.py and gen_oke_1013.py: each raw figure is read from its own labelled row of a named table (the
row text is kept in the fact and written to the verbatim checklist) or from the sentence that holds it (asserted present word for word),
every rate, margin and change is computed, and every quote is asserted present in its own filing. Only filings accepted on or before
2017-12-31 are read. The downloads (keep them outside the repo, e.g. the session scratchpad):

    python3 retro/tools/edgar.py index 1039684 <dir>
    python3 retro/tools/edgar.py fetch 1039684 <dir> --from 2013-12-01 --to 2017-12-31 --forms 8-K 8-K/A 10-K 10-K/A 10-Q

    python3 -I retro/generators/oke/gen_oke_1417.py --filings <dir> [--facts-in <2008-2013 sheet>] [--out retro/facts/OKE.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_oke_1417.json

--facts-in is the 2008-2013 sheet gen_oke_1013.py writes (default: retro/facts/OKE.json, which must then hold 2008-2013 only).
What the batch reads and decides is in retro/README.md, "OKE 2014-2017".
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
START, CUT = "2014-01-01", "2017-12-31"
CIK = 1039684
ROWS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("OKE")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
old = json.load(open(A.facts_in or os.path.join(REPO, "retro", "facts", "OKE.json"), encoding="utf-8"))
assert all(s["published"] <= "2013-12-31" for s in old["sources"].values()), "--facts-in must be the 2008-2013 sheet"
f = copy.deepcopy(old)
CHECK = {}
TEXT = {}
norm = lambda s: re.sub(r"\s+", " ", s).strip()
# the 8-K of 2013-12-02 (2014 guidance) was read by the 2010-2013 batch for its 2013 content only; its FY2014 net income midpoint is
# current from the FY2013 vintage, after that range, so it enters here with its own date (2013-12-03)
EARLY = {"0001039684-13-000108"}


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
    t = t.replace(",", "").replace("$", "").replace("~", "").strip()
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
    assert START <= day <= CUT or acc in EARLY, (acc, day)
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

# ── the 10-Ks: the FY2013-FY2016 vintages ─────────────────────────────────────────────────────────────────────────────────────────
K = {"F2013": "0001039684-14-000019", "F2014": "0001039684-15-000017", "F2015": "0001039684-16-000113", "F2016": "0001039684-17-000019"}
DK = {k: path(a, "10-K__*.rows.txt") for k, a in K.items()}
# the 8-K of 2017-07-06 re-files the FY2016 10-K's Item 8 with one added footnote (condensed consolidating information for the
# guarantees that followed the ONEOK Partners merger): no figure the models read changes, so it is no vintage (the NEM rule)
RECAST = path("0001039684-17-000085", "8-K__*.rows.txt")
quote(RECAST, "No other information in the 2016 Form 10-K, other than that relating to the information identified above, is being "
      "updated by this filing.")

# ── the ONE Gas distribution (a spin-off, not a split): one ONE Gas share for every four ONEOK shares ─────────────────────────────
DIST_ANN, DIST_DONE = "0001193125-14-006786", "0001039684-14-000010"
DQ1 = quote(path(DIST_ANN, "8-K__*.rows.txt"), "ONEOK will distribute one share of common stock of ONE Gas, par value $0.01 per share, "
            "for every four shares of ONEOK common stock held by ONEOK shareholders of record as of the close of business on January 21, "
            "2014, the record date for the Distribution.")
DQ2 = quote(path(DIST_DONE, "8-K__*.rows.txt"), "On January 31, 2014, ONEOK completed the Distribution and the separation of ONE Gas from "
            "ONEOK. ONE Gas is now an independent, publicly traded, 100 percent regulated natural gas distribution utility trading under the "
            "ticker symbol “OGS” on the New York Stock Exchange. Following the close of business on January 31, ONEOK distributed one share "
            "of ONE Gas Common Stock, par value $0.01 per share, for every four shares of common stock of ONEOK held by shareholders of "
            "record as of the close of business on January 21, 2014, the record date for the Distribution.")
# the completion 8-K's pro forma statements (Exhibit 99.3) are unused (the BKR, PFE, CMCSA, BMY, SO and SPGI pro forma rule)
quote(path(DIST_DONE, "8-K__*.rows.txt"), "The unaudited pro forma condensed consolidated balance sheet of ONEOK, Inc. and its subsidiaries "
      "as of September 30, 2013")

# ── sources, in date order ───────────────────────────────────────────────────────────────────────────────────────────────────────
plan = [("guide8k", "0001039684-13-000108", "ONEOK 8-K: 2014 financial guidance (Item 7.01; Exhibit A, earnings guidance midpoints)"),
        ("distann", DIST_ANN),
        ("div", "0001039684-14-000004", 0.40),
        ("distdone", DIST_DONE),
        ("print", "Q4 2013", 2013, 4, "0001039684-14-000016"),
        ("k", "F2013"),
        ("div", "0001039684-14-000029", 0.56),
        ("print", "Q1 2014", 2014, 1, "0001039684-14-000031"),
        ("div", "0001039684-14-000059", 0.575),
        ("print", "Q2 2014", 2014, 2, "0001039684-14-000063"),
        ("div", "0001039684-14-000079", 0.59),
        ("print", "Q3 2014", 2014, 3, "0001039684-14-000083"),
        ("guide8k", "0001039684-14-000094", "ONEOK 8-K: next-year financial guidance; the current-year midpoints restated (Item 7.01)"),
        ("div", "0001039684-15-000006", 0.605),
        ("print", "Q4 2014", 2014, 4, "0001039684-15-000014"),
        ("k", "F2014"),
        ("print", "Q1 2015", 2015, 1, "0001039684-15-000031"),
        ("print", "Q2 2015", 2015, 2, "0001039684-15-000057"),
        ("div", "0001039684-15-000070", 0.615),
        ("print", "Q3 2015", 2015, 3, "0001039684-15-000073"),
        ("guide8k", "0001039684-15-000086", "ONEOK 8-K: 2016 financial guidance (Item 7.01)"),
        ("print", "Q4 2015", 2015, 4, "0001039684-16-000111"),
        ("k", "F2015"),
        ("print", "Q1 2016", 2016, 1, "0001039684-16-000123"),
        ("print", "Q2 2016", 2016, 2, "0001039684-16-000143"),
        ("print", "Q3 2016", 2016, 3, "0001039684-16-000157"),
        ("guide8k", "0001193125-17-027652", "ONEOK 8-K: 2017 financial guidance, assuming the acquisition of ONEOK Partners effective Jan. 1, "
                                            "2017 (Items 2.02, 7.01)"),
        ("print", "Q4 2016", 2016, 4, "0001039684-17-000012"),
        ("k", "F2016"),
        ("print", "Q1 2017", 2017, 1, "0001039684-17-000042"),
        ("div", "0001039684-17-000092", 0.745),
        ("print", "Q2 2017", 2017, 2, "0001039684-17-000096"),
        ("print", "Q3 2017", 2017, 3, "0001039684-17-000115")]
SID_PRINT, SID_8K, SID_DIV, SID_K = {}, {}, {}, {}
S_DIST_ANN = S_DIST_DONE = None
for step in plan:
    if step[0] == "print":
        _, q, fy, n, acc = step
        SID_PRINT[q] = src(acc, f"ONEOK {q} results (8-K exhibit 99.1)",
                           f"{q}: revenues, net margin, operating income, income before income taxes, diluted EPS from continuing "
                           "operations, diluted shares" + (" and the Distribution segment's operating income" if q == "Q4 2013" else "")
                           + "; the net income guidance where the release gives one")
    elif step[0] == "guide8k":
        SID_8K[step[1]] = src(step[1], step[2], "the net income guidance it states")
    elif step[0] == "div":
        SID_DIV[step[1]] = src(step[1], f"ONEOK 8-K: quarterly dividend of ${step[2]:g} (Items 7.01, 8.01)",
                               f"the quarterly dividend rate, ${step[2]:g} a share")
    elif step[0] == "k":
        SID_K[step[1]] = src(K[step[1]], f"ONEOK {step[1].replace('F', 'FY')} 10-K", f"history vintage {step[1].replace('F', 'FY')}; the 'why'")
    elif step[0] == "distann":
        S_DIST_ANN = src(DIST_ANN, "ONEOK 8-K: the ONE Gas distribution approved; ratio and record date (Items 5.02, 8.01)",
                         "the distribution ratio (one ONE Gas share for every four ONEOK shares) and its record date")
    elif step[0] == "distdone":
        S_DIST_DONE = src(DIST_DONE, "ONEOK 8-K: the ONE Gas distribution completed (Items 2.01, 2.04, 8.01, 9.01)",
                          "the separation of ONE Gas completed on January 31, 2014, one share for every four ONEOK shares")
srt_src = sorted(SOURCES.items(), key=lambda kv: (kv[1]["published"], int(kv[0][2:])))
assert [k for k, _ in srt_src] == sorted(SOURCES, key=lambda k: int(k[2:])), "source ids must follow publication order"
SPUB = {**{k: v["published"] for k, v in old["sources"].items()}, **{k: v["published"] for k, v in SOURCES.items()}}

# ── history vintages: each year from the latest filing that reports it; the ten fiscal years to the latest one ─────────────────────
V12 = old["history_vintages"][-1]                     # the FY2012 vintage (2010-2013 sheet)
assert V12["fy_label"] == "FY12"
ST = r"^CONSOLIDATED STATEMENTS OF INCOME$"
I6 = r"^ITEM 6\.( \|)? SELECTED FINANCIAL DATA$"


def item6_eps(fk):
    return row(DK[fk], r"Diluted", I6, r"^Earnings per share - continuing operations$")


def stmt(fk, label, n=3, after=None):
    return row(DK[fk], label, ST, after, n=n)


def why(fk, lead, extra):
    lo = joined(DK[fk]).lower()
    # DURABLE needs the company not to call its own business cyclical (the MU rule): the only use of the word is the billing cycle
    assert lo.count("cyclical") == lo.count("invoiced on a cyclical basis"), (fk, "a 10-K that calls the business cyclical")
    q = [quote(DK[fk], lead), quote(DK[fk], "Our cash flow depends heavily on the earnings and distributions of ONEOK Partners."),
         quote(DK[fk], extra)]
    label = fk.replace("F", "FY")
    tail = ("it calls no business of the company cyclical, the word appearing only in its billing cycle" if "cyclical" in lo else
            "it does not use the word cyclical")
    return " ".join(f"'{x}'" for x in q) + f" (the {label} 10-K's own words; {tail}, so DURABLE, the MU rule)"


def groups(fk, fy):
    """Segment sales to unaffiliated customers, the last year and the one before, by the segment note's own column heads (Other,
    eliminations and totals left out)."""
    out = {}
    ls = lines(DK[fk])
    for y in (fy, fy - 1):
        k = next(i for i, l in enumerate(ls) if l.startswith(f"Year Ended December 31, {y} |") and ("ONEOK" in l or "Gathering" in l))
        heads = [c.strip() for c in ls[k].split("|")[1:]]
        r = next(l for l in ls[k:k + 6] if l.startswith("Sales to unaffiliated customers |"))
        CHECK.setdefault(DK[fk], []).append(r)
        vals = [num(c) for c in r.split("|")[1:] if c.strip()]
        assert len(vals) == len(heads), (fk, y, heads, vals)
        out[y] = {h: v for h, v in zip(heads, vals) if not re.search(r"(?i)^(Other|Total)", h)}
    name = lambda h: re.sub(r"\s*\([a-z]\)$", "", re.sub(r"(?<=[a-z])(?=[A-Z])", " ", h.replace("ONEOKPartners", "ONEOK Partners")))
    return [[name(h), round(v / 1e6, 3), pct1(out[fy - 1][h], v)] for h, v in out[fy].items()]


def vintage(fk, fy, eps, rev, sh, lead, extra, div_q, div_sentence, restate_note, business_line, kind_text, theme_quotes):
    """eps / rev / sh: {year: (value, source id)}; the per-year sources give each year's publication date (on_basis)."""
    st = {"rev": stmt(fk, r"(Total revenues|Revenues)")[0], "oi": stmt(fk, r"Operating income")[0],
          "pti": stmt(fk, r"Income before income taxes")[0], "tax": [abs(x) for x in stmt(fk, r"Income taxes( \(Note [A-Z]\))?")[0]]}
    cf = r"^CONSOLIDATED STATEMENTS OF CASH FLOWS( \||$)"
    cfo = row(DK[fk], r"Cash provided by operating activities", cf, n=3)[0]
    cx = [abs(x) for x in row(DK[fk], r"Capital expenditures \(less allowance for equity funds used during construction\)", cf, n=3)[0]]
    try:
        rp = [abs(x) for x in row(DK[fk], r"Repurchase of common stock", cf, n=3)[0]]
        cash_return = f"repurchases of common stock ${rp[0] / 1000:,.1f}M in {fy} (FY{fy} 10-K's statement of cash flows)"
    except AssertionError:      # the FY2015 and FY2016 statements of cash flows have no repurchase line
        cash_return = f"no repurchase of common stock in {fy} (the FY{fy} 10-K's statement of cash flows has no repurchase line)"
    sid = SID_K[fk]
    years = sorted(eps)
    assert years == list(range(years[0], fy + 1)) and len(years) == 10, (fk, years)
    first = years[0]
    v = {
        "published": SPUB[sid], "sources": sorted({sid} | {s for _, s in eps.values()} | {s for _, s in rev.values()}
                                                 | {s for _, s in sh.values()}, key=lambda s: -int(s[2:])),
        "company": "ONEOK, Inc.", "exchange": "NYSE", "symbol": "OKE",
        "business_line": business_line,
        "fy_label": f"FY{fy % 100:02d}", "fiscal_year_ends": {str(y): f"{y}-12-31" for y in years},
        "eps_normalized": {str(y): eps[y][0] for y in years}, "eps_sources": {str(y): eps[y][1] for y in years},
        "eps_published": {str(y): SPUB[eps[y][1]] for y in years},
        "eps_excluded": {}, "eps_first_excluded": {},
        "revenue_usd_b": {str(y): round(rev[y][0] / 1e6, 6) if rev[y][1] in SOURCES else rev[y][0] for y in years},
        "revenue_sources": {str(y): rev[y][1] for y in years},
        "diluted_shares_m": {str(y): round(sh[y][0] / 1000, 3) if sh[y][1] in SOURCES else sh[y][0] for y in years},
        "shares_sources": {str(y): sh[y][1] for y in years},
        "shares_published": {str(y): SPUB[sh[y][1]] for y in years},
        "shares_note": "diluted average shares of common stock, millions (each statement of income)",
        "normalization": V12["normalization"].split("; 2008-2012 from the FY2012 10-K")[0] + "; " + restate_note,
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
        "dividend_annual": round(div_q * 4, 3),
        "dividend_note": f"${div_q:g} a quarter, ${div_q * 4:g} a year: '{quote(DK[fk], div_sentence)}' (FY{fy} 10-K)",
        "fcf_label": f"FY{fy % 100:02d}", "fcf_b": round((cfo[0] - cx[0]) / 1e6, 3),
        "fcf_note": (f"cash provided by operating activities ${cfo[0] / 1000:,.1f}M less capital expenditures ${cx[0] / 1000:,.1f}M "
                     f"(FY{fy} 10-K, consolidated, ONEOK Partners' included)"),
        "cash_return_text": cash_return,
        "groups": groups(fk, fy), "groups_basis": f"FY{fy % 100:02d} segment sales to unaffiliated customers (FY{fy} 10-K segment note; "
                                                  "eliminations and Other left out)",
        "margin_signal_name": "Pre-tax margin change",
        "kind": "DURABLE", "kind_text": kind_text,
        "why": why(fk, lead, extra),
        # (OKE 2014-2017) the 10-K's own words that the builder quotes beside a live theme's registered scope (text only)
        "theme_quotes": {k: quote(DK[fk], s) for k, s in theme_quotes.items()},
    }
    return v


c_eps = {int(y): (v, V12["eps_sources"][y]) for y, v in V12["eps_normalized"].items()}
c_rev = {int(y): (v, V12["revenue_sources"][y]) for y, v in V12["revenue_usd_b"].items()}
c_sh = {int(y): (v, V12["shares_sources"][y]) for y, v in V12["diluted_shares_m"].items()}
X2 = "The volatility of natural gas, crude oil and NGL prices could affect adversely ONEOK Partners’ cash flows."
GHG = "ONEOK Partners may face significant costs to comply with the regulation of GHG emissions."
RES = ("ONEOK Partners may also rely on estimates of proved reserves in its decision to construct new pipelines and facilities, which may "
       "prove to be inaccurate because there are numerous uncertainties inherent in estimating quantities of proved reserves.")
RES2 = ("ONEOK Partners may rely on estimates of proved reserves in its decision to construct new pipelines and facilities, which may "
        "prove to be inaccurate because there are numerous uncertainties inherent in estimating quantities of proved reserves")
BL_GP = ("the general partner of ONEOK Partners, L.P. (NYSE: OKS), consolidated: natural gas gathering and processing, natural gas "
         "liquids and natural gas pipelines")
KT_GP = "The general partner of a midstream partnership"


def themes(fk):
    out = {"ENERGY_TRANSITION_ghg": GHG} if GHG in joined(DK[fk]) else {}
    res = [x for x in (RES, RES2) if norm(x) in joined(DK[fk])]
    assert len(res) == 1, (fk, "the reserves sentence")       # the producers' reserves, not ONEOK Partners' own
    out["ENERGY_TRANSITION_reserves"] = res[0]
    if "cloud computing arrangement" in joined(DK[fk]).lower():
        out["CLOUD_words"] = next(s for s in ("ASU 2015-05, “Intangibles—Goodwill and Other—Internal-Use Software (Subtopic 350-40): Customer’s "
                                              "Accounting for Fees Paid in a Cloud Computing Arrangement,” which clarifies whether a cloud "
                                              "computing arrangement includes a software license.",
                                              "The standard clarifies whether a cloud computing arrangement includes a software license.")
                                  if norm(s) in joined(DK[fk]))
    return out


V = []
# FY2013 10-K (2014-02-26): 2009-2013 EPS from continuing operations in Item 6 (the Distribution and Energy Services segments still in
# continuing operations: the separation came after the year), 2011-2013 statements
e, _ = item6_eps("F2013")
assert e == [1.27, 1.64, 1.67, 1.55, 1.40], e
r, _ = stmt("F2013", r"Revenues")
s, _ = stmt("F2013", r"Diluted", after=r"(?i)^Average shares")
S13 = SID_K["F2013"]
eps13 = {**c_eps, **{y: (e[2013 - y], S13) for y in range(2009, 2014)}}
rev13 = {**c_rev, 2011: (r[2], S13), 2012: (r[1], S13), 2013: (r[0], S13)}
sh13 = {**c_sh, 2011: (s[2], S13), 2012: (s[1], S13), 2013: (s[0], S13)}
for d in (eps13, rev13, sh13):
    del d[2003]
Q13 = quote(path("0001039684-14-000016", "EX-99.1__*.rows.txt"), "2013 net income attributable to ONEOK was $266.5 million, or $1.27 per "
            "diluted share, which includes non-cash, after-tax charges of $87.2 million, or 42 cents per diluted share, associated with the "
            "energy services segment wind down and after-tax costs of $19.6 million, or 9 cents per diluted share, associated with the ONE "
            "Gas separation.")
V.append(vintage("F2013", 2013, eps13, rev13, sh13, "We are a diversified energy company and successor to the company founded in 1906 "
                 "as Oklahoma Natural Gas Company.", X2, 0.40, "In January 2014, we declared a dividend of $0.40 per share ($1.60 per share "
                 "on an annualized basis) which was paid on February 18, 2014, to shareholders of record as of February 10, 2014.",
                 "2009-2013 from the FY2013 10-K's Item 6, 'Earnings per share - continuing operations', the natural gas distribution and "
                 "energy services businesses in (the separation of ONE Gas came on January 31, 2014, after the year); 2013 at GAAP $1.27: "
                 f"its listed items ('{Q13}', the Q4 2013 release) are $106.8M after tax against $266.5M, under half the year's income "
                 "without them, and no filing publishes EPS without them; the ten fiscal years to the latest one, so 2003 leaves and the "
                 "window starts with 2004",
                 "natural gas distribution (Oklahoma, Kansas, Texas; separated as ONE Gas, Inc. on January 31, 2014, in the FY2013 figures) "
                 "and energy services (wound down); " + BL_GP,
                 "A gas distributor (separated on 2014-01-31) and the general partner of a midstream partnership", themes("F2013")))
# FY2014 10-K (2015-02-25): EPS from continuing operations, 2010-2014 restated without the natural gas distribution business (ONE Gas)
# and the energy services business (both discontinued operations from the Q1 2014 release); 2012-2014 statements likewise; 2005-2009
# as their own filings report them, the distribution and energy services businesses in (a seam, as published)
e, _ = item6_eps("F2014")
assert e == [1.52, 1.33, 1.40, 1.15, 0.66], e
r, _ = stmt("F2014", r"Total revenues")
s, _ = stmt("F2014", r"Diluted", after=r"(?i)^Average shares")
S14 = SID_K["F2014"]
eps14 = {**eps13, **{y: (e[2014 - y], S14) for y in range(2010, 2015)}}
rev14 = {**rev13, 2012: (r[2], S14), 2013: (r[1], S14), 2014: (r[0], S14)}
sh14 = {**sh13, 2012: (s[2], S14), 2013: (s[1], S14), 2014: (s[0], S14)}
for d in (eps14, rev14, sh14):
    del d[2004]
LEAD = lambda y, p: (f"We are the sole general partner and, as of December 31, {y}, owned {p} percent of ONEOK Partners (NYSE: OKS), one of "
                     "the largest publicly traded master limited partnerships.")
QSEP = quote(DK["F2014"], "Wind Down of Energy Services Business - We completed the wind down of our energy services business, which ceased "
             "operations on March 31, 2014, and was classified as discontinued operations.")
Q14 = quote(path("0001039684-15-000014", "EX-99.1__*.rows.txt"), "The decrease in equity earnings is primarily due to a $76.4 million "
            "noncash impairment charge at ONEOK Partners in the third quarter 2014.")
V.append(vintage("F2014", 2014, eps14, rev14, sh14, LEAD(2014, "37.8"), X2, 0.605, "In January 2015, we declared a dividend of $0.605 per "
                 "share ($2.42 per share on an annualized basis), which was paid on February 13, 2015, to shareholders of record as of "
                 "January 30, 2015.",
                 "2010-2014 from the FY2014 10-K's Item 6, 'Earnings per share - continuing operations', restated without the natural gas "
                 f"distribution business (ONE Gas, separated on January 31, 2014) and the energy services business ('{QSEP}'), and 2012-2014 "
                 "revenues and shares likewise; 2005-2009 as their own filings report them, both businesses in (a seam, as published); 2014 "
                 f"at GAAP (its one listed item, '{Q14}' (the Q4 2014 release), is ONEOK Partners' and far under the year's $319.7M of "
                 "continuing income attributable to ONEOK even in full); the ten fiscal years to the latest one, so 2004 leaves and the "
                 "window starts with 2005",
                 BL_GP, KT_GP, themes("F2014")))
# FY2015 10-K (2016-02-24): 2011-2015 from Item 6 (continuing operations), 2013-2015 statements
e, _ = item6_eps("F2015")
assert e == [1.19, 1.52, 1.33, 1.40, 1.15], e
r, _ = stmt("F2015", r"Total revenues")
s, _ = stmt("F2015", r"Diluted", after=r"(?i)^Average shares")
S15 = SID_K["F2015"]
eps15 = {**eps14, **{y: (e[2015 - y], S15) for y in range(2011, 2016)}}
rev15 = {**rev14, 2013: (r[2], S15), 2014: (r[1], S15), 2015: (r[0], S15)}
sh15 = {**sh14, 2013: (s[2], S15), 2014: (s[1], S15), 2015: (s[0], S15)}
for d in (eps15, rev15, sh15):
    del d[2005]
Q15 = quote(path("0001039684-16-000111", "EX-99.1__*.rows.txt"), "Amounts include noncash impairment charges at ONEOK Partners of $264.3 "
            "million, or 33 cents per diluted share, in the fourth quarter 2015; and $76.4 million, or 9 cents per diluted share, in the third "
            "quarter 2014.")
V.append(vintage("F2015", 2015, eps15, rev15, sh15, LEAD(2015, "41.2"), X2, 0.615, "In January 2016, we declared a dividend of $0.615 per "
                 "share ($2.46 per share on an annualized basis), which was paid on February 12, 2016, to shareholders of record as of "
                 "February 1, 2016.",
                 "2011-2015 from the FY2015 10-K's Item 6, 'Earnings per share - continuing operations'; 2015 at GAAP $1.19: its listed item "
                 f"('{Q15}', the Q4 2015 release) is 33 cents a diluted share against $1.52 without it, under half, and no filing publishes "
                 "a full-year EPS without it (the release's 45 cents is the quarter's); the ten fiscal years to the latest one, so 2005 leaves "
                 "(with the company's figure without the gain on sale) and the window starts with 2006",
                 BL_GP, KT_GP, themes("F2015")))
# FY2016 10-K (2017-03-01): 2012-2016 from Item 6, 2014-2016 statements
e, _ = item6_eps("F2016")
assert e == [1.67, 1.19, 1.52, 1.33, 1.40], e
r, _ = stmt("F2016", r"Total revenues")
s, _ = stmt("F2016", r"Diluted", after=r"(?i)^Average shares")
S16 = SID_K["F2016"]
eps16 = {**eps15, **{y: (e[2016 - y], S16) for y in range(2012, 2017)}}
rev16 = {**rev15, 2014: (r[2], S16), 2015: (r[1], S16), 2016: (r[0], S16)}
sh16 = {**sh15, 2014: (s[2], S16), 2015: (s[1], S16), 2016: (s[0], S16)}
for d in (eps16, rev16, sh16):
    del d[2006]
V.append(vintage("F2016", 2016, eps16, rev16, sh16, LEAD(2016, "41.2"), X2, 0.615, "In January 2017, we declared a dividend of $0.615 per "
                 "share ($2.46 per share on an annualized basis), which was paid on February 14, 2017, to shareholders of record as of "
                 "January 30, 2017.",
                 "2012-2016 from the FY2016 10-K's Item 6, 'Earnings per share - continuing operations'; 2016 at GAAP (no listed item); the ten "
                 "fiscal years to the latest one, so 2006 leaves (with the company's figure without the gain on sale) and the window starts "
                 "with 2007",
                 BL_GP, KT_GP, themes("F2016")))
for v in V:
    assert all(v["eps_published"][y] <= v["published"] for y in v["eps_normalized"])
# the 2005 and 2006 company figures leave with the FY2014 and FY2015 vintages; 2007 (FY2011 10-K, pre-split) is halved by on_basis
assert "2005" not in V[2]["eps_normalized"] and V[3]["eps_published"]["2007"] < "2012-06-04"

# ── the prints ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
NEXT = {1: "Q2 print (early August)", 2: "Q3 print (early November)", 3: "Q4 and full-year print, with the 10-K (late February)",
        4: "Q1 print (late April or early May)"}
PR = []
MON = {m: i for i, m in enumerate(["Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"], 1)}


def fmt_e(x):
    return f"${x:.2f}" if x >= 0 else f"$({-x:.2f})"


def fm(x):
    return f"${x:,.1f}M" if x >= 0 else f"$({-x:,.1f})M"


def prt(q, fy, n, acc):
    sid = SID_PRINT[q]
    p = path(acc, "EX-9[59].1__*.rows.txt")     # the Q3 2015 release is filed as exhibit 95.1
    dl = next(l for l in lines(p) if l.startswith("TULSA, Okla."))
    m = re.match(r"TULSA, Okla\. [–-] (\w+)\.? (\d+), (\d{4})", dl)
    rel = f"{m.group(1)[:3]} {int(m.group(2))}"
    rv, t_rv = row(p, r"(Total revenues|Revenues)", ST)
    try:
        nm, t_nm = row(p, r"Net margin", ST, n=len(rv))
        cost = None
    except AssertionError:
        # (from the Q4 2015 release) the statement of income no longer prints a net margin line: net margin is revenues less cost of
        # sales and fuel, ONEOK's own definition of it (the first line of its Item 6 to FY2013), computed from the two printed lines
        cost, t_nm = row(p, r"Cost of sales and fuel \(exclusive of items shown separately below\)", ST, n=len(rv))
        nm = [a - b for a, b in zip(rv, cost)]
    oi, t_oi = row(p, r"Operating income", ST)
    pti, t_pt = row(p, r"Income( \(loss\))? before income taxes", ST)
    eps, t_e = row(p, r"Income from continuing operations", ST, r"^Diluted earnings per (common )?share:?$")
    sh, t_s = row(p, r"Diluted", ST, r"(?i)^Average shares")
    cash, t_c = row(p, r"Cash and cash equivalents", r"^CONSOLIDATED BALANCE SHEETS$")
    if q == "Q4 2013":       # the last print with the natural gas distribution segment
        ds, t_d = row(p, r"Operating income( \(loss\))?", r"(?i)INFORMATION AT A GLANCE", r"(?i)^(Natural Gas )?Distribution$")
        dm, dpm, dnote = ds[0], ds[1], f"Distribution operating income {fm(ds[0])} vs {fm(ds[1])}"
    else:
        # from the Q1 2014 release the separated natural gas distribution business is in discontinued operations: the release has no
        # Distribution segment, so the signal is n/r (not reported; the engine scores it at BASE)
        assert not re.search(r"(?i)^(Natural Gas )?Distribution$", "\n".join(lines(p)), re.M), (q, "a Distribution segment in the release")
        ds = t_d = None
        dm = dpm = None
        dnote = "Distribution operating income n/r (the natural gas distribution business separated as ONE Gas on January 31, 2014)"
    r = {"rev_m": rv[0] / 1000, "rev_prior_m": rv[1] / 1000, "nm_m": nm[0] / 1000, "nm_prior_m": nm[1] / 1000,
         "oi_m": oi[0] / 1000, "oi_prior_m": oi[1] / 1000, "pti_m": pti[0] / 1000, "pti_prior_m": pti[1] / 1000,
         "dist_m": dm, "dist_prior_m": dpm, "eps_q": eps[0], "eps_q_prior": eps[1], "dil_sh_m": round(sh[0] / 1000, 3)}
    if cost is not None:
        r.update({"cost_m": cost[0] / 1000, "cost_prior_m": cost[1] / 1000})
    d = {"quarter": q, "fy": fy, "q": n, "published": SPUB[sid], "source": sid, "release": rel, "release_time": SOURCES[sid]["filed"],
         "raw": r,
         "rows": {"revenues": t_rv, "net_margin": t_nm, "operating_income": t_oi, "pretax": t_pt, "eps": t_e, "shares": t_s, "cash": t_c,
                  **({"distribution": t_d} if t_d else {})},
         "source_title": SOURCES[sid]["title"]}
    d.update({"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": g1(r["rev_prior_m"], r["rev_m"]),
              "nm_pct": g1(r["nm_prior_m"], r["nm_m"]), "dist_pct": g1(dpm, dm) if dm is not None else None,
              "opm": m2(r["oi_m"], r["rev_m"]), "opm_bp": round((m2(r["oi_m"], r["rev_m"]) - m2(r["oi_prior_m"], r["rev_prior_m"])) * 100, 1),
              "ptm": m2(r["pti_m"], r["rev_m"]), "ptm_bp": round((m2(r["pti_m"], r["rev_m"]) - m2(r["pti_prior_m"], r["rev_prior_m"])) * 100, 1),
              "eps_q": r["eps_q"], "eps_q_prior": r["eps_q_prior"], "diluted_shares_m": r["dil_sh_m"],
              "sales_note": f"revenues ${r['rev_m']:,.1f}M vs ${r['rev_prior_m']:,.1f}M a year earlier",
              "nm_note": (f"net margin ${r['nm_m']:,.1f}M vs ${r['nm_prior_m']:,.1f}M"
                          + (" (revenues less cost of sales and fuel: the statement prints no net margin line from the Q4 2015 release)"
                             if cost is not None else "")),
              "dist_note": dnote,
              "margin_note": f"operating income ${r['oi_m']:,.1f}M, income before income taxes {fm(r['pti_m'])}",
              "eps_note": f"diluted {fmt_e(r['eps_q'])} vs {fmt_e(r['eps_q_prior'])} from continuing operations"
                          + ("" if q == "Q4 2013" else " (the natural gas distribution and energy services businesses discontinued from the "
                                                      "Q1 2014 release)"),
              "cash_note": f"cash and cash equivalents ${cash[0] / 1000:,.1f}M at the quarter's end (consolidated)",
              "next_print": NEXT[n]})
    if q == "Q3 2017":
        d["eps_note"] += "; ONEOK Partners' common units it did not own were acquired on June 30, 2017, for ONEOK common stock (in the shares)"
    PR.append(d)


for step in plan:
    if step[0] == "print":
        prt(*step[1:])
# the computed net margin matches the year-ago net margin the earlier releases print (Q4 2014 and Q1-Q3 2015)
for q, qa in (("Q4 2015", "Q4 2014"), ("Q1 2016", "Q1 2015"), ("Q2 2016", "Q2 2015"), ("Q3 2016", "Q3 2015")):
    a, b = next(p for p in PR if p["quarter"] == q), next(p for p in PR if p["quarter"] == qa)
    assert abs(a["raw"]["nm_prior_m"] - b["raw"]["nm_m"]) < 1e-6, (q, a["raw"]["nm_prior_m"], b["raw"]["nm_m"])
# each Q4 print came a trading day before its 10-K, and the week's date (the trading day after the print) is the 10-K's day
for q, fk in (("Q4 2013", "F2013"), ("Q4 2014", "F2014"), ("Q4 2015", "F2015"), ("Q4 2016", "F2016")):
    p = next(x for x in PR if x["quarter"] == q)
    k = SPUB[SID_K[fk]]
    assert p["published"] < k and [d for d in TDAYS if p["published"] < d <= k] == [k], (q, "the 10-K comes the next trading day")
assert [p["published"] for p in PR] == sorted(p["published"] for p in PR)

# ── EPS guides: ONEOK's GAAP net income attributable to ONEOK for the year ─────────────────────────────────────────────────────────
# From 2014 ONEOK guides cash flow available for dividends in ranges in its text and gives net income attributable to ONEOK only in its
# guidance tables, as "midpoints of ranges provided" (2014, 2015) or "~" (2016): read as a point net income guide (lo = hi), over the
# diluted shares of the latest print public on the guide's date (the KMI rule of "OKE 2010-2013"). The FY2017 range of the 8-K of
# 2017-02-02 assumes the pending acquisition of ONEOK Partners effective Jan. 1, 2017 and excludes its one-time fees: a pro forma guide
# of a pending deal, which adds nothing (the XOM XTO and PFE rule; `pro_forma`, text only)
EG = []


def eguide(fy, sid, acc, doc, s, lo, hi, kind, note=None, extra=None, col=1):
    cands = sorted(glob.glob(os.path.join(SP, "*", acc, "EX-9*.rows.txt")) + glob.glob(os.path.join(SP, "*", acc, "8-K__*.rows.txt")))
    hits = [c for c in cands if norm(s) in joined(c)]
    assert hits, (doc, s[:80])
    qt = quote(hits[0], s)
    if extra:
        quote(hits[0], extra)
    g = {"fy": fy, "published": SPUB[sid], "source": sid, "doc": doc, "quote": qt}
    if kind == "range":
        assert f"${lo:.0f} million to ${hi:.0f} million" in qt, (doc, lo, hi)
    elif kind == "table":
        cells = [c.strip() for c in qt.split("|")]
        assert cells[0] == "Net income attributable to ONEOK" and num(cells[col]) == lo == hi, (doc, qt)
    elif kind == "approx":
        assert f"approximately ${lo:.0f} million" in qt and lo == hi, (doc, qt)
    if kind == "pro_forma":
        g["pro_forma_ni_m"] = [lo, hi]
        g["pro_forma_note"] = note
    else:
        g["ni_guide_m"] = [lo, hi]
        if note:
            g["ni_guide_note"] = note
        # the per-share figure: net income over the diluted shares of the latest print public on the guide's date (its own release's
        # where it is in one; the KMI rule)
        allp = old["prints"] + PR
        shp = [p for p in allp if p["published"] <= g["published"]]
        g["shares_print"] = shp[-1]["quarter"]
    EG.append(g)


MID = "*Amounts shown are midpoints of ranges provided."
P = SID_PRINT
G1202 = "0001039684-13-000108"
eguide(2014, SID_8K[G1202], G1202, "8-K of 2013-12-03", "Net income attributable to ONEOK | 285 | 260 | 25", 285, 285, "table",
       "Exhibit A's 2014 guidance column, 'Amounts shown are midpoints of ranges provided.'", MID)
eguide(2014, P["Q3 2014"], "0001039684-14-000083", "Q3 2014 release", "Net income attributable to ONEOK | 316 | 285 | 31", 316, 316, "table",
       "the guidance midpoint table's updated 2014 column, 'Amounts shown are midpoints of ranges provided.'", MID)
G1203 = "0001039684-14-000094"
eguide(2014, SID_8K[G1203], G1203, "8-K of 2014-12-03", "Net income attributable to ONEOK | 393 | 316 | 77", 316, 316, "table",
       "the earnings guidance table's 2014 column (316), 'Amounts shown are midpoints of ranges provided.'", MID, col=2)
eguide(2015, SID_8K[G1203], G1203, "8-K of 2014-12-03", "Net income attributable to ONEOK | 393 | 316 | 77", 393, 393, "table",
       "the earnings guidance table's next-year column, 'Amounts shown are midpoints of ranges provided.'", MID)
eguide(2015, P["Q4 2014"], "0001039684-15-000014", "Q4 2014 release", "Net income attributable to ONEOK | 317 | 393 | (76)", 317, 317,
       "table", "the guidance midpoint table's updated 2015 column, 'Amounts shown are midpoints of ranges provided.'", MID)
G1221 = "0001039684-15-000086"
eguide(2016, SID_8K[G1221], G1221, "8-K of 2015-12-22", "Net income attributable to ONEOK | ~ $360", 360, 360, "table",
       "the guidance table's '~ $360' (approximately)")
eguide(2016, P["Q2 2016"], "0001039684-16-000143", "Q2 2016 release", "Maintaining 2016 net income guidance of approximately $360 million, "
       "cash flow available for dividends guidance of approximately $675 million and dividend coverage ratio guidance of approximately 1.3 "
       "times;", 360, 360, "approx", "approximately")
G0201 = "0001193125-17-027652"
eguide(2017, SID_8K[G0201], G0201, "8-K of 2017-02-02", "Net income (a) (b) | 575 | - | 755", 575, 755, "pro_forma",
       "'(b) | Assumes ONEOK’s acquisition of ONEOK Partners effective Jan. 1, 2017.' and '(a) | Excludes one-time transaction fees "
       "associated with the acquisition of ONEOK Partners.': a guide on the pending acquisition, pro forma, unused (the XOM XTO and PFE rule)",
       "Assumes ONEOK’s acquisition of ONEOK Partners effective Jan. 1, 2017.")
quote(path(G0201, "EX-99.1__*.rows.txt"), "Excludes one-time transaction fees associated with the acquisition of ONEOK Partners.")
eguide(2017, P["Q2 2017"], "0001039684-17-000096", "Q2 2017 release", "ONEOK’s full-year 2017 net income is expected to be in the range of "
       "$635 million to $795 million, compared with its previously announced range of $575 million to $755 million. The updated guidance "
       "reflects the completed merger transaction with ONEOK Partners and nonrecurring and transaction-related charges, which were not "
       "included in ONEOK’s financial guidance provided on Feb. 1, 2017.", 635, 795, "range")
eguide(2017, P["Q3 2017"], "0001039684-17-000115", "Q3 2017 release", "Maintaining 2017 net income guidance of $635 million to $795 million",
       635, 795, "range")
EG.sort(key=lambda g: (g["published"], g["fy"]))
for g in EG:                                     # the doc label carries the date the fact counts from
    if g["doc"].startswith("8-K of"):
        assert g["doc"] == f"8-K of {g['published']}", (g["doc"], g["published"])
# ONEOK Partners' own net income range in the Q2 and Q3 2015 releases is the partnership's (no field)
quote(path("0001039684-15-000057", "EX-99.1__*.rows.txt"), "Reaffirming its 2015 adjusted EBITDA guidance range of $1.51 billion to $1.73 "
      "billion; its DCF guidance range of $1.08 billion to $1.26 billion; and its net income guidance range of $845 million to $1.01 billion "
      "provided on Feb. 23, 2015;")

# ── dividends: each rate change from the first filing that states it as declared ──
DV = []
DIVQ = {"0001039684-14-000004": ("On January 15, 2014, our board of directors approved a cash dividend of 40 cents per share of common stock",
                                 0.40),
        "0001039684-14-000029": ("On April 17, 2014, our board of directors approved a cash dividend of 56 cents per share of common stock",
                                 0.56),
        "0001039684-14-000059": ("On July 23, 2014, our board of directors approved a cash dividend of 57.5 cents per share of common stock",
                                 0.575),
        "0001039684-14-000079": ("On October 22, 2014, our board of directors approved a cash dividend of 59 cents per share of common "
                                 "stock", 0.59),
        "0001039684-15-000006": ("On January 14, 2015, our board of directors approved a cash dividend of 60.5 cents per share of common "
                                 "stock", 0.605),
        "0001039684-15-000070": ("On October 21, 2015, our board of directors approved a cash dividend of 61.5 cents per share of common "
                                 "stock", 0.615),
        "0001039684-17-000092": ("On July 26, 2017, our board of directors approved a cash dividend of 74.5 cents per share of common stock",
                                 0.745)}
for acc, (s, qd) in DIVQ.items():
    sid = SID_DIV[acc]
    qt = quote(path(acc, "8-K__*.rows.txt"), s)
    DV.append({"published": SPUB[sid], "quarterly": qd, "source": sid,
               "note": f"${qd:g} a quarter, ${qd * 4:g} a year: '{qt}' (ONEOK 8-K of {SPUB[sid]})"})
# unchanged rates (read by their text): 2015-04-17 and 2015-07-24 (60.5 cents), 2016-01-22 to 2017-04-21 (61.5 cents), 2017-10-26 (74.5)
for acc, c in (("0001039684-15-000029", "60.5"), ("0001039684-15-000053", "60.5"), ("0001039684-16-000099", "61.5"),
               ("0001039684-16-000121", "61.5"), ("0001039684-16-000141", "61.5"), ("0001039684-16-000155", "61.5"),
               ("0001039684-17-000004", "61.5"), ("0001039684-17-000036", "61.5"), ("0001039684-17-000113", "74.5")):
    assert f"cash dividend of {c} cents per share" in joined(path(acc, "8-K__*.rows.txt")), acc
DV.sort(key=lambda x: x["published"])

# ── the distribution record (the 'distributions' rule of MAR, PFE, BMY, SO, CMCSA and SPGI) ──
YF = {dt.datetime.fromtimestamp(v["date"] + off, dt.timezone.utc).date().isoformat(): v["numerator"] / v["denominator"]
      for v in chart["events"]["splits"].values()}
assert YF["2014-02-03"] == 1.1422
DISTS = [{"effective": "2014-02-03", "yahoo_factor": 1.1422, "source": S_DIST_DONE, "kind": "spin-off",
          "note": (f"the separation of ONE Gas, Inc. (NYSE: OGS): '{DQ2}' (8-K accepted 2014-02-05 after the close, {S_DIST_DONE}; the ratio "
                   f"and the record date were stated in the 8-K of {SPUB[S_DIST_ANN]}, {S_DIST_ANN}: '{DQ1}'); Yahoo books it as an "
                   "11422:10000 split on 2014-02-03, the first day the stock traded without ONE Gas; it is not a split, so from that date "
                   "its factor is undone for the days before it and prices stay as traded (the window's days before it with ONE Gas, the SO "
                   "Mirant reading); per-share facts are not restated, and the history keeps the distribution business until a filing "
                   "restates it (the FY2014 10-K)")}]
assert SPUB[S_DIST_DONE] > "2014-02-03" and not [d for d in TDAYS if "2014-02-03" <= d < SPUB[S_DIST_DONE]
                                                  and dt.date.fromisoformat(d).weekday() == 4], "no weekly date before its source"

# ── assemble ──
for k in ("history_vintages", "prints", "eps_guides", "dividends"):
    assert all(x["published"] <= "2013-12-31" for x in f[k]), k
f["sources"] = {**old["sources"], **dict(sorted(SOURCES.items(), key=lambda kv: int(kv[0][2:])))}
f["history_vintages"] = old["history_vintages"] + V
f["prints"] = old["prints"] + PR
f["eps_guides"] = old["eps_guides"] + EG
f["dividends"] = old["dividends"] + DV
f["distributions"] = DISTS
f["price_basis"] = ("Yahoo OKE, split-adjusted to today's shares: its 2:1 of 2001-06-12 precedes the P/E window (2002-01-01 on) and every "
                    "per-share fact; its 2:1 of 2012-06-04 is the 'splits' record (before it the builder multiplies Yahoo's close by 2, after "
                    "it the per-share facts published before it are halved, on_basis); its 11422:10000 factor of 2014-02-03 (the ONE Gas "
                    "separation) is the 'distributions' record: before it the builder multiplies Yahoo's close by it, and from it the factor "
                    "is undone for the days before it, so every price is the close as traded")
f["_doc"] = old["_doc"].replace("and gen_oke_1013.py (2010-2013)", "gen_oke_1013.py (2010-2013) and gen_oke_1417.py (2014-2017)")
assert "gen_oke_1417.py" in f["_doc"]
assert all(s["published"] <= CUT for s in f["sources"].values())
for k in ("rule_t", "listings", "company_names", "events", "guides", "splits"):
    assert f[k] == old[k], k
out = A.out or os.path.join(REPO, "retro", "facts", "OKE.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(f, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_oke_1417.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump({k: v for k, v in CHECK.items() if v}, fh, ensure_ascii=False, indent=1)
print(f"{out}: +{len(V)} vintages, +{len(PR)} prints, +{len(EG)} EPS guides, +{len(DV)} dividends, +{len(SOURCES)} sources; "
      f"{sum(len(v) for v in CHECK.values())} quotes in {ck}")
for p in PR:
    print(p["quarter"], p["published"], p["sales_pct"], p["nm_pct"], p["dist_pct"], p["opm_bp"], p["ptm_bp"], p["eps_q"], p["eps_q_prior"],
          p["diluted_shares_m"], p["release"])
for g in EG:
    print(g["fy"], g["published"], g["doc"], g.get("ni_guide_m") or g.get("pro_forma_ni_m"), g.get("shares_print"))
for v in V:
    print(v["fy_label"], v["published"], v["eps_normalized"], v["groups"])
