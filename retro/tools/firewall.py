#!/usr/bin/env python3
"""
Firewall test: plant fake future facts and prices after CUTOFF, rebuild every archived date before it,
and require byte-identical models. Restores the fact sheet and the price cache afterwards, even on failure.

    python3 retro/tools/firewall.py 2015-01-01
    python3 retro/tools/firewall.py 2008-03-31 UNP          # the UNP series in staging/retrospective

Plants a print, a history vintage, an event per live theme and a company name (UNP: also a guide and a
dividend), all dated after CUTOFF and filled with absurd values, and multiplies every price of the ticker and
the S&P 500 from CUTOFF on by 10. Run it on a clean working tree (commit first). Exit code 0 means no model
before CUTOFF changed.

Controls (does altering one real input change exactly the dates after its release?) are case by case;
see retro/README.md, "Adding dates".
"""
import copy
import datetime as dt
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
cutoff = sys.argv[1]
TICKER = sys.argv[2].upper() if len(sys.argv) > 2 else "ACN"
FACTS = os.path.join(ROOT, "retro", "facts", f"{TICKER}.json")
CACHE = [os.path.join(ROOT, "retro", ".cache", n) for n in (f"{TICKER}.json", "_GSPC.json")]
OUTDIR = {"ACN": "archive/retrospective/ACN", "UNP": "staging/retrospective/UNP"}[TICKER]
ARCHIVE = os.path.join(ROOT, OUTDIR)
BUILDER = os.path.join(ROOT, "retro", f"build_{TICKER.lower()}.py")
# absurd values for every field the builder reads from a print
PLANT = {"ACN": dict(quarter="Q9 FY99", revenue_lc=-60, margin_bp=-999, fy_eps_guide=[0.1, 0.2], fy_rev_guide_lc=[-40, -30],
                     fy_fx=-50.0, fy_margin_guide=[1, 2], tax_rate=0.9, groups=[["PLANTED", 1, -99]],
                     cash_return_text="PLANTED", dividend_annual=9.99, dividend_note="PLANTED"),
         "UNP": dict(quarter="Q1 2099", fy=2099, commodity_pct=-60, carloads_pct=-60, arc_pct=-60, gtm_per_employee_pct=-60,
                     op_ratio=199.0, op_ratio_pt=99.0, groups=[["PLANTED", 1, -99]], cash_return_text="PLANTED",
                     outlook_short="PLANTED", diluted_shares_m=1.0, cash_b=99.0)}[TICKER]

git = lambda *a: subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True, check=True).stdout
if git("status", "--porcelain", "retro/facts", OUTDIR).strip():
    sys.exit("commit first: the fact sheet or the archive has uncommitted changes")

later = (dt.date.fromisoformat(cutoff) + dt.timedelta(days=10)).isoformat()
dates = sorted(os.path.basename(d) for d in glob.glob(os.path.join(ARCHIVE, "20*")) if os.path.basename(d) < cutoff)
backup = tempfile.mkdtemp()
changed = planted = ["not run"]
saved = {p: os.path.join(backup, f"{i}.json") for i, p in enumerate([FACTS] + CACHE)}   # two files are named ACN.json
for p, b in saved.items():
    shutil.copy(p, b)
try:
    with open(FACTS, encoding="utf-8") as fh:
        f = json.load(fh)
    last = copy.deepcopy(max(f["prints"], key=lambda p: p["published"] if p["published"] < cutoff else ""))
    last.pop("fy_actual", None)
    last.update(published=later, **PLANT)
    f["prints"].append(last)
    if "guides" in f:      # a guide for every fiscal year in the fact sheet, and a dividend
        for y in {g["fy"] for g in f["guides"]} | {2099}:
            f["guides"].append({"fy": y, "published": later, "source": last["source"], "doc": "PLANTED", "eps_guide": [0.1, 0.2],
                                "rev_guide": [-40, -30], "rev_guide_label": "PLANTED", "volume_guide": [-50, -40]})
        f["dividends"].append({"published": later, "source": last["source"], "quarterly": 9.99, "note": "PLANTED"})
    if "splits" in f:      # a split announced after CUTOFF, on a split date of the price data after CUTOFF
        with open(CACHE[0]) as fh:
            r = json.load(fh)["chart"]["result"][0]
        off = r["meta"]["gmtoffset"]
        days = sorted(dt.datetime.fromtimestamp(v["date"] + off, dt.timezone.utc).date().isoformat()
                      for v in r.get("events", {}).get("splits", {}).values())
        f["splits"] += [{"published": later, "source": last["source"], "effective": d, "ratio": 10, "note": "PLANTED"}
                        for d in days if d > later][:1]
    v = copy.deepcopy(max((x for x in f["history_vintages"] if x["published"] < cutoff), key=lambda x: x["published"]))
    v.update(published=later, why="PLANTED", company="PLANTED")
    v["eps_normalized"] = {**v["eps_normalized"], "2099": 0.01}
    f["history_vintages"].append(v)
    for theme in {e["theme"] for e in f["events"] if e["published"] < cutoff}:
        e = copy.deepcopy(max((e for e in f["events"] if e["theme"] == theme and e["published"] < cutoff), key=lambda e: e["published"]))
        e.update(published=later, doc="PLANTED")
        f["events"].append(e)
    f.setdefault("company_names", []).append({"published": later, "name": "PLANTED", "source": last["source"]})
    with open(FACTS, "w", encoding="utf-8") as fh:
        json.dump(f, fh, indent=1)
    ts_cut = dt.datetime.fromisoformat(cutoff).timestamp()
    for c in CACHE:
        with open(c) as fh:
            d = json.load(fh)
        r = d["chart"]["result"][0]
        for blk in r["indicators"].get("quote", []) + r["indicators"].get("adjclose", []):
            for arr in blk.values():
                if isinstance(arr, list):
                    for i, t in enumerate(r["timestamp"]):
                        if t >= ts_cut and arr[i] is not None:
                            arr[i] *= 10
        with open(c, "w") as fh:
            json.dump(d, fh)
    subprocess.run([sys.executable, BUILDER, *dates], check=True, capture_output=True)
    changed = [l for l in git("status", "--porcelain", OUTDIR).splitlines() if l.strip()]
    planted = [d for d in dates if "PLANTED" in open(os.path.join(ARCHIVE, d, "model.py"), encoding="utf-8").read()]
    print(f"{len(dates)} dates before {cutoff}: {len(changed)} files changed, {len(planted)} models contain planted text")
finally:
    for p, b in saved.items():
        shutil.copy(b, p)
    git("checkout", "--", OUTDIR)
sys.exit(1 if changed or planted else 0)
