#!/usr/bin/env python3
"""
HINDSIGHT: stop-losses and S&P 500 hedges on the combined growth + value book with the yield tilt (combo_book.py).
Prints the tables quoted in staging/retrospective/COMBO_RISK.md.

The book itself is post-hoc (COMBO_BOOK.md). This script asks only which risk controls improve it, under a rule fixed
before the first run.

FIXED in this docstring before the first run; every cell is printed.
- Base book: combo_book.py's COMBINED + YIELD TILT. Two growth picks (the highest own P/E percentile in the growth basket)
  and two value picks (the most negative e2_rev in the value basket), 75% to the sleeve the 10-year yield trend (Y6)
  favours. Bought each month and held 1 month.
- A. Per-position stops. Each is checked at every close and traded at the next close; the proceeds sit in cash for the
  rest of the month.
  - NONE.
  - FIX10, FIX15, FIX20: exit at -10/-15/-20% from the entry.
  - TRAIL10, TRAIL15, TRAIL20: exit at -10/-15/-20% from the highest close since the entry.
  - TRAIL15+MA50, TRAIL20+MA50: as TRAIL, with re-entry after a close above the 50-day average; the stop then resets.
  - VOL2, VOL3: trailing stop at 2 or 3 x the stock's monthly volatility (63-day stdev of daily returns x sqrt(21),
    measured at entry). Where the price file has under 20 days before the entry (the first weeks of 2008), 15%: a gap
    found on the first run.
- B. Portfolio overlays, applied to the book with no stop and to the book with TRAIL15 (the main setting of
  COMBO_BOOK.md). A signal at a close is traded at the next close (ratio_b_hedge.py's lag=1). The S&P 500 (^GSPC) gives
  the signals; SPY is the hedge.
  - none.
  - MA50 / MA100 / MA200 x 50% / 100%: short SPY (50% or 100% of the book) while the S&P closes below its 50/100/200-day
    average.
  - MA100 BETA: short SPY at the book's own trailing beta (126 days, clipped to 0-1.5) while below the 100-day average.
  - CASH100 / HALFCASH100: sell all / half of the book to cash while below the 100-day average.
  - CROSS 50%: short 50% while the 50-day average is below the 200-day average.
  - DD10 50%: short 50% while the S&P is more than 10% below its 252-day high.
  - VOL25 50%: short 50% while the S&P's 21-day realised volatility is above 25% a year.
  - VT20 / VT25: scale the book to a 20% / 25% volatility target from its own 63-day realised volatility, never above
    100%; the rest in cash.
  - OWN100: half the book to cash while the book's own equity curve is below its 100-day average.
- Cash earns nothing; the short pays no borrow and earns no interest.
- Costs: combo_book.py's 0.10% cost charge for the book and its stops, plus 0.10% on each change in hedge ratio or exposure.
- THE RULE. A control improves the book if, after costs:
  - its Sharpe is higher in both 2008-2016 and 2017-2026;
  - its 2008-2026 worst drawdown is shallower.
  Among the controls that pass, the best is the one with the highest 2008-2026 Sharpe.
- C. The best stop from A, combined with the best overlay from B on that stop's base. If no overlay passes on that base,
  the best overlay on the no-stop base is used. One cell.
- Then: the S&P stress windows (named before the run from market history; descriptive only); calendar years for the
  candidates; the overlays' state now.

Everything printed is a label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule"). Reads only.

    python3 staging/retrospective/combo_risk.py                    # every table
    python3 staging/retrospective/combo_risk.py --json out.json    # also the chart data
"""
import bisect
import contextlib
import datetime
import io
import json
import math
import os
import statistics
import sys

os.environ["RETRO_UNIVERSE"] = "all"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import combo_book as C  # noqa: E402
TS, P = C.TS, C.P
H = P.H
DAYS, MONTHS, DAY_POS, ENTRY, NDAYS, LEVEL, MA50 = C.DAYS, C.MONTHS, C.DAY_POS, C.ENTRY, C.NDAYS, TS.LEVEL, TS.MA50
SPY = P.SPY
BOOK = "COMBINED + YIELD TILT"
COST = 0.001

STOPS = [("NONE", None, None, False), ("FIX10", 0.10, "fixed", False), ("FIX15", 0.15, "fixed", False),
         ("FIX20", 0.20, "fixed", False), ("TRAIL10", 0.10, "trail", False), ("TRAIL15", 0.15, "trail", False),
         ("TRAIL20", 0.20, "trail", False), ("TRAIL15+MA50", 0.15, "trail", True), ("TRAIL20+MA50", 0.20, "trail", True),
         ("VOL2", 2.0, "vol", False), ("VOL3", 3.0, "vol", False)]


