#!/usr/bin/env python3
"""
Build GOOG retrospective models from the dated fact sheet (retro/facts/GOOG.json).

The GOOG sibling of build_mu.py: the same frozen rules (retro method r2), the same weekly dates and the same market statistics, with
the NVDA and MU signal set, receivables in the place of inventories, and Google's own rule-T thresholds
(retro/templates/goog_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage and prints whose 'published' date is <= AS_OF (and a print's 10-Q restatement from its date),
  2. computes every market statistic from daily prices truncated at AS_OF (Yahoo's GOOG series before 2014 is the Class A common
     stock that traded as NASDAQ: GOOG; its later share distributions are undone, so every price is the close as traded),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Google's fiscal year is the calendar year. The method r2 inputs map as follows (retro/README.md, "GOOG"; decided before any GOOG
model was built or scored):
  - EPS: GAAP diluted EPS, each year from the latest filing that reports it, except FY2004 at the company's figure before material
    non-recurring items ($1.49; GAAP $1.46: the ACN rule). The releases' non-GAAP EPS from Q4 2005 removes stock-based compensation,
    which recurs, so no later year has a figure excluding only one-offs. FY1999 and FY2000 are losses and the first years, so the
    history starts with FY2001 ('eps_first_excluded'); the P/E window starts at the listing, 2004-08-19 ('pe_window_start');
  - current-FY EPS: no filing of the period gives an EPS guide, so the last full year in the history stands (the rollover rule);
  - forward revenue growth: no filing of the period guides revenue in numbers (the 10-Ks say in words that the growth rate will
    decline, display only; the releases estimate stock-based compensation, dilution and capital expenditure only), so the latest
    quarter's revenue growth stands in (the UNP rule);
  - guided margin step: none (no margin guide); the margin signal uses the latest quarter's operating-margin change;
  - a quarter its own 10-Q restates (Q3 2008: the Authors Guild and AAP settlement, agreed after the release and expensed in the
    quarter) takes the 10-Q's figures from the 10-Q's date ('restated'; the history rule, a quarter from the latest filing that
    reports it).
The kind is CYCLICAL: each 10-K says so of its own business ("the cyclicality and seasonality in our business"; the BKR, CAT and NVDA
reading). No disruption theme in taxonomy_eras.json is live for a search and advertising company in 2008-2009, so the builder refuses
events until a theme encoding is decided, and it refuses guides, dividends and listings until their encodings are decided.
From 2014 (retro/README.md, "GOOG 2014-2017"): the Class C dividend of 2014 is a two-for-one split ('splits', effective on its record
date 2014-03-27, Yahoo's split date), and every history figure is restated on the basis of the filing it comes from; Yahoo's GOOG series
is the Class C capital stock from that date, and EPS is the priced class's (Class C from the split); Alphabet Inc. is the successor
issuer from its 8-K12B ('company_names', the ACN rule); a Q4 release that prints no full-year diluted share count leaves the share
history as it was until the 10-K.
From 2022 (retro/README.md, "GOOG 2022-2026"): the 20-for-one stock dividend of 2022 is a split ('splits', effective on the first
split-adjusted trading day, 2022-07-18, Yahoo's split date); dividends, from the first in April 2024, are the latest declared rate, each
from the first filing that states it (the MSFT rule); GENAI (live from 2022-11-30 and scoped to generative AI substituting search among
other products) joins the watch list from the first 10-K whose competition risk factor names other companies' AI products
(genai_company_acknowledged, the FY2023 10-K; the MSFT rule), company-acknowledged with no market read: its factor pair nets to zero and
the theme signal stays at 2/4, so only text changes; a 10-K's words are replaced by the next 10-K's.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. Google released after the close on Thursdays, so a print is dated the Friday, the week's last
trading day, and meets its close (public before the open; the AVGO rule).

Output goes to staging/retrospective/GOOG until the series is added to the archive (--out archive/retrospective/GOOG).

Usage
  python3 retro/build_goog.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_goog.py --weekly 2009-01-05 2009-12-31
  python3 retro/build_goog.py 2008-04-18
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/GOOG/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "GOOG.json")
ENGINE = os.path.join(HERE, "templates", "goog_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "GOOG")
SYMBOL = "GOOG"
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"revenue": (-88, 73, 234, 8585), "gross_margin": (-2910, -1350, 210, 38090), "opex_gap": (183, 72, -38, -8252),
                     "receivables_gap": (55, 28, 2, -84), "op_margin": (-5090, -1910, 1280, 288470)}
RULE_T_KEYS = {"revenue": (1, False), "gross_margin": (10, False), "opex_gap": (1, True), "receivables_gap": (1, True),
               "op_margin": (10, False)}           # (rounding unit, lower is better)


def fiscal_year(day):
    """The fiscal year a calendar day belongs to: Google's fiscal year is the calendar year."""
    return int(day[:4])


