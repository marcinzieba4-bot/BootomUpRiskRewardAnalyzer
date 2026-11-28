#!/usr/bin/env python3
"""
Build TRGP retrospective models from the dated fact sheet (retro/facts/TRGP.json).

The TRGP sibling of build_lyb.py's new-listing builder: the same frozen rules (retro method r2), the same weekly dates and the same
market statistics, with midstream signals (retro/templates/trgp_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints, outlooks and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, from the listing (the listing rule of method r2),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Targa Resources Corp.'s common stock has been listed on the NYSE as TRGP since 2010-12-07 (FY2010 10-K, Item 5; before the IPO "No
public market currently exists for our common stock", the 424B1 of 2010-12-07), so no TRGP share traded in 2008-2009 and no date of
those years can be built (retro/README.md, "TRGP"). Targa Resources Partners LP (NYSE: NGLS), which TRC controls and consolidates, is
a separate listed partnership: its unit prices and per-unit earnings are never substituted. From the listing, 2010 is a loss per share
($(30.94), after the Series B and common-equivalent dividends of the pre-IPO recapitalization) and 2008-2009 have no EPS to common
shareholders, so the first full year of EPS is 2011, published in the Q4 2011 release (8-K accepted 2012-02-23 07:21 ET, before the
open): no date before the first weekly date after it, 2012-02-24, can be built, and the builder refuses them with that reason. 2010 is
excluded (a loss): its days leave the P/E window ("ex-FY10"). EPS is GAAP diluted EPS, each year from the latest filing that reports
it.

Targa guides no revenue, EPS or margin in numbers in any filing of 2011-2013 (the releases and the outlook 8-K of 2012-10-17 give the
Partnership's Adjusted EBITDA and distribution growth and TRC's dividend growth: display only), so:
  - current-FY EPS: the last full year's GAAP EPS stands (the PFE rule for a year with no reported-EPS guide),
  - BASE growth and the growth factor: the latest quarter's revenue growth as reported (the SO, UNP, KMI and LYB no-guide rule),
  - guided margin step: none; the margin signal uses the latest quarter's change.

Signals (each against the year-ago quarter as the release shows it): the Partnership's Natural Gas Gathering and Processing (Field plus
Coastal) and Logistics and Marketing (Logistics Assets plus Marketing and Distribution) segment operating margin growth (the two
divisions the 10-Ks report, segment operating margin being the measure management reviews), revenue growth, the operating margin change
and the pre-tax margin change, from TRC's consolidated statement of operations in the joint release.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it.

Output goes to staging/retrospective/TRGP until the series is added to the archive (--out archive/retrospective/TRGP).

Usage
  python3 retro/build_trgp.py --weekly 2012-02-20 2013-12-31     # 98 dates, 2012-02-24 .. 2013-12-31
  python3 retro/build_trgp.py 2012-02-24
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/TRGP/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "TRGP.json")
ENGINE = os.path.join(HERE, "templates", "trgp_engine.py.tmpl")
# (TRGP 2014-2017) the None-tolerant copy: TRC's own releases from Q1 2016 print no EPS, so a print whose 10-Q is not yet public shows
# its EPS as n/r (the BKR, SPGI, SCHW and LYB encoding: the earlier models keep the original engine byte for byte)
ENGINE2 = os.path.join(HERE, "templates", "trgp2_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "TRGP")
SYMBOL = "TRGP"
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"gp": (-115, -44, 26, 34), "lm": (-35, 5, 44, 93), "revenue": (-106, -43, 19, 28),
                     "op_margin": (-240, -120, 0, 190), "pretax_margin": (-150, -60, 30, 190)}
RULE_T_KEYS = {"gp": (1, False), "lm": (1, False), "revenue": (1, False), "op_margin": (10, False), "pretax_margin": (10, False)}
PRINT_KEYS = {"quarter", "fy", "q", "published", "source", "release", "release_time", "period_end", "raw", "sales_b", "sales_pct",
              "opm", "opm_bp", "ptm", "ptm_bp", "eps_q", "eps_q_prior", "diluted_shares_m", "gp_pct", "lm_pct", "seg_note",
              "sales_note", "margin_note", "eps_note", "cash_note", "next_print", "fy_actual", "restated"}
FY_KEYS = {"fy", "fy_label", "eps_normalized", "excluded_note", "revenue_usd_b", "diluted_shares_m", "normalization_note", "op_margin",
           "op_margin_note", "sales_growth", "check_pretax_margin", "check_pretax_note", "tax_rate", "tax_note", "one_off_test",
           "eps_gaap"}


def fiscal_year_end(n):
    """Targa Resources Corp.'s fiscal year n is the calendar year n."""
    return dt.date(n, 12, 31)


