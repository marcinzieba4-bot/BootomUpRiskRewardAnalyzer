#!/usr/bin/env python3
"""How far each LYB judgement call moves the classes: rebuild the 100 dates (2012-02-10 to 2013-12-31) with one encoding changed (in
memory, into a scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/lyb/sens_lyb.py <scratch-out>                          # the 100 dates of 2012-2013
    python3 retro/generators/lyb/sens_lyb.py <scratch-out> 2014-01-01 2017-12-31    # the 209 of 2014-2017 (README, "LYB 2014-2017")
    python3 retro/generators/lyb/sens_lyb.py <scratch-out> 2018-01-01 2021-12-31    # the 209 of 2018-2021 (README, "LYB 2018-2021")
    python3 retro/generators/lyb/sens_lyb.py <scratch-out> 2022-01-03 2026-11-22    # the 255 of 2022-2026 (README, "LYB 2022-2026")
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
RANGE = (sys.argv[2], sys.argv[3]) if len(sys.argv) > 3 else ("2012-02-06", "2013-12-31")
dates = weekly_dates(RANGE[0], RANGE[1], sorted(raw), facts0["prints"])
assert len(dates) == {"2012-02-06": 100, "2014-01-01": 209, "2018-01-01": 209, "2022-01-03": 255}.get(RANGE[0], len(dates))
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
    v["revenue_usd_b"].pop("2010", None)
V["the combined 2010 not a year of revenues"] = (f, engine0, B)
# 2. the revenue history from 2008 only (the Predecessor's 2006-2007, Basell before Lyondell Chemical, left out)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    for y in ("2006", "2007"):
        v["revenue_usd_b"].pop(y, None)
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
# 9. the company's EPS excluding the lower of cost or market adjustments (Table 1's 'Excluding LCM Impact' block, which also removes an
# item that recurs): FY14 $8.92, FY15 $10.35, FY16 $9.20 (Q4 2014, Q4 2015 and Q4 2016 releases), FY13 and earlier as reported
LCM = {"2014": 8.92, "2015": 10.35, "2016": 9.20}
f = copy.deepcopy(facts0)
for p in f["prints"]:
    a = p.get("fy_actual")
    if a and str(a["fy"]) in LCM:
        a["eps_normalized"] = LCM[str(a["fy"])]
for v in f["history_vintages"]:
    for y, e in LCM.items():
        if y in v["eps_normalized"]:
            v["eps_normalized"][y] = e
V["the company's EPS excluding LCM ($8.92, $10.35, $9.20)"] = (f, engine0, B)
# 10. ENERGY_TRANSITION read as out of scope (no watch list; the 'why' as before its live date)
modet = variant_module('    if et["live_from"] <= as_of and not et_out:\n', "    if False:\n")
V["ENERGY_TRANSITION out of scope"] = (facts0, engine0, modet)
# 11. the ten-year roll unused (every revenue year kept)
f = copy.deepcopy(facts0)
allrev = {}
for v in f["history_vintages"]:                    # every year each vintage dropped, at the latest value before it dropped
    allrev.update(v["revenue_usd_b"])
    for y, x in allrev.items():
        v["revenue_usd_b"].setdefault(y, x)
V["the ten-year roll unused (every revenue year kept)"] = (f, engine0, B)
# 12. FY2017 without its listed one-offs: the Q4 2017 release says they 'positively impacted full year 2017 earnings by $2.05 per
# share' (the tax reform benefit, the Geosel gain and the bond refinancing), so $12.28 - $2.05 = $10.23 (derived: no filing prints it)
def set_eps(f, y, e):
    for p in f["prints"]:
        a = p.get("fy_actual")
        if a and a["fy"] == y:
            a["eps_normalized"] = e
            if "eps_gaap" in a:          # a 2022-2026 Q4 print: the tested figure stands in for its GAAP EPS too
                a["eps_gaap"] = e
    for v in f["history_vintages"]:
        if str(y) in v["eps_normalized"]:
            v["eps_normalized"][str(y)] = e


f = copy.deepcopy(facts0)
set_eps(f, 2017, 10.23)
V["FY2017 without its listed one-offs ($10.23, derived)"] = (f, engine0, B)
# 13. FY2020 at the company's EPS excluding LCM and impairment ($5.61, the Q4 2020 release's Table 1; it also removes the LCM
# adjustments, which recur); FY2019 and earlier as reported
f = copy.deepcopy(facts0)
set_eps(f, 2020, 5.61)
V["FY2020 excluding LCM and impairment ($5.61)"] = (f, engine0, B)
# 14. the 2010 share count kept after the ten-year roll (the FY2020 vintage)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    if v["fy_label"] == "FY20":
        v["diluted_shares_m"]["2010"] = 564.0
V["the 2010 share count kept in the FY2020 vintage"] = (f, engine0, B)
# 15. the 10-Q's operating income unused: the four prints without it in the release (Q1-Q2 2018, Q2-Q3 2021) score the operating
# margin signal at its BASE threshold (70 bp), as an unreported signal would (the engine prints the margin, so the value stands in)
modoi = variant_module("    i = public.index(latest)\n",
                       "    i = public.index(latest)\n    if latest.get('oi_source'):\n        latest = {**latest, 'opm_bp': 70.0}\n")
V["the 10-Q's operating income unused (those prints' margin signal at BASE)"] = (facts0, engine0, modoi)
# 6./7. every data signal at its BEAR or XBULL value
def at_values(e, vals):
    i0, i1 = e.index("SIGNALS = ["), e.index('THEME_SIGNAL_NAME, "/4"')
    blk = e[i0:i1]
    for key, val in zip(('_f(LATEST["opa_pct"])', '_f(LATEST["ind_pct"])', '_f(LATEST["sales_pct"])', '_f(LATEST["opm_bp"])'), vals):
        assert key in blk
        blk = blk.replace(key, val)
    k = 'round((FY_MARGIN_BASE - PREV_FY_MARGIN) * 100, 1) if MARGIN_GUIDED else _f(LATEST["ptm_bp"])'
    assert k in blk
    return e[:i0] + blk.replace(k, vals[4]) + e[i1:]


engine_nr0 = open(B.ENGINE_NR, encoding="utf-8").read()
os.makedirs(OUT, exist_ok=True)
for lab, vals in (("BEAR", ("-299.0", "-41.0", "-108.0", "-480.0", "-3290.0")), ("XBULL", ("707.0", "168.0", "196.0", "1270.0", "3550.0"))):
    nr = os.path.join(OUT, f"lyb2_{lab}.tmpl")
    open(nr, "w", encoding="utf-8").write(at_values(engine_nr0, vals))
    modnr = variant_module('ENGINE_NR = os.path.join(HERE, "templates", "lyb2_engine.py.tmpl")', f"ENGINE_NR = {nr!r}")
    V[f"every data signal at its {lab} value"] = (facts0, at_values(engine0, vals), modnr)
if RANGE[0] >= "2022-01-01":
    # ── 2022-2026 (retro/README.md, "LYB 2022-2026"): the calls that still reach these dates, and this batch's own ──
    V = {k: V[k] for k in ("the company's EPS excluding LCM ($8.92, $10.35, $9.20)", "FY2017 without its listed one-offs ($10.23, derived)",
                           "FY2020 excluding LCM and impairment ($5.61)", "ENERGY_TRANSITION out of scope",
                           "the 10-Q's operating income unused (those prints' margin signal at BASE)",
                           "every data signal at its BEAR value", "every data signal at its XBULL value")}
    # a. the company's EPS excluding identified items (it also removes the LCM adjustments and recurring asset write-downs): FY21
    # $18.19, FY22 $12.46, FY23 $8.65, FY24 $6.40 (each Q4 release's Table 3), FY25 $1.70 (the Q4 2025 release), so FY2025 is kept
    f = copy.deepcopy(facts0)
    ADJ = {2021: 18.19, 2022: 12.46, 2023: 8.65, 2024: 6.40}
    for y, e in ADJ.items():
        set_eps(f, y, e)
    for p in f["prints"]:
        a = p.get("fy_actual")
        if a and a["fy"] == 2025:
            a.update(eps_normalized=1.70, eps_gaap=1.70, excluded_note=None)
            a["one_off_test"].update(items_after_tax_m=0.0, income_attributable_m=563.0, distorted=False)   # on the adjusted figure
    for v in f["history_vintages"]:
        if v["eps_excluded"].pop("2025", None):
            v["eps_normalized"]["2025"] = 1.70
    V["the company's EPS excluding identified items (FY21-FY25: $18.19, $12.46, $8.65, $6.40, $1.70)"] = (f, engine0, B)
    # b. the Q4 operating income derived, from each 10-K's date, as the 10-K's year less the Q3 10-Q's nine months (both years; for
    # Q4 2025 the pre-tax income too): Q4 2021 $911M vs $893M, Q4 2022 $487M vs $911M, Q4 2023 $315M vs $487M, Q4 2024 $(659)M vs
    # $315M, Q4 2025 $(88)M vs $(597)M, pre-tax $(142)M vs $(818)M (no filing prints these quarters; derived for this test only)
    Q4D = {"Q4 2021": ("2022-02-25", 911.0, 893.0, None), "Q4 2022": ("2023-02-23", 487.0, 911.0, None),
           "Q4 2023": ("2024-02-22", 315.0, 487.0, None), "Q4 2024": ("2025-02-27", -659.0, 315.0, None),
           "Q4 2025": ("2026-02-20", -88.0, -597.0, (-142.0, -818.0))}
    modq4 = variant_module("    i = public.index(latest)\n",
                           "    i = public.index(latest)\n"
                           f"    _Q4D = {Q4D!r}\n"
                           "    if latest['quarter'] in _Q4D and as_of >= _Q4D[latest['quarter']][0]:\n"
                           "        _d, _o, _op, _pt = _Q4D[latest['quarter']]\n"
                           "        _r = latest['raw']\n"
                           "        _mg = lambda x, r: round(x / r * 100 + 0.0, 2)\n"
                           "        latest = {**latest, 'opm': _mg(_o, _r['rev_m']), 'opm_bp': round((_mg(_o, _r['rev_m']) - _mg(_op, _r['rev_prior_m'])) * 100, 1)}\n"
                           "        if _pt:\n"
                           "            latest.update(ptm=_mg(_pt[0], _r['rev_m']), ptm_bp=round((_mg(_pt[0], _r['rev_m']) - _mg(_pt[1], _r['rev_prior_m'])) * 100, 1))\n"
                           "        prints = prints[:-1] + [latest] if prints[-1]['quarter'] == latest['quarter'] else prints\n")
    V["the Q4 operating income derived from each 10-K (year less nine months)"] = (facts0, engine0, modq4)
    # c. Q3 2026's segment signals n/r (no year-ago column in its release) instead of the Q3 2025 release's year-ago quarter
    modseg = variant_module("    i = public.index(latest)\n",
                            "    i = public.index(latest)\n    if latest['quarter'] == 'Q3 2026':\n"
                            "        latest = {**latest, 'opa_pct': None, 'ind_pct': None}\n")
    V["Q3 2026's segment signals n/r (no year-ago quarter from the Q3 2025 release)"] = (facts0, engine0, modseg)
    # d. the FY2025 10-K's restatement of FY2023-FY2024 (the refining business discontinued) unused: FY23 $6.48, FY24 $4.14 kept
    f = copy.deepcopy(facts0)
    for v in f["history_vintages"]:
        if v["fy_label"] == "FY25":
            v["eps_normalized"].update({"2023": 6.48, "2024": 4.14})
    V["the FY2025 10-K's restated FY2023-FY2024 unused ($6.48, $4.14)"] = (f, engine0, B)
    # e. the EPS history not cut to the ten fiscal years (2011 on kept in every vintage)
    f = copy.deepcopy(facts0)
    allep = {}
    for v in f["history_vintages"]:
        allep.update(v["eps_normalized"])
        for y, x in allep.items():
            if y not in v.get("eps_excluded", {}):
                v["eps_normalized"].setdefault(y, x)
        v["eps_normalized"] = dict(sorted(v["eps_normalized"].items()))
    V["the EPS history not cut to ten years (2011 on kept)"] = (f, engine0, B)
for name, (f, e, m) in V.items():
    try:
        r = classify_all(f, e, "v", m)
    except (AssertionError, SystemExit, ZeroDivisionError, KeyError) as x:
        print(f"{name}: not buildable ({type(x).__name__}: {x})")
        continue
    c, t, mv, span = diff(base, r)
    print(f"{name}: {c} classes, {t} tiers {mv} {span or ''}")
