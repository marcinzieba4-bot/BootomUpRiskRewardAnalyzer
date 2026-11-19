#!/usr/bin/env python3
"""
Build V retrospective models from the dated fact sheet (retro/facts/V.json).

The V sibling of build_goog.py: the same frozen rules (retro method r2), the same weekly dates and the same market statistics, with a
payments network's signal set and Visa's own rule-T thresholds (retro/templates/v_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage and prints whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF (Yahoo's V series is the class A common stock, NYSE: V, from
     its 2008-03-19 listing; the four-for-one split of 2015-03-19 is undone, so every price is the close as traded),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Visa's fiscal year ends on September 30 (FY2009 = 2008-10-01 to 2009-09-30). The method r2 inputs map as follows (retro/README.md,
"V"; decided before any V model was built or scored):
  - revenue: total operating revenues (service, data processing, international transaction and other revenues, net of volume and
    support incentives), each year from the latest filing that reports it;
  - EPS: GAAP diluted EPS of the class A common stock (class B and C as converted), each year from the latest filing that reports it;
    a company figure excluding only one-offs where one is published (the ACN rule): none is, as Visa's adjusted figures also remove
    asset step-up amortization, which recurs (the NKE FY2007, AVGO and PFE rule). FY2008, Visa Inc.'s first year with EPS (Visa U.S.A.
    was a non-stock company), is a distorted year (the AAPL FY2002 test: its covered-litigation reserve exceeds its net income after
    tax), so the history and the P/E window start after it ('eps_first_excluded', 'pe_window_start' 2008-10-01). Until the Q4 FY09
    print no year is in the history, and the builder refuses the date: no V model exists before 2009-10-28;
  - current-FY EPS: the EPS guide ("growth of greater than 20%") is a one-sided bound and gives no field (the PEP, UNP and LOW rule),
    so the last full year in the history stands (the rollover rule);
  - forward revenue growth: Visa guides the fiscal year's net revenue growth, not the next quarter's, so the fiscal-year range stands
    in (method r2's fallback, "No next-quarter guide"): the Q4 FY09 print's FY2010 "at the lower end of the 11% to 15% range" keeps the
    11-15% range, the words in the note (the ACN words rule); with no guide for the current year, the latest quarter's revenue growth
    (the UNP rule);
  - guided margin step: none (the operating margin is guided in words, "in the mid 50% range"); the margin signal uses the latest
    quarter's operating-margin change;
  - dividend: the latest declared quarterly rate, each from the first filing that states it ('dividends').
The kind is DURABLE: the 10-Ks tie results to spending and the economy but do not call the business cyclical (the LOW, SHW and JPM
reading). No disruption theme in taxonomy_eras.json is live for a payments network in 2008-2009 so the
builder refuses events until a theme encoding is decided, and it refuses separate guides, listings, splits, company names and 10-Q
restatements until their encodings are decided.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. Visa released after the close, so a print is dated the next trading day (public before its open)
and the weekly date is the trading day after that.

Output goes to staging/retrospective/V until the series is added to the archive (--out archive/retrospective/V).

Usage
  python3 retro/build_v.py --weekly 2009-10-26 2009-12-31
  python3 retro/build_v.py 2009-11-06
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/V/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "V.json")
ENGINE = os.path.join(HERE, "templates", "v_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "V")
SYMBOL = "V"
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"revenue": (-3, 10, 22, 74), "net_to_gross": (-640, -330, -30, 430), "opex_gap": (13, 2, -9, -25),
                     "receivables_gap": (6, -1, -9, -35), "op_margin": (-15780, -7710, 350, 8930)}
RULE_T_KEYS = {"revenue": (1, False), "net_to_gross": (10, False), "opex_gap": (1, True), "receivables_gap": (1, True),
               "op_margin": (10, False)}           # (rounding unit, lower is better)


def fiscal_year(day):
    """The fiscal year a calendar day belongs to: Visa's fiscal year ends on September 30 (2008-10-01 is FY2009's first day)."""
    return int(day[:4]) + (1 if int(day[5:7]) >= 10 else 0)


def rule_t_value(k, r):
    """One annual rule-T value from its raw figures ($ millions, (prior, current))."""
    pct = lambda a, b: (b / a - 1) * 100
    if k == "revenue":
        return round(pct(*r["revenue_m"]) + 0.0, 2)
    if k == "net_to_gross":
        (v0, v1), (a0, a1) = r["incentives_m"], r["revenue_m"]
        return round((a1 / (a1 + v1) - a0 / (a0 + v0)) * 10000 + 0.0, 1)
    if k == "op_margin":
        (o0, o1), (a0, a1) = r["op_income_m"], r["revenue_m"]
        return round((o1 / a1 - o0 / a0) * 10000 + 0.0, 1)
    if k == "opex_gap":
        (x0, x1), (l0, l1), (a0, a1) = r["opex_m"], r["litigation_m"], r["revenue_m"]
        return round(pct(x0 - l0, x1 - l1) - pct(a0, a1) + 0.0, 2)
    (i0, i1), (a0, a1) = r["receivables_m"], r["revenue_m"]
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
    """A print's growth, net-to-gross share, margins and gaps from its raw published figures ($ millions)."""
    pct = lambda a, b: (b / a - 1) * 100
    r1 = lambda x: round(x + 0.0, 1)
    nt, nt0 = r["sales_m"] / r["gross_m"] * 100, r["sales_prior_m"] / r["gross_prior_m"] * 100
    om, om0 = r["op_income_m"] / r["sales_m"] * 100, r["op_income_prior_m"] / r["sales_prior_m"] * 100
    ox, ox0 = r["opex_m"] - r["litigation_m"], r["opex_prior_m"] - r["litigation_prior_m"]
    return dict(sales_pct=r1(pct(r["sales_prior_m"], r["sales_m"])), seq_pct=r1(pct(r["sales_prev_q_m"], r["sales_m"])),
                net_to_gross=round(nt + 0.0, 2), net_to_gross_bp=r1((nt - nt0) * 100), op_margin=round(om + 0.0, 2),
                op_margin_bp=r1((om - om0) * 100), opex_pct=r1(pct(ox0, ox)), opex_gap_pp=r1(pct(ox0, ox) - pct(r["sales_prior_m"], r["sales_m"])),
                receivables_pct=r1(pct(r["receivables_prior_m"], r["receivables_m"])),
                receivables_gap_pp=r1(pct(r["receivables_prior_m"], r["receivables_m"]) - pct(r["sales_prior_m"], r["sales_m"])))


