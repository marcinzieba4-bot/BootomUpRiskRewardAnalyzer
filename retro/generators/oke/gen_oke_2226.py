#!/usr/bin/env python3
"""Extend retro/facts/OKE.json with 2022-2026 (filings accepted 2021-12-01 to 2026-11-27), asserting that every earlier fact is
unchanged. Same discipline as gen_oke.py, gen_oke_1013.py, gen_oke_1417.py and gen_oke_1821.py: each raw figure is read from its own
labelled row of a named table (the row text is kept in the fact and written to the verbatim checklist) or from the sentence that holds it
(asserted present word for word), every rate, margin and change is computed, and every quote is asserted present in its own filing. Only
filings accepted on or before 2026-11-27 are read. The downloads (keep them outside the repo, e.g. the session scratchpad):

    python3 retro/tools/edgar.py index 1039684 <dir>
    python3 retro/tools/edgar.py fetch 1039684 <dir> --from 2021-12-01 --to 2026-11-28 --forms 8-K 8-K/A 10-K 10-K/A 10-Q

    python3 -I retro/generators/oke/gen_oke_2226.py --filings <dir> [--facts-in <2008-2021 sheet>] [--out retro/facts/OKE.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_oke_2226.json

The earnings releases are still page images with a text layer (read with `trow`, as gen_oke_1821.py); from the Q1 2023 release their
statements are in millions (shares in millions), before in thousands. The FY2021-FY2025 10-Ks reserve Item 6, so each vintage takes the
three years of its statement of income and the earlier years from the latest earlier vintage; from the FY2023 10-K the statements are in
millions (the rounded figures replace the earlier exact ones, as published).

--facts-in is the 2008-2021 sheet gen_oke_1821.py writes (default: retro/facts/OKE.json, which must then hold 2008-2021 only).
What the batch reads and decides is in retro/README.md, "OKE 2022-2026".
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
START, CUT = "2022-01-01", "2026-11-27"
CIK = 1039684
ROWS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("OKE")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
old = json.load(open(A.facts_in or os.path.join(REPO, "retro", "facts", "OKE.json"), encoding="utf-8"))
assert all(s["published"] <= "2021-12-31" for s in old["sources"].values()), "--facts-in must be the 2008-2021 sheet"
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


def sentence(p, start, contains=None):
    """The sentence of a filing that starts with `start` (and holds `contains`), word for word to its first full stop followed by a
    space; added to the checklist."""
    t = joined(p)
    for m in re.finditer(re.escape(start), t):
        e = t.find(". ", m.start())
        s = t[m.start():e + 1]
        if contains is None or contains in s:
            return quote(p, s)
    raise AssertionError((os.path.basename(p), start, contains))


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
    followed by exactly n numbers (a footnote mark such as '(a)' may follow the label); returns (numbers, the matched text, which goes to
    the checklist)."""
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
    if day not in TDAYS:
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

# ── the 10-Ks: the FY2021-FY2025 vintages ─────────────────────────────────────────────────────────────────────────────────────────
K = {"F2021": "0001039684-22-000015", "F2022": "0001039684-23-000016", "F2023": "0001039684-24-000015", "F2024": "0001039684-25-000036",
     "F2025": "0001039684-26-000006"}
DK = {k: path(a, "10-K__*.rows.txt") for k, a in K.items()}
REL = lambda acc: path(acc, "EX-99.1__*.rows.txt")
# the statements' unit: thousands of dollars (and of shares) in the FY2021 and FY2022 10-Ks, millions from the FY2023 10-K; every figure
# below is carried in thousands (x1000 where the filing prints millions)
KU = {"F2021": 1, "F2022": 1, "F2023": 1000, "F2024": 1000, "F2025": 1000}

# ── sources, in date order ───────────────────────────────────────────────────────────────────────────────────────────────────────
G25 = "0001039684-25-000043"
plan = [("print", "Q4 2021", 2021, 4, "0001039684-22-000010"),
        ("k", "F2021"),
        ("print", "Q1 2022", 2022, 1, "0001039684-22-000031"),
        ("print", "Q2 2022", 2022, 2, "0001039684-22-000057"),
        ("print", "Q3 2022", 2022, 3, "0001039684-22-000073"),
        ("div", "0001039684-23-000006", 0.955),
        ("print", "Q4 2022", 2022, 4, "0001039684-23-000012"),
        ("k", "F2022"),
        ("print", "Q1 2023", 2023, 1, "0001039684-23-000034"),
        ("print", "Q2 2023", 2023, 2, "0001039684-23-000058"),
        ("print", "Q3 2023", 2023, 3, "0001039684-23-000079"),
        ("div", "0001039684-24-000004", 0.99),
        ("print", "Q4 2023", 2023, 4, "0001039684-24-000013"),
        ("k", "F2023"),
        ("print", "Q1 2024", 2024, 1, "0001039684-24-000032"),
        ("print", "Q2 2024", 2024, 2, "0001039684-24-000135"),
        ("print", "Q3 2024", 2024, 3, "0001039684-24-000339"),
        ("print", "Q4 2024", 2024, 4, "0001039684-25-000026"),
        ("k", "F2024"),
        ("guide8k", G25, "ONEOK 8-K: 2025 financial guidance (Items 7.01, 9.01)"),
        ("print", "Q1 2025", 2025, 1, "0001039684-25-000058"),
        ("print", "Q2 2025", 2025, 2, "0001039684-25-000110"),
        ("print", "Q3 2025", 2025, 3, "0001039684-25-000121"),
        ("print", "Q4 2025", 2025, 4, "0001039684-26-000004"),
        ("k", "F2025"),
        ("print", "Q1 2026", 2026, 1, "0001039684-26-000015"),
        ("print", "Q2 2026", 2026, 2, "0001039684-26-000027"),
        ("print", "Q3 2026", 2026, 3, "0001039684-26-000036")]
