#!/usr/bin/env python3
"""How far each TRGP 2018-2021 judgement call moves the classes: rebuild the 209 dates (2018-01-05 to 2021-12-31) with one encoding
changed (in memory, into a scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/trgp/sens_trgp_1821.py <scratch-out>        # README, "TRGP 2018-2021"
"""
import contextlib, copy, io, json, os, runpy, shutil, sys, types
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = sys.argv[1]
sys.path.insert(0, os.path.join(REPO, "retro"))
import build_trgp as B  # noqa: E402
import retro_tool as T  # noqa: E402
from build_acn import load_series, weekly_dates  # noqa: E402
facts0 = json.load(open(B.FACTS, encoding="utf-8"))
engine0 = open(B.ENGINE, encoding="utf-8").read()
raw, spx = load_series("TRGP"), load_series("^GSPC")
RANGE = ("2018-01-01", "2021-12-31")
dates = weekly_dates(RANGE[0], RANGE[1], sorted(raw), facts0["prints"])
assert len(dates) == 209
tax = T.load_taxonomy()


def variant_module(old, new):
    """A copy of build_trgp with one piece of its source replaced (the module on disk is untouched)."""
    src = open(B.__file__, encoding="utf-8").read()
    assert src.count(old) == 1, old
    m = types.ModuleType("build_trgp_variant")
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
json.dump(base, open(os.path.join(OUT, "main_trgp_1821.json"), "w"), indent=0)
V = {}
P = {p["quarter"]: i for i, p in enumerate(facts0["prints"])}
EG = [i for i, g in enumerate(facts0["guides"]) if "ni_trc_est_m" in g]
# 1. the estimated net income attributable to TRC read as display only (the Adjusted EBITDA reconciliation, no earnings guide): the last
#    full year's EPS, FY15's $1.09, stands on every date
f = copy.deepcopy(facts0)
for i in EG:
    g = f["guides"][i]
    f["guides"][i] = {k: g[k] for k in ("fy", "published", "source", "rev_none", "display")}
V["the estimated net income read as display only (FY15 stands)"] = (f, engine0, B)
# 2. no preferred dividends deducted (net income attributable to TRC over the basic count)
f = copy.deepcopy(facts0)
for i in EG:
    f["guides"][i]["pref_q_m"] = [0.0, 0.0]
V["no Series A dividends deducted from the estimate"] = (f, engine0, B)
# 3. the deemed dividends left out of the deduction (cash dividends only)
f = copy.deepcopy(facts0)
for i in EG:
    f["guides"][i]["pref_q_m"] = [f["guides"][i]["pref_q_m"][0], 0.0]
V["cash Series A dividends only (deemed left out)"] = (f, engine0, B)
# 4. the if-converted reading: net income attributable to TRC over the latest public diluted count (Q1 and Q3 2021 include the preferred's
#    conversion shares)
f = copy.deepcopy(facts0)
pub = lambda p: [p] + p.get("restated", [])
for i in EG:
    g = f["guides"][i]
    cands = [(r["published"], r["diluted_shares_m"]) for p in f["prints"] for r in pub(p)
             if r.get("diluted_shares_m") and r["published"] <= g["published"]]
    g["pref_q_m"], g["shares_basic_m"] = [0.0, 0.0], max(cands)[1]
V["if-converted: estimate over the latest diluted count, no deduction"] = (f, engine0, B)
# 5. the loss years at an upper bound without their listed items (pre-tax, before tax and noncontrolling interests; no filing prints it):
#    FY17 ($(63.4)M + $378.0M - $269.5M), FY18 (+ $210.0M), FY19 (+ $243.2M: still a loss), FY20 (+ $2,442.8M), on each year's diluted count
f = copy.deepcopy(facts0)
UP = {2017: (-63.4 + 378.0 - 269.5) / 206.9, 2018: (-119.3 + 210.0) / 224.2, 2020: (-1684.8 + 2442.8) / 232.2}
for p in f["prints"]:
    a = p.get("fy_actual")
    if a and a["fy"] in UP:
        a.update(eps_normalized=round(UP[a["fy"]], 2), eps_gaap=round(UP[a["fy"]], 2), excluded_note=None)
        a["one_off_test"].update(items_after_tax_m=0.0, distorted=False, kind="charges", income_attributable_m=1.0)
for v in f["history_vintages"]:
    for y, e in UP.items():
        if str(y) in v["eps_excluded"]:
            v["eps_excluded"].pop(str(y))
            v["eps_normalized"][str(y)] = round(e, 2)
V["FY17, FY18, FY20 at a pre-tax upper bound without the listed items"] = (f, engine0, B)
# 6. CYCLICAL instead of DURABLE
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    v["kind"] = "CYCLICAL"
V["CYCLICAL instead of DURABLE"] = (f, engine0, B)


# 7./8. every data signal at its BEAR or XBULL value
def at_values(e, vals):
    i0, i1 = e.index("SIGNALS = ["), e.index('THEME_SIGNAL_NAME, "/4"')
    blk = e[i0:i1]
    for key, val in zip(('_f(LATEST["gp_pct"])', '_f(LATEST["lm_pct"])', '_f(LATEST["sales_pct"])', '_f(LATEST["opm_bp"])'), vals):
        assert key in blk
        blk = blk.replace(key, val)
    k = 'round((FY_MARGIN_BASE - PREV_FY_MARGIN) * 100, 1) if MARGIN_GUIDED else _f(LATEST["ptm_bp"])'
    assert k in blk
    return e[:i0] + blk.replace(k, vals[4]) + e[i1:]


os.makedirs(OUT, exist_ok=True)
for lab, vals in (("BEAR", ("-115.0", "-35.0", "-106.0", "-240.0", "-150.0")), ("XBULL", ("34.0", "93.0", "28.0", "190.0", "190.0"))):
    e = at_values(engine0, vals)
    e2 = at_values(open(B.ENGINE2, encoding="utf-8").read(), vals)
    m = variant_module('ENGINE2 = os.path.join(HERE, "templates", "trgp2_engine.py.tmpl")',
                       'ENGINE2 = os.path.join(HERE, "templates", "trgp2_engine.py.tmpl")')    # a copy; its ENGINE2 is set below
    V[f"every data signal at its {lab} value"] = (facts0, e, (m, e2))
for name, (f, e, m) in V.items():
    if isinstance(m, tuple):
        m, e2 = m
        open(os.path.join(OUT, f"e2_{len(name)}.tmpl"), "w", encoding="utf-8").write(e2)
        m.ENGINE2 = os.path.join(OUT, f"e2_{len(name)}.tmpl")
    try:
        r = classify_all(f, e, "v", m)
    except (AssertionError, SystemExit, ZeroDivisionError, KeyError, IndexError) as x:
        print(f"{name}: not buildable ({type(x).__name__}: {x})")
        continue
    c, t, mv, span = diff(base, r)
    print(f"{name}: {c} classes, {t} tiers {mv} {span or ''}")
