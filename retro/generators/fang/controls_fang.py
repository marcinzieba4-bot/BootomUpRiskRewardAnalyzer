#!/usr/bin/env python3
"""Controls for the FANG gate (no date is built, so controls.py's model rebuild does not apply; retro/README.md, "FANG 2008-2009").

For each history vintage that decides the gate (the S-1/A No. 6, the 424B4 prospectus, the FY2012 10-K), alter it in memory so that
its latest full year would anchor a P/E (that year's GAAP EPS set to $9.99), refuse every weekly date of 2008-2013 again, and require
that the refusals change on exactly the weekly dates from the vintage's publication until a later vintage supersedes it, and on no
date before; the dates that would pass are those with a FANG close (from 2012-10-12). A last control sets the series start a year
earlier in memory and requires that only the price reason of the dates in that year changes. Nothing on disk changes.

    python3 retro/generators/fang/controls_fang.py [START END]      # default 2008-01-01 2013-12-31; 2014-2017: 2008-01-01 2017-12-31

A vintage that already anchors a P/E (the FY2013-FY2016 10-Ks) is controlled the other way: every year set to a loss, and the dates
from its publication to the next vintage must become refused (the CHTR 2014-2017 extension).
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RETRO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, RETRO)
import build_fang  # noqa: E402

start, end = (sys.argv[1:3] if len(sys.argv) > 2 else ("2008-01-01", "2013-12-31"))
with open(build_fang.FACTS, encoding="utf-8") as fh:
    f0 = json.load(fh)
fang, spx = build_fang.trading_days("FANG"), build_fang.trading_days("^GSPC")
dates = build_fang.weekly_dates(start, end, spx)
g = lambda d, f, px=fang: build_fang.gate(d, f, {k: c for k, c in px.items() if k <= d})
base = {d: g(d, f0) for d in dates}
vint = sorted(f0["history_vintages"], key=lambda v: v["published"])
nxt_v = lambda day: min([v["published"] for v in vint if v["published"] > day] + ["9999-12-31"])

bad = 0
for i, v in enumerate(vint):
    f1 = copy.deepcopy(f0)
    vv = sorted(f1["history_vintages"], key=lambda v: v["published"])[i]
    y = max((k for k, p in vv["periods"].items() if p["months"] == 12), key=lambda k: vv["periods"][k]["end"])
    # (2014-2017, retro/README.md, "FANG 2014-2017") a vintage that already anchors (a positive GAAP year) gets every year a loss,
    # so its dates must become refused; one that does not gets its latest year a positive EPS, so its dates must pass
    anchors = any(p["months"] == 12 and (p["eps_diluted"] or 0) > 0 for p in vv["periods"].values())
    if anchors:
        for p in vv["periods"].values():
            p["eps_diluted"] = -9.99 if p["eps_diluted"] is not None else None
    else:
        vv["periods"][y]["eps_diluted"] = 9.99
    changed = [d for d in dates if g(d, f1) != base[d]]
    want = [d for d in dates if v["published"] <= d < nxt_v(v["published"])]
    early = [d for d in changed if d < v["published"]]
    passing = [d for d in changed if not g(d, f1)]
    ok = changed == want and not early and passing == ([] if anchors else [d for d in want if d in fang])
    bad += not ok
    span = f"{changed[0]}..{changed[-1]}" if changed else "none"
    print(f"{'ok ' if ok else 'BAD'} vintage {v['source']} ({v['fy_label']}, FY{y}{', every year a loss' if anchors else ''}) published "
          f"{v['published']}: {len(changed):>3} dates change ({span}), {len(want)} expected, {len(early)} before publication, "
          f"{len(passing)} would pass the gate")

# the price reason: a FANG close a year before the series start removes only that year's price reason (every date stays refused)
px = dict(fang)
early_days = [d for d in spx if "2011-10-12" <= d < f0["series_start"]]
px.update({d: 1.0 for d in early_days})
f1 = copy.deepcopy(f0)
f1["series_start"] = early_days[0]
has_px = lambda why: any(w.startswith("no FANG close") for w in why)       # the reason's text names the series start, so compare its presence
changed = [d for d in dates if has_px(g(d, f1, px)) != has_px(base[d]) or [w for w in g(d, f1, px) if not w.startswith("no FANG close")]
           != [w for w in base[d] if not w.startswith("no FANG close")]]
want = [d for d in dates if early_days[0] <= d < f0["series_start"]]
ok = changed == want and all(g(d, f1, px) for d in changed)
bad += not ok
print(f"{'ok ' if ok else 'BAD'} series start moved to {early_days[0]}: {len(changed)} dates change, {len(want)} expected, "
      "every one still refused (no vintage anchors)")
print(f"{len(vint) + 1 - bad} of {len(vint) + 1} controls behave")
sys.exit(1 if bad else 0)
