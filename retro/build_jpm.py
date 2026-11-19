#!/usr/bin/env python3
"""
Build JPM retrospective models from the dated fact sheet (retro/facts/JPM.json).

The JPM sibling of build_goog.py: the same frozen rules (retro method r2), the same weekly dates and the same market statistics, with
a bank's signal set and JPMorgan Chase's own rule-T thresholds (retro/templates/jpm_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage and prints whose 'published' date is <= AS_OF (and a print's 10-Q restatement from its date),
  2. computes every market statistic from daily prices truncated at AS_OF (Yahoo's JPM series; its two splits, 1998 and 2000, precede
     the P/E window, so every price is the close as traded),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

JPMorgan Chase's fiscal year is the calendar year. The method r2 inputs map as follows (retro/README.md, "JPM"; decided before any JPM
model was built or scored):
  - revenue: total net revenue on the reported basis (noninterest revenue plus net interest income), the income statement's own
    total; the managed basis, which adds back securitized credit card results and tax-equivalent adjustments, is not used;
  - EPS: diluted EPS from continuing operations (before the 2008 extraordinary gain), each year from the latest filing that reports
    it; where an earnings supplement on the same basis publishes the figure excluding merger costs, that figure (the ACN rule): FY2005
    on. FY2002 is a distorted year (the AAPL FY2002 test) whose operating EPS was published on an earlier basis (the UNP trucking rule),
    so the history and the P/E window start with FY2003 ('eps_first_excluded', 'pe_window_start');
  - current-FY EPS: no filing of the period gives an EPS guide, so the last full year in the history stands (the rollover rule);
  - forward revenue growth: no filing of the period guides revenue in numbers (the releases and slides give credit-loss and
    segment outlooks only), so the latest quarter's revenue growth stands in (the UNP rule);
  - guided margin step: none (no margin guide); the margin signal uses the latest quarter's pre-tax margin change;
  - a quarter's figure its own 10-Q restates (nonperforming assets, Q2 and Q3 2008 and Q1 2012) takes the 10-Q's figures from the
    10-Q's date, and a quarter a later release prints as restated (Q1 2012, the synthetic credit portfolio) takes that release's from
    its date ('restated', a list in publication order: a quarter from the latest filing that reports it);
  - a Q4 supplement that republishes the previous year's company figure on a revised basis restates it in the history from its own
    date ('restates' on the full-year actuals: FY2008 at $0.88 from the Q4 2009 supplement);
  - dividend: the latest declared quarterly rate, each from the first filing that states it ('dividends').
The kind is DURABLE: the 10-Ks tie results to markets and the economy but do not call the business cyclical (the LOW and SHW
reading). No disruption theme in taxonomy_eras.json is live for a bank holding company in 2008-2009, so the builder refuses events
until a theme encoding is decided, and it refuses guides, listings, splits and company names until their encodings are decided.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. JPMorgan Chase released before the open, so a print's date is its release day and the weekly date
is the next trading day.

Output goes to staging/retrospective/JPM until the series is added to the archive (--out archive/retrospective/JPM).

Usage
  python3 retro/build_jpm.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_jpm.py --weekly 2009-01-05 2009-12-31
  python3 retro/build_jpm.py --weekly 2010-01-04 2013-12-31
  python3 retro/build_jpm.py 2008-04-17
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/JPM/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "JPM.json")
ENGINE = os.path.join(HERE, "templates", "jpm_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "JPM")
SYMBOL = "JPM"
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"revenue": (-33, -12, 10, 29), "credit_cost": (1340, 670, 0, -1020), "expense_gap": (65, 29, -7, -17),
                     "npa_gap": (231, 109, -12, -85), "pretax_margin": (-3910, -1760, 400, 2200)}
RULE_T_KEYS = {"revenue": (1, False), "credit_cost": (10, True), "expense_gap": (1, True), "npa_gap": (1, True),
               "pretax_margin": (10, False)}           # (rounding unit, lower is better)


def fiscal_year(day):
    """The fiscal year a calendar day belongs to: JPMorgan Chase's fiscal year is the calendar year."""
    return int(day[:4])