def rule_t_value(k, r):
    """One annual rule-T value from its raw figures ($ thousands, (prior, current))."""
    pct = lambda a, b: (b / a - 1) * 100
    if k == "revenue":
        return round(pct(*r["revenue_k"]) + 0.0, 2)
    if k == "gross_margin":
        (c0, c1), (a0, a1) = r["cost_k"], r["revenue_k"]
        return round(((a1 - c1) / a1 - (a0 - c0) / a0) * 10000 + 0.0, 1)
    if k == "op_margin":
        (o0, o1), (a0, a1) = r["op_income_k"], r["revenue_k"]
        return round((o1 / a1 - o0 / a0) * 10000 + 0.0, 1)
    if k == "opex_gap":
        (d0, d1), (s0, s1), (g0, g1), (a0, a1) = r["rd_k"], r["sm_k"], r["ga_k"], r["revenue_k"]
        return round(pct(d0 + s0 + g0, d1 + s1 + g1) - pct(a0, a1) + 0.0, 2)
    (i0, i1), (a0, a1) = r["receivables_k"], r["revenue_k"]
    return round(pct(i0, i1) - pct(a0, a1) + 0.0, 2)


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
    """A print's margins, growth and gaps from its raw published figures ($ thousands)."""
    pct = lambda a, b: (b / a - 1) * 100
    r1 = lambda x: round(x + 0.0, 1)
    gm, gm0 = r["gross_profit_k"] / r["sales_k"] * 100, r["gross_profit_prior_k"] / r["sales_prior_k"] * 100
    om, om0 = r["op_income_k"] / r["sales_k"] * 100, r["op_income_prior_k"] / r["sales_prior_k"] * 100
    ox, ox0 = r["rd_k"] + r["sm_k"] + r["ga_k"], r["rd_prior_k"] + r["sm_prior_k"] + r["ga_prior_k"]
    return dict(sales_pct=r1(pct(r["sales_prior_k"], r["sales_k"])), seq_pct=r1(pct(r["sales_prev_q_k"], r["sales_k"])),
                gross_margin=round(gm + 0.0, 2), gross_margin_bp=r1((gm - gm0) * 100), op_margin=round(om + 0.0, 2),
                op_margin_bp=r1((om - om0) * 100), opex_pct=r1(pct(ox0, ox)), opex_gap_pp=r1(pct(ox0, ox) - pct(r["sales_prior_k"], r["sales_k"])),
                receivables_pct=r1(pct(r["receivables_prior_k"], r["receivables_k"])),
                receivables_gap_pp=r1(pct(r["receivables_prior_k"], r["receivables_k"]) - pct(r["sales_prior_k"], r["sales_k"])))


def check_print(p, as_of):
    """Re-derive a print's (and its restatement's, once public) margins, growth and gaps from its raw figures; they must match the
    fact sheet."""
    for x in [p] + ([p["restated"]] if p.get("restated") and p["restated"]["published"] <= as_of else []):
        for k, v in derived(x["raw"]).items():
            assert x[k] == v, (p["quarter"], k, x[k], v)


def as_restated(p, as_of):
    """A print with its 10-Q restatement applied once the 10-Q is public (the 10-Q is the latest filing reporting the quarter)."""
    rs = p.get("restated")
    if not rs or rs["published"] > as_of:
        return p
    q = {**p, **{k: v for k, v in rs.items() if k not in ("published", "source", "rows")}}
    q["extra_sources"] = list(p.get("extra_sources", [])) + [rs["source"]]
    return q


