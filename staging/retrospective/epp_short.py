#!/usr/bin/env python3
"""
HINDSIGHT: is a small and shrinking EPP gap the mark of a structural loser? Test shorting those stocks against a long
S&P 500 position. Prints the tables quoted in staging/retrospective/EPP_SHORT.md.

THE RULES, fixed in this docstring before the first run; every variant below is printed.
- Readings: each weekly date's point-in-time EPP gap (analysis.json). Its change is measured against the same ticker's
  date 13, 26 or 52 weeks earlier, within 6 days. The 12-month price change comes from cross_ticker_oos.py, both public
  at the as-of date.
- Signals:
  - MAIN: EPP gap <= 40% (the engine's band edge) and lower than 26 weeks earlier.
  - Variants:
    - gap <= 0% (below the floor);
    - 13-week and 52-week look-backs;
    - a shrink of 20 points or more;
    - MAIN plus a 12-month price fall (shrinking because the price fell, not because EPS grew).
- The trade: short the stock and buy the same amount of SPY, from the close after the as-of date. Its return is SPY's
  total return minus the stock's (the short pays the dividends). Measured at 1, 3, 6, 12 and 24 months.
- The basket: each month, on each ticker's first as-of date of the month, short every ticker that signals, in equal
  weight, against 100% SPY, entered at the next trading day's close. Rebalanced monthly (1m), and overlapping cohorts
  held 6 and 12 months (as in ratio_b_basket.py). A month with no signal holds nothing. No costs, borrow fees or interest.
- Also: with and without tech (AAPL, MSFT, AVGO, ACN), per ticker, calendar years, and the newest signals.

SECOND TEST, the falling-EPS filter (added on request after the first run; its rules were fixed here before it ran):
- E1, last year down: the last fiscal year in the date's EPS_NORM history is below the year before it (the previous
  year present).
- E2, EPS down over 6 months: the date's EPP_TODAY_EPS (the EPS its floor uses: the year's guide, or the last full year)
  is lower than the same ticker's value 26 weeks earlier. The earlier value is moved to today's share basis through the
  splits in retro/facts. Dates with an EPS of zero or below 26 weeks earlier are left out.
- E3: E1 and E2 together.
- Signals:
  - each filter alone;
  - MAIN with each filter;
  - "below the floor and shrinking" with E1 and with E2;
  - MAIN with E2 and the price down over 12 months.
- The same pair horizons, basket rules, per-ticker table and newest signals as above.
Sections: eps_signals eps_pairs eps_per eps_book eps_years eps_now.

Survivorship cuts against this test: the eleven are 2026's survivors, and the companies that kept falling, which a
short would profit from most, are not in the sample.

Everything printed is a label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule"). Reads only; the first run needs the network (retro/.cache/, gitignored).

    python3 staging/retrospective/epp_short.py                 # every table
    python3 staging/retrospective/epp_short.py signals book    # selected sections

Sections: signals pairs per book years now (first test); eps_signals eps_pairs eps_per eps_book eps_years eps_now;
eps_post (post-hoc, chosen after reading eps_pairs)
"""
import ast
import bisect
import datetime as dt
import json
import math
import os
import re
import statistics
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ratio_b_basket as B  # noqa: E402  (total-return indices, monthly first dates and entries)

X = B.X
TECH = ("AAPL", "MSFT", "AVGO", "ACN")
NONTECH = tuple(t for t in X.ALL if t not in TECH)
HORIZONS = (("1m", 21), ("3m", 63), ("6m", 126), ("12m", 252), ("24m", 504))
DAYS = B.DAYS
med = statistics.median_high

for r in X.R:
    r["gap"] = json.load(open(os.path.join(X.ROOT, X.SERIES[r["ticker"]], r["as_of"], "analysis.json")))["metrics"]["epp_gap_pct"]
