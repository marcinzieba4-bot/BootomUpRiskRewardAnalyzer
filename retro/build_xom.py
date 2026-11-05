#!/usr/bin/env python3
"""
Build XOM retrospective models from the dated fact sheet (retro/facts/XOM.json).

The XOM sibling of build_msft.py: the same frozen rules (retro method r2), the same weekly dates and the same market
statistics, with integrated oil and gas signals (retro/templates/xom_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, on the AS_OF share basis (ExxonMobil last split
     on 2001-07-19, so for every date from then Yahoo's split-adjusted series is the price as traded; the split restates the
     per-share facts published before it),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

ExxonMobil's fiscal year is the calendar year. It gives no earnings, revenue, volume or margin guidance in numbers in any filing
of the period, so the no-guide rules of method r2 apply on every date (retro/README.md, "XOM"):
  - current-FY EPS: the last full year's EPS stands (the rollover rule, as for UNP from 2008-01-25 and NKE),
  - forward revenue growth: the latest quarter's revenue growth, as reported (the UNP rule; no filing states a currency effect
    on revenue, so it is the reported growth, the MSFT and PEP fallback),
  - guided margin step: none; the margin signal uses the latest quarter's change in pre-tax margin.
Revenue is total revenues and other income, the one revenue line the releases publish, and the annual history takes it from the
10-K income statements. EPS is diluted EPS from continuing operations before extraordinary items and the cumulative effect of
accounting changes, each year from the latest filing that reports it, and the company's earnings per share excluding special items
replace it where a filing publishes them (the ACN rule). From 2009 the analyst-meeting 8-Ks state the current year's production
outlook in numbers: a volume guide, display only (method r2 has no volume input; the UNP rule). Any other guide field needs its
encoding decided first. A Q4 print may restate an earlier year's figure excluding special items ('restates': the Q4 2009
release's 2008 $8.44 under the participating-securities EPS rule adopted in 2009), until the next 10-K vintage carries it.
From Q1 2013 the releases no longer report special items, so each later year is GAAP; FY2016's $2 billion impairment is excluded
in dollars only, so it stays in (nothing is derived; retro/README.md, "XOM 2013-2017"). The one event kind encoded: each 10-K's
climate-change risk factor (transition_company_acknowledged) puts ENERGY_TRANSITION on the watch list from the theme's live date
(2015-12-12), company-acknowledged with no market read: text only (the MSFT CLOUD rule). From the FY2012 vintage the 'why' ends
with a clause on the theme's status on AS_OF ('why_theme_tail').

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release,
where it is the first trading day after it. ExxonMobil's earnings 8-Ks of 2007-2008 were accepted before the open or during the
session on the release day, so a print is dated that day; a print released on the week's last trading day before the open meets
that day's close (release_time; the Q4 2007 print, Friday 2008-02-01).

Output goes to staging/retrospective/XOM until the series is added to the archive (--out archive/retrospective/XOM).

Usage
  python3 retro/build_xom.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_xom.py --weekly 2009-01-05 2012-12-31
  python3 retro/build_xom.py --weekly 2013-01-07 2017-12-31
  python3 retro/build_xom.py 2008-02-01
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/XOM/<AS_OF>
"""
import argparse
import datetime as dt
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import retro_tool  # noqa: E402
from build_acn import MONTHS, load_series, minus_years, weekly_dates  # noqa: E402
from build_unp import money, on_basis  # noqa: E402

FACTS = os.path.join(HERE, "facts", "XOM.json")
ENGINE = os.path.join(HERE, "templates", "xom_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "XOM")
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"production": (-7, -4, -1, 4), "product_sales": (-20, -10, 0, 3), "revenue": (-41, -16, 9, 25),
                     "chem_sales": (-9, -4, 1, 7), "pretax_margin": (-630, -270, 90, 560)}
# the guide fields this builder has an encoding for: a current-year production outlook in numbers ('production_quote'), display only
GUIDE_KEYS = {"fy", "published", "source", "doc", "production_quote", "note"}
RULE_T_KEYS = {"production": (1, False), "product_sales": (1, False), "revenue": (1, False), "chem_sales": (1, False),
               "pretax_margin": (10, False)}           # (rounding unit, lower is better)


def fiscal_year_end(n):
    """ExxonMobil's fiscal year n is the calendar year n."""
    return dt.date(n, 12, 31)


