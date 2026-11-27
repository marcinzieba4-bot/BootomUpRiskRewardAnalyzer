#!/usr/bin/env python3
"""
Build NEM retrospective models from the dated fact sheet (retro/facts/NEM.json).

The NEM sibling of build_mu.py: the same frozen rules (retro method r2), the same weekly dates and the same market statistics,
with a gold miner's signals and Newmont's own rule-T thresholds (retro/templates/nem_engine.py.tmpl). For each as-of date the
builder
  1. selects only the history vintage, prints and outlooks whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF (Yahoo's NEM series; no split since 1994, so every
     price from the P/E window's start is the close as traded),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Newmont's fiscal year is the calendar year. The method r2 inputs map as follows (retro/README.md, "NEM"; decided before any NEM
model was built or scored):
  - EPS: GAAP diluted EPS from continuing operations before the cumulative effect of accounting changes, each year from the latest
    filing that reports it. 1998-2001 are losses and FY2001 takes the years before it (the MU FY2003 rule), so the history and the
    P/E window start with FY2002 ('pe_window_start'). FY2007 is a loss with no figure excluding only its one-offs: a gap
    ('eps_excluded'), its own days leave the P/E window. The releases' adjusted net income (from Q1 2008) also removes items that
    recur in every period it tabulates (legacy closure obligations, write-downs of marketable securities), so GAAP stands (the PEP
    2008 core rule);
  - current-FY EPS: no filing gives an EPS guide, so the last full year in the history stands (the rollover rule): FY06 to the Q4
    2007 print, then FY06 again (FY07 excluded), then FY08;
  - forward revenue growth: no filing guides revenue in numbers, so the latest quarter's revenue growth stands in (the UNP rule);
    the outlooks for equity gold sales and costs applicable to sales per ounce, and the Q4 2007 table of cost components, are
    display only (the XOM production rule and the MSFT segment rule);
  - guided margin step: none (no margin guide); the margin signal uses the latest quarter's pre-tax margin change.
The kind is DURABLE: no Newmont 10-K of FY2006-FY2008 calls the business cyclical (the MU rule). No disruption theme in
taxonomy_eras.json is live for a gold miner in 2008-2009, so the builder refuses events until a theme encoding is decided.
Every Q4 print came the same day as its 10-K (2008-02-21, 2009-02-19), so no print carries full-year actuals of its own.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. Every release of the range came before the open or during the session on a Wednesday or a
Thursday, so the week's date is the next trading day.

Output goes to staging/retrospective/NEM until the series is added to the archive (--out archive/retrospective/NEM).

Usage
  python3 retro/build_nem.py --weekly 2008-01-01 2009-12-31
  python3 retro/build_nem.py 2008-02-22
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/NEM/<AS_OF>
"""
import argparse
import copy
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

FACTS = os.path.join(HERE, "facts", "NEM.json")
ENGINE = os.path.join(HERE, "templates", "nem_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "NEM")
SYMBOL = "NEM"
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"oz": (-27, -13, 1, 40), "cas": (52, 28, 5, -14), "revenue": (-33, -10, 13, 55), "eps": (-106, -34, 38, 297),
                     "margin": (-8210, -4020, 180, 3780)}
RULE_T_KEYS = {"oz": (1, False), "cas": (1, True), "revenue": (1, False), "eps": (1, False), "margin": (10, False)}
GUIDE_KEYS = {"fy", "published", "source", "doc", "display", "unused"}      # display only: no guide field has an encoding


def fiscal_year_end(n):
    """Newmont's fiscal year n is the calendar year n."""
    return dt.date(n, 12, 31)


def fiscal_year(day):
    return dt.date.fromisoformat(day).year


def rule_t_value(k, r):
    """One annual rule-T value from its raw figures ((prior, current))."""
    pct = lambda a, b: round((b / a - 1) * 100 + 0.0, 2)
    if k == "oz":
        return pct(*r["oz_k"])
    if k == "cas":
        return pct(*r["cost"])
    if k == "revenue":
        return pct(*r["revenue_m"])
    if k == "eps":
        return pct(*r["eps"])
    (p0, p1), (s0, s1) = r["pretax_m"], r["sales_m"]
    return round((p1 / s1 - p0 / s0) * 10000 + 0.0, 1)


