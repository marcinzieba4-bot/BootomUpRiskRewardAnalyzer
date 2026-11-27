#!/usr/bin/env python3
"""How far each SCHW 2008-2009 judgement call moves the classes: rebuild the dates with one encoding changed (in memory,
into a scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/schw/sens_schw.py <scratch-out>

The encodings tried are SCHW's own (retro/README.md, "SCHW"); copy the pattern, not the cases, for another ticker.
"""
import contextlib
import copy
import glob
import io
import json
import os
import runpy
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = sys.argv[1]
sys.path.insert(0, os.path.join(REPO, "retro"))
import build_schw as B  # noqa: E402
import retro_tool as T  # noqa: E402
from build_acn import load_series, weekly_dates  # noqa: E402

facts0 = json.load(open(B.FACTS, encoding="utf-8"))
engine0 = open(B.ENGINE, encoding="utf-8").read()
raw, spx = load_series("SCHW"), load_series("^GSPC")
dates = weekly_dates("2008-01-01", "2008-12-31", sorted(raw), facts0["prints"]) + \
    weekly_dates("2009-01-05", "2009-12-31", sorted(raw), facts0["prints"])
assert len(dates) == 105
tax = T.load_taxonomy()


def classify_all(facts, engine, tag):
    out = os.path.join(OUT, tag)
    shutil.rmtree(out, ignore_errors=True)
    res = {}
    for d in dates:
        with contextlib.redirect_stdout(io.StringIO()):
            B.build(d, facts, raw, spx, engine, out)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            g = runpy.run_path(os.path.join(out, d, "model.py"), run_name="__retro__")
        q = T.retro_classify(dict(g["RESULT"], report=buf.getvalue()), g["PIT_PROFILE"], tax)
        res[d] = (q["price_state"], g["RESULT"]["signal_short"])
    return res


def diff(a, b):
    cls = sum(a[d][0] != b[d][0] for d in dates)
    tier = sum(a[d][1] != b[d][1] for d in dates)
    moves = {}
    for d in dates:
        if a[d][0] != b[d][0]:
            k = f"{a[d][0]}->{b[d][0]}"
            moves[k] = moves.get(k, 0) + 1
    return cls, tier, moves


base = classify_all(facts0, engine0, "main")
cnt = {}
for d in dates:
    cnt[base[d][0]] = cnt.get(base[d][0], 0) + 1
tiers = {}
for d in dates:
    tiers[base[d][1]] = tiers.get(base[d][1], 0) + 1
print("main:", cnt, tiers)
json.dump(base, open(os.path.join(OUT, "main.json"), "w"), indent=0)

variants = {}
# 1. FY2002 kept at GAAP $0.09 (no AAPL-test exclusion): the history and the window from 2002
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    v["eps_normalized"] = {"2002": 0.09, **v["eps_normalized"]}
    v["revenue_usd_b"] = {"2002": 3.293, **v["revenue_usd_b"]}
    v["diluted_shares_m"] = {"2002": 1375.0, **v["diluted_shares_m"]}
    v["eps_first_excluded"] = {}
    v["pe_window_start"] = "2002-01-01"
variants["FY2002 kept at $0.09, history and window from 2002"] = (f, engine0)
# 2. no net share repurchase in BASE (a flat share history; shows what BASE rests on)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    v["diluted_shares_m"] = {y: 1000.0 for y in v["diluted_shares_m"]}
for p in f["prints"]:
    if p.get("fy_actual"):
        p["fy_actual"]["diluted_shares_m"] = 1000.0
variants["no net buyback in BASE (flat share history)"] = (f, engine0)
# 3. FY2008 at $1.10, the Q3 charges' $.04 excluded (a derived figure; no filing publishes it)
f = copy.deepcopy(facts0)
for p in f["prints"]:
    if p["quarter"] == "Q4 2008":
        p["fy_actual"]["eps_normalized"] = 1.10
for v in f["history_vintages"]:
    if "2008" in v["eps_normalized"]:
        v["eps_normalized"]["2008"] = 1.10
variants["FY2008 at $1.10 without the Q3 2008 securities charges"] = (f, engine0)
# 4./5. every data signal at its BEAR or XBULL value
for lab, idx in (("BEAR", 2), ("XBULL", 5)):
    e = engine0
    for key in ('float(LATEST["sales_pct"])', 'float(LATEST["ca_pct"])', 'float(LATEST["expense_gap_pp"])', 'float(LATEST["dart_pct"])'):
        assert key in e
    sig_start = e.index("SIGNALS = [")
    sig_end = e.index("WEIGHTS = [")
    block = e[sig_start:sig_end]
    new = block
    vals = {"BEAR": ("-56.0", "-34.0", "35.0", "-91.0", "-3510.0"), "XBULL": ("41.0", "42.0", "-16.0", "68.0", "1330.0")}[lab]
    for key, val in zip(('float(LATEST["sales_pct"])', 'float(LATEST["ca_pct"])', 'float(LATEST["expense_gap_pp"])',
                         'float(LATEST["dart_pct"])'), vals[:4]):
        new = new.replace(key, val)
    new = new.replace('round((FY_MARGIN_BASE - PREV_FY_MARGIN) * 100, 1) if MARGIN_GUIDED else float(LATEST["pretax_margin_bp"])', vals[4])
    variants[f"every data signal at its {lab} value"] = (facts0, e[:sig_start] + new + e[sig_end:])
# 6. the Friday 2009-01-16 print read as not meeting that day's close: the date takes the state before it
f = copy.deepcopy(facts0)
for p in f["prints"]:
    if p["quarter"] == "Q4 2008":
        p["published"] = "2009-01-20"
        f["sources"][p["source"]] = {**f["sources"][p["source"]], "published": "2009-01-20"}
variants["the Q4 2008 print from the next trading day (2009-01-20)"] = (f, engine0)

for name, (f, e) in variants.items():
    r = classify_all(f, e, "v")
    c, t, mv = diff(base, r)
    print(f"{name}: {c} classes, {t} tiers {mv}")