for t in X.ALL:
    rs = [r for r in X.R if r["ticker"] == t]
    by = {r["date"]: r for r in rs}
    for r in rs:
        for w in (13, 26, 52):
            target = r["date"] - dt.timedelta(weeks=w)
            hit = next((by[target + dt.timedelta(days=k)] for k in sorted(range(-6, 7), key=abs) if target + dt.timedelta(days=k) in by), None)
            r[f"dgap{w}"] = r["gap"] - hit["gap"] if hit else None

EPS_NORM_RE = re.compile(r"^EPS_NORM\s*=\s*(\{[^}]*\})", re.M)
EPS_TODAY_RE = re.compile(r"^EPP_TODAY_EPS\s*=\s*(-?[0-9.]+)", re.M)
for r in X.R:
    src = open(os.path.join(X.ROOT, X.SERIES[r["ticker"]], r["as_of"], "model.py"), encoding="utf-8").read()
    hist = ast.literal_eval(EPS_NORM_RE.search(src).group(1))
    ys = sorted(hist)
    r["eps_last_down"] = len(ys) >= 2 and hist[ys[-1]] < hist[ys[-2]]
    r["eps_now"] = float(EPS_TODAY_RE.search(src).group(1))
for t in X.ALL:
    sp = X.splits(t)
    rs = [r for r in X.R if r["ticker"] == t]
    by = {r["date"]: r for r in rs}
    for r in rs:
        target = r["date"] - dt.timedelta(weeks=26)
        hit = next((by[target + dt.timedelta(days=k)] for k in sorted(range(-6, 7), key=abs) if target + dt.timedelta(days=k) in by), None)
        r["eps_down26"] = None
        if hit and hit["eps_now"] > 0:
            ratio = math.prod(x for e, x in sp if hit["date"] < e <= r["date"])
            r["eps_down26"] = r["eps_now"] < hit["eps_now"] / ratio

LAST = B.LAST
for r in X.R:
    i = bisect.bisect_right(DAYS, r["as_of"])                   # entry: the next trading day's close
    if i >= len(DAYS):
        continue
    r["entry"] = DAYS[i]
    for h, n in HORIZONS:
        if i + n < len(DAYS):
            d0, d1 = DAYS[i], DAYS[i + n]
            stock = B.level(r["ticker"], d1) / B.level(r["ticker"], d0) - 1
            spy = B.level("SPY", d1) / B.level("SPY", d0) - 1
            r[f"pair_{h}"] = spy - stock

SIGNALS = (
    ("**MAIN: gap <= 40%, lower than 26 weeks ago**", lambda r: r["gap"] <= 40 and r["dgap26"] is not None and r["dgap26"] < 0),
    ("gap <= 0%, lower than 26 weeks ago", lambda r: r["gap"] <= 0 and r["dgap26"] is not None and r["dgap26"] < 0),
    ("gap <= 40%, lower than 13 weeks ago", lambda r: r["gap"] <= 40 and r["dgap13"] is not None and r["dgap13"] < 0),
    ("gap <= 40%, lower than 52 weeks ago", lambda r: r["gap"] <= 40 and r["dgap52"] is not None and r["dgap52"] < 0),
    ("gap <= 40%, down 20+ points in 26 weeks", lambda r: r["gap"] <= 40 and r["dgap26"] is not None and r["dgap26"] <= -20),
    ("MAIN and the price down over 12 months", lambda r: r["gap"] <= 40 and r["dgap26"] is not None and r["dgap26"] < 0
     and r["chg_12m"] is not None and r["chg_12m"] < 0),
)
BASELINE = (("gap <= 40%, any change", lambda r: r["gap"] <= 40), ("gap > 40%", lambda r: r["gap"] > 40), ("every date", lambda r: True))


def pct(v):
    return "-" if v is None else f"{v * 100:+.1f}%"


