#!/usr/bin/env python3
"""
Build SCHW retrospective models from the dated fact sheet (retro/facts/SCHW.json).

The SCHW sibling of build_jpm.py: the same frozen rules (retro method r2), the same weekly dates and the same market statistics, with
a securities broker's signal set and The Charles Schwab Corporation's own rule-T thresholds (retro/templates/schw_engine.py.tmpl).
For each as-of date the builder
  1. selects only the history vintage and prints whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF (Yahoo's SCHW series; its splits, the last on 2000-05-31,
     precede the P/E window, so every price is the close as traded),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Schwab's fiscal year is the calendar year. The method r2 inputs map as follows (retro/README.md, "SCHW"; decided before any SCHW
model was built or scored):
  - revenue: net revenues (interest expense netted, as the statement of income totals them), continuing operations (U.S. Trust,
    sold on 2007-07-01, discontinued), each year from the latest filing that reports it;
  - EPS: diluted EPS from continuing operations, GAAP (no filing on that basis publishes a figure excluding one-offs), each year from
    the latest filing that reports it. FY2002 is a distorted year (the AAPL FY2002 test) whose adjusted figure is in dollars on an
    earlier basis, so the history and the P/E window start with FY2003 ('eps_first_excluded', 'pe_window_start'; the JPM rule);
  - current-FY EPS: no filing of the period gives an EPS guide, so the last full year in the history stands (the rollover rule);
  - forward revenue growth: no filing of the period guides revenue in numbers (the Q4 2008 release's goal of cutting 2009 expenses
    by 7 to 8% of 2008's total is a cost component), so the latest quarter's revenue growth stands in (the UNP rule);
  - guided margin step: none (no margin guide); the margin signal uses the latest quarter's pre-tax margin change;
  - dividend: the latest declared quarterly rate, each from the first filing that states it ('dividends'); the 2007 special
    dividend is not a rate.
(SCHW 2010-2013) The listing moves from Nasdaq to the NYSE on 2010-03-05, the date the FY2009 10-K states ('listings', the PEP
encoding); Q1 2010 is restated twice, by the 8-K of 2010-04-20 and the Q1 2010 10-Q ('restated', the JPM encoding: each from its own
date); the Q1 2010 and Q3 2013 outlooks are bounds and words that feed no field ('outlook_words', text only); from CLOUD's live date the
'why' quotes every live theme's registered scope (the CB 2014-2017 and UNH wording).
(SCHW 2014-2017) No new encoding of a number: the rate increases to $0.07 and $0.08 a quarter are 'dividends' facts; the Q1 2015
expense outlook is words ('outlook_words'); the releases' per-share effects of non-recurring items (from Q3 2015) are not an EPS
without them, so GAAP stands. From ECOMMERCE's live date (2015-01-01) the 'why' names each live theme's subject the 10-Ks were
searched for, and the FY2015 and FY2016 10-Ks' one cloud sentence (an accounting standard) is quoted ('cloud_words', text only).
(SCHW 2018-2021) No new encoding of a number: GAAP every year (the tax reform legislation's $0.03 in FY2017, the severance and acquisition items in
FY2019; from Q2 2020 the releases' adjusted EPS also removes the recurring amortization of acquired intangibles); TD Ameritrade (from
2020-10-06) in the figures as published; the rate increases to $0.10, $0.13, $0.17 and $0.18 a quarter are 'dividends' facts. From the
Q1 2020 release the activity table prints clients' daily average trades (DATs) only, not revenue trades: the trades signal is not
reported (None), scores BASE and prints n/r through schw2_engine.py.tmpl, the None-tolerant copy (the BKR bkr3 and SPGI spgi2
encoding), with DATs in the text only. From EV's live date the 'why' names electric vehicles among the subjects the 10-Ks were searched
for; from CRYPTO's (2020-10-21), whose scope names banks and exchanges, it says no 10-K names cryptocurrency, blockchain, digital assets or
a distributed ledger, so the watch list stays empty (the SPGI 2018-2021 reading).
(SCHW 2022-2026) No new encoding of a number: Item 6 is reserved from the FY2021 10-K, so each vintage takes three years from the MD&A
overview and the statements of income and keeps earlier years from the latest earlier vintage; GAAP every year (the releases' adjusted
EPS also removes the recurring amortization of acquired intangibles); the rate increases to $0.20, $0.22, $0.25, $0.27 and $0.32 a
quarter are 'dividends' facts; DATs only, so every date uses schw2_engine.py.tmpl. Text only: from the FY2021 10-K the cloud words are
Schwab's own reliance on cloud technologies ('cloud_reading'); GENAI and GLP1 join the live themes the 'why' names, and the FY2023-FY2025
10-Ks' artificial intelligence words are quoted ('ai_words'; GENAI's scope names no broker or bank); from the FY2025 10-K, which names
digital assets among industry and competitive trends ('crypto_quote') and Schwab's own planned spot crypto trading ('crypto_own_quote'),
CRYPTO is on the watch list, company-acknowledged with no market read, with a factor pair that nets to zero (the JPM and V encodings).
The kind is DURABLE: the 10-Ks tie results to markets, rates and investor engagement but do not call the business cyclical (the
JPM, LOW and SHW reading). No disruption theme in taxonomy_eras.json is live for a securities broker and bank in 2008-2009, so the
builder refuses events until a theme encoding is decided, and it refuses guides, listings, splits and company names until their
encodings are decided.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. Schwab's earnings 8-Ks of 2007-2009 were accepted during market hours (two after the close, dated
the next trading day); a print on the week's last trading day (Friday 2009-01-16) dates its own week and meets that close, public
before it by its 8-K's acceptance time (the UNP Good Friday 2014 rule, tagged "released during the session"). From Q3 2014 the 8-Ks
are accepted after the close and dated the next trading day; on a Friday (Q2 2015, 2015-07-17) that day is the week's date and the
print, public before its open, meets its close (the AVGO and CRM rule).

Output goes to staging/retrospective/SCHW until the series is added to the archive (--out archive/retrospective/SCHW).

Usage
  python3 retro/build_schw.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_schw.py --weekly 2009-01-05 2009-12-31
  python3 retro/build_schw.py 2008-04-16
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/SCHW/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "SCHW.json")
ENGINE = os.path.join(HERE, "templates", "schw_engine.py.tmpl")
# (SCHW 2018-2021) the None-tolerant copy, used when the latest release does not report daily average revenue trades (from Q1 2020)
ENGINE2 = os.path.join(HERE, "templates", "schw2_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "SCHW")
SYMBOL = "SCHW"
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"revenue": (-56, -22, 12, 41), "client_assets": (-34, -10, 15, 42), "expense_gap": (35, 16, -3, -16),
                     "dart": (-91, -34, 22, 68), "pretax_margin": (-3510, -1640, 230, 1330)}
RULE_T_KEYS = {"revenue": (1, False), "client_assets": (1, False), "expense_gap": (1, True), "dart": (1, False),
               "pretax_margin": (10, False)}           # (rounding unit, lower is better)


def fiscal_year(day):
    """The fiscal year a calendar day belongs to: Schwab's fiscal year is the calendar year."""
    return int(day[:4])


