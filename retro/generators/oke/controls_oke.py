#!/usr/bin/env python3
"""Controls for the OKE series (in memory; nothing on disk changes): alter one value of each dated fact, rebuild every weekly date
of the range, and require that no model dated before the fact's publication changes; report whether the first weekly date on or
after it changes (a fact that changes nothing is 'inert').

    python3 retro/generators/oke/controls_oke.py [--from 2007-06-01] [--to 2009-12-31] [--start 2008-01-01] [--end 2009-12-31]

The generic retro/tools/controls.py alters a print's eps_q alone, which build_oke.py's check that every print matches its raw
figures refuses; here each print's revenues are raised 10% with every derived field re-derived, each vintage's last-year EPS and
revenue are raised, each EPS guide's range is raised by $0.10 and each dividend is set to $0.99 a quarter.
"""
import argparse
import contextlib
import copy
import io
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RETRO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, RETRO)
import build_oke as B  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--from", dest="frm", default="2007-06-01")
ap.add_argument("--to", default="2009-12-31")
ap.add_argument("--start", default="2008-01-01")
ap.add_argument("--end", default="2009-12-31")
a = ap.parse_args()
facts0 = json.load(open(B.FACTS, encoding="utf-8"))
engine = open(B.ENGINE, encoding="utf-8").read()
raw, spx = B.load_series(B.SYMBOL), B.load_series("^GSPC")
dates = B.weekly_dates(a.start, a.end, sorted(raw), facts0["prints"])
tmp = tempfile.mkdtemp()


def build_all(f):
    out = os.path.join(tmp, "m")
    with contextlib.redirect_stdout(io.StringIO()):
        for d in dates:
            B.build(d, f, raw, spx, engine, out)
    res = {d: open(os.path.join(out, d, "model.py"), encoding="utf-8").read() for d in dates}
    shutil.rmtree(out)
    return res


def bump_print(p):
    r = p["raw"]
    r["rev_m"] = round(r["rev_m"] * 1.1, 6)
    g = lambda x, y: round((y / x - 1) * 100 + 0.0, 1) if x > 0 else round((y - x) / abs(x) * 100 + 0.0, 1)
    mg = lambda x, rev: round(x / rev * 100 + 0.0, 2)
    p.update(sales_b=round(r["rev_m"] / 1000, 3), sales_pct=g(r["rev_prior_m"], r["rev_m"]), opm=mg(r["oi_m"], r["rev_m"]),
             opm_bp=round((mg(r["oi_m"], r["rev_m"]) - mg(r["oi_prior_m"], r["rev_prior_m"])) * 100, 1), ptm=mg(r["pti_m"], r["rev_m"]),
             ptm_bp=round((mg(r["pti_m"], r["rev_m"]) - mg(r["pti_prior_m"], r["rev_prior_m"])) * 100, 1))


inside = lambda x: a.frm <= x["published"] <= a.to
cs = []
for i, p in enumerate(facts0["prints"]):
    if inside(p):
        cs.append((f"{p['quarter']} print, revenues +10%", p["published"], lambda f, i=i: bump_print(f["prints"][i])))
for i, v in enumerate(facts0["history_vintages"]):
    if inside(v):
        y = max(v["eps_normalized"])
        cs.append((f"{v['fy_label']} vintage, its {y} EPS +0.01 and revenue +0.5", v["published"],
                   lambda f, i=i, y=y: (f["history_vintages"][i]["eps_normalized"].update({y: f["history_vintages"][i]["eps_normalized"][y] + 0.01}),
                                        f["history_vintages"][i]["revenue_usd_b"].update({y: f["history_vintages"][i]["revenue_usd_b"][y] + 0.5}))))
for i, g in enumerate(facts0["eps_guides"]):
    if inside(g):
        cs.append((f"FY{g['fy']} EPS guide of {g['published']} ({g['doc']}), +$0.10", g["published"],
                   lambda f, i=i: f["eps_guides"][i].update(eps_guide=[x + 0.10 for x in f["eps_guides"][i]["eps_guide"]])))
for i, d in enumerate(facts0["dividends"]):
    if inside(d):
        cs.append((f"dividend of {d['published']}, $0.99 a quarter", d["published"], lambda f, i=i: f["dividends"][i].update(quarterly=0.99)))
try:
    base = build_all(facts0)
    bad = live = 0
    for name, pub, fn in cs:
        f = copy.deepcopy(facts0)
        fn(f)
        r = build_all(f)
        ch = [d for d in dates if r[d] != base[d]]
        early = [d for d in ch if d < pub]
        first = min((d for d in dates if d >= pub), default=None)
        bad += bool(early)
        live += bool(ch)
        print(f"{name} (published {pub}): {len(ch)} dates change, first {ch[0] if ch else '-'}, last {ch[-1] if ch else '-'}; "
              f"before publication {len(early)}; first weekly date on/after it {first} {'changes' if first in ch else 'unchanged'}",
              flush=True)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
print(f"OKE {len(dates)} dates, {len(cs)} controls: {live} change dates on or after their publication, {len(cs) - live} inert, "
      f"{bad} change an earlier date")
sys.exit(1 if bad else 0)
