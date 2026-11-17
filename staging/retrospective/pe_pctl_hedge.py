#!/usr/bin/env python3
"""
HINDSIGHT: long the three stocks trading highest against their own 10-year P/E history, with a tactical S&P 500 hedge.
Prints the tables quoted in staging/retrospective/PE_PCTL_HEDGE.md.

THE RULES, fixed in this docstring before the first run; every variant below is printed.
- Universe: the twenty-four retrospective series (RETRO_UNIVERSE=all). Also the ORIGINAL eleven, the NEW thirteen, and
  ALL without tech (AAPL, MSFT, AVGO, ACN, NVDA removed).
- Signal: each ticker's PE_NOW_PCTL (its own 10-year P/E percentile, point-in-time) on its first as-of date of the month.
- Long book: the three highest, equal weight. Ties at the third place share it: names above the tied value get 1/3
  each, and the tied names split what is left equally. The alphabetical tie-break of pattern_search_24.py is printed
  beside it for comparison. Entry at the next trading day's close. Held in overlapping monthly cohorts of 6 months
  (main), or rebalanced monthly (1m). Dividends reinvested; daily returns.
- Hedge: short SPY at 100% or 50% of the portfolio while the S&P 500 closes below its 100-day average (traded at the
  next day's close; ratio_b_hedge.py's rule). Variants: the 200-day average at 50%; a static 50% short. No cash interest
  or borrow fees.
- Compared with: SPY; EQUAL (every ticker of the universe, rebalanced monthly), unhedged and with the same hedge.
- Also:
  - halves (2008-2016, 2017-2026) and calendar years;
  - every SPY drawdown of 15% or more;
  - a 0.10% charge on every dollar traded (monthly book turnover from the target weights, and each hedge open or close);
  - 200 runs of three random tickers a month (seeded), with the same cohorts and hedge;
  - the share of months with a tie at the third place;
  - the current book.

Everything printed is a label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule"). Reads only; the first run needs the network (retro/.cache/, gitignored).

    python3 staging/retrospective/pe_pctl_hedge.py                  # every table
    python3 staging/retrospective/pe_pctl_hedge.py main years       # selected sections

Sections: ties main universes years episodes costs random now
"""
import bisect
import contextlib
import io
import math
import os
import random
import statistics
import sys

os.environ["RETRO_UNIVERSE"] = "all"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import ratio_b_hedge as H  # noqa: E402  (daily calendar, S&P 500 100-day flags, SPY daily, episodes)
B, X = H.B, H.B.X
DAYS, MONTHS = H.DAYS, B.MONTHS
ENTRIES = [B.ENTRY[m] for m in MONTHS]
DAY_POS = {d: j for j, d in enumerate(DAYS)}
ORIGINAL, NEW = X.DISCOVERY + X.TEST, X.LATER
ALL = ORIGINAL + NEW
TECH = ("AAPL", "MSFT", "AVGO", "ACN", "NVDA")
UNIVERSES = (("ALL twenty-four", ALL), ("ORIGINAL eleven", ORIGINAL), ("NEW thirteen", NEW),
             ("ALL without tech", tuple(t for t in ALL if t not in TECH)))
ROWMAP = {(r["ticker"], r["as_of"]): r for r in X.R}
LEVEL = {t: [B.level(t, d) for d in DAYS] for t in ALL}
SPY = H.SPY
YEARS = (len(DAYS) - 1) / 252
FLAG100 = H.FLAGS
FLAG200 = H.hedge_flags(200, 1)
ALWAYS = [0] + [1] * (len(DAYS) - 1)


def pctl(m, t):
    return ROWMAP[(t, FIRST(m)[t]["as_of"])]["pe_pctl"]


def FIRST(m):
    return B.FIRST[m]


def top3(m, u, tie="split"):
    """{ticker: weight} for the three highest own P/E percentiles."""
    names = [t for t in FIRST(m) if t in u]
    if tie == "alpha":                                           # pattern_search_24.py: ties broken by name, descending
        pick = sorted(names, key=lambda t: (pctl(m, t), t), reverse=True)[:3]
        return {t: 1 / 3 for t in pick}
    vals = sorted((pctl(m, t) for t in names), reverse=True)
    cut = vals[min(2, len(vals) - 1)]
    above = [t for t in names if pctl(m, t) > cut]
    tied = [t for t in names if pctl(m, t) == cut]
    w = {t: 1 / 3 for t in above}
    rest = (3 - len(above)) / 3
    for t in tied:
        w[t] = rest / len(tied)
    return w


