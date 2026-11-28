#!/usr/bin/env python3
"""How far each FANG 2018-2021 judgement call moves the classes: rebuild the 209 built dates (2018-01-05 to 2021-12-31) with one encoding
changed (in memory, into a scratch folder) and classify offline with retro_tool's own classifier. No outcome is read. (The 2014-2017
batch's calls are sens_fang.py.)

    python3 retro/generators/fang/sens_fang_1821.py <scratch-out>
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
dates = weekly_dates("2018-01-01", "2021-12-31", sorted(spx), facts0["prints"])
assert len(dates) == 209
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
            o = a["one_off_test"]                         # the figure without the one-offs: their pre-tax amounts added back
            o.update(eps_gaap=eps, loss=eps <= 0, distorted=False, kept=True,
                     pretax_m=o["pretax_m"] + o["listed_charges_m"] - o["listed_benefits_m"], listed_charges_m=0.0, listed_benefits_m=0.0)
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
json.dump(base, open(os.path.join(OUT, "main_fang_1821.json"), "w"), indent=0)
V = {}
V["every signal at its BEAR value"] = (facts0, signals_at(engine0, 2))
V["every signal at its XBULL value"] = (facts0, signals_at(engine0, 5))
old = "BUYBACK           = _cagr(SHARES_HIST[_SY[-1]], SHARES_HIST[_SY[0]], _SY[-1] - _SY[0]) if len(_SY) > 1 else 0.0"
assert engine0.count(old) == 1
V["no net share change in BASE"] = (facts0, engine0.replace(old, "BUYBACK = 0.0"))
# FY2019 kept at GAAP $1.47 (the distorted-year exclusion undone), and at the company's adjusted $6.93 (Q4 2019 release; marks out too)
V["FY2019 kept at GAAP $1.47"] = (set_eps(facts0, "2019", 1.47), engine0)
V["FY2019 at the adjusted $6.93"] = (set_eps(facts0, "2019", 6.93), engine0)
# FY2018 at the company's adjusted $5.87 (Q4 2018 release: removes the derivative gain, other income and merger costs)
V["FY2018 at the adjusted $5.87"] = (set_eps(facts0, "2018", 5.87), engine0)
# the EPS history as each 10-K's own five Item 6 years only (no carried years: FY13 leaves with the FY2018 10-K, FY14 with the FY2019)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    if "eps_normalized" in v and v["published"] >= "2018-01-01":
        fy = int(v["fy_label"][2:]) + 2000
        gone = {k: "outside the 10-K's five years (sensitivity)" for k in v["eps_normalized"] if int(k) <= fy - 5}
        v["eps_normalized"] = {k: x for k, x in v["eps_normalized"].items() if int(k) > fy - 5}
        v["eps_excluded"] = {**v["eps_excluded"], **gone}   # their days leave the P/E window, as an excluded year's do
V["EPS history: the 10-K's own five years only"] = (f, engine0)
# no dividend (the rate at 0)
f = copy.deepcopy(facts0)
for d in f["dividends"]:
    d["annual"] = 0.0
V["dividend at 0"] = (f, engine0)
for name, (f, e) in V.items():
    n, nt, mv, span = diff(base, classify_all(f, e, "v"))
    print(f"{name}: {n} classes {mv}{f' ({span[0]} .. {span[1]})' if span else ''}, {nt} tiers", flush=True)
