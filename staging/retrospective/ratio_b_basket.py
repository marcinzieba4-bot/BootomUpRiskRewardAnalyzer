#!/usr/bin/env python3
"""
HINDSIGHT: long/short baskets built on Ratio B across the eleven retrospective series, 2008-2026. Prints the tables
quoted in staging/retrospective/RATIO_B_BASKET.md.

THE RULES, fixed in this docstring before the first run; every basket and holding period is printed.
- Signal: each ticker's Ratio B on its first as-of date of each calendar month (the frozen engine's point-in-time
  reading: downside to BEAR / upside to BULL; negative below BEAR, inf at or above BULL). A ticker joins the universe at
  its first as-of date (AVGO in August 2009).
- Baskets, equal weight within each leg:
  TIER   long Ratio B < 0.75 (the engine's BUY tier, below-BEAR included), short Ratio B >= 1.75 (AVOID, above-BULL included);
  BULL   long Ratio B < 0.75, short only the tickers at or above their BULL price (Ratio B inf);
  RANK3  long the three lowest Ratio B, short the three highest. Tickers above BULL all read inf, so among them the one
         furthest above its BULL price ranks highest (the upside term of Ratio B); remaining ties go by ticker name.
- Formation on the month's latest first-of-month as-of date, entry at the next trading day's close (so no position uses
  the close its signal was read on). Dividends reinvested (Yahoo, through retro_tool.fetch_prices); no costs, borrow
  fees or financing. The spread is the long leg's return minus the short leg's (100% long, 100% short).
- Holding: rebalanced every month (1m), and overlapping cohorts held 24, 36 and 48 months. Each month a new cohort is
  formed and the portfolio is the equal average of the live cohorts, in the manner of Jegadeesh-Titman. A month in which
  a leg is empty holds nothing in that cohort (spread 0).
  [Changed after the first run: in a month a leg is empty, that leg's own return is the EQUAL basket's, so that "long
  minus EQUAL" and "EQUAL minus short" are 0 then. The first run booked 0% to both legs, which distorted those two
  lines for TIER and BULL. The spread itself is unchanged.]
- Stats: annual return, volatility and Sharpe (no risk-free rate; the spread is self-financing), worst drawdown, share
  of positive months, a Newey-West t-stat (12 lags) on the mean monthly spread, beta and correlation to SPY, average
  names per leg, empty-leg months. Then calendar years, four sub-periods, each ticker left out in turn, and every cohort's
  own 2-, 3- and 4-year result.

Everything printed is a label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule"). The first run needs the network (retro/.cache/, gitignored).

    python3 staging/retrospective/ratio_b_basket.py               # every table
    python3 staging/retrospective/ratio_b_basket.py summary years # selected sections

Sections: summary legs years periods loo cohorts sens age members
(sens, age, turnover and the "long minus SPY" line were added after the first run, as checks; they are labelled where printed.)
Medians of an even count take the upper middle value (statistics.median_high).
"""
import bisect
import json
import math
import os
import statistics
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "retro"))
sys.path.insert(0, HERE)
import retro_tool as rt  # noqa: E402
import cross_ticker_oos as X  # noqa: E402  (point-in-time rows; prints nothing on import)

med = statistics.median_high
TICKERS = X.ALL
HOLDS = (1, 24, 36, 48)
BASKETS = ("TIER", "BULL", "RANK3")             # the three fixed before the first run; RANK2/RANK4 only in sens


def tr_index(symbol):
    """Sorted trading days and a total-return index, dividends reinvested on the ex-date (or the next trading day)."""
    closes, divs = rt.fetch_prices(symbol)
    days = sorted(closes)
    cash = defaultdict(float)
    for d, a in divs:
        i = bisect.bisect_left(days, d)
        if i < len(days):
            cash[days[i]] += a
    idx, out = 1.0, []
    for i, d in enumerate(days):
        if i:
            idx *= (closes[d] + cash.get(d, 0.0)) / closes[days[i - 1]]
        out.append(idx)
    return days, out


IDX = {s: tr_index(s) for s in TICKERS + ("SPY",)}
LAST = min(IDX[s][0][-1] for s in IDX)
DAYS = IDX["SPY"][0]


