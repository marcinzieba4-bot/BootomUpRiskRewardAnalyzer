#!/usr/bin/env python3
"""
HINDSIGHT: the three lowest Ratio B stocks, held long and rebalanced monthly, with a tactical S&P 500 hedge. Prints the
tables quoted in staging/retrospective/RATIO_B_HEDGE.md.

THE RULES, fixed in this docstring before the first run; every variant below is printed.
- Long book: RANK3's long leg from ratio_b_basket.py, unchanged. Each month the three tickers with the lowest
  point-in-time Ratio B, equal weight, entered at the next trading day's close after formation, held to the next month's
  entry. Dividends reinvested.
- Hedge (the main case, TACTICAL): when the S&P 500 index (^GSPC) closes below its 100-day simple moving average, short
  SPY equal to 100% of the portfolio, from the NEXT trading day's close. Close the short at the next trading day's close
  after the index closes back above the average. While on, the hedge is kept at 100% of the portfolio each day. The short
  pays SPY's dividends (its total return).
- Not modelled: interest on the short proceeds or idle cash (it would add to every hedged variant), borrow fees,
  commissions, taxes.
- Compared with: SPY; EQUAL (all eleven, rebalanced monthly); LONG3 (unhedged); ALWAYS (LONG3 with SPY shorted every
  day); HEDGE ONLY (the short SPY leg alone, flat when off); EQUAL + TACTICAL (the same hedge on the equal basket).
- Sensitivity: a 50% hedge; trading at the signal day's own close; a 50-day and a 200-day average.
- Stats from daily returns: annual return, volatility, Sharpe (no risk-free rate), worst drawdown, return / worst
  drawdown, beta to SPY, share of days hedged, hedge entries per year, the median hedge spell. Then calendar years, every
  SPY drawdown of 15% or more (peak to trough, and the six months after the trough), four sub-periods, and each ticker
  left out of the long book in turn.

Everything printed is a label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule"). The first run needs the network (retro/.cache/, gitignored).

    python3 staging/retrospective/ratio_b_hedge.py                  # every table
    python3 staging/retrospective/ratio_b_hedge.py summary episodes  # selected sections

Sections: summary sens years episodes periods loo worst now
(worst was added after the first run.)
"""
import bisect
import math
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ratio_b_basket as B  # noqa: E402  (the long book's signals, entries and the total-return indices)

rt = B.rt
GSPC, _ = rt.fetch_prices("^GSPC")
GDAYS = sorted(GSPC)
DAYS = [d for d in B.DAYS if B.ENTRY[B.MONTHS[0]] <= d <= B.LAST]


def below_ma(n):
    """{day: True if the S&P 500 closed below its n-day simple moving average that day}."""
    out, closes = {}, [GSPC[d] for d in GDAYS]
    run = sum(closes[:n])
    for i in range(n - 1, len(GDAYS)):
        if i >= n:
            run += closes[i] - closes[i - n]
        out[GDAYS[i]] = closes[i] < run / n
    return out


def long_book(universe=B.TICKERS, basket="RANK3"):
    """Daily returns of the long leg (and the names held), position over (DAYS[j-1], DAYS[j]]."""
    months = B.MONTHS
    entries = [B.ENTRY[m] for m in months]
    names = {m: B.legs(basket, [s for t, s in B.FIRST[m].items() if t in universe])[0] for m in months}
    rets, held = [0.0], [names[months[0]]]
    for j in range(1, len(DAYS)):
        prev, d = DAYS[j - 1], DAYS[j]
        m = months[bisect.bisect_right(entries, prev) - 1]           # the basket held at the previous close
        e = B.ENTRY[m]
        v0 = statistics.fmean(B.level(t, prev) / B.level(t, e) for t in names[m])
        v1 = statistics.fmean(B.level(t, d) / B.level(t, e) for t in names[m])
        rets.append(v1 / v0 - 1)
        held.append(names[m])
    return rets, held


