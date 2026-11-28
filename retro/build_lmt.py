#!/usr/bin/env python3
"""
Build LMT retrospective models from the dated fact sheet (retro/facts/LMT.json).

The LMT sibling of build_cat.py: the same frozen rules (retro method r2), the same weekly dates and the same market statistics,
with defense prime contractor signals (retro/templates/lmt_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints, guides and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, as traded (Yahoo's series is adjusted for the 1995
     combination factor and the 1999 2-for-1 split, both before every per-share fact in the fact sheet, so Yahoo's close is the
     price as traded on every day of every window),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Lockheed Martin's fiscal year is the calendar year. EPS is diluted EPS (from continuing operations where the five-year summary reports
the line), each year from the latest 10-K that reports it; the unusual items' per-share effects stay in (no filing publishes an EPS
excluding them for 2003-2008: the NKE FY2008 rule). FY2002 is excluded (its unusual items exceed its earnings from continuing operations
and no per-share figure excluding them was published: the AAPL FY2002 test), so the history and the P/E window start with FY2003
('pe_window_start'; the ACN FY02 rule). The releases guide the fiscal year only, never a quarter, in an outlook table whose 'Current
Update' column holds net sales, segment operating profit, diluted EPS and cash from operations; the third-quarter release adds a
preliminary outlook for the next year. The method r2 inputs map as follows (retro/README.md, "LMT"):
  - current-FY EPS: the diluted EPS guide midpoint; no guide: the last full year's EPS stands (the rollover rule),
  - forward revenue growth: no next-quarter guide, so the fiscal-year net sales guide, a dollar range read against the last full
    year (the PFE and CAT rule),
  - guided margin step: none (the segment operating profit guide is a dollar range: no margin is derived from two guided figures, the
    MSFT, AAPL and AVGO rule); the margin signal takes the latest quarter's segment margin change; segment operating profit and cash
    from operations are shown in the guide line only.
From 2010 (retro/README.md, "LMT 2010-2013"): diluted EPS from continuing operations where the release or the five-year summary reports
the line (PAE and EIG in discontinued operations from mid-2010); a release that republishes earlier years' EPS restates them until a later
10-K ('restates', EPS only: the Q4 2010 and Q4 2011 releases' prior year, the Q1 2011 release's 2008-2010 adjusted for the change in
revenue recognition); words in the outlook's current column keep the last numeric range, and a level stated as about is a number.
From 2014 (retro/README.md, "LMT 2014-2017"): the same encodings through Sikorsky (acquired 2015-11-06) and the IS&GS divestiture (in
discontinued operations from the Q3 2016 release; the Q4 2016 release restates FY2015's EPS, the FY2016 10-K 2012-2016, earlier years
stay as published: a seam); the current column is found by its header (the Q3 2016 release's 'Current Outlook Adjusted for IS&GS');
ECOMMERCE, STREAMING and ENERGY_TRANSITION are read as out of scope, and the texts give every live theme's reading as of AS_OF.
From 2018 (retro/README.md, "LMT 2018-2021"): FY2017's GAAP EPS fails the AAPL FY2002 test (the Tax Act), so it is the company's figure
from the latest filing that publishes one ($13.33, restated to $13.27 by the Q4 2018 release); the 2018 net sales guide is read against
the 2017 pro forma for the 2018 standards that the release states beside it ('rev_base_usd_b', the ACN restated-base rule); a guide given
with and without an announced item takes the figure without it (the 2021 pension settlement); EPS growth against a year-ago loss is over
the loss's absolute value (the CAT rule); EV and CRYPTO are read as out of scope.
From 2022 (retro/README.md, "LMT 2022-2026"): GAAP EPS throughout, as the company's adjusted EPS also removes recurring mark-to-market
investment items (2021-2023) or results of programs in performance (2024); an outlook that includes a booked one-off with no figure
without it stands as published (the 2022 pension settlement, the 2025 program losses); from 2023 segment operating profit excludes
intangible asset amortization, each print against the year-ago quarter as its own release recasts it; GENAI and GLP1 are read as out of
scope from each vintage's own words.
Signals: backlog growth (total backlog at the quarter's end against the year-ago quarter's end, as that quarter's own release shows it:
the MSFT rule), net sales growth, segment operating profit growth, diluted EPS growth and the segment operating margin change, each
against the year-ago quarter as the release shows it.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. Every earnings 8-K of 2006-2021 was accepted before the open (06:30-07:42 ET) on a Monday (Q2 2015,
Q4 2017 and Q2 2021), a Tuesday, a Wednesday or a Thursday, so each such week is dated the next trading day; so was every one of
2022-2026 (06:26-07:42 ET, Tuesdays, and Thursdays from Q4 2025).

Output goes to staging/retrospective/LMT until the series is added to the archive (--out archive/retrospective/LMT).

Usage
  python3 retro/build_lmt.py --weekly 2008-01-01 2009-12-31
  python3 retro/build_lmt.py --weekly 2010-01-04 2013-12-31
  python3 retro/build_lmt.py --weekly 2014-01-06 2017-12-31
  python3 retro/build_lmt.py --weekly 2018-01-01 2021-12-31
  python3 retro/build_lmt.py --weekly 2022-01-03 2026-11-15
  python3 retro/build_lmt.py 2008-01-25
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/LMT/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "LMT.json")
ENGINE = os.path.join(HERE, "templates", "lmt_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "LMT")
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"backlog": (-14, -7, 1, 29), "sales": (-19, -7, 5, 20), "segop": (-18, 0, 18, 22), "eps": (0, 21, 41, 45),
                     "seg_margin": (-30, 10, 50, 100)}
RULE_T_KEYS = {"backlog": (1, False), "sales": (1, False), "segop": (1, False), "eps": (1, False),
               "seg_margin": (10, False)}          # (rounding unit, lower is better)
# the disruption themes this builder has an encoding for: OFFSHORE is live from 2004-11-05 but scoped to offshore delivery in
# Western consulting, systems integration and outsourcing, which Lockheed Martin's 10-Ks never name as competition; CLOUD is live from
# 2012-10-30 but scoped to public cloud displacing on-premise hardware, storage, databases and data-center outsourcing, and the
# FY2009-FY2012 10-Ks never mention cloud (retro/README.md, "LMT 2010-2013"; text only). From 2015 ECOMMERCE, STREAMING and
# ENERGY_TRANSITION become live; their scopes (physical retail, linear TV, oil, gas and coal reserves and refining) name nothing Lockheed
# Martin sells or holds, so they are read as out of scope too, and the FY2016 10-K's one mention of cloud computing (a technology
# advance in its competition paragraph) leaves CLOUD out of scope (retro/README.md, "LMT 2014-2017"; text only)
# From 2020 EV and CRYPTO become live; their scopes (road vehicles' powertrains and fuel retail, payments, banks and exchanges) name
# nothing Lockheed Martin sells or holds either, and from the FY2017 vintage the theme reading quotes the 10-K's oil and gas market for
# Sikorsky's commercial helicopters ('oil_words'); text only (retro/README.md, "LMT 2018-2021")
# From 2022-11-30 GENAI and from 2023-08-08 GLP1 become live; their scopes (software seats, IT services, professional information,
# search, education content and mobility; snacks, beverages and sleep-apnea, diabetes and cardio devices) name nothing Lockheed Martin
# sells, and its 10-Ks name artificial intelligence only among the technological advances enabling new competitors (and from the FY2023
# 10-K a technology others may misuse, from FY2024 one it must integrate into its own processes and offerings: 'ai_words'), never as a
# substitute for its products, and never name GLP-1 drugs; from the FY2021 10-K the climate reading quotes the vintage's regulation and
# severe-weather words ('climate_words', 'weather_words'); text only (retro/README.md, "LMT 2022-2026")
ENCODED_THEMES = {"OFFSHORE", "CLOUD", "ECOMMERCE", "STREAMING", "ENERGY_TRANSITION", "EV", "CRYPTO", "GENAI", "GLP1"}
THEME_ORDER = ("OFFSHORE", "CLOUD", "ECOMMERCE", "STREAMING", "ENERGY_TRANSITION", "EV", "CRYPTO", "GENAI", "GLP1")
THEME_SCOPE = {"OFFSHORE": "offshore delivery taking share in Western consulting, systems integration and outsourcing",
               "CLOUD": "public cloud displacing on-premise hardware, storage, databases and data-center outsourcing",
               "ECOMMERCE": "e-commerce displacing physical retail, malls, grocery and distribution",
               "STREAMING": "streaming displacing linear TV networks and pay-TV bundles",
               "ENERGY_TRANSITION": "decarbonisation stranding oil, gas and coal reserves and refining",
               "EV": "battery-electric vehicles displacing ICE powertrains, auto parts suppliers and fuel retail",
               "CRYPTO": "crypto-assets disintermediating payments networks, banks, exchanges and remittance",
               "GENAI": "generative or autonomous AI substituting software seats, IT services and BPO hours, professional information, search, "
                        "education content and mobility",
               "GLP1": "GLP-1 obesity drugs reducing demand for snacks, beverages and sleep-apnea, diabetes and cardio devices"}
AI_ROLES = ("among technological advances enabling new factors of competition", "as a threat in others' hands",
            "as a technology to integrate into its own processes and offerings")


def theme_reading(themes, as_of, h, plural):
    """Every live theme's scope and what the 10-K (or, plural, the 10-Ks) say about it, from the vintage's own words (LMT 2014-2017)."""
    live = [k for k in THEME_ORDER if themes[k]["live_from"] <= as_of]
    scopes = [f"{k} (live from {themes[k]['live_from']}) " + ("is scoped to " if i == 0 else "to ") + THEME_SCOPE[k]
              for i, k in enumerate(live)]
    scope = scopes[0] if len(scopes) == 1 else ", ".join(scopes[:-1]) + ", and " + scopes[-1]
    s = (lambda one, many: many if plural else one)
    doc = s("the 10-K", "the 10-Ks")
    absent = ["offshore competition"] + [w for k, w in (("ECOMMERCE", "e-commerce"), ("STREAMING", "streaming"),
                                                         ("EV", "electric vehicles"), ("CRYPTO", "crypto-assets"),
                                                         ("GLP1", "GLP-1 drugs")) if k in live]
    text = f"{scope}; {doc} {s('names', 'name')} no " + (absent[0] if len(absent) == 1 else
                                                         ", ".join(absent[:-1]) + " or " + absent[-1])
    if "CLOUD" in live:
        text += (f" and {s('names', 'name')} cloud computing only among technological advances 'enabling new factors of competition for "
                 "both traditional and non-traditional competitors', not as a substitute for its products" if h.get("cloud_words") else
                 f" and {s('does', 'do')} not mention cloud")
    # from the FY2021 10-K the climate words name regulation and severe weather, not only future regulation (LMT 2022-2026)
    climate = (f"climate change only as a source of regulation and cost ('{h['climate_words']}') and of severe weather "
               f"('{h['weather_words']}')" if h.get("weather_words") else
               f"climate change only among concerns that could bring future regulation ('{h.get('climate_words')}')")
    if "ENERGY_TRANSITION" in live and h.get("oil_words"):
        text += (f"; Lockheed Martin holds no oil, gas or coal reserves or refining, and {doc} {s('names', 'name')} oil and gas only as a "
                 f"market for Sikorsky's commercial helicopters ('{h['oil_words']}') and {climate}")
    elif "ENERGY_TRANSITION" in live:
        text += f"; Lockheed Martin holds no oil, gas or coal reserves or refining, and {doc} {s('names', 'name')} {climate}"
    if "GENAI" in live:
        roles = [f"{AI_ROLES[i]} ('{w}')" for i, w in enumerate(h["ai_words"])]
        text += (f"; {doc} {s('names', 'name')} artificial intelligence only " + (roles[0] if len(roles) == 1 else
                 ", ".join(roles[:-1]) + " and " + roles[-1]) + ", never as a substitute for its aircraft, missiles, helicopters and satellites")
    return text


def fiscal_year_end(n):
    """Lockheed Martin's fiscal year n is the calendar year n."""
    return dt.date(n, 12, 31)


