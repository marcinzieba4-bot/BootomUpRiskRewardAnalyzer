#!/usr/bin/env python3
"""
Firewall test: plant fake future facts and prices after CUTOFF, rebuild every archived date before it,
and require byte-identical models. Restores the fact sheet and the price cache afterwards, even on failure.

    python3 retro/tools/firewall.py 2015-01-01
    python3 retro/tools/firewall.py 2008-03-31 UNP          # the UNP series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 LOW          # the LOW series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 AAPL         # the AAPL series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 NKE          # the NKE series in staging/retrospective
    python3 retro/tools/firewall.py 2009-10-01 AVGO         # the AVGO series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 PEP          # the PEP series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 MSFT         # the MSFT series in staging/retrospective

Plants a print, a history vintage, an event per live theme and a company name (UNP: also a guide and a
dividend; LOW and AAPL: also a guide with every guided field; NKE: a guide in words, and futures orders on the last print before
CUTOFF that a filing after it states, the 'futures_later' rule; AVGO: a later guide for every guided quarter; PEP: a display-only guide, and total servings that a filing after CUTOFF
first states on the last print before it, the 'servings_later' rule, and a listing on a new exchange; MSFT: a guide with every guided field, a later
range for every quarter the fact sheet guides, a later withdrawal of every guided year and call-only guidance words; a CLOUD event
from a later 10-K, as for every live theme), all dated after CUTOFF and filled with absurd values, and multiplies every price of the ticker and
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
OUTDIR = {"ACN": "archive/retrospective/ACN", "UNP": "staging/retrospective/UNP", "LOW": "staging/retrospective/LOW",
          "AAPL": "staging/retrospective/AAPL", "NKE": "staging/retrospective/NKE", "AVGO": "staging/retrospective/AVGO",
          "PEP": "staging/retrospective/PEP", "MSFT": "staging/retrospective/MSFT"}[TICKER]
ARCHIVE = os.path.join(ROOT, OUTDIR)
BUILDER = os.path.join(ROOT, "retro", f"build_{TICKER.lower()}.py")
# absurd values for every field the builder reads from a print
PLANT = {"ACN": dict(quarter="Q9 FY99", revenue_lc=-60, margin_bp=-999, fy_eps_guide=[0.1, 0.2], fy_rev_guide_lc=[-40, -30],
                     fy_fx=-50.0, fy_margin_guide=[1, 2], tax_rate=0.9, groups=[["PLANTED", 1, -99]],
                     cash_return_text="PLANTED", dividend_annual=9.99, dividend_note="PLANTED"),
         "UNP": dict(quarter="Q1 2099", fy=2099, commodity_pct=-60, carloads_pct=-60, arc_pct=-60, gtm_per_employee_pct=-60,
                     op_ratio=199.0, op_ratio_pt=99.0, groups=[["PLANTED", 1, -99]], cash_return_text="PLANTED",
                     outlook_short="PLANTED", diluted_shares_m=1.0, cash_b=99.0),
         "LOW": dict(quarter="Q1 FY99", fy=2099, q=1, sales_b=0.01, sales_pct=-60.0, comps_pct=-60.0, gross_margin=1.0,
                     gross_margin_bp=-999, op_margin=-50.0, op_margin_bp=-999, inventory_pct=99.0, inventory_gap_pp=99.0,
                     eps_q=0.01, eps_q_prior=9.99, stores=1, sq_ft_pct=-60.0, cash_return_text="PLANTED",
                     outlook_short="PLANTED", next_print="PLANTED", diluted_shares_m=1.0, cash_b=99.0),
         "AAPL": dict(quarter="Q1 FY99", fy=2099, q=1, sales_b=0.01, sales_pct=-60.0, gross_margin=1.0, gross_margin_bp=-999,
                      op_margin=-50.0, op_margin_bp=-999, mac_units_k=1, mac_units_pct=-60.0, non_mac_pct=-60.0, ipod_units_k=1,
                      ipod_units_pct=-60.0, iphone_units_k=1, eps_q=0.01, eps_q_prior=9.99, deferred_iphone_b=99.0,
                      non_gaap_note="PLANTED", cash_return_text="PLANTED", outlook_short="PLANTED", next_print="PLANTED",
                      diluted_shares_m=1.0, cash_b=99.0, mac_sales_pct=-60.0, iphone_sales_pct=-60.0),
         "NKE": dict(quarter="Q1 FY99", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, lc_pct=-60.0,
                     lc_note="PLANTED", futures_pct=-60.0, futures_fx_pp=-99.0, futures_b=0.01, futures_note="PLANTED",
                     futures_fx_note="PLANTED", gross_margin=1.0, gross_margin_bp=-999.0, pretax_margin=-50.0,
                     pretax_margin_bp=-999.0, inventory_b=99.0, inventory_pct=99.0, inventory_gap_pp=99.0, eps_q=0.01,
                     eps_q_prior=9.99, eps_note="PLANTED", diluted_shares_m=1.0, cash_b=99.0, next_print="PLANTED",
                     cash_return_text="PLANTED"),
         "AVGO": dict(quarter="Q1 FY99", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, seq_pct=-60.0,
                      sales_note="PLANTED", gross_margin=1.0, gross_margin_bp=-999.0, op_margin=-50.0, op_margin_bp=-999.0,
                      opex_pct=99.0, opex_gap_pp=99.0, inventory_b=99.0, inventory_pct=99.0, inventory_gap_pp=99.0,
                      inventory_note="PLANTED", eps_q=0.01, eps_q_prior=9.99, eps_note="PLANTED", shares_note="PLANTED",
                      diluted_shares_m=1.0, cash_b=99.0, ltd_b=99.0, next_print="PLANTED", cash_return_text="PLANTED",
                      raw=dict(sales_m=1, sales_prior_m=99, sales_prev_q_m=99, cogs_m=1, cogs_prior_m=1, rd_m=99, rd_prior_m=1,
                               sga_m=99, sga_prior_m=1, op_income_m=-99, op_income_prior_m=99, inventory_m=99, inventory_prior_m=1)),
         "PEP": dict(quarter="Q1 2099", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, lc_pct=-60.0, lc_note="PLANTED",
                     servings_pct=-60.0, servings_note="PLANTED", gross_margin=1.0, gross_margin_bp=-999.0, op_margin=-50.0,
                     op_margin_bp=-999.0, inventory_b=99.0, inventory_pct=99.0, inventory_gap_pp=99.0, eps_q=0.01, eps_q_prior=9.99,
                     eps_note="PLANTED", diluted_shares_m=1.0, cash_b=99.0, next_print="PLANTED", cash_return_text="PLANTED",
                     raw=dict(sales_m=1, sales_prior_m=99, cogs_m=1, cogs_prior_m=1, op_m=-99, op_prior_m=99, inventory_m=99,
                              inventory_prior_m=1)),
         "MSFT": dict(quarter="Q1 FY99", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, unearned_b=0.01, unearned_pct=-60.0,
                      receivables_b=99.0, receivables_pct=99.0, receivables_gap_pp=99.0, gross_margin=1.0, gross_margin_bp=-999.0,
                      op_margin=-50.0, op_margin_bp=-999.0, eps_q=0.01, eps_q_prior=9.99, eps_note="PLANTED", diluted_shares_m=1.0,
                      cash_b=99.0, next_print="PLANTED", cash_return_text="PLANTED", fx_note="PLANTED", sales_note="PLANTED",
                      unearned_note="PLANTED", receivables_note="PLANTED", lc_pct=-60.0, lc_note="PLANTED", guide_on_call="PLANTED",
                      raw=dict(sales_m=1, sales_prior_m=99, cogs_m=1, cogs_prior_m=1, op_m=-99, op_prior_m=99, ar_m=99, ar_prior_m=1,
                               unearned_m=1, unearned_prior_m=99))}[TICKER]
# LOW and AAPL guides carry more fields than UNP's: plant every one the builder reads (NKE's are words only)
GUIDE_PLANT = {"LOW": dict(comps_guide=[-50, -40], op_margin_guide_bp=[-999, -999], margin_def="PLANTED", stores_guide=1,
                           store_opening_m=9999, fy_words="PLANTED",
                           q_guide={"quarter": "Q4 FY99", "sales": [-40, -30], "comps": [-50, -40], "eps": [0.1, 0.2]}),
               "AAPL": dict(gm_guide_pct=[1, 2], q_guide_note="PLANTED",
                            q_guide={"quarter": "Q4 FY99", "sales_usd_b": [0.1, 0.2], "eps": [0.1, 0.2], "prior_sales_b": 99.0,
                                     "prior_source": "A14", "prior_label": "PLANTED", "gm_pct": [1, 2], "opex_usd_b": [99.0, 99.0],
                                     "oie_usd_b": [99.0, 99.0], "tax_pct": [99.0, 99.0]}),
               "NKE": dict(words=["PLANTED"]),
               "AVGO": dict(quarter="Q9 FY99", seq_pct=[-50, -40], base_quarter="PLANTED", base_sales_m=1, level_m=[0.5, 0.6],
                            prior_label="PLANTED", prior_sales_m=1, prior_source="V1", yoy_pct=[-50, -40], quote="PLANTED",
                            display="PLANTED"),
               "PEP": dict(display="PLANTED", unused="PLANTED"),
               "MSFT": dict(rev_guide_usd_b=[0.1, 0.2], op_income_guide_usd_b=[0.1, 0.2], note="PLANTED", opex_guide_usd_b=[0.1, 0.2],
                            q_guide={"quarter": "Q4 FY99", "sales_usd_b": [0.1, 0.2], "op_income_usd_b": [0.1, 0.2], "eps": [0.1, 0.2],
                                     "eps_words": "PLANTED", "prior_sales_b": 99.0, "prior_source": "MS1", "prior_label": "PLANTED"})}.get(TICKER, {})

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
    last.pop("servings_later", None)
    last.update(published=later, **PLANT)
    f["prints"].append(last)
    if "guides" in f:      # a guide for every fiscal year in the fact sheet, and a dividend
        for y in {g["fy"] for g in f["guides"]} | {2099}:
            f["guides"].append({"fy": y, "published": later, "source": last["source"], "doc": "PLANTED", "eps_guide": [0.1, 0.2],
                                "rev_guide": [-40, -30], "rev_guide_label": "PLANTED", "volume_guide": [-50, -40], **GUIDE_PLANT})
        f["dividends"].append({"published": later, "source": last["source"], "quarterly": 9.99, "note": "PLANTED"})
    if TICKER == "AAPL":   # a later withdrawal of every field of every guided quarter (the update of 2020-02-17 rule)
        for g in [g for g in f["guides"] if g["published"] < cutoff and "sales_usd_b" in g.get("q_guide", {})]:
            f["guides"].append({"fy": g["fy"], "published": later, "source": last["source"], "doc": "PLANTED", "quote": "PLANTED",
                                "q_guide": {"quarter": g["q_guide"]["quarter"],
                                            "withdrawn": ["sales_usd_b", "eps", "gm_pct", "opex_usd_b", "oie_usd_b", "tax_pct"]}})
    if TICKER == "NKE":    # futures orders that a filing after CUTOFF first states, on the last print before it
        p0 = max((p for p in f["prints"] if p["published"] < cutoff), key=lambda p: p["published"])
        if p0.get("futures_later", {}).get("published", cutoff) >= cutoff:     # a real one public before CUTOFF stays
            p0["futures_later"] = {"published": later, "source": p0["source"], "futures_pct": -60.0, "futures_fx_pp": -99.0,
                                   "futures_b": 0.01, "futures_note": "PLANTED", "futures_fx_note": "PLANTED"}
    if TICKER == "PEP":    # total servings that a filing after CUTOFF first states, on the last print before it (servings_later)
        p0 = max((p for p in f["prints"] if p["published"] < cutoff), key=lambda p: p["published"])
        if p0["servings_pct"] is None and p0.get("servings_later", {}).get("published", cutoff) >= cutoff:
            p0["servings_later"] = {"published": later, "source": p0["source"], "pct": -60.0, "note": "PLANTED"}
    if TICKER == "AVGO":   # a later guide for every quarter or fiscal year guided before CUTOFF, with absurd values (the latest guide
                           # for a quarter or year wins), absurd margin levels, and a later withdrawal of every fiscal year guided before it
        for g in [g for g in f["guides"] if g["published"] < cutoff]:
            f["guides"].append({**copy.deepcopy(g), "published": later, "doc": "PLANTED", "seq_pct": [-50, -40], "level_m": [0.5, 0.6],
                                "yoy_pct": [-99, -98], "quote": "PLANTED", "display": "PLANTED",
                                **({"op_margin_guide_pct": [1.0, 2.0], "margin_quote": "PLANTED"} if "op_margin_guide_pct" in g else {})})
        for y in sorted({(g["fy"], g["period"]) for g in f["guides"] if g.get("period") and g["published"] < cutoff}):
            f["guides"].append({"fy": y[0], "published": later, "source": last["source"], "doc": "PLANTED", "period": y[1],
                                "withdrawn": True, "quote": "PLANTED", "display": "PLANTED"})
    if "capital_return" in f:      # AAPL: a capital return statement (catalyst 5)
        f["capital_return"].append({"published": later, "source": last["source"], "doc": "PLANTED", "text": "PLANTED"})
    if "splits" in f:      # a split announced after CUTOFF, on a split date of the price data after CUTOFF
        with open(CACHE[0]) as fh:
            r = json.load(fh)["chart"]["result"][0]
        off = r["meta"]["gmtoffset"]
        days = sorted(dt.datetime.fromtimestamp(v["date"] + off, dt.timezone.utc).date().isoformat()
                      for v in r.get("events", {}).get("splits", {}).values())
        f["splits"] += [{"published": later, "source": last["source"], "effective": d, "ratio": 10, "note": "PLANTED"}
                        for d in days if d > later][:1]
    if TICKER == "MSFT":   # a later range for every quarter guided in the fact sheet, with absurd values (the latest guide for a quarter
                           # wins): a later guide may never reach an earlier date
        for q in sorted({g["q_guide"]["quarter"] for g in f["guides"] if "q_guide" in g}):
            f["guides"].append({"fy": 2000 + int(q.split("FY")[1]), "published": later, "source": last["source"], "doc": "PLANTED",
                                "eps_guide": [0.1, 0.2], "q_guide": {**GUIDE_PLANT["q_guide"], "quarter": q}})
        for y in sorted({g["fy"] for g in f["guides"] if g["published"] < cutoff}):   # and a later withdrawal of every guided year
            f["guides"].append({"fy": y, "published": later, "source": last["source"], "doc": "PLANTED", "withdrawn": True,
                                "quote": "PLANTED", "opex_guide_usd_b": [0.1, 0.2]})
    if "listings" in f:    # PEP: an exchange change announced and effective after CUTOFF
        f["listings"].append({"published": later, "effective": later, "exchange": "PLANTED", "source": last["source"], "note": "PLANTED"})
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