def level(symbol, date):
    days, v = IDX[symbol]
    return v[bisect.bisect_right(days, date) - 1]


# point-in-time Ratio B and the BULL upside on each ticker's first as-of date of the month
FIRST = defaultdict(dict)
for r in sorted(X.R, key=lambda r: r["as_of"]):
    if r["ticker"] not in FIRST[r["as_of"][:7]]:
        a = json.load(open(os.path.join(X.ROOT, X.SERIES[r["ticker"]], r["as_of"], "analysis.json")))
        FIRST[r["as_of"][:7]][r["ticker"]] = {"ticker": r["ticker"], "as_of": r["as_of"], "rb": a["metrics"]["ratio_b"],
                                              "up": a["metrics"]["scenarios"]["BULL"]["price"] / a["price"] - 1}
MONTHS = sorted(m for m in FIRST if m <= "2026-10")
ENTRY = {}
for m in MONTHS:
    formed = max(s["as_of"] for s in FIRST[m].values())
    ENTRY[m] = DAYS[bisect.bisect_right(DAYS, formed)]          # the next trading day after formation
ENDS = [ENTRY[m] for m in MONTHS[1:]] + [LAST]                  # month m runs from ENTRY[m] to the next entry
RET = {m: {s: level(s, e) / level(s, ENTRY[m]) - 1 for s in TICKERS + ("SPY",) if s == "SPY" or s in FIRST[m]}
       for m, e in zip(MONTHS, ENDS)}


def rank_key(s):
    """Lower = more attractive by Ratio B. Above BULL (inf): the further above BULL (more negative upside), the higher."""
    return (1, -s["up"], s["ticker"]) if math.isinf(s["rb"]) else (0, s["rb"], s["ticker"])


def legs(basket, sigs):
    if basket == "TIER":
        return [s["ticker"] for s in sigs if s["rb"] < 0.75], [s["ticker"] for s in sigs if s["rb"] >= 1.75]
    if basket == "BULL":
        return [s["ticker"] for s in sigs if s["rb"] < 0.75], [s["ticker"] for s in sigs if math.isinf(s["rb"])]
    n = int(basket[4:])                                          # RANK2 / RANK3 / RANK4
    order = sorted(sigs, key=rank_key)
    return [s["ticker"] for s in order[:n]], [s["ticker"] for s in order[-n:]]


def run(basket, hold, universe=TICKERS, months=None):
    """Monthly series of (long, short, spread, SPY) for the overlapping-cohort portfolio, plus each cohort's legs."""
    months = months or MONTHS
    cohorts = {}
    for m in months:
        sigs = [s for t, s in FIRST[m].items() if t in universe]
        cohorts[m] = legs(basket, sigs)
    out, empty, nl, ns, turn = [], 0, [], [], []
    for j, m in enumerate(months):
        live = months[max(0, j - hold + 1): j + 1]
        lr, sr, sp = [], [], []
        eq = statistics.fmean(v for t, v in RET[m].items() if t != "SPY" and t in universe)
        for c in live:
            lg, sh = cohorts[c]
            a = statistics.fmean(RET[m][t] for t in lg) if lg else eq
            b = statistics.fmean(RET[m][t] for t in sh) if sh else eq
            lr.append(a); sr.append(b); sp.append(a - b if lg and sh else 0.0)
        lg, sh = cohorts[m]
        empty += not lg or not sh
        nl.append(len(lg)); ns.append(len(sh))
        if j:                                                    # share of each leg's names that are new this month
            pl, ps = cohorts[months[j - 1]]
            turn += [len(set(x) - set(y)) / len(x) for x, y in ((lg, pl), (sh, ps)) if x]
        out.append((m, statistics.fmean(lr), statistics.fmean(sr), statistics.fmean(sp), RET[m]["SPY"]))
    return out, cohorts, {"empty": empty, "long_n": statistics.fmean(nl), "short_n": statistics.fmean(ns),
                          "turnover": statistics.fmean(turn)}


