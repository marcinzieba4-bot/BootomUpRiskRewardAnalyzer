#!/usr/bin/env python3
"""
HINDSIGHT: pool the ACN, UNP and LOW retrospectives and print the cross-ticker tables quoted in
staging/retrospective/CROSS_TICKER_FINDINGS.md.

Reads only what is already in the repo and writes nothing. Each row joins one date's point-in-time values
(analysis.json, model.py literals parsed with ast and never executed, report.txt's 52-week range) with its
outcome.json. The patterns it prints are labels and hypotheses: nothing here may enter a model, a fact sheet,
a builder or a method rule (retro/README.md, "The one rule").

    python3 staging/retrospective/cross_ticker.py              # every table
    python3 staging/retrospective/cross_ticker.py zones grid   # selected sections

Sections: base class risk pctl horizon zones grid composition crash spy landing rank tried latest
Medians of an even count take the upper middle value (statistics.median_high), as in the FINDINGS files.
"""
import ast
import datetime as dt
import json
import math
import os
import re
import statistics
import sys
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SERIES = {"ACN": "archive/retrospective/ACN", "UNP": "staging/retrospective/UNP", "LOW": "staging/retrospective/LOW"}
SPLITS = {"ACN": [], "UNP": [dt.date(2008, 5, 29), dt.date(2014, 6, 9)], "LOW": []}   # 2-for-1 splits inside the series
LITERALS = {"PE_PCTL", "PE_NOW_PCTL", "EPS_NORM", "EPP_TODAY_EPS", "EPS_LABEL"}
RANGE_52W = re.compile(r"52-week range:\s+\$([\d,.]+)\s+–\s+\$([\d,.]+)")
HORIZONS = {"6m": 0.5, "1y": 1, "2y": 2, "3y": 3}
T = tuple(SERIES)
med = statistics.median_high

# The two zones: the stock's own 10-year P/E percentile read together with its trailing 12-month price change.
CHEAP_FALLING = lambda r: r["pe_pctl"] < 40 and r["chg_12m"] is not None and r["chg_12m"] <= -0.10
EXPENSIVE_RUNNING = lambda r: r["pe_pctl"] >= 80 and r["chg_12m"] is not None and r["chg_12m"] > 0.25
CRASH = lambda r: r["dd_52w"] <= -0.40 or (r["chg_12m"] is not None and r["chg_12m"] <= -0.25)


def model_literals(path):
    out = {}
    for node in ast.parse(open(path, encoding="utf-8").read()).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and getattr(node.targets[0], "id", None) in LITERALS:
            out[node.targets[0].id] = ast.literal_eval(node.value)
    return out


