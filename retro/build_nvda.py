#!/usr/bin/env python3
"""
Build NVDA retrospective models from the dated fact sheet (retro/facts/NVDA.json).

The NVDA sibling of build_avgo.py: the same frozen rules (retro method r2), the same weekly dates and the same market statistics,
with the AVGO semiconductor signals and NVIDIA's own rule-T thresholds (retro/templates/nvda_engine.py.tmpl). For each as-of date
the builder
  1. selects only the history vintage, prints and guides whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, on the AS_OF share basis (Yahoo's split-adjusted series
     times the splits after AS_OF), so the price and the per-share facts share one basis,
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

NVIDIA listed on 1999-01-22 (Nasdaq: NVDA), inside the ten-year window of every 2008-2009 date, so the window runs from the listing
(method r2, "A listing inside the window"). Its fiscal year ends on the last Sunday in January (FY2008: 2008-01-27). It has no fiscal
1998: it reported calendar years to 1997 (a loss), then the one-month transition period of January 1998, so the history starts with
FY1999. The method r2 inputs map as follows (retro/README.md, "NVDA"; decided before any NVDA model was built or scored):
  - EPS: GAAP diluted EPS, each year from the latest filing that reports it; the company's non-GAAP EPS excludes stock-based
    compensation, which recurs, so GAAP stands (the NKE FY2007 and AVGO rule). FY2009 lost $(0.05) and is excluded as the latest
    year (the AVGO FY2009 and XOM FY2020 rule): its own days leave the P/E window and FY2008 stays the last full year;
  - current-FY EPS: no filing of the period gives an EPS guide, so the last full year in the history stands (the rollover rule);
  - forward revenue growth: the next-quarter revenue guide (from the Q2 FY10 release), read as a dollar level on the quarter just
    reported and then against the year-ago quarter (the AVGO and AAPL rule); with none in scope, the latest quarter's revenue growth
    (the UNP rule). The 10-Qs' and 10-K's revenue words ('grow slightly', 'decline slightly') are display only;
  - guided margin step: none (no fiscal-year margin guide); the margin signal uses the latest quarter's operating-margin change. The
    Q4 FY10 outlook's GAAP gross margin and operating expenses are display only (the AVGO rule).
Splits: the two-for-one effective 2006-04-07 and the three-for-two effective 2007-09-11 restate every per-share fact on a basis
before them. A figure's basis is its filing's date, except where 'share_basis' says otherwise: the FY2006 10-K/A of 2006-11-29
restates the Original Filing without reflecting later events, so its FY2002 EPS and shares are on the basis before the 2006 split.
The kind is CYCLICAL on the 10-Ks' own "Our business is cyclical in nature" (the BKR reading); no disruption theme in
taxonomy_eras.json is live for a GPU maker in 2008-2009, so the builder refuses events until a theme encoding is decided.

From 2010 on (decided on 2026-11-13 before any 2010-2013 date was built or scored; retro/README.md, "NVDA 2010-2013"):
  - FY2010 lost $(0.12) and is excluded like FY2009, so both leave the EPS history and the P/E window and FY2008 stays the last full
    year until FY2011 enters with the Q4 FY11 print;
  - from the Q4 FY12 release the next quarter's revenue is guided as a dollar level, a range or a figure plus or minus a percent
    ('level_stated', 'level_center_m', 'level_pm_pct'), read against the year-ago quarter directly (the AAPL and AVGO level rule);
    "flat" is 0 (the RCL and LOW rule);
  - the quarterly dividend from the 8-K of 2012-11-08 ($0.075) and the Q3 FY14 release ($0.085), each from the first filing that
    states it.

From 2014 on (decided on 2026-11-13 before any 2014-2017 date was built or scored; retro/README.md, "NVDA 2014-2017"): the method
and the encodings above are unchanged; the one builder change is the text for a print public before its outlook ('outlook_later':
the Q1 FY15 results, released before the open of 2014-05-06 after a preliminary draft was emailed internally, with the Q2 FY15
outlook only in the release of May 8), whose dates take the latest quarter's revenue growth, as for any print with no guide in scope.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. NVIDIA released after the close, so a print is dated the next trading day; on a Friday that is
the week's last trading day, and the print meets its close (public before the open; the AVGO rule).

Output goes to staging/retrospective/NVDA until the series is added to the archive (--out archive/retrospective/NVDA).

Usage
  python3 retro/build_nvda.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_nvda.py --weekly 2009-01-05 2009-12-31
  python3 retro/build_nvda.py --weekly 2010-01-04 2013-12-31
  python3 retro/build_nvda.py --weekly 2014-01-06 2017-12-31
  python3 retro/build_nvda.py 2008-02-15
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/NVDA/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "NVDA.json")
ENGINE = os.path.join(HERE, "templates", "nvda_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "NVDA")
# the guide fields this builder has an encoding for; any other field needs its encoding decided first (a next-quarter revenue guide
# stated as sequential growth, or from the Q4 FY12 release as a dollar level, a range or a figure plus or minus a percent
# ('level_stated', 'level_center_m', 'level_pm_pct'), each read against the year-ago quarter; or words, display only)
GUIDE_KEYS = {"fy", "published", "source", "doc", "quarter", "seq_pct", "base_quarter", "base_sales_m", "level_m", "prior_label",
              "prior_sales_m", "prior_source", "yoy_pct", "quote", "display", "words", "level_stated", "level_center_m", "level_pm_pct"}
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"revenue": (-43, -5, 34, 137), "gross_margin": (-1760, -770, 210, 720), "opex_gap": (47, 22, -2, -47),
                     "inventory_gap": (115, 66, 17, -105), "op_margin": (-2010, -950, 120, 1280)}
RULE_T_KEYS = {"revenue": (1, False), "gross_margin": (10, False), "opex_gap": (1, True), "inventory_gap": (1, True),
               "op_margin": (10, False)}           # (rounding unit, lower is better)


def fiscal_year_end(n):
    """NVIDIA's fiscal year n ends on the last Sunday in January of calendar year n (the FY2009 10-K: 'a 52 or 53-week year, ending
    on the last Sunday in January')."""
    d = dt.date(n, 1, 31)
    return d - dt.timedelta((d.weekday() - 6) % 7)


