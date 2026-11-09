#!/usr/bin/env python3
"""
HINDSIGHT: long the lowest Ratio B stocks and short the stocks with falling EPS, optimised the honest way: settings
chosen on one half of the years and judged on the other. Prints the tables quoted in
staging/retrospective/RATIO_B_EPS_LS.md.

THE PROCEDURE, fixed in this docstring before the first run.
- Monthly, on each ticker's first as-of date of the month. Entry is at the next trading day's close, held to the next
  month's entry; dividends are reinvested and the shorts pay them (RET and FIRST from ratio_b_basket.py). Point-in-time
  falling-EPS readings come from epp_short.py: E1 (the last fiscal year's EPS below the year before) and E2 (the EPS the
  floor uses, lower than 26 weeks earlier, adjusted for splits).
- The book: long 100% in the N lowest Ratio B stocks (equal weight). Short SIZE x 100% in the falling-EPS stocks (equal
  weight within each monthly cohort; a cohort is held HOLD months, overlapping). No costs, borrow fees or cash interest.
- The settings, all combinations, 216 per universe:
  - N: 2, 3 or 4;
  - EXCL: whether falling-EPS stocks (by the same filter) are barred from the long side;
  - FILTER: E1, E2 or E3 (both);
  - HOLD: 1, 3 or 6 months;
  - SIZE: 50% or 100%;
  - EMPTY: in a cohort with no falling-EPS stock, hold cash or short SPY instead.
- Universes: ALL eleven, and NON-TECH (without AAPL, MSFT, AVGO, ACN).
- Optimising:
  - Pick the setting with the best Sharpe on 2008-01 to 2016-12 (TRAIN A), and report it on 2017-01 to 2026-10 (TEST A),
    untouched. Then the reverse (TRAIN B = 2017-2026, TEST B = 2008-2016).
  - Also: the rank correlation of all 216 settings' train and test Sharpes (does a good setting stay good?); the average
    Sharpe for each value of each setting over the full period (where the plateau is); the full-period best setting,
    which is in-sample and labelled so; and the chosen setting's calendar years and leave-one-ticker-out results.
- Benchmarks: SPY; EQUAL (all of the universe); the long side alone; the long side minus 100% SPY.

Everything printed is a label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule"). Reads only; the first run needs the network (retro/.cache/, gitignored).

    python3 staging/retrospective/ratio_b_eps_ls.py                # every table
    python3 staging/retrospective/ratio_b_eps_ls.py split plateau  # selected sections

Sections: bench split plateau best years loo now
"""
import contextlib
import io
import itertools
import math
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import epp_short as ES  # noqa: E402  (falling-EPS readings; it also loads ratio_b_basket)
B, X = ES.B, ES.X
MONTHS, RET, FIRST = B.MONTHS, B.RET, B.FIRST
TECH = ("AAPL", "MSFT", "AVGO", "ACN")
UNIVERSES = (("ALL eleven", X.ALL), ("NON-TECH seven", tuple(t for t in X.ALL if t not in TECH)))
HALF_A = [m for m in MONTHS if m <= "2016-12"]
HALF_B = [m for m in MONTHS if m >= "2017-01"]
FILTERS = {"E1": lambda r: r["eps_last_down"], "E2": lambda r: r["eps_down26"] is True,
           "E3": lambda r: r["eps_last_down"] and r["eps_down26"] is True}
GRID = [dict(n=n, excl=excl, filt=f, hold=h, size=s, empty=e)
        for n, excl, f, h, s, e in itertools.product((2, 3, 4), (False, True), ("E1", "E2", "E3"), (1, 3, 6), (0.5, 1.0), ("cash", "SPY"))]
med = statistics.median_high


def row(t, m):
    return ES.ROW[(t, FIRST[m][t]["as_of"])]


def series(cfg, universe):
    """Monthly portfolio returns {month: r} and the share of months with at least one falling-EPS short formed."""
    f = FILTERS[cfg["filt"]]
    longs, shorts = {}, {}
    for m in MONTHS:
        names = [t for t in FIRST[m] if t in universe]
        falling = [t for t in names if f(row(t, m))]
        pool = [FIRST[m][t] for t in names if not (cfg["excl"] and t in falling)] or [FIRST[m][t] for t in names]
        longs[m] = [s["ticker"] for s in sorted(pool, key=B.rank_key)[:cfg["n"]]]
        shorts[m] = falling
    out = {}
    for j, m in enumerate(MONTHS):
        lr = statistics.fmean(RET[m][t] for t in longs[m])
        legs = []
        for c in MONTHS[max(0, j - cfg["hold"] + 1): j + 1]:
            if shorts[c]:
                legs.append(statistics.fmean(RET[m][t] for t in shorts[c]))
            else:
                legs.append(RET[m]["SPY"] if cfg["empty"] == "SPY" else 0.0)
        out[m] = lr - cfg["size"] * statistics.fmean(legs)
    return out, sum(bool(shorts[m]) for m in MONTHS) / len(MONTHS)