def load():
    rows = []
    for t, rel in SERIES.items():
        base = os.path.join(ROOT, rel)
        for d in sorted(x for x in os.listdir(base) if re.match(r"\d{4}-\d{2}-\d{2}$", x)):
            f = os.path.join(base, d)
            a = json.load(open(os.path.join(f, "analysis.json")))
            m = model_literals(os.path.join(f, "model.py"))
            hi = float(RANGE_52W.search(open(os.path.join(f, "report.txt"), encoding="utf-8").read()).group(2).replace(",", ""))
            o = json.load(open(os.path.join(f, "outcome.json"))) if os.path.exists(os.path.join(f, "outcome.json")) else {}
            hist = {int(y): v for y, v in m["EPS_NORM"].items()}
            last = max(hist)
            sc = a["metrics"]["scenarios"]
            band = next(name for name, edge in (("below BEAR", "BEAR"), ("BEAR to BASE", "BASE"), ("BASE to BULL", "BULL"))
                        if a["price"] < sc[edge]["price"]) if a["price"] < sc["BULL"]["price"] else "above BULL"
            r = {"ticker": t, "as_of": d, "year": int(d[:4]), "price": a["price"],
                 "class": a["classification"]["price_state"], "tier": a["legacy_signal_short"],
                 "kind": a["classification"]["business_kind"], "proxy": a["metrics"]["proxy_composite"],
                 "ratio_b": a["metrics"]["ratio_b"], "adj_gap": a["metrics"]["adj_gap"], "epp_gap": a["metrics"]["epp_gap_pct"],
                 "pe_pctl": m["PE_NOW_PCTL"], "pe_vs_median": a["price"] / m["EPP_TODAY_EPS"] / m["PE_PCTL"]["median"],
                 "eps_guided": "no numeric EPS guide" not in m.get("EPS_LABEL", ""),
                 "eps_cycle": ("last year down" if hist.get(last - 1, 0) > 0 and hist[last] < hist[last - 1] else
                               "up, below the old peak" if hist[last] < max(v for y, v in hist.items() if y < last) else "a record"),
                 "dd_52w": a["price"] / hi - 1, "band": band,
                 "base_growth": (sc["BASE"]["eps"] / m["EPP_TODAY_EPS"]) ** 0.5 - 1 if sc["BASE"]["eps"] > 0 else None,
                 "landing": o.get("scenario_landing_2y")}
            for k, h in o.get("horizons", {}).items():
                r[f"tr_{k}"], r[f"ex_{k}"], r[f"hurdle_{k}"] = h["total_return_pct"], h["excess_pct"], h["hurdle_pct"]
                r[f"spy_{k}"] = h["benchmark_total_return_pct"]
            r["mdd_2y"] = (o.get("within_2y") or {}).get("max_drawdown_pct")
            rows.append(r)
    # trailing 12-month price change from the weekly series itself: prices public by AS_OF, on the as-of share basis
    for t in T:
        ds = [(dt.date.fromisoformat(r["as_of"]), r) for r in rows if r["ticker"] == t]
        for d0, r in ds:
            d1, r1 = min(ds, key=lambda x: abs((x[0] - (d0 - dt.timedelta(days=364))).days))
            ok = d1 < d0 and abs((d1 - (d0 - dt.timedelta(days=364))).days) <= 6
            r["chg_12m"] = r["price"] / (r1["price"] / 2 ** sum(d1 < s <= d0 for s in SPLITS[t])) - 1 if ok else None
    return rows


R = load()
SCORED = [r for r in R if "tr_2y" in r]
BASE = {t: med([r["tr_2y"] for r in SCORED if r["ticker"] == t]) for t in T}


def episodes(rs, gap=21):
    n = 0
    for t in T:
        prev = None
        for d in sorted(dt.date.fromisoformat(r["as_of"]) for r in rs if r["ticker"] == t):
            n += prev is None or (d - prev).days > gap
            prev = d
    return n


def pct(v, unit="%"):
    return f"{v:+.0f}{unit}" if v is not None else "-"


def table(title, groups):
    print(f"\n### {title}\n")
    print("| Group | Dates | Episodes | Median 1y | Median 2y | Median 3y | 2y vs SPY | Cleared hurdle | Beat SPY | "
          "Lost money (2y) | Median drawdown | 2y vs ticker base | ACN / UNP / LOW 2y (dates) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for name, rs in groups:
        s = [r for r in rs if "tr_2y" in r]
        if not s:
            print(f"| {name} | 0 | | | | | | | | | | | |")
            continue
        m3 = [r["tr_3y"] for r in rs if "tr_3y" in r]
        m1 = [r["tr_1y"] for r in rs if "tr_1y" in r]
        per = " / ".join(f"{pct(med([r['tr_2y'] for r in s if r['ticker'] == t]))} ({sum(r['ticker'] == t for r in s)})"
                         if any(r["ticker"] == t for r in s) else "-" for t in T)
        print(f"| {name} | {len(s)} | {episodes(s)} | {pct(med(m1) if m1 else None)} | {pct(med([r['tr_2y'] for r in s]))} | "
              f"{pct(med(m3) if m3 else None)} | {pct(med([r['ex_2y'] for r in s]), 'pp')} | "
              f"{100 * sum(r['tr_2y'] >= r['hurdle_2y'] for r in s) / len(s):.0f}% | {100 * sum(r['ex_2y'] > 0 for r in s) / len(s):.0f}% | "
              f"{100 * sum(r['tr_2y'] < 0 for r in s) / len(s):.0f}% | {pct(med([r['mdd_2y'] for r in s]))} | "
              f"{pct(med([r['tr_2y'] - BASE[r['ticker']] for r in s]), 'pp')} | {per} |")


def spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=v.__getitem__)
        rk = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                rk[order[k]] = (i + j) / 2
            i = j + 1
        return rk
    a, b = rank(xs), rank(ys)
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    return cov / math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))


