#!/usr/bin/env python3
"""
HINDSIGHT: the Ratio B long / falling-EPS short book on all twenty-four retrospective series, with the thirteen tickers built
after the strategy was designed (BKR, BMY, CAT, CMCSA, CTVA, F, KMI, LMT, MAR, NVDA, PFE, RCL, SO) as an out-of-sample test.
Also a few other patterns. Prints the tables quoted in staging/retrospective/RATIO_B_EPS_24.md.

THE RULES, fixed in this docstring before the first run on the thirteen; every strategy and pattern below is printed.
- Data: cross_ticker_oos.py with RETRO_UNIVERSE=all (set below), so the original eleven reproduce their earlier numbers.
  Monthly, on each ticker's first as-of date of the month, entered at the next trading day's close and held to the next
  month's entry; dividends reinvested, the shorts pay them (ratio_b_basket.py). No costs, borrow fees or cash interest.
- EPS filters, all point-in-time (audited in eps_pit_check.py):
  - E1: last fiscal year's reported EPS below the year before.
  - RQ: the latest released quarter's EPS below the same quarter a year earlier.
  - RB: RQ and E1, reported only.
  - E3: E1 and the floor's EPS (guide or last year) lower than 26 weeks earlier. Uses public company guidance.
- Universes:
  - ORIGINAL eleven (the strategy was designed on them);
  - NEW thirteen (built after; the out-of-sample test);
  - ALL twenty-four;
  - each also without tech (GICS Information Technology: AAPL, MSFT, AVGO, ACN, NVDA).
- Strategies (frozen from RATIO_B_EPS_LS.md and EPS_PIT_CHECK.md):
  - A: long the 3 lowest Ratio B, unhedged;
  - B (main): A plus a short sleeve of 50% in RB stocks, each cohort held 6 months, cash when a cohort is empty;
  - C: A plus a 50% E3 sleeve, 6 months, SPY when a cohort is empty;
  - D: A minus a static 50% SPY;
  - E: B with 6 long names.
  - Benchmarks: SPY, and EQUAL (every ticker in the universe, rebalanced monthly).
- Other patterns, each a long side plus a 50% short sleeve held 6 months (cash when empty). Shown for ORIGINAL and NEW
  side by side; nothing is chosen on NEW.
  - O1: long 3 lowest Ratio B; short the tickers above their BULL price (Ratio B inf).
  - O2: long 3 lowest Ratio B; short "expensive & running" (own P/E percentile >= 80 and 12-month change > +25%).
  - O3: long 3 lowest Ratio B; short RQ.
  - O4: long 3 lowest Ratio B among tickers not flagged RB; short RB.
  - O5: long the 3 furthest below their 52-week high (price only); short RB.
  - O6: long 3 lowest Ratio B among tickers whose latest quarter's EPS is NOT below a year earlier (not RQ); short RB.
- Checks:
  - each leg against EQUAL;
  - 200 runs of 3 random longs a month (seeded) with the same RB sleeve;
  - the halves 2008-2016 and 2017-2026;
  - each ticker left out (B on NEW and ALL);
  - calendar years;
  - the newest book.

Everything printed is a label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule"). Reads only; the first run needs the network (retro/.cache/, gitignored).

    python3 staging/retrospective/ratio_b_eps_24.py                    # every table
    python3 staging/retrospective/ratio_b_eps_24.py main patterns      # selected sections

Sections: main legs random halves patterns loo years now posthoc
(posthoc was added after reading the NEW results, and is labelled so where it prints: leads for a fresh test, not findings.)
"""
import contextlib
import io
import json
import math
import os
import random
import statistics
import sys

os.environ["RETRO_UNIVERSE"] = "all"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import epp_short as ES  # noqa: E402  (E1/E2 readings on every row; loads ratio_b_basket and cross_ticker_oos)
B, X = ES.B, ES.X
MONTHS, RET, FIRST = B.MONTHS, B.RET, B.FIRST
TECH = ("AAPL", "MSFT", "AVGO", "ACN", "NVDA")
ORIGINAL, NEW = X.DISCOVERY + X.TEST, X.LATER
ALL = ORIGINAL + NEW
nt = lambda u: tuple(t for t in u if t not in TECH)
UNIVERSES = (("ORIGINAL eleven", ORIGINAL), ("NEW thirteen", NEW), ("ALL twenty-four", ALL),
             ("ORIGINAL without tech", nt(ORIGINAL)), ("NEW without tech", nt(NEW)), ("ALL without tech", nt(ALL)))
HALF_A = [m for m in MONTHS if m <= "2016-12"]
HALF_B = [m for m in MONTHS if m >= "2017-01"]

