#!/usr/bin/env python3
"""
Build BKR retrospective models from the dated fact sheet (retro/facts/BKR.json).

The BKR sibling of build_xom.py: the same frozen rules (retro method r2), the same weekly dates and the same market statistics,
with oilfield services signals (retro/templates/bkr_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF (Baker Hughes did not split after 1990, so Yahoo's
     split-adjusted series is the price as traded),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

The company of 2007-2017 is Baker Hughes Incorporated, listed on the NYSE as BHI, to its last weekly date (2017-06-30; the
combination with GE's oil and gas business closed on 2017-07-03, retro/README.md, "BKR 2014-2017"). BKR is the series key (TICKER, the folder, the
index) and the symbol under which Yahoo serves the price history; every printed line names the listing of the date
(LISTED_SYMBOL = "BHI"; retro/README.md, "BKR").

From 2017-07-05 the listed company is Baker Hughes, a GE company (BHGE; Baker Hughes Company, BKR, from October 2019), whose
financial statements are GE Oil & Gas's before the closing. It is built as a new listing (build_bhge below; retro/README.md,
"BKR 2018-2021"): its own vintages, prints and rule-T values (the fact sheet's entries with "era": "bhge" and 'rule_t_bhge'), its own
engine (retro/templates/bkr2_engine.py.tmpl: orders, revenue, gross, segment and operating margin), the P/E window from the listing
(the listing rule of method r2) and the bounds rule for a history of one year. Nothing of Baker Hughes Incorporated's history, prints,
dividends or thresholds enters those models. No date can be built until a full year of the new company's EPS is public (the Q4 2018
release, 2019-01-31): 2017 is a loss for July 3 to December 31 and not a full year.

Baker Hughes' fiscal year is the calendar year from 1998 (fiscal 1997 ended September 30, 1997). It gives no EPS, total-revenue or
margin guidance in numbers in any filing of 2007-2009, so the no-guide rules of method r2 apply on every date (retro/README.md, "BKR"):
  - current-FY EPS: the last full year's EPS stands (the rollover rule, as for UNP, NKE and XOM),
  - forward revenue growth: the latest quarter's total revenue growth, as reported (the UNP and XOM rule),
  - guided margin step: none; the margin signal uses the latest quarter's change in operating margin.
Each release's Outlook section guides revenue outside North America (in words, or as a range for the year or the next quarter),
corporate expenses, capital expenditures, depreciation and the tax rate; it is kept on the print ('outlook') and shown in the
guide line, display only: it guides a region, not the company's revenue. The 2009 releases have no Outlook section.
EPS is diluted EPS from continuing operations before extraordinary items and the cumulative effect of accounting changes, each year
from the latest filing that reports it, and the company's operating profit per diluted share replaces it where a filing publishes
one (the ACN rule). 1998, a loss with no published figure excluding its charges, is excluded; the history and the P/E window start
with 1999 (the ACN FY02 and AAPL FY2002 rule; 'pe_window_start'). 2015 and 2016, losses even on the company's adjusted figures, are
excluded as later years (the XOM FY2020 note: 'eps_excluded'; their days leave the P/E window and FY14's EPS stands). No disruption
theme in scope is live for an oilfield services company (ENERGY_TRANSITION, live from 2015-12-12, is scoped to reserves and refining),
so the events list must stay empty until an encoding is decided.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. Baker Hughes' earnings 8-Ks of 2007-2009 were accepted before the open on the release day; a print
released before the open on the week's last trading day meets that day's close (release_time).

Output goes to staging/retrospective/BKR until the series is added to the archive (--out archive/retrospective/BKR).

Usage
  python3 retro/build_bkr.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_bkr.py --weekly 2009-01-05 2009-12-31
  python3 retro/build_bkr.py --weekly 2010-01-04 2013-12-31
  python3 retro/build_bkr.py --weekly 2014-01-01 2017-06-30
  python3 retro/build_bkr.py --weekly 2019-01-28 2021-12-31      # the new company: 153 dates, 2019-02-01 .. 2021-12-31
  python3 retro/build_bkr.py 2008-01-31
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/BKR/<AS_OF>
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
from build_unp import money  # noqa: E402

FACTS = os.path.join(HERE, "facts", "BKR.json")
ENGINE = os.path.join(HERE, "templates", "bkr_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "BKR")
SYMBOL = "BKR"                 # the series key and Yahoo's symbol for the price history
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"na_rev": (-42, -14, 14, 31), "intl_rev": (-64, -27, 11, 22), "revenue": (-58, -23, 12, 26),
                     "gross_margin": (-670, -300, 60, 640), "op_margin": (-2440, -1060, 330, 750)}
RULE_T_KEYS = {"na_rev": (1, False), "intl_rev": (1, False), "revenue": (1, False), "gross_margin": (10, False),
               "op_margin": (10, False)}           # (rounding unit, lower is better)
PRINT_KEYS = {"quarter", "fy", "q", "published", "source", "release", "release_time", "period_end", "raw", "sales_note", "na_note",
              "intl_note", "margin_note", "eps_q", "eps_q_prior", "eps_note", "diluted_shares_m", "cash_b", "cash_note", "capex_note",
              "next_print", "cash_return_text", "sales_b", "sales_pct", "na_pct", "intl_pct", "gross_margin", "gross_margin_bp",
              "op_margin", "op_margin_bp", "rig_note", "outlook", "fy_actual", "extra_sources", "pro_forma", "basis_note"}
# the guide fields this builder has an encoding for: an 8-K's outlook for one quarter, display only (retro/README.md, "BKR 2010-2013")
GUIDE_KEYS = {"fy", "published", "source", "doc", "quarter", "display"}
# ── the company listed on 2017-07-05 (Baker Hughes, a GE company; Baker Hughes Company): its own engine, thresholds and encodings ──
ERA2 = "bhge"
ENGINE2 = os.path.join(HERE, "templates", "bkr2_engine.py.tmpl")
ENGINE2_THRESHOLDS = {"orders": (-63, -27, 10, 55), "revenue": (-50, -20, 9, 33), "gross_margin": (-770, -470, -170, 120),
                      "seg_margin": (-710, -510, -310, 190), "op_margin": (-2640, -1330, -20, 580)}
RULE_T2_KEYS = {"orders": (1, False), "revenue": (1, False), "gross_margin": (10, False), "seg_margin": (10, False), "op_margin": (10, False)}
PRINT2_KEYS = {"era", "quarter", "fy", "q", "published", "source", "release", "release_time", "period_end", "raw", "sales_note", "orders_note",
               "seg_note", "margin_note", "segments_note", "eps_q", "eps_q_prior", "eps_note", "diluted_shares_m", "cash_b", "cash_note",
               "capex_note", "rpo_note", "next_print", "cash_return_text", "sales_b", "sales_pct", "orders_pct", "gross_margin", "gross_margin_bp",
               "seg_margin", "seg_margin_bp", "op_margin", "op_margin_bp", "fy_actual", "extra_sources", "basis_note"}
FY2_KEYS = {"fy", "fy_label", "eps_normalized", "excluded_note", "revenue_usd_b", "diluted_shares_m", "normalization_note", "op_margin",
            "op_margin_note", "sales_growth", "sales_note", "orders_pct", "orders_note", "check_pretax_margin", "check_pretax_note", "tax_rate",
            "tax_note", "groups", "groups_basis", "one_off_test"}
GUIDE2_KEYS = GUIDE_KEYS | {"era"}
SEGMENTS2 = ("ofs", "ofe", "tps", "ds")


def fiscal_year_end(n):
    """Baker Hughes' fiscal year n is the calendar year n from 1998."""
    return dt.date(n, 12, 31)


