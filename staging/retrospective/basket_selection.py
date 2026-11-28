#!/usr/bin/env python3
"""
HINDSIGHT: selection inside the growth and value baskets of style_switch.py. Which point-in-time readings pick the better
members of each basket, and does picking them improve the yield-switched book? Prints the tables quoted in
staging/retrospective/BASKET_SELECTION.md.

THE PROCEDURE, fixed in this docstring before the first run.
- Baskets: style_switch.py's monthly GROWTH and VALUE baskets (about seven names each, out of twenty-four).
- Readings, all public by the as-of date:
  - from pattern_search_24.py: rb, epp_gap, base_up, adj_gap, cons2y, proxy, pe_pctl, eps_fy_g, eps_q_g, chg_1m,
    mom_12_1, dd_52w, vol, dy;
  - dgap26: the EPP gap's change over 26 weeks;
  - e2_rev: the floor's EPS (guide or last year) against 26 weeks earlier, split-adjusted;
  - eps_accel: the latest quarter's year-on-year EPS growth minus the previous quarter's (retro/facts prints);
  - eps_downyears: the number of falls among the last ten EPS_NORM steps (fewer = steadier);
  - peg: P/E (price / EPP_TODAY_EPS) over the 5-year EPS growth in percent, when both are positive;
  - div_g: trailing-12-month dividends against the 12 months before (Yahoo);
  - durable: 1 if the business kind is DURABLE.
  - Growth ratios are clipped to +-300%.
- Test:
  - Inside each basket, each month, the Spearman rank correlation (IC) between a reading and the next six months'
    return of the basket's members; 6 or more members with the reading.
  - Mean IC and Newey-West t (lag 6) over 2008-2026, the mean in each half (2008-2016, 2017-2026), and the IC against
    the next month's return as a check.
  - A reading REPLICATES in a basket if its mean IC has the same sign in both halves and |t| >= 2 over the full period.
- Books, for replicating readings only, in the direction of the sign:
  - the basket's best three, equal weight, rebalanced monthly, against the whole basket;
  - the yield-switched book: hold the best three of the basket the Y6 rule names that month (value when the 10-year
    yield is above its level 126 trading days earlier), against switching whole baskets (style_switch.py's Y6 book).
- With 40-odd tests, a couple of false passes are expected. Treat every pass as a hypothesis.

Everything printed is a label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule"). Reads only.

    python3 staging/retrospective/basket_selection.py               # every table
    python3 staging/retrospective/basket_selection.py ic books      # selected sections

Sections: ic books now (first run); posthoc (added after it, labelled so)
"""
import ast
import bisect
import contextlib
import datetime as dt
import io
import json
import math
import os
import re
import statistics
import sys

os.environ["RETRO_UNIVERSE"] = "all"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import pattern_search_24 as PS  # noqa: E402  (ROWS: readings and forward returns per month and ticker)
    import style_switch as SS  # noqa: E402  (BASKETS, the Y6 signal)
    import epp_short as ES  # noqa: E402  (eps_now and the EPP gap change on every row)
B, X = PS.B, PS.X
MONTHS, FIRST, RET = B.MONTHS, B.FIRST, B.RET
HALF_A = [m for m in MONTHS if m <= "2016-12"]
HALF_B = [m for m in MONTHS if m >= "2017-01"]
EPS_NORM_RE = re.compile(r"^EPS_NORM\s*=\s*(\{[^}]*\})", re.M)
EPS_TODAY_RE = re.compile(r"^EPP_TODAY_EPS\s*=\s*(-?[0-9.]+)", re.M)
clip = lambda v: None if v is None else max(-3.0, min(3.0, v))

# facts prints for EPS acceleration
QP = {}
for t in X.ALL:
    d = json.load(open(os.path.join(X.ROOT, "retro", "facts", f"{t}.json")))
    QP[t] = sorted((p["published"], p["eps_q"], p["eps_q_prior"]) for p in d["prints"]
                   if isinstance(p.get("eps_q"), (int, float)) and isinstance(p.get("eps_q_prior"), (int, float)))
BY_T = {}
for r in ES.X.R:
    BY_T.setdefault(r["ticker"], {})[r["date"]] = r