def on_basis(facts, as_of):
    """The fact sheet with every per-share fact on the AS_OF share basis: a split effective on or before AS_OF divides per-share values
    whose share basis predates it and multiplies share counts by it (the NVDA helper). A history figure's basis is the date of the
    filing it comes from (each year from the latest filing that reports it: 'eps_sources', 'shares_sources'), unless 'share_basis'
    says otherwise; a print's is its own date. Google's one split in scope is the Class C distribution (2014-03-27): before it this
    is the identity."""
    f = copy.deepcopy(facts)
    splits = [s for s in f.get("splits", []) if s["effective"] <= as_of]
    k = lambda basis: math.prod(s["ratio"] for s in splits if basis < s["effective"])
    pub = lambda v, kind, y: (f["sources"][v[kind][y]]["published"] if y in v.get(kind, {}) else v["published"])
    for v in f["history_vintages"]:
        eps_basis = lambda y: v.get("share_basis", {}).get(y, pub(v, "eps_sources", y))
        shares_basis = lambda y: v.get("share_basis", {}).get(y, pub(v, "shares_sources", y))
        v["eps_normalized"] = {y: e / k(eps_basis(y)) for y, e in v["eps_normalized"].items()}
        v["diluted_shares_m"] = {y: n * k(shares_basis(y)) for y, n in v["diluted_shares_m"].items()}
        notes = []
        for s in splits:
            restated = [y for y in sorted(v["eps_normalized"]) if eps_basis(y) < s["effective"]]
            if restated:
                notes.append(f"per share ÷{s['ratio']:g} for the split effective {s['effective']} ({s['source']}) on "
                             f"FY{restated[0][2:]}-FY{restated[-1][2:]}")
        v["split_note"] = "; ".join(notes)
    for p in f["prints"]:
        r = k(p["published"])
        for x in [p] + ([p["restated"]] if p.get("restated") else []):
            for key in ("eps_q", "eps_q_prior"):
                if key in x:
                    x[key] = x[key] / r
            if "diluted_shares_m" in x:
                x["diluted_shares_m"] = x["diluted_shares_m"] * r
        if p.get("fy_actual") and p["fy_actual"]["eps_normalized"] is not None:
            p["fy_actual"]["eps_normalized"] /= r
        if p.get("fy_actual") and p["fy_actual"]["diluted_shares_m"] is not None:
            p["fy_actual"]["diluted_shares_m"] *= r
    for d in f.get("dividends", []):
        d["quarterly"] /= k(d["published"])
    for v in f["history_vintages"]:
        if v.get("dividend_annual") is not None:
            v["dividend_annual"] /= k(v["published"])
    return f, [s["source"] for s in splits]


