#!/usr/bin/env python3
"""
HINDSIGHT: what worked over the long run (5-10 years) across the eleven retrospective series, and whether a simple
monthly-investing rule built on point-in-time readings beat buying everything equally. Prints the tables quoted in
staging/retrospective/LONG_TERM_FINDINGS.md.

Inputs, all read and never written:
- each date's point-in-time readings, loaded by cross_ticker_oos.py (own 10-year P/E percentile, 12-month price change,
  distance below the 52-week high, house class and tier);
- daily closes and dividends from Yahoo through retro_tool.fetch_prices, the source and cache (retro/.cache/,
  gitignored) that the outcome.json files use. The first run needs the network.
Long horizons reinvest dividends (a total-return index). outcome.json adds the cash without reinvesting, which matters
little at two years but more at ten.

Everything printed is a label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

THE MONTHLY-INVESTING TEST. The rules and the scoring below were fixed in this docstring before the first run, and every
rule is printed, the losers included.
- Each calendar month, $1,000 is invested on each ticker's first as-of date that month, using only that date's
  point-in-time readings. Purchases are at that day's close, dividends are reinvested, nothing is ever sold, and there
  are no costs or taxes. A ticker joins the universe at its first as-of date (AVGO in August 2009).
- Rules: SPY; RSP (the equal-weight S&P 500); EQUAL (split equally across the tickers listed that month);
  DEEPEST_FALL (all into the ticker furthest below its 52-week high); FALL_RANKED (split by rank of the distance below the
  52-week high, deepest weighted most); CRASH_FIRST (split equally across tickers in the frozen crash zone, else EQUAL);
  CHEAPEST_PE (all into the lowest own P/E percentile); CHEAP_RANKED (split by rank, cheapest weighted most);
  STRONGEST_12M (all into the largest 12-month gain); STRONG_RANKED (split by rank, strongest weighted most);
  HOUSE_CHEAP (equal across class CHEAP, else EQUAL); SKIP_EXP_RUNNING (equal across the tickers not in expensive &
  running, else EQUAL). Ties split equally. A rule with no candidates that month (no 12-month history in 2008) falls
  back to EQUAL.
- Scored on: the money-weighted annual return (IRR) over 2008-01 to 2026-10, valued at the last close; every five-year
  and ten-year contribution window starting in January, valued at the window's end; and the full period with each
  ticker left out in turn. EQUAL is the fair benchmark, because every rule draws on the same eleven stocks picked in 2026.

    python3 staging/retrospective/long_term.py               # every table
    python3 staging/retrospective/long_term.py sim windows    # selected sections

Sections: horizons rank sim windows loo
Medians of an even count take the upper middle value (statistics.median_high).
"""
import bisect
import datetime as dt
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
import cross_ticker_oos as X  # noqa: E402  (loads the point-in-time rows; prints nothing on import)

med = statistics.median_high
TICKERS = X.ALL
HORIZONS = (("3y", 36), ("5y", 60), ("7y", 84), ("10y", 120))
AMOUNT = 1000.0


def tr_index(symbol):
    """Sorted trading days and a total-return index with dividends reinvested on the ex-date (or the next trading day)."""
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


IDX = {s: tr_index(s) for s in TICKERS + ("SPY", "RSP")}
LAST = min(IDX[s][0][-1] for s in IDX)


def level(symbol, date):
    days, v = IDX[symbol]
    i = bisect.bisect_right(days, date) - 1
    return v[i] if i >= 0 else None


def fwd(symbol, start, months):
    end = rt.add_months(start, months)
    if end > LAST:
        return None
    return level(symbol, end) / level(symbol, start) - 1


def ann(ret, months):
    return (1 + ret) ** (12 / months) - 1


for r in X.R:
    for h, m in HORIZONS:
        t = fwd(r["ticker"], r["as_of"], m)
        if t is None:
            continue
        r[f"lt_{h}"] = ann(t, m)
        r[f"lt_spy_{h}"] = ann(fwd("SPY", r["as_of"], m), m)
        r[f"lt_rsp_{h}"] = ann(fwd("RSP", r["as_of"], m), m)
LBASE = {(t, h): med([r[f"lt_{h}"] for r in X.R if r["ticker"] == t and f"lt_{h}" in r]) for t in TICKERS for h, _ in HORIZONS}


def p1(v, unit="%"):
    return "-" if v is None else f"{v * 100:+.1f}{unit}"


