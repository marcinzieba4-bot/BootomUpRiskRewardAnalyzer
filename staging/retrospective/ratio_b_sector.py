#!/usr/bin/env python3
"""
HINDSIGHT: the Ratio B long book with every position hedged by its own sector ETF, on the full eleven (with tech) and on
the seven without tech. Prints the tables quoted in staging/retrospective/RATIO_B_SECTOR.md.

THE RULES, fixed in this docstring before the first run; every variant below is printed.
- Sectors (GICS, the same for these eleven over 2008-2026), each with its Select Sector SPDR:
  AAPL, MSFT, AVGO, ACN -> XLK; XOM -> XLE; PEP, WMT -> XLP; LOW, NKE -> XLY; UNP -> XLI; SHW -> XLB.
- Universes: ALL (the eleven) and NON-TECH (without AAPL, MSFT, AVGO, ACN: UNP, LOW, NKE, PEP, SHW, WMT, XOM).
- Long book: each month the three lowest point-in-time Ratio B in the universe, equal weight at entry, held to the next
  entry (RANK3's long leg in ratio_b_basket.py).
- Hedge modes. Each hedge is short the position's sector ETF, sized to the position's value each day:
  TACTICAL (main)  100% of the position while its sector ETF closes below the ETF's own 100-day average;
  TACTICAL 50%     the same at half size;
  SPX TIMING       100% of the position while the S&P 500 is below its 100-day average (ratio_b_hedge.py's timing);
  ALWAYS           100% of the position every day: a pure stock-against-its-sector bet;
  and for reference: UNHEDGED, and the whole book hedged with SPY on the S&P 500 timing (ratio_b_hedge.py).
  Every signal is read at a close and traded at the next trading day's close. The shorts pay the ETFs' dividends.
  No interest on cash, borrow fees or taxes.
- Also: every SPY drawdown of 15% or more; calendar years; 200 runs of three random tickers a month from the same
  universe with the same hedges (seeded); a 0.10% charge on every dollar traded (long-book rebalances and every change
  in hedge size); the current positions.

Everything printed is a label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule"). Reads only; the first run needs the network (retro/.cache/, gitignored).

    python3 staging/retrospective/ratio_b_sector.py                # every table
    python3 staging/retrospective/ratio_b_sector.py summary years  # selected sections

Sections: summary episodes years random costs overlap now
(overlap was added after the first run.)
"""
import bisect
import math
import os
import random
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ratio_b_nontech as N  # noqa: E402  (daily ETF returns, 100-day flags, the S&P 500 timing, the calendar)

R, H, B = N.R, N.H, N.B
DAYS, MONTHS = N.DAYS, N.MONTHS
ENTRIES = [B.ENTRY[m] for m in MONTHS]
SECTOR = {"AAPL": "XLK", "MSFT": "XLK", "AVGO": "XLK", "ACN": "XLK", "XOM": "XLE", "PEP": "XLP", "WMT": "XLP",
          "LOW": "XLY", "NKE": "XLY", "UNP": "XLI", "SHW": "XLB"}
ETFS = sorted(set(SECTOR.values()))
EDAILY = {e: N.daily(e) for e in ETFS}
EFLAG = {e: N.flags_for(e) for e in ETFS}
SPX = N.FLAG["SPY"]
SPY = N.ETF["SPY"]
UNIVERSES = (("ALL eleven (with tech)", B.TICKERS), ("NON-TECH seven", N.NONTECH))
MODES = ("UNHEDGED", "TACTICAL", "TACTICAL 50%", "SPX TIMING", "ALWAYS", "SPY HEDGE (reference)")


DAY_POS = {d: j for j, d in enumerate(DAYS)}
LEVEL = {t: [B.level(t, d) for d in DAYS] for t in B.TICKERS}       # each ticker's total-return index on the calendar


def simulate(names, cost=0.0, modes=MODES):
    """Daily returns for every mode, plus the average hedge size (share of the book) for each."""
    out = {k: [0.0] for k in modes}
    size = {k: [] for k in modes}
    prev_h = {k: {} for k in modes}
    for j in range(1, len(DAYS)):
        m = MONTHS[bisect.bisect_right(ENTRIES, DAYS[j - 1]) - 1]
        e = DAY_POS[B.ENTRY[m]]
        v = {t: LEVEL[t][j - 1] / LEVEL[t][e] for t in names[m]}
        tot = sum(v.values())
        w = {t: v[t] / tot for t in v}
        long = sum(w[t] * (LEVEL[t][j] / LEVEL[t][j - 1] - 1) for t in w)
        for k in modes:
            hs = {}                                             # hedge notional per instrument, share of the book
            if k == "SPY HEDGE (reference)":
                if SPX[j]:
                    hs["SPY"] = 1.0
            elif k != "UNHEDGED":
                for t in w:
                    sct = SECTOR[t]
                    on = 1 if k == "ALWAYS" else SPX[j] if k == "SPX TIMING" else EFLAG[sct][j]
                    if on:
                        hs[sct] = hs.get(sct, 0.0) + w[t] * (0.5 if k == "TACTICAL 50%" else 1.0)
            hed = sum(n * (SPY[j] if x == "SPY" else EDAILY[x][j]) for x, n in hs.items())
            c = cost * sum(abs(hs.get(x, 0) - prev_h[k].get(x, 0)) for x in set(hs) | set(prev_h[k])) if cost else 0.0
            out[k].append(long - hed - c)
            size[k].append(sum(hs.values()))
            prev_h[k] = hs
    return out, {k: statistics.fmean(v) for k, v in size.items()}