def stop_level(stop, t, e):
    _, level, kind, _ = stop
    if kind != "vol":
        return level
    L = LEVEL[t]
    rs = [L[j] / L[j - 1] - 1 for j in range(max(1, e - 62), e + 1)]
    if len(rs) < 20:              # the first weeks of 2008, before the price file has 20 days: 15% (found on the first run)
        return 0.15
    return level * statistics.pstdev(rs) * math.sqrt(21)


def cohort_path(ci, w, stop):
    """One month's cohort (tilt_switch.cohort_path, with the stop level set per position)."""
    _, _, kind, reenter = stop
    e = DAY_POS[ENTRY[MONTHS[ci]]]
    end = DAY_POS[ENTRY[MONTHS[ci + 1]]] if ci + 1 < len(MONTHS) else NDAYS - 1
    total = [0.0] * (end - e + 1)
    exits = entries = 0
    for t, x in w.items():
        L = LEVEL[t]
        level = stop_level(stop, t, e) if kind else None
        held, val, ref, order = True, x, L[e], None
        total[0] += val
        for k, j in enumerate(range(e + 1, end + 1), start=1):
            if held:
                val *= L[j] / L[j - 1]
            if order == "sell":
                held, order = False, None
                exits += 1
            elif order == "buy":
                held, order, ref = True, None, L[j]
                entries += 1
            if level is not None:
                if held:
                    ref = max(ref, L[j]) if kind in ("trail", "vol") else ref
                    if L[j] / ref - 1 <= -level:
                        order = "sell"
                elif reenter and MA50[t][j] is not None and L[j] > MA50[t][j]:
                    order = "buy"
            total[k] += val
    return e, total, exits, entries


CACHE = {}


def base(stop_name):
    """The book's daily returns after its own costs, with the stop."""
    if stop_name not in CACHE:
        stop = next(s for s in STOPS if s[0] == stop_name)
        W = {m: C.weights(BOOK, m) for m in MONTHS}
        rets, ex, en = [0.0] * NDAYS, 0, 0
        for ci, m in enumerate(MONTHS):
            e, total, a, b = cohort_path(ci, W[m], stop)
            ex, en = ex + a, en + b
            for k in range(1, len(total)):
                rets[e + k] = total[k] / total[k - 1] - 1
        years = (NDAYS - 1) / 252
        info = {"exits": ex / years, "entries": en / years, "W": W}
        CACHE[stop_name] = (TS.costed(rets, info, 1, False, COST), info)
    return CACHE[stop_name][0]


# ---- S&P signals (on ^GSPC's own calendar, from before 2008), mapped to the book's days with lag 1 ----
G, GD = H.GSPC, H.GDAYS
GC = [G[d] for d in GD]


def ma(n):
    out, run = {}, 0.0
    for i, c in enumerate(GC):
        run += c - (GC[i - n] if i >= n else 0.0)
        if i >= n - 1:
            out[GD[i]] = run / n
    return out


MA = {n: ma(n) for n in (50, 100, 200)}
SIG = {
    "below50": {d: G[d] < MA[50][d] for d in MA[50]},
    "below100": {d: G[d] < MA[100][d] for d in MA[100]},
    "below200": {d: G[d] < MA[200][d] for d in MA[200]},
    "cross": {d: MA[50][d] < MA[200][d] for d in MA[200]},
    "dd10": {GD[i]: GC[i] < 0.9 * max(GC[max(0, i - 251): i + 1]) for i in range(251, len(GD))},
    "vol25": {GD[i]: statistics.pstdev([GC[k] / GC[k - 1] - 1 for k in range(i - 20, i + 1)]) * math.sqrt(252) > 0.25
              for i in range(21, len(GD))},
}


def lagged(sig):
    """flags[j] = 1 if the position is on over (DAYS[j-1], DAYS[j]]: the signal of DAYS[j-2] traded at DAYS[j-1]'s close."""
    return [0] + [int(j >= 2 and bool(sig.get(DAYS[j - 2], False))) for j in range(1, NDAYS)]


FLAGS = {k: lagged(v) for k, v in SIG.items()}
assert FLAGS["below100"] == H.hedge_flags(100, 1), "the 100-day flags must match ratio_b_hedge.py's"


def apply(r, expo, hedge):
    """expo[j]: share of the book held; hedge[j]: SPY short as a share of the book. Costs on each change."""
    out = [0.0]
    for j in range(1, NDAYS):
        x = expo[j] * r[j] - hedge[j] * SPY[j]
        x -= COST * (abs(expo[j] - expo[j - 1]) + abs(hedge[j] - hedge[j - 1]))
        out.append(x)
    return out


