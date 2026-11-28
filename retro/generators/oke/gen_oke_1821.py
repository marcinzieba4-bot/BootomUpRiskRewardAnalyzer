#!/usr/bin/env python3
"""Extend retro/facts/OKE.json with 2018-2021 (filings accepted 2017-12-01 to 2021-12-31), asserting that every earlier fact is
unchanged. Same discipline as gen_oke.py, gen_oke_1013.py and gen_oke_1417.py: each raw figure is read from its own labelled row of a
named table (the row text is kept in the fact and written to the verbatim checklist) or from the sentence that holds it (asserted present
word for word), every rate, margin and change is computed, and every quote is asserted present in its own filing. Only filings accepted on
or before 2021-12-31 are read. The downloads (keep them outside the repo, e.g. the session scratchpad):

    python3 retro/tools/edgar.py index 1039684 <dir>
    python3 retro/tools/edgar.py fetch 1039684 <dir> --from 2017-12-01 --to 2021-12-31 --forms 8-K 8-K/A 10-K 10-K/A 10-Q

    python3 -I retro/generators/oke/gen_oke_1821.py --filings <dir> [--facts-in <2008-2017 sheet>] [--out retro/facts/OKE.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_oke_1821.json

From the Q4 2017 release every earnings release (8-K exhibit 99.1) is a set of page images with a text layer (Workiva slides): its
tables have no cells, so each figure is read from the text layer as converted (`.rows.txt`, one line a page), a label followed by the
table's numbers, and the matched text goes to the checklist (`trow`). The 10-Ks are HTML tables, read by row as before.

--facts-in is the 2008-2017 sheet gen_oke_1417.py writes (default: retro/facts/OKE.json, which must then hold 2008-2017 only).
What the batch reads and decides is in retro/README.md, "OKE 2018-2021".
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
START, CUT = "2018-01-01", "2021-12-31"
CIK = 1039684
ROWS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("OKE")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
old = json.load(open(A.facts_in or os.path.join(REPO, "retro", "facts", "OKE.json"), encoding="utf-8"))
assert all(s["published"] <= "2017-12-31" for s in old["sources"].values()), "--facts-in must be the 2008-2017 sheet"
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
    t = t.replace(",", "").replace("$", "").replace("~", "").replace(" ", "").strip()
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


TNUM = r"(?:\$ ?)?(?:\( ?[\d,]+(?:\.\d+)? ?\)|[\d,]+(?:\.\d+)?|—)"


def trow(p, label, anchor, n, after=None):
    """A row of a release's text layer (the slides have no table cells): the first `label` at or after `anchor` (then `after`) that is
    followed by exactly n numbers (a footnote mark such as '(a)' may follow the label); returns (numbers, the matched text, which goes to the checklist)."""
    t = joined(p)
    i = re.search(anchor, t).start()
    if after:
        i = re.compile(after).search(t, i).start()
    m = re.compile(rf"(?:(?<= )|^)(?:{label})(?: \([a-z]\))? ((?:{TNUM} ){{{n - 1}}}{TNUM})(?= (?!{TNUM}(?: |$))|$)").search(t, i)
    assert m, (os.path.basename(p), label, anchor)
    vals = [num(x) for x in re.findall(r"\( ?[\d,]+(?:\.\d+)? ?\)|[\d,]+(?:\.\d+)?|—", m.group(1))]
    assert len(vals) == n, (os.path.basename(p), label, m.group(0))
    CHECK.setdefault(p, []).append(m.group(0))
    return vals, m.group(0)


def pub(acc):
    """The date a filing counts from (the acceptance-time rule): EDGAR's UTC time in ET; at or after 16:00, or on a day the market is
    closed, the next trading day."""
    r = ROWS[acc]
    t = dt.datetime.fromisoformat(r[1].replace("Z", "+00:00")).astimezone(ET)
    day = t.date().isoformat()
    if day not in TDAYS:          # (2019-04-19, Good Friday: the market closed; the UNP Good Friday rule)
        day = min(d for d in TDAYS if d > day)
        when = f"accepted {t:%Y-%m-%d %H:%M} ET, a market holiday: counts from {day}"
    elif (t.hour, t.minute) >= (16, 0):
        day = min(d for d in TDAYS if d > day)
        when = f"accepted {t:%Y-%m-%d %H:%M} ET, after the close: counts from {day}"
    elif (t.hour, t.minute) < (9, 30):
        when = f"accepted {t:%Y-%m-%d %H:%M} ET, before the open"
    else:
        when = f"accepted {t:%Y-%m-%d %H:%M} ET, during the session"
    assert START <= day <= CUT, (acc, day)
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

# ── the 10-Ks: the FY2017-FY2020 vintages ─────────────────────────────────────────────────────────────────────────────────────────
K = {"F2017": "0001039684-18-000021", "F2018": "0001039684-19-000016", "F2019": "0001039684-20-000012", "F2020": "0001039684-21-000015"}
DK = {k: path(a, "10-K__*.rows.txt") for k, a in K.items()}
REL = lambda acc: path(acc, "EX-99.1__*.rows.txt")

# ── sources, in date order ───────────────────────────────────────────────────────────────────────────────────────────────────────
G18, MAR20 = "0001039684-18-000008", "0001039684-20-000018"
plan = [("div", "0001039684-18-000004", 0.77),
        ("guide8k", G18, "ONEOK 8-K: 2018 financial guidance (Items 7.01, 9.01)"),
        ("print", "Q4 2017", 2017, 4, "0001039684-18-000018"),
        ("k", "F2017"),
        ("div", "0001039684-18-000030", 0.795),
        ("print", "Q1 2018", 2018, 1, "0001039684-18-000032"),
        ("div", "0001039684-18-000051", 0.825),
        ("print", "Q2 2018", 2018, 2, "0001039684-18-000054"),
        ("div", "0001039684-18-000074", 0.855),
        ("print", "Q3 2018", 2018, 3, "0001039684-18-000076"),
        ("div", "0001039684-19-000004", 0.86),
        ("print", "Q4 2018", 2018, 4, "0001039684-19-000014"),
        ("k", "F2018"),
        ("div", "0001039684-19-000024", 0.865),
        ("print", "Q1 2019", 2019, 1, "0001039684-19-000028"),
        ("div", "0001039684-19-000050", 0.89),
        ("print", "Q2 2019", 2019, 2, "0001039684-19-000054"),
        ("div", "0001039684-19-000071", 0.915),
        ("print", "Q3 2019", 2019, 3, "0001039684-19-000074"),
        ("div", "0001039684-20-000004", 0.935),
        ("print", "Q4 2019", 2019, 4, "0001039684-20-000010"),
        ("k", "F2019"),
        ("guide8k", MAR20, "ONEOK 8-K: a $500 million decrease in 2020 capital spending (Items 7.01, 9.01)"),
        ("print", "Q1 2020", 2020, 1, "0001039684-20-000033"),
        ("print", "Q2 2020", 2020, 2, "0001039684-20-000054"),
        ("print", "Q3 2020", 2020, 3, "0001039684-20-000073"),
        ("print", "Q4 2020", 2020, 4, "0001039684-21-000010"),
        ("k", "F2020"),
        ("print", "Q1 2021", 2021, 1, "0001039684-21-000032"),
        ("print", "Q2 2021", 2021, 2, "0001039684-21-000054"),
        ("print", "Q3 2021", 2021, 3, "0001039684-21-000069")]
SID_PRINT, SID_8K, SID_DIV, SID_K, ACC_PRINT = {}, {}, {}, {}, {}
for step in plan:
    if step[0] == "print":
        _, q, fy, n, acc = step
        ACC_PRINT[q] = acc
        SID_PRINT[q] = src(acc, f"ONEOK {q} results (8-K exhibit 99.1)",
                           f"{q}: revenues, cost of sales and fuel (net margin), operating income, income before income taxes, diluted EPS, "
                           "diluted shares; the net income guidance where the release gives one")
    elif step[0] == "guide8k":
        SID_8K[step[1]] = src(step[1], step[2], "the net income guidance it states")
    elif step[0] == "div":
        SID_DIV[step[1]] = src(step[1], f"ONEOK 8-K: quarterly dividend of ${step[2]:g} (Items 7.01, 8.01)",
                               f"the quarterly dividend rate, ${step[2]:g} a share")
    elif step[0] == "k":
        SID_K[step[1]] = src(K[step[1]], f"ONEOK {step[1].replace('F', 'FY')} 10-K", f"history vintage {step[1].replace('F', 'FY')}; the 'why'")
srt_src = sorted(SOURCES.items(), key=lambda kv: (kv[1]["published"], int(kv[0][2:])))
assert [k for k, _ in srt_src] == sorted(SOURCES, key=lambda k: int(k[2:])), "source ids must follow publication order"
SPUB = {**{k: v["published"] for k, v in old["sources"].items()}, **{k: v["published"] for k, v in SOURCES.items()}}

# ── history vintages: each year from the latest filing that reports it; the ten fiscal years to the latest one ─────────────────────
V16 = old["history_vintages"][-1]                     # the FY2016 vintage (2014-2017 sheet)
assert V16["fy_label"] == "FY16"
ST = r"^CONSOLIDATED STATEMENTS OF INCOME$"
I6 = r"^ITEM 6\.( \|)? SELECTED FINANCIAL DATA$"


def stmt(fk, label, n=3, after=None):
    return row(DK[fk], label, ST, after, n=n)


LEAD17 = ("We are a leading midstream service provider and own one of the nation’s premier natural gas liquids systems, connecting NGL "
          "supply in the Mid-Continent, Permian and Rocky Mountain regions with key market centers and an extensive network of natural "
          "gas gathering, processing, storage and transportation assets.")
LEAD19 = ("We are a leading midstream service provider and own one of the nation’s premier NGL systems, connecting NGL supply in the "
          "Rocky Mountain, Permian and Mid-Continent regions with key market centers and an extensive network of natural gas gathering, "
          "processing, storage and transportation assets.")
VOL = "The volatility of natural gas, crude oil and NGL prices could affect adversely our earnings and cash flows."
FEE = {"F2017": "We operate primarily fee-based businesses in each of our three reportable segments.",
       "F2018": "We operate primarily fee-based businesses in each of our three reportable segments, and our consolidated earnings were "
                "nearly 90 percent fee-based in 2018.",
       "F2019": "We operate primarily fee-based businesses in each of our three reportable segments, and our consolidated earnings were "
                "approximately 90% fee-based in 2019.",
       "F2020": "Each of our three segments’ earnings are primarily fee-based, and our consolidated earnings were more than 90% fee-based "
                "in 2020."}
GHG = "We may face significant costs to comply with the regulation of GHG emissions."
RES = {"F2017": ("We generally contract with crude oil and natural gas producers who have proven reserves or are currently producing "
                 "natural gas in areas within our existing infrastructure and need gathering and processing services."),
       "F2018": ("We may not be able to accurately estimate hydrocarbon reserves and production volumes expected to be delivered to us for "
                 "a variety of reasons, including the unavailability of sufficiently detailed information and unanticipated changes in "
                 "producers’ expected drilling schedules.")}
RES["F2019"] = RES["F2020"] = RES["F2018"]
DEMAND = ("Changes in regulatory policies, public sentiment or technology due to the threat of climate change that result in a reduction "
          "in the demand for hydrocarbon products, restrictions on their use, or increased use of renewable energy could reduce future "
          "demand for hydrocarbons and reduce volumes available to us for gathering, processing, fractionation, transportation, storage "
          "and marketing.")
BL = ("a midstream service provider: natural gas gathering and processing, natural gas liquids and natural gas pipelines (ONEOK Partners' "
      "common units it did not own acquired for ONEOK common stock on June 30, 2017)")
KT = "A midstream service provider"


def why(fk):
    lo = joined(DK[fk]).lower()
    # DURABLE needs the company not to call its own business cyclical (the MU rule): no FY2017-FY2020 10-K uses the word
    assert "cyclical" not in lo, (fk, "a 10-K that uses the word cyclical")
    lead = LEAD17 if fk in ("F2017", "F2018") else LEAD19
    q = [quote(DK[fk], lead), quote(DK[fk], FEE[fk]), quote(DK[fk], VOL)]
    return " ".join(f"'{x}'" for x in q) + (f" (the {fk.replace('F', 'FY')} 10-K's own words; it does not use the word cyclical, so "
                                            "DURABLE, the MU rule)")


def themes(fk):
    """The 10-K's own words the builder quotes beside a live theme's scope (text only): the GHG risk factor, the producers' reserves
    (ONEOK holds none of its own), and from the FY2019 10-K the climate-demand risk factor; no 10-K names electric vehicles or crypto."""
    t = joined(DK[fk])
    out = {"ENERGY_TRANSITION_ghg": quote(DK[fk], GHG), "ENERGY_TRANSITION_reserves": quote(DK[fk], RES[fk])}
    if norm(DEMAND) in t:
        out["ENERGY_TRANSITION_demand"] = quote(DK[fk], DEMAND)
    assert (fk in ("F2019", "F2020")) == ("ENERGY_TRANSITION_demand" in out), fk
    for w in ("electric vehicle", "crypto", "blockchain", "bitcoin", "digital asset", "cloud"):
        assert w not in t.lower(), (fk, w)
    return out


def groups(fk, fy):
    """Segment revenues, the last year and the one before, by the segment note's own column heads (Other, eliminations and totals left
    out): sales to unaffiliated customers in the FY2017 10-K; from the FY2018 10-K the note prints no such row (ASC 606's
    disaggregated revenues), so each segment's total revenues, intersegment revenues in, both years."""
    lab = r"Sales to unaffiliated customers" if fk == "F2017" else r"Total revenues( \(c\))?"
    out = {}
    ls = lines(DK[fk])
    for y in (fy, fy - 1):
        k = next(i for i, l in enumerate(ls) if l.startswith(f"Year Ended December 31, {y} |") and "Gathering" in l)
        heads = [c.strip() for c in ls[k].split("|")[1:]]
        r = next(l for l in ls[k:k + 12] if re.match(lab + r" \|", l))
        CHECK.setdefault(DK[fk], []).append(r)
        vals = [num(c) for c in r.split("|")[1:] if c.strip()]
        assert len(vals) == len(heads), (fk, y, heads, vals)
        out[y] = {h: v for h, v in zip(heads, vals) if not re.search(r"(?i)^(Other|Total)", h)}
    name = lambda h: re.sub(r"\s*\([a-z]\)$", "", re.sub(r"(?<=[a-z])(?=[A-Z])", " ", h))
    return [[name(h), round(v / 1e6, 3), pct1(out[fy - 1][h], v)] for h, v in out[fy].items()]