def charge_rebalances(rets, names, cost):
    """Charge the long book's monthly rebalance (from drifted to new equal weights) on the first day it is held."""
    out, prev = list(rets), None
    for i, m in enumerate(MONTHS):
        new = {t: 1 / 3 for t in names[m]}
        if prev is None:
            tr = 1.0
        else:
            pm = MONTHS[i - 1]
            g = {t: B.level(t, B.ENTRY[m]) / B.level(t, B.ENTRY[pm]) for t in prev}
            s = sum(prev[t] * g[t] for t in prev)
            drift = {t: prev[t] * g[t] / s for t in prev}
            tr = sum(abs(new.get(t, 0) - drift.get(t, 0)) for t in set(new) | set(drift))
        j = bisect.bisect_right(DAYS, B.ENTRY[m])
        if j < len(out):
            out[j] -= cost * tr
        prev = new
    return out


def stats(r):
    xs = r[1:]
    mu, sd = statistics.fmean(xs), statistics.pstdev(xs)
    s = SPY[1:]
    ms = statistics.fmean(s)
    beta = sum((a - mu) * (b - ms) for a, b in zip(xs, s)) / sum((b - ms) ** 2 for b in s)
    c, dd = R.cagr(r), R.mdd(r)
    return {"cagr": c, "vol": sd * math.sqrt(252), "sharpe": mu / sd * math.sqrt(252), "mdd": dd, "calmar": c / -dd, "beta": beta}


def pct(v):
    return f"{v * 100:+.1f}%"


RUNS = {}
for label, u in UNIVERSES:
    names = R.ratio_b_names(u)
    RUNS[label] = (names,) + simulate(names)


def section_summary():
    for label, u in UNIVERSES:
        names, out, size = RUNS[label]
        eq = R.book(R.all_names(u))
        print(f"\n### {label}: {', '.join(u)} ({DAYS[0]} to {DAYS[-1]})\n")
        print("| Strategy | Annual return | Volatility | Sharpe | Worst drawdown | Return / drawdown | Beta to SPY | Average hedge (share of book) |")
        print("|---|---|---|---|---|---|---|---|")
        for name, r, hs in (("SPY bought and held", SPY, None), ("Equal weight of the universe, unhedged", eq, None)):
            st = stats(r)
            print(f"| {name} | {pct(st['cagr'])} | {st['vol'] * 100:.1f}% | {st['sharpe']:.2f} | {st['mdd'] * 100:.0f}% | {st['calmar']:.2f} | {st['beta']:+.2f} | - |")
        for k in MODES:
            st = stats(out[k])
            bold = "**" if k == "TACTICAL" else ""
            print(f"| {bold}Ratio B book, {k}{bold} | {bold}{pct(st['cagr'])}{bold} | {st['vol'] * 100:.1f}% | {st['sharpe']:.2f} | "
                  f"{st['mdd'] * 100:.0f}% | {st['calmar']:.2f} | {st['beta']:+.2f} | {size[k] * 100:.0f}% |")


def section_episodes():
    for label, _ in UNIVERSES:
        out = RUNS[label][1]
        print(f"\n### Every SPY drawdown of 15% or more, peak to trough: {label}\n")
        cols = ("UNHEDGED", "TACTICAL", "SPX TIMING", "ALWAYS", "SPY HEDGE (reference)")
        print("| SPY peak - trough | SPY | " + " | ".join(cols) + " |\n|---|---|" + "---|" * len(cols))
        for a, b in H.episodes():
            print(f"| {a} - {b} | {pct(H.window(SPY, a, b))} | " + " | ".join(pct(H.window(out[k], a, b)) for k in cols) + " |")


def section_years():
    yrs = sorted({d[:4] for d in DAYS[1:]})
    yearly = lambda r, y: math.prod(1 + x for d, x in zip(DAYS[1:], r[1:]) if d[:4] == y) - 1
    for label, _ in UNIVERSES:
        out = RUNS[label][1]
        cols = ("UNHEDGED", "TACTICAL", "SPX TIMING", "ALWAYS", "SPY HEDGE (reference)")
        print(f"\n### Calendar years: {label}\n")
        print("| Year | SPY | " + " | ".join(cols) + " |\n|---|---|" + "---|" * len(cols))
        for y in yrs:
            print(f"| {y} | {pct(yearly(SPY, y))} | " + " | ".join(pct(yearly(out[k], y)) for k in cols) + " |")
        print("| years positive | " + f"{sum(yearly(SPY, y) > 0 for y in yrs)} of {len(yrs)} | " +
              " | ".join(f"{sum(yearly(out[k], y) > 0 for y in yrs)} of {len(yrs)}" for k in cols) + " |")


