#!/usr/bin/env python3
"""How far each TRGP judgement call moves the classes: rebuild the 98 dates (2012-02-24 to 2013-12-31) with one encoding changed (in
memory, into a scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/trgp/sens_trgp.py <scratch-out>                        # the 98 dates of 2012-2013 (README, "TRGP")
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
RANGE = (sys.argv[2], sys.argv[3]) if len(sys.argv) > 3 else ("2012-02-20", "2013-12-31")
dates = weekly_dates(RANGE[0], RANGE[1], sorted(raw), facts0["prints"])
assert len(dates) == {"2012-02-20": 98}.get(RANGE[0], len(dates))
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
json.dump(base, open(os.path.join(OUT, "main_trgp.json"), "w"), indent=0)
V = {}
# 1. CYCLICAL instead of DURABLE (the distribution policy's "seasonal and cyclical factors" read as the 10-Ks calling the business cyclical)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    v["kind"] = "CYCLICAL"
V["CYCLICAL instead of DURABLE"] = (f, engine0, B)
# 2. the revenue history from 2010 only (the IPO year; the pre-IPO years of the consolidated company left out)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    for y in [y for y in v["revenue_usd_b"] if y < "2010"]:
        v["revenue_usd_b"].pop(y)
V["the revenue history from 2010 (no 2006-2009)"] = (f, engine0, B)
# 3. FY2010's 6.5M weighted diluted shares in the buyback (the pre-IPO count, before the Series B converted)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    v["diluted_shares_m"] = {"2010": 6.5, **v["diluted_shares_m"]}
V["FY2010's 6.5M shares in the buyback"] = (f, engine0, B)
# 4. 2010's days kept in the P/E window, priced on the first full year's EPS (FY2011's; an anchor no rule gives)
modw = variant_module("    window = [d for d in window if fy(d) not in excluded]\n",
                      "    eps.update({y: eps_hist[min(eps_hist)] for y in excluded})\n    gone = []\n")
V["2010's days in the P/E window on FY2011's EPS"] = (facts0, engine0, modw)
# 5. BASE on TRC's dividend outlook (the midpoint of 25% to 30%+ for 2013 from 2012-10-18; "in excess of 25%" read as 25% for 2014)
modd = variant_module('    fwd = [latest["sales_pct"]] * 2\n',
                      '    _g = [g for g in guides if g["fy"] >= cur_fy]\n'
                      '    fwd = [{2013: 27.5, 2014: 25.0}[_g[-1]["fy"]]] * 2 if _g else [latest["sales_pct"]] * 2\n')
V["BASE on TRC's dividend outlook (27.5%, then 25%)"] = (facts0, engine0, modd)


# 6./7. every data signal at its BEAR or XBULL value
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
    V[f"every data signal at its {lab} value"] = (facts0, at_values(engine0, vals), B)
for name, (f, e, m) in V.items():
    try:
        r = classify_all(f, e, "v", m)
    except (AssertionError, SystemExit, ZeroDivisionError, KeyError, IndexError) as x:
        print(f"{name}: not buildable ({type(x).__name__}: {x})")
        continue
    c, t, mv, span = diff(base, r)
    print(f"{name}: {c} classes, {t} tiers {mv} {span or ''}")
