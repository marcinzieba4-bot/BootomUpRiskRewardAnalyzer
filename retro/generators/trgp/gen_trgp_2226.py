#!/usr/bin/env python3
"""Extend retro/facts/TRGP.json with 2022-2026 (filings accepted 2021-12-31 to 2026-11-28), asserting that every earlier fact is unchanged.

The discipline of the 2012-2021 sheet (gen_trgp.py, gen_trgp_1417.py, gen_trgp_1821.py; retro/README.md, "TRGP" to "TRGP 2018-2021"): each
figure from its own row by label under an anchored heading, each quoted sentence asserted present in its own filing, every rate, margin,
tax rate and growth figure computed, a verbatim checklist written. Read: TRC's twenty earnings releases from Q4 2021 to Q3 2026, the
FY2021-FY2025 10-Ks (Item 6 is reserved in each, so the statements of operations and cash flows give three years; the segment note, Items 1,
1A and 7A), the fifteen 10-Qs of Q1 2022 to Q3 2026 (the releases print no EPS or share count: each 10-Q gives the quarter's EPS and shares
from its own date; no 10-K has selected quarterly data any more, so a fourth quarter's EPS stays n/r), the 8-K of 2022-06-17 (Exhibit 99.1,
the Lucid acquisition and the updated standalone 2022 outlook with its estimated net income), and every other 8-K of 2022-2026 by its item
text and exhibits. Run:

    python3 retro/tools/edgar.py index 1389170 <dir>
    python3 retro/tools/edgar.py fetch 1389170 <dir> --from 2021-12-31 --to 2026-11-28 --forms 10-K 10-Q 8-K 10-K/A 8-K/A 10-Q/A
    python3 -I retro/generators/trgp/gen_trgp_2226.py --filings <dir> --facts-in <the 2012-2021 sheet>
    python3 -I retro/tools/verbatim.py <dir>/checklist_trgp_2226.json

--facts-in is the 2012-2021 sheet (default retro/facts/TRGP.json, which must then hold no fact published after 2021-12-31; the generator
refuses a sheet that already holds one; gen_trgp.py, gen_trgp_1417.py and gen_trgp_1821.py regenerate it from the earlier filings). It
only appends.
"""
import argparse
import copy
import datetime as dt
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))       # retro/generators/trgp -> the repository
_ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("--filings", required=True, help="folder edgar.py wrote (allrows.json, tenk/, tenq/, eightk/); keep it outside the repo")
_ap.add_argument("--facts-in", help="the 2012-2021 fact sheet to extend (default retro/facts/TRGP.json)")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/TRGP.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_trgp_2226.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402  (the repo's own tool: trading days from the Yahoo cache)

ET = ZoneInfo("America/New_York")
START, CUT = "2021-12-31", "2026-11-28"
CIK = 1389170
FILINGS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("TRGP")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
CHECK = {}

FIN = A.facts_in or os.path.join(REPO, "retro", "facts", "TRGP.json")
with open(FIN, encoding="utf-8") as fh:
    facts = json.load(fh)
BEFORE = copy.deepcopy(facts)
_later = [p["published"] for k in ("prints", "history_vintages", "guides", "dividends") for p in facts[k] if p["published"] > START]
assert not _later, ("the input sheet already holds facts after 2021-12-31", _later[:3])


def norm(s):
    return re.sub(r"\s+", " ", s.replace(" ", " ")).strip()


def doc(acc, prefix):
    for sub in ("tenk", "tenq", "eightk", "other"):
        d = os.path.join(SP, sub, acc)
        if os.path.isdir(d):
            hits = sorted(f for f in os.listdir(d) if f.startswith(prefix) and f.endswith(".rows.txt"))
            assert len(hits) == 1, (acc, prefix, hits)
            return os.path.join(d, hits[0])
    raise AssertionError(acc)


TEXT, ORIG = {}, {}


def lines(path):
    if path not in TEXT:
        with open(path, encoding="utf-8", errors="replace") as fh:
            ORIG[path] = [norm(x) for x in fh.read().split("\n")]
        # the releases split a negative percentage over two cells: "(7 | %)" -> "(7%)" (the checklist keeps the original row)
        TEXT[path] = [re.sub(r"\((\d+) \| %\)", r"(\1%)", x) for x in ORIG[path]]
    return TEXT[path]


def full(path):
    return norm(" ".join(lines(path)))


def quote(path, s):
    """Assert a sentence or fragment is in its filing, word for word; add it to the checklist."""
    assert norm(s) in full(path), (path, s[:120])
    CHECK.setdefault(path, []).append(s)
    return s


def num(tok):
    t = tok.strip().replace("$", "").replace(",", "").strip()
    if t in ("—", "-", "–", ""):
        return 0.0
    neg = t.startswith("(") and t.endswith(")")
    v = float(t.strip("()%"))
    return -v if neg else v


DASH = lambda t: t.replace("—", "-").replace("–", "-")


def row(path, labels, start=0, stop=None, optional=False):
    """The unique row in lines[start:stop] whose first cell is one of `labels` (dashes normalized); (row, numeric values)."""
    labels = [labels] if isinstance(labels, str) else labels
    key = lambda x: re.sub(r"\s*-\s*", "-", DASH(x.split(" |")[0].strip()))
    want = {re.sub(r"\s*-\s*", "-", DASH(lb)) for lb in labels}
    L = lines(path)
    stop = len(L) if stop is None else stop
    hits = [k for k in range(start, min(stop, len(L))) if "|" in L[k] and key(L[k]) in want]
    if optional and not hits:
        return None, None
    assert len(hits) == 1, (path, labels, len(hits), [L[k] for k in hits[:3]], start, stop)
    r = L[hits[0]]
    vals = [None if t.strip() == "NM" else num(t) for t in r.split("|")[1:] if t.strip()]
    CHECK.setdefault(path, []).append(ORIG[path][hits[0]])
    return r, vals


def line_no(path, pred, start=0):
    L = lines(path)
    return next(i for i in range(start, len(L)) if pred(L[i]))


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
SRC = facts["sources"]


def source(sid, acc, title, path, supports):
    assert sid not in SRC, sid
    p, filed = published(acc)
    assert START < p <= CUT, (sid, p)
    fn = os.path.basename(path).split("__", 1)[1].replace(".rows.txt", ".htm")
    SRC[sid] = dict(published=p, filed=filed, title=title, url=URL(acc, fn), supports=supports)
    return sid


usd_m = lambda v: f"${v:,.1f}M" if v >= 0 else f"$({-v:,.1f})M"
pct = lambda a, b: round((b / a - 1) * 100, 1) if a > 0 else round((b - a) / abs(a) * 100, 1) if a < 0 else None
mg = lambda x, rev: round(x / rev * 100 + 0.0, 2)
bp = lambda x, rev, x0, rev0: round((mg(x, rev) - mg(x0, rev0)) * 100, 1)
eps_s = lambda v: "n/r" if v is None else (f"${v:.2f}" if v >= 0 else f"$({-v:.2f})")
SENT = r"(?:[^.]|\.(?=\d))*"                      # a sentence's body: no period except a decimal point

# ── filings ─────────────────────────────────────────────────────────────────────
REL = {"Q4 2021": "0001564590-22-006471", "Q1 2022": "0001564590-22-017997", "Q2 2022": "0001564590-22-027898",
       "Q3 2022": "0000950170-22-021492", "Q4 2022": "0000950170-23-003561", "Q1 2023": "0000950170-23-017422",
       "Q2 2023": "0000950170-23-037533", "Q3 2023": "0000950170-23-057723", "Q4 2023": "0000950170-24-015593",
       "Q1 2024": "0000950170-24-051550", "Q2 2024": "0000950170-24-088922", "Q3 2024": "0000950170-24-121056",
       "Q4 2024": "0000950170-25-023713", "Q1 2025": "0000950170-25-061423", "Q2 2025": "0001193125-25-174913",
       "Q3 2025": "0001193125-25-265621", "Q4 2025": "0001193125-26-058040", "Q1 2026": "0001193125-26-210165",
       "Q2 2026": "0001193125-26-336525", "Q3 2026": "0001193125-26-448401"}
FREL = {q: doc(a, "EX-99") for q, a in REL.items()}
SID = {q: f"TG{130 + i}" for i, q in enumerate(REL)}
K21, K22, K23, K24, K25 = ("0001564590-22-006563", "0000950170-23-003797", "0000950170-24-015841", "0000950170-25-023983",
                           "0001193125-26-059296")
TENQ = {"Q1 2022": "0001564590-22-018168", "Q2 2022": "0001564590-22-027962", "Q3 2022": "0000950170-22-021813",
        "Q1 2023": "0000950170-23-017657", "Q2 2023": "0000950170-23-037748", "Q3 2023": "0000950170-23-058137",
        "Q1 2024": "0000950170-24-051853", "Q2 2024": "0000950170-24-089135", "Q3 2024": "0000950170-24-121370",
        "Q1 2025": "0000950170-25-061595", "Q2 2025": "0001193125-25-175239", "Q3 2025": "0001193125-25-266435",
        "Q1 2026": "0001193125-26-211698", "Q2 2026": "0001193125-26-337729", "Q3 2026": "0001193125-26-449541"}
LUCID8K = "0001193125-22-176591"                                       # the 8-K of 2022-06-17: Lucid and the standalone 2022 outlook
REDEEM8K = "0001193125-22-107284"                                      # the 8-K of 2022-04-18: the Series A called for redemption
QK = {"Q4 2021": K21, "Q4 2022": K22, "Q4 2023": K23, "Q4 2024": K24, "Q4 2025": K25}   # the 10-K that follows each Q4 release

# ── release tables ──────────────────────────────────────────────────────────────


def ops_trc(path, yr):
    """TRC's releases: the consolidated statement of operations at the top; income before income taxes is net income less the income tax
    line (no pre-tax row; the LYB 2018 derivation, as in 2016-2021); the to-common deductions (Series A dividends, cash and deemed, and the
    premium on repurchase of noncontrolling interests) where printed; no EPS or share count."""
    i = line_no(path, lambda x: x.startswith("Total revenues |"))
    j = i + 40
    take = lambda v: None if v is None else ((v[0], v[1], v[4], v[5]) if yr else (v[0], v[1]))
    g = lambda lab, opt=False: take(row(path, lab, i, j, optional=opt)[1])
    vals = {"rev": g("Total revenues"), "oi": g("Income (loss) from operations"), "ni": g("Net income (loss)"),
            "tax": g("Income tax (expense) benefit"), "nit": g("Net income (loss) attributable to Targa Resources Corp."),
            "nia": g("Net income (loss) attributable to common shareholders"),
            "pref": g("Dividends on Series A Preferred Stock", True), "deemed": g("Deemed dividends on Series A Preferred Stock", True),
            "prem": g("Premium on repurchase of noncontrolling interests, net of tax", True)}
    vals["pti"] = tuple(round(n - t, 1) for n, t in zip(vals["ni"], vals["tax"]))
    zero = (0.0,) * len(vals["rev"])
    ded = [sum(x) for x in zip(*[vals[k] or zero for k in ("pref", "deemed", "prem")])]
    assert all(abs(t - d - c) < 0.15 for t, d, c in zip(vals["nit"], ded, vals["nia"])), (path, "TRC less the deductions = to common")
    return vals


def seg_trc(path):
    """The two segments: each one's first 'Operating margin' row under its own heading."""
    out = []
    for name in ("Gathering and Processing Segment", "Logistics and Transportation Segment"):
        h = line_no(path, lambda x: x == name)
        k = line_no(path, lambda x: x.startswith("Operating margin |"), h)
        assert k - h < 15, (path, name)
        v = row(path, "Operating margin", k, k + 1)[1]
        out.append((v[0], v[1]))
    return out[0], out[1]


def sentence(path, pattern, flags=0):
    m = re.search(pattern, full(path), flags)
    assert m, (path, pattern)
    return quote(path, m.group(0))


# ── prints ──────────────────────────────────────────────────────────────────────
QDATE = {1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"}
prints, dividends, OPS = [], [], {}
for q, acc in REL.items():
    f = FREL[q]
    qn, fy = int(q[1]), int(q[3:])
    o = ops_trc(f, qn == 4 or qn > 1)
    OPS[q] = o
    gp, lm = seg_trc(f)
    call = sentence(f, r"will host a conference call for the investment community at [^.]*? (a\.m\.|p\.m\.) Eastern [Tt]ime")
    pub, filed = published(acc)
    source(SID[q], acc, f"Targa Resources Corp. {q} results (8-K, Exhibit 99.1)", f,
           "Targa Resources Corp.'s consolidated results (revenues, income from operations, net income and the income tax line, net income "
           "attributable to TRC and to common shareholders and the deductions between them; no EPS or share count) and its two segments' "
           "operating margins, each with the year-ago quarter as this release shows it; the TRC dividend declared; the estimated net income "
           "attributable to TRC that reconciles its adjusted EBITDA outlook")
    raw = {"rev_m": o["rev"][0], "rev_prior_m": o["rev"][1], "oi_m": o["oi"][0], "oi_prior_m": o["oi"][1],
           "pti_m": o["pti"][0], "pti_prior_m": o["pti"][1], "eps_q": None, "eps_q_prior": None,
           "dil_sh_m": None, "gp_m": round(gp[0], 1), "gp_prior_m": round(gp[1], 1), "lm_m": round(lm[0], 1),
           "lm_prior_m": round(lm[1], 1), "nia_m": o["nia"][0]}
    pr = {"quarter": q, "fy": fy, "q": qn, "published": pub, "source": SID[q],
          "release": dt.date.fromisoformat(pub).strftime("%b %-d"),
          "release_time": f"8-K {filed}; {call}", "period_end": f"{fy}-{QDATE[qn]}", "raw": raw,
          "sales_b": round(raw["rev_m"] / 1000, 3), "sales_pct": pct(raw["rev_prior_m"], raw["rev_m"]),
          "opm": mg(raw["oi_m"], raw["rev_m"]), "opm_bp": bp(raw["oi_m"], raw["rev_m"], raw["oi_prior_m"], raw["rev_prior_m"]),
          "ptm": mg(raw["pti_m"], raw["rev_m"]), "ptm_bp": bp(raw["pti_m"], raw["rev_m"], raw["pti_prior_m"], raw["rev_prior_m"]),
          "eps_q": None, "eps_q_prior": None, "diluted_shares_m": None,
          "gp_pct": pct(raw["gp_prior_m"], raw["gp_m"]), "lm_pct": pct(raw["lm_prior_m"], raw["lm_m"]),
          "seg_note": (f"Gathering and Processing segment operating margin {usd_m(gp[0])} vs {usd_m(gp[1])}, Logistics and Transportation "
                       f"segment {usd_m(lm[0])} vs {usd_m(lm[1])} (TRC's two segments; the year-ago quarter as the release shows it)"),
          "sales_note": f"revenues {usd_m(raw['rev_m'])} vs {usd_m(raw['rev_prior_m'])}",
          "margin_note": (f"income from operations {usd_m(raw['oi_m'])} vs {usd_m(raw['oi_prior_m'])}; income before income taxes "
                          f"{usd_m(raw['pti_m'])} vs {usd_m(raw['pti_prior_m'])} (net income less the income tax line)"),
          "eps_note": ("GAAP, diluted: not in the release (TRC's releases print no per-share figure); net income attributable to common "
                       f"shareholders {usd_m(o['nia'][0])} vs {usd_m(o['nia'][1])}"),
          "next_print": f"the Q{qn % 4 + 1} {fy + (1 if qn == 4 else 0)} release"}
    i = line_no(f, lambda x: x.startswith("Total revenues |"))
    cr, cv = row(f, ["Distributable cash flow (1)", "Distributable cash flow (2)"], i, i + 45, optional=True)
    if cr is None:                                # from Q1 2024 the summary table's cash measure is adjusted free cash flow
        cr, cv = row(f, "Adjusted free cash flow (1)", i, i + 45)
    clab = re.sub(r" \(\d\)$", "", cr.split(" |")[0])
    pr["cash_note"] = f"TRC {clab[0].lower() + clab[1:]} {usd_m(cv[0])} (non-GAAP, display only)"
    dm = re.search(r"(?:TRC|Targa|the Company) declared (?:an increase to its |a )quarterly (?:cash )?dividend (?:of|to) (\$[\d.]+) per "
                   r"(?:share of its common stock|common share)(?: for the (?:first|second|third|fourth) quarter of \d{4})?", full(f))
    assert dm, (q, "dividend")
    quote(f, dm.group(0))
    rate = float(dm.group(1).strip("$"))
    dividends.append({"published": pub, "source": SID[q], "quarterly": round(rate, 5),
                      "note": f"${rate:.5f}".rstrip("0").rstrip(".") + f" a quarter, declared with the {q} release",
                      "quote": dm.group(0)})
    prints.append(pr)
PQ = {p["quarter"]: p for p in prints}

# ── EPS and diluted shares: each 10-Q from its own date (no 10-K has selected quarterly data: a Q4's EPS stays n/r) ──
QSH = {}                                          # basic weighted shares of each quarter (10-Q) or year (10-K), with the filing's source
for i, (q, acc) in enumerate(TENQ.items()):
    f = doc(acc, "10-Q__")
    sid = f"TG{150 + i}"
    source(sid, acc, f"Targa Resources Corp. {q} 10-Q", f, "the quarter's diluted EPS and weighted-average shares, with the year-ago "
           "quarter (the release prints neither)")
    n = line_no(f, lambda x: x == "CONSOLIDATED STATEMENTS OF OPERATIONS")
    e = row(f, "Net income (loss) per common share - diluted", n, n + 50)[1]
    s = row(f, "Weighted average shares outstanding - diluted", n, n + 50)[1]
    sb = row(f, "Weighted average shares outstanding - basic", n, n + 50)[1]
    nia = row(f, "Net income (loss) attributable to common shareholders", n, n + 50)[1]
    p = PQ[q]
    assert abs(nia[0] - p["raw"]["nia_m"]) < 1e-9, (q, "the 10-Q's income = the release's")
    QSH[q] = (sb[0], sid, SRC[sid]["published"], "basic weighted-average shares of the quarter")
    raw = {**p["raw"], "eps_q": e[0], "eps_q_prior": e[1], "dil_sh_m": s[0]}
    p["restated"] = [{"published": SRC[sid]["published"], "source": sid, "raw": raw, "eps_q": e[0], "eps_q_prior": e[1],
                      "diluted_shares_m": s[0],
                      "eps_note": f"GAAP, diluted, {eps_s(e[0])} against {eps_s(e[1])} a year earlier (the {q} 10-Q of {SRC[sid]['published']}; "
                                  "the release prints no per-share figure)"}]

# ── history vintages: Item 6 is reserved, so each 10-K gives three years from its statements, earlier years carried ──
PTI_L = ["Income (loss) before income taxes", "Income before income taxes"]


def stmt(path):
    """The consolidated statement of operations (three years) and the statement of cash flows."""
    i0 = max(k for k, x in enumerate(lines(path)) if x == "CONSOLIDATED STATEMENTS OF OPERATIONS")
    hdr = next(k for k in range(i0, i0 + 6) if re.fullmatch(r"20\d\d \| 20\d\d \| 20\d\d", lines(path)[k]))
    yrs = [int(y) for y in lines(path)[hdr].split(" | ")]
    e0 = min(i0 + 45, line_no(path, lambda x: x.startswith("CONSOLIDATED STATEMENTS OF COMPREHENSIVE"), i0))
    g = lambda lab, opt=False: row(path, lab, i0, e0, optional=opt)[1]
    out = {"rev": g("Total revenues"), "pti": g(PTI_L), "ni": g("Net income (loss)"),
           "nit": g("Net income (loss) attributable to Targa Resources Corp."),
           "nia": g("Net income (loss) attributable to common shareholders"),
           "sh": g("Weighted average shares outstanding - diluted"), "shb": g("Weighted average shares outstanding - basic"),
           "eps": g("Net income (loss) per common share - diluted"), "pref": g("Dividends on Series A Preferred Stock", True),
           "deemed": g("Deemed dividends on Series A Preferred Stock", True),
           "prem": g("Premium on repurchase of noncontrolling interests, net of tax", True),
           "imp": g("Impairment of long-lived assets", True),
           "gain": g(["Gain (loss) from sale of equity method investment", "Gain (loss) from sale of equity-method investment"], True)}
    c0 = line_no(path, lambda x: x == "CONSOLIDATED STATEMENTS OF CASH FLOWS", i0)
    out["cfo"] = row(path, ["Net cash provided by operating activities", "Net cash provided by (used in) operating activities"], c0, c0 + 90)[1]
    out["capex"] = row(path, "Outlays for property, plant and equipment", c0, c0 + 90)[1]
    dl = ["Dividends paid to common and Series A preferred shareholders", "Dividends paid to common and Series A Preferred shareholders",
          "Dividends paid to common shareholders"]
    divr, out["divs"] = row(path, dl, c0, c0 + 90)
    out["divlab"] = divr.split(" |")[0]
    return yrs, out


def groups2(path):
    """The two segments: the segment note's first operating margin row (display only)."""
    L = lines(path)
    n = max(k for k in range(len(L)) if re.match(r"Note \d+ . Segment Information$", L[k]))
    k = line_no(path, lambda x: x.startswith("Operating margin |") or x.startswith("Operating margin (1) |"), n)
    v = row(path, ["Operating margin", "Operating margin (1)"], k, k + 1)[1]
    if len(v) == 4:                                # 'Total Reportable Segments' then 'Other' (FY2024 on)
        assert abs(v[0] + v[1] - v[2]) < 0.15, (path, v)
    else:                                          # the two segments then 'Other'
        assert len(v) == 3, (path, v)
    return v[:2]


COMMODITY_OLD = "Our primary natural gas gathering and processing arrangements that expose us to commodity price risk are our percent-of-proceeds arrangements."
COMMODITY_NEW = ("Some of the commercial agreements in our natural gas gathering and processing business are percent-of-proceeds arrangements "
                 "that expose us to commodity price risk.")                    # the FY2024 and FY2025 10-Ks
RISK = ("Our cash flow is affected by supply and demand for natural gas, NGL products and crude oil and by natural gas, NGL, crude oil and "
        "condensate prices, and decreases in commodity prices and/or activity levels could adversely affect our results of operations and "
        "financial condition.")
REFSERV = ("In our refinery services business, we typically provide NGL balancing services through contractual arrangements with refiners in "
           "several locations to purchase and/or market propane and to supply butanes.")
GHG_RE = r"Our and our customers’ operations are subject to a number of risks (?:arising out of|related to) the (?:potential )?threat of climate change" + SENT + r"\."
# the Channelview Splitter, as each 10-K describes it (the theme clause: ENERGY_TRANSITION's refining read as out of scope)
SPLIT = {
    K21: (r"On December 26, 2018, Vitol Americas Corp\. \(“Vitol”\) filed a lawsuit" + SENT + r"\.", "the subject of the terminated "
          "agreement's litigation (Targa Channelview, sold in October 2020)"),
    K22: (r"On December 26, 2018, Vitol Americas Corp\. \(“Vitol”\) filed a lawsuit" + SENT + r"\.", "the subject of the terminated "
          "agreement's litigation (Targa Channelview, sold in October 2020)"),
    K23: (r"On December 26, 2018, Vitol Americas Corp\. \(“Vitol”\) filed a lawsuit" + SENT + r"\.", "the subject of the terminated "
          "agreement's litigation (Targa Channelview, sold in October 2020)"),
    K24: (r"On April 26, 2024 as a result of the final determination of Targa’s appeal" + SENT + r"\.", "a former subsidiary's "
          "agreement whose litigation ended with a payment"),
    K25: (r"The year ended December 31, 2024 includes \$55\.8 million of interest expense on a 2024 legal ruling" + SENT + r"\.",
          "a former subsidiary's agreement, named only for the 2024 ruling's interest")}
AI_RE = (r"Advances in computer capabilities, rapid changes and innovation in the field of artificial intelligence" + SENT + r"\.",
         r"As the breadth and complexity of the technologies we use continue to grow" + SENT + r"\.")

VS = [(K21, "TG120", "Targa Resources Corp. FY2021 10-K"), (K22, "TG121", "Targa Resources Corp. FY2022 10-K"),
      (K23, "TG122", "Targa Resources Corp. FY2023 10-K"), (K24, "TG123", "Targa Resources Corp. FY2024 10-K"),
      (K25, "TG124", "Targa Resources Corp. FY2025 10-K")]
prev = facts["history_vintages"][-1]
vintages, YSH = [], {}
TEN = lambda d, last: {y: d[y] for y in sorted(d, key=int, reverse=True) if last - 9 <= int(y) <= last}   # the ten fiscal years
for acc, sid, title in VS:
    f = doc(acc, "10-K__")
    assert quote(f, "Item 6. Reserved"), sid
    yrs, s = stmt(f)
    last = yrs[0]
    source(sid, acc, title, f, "the statements of operations and cash flows (three years: Item 6 is reserved), the segment note and the "
           "risk factors")
    YSH[last] = (s["shb"][0], sid, SRC[sid]["published"], "basic weighted-average shares of the year")
    tax = round(s["pti"][0] - s["ni"][0], 1)
    gv = groups2(f)
    own = {str(y): s["eps"][k] for k, y in enumerate(yrs) if s["eps"][k] > 0}
    eps_norm = {**own, **{y: v for y, v in prev["eps_normalized"].items() if int(y) < min(yrs)}}   # earlier years carried
    excl = {y: v for y, v in prev["eps_excluded"].items() if y not in own}
    for k, y in enumerate(yrs):
        if s["eps"][k] <= 0 and str(y) not in excl:
            excl[str(y)] = (f"{eps_s(s['eps'][k])} a diluted share for {y} (net loss attributable to common shareholders of "
                            f"{usd_m(s['nia'][k])} after the Series A preferred dividends): a loss, so no P/E (the F, MU and CRM loss rule); "
                            "its days leave the window")
    assert (s["eps"][0] > 0) == (last >= 2022), (sid, "2021 is the loss; 2022-2025 are positive")
    # the one-off test on the latest year (the items the Q4 release and the statement list; the AAPL FY2002 test and its mirror)
    nia = s["nia"][0]
    if last == 2021:
        items, note = round(s["imp"][0], 1), ("a loss: net loss attributable to common shareholders of $(16.1) million after the Series A "
                                                "preferred dividends; its listed item, the $452.3 million impairment of long-lived assets "
                                                "(pre-tax, SouthTX), is listed for completeness: a loss year has no P/E either way")
    elif last == 2022:
        ben = s["gain"][0]
        chg = round(s["deemed"][0] + s["prem"][0], 1)
        items = round(chg - ben, 1)
        note = (f"kept: the {usd_m(ben)} gain from the sale of the equity method investment (the GCX Sale; pre-tax, before the "
                f"noncontrolling interests, so an upper bound) less the {usd_m(s['deemed'][0])} of deemed dividends on the Series A "
                f"redemption and the {usd_m(s['prem'][0])} premium on repurchase of noncontrolling interests (the DevCo JV Repurchase) "
                f"nets to benefits of {usd_m(-items)} against {usd_m(nia)} attributable to common shareholders (the mirror test is not met)")
    elif last == 2023:
        items = s["prem"][0]
        note = (f"kept: the {usd_m(items)} premium on repurchase of noncontrolling interests, net of tax (the Grand Prix Transaction), "
                f"against {usd_m(nia)} attributable to common shareholders (the AAPL FY2002 test is not met: {items / nia * 100:.0f}% of it)")
    elif last == 2024:
        splitter = 55.8
        quote(f, "The year ended December 31, 2024 includes $55.8 million of interest expense associated with the Splitter Agreement ruling.")
        items = round(s["prem"][0] + splitter, 1)
        note = (f"kept: the {usd_m(s['prem'][0])} premium on repurchase of noncontrolling interests (the CBF Acquisition) and the $55.8 "
                f"million of interest on the Splitter Agreement ruling (pre-tax) against {usd_m(nia)} attributable to common shareholders")
    else:
        items = s["prem"][0]
        note = (f"kept: the {usd_m(items)} premium on repurchase of noncontrolling interests (the Badlands Transaction) against "
                f"{usd_m(nia)} attributable to common shareholders")
    oot = {"fy": last, "items_after_tax_m": items, "income_attributable_m": nia,
           "distorted": ((-items > nia + items) if items < 0 else (items > nia)),
           "kind": "benefits" if items < 0 else "charges", "note": note, "eps_gaap": s["eps"][0]}
    assert last == 2021 or not oot["distorted"], (sid, "no year of 2022-2025 is distorted")
    COMMODITY = COMMODITY_NEW if last >= 2024 else COMMODITY_OLD
    for k in (COMMODITY, RISK, REFSERV):
        quote(f, k)
    ghg = sentence(f, GHG_RE)
    s1 = sentence(f, SPLIT[acc][0])
    txt = full(f)
    assert not re.search(r"cyclical", txt, flags=re.I), (sid, "no 10-K of 2021-2025 says cyclical")
    for w in ("e-commerce", "streaming", "electric vehicle", "blockchain", "bitcoin", "cryptocurrenc", "digital asset", "GLP-1", "obesity",
              "generative"):
        assert not re.search(w, txt, flags=re.I), (sid, w)
    assert len(re.findall(r"crypto", txt, flags=re.I)) == len(re.findall(r"cryptography", txt, flags=re.I)), (sid, "crypto = cryptography")
    if re.search("artificial intelligence|cloud", txt, flags=re.I):
        a1, a2 = (sentence(f, x) for x in AI_RE)
        assert len(re.findall("artificial intelligence|cloud", txt, flags=re.I)) == len(re.findall("artificial intelligence|cloud", a1 + " " + a2,
                                                                                                   flags=re.I)), sid
        ai_text = (f"the {title} names artificial intelligence, cryptography and cloud only in its cybersecurity risk factor ('{a1}' "
                   f"'{a2}')")
        cloud_text = f"the {title} names cloud only in its cybersecurity risk factor"
    else:
        ai_text = f"the {title} does not name artificial intelligence"
        cloud_text = f"the {title} does not name cloud"
    revs = {**prev["revenue_usd_b"], **{str(y): round(s["rev"][k] / 1000, 4) for k, y in enumerate(yrs)}}
    rsrc = {**prev["revenue_sources"], **{str(y): sid for y in yrs}}
    revs, eps_norm, excl = TEN(revs, last), TEN(eps_norm, last), TEN(excl, last)
    rsrc = {y: rsrc[y] for y in revs}
    shares = TEN({**prev["diluted_shares_m"], **{str(y): s["sh"][k] for k, y in enumerate(yrs)}}, last)
    srcs = [sid] + [x for x in dict.fromkeys(rsrc.values()) if x != sid]
    v = {**{k: prev[k] for k in ("company", "exchange", "symbol", "pe_window_start", "kind", "margin_signal_name", "kind_text",
                                 "business_line")},
         "normalization": ("diluted EPS, GAAP, each year from the latest filing that reports it (from the FY2021 10-K, Item 6 being "
                           "reserved, three years from the statement of operations and earlier years from the latest earlier vintage); the "
                           "ten fiscal years to the latest one"),
         "published": SRC[sid]["published"], "sources": srcs,
         "fy_label": f"FY{last % 100:02d}", "fiscal_year_ends": {str(last): f"{last}-12-31"},
         "eps_normalized": eps_norm, "eps_excluded": excl,
         "revenue_usd_b": revs, "revenue_sources": rsrc,
         "revenue_note": ("consolidated revenues; each year from the latest 10-K that reports it (three years from each statement of "
                          "operations from the FY2021 10-K); the ten fiscal years to the latest one; 2018 on under ASC 606, 2017 and earlier "
                          "as first reported (a seam)"),
         "diluted_shares_m": shares,
         "shares_note": ("diluted weighted-average shares of the statements of operations, the ten fiscal years to the latest one; 2016 "
                         "includes the 104.5M shares issued for the Partnership's public common units"),
         "prev_fy_op_margin": mg(s["pti"][0], s["rev"][0]),
         "prev_fy_op_margin_note": f"FY{last % 100:02d} income before income taxes {usd_m(s['pti'][0])} / revenues {usd_m(s['rev'][0])} ({title})",
         "prev_fy_sales_growth": pct(s["rev"][1], s["rev"][0]),
         "check_pretax_margin": mg(s["pti"][0], s["rev"][0]),
         "check_pretax_note": f"FY{last % 100:02d} income before income taxes / revenues ({title}), before the noncontrolling interests",
         "tax_rate": round(tax / s["pti"][0], 3),
         "tax_note": (f"FY{last % 100:02d} effective rate: income tax {usd_m(tax)} (income before income taxes less net income) on "
                      f"{usd_m(s['pti'][0])} ({title})"),
         "dividend_annual": None, "dividend_note": None,
         "fcf_b": round((s["cfo"][0] + s["capex"][0]) / 1000, 3), "fcf_label": f"FY{last % 100:02d}",
         "fcf_note": (f"consolidated net cash provided by operating activities {usd_m(s['cfo'][0])} less outlays for property, plant and "
                      f"equipment {usd_m(-s['capex'][0])} ({title})"),
         "cash_return_text": f"{usd_m(-s['divs'][0])} of {s['divlab'][0].lower() + s['divlab'][1:]} in FY{last % 100:02d}",
         "groups": [["Gathering and Processing", round(gv[0] / 1000, 4), None], ["Logistics and Transportation", round(gv[1] / 1000, 4), None]],
         "groups_basis": (f"FY{last % 100:02d} segment operating margin, USD bn ({title}'s segment note; 'Other', the hedges, and Corporate "
                          "and Eliminations left out)"),
         "why": (f"Commodity exposure ({title}): {COMMODITY} Risk factor: '{RISK}' The {title} does not call the business cyclical (the "
                 "dividend policy's 'seasonal and cyclical factors' of the earlier 10-Ks no longer appears); no theme in taxonomy_eras.json "
                 "is live for a midstream natural gas company on this date"),
         "ghg_quote": ghg, "refinery_quote": REFSERV, "tenk_label": title,
         "splitter_text": f"the Channelview Splitter is {SPLIT[acc][1]}: '{s1}'",
         "cloud_text": cloud_text,
         # (TRGP 2022-2026) the vintage's own words on artificial intelligence (GENAI live 2022-11-30), text only
         "ai_text": ai_text,
         "one_off_test": oot}
    vintages.append(v)
    prev = v

# every Q4 release's year reaches the models only through its 10-K, which is public by the first weekly date after the release
for q, k in QK.items():
    kp = SRC[next(x for a, x, _ in VS if a == k)]["published"]
    assert kp <= next_tday(PQ[q]["published"]), (q, "the 10-K comes after the first weekly date", kp)

# ── outlooks: each release's adjusted EBITDA outlook (display only) and the estimated net income attributable to TRC that reconciles it (a
#    GAAP earnings guide: the KMI 2019-2022 rule and the TRGP 2018-2021 encoding; per share as below) ──
F8 = doc(LUCID8K, "EX-99.1__")
source("TG34", LUCID8K, "Targa Resources Corp. Lucid acquisition and updated standalone 2022 outlook (8-K of 2022-06-17, Exhibit 99.1)", F8,
       "TRC's updated standalone 2022 adjusted EBITDA outlook and the estimated standalone net income attributable to TRC that reconciles it")
FR = doc(REDEEM8K, "EX-99.1__")
source("TG35", REDEEM8K, "Targa Resources Corp. full redemption of its 9.5% Series A Preferred Stock (8-K of 2022-04-18, Exhibit 99.1)", FR,
       "the call of every Series A preferred share for redemption on May 3, 2022")
REDEEM_Q = quote(FR, "Following the redemption, there will be no Series A Preferred Stock outstanding, dividends on the Series A Preferred "
                     "Stock will cease to accumulate and all rights of the holders of shares of Series A Preferred Stock will terminate, except "
                     "the right of such holders to receive the Redemption Consideration (as defined below).")
REDEEMED = quote(FREL["Q1 2022"], "In May 2022, Targa redeemed in full all of the Company’s issued and outstanding shares of Series A Preferred.")
R_PUB = PQ["Q1 2022"]["published"]                # from this release no Series A is outstanding


def ni_guide(path, fy):
    """The reconciliation of estimated net income attributable to TRC to estimated adjusted EBITDA: its first row."""
    h = line_no(path, lambda x: x.startswith("Reconciliation of Estimated Net Income") and ("TRC" in x or "Targa Resources Corp" in x))
    yl = next(k for k in range(h - 4, h) if re.fullmatch(rf"{fy}E", lines(path)[k]))
    r, v = row(path, ["Net income attributable to TRC", "Net income attributable to Targa Resources Corp."], h, h + 4)
    assert len(v) == 1 and yl, (path, r)
    return v[0], r


EB_RE = (r"(?:For (?:full year )?20\d\d, )?(?:Targa|the Company|The Company)[^.]*?(?:estimates?|expects?|expectation|maintains)[^.]*?"
         r"adjusted EBITDA" + SENT + r"\$[\d.,]+ (?:billion|million)" + SENT)
guides = []
GQ = list(REL) + ["8-K"]
for q in sorted(GQ, key=lambda x: SRC["TG34"]["published"] if x == "8-K" else PQ[x]["published"]):
    path = F8 if q == "8-K" else FREL[q]
    pub = SRC["TG34"]["published"] if q == "8-K" else PQ[q]["published"]
    gfy = (int(q[3:]) + 1 if q.startswith("Q4") else int(q[3:])) if q != "8-K" else 2022
    ni, r = ni_guide(path, gfy)
    m = re.search(EB_RE, full(path)) or re.search(r"Continue to estimate full year 20\d\d adjusted EBITDA" + SENT, full(path))
    assert m, (q, "adjusted EBITDA outlook")
    t_ = full(path)                                # the whole sentence: back to the previous sentence or bullet boundary
    b = max(t_.rfind(". ", 0, m.start()) + 2, t_.rfind("• ", 0, m.start()) + 2, t_.rfind("| ", 0, m.start()) + 2,
            t_.rfind("Outlook ", 0, m.start()) + 8 if t_.rfind("Outlook ", 0, m.start()) > t_.rfind(". ", 0, m.start()) else 0)
    eb = t_[b:m.end()].strip()
    eb = next(x for x in re.split(r" • \| | • | \| ", eb) if "adjusted EBITDA" in x and "$" in x)     # one bullet, not its neighbours
    eb = re.split(r" On [A-Z][a-z]+ \d+, \d{4}, the Company declared", eb)[0]
    eb = re.sub(r"^(?:and Capital (?:Return Expectations|Allocation Update)|\d{4} Updated Financial Estimates) ", "", eb)
    eb = quote(path, eb)
    dv = re.search(rf"[^.•]*annual(?:ized)? common (?:stock )?dividend[^.]*?\$[\d.]+ per share (?:for|in) {gfy}" + SENT, full(path))
    dvq = quote(path, dv.group(0).strip()) if dv else None
    # the per-share figure: net income attributable to TRC less the to-common deductions, over the latest basic weighted-average share count
    # public on the guide's own date (a 10-Q's quarter or a 10-K's year; the releases print none):
    #  - while the Series A is outstanding (to the Q4 2021 release), its dividends at the release's own quarter's rate, cash and deemed, x4
    #    (the TRGP 2018-2021 rule, unchanged);
    #  - (new, TRGP 2022-2026) once a filing states it redeemed in full (the Q1 2022 release, 2022-05-05), no preferred dividend recurs, and
    #    the deduction is what the latest statement of operations public on the guide's date has already deducted for the guide's own year
    #    (Series A dividends, cash and deemed, and the premium on repurchase of noncontrolling interests, year to date); a guide for a year
    #    that statement does not reach (a Q4 release's next year) deducts nothing. Decided before any 2022-2026 model was built.
    sq = "Q1 2022" if q == "8-K" else q
    o = OPS[sq]
    if pub < R_PUB:
        pc, pd = o["pref"][0], (o["deemed"] or (0.0,))[0]
        ded = {"pref_q_m": [pc, pd], "pref_source": SID[sq]}
    else:
        yfy = int(sq[3:])
        if yfy == gfy:
            ytd = {k: (o[k][2] if len(o[k]) == 4 else o[k][0]) if o[k] else 0.0 for k in ("pref", "deemed", "prem")}
            d = round(sum(ytd.values()), 1)
            why = ", ".join(f"{lab} {usd_m(ytd[k])}" for k, lab in (("pref", "Series A dividends"), ("deemed", "deemed dividends"),
                                                                     ("prem", "premium on repurchase of noncontrolling interests"))
                            if ytd[k])
            how = (f"{usd_m(d)} deducted for {gfy} to date in the {sq} release's statement ({why})" if d else
                   f"nothing deducted for {gfy} to date in the {sq} release's statement")
        else:
            d, how = 0.0, f"no deduction recorded for {gfy} yet (the {sq} release's statement ends with {yfy})"
        ded = {"deduct_ytd_m": d, "deduct_source": SID[sq],
               "deduct_note": f"no Series A outstanding from the Q1 2022 release ('{REDEEMED}'): {how}"}
    sh, ssid, spub, sdesc = max((x for x in list(QSH.values()) + list(YSH.values()) if x[2] <= pub), key=lambda x: (x[2], x[1]))
    g = {"fy": gfy, "published": pub, "source": "TG34" if q == "8-K" else SID[q], "rev_none": True,
         "ni_trc_est_m": ni, **ded, "shares_basic_m": sh, "shares_source": ssid,
         "shares_note": f"{sdesc} ({SRC[ssid]['title']}, {spub})",
         "ni_row": r,
         "doc": ("8-K of 2022-06-17" if q == "8-K" else f"{q} release"),
         "display": (f"TRC {gfy} outlook ({'the 8-K of 2022-06-17, standalone, before the Lucid acquisition' if q == '8-K' else 'the ' + q + ' release'}): "
                     f"'{eb}' (adjusted EBITDA, non-GAAP, display only)" + (f"; '{dvq}' (display only)" if dvq else "")
                     + f", reconciled to an estimated net income attributable to TRC of {usd_m(ni)}; no revenue or margin guide")}
    guides.append(g)
for g in guides:
    if g["published"] < min(x[2] for x in list(QSH.values()) + list(YSH.values())):
        raise AssertionError(("a guide before any 2022 count", g["published"]))

# ── append ──────────────────────────────────────────────────────────────────────
facts["history_vintages"] += vintages
facts["prints"] += prints
facts["guides"] += guides
facts["dividends"] += dividends
for k in ("history_vintages", "prints", "guides", "dividends"):
    n = len(BEFORE[k])
    assert facts[k][:n] == BEFORE[k], (k, "an earlier fact changed")
assert {k: v for k, v in facts["sources"].items() if k in BEFORE["sources"]} == BEFORE["sources"]
assert facts["rule_t"] == BEFORE["rule_t"], "rule T stays frozen at 2012-02-24"
assert facts["revenue_restatements"] == BEFORE["revenue_restatements"]
# dated by the release that states the redemption done (from which the guides deduct the year's recorded amounts); the call's 8-K, TG35,
# carries its own date in the sources
facts["series_a_redemption"] = {"published": R_PUB, "source": SID["Q1 2022"], "quote": REDEEMED, "call_source": "TG35",
                                "call_quote": REDEEM_Q}
facts["_doc"] = BEFORE["_doc"] + (" 2022-2026 appended by retro/generators/trgp/gen_trgp_2226.py from the same filings' rows, every earlier "
                                  "fact asserted unchanged.")
out = A.out or os.path.join(REPO, "retro", "facts", "TRGP.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(facts, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_trgp_2226.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump(CHECK, fh, ensure_ascii=False, indent=1)
print(out, len(prints), "prints", len(vintages), "vintages", len(dividends), "dividends", len(guides), "guides",
      sum(len(v) for v in CHECK.values()), "checked strings")
for p in prints:
    print(p["quarter"], p["published"], p["sales_pct"], p["gp_pct"], p["lm_pct"], p["opm_bp"], p["ptm_bp"],
          [(r["published"], r["eps_q"], r.get("diluted_shares_m")) for r in p.get("restated", [])])
for v in vintages:
    print(v["fy_label"], v["published"], v["eps_normalized"], sorted(v["eps_excluded"]), v["diluted_shares_m"], v["tax_rate"], v["groups"],
          v["one_off_test"]["items_after_tax_m"], v["one_off_test"]["income_attributable_m"])
for g in guides:
    print(g["fy"], g["published"], g.get("ni_trc_est_m"), g.get("pref_q_m"), g.get("deduct_ytd_m"), g.get("shares_basic_m"), g.get("shares_source"))