# ─────────────────────────────────────────────────────────────────────────────
# Single entries held 3-10 years
# ─────────────────────────────────────────────────────────────────────────────
GROUPS = (
    ("all dates", lambda r: True),
    ("crash (frozen rule)", X.CRASH),
    ("cheap & falling (frozen rule)", X.CHEAP_FALLING),
    ("expensive & running (frozen rule)", X.EXPENSIVE_RUNNING),
    ("40%+ below the 52w high", lambda r: r["dd_52w"] <= -0.40),
    ("30-40% below", lambda r: -0.40 < r["dd_52w"] <= -0.30),
    ("20-30% below", lambda r: -0.30 < r["dd_52w"] <= -0.20),
    ("10-20% below", lambda r: -0.20 < r["dd_52w"] <= -0.10),
    ("within 10% of the high", lambda r: r["dd_52w"] > -0.10),
    ("own P/E pctl 0-19", lambda r: r["pe_pctl"] < 20),
    ("own P/E pctl 20-39", lambda r: 20 <= r["pe_pctl"] < 40),
    ("own P/E pctl 40-79", lambda r: 40 <= r["pe_pctl"] < 80),
    ("own P/E pctl 80-100", lambda r: r["pe_pctl"] >= 80),
    ("class CHEAP", lambda r: r["class"] == "CHEAP"),
    ("class RICH", lambda r: r["class"] == "RICH"),
    ("tier BUY", lambda r: r["tier"] == "BUY"),
    ("tier AVOID", lambda r: r["tier"] == "AVOID"),
)


def section_horizons():
    for h, m in HORIZONS:
        s_all = [r for r in X.R if f"lt_{h}" in r]
        first, last = min(r["as_of"] for r in s_all), max(r["as_of"] for r in s_all)
        print(f"\n### Held {h} (start dates {first} to {last}; annual rates, dividends reinvested)\n")
        print("| Group | Dates | Episodes | Tickers | Median /yr | vs own base /yr | Beat own base | vs SPY /yr | Beat SPY | "
              "vs RSP /yr | Lost money |\n|---|---|---|---|---|---|---|---|---|---|---|")
        for name, f in GROUPS:
            s = [r for r in s_all if f(r)]
            if not s:
                print(f"| {name} | 0 |" + " |" * 9)
                continue
            print(f"| {name} | {len(s)} | {X.episodes(s)} | {len({r['ticker'] for r in s})} | {p1(med([r[f'lt_{h}'] for r in s]))} | "
                  f"{p1(med([r[f'lt_{h}'] - LBASE[(r['ticker'], h)] for r in s]), 'pp')} | "
                  f"{100 * sum(r[f'lt_{h}'] > LBASE[(r['ticker'], h)] for r in s) / len(s):.0f}% | "
                  f"{p1(med([r[f'lt_{h}'] - r[f'lt_spy_{h}'] for r in s]), 'pp')} | {100 * sum(r[f'lt_{h}'] > r[f'lt_spy_{h}'] for r in s) / len(s):.0f}% | "
                  f"{p1(med([r[f'lt_{h}'] - r[f'lt_rsp_{h}'] for r in s]), 'pp')} | {100 * sum(r[f'lt_{h}'] < 0 for r in s) / len(s):.0f}% |")
    print("\n### Each ticker's own base (median annual rate over its dates with that horizon)\n")
    print("| Ticker | " + " | ".join(h for h, _ in HORIZONS) + " | Beat SPY at 5y | Beat SPY at 10y |\n|---|" + "---|" * (len(HORIZONS) + 2))
    for t in TICKERS:
        s5 = [r for r in X.R if r["ticker"] == t and "lt_5y" in r]
        s10 = [r for r in X.R if r["ticker"] == t and "lt_10y" in r]
        print(f"| {t} | " + " | ".join(p1(LBASE[(t, h)]) for h, _ in HORIZONS) +
              f" | {100 * sum(r['lt_5y'] > r['lt_spy_5y'] for r in s5) / len(s5):.0f}% | {100 * sum(r['lt_10y'] > r['lt_spy_10y'] for r in s10) / len(s10):.0f}% |")


def section_rank():
    print("\n### Within each ticker's own series: rank correlation with the forward annual rate (+ = a lower reading did better)\n")
    keys = (("12m change", "chg_12m"), ("52w high distance", "dd_52w"), ("own P/E pctl", "pe_pctl"))
    print("| Ticker | " + " | ".join(f"{n} {h}" for n, _ in keys for h, _ in HORIZONS) + " |\n|---|" + "---|" * (len(keys) * len(HORIZONS)))
    pos = Counter()
    for t in TICKERS:
        cells = []
        for n, k in keys:
            for h, _ in HORIZONS:
                s = [r for r in X.R if r["ticker"] == t and f"lt_{h}" in r and r[k] is not None]
                v = -X.spearman([r[k] for r in s], [r[f"lt_{h}"] for r in s])
                pos[(n, h)] += v > 0
                cells.append(f"{v:+.2f}")
        print(f"| {t} | " + " | ".join(cells) + " |")
    print("| positive in | " + " | ".join(f"{pos[(n, h)]} of {len(TICKERS)}" for n, _ in keys for h, _ in HORIZONS) + " |")