def equal_w(m, u):
    names = [t for t in FIRST(m) if t in u]
    return {t: 1 / len(names) for t in names}


def daily(weights, hold):
    """Daily returns: each month a cohort is bought at its weights and held `hold` months; live cohorts weigh equally
    from each month's entry and drift within the month."""
    rets = [0.0]
    for j in range(1, len(DAYS)):
        i = bisect.bisect_right(ENTRIES, DAYS[j - 1]) - 1
        m = MONTHS[i]
        e = DAY_POS[B.ENTRY[m]]
        live = MONTHS[max(0, i - hold + 1): i + 1]
        num = den = 0.0
        for c in live:
            ec = DAY_POS[B.ENTRY[c]]
            w = weights[c]
            v = lambda k: sum(x * LEVEL[t][k] / LEVEL[t][ec] for t, x in w.items())
            base = v(e)
            num += v(j) / base
            den += v(j - 1) / base
        rets.append(num / den - 1)
    return rets


def hedged(rets, flags, ratio):
    return [r - ratio * f * s for r, f, s in zip(rets, flags, SPY)]


def stats(r, lo=None, hi=None):
    xs = [x for d, x in zip(DAYS[1:], r[1:]) if (lo is None or d[:4] >= lo) and (hi is None or d[:4] <= hi)]
    v, pk, mdd = 1.0, 1.0, 0.0
    for x in xs:
        v *= 1 + x
        pk = max(pk, v)
        mdd = min(mdd, v / pk - 1)
    mu, sd = statistics.fmean(xs), statistics.pstdev(xs)
    ss = [s for d, s in zip(DAYS[1:], SPY[1:]) if (lo is None or d[:4] >= lo) and (hi is None or d[:4] <= hi)]
    ms = statistics.fmean(ss)
    beta = sum((a - mu) * (b - ms) for a, b in zip(xs, ss)) / sum((b - ms) ** 2 for b in ss)
    return v ** (252 / len(xs)) - 1, sd * math.sqrt(252), mu / sd * math.sqrt(252), mdd, beta


def pct(v):
    return f"{v * 100:+.1f}%"


def cell(r, lo=None, hi=None):
    c, _, sh, dd, _ = stats(r, lo, hi)
    return f"{pct(c)} / {sh:.2f} / {dd * 100:.0f}%"


HEDGES = (("no hedge", None, 0.0), ("S&P 100-day, 100%", FLAG100, 1.0), ("S&P 100-day, 50%", FLAG100, 0.5),
          ("S&P 200-day, 50%", FLAG200, 0.5), ("static 50% SPY short", ALWAYS, 0.5))


def books(u, hold=6, tie="split"):
    w = {m: top3(m, u, tie) for m in MONTHS}
    return daily(w, hold), w


CACHE = {}


def book_for(u, hold=6, tie="split"):
    k = (u, hold, tie)
    if k not in CACHE:
        CACHE[k] = books(u, hold, tie)
    return CACHE[k]


def section_ties():
    n = 0
    for m in MONTHS:
        names = list(FIRST(m))
        vals = sorted((pctl(m, t) for t in names), reverse=True)
        cut = vals[2]
        n += sum(pctl(m, t) == cut for t in names) > 1 and sum(pctl(m, t) >= cut for t in names) > 3
    print(f"\n### Ties: in {n} of {len(MONTHS)} months ({100 * n / len(MONTHS):.0f}%) more than three of the twenty-four stood at or above "
          f"the third-place percentile, so the tie rule decided part of the book.")


