#!/usr/bin/env python3
"""
Build LLY retrospective models from the dated fact sheet (retro/facts/LLY.json).

The LLY sibling of build_bmy.py: the same frozen rules (retro method r2), the same weekly dates and the same market statistics,
with pharmaceutical signals (retro/templates/lly_engine.py.tmpl, the BMY engine with Eli Lilly's own rule-T thresholds; a figure no
filing public on AS_OF states scores BASE and prints "n/r"). For each as-of date the builder
  1. selects only the history vintage, prints, guides and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, as traded (Yahoo's last split is 1997-10-16, before every
     P/E window here, so the close is the price as traded),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Eli Lilly's fiscal year is the calendar year. EPS is GAAP diluted EPS from continuing operations before extraordinary items and accounting
changes: the company's adjusted and pro forma figures also remove in-process research and development, which recurs, and add acquisitions
as if completed earlier, so they are shown and never used (the NKE FY2007, PFE and BMY rule). Each release guides the fiscal year: reported
and adjusted EPS as ranges in numbers, revenue growth in words. The method r2 inputs map as follows (retro/README.md, "LLY"):
  - current-FY EPS: the fiscal-year reported EPS guide midpoint; a range whose midpoint is a loss has no P/E (the r2 loss rule), so it is
    read as no numeric guide (the 8-K of 2008-12-11, FY2008 after the ImClone charge); with no usable guide the last full year's EPS
    stands (the rollover rule),
  - forward revenue growth: no next-quarter guide and no fiscal-year revenue guide in numbers (words are not figures), so the latest
    quarter's sales growth excluding foreign exchange, the release's growth less the exchange-rate points it states (the NKE, MSFT and
    BMY rule),
  - guided margin step: none (the gross-margin and expense guides are words); the margin signal takes the latest quarter's pre-tax
    margin change.
Company-wide U.S. and outside-U.S. sales growth is as each filing states it: in the release from Q4 2008, in the 10-Q for Q2 2007 to Q3
2008 ('geo_later': from the 10-Q's own date, the NKE futures and PEP servings rule), in no filing for Q4 2007 (the slot stays empty, the
AAPL Mac-unit rule). A year whose reported EPS is a loss or under half the EPS without its listed items, with no figure excluding only
one-offs, leaves the EPS history but stays reported ('eps_excluded' on a vintage, an 'excluded_note' and no EPS on a Q4 print's full-year
actuals: FY2008; the NKE FY2018, XOM FY2020 and BMY 2015 encoding): its own days leave the P/E window, and the current year is the one
after the latest reported year.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. The earnings 8-Ks of 2008-2009 were accepted before the open or during the session on the release
day, none on a week's last trading day.

Output goes to staging/retrospective/LLY until the series is added to the archive (--out archive/retrospective/LLY).

Usage
  python3 retro/build_lly.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_lly.py --weekly 2009-01-05 2009-12-31
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/LLY/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "LLY.json")
ENGINE = os.path.join(HERE, "templates", "lly_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "LLY")
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"us": (-31, -11, 8, 25), "intl": (-7, 1, 9, 19), "sales": (-16, -4, 8, 16),
                     "gross_margin": (-450, -200, 50, 250), "pretax_margin": (-1400, -750, -90, 590)}
RULE_T_KEYS = {"us": (1, False), "intl": (1, False), "sales": (1, False), "gross_margin": (10, False),
               "pretax_margin": (10, False)}           # (rounding unit, lower is better)


def fiscal_year_end(n):
    """Eli Lilly's fiscal year n is the calendar year n."""
    return dt.date(n, 12, 31)


def fiscal_year(day):
    return dt.date.fromisoformat(day).year


def eps_rng(lo, hi):
    """an EPS range: '3.80-3.95'; a loss in parentheses: '(2.06)-(1.56)'"""
    m = lambda v: f"({money(-v)})" if v < 0 else money(v)
    return m(lo) if lo == hi else f"{m(lo)}-{m(hi)}"