# RQ from each fact sheet's prints: the latest release published by the as-of date
QP = {}
for t in ALL:
    d = json.load(open(os.path.join(X.ROOT, "retro", "facts", f"{t}.json")))
    QP[t] = sorted((p["published"], p["eps_q"], p["eps_q_prior"]) for p in d["prints"]
                   if isinstance(p.get("eps_q"), (int, float)) and isinstance(p.get("eps_q_prior"), (int, float)))
for r in X.R:
    qs = [q for q in QP[r["ticker"]] if q[0] <= r["as_of"]]
    r["rq_down"] = (qs[-1][1] < qs[-1][2]) if qs else None

E1 = lambda r: r["eps_last_down"]
RQ = lambda r: r["rq_down"] is True
RB = lambda r: RQ(r) and E1(r)
E3 = lambda r: E1(r) and r["eps_down26"] is True
INF = lambda r: math.isinf(FIRST_RB[(r["ticker"], r["as_of"])])
FIRST_RB = {(t, s["as_of"]): s["rb"] for m in MONTHS for t, s in FIRST[m].items()}


END = dict(zip(MONTHS, B.ENDS))


def ret(m, t):
    """The month's return; a short still held after its ticker's series ends (CTVA from October 2026) uses the price."""
    r = RET[m].get(t)
    return r if r is not None else B.level(t, END[m]) / B.level(t, B.ENTRY[m]) - 1


def row(t, m):
    return ES.ROW[(t, FIRST[m][t]["as_of"])]


def names_in(m, u):
    return [t for t in FIRST[m] if t in u]


def low_rb(n, exclude=None):
    def sel(m, names):
        pool = [t for t in names if not (exclude and exclude(row(t, m)))] or names
        return [s["ticker"] for s in sorted((FIRST[m][t] for t in pool), key=B.rank_key)[:n]]
    return sel


def deepest(n):
    return lambda m, names: sorted(names, key=lambda t: row(t, m)["dd_52w"])[:n]


def flagged(f):
    return lambda m, names: [t for t in names if f(row(t, m))]


def book(long_sel, short_sel, u, size=0.5, hold=6, empty="cash", spy_static=0.0):
    longs, shorts = {}, {}
    for m in MONTHS:
        nm = names_in(m, u)
        longs[m] = long_sel(m, nm)
        shorts[m] = short_sel(m, nm) if short_sel else []
    out = {}
    for j, m in enumerate(MONTHS):
        lr = statistics.fmean(RET[m][t] for t in longs[m])
        legs = []
        if short_sel:
            for c in MONTHS[max(0, j - hold + 1): j + 1]:
                legs.append(statistics.fmean(ret(m, t) for t in shorts[c]) if shorts[c] else (RET[m]["SPY"] if empty == "SPY" else 0.0))
        out[m] = lr - (size * statistics.fmean(legs) if legs else 0.0) - spy_static * RET[m]["SPY"]
    return out, longs, shorts


def stats(s, months=None):
    xs = [s[m] for m in (months or MONTHS)]
    n = len(xs)
    g = math.prod(1 + x for x in xs)
    mu, sd = statistics.fmean(xs), statistics.pstdev(xs)
    v, pk, mdd = 1.0, 1.0, 0.0
    for x in xs:
        v *= 1 + x
        pk = max(pk, v)
        mdd = min(mdd, v / pk - 1)
    return {"cagr": g ** (12 / n) - 1, "sharpe": mu / sd * math.sqrt(12) if sd else 0.0, "mdd": mdd, "vol": sd * math.sqrt(12)}


def beta(s):
    xs, ys = [s[m] for m in MONTHS], [RET[m]["SPY"] for m in MONTHS]
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((y - my) ** 2 for y in ys)


def pct(v):
    return f"{v * 100:+.1f}%"


def cell(s, months=None):
    st = stats(s, months)
    return f"{pct(st['cagr'])} / {st['sharpe']:.2f} / {st['mdd'] * 100:.0f}%"


def strategies(u):
    return {
        "SPY": {m: RET[m]["SPY"] for m in MONTHS},
        "EQUAL": {m: statistics.fmean(RET[m][t] for t in names_in(m, u)) for m in MONTHS},
        "A: long 3 lowest Ratio B": book(low_rb(3), None, u)[0],
        "**B: A + 50% RB short (reported EPS), 6m**": book(low_rb(3), flagged(RB), u)[0],
        "C: A + 50% E3 short (uses guidance), 6m, empty=SPY": book(low_rb(3), flagged(E3), u, empty="SPY")[0],
        "D: A - 50% SPY": book(low_rb(3), None, u, spy_static=0.5)[0],
        "E: long 6 lowest Ratio B + 50% RB short": book(low_rb(6), flagged(RB), u)[0],
    }


STRATS = {name: strategies(u) for name, u in UNIVERSES}