def stats(xs):
    n = len(xs)
    growth = math.prod(1 + x for x in xs)
    cagr = growth ** (12 / n) - 1
    mu, sd = statistics.fmean(xs), statistics.pstdev(xs)
    peak, mdd, v = 1.0, 0.0, 1.0
    for x in xs:
        v *= 1 + x
        peak = max(peak, v)
        mdd = min(mdd, v / peak - 1)
    lag = 12                                                     # Newey-West on the mean
    dev = [x - mu for x in xs]
    s = sum(d * d for d in dev) / n
    for k in range(1, lag + 1):
        s += 2 * (1 - k / (lag + 1)) * sum(dev[i] * dev[i - k] for i in range(k, n)) / n
    t = mu / math.sqrt(s / n) if s > 0 else 0.0
    return {"cagr": cagr, "vol": sd * math.sqrt(12), "sharpe": mu / sd * math.sqrt(12) if sd else 0.0, "mdd": mdd,
            "pos": sum(x > 0 for x in xs) / n, "t": t, "best": max(xs), "worst": min(xs), "total": growth - 1}


def beta(xs, ys):
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    vy = sum((y - my) ** 2 for y in ys)
    vx = sum((x - mx) ** 2 for x in xs)
    return cov / vy, cov / math.sqrt(vx * vy)


def f1(v):
    return f"{v * 100:+.1f}%"