def fiscal_year(day):
    return dt.date.fromisoformat(day).year


def rule_t(rt):
    """Rule T thresholds from the annual values: XBULL best, BULL median, BASE worst, BEAR one median-to-worst step beyond
    the worst; rounded half up to whole percent and to 10 bp."""
    out = {}
    for k, (unit, lower) in RULE_T_KEYS.items():
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
    """Re-derive a print's growth rates and margin from its raw published figures (they must match the fact sheet)."""
    r = p["raw"]
    pct = lambda a, b: (b / a - 1) * 100
    m, m0 = r["pretax_m"] / r["rev_m"] * 100, r["pretax_prior_m"] / r["rev_prior_m"] * 100
    want = {"sales_b": r["rev_m"] / 1000, "sales_pct": round(pct(r["rev_prior_m"], r["rev_m"]), 1),
            "pretax_margin": round(m + 0.0, 2), "pretax_margin_bp": round((m - m0) * 100, 1),
            "production_pct": round(pct(r["oe_prior_kbd"], r["oe_kbd"]), 1),
            "product_sales_pct": round(pct(r["pps_prior_kbd"], r["pps_kbd"]), 1),
            "chem_pct": round(pct(r["chem_prior_kt"], r["chem_kt"]), 1)}
    for k, v in want.items():
        assert abs(p[k] - v) < 1e-9, (p["quarter"], k, p[k], v)


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    chart = retro_tool.chart("XOM")
    fx = retro_tool.split_factor(chart, as_of)
    assert fx == 1.0, "a split after 2001-07-19 needs its encoding first (prices on the AS_OF share basis, the UNP rule)"
    off = chart["meta"]["gmtoffset"]
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + off, dt.timezone.utc).date().isoformat()
                    for v in chart.get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo_splits for s in facts.get("splits", [])), "a split's effective date must match the price data"
    px = dict(raw)
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    # ExxonMobil gives no earnings, revenue or margin guidance in numbers; a guide public on AS_OF may carry only encoded fields
    for g in [g for g in facts["guides"] if g["published"] <= as_of]:
        assert set(g) <= GUIDE_KEYS, (g["doc"], "a guide field with no encoding yet; decide one first")
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        check_print(p)
    facts, split_ids = on_basis(facts, as_of)      # the 2001 split: 1998 EPS and the first year's diluted shares
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    # prints published by AS_OF that report a fiscal year after the history (a Q4 print reports the year just ended, so it
    # stays in scope after the 10-K that follows it)
    first_fy = max(int(k) for k in h["eps_normalized"]) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    prints = [p for p in facts["prints"] if p["published"] <= as_of and guide_fy(p) >= first_fy]
    # no disruption theme in taxonomy_eras.json is live for an oil and gas producer to 2015-12-11 (ENERGY_TRANSITION, which carries
    # oil, gas and refining, is live from 2015-12-12); the 10-K's alternative-energy and climate-change wording stays in the
    # durability 'why' (the PEP obesity rule). The one encoding decided (retro/README.md, "XOM 2013-2017"): each 10-K's climate-change
    # risk factor (transition_company_acknowledged) puts ENERGY_TRANSITION on the watch list from the theme's live date, with the
    # latest 10-K's words (a 10-K's wording is replaced by the next 10-K's; the MSFT CLOUD rule). Any other event kind needs its
    # encoding decided first
    events = [e for e in facts["events"] if e["published"] <= as_of and (h["published"] <= e["published"] or "doc" not in e)]
    if any(e["kind"] != "transition_company_acknowledged" for e in events):
        sys.exit(f"{as_of}: the XOM builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
    themes = retro_tool.load_taxonomy()["themes"]
    events = [e for e in events if themes[e["theme"]]["live_from"] <= as_of]      # a theme counts only from its live date
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is public yet")
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage
    h = {**h, "extended": ""}
    for p in prints:
        a = p.get("fy_actual")
        if a and str(a["fy"]) not in h["eps_normalized"]:          # the 10-K vintage, once out, wins
            y = str(a["fy"])
            # an earlier year's company figure excluding special items, first published in this release ('restates'), replaces it until
            # the next 10-K vintage carries it (the ACN rule; the MSFT Q4 FY12 encoding)
            eps_n = {**h["eps_normalized"], y: a["eps_normalized"]}
            for yy, e in a.get("restates", {}).items():
                assert yy in eps_n, (p["quarter"], yy, "restates a year outside the history")
                eps_n[yy] = e
            h.update(fy_label=a["fy_label"],
                     eps_normalized=eps_n,
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]},
                     diluted_shares_m={**h["diluted_shares_m"], y: a["diluted_shares_m"]},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_pretax_margin=a["pretax_margin"], prev_fy_pretax_margin_note=a["pretax_margin_note"],
                     prev_fy_sales_growth=a["sales_growth"], prev_fy_production_pct=a["production_pct"],
                     prev_fy_production_note=f'{a["production_note"]}',
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    latest = prints[-1]
    # the previous quarter is the print published just before the latest one (in or out of the history's scope); before the
    # first print in the fact sheet, the vintage names it
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    i = public.index(latest)
    prev = (public[i - 1]["production_pct"], public[i - 1]["quarter"]) if i > 0 else (h["prev_q_production_pct"], h["prev_q_label"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    cur_fy = max(eps_hist) + 1
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── no guide in numbers: the last full year's EPS stands, and BASE takes the latest quarter's revenue growth ──
    eps_now = eps_hist[cur_fy - 1]
    eps_label = f"{fy_e}: no EPS guide in numbers, FY{(cur_fy - 1) % 100:02d}'s ${money(eps_now)} stands"
    fwd = [latest["sales_pct"]] * 2
    fwd_label, fwd_short, fwd_period = (f"no {next_q} revenue guide, {latest['quarter']} revenue as reported",
                                        f"{latest['quarter'][:2]} revenue", latest["quarter"])
    words = (f"; the {latest['quarter']} release, in words: '{latest['outlook_words']}' (no field)" if latest.get("outlook_words") else "")
    # the latest production outlook for the current year, display only (the UNP volume-guide rule)
    gp = next((g for g in reversed([g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]) if "production_quote" in g), None)
    if gp:
        guide_text = (f"{fy_now}: no earnings, revenue or margin guide in numbers (BASE takes {latest['quarter']} revenue growth); production "
                      f"outlook ({gp['doc']}): '{gp['production_quote']}' ({gp['note']}; display only: method r2 has no volume input)" + words)
    else:
        guide_text = (f"{fy_now}: no guide in numbers in any filing (ExxonMobil gives no earnings, revenue, volume or margin guidance; "
                      f"BASE takes {latest['quarter']} revenue growth)" + words)
    margin_guided = False                          # no pre-tax margin guide in numbers: no guided step
    fy_margin_base = h["prev_fy_pretax_margin"]

    # ── dividend: the latest declared rate ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts["dividends"] if d["published"] <= as_of]
    divs.append((h.get("dividend_published", h["published"]), h["dividend_annual"], h["dividend_note"], None))
    _, dividend, dividend_note, dividend_src = max(divs, key=lambda x: x[0])

    # ── market statistics, prices truncated at AS_OF ──
    days = sorted(d for d in px if d <= as_of)
    close = px[as_of][2]
    yr = [d for d in days if d > minus_years(as_of, 1)]
    low52, high52 = min(px[d][1] for d in yr), max(px[d][0] for d in yr)
    common = [d for d in yr if d in spx]
    ra = [math.log(px[common[i]][2] / px[common[i - 1]][2]) for i in range(1, len(common))]
    rm = [math.log(spx[common[i]][2] / spx[common[i - 1]][2]) for i in range(1, len(common))]
    ma, mm = sum(ra) / len(ra), sum(rm) / len(rm)
    vol = (sum((x - ma) ** 2 for x in ra) / len(ra)) ** 0.5 * 252 ** 0.5
    beta = (sum((x - ma) * (y - mm) for x, y in zip(ra, rm)) / len(ra)) / (sum((y - mm) ** 2 for y in rm) / len(rm))
    eps = {**eps_hist, cur_fy: eps_now}                                # + current-FY EPS, for the P/E series
    fy = lambda d: min(fiscal_year(d), cur_fy)     # a day past the last reported year keeps the current year's EPS
    window = [d for d in days if d > minus_years(as_of, 10) and (not h["pe_window_start"] or d >= h["pe_window_start"])]
    assert all(fy(d) in eps for d in window), (as_of, "P/E window needs EPS for every fiscal year")
    years = (dt.date.fromisoformat(as_of) - dt.date.fromisoformat(window[0])).days / 365.25
    window_label = "10-yr" if years > 9.9 else f"{years:.1f}-yr"
    pe = {d: px[d][2] / eps[fy(d)] for d in window}
    srt = sorted(pe.values())
    qtl = lambda p: round(srt[int(p * (len(srt) - 1))], 1)
    pctl = {"p5": qtl(.05), "p10": qtl(.10), "p25": qtl(.25), "median": qtl(.5), "p75": qtl(.75), "p90": qtl(.9), "max": round(srt[-1], 1)}
    pe_now_pctl = round(sum(v <= close / eps_now for v in srt) / len(srt) * 100)
    yearly = []
    for y in sorted({d[:4] for d in window}):
        dd = min((d for d in window if d.startswith(y)), key=lambda d: pe[d])
        yearly.append((y, round(pe[dd], 1), dd))
    ref = min(yr, key=lambda d: px[d][2])

    # ── era-dependent text, from facts only: no disruption theme has dated evidence on AS_OF ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
    key_tail = ("Prices drive earnings, by the company's own account; the bear needs crude\n"
                "  and gas realizations to fall, not only volumes.")
    theme_summary = "no disruption theme has dated evidence"
    why = h["why"]
    if h.get("why_theme_tail"):                    # from the FY2012 vintage the theme clause follows the theme's status on AS_OF
        why += "; no disruption theme is live for an oil and gas producer, so the alternative-energy and climate-change wording stays here"
    for e in [e for e in events if e["kind"] == "transition_company_acknowledged"][-1:]:
        # ENERGY_TRANSITION is live from 2015-12-12 and scoped to oil, gas and coal reserves and refining; the latest 10-K's climate-change
        # risk factor puts it on the watch list (the ACN CLOUD rule, as for MSFT: company-acknowledged, no market read). The factor pair
        # nets to zero and the theme signal stays at 2/4, so only text changes; re-filing needs dated evidence of market pricing
        val_word = "a premium" if pe_now_pctl >= 70 else "a discount to its own history" if pe_now_pctl <= 30 else "near its own median"
        stage = "transition"
        watch = [{"theme": "ENERGY_TRANSITION", "status": "live, company-acknowledged; no market read",
                  "reason": (f"Live: ExxonMobil's own {e['doc']}, under '{e['heading']}', says '{e['risk_quote']}' Under "
                             f"'{e['offering_heading']}': '{e['offering']}' The stock trades at {close / eps_now:.1f}x {fy_e_s} — {val_word}. "
                             "Re-file as DISRUPTION_EXPOSED (ENERGY_TRANSITION) only if dated evidence shows the market pricing "
                             "decarbonisation of ExxonMobil's reserves and refining specifically.")}]
        factors = [(f"Lower-carbon research: {e['offering_short']} — ExxonMobil funds it as well", 0.2, 0.10),
                   (f"Climate rules ({e['doc']}): {e['risk_short']}", -0.2, 0.10)]
        sig_name = "Energy transition: net effect on hydrocarbon demand"
        trigger = "Greenhouse gas rules cut hydrocarbon demand faster than ExxonMobil's own lower-carbon research pays off"
        theme_summary = "the energy transition is live and company-acknowledged; no dated evidence ties the multiple to it"
        assert h.get("why_theme_tail"), "a vintage before FY2012 states that no theme is live"
        why = h["why"] + ("; ENERGY_TRANSITION is live (from 2015-12-12) and its climate-change risk factor puts it on the watch list: "
                          "company-acknowledged, with no dated evidence that the market prices it for ExxonMobil")
    cat3 = (f"(3) The {fy_now} production outlook — '{gp['production_quote']}' ({gp['doc']}; display only): no earnings or revenue guide"
            if gp else f"(3) A {fy_now} guide — none: ExxonMobil gives no earnings, revenue or volume guidance in its filings")
    cat4 = f"(4) Capital and exploration expenditures — {latest['capex_note']} in {latest['quarter']}: the projects the volumes need"

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    # a print dated AS_OF meets AS_OF's close only if it was public before the open (the week's last trading day)
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    company = h["company"]
    exchange = h["exchange"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])]
           + ([dividend_src] if dividend_src else []) + ([gp["source"]] if gp else []) + split_ids + [e["id"] for e in events])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "A0", "published": as_of, "title": "Yahoo Finance daily prices, XOM and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/XOM/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "pretax_margin", "pretax_margin_bp", "production_pct",
                   "product_sales_pct", "chem_pct", "eps_q", "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    eps_note = (f"; EPS {latest['eps_note']}" if latest.get("eps_note") else "") + (f"; {latest['deal_note']}" if latest.get("deal_note") else "")
    volumes = (f"Volumes: oil-equivalent production {latest['production_pct']:+.1f}% ('{latest['production_note']}'); "
               f"petroleum product sales {latest['product_sales_pct']:+.1f}%; chemical prime product sales {latest['chem_pct']:+.1f}%; "
               f"revenue {latest['sales_pct']:+.1f}% as reported ({latest['sales_note']}){eps_note}")
    fy_rev = rev[max(rev)] * (1 + sum(fwd) / 2 / 100)
    fy_rev_label = f"{fwd_label}, applied to the year (no {fy_now} revenue guide)"
    R = repr
    head = f'''#!/usr/bin/env python3
"""
XOM Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: XOM)  ·  {h["business_line"]}
Generated by retro/build_xom.py from retro/facts/XOM.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "XOM"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); integrated oil and gas signals")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts above.
PIT_PROFILE = {{
    "kind": "CYCLICAL",
    "risk": 2,
    "why": {R(why)},
    "theme_watch": {R(watch)},
    "evidence": {R(list(dict.fromkeys(e["id"] for e in events)))},
}}

# ── FACTS: market (prices truncated at AS_OF, as traded on each day) ──────────
CURRENT_PRICE   = {close:.2f}   # USD, {exchange} close {as_of}
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2
PE_PCTL         = {R(pctl)}   # current-FY P/E over the window below
PE_NOW_PCTL     = {pe_now_pctl}    # share of those daily P/Es at or below the AS_OF one
WINDOW_LABEL    = {R(window_label)}   # P/E window: {window[0]} .. AS_OF
YEARLY_MIN_PE   = {R(yearly)}   # (calendar year, lowest P/E, date)
VOL_ANNUAL_PCT  = {vol:.3f}   # 1-yr realized, daily log returns
VOL_BETA        = {beta:.2f}    # 1-yr beta vs S&P 500
VOL_52W_LOW     = {low52:.2f}
VOL_52W_HIGH    = {high52:.2f}
REF_LOW         = {px[ref][2]:.2f}   # lowest close of the last 52 weeks, {ref}
REF_LOW_LABEL   = {R(MONTHS[int(ref[5:7]) - 1])}

# ── FACTS: company history ({", ".join(h["sources"])}, vintage {h["published"]}{h["extended"]}) ──
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}{"; " + h["split_note"] if h.get("split_note") else ""}
REVENUE_HIST  = {R(rev)}   # total revenues and other income, USD bn
SHARES_HIST   = {R({y: round(v, 1) for y, v in shares.items()})}   # diluted, millions, on the AS_OF share basis
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_pretax_margin"]}   # pre-tax margin, {h["prev_fy_pretax_margin_note"]}
CHECK_PRETAX_MARGIN = {h["prev_fy_pretax_margin"]}   # the same, for the EPS check
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_PRODUCTION = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # no revenue guide: the latest quarter's revenue growth, as reported
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no margin guide, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {fy_rev:.2f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenue {h['prev_fy_sales_growth']:+.1f}%, oil-equivalent production {h['prev_fy_production_pct']:+.1f}% ({h['prev_fy_production_note']}); {latest['quarter'].split()[0]} pre-tax margin {latest['pretax_margin']:.2f}% ({latest['pretax_margin_bp']:+.0f}bp)")}
BALANCE_TEXT    = {R(f"Cash and cash equivalents ${latest['cash_b']:.2f}B, {h['fcf_label']} free cash flow ${h['fcf_b']:.2f}B, dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
VOLUMES_TEXT    = {R(volumes)}
CAPITAL_RETURN  = {R(latest["cash_return_text"])}
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
    return tag, latest["quarter"], stage


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dates", nargs="*")
    ap.add_argument("--weekly", nargs=2, metavar=("START", "END"))
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/XOM)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("XOM"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<34}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
