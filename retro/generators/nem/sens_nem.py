#!/usr/bin/env python3
"""How far each NEM 2008-2009 judgement call moves the classes: rebuild the 105 dates with one encoding changed (in memory, into a
scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/nem/sens_nem.py <scratch-out>
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
raw, spx = load_series("NEM"), load_series("^GSPC")
dates = weekly_dates("2008-01-01", "2009-12-31", sorted(raw), facts0["prints"])
assert len(dates) == 105
tax = T.load_taxonomy()


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
            mod.build(d, facts, raw, spx, engine, out)
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
json.dump(base, open(os.path.join(OUT, "main_nem.json"), "w"), indent=0)
V = {}
# 1. the company's adjusted net income per share for FY2007 ($1.33) and FY2008 ($1.99), first published in the Q4 2008 release
#    (2009-02-19), in the vintages from it: FY2007 back in the history, FY2008 on the adjusted basis
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    if v["published"] >= "2009-02-19":
        v["eps_normalized"].update({"2007": 1.33, "2008": 1.99})
        v["eps_excluded"] = {}
V["FY2007 and FY2008 at the company's adjusted $1.33 and $1.99 (from the Q4 2008 release)"] = (f, engine0, B)
# 2. FY2007 without the listed continuing charges, derived: ($(963)M + $1,544M) / 452M = $1.29 (no filing publishes it)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    if "2007" in v.get("eps_excluded", {}):
        v["eps_normalized"]["2007"] = round((-963 + 1544) / 452, 2)
        v["eps_excluded"] = {}
V["FY2007 derived without its listed charges ($1.29)"] = (f, engine0, B)
# 3. BASE on the latest quarter's gold ounces sold growth instead of revenue growth (the XOM production test)
mod = variant_module('    fwd = [latest["sales_pct"]] * 2\n', '    fwd = [latest["oz_pct"]] * 2\n')
V["BASE on the latest quarter's gold ounces sold growth"] = (facts0, engine0, mod)
# 4./5. every data signal at its BEAR or XBULL value
for lab, vals in (("BEAR", ("-27.0", "52.0", "-33.0", "-106.0", "-8210.0")), ("XBULL", ("40.0", "-14.0", "55.0", "297.0", "3780.0"))):
    e = engine0
    i0, i1 = e.index("SIGNALS = ["), e.index("THEME_SIGNAL_NAME, \"/4\"")
    blk = e[i0:i1]
    for key, val in zip(('float(LATEST["oz_pct"])', 'float(LATEST["cas_pct"])', 'float(LATEST["sales_pct"])', 'float(LATEST["eps_pct"])'), vals):
        assert key in blk
        blk = blk.replace(key, val)
    k = 'round((FY_MARGIN_BASE - PREV_FY_MARGIN) * 100, 1) if MARGIN_GUIDED else float(LATEST["margin_bp"])'
    assert k in blk
    blk = blk.replace(k, vals[4])
    V[f"every data signal at its {lab} value"] = (facts0, e[:i0] + blk + e[i1:], B)
for name, (f, e, m) in V.items():
    r = classify_all(f, e, "v", m)
    c, t, mv, span = diff(base, r)
    print(f"{name}: {c} classes, {t} tiers {mv} {span or ''}")