def section_main():
    for name, u in UNIVERSES:
        print(f"\n### {name} ({len(u)} tickers): annual return / Sharpe / worst drawdown (monthly data)\n")
        print("| Strategy | Full period | 2008-2016 | 2017-2026 | Beta to SPY |\n|---|---|---|---|---|")
        for k, s in STRATS[name].items():
            print(f"| {k} | {cell(s)} | {cell(s, HALF_A)} | {cell(s, HALF_B)} | {beta(s):+.2f} |")


def section_legs():
    print("\n### Each leg against EQUAL (mean monthly difference, annualised; share of months above)\n")
    print("| Universe | Long 3 lowest Ratio B minus EQUAL | RB names minus EQUAL (negative = a good short) | RQ names minus EQUAL | "
          "E3 names minus EQUAL | Above-BULL names minus EQUAL |\n|---|---|---|---|---|---|")
    for name, u in UNIVERSES:
        eq = STRATS[name]["EQUAL"]
        cells = []
        _, longs, _ = book(low_rb(3), None, u)
        d = [statistics.fmean(RET[m][t] for t in longs[m]) - eq[m] for m in MONTHS]
        cells.append(f"{statistics.fmean(d) * 1200:+.1f}%/yr ({100 * sum(x > 0 for x in d) / len(d):.0f}%)")
        for f in (RB, RQ, E3, INF):
            d = [statistics.fmean(RET[m][t] for t in ns) - eq[m] for m in MONTHS for ns in [[t for t in names_in(m, u) if f(row(t, m))]] if ns]
            cells.append(f"{statistics.fmean(d) * 1200:+.1f}%/yr ({100 * sum(x > 0 for x in d) / len(d):.0f}%, {len(d)} months)" if d else "-")
        print(f"| {name} | " + " | ".join(cells) + " |")


def section_random(runs=200):
    print(f"\n### 3 random longs a month ({runs} runs, seeded), unhedged and with the same 50% RB sleeve\n")
    print("| Universe | Random median, unhedged | Ratio B (A) | Runs at or above A | Random median + RB sleeve | Ratio B + RB (B) | Runs at or above B |")
    print("|---|---|---|---|---|---|---|")
    for name, u in UNIVERSES[:3]:
        rng = random.Random(20261117)
        ru, rh = [], []
        for _ in range(runs):
            pick = {m: rng.sample(sorted(names_in(m, u)), 3) for m in MONTHS}
            sel = lambda m, names, pick=pick: pick[m]
            ru.append(stats(book(sel, None, u)[0])["cagr"])
            rh.append(stats(book(sel, flagged(RB), u)[0])["cagr"])
        a = stats(STRATS[name]["A: long 3 lowest Ratio B"])["cagr"]
        b = stats(STRATS[name]["**B: A + 50% RB short (reported EPS), 6m**"])["cagr"]
        print(f"| {name} | {pct(statistics.median(ru))} | {pct(a)} | {sum(x >= a for x in ru)} of {runs} | {pct(statistics.median(rh))} | "
              f"{pct(b)} | {sum(x >= b for x in rh)} of {runs} |")


def section_halves():
    print("\n### Main strategy B by half, every universe (annual return / Sharpe / worst drawdown)\n")
    print("| Universe | 2008-2016 | 2017-2026 | A unhedged, 2008-2016 | A unhedged, 2017-2026 |\n|---|---|---|---|---|")
    for name, _ in UNIVERSES:
        s, a = STRATS[name]["**B: A + 50% RB short (reported EPS), 6m**"], STRATS[name]["A: long 3 lowest Ratio B"]
        print(f"| {name} | {cell(s, HALF_A)} | {cell(s, HALF_B)} | {cell(a, HALF_A)} | {cell(a, HALF_B)} |")


PATTERNS = (
    ("B (main): long 3 lowest Ratio B; short RB", lambda u: book(low_rb(3), flagged(RB), u)[0]),
    ("O1: long 3 lowest Ratio B; short above-BULL", lambda u: book(low_rb(3), flagged(INF), u)[0]),
    ("O2: long 3 lowest Ratio B; short expensive & running", lambda u: book(low_rb(3), flagged(X.EXPENSIVE_RUNNING), u)[0]),
    ("O3: long 3 lowest Ratio B; short RQ", lambda u: book(low_rb(3), flagged(RQ), u)[0]),
    ("O4: long 3 lowest Ratio B, RB barred; short RB", lambda u: book(low_rb(3, RB), flagged(RB), u)[0]),
    ("O5: long 3 deepest below the 52-week high; short RB", lambda u: book(deepest(3), flagged(RB), u)[0]),
    ("O6: long 3 lowest Ratio B, RQ barred; short RB", lambda u: book(low_rb(3, RQ), flagged(RB), u)[0]),
)


