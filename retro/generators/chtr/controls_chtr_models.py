#!/usr/bin/env python3
"""CHTR model controls (retro/README.md, "CHTR 2018-2021"): alter one value of each dated fact a model reads and check that no model dated
before its publication changes, and that the first weekly date on or after it does. In memory and a temporary folder; nothing in the
repository changes. (The gate's own controls, 2008-2021, are controls_chtr.py.)

    python3 retro/generators/chtr/controls_chtr_models.py

build_chtr.py's check_print re-derives every rate from a print's raw figures, so a print's control raises its total customer
relationships by 100K and re-derives the growth; a vintage's control raises its last year's revenues and its Item 1 relationships growth;
the streaming words, the no-dividend statement and the listing are altered as they stand. A fact published before the first built date
(the Q3 2018 print, the FY2018 10-K's companions of the same morning excepted) reaches the first date or no date.
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
import build_chtr as B  # noqa: E402
from build_acn import load_series, weekly_dates  # noqa: E402

START, END = "2019-01-28", "2021-12-31"
facts0 = json.load(open(B.FACTS, encoding="utf-8"))
engine = open(B.ENGINE, encoding="utf-8").read()
raw, spx = load_series("CHTR"), load_series("^GSPC")
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


def rel(f, i):
    p = f["prints"][i]
    p["raw"]["rel_k"] += 100.0
    p["rel_pct"] = round((p["raw"]["rel_k"] / p["raw"]["rel_prior_k"] - 1) * 100, 2)


C = []
for i, p in enumerate(facts0["prints"]):
    C.append((f"{p['quarter']} print, its customer relationships", p["published"], lambda f, i=i: rel(f, i)))
for i, v in enumerate(facts0["history_vintages"]):
    if "model" not in v:
        continue
    y = max(v["periods"])
    C.append((f"{v['fy_label']} vintage, its {y} revenues", v["published"],
              lambda f, i=i, y=y: f["history_vintages"][i]["periods"][y].update(revenue_m=f["history_vintages"][i]["periods"][y]["revenue_m"] + 500)))
    C.append((f"{v['fy_label']} vintage, its relationships growth", v["published"],
              lambda f, i=i: f["history_vintages"][i]["model"].update(rel_pct=f["history_vintages"][i]["model"]["rel_pct"] + 1.0)))
for i, e in enumerate(facts0["events"]):
    C.append((f"{e['doc']} streaming words", e["published"],
              lambda f, i=i: f["events"][i].update(risk_quote=f["events"][i]["risk_quote"] + " CTRL")))
for i, x in enumerate(facts0["no_dividend"]):
    C.append((f"no-dividend statement of {x['published']} ({x['source']})", x["published"],
              lambda f, i=i: f["no_dividend"][i].update(quote=f["no_dividend"][i]["quote"] + " CTRL")))
for i, x in enumerate(facts0["listings"]):
    C.append((f"listing of {x['published']} ({x['source']})", x["published"],
              lambda f, i=i: f["listings"][i].update(symbol="CTRL")))
base = build_all(facts0)
bad = first_hit = inert = 0
for name, pub, fn in C:
    f = copy.deepcopy(facts0)
    fn(f)
    first = min((d for d in dates if d >= pub), default=None)
    r = build_all(f, upto=first or "9999")
    changed = [d for d in r if r[d] != base[d]]
    early = [d for d in changed if d < pub]
    bad += bool(early)
    if changed and changed[-1] == first:
        first_hit += 1
    elif not changed:
        inert += 1
    print(f"{'FAIL' if early else 'ok  '} {name} (published {pub}): "
          + (f"the first date on or after it, {first}, changes" if first in changed else f"the first date on or after it ({first}) does not change")
          + (f"; EARLY {early}" if early else ""))
print(f"{len(C)} controls: {len(C) - bad} change no earlier model; {first_hit} change the first weekly date on or after publication, "
      f"{inert} change none")
shutil.rmtree(tmp)
sys.exit(1 if bad else 0)