def section_summary():
    print(f"\n### The long/short spread, {MONTHS[0]} to {MONTHS[-1]} ({len(MONTHS)} months, last return to {LAST})\n")
    print("| Basket | Hold | Annual return | Volatility | Sharpe | Worst drawdown | Positive months | t-stat (NW) | "
          "Beta to SPY | Corr. to SPY | Total | Names long / short | Empty-leg months | New names a month (added later) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for b in BASKETS:
        for h in HOLDS:
            o, _, info = run(b, h)
            sp, spy = [x[3] for x in o], [x[4] for x in o]
            st = stats(sp)
            be, co = beta(sp, spy)
            print(f"| {b} | {h}m | {f1(st['cagr'])} | {st['vol'] * 100:.1f}% | {st['sharpe']:+.2f} | {st['mdd'] * 100:.0f}% | "
                  f"{st['pos'] * 100:.0f}% | {st['t']:+.2f} | {be:+.2f} | {co:+.2f} | {f1(st['total'])} | "
                  f"{info['long_n']:.1f} / {info['short_n']:.1f} | {info['empty']} | {info['turnover'] * 100:.0f}% |")


def section_legs():
    print("\n### Each leg on its own, against SPY and an equal-weight basket of all eleven (rebalanced monthly)\n")
    print("| Series | Annual return | Volatility | Sharpe | Worst drawdown | Beta to SPY |\n|---|---|---|---|---|---|")
    spy = [RET[m]["SPY"] for m in MONTHS]
    eq = [statistics.fmean(v for t, v in RET[m].items() if t != "SPY") for m in MONTHS]
    rows = [("SPY", spy), ("EQUAL (all eleven)", eq)]
    for b in BASKETS:
        for h in (1, 24):
            o, _, _ = run(b, h)
            rows += [(f"{b} {h}m long leg", [x[1] for x in o]), (f"{b} {h}m short leg", [x[2] for x in o]),
                     (f"{b} {h}m long minus SPY (added later)", [x[1] - x[4] for x in o]),
                     (f"{b} {h}m long minus EQUAL", [x[1] - e for x, e in zip(o, eq)]),
                     (f"{b} {h}m EQUAL minus short", [e - x[2] for x, e in zip(o, eq)])]
    for name, xs in rows:
        st = stats(xs)
        print(f"| {name} | {f1(st['cagr'])} | {st['vol'] * 100:.1f}% | {st['sharpe']:+.2f} | {st['mdd'] * 100:.0f}% | {beta(xs, spy)[0]:+.2f} |")


def section_years():
    print("\n### Calendar-year spread (long minus short, compounded within the year)\n")
    cols = [(b, h) for b in BASKETS for h in (1, 24)]
    series = {c: run(*c)[0] for c in cols}
    print("| Year | " + " | ".join(f"{b} {h}m" for b, h in cols) + " | SPY |\n|---|" + "---|" * (len(cols) + 1))
    for y in sorted({m[:4] for m in MONTHS}):
        cells = [f1(math.prod(1 + x[3] for x in series[c] if x[0][:4] == y) - 1) for c in cols]
        spy = math.prod(1 + RET[m]["SPY"] for m in MONTHS if m[:4] == y) - 1
        print(f"| {y} | " + " | ".join(cells) + f" | {f1(spy)} |")
    print("| positive years | " + " | ".join(
        f"{sum(math.prod(1 + x[3] for x in series[c] if x[0][:4] == y) > 1 for y in {m[:4] for m in MONTHS})} of {len({m[:4] for m in MONTHS})}"
        for c in cols) + " | |")


PERIODS = (("2008-2012", "2008-01", "2012-12"), ("2013-2017", "2013-01", "2017-12"), ("2018-2022", "2018-01", "2022-12"),
           ("2023-2026", "2023-01", "2026-12"))


def section_periods():
    print("\n### Sub-periods (annual spread return / Sharpe; the full-period run cut into pieces)\n")
    print("| Basket | Hold | " + " | ".join(p for p, _, _ in PERIODS) + " |\n|---|---|" + "---|" * len(PERIODS))
    for b in BASKETS:
        for h in HOLDS:
            o, _, _ = run(b, h)
            cells = []
            for _, a, z in PERIODS:
                st = stats([x[3] for x in o if a <= x[0] <= z])
                cells.append(f"{f1(st['cagr'])} / {st['sharpe']:+.2f}")
            print(f"| {b} | {h}m | " + " | ".join(cells) + " |")


def section_loo():
    print("\n### Each ticker left out in turn (annual spread return over the full period)\n")
    print("| Basket | Hold | All | " + " | ".join(f"no {t}" for t in TICKERS) + " | Positive |\n|---|---|---|" + "---|" * (len(TICKERS) + 1))
    for b in BASKETS:
        for h in (1, 24):
            full = stats([x[3] for x in run(b, h)[0]])["cagr"]
            v = [stats([x[3] for x in run(b, h, tuple(u for u in TICKERS if u != t))[0]])["cagr"] for t in TICKERS]
            print(f"| {b} | {h}m | {f1(full)} | " + " | ".join(f1(x) for x in v) + f" | {sum(x > 0 for x in v)} of {len(v)} |")


def section_cohorts():
    print("\n### Every monthly cohort held to its end: 2, 3 and 4 years (long and short legs compounded on their own)\n")
    print("| Basket | Hold | Cohorts | Median long | Median short | Median spread | Long beat short | Worst spread | Best spread | "
          "Long beat SPY |\n|---|---|---|---|---|---|---|---|---|---|")
    for b in BASKETS:
        _, cohorts, _ = run(b, 1)
        for h in (24, 36, 48):
            res = []
            for i, m in enumerate(MONTHS):
                if i + h > len(MONTHS) - 1:                      # the cohort's last month must be complete
                    break
                lg, sh = cohorts[m]
                if not lg or not sh:
                    continue
                span = MONTHS[i:i + h]
                L = math.prod(1 + statistics.fmean(RET[k][t] for t in lg) for k in span) - 1
                S = math.prod(1 + statistics.fmean(RET[k][t] for t in sh) for k in span) - 1
                P = math.prod(1 + RET[k]["SPY"] for k in span) - 1
                res.append((L, S, P))
            print(f"| {b} | {h}m | {len(res)} | {f1(med([x[0] for x in res]))} | {f1(med([x[1] for x in res]))} | "
                  f"{f1(med([x[0] - x[1] for x in res]))} | {100 * sum(x[0] > x[1] for x in res) / len(res):.0f}% | "
                  f"{f1(min(x[0] - x[1] for x in res))} | {f1(max(x[0] - x[1] for x in res))} | {100 * sum(x[0] > x[2] for x in res) / len(res):.0f}% |")


def section_sens():
    """Added after the first run: is RANK3 a knife-edge on the number of names?"""
    print("\n### Sensitivity (added after the first run): two or four names a side instead of three\n")
    print("| Basket | Hold | Annual return | Sharpe | Worst drawdown | t-stat (NW) | Positive years | Leave-one-out positive |")
    print("|---|---|---|---|---|---|---|---|")
    for b in ("RANK2", "RANK3", "RANK4"):
        for h in (1, 24, 36):
            o, _, _ = run(b, h)
            st = stats([x[3] for x in o])
            yrs = sorted({m[:4] for m in MONTHS})
            py = sum(math.prod(1 + x[3] for x in o if x[0][:4] == y) > 1 for y in yrs)
            loo = sum(stats([x[3] for x in run(b, h, tuple(u for u in TICKERS if u != t))[0]])["cagr"] > 0 for t in TICKERS)
            print(f"| {b} | {h}m | {f1(st['cagr'])} | {st['sharpe']:+.2f} | {st['mdd'] * 100:.0f}% | {st['t']:+.2f} | {py} of {len(yrs)} | {loo} of {len(TICKERS)} |")


def section_age():
    """Added after the first run: in which months of a cohort's life does the spread come?"""
    print("\n### Spread by the cohort's age (added after the first run): mean monthly spread, annualised, and the share positive\n")
    ages = ((1, 1), (2, 3), (4, 6), (7, 12), (13, 24), (25, 36), (37, 48))
    print("| Basket | " + " | ".join(f"month {a}" if a == b else f"months {a}-{b}" for a, b in ages) + " |\n|---|" + "---|" * len(ages))
    for bname in BASKETS:
        _, cohorts, _ = run(bname, 1)
        by = defaultdict(list)
        for i, m in enumerate(MONTHS):
            lg, sh = cohorts[m]
            if not lg or not sh:
                continue
            for k in range(48):
                if i + k >= len(MONTHS):
                    break
                mk = MONTHS[i + k]
                by[k + 1].append(statistics.fmean(RET[mk][t] for t in lg) - statistics.fmean(RET[mk][t] for t in sh))
        cells = []
        for a, b in ages:
            v = [x for k in range(a, b + 1) for x in by[k]]
            cells.append(f"{statistics.fmean(v) * 1200:+.1f}%/yr ({100 * sum(x > 0 for x in v) / len(v):.0f}%)")
        print(f"| {bname} | " + " | ".join(cells) + " |")


def section_members():
    print("\n### Who sat in each leg (share of months), and the newest basket\n")
    for b in BASKETS:
        _, cohorts, _ = run(b, 1)
        cl, cs = Counter(), Counter()
        for m in MONTHS:
            cl.update(cohorts[m][0]); cs.update(cohorts[m][1])
        print(f"- {b} long: " + ", ".join(f"{t} {100 * n / len(MONTHS):.0f}%" for t, n in cl.most_common(6)))
        print(f"- {b} short: " + ", ".join(f"{t} {100 * n / len(MONTHS):.0f}%" for t, n in cs.most_common(6)))
    sigs = []
    for t in TICKERS:                                            # each ticker's latest as-of date
        d = max(r["as_of"] for r in X.R if r["ticker"] == t)
        a = json.load(open(os.path.join(X.ROOT, X.SERIES[t], d, "analysis.json")))
        sigs.append({"ticker": t, "as_of": d, "rb": a["metrics"]["ratio_b"], "up": a["metrics"]["scenarios"]["BULL"]["price"] / a["price"] - 1})
    fmt = lambda v: "inf" if math.isinf(v) else f"{v:.2f}"
    print(f"\nNewest readings ({min(s['as_of'] for s in sigs)} to {max(s['as_of'] for s in sigs)}), lowest Ratio B first: " + ", ".join(
        f"{s['ticker']} {fmt(s['rb'])}" for s in sorted(sigs, key=rank_key)))
    for b in BASKETS:
        lg, sh = legs(b, sigs)
        print(f"- {b}: long {', '.join(lg) or '-'}; short {', '.join(sh) or '-'}")


SECTIONS = {"summary": section_summary, "legs": section_legs, "years": section_years, "periods": section_periods,
            "loo": section_loo, "cohorts": section_cohorts, "sens": section_sens, "age": section_age,
            "members": section_members}

if __name__ == "__main__":
    print(f"HINDSIGHT. {len(TICKERS)} tickers, {len(MONTHS)} monthly formations {MONTHS[0]} to {MONTHS[-1]}; prices to {LAST}.")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
