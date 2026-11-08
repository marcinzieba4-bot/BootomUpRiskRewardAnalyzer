#!/usr/bin/env python3
"""
HINDSIGHT: test the ACN/UNP/LOW cross-ticker patterns (CROSS_TICKER_FINDINGS.md) out of sample on the eight tickers built
after them (AAPL, AVGO, MSFT, NKE, PEP, SHW, WMT, XOM), and pool all eleven. Prints the tables quoted in
staging/retrospective/CROSS_TICKER_OUT_OF_SAMPLE.md.

Reads only what is already in the repo and writes nothing. Each row joins one date's point-in-time values (analysis.json,
the PE_NOW_PCTL literal read from model.py as text and never executed, report.txt's 52-week high) with its outcome.json.
The trailing 12-month price change comes from the weekly series itself, restated across the splits in each ticker's fact
sheet (retro/facts/<TICKER>.json, "splits"), so it uses only prices public by the as-of date. Everything printed is a
label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule (retro/README.md,
"The one rule"), and nothing from one ticker's outcomes enters another ticker's models.

The three zones are copied unchanged from cross_ticker.py, where they were fixed on ACN, UNP and LOW before any of the
eight newer tickers existed. That is what makes the eight an out-of-sample test of them. Every other cut printed here
(the 52-week drawdown buckets, the market-wide split, the same-week ranks) was chosen while looking at all eleven.

    python3 staging/retrospective/cross_ticker_oos.py              # every table
    python3 staging/retrospective/cross_ticker_oos.py zones per    # selected sections

Sections: base zones per single grid house rank xrank breadth quarter composition latest
Medians of an even count take the upper middle value (statistics.median_high), as in the FINDINGS files.
"""
import datetime as dt
import json
import math
import os
import re
import statistics
import sys
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DISCOVERY = ("ACN", "UNP", "LOW")
TEST = ("AAPL", "AVGO", "MSFT", "NKE", "PEP", "SHW", "WMT", "XOM")
ALL = DISCOVERY + TEST
SERIES = {t: "archive/retrospective/ACN" if t == "ACN" else f"staging/retrospective/{t}" for t in ALL}
SETS = (("discovery (ACN, UNP, LOW)", DISCOVERY), ("out of sample (the eight newer tickers)", TEST), ("all eleven", ALL))
PE_NOW = re.compile(r"^PE_NOW_PCTL\s*=\s*(\d+)\s*(?:#.*)?$", re.M)
RANGE_52W = re.compile(r"52-week range:\s+\$([\d,.]+)\s+–\s+\$([\d,.]+)")
med = statistics.median_high

# Frozen in cross_ticker.py on ACN, UNP and LOW; copied unchanged.
CHEAP_FALLING = lambda r: r["pe_pctl"] < 40 and r["chg_12m"] is not None and r["chg_12m"] <= -0.10
EXPENSIVE_RUNNING = lambda r: r["pe_pctl"] >= 80 and r["chg_12m"] is not None and r["chg_12m"] > 0.25
CRASH = lambda r: r["dd_52w"] <= -0.40 or (r["chg_12m"] is not None and r["chg_12m"] <= -0.25)
FELL_12M = lambda r: r["chg_12m"] is not None and r["chg_12m"] <= -0.10


def splits(t):
    path = os.path.join(ROOT, "retro", "facts", f"{t}.json")
    if not os.path.exists(path):
        return []
    return [(dt.date.fromisoformat(s["effective"]), s["ratio"]) for s in json.load(open(path)).get("splits", [])]