ONES, ZEROS = [1.0] * NDAYS, [0.0] * NDAYS


def rolling_beta(r, j, n=126):
    lo = max(1, j - 1 - n)
    xs, ss = r[lo: j - 1], SPY[lo: j - 1]
    if len(xs) < 40:
        return 1.0
    mx, ms = statistics.fmean(xs), statistics.fmean(ss)
    vs = sum((b - ms) ** 2 for b in ss)
    return max(0.0, min(1.5, sum((a - mx) * (b - ms) for a, b in zip(xs, ss)) / vs)) if vs else 1.0


def overlay(name, r):
    f = FLAGS
    if name == "none":
        return r, ONES, ZEROS
    if name.startswith("MA") and name.endswith("%"):
        n, ratio = name[2:].split()
        hedge = [ratio == "100%" and 1.0 or 0.5 if x else 0.0 for x in f["below" + n]]
        return apply(r, ONES, hedge), ONES, hedge
    if name == "MA100 BETA":
        hedge = [rolling_beta(r, j) if f["below100"][j] else 0.0 for j in range(NDAYS)]
        return apply(r, ONES, hedge), ONES, hedge
    if name in ("CASH100", "HALFCASH100"):
        cut = 1.0 if name == "CASH100" else 0.5
        expo = [1.0 - cut * x for x in f["below100"]]
        return apply(r, expo, ZEROS), expo, ZEROS
    if name in ("CROSS 50%", "DD10 50%", "VOL25 50%"):
        hedge = [0.5 * x for x in f[{"CROSS 50%": "cross", "DD10 50%": "dd10", "VOL25 50%": "vol25"}[name]]]
        return apply(r, ONES, hedge), ONES, hedge
    if name in ("VT20", "VT25"):
        target = 0.20 if name == "VT20" else 0.25
        expo = [1.0, 1.0]
        for j in range(2, NDAYS):
            xs = r[max(1, j - 64): j - 1]
            vol = statistics.pstdev(xs) * math.sqrt(252) if len(xs) >= 20 else 0.0
            expo.append(min(1.0, target / vol) if vol > 0 else 1.0)
        return apply(r, expo, ZEROS), expo, ZEROS
    if name == "OWN100":
        eq, v = [1.0], 1.0
        for x in r[1:]:
            v *= 1 + x
            eq.append(v)
        below, run = [False] * NDAYS, 0.0
        for j in range(NDAYS):
            run += eq[j] - (eq[j - 100] if j >= 100 else 0.0)
            below[j] = j >= 99 and eq[j] < run / 100
        expo = [1.0] + [0.5 if j >= 2 and below[j - 2] else 1.0 for j in range(1, NDAYS)]
        return apply(r, expo, ZEROS), expo, ZEROS
    raise KeyError(name)


OVERLAYS = ["none", "MA50 50%", "MA50 100%", "MA100 50%", "MA100 100%", "MA200 50%", "MA200 100%", "MA100 BETA",
            "CASH100", "HALFCASH100", "CROSS 50%", "DD10 50%", "VOL25 50%", "VT20", "VT25", "OWN100"]


def st(r, lo=None, hi=None):
    c, v, sh, dd, b = P.stats(r, lo, hi)
    return {"cagr": c, "vol": v, "sharpe": sh, "mdd": dd, "beta": b}


def judge(r, ref):
    a1, a2, af = st(r, hi="2016"), st(r, lo="2017"), st(r)
    b1, b2, bf = st(ref, hi="2016"), st(ref, lo="2017"), st(ref)
    return a1["sharpe"] > b1["sharpe"] and a2["sharpe"] > b2["sharpe"] and af["mdd"] > bf["mdd"]


def row(r):
    s, s1, s2 = st(r), st(r, hi="2016"), st(r, lo="2017")
    return (f"{s['cagr'] * 100:+.1f}% | {s['vol'] * 100:.1f}% | {s['sharpe']:.2f} | {s['mdd'] * 100:.1f}% | "
            f"{s['cagr'] / -s['mdd']:.2f} | {s1['sharpe']:.2f} | {s2['sharpe']:.2f}")


HEAD = "| Annual | Vol | Sharpe | Worst drawdown | Calmar | Sharpe 2008-16 | Sharpe 2017-26 | Passes the rule |"


