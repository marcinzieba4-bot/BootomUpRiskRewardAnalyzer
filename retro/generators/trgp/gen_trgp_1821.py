#!/usr/bin/env python3
"""Extend retro/facts/TRGP.json with 2018-2021 (filings accepted 2017-12-31 to 2021-12-31), asserting that every earlier fact is unchanged.

The discipline of the 2012-2017 sheet (gen_trgp.py, gen_trgp_1417.py; retro/README.md, "TRGP" to "TRGP 2014-2017"): each figure from its own
row by label under an anchored heading, each quoted sentence asserted present in its own filing, every rate, margin, tax rate and growth
figure computed, a verbatim checklist written. Read: TRC's sixteen earnings releases from Q4 2017 to Q3 2021, the FY2017-FY2020 10-Ks
(Item 6, the statements of operations and cash flows, the selected quarterly data to FY2019, the segment note, Items 1, 1A and 7A), the
twelve 10-Qs of 2018-2021 (the releases print no EPS or share count: each 10-Q gives the quarter's EPS and shares from its own date, and a
Q4's EPS comes from the next 10-K's selected quarterly data, which the FY2020 10-K no longer has), the outlook 8-K of 2020-10-05 (Exhibit
99.1), and every other 8-K of 2018-2021 by its item text and exhibits. New in this batch: from the Q4 2018 release each release reconciles
its Adjusted EBITDA outlook to an estimated GAAP net income attributable to TRC for the year, a GAAP earnings guide (the KMI 2019-2022
rule; its per-share figure is derived here, retro/README.md, "TRGP 2018-2021"). Run:

    python3 retro/tools/edgar.py index 1389170 <dir>
    python3 retro/tools/edgar.py fetch 1389170 <dir> --from 2017-12-31 --to 2021-12-31 --forms 10-K 10-Q 8-K 10-K/A 8-K/A 10-Q/A
    python3 -I retro/generators/trgp/gen_trgp_1821.py --filings <dir> --facts-in <the 2012-2017 sheet>
    python3 -I retro/tools/verbatim.py <dir>/checklist_trgp_1821.json

--facts-in is the 2012-2017 sheet (default retro/facts/TRGP.json, which must then hold no fact published after 2017-12-31; the generator
refuses a sheet that already holds one; gen_trgp.py and gen_trgp_1417.py regenerate it from the earlier filings). It only appends.
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
_ap.add_argument("--facts-in", help="the 2012-2017 fact sheet to extend (default retro/facts/TRGP.json)")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/TRGP.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_trgp_1821.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402  (the repo's own tool: trading days from the Yahoo cache)

ET = ZoneInfo("America/New_York")
START, CUT = "2017-12-31", "2021-12-31"
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
assert not _later, ("the input sheet already holds facts after 2017-12-31", _later[:3])


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
    v = float(t.strip("()%"))
    return -v if neg else v


DASH = lambda t: t.replace("—", "-").replace("–", "-")


def row(path, labels, start=0, stop=None):
    """The unique row in lines[start:stop] whose first cell is one of `labels` (dashes normalized); (row, numeric values)."""
    labels = [labels] if isinstance(labels, str) else labels
    key = lambda x: re.sub(r"\s*-\s*", "-", DASH(x.split(" |")[0].strip()))
    want = {re.sub(r"\s*-\s*", "-", DASH(lb)) for lb in labels}
    L = lines(path)
    stop = len(L) if stop is None else stop
    hits = [k for k in range(start, min(stop, len(L))) if "|" in L[k] and key(L[k]) in want]
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

# ── filings ─────────────────────────────────────────────────────────────────────
REL = {"Q4 2017": "0001564590-18-002150", "Q1 2018": "0001564590-18-010494", "Q2 2018": "0001564590-18-020722",
       "Q3 2018": "0001564590-18-028248", "Q4 2018": "0001564590-19-003346", "Q1 2019": "0001564590-19-016180",
       "Q2 2019": "0001564590-19-030408", "Q3 2019": "0001564590-19-041347", "Q4 2019": "0001564590-20-005394",
       "Q1 2020": "0001564590-20-022319", "Q2 2020": "0001564590-20-037193", "Q3 2020": "0001564590-20-050801",
       "Q4 2020": "0001564590-21-006487", "Q1 2021": "0001564590-21-024441", "Q2 2021": "0001564590-21-041137",
       "Q3 2021": "0001564590-21-054197"}
FREL = {q: doc(a, "EX-99.1__") for q, a in REL.items()}
SID = {q: f"TG{80 + i}" for i, q in enumerate(REL)}
K17, K18, K19, K20 = "0001564590-18-002330", "0001564590-19-005727", "0001564590-20-005592", "0001564590-21-006640"
TENQ = {"Q1 2018": "0001564590-18-010735", "Q2 2018": "0001564590-18-020681", "Q3 2018": "0001564590-18-028429",
        "Q1 2019": "0001564590-19-017121", "Q2 2019": "0001564590-19-030955", "Q3 2019": "0001564590-19-041853",
        "Q1 2020": "0001564590-20-022780", "Q2 2020": "0001564590-20-037565", "Q3 2020": "0001564590-20-051164",
        "Q1 2021": "0001564590-21-024819", "Q2 2021": "0001564590-21-041376", "Q3 2021": "0001564590-21-054348"}
OUT8K = "0001193125-20-263201"                                          # the 8-K of 2020-10-05: the updated 2020 outlook
# the 10-K that publishes each Q4's EPS (its selected quarterly data) and each year's basic shares
QK = {"Q4 2017": K17, "Q4 2018": K18, "Q4 2019": K19}

# ── release tables ──────────────────────────────────────────────────────────────


def ops_trc(path, yr):
    """TRC's releases: the summary table at the top; income before income taxes is net income less the income tax line (the table
    prints no pre-tax row; the LYB 2018 derivation, as in 2016-2017); no EPS or share count."""
    i = line_no(path, lambda x: x.startswith("Total revenues |"))
    j = i + 40
    take = lambda v: (v[0], v[1], v[4], v[5]) if yr else (v[0], v[1])
    vals = {"rev": take(row(path, "Total revenues", i, j)[1]),
            "oi": take(row(path, ["Income (loss) from operations", "Income from operations"], i, j)[1]),
            "ni": take(row(path, ["Net income (loss)", "Net income"], i, j)[1]),
            "tax": take(row(path, "Income tax (expense) benefit", i, j)[1]),
            "nia": take(row(path, ["Net income (loss) attributable to common shareholders",
                                   "Net income attributable to common shareholders"], i, j)[1]),
            "pref": take(row(path, "Dividends on Series A Preferred Stock", i, j)[1]),
            "deemed": take(row(path, "Deemed dividends on Series A Preferred Stock", i, j)[1])}
    vals["pti"] = tuple(round(n - t, 1) for n, t in zip(vals["ni"], vals["tax"]))
    return vals


def seg_trc(path):
    """The two segments: each one's first 'Operating margin' row under its own heading (Logistics and Marketing, renamed Logistics and
    Transportation from the Q4 2019 release with no change to reported results)."""
    out = []
    for names in (("Gathering and Processing Segment",), ("Logistics and Marketing Segment", "Logistics and Transportation Segment")):
        h = line_no(path, lambda x: x in names)
        k = line_no(path, lambda x: x.startswith("Operating margin |"), h)
        assert k - h < 15, (path, names)
        v = row(path, "Operating margin", k, k + 1)[1]
        out.append((v[0], v[1]))
    return out[0], out[1]


def sentence(path, pattern):
    full = norm(" ".join(lines(path)))
    m = re.search(pattern, full)
    assert m, (path, pattern)
    return quote(path, m.group(0))


RENAME = None                                    # the Q4 2019 release's sentence on the renamed segment

# ── prints ──────────────────────────────────────────────────────────────────────
QDATE = {1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"}
prints, dividends, PREF = [], [], {}
for q, acc in REL.items():
    f = FREL[q]
    qn, fy = int(q[1]), int(q[3:])
    o = ops_trc(f, qn == 4)
    gp, lm = seg_trc(f)
    renamed = (fy, qn) >= (2019, 4)
    if (fy, qn) == (2019, 4):
        RENAME = quote(f, "In the fourth quarter of 2019, we renamed the Logistics and Marketing segment as “Logistics and Transportation.” The "
                          "updated name better describes the business composition and activity of the segment given the recent completion of "
                          "Grand Prix. The change in naming convention did not impact previously reported results for the segment.")
    call = sentence(f, r"will host a conference call for the investment community at [^.]*? (a\.m\.|p\.m\.) Eastern [Tt]ime")
    pub, filed = published(acc)
    source(SID[q], acc, f"Targa Resources Corp. {q} results (8-K, Exhibit 99.1)", f,
           "Targa Resources Corp.'s consolidated results (revenues, income from operations, net income and the income tax line, net income "
           "attributable to common shareholders and the Series A preferred dividends; no EPS or share count) and its two segments' operating "
           "margins, each with the year-ago quarter as this release shows it; the TRC dividend declared"
           + ("; the estimated net income attributable to TRC that reconciles its Adjusted EBITDA outlook" if (fy, qn) >= (2018, 4) and
              (fy, qn) not in ((2019, 1), (2019, 2), (2019, 3)) else ""))
    raw = {"rev_m": o["rev"][0], "rev_prior_m": o["rev"][1], "oi_m": o["oi"][0], "oi_prior_m": o["oi"][1],
           "pti_m": o["pti"][0], "pti_prior_m": o["pti"][1], "eps_q": None, "eps_q_prior": None,
           "dil_sh_m": None, "gp_m": round(gp[0], 1), "gp_prior_m": round(gp[1], 1), "lm_m": round(lm[0], 1),
           "lm_prior_m": round(lm[1], 1), "nia_m": o["nia"][0]}
    PREF[q] = (o["pref"][0], o["deemed"][0])
    lmname = "Logistics and Transportation segment (the former Logistics and Marketing, renamed)" if renamed else "Logistics and Marketing segment"
    pr = {"quarter": q, "fy": fy, "q": qn, "published": pub, "source": SID[q],
          "release": dt.date.fromisoformat(pub).strftime("%b %-d"),
          "release_time": f"8-K {filed}; {call}", "period_end": f"{fy}-{QDATE[qn]}", "raw": raw,
          "sales_b": round(raw["rev_m"] / 1000, 3), "sales_pct": pct(raw["rev_prior_m"], raw["rev_m"]),
          "opm": mg(raw["oi_m"], raw["rev_m"]), "opm_bp": bp(raw["oi_m"], raw["rev_m"], raw["oi_prior_m"], raw["rev_prior_m"]),
          "ptm": mg(raw["pti_m"], raw["rev_m"]), "ptm_bp": bp(raw["pti_m"], raw["rev_m"], raw["pti_prior_m"], raw["rev_prior_m"]),
          "eps_q": None, "eps_q_prior": None, "diluted_shares_m": None,
          "gp_pct": pct(raw["gp_prior_m"], raw["gp_m"]), "lm_pct": pct(raw["lm_prior_m"], raw["lm_m"]),
          "seg_note": (f"Gathering and Processing segment operating margin {usd_m(gp[0])} vs {usd_m(gp[1])}, {lmname} {usd_m(lm[0])} vs "
                       f"{usd_m(lm[1])} (TRC's two segments; the year-ago quarter as the release shows it)"),
          "sales_note": f"revenues {usd_m(raw['rev_m'])} vs {usd_m(raw['rev_prior_m'])}",
          "margin_note": (f"income from operations {usd_m(raw['oi_m'])} vs {usd_m(raw['oi_prior_m'])}; income before income taxes "
                          f"{usd_m(raw['pti_m'])} vs {usd_m(raw['pti_prior_m'])} (net income less the income tax line)"),
          "eps_note": ("GAAP, diluted: not in the release (TRC's releases print no per-share figure); net income attributable to common "
                       f"shareholders {usd_m(o['nia'][0])} vs {usd_m(o['nia'][1])}"),
          "next_print": f"the Q{qn % 4 + 1} {fy + (1 if qn == 4 else 0)} release"}
    full = norm(" ".join(lines(f)))
    m = (re.search(r"The Company reported distributable cash flow for the (?:fourth|third|second|first) quarter of \d{4} of "
                   r"\$([\d.]+) million", full)
         or re.search(r"The Company reported distributable cash flow and (?:adjusted )?free cash flow before dividends for the "
                      r"(?:fourth|third|second|first) quarter of \d{4} of \$([\d.]+) million", full))
    assert m, (q, "TRC distributable cash flow")
    quote(f, m.group(0))
    pr["cash_note"] = f"TRC distributable cash flow ${float(m.group(1)):.1f}M (non-GAAP, display only)"
    dm = re.search(r"TRC declared a quarterly dividend of (\$[\d.]+) per share of its common stock for the three months ended "
                   r"[A-Za-z]+ \d+, \d{4}", full)
    assert dm, (q, "dividend")
    quote(f, dm.group(0))
    rate = float(dm.group(1).strip("$"))
    dividends.append({"published": pub, "source": SID[q], "quarterly": round(rate, 5),
                      "note": f"${rate:.5f}".rstrip("0").rstrip(".") + f" a quarter, declared for {q} (the {q} release)",
                      "quote": dm.group(0)})
    if qn == 4:                                   # the year: the release's year columns
        yr = {k: v[2] for k, v in o.items()}
        yr0 = {k: v[3] for k, v in o.items()}
        tax = round(yr["pti"] - yr["ni"], 1)
        i = line_no(f, lambda x: x.startswith("Total revenues |"))
        if fy == 2017:
            quote(f, "The fourth quarter of 2017, in connection with the Company’s initial analysis of the impact of the U.S. government’s "
                     "recently enacted comprehensive tax legislation commonly referred to as the Tax Cuts and Jobs Act (the “Tax Act”), "
                     "included a discrete net deferred tax benefit of $269.5 million.")
            imp = row(f, "Impairment of property, plant and equipment", i, i + 40)[1][4]
            items = round(imp - 269.5, 1)
            note = ("a loss: net loss attributable to common shareholders of $(63.4) million after the Series A preferred dividends (the "
                    "release prints no per-share figure); its listed items, the $378.0 million impairment of property, plant and equipment "
                    "(pre-tax) and the $269.5 million discrete net deferred tax benefit of the Tax Act, net to charges of $108.5 million and "
                    "are listed for completeness: a loss year has no P/E either way")
        elif fy == 2018:
            imp = row(f, "Impairment of goodwill", i, i + 40)[1][4]
            items = imp
            note = ("a loss: net loss attributable to common shareholders of $(119.3) million after the Series A preferred dividends (the "
                    f"release prints no per-share figure); its listed item, the {usd_m(imp)} impairment of goodwill (pre-tax), is listed for "
                    "completeness: a loss year has no P/E either way")
        elif fy == 2019:
            imp = row(f, "Impairment of property, plant and equipment", i, i + 40)[1][4]
            items = imp
            note = ("a loss: net loss attributable to common shareholders of $(334.0) million after the Series A preferred dividends (the "
                    f"release prints no per-share figure); its listed item, the {usd_m(imp)} impairment of property, plant and equipment "
                    "(pre-tax), is listed for completeness: a loss year has no P/E either way")
        else:
            imp = row(f, "Impairment of long-lived assets", i, i + 40)[1][2]
            items = imp
            note = ("a loss: net loss attributable to common shareholders of $(1,684.8) million after the Series A preferred dividends (the "
                    f"release prints no per-share figure); its listed item, the {usd_m(imp)} impairment of long-lived assets (pre-tax, the "
                    "first quarter), is listed for completeness: a loss year has no P/E either way")
        assert yr["nia"] < 0, (q, "every year of 2017-2020 is a loss to common shareholders")
        fa = {"fy": fy, "fy_label": f"FY{fy % 100:02d}", "eps_normalized": None, "eps_gaap": None,
              "excluded_note": (f"a loss: net loss attributable to common shareholders of {usd_m(yr['nia'])} for {fy} (the {q} release, which "
                                "prints no per-share figure), so no P/E (the F, MU and CRM loss rule)"),
              "revenue_usd_b": round(yr["rev"] / 1000, 4),
              "normalization_note": f"FY{fy % 100:02d} a loss to common shareholders, from the {q} release ({pub}) until the 10-K",
              "op_margin": mg(yr["pti"], yr["rev"]),
              "op_margin_note": f"FY{fy % 100:02d} income before income taxes {usd_m(yr['pti'])} / revenues {usd_m(yr['rev'])} ({q} release)",
              "sales_growth": pct(yr0["rev"], yr["rev"]), "check_pretax_margin": mg(yr["pti"], yr["rev"]),
              "check_pretax_note": f"FY{fy % 100:02d} income before income taxes / revenues ({q} release), before the noncontrolling interests",
              "tax_rate": round(tax / yr["pti"], 3),
              "tax_note": f"FY{fy % 100:02d} effective rate: income tax {usd_m(tax)} (income before income taxes less net income) on {usd_m(yr['pti'])}",
              "one_off_test": {"items_after_tax_m": items, "income_attributable_m": yr["nia"],
                               "distorted": ((-items > yr["nia"] + items) if items < 0 else (items > yr["nia"])),
                               "kind": "benefits" if items < 0 else "charges", "note": note}}
        pr["fy_actual"] = fa
    prints.append(pr)
PQ = {p["quarter"]: p for p in prints}
assert RENAME

# ── EPS and diluted shares: each 10-Q from its own date; a Q4 from the next 10-K's selected quarterly data (to FY2019) ──
QSH = {}                                          # basic weighted shares of each quarter (10-Q) or year (10-K), with the filing's source
for i, (q, acc) in enumerate(TENQ.items()):
    f = doc(acc, "10-Q__")
    sid = f"TG{100 + i}"
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

# ── history vintages ────────────────────────────────────────────────────────────


def sel(path):
    """Item 6, Selected Financial Data: the year header and the rows the models read."""
    L = lines(path)
    i = max(k for k in range(len(L)) if re.sub(r" \| ", " ", L[k]).startswith("Item 6. Selected Financial Data") and "|" not in L[k][-6:])
    yi = next(k for k in range(i, i + 8) if re.fullmatch(r"(20\d\d \| ){4}20\d\d", L[k]))
    years = [int(y) for y in L[yi].split(" | ")]
    stop = i + 40
    rev = row(path, ["Revenues", "Revenues(1)", "Revenues (1)"], i, stop)[1]
    epsr = row(path, ["Net income (loss) per common share - diluted", "Net income per common share - diluted"], i, stop)
    return years, dict(zip(years, rev)), dict(zip(years, epsr[1])), epsr[0]


PTI_L = ["Income before income taxes", "Income (loss) before income taxes"]


def stmt(path):
    """The consolidated statement of operations (last three years) and the statement of cash flows."""
    i0 = line_no(path, lambda x: x == "CONSOLIDATED STATEMENTS OF OPERATIONS")
    hdr = next(k for k in range(i0, i0 + 6) if re.fullmatch(r"20\d\d \| 20\d\d \| 20\d\d", lines(path)[k]))
    yrs = [int(y) for y in lines(path)[hdr].split(" | ")]
    e0 = min(i0 + 45, line_no(path, lambda x: x.startswith("CONSOLIDATED STATEMENTS OF COMPREHENSIVE"), i0))
    pti = row(path, PTI_L, i0, e0)[1]
    ni = row(path, ["Net income", "Net income (loss)"], i0, e0)[1]
    nia = row(path, ["Net income available to common shareholders", "Net income (loss) attributable to common shareholders"], i0, e0)[1]
    sh = row(path, "Weighted average shares outstanding - diluted", i0, e0)[1]
    shb = row(path, "Weighted average shares outstanding - basic", i0, e0)[1]
    eps = row(path, ["Net income available per common share - diluted", "Net income (loss) per common share - diluted"], i0, e0)[1]
    c0 = line_no(path, lambda x: x == "CONSOLIDATED STATEMENTS OF CASH FLOWS", i0)
    cfo = row(path, "Net cash provided by operating activities", c0, c0 + 90)[1]
    capex = row(path, "Outlays for property, plant and equipment", c0, c0 + 90)[1]
    dl = ["Dividends to common and common equivalent shareholders", "Dividends to common shareholders",
          "Dividends paid to common and preferred shareholders", "Dividends paid to common and Series A preferred shareholders"]
    divr, divs = row(path, dl, c0, c0 + 90)
    return yrs, pti, ni, nia, sh, shb, eps, cfo, capex, divs, divr.split(" |")[0]


def groups2(path):
    """The two segments: the segment note's first operating margin row (display only)."""
    L = lines(path)
    n = max(k for k in range(len(L)) if re.match(r"Note \d+ . Segment Information$", L[k]))
    k = line_no(path, lambda x: x.startswith("Operating margin |"), n)
    v = row(path, "Operating margin", k, k + 1)[1]
    assert abs(sum(v[:-1]) - v[-1]) < 0.15, (path, v)
    return v[:2]


