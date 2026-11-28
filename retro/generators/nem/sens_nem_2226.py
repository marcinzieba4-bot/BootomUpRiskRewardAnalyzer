#!/usr/bin/env python3
"""How far each NEM 2022-2026 judgement call moves the classes: rebuild the 256 dates with one encoding changed (in memory, into a
scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/nem/sens_nem_2226.py <scratch-out>
"""
import contextlib, copy, io, json, os, runpy, shutil, sys, types
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = sys.argv[1]
sys.path.insert(0, os.path.join(REPO, "retro"))
import build_nem as B  # noqa: E402
import retro_tool as T  # noqa: E402
from build_acn import load_series, weekly_dates  # noqa: E402
facts0 = json.load(open(B.FACTS, encoding="utf-8"))
engine0 = open(B.ENGINE, encoding="utf-8").read()
engine20 = open(B.ENGINE2, encoding="utf-8").read()
raw, spx = load_series("NEM"), load_series("^GSPC")
dates = weekly_dates("2022-01-01", "2026-11-27", sorted(raw), facts0["prints"])
assert len(dates) == 256
tax = T.load_taxonomy()
os.makedirs(OUT, exist_ok=True)


def variant_module(old, new):
    """A copy of build_nem with one line of its source replaced (the module on disk is untouched)."""
    src = open(B.__file__, encoding="utf-8").read()
    assert src.count(old) == 1, old
    m = types.ModuleType("build_nem_variant")
    m.__file__ = B.__file__
    exec(compile(src.replace(old, new), B.__file__, "exec"), m.__dict__)
    return m


def classify_all(facts, engine, tag, mod=B):
    out = os.path.join(OUT, tag)
    shutil.rmtree(out, ignore_errors=True)
    res = {}
    for d in dates:
        with contextlib.redirect_stdout(io.StringIO()):
            mod.build(d, facts, raw, spx, engine, out, engine20)
        mp = os.path.join(out, d, "model.py")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            g = runpy.run_path(mp, run_name="__retro__")
        q = T.retro_classify(dict(g["RESULT"], report=buf.getvalue()), g["PIT_PROFILE"], tax)
        res[d] = (q["price_state"], g["RESULT"]["signal_short"])
    return res


def diff(a, b):
    mv = {}
    for d in dates:
        if a[d][0] != b[d][0]:
            k = f"{a[d][0]}->{b[d][0]}"
            mv[k] = mv.get(k, 0) + 1
    ch = [d for d in dates if a[d][0] != b[d][0]]
    return len(ch), sum(a[d][1] != b[d][1] for d in dates), mv, (ch[0], ch[-1]) if ch else None


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
json.dump(base, open(os.path.join(OUT, "main_nem_2226.json"), "w"), indent=0)
V = {}


def adjusted(years, fy23=1.57):
    """The company's adjusted net income per diluted share for the given years, in every vintage from FY2020's (and the Q4 2023
    print's full-year actuals) that holds them: FY20 $2.66, FY21 $2.96, FY22 $1.85, FY23 $1.57 (the FY2023 10-K; the release's $1.61),
    FY24 $3.48, FY25 $6.89, each from the highlights table or the Q4 release that prints it."""
    adj = {"2020": 2.66, "2021": 2.96, "2022": 1.85, "2023": fy23, "2024": 3.48, "2025": 6.89}
    f = copy.deepcopy(facts0)
    for v in f["history_vintages"]:
        if v["published"] >= "2021-01-01":
            for y in years:
                if y in v["eps_normalized"] or y in v["eps_excluded"]:
                    v["eps_normalized"][y] = adj[y]
                    v["eps_excluded"].pop(y, None)
            v["eps_normalized"] = dict(sorted(v["eps_normalized"].items()))
    for p in f["prints"]:
        if p.get("fy_actual") and str(p["fy_actual"]["fy"]) in years:
            p["fy_actual"]["eps"] = 1.61
    return f


def kept21():
    """FY2021 kept at GAAP $1.39 (the AAPL FY2002 test not applied) in every vintage that holds it."""
    f = copy.deepcopy(facts0)
    for v in f["history_vintages"]:
        if "2021" in v["eps_excluded"]:
            del v["eps_excluded"]["2021"]
            v["eps_normalized"] = dict(sorted({**v["eps_normalized"], "2021": 1.39}.items()))
    return f


V["FY2021 kept at GAAP $1.39"] = (kept21(), engine0, B)
V["the adjusted net income per share 2020-2025"] = (adjusted(("2020", "2021", "2022", "2023", "2024", "2025")), engine0, B)
V["the adjusted net income per share 2021-2023 only (the excluded years)"] = (adjusted(("2021", "2022", "2023")), engine0, B)
# the by-product costs applicable to sales per ounce from the Q4 2025 release (the reconciliation's figure) instead of the summary table's
# co-product line
f = copy.deepcopy(facts0)
for p in f["prints"]:
    if "cas_byproduct" in p["rows"]:
        v = [float(x.replace(",", "")) for x in p["rows"]["cas_byproduct"].split(" | ")[1:]]
        p["raw"]["cas"], p["raw"]["cas_prior"] = v[0], v[1]
        p["cas_pct"] = round((v[0] / v[1] - 1) * 100 + 0.0, 1)
V["the by-product CAS per ounce from Q4 2025"] = (f, engine0, B)
mod = variant_module('    fwd = [latest["sales_pct"]] * 2\n', '    fwd = [latest["oz_pct"]] * 2\n')
V["BASE on the latest quarter's gold ounces growth"] = (facts0, engine0, mod)
mod = variant_module('    fwd = [latest["sales_pct"]] * 2\n',
                     '    fwd = [0.0 if latest["quarter"] in ("Q4 2023", "Q1 2024", "Q2 2024", "Q3 2024") else latest["sales_pct"]] * 2\n')
V["BASE at 0% on the Newcrest quarters"] = (facts0, engine0, mod)
mod = variant_module('    if not divs:                                   # no declared rate', '    divs = []\n    if not divs:                                   # no declared rate')
V["the vintage's dividend instead of the declared rates"] = (facts0, engine0, mod)
mod = variant_module("d > minus_years(as_of, 10) and", "d > minus_years(as_of, 5) and")
V["a five-year P/E window"] = (facts0, engine0, mod)


def sig(e, vals):
    i0, i1 = e.index("SIGNALS = ["), e.index("THEME_SIGNAL_NAME, \"/4\"")
    blk = e[i0:i1]
    for key, val in zip(('float(LATEST["oz_pct"])', 'float(LATEST["cas_pct"])', 'float(LATEST["sales_pct"])', 'float(LATEST["eps_pct"])'), vals):
        assert key in blk
        blk = blk.replace(key, val)
    k = 'round((FY_MARGIN_BASE - PREV_FY_MARGIN) * 100, 1) if MARGIN_GUIDED else float(LATEST["margin_bp"])'
    assert k in blk
    return e[:i0] + blk.replace(k, vals[4]) + e[i1:]


for lab, vals in (("BEAR", ("-27.0", "52.0", "-33.0", "-106.0", "-8210.0")), ("XBULL", ("40.0", "-14.0", "55.0", "297.0", "3780.0"))):
    V[f"every data signal at its {lab} value"] = (facts0, sig(engine0, vals), B)
for name, (f, e, m) in V.items():
    r = classify_all(f, e, "v", m)
    c, t, mv, span = diff(base, r)
    print(f"{name}: {c} classes, {t} tiers {mv} {span or ''}")
