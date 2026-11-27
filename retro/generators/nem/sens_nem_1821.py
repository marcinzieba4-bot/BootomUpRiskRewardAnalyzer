#!/usr/bin/env python3
"""How far each NEM 2018-2021 judgement call moves the classes: rebuild the 209 dates with one encoding changed (in memory, into a
scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/nem/sens_nem_1821.py <scratch-out>
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
engine30 = open(B.ENGINE3, encoding="utf-8").read()
raw, spx = load_series("NEM"), load_series("^GSPC")
dates = weekly_dates("2018-01-01", "2021-12-31", sorted(raw), facts0["prints"])
assert len(dates) == 209
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


def classify_all(facts, engine, tag, mod=B, engine3=None):
    out = os.path.join(OUT, tag)
    shutil.rmtree(out, ignore_errors=True)
    keep = mod.ENGINE3
    if engine3 is not None:                       # the nem3 copy is read from disk by build(): a scratch copy for the variant
        mod.ENGINE3 = os.path.join(OUT, "nem3_variant.py.tmpl")
        open(mod.ENGINE3, "w", encoding="utf-8").write(engine3)
    res = {}
    try:
        for d in dates:
            with contextlib.redirect_stdout(io.StringIO()):
                mod.build(d, facts, raw, spx, engine, out, engine20)
            mp = os.path.join(out, d, "model.py")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                g = runpy.run_path(mp, run_name="__retro__")
            q = T.retro_classify(dict(g["RESULT"], report=buf.getvalue()), g["PIT_PROFILE"], tax)
            res[d] = (q["price_state"], g["RESULT"]["signal_short"])
    finally:
        mod.ENGINE3 = keep
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
json.dump(base, open(os.path.join(OUT, "main_nem_1821.json"), "w"), indent=0)
V = {}
NEW = [v for v in facts0["history_vintages"] if v["published"] >= "2018-01-01"]


def kept(years):
    """Years kept at their GAAP EPS in every 2018-2021 vintage that reports them (excluded by the frozen tests in the main build)."""
    f = copy.deepcopy(facts0)
    gaap = {"FY18": {"2018": 0.53}, "FY19": {"2018": 0.53, "2019": 3.91}, "FY20": {"2018": 0.53, "2019": 3.91}}
    for v in f["history_vintages"]:
        if v["published"] >= "2018-01-01":
            for y, e in gaap.get(v["fy_label"], {}).items():
                if y in years:
                    v["eps_normalized"][y] = e
                    del v["eps_excluded"][y]
    return f


# 1.-3. FY2018 kept at GAAP $0.53 (the AAPL FY2002 test read on the one-off items alone); FY2019 kept at GAAP $3.91 (the mirror not
#       applied to the Nevada Gold Mines gain); both
V["FY2018 kept at GAAP $0.53"] = (kept({"2018"}), engine0, B, None)
V["FY2019 kept at GAAP $3.91"] = (kept({"2019"}), engine0, B, None)
V["FY2018 and FY2019 kept at GAAP"] = (kept({"2018", "2019"}), engine0, B, None)
# 4. the company's adjusted net income per diluted share for 2017-2020 (FY17 $1.46 in the Q4 2017 release, $1.45 in the FY2018-FY2019
#    10-Ks' highlights tables; FY18 $1.34; FY19 $1.32; FY20 $2.66), from the vintage after each Q4 release that first prints it
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    if v["published"] >= "2018-01-01":
        adj = {"2017": 1.46 if v["published"] < "2019-01-01" else 1.45, "2018": 1.34, "2019": 1.32, "2020": 2.66}
        for y, a in adj.items():
            if y in v["eps_normalized"] or y in v["eps_excluded"]:
                v["eps_normalized"][y] = a
                v["eps_excluded"].pop(y, None)
V["the adjusted net income per share 2017-2020"] = (f, engine0, B, None)
# 5. the 8-K of 2018-04-26 not a vintage of its own (FY14 $1.30 to the FY2018 10-K)
f = copy.deepcopy(facts0)
f["history_vintages"] = [v for v in f["history_vintages"] if v["published"] != "2018-04-26"]
V["the 8-K of 2018-04-26 not a vintage"] = (f, engine0, B, None)
# 6. BASE on the latest quarter's gold ounces growth instead of revenue growth (the XOM production test)
mod = variant_module('    fwd = [latest["sales_pct"]] * 2\n', '    fwd = [latest["oz_pct"]] * 2\n')
V["BASE on the latest quarter's gold ounces growth"] = (facts0, engine0, mod, None)
# 7. BASE at 0% on the four prints whose year-ago quarter is before the Goldcorp acquisition (Q2 2019 to Q1 2020)
mod = variant_module('    fwd = [latest["sales_pct"]] * 2\n',
                     '    fwd = [0.0 if latest["quarter"] in ("Q2 2019", "Q3 2019", "Q4 2019", "Q1 2020") else latest["sales_pct"]] * 2\n')
V["BASE at 0% on the Goldcorp quarters"] = (facts0, engine0, mod, None)
# 8. the vintage's dividend instead of the declared rates
mod = variant_module('    if not divs:                                   # no declared rate', '    divs = []\n    if not divs:                                   # no declared rate')
V["the vintage's dividend instead of the declared rates"] = (facts0, engine0, mod, None)
# 9. a five-year P/E window instead of ten
mod = variant_module("d > minus_years(as_of, 10) and", "d > minus_years(as_of, 5) and")
V["a five-year P/E window"] = (facts0, engine0, mod, None)


# 10./11. every data signal at its BEAR or XBULL value (all three engines)
def sig(e, vals):
    i0, i1 = e.index("SIGNALS = ["), e.index("THEME_SIGNAL_NAME, \"/4\"")
    blk = e[i0:i1]
    eps_key = '_f(LATEST["eps_pct"])' if '_f(LATEST["eps_pct"])' in blk else 'float(LATEST["eps_pct"])'
    for key, val in zip(('float(LATEST["oz_pct"])', 'float(LATEST["cas_pct"])', 'float(LATEST["sales_pct"])', eps_key), vals):
        assert key in blk
        blk = blk.replace(key, val)
    k = 'round((FY_MARGIN_BASE - PREV_FY_MARGIN) * 100, 1) if MARGIN_GUIDED else float(LATEST["margin_bp"])'
    assert k in blk
    return e[:i0] + blk.replace(k, vals[4]) + e[i1:]


for lab, vals in (("BEAR", ("-27.0", "52.0", "-33.0", "-106.0", "-8210.0")), ("XBULL", ("40.0", "-14.0", "55.0", "297.0", "3780.0"))):
    V[f"every data signal at its {lab} value"] = (facts0, sig(engine0, vals), B, sig(engine30, vals))
for name, (f, e, m, e3) in V.items():
    r = classify_all(f, e, "v", m, e3)
    c, t, mv, span = diff(base, r)
    print(f"{name}: {c} classes, {t} tiers {mv} {span or ''}")