def rule_t_value(k, r):
    """One annual rule-T value from its raw figures ((prior, current): $ millions, $ billions, thousands of trades, % margins)."""
    pct = lambda a, b: (b / a - 1) * 100
    if k == "revenue":
        return round(pct(*r["revenue_m"]) + 0.0, 2)
    if k == "client_assets":
        return round(pct(*r["client_assets_b"]) + 0.0, 2)
    if k == "dart":
        return round(pct(*r["dart_k"]) + 0.0, 2)
    if k == "expense_gap":
        return round(pct(*r["expense_m"]) - pct(*r["revenue_m"]) + 0.0, 2)
    m0, m1 = r["margin_pct"]                   # the pre-tax profit margin as each 10-K prints it
    return round((m1 - m0) * 100 + 0.0, 1)


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
    """A print's growth, margins and gaps from its raw published figures ($ millions; client assets $ billions; trades thousands)."""
    pct = lambda a, b: (b / a - 1) * 100
    r1 = lambda x: round(x + 0.0, 1)
    pm, pm0 = r["pretax_m"] / r["revenue_m"] * 100, r["pretax_prior_m"] / r["revenue_prior_m"] * 100
    return dict(sales_pct=r1(pct(r["revenue_prior_m"], r["revenue_m"])), seq_pct=r1(pct(r["revenue_prev_q_m"], r["revenue_m"])),
                pretax_margin=round(pm + 0.0, 2), pretax_margin_bp=r1((pm - pm0) * 100),
                expense_pct=r1(pct(r["expense_prior_m"], r["expense_m"])),
                expense_gap_pp=r1(pct(r["expense_prior_m"], r["expense_m"]) - pct(r["revenue_prior_m"], r["revenue_m"])),
                ca_pct=r1(pct(r["client_assets_prior_b"], r["client_assets_b"])),
                # (SCHW 2018-2021) from the Q1 2020 release revenue trades are not reported: None, scored BASE (n/r)
                dart_pct=None if r["dart_k"] is None else r1(pct(r["dart_prior_k"], r["dart_k"])))


