#!/usr/bin/env python3
"""
Build SPGI retrospective models from the dated fact sheet (retro/facts/SPGI.json).

The SPGI sibling of build_cat.py: the same frozen rules (retro method r2), the same weekly dates and the same market statistics,
with ratings, education and information signals (retro/templates/spgi_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints, guides and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, as traded (Yahoo's split-adjusted series times its
     factors after AS_OF: for 2008-2009 only the 1057:1000 factor of 2026-07-01, Yahoo's booking of the Mobility Global
     distribution, so the product is the close as traded; the 2-for-1 split of 2005-05-18 restates the per-share facts published
     before it through the fact sheet's 'splits', the 1999 split precedes every one),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

The company of 2008-2009 is The McGraw-Hill Companies, Inc., listed on the NYSE as MHP. SPGI is the series key (TICKER, the folder,
the index) and the symbol under which Yahoo serves the price history (S&P Global's ticker from 2016); every printed line names the
listing of the date (LISTED_SYMBOL = "MHP"; the BKR encoding; retro/README.md, "SPGI"). A change of name ('company_names', from
its publication until a later vintage carries it) and of listing ('listings', from its effective date once published) apply from
their dates: McGraw Hill Financial, Inc. from the 8-K of 2013-05-06, NYSE: MHFI from 2013-05-14 (retro/README.md, "SPGI 2010-2013").

McGraw-Hill's fiscal year is the calendar year. EPS is diluted EPS from continuing operations before the extraordinary item and the
cumulative adjustment, as each 10-K's Eleven-Year Financial Review reports it: no filing publishes a figure excluding only one-offs
on that basis (the releases list one-offs' per-share effects without a figure excluding them; the FY1998-FY1999 10-Ks' figures
excluding one-time items predate the 2003 discontinued-operations restatement, the UNP trucking rule), so no year is adjusted and
none is excluded. The releases guide the fiscal year only, never a quarter: diluted EPS as a range or as growth on the last full
year (on the basis the guide states: 2008 growth on 2007 without the two items the guide excludes), consolidated revenue as growth
(2009 only), and segment revenue and margin ranges (components: no total is derived, the MSFT segment rule). The method r2 inputs
map as follows (retro/README.md, "SPGI"):
  - current-FY EPS: the fiscal-year EPS guide midpoint (a growth guide on its stated base, at its midpoint); words or a one-sided
    bound ('double-digit earnings growth in 2007') give no field, so the last full year's EPS stands (the rollover rule),
  - forward revenue growth: no next-quarter guide, so the fiscal-year consolidated revenue guide as stated; none in numbers (2007,
    2008: segments only), so the latest quarter's revenue growth as reported (the CAT, GOOG and JPM rule),
  - guided margin step: none (the margin guides are segments'); the margin signal takes the latest quarter's change.
Quarter values in the signals are as reported (the CAT reading): the releases' 'as adjusted' segment profit, which excludes
restructuring, is in the print's note only.

From 2010 (retro/README.md, "SPGI 2010-2013"): each year's EPS is from the latest filing that reports it, at the company's figure
excluding only one-offs where a release on the same basis publishes it (2009-2012); a release that republishes an earlier year on a
new basis restates it until the next 10-K ('restates', the CAT and PFE encoding, EPS only); revenue guides are words (no field), so
BASE is the latest quarter's revenue growth as reported; the Financial Services line of 2011 on is the release's Standard & Poor's
(S&P Ratings) and McGraw-Hill Financial (S&P Capital IQ / S&P Indices, then S&P Capital IQ and S&P Dow Jones Indices) less the
royalty elimination ('fs_parts'), the old segment's scope; the third segment is the release's ('im_label'); McGraw-Hill Education
is not reported from the Q4 2012 release (a discontinued operation): its signal is None, scores BASE and prints n/r, through
retro/templates/spgi2_engine.py.tmpl, the None-tolerant copy of the engine used whenever the latest release's segment table is
not the 2007-2009 one (the BKR bkr3 encoding).

From 2014 (retro/README.md, "SPGI 2014-2017"): McGraw Hill Construction is discontinued from the Q3 2014 release, and the 8-K of
2014-11-05 that recasts FY2013 without it is a history vintage of its own (the MSFT recast rule); the company's figure excluding only
one-offs stands for 2013-2015 (FY2014 $3.88 against GAAP $(1.08)); from 2016 the adjusted figures and guides also remove deal-related
amortization, which recurs, so FY2016 is GAAP ($7.94) and the FY2016 guides feed nothing ('eps_guide_amort', the guide line only: FY15's
$4.53 stands), while the FY2017 GAAP ranges are the guide; FY2017's reported revenue 'unchanged from the prior year' is 0% (the RCL and
LOW rule), and its later words leave the range standing; the Financial Services line keeps the old scope from the release's rows
(Ratings, S&P Capital IQ / Market Intelligence, S&P Dow Jones Indices, less the royalty elimination; Market Intelligence from its own
row once it is inside Market and Commodities Intelligence); a year-ago loss measures EPS growth on its absolute value (the CAT rule);
S&P Global Inc. from the 8-K of 2016-04-29 (dated 2016-05-02) and NYSE: SPGI from the S-3 of 2016-06-29 (dated 2016-06-30).

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. Every earnings 8-K of 2007-2009 was accepted before the open (06:59-07:58 ET; the call at 8:30 a.m.).

Output goes to staging/retrospective/SPGI until the series is added to the archive (--out archive/retrospective/SPGI).

Usage
  python3 retro/build_spgi.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_spgi.py --weekly 2009-01-05 2009-12-31
  python3 retro/build_spgi.py --weekly 2010-01-04 2013-12-31
  python3 retro/build_spgi.py --weekly 2014-01-06 2017-12-31
  python3 retro/build_spgi.py 2008-01-25
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/SPGI/<AS_OF>
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

SYMBOL, LISTED = "SPGI", "MHP"
FACTS = os.path.join(HERE, "facts", "SPGI.json")
ENGINE = os.path.join(HERE, "templates", "spgi_engine.py.tmpl")
ENGINE2 = os.path.join(HERE, "templates", "spgi2_engine.py.tmpl")   # the latest release's segment table is not the 2007-2009 one
OUT = os.path.join(ROOT, "staging", "retrospective", "SPGI")
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"fs": (-7, 4, 14, 18), "mhe": (-16, -6, 5, 23), "sales": (1, 4, 7, 15), "eps": (-98, -43, 13, 53),
                     "op_margin": (-970, -440, 90, 460)}
RULE_T_KEYS = {"fs": (1, False), "mhe": (1, False), "sales": (1, False), "eps": (1, False),
               "op_margin": (10, False)}           # (rounding unit, lower is better)
GUIDE_KEYS = {"fy", "published", "source", "doc", "quotes", "words", "eps_guide", "eps_guide_note", "eps_growth", "eps_growth_base",
              "eps_growth_base_note", "rev_guide_pct", "seg_words", "rev_words", "note",
              "eps_guide_amort", "eps_guide_amort_note"}   # from 2016: an adjusted range that also removes recurring amortization (no field)
PRINT_TOL = {None: 2, "k": 2, "m1": 150, "m0": 1500}   # segment sums, $ thousands: the release's own rounding (thousands, $0.1M, $1M)
OLD_SEGMENTS = "Information & Media"                     # the third segment of the 2007-2009 tables (spgi_engine.py.tmpl)


def fiscal_year_end(n):
    """McGraw-Hill's fiscal year n is the calendar year n."""
    return dt.date(n, 12, 31)


