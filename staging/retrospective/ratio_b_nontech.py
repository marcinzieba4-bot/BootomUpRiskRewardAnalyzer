#!/usr/bin/env python3
"""
HINDSIGHT: the Ratio B long book without technology stocks, hedged tactically with the Dow or a Russell index instead of
the S&P 500. Prints the tables quoted in staging/retrospective/RATIO_B_NONTECH.md.

THE RULES, fixed in this docstring before the first run; every variant below is printed.
- Universe (main): the eleven minus the GICS Information Technology sector: AAPL, AVGO, MSFT and ACN (IT services).
  That leaves UNP, LOW, NKE, PEP, SHW, WMT, XOM. Sensitivity: the same with ACN kept (eight tickers).
- Long book: each month the three tickers in the universe with the lowest point-in-time Ratio B, equal weight (RANK3's
  long leg in ratio_b_basket.py, restricted to the universe).
- Hedges: short the ETF equal to 100% (and, as a variant, 50%) of the portfolio while its index closes below its
  100-day simple moving average. Enter and exit at the next trading day's close. Pairs: SPY on ^GSPC (the S&P 500,
  reference), DIA on ^DJI (the Dow), IWM on ^RUT (Russell 2000), IWB on ^RUI (Russell 1000), IWD on ^RLV (Russell 1000
  Value). The short pays the ETF's dividends. No interest on cash, borrow fees or taxes.
- Compared with: each ETF bought and held; the universe's equal-weight basket, unhedged and with each 100% hedge.
- Also: the long book's beta and correlation to each ETF; every SPY drawdown of 15% or more; calendar years; three
  random tickers a month from the same universe (300 runs, seeded); a 0.10% charge on every dollar traded.

Everything printed is a label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule"). Reads only; the first run needs the network (retro/.cache/, gitignored).

    python3 staging/retrospective/ratio_b_nontech.py                # every table
    python3 staging/retrospective/ratio_b_nontech.py summary years  # selected sections

Sections: summary fit years episodes random costs now
"""
import bisect
import math
import os
import random
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ratio_b_reality as R  # noqa: E402  (book(), the daily calendar, cagr/mdd)

H, B = R.H, R.B
DAYS, MONTHS = H.DAYS, B.MONTHS
TECH = ("AAPL", "AVGO", "MSFT", "ACN")
NONTECH = tuple(t for t in B.TICKERS if t not in TECH)
WITH_ACN = NONTECH + ("ACN",)
HEDGES = (("SPY", "^GSPC", "S&P 500"), ("DIA", "^DJI", "Dow"), ("IWM", "^RUT", "Russell 2000"),
          ("IWB", "^RUI", "Russell 1000"), ("IWD", "^RLV", "Russell 1000 Value"))
YEARS = R.YEARS


def daily(symbol):
    days, idx = B.tr_index(symbol)
    lv = lambda d: idx[bisect.bisect_right(days, d) - 1]
    return [0.0] + [lv(DAYS[j]) / lv(DAYS[j - 1]) - 1 for j in range(1, len(DAYS))]


def flags_for(index, n=100):
    """flags[j] = 1 if the short is on over (DAYS[j-1], DAYS[j]]: the index closed below its n-day average on DAYS[j-2]."""
    closes, _ = B.rt.fetch_prices(index)
    ks = sorted(closes)
    below, run = {}, sum(closes[k] for k in ks[:n])
    for i in range(n - 1, len(ks)):
        if i >= n:
            run += closes[ks[i]] - closes[ks[i - n]]
        below[ks[i]] = closes[ks[i]] < run / n
    def on(d):
        i = bisect.bisect_right(ks, d) - 1                     # the index's latest close on or before d
        return below.get(ks[i], False)
    return [0] + [int(j >= 2 and on(DAYS[j - 2])) for j in range(1, len(DAYS))]


ETF = {e: daily(e) for e, _, _ in HEDGES}
FLAG = {e: flags_for(i) for e, i, _ in HEDGES}


def hedge(longs, etf, ratio=1.0):
    return [r - ratio * f * h for r, f, h in zip(longs, FLAG[etf], ETF[etf])]


def stats(r, flags=None):
    xs = r[1:]
    mu, sd = statistics.fmean(xs), statistics.pstdev(xs)
    out = {"cagr": R.cagr(r), "vol": sd * math.sqrt(252), "sharpe": mu / sd * math.sqrt(252), "mdd": R.mdd(r)}
    out["calmar"] = out["cagr"] / -out["mdd"]
    if flags:
        f = flags[1:]
        out["hedged"] = sum(f) / len(f)
        out["entries"] = sum(1 for a, b in zip(f, f[1:]) if b and not a) / YEARS
    return out


