#!/usr/bin/env python3
"""How far each CHTR 2018-2021 judgement call moves the classes: rebuild the 153 dates (2019-02-01 to 2021-12-31) with one encoding
changed (in memory, into a scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/chtr/sens_chtr.py <scratch-out>
"""
import contextlib, copy, io, json, os, runpy, shutil, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = sys.argv[1]
sys.path.insert(0, os.path.join(REPO, "retro"))
import build_chtr as B  # noqa: E402
import retro_tool as T  # noqa: E402
from build_acn import load_series, weekly_dates  # noqa: E402
facts0 = json.load(open(B.FACTS, encoding="utf-8"))
engine0 = open(B.ENGINE, encoding="utf-8").read()
raw, spx = load_series("CHTR"), load_series("^GSPC")
dates = weekly_dates("2019-01-28", "2021-12-31", sorted(spx), facts0["prints"])
assert len(dates) == 153
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
    shutil.rmtree(out, ignore_errors=True)
    return res


def diff(a, b):
    mv = {}
    ch = [d for d in dates if a[d][0] != b[d][0]]
    for d in ch:
        k = f"{a[d][0]}->{b[d][0]}"
        mv[k] = mv.get(k, 0) + 1
    return len(ch), sum(a[d][1] != b[d][1] for d in dates), mv, (ch[0], ch[-1]) if ch else None


def signals_at(engine, col):
    """Every scored signal at one of its thresholds (col 2 BEAR, 5 XBULL), from the engine's own SIGNALS table."""
    vals = {"rel_pct": (2.0, 293.0), "sales_pct": (-4.0, 197.0), "ocf_margin_bp": (-240.0, 160.0), "capex_bp": (960.0, -550.0),
            "op_margin_bp": (-560.0, 210.0)}
    e = engine
    for k, (bear, xbull) in vals.items():
        old = f'float(LATEST["{k}"])'
        assert e.count(old) == 1, k
        e = e.replace(old, repr(bear if col == 2 else xbull))
    return e


base = classify_all(facts0, engine0, "main")
cnt, tiers = {}, {}
for d in dates:
    cnt[base[d][0]] = cnt.get(base[d][0], 0) + 1
    tiers[base[d][1]] = tiers.get(base[d][1], 0) + 1
print("main:", cnt, tiers)
json.dump(base, open(os.path.join(OUT, "main_chtr.json"), "w"), indent=0)
V = {}
V["every signal at its BEAR value"] = (facts0, signals_at(engine0, 2))
V["every signal at its XBULL value"] = (facts0, signals_at(engine0, 5))
old = "BUYBACK           = _cagr(SHARES_HIST[_SY[-1]], SHARES_HIST[_SY[0]], _SY[-1] - _SY[0]) if len(_SY) > 1 else 0.0"
assert engine0.count(old) == 1
V["no net buyback in BASE"] = (facts0, engine0.replace(old, "BUYBACK = 0.0"))
# FY2017 kept at GAAP $34.09 (its Tax Reform benefit not tested): the history and the window start with 2017
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    if "2017" in v.get("one_off_tests", {}):
        v["one_off_tests"]["2017"] = {**v["one_off_tests"]["2017"], "distorted": False}
f["history_start"] = {**f["history_start"], "fy": 2017}
V["FY2017 kept at GAAP $34.09 (history and window from 2017)"] = (f, engine0)
for name, (f, e) in V.items():
    n, nt, mv, span = diff(base, classify_all(f, e, "v"))
    print(f"{name}: {n} classes {mv}{f' ({span[0]} .. {span[1]})' if span else ''}, {nt} tiers")
