#!/usr/bin/env python3
"""TRGP controls (retro/README.md, "TRGP"): alter one value of each dated fact and check that no model dated before its publication
changes, and whether the first weekly date on or after it does. In memory; nothing on disk changes.

    python3 retro/generators/trgp/controls_trgp.py                        # the 2012-2013 dates

build_trgp.py's check_print re-derives every rate from a print's raw figures, so a print's control alters its Gathering and Processing
operating margin and re-derives the rate; a Q4 print's full-year revenue, a vintage's last-year revenue, each dividend and each outlook's
display are altered as they stand. A fact published before the first date reaches the first date or no date.
"""
import contextlib, copy, io, json, os, shutil, sys, tempfile
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO, "retro"))
import build_trgp as B  # noqa: E402
from build_acn import load_series, weekly_dates  # noqa: E402

START, END = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("2012-02-20", "2013-12-31")
facts0 = json.load(open(B.FACTS, encoding="utf-8"))
engine = open(B.ENGINE, encoding="utf-8").read()
raw, spx = load_series("TRGP"), load_series("^GSPC")
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


def gp(f, i):
    p = f["prints"][i]
    p["raw"]["gp_m"] += 50.0
    r = p["raw"]
    a, b = r["gp_prior_m"], r["gp_m"]
    p["gp_pct"] = round((b / a - 1) * 100, 1) if a > 0 else round((b - a) / abs(a) * 100, 1)


C = []
for i, p in enumerate(facts0["prints"]):
    C.append((f"{p['quarter']} print, its Gathering and Processing operating margin", p["published"], lambda f, i=i: gp(f, i)))
    if p.get("fy_actual"):
        C.append((f"{p['quarter']} full-year revenue", p["published"],
                  lambda f, i=i: f["prints"][i]["fy_actual"].update(revenue_usd_b=f["prints"][i]["fy_actual"]["revenue_usd_b"] + 0.5)))
for i, v in enumerate(facts0["history_vintages"]):
    y = max(v["revenue_usd_b"])
    C.append((f"{v['fy_label']} vintage, its {y} revenue", v["published"],
              lambda f, i=i, y=y: f["history_vintages"][i]["revenue_usd_b"].update({y: f["history_vintages"][i]["revenue_usd_b"][y] + 0.5})))
for i, d in enumerate(facts0["dividends"]):
    C.append((f"dividend of {d['published']} ({d['source']})", d["published"],
              lambda f, i=i: f["dividends"][i].update(quarterly=f["dividends"][i]["quarterly"] + 0.01)))
for i, g in enumerate(facts0["guides"]):
    C.append((f"FY{g['fy']} outlook of {g['published']} ({g['source']}), its display", g["published"],
              lambda f, i=i: f["guides"][i].update(display=f["guides"][i]["display"] + " CTRL")))
base = build_all(facts0)
bad = first_hit = inert = 0
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