SID_PRINT, SID_8K, SID_DIV, SID_K, ACC_PRINT = {}, {}, {}, {}, {}
for step in plan:
    if step[0] == "print":
        _, q, fy, n, acc = step
        ACC_PRINT[q] = acc
        SID_PRINT[q] = src(acc, f"ONEOK {q} results (8-K exhibit 99.1)",
                           f"{q}: revenues, cost of sales and fuel (net margin), operating income, income before income taxes, diluted EPS, "
                           "diluted shares; the EPS guidance where the release gives one; the dividend rate where it first states one")
    elif step[0] == "guide8k":
        SID_8K[step[1]] = src(step[1], step[2], "the EPS guidance it states")
    elif step[0] == "div":
        SID_DIV[step[1]] = src(step[1], f"ONEOK 8-K: quarterly dividend of ${step[2]:g} (Items 7.01, 8.01)",
                               f"the quarterly dividend rate, ${step[2]:g} a share")
    elif step[0] == "k":
        SID_K[step[1]] = src(K[step[1]], f"ONEOK {step[1].replace('F', 'FY')} 10-K", f"history vintage {step[1].replace('F', 'FY')}; the 'why'")
srt_src = sorted(SOURCES.items(), key=lambda kv: (kv[1]["published"], int(kv[0][2:])))
assert [k for k, _ in srt_src] == sorted(SOURCES, key=lambda k: int(k[2:])), "source ids must follow publication order"
SPUB = {**{k: v["published"] for k, v in old["sources"].items()}, **{k: v["published"] for k, v in SOURCES.items()}}
# the FY2025 guidance 8-K and the FY2024 10-K count from the same day (accepted 16:32 and 16:21 ET on 2025-02-25)
assert SPUB[SID_8K[G25]] == SPUB[SID_K["F2024"]] == "2025-02-26"

# ── history vintages: each year from the latest filing that reports it; the ten fiscal years to the latest one ─────────────────────
V20 = old["history_vintages"][-1]                     # the FY2020 vintage (2018-2021 sheet)
assert V20["fy_label"] == "FY20"
ST = r"^CONSOLIDATED STATEMENTS OF INCOME$"


def stmt(fk, label, n=3, after=None):
    v, t = row(DK[fk], label, ST, after, n=n)
    return [x * KU[fk] for x in v], t


VOL = {"F2021": "The volatility of natural gas, crude oil and NGL prices could affect adversely our earnings and cash flows.",
       "F2023": "The volatility of natural gas, NGL, Refined Products and crude oil prices could affect adversely our earnings and cash flows.",
       "F2025": "The volatility of natural gas, NGL, Refined Products and crude oil prices could adversely affect our earnings and cash flows."}
VOL["F2022"], VOL["F2024"] = VOL["F2021"], VOL["F2023"]
GHG = "We may face significant costs to comply with the regulation of GHG emissions."
RES = ("We may not be able to accurately estimate hydrocarbon reserves and production volumes expected to be delivered to us for a variety "
       "of reasons, including the unavailability of sufficiently detailed information and unanticipated changes in producers’ expected "
       "drilling schedules.")
# the FY2019-FY2020 climate-demand risk factor is gone from the FY2021 10-K; its climate risk factor heading is quoted instead (text only)
ESG = {"F2021": "Increasing attention to ESG matters, including climate change, may impact our business.",
       "F2023": "Increasing attention to ESG issues, including climate change, may impact our business.",
       "F2025": "Scrutiny and conflicting stakeholder expectations regarding ESG issues, including climate change, may impact our business."}
ESG["F2022"], ESG["F2024"] = ESG["F2023"], ESG["F2023"]
DEMAND_GONE = ("Changes in regulatory policies, public sentiment or technology due to the threat of climate change that result in a "
               "reduction in the demand for hydrocarbon products")
# CLOUD's and GENAI's words in the 10-Ks are ONEOK's own vendors and computing policy (cybersecurity), text only
CLOUDW = {"F2023": "In order to manage these cybersecurity risks, including our use of third-party software and cloud vendors, we have "
                   "developed and implemented a cybersecurity risk management program intended to protect the confidentiality, integrity "
                   "and availability of our critical systems and information.",
          "F2024": "In addition, we conduct risk assessments of enterprise third-party software and cloud vendors by utilizing security "
                   "questionnaires prior to procurement.",
          "F2025": "In addition, we conduct risk assessments of new enterprise third-party software and cloud vendors by utilizing security "
                   "questionnaires prior to procurement."}
AIW = {"F2025": "The use of emerging technologies, including the use of Cloud Services and Artificial Intelligence, is governed by our "
                "End-User Computing Policy."}
BL = {"F2021": ("a midstream service provider: natural gas gathering and processing, natural gas liquids and natural gas pipelines (ONEOK "
                "Partners' common units it did not own acquired for ONEOK common stock on June 30, 2017)"),
      "F2023": ("a midstream service provider: natural gas gathering and processing, natural gas liquids, natural gas pipelines and, from "
                "the Magellan Midstream Partners acquisition of September 25, 2023 (its units acquired for cash and ONEOK common stock), "
                "refined products and crude"),
      "F2024": ("a midstream service provider: natural gas gathering and processing, natural gas liquids, natural gas pipelines and refined "
                "products and crude (Magellan Midstream Partners from September 25, 2023; the controlling interest in EnLink Midstream "
                "from October 15, 2024 and Medallion Midstream from October 31, 2024, both for cash; EnLink's public units for ONEOK "
                "common stock on January 31, 2025)")}
BL["F2022"], BL["F2025"] = BL["F2021"], BL["F2024"]
KT = "A midstream service provider"


def why(fk):
    lo = joined(DK[fk]).lower()
    # DURABLE needs the company not to call its own business cyclical (the MU rule): no FY2021-FY2025 10-K uses the word
    assert "cyclical" not in lo, (fk, "a 10-K that uses the word cyclical")
    q = [sentence(DK[fk], "We are a leading midstream service provider"), sentence(DK[fk], "Each of our ", "consolidated earnings were"),
         quote(DK[fk], VOL[fk])]
    return " ".join(f"'{x}'" for x in q) + (f" (the {fk.replace('F', 'FY')} 10-K's own words; it does not use the word cyclical, so "
                                            "DURABLE, the MU rule)")