def load():
    rows = []
    for t in ALL:
        base = os.path.join(ROOT, SERIES[t])
        for d in sorted(x for x in os.listdir(base) if re.match(r"\d{4}-\d{2}-\d{2}$", x)):
            f = os.path.join(base, d)
            a = json.load(open(os.path.join(f, "analysis.json")))
            found = PE_NOW.findall(open(os.path.join(f, "model.py"), encoding="utf-8").read())
            assert len(found) == 1, f"{t} {d}: expected one PE_NOW_PCTL literal, found {len(found)}"
            hi = float(RANGE_52W.search(open(os.path.join(f, "report.txt"), encoding="utf-8").read()).group(2).replace(",", ""))
            o = json.load(open(os.path.join(f, "outcome.json"))) if os.path.exists(os.path.join(f, "outcome.json")) else {}
            r = {"ticker": t, "as_of": d, "date": dt.date.fromisoformat(d), "year": int(d[:4]), "price": a["price"],
                 "class": a["classification"]["price_state"], "tier": a["legacy_signal_short"],
                 "kind": a["classification"]["business_kind"], "pe_pctl": int(found[0]), "dd_52w": a["price"] / hi - 1,
                 "above_base": a["price"] >= a["metrics"]["scenarios"]["BASE"]["price"]}
            for k, h in o.get("horizons", {}).items():
                r[f"tr_{k}"], r[f"ex_{k}"], r[f"hurdle_{k}"] = h["total_return_pct"], h["excess_pct"], h["hurdle_pct"]
                r[f"spy_{k}"] = h["benchmark_total_return_pct"]
            r["mdd_2y"] = (o.get("within_2y") or {}).get("max_drawdown_pct")
            rows.append(r)
    for t in ALL:
        sp = splits(t)
        ds = [r for r in rows if r["ticker"] == t]
        by_date = {r["date"]: r for r in ds}
        for r in ds:
            target = r["date"] - dt.timedelta(days=364)
            near = [by_date[target + dt.timedelta(days=k)] for k in sorted(range(-6, 7), key=abs) if target + dt.timedelta(days=k) in by_date]
            r1 = near[0] if near else None
            if r1 is None or r1["date"] >= r["date"]:
                r["chg_12m"] = None
                continue
            ratio = math.prod(x for e, x in sp if r1["date"] < e <= r["date"])
            r["chg_12m"] = r["price"] / (r1["price"] / ratio) - 1
    # point-in-time breadth: the share of the tickers listed that ISO week whose own 12-month change was -10% or worse
    by_week = defaultdict(list)
    for r in rows:
        if r["chg_12m"] is not None:
            by_week[r["date"].isocalendar()[:2]].append(r)
    for r in rows:
        w = by_week.get(r["date"].isocalendar()[:2])
        r["breadth_down"] = sum(FELL_12M(x) for x in w) / len(w) if w else None
    return rows


R = load()
SCORED = [r for r in R if "tr_2y" in r]
BASE = {t: med([r["tr_2y"] for r in SCORED if r["ticker"] == t]) for t in ALL}
MARKET_WIDE = lambda r: r["breadth_down"] is not None and r["breadth_down"] >= 0.5


def of(ts, f=lambda r: True):
    return [r for r in R if r["ticker"] in ts and f(r)]


def episodes(rs, gap=21):
    n = 0
    for t in ALL:
        prev = None
        for d in sorted(r["date"] for r in rs if r["ticker"] == t):
            n += prev is None or (d - prev).days > gap
            prev = d
    return n


def pct(v, unit="%"):
    return f"{v:+.0f}{unit}" if v is not None else "-"


def share(rs, f):
    return f"{100 * sum(map(f, rs)) / len(rs):.0f}%"


