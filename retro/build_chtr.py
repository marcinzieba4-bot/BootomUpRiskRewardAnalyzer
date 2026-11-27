#!/usr/bin/env python3
"""
CHTR (Charter Communications, Inc.) retrospective builder: the buildability gate, before any model.

    python3 retro/build_chtr.py --weekly 2008-01-01 2009-12-31        # the requested range: every date refused, with its reason
    python3 retro/build_chtr.py --weekly 2010-01-01 2013-12-31        # the fallback range: every date refused, with its reason
    python3 retro/build_chtr.py --weekly 2014-01-01 2017-12-31        # the 2014-2017 batch: every date refused, with its reason
    python3 retro/build_chtr.py --weekly 2018-01-01 2021-12-31        # the 2018-2021 batch: 56 dates refused, 153 built (2019-02-01 on)
    python3 retro/build_chtr.py --check --json START END              # buildable dates as JSON (firewall.py's CHTR gate test)
    python3 retro/build_chtr.py --gate-md                             # rewrite staging/retrospective/CHTR/GATE.md (every batch's dates)

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
mirror, 'one_off_tests'): FY2016's $15.94 with the approximately $3.3 billion valuation allowance reversal, and FY2017's $34.09 with
the approximately $9.3 billion Tax Reform benefit. The gate's own weekly dates are the last trading day of each ISO week.

From 2019-01-31 (the Q4 2018 release and the FY2018 10-K, the same morning) FY2018's GAAP $5.22 anchors, and the dates that pass the
gate are built (retro/README.md, "CHTR 2018-2021"): the weekly dates of build_acn.weekly_dates (in an earnings week, the first trading
day after the release; a release on the week's last trading day meets that day's close if it was public before the close), each
model the facts public on AS_OF plus retro/templates/chtr_engine.py.tmpl. The encodings:
  - history: the latest 10-K vintage; FY2017 is a distorted year that is not the latest once FY2018 is in, so the history and the P/E
    window start after it ('history_start': 2018, the window from 2018-01-01; the ACN FY02, AAPL FY2002 and CMCSA 2003 rule);
  - no revenue, EPS or margin guide in numbers in any filing: current-FY EPS is the last full year's (the rollover rule), BASE and the
    growth factor take the latest quarter's revenue growth as reported plus the net buyback, no margin step; the releases' capital
    expenditure outlooks are words, shown in the guide line (the CMCSA capex-guide rule);
  - prices as traded (Yahoo records no split for CHTR); the 2016-05-18 Parent Merger Exchange Ratio (0.9042) precedes every day any
    model reads (the window and the 52 weeks start on or after 2018-01-02), so it needs no price encoding: the builder asserts it;
  - signals: total customer relationships (the first customer line of every release), revenue, the Adjusted EBITDA margin, capital
    intensity (purchases of property, plant and equipment on revenues, lower is better) and the operating margin, each against the
    year-ago quarter in the same release, with rule T over the FY2018 10-K's decade (the Successor's 2011-2018 changes);
  - durability DURABLE (the 10-Ks' "seasonal and cyclical variations" are advertising and seasonal-area patterns), STREAMING on the watch
    list from each 10-K's online-video words (company-acknowledged, the CMCSA encoding: a factor pair that nets to zero).
"""
import argparse
import datetime as dt
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import retro_tool  # noqa: E402
from build_acn import MONTHS, load_series, minus_years  # noqa: E402
from build_acn import weekly_dates as build_weekly_dates  # noqa: E402

