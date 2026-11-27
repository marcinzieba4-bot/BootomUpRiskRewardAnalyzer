#!/usr/bin/env python3
"""
Build CRM retrospective models from the dated fact sheet (retro/facts/CRM.json).

salesforce.com, inc., NYSE: CRM (CIK 1108524), the first subscription software company in the retrospectives. The NVDA sibling
(build_nvda.py) with a subscription company's fields: the same frozen rules (retro method r2), the same weekly dates and the same
market statistics, with the NVDA signal set's subscription counterparts and salesforce.com's own rule-T thresholds
(retro/templates/crm_engine.py.tmpl), the UNH fiscal-year EPS guide midpoint and the NVDA dollar-level next-quarter revenue guide.
For each as-of date the builder
  1. selects only the history vintage, prints and guides whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, on the AS_OF share basis (Yahoo's split-adjusted series
     times the splits after AS_OF: x4 for the four-for-one split of 2013-04-18, so every 2008-2009 price is the price as traded),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

salesforce.com listed on 2004-06-23 (NYSE: CRM), inside the ten-year window of every 2008-2009 date, so the window runs from the
listing (method r2, "A listing inside the window"). Its fiscal year ends on January 31 (FY2009: February 1, 2008 to January 31,
2009). The method r2 inputs map as follows (retro/README.md, "CRM"; decided before any CRM model was built or scored):
  - EPS: GAAP diluted EPS, each year from the latest filing that reports it, except FY2006 at the company's figure excluding only
    one-offs ($0.181, the Q4 FY06 release: without the reversal of the deferred tax valuation allowance and the lease recovery; the
    ACN rule); the releases of Q4 FY07 on print GAAP only. The inception period to January 2000 and fiscal 2001-2003 are losses and
    FY2004 is distorted by a one-off benefit (the mirror test: its $3,445K lease recovery against $794K of pre-tax income without it);
    FY2004 is not the latest year, so it takes the years before it (the PFE 2003 and MU FY2003 rule): the history starts with FY2005
    and the P/E window after January 31, 2004, i.e. at the listing. FY2007's GAAP EPS is $0.00 (break-even), which has no P/E (the F
    2009 rule): it is excluded as the latest year of the FY2007 10-K (its own days leave the window) and stays a gap after;
  - current-FY EPS: the midpoint of the fiscal-year GAAP diluted EPS range, from the latest guide public on AS_OF that states one
    (the UNH rule); a range given with and without an acquisition's effect (InStranet, 2008-08-20) is used with it, as the effect
    recurs; a guided loss has no P/E; with no range yet, the last full year's EPS stands (the rollover rule);
  - forward revenue growth: the next quarter's revenue guide, a dollar range, read against the year-ago quarter's revenues from that
    quarter's own release (the AAPL, AVGO and NVDA level rule); with none in scope, the latest quarter's revenue growth (the UNP rule);
  - guided margin step: none (no filing guides a margin); the margin signal uses the latest quarter's operating margin change;
  - the fiscal-year revenue guide sets the segment bridge's total only (display), else the forward growth applied to the year;
  - dividend: none ("We have never paid any cash dividends on our common stock.").
The kind is DURABLE: no 10-K calls the business cyclical. No disruption theme in taxonomy_eras.json is live for a subscription
software company in 2008-2009 (OFFSHORE is scoped to IT services; CLOUD is not live before 2012-10-30, and the FY2008-FY2009 10-Ks
name cloud computing as salesforce.com's own model), so the builder refuses events until a theme encoding is decided; it also refuses
a dividend, a change of company name and a distribution, none of which occurs.

From 2010 on (decided on 2026-11-26 in the session that built and scored 2008-2009, before any 2010-2012 date was built or scored;
retro/README.md, "CRM 2010-2012"): the method and the encodings above carry the FY2010-FY2012 vintages and the Q4 FY10 to Q3 FY13
prints; FY2012 ($(0.09), a loss) is excluded as the latest year like FY2007, and the FY2012-FY2013 guides that are losses have no P/E, so
FY11's $0.47 stands (the loss-guide rule); the builder gains a fiscal-year revenue guide stated as growth ('rev_guide_pct', the segment
bridge only), the convertible senior notes of January 2010 in the balance text ('debt_note' on a print; 'no debt' without one), and, from
CLOUD's live date (2012-10-30), every live theme's scope in the "why" (the CB and UNH wording), CLOUD out of scope as salesforce.com's own
model.

From 2013 on (retro/README.md, "CRM 2013-2017"; decided before any 2013-2017 date was built or scored, in a new session that had not
opened the 2008-2012 outcomes or findings): a reduced-data batch. SEC refused this session's downloads of the filing documents, so from
the first filing not read (the 8-K of 2013-02-22, public 2013-02-25; 'reduced_data' in the fact sheet) the facts are SEC's XBRL company
facts of the 10-Qs and 10-Ks only, each dated by its filing: the 10-Q or 10-K is the print, the 10-K the vintage, and the releases'
guidance is not in the sheet, so the method's own fallbacks apply (the latest quarter's revenue growth for the forward guide, the last
full year's EPS for the current year: the rollover rule) and every text says the guide is not in this fact sheet rather than that none
was given. The four-for-one split of 2013-04-18 (the price series' event) puts every earlier per-share figure on the new basis. The
themes live from 2015 (ECOMMERCE, STREAMING, ENERGY_TRANSITION) name no software business, so the watch list stays empty.
From 2018 (retro/README.md, "CRM 2018-2021", decided in the session that scored 2013-2017): the same reduced data, now with ASC 606
(the FY2019 10-K restates FY2017-FY2018; unearned revenue for deferred revenue from Q1 FY19), total revenues standing in for subscription
and support where professional services is not tagged, and EV and CRYPTO (live 2020) also naming no software business.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. salesforce.com released after the close, so a print is dated the next trading day; on a Friday
that is the week's last trading day, and the print meets its close (public before the open; the AVGO rule).

Output goes to staging/retrospective/CRM until the series is added to the archive (--out archive/retrospective/CRM).

Usage
  python3 retro/build_crm.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_crm.py --weekly 2009-01-05 2009-12-31
  python3 retro/build_crm.py --weekly 2010-01-04 2012-12-31
  python3 retro/build_crm.py --weekly 2013-01-01 2017-12-31
  python3 retro/build_crm.py --weekly 2018-01-01 2021-12-31
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/CRM/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "CRM.json")
with open(os.path.join(HERE, "taxonomy_eras.json"), encoding="utf-8") as _fh:
    TAXO = json.load(_fh)
ENGINE = os.path.join(HERE, "templates", "crm_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "CRM")
SYMBOL = "CRM"
# the guide fields this builder has an encoding for; any other field needs its encoding decided first
GUIDE_KEYS = {"fy", "published", "source", "doc", "quarter", "level_stated", "level_m", "prior_label", "prior_sales_m", "prior_source",
              "prior_row", "yoy_pct", "quote", "rev_guide_usd_b", "rev_quote", "eps_guide", "eps_quote", "eps_guide_note", "eps_ex_item",
              "note", "display", "rev_guide_pct"}       # (CRM 2010-2012) a fiscal-year revenue guide stated as growth
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"sub": (40, 61, 82, 328), "deferred": (43, 68, 93, 169), "gross_margin": (-740, -330, 70, 3600),
                     "opex_gap": (49, 12, -24, -305), "op_margin": (-2800, -720, 1360, 48650)}
RULE_T_KEYS = {"sub": (1, False), "deferred": (1, False), "gross_margin": (10, False), "opex_gap": (1, True),
               "op_margin": (10, False)}           # (rounding unit, lower is better)


def fiscal_year(day):
    """salesforce.com's fiscal year n runs from February 1 of calendar year n-1 to January 31 of year n ('Our fiscal year ends on
    January 31.')."""
    d = dt.date.fromisoformat(day)
    return d.year + (1 if d.month >= 2 else 0)


