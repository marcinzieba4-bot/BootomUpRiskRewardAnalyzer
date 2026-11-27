#!/usr/bin/env python3
"""
Controls: alter one value of each dated fact, rebuild every weekly date in memory, and require that no model dated before the
fact's publication changes. The rebuilt models are compared with a baseline built the same way (nothing on disk changes).

    python3 retro/tools/controls.py SCHW 2010-01-01 2013-12-31 [--only prints,history_vintages]

Each fact published from START to END gets one control:
  - a print: its quarter EPS (eps_q) +0.01, and for a Q4 print its full-year revenue (fy_actual.revenue_usd_b) +0.5;
  - a restatement inside a print ('restated'): its eps_q +0.01;
  - a history vintage: its latest year's EPS (eps_normalized) +0.01;
  - a dividend: its quarterly rate set to 0.99; a listing: its exchange set to "CTRL";
  - a guide: its first numeric field (eps_lo, eps_mid, rev_lo, ...) +0.01.
Each line reports how many dates change, the first and last, how many precede the fact's publication (must be 0), and whether
the first weekly date on or after it changes (a fact that changes nothing is "inert": its field may not reach the model).

Works with the builders that share build(as_of, facts, raw, spx, engine, out) and one ENGINE (all but ACN, SPGI and F before
2022; BKR's eras share one engine file per run). A few minutes per batch of 209 dates: each control rebuilds every date.
"""
import argparse
import contextlib
import copy
import importlib
import inspect
import io
import json
import os
import shutil
import signal
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from factwalk import RETRO  # noqa: E402

sys.path.insert(0, RETRO)

GUIDE_FIELDS = ("eps_lo", "eps_mid", "eps_hi", "eps", "rev_lo", "rev_mid", "rev_hi", "revenue_lo", "revenue_hi", "lo", "hi")


def controls(facts, start, end, only):
    out = []
    inside = lambda x: start <= x["published"] <= end     # noqa: E731
    want = lambda k: not only or k in only                # noqa: E731
    if want("prints"):
        for i, p in enumerate(facts["prints"]):
            for j, r in enumerate(p.get("restated", []) if isinstance(p.get("restated"), list) else []):
                if inside(r) and isinstance(r.get("eps_q"), (int, float)):
                    out.append((f"{p['quarter']} restatement of {r['published']}, its quarter EPS", r["published"],
                                lambda f, i=i, j=j: f["prints"][i]["restated"][j].update(eps_q=f["prints"][i]["restated"][j]["eps_q"] + 0.01)))
            if not inside(p):
                continue
            if isinstance(p.get("eps_q"), (int, float)):
                out.append((f"{p['quarter']} quarter EPS", p["published"],
                            lambda f, i=i: f["prints"][i].update(eps_q=f["prints"][i]["eps_q"] + 0.01)))
            if isinstance((p.get("fy_actual") or {}).get("revenue_usd_b"), (int, float)):
                out.append((f"{p['quarter']} full-year revenue", p["published"],
                            lambda f, i=i: f["prints"][i]["fy_actual"].update(revenue_usd_b=f["prints"][i]["fy_actual"]["revenue_usd_b"] + 0.5)))
    if want("history_vintages"):
        for i, v in enumerate(facts["history_vintages"]):
            if inside(v) and v.get("eps_normalized"):
                y = max(v["eps_normalized"])
                out.append((f"{v.get('fy_label', i)} vintage, its {y} EPS", v["published"],
                            lambda f, i=i, y=y: f["history_vintages"][i]["eps_normalized"].update({y: f["history_vintages"][i]["eps_normalized"][y] + 0.01})))
    if want("dividends"):
        for i, d in enumerate(facts.get("dividends") or []):
            if isinstance(d, dict) and inside(d) and "quarterly" in d:
                out.append((f"dividend of {d['published']}", d["published"], lambda f, i=i: f["dividends"][i].update(quarterly=0.99)))
    if want("listings"):
        for i, x in enumerate(facts.get("listings") or []):
            if isinstance(x, dict) and inside(x):
                out.append((f"listing of {x['published']} (effective {x.get('effective')})", x["published"],
                            lambda f, i=i: f["listings"][i].update(exchange="CTRL")))
    if want("guides"):
        for i, g in enumerate(facts.get("guides") or []):
            if isinstance(g, dict) and inside(g):
                k = next((k for k in GUIDE_FIELDS if isinstance(g.get(k), (int, float))), None)
                if k:
                    out.append((f"guide of {g['published']} ({k})", g["published"],
                                lambda f, i=i, k=k: f["guides"][i].update({k: f["guides"][i][k] + 0.01})))
    return out


def main():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ticker")
    ap.add_argument("start")
    ap.add_argument("end")
    ap.add_argument("--only", default="", help="comma-separated fact kinds (prints, history_vintages, dividends, listings, guides)")
    a = ap.parse_args()
    B = importlib.import_module(f"build_{a.ticker.lower()}")
    params = list(inspect.signature(B.build).parameters)
    if params != ["as_of", "facts", "raw", "spx", "engine", "out"]:
        sys.exit(f"build_{a.ticker.lower()}.build{tuple(params)}: not the common signature; write a control script for it")
    facts0 = json.load(open(B.FACTS, encoding="utf-8"))
    engine = open(B.ENGINE, encoding="utf-8").read()
    raw, spx = B.load_series(getattr(B, "SYMBOL", a.ticker)), B.load_series("^GSPC")
    dates = B.weekly_dates(a.start, a.end, sorted(raw), facts0["prints"])
    tmp = tempfile.mkdtemp()

    def build_all(facts):
        out = os.path.join(tmp, "m")
        with contextlib.redirect_stdout(io.StringIO()):
            for d in dates:
                B.build(d, facts, raw, spx, engine, out)
        res = {d: open(os.path.join(out, d, "model.py"), encoding="utf-8").read() for d in dates}
        shutil.rmtree(out)
        return res

    try:
        base = build_all(facts0)
        cs = controls(facts0, a.start, a.end, set(filter(None, a.only.split(","))))
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
    print(f"{a.ticker} {len(dates)} dates, {len(cs)} controls: {live} change dates on or after their publication, {len(cs) - live} inert, "
          f"{bad} change an earlier date")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
