#!/usr/bin/env python3
"""
HINDSIGHT: the growth-basket selection and the value-basket selection held together as one book, and then the
10-year yield filter applied to that book. Prints the tables quoted in staging/retrospective/COMBO_BOOK.md.

Both selections are POST-HOC: they come from basket_selection.py's near-misses and were then swept in tilt_switch.py.
This script adds no new selection rule; it asks only whether holding both sleeves, and tilting between them on the
yield trend, beats switching all the way.

FIXED in this docstring before the first run; every cell is printed.
- Engine, calendar, data, baskets and the Y6 signal are tilt_switch.py's (daily total-return data, monthly entries).
- Two sleeves, formed every month whatever the yield says:
  - GROWTH sleeve: the n growth-basket members with the highest own P/E percentile (ties broken by the EPP gap).
  - VALUE sleeve: the n value-basket members with the most negative e2_rev (the floor's EPS against 26 weeks earlier).
  - n = 2 is the main case; n = 3 is printed as a check.
- Books (sleeve weights; equal weight inside a sleeve):
  - GROWTH PICKS: the growth sleeve alone, always.
  - VALUE PICKS: the value sleeve alone, always.
  - COMBINED 50/50: half in each sleeve, always (no yield filter).
  - COMBINED + YIELD TILT: 75% in the sleeve Y6 favours, 25% in the other. Y6 favours VALUE when the 10-year yield
    is above its level 126 trading days earlier, GROWTH otherwise. This is the headline book ("combine, then apply the
    yield filter").
  - YIELD SWITCH: 100% in the favoured sleeve (tilt_switch.py's "2 picks").
  - The same five built from whole baskets in place of the picks: WHOLE GROWTH, WHOLE VALUE, WHOLE 50/50,
    WHOLE TILT 75/25 and WHOLE SWITCH. Then SPY.
- Holding and stops: 1-month cohorts with NONE or TRAIL15 (trailing -15% from the peak; cash for the rest of the
  cohort), and 3-month cohorts with NONE or TRAIL15+MA50 (re-entry after a close above the 50-day average).
- MAIN configuration, named before the run: 1-month hold, TRAIL15, after the 0.10% cost charge of tilt_switch.py.
  That choice is TILT_SWITCH.md's best region, so it is itself hindsight.
- Optional overlay HEDGE50 (short 50% SPY while the S&P 500 is below its 100-day average; ratio_b_hedge.py).
- Stats: annual return, volatility, Sharpe, Sortino, worst drawdown with its dates and the longest time under water,
  Calmar, beta and correlation to SPY, monthly hit rate, months beating SPY, best and worst month and year, years
  positive, 2008-2016 and 2017-2026. Then each sleeve's annual return inside Y6's VALUE and GROWTH regimes, calendar
  years, and the newest month.

Everything printed is a label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule"). Reads only.

    python3 staging/retrospective/combo_book.py                    # every table
    python3 staging/retrospective/combo_book.py --json out.json    # also the chart data (weekly curves), to a path
"""
import bisect
import contextlib
import datetime
import io
import json
import math
import os
import statistics
import sys

os.environ["RETRO_UNIVERSE"] = "all"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import tilt_switch as TS  # noqa: E402  (engine, stops, costs, baskets, Y6)
P, BS, SS = TS.P, TS.BS, TS.SS
DAYS, MONTHS, DAY_POS, ENTRY, NDAYS = TS.DAYS, TS.MONTHS, TS.DAY_POS, TS.ENTRY, TS.NDAYS
STOP = {s[0]: s for s in TS.STOPS}
CONFIGS = ((1, "NONE"), (1, "TRAIL15"), (3, "NONE"), (3, "TRAIL15+MA50"))
MAIN = (1, "TRAIL15")
PICK_BOOKS = ("GROWTH PICKS", "VALUE PICKS", "COMBINED 50/50", "COMBINED + YIELD TILT", "YIELD SWITCH")
WHOLE_BOOKS = ("WHOLE GROWTH", "WHOLE VALUE", "WHOLE 50/50", "WHOLE TILT 75/25", "WHOLE SWITCH")


def growth_sleeve(m, n):
    names = SS.BASKETS[m]["growth"]
    pts = sorted((((BS.val(m, t, "pe_pctl") or -1), (BS.val(m, t, "epp_gap") or -1e9)), t) for t in names)[::-1]
    return [t for _, t in pts[:n]] or names[:n]