def vintage(fk, fy, eps, rev, sh, div_sentence, div_q, restate_note, pretax_note):
    """eps / rev / sh: {year: (value, source id)}; the per-year sources give each year's publication date (on_basis)."""
    st = {"rev": stmt(fk, r"Total revenues( \(Note [A-Z]\))?")[0], "oi": stmt(fk, r"Operating income")[0],
          "pti": stmt(fk, r"Income before income taxes")[0], "tax": [abs(x) for x in stmt(fk, r"Income taxes( \(Note [A-Z]\))?")[0]]}
    cf = r"^CONSOLIDATED STATEMENTS OF CASH FLOWS( \||$)"
    cfo = row(DK[fk], r"Cash provided by operating activities", cf, n=3)[0]
    cx = [abs(x) for x in row(DK[fk], r"Capital expenditures \(less allowance for equity funds used during construction\)", cf, n=3)[0]]
    iss = row(DK[fk], r"Issuance of common stock", cf, n=3)[0]
    assert not [l for l in lines(DK[fk]) if l.startswith("Repurchase of common stock")], (fk, "a repurchase line")
    cash_return = (f"no repurchase of common stock in {fy} (the FY{fy} 10-K's statement of cash flows has no repurchase line); issuance of "
                   f"common stock ${iss[0] / 1000:,.1f}M")
    sid = SID_K[fk]
    years = sorted(eps)
    assert years == list(range(years[0], fy + 1)) and len(years) == 10, (fk, years)
    first = years[0]
    return {
        "published": SPUB[sid], "sources": sorted({sid} | {s for _, s in eps.values()} | {s for _, s in rev.values()}
                                                 | {s for _, s in sh.values()}, key=lambda s: -int(s[2:])),
        "company": "ONEOK, Inc.", "exchange": "NYSE", "symbol": "OKE",
        "business_line": BL,
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
        "normalization": V16["normalization"].split("; 2012-2016 from the FY2016 10-K")[0] + "; " + restate_note,
        "pe_window_start": f"{first}-01-01",
        "prev_fy_op_margin": m2(st["oi"][0], st["rev"][0]),
        "prev_fy_op_margin_note": (f"FY{fy % 100:02d} operating income ${st['oi'][0] / 1000:,.1f}M / revenues ${st['rev'][0] / 1000:,.1f}M "
                                   f"(FY{fy} 10-K), the operating margin"),
        "check_pretax_margin": m2(st["pti"][0], st["rev"][0]),
        "check_pretax_note": (f"FY{fy % 100:02d} income before income taxes ${st['pti'][0] / 1000:,.1f}M / revenues ${st['rev'][0] / 1000:,.1f}M "
                              f"(FY{fy} 10-K); {pretax_note}"),
        "tax_rate": round(st["tax"][0] / st["pti"][0], 4),
        "tax_note": (f"FY{fy % 100:02d} income taxes ${st['tax'][0] / 1000:,.1f}M / income before income taxes ${st['pti'][0] / 1000:,.1f}M "
                     f"(FY{fy} 10-K)"),
        "prev_fy_sales_growth": pct1(st["rev"][1], st["rev"][0]),
        "dividend_annual": round(div_q * 4, 3),
        "dividend_note": f"${div_q:g} a quarter, ${div_q * 4:g} a year: '{quote(DK[fk], div_sentence)}' (FY{fy} 10-K)",
        "fcf_label": f"FY{fy % 100:02d}", "fcf_b": round((cfo[0] - cx[0]) / 1e6, 3),
        "fcf_note": (f"cash provided by operating activities ${cfo[0] / 1000:,.1f}M less capital expenditures ${cx[0] / 1000:,.1f}M "
                     f"(FY{fy} 10-K, consolidated)"),
        "cash_return_text": cash_return,
        "groups": groups(fk, fy),
        "groups_basis": (f"FY{fy % 100:02d} segment sales to unaffiliated customers (FY{fy} 10-K segment note; eliminations and Other left "
                         "out)" if fk == "F2017" else
                         f"FY{fy % 100:02d} segment total revenues, intersegment revenues included (FY{fy} 10-K segment note, which prints "
                         "no sales to unaffiliated customers from the FY2018 10-K; eliminations and Other left out)"),
        "margin_signal_name": "Pre-tax margin change",
        "kind": "DURABLE", "kind_text": KT,
        "why": why(fk),
        "theme_quotes": themes(fk),
        # (OKE 2018-2021) after the ONEOK Partners merger the reserves reading names ONEOK itself; the words no 10-K uses (asserted)
        "theme_holder": "ONEOK",
        "theme_absent": ["electric vehicle", "crypto"],
    }


