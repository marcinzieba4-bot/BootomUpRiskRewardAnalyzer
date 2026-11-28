#!/usr/bin/env python3
"""
HINDSIGHT: does a small EPP gap (or a low Ratio B) mean little room left to fall? And what would selling puts on that idea,
with fixed size or with martingale sizing, have done? Prints the tables quoted in staging/retrospective/EPP_DOWNSIDE.md.

THE TESTS, fixed in this docstring before the first run.
- Every weekly date of the eleven series. Point-in-time readings from analysis.json: the EPP gap, Ratio B, and the BEAR
  price as a share of the price. Prices are Yahoo daily closes (split-adjusted, price only: a put is written on the price).
  Entry is the first close AFTER the as-of date. The EPP floor and the BEAR price are carried to the adjusted series as the
  same share of the as-of close.
- Downside measured after entry over 21, 63, 126 and 252 trading days (1, 3, 6, 12 months):
  - the worst close (the deepest fall from the entry price);
  - the close at the end of the window;
  - the same move in units of the stock's trailing volatility, sigma = the larger of its 252-day and 21-day realised
    volatility before the as-of date, scaled to the window. A fall of more than 1 sigma happens about 16% of the time if
    returns were normal.
- Groups: the engine's EPP bands (<= 0%, 0-40%, 40-100%, 100-200%, > 200%); the engine's Ratio B tiers (below BEAR, < 0.75,
  0.75-1.75, >= 1.75, above BULL); and combined cells (below the floor; 0-40%; Ratio B < 0.75 with EPP gap <= 40%; below
  BEAR; below BEAR and below the floor; above BULL with EPP gap > 100%).
- Floor test: from dates above the EPP floor (or above the BEAR price), how often did the worst close within 3 and 12
  months fall below it, and how far below?
- Put selling (an approximation; no option prices are in the repo). Each month, on each ticker's first as-of date of the
  month:
  - sell a 1-month put (21 trading days) on every ticker that passes the filter. Strike 5% or 10% below the entry close,
    equal notional across tickers, cash-secured (the strikes add up to the capital committed);
  - premium by Black-Scholes, rate 0, volatility = sigma (above) x 1.1. Sensitivity at x 0.9 and x 1.3, since real
    implied volatility is not available.
  - Filters:
    - ALL (every ticker);
    - EPP gap <= 40%;
    - Ratio B < 0.75 with EPP gap <= 40%;
    - below the BEAR price.
  - Sizing:
    - FIXED, committing 100% of equity each month;
    - MARTINGALE, starting at 10% of equity, doubling the commitment after each losing month and back to 10% after a
      winning one. Two martingale variants: capped at 100% (cash-secured), or uncapped (margin). The account is ruined
      if equity reaches zero.
  - Run on all eleven and on the seven without tech (AAPL, MSFT, AVGO, ACN removed).

Everything printed is a label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule"). Reads only; the first run needs the network (retro/.cache/, gitignored).

    python3 staging/retrospective/epp_downside.py                 # every table
    python3 staging/retrospective/epp_downside.py floor bands     # selected sections

Sections: bands combo floor puts streaks single now
(single was added after the first run.)
"""
import bisect
import json
import math
import os
import statistics
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ratio_b_basket as B  # noqa: E402  (tickers, series paths, retro_tool, monthly first dates and entries)

X, rt = B.X, B.rt
WINDOWS = (21, 63, 126, 252)
TECH = ("AAPL", "MSFT", "AVGO", "ACN")
NONTECH = tuple(t for t in X.ALL if t not in TECH)
PX = {}
for t in X.ALL:
    c, _ = rt.fetch_prices(t)
    ks = sorted(c)
    PX[t] = (ks, [c[k] for k in ks])


def vol(closes, i, n):
    lr = [math.log(closes[k] / closes[k - 1]) for k in range(max(1, i - n + 1), i + 1)]
    return statistics.pstdev(lr) * math.sqrt(252) if len(lr) > 5 else None


