#!/usr/bin/env python3
"""How far each NEM 2010-2013 judgement call moves the classes: rebuild the 209 dates with one encoding changed (in memory, into a
scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/nem/sens_nem_1013.py <scratch-out>
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
dates = weekly_dates("2010-01-01", "2013-12-31", sorted(raw), facts0["prints"])
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
json.dump(base, open(os.path.join(OUT, "main_nem_1013.json"), "w"), indent=0)
V = {}
# 1. FY2011 at the company's adjusted net income per share: $4.39 basic in the FY2011 vintage (the Q4 2011 release), $4.31 diluted in
#    the FY2012 vintage (the Q4 2012 release)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    if "2011" in v.get("eps_excluded", {}):
        v["eps_normalized"]["2011"] = 4.39 if v["fy_label"] == "FY11" else 4.31
        del v["eps_excluded"]["2011"]
V["FY2011 at the company's adjusted $4.39 / $4.31"] = (f, engine0, B, None)
# 2. FY2011 derived without its listed items: ($502M + $1,668M) / 504M = $4.31 (no filing publishes it)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    if "2011" in v.get("eps_excluded", {}):
        v["eps_normalized"]["2011"] = round((502 + 1668) / 504, 2)
        del v["eps_excluded"]["2011"]
V["FY2011 derived without its listed items ($4.31)"] = (f, engine0, B, None)
# 3. the adjusted net income per share every year, from the vintage after each Q4 release that first prints it (FY07 $1.33, FY08
#    $1.99, FY09 $2.79, FY10 $3.85, FY11 $4.39 then $4.31 diluted, FY12 $3.71 diluted)
f = copy.deepcopy(facts0)
ADJ = {"2007": 1.33, "2008": 1.99, "2009": 2.79, "2010": 3.85, "2011": 4.39, "2012": 3.71}
for v in f["history_vintages"]:
    if v["published"] >= "2010-01-01":
        for y, a in ADJ.items():
            if y in v["eps_normalized"] or y in v["eps_excluded"]:
                v["eps_normalized"][y] = 4.31 if (y == "2011" and v["fy_label"] == "FY12") else a
        v["eps_excluded"] = {}
V["the adjusted net income per share every year 2007-2012"] = (f, engine0, B, None)
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