def stats(xs):
    n = len(xs)
    g = math.prod(1 + x for x in xs)
    mu, sd = statistics.fmean(xs), statistics.pstdev(xs)
    v, pk, mdd = 1.0, 1.0, 0.0
    for x in xs:
        v *= 1 + x
        pk = max(pk, v)
        mdd = min(mdd, v / pk - 1)
    return {"cagr": g ** (12 / n) - 1, "vol": sd * math.sqrt(12), "sharpe": mu / sd * math.sqrt(12) if sd else 0.0, "mdd": mdd}


def beta(months, s):
    xs, ys = [s[m] for m in months], [RET[m]["SPY"] for m in months]
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((y - my) ** 2 for y in ys)


def pct(v):
    return f"{v * 100:+.1f}%"


def label(c):
    return (f"N={c['n']}, {'bar falling-EPS from long' if c['excl'] else 'long unfiltered'}, short {c['filt']}, "
            f"hold {c['hold']}m, size {c['size']:.0%}, empty={c['empty']}")


def spearman(a, b):
    return X.spearman(a, b)


RESULTS = {}
for name, u in UNIVERSES:
    RESULTS[name] = [(cfg, *series(cfg, u)) for cfg in GRID]


def cell(s, months):
    st = stats([s[m] for m in months])
    return f"{pct(st['cagr'])} / {st['sharpe']:.2f} / {st['mdd'] * 100:.0f}%"


def section_bench():
    print("\n### Benchmarks (annual return / Sharpe / worst drawdown)\n")
    print("| Universe | Series | 2008-2016 | 2017-2026 | Full period |\n|---|---|---|---|---|")
    for name, u in UNIVERSES:
        spy = {m: RET[m]["SPY"] for m in MONTHS}
        eq = {m: statistics.fmean(RET[m][t] for t in FIRST[m] if t in u) for m in MONTHS}
        low3 = {m: [x["ticker"] for x in sorted((FIRST[m][t] for t in FIRST[m] if t in u), key=B.rank_key)[:3]] for m in MONTHS}
        lo = {m: statistics.fmean(RET[m][t] for t in low3[m]) for m in MONTHS}
        hedged = {m: lo[m] - RET[m]["SPY"] for m in MONTHS}
        for lab, s in (("SPY", spy), ("EQUAL", eq), ("long 3 lowest Ratio B, no short", lo), ("long 3 lowest minus 100% SPY", hedged)):
            print(f"| {name} | {lab} | {cell(s, HALF_A)} | {cell(s, HALF_B)} | {cell(s, MONTHS)} |")