def section_signals():
    print("\n### How often each signal fired (all eleven)\n")
    print("| Signal | Dates | Episodes | Tickers (dates) | Price down over 12 months |\n|---|---|---|---|---|")
    for name, f in SIGNALS:
        s = [r for r in X.R if f(r)]
        down = [r["chg_12m"] < 0 for r in s if r["chg_12m"] is not None]
        print(f"| {name} | {len(s)} | {X.episodes(s)} | {', '.join(f'{t} {n}' for t, n in Counter(r['ticker'] for r in s).most_common(5))} | "
              f"{100 * sum(down) / len(down):.0f}% |")


def pair_table(title, rows):
    print(f"\n### {title}: short the stock, long SPY (SPY's return minus the stock's; positive = the trade won)\n")
    print("| Signal | Dates (12m) | Episodes | " + " | ".join(f"{h}: median / won" for h, _ in HORIZONS) + " |\n|---|---|---|" + "---|" * len(HORIZONS))
    for name, f in SIGNALS + BASELINE:
        s = [r for r in rows if f(r)]
        s12 = [r for r in s if "pair_12m" in r]
        cells = []
        for h, _ in HORIZONS:
            v = [r[f"pair_{h}"] for r in s if f"pair_{h}" in r]
            cells.append(f"{pct(med(v))} / {100 * sum(x > 0 for x in v) / len(v):.0f}%" if v else "-")
        print(f"| {name} | {len(s12)} | {X.episodes(s12)} | " + " | ".join(cells) + " |")


def section_pairs():
    pair_table("All eleven", X.R)
    pair_table("Without tech", [r for r in X.R if r["ticker"] in NONTECH])


def section_per():
    f = SIGNALS[0][1]
    print("\n### Per ticker, MAIN signal: the pair over 12 months (median, share won) and the years it fired\n")
    print("| Ticker | Dates | 12m: median / won | 24m: median / won | Years (dates) |\n|---|---|---|---|---|")
    for t in X.ALL:
        s = [r for r in X.R if r["ticker"] == t and f(r)]
        c = []
        for h in ("12m", "24m"):
            v = [r[f"pair_{h}"] for r in s if f"pair_{h}" in r]
            c.append(f"{pct(med(v))} / {100 * sum(x > 0 for x in v) / len(v):.0f}%" if v else "-")
        print(f"| {t} | {len(s)} | {c[0]} | {c[1]} | {', '.join(f'{y} ({n})' for y, n in sorted(Counter(r['year'] for r in s).items()))} |")


# ── the monthly basket ───────────────────────────────────────────────────────
ROW = {(r["ticker"], r["as_of"]): r for r in X.R}
MONTHS = B.MONTHS
ENDS = [B.ENTRY[m] for m in MONTHS[1:]] + [LAST]
RET = {m: {s: B.level(s, e) / B.level(s, B.ENTRY[m]) - 1 for s in X.ALL + ("SPY",) if s == "SPY" or s in B.FIRST[m]}
       for m, e in zip(MONTHS, ENDS)}


def shorts(m, f, universe):
    return [t for t, s in B.FIRST[m].items() if t in universe and f(ROW[(t, s["as_of"])])]


def run(f, hold, universe=X.ALL):
    cohorts = {m: shorts(m, f, universe) for m in MONTHS}
    out = []
    for j, m in enumerate(MONTHS):
        live = MONTHS[max(0, j - hold + 1): j + 1]
        legs = [RET[m]["SPY"] - statistics.fmean(RET[m][t] for t in cohorts[c]) if cohorts[c] else 0.0 for c in live]
        out.append((m, statistics.fmean(legs), bool(cohorts[m])))
    return out


def stats(xs):
    n = len(xs)
    g = math.prod(1 + x for x in xs)
    mu, sd = statistics.fmean(xs), statistics.pstdev(xs)
    v, pk, mdd = 1.0, 1.0, 0.0
    for x in xs:
        v *= 1 + x
        pk = max(pk, v)
        mdd = min(mdd, v / pk - 1)
    return g ** (12 / n) - 1, sd * math.sqrt(12), (mu / sd * math.sqrt(12) if sd else 0.0), mdd, g - 1