def by_ticker_year(title, rs):
    g = defaultdict(list)
    for r in rs:
        g[(r["ticker"], r["year"])].append(r)
    print(f"\n### {title}\n")
    print("| Ticker | Year | Dates (with 2y outcome) | First - last | Median 2y | Median 3y | 2y vs SPY | Ticker base 2y | House class |")
    print("|---|---|---|---|---|---|---|---|---|")
    for (t, y), v in sorted(g.items()):
        s2 = [r["tr_2y"] for r in v if "tr_2y" in r]; s3 = [r["tr_3y"] for r in v if "tr_3y" in r]
        print(f"| {t} | {y} | {len(v)} ({len(s2)}) | {min(r['as_of'] for r in v)} - {max(r['as_of'] for r in v)} | "
              f"{pct(med(s2)) if s2 else 'not yet'} | {pct(med(s3)) if s3 else 'not yet'} | "
              f"{pct(med([r['ex_2y'] for r in v if 'ex_2y' in r]), 'pp') if s2 else '-'} | {pct(BASE[t])} | "
              f"{'/'.join(f'{c} {n}' for c, n in sorted(Counter(r['class'] for r in v).items()))} |")


def section_base():
    table("Every scored date, and each ticker's base", [("all", R)] + [(t, [r for r in R if r["ticker"] == t]) for t in T])


def section_class():
    table("The house class and legacy tier, pooled", [(f"class {c}", [r for r in R if r["class"] == c]) for c in ("CHEAP", "FAIR", "RICH")]
          + [(f"tier {c}", [r for r in R if r["tier"] == c]) for c in ("BUY", "ACCUMULATE", "WATCHLIST", "AVOID")])


def section_pctl():
    table("Own 10-year P/E percentile alone", [(f"percentile {a}-{b - 1}", [r for r in R if a <= r["pe_pctl"] < b])
                                               for a, b in ((0, 20), (20, 40), (40, 60), (60, 80), (80, 90), (90, 101))])
    groups = []
    for vn, a, b in (("pctl < 40", 0, 40), ("pctl 40-79", 40, 80), ("pctl >= 80", 80, 101)):
        for cn, lo, hi in (("12m <= -10%", -9, -0.10), ("12m -10% to +10%", -0.10, 0.10), ("12m +10% to +25%", 0.10, 0.25), ("12m > +25%", 0.25, 9)):
            groups.append((f"{vn}, {cn}", [r for r in R if a <= r["pe_pctl"] < b and r["chg_12m"] is not None and lo < r["chg_12m"] <= hi]))
    table("Own P/E percentile x trailing 12-month price change (from 2009)", groups)


