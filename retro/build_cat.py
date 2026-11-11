#!/usr/bin/env python3
"""
Build CAT retrospective models from the dated fact sheet (retro/facts/CAT.json).

The CAT sibling of build_cmcsa.py: the same frozen rules (retro method r2), the same weekly dates and the same market statistics,
with machinery and engines signals (retro/templates/cat_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints, guides and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, as traded (Yahoo's split-adjusted series times the
     splits after AS_OF: none after 2005, so from 2008 Yahoo's close is the price as traded; the 2-for-1 split of 2005-07-14
     restates the per-share facts published before it through the fact sheet's 'splits', the 1997 split precedes every one),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Caterpillar's fiscal year is the calendar year. EPS is profit per share - diluted, replaced by the company's figure where a filing
publishes one excluding only one-offs (2001: the Q4 2001 release's $2.60 excluding the nonrecurring charges; 2009: $2.18 excluding
redundancy costs; the ACN rule). 2011 stays $7.40 as reported: its $7.79 'excluding the impact of the acquisition of Bucyrus' leaves out
a whole business, not only one-offs (the CMCSA rule); 2012 stays $8.48, with the Siwei goodwill impairment in it, as no figure excluding
it is published. The releases guide the fiscal year only, never a quarter: sales and revenues as a dollar level or range ('about $44 billion', '$42 to $44
billion', 'plus or minus 10 percent from $40 billion') or as growth on the last year ('up 5 to 10 percent'), and profit per share as
a dollar level or range or as growth ('up 5 to 15 percent from 2007'); the 2009 guides are stated with and without redundancy costs,
the 2011 guides from the Q2 2011 release with and without Bucyrus (the figure including it is used: the acquisition had closed).
The method r2 inputs map as follows (retro/README.md, "CAT"):
  - current-FY EPS: the fiscal-year profit per share guide midpoint (a growth guide on its stated base, at its midpoint), the figure
    excluding redundancy costs where both are given (the ACN rule for a guide with and without an announced item); no guide: the last
    full year's EPS stands (the rollover rule),
  - forward revenue growth: no next-quarter guide, so the fiscal-year sales and revenues guide (a dollar guide read against the last
    full year, the PFE rule; a growth guide as stated); each field from the latest guide that states it, in either form (the WMT
    rule); a one-sided bound or words ('to top $50 billion', 'about flat') give no field (the PEP, UNP, LOW, WMT and CMCSA rule),
  - guided margin step: none (no margin guide in numbers); the margin signal takes the latest quarter's operating margin change.
A recast of earlier statements is a history vintage of its own (the MSFT recast rule): the 8-K of 2009-05-14 (SFAS 160 and the 2009
segments; dated 2009-05-15) changes only profit before taxes and operating cash flow, which feed the display-only EPS check and balance line.
The 8-K of 2011-05-23 recasts FY2008-FY2010 for the 2011 segments: from then, and in every print from Q1 2011, the Machinery line is
the external sales of Construction Industries plus Resource Industries and the Engines line those of Power Systems (lines(); the
company describes its segments as supporting customers using machinery and using engines and turbines). From the FY2010 10-K, whose
Item 1A calls the demand for Caterpillar's own products cyclical, the kind is CYCLICAL (the class label only; retro/README.md, "CAT
2010-2013"). A print whose year-ago quarter is a loss (Q1 2010) measures profit per share growth on that loss's absolute value.
From 2014 (retro/README.md, "CAT 2014-2017"): Power Systems is Energy & Transportation from Q1 2014 ('et_m'), still the Engines line;
the company's profit per share excluding restructuring costs (from 2016 also mark-to-market pension and OPEB gains and losses, and in
2016 a goodwill impairment and a deferred tax valuation allowance) is the ACN-rule figure for 2013-2016 and for the guides; the 8-K of
2016-05-16 recasting 2011-2015 for mark-to-market pension accounting is a vintage of its own; a release that republishes an earlier
year's company figure restates it until the next 10-K ('restates', the PFE encoding, EPS only); ENERGY_TRANSITION, live from
2015-12-12, is scoped to reserves and refining, so it stays off the watch list and the texts say so ('why_theme_tail', the BKR reading).
From 2018 (retro/README.md, "CAT 2018-2022"): the releases guide profit per share only (the company's adjusted range where both are
given), so BASE takes the latest quarter's sales growth; a guide may withdraw named fields of its year ('withdrawn': the 8-K of
2020-03-26), which voids them in every earlier guide for that year; no outlook follows in 2020-2022, so the last full year's EPS
stands; EV, live from 2020-01-01, is read as out of scope as well (text only).

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. The earnings 8-Ks of 2007-2017 were accepted before the open, except Q1 2008's and Q4 2010's
(during the session); the Q2 2007 to Q1 2008, Q1 2011, Q2 2011 and Q1 2016 releases came on Fridays, so each of those weeks is dated
its release day.

Output goes to staging/retrospective/CAT until the series is added to the archive (--out archive/retrospective/CAT).

Usage
  python3 retro/build_cat.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_cat.py --weekly 2009-01-05 2009-12-31
  python3 retro/build_cat.py --weekly 2010-01-04 2013-12-31
  python3 retro/build_cat.py --weekly 2014-01-06 2017-12-31
  python3 retro/build_cat.py --weekly 2018-01-01 2022-12-31
  python3 retro/build_cat.py 2008-01-25
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/CAT/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "CAT.json")
ENGINE = os.path.join(HERE, "templates", "cat_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "CAT")
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"mach": (-33, -13, 8, 38), "eng": (-19, -3, 13, 37), "sales": (-24, -6, 12, 33), "eps": (-92, -36, 20, 85),
                     "op_margin": (-710, -320, 80, 160)}
RULE_T_KEYS = {"mach": (1, False), "eng": (1, False), "sales": (1, False), "eps": (1, False),
               "op_margin": (10, False)}           # (rounding unit, lower is better)


def fiscal_year_end(n):
    """Caterpillar's fiscal year n is the calendar year n."""
    return dt.date(n, 12, 31)


