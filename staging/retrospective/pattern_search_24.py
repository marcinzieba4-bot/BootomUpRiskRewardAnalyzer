#!/usr/bin/env python3
"""
HINDSIGHT: a disciplined pattern search over the twenty-four retrospective series. Which point-in-time readings rank
stocks' next six months correctly, in every part of the sample? Prints the tables quoted in
staging/retrospective/PATTERN_SEARCH_24.md.

THE PROCEDURE, fixed in this docstring before the first run.
- Rows: each ticker's first as-of date of each month (ratio_b_basket.py with RETRO_UNIVERSE=all). Entry is at the next
  trading day's close. Target: the total return over the next 126 trading days (six months), and over 252 (twelve
  months) as a check.
- Signals, all public by the as-of date:
  - from analysis.json:
    - rb (Ratio B);
    - epp_gap;
    - base_up (BASE scenario price / price - 1);
    - adj_gap (the house model-vs-market gap);
    - cons2y (the house's conservative two-year return);
    - proxy (the business-dashboard composite);
    - obsol (obsolescence risk, 1-5);
  - from model.py: pe_pctl (own 10-year P/E percentile); eps_fy_g (growth of the last fiscal year's EPS over the year
    before);
  - from retro/facts prints: eps_q_g (the latest released quarter's EPS against the same quarter a year earlier);
  - from Yahoo closes up to the as-of date:
    - chg_1m (21 trading days);
    - chg_12m (252);
    - mom_12_1 (12 months excluding the last one);
    - dd_52w (the close against the 252-day high);
    - vol (252-day realised volatility);
    - dy (dividends with an ex-date in the 365 days before, over the price).
  - The growth ratios divide by the absolute base and are clipped to +-300%.
- Test: each month, the Spearman rank correlation (IC) between a signal and the forward return across the stocks in a
  universe (8 or more stocks). Mean IC, Newey-West t (lag 6, the overlap of six-month windows) and the share of months
  above zero.
- Cells: ORIGINAL eleven and NEW thirteen, each over 2008-2016 (A) and 2017-2026 (B), plus ALL twenty-four.
- A signal REPLICATES if its mean IC has the same sign in all four cells (ORIGINAL-A, ORIGINAL-B, NEW-A, NEW-B) and its
  ALL-twenty-four t-stat over the full period is 2 or more in size.
- Portfolios, only for signals that replicate, in the direction of the sign:
  - long the 3 best-ranked of ALL twenty-four each month, cohorts held 6 months (and 1 month);
  - the long-short (best 3 minus worst 3, 6 months).
  - Each against EQUAL (all twenty-four), with halves and the ORIGINAL / NEW universes on their own.
  - A COMPOSITE (the average of the replicating signals' monthly rank percentiles, signed) is run the same way.
- Within each ticker's own series: the rank correlation of each signal with its forward six-month return, and the
  count of tickers with each sign (supplementary).

Everything printed is a label or a hypothesis: nothing here may enter a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule"). Reads only.

    python3 staging/retrospective/pattern_search_24.py               # every table
    python3 staging/retrospective/pattern_search_24.py ic portfolios # selected sections

Sections: ic within portfolios composite now (first run); capm years posthoc (added after reading it, labelled so)
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
    import ratio_b_basket as B  # noqa: E402
X, rt = B.X, B.rt
MONTHS, FIRST = B.MONTHS, B.FIRST
ORIGINAL, NEW = X.DISCOVERY + X.TEST, X.LATER
ALL = ORIGINAL + NEW
HALF_A = [m for m in MONTHS if m <= "2016-12"]
HALF_B = [m for m in MONTHS if m >= "2017-01"]
DAYS = B.DAYS
EPS_NORM_RE = re.compile(r"^EPS_NORM\s*=\s*(\{[^}]*\})", re.M)
SIGNALS = ("rb", "epp_gap", "base_up", "adj_gap", "cons2y", "proxy", "obsol", "pe_pctl", "eps_fy_g", "eps_q_g",
           "chg_1m", "chg_12m", "mom_12_1", "dd_52w", "vol", "dy")

PX = {t: rt.fetch_prices(t) for t in ALL}
PXK = {t: sorted(PX[t][0]) for t in ALL}
QP = {}
for t in ALL:
    d = json.load(open(os.path.join(X.ROOT, "retro", "facts", f"{t}.json")))
    QP[t] = sorted((p["published"], p["eps_q"], p["eps_q_prior"]) for p in d["prints"]
                   if isinstance(p.get("eps_q"), (int, float)) and isinstance(p.get("eps_q_prior"), (int, float)))


def growth(new, old):
    if old is None or new is None or old == 0:
        return None
    return max(-3.0, min(3.0, (new - old) / abs(old)))


def features(t, s):
    """The point-in-time readings of ticker t on its as-of date s['as_of']."""
    a_of = s["as_of"]
    folder = os.path.join(X.ROOT, X.SERIES[t], a_of)
    a = json.load(open(os.path.join(folder, "analysis.json")))
    m = a["metrics"]
    src = open(os.path.join(folder, "model.py"), encoding="utf-8").read()
    hist = ast.literal_eval(EPS_NORM_RE.search(src).group(1))
    ys = sorted(hist)
    r = ROWMAP[(t, a_of)]
    closes, divs = PX[t]
    ks = PXK[t]
    i = bisect.bisect_right(ks, a_of) - 1
    c = lambda k: closes[ks[k]]
    lr = [math.log(c(k) / c(k - 1)) for k in range(max(1, i - 251), i + 1)]
    qs = [q for q in QP[t] if q[0] <= a_of]
    start = (dt.date.fromisoformat(a_of) - dt.timedelta(days=365)).isoformat()
    f = {"rb": m["ratio_b"], "epp_gap": m["epp_gap_pct"], "base_up": m["scenarios"]["BASE"]["price"] / a["price"] - 1,
         "adj_gap": m["adj_gap"], "cons2y": m.get("cons_return_2yr"), "proxy": m["proxy_composite"],
         "obsol": a["classification"].get("obsolescence_risk"), "pe_pctl": r["pe_pctl"],
         "eps_fy_g": growth(hist[ys[-1]], hist[ys[-2]]) if len(ys) >= 2 else None,
         "eps_q_g": growth(qs[-1][1], qs[-1][2]) if qs else None,
         "chg_1m": c(i) / c(i - 21) - 1 if i >= 21 else None, "chg_12m": c(i) / c(i - 252) - 1 if i >= 252 else None,
         "mom_12_1": c(i - 21) / c(i - 252) - 1 if i >= 252 else None,
         "dd_52w": c(i) / max(c(k) for k in range(max(0, i - 251), i + 1)) - 1,
         "vol": statistics.pstdev(lr) * math.sqrt(252) if len(lr) > 20 else None,
         "dy": sum(v for d, v in divs if start < d <= a_of) / c(i)}
    return f


ROWMAP = {(r["ticker"], r["as_of"]): r for r in X.R}
ROWS = {}                                                        # (month, ticker) -> features + forward returns
for mo in MONTHS:
    for t, s in FIRST[mo].items():
        f = features(t, s)
        e = bisect.bisect_right(DAYS, s["as_of"])
        for n, key in ((126, "f6"), (252, "f12")):
            if e + n < len(DAYS):
                f[key] = B.level(t, DAYS[e + n]) / B.level(t, DAYS[e]) - 1
        f["kind"] = ROWMAP[(t, s["as_of"])]["kind"]
        ROWS[(mo, t)] = f


def ic_series(sig, u, months, target="f6"):
    out = []
    for mo in months:
        pts = [(ROWS[(mo, t)][sig], ROWS[(mo, t)][target]) for t in FIRST[mo] if t in u
               and ROWS[(mo, t)].get(sig) is not None and target in ROWS[(mo, t)]]
        pts = [(x, y) for x, y in pts if not (isinstance(x, float) and math.isnan(x))]
        if len(pts) >= 8:
            out.append(X.spearman([x for x, _ in pts], [y for _, y in pts]))
    return out


def nw_t(xs, lag=6):
    n = len(xs)
    if n < 10:
        return 0.0
    mu = statistics.fmean(xs)
    d = [x - mu for x in xs]
    s = sum(v * v for v in d) / n
    for k in range(1, lag + 1):
        s += 2 * (1 - k / (lag + 1)) * sum(d[i] * d[i - k] for i in range(k, n)) / n
    return mu / math.sqrt(s / n) if s > 0 else 0.0


CELLS = (("ORIGINAL 2008-16", ORIGINAL, HALF_A), ("ORIGINAL 2017-26", ORIGINAL, HALF_B),
         ("NEW 2008-16", NEW, HALF_A), ("NEW 2017-26", NEW, HALF_B))


def replicating():
    out = []
    for sig in SIGNALS:
        means = [statistics.fmean(v) if (v := ic_series(sig, u, ms)) else 0.0 for _, u, ms in CELLS]
        full = ic_series(sig, ALL, MONTHS)
        t = nw_t(full)
        same = all(x > 0 for x in means) or all(x < 0 for x in means)
        out.append((sig, means, statistics.fmean(full), t, same and abs(t) >= 2))
    return out


REP = replicating()


def section_ic():
    print("\n### Monthly cross-sectional rank correlation with the next six months' return (+ = a higher reading did better)\n")
    print("| Signal | " + " | ".join(c for c, _, _ in CELLS) + " | ALL 24: mean IC | t (NW) | months above 0 | 12m target: mean IC / t | Replicates? |")
    print("|---|" + "---|" * (len(CELLS) + 5))
    for sig, means, full, t, ok in REP:
        f = ic_series(sig, ALL, MONTHS)
        f12 = ic_series(sig, ALL, MONTHS, "f12")
        print(f"| {sig} | " + " | ".join(f"{x:+.3f}" for x in means) + f" | {full:+.3f} | {t:+.2f} | {100 * sum(x > 0 for x in f) / len(f):.0f}% | "
              f"{statistics.fmean(f12):+.3f} / {nw_t(f12, 12):+.2f} | {'**YES**' if ok else 'no'} |")


def section_within():
    print("\n### Within each ticker's own series: rank correlation of the signal with its own next six months (count of tickers)\n")
    print("| Signal | Tickers positive | Tickers negative | Median correlation |\n|---|---|---|---|")
    for sig in SIGNALS:
        cs = []
        for t in ALL:
            pts = [(ROWS[(mo, t)][sig], ROWS[(mo, t)]["f6"]) for mo in MONTHS if (mo, t) in ROWS
                   and ROWS[(mo, t)].get(sig) is not None and "f6" in ROWS[(mo, t)]]
            if len(pts) >= 24:
                cs.append(X.spearman([x for x, _ in pts], [y for _, y in pts]))
        print(f"| {sig} | {sum(c > 0 for c in cs)} | {sum(c < 0 for c in cs)} | {statistics.median(cs):+.2f} |")


def score_book(score, u, hold, n=3, worst=False):
    """Monthly returns of a book long the n best (or worst) by score, cohorts held `hold` months."""
    picks = {}
    for mo in MONTHS:
        pts = [(score(mo, t), t) for t in FIRST[mo] if t in u and score(mo, t) is not None]
        pts.sort(reverse=not worst)
        picks[mo] = [t for _, t in pts[:n]]
    out = {}
    end = dict(zip(MONTHS, B.ENDS))
    for j, mo in enumerate(MONTHS):
        legs = []
        for c in MONTHS[max(0, j - hold + 1): j + 1]:
            if picks[c]:
                legs.append(statistics.fmean(B.level(t, end[mo]) / B.level(t, B.ENTRY[mo]) - 1 for t in picks[c]))
        out[mo] = statistics.fmean(legs) if legs else 0.0
    return out, picks


def stats(s, months=None):
    xs = [s[m] for m in (months or MONTHS)]
    g = math.prod(1 + x for x in xs)
    mu, sd = statistics.fmean(xs), statistics.pstdev(xs)
    v, pk, mdd = 1.0, 1.0, 0.0
    for x in xs:
        v *= 1 + x
        pk = max(pk, v)
        mdd = min(mdd, v / pk - 1)
    return g ** (12 / len(xs)) - 1, (mu / sd * math.sqrt(12) if sd else 0.0), mdd


def cell(s, months=None):
    c, sh, dd = stats(s, months)
    return f"{c * 100:+.1f}% / {sh:.2f} / {dd * 100:.0f}%"


def equal(u):
    end = dict(zip(MONTHS, B.ENDS))
    return {mo: statistics.fmean(B.level(t, end[mo]) / B.level(t, B.ENTRY[mo]) - 1 for t in FIRST[mo] if t in u) for mo in MONTHS}


def signed(sig, sign):
    def f(mo, t):
        v = ROWS[(mo, t)].get(sig)
        if v is None or (isinstance(v, float) and math.isnan(v)):
            return None
        return sign * (1e9 if v == math.inf else -1e9 if v == -math.inf else v)
    return f


def section_portfolios():
    reps = [(sig, 1 if full > 0 else -1) for sig, _, full, _, ok in REP if ok]
    print(f"\n### Portfolios on the replicating signals: {', '.join(f"{s} ({'+' if g > 0 else '-'})" for s, g in reps) or 'none'}\n")
    if not reps:
        return
    print("| Signal | Book | ALL 24: full period | 2008-2016 | 2017-2026 | ORIGINAL only | NEW only |\n|---|---|---|---|---|---|---|")
    for lab, u in (("EQUAL (reference)", None),):
        print(f"| - | {lab} | {cell(equal(ALL))} | {cell(equal(ALL), HALF_A)} | {cell(equal(ALL), HALF_B)} | {cell(equal(ORIGINAL))} | {cell(equal(NEW))} |")
    for sig, g in reps:
        for hold in (6, 1):
            s = score_book(signed(sig, g), ALL, hold)[0]
            so = score_book(signed(sig, g), ORIGINAL, hold)[0]
            sn = score_book(signed(sig, g), NEW, hold)[0]
            print(f"| {sig} | long best 3, hold {hold}m | {cell(s)} | {cell(s, HALF_A)} | {cell(s, HALF_B)} | {cell(so)} | {cell(sn)} |")
        best = score_book(signed(sig, g), ALL, 6)[0]
        worst = score_book(signed(sig, g), ALL, 6, worst=True)[0]
        ls = {m: best[m] - worst[m] for m in MONTHS}
        print(f"| {sig} | best 3 minus worst 3, 6m | {cell(ls)} | {cell(ls, HALF_A)} | {cell(ls, HALF_B)} | - | - |")


def section_composite():
    reps = [(sig, 1 if full > 0 else -1) for sig, _, full, _, ok in REP if ok]
    if len(reps) < 2:
        print("\n### Composite: fewer than two replicating signals; not built\n")
        return

    def comp(mo, t, u=ALL):
        names = [x for x in FIRST[mo] if x in u]
        tot, n = 0.0, 0
        for sig, g in reps:
            vals = [(signed(sig, g)(mo, x), x) for x in names]
            vals = [(v, x) for v, x in vals if v is not None]
            if not vals or signed(sig, g)(mo, t) is None:
                continue
            order = sorted(v for v, _ in vals)
            tot += bisect.bisect_left(order, signed(sig, g)(mo, t)) / max(1, len(order) - 1)
            n += 1
        return tot / n if n else None
    print(f"\n### Composite of {', '.join(s for s, _ in reps)} (average signed rank percentile)\n")
    print("| Book | ALL 24: full period | 2008-2016 | 2017-2026 | ORIGINAL only | NEW only |\n|---|---|---|---|---|---|")
    for hold in (6, 1):
        s = score_book(comp, ALL, hold)[0]
        so = score_book(lambda mo, t: comp(mo, t, ORIGINAL), ORIGINAL, hold)[0]
        sn = score_book(lambda mo, t: comp(mo, t, NEW), NEW, hold)[0]
        print(f"| long best 3, hold {hold}m | {cell(s)} | {cell(s, HALF_A)} | {cell(s, HALF_B)} | {cell(so)} | {cell(sn)} |")
    best, worst = score_book(comp, ALL, 6)[0], score_book(comp, ALL, 6, worst=True)[0]
    ls = {m: best[m] - worst[m] for m in MONTHS}
    print(f"| best 3 minus worst 3, 6m | {cell(ls)} | {cell(ls, HALF_A)} | {cell(ls, HALF_B)} | - | - |")


def capm(s):
    xs, ys = [s[m] for m in MONTHS], [B.RET[m]["SPY"] for m in MONTHS]
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((y - my) ** 2 for y in ys)
    resid = [x - b * y for x, y in zip(xs, ys)]
    a = statistics.fmean(resid)
    sd = statistics.pstdev([r - a for r in resid])
    return b, a * 12, (a / sd * math.sqrt(len(xs)) if sd else 0.0)


def rep_books():
    reps = [(sig, 1 if full > 0 else -1) for sig, _, full, _, ok in REP if ok]
    books = {"EQUAL (all 24)": equal(ALL)}
    for sig, g in reps:
        books[f"{sig}: long best 3, 6m"] = score_book(signed(sig, g), ALL, 6)[0]
        b, w = score_book(signed(sig, g), ALL, 6)[0], score_book(signed(sig, g), ALL, 6, worst=True)[0]
        books[f"{sig}: best 3 minus worst 3"] = {m: b[m] - w[m] for m in MONTHS}
    return books


def section_capm():
    """Added after the first run: how much of each book is market exposure (beta), and what is left (alpha)?"""
    print("\n### Market exposure and what is left: beta to SPY, and the yearly return beyond beta x SPY (added after the first run)\n")
    print("| Book | Beta to SPY | Return beyond beta x SPY, per year | t-stat of that |\n|---|---|---|---|")
    for k, s in rep_books().items():
        b, a, t = capm(s)
        print(f"| {k} | {b:+.2f} | {a * 100:+.1f}% | {t:+.2f} |")


def section_years():
    """Added after the first run: calendar years, with 2022 (a year value stocks won) in view."""
    books = rep_books()
    keys = ["EQUAL (all 24)"] + [k for k in books if k != "EQUAL (all 24)"]
    yrs = sorted({m[:4] for m in MONTHS})
    print("\n### Calendar years (added after the first run)\n")
    print("| Year | SPY | " + " | ".join(keys) + " |\n|---|---|" + "---|" * len(keys))
    for y in yrs:
        spy = math.prod(1 + B.RET[m]["SPY"] for m in MONTHS if m[:4] == y) - 1
        print(f"| {y} | {spy * 100:+.1f}% | " + " | ".join(f"{(math.prod(1 + books[k][m] for m in MONTHS if m[:4] == y) - 1) * 100:+.1f}%" for k in keys) + " |")


def section_posthoc():
    """POST-HOC (chosen after reading the cross-sectional and within-ticker results): the cross-sectional style picks the
    pool, the within-ticker dip times the entry."""
    reps = [(sig, 1 if full > 0 else -1) for sig, _, full, _, ok in REP if ok]

    def comp(mo, t):
        tot, n = 0.0, 0
        for sig, g in reps:
            vals = sorted(v for x in FIRST[mo] if (v := signed(sig, g)(mo, x)) is not None)
            v = signed(sig, g)(mo, t)
            if v is None or not vals:
                continue
            tot += bisect.bisect_left(vals, v) / max(1, len(vals) - 1)
            n += 1
        return tot / n if n else None

    def pool_then(key, n_pool=8):
        def score(mo, t):
            pool = sorted((x for x in FIRST[mo] if comp(mo, x) is not None), key=lambda x: -comp(mo, x))[:n_pool]
            if t not in pool or ROWS[(mo, t)].get(key) is None:
                return None
            return -ROWS[(mo, t)][key]                          # lower 1-month change / deeper below the high ranks first
        return score
    print("\n### POST-HOC: the composite's top 8, then the 3 that just fell (a lead for a fresh test, not a finding)\n")
    print("| Book | ALL 24: full period | 2008-2016 | 2017-2026 | Beta | Return beyond beta x SPY |\n|---|---|---|---|---|---|")
    for lab, sc, hold in (("composite top 3, 6m (from above)", comp, 6), ("top 8, then the 3 with the weakest last month, 1m", pool_then("chg_1m"), 1),
                          ("top 8, then the 3 deepest below the 52-week high, 6m", pool_then("dd_52w"), 6)):
        s = score_book(sc, ALL, hold)[0]
        b, a, _ = capm(s)
        print(f"| {lab} | {cell(s)} | {cell(s, HALF_A)} | {cell(s, HALF_B)} | {b:+.2f} | {a * 100:+.1f}% |")


def section_now():
    reps = [(sig, 1 if full > 0 else -1) for sig, _, full, _, ok in REP if ok]
    mo = MONTHS[-1]
    print(f"\n### The newest month ({mo}): the replicating signals' best and worst three of ALL twenty-four\n")
    for sig, g in reps:
        pts = sorted(((signed(sig, g)(mo, t), t) for t in FIRST[mo] if signed(sig, g)(mo, t) is not None), reverse=True)
        print(f"- {sig}: best {', '.join(t for _, t in pts[:3])}; worst {', '.join(t for _, t in pts[-3:])}")


SECTIONS = {"ic": section_ic, "within": section_within, "portfolios": section_portfolios, "composite": section_composite, "now": section_now,
            "capm": section_capm, "years": section_years, "posthoc": section_posthoc}

if __name__ == "__main__":
    print(f"HINDSIGHT. {len(ALL)} tickers, {len(ROWS)} ticker-months, {MONTHS[0]} to {MONTHS[-1]}.")
    for name in sys.argv[1:] or SECTIONS:
        SECTIONS[name]()