c_eps = {int(y): (v, V16["eps_sources"][y]) for y, v in V16["eps_normalized"].items()}
c_rev = {int(y): (v, V16["revenue_sources"][y]) for y, v in V16["revenue_usd_b"].items()}
c_sh = {int(y): (v, V16["shares_sources"][y]) for y, v in V16["diluted_shares_m"].items()}
V = []
NCI = "the noncontrolling interests (ONEOK Partners' public unitholders to June 30, 2017) and preferred dividends come after it, so the check overstates ONEOK's own EPS"
NCI2 = "the noncontrolling interests and preferred dividends (under $5 million) come after it, so the check slightly overstates ONEOK's own EPS"

# FY2017 10-K (2018-02-28): 2013-2017 from Item 6, 'Earnings per share - continuing operations'; 2015-2017 statements
e, _ = row(DK["F2017"], r"Diluted", I6, r"^Earnings per share - continuing operations$")
assert e == [1.29, 1.67, 1.19, 1.52, 1.33], e
r, _ = stmt("F2017", r"Total revenues")
s, _ = stmt("F2017", r"Diluted", after=r"(?i)^Average shares")
S17 = SID_K["F2017"]
eps17 = {**c_eps, **{y: (e[2017 - y], S17) for y in range(2013, 2018)}}
rev17 = {**c_rev, 2015: (r[2], S17), 2016: (r[1], S17), 2017: (r[0], S17)}
sh17 = {**c_sh, 2015: (s[2], S17), 2016: (s[1], S17), 2017: (s[0], S17)}
for d in (eps17, rev17, sh17):
    del d[2007]