def equal_book():
    months, entries = B.MONTHS, [B.ENTRY[m] for m in B.MONTHS]
    rets = [0.0]
    for j in range(1, len(DAYS)):
        prev, d = DAYS[j - 1], DAYS[j]
        m = months[bisect.bisect_right(entries, prev) - 1]
        e, ts = B.ENTRY[m], list(B.FIRST[m])
        v0 = statistics.fmean(B.level(t, prev) / B.level(t, e) for t in ts)
        v1 = statistics.fmean(B.level(t, d) / B.level(t, e) for t in ts)
        rets.append(v1 / v0 - 1)
    return rets


SPY = [0.0] + [B.level("SPY", DAYS[j]) / B.level("SPY", DAYS[j - 1]) - 1 for j in range(1, len(DAYS))]


def hedge_flags(n=100, lag=1):
    """flags[j] = 1 if the short is on over (DAYS[j-1], DAYS[j]]. lag=1: the signal of day j-2 traded at day j-1's close."""
    sig = below_ma(n)
    return [0] + [int(j - 1 - lag >= 0 and sig[DAYS[j - 1 - lag]]) if lag else int(sig[DAYS[j - 1]]) for j in range(1, len(DAYS))]


def combine(longs, flags, ratio=1.0):
    return [r - ratio * f * s for r, f, s in zip(longs, flags, SPY)]


def stats(rets, flags=None):
    r = rets[1:]
    n = len(r)
    v, peak, mdd = 1.0, 1.0, 0.0
    for x in r:
        v *= 1 + x
        peak = max(peak, v)
        mdd = min(mdd, v / peak - 1)
    years = (len(DAYS) - 1) / 252
    cagr = v ** (1 / years) - 1
    mu, sd = statistics.fmean(r), statistics.pstdev(r)
    s = SPY[1:]
    ms = statistics.fmean(s)
    beta = sum((a - mu) * (b - ms) for a, b in zip(r, s)) / sum((b - ms) ** 2 for b in s)
    out = {"cagr": cagr, "vol": sd * math.sqrt(252), "sharpe": mu / sd * math.sqrt(252) if sd else 0.0, "mdd": mdd,
           "calmar": cagr / -mdd if mdd else 0.0, "beta": beta, "total": v - 1}
    if flags:
        f = flags[1:]
        spells, cur = [], 0
        for x in f:
            if x:
                cur += 1
            elif cur:
                spells.append(cur)
                cur = 0
        if cur:
            spells.append(cur)
        out.update(hedged=sum(f) / n, entries=len(spells) / years, spell=statistics.median_high(spells) if spells else 0)
    return out


def pct(v):
    return f"{v * 100:+.1f}%"


LONG3, HELD = long_book()
EQUAL = equal_book()
FLAGS = hedge_flags()
MAIN = {
    "SPY": (SPY, None),
    "EQUAL (all eleven)": (EQUAL, None),
    "LONG3 (unhedged)": (LONG3, None),
    "LONG3 + ALWAYS short SPY": (combine(LONG3, [0] + [1] * (len(DAYS) - 1)), None),
    "**LONG3 + TACTICAL hedge (100-day)**": (combine(LONG3, FLAGS), FLAGS),
    "HEDGE ONLY (short SPY below the 100-day)": (combine([0.0] * len(DAYS), FLAGS), FLAGS),
    "EQUAL + TACTICAL hedge": (combine(EQUAL, FLAGS), FLAGS),
}
TACT = MAIN["**LONG3 + TACTICAL hedge (100-day)**"][0]


def row(name, rets, flags):
    st = stats(rets, flags)
    h = (f"{st['hedged'] * 100:.0f}% | {st['entries']:.1f} | {st['spell']}" if flags else " - | - | -")
    return (f"| {name} | {pct(st['cagr'])} | {st['vol'] * 100:.1f}% | {st['sharpe']:.2f} | {st['mdd'] * 100:.0f}% | {st['calmar']:.2f} | "
            f"{st['beta']:+.2f} | {pct(st['total'])} | {h} |")