def rule_t_value(k, r):
    """One annual rule-T value from its raw figures ($ thousands, (prior, current))."""
    pct = lambda a, b: (b / a - 1) * 100
    if k == "sub":
        return round(pct(*r["sub_k"]) + 0.0, 2)
    if k == "deferred":
        return round(pct(*r["deferred_k"]) + 0.0, 2)
    if k == "gross_margin":
        (g0, g1), (a0, a1) = r["gross_profit_k"], r["revenue_k"]
        return round((g1 / a1 - g0 / a0) * 10000 + 0.0, 1)
    if k == "op_margin":
        (o0, o1), (a0, a1) = r["op_income_k"], r["revenue_k"]
        return round((o1 / a1 - o0 / a0) * 10000 + 0.0, 1)
    (d0, d1), (m0, m1), (g0, g1), (a0, a1) = r["rd_k"], r["ms_k"], r["ga_k"], r["revenue_k"]
    return round(pct(d0 + m0 + g0, d1 + m1 + g1) - pct(a0, a1) + 0.0, 2)


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
    """Re-derive a print's growth rates, margins and gap from its raw published figures ($ thousands; they must match)."""
    r = p["raw"]
    pct = lambda a, b: (b / a - 1) * 100
    r1 = lambda x: round(x + 0.0, 1)
    gm, gm0 = r["gross_profit_k"] / r["sales_k"] * 100, r["gross_profit_prior_k"] / r["sales_prior_k"] * 100
    om, om0 = r["op_income_k"] / r["sales_k"] * 100, r["op_income_prior_k"] / r["sales_prior_k"] * 100
    ox, ox0 = r["rd_k"] + r["ms_k"] + r["ga_k"], r["rd_prior_k"] + r["ms_prior_k"] + r["ga_prior_k"]
    want = dict(sales_b=round(r["sales_k"] / 1e6, 4), sales_pct=r1(pct(r["sales_prior_k"], r["sales_k"])),
                seq_pct=r1(pct(r["sales_prev_q_k"], r["sales_k"])), sub_pct=r1(pct(r["sub_prior_k"], r["sub_k"])),
                deferred_b=round(r["deferred_k"] / 1e6, 4), deferred_pct=r1(pct(r["deferred_prior_k"], r["deferred_k"])),
                gross_margin=round(gm + 0.0, 2), gross_margin_bp=r1((gm - gm0) * 100), op_margin=round(om + 0.0, 2),
                op_margin_bp=r1((om - om0) * 100), opex_pct=r1(pct(ox0, ox)), opex_gap_pp=r1(pct(ox0, ox) - pct(r["sales_prior_k"], r["sales_k"])))
    for k, v in want.items():
        assert p[k] == v, (p["quarter"], k, p[k], v)


