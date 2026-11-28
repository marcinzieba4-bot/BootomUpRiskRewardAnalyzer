#!/usr/bin/env python3
"""
FANG (Diamondback Energy, Inc.) retrospective builder: the buildability gate, before any model.

    python3 retro/build_fang.py --weekly 2008-01-01 2009-12-31        # the requested range: every date refused, with its reason
    python3 retro/build_fang.py --weekly 2010-01-01 2013-12-31        # the fallback range: every date refused, with its reason
    python3 retro/build_fang.py --gate-md                             # rewrite staging/retrospective/FANG/GATE.md (both ranges)
    python3 retro/build_fang.py --check START END --json              # buildable dates as JSON (firewall.py's FANG gate test)
    python3 retro/build_fang.py --pro-forma --weekly START END        # sensitivity only: pro forma per-share figures counted as EPS

Method r2 needs, on each as-of date, (1) a close of the stock as traded, and (2) the stock's own P/E: at least one full fiscal year
of positive EPS of the company whose shares are priced, as its own filings public on that date publish it (the listing rule of
AVGO, V, KMI, CTVA and LYB; the loss and gap rules of F, MU and CRM; a predecessor's history is never substituted: KMI, CTVA, LYB).
The gate reads only retro/facts/FANG.json and Yahoo's FANG and ^GSPC series truncated at the as-of date:

  (1) price: Yahoo's FANG series is Diamondback Energy, Inc.'s common stock from 2012-10-12, its first trading day (NASDAQ: FANG);
      no share of the issuer or of its predecessors (Windsor Permian LLC and Windsor UT LLC, limited liability companies) traded
      before it;
  (2) anchor: the latest offering document or 10-K vintage public on the date; a period counts as a year only if it is twelve months
      (the six months of 2012 and the 2007 period from inception are not years: the CTVA 2017 rule), and only a positive per-share
      figure that the filing publishes as the company's own EPS can anchor a P/E. The predecessors' years have no per-share figure
      (membership interests, not shares), and the only per-share figures in any filing to 2013-12-31 are pro forma (2011 $(0.04),
      the six months of 2012 $1.07, 2012 $0.60), which are never used (the CTVA and CHTR rule). FY2012 also fails the AAPL FY2002
      test (the $54.1M first-day deferred tax charge of the Merger exceeds its $18.4M of income before income taxes; GAAP net loss).

Every weekly date of 2008-2013 fails (2), and every date before 2012-10-12 fails (1) too, so the builder writes nothing but GATE.md
(retro/README.md, "FANG 2008-2009"). A date that passes both would still need the prints, guides, rule-T thresholds and signals,
none of which is transcribed, so the builder stops there rather than build from a partial sheet. Weekly dates are the last trading
day of each ISO week (no print is transcribed, so no earnings week moves a date).
"""
import argparse
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import retro_tool  # noqa: E402

FACTS = os.path.join(HERE, "facts", "FANG.json")
ENGINE = os.path.join(HERE, "templates", "fang_engine.py.tmpl")
OUT = os.path.join(os.path.dirname(HERE), "staging", "retrospective", "FANG")
GATE_RANGES = [("2008-01-01", "2009-12-31"), ("2010-01-01", "2013-12-31")]


def trading_days(symbol):
    closes, _ = retro_tool.fetch_prices(symbol, as_traded=True)
    return closes


def weekly_dates(start, end, days):
    """The last trading day of each ISO week from START to END (inclusive)."""
    weeks = {}
    for d in sorted(x for x in days if start <= x <= end):
        weeks[dt.date.fromisoformat(d).isocalendar()[:2]] = d
    return sorted(weeks.values())


def _year_txt(k, p):
    if p["eps_diluted"] is not None:
        return f"{k} {p['eps_diluted']:+.2f}"
    pf = f", pro forma {p['eps_pro_forma']:+.2f} not used" if p["eps_pro_forma"] is not None else ""
    return f"{k} no EPS (net income {p['net_income_m']:+,.1f}M{pf})"