HEAD = ("| Strategy | Annual return | Volatility | Sharpe | Worst drawdown | Return / drawdown | Beta to SPY | Total | Days hedged | "
        "Hedge entries a year | Median spell (days) |\n|---|---|---|---|---|---|---|---|---|---|---|")


def section_summary():
    print(f"\n### {DAYS[0]} to {DAYS[-1]} ({(len(DAYS) - 1) / 252:.1f} years of daily returns)\n")
    print(HEAD)
    for k, (r, f) in MAIN.items():
        print(row(k, r, f))


def section_sens():
    print("\n### Sensitivity: the hedge's size, timing and average\n")
    print(HEAD)
    variants = (("100-day, 100% hedge, next-day close (main)", 100, 1, 1.0), ("100-day, 50% hedge", 100, 1, 0.5),
                ("100-day, traded at the signal day's close", 100, 0, 1.0), ("50-day average", 50, 1, 1.0),
                ("200-day average", 200, 1, 1.0))
    for name, n, lag, ratio in variants:
        f = hedge_flags(n, lag)
        print(row(name, combine(LONG3, f, ratio), f))


def yearly(rets, y):
    return math.prod(1 + r for d, r in zip(DAYS[1:], rets[1:]) if d[:4] == y) - 1


def section_years():
    cols = ("SPY", "EQUAL (all eleven)", "LONG3 (unhedged)", "LONG3 + ALWAYS short SPY", "**LONG3 + TACTICAL hedge (100-day)**",
            "HEDGE ONLY (short SPY below the 100-day)")
    print("\n### Calendar years\n")
    print("| Year | SPY | EQUAL | LONG3 | LONG3 always hedged | **LONG3 tactical** | Hedge leg | Days hedged |\n|---|---|---|---|---|---|---|---|")
    yrs = sorted({d[:4] for d in DAYS[1:]})
    for y in yrs:
        hd = [f for d, f in zip(DAYS[1:], FLAGS[1:]) if d[:4] == y]
        print(f"| {y} | " + " | ".join(pct(yearly(MAIN[c][0], y)) for c in cols) + f" | {100 * sum(hd) / len(hd):.0f}% |")
    print("| years positive | " + " | ".join(f"{sum(yearly(MAIN[c][0], y) > 0 for y in yrs)} of {len(yrs)}" for c in cols) + " | |")
    print("| years beating SPY | " + " | ".join(f"{sum(yearly(MAIN[c][0], y) > yearly(SPY, y) for y in yrs)} of {len(yrs)}" for c in cols) + " | |")


def episodes(threshold=0.15):
    """SPY total-return drawdowns of `threshold` or more: (peak day, trough day)."""
    out, v, peak, pk, tr, tv, inside = [], 1.0, 1.0, DAYS[0], None, None, False
    for d, r in zip(DAYS[1:], SPY[1:]):
        v *= 1 + r
        if v >= peak:
            if inside:
                out.append((pk, tr))
                inside = False
            peak, pk, tr, tv = v, d, None, None
        else:
            if tv is None or v < tv:
                tr, tv = d, v
            if v / peak - 1 <= -threshold:
                inside = True
    if inside:
        out.append((pk, tr))
    return out


def window(rets, a, b):
    return math.prod(1 + r for d, r in zip(DAYS[1:], rets[1:]) if a < d <= b) - 1


def section_episodes():
    print("\n### Every SPY drawdown of 15% or more: peak to trough, then the six months after the trough\n")
    print("| SPY peak - trough | SPY | LONG3 | LONG3 tactical | Days hedged | After the trough: SPY | LONG3 | LONG3 tactical |")
    print("|---|---|---|---|---|---|---|---|")
    for a, b in episodes():
        after = DAYS[min(len(DAYS) - 1, DAYS.index(b) + 126)]
        hd = [f for d, f in zip(DAYS[1:], FLAGS[1:]) if a < d <= b]
        print(f"| {a} - {b} | {pct(window(SPY, a, b))} | {pct(window(LONG3, a, b))} | {pct(window(TACT, a, b))} | "
              f"{100 * sum(hd) / max(1, len(hd)):.0f}% | {pct(window(SPY, b, after))} | {pct(window(LONG3, b, after))} | {pct(window(TACT, b, after))} |")


