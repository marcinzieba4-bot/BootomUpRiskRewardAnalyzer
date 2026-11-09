#!/usr/bin/env python3
"""
HINDSIGHT check of the falling-EPS short (epp_short.py, ratio_b_eps_ls.py): did it use anything that was not public
before the short was placed, and does it survive with reported EPS only (no guidance)? Prints the tables quoted in
staging/retrospective/EPS_PIT_CHECK.md.

THE CHECKS, fixed in this docstring before the first run.
- Audit E1 (the last fiscal year's EPS below the year before, from the date's EPS_NORM). On every date, the last year
  in EPS_NORM must have been reported by the as-of date: in a history vintage (retro/facts, history_vintages) or a Q4
  print (prints, q == 4) published on or before it.
- Audit E2 (EPP_TODAY_EPS lower than 26 weeks earlier). Classify each date's EPP_TODAY_EPS from its own comment: "stands"
  marks the last reported full year, otherwise it is a guide. For every guide-based date, look for a numeric EPS guide
  for the same fiscal year published on or before the as-of date whose value (the midpoint of a range) matches within
  2%, after any split between the guide and the date. These are the guides list, or ACN's prints' fy_eps_guide. A
  date whose comment says the EPS comes from a growth guide counts if an EPS growth guide for that fiscal year was
  published by then. [Both widened after the first run: some sheets label Q4 prints only by name ("Q4 2007"), and some
  dates use growth guides, so the first pass flagged ACN and UNP Q4 dates and NKE and WMT growth-guide dates. Count
  the dates where only a guide published AFTER the as-of date matches: that would be a leak.
- The trade is entered at the close of the next trading day after the as-of date, so anything published on the as-of
  date (after-close releases are already dated the next day in retro/facts) is public before the entry.
- Reported-only filters:
  - RQ, the quarter: the latest print published on or before the as-of date has quarterly EPS (eps_q) below the same
    quarter a year earlier (eps_q_prior), both as printed in that release.
  - RB, both: RQ and E1 (reported annual EPS down). The reported-only twin of E3.
  - ACN's prints carry no quarterly EPS, so RQ and RB never fire on ACN.
- Re-run of ratio_b_eps_ls.py with the reported-only filters:
  (a) its frozen pick (N=3, long unfiltered, hold 6m, 50%) with E3 swapped for RB, side by side;
  (b) its full procedure (216 settings, chosen on one half and judged on the other) with the short filter taken from
      E1, RQ, RB instead of E1, E2, E3.

Everything printed is a label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule"). Reads only.

    python3 staging/retrospective/eps_pit_check.py                 # every table
    python3 staging/retrospective/eps_pit_check.py audit frozen    # selected sections

Sections: audit frozen split now
"""
import bisect
import contextlib
import io
import itertools
import json
import math
import os
import re
import statistics
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import ratio_b_eps_ls as LS  # noqa: E402  (the long/short machinery; it loads epp_short and ratio_b_basket)
ES, B, X = LS.ES, LS.B, LS.X
FACTS = {t: json.load(open(os.path.join(X.ROOT, "retro", "facts", f"{t}.json"))) for t in X.ALL}
TODAY_LINE = re.compile(r"^EPP_TODAY_EPS\s*=\s*(-?[0-9.]+)\s*#\s*(.*)$", re.M)
FY_LABEL = re.compile(r"FY(\d{4})E")


def fy_of_label(lbl):
    m = re.match(r"FY(\d{2,4})", lbl or "")
    if not m:
        return None
    y = int(m.group(1))
    return y + 2000 if y < 100 else y


REPORTED = {}                                                    # ticker -> sorted [(published, fiscal year reported)]
for t, d in FACTS.items():
    ev = [(v["published"], max(int(k) for k in v["eps_normalized"])) for v in d.get("history_vintages", []) if v.get("eps_normalized")]
    for p in d["prints"]:                                        # Q4 releases; some sheets carry only the label ("Q4 2007", "Q4 FY08")
        lbl = str(p.get("quarter", ""))
        if p.get("q") == 4 or lbl.startswith("Q4"):
            fy = p.get("fy")
            if not fy:
                m = re.search(r"(?:FY)?(\d{4}|\d{2})\s*$", lbl)
                fy = (2000 + int(m.group(1)) if len(m.group(1)) == 2 else int(m.group(1))) if m else None
            if fy:
                ev.append((p["published"], fy))
    REPORTED[t] = sorted(ev)

GROWTH_GUIDES = {t: sorted((g["published"], g["fy"]) for g in d.get("guides", []) if g.get("eps_growth") is not None)
                 for t, d in FACTS.items()}                      # EPS growth guides (a percentage on the prior year)