def themes(fk):
    """The 10-K's own words the builder quotes beside a live theme's scope (text only): the GHG risk factor, the producers' reserves
    (ONEOK holds none of its own), the climate risk factor's heading (the climate-demand factor of the FY2019-FY2020 10-Ks is gone), and
    from the FY2023 10-K the cloud vendors and from the FY2025 10-K the artificial intelligence of its cybersecurity text; no 10-K names
    electric vehicles, crypto or GLP-1."""
    t = joined(DK[fk])
    assert norm(DEMAND_GONE) not in t, (fk, "the climate-demand risk factor is back")
    out = {"ENERGY_TRANSITION_ghg": quote(DK[fk], GHG), "ENERGY_TRANSITION_reserves": quote(DK[fk], RES),
           "ENERGY_TRANSITION_esg": quote(DK[fk], ESG[fk])}
    if fk in CLOUDW:
        out["CLOUD_vendor"] = quote(DK[fk], CLOUDW[fk])
    else:
        assert "cloud" not in t.lower(), (fk, "cloud")
    if fk in AIW:
        out["GENAI_words"] = quote(DK[fk], AIW[fk])
    else:
        assert not re.search(r"(?i)artificial intelligence|generative|machine learning", t), (fk, "AI words")
    for w in ("electric vehicle", "crypto", "blockchain", "bitcoin", "digital asset", "glp-1", "obesity"):
        assert w not in t.lower(), (fk, w)
    return out


def groups(fk, fy):
    """Segment total revenues, intersegment revenues in, the last year and the one before, by the segment note's own column heads
    (Total Segments left out); a segment with no prior-year column (Refined Products and Crude in the FY2023 10-K) has no growth."""
    out = {}
    ls = lines(DK[fk])
    for y in (fy, fy - 1):
        k = next(i for i, l in enumerate(ls) if re.match(rf"Year Ended (December|Dec\.) 31, {y} \|", l) and "Gathering" in l)
        heads = [c.strip() for c in ls[k].split("|")[1:]]
        unit = 1 if ls[k + 1].startswith("(Thousands of dollars)") else 1000
        assert ls[k + 1].startswith(("(Thousands of dollars)", "(Millions of dollars)")), (fk, y, ls[k + 1])
        r = next(l for l in ls[k:k + 14] if re.match(r"Total revenues( \([a-z]\))? \|", l))
        CHECK.setdefault(DK[fk], []).append(r)
        vals = [num(c) * unit for c in r.split("|")[1:] if c.strip()]
        assert len(vals) == len(heads), (fk, y, heads, vals)
        out[y] = {re.sub(r"\s+", "", re.sub(r"\s*\([a-z]\)$", "", h)): (h, v) for h, v in zip(heads, vals)
                  if not re.search(r"(?i)^(Other|Total)", h)}
    name = lambda h: re.sub(r"\s*\([a-z]\)$", "", re.sub(r"(?<=[a-z])(?=[A-Z])", " ", h))
    return [[name(h), round(v / 1e6, 3), pct1(out[fy - 1][k][1], v) if k in out[fy - 1] else None] for k, (h, v) in out[fy].items()]


def vintage(fk, fy, eps, rev, sh, div_fragment, div_q, restate_note, pretax_note):
    """eps / rev / sh: {year: (value, source id)}; the per-year sources give each year's publication date (on_basis)."""
    st = {"rev": stmt(fk, r"Total revenues( \(Note [A-Z]\))?")[0], "oi": stmt(fk, r"Operating income")[0],
          "pti": stmt(fk, r"Income before income taxes")[0], "tax": [abs(x) for x in stmt(fk, r"Income taxes( \(Note [A-Z]\))?")[0]]}
    cf = r"^CONSOLIDATED STATEMENTS OF CASH FLOWS( \||$)"
    u = KU[fk]
    cfo = [x * u for x in row(DK[fk], r"Cash provided by operating activities", cf, n=3)[0]]
    cx = [abs(x) * u for x in row(DK[fk], r"Capital expenditures \(less allowance for equity funds used during construction\)", cf, n=3)[0]]
    ls = lines(DK[fk])
    c0 = next(i for i, l in enumerate(ls) if re.search(cf, l))
    c1 = next(i for i in range(c0, len(ls)) if ls[i].startswith("Cash and cash equivalents at end of period"))
    rep = [l for l in ls[c0:c1] if l.startswith("Repurchase of common stock")]
    iss = [l for l in ls[c0:c1] if l.startswith("Issuance of common stock")]
    parts = []
    if rep:
        r_, _ = row(DK[fk], r"Repurchase of common stock( \(Note [A-Z]\))?", cf, n=3)
        parts.append(f"repurchase of common stock ${abs(r_[0]) * u / 1000:,.1f}M" if r_[0] else
                     f"no repurchase of common stock in {fy} (the FY{fy} 10-K's statement of cash flows prints none for the year)")
    else:
        parts.append(f"no repurchase of common stock in {fy} (the FY{fy} 10-K's statement of cash flows has no repurchase line)")
    if iss:
        i_, _ = row(DK[fk], r"Issuance of common stock", cf, n=3)
        parts.append(f"issuance of common stock ${i_[0] * u / 1000:,.1f}M")
    else:
        parts.append("no issuance of common stock for cash (no such line)")
    cash_return = "; ".join(parts)
    sid = SID_K[fk]
    years = sorted(eps)
    assert years == list(range(years[0], fy + 1)) and len(years) == 10, (fk, years)
    first = years[0]
    return {
        "published": SPUB[sid], "sources": sorted({sid} | {s for _, s in eps.values()} | {s for _, s in rev.values()}
                                                 | {s for _, s in sh.values()}, key=lambda s: -int(s[2:])),
        "company": "ONEOK, Inc.", "exchange": "NYSE", "symbol": "OKE",
        "business_line": BL[fk],
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
        "normalization": V20["normalization"].split("; 2018-2020 from the FY2020 10-K")[0] + "; " + restate_note,
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
        "dividend_note": f"${div_q:g} a quarter, ${div_q * 4:g} a year: '{quote(DK[fk], div_fragment)}' (FY{fy} 10-K)",
        "fcf_label": f"FY{fy % 100:02d}", "fcf_b": round((cfo[0] - cx[0]) / 1e6, 3),
        "fcf_note": (f"cash provided by operating activities ${cfo[0] / 1000:,.1f}M less capital expenditures ${cx[0] / 1000:,.1f}M "
                     f"(FY{fy} 10-K, consolidated)"),
        "cash_return_text": cash_return,
        "groups": groups(fk, fy),
        "groups_basis": (f"FY{fy % 100:02d} segment total revenues, intersegment revenues included (FY{fy} 10-K segment note; eliminations "
                         "and Other left out)"),
        "margin_signal_name": "Pre-tax margin change",
        "kind": "DURABLE", "kind_text": KT,
        "why": why(fk),
        "theme_quotes": themes(fk),
        "theme_holder": "ONEOK",
        # (OKE 2022-2026) the words no 10-K uses (asserted): GLP1's subject joins EV's and CRYPTO's, and artificial intelligence where
        # the 10-K names none (to the FY2024 10-K)
        "theme_absent": ["electric vehicle", "crypto", "GLP-1"] + ([] if fk in AIW else ["artificial intelligence"]),
    }