# FY2017's listed items (the Q4 2017 release): the Tax Cuts and Jobs Act's $141.3M (47 cents for the year), the $20.2M impairments
# (4 cents) and about $50M of merger-related costs (10 cents): 61 cents against $1.29, so reported EPS is above half the year's EPS
# without them ($1.90), and no filing publishes a full-year EPS without them: kept at GAAP (the AAPL FY2002 test; the LYB, UNH and CB
# reading of the Tax Act)
Q17 = quote(REL("0001039684-18-000018"), "Three-month and full-year periods ending Dec. 31, 2017, include one-time noncash charges of $141.3 "
            "million, or 36 cents per diluted share and 47 cents per diluted share, respectively, related to the enactment of the Tax Cuts "
            "and Jobs Act. The full-year ending Dec. 31, 2017, also includes noncash impairment charges of approximately $20.2 million, or 4 "
            "cents per diluted share, and approximately $50 million, or 10 cents per diluted share, in one-time and ONEOK and ONEOK Partners "
            "merger transaction-related costs.")
assert round(1.29 + 0.47 + 0.04 + 0.10, 2) == 1.90 and 1.29 > 1.90 / 2
V.append(vintage("F2017", 2017, eps17, rev17, sh17,
                 "In February 2018, we paid a quarterly dividend of $0.77 per share ($3.08 per share on an annualized basis), an increase of "
                 "25 percent compared with the same quarter in the prior year.", 0.77,
                 "2013-2017 from the FY2017 10-K's Item 6, 'Earnings per share - continuing operations'; 2017 at GAAP $1.29, on the year's "
                 f"299.8M diluted shares (ONEOK Partners' public units exchanged for 168.9M ONEOK shares on June 30, 2017): its listed items "
                 f"('{Q17}', the Q4 2017 release) are 61 cents a diluted share against $1.90 without them, under half, and no filing "
                 "publishes a full-year EPS without them; the ten fiscal years to the latest one, so 2007 leaves and the window starts "
                 "with 2008", NCI))
# FY2018 10-K (2019-02-27): Item 6 prints 'Earnings per share - total' only, so 2016-2018 from the statement of income's diluted EPS
# from continuing operations (2017-2018 have no discontinued operations; 2016's $1.67 as before), 2014-2015 kept from the FY2017 10-K
# (the latest filing that reports their EPS from continuing operations); ASC 606 from 2018 without restatement (a seam, as published)
i6, _ = row(DK["F2018"], r"Diluted", I6, r"^Earnings per share - total$")
assert i6 == [2.78, 1.29, 1.66, 1.16, 1.49], i6
e, _ = stmt("F2018", r"Income from continuing operations \(Note I\)", after=r"^Diluted earnings per common share:$")
assert e == [2.78, 1.29, 1.67], e
r, _ = stmt("F2018", r"Total revenues")
s, _ = stmt("F2018", r"Diluted", after=r"(?i)^Average shares")
S18 = SID_K["F2018"]
eps18 = {**eps17, **{y: (e[2018 - y], S18) for y in range(2016, 2019)}}
rev18 = {**rev17, 2016: (r[2], S18), 2017: (r[1], S18), 2018: (r[0], S18)}
sh18 = {**sh17, 2016: (s[2], S18), 2017: (s[1], S18), 2018: (s[0], S18)}
for d in (eps18, rev18, sh18):
    del d[2008]