def section_book():
    for label, u in (("all eleven", X.ALL), ("without tech", NONTECH)):
        print(f"\n### The monthly basket, {label}: short the signalled stocks, long SPY ({MONTHS[0]} to {MONTHS[-1]})\n")
        print("| Signal | Hold | Annual return | Volatility | Sharpe | Worst drawdown | Total | Months with a position | Positive months |")
        print("|---|---|---|---|---|---|---|---|---|")
        for name, f in SIGNALS:
            for hold in (1, 6, 12):
                o = run(f, hold, u)
                xs = [x for _, x, _ in o]
                c, vol, sh, dd, tot = stats(xs)
                active = [x for _, x, a in o if a]
                print(f"| {name} | {hold}m | {pct(c)} | {vol * 100:.1f}% | {sh:+.2f} | {dd * 100:.0f}% | {pct(tot)} | {sum(a for _, _, a in o)} | "
                      f"{100 * sum(x > 0 for x in active) / max(1, len(active)):.0f}% |")


def section_years():
    yrs = sorted({m[:4] for m in MONTHS})
    cols = [("MAIN 1m, all", SIGNALS[0][1], 1, X.ALL), ("MAIN 12m, all", SIGNALS[0][1], 12, X.ALL),
            ("MAIN 1m, non-tech", SIGNALS[0][1], 1, NONTECH), ("MAIN + price down 1m, all", SIGNALS[5][1], 1, X.ALL)]
    series = {n: run(f, h, u) for n, f, h, u in cols}
    print("\n### Calendar years of the basket\n")
    print("| Year | " + " | ".join(n for n, *_ in cols) + " | SPY |\n|---|" + "---|" * (len(cols) + 1))
    for y in yrs:
        cells = [pct(math.prod(1 + x for m, x, _ in series[n] if m[:4] == y) - 1) for n, *_ in cols]
        print(f"| {y} | " + " | ".join(cells) + f" | {pct(math.prod(1 + RET[m]['SPY'] for m in MONTHS if m[:4] == y) - 1)} |")


def section_now():
    print("\n### The newest date of each ticker\n")
    print("| Ticker | As of | EPP gap | Change over 26 weeks | 12m price change | MAIN signal |\n|---|---|---|---|---|---|")
    for t in X.ALL:
        r = max((x for x in X.R if x["ticker"] == t), key=lambda x: x["as_of"])
        d = r["dgap26"]
        print(f"| {t} | {r['as_of']} | {r['gap']:+.0f}% | {'-' if d is None else f'{d:+.0f} points'} | {pct(r['chg_12m'])} | "
              f"{'SHORT' if SIGNALS[0][1](r) else '-'} |")


# ── second test: the falling-EPS filter ──────────────────────────────────────
MAIN = SIGNALS[0][1]
FLOOR_SHRINK = SIGNALS[1][1]
E1 = lambda r: r["eps_last_down"]
E2 = lambda r: r["eps_down26"] is True
EPS_SIGNALS = (
    ("E1 alone: last year's EPS down", E1),
    ("E2 alone: EPS lower than 26 weeks ago", E2),
    ("E3 alone: both", lambda r: E1(r) and E2(r)),
    ("MAIN + E1", lambda r: MAIN(r) and E1(r)),
    ("**MAIN + E2**", lambda r: MAIN(r) and E2(r)),
    ("MAIN + E3", lambda r: MAIN(r) and E1(r) and E2(r)),
    ("below the floor and shrinking + E1", lambda r: FLOOR_SHRINK(r) and E1(r)),
    ("below the floor and shrinking + E2", lambda r: FLOOR_SHRINK(r) and E2(r)),
    ("MAIN + E2 + price down over 12 months", lambda r: MAIN(r) and E2(r) and r["chg_12m"] is not None and r["chg_12m"] < 0),
)
EPS_BASE = ((SIGNALS[0][0].replace("*", "") + " (no EPS filter)", MAIN), ("every date", lambda r: True))