c_eps = {int(y): (v, V20["eps_sources"][y]) for y, v in V20["eps_normalized"].items()}
c_rev = {int(y): (v, V20["revenue_sources"][y]) for y, v in V20["revenue_usd_b"].items()}
c_sh = {int(y): (v, V20["shares_sources"][y]) for y, v in V20["diluted_shares_m"].items()}
V = []
NCI2 = "the noncontrolling interests and preferred dividends (under $5 million) come after it, so the check slightly overstates ONEOK's own EPS"
NCI3 = ("the noncontrolling interests (EnLink's public unitholders from October 15, 2024 to January 31, 2025) and preferred dividends come "
        "after it, so the check overstates ONEOK's own EPS")


def roll(prev, fk, fy, e_label, r_label, after_sh=r"(?i)^Average shares"):
    """The three statement years of a 10-K over the earlier vintage's years, the eleventh year from the end leaving."""
    e, _ = stmt(fk, e_label)
    e = [x / KU[fk] for x in e]                      # per-share figures are not scaled
    r, _ = stmt(fk, r_label)
    s, _ = stmt(fk, r"Diluted", after=after_sh)
    sid = SID_K[fk]
    pe, pr, ps = prev
    eps_ = {**pe, **{fy - i: (e[i], sid) for i in range(3)}}
    rev_ = {**pr, **{fy - i: (r[i], sid) for i in range(3)}}
    sh_ = {**ps, **{fy - i: (s[i], sid) for i in range(3)}}
    for d in (eps_, rev_, sh_):
        del d[fy - 10]
    return (eps_, rev_, sh_), e


# FY2021 10-K (2022-03-02): Item 6 reserved; 2019-2021 from the statement of income (no discontinued operations), earlier years carried
H21, e = roll((c_eps, c_rev, c_sh), "F2021", 2021, r"Diluted EPS \(Note I\)", r"Total revenues \(Note P\)")
assert e == [3.35, 1.42, 3.07], e
assert quote(DK["F2021"], "ITEM 6. [RESERVED]")
Q21 = quote(REL("0001039684-22-000010"), "Amounts for the year ended Dec. 31, 2021, include a noncash tax impact of $19.4 million, or 4 cents "
            "per diluted share, related to previously recognized gains on certain benefit plan investments.")
V.append(vintage("F2021", 2021, *H21, "In February 2022, we paid a quarterly common stock dividend of $0.935 per share ($3.74 per share on "
                 "an annualized basis)", 0.935,
                 "2019-2021 from the FY2021 10-K's statement of income (Item 6 is reserved; earlier years from the latest earlier 10-K); 2021 "
                 f"at GAAP $3.35: its one listed item ('{Q21}', the Q4 2021 release) is 4 cents; the ten fiscal years to the latest one, so "
                 "2011 leaves and the window starts with 2012", NCI2))
# FY2022 10-K (2023-03-01): 2020-2022 from the statement of income
H22, e = roll(H21, "F2022", 2022, r"Diluted EPS \(Note J\)", r"Total revenues \(Note Q\)")
assert e == [3.84, 3.35, 1.42], e
Q22 = quote(REL("0001039684-23-000012"), "Amounts for the year ended Dec. 31, 2022, include a $5 million property insurance deductible and "
            "an approximately $30 million earnings impact in the natural gas liquids segment from the 45-day waiting period for business "
            "interruption coverage related to the Medford incident, which together represent 6 cents per diluted share after tax.")
V.append(vintage("F2022", 2022, *H22, "In February 2023, we paid a quarterly common stock dividend of $0.955 per share ($3.82 per share on "
                 "an annualized basis)", 0.955,
                 f"2020-2022 from the FY2022 10-K's statement of income; 2022 at GAAP $3.84: its listed items ('{Q22}', the Q4 2022 "
                 "release) are 6 cents; the ten fiscal years to the latest one, so 2012 leaves and the window starts with 2013", NCI2))
# FY2023 10-K (2024-02-28): 2021-2023 from the statement of income, in millions from this 10-K (the rounded figures replace the exact
# ones, as published); Magellan from September 25, 2023, as published (about 135 million ONEOK shares issued, in the diluted average from then)
H23, e = roll(H22, "F2023", 2023, r"Diluted EPS \(Note J\)", r"Total revenues \(Note P\)")
assert e == [5.48, 3.84, 3.35], e
Q23 = quote(REL("0001039684-24-000013"), "Amounts for the year ended Dec. 31, 2023, include a pre-tax benefit of $633 million related to the "
            "Medford incident, including a one-time insurance settlement gain of $779 million, offset partially by $146 million of "
            "third-party fractionation costs incurred in 2023; and pre-tax impacts of $158 million in transaction costs, $49 million in "
            "interest income, $41 million related to net gains on open market repurchases of debt and $21 million in interest expense "
            "related to the transaction-related bridge facility commitment fees, all resulting in a net benefit of 87 cents per diluted "
            "share after tax.")