def fiscal_year(day):
    """The fiscal year a calendar day belongs to."""
    d = dt.date.fromisoformat(day)
    return d.year if d <= fiscal_year_end(d.year) else d.year + 1


def rule_t_value(k, r):
    """One annual rule-T value from its raw figures ($ thousands, (prior, current))."""
    pct = lambda a, b: (b / a - 1) * 100
    if k == "revenue":
        return round(pct(*r["revenue_k"]) + 0.0, 2)
    if k == "gross_margin":
        (g0, g1), (a0, a1) = r["gross_profit_k"], r["revenue_k"]
        return round((g1 / a1 - g0 / a0) * 10000 + 0.0, 1)
    if k == "op_margin":
        (o0, o1), (a0, a1) = r["op_income_k"], r["revenue_k"]
        return round((o1 / a1 - o0 / a0) * 10000 + 0.0, 1)
    if k == "opex_gap":
        (d0, d1), (s0, s1), (a0, a1) = r["rd_k"], r["sga_k"], r["revenue_k"]
        return round(pct(d0 + s0, d1 + s1) - pct(a0, a1) + 0.0, 2)
    (i0, i1), (a0, a1) = r["inventory_k"], r["revenue_k"]
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


def check_print(p):
    """Re-derive a print's margins, growth and gaps from its raw published figures ($ thousands; they must match the fact sheet)."""
    r = p["raw"]
    pct = lambda a, b: (b / a - 1) * 100
    r1 = lambda x: round(x + 0.0, 1)
    gm, gm0 = r["gross_profit_k"] / r["sales_k"] * 100, r["gross_profit_prior_k"] / r["sales_prior_k"] * 100
    om, om0 = r["op_income_k"] / r["sales_k"] * 100, r["op_income_prior_k"] / r["sales_prior_k"] * 100
    ox, ox0 = r["rd_k"] + r["sga_k"], r["rd_prior_k"] + r["sga_prior_k"]
    want = dict(sales_pct=r1(pct(r["sales_prior_k"], r["sales_k"])), seq_pct=r1(pct(r["sales_prev_q_k"], r["sales_k"])),
                gross_margin=round(gm + 0.0, 2), gross_margin_bp=r1((gm - gm0) * 100), op_margin=round(om + 0.0, 2),
                op_margin_bp=r1((om - om0) * 100), opex_pct=r1(pct(ox0, ox)), opex_gap_pp=r1(pct(ox0, ox) - pct(r["sales_prior_k"], r["sales_k"])),
                inventory_pct=r1(pct(r["inventory_prior_k"], r["inventory_k"])),
                inventory_gap_pp=r1(pct(r["inventory_prior_k"], r["inventory_k"]) - pct(r["sales_prior_k"], r["sales_k"])))
    for k, v in want.items():
        assert p[k] == v, (p["quarter"], k, p[k], v)