def fiscal_year(day):
    return dt.date.fromisoformat(day).year


def rule_t(rt, keys=RULE_T_KEYS):
    """Rule T thresholds from the annual values: XBULL best, BULL median, BASE worst, BEAR one median-to-worst step beyond
    the worst; rounded half up to whole percent and to 10 bp."""
    out = {}
    for k, (unit, lower) in keys.items():
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


def as_restated(p, as_of):
    """(TRGP 2014-2017) A print with its restatements applied, in order, once each is public (a quarter from the latest filing that
    reports it: the JPM and SCHW encoding): the revenues the 8-K of 2014-10-23 revises (Q1 and Q2 2014), and the EPS and diluted shares
    of TRC's own releases from Q1 2016, which print neither, from the 10-Q (Q4 2016: the FY2016 10-K's quarterly data)."""
    q = p
    for rs in p.get("restated", []):
        if rs["published"] <= as_of:
            q = {**q, **{k: v for k, v in rs.items() if k not in ("published", "source")}}
            q["extra_sources"] = list(q.get("extra_sources", [])) + [rs["source"]]
    return q


def check_print(p, as_of=None):
    """Re-derive a print's growth rates and margins from its raw published figures (they must match the fact sheet); a restated
    version once public, too."""
    assert set(p) <= PRINT_KEYS, (p["quarter"], sorted(set(p) - PRINT_KEYS), "a print field with no encoding yet; decide one first")
    for rs in [r for r in p.get("restated", []) if as_of is None or r["published"] <= as_of]:
        assert set(rs) <= PRINT_KEYS | {"published", "source"}, (p["quarter"], "a restated field with no encoding yet")
        check_print({**{k: v for k, v in p.items() if k not in ("restated", "fy_actual")},
                     **{k: v for k, v in rs.items() if k not in ("published", "source")}})
    r = p["raw"]
    # growth on the year-ago figure; against a year-ago loss, over the loss's absolute value (the CAT 2014-2017 and SO 2018-2021 rule)
    pct = lambda a, b: round((b / a - 1) * 100, 1) if a > 0 else round((b - a) / abs(a) * 100, 1) if a < 0 else None
    mg = lambda x, rev: round(x / rev * 100 + 0.0, 2)
    m_ = lambda x, rev: mg(x, rev)
    bp_ = lambda x, rev, xp, revp: round((mg(x, rev) - mg(xp, revp)) * 100, 1)
    want = {"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": pct(r["rev_prior_m"], r["rev_m"]),
            "opm": m_(r["oi_m"], r["rev_m"]), "opm_bp": bp_(r["oi_m"], r["rev_m"], r["oi_prior_m"], r["rev_prior_m"]),
            "ptm": m_(r["pti_m"], r["rev_m"]), "ptm_bp": bp_(r["pti_m"], r["rev_m"], r["pti_prior_m"], r["rev_prior_m"]),
            "eps_q": r["eps_q"], "eps_q_prior": r["eps_q_prior"], "diluted_shares_m": r["dil_sh_m"],
            "gp_pct": pct(r["gp_prior_m"], r["gp_m"]), "lm_pct": pct(r["lm_prior_m"], r["lm_m"])}
    for k, v in want.items():
        assert p[k] == v or (v is not None and abs(p[k] - v) < 1e-9), (p["quarter"], k, p[k], v)
    a = p.get("fy_actual")
    if a:
        assert set(a) <= FY_KEYS, (p["quarter"], sorted(set(a) - FY_KEYS), "a full-year field with no encoding yet; decide one first")
        t = a["one_off_test"]
        kept = a["eps_normalized"] is not None
        # a year is kept at GAAP unless it is a loss or its listed one-off charges exceed its income attributable to TRC (the AAPL FY2002
        # test), or, where the listed items are a net benefit, the benefit exceeds the income without it (the mirror test)
        it, inc = t["items_after_tax_m"], t["income_attributable_m"]
        assert t["kind"] == ("benefits" if it < 0 else "charges"), (p["quarter"], "the one-off test's kind")
        assert t["distorted"] == ((-it > inc + it) if it < 0 else (it > inc)), (p["quarter"], "the one-off test")
        gaap = a.get("eps_gaap", a["eps_normalized"])          # a loss year would carry its GAAP EPS here, out of the history
        # (TRGP 2014-2017) TRC's own Q4 2016 release prints no per-share figure ('eps_gaap' None): its year is a loss by the net loss
        # attributable to common shareholders it reports
        loss = (inc < 0) if gaap is None else (gaap <= 0)
        assert gaap is not None or inc < 0, (p["quarter"], "a year with no published EPS must be a loss by its reported income")
        assert kept == (not t["distorted"] and not loss), (p["quarter"], "the year's EPS and the one-off test disagree")
        assert not kept or gaap == a["eps_normalized"], (p["quarter"], "a kept year is its GAAP EPS")