QASC = quote(DK["F2018"], "In 2017 and prior periods, these fees were recorded as services revenue.")
V.append(vintage("F2018", 2018, eps18, rev18, sh18,
                 "In February 2019, we paid a quarterly dividend of $0.86 per share ($3.44 per share on an annualized basis), an increase of "
                 "12 percent compared with the same quarter in the prior year.", 0.86,
                 "2016-2018 from the FY2018 10-K's statement of income, diluted EPS from continuing operations (its Item 6 prints EPS - "
                 "total only; 2017 and 2018 have no discontinued operations), 2014-2015 from the FY2017 10-K's Item 6; 2018 at GAAP $2.78 "
                 "(no listed item); revenues on ASC 606 from 2018 without restatement ('" + QASC + "', a seam, as published); the ten fiscal "
                 "years to the latest one, so 2008 leaves and the window starts with 2009", NCI2))
# FY2019 10-K (2020-02-26): 2017-2019 from the statement of income (no discontinued operations), earlier years carried
i6, _ = row(DK["F2019"], r"Diluted", I6, r"^Earnings per share - total$")
assert i6 == [3.07, 2.78, 1.29, 1.66, 1.16], i6
e, _ = stmt("F2019", r"Diluted earnings per common share \(Note I\)")
assert e == [3.07, 2.78, 1.29], e
r, _ = stmt("F2019", r"Total revenues \(Note P\)")
s, _ = stmt("F2019", r"Diluted", after=r"(?i)^Average shares")
S19 = SID_K["F2019"]
eps19 = {**eps18, **{y: (e[2019 - y], S19) for y in range(2017, 2020)}}
rev19 = {**rev18, 2017: (r[2], S19), 2018: (r[1], S19), 2019: (r[0], S19)}
sh19 = {**sh18, 2017: (s[2], S19), 2018: (s[1], S19), 2019: (s[0], S19)}
for d in (eps19, rev19, sh19):
    del d[2009]
V.append(vintage("F2019", 2019, eps19, rev19, sh19,
                 "In February 2020, we paid a quarterly dividend of $0.935 per share ($3.74 per share on an annualized basis), an increase "
                 "of 9% compared with the same quarter in the prior year.", 0.935,
                 "2017-2019 from the FY2019 10-K's statement of income (no discontinued operations); 2019 at GAAP $3.07 (no listed item); "
                 "the ten fiscal years to the latest one, so 2009 (the last year with the distribution business in) leaves and the window "
                 "starts with 2010", NCI2))
# FY2020 10-K (2021-02-24): 2018-2020 from the statement of income; 2020 at GAAP $1.42 with the impairments: its listed items (the Q4
# 2020 release) are $1.15 a diluted share of charges and 6 cents of benefits, $1.09 net against $2.51 without them, under half, and no
# filing publishes a full-year EPS without them (the Q1 2020 release's 83 cents is the quarter's)
i6, _ = row(DK["F2020"], r"Diluted", I6, r"^EPS - total$")
assert i6 == [1.42, 3.07, 2.78, 1.29, 1.66], i6
e, _ = stmt("F2020", r"Diluted EPS \(Note I\)")
assert e == [1.42, 3.07, 2.78], e
r, _ = stmt("F2020", r"Total revenues \(Note P\)")
s, _ = stmt("F2020", r"Diluted", after=r"(?i)^Average shares")
S20 = SID_K["F2020"]
eps20 = {**eps19, **{y: (e[2020 - y], S20) for y in range(2018, 2021)}}
rev20 = {**rev19, 2018: (r[2], S20), 2019: (r[1], S20), 2020: (r[0], S20)}
sh20 = {**sh19, 2018: (s[2], S20), 2019: (s[1], S20), 2020: (s[0], S20)}
for d in (eps20, rev20, sh20):
    del d[2010]
Q20 = quote(REL("0001039684-21-000010"), "Amounts for the year ended Dec. 31, 2020, include benefits of $22.3 million, or 4 cents per diluted "
            "share after-tax, related to net gains on open market repurchases of debt and $11.2 million, or 2 cents per diluted share "
            "after-tax, related to the mark- to-market of ONEOK’s share-based compensation plan, and noncash charges of $644.9 million, or "
            "$1.15 per diluted share after-tax, related primarily to impairments in the natural gas gathering and processing segment.")
assert round(1.42 + 1.15 - 0.04 - 0.02, 2) == 2.51 and 1.42 > 2.51 / 2 and 1.42 > (1.42 + 1.15) / 2
V.append(vintage("F2020", 2020, eps20, rev20, sh20,
                 "In February 2021, we maintained and paid a quarterly dividend of $0.935 per share ($3.74 per share on an annualized "
                 "basis), which is consistent with the same quarter in the prior year.", 0.935,
                 "2018-2020 from the FY2020 10-K's statement of income; 2020 at GAAP $1.42: its listed items ('" + Q20 + "', the Q4 2020 "
                 "release) are $1.09 a diluted share net ($1.15 of charges alone) against $2.51 without them, under half, and no filing "
                 "publishes a full-year EPS without them (the Q1 2020 release's 83 cents excluding the impairments is the quarter's); the "
                 "ten fiscal years to the latest one, so 2010 leaves and the window starts with 2011", NCI2))
for v in V:
    assert all(v["eps_published"][y] <= v["published"] for y in v["eps_normalized"])
assert [v["pe_window_start"] for v in V] == ["2008-01-01", "2009-01-01", "2010-01-01", "2011-01-01"]

# ── the prints (text layer) ──────────────────────────────────────────────────────────────────────────────────────────────────────
NEXT = {1: "Q2 print (late July or early August)", 2: "Q3 print (late October or early November)",
        3: "Q4 and full-year print, with the 10-K (late February)", 4: "Q1 print (late April or early May)"}
PR = []
SI = r"CONSOLIDATED STATEMENTS OF INCOME"
BS = r"CONSOLIDATED BALANCE SHEETS"


def fmt_e(x):
    return f"${x:.2f}" if x >= 0 else f"$({-x:.2f})"


def fm(x):
    return f"${x:,.1f}M" if x >= 0 else f"$({-x:,.1f})M"


