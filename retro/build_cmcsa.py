#!/usr/bin/env python3
"""
Build CMCSA retrospective models from the dated fact sheet (retro/facts/CMCSA.json).

The CMCSA sibling of build_pfe.py: the same frozen rules (retro method r2), the same weekly dates and the same market statistics,
with cable signals (retro/templates/cmcsa_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints, guides and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, as traded (Yahoo's series times its factors after AS_OF:
     the 2-for-1 split of 2017-02-21 on the dates before it, and the 1.067 of 2026-01-05; each split restates the per-share facts
     published before it through the fact sheet's 'splits': the 3-for-2 of 2007-02-22 precedes every date, and the 2-for-1 of
     2017-02-21 halves the earlier per-share facts from its own date),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Comcast's fiscal year is the calendar year. EPS is diluted EPS from continuing operations, replaced by the company's adjusted figure
where that figure excludes only one-offs (2006-2008; the ACN rule); the company's 2004-2005 adjusted income strips all investment and
other income, which recur, so it is not used. 2003 (a loss from continuing operations) is excluded and the history and the P/E window
start with 2004 ('pe_window_start'; the ACN FY02, AAPL FY2002 and PFE 2003 rule). The releases guide consolidated revenue growth for
the fiscal year in percent, pro forma, and no EPS. The method r2 inputs map as follows (retro/README.md, "CMCSA"):
  - current-FY EPS: no EPS guide, so the last full year's EPS stands (the rollover rule),
  - forward revenue growth: no next-quarter guide, so the fiscal-year revenue growth range as stated (the release's own percentage,
    the MAR rule); a one-sided bound ('at least 11%') or no guide in numbers: the latest quarter's revenue growth as reported,
  - guided margin step: none (the operating cash flow growth guide is not an operating-margin guide; the AAPL gross-margin rule);
    the margin signal takes the latest quarter's operating margin change.

A Q4 print may restate an earlier year's EPS ('restates'): the Q4 2010 release first publishes 2009's EPS excluding one-offs ($1.11;
GAAP $1.26), so it replaces that year from the print until a 10-K vintage published after the print carries it (the PFE, XOM, SHW and
BKR encoding; retro/README.md, "CMCSA 2010-2013"). NBCUniversal (consolidated from 2011-01-28) enters through the prints as published.

From 2014 (retro/README.md, "CMCSA 2014-2017"): each 10-K vintage holds the ten years to its own year; no filing gives an outlook in
numbers, so BASE takes the latest quarter's reported growth; STREAMING, live from 2015-08-04, joins the watch list from each 10-K's
consumer-behaviour risk factor (company-acknowledged, no market read: the label and text only).

From 2018 (retro/README.md, "CMCSA 2018-2021"): the 10-K vintages after the 2017 split hold each year as first published, with
'eps_published' and 'shares_published' dating the pre-split figures so the split restates them; the company's EPS excluding one-offs
stands for 2017 ($2.06, restated to $2.03 by the Q4 2018 release, 'restates') and 2018 ($2.55); from 2019 its Adjusted EPS also excludes
amortization of acquisition-related intangible assets, which recurs, so 2019 and 2020 are GAAP (the 2004-2005 rule). Still no outlook
in numbers; Sky enters the growth as published from the fourth quarter of 2018.

From 2022 (retro/README.md, "CMCSA 2022-2026"): 2022 is excluded as a distorted year (the Sky impairments; reported EPS under half the
EPS without its listed items, no figure excluding only them), in the PFE encoding ('eps_excluded', an 'excluded_note' on the Q4 2022
print's 'fy_actual'; its days leave the P/E window); the 2026 separation of Versant is a distribution ('distributions', the MAR and PFE
rule: Yahoo's factor is undone for the days before it); from the FY2023 10-K the share line counts the Connectivity & Platforms segments.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. The earnings 8-Ks of 2007-2017 were accepted before the open except Q1 2011's (after the close, dated
the next trading day); only Q3 2012's came on a Friday.

Output goes to staging/retrospective/CMCSA until the series is added to the archive (--out archive/retrospective/CMCSA).

Usage
  python3 retro/build_cmcsa.py --weekly 2008-01-01 2009-12-31
  python3 retro/build_cmcsa.py 2008-02-15
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/CMCSA/<AS_OF>
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
from build_unp import money, on_basis, pct_range  # noqa: E402

FACTS = os.path.join(HERE, "facts", "CMCSA.json")
ENGINE = os.path.join(HERE, "templates", "cmcsa_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "CMCSA")
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"video": (-10, -1, 8, 151), "sales": (0, 10, 19, 126), "ocf_margin": (-510, -230, 50, 220),
                     "capex": (1270, 620, -30, -1150), "op_margin": (-2440, -1210, 10, 3370)}
RULE_T_KEYS = {"video": (1, False), "sales": (1, False), "ocf_margin": (10, False), "capex": (10, True),
               "op_margin": (10, False)}           # (rounding unit, lower is better)


def fiscal_year_end(n):
    """Comcast's fiscal year n is the calendar year n."""
    return dt.date(n, 12, 31)