COMMODITY = "Our primary natural gas gathering and processing arrangements that expose us to commodity price risk are our percent-of-proceeds arrangements."
CYCLE = "even if our business experiences fluctuations in cash from operations due to seasonal and cyclical factors"
RISK = {"old": ("Our cash flow is affected by supply and demand for natural gas and NGL products and by natural gas, NGL, crude oil and "
                "condensate prices, and decreases in these prices could adversely affect our results of operations and financial condition."),
        "new": ("Our cash flow is affected by supply and demand for natural gas, NGL products and crude oil and by natural gas, NGL, crude oil "
                "and condensate prices, and decreases in supply, demand or these prices could adversely affect our results of operations and "
                "financial condition.")}
GHG = {"old": ("The adoption and implementation of climate change legislation or regulations restricting emissions of GHGs could result in "
               "increased operating costs and reduced demand for the products and services we provide."),
       "new": ("Our and our customers’ operations are subject to a number of risks arising out of the threat of climate change (including "
               "legislation or regulation to address climate change) that could result in increased operating costs, limit the areas in "
               "which oil and natural gas production may occur, and reduce demand for the products and services we provide.")}
REFSERV = {"old": ("In our refinery services business, we typically provide NGL balancing services via contractual arrangements with refiners "
                   "to purchase and/or market propane and to supply butanes."),
           "new": ("In our refinery services business, we typically provide NGL balancing services through contractual arrangements with "
                   "refiners to purchase and/or market propane and to supply butanes.")}
