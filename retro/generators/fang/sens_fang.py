#!/usr/bin/env python3
"""How far each FANG 2014-2017 judgement call moves the classes: rebuild the 202 built dates (2014-02-21 to 2017-12-29) with one encoding
changed (in memory, into a scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/fang/sens_fang.py <scratch-out>
"""
import contextlib, copy, io, json, os, runpy, shutil, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = sys.argv[1]
sys.path.insert(0, os.path.join(REPO, "retro"))
import build_fang as B  # noqa: E402
import retro_tool as T  # noqa: E402
from build_acn import load_series, weekly_dates  # noqa: E402
facts0 = json.load(open(B.FACTS, encoding="utf-8"))
engine0 = open(B.ENGINE, encoding="utf-8").read()
raw, spx = load_series("FANG"), load_series("^GSPC")
dates = [d for d in weekly_dates("2014-01-01", "2017-12-31", sorted(spx), facts0["prints"]) if d >= "2014-02-21"]
assert len(dates) == 202
tax = T.load_taxonomy()


def classify_all(facts, engine, tag):
    out = os.path.join(OUT, tag)
    shutil.rmtree(out, ignore_errors=True)
    res = {}
    for d in dates:
        with contextlib.redirect_stdout(io.StringIO()):
            B.build(d, facts, raw, spx, engine, out)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            g = runpy.run_path(os.path.join(out, d, "model.py"), run_name="__retro__")
        q = T.retro_classify(dict(g["RESULT"], report=buf.getvalue()), g["PIT_PROFILE"], tax)
        res[d] = (q["price_state"], g["RESULT"]["signal_short"])
    shutil.rmtree(out, ignore_errors=True)
    return res


def diff(a, b):
    mv = {}
    ch = [d for d in dates if a[d][0] != b[d][0]]
    for d in ch:
        k = f"{a[d][0]}->{b[d][0]}"
        mv[k] = mv.get(k, 0) + 1
    return len(ch), sum(a[d][1] != b[d][1] for d in dates), mv, (ch[0], ch[-1]) if ch else None


def signals_at(engine, col):
    """Every scored signal at one of its thresholds (BEAR or XBULL), from the engine's own SIGNALS table."""
    vals = {"production_pct": (14.0, 148.0), "oil_pct": (52.0, 167.0), "sales_pct": (-142.0, 177.0), "loe_boe_pct": (130.0, -44.0),
            "pretax_margin_bp": (-8730.0, 49380.0)}
    e = engine
    for k, (bear, xbull) in vals.items():
        old = f'_f(LATEST["{k}"])'
        assert e.count(old) == 1, k
        e = e.replace(old, repr(bear if col == 2 else xbull))
    return e


def set_eps(facts, year, eps):
    """A year's EPS at another figure in every vintage and Q4 print that holds it, kept in the history."""
    f = copy.deepcopy(facts)
    for v in f["history_vintages"]:
        if "eps_normalized" in v and (year in v["eps_normalized"] or year in v["eps_excluded"]):
            v["eps_normalized"][year] = eps
            v["eps_excluded"].pop(year, None)
    for p in f["prints"]:
        a = p.get("fy_actual")
        if a and str(a["fy"]) == year:
            a["eps_gaap"] = eps
            a["one_off_test"].update(eps_gaap=eps, loss=eps <= 0, distorted=False, kept=True)   # the figure without the one-offs
    return f


base = classify_all(facts0, engine0, "main")
cnt, tiers = {}, {}
for d in dates:
    cnt[base[d][0]] = cnt.get(base[d][0], 0) + 1
    tiers[base[d][1]] = tiers.get(base[d][1], 0) + 1
print("main:", cnt, tiers)
by_year = {}
for d in dates:
    by_year.setdefault(d[:4], {}).setdefault(base[d][0], 0)
    by_year[d[:4]][base[d][0]] += 1
print("by year:", by_year)
json.dump(base, open(os.path.join(OUT, "main_fang.json"), "w"), indent=0)
V = {}
V["every signal at its BEAR value"] = (facts0, signals_at(engine0, 2))
V["every signal at its XBULL value"] = (facts0, signals_at(engine0, 5))
old = "BUYBACK           = _cagr(SHARES_HIST[_SY[-1]], SHARES_HIST[_SY[0]], _SY[-1] - _SY[0]) if len(_SY) > 1 else 0.0"
assert engine0.count(old) == 1
V["no net share issuance in BASE"] = (facts0, engine0.replace(old, "BUYBACK = 0.0"))
# the company's adjusted EPS, which also removes the non-cash derivative marks (recurring): FY13 $1.21, FY14 $2.24 (the releases)
V["FY2013 $1.21 and FY2014 $2.24 (adjusted, hedge marks out)"] = (set_eps(set_eps(facts0, "2013", 1.21), "2014", 2.24), engine0)
# the loss years at the company's adjusted EPS (FY15 $1.81, Q4 2015 release; FY16 $1.87, Q4 2016 release)
V["FY2015 $1.81 and FY2016 $1.87 (adjusted) kept"] = (set_eps(set_eps(facts0, "2015", 1.81), "2016", 1.87), engine0)
# the revenue history without the Predecessors' years (2008-2011): from 2012, the year of the IPO, on
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    if "revenue_usd_b" in v:
        v["revenue_usd_b"] = {k: x for k, x in v["revenue_usd_b"].items() if k >= "2012"}
V["revenue history from 2012 (Predecessors' years out)"] = (f, engine0)
for name, (f, e) in V.items():
    n, nt, mv, span = diff(base, classify_all(f, e, "v"))
    print(f"{name}: {n} classes {mv}{f' ({span[0]} .. {span[1]})' if span else ''}, {nt} tiers", flush=True)