def value_sleeve(m, n):
    names = SS.BASKETS[m]["value"]
    pts = sorted((v, t) for v, t in ((BS.val(m, t, "e2_rev"), t) for t in names) if v is not None)
    return [t for _, t in pts[:n]] or names[:n]


def value_share(book, m):
    fav_value = TS.basket(m) == "value"
    kind = book.replace("WHOLE ", "").replace("COMBINED + YIELD ", "").replace("COMBINED ", "")
    return {"GROWTH PICKS": 0.0, "VALUE PICKS": 1.0, "50/50": 0.5, "TILT": 0.75 if fav_value else 0.25,
            "TILT 75/25": 0.75 if fav_value else 0.25, "YIELD SWITCH": 1.0 if fav_value else 0.0,
            "SWITCH": 1.0 if fav_value else 0.0, "GROWTH": 0.0, "VALUE": 1.0}[kind]


def weights(book, m, n=2):
    if book.startswith("WHOLE"):
        g, v = SS.BASKETS[m]["growth"], SS.BASKETS[m]["value"]
    else:
        g, v = growth_sleeve(m, n), value_sleeve(m, n)
    sv = value_share(book, m)
    w = {}
    for names, share in ((v, sv), (g, 1 - sv)):
        if share > 0:
            for t in names:
                w[t] = w.get(t, 0.0) + share / len(names)
    return w


def run_w(W, hold, stop):
    """tilt_switch.run with the month's weights given: cohorts combined into one daily return series."""
    paths, ex, en, cash = {}, 0, 0, []
    for ci, m in enumerate(MONTHS):
        e, total, a, b, c = TS.cohort_path(ci, W[m], hold, stop)
        paths[m] = (e, total)
        ex, en = ex + a, en + b
        cash.append(c)
    entries = [DAY_POS[ENTRY[m]] for m in MONTHS]
    rets = [0.0]
    for j in range(1, NDAYS):
        i = bisect.bisect_right(entries, j - 1) - 1
        em = entries[i]
        num = den = 0.0
        for c in MONTHS[max(0, i - hold + 1): i + 1]:
            e, total = paths[c]
            base = total[em - e]
            num += total[min(j - e, len(total) - 1)] / base
            den += total[min(j - 1 - e, len(total) - 1)] / base
        rets.append(num / den - 1)
    years = (NDAYS - 1) / 252
    return rets, {"exits": ex / years, "entries": en / years, "cash": statistics.fmean(cash), "W": W}


CACHE = {}


def book(name, hold, stop, n=2, hedge=False, costs=True):
    k = (name, hold, stop, n)
    if k not in CACHE:
        CACHE[k] = run_w({m: weights(name, m, n) for m in MONTHS}, hold, STOP[stop])
    r, info = CACHE[k]
    if hedge:
        r = P.hedged(r, P.FLAG100, 0.5)
    return TS.costed(r, info, hold, hedge) if costs else r


def spy():
    return P.SPY


def compound(xs):
    return math.prod(1 + x for x in xs) - 1


def by_period(r, key):
    out = {}
    for d, x in zip(DAYS[1:], r[1:]):
        out.setdefault(key(d), []).append(x)
    return {k: compound(v) for k, v in out.items()}


