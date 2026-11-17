#!/usr/bin/env python3
"""
HINDSIGHT: the yield-switched growth/value book with a tilt inside each basket, held over several horizons, with 1-3
picks, and with stop-losses and re-entry. Prints the tables quoted in staging/retrospective/TILT_SWITCH.md.

The tilt itself is POST-HOC: it was chosen after basket_selection.py's near-misses (inside VALUE an EPS cut did better;
inside GROWTH the dearest against their own history did better). Everything below is a sweep around that one idea. Read
the grid for a stable region, not for its best cell.

THE GRID, fixed in this docstring before the first run; every cell is printed.
- Each month (ratio_b_basket.py's monthly entries, daily total-return data), style_switch.py's Y6 rule names the
  basket: VALUE when the 10-year yield is above its level 126 trading days earlier, otherwise GROWTH. A new cohort
  is bought from that basket:
  - VALUE picks: the members with the most negative e2_rev (the floor's EPS against 26 weeks earlier).
  - GROWTH picks: the highest own P/E percentile, ties broken by the EPP gap.
  - Selections: 1, 2 or 3 picks; WHOLE (every member); TILT (half WHOLE, half the 2 picks). Equal weight inside each.
- Holding: cohorts held 1, 3, 6 or 12 months. Live cohorts are re-weighted equally at each monthly entry and drift
  within the month.
- Stops, per position, on its total-return index. A signal at a close is traded at the next close, and the proceeds
  sit in cash.
  - NONE.
  - FIX15: exit at -15% from the entry; stay out for the rest of the cohort.
  - TRAIL15: exit at -15% from the highest close since entry; stay out.
  - TRAIL10/15/20 + MA50: exit at -10/-15/-20% from the peak; re-enter after a close above the 50-day average of the
    index, and the stop resets.
- Portfolio overlays, on the 2-pick and TILT books held 6 months: TREND (all to cash while the S&P 500 is below its
  100-day average, back in above it; next-close trades) and HEDGE50 (short 50% SPY while it is below; ratio_b_hedge.py).
- Stats: annual return, Sharpe, worst drawdown, beta, 2008-2016 and 2017-2026, stop exits a year, the share of time
  in cash. Then a 0.10% charge on each dollar traded (cohort turnover and stop trades, approximated), and calendar
  years for the main cells.

Everything printed is a label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule"). Reads only.

    python3 staging/retrospective/tilt_switch.py               # every table
    python3 staging/retrospective/tilt_switch.py grid stops     # selected sections

Sections: grid stops overlays years now (first run); short (added after it, labelled so)
"""
import bisect
import contextlib
import io
import math
import os
import statistics
import sys

os.environ["RETRO_UNIVERSE"] = "all"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import pe_pctl_hedge as P  # noqa: E402  (daily calendar, LEVEL, SPY, the S&P 100-day flags, stats)
    import basket_selection as BS  # noqa: E402  (readings per month and ticker, the baskets, the Y6 signal)
SS, PS = BS.SS, BS.PS
DAYS, MONTHS, LEVEL, DAY_POS = P.DAYS, P.MONTHS, P.LEVEL, P.DAY_POS
ENTRY = P.B.ENTRY
NDAYS = len(DAYS)
MA50 = {}
for t, lv in LEVEL.items():
    run, out = 0.0, []
    for j, v in enumerate(lv):
        run += v - (lv[j - 50] if j >= 50 else 0.0)
        out.append(run / 50 if j >= 49 else None)
    MA50[t] = out
SELECTIONS = ("1 pick", "2 picks", "3 picks", "TILT", "WHOLE")
HOLDS = (1, 3, 6, 12)
STOPS = (("NONE", None, None, False), ("FIX15", 0.15, "fixed", False), ("TRAIL15", 0.15, "trail", False),
         ("TRAIL10+MA50", 0.10, "trail", True), ("TRAIL15+MA50", 0.15, "trail", True), ("TRAIL20+MA50", 0.20, "trail", True))


def basket(m):
    return "value" if SS.SIG_B[m]["Y6"] == 1.0 else "growth"


def picks(m, n):
    b = basket(m)
    names = SS.BASKETS[m][b]
    if b == "value":
        pts = [(BS.val(m, t, "e2_rev"), t) for t in names]
        pts = sorted((v, t) for v, t in pts if v is not None)              # most negative first
    else:
        pts = [((BS.val(m, t, "pe_pctl") or -1, BS.val(m, t, "epp_gap") or -1e9), t) for t in names]
        pts = sorted(pts, reverse=True)
    chosen = [t for _, t in pts[:n]]
    return chosen or names[:n]


def weights(m, sel):
    names = SS.BASKETS[m][basket(m)]
    if sel == "WHOLE":
        return {t: 1 / len(names) for t in names}
    if sel == "TILT":
        w = {t: 0.5 / len(names) for t in names}
        for t in picks(m, 2):
            w[t] = w.get(t, 0.0) + 0.25
        return w
    n = int(sel[0])
    ch = picks(m, n)
    return {t: 1 / len(ch) for t in ch}