def section_random(runs=200):
    rng = random.Random(20261108)
    for label, u in UNIVERSES:
        res = {k: [] for k in ("UNHEDGED", "TACTICAL", "ALWAYS")}
        for _ in range(runs):
            names = {m: rng.sample(sorted(t for t in B.FIRST[m] if t in u), 3) for m in MONTHS}
            out, _ = simulate(names, modes=tuple(res))
            for k in res:
                res[k].append(R.cagr(out[k]))
        print(f"\n### Three random tickers a month from {label} ({runs} runs), same sector hedges\n")
        print("| Mode | Random 5th pct | Random median | Random 95th pct | Ratio B book | Runs at or above the book |\n|---|---|---|---|---|---|")
        for k, s in res.items():
            s = sorted(s)
            q = lambda p: s[min(len(s) - 1, int(p * len(s)))]
            rb = R.cagr(RUNS[label][1][k])
            print(f"| {k} | {pct(q(0.05))} | {pct(q(0.5))} | {pct(q(0.95))} | **{pct(rb)}** | {sum(x >= rb for x in s)} of {runs} |")


def section_costs(c=0.001):
    print(f"\n### After a {c * 100:.2f}% charge on every dollar traded (rebalances and every change in hedge size)\n")
    print("| Universe | " + " | ".join(MODES) + " |\n|---|" + "---|" * len(MODES))
    for label, _ in UNIVERSES:
        names = RUNS[label][0]
        out, _ = simulate(names, cost=c)
        cells = []
        for k in MODES:
            r = charge_rebalances(out[k], names, c)
            cells.append(f"{pct(R.cagr(r))} / {R.mdd(r) * 100:.0f}%")
        print(f"| {label} | " + " | ".join(cells) + " |")


def section_overlap():
    """Added after the first run: is a Ratio B pick's sector ETF already below its 100-day average when the pick is bought?"""
    print("\n### At entry, is the pick's own sector ETF below its 100-day average? (added after the first run)\n")
    print("| Universe | Ratio B picks with the sector hedge on at entry | All universe stocks, same months | Next month: sector ETF return when on / off |")
    print("|---|---|---|---|")
    for label, u in UNIVERSES:
        names = RUNS[label][0]
        pick_on, all_on, n_pick, n_all, nxt_on, nxt_off = 0, 0, 0, 0, [], []
        for i, m in enumerate(MONTHS[:-1]):
            j = DAY_POS[B.ENTRY[m]] + 1                       # the first day the new book is held
            if j >= len(DAYS):
                continue
            k = DAY_POS[B.ENTRY[MONTHS[i + 1]]]
            for t in B.FIRST[m]:
                if t not in u:
                    continue
                on = EFLAG[SECTOR[t]][j]
                n_all += 1
                all_on += on
                if t in names[m]:
                    n_pick += 1
                    pick_on += on
                    g = math.prod(1 + x for x in EDAILY[SECTOR[t]][j:k + 1]) - 1
                    (nxt_on if on else nxt_off).append(g)
        print(f"| {label} | {100 * pick_on / n_pick:.0f}% of {n_pick} | {100 * all_on / n_all:.0f}% of {n_all} | "
              f"{pct(statistics.fmean(nxt_on))} / {pct(statistics.fmean(nxt_off))} |")


def section_now():
    print("\n### Now (each sector ETF against its own 100-day average on the last close)\n")
    status = {}
    for e in ETFS:
        closes, _ = B.rt.fetch_prices(e)
        ks = sorted(closes)
        ma = statistics.fmean(closes[k] for k in ks[-100:])
        status[e] = (closes[ks[-1]], ma, ks[-1])
    for label, _ in UNIVERSES:
        names = RUNS[label][0][MONTHS[-1]]
        print(f"- {label}: long book since {B.ENTRY[MONTHS[-1]]}: " + "; ".join(
            f"{t} -> {SECTOR[t]} ({(status[SECTOR[t]][0] / status[SECTOR[t]][1] - 1) * 100:+.1f}% vs its 100-day, "
            f"hedge {'ON' if status[SECTOR[t]][0] < status[SECTOR[t]][1] else 'off'})" for t in names))
    print("\nAll sector ETFs: " + ", ".join(f"{e} {(c / m - 1) * 100:+.1f}%" for e, (c, m, _) in status.items()) + f" (close {status[ETFS[0]][2]}).")


SECTIONS = {"summary": section_summary, "episodes": section_episodes, "years": section_years, "random": section_random,
            "costs": section_costs, "overlap": section_overlap,
            "now": section_now}

if __name__ == "__main__":
    print(f"HINDSIGHT. Ratio B book hedged with sector ETFs, daily {DAYS[0]} to {DAYS[-1]}.")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