def full_stats(r):
    cagr, vol, sh, mdd, beta = P.stats(r)
    xs, ss = r[1:], P.SPY[1:]
    down = math.sqrt(statistics.fmean(min(x, 0.0) ** 2 for x in xs))
    sortino = statistics.fmean(xs) / down * math.sqrt(252)
    corr = statistics.correlation(xs, ss)
    v, pk, pk_i, worst, w_pk, w_tr, under, longest, l_from = 1.0, 1.0, 0, 0.0, 0, 0, 0, 0, 0
    for i, x in enumerate(xs, start=1):
        v *= 1 + x
        if v >= pk:
            pk, pk_i, under = v, i, 0
        else:
            under += 1
            if under > longest:
                longest, l_from = under, pk_i
        if v / pk - 1 < worst:
            worst, w_pk, w_tr = v / pk - 1, pk_i, i
    eq = [1.0]
    for x in xs:
        eq.append(eq[-1] * (1 + x))
    rec = next((i for i in range(w_tr, NDAYS) if eq[i] >= eq[w_pk]), None)
    mon, mon_s = by_period(r, lambda d: d[:7]), by_period(P.SPY, lambda d: d[:7])
    yr = by_period(r, lambda d: d[:4])
    return {"cagr": cagr, "vol": vol, "sharpe": sh, "sortino": sortino, "mdd": mdd, "calmar": cagr / -mdd if mdd else None,
            "beta": beta, "corr": corr, "mdd_peak": DAYS[w_pk], "mdd_trough": DAYS[w_tr],
            "mdd_recovered": DAYS[rec] if rec else None, "underwater_years": longest / 252, "underwater_from": DAYS[l_from],
            "hit": sum(x > 0 for x in mon.values()) / len(mon), "beat_spy": sum(mon[k] > mon_s[k] for k in mon) / len(mon),
            "best_month": max(mon.items(), key=lambda kv: kv[1]), "worst_month": min(mon.items(), key=lambda kv: kv[1]),
            "best_year": max(yr.items(), key=lambda kv: kv[1]), "worst_year": min(yr.items(), key=lambda kv: kv[1]),
            "years_pos": sum(x > 0 for x in yr.values()), "years": len(yr), "first_half": P.stats(r, hi="2016"),
            "second_half": P.stats(r, lo="2017"), "total": math.prod(1 + x for x in xs) - 1}


def cell(r, lo=None, hi=None):
    c, _, sh, dd, _ = P.stats(r, lo, hi)
    return f"{c * 100:+.1f}% / {sh:.2f} / {dd * 100:.0f}%"


def section_main():
    h, s = MAIN
    print(f"\n### Main configuration: {h}-month hold, {s}, after 0.10% costs (annual / Sharpe / worst drawdown; daily, "
          f"{DAYS[0]} to {DAYS[-1]})\n")
    print("| Book | 2008-2026 | 2008-2016 | 2017-2026 | Beta | With HEDGE50 |\n|---|---|---|---|---|---|")
    for name in PICK_BOOKS + WHOLE_BOOKS:
        r = book(name, h, s)
        print(f"| {name} | {cell(r)} | {cell(r, hi='2016')} | {cell(r, lo='2017')} | {P.stats(r)[4]:.2f} | "
              f"{cell(book(name, h, s, hedge=True))} |")
    print(f"| SPY | {cell(P.SPY)} | {cell(P.SPY, hi='2016')} | {cell(P.SPY, lo='2017')} | 1.00 | {cell(P.hedged(P.SPY, P.FLAG100, 0.5))} |")


def section_grid():
    print("\n### Every holding / stop setting, after 0.10% costs (annual / Sharpe / worst drawdown)\n")
    print("| Book | Picks a sleeve | " + " | ".join(f"{h}m {s}" for h, s in CONFIGS) + " |\n|---|---|" + "---|" * len(CONFIGS))
    for name in PICK_BOOKS:
        for n in (2, 3):
            print(f"| {name} | {n} | " + " | ".join(cell(book(name, h, s, n)) for h, s in CONFIGS) + " |")
    for name in WHOLE_BOOKS:
        print(f"| {name} | all | " + " | ".join(cell(book(name, h, s)) for h, s in CONFIGS) + " |")


def regime_days():
    entries = [DAY_POS[ENTRY[m]] for m in MONTHS]
    out = [None]
    for j in range(1, NDAYS):
        i = bisect.bisect_right(entries, j - 1) - 1
        out.append(TS.basket(MONTHS[i]) if i >= 0 else None)
    return out


def section_regimes():
    reg = regime_days()
    print("\n### Each sleeve inside the yield regimes (1-month hold, no stop, before costs; annualised)\n")
    n_v = sum(x == "value" for x in reg[1:])
    print(f"Y6 said VALUE on {n_v / (NDAYS - 1) * 100:.0f}% of days.\n")
    print("| Sleeve | When Y6 says VALUE | When Y6 says GROWTH | All days |\n|---|---|---|---|")
    for name in ("GROWTH PICKS", "VALUE PICKS", "WHOLE GROWTH", "WHOLE VALUE"):
        r = book(name, 1, "NONE", costs=False)
        cells = []
        for want in ("value", "growth"):
            xs = [x for x, g in zip(r[1:], reg[1:]) if g == want]
            cells.append(f"{(math.prod(1 + x for x in xs) ** (252 / len(xs)) - 1) * 100:+.1f}%")
        print(f"| {name} | " + " | ".join(cells) + f" | {P.stats(r)[0] * 100:+.1f}% |")
    cells = []
    for want in ("value", "growth"):
        xs = [x for x, g in zip(P.SPY[1:], reg[1:]) if g == want]
        cells.append(f"{(math.prod(1 + x for x in xs) ** (252 / len(xs)) - 1) * 100:+.1f}%")
    print("| SPY | " + " | ".join(cells) + f" | {P.stats(P.SPY)[0] * 100:+.1f}% |")