def check_guide(g):
    if g.get("level_stated"):     # a dollar range for the next quarter, read against the year-ago quarter
        lv = g["level_m"]
        assert lv[0] <= lv[1], (g["doc"], lv)
        assert [round((x / g["prior_sales_m"] - 1) * 100 + 0.0, 1) for x in lv] == g["yoy_pct"], (g["doc"], "yoy")
    if g.get("eps_guide") is not None:
        assert g["eps_guide"][0] <= g["eps_guide"][1], g["doc"]


def on_basis(facts, as_of):
    """The fact sheet with every per-share fact on the AS_OF share basis: a split effective on or before AS_OF divides per-share values
    whose share basis predates it and multiplies share counts by it (the NVDA helper; no split falls in 2008-2009). A figure's basis
    is its filing's date: a vintage year's the date of the filing it comes from ('eps_published', else the vintage's)."""
    f = copy.deepcopy(facts)
    splits = [s for s in f.get("splits", []) if s["effective"] <= as_of]
    k = lambda basis: math.prod(s["ratio"] for s in splits if basis < s["effective"])
    for v in f["history_vintages"]:
        basis = lambda y: v.get("eps_published", {}).get(y, v["published"])
        v["eps_normalized"] = {y: e / k(basis(y)) for y, e in v["eps_normalized"].items()}
        v["diluted_shares_m"] = {y: n * k(basis(y)) for y, n in v["diluted_shares_m"].items()}
        notes = []
        for s in splits:
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
    for g in f["guides"]:
        if g.get("eps_guide") is not None:
            g["eps_guide"] = [x / k(g["published"]) for x in g["eps_guide"]]
    return f, [s["source"] for s in splits]