def pct(v):
    return f"{v * 100:+.1f}%"


def line(name, r, flags=None):
    st = stats(r, flags)
    tail = f"{st['hedged'] * 100:.0f}% | {st['entries']:.1f}" if flags else "- | -"
    return (f"| {name} | {pct(st['cagr'])} | {st['vol'] * 100:.1f}% | {st['sharpe']:.2f} | {st['mdd'] * 100:.0f}% | "
            f"{st['calmar']:.2f} | {tail} |")


HEAD = ("| Strategy | Annual return | Volatility | Sharpe | Worst drawdown | Return / drawdown | Days hedged | Hedge entries a year |\n"
        "|---|---|---|---|---|---|---|---|")
BOOK = R.book(R.ratio_b_names(NONTECH))
BOOK_ACN = R.book(R.ratio_b_names(WITH_ACN))
EQUAL = R.book(R.all_names(NONTECH))


def section_summary():
    print(f"\n### Non-tech universe ({', '.join(NONTECH)}), {DAYS[0]} to {DAYS[-1]}\n")
    print(HEAD)
    for e, _, name in HEDGES:
        print(line(f"{e} ({name}) bought and held", ETF[e]))
    print(line("Equal weight of the seven, unhedged", EQUAL))
    print(line("**Ratio B book (3 lowest of the seven), unhedged**", BOOK))
    for e, _, name in HEDGES:
        for ratio in (1.0, 0.5):
            print(line(f"Ratio B book + {e} hedge ({name}), {ratio:.0%}", hedge(BOOK, e, ratio), FLAG[e]))
    for e, _, name in HEDGES:
        print(line(f"Equal weight + {e} hedge, 100%", hedge(EQUAL, e), FLAG[e]))
    print(f"\n### Sensitivity: ACN kept ({len(WITH_ACN)} tickers)\n")
    print(HEAD)
    print(line("Ratio B book, unhedged", BOOK_ACN))
    for e, _, name in HEDGES:
        for ratio in (1.0, 0.5):
            print(line(f"Ratio B book + {e} hedge ({name}), {ratio:.0%}", hedge(BOOK_ACN, e, ratio), FLAG[e]))


def section_fit():
    print("\n### How well each index tracks the non-tech book (daily, full period)\n")
    print("| ETF | Beta of the book to it | Correlation | Share of days its index was below the 100-day | ETF annual return |")
    print("|---|---|---|---|---|")
    xs = BOOK[1:]
    for e, _, name in HEDGES:
        ys = ETF[e][1:]
        mx, my = statistics.fmean(xs), statistics.fmean(ys)
        cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        vy, vx = sum((y - my) ** 2 for y in ys), sum((x - mx) ** 2 for x in xs)
        print(f"| {e} ({name}) | {cov / vy:.2f} | {cov / math.sqrt(vx * vy):.2f} | {100 * sum(FLAG[e][1:]) / len(xs):.0f}% | {pct(R.cagr(ETF[e]))} |")


def yearly(r, y):
    return math.prod(1 + x for d, x in zip(DAYS[1:], r[1:]) if d[:4] == y) - 1


def section_years():
    cols = [("SPY", ETF["SPY"]), ("DIA", ETF["DIA"]), ("IWM", ETF["IWM"]), ("Book", BOOK)]
    cols += [(f"Book + {e}", hedge(BOOK, e)) for e, _, _ in HEDGES]
    print("\n### Calendar years (100% hedges)\n")
    print("| Year | " + " | ".join(n for n, _ in cols) + " |\n|---|" + "---|" * len(cols))
    yrs = sorted({d[:4] for d in DAYS[1:]})
    for y in yrs:
        print(f"| {y} | " + " | ".join(pct(yearly(r, y)) for _, r in cols) + " |")
    print("| years positive | " + " | ".join(f"{sum(yearly(r, y) > 0 for y in yrs)} of {len(yrs)}" for _, r in cols) + " |")
    print("| years beating SPY | " + " | ".join(f"{sum(yearly(r, y) > yearly(ETF['SPY'], y) for y in yrs)} of {len(yrs)}" for _, r in cols) + " |")


