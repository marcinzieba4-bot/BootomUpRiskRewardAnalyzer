#!/usr/bin/env python3
"""How far each TRGP 2022-2026 judgement call moves the classes: rebuild the 256 dates (2022-01-07 to 2026-11-27) with one encoding
changed (in memory, into a scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/trgp/sens_trgp_2226.py <scratch-out>        # README, "TRGP 2022-2026"
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
RANGE = ("2022-01-01", "2026-11-27")
dates = weekly_dates(RANGE[0], RANGE[1], sorted(raw), facts0["prints"])
assert len(dates) == 256
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
json.dump(base, open(os.path.join(OUT, "main_trgp_2226.json"), "w"), indent=0)
V = {}
EG = [i for i, g in enumerate(facts0["guides"]) if "ni_trc_est_m" in g and g["published"] >= "2022-01-01"]
OPS = {p["source"]: p for p in facts0["prints"]}
# 1. the estimated net income attributable to TRC read as display only: the last full year's EPS stands on every date
f = copy.deepcopy(facts0)
for i in EG:
    g = f["guides"][i]
    f["guides"][i] = {k: g[k] for k in ("fy", "published", "source", "rev_none", "display")}
V["the estimated net income read as display only (the last full year stands)"] = (f, engine0, B)
# 2. no deduction once the Series A is redeemed (the premiums on repurchase of noncontrolling interests and the redemption's deemed
#    dividends not deducted)
f = copy.deepcopy(facts0)
for i in EG:
    if "deduct_ytd_m" in f["guides"][i]:
        f["guides"][i]["deduct_ytd_m"] = 0.0
V["nothing deducted after the redemption"] = (f, engine0, B)
# 3. the 2018-2021 rule read literally after the redemption: 4 x the release's own quarter's Series A dividends, cash and deemed (Q2 2022:
#    $8.2M + $215.5M), no premium
QPREF = {"TG131": 21.8, "TG132": 8.2 + 215.5, "TG133": 0.0}
f = copy.deepcopy(facts0)
for i in EG:
    g = f["guides"][i]
    if "deduct_ytd_m" in g:
        g["deduct_ytd_m"] = round(4 * QPREF.get(g["deduct_source"], 0.0), 1)
V["the quarterly-rate rule read literally after the redemption (x4, no premium)"] = (f, engine0, B)
# 4. the to-common one-offs added back (derived, no filing prints them): FY22 $1,195.5M / 231.1M = $5.17 (no deemed dividends or premium),
#    FY23 $1,345.9M / 226.0M = $5.96 (no Grand Prix premium)
f = copy.deepcopy(facts0)
ADD = {"2022": round(1195.5 / 231.1, 2), "2023": round(1345.9 / 226.0, 2)}
for v in f["history_vintages"]:
    for y, e in ADD.items():
        if y in v["eps_normalized"]:
            v["eps_normalized"][y] = e
            if v.get("one_off_test", {}).get("fy") == int(y):
                v["one_off_test"]["eps_gaap"] = e
V["FY22 and FY23 without their to-common one-offs (derived $5.17, $5.96)"] = (f, engine0, B)
# 5. FY2021 at a pre-tax upper bound without its impairment ($(16.1)M + $452.3M over 228.6M = $1.91; no filing prints it)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    if "2021" in v["eps_excluded"]:
        v["eps_excluded"].pop("2021")
        v["eps_normalized"]["2021"] = round((-16.1 + 452.3) / 228.6, 2)
        if v.get("one_off_test", {}).get("fy") == 2021:
            v["one_off_test"].update(items_after_tax_m=0.0, income_attributable_m=1.0, distorted=False, eps_gaap=round((-16.1 + 452.3) / 228.6, 2))
V["FY21 at a pre-tax upper bound without its impairment ($1.91)"] = (f, engine0, B)
# 6. no ten-year cut of the EPS and share histories (every year from 2011 kept)
f = copy.deepcopy(facts0)
v20 = next(v for v in f["history_vintages"] if v["fy_label"] == "FY20")
for v in f["history_vintages"]:
    if v["published"] > "2022-01-01":
        v["eps_normalized"] = {**v20["eps_normalized"], **v["eps_normalized"]}
        v["diluted_shares_m"] = {**v20["diluted_shares_m"], **v["diluted_shares_m"]}
V["no ten-year cut of the EPS and share histories"] = (f, engine0, B)
# 7. the 8-K of 2022-06-17's standalone estimate unused (the Q1 2022 release's stands to the Q2 2022 release)
f = copy.deepcopy(facts0)
f["guides"] = [g for g in f["guides"] if g["source"] != "TG34"]
V["the 8-K of 2022-06-17's standalone estimate unused"] = (f, engine0, B)
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
