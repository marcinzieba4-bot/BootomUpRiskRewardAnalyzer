#!/usr/bin/env python3
"""
Build SO retrospective models from the dated fact sheet (retro/facts/SO.json).

The SO sibling of build_f.py (its early era, build_r2008) with the BMY 'distributions' rule: the same frozen rules (retro method r2), the
same weekly dates and the same market statistics, with electric utility signals (retro/templates/so_engine.py.tmpl). For each as-of date
the builder
  1. selects only the history vintage, prints and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, as traded (Yahoo's 2-for-1 split of 1994 precedes every
     per-share fact; the 2001 Mirant spin-off, which Yahoo books as a 10000:6109 split on 2001-04-03, is undone for the days before it,
     the 'distributions' rule of MAR, PFE and BMY),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Southern Company's fiscal year is the calendar year. No filing of 2007-2009 guides EPS, revenue or a margin in numbers: each release says
earnings guidance is discussed on the analyst call, and no transcript or slides are filed. So the no-guide rules of method r2 apply on
every date (retro/README.md, "SO"):
  - current-FY EPS: the last full year's EPS stands (the rollover rule),
  - forward revenue growth: the latest quarter's total revenue growth, as reported (the UNP rule),
  - guided margin step: none; the margin signal uses the latest quarter's change in the operating margin.
EPS is GAAP diluted EPS from continuing operations where the 10-K reports the line, else diluted EPS (the LOW and UNP rule), each year
from the latest 10-K that reports it. The company's figures excluding synthetic fuels (and, in Q2 2008 to Q4 2008, the leveraged lease
charges with them) remove an ongoing operation, not only one-offs, so GAAP stands (the AAPL 2008, NKE FY2013 and BMY rule); from the
Q1 2009 release its figure excludes only one-offs (the MC Asset Recovery settlement, the 2008 leveraged lease charges) and the quarterly
EPS signal uses it. A Q4 release comes weeks before its 10-K, so a Q4 print carries the year's actuals (fy_actual) until the 10-K. No
disruption theme in taxonomy_eras.json is live for an electric utility in 2008-2009 (ENERGY_TRANSITION, scoped to reserves and refining,
from 2015-12-12), so the watch list is empty and the builder refuses events until a theme encoding is decided.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it (every release of the period came on a Wednesday or Thursday).

Output goes to staging/retrospective/SO until the series is added to the archive (--out archive/retrospective/SO).

Usage
  python3 retro/build_so.py --weekly 2008-01-01 2009-12-31
  python3 retro/build_so.py 2008-01-31
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/SO/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "SO.json")
ENGINE = os.path.join(HERE, "templates", "so_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "SO")
# rule T, the engine's signal thresholds over 1997-2006 (the FY2006 10-K, the vintage public on 2008-01-04): (BEAR, BASE, BULL, XBULL);
# the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"kwh": (-8, -3, 2, 6), "segment": (-7, -2, 3, 13), "revenue": (-10, -2, 6, 16), "eps": (-15, -6, 3, 15),
                     "margin": (-410, -220, -30, 150)}
RULE_T_KEYS = {"kwh": (1, False), "segment": (1, False), "revenue": (1, False), "eps": (1, False),
               "margin": (10, False)}           # (rounding unit, lower is better)


def fiscal_year_end(n):
    """Southern Company's fiscal year n is the calendar year n."""
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
    """Re-derive a print's growth rates, margins and EPS growth from its raw published figures (they must match the fact sheet)."""
    r = p["raw"]
    pct = lambda a, b: round((b / a - 1) * 100, 1)
    m, m0 = r["opinc_m"] / r["rev_m"] * 100, r["opinc_prior_m"] / r["rev_prior_m"] * 100
    want = {"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": pct(r["rev_prior_m"], r["rev_m"]),
            "kwh_pct": pct(r["kwh_prior_m"], r["kwh_m"]), "seg_pct": pct(r["seg_prior_m"], r["seg_m"]),
            "margin": round(m, 2), "margin_prior": round(m0, 2), "margin_bp": round((m - m0) * 100, 1),
            "eps_pct": pct(p["eps_q_prior"], p["eps_q"])}
    for k, v in want.items():
        assert p[k] == v or abs(p[k] - v) < 1e-9, (p["quarter"], k, p[k], v)
    # the EPS signal's basis: the company's figure excluding items only when every item it excludes is a one-off
    want_eps = (p["eps_ex"], p["eps_ex_prior"]) if p["eps_basis"] == "excluding items" else (p["eps_gaap"], p["eps_gaap_prior"])
    assert (p["eps_q"], p["eps_q_prior"]) == want_eps, (p["quarter"], "EPS basis")
    assert p["eps_basis"] == "GAAP" or "synthetic fuels" not in p["eps_note"], (p["quarter"], "a figure excluding synthetic fuels is not used")


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    chart = retro_tool.chart("SO")
    off = chart["meta"]["gmtoffset"]
    ydate = lambda v: dt.datetime.fromtimestamp(v["date"] + off, dt.timezone.utc).date().isoformat()
    dist_days = {x["effective"] for x in facts.get("distributions", [])}
    later_splits = [v for v in chart.get("events", {}).get("splits", {}).values() if ydate(v) > as_of and ydate(v) not in dist_days]
    assert not later_splits, "a split after AS_OF needs its encoding first (prices on the AS_OF share basis, the UNP rule)"
    assert not facts.get("splits"), "the SO builder has no split encoding (the 1994 split precedes every per-share fact)"
    px = dict(raw)
    # a distribution (the 2001 spin-off of Mirant) is not a split: Yahoo books it as a 10000:6109 split on 2001-04-03, so its factor is
    # undone for the days before that date and every price stays as traded (the MAR, PFE and BMY 'distributions' rule; the drop stays in
    # the series); per-share facts are not restated
    for x in facts.get("distributions", []):
        ev = [v for v in chart.get("events", {}).get("splits", {}).values() if ydate(v) == x["effective"]]
        num, den = x["yahoo_ratio"]
        assert len(ev) == 1 and (ev[0]["numerator"], ev[0]["denominator"]) == (num, den), (x["effective"], "Yahoo's factor")
        if x["effective"] <= as_of:
            px = {d: (tuple(v * num / den for v in hlc) if d < x["effective"] else hlc) for d, hlc in px.items()}
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    assert not [g for g in facts["guides"] if g["published"] <= as_of], "a guide needs its encoding first (no SO filing guides in numbers)"
    events = [e for e in facts["events"] if e["published"] <= as_of]
    if events:
        sys.exit(f"{as_of}: the SO builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    for p in public:                               # a print public on AS_OF must match its raw figures
        check_print(p)
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    first_fy = max(int(k) for k in h["eps_normalized"]) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["q"] == 4 else 0)
    prints = [p for p in public if guide_fy(p) >= first_fy]
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is public yet")
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage
    h = {**h, "extended": ""}
    for p in prints:
        a = p.get("fy_actual")
        if a and str(a["fy"]) not in h["eps_normalized"]:          # the 10-K vintage, once out, wins
            y = str(a["fy"])
            shares = dict(h["diluted_shares_m"])
            if a["diluted_shares_m"] is not None:                 # a release with no diluted count leaves the shares history to the 10-K
                shares[y] = a["diluted_shares_m"]
            if a.get("eps_basis"):                               # the release's own figure excluding only one-offs (SO 2010-2013)
                h["eps_bases"] = {**h.get("eps_bases", {}), y: a["eps_basis"]}
            h.update(fy_label=a["fy_label"], eps_normalized={**h["eps_normalized"], y: a["eps_normalized"]},
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]}, diluted_shares_m=shares,
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_margin=a["margin"], prev_fy_margin_note=a["margin_note"],
                     check_pretax_margin=a["check_pretax_margin"], check_pretax_note=a["check_pretax_note"],
                     prev_fy_sales_growth=a["sales_growth"], prev_fy_kwh_pct=a["kwh_pct"], prev_fy_seg_pct=a["seg_pct"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     sources=h["sources"] + [p["source"]], extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    latest = prints[-1]
    i = public.index(latest)
    assert i > 0, "the previous quarter must be in the fact sheet"
    prev = (public[i - 1]["kwh_pct"], public[i - 1]["quarter"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    cur_fy = max(eps_hist) + 1
    last_fy = cur_fy - 1
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── no guide in numbers: BASE takes the latest quarter's revenue growth; the last full year's EPS stands ──
    eps_now = eps_hist[last_fy]
    # the last full year's EPS, on its basis: GAAP, or the company's figure excluding only one-offs where a filing states it (SO 2010-2013)
    basis = h.get("eps_bases", {}).get(str(last_fy))
    eps_label = (f"{fy_e}: no EPS guide in numbers in any filing, FY{last_fy % 100:02d}'s ${money(eps_now)} "
                 + (f"(the company's figure {basis})" if basis else "(GAAP)") + " stands")
    fwd = [latest["sales_pct"]] * 2
    fwd_label, fwd_short, fwd_period = (f"no {next_q} revenue guide, {latest['quarter']} revenue as reported",
                                        f"{latest['quarter'][:2]} revenue", latest["quarter"])
    # what the latest release that mentions the analyst call says about it (from the Q2 2011 release it no longer names earnings guidance)
    calls = [p for p in public if p.get("call_words")]
    said = [p for p in calls if "guidance" in p["call_words"]]
    if calls and "guidance" in calls[-1]["call_words"]:
        call_txt = (f"the {calls[-1]['quarter']} release: management 'will discuss earnings and earnings guidance' on the analyst call, and "
                    "no transcript or slides are filed")
    elif calls:
        call_txt = (f"the {calls[-1]['quarter']} release says only that management '{calls[-1]['call_words']}' on the analyst call"
                    + (f"; the {said[-1]['quarter']} release was the last to name earnings guidance" if said else "")
                    + "; no transcript or slides are filed")
    else:
        call_txt = "no transcript or slides of the analyst calls are filed"
    guide_text = (f"{fy_now}: no EPS, revenue or margin guide in numbers in any filing ({call_txt}; BASE takes {latest['quarter']} "
                  "revenue growth)")
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
    fy = lambda d: min(fiscal_year(d), cur_fy)     # a day past the last guided year keeps that year's EPS
    window = [d for d in days if d > minus_years(as_of, 10) and (not h["pe_window_start"] or d >= h["pe_window_start"])]
    assert all(fy(d) in eps for d in window), (as_of, "P/E window needs EPS for every fiscal year")
    years = (dt.date.fromisoformat(as_of) - dt.date.fromisoformat(window[0])).days / 365.25
    window_label = "10-yr" if years > 9.9 else f"{years:.1f}-yr"
    pe = {d: px[d][2] / eps[fy(d)] for d in window}
    srt = sorted(pe.values())
    qtl = lambda p: round(srt[int(p * (len(srt) - 1))], 1)
    pctl = {"p5": qtl(.05), "p10": qtl(.10), "p25": qtl(.25), "median": qtl(.5), "p75": qtl(.75), "p90": qtl(.9), "max": round(srt[-1], 1)}
    pe_now_pctl = round(sum(v <= close / eps_now for v in srt) / len(srt) * 100)
    # the window's days before the Mirant distribution are priced as traded, with Mirant (the 'distributions' rule)
    mirant_txt = "".join(f" (days before {x['effective']} as traded, with Mirant)" for x in facts.get("distributions", [])
                         if window[0] < x["effective"] <= as_of)
    yearly = []
    for y in sorted({d[:4] for d in window}):
        dd = min((d for d in window if d.startswith(y)), key=lambda d: pe[d])
        yearly.append((y, round(pe[dd], 1), dd))
    ref = min(yr, key=lambda d: px[d][2])

    # ── era text: no disruption theme in the registry is live for an electric utility on these dates (the text names none) ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live for a utility", "No disruption theme is live for an electric utility"
    theme_summary = "no disruption theme is live for an electric utility on this date"
    why = h["why"] + ("; no disruption theme in the registry is live for an electric utility on this date, so the watch list is empty and "
                      "the 10-K's words on climate change legislation stay here (the PEP obesity rule)")
    kind, pit_risk = "DURABLE", 2
    cat3 = f"(3) A {fy_now} earnings guide in numbers — none in any filing (guidance is given on the analyst call only)"
    cat4 = (f"(4) Electric utilities' net income — {latest['seg_pct']:+.1f}% in {latest['quarter']} (${latest['raw']['seg_m']:,.0f}M vs "
            f"${latest['raw']['seg_prior_m']:,.0f}M): rate relief against sales, weather and costs")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        rt = same_day[-1].get("release_time", "")
        assert "before the open" in rt or "during the session" in rt, (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the close")
        tag = (f"(day of the {same_day[-1]['quarter']} print, public before the open)" if "before the open" in rt else
               f"(day of the {same_day[-1]['quarter']} print, released during the session)")

    company, exchange = h["company"], h["exchange"]
    ids = (list(h["sources"]) + [p["source"] for p in prints] + [public[i - 1]["source"]] + ([dividend_src] if dividend_src else [])
           + [x["source"] for x in facts.get("distributions", []) if x["effective"] <= as_of])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "W0", "published": as_of, "title": "Yahoo Finance daily prices, SO and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/SO/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "margin", "margin_bp", "kwh_pct", "kwh_wa_pct", "seg_pct",
                   "eps_q", "eps_q_prior", "eps_pct", "eps_basis")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    rw = latest["raw"]
    wa = (f", weather-adjusted {latest['kwh_wa_pct']:+.1f}%" if latest["kwh_wa_pct"] is not None
          else ", no weather-adjusted figure in the release")
    volumes = (f"Retail kWh {latest['kwh_pct']:+.1f}% as reported ({rw['kwh_prior_m']:,.0f} to {rw['kwh_m']:,.0f} million kWh{wa}); "
               f"electric utilities' net income {latest['seg_pct']:+.1f}% (${rw['seg_prior_m']:,.0f}M to ${rw['seg_m']:,.0f}M, the "
               f"traditional operating companies and Southern Power" + (f"; {latest['seg_note']}" if latest.get("seg_note") else "")
               + f"); revenue {latest['sales_pct']:+.1f}% as reported "
               f"(${rw['rev_prior_m']:,.0f}M to ${rw['rev_m']:,.0f}M); operating income ${rw['opinc_prior_m']:,.0f}M to ${rw['opinc_m']:,.0f}M"
               + (f" ({latest['margin_note']})" if latest.get("margin_note") else "") + f"; EPS: {latest['eps_note']}")
    fy_rev = rev[max(rev)] * (1 + sum(fwd) / 2 / 100)
    fy_rev_label = f"{fwd_label}, applied to the year (no {fy_now} revenue guide)"
    dil_note = (f"the release's average shares ({latest['quarter']}; basic: diluted EPS differs by not more than 1 cent, as the release "
                "states; display only)")
    R = repr
    head = f'''#!/usr/bin/env python3
"""
SO Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: SO)  ·  {h["business_line"]}
Generated by retro/build_so.py from retro/facts/SO.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "SO"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); electric utility signals")
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
WINDOW_LABEL    = {R(window_label)}   # P/E window: {window[0]} .. AS_OF{mirant_txt}
YEARLY_MIN_PE   = {R(yearly)}   # (calendar year, lowest P/E, date)
VOL_ANNUAL_PCT  = {vol:.3f}   # 1-yr realized, daily log returns
VOL_BETA        = {beta:.2f}    # 1-yr beta vs S&P 500
VOL_52W_LOW     = {low52:.2f}
VOL_52W_HIGH    = {high52:.2f}
REF_LOW         = {px[ref][2]:.2f}   # lowest close of the last 52 weeks, {ref}
REF_LOW_LABEL   = {R(MONTHS[int(ref[5:7]) - 1])}

# ── FACTS: company history ({", ".join(dict.fromkeys(h["sources"]))}, vintage {h["published"]}{h["extended"]}) ──
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}
REVENUE_HIST  = {R(rev)}   # total operating revenues, USD bn
SHARES_HIST   = {R({y: round(v, 1) for y, v in shares.items()})}   # diluted, millions ({h["shares_note"]})
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_margin"]}   # {h["prev_fy_margin_note"]}
CHECK_MARGIN_PCT = {h["check_pretax_margin"]}   # pre-tax margin, for the EPS check: {h["check_pretax_note"]}
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_KWH        = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # no revenue guide: the latest quarter's revenue growth, as reported
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no margin guide, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {fy_rev:.2f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {latest["shares_m"] / 1000:.4f}   # {dil_note}
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenue {h['prev_fy_sales_growth']:+.1f}%, retail kWh {h['prev_fy_kwh_pct']:+.1f}%, electric utilities' net income {h['prev_fy_seg_pct']:+.1f}%; {latest['quarter']} operating margin {latest['margin']:.1f}% ({latest['margin_bp']:+.1f}bp)")}
BALANCE_TEXT    = {R(f"{h['fy_label']} year-end cash ${h['cash_b']:.3f}B, {h['fcf_label']} free cash flow ${h['fcf_b']:.2f}B ({h['fcf_note']}), dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/SO)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("SO"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<34}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