# ─────────────────────────────────────────────────────────────────────────────
# Monthly investing
# ─────────────────────────────────────────────────────────────────────────────
MONTHLY = defaultdict(dict)        # "YYYY-MM" -> {ticker: that ticker's first row of the month}
for r in sorted(X.R, key=lambda r: r["as_of"]):
    MONTHLY[r["as_of"][:7]].setdefault(r["ticker"], r)
MONTHS = sorted(m for m in MONTHLY if m <= "2026-10")


def equal(rows):
    return {r["ticker"]: 1 / len(rows) for r in rows}


def pick(rows, key, lowest):
    cand = [r for r in rows if r[key] is not None]
    if not cand:
        return equal(rows)
    best = (min if lowest else max)(r[key] for r in cand)
    top = [r for r in cand if r[key] == best]
    return {r["ticker"]: 1 / len(top) for r in top}


def ranked(rows, key, lowest):
    cand = [r for r in rows if r[key] is not None]
    if not cand:
        return equal(rows)
    order = sorted(cand, key=lambda r: r[key], reverse=lowest)      # the most favoured last, so it gets the top rank
    w = {}
    i = 0
    while i < len(order):                                           # ties share the average rank
        j = i
        while j + 1 < len(order) and order[j + 1][key] == order[i][key]:
            j += 1
        for k in range(i, j + 1):
            w[order[k]["ticker"]] = (i + j) / 2 + 1
        i = j + 1
    tot = sum(w.values())
    return {t: v / tot for t, v in w.items()}


def subset(rows, f):
    s = [r for r in rows if f(r)]
    return equal(s) if s else equal(rows)


RULES = {
    "EQUAL": equal,
    "DEEPEST_FALL": lambda rows: pick(rows, "dd_52w", True),
    "FALL_RANKED": lambda rows: ranked(rows, "dd_52w", True),
    "CRASH_FIRST": lambda rows: subset(rows, X.CRASH),
    "CHEAPEST_PE": lambda rows: pick(rows, "pe_pctl", True),
    "CHEAP_RANKED": lambda rows: ranked(rows, "pe_pctl", True),
    "STRONGEST_12M": lambda rows: pick(rows, "chg_12m", False),
    "STRONG_RANKED": lambda rows: ranked(rows, "chg_12m", False),
    "HOUSE_CHEAP": lambda rows: subset(rows, lambda r: r["class"] == "CHEAP"),
    "SKIP_EXP_RUNNING": lambda rows: subset(rows, lambda r: not X.EXPENSIVE_RUNNING(r)),
}
ORDER = ("SPY", "RSP") + tuple(RULES)