FACTS = os.path.join(HERE, "facts", "CHTR.json")
ENGINE = os.path.join(HERE, "templates", "chtr_engine.py.tmpl")
OUT = os.path.join(os.path.dirname(HERE), "staging", "retrospective", "CHTR")
EMERGENCE = "2009-11-30"       # the Plan's Effective Date (Form 15-12G of 2009-12-02, CH7): the Predecessor's stock was cancelled
PARENT_MERGER = "2016-05-18"   # the Parent Merger Exchange Ratio (0.9042), recorded, not encoded: no model reads a price before it
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder re-derives them from the fact sheet
ENGINE_THRESHOLDS = {"relationships": (2, 3, 5, 293), "revenue": (-4, 2, 8, 197), "ocf_margin": (-240, -120, 0, 160),
                     "capex": (960, 510, 60, -550), "op_margin": (-560, -290, -30, 210)}
RULE_T_KEYS = {"relationships": (1, False), "revenue": (1, False), "ocf_margin": (10, False), "capex": (10, True), "op_margin": (10, False)}
PRINT_KEYS = {"quarter", "fy", "q", "published", "source", "release", "release_time", "raw", "sales_b", "sales_pct", "rel_pct",
              "ocf_margin", "ocf_margin_bp", "op_margin", "op_margin_bp", "capex_pct", "capex_bp", "eps_q", "eps_q_prior",
              "diluted_shares_m", "cash_note", "next_print", "capex_outlook"}
LIVE_SCOPES_READ = ["OFFSHORE", "CLOUD", "ECOMMERCE", "STREAMING", "ENERGY_TRANSITION", "EV", "CRYPTO"]   # the themes the 10-Ks were read for


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


def rule_t(rt, keys=RULE_T_KEYS):
    """Rule T thresholds from the annual values: XBULL best, BULL median, BASE worst, BEAR one median-to-worst step beyond the worst
    (mirrored when lower is better); rounded half up to whole percent and to 10 bp."""
    out = {}
    for k, (unit, lower) in keys.items():
        assert (rt[k]["unit"], rt[k]["lower_is_better"]) == (unit, lower), (k, "the fact sheet's unit or direction differs")
        v = sorted(rt[k]["values"].values())
        assert len(v) >= 2, (k, "rule T needs at least two annual values")
        n = len(v)
        med = v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
        worst, best = (v[-1], v[0]) if lower else (v[0], v[-1])
        r = lambda x: math.floor(x / unit + 0.5) * unit
        out[k] = (r(worst + (worst - med)), r(worst), r(med), r(best))
        assert tuple(rt[k]["thresholds"][s] for s in ("BEAR", "BASE", "BULL", "XBULL")) == out[k], (k, "stored thresholds differ")
    return out


def check_print(p):
    """Re-derive a print's growth and margins from its raw published figures (they must match the fact sheet)."""
    assert set(p) <= PRINT_KEYS, (p["quarter"], sorted(set(p) - PRINT_KEYS), "a print field with no encoding yet; decide one first")
    r = p["raw"]
    pct = lambda a, b: round((b / a - 1) * 100, 2)
    mg = lambda x, rev: round(x / rev * 100, 2)
    want = {"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": pct(r["rev_prior_m"], r["rev_m"]), "rel_pct": pct(r["rel_prior_k"], r["rel_k"]),
            "ocf_margin": mg(r["ebitda_m"], r["rev_m"]),
            "ocf_margin_bp": round((mg(r["ebitda_m"], r["rev_m"]) - mg(r["ebitda_prior_m"], r["rev_prior_m"])) * 100, 1),
            "op_margin": mg(r["oi_m"], r["rev_m"]), "op_margin_bp": round((mg(r["oi_m"], r["rev_m"]) - mg(r["oi_prior_m"], r["rev_prior_m"])) * 100, 1),
            "capex_pct": mg(r["capex_m"], r["rev_m"]),
            "capex_bp": round((mg(r["capex_m"], r["rev_m"]) - mg(r["capex_prior_m"], r["rev_prior_m"])) * 100, 1),
            "eps_q": r["eps_q"], "eps_q_prior": r["eps_q_prior"], "diluted_shares_m": r["dil_sh_m"]}
    for k, v in want.items():
        assert p[k] == v or abs(p[k] - v) < 1e-9, (p["quarter"], k, p[k], v)