def rule_t_value(k, r):
    """One annual rule-T value from its raw figures ($ millions, (prior, current))."""
    pct = lambda a, b: (b / a - 1) * 100
    if k == "revenue":
        return round(pct(*r["revenue_m"]) + 0.0, 2)
    if k == "credit_cost":
        (p0, p1), (a0, a1) = r["provision_m"], r["revenue_m"]
        return round((p1 / a1 - p0 / a0) * 10000 + 0.0, 1)
    if k == "expense_gap":
        return round(pct(*r["expense_m"]) - pct(*r["revenue_m"]) + 0.0, 2)
    if k == "npa_gap":
        return round(pct(*r["npa_m"]) - pct(*r["loans_m"]) + 0.0, 2)
    (o0, o1), (a0, a1) = r["pretax_m"], r["revenue_m"]
    return round((o1 / a1 - o0 / a0) * 10000 + 0.0, 1)


def rule_t(rt):
    """Rule T thresholds from the annual values (re-derived from the raw figures): XBULL best, BULL median, BASE worst, BEAR one
    median-to-worst step beyond the worst; rounded half up to whole percent or points and to 10 bp."""
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


def derived(r):
    """A print's growth, credit cost, margins and gaps from its raw published figures ($ millions)."""
    pct = lambda a, b: (b / a - 1) * 100
    r1 = lambda x: round(x + 0.0, 1)
    cc, cc0 = r["provision_m"] / r["revenue_m"] * 100, r["provision_prior_m"] / r["revenue_prior_m"] * 100
    pm, pm0 = r["pretax_m"] / r["revenue_m"] * 100, r["pretax_prior_m"] / r["revenue_prior_m"] * 100
    return dict(sales_pct=r1(pct(r["revenue_prior_m"], r["revenue_m"])), seq_pct=r1(pct(r["revenue_prev_q_m"], r["revenue_m"])),
                credit_cost=round(cc + 0.0, 2), credit_cost_bp=r1((cc - cc0) * 100), pretax_margin=round(pm + 0.0, 2),
                pretax_margin_bp=r1((pm - pm0) * 100), expense_pct=r1(pct(r["expense_prior_m"], r["expense_m"])),
                expense_gap_pp=r1(pct(r["expense_prior_m"], r["expense_m"]) - pct(r["revenue_prior_m"], r["revenue_m"])),
                npa_pct=r1(pct(r["npa_prior_m"], r["npa_m"])), loans_pct=r1(pct(r["loans_prior_m"], r["loans_m"])),
                npa_gap_pp=r1(pct(r["npa_prior_m"], r["npa_m"]) - pct(r["loans_prior_m"], r["loans_m"])))


def check_print(p, as_of):
    """Re-derive a print's (and its restatement's, once public) margins, growth and gaps from its raw figures; they must match the
    fact sheet."""
    for x in [p] + [r for r in p.get("restated", []) if r["published"] <= as_of]:
        for k, v in derived(x["raw"]).items():
            assert x[k] == v, (p["quarter"], k, x[k], v)