def table(title, groups, per=None):
    """per: tickers whose own 2y median minus their own base is printed in a last column (dates in brackets)."""
    print(f"\n### {title}\n")
    print("| Group | Dates | Episodes | Median 2y | Median 3y | 2y vs SPY | Beat SPY | Lost money (2y) | Median drawdown | "
          "2y vs own base | Beat own base |" + (f" {' / '.join(per)}: 2y vs own base (dates) |" if per else ""))
    print("|---" * (11 + bool(per)) + "|")
    for name, rs in groups:
        s = [r for r in rs if "tr_2y" in r]
        if not s:
            print(f"| {name} | 0 |" + " |" * (9 + bool(per)))
            continue
        s3 = [r["tr_3y"] for r in rs if "tr_3y" in r]
        line = (f"| {name} | {len(s)} | {episodes(s)} | {pct(med([r['tr_2y'] for r in s]))} | {pct(med(s3) if s3 else None)} | "
                f"{pct(med([r['ex_2y'] for r in s]), 'pp')} | {share(s, lambda r: r['ex_2y'] > 0)} | {share(s, lambda r: r['tr_2y'] < 0)} | "
                f"{pct(med([r['mdd_2y'] for r in s if r['mdd_2y'] is not None]))} | "
                f"{pct(med([r['tr_2y'] - BASE[r['ticker']] for r in s]), 'pp')} | {share(s, lambda r: r['tr_2y'] > BASE[r['ticker']])} |")
        if per:
            line += " " + " / ".join(f"{pct(med([r['tr_2y'] for r in s if r['ticker'] == t]) - BASE[t], '')} ({sum(r['ticker'] == t for r in s)})"
                                     if any(r["ticker"] == t for r in s) else "-" for t in per) + " |"
        print(line)


def spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=v.__getitem__)
        rk, i = [0.0] * len(v), 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                rk[order[k]] = (i + j) / 2
            i = j + 1
        return rk
    a, b = rank(xs), rank(ys)
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / den if den else 0.0


def section_base():
    print("\n### Each ticker's base (median two-year total return over all its scored dates)\n")
    print("| Ticker | Set | Dates | With a 2y outcome | Base 2y | Median 3y | SPY 2y, same dates | Beat SPY (2y) | Lost money (2y) |")
    print("|---|---|---|---|---|---|---|---|---|")
    for t in ALL:
        s = [r for r in SCORED if r["ticker"] == t]
        s3 = [r["tr_3y"] for r in R if r["ticker"] == t and "tr_3y" in r]
        print(f"| {t} | {'discovery' if t in DISCOVERY else 'test'} | {sum(r['ticker'] == t for r in R)} | {len(s)} | {pct(BASE[t])} | "
              f"{pct(med(s3))} | {pct(med([r['spy_2y'] for r in s]))} | {share(s, lambda r: r['ex_2y'] > 0)} | {share(s, lambda r: r['tr_2y'] < 0)} |")
    print(f"\n{len(R)} dates, {len(SCORED)} with a two-year outcome ({min(r['as_of'] for r in SCORED)} to {max(r['as_of'] for r in SCORED)}).")


def section_zones():
    for label, ts in SETS:
        rest = of(ts, lambda r: r["chg_12m"] is not None and not CHEAP_FALLING(r) and not EXPENSIVE_RUNNING(r))
        table(f"The frozen zones, {label}",
              [("cheap & falling", of(ts, CHEAP_FALLING)),
               ("  without crash dates", of(ts, lambda r: CHEAP_FALLING(r) and not CRASH(r))),
               ("expensive & running", of(ts, EXPENSIVE_RUNNING)),
               ("crash entries", of(ts, CRASH)),
               ("every other date with a 12m history", rest),
               ("all dates", of(ts))], per=ts if ts != ALL else None)
    ex = tuple(t for t in TEST if t != "NKE")
    table("Out of sample without NKE", [("cheap & falling", of(ex, CHEAP_FALLING)), ("crash entries", of(ex, CRASH)),
                                        ("expensive & running", of(ex, EXPENSIVE_RUNNING)), ("all dates", of(ex))])


def section_per():
    print("\n### Per ticker: 2y median minus the ticker's own base (dates with a 2y outcome, share that lost money over two years)\n")
    cols = (("Cheap & falling", CHEAP_FALLING), ("Expensive & running", EXPENSIVE_RUNNING), ("Crash", CRASH),
            ("Class CHEAP", lambda r: r["class"] == "CHEAP"), ("Class RICH", lambda r: r["class"] == "RICH"),
            ("Price below BASE", lambda r: not r["above_base"]), ("Price at or above BASE", lambda r: r["above_base"]))
    print("| Ticker | Base 2y | " + " | ".join(c for c, _ in cols) + " |\n|---|---|" + "---|" * len(cols))
    for t in ALL:
        cells = []
        for _, f in cols:
            s = [r for r in SCORED if r["ticker"] == t and f(r)]
            cells.append(f"{pct(med([r['tr_2y'] for r in s]) - BASE[t], 'pp')} ({len(s)}, {share(s, lambda r: r['tr_2y'] < 0)})" if s else "-")
        print(f"| {t} | {pct(BASE[t])} | " + " | ".join(cells) + " |")


