#!/usr/bin/env python3
"""
Build F retrospective models from the dated fact sheet (retro/facts/F.json).

The F sibling of build_xom.py: the same frozen rules (retro method r2), the same weekly dates and the same market statistics,
with automaker signals (retro/templates/f_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints, guides, dividends and events whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF (Ford last split on 2000-08-03, so for every date
     from 2012 Yahoo's split-adjusted close is the price as traded),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Ford's fiscal year is the calendar year. No filing of 2021-2026 guides EPS, revenue or a margin in numbers: the releases guide
company adjusted EBIT and adjusted free cash flow in dollars (display only, the AVGO 2009 and BKR rule), so the no-guide rules of
method r2 apply on every date (retro/README.md, "F"):
  - current-FY EPS: the last full year's EPS stands (the rollover rule),
  - forward revenue growth: the latest quarter's revenue growth, as reported (the UNP rule),
  - guided margin step: none; the margin signal uses the latest quarter's change in the company adjusted EBIT margin.
EPS is the company's adjusted EPS (diluted, excluding pre-tax and tax special items) from the latest filing that publishes it, else
GAAP diluted EPS (the ACN rule); 2011 is excluded (a year distorted by its $12.4 billion valuation-allowance release with no
after-tax figure without it), so the FY2020 vintage's history and P/E window start in 2012. Every earnings 8-K of 2021-2026 was
accepted after the close and its 10-Q or 10-K the same evening, so a Q4 print and its 10-K share one date and a Q4 print never
extends the history (the fact sheet has no 'fy_actual'). The one event kind encoded: each 10-K's risk factor on a shift in demand
away from Ford's larger combustion-engine vehicles (ev_company_acknowledged) puts EV on the watch list, company-acknowledged with no
market read: text only (the MSFT CLOUD rule). No market evidence names Ford, so the stock is never re-filed.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where
it is the first trading day after the print became public (a print dated the week's last trading day meets that day's close: it was
public before the open, release_time).

Output goes to staging/retrospective/F until the series is added to the archive (--out archive/retrospective/F).

Usage
  python3 retro/build_f.py --weekly 2022-01-03 2026-11-08
  python3 retro/build_f.py 2022-02-04
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/F/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "F.json")
ENGINE = os.path.join(HERE, "templates", "f_engine.py.tmpl")
ENGINE08 = os.path.join(HERE, "templates", "f08_engine.py.tmpl")      # dates before ERA_2022 (retro/README.md, F 2008 era)
ERA_2022 = "2022-01-01"             # the first series built (2022-2026) starts here, with the FY2011-FY2020 rule-T decade
OUT = os.path.join(ROOT, "staging", "retrospective", "F")
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"wholesales": (-44, -22, 0, 12), "ford_credit": (-46, -29, -13, 14), "revenue": (-39, -18, 2, 10),
                     "adj_eps": (-122, -66, -9, 233), "margin": (-220, -190, -150, -30)}
# the guide fields this builder has an encoding for: a full-year adjusted EBIT outlook quoted from a filing, display only
GUIDE_KEYS = {"fy", "published", "source", "doc", "quote", "note"}
RULE_T_KEYS = {"wholesales": (1, False), "ford_credit": (1, False), "revenue": (1, False), "adj_eps": (1, False),
               "margin": (10, False)}           # (rounding unit, lower is better)


def fiscal_year_end(n):
    """Ford's fiscal year n is the calendar year n."""
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
    """Re-derive a print's growth rates and margin change from its raw published figures (they must match the fact sheet)."""
    r = p["raw"]
    pct = lambda a, b: round((b / a - 1) * 100, 1)
    want = {"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": pct(r["rev_prior_m"], r["rev_m"]),
            "ws_pct": pct(r["ws_prior_k"], r["ws_k"]), "fc_pct": pct(r["fc_ebt_prior_m"], r["fc_ebt_m"]),
            "margin_bp": round((p["margin"] - p["margin_prior"]) * 100),
            "eps_pct": pct(p["eps_q_prior"], p["eps_q"]) if p["eps_q_prior"] > 0 else None}
    for k, v in want.items():
        assert p[k] == v or abs(p[k] - v) < 1e-9, (p["quarter"], k, p[k], v)


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    chart = retro_tool.chart("F")
    fx = retro_tool.split_factor(chart, as_of)
    assert fx == 1.0, "a split after 2000-08-03 needs its encoding first (prices on the AS_OF share basis, the UNP rule)"
    assert not [x for x in facts.get("splits", []) if x["published"] <= as_of], "the F builder has no split encoding"
    px = dict(raw)
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    for g in [g for g in facts["guides"] if g["published"] <= as_of]:
        assert set(g) <= GUIDE_KEYS, (g["doc"], "a guide field with no encoding yet; decide one first")
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    # a Q4 print's 10-K is public the same day (both after the close), so no print extends the history: none carries actuals
    # (the prints of the early era, before 2021, have their own encoding and checks: build_r2008)
    era = [p for p in facts["prints"] if p["published"] <= as_of and p["fy"] >= 2021]
    assert not any("fy_actual" in p for p in era), "a Q4 print with full-year actuals needs its encoding first"
    for p in era:  # a print public on AS_OF must match its raw figures
        check_print(p)
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    # a year excluded from the EPS history (eps_excluded, the AVGO FY2018 mirror test: FY2011) is still reported
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["q"] == 4 else 0)
    prints = [p for p in facts["prints"] if p["published"] <= as_of and guide_fy(p) >= first_fy]
    # a 10-K's wording (an event with a 'doc') is replaced by the next 10-K; the one encoded kind is the 10-K's EV risk factor
    events = [e for e in facts["events"] if e["published"] <= as_of and (h["published"] <= e["published"] or "doc" not in e)]
    if any(e["kind"] != "ev_company_acknowledged" for e in events):
        sys.exit(f"{as_of}: the F builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
    themes = retro_tool.load_taxonomy()["themes"]
    events = [e for e in events if themes[e["theme"]]["live_from"] <= as_of]
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is public yet")
    latest = prints[-1]
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    i = public.index(latest)
    prev = (public[i - 1]["ws_pct"], public[i - 1]["quarter"]) if i > 0 else (h["prev_q_ws_pct"], h["prev_q_label"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    excluded = {int(k): v for k, v in h.get("eps_excluded", {}).items()}
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── no guide in numbers: the last full year's EPS stands, and BASE takes the latest quarter's revenue growth ──
    eps_now = eps_hist[last_fy]
    eps_label = f"{fy_e}: no EPS guide in numbers, FY{last_fy % 100:02d}'s ${money(eps_now)} (company adjusted) stands"
    fwd = [latest["sales_pct"]] * 2
    fwd_label, fwd_short, fwd_period = (f"no {next_q} revenue guide, {latest['quarter']} revenue as reported",
                                        f"{latest['quarter'][:2]} revenue", latest["quarter"])
    # the latest full-year adjusted EBIT outlook for the current year, display only
    gp = next((g for g in reversed([g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy])), None)
    if gp:
        guide_text = (f"{fy_now}: no EPS, revenue or margin guide in numbers (BASE takes {latest['quarter']} revenue growth); "
                      f"full-year outlook ({gp['doc']}, {gp['published']}): '{gp['quote']}' (display only: method r2 has no EBIT input)")
    else:
        guide_text = (f"{fy_now}: no guide in any filing yet (Ford guides adjusted EBIT and free cash flow in dollars, display only; "
                      f"BASE takes {latest['quarter']} revenue growth)")
    margin_guided = False
    fy_margin_base = h["prev_fy_margin"]

    # ── dividend: the latest declared regular rate ──
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

    # ── era-dependent text, from facts only ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none on the watch list", "No disruption theme acknowledged"
    theme_summary = "EV is live but no 10-K risk factor names a shift away from Ford's combustion-engine vehicles yet"
    why = h["why"] + ("; EV (live from about 2020) is not on the watch list: no risk factor of this 10-K names a shift away from "
                      "Ford's combustion-engine vehicles")
    for e in events[-1:]:
        # EV is live from 2020 and scoped to ICE powertrains; the latest 10-K's risk factor puts it on the watch list (the ACN CLOUD
        # rule, as for MSFT and XOM: company-acknowledged, no market read). The factor pair nets to zero and the theme signal stays at
        # 2/4, so only text changes; re-filing needs dated evidence that the market prices EV substitution of Ford's profits
        val_word = "a premium" if pe_now_pctl >= 70 else "a discount to its own history" if pe_now_pctl <= 30 else "near its own median"
        stage = "acknowledged"
        watch = [{"theme": "EV", "status": "live, company-acknowledged; no market read",
                  "reason": (f"Live: Ford's own {e['doc']}, under '{e['heading']}', says '{e['risk_quote']}' Its business: "
                             f"'{e['offering']}'. The stock trades at {close / eps_now:.1f}x {fy_e_s} — {val_word}. "
                             "Re-file as DISRUPTION_EXPOSED (EV) only if dated evidence shows the market pricing electric-vehicle "
                             "substitution of Ford's combustion-engine profits specifically.")}]
        factors = [("Electrified vehicles of its own: Ford sells them as well", 0.2, 0.10),
                    (f"EV shift ({e['doc']}): {e['risk_short']}", -0.2, 0.10)]
        sig_name = "EV shift: net effect on Ford's profit pool"
        trigger = "Demand moves from larger combustion-engine vehicles to less profitable ones faster than Ford adapts"
        theme_summary = "EV is live and company-acknowledged; no dated evidence ties the multiple to it"
        why = h["why"] + ("; EV is live (from about 2020) and its 10-K risk factor puts it on the watch list: company-acknowledged, "
                          "with no dated evidence that the market prices it for Ford")
    kind, pit_risk = "DURABLE", 2
    cat3 = (f"(3) The {fy_now} adjusted EBIT outlook — '{gp['quote']}' ({gp['doc']}; display only): no EPS or revenue guide"
            if gp else f"(3) A {fy_now} outlook — none yet: Ford guides adjusted EBIT in dollars, display only")
    cat4 = (f"(4) Ford Credit EBT — {latest['fc_pct']:+.1f}% in {latest['quarter']} (${latest['raw']['fc_ebt_m']:,.0f}M): "
            "credit losses, lease residuals and funding costs")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    renames = [n for n in facts.get("company_names", []) if h["published"] < n["published"] <= as_of]
    company = renames[-1]["name"] if renames else h["company"]
    exchange = h["exchange"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])]
           + ([dividend_src] if dividend_src else []) + ([gp["source"]] if gp else []) + [e["id"] for e in events]
           + [n["source"] for n in renames])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "A0", "published": as_of, "title": "Yahoo Finance daily prices, F and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/F/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "margin", "margin_bp", "ws_pct", "fc_pct", "eps_q", "eps_q_prior",
                   "eps_pct")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    rw = latest["raw"]
    volumes = (f"Wholesales {latest['ws_pct']:+.1f}% ({rw['ws_prior_k']:,.0f}K to {rw['ws_k']:,.0f}K, {latest['ws_note']}); "
               f"Ford Credit EBT {latest['fc_pct']:+.1f}% (${rw['fc_ebt_prior_m']:,.0f}M to ${rw['fc_ebt_m']:,.0f}M); "
               f"revenue {latest['sales_pct']:+.1f}% as reported; adjusted EPS ${latest['eps_q']:.2f} vs ${latest['eps_q_prior']:.2f} "
               f"(GAAP ${latest['eps_gaap']:.2f} vs ${latest['eps_gaap_prior']:.2f})" + (f"; {latest['q4_note']}" if latest.get("q4_note") else ""))
    fy_rev = rev[max(rev)] * (1 + sum(fwd) / 2 / 100)
    fy_rev_label = f"{fwd_label}, applied to the year (no {fy_now} revenue guide)"
    R = repr
    head = f'''#!/usr/bin/env python3
"""
F Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: F)  ·  {h["business_line"]}
Generated by retro/build_f.py from retro/facts/F.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "F"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); automaker signals")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts above.
PIT_PROFILE = {{
    "kind": "{kind}",
    "risk": {pit_risk},
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

# ── FACTS: company history ({", ".join(h["sources"])}, vintage {h["published"]}) ──
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}
REVENUE_HIST  = {R(rev)}   # total revenues, USD bn
SHARES_HIST   = {R({y: round(v, 1) for y, v in shares.items()})}   # diluted, millions ({h["shares_note"]})
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_margin"]}   # {h["prev_fy_margin_note"]}
CHECK_MARGIN_PCT = {h["prev_fy_margin"]}   # the same, for the EPS check (display only)
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_WHOLESALES = {R(prev)}
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
NEXT_PRINT      = {R(f"{next_q} print")}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenue {h['prev_fy_sales_growth']:+.1f}%, wholesales {h['prev_fy_ws_pct']:+.1f}% ({h['prev_fy_ws_note']}); {latest['quarter']} adjusted EBIT margin {latest['margin']:.1f}% ({latest['margin_bp']:+d}bp)")}
BALANCE_TEXT    = {R(f"Cash and cash equivalents ${latest['cash_b']:.2f}B, {h['fcf_label']} adjusted free cash flow ${h['fcf_b']:.2f}B, dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
VOLUMES_TEXT    = {R(volumes)}
CAPITAL_RETURN  = {R(h["cash_return_text"])}
THEME_FACTORS   = {R(factors)}
THEME_SIGNAL_NAME    = {R(sig_name)}
THEME_SIGNAL_TRIGGER = {R(trigger)}
THEME_SUMMARY        = {R(theme_summary)}
CATALYST_3      = {R(cat3)}
CATALYST_4      = {R(cat4)}
'''
    os.makedirs(os.path.join(out, as_of), exist_ok=True)
    with open(os.path.join(out, as_of, "model.py"), "w", encoding="utf-8") as fh:
        fh.write(head + engine)
    return tag, latest["quarter"], stage