def gate(as_of, facts, fang, pro_forma=False):
    """The reasons a date cannot be built (empty: it passes the gate). pro_forma=True is the sensitivity, never the rule."""
    why = []
    if as_of not in fang:
        why.append(f"no FANG close on {as_of}: Yahoo's FANG series starts on {facts['series_start']}, the first trading day of "
                   "Diamondback's common stock; no share of it or its predecessors traded before")
    vs = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vs:
        return why + [f"no offering document or 10-K of Diamondback in the fact sheet is public on {as_of} (the S-1 of 2012-02-14 "
                      "and its Amendments No. 1-5 were not read: every date before Amendment No. 6 precedes the listing)"]
    v = max(vs, key=lambda v: v["published"])
    years = {k: p for k, p in v["periods"].items() if p["months"] == 12}
    eps = lambda p: p["eps_diluted"] if p["eps_diluted"] is not None else (p["eps_pro_forma"] if pro_forma else None)
    kept = {k: eps(p) for k, p in years.items() if eps(p) is not None and eps(p) > 0}
    if not kept:
        part = ", ".join(f"{k} ({p['months']} months)" for k, p in sorted(v["periods"].items()) if p["months"] != 12)
        doc = f"{v['fy_label']} 10-K" if v["kind"] == "10-K" else v["fy_label"]
        why.append(f"no full year of positive EPS of Diamondback's own shares in the {doc} ({v['source']}, "
                   f"{v['published']}): years " + ", ".join(_year_txt(k, p) for k, p in sorted(years.items()))
                   + (f"; not years: {part}" if part else ""))
    return why


def write_gate_md(secs, path):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("# FANG: the buildability gate (no date built)\n\nGenerated by `retro/build_fang.py --gate-md` (retro/README.md, "
                 "\"FANG 2008-2009\"). Each weekly date and the reason method r2 cannot build it; nothing else is written.\n\n```\n")
        for sec in secs:
            for d, why in sec:
                fh.write(f"{d}  " + ("passes the gate" if not why else "not built: " + "; ".join(why)) + "\n")
            fh.write(f"{len(sec)} dates: {sum(1 for _, w in sec if not w)} pass the gate, {sum(1 for _, w in sec if w)} refused; "
                     "nothing written\n")
        fh.write("```\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dates", nargs="*")
    ap.add_argument("--weekly", nargs=2, metavar=("START", "END"))
    ap.add_argument("--check", nargs=2, metavar=("START", "END"), help="report which weekly dates pass the gate")
    ap.add_argument("--json", action="store_true", help="with --check: print the passing dates as a JSON list only")
    ap.add_argument("--gate-md", action="store_true", help="write GATE.md: the gate's result on every weekly date of each range")
    ap.add_argument("--pro-forma", action="store_true", help="sensitivity: count pro forma per-share figures as EPS (writes nothing)")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    assert os.path.exists(ENGINE), ENGINE
    fang, spx = trading_days("FANG"), trading_days("^GSPC")
    assert min(fang) == facts["series_start"], (min(fang), "Yahoo's FANG series no longer starts where the fact sheet says")
    g = lambda d: gate(d, facts, {k: c for k, c in fang.items() if k <= d}, a.pro_forma)
    if a.gate_md:
        assert not a.pro_forma, "GATE.md is the rule's result, never the sensitivity's"
        secs = [[(d, g(d)) for d in weekly_dates(r0, r1, spx)] for r0, r1 in GATE_RANGES]
        os.makedirs(a.out, exist_ok=True)
        write_gate_md(secs, os.path.join(a.out, "GATE.md"))
        print(f"{os.path.join(a.out, 'GATE.md')}: {sum(len(x) for x in secs)} dates, {sum(1 for x in secs for _, w in x if w)} refused")
        return
    rng = a.check or a.weekly
    dates = sorted(set(a.dates) | set(weekly_dates(rng[0], rng[1], spx) if rng else []))
    for d in dates:
        if d not in spx:
            sys.exit(f"{d} is not a trading day")
    passing, refused = [], {}
    for d in dates:
        why = g(d)
        (refused.__setitem__(d, why) if why else passing.append(d))
    if a.check and a.json:
        print(json.dumps(passing))
        return
    for d in dates:
        print(f"{d}  " + ("passes the gate" if d in passing else "not built: " + "; ".join(refused[d])))
    print(f"{len(dates)} dates: {len(passing)} pass the gate, {len(refused)} refused; nothing written"
          + (" (sensitivity: pro forma per-share figures counted as EPS)" if a.pro_forma else ""))
    if passing and not a.check and not a.pro_forma:
        sys.exit(f"{passing[0]}: passes the gate, but the FANG prints, guides, rule-T thresholds and signals are not transcribed; "
                 "extend retro/facts/FANG.json and decide the engine's signals first (retro/README.md, \"FANG 2008-2009\")")


if __name__ == "__main__":
    main()