def extra(t, a_of, row):
    """The readings this script adds to pattern_search_24.py's."""
    r = ES.ROW[(t, a_of)]
    out = {"dgap26": r.get("dgap26"), "durable": 1.0 if row.get("kind") == "DURABLE" else 0.0}
    by = BY_T[t]
    target = r["date"] - dt.timedelta(weeks=26)
    hit = next((by[target + dt.timedelta(days=k)] for k in sorted(range(-6, 7), key=abs) if target + dt.timedelta(days=k) in by), None)
    out["e2_rev"] = None
    if hit and hit["eps_now"] > 0:
        ratio = math.prod(x for e, x in X.splits(t) if hit["date"] < e <= r["date"])
        out["e2_rev"] = clip(r["eps_now"] / (hit["eps_now"] / ratio) - 1)
    qs = [q for q in QP[t] if q[0] <= a_of]
    g = lambda q: (q[1] - q[2]) / abs(q[2]) if q[2] else None
    out["eps_accel"] = clip(g(qs[-1]) - g(qs[-2])) if len(qs) >= 2 and g(qs[-1]) is not None and g(qs[-2]) is not None else None
    src = open(os.path.join(X.ROOT, X.SERIES[t], a_of, "model.py"), encoding="utf-8").read()
    hist = ast.literal_eval(EPS_NORM_RE.search(src).group(1))
    ys = sorted(hist)[-11:]
    out["eps_downyears"] = float(sum(hist[b] < hist[a] for a, b in zip(ys, ys[1:]))) if len(ys) >= 6 else None
    eps = float(EPS_TODAY_RE.search(src).group(1))
    a = json.load(open(os.path.join(X.ROOT, X.SERIES[t], a_of, "analysis.json")))
    full = sorted(hist)
    g5 = (hist[full[-1]] / hist[full[-1] - 5]) ** 0.2 - 1 if (full[-1] - 5) in hist and hist[full[-1]] > 0 and hist[full[-1] - 5] > 0 else None
    out["peg"] = (a["price"] / eps) / (g5 * 100) if eps > 0 and g5 and g5 > 0 else None
    closes, divs = PS.PX[t]
    d0 = dt.date.fromisoformat(a_of)
    s1, s2 = (d0 - dt.timedelta(days=365)).isoformat(), (d0 - dt.timedelta(days=730)).isoformat()
    now = sum(v for d, v in divs if s1 < d <= a_of)
    before = sum(v for d, v in divs if s2 < d <= s1)
    out["div_g"] = clip(now / before - 1) if before > 0 else None
    return out


for (m, t), row in PS.ROWS.items():
    row.update(extra(t, FIRST[m][t]["as_of"], row))
    row["f1"] = RET[m][t]

SIGNALS = ("rb", "epp_gap", "dgap26", "pe_pctl", "base_up", "adj_gap", "cons2y", "proxy", "durable",
           "eps_q_g", "eps_accel", "eps_fy_g", "e2_rev", "eps_downyears", "peg", "div_g",
           "chg_1m", "mom_12_1", "dd_52w", "vol", "dy")
BASKET_NAMES = ("value", "growth")


def val(m, t, sig):
    v = PS.ROWS[(m, t)].get(sig)
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None
    return 1e9 if v == math.inf else v


def ic(sig, basket, months, target="f6"):
    out = []
    for m in months:
        pts = [(val(m, t, sig), PS.ROWS[(m, t)].get(target)) for t in SS.BASKETS[m][basket]]
        pts = [(x, y) for x, y in pts if x is not None and y is not None]
        if len(pts) >= 6 and len({x for x, _ in pts}) > 1:
            out.append(X.spearman([x for x, _ in pts], [y for _, y in pts]))
    return out


def result(sig, basket):
    full = ic(sig, basket, MONTHS)
    a, b = ic(sig, basket, HALF_A), ic(sig, basket, HALF_B)
    f1 = ic(sig, basket, MONTHS, "f1")
    t = PS.nw_t(full) if len(full) > 10 else 0.0
    ma, mb = (statistics.fmean(a) if a else 0.0), (statistics.fmean(b) if b else 0.0)
    ok = len(full) > 60 and ((ma > 0 and mb > 0) or (ma < 0 and mb < 0)) and abs(t) >= 2
    return {"full": statistics.fmean(full) if full else 0.0, "a": ma, "b": mb, "t": t, "n": len(full), "f1": statistics.fmean(f1) if f1 else 0.0,
            "pos": (sum(x > 0 for x in full) / len(full)) if full else 0.0, "ok": ok}