def section_main():
    r6, _ = book_for(ALL, 6)
    r1, _ = book_for(ALL, 1)
    ra, _ = book_for(ALL, 6, "alpha")
    eq = daily({m: equal_w(m, ALL) for m in MONTHS}, 1)
    print(f"\n### ALL twenty-four, {DAYS[0]} to {DAYS[-1]} (annual return / Sharpe / worst drawdown, daily data)\n")
    print("| Book | Hedge | Full period | 2008-2016 | 2017-2026 | Volatility | Beta | Days hedged |\n|---|---|---|---|---|---|---|---|")
    print(f"| SPY | - | {cell(SPY)} | {cell(SPY, hi='2016')} | {cell(SPY, lo='2017')} | {stats(SPY)[1] * 100:.0f}% | 1.00 | - |")
    for lab, base in (("EQUAL (all 24)", eq), ("**Top 3 own P/E percentile, 6m cohorts**", r6), ("Top 3, rebalanced monthly", r1),
                      ("Top 3, 6m, alphabetical ties (pattern search)", ra)):
        for hname, fl, ratio in HEDGES:
            if base is not r6 and hname not in ("no hedge", "S&P 100-day, 100%", "S&P 100-day, 50%"):
                continue
            r = base if fl is None else hedged(base, fl, ratio)
            c, vol, sh, dd, b = stats(r)
            hd = f"{100 * sum(fl[1:]) / (len(DAYS) - 1):.0f}%" if fl is not None else "-"
            print(f"| {lab} | {hname} | {cell(r)} | {cell(r, hi='2016')} | {cell(r, lo='2017')} | {vol * 100:.0f}% | {b:+.2f} | {hd} |")


def section_universes():
    print("\n### The same book on each universe (annual return / Sharpe / worst drawdown)\n")
    print("| Universe | EQUAL, no hedge | EQUAL + S&P 100-day 50% | Top 3, no hedge | Top 3 + S&P 100-day 100% | **Top 3 + S&P 100-day 50%** |\n|---|---|---|---|---|---|")
    for name, u in UNIVERSES:
        eq = daily({m: equal_w(m, u) for m in MONTHS}, 1)
        r6, _ = book_for(u, 6)
        print(f"| {name} | {cell(eq)} | {cell(hedged(eq, FLAG100, 0.5))} | {cell(r6)} | {cell(hedged(r6, FLAG100, 1.0))} | {cell(hedged(r6, FLAG100, 0.5))} |")


def section_years():
    r6, _ = book_for(ALL, 6)
    eq = daily({m: equal_w(m, ALL) for m in MONTHS}, 1)
    cols = (("SPY", SPY), ("EQUAL", eq), ("Top 3", r6), ("Top 3 + 100% hedge", hedged(r6, FLAG100, 1.0)), ("Top 3 + 50% hedge", hedged(r6, FLAG100, 0.5)))
    yrs = sorted({d[:4] for d in DAYS[1:]})
    print("\n### Calendar years, ALL twenty-four\n")
    print("| Year | " + " | ".join(n for n, _ in cols) + " | Days hedged |\n|---|" + "---|" * (len(cols) + 1))
    for y in yrs:
        hd = [f for d, f in zip(DAYS[1:], FLAG100[1:]) if d[:4] == y]
        print(f"| {y} | " + " | ".join(pct(math.prod(1 + x for d, x in zip(DAYS[1:], r[1:]) if d[:4] == y) - 1) for _, r in cols) +
              f" | {100 * sum(hd) / len(hd):.0f}% |")
    print("| years positive | " + " | ".join(f"{sum(math.prod(1 + x for d, x in zip(DAYS[1:], r[1:]) if d[:4] == y) > 1 for y in yrs)} of {len(yrs)}"
                                         for _, r in cols) + " | |")


def section_episodes():
    r6, _ = book_for(ALL, 6)
    cols = (("SPY", SPY), ("Top 3", r6), ("Top 3 + 100% hedge", hedged(r6, FLAG100, 1.0)), ("Top 3 + 50% hedge", hedged(r6, FLAG100, 0.5)))
    print("\n### Every SPY drawdown of 15% or more, peak to trough, ALL twenty-four\n")
    print("| SPY peak - trough | " + " | ".join(n for n, _ in cols) + " |\n|---|" + "---|" * len(cols))
    for a, b in H.episodes():
        print(f"| {a} - {b} | " + " | ".join(pct(H.window(r, a, b)) for _, r in cols) + " |")


