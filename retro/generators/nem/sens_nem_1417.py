#!/usr/bin/env python3
"""How far each NEM 2014-2017 judgement call moves the classes: rebuild the 209 dates with one encoding changed (in memory, into a
scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/nem/sens_nem_1417.py <scratch-out>
"""
import contextlib, copy, io, json, os, re, runpy, shutil, sys, types
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
dates = weekly_dates("2014-01-01", "2017-12-31", sorted(raw), facts0["prints"])
assert len(dates) == 209
tax = T.load_taxonomy()


def variant_module(old, new):
    """A copy of build_nem with one line of its source replaced (the module on disk is untouched)."""
    src = open(B.__file__, encoding="utf-8").read()
    assert src.count(old) == 1, old
    m = types.ModuleType("build_nem_variant")
    m.__file__ = B.__file__
    exec(compile(src.replace(old, new), B.__file__, "exec"), m.__dict__)
    return m


def classify_all(facts, engine, tag, mod=B, engine2=None):
    out = os.path.join(OUT, tag)
    shutil.rmtree(out, ignore_errors=True)
    res = {}
    for d in dates:
        with contextlib.redirect_stdout(io.StringIO()):
            mod.build(d, facts, raw, spx, engine, out, engine2 or engine20)
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
json.dump(base, open(os.path.join(OUT, "main_nem_1417.json"), "w"), indent=0)
V = {}
# 1. FY2015 kept at GAAP $0.38 (the AAPL FY2002 test read on the one-off items alone, leaving out the recurring impairments, asset sales
#    and tax adjustments: $92M against $193M) in the FY2015 vintage; the FY2016 vintage's $0.00 still has no P/E
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    if v["fy_label"] == "FY15":
        v["eps_normalized"]["2015"] = 0.38
        del v["eps_excluded"]["2015"]
V["FY2015 kept at GAAP $0.38"] = (f, engine0, B, None)
# 2. the company's adjusted net income per diluted share for 2013-2016, from the vintage after each Q4 release that first prints it
#    (FY13 $1.40, then $1.25 from the FY2014 10-K; FY14 $1.09; FY15 $0.98, then $0.63 without Batu Hijau from the FY2016 10-K; FY16 $1.16)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    if v["published"] >= "2014-01-01":
        adj = {"2013": 1.40 if v["fy_label"] == "FY13" else 1.25, "2014": 1.09, "2015": 0.63 if v["fy_label"] == "FY16" else 0.98,
               "2016": 1.16}
        for y, a in adj.items():
            if y in v["eps_normalized"] or y in v["eps_excluded"]:
                v["eps_normalized"][y] = a
                v["eps_excluded"].pop(y, None)
V["the adjusted net income per share 2013-2016"] = (f, engine0, B, None)
# 3. the FY2016 10-K's restated 2012-2015 unused (FY14 $1.10 and FY12 $3.76 kept: the earlier basis with Batu Hijau)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    if v["fy_label"] == "FY16":
        v["eps_normalized"].update({"2012": 3.76, "2014": 1.10})
V["FY14 $1.10 and FY12 $3.76 kept in the FY2016 vintage"] = (f, engine0, B, None)
# 4. the 8-K of 2014-06-13 not a vintage of its own (FY12 $3.78 to the FY2014 10-K)
f = copy.deepcopy(facts0)
f["history_vintages"] = [v for v in f["history_vintages"] if v["published"] != "2014-06-13"]
V["the 8-K of 2014-06-13 not a vintage"] = (f, engine0, B, None)
# 4. BASE on the latest quarter's gold ounces growth instead of revenue growth (the XOM production test)
mod = variant_module('    fwd = [latest["sales_pct"]] * 2\n', '    fwd = [latest["oz_pct"]] * 2\n')
V["BASE on the latest quarter's gold ounces growth"] = (facts0, engine0, mod, None)
# 5. the vintage's dividend instead of the declared rates
mod = variant_module('    if not divs:                                   # no declared rate', '    divs = []\n    if not divs:                                   # no declared rate')
V["the vintage's dividend instead of the declared rates"] = (facts0, engine0, mod, None)
# 6. a five-year P/E window instead of ten (the call the classes rest on: the 2002-2006 regime of 26-100x GAAP multiples)
mod = variant_module("d > minus_years(as_of, 10) and", "d > minus_years(as_of, 5) and")
V["a five-year P/E window"] = (facts0, engine0, mod, None)
# 6./7. every data signal at its BEAR or XBULL value (both engines)
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
    V[f"every data signal at its {lab} value"] = (facts0, sig(engine0, vals), B, sig(engine20, vals))
for name, (f, e, m, e2) in V.items():
    r = classify_all(f, e, "v", m, e2)
    c, t, mv, span = diff(base, r)
    print(f"{name}: {c} classes, {t} tiers {mv} {span or ''}")