def _usd_b(x):
    return f"${x:.3f}B" if x >= 0 else f"$({-x:.3f})B"


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    chart = retro_tool.chart(SYMBOL)
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat()
                    for v in chart.get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo_splits for s in facts.get("splits", [])), "a split's effective date must match the price data"
    # no filing guides revenue, EPS or a margin in numbers and none states a listing change: the builder refuses any such fact until
    # its encoding is decided (a change of company name is applied below: Alphabet Inc., the successor issuer; dividends, from 2024, are
    # the latest declared rate)
    for kind in ("guides", "listings"):
        if [x for x in facts.get(kind, []) if x["published"] <= as_of]:
            sys.exit(f"{as_of}: the GOOG builder has no encoding for {kind}; decide one first")
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        check_print(p, as_of)
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    facts, split_ids = on_basis(facts, as_of)
    split_dates = [s["effective"] for s in facts.get("splits", []) if s["effective"] <= as_of]
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
    # no disruption theme in taxonomy_eras.json is live for a search and advertising company to 2022-11-29. The one encoding decided
    # (retro/README.md, "GOOG 2022-2026"): each 10-K whose competition risk factor names other companies' AI products puts GENAI (live
    # from 2022-11-30) on the watch list with that 10-K's words (genai_company_acknowledged; a 10-K's wording is replaced by the next
    # 10-K's, an event without a 'doc' would stay in scope once public). Any other event kind needs its encoding decided first
    events = [e for e in facts["events"] if e["published"] <= as_of and (h["published"] <= e["published"] or "doc" not in e)]
    if any(e["kind"] != "genai_company_acknowledged" for e in events):
        sys.exit(f"{as_of}: the GOOG builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
    themes = retro_tool.load_taxonomy()["themes"]
    events = [e for e in events if themes[e["theme"]]["live_from"] <= as_of]      # a theme counts only from its live date
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
                     prev_fy_gross_margin=a["gross_margin"], prev_fy_sales_growth=a["sales_growth"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
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
                  f"(the UNP rule); in words only, the {h['fy_label']} 10-K: '{h['outlook_words']}' (display only); the releases "
                  "estimate stock-based compensation, dilution and capital expenditure, which method r2 has no input for")
    cat3 = (f"(3) A {next_q} revenue guide — none: Google gives no revenue, EPS or margin outlook in any filing; aggregate paid "
            "clicks and traffic acquisition costs are in each release")
    margin_guided = False                          # no margin guide: no guided step; the signal uses the latest quarter's change
    fy_margin_base = h["prev_fy_op_margin"]

    # ── dividend: never declared or paid (each 10-K's Item 5) ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts.get("dividends", []) if d["published"] <= as_of]
    if h["dividend_annual"] is not None:
        divs.append((h["published"], h["dividend_annual"], h["dividend_note"], None))
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
    # the window: up to ten years, from the listing (2004-08-19; the r2 listing rule)
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
    key_tail = ("An advertising slowdown shows up in paid clicks and revenue growth first;\n"
                "  the bear needs it in gross margin as well.")
    theme_summary = "no disruption theme has dated evidence"
    cat4 = (f"(4) Receivables — {latest['receivables_pct']:+.1f}% against revenue {latest['sales_pct']:+.1f}% in {latest['quarter']} "
            f"({latest['receivables_gap_pp']:+.1f}pp): advertisers paying more slowly would show here first")
    for e in [e for e in events if e["kind"] == "genai_company_acknowledged"][-1:]:
        # GENAI is live from 2022-11-30 and its scope names search; the latest 10-K's competition risk factor names other companies' AI
        # products, so it joins the watch list (the MSFT rule: company-acknowledged, no market read). The factor pair nets to zero and the
        # theme signal stays at 2/4, so only text changes; re-filing needs dated evidence of the market pricing it for Google
        val_word = "a premium" if pe_now_pctl >= 70 else "a discount to its own history" if pe_now_pctl <= 30 else "near its own median"
        stage = "genai"
        watch = [{"theme": "GENAI", "status": "live, company-acknowledged; no market read",
                  "reason": (f"Live: Alphabet's own {e['doc']}, under '{e['heading']}', says '{e['risk_quote']}' and '{e['rival_quote']}'"
                             + (f" and that '{e['usage_quote']}'" if e.get("usage_quote") else "") +
                             f" It builds generative AI of its own: '{e['offering']}' The stock trades at {close / eps_now:.1f}x {fy_e_s} — "
                             f"{val_word}. Re-file as DISRUPTION_EXPOSED (GENAI) only if dated evidence shows the market pricing "
                             "generative-AI substitution of Google Search specifically.")}]
        factors = [(f"Generative AI: {e['offering_short']}", 0.2, 0.10),
                   (f"AI competition ({e['doc']}): {e['risk_short']}", -0.2, 0.10)]
        sig_name = "Generative AI: net effect on Search and advertising"
        trigger = "Users take queries to other companies' AI products faster than Google's own AI keeps them"
        theme_summary = "generative AI is live and company-acknowledged; no dated evidence ties the multiple to it"

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    # only a print public before the open can meet AS_OF's close: Google released after the previous day's close, so a print dated
    # AS_OF occurs only in a week with no trading day after it (a Friday)
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    # a change of company name filed after the vintage (the ACN rule; Alphabet Inc., the successor issuer, from its 8-K12B)
    renames = [n for n in facts.get("company_names", []) if h["published"] < n["published"] <= as_of]
    company = renames[-1]["name"] if renames else h["company"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])]
           + [public[i - 1]["source"]] + ([dividend_src] if dividend_src else []) + split_ids + [n["source"] for n in renames]
           + [e["id"] for e in events])
    # the security priced: Yahoo's GOOG series is the Class A common stock before the Class C distribution, the Class C capital stock
    # from its split date (the first split, 2014-03-27; the 2022 split is a split of the same stock)
    security = (f"; the Class C capital stock (Yahoo's GOOG series from {split_dates[0]})" if split_dates else "")
    sources = [dict(id=x, **facts["sources"][x]) for x in dict.fromkeys(ids)]
    sources.append({"id": "Y0", "published": as_of, "title": "Yahoo Finance daily prices, GOOG and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/GOOG/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E "
                                f"distribution from {window[0]}"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "seq_pct", "gross_margin", "gross_margin_bp", "op_margin",
                   "op_margin_bp", "opex_pct", "opex_gap_pp", "receivables_b", "receivables_pct", "receivables_gap_pp", "eps_q",
                   "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    first_excl = "; ".join(f"FY{int(y) % 100:02d} {t}" for y, t in sorted(h.get("eps_first_excluded", {}).items()))
    rev_text = (f"Revenue: {latest['sales_note']}; {latest['receivables_note']}; {latest['eps_note']}; {latest['shares_note']}"
                + (f"; {latest['note']}" if latest.get("note") else ""))
    cash_return = latest["cash_return_text"] or h["cash_return_text"]
    R = repr
    head = f'''#!/usr/bin/env python3
"""
GOOG Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: GOOG)  ·  {h["business_line"]}
Generated by retro/build_goog.py from retro/facts/GOOG.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "GOOG"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); revenue, margin, expense and "
               "receivables signals with Google's rule-T thresholds")
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
CURRENT_PRICE   = {close:.2f}   # USD, {exchange} close {as_of}, as traded{security}
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2
PE_PCTL         = {R(pctl)}   # current-FY P/E over the window below
PE_NOW_PCTL     = {pe_now_pctl}    # share of those daily P/Es at or below the AS_OF one
WINDOW_LABEL    = {R(window_label)}   # P/E window: {window[0]} .. AS_OF ({len(window)} trading days; from the listing)
YEARLY_MIN_PE   = {R(yearly)}   # (calendar year, lowest P/E, date)
VOL_ANNUAL_PCT  = {vol:.3f}   # 1-yr realized, daily log returns
VOL_BETA        = {beta:.2f}    # 1-yr beta vs S&P 500
VOL_52W_LOW     = {low52:.2f}
VOL_52W_HIGH    = {high52:.2f}
REF_LOW         = {px[ref][2]:.2f}   # lowest close of the last 52 weeks, {ref}
REF_LOW_LABEL   = {R(MONTHS[int(ref[5:7]) - 1])}

# ── FACTS: company history ({", ".join(h["sources"])}, vintage {h["published"]}{h["extended"]}) ──
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}{"; " + h["split_note"] if h.get("split_note") else ""}
EPS_FIRST_EXCLUDED = {R(first_excl)}
EPS_EXCLUDED  = {R({y: t for y, t in sorted(excluded.items())})}
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # revenues, USD bn
SHARES_HIST   = {R({y: round(v, 3) for y, v in shares.items()})}   # diluted, millions
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # operating margin, {h["prev_fy_op_margin_note"]}
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
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenues {h['prev_fy_sales_growth']:+.1f}%, gross margin {h['prev_fy_gross_margin']:.1f}%; {latest['quarter'].split()[0]} gross margin {latest['gross_margin']:.2f}% ({latest['gross_margin_bp']:+.0f}bp YoY)")}
BALANCE_TEXT    = {R(f"Cash, cash equivalents and marketable securities ${latest['cash_b']:.3f}B, {latest['debt_note']} ({latest['quarter']}), {h['fcf_label']} free cash flow {_usd_b(h['fcf_b'])} ({h['fcf_note']}), " + (f"dividend ${dividend:.2f} a year" if dividend else "no dividend"))}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/GOOG)")
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