def rule_t(rt):
    """Rule T thresholds from the annual values (re-derived from the raw figures): XBULL best, BULL median, BASE worst, BEAR one
    median-to-worst step beyond the worst; rounded half up to whole percent and to 10 bp."""
    out = {}
    for k, (unit, lower) in RULE_T_KEYS.items():
        assert (rt[k]["unit"], rt[k]["lower_is_better"]) == (unit, lower), (k, "the fact sheet's unit or direction differs")
        for y, r in rt[k]["raw"].items():
            assert rule_t_value(k, r) == rt[k]["values"][y], (k, y, "a rule-T value differs from its raw figures")
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
    r = p["raw"]
    pct = lambda a, b: round((b / a - 1) * 100 + 0.0, 1)
    g = lambda a, b: pct(a, b) if a > 0 else round((b - a) / abs(a) * 100 + 0.0, 1)   # over a year-ago loss's absolute value (CAT)
    m, m0 = r["pretax_m"] / r["rev_m"] * 100, r["pretax_prior_m"] / r["rev_prior_m"] * 100
    want = {"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": pct(r["rev_prior_m"], r["rev_m"]), "oz_pct": pct(r["oz_prior_k"], r["oz_k"]),
            "cas_pct": pct(r["cas_prior"], r["cas"]), "pretax_margin": round(m + 0.0, 2), "pretax_margin_prior": round(m0 + 0.0, 2),
            "margin_bp": round((m - m0) * 100 + 0.0, 1), "eps_pct": g(p["eps_q_prior"], p["eps_q"])}
    for k, v in want.items():
        assert p[k] == v, (p["quarter"], k, p[k], v)
    assert "fy_actual" not in p, (p["quarter"], "a Q4 print's own full-year actuals need their encoding (each came with its 10-K)")


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    chart = retro_tool.chart(SYMBOL)
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat()
                    for v in chart.get("events", {}).get("splits", {}).values()}
    # the price data's only split (1994) precedes the P/E window; a later split needs its share-basis encoding first
    assert not {d for d in yahoo_splits if "2002-01-01" <= d <= as_of}, (as_of, "an unencoded split")
    assert not facts.get("splits") and not facts.get("distributions"), "the NEM builder has no split or distribution encoding"
    for v in facts["history_vintages"]:
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    assert not [g for g in facts.get("eps_guides", []) if g["published"] <= as_of], "an EPS guide with a field needs its encoding first"
    for g in [g for g in facts["guides"] if g["published"] <= as_of]:   # a guide public on AS_OF: display only
        assert set(g) == GUIDE_KEYS, (g["doc"], "a guide field the builder has no encoding for", set(g) ^ GUIDE_KEYS)
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        check_print(p)
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    assert not [x for x in facts.get("company_names", []) if x["published"] <= as_of], "a change of name needs its encoding first"
    facts = copy.deepcopy(facts)
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["q"] == 4 else 0)
    prints = [p for p in facts["prints"] if p["published"] <= as_of and guide_fy(p) >= first_fy]
    for p in prints:                               # a Q4 print in scope came with its 10-K: the vintage reports its year
        assert p["q"] != 4 or p["fy"] in reported(h), (as_of, p["quarter"], "a Q4 print ahead of its 10-K needs full-year actuals")
    events = [e for e in facts["events"] if e["published"] <= as_of]
    if events:
        sys.exit(f"{as_of}: the NEM builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is public yet")
    latest = prints[-1]
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    i = public.index(latest)
    assert i > 0, (as_of, "the fact sheet needs the print before the latest one")
    prev = (public[i - 1]["oz_pct"], public[i - 1]["quarter"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}   # reported history only: the rules use this
    excluded = {int(k): v for k, v in h.get("eps_excluded", {}).items()}
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)        # the last full year in the history: cur_fy - 1 unless that year is excluded
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── current-FY EPS: no EPS guide in any filing of the period, so the last full year's EPS stands ──
    eps_now = eps_hist[last_fy]
    eps_label = f"{fy_e}: no EPS guide in numbers, FY{last_fy % 100:02d}'s ${money(eps_now)} (GAAP) stands" + (
        " (FY" + ", FY".join(f"{y % 100:02d}" for y in range(last_fy + 1, cur_fy)) + " excluded: a loss)" if cur_fy > last_fy + 1 else "")
    # ── forward revenue growth: no revenue guide in any filing, so the latest quarter's revenue growth (the UNP rule) ──
    fwd = [latest["sales_pct"]] * 2
    fwd_label = f"{latest['quarter']} revenue growth (no revenue guide)"
    fwd_short, fwd_period = f"{latest['quarter'].split()[0]} revenue YoY", latest["quarter"]
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    guide_ids = []
    if guides:
        g = guides[-1]
        guide_text = (f"{fy_now} outlook ({g['doc']}, {g['published']}, display only): '{g['display']}' — {g['unused']}; BASE takes "
                      f"{latest['quarter']} revenue growth")
        guide_ids = [g["source"]]
        cat3 = (f"(3) The {fy_now} outlook — gold sales and unit costs, not revenue or EPS ({g['doc']}): the gold price sets revenue")
    else:
        guide_text = (f"{fy_now}: no outlook in scope; no filing guides revenue, EPS or a margin (BASE takes {latest['quarter']} "
                      "revenue growth)")
        cat3 = f"(3) A {fy_now} outlook — none yet: Newmont guides equity gold sales and unit costs, not revenue or EPS"
    margin_guided = False                          # no margin guide: no guided step; the signal uses the latest quarter's change
    fy_margin_base = h["prev_fy_margin"]

    # ── dividend: the latest declared rate (each 10-K; $0.10 a quarter throughout) ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts.get("dividends", []) if d["published"] <= as_of]
    divs.append((h["published"], h["dividend_annual"], h["dividend_note"], None))
    _, dividend, dividend_note, dividend_src = max(divs, key=lambda x: x[0])

    # ── listing (display): NYSE: NEM ──
    listing = [x for x in facts["listings"] if x["published"] <= as_of and x["effective"] <= as_of]
    assert listing, (as_of, "no listing in scope")
    exchange, listed = listing[-1]["exchange"], listing[-1]["symbol"]
    listing_ids = [listing[-1]["source"]]

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
    fy = lambda d: min(fiscal_year(d), cur_fy)     # a day past the last guided year keeps that year's EPS
    # the window: up to ten years, from the day after the last loss year that took the years before it (FY2001)
    window = [d for d in days if d > minus_years(as_of, 10) and (not h["pe_window_start"] or d >= h["pe_window_start"])]
    gone = sorted({fy(d) for d in window} & set(excluded))       # an excluded year's own days leave the window
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

    # ── era-dependent text, from facts only: no disruption theme in the registry is live for a gold miner on these dates ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
    key_tail = ("A gold miner's downturn shows up in unit costs and ounces first;\n"
                "  the bear needs the gold price to stop covering them.")
    theme_summary = "no disruption theme has dated evidence"
    live = [k for k, t in retro_tool.load_taxonomy()["themes"].items() if t["live_from"] <= as_of]
    assert set(live) <= {"OFFSHORE"}, (as_of, "a live theme needs its scope reading for a gold miner first", live)
    cat4 = (f"(4) Ounces — consolidated gold ounces sold {latest['oz_pct']:+.1f}% in {latest['quarter']} against revenue "
            f"{latest['sales_pct']:+.1f}%: the metal price, not volume, has carried revenue")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    company = h["company"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]]] + [public[i - 1]["source"]] + guide_ids
           + ([dividend_src] if dividend_src else []) + listing_ids)
    sources = [dict(id=x, **facts["sources"][x]) for x in dict.fromkeys(ids)]
    sources.append({"id": "Y0", "published": as_of, "title": "Yahoo Finance daily prices, NEM and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/NEM/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E "
                                f"distribution from {window[0]}"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "oz_pct", "cas", "cas_pct", "pretax_margin", "margin_bp", "eps_q",
                   "eps_q_prior", "eps_pct")
    L = {k: latest.get(k) for k in latest_keys}
    L["cas"] = latest["raw"]["cas"]
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    first_excl = "; ".join(f"FY{int(y) % 100:02d} {t}" for y, t in sorted(h.get("eps_first_excluded", {}).items()))
    rev_text = (f"Revenue: {latest['rev_note']}; {latest['oz_note']}; {latest['cas_note']}; {latest['eps_note']}; diluted shares "
                f"{latest['diluted_shares_m']:,.0f}M" + (f"; adjusted figures, display only: {latest['adj_note']}" if latest.get("adj_note") else ""))
    R = repr
    head = f'''#!/usr/bin/env python3
"""
NEM Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: {listed})  ·  {h["business_line"]}
Generated by retro/build_nem.py from retro/facts/NEM.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "NEM"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); gold-miner signals with "
               "Newmont's rule-T thresholds")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts above.
PIT_PROFILE = {{
    "kind": {R(h["kind"])},
    "risk": 2,
    "why": {R(h["why"])},
    "theme_watch": {R(watch)},
    "evidence": [],
}}

# ── FACTS: market (prices truncated at AS_OF, as traded) ─────────────────────
EXCHANGE        = {R(exchange)}   # display only; {listing[-1]["note"]}
CURRENT_PRICE   = {close:.2f}   # USD, {exchange} close {as_of}, as traded
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2
PE_PCTL         = {R(pctl)}   # current-FY P/E over the window below
PE_NOW_PCTL     = {pe_now_pctl}    # share of those daily P/Es at or below the AS_OF one
WINDOW_LABEL    = {R(window_label)}   # P/E window: {window[0]} .. AS_OF ({len(window)} trading days)
YEARLY_MIN_PE   = {R(yearly)}   # (calendar year, lowest P/E, date)
VOL_ANNUAL_PCT  = {vol:.3f}   # 1-yr realized, daily log returns
VOL_BETA        = {beta:.2f}    # 1-yr beta vs S&P 500
VOL_52W_LOW     = {low52:.2f}
VOL_52W_HIGH    = {high52:.2f}
REF_LOW         = {px[ref][2]:.2f}   # lowest close of the last 52 weeks, {ref}
REF_LOW_LABEL   = {R(MONTHS[int(ref[5:7]) - 1])}

# ── FACTS: company history ({", ".join(h["sources"])}, vintage {h["published"]}) ──
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}
EPS_FIRST_EXCLUDED = {R(first_excl)}
EPS_EXCLUDED  = {R({y: t for y, t in sorted(excluded.items())})}
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # revenues, USD bn
SHARES_HIST   = {R({y: round(v, 3) for y, v in shares.items()})}   # diluted, millions
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_margin"]}   # pre-tax margin, {h["prev_fy_margin_note"]}
CHECK_PRETAX_MARGIN = {h["prev_fy_margin"]}   # pre-tax margin for the EPS check (display), the same figure
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and the {fy_now} outlook ──
LATEST          = {R(L)}
PREV_SALES      = {R(prev)}   # the previous print's gold ounces sold growth
EPP_TODAY_EPS   = {round(eps_now, 6)}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # no revenue guide in any filing: the latest quarter's revenue growth (the UNP rule)
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no margin guide, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {rev[max(rev)] * (1 + sum(fwd) / 2 / 100):.4f}
FY_REVENUE_LABEL = {R(f"the {fwd_label}, YoY, applied to the year (no {fy_now} revenue guide)")}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} consolidated gold ounces sold {h['prev_fy_oz_k']:,.0f}K ({h['prev_fy_oz_pct']:+.1f}%), costs applicable to sales ${h['prev_fy_cas']:,.0f}/oz ({h['prev_fy_cas_pct']:+.1f}%) ({h['franchise_source']}); {latest['quarter'].split()[0]} ${latest['raw']['cas']:,.0f}/oz ({latest['cas_pct']:+.1f}% YoY)")}
BALANCE_TEXT    = {R(f"Cash and cash equivalents ${latest['cash_b']:.3f}B, {latest['debt_note']} ({latest['quarter']}), {h['fcf_label']} free cash flow ${h['fcf_b']:.3f}B ({h['fcf_note']}), dividend ${dividend:.2f} a year")}
REVENUE_TEXT    = {R(rev_text)}
CAPITAL_RETURN  = {R(h["cash_return_text"])}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/NEM)")
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
        print(f"{d}  {tag:<45}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