def fiscal_year(day):
    return dt.date.fromisoformat(day).year


def rule_t_value(k, r):
    """One annual rule-T value from its raw figures ($ millions; subscribers in the unit of their table)."""
    if k == "video":
        return round((r["subscribers"][1] / r["subscribers"][0] - 1) * 100, 2)
    (a0, a1), (o0, o1) = r["revenues_m"], r["operating_income_m"]
    if k == "sales":
        return round((a1 / a0 - 1) * 100, 2)
    if k == "op_margin":
        return round((o1 / a1 - o0 / a0) * 10000, 1)
    if k == "ocf_margin":                    # operating income before depreciation and amortization
        (d0, d1), (m0, m1) = r["depreciation_m"], r["amortization_m"]
        return round(((o1 + d1 + m1) / a1 - (o0 + d0 + m0) / a0) * 10000, 1)
    c0, c1 = r["capex_m"]                    # capital expenditures as a share of revenues
    return round((c1 / a1 - c0 / a0) * 10000, 1)


def rule_t(rt):
    """Rule T thresholds from the annual values (re-derived from the raw figures): XBULL best, BULL median, BASE worst, BEAR one
    median-to-worst step beyond the worst (mirrored when lower is better); rounded half up to whole percent and to 10 bp."""
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
    """Re-derive a print's growth and margins from its raw published figures (they must match)."""
    r = p["raw"]
    m, m0 = r["ocf_m"] / r["rev_m"] * 100, r["ocf_prior_m"] / r["rev_prior_m"] * 100
    o, o0 = r["oi_m"] / r["rev_m"] * 100, r["oi_prior_m"] / r["rev_prior_m"] * 100
    c, c0 = r["capex_m"] / r["rev_m"] * 100, r["capex_prior_m"] / r["rev_prior_m"] * 100
    want = {"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": round((r["rev_m"] / r["rev_prior_m"] - 1) * 100, 1),
            "video_pct": round((r["video_k"] / r["video_prior_k"] - 1) * 100, 2),
            "ocf_margin": round(m, 2), "ocf_margin_bp": round((m - m0) * 100, 1), "op_margin": round(o, 2),
            "op_margin_bp": round((o - o0) * 100, 1), "capex_pct": round(c, 2), "capex_bp": round((c - c0) * 100, 1),
            "diluted_shares_m": float(r["diluted_shares_m"])}
    for k, v in want.items():
        assert p[k] == v or abs(p[k] - v) < 1e-9, (p["quarter"], k, p[k], v)


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    # every price of the window as traded: Yahoo's split-adjusted series times its factors after AS_OF (2017's 2-for-1, 2026's 1.067)
    chart = retro_tool.chart("CMCSA")
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    # a split record must sit on a split date of the price data; on_basis applies it from its effective date
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat()
                    for v in chart.get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo_splits for s in facts.get("splits", [])), "a split's effective date must match the price data"
    # a distribution (the 2026-01-02 separation of Versant, one Versant share for every 25 Comcast shares) is not a split: Yahoo books
    # it as a 1067:1000 split on 2026-01-05, so from that date its factor is undone for the days before it and every price stays as
    # traded (the MAR and PFE 'distributions' rule; the drop stays in the series); per-share facts are not restated
    for x in facts.get("distributions", []):
        ev = [v for v in chart.get("events", {}).get("splits", {}).values()
              if dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat() == x["effective"]]
        assert len(ev) == 1 and ev[0]["numerator"] / ev[0]["denominator"] == x["yahoo_factor"], (x["effective"], "Yahoo's factor")
        if x["effective"] <= as_of:
            px = {d: (tuple(v * x["yahoo_factor"] for v in hlc) if d < x["effective"] else hlc) for d, hlc in px.items()}
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        check_print(p)
    # on_basis (the shared split helper) divides every Q4 print's full-year EPS; an excluded year has none, so a NaN stands in for it
    # there and None comes back after (the NKE, XOM and PFE encoding; no split follows an excluded year in the fact sheet)
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
    # a year excluded from the EPS history ('eps_excluded': a year distorted by one-offs with no published figure excluding only them;
    # retro/README.md, "CMCSA 2022-2026") is still reported (the NKE FY2018, XOM FY2020 and PFE 2023 rule)
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
    # prints published by AS_OF that report a fiscal year after the history (a Q4 print reports the year just ended, so it
    # stays in scope after the 10-K that follows it)
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    prints = [p for p in facts["prints"] if p["published"] <= as_of and guide_fy(p) >= first_fy]
    # no disruption theme in taxonomy_eras.json is live for a cable operator before STREAMING (scoped to linear TV networks and pay-TV
    # bundles, live from 2015-08-04). The one encoding decided (retro/README.md, "CMCSA 2014-2017"): each 10-K's consumer-behaviour risk
    # factor, which names online video services as competition for Comcast's video services (streaming_company_acknowledged), puts
    # STREAMING on the watch list from the theme's live date, with the latest 10-K's words (a 10-K's wording is replaced by the next
    # 10-K's; the MSFT CLOUD, XOM and WMT rule). Any other event kind needs its encoding decided first
    events = [e for e in facts["events"] if e["published"] <= as_of and (h["published"] <= e["published"] or "doc" not in e)]
    if any(e["kind"] != "streaming_company_acknowledged" for e in events):
        sys.exit(f"{as_of}: the CMCSA builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
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
            if a["eps_normalized"] is None:           # an excluded year: reported, but out of the EPS history
                h.update(eps_excluded={**h.get("eps_excluded", {}), y: a["excluded_note"]})
            h.update(fy_label=a["fy_label"],
                     eps_normalized={**h["eps_normalized"], **({y: a["eps_normalized"]} if a["eps_normalized"] is not None else {})},
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]},
                     diluted_shares_m={**h["diluted_shares_m"], y: a["diluted_shares_m"]},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_op_margin=a["op_margin"], prev_fy_op_margin_note=f'FY{y[2:]} operating margin ({p["source"]})',
                     prev_fy_ocf_margin=a["ocf_margin"],
                     prev_fy_pretax_margin=a["pretax_margin"], prev_fy_pretax_margin_note=a["pretax_margin_note"],
                     prev_fy_sales_growth=a["sales_growth"], prev_fy_capex_pct=a["capex_pct"],
                     prev_fy_video_pct=a["video_pct"], prev_fy_video_note=a["video_note"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    # a Q4 print may restate an earlier year's EPS ('restates': the Q4 2010 release first publishes 2009 excluding one-offs); each year
    # comes from the latest filing that reports it, so the restated figure replaces the year from the print until a 10-K vintage
    # published after the print carries the year (retro/README.md, "CMCSA 2010-2013")
    for p in prints:
        if p.get("restates") and p["published"] > h["published"]:
            for yy, r in p["restates"].items():
                assert yy in h["eps_normalized"], (p["quarter"], yy, "restates a year outside the history")
                h.update(eps_normalized={**h["eps_normalized"], yy: r["eps"]},
                         normalization=f'{h["normalization"]}; {p["restates_note"]}',
                         extended=f'{h["extended"]}, FY{yy[2:]} restated by {p["source"]} ({p["published"]})')
    latest = prints[-1]
    # the previous quarter is the print published just before the latest one (in or out of the history's scope)
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    i = public.index(latest)
    assert i > 0, (as_of, "the fact sheet needs the print before the latest one")
    prev = (public[i - 1]["video_pct"], public[i - 1]["quarter"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    excluded = {int(k): v for k, v in h.get("eps_excluded", {}).items()}
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)        # the last full year in the history: cur_fy - 1 unless that year is excluded
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    last_rev = rev[max(rev)]

    # ── guides for the current fiscal year, each field from the latest guide that states it ──
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    stated = lambda k: next((g for g in reversed(guides) if k in g), None)
    gr = stated("rev_guide_pct")
    eps_now = eps_hist[last_fy]              # Comcast guides no EPS: the last full year's EPS stands (rollover rule)
    eps_label = f"{fy_e}: no EPS guide, {fy_now[:2]}{last_fy % 100:02d}'s ${money(eps_now)} stands" + "".join(
        f" (FY{y % 100:02d} is excluded: {excluded[y]})" for y in range(last_fy + 1, cur_fy))
    fy_prev_s = f"FY{max(rev) % 100:02d}"
    if gr:                                   # the fiscal-year revenue growth range, as the release states it (pro forma)
        fwd = [float(v) for v in gr["rev_guide_pct"]]
        fwd_label, fwd_short, fwd_period = f"{fy_now} revenue guide", f"{fy_now} guide", fy_now
        fwd_kind = f"fiscal-year {gr['rev_label']} {pct_range(*fwd)} as stated (no next-quarter guide)"
        fy_rev_b, fy_rev_label = last_rev * (1 + sum(fwd) / 2 / 100), f"{fy_now} revenue guide midpoint, on {fy_prev_s} as reported"
    else:                                    # no revenue guide in numbers: the latest quarter's growth as reported
        fwd = [latest["sales_pct"]] * 2
        fwd_label = f"no {fy_now} revenue guide in numbers, {latest['quarter']} revenue growth"
        fwd_short, fwd_period = f"{latest['quarter'][:2]} revenues", latest["quarter"]
        fwd_kind = f"no revenue guide in numbers: {latest['quarter']} growth as reported"
        fy_rev_b = last_rev * (1 + latest["sales_pct"] / 100)
        fy_rev_label = f"{fwd_label}, applied to the year"
    if guides:
        g = guides[-1]
        bits = ([f"{gr['rev_label']} {pct_range(*fwd)}"] if gr else []) + \
               ([f"'{g['rev_words']}' (a one-sided bound: no field)"] if "rev_words" in g and not gr else []) + \
               ["no EPS guide"] + ([g["note"]] if g.get("note") else [])
        guide_text = f"{fy_now} guide ({', '.join(dict.fromkeys(x['doc'] for x in guides))}): " + "; ".join(bits)
    else:
        guide_text = f"{fy_now}: no guide in numbers yet"
    margin_guided = False                          # no operating-margin guide: no guided step
    fy_margin_base = h["prev_fy_op_margin"]

    # ── dividend: the latest declared rate (the latest declaration public on AS_OF, else the vintage's) ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts["dividends"] if d["published"] <= as_of]
    if divs:
        _, dividend, dividend_note, dividend_src = max(divs, key=lambda x: x[0])
    else:
        dividend, dividend_note, dividend_src = h["dividend_annual"], h["dividend_note"], None

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
    window = [d for d in days if d > minus_years(as_of, 10) and (not h["pe_window_start"] or d >= h["pe_window_start"])]
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

    # ── era-dependent text, from facts only: which disruption theme has dated evidence on AS_OF ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
    key_tail = ("DBS and phone-company video are the competition the 10-K names; pricing and\n"
                "  digital, Internet and phone growth are what must cover the video losses.")
    theme_summary = "no disruption theme has dated evidence"
    why = h["why"]
    if h.get("why_theme_tail"):                    # from the FY2014 vintage the theme clause follows the theme's status on AS_OF
        why += "; no disruption theme is live for it"
    for e in [e for e in events if e["kind"] == "streaming_company_acknowledged"][-1:]:
        # STREAMING is live from 2015-08-04; the latest 10-K's consumer-behaviour risk factor puts it on the watch list (the ACN CLOUD
        # rule, as for WMT: company-acknowledged, no market read). The factor pair nets to zero and the theme signal stays at 2/4, so only
        # text changes. The registry's market-pricing event (2015-08-04) is Disney's cable-network outlook and a sector sell-off, which
        # names no Comcast fact, so it is quoted from its date and re-files nothing (the WMT, LOW and PEP reading); re-filing needs dated
        # evidence of market pricing for Comcast
        th = themes[e["theme"]]
        mp = [x for x in th["pit_evidence"] if x["date"] <= as_of]
        mp_txt = (f" The theme registry dates the market's pricing of streaming to {mp[-1]['date']} ({mp[-1]['event']}), evidence that "
                  "names Disney's networks, not Comcast." if mp else "")
        val_word = "a premium" if pe_now_pctl >= 70 else "a discount to its own history" if pe_now_pctl <= 30 else "near its own median"
        stage = "streaming"
        watch = [{"theme": "STREAMING", "status": "live, company-acknowledged; no market read",
                  "reason": (f"Live: Comcast's own {e['doc']} says '{e['risk_quote']}' At the same time {e['offering']}. "
                             f"The stock trades at {close / eps_now:.1f}x {fy_e_s} — {val_word}.{mp_txt} Re-file as DISRUPTION_EXPOSED "
                             "(STREAMING) only if dated evidence shows the market pricing streaming substitution of Comcast's video "
                             "customers or networks specifically.")}]
        factors = [(f"Own streaming: {e['offering_short']}", 0.2, 0.10),
                   (f"Online video competition ({e['doc']}): {e['risk_short']}", -0.2, 0.10)]
        sig_name = "Streaming: net effect on video demand"
        trigger = "Online video takes video customers and viewing faster than Comcast's own streaming keeps them"
        key_tail = ("DBS, phone-company and online video services are the competition the 10-K names;\n"
                    "  pricing and Internet and business services growth must cover the video losses.")
        theme_summary = "streaming is live and company-acknowledged; no dated evidence ties the multiple to it"
        assert h.get("why_theme_tail"), "a vintage before FY2014 states that no theme is live"
        why = h["why"] + ("; STREAMING is live (from 2015-08-04) and its consumer-behaviour risk factor puts it on the watch list: "
                          "company-acknowledged, with no dated evidence that the market prices it for Comcast")
    cat3 = (f"(3) {fy_now} revenue guide {pct_range(*fwd)} ({gr['doc']}): the company's own read of the year" if gr else
            f"(3) A {fy_now} revenue guide in numbers — none yet")
    cat4 = (f"(4) Capital intensity — capital expenditures {latest['capex_pct']:.1f}% of revenues in {latest['quarter']} "
            f"({latest['capex_bp']:+.1f}bp): set-top boxes and network against free cash flow")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{latest['next_print'].split(' print')[0]} print)"
    # a print dated AS_OF meets AS_OF's close only if it was public before it: before the open or during the session
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        rt = same_day[-1].get("release_time", "")
        assert "before the open" in rt or "during the session" in rt, (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the close")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the close)"

    company, exchange = h["company"], h["exchange"]
    groups = [tuple(g) for g in h["groups"]]
    ids = (list(h["sources"]) + [p["source"] for p in prints] + [g["source"] for g in guides]
           + ([dividend_src] if dividend_src else []) + split_ids + [e["id"] for e in events]
           + [x["source"] for x in facts.get("distributions", []) if x["effective"] <= as_of])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "W0", "published": as_of, "title": "Yahoo Finance daily prices, CMCSA and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/CMCSA/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "video_pct", "ocf_margin", "ocf_margin_bp", "op_margin",
                   "op_margin_bp", "capex_pct", "capex_bp", "eps_q", "eps_q_prior")
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    r = latest["raw"]
    volumes = (f"video subscribers {r['video_k']:,}K against {r['video_prior_k']:,}K a year earlier ({latest['video_pct']:+.2f}%), "
               f"as the release shows them; capital expenditures ${r['capex_m']:,}M against ${r['capex_prior_m']:,}M"
               + (f"; {latest['note']}" if latest.get("note") else ""))
    cable_names = [n for n, _, _ in groups if n in ("Cable", "Cable Communications")]
    cable_word = "cable" if cable_names else "connectivity & platforms"          # the segments from the FY2023 10-K
    cable_names = cable_names or [n for n, _, _ in groups if "Connectivity" in n]
    cable = sum(v for n, v, _ in groups if n in cable_names) / sum(v for _, v, _ in groups) * 100
    R = repr
    head = f'''#!/usr/bin/env python3
"""
CMCSA Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: CMCSA)  ·  {h["business_line"]}
Generated by retro/build_cmcsa.py from retro/facts/CMCSA.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "CMCSA"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); cable signals")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts above.
PIT_PROFILE = {{
    "kind": "DURABLE",
    "risk": 2,
    "why": {R(why)},
    "theme_watch": {R(watch)},
    "evidence": {R(list(dict.fromkeys(e["id"] for e in events)))},
}}

# ── FACTS: market (prices truncated at AS_OF, as traded on each day) ──────────
CURRENT_PRICE   = {close:.2f}   # USD, {exchange} close {as_of}, as traded (Yahoo's adjusted close x{fx:g})
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

# ── FACTS: company history ({", ".join(h["sources"])}, vintage {h["published"]}{h["extended"]}) ──
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}{("; " + h["split_note"]) if h.get("split_note") else ""}
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # revenues, USD bn
SHARES_HIST   = {R({y: round(v, 3) for y, v in shares.items()})}   # diluted, millions
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # operating margin, {h["prev_fy_op_margin_note"]}
CHECK_PRETAX_MARGIN = {h["prev_fy_pretax_margin"]}   # {h["prev_fy_pretax_margin_note"]}, for the EPS check
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_VIDEO      = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # {fwd_kind}
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no operating-margin guide in numbers, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {fy_rev_b:.2f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R(groups)}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenues {h['prev_fy_sales_growth']:+.1f}%, {cable_word} {cable:.0f}% of segment revenues, video subscribers {h['prev_fy_video_pct']:+.2f}% ({h['prev_fy_video_note']}); {latest['quarter'].split()[0]} operating cash flow margin {latest['ocf_margin']:.2f}% ({latest['ocf_margin_bp']:+.1f}bp)")}
BALANCE_TEXT    = {R(f"{h['fcf_label']} year-end cash and current investments ${h['cash_b']:.2f}B, {h['fcf_label']} free cash flow ${h['fcf_b']:.2f}B, dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
VOLUMES_TEXT    = {R(volumes)}
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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dates", nargs="*")
    ap.add_argument("--weekly", nargs=2, metavar=("START", "END"))
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/CMCSA)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("CMCSA"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<34}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