assert 0.87 < (5.48 - 0.87) / 2
V.append(vintage("F2023", 2023, *H23, "In February 2024, we paid a quarterly common stock dividend of $0.99 per share ($3.96 per share on "
                 "an annualized basis)", 0.99,
                 f"2021-2023 from the FY2023 10-K's statement of income, in millions (rounded, as published); 2023 at GAAP $5.48: its "
                 f"listed items ('{Q23}', the Q4 2023 release) are a net benefit of 87 cents against $4.61 without them, under half (the "
                 "mirror of the AAPL FY2002 test), and no filing publishes a full-year EPS without them; Magellan Midstream Partners from "
                 "September 25, 2023, as published; the ten fiscal years to the latest one, so 2013 leaves and the window starts with 2014",
                 NCI2))
# FY2024 10-K (2025-02-26): 2022-2024 from the statement of income; EPS on net income attributable to ONEOK (EnLink's noncontrolling
# interests from October 15, 2024)
H24, e = roll(H23, "F2024", 2024, r"Diluted EPS \(Note K\)", r"Total revenues \(Note R\)")
assert e == [5.17, 5.48, 3.84], e
Q24 = quote(REL("0001039684-25-000026"), "Amounts for the three months and year ended Dec. 31, 2024, include pre-tax gains of $237 million "
            "and $286 million, respectively, related to non-strategic asset divestitures; interest income of $25 million and $39 million, "
            "respectively; and transaction costs of $56 million and $96 million, respectively, related to ONEOK’s acquisitions; resulting "
            "in a net benefit of 27 cents and 30 cents per diluted share after tax, respectively.")
assert 0.30 < (5.17 - 0.30) / 2
V.append(vintage("F2024", 2024, *H24, "In February 2025, we paid a quarterly common stock dividend of $1.03 per share ($4.12 per share on "
                 "an annualized basis)", 1.03,
                 f"2022-2024 from the FY2024 10-K's statement of income (EPS on net income attributable to ONEOK); 2024 at GAAP $5.17: its "
                 f"listed items ('{Q24}', the Q4 2024 release) are a net benefit of 30 cents, under half; EnLink Midstream (the controlling "
                 "interest from October 15, 2024) and Medallion Midstream (from October 31, 2024) as published; the ten fiscal years to "
                 "the latest one, so 2014 leaves and the window starts with 2015", NCI3))
# FY2025 10-K (2026-02-25): 2023-2025 from the statement of income; EnLink's public units acquired for ONEOK stock on January 31, 2025
H25, e = roll(H24, "F2025", 2025, r"Diluted EPS \(Note J\)", r"Total revenues \(Note Q\)")
assert e == [5.42, 5.17, 5.48], e
Q25 = quote(REL("0001039684-26-000004"), "Amounts for the three months and year ended Dec. 31, 2025, include pretax impacts of $7 million "
            "and $81 million, respectively, of transaction costs, related to ONEOK’s acquisitions, resulting in a net impact of "
            "approximately 1 cent and 10 cents per diluted share after tax, respectively.")
V.append(vintage("F2025", 2025, *H25, "In February 2026, we paid a quarterly common stock dividend of $1.07 per share ($4.28 per share on "
                 "an annualized basis)", 1.07,
                 f"2023-2025 from the FY2025 10-K's statement of income (EPS on net income attributable to ONEOK); 2025 at GAAP $5.42: its "
                 f"listed items ('{Q25}', the Q4 2025 release) are 10 cents; EnLink's public units acquired for ONEOK common stock on "
                 "January 31, 2025, as published; the ten fiscal years to the latest one, so 2015 leaves and the window starts with 2016",
                 NCI3))
for v in V:
    assert all(v["eps_published"][y] <= v["published"] for y in v["eps_normalized"])
assert [v["pe_window_start"] for v in V] == ["2012-01-01", "2013-01-01", "2014-01-01", "2015-01-01", "2016-01-01"]

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
    i = t.find("CONSOLIDATED STATEMENTS OF INCOME")
    u = re.search(r"\((Thousands|Millions) of dollars", t[i:i + 600]).group(1)
    mul = 1 if u == "Thousands" else 1000          # carried in thousands
    k = 2 if n == 1 else 4                         # Q1: the quarter only; Q2-Q4: the quarter and the year to date
    sc = lambda v: [x * mul for x in v]
    rv, t_rv = trow(p, r"Total revenues", SI, k)
    cost, t_nm = trow(p, r"Cost of sales and fuel \(exclusive of items shown separately below\)", SI, k)
    oi, t_oi = trow(p, r"Operating income", SI, k)
    pti, t_pt = trow(p, r"Income before income taxes", SI, k)
    eps, t_e = trow(p, r"Diluted earnings per common share", SI, k)
    sh, t_s = trow(p, r"Diluted", SI, k, after=r"Average shares \((?:thousands|millions)\)")
    cash, t_c = trow(p, r"Cash and cash equivalents", BS, 2)
    rv, cost, oi, pti, sh, cash = sc(rv), sc(cost), sc(oi), sc(pti), sc(sh), sc(cash)
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
                            + (" (the statements in millions from this release)" if q == "Q1 2023" else ""),
              "nm_note": f"net margin ${r['nm_m']:,.1f}M vs ${r['nm_prior_m']:,.1f}M (revenues less cost of sales and fuel)",
              "dist_note": "Distribution operating income n/r (the natural gas distribution business separated as ONE Gas on January 31, 2014)",
              "margin_note": f"operating income {fm(r['oi_m'])}, income before income taxes {fm(r['pti_m'])}",
              "eps_note": f"diluted {fmt_e(r['eps_q'])} vs {fmt_e(r['eps_q_prior'])} (no discontinued operations)",
              "cash_note": f"cash and cash equivalents ${cash[0] / 1000:,.1f}M at the quarter's end (consolidated)",
              "next_print": NEXT[n]})
    if (fy, n) >= (2024, 4):
        d["eps_note"] += "; on net income attributable to ONEOK"
    if q == "Q1 2023":
        d["eps_note"] += "; the quarter includes the Medford incident's $779 million insurance settlement gain"
    if q == "Q3 2023":
        d["eps_note"] += "; Magellan Midstream Partners from September 25, 2023, as published"
    if q == "Q3 2026":
        d["eps_note"] += "; the quarter includes a one-time noncash income tax benefit of $336 million, $0.53 a diluted share"
    PR.append(d)


