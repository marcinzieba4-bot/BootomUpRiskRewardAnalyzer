#!/usr/bin/env python3
"""How far each LYB judgement call moves the classes: rebuild the 100 dates (2012-02-10 to 2013-12-31) with one encoding changed (in
memory, into a scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/lyb/sens_lyb.py <scratch-out>
"""
import contextlib, copy, io, json, os, runpy, shutil, sys, types
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = sys.argv[1]
sys.path.insert(0, os.path.join(REPO, "retro"))
import build_lyb as B  # noqa: E402
import retro_tool as T  # noqa: E402
from build_acn import load_series, weekly_dates  # noqa: E402
facts0 = json.load(open(B.FACTS, encoding="utf-8"))
engine0 = open(B.ENGINE, encoding="utf-8").read()
raw, spx = load_series("LYB"), load_series("^GSPC")
dates = weekly_dates("2012-02-06", "2013-12-31", sorted(raw), facts0["prints"])
assert len(dates) == 100
tax = T.load_taxonomy()


def variant_module(old, new):
    """A copy of build_lyb with one piece of its source replaced (the module on disk is untouched)."""
    src = open(B.__file__, encoding="utf-8").read()
    assert src.count(old) == 1, old
    m = types.ModuleType("build_lyb_variant")
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
json.dump(base, open(os.path.join(OUT, "main_lyb.json"), "w"), indent=0)
V = {}
# 1. the combined 2010 not a year of revenues (out of the revenue history; rule T keeps its own values)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    v["revenue_usd_b"].pop("2010")
V["the combined 2010 not a year of revenues"] = (f, engine0, B)
# 2. the revenue history from 2008 only (the Predecessor's 2006-2007, Basell before Lyondell Chemical, left out)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    for y in ("2006", "2007"):
        v["revenue_usd_b"].pop(y)
V["the revenue history from 2008 (no 2006-2007)"] = (f, engine0, B)
# 3. the company's adjusted EPS (also removes the warrants' mark to market, impairments and other items that recur): FY11 $4.71
# (Q4 2011 release, Table 9), $5.01 from continuing operations from the Q2 2012 release ($4.32 + $0.69), FY12 $5.22 ($4.96 + $0.26)
f = copy.deepcopy(facts0)
for p in f["prints"]:
    a = p.get("fy_actual")
    if a and a["fy"] == 2011:
        a["eps_normalized"] = 4.71
    if a and a["fy"] == 2012:
        a["eps_normalized"] = 5.22
    for y, rs in p.get("restates", {}).items():
        rs["eps_normalized"] = 5.01
for v in f["history_vintages"]:
    if "2011" in v["eps_normalized"]:
        v["eps_normalized"]["2011"] = 4.71 if v["fy_label"] == "FY11" else 5.01
    if "2012" in v["eps_normalized"]:
        v["eps_normalized"]["2012"] = 5.22
V["the company's adjusted EPS ($4.71, $5.01, $5.22)"] = (f, engine0, B)
# 4. the Q2 2012 restatement unused (FY2011 stays $3.74 and $51.0B until the FY2012 10-K)
f = copy.deepcopy(facts0)
for p in f["prints"]:
    p.pop("restates", None)
V["the Q2 2012 restatement of FY2011 unused"] = (f, engine0, B)
# 5. share counts from 2011 only (no Successor 2010 count)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    v["diluted_shares_m"].pop("2010", None)
f["history_vintages"][0]["diluted_shares_m"] = {}
V["share counts from 2011 only"] = (f, engine0, B)
# 8. 2010's days kept in the P/E window, priced on the first full year's EPS (FY2011's; an anchor no rule gives)
modw = variant_module("    window = [d for d in window if fy(d) not in excluded]\n",
                      "    eps.update({y: eps_hist[min(eps_hist)] for y in excluded})\n    gone = []\n")
V["2010's days in the P/E window on FY2011's EPS"] = (facts0, engine0, modw)
# 6./7. every data signal at its BEAR or XBULL value
for lab, vals in (("BEAR", ("-299.0", "-41.0", "-108.0", "-480.0", "-3290.0")), ("XBULL", ("707.0", "168.0", "196.0", "1270.0", "3550.0"))):
    e = engine0
    i0, i1 = e.index("SIGNALS = ["), e.index('THEME_SIGNAL_NAME, "/4"')
    blk = e[i0:i1]
    for key, val in zip(('_f(LATEST["opa_pct"])', '_f(LATEST["ind_pct"])', '_f(LATEST["sales_pct"])', '_f(LATEST["opm_bp"])'), vals):
        assert key in blk
        blk = blk.replace(key, val)
    k = 'round((FY_MARGIN_BASE - PREV_FY_MARGIN) * 100, 1) if MARGIN_GUIDED else _f(LATEST["ptm_bp"])'
    assert k in blk
    blk = blk.replace(k, vals[4])
    V[f"every data signal at its {lab} value"] = (facts0, e[:i0] + blk + e[i1:], B)
for name, (f, e, m) in V.items():
    try:
        r = classify_all(f, e, "v", m)
    except (AssertionError, SystemExit, ZeroDivisionError, KeyError) as x:
        print(f"{name}: not buildable ({type(x).__name__}: {x})")
        continue
    c, t, mv, span = diff(base, r)
    print(f"{name}: {c} classes, {t} tiers {mv} {span or ''}")