def check_print(p, as_of):
    """Re-derive a print's (and its restatements', once public) margins, growth and gaps from its raw figures; they must match the
    fact sheet. Every 10-Q of 2007-2009 reports its quarter's signal rows as the release does; Q1 2010 is restated twice (the 8-K of
    2010-04-20 and the Q1 2010 10-Q, SCHW 2010-2013)."""
    for x in [p] + [r for r in p.get("restated", []) if r["published"] <= as_of]:
        for k, v in derived(x["raw"]).items():
            assert x[k] == v, (p["quarter"], k, x[k], v)


def as_restated(p, as_of):
    """A print with its restatements applied, in order, once each is public (a quarter from the latest filing that reports it: the
    JPM encoding)."""
    q = p
    for rs in p.get("restated", []):
        if rs["published"] <= as_of:
            q = {**q, **{k: v for k, v in rs.items() if k not in ("published", "source", "rows")}}
            q["extra_sources"] = list(q.get("extra_sources", [])) + [rs["source"]]
    return q


def build(as_of, facts, raw, spx, engine, out):
    with open(ENGINE2, encoding="utf-8") as fh:        # (SCHW 2018-2021) the None-tolerant copy, read beside the common signature
        engine2 = fh.read()
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    chart = retro_tool.chart(SYMBOL)
    assert retro_tool.split_factor(chart, as_of) == 1.0, "a split after AS_OF needs an encoding ('splits')"
    px = raw
    # no filing guides revenue, EPS or a margin in a range or a level, and none states a split or a change of company name: the builder
    # refuses any such fact, and any event, until its encoding is decided. The listing moves from Nasdaq to the NYSE on 2010-03-05, as
    # the FY2009 10-K states ('listings', the PEP encoding: effective on its stated date once the filing is public)
    for kind in ("guides", "splits", "company_names", "events"):
        if [x for x in facts.get(kind, []) if x.get("published", x.get("effective", "")) <= as_of]:
            sys.exit(f"{as_of}: the SCHW builder has no encoding for {kind}; decide one first")
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
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage; the 10-K in force keeps
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
                     prev_fy_sales_growth=a["sales_growth"], prev_fy_client_assets_b=a["client_assets_b"],
                     prev_fy_client_assets_growth=a["client_assets_growth"], prev_fy_nna_b=None,
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
            assert not a.get("restates") and not a.get("restates_revenue"), (p["quarter"], "no encoding for a restated year")
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

    # (SCHW 2010-2013) an outlook for the current year that gives bounds and words only ('outlook_words' on the print: Q1 2010, Q3
    # 2013): no field, text only (the UNH and SPGI bound and words rules)
    outlook = [p for p in prints if p.get("outlook_fy") == cur_fy]
    outlook = outlook[-1] if outlook else None
    # ── current-FY EPS: no EPS guide in any filing of the period, so the last full year's EPS stands ──
    eps_now = eps_hist[last_fy]
    no_eps = (f"no EPS range or level ('{outlook['eps_words']}' is words)" if outlook and outlook.get("eps_words") else
              "no EPS guide in numbers")
    eps_label = f"{fy_e}: {no_eps}, FY{last_fy % 100:02d}'s ${money(eps_now)} stands" + "".join(
        f" (FY{y % 100:02d} is excluded: {excluded[y]})" for y in range(last_fy + 1, cur_fy))
    eps_label_short = (f"{fy_e}: {no_eps}, FY{last_fy % 100:02d}'s ${money(eps_now)} stands (FY" +
                       ", FY".join(f"{y % 100:02d}" for y in range(last_fy + 1, cur_fy)) + " excluded)") if cur_fy > last_fy + 1 else eps_label
    # ── forward revenue growth: no revenue guide in any filing, so the latest quarter's revenue growth (the UNP rule) ──
    fwd = [latest["sales_pct"]] * 2
    fwd_label = f"{latest['quarter']} revenue growth (no {next_q} guide)"
    fwd_short, fwd_period = f"{latest['quarter'].split()[0]} revenue YoY", latest["quarter"]
    guide_text = (f"{next_q}: no revenue, EPS or margin guide in numbers in any filing; the latest quarter's revenue growth stands in "
                  "(the UNP rule)" + ("; the expense goal (2009 cuts of 7 to 8% of 2008's total spending) is a cost component, which "
                                      "method r2 has no input for" if latest["published"] >= "2009-01-16" and cur_fy == 2009 else ""))
    cat3 = (f"(3) A {next_q} revenue guide — none: Schwab gives no revenue, EPS or margin outlook in numbers in any filing; "
            "the monthly activity reports in each release track client assets, net new assets and trades")
    if outlook:
        guide_text = (f"{next_q}: no revenue, EPS or margin guide in a range or a level in any filing; the latest quarter's revenue growth "
                      f"stands in (the UNP rule); the {outlook['quarter']} release's outlook ('{outlook['outlook_words']}') feeds no "
                      f"field: {outlook['outlook_reading']}")
        cat3 = (f"(3) A {next_q} revenue guide — none in a range or a level: the {outlook['quarter']} release's outlook is bounds and "
                "words; the monthly activity reports in each release track client assets, net new assets and trades")
    margin_guided = False                          # no margin guide: no guided step; the signal uses the latest quarter's change
    fy_margin_base = h["prev_fy_op_margin"]

    # ── dividend: the latest declared quarterly rate, each from the first filing that states it ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts.get("dividends", []) if d["published"] <= as_of]
    _, dividend, dividend_note, dividend_src = max(divs, key=lambda x: x[0])
    exchange = h["exchange"]
    moved = [x for x in facts.get("listings", []) if x["published"] <= as_of and x["effective"] <= as_of]
    if moved:
        exchange = max(moved, key=lambda x: x["effective"])["exchange"]

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
    key_tail = ("Lower markets and rates show up in client assets and asset-based fees first;\n"
                "  the bear needs them in net revenue as well.")
    theme_summary = "no disruption theme has dated evidence"
    cat4 = (f"(4) Trading activity — {latest['dart_k']:.1f}K daily average revenue trades in {latest['quarter']} "
            f"({latest['dart_pct']:+.1f}% YoY): the driver of trading revenue") if latest["dart_k"] is not None else (
            f"(4) Trading activity — revenue trades not reported in {latest['quarter']}: from the Q1 2020 release the activity table "
            f"prints clients' daily average trades (DATs) only ({latest['dats_k']:,.1f}K vs {latest['dats_prior_k']:,.1f}K a year "
            "earlier, display only), so the signal scores BASE (n/r)")
    why = h["why"]
    # from CLOUD's live date (2012-10-30) every live theme is quoted with its registered scope (the CB 2014-2017 and UNH wording)
    live = sorted(((t["live_from"], k, t["scope"]) for k, t in retro_tool.load_taxonomy()["themes"].items() if t["live_from"] <= as_of))
    if [k for _, k, _ in live] != ["OFFSHORE"]:
        scopes = ", ".join(f"{k} {'is scoped to' if i == 0 else 'to'} '{sc}'" for i, (_, k, sc) in enumerate(live))
        head = why.split("; no theme in taxonomy_eras.json is live")[0]
        assert head != why, (as_of, "the vintage's why lost its theme clause")
        # (SCHW 2014-2017) from ECOMMERCE's live date the clause names each live theme's subject the 10-Ks were searched for, and
        # from the FY2015 10-K, which names cloud computing only in an accounting standard ('cloud_words'), it quotes those words
        # (the UNH 'cloud_words' and LMT FY2016 readings); with OFFSHORE and CLOUD alone the clause is as before
        words = {"OFFSHORE": "offshore delivery", "CLOUD": "cloud", "ECOMMERCE": "e-commerce", "STREAMING": "streaming",
                 "ENERGY_TRANSITION": "decarbonisation", "EV": "electric vehicles", "GENAI": "artificial intelligence",
                 "GLP1": "GLP-1 drugs"}
        live_k = [k for _, k, _ in live]
        if live_k == ["OFFSHORE", "CLOUD"]:
            none10k = "no 10-K names cloud or offshore delivery"
        else:
            assert set(live_k) <= set(words) | {"CRYPTO"}, (as_of, "a live theme the SCHW 10-Ks were not searched for", live_k)
            named = [words[k] for k in live_k if k != "CRYPTO" and not (k == "CLOUD" and h.get("cloud_words"))
                     and not (k == "GENAI" and h.get("ai_words"))]
            none10k = "no 10-K names " + ", ".join(named[:-1]) + " or " + named[-1]
            tenk = h['fy_label'].replace('FY', 'FY20')
            if h.get("cloud_words"):
                # (SCHW 2022-2026) from the FY2021 10-K the cloud words are Schwab's own reliance on cloud technologies
                # ('cloud_reading'); before it, an accounting standard
                none10k += (f", and the {tenk} 10-K {h.get('cloud_reading', 'names cloud computing only in an accounting standard')} "
                            f"('{h['cloud_words']}'), not as a way its own business is delivered or displaced")
            if h.get("ai_words"):
                # (SCHW 2022-2026) GENAI (live 2022-11-30) is scoped to software, IT services, professional information, search,
                # education and mobility, none of them brokerage or banking; the FY2023-FY2025 10-Ks name artificial intelligence as a
                # tool of fraud and cyber attack and, in FY2025, among industry and competitive trends ('ai_words', text only: the UNH
                # and JPM 2022-2026 readings)
                none10k += (f", and the {tenk} 10-K names artificial intelligence only as " +
                            ("a tool of external fraud and cyber attack and among its industry and competitive trends" if len(h["ai_words"]) > 1
                             else "a tool of external fraud and cyber attack") + " (" +
                            " ".join(f"'{w}'" for w in h["ai_words"]) + "), not as a substitute for its own services")
        cr_q = h.get("crypto_quote") if "CRYPTO" in live_k else None
        if cr_q:
            # (SCHW 2022-2026) the FY2025 10-K names digital assets among industry and competitive trends ('crypto_quote') and Schwab's
            # own planned spot crypto trading ('crypto_own_quote'). CRYPTO's scope names banks and exchanges, so the current 10-K's
            # words put it on the watch list, company-acknowledged, with no market read (the JPM encoding), and the offering of its own
            # adds a factor pair that nets to zero (the V encoding); the theme signal stays at 2/4, so only text changes
            cr = retro_tool.load_taxonomy()["themes"]["CRYPTO"]
            val_word = "a premium" if pe_now_pctl >= 70 else "a discount to its own history" if pe_now_pctl <= 30 else "near its own median"
            own = h.get("crypto_own_quote")
            stage = "crypto"
            watch = [{"theme": "CRYPTO", "status": "live, company-acknowledged; no market read",
                      "reason": (f"Live: Schwab's own {tenk} 10-K lists '{cr_q}'" + (f" It names a crypto offering of its own: '{own}'"
                                                                                      if own else "") +
                                 f" The stock trades at {close / eps_now:.1f}x {fy_e_s} — {val_word}. Re-file as DISRUPTION_EXPOSED "
                                 "(CRYPTO) only if dated evidence shows the market pricing crypto disintermediation of Schwab's "
                                 "brokerage and banking specifically.")}]
            if own:
                factors = [(f"Crypto: Schwab's own planned spot crypto trading ({tenk} 10-K)", 0.2, 0.10),
                           (f"Crypto competition ({tenk} 10-K): digital assets among industry and competitive trends", -0.2, 0.10)]
            sig_name = "Crypto: disintermediation of brokerage and banking"
            trigger = "Investors move to crypto platforms that need no broker or bank faster than Schwab offers the assets itself"
            theme_summary = "crypto is live and company-acknowledged; no dated evidence ties the multiple to it"
            why = (head + "; of the live themes in taxonomy_eras.json, " + scopes + ": CRYPTO names banks and exchanges, and the "
                   f"{tenk} 10-K names digital assets among Schwab's industry and competitive trends and a crypto trading offer of its "
                   f"own, so CRYPTO is on the watch list; of the rest none names brokerage or banking, and {none10k}; CRYPTO is live "
                   f"(from {cr['live_from']}): these words put it on the watch list, company-acknowledged, with no dated evidence that "
                   "the market prices it for Schwab")
        elif "CRYPTO" in live_k:
            # (SCHW 2018-2021) CRYPTO's registered scope names banks and exchanges, but no 10-K of these years names cryptocurrency,
            # blockchain, digital assets or a distributed ledger, so nothing dated ties the theme to Schwab: no watch item (the SPGI
            # 2018-2021 reading; JPM's and V's watch items rest on their own 10-Ks' crypto words). Text only either way: the JPM
            # encoding adds no factor pair, so the theme signal stays at 2/4
            why = (head + "; no disruption theme in taxonomy_eras.json has dated evidence for a securities broker and bank on this date "
                   f"(of the live themes, {scopes}: CRYPTO alone names banks and exchanges, and no 10-K names cryptocurrency, "
                   f"blockchain, digital assets or a distributed ledger, so nothing dated ties it to Schwab; of the rest none names "
                   f"brokerage or banking, and {none10k}), so the watch list is empty and these words stay here (the PEP obesity rule)")
        else:
            why = (head + "; no disruption theme in taxonomy_eras.json is live for a securities broker and bank on this date (of the live "
                   f"themes, {scopes}: none names brokerage or banking, and {none10k}), so the watch list is "
                   "empty and these words stay here (the PEP obesity rule)")
    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    # a print dated AS_OF occurs only in a week with no trading day after it; it meets AS_OF's close only if it was public before that
    # close: an 8-K accepted before the open or during market hours (the UNP Good Friday 2014 rule)
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        rt = same_day[-1].get("release_time", "")
        # (SCHW 2014-2017) an 8-K accepted after the previous trading day's close is dated AS_OF and public before its open: on a
        # Friday (Q2 2015, 2015-07-17) that day is the week's date and the print meets its close (the AVGO and CRM rule)
        early = "before the open" in rt or "(after the close), so dated the next trading day" in rt
        assert early or "during market hours" in rt, (as_of, same_day[-1]["quarter"], "not public before the close")
        tag = (f"(day of the {same_day[-1]['quarter']} print, public before the open)" if early else
               f"(day of the {same_day[-1]['quarter']} print, released during the session)")

    company = h["company"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])]
           + [public[i - 1]["source"]] + ([dividend_src] if dividend_src else [])
           + ([max(moved, key=lambda x: x["effective"])["source"]] if moved else []))
    sources = [dict(id=x, **facts["sources"][x]) for x in dict.fromkeys(ids)]
    sources.append({"id": "Y0", "published": as_of, "title": "Yahoo Finance daily prices, SCHW and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/SCHW/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E "
                                f"distribution from {window[0]}"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "seq_pct", "pretax_margin", "pretax_margin_bp", "expense_pct",
                   "expense_gap_pp", "ca_b", "ca_pct", "dart_k", "dart_pct", "nna_b", "eps_q", "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    first_excl = "; ".join(f"FY{int(y) % 100:02d} {t}" for y, t in sorted(h.get("eps_first_excluded", {}).items()))
    rev_text = (f"Revenue: {latest['sales_note']}; {latest['client_note']}; {latest['eps_note']}; {latest['shares_note']}"
                + (f"; {latest['note']}" if latest.get("note") else ""))
    cash_return = f"dividend {dividend_note}"
    R = repr
    head = f'''#!/usr/bin/env python3
"""
SCHW Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: SCHW)  ·  {h["business_line"]}
Generated by retro/build_schw.py from retro/facts/SCHW.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "SCHW"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); net revenue, client assets, expense, "
               "trading activity and pre-tax margin signals with Schwab's rule-T thresholds")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts above.
PIT_PROFILE = {{
    "kind": {R(h["kind"])},
    "risk": 2,
    "why": {R(why)},
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
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}{"; " + h["acquisition_note"] if h.get("acquisition_note") else ""}
EPS_FIRST_EXCLUDED = {R(first_excl)}
EPS_EXCLUDED  = {R({y: t for y, t in sorted(excluded.items())})}
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # net revenues, continuing operations, USD bn
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
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} net revenues {h['prev_fy_sales_growth']:+.1f}%, client assets ${h['prev_fy_client_assets_b']:,.1f}B ({h['prev_fy_client_assets_growth']:+.1f}%); {latest['quarter'].split()[0]} net new client assets ${latest['nna_b']:.1f}B")}
BALANCE_TEXT    = {R(f"Client assets ${latest['ca_b']:,.1f}B ({latest['ca_pct']:+.1f}% YoY) at the end of {latest['quarter']}, pre-tax margin {latest['pretax_margin']:.1f}%, dividend ${dividend:.2f} a year")}
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
        fh.write(head + (engine2 if latest["dart_k"] is None else engine))
    return tag, latest["quarter"], stage


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dates", nargs="*")
    ap.add_argument("--weekly", nargs=2, metavar=("START", "END"))
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/SCHW)")
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
