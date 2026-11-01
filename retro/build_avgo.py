#!/usr/bin/env python3
"""
Build AVGO retrospective models from the dated fact sheet (retro/facts/AVGO.json).

The AVGO sibling of build_nke.py: the same frozen rules (retro method r2), the same weekly dates and the same market
statistics, with analog semiconductor signals (retro/templates/avgo_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints, guides and events whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, as traded on each day (Yahoo's
     split-adjusted series with the later splits undone), so the price and the per-share facts share one basis,
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Avago Technologies Limited listed on 2009-08-06 (Nasdaq: AVGO); before that it filed only as the issuer of notes. The series
starts at the listing (the owner's choice: no AVGO price exists in 2008), and two rules, decided on 2026-11-01 before any AVGO
model was built or scored, cover what a new listing lacks (retro/README.md, "AVGO"):
  - the listing rule: the stock's own P/E exists only from its first trading day, so the P/E window runs from the listing,
    up to ten years (labelled in trading days below a year);
  - the bounds rule: where the history is too short to measure a rule, the rule's own bound stands (BEAR's 0% cap, BULL's BASE
    floor, XBULL's BULL floor, no net buyback, a neutral growth factor; in the engine).
Avago's fiscal year ended on October 31 to FY2007 and from FY2008 on the Sunday closest to October 31. It gave no fiscal-year
revenue, EPS or margin guide; each release guides the next quarter's revenue as growth on the quarter just reported. The method
r2 inputs map with the fallbacks decided before any AVGO date was built or scored:
  - current-FY EPS: no EPS guide in numbers, so the last full year in the history stands (the rollover rule): FY08's $0.26;
    FY06, FY07 and FY09 were losses with no published adjusted figure and are excluded (the ACN FY02 / AAPL FY2001 rule;
    FY09 as a latest year, the NKE FY2018 rule);
  - forward revenue growth: the next-quarter guide, read as a dollar level on the reported quarter and then as growth on the
    same quarter a year earlier (the AAPL dollar-level rule); with no guide for the next quarter in scope, the latest quarter's
    revenue growth (the UNP rule);
  - guided margin step: none (no fiscal-year margin guide); the margin signal uses the latest quarter's operating-margin change.
The quarter outlook's other lines (gross margin, operating expenses, interest, taxes, share count) are display only.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings
release, where it is the first trading day after it. Avago released after the close, so a print is dated the next trading
day (its 8-K's acceptance time); in 2009 that day was a Friday, the week's last trading day, so the print meets its close
(public before the open).

From 2016-02-02 the listed company is Broadcom Limited, the successor issuer to Avago (company_names in the fact sheet). The one
theme encoding decided so far: the FY2016 10-K names the shift to cloud-based IT as a risk to its own segments (CLOUD, live from
2012-10-30), so CLOUD joins the watch list (company-acknowledged, no market read); the factor pair nets to zero and the theme signal
stays at 2/4, so only text changes.

Output goes to staging/retrospective/AVGO until the series is added to the archive (--out archive/retrospective/AVGO).

Usage
  python3 retro/build_avgo.py --weekly 2009-08-03 2009-12-31
  python3 retro/build_avgo.py --weekly 2010-01-04 2012-12-31
  python3 retro/build_avgo.py --weekly 2013-01-07 2016-12-31
  python3 retro/build_avgo.py 2009-09-04
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/AVGO/<AS_OF>
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
from build_unp import money, on_basis  # noqa: E402

FACTS = os.path.join(HERE, "facts", "AVGO.json")
ENGINE = os.path.join(HERE, "templates", "avgo_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "AVGO")
# the guide fields this builder has an encoding for; any other field (a number) needs its encoding decided first
# (level_stated: a guide stated as a dollar level, read against the year-ago quarter directly, from the 8-K of 2010-08-10)
GUIDE_KEYS = {"fy", "published", "source", "doc", "quarter", "seq_pct", "base_quarter", "base_sales_m", "level_m", "prior_label",
              "prior_sales_m", "prior_source", "yoy_pct", "quote", "display", "level_stated"}
# rule T, the engine's signal thresholds: (rule_t key, BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"revenue": (-39, -18, 4, 11), "gross_margin": (-1080, -560, -30, 1480), "opex_gap": (31, 16, 2, -18),
                     "inventory_gap": (54, 23, -8, -18), "op_margin": (-1540, -820, -100, 1630)}
RULE_T_KEYS = {"revenue": (1, False), "gross_margin": (10, False), "opex_gap": (1, True), "inventory_gap": (1, True),
               "op_margin": (10, False)}


def fiscal_year_end(n):
    """Avago's fiscal year n ends on October 31 to FY2007 and from FY2008 on the Sunday closest to October 31."""
    d = dt.date(n, 10, 31)
    if n <= 2007:
        return d
    back, fwd = (d.weekday() - 6) % 7, (6 - d.weekday()) % 7
    return d - dt.timedelta(back) if back <= fwd else d + dt.timedelta(fwd)