PERIODS = (("2008-2012", "2008", "2012"), ("2013-2017", "2013", "2017"), ("2018-2022", "2018", "2022"), ("2023-2026", "2023", "2026"))


def section_periods():
    print("\n### Sub-periods (annual return / worst drawdown)\n")
    print("| Strategy | " + " | ".join(p for p, _, _ in PERIODS) + " |\n|---|" + "---|" * len(PERIODS))
    for k in ("SPY", "LONG3 (unhedged)", "LONG3 + ALWAYS short SPY", "**LONG3 + TACTICAL hedge (100-day)**", "HEDGE ONLY (short SPY below the 100-day)"):
        r = MAIN[k][0]
        cells = []
        for _, a, z in PERIODS:
            sub = [x for d, x in zip(DAYS[1:], r[1:]) if a <= d[:4] <= z]
            yrs = len(sub) / 252
            v, pk, mdd = 1.0, 1.0, 0.0
            for x in sub:
                v *= 1 + x
                pk = max(pk, v)
                mdd = min(mdd, v / pk - 1)
            cells.append(f"{pct(v ** (1 / yrs) - 1)} / {mdd * 100:.0f}%")
        print(f"| {k} | " + " | ".join(cells) + " |")


def section_loo():
    print("\n### Each ticker left out of the long book in turn (LONG3 + TACTICAL: annual return / worst drawdown)\n")
    print("| All | " + " | ".join(f"no {t}" for t in B.TICKERS) + " |\n|---|" + "---|" * len(B.TICKERS))
    full = stats(TACT)
    cells = []
    for t in B.TICKERS:
        lr, _ = long_book(tuple(u for u in B.TICKERS if u != t))
        st = stats(combine(lr, FLAGS))
        cells.append(f"{pct(st['cagr'])} / {st['mdd'] * 100:.0f}%")
    print(f"| {pct(full['cagr'])} / {full['mdd'] * 100:.0f}% | " + " | ".join(cells) + " |")


def section_worst():
    """Added after the first run: when did each strategy's worst drawdown happen?"""
    print("\n### Where each worst drawdown sat (added after the first run)\n")
    print("| Strategy | Worst drawdown | Peak | Trough | Recovered |\n|---|---|---|---|---|")
    for k, (r, _) in MAIN.items():
        v, peak, pk, best = 1.0, 1.0, DAYS[0], (0.0, None, None)
        path = []
        for d, x in zip(DAYS[1:], r[1:]):
            v *= 1 + x
            if v > peak:
                peak, pk = v, d
            path.append((d, v))
            if v / peak - 1 < best[0]:
                best = (v / peak - 1, pk, d, peak)
        rec = next((d for d, x in path if d > best[2] and x >= best[3]), "not yet")
        print(f"| {k} | {best[0] * 100:.0f}% | {best[1]} | {best[2]} | {rec} |")


def section_now():
    sig = below_ma(100)
    d = GDAYS[-1]
    i = GDAYS.index(d)
    ma = statistics.fmean(GSPC[x] for x in GDAYS[i - 99:i + 1])
    print(f"\n### Now\n\nS&P 500 close {GSPC[d]:,.2f} on {d}; 100-day average {ma:,.2f} "
          f"({(GSPC[d] / ma - 1) * 100:+.1f}%): {'BELOW, the hedge is on' if sig[d] else 'above, no hedge'}. "
          f"Long book held since the last entry: {', '.join(HELD[-1])}.")


SECTIONS = {"summary": section_summary, "sens": section_sens, "years": section_years, "episodes": section_episodes,
            "periods": section_periods, "loo": section_loo, "worst": section_worst,
            "now": section_now}

if __name__ == "__main__":
    print(f"HINDSIGHT. Long book RANK3 (ratio_b_basket.py), daily from {DAYS[0]} to {DAYS[-1]}; hedge on ^GSPC's 100-day average.")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
