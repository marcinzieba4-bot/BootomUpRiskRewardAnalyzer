#!/usr/bin/env python3
"""
HINDSIGHT: Ratio B and the EPP gap (the price's distance above the EPP floor) against the 2-, 3- and 4-year outcome, across
the eleven retrospective series. Prints the tables quoted in staging/retrospective/RATIO_EPP_FINDINGS.md.

Both readings are the frozen engine's own, the same in all eleven templates (retro/templates/*_engine.py.tmpl):
- Ratio B = downside to the BEAR price / upside to the BULL price. Negative when the price is under BEAR, inf when it is at
  or above BULL. The legacy tier reads it at the engine's cuts: BUY < 0.75, ACCUMULATE < 1.10, WATCHLIST < 1.75, AVOID.
- EPP gap = (price - EPP) / EPP, where EPP = the year's EPS x the median of the stock's yearly-minimum P/Es (the panic
  floor). The engine's EPP adjustment bands it at <= 0% (below the floor), 0-40%, 40-100%, 100-200% and above 200%.
Every cut below is one of those engine cuts, plus the two structural edges of Ratio B (below BEAR, above BULL). None was
chosen here, so the grid itself carries no hindsight. Reading a pattern out of it does.

Outcomes use retro_tool's total_return and Yahoo source, the convention of outcome.json (cash dividends added, not
reinvested). The 2y and 3y figures therefore equal the stored outcome.json values, and 4y extends them. The first run
needs the network (retro/.cache/, gitignored). Nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

    python3 staging/retrospective/ratio_epp.py              # every table
    python3 staging/retrospective/ratio_epp.py grid sets    # selected sections

Sections: check one grid sets per rank week fall cushion deep latest
(cushion and deep were added after the first run, to split the cells that stood out; they are in-sample reads.)
Medians of an even count take the upper middle value (statistics.median_high).
"""
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
HORIZONS = (("2y", 24), ("3y", 36), ("4y", 48))
RB_BANDS = ("below BEAR (<0)", "BUY (<0.75)", "ACCUMULATE (<1.10)", "WATCHLIST (<1.75)", "AVOID (>=1.75)", "above BULL (inf)")
EPP_BANDS = ("below floor (<=0%)", "0-40%", "40-100%", "100-200%", ">200%")


def rb_band(v):
    if v < 0:
        return RB_BANDS[0]
    if v < 0.75:
        return RB_BANDS[1]
    if v < 1.10:
        return RB_BANDS[2]
    if v < 1.75:
        return RB_BANDS[3]
    return RB_BANDS[5] if math.isinf(v) else RB_BANDS[4]


def epp_band(g):
    return EPP_BANDS[0] if g <= 0 else EPP_BANDS[1] if g <= 40 else EPP_BANDS[2] if g <= 100 else EPP_BANDS[3] if g <= 200 else EPP_BANDS[4]


PRICES = {t: rt.fetch_prices(t) for t in X.ALL + ("SPY",)}
LAST = min(max(PRICES[t][0]) for t in PRICES)
for r in X.R:
    a = json.load(open(os.path.join(X.ROOT, X.SERIES[r["ticker"]], r["as_of"], "analysis.json")))
    r["ratio_b"], r["epp_gap"] = a["metrics"]["ratio_b"], a["metrics"]["epp_gap_pct"]
    r["rb_band"], r["epp_band"] = rb_band(r["ratio_b"]), epp_band(r["epp_gap"])
    for h, m in HORIZONS:
        end = rt.add_months(r["as_of"], m)
        if end > LAST:
            continue
        _, _, tr, _ = rt.total_return(*PRICES[r["ticker"]], r["as_of"], end)
        _, _, btr, _ = rt.total_return(*PRICES["SPY"], r["as_of"], end)
        r[f"r_{h}"], r[f"s_{h}"] = tr * 100, btr * 100
BASE = {(t, h): med([r[f"r_{h}"] for r in X.R if r["ticker"] == t and f"r_{h}" in r]) for t in X.ALL for h, _ in HORIZONS}


def pct(v, unit="%"):
    return "-" if v is None else f"{v:+.0f}{unit}"


def stats(rs, h):
    s = [r for r in rs if f"r_{h}" in r]
    if not s:
        return None
    return {"n": len(s), "ep": X.episodes(s), "tk": len({r["ticker"] for r in s}),
            "med": med([r[f"r_{h}"] for r in s]),
            "vb": med([r[f"r_{h}"] - BASE[(r["ticker"], h)] for r in s]),
            "beat_b": 100 * sum(r[f"r_{h}"] > BASE[(r["ticker"], h)] for r in s) / len(s),
            "vs": med([r[f"r_{h}"] - r[f"s_{h}"] for r in s]),
            "beat_s": 100 * sum(r[f"r_{h}"] > r[f"s_{h}"] for r in s) / len(s),
            "lost": 100 * sum(r[f"r_{h}"] < 0 for r in s) / len(s)}