def fiscal_year(day):
    """The fiscal year a calendar day belongs to."""
    d = dt.date.fromisoformat(day)
    return d.year if d <= fiscal_year_end(d.year) else d.year + 1


def rule_t(rt):
    """Rule T thresholds from the annual values the filings report (four, three for the inventory gap; the LOW and NKE
    formula on fewer than ten): XBULL best, BULL median, BASE worst, BEAR one median-to-worst step beyond the worst; rounded
    half up to whole percent or points and to 10 bp."""
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
    """Re-derive a print's margins, growth and gaps from its raw published figures (they must match the fact sheet)."""
    r = p["raw"]
    pct = lambda a, b: (b / a - 1) * 100
    r1 = lambda x: round(x + 0.0, 1)
    want = dict(sales_pct=r1(pct(r["sales_prior_m"], r["sales_m"])), seq_pct=r1(pct(r["sales_prev_q_m"], r["sales_m"])),
                gross_margin=round((r["sales_m"] - r["cogs_m"]) / r["sales_m"] * 100, 2),
                gross_margin_bp=r1(((r["sales_m"] - r["cogs_m"]) / r["sales_m"]
                                    - (r["sales_prior_m"] - r["cogs_prior_m"]) / r["sales_prior_m"]) * 10000),
                op_margin=round(r["op_income_m"] / r["sales_m"] * 100, 2),
                op_margin_bp=r1((r["op_income_m"] / r["sales_m"] - r["op_income_prior_m"] / r["sales_prior_m"]) * 10000),
                opex_pct=r1(pct(r["rd_prior_m"] + r["sga_prior_m"], r["rd_m"] + r["sga_m"])),
                opex_gap_pp=r1(pct(r["rd_prior_m"] + r["sga_prior_m"], r["rd_m"] + r["sga_m"]) - pct(r["sales_prior_m"], r["sales_m"])),
                inventory_pct=r1(pct(r["inventory_prior_m"], r["inventory_m"])),
                inventory_gap_pp=r1(pct(r["inventory_prior_m"], r["inventory_m"]) - pct(r["sales_prior_m"], r["sales_m"])))
    for k, v in want.items():
        assert p[k] == v, (p["quarter"], k, p[k], v)


