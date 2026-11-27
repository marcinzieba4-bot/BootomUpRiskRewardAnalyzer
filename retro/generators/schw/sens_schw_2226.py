#!/usr/bin/env python3
"""How far each SCHW 2022-2026 judgement call moves the classes: rebuild the dates with one encoding changed (in memory,
into a scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/schw/sens_schw_2226.py <scratch-out>

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
engine20 = open(B.ENGINE2, encoding="utf-8").read()
ENG2 = os.path.join(OUT, "schw2_engine.py.tmpl")
raw, spx = load_series("SCHW"), load_series("^GSPC")
dates = weekly_dates("2022-01-03", "2026-11-22", sorted(raw), facts0["prints"])
assert len(dates) == 255
tax = T.load_taxonomy()


def classify_all(facts, engine, tag, patch=None, engine2=None):
    os.makedirs(OUT, exist_ok=True)
    open(ENG2, "w", encoding="utf-8").write(engine2 or engine20)     # the None-tolerant copy the builder reads for n/r trades
    B.ENGINE2 = ENG2
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
json.dump(base, open(os.path.join(OUT, "main2226.json"), "w"), indent=0)
V = {}
# 1. the company's adjusted diluted EPS every year (it also removes the recurring amortization of acquired intangibles; Q4 releases)
ADJ = {"2021": 3.25, "2022": 3.90, "2023": 3.13, "2024": 3.25, "2025": 4.87}
# 2. FY2023 without only the restructuring and acquisition and integration-related costs: $2.54 + $.22 + $.27 less their share of the
#    stated $(.19) tax effects (derived; no filing prints it)
for lab, sub in (("the company's adjusted EPS for FY2021-FY2025 (amortization out too)", ADJ),
                 ("FY2023 at $2.91 without the restructuring and integration costs (derived)", {"2023": 2.91})):
    f = copy.deepcopy(facts0)
    for p in f["prints"]:
        a = p.get("fy_actual")
        if a and str(a["fy"]) in sub:
            a["eps_normalized"] = sub[str(a["fy"])]
    for v in f["history_vintages"]:
        for y, e in sub.items():
            if y in v["eps_normalized"]:
                v["eps_normalized"][y] = e
    V[lab] = (f, engine0, None, None)
# 3. from Q1 2023 the release hosts its business update 'this morning' (8:30-9:00 a.m. ET): each print from its dateline day, before
#    the open, instead of the 8-K's next trading day
f = copy.deepcopy(facts0)
for p in f["prints"]:
    if p["published"] > "2023-04-01" and "this morning" in p.get("release_time", ""):
        d0 = re.search(r"accepted (\d{4}-\d\d-\d\d) ", p["release_time"]).group(1)
        p["published"] = f["sources"][p["source"]]["published"] = d0
        p["release_time"] = f"released {d0} before the open (illustrative)"
V["each print from Q1 2023 on its release morning (not the 8-K's next day)"] = (f, engine0, None, None)
# 4. the three Friday prints (filed after Thursday's close) from the next trading day
f = copy.deepcopy(facts0)
NEXT = {"Q3 2025": "2025-10-20", "Q1 2026": "2026-04-20", "Q3 2026": "2026-10-19"}
for p in f["prints"]:
    if p["quarter"] in NEXT:
        p["published"] = NEXT[p["quarter"]]
V["the three Friday prints from the next trading day"] = (f, engine0, None, None)
# 5. no net share change in BASE
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    v["diluted_shares_m"] = {y: 1000.0 for y in v["diluted_shares_m"]}
for p in f["prints"]:
    if p.get("fy_actual"):
        p["fy_actual"]["diluted_shares_m"] = 1000.0
V["no net share change in BASE (flat share history)"] = (f, engine0, None, None)
# 6. CRYPTO off the watch list (no crypto words in the FY2025 vintage)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    v.pop("crypto_quote", None), v.pop("crypto_own_quote", None)
V["CRYPTO off the watch list"] = (f, engine0, None, None)
# 7. DATs as the trades signal (the successor row)
f = copy.deepcopy(facts0)
for p in f["prints"]:
    if p.get("dats_k") is not None:
        p["dart_k"], p["raw"]["dart_k"], p["raw"]["dart_prior_k"] = p["dats_k"], p["dats_k"], p["dats_prior_k"]
        p["dart_pct"] = round((p["dats_k"] / p["dats_prior_k"] - 1) * 100 + 0.0, 1)
V["DATs as the trades signal (not n/r)"] = (f, engine0, None, None)
# 8./9. every data signal at its BEAR or XBULL value (both engines)
for lab in ("BEAR", "XBULL"):
    vals = {"BEAR": ("-56.0", "-34.0", "35.0", "-91.0", "-3510.0"), "XBULL": ("41.0", "42.0", "-16.0", "68.0", "1330.0")}[lab]
    out = []
    for e, dk in ((engine0, 'float(LATEST["dart_pct"])'), (engine20, '_f(LATEST["dart_pct"])')):
        i0, i1 = e.index("SIGNALS = ["), e.index("WEIGHTS = [")
        blk = e[i0:i1]
        for key, val in zip(('float(LATEST["sales_pct"])', 'float(LATEST["ca_pct"])', 'float(LATEST["expense_gap_pp"])', dk), vals):
            assert key in blk, key
            blk = blk.replace(key, val)
        blk = blk.replace('round((FY_MARGIN_BASE - PREV_FY_MARGIN) * 100, 1) if MARGIN_GUIDED else float(LATEST["pretax_margin_bp"])', vals[4])
        out.append(e[:i0] + blk + e[i1:])
    V[f"every data signal at its {lab} value"] = (facts0, out[0], None, out[1])
for name, (f, e, patch, e2) in V.items():
    r = classify_all(f, e, "v", patch, e2)
    c, t, mv = diff(base, r)
    print(f"{name}: {c} classes, {t} tiers {mv}")
