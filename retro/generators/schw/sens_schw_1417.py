#!/usr/bin/env python3
"""How far each SCHW 2014-2017 judgement call moves the classes: rebuild the dates with one encoding changed (in memory,
into a scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/schw/sens_schw_1417.py <scratch-out>

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
dates = weekly_dates("2014-01-06", "2017-12-31", sorted(raw), facts0["prints"])
assert len(dates) == 208
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
json.dump(base, open(os.path.join(OUT, "main1417.json"), "w"), indent=0)
V = {}
# 1. FY2015 at $0.97 and FY2016 at $1.30: GAAP less the per-share effects the releases' 'EPS Impact of Certain Non-Recurring Items'
#    tables list (FY15: litigation proceeds .04, tax benefits .02; FY16: litigation proceeds .01; a derived figure, no filing prints it);
#    FY2014's listed items net to zero (.02 - .03 + .01)
f = copy.deepcopy(facts0)
ADJ = {"2015": 0.97, "2016": 1.30}
for p in f["prints"]:
    a = p.get("fy_actual")
    if a and str(a["fy"]) in ADJ:
        a["eps_normalized"] = ADJ[str(a["fy"])]
for v in f["history_vintages"]:
    for y, e in ADJ.items():
        if y in v["eps_normalized"]:
            v["eps_normalized"][y] = e
V["FY2015 at $0.97 and FY2016 at $1.30 without the listed non-recurring items (derived)"] = (f, engine0, None)
# 2. the two Friday prints (Q2 2015 on 2015-07-17, Q3 2015 on 2015-10-16, filed after Thursday's close) not counted on their own Friday
f = copy.deepcopy(facts0)
for p in f["prints"]:
    if p["quarter"] in ("Q2 2015", "Q3 2015"):
        p["published"] = {"Q2 2015": "2015-07-20", "Q3 2015": "2015-10-19"}[p["quarter"]]
V["the Q2 and Q3 2015 prints from the next Monday (not their own Friday)"] = (f, engine0, None)
# 3. no net buyback/issuance in BASE
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