RES = {(s, b): result(s, b) for s in SIGNALS for b in BASKET_NAMES}


def section_ic():
    for b in BASKET_NAMES:
        print(f"\n### Inside the {b.upper()} basket: IC with the members' next six months (+ = a higher reading did better)\n")
        print("| Reading | Months | 2008-2016 | 2017-2026 | Full | t (NW) | Months above 0 | Next month's IC | Replicates? |\n|---|---|---|---|---|---|---|---|---|")
        for s in sorted(SIGNALS, key=lambda s: -abs(RES[(s, b)]["t"])):
            r = RES[(s, b)]
            print(f"| {s} | {r['n']} | {r['a']:+.3f} | {r['b']:+.3f} | {r['full']:+.3f} | {r['t']:+.2f} | {100 * r['pos']:.0f}% | {r['f1']:+.3f} | "
                  f"{'**YES**' if r['ok'] else 'no'} |")


def pick(m, basket, sig, sign, n=3):
    pts = [(val(m, t, sig), t) for t in SS.BASKETS[m][basket]]
    pts = [(sign * v, t) for v, t in pts if v is not None]
    pts.sort(reverse=True)
    return [t for _, t in pts[:n]] or SS.BASKETS[m][basket][:n]


def stats(xs):
    g = math.prod(1 + x for x in xs)
    mu, sd = statistics.fmean(xs), statistics.pstdev(xs)
    v, pk, mdd = 1.0, 1.0, 0.0
    for x in xs:
        v *= 1 + x
        pk = max(pk, v)
        mdd = min(mdd, v / pk - 1)
    return f"{(g ** (12 / len(xs)) - 1) * 100:+.1f}% / {(mu / sd * math.sqrt(12) if sd else 0):.2f} / {mdd * 100:.0f}%"


def section_books():
    reps = [(s, b, 1 if RES[(s, b)]["full"] > 0 else -1) for s in SIGNALS for b in BASKET_NAMES if RES[(s, b)]["ok"]]
    print("\n### Replicating readings: " + (", ".join(f"{s} in {b} ({'+' if g > 0 else '-'})" for s, b, g in reps) or "none"))
    whole = {b: {m: statistics.fmean(RET[m][t] for t in SS.BASKETS[m][b]) for m in MONTHS} for b in BASKET_NAMES}
    print("\n### Inside one basket: the best three against the whole basket, rebalanced monthly (annual / Sharpe / worst drawdown)\n")
    print("| Basket | Book | 2008-2026 | 2008-2016 | 2017-2026 |\n|---|---|---|---|---|")
    for b in BASKET_NAMES:
        s = whole[b]
        print(f"| {b} | whole basket | {stats([s[m] for m in MONTHS])} | {stats([s[m] for m in HALF_A])} | {stats([s[m] for m in HALF_B])} |")
        for sig, bb, g in reps:
            if bb != b:
                continue
            x = {m: statistics.fmean(RET[m][t] for t in pick(m, b, sig, g)) for m in MONTHS}
            print(f"| {b} | best 3 by {sig} ({'+' if g > 0 else '-'}) | {stats([x[m] for m in MONTHS])} | {stats([x[m] for m in HALF_A])} | {stats([x[m] for m in HALF_B])} |")
    print("\n### The yield-switched book (Y6: value when the 10-year yield is above its level 6 months ago)\n")
    print("| Book | 2008-2026 | 2008-2016 | 2017-2026 |\n|---|---|---|---|")
    sw = {m: whole["value"][m] if SS.SIG_B[m]["Y6"] == 1.0 else whole["growth"][m] for m in MONTHS}
    print(f"| switch whole baskets (style_switch.py) | {stats([sw[m] for m in MONTHS])} | {stats([sw[m] for m in HALF_A])} | {stats([sw[m] for m in HALF_B])} |")
    by_basket = {b: [(s, g) for s, bb, g in reps if bb == b] for b in BASKET_NAMES}
    combos = []
    for vs in by_basket["value"] or [(None, 0)]:
        for gs in by_basket["growth"] or [(None, 0)]:
            combos.append((vs, gs))
    for (vsig, vg), (gsig, gg) in combos:
        def leg(m, b, sig, g):
            return statistics.fmean(RET[m][t] for t in (pick(m, b, sig, g) if sig else SS.BASKETS[m][b]))
        x = {m: leg(m, "value", vsig, vg) if SS.SIG_B[m]["Y6"] == 1.0 else leg(m, "growth", gsig, gg) for m in MONTHS}
        lab = f"switch: value {'best 3 by ' + vsig if vsig else 'whole'}; growth {'best 3 by ' + gsig if gsig else 'whole'}"
        print(f"| {lab} | {stats([x[m] for m in MONTHS])} | {stats([x[m] for m in HALF_A])} | {stats([x[m] for m in HALF_B])} |")
    spy = [RET[m]["SPY"] for m in MONTHS]
    print(f"| SPY | {stats(spy)} | {stats([RET[m]['SPY'] for m in HALF_A])} | {stats([RET[m]['SPY'] for m in HALF_B])} |")