# ═════════════════════════════════════════════════════════════════════════════
# The early era (dates before ERA_2022): retro/README.md, "F 2008-2011". Decided before any of its models was built.
#   - signals: wholesales, Ford Credit pre-tax, revenue (GAAP), EPS excluding special items, the GAAP pre-tax margin change;
#     rule T over 1997-2006 (rule_t_r2008), the engine f08_engine.py.tmpl;
#   - EPS: the company's figure excluding special items from its Q4 releases (the 10-Ks publish none); 2001, a loss on that
#     figure and not the latest year, takes the history and the window with it (pe_window_start 2002-01-01); 2006-2009 are
#     excluded as the latest years (losses, and 2009's $0.00) and stay gaps; a year excluded for want of a positive figure
#     re-enters when a later filing publishes one ('readmits': 2009's $0.01 in the Q4 2010 release);
#   - a Q4 print extends the history from its release to the 10-K (the releases came weeks before the 10-Ks).
# ═════════════════════════════════════════════════════════════════════════════
ENGINE_THRESHOLDS_R2008 = {"wholesales": (-10, -6, -1, 6), "ford_credit": (-98, -33, 32, 85), "revenue": (-22, -9, 3, 6),
                           "adj_eps": (-192, -53, 87, 102), "margin": (-1820, -1000, -180, 630)}


