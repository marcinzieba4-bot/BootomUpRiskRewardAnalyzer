#!/usr/bin/env python3
"""
HINDSIGHT: split the twenty-four retrospective series into a growth and a value basket each month, and test whether bond
yields and the ISM manufacturing index say when to hold which. The same rules run on the Russell 1000 Growth and Value
ETFs (IWF, IWD) from 2000. Prints the tables quoted in staging/retrospective/STYLE_SWITCH.md.

THE RULES, fixed in this docstring before the first run; every rule below is printed.
- Baskets, point-in-time, each month on each ticker's first as-of date (ratio_b_basket.py, RETRO_UNIVERSE=all):
  - EY = EPP_TODAY_EPS / price (model.py and analysis.json, the as-of basis);
  - DY = Yahoo dividends with an ex-date in the 365 days before, over the close;
  - G5 = the 5-year EPS growth rate from EPS_NORM (the last year against five years earlier, both positive).
  - The VALUE score is the average of the percentile ranks of EY (high), DY (high) and G5 (low); a missing reading is
    skipped.
  - The most value-like third is the VALUE basket and the least value-like third the GROWTH basket. Equal weight,
    rebalanced monthly; entry at the next trading day's close (the RET of ratio_b_basket.py).
- ETFs: IWF (Russell 1000 Growth) and IWD (Russell 1000 Value), total return, held from the first trading day of each
  month, 2000-07 to 2026-11. The signal is read at the previous trading day's close.
- Macro readings, all public by the signal date:
  - the 10-year Treasury yield (^TNX) and the 13-week bill (^IRX), Yahoo daily closes;
  - the ISM manufacturing PMI, as 50 + half the OECD's US manufacturing confidence balance
    (data/us_mfg_confidence_oecd.csv, which equals 2 x (PMI - 50)). A month's PMI is used from the 5th calendar day of
    the next month (ISM publishes on the first business day); the series ends 2026-05, and its last value carries
    forward.
- Signals (hold VALUE when true, GROWTH when false):
  - Y3: the 10-year yield is higher than 63 trading days earlier.
  - Y6: the same over 126 trading days.
  - C3: the curve (10-year minus 13-week) is steeper than 63 trading days earlier.
  - I50: the PMI is 50 or above.
  - I3: the PMI is higher than three months earlier.
  - COMBO A: value if Y6 and I3; growth if neither; otherwise half and half.
  - COMBO B: value if I50 and Y6; growth if neither; otherwise half and half.
- Tests:
  - The value-minus-growth return in the next month, by the signal's state: mean, Welch t, months.
  - The switching book (hold what the signal says, rebalanced monthly) against always growth, always value, half and
    half, and SPY.
  - Periods: baskets 2008-2016 and 2017-2026; ETFs 2000-2007 (before every retrospective date), 2008-2016, 2017-2026.

Everything printed is a label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule"). Reads only; the first run needs the network for Yahoo (retro/.cache/, gitignored).

    python3 staging/retrospective/style_switch.py                 # every table
    python3 staging/retrospective/style_switch.py spread switch   # selected sections

Sections: baskets spread switch years now (first run); contrib (added after it, labelled so)
"""
import ast
import bisect
import contextlib
import csv
import datetime as dt
import io
import json
import math
import os
import re
import statistics
import sys
from collections import Counter

os.environ["RETRO_UNIVERSE"] = "all"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import ratio_b_basket as B  # noqa: E402
X, rt = B.X, B.rt
MONTHS, FIRST, RET = B.MONTHS, B.FIRST, B.RET
EPS_NORM_RE = re.compile(r"^EPS_NORM\s*=\s*(\{[^}]*\})", re.M)
EPS_TODAY_RE = re.compile(r"^EPP_TODAY_EPS\s*=\s*(-?[0-9.]+)", re.M)

# ── macro readings ───────────────────────────────────────────────────────────
TNX, _ = rt.fetch_prices("^TNX")
IRX, _ = rt.fetch_prices("^IRX")
TK = sorted(TNX)
IK = sorted(IRX)
PMI = {}
with open(os.path.join(HERE, "data", "us_mfg_confidence_oecd.csv")) as fh:
    for row in csv.reader(l for l in fh if not l.startswith("#")):
        if row[0] != "month":
            PMI[row[0]] = 50 + float(row[1]) / 2
PMI_MONTHS = sorted(PMI)


def on_or_before(keys, series, d, back=0):
    i = bisect.bisect_right(keys, d) - 1 - back
    return series[keys[i]] if i >= 0 else None


def pmi_month(d):
    """The latest PMI month usable on date d: month M from the 5th of M+1."""
    usable = [m for m in PMI_MONTHS if (dt.date(int(m[:4]) + (m[5:] == "12"), int(m[5:]) % 12 + 1, 5)).isoformat() <= d]
    return usable[-1] if usable else None