def kind_text(q):
    """The 10-K's own description of the company, shortened for the volatility line."""
    if q.startswith("We are the second largest cable operator in the United States"):
        return "The second largest U.S. cable operator"
    assert q.startswith("We are a leading broadband connectivity company and cable operator"), q
    return "A broadband connectivity company and cable operator"


def build(as_of, facts, raw, spx, engine, out):
    """Write <out>/<as_of>/model.py for a date that passes the gate."""
    chtr = {d: v[2] for d, v in raw.items()}
    why = gate(as_of, facts, {k: c for k, c in chtr.items() if k <= as_of})
    if why:
        sys.exit(f"{as_of}: not built: " + "; ".join(why))
    chart = retro_tool.chart("CHTR")
    assert not chart.get("events", {}).get("splits"), "Yahoo records a CHTR split: decide its encoding first"
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    for p in public:
        check_print(p)
    assert not [g for g in facts["guides"] if g["published"] <= as_of], "a guide needs its encoding first (no CHTR filing gives one)"
    assert not [d for d in facts["dividends"] if d["published"] <= as_of], "a dividend needs its encoding first (Charter pays none)"
    h = max((v for v in facts["history_vintages"] if v["published"] <= as_of), key=lambda v: v["published"])
    assert "model" in h, (as_of, "the latest vintage has no model fields")
    m = h["model"]
    hs = facts["history_start"]
    assert hs["published"] <= as_of
    tests = h["one_off_tests"]
    years = sorted(int(k) for k in h["periods"] if int(k) >= hs["fy"])
    kept = {y: h["periods"][str(y)]["eps_diluted"] for y in years
            if h["periods"][str(y)]["eps_diluted"] > 0 and not tests.get(str(y), {}).get("distorted")}
    assert sorted(kept) == years, (as_of, "a year of the history is a loss or distorted: decide its encoding first")
    rev = {y: round(h["periods"][str(y)]["revenue_m"] / 1000, 3) for y in years}
    shares = {y: h["periods"][str(y)]["diluted_shares_m"] for y in years}
    last_fy = max(years)
    cur_fy = last_fy + 1
    prints = [p for p in public if p["fy"] + (1 if p["q"] == 4 else 0) >= cur_fy]
    assert prints, (as_of, "no print after the history")
    latest = prints[-1]
    i = public.index(latest)
    prev = (public[i - 1]["rel_pct"], public[i - 1]["quarter"])
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    excl = tests["2017"]
    eps_now = kept[last_fy]
    eps_label = f"{fy_e}: no EPS guide in numbers, FY{last_fy % 100:02d}'s ${eps_now:.2f} (GAAP) stands"
    normalization = (f"GAAP diluted EPS from the {h['fy_label']} 10-K's selected financial data, every year kept by the one-off test; the history "
                     f"starts with FY2018: FY2017's ${h['periods']['2017']['eps_diluted']:.2f} is excluded ({excl['note']}), and FY2016 and the "
                     "loss years before it with it")
    fwd = [latest["sales_pct"]] * 2
    fwd_label, fwd_short, fwd_period = (f"no {fy_now} revenue guide in numbers, {latest['quarter']} revenues as reported",
                                        f"{latest['quarter'][:2]} revenues", latest["quarter"])
    cx = latest.get("capex_outlook")
    guide_text = (f"{fy_now}: no revenue, EPS or margin guide in numbers (BASE takes {latest['quarter']} revenue growth as reported)"
                  + (f"; capital expenditure outlook in words: '{cx}'" if cx else ""))

    # ── market statistics, prices as traded, truncated at AS_OF; the window from the history's start (2018-01-01) ──
    px = {d: v for d, v in raw.items() if d <= as_of}
    days = sorted(px)
    close = px[as_of][2]
    yr = [d for d in days if d > minus_years(as_of, 1)]
    low52, high52 = min(px[d][1] for d in yr), max(px[d][0] for d in yr)
    common = [d for d in yr if d in spx]
    ra = [math.log(px[common[k]][2] / px[common[k - 1]][2]) for k in range(1, len(common))]
    rm = [math.log(spx[common[k]][2] / spx[common[k - 1]][2]) for k in range(1, len(common))]
    ma, mm = sum(ra) / len(ra), sum(rm) / len(rm)
    vol = (sum((x - ma) ** 2 for x in ra) / len(ra)) ** 0.5 * 252 ** 0.5
    beta = (sum((x - ma) * (y - mm) for x, y in zip(ra, rm)) / len(ra)) / (sum((y - mm) ** 2 for y in rm) / len(rm))
    start = f"{hs['fy']}-01-01"
    window = [d for d in days if d > minus_years(as_of, 10) and d >= start]
    assert window[0] > PARENT_MERGER and min(yr) > PARENT_MERGER, "a statistic reads a day before the Parent Merger: encode it first"
    eps = {**kept, cur_fy: eps_now}
    fy = lambda d: min(int(d[:4]), cur_fy)
    yrs = (dt.date.fromisoformat(as_of) - dt.date.fromisoformat(window[0])).days / 365.25
    window_label = "10-yr" if yrs > 9.9 else f"{yrs:.1f}-yr"
    pe = {d: px[d][2] / eps[fy(d)] for d in window}
    srt = sorted(pe.values())
    qtl = lambda q: round(srt[int(q * (len(srt) - 1))], 1)
    pctl = {"p5": qtl(.05), "p10": qtl(.10), "p25": qtl(.25), "median": qtl(.5), "p75": qtl(.75), "p90": qtl(.9), "max": round(srt[-1], 1)}
    pe_now_pctl = round(sum(v <= close / eps_now for v in srt) / len(srt) * 100)
    yearly = []
    for y in sorted({d[:4] for d in window}):
        dd = min((d for d in window if d.startswith(y)), key=lambda d: pe[d])
        yearly.append((y, round(pe[dd], 1), dd))
    ref = min(yr, key=lambda d: px[d][2])

    # ── durability and themes, from the latest 10-K's words ──
    themes = retro_tool.load_taxonomy()["themes"]
    live = sorted((t["live_from"], k) for k, t in themes.items() if t["live_from"] <= as_of)
    live_k = [k for _, k in live]
    assert set(live_k) <= set(LIVE_SCOPES_READ), (as_of, "a live theme the CHTR 10-Ks were not read for", live_k)
    ev = [e for e in facts["events"] if e["published"] <= as_of and e["published"] >= h["published"]]
    assert [e["kind"] for e in ev] == ["streaming_company_acknowledged"], (as_of, "an event kind with no encoding", ev)
    e = ev[-1]
    assert e["source"] == h["source"]
    others = ", ".join(f"{k} to '{themes[k]['scope']}'" for k in live_k if k != "STREAMING")
    why = (f"{m['business_quote']} The 10-K's '{m['cyclical_quote']}' names seasonal service areas and advertising patterns ('"
           f"{m['cyclical_quote2']}'), not the cycle of the business's earnings, so DURABLE (the SPGI reading). STREAMING ('"
           f"{themes['STREAMING']['scope']}') is live from {themes['STREAMING']['live_from']} and the {e['doc']}'s words put it on the watch "
           f"list: company-acknowledged, with no dated evidence that the market prices it for Charter. Of the other live themes, {others}: "
           "none names a cable operator")
    mp = [x for x in themes["STREAMING"]["pit_evidence"] if x["date"] <= as_of]
    mp_txt = (f" The theme registry dates the market's pricing of streaming to {mp[-1]['date']} ({mp[-1]['event']}), evidence that names "
              "Disney's networks, not Charter." if mp else "")
    val_word = "a premium" if pe_now_pctl >= 70 else "a discount to its own history" if pe_now_pctl <= 30 else "near its own median"
    watch = [{"theme": "STREAMING", "status": "live, company-acknowledged; no market read",
              "reason": (f"Live: Charter's own {e['doc']} says '{e['risk_quote']}' At the same time {e['offering']}. The stock trades at "
                         f"{close / eps_now:.1f}x {fy_e_s} — {val_word}.{mp_txt} Re-file as DISRUPTION_EXPOSED (STREAMING) only if dated "
                         "evidence shows the market pricing streaming substitution of Charter's video customers specifically.")}]
    factors = [(f"Own streaming: {e['offering_short']}", 0.2, 0.10),
               (f"Online video competition ({e['doc']}): {e['risk_short']}", -0.2, 0.10)]
    sig_name = "Streaming: net effect on video demand"
    trigger = "Online video takes video customers faster than Internet and mobile growth replaces them"
    key_tail = ("Online video, fiber and wireless rivals are the competition the 10-K names;\n"
                "  Internet, mobile and business growth must cover the video losses.")
    theme_summary = "streaming is live and company-acknowledged; no dated evidence ties the multiple to it"
    cat3 = f"(3) A {fy_now} revenue, EPS or margin guide in numbers — none in the filings (the capital expenditure outlook is in words)"
    cat4 = (f"(4) Capital intensity — purchases of property, plant and equipment {latest['capex_pct']:.1f}% of revenues in "
            f"{latest['quarter']} ({latest['capex_bp']:+.1f}bp): network, mobile and equipment spend against free cash flow")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{latest['next_print'].split(' print')[0]} print)"
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        rt = same_day[-1]["release_time"]
        assert "before the open" in rt or "during the session" in rt, (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the close")
        tag = (f"(day of the {same_day[-1]['quarter']} print, public before the open)" if "before the open" in rt else
               f"(day of the {same_day[-1]['quarter']} print, released during the session)")

    company = CCI = "Charter Communications, Inc."
    listing = [x for x in facts["listings"] if x["published"] <= as_of][-1]
    exchange, listed = "NASDAQ", listing["symbol"]
    nodiv = [x for x in facts["no_dividend"] if x["published"] <= as_of][-1]
    ids = [h["source"]] + [p["source"] for p in prints] + [public[i - 1]["source"], listing["source"], nodiv["source"], e["source"]]
    sources = [dict(id=k, **facts["sources"][k]) for k in dict.fromkeys(ids)]
    sources.append({"id": "Y0", "published": as_of,
                    "title": f"Yahoo Finance daily prices, {CCI} Class A common stock ({exchange}: {listed}) and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/CHTR/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution "
                                f"from {window[0]}"})
    for x in sources:
        assert x["published"] <= as_of, (as_of, x["id"])
    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "rel_pct", "ocf_margin", "ocf_margin_bp", "op_margin", "op_margin_bp",
                   "capex_pct", "capex_bp", "eps_q", "eps_q_prior")
    r = latest["raw"]
    volumes = (f"total customer relationships {r['rel_k']:,.0f}K against {r['rel_prior_k']:,.0f}K a year earlier ({latest['rel_pct']:+.2f}%), "
               f"as the release shows them; purchases of property, plant and equipment ${r['capex_m']:,.0f}M against "
               f"${r['capex_prior_m']:,.0f}M; {latest['cash_note']}")
    fy_rev = rev[last_fy] * (1 + sum(fwd) / 2 / 100)
    fy_rev_label = f"{fwd_label}, applied to the year (no {fy_now} revenue guide)"
    groups = [tuple(g) for g in m["groups"]]
    fcf = f"${m['fcf_b']:.2f}B" if m["fcf_b"] >= 0 else f"$({-m['fcf_b']:.2f})B"
    R = repr
    head = f'''#!/usr/bin/env python3
"""
CHTR Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: {listed})  ·  {m["business_quote"].split(" and ")[0].replace("We are ", "")}
Generated by retro/build_chtr.py from retro/facts/CHTR.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "CHTR"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); cable signals")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts above.
PIT_PROFILE = {{
    "kind": "DURABLE",
    "risk": 2,
    "why": {R(why)},
    "theme_watch": {R(watch)},
    "evidence": {R([e["id"]])},
}}

# ── FACTS: market (prices truncated at AS_OF, as traded on each day) ──────────
CURRENT_PRICE   = {close:.2f}   # USD, {exchange} close {as_of}, as traded (Yahoo records no split)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2
PE_PCTL         = {R(pctl)}   # current-FY P/E over the window below
PE_NOW_PCTL     = {pe_now_pctl}    # share of those daily P/Es at or below the AS_OF one
WINDOW_LABEL    = {R(window_label)}   # P/E window: {window[0]} .. AS_OF (the history starts with FY2018)
YEARLY_MIN_PE   = {R(yearly)}   # (calendar year, lowest P/E, date)
VOL_ANNUAL_PCT  = {vol:.3f}   # 1-yr realized, daily log returns
VOL_BETA        = {beta:.2f}    # 1-yr beta vs S&P 500
VOL_52W_LOW     = {low52:.2f}
VOL_52W_HIGH    = {high52:.2f}
REF_LOW         = {px[ref][2]:.2f}   # lowest close of the last 52 weeks, {ref}
REF_LOW_LABEL   = {R(MONTHS[int(ref[5:7]) - 1])}

# ── FACTS: company history ({h["source"]}, vintage {h["published"]}) ──
EPS_NORM      = {R({y: round(v, 4) for y, v in kept.items()})}   # {normalization}
REVENUE_HIST  = {R(rev)}   # revenues, USD bn, Item 6
SHARES_HIST   = {R({y: round(v, 3) for y, v in shares.items()})}   # diluted weighted average shares, millions, Item 6
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {m["op_margin"]}   # operating margin (income from operations on revenues), {h["fy_label"]}
CHECK_PRETAX_MARGIN = {m["pretax_margin"]}   # income before income taxes on revenues, {h["fy_label"]} (before the noncontrolling interest), for the EPS check
TAX_RATE      = {m["tax_rate"]}   # income tax expense on income before income taxes, {h["fy_label"]}
CONS_DIVIDEND = 0.00   # no dividend: {nodiv["quote"]} ({nodiv["source"]})
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = "Operating margin change"
KIND_TEXT     = {R(kind_text(m["business_quote"]))}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} outlook ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_REL        = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # no revenue guide in numbers: the latest quarter's revenue growth as reported
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = False   # no margin guide: no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {m["op_margin"]}
FY_REVENUE_B    = {fy_rev:.2f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R(groups)}
GROUPS_BASIS    = {R(f"{h['fy_label']} revenues by service offering (10-K)")}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenues {m['sales_growth']:+.1f}%, total customer relationships {m['rel_pct']:+.2f}% (10-K); {latest['quarter'].split()[0]} Adjusted EBITDA margin {latest['ocf_margin']:.2f}% ({latest['ocf_margin_bp']:+.1f}bp)")}
BALANCE_TEXT    = {R(f"{h['fy_label']} year-end cash ${m['cash_b']:.2f}B, {h['fy_label']} free cash flow {fcf} (operating cash flow less purchases of property, plant and equipment), no dividend, {latest['cash_note']}")}
VOLUMES_TEXT    = {R(volumes)}
CAPITAL_RETURN  = {R(latest["cash_note"])}
THEME_FACTORS   = {R(factors)}
THEME_SIGNAL_NAME    = {R(sig_name)}
THEME_SIGNAL_TRIGGER = {R(trigger)}
THEME_SUMMARY        = {R(theme_summary)}
KEY_TRIGGER_TAIL     = {R(key_tail)}
CATALYST_3      = {R(cat3)}
CATALYST_4      = {R(cat4)}
'''
    os.makedirs(os.path.join(out, as_of), exist_ok=True)
    with open(os.path.join(out, as_of, "model.py"), "w", encoding="utf-8") as fh:
        fh.write(head + engine)
    return tag, latest["quarter"]