def prt(q, fy, n, acc):
    sid = SID_PRINT[q]
    p = REL(acc)
    t = joined(p)
    m = re.search(r"TULSA, Okla\. ?[–-]+ ?(\w+)\.? (\d+), (\d{4})", t)
    rel = f"{m.group(1)[:3]} {int(m.group(2))}"
    k = 2 if n == 1 else 4                       # Q1: the quarter only; Q2-Q4: the quarter and the year to date
    rv, t_rv = trow(p, r"Total revenues", SI, k)
    cost, t_nm = trow(p, r"Cost of sales and fuel \(exclusive of items shown separately below\)", SI, k)
    oi, t_oi = trow(p, r"Operating income(?: \(loss\))?", SI, k)
    pti, t_pt = trow(p, r"Income(?: \(loss\))? before income taxes", SI, k)
    if q == "Q4 2017":       # the last release with a discontinued operations line (2016's)
        eps, t_e = trow(p, r"Income from continuing operations", SI, k, after=r"Diluted earnings per common share:")
    else:
        eps, t_e = trow(p, r"Diluted (?:earnings(?: \(loss\))? per common share|EPS)", SI, k)
    sh, t_s = trow(p, r"Diluted", SI, k, after=r"Average shares \(thousands\)")
    cash, t_c = trow(p, r"Cash and cash equivalents", BS, 2)
    assert not re.search(r"(?i)\b(Natural Gas )?Distribution segment", t), (q, "a Distribution segment")
    nm = [a - b for a, b in zip(rv, cost)]
    r = {"rev_m": rv[0] / 1000, "rev_prior_m": rv[1] / 1000, "nm_m": nm[0] / 1000, "nm_prior_m": nm[1] / 1000,
         "oi_m": oi[0] / 1000, "oi_prior_m": oi[1] / 1000, "pti_m": pti[0] / 1000, "pti_prior_m": pti[1] / 1000,
         "dist_m": None, "dist_prior_m": None, "eps_q": eps[0], "eps_q_prior": eps[1], "dil_sh_m": round(sh[0] / 1000, 3),
         "cost_m": cost[0] / 1000, "cost_prior_m": cost[1] / 1000}
    d = {"quarter": q, "fy": fy, "q": n, "published": SPUB[sid], "source": sid, "release": rel, "release_time": SOURCES[sid]["filed"],
         "raw": r,
         "rows": {"revenues": t_rv, "net_margin": t_nm, "operating_income": t_oi, "pretax": t_pt, "eps": t_e, "shares": t_s, "cash": t_c},
         "source_title": SOURCES[sid]["title"]}
    d.update({"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": g1(r["rev_prior_m"], r["rev_m"]),
              "nm_pct": g1(r["nm_prior_m"], r["nm_m"]), "dist_pct": None,
              "opm": m2(r["oi_m"], r["rev_m"]), "opm_bp": round((m2(r["oi_m"], r["rev_m"]) - m2(r["oi_prior_m"], r["rev_prior_m"])) * 100, 1),
              "ptm": m2(r["pti_m"], r["rev_m"]), "ptm_bp": round((m2(r["pti_m"], r["rev_m"]) - m2(r["pti_prior_m"], r["rev_prior_m"])) * 100, 1),
              "eps_q": r["eps_q"], "eps_q_prior": r["eps_q_prior"], "diluted_shares_m": r["dil_sh_m"],
              "sales_note": f"revenues ${r['rev_m']:,.1f}M vs ${r['rev_prior_m']:,.1f}M a year earlier"
                            + (" (2018 on ASC 606, 2017 as first reported: a seam, as published)" if fy == 2018 else ""),
              "nm_note": f"net margin ${r['nm_m']:,.1f}M vs ${r['nm_prior_m']:,.1f}M (revenues less cost of sales and fuel)",
              "dist_note": "Distribution operating income n/r (the natural gas distribution business separated as ONE Gas on January 31, 2014)",
              "margin_note": f"operating income {fm(r['oi_m'])}, income before income taxes {fm(r['pti_m'])}",
              "eps_note": f"diluted {fmt_e(r['eps_q'])} vs {fmt_e(r['eps_q_prior'])}"
                          + (" from continuing operations" if q == "Q4 2017" else " (no discontinued operations)"),
              "cash_note": f"cash and cash equivalents ${cash[0] / 1000:,.1f}M at the quarter's end (consolidated)",
              "next_print": NEXT[n]})
    if q == "Q4 2017":
        d["eps_note"] += "; the quarter's $0.36 of Tax Cuts and Jobs Act charges in"
    if q in ("Q1 2020", "Q2 2020", "Q3 2020"):
        d["eps_note"] += "; the year includes $641.8 million of noncash impairment charges in the first quarter"
    PR.append(d)


for step in plan:
    if step[0] == "print":
        prt(*step[1:])
# the year-ago figures each release prints are the earlier print's own (recast lines excepted: ASU 2017-07 moved pension costs out of
# operating income from 2018, so the year-ago operating income differs from 2018-2019; revenues, cost and EPS agree)
allp = {p["quarter"]: p for p in old["prints"] + PR}
for p in PR:
    qa = f"{p['quarter'][:2]} {p['fy'] - 1}"
    a = allp[qa]
    assert abs(p["raw"]["rev_prior_m"] - a["raw"]["rev_m"]) < 1e-6 and p["raw"]["eps_q_prior"] == a["raw"]["eps_q"], (p["quarter"], qa)
# each Q4 print came a trading day before its 10-K, and the week's date (the trading day after the print) is the 10-K's day
for q, fk in (("Q4 2017", "F2017"), ("Q4 2018", "F2018"), ("Q4 2019", "F2019"), ("Q4 2020", "F2020")):
    p = next(x for x in PR if x["quarter"] == q)
    k = SPUB[SID_K[fk]]
    assert p["published"] < k and [d for d in TDAYS if p["published"] < d <= k] == [k], (q, "the 10-K comes the next trading day")
assert [p["published"] for p in PR] == sorted(p["published"] for p in PR)

# ── EPS guides: ONEOK's GAAP net income for the year ─────────────────────────────────────────────────────────────────────────────────
# ONEOK guides "Net income" in dollars (from 2018 consolidated net income, the noncontrolling interests and preferred dividends under
# $5 million a year) and, from the 2020 guidance, also "Diluted earnings per common share": the per-share figure where stated, else net
# income over the diluted shares of the latest print public on the guide's date (its own release's where it is in one; the KMI rule of
# "OKE 2010-2013"); a range restated in words keeps the last range; a numeric range restated in a later release is a guide of that
# release (the Q1 2018 and Q2 2021 maintained ranges, the Q3 2020 restated outlook, as the Q3 2017 one).
EG = []


