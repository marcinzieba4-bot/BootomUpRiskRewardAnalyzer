#!/usr/bin/env python3
"""How far each CHTR 2022-2026 judgement call moves the classes: rebuild the 255 dates (2022-01-07 to 2026-11-20) with one encoding
changed (in memory, into a scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/chtr/sens_chtr_2226.py <scratch-out>
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
# sens_chtr.py's helpers, on this batch's dates (it runs its own 2018-2021 variants only when run as a script)
src = open(os.path.join(HERE, "sens_chtr.py"), encoding="utf-8").read()
head = src.split("base = classify_all(facts0, engine0, \"main\")")[0]
head = head.replace('dates = weekly_dates("2019-01-28", "2021-12-31", sorted(spx), facts0["prints"])\nassert len(dates) == 153',
                    'dates = weekly_dates("2022-01-03", "2026-11-22", sorted(spx), facts0["prints"])\nassert len(dates) == 255')
assert "2022-01-03" in head
g = {"__file__": os.path.join(HERE, "sens_chtr.py")}
sys.argv = [sys.argv[0], OUT]
exec(compile(head, "sens_chtr_2226", "exec"), g)
classify_all, diff, signals_at, facts0, engine0, dates = (g[k] for k in ("classify_all", "diff", "signals_at", "facts0", "engine0", "dates"))

base = classify_all(facts0, engine0, "main")
cnt, tiers, by_year = {}, {}, {}
for d in dates:
    cnt[base[d][0]] = cnt.get(base[d][0], 0) + 1
    tiers[base[d][1]] = tiers.get(base[d][1], 0) + 1
    by_year.setdefault(d[:4], {}).setdefault(base[d][0], 0)
    by_year[d[:4]][base[d][0]] += 1
print("main:", cnt, tiers)
print("by year:", by_year)
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
# the Q3 2026 print on the release's pro forma columns (the Cox Transactions as if closed on 2024-01-01), not its actual ones
f = copy.deepcopy(facts0)
p = next(p for p in f["prints"] if p["quarter"] == "Q3 2026")
PF = {"rev_m": 16505.0, "rev_prior_m": 16764.0, "ebitda_m": 6587.0, "ebitda_prior_m": 6862.0, "rel_k": 36691.0, "rel_prior_k": 37658.0}
p["raw"].update(PF)
r = p["raw"]
p.update(sales_b=round(r["rev_m"] / 1000, 3), sales_pct=round((r["rev_m"] / r["rev_prior_m"] - 1) * 100, 2),
         rel_pct=round((r["rel_k"] / r["rel_prior_k"] - 1) * 100, 2), ocf_margin=round(r["ebitda_m"] / r["rev_m"] * 100, 2),
         ocf_margin_bp=round((round(r["ebitda_m"] / r["rev_m"] * 100, 2) - round(r["ebitda_prior_m"] / r["rev_prior_m"] * 100, 2)) * 100, 1),
         op_margin=round(r["oi_m"] / r["rev_m"] * 100, 2),
         op_margin_bp=round((round(r["oi_m"] / r["rev_m"] * 100, 2) - round(r["oi_prior_m"] / r["rev_prior_m"] * 100, 2)) * 100, 1),
         capex_pct=round(r["capex_m"] / r["rev_m"] * 100, 2),
         capex_bp=round((round(r["capex_m"] / r["rev_m"] * 100, 2) - round(r["capex_prior_m"] / r["rev_prior_m"] * 100, 2)) * 100, 1))
V["Q3 2026 revenue, Adjusted EBITDA and customer relationships on the pro forma columns"] = (f, engine0)
# the Q3 2026 print's customer relationships against the key operating results' pro forma year-ago column only
f = copy.deepcopy(facts0)
p = next(p for p in f["prints"] if p["quarter"] == "Q3 2026")
p["raw"]["rel_prior_k"] = 37658.0
p["rel_pct"] = round((p["raw"]["rel_k"] / p["raw"]["rel_prior_k"] - 1) * 100, 2)
V["Q3 2026 customer relationships against the pro forma year-ago column"] = (f, engine0)
for name, (f, e) in V.items():
    n, nt, mv, span = diff(base, classify_all(f, e, "v"))
    print(f"{name}: {n} classes {mv}{f' ({span[0]} .. {span[1]})' if span else ''}, {nt} tiers")
# a five-year P/E window (the LLY and UNH regime test): the window and its calendar-year lows from five years back, not ten
B = g["B"]
_my = B.minus_years
B.minus_years = lambda d, n: _my(d, 5 if n == 10 else n)
try:
    n, nt, mv, span = diff(base, classify_all(facts0, engine0, "v"))
finally:
    B.minus_years = _my
print(f"a five-year P/E window: {n} classes {mv}{f' ({span[0]} .. {span[1]})' if span else ''}, {nt} tiers")