def section_single():
    for label, ts in SETS[1:]:
        table(f"Own 10-year P/E percentile alone, {label}",
              [(f"percentile {a}-{b - 1}", of(ts, lambda r, a=a, b=b: a <= r["pe_pctl"] < b))
               for a, b in ((0, 20), (20, 40), (40, 60), (60, 80), (80, 90), (90, 101))])
        table(f"Trailing 12-month price change alone, {label}",
              [(name, of(ts, lambda r, lo=lo, hi=hi: r["chg_12m"] is not None and lo < r["chg_12m"] <= hi))
               for name, lo, hi in (("-25% or worse", -9, -0.25), ("-25% to -10%", -0.25, -0.10), ("-10% to +10%", -0.10, 0.10),
                                    ("+10% to +25%", 0.10, 0.25), ("+25% to +50%", 0.25, 0.50), ("above +50%", 0.50, 9))])
        table(f"Distance below the 52-week high, {label}",
              [(name, of(ts, lambda r, lo=lo, hi=hi: lo < r["dd_52w"] <= hi))
               for name, lo, hi in (("40% or more below", -9, -0.40), ("30-40% below", -0.40, -0.30), ("20-30% below", -0.30, -0.20),
                                    ("10-20% below", -0.20, -0.10), ("5-10% below", -0.10, -0.05), ("within 5%", -0.05, 1))],
              per=ts if ts == TEST else None)


def section_grid():
    for label, ts in SETS[1:]:
        groups = []
        for vn, a, b in (("pctl < 40", 0, 40), ("pctl 40-79", 40, 80), ("pctl >= 80", 80, 101)):
            for cn, lo, hi in (("12m <= -10%", -9, -0.10), ("12m -10% to +10%", -0.10, 0.10), ("12m +10% to +25%", 0.10, 0.25), ("12m > +25%", 0.25, 9)):
                groups.append((f"{vn}, {cn}", of(ts, lambda r, a=a, b=b, lo=lo, hi=hi: a <= r["pe_pctl"] < b and r["chg_12m"] is not None and lo < r["chg_12m"] <= hi)))
        table(f"Own P/E percentile x trailing 12-month price change, {label}", groups)


def section_house():
    for label, ts in SETS:
        table(f"The house class, tier and BASE price, {label}",
              [(f"class {c}", of(ts, lambda r, c=c: r["class"] == c)) for c in ("CHEAP", "FAIR", "RICH")] +
              [("price below the BASE price", of(ts, lambda r: not r["above_base"])), ("price at or above the BASE price", of(ts, lambda r: r["above_base"]))] +
              [(f"tier {c}", of(ts, lambda r, c=c: r["tier"] == c)) for c in ("BUY", "ACCUMULATE", "WATCHLIST", "AVOID")])


def section_rank():
    print("\n### Within each ticker's own series: rank correlation with the forward total return (sign set so + = lower did better)\n")
    keys = (("own P/E pctl", "pe_pctl"), ("12m change", "chg_12m"), ("52w high distance", "dd_52w"))
    hs = ("1y", "2y", "3y")
    print("| Ticker | " + " | ".join(f"{n} {h}" for n, _ in keys for h in hs) + " |\n|---|" + "---|" * 9)
    pos = Counter()
    for t in ALL:
        cells = []
        for n, k in keys:
            for h in hs:
                s = [r for r in R if r["ticker"] == t and f"tr_{h}" in r and r[k] is not None]
                v = -spearman([r[k] for r in s], [r[f"tr_{h}"] for r in s])
                pos[(n, h)] += v > 0
                cells.append(f"{v:+.2f}")
        print(f"| {t} | " + " | ".join(cells) + " |")
    print("| positive in | " + " | ".join(f"{pos[(n, h)]} of {len(ALL)}" for n, _ in keys for h in hs) + " |")