def table(title, groups):
    print(f"\n### {title}\n")
    print("| Group | Horizon | Dates | Episodes | Tickers | Median | vs own base | Beat own base | vs SPY | Beat SPY | Lost money |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for name, rs in groups:
        for h, _ in HORIZONS:
            st = stats(rs, h)
            if st:
                print(f"| {name} | {h} | {st['n']} | {st['ep']} | {st['tk']} | {pct(st['med'])} | {pct(st['vb'], 'pp')} | {st['beat_b']:.0f}% | "
                      f"{pct(st['vs'], 'pp')} | {st['beat_s']:.0f}% | {st['lost']:.0f}% |")
            else:
                print(f"| {name} | {h} | 0 | | | | | | | | |")


def section_check():
    mism = n = 0
    for r in X.R:
        for h in ("2y", "3y"):
            if f"tr_{h}" in r and f"r_{h}" in r:
                n += 1
                mism += abs(r[f"tr_{h}"] - r[f"r_{h}"]) > 0.15
    print(f"\nCheck: {n} stored 2y/3y outcomes recomputed, {mism} differ by more than 0.15pp. Prices to {LAST}. "
          + ", ".join(f"{sum(f'r_{h}' in r for r in X.R)} dates with a {h} outcome" for h, _ in HORIZONS) + ".")


def section_one():
    table("Ratio B alone (the engine's tier cuts), all eleven", [(b, [r for r in X.R if r["rb_band"] == b]) for b in RB_BANDS])
    table("EPP gap alone (the engine's bands), all eleven", [(b, [r for r in X.R if r["epp_band"] == b]) for b in EPP_BANDS])


def section_grid():
    for h, _ in HORIZONS:
        for title, key in (("median return minus the ticker's own base", "vb"), ("share of dates that lost money", "lost"),
                           ("share that beat SPY", "beat_s")):
            print(f"\n### Ratio B x EPP gap, {h}: {title} (dates in brackets; cells under 20 dates left out)\n")
            print("| Ratio B \\ EPP gap | " + " | ".join(EPP_BANDS) + " |\n|---|" + "---|" * len(EPP_BANDS))
            for rb in RB_BANDS:
                cells = []
                for eb in EPP_BANDS:
                    st = stats([r for r in X.R if r["rb_band"] == rb and r["epp_band"] == eb], h)
                    if not st or st["n"] < 20:
                        cells.append("")
                    else:
                        v = st[key]
                        cells.append(f"{pct(v, 'pp') if key == 'vb' else f'{v:.0f}%'} ({st['n']})")
                print(f"| {rb} | " + " | ".join(cells) + " |")


ZONES = (
    ("A. Ratio B < 0.75 and EPP gap <= 40% (BUY tier, near or below the floor)", lambda r: r["ratio_b"] < 0.75 and r["epp_gap"] <= 40),
    ("  A1. ...and EPP gap <= 0% (below the floor)", lambda r: r["ratio_b"] < 0.75 and r["epp_gap"] <= 0),
    ("  A2. ...and EPP gap 0-40%", lambda r: r["ratio_b"] < 0.75 and 0 < r["epp_gap"] <= 40),
    ("B. Ratio B < 0.75 and EPP gap > 40% (BUY tier, far above the floor)", lambda r: r["ratio_b"] < 0.75 and r["epp_gap"] > 40),
    ("C. Ratio B >= 1.10 and EPP gap <= 40% (weak tier, near the floor)", lambda r: r["ratio_b"] >= 1.10 and r["epp_gap"] <= 40),
    ("D. Ratio B >= 1.75 and EPP gap > 40% (AVOID tier, far above the floor)", lambda r: r["ratio_b"] >= 1.75 and r["epp_gap"] > 40),
    ("  D1. ...above BULL (inf) and EPP gap > 100%", lambda r: math.isinf(r["ratio_b"]) and r["epp_gap"] > 100),
    ("every date", lambda r: True),
)


def section_sets():
    for label, ts in X.SETS:
        table(f"The combined zones, {label}", [(name, [r for r in X.R if r["ticker"] in ts and f(r)]) for name, f in ZONES])


def section_per():
    for h in ("2y", "4y"):
        print(f"\n### Per ticker, {h}: median minus the ticker's own base (dates; share that lost money)\n")
        print("| Ticker | Base | " + " | ".join(n.split(" (")[0].strip() for n, _ in ZONES[:-1]) + " |\n|---|---|" + "---|" * (len(ZONES) - 1))
        for t in X.ALL:
            cells = []
            for _, f in ZONES[:-1]:
                st = stats([r for r in X.R if r["ticker"] == t and f(r)], h)
                cells.append(f"{pct(st['vb'], 'pp')} ({st['n']}, {st['lost']:.0f}%)" if st and st["n"] >= 10 else "-")
            print(f"| {t} | {pct(BASE[(t, h)])} | " + " | ".join(cells) + " |")


def section_rank():
    print("\n### Within each ticker's own series: rank correlation with the forward return (+ = a lower reading did better)\n")
    keys = (("Ratio B", "ratio_b"), ("EPP gap", "epp_gap"), ("52w high distance", "dd_52w"), ("own P/E pctl", "pe_pctl"))
    print("| Ticker | " + " | ".join(f"{n} {h}" for n, _ in keys for h, _ in HORIZONS) + " |\n|---|" + "---|" * (len(keys) * len(HORIZONS)))
    pos = Counter()
    for t in X.ALL:
        cells = []
        for n, k in keys:
            for h, _ in HORIZONS:
                s = [r for r in X.R if r["ticker"] == t and f"r_{h}" in r]
                v = -X.spearman([r[k] for r in s], [r[f"r_{h}"] for r in s])
                pos[(n, h)] += v > 0
                cells.append(f"{v:+.2f}")
        print(f"| {t} | " + " | ".join(cells) + " |")
    print("| positive in | " + " | ".join(f"{pos[(n, h)]} of {len(X.ALL)}" for n, _ in keys for h, _ in HORIZONS) + " |")


def section_week():
    """The same week across tickers, which removes the market's path: does a lower Ratio B or EPP gap pick the better stock?"""
    by_week = defaultdict(list)
    for r in X.R:
        if "r_2y" in r:
            by_week[r["date"].isocalendar()[:2]].append(r)
    print("\n### The same week across tickers (weeks with six or more tickers scored)\n")
    print("| Horizon | Reading | Weeks | Mean weekly rank correlation (+ = lower did better) | Weeks above zero | "
          "Zone A mean place (0-1) | Zone D mean place |\n|---|---|---|---|---|---|---|")
    for h, _ in HORIZONS:
        for n, k in (("Ratio B", "ratio_b"), ("EPP gap", "epp_gap")):
            ic, pa, pd = [], [], []
            for rs in by_week.values():
                rs = [r for r in rs if f"r_{h}" in r]
                if len(rs) < 6:
                    continue
                ic.append(-X.spearman([r[k] for r in rs], [r[f"r_{h}"] for r in rs]))
                order = sorted(rs, key=lambda r: r[f"r_{h}"])
                place = {id(r): i / (len(order) - 1) for i, r in enumerate(order)}
                pa += [place[id(r)] for r in rs if ZONES[0][1](r)]
                pd += [place[id(r)] for r in rs if ZONES[5][1](r)]
            print(f"| {h} | {n} | {len(ic)} | {statistics.fmean(ic):+.2f} | {100 * sum(x > 0 for x in ic) / len(ic):.0f}% | "
                  f"{statistics.fmean(pa):.2f} | {statistics.fmean(pd):.2f} |")


def section_fall():
    """Is the reading just the price fall in disguise? Hold the 52-week distance roughly fixed and split by the zones."""
    falls = (("within 10% of the 52w high", lambda r: r["dd_52w"] > -0.10), ("10-20% below", lambda r: -0.20 < r["dd_52w"] <= -0.10),
             ("20-30% below", lambda r: -0.30 < r["dd_52w"] <= -0.20), ("30%+ below", lambda r: r["dd_52w"] <= -0.30))
    groups = []
    for fn, ff in falls:
        for zn, zf in (("zone A", ZONES[0][1]), ("zone D", ZONES[5][1]), ("neither", lambda r: not ZONES[0][1](r) and not ZONES[5][1](r))):
            groups.append((f"{fn}, {zn}", [r for r in X.R if ff(r) and zf(r)]))
    table("Zones A and D inside each band of distance below the 52-week high, all eleven", groups)


CUSHION = (
    ("price below the BEAR price (Ratio B < 0)", lambda r: r["ratio_b"] < 0),
    ("  ...and below the EPP floor", lambda r: r["ratio_b"] < 0 and r["epp_gap"] <= 0),
    ("below the EPP floor (gap <= 0%), any Ratio B", lambda r: r["epp_gap"] <= 0),
    ("Ratio B 0-0.75 and EPP gap 0-40% (zone A2)", lambda r: 0 <= r["ratio_b"] < 0.75 and 0 < r["epp_gap"] <= 40),
    ("above the BULL price and EPP gap > 100% (zone D1)", lambda r: math.isinf(r["ratio_b"]) and r["epp_gap"] > 100),
    ("every date", lambda r: True),
)


def section_cushion():
    """Added after the first run, to split the cells that stood out: below BEAR, below the floor, A2 and D1, by ticker set."""
    for label, ts in X.SETS:
        table(f"Cushion cells, {label}", [(name, [r for r in X.R if r["ticker"] in ts and f(r)]) for name, f in CUSHION])
    print("\n### Per ticker: below the BEAR price, and zone D1 (dates with a 2y outcome; 2y median minus own base; lost money at 2y / 4y)\n")
    print("| Ticker | Below BEAR | Below BEAR: years | Zone D1 | Zone D1: years |\n|---|---|---|---|---|")
    for t in X.ALL:
        cells = []
        for f in (CUSHION[0][1], CUSHION[4][1]):
            s = [r for r in X.R if r["ticker"] == t and f(r) and "r_2y" in r]
            s4 = [r for r in s if "r_4y" in r]
            cells.append((f"{pct(med([r['r_2y'] - BASE[(t, '2y')] for r in s]), 'pp')} ({len(s)}; {100 * sum(r['r_2y'] < 0 for r in s) / len(s):.0f}% / "
                          f"{100 * sum(r['r_4y'] < 0 for r in s4) / len(s4) if s4 else 0:.0f}%)" if s else "-",
                          ", ".join(f"{y} ({n})" for y, n in sorted(Counter(r["year"] for r in s).items())) or "-"))
        print(f"| {t} | {cells[0][0]} | {cells[0][1]} | {cells[1][0]} | {cells[1][1]} |")
    print("\n### Dates below the BEAR price that have no 2y outcome yet: the one-year record (stored outcome.json)\n")
    print("| Ticker | Dates | First - last | With a 1y outcome | Median 1y | Lost money (1y) | Kind |\n|---|---|---|---|---|---|---|")
    for t in X.ALL:
        s = [r for r in X.R if r["ticker"] == t and r["ratio_b"] < 0 and "r_2y" not in r]
        if s:
            one = [r for r in s if "tr_1y" in r]
            print(f"| {t} | {len(s)} | {s[0]['as_of']} - {s[-1]['as_of']} | {len(one)} | {pct(med([r['tr_1y'] for r in one])) if one else '-'} | "
                  f"{100 * sum(r['tr_1y'] < 0 for r in one) / len(one) if one else 0:.0f}% | {', '.join(f'{k} {n}' for k, n in sorted(Counter(r['kind'] for r in s).items()))} |")


def section_deep():
    """Added after the first run: inside a deep fall (30%+ below the 52-week high), zone A against the rest, and who lost."""
    deep = [r for r in X.R if r["dd_52w"] <= -0.30]
    a = ZONES[0][1]
    for label, ts in X.SETS:
        table(f"30%+ below the 52-week high, zone A against the rest, {label}",
              [("zone A", [r for r in deep if r["ticker"] in ts and a(r)]), ("not zone A", [r for r in deep if r["ticker"] in ts and not a(r)])])
    for name, f in (("not zone A", lambda r: not a(r)), ("zone A", a)):
        lost = Counter((r["ticker"], r["year"]) for r in deep if f(r) and "r_2y" in r and r["r_2y"] < 0)
        print(f"\nDeep-fall dates that lost money over two years, {name}: " + ", ".join(f"{t} {y} ({n})" for (t, y), n in sorted(lost.items())) + ".")


def section_latest():
    print("\n### The newest date of each ticker (point-in-time readings; the zones are hindsight hypotheses)\n")
    print("| Ticker | As of | Price | Ratio B | EPP gap | Below 52w high | Zone | Tier / class |\n|---|---|---|---|---|---|---|---|")
    for t in X.ALL:
        r = [x for x in X.R if x["ticker"] == t][-1]
        zone = next((n.split(".")[0].strip() for n, f in ZONES[:-1] if not n.startswith("  ") and f(r)), "none")
        print(f"| {t} | {r['as_of']} | ${r['price']:.2f} | {r['ratio_b']:.2f}x | {r['epp_gap']:+.0f}% | {r['dd_52w'] * 100:+.0f}% | {zone} | "
              f"{r['tier']} / {r['class']} |")


SECTIONS = {"check": section_check, "one": section_one, "grid": section_grid, "sets": section_sets, "per": section_per,
            "rank": section_rank, "week": section_week, "fall": section_fall, "cushion": section_cushion, "deep": section_deep,
            "latest": section_latest}

if __name__ == "__main__":
    print(f"HINDSIGHT. {len(X.R)} point-in-time dates across {len(X.ALL)} tickers.")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