def as_restated(p, as_of):
    """A print with its restatements applied, in order, once each is public (a quarter from the latest filing that reports it): a 10-Q
    that reports a figure differently from the release, or a later release that prints the quarter as restated."""
    q = p
    for rs in p.get("restated", []):
        if rs["published"] <= as_of:
            q = {**q, **{k: v for k, v in rs.items() if k not in ("published", "source", "rows")}}
            q["extra_sources"] = list(q.get("extra_sources", [])) + [rs["source"]]
    return q


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    chart = retro_tool.chart(SYMBOL)
    assert retro_tool.split_factor(chart, as_of) == 1.0, "a split after AS_OF needs an encoding ('splits')"
    px = raw
    # no filing guides revenue, EPS or a margin in numbers, and none states a listing change, a split or a change of company name:
    # the builder refuses any such fact, and any event, until its encoding is decided
    for kind in ("guides", "listings", "splits", "company_names", "events"):
        if [x for x in facts.get(kind, []) if x.get("published", x.get("effective", "")) <= as_of]:
            sys.exit(f"{as_of}: the JPM builder has no encoding for {kind}; decide one first")
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        check_print(p, as_of)
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    # prints published by AS_OF that report a fiscal year after the history (a Q4 print reports the year just ended, so it stays in
    # scope after the 10-K that follows it)
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    public = [as_restated(p, as_of) for p in facts["prints"] if p["published"] <= as_of]
    prints = [p for p in public if guide_fy(p) >= first_fy]
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is public yet")
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage
    h = {**h, "extended": ""}
    for p in prints:
        a = p.get("fy_actual")
        if a and a["fy"] not in reported(h):          # the 10-K vintage, once out, wins
            y = str(a["fy"])
            if a["eps_normalized"] is None:           # a loss year: reported, but out of the EPS history
                h.update(eps_excluded={**h.get("eps_excluded", {}), y: a["excluded_note"]})
            h.update(fy_label=a["fy_label"],
                     eps_normalized={**h["eps_normalized"], **({y: a["eps_normalized"]} if a["eps_normalized"] is not None else {})},
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]},
                     # a Q4 release that prints no full-year diluted share count (Q4 2015, Q4 2016) leaves the share history as
                     # it was until the 10-K
                     diluted_shares_m={**h["diluted_shares_m"],
                                       **({y: a["diluted_shares_m"]} if a["diluted_shares_m"] is not None else {})},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_op_margin=a["op_margin"], prev_fy_op_margin_note=a["op_margin_note"],
                     prev_fy_pretax_margin=a["pretax_margin"], prev_fy_pretax_margin_note=a["pretax_margin_note"],
                     prev_fy_credit_cost=a["credit_cost"], prev_fy_sales_growth=a["sales_growth"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
            if a.get("restates"):                     # an earlier year's company figure the same supplement republishes on a revised basis
                h.update(eps_normalized={**h["eps_normalized"], **a["restates"]},
                         normalization=f'{h["normalization"]}; {a["restates_note"]}')
    latest = prints[-1]
    # the previous quarter is the print published just before the latest one (in or out of the history's scope)
    i = public.index(latest)
    assert i > 0, (as_of, "the fact sheet needs the print before the latest one")
    prev = (public[i - 1]["sales_pct"], public[i - 1]["quarter"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}   # reported history only: the rules use this
    excluded = {int(k): v for k, v in h.get("eps_excluded", {}).items()}
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)        # the last full year in the history: cur_fy - 1 unless that year is excluded
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── current-FY EPS: no EPS guide in any filing of the period, so the last full year's EPS stands ──
    eps_now = eps_hist[last_fy]
    eps_label = f"{fy_e}: no EPS guide in numbers, FY{last_fy % 100:02d}'s ${money(eps_now)} stands" + "".join(
        f" (FY{y % 100:02d} is excluded: {excluded[y]})" for y in range(last_fy + 1, cur_fy))
    eps_label_short = (f"{fy_e}: no EPS guide in numbers, FY{last_fy % 100:02d}'s ${money(eps_now)} stands (FY" +
                       ", FY".join(f"{y % 100:02d}" for y in range(last_fy + 1, cur_fy)) + " excluded)") if cur_fy > last_fy + 1 else eps_label
    # ── forward revenue growth: no revenue guide in any filing, so the latest quarter's revenue growth (the UNP rule) ──
    fwd = [latest["sales_pct"]] * 2
    fwd_label = f"{latest['quarter']} revenue growth (no {next_q} guide)"
    fwd_short, fwd_period = f"{latest['quarter'].split()[0]} revenue YoY", latest["quarter"]
    guide_text = (f"{next_q}: no revenue, EPS or margin guide in numbers in any filing; the latest quarter's revenue growth stands in "
                  "(the UNP rule); the releases, 10-Qs and investor slides give credit-loss and segment outlooks only, which method r2 "
                  "has no input for")
    cat3 = (f"(3) A {next_q} revenue guide — none: JPMorgan Chase gives no firm-wide revenue, EPS or margin outlook in any filing; "
            "net charge-offs and reserve builds by business are in each supplement")
    margin_guided = False                          # no margin guide: no guided step; the signal uses the latest quarter's change
    fy_margin_base = h["prev_fy_op_margin"]

    # ── dividend: the latest declared quarterly rate, each from the first filing that states it ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts.get("dividends", []) if d["published"] <= as_of]
    _, dividend, dividend_note, dividend_src = max(divs, key=lambda x: x[0])
    exchange = h["exchange"]

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
    # the window: up to ten years, from the first year in the history (2003-01-01: the excluded FY2002 and the years before it leave)
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

    # ── era-dependent text, from facts only: no disruption theme has dated evidence on AS_OF ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
    key_tail = ("A credit downturn shows up in nonperforming assets and the provision first;\n"
                "  the bear needs it in net revenue as well.")
    theme_summary = "no disruption theme has dated evidence"
    cat4 = (f"(4) Nonperforming assets — {latest['npa_pct']:+.1f}% against loans {latest['loans_pct']:+.1f}% in {latest['quarter']} "
            f"({latest['npa_gap_pp']:+.1f}pp): problem loans outgrowing the book would show here first")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    # only a print public before the open can meet AS_OF's close: JPMorgan Chase released before the open, so a print dated AS_OF
    # occurs only in a week with no trading day after it
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    company = h["company"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])]
           + [public[i - 1]["source"]] + ([dividend_src] if dividend_src else []))
    sources = [dict(id=x, **facts["sources"][x]) for x in dict.fromkeys(ids)]
    sources.append({"id": "Y0", "published": as_of, "title": "Yahoo Finance daily prices, JPM and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/JPM/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E "
                                f"distribution from {window[0]}"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "seq_pct", "credit_cost", "credit_cost_bp", "pretax_margin",
                   "pretax_margin_bp", "expense_pct", "expense_gap_pp", "npa_b", "npa_pct", "loans_pct", "npa_gap_pp", "eps_q",
                   "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    first_excl = "; ".join(f"FY{int(y) % 100:02d} {t}" for y, t in sorted(h.get("eps_first_excluded", {}).items()))
    rev_text = (f"Revenue: {latest['sales_note']}; {latest['credit_note']}; {latest['eps_note']}; {latest['shares_note']}"
                + (f"; {latest['note']}" if latest.get("note") else ""))
    cash_return = f"dividend {dividend_note}; Tier 1 capital ratio {latest['tier1']:.1f}% at the end of {latest['quarter']}"
    R = repr
    head = f'''#!/usr/bin/env python3
"""
JPM Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: JPM)  ·  {h["business_line"]}
Generated by retro/build_jpm.py from retro/facts/JPM.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "JPM"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); net revenue, credit cost, expense, "
               "nonperforming-asset and pre-tax margin signals with JPMorgan Chase's rule-T thresholds")
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
EXCHANGE        = {R(exchange)}   # display only
CURRENT_PRICE   = {close:.2f}   # USD, {exchange} close {as_of}, as traded
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2
PE_PCTL         = {R(pctl)}   # current-FY P/E over the window below
PE_NOW_PCTL     = {pe_now_pctl}    # share of those daily P/Es at or below the AS_OF one
WINDOW_LABEL    = {R(window_label)}   # P/E window: {window[0]} .. AS_OF ({len(window)} trading days; from the first year in the history)
YEARLY_MIN_PE   = {R(yearly)}   # (calendar year, lowest P/E, date)
VOL_ANNUAL_PCT  = {vol:.3f}   # 1-yr realized, daily log returns
VOL_BETA        = {beta:.2f}    # 1-yr beta vs S&P 500
VOL_52W_LOW     = {low52:.2f}
VOL_52W_HIGH    = {high52:.2f}
REF_LOW         = {px[ref][2]:.2f}   # lowest close of the last 52 weeks, {ref}
REF_LOW_LABEL   = {R(MONTHS[int(ref[5:7]) - 1])}

# ── FACTS: company history ({", ".join(h["sources"])}, vintage {h["published"]}{h["extended"]}) ──
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}
EPS_FIRST_EXCLUDED = {R(first_excl)}
EPS_EXCLUDED  = {R({y: t for y, t in sorted(excluded.items())})}
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # total net revenue, reported basis, USD bn
SHARES_HIST   = {R({y: round(v, 3) for y, v in shares.items()})}   # diluted, millions
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # pre-tax margin, {h["prev_fy_op_margin_note"]}
CHECK_PRETAX_MARGIN = {h["prev_fy_pretax_margin"]}   # pre-tax margin for the EPS check (display), {h["prev_fy_pretax_margin_note"]}
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and the {next_q} outlook ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_SALES      = {R(prev)}
EPP_TODAY_EPS   = {round(eps_now, 6)}   # {eps_label_short}
EPS_LABEL       = {R(eps_label_short)}
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
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} total net revenue {h['prev_fy_sales_growth']:+.1f}%, provision {h['prev_fy_credit_cost']:.1f}% of revenue; {latest['quarter'].split()[0]} provision {latest['credit_cost']:.1f}% of revenue ({latest['credit_cost_bp']:+.0f}bp YoY)")}
BALANCE_TEXT    = {R(f"Tier 1 capital ratio {latest['tier1']:.1f}%, nonperforming assets ${latest['npa_b']:.3f}B ({latest['npa_pct']:+.1f}% YoY) at the end of {latest['quarter']}, dividend ${dividend:.2f} a year")}
REVENUE_TEXT    = {R(rev_text)}
CAPITAL_RETURN  = {R(cash_return)}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/JPM)")
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