def check_print(p):
    """Re-derive a print's growth, shares, margins and gaps from its raw figures; they must match the fact sheet."""
    for k, v in derived(p["raw"]).items():
        assert p[k] == v, (p["quarter"], k, p[k], v)


def _usd_b(x):
    return f"${x:.3f}B" if x >= 0 else f"$({-x:.3f})B"


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    chart = retro_tool.chart(SYMBOL)
    fx = retro_tool.split_factor(chart, as_of)       # Yahoo's series is on today's shares: undo the later split
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    # no separate guide, listing change, split, change of company name, theme event or 10-Q restatement is encoded: the builder refuses
    # any such fact until its encoding is decided
    for kind in ("guides", "listings", "splits", "company_names", "events"):
        if [x for x in facts.get(kind, []) if x.get("published", x.get("effective", "")) <= as_of]:
            sys.exit(f"{as_of}: the V builder has no encoding for {kind}; decide one first")
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        assert "restated" not in p, (p["quarter"], "a 10-Q restatement needs its encoding decided first")
        check_print(p)
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    # the years the vintage reports, in the history or out of it (FY2008, a distorted first year, is reported and excluded)
    reported = lambda h: ({int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
                          | {int(k) for k in h.get("eps_first_excluded", {})})
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["q"] == 4 else 0)
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    prints = [p for p in public if guide_fy(p) >= first_fy]
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is public yet")
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage
    h = {**h, "extended": ""}
    for p in prints:
        a = p.get("fy_actual")
        if a and a["fy"] not in reported(h):          # the 10-K vintage, once out, wins
            y = str(a["fy"])
            if a["eps_normalized"] is None:           # a loss or distorted year: reported, but out of the EPS history
                h.update(eps_excluded={**h.get("eps_excluded", {}), y: a["excluded_note"]})
            h.update(fy_label=a["fy_label"],
                     eps_normalized={**h["eps_normalized"], **({y: a["eps_normalized"]} if a["eps_normalized"] is not None else {})},
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]},
                     diluted_shares_m={**h["diluted_shares_m"],
                                       **({y: a["diluted_shares_m"]} if a["diluted_shares_m"] is not None else {})},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_op_margin=a["op_margin"], prev_fy_op_margin_note=a["op_margin_note"],
                     prev_fy_pretax_margin=a["pretax_margin"], prev_fy_pretax_margin_note=a["pretax_margin_note"],
                     prev_fy_net_to_gross=a["net_to_gross"], prev_fy_sales_growth=a["sales_growth"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     groups=a["groups"], groups_basis=a["groups_basis"],
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    if not h["eps_normalized"]:
        # FY2008 is excluded and no later year is reported yet: no current-FY P/E can be computed (method r2 has no EPS anchor for a
        # period that is not a full year in the history; retro/README.md, "V")
        sys.exit(f"{as_of}: no fiscal year in the EPS history yet "
                 f"({', '.join('FY' + y for y in sorted(h.get('eps_first_excluded', {})))} excluded); the first V date follows the Q4 FY09 print")
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
    next_q = f"Q{nq % 4 + 1} FY{(latest['fy'] + (1 if nq == 4 else 0)) % 100:02d}"
    g = latest.get("guide") if latest.get("guide", {}).get("fy") == cur_fy else None

    # ── current-FY EPS: the EPS guide is a one-sided bound (no field), so the last full year's EPS stands ──
    eps_now = eps_hist[last_fy]
    eps_label = (f"{fy_e}: no EPS guide in numbers (growth 'of greater than 20%' is a one-sided bound), FY{last_fy % 100:02d}'s "
                 f"${money(eps_now)} stands" if g else f"{fy_e}: no EPS guide in numbers, FY{last_fy % 100:02d}'s ${money(eps_now)} stands")
    eps_label += "".join(f" (FY{y % 100:02d} is excluded: {excluded[y]})" for y in range(last_fy + 1, cur_fy))
    eps_label_short = eps_label if cur_fy == last_fy + 1 else (
        f"{fy_e}: no EPS guide in numbers, FY{last_fy % 100:02d}'s ${money(eps_now)} stands (FY" +
        ", FY".join(f"{y % 100:02d}" for y in range(last_fy + 1, cur_fy)) + " excluded)")
    # ── forward revenue growth: the fiscal year's net revenue growth range (no next-quarter guide), else the latest quarter ──
    if g and g.get("revenue_growth"):
        fwd = list(g["revenue_growth"])
        fwd_label = f"{fy_now} net revenue growth guide"
        fwd_short, fwd_period = f"{fy_now} revenue guide", f"FY{cur_fy}"
        guide_text = (f"{fy_now} ({latest['quarter']} print): '{g['revenue_words']}' — the {fwd[0]}-{fwd[1]}% range stands, its words in "
                      f"the note (the ACN words rule); '{g['eps_words']}' is a one-sided bound and gives no field; '{g['margin_words']}' "
                      "is words and gives no margin step; no next-quarter guide is given, so the fiscal-year range stands in (method r2's "
                      "fallback)")
        fy_rev_label = f"the {fy_now} net revenue growth guide's midpoint"
    else:
        fwd = [latest["sales_pct"]] * 2
        fwd_label = f"{latest['quarter']} revenue growth (no {fy_now} revenue range)"
        fwd_short, fwd_period = f"{latest['quarter'].split()[0]} revenue YoY", latest["quarter"]
        guide_text = f"{fy_now}: no revenue growth range in numbers; the latest quarter's revenue growth stands in (the UNP rule)"
        fy_rev_label = f"the {fwd_label}, YoY, applied to the year"
    cat3 = (f"(3) Payments volume and processed transactions — the drivers of service and data processing revenues, in each release "
            f"({latest['quarter']}: see the revenue line)")
    margin_guided = False                          # no margin guide in numbers: no guided step; the signal uses the latest quarter's change
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
    # the window: up to ten years, from the first year in the history (2008-10-01: the excluded FY2008 leaves, and with it the days
    # from the 2008-03-19 listing)
    window = [d for d in days if d > minus_years(as_of, 10) and (not h["pe_window_start"] or d >= h["pe_window_start"])]
    assert window[0] >= h["listing"], "the window never starts before the listing"
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
    key_tail = ("A spending slowdown shows up in payments volume and service revenues first;\n"
                "  the bear needs it in processed transactions as well.")
    theme_summary = "no disruption theme has dated evidence"
    cat4 = (f"(4) Receivables — {latest['receivables_pct']:+.1f}% against revenue {latest['sales_pct']:+.1f}% in {latest['quarter']} "
            f"({latest['receivables_gap_pp']:+.1f}pp): clients paying more slowly would show here first")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    # only a print public before the open can meet AS_OF's close: Visa released after the previous day's close, so a print dated AS_OF
    # occurs only in a week with no trading day after it
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    company = h["company"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])]
           + [public[i - 1]["source"]] + public[i - 1].get("extra_sources", []) + ([dividend_src] if dividend_src else []))
    sources = [dict(id=x, **facts["sources"][x]) for x in dict.fromkeys(ids)]
    sources.append({"id": "Y0", "published": as_of, "title": "Yahoo Finance daily prices, V and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/V/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E "
                                f"distribution from {window[0]}"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "seq_pct", "net_to_gross", "net_to_gross_bp", "op_margin",
                   "op_margin_bp", "opex_pct", "opex_gap_pp", "receivables_b", "receivables_pct", "receivables_gap_pp", "eps_q",
                   "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    first_excl = "; ".join(f"FY{int(y) % 100:02d} {t}" for y, t in sorted(h.get("eps_first_excluded", {}).items()))
    rev_text = (f"Revenue: {latest['sales_note']}; {latest['receivables_note']}; {latest['eps_note']}; {latest['shares_note']}"
                + (f"; {latest['note']}" if latest.get("note") else ""))
    cash_return = (f"dividend {dividend_note}" + (f"; {latest['cash_return_text']}" if latest.get("cash_return_text") else ""))
    R = repr
    head = f'''#!/usr/bin/env python3
"""
V Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: V)  ·  {h["business_line"]}
Generated by retro/build_v.py from retro/facts/V.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "V"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); revenue, net-to-gross, expense, "
               "receivables and operating-margin signals with Visa's rule-T thresholds")
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
CURRENT_PRICE   = {close:.2f}   # USD, {exchange} close {as_of}, as traded (listed {h["listing"]})
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
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # total operating revenues, USD bn
SHARES_HIST   = {R({y: round(v, 3) for y, v in shares.items()})}   # diluted class A, as converted, millions
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # operating margin, {h["prev_fy_op_margin_note"]}
CHECK_PRETAX_MARGIN = {h["prev_fy_pretax_margin"]}   # pre-tax margin for the EPS check (display), {h["prev_fy_pretax_margin_note"]}
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and the {fy_now} outlook ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_SALES      = {R(prev)}
EPP_TODAY_EPS   = {round(eps_now, 6)}   # {eps_label_short}
EPS_LABEL       = {R(eps_label_short)}
FWD_GUIDE       = {R(tuple(fwd))}   # the fiscal year's net revenue growth range (no next-quarter guide), else the latest quarter
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no margin guide in numbers, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {rev[max(rev)] * (1 + sum(fwd) / 2 / 100):.4f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} total operating revenues {h['prev_fy_sales_growth']:+.1f}%, {h['prev_fy_net_to_gross']:.1f}% of gross revenues kept after client incentives; {latest['quarter'].split()[0]} {latest['net_to_gross']:.2f}% ({latest['net_to_gross_bp']:+.0f}bp YoY)")}
BALANCE_TEXT    = {R(f"Cash and cash equivalents ${latest['cash_b']:.3f}B, {latest['debt_note']} ({latest['quarter']}), {h['fcf_label']} free cash flow {_usd_b(h['fcf_b'])} ({h['fcf_note']}), " + (f"dividend ${dividend:.2f} a year" if dividend else "no dividend"))}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/V)")
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