# the Channelview Splitter, as each 10-K describes it (the builder's theme clause: ENERGY_TRANSITION's refining read as out of scope)
SPLIT = {
    K17: ("entered into a long-term, fee-based agreement (“Splitter Agreement”) under which Targa Terminals will build and operate a 35,000 "
          "Bbl/d crude oil and condensate splitter at our Channelview Terminal on the Houston Ship Channel (“Channelview Splitter”).",
          "The Channelview Splitter is expected to be completed in the second quarter of 2018, and has an estimated total cost of "
          "approximately $140 million.",
          "a fee-based service under construction"),
    K18: ("entered into a long-term, fee-based agreement (the “Splitter Agreement”) under which we would build and operate a 35,000 Bbl/d "
          "crude oil and condensate splitter at our Channelview Terminal on the Houston Ship Channel (the “Channelview Splitter”).",
          "In December 2018, Vitol elected to terminate the Splitter Agreement.",
          "a fee-based service whose customer terminated the agreement"),
    K19: ("Our Petroleum Logistics business owns and operates a storage and terminaling facility in Channelview, Texas, including a 35,000 "
          "Bbl/d nameplate capacity crude oil and condensate splitter (the “Channelview Splitter”).", None,
          "a terminaling asset of the Petroleum Logistics business"),
    K20: ("which provided for Targa Channelview to construct a crude oil and condensate splitter (the “Splitter”) adjacent to a barge dock "
          "owned by Targa Channelview to provide services contemplated by the Splitter Agreement.",
          "and on December 23, 2018, Vitol voluntarily elected to terminate the Splitter Agreement claiming that Targa Channelview failed to "
          "timely achieve start-up of the Splitter.",
          "the subject of the terminated agreement's litigation")}