def cohort_path(ci, w, hold, stop):
    """The cohort's value from its entry day to its last day, and its stop exits and re-entries."""
    _, level, kind, reenter = stop
    e = DAY_POS[ENTRY[MONTHS[ci]]]
    end_i = ci + hold
    end = DAY_POS[ENTRY[MONTHS[end_i]]] if end_i < len(MONTHS) else NDAYS - 1
    total = [0.0] * (end - e + 1)
    exits = entries = 0
    cash_days = 0.0
    for t, x in w.items():
        L = LEVEL[t]
        held, val, ref, order = True, x, L[e], None
        total[0] += val
        for k, j in enumerate(range(e + 1, end + 1), start=1):
            if held:
                val *= L[j] / L[j - 1]
            if order == "sell":
                held, order = False, None
                exits += 1
            elif order == "buy":
                held, order, ref = True, None, L[j]
                entries += 1
            if level is not None:
                if held:
                    ref = max(ref, L[j]) if kind == "trail" else ref
                    if L[j] / ref - 1 <= -level:
                        order = "sell"
                elif reenter and MA50[t][j] is not None and L[j] > MA50[t][j]:
                    order = "buy"
            if not held:
                cash_days += x
            total[k] += val
    return e, total, exits, entries, cash_days / max(1, end - e)


def run(sel, hold, stop):
    W = {m: weights(m, sel) for m in MONTHS}
    paths, ex, en, cash = {}, 0, 0, []
    for ci, m in enumerate(MONTHS):
        e, total, a, b, c = cohort_path(ci, W[m], hold, stop)
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


def cell(r, lo=None, hi=None):
    c, _, sh, dd, _ = P.stats(r, lo, hi)
    return f"{c * 100:+.1f}% / {sh:.2f} / {dd * 100:.0f}%"


CACHE = {}


def get(sel, hold, stop):
    k = (sel, hold, stop[0])
    if k not in CACHE:
        CACHE[k] = run(sel, hold, stop)
    return CACHE[k]


def section_grid():
    print(f"\n### No stop: selection x holding period (annual return / Sharpe / worst drawdown, daily, {DAYS[0]} to {DAYS[-1]})\n")
    print("| Selection | Hold | 2008-2026 | 2008-2016 | 2017-2026 | Beta |\n|---|---|---|---|---|---|")
    for sel in SELECTIONS:
        for h in HOLDS:
            r, _ = get(sel, h, STOPS[0])
            print(f"| {sel} | {h}m | {cell(r)} | {cell(r, hi='2016')} | {cell(r, lo='2017')} | {P.stats(r)[4]:+.2f} |")
    print(f"| SPY | - | {cell(P.SPY)} | {cell(P.SPY, hi='2016')} | {cell(P.SPY, lo='2017')} | 1.00 |")


def section_stops():
    print("\n### Stops: full period, annual return / Sharpe / worst drawdown (stop exits a year; share of position-time in cash)\n")
    print("| Selection | Hold | " + " | ".join(s[0] for s in STOPS) + " |\n|---|---|" + "---|" * len(STOPS))
    for sel in SELECTIONS:
        for h in HOLDS:
            cells = []
            for st in STOPS:
                r, info = get(sel, h, st)
                extra = "" if st[0] == "NONE" else f" ({info['exits']:.1f}/yr, {info['cash'] * 100:.0f}% cash)"
                cells.append(cell(r) + extra)
            print(f"| {sel} | {h}m | " + " | ".join(cells) + " |")


def section_overlays():
    print("\n### Portfolio overlays on 6-month holds (annual return / Sharpe / worst drawdown)\n")
    print("| Selection | Stop | Overlay | 2008-2026 | 2008-2016 | 2017-2026 | After 0.10% costs |\n|---|---|---|---|---|---|---|")
    flags = P.FLAG100
    for sel in ("2 picks", "TILT", "WHOLE"):
        for st in (STOPS[0], STOPS[4]):
            r, info = get(sel, 6, st)
            for oname, f in (("none", lambda r: r), ("TREND (cash below the S&P 100-day)", lambda r: [x * (1 - fl) for x, fl in zip(r, flags)]),
                             ("HEDGE50", lambda r: P.hedged(r, flags, 0.5))):
                rr = f(r)
                cost = costed(rr, info, 6, oname != "none")
                print(f"| {sel} | {st[0]} | {oname} | {cell(rr)} | {cell(rr, hi='2016')} | {cell(rr, lo='2017')} | {cell(cost)} |")