def fiscal_year(day):
    return dt.date.fromisoformat(day).year


def eps_rng(lo, hi):
    """an EPS range: '7.05-7.25'"""
    return money(lo) if lo == hi else f"{money(lo)}-{money(hi)}"


def usd_rng(lo, hi):
    """a dollar level or range in billions: '$41.8-42.8B'"""
    f = lambda x: f"{x:g}"
    return f"${f(lo)}B" if lo == hi else f"${f(lo)}-{f(hi)}B"


def rule_t_value(k, r):
    """One annual rule-T value from its raw figures ($ millions; EPS in dollars)."""
    if k == "backlog":
        a0, a1 = r["backlog_m"]
    elif k == "sales":
        a0, a1 = r["sales_m"]
    elif k == "segop":
        a0, a1 = r["segop_m"]
    elif k == "eps":
        a0, a1 = r["eps"]
    else:                                                  # segment operating profit on net sales
        (o0, o1), (s0, s1) = r["segop_m"], r["sales_m"]
        return round((o1 / s1 - o0 / s0) * 10000, 1)
    return round((a1 / a0 - 1) * 100, 2)


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
    """Re-derive a print's growth and margins from its raw published figures (they must match)."""
    r = p["raw"]
    m, m0 = r["segop_m"] / r["rev_m"] * 100, r["segop_prior_m"] / r["rev_prior_m"] * 100
    want = {"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": round((r["rev_m"] / r["rev_prior_m"] - 1) * 100, 1),
            "backlog_pct": round((r["backlog_m"] / r["backlog_prior_m"] - 1) * 100, 1),
            "segop_pct": round((r["segop_m"] / r["segop_prior_m"] - 1) * 100, 1),
            "seg_margin": round(m, 2), "seg_margin_bp": round((m - m0) * 100, 1),
            # against a year-ago loss, growth over the loss's absolute value (the CAT rule; first needed for Q4 2018)
            "eps_pct": round((p["eps_q"] / p["eps_q_prior"] - 1) * 100, 1) if p["eps_q_prior"] > 0 else
                       round((p["eps_q"] - p["eps_q_prior"]) / abs(p["eps_q_prior"]) * 100, 1),
            "diluted_shares_m": float(r["diluted_shares_m"])}
    for k, v in want.items():
        assert p[k] == v or abs(p[k] - v) < 1e-9, (p["quarter"], k, p[k], v)


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    # every price of the window as traded: Yahoo's split-adjusted series times the splits after AS_OF (none after 1999)
    chart = retro_tool.chart("LMT")
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat()
                    for v in chart.get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo_splits for s in facts.get("splits", [])), "a split's effective date must match the price data"
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
        # every per-share fact postdates the last split in the price data (1999-01-04), so no split restates it
        last_split = max(yahoo_splits)
        assert v["published"] > last_split and min(int(y) for y in v["eps_normalized"]) > int(last_split[:4]), \
            (v["published"], "a per-share fact precedes the last split: it needs a 'splits' record")
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        check_print(p)
    facts, split_ids = on_basis(facts, as_of)
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    reported = lambda h: {int(k) for k in h["eps_normalized"]}
    # prints published by AS_OF that report a fiscal year after the history (a Q4 print reports the year just ended, so it
    # stays in scope after the 10-K that follows it)
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    prints = [p for p in facts["prints"] if p["published"] <= as_of and guide_fy(p) >= first_fy]
    # no disruption theme in scope is live for a defense prime contractor in 2008-2009; the builder refuses events, and refuses a
    # date on which a theme it has no encoding for is live
    events = [e for e in facts["events"] if e["published"] <= as_of and (h["published"] <= e["published"] or "doc" not in e)]
    if events:
        sys.exit(f"{as_of}: the LMT builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
    themes = retro_tool.load_taxonomy()["themes"]
    live = sorted(k for k, t in themes.items() if t["live_from"] <= as_of)
    if set(live) - ENCODED_THEMES:
        sys.exit(f"{as_of}: themes {sorted(set(live) - ENCODED_THEMES)} are live and the LMT builder has no reading of them; decide one first")
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is public yet")
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage
    h = {**h, "extended": ""}
    for p in prints:
        a = p.get("fy_actual")
        if a and a["fy"] not in reported(h):          # the 10-K vintage, once out, wins
            y = str(a["fy"])
            h.update(fy_label=a["fy_label"],
                     eps_normalized={**h["eps_normalized"], y: a["eps_normalized"]},
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]},
                     diluted_shares_m={**h["diluted_shares_m"], y: a["diluted_shares_m"]},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_op_margin=a["op_margin"], prev_fy_op_margin_note=f'FY{y[2:]} segment operating margin ({p["source"]})',
                     prev_fy_pretax_margin=a["pretax_margin"], prev_fy_pretax_margin_note=a["pretax_margin_note"],
                     prev_fy_sales_growth=a["sales_growth"], prev_fy_backlog_pct=a["backlog_pct"], prev_fy_segop_pct=a["segop_pct"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    # a release may republish earlier years' EPS (the Q4 2010 and Q4 2011 releases' prior year from continuing operations, the Q1 2011
    # release's 2008-2010 adjusted for the change in revenue recognition); each year comes from the latest filing that reports it, so the
    # figure replaces the year from the print until a 10-K vintage published after the print carries the year (the PFE and CAT
    # 'restates' encoding, EPS only; retro/README.md, "LMT 2010-2013")
    for p in prints:
        if p.get("restates") and p["published"] > h["published"]:
            for yy, rr in p["restates"].items():
                assert yy in h["eps_normalized"], (p["quarter"], yy, "restates a year outside the history")
                h.update(eps_normalized={**h["eps_normalized"], yy: rr["eps"]}, normalization=f'{h["normalization"]}; {rr["note"]}',
                         extended=f'{h["extended"]}, FY{yy[2:]} restated by {p["source"]} ({p["published"]})')
    latest = prints[-1]
    # the previous quarter is the print published just before the latest one (in or out of the history's scope)
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    i = public.index(latest)
    assert i > 0, (as_of, "the fact sheet needs the print before the latest one")
    prev = (public[i - 1]["backlog_pct"], public[i - 1]["quarter"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    last_rev = rev[max(rev)]
    fy_prev_s = f"FY{max(rev) % 100:02d}"

    # ── guides for the current fiscal year, each field from the latest guide that states it ──
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    stated = lambda *ks: next((g for g in reversed(guides) if any(k in g for k in ks)), None)
    ge, gr, gs = stated("eps_guide"), stated("rev_guide_usd_b"), stated("segop_guide_usd_b")
    if ge:                                             # a dollar range: its midpoint
        eps_now = round(sum(ge["eps_guide"]) / 2, 3)
        eps_fig = f"${eps_rng(*ge['eps_guide'])}"
        eps_label = f"{fy_e} EPS, guide midpoint ({ge['doc']})"
    else:                                              # no numeric EPS guide: the last full year's EPS stands (rollover rule)
        eps_now = eps_hist[last_fy]
        eps_fig = None
        eps_label = f"{fy_e}: no numeric diluted EPS guide yet, FY{last_fy % 100:02d}'s ${money(eps_now)} stands"
    # a release that states the last full year restated for an accounting change beside the guide gives the base the guide is read
    # against (the ACN restated-base rule; 'rev_base_usd_b': the Q4 2017 release's 2017 pro forma for the 2018 standards); otherwise the
    # last full year in the history (retro/README.md, "LMT 2018-2021")
    gb = stated("rev_base_usd_b")
    if gr:                                             # a dollar range, read against the last full year (the PFE rule)
        base_rev, base_txt = ((gb["rev_base_usd_b"], gb["rev_base_label"]) if gb else (last_rev, f"{fy_prev_s}'s"))
        fwd = [round((v / base_rev - 1) * 100, 1) for v in gr["rev_guide_usd_b"]]
        rev_fig = usd_rng(*gr["rev_guide_usd_b"])
        fwd_kind = f"fiscal-year net sales guide {rev_fig} on {base_txt} ${base_rev:.3f}B (no next-quarter guide)"
        fy_rev_b, fy_rev_label = sum(gr["rev_guide_usd_b"]) / 2, f"{fy_now} net sales guide midpoint"
        fwd_label, fwd_short, fwd_period = f"{fy_now} net sales guide", f"{fy_now} guide", fy_now
    else:                                              # no net sales guide in numbers: the latest quarter's growth as reported
        fwd = [latest["sales_pct"]] * 2
        rev_fig = None
        fwd_kind = f"no net sales guide in numbers: {latest['quarter']} growth as reported"
        fy_rev_b = last_rev * (1 + latest["sales_pct"] / 100)
        fy_rev_label = f"no {fy_now} net sales guide in numbers, {latest['quarter']} growth, applied to the year"
        fwd_label = f"no {fy_now} net sales guide in numbers, {latest['quarter']} growth"
        fwd_short, fwd_period = f"{latest['quarter'][:2]} net sales", latest["quarter"]
    if guides:
        bits = ([f"net sales {rev_fig}"] if gr else []) + \
               ([f"{ge.get('eps_label', 'diluted EPS')} {eps_fig}"] if ge else ["no diluted EPS guide in numbers"]) + \
               ([f"segment operating profit {usd_rng(*gs['segop_guide_usd_b'])} and cash from operations {gs['cfo_words']}M "
                 "(display only: no margin is derived from two guided figures)"] if gs else []) + \
               [g["note"] for g in guides[-1:] if g.get("note")]
        guide_text = f"{fy_now} guide ({', '.join(dict.fromkeys(x['doc'] for x in guides))}): " + "; ".join(bits)
    else:
        guide_text = f"{fy_now}: no guide in numbers yet"
    margin_guided = False                          # no margin guide in numbers: no guided step
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
    assert all(fy(d) in eps for d in window), (as_of, "P/E window needs EPS for every fiscal year")
    years = (dt.date.fromisoformat(as_of) - dt.date.fromisoformat(window[0])).days / 365.25
    window_label = "10-yr" if years > 9.9 else f"{years:.1f}-yr"
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

    # ── era-dependent text, from facts only: OFFSHORE is the only live theme on any date of 2008-2009, and it is out of scope ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none in scope", "No live disruption theme covers defense and government programs"
    key_tail = ("The 10-K ties future sales to Congressional appropriations for defense procurement\n"
                "  and research and development; a terminated or delayed program leaves the backlog.")
    off = themes["OFFSHORE"]
    theme_summary = (f"OFFSHORE (live from {off['live_from']}) is scoped to offshore delivery in Western consulting, systems integration "
                     "and outsourcing, and the 10-Ks name no offshore competition; no theme in scope has dated evidence")
    cl = themes["CLOUD"]
    if cl["live_from"] <= as_of:
        theme_summary = (f"OFFSHORE (live from {off['live_from']}) is scoped to offshore delivery in Western consulting, systems "
                         f"integration and outsourcing, and CLOUD (live from {cl['live_from']}) to public cloud displacing on-premise "
                         "hardware, storage, databases and data-center outsourcing; the 10-Ks name no offshore competition and do not "
                         "mention cloud, so no theme in scope has dated evidence")
    # from 2015 more themes are live, and from the FY2016 10-K cloud is mentioned: the texts name every live theme's scope and what the
    # 10-Ks say, and from the FY2013 vintage ('why_themes') the "why" ends with that reading as of AS_OF, not a fixed clause; every
    # earlier vintage keeps its text, and every earlier date has only OFFSHORE and CLOUD live, so those dates rebuild byte-identical
    if any(themes[k]["live_from"] <= as_of for k in ("ECOMMERCE", "STREAMING", "ENERGY_TRANSITION")) or h.get("cloud_words"):
        theme_summary = theme_reading(themes, as_of, h, plural=True) + ", so no theme in scope has dated evidence"
    why = h["why"]
    if h.get("why_themes"):
        why += "; " + theme_reading(themes, as_of, h, plural=False) + ", so no disruption theme in scope is live"
    cat3 = (f"(3) {fy_now} {ge.get('eps_label', 'diluted EPS')} guide {eps_fig} ({ge['doc']}): the company's own read of the year, FAS/CAS pension adjustment included"
            if ge else f"(3) A {fy_now} diluted EPS guide in numbers — none yet")
    cat4 = (f"(4) {fy_now} net sales guide {rev_fig} ({gr['doc']}): program volume in one number" if gr else
            f"(4) A {fy_now} net sales guide in numbers — none yet")

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
    ids = (list(h["sources"]) + [p["source"] for p in prints] + [latest["backlog_prior_source"]] + [g["source"] for g in guides]
           + ([dividend_src] if dividend_src else []) + split_ids + [e["id"] for e in events])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "W0", "published": as_of, "title": "Yahoo Finance daily prices, LMT and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/LMT/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "backlog_pct", "segop_pct", "seg_margin", "seg_margin_bp", "eps_q",
                   "eps_q_prior", "eps_pct")
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    r = latest["raw"]
    volumes = (f"Total backlog ${r['backlog_m']:,.0f}M at the quarter's end against ${r['backlog_prior_m']:,.0f}M at "
               f"{latest['backlog_prior_label']} ({latest['backlog_pct']:+.1f}%); segment operating profit ${r['segop_m']:,.0f}M against "
               f"${r['segop_prior_m']:,.0f}M a year earlier ({latest['segop_pct']:+.1f}%), as the releases show them"
               + (f"; {latest['note']}" if latest.get("note") else ""))
    R = repr
    head = f'''#!/usr/bin/env python3
"""
LMT Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: LMT)  ·  {h["business_line"]}
Generated by retro/build_lmt.py from retro/facts/LMT.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "LMT"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); defense prime contractor signals")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts above.
PIT_PROFILE = {{
    "kind": "{h.get('kind', 'DURABLE')}",
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
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # net sales, USD bn
SHARES_HIST   = {R({y: round(v, 3) for y, v in shares.items()})}   # diluted, millions
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # segment operating margin, {h["prev_fy_op_margin_note"]}
CHECK_PRETAX_MARGIN = {h["prev_fy_pretax_margin"]}   # {h["prev_fy_pretax_margin_note"]}, for the EPS check
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_BACKLOG    = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # {fwd_kind}
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no margin guide in numbers, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {fy_rev_b:.2f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R(groups)}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} net sales {h['prev_fy_sales_growth']:+.1f}%, backlog {h['prev_fy_backlog_pct']:+.1f}%, segment operating profit {h['prev_fy_segop_pct']:+.1f}%; {latest['quarter'].split()[0]} segment margin {latest['seg_margin']:.2f}% ({latest['seg_margin_bp']:+.1f}bp)")}
BALANCE_TEXT    = {R(f"{h['cash_label']} year-end {h.get('cash_words', 'cash and short-term investments')} ${h['cash_b']:.3f}B, {h['cash_label']} operating cash flow ${h['ocf_b']:.3f}B, dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/LMT)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("LMT"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<34}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