for step in plan:
    if step[0] == "print":
        prt(*step[1:])
# the year-ago figures each release prints are the earlier print's own (within half a million where the units changed to millions in
# 2023; EPS exactly)
allp = {p["quarter"]: p for p in old["prints"] + PR}
for p in PR:
    qa = f"{p['quarter'][:2]} {p['fy'] - 1}"
    a = allp[qa]
    tol = 0.5 + 1e-9 if p["fy"] == 2023 else 1e-6
    if p["quarter"] == "Q2 2023":     # its year-ago revenues print $5,996M against Q2 2022's $5,996.721M (a $1M difference, as printed)
        tol = 1.0
    assert abs(p["raw"]["rev_prior_m"] - a["raw"]["rev_m"]) <= tol and p["raw"]["eps_q_prior"] == a["raw"]["eps_q"], (p["quarter"], qa)
# each Q4 print came a trading day before its 10-K, and the week's date (the trading day after the print) is the 10-K's day
for q, fk in (("Q4 2021", "F2021"), ("Q4 2022", "F2022"), ("Q4 2023", "F2023"), ("Q4 2024", "F2024"), ("Q4 2025", "F2025")):
    p = next(x for x in PR if x["quarter"] == q)
    k = SPUB[SID_K[fk]]
    assert p["published"] < k and [d for d in TDAYS if p["published"] < d <= k] == [k], (q, "the 10-K comes the next trading day")
assert [p["published"] for p in PR] == sorted(p["published"] for p in PR)
assert all("after the close" in p["release_time"] for p in PR), "a release not after the close"

# ── EPS guides: ONEOK's GAAP diluted EPS for the year ────────────────────────────────────────────────────────────────────────────────
# From 2022 every numeric guide states diluted EPS, as a range in the guidance table or as a midpoint alone: the per-share range where
# stated, a stated midpoint alone a point (lo = hi; the Q3 2021 encoding); one-offs in as published (the LLY and UNH rule); words keep
# the last range. A guide that includes an acquisition pending on its date is not used (the 2017-02-02 rule of "OKE 2014-2017": a pending
# deal adds nothing); of a release's two guides, the one without a pending deal, with the closed acquisitions in where it has them.
EG = []


def eguide(fy, sid, p, doc, s, kind, lo=None, hi=None, note=None, extra=()):
    qt = quote(p, s)
    for x in extra:
        quote(p, x)
    g = {"fy": fy, "published": SPUB[sid], "source": sid, "doc": doc, "quote": qt}
    if kind == "words":
        g["words"] = True
    else:
        g["eps_guide"] = [lo, hi]
        if note:
            g["eps_guide_note"] = note
    EG.append(g)


P = SID_PRINT
R_ = lambda q: REL(ACC_PRINT[q])
eguide(2022, P["Q4 2021"], R_("Q4 2021"), "Q4 2021 release", "2022 Guidance Range (Millions of dollars, except per share amounts) ONEOK, "
       "Inc. Net income $ 1,550 - $ 1,830 Diluted earnings per common share $ 3.45 - $ 4.07", "eps", 3.45, 4.07,
       "the per-share range the release states beside net income of $1,550-1,830 million")
eguide(2022, P["Q1 2022"], R_("Q1 2022"), "Q1 2022 release", "affirmed full-year 2022 financial guidance", "words")
eguide(2022, P["Q2 2022"], R_("Q2 2022"), "Q2 2022 release", "affirmed full-year 2022 financial guidance", "words")
eguide(2022, P["Q3 2022"], R_("Q3 2022"), "Q3 2022 release", "affirmed its full-year 2022 financial guidance midpoints", "words")
# the Q3 2022 release's 2023 outlook ('ONEOK expects a more than 10% increase in 2023 net income ...') is a one-sided bound, no field;
# FY2023 becomes the current year only with the FY2022 10-K, after the Q4 2022 range (asserted below)
quote(R_("Q3 2022"), "ONEOK expects a more than 10% increase in 2023 net income and adjusted earnings before interest, taxes, depreciation "
      "and amortization (adjusted EBITDA), compared with its 2022 guidance midpoints.")
eguide(2023, P["Q4 2022"], R_("Q4 2022"), "Q4 2022 release", "2023 Guidance Range (Millions of dollars, except per share amounts) ONEOK, "
       "Inc. Net income $ 2,260 - $ 2,560 Diluted earnings per common share $ 5.03 - $ 5.69", "eps", 5.03, 5.69,
       "the per-share range the release states beside net income of $2,260-2,560 million, the Medford insurance settlement gain in",
       extra=["ONEOK’s 2023 net income and adjusted EBITDA guidance include a total impact of $539.3 million related to the Medford "
              "incident, comprised of a one-time insurance settlement gain of $779.3 million partially offset by an estimated $240 million "
              "primarily related to third- party fractionation costs, which ONEOK expects to incur in 2023."])
eguide(2023, P["Q1 2023"], R_("Q1 2023"), "Q1 2023 release", "affirmed full-year 2023 financial guidance", "words")
eguide(2023, P["Q2 2023"], R_("Q2 2023"), "Q2 2023 release", "Earnings per diluted share increased to a midpoint of $5.54 compared with a "
       "previous midpoint of $5.36.", "eps", 5.54, 5.54,
       "the per-share midpoint the release states, beside net income of $2,390-2,590 million, on a stand-alone basis: the Magellan "
       "merger was pending and the guide excludes it",
       extra=["These midpoints and ranges exclude the impact of the pending merger with Magellan Midstream Partners and future "
              "merger-related costs, to be comparable with the original guidance provided on Feb. 27, 2023."])