def section_xrank():
    """The same calendar week across tickers: removes the market's path, which every stock shares that week."""
    by_week = defaultdict(list)
    for r in SCORED:
        by_week[r["date"].isocalendar()[:2]].append(r)
    groups = (("own P/E pctl < 40", lambda r: r["pe_pctl"] < 40), ("own P/E pctl >= 80", lambda r: r["pe_pctl"] >= 80),
              ("12m change <= -10%", FELL_12M), ("12m change > +25%", lambda r: r["chg_12m"] is not None and r["chg_12m"] > 0.25),
              ("cheap & falling", CHEAP_FALLING), ("expensive & running", EXPENSIVE_RUNNING), ("crash entries", CRASH),
              ("class CHEAP", lambda r: r["class"] == "CHEAP"), ("class RICH", lambda r: r["class"] == "RICH"))
    for label, ts in SETS[1:]:
        acc, ic = defaultdict(list), defaultdict(list)
        weeks = 0
        for rs in by_week.values():
            rs = [r for r in rs if r["ticker"] in ts]
            if len(rs) < 6:
                continue
            weeks += 1
            order = sorted(rs, key=lambda r: r["tr_2y"])
            place = {id(r): i / (len(order) - 1) for i, r in enumerate(order)}
            for name, f in groups:
                acc[name] += [(place[id(r)], r["ticker"]) for r in rs if f(r)]
            for n, k in (("own P/E pctl", "pe_pctl"), ("12m change", "chg_12m"), ("52w high distance", "dd_52w")):
                v = [r for r in rs if r[k] is not None]
                if len(v) >= 6:
                    ic[n].append(-spearman([r[k] for r in v], [r["tr_2y"] for r in v]))
        print(f"\n### The same week across tickers, {label} ({weeks} weeks with six or more tickers scored)\n")
        print("Each week the tickers are ranked by their two-year return: 0.00 the worst that week, 1.00 the best, 0.50 the middle.\n")
        print("| Group | Stock-weeks | Mean place | In the top half | Most frequent tickers |\n|---|---|---|---|---|")
        for name, _ in groups:
            v = acc[name]
            print(f"| {name} | {len(v)} | {statistics.fmean(x for x, _ in v):.2f} | {100 * sum(x > 0.5 for x, _ in v) / len(v):.0f}% | "
                  f"{', '.join(f'{t} {n}' for t, n in Counter(t for _, t in v).most_common(4))} |")
        print("\n| Weekly rank correlation with the 2y return (+ = lower did better) | Weeks | Mean | Weeks above zero |\n|---|---|---|---|")
        for n, v in ic.items():
            print(f"| {n} | {len(v)} | {statistics.fmean(v):+.2f} | {100 * sum(x > 0 for x in v) / len(v):.0f}% |")


def section_breadth():
    for label, ts in SETS:
        table(f"Market-wide against stock-specific declines, {label} (market-wide: at least half the tickers listed that week "
              "were down 10% or more over 12 months)",
              [("cheap & falling, market-wide", of(ts, lambda r: CHEAP_FALLING(r) and MARKET_WIDE(r))),
               ("cheap & falling, stock-specific", of(ts, lambda r: CHEAP_FALLING(r) and not MARKET_WIDE(r))),
               ("crash, market-wide", of(ts, lambda r: CRASH(r) and MARKET_WIDE(r))),
               ("crash, stock-specific", of(ts, lambda r: CRASH(r) and not MARKET_WIDE(r))),
               ("12m change <= -10%, market-wide", of(ts, lambda r: FELL_12M(r) and MARKET_WIDE(r))),
               ("12m change <= -10%, stock-specific", of(ts, lambda r: FELL_12M(r) and not MARKET_WIDE(r))),
               ("any date in a market-wide week", of(ts, MARKET_WIDE))])