def fiscal_year(day):
    return dt.date.fromisoformat(day).year


def eps_rng(lo, hi):
    """an EPS range: '2.65-2.75'"""
    return money(lo) if lo == hi else f"{money(lo)}-{money(hi)}"


def rule_t_value(k, r):
    """One annual rule-T value from its raw figures ($ thousands; EPS in dollars)."""
    if k == "eps":
        e0, e1 = r["eps"]
        return round((e1 / e0 - 1) * 100, 2)
    a0, a1 = r["revenue_k"]
    if k in ("fs", "mhe", "sales"):
        return round((a1 / a0 - 1) * 100, 2)
    o0, o1 = r["segop_k"]                               # segment operating profit on revenue
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


def check_print(p):
    """Re-derive a print's growth and margins from its raw published figures (they must match)."""
    r = p["raw"]
    tol = PRINT_TOL[r.get("units")]
    mhe, mhe0 = (r["mhe_k"], r["mhe_prior_k"]) if r["mhe_k"] is not None else (0, 0)   # None: not reported (discontinued)
    assert abs(r["fs_k"] + mhe + r["im_k"] - r["rev_k"]) <= tol, (p["quarter"], "segments sum to revenue")
    assert abs(r["fs_prior_k"] + mhe0 + r["im_prior_k"] - r["rev_prior_k"]) <= tol, (p["quarter"], "year-ago segments")
    if "fs_parts" in r:                                # the Financial Services line from the release's own rows
        for k, f in ((0, "fs_k"), (1, "fs_prior_k")):
            assert abs(sum(v[k] for v in r["fs_parts"].values()) - r[f]) <= 2, (p["quarter"], f, "Financial Services parts")
    o, o0 = r["segop_k"] / r["rev_k"] * 100, r["segop_prior_k"] / r["rev_prior_k"] * 100
    pct = lambda a, b: round((a / b - 1) * 100, 1)
    e1, e0q = p["eps_q"], p["eps_q_prior"]
    want = {"sales_b": round(r["rev_k"] / 1e6, 3), "sales_pct": pct(r["rev_k"], r["rev_prior_k"]),
            "fs_pct": pct(r["fs_k"], r["fs_prior_k"]),
            "mhe_pct": pct(r["mhe_k"], r["mhe_prior_k"]) if r["mhe_k"] is not None else None,
            "im_pct": pct(r["im_k"], r["im_prior_k"]),
            "op_margin": round(o, 2), "op_margin_bp": round((o - o0) * 100, 1),
            # growth on a year-ago loss is measured on its absolute value, so its direction stays right (the CAT rule; Q4 2015,
            # whose year-ago Q4 2014 carries the legal settlements); every other base is positive, where the two forms agree
            "eps_pct": round((e1 / e0q - 1) * 100, 1) if e0q > 0 else round((e1 - e0q) / abs(e0q) * 100, 1),
            "diluted_shares_m": r["diluted_shares_k"] / 1000}
    assert e0q != 0, (p["quarter"], "a zero year-ago EPS needs its encoding first")
    for k, v in want.items():
        assert p[k] == v or (v is not None and abs(p[k] - v) < 1e-9), (p["quarter"], k, p[k], v)