CLOUD18 = "Customer’s Accounting for Implementation Costs Incurred in a Cloud Computing Arrangement That is a Service Contract"

VS = [(K17, "TG70", "Targa Resources Corp. FY2017 10-K", "old", "old", "old"),
      (K18, "TG71", "Targa Resources Corp. FY2018 10-K", "old", "old", "old"),
      (K19, "TG72", "Targa Resources Corp. FY2019 10-K", "old", "new", "new"),
      (K20, "TG73", "Targa Resources Corp. FY2020 10-K", "new", "new", "new")]
prev = facts["history_vintages"][-1]
vintages, YSH, QEPS = [], {}, {}
for acc, sid, title, rk, gk, fk in VS:
    f = doc(acc, "10-K__")
    years, rev, eps, epsrow = sel(f)
    last = years[0]
    source(sid, acc, title, f, "Item 6 (selected financial data: revenues and EPS), the statements of operations and cash flows, the segment "
           "note, the risk factors" + ("" if acc == K20 else " and the selected quarterly data (the fourth quarter's EPS)"))
    yrs, pti, ni, nia, sh, shb, eps3, cfo, capex, divs, divlab = stmt(f)
    assert yrs[0] == last and all(abs(eps3[k] - eps[yrs[k]]) < 1e-9 for k in range(3)), (sid, "statement EPS = Item 6 EPS")
    YSH[last] = (shb[0], sid, SRC[sid]["published"], "basic weighted-average shares of the year")
    tax = round(pti[0] - ni[0], 1)
    gv = groups2(f)
    own = {str(y): eps[y] for y in sorted(eps, reverse=True) if y >= 2011 and eps[y] > 0}
    eps_norm = {**own, **{y: v for y, v in prev["eps_normalized"].items() if y not in own and int(y) < min(eps)}}   # earlier years carried
    for y in years:
        assert (eps[y] > 0) == (y < 2016), (sid, y)                     # 2016-2020 are the losses
    excl = dict(prev["eps_excluded"])
    for y in years:
        if eps[y] <= 0 and str(y) not in excl:
            yi = yrs.index(y)
            excl[str(y)] = (f"{eps_s(eps[y])} a diluted share for {y} (net loss attributable to common shareholders of {usd_m(nia[yi])} after "
                            "the Series A preferred dividends): a loss, so no P/E (the F, MU and CRM loss rule); its days leave the window")
    for k in (COMMODITY, CYCLE, RISK[rk], GHG[gk], REFSERV[fk]):
        quote(f, k)
    s1, s2, s_kind = SPLIT[acc]
    quote(f, s1)
    if s2:
        quote(f, s2)
    if acc == K18:
        quote(f, CLOUD18)
        cloud_text = (f"the {title} names cloud only in an accounting standard's title, '{CLOUD18}'")
    else:
        nc = len(re.findall("cloud", norm(" ".join(lines(f))), flags=re.I))
        assert nc == 0, (sid, "cloud", nc)
        cloud_text = f"the {title} does not name cloud"
    full = norm(" ".join(lines(f)))
    for w in ("e-commerce", "streaming", "electric vehicle", "crypto", "blockchain", "bitcoin"):
        assert not re.search(w, full, flags=re.I), (sid, w)
    revs = {**prev["revenue_usd_b"], **{str(y): round(rev[y] / 1000, 4) for y in years}}
    rsrc = {**prev["revenue_sources"], **{str(y): sid for y in years}}
    keep = sorted(revs, key=int)[-10:]                       # the ten fiscal years to the latest one
    revs = {y: revs[y] for y in sorted(revs, key=int, reverse=True) if y in keep}
    rsrc = {y: rsrc[y] for y in revs}
    shares = {**prev["diluted_shares_m"], **{str(y): s for y, s in zip(yrs, sh) if y >= 2011}}
    srcs = [sid] + [s for s in dict.fromkeys(rsrc.values()) if s != sid]
    if acc != K20:                                # the fourth quarter's EPS from the selected quarterly data (to FY2019)
        nq = max(k for k, x in enumerate(lines(f)) if x.startswith("Note") and "Selected Quarterly Financial Data" in x)
        qe = row(f, ["Net income (loss) per common share - diluted", "Net income (loss) per common share - diluted (2)",
                     "Net income (loss) per common share - diluted (3)"], nq, nq + 11)[1]
        qn_ = row(f, "Net income (loss) attributable to common shareholders", nq, nq + 11)[1]
        y0 = line_no(f, lambda x: x == str(last - 1), nq)
        qe0 = row(f, ["Net income (loss) per common share - diluted", "Net income (loss) per common share - diluted (2)",
                      "Net income (loss) per common share - diluted (3)", "Net income per common share - diluted"], y0, y0 + 8)[1]
        assert abs(qe[4] - eps[last]) < 1e-9, (sid, "the quarterly data's year = Item 6")
        QEPS[f"Q4 {last}"] = (qe[3], qe0[3], qn_[3], sid)
    voice_renamed = acc in (K19, K20)
    v = {**{k: prev[k] for k in ("company", "exchange", "symbol", "pe_window_start", "kind", "margin_signal_name", "kind_text", "normalization")},
         "business_line": ("Natural gas gathering and processing, NGL logistics and transportation" if voice_renamed else
                           "Natural gas gathering and processing, NGL logistics and marketing"),
         "published": SRC[sid]["published"], "sources": srcs,
         "fy_label": f"FY{last % 100:02d}", "fiscal_year_ends": {str(last): f"{last}-12-31"},
         "eps_normalized": eps_norm, "eps_excluded": excl,
         "revenue_usd_b": revs, "revenue_sources": rsrc,
         "revenue_note": ("consolidated revenues (the Partnership in, as TRC consolidates it); each year from the latest 10-K that reports it"
                          "; the ten fiscal years to the latest one; 2018 on under ASC 606, 2017 and earlier as first reported (a seam)"
                          if last >= 2018 else prev["revenue_note"]),
         "diluted_shares_m": {y: shares[y] for y in sorted(shares, key=int, reverse=True)},
         "shares_note": prev["shares_note"],
         "prev_fy_op_margin": mg(pti[0], rev[last]),
         "prev_fy_op_margin_note": f"FY{last % 100:02d} income before income taxes {usd_m(pti[0])} / revenues {usd_m(rev[last])} ({title})",
         "prev_fy_sales_growth": pct(rev[years[1]], rev[last]),
         "check_pretax_margin": mg(pti[0], rev[last]),
         "check_pretax_note": f"FY{last % 100:02d} income before income taxes / revenues ({title}), before the noncontrolling interests",
         "tax_rate": round(tax / pti[0], 3),
         "tax_note": f"FY{last % 100:02d} effective rate: income tax {usd_m(tax)} (income before income taxes less net income) on {usd_m(pti[0])} ({title})",
         "dividend_annual": None, "dividend_note": None,
         "fcf_b": round((cfo[0] + capex[0]) / 1000, 3), "fcf_label": f"FY{last % 100:02d}",
         "fcf_note": (f"consolidated net cash provided by operating activities {usd_m(cfo[0])} less outlays for property, plant and "
                      f"equipment {usd_m(-capex[0])} ({title})"),
         "cash_return_text": f"{usd_m(-divs[0])} of {divlab[0].lower() + divlab[1:]} in FY{last % 100:02d}",
         "groups": [["Gathering and Processing", round(gv[0] / 1000, 4), None],
                    ["Logistics and Transportation" if voice_renamed else "Logistics and Marketing", round(gv[1] / 1000, 4), None]],
         "groups_basis": (f"FY{last % 100:02d} segment operating margin, USD bn ({title}'s segment note; 'Other', the hedges, and Corporate "
                          "and Eliminations left out)"),
         "why": (f"Commodity exposure ({title}): {COMMODITY} Distribution policy: '{CYCLE}' (the boilerplate of the dividend policy, not a "
                 f"statement that the business is cyclical: the CHTR reading). Risk factor: '{RISK[rk]}'; no theme in taxonomy_eras.json is "
                 "live for a midstream natural gas company on this date"),
         "ghg_quote": GHG[gk], "refinery_quote": REFSERV[fk], "tenk_label": title,
         # (TRGP 2018-2021) the theme clause's own words for these vintages: the splitter as each 10-K describes it, and the 10-K's cloud
         "splitter_text": f"the Channelview Splitter is {s_kind}: '{s1}'" + (f" '{s2}'" if s2 else ""),
         "cloud_text": cloud_text}
    vintages.append(v)
    prev = v