def fiscal_year(day):
    return dt.date.fromisoformat(day).year


def rule_t(rt, keys=RULE_T_KEYS):
    """Rule T thresholds from the annual values: XBULL best, BULL median, BASE worst, BEAR one median-to-worst step beyond
    the worst; rounded half up to whole percent and to 10 bp."""
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
    """Re-derive a print's growth rates and margins from its raw published figures (they must match the fact sheet)."""
    assert set(p) <= PRINT_KEYS, (p["quarter"], sorted(set(p) - PRINT_KEYS), "a print field with no encoding yet; decide one first")
    r = p["raw"]
    pct = lambda a, b: (b / a - 1) * 100
    gm = lambda rev, c, s, e: (rev - c - s - e) / rev * 100
    g1, g0 = gm(r["rev_m"], r["cos_m"], r["cosr_m"], r["rne_m"]), gm(r["rev_prior_m"], r["cos_prior_m"], r["cosr_prior_m"], r["rne_prior_m"])
    o1, o0 = r["oi_m"] / r["rev_m"] * 100, r["oi_prior_m"] / r["rev_prior_m"] * 100
    want = {"sales_b": round(r["rev_m"] / 1000, 4), "sales_pct": round(pct(r["rev_prior_m"], r["rev_m"]), 1),
            "na_pct": round(pct(r["na_prior_m"], r["na_m"]), 1),
            "intl_pct": round(pct(r["oilfield_prior_m"] - r["na_prior_m"] - r.get("ind_prior_m", 0),
                                  r["oilfield_m"] - r["na_m"] - r.get("ind_m", 0)), 1),
            "gross_margin": round(g1 + 0.0, 2), "gross_margin_bp": round((g1 - g0) * 100, 1),
            "op_margin": round(o1 + 0.0, 2), "op_margin_bp": round((o1 - o0) * 100, 1)}
    for k, v in want.items():
        assert abs(p[k] - v) < 1e-9, (p["quarter"], k, p[k], v)


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    # Baker Hughes Incorporated traded to the close of 2017-07-03; from the listing of Baker Hughes, a GE company the date is the new
    # company's (its own vintages, prints, thresholds and engine; retro/README.md, "BKR 2018-2021")
    if facts.get("listing") and as_of > facts["listing"]["last_day_predecessor"]:
        return build_bhge(as_of, facts, raw, spx, out)
    chart = retro_tool.chart(SYMBOL)
    assert retro_tool.split_factor(chart, as_of) == 1.0, "a split after AS_OF needs its encoding first (prices on the AS_OF share basis)"
    assert not chart.get("events", {}).get("splits") and not facts.get("splits"), "a split needs its encoding first (the UNP rule)"
    px = dict(raw)
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    # Baker Hughes gives no EPS, revenue or margin guidance in numbers; its outlook bullets live on the prints (display only), and an 8-K's
    # outlook for one quarter is a display-only guide (from 2011)
    for g in [g for g in facts["guides"] if g["published"] <= as_of]:
        assert set(g) <= GUIDE_KEYS, (g["doc"], "a guide field with no encoding yet; decide one first")
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        check_print(p)
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    # prints published by AS_OF that report a fiscal year after the history (a Q4 print reports the year just ended, so it stays
    # in scope after the 10-K that follows it)
    # a year excluded from the EPS history ('eps_excluded': a loss even on the company's figure; retro/README.md, "BKR 2014-2017", the XOM
    # FY2020 note of method r2) is still reported (the NKE FY2018 rule)
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    prints = [p for p in facts["prints"] if p["published"] <= as_of and guide_fy(p) >= first_fy]
    # no disruption theme in taxonomy_eras.json is live for an oilfield services company in 2008-2009 (ENERGY_TRANSITION, scoped
    # to oil, gas and coal reserves and refining, is live from 2015-12-12); the 10-K's greenhouse-gas wording stays in the 'why'
    # (the PEP obesity rule). Any event needs its encoding decided first
    events = [e for e in facts["events"] if e["published"] <= as_of]
    if events:
        sys.exit(f"{as_of}: the BKR builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is public yet")
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage
    h = {**h, "extended": ""}
    for p in prints:
        a = p.get("fy_actual")
        if a and a["fy"] not in reported(h):          # the 10-K vintage, once out, wins
            y = str(a["fy"])
            # an earlier year's company figure first published on a new basis in this release ('restates') replaces it until the next
            # 10-K vintage (the XOM encoding; the Q4 2012 release's 2011 from continuing operations)
            eps_n = {**h["eps_normalized"], **({y: a["eps_normalized"]} if a["eps_normalized"] is not None else {})}
            if a["eps_normalized"] is None:           # an excluded year: reported, but out of the EPS history
                h.update(eps_excluded={**h.get("eps_excluded", {}), y: a["excluded_note"]})
            for yy, e in a.get("restates", {}).items():
                assert yy in eps_n, (p["quarter"], yy, "restates a year outside the history")
                eps_n[yy] = e
            h.update(fy_label=a["fy_label"],
                     eps_normalized=eps_n,
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]},
                     diluted_shares_m={**h["diluted_shares_m"], y: a["diluted_shares_m"]},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_op_margin=a["op_margin"], prev_fy_op_margin_note=a["op_margin_note"],
                     prev_fy_sales_growth=a["sales_growth"], prev_fy_na_pct=a["na_pct"], prev_fy_na_note=a["na_note"],
                     check_pretax_margin=a["check_pretax_margin"], check_pretax_note=a["check_pretax_note"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     groups=a["groups"], groups_basis=a["groups_basis"],
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    latest = prints[-1]
    # the previous quarter is the print published just before the latest one (in or out of the history's scope); before the
    # first print in the fact sheet, the vintage names it
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    i = public.index(latest)
    prev = (public[i - 1]["na_pct"], public[i - 1]["quarter"]) if i > 0 else (h["prev_q_na_pct"], h["prev_q_label"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    excluded = {int(k): v for k, v in h.get("eps_excluded", {}).items()}
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)        # the last full year in the history: cur_fy - 1 unless that year is excluded
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── no guide in numbers: the last full year's EPS stands, and BASE takes the latest quarter's revenue growth ──
    eps_now = eps_hist[last_fy]
    eps_label = f"{fy_e}: no EPS guide in numbers, FY{last_fy % 100:02d}'s ${money(eps_now)} stands" + "".join(
        f" (FY{y % 100:02d} is excluded: {excluded[y]})" for y in range(last_fy + 1, cur_fy))
    fwd = [latest["sales_pct"]] * 2
    fwd_label, fwd_short, fwd_period = (f"no {next_q} revenue guide, {latest['quarter']} revenue as reported",
                                        f"{latest['quarter'][:2]} revenue", latest["quarter"])
    outlook = latest.get("outlook")
    # an 8-K's outlook for the quarter not yet reported, display only (method r2 has no input for it)
    gq = [g for g in facts["guides"] if g["published"] <= as_of and g.get("quarter") == next_q and g["published"] > latest["published"]]
    g_text = "".join(f"; the {g['doc']} on {g['quarter']}, display only: '{g['display']}'" for g in gq)
    if outlook:
        guide_text = (f"{fy_now}: no EPS, revenue or margin guide in numbers (BASE takes {latest['quarter']} revenue growth); the "
                      f"{latest['quarter']} release's outlook for revenue outside North America, display only (it guides a region, not "
                      "the company's revenue): " + " ".join(f"'{o}'" for o in outlook))
    else:
        guide_text = (f"{fy_now}: no guide in numbers (BASE takes {latest['quarter']} revenue growth); the {latest['quarter']} release "
                      "has no Outlook section")
    guide_text += g_text
    margin_guided = False                          # no operating-margin guide in numbers: no guided step
    fy_margin_base = h["prev_fy_op_margin"]

    # ── dividend: the latest declared rate ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts["dividends"] if d["published"] <= as_of]
    divs.append((h["published"], h["dividend_annual"], h["dividend_note"], None))
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
    # an excluded year's own days leave the window (the r2 rule's "the window starts after it", for a year that is not the first)
    gone = sorted({fy(d) for d in window} & set(excluded))
    window = [d for d in window if fy(d) not in excluded]
    assert all(fy(d) in eps for d in window), (as_of, "P/E window needs EPS for every fiscal year")
    years = (dt.date.fromisoformat(as_of) - dt.date.fromisoformat(window[0])).days / 365.25
    window_label = ("10-yr" if years > 9.9 else f"{years:.1f}-yr") + "".join(f" ex-FY{y % 100:02d}" for y in gone)
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

    # ── era-dependent text, from facts only: no disruption theme in scope for an oilfield services company ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
    key_tail = ("Activity drives revenue, by the company's own account; the bear needs\n"
                "  customers' spending to fall, not only the rig count.")
    theme_summary = "no disruption theme has dated evidence"
    why = h["why"]
    # ENERGY_TRANSITION is live from 2015-12-12 and scoped to oil, gas and coal reserves and refining, which an oilfield services company
    # does not hold (retro/README.md, "BKR 2014-2017"): from its live date the texts say so, and the greenhouse-gas wording stays in the
    # "why" (the PEP obesity rule). From the FY2013 vintage the "why" ends with a clause that follows the theme's status on AS_OF
    # ('why_theme_tail'); the earlier vintages keep their text, so those dates rebuild byte-identical
    et = retro_tool.load_taxonomy()["themes"]["ENERGY_TRANSITION"]
    et_live = et["live_from"] <= as_of
    if et_live:
        sig_name, trigger = "Disruption theme: none in scope", "No live disruption theme covers oilfield services"
        theme_summary = (f"ENERGY_TRANSITION is live from {et['live_from']} but scoped to oil, gas and coal reserves and refining; no theme "
                         "in scope has dated evidence")
    if h.get("why_theme_tail"):
        why += ("; ENERGY_TRANSITION is live from " + et["live_from"] + " but scoped to oil, gas and coal reserves and refining, which an "
                "oilfield services company does not hold, so the greenhouse-gas wording stays here" if et_live else
                "; no disruption theme is live for an oilfield services company, so the greenhouse-gas wording stays here")
    kind, pit_risk = "CYCLICAL", 2
    cat3 = (f"(3) A {fy_now} guide — none in numbers: Baker Hughes guides revenue outside North America, not EPS or total revenue"
            + (f" ({latest['quarter']} outlook: '{outlook[0]}')" if outlook else f"; the {latest['quarter']} release has no Outlook section"))
    cat4 = f"(4) Capital expenditures — {latest['capex_note']}"

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    # a print dated AS_OF meets AS_OF's close only if it was public before the open (the week's last trading day)
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    renames = [n for n in facts.get("company_names", []) if h["published"] < n["published"] <= as_of]
    company = renames[-1]["name"] if renames else h["company"]
    exchange, listed = h["exchange"], h["symbol"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])]
           + ([dividend_src] if dividend_src else []) + [n["source"] for n in renames] + [g["source"] for g in gq])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "A0", "published": as_of,
                    "title": f"Yahoo Finance daily prices, Baker Hughes common stock ({exchange}: {listed}) and S&P 500, truncated at AS_OF",
                    "url": f"https://finance.yahoo.com/quote/{SYMBOL}/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "na_pct", "intl_pct", "gross_margin", "gross_margin_bp",
                   "op_margin", "op_margin_bp", "eps_q", "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    eps_note = f"; EPS {latest['eps_note']}" if latest.get("eps_note") else ""
    activity = (f"Activity: North America {latest['na_pct']:+.1f}% ({latest['na_note']}); outside North America {latest['intl_pct']:+.1f}% "
                f"({latest['intl_note']}); revenue {latest['sales_pct']:+.1f}% as reported ({latest['sales_note']})"
                + (f"; the release on the rig count: '{latest['rig_note']}'" if latest.get("rig_note") else "") + eps_note
                + (f"; basis: {latest['basis_note']}" if latest.get("basis_note") else ""))
    pf = latest.get("pro_forma")
    if pf:                                         # the release's pro forma combined table, display only (acquisitions stay in growth)
        pint = lambda d: d["rev_m"] - d["na_m"] - d["ind_m"]
        pint0 = lambda d: d["rev_prior_m"] - d["na_prior_m"] - d["ind_prior_m"]
        activity += (f"; pro forma combined with BJ Services (the release's own table, display only): revenue "
                     f"{(pf['rev_m'] / pf['rev_prior_m'] - 1) * 100:+.1f}%, North America {(pf['na_m'] / pf['na_prior_m'] - 1) * 100:+.1f}%, "
                     f"outside North America {(pint(pf) / pint0(pf) - 1) * 100:+.1f}%")
    fy_rev = rev[max(rev)] * (1 + sum(fwd) / 2 / 100)
    fy_rev_label = f"{fwd_label}, applied to the year (no {fy_now} revenue guide)"
    R = repr
    head = f'''#!/usr/bin/env python3
"""
{listed} Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: {listed})  ·  {h["business_line"]}
Generated by retro/build_bkr.py from retro/facts/BKR.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "{SYMBOL}"   # series key
LISTED_SYMBOL = "{listed}"   # the listing on AS_OF
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); oilfield services signals")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts above.
PIT_PROFILE = {{
    "kind": "{kind}",
    "risk": {pit_risk},
    "why": {R(why)},
    "theme_watch": {R(watch)},
    "evidence": [],
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
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}
REVENUE_HIST  = {R(rev)}   # revenues, USD bn
SHARES_HIST   = {R({y: round(v, 1) for y, v in shares.items()})}   # diluted, millions
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # operating margin, {h["prev_fy_op_margin_note"]}
CHECK_PRETAX_MARGIN = {h["check_pretax_margin"]}   # {h["check_pretax_note"]}
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_NA         = {R(prev)}
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
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenue {h['prev_fy_sales_growth']:+.1f}%, North America {h['prev_fy_na_pct']:+.1f}% ({h['prev_fy_na_note']}); {latest['quarter'].split()[0]} operating margin {latest['op_margin']:.2f}% ({latest['op_margin_bp']:+.0f}bp)")}
BALANCE_TEXT    = {R(f"Cash and short-term investments ${latest['cash_b']:.2f}B, {h['fcf_label']} free cash flow ${h['fcf_b']:.2f}B, dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
ACTIVITY_TEXT   = {R(activity)}
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


def check_print2(p):
    """Re-derive a print of the company listed on 2017-07-05 from its raw published figures (they must match the fact sheet)."""
    assert set(p) <= PRINT2_KEYS, (p["quarter"], sorted(set(p) - PRINT2_KEYS), "a print field with no encoding yet; decide one first")
    r = p["raw"]
    pct = lambda a, b: (b / a - 1) * 100
    gm = lambda rev, cor: (rev - cor) / rev * 100
    g1, g0 = gm(r["rev_m"], r["cor_m"]), gm(r["rev_prior_m"], r["cor_prior_m"])
    s1, s0 = r["segoi_m"] / r["rev_m"] * 100, r["segoi_prior_m"] / r["rev_prior_m"] * 100
    o1, o0 = r["oi_m"] / r["rev_m"] * 100, r["oi_prior_m"] / r["rev_prior_m"] * 100
    want = {"sales_b": round(r["rev_m"] / 1000, 4), "sales_pct": round(pct(r["rev_prior_m"], r["rev_m"]), 1),
            "orders_pct": round(pct(r["orders_prior_m"], r["orders_m"]), 1),
            "gross_margin": round(g1 + 0.0, 2), "gross_margin_bp": round((g1 - g0) * 100, 1),
            "seg_margin": round(s1 + 0.0, 2), "seg_margin_bp": round((s1 - s0) * 100, 1),
            "op_margin": round(o1 + 0.0, 2), "op_margin_bp": round((o1 - o0) * 100, 1)}
    for k, v in want.items():
        assert abs(p[k] - v) < 1e-9, (p["quarter"], k, p[k], v)
    for suffix in ("_m", "_prior_m"):               # the four segments make the revenue (rounded figures: within 2)
        assert abs(sum(r[k + suffix] for k in SEGMENTS2) - r["rev" + suffix]) <= 2, (p["quarter"], suffix)
    a = p.get("fy_actual")
    if a:
        assert set(a) <= FY2_KEYS, (p["quarter"], sorted(set(a) - FY2_KEYS), "a full-year field with no encoding yet; decide one first")
        # the release gives the Class A share count only; the history's counts (Class A plus Class B) stay the 10-K's
        assert a["diluted_shares_m"] is None, (p["quarter"], "a full-year share count needs its encoding first")
        t = a.get("one_off_test")
        if a["eps_normalized"] is not None or t:    # a year kept at GAAP, or excluded as distorted: the test's own figures decide
            assert sum(t["items_attributable_m"]) == t["items_total_m"], (p["quarter"], "the one-off test's items do not sum")
            assert (t["items_total_m"] > t["net_income_attributable_m"]) == t["distorted"] == (a["eps_normalized"] is None), (
                p["quarter"], "the year's EPS and the one-off test disagree")


def build_bhge(as_of, facts, raw, spx, out):
    """A date of the company listed on 2017-07-05 (Baker Hughes, a GE company; Baker Hughes Company): the same frozen rules on its
    own facts, with the listing rule (the P/E window runs from the listing) and the bounds rule (a history of one year)."""
    listing = facts["listing"]
    first_day = listing["first_trading_day"]
    assert listing["published"] <= as_of and first_day <= as_of
    with open(ENGINE2, encoding="utf-8") as fh:
        engine = fh.read()
    chart = retro_tool.chart(SYMBOL)
    assert retro_tool.split_factor(chart, as_of) == 1.0, "a split after AS_OF needs its encoding first (prices on the AS_OF share basis)"
    assert not chart.get("events", {}).get("splits") and not facts.get("splits"), "a split needs its encoding first (the UNP rule)"
    px = dict(raw)
    era = lambda x: x.get("era") == ERA2
    vintages = [v for v in facts["history_vintages"] if era(v) and v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: Baker Hughes Incorporated's last trading day was {listing['last_day_predecessor']}; no annual history of the company "
                 f"listed on {first_day} is in the fact sheet for this date (and none of its years has a full year of EPS before the Q4 2018 release)")
    for v in vintages:                                 # the fiscal calendar the filings state must match the rule
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    # no EPS, revenue or margin guidance in numbers in any filing; an 8-K's figures for one quarter are a display-only guide
    for g in [g for g in facts["guides"] if era(g) and g["published"] <= as_of]:
        assert set(g) <= GUIDE2_KEYS, (g["doc"], "a guide field with no encoding yet; decide one first")
    assert rule_t(facts["rule_t_bhge"], RULE_T2_KEYS) == ENGINE2_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    public = [p for p in facts["prints"] if era(p) and p["published"] <= as_of]
    for p in public:                                   # a print public on AS_OF must match its raw figures
        check_print2(p)
    h = vintages[-1]                                   # latest annual history public on AS_OF
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    prints = [p for p in public if guide_fy(p) >= first_fy]
    events = [e for e in facts["events"] if e["published"] <= as_of]
    if events:
        sys.exit(f"{as_of}: the BKR builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
    if not prints:
        sys.exit(f"{as_of}: no quarterly print of the company listed on {first_day} after FY{first_fy - 1} is in the fact sheet for this date")
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage
    h = {**h, "extended": ""}
    for p in prints:
        a = p.get("fy_actual")
        if a and a["fy"] not in reported(h):          # the 10-K vintage, once out, wins
            y = str(a["fy"])
            eps_n = {**h["eps_normalized"], **({y: a["eps_normalized"]} if a["eps_normalized"] is not None else {})}
            if a["eps_normalized"] is None:           # an excluded year: reported, but out of the EPS history
                h.update(eps_excluded={**h.get("eps_excluded", {}), y: a["excluded_note"]})
            h.update(fy_label=a["fy_label"],
                     eps_normalized=eps_n,
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_op_margin=a["op_margin"], prev_fy_op_margin_note=a["op_margin_note"],
                     prev_fy_sales_growth=a["sales_growth"], prev_fy_orders_pct=a["orders_pct"], prev_fy_orders_note=a["orders_note"],
                     check_pretax_margin=a["check_pretax_margin"], check_pretax_note=a["check_pretax_note"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     groups=a["groups"], groups_basis=a["groups_basis"],
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    latest = prints[-1]
    i = public.index(latest)
    prev = (public[i - 1]["orders_pct"], public[i - 1]["quarter"]) if i > 0 else (h["prev_q_orders_pct"], h["prev_q_label"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    excluded = {int(k): v for k, v in h.get("eps_excluded", {}).items()}
    if not eps_hist:                                   # a loss for half a year is the only year reported: no P/E, no model
        sys.exit(f"{as_of}: no full year of EPS of the company listed on {first_day} is public yet, so the stock has no P/E of its own (method r2)")
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)        # the last full year in the history: cur_fy - 1 unless that year is excluded
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── no guide in numbers: the last full year's EPS stands, and BASE takes the latest quarter's revenue growth ──
    eps_now = eps_hist[last_fy]
    eps_label = f"{fy_e}: no EPS guide in numbers, FY{last_fy % 100:02d}'s ${money(eps_now)} stands" + "".join(
        f" (FY{y % 100:02d} is excluded: {excluded[y]})" for y in range(last_fy + 1, cur_fy))
    fwd = [latest["sales_pct"]] * 2
    fwd_label, fwd_short, fwd_period = (f"no {next_q} revenue guide, {latest['quarter']} revenue as reported",
                                        f"{latest['quarter'][:2]} revenue", latest["quarter"])
    gq = [g for g in facts["guides"] if era(g) and g["published"] <= as_of and g.get("quarter") == next_q and g["published"] > latest["published"]]
    guide_text = (f"{fy_now}: no guide in numbers (BASE takes {latest['quarter']} revenue growth); the {latest['quarter']} release gives no "
                  "outlook in numbers") + "".join(f"; the {g['doc']} on {g['quarter']}, display only: '{g['display']}'" for g in gq)
    margin_guided = False                          # no operating-margin guide in numbers: no guided step
    fy_margin_base = h["prev_fy_op_margin"]

    # ── dividend: the latest declared rate (the predecessor's dividends are another company's) ──
    assert not [d for d in facts["dividends"] if era(d) and d["published"] <= as_of], "a dividend change of the new company needs its encoding first"
    dividend, dividend_note = h["dividend_annual"], h["dividend_note"]

    # ── market statistics, prices truncated at AS_OF, from the listing (the listing rule) ──
    days = sorted(d for d in px if first_day <= d <= as_of)
    close = px[as_of][2]
    assert minus_years(as_of, 1) >= first_day, (as_of, "less than a year since the listing: the 52-week statistics need their encoding first")
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
    assert h["pe_window_start"] == first_day, "the P/E window of the new company runs from its listing"
    window = [d for d in days if d > minus_years(as_of, 10)]
    # an excluded year's own days leave the window (2017, a loss for half a year; a later year distorted or at a loss)
    gone = sorted({fy(d) for d in window} & set(excluded))
    window = [d for d in window if fy(d) not in excluded]
    assert all(fy(d) in eps for d in window), (as_of, "P/E window needs EPS for every fiscal year")
    years = (dt.date.fromisoformat(as_of) - dt.date.fromisoformat(window[0])).days / 365.25
    assert years >= 1, (as_of, "a window under a year needs the trading-day label first (the AVGO encoding)")
    window_label = ("10-yr" if years > 9.9 else f"{years:.1f}-yr") + "".join(f" ex-FY{y % 100:02d}" for y in gone)
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

    # ── era-dependent text, from facts only: ENERGY_TRANSITION is live but scoped to reserves and refining ──
    stage, watch, factors = "none", [], []
    et = retro_tool.load_taxonomy()["themes"]["ENERGY_TRANSITION"]
    assert et["live_from"] <= as_of
    sig_name, trigger = "Disruption theme: none in scope", "No live disruption theme covers oilfield services and equipment"
    theme_summary = (f"ENERGY_TRANSITION is live from {et['live_from']} but scoped to oil, gas and coal reserves and refining; no theme "
                     "in scope has dated evidence")
    key_tail = ("Customers' spending drives revenue, by the company's own account; the bear needs\n"
                "  that spending to fall, not only one quarter's orders.")
    why = h["why"]
    if h.get("why_theme_tail"):
        why += ("; ENERGY_TRANSITION is live from " + et["live_from"] + " but scoped to oil, gas and coal reserves and refining, which an "
                "oilfield services and equipment company does not hold, so the climate-change wording stays here")
    kind, pit_risk = "CYCLICAL", 2
    cat3 = (f"(3) A {fy_now} guide — none in numbers: no filing guides EPS, revenue or a margin; the {latest['quarter']} release on the "
            f"work in hand: '{latest['rpo_note']}'")
    cat4 = f"(4) Capital expenditures — {latest['capex_note']}"

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    # a name or a listing changed since the vintage applies from its date (the ticker symbol BKR, then Nasdaq)
    renames = [n for n in facts.get("company_names", []) if h["published"] < n["published"] <= as_of]
    company = renames[-1]["name"] if renames else h["company"]
    moved = [x for x in facts.get("listings", []) if h["published"] < x["published"] <= as_of and x["effective"] <= as_of]
    exchange, listed = (moved[-1]["exchange"], moved[-1].get("symbol", h["symbol"])) if moved else (h["exchange"], h["symbol"])
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])]
           + [n["source"] for n in renames] + [x["source"] for x in moved] + [g["source"] for g in gq])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "A0", "published": as_of,
                    "title": f"Yahoo Finance daily prices, {company} Class A common stock ({exchange}: {listed}) and S&P 500, truncated at AS_OF",
                    "url": f"https://finance.yahoo.com/quote/{SYMBOL}/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution "
                                f"since the listing on {first_day}"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "orders_pct", "gross_margin", "gross_margin_bp", "seg_margin", "seg_margin_bp",
                   "op_margin", "op_margin_bp", "eps_q", "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    activity = (f"Activity: orders {latest['orders_pct']:+.1f}% ({latest['orders_note']}); revenue {latest['sales_pct']:+.1f}% as reported "
                f"({latest['sales_note']}); by segment: {latest['segments_note']}; {latest['seg_note']}; {latest['margin_note']}; "
                f"EPS {latest['eps_note']}" + (f"; basis: {latest['basis_note']}" if latest.get("basis_note") else ""))
    fy_rev = rev[max(rev)] * (1 + sum(fwd) / 2 / 100)
    fy_rev_label = f"{fwd_label}, applied to the year (no {fy_now} revenue guide)"
    fcf_text = f"${h['fcf_b']:.2f}B" if h["fcf_b"] >= 0 else f"$({-h['fcf_b']:.2f})B"
    R = repr
    head = f'''#!/usr/bin/env python3
