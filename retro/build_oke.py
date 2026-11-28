#!/usr/bin/env python3
"""
Build OKE retrospective models from the dated fact sheet (retro/facts/OKE.json).

ONEOK, Inc., NYSE: OKE (CIK 1039684). The KMI sibling for a gas distributor that is also the general partner of a consolidated
midstream partnership: the same frozen rules (retro method r2), the same weekly dates and the same market statistics, with ONEOK's
own signals and rule-T thresholds (retro/templates/oke_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints, EPS guides and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF (Yahoo's OKE series times its factors after AS_OF, which
     gives the close as traded; the only factor inside the P/E window's reach is the 2:1 split of 2001-06-12, before its start),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

ONEOK's fiscal year is the calendar year from 2000 (fiscal 1997-1999 ended August 31; the four months to December 31, 1999 were a
transition period). The method r2 inputs map as follows (retro/README.md, "OKE"; decided before any OKE model was built or scored):
  - EPS: diluted EPS from continuing operations (before the 2003 cumulative effect), each year from the latest filing that reports it,
    at the company's figure excluding only one-offs where a filing prints it (2005 $2.53 and 2006 $2.40 without the gains on sale,
    the FY2006 10-K; the ACN rule), GAAP otherwise. FY2001 fails the AAPL FY2002 test on the latest filing that reports it (the OCC
    ruling and the Enron bankruptcy, $72.0M of listed items, against $43.5M of income from continuing operations), so the history and
    the P/E window start with FY2002 ('pe_window_start' 2002-01-01; the August fiscal years and the transition period stay out);
  - current-FY EPS: the midpoint of the latest 'net income guidance' range per diluted share for the year (the releases and the
    Item 7.01 guidance 8-Ks), GAAP; with none, the last full year's EPS (the rollover rule);
  - forward revenue growth: no filing guides revenue, so the latest quarter's revenue growth as reported stands in (the UNP rule);
    the segment operating income guides (Exhibit A of the guidance 8-Ks and releases) are components (the MSFT segment rule): no field;
  - guided margin step: none (no margin guide); the margin signal uses the latest quarter's pre-tax margin change;
  - dividend: the latest declared quarterly rate from the first filing that states it (the dividend 8-Ks), else the vintage's.
The kind is DURABLE: no ONEOK 10-K of FY2006-FY2008 calls its business cyclical (the word appears only in its billing cycle). No
disruption theme in taxonomy_eras.json is live for a gas utility and midstream company in 2008-2009 (OFFSHORE is scoped to IT services),
so the builder refuses events, and any other live theme, until an encoding is decided. ONEOK Partners, L.P. (NYSE: OKS) is a separate
listed entity: its units' prices and per-unit figures are never used; what ONEOK's own filings consolidate is in as published.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. Every earnings 8-K of 2007-2009 was accepted after the close and counts from the next trading day.
Each Q4 print came one trading day before its 10-K, and no weekly date falls between them (the builder asserts the vintage is public).

Output goes to staging/retrospective/OKE until the series is added to the archive (--out archive/retrospective/OKE).

Usage
  python3 retro/build_oke.py --weekly 2008-01-01 2009-12-31
  python3 retro/build_oke.py 2008-02-27
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/OKE/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "OKE.json")
ENGINE = os.path.join(HERE, "templates", "oke_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "OKE")
SYMBOL = "OKE"
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"nm": (-8, 5, 17, 38), "dist": (-88, -42, 3, 57), "revenue": (-38, -6, 26, 261),
                     "op_margin": (-1350, -720, -100, 430), "pretax_margin": (-1150, -590, -30, 620)}
RULE_T_KEYS = {"nm": (1, False), "dist": (1, False), "revenue": (1, False), "op_margin": (10, False), "pretax_margin": (10, False)}
PRINT_KEYS = {"quarter", "fy", "q", "published", "source", "release", "release_time", "raw", "rows", "sales_b", "sales_pct", "nm_pct",
              "dist_pct", "opm", "opm_bp", "ptm", "ptm_bp", "eps_q", "eps_q_prior", "diluted_shares_m", "sales_note", "nm_note",
              "dist_note", "margin_note", "eps_note", "cash_note", "next_print", "source_title"}
GUIDE_KEYS = {"fy", "published", "source", "doc", "eps_guide", "quote"}
SPLITS_AFTER = {"2012-06-04": 2.0, "2014-02-03": 1.1422}   # Yahoo's factors after every built date: the 2:1 split, the ONE Gas distribution
STOP = "2012-06-04"                                          # from here a factor falls inside the window: encode it first


def fiscal_year_end(n):
    """ONEOK's fiscal year n is the calendar year n (from 2000)."""
    return dt.date(n, 12, 31)