GUIDES = {}                                                      # ticker -> [(published, fy, value)]
for t, d in FACTS.items():
    out = []
    for g in d.get("guides", []):
        v = g.get("eps_guide")
        if v is not None:
            out.append((g["published"], g["fy"], statistics.fmean(v) if isinstance(v, list) else float(v)))
    for p in d["prints"]:
        v = p.get("fy_eps_guide")
        if v is not None:
            out.append((p["published"], None, statistics.fmean(v) if isinstance(v, list) else float(v)))
    GUIDES[t] = sorted(out, key=lambda x: x[0])

QPRINTS = {t: sorted((p["published"], p["eps_q"], p["eps_q_prior"]) for p in d["prints"]
                     if isinstance(p.get("eps_q"), (int, float)) and isinstance(p.get("eps_q_prior"), (int, float))) for t, d in FACTS.items()}

for r in X.R:
    t, a = r["ticker"], r["as_of"]
    src = open(os.path.join(X.ROOT, X.SERIES[t], a, "model.py"), encoding="utf-8").read()
    mt = TODAY_LINE.search(src)
    r["eps_comment"] = mt.group(2) if mt else ""
    r["eps_is_guide"] = "stands" not in r["eps_comment"]
    fm = FY_LABEL.search(r["eps_comment"])
    r["eps_fy"] = int(fm.group(1)) if fm else None
    qs = [q for q in QPRINTS[t] if q[0] <= a]
    r["rq_down"] = (qs[-1][1] < qs[-1][2]) if qs else None
    rep = [fy for pub, fy in REPORTED[t] if pub <= a]
    r["known_fy"] = max(rep) if rep else None
    r["e1_last_fy"] = max(int(k) for k in ES.ast.literal_eval(ES.EPS_NORM_RE.search(src).group(1)))

FILTERS = {"RQ": lambda r: r["rq_down"] is True, "RB": lambda r: r["rq_down"] is True and r["eps_last_down"]}
LS.FILTERS.update(FILTERS)                                       # the long/short machinery reads its filters from here


def pct(v):
    return f"{v * 100:+.1f}%"


def section_audit():
    rows = X.R
    bad_e1 = [r for r in rows if r["known_fy"] is None or r["e1_last_fy"] > r["known_fy"]]
    print("\n### Audit of E1: is the last year in EPS_NORM reported by the as-of date?\n")
    print(f"{len(rows)} dates checked; dates whose last EPS_NORM year was not yet reported (vintage or Q4 print) by the as-of date: "
          f"**{len(bad_e1)}**." + ("" if not bad_e1 else " First: " + ", ".join(f"{r['ticker']} {r['as_of']} (FY{r['e1_last_fy']}, known FY{r['known_fy']})" for r in bad_e1[:8])))
    print("\n### Audit of E2: what EPP_TODAY_EPS is, and whether each guide was public by the as-of date\n")
    print("| Ticker | Dates | Reported full year ('stands') | Guide-based | Guide matched by one published by the as-of date | "
          "Matched only by a later guide (leak) | Not matched at all |\n|---|---|---|---|---|---|---|")
    tot = Counter()
    for t in X.ALL:
        rs = [r for r in rows if r["ticker"] == t]
        g = [r for r in rs if r["eps_is_guide"]]
        ok = leak = none = 0
        sp = X.splits(t)
        for r in g:
            def match(pool):
                for pub, fy, val in pool:
                    if fy is not None and r["eps_fy"] is not None and fy != r["eps_fy"]:
                        continue
                    ratio = math.prod(x for e, x in sp if pub < e.isoformat() <= r["as_of"])
                    if val and abs(val / ratio / r["eps_now"] - 1) <= 0.02:
                        return True
                return False
            before = [x for x in GUIDES[t] if x[0] <= r["as_of"]]
            after = [x for x in GUIDES[t] if x[0] > r["as_of"]]
            growth = "growth" in r["eps_comment"]
            g_before = growth and any(pub <= r["as_of"] and fy == r["eps_fy"] for pub, fy in GROWTH_GUIDES[t])
            g_after = growth and any(pub > r["as_of"] and fy == r["eps_fy"] for pub, fy in GROWTH_GUIDES[t])
            if match(before) or g_before:
                ok += 1
            elif match(after) or g_after:
                leak += 1
            else:
                none += 1
        tot.update(dates=len(rs), rep=len(rs) - len(g), guide=len(g), ok=ok, leak=leak, none=none)
        print(f"| {t} | {len(rs)} | {len(rs) - len(g)} | {len(g)} | {ok} | {leak} | {none} |")
    print(f"| all | {tot['dates']} | {tot['rep']} | {tot['guide']} | {tot['ok']} | **{tot['leak']}** | {tot['none']} |")
    sig = [r for r in rows if ES.E1(r) and ES.E2(r)]
    print(f"\nOf the {len(sig)} dates on which E3 fired, {sum(r['eps_is_guide'] for r in sig)} had a guide-based EPP_TODAY_EPS "
          f"({100 * sum(r['eps_is_guide'] for r in sig) / len(sig):.0f}%).")
    print("\n### The reported-only filters: how often they fire\n")
    print("| Filter | Dates | Tickers (dates) |\n|---|---|---|")
    for name, f in (("E1 (reported annual EPS down)", ES.E1), ("RQ (latest quarter's EPS below the same quarter a year earlier)", FILTERS["RQ"]),
                    ("RB (RQ and E1)", FILTERS["RB"]), ("E3 (E1 and the floor's EPS lower than 26 weeks ago; uses guides)", lambda r: ES.E1(r) and ES.E2(r))):
        s = [r for r in rows if f(r)]
        print(f"| {name} | {len(s)} | {', '.join(f'{t} {n}' for t, n in Counter(r['ticker'] for r in s).most_common(6))} |")


