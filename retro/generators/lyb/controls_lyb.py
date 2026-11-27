#!/usr/bin/env python3
"""LYB controls (retro/README.md, "LYB"): alter one value of each dated fact and check that no model dated before its publication
changes, and whether the first weekly date on or after it does. In memory; nothing on disk changes.

    python3 retro/generators/lyb/controls_lyb.py                          # the 2012-2013 dates
    python3 retro/generators/lyb/controls_lyb.py 2014-01-01 2017-12-31    # the 2014-2017 dates (retro/README.md, "LYB 2014-2017")

build_lyb.py's check_print re-derives every rate from a print's raw figures, so a print's control alters its O&P-Americas operating
income and re-derives the rate; a Q4 print's full-year revenue, a vintage's last-year revenue, the restatement's EPS, each dividend and
the repurchase program's text are altered as they stand. A fact published before the first date reaches the first date or no date.
"""
import contextlib, copy, io, json, os, shutil, sys, tempfile
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO, "retro"))
import build_lyb as B  # noqa: E402
from build_acn import load_series, weekly_dates  # noqa: E402

START, END = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("2012-02-06", "2013-12-31")
facts0 = json.load(open(B.FACTS, encoding="utf-8"))
engine = open(B.ENGINE, encoding="utf-8").read()
raw, spx = load_series("LYB"), load_series("^GSPC")
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


def opa(f, i):
    p = f["prints"][i]
    p["raw"]["opa_m"] += 100.0
    r = p["raw"]
    a, b = r["opa_prior_m"], r["opa_m"]
    p["opa_pct"] = round((b / a - 1) * 100, 1) if a > 0 else round((b - a) / abs(a) * 100, 1)


C = []
for i, p in enumerate(facts0["prints"]):
    C.append((f"{p['quarter']} print, its O&P-Americas operating income", p["published"], lambda f, i=i: opa(f, i)))
    if p.get("fy_actual"):
        C.append((f"{p['quarter']} full-year revenue", p["published"],
                  lambda f, i=i: f["prints"][i]["fy_actual"].update(revenue_usd_b=f["prints"][i]["fy_actual"]["revenue_usd_b"] + 0.5)))
    for y in p.get("restates", {}):
        C.append((f"{p['quarter']} restatement of FY{y}, its EPS", p["published"],
                  lambda f, i=i, y=y: f["prints"][i]["restates"][y].update(eps_normalized=f["prints"][i]["restates"][y]["eps_normalized"] + 0.01)))
for i, v in enumerate(facts0["history_vintages"]):
    y = max(v["revenue_usd_b"])
    C.append((f"{v['fy_label']} vintage, its {y} revenue", v["published"],
              lambda f, i=i, y=y: f["history_vintages"][i]["revenue_usd_b"].update({y: f["history_vintages"][i]["revenue_usd_b"][y] + 0.5})))
    if v.get("refining_quote"):              # the watch list's 10-K words (from ENERGY_TRANSITION's live date, 2015-12-12)
        C.append((f"{v['fy_label']} vintage, its refining sentence", v["published"],
                  lambda f, i=i: f["history_vintages"][i].update(refining_quote=f["history_vintages"][i]["refining_quote"] + " CTRL")))
for i, d in enumerate(facts0["dividends"]):
    C.append((f"dividend of {d['published']} ({d['source']})", d["published"],
              lambda f, i=i: f["dividends"][i].update(quarterly=f["dividends"][i]["quarterly"] + 0.01)))
for i, b in enumerate(facts0["buyback_programs"]):
    C.append((f"repurchase program of {b['published']}", b["published"],
              lambda f, i=i: f["buyback_programs"][i].update(text=f["buyback_programs"][i]["text"] + " CTRL")))
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