def check_print_r2008(p):
    """Re-derive an early-era print's growth rates and margins from its raw published figures."""
    r = p["raw"]
    pct = lambda a, b: round((b / a - 1) * 100, 1)
    mg = lambda pt, rv: round(pt / (rv * 1000) * 100, 2)
    want = {"sales_b": r["rev_b"], "sales_pct": pct(r["rev_prior_b"], r["rev_b"]), "ws_pct": pct(r["ws_prior_k"], r["ws_k"]),
            "fc_pct": pct(r["fc_ebt_prior_m"], r["fc_ebt_m"]) if r["fc_ebt_prior_m"] > 0 else None,
            "margin": mg(r["pretax_m"], r["rev_b"]), "margin_prior": mg(r["pretax_prior_m"], r["rev_prior_b"]),
            "eps_pct": pct(p["eps_q_prior"], p["eps_q"]) if p["eps_q_prior"] > 0 else None}
    want["margin_bp"] = round((want["margin"] - want["margin_prior"]) * 100)
    for k, v in want.items():
        assert p[k] == v or (v is not None and abs(p[k] - v) < 1e-9), (p["quarter"], k, p[k], v)
    assert (p.get("fc_note") is not None) == (want["fc_pct"] is None), (p["quarter"], "a Ford Credit change without a value needs its note")


