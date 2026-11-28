#!/usr/bin/env python3
"""How far each SCHW 2010-2013 judgement call moves the classes: rebuild the dates with one encoding changed (in memory,
into a scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/schw/sens_schw_1013.py <scratch-out>

The encodings tried are SCHW's own (retro/README.md, "SCHW"); copy the pattern, not the cases, for another ticker.
"""
import contextlib, copy, io, json, os, re, runpy, shutil, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = sys.argv[1]
sys.path.insert(0, os.path.join(REPO, "retro"))
import build_schw as B  # noqa: E402
import retro_tool as T  # noqa: E402
from build_acn import load_series, weekly_dates  # noqa: E402
facts0 = json.load(open(B.FACTS, encoding="utf-8"))
engine0 = open(B.ENGINE, encoding="utf-8").read()
raw, spx = load_series("SCHW"), load_series("^GSPC")
dates = weekly_dates("2010-01-04", "2013-12-31", sorted(raw), facts0["prints"])
assert len(dates) == 209
tax = T.load_taxonomy()


def classify_all(facts, engine, tag, patch=None):
    out = os.path.join(OUT, tag)
    shutil.rmtree(out, ignore_errors=True)
    res = {}
    for d in dates:
        with contextlib.redirect_stdout(io.StringIO()):
            B.build(d, facts, raw, spx, engine, out)
        mp = os.path.join(out, d, "model.py")
        if patch:
            t = open(mp, encoding="utf-8").read()
            t2 = patch(d, t)
            open(mp, "w", encoding="utf-8").write(t2)
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
    return sum(a[d][0] != b[d][0] for d in dates), sum(a[d][1] != b[d][1] for d in dates), mv


base = classify_all(facts0, engine0, "main")
cnt, tiers = {}, {}
for d in dates:
    cnt[base[d][0]] = cnt.get(base[d][0], 0) + 1
    tiers[base[d][1]] = tiers.get(base[d][1], 0) + 1
print("main:", cnt, tiers)
json.dump(base, open(os.path.join(OUT, "main1013.json"), "w"), indent=0)
V = {}
# 1. FY2010 at $0.65: the releases' net income excluding charges ($775M) over FY2010's 1,194M diluted shares (a derived figure)
f = copy.deepcopy(facts0)
for p in f["prints"]:
    if p["quarter"] == "Q4 2010":
        p["fy_actual"]["eps_normalized"] = 0.65
for v in f["history_vintages"]:
    if "2010" in v["eps_normalized"]:
        v["eps_normalized"]["2010"] = 0.65
V["FY2010 at $0.65 without the charges (net income ex charges / diluted shares, derived)"] = (f, engine0, None)
# 2. FY13E at $0.75: 'mid-$.70s' read as a level, from the Q3 2013 print
def p2(d, t):
    if d >= "2013-10-17":
        t = re.sub(r"EPP_TODAY_EPS   = [\d.]+", "EPP_TODAY_EPS   = 0.75", t)
    return t
V["FY13E at $0.75 ('mid-$.70s' read as a level) from 2013-10-17"] = (facts0, engine0, p2)
# 3. the Q1 2010 'at least 25%' margin read as a guided level: a margin step from FY09's 30.43% to 25% for FY2010
def p3(d, t):
    if "2010-04-16" <= d <= "2011-01-14":
        t = t.replace("MARGIN_GUIDED   = False", "MARGIN_GUIDED   = True")
        t = re.sub(r"FY_MARGIN_BASE  = [\d.]+", "FY_MARGIN_BASE  = 25.0", t)
    return t
V["the Q1 2010 'at least 25%' read as a FY2010 margin of 25% (2010-04-16 to 2011-01-14)"] = (facts0, engine0, p3)
# 4. Q1 2010 as released (no restatement)
f = copy.deepcopy(facts0)
for p in f["prints"]:
    p.pop("restated", None)
V["Q1 2010 as released, no restatement"] = (f, engine0, None)
# 5. FY2002 kept at $0.09, the history and window from 2002 (ten years to the latest one)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    v["eps_normalized"] = {"2002": 0.09, **v["eps_normalized"]}
    v["revenue_usd_b"] = {"2002": 3.293, **v["revenue_usd_b"]}
    v["diluted_shares_m"] = {"2002": 1375.0, **v["diluted_shares_m"]}
    for k in ("eps_normalized", "revenue_usd_b", "diluted_shares_m"):
        v[k] = {y: v[k][y] for y in sorted(v[k])[-10:]}
    v["eps_first_excluded"] = {}
    v["pe_window_start"] = "2002-01-01"
V["FY2002 kept at $0.09, history and window from 2002"] = (f, engine0, None)
# 6. no net buyback/issuance in BASE
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    v["diluted_shares_m"] = {y: 1000.0 for y in v["diluted_shares_m"]}
for p in f["prints"]:
    if p.get("fy_actual"):
        p["fy_actual"]["diluted_shares_m"] = 1000.0
V["no net share issuance in BASE (flat share history)"] = (f, engine0, None)
# 7./8. every data signal at its BEAR or XBULL value
for lab in ("BEAR", "XBULL"):
    e = engine0
    i0, i1 = e.index("SIGNALS = ["), e.index("WEIGHTS = [")
    blk = e[i0:i1]
    vals = {"BEAR": ("-56.0", "-34.0", "35.0", "-91.0", "-3510.0"), "XBULL": ("41.0", "42.0", "-16.0", "68.0", "1330.0")}[lab]
    for key, val in zip(('float(LATEST["sales_pct"])', 'float(LATEST["ca_pct"])', 'float(LATEST["expense_gap_pp"])', 'float(LATEST["dart_pct"])'), vals):
        blk = blk.replace(key, val)
    blk = blk.replace('round((FY_MARGIN_BASE - PREV_FY_MARGIN) * 100, 1) if MARGIN_GUIDED else float(LATEST["pretax_margin_bp"])', vals[4])
    V[f"every data signal at its {lab} value"] = (facts0, e[:i0] + blk + e[i1:], None)
for name, (f, e, patch) in V.items():
    r = classify_all(f, e, "v", patch)
    c, t, mv = diff(base, r)
    print(f"{name}: {c} classes, {t} tiers {mv}")