def section_eps_signals():
    print("\n### How often each falling-EPS signal fired (all eleven)\n")
    print("| Signal | Dates | Episodes | Tickers (dates) | Price down over 12 months |\n|---|---|---|---|---|")
    for name, f in EPS_SIGNALS:
        s = [r for r in X.R if f(r)]
        down = [r["chg_12m"] < 0 for r in s if r["chg_12m"] is not None]
        print(f"| {name} | {len(s)} | {X.episodes(s)} | {', '.join(f'{t} {n}' for t, n in Counter(r['ticker'] for r in s).most_common(5))} | "
              f"{100 * sum(down) / max(1, len(down)):.0f}% |")


def eps_pair_table(title, rows):
    print(f"\n### {title}: short the stock, long SPY (positive = the trade won)\n")
    print("| Signal | Dates (12m) | Episodes | " + " | ".join(f"{h}: median / won" for h, _ in HORIZONS) + " |\n|---|---|---|" + "---|" * len(HORIZONS))
    for name, f in EPS_SIGNALS + EPS_BASE:
        s = [r for r in rows if f(r)]
        s12 = [r for r in s if "pair_12m" in r]
        cells = []
        for h, _ in HORIZONS:
            v = [r[f"pair_{h}"] for r in s if f"pair_{h}" in r]
            cells.append(f"{pct(med(v))} / {100 * sum(x > 0 for x in v) / len(v):.0f}%" if v else "-")
        print(f"| {name} | {len(s12)} | {X.episodes(s12) if s12 else 0} | " + " | ".join(cells) + " |")


def section_eps_pairs():
    eps_pair_table("Falling-EPS filter, all eleven", X.R)
    eps_pair_table("Falling-EPS filter, without tech", [r for r in X.R if r["ticker"] in NONTECH])


def section_eps_per():
    f = EPS_SIGNALS[4][1]
    print("\n### Per ticker, MAIN + E2: the pair over 12 and 24 months (median, share won) and the years it fired\n")
    print("| Ticker | Dates | 12m: median / won | 24m: median / won | Years (dates) |\n|---|---|---|---|---|")
    for t in X.ALL:
        s = [r for r in X.R if r["ticker"] == t and f(r)]
        if not s:
            print(f"| {t} | 0 | - | - | - |")
            continue
        c = []
        for h in ("12m", "24m"):
            v = [r[f"pair_{h}"] for r in s if f"pair_{h}" in r]
            c.append(f"{pct(med(v))} / {100 * sum(x > 0 for x in v) / len(v):.0f}%" if v else "-")
        print(f"| {t} | {len(s)} | {c[0]} | {c[1]} | {', '.join(f'{y} ({n})' for y, n in sorted(Counter(r['year'] for r in s).items()))} |")


def section_eps_book():
    for label, u in (("all eleven", X.ALL), ("without tech", NONTECH)):
        print(f"\n### The monthly basket with the falling-EPS filter, {label} ({MONTHS[0]} to {MONTHS[-1]})\n")
        print("| Signal | Hold | Annual return | Volatility | Sharpe | Worst drawdown | Total | Months with a position | Positive months |")
        print("|---|---|---|---|---|---|---|---|---|")
        for name, f in EPS_SIGNALS[3:] + EPS_BASE[:1]:
            for hold in (1, 6, 12):
                o = run(f, hold, u)
                xs = [x for _, x, _ in o]
                c, vol, sh, dd, tot = stats(xs)
                active = [x for _, x, a in o if a]
                print(f"| {name} | {hold}m | {pct(c)} | {vol * 100:.1f}% | {sh:+.2f} | {dd * 100:.0f}% | {pct(tot)} | {sum(a for _, _, a in o)} | "
                      f"{100 * sum(x > 0 for x in active) / max(1, len(active)):.0f}% |")


