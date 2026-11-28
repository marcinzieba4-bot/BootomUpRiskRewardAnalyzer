#!/usr/bin/env python3
"""How far each TRGP 2014-2017 judgement call moves the classes: rebuild the 209 dates (2014-01-03 to 2017-12-29) with one encoding
changed (in memory, into a scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/trgp/sens_trgp_1417.py <scratch-out>        # README, "TRGP 2014-2017"
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
RANGE = ("2014-01-01", "2017-12-31")
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
json.dump(base, open(os.path.join(OUT, "main_trgp_1417.json"), "w"), indent=0)
V = {}
P = {p["quarter"]: i for i, p in enumerate(facts0["prints"])}
# 1. FY2015 excluded as distorted (its listed items read as exceeding TRC's income: the Partnership's charges counted in full)
f = copy.deepcopy(facts0)
a = f["prints"][P["Q4 2015"]]["fy_actual"]
a.update(eps_normalized=None, excluded_note="distorted (sensitivity)", eps_gaap=1.09)
a["one_off_test"].update(items_after_tax_m=99.0, distorted=True)
for v in f["history_vintages"]:
    if "2015" in v["eps_normalized"]:
        v["eps_normalized"].pop("2015")
        v["eps_excluded"]["2015"] = "distorted (sensitivity)"
V["FY2015 excluded as distorted"] = (f, engine0, B)
# 2. FY2015 at a derived $1.57 (TRC's $83.9M before the goodwill impairment on 53.6M diluted shares; no filing prints it per share)
f = copy.deepcopy(facts0)
f["prints"][P["Q4 2015"]]["fy_actual"]["eps_normalized"] = 1.57
for v in f["history_vintages"]:
    if "2015" in v["eps_normalized"]:
        v["eps_normalized"]["2015"] = 1.57
V["FY2015 at a derived $1.57 (before the goodwill impairment)"] = (f, engine0, B)
# 3. 2016's share count (the buy-in's 104.5M shares) left out of the buyback
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    v["diluted_shares_m"].pop("2016", None)
V["2016's share count out of the buyback"] = (f, engine0, B)
# 4. the 8-K of 2014-10-23's revenue revision unused (prints and history as first published until a later filing)
f = copy.deepcopy(facts0)
f["revenue_restatements"] = []
for p in f["prints"]:
    p["restated"] = [r for r in p.get("restated", []) if r["source"] != "TG60"]
    if not p["restated"]:
        p.pop("restated")
V["the revenue revision of 2014-10-23 unused"] = (f, engine0, B)
# 5. BASE on TRC's dividend outlooks (2015: about 35% from 2014-10-14; 2016: 15% from 2015-11-03; 2017: 0%, the $3.64 dividend held;
#    2014: "in excess of 25%" read as 25%)
modd = variant_module('    fwd = [latest["sales_pct"]] * 2\n',
                      '    _g = [g for g in guides if g["fy"] >= cur_fy]\n'
                      '    fwd = [{2013: 27.5, 2014: 25.0, 2015: 35.0, 2016: 15.0, 2017: 0.0}[_g[-1]["fy"]]] * 2 if _g else [latest["sales_pct"]] * 2\n')
V["BASE on TRC's dividend outlooks"] = (facts0, engine0, modd)
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