def cohort_book(chooser, hold):
    """Monthly returns of overlapping cohorts held `hold` months; chooser(m) gives a cohort's names."""
    picks = {m: chooser(m) for m in MONTHS}
    end = dict(zip(MONTHS, B.ENDS))
    out = {}
    for j, m in enumerate(MONTHS):
        legs = [statistics.fmean(B.level(t, end[m]) / B.level(t, B.ENTRY[m]) - 1 for t in picks[c]) for c in MONTHS[max(0, j - hold + 1): j + 1]]
        out[m] = statistics.fmean(legs)
    return out


def section_posthoc():
    """POST-HOC (chosen after reading the ic and books tables): six-month holds, and a contrarian-value / strong-growth
    switch. Leads for a fresh test, not findings."""
    print("\n### POST-HOC: six-month holds, and a contrarian-value / strong-growth switch (chosen after the first run)\n")
    print("| Book | 2008-2026 | 2008-2016 | 2017-2026 |\n|---|---|---|---|")
    rows = (
        ("value, whole basket, 6m cohorts", lambda m: SS.BASKETS[m]["value"], 6),
        ("value, best 3 by peg (+), 6m cohorts", lambda m: pick(m, "value", "peg", 1), 6),
        ("value, best 3 by e2_rev (-: EPS just cut), 6m cohorts", lambda m: pick(m, "value", "e2_rev", -1), 6),
        ("growth, whole basket, 6m cohorts", lambda m: SS.BASKETS[m]["growth"], 6),
        ("growth, best 3 by pe_pctl (+), 6m cohorts", lambda m: pick(m, "growth", "pe_pctl", 1), 6),
    )
    books = {}
    for lab, ch, h in rows:
        x = cohort_book(ch, h)
        books[lab] = x
        print(f"| {lab} | {stats([x[m] for m in MONTHS])} | {stats([x[m] for m in HALF_A])} | {stats([x[m] for m in HALF_B])} |")
    for lab, vk, gk in (("switch on Y6: whole baskets, 6m cohorts", "value, whole basket, 6m cohorts", "growth, whole basket, 6m cohorts"),
                        ("switch on Y6: value EPS-cut best 3 / growth pe_pctl best 3, 6m cohorts",
                         "value, best 3 by e2_rev (-: EPS just cut), 6m cohorts", "growth, best 3 by pe_pctl (+), 6m cohorts")):
        x = {m: books[vk][m] if SS.SIG_B[m]["Y6"] == 1.0 else books[gk][m] for m in MONTHS}
        print(f"| {lab} | {stats([x[m] for m in MONTHS])} | {stats([x[m] for m in HALF_A])} | {stats([x[m] for m in HALF_B])} |")


def section_now():
    reps = [(s, b, 1 if RES[(s, b)]["full"] > 0 else -1) for s in SIGNALS for b in BASKET_NAMES if RES[(s, b)]["ok"]]
    m = MONTHS[-1]
    print(f"\n### The newest month ({m}); the Y6 rule says {'VALUE' if SS.SIG_B[m]['Y6'] == 1.0 else 'GROWTH'}\n")
    for b in BASKET_NAMES:
        print(f"- {b.upper()} basket: {', '.join(SS.BASKETS[m][b])}")
        for s, bb, g in reps:
            if bb == b:
                print(f"  - best 3 by {s} ({'+' if g > 0 else '-'}): {', '.join(pick(m, b, s, g))}")


SECTIONS = {"ic": section_ic, "books": section_books, "now": section_now, "posthoc": section_posthoc}

if __name__ == "__main__":
    print(f"HINDSIGHT. Baskets {MONTHS[0]} to {MONTHS[-1]}; {len(SIGNALS)} readings x 2 baskets.")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