def build(as_of, facts, raw, spx, engines, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    # Yahoo books the 2026-07-01 Mobility Global distribution as a split: it is not one, so no date on or after it is built until
    # it is encoded as a distribution (the MAR, PFE and CMCSA 'distributions' rule; retro/README.md, "SPGI")
    for x in facts["distributions_later"]:
        if as_of >= x["effective"]:
            sys.exit(f"{as_of}: encode the {x['effective']} distribution first (the 'distributions' rule)")
    # every price of the window as traded: Yahoo's split-adjusted series times its factors after AS_OF (2026's 1.057)
    chart = retro_tool.chart(SYMBOL)
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    # a split record must sit on a split date of the price data; on_basis applies it from its effective date
    yahoo = {dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat():
             v["numerator"] / v["denominator"] for v in chart.get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo for s in facts.get("splits", [])), "a split's effective date must match the price data"
    assert all(yahoo.get(x["effective"]) == x["yahoo_factor"] for x in facts["distributions_later"]), "Yahoo's distribution factor"
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        check_print(p)
    for g in [g for g in facts["guides"] if g["published"] <= as_of]:   # a guide public on AS_OF: only fields with an encoding
        assert set(g) <= GUIDE_KEYS, (g["doc"], "a guide field the builder has no encoding for", set(g) - GUIDE_KEYS)
    if [d for d in facts["dividends"] if d["published"] <= as_of and "quarterly" not in d]:
        sys.exit(f"{as_of}: a dividend without a quarterly rate needs its encoding first")
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
    # no disruption theme in taxonomy_eras.json is live for a ratings, education and business information company in 2008-2013
    # (GENAI, whose scope names education content and professional information, from 2022-11-30; STREAMING, scoped to linear TV
    # networks, from 2015-08-04; OFFSHORE to IT services): the builder refuses events until a theme encoding is decided
    events = [e for e in facts["events"] if e["published"] <= as_of and (h["published"] <= e["published"] or "doc" not in e)]
    if events:
        sys.exit(f"{as_of}: the SPGI builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
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
                     prev_fy_sales_growth=a["sales_growth"], prev_fy_fs_pct=a["fs_pct"], prev_fy_mhe_pct=a["mhe_pct"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    # a release may republish an earlier year's company figure on a new basis ('restates': the Q4 2010 release's 2009 excluding
    # one-offs, the Q3 and Q4 2011 releases' 2010 without the Broadcasting Group, the Q4 2012 release's 2011 without McGraw-Hill
    # Education); each year comes from the latest filing that reports it, so the figure replaces the year from the print until a
    # 10-K vintage published after the print carries the year (the CAT and PFE encoding, EPS only; retro/README.md, "SPGI 2010-2013")
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
    prev = (public[i - 1]["fs_pct"], public[i - 1]["quarter"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    last_rev = rev[max(rev)]
    fy_prev_s = f"FY{max(rev) % 100:02d}"

    # ── guides for the current fiscal year, each field from the latest guide that states it (in either form, the WMT rule) ──
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    stated = lambda *ks: next((g for g in reversed(guides) if any(k in g for k in ks)), None)
    ge = stated("eps_guide", "eps_growth")
    gr = stated("rev_guide_pct")
    gw = stated("words")
    gs = stated("seg_words")
    grw = stated("rev_words")                          # revenue growth in words ('high single-digit'): no field
    if gw and ((ge and gw["published"] < ge["published"]) or (gr and gw["published"] < gr["published"])):
        gw = None                                      # a later numeric guide replaces words about an earlier one
    if ge and "eps_guide" in ge:                       # a dollar range: its midpoint
        eps_now = round(sum(ge["eps_guide"]) / 2, 3)
        eps_fig = f"${eps_rng(*ge['eps_guide'])}"
        eps_label = f"{fy_e} EPS, guide midpoint" + (f" ({ge['eps_guide_note']})" if ge.get("eps_guide_note") else "")
    elif ge:                                           # growth on its stated base (the last full year unless the guide names another)
        base = ge.get("eps_growth_base", eps_hist[cur_fy - 1])
        base_s = ge.get("eps_growth_base_note", f"FY{(cur_fy - 1) % 100:02d}'s ${money(base)}")
        mid = sum(ge["eps_growth"]) / 2
        eps_now = round(base * (1 + mid / 100), 2)
        eps_fig = f"{pct_range(*ge['eps_growth'])} on {base_s}"
        eps_label = f"{fy_e} EPS, {base_s} {mid:+g}%, the midpoint of the {ge['doc']}'s EPS growth guide"
    else:                                              # no numeric EPS guide: the last full year's EPS stands (rollover rule)
        eps_now = eps_hist[last_fy]
        eps_fig = None
        eps_label = f"{fy_e}: no numeric EPS guide yet, FY{last_fy % 100:02d}'s ${money(eps_now)} stands"
    # from 2016 the adjusted ranges also remove deal-related amortization, which recurs: not a figure excluding only one-offs (the
    # CMCSA, PFE and AVGO reading), so they feed nothing and are shown in the guide line only (retro/README.md, "SPGI 2014-2017")
    ga = stated("eps_guide_amort")
    amort_fig = f"${eps_rng(*ga['eps_guide_amort'])}" if ga else None
    if ga and not ge:
        eps_label = (f"{fy_e}: the EPS guide ({amort_fig}, {ga['doc']}) also removes recurring deal-related amortization (no "
                     f"field), FY{last_fy % 100:02d}'s ${money(eps_now)} stands")
    if gr:                                             # consolidated revenue growth as stated (no next-quarter guide)
        fwd = [float(v) for v in gr["rev_guide_pct"]]
        rev_fig = pct_range(*gr["rev_guide_pct"])
        fwd_kind = f"fiscal-year consolidated revenue guide {rev_fig} as stated (no next-quarter guide)"
        fy_rev_b, fy_rev_label = last_rev * (1 + sum(fwd) / 2 / 100), f"{fy_now} revenue guide midpoint, on {fy_prev_s}"
        fwd_label, fwd_short, fwd_period = f"{fy_now} revenue guide", f"{fy_now} guide", fy_now
    else:                                              # no consolidated revenue guide in numbers: the latest quarter's growth as reported
        fwd = [latest["sales_pct"]] * 2
        rev_fig = None
        fwd_kind = f"no consolidated revenue guide in numbers: {latest['quarter']} growth as reported"
        fy_rev_b = last_rev * (1 + latest["sales_pct"] / 100)
        fy_rev_label = f"no {fy_now} revenue guide in numbers, {latest['quarter']} growth, applied to the year"
        fwd_label = f"no {fy_now} revenue guide in numbers, {latest['quarter']} growth"
        fwd_short, fwd_period = f"{latest['quarter'][:2]} revenue", latest["quarter"]
    if guides:
        bits = ([f"revenue {rev_fig}"] if gr else []) + \
               ([f"'{gs['seg_words']}' (components: no total is derived)"] if gs and not gr else []) + \
               ([f"revenue growth in words, '{grw['rev_words']}' (no field)"] if grw and not gr else []) + \
               ([f"revenue growth in words since, '{grw['rev_words']}' ({grw['doc']}: the range stands)"]
                if grw and gr and grw["published"] > gr["published"] else []) + \
               ([f"EPS {eps_fig}" + (f" ({ge['eps_guide_note']})" if ge.get("eps_guide_note") else "")] if ge else
                [] if ga else ["no EPS guide in numbers"]) + \
               ([f"adjusted EPS {amort_fig} ({ga['eps_guide_amort_note']}: no field, amortization recurs)"] if ga else []) + \
               ([f"'{gw['words']}' (words or a one-sided bound: no field)"] if gw else []) + \
               [g["note"] for g in guides[-1:] if g.get("note")]
        guide_text = f"{fy_now} guide ({', '.join(dict.fromkeys(x['doc'] for x in guides))}): " + "; ".join(bits)
    else:
        guide_text = f"{fy_now}: no guide in numbers yet"
    margin_guided = False                          # no consolidated margin guide in numbers: no guided step
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

    # ── era-dependent text, from facts only: no disruption theme is live for McGraw-Hill on any date of 2008-2009 ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
    key_tail = h.get("key_tail", "The 10-K ties results to the volume of debt issued in the capital markets, to state\n"
                                 "  adoption opportunities and educational funding, and to advertising.")
    theme_summary = "no disruption theme has dated evidence"
    why = h["why"]
    cat3 = (f"(3) {fy_now} EPS guide {eps_fig} ({ge['doc']}): the company's own read of the year" if ge else
            f"(3) A {fy_now} EPS guide on the history's basis — none (the adjusted guide also removes deal-related amortization)"
            if ga else f"(3) A {fy_now} EPS guide in numbers — none yet")
    cat4_tail = h.get("cat4_tail", "issuance, adoptions and advertising in one number")
    cat4 = (f"(4) {fy_now} revenue guide {rev_fig} ({gr['doc']}): {cat4_tail}" if gr else
            f"(4) A {fy_now} consolidated revenue guide in numbers — none yet" +
            (" (revenue growth in words only)" if grw else " (segment ranges only)" if gs else ""))

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{latest['next_print'].split(' print')[0]} print)"
    # a print dated AS_OF meets AS_OF's close only if it was public before it: before the open or during the session
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        rt = same_day[-1].get("release_time", "")
        assert "before the open" in rt or "during the session" in rt, (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the close")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the close)"

    # a name changed since the vintage applies from its publication; a listing from its effective date, once published
    renames = [n for n in facts["company_names"] if h["published"] < n["published"] <= as_of]
    company = renames[-1]["name"] if renames else h["company"]
    moved = [x for x in facts.get("listings", []) if x["published"] <= as_of and x["effective"] <= as_of]
    exchange, listed = (moved[-1]["exchange"], moved[-1]["symbol"]) if moved else (h["exchange"], LISTED)
    groups = [tuple(g) for g in h["groups"]]
    ids = (list(h["sources"]) + [p["source"] for p in prints] + [g["source"] for g in guides]
           + ([dividend_src] if dividend_src else []) + split_ids + [e["id"] for e in events]
           + [n["source"] for n in renames] + [x["source"] for x in moved])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "W0", "published": as_of, "title": f"Yahoo Finance daily prices, {listed} and S&P 500, truncated at AS_OF",
                    "url": f"https://finance.yahoo.com/quote/{SYMBOL}/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "fs_pct", "mhe_pct", "im_pct", "op_margin", "op_margin_bp", "eps_q",
                   "eps_q_prior", "eps_pct")
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    r = latest["raw"]
    other = latest.get("im_label", OLD_SEGMENTS)
    mhe_text = (f"McGraw-Hill Education ${r['mhe_k'] / 1000:,.1f}M against ${r['mhe_prior_k'] / 1000:,.1f}M ({latest['mhe_pct']:+.1f}%)"
                if r["mhe_k"] is not None else "McGraw-Hill Education not reported")
    volumes = (f"Financial Services revenue ${r['fs_k'] / 1000:,.1f}M against ${r['fs_prior_k'] / 1000:,.1f}M a year earlier "
               f"({latest['fs_pct']:+.1f}%), {mhe_text}, {other} ${r['im_k'] / 1000:,.1f}M ({latest['im_pct']:+.1f}%), as the release's "
               "segment table shows them" + (f"; {latest['note']}" if latest.get("note") else ""))
    # the engine: the 2007-2009 segment table, else its None-tolerant copy (a segment not reported, the third segment renamed)
    engine2 = latest["mhe_pct"] is None or OLD_SEGMENTS not in other
    engine = engines[1] if engine2 else engines[0]
    fmt = lambda v: "n/r" if v is None else f"{v:+.1f}%"
    R = repr
    head = f'''#!/usr/bin/env python3
"""
{listed} Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: {listed})  ·  {h["business_line"]}
Generated by retro/build_spgi.py from retro/facts/SPGI.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "{SYMBOL}"   # series key
LISTED_SYMBOL = "{listed}"   # the listing on AS_OF
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); ratings, education and information signals")
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
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # revenue, USD bn
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
{f"OTHER_SEGMENT   = {R(other)}   # the release's third segment" + chr(10) if engine2 else ""}PREV_FS         = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # {fwd_kind}
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no consolidated margin guide in numbers, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {fy_rev_b:.2f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R(groups)}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenue {h['prev_fy_sales_growth']:+.1f}%, Financial Services {h['prev_fy_fs_pct']:+.1f}%, Education {fmt(h['prev_fy_mhe_pct'])}; {latest['quarter'].split()[0]} segment operating margin {latest['op_margin']:.2f}% ({latest['op_margin_bp']:+.1f}bp)")}
BALANCE_TEXT    = {R(f"{h['cash_label']} year-end cash and equivalents ${h['cash_b']:.3f}B, {h['cash_label']} operating cash flow ${h['ocf_b']:.3f}B, dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/SPGI)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    engines = []
    for path in (ENGINE, ENGINE2):
        with open(path, encoding="utf-8") as fh:
            engines.append(fh.read())
    raw, spx = load_series(SYMBOL), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engines, os.path.abspath(a.out))
        print(f"{d}  {tag:<34}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