def signals(d):
    y0, y63, y126 = on_or_before(TK, TNX, d), on_or_before(TK, TNX, d, 63), on_or_before(TK, TNX, d, 126)
    b0, b63 = on_or_before(IK, IRX, d), on_or_before(IK, IRX, d, 63)
    pm = pmi_month(d)
    i = PMI_MONTHS.index(pm)
    p0, p3 = PMI[pm], PMI[PMI_MONTHS[i - 3]]
    s = {"Y3": y0 > y63, "Y6": y0 > y126, "C3": (y0 - b0) > (y63 - b63), "I50": p0 >= 50, "I3": p0 > p3}
    s["COMBO A"] = 1.0 if s["Y6"] and s["I3"] else 0.0 if not s["Y6"] and not s["I3"] else 0.5
    s["COMBO B"] = 1.0 if s["I50"] and s["Y6"] else 0.0 if not s["I50"] and not s["Y6"] else 0.5
    for k in ("Y3", "Y6", "C3", "I50", "I3"):
        s[k] = 1.0 if s[k] else 0.0
    s.update(_y10=y0, _curve=y0 - b0, _pmi=p0, _pmi_month=pm)
    return s


RULES = ("Y3", "Y6", "C3", "I50", "I3", "COMBO A", "COMBO B")

# ── the baskets ──────────────────────────────────────────────────────────────
PX = {t: rt.fetch_prices(t) for t in X.ALL}
PXK = {t: sorted(PX[t][0]) for t in X.ALL}


def readings(t, a_of):
    folder = os.path.join(X.ROOT, X.SERIES[t], a_of)
    a = json.load(open(os.path.join(folder, "analysis.json")))
    src = open(os.path.join(folder, "model.py"), encoding="utf-8").read()
    eps = float(EPS_TODAY_RE.search(src).group(1))
    hist = ast.literal_eval(EPS_NORM_RE.search(src).group(1))
    ys = sorted(hist)
    g5 = None
    if ys and (ys[-1] - 5) in hist and hist[ys[-1]] > 0 and hist[ys[-1] - 5] > 0:
        g5 = (hist[ys[-1]] / hist[ys[-1] - 5]) ** 0.2 - 1
    closes, divs = PX[t]
    c = on_or_before(PXK[t], closes, a_of)
    start = (dt.date.fromisoformat(a_of) - dt.timedelta(days=365)).isoformat()
    dy = sum(v for d, v in divs if start < d <= a_of) / c
    return {"ey": eps / a["price"], "dy": dy, "g5": g5}


def pct_rank(vals, v):
    s = sorted(vals)
    return bisect.bisect_left(s, v) / max(1, len(s) - 1)