def fiscal_year(day):
    return dt.date.fromisoformat(day).year


def rule_t_value(k, r):
    """One annual rule-T value from its raw figures ((prior, current), thousands of dollars)."""
    pct = lambda a, b: round((b / a - 1) * 100 + 0.0, 2)
    if k == "revenue":
        return pct(*r["revenue_k"])
    if k == "nm":
        return pct(*r["net_margin_k"])
    if k == "dist":
        a, b = r["dist_oi_k"]
        return pct(a, b) if a > 0 else round((b - a) / abs(a) * 100 + 0.0, 2)
    (x0, x1), (s0, s1) = (r["oi_k"] if k == "op_margin" else r["pti_k"]), r["revenue_k"]
    return round((x1 / s1 - x0 / s0) * 10000 + 0.0, 1)


def rule_t(rt, keys=RULE_T_KEYS):
    """Rule T thresholds from the annual values (re-derived from the raw figures): XBULL best, BULL median, BASE worst, BEAR one
    median-to-worst step beyond the worst; rounded half up to whole percent and to 10 bp."""
    out = {}
    for k, (unit, lower) in keys.items():
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
    assert set(p) <= PRINT_KEYS, (p["quarter"], sorted(set(p) - PRINT_KEYS), "a print field with no encoding yet; decide one first")
    r = p["raw"]
    # growth on the year-ago figure; against a year-ago loss, over the loss's absolute value (the CAT rule: the Distribution
    # segment's third quarters)
    g = lambda a, b: round((b / a - 1) * 100 + 0.0, 1) if a > 0 else round((b - a) / abs(a) * 100 + 0.0, 1)
    mg = lambda x, rev: round(x / rev * 100 + 0.0, 2)
    want = {"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": g(r["rev_prior_m"], r["rev_m"]), "nm_pct": g(r["nm_prior_m"], r["nm_m"]),
            "dist_pct": g(r["dist_prior_m"], r["dist_m"]),
            "opm": mg(r["oi_m"], r["rev_m"]), "opm_bp": round((mg(r["oi_m"], r["rev_m"]) - mg(r["oi_prior_m"], r["rev_prior_m"])) * 100, 1),
            "ptm": mg(r["pti_m"], r["rev_m"]), "ptm_bp": round((mg(r["pti_m"], r["rev_m"]) - mg(r["pti_prior_m"], r["rev_prior_m"])) * 100, 1),
            "eps_q": r["eps_q"], "eps_q_prior": r["eps_q_prior"], "diluted_shares_m": r["dil_sh_m"]}
    for k, v in want.items():
        assert p[k] == v or (v is not None and abs(p[k] - v) < 1e-9), (p["quarter"], k, p[k], v)


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    if as_of >= STOP:
        sys.exit(f"{as_of}: Yahoo's 2012-06-04 split (and the 2014-02-03 ONE Gas factor) would fall inside the window; encode them first")
    chart = retro_tool.chart(SYMBOL)
    off = chart["meta"]["gmtoffset"]
    yahoo = {dt.datetime.fromtimestamp(v["date"] + off, dt.timezone.utc).date().isoformat(): v["numerator"] / v["denominator"]
             for v in chart.get("events", {}).get("splits", {}).values()}
    later = {d: round(f, 4) for d, f in yahoo.items() if d > as_of}
    assert later == SPLITS_AFTER, (as_of, "Yahoo's factors after AS_OF differ from the encoded ones", later)
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}   # Yahoo's close times the later factors: the price as traded
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    for v in vintages:                                 # the fiscal calendar the vintages state must match the rule
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
        assert not {d for d in yahoo if v["pe_window_start"] <= d <= as_of}, (as_of, "an unencoded split inside the P/E window")
    for g in [g for g in facts["eps_guides"] if g["published"] <= as_of]:
        assert set(g) == GUIDE_KEYS, (g["doc"], "a guide field with no encoding yet; decide one first", set(g) ^ GUIDE_KEYS)
    assert not [g for g in facts["guides"] if g["published"] <= as_of], "a non-EPS guide with a field needs its encoding first"
    assert not [n for n in facts["company_names"] if n["published"] <= as_of], "a change of company name needs its encoding first"
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    for p in public:                                   # a print public on AS_OF must match its raw figures
        check_print(p)
    h = vintages[-1]                                   # latest annual history public on AS_OF
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["q"] == 4 else 0)
    prints = [p for p in public if guide_fy(p) >= first_fy]
    for p in prints:                                   # a Q4 print in scope came a trading day before its 10-K: no weekly date between
        assert p["q"] != 4 or p["fy"] in reported(h), (as_of, p["quarter"], "a Q4 print ahead of its 10-K needs full-year actuals")
    events = [e for e in facts["events"] if e["published"] <= as_of]
    if events:
        sys.exit(f"{as_of}: the OKE builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is in the fact sheet for this date")
    latest = prints[-1]
    i = public.index(latest)
    assert i > 0, (as_of, "the fact sheet needs the print before the latest one")
    prev_seg = (public[i - 1]["nm_pct"], public[i - 1]["quarter"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    excluded = {int(k): v for k, v in h.get("eps_excluded", {}).items()}
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)        # the last full year in the history: cur_fy - 1 unless that year is excluded
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── current-FY EPS: the latest net income guidance range per diluted share for the year (midpoint), else the last full year ──
    egs = [g for g in facts["eps_guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    excluded_tail = "".join(f" (FY{y % 100:02d} is excluded: {excluded[y]})" for y in range(last_fy + 1, cur_fy))
    if egs:
        eg = egs[-1]
        lo, hi = eg["eps_guide"]
        eps_now = round((lo + hi) / 2, 3)
        how = f"the {eg['doc']}'s ${lo:.2f}-{hi:.2f} a diluted share, midpoint"
        eps_label = f"{fy_e}: GAAP net income guidance, {how} = ${money(eps_now)}" + excluded_tail
        guide_ids = [eg["source"]]
    else:
        eg = None
        eps_now = eps_hist[last_fy]
        how = None
        eps_label = f"{fy_e}: no EPS guide in scope yet, FY{last_fy % 100:02d}'s ${money(eps_now)} stands" + excluded_tail
        guide_ids = []
    fwd = [latest["sales_pct"]] * 2
    fwd_label, fwd_short, fwd_period = (f"no {fy_now} revenue guide in numbers, {latest['quarter']} revenues as reported",
                                        f"{latest['quarter'][:2]} revenues", latest["quarter"])
    guide_text = (f"{fy_now}: no revenue or margin guide in numbers (BASE takes {latest['quarter']} revenue growth as reported); "
                  + (f"EPS ${money(eps_now)} from the {eg['doc']}: '{eg['quote']}'" if eg else "no EPS guide for the year yet"))
    margin_guided = False                          # no margin guide: no guided step
    fy_margin_base = h["prev_fy_op_margin"]

    # ── dividend: the latest declared rate ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts["dividends"] if d["published"] <= as_of]
    divs.append((h["published"], h["dividend_annual"], h["dividend_note"], None))
    _, dividend, dividend_note, dividend_src = max(divs, key=lambda x: x[0])

    # ── listing (display): NYSE: OKE ──
    listing = [x for x in facts["listings"] if x["published"] <= as_of and x["effective"] <= as_of]
    assert listing, (as_of, "no listing in scope")
    exchange, listed = listing[-1]["exchange"], listing[-1]["symbol"]

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
    # the window: up to ten years, from the day after the distorted FY2001 that took the years before it
    window = [d for d in days if d > minus_years(as_of, 10) and d >= h["pe_window_start"]]
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

    # ── era-dependent text, from facts only: no disruption theme in the registry is live for a gas distributor and midstream
    # partnership's general partner on these dates (OFFSHORE is scoped to IT services) ──
    live = sorted(((t["live_from"], k, t["scope"]) for k, t in retro_tool.load_taxonomy()["themes"].items() if t["live_from"] <= as_of))
    assert [k for _, k, _ in live] == ["OFFSHORE"], (as_of, "a live theme needs its scope reading for OKE first", live)
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none in scope", "No live disruption theme covers gas utilities or midstream"
    theme_summary = "no theme in the registry is live for a gas distributor and midstream company on this date; none has dated evidence"
    key_tail = ("Regulated distribution rates and fee-based pipelines carry part of the cash, NGL spreads\n"
                "  and storage margins the rest; the bear needs both to give way.")
    why = h["why"]
    kind, pit_risk = "DURABLE", 2
    cat3 = (f"(3) The {fy_now} outlook — GAAP EPS ${money(eps_now)} ({how}); no revenue or margin guide in numbers" if eg else
            f"(3) The {fy_now} outlook — none yet: ONEOK guides net income per diluted share, not revenue or a margin")
    cat4 = f"(4) Free cash flow — {h['fcf_label']} {h['fcf_note']}"

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        rt = same_day[-1].get("release_time", "")
        assert "before the open" in rt or f"after the close: counts from {as_of}" in rt, (as_of, same_day[-1]["quarter"],
                                                                                         "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    company = h["company"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]]] + [public[i - 1]["source"]] + guide_ids
           + ([dividend_src] if dividend_src else []) + [listing[-1]["source"]])
    sources = [dict(id=x, **facts["sources"][x]) for x in dict.fromkeys(ids)]
    sources.append({"id": "Y0", "published": as_of,
                    "title": f"Yahoo Finance daily prices, {company} common stock ({exchange}: {listed}) and S&P 500, truncated at AS_OF",
                    "url": f"https://finance.yahoo.com/quote/{SYMBOL}/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E "
                                f"distribution from {window[0]}"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "opm", "opm_bp", "ptm", "ptm_bp", "eps_q", "eps_q_prior", "nm_pct",
                   "dist_pct")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    first_excl = "; ".join(f"FY{int(y) % 100:02d} {t}" for y, t in sorted(h.get("eps_first_excluded", {}).items()))
    activity = (f"Activity: {latest['sales_note']}; {latest['nm_note']}; {latest['dist_note']}; {latest['margin_note']}; "
                f"{latest['cash_note']}; EPS {latest['eps_note']}")
    fy_rev = rev[max(rev)] * (1 + sum(fwd) / 2 / 100)
    fy_rev_label = f"{fwd_label}, applied to the year (no {fy_now} revenue guide)"
    franchise_q = f"{latest['quarter'].split()[0]} net margin {latest['nm_pct']:+.1f}%, operating margin {latest['opm']:.2f}% ({latest['opm_bp']:+.0f}bp)"
    fcf_text = f"${h['fcf_b']:.2f}B" if h["fcf_b"] >= 0 else f"$({-h['fcf_b']:.2f})B"
    LATEST = {k: latest.get(k) for k in latest_keys}
    R = repr
    head = f'''#!/usr/bin/env python3
"""
{listed} Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: {listed})  ·  {h["business_line"]}
Generated by retro/build_oke.py from retro/facts/OKE.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "{SYMBOL}"
LISTED_SYMBOL = "{listed}"   # the listing on AS_OF
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); gas distribution and midstream "
               "signals with ONEOK's rule-T thresholds")
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
EXCHANGE        = {R(exchange)}   # display only; {listing[-1]["note"]}
CURRENT_PRICE   = {close:.2f}   # USD, {exchange} close {as_of}, as traded
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
EPS_FIRST_EXCLUDED = {R(first_excl)}
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # revenues, USD bn
SHARES_HIST   = {R({y: round(v, 3) for y, v in shares.items()})}   # {h["shares_note"]}
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # {h["prev_fy_op_margin_note"]}
CHECK_PRETAX_MARGIN = {h["check_pretax_margin"]}   # {h["check_pretax_note"]}
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}
KIND_TEXT     = {R(h["kind_text"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} outlook ──
LATEST          = {R(LATEST)}
PREV_SEG        = {R(prev_seg)}   # the previous print's net margin growth
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # no revenue guide in numbers: the latest quarter's revenue growth as reported
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no margin guide, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {fy_rev:.2f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {round(latest["diluted_shares_m"] / 1000, 4)!r}   # diluted shares, bn
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenues {h['prev_fy_sales_growth']:+.1f}%; {franchise_q}")}
BALANCE_TEXT    = {R(f"{h['fcf_label']} free cash flow {fcf_text} (consolidated), dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
ACTIVITY_TEXT   = {R(activity)}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/OKE)")
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