def section_stops():
    ref = base("NONE")
    print(f"\n### A. Stops on the book (after costs; daily {DAYS[0]} to {DAYS[-1]}). The rule is judged against NONE.\n")
    print("| Stop " + HEAD + " Exits a year |\n|---|---|---|---|---|---|---|---|---|---|")
    passing = []
    for s in STOPS:
        r = base(s[0])
        ok = s[0] != "NONE" and judge(r, ref)
        if ok:
            passing.append((st(r)["sharpe"], s[0]))
        print(f"| {s[0]} | {row(r)} | {'yes' if ok else ('-' if s[0] == 'NONE' else 'no')} | {CACHE[s[0]][1]['exits']:.1f} |")
    best = max(passing)[1] if passing else "NONE"
    print(f"\nBest stop by the rule: **{best}**")
    return best


def section_overlays(stop_name):
    r0 = base(stop_name)
    print(f"\n### B. Overlays on the book with stop {stop_name} (after costs). The rule is judged against 'none'.\n")
    print("| Overlay " + HEAD + " Share of days on | Changes a year |\n|---|---|---|---|---|---|---|---|---|---|---|")
    passing = []
    for o in OVERLAYS:
        r, expo, hedge = overlay(o, r0)
        ok = o != "none" and judge(r, r0)
        if ok:
            passing.append((st(r)["sharpe"], o))
        on = sum(1 for j in range(1, NDAYS) if expo[j] < 1 or hedge[j] > 0) / (NDAYS - 1)
        ch = sum(1 for j in range(1, NDAYS) if expo[j] != expo[j - 1] or hedge[j] != hedge[j - 1]) / ((NDAYS - 1) / 252)
        print(f"| {o} | {row(r)} | {'yes' if ok else ('-' if o == 'none' else 'no')} | {on * 100:.0f}% | {ch:.1f} |")
    best = max(passing)[1] if passing else None
    print(f"\nBest overlay by the rule on {stop_name}: **{best}**")
    return best


def section_combined(best_stop, best_by_base):
    ov = best_by_base.get(best_stop) or best_by_base.get("NONE")
    print(f"\n### C. The best stop with the best overlay: {best_stop} + {ov}\n")
    print("| Book " + HEAD.replace(" Passes the rule |", "") + "\n|---|---|---|---|---|---|---|---|")
    for label, r in candidates(best_stop, best_by_base):
        print(f"| {label} | {row(r)} |")
    return ov


def candidates(best_stop, best_by_base):
    ov = best_by_base.get(best_stop) or best_by_base.get("NONE")
    out = [("No stop, no overlay", base("NONE")), ("TRAIL15 (COMBO_BOOK.md's main)", base("TRAIL15"))]
    if best_stop not in ("NONE", "TRAIL15"):
        out.append((f"{best_stop}", base(best_stop)))
    for s in ("NONE", "TRAIL15"):
        if best_by_base.get(s):
            out.append((f"{s} + {best_by_base[s]}", overlay(best_by_base[s], base(s))[0]))
    if ov:
        out.append((f"{best_stop} + {ov} (C)", overlay(ov, base(best_stop))[0]))
    out.append(("TRAIL15 + MA100 50% (the usual hedge)", overlay("MA100 50%", base("TRAIL15"))[0]))
    seen, uniq = set(), []
    for label, r in out:
        key = label.split(" (")[0]
        if key not in seen:
            seen.add(key)
            uniq.append((label, r))
    return uniq + [("SPY", SPY)]


WINDOWS = [("Lehman crash", "2008-09-01", "2009-03-09"), ("US downgrade", "2011-07-22", "2011-10-03"),
           ("China / oil", "2015-08-01", "2016-02-11"), ("Q4 2018", "2018-09-20", "2018-12-24"),
           ("Covid crash", "2020-02-19", "2020-03-23"), ("2022 bear", "2022-01-03", "2022-10-12"),
           ("Tariff shock", "2025-02-19", "2025-04-08")]


def window_ret(r, a, b):
    return math.prod(1 + x for d, x in zip(DAYS[1:], r[1:]) if a < d <= b) - 1


def section_windows(cands):
    print("\n### S&P stress windows (descriptive; return from the first date's close to the last date's close)\n")
    print("| Window | " + " | ".join(l for l, _ in cands) + " |\n|---|" + "---|" * len(cands))
    for name, a, b in WINDOWS:
        print(f"| {name} ({a} to {b}) | " + " | ".join(f"{window_ret(r, a, b) * 100:+.1f}%" for _, r in cands) + " |")