def _range(v):
    lo, hi = v
    return f"{lo:+g}%" if lo == hi else f"{lo:+g}% to {hi:+g}%"


def _eps_rng(v):
    m = lambda x: f"({money(-x)})" if x < 0 else money(x)
    return m(v[0]) if v[0] == v[1] else f"{m(v[0])}-{m(v[1])}"


def _usd_rng(v):
    b = lambda x: f"{x:.3f}".rstrip("0").rstrip(".") if x < 10 else f"{x:.2f}"
    return f"${b(v[0])}B" if v[0] == v[1] else f"${b(v[0])}-{b(v[1])}B"


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    listing = facts["listing"]["first_trading_day"]
    assert min(raw) == listing, ("the price data must start on the listing day", min(raw), listing)
    # every price of the window on the AS_OF share basis: Yahoo's split-adjusted series times the splits after AS_OF
    chart = retro_tool.chart(SYMBOL)
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat()
                    for v in chart.get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo_splits for s in facts.get("splits", [])), "a split's effective date must match the price data"
    for kind in ("events", "company_names", "distributions", "dividends"):
        if [x for x in facts.get(kind, []) if x.get("published", x.get("effective", "")) <= as_of]:
            sys.exit(f"{as_of}: the CRM builder has no encoding for {kind}; decide one first")
    for g in [g for g in facts["guides"] if g["published"] <= as_of]:      # a guide public on AS_OF may carry only encoded fields
        assert set(g) <= GUIDE_KEYS, (g["doc"], "a guide field with no encoding yet; decide one first", set(g) - GUIDE_KEYS)
        check_guide(g)
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        check_print(p)
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    for v in facts["history_vintages"]:
        assert v["fiscal_year"] == "ends January 31"
    # on_basis divides every Q4 print's full-year EPS; an excluded year has none, so a NaN stands in for it there and None comes
    # back after (the LLY, BMY and UNH encoding: FY2007, $0.00, has no P/E)
    held = {p["quarter"] for p in facts["prints"] if "fy_actual" in p and p["fy_actual"]["eps_normalized"] is None}
    facts = {**facts, "prints": [{**p, "fy_actual": {**p["fy_actual"], "eps_normalized": math.nan}} if p["quarter"] in held else p
                                 for p in facts["prints"]]}
    facts, split_ids = on_basis(facts, as_of)
    for p in facts["prints"]:
        if p["quarter"] in held:
            p["fy_actual"]["eps_normalized"] = None
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    # prints published by AS_OF that report a fiscal year after the history (a Q4 print reports the year just ended, so it stays in
    # scope after the 10-K that follows it); a year excluded from the EPS history ('eps_excluded': FY2007, $0.00) is still reported
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    prints = [p for p in facts["prints"] if p["published"] <= as_of and guide_fy(p) >= first_fy]
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is public yet")
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage
    h = {**h, "extended": ""}
    for p in prints:
        a = p.get("fy_actual")
        if a and a["fy"] not in reported(h):          # the 10-K vintage, once out, wins
            y = str(a["fy"])
            if a["eps_normalized"] is None:           # a year with no P/E: reported, but out of the EPS history
                h.update(eps_excluded={**h.get("eps_excluded", {}), y: a["excluded_note"]})
            h.update(fy_label=a["fy_label"],
                     eps_normalized={**h["eps_normalized"], **({y: a["eps_normalized"]} if a["eps_normalized"] is not None else {})},
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]},
                     diluted_shares_m={**h["diluted_shares_m"], y: a["diluted_shares_m"]},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_op_margin=a["op_margin"], prev_fy_op_margin_note=a["op_margin_note"],
                     prev_fy_pretax_margin=a["pretax_margin"], prev_fy_pretax_margin_note=a["pretax_margin_note"],
                     prev_fy_gross_margin=a["gross_margin"], prev_fy_sales_growth=a["sales_growth"], prev_fy_sub_growth=a["sub_growth"],
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
    # (CRM 2013-2017) a reduced-data date: the earnings releases, other 8-Ks and 10-K text published from 'first_unread' are not in the sheet
    reduced = as_of >= facts.get("reduced_data", {}).get("first_unread", "9999")
    absent = "not in this fact sheet (reduced-data batch)"
    last_fy = max(eps_hist)        # the last full year in the history: cur_fy - 1 unless that year is excluded
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} FY{(latest['fy'] + (1 if nq == 4 else 0)) % 100:02d}"

    # ── guides for the current fiscal year: each field from the latest guide public on AS_OF that states it ──
    fy_guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    stated = lambda k: next((g for g in reversed(fy_guides) if g.get(k) is not None), None)
    ge = stated("eps_guide")
    # the latest fiscal-year revenue guide, in dollars or (CRM 2010-2012) as growth on the last full year
    gr = next((g for g in reversed(fy_guides) if g.get("rev_guide_usd_b") is not None or g.get("rev_guide_pct") is not None), None)
    loss_guide = bool(ge) and sum(ge["eps_guide"]) / 2 <= 0
    if ge and not loss_guide:
        eps_now = round(sum(ge["eps_guide"]) / 2, 6)
        eps_label = f"{fy_e} EPS, guide midpoint (${_eps_rng(ge['eps_guide'])}, {ge['doc']}: {ge['eps_guide_note']})"
    else:      # no numeric EPS guide yet, or a guided loss (no P/E): the last full year's EPS stands (the rollover rule)
        eps_now = eps_hist[last_fy]
        why = (f"the EPS guide (${_eps_rng(ge['eps_guide'])}, {ge['doc']}) is not positive, which has no P/E" if loss_guide
               else f"the EPS guide is {absent}" if reduced else "no numeric EPS guide yet")
        eps_label = f"{fy_e}: {why}, FY{last_fy % 100:02d}'s ${money(eps_now)} stands" + "".join(
            f" ({excluded[y]})" if excluded[y].startswith(f"FY{y} is excluded") else f" (FY{y % 100:02d} is excluded: {excluded[y]})"
            for y in range(last_fy + 1, cur_fy))
    eps_label_short = (f"{fy_e} EPS, guide midpoint (${_eps_rng(ge['eps_guide'])}, {ge['doc']})" if ge and not loss_guide
                       else eps_label)
    # ── forward revenue growth: the latest numeric guide for the quarter after the latest print, as growth on the year-ago quarter;
    # with none in scope, the latest quarter's revenue growth (the UNP rule) ──
    qg = [g for g in facts["guides"] if g["published"] <= as_of and g.get("quarter") == next_q and g.get("level_stated")]
    if qg:
        g = qg[-1]
        fwd = list(g["yoy_pct"])
        lvl = f"${g['level_m'][0]:,.0f}M" if g["level_m"][0] == g["level_m"][1] else f"${g['level_m'][0]:,.0f}-{g['level_m'][1]:,.0f}M"
        fwd_label = f"{next_q} revenue guide ({g['doc']})"
        fwd_short, fwd_period = f"{next_q} guide YoY", next_q
        q_text = (f"{next_q} revenue {lvl} ('{g['quote']}') against {g['prior_label']}'s ${g['prior_sales_m']:,.1f}M: "
                  f"{_range(fwd)} YoY; display only: {g['display']}")
        guide_ids = [g["source"], g["prior_source"]]
    else:
        fwd = [latest["sales_pct"]] * 2
        fwd_label = f"{latest['quarter']} revenue growth (" + (f"the {next_q} guide is {absent}" if reduced else f"no {next_q} guide in numbers") + ")"
        fwd_short, fwd_period = f"{latest['quarter'].split()[0]} revenue YoY", latest["quarter"]
        q_text = (f"{next_q}: the revenue guide is {absent}" if reduced else f"{next_q}: no revenue guide in numbers") + \
            "; the latest quarter's revenue growth stands in (the UNP rule)"
        guide_ids = []
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    last_rev = rev[max(rev)]
    fy_prev = f"FY{max(rev) % 100:02d}"
    pct_rng = lambda v: f"{v[0]:g}%" if v[0] == v[1] else f"{v[0]:g}-{v[1]:g}%"
    if gr and gr.get("rev_guide_usd_b") is not None:      # the fiscal-year revenue guide sets the segment bridge's total only (display)
        fy_rev_b = sum(gr["rev_guide_usd_b"]) / 2
        fy_rev_label = f"{fy_now} revenue guide midpoint ({_usd_rng(gr['rev_guide_usd_b'])}, {gr['doc']})"
    elif gr:        # (CRM 2010-2012) stated as growth: read on the last full year's revenues (the CAT and CMCSA reading), display only
        fy_rev_b = last_rev * (1 + sum(gr["rev_guide_pct"]) / 2 / 100)
        fy_rev_label = f"{fy_now} revenue guide midpoint ({pct_rng(gr['rev_guide_pct'])} growth on {fy_prev}'s ${last_rev:.3f}B, {gr['doc']})"
    else:
        fy_rev_b = last_rev * (1 + sum(fwd) / 2 / 100)
        fy_rev_label = f"the {fwd_label}, YoY, applied to the year (" + (f"the {fy_now} revenue guide is {absent}" if reduced else f"no {fy_now} revenue guide") + ")"
    bits = ([f"EPS ${_eps_rng(ge['eps_guide'])} ({ge['doc']}: {ge['eps_guide_note']})"
             + (" (not positive: no P/E, so not used)" if loss_guide else "")
             + (f"; without the acquisition ${_eps_rng(ge['eps_ex_item']['eps'])}, not used ('{ge['eps_ex_item']['quote']}')"
                if ge.get("eps_ex_item") else "")] if ge else [f"the {fy_now} EPS range is {absent}" if reduced else f"no {fy_now} EPS range in numbers yet"])
    bits += ([f"revenue {_usd_rng(gr['rev_guide_usd_b'])} ({gr['doc']}; the segment bridge only)"] if gr and gr.get("rev_guide_usd_b") is not None
             else [f"revenue growth {pct_rng(gr['rev_guide_pct'])} ({gr['doc']}; the segment bridge only)"] if gr else
             [f"the {fy_now} revenue range is {absent}" if reduced else f"no {fy_now} revenue range in numbers"])
    bits += [g["note"] for g in fy_guides[-1:] if g.get("note")]
    guide_text = (f"{next_q} outlook: {q_text}; {fy_now} guide" + (f" ({', '.join(dict.fromkeys(g['doc'] for g in fy_guides))})" if fy_guides else "")
                  + ": " + "; ".join(bits) + ("; no margin guide in this fact sheet" if reduced else "; no margin guide"))
    cat3 = (f"(3) The {fy_now} EPS guide — ${_eps_rng(ge['eps_guide'])} GAAP ({ge['doc']})" if ge else
            f"(3) The {fy_now} EPS guide — {absent}" if reduced else f"(3) A numeric {fy_now} EPS guide — none yet")
    margin_guided = False                          # no margin guide: no guided step; the signal uses the latest quarter
    fy_margin_base = h["prev_fy_op_margin"]
    guide_src = [g["source"] for g in fy_guides]

    # ── dividend: none ('We have never paid any cash dividends on our common stock.') ──
    dividend, dividend_note = h["dividend_annual"], h["dividend_note"]

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
    # the listing rule: the window runs from the first trading day (every price day is on or after it), up to ten years, and not
    # before the day after the excluded first year (FY2004: 2004-02-01, before the listing)
    window = [d for d in days if d > minus_years(as_of, 10) and (not h["pe_window_start"] or d >= h["pe_window_start"])]
    assert window[0] >= listing
    # an excluded year's own days leave the window (the r2 rule for a distorted latest year, kept once it is a gap)
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

    # ── era-dependent text, from facts only: no disruption theme is live for a subscription software company on AS_OF ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
    key_tail = ("A subscription slowdown shows up in deferred revenue first, then in\n"
                "  subscription and support revenue a few quarters later.")
    theme_summary = "no disruption theme has dated evidence"
    # CLOUD is not live before 2012-10-30 (a date no earlier model may print); the 10-Ks' cloud computing words name salesforce.com's
    # own model, the side that displaces on-premise software, not a substitute for it (the GOOG, AVGO and NVDA reading)
    live = sorted(((t["live_from"], k, t["scope"]) for k, t in TAXO["themes"].items() if t["live_from"] <= as_of))
    # (CRM 2013-2017) the themes live from 2015 are scoped to retail, pay-TV and fossil fuels, (CRM 2018-2021) EV and CRYPTO to
    # automotive and to payments, banks and exchanges: none names a software business
    later = ("ECOMMERCE", "STREAMING", "ENERGY_TRANSITION", "EV", "CRYPTO")
    assert {k for _, k, _ in live} <= {"OFFSHORE", "CLOUD", *later}, (as_of, live, "a theme with no encoding is live: decide its encoding first")
    if [k for _, k, _ in live] == ["OFFSHORE"]:
        why = (h["why"] + "; no disruption theme in taxonomy_eras.json is live for a subscription software company on this date "
               "(OFFSHORE, the one theme live, is scoped to IT services, and the 10-K's cloud computing words, where it has them, describe "
               "salesforce.com's own model, not a substitute for it), so the watch list is empty and these words stay here (the PEP "
               "obesity rule)")
    else:            # (CRM 2010-2012) from CLOUD's live date: every live theme with its registered scope (the CB and UNH wording)
        scopes = ", ".join(f"{k} {'is scoped to' if i == 0 else 'to'} '{sc}'" for i, (_, k, sc) in enumerate(live))
        tenk = "the FY2012 10-K (the last whose text is in this fact sheet)" if reduced else "the 10-K"
        rest = [k for _, k, _ in live if k in later]
        rest_text = (f"; {', '.join(rest[:-1]) + ' and ' + rest[-1] if len(rest) > 1 else rest[0]} "
                     f"name{'s' if len(rest) == 1 else ''} no software business") if rest else ""
        why = (h["why"] + "; no disruption theme in taxonomy_eras.json is live for a subscription software company on this date (of the "
               f"live themes, {scopes}: {tenk} names cloud computing as salesforce.com's own model, the side that displaces on-premise "
               f"software, not a substitute for it, and names no offshore delivery{rest_text}), so the watch list is empty and these words "
               "stay here (the PEP obesity rule)")
    cat4 = (f"(4) Operating expenses — R&D, marketing and sales and G&A {latest['opex_pct']:+.1f}% against revenue "
            f"{latest['sales_pct']:+.1f}% in {latest['quarter']} ({latest['opex_gap_pp']:+.1f}pp): the cost of growth")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    # only a print public before the open can meet AS_OF's close: salesforce.com released after the previous day's close, so a print
    # dated AS_OF occurs only in a week with no trading day after it (a Friday)
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    company, exchange = h["company"], h["exchange"]
    ids = (list(h["sources"]) + [facts["listing"]["source"]] + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])]
           + [public[i - 1]["source"]] + guide_ids + guide_src + split_ids)
    sources = [dict(id=x, **facts["sources"][x]) for x in dict.fromkeys(ids)]
    sources.append({"id": "Y0", "published": as_of, "title": "Yahoo Finance daily prices, CRM and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/CRM/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF (Yahoo's split-adjusted close x{fx:g}), 52-week range, realized vol, "
                                f"beta, the {window_label} P/E distribution from the listing on {listing}"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "seq_pct", "sub_pct", "deferred_b", "deferred_pct", "gross_margin",
                   "gross_margin_bp", "op_margin", "op_margin_bp", "opex_pct", "opex_gap_pp", "eps_q", "eps_q_prior")
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    first_excl = "; ".join(f"FY{int(y) % 100:02d} {t}" for y, t in sorted(h.get("eps_first_excluded", {}).items()))
    rev_text = (f"Revenue: {latest['sales_note']}; {latest['deferred_note']}; {latest['eps_note']}; {latest['shares_note']}"
                + (f"; {latest['note']}" if latest.get("note") else ""))
    cash_return = h["cash_return_text"]
    R = repr
    methodology_tail = ('\n               "; reduced-data batch from ' + facts["reduced_data"]["first_unread"] + ': SEC XBRL company facts of the 10-Qs "\n'
                        '               "and 10-Ks only (the earnings releases, their guidance and the 10-Ks\' text are not in the fact sheet)"'
                        if reduced else "")
    head = f'''#!/usr/bin/env python3
"""
CRM Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: CRM)  ·  {h["business_line"]}
Generated by retro/build_crm.py from retro/facts/CRM.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "CRM"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); subscription software signals with "
               "salesforce.com's rule-T thresholds; the listing rule (CRM listed 2004-06-23)"{methodology_tail})
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts above.
PIT_PROFILE = {{
    "kind": {R(h["kind"])},
    "risk": 2,
    "why": {R(why)},
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
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # total revenues, USD bn
SHARES_HIST   = {R({y: round(v, 3) for y, v in shares.items()})}   # diluted, millions
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # operating margin, {h["prev_fy_op_margin_note"]}
CHECK_PRETAX_MARGIN = {h["prev_fy_pretax_margin"]}   # pre-tax margin for the EPS check (display), {h["prev_fy_pretax_margin_note"]}
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}), the {next_q} outlook and the {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_SALES      = {R(prev)}
EPP_TODAY_EPS   = {round(eps_now, 6)}   # {eps_label}
EPS_LABEL       = {R(eps_label_short)}
FWD_GUIDE       = {R(tuple(fwd))}   # the next-quarter revenue guide as growth on the year-ago quarter (else the latest quarter's growth)
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no margin guide, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {fy_rev_b:.4f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenues {h['prev_fy_sales_growth']:+.1f}%, " + (f"subscription and support {h['prev_fy_sub_growth']:+.1f}%" if h['prev_fy_sub_growth'] is not None else "subscription and support not in the company facts") + f", gross margin {h['prev_fy_gross_margin']:.1f}%; {latest['quarter'].split()[0]} " + ("unearned" if latest['deferred_note'].startswith("unearned") else "deferred") + f" revenue {latest['deferred_pct']:+.1f}% YoY")}
BALANCE_TEXT    = {R(f"Cash, cash equivalents and marketable securities ${latest['cash_b']:.3f}B ({latest['quarter']}), {latest.get('debt_note', 'no debt')}, {h['fcf_label']} free cash flow ${h['fcf_b']:.3f}B ({h['fcf_note']}), " + (f"dividend ${dividend:.2f} a year" if dividend else "no dividend"))}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/CRM)")
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