def check_guide(g):
    lv = g["level_m"] if g.get("level_stated") else [round(g["base_sales_m"] * (1 + s / 100), 2) for s in g["seq_pct"]]
    assert lv == g["level_m"] and lv[0] <= lv[1], (g["doc"], lv)
    assert [round((x / g["prior_sales_m"] - 1) * 100 + 0.0, 1) for x in lv] == g["yoy_pct"], (g["doc"], "yoy")


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    listing = facts["listing"]["first_trading_day"]
    assert min(raw) == listing, ("the price data must start on the listing day", min(raw), listing)
    # every price of the window on the AS_OF share basis: Yahoo's split-adjusted series times the splits after AS_OF,
    # so the AS_OF close is the price as traded and the per-share facts below share its basis
    chart = retro_tool.chart("AVGO")
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
    # on_basis (the shared split helper) divides every Q4 print's full-year EPS; an excluded year has none, so a NaN stands in
    # for it there and None comes back after (no split follows a distorted year in the fact sheet, so nothing else changes)
    held = {p["quarter"] for p in facts["prints"] if "fy_actual" in p and p["fy_actual"]["eps_normalized"] is None}
    facts = {**facts, "prints": [{**p, "fy_actual": {**p["fy_actual"], "eps_normalized": math.nan}} if p["quarter"] in held else p
                                 for p in facts["prints"]]}
    facts, split_ids = on_basis(facts, as_of)
    for p in facts["prints"]:
        if p["quarter"] in held:
            p["fy_actual"]["eps_normalized"] = None
            assert not any(p["published"] < sp["effective"] <= as_of for sp in facts.get("splits", [])), \
                (as_of, "a split after an excluded year: decide how its GAAP figure is restated first")
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    # prints published by AS_OF that report a fiscal year after the history (a Q4 print reports the year just ended,
    # so it stays in scope after the 10-K that follows it); events published since the vintage
    # a year excluded from the EPS history ('eps_excluded': a distorted latest year with no published adjusted figure) is still
    # reported; the first years left out ('eps_first_excluded') precede the history, which starts after them
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    prints = [p for p in facts["prints"] if p["published"] <= as_of and guide_fy(p) >= first_fy]
    events = [e for e in facts["events"] if e["published"] <= as_of and (h["published"] <= e["published"] or "doc" not in e)]
    # the one theme encoding decided so far: a 10-K whose risk factors name the shift to cloud-based IT as a risk to the company's
    # own segments (CLOUD, from the FY2016 10-K; the FY2009-FY2015 10-Ks name cloud only for their own IT service providers) puts
    # the theme on the watch list. No other theme in taxonomy_eras.json is live for this semiconductor maker in 2009-2016
    # (OFFSHORE is scoped to IT services, GENAI is live from 2022-11-30): any other kind of event needs its encoding decided first
    if any(e["kind"] != "cloud_company_acknowledged" for e in events):
        sys.exit(f"{as_of}: the AVGO builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is public yet")
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage
    h = {**h, "extended": ""}
    for p in prints:
        a = p.get("fy_actual")
        if a and a["fy"] not in reported(h):          # the 10-K vintage, once out, wins
            y = str(a["fy"])
            if a["eps_normalized"] is None:           # a distorted year: reported, but out of the EPS history
                h.update(eps_excluded={**h.get("eps_excluded", {}), y: a["excluded_note"]})
            h.update(fy_label=a["fy_label"],
                     eps_normalized={**h["eps_normalized"], **({y: a["eps_normalized"]} if a["eps_normalized"] is not None else {})},
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]},
                     diluted_shares_m={**h["diluted_shares_m"], y: a["diluted_shares_m"]},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_op_margin=a["op_margin"], prev_fy_op_margin_note=a["op_margin_note"],
                     prev_fy_pretax_margin=a["pretax_margin"], prev_fy_pretax_margin_note=a["pretax_margin_note"],
                     prev_fy_gross_margin=a["gross_margin"], prev_fy_sales_growth=a["sales_growth"],
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    latest = prints[-1]
    prev = ((prints[-2]["sales_pct"], prints[-2]["quarter"]) if len(prints) > 1
            else (h["prev_q_sales_pct"], h["prev_q_label"]))
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
    # ── forward revenue growth: the latest guide for the quarter after the latest print, as growth on the year-ago quarter ──
    qg = [g for g in facts["guides"] if g["published"] <= as_of and g["quarter"] == next_q]
    if qg:
        g = qg[-1]
        fwd = list(g["yoy_pct"])
        lvl = (f"${g['level_m'][0]:,.1f}M" if g["level_m"][0] == g["level_m"][1] else
               f"${g['level_m'][0]:,.1f}M-${g['level_m'][1]:,.1f}M")
        prior = f"{g['prior_label']}'s ${g['prior_sales_m']:,}M"
        fwd_label = f"{next_q} revenue guide ({g['doc']})"
        fwd_short, fwd_period = f"{next_q} guide YoY", next_q
        if g.get("level_stated"):     # a dollar level or range: read against the year-ago quarter directly (the AAPL rule)
            seq = f"about {lvl}" if g["level_m"][0] == g["level_m"][1] else lvl
            guide_text = (f"{next_q} outlook ({g['doc']}): net revenue {lvl} ('{g['quote']}') against {prior}: {_range(fwd)} YoY; "
                          f"display only: {g['display']}; no fiscal-year revenue, EPS or margin guide")
            cat3 = (f"(3) The {next_q} guide — {seq} ({_range(fwd)} YoY): Avago guides one quarter at a time, in revenue only")
        else:
            sg = lambda x: f"{x:+g}%" if x else "0%"
            seq = sg(g["seq_pct"][0]) if g["seq_pct"][0] == g["seq_pct"][1] else f"{sg(g['seq_pct'][0])} to {sg(g['seq_pct'][1])}"
            guide_text = (f"{next_q} outlook ({g['doc']}): net revenue {seq} on {g['base_quarter']}'s ${g['base_sales_m']:,}M ('{g['quote']}'), "
                          f"i.e. {lvl} against {prior}: {_range(fwd)} YoY; display only: {g['display']}; "
                          f"no fiscal-year revenue, EPS or margin guide")
            cat3 = (f"(3) The {next_q} guide — {seq} on {g['base_quarter']} ({_range(fwd)} YoY): Avago guides one quarter at a time, "
                    f"in revenue only")
        guide_ids = [g["source"], g["prior_source"]]
    else:
        fwd = [latest["sales_pct"]] * 2
        fwd_label = f"{latest['quarter']} revenue growth (no {next_q} guide in scope)"
        fwd_short, fwd_period = f"{latest['quarter'].split()[0]} revenue YoY", latest["quarter"]
        guide_text = f"{next_q}: no revenue guide in scope yet; no fiscal-year revenue, EPS or margin guide"
        guide_ids = []
        cat3 = f"(3) A {next_q} guide — none in scope yet: Avago guides one quarter at a time, in revenue only"
    # no margin guide in any filing of the period: no guided step, and the margin signal uses the latest quarter
    margin_guided = False
    fy_margin_base = h["prev_fy_op_margin"]

    # ── dividend: none declared ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts["dividends"] if d["published"] <= as_of]
    divs.append((h.get("dividend_published", h["published"]), h["dividend_annual"], h["dividend_note"], None))
    _, dividend, dividend_note, dividend_src = max(divs, key=lambda x: x[0])

    # ── market statistics, prices truncated at AS_OF (all from the listing on) ──
    days = sorted(d for d in px if d <= as_of)
    close = px[as_of][2]
    yr = [d for d in days if d > minus_years(as_of, 1)]
    low52, high52 = min(px[d][1] for d in yr), max(px[d][0] for d in yr)
    common = [d for d in yr if d in spx]
    ra = [math.log(px[common[i]][2] / px[common[i - 1]][2]) for i in range(1, len(common))]
    rm = [math.log(spx[common[i]][2] / spx[common[i - 1]][2]) for i in range(1, len(common))]
    if len(ra) >= 2:            # realized volatility and beta need at least two daily returns since the listing
        ma, mm = sum(ra) / len(ra), sum(rm) / len(rm)
        vol = (sum((x - ma) ** 2 for x in ra) / len(ra)) ** 0.5 * 252 ** 0.5
        beta = (sum((x - ma) * (y - mm) for x, y in zip(ra, rm)) / len(ra)) / (sum((y - mm) ** 2 for y in rm) / len(rm))
    else:
        vol = beta = None
    eps = {**eps_hist, cur_fy: eps_now}                                # + current-FY EPS, for the P/E series
    # fiscal year of a day; a day past the last guided year keeps that year's EPS
    fy = lambda d: min(fiscal_year(d), cur_fy)
    # the listing rule: the window runs from the first trading day (every price day is on or after it), up to ten years
    window = [d for d in days if d > minus_years(as_of, 10) and (not h["pe_window_start"] or d >= h["pe_window_start"])]
    assert window[0] >= listing
    # an excluded year's own days leave the window (the r2 rule's "the window starts after it", for a year that is not the first)
    gone = sorted({fy(d) for d in window} & set(excluded))
    window = [d for d in window if fy(d) not in excluded]
    assert window, (as_of, "no P/E day left in the window")
    assert all(fy(d) in eps for d in window), (as_of, "P/E window needs EPS for every fiscal year")
    years = (dt.date.fromisoformat(as_of) - dt.date.fromisoformat(window[0])).days / 365.25
    window_label = ("10-yr" if years > 9.9 else f"{years:.1f}-yr" if years >= 1 else f"{len(window)}-trading-day") + "".join(
        f" ex-FY{y % 100:02d}" for y in gone)
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

    # ── era-dependent text, from facts only: which disruption theme has dated evidence on AS_OF ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
    key_tail = ("A semiconductor downturn shows up in distributor inventories and the\n"
                "  next-quarter guide first; the bear needs it in gross margin as well.")
    theme_summary = "no disruption theme has dated evidence"
    for e in [e for e in events if e["kind"] == "cloud_company_acknowledged"][-1:]:
        # CLOUD is live from 2012-10-30 and scoped to on-premise hardware and storage; the first 10-K whose risk factors name the
        # shift to cloud-based IT as a risk to the company's own segments (FY2016) puts it on the watch list (the ACN CLOUD rule,
        # as for LOW and NKE: company-acknowledged, no market read). The factor pair nets to zero and the theme signal stays at
        # 2/4, so only text changes; re-filing needs dated evidence of market pricing
        val_word = "a premium" if pe_now_pctl >= 70 else "a discount to its own history" if pe_now_pctl <= 30 else "near its own median"
        stage = "cloud"
        watch = [{"theme": "CLOUD", "status": "live, company-acknowledged; no market read",
                  "reason": (f"Live: the company's own {e['doc']} says '{e['risk_quote']}' At the same time {e['offering']}. "
                             f"The stock trades at {close / eps_now:.1f}x {fy_e_s} — {val_word}. Re-file as DISRUPTION_EXPOSED (CLOUD) "
                             "only if dated evidence shows the market pricing cloud substitution of its enterprise storage and "
                             "networking specifically.")}]
        factors = [(f"Cloud data centers: {e['offering_short']} — it sells to them as well", 0.2, 0.10),
                   (f"Shift to cloud-based IT ({e['doc']}): {e['risk_short']}", -0.2, 0.10)]
        sig_name = "Cloud: net effect on enterprise storage and networking"
        trigger = "Enterprise data centers move to the cloud faster than its cloud data-center sales grow"
        theme_summary = "cloud is live and company-acknowledged; no dated evidence ties the multiple to it"
    cat4 = (f"(4) Inventories — {latest['inventory_pct']:+.1f}% against net revenue {latest['sales_pct']:+.1f}% in {latest['quarter']} "
            f"({latest['inventory_gap_pp']:+.1f}pp): write-downs follow if orders slow")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    # only a print public before the open can meet AS_OF's close: Avago released after the previous day's close, so a print
    # dated AS_OF occurs only in a week with no trading day after it (the Fridays 2009-09-04 and 2009-12-04)
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    renames = [n for n in facts.get("company_names", []) if h["published"] < n["published"] <= as_of]
    company = renames[-1]["name"] if renames else h["company"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])] + guide_ids
           + ([dividend_src] if dividend_src else []) + split_ids + [e["id"] for e in events] + [n["source"] for n in renames])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "A0", "published": as_of, "title": "Yahoo Finance daily prices, AVGO and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/AVGO/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, the range since the listing on {listing}, realized vol, beta, "
                                f"the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "seq_pct", "gross_margin", "gross_margin_bp", "op_margin",
                   "op_margin_bp", "opex_pct", "opex_gap_pp", "inventory_b", "inventory_pct", "inventory_gap_pp", "eps_q", "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    first_excl = "; ".join(f"FY{int(y) % 100:02d} {t}" for y, t in sorted(h.get("eps_first_excluded", {}).items()))
    rev_text = (f"Net revenue: {latest['sales_note']}; {latest['inventory_note']}; {latest['eps_note']}; {latest['shares_note']}")
    R = repr
    head = f'''#!/usr/bin/env python3
"""
AVGO Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} (Nasdaq: AVGO)  ·  {h["business_line"]}
Generated by retro/build_avgo.py from retro/facts/AVGO.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "AVGO"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); analog semiconductor signals; "
               "the listing and short-history bounds rules (AVGO)")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts and events above.
PIT_PROFILE = {{
    "kind": "DURABLE",
    "risk": 2,
    "why": {R(h["why"])},
    "theme_watch": {R(watch)},
    "evidence": {R(list(dict.fromkeys(e["id"] for e in events)))},
}}

# ── FACTS: market (prices truncated at AS_OF, as traded on each day, from the listing) ──
LISTING_DATE    = "{listing}"   # first trading day ({facts["listing"]["exchange"]})
CURRENT_PRICE   = {close:.2f}   # USD, Nasdaq close {as_of}
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2
PE_PCTL         = {R(pctl)}   # current-FY P/E over the window below
PE_NOW_PCTL     = {pe_now_pctl}    # share of those daily P/Es at or below the AS_OF one
WINDOW_LABEL    = {R(window_label)}   # P/E window: {window[0]} .. AS_OF ({len(window)} trading days)
YEARLY_MIN_PE   = {R(yearly)}   # (calendar year, lowest P/E, date)
VOL_RETURNS     = {len(ra)}   # daily returns since the listing
VOL_ANNUAL_PCT  = {f"{vol:.3f}" if vol is not None else None}   # realized, daily log returns (None: fewer than two returns)
VOL_BETA        = {f"{beta:.2f}" if beta is not None else None}    # beta vs S&P 500 over the same days
VOL_52W_LOW     = {low52:.2f}
VOL_52W_HIGH    = {high52:.2f}
REF_LOW         = {px[ref][2]:.2f}   # lowest close since the listing, {ref}
REF_LOW_LABEL   = {R(MONTHS[int(ref[5:7]) - 1])}

# ── FACTS: company history ({", ".join(h["sources"])}, vintage {h["published"]}{h["extended"]}) ──
EPS_NORM      = {R(eps_hist)}   # {h["normalization"]}
EPS_FIRST_EXCLUDED = {R(first_excl)}
REVENUE_HIST  = {R(rev)}   # net revenue, USD bn
SHARES_HIST   = {R(shares)}   # diluted, millions
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
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
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
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} net revenue {h['prev_fy_sales_growth']:+.1f}%, gross margin {h['prev_fy_gross_margin']:.1f}%; {latest['quarter'].split()[0]} gross margin {latest['gross_margin']:.2f}% ({latest['gross_margin_bp']:+.0f}bp YoY)")}
BALANCE_TEXT    = {R(f"Cash ${latest['cash_b']:.3f}B, " + (f"long-term debt ${latest['ltd_b']:.3f}B" if latest['ltd_b'] else "no long-term debt") + f" ({latest['quarter']}), {h['fcf_label']} free cash flow ${h['fcf_b']:.3f}B ({h['fcf_note']}), " + (f"dividend ${dividend:.2f} a year" if dividend else "no dividend"))}
REVENUE_TEXT    = {R(rev_text)}
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


def _range(v):
    lo, hi = v
    return f"{lo:+g}%" if lo == hi else f"{lo:+g}% to {hi:+g}%"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dates", nargs="*")
    ap.add_argument("--weekly", nargs=2, metavar=("START", "END"))
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/AVGO)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("AVGO"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<45}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