# Q4's EPS from the next 10-K (to FY2019), from the 10-K's date; Q4 2020 stays n/r (the FY2020 10-K has no selected quarterly data)
for q, (e, e0, nq_, sid) in QEPS.items():
    p = PQ[q]
    # the 10-K's fourth quarter may differ from the release's by a few tenths (Q4 2018: $(137.3)M against $(137.0)M): only its EPS is used
    assert abs(nq_ - p["raw"]["nia_m"]) < 0.5, (q, "the 10-K's quarter = the release's", nq_, p["raw"]["nia_m"])
    diff = "" if abs(nq_ - p["raw"]["nia_m"]) < 1e-9 else (f"; the 10-K's quarter has net income attributable to common shareholders of "
                                                           f"{usd_m(nq_)} against the release's {usd_m(p['raw']['nia_m'])}")
    raw = {**p["raw"], "eps_q": e, "eps_q_prior": e0}
    p["restated"] = [{"published": SRC[sid]["published"], "source": sid, "raw": raw, "eps_q": e, "eps_q_prior": e0,
                      "eps_note": f"GAAP, diluted, {eps_s(e)} against {eps_s(e0)} a year earlier (the {SRC[sid]['title'].split('Corp. ')[1]}'s "
                                  f"selected quarterly data, {SRC[sid]['published']}; the release prints no per-share figure{diff})"}]