def build_r2008(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    chart = retro_tool.chart("F")
    assert retro_tool.split_factor(chart, as_of) == 1.0, "a split after 2000-08-03 needs its encoding first"
    assert not [x for x in facts.get("splits", []) if x["published"] <= as_of], "the F builder has no split encoding"
    px = dict(raw)
    for v in facts["history_vintages"]:
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    assert rule_t(facts["rule_t_r2008"]) == ENGINE_THRESHOLDS_R2008, "the early-era thresholds must follow rule T on the fact sheet's values"
    assert not [g for g in facts["guides"] if g["published"] <= as_of], "an early-era guide needs its encoding first (none is in numbers)"
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    for p in public:
        check_print_r2008(p)
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["q"] == 4 else 0)
    prints = [p for p in public if guide_fy(p) >= first_fy]
    events = [e for e in facts["events"] if e["published"] <= as_of]
    assert not events, f"{as_of}: no event kind is encoded for the early era (no theme is live for an automaker before 2020-01-01)"
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is public yet")
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage
    h = {**h, "extended": ""}
    for p in prints:
        a = p.get("fy_actual")
        if a and a["fy"] not in reported(h):
            y = str(a["fy"])
            eps_n = {**h["eps_normalized"], **({y: a["eps_normalized"]} if a["eps_normalized"] is not None else {})}
            excl = dict(h.get("eps_excluded", {}))
            if a["eps_normalized"] is None:
                excl[y] = a["excluded_note"]
            for yy, n in a.get("excluded_updates", {}).items():   # a later figure for a year already excluded: the note follows it
                assert yy in excl, (p["quarter"], yy)
                excl[yy] = n
            for yy, e in a.get("readmits", {}).items():           # a positive company figure for an excluded year: it re-enters
                assert yy in excl and e > 0, (p["quarter"], yy, e)
                del excl[yy]
                eps_n[yy] = e
            shares = dict(h["diluted_shares_m"])
            if a["diluted_shares_m"] is not None:                 # a release with no count leaves the shares history to the 10-K
                shares[y] = a["diluted_shares_m"]
            h.update(fy_label=a["fy_label"], eps_normalized=eps_n, eps_excluded=excl,
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]}, diluted_shares_m=shares,
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}' + (f'; {a["readmit_note"]}' if a.get("readmit_note") else ""),
                     prev_fy_margin=a["pretax_margin"], prev_fy_margin_note=a["pretax_margin_note"],
                     prev_fy_sales_growth=a["sales_growth"], prev_fy_ws_pct=a["ws_pct"], prev_fy_ws_note=a["ws_note"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     sources=h["sources"] + [p["source"]], extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    # a later filing that republishes an earlier year's company figure restates it until a 10-K vintage published after it (the CAT
    # 'restates' encoding, EPS only; retro/README.md, "F 2015-2018"): the Q4 2014 release's 2013, and the 8-K of 2016-01-07's 2013 and
    # 2014 on mark-to-market pension accounting
    for r in facts.get("restatements_r2008", []):
        if h["published"] < r["published"] <= as_of:
            for yy, x in r["years"].items():
                assert yy in h["eps_normalized"], (r["doc"], yy, "restates a year outside the history")
                h.update(eps_normalized={**h["eps_normalized"], yy: x["eps"]}, normalization=f'{h["normalization"]}; {x["note"]}',
                         sources=h["sources"] + [r["source"]],
                         extended=f'{h["extended"]}, FY{yy[2:]} restated by {r["source"]} ({r["published"]})')
    latest = prints[-1]
    i = public.index(latest)
    prev = (public[i - 1]["ws_pct"], public[i - 1]["quarter"]) if i > 0 else (h["prev_q_ws_pct"], h["prev_q_label"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    excluded = {int(k): v for k, v in h.get("eps_excluded", {}).items()}
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)        # the last full year in the history: cur_fy - 1 unless that year is excluded
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"
    # a fiscal-year adjusted EPS guide in numbers (Ford guides a range from the Q2 2017 release; a preliminary full-year figure is
    # recorded as a guide, the SHW rule): the latest one for the current year, its midpoint (the CAT encoding)
    ge = ([g for g in facts.get("eps_guides_r2008", []) if g["published"] <= as_of and g["fy"] == cur_fy] or [None])[-1]

    # ── no revenue guide in numbers: BASE takes the latest quarter's revenue growth; without an EPS guide the last full year's EPS stands ──
    if ge:
        eps_now = round(sum(ge["eps"]) / 2, 3)
        eps_fig = f"${ge['eps'][0]:.2f}" if ge["eps"][0] == ge["eps"][1] else f"${ge['eps'][0]:.2f}-{ge['eps'][1]:.2f}"
        eps_label = f"{fy_e} EPS, guide midpoint: adjusted EPS {eps_fig} ({ge['doc']}, {ge['published']})"
    else:
        eps_now = eps_hist[last_fy]
        eps_label = (f"{fy_e}: no EPS guide in numbers, FY{last_fy % 100:02d}'s ${money(eps_now)} (excluding special items) stands"
                     + "".join(f" (FY{y % 100:02d} is excluded: {excluded[y]})" for y in range(last_fy + 1, cur_fy)))
    fwd = [latest["sales_pct"]] * 2
    fwd_label, fwd_short, fwd_period = (f"no {next_q} revenue guide, {latest['quarter']} revenue as reported",
                                        f"{latest['quarter'][:2]} revenue", latest["quarter"])
    if ge:
        guide_text = (f"{fy_now}: adjusted EPS {eps_fig} ({ge['doc']}, {ge['published']}: '{ge['quote']}'); no revenue or margin guide "
                      f"in numbers (BASE takes {latest['quarter']} revenue growth)")
    else:
        guide_text = (f"{fy_now}: no EPS, revenue or margin guide in numbers in any filing (Ford's outlook is in words and planning "
                      f"assumptions, not encoded; BASE takes {latest['quarter']} revenue growth)")
    margin_guided = False
    fy_margin_base = h["prev_fy_margin"]

    # ── dividend: the latest declared regular rate ──
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
    eps = {**eps_hist, cur_fy: eps_now}
    fy = lambda d: min(fiscal_year(d), cur_fy)
    window = [d for d in days if d > minus_years(as_of, 10) and (not h["pe_window_start"] or d >= h["pe_window_start"])]
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

    # ── era text: no disruption theme in the registry is live for an automaker in the early era (the text names none: a later
    #    theme's live date is not public on AS_OF) ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live for an automaker", "No disruption theme is live for an automaker"
    theme_summary = "no disruption theme is live for an automaker on this date"
    why = h["why"] + ("; no disruption theme in the registry is live for an automaker on this date, so the watch list is empty "
                      "and the 10-K's words on the shift away from trucks and SUVs stay here (the PEP obesity rule)")
    kind, pit_risk = "DURABLE", 2
    cat3 = (f"(3) The {fy_now} adjusted EPS guide — {eps_fig} ({ge['doc']}): the EPS anchor" if ge else
            f"(3) A {fy_now} outlook in numbers — none: Ford's outlook is in words and planning assumptions")
    fc_txt = (f"{latest['fc_pct']:+.1f}%" if latest["fc_pct"] is not None else "n/r")
    cat4 = (f"(4) Ford Credit pre-tax — {fc_txt} in {latest['quarter']} (${latest['raw']['fc_ebt_m']:,.0f}M vs "
            f"${latest['raw']['fc_ebt_prior_m']:,.0f}M): credit losses, lease residuals and funding costs")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    company, exchange = h["company"], h["exchange"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])]
           + ([dividend_src] if dividend_src else []) + ([ge["source"]] if ge else []))
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "A0", "published": as_of, "title": "Yahoo Finance daily prices, F and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/F/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "margin", "margin_bp", "ws_pct", "fc_pct", "eps_q", "eps_q_prior",
                   "eps_pct")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    rw = latest["raw"]
    # the cash measure the print states (Automotive gross cash to 2015, Automotive cash, then Company cash); n/r when its filings state none
    cash_txt = (f"{latest.get('cash_label', 'Automotive gross cash')} ${latest['cash_b']:.1f}B" if latest["cash_b"] is not None
                else f"{latest.get('cash_label', 'Automotive gross cash')} n/r")
    volumes = (f"Wholesales {latest['ws_pct']:+.1f}% ({rw['ws_prior_k']:,.0f}K to {rw['ws_k']:,.0f}K, {latest['ws_note']}); "
               f"Ford Credit pre-tax {fc_txt} (${rw['fc_ebt_prior_m']:,.0f}M to ${rw['fc_ebt_m']:,.0f}M"
               + (f"; {latest['fc_note']}" if latest.get("fc_note") else "") + "); "
               f"revenue {latest['sales_pct']:+.1f}% as reported (${rw['rev_prior_b']:.1f}B to ${rw['rev_b']:.1f}B); "
               f"pre-tax ${rw['pretax_prior_m']:,.0f}M to ${rw['pretax_m']:,.0f}M; EPS excluding special items ${latest['eps_q']:.2f} vs "
               f"${latest['eps_q_prior']:.2f} (GAAP ${latest['eps_gaap']:.2f} vs ${latest['eps_gaap_prior']:.2f})")
    fy_rev = rev[max(rev)] * (1 + sum(fwd) / 2 / 100)
    fy_rev_label = f"{fwd_label}, applied to the year (no {fy_now} revenue guide)"
    dil_m = latest["diluted_shares_m"] if latest["diluted_shares_m"] is not None else shares[max(shares)]
    dil_note = ("the release's diluted shares" if latest["diluted_shares_m"] is not None
                else f"the release states no share count: FY{max(shares) % 100:02d}'s diluted shares (display only)")
    R = repr
    head = f'''#!/usr/bin/env python3
"""
F Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: F)  ·  {h["business_line"]}
Generated by retro/build_f.py from retro/facts/F.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "F"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); automaker signals, the early era")
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

# ── FACTS: company history ({", ".join(dict.fromkeys(h["sources"]))}, vintage {h["published"]}{h["extended"]}) ──
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}
REVENUE_HIST  = {R(rev)}   # total sales and revenues, USD bn
SHARES_HIST   = {R({y: round(v, 1) for y, v in shares.items()})}   # diluted, millions ({h["shares_note"]})
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_margin"]}   # {h["prev_fy_margin_note"]}
CHECK_MARGIN_PCT = {h["prev_fy_margin"]}   # the same, for the EPS check (display only)
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_WHOLESALES = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # no revenue guide: the latest quarter's revenue growth, as reported
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no margin guide, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {fy_rev:.2f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {dil_m / 1000:.4f}   # {dil_note}
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(f"{next_q} print")}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenue {h['prev_fy_sales_growth']:+.1f}%, wholesales {h['prev_fy_ws_pct']:+.1f}% ({h['prev_fy_ws_note']}); {latest['quarter']} pre-tax margin {latest['margin']:.1f}% ({latest['margin_bp']:+d}bp)")}
BALANCE_TEXT    = {R(f"{cash_txt}, {h['fcf_label']} {h.get('fcf_name', 'Automotive operating-related cash flow')} ${h['fcf_b']:.1f}B, dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
VOLUMES_TEXT    = {R(volumes)}
CAPITAL_RETURN  = {R(h["cash_return_text"])}
THEME_FACTORS   = {R(factors)}
THEME_SIGNAL_NAME    = {R(sig_name)}
THEME_SIGNAL_TRIGGER = {R(trigger)}
THEME_SUMMARY        = {R(theme_summary)}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/F)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    with open(ENGINE08, encoding="utf-8") as fh:
        engine08 = fh.read()
    raw, spx = load_series("F"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        if d < ERA_2022:
            tag, q, stage = build_r2008(d, facts, raw, spx, engine08, os.path.abspath(a.out))
        else:
            tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<34}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