def check_guide(g):
    if "words" in g:              # words only: no figure, display only
        assert not set(g) & {"seq_pct", "level_m", "yoy_pct"}, (g["doc"], "a words-only guide carries no number")
        return
    if g.get("level_stated"):     # a dollar level: a range as stated, or a figure plus or minus a percent
        c, pm = g.get("level_center_m"), g.get("level_pm_pct")
        lv = [round(c * (1 - pm / 100), 2), round(c * (1 + pm / 100), 2)] if c is not None else g["level_m"]
    else:
        lv = [round(g["base_sales_m"] * (1 + s / 100), 2) for s in g["seq_pct"]]
    assert lv == g["level_m"] and lv[0] <= lv[1], (g["doc"], lv)
    assert [round((x / g["prior_sales_m"] - 1) * 100 + 0.0, 1) for x in lv] == g["yoy_pct"], (g["doc"], "yoy")


def on_basis(facts, as_of):
    """The fact sheet with every per-share fact on the AS_OF share basis: a split effective on or before AS_OF divides per-share values
    whose share basis predates it and multiplies share counts by it. A figure's basis is its filing's date, a vintage year's the date
    of the filing it comes from ('eps_published'), or its 'share_basis' where that predates the filing (the FY2006 10-K/A's FY2002, on
    the Original Filing's basis). The UNP helper with that one field added."""
    f = copy.deepcopy(facts)
    splits = [s for s in f.get("splits", []) if s["effective"] <= as_of]
    k = lambda basis: math.prod(s["ratio"] for s in splits if basis < s["effective"])
    for v in f["history_vintages"]:
        basis = lambda y: v.get("share_basis", {}).get(y, v.get("eps_published", {}).get(y, v["published"]))
        v["eps_normalized"] = {y: e / k(basis(y)) for y, e in v["eps_normalized"].items()}
        v["diluted_shares_m"] = {y: n * k(basis(y)) for y, n in v["diluted_shares_m"].items()}
        notes = []
        for s in splits:                     # each split names the years it restates (on a basis before its effective date)
            restated = [y for y in sorted(v["eps_normalized"]) if basis(y) < s["effective"]]
            if restated:
                notes.append(f"per share ÷{s['ratio']:g} for the {s['label']} split effective {s['effective']} ({s['source']}) on "
                             f"FY{restated[0][2:]}-FY{restated[-1][2:]}")
        v["split_note"] = "; ".join(notes)
    for p in f["prints"]:
        r = k(p["published"])
        p["eps_q"], p["eps_q_prior"], p["diluted_shares_m"] = p["eps_q"] / r, p["eps_q_prior"] / r, p["diluted_shares_m"] * r
        if p.get("fy_actual") and p["fy_actual"]["eps_normalized"] is not None:
            p["fy_actual"]["eps_normalized"] /= r
        if p.get("fy_actual"):
            p["fy_actual"]["diluted_shares_m"] *= r
    # a dividend rate is a per-share figure too (from NVDA 2018-2021: the four-for-one split of 2021-07-20 restates the rates before it)
    for d in f.get("dividends", []):
        d["quarterly"] /= k(d["published"])
    for v in f["history_vintages"]:
        if v.get("dividend_annual") is not None:
            v["dividend_annual"] /= k(v["published"])
    return f, [s["source"] for s in splits]


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    listing = facts["listing"]["first_trading_day"]
    assert min(raw) == listing, ("the price data must start on the listing day", min(raw), listing)
    # every price of the window on the AS_OF share basis: Yahoo's split-adjusted series times the splits after AS_OF
    chart = retro_tool.chart("NVDA")
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat()
                    for v in chart.get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo_splits for s in facts.get("splits", [])), "a split's effective date must match the price data"
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    for g in [g for g in facts["guides"] if g["published"] <= as_of]:      # a guide public on AS_OF may carry only encoded fields
        assert set(g) <= GUIDE_KEYS, (g["doc"], "a guide field with no encoding yet; decide one first")
        check_guide(g)
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        check_print(p)
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    facts, split_ids = on_basis(facts, as_of)
    live_splits = [s for s in facts.get("splits", []) if s["effective"] <= as_of]
    split_txt = lambda pub, fmt: "".join(fmt.format(l=s["label"], e=s["effective"]) for s in live_splits if pub < s["effective"])
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    # prints published by AS_OF that report a fiscal year after the history (a Q4 print reports the year just ended, so it stays in
    # scope after the 10-K that follows it); a year excluded from the EPS history ('eps_excluded': FY2009, a loss) is still reported
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    prints = [p for p in facts["prints"] if p["published"] <= as_of and guide_fy(p) >= first_fy]
    # no disruption theme in taxonomy_eras.json is live for a GPU maker in 2008-2009 (CLOUD from 2012-10-30 is scoped to on-premise IT,
    # OFFSHORE to IT services, GENAI from 2022-11-30): the builder refuses events until a theme encoding is decided
    events = [e for e in facts["events"] if e["published"] <= as_of]
    if events:
        sys.exit(f"{as_of}: the NVDA builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
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
                     diluted_shares_m={**h["diluted_shares_m"], y: a["diluted_shares_m"]},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_op_margin=a["op_margin"], prev_fy_op_margin_note=a["op_margin_note"],
                     prev_fy_pretax_margin=a["pretax_margin"], prev_fy_pretax_margin_note=a["pretax_margin_note"],
                     prev_fy_gross_margin=a["gross_margin"], prev_fy_sales_growth=a["sales_growth"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    latest = prints[-1]
    # the previous quarter is the print published just before the latest one (in or out of the history's scope)
    public = [p for p in facts["prints"] if p["published"] <= as_of]
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

    # ── current-FY EPS: no EPS guide in numbers in any filing of the period, so the last full year's EPS stands ──
    eps_now = eps_hist[last_fy]
    eps_label = f"{fy_e}: no EPS guide in numbers, FY{last_fy % 100:02d}'s ${money(eps_now)} stands" + "".join(
        f" (FY{y % 100:02d} is excluded: {excluded[y]})" for y in range(last_fy + 1, cur_fy))
    # ── forward revenue growth: the latest numeric guide for the quarter after the latest print, as growth on the year-ago quarter;
    # with none in scope, the latest quarter's revenue growth (the UNP rule); revenue words are display only ──
    live = [g for g in facts["guides"] if g["published"] <= as_of and g.get("quarter") == next_q]
    qg = [g for g in live if "seq_pct" in g or g.get("level_stated")]
    words = [g for g in live if "words" in g]
    w = words[-1] if words else None
    if qg:
        g = qg[-1]
        fwd = list(g["yoy_pct"])
        lvl = f"${g['level_m'][0]:,.1f}M" if g["level_m"][0] == g["level_m"][1] else f"${g['level_m'][0]:,.1f}M-${g['level_m'][1]:,.1f}M"
        sg = lambda x: f"{x:+g}%" if x else "0%"
        seq = (None if g.get("level_stated") else
               sg(g["seq_pct"][0]) if g["seq_pct"][0] == g["seq_pct"][1] else f"{sg(g['seq_pct'][0])} to {sg(g['seq_pct'][1])}")
        later_words = (f"; restated in words in the {w['doc']}: '{w['words']}' (the last numeric range stands, the ACN rule)"
                       if w and w["published"] > g["published"] else "")
        fwd_label = f"{next_q} revenue guide ({g['doc']})"
        fwd_short, fwd_period = f"{next_q} guide YoY", next_q
        if g.get("level_stated"):     # a dollar level, read against the year-ago quarter directly (the AAPL and AVGO rule)
            stated = (f"${g['level_center_m']:,.1f}M ±{g['level_pm_pct']:g}%, i.e. {lvl}" if g.get("level_center_m") is not None else lvl)
            guide_text = (f"{next_q} outlook ({g['doc']}): revenue {stated} ('{g['quote']}') against {g['prior_label']}'s "
                          f"${g['prior_sales_m']:,.1f}M: {_range(fwd)} YoY; display only: {g['display']}{later_words}; "
                          "no fiscal-year revenue, EPS or margin guide")
            cat3 = f"(3) The {next_q} guide — revenue {stated} ({_range(fwd)} YoY): NVIDIA guides one quarter at a time, in revenue"
        else:
            guide_text = (f"{next_q} outlook ({g['doc']}): revenue {seq} on {g['base_quarter']}'s ${g['base_sales_m']:,.1f}M ('{g['quote']}'), "
                          f"i.e. {lvl} against {g['prior_label']}'s ${g['prior_sales_m']:,.1f}M: {_range(fwd)} YoY; display only: {g['display']}"
                          f"{later_words}; no fiscal-year revenue, EPS or margin guide")
            cat3 = f"(3) The {next_q} guide — {seq} on {g['base_quarter']} ({_range(fwd)} YoY): NVIDIA guides one quarter at a time, in revenue"
        guide_ids = [g["source"], g["prior_source"]] + ([w["source"]] if later_words else [])
    elif latest.get("outlook_later"):   # results public before their outlook (Q1 FY15: released early on 2014-05-06, outlook on May 8)
        fwd = [latest["sales_pct"]] * 2
        fwd_label = f"{latest['quarter']} revenue growth (no {next_q} guide in numbers yet)"
        fwd_short, fwd_period = f"{latest['quarter'].split()[0]} revenue YoY", latest["quarter"]
        guide_text = (f"{next_q}: no revenue guide in numbers yet: the {latest['quarter']} results came out ahead of their outlook "
                      f"('{latest['outlook_later']}'); the latest quarter's revenue growth stands in (the UNP rule); no fiscal-year "
                      "revenue, EPS or margin guide")
        cat3 = f"(3) The {next_q} guide — not published yet: '{latest['outlook_later']}'"
        guide_ids = []
    else:
        fwd = [latest["sales_pct"]] * 2
        fwd_label = f"{latest['quarter']} revenue growth (no {next_q} guide in numbers)"
        fwd_short, fwd_period = f"{latest['quarter'].split()[0]} revenue YoY", latest["quarter"]
        guide_text = (f"{next_q}: no revenue guide in numbers in any filing" +
                      (f"; in words only ({w['doc']}): '{w['words']}'" if w else "") + "; no fiscal-year revenue, EPS or margin guide")
        cat3 = (f"(3) A {next_q} revenue guide — none in numbers" + (f"; the {w['doc']} says '{w['words']}'" if w else "") +
                ": NVIDIA's outlook is given on its calls, which are not filings")
        guide_ids = [w["source"]] if w else []
    margin_guided = False                          # no fiscal-year margin guide: no guided step; the signal uses the latest quarter
    fy_margin_base = h["prev_fy_op_margin"]

    # ── dividend: none ('We have never paid and do not expect to pay cash dividends for the foreseeable future.') ──
    per_split = lambda pub, rate: split_txt(pub, " (per share before the {l} split effective {e})") if rate else ""   # a rate, not "none"
    divs = [(d["published"], d["quarterly"] * 4, d["note"] + per_split(d["published"], d["quarterly"]), d["source"])
            for d in facts["dividends"] if d["published"] <= as_of]
    if h["dividend_annual"] is not None:      # a 10-K that states no rate (the FY2021 10-K) leaves the latest filing that states one
        divs.append((h["published"], h["dividend_annual"], h["dividend_note"] + per_split(h["published"], h["dividend_annual"]), None))
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
    fy = lambda d: min(fiscal_year(d), cur_fy)     # a day past the last guided year keeps that year's EPS
    # the listing rule: the window runs from the first trading day (every price day is on or after it), up to ten years
    window = [d for d in days if d > minus_years(as_of, 10) and (not h["pe_window_start"] or d >= h["pe_window_start"])]
    assert window[0] >= listing
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

    # ── era-dependent text, from facts only: no disruption theme has dated evidence on AS_OF ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
    key_tail = ("A GPU downturn shows up in channel inventories and the next quarter's\n"
                "  revenue first; the bear needs it in gross margin as well.")
    theme_summary = "no disruption theme has dated evidence"
    cat4 = (f"(4) Inventories — {latest['inventory_pct']:+.1f}% against revenue {latest['sales_pct']:+.1f}% in {latest['quarter']} "
            f"({latest['inventory_gap_pp']:+.1f}pp): write-downs follow if orders slow")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    # only a print public before the open can meet AS_OF's close: NVIDIA released after the previous day's close, so a print dated
    # AS_OF occurs only in a week with no trading day after it (a Friday)
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    company, exchange = h["company"], h["exchange"]
    ids = (list(h["sources"]) + [facts["listing"]["source"]] + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])]
           + [public[i - 1]["source"]] + guide_ids + ([dividend_src] if dividend_src else []) + split_ids)
    sources = [dict(id=x, **facts["sources"][x]) for x in dict.fromkeys(ids)]
    sources.append({"id": "Y0", "published": as_of, "title": "Yahoo Finance daily prices, NVDA and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/NVDA/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF (Yahoo's split-adjusted close x{fx:g}), 52-week range, realized vol, "
                                f"beta, the {window_label} P/E distribution from the listing on {listing}"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "seq_pct", "gross_margin", "gross_margin_bp", "op_margin",
                   "op_margin_bp", "opex_pct", "opex_gap_pp", "inventory_b", "inventory_pct", "inventory_gap_pp", "eps_q", "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    first_excl = "; ".join(f"FY{int(y) % 100:02d} {t}" for y, t in sorted(h.get("eps_first_excluded", {}).items()))
    rev_text = (f"Revenue: {latest['sales_note']}; {latest['inventory_note']}; {latest['eps_note']}; {latest['shares_note']}"
                + (f"; {latest['note']}" if latest.get("note") else ""))
    # the vintage's repurchase words count shares on the basis of its filing: a later split is named (FY2007 10-K: before 2007-09-11)
    cash_return = latest["cash_return_text"] or (h["cash_return_text"] + split_txt(h["published"], " (shares before the {l} split effective {e})"))
    R = repr
    head = f'''#!/usr/bin/env python3
"""
NVDA Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: NVDA)  ·  {h["business_line"]}
Generated by retro/build_nvda.py from retro/facts/NVDA.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "NVDA"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); semiconductor signals with "
               "NVIDIA's rule-T thresholds; the listing rule (NVDA listed 1999-01-22)")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts above.
PIT_PROFILE = {{
    "kind": {R(h["kind"])},
    "risk": 2,
    "why": {R(h["why"])},
    "theme_watch": {R(watch)},
    "evidence": [],
}}

# ── FACTS: market (prices truncated at AS_OF, on the AS_OF share basis) ───────
LISTING_DATE    = "{listing}"   # first trading day ({facts["listing"]["exchange"]}): the P/E window starts no earlier
CURRENT_PRICE   = {close:.2f}   # USD, {exchange} close {as_of}, as traded (Yahoo's split-adjusted close x{fx:g})
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

# ── FACTS: company history ({", ".join(h["sources"])}, vintage {h["published"]}{h["extended"]}) ──
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}{"; " + h["split_note"] if h.get("split_note") else ""}
EPS_FIRST_EXCLUDED = {R(first_excl)}
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # revenue, USD bn
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
EPP_TODAY_EPS   = {round(eps_now, 6)}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # the next-quarter revenue guide as growth on the year-ago quarter (else the latest quarter's growth)
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
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenue {h['prev_fy_sales_growth']:+.1f}%, gross margin {h['prev_fy_gross_margin']:.1f}%; {latest['quarter'].split()[0]} gross margin {latest['gross_margin']:.2f}% ({latest['gross_margin_bp']:+.0f}bp YoY)")}
BALANCE_TEXT    = {R(f"Cash, cash equivalents and marketable securities ${latest['cash_b']:.3f}B, {latest['debt_note']} ({latest['quarter']}), {h['fcf_label']} free cash flow ${h['fcf_b']:.3f}B ({h['fcf_note']}), " + (f"dividend ${dividend:.2f} a year" if dividend else "no dividend"))}
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


def _range(v):
    lo, hi = v
    return f"{lo:+g}%" if lo == hi else f"{lo:+g}% to {hi:+g}%"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dates", nargs="*")
    ap.add_argument("--weekly", nargs=2, metavar=("START", "END"))
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/NVDA)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("NVDA"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<45}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
