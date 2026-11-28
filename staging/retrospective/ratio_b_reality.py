#!/usr/bin/env python3
"""
HINDSIGHT: a reality check on ratio_b_hedge.py's main result (the three lowest Ratio B stocks with a tactical 100-day
S&P 500 hedge, +27% a year 2008-2026). How much of it is the stock list, and how much is Ratio B? Prints the tables quoted
in staging/retrospective/RATIO_B_HEDGE.md, "Is the 27% real?".

THE TESTS, fixed here before the first run:
- random   each month pick three of the listed tickers at random (seeded), same entry, hold and hedge; 300 runs.
           Where does the Ratio B book's result fall in that spread?
- universe the same strategy and its equal-weight benchmark on (a) the eleven without the three biggest compounders
           (AVGO, AAPL, MSFT) and (b) only the six tickers with the lowest total return over the period. (b) selects with
           hindsight in the pessimistic direction, as a stress test.
- contrib  each ticker's share of the Ratio B book's log return, and the months it was held.
- costs    a charge of 0.10% and 0.25% on every dollar traded: the long book's monthly rebalance (from drifted to new
           weights) and each hedge open and close (100% of the portfolio).
- hand     three sample months recomputed from raw closes and dividends, outside the index machinery.

Reads only; writes nothing. Nothing here may enter a model, a fact sheet, a builder or a method rule.

    python3 staging/retrospective/ratio_b_reality.py                # every table
    python3 staging/retrospective/ratio_b_reality.py random costs   # selected sections

Sections: random universe contrib costs hand
"""
import bisect
import math
import os
import random
import statistics
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ratio_b_hedge as H  # noqa: E402  (long book, hedge flags, daily SPY)

B = H.B
DAYS, MONTHS = H.DAYS, B.MONTHS
ENTRIES = [B.ENTRY[m] for m in MONTHS]
YEARS = (len(DAYS) - 1) / 252


def book(names):
    """Daily returns of an equal-weight book bought at each month's entry and held to the next. names: {month: [tickers]}."""
    rets = [0.0]
    for j in range(1, len(DAYS)):
        prev, d = DAYS[j - 1], DAYS[j]
        m = MONTHS[bisect.bisect_right(ENTRIES, prev) - 1]
        e = B.ENTRY[m]
        v0 = statistics.fmean(B.level(t, prev) / B.level(t, e) for t in names[m])
        v1 = statistics.fmean(B.level(t, d) / B.level(t, e) for t in names[m])
        rets.append(v1 / v0 - 1)
    return rets


def cagr(rets):
    return math.prod(1 + r for r in rets[1:]) ** (1 / YEARS) - 1


def mdd(rets):
    v, pk, out = 1.0, 1.0, 0.0
    for r in rets[1:]:
        v *= 1 + r
        pk = max(pk, v)
        out = min(out, v / pk - 1)
    return out


def ratio_b_names(universe):
    return {m: B.legs("RANK3", [s for t, s in B.FIRST[m].items() if t in universe])[0] for m in MONTHS}


def all_names(universe):
    return {m: [t for t in B.FIRST[m] if t in universe] for m in MONTHS}


def pct(v):
    return f"{v * 100:+.1f}%"


MAIN_NAMES = ratio_b_names(B.TICKERS)
MAIN = H.combine(book(MAIN_NAMES), H.FLAGS)


def section_random(runs=300):
    rng = random.Random(20261108)
    res_h, res_u = [], []
    for _ in range(runs):
        names = {m: rng.sample(sorted(B.FIRST[m]), 3) for m in MONTHS}
        r = book(names)
        res_u.append(cagr(r))
        res_h.append(cagr(H.combine(r, H.FLAGS)))
    rb_u, rb_h = cagr(book(MAIN_NAMES)), cagr(MAIN)
    for label, res, rb in (("unhedged", res_u, rb_u), ("with the 100-day hedge", res_h, rb_h)):
        s = sorted(res)
        q = lambda p: s[min(len(s) - 1, int(p * len(s)))]
        print(f"\n### Three random stocks a month from the same eleven, {label} ({runs} runs)\n")
        print("| | Annual return |\n|---|---|")
        for name, v in (("5th percentile", q(0.05)), ("median", q(0.50)), ("95th percentile", q(0.95)), ("best run", s[-1]),
                        ("**Ratio B book**", rb)):
            print(f"| {name} | {pct(v)} |")
        print(f"\nRandom runs at or above the Ratio B book: {sum(x >= rb for x in res)} of {runs}. "
              f"Ratio B book minus the random median: {pct(rb - q(0.5))} a year.")


