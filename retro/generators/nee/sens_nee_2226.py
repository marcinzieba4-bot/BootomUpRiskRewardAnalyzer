#!/usr/bin/env python3
"""How far each NEE 2022-2026 judgement call moves the classes: rebuild the 255 dates with one encoding changed (in memory, into a
scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/nee/sens_nee_2226.py <scratch-out>
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
dates = weekly_dates("2022-01-03", "2026-11-22", sorted(raw), facts0["prints"])
assert len(dates) == 255
tax = T.load_taxonomy()


def variant_module(*pairs):
    """A copy of build_nee with lines of its source replaced (the module on disk is untouched)."""
    src = open(B.__file__, encoding="utf-8").read()
    for old, new in pairs:
        assert src.count(old) == 1, old
        src = src.replace(old, new)
    m = types.ModuleType("build_nee_variant")
    m.__file__ = B.__file__
    exec(compile(src, B.__file__, "exec"), m.__dict__)
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
for y in range(2022, 2027):
    c = {}
    for d in dates:
        if d.startswith(str(y)):
            c[base[d][0]] = c.get(base[d][0], 0) + 1
    print(" ", y, c)
json.dump(base, open(os.path.join(OUT, "main2226.json"), "w"), indent=0)
V = {}
# 1. the adjusted EPS outlook as current-FY EPS: the midpoint of the latest numeric range for the year (history GAAP)
mod = variant_module(("    eps_now = eps_hist[last_fy]\n",
                      "    eps_now = eps_hist[last_fy]\n"
                      "    _rg = [re.findall(r'\\$(\\d+\\.\\d+) (?:to|and) \\$(\\d+\\.\\d+)', x['display']) for x in guides]\n"
                      "    _rg = [r[0] for r in _rg if r]\n"
                      "    if _rg:\n"
                      "        eps_now = round((float(_rg[-1][0]) + float(_rg[-1][1])) / 2, 4)\n"))
mod.re = re
V["the adjusted EPS outlook's midpoint as current-FY EPS (history GAAP)"] = (facts0, engine0, mod)


# 2. history years at the company's adjusted EPS (each Q4 release's adjusted full year; before the 2020 split divided by 4)
def adjusted(years):
    adj = {}
    for p in facts0["prints"]:
        a = p.get("fy_actual")
        if a and a["fy"] in years:
            adj[str(a["fy"])] = (a["raw"]["eps_adj"], p["published"])
    f = copy.deepcopy(facts0)
    for v in f["history_vintages"]:
        for y, (a, pub) in adj.items():
            if y in v["eps_normalized"]:
                pre = pub < "2020-10-27" and v["eps_published"][y] >= "2020-10-27"
                v["eps_normalized"][y] = round(a / 4, 4) if pre else a
    for p in f["prints"]:
        a = p.get("fy_actual")
        if a and str(a["fy"]) in adj:
            a["eps_normalized"] = adj[str(a["fy"])][0]
    return f, {y: v[0] for y, v in adj.items()}


f, a = adjusted(range(2017, 2026))
V[f"FY2017-FY2025 at the company's adjusted EPS {a}"] = (f, engine0, B)
f, a = adjusted(range(2021, 2026))
V[f"FY2021-FY2025 at the company's adjusted EPS {a}"] = (f, engine0, B)
f, a = adjusted((2017, 2018))
V[f"FY2017 and FY2018 at the company's adjusted EPS {a}"] = (f, engine0, B)
# 3. the releases' adjusted quarterly EPS for the EPS signal (the Q4 2021 print then has a growth rate)
f = copy.deepcopy(facts0)
for p in f["prints"]:
    if p["published"] >= "2017-07-01":
        p["eps_q"], p["eps_q_prior"] = p["eps_adj"], p["eps_adj_prior"]
        p["eps_pct"] = round((p["eps_q"] / p["eps_q_prior"] - 1) * 100, 1)
modq = variant_module(("    for p in public:                               # a print public on AS_OF must match its raw figures\n"
                       "        check_print(p)\n", ""))
V["the releases' adjusted quarterly EPS for the EPS signal"] = (f, engine0, modq)
# 4. the Q4 2021 print's n/m EPS growth (against $0.00) at its BEAR or XBULL value instead of BASE
for lab, val in (("BEAR", -31.0), ("XBULL", 38.0)):
    f = copy.deepcopy(facts0)
    p = [p for p in f["prints"] if p["quarter"] == "Q4 2021"][0]
    p["eps_pct"] = val
    V[f"the Q4 2021 print's n/m EPS growth at its {lab} value"] = (f, engine0, modq)
# 5./6. every reported data signal at its BEAR or XBULL value (FPL's energy sales stay as reported: n/r)
lenient = variant_module(('        assert engine.count(old) == 1, ("an EPS edit must match the engine once", old)\n',
                          '        if engine.count(old) != 1:\n            continue\n'))
for lab, vals in (("BEAR", ("-16.0", "-15.0", "-31.0", "-840.0")), ("XBULL", ("12.0", "33.0", "38.0", "320.0"))):
    e = engine0
    i0, i1 = e.index("SIGNALS = ["), e.index("THEME_SIGNAL_NAME, \"/4\"")
    blk = e[i0:i1]
    for key, val in zip(('float(LATEST["seg_pct"])', 'float(LATEST["sales_pct"])', 'float(LATEST["eps_pct"])'), vals):
        assert key in blk
        blk = blk.replace(key, val)
    k = 'round((FY_MARGIN_BASE - PREV_FY_MARGIN) * 100, 1) if MARGIN_GUIDED else float(LATEST["margin_bp"])'
    assert k in blk
    blk = blk.replace(k, vals[3])
    V[f"every reported data signal at its {lab} value"] = (facts0, e[:i0] + blk + e[i1:], lenient)
# 7./8. FPL's energy sales, n/r, at its BEAR or XBULL value instead of BASE
for lab, val in (("BEAR", "-5.0"), ("XBULL", "8.0")):
    m = variant_module(("""    ('float(LATEST["kwh_pct"])', '_f(LATEST["kwh_pct"])'),\n""",
                        f"""    ('float(LATEST["kwh_pct"])', '{val}'),\n"""))
    V[f"FPL's n/r energy sales at its {lab} value"] = (facts0, engine0, m)
for name, (f, e, m) in V.items():
    r = classify_all(f, e, "v", m)
    c, t, mv, span = diff(base, r)
    print(f"{name}: {c} classes, {t} tiers {mv} {span or ''}")
