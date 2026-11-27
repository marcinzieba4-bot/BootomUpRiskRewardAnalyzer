#!/usr/bin/env python3
"""
CHTR (Charter Communications, Inc.) retrospective builder: the buildability gate, before any model.

    python3 retro/build_chtr.py --weekly 2008-01-01 2009-12-31        # the requested range: every date refused, with its reason
    python3 retro/build_chtr.py --weekly 2010-01-01 2013-12-31        # the fallback range: every date refused, with its reason
    python3 retro/build_chtr.py --weekly 2014-01-01 2017-12-31        # the 2014-2017 batch: every date refused, with its reason
    python3 retro/build_chtr.py --check --json START END              # buildable dates as JSON (firewall.py's CHTR gate test)

Method r2 needs, on each as-of date, (1) a close of the stock as traded, and (2) the stock's own P/E: at least one full fiscal year
of positive EPS, of the company whose shares are priced, in the filings public on that date (the listing rule of AVGO, V, KMI and
CTVA; the loss and gap rules of F, MU and CRM; the BKR 2018 rule for a new listing after a predecessor). The gate reads only
retro/facts/CHTR.json and Yahoo's CHTR and ^GSPC series truncated at the as-of date:

  (1) price: Yahoo's CHTR series is the Successor's Class A common stock from 2010-01-05 (retro/facts/CHTR.json, 'price_basis');
      no close of the Predecessor's Class A (NASDAQ: CHTR to 2009-04-06, then the OTC Bulletin Board or the Pink Sheets to its
      cancellation on 2009-11-30) is served;
  (2) anchor: the latest 10-K vintage public on the date; a period counts as a year only if it is twelve months (the Predecessor's
      eleven months to 2009-11-30 and the Successor's first month are not years: the CTVA 2017 rule), only years of the issuer
      whose shares the date prices count (from the 2009-11-30 emergence, the Successor's; the BKR 2018 rule), and only a positive
      diluted EPS can anchor a P/E (a loss has none: the F, MU and CRM rule).

Every weekly date of 2008-2017 fails (2), and every date before 2010-01-05 fails (1) too, so the builder writes nothing
(retro/README.md, "CHTR 2008-2009", "CHTR 2014-2017"). From the FY2014 10-K the vintages name no Predecessor or Successor and print
only the post-emergence years ('priced_issuers'); a Q4 release's full year extends the vintage until its 10-K ('q4_actuals'); and a
positive year whose listed one-offs distort it, with no figure excluding only them, does not anchor (the AAPL FY2002 test and its
mirror, 'one_off_tests'): FY2016's $15.94 with the approximately $3.3 billion valuation allowance reversal. A date that passes both would still need the prints, guides, rule-T thresholds and signals,
none of which is transcribed, so the builder stops there rather than build from a partial sheet. Weekly dates are the last
trading day of each ISO week (no print is transcribed, so no earnings week moves a date).
"""
import argparse
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import retro_tool  # noqa: E402

FACTS = os.path.join(HERE, "facts", "CHTR.json")
ENGINE = os.path.join(HERE, "templates", "chtr_engine.py.tmpl")
OUT = os.path.join(os.path.dirname(HERE), "staging", "retrospective", "CHTR")
EMERGENCE = "2009-11-30"       # the Plan's Effective Date (Form 15-12G of 2009-12-02, CH7): the Predecessor's stock was cancelled


def trading_days(symbol):
    closes, _ = retro_tool.fetch_prices(symbol, as_traded=True)
    return closes


def weekly_dates(start, end, days):
    """The last trading day of each ISO week from START to END (inclusive)."""
    weeks = {}
    for d in sorted(x for x in days if start <= x <= end):
        weeks[dt.date.fromisoformat(d).isocalendar()[:2]] = d
    return sorted(weeks.values())