def section_patterns():
    for name, u in UNIVERSES:
        print(f"\n### Other patterns, {name} (annual return / Sharpe / worst drawdown)\n")
        print("| Pattern | Full period | 2008-2016 | 2017-2026 |\n|---|---|---|---|")
        for pname, f in PATTERNS:
            s = f(u)
            print(f"| {pname} | {cell(s)} | {cell(s, HALF_A)} | {cell(s, HALF_B)} |")


def section_loo():
    for name, u in (UNIVERSES[1], UNIVERSES[2], UNIVERSES[5]):
        cells = []
        for t in u:
            s = book(low_rb(3), flagged(RB), tuple(x for x in u if x != t))[0]
            st = stats(s)
            cells.append(f"no {t}: {pct(st['cagr'])} / {st['sharpe']:.2f}")
        print(f"\n- {name}, B with each ticker left out: " + "; ".join(cells))


def section_years():
    yrs = sorted({m[:4] for m in MONTHS})
    cols = [(n, STRATS[n]["**B: A + 50% RB short (reported EPS), 6m**"]) for n in ("NEW thirteen", "ALL twenty-four", "ALL without tech")]
    cols.append(("SPY", STRATS["ALL twenty-four"]["SPY"]))
    print("\n### Calendar years of B\n")
    print("| Year | " + " | ".join(n for n, _ in cols) + " |\n|---|" + "---|" * len(cols))
    for y in yrs:
        print(f"| {y} | " + " | ".join(pct(math.prod(1 + s[m] for m in MONTHS if m[:4] == y) - 1) for _, s in cols) + " |")
    print("| years positive | " + " | ".join(f"{sum(math.prod(1 + s[m] for m in MONTHS if m[:4] == y) > 1 for y in yrs)} of {len(yrs)}" for _, s in cols) + " |")


def section_now():
    m = MONTHS[-1]
    print(f"\n### The newest month ({m})\n")
    for name, u in UNIVERSES:
        nm = names_in(m, u)
        longs = low_rb(3)(m, nm)
        print(f"- {name}: long {', '.join(longs)}; RB short: {', '.join(flagged(RB)(m, nm)) or 'none'}; E3: {', '.join(flagged(E3)(m, nm)) or 'none'}")


def sleeve(sel, u, hold=6):
    """A long-only sleeve of the selected names, cohorts held `hold` months; an empty cohort holds EQUAL."""
    picks = {m: sel(m, names_in(m, u)) for m in MONTHS}
    out = {}
    for j, m in enumerate(MONTHS):
        eq = statistics.fmean(RET[m][t] for t in names_in(m, u))
        legs = [statistics.fmean(ret(m, t) for t in picks[c]) if picks[c] else eq for c in MONTHS[max(0, j - hold + 1): j + 1]]
        out[m] = statistics.fmean(legs)
    return out


POSTHOC = (
    ("H1: long 3 deepest below the 52-week high, unhedged", lambda u: book(deepest(3), None, u)[0]),
    ("H2: long every BUY-tier stock (Ratio B < 0.75), equal weight", lambda u: sleeve(flagged(lambda r: FIRST_RB[(r["ticker"], r["as_of"])] < 0.75), u, hold=1)),
    ("H3: long the falling-EPS stocks (RB), held 6 months", lambda u: sleeve(flagged(RB), u, hold=6)),
    ("H4: H1 minus a static 50% SPY", lambda u: book(deepest(3), None, u, spy_static=0.5)[0]),
)


def section_posthoc():
    print("\n### POST-HOC (chosen after reading the NEW results): leads for a fresh test, not findings\n")
    print("| Universe | Pattern | Full period | 2008-2016 | 2017-2026 | Beta | Versus EQUAL, full period |\n|---|---|---|---|---|---|---|")
    for name, u in (UNIVERSES[0], UNIVERSES[1], UNIVERSES[2], UNIVERSES[5]):
        eq = STRATS[name]["EQUAL"]
        print(f"| {name} | EQUAL (reference) | {cell(eq)} | {cell(eq, HALF_A)} | {cell(eq, HALF_B)} | {beta(eq):+.2f} | - |")
        for pname, f in POSTHOC:
            s = f(u)
            print(f"| {name} | {pname} | {cell(s)} | {cell(s, HALF_A)} | {cell(s, HALF_B)} | {beta(s):+.2f} | "
                  f"{pct(stats(s)['cagr'] - stats(eq)['cagr'])} |")


SECTIONS = {"main": section_main, "legs": section_legs, "random": section_random, "halves": section_halves,
            "patterns": section_patterns, "loo": section_loo, "years": section_years, "now": section_now,
            "posthoc": section_posthoc}

if __name__ == "__main__":
    print(f"HINDSIGHT. {len(X.ALL)} tickers ({len(X.R)} dates); months {MONTHS[0]} to {MONTHS[-1]}.")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