def eguide(fy, sid, acc, doc, s, kind, lo=None, hi=None, note=None, extra=()):
    p = REL(acc)
    qt = quote(p, s)
    for x in extra:
        quote(p, x)
    g = {"fy": fy, "published": SPUB[sid], "source": sid, "doc": doc, "quote": qt}
    if kind == "words":
        g["words"] = True
    elif kind == "eps":
        g["eps_guide"] = [lo, hi]
        if note:
            g["eps_guide_note"] = note
    else:
        g["ni_guide_m"] = [lo, hi]
        if note:
            g["ni_guide_note"] = note
        shp = [p for p in old["prints"] + PR if p["published"] <= g["published"]]
        g["shares_print"] = shp[-1]["quarter"]
    EG.append(g)


P = SID_PRINT
A_ = ACC_PRINT
eguide(2018, SID_8K[G18], G18, "8-K of 2018-01-24", "ONEOK’s full-year 2018 net income is expected to be in the range of $955 million to "
       "$1.155 billion.", "ni", 955, 1155)
eguide(2018, P["Q1 2018"], A_["Q1 2018"], "Q1 2018 release", "Maintaining 2018 net income guidance of $955 million to $1,155 million", "ni",
       955, 1155)
eguide(2018, P["Q2 2018"], A_["Q2 2018"], "Q2 2018 release", "ONEOK increases its 2018 net income guidance midpoint to $1,085 million from "
       "$1,055 million and its adjusted EBITDA guidance midpoint to $2,350 million from $2,315 million, and narrows its 2018 financial "
       "guidance ranges.", "ni", 1020, 1150, extra=["Net income $ 1,020 - $ 1,150"])
eguide(2018, P["Q3 2018"], A_["Q3 2018"], "Q3 2018 release", "ONEOK’s full-year 2018 net income is expected to be in the range of $1,140 "
       "million to $1,220 million, compared with the range of $1,020 million to $1,150 million announced July 31, 2018.", "ni", 1140, 1220)
eguide(2019, P["Q4 2018"], A_["Q4 2018"], "Q4 2018 release", "2019 Guidance Range (Millions of dollars) ONEOK, Inc. Net income $ 1,140 - $ "
       "1,400", "ni", 1140, 1400)
eguide(2019, P["Q2 2019"], A_["Q2 2019"], "Q2 2019 release", "we feel confident in achieving our 2019 financial guidance", "words",
       extra=["Maintains 2019 Financial Guidance"])
eguide(2019, P["Q3 2019"], A_["Q3 2019"], "Q3 2019 release", "ONEOK’s full-year 2019 net income is expected to be in the range of $1,220 "
       "million to $1,330 million, compared with the range of $1,140 million to $1,400 million announced Feb. 25, 2019.", "ni", 1220, 1330)
eguide(2020, P["Q4 2019"], A_["Q4 2019"], "Q4 2019 release", "2020 Guidance Range (Millions of dollars) ONEOK, Inc. Net income $ 1,355 - $ "
       "1,605 Diluted earnings per common share $ 3.25 - $ 3.85", "eps", 3.25, 3.85,
       "the per-share range the release states beside net income of $1,355-1,605 million")
EG.append({"fy": 2020, "published": SPUB[SID_8K[MAR20]], "source": SID_8K[MAR20], "doc": f"8-K of {SPUB[SID_8K[MAR20]]}",
           "quote": quote(path(MAR20, "EX-99.1__*.rows.txt"), "factoring in the current commodity price environment and assumed rig "
                          "reductions, we expect our 2020 results to be within our previously announced guidance ranges"), "words": True})
# (decided here) the Q1 2020 release withdraws the February guidance and in the same text gives a numeric range of 2020 net income,
# GAAP, the first quarter's impairments in: a later numeric range of the year's net income, so it is the guide (numbers only; one-offs
# in, the LLY and UNH rule); its later restatements in words keep it, and the Q3 2020 release restates it in numbers
WD = "ONEOK is withdrawing its 2020 guidance expectations"      # cut to the current year (the sentence names the next year's outlook too)
eguide(2020, P["Q1 2020"], A_["Q1 2020"], "Q1 2020 release", "ONEOK has performed a scenario analysis, and based on currently available "
       "information, believes the range of possible 2020 net income results will likely be between $500 million and $900 million, which "
       "includes the $641.8 million impact of first quarter impairment charges", "ni", 500, 900,
       "a 2020 outlook given as the release withdraws the guidance of the Q4 2019 release: '" + WD + "'", extra=[WD])
eguide(2020, P["Q2 2020"], A_["Q2 2020"], "Q2 2020 release", "ONEOK expects 2020 net income and adjusted earnings before interest, taxes, "
       "depreciation and amortization (adjusted EBITDA) results to be at the low end of the ranges provided on April 28, 2020.", "words")
eguide(2020, P["Q3 2020"], A_["Q3 2020"], "Q3 2020 release", "2020 net income and adjusted earnings before interest, taxes, depreciation and "
       "amortization (adjusted EBITDA) are now expected to approach the midpoint of the ranges provided on April 28, 2020, of $500 million "
       "to $900 million, and $2,600 million to $3,000 million, respectively.", "ni", 500, 900,
       "the April 28 outlook range restated, 'approach the midpoint'")
eguide(2021, P["Q4 2020"], A_["Q4 2020"], "Q4 2020 release", "2021 Guidance Range (Millions of dollars, except per share amounts) ONEOK, Inc. "
       "Net income $ 1,075 - $ 1,375 Diluted earnings per common share $ 2.40 - $ 3.08", "eps", 2.40, 3.08,
       "the per-share range the release states beside net income of $1,075-1,375 million")
eguide(2021, P["Q1 2021"], A_["Q1 2021"], "Q1 2021 release", "2021 Guidance Range (Millions of dollars, except per share amounts) ONEOK, Inc. "
       "Net income $ 1,200 - $ 1,500 Diluted earnings per common share $ 2.69 - $ 3.35", "eps", 2.69, 3.35,
       "the per-share range the release states beside net income of $1,200-1,500 million")