def xirr(flows):
    """flows: [(date string, amount)], contributions negative, the final value positive. Annual money-weighted return."""
    d0 = dt.date.fromisoformat(flows[0][0])
    tf = [((dt.date.fromisoformat(d) - d0).days / 365.25, a) for d, a in flows]
    npv = lambda rate: sum(a / (1 + rate) ** t for t, a in tf)
    lo, hi = -0.99, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if npv(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def simulate(rule, months, end, universe=TICKERS):
    """Units held per symbol after investing AMOUNT each month; returns (IRR, final value, invested, units, TWR path)."""
    units, flows, path = defaultdict(float), [], []
    for m in months:
        rows = [r for t, r in MONTHLY[m].items() if t in universe]
        if not rows:
            continue
        day = min(r["as_of"] for r in rows)
        before = sum(u * level(s, day) for s, u in units.items())
        if rule in ("SPY", "RSP"):
            alloc = {rule: (1.0, day)}
        else:
            w = RULES[rule](rows)
            alloc = {t: (w[t], MONTHLY[m][t]["as_of"]) for t in w}
        for s, (wt, d) in alloc.items():
            units[s] += AMOUNT * wt / level(s, d)
        path.append((day, before, sum(u * level(s, day) for s, u in units.items())))
        flows.append((day, -AMOUNT))
    value = sum(u * level(s, end) for s, u in units.items())
    flows.append((end, value))
    twr, peak, mdd = 1.0, 1.0, 0.0                 # time-weighted path: growth between contributions, flows removed
    for (_, _, after), (_, before, _) in zip(path, path[1:]):
        twr *= before / after
        peak = max(peak, twr)
        mdd = min(mdd, twr / peak - 1)
    return xirr(flows), value, AMOUNT * (len(flows) - 1), units, mdd


def first_trading_day(date):
    days = IDX["SPY"][0]
    return days[bisect.bisect_left(days, date)]


def section_sim():
    res = {k: simulate(k, MONTHS, LAST) for k in ORDER}
    eq = res["EQUAL"]
    print(f"\n### $1,000 a month, {MONTHS[0]} to {MONTHS[-1]} ({len(MONTHS)} months), valued at the last close {LAST}\n")
    print("| Rule | Invested | Final value | Annual return (IRR) | vs EQUAL | vs SPY | Worst fall (time-weighted) | Largest holding at the end |")
    print("|---|---|---|---|---|---|---|---|")
    for k in ORDER:
        irr, v, inv, units, mdd = res[k]
        hold = {s: u * level(s, LAST) for s, u in units.items()}
        top = max(hold, key=hold.get)
        print(f"| {k} | ${inv:,.0f} | ${v:,.0f} | {irr * 100:.1f}% | {p1(irr - eq[0], 'pp')} | {p1(irr - res['SPY'][0], 'pp')} | "
              f"{mdd * 100:.0f}% | {top} {100 * hold[top] / v:.0f}% |")
    print("\nWhere each rule's money went (share of all contributions, top three):\n")
    for k in RULES:
        spent = Counter()
        for m in MONTHS:
            rows = list(MONTHLY[m].values())
            for t, w in RULES[k](rows).items():
                spent[t] += w
        tot = sum(spent.values())
        print(f"- {k}: " + ", ".join(f"{t} {100 * v / tot:.0f}%" for t, v in spent.most_common(3)))


def windows(years):
    out = []
    for y in range(2008, 2027):
        end = first_trading_day(f"{y + years}-01-01") if f"{y + years}-01-01" <= LAST else None
        if end is None:
            break
        out.append((y, [m for m in MONTHS if f"{y}-01" <= m <= f"{y + years - 1}-12"], end))
    return out


def section_windows():
    for years in (5, 10):
        ws = windows(years)
        table = {k: [simulate(k, ms, end)[0] for _, ms, end in ws] for k in ORDER}
        print(f"\n### {years}-year monthly-investing windows (start each January, valued at the window's end; annual IRR)\n")
        print("| Rule | " + " | ".join(f"{y}-{y + years - 1}" for y, _, _ in ws) + " | Beat EQUAL | Beat SPY | Median vs EQUAL |")
        print("|---|" + "---|" * (len(ws) + 3))
        for k in ORDER:
            v = table[k]
            print(f"| {k} | " + " | ".join(f"{x * 100:.1f}" for x in v) +
                  f" | {sum(a > b for a, b in zip(v, table['EQUAL']))} of {len(ws)} | {sum(a > b for a, b in zip(v, table['SPY']))} of {len(ws)} | "
                  f"{p1(med([a - b for a, b in zip(v, table['EQUAL'])]), 'pp')} |")


def section_loo():
    print(f"\n### The full period with one ticker left out (annual IRR minus EQUAL's on the same ten tickers)\n")
    print("| Rule | " + " | ".join(f"no {t}" for t in TICKERS) + " | Beat EQUAL | Worst |\n|---|" + "---|" * (len(TICKERS) + 2))
    rows = defaultdict(list)
    for t in TICKERS:
        uni = tuple(x for x in TICKERS if x != t)
        base = simulate("EQUAL", MONTHS, LAST, uni)[0]
        for k in ORDER:
            if k != "EQUAL":
                rows[k].append(simulate(k, MONTHS, LAST, uni)[0] - base)
    for k in ORDER:
        if k == "EQUAL":
            continue
        v = rows[k]
        print(f"| {k} | " + " | ".join(f"{x * 100:+.1f}" for x in v) + f" | {sum(x > 0 for x in v)} of {len(v)} | {min(v) * 100:+.1f}pp |")


SECTIONS = {"horizons": section_horizons, "rank": section_rank, "sim": section_sim, "windows": section_windows, "loo": section_loo}

if __name__ == "__main__":
    print(f"HINDSIGHT. {len(X.R)} point-in-time dates across {len(TICKERS)} tickers; prices and dividends to {LAST}. "
          + ", ".join(f"{sum(f'lt_{h}' in r for r in X.R)} dates with a {h} outcome" for h, _ in HORIZONS) + ".")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
