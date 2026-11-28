#!/usr/bin/env python3
"""NEE 2014-2017 controls (retro/README.md, "NEE 2014-2017"): alter one value of each fact published in the range and check that no
model dated before its publication changes, and whether the first weekly date on or after it does. In memory; nothing on disk changes.

    python3 retro/generators/nee/controls_nee_1417.py

The generic retro/tools/controls.py alters a print's EPS alone, which build_nee.py's check_print refuses (every rate is re-derived from
the raw figures), so a print's control alters its energy sales and re-derives the rate, as the 2008-2013 controls did; a Q4 print's
full-year revenue, a vintage's last-year revenue and a guide's quoted text are altered as they stand.
"""
import contextlib, copy, io, json, os, shutil, sys, tempfile
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO, "retro"))
import build_nee as B  # noqa: E402
from build_acn import load_series, weekly_dates  # noqa: E402

START, END = "2014-01-06", "2017-12-31"
facts0 = json.load(open(B.FACTS, encoding="utf-8"))
engine = open(B.ENGINE, encoding="utf-8").read()
raw, spx = load_series("NEE"), load_series("^GSPC")
dates = weekly_dates(START, END, sorted(raw), facts0["prints"])
tmp = tempfile.mkdtemp()


def build_all(facts):
    out = os.path.join(tmp, "m")
    with contextlib.redirect_stdout(io.StringIO()):
        for d in dates:
            B.build(d, facts, raw, spx, engine, out)
    res = {d: open(os.path.join(out, d, "model.py"), encoding="utf-8").read() for d in dates}
    shutil.rmtree(out)
    return res


def kwh(f, i):
    p = f["prints"][i]
    p["raw"]["kwh_m"] += 1000.0
    p["kwh_pct"] = round((p["raw"]["kwh_m"] / p["raw"]["kwh_prior_m"] - 1) * 100, 1)


C = []
inside = lambda x: START <= x["published"] <= END   # noqa: E731
for i, p in enumerate(facts0["prints"]):
    if inside(p):
        C.append((f"{p['quarter']} print, its energy sales", p["published"], lambda f, i=i: kwh(f, i)))
        if p.get("fy_actual"):
            C.append((f"{p['quarter']} full-year revenue", p["published"],
                      lambda f, i=i: f["prints"][i]["fy_actual"].update(revenue_usd_b=f["prints"][i]["fy_actual"]["revenue_usd_b"] + 0.5)))
for i, v in enumerate(facts0["history_vintages"]):
    if inside(v):
        y = max(v["revenue_usd_b"])
        C.append((f"{v['fy_label']} vintage, its {y} revenue", v["published"],
                  lambda f, i=i, y=y: f["history_vintages"][i]["revenue_usd_b"].update({y: f["history_vintages"][i]["revenue_usd_b"][y] + 0.5})))
for i, g in enumerate(facts0["guides"]):
    if inside(g):
        C.append((f"FY{g['fy']} guide of {g['published']} ({g['doc']})", g["published"],
                  lambda f, i=i: f["guides"][i].update(display=f["guides"][i]["display"] + " CTRL")))
base = build_all(facts0)
bad = 0
first_hit = inert = 0
for name, pub, fn in C:
    f = copy.deepcopy(facts0)
    fn(f)
    r = build_all(f)
    changed = [d for d in dates if r[d] != base[d]]
    early = [d for d in changed if d < pub]
    first = min((d for d in dates if d >= pub), default=None)
    bad += bool(early)
    if changed and changed[0] == first:
        first_hit += 1
    elif not changed:
        inert += 1
    print(f"{'FAIL' if early else 'ok  '} {name}: {len(changed)} dates changed"
          + (f", {changed[0]} .. {changed[-1]}" if changed else " (inert)") + (f"; EARLY {early}" if early else "")
          + ("" if not changed or changed[0] == first else f"; first change {changed[0]}, first date on or after {first}"))
print(f"{len(C)} controls: {len(C) - bad} change no earlier model; {first_hit} change the first weekly date on or after "
      f"publication, {inert} inert")
shutil.rmtree(tmp)
sys.exit(1 if bad else 0)