ROWS = []
for r in X.R:
    t = r["ticker"]
    a = json.load(open(os.path.join(X.ROOT, X.SERIES[t], r["as_of"], "analysis.json")))
    m = a["metrics"]
    ks, cl = PX[t]
    i = bisect.bisect_right(ks, r["as_of"]) - 1                 # the as-of close
    e = i + 1                                                    # entry: the next close
    if e >= len(cl):
        continue
    s1, s21 = vol(cl, i, 252), vol(cl, i, 21)
    if s1 is None and s21 is None:                               # too little history (AVGO's first days after listing)
        continue
    row = {"ticker": t, "as_of": r["as_of"], "date": r["date"], "year": r["year"], "gap": m["epp_gap_pct"], "rb": m["ratio_b"],
           "floor": cl[i] / (1 + m["epp_gap_pct"] / 100), "bear": cl[i] * m["scenarios"]["BEAR"]["price"] / a["price"],
           "s0": cl[e], "entry": ks[e], "sigma": max(x for x in (s1, s21) if x is not None)}
    for n in WINDOWS:
        if e + n < len(cl):
            seg = cl[e + 1:e + n + 1]
            row[f"min{n}"] = min(seg) / cl[e] - 1
            row[f"end{n}"] = cl[e + n] / cl[e] - 1
            sd = row["sigma"] * math.sqrt(n / 252)
            row[f"zend{n}"] = math.log(cl[e + n] / cl[e]) / sd
            row[f"zmin{n}"] = math.log(min(seg) / cl[e]) / sd
            row[f"brk_floor{n}"] = min(seg) < row["floor"] if row["gap"] > 0 else None
            row[f"below_floor{n}"] = min(seg) / row["floor"] - 1
            row[f"brk_bear{n}"] = min(seg) < row["bear"] if row["rb"] >= 0 else None
            row[f"below_bear{n}"] = min(seg) / row["bear"] - 1
    ROWS.append(row)

med = statistics.median_high


def q(xs, p):
    s = sorted(xs)
    return s[min(len(s) - 1, int(p * len(s)))]


def pct(v):
    return "-" if v is None else f"{v * 100:+.0f}%"


def share(xs):
    return f"{100 * sum(xs) / len(xs):.0f}%" if xs else "-"


EPP_BANDS = (("below the floor (<= 0%)", lambda r: r["gap"] <= 0), ("0-40%", lambda r: 0 < r["gap"] <= 40),
             ("40-100%", lambda r: 40 < r["gap"] <= 100), ("100-200%", lambda r: 100 < r["gap"] <= 200), ("> 200%", lambda r: r["gap"] > 200))
RB_BANDS = (("below BEAR (< 0)", lambda r: r["rb"] < 0), ("BUY (0-0.75)", lambda r: 0 <= r["rb"] < 0.75),
            ("0.75-1.75", lambda r: 0.75 <= r["rb"] < 1.75), (">= 1.75", lambda r: 1.75 <= r["rb"] < math.inf),
            ("above BULL (inf)", lambda r: math.isinf(r["rb"])))
COMBO = (("below the EPP floor", lambda r: r["gap"] <= 0), ("EPP gap 0-40%", lambda r: 0 < r["gap"] <= 40),
         ("Ratio B < 0.75 and EPP gap <= 40%", lambda r: r["rb"] < 0.75 and r["gap"] <= 40),
         ("below BEAR (Ratio B < 0)", lambda r: r["rb"] < 0), ("below BEAR and below the floor", lambda r: r["rb"] < 0 and r["gap"] <= 0),
         ("above BULL and EPP gap > 100%", lambda r: math.isinf(r["rb"]) and r["gap"] > 100), ("every date", lambda r: True))