def section_risk():
    print("\n### Share of dates that lost money over two years (median drawdown inside the two years), per ticker\n")
    print("| Group | ACN | UNP | LOW |\n|---|---|---|---|")
    for name, f in (("class CHEAP", lambda r: r["class"] == "CHEAP"), ("class FAIR", lambda r: r["class"] == "FAIR"),
                    ("class RICH", lambda r: r["class"] == "RICH"), ("tier BUY", lambda r: r["tier"] == "BUY"),
                    ("tier AVOID", lambda r: r["tier"] == "AVOID"),
                    ("price below the BASE scenario price", lambda r: r["band"] in ("below BEAR", "BEAR to BASE")),
                    ("price above the BASE scenario price", lambda r: r["band"] in ("BASE to BULL", "above BULL")),
                    ("cheap & falling", CHEAP_FALLING), ("expensive & running", EXPENSIVE_RUNNING)):
        cells = []
        for t in T:
            s = [r for r in SCORED if r["ticker"] == t and f(r)]
            cells.append(f"{100 * sum(r['tr_2y'] < 0 for r in s) / len(s):.0f}% of {len(s)} ({pct(med([r['mdd_2y'] for r in s]))})" if s else "-")
        print(f"| {name} | " + " | ".join(cells) + " |")
    lost = [r for r in SCORED if r["tr_2y"] < 0]
    print(f"\n{len(lost)} dates lost money over two years: {sum(r['class'] == 'RICH' for r in lost)} were class RICH and "
          f"{sum(r['band'] in ('BASE to BULL', 'above BULL') for r in lost)} had a price above the BASE scenario price.")
    years = Counter((r["ticker"], r["year"]) for r in lost)
    print("\nLosing dates by start year: " + ", ".join(f"{t} {y} ({n})" for (t, y), n in sorted(years.items())) + ".")


def section_horizon():
    zones = [("own pctl < 40", lambda r: r["pe_pctl"] < 40), ("own pctl >= 80", lambda r: r["pe_pctl"] >= 80),
             ("cheap & falling", CHEAP_FALLING), ("expensive & running", EXPENSIVE_RUNNING),
             ("house class CHEAP", lambda r: r["class"] == "CHEAP"), ("house class RICH", lambda r: r["class"] == "RICH"),
             ("all dates", lambda r: True)]
    print("\n### Median total return per year, and median excess vs SPY (not annualized), by horizon\n")
    print("| Zone | " + " | ".join(f"{h} /yr" for h in HORIZONS) + " | " + " | ".join(f"{h} vs SPY" for h in HORIZONS) + " |")
    print("|---|" + "---|" * 8)
    for name, f in zones:
        ann, exc = [], []
        for h, yrs in HORIZONS.items():
            s = [r for r in R if f(r) and f"tr_{h}" in r]
            ann.append(f"{((1 + med([r[f'tr_{h}'] for r in s]) / 100) ** (1 / yrs) - 1) * 100:+.1f}%")
            exc.append(pct(med([r[f"ex_{h}"] for r in s]), "pp"))
        print(f"| {name} | " + " | ".join(ann) + " | " + " | ".join(exc) + " |")


