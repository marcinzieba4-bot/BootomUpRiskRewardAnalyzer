#!/usr/bin/env python3
"""FANG model controls (retro/README.md, "FANG 2014-2017"): alter one value of each dated fact a model reads and check that no model dated
before its publication changes, and that the first weekly date on or after it does. In memory and a temporary folder; nothing in the
repository changes. (The gate's own controls, 2008-2013, are controls_fang.py.)

    python3 retro/generators/fang/controls_fang_models.py [START END]     # default 2014-02-17 2017-12-31

build_fang.py's check_print re-derives every rate from a print's raw figures, so a print's control raises its oil-equivalent production
by 10 MBOE and re-derives the growth (a Q4 print: also its full-year EPS); a vintage's control raises its last year's revenues and its
last kept year's EPS; the 10-K words (the business, cyclical, prices and climate legislation sentences) and the no-dividend statement
are altered as they stand. A fact published before the first built date (the Q3 2013 print, the FY2013 10-K) reaches the first date or
no date.
"""
import contextlib
import copy
import io
import json
import os
import shutil
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO, "retro"))
import build_fang as B  # noqa: E402
from build_acn import load_series, weekly_dates  # noqa: E402

START, END = sys.argv[1:3] if len(sys.argv) > 2 else ("2014-02-17", "2017-12-31")
facts0 = json.load(open(B.FACTS, encoding="utf-8"))
engine = open(B.ENGINE, encoding="utf-8").read()
raw, spx = load_series("FANG"), load_series("^GSPC")
dates = weekly_dates(START, END, sorted(spx), facts0["prints"])
tmp = tempfile.mkdtemp()


def build_all(facts, upto="9999"):
    out = os.path.join(tmp, "m")
    res = {}
    with contextlib.redirect_stdout(io.StringIO()):
        for d in dates:
            if d > upto:
                break
            B.build(d, facts, raw, spx, engine, out)
            res[d] = open(os.path.join(out, d, "model.py"), encoding="utf-8").read()
    shutil.rmtree(out, ignore_errors=True)
    return res


def prod(f, i):
    p = f["prints"][i]
    p["raw"]["boe_k"] += 10.0
    p["production_pct"] = round(round((p["raw"]["boe_k"] / p["raw"]["boe_prior_k"] - 1) * 100, 2), 1)
    if p.get("fy_actual"):
        p["fy_actual"]["eps_gaap"] = round(p["fy_actual"]["eps_gaap"] + 0.01, 2)
        p["fy_actual"]["one_off_test"]["eps_gaap"] = p["fy_actual"]["eps_gaap"]


C = []
for i, p in enumerate(facts0["prints"]):
    C.append((f"{p['quarter']} print, its production" + (" and full-year EPS" if p.get("fy_actual") else ""), p["published"],
              lambda f, i=i: prod(f, i)))
for i, v in enumerate(facts0["history_vintages"]):
    if "eps_normalized" not in v:
        continue
    y = max(v["revenue_usd_b"])
    k = max(v["eps_normalized"])
    C.append((f"{v['fy_label']} vintage, its {y} revenues", v["published"],
              lambda f, i=i, y=y: f["history_vintages"][i]["revenue_usd_b"].update({y: f["history_vintages"][i]["revenue_usd_b"][y] + 0.05})))
    C.append((f"{v['fy_label']} vintage, its {k} EPS", v["published"],
              lambda f, i=i, k=k: f["history_vintages"][i]["eps_normalized"].update({k: f["history_vintages"][i]["eps_normalized"][k] + 0.01})))
    for q in ("business_quote", "cyclical_quote", "transition_quote", "no_dividend_quote"):
        C.append((f"{v['fy_label']} vintage, its {q}", v["published"],
                  lambda f, i=i, q=q: f["history_vintages"][i].update({q: f["history_vintages"][i][q] + " CTRL"})))
base = build_all(facts0)
bad = first_hit = inert = 0
for name, pub, fn in C:
    f = copy.deepcopy(facts0)
    fn(f)
    first = min((d for d in dates if d >= pub), default=None)
    r = build_all(f)
    changed = [d for d in r if r[d] != base[d]]
    early = [d for d in changed if d < pub]
    bad += bool(early)
    if first in changed:
        first_hit += 1
    elif not changed:
        inert += 1
    print(f"{'FAIL' if early else 'ok  '} {name} (published {pub}): {len(changed)} dates change"
          + (f", the first date on or after it, {first}, among them" if first in changed else f"; the first date on or after it ({first}) does not")
          + (f"; EARLY {early}" if early else ""), flush=True)
print(f"{len(C)} controls: {len(C) - bad} change no earlier model; {first_hit} change the first weekly date on or after publication, "
      f"{inert} change none")
shutil.rmtree(tmp)
sys.exit(1 if bad else 0)