# (decided here) the Q3 2023 release gives a consolidated guide (Magellan, closed on September 25, 2023, in, with $175 million of
# transaction costs and the inventory valuation) beside the pre-acquisition basis: the consolidated midpoint is the guide (the
# acquisition in as published; the pre-acquisition basis leaves out a closed acquisition)
Q3T = ("2023 Guidance Range (Millions of dollars, except per share amounts) Consolidated Guidance Midpoints(b) ONEOK Pre-Acquisition "
       "Guidance Midpoints ONEOK, Inc. Previous(a) Updated Net income $ 2,490 $ 2,610 $ 2,600 Diluted earnings per common share $ 5.54 $ "
       "5.81 $ 5.36")
eguide(2023, P["Q3 2023"], R_("Q3 2023"), "Q3 2023 release", Q3T, "eps", 5.36, 5.36,
       "the consolidated midpoint the release states, Magellan in from September 25, 2023 with $175 million of transaction costs, beside "
       "net income of $2,600 million; the pre-acquisition basis's $5.81 leaves out the closed acquisition, unused",
       extra=["(b) Includes $175 million of transaction costs and the unfavorable impact of acquisition-related commodity inventory "
              "valuation."])
eguide(2024, P["Q4 2023"], R_("Q4 2023"), "Q4 2023 release", "2024 Guidance Range (Millions of dollars, except per share amounts) ONEOK, "
       "Inc. Net income $2,610 - $3,010 Diluted earnings per common share $4.45 - $5.14", "eps", 4.45, 5.14,
       "the per-share range the release states beside net income of $2,610-3,010 million")
eguide(2024, P["Q1 2024"], R_("Q1 2024"), "Q1 2024 release", "Earnings per diluted share increased to a midpoint of $4.92.", "eps",
       4.92, 4.92, "the per-share midpoint the release states, beside net income of $2,730-3,030 million",
       extra=["ONEOK increased 2024 net income guidance to a range of $2.73 billion to $3.03 billion, compared with the previously announced "
              "range of $2.61 billion to $3.01 billion."])
eguide(2024, P["Q2 2024"], R_("Q2 2024"), "Q2 2024 release", "affirmed full-year 2024 financial guidance", "words")
# (decided here) the Q3 2024 release's consolidated guide includes the Medallion acquisition, pending on its date (closed October 31,
# 2024): not used (the pending-deal rule); its stand-alone guide (EnLink's controlling interest, closed October 15, 2024, and Medallion
# both out) is the guide
eguide(2024, P["Q3 2024"], R_("Q3 2024"), "Q3 2024 release", "Earnings per diluted share increased to a midpoint of $5.02 compared with a "
       "previous midpoint of $4.92.", "eps", 5.02, 5.02,
       "the stand-alone midpoint the release states, beside net income of $2,870-3,020 million, EnLink and Medallion out; its consolidated "
       "midpoint of $5.11, net income of $2,895-3,095 million, includes the Medallion acquisition then pending, unused",
       extra=["ONEOK Consolidated (includes expected future contributions from EnLink and Medallion): • Net income midpoint of $2.995 "
              "billion. • Earnings per diluted share midpoint of $5.11.",
              "These midpoints and ranges exclude the contribution from ONEOK’s acquisition of the controlling interest in EnLink, the "
              "pending acquisition of Medallion and related transaction costs, to be comparable with ONEOK’s guidance provided on April "
              "30, 2024."])
# the Q4 2024 release gives no 2025 guidance (asserted); the 8-K of 2025-02-26 does
assert [m.start() for m in re.finditer(r"(?i)guidance", joined(R_("Q4 2024")))] == [joined(R_("Q4 2024")).find("“guidance,”") + 1], \
    "a guide in the Q4 2024 release (its one 'guidance' is the forward-looking statements' word list)"
eguide(2025, SID_8K[G25], path(G25, "EX-99.1__*.rows.txt"), f"8-K of {SPUB[SID_8K[G25]]}", "2025 Guidance Range (Millions of dollars, "
       "except per share amounts) ONEOK, Inc. Net income $3,210 - $3,690 Net income attributable to ONEOK $3,110 - $3,610 Diluted earnings "
       "per common share $4.97 - $5.77", "eps", 4.97, 5.77,
       "the per-share range the 8-K states beside net income attributable to ONEOK of $3,110-3,610 million")
eguide(2025, P["Q1 2025"], R_("Q1 2025"), "Q1 2025 release", "affirmed full-year 2025 financial guidance", "words")
eguide(2025, P["Q2 2025"], R_("Q2 2025"), "Q2 2025 release", "affirmed full-year 2025 financial guidance ranges", "words")
eguide(2025, P["Q3 2025"], R_("Q3 2025"), "Q3 2025 release", "affirmed full-year 2025 net income and adjusted EBITDA guidance ranges",
       "words")
# the 8-K's 2026 outlook ('greater than 15% earnings per share growth') is a one-sided bound, no field; FY2026 becomes the current year
# only with the FY2025 10-K, after the Q4 2025 range (asserted below)
quote(path(G25, "EX-99.1__*.rows.txt"), "ONEOK expects greater than 15% earnings per share growth and adjusted EBITDA growth approaching "
      "10% in 2026, compared with 2025 guidance midpoints.")
eguide(2026, P["Q4 2025"], R_("Q4 2025"), "Q4 2025 release", "2026 Guidance Range (Millions of dollars, except per share amounts) ONEOK, "
       "Inc. Net income $3,190 - $3,710 Diluted earnings per common share $5.04 - $5.87", "eps", 5.04, 5.87,
       "the per-share range the release states beside net income of $3,190-3,710 million")
eguide(2026, P["Q1 2026"], R_("Q1 2026"), "Q1 2026 release", "Earnings per diluted share increased to a midpoint of $5.53.", "eps",
       5.53, 5.53, "the per-share midpoint the release states, beside net income of $3,210-3,790 million",
       extra=["ONEOK increased 2026 net income guidance to a range of $3.21 billion to $3.79 billion."])
eguide(2026, P["Q2 2026"], R_("Q2 2026"), "Q2 2026 release", "Earnings per diluted share increased to a midpoint of $5.68", "eps",
       5.68, 5.68, "the per-share midpoint the release states, beside net income of $3,410-3,790 million",
       extra=["ONEOK increased 2026 net income guidance to a range of $3.41 billion to $3.79 billion."])
