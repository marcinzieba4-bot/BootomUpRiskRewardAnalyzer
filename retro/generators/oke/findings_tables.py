#!/usr/bin/env python3
"""HINDSIGHT. Tables for staging/retrospective/OKE/FINDINGS.md from outcome.json (labels, never inputs): 2-year returns by
class and legacy tier, by current-FY EPS and by latest print, per year, plus 3-year and drawdown lines.

    python3 retro/generators/oke/findings_tables.py 2008,2009
    python3 retro/generators/oke/findings_tables.py 2010,2011,2012,2013
    python3 retro/generators/oke/findings_tables.py 2014,2015,2016,2017

Run it only after the batch's build, validation outputs, README section and firewall result are committed and pushed, and
`retro_tool.py outcome` has written the outcomes (retro/README.md, "Adding dates"). Nothing it prints may feed a fact sheet,
a builder or a rule.
"""
import glob
import json
import os
import re
import statistics
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
rows = []
pending = []
for d in sorted(x for x in glob.glob(os.path.join(REPO, "staging", "retrospective", "OKE", "20*")) if os.path.basename(x)[:4] in sys.argv[1].split(",")):
    a = json.load(open(os.path.join(d, "analysis.json")))
    if not os.path.exists(os.path.join(d, "outcome.json")):     # (NEM 2022-2026) the newest date: no outcome yet
        pending.append(os.path.basename(d))
        continue
    o = json.load(open(os.path.join(d, "outcome.json")))
    m = open(os.path.join(d, "model.py"), encoding="utf-8").read()
    eps = eval(re.search(r'^EPS_LABEL\s+= (.+)$', m, re.M).group(1))
    fy = re.search(r"(FY\d{4}E): GAAP net income guidance, the (.+?)'s \$([\d.]+-[\d.]+) a diluted share, midpoint = \$([\d.]+)", eps)
    if not fy:     # (OKE 2010-2013) a net income range in millions over a print's diluted shares
        fy = re.search(r"(FY\d{4}E): GAAP net income guidance, the (.+?)'s \$([\d,]+-[\d,]+ million) .*? = \$([\d.]+)", eps)
    if not fy:     # (OKE 2014-2017) a point from the guidance tables, or no guide (the last full year's EPS)
        fy = re.search(r"(FY\d{4}E): GAAP net income guidance, the (.+?)'s \$([\d,]+ million) .*? = \$([\d.]+)", eps)
    if not fy:
        fy = re.search(r"(FY\d{4}E): no EPS guide in scope yet, (FY\d\d)'s \$([\d.]+)() stands", eps)
        fy = type("M", (), {"group": lambda self, i, f=fy: {1: f.group(1), 2: "last full year, " + f.group(2), 3: f.group(3),
                                                              4: f.group(3)}[i]})()
    q = re.search(r"latest print (Q\d \d{4})", a["summary"]) or re.search(r'"quarter": "(Q\d \d{4})"', m)
    lq = re.search(r"LATEST\s+= \{'quarter': '(Q\d \d{4})'", m).group(1)
    h2, h3 = o["horizons"].get("2y"), o["horizons"].get("3y")
    if not h2 or o.get("within_2y") is None or o.get("call_check_2y") is None:   # (NEE 2022-2026) no 2-year horizon yet: left out
        pending.append(a["as_of"])
        continue
    rows.append(dict(date=a["as_of"], price=a["price"], cls=a["classification"]["price_state"], tier=a["legacy_signal_short"],
                     fy=f"{fy.group(1)[:2]}{fy.group(1)[4:]} ${fy.group(4)} (the {fy.group(2)}'s ${fy.group(3)})", lq=lq,
                     r2=h2["total_return_pct"], x2=h2["excess_pct"], hu2=h2["hurdle_pct"], r3=h3["total_return_pct"] if h3 else None,
                     x3=h3["excess_pct"] if h3 else None, hu3=h3["hurdle_pct"] if h3 else None,
                     avg=o["within_2y"]["return_to_avg_price_m12_m24_pct"], dd=o["within_2y"]["max_drawdown_pct"],
                     hit=o["call_check_2y"]["hit"], land=o["scenario_landing_2y"], r1=o["horizons"]["1y"]["total_return_pct"],
                     x1=o["horizons"]["1y"]["excess_pct"], drift=o.get("profile_drift")))


def line(name, rs):
    med = statistics.median_high([r["r2"] for r in rs])
    return (f"| {name} ({rs[0]['date']} to {rs[-1]['date']}) | {len(rs)} | {med:+.1f}% | {min(r['r2'] for r in rs):+.1f}% to "
            f"{max(r['r2'] for r in rs):+.1f}% | {sum(r['r2'] >= r['hu2'] for r in rs)} | {sum(r['x2'] > 0 for r in rs)} | "
            f"{statistics.median_high([r['avg'] for r in rs]):+.1f}% | {sum(r['hit'] for r in rs)} |")


for yr in sys.argv[1].split(","):
    rs = [r for r in rows if r["date"].startswith(yr)]
    print(f"\n## {yr} ({len(rs)} dates)\n")
    print("| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |")
    print("|---|---|---|---|---|---|---|---|")
    for key, lab in (("cls", "class"), ("fy", "current year"), ("lq", "latest print")):
        groups = {}
        for r in rs:
            k = f"class {r['cls']}, legacy tier {r['tier']}" if key == "cls" else (r[key] if key == "fy" else f"latest print {r[key]}")
            groups.setdefault(k, []).append(r)
        for k, g in groups.items():
            print(line(k, g))
    if not rs:
        continue
    r3s = [r for r in rs if r["r3"] is not None]
    print(f"3y ({len(r3s)} dates with one): {sum(r['r3'] >= r['hu3'] for r in rs if r['r3'] is not None)} of {len(rs)} cleared, "
          f"{sum(r['x3'] > 0 for r in rs if r['x3'] is not None)} beat SPY; range {min(r['r3'] for r in r3s):+.1f}% to {max(r['r3'] for r in r3s):+.1f}%" if r3s else "3y: none yet")
    print("1y range", min(r["r1"] for r in rs), max(r["r1"] for r in rs), "excess 2y", min(r["x2"] for r in rs), max(r["x2"] for r in rs))
    print("drawdown", min(r["dd"] for r in rs), max(r["dd"] for r in rs))
lands = {}
for r in rows:
    lands[r["land"]] = lands.get(r["land"], 0) + 1
print("landing", lands)
print("drift", {json.dumps(r["drift"], sort_keys=True)[:160] for r in rows})
for r in rows:
    print(r["date"], r["price"], r["fy"], r["lq"], r["r2"], r["x2"], r["hu2"], r["r3"], r["avg"], r["dd"], r["hit"], r["land"])
print("no 2-year horizon yet:", len(pending), pending[:1], pending[-1:])