# ── outlooks: the Adjusted EBITDA outlooks (display only) and, from the Q4 2018 release, the estimated net income attributable to TRC
#    that reconciles them (a GAAP earnings guide: the KMI 2019-2022 rule; per share as below) ──
F8 = doc(OUT8K, "EX-99.1__")
source("TG33", OUT8K, "Targa Resources Corp. updated 2020 outlook and common share repurchase program (8-K of 2020-10-05, Exhibit 99.1)",
       F8, "TRC's updated 2020 Adjusted EBITDA outlook and the estimated net loss attributable to TRC that reconciles it")
EB18 = quote(FREL["Q4 2017"], "Targa estimates Adjusted EBITDA to be between $1,225 million and $1,325 million.")
EBITDA = {"Q4 2018": "Targa estimates full year Adjusted EBITDA to be between $1,300 million and $1,400 million.",
          "Q4 2019": "For 2020, Targa estimates full year Adjusted EBITDA to be between $1,625 million and $1,750 million",
          "Q1 2020": "Targa has updated its estimated full-year 2020 Adjusted EBITDA range to $1.4 billion to $1.625 billion.",
          "Q2 2020": "now estimates full year Adjusted EBITDA to be between $1.5 billion to $1.625 billion.",
          "8-K": "Targa currently estimates its full-year 2020 Adjusted EBITDA to be at or around the high end of its previously provided outlook of $1.5 billion to $1.625 billion.",
          "Q3 2020": "Targa estimates its full year 2020 Adjusted EBITDA to be at or around the high end of its previously provided outlook of $1.5 billion to $1.625 billion.",
          "Q4 2020": "For 2021, Targa estimates full year Adjusted EBITDA to be between $1,675 million and $1,775 million",
          "Q1 2021": "Targa is increasing its estimated full year Adjusted EBITDA to be between $1,800 million and $1,900 million.",
          "Q2 2021": "For full year 2021, Targa is increasing its estimated Adjusted EBITDA range to between $1.9 billion and $2.0 billion.",
          "Q3 2021": "For full year 2021, Targa now estimates adjusted EBITDA to exceed the top end of its previously disclosed range of $1.9 billion to $2.0 billion"}