def fiscal_year(day):
    return dt.date.fromisoformat(day).year


def eps_rng(lo, hi):
    """an EPS range: '5.20-5.60', a loss in parentheses"""
    m = lambda x: f"({money(-x)})" if x < 0 else money(x)
    return m(lo) if lo == hi else f"{m(lo)}-{m(hi)}"


def usd_rng(lo, hi):
    """a dollar level or range in billions: '$44B', '$42-44B', '$31.5-38.5B'"""
    f = lambda x: f"{x:g}"
    return f"${f(lo)}B" if lo == hi else f"${f(lo)}-{f(hi)}B"


def rule_t_value(k, r):
    """One annual rule-T value from its raw figures ($ millions; profit per share in dollars)."""
    if k in ("mach", "eng"):
        a0, a1 = r["sales_m"]
        return round((a1 / a0 - 1) * 100, 2)
    if k == "eps":
        e0, e1 = r["eps"]
        return round((e1 / e0 - 1) * 100, 2)
    (a0, a1) = r["revenues_m"]
    if k == "sales":
        return round((a1 / a0 - 1) * 100, 2)
    o0, o1 = r["operating_profit_m"]                     # operating profit on sales and revenues
    return round((o1 / a1 - o0 / a0) * 10000, 1)


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


def lines(r):
    """The Machinery and Engines lines of a print: as reported to 2010; from the 2011 segments, Construction Industries plus Resource
    Industries and Power Systems (retro/README.md, "CAT 2010-2013"), renamed Energy & Transportation from Q1 2014 ('et_m'; "CAT
    2014-2017")."""
    if "ci_m" in r:
        e, e0 = (r["et_m"], r["et_prior_m"]) if "et_m" in r else (r["ps_m"], r["ps_prior_m"])
        return r["ci_m"] + r["ri_m"], r["ci_prior_m"] + r["ri_prior_m"], e, e0
    return r["mach_m"], r["mach_prior_m"], r["eng_m"], r["eng_prior_m"]