def section_universe():
    ranked = sorted(B.TICKERS, key=lambda t: B.level(t, B.LAST) / B.level(t, B.ENTRY[next(m for m in MONTHS if t in B.FIRST[m])]))
    sets = (("all eleven", B.TICKERS), ("without AVGO, AAPL, MSFT", tuple(t for t in B.TICKERS if t not in ("AVGO", "AAPL", "MSFT"))),
            (f"only the six weakest ({', '.join(sorted(ranked[:6]))})", tuple(ranked[:6])))
    print("\n### The same strategy on smaller, weaker universes (annual return / worst drawdown)\n")
    print("| Universe | SPY | Equal weight, unhedged | Equal weight + hedge | Ratio B book, unhedged | **Ratio B book + hedge** | "
          "Ratio B minus equal, both hedged |\n|---|---|---|---|---|---|---|")
    for name, u in sets:
        eq, rb = book(all_names(u)), book(ratio_b_names(u))
        eqh, rbh = H.combine(eq, H.FLAGS), H.combine(rb, H.FLAGS)
        print(f"| {name} | {pct(cagr(H.SPY))} / {mdd(H.SPY) * 100:.0f}% | {pct(cagr(eq))} / {mdd(eq) * 100:.0f}% | "
              f"{pct(cagr(eqh))} / {mdd(eqh) * 100:.0f}% | {pct(cagr(rb))} / {mdd(rb) * 100:.0f}% | "
              f"**{pct(cagr(rbh))} / {mdd(rbh) * 100:.0f}%** | {pct(cagr(rbh) - cagr(eqh))} |")


def section_contrib():
    logs, months = defaultdict(float), defaultdict(int)
    for i, m in enumerate(MONTHS):
        end = B.ENTRY[MONTHS[i + 1]] if i + 1 < len(MONTHS) else B.LAST
        for t in MAIN_NAMES[m]:
            logs[t] += math.log(1 + (B.level(t, end) / B.level(t, B.ENTRY[m]) - 1)) / 3
            months[t] += 1
    tot = sum(logs.values())
    print("\n### Where the unhedged Ratio B book's return came from (share of its total log return; months held)\n")
    print("| Ticker | Share of the return | Months in the book |\n|---|---|---|")
    for t in sorted(logs, key=logs.get, reverse=True):
        print(f"| {t} | {100 * logs[t] / tot:.0f}% | {months[t]} |")


def section_costs():
    flags = H.FLAGS
    base = book(MAIN_NAMES)
    print("\n### After trading costs (on every dollar traded: monthly rebalance and each hedge open and close)\n")
    print("| Cost a trade | Annual return | Worst drawdown | Long-book turnover a year | Hedge trades a year |\n|---|---|---|---|---|")
    # turnover: from drifted weights to the new equal weights at each entry
    turn, w_prev = [], None
    for i, m in enumerate(MONTHS):
        new = {t: 1 / 3 for t in MAIN_NAMES[m]}
        if w_prev is not None:
            pm = MONTHS[i - 1]
            grow = {t: B.level(t, B.ENTRY[m]) / B.level(t, B.ENTRY[pm]) for t in w_prev}
            tot = sum(w_prev[t] * grow[t] for t in w_prev)
            drift = {t: w_prev[t] * grow[t] / tot for t in w_prev}
            turn.append(sum(abs(new.get(t, 0) - drift.get(t, 0)) for t in set(new) | set(drift)))
        else:
            turn.append(1.0)
        w_prev = new
    switches = sum(1 for a, b in zip(flags, flags[1:]) if a != b)
    for c in (0.0, 0.001, 0.0025):
        rets = H.combine(base, flags)
        rets = list(rets)
        for i, m in enumerate(MONTHS):                     # charge the rebalance on the first day it is held
            j = bisect.bisect_right(DAYS, B.ENTRY[m])
            if j < len(rets):
                rets[j] -= c * turn[i]
        for j in range(1, len(flags)):
            if flags[j] != flags[j - 1]:
                rets[j] -= c                               # open or close 100% of the portfolio in SPY
        print(f"| {c * 100:.2f}% | {pct(cagr(rets))} | {mdd(rets) * 100:.0f}% | {sum(turn) / YEARS * 100:.0f}% | {switches / YEARS:.1f} |")


def section_hand():
    """Recompute three months from raw closes and dividends: (close_end + dividends paid in between) / close_start."""
    print("\n### Three months recomputed by hand from raw Yahoo closes and dividends (no index machinery)\n")
    print("| Month | Names | Entry | Exit | By hand | Index machinery |\n|---|---|---|---|---|---|")
    for m in ("2009-03", "2016-02", "2022-06"):
        i = MONTHS.index(m)
        a, b = B.ENTRY[m], B.ENTRY[MONTHS[i + 1]]
        hand, mach = [], []
        for t in MAIN_NAMES[m]:
            closes, divs = B.rt.fetch_prices(t)
            _, c0 = B.rt.close_on_or_before(closes, a)
            _, c1 = B.rt.close_on_or_before(closes, b)
            hand.append((c1 + sum(x for d, x in divs if a < d <= b)) / c0 - 1)
            mach.append(B.level(t, b) / B.level(t, a) - 1)
        print(f"| {m} | {', '.join(MAIN_NAMES[m])} | {a} | {b} | {pct(statistics.fmean(hand))} | {pct(statistics.fmean(mach))} |")


SECTIONS = {"random": section_random, "universe": section_universe, "contrib": section_contrib, "costs": section_costs, "hand": section_hand}

if __name__ == "__main__":
    print(f"HINDSIGHT. Ratio B book + 100-day hedge: {pct(cagr(MAIN))} a year, worst drawdown {mdd(MAIN) * 100:.0f}%, {DAYS[0]} to {DAYS[-1]}.")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