def usd_rng(lo, hi):
    """a dollar revenue guide in billions: '$21.8-22.8B' (the BMY form)"""
    b = lambda v: f"{v:.1f}" if round(v, 1) == v else f"{v:.2f}"
    return f"about ${b(lo)}B" if lo == hi else f"${b(lo)}-{b(hi)}B"


def rule_t_value(k, r):
    """One annual rule-T value from its raw figures ($ millions)."""
    if k == "us":
        return round((r["us_m"][1] / r["us_m"][0] - 1) * 100, 2)
    if k == "intl":
        (u0, u1), (t0, t1) = r["us_m"], r["total_m"]
        return round(((t1 - u1) / (t0 - u0) - 1) * 100, 2)
    if k == "sales":
        return round((r["revenues_m"][1] / r["revenues_m"][0] - 1) * 100, 2)
    if k == "gross_margin":
        (a0, a1), (c0, c1) = r["revenues_m"], r["cost_of_sales_m"]
        return round(((a1 - c1) / a1 - (a0 - c0) / a0) * 10000, 1)
    (a0, a1), (p0, p1) = r["revenues_m"], r["pretax_m"]
    return round((p1 / a1 - p0 / a0) * 10000, 1)


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
    m, m0 = (r["rev_m"] - r["cos_m"]) / r["rev_m"] * 100, (r["rev_prior_m"] - r["cos_prior_m"]) / r["rev_prior_m"] * 100
    t, t0 = r["pretax_m"] / r["rev_m"] * 100, r["pretax_prior_m"] / r["rev_prior_m"] * 100
    want = {"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": round((r["rev_m"] / r["rev_prior_m"] - 1) * 100, 1),
            "gross_margin": round(m, 2), "gross_margin_bp": round((m - m0) * 100, 1), "pretax_margin": round(t, 2),
            "pretax_margin_bp": round((t - t0) * 100, 1), "diluted_shares_m": float(r["diluted_shares_m"])}
    for k, v in want.items():
        assert p[k] == v or abs(p[k] - v) < 1e-9, (p["quarter"], k, p[k], v)
    for g in [p] + ([p["geo_later"]] if p.get("geo_later") else []):       # U.S. plus outside the U.S. add to the quarter's sales
        if g.get("us_b") is not None:
            assert abs(g["us_b"] + g["intl_b"] - r["rev_m"] / 1000) < 0.0015, (p["quarter"], "U.S. + outside the U.S.")
    assert not (p.get("us_pct") is not None and p.get("geo_later")), (p["quarter"], "one source for the U.S. split")