eguide(2021, P["Q2 2021"], A_["Q2 2021"], "Q2 2021 release", "ONEOK now expects 2021 net income and adjusted earnings before interest, "
       "taxes, depreciation and amortization (adjusted EBITDA) to be above the midpoints of the ranges provided on April 27, 2021, of $1,200 "
       "million to $1,500 million, and $3,050 million to $3,350 million, respectively.", "ni", 1200, 1500,
       "the April 27 range restated; 'above the midpoints' is a one-sided bound, no field")
eguide(2021, P["Q3 2021"], A_["Q3 2021"], "Q3 2021 release", "10% earnings per diluted share increase to a midpoint of $3.33.", "eps",
       3.33, 3.33, "the per-share midpoint the release states, beside net income of $1,430-1,550 million",
       extra=["ONEOK increased 2021 net income guidance to a range of $1.43 billion to $1.55 billion, compared with the previously "
              "announced range of $1.20 billion to $1.50 billion."])
EG.sort(key=lambda g: (g["published"], g["fy"]))
for g in EG:                                     # the doc label carries the date the fact counts from
    if g["doc"].startswith("8-K of"):
        assert g["doc"] == f"8-K of {g['published']}", (g["doc"], g["published"])
# the Q1 2019 release states no guidance (asserted), so the Q4 2018 range stands
assert not re.search(r"(?i)net income guidance|guidance range|maintain", joined(REL(A_["Q1 2019"]))), "a Q1 2019 guide"

# ── dividends: each rate change from the first filing that states it as declared ──
DV = []
DIVQ = {"0001039684-18-000004": ("On January 17, 2018, our board of directors approved a cash dividend of 77 cents per share of common stock", 0.77),
        "0001039684-18-000030": ("On April 19, 2018, our board of directors approved a cash dividend of 79.5 cents per share of common stock", 0.795),
        "0001039684-18-000051": ("On July 25, 2018, our board of directors approved a cash dividend of 82.5 cents per share of common stock", 0.825),
        "0001039684-18-000074": ("On October 24, 2018, our board of directors approved a cash dividend of 85.5 cents per share of common stock",
                                 0.855),
        "0001039684-19-000004": ("On January 16, 2019, our board of directors approved a cash dividend of 86 cents per share of common stock", 0.86),
        "0001039684-19-000024": ("On April 18, 2019, our board of directors approved a cash dividend of 86.5 cents per share of common stock", 0.865),
        "0001039684-19-000050": ("On July 24, 2019, our board of directors approved a cash dividend of 89 cents per share of common stock", 0.89),
        "0001039684-19-000071": ("On October 23, 2019, our board of directors approved a cash dividend of 91.5 cents per share of common stock",
                                 0.915),
        "0001039684-20-000004": ("On January 15, 2020, our board of directors approved a cash dividend of 93.5 cents per share of common stock",
                                 0.935)}
for acc, (s, qd) in DIVQ.items():
    sid = SID_DIV[acc]
    qt = quote(path(acc, "8-K__*.rows.txt"), s)
    DV.append({"published": SPUB[sid], "quarterly": qd, "source": sid,
               "note": f"${qd:g} a quarter, ${qd * 4:g} a year: '{qt}' (ONEOK 8-K of {SPUB[sid]})"})
# unchanged rates (read by their text): 2020-04-17 to 2021-10-20, 93.5 cents
for acc in ("0001039684-20-000028", "0001039684-20-000052", "0001039684-20-000071", "0001039684-21-000006", "0001039684-21-000030",
            "0001039684-21-000052", "0001039684-21-000067"):
    assert "dividend of 93.5 cents per share" in joined(path(acc, "8-K__*.rows.txt")), acc
DV.sort(key=lambda x: x["published"])

# ── assemble ──
for k in ("history_vintages", "prints", "eps_guides", "dividends"):
    assert all(x["published"] <= "2017-12-31" for x in f[k]), k
f["sources"] = {**old["sources"], **dict(sorted(SOURCES.items(), key=lambda kv: int(kv[0][2:])))}
f["history_vintages"] = old["history_vintages"] + V
f["prints"] = old["prints"] + PR
f["eps_guides"] = old["eps_guides"] + EG
f["dividends"] = old["dividends"] + DV
f["_doc"] = old["_doc"].replace("gen_oke_1013.py (2010-2013) and gen_oke_1417.py (2014-2017)",
                                "gen_oke_1013.py (2010-2013), gen_oke_1417.py (2014-2017) and gen_oke_1821.py (2018-2021)")
assert "gen_oke_1821.py" in f["_doc"]
assert all(s["published"] <= CUT for s in f["sources"].values())
for k in ("rule_t", "listings", "company_names", "events", "guides", "splits", "distributions", "price_basis"):
    assert f[k] == old[k], k
YF = {dt.datetime.fromtimestamp(v["date"] + off, dt.timezone.utc).date().isoformat() for v in chart["events"]["splits"].values()}
assert not [d for d in YF if "2014-02-03" < d <= CUT], "a split or distribution in 2018-2021 needs its encoding"
out = A.out or os.path.join(REPO, "retro", "facts", "OKE.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(f, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_oke_1821.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump({k: v for k, v in CHECK.items() if v}, fh, ensure_ascii=False, indent=1)
print(f"{out}: +{len(V)} vintages, +{len(PR)} prints, +{len(EG)} EPS guides, +{len(DV)} dividends, +{len(SOURCES)} sources; "
      f"{sum(len(v) for v in CHECK.values())} quotes in {ck}")
for p in PR:
    print(p["quarter"], p["published"], p["sales_pct"], p["nm_pct"], p["opm_bp"], p["ptm_bp"], p["eps_q"], p["eps_q_prior"],
          p["diluted_shares_m"], p["release"])
for g in EG:
    print(g["fy"], g["published"], g["doc"], g.get("ni_guide_m") or g.get("eps_guide") or "words", g.get("shares_print"))
for v in V:
    print(v["fy_label"], v["published"], v["eps_normalized"], v["groups"])