def section_quarter():
    seen, q = set(), []
    for r in sorted(SCORED, key=lambda r: (r["ticker"], r["as_of"])):
        k = (r["ticker"], r["as_of"][:4], (int(r["as_of"][5:7]) - 1) // 3)
        if k not in seen and r["chg_12m"] is not None:
            seen.add(k)
            q.append(r)
    for label, ts in SETS:
        print(f"\n### One date per quarter (the first scored date of each quarter with a 12m history), {label}\n")
        print("| Zone | Dates | Median 2y | 2y vs own base | Beat own base | Beat SPY | Lost money (2y) |\n|---|---|---|---|---|---|---|")
        for name, f in (("cheap & falling", CHEAP_FALLING), ("expensive & running", EXPENSIVE_RUNNING), ("crash entries", CRASH),
                        ("every other date", lambda r: not CHEAP_FALLING(r) and not EXPENSIVE_RUNNING(r))):
            s = [r for r in q if r["ticker"] in ts and f(r)]
            if s:
                print(f"| {name} | {len(s)} | {pct(med([r['tr_2y'] for r in s]))} | {pct(med([r['tr_2y'] - BASE[r['ticker']] for r in s]), 'pp')} | "
                      f"{share(s, lambda r: r['tr_2y'] > BASE[r['ticker']])} | {share(s, lambda r: r['ex_2y'] > 0)} | {share(s, lambda r: r['tr_2y'] < 0)} |")


def section_composition():
    for name, f in (("Crash entries", CRASH), ("Cheap & falling", CHEAP_FALLING)):
        g = defaultdict(list)
        for r in of(TEST, f):
            g[(r["ticker"], r["year"])].append(r)
        print(f"\n### {name}, out of sample, by ticker and year\n")
        print("| Ticker | Year | Dates (with 2y outcome) | First - last | Median 2y | 2y vs SPY | 2y vs own base | Median 3y | Kind |")
        print("|---|---|---|---|---|---|---|---|---|")
        for (t, y), v in sorted(g.items()):
            s2 = [r for r in v if "tr_2y" in r]
            s3 = [r["tr_3y"] for r in v if "tr_3y" in r]
            m2 = med([r["tr_2y"] for r in s2]) if s2 else None
            print(f"| {t} | {y} | {len(v)} ({len(s2)}) | {v[0]['as_of']} - {v[-1]['as_of']} | {pct(m2) if s2 else 'not yet'} | "
                  f"{pct(med([r['ex_2y'] for r in s2]), 'pp') if s2 else '-'} | {pct(m2 - BASE[t], 'pp') if s2 else '-'} | "
                  f"{pct(med(s3)) if s3 else '-'} | {', '.join(f'{k} {n}' for k, n in sorted(Counter(r['kind'] for r in v).items()))} |")


def section_latest():
    print("\n### The newest date of each ticker (point-in-time values; the zones are hindsight hypotheses, not model output)\n")
    print("| Ticker | As of | Price | Own P/E pctl | 12m change | Below 52w high | Zone | House class / tier | Kind |\n|---|---|---|---|---|---|---|---|---|")
    for t in ALL:
        r = [x for x in R if x["ticker"] == t][-1]
        zone = ", ".join(n for n, f in (("cheap & falling", CHEAP_FALLING), ("expensive & running", EXPENSIVE_RUNNING), ("crash", CRASH)) if f(r)) or "none"
        print(f"| {t} | {r['as_of']} | ${r['price']:.2f} | {r['pe_pctl']} | {pct(r['chg_12m'] * 100)} | {pct(r['dd_52w'] * 100)} | {zone} | "
              f"{r['class']} / {r['tier']} | {r['kind']} |")


SECTIONS = {"base": section_base, "zones": section_zones, "per": section_per, "single": section_single, "grid": section_grid,
            "house": section_house, "rank": section_rank, "xrank": section_xrank, "breadth": section_breadth,
            "quarter": section_quarter, "composition": section_composition, "latest": section_latest}

if __name__ == "__main__":
    print(f"HINDSIGHT. {len(R)} dates across {len(ALL)} tickers; {len(SCORED)} with a two-year outcome. "
          f"Discovery set {', '.join(DISCOVERY)}; out-of-sample set {', '.join(TEST)}.")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