GATE_RANGES = [("2008-01-01", "2009-12-31"), ("2010-01-01", "2013-12-31"), ("2014-01-01", "2017-12-31"), ("2018-01-01", "2021-12-31")]


def write_gate_md(sections, path):
    """GATE.md: each batch's weekly dates (the gate's own, the last trading day of each ISO week) with the gate's result, as the
    --weekly runs print them; a date that passes the gate is built (its own folder)."""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("# CHTR: the buildability gate\n\nGenerated by `retro/build_chtr.py --gate-md` (retro/README.md, \"CHTR 2008-2009\", "
                 "\"CHTR 2014-2017\", \"CHTR 2018-2021\"). Each weekly date of each batch and the gate's result: the reason method r2 "
                 "cannot build it, or that it passes (and is built, in its own folder, on the builder's weekly date of that week).\n\n```\n")
        for k, (res) in enumerate(sections):
            if k:
                fh.write("\n")
            for d, why in res:
                fh.write(f"{d}  " + ("passes the gate: built" if not why else "not built: " + "; ".join(why)) + "\n")
            n = sum(1 for _, w in res if not w)
            fh.write(f"{len(res)} dates: {n} pass the gate, {len(res) - n} refused; "
                     + ("nothing written" if not n else f"{n} built") + "\n")
        fh.write("```\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dates", nargs="*")
    ap.add_argument("--weekly", nargs=2, metavar=("START", "END"))
    ap.add_argument("--check", nargs=2, metavar=("START", "END"), help="report which weekly dates pass the gate")
    ap.add_argument("--json", action="store_true", help="with --check: print the passing dates as a JSON list only")
    ap.add_argument("--gate-md", action="store_true", help="write GATE.md: the gate's result on every weekly date of each batch")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    assert os.path.exists(ENGINE), ENGINE
    chtr, spx = trading_days("CHTR"), trading_days("^GSPC")
    assert min(chtr) == facts["series_start"], (min(chtr), "Yahoo's CHTR series no longer starts where the fact sheet says")
    if a.gate_md:
        secs = [[(d, gate(d, facts, {k: c for k, c in chtr.items() if k <= d})) for d in weekly_dates(r0, r1, spx)] for r0, r1 in GATE_RANGES]
        write_gate_md(secs, os.path.join(a.out, "GATE.md"))
        print(f"{os.path.join(a.out, 'GATE.md')}: {sum(len(x) for x in secs)} dates, {sum(1 for x in secs for _, w in x if w)} refused")
        return
    if (a.weekly or a.dates) and not a.check:
        raw = load_series("CHTR")
        spx3 = load_series("^GSPC")
        with open(ENGINE, encoding="utf-8") as fh:
            engine = fh.read()
        ds = sorted(set(a.dates) | set(build_weekly_dates(a.weekly[0], a.weekly[1], sorted(spx3), facts["prints"]) if a.weekly else []))
        nb = 0
        for d in ds:
            why = gate(d, facts, {k: c for k, c in chtr.items() if k <= d})
            if why:
                print(f"{d}  not built: " + "; ".join(why)[:160] + " ...")
                continue
            tag, q = build(d, facts, raw, spx3, engine, os.path.abspath(a.out))
            nb += 1
            print(f"{d}  {tag:<46}  latest print {q}")
        print(f"{len(ds)} dates: {nb} built, {len(ds) - nb} refused")
        return
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
    print(f"{len(dates)} dates: {len(passing)} pass the gate, {len(refused)} refused; nothing written (--check)")


if __name__ == "__main__":
    main()