def section_zones():
    rest = [r for r in R if r["chg_12m"] is not None and not CHEAP_FALLING(r) and not EXPENSIVE_RUNNING(r)]
    cf = [r for r in R if CHEAP_FALLING(r)]
    table("The two zones (own P/E percentile < 40 and 12m change <= -10%; >= 80 and > +25%)",
          [("cheap & falling", cf), ("  without crash dates", [r for r in cf if not CRASH(r)]),
           ("  house class RICH inside it", [r for r in cf if r["class"] == "RICH"]),
           ("expensive & running", [r for r in R if EXPENSIVE_RUNNING(r)]), ("every other date from 2009", rest)])
    cf2 = [r for r in cf if "tr_2y" in r]
    rich = [r for r in cf2 if r["class"] == "RICH" and r["base_growth"] is not None]
    print(f"\nInside cheap & falling (dates with a 2-year outcome) the house class read RICH on {len(rich)} of {len(cf2)} dates "
          f"(median BASE growth {med([r['base_growth'] for r in rich]) * 100:+.0f}%/yr, proxy composite {med([r['proxy'] for r in rich]):.2f}); "
          f"the legacy tier read BUY on {sum(r['tier'] == 'BUY' for r in cf2)}. Kinds on those dates: {dict(Counter(r['kind'] for r in cf2))}.")
    for name, f in (("cheap & falling", CHEAP_FALLING), ("expensive & running", EXPENSIVE_RUNNING)):
        s3 = [r for r in R if f(r) and "tr_3y" in r]
        print(f"{name}: {sum(r['tr_3y'] < 0 for r in s3)} of {len(s3)} dates lost money over three years.")
    new = [r for r in cf if "tr_2y" not in r and r["ticker"] == "ACN"]
    one = [r for r in new if "tr_1y" in r]
    print(f"\nACN cheap & falling without a 2-year outcome: {len(new)} dates, {new[0]['as_of']} to {new[-1]['as_of']}; "
          f"{len(one)} with a 1-year outcome ({dict(Counter(r['kind'] for r in one))}): median {pct(med([r['tr_1y'] for r in one]))} "
          f"({pct(min(r['tr_1y'] for r in one))} to {pct(max(r['tr_1y'] for r in one))}), median {pct(med([r['ex_1y'] for r in one]), 'pp')} "
          f"vs SPY, {sum(r['ex_1y'] > 0 for r in one)} beat SPY.")
    seen, q = set(), []
    for r in sorted(SCORED, key=lambda r: (r["ticker"], r["as_of"])):
        k = (r["ticker"], r["as_of"][:4], (int(r["as_of"][5:7]) - 1) // 3)
        if k not in seen and r["chg_12m"] is not None:
            seen.add(k); q.append(r)
    print("\nOne date per quarter (the first scored date of each quarter, from 2009), to thin the overlap:\n")
    print("| Zone | Dates | Median 2y | Cleared hurdle | Lost money (2y) |\n|---|---|---|---|---|")
    for name, f in (("cheap & falling", CHEAP_FALLING), ("expensive & running", EXPENSIVE_RUNNING),
                    ("every other date", lambda r: not CHEAP_FALLING(r) and not EXPENSIVE_RUNNING(r))):
        s = [r for r in q if f(r)]
        print(f"| {name} | {len(s)} | {pct(med([r['tr_2y'] for r in s]))} | {100 * sum(r['tr_2y'] >= r['hurdle_2y'] for r in s) / len(s):.0f}% | "
              f"{100 * sum(r['tr_2y'] < 0 for r in s) / len(s):.0f}% |")


def section_grid():
    print("\n### Threshold grid (2y median; lost-money share; each ticker's 2y median minus its base, ACN / UNP / LOW)\n")
    print("| Rule | Dates | Episodes | Median 2y | Lost money | vs base ACN / UNP / LOW |\n|---|---|---|---|---|---|")
    rules = [(f"pctl < {p}, 12m <= {c:+.0%}", lambda r, p=p, c=c: r["pe_pctl"] < p and r["chg_12m"] is not None and r["chg_12m"] <= c)
             for p in (30, 40, 50) for c in (0.0, -0.10, -0.20)]
    rules += [(f"pctl >= {p}, 12m > {c:+.0%}", lambda r, p=p, c=c: r["pe_pctl"] >= p and r["chg_12m"] is not None and r["chg_12m"] > c)
              for p in (70, 80, 90) for c in (0.15, 0.25, 0.35)]
    for name, f in rules:
        s = [r for r in SCORED if f(r)]
        vs = " / ".join(pct(med([r["tr_2y"] for r in s if r["ticker"] == t]) - BASE[t], "pp")
                        if sum(r["ticker"] == t for r in s) >= 5 else "-" for t in T)
        print(f"| {name} | {len(s)} | {episodes(s)} | {pct(med([r['tr_2y'] for r in s]))} | {100 * sum(r['tr_2y'] < 0 for r in s) / len(s):.0f}% | {vs} |")


def section_composition():
    by_ticker_year("Cheap & falling, by ticker and year", [r for r in R if CHEAP_FALLING(r)])
    by_ticker_year("Expensive & running, by ticker and year", [r for r in R if EXPENSIVE_RUNNING(r)])


def section_crash():
    table("Crash entries (>= 40% below the 52-week high, or 12m change <= -25%)", [("crash entries", [r for r in R if CRASH(r)])])
    by_ticker_year("Crash entries, by ticker and year", [r for r in R if CRASH(r)])


def section_spy():
    wk = lambda r: dt.date.fromisoformat(r["as_of"]).isocalendar()[:2]
    by = {t: {wk(r): r for r in SCORED if r["ticker"] == t} for t in T}
    common = sorted(set.intersection(*(set(v) for v in by.values())))
    print("\n### Beating SPY over two years, by start year (weeks scored for all three)\n")
    print("| Start year | SPY 2y median | ACN beat SPY | UNP beat SPY | LOW beat SPY | All three beat | All three lag |")
    print("|---|---|---|---|---|---|---|")
    for y in sorted({by["ACN"][k]["year"] for k in common}):
        ks = [k for k in common if by["ACN"][k]["year"] == y]
        cells = [f"{100 * sum(by[t][k]['ex_2y'] > 0 for k in ks) / len(ks):.0f}% ({pct(med([by[t][k]['ex_2y'] for k in ks]), 'pp')})" for t in T]
        print(f"| {y} | {pct(med([by['ACN'][k]['spy_2y'] for k in ks]))} | " + " | ".join(cells) +
              f" | {sum(all(by[t][k]['ex_2y'] > 0 for t in T) for k in ks)}/{len(ks)} | {sum(all(by[t][k]['ex_2y'] < 0 for t in T) for k in ks)}/{len(ks)} |")

    def corr(a, b):
        ma, mb = statistics.fmean(a), statistics.fmean(b)
        return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    print("\nCorrelation of the same weeks' 2-year outcomes across tickers (" + str(len(common)) + " weeks): " + "; ".join(
        f"{a}-{b} total return {corr([by[a][k]['tr_2y'] for k in common], [by[b][k]['tr_2y'] for k in common]):+.2f}, "
        f"excess vs SPY {corr([by[a][k]['ex_2y'] for k in common], [by[b][k]['ex_2y'] for k in common]):+.2f}"
        for a, b in (("ACN", "UNP"), ("ACN", "LOW"), ("UNP", "LOW"))) + ".")


def section_landing():
    print("\n### Where the 2-year price landed (nearest scenario price), by start-year era\n")
    print("| Ticker | Start years | Dates | BEAR | BASE | BULL | XBULL | BEAR or BASE | BULL or XBULL |\n|---|---|---|---|---|---|---|---|---|")
    for t in T:
        for a, b in ((2008, 2012), (2013, 2017), (2018, 2020), (2021, 2024)):
            s = [r for r in SCORED if r["ticker"] == t and a <= r["year"] <= b]
            c = Counter(r["landing"] for r in s)
            print(f"| {t} | {a}-{b} | {len(s)} | " + " | ".join(f"{100 * c[k] / len(s):.0f}%" for k in ("BEAR", "BASE", "BULL", "XBULL")) +
                  f" | {100 * (c['BEAR'] + c['BASE']) / len(s):.0f}% | {100 * (c['BULL'] + c['XBULL']) / len(s):.0f}% |")


def section_rank():
    print("\n### Rank correlation with the forward total return, within each ticker's series (sign set so + = cheaper did better;"
          " for the business dashboard + = stronger numbers did better)\n")
    print("| Measure | " + " | ".join(f"{t} {h}" for t in T for h in HORIZONS) + " |\n|---|" + "---|" * 12)
    for name, key, sign in (("own P/E percentile", "pe_pctl", -1), ("P/E vs own median", "pe_vs_median", -1), ("price vs EPP floor", "epp_gap", -1),
                            ("12m price change", "chg_12m", -1), ("Ratio B", "ratio_b", -1), ("adjusted gap", "adj_gap", 1),
                            ("business dashboard (proxy)", "proxy", 1)):
        cells = []
        for t in T:
            for h in HORIZONS:
                s = [r for r in R if r["ticker"] == t and f"tr_{h}" in r and r[key] is not None and r[key] != math.inf]
                cells.append(f"{sign * spearman([r[key] for r in s], [r[f'tr_{h}'] for r in s]):+.2f}")
        print(f"| {name} | " + " | ".join(cells) + " |")


def section_tried():
    """Partners for the valuation read that were tried and showed no consistent sign across the three tickers."""
    groups = []
    for vn, a, b in (("pctl < 40", 0, 40), ("pctl 40-79", 40, 80), ("pctl >= 80", 80, 101)):
        for c in ("last year down", "up, below the old peak", "a record"):
            groups.append((f"{vn}, EPS {c}", [r for r in R if a <= r["pe_pctl"] < b and r["eps_cycle"] == c]))
    table("Tried: own P/E percentile x the EPS cycle (the last full year against the dated history)", groups)
    cut = {t: sorted(r["proxy"] for r in R if r["ticker"] == t) for t in T}
    third = lambda r: ("weak", "mid", "strong")[sum(r["proxy"] >= cut[r["ticker"]][len(cut[r["ticker"]]) * k // 3] for k in (1, 2))]
    table("Tried: own P/E percentile x the business dashboard (each ticker's thirds of its proxy composite over the "
          "whole series, a hindsight cut)", [(f"{vn}, numbers {p}", [r for r in R if a <= r["pe_pctl"] < b and third(r) == p])
                                            for vn, a, b in (("pctl < 40", 0, 40), ("pctl 40-79", 40, 80), ("pctl >= 80", 80, 101))
                                            for p in ("weak", "mid", "strong")])
    table("Tried: the price against the house scenario prices", [(f"price {b}", [r for r in R if r["band"] == b])
                                                                 for b in ("below BEAR", "BEAR to BASE", "BASE to BULL", "above BULL")])


def section_latest():
    print("\n### The newest dates (point-in-time values; zones are hindsight hypotheses, not model output)\n")
    print("| Ticker | As of | Price | Own P/E pctl | 12m change | Zone | House class / tier | Kind |\n|---|---|---|---|---|---|---|---|")
    for t in T:
        for r in [r for r in R if r["ticker"] == t][-4:]:
            zone = "cheap & falling" if CHEAP_FALLING(r) else "expensive & running" if EXPENSIVE_RUNNING(r) else "neither"
            print(f"| {t} | {r['as_of']} | ${r['price']:.2f} | {r['pe_pctl']} | {pct(r['chg_12m'] * 100)} | {zone} | "
                  f"{r['class']} / {r['tier']} | {r['kind']} |")
    print()
    for t in T:
        for name, f in (("cheap & falling", CHEAP_FALLING), ("expensive & running", EXPENSIVE_RUNNING)):
            s = [r for r in R if r["ticker"] == t and r["year"] == 2026 and f(r)]
            if s:
                print(f"- {t} 2026, {name}: {len(s)} dates, {s[0]['as_of']} to {s[-1]['as_of']}; percentile {min(r['pe_pctl'] for r in s)}-"
                      f"{max(r['pe_pctl'] for r in s)}, 12m change {pct(min(r['chg_12m'] for r in s) * 100)} to {pct(max(r['chg_12m'] for r in s) * 100)}; "
                      f"class {dict(Counter(r['class'] for r in s))}, tier {dict(Counter(r['tier'] for r in s))}, kind {dict(Counter(r['kind'] for r in s))}")


SECTIONS = {"base": section_base, "class": section_class, "risk": section_risk, "pctl": section_pctl, "horizon": section_horizon, "zones": section_zones,
            "grid": section_grid, "composition": section_composition, "crash": section_crash, "spy": section_spy,
            "landing": section_landing, "rank": section_rank, "tried": section_tried, "latest": section_latest}

if __name__ == "__main__":
    counts = Counter(r["ticker"] for r in R)
    print(f"HINDSIGHT. {len(R)} dates ({', '.join(f'{t} {counts[t]}' for t in T)}); {len(SCORED)} with a 2-year outcome, "
          f"{min(r['as_of'] for r in SCORED)} to {max(r['as_of'] for r in SCORED)}; {sum('tr_3y' in r for r in R)} with a 3-year outcome. "
          f"Ticker base (median 2y total return): " + ", ".join(f"{t} {pct(BASE[t])}" for t in T) + ". Dates whose P/E runs on the "
          f"last full year (no numeric EPS guide): " + ", ".join(f"{t} {sum(not r['eps_guided'] for r in R if r['ticker'] == t)}" for t in T) + ".")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