def downside_table(title, groups, rows=None):
    rows = rows if rows is not None else ROWS
    print(f"\n### {title}\n")
    print("| Group | Dates | Episodes | Median sigma | 1m: close < -10% | 1m: below -1 sigma | 3m: median worst | 3m: worst 5% | "
          "3m: worst < -20% | 3m: below -1 sigma | 12m: worst 5% | 12m: worst < -30% |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    for name, f in groups:
        s = [r for r in rows if f(r)]
        s1, s3, s12 = [r for r in s if "end21" in r], [r for r in s if "min63" in r], [r for r in s if "min252" in r]
        if not s3:
            print(f"| {name} | 0 |" + " |" * 10)
            continue
        print(f"| {name} | {len(s3)} | {X.episodes(s3)} | {med([r['sigma'] for r in s3]) * 100:.0f}% | "
              f"{share([r['end21'] < -0.10 for r in s1])} | {share([r['zend21'] < -1 for r in s1])} | "
              f"{pct(med([r['min63'] for r in s3]))} | {pct(q([r['min63'] for r in s3], 0.05))} | {share([r['min63'] < -0.20 for r in s3])} | "
              f"{share([r['zend63'] < -1 for r in s3])} | {pct(q([r['min252'] for r in s12], 0.05)) if s12 else '-'} | "
              f"{share([r['min252'] < -0.30 for r in s12])} |")


def section_bands():
    downside_table("By EPP gap (the engine's bands), all eleven", EPP_BANDS)
    downside_table("By Ratio B (the engine's tiers), all eleven", RB_BANDS)


def section_combo():
    for label, ts in (("all eleven", X.ALL), ("without tech", NONTECH)):
        downside_table(f"EPP gap with the Ratio B filter, {label}", COMBO, [r for r in ROWS if r["ticker"] in ts])


def section_floor():
    print("\n### Did the EPP floor and the BEAR price hold? (all eleven)\n")
    print("| Start | Level | Dates | Worst close fell below it within 3 months | within 12 months | When it broke within 12 months: median / worst 5% below the level |")
    print("|---|---|---|---|---|---|")
    for name, f, lvl in (("above the floor, gap 0-40%", lambda r: 0 < r["gap"] <= 40, "floor"),
                         ("above the floor, gap 40-100%", lambda r: 40 < r["gap"] <= 100, "floor"),
                         ("above the floor, any gap", lambda r: r["gap"] > 0, "floor"),
                         ("above BEAR, Ratio B 0-0.75", lambda r: 0 <= r["rb"] < 0.75, "bear"),
                         ("above BEAR, any Ratio B", lambda r: r["rb"] >= 0, "bear")):
        s = [r for r in ROWS if f(r) and "min252" in r]
        k3, k12 = ("brk_floor63", "brk_floor252") if lvl == "floor" else ("brk_bear63", "brk_bear252")
        depth = [r["below_floor252" if lvl == "floor" else "below_bear252"] for r in s if r[k12]]
        print(f"| {name} | {'EPP floor' if lvl == 'floor' else 'BEAR price'} | {len(s)} | {share([r[k3] for r in s])} | {share([r[k12] for r in s])} | "
              f"{pct(med(depth)) if depth else '-'} / {pct(q(depth, 0.05)) if depth else '-'} |")
    print("\n### Already below the floor: how much further did it fall? (all eleven)\n")
    print("| Start | Dates | Episodes | 3m: median worst | 3m: worst 5% | 12m: median worst | 12m: worst 5% | 12m: worst < -20% |\n|---|---|---|---|---|---|---|---|")
    for name, f in (("below the floor (gap <= 0%)", lambda r: r["gap"] <= 0), ("below BEAR (Ratio B < 0)", lambda r: r["rb"] < 0),
                    ("below both", lambda r: r["gap"] <= 0 and r["rb"] < 0), ("every date", lambda r: True)):
        s = [r for r in ROWS if f(r) and "min252" in r]
        print(f"| {name} | {len(s)} | {X.episodes(s)} | {pct(med([r['min63'] for r in s]))} | {pct(q([r['min63'] for r in s], 0.05))} | "
              f"{pct(med([r['min252'] for r in s]))} | {pct(q([r['min252'] for r in s], 0.05))} | {share([r['min252'] < -0.20 for r in s])} |")
    print("\nWorst 12-month falls from below the floor (the tail a put seller carries):")
    s = sorted((r for r in ROWS if r["gap"] <= 0 and "min252" in r), key=lambda r: r["min252"])
    seen = set()
    for r in s:
        if (r["ticker"], r["year"]) in seen:
            continue
        seen.add((r["ticker"], r["year"]))
        print(f"- {r['ticker']} from {r['as_of']} (gap {r['gap']:+.0f}%, Ratio B {r['rb']:.2f}): worst {pct(r['min252'])} within 12 months")
        if len(seen) == 6:
            break


# ── Put selling ──────────────────────────────────────────────────────────────
def bs_put(s, k, t, sig):
    if sig <= 0 or t <= 0:
        return max(k - s, 0.0)
    d1 = (math.log(s / k) + 0.5 * sig * sig * t) / (sig * math.sqrt(t))
    d2 = d1 - sig * math.sqrt(t)
    n = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    return k * n(-d2) - s * n(-d1)


BY_KEY = {(r["ticker"], r["as_of"]): r for r in ROWS}
FILTERS = (("ALL", lambda r: True), ("EPP gap <= 40%", lambda r: r["gap"] <= 40),
           ("Ratio B < 0.75 and EPP gap <= 40%", lambda r: r["rb"] < 0.75 and r["gap"] <= 40), ("below BEAR", lambda r: r["rb"] < 0))


def monthly_trades(filt, otm, ivx, universe):
    """Per month: the return on capital committed (premium minus payoff over summed strikes), or None if nothing passed."""
    out = []
    for m in B.MONTHS:
        legs = []
        for t, s in B.FIRST[m].items():
            r = BY_KEY.get((t, s["as_of"]))
            if t not in universe or r is None or "end21" not in r or not filt(r):
                continue
            k = 1 - otm                                         # per $1 of entry price
            prem = bs_put(1.0, k, 21 / 252, r["sigma"] * ivx)
            st = 1 + r["end21"]
            legs.append((prem - max(k - st, 0.0)) / k)
        out.append((m, statistics.fmean(legs) if legs else None, len(legs)))
    return out


def run_sizing(trades, mode, base=0.10):
    eq, peak, mdd, frac, worst, ruin, maxfrac = 1.0, 1.0, 0.0, base, 0.0, None, base
    for m, r, _ in trades:
        if r is None:
            continue
        f = 1.0 if mode == "FIXED" else frac
        eq *= 1 + f * r
        worst = min(worst, f * r)
        if eq <= 0:
            ruin = m
            eq = 0.0
            mdd = -1.0
            break
        peak = max(peak, eq)
        mdd = min(mdd, eq / peak - 1)
        if mode != "FIXED":
            frac = base if r > 0 else frac * 2
            if mode == "MARTINGALE capped":
                frac = min(frac, 1.0)
            maxfrac = max(maxfrac, frac)
    yrs = len(B.MONTHS) / 12
    cagr = eq ** (1 / yrs) - 1 if eq > 0 else -1.0
    return cagr, mdd, worst, ruin, maxfrac


def section_puts():
    for label, u in (("all eleven", X.ALL), ("without tech", NONTECH)):
        print(f"\n### Selling 1-month puts, {label}: {B.MONTHS[0]} to {B.MONTHS[-1]} (premium = Black-Scholes at 1.1 x sigma)\n")
        print("| Filter | Strike | Months traded | Losing months | Worst month (on committed capital) | FIXED: annual / worst drawdown | "
              "MARTINGALE capped at 100%: annual / worst drawdown / largest commitment | MARTINGALE uncapped: annual / worst drawdown / ruin |")
        print("|---|---|---|---|---|---|---|---|")
        for fname, f in FILTERS:
            for otm in (0.05, 0.10):
                tr = monthly_trades(f, otm, 1.1, u)
                rs = [r for _, r, _ in tr if r is not None]
                if not rs:
                    continue
                fx = run_sizing(tr, "FIXED")
                mc = run_sizing(tr, "MARTINGALE capped")
                mu = run_sizing(tr, "MARTINGALE uncapped")
                print(f"| {fname} | {otm:.0%} below | {len(rs)} | {sum(r < 0 for r in rs)} | {pct(min(rs))} | {pct(fx[0])} / {pct(fx[1])} | "
                      f"{pct(mc[0])} / {pct(mc[1])} / {mc[4]:.0%} | {pct(mu[0])} / {pct(mu[1])} / {mu[3] or 'none'} (peak {mu[4]:.0%}) |")
        print(f"\nPremium sensitivity ({label}, filter Ratio B < 0.75 and EPP gap <= 40%, 10% below, FIXED sizing):")
        for ivx in (0.9, 1.1, 1.3):
            tr = monthly_trades(FILTERS[2][1], 0.10, ivx, u)
            fx = run_sizing(tr, "FIXED")
            print(f"- volatility x {ivx}: annual {pct(fx[0])}, worst drawdown {pct(fx[1])}")


def section_streaks():
    print("\n### Losing streaks and the worst months (1-month puts 10% below, filter Ratio B < 0.75 and EPP gap <= 40%, all eleven)\n")
    tr = monthly_trades(FILTERS[2][1], 0.10, 1.1, X.ALL)
    rs = [(m, r) for m, r, _ in tr if r is not None]
    streak, best, cur_start, worst_runs = 0, 0, None, []
    for m, r in rs:
        if r < 0:
            streak += 1
            cur_start = cur_start or m
            best = max(best, streak)
        else:
            if streak >= 2:
                worst_runs.append((cur_start, streak))
            streak, cur_start = 0, None
    print(f"Longest run of losing months: {best}. Runs of two or more: " + (", ".join(f"{a} ({n})" for a, n in worst_runs) or "none") + ".")
    print("\nWorst months (return on the capital committed that month):")
    for m, r in sorted(rs, key=lambda x: x[1])[:8]:
        print(f"- {m}: {pct(r)}")


def section_single():
    """Added after the first run: the martingale on one stock at a time, where losing months can come in a row."""
    print("\n### One stock at a time: monthly 1-month puts 5% below, premium at 1.1 x sigma (added after the first run)\n")
    print("| Ticker | Filter | Months traded | Losing months | Longest losing run | Worst month | FIXED 100%: annual / worst drawdown | "
          "MARTINGALE uncapped (base 10%): annual / worst drawdown / largest commitment / ruin |\n|---|---|---|---|---|---|---|---|")
    for t in X.ALL:
        for fname, f in (("ALL", lambda r: True), ("EPP gap <= 40%", lambda r: r["gap"] <= 40)):
            tr = monthly_trades(f, 0.05, 1.1, (t,))
            rs = [r for _, r, _ in tr if r is not None]
            if len(rs) < 12:
                continue
            run = best = 0
            for r in rs:
                run = run + 1 if r < 0 else 0
                best = max(best, run)
            fx = run_sizing(tr, "FIXED")
            mu = run_sizing(tr, "MARTINGALE uncapped")
            print(f"| {t} | {fname} | {len(rs)} | {sum(r < 0 for r in rs)} | {best} | {pct(min(rs))} | {pct(fx[0])} / {pct(fx[1])} | "
                  f"{pct(mu[0])} / {pct(mu[1])} / {mu[4]:.0%} / {mu[3] or 'none'} |")


def fmt_rb(v):
    return "inf" if math.isinf(v) else f"{v:.2f}"


def section_now():
    print("\n### The newest dates: EPP floor and BEAR price as a fall from the last close\n")
    print("| Ticker | As of | EPP gap | Fall to the EPP floor | Ratio B | Fall to BEAR | Sigma (annual) | 1-sigma 1-month move |\n|---|---|---|---|---|---|---|---|")
    for t in X.ALL:
        r = max((x for x in ROWS if x["ticker"] == t), key=lambda x: x["as_of"])
        ks, cl = PX[t]
        last = cl[-1]
        print(f"| {t} | {r['as_of']} | {r['gap']:+.0f}% | {pct(r['floor'] / last - 1)} | {fmt_rb(r['rb'])} | "
              f"{pct(r['bear'] / last - 1)} | {r['sigma'] * 100:.0f}% | {pct(-r['sigma'] * math.sqrt(21 / 252))} |")


SECTIONS = {"bands": section_bands, "combo": section_combo, "floor": section_floor, "puts": section_puts,
            "streaks": section_streaks, "single": section_single,
            "now": section_now}

if __name__ == "__main__":
    print(f"HINDSIGHT. {len(ROWS)} dates across {len(X.ALL)} tickers; prices to {max(PX[t][0][-1] for t in X.ALL)}.")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