def section_eps_years():
    yrs = sorted({m[:4] for m in MONTHS})
    cols = [("MAIN + E2, 1m, all", EPS_SIGNALS[4][1], 1, X.ALL), ("MAIN + E2, 12m, all", EPS_SIGNALS[4][1], 12, X.ALL),
            ("MAIN + E2, 12m, non-tech", EPS_SIGNALS[4][1], 12, NONTECH), ("MAIN (no filter), 12m, all", MAIN, 12, X.ALL)]
    series = {n: run(f, h, u) for n, f, h, u in cols}
    print("\n### Calendar years of the falling-EPS basket\n")
    print("| Year | " + " | ".join(n for n, *_ in cols) + " | SPY |\n|---|" + "---|" * (len(cols) + 1))
    for y in yrs:
        cells = [pct(math.prod(1 + x for m, x, _ in series[n] if m[:4] == y) - 1) for n, *_ in cols]
        print(f"| {y} | " + " | ".join(cells) + f" | {pct(math.prod(1 + RET[m]['SPY'] for m in MONTHS if m[:4] == y) - 1)} |")
    print("| years positive | " + " | ".join(f"{sum(math.prod(1 + x for m, x, _ in series[n] if m[:4] == y) > 1 for y in yrs)} of {len(yrs)}"
                                         for n, *_ in cols) + " | |")


def section_eps_post():
    """POST-HOC (added after reading eps_pairs): the falling-EPS filters alone, without the EPP gap, held 3 and 6 months."""
    print("\n### Post-hoc: falling EPS alone as a short against SPY, held 3 and 6 months (chosen after seeing the pair table)\n")
    print("| Universe | Signal | Hold | Annual return | Volatility | Sharpe | Worst drawdown | Months with a position |\n|---|---|---|---|---|---|---|---|")
    for label, u in (("all eleven", X.ALL), ("without tech", NONTECH)):
        for name, f in EPS_SIGNALS[1:3]:
            for hold in (3, 6):
                o = run(f, hold, u)
                c, vol, sh, dd, _ = stats([x for _, x, _ in o])
                print(f"| {label} | {name} | {hold}m | {pct(c)} | {vol * 100:.1f}% | {sh:+.2f} | {dd * 100:.0f}% | {sum(a for _, _, a in o)} |")


def section_eps_now():
    print("\n### The newest date of each ticker, with the falling-EPS readings\n")
    print("| Ticker | As of | EPP gap | Gap change, 26 weeks | E1: last year's EPS down | E2: EPS lower than 26 weeks ago | 12m price | MAIN + E2 |")
    print("|---|---|---|---|---|---|---|---|")
    for t in X.ALL:
        r = max((x for x in X.R if x["ticker"] == t), key=lambda x: x["as_of"])
        d = r["dgap26"]
        print(f"| {t} | {r['as_of']} | {r['gap']:+.0f}% | {'-' if d is None else f'{d:+.0f} points'} | {'yes' if E1(r) else 'no'} | "
              f"{'yes' if E2(r) else 'no' if r['eps_down26'] is False else '-'} | {pct(r['chg_12m'])} | {'SHORT' if EPS_SIGNALS[4][1](r) else '-'} |")


SECTIONS = {"signals": section_signals, "pairs": section_pairs, "per": section_per, "book": section_book, "years": section_years, "now": section_now,
            "eps_signals": section_eps_signals, "eps_pairs": section_eps_pairs, "eps_per": section_eps_per, "eps_book": section_eps_book,
            "eps_years": section_eps_years, "eps_now": section_eps_now,
            "eps_post": section_eps_post}

if __name__ == "__main__":
    print(f"HINDSIGHT. {len(X.R)} weekly dates across {len(X.ALL)} tickers; prices to {LAST}.")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