def check_print(p):
    """Re-derive a print's growth and margins from its raw published figures (they must match)."""
    r = p["raw"]
    o, o0 = r["oi_m"] / r["rev_m"] * 100, r["oi_prior_m"] / r["rev_prior_m"] * 100
    m, m0, e, e0 = lines(r)
    e1, e0q = p["eps_q"], p["eps_q_prior"]
    want = {"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": round((r["rev_m"] / r["rev_prior_m"] - 1) * 100, 1),
            "mach_pct": round((m / m0 - 1) * 100, 1),
            "eng_pct": round((e / e0 - 1) * 100, 1),
            "op_margin": round(o, 2), "op_margin_bp": round((o - o0) * 100, 1),
            # growth on a loss is measured on its absolute value, so its direction stays right (every earlier base is positive)
            "eps_pct": round((e1 / e0q - 1) * 100, 1) if e0q > 0 else round((e1 - e0q) / abs(e0q) * 100, 1),
            "diluted_shares_m": float(r["diluted_shares_m"])}
    for k, v in want.items():
        assert p[k] == v or abs(p[k] - v) < 1e-9, (p["quarter"], k, p[k], v)


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    # every price of the window as traded: Yahoo's split-adjusted series times the splits after AS_OF (none after 2005)
    chart = retro_tool.chart("CAT")
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    # a split record must sit on a split date of the price data; on_basis applies it from its effective date
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat()
                    for v in chart.get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo_splits for s in facts.get("splits", [])), "a split's effective date must match the price data"
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
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
    # no disruption theme in taxonomy_eras.json is live for a construction and mining equipment and engine maker in 2008-2009
    # (ENERGY_TRANSITION, scoped to oil, gas, coal and refining, from 2015-12-12; EV from about 2020; OFFSHORE to IT services):
    # the builder refuses events until a theme encoding is decided
    events = [e for e in facts["events"] if e["published"] <= as_of and (h["published"] <= e["published"] or "doc" not in e)]
    if events:
        sys.exit(f"{as_of}: the CAT builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
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
                     prev_fy_op_margin=a["op_margin"], prev_fy_op_margin_note=f'FY{y[2:]} operating margin ({p["source"]})',
                     prev_fy_pretax_margin=a["pretax_margin"], prev_fy_pretax_margin_note=a["pretax_margin_note"],
                     prev_fy_sales_growth=a["sales_growth"], prev_fy_mach_pct=a["mach_pct"], prev_fy_eng_pct=a["eng_pct"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    # a release may republish an earlier year's company figure ('restates': the Q4 2014 release's 2013 excluding restructuring costs,
    # the Q1 2016 release's 2015 recast for mark-to-market pension accounting, the Q4 2016 release's 2015 adjusted figure); each year
    # comes from the latest filing that reports it, so the figure replaces the year from the print until a 10-K vintage published after
    # the print carries the year (the PFE encoding, EPS only; retro/README.md, "CAT 2014-2017")
    for p in prints:
        if p.get("restates") and p["published"] > h["published"]:
            for yy, r in p["restates"].items():
                assert yy in h["eps_normalized"], (p["quarter"], yy, "restates a year outside the history")
                h.update(eps_normalized={**h["eps_normalized"], yy: r["eps"]}, normalization=f'{h["normalization"]}; {r["note"]}',
                         extended=f'{h["extended"]}, FY{yy[2:]} restated by {p["source"]} ({p["published"]})')
    latest = prints[-1]
    # the previous quarter is the print published just before the latest one (in or out of the history's scope)
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    i = public.index(latest)
    assert i > 0, (as_of, "the fact sheet needs the print before the latest one")
    prev = (public[i - 1]["mach_pct"], public[i - 1]["quarter"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    last_rev = rev[max(rev)]
    fy_prev_s = f"FY{max(rev) % 100:02d}"

    # ── guides for the current fiscal year, each field from the latest guide that states it (in either form, the WMT rule) ──
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    # a withdrawal voids the fields it names in every earlier guide for its year (the WMT, LOW and SHW rule: the 8-K of 2020-03-26;
    # retro/README.md, "CAT 2018-2022"), so the last full year's EPS stands and BASE takes the latest quarter's sales growth
    wd = [g for g in guides if g.get("withdrawn")]
    for w in wd:
        guides = [({k: v for k, v in g.items() if k not in w["withdrawn"]} if g["published"] < w["published"] else g) for g in guides]
    w = wd[-1] if wd else None
    stated = lambda *ks: next((g for g in reversed(guides) if any(k in g for k in ks)), None)
    ge = stated("eps_guide", "eps_growth")
    gr = stated("rev_guide_usd_b", "rev_guide_pct")
    grw = stated("rev_words")
    if grw and gr and grw["published"] < gr["published"]:
        grw = None                                     # a later numeric guide replaces words about an earlier one
    if ge and "eps_guide" in ge:                       # a dollar level or range: its midpoint
        eps_now = round(sum(ge["eps_guide"]) / 2, 3)
        eps_fig = f"${eps_rng(*ge['eps_guide'])}"
        eps_label = f"{fy_e} EPS, guide midpoint" + (f" ({ge['eps_guide_note']})" if ge.get("eps_guide_note") else "")
    elif ge:                                           # growth on its stated base (the last full year unless the guide names another)
        base = ge.get("eps_growth_base", eps_hist[cur_fy - 1])
        base_s = ge.get("eps_growth_base_note", f"FY{(cur_fy - 1) % 100:02d}'s ${money(base)}")
        mid = sum(ge["eps_growth"]) / 2
        eps_now = round(base * (1 + mid / 100), 2)
        eps_fig = f"{pct_range(*ge['eps_growth'])} on {base_s}"
        eps_label = f"{fy_e} EPS, {base_s} {mid:+g}%, the midpoint of the {ge['doc']}'s profit per share growth guide"
    else:                                              # no numeric EPS guide: the last full year's EPS stands (rollover rule)
        eps_now = eps_hist[last_fy]
        eps_fig = None
        eps_label = (f"{fy_e}: the {w['doc']} withdrew the outlook ('{w['withdrawn_quote']}'), FY{last_fy % 100:02d}'s "
                     f"${money(eps_now)} stands" if w else
                     f"{fy_e}: no numeric profit per share guide yet, FY{last_fy % 100:02d}'s ${money(eps_now)} stands")
    if gr and "rev_guide_usd_b" in gr:                 # a dollar level or range, read against the last full year (the PFE rule)
        fwd = [round((v / last_rev - 1) * 100, 1) for v in gr["rev_guide_usd_b"]]
        rev_fig = usd_rng(*gr["rev_guide_usd_b"])
        fwd_kind = f"fiscal-year sales and revenues guide {rev_fig} on {fy_prev_s}'s ${last_rev:.3f}B (no next-quarter guide)"
        fy_rev_b, fy_rev_label = sum(gr["rev_guide_usd_b"]) / 2, f"{fy_now} sales and revenues guide midpoint"
    elif gr:                                           # growth as stated, on its stated base (the last full year unless named)
        base_b = gr.get("rev_growth_base_b", last_rev)
        fwd = [round((base_b * (1 + v / 100) / last_rev - 1) * 100, 1) for v in gr["rev_guide_pct"]]
        rev_fig = f"{pct_range(*gr['rev_guide_pct'])}" + (f" on {gr['rev_growth_base_note']}" if gr.get("rev_growth_base_note") else "")
        fwd_kind = f"fiscal-year sales and revenues guide {rev_fig} as stated (no next-quarter guide)"
        fy_rev_b, fy_rev_label = last_rev * (1 + sum(fwd) / 2 / 100), f"{fy_now} sales and revenues guide midpoint, on {fy_prev_s}"
    else:                                              # no revenue guide in numbers: the latest quarter's growth as reported
        fwd = [latest["sales_pct"]] * 2
        rev_fig = None
        fwd_kind = f"no sales and revenues guide in numbers: {latest['quarter']} growth as reported"
        fy_rev_b = last_rev * (1 + latest["sales_pct"] / 100)
        fy_rev_label = f"no {fy_now} sales and revenues guide in numbers, {latest['quarter']} growth, applied to the year"
    if gr:
        fwd_label, fwd_short, fwd_period = f"{fy_now} sales and revenues guide", f"{fy_now} guide", fy_now
    else:
        fwd_label = f"no {fy_now} sales and revenues guide in numbers, {latest['quarter']} growth"
        fwd_short, fwd_period = f"{latest['quarter'][:2]} sales and revenues", latest["quarter"]
    if guides:
        bits = ([f"sales and revenues {rev_fig}"] if gr else []) + \
               ([f"'{grw['rev_words']}' (words or a one-sided bound: no field)"] if grw else []) + \
               ([f"profit per share {eps_fig}" + (f" ({ge['eps_guide_note']})" if ge.get("eps_guide_note") else "")] if ge else
                ["no profit per share guide in numbers"]) + \
               ([f"withdrawn by the {w['doc']}: '{w['withdrawn_quote']}'"] if w else []) + \
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

    # ── era-dependent text, from facts only: no disruption theme is live for Caterpillar on any date of 2008-2009 ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
    key_tail = ("The 10-K ties demand to the energy and mining industries and to infrastructure,\n"
                "  housing and commercial construction; dealer inventory changes move company sales either way.")
    theme_summary = "no disruption theme has dated evidence"
    why = h["why"]
    # ENERGY_TRANSITION is live from 2015-12-12 and scoped to oil, gas and coal reserves and refining, which a maker of construction and
    # mining equipment, engines and turbines does not hold (the BKR reading; retro/README.md, "CAT 2014-2017"): from its live date the
    # texts say so, and the 10-Ks' carbon-emissions and climate-change wording stays in the "why" (the PEP obesity rule). From the FY2013
    # vintage the "why" ends with a clause that follows the theme's status on AS_OF ('why_theme_tail', naming the 10-K's wording); the
    # earlier vintages keep their text and every earlier date precedes the live date, so those dates rebuild byte-identical
    et = retro_tool.load_taxonomy()["themes"]["ENERGY_TRANSITION"]
    et_live = et["live_from"] <= as_of
    maker = "a maker of construction and mining equipment, engines and turbines"
    if et_live:
        sig_name = "Disruption theme: none in scope"
        trigger = "No live disruption theme covers construction and mining equipment, engines and turbines"
        theme_summary = (f"ENERGY_TRANSITION is live from {et['live_from']} but scoped to oil, gas and coal reserves and refining; no theme "
                         "in scope has dated evidence")
    # EV is live from 2020-01-01 (an approximate date) and scoped to battery-electric vehicles displacing ICE powertrains, auto parts
    # suppliers and fuel retail; Caterpillar's machines, off-highway engines and turbines are not road vehicles and its 10-Ks name no
    # electrification risk, so it is read as out of scope too (retro/README.md, "CAT 2018-2022"; text only, and every earlier date
    # precedes its live date)
    ev = retro_tool.load_taxonomy()["themes"]["EV"]
    ev_live = ev["live_from"] <= as_of
    if ev_live:
        theme_summary = (f"ENERGY_TRANSITION (live from {et['live_from']}) and EV (live from {ev['live_from']}) are scoped to oil, gas "
                         "and coal reserves and refining and to battery-electric vehicles; no theme in scope has dated evidence")
    if h.get("why_theme_tail"):
        why += (f"; ENERGY_TRANSITION (live from {et['live_from']}) is scoped to oil, gas and coal reserves and refining, which {maker} "
                f"does not hold, and EV (live from {ev['live_from']}) to battery-electric vehicles displacing ICE powertrains, auto parts "
                f"suppliers and fuel retail, which its machines, off-highway engines and turbines are not, so {h['why_theme_tail']} "
                "stays here" if ev_live else
                f"; ENERGY_TRANSITION is live from {et['live_from']} but scoped to oil, gas and coal reserves and refining, which {maker} "
                f"does not hold, so {h['why_theme_tail']} stays here" if et_live else
                f"; no disruption theme is live for {maker}, so {h['why_theme_tail']} stays here")
    cat3 = (f"(3) {fy_now} profit per share guide {eps_fig} ({ge['doc']}): the company's own read of the year" if ge else
            f"(3) A {fy_now} profit per share guide in numbers — withdrawn by the {w['doc']}" if w else
            f"(3) A {fy_now} profit per share guide in numbers — none yet")
    cat4 = (f"(4) {fy_now} sales and revenues guide {rev_fig} ({gr['doc']}): volume, price and currency in one number" if gr else
            f"(4) A {fy_now} sales and revenues guide in numbers — none yet")

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
           + ([dividend_src] if dividend_src else []) + split_ids + [e["id"] for e in events])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "W0", "published": as_of, "title": "Yahoo Finance daily prices, CAT and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/CAT/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "mach_pct", "eng_pct", "op_margin", "op_margin_bp", "eps_q",
                   "eps_q_prior", "eps_pct")
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    r = latest["raw"]
    if "ci_m" in r:        # the 2011 segments read as the successors of the Machinery and Engines lines
        e_name, e, e0 = (("Energy & Transportation", r["et_m"], r["et_prior_m"]) if "et_m" in r else
                         ("Power Systems", r["ps_m"], r["ps_prior_m"]))
        volumes = (f"Machinery (Construction Industries ${r['ci_m']:,}M and Resource Industries ${r['ri_m']:,}M against "
                   f"${r['ci_prior_m']:,}M and ${r['ri_prior_m']:,}M a year earlier, {latest['mach_pct']:+.1f}%), Engines ({e_name} "
                   f"${e:,}M against ${e0:,}M, {latest['eng_pct']:+.1f}%), as the release's sales and revenues by "
                   "segment show them" + (f"; {latest['note']}" if latest.get("note") else ""))
    else:
        volumes = (f"Machinery sales ${r['mach_m']:,}M against ${r['mach_prior_m']:,}M a year earlier ({latest['mach_pct']:+.1f}%), "
                   f"Engines ${r['eng_m']:,}M against ${r['eng_prior_m']:,}M ({latest['eng_pct']:+.1f}%), as the release's sales table "
                   "shows them" + (f"; {latest['note']}" if latest.get("note") else ""))
    R = repr
    pp = lambda x: "n/r" if x is None else f"{x:+.1f}%"    # a full-year line the Q4 release does not report (FY2012's segments)
    head = f'''#!/usr/bin/env python3
"""
CAT Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: CAT)  ·  {h["business_line"]}
Generated by retro/build_cat.py from retro/facts/CAT.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "CAT"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); machinery and engines signals")
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
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}{("; " + h["split_note"]) if h.get("split_note") else ""}
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # sales and revenues, USD bn
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
PREV_MACH       = {R(prev)}
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
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} sales and revenues {h['prev_fy_sales_growth']:+.1f}%, Machinery {pp(h['prev_fy_mach_pct'])}, Engines {pp(h['prev_fy_eng_pct'])}; {latest['quarter'].split()[0]} operating margin {latest['op_margin']:.2f}% ({latest['op_margin_bp']:+.1f}bp)")}
BALANCE_TEXT    = {R(f"{h['cash_label']} year-end cash and short-term investments ${h['cash_b']:.3f}B, {h['cash_label']} operating cash flow ${h['ocf_b']:.3f}B, dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/CAT)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("CAT"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<34}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