def section_years(cands):
    yrs = sorted({d[:4] for d in DAYS[1:]})
    print("\n### Calendar years\n")
    print("| Year | " + " | ".join(l for l, _ in cands) + " |\n|---|" + "---|" * len(cands))
    for y in yrs:
        print(f"| {y} | " + " | ".join(f"{(math.prod(1 + x for d, x in zip(DAYS[1:], r[1:]) if d[:4] == y) - 1) * 100:+.1f}%"
                                       for _, r in cands) + " |")


def section_now():
    d = GD[-1]
    print(f"\n### The signals now (S&P close {d}: {G[d]:,.0f})\n")
    for n in (50, 100, 200):
        print(f"- {n}-day average {MA[n][d]:,.0f}: the S&P is {'BELOW' if G[d] < MA[n][d] else 'above'} it "
              f"({(G[d] / MA[n][d] - 1) * 100:+.1f}%)")
    i = len(GD) - 1
    hi = max(GC[i - 251: i + 1])
    vol = statistics.pstdev([GC[k] / GC[k - 1] - 1 for k in range(i - 20, i + 1)]) * math.sqrt(252)
    print(f"- 50-day vs 200-day: {'below (death cross)' if MA[50][d] < MA[200][d] else 'above'}")
    print(f"- off the 252-day high: {(G[d] / hi - 1) * 100:+.1f}%; 21-day volatility {vol * 100:.1f}%")


def main(json_path=None):
    print(f"HINDSIGHT (post-hoc book; risk controls judged by a rule fixed in advance). Daily {DAYS[0]} to {DAYS[-1]}.")
    chk = (st(base("TRAIL15"))["cagr"], st(C.book(BOOK, 1, "TRAIL15"))["cagr"])
    print(f"Check: this engine's TRAIL15 book {chk[0] * 100:+.2f}% a year, combo_book.py's {chk[1] * 100:+.2f}%.")
    best_stop = section_stops()
    best_by_base = {s: section_overlays(s) for s in ("NONE", "TRAIL15")}
    if best_stop not in best_by_base:
        best_by_base[best_stop] = section_overlays(best_stop)
    section_combined(best_stop, best_by_base)
    cands = candidates(best_stop, best_by_base)
    section_windows(cands)
    section_years(cands)
    section_now()
    if json_path:
        week = [datetime.date.fromisoformat(x).isocalendar()[:2] for x in DAYS]
        keep = [j for j in range(NDAYS) if j == 0 or j == NDAYS - 1 or week[j] != week[j + 1]]
        curves = {}
        for label, r in cands:
            v, pk, eq, dd = 1.0, 1.0, [], []
            for j, x in enumerate(r):
                v *= 1 + (x if j else 0.0)
                pk = max(pk, v)
                eq.append(v)
                dd.append(v / pk - 1)
            s, s1, s2 = st(r), st(r, hi="2016"), st(r, lo="2017")
            curves[label] = {"eq": [round(eq[j], 5) for j in keep], "dd": [round(dd[j], 5) for j in keep],
                             "stats": [s["cagr"], s["vol"], s["sharpe"], s["mdd"], s1["sharpe"], s2["sharpe"]],
                             "windows": [window_ret(r, a, b) for _, a, b in WINDOWS]}
        tables = {"stops": [[s[0], *(lambda r: [st(r)["cagr"], st(r)["sharpe"], st(r)["mdd"], st(r, hi="2016")["sharpe"],
                                                 st(r, lo="2017")["sharpe"], s[0] != "NONE" and judge(r, base("NONE"))])(base(s[0]))]
                            for s in STOPS],
                  "overlays": {b: [[o, *(lambda r: [st(r)["cagr"], st(r)["sharpe"], st(r)["mdd"], st(r, hi="2016")["sharpe"],
                                                     st(r, lo="2017")["sharpe"], o != "none" and judge(r, base(b))])(overlay(o, base(b))[0])]
                                    for o in OVERLAYS] for b in ("NONE", "TRAIL15")}}
        with open(json_path, "w") as fh:
            d, i = GD[-1], len(GD) - 1
            now = {"date": d, "close": G[d], "ma": {n: MA[n][d] for n in (50, 100, 200)}, "cross": MA[50][d] < MA[200][d],
                   "off_high": G[d] / max(GC[i - 251: i + 1]) - 1,
                   "vol21": statistics.pstdev([GC[k] / GC[k - 1] - 1 for k in range(i - 20, i + 1)]) * math.sqrt(252)}
            json.dump({"dates": [DAYS[j] for j in keep], "curves": curves, "windows": WINDOWS, "tables": tables,
                       "best_stop": best_stop, "best_overlay": best_by_base, "now": now}, fh)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args[args.index("--json") + 1] if "--json" in args else None)