guides = [{"fy": 2018, "published": PQ["Q4 2017"]["published"], "source": SID["Q4 2017"], "rev_none": True,
           "display": f"TRC 2018 outlook: '{EB18}'; no revenue, EPS or margin guide (the 2018 guidance is Adjusted EBITDA, capital spending "
                      "and volumes; display only)"}]


def ni_guide(path, fy):
    """The release's 'Reconciliation of Estimated Net Income (Loss) attributable to TRC to (Estimated) Adjusted EBITDA': its first row."""
    h = line_no(path, lambda x: x.startswith("Reconciliation of Estimated Net") and "attributable to TRC" in x)
    yl = next(k for k in range(h - 4, h) if re.fullmatch(rf"{fy}E?(\(1\))?", lines(path)[k]))
    r, v = row(path, ["Net income attributable to TRC", "Net income (loss) attributable to TRC", "Net loss attributable to TRC"], h, h + 3)
    assert len(v) == 1 and yl, (path, r)
    return v[0], r


for q in ("Q4 2018", "Q4 2019", "Q1 2020", "Q2 2020", "8-K", "Q3 2020", "Q4 2020", "Q1 2021", "Q2 2021", "Q3 2021"):
    path = F8 if q == "8-K" else FREL[q]
    gfy = 2019 if q == "Q4 2018" else 2020 if q in ("Q4 2019", "Q1 2020", "Q2 2020", "8-K", "Q3 2020") else 2021
    ni, r = ni_guide(path, gfy)
    eb = quote(path, EBITDA[q])
    rel = "Q3 2020" if q == "8-K" else q                        # the 8-K's own date sits between the Q2 and Q3 2020 releases
    pub = SRC["TG33"]["published"] if q == "8-K" else PQ[q]["published"]
    sq = "Q2 2020" if q == "8-K" else q
    # the per-share figure: net income attributable to TRC less the Series A preferred dividends at the release's own quarter's rate
    # (cash and deemed, x4), over the latest basic weighted-average share count public on the guide's own date (a 10-Q's quarter or a
    # 10-K's year; the releases print none) (the KMI 2019-2022 rule, with TRC's preferred dividends; decided before any 2018-2021 model
    # was built)
    pc, pd = PREF[sq]
    sh, ssid, spub, sdesc = max((x for x in list(QSH.values()) + list(YSH.values()) if x[2] <= pub), key=lambda x: (x[2], x[1]))
    g = {"fy": gfy, "published": pub, "source": "TG33" if q == "8-K" else SID[q], "rev_none": True,
         "ni_trc_est_m": ni, "pref_q_m": [pc, pd], "pref_source": SID[sq], "shares_basic_m": sh, "shares_source": ssid,
         "shares_note": f"{sdesc} ({SRC[ssid]['title']}, {spub})",
         "ni_row": r,
         "doc": ("8-K of 2020-10-05" if q == "8-K" else f"{q} release"),
         "display": (f"TRC {gfy} outlook ({'the 8-K of 2020-10-05' if q == '8-K' else 'the ' + q + ' release'}): '{eb}' (Adjusted EBITDA, "
                     f"non-GAAP, display only), reconciled to an estimated net {'income' if ni >= 0 else 'loss'} attributable to TRC of "
                     f"{usd_m(ni)}; no revenue or margin guide")}
    guides.append(g)

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
facts["segment_rename"] = {"published": PQ["Q4 2019"]["published"], "source": SID["Q4 2019"], "quote": RENAME}
facts["_doc"] = BEFORE["_doc"] + (" 2018-2021 appended by retro/generators/trgp/gen_trgp_1821.py from the same filings' rows, every earlier "
                                  "fact asserted unchanged.")
out = A.out or os.path.join(REPO, "retro", "facts", "TRGP.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(facts, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_trgp_1821.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump(CHECK, fh, ensure_ascii=False, indent=1)
print(out, len(prints), "prints", len(vintages), "vintages", len(dividends), "dividends", len(guides), "guides",
      sum(len(v) for v in CHECK.values()), "checked strings")
for p in prints:
    print(p["quarter"], p["published"], p["sales_pct"], p["gp_pct"], p["lm_pct"], p["opm_bp"], p["ptm_bp"],
          [(r["published"], r["eps_q"], r.get("diluted_shares_m")) for r in p.get("restated", [])])
for v in vintages:
    print(v["fy_label"], v["published"], v["eps_normalized"], sorted(v["eps_excluded"]), v["diluted_shares_m"], v["tax_rate"], v["groups"])
for g in guides:
    print(g["fy"], g["published"], g.get("ni_trc_est_m"), g.get("pref_q_m"), g.get("shares_basic_m"), g.get("shares_source"))