def gate(as_of, facts, chtr):
    """The reasons a date cannot be built (empty: it passes the gate)."""
    why = []
    if as_of not in chtr:
        why.append(f"no CHTR close on {as_of}: Yahoo's CHTR series starts on {facts['series_start']}, and no close of a Charter "
                   "Class A share before it is served")
    vs = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vs:
        return why + [f"no 10-K vintage is public on {as_of}"]
    v = max(vs, key=lambda v: v["published"])
    # a Q4 release's full year extends the vintage from the release until the 10-K that reports the year (the vintage rule)
    q4 = [a for a in facts.get("q4_actuals", []) if a["published"] <= as_of and str(a["fy"]) not in v["periods"]]
    periods = {**v["periods"], **{str(a["fy"]): a["period"] for a in q4}}
    tests = {**v.get("one_off_tests", {}), **{str(a["fy"]): a["one_off_test"] for a in q4 if "one_off_test" in a}}
    # from the emergence only the priced shares' periods are years of them: the Successor's in the vintages that label the
    # Predecessor and the Successor (FY2009-FY2013 10-Ks); in the later ones every period is the post-emergence company's
    # ('priced_issuers'); before it every period of the issuer counts (those filings know no Successor)
    priced = v.get("priced_issuers", ["Successor"])
    issuer = (f"the {priced[0]}'s" if "priced_issuers" not in v else f"{priced[0]}'s") if as_of >= EMERGENCE else "the issuer's"
    from_q4 = {str(a["fy"]) for a in q4}                 # a Q4 release's year (2014 on) is the post-emergence company's
    years = {k: p for k, p in periods.items() if p["months"] == 12 and (as_of < EMERGENCE or p["issuer"] in priced or k in from_q4)}
    # a positive year whose listed one-offs distort it, with no published figure excluding only them, is excluded (the AAPL FY2002
    # test and its mirror); no year of 1999-2015 is positive, so the test arises first for FY2016
    distorted = {k: t for k, t in tests.items() if k in years and t["distorted"] and t["figure_without_published"] is None}
    kept = {k: p["eps_diluted"] for k, p in years.items() if p["eps_diluted"] > 0 and k not in distorted}
    if not kept:
        losses = ", ".join(f"{k} {p['eps_diluted']:+.2f}" for k, p in sorted(years.items()) if k not in distorted)
        part = ", ".join(f"{k} ({p['issuer']}, {p['months']} month{'s' if p['months'] > 1 else ''}) {p['eps_diluted']:+.2f}"
                         for k, p in sorted(periods.items()) if p["months"] != 12)
        excl = "; ".join(f"{k} {years[k]['eps_diluted']:+.2f} excluded: the listed one-off benefit (${t['items_after_tax_m']:,.0f}M, "
                         f"{t['item']}) exceeds the year's income without it (${t['income_without_m']:,.0f}M of "
                         f"${t['income_attributable_m']:,.0f}M), and no filing publishes a figure excluding only it (the mirror of the "
                         "AAPL FY2002 test)" for k, t in sorted(distorted.items()))
        src = f"the {v['fy_label']} 10-K ({v['source']}, {v['published']})" + "".join(
            f" and the Q4 {a['fy']} release ({a['source']}, {a['published']})" for a in q4)
        why.append(f"no full year of positive EPS of {issuer} shares in {src}: " + (f"years {losses}" if losses else "no full year")
                   + (f"; not years: {part}" if part else "") + (f"; {excl}" if excl else ""))
    return why


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dates", nargs="*")
    ap.add_argument("--weekly", nargs=2, metavar=("START", "END"))
    ap.add_argument("--check", nargs=2, metavar=("START", "END"), help="report which weekly dates pass the gate")
    ap.add_argument("--json", action="store_true", help="with --check: print the passing dates as a JSON list only")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    assert os.path.exists(ENGINE), ENGINE
    chtr, spx = trading_days("CHTR"), trading_days("^GSPC")
    assert min(chtr) == facts["series_start"], (min(chtr), "Yahoo's CHTR series no longer starts where the fact sheet says")
    rng = a.check or a.weekly
    dates = sorted(set(a.dates) | set(weekly_dates(rng[0], rng[1], spx) if rng else []))
    for d in dates:
        if d not in spx:
            sys.exit(f"{d} is not a trading day")
    passing, refused = [], {}
    for d in dates:
        why = gate(d, facts, {k: c for k, c in chtr.items() if k <= d})
        (refused.__setitem__(d, why) if why else passing.append(d))
    if a.check and a.json:
        print(json.dumps(passing))
        return
    for d in dates:
        print(f"{d}  " + ("passes the gate" if d in passing else "not built: " + "; ".join(refused[d])))
    print(f"{len(dates)} dates: {len(passing)} pass the gate, {len(refused)} refused; nothing written")
    if passing and not a.check:
        sys.exit(f"{passing[0]}: passes the gate, but the CHTR prints, guides, rule-T thresholds and signals are not transcribed; "
                 "extend retro/facts/CHTR.json and decide the engine's signals first (retro/README.md, \"CHTR 2014-2017\")")


if __name__ == "__main__":
    main()