def section_split():
    for name, _ in UNIVERSES:
        res = RESULTS[name]
        print(f"\n### {name}: optimise on one half, judge on the other (annual return / Sharpe / worst drawdown)\n")
        print("| Chosen on | Setting chosen | Train | Test (untouched) | Test rank of 216 | Median setting in test |\n|---|---|---|---|---|---|")
        for train, test, tl in ((HALF_A, HALF_B, "2008-2016"), (HALF_B, HALF_A, "2017-2026")):
            sh_tr = [stats([s[m] for m in train])["sharpe"] for _, s, _ in res]
            sh_te = [stats([s[m] for m in test])["sharpe"] for _, s, _ in res]
            i = max(range(len(res)), key=lambda k: sh_tr[k])
            rank = 1 + sum(x > sh_te[i] for x in sh_te)
            mid = sorted(range(len(res)), key=lambda k: sh_te[k])[len(res) // 2]
            print(f"| {tl} | {label(res[i][0])} | {cell(res[i][1], train)} | **{cell(res[i][1], test)}** | {rank} | {cell(res[mid][1], test)} |")
            top = sorted(range(len(res)), key=lambda k: -sh_tr[k])[:10]
            print(f"| {tl}, top 10 averaged | the ten best on train | Sharpe {statistics.fmean(sh_tr[k] for k in top):.2f} | "
                  f"Sharpe {statistics.fmean(sh_te[k] for k in top):.2f} | - | Sharpe {med(sh_te):.2f} (all 216) |")
        sa = [stats([s[m] for m in HALF_A])["sharpe"] for _, s, _ in res]
        sb = [stats([s[m] for m in HALF_B])["sharpe"] for _, s, _ in res]
        print(f"\nRank correlation of the 216 settings' Sharpe, 2008-2016 against 2017-2026: {spearman(sa, sb):+.2f} "
              f"(+1: the same settings win in both halves; 0: winning in one half says nothing about the other).")


def section_plateau():
    keys = (("n", "long names"), ("excl", "bar falling-EPS from long"), ("filt", "short filter"), ("hold", "short hold, months"),
            ("size", "short size"), ("empty", "no falling-EPS stock"))
    for name, _ in UNIVERSES:
        res = RESULTS[name]
        print(f"\n### {name}: average Sharpe of every setting that shares a value (2008-2016 / 2017-2026 / full)\n")
        print("| Setting | Value | Settings | 2008-2016 | 2017-2026 | Full period |\n|---|---|---|---|---|---|")
        for k, lab in keys:
            for v in sorted({c[k] for c, _, _ in res}, key=str):
                g = [s for c, s, _ in res if c[k] == v]
                a = statistics.fmean(stats([s[m] for m in HALF_A])["sharpe"] for s in g)
                b = statistics.fmean(stats([s[m] for m in HALF_B])["sharpe"] for s in g)
                f = statistics.fmean(stats([s[m] for m in MONTHS])["sharpe"] for s in g)
                print(f"| {lab} | {v} | {len(g)} | {a:.2f} | {b:.2f} | {f:.2f} |")


def chosen(name):
    """The full-period best Sharpe among settings that rank in the top quarter of BOTH halves (in-sample, labelled so)."""
    res = RESULTS[name]
    sa = [stats([s[m] for m in HALF_A])["sharpe"] for _, s, _ in res]
    sb = [stats([s[m] for m in HALF_B])["sharpe"] for _, s, _ in res]
    qa, qb = sorted(sa)[int(0.75 * len(sa))], sorted(sb)[int(0.75 * len(sb))]
    both = [k for k in range(len(res)) if sa[k] >= qa and sb[k] >= qb]
    pool = both or list(range(len(res)))
    k = max(pool, key=lambda k: stats([res[k][1][m] for m in MONTHS])["sharpe"])
    return res[k], len(both)


def section_best():
    print("\n### The in-sample pick: best full-period Sharpe among settings in the top quarter of both halves (IN-SAMPLE)\n")
    print("| Universe | Setting | Settings in both top quarters | 2008-2016 | 2017-2026 | Full period | Beta to SPY | Months with a falling-EPS short |")
    print("|---|---|---|---|---|---|---|---|")
    for name, _ in UNIVERSES:
        (cfg, s, active), nboth = chosen(name)
        print(f"| {name} | {label(cfg)} | {nboth} | {cell(s, HALF_A)} | {cell(s, HALF_B)} | **{cell(s, MONTHS)}** | {beta(MONTHS, s):+.2f} | {active * 100:.0f}% |")


def section_years():
    yrs = sorted({m[:4] for m in MONTHS})
    picks = {name: chosen(name)[0][1] for name, _ in UNIVERSES}
    print("\n### Calendar years of the in-sample pick\n")
    print("| Year | " + " | ".join(picks) + " | SPY |\n|---|" + "---|" * (len(picks) + 1))
    for y in yrs:
        print(f"| {y} | " + " | ".join(pct(math.prod(1 + s[m] for m in MONTHS if m[:4] == y) - 1) for s in picks.values()) +
              f" | {pct(math.prod(1 + RET[m]['SPY'] for m in MONTHS if m[:4] == y) - 1)} |")
    print("| years positive | " + " | ".join(f"{sum(math.prod(1 + s[m] for m in MONTHS if m[:4] == y) > 1 for y in yrs)} of {len(yrs)}"
                                         for s in picks.values()) + " | |")


def section_loo():
    print("\n### The in-sample pick with each ticker left out (full-period annual return / Sharpe)\n")
    for name, u in UNIVERSES:
        (cfg, _, _), _ = chosen(name)
        cells = []
        for t in u:
            s, _ = series(cfg, tuple(x for x in u if x != t))
            st = stats([s[m] for m in MONTHS])
            cells.append(f"no {t}: {pct(st['cagr'])} / {st['sharpe']:.2f}")
        print(f"- {name}: " + "; ".join(cells))


def section_now():
    print("\n### The newest month in the sample\n")
    m = MONTHS[-1]
    for name, u in UNIVERSES:
        (cfg, _, _), _ = chosen(name)
        f = FILTERS[cfg["filt"]]
        names = [t for t in FIRST[m] if t in u]
        falling = [t for t in names if f(row(t, m))]
        pool = [FIRST[m][t] for t in names if not (cfg["excl"] and t in falling)] or [FIRST[m][t] for t in names]
        longs = [s["ticker"] for s in sorted(pool, key=B.rank_key)[:cfg["n"]]]
        print(f"- {name} ({m}, {label(cfg)}): long {', '.join(longs)}; short {', '.join(falling) or ('SPY' if cfg['empty'] == 'SPY' else 'nothing')}")


SECTIONS = {"bench": section_bench, "split": section_split, "plateau": section_plateau, "best": section_best,
            "years": section_years, "loo": section_loo, "now": section_now}

if __name__ == "__main__":
    print(f"HINDSIGHT. {len(GRID)} settings per universe; months {MONTHS[0]} to {MONTHS[-1]}; halves 2008-2016 / 2017-2026.")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