def costed(r, info, hold, overlay, c=0.001):
    """Approximate costs: each month a cohort of 1/hold of the book is bought and one sold; each stop exit or re-entry
    trades its position (about 1/(hold x names) of the book); each overlay switch trades the whole book."""
    out = list(r)
    names = statistics.fmean(len(w) for w in info["W"].values())
    for m in MONTHS:
        j = bisect.bisect_right(DAYS, ENTRY[m])
        if j < len(out):
            out[j] -= c * 2 / hold
    per_day = c * (info["exits"] + info["entries"]) / (hold * names) / 252
    out = [x - per_day for x in out]
    if overlay:
        for j in range(1, len(out)):
            if P.FLAG100[j] != P.FLAG100[j - 1]:
                out[j] -= c
    return out


def section_years():
    cols = [("WHOLE 6m", get("WHOLE", 6, STOPS[0])[0]), ("TILT 6m", get("TILT", 6, STOPS[0])[0]),
            ("2 picks 6m", get("2 picks", 6, STOPS[0])[0]), ("2 picks 6m TRAIL15+MA50", get("2 picks", 6, STOPS[4])[0]),
            ("1 pick 6m", get("1 pick", 6, STOPS[0])[0]), ("SPY", P.SPY)]
    yrs = sorted({d[:4] for d in DAYS[1:]})
    print("\n### Calendar years\n")
    print("| Year | " + " | ".join(n for n, _ in cols) + " |\n|---|" + "---|" * len(cols))
    for y in yrs:
        print(f"| {y} | " + " | ".join(f"{(math.prod(1 + x for d, x in zip(DAYS[1:], r[1:]) if d[:4] == y) - 1) * 100:+.1f}%" for _, r in cols) + " |")
    print("| years positive | " + " | ".join(f"{sum(math.prod(1 + x for d, x in zip(DAYS[1:], r[1:]) if d[:4] == y) > 1 for y in yrs)} of {len(yrs)}" for _, r in cols) + " |")


def section_short():
    """Added after the first run: the 1- and 3-month holds came out best, so costs, the half hedge and calendar years
    for them (labelled where printed)."""
    print("\n### Added after the first run: 1- and 3-month holds with costs and the half hedge (annual / Sharpe / worst drawdown)\n")
    print("| Selection | Hold | Stop | Overlay | Before costs | After 0.10% costs | 2008-2016 | 2017-2026 |\n|---|---|---|---|---|---|---|---|")
    rows = []
    for sel in ("2 picks", "TILT", "WHOLE"):
        for h in (1, 3):
            for st in (STOPS[0], STOPS[2], STOPS[4]):
                r, info = get(sel, h, st)
                for oname, f in (("none", lambda r: r), ("HEDGE50", lambda r: P.hedged(r, P.FLAG100, 0.5))):
                    rr = f(r)
                    cc = costed(rr, info, h, oname != "none")
                    rows.append((sel, h, st[0], oname, cc))
                    print(f"| {sel} | {h}m | {st[0]} | {oname} | {cell(rr)} | {cell(cc)} | {cell(cc, hi='2016')} | {cell(cc, lo='2017')} |")
    pick_rows = [r for r in rows if (r[0], r[1], r[2], r[3]) in (("2 picks", 1, "TRAIL15", "none"), ("2 picks", 3, "TRAIL15+MA50", "HEDGE50"),
                                                                 ("TILT", 1, "TRAIL15", "none"), ("WHOLE", 1, "NONE", "none"))]
    yrs = sorted({d[:4] for d in DAYS[1:]})
    print("\n### Calendar years, after costs (added after the first run)\n")
    print("| Year | " + " | ".join(f"{a} {b}m {c} {d}" for a, b, c, d, _ in pick_rows) + " | SPY |\n|---|" + "---|" * (len(pick_rows) + 1))
    for y in yrs:
        cells = [f"{(math.prod(1 + x for dd, x in zip(DAYS[1:], r[1:]) if dd[:4] == y) - 1) * 100:+.1f}%" for *_, r in pick_rows]
        spy = math.prod(1 + x for dd, x in zip(DAYS[1:], P.SPY[1:]) if dd[:4] == y) - 1
        print(f"| {y} | " + " | ".join(cells) + f" | {spy * 100:+.1f}% |")


def section_now():
    m = MONTHS[-1]
    print(f"\n### The newest month ({m}): Y6 names {basket(m).upper()}\n")
    print(f"- basket: {', '.join(SS.BASKETS[m][basket(m)])}")
    for n in (1, 2, 3):
        print(f"- {n} pick(s): {', '.join(picks(m, n))}")
    for t in SS.BASKETS[m][basket(m)]:
        print(f"  - {t}: e2_rev {BS.val(m, t, 'e2_rev')}, own P/E pctl {BS.val(m, t, 'pe_pctl')}")


SECTIONS = {"grid": section_grid, "stops": section_stops, "overlays": section_overlays, "years": section_years, "now": section_now,
            "short": section_short}

if __name__ == "__main__":
    print(f"HINDSIGHT (post-hoc idea; a sweep). Daily {DAYS[0]} to {DAYS[-1]}.")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