def detail_rows():
    h, s = MAIN
    return [(name, book(name, h, s)) for name in ("COMBINED + YIELD TILT", "COMBINED 50/50", "YIELD SWITCH", "WHOLE SWITCH")] + [("SPY", P.SPY)]


def section_detail():
    rows = [(n, {**full_stats(r), "is_spy": n == "SPY"}) for n, r in detail_rows()]
    print(f"\n### Detailed statistics, main configuration ({MAIN[0]}-month hold, {MAIN[1]}, after costs)\n")
    print("| Statistic | " + " | ".join(n for n, _ in rows) + " |\n|---|" + "---|" * len(rows))
    f = {
        "Annual return": lambda s: f"{s['cagr'] * 100:+.1f}%",
        "Growth of $1": lambda s: f"${1 + s['total']:.1f}",
        "Volatility": lambda s: f"{s['vol'] * 100:.1f}%",
        "Sharpe": lambda s: f"{s['sharpe']:.2f}",
        "Sortino": lambda s: f"{s['sortino']:.2f}",
        "Worst drawdown": lambda s: f"{s['mdd'] * 100:.1f}%",
        "  peak / trough / recovered": lambda s: f"{s['mdd_peak']} / {s['mdd_trough']} / {s['mdd_recovered'] or 'not yet'}",
        "Longest under water": lambda s: f"{s['underwater_years']:.1f} yrs (from {s['underwater_from']})",
        "Calmar": lambda s: f"{s['calmar']:.2f}",
        "Beta / correlation to SPY": lambda s: f"{s['beta']:.2f} / {s['corr']:.2f}",
        "Months positive": lambda s: f"{s['hit'] * 100:.0f}%",
        "Months beating SPY": lambda s: "-" if s["is_spy"] else f"{s['beat_spy'] * 100:.0f}%",
        "Best / worst month": lambda s: f"{s['best_month'][1] * 100:+.1f}% ({s['best_month'][0]}) / {s['worst_month'][1] * 100:+.1f}% ({s['worst_month'][0]})",
        "Best / worst year": lambda s: f"{s['best_year'][1] * 100:+.1f}% ({s['best_year'][0]}) / {s['worst_year'][1] * 100:+.1f}% ({s['worst_year'][0]})",
        "Years positive": lambda s: f"{s['years_pos']} of {s['years']}",
        "2008-2016": lambda s: f"{s['first_half'][0] * 100:+.1f}% / {s['first_half'][2]:.2f} / {s['first_half'][3] * 100:.0f}%",
        "2017-2026": lambda s: f"{s['second_half'][0] * 100:+.1f}% / {s['second_half'][2]:.2f} / {s['second_half'][3] * 100:.0f}%",
    }
    for label, fn in f.items():
        print(f"| {label} | " + " | ".join(fn(s) for _, s in rows) + " |")


def section_years():
    rows = detail_rows()
    yrs = sorted({d[:4] for d in DAYS[1:]})
    print("\n### Calendar years, main configuration, after costs\n")
    print("| Year | Y6 share in VALUE | " + " | ".join(n for n, _ in rows) + " |\n|---|---|" + "---|" * len(rows))
    reg = regime_days()
    for y in yrs:
        idx = [j for j in range(1, NDAYS) if DAYS[j][:4] == y]
        share = sum(reg[j] == "value" for j in idx) / len(idx)
        print(f"| {y} | {share * 100:.0f}% | " + " | ".join(f"{compound([r[j] for j in idx]) * 100:+.1f}%" for _, r in rows) + " |")