"""
{listed} Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: {listed})  ·  {h["business_line"]}
Generated by retro/build_bkr.py from retro/facts/BKR.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "{SYMBOL}"   # series key
LISTED_SYMBOL = "{listed}"   # the listing on AS_OF
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); orders, revenue and margin signals; "
               "the listing and short-history bounds rules")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts above.
PIT_PROFILE = {{
    "kind": "{kind}",
    "risk": {pit_risk},
    "why": {R(why)},
    "theme_watch": {R(watch)},
    "evidence": [],
}}

# ── FACTS: market (prices truncated at AS_OF, as traded on each day, from the listing) ──
LISTING_DATE    = "{first_day}"   # first trading day of the Class A common stock ({listing["exchange"]}: {listing["symbol"]})
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
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}
REVENUE_HIST  = {R(rev)}   # revenue, USD bn (GE Oil & Gas before July 3, 2017)
SHARES_HIST   = {R({y: round(v, 1) for y, v in shares.items()})}   # {h["shares_note"]}
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # operating margin, {h["prev_fy_op_margin_note"]}
CHECK_PRETAX_MARGIN = {h["check_pretax_margin"]}   # {h["check_pretax_note"]}
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}
KIND_TEXT     = {R(h["kind_text"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_ORDERS     = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # no revenue guide: the latest quarter's revenue growth, as reported
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no margin guide, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {fy_rev:.2f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {shares[max(shares)] / 1000:.4f}
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenue {h['prev_fy_sales_growth']:+.1f}%, orders {h['prev_fy_orders_pct']:+.1f}% ({h['prev_fy_orders_note']}); {latest['quarter'].split()[0]} segment operating margin {latest['seg_margin']:.2f}% ({latest['seg_margin_bp']:+.0f}bp)")}
BALANCE_TEXT    = {R(f"Cash and cash equivalents ${latest['cash_b']:.2f}B, {h['fcf_label']} free cash flow {fcf_text}, dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
ACTIVITY_TEXT   = {R(activity)}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/BKR)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series(SYMBOL), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<34}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