def section_episodes():
    print("\n### Every SPY drawdown of 15% or more, peak to trough (100% hedges)\n")
    cols = [("SPY", ETF["SPY"]), ("Book", BOOK)] + [(f"Book + {e}", hedge(BOOK, e)) for e, _, _ in HEDGES]
    print("| SPY peak - trough | " + " | ".join(n for n, _ in cols) + " |\n|---|" + "---|" * len(cols))
    for a, b in H.episodes():
        print(f"| {a} - {b} | " + " | ".join(pct(H.window(r, a, b)) for _, r in cols) + " |")


def section_random(runs=300):
    rng = random.Random(20261108)
    res = {e: [] for e, _, _ in HEDGES}
    res["unhedged"] = []
    for _ in range(runs):
        r = R.book({m: rng.sample(sorted(t for t in B.FIRST[m] if t in NONTECH), 3) for m in MONTHS})
        res["unhedged"].append(R.cagr(r))
        for e, _, _ in HEDGES:
            res[e].append(R.cagr(hedge(r, e)))
    print(f"\n### Three random non-tech tickers a month ({runs} runs) against the Ratio B book\n")
    print("| Hedge | Random 5th pct | Random median | Random 95th pct | Ratio B book | Runs at or above the book |\n|---|---|---|---|---|---|")
    for k in ["unhedged"] + [e for e, _, _ in HEDGES]:
        s = sorted(res[k])
        q = lambda p: s[min(len(s) - 1, int(p * len(s)))]
        rb = R.cagr(BOOK if k == "unhedged" else hedge(BOOK, k))
        print(f"| {k} | {pct(q(0.05))} | {pct(q(0.5))} | {pct(q(0.95))} | **{pct(rb)}** | {sum(x >= rb for x in s)} of {runs} |")


def section_costs(c=0.001):
    names = R.ratio_b_names(NONTECH)
    turn, prev = [], None
    for i, m in enumerate(MONTHS):
        new = {t: 1 / 3 for t in names[m]}
        if prev is None:
            turn.append(1.0)
        else:
            pm = MONTHS[i - 1]
            g = {t: B.level(t, B.ENTRY[m]) / B.level(t, B.ENTRY[pm]) for t in prev}
            tot = sum(prev[t] * g[t] for t in prev)
            drift = {t: prev[t] * g[t] / tot for t in prev}
            turn.append(sum(abs(new.get(t, 0) - drift.get(t, 0)) for t in set(new) | set(drift)))
        prev = new
    print(f"\n### After a {c * 100:.2f}% charge on every dollar traded (rebalances and hedge opens/closes)\n")
    print("| Strategy | Annual return | Worst drawdown |\n|---|---|---|")
    for e in [None] + [x for x, _, _ in HEDGES]:
        r = list(BOOK if e is None else hedge(BOOK, e))
        for i, m in enumerate(MONTHS):
            j = bisect.bisect_right(DAYS, B.ENTRY[m])
            if j < len(r):
                r[j] -= c * turn[i]
        if e:
            for j in range(1, len(r)):
                if FLAG[e][j] != FLAG[e][j - 1]:
                    r[j] -= c
        print(f"| Ratio B book{'' if e is None else ' + ' + e + ' hedge'} | {pct(R.cagr(r))} | {R.mdd(r) * 100:.0f}% |")
    print(f"\nLong-book turnover: {sum(turn) / YEARS * 100:.0f}% a year.")


def section_now():
    names = R.ratio_b_names(NONTECH)[MONTHS[-1]]
    print(f"\n### Now\n\nLong book since the last monthly entry ({B.ENTRY[MONTHS[-1]]}): {', '.join(names)}.")
    for e, i, name in HEDGES:
        closes, _ = B.rt.fetch_prices(i)
        ks = sorted(closes)
        ma = statistics.fmean(closes[k] for k in ks[-100:])
        print(f"- {name} ({i}) {closes[ks[-1]]:,.2f} on {ks[-1]}, 100-day average {ma:,.2f} ({(closes[ks[-1]] / ma - 1) * 100:+.1f}%): "
              f"{'below, hedge ON' if closes[ks[-1]] < ma else 'above, no hedge'}")


SECTIONS = {"summary": section_summary, "fit": section_fit, "years": section_years, "episodes": section_episodes,
            "random": section_random, "costs": section_costs, "now": section_now}

if __name__ == "__main__":
    print(f"HINDSIGHT. Non-tech Ratio B book ({', '.join(NONTECH)}), daily {DAYS[0]} to {DAYS[-1]}.")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