eguide(2026, P["Q3 2026"], R_("Q3 2026"), "Q3 2026 release", "Earnings per diluted share increased to a midpoint of $6.30", "eps",
       6.30, 6.30, "the per-share midpoint the release states, beside net income of $4,090-4,270 million; the Brazos Permian Midland "
       "acquisition (completed) and the quarter's one-time $336 million tax benefit in, as published",
       extra=["ONEOK increased 2026 net income guidance to a range of $4.09 billion to $4.27 billion."])
EG.sort(key=lambda g: (g["published"], g["fy"]))
for g in EG:                                     # the doc label carries the date the fact counts from
    if g["doc"].startswith("8-K of"):
        assert g["doc"] == f"8-K of {g['published']}", (g["doc"], g["published"])
# each year's first numeric guide is public before the vintage that makes the year current
for fy, fk in ((2023, "F2022"), (2026, "F2025")):
    assert min(g["published"] for g in EG if g["fy"] == fy and "eps_guide" in g) < SPUB[SID_K[fk]], fy

# ── dividends: each rate change from the first filing that states it as declared ──
DV = []
DIVQ = [(SID_DIV["0001039684-23-000006"], path("0001039684-23-000006", "8-K__*.rows.txt"),
         "On January 18, 2023, we announced that our board of directors increased our quarterly dividend to 95.5 cents per share of "
         "common stock, an increase of 2%", 0.955, "ONEOK 8-K"),
        (SID_DIV["0001039684-24-000004"], path("0001039684-24-000004", "8-K__*.rows.txt"),
         "On January 17, 2024, we announced that our board of directors declared a quarterly cash dividend of 99 cents per share of common "
         "stock, an increase of 3.7% from the previous quarter", 0.99, "ONEOK 8-K"),
        # from 2025 no dividend 8-K: the January 2025 and January 2026 increases are first stated in the Q4 releases
        (P["Q4 2024"], R_("Q4 2024"), "In January 2025, ONEOK increased its quarterly dividend 4% to $1.03 per share, or $4.12 per share "
         "annualized.", 1.03, "ONEOK Q4 2024 release"),
        (P["Q4 2025"], R_("Q4 2025"), "In January 2026, ONEOK increased its quarterly dividend 4% to $1.07 per share, or $4.28 per share "
         "annualized.", 1.07, "ONEOK Q4 2025 release")]
for sid, p, s, qd, doc in DIVQ:
    qt = quote(p, s)
    DV.append({"published": SPUB[sid], "quarterly": qd, "source": sid,
               "note": f"${qd:g} a quarter, ${qd * 4:g} a year: '{qt}' ({doc} of {SPUB[sid]})"})
# unchanged rates (read by their text)
for acc, w in (("0001039684-22-000006", "93.5 cents per share"), ("0001039684-22-000029", "93.5 cents per share"),
               ("0001039684-22-000053", "93.5 cents per share"), ("0001039684-22-000071", "93.5 cents per share"),
               ("0001628280-23-012601", "95.5 cents per share"), ("0001039684-23-000054", "95.5 cents per share"),
               ("0001039684-23-000077", "95.5 cents per share"), ("0001039684-24-000029", "99 cents per share"),
               ("0001039684-24-000120", "99 cents per share"), ("0001039684-24-000337", "99 cents per share"),
               ("0001039684-25-000056", "$1.03 per share"), ("0001039684-25-000107", "$1.03 per share")):
    t = joined(path(acc, "8-K__*.rows.txt"))
    assert w in t and "unchanged from the previous quarter" in t, acc
for q, w in (("Q3 2025", "$1.03 per share"), ("Q1 2026", "$1.07 per share"), ("Q2 2026", "$1.07 per share"), ("Q3 2026", "$1.07 per share")):
    assert re.search(r"declared a quarterly dividend of " + re.escape(w), joined(R_(q))), q
DV.sort(key=lambda x: x["published"])

# ── assemble ──
for k in ("history_vintages", "prints", "eps_guides", "dividends"):
    assert all(x["published"] <= "2021-12-31" for x in f[k]), k
f["sources"] = {**old["sources"], **dict(sorted(SOURCES.items(), key=lambda kv: int(kv[0][2:])))}
f["history_vintages"] = old["history_vintages"] + V
f["prints"] = old["prints"] + PR
f["eps_guides"] = old["eps_guides"] + EG
f["dividends"] = old["dividends"] + DV
f["_doc"] = old["_doc"].replace("gen_oke_1417.py (2014-2017) and gen_oke_1821.py (2018-2021)",
                                "gen_oke_1417.py (2014-2017), gen_oke_1821.py (2018-2021) and gen_oke_2226.py (2022-2026)")
assert "gen_oke_2226.py" in f["_doc"]
assert all(s["published"] <= CUT for s in f["sources"].values())
for k in ("rule_t", "listings", "company_names", "events", "guides", "splits", "distributions", "price_basis"):
    assert f[k] == old[k], k
YF = {dt.datetime.fromtimestamp(v["date"] + off, dt.timezone.utc).date().isoformat() for v in chart["events"]["splits"].values()}
assert not [d for d in YF if "2014-02-03" < d <= CUT], "a split or distribution in 2022-2026 needs its encoding"
out = A.out or os.path.join(REPO, "retro", "facts", "OKE.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(f, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_oke_2226.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump({k: v for k, v in CHECK.items() if v}, fh, ensure_ascii=False, indent=1)
print(f"{out}: +{len(V)} vintages, +{len(PR)} prints, +{len(EG)} EPS guides, +{len(DV)} dividends, +{len(SOURCES)} sources; "
      f"{sum(len(v) for v in CHECK.values())} quotes in {ck}")
for p in PR:
    print(p["quarter"], p["published"], p["sales_pct"], p["nm_pct"], p["opm_bp"], p["ptm_bp"], p["eps_q"], p["eps_q_prior"],
          p["diluted_shares_m"], p["release"])
for g in EG:
    print(g["fy"], g["published"], g["doc"], g.get("eps_guide") or "words")
for v in V:
    print(v["fy_label"], v["published"], v["eps_normalized"], v["groups"], v["cash_return_text"])
