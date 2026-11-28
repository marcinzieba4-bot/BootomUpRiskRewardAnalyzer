#!/usr/bin/env python3
"""How far each OKE 2014-2017 judgement call moves the classes: rebuild the 209 dates with one encoding changed (in memory, into a
scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/oke/sens_oke_1417.py <scratch-out>
"""
import contextlib, copy, io, json, os, runpy, shutil, sys, types
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = sys.argv[1]
sys.path.insert(0, os.path.join(REPO, "retro"))
import build_oke as B  # noqa: E402
import retro_tool as T  # noqa: E402
from build_acn import load_series, weekly_dates  # noqa: E402
facts0 = json.load(open(B.FACTS, encoding="utf-8"))
engine0 = open(B.ENGINE, encoding="utf-8").read()
raw, spx = load_series("OKE"), load_series("^GSPC")
dates = weekly_dates("2014-01-01", "2017-12-31", sorted(raw), facts0["prints"])
assert len(dates) == 209
tax = T.load_taxonomy()


def variant_module(old, new):
    """A copy of build_oke with one line of its source replaced (the module on disk is untouched)."""
    src = open(B.__file__, encoding="utf-8").read()
    assert src.count(old) == 1, old
    m = types.ModuleType("build_oke_variant")
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
json.dump(base, open(os.path.join(OUT, "main_oke_1417.json"), "w"), indent=0)
V = {}
# 1. the window's days before the ONE Gas separation priced without ONE Gas (Yahoo's factor kept, as if a split) instead of as traded
mod = variant_module('    for x in [x for x in dists if x["effective"] <= as_of]:\n', '    for x in []:\n')
V["days before 2014-02-03 at Yahoo's adjusted price (without ONE Gas)"] = (facts0, engine0, mod)
# 2. the restated 2010-2013 (without ONE Gas and energy services) not used: the FY2013 10-K's figures kept in the later vintages
f = copy.deepcopy(facts0)
v13 = next(v for v in f["history_vintages"] if v["fy_label"] == "FY13")
for v in f["history_vintages"]:
    if v["fy_label"] in ("FY14", "FY15", "FY16"):
        for y in ("2010", "2011", "2012", "2013"):
            if y in v["eps_normalized"]:
                v["eps_normalized"][y] = v13["eps_normalized"][y]
                v["eps_published"][y] = v13["eps_published"][y]
V["2010-2013 EPS as the FY2013 10-K reports them (no restatement)"] = (f, engine0, B)
# 3. the guidance tables' net income points (2014-2016) unused: the last full year's EPS stands
f = copy.deepcopy(facts0)
f["eps_guides"] = [g for g in f["eps_guides"] if "ni_guide_note" not in g]
V["the table points (2014-2016) unused"] = (f, engine0, B)
# 4. no EPS guide used from 2014
f = copy.deepcopy(facts0)
f["eps_guides"] = [g for g in f["eps_guides"] if g["fy"] < 2014]
V["no EPS guide used from FY2014: the last full year's EPS"] = (f, engine0, B)
# 5. the Q2 2017 range over the release's period-end shares outstanding (380.0M) instead of the quarter's diluted shares (214.0M)
mod = variant_module('            sh = sp[0]["diluted_shares_m"]\n',
                     '            sh = 380.005 if eg["doc"] == "Q2 2017 release" else sp[0]["diluted_shares_m"]\n')
V["the Q2 2017 range over the 380.0M shares outstanding at June 30"] = (facts0, engine0, mod)
# 6. the pro forma FY2017 range of the 8-K of 2017-02-02 used, over the latest print's diluted shares (Q3 2016)
f = copy.deepcopy(facts0)
for g in f["eps_guides"]:
    if "pro_forma_ni_m" in g:
        g["ni_guide_m"] = g.pop("pro_forma_ni_m")
        g.pop("pro_forma_note")
        g["shares_print"] = "Q3 2016"
V["the pro forma FY2017 range used (over Q3 2016's shares)"] = (f, engine0, B)
# 7. BASE on the latest quarter's net margin growth instead of revenue growth as reported
mod = variant_module('    fwd = [latest["sales_pct"]] * 2\n', '    fwd = [latest["nm_pct"]] * 2\n')
V["BASE on the latest quarter's net margin growth instead of revenues"] = (facts0, engine0, mod)
# 8. FY2005 and FY2006 at GAAP ($3.73, $2.68; halved after the split)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    for y, gaap in (("2005", 3.73), ("2006", 2.68)):
        if y in v["eps_normalized"]:
            v["eps_normalized"][y] = gaap
V["FY2005 and FY2006 at GAAP ($3.73, $2.68)"] = (f, engine0, B)
# 9. a five-year P/E window
mod = variant_module('    window = [d for d in days if d > minus_years(as_of, 10) and d >= h["pe_window_start"]]\n',
                     '    window = [d for d in days if d > minus_years(as_of, 5) and d >= h["pe_window_start"]]\n')
V["a five-year P/E window"] = (facts0, engine0, mod)
# 10./11. the Distribution signal (n/r from Q1 2014, scored at BASE) at its BEAR or XBULL value
for lab, val in (("BEAR", "-88.0"), ("XBULL", "57.0")):
    e = engine0.replace('_f(LATEST["dist_pct"])', f'(_f(LATEST["dist_pct"]) if LATEST["dist_pct"] is not None else {val})', 1)
    assert e != engine0
    V[f"the n/r Distribution signal at its {lab} value"] = (facts0, e, B)
# 12./13. every data signal at its BEAR or XBULL value
for lab, vals in (("BEAR", ("-8.0", "-88.0", "-38.0", "-1350.0", "-1150.0")), ("XBULL", ("38.0", "57.0", "261.0", "430.0", "620.0"))):
    e = engine0
    i0, i1 = e.index("SIGNALS = ["), e.index("THEME_SIGNAL_NAME, \"/4\"")
    blk = e[i0:i1]
    for key, val in zip(('_f(LATEST["nm_pct"])', '_f(LATEST["dist_pct"])', '_f(LATEST["sales_pct"])', '_f(LATEST["opm_bp"])',
                         '_f(LATEST["ptm_bp"])'), vals):
        assert key in blk
        blk = blk.replace(key, val)
    V[f"every data signal at its {lab} value"] = (facts0, e[:i0] + blk + e[i1:], B)
for name, (f, e, m) in V.items():
    r = classify_all(f, e, "v", m)
    c, t, mv, span = diff(base, r)
    print(f"{name}: {c} classes, {t} tiers {mv} {span or ''}", flush=True)