def section_costs(c=0.001):
    r6, w = book_for(ALL, 6)
    target = {}
    for i, m in enumerate(MONTHS):                               # the portfolio's target weights: the live cohorts averaged
        live = MONTHS[max(0, i - 5): i + 1]
        tw = {}
        for cm in live:
            for t, x in w[cm].items():
                tw[t] = tw.get(t, 0.0) + x / len(live)
        target[m] = tw
    turn = []
    for i, m in enumerate(MONTHS):
        prev = target[MONTHS[i - 1]] if i else {}
        turn.append(sum(abs(target[m].get(t, 0) - prev.get(t, 0)) for t in set(target[m]) | set(prev)))
    print(f"\n### After a {c * 100:.2f}% charge on every dollar traded, ALL twenty-four\n")
    print(f"Book turnover: {sum(turn) / YEARS * 100:.0f}% a year; 100-day hedge entries and exits: "
          f"{sum(1 for a, b in zip(FLAG100, FLAG100[1:]) if a != b) / YEARS:.1f} a year.\n")
    print("| Hedge | Before costs | After costs |\n|---|---|---|")
    for hname, fl, ratio in HEDGES:
        r = list(r6 if fl is None else hedged(r6, fl, ratio))
        base = cell(r)
        for i, m in enumerate(MONTHS):
            j = bisect.bisect_right(DAYS, B.ENTRY[m])
            if j < len(r):
                r[j] -= c * turn[i]
        if fl is not None:
            for j in range(1, len(r)):
                if fl[j] != fl[j - 1]:
                    r[j] -= c * ratio
        print(f"| {hname} | {base} | {cell(r)} |")


def section_random(runs=200):
    rng = random.Random(20261117)
    res_u, res_h = [], []
    for _ in range(runs):
        w = {m: {t: 1 / 3 for t in rng.sample(sorted(FIRST(m)), 3)} for m in MONTHS}
        r = daily(w, 6)
        res_u.append(stats(r)[0])
        res_h.append(stats(hedged(r, FLAG100, 0.5))[0])
    r6, _ = book_for(ALL, 6)
    a, b = stats(r6)[0], stats(hedged(r6, FLAG100, 0.5))[0]
    print(f"\n### Three random tickers a month from the twenty-four, 6m cohorts ({runs} runs)\n")
    print("| Hedge | Random 5th pct | Random median | Random 95th pct | Top 3 own P/E percentile | Runs at or above it |\n|---|---|---|---|---|---|")
    for lab, res, v in (("none", res_u, a), ("S&P 100-day, 50%", res_h, b)):
        s = sorted(res)
        q = lambda p: s[min(len(s) - 1, int(p * len(s)))]
        print(f"| {lab} | {pct(q(0.05))} | {pct(q(0.5))} | {pct(q(0.95))} | **{pct(v)}** | {sum(x >= v for x in s)} of {runs} |")


def section_now():
    latest = {}
    for t in ALL:
        r = max((x for x in X.R if x["ticker"] == t), key=lambda x: x["as_of"])
        latest[t] = r
    order = sorted(ALL, key=lambda t: latest[t]["pe_pctl"], reverse=True)
    m = MONTHS[-1]
    print(f"\n### Now\n\nNewest readings, highest own P/E percentile first: " + ", ".join(f"{t} {latest[t]['pe_pctl']} ({latest[t]['as_of']})" for t in order[:8]) + ".")
    print(f"The last monthly cohort ({m}): " + ", ".join(f"{t} {w * 100:.0f}%" for t, w in sorted(top3(m, ALL).items(), key=lambda x: -x[1])) + ".")
    closes, _ = B.rt.fetch_prices("^GSPC")
    ks = sorted(closes)
    ma = statistics.fmean(closes[k] for k in ks[-100:])
    print(f"S&P 500 {closes[ks[-1]]:,.2f} on {ks[-1]}; 100-day average {ma:,.2f} ({(closes[ks[-1]] / ma - 1) * 100:+.1f}%): "
          f"{'below, the hedge is ON' if closes[ks[-1]] < ma else 'above, no hedge'}.")


SECTIONS = {"ties": section_ties, "main": section_main, "universes": section_universes, "years": section_years,
            "episodes": section_episodes, "costs": section_costs, "random": section_random, "now": section_now}

if __name__ == "__main__":
    print(f"HINDSIGHT. {len(ALL)} tickers; daily {DAYS[0]} to {DAYS[-1]}.")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
