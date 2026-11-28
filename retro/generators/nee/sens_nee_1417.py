#!/usr/bin/env python3
"""How far each NEE 2014-2017 judgement call moves the classes: rebuild the 208 dates with one encoding changed (in memory, into a
scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/nee/sens_nee_1417.py <scratch-out>
"""
import contextlib, copy, io, json, os, re, runpy, shutil, sys, types
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = sys.argv[1]
sys.path.insert(0, os.path.join(REPO, "retro"))
import build_nee as B  # noqa: E402
import retro_tool as T  # noqa: E402
from build_acn import load_series, weekly_dates  # noqa: E402
facts0 = json.load(open(B.FACTS, encoding="utf-8"))
engine0 = open(B.ENGINE, encoding="utf-8").read()
raw, spx = load_series("NEE"), load_series("^GSPC")
dates = weekly_dates("2014-01-06", "2017-12-31", sorted(raw), facts0["prints"])
assert len(dates) == 208
tax = T.load_taxonomy()


def variant_module(old, new):
    """A copy of build_nee with one line of its source replaced (the module on disk is untouched)."""
    src = open(B.__file__, encoding="utf-8").read()
    assert src.count(old) == 1, old
    m = types.ModuleType("build_nee_variant")
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
json.dump(base, open(os.path.join(OUT, "main1417.json"), "w"), indent=0)
V = {}
# 1. the adjusted EPS outlook as current-FY EPS: the midpoint of the latest range for the year (words keep the range they repeat)
mod = variant_module("    eps_now = eps_hist[last_fy]\n",
                     "    eps_now = eps_hist[last_fy]\n"
                     "    if guides:\n"
                     "        _r = [float(x) for x in re.findall(r'\\$(\\d+\\.\\d+)', guides[-1]['display'])][:2]\n"
                     "        eps_now = round(sum(_r) / 2, 3)\n")
mod.re = re
V["the adjusted EPS outlook's midpoint as current-FY EPS (history GAAP)"] = (facts0, engine0, mod)
# 2. FY2013 from continuing operations: $4.03 (FY2013 10-K), $3.93 (FY2014-FY2016 10-Ks); the Q4 2013 release's $4.47 kept
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    if v["published"] >= "2014-01-01" and "2013" in v["eps_normalized"]:
        v["eps_normalized"]["2013"] = 4.03 if v["fy_label"] == "FY13" else 3.93
V["FY2013 from continuing operations ($4.03, then $3.93 restated)"] = (f, engine0, B)
f2 = copy.deepcopy(f)
for p in f2["prints"]:
    if p.get("fy_actual", {}).get("fy") == 2013:
        p["fy_actual"]["eps_normalized"] = 4.03
V["FY2013 from continuing operations, the Q4 2013 print too ($4.03)"] = (f2, engine0, B)
# 3. the releases' adjusted quarterly EPS for the EPS signal
f = copy.deepcopy(facts0)
for p in f["prints"]:
    if p["published"] >= "2013-07-01":
        p["eps_q"], p["eps_q_prior"] = p["eps_adj"], p["eps_adj_prior"]
        p["eps_pct"] = round((p["eps_q"] / p["eps_q_prior"] - 1) * 100, 1)
modq = variant_module("    for p in public:                               # a print public on AS_OF must match its raw figures\n"
                      "        check_print(p)\n", "")
V["the releases' adjusted quarterly EPS for the EPS signal"] = (f, engine0, modq)
# 4./5. every data signal at its BEAR or XBULL value
for lab, vals in (("BEAR", ("-5.0", "-16.0", "-15.0", "-31.0", "-840.0")), ("XBULL", ("8.0", "12.0", "33.0", "38.0", "320.0"))):
    e = engine0
    i0, i1 = e.index("SIGNALS = ["), e.index("THEME_SIGNAL_NAME, \"/4\"")
    blk = e[i0:i1]
    for key, val in zip(('float(LATEST["kwh_pct"])', 'float(LATEST["seg_pct"])', 'float(LATEST["sales_pct"])', 'float(LATEST["eps_pct"])'), vals):
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