BASKETS = {}
for m in MONTHS:
    names = list(FIRST[m])
    rd = {t: readings(t, FIRST[m][t]["as_of"]) for t in names}
    score = {}
    for t in names:
        parts = []
        for key, sign in (("ey", 1), ("dy", 1), ("g5", -1)):
            vals = [sign * rd[x][key] for x in names if rd[x][key] is not None]
            if rd[t][key] is not None and len(vals) > 2:
                parts.append(pct_rank(vals, sign * rd[t][key]))
        score[t] = statistics.fmean(parts) if parts else 0.5
    k = max(3, len(names) // 3)
    order = sorted(names, key=lambda t: score[t])
    BASKETS[m] = {"growth": order[:k], "value": order[-k:]}
FORM = {m: max(s["as_of"] for s in FIRST[m].values()) for m in MONTHS}   # the signal date: the month's formation
G = {m: statistics.fmean(RET[m][t] for t in BASKETS[m]["growth"]) for m in MONTHS}
V = {m: statistics.fmean(RET[m][t] for t in BASKETS[m]["value"]) for m in MONTHS}
SPY_B = {m: RET[m]["SPY"] for m in MONTHS}
SIG_B = {m: signals(FORM[m]) for m in MONTHS}

# ── the ETFs ─────────────────────────────────────────────────────────────────
def tr_monthly(sym, firsts):
    days, idx = B.tr_index(sym)
    lv = lambda d: idx[bisect.bisect_right(days, d) - 1]
    return [lv(b) / lv(a) - 1 for a, b in zip(firsts, firsts[1:])]


ALLDAYS = B.DAYS
FIRSTS = []
for d in ALLDAYS:
    if d >= "2000-07-01" and (not FIRSTS or d[:7] != FIRSTS[-1][:7]):
        FIRSTS.append(d)
EMONTHS = [d[:7] for d in FIRSTS[:-1]]
IWF = dict(zip(EMONTHS, tr_monthly("IWF", FIRSTS)))
IWD = dict(zip(EMONTHS, tr_monthly("IWD", FIRSTS)))
SPY_E = dict(zip(EMONTHS, tr_monthly("SPY", FIRSTS)))
SIG_E = {m: signals(ALLDAYS[bisect.bisect_left(ALLDAYS, d) - 1]) for m, d in zip(EMONTHS, FIRSTS)}


def pct(v):
    return f"{v * 100:+.1f}%"


def stats(xs):
    g = math.prod(1 + x for x in xs)
    mu, sd = statistics.fmean(xs), statistics.pstdev(xs)
    v, pk, mdd = 1.0, 1.0, 0.0
    for x in xs:
        v *= 1 + x
        pk = max(pk, v)
        mdd = min(mdd, v / pk - 1)
    return g ** (12 / len(xs)) - 1, (mu / sd * math.sqrt(12) if sd else 0.0), mdd


def cell(xs):
    c, sh, dd = stats(xs)
    return f"{pct(c)} / {sh:.2f} / {dd * 100:.0f}%"


def welch(a, b):
    if len(a) < 3 or len(b) < 3:
        return 0.0
    va, vb = statistics.variance(a), statistics.variance(b)
    return (statistics.fmean(a) - statistics.fmean(b)) / math.sqrt(va / len(a) + vb / len(b))


SETS = (("Baskets 2008-2026", MONTHS, V, G, SPY_B, SIG_B), ("Baskets 2008-2016", [m for m in MONTHS if m <= "2016-12"], V, G, SPY_B, SIG_B),
        ("Baskets 2017-2026", [m for m in MONTHS if m >= "2017-01"], V, G, SPY_B, SIG_B),
        ("IWD-IWF 2000-2026", EMONTHS, IWD, IWF, SPY_E, SIG_E), ("IWD-IWF 2000-2007", [m for m in EMONTHS if m <= "2007-12"], IWD, IWF, SPY_E, SIG_E),
        ("IWD-IWF 2008-2016", [m for m in EMONTHS if "2008-01" <= m <= "2016-12"], IWD, IWF, SPY_E, SIG_E),
        ("IWD-IWF 2017-2026", [m for m in EMONTHS if m >= "2017-01"], IWD, IWF, SPY_E, SIG_E))


def section_baskets():
    gc = Counter(t for m in MONTHS for t in BASKETS[m]["growth"])
    vc = Counter(t for m in MONTHS for t in BASKETS[m]["value"])
    n = len(MONTHS)
    print("\n### The baskets (share of months each ticker sat in each)\n")
    print("- GROWTH: " + ", ".join(f"{t} {100 * c / n:.0f}%" for t, c in gc.most_common(12)))
    print("- VALUE: " + ", ".join(f"{t} {100 * c / n:.0f}%" for t, c in vc.most_common(12)))
    print(f"- Names per basket: {statistics.fmean(len(BASKETS[m]['growth']) for m in MONTHS):.1f} on average.")
    print("\n| Series | 2008-2026 | 2008-2016 | 2017-2026 |\n|---|---|---|---|")
    for lab, s in (("GROWTH basket", G), ("VALUE basket", V), ("SPY", SPY_B)):
        print(f"| {lab} | {cell([s[m] for m in MONTHS])} | {cell([s[m] for m in MONTHS if m <= '2016-12'])} | {cell([s[m] for m in MONTHS if m >= '2017-01'])} |")
    print("| IWF / IWD 2000-2026 | " + f"{cell(list(IWF.values()))} / {cell(list(IWD.values()))} | | |")


def section_spread():
    for name, ms, v, g, _, sig in SETS:
        print(f"\n### {name}: next month's value-minus-growth return, by the signal's state ({len(ms)} months)\n")
        print("| Rule | Says VALUE: months / mean spread | Says GROWTH: months / mean spread | Difference | Welch t | Right sign? |\n|---|---|---|---|---|---|")
        for rule in RULES:
            a = [v[m] - g[m] for m in ms if sig[m][rule] == 1.0]
            b = [v[m] - g[m] for m in ms if sig[m][rule] == 0.0]
            ma = statistics.fmean(a) if a else float("nan")
            mb = statistics.fmean(b) if b else float("nan")
            print(f"| {rule} | {len(a)} / {pct(ma)} | {len(b)} / {pct(mb)} | {pct(ma - mb)} | {welch(a, b):+.2f} | {'yes' if ma > mb else 'NO'} |")


def book(ms, v, g, sig, rule):
    return [sig[m][rule] * v[m] + (1 - sig[m][rule]) * g[m] for m in ms]


def section_switch():
    for name, ms, v, g, spy, sig in SETS:
        print(f"\n### {name}: switching books (annual return / Sharpe / worst drawdown, monthly)\n")
        print("| Book | Result | Months in value | Switches a year |\n|---|---|---|---|")
        for lab, xs in (("always GROWTH", [g[m] for m in ms]), ("always VALUE", [v[m] for m in ms]),
                        ("half and half", [(v[m] + g[m]) / 2 for m in ms]), ("SPY", [spy[m] for m in ms])):
            print(f"| {lab} | {cell(xs)} | - | - |")
        for rule in RULES:
            xs = book(ms, v, g, sig, rule)
            w = [sig[m][rule] for m in ms]
            sw = sum(abs(a - b) > 0 for a, b in zip(w, w[1:])) / (len(ms) / 12)
            print(f"| switch on {rule} | {cell(xs)} | {100 * statistics.fmean(w):.0f}% | {sw:.1f} |")


def section_years():
    yrs = sorted({m[:4] for m in EMONTHS})
    print("\n### Calendar years: value minus growth (IWD - IWF, and the baskets), with the signals' average state\n")
    print("| Year | IWD - IWF | Baskets V - G | Y6 (share in value) | I50 | I3 | COMBO A | PMI (Dec) | 10y (Dec) |\n|---|---|---|---|---|---|---|---|---|")
    for y in yrs:
        em = [m for m in EMONTHS if m[:4] == y]
        bm = [m for m in MONTHS if m[:4] == y]
        e = math.prod(1 + IWD[m] for m in em) - math.prod(1 + IWF[m] for m in em)
        bv = (math.prod(1 + V[m] for m in bm) - math.prod(1 + G[m] for m in bm)) if bm else None
        sig = [SIG_E[m] for m in em]
        last = sig[-1]
        print(f"| {y} | {pct(e)} | {pct(bv) if bv is not None else '-'} | {100 * statistics.fmean(s['Y6'] for s in sig):.0f}% | "
              f"{100 * statistics.fmean(s['I50'] for s in sig):.0f}% | {100 * statistics.fmean(s['I3'] for s in sig):.0f}% | "
              f"{100 * statistics.fmean(s['COMBO A'] for s in sig):.0f}% | {last['_pmi']:.1f} ({last['_pmi_month']}) | {last['_y10']:.2f}% |")


def section_contrib():
    """Added after the first run: which years did the switching gain come from (against half and half)?"""
    print("\n### Switching minus half-and-half, by calendar year (added after the first run)\n")
    print("| Year | IWD/IWF: Y6 | IWD/IWF: C3 | IWD/IWF: Y3 | Baskets: Y6 | Baskets: COMBO B |\n|---|---|---|---|---|---|")
    yrs = sorted({m[:4] for m in EMONTHS})
    tot = Counter()
    for y in yrs:
        em = [m for m in EMONTHS if m[:4] == y]
        bm = [m for m in MONTHS if m[:4] == y]
        def ex(ms, v, g, sig, rule):
            sw = math.prod(1 + x for x in book(ms, v, g, sig, rule))
            hh = math.prod(1 + (v[m] + g[m]) / 2 for m in ms)
            return sw - hh
        cells = [ex(em, IWD, IWF, SIG_E, r) for r in ("Y6", "C3", "Y3")]
        cells += [ex(bm, V, G, SIG_B, r) if bm else None for r in ("Y6", "COMBO B")]
        for k, c in zip(("e6", "ec", "e3", "b6", "bb"), cells):
            if c is not None:
                tot[k] += c
        print(f"| {y} | " + " | ".join(pct(c) if c is not None else "-" for c in cells) + " |")
    print("| sum | " + " | ".join(pct(tot[k]) for k in ("e6", "ec", "e3", "b6", "bb")) + " |")


def section_now():
    d = ALLDAYS[-1]
    s = signals(d)
    m = MONTHS[-1]
    print(f"\n### Now ({d})\n")
    print(f"- 10-year yield {s['_y10']:.2f}%; curve (10y - 13w) {s['_curve']:+.2f} points; PMI {s['_pmi']:.1f} ({s['_pmi_month']}, the latest in the file).")
    print("- Rules: " + ", ".join(f"{r} {'VALUE' if s[r] == 1 else 'GROWTH' if s[r] == 0 else 'half/half'}" for r in RULES) + ".")
    print(f"- The newest baskets ({m}): GROWTH {', '.join(BASKETS[m]['growth'])}; VALUE {', '.join(BASKETS[m]['value'])}.")


SECTIONS = {"baskets": section_baskets, "spread": section_spread, "switch": section_switch, "years": section_years, "now": section_now,
            "contrib": section_contrib}

if __name__ == "__main__":
    print(f"HINDSIGHT. Baskets {MONTHS[0]} to {MONTHS[-1]}; ETFs {EMONTHS[0]} to {EMONTHS[-1]}; PMI to {PMI_MONTHS[-1]}.")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
