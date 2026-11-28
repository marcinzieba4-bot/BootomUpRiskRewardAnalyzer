#!/usr/bin/env python3
"""Controls for the OKE series (in memory; nothing on disk changes): alter one value of each dated fact, rebuild every weekly date
of the range, and require that no model dated before the fact's publication changes; report whether the first weekly date on or
after it changes (a fact that changes nothing is 'inert').

    python3 retro/generators/oke/controls_oke_1417.py [--from 2010-01-01] [--to 2013-12-31] [--start 2010-01-01] [--end 2013-12-31]

The generic retro/tools/controls.py alters a print's eps_q alone, which build_oke.py's check that every print matches its raw
figures refuses; here each print's revenues are raised 10% with every derived field re-derived, each vintage's last-year EPS and
revenue are raised, each EPS guide's range is raised by $0.10 (a net income range, from 2010, by $20 million), each dividend is set to
$0.99 a quarter and the split's ratio is set to 3 (OKE 2010-2013; a guide in words has no figure to alter and is reported inert).
OKE 2014-2017 adds: a point net income guide is raised by $20 million, a pro forma guide (text only) by $20 million, a print whose
net margin is revenues less cost of sales and fuel keeps its cost (net margin re-derived), and the ONE Gas distribution's factor is set
to 1.5 (which the builder must refuse against Yahoo's from its effective date).
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
ap.add_argument("--from", dest="frm", default="2013-12-01")
ap.add_argument("--to", default="2017-12-31")
ap.add_argument("--start", default="2014-01-01")
ap.add_argument("--end", default="2017-12-31")
a = ap.parse_args()
facts0 = json.load(open(B.FACTS, encoding="utf-8"))
engine = open(B.ENGINE, encoding="utf-8").read()
raw, spx = B.load_series(B.SYMBOL), B.load_series("^GSPC")
dates = B.weekly_dates(a.start, a.end, sorted(raw), facts0["prints"])
tmp = tempfile.mkdtemp()


def build_all(f):
    out = os.path.join(tmp, "m")
    with contextlib.redirect_stdout(io.StringIO()):
        res = {}
        for d in dates:
            try:
                B.build(d, f, raw, spx, engine, out)
                res[d] = open(os.path.join(out, d, "model.py"), encoding="utf-8").read()
            except (AssertionError, SystemExit) as e:
                res[d] = f"REFUSED: {e}"
    shutil.rmtree(out, ignore_errors=True)
    return res


def bump_print(p):
    r = p["raw"]
    r["rev_m"] = round(r["rev_m"] * 1.1, 6)
    g = lambda x, y: round((y / x - 1) * 100 + 0.0, 1) if x > 0 else round((y - x) / abs(x) * 100 + 0.0, 1)
    mg = lambda x, rev: round(x / rev * 100 + 0.0, 2)
    if "cost_m" in r:          # (OKE 2014-2017) net margin is revenues less cost of sales and fuel: re-derived
        r["nm_m"] = r["rev_m"] - r["cost_m"]
        p.update(nm_pct=g(r["nm_prior_m"], r["nm_m"]))
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
def bump_guide(g):
    if "eps_guide" in g:
        g["eps_guide"] = [x + 0.10 for x in g["eps_guide"]]
    elif "ni_guide_m" in g:
        g["ni_guide_m"] = [x + 20 for x in g["ni_guide_m"]]
    elif "pro_forma_ni_m" in g:                  # (OKE 2014-2017) text only
        g["pro_forma_ni_m"] = [x + 20 for x in g["pro_forma_ni_m"]]
    else:                                        # words: no figure; alter the quoted text instead
        g["quote"] += " PLANTED"


for i, g in enumerate(facts0["eps_guides"]):
    if inside(g):
        cs.append((f"FY{g['fy']} EPS guide of {g['published']} ({g['doc']}), {'+$0.10' if 'eps_guide' in g else '+$20M' if 'ni_guide_m' in g or 'pro_forma_ni_m' in g else 'words'}",
                   g["published"], lambda f, i=i: bump_guide(f["eps_guides"][i])))
for i, s in enumerate(facts0.get("splits", [])):
    if a.frm <= s["effective"] <= a.to:
        cs.append((f"split of {s['effective']}, ratio 3 (the builder must refuse it against Yahoo's)", s["effective"],
                   lambda f, i=i: f["splits"][i].update(ratio=3.0)))
for i, x in enumerate(facts0.get("distributions", [])):
    if a.frm <= x["effective"] <= a.to:
        cs.append((f"distribution of {x['effective']}, factor 1.5 (the builder must refuse it against Yahoo's)", x["effective"],
                   lambda f, i=i: f["distributions"][i].update(yahoo_factor=1.5)))
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