def frozen(filt):
    return dict(n=3, excl=False, filt=filt, hold=6, size=0.5, empty="SPY")


def section_frozen():
    print("\n### The frozen pick (N=3, long unfiltered, short hold 6m, size 50%), E3 against the reported-only filters\n")
    print("| Universe | Short filter | Empty cohort | 2008-2016 | 2017-2026 | Full period | Beta to SPY | Months with a short formed |")
    print("|---|---|---|---|---|---|---|---|")
    for name, u in LS.UNIVERSES:
        for f in ("E3", "RB", "RQ", "E1"):
            for empty in ("SPY", "cash"):
                cfg = dict(frozen(f), empty=empty)
                s, active = LS.series(cfg, u)
                print(f"| {name} | {f} | {empty} | {LS.cell(s, LS.HALF_A)} | {LS.cell(s, LS.HALF_B)} | {LS.cell(s, LS.MONTHS)} | "
                      f"{LS.beta(LS.MONTHS, s):+.2f} | {active * 100:.0f}% |")


def section_split():
    grid = [dict(n=n, excl=excl, filt=f, hold=h, size=s, empty=e)
            for n, excl, f, h, s, e in itertools.product((2, 3, 4), (False, True), ("E1", "RQ", "RB"), (1, 3, 6), (0.5, 1.0), ("cash", "SPY"))]
    for name, u in LS.UNIVERSES:
        res = [(cfg, *LS.series(cfg, u)) for cfg in grid]
        print(f"\n### {name}, reported-only filters: optimise on one half, judge on the other\n")
        print("| Chosen on | Setting chosen | Train | Test (untouched) | Test rank of 216 | Median setting in test |\n|---|---|---|---|---|---|")
        for train, test, tl in ((LS.HALF_A, LS.HALF_B, "2008-2016"), (LS.HALF_B, LS.HALF_A, "2017-2026")):
            sh_tr = [LS.stats([s[m] for m in train])["sharpe"] for _, s, _ in res]
            sh_te = [LS.stats([s[m] for m in test])["sharpe"] for _, s, _ in res]
            i = max(range(len(res)), key=lambda k: sh_tr[k])
            rank = 1 + sum(x > sh_te[i] for x in sh_te)
            mid = sorted(range(len(res)), key=lambda k: sh_te[k])[len(res) // 2]
            print(f"| {tl} | {LS.label(res[i][0])} | {LS.cell(res[i][1], train)} | **{LS.cell(res[i][1], test)}** | {rank} | {LS.cell(res[mid][1], test)} |")
        sa = [LS.stats([s[m] for m in LS.HALF_A])["sharpe"] for _, s, _ in res]
        sb = [LS.stats([s[m] for m in LS.HALF_B])["sharpe"] for _, s, _ in res]
        print(f"\nRank correlation of the settings' Sharpe between the halves: {X.spearman(sa, sb):+.2f}.")
        print("\nAverage full-period Sharpe by short filter: " + ", ".join(
            f"{f} {statistics.fmean(LS.stats([s[m] for m in LS.MONTHS])['sharpe'] for c, s, _ in res if c['filt'] == f):.2f}" for f in ("E1", "RQ", "RB")))


def section_now():
    m = LS.MONTHS[-1]
    print(f"\n### The newest month ({m}) with the reported-only filter RB\n")
    for name, u in LS.UNIVERSES:
        names = [t for t in LS.FIRST[m] if t in u]
        rows = {t: LS.row(t, m) for t in names}
        longs = [s["ticker"] for s in sorted((LS.FIRST[m][t] for t in names), key=B.rank_key)[:3]]
        rb = [t for t in names if FILTERS["RB"](rows[t])]
        rq = [t for t in names if FILTERS["RQ"](rows[t])]
        e3 = [t for t in names if ES.E1(rows[t]) and ES.E2(rows[t])]
        print(f"- {name}: long {', '.join(longs)}; RB short: {', '.join(rb) or 'none'}; RQ: {', '.join(rq) or 'none'}; E3 (for comparison): {', '.join(e3) or 'none'}")


SECTIONS = {"audit": section_audit, "frozen": section_frozen, "split": section_split, "now": section_now}

if __name__ == "__main__":
    print(f"HINDSIGHT. {len(X.R)} dates across {len(X.ALL)} tickers.")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