def first_buildable(facts):
    """The release that first publishes a full year of TRC's EPS (FY2011, the Q4 2011 release): no date before it has a P/E."""
    return min(p["published"] for p in facts["prints"] if p.get("fy_actual") and p["fy_actual"]["eps_normalized"])


def build(as_of, facts, raw, spx, engine, out):
    listing = facts["listing"]
    first_day = listing["first_trading_day"]
    if as_of < first_day:
        sys.exit(f"{as_of}: Targa Resources Corp.'s common stock was first listed and traded on {first_day} (NYSE: TRGP); no TRGP share "
                 "and no P/E of its own exists before it, and the units of Targa Resources Partners LP (NYSE: NGLS) are a different "
                 "security, never substituted (the listing rule; retro/README.md, \"TRGP\")")
    if as_of <= first_buildable(facts):
        sys.exit(f"{as_of}: no full year of Targa Resources Corp.'s EPS is public yet (2010 is a loss per share and 2008-2009 have no EPS "
                 f"to common shareholders; the first, 2011, comes with the Q4 2011 release of {first_buildable(facts)}), so the stock has no "
                 "P/E of its own (method r2; retro/README.md, \"TRGP\")")
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    if as_of < first_day:
        sys.exit(f"{as_of}: Targa Resources Corp.'s common stock was first listed and traded on {first_day} (NYSE: TRGP); no TRGP share "
                 "and no P/E of its own exists before it, and the units of Targa Resources Partners LP (NYSE: NGLS) are a different "
                 "security, never substituted (the listing rule; retro/README.md, \"TRGP\")")
    chart = retro_tool.chart(SYMBOL)
    assert not chart.get("events", {}).get("splits") and not facts["distributions"], "a split or distribution needs its encoding first"
    assert min(raw) == first_day, ("the price data's first day moved", min(raw))     # Yahoo's TRGP series starts at the listing
    px = {d: v for d, v in raw.items() if d >= first_day}   # no split or distribution: Yahoo's close is the price as traded
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no annual history of Targa Resources Corp. as a listed company is public yet (the FY2010 10-K, 2011-02-28), "
                 "and no full year of EPS until the Q4 2011 release (2012-02-23): no P/E of its own (retro/README.md, \"TRGP\")")
    for v in vintages:                                 # the fiscal calendar the filings state must match the rule
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    guides = [g for g in facts["guides"] if g["published"] <= as_of]
    assert all(g["rev_none"] and set(g) == {"fy", "published", "source", "rev_none", "display"} for g in guides), \
        "a guide in numbers needs its encoding first (no TRGP filing of 2011-2013 guides revenue, EPS or a margin)"
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    for p in facts["prints"]:                          # a print public on AS_OF must match its raw figures (and its restatements)
        if p["published"] <= as_of:
            check_print(p, as_of)
    public = [as_restated(p, as_of) for p in facts["prints"] if p["published"] <= as_of]
    h = vintages[-1]                                   # latest annual history public on AS_OF
    # (TRGP 2014-2017) a revenue revision filed after the vintage (the 8-K of 2014-10-23: 2011-2013 on the net basis of NGL buy-sell
    # transactions) replaces those years until a later 10-K reports them
    for rv in facts.get("revenue_restatements", []):
        if h["published"] < rv["published"] <= as_of:
            h = {**h, "revenue_usd_b": {**h["revenue_usd_b"], **rv["revenue_usd_b"]},
                 "revenue_sources": {**h["revenue_sources"], **{y: rv["source"] for y in rv["revenue_usd_b"]}},
                 "sources": list(h["sources"]) + [rv["source"]],
                 "revenue_note": f'{h["revenue_note"]}; {rv["note"]}'}
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    prints = [p for p in public if guide_fy(p) >= first_fy]
    events = [e for e in facts["events"] if e["published"] <= as_of]
    if events:
        sys.exit(f"{as_of}: the TRGP builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is in the fact sheet for this date")
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage
    h = {**h, "extended": ""}
    for p in prints:
        a = p.get("fy_actual")
        if a and a["fy"] not in reported(h):          # the 10-K vintage, once out, wins
            y = str(a["fy"])
            if a["eps_normalized"] is None:           # an excluded year: reported, but out of the EPS history
                h.update(eps_excluded={**h.get("eps_excluded", {}), y: a["excluded_note"]})
            else:
                h.update(eps_normalized={**h["eps_normalized"], y: a["eps_normalized"]})
            h.update(fy_label=a["fy_label"],
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]},
                     # (TRGP 2014-2017) TRC's own Q4 2016 release prints no share count: the year's count waits for the 10-K
                     diluted_shares_m={**h["diluted_shares_m"], **({y: a["diluted_shares_m"]} if "diluted_shares_m" in a else {})},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_sales_growth=a["sales_growth"],
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
            if a["op_margin"] is not None:
                h.update(prev_fy_op_margin=a["op_margin"], prev_fy_op_margin_note=a["op_margin_note"],
                         check_pretax_margin=a["check_pretax_margin"], check_pretax_note=a["check_pretax_note"],
                         tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})')
            else:                                     # Q4 2025: the release prints no pre-tax income; the vintage's last year's stand
                h.update(normalization=f'{h["normalization"]}; FY{y[2:]}\'s income before income taxes is not in the {p["quarter"]} '
                                       "release, so the pre-tax margin and tax rate below are the vintage's last year's until the 10-K")
    for k in ("prev_fy_op_margin", "check_pretax_margin", "tax_rate"):
        assert h[k] is not None, (as_of, k, "the vintage's last year needs its Q4 print's full-year figures")
    latest = prints[-1]
    i = public.index(latest)
    prev_seg = (public[i - 1]["gp_pct"], public[i - 1]["quarter"]) if i > 0 else (None, "no earlier print")
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    excluded = {int(k): v for k, v in h.get("eps_excluded", {}).items()}
    if not eps_hist:                                   # 2010 a loss, 2008-2009 no EPS to common shareholders: no full year, no P/E
        sys.exit(f"{as_of}: no full year of Targa Resources Corp.'s EPS is public yet (2010 is a loss per share and 2008-2009 have no EPS "
                 "to common shareholders; the first, 2011, comes with the Q4 2011 release of 2012-02-23), so the stock has no P/E of its "
                 "own (method r2; retro/README.md, \"TRGP\")")
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)        # the last full year in the history: cur_fy - 1 unless that year is excluded
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── current-FY EPS: no guide in numbers, so the last full year's EPS stands (the PFE rule) ──
    excluded_tail = "".join(f" (FY{y % 100:02d} is excluded: {excluded[y]})" for y in range(last_fy + 1, cur_fy))
    eps_now = eps_hist[last_fy]
    eps_label = (f"{fy_e}: no reported (GAAP) EPS guide, FY{last_fy % 100:02d}'s ${money(eps_now)} stands" + excluded_tail)
    fwd = [latest["sales_pct"]] * 2
    fwd_label, fwd_short, fwd_period = (f"no {fy_now} revenue guide in numbers, {latest['quarter']} revenues as reported",
                                        f"{latest['quarter'][:2]} revenues", latest["quarter"])
    g_now = [g for g in guides if g["fy"] >= cur_fy]
    guide_text = (f"{fy_now}: no revenue, EPS or margin guide in numbers (BASE takes {latest['quarter']} revenue growth as reported)"
                  + (f"; {g_now[-1]['display']} ({g_now[-1]['source']}, {g_now[-1]['published']})" if g_now else ""))
    margin_guided = False                          # no margin guide: no guided step
    fy_margin_base = h["prev_fy_op_margin"]

    # ── dividend: the latest declared quarterly rate, from the release that states it ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts["dividends"] if d["published"] <= as_of]
    _, dividend, dividend_note, dividend_src = max(divs, key=lambda x: x[0])
    assert not facts["buyback_programs"], "a repurchase program needs its encoding first"
    bb = None
    cash_return = h["cash_return_text"]

    # ── market statistics, prices truncated at AS_OF, from the listing (the listing rule) ──
    days = sorted(d for d in px if first_day <= d <= as_of)
    close = px[as_of][2]
    assert minus_years(as_of, 1) >= first_day, (as_of, "less than a year since the listing: the 52-week statistics need their encoding first")
    yr = [d for d in days if d > minus_years(as_of, 1)]
    low52, high52 = min(px[d][1] for d in yr), max(px[d][0] for d in yr)
    common = [d for d in yr if d in spx]
    ra = [math.log(px[common[i]][2] / px[common[i - 1]][2]) for i in range(1, len(common))]
    rm = [math.log(spx[common[i]][2] / spx[common[i - 1]][2]) for i in range(1, len(common))]
    ma, mm = sum(ra) / len(ra), sum(rm) / len(rm)
    vol = (sum((x - ma) ** 2 for x in ra) / len(ra)) ** 0.5 * 252 ** 0.5
    beta = (sum((x - ma) * (y - mm) for x, y in zip(ra, rm)) / len(ra)) / (sum((y - mm) ** 2 for y in rm) / len(rm))
    eps = {**eps_hist, cur_fy: eps_now}                                # + current-FY EPS, for the P/E series
    fy = lambda d: min(fiscal_year(d), cur_fy)     # a day past the last reported year keeps the current year's EPS
    assert h["pe_window_start"] == first_day, "the P/E window runs from the listing"
    window = [d for d in days if d > minus_years(as_of, 10)]
    # an excluded year's own days leave the window (2010, a loss)
    gone = sorted({fy(d) for d in window} & set(excluded))
    window = [d for d in window if fy(d) not in excluded]
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

    # ── era-dependent text, from facts only: no disruption theme in the registry is live for a midstream natural gas company ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none in scope", "No live disruption theme covers midstream natural gas and NGLs"
    theme_summary = "no theme in the registry is live for a midstream natural gas company on this date; none has dated evidence"
    key_tail = ("By the company's own account the Partnership's percent-of-proceeds arrangements expose it to commodity prices;\n"
                "  the bear needs NGL prices and volumes to fall across the segments, not one quarter's.")
    if "Our primary natural gas gathering" in h["why"]:      # (TRGP 2014-2017) the FY2016 10-K speaks for TRC itself after the buy-in
        key_tail = ("By the company's own account its percent-of-proceeds arrangements expose it to commodity prices;\n"
                    "  the bear needs NGL prices and volumes to fall across the segments, not one quarter's.")
    why = h["why"]
    # from CLOUD's live date (2012-10-30) every live theme is quoted with its registered scope (the CB 2014-2017, UNH, SCHW and LYB wording)
    live = sorted(((t["live_from"], k, t["scope"]) for k, t in retro_tool.load_taxonomy()["themes"].items() if t["live_from"] <= as_of))
    live_k = [k for _, k, _ in live]
    # (TRGP 2014-2017) ECOMMERCE (2015-01-01), STREAMING (2015-08-04) and ENERGY_TRANSITION (2015-12-12) were searched for in the
    # FY2013-FY2016 10-Ks: no 10-K names e-commerce or streaming, and ENERGY_TRANSITION's reserves and refining are read as out of scope
    # for a gatherer and processor that holds neither (the BKR reading), its greenhouse gas risk factor quoted in the "why"
    ALL = ["OFFSHORE", "CLOUD", "ECOMMERCE", "STREAMING", "ENERGY_TRANSITION"]
    assert live_k == ALL[:len(live_k)], (as_of, "a live theme the TRGP 10-Ks were not searched for", live_k)
    if len(live_k) > 2:
        assert "ghg_quote" in h, (as_of, "a vintage before FY2013 has no greenhouse gas quote")
        scopes = ", ".join(f"{k} {'is scoped to' if i == 0 else 'to'} '{sc}'" for i, (_, k, sc) in enumerate(live))
        head = why.split("; no theme in taxonomy_eras.json is live")[0]
        assert head != why, (as_of, "the vintage's why lost its theme clause")
        et = ""
        if "ENERGY_TRANSITION" in live_k:
            et = (" but ENERGY_TRANSITION, whose oil, gas and coal reserves and refining a gatherer and processor does not hold (the BKR "
                  f"reading: the {h['tenk_label']} names no reserves of Targa's, and its refinery services are NGL balancing for refiners, "
                  f"'{h['refinery_quote']}'" + (f"; the Channelview Splitter is a '{h['splitter_quote']}' at Channelview, under construction"
                                                if "splitter_quote" in h else "") + ")")
        why = (head + "; no disruption theme in taxonomy_eras.json is live for a midstream natural gas company on this date (of the "
               f"live themes, {scopes}: none names midstream energy{et}; the 10-Ks' 'offshore' is the Gulf of Mexico, they name cloud "
               "only as a director's other board, Cloud Peak Energy Inc., and no 10-K names e-commerce or streaming), so the watch list "
               f"is empty and these words stay here, with the greenhouse gas risk factor: '{h['ghg_quote']}' (the PEP obesity rule)")
    elif live_k != ["OFFSHORE"]:
        scopes = ", ".join(f"{k} {'is scoped to' if i == 0 else 'to'} '{sc}'" for i, (_, k, sc) in enumerate(live))
        head = why.split("; no theme in taxonomy_eras.json is live")[0]
        assert head != why, (as_of, "the vintage's why lost its theme clause")
        why = (head + "; no disruption theme in taxonomy_eras.json is live for a midstream natural gas company on this date (of the "
               f"live themes, {scopes}: none names midstream energy; the 10-Ks' 'offshore' is the Gulf of Mexico, and they name cloud "
               "only as a director's other board, Cloud Peak Energy Inc.), so the watch list is empty and these words stay here (the "
               "PEP obesity rule)")
    kind, pit_risk = h["kind"], 2
    cat3 = f"(3) The {fy_now} outlook — no revenue, EPS or margin guide in numbers (the outlooks are the Partnership's EBITDA and TRC's dividends)"
    if cur_fy >= 2017:                                 # (TRGP 2014-2017) TRC's own 2017 guidance: volumes, capital spending, the dividend
        cat3 = f"(3) The {fy_now} outlook — no revenue, EPS or margin guide in numbers (the outlooks are volumes, capital spending and TRC's dividend)"
    cat4 = f"(4) Free cash flow — {h['fcf_label']} {h['fcf_note']}"

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    # a print dated AS_OF occurs only in a week with no trading day after it; it meets AS_OF's close only if it was public before that
    # close: an 8-K accepted before the open or during market hours (the UNP Good Friday 2014 and SCHW rule)
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        rt = same_day[-1].get("release_time", "")
        early = "(before the open)" in rt
        assert early or "(during market hours)" in rt, (as_of, same_day[-1]["quarter"], "not public before the close")
        tag = (f"(day of the {same_day[-1]['quarter']} print, public before the open)" if early else
               f"(day of the {same_day[-1]['quarter']} print, released during the session)")

    company, exchange, listed = h["company"], h["exchange"], h["symbol"]
    ids = (list(h["sources"]) + [p["source"] for p in prints] + list(latest.get("extra_sources", [])) + [public[i - 1]["source"]]
           + [listing["source"]]
           + ([dividend_src] if dividend_src else []) + ([g_now[-1]["source"]] if g_now else []))
    sources = [dict(id=i, **{k: v for k, v in facts["sources"][i].items()}) for i in dict.fromkeys(ids)]
    sources.append({"id": "A0", "published": as_of,
                    "title": f"Yahoo Finance daily prices, {company} common stock ({exchange}: {listed}) and S&P 500, truncated at AS_OF",
                    "url": f"https://finance.yahoo.com/quote/{SYMBOL}/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution "
                                f"since the listing on {first_day}"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "opm", "opm_bp", "ptm", "ptm_bp", "eps_q", "eps_q_prior",
                   "gp_pct", "lm_pct")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    activity = (f"Activity: {latest['sales_note']}; segments: {latest['seg_note']}; {latest['margin_note']}; {latest['cash_note']}; "
                f"EPS {latest['eps_note']}")
    fy_rev = rev[max(rev)] * (1 + sum(fwd) / 2 / 100)
    fy_rev_label = f"{fwd_label}, applied to the year (no {fy_now} revenue guide)"
    franchise_q = (f"{latest['quarter'].split()[0]} operating margin {latest['opm']:.2f}% ({latest['opm_bp']:+.0f}bp)" if latest["opm"] is not None
                   else f"{latest['quarter'].split()[0]} operating margin n/r (no operating income for the quarter in the filings)")
    fcf_text = f"${h['fcf_b']:.2f}B" if h["fcf_b"] >= 0 else f"$({-h['fcf_b']:.2f})B"
    LATEST = {k: latest.get(k) for k in latest_keys}
    # (TRGP 2014-2017) TRC's own releases print no share count: until the 10-Q, the latest diluted count public (display only)
    sh_dil, sh_dil_note = latest["diluted_shares_m"], ""
    if sh_dil is None:
        src_p = next(p for p in reversed(public[:i]) if p["diluted_shares_m"] is not None)
        sh_dil, sh_dil_note = src_p["diluted_shares_m"], f" ({src_p['quarter']}'s; the {latest['quarter']} release prints no share count)"
    if latest["eps_q"] is None or latest["eps_q_prior"] is None:
        with open(ENGINE2, encoding="utf-8") as fh:
            engine = fh.read()
    R = repr
    head = f'''#!/usr/bin/env python3
"""
{listed} Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: {listed})  ·  {h["business_line"]}
Generated by retro/build_trgp.py from retro/facts/TRGP.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "{SYMBOL}"
LISTED_SYMBOL = "{listed}"   # the listing on AS_OF
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); midstream signals")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts above.
PIT_PROFILE = {{
    "kind": "{kind}",
    "risk": {pit_risk},
    "why": {R(why)},
    "theme_watch": {R(watch)},
    "evidence": [],
}}

# ── FACTS: market (prices truncated at AS_OF, as traded on each day) ──────────
CURRENT_PRICE   = {close:.2f}   # USD, {exchange} close {as_of}
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
REVENUE_HIST  = {R(rev)}   # revenues, USD bn; {h["revenue_note"]}
SHARES_HIST   = {R({y: round(v, 1) for y, v in shares.items()})}   # {h["shares_note"]}
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # pre-tax margin, {h["prev_fy_op_margin_note"]}
CHECK_PRETAX_MARGIN = {h["check_pretax_margin"]}   # {h["check_pretax_note"]}
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}
KIND_TEXT     = {R(h["kind_text"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} outlook ──
LATEST          = {R(LATEST)}
PREV_SEG        = {R(prev_seg)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # no revenue guide in numbers: the latest quarter's revenue growth as reported
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no margin guide, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {fy_rev:.2f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {round(sh_dil / 1000, 4)!r}   # diluted shares, bn{sh_dil_note}
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenues {h['prev_fy_sales_growth']:+.1f}%; {franchise_q}")}
BALANCE_TEXT    = {R(f"{h['fcf_label']} free cash flow {fcf_text}, dividend ${dividend:.2f} a year, {cash_return}")}
ACTIVITY_TEXT   = {R(activity)}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/TRGP)")
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
        print(f"{d}  {tag:<34}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
