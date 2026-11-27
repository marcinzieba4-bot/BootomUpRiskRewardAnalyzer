#!/usr/bin/env python3
"""Controls for the CHTR gate (no date is built, so controls.py's model rebuild does not apply; retro/README.md, "CHTR 2014-2017").

For each dated fact that decides the gate (each 10-K vintage, each Q4 release's full year, the FY2016 one-off test), alter it in
memory so that its year would anchor a P/E (the vintage's or release's latest year set to $9.99 of positive EPS; the one-off test
marked not distorted), refuse every weekly date of 2008-2017 again, and require that the refusals change on exactly the weekly
dates from the fact's publication until a later fact supersedes it (or, for a year of the Predecessor, until the 2009-11-30
emergence, after which it is not a year of the priced shares), and on no date before. Nothing on disk changes.

    python3 retro/generators/chtr/controls_chtr.py [START END]      # default 2008-01-01 2017-12-31
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RETRO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, RETRO)
import build_chtr  # noqa: E402

start, end = (sys.argv[1:3] if len(sys.argv) > 2 else ("2008-01-01", "2017-12-31"))
with open(build_chtr.FACTS, encoding="utf-8") as fh:
    f0 = json.load(fh)
chtr, spx = build_chtr.trading_days("CHTR"), build_chtr.trading_days("^GSPC")
dates = build_chtr.weekly_dates(start, end, spx)
g = lambda d, f: build_chtr.gate(d, f, {k: c for k, c in chtr.items() if k <= d})
base = {d: g(d, f0) for d in dates}
vint = sorted(f0["history_vintages"], key=lambda v: v["published"])
nxt_v = lambda day: min([v["published"] for v in vint if v["published"] > day] + ["9999-12-31"])

controls = []
for i, v in enumerate(vint):
    def alter(f, i=i):
        vv = sorted(f["history_vintages"], key=lambda v: v["published"])[i]
        twelve = [k for k, p in vv["periods"].items() if p["months"] == 12]
        y = max(twelve, key=lambda k: vv["periods"][k]["end"])
        vv["periods"][y]["eps_diluted"] = 9.99
        vv.get("one_off_tests", {}).pop(y, None)
    # a year of the issuer that is not the priced shares' after the emergence (the Predecessor's) counts only until it
    twelve = [k for k, p in v["periods"].items() if p["months"] == 12]
    y = max(twelve, key=lambda k: v["periods"][k]["end"])
    until = nxt_v(v["published"])
    if v["periods"][y]["issuer"] not in v.get("priced_issuers", ["Successor"]):
        until = min(until, build_chtr.EMERGENCE)
    controls.append((f"vintage {v['source']} ({v['fy_label']}, FY{y} {v['periods'][y]['issuer'].split(',')[0]})", v["published"],
                     until, alter))
for j, a in enumerate(f0.get("q4_actuals", [])):
    def alter(f, j=j):
        f["q4_actuals"][j]["period"]["eps_diluted"] = 9.99
        f["q4_actuals"][j].pop("one_off_test", None)
    # a release's year counts from its date until the 10-K that reports the year (the same morning for Q4 2016: inert)
    ends = min(v["published"] for v in vint if str(a["fy"]) in v["periods"])
    controls.append((f"Q4 {a['fy']} release {a['source']}", a["published"], ends, alter))
for v in vint:
    for y in v.get("one_off_tests", {}):
        def alter(f, src=v["source"], y=y):
            next(x for x in f["history_vintages"] if x["source"] == src)["one_off_tests"][y]["distorted"] = False
        controls.append((f"one-off test FY{y} in {v['source']}", v["published"], nxt_v(v["published"]), alter))

bad = 0
for name, pub, until, alter in controls:
    f1 = copy.deepcopy(f0)
    alter(f1)
    changed = [d for d in dates if g(d, f1) != base[d]]
    want = [d for d in dates if pub <= d < until]
    early = [d for d in changed if d < pub]
    passing = [d for d in changed if not g(d, f1)]
    ok = changed == want and not early
    bad += not ok
    span = f"{changed[0]}..{changed[-1]}" if changed else "none"
    print(f"{'ok ' if ok else 'BAD'} {name:<48} published {pub}: {len(changed):>3} dates change ({span}), {len(want)} expected, "
          f"{len(early)} before publication, {len(passing)} would pass the gate")
print(f"{len(controls) - bad} of {len(controls)} controls behave")
sys.exit(1 if bad else 0)