def section_now():
    m = MONTHS[-1]
    fav = TS.basket(m)
    print(f"\n### The newest month ({m}, bought {ENTRY[m]}): Y6 favours {fav.upper()}\n")
    print(f"- growth sleeve (highest own P/E percentile): {', '.join(growth_sleeve(m, 2))} (third: {growth_sleeve(m, 3)[2]})")
    print(f"- value sleeve (largest 26-week EPS cut): {', '.join(value_sleeve(m, 2))} (third: {value_sleeve(m, 3)[2]})")
    w = weights("COMBINED + YIELD TILT", m)
    print("- COMBINED + YIELD TILT weights: " + ", ".join(f"{t} {x * 100:.1f}%" for t, x in sorted(w.items(), key=lambda kv: -kv[1])))
    for t in SS.BASKETS[m]["growth"] + SS.BASKETS[m]["value"]:
        print(f"  - {t}: own P/E pctl {BS.val(m, t, 'pe_pctl')}, e2_rev {BS.val(m, t, 'e2_rev')}, EPP gap {BS.val(m, t, 'epp_gap')}")


def write_json(path):
    rows = detail_rows() + [("GROWTH PICKS", book("GROWTH PICKS", *MAIN)), ("VALUE PICKS", book("VALUE PICKS", *MAIN))]
    week = [datetime.date.fromisoformat(d).isocalendar()[:2] for d in DAYS]
    keep = [j for j in range(NDAYS) if j == 0 or j == NDAYS - 1 or week[j] != week[j + 1]]   # each week's last day
    curves = {}
    for name, r in rows:
        v, pk, eq, dd = 1.0, 1.0, [], []
        for j, x in enumerate(r):
            v *= 1 + (x if j else 0.0)
            pk = max(pk, v)
            eq.append(v)
            dd.append(v / pk - 1)
        curves[name] = {"eq": [round(eq[j], 5) for j in keep], "dd": [round(dd[j], 5) for j in keep],
                        "years": by_period(r, lambda d: d[:4]), "months": by_period(r, lambda d: d[:7])}
    reg = [{"month": m, "from": ENTRY[m], "regime": TS.basket(m), "growth": growth_sleeve(m, 2), "value": value_sleeve(m, 2)}
           for m in MONTHS]
    stats = {name: {k: v for k, v in full_stats(r).items()} for name, r in rows}
    grid = {name: {f"{h}m {s}": P.stats(book(name, h, s))[:4] for h, s in CONFIGS} for name in PICK_BOOKS + WHOLE_BOOKS}
    rd = regime_days()
    by_regime = {}
    for name in ("GROWTH PICKS", "VALUE PICKS", "WHOLE GROWTH", "WHOLE VALUE", "SPY"):
        r = P.SPY if name == "SPY" else book(name, 1, "NONE", costs=False)
        by_regime[name] = {want: math.prod(1 + x for x, g in zip(r[1:], rd[1:]) if g == want) **
                           (252 / sum(g == want for g in rd[1:])) - 1 for want in ("value", "growth")}
    m = MONTHS[-1]
    now = {"month": m, "bought": ENTRY[m], "regime": TS.basket(m), "weights": weights("COMBINED + YIELD TILT", m),
           "members": {side: [{"t": t, "pe_pctl": BS.val(m, t, "pe_pctl"), "e2_rev": BS.val(m, t, "e2_rev"),
                               "epp_gap": BS.val(m, t, "epp_gap")} for t in SS.BASKETS[m][side]] for side in ("growth", "value")}}
    with open(path, "w") as fh:
        json.dump({"dates": [DAYS[j] for j in keep], "curves": curves, "regimes": reg, "stats": stats, "grid": grid,
                   "by_regime": by_regime, "now": now, "main": f"{MAIN[0]}-month hold, {MAIN[1]}, after 0.10% costs"}, fh)


SECTIONS = {"main": section_main, "grid": section_grid, "regimes": section_regimes, "detail": section_detail,
            "years": section_years, "now": section_now}

if __name__ == "__main__":
    args = sys.argv[1:]
    out = None
    if "--json" in args:
        i = args.index("--json")
        out = args[i + 1]
        args = args[:i] + args[i + 2:]
    print(f"HINDSIGHT (post-hoc selections; combined, then the yield filter). Daily {DAYS[0]} to {DAYS[-1]}.")
    for name in args or SECTIONS:
        SECTIONS[name]()
    if out:
        write_json(out)