def geo(p, as_of):
    """A print's company-wide U.S. and outside-U.S. growth as public on AS_OF: (us_pct, intl_pct, note, source id or None)."""
    if p.get("us_pct") is not None:
        return p["us_pct"], p["intl_pct"], p["geo_note"], None
    gl = p.get("geo_later")
    if gl and gl["published"] <= as_of:
        return gl["us_pct"], gl["intl_pct"], gl["note"], gl["source"]
    # the same words whether or not a later filing states the split: nothing about a filing after AS_OF may show (the firewall rule)
    return (None, None, f"the {p['quarter']} release gives no company-wide U.S. and outside-U.S. split, and no filing public on AS_OF "
                        "states it (n/r)", None)


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    # every price of the window on the AS_OF share basis: Yahoo's split-adjusted series times its factors after AS_OF (none after 1997)
    chart = retro_tool.chart("LLY")
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    # no split restates a per-share fact of the fact sheet (every history year comes from a filing after the 1997 split); a split record
    # would have to sit on a split date of the price data, and on_basis applies it only from its effective date
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat()
                    for v in chart.get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo_splits for s in facts.get("splits", [])), "a split's effective date must match the price data"
    assert not facts.get("distributions"), "a distribution needs the 'distributions' encoding first (the BMY and MAR rule)"
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        check_print(p)
    # on_basis (the shared split helper) divides every Q4 print's full-year EPS; an excluded year has none, so a NaN stands in for it
    # there and None comes back after (the NKE, XOM, PFE and BMY encoding; LLY has no split after 1997)
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
    # a year excluded from the EPS history ('eps_excluded': FY2008, a loss with no published figure excluding only one-offs) is still
    # reported (the NKE FY2018, XOM FY2020 and BMY 2015 rule)
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
    # prints published by AS_OF that report a fiscal year after the history (a Q4 print reports the year just ended, so it stays in
    # scope after the 10-K that follows it)
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    prints = [p for p in facts["prints"] if p["published"] <= as_of and guide_fy(p) >= first_fy]
    # no disruption theme in taxonomy_eras.json is live for a pharmaceutical company in 2008-2009 (GLP1, from 2023-08-08, is scoped
    # to snacks, beverages and devices; OFFSHORE to IT services); the builder refuses events until a theme encoding is decided
    events = [e for e in facts["events"] if e["published"] <= as_of]
    if events:
        sys.exit(f"{as_of}: the LLY builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
    if [c for c in facts.get("company_names", []) if c["published"] <= as_of]:
        sys.exit(f"{as_of}: the LLY builder has no encoding for a change of company name; decide one first")
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is public yet")
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage
    h = {**h, "extended": ""}
    for p in prints:
        a = p.get("fy_actual")
        if a and a["fy"] not in reported(h):                        # the 10-K vintage, once out, wins
            y = str(a["fy"])
            if a["eps_normalized"] is None:           # an excluded year: reported, but out of the EPS history
                h.update(eps_excluded={**h.get("eps_excluded", {}), y: a["excluded_note"]})
            h.update(fy_label=a["fy_label"],
                     eps_normalized={**h["eps_normalized"], **({y: a["eps_normalized"]} if a["eps_normalized"] is not None else {})},
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]},
                     diluted_shares_m={**h["diluted_shares_m"], y: a["diluted_shares_m"]},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_pretax_margin=a["pretax_margin"], prev_fy_pretax_margin_note=a["pretax_margin_note"],
                     prev_fy_gross_margin=a["gross_margin"], prev_fy_sales_growth=a["sales_growth"],
                     prev_fy_us_pct=a["us_pct"], prev_fy_intl_pct=a["intl_pct"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})',
                     **({"revenue_label": a["revenue_label"]} if a.get("revenue_label") else {}))
            if a.get("restates_revenue"):     # (LLY 2010-2013) the same release prints the year before on a revised basis (FY2008
                                              # under EITF 07-1 in the Q4 2009 release): the history takes it until the 10-K (the JPM rule)
                h.update(revenue_usd_b={**h["revenue_usd_b"], **a["restates_revenue"]},
                         extended=f'{h["extended"]}; {a["restates_revenue_note"]}')
    latest = prints[-1]
    # the previous quarter is the print published just before the latest one (in or out of the history's scope)
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    i = public.index(latest)
    assert i > 0, (as_of, "the fact sheet needs the print before the latest one")
    us_now, intl_now, geo_note, geo_src = geo(latest, as_of)
    prev = (geo(public[i - 1], as_of)[0], public[i - 1]["quarter"])
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
    ge, ga, gw, gr = stated("eps_guide"), stated("eps_adj"), stated("rev_words"), stated("rev_guide_usd_b")
    loss_guide = bool(ge) and sum(ge["eps_guide"]) / 2 <= 0
    if ge and not loss_guide:
        eps_now = round(sum(ge["eps_guide"]) / 2, 3)
        eps_label = f"{fy_e} reported EPS, guide midpoint"
    else:   # no numeric reported EPS guide, or a guided loss (no P/E, the r2 loss rule): the last full year's EPS stands (rollover rule)
        eps_now = eps_hist[last_fy]
        why = (f"the reported EPS guide (${eps_rng(*ge['eps_guide'])}, {ge['doc']}) is a loss, which has no P/E" if loss_guide
               else "no numeric reported EPS guide yet")
        eps_label = (f"{fy_e}: {why}, FY{last_fy % 100:02d}'s ${money(eps_now)} stands" +
                     "".join(f" (FY{y % 100:02d} is excluded: {excluded[y]})" for y in range(last_fy + 1, cur_fy)))
    noun = "total revenue" if latest["fy"] >= 2009 else "net sales"
    fy_prev_s = f"FY{max(rev) % 100:02d}"
    if gr and not (gw and gw["published"] > gr["published"]):
        # (LLY 2010-2013) from the FY2012 guide (the 8-K of 2012-01-05) revenue is guided in dollars: the range read as growth on the
        # last full year's revenue in the history (the PFE, LOW and BMY dollar-level rule); no next-quarter guide
        fwd = [round((v / last_rev - 1) * 100, 1) for v in gr["rev_guide_usd_b"]]
        fwd_label, fwd_short, fwd_period = f"{fy_now} revenue guide", f"{fy_now} guide", fy_now
        fwd_kind = (f"fiscal-year {gr['rev_label']} guide {usd_rng(*gr['rev_guide_usd_b'])} on {fy_prev_s}'s "
                    f"${last_rev:.3f}B (no next-quarter guide)")
        fy_rev_b, fy_rev_label = sum(gr["rev_guide_usd_b"]) / 2, f"{fy_now} revenue guide midpoint"
    else:
        # no next-quarter guide and no revenue guide in numbers (each release states revenue growth in words only): the latest
        # quarter's sales growth excluding foreign exchange, the release's growth less the exchange-rate points it states (the NKE,
        # MSFT and BMY rule)
        gr = None
        fwd = [latest["lc_pct"]] * 2
        q2 = latest["quarter"][:2]
        fwd_label = f"no {fy_now} revenue guide in numbers, {latest['quarter']} {noun} growth ex-FX"
        fwd_short, fwd_period = f"{q2} sales ex-FX", latest["quarter"]
        fwd_kind = f"no revenue guide in numbers: {latest['quarter']} {noun} growth excluding foreign exchange ({latest['lc_note']})"
        fy_rev_b = last_rev * (1 + latest["lc_pct"] / 100)
        fy_rev_label = f"{latest['quarter']} {noun} growth ex-FX, applied to the year"
    if guides:
        bits = ([f"reported EPS ${eps_rng(*ge['eps_guide'])}" + (" (a loss: no P/E, so not used)" if loss_guide else "")]
                if ge else ["no reported EPS range in numbers"]) + \
               ([f"the company's adjusted EPS ${eps_rng(*ga['eps_adj'])} "
                 f"({ga.get('adj_why', 'shown only: it also removes in-process research and development, which recurs')})"] if ga else []) + \
               ([f"{gr['rev_label']} {usd_rng(*gr['rev_guide_usd_b'])} ({pct_range(*fwd)} on {fy_prev_s}'s ${last_rev:.2f}B)"]
                if gr else []) + \
               ([f"revenue in words only: '{gw['rev_words']}'"] if gw and not gr else []) + \
               ([g["note"] for g in guides[-1:] if g.get("note")])
        guide_text = f"{fy_now} guide ({', '.join(dict.fromkeys(g['doc'] for g in guides))}): " + "; ".join(bits)
    else:
        guide_text = f"{fy_now}: no guide yet"
    margin_guided = False                          # no pre-tax margin guide in numbers: no guided step
    fy_margin_base = h["prev_fy_pretax_margin"]

    # ── dividend: the latest declared rate (each rate is first stated in a 10-K, so it rides on the vintage) ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts["dividends"] if d["published"] <= as_of]
    divs.append((h["published"], h["dividend_annual"], h["dividend_note"], None))
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

    # ── era-dependent text, from facts only: no disruption theme has dated evidence on AS_OF ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
    key_tail = ("Patent expirations drive the decline, by the company's own account; the bear needs\n"
                "  new products and cost cuts to stop covering them.")
    theme_summary = "no disruption theme has dated evidence"
    cat3 = (f"(3) {fy_now} reported EPS guide ${eps_rng(*ge['eps_guide'])} ({ge['doc']})" + (": a loss, no P/E" if loss_guide else "")
            if ge else f"(3) A numeric {fy_now} reported EPS guide — none yet")
    cat4 = (f"(4) Pre-tax margin — {latest['pretax_margin']:.2f}% in {latest['quarter']} ({latest['pretax_margin_bp']:+.1f}bp): "
            "where in-process R&D, restructuring and litigation charges land")

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
           + ([dividend_src] if dividend_src else []) + ([geo_src] if geo_src else []) + split_ids)
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "W0", "published": as_of, "title": "Yahoo Finance daily prices, LLY and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/LLY/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "lc_pct", "us_pct", "intl_pct", "gross_margin", "gross_margin_bp",
                   "pretax_margin", "pretax_margin_bp", "eps_q", "eps_q_prior")
    latest_view = {**latest, "us_pct": us_now, "intl_pct": intl_now}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    pv = lambda v, u="%": "n/r" if v is None else f"{v:+.1f}{u}"
    volumes = (f"company-wide U.S. and outside-U.S. sales: {geo_note}; {noun} growth ex-FX {latest['lc_pct']:+.0f}% ({latest['lc_note']})"
               + (f"; {latest['eps_note']}" if latest.get("eps_note") else "")
               + (f"; {latest['note']}" if latest.get("note") else ""))
    lead_name, lead_v = groups[0][0], groups[0][1]       # the largest product class: Neurosciences (Neuroscience from FY2009)
    # (LLY 2010-2013) total revenue from the FY2009 10-K and the Q4 2009 release ('revenue_label'); the product classes add to net
    # product sales in the FY2009 10-K and to revenue from the FY2010 10-K
    sw = "total revenue" if h.get("revenue_label") else "net sales"
    gw_basis = "the product classes" if h.get("revenue_label") else "net sales"
    lead = lead_v / sum(v for _, v, _ in groups) * 100
    R = repr
    head = f'''#!/usr/bin/env python3
"""
LLY Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: LLY)  ·  {h["business_line"]}
Generated by retro/build_lly.py from retro/facts/LLY.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "LLY"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); pharmaceutical signals")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts above.
PIT_PROFILE = {{
    "kind": "DURABLE",
    "risk": 2,
    "why": {R(h["why"])},
    "theme_watch": {R(watch)},
    "evidence": [],
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
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # {h.get("revenue_label", "net sales")}, USD bn
SHARES_HIST   = {R({y: round(v, 3) for y, v in shares.items()})}   # diluted, millions
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_pretax_margin"]}   # pre-tax margin, {h["prev_fy_pretax_margin_note"]}
CHECK_PRETAX_MARGIN = {h["prev_fy_pretax_margin"]}   # the same, for the EPS check
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({k: latest_view.get(k) for k in latest_keys})}
PREV_US         = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # {fwd_kind}
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no pre-tax margin guide in numbers, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {fy_rev_b:.2f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R(groups)}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} {sw} {h['prev_fy_sales_growth']:+.1f}% (U.S. {pv(h['prev_fy_us_pct'])}, outside the U.S. {pv(h['prev_fy_intl_pct'])}), {lead_name} {lead:.0f}% of {gw_basis}; {latest['quarter'].split()[0]} gross margin {latest['gross_margin']:.2f}% ({latest['gross_margin_bp']:+.1f}bp)")}
BALANCE_TEXT    = {R(f"{h['fcf_label']} year-end cash and short-term investments ${h['cash_b']:.2f}B, {h['fcf_label']} free cash flow ${h['fcf_b']:.2f}B, dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/LLY)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("LLY"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<34}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
