#!/usr/bin/env python3
"""
Build WMT retrospective models from the dated fact sheet (retro/facts/WMT.json).

The WMT sibling of build_low.py and build_shw.py: the same frozen rules (retro method r2), the same weekly dates and the same
market statistics, with discount-retail signals in the LOW layout (retro/templates/wmt_engine.py.tmpl). For each as-of date the
builder
  1. selects only the history vintage, prints, guides and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, on the AS_OF share basis (Yahoo's split-adjusted
     series times the splits after AS_OF: the three-for-one split of 2024-02-26 for every date before it; the two-for-one split of
     1999-04-19 precedes every per-share fact in the fact sheet, so nothing is restated),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Walmart's fiscal year N ends on January 31 of calendar year N (fiscal 2008 ended 2008-01-31). Each earnings release guides diluted
EPS from continuing operations for the next quarter and, in most releases, for the fiscal year, and U.S. comparable store sales for
the next quarter in most; from the Q4 FY11 release some guide fiscal-year net sales, and none guides a margin in numbers. Guides
are therefore their own dated list, as for LOW and SHW, and each field comes from the latest guide for the current fiscal year that
states it. The method r2 inputs map as follows (retro/README.md, "WMT"):
  - current-FY EPS: the fiscal-year EPS guide midpoint (no numeric EPS guide: the last full year's EPS stands),
  - forward revenue growth: the next-quarter net sales guide for a quarter not yet reported (none in numbers: the fiscal-year net
    sales guide; none either: the latest quarter's net sales growth excluding the currency effect the release states, the NKE, PEP
    and SHW rule, or as reported when the release states none, as every release of 2007-2008 does),
  - guided margin step: none (no margin guide in numbers); the margin signal takes the latest quarter's operating-margin change.
The comparable store sales guide for the next quarter is shown in the guide line and feeds no input, as are a net sales guide's
note ('rev_guide_note') and a later update in words to the fiscal-year EPS range ('fy_words', shown while no later numeric range
replaces it; the range stands, the ACN rule; retro/README.md, "WMT 2012-2014").
A later print may publish an earlier year's company figure on a new basis ('restates': the Q4 FY11 release's FY10 underlying $3.67 as
adjusted for the change in inventory accounting); it replaces the year from that print until a 10-K vintage published after it carries
the year (the SHW rule; retro/README.md, "WMT 2009-2011").
From 2015 (retro/README.md, "WMT 2015-2017"): ECOMMERCE, live from 2015-01-01, joins the watch list from each 10-K's competition risk
factor (company-acknowledged, no market read; text only); a fiscal-year net sales guide stated excluding currency ('rev_basis') is method
r2's local-currency guide; and a one-off inside operating income that a release states in dollars, with the change excluding it, leaves
that release's operating margin ('op_oneoff_m', 'op_oneoff_prior_m').
From 2018 (retro/README.md, "WMT 2018-2020"): a guide may withdraw named fields of its year ('withdrawn', the SHW rule; the Q1 FY21
release), and net sales guided only in words or as a one-sided bound ('rev_words') are shown and give no field.
From 2021 (retro/README.md, "WMT 2021-2023"): an EPS guide stated as growth on the last full year ('eps_growth', a range in percent: the
NKE rule) gives the current-FY EPS as that year's EPS times the midpoint, and the latest EPS guide in either form stands; a next-quarter
net sales guide may carry its basis ('sales_basis'); and a net sales guide stated as reported growth with the currency effect for the
guided period in dollars in the same filing is converted to constant currency on the year-ago net sales (the PEP 2026 rule and the WMT
2012-2014 conversion: 'rev_reported', 'rev_currency_m', 'rev_prior_m'; in a quarter guide 'sales_reported', 'currency_m', 'prior_m'),
which the builder re-derives.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release,
where it is the first trading day after it. The earnings 8-Ks were accepted before the open on the release day.

Output goes to staging/retrospective/WMT until the series is added to the archive (--out archive/retrospective/WMT).

Usage
  python3 retro/build_wmt.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_wmt.py --weekly 2009-01-05 2011-12-31
  python3 retro/build_wmt.py --weekly 2012-01-02 2014-12-31
  python3 retro/build_wmt.py --weekly 2015-01-05 2017-12-31
  python3 retro/build_wmt.py --weekly 2018-01-01 2020-12-31
  python3 retro/build_wmt.py --weekly 2021-01-04 2023-12-31
  python3 retro/build_wmt.py 2008-02-20
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/WMT/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "WMT.json")
ENGINE = os.path.join(HERE, "templates", "wmt_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "WMT")
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"comps": (-1, 2, 5, 9), "gross_margin": (-60, -20, 30, 60), "sales": (7, 10, 13, 19),
                     "inventory_gap": (6, 1, -4, -15), "op_margin": (-90, -40, 10, 40)}
RULE_T_KEYS = {"comps": (1, False), "gross_margin": (10, False), "sales": (1, False), "inventory_gap": (1, True),
               "op_margin": (10, False)}           # (rounding unit, lower is better)


def fiscal_year_end(n):
    """Walmart's fiscal year n ends on January 31 of calendar year n."""
    return dt.date(n, 1, 31)


def fiscal_year(day):
    """The fiscal year a calendar day belongs to."""
    d = dt.date.fromisoformat(day)
    return d.year + 1 if d > fiscal_year_end(d.year) else d.year


def eps_rng(lo, hi):
    """an EPS range: '3.13-3.17', or one figure for a point"""
    return money(lo) if lo == hi else f"{money(lo)}-{money(hi)}"


def rule_t(rt):
    """Rule T thresholds from the annual values: XBULL best, BULL median, BASE worst, BEAR one median-to-worst step beyond
    the worst; rounded half up to whole percent and points and to 10 bp. The values are first re-derived from the raw figures
    the fact sheet keeps (the FY2007 10-K's Eleven-Year Financial Summary; each operating-margin change from its own filing)."""
    raw = rt["raw"]
    s = {int(k): v for k, v in raw["summary_fy1997_2007"]["net_sales_m"].items()}
    c = {int(k): v for k, v in raw["summary_fy1997_2007"]["cost_of_sales_m"].items()}
    i = {int(k): v for k, v in raw["summary_fy1997_2007"]["inventories_m"].items()}
    cp = {int(k): v for k, v in raw["summary_fy1997_2007"]["comps_pct"].items()}
    gm = lambda y: (s[y] - c[y]) / s[y] * 100
    opm = lambda t: (t[0] + t[1] - t[2] - t[3]) / t[0] * 100
    r2 = lambda x: round(x + 1e-12, 2)
    years = [int(y) for y in rt["comps"]["values"]]
    want = {"comps": {y: float(cp[y]) for y in years},
            "gross_margin": {y: r2((gm(y) - gm(y - 1)) * 100) for y in years},
            "sales": {y: r2((s[y] / s[y - 1] - 1) * 100) for y in years},
            "inventory_gap": {y: r2((i[y] / i[y - 1] - 1) * 100 - (s[y] / s[y - 1] - 1) * 100) for y in years},
            "op_margin": {y: r2((opm(raw["op_income_statements"][str(y)][str(y)]) -
                                 opm(raw["op_income_statements"][str(y)][str(y - 1)])) * 100) for y in years}}
    out = {}
    for k, (unit, lower) in RULE_T_KEYS.items():
        assert (rt[k]["unit"], rt[k]["lower_is_better"]) == (unit, lower), (k, "the fact sheet's unit or direction differs")
        assert {int(y): v for y, v in rt[k]["values"].items()} == want[k], (k, "values differ from the raw figures")
        v = sorted(rt[k]["values"].values())
        assert len(v) >= 2, (k, "rule T needs at least two annual values")
        n = len(v)
        med = v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
        worst, best = (v[-1], v[0]) if lower else (v[0], v[-1])
        r = lambda x: math.floor(x / unit + 0.5) * unit
        out[k] = (r(worst + (worst - med)), r(worst), r(med), r(best))
        assert tuple(rt[k]["thresholds"][t] for t in ("BEAR", "BASE", "BULL", "XBULL")) == out[k], (k, "stored thresholds differ")
    return out


def check_print(p):
    """Re-derive a print's growth, margins and inventory growth from its raw published figures (they must match)."""
    r = p["raw"]
    assert r["ns_m"] + r["other_m"] - r["cogs_m"] - r["sga_m"] == r["op_m"], (p["quarter"], "operating income")
    assert r["ns_prior_m"] + r["other_prior_m"] - r["cogs_prior_m"] - r["sga_prior_m"] == r["op_prior_m"], (p["quarter"], "prior")
    m, m0 = (r["ns_m"] - r["cogs_m"]) / r["ns_m"] * 100, (r["ns_prior_m"] - r["cogs_prior_m"]) / r["ns_prior_m"] * 100
    # a one-off inside operating income that the release states in dollars, with the change excluding it, leaves that release's operating
    # margin ('op_oneoff_m' in the quarter, 'op_oneoff_prior_m' in the year-ago quarter; retro/README.md, "WMT 2015-2017")
    o = (r["op_m"] - r.get("op_oneoff_m", 0)) / r["ns_m"] * 100
    o0 = (r["op_prior_m"] - r.get("op_oneoff_prior_m", 0)) / r["ns_prior_m"] * 100
    sp = round((r["ns_m"] / r["ns_prior_m"] - 1) * 100, 1)
    ip = round((r["inv_m"] / r["inv_prior_m"] - 1) * 100, 1)
    want = {"sales_b": round(r["ns_m"] / 1000, 3), "sales_pct": sp, "gross_margin": round(m, 2),
            "gross_margin_bp": round((m - m0) * 100, 1), "op_margin": round(o, 2), "op_margin_bp": round((o - o0) * 100, 1),
            "inventory_pct": ip, "inventory_gap_pp": round(ip - sp, 1), "diluted_shares_m": r["diluted_shares_m"]}
    for k, v in want.items():
        assert p[k] == v or abs(p[k] - v) < 1e-9, (p["quarter"], k, p[k], v)
    if p.get("currency_m") is not None:            # a stated dollar effect re-derives the constant-currency growth (or agrees with a stated one)
        d = round(((r["ns_m"] - p["currency_m"]) / r["ns_prior_m"] - 1) * 100, 1)
        assert (p["lc_pct"] == d) if p["lc_basis"] == "derived" else abs(p["lc_pct"] - d) <= 0.11, (p["quarter"], "currency", p["lc_pct"], d)


def check_guide(g):
    """Re-derive a net sales guide converted to constant currency from reported growth and the currency effect the same filing
    states for the guided period, on the year-ago net sales (retro/README.md, "WMT 2021-2023"); the stored range must match."""
    conv = lambda rep, cur, prior: [round(x - cur / prior * 100 + 1e-12, 1) for x in rep]
    if "rev_reported" in g:
        assert g["rev_guide"] == conv(g["rev_reported"], g["rev_currency_m"], g["rev_prior_m"]), (g["doc"], "rev_guide", g["rev_guide"])
    q = g.get("q_guide", {})
    if "sales_reported" in q:
        assert q["sales"] == conv(q["sales_reported"], q["currency_m"], q["prior_m"]), (g["doc"], q["quarter"], "sales", q["sales"])


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    # every price of the window on the AS_OF share basis: Yahoo's split-adjusted series times the splits after AS_OF
    chart = retro_tool.chart("WMT")
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat()
                    for v in chart.get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo_splits for s in facts.get("splits", [])), "a split's effective date must match the price data"
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        check_print(p)
    for g in [g for g in facts["guides"] if g["published"] <= as_of]:  # and a converted guide its reported growth and currency
        check_guide(g)
    facts, split_ids = on_basis(facts, as_of)
    for g in facts["guides"]:                      # a next-quarter EPS guide is per share too (on_basis covers the rest)
        r = math.prod(s["ratio"] for s in facts.get("splits", []) if g["published"] < s["effective"] <= as_of)
        if r != 1 and "eps" in g.get("q_guide", {}):
            g["q_guide"]["eps"] = [e / r for e in g["q_guide"]["eps"]]
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    # prints published by AS_OF that report a fiscal year after the history (a Q4 print reports the year just ended, so it
    # stays in scope after the 10-K that follows it)
    first_fy = max(int(k) for k in h["eps_normalized"]) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    prints = [p for p in facts["prints"] if p["published"] <= as_of and guide_fy(p) >= first_fy]
    # no disruption theme in taxonomy_eras.json is live for a discount retailer before 2015 (ECOMMERCE, scoped to physical retail, from
    # 2015-01-01). The one encoding decided (retro/README.md, "WMT 2015-2017"): each 10-K's competition risk factor, which names e-commerce or
    # digital retail (ecommerce_company_acknowledged), puts ECOMMERCE on the watch list from the theme's live date, with the latest 10-K's
    # words (a 10-K's wording is replaced by the next 10-K's; the MSFT CLOUD and XOM rule). Any other event kind needs its encoding decided first
    events = [e for e in facts["events"] if e["published"] <= as_of and (h["published"] <= e["published"] or "doc" not in e)]
    if any(e["kind"] != "ecommerce_company_acknowledged" for e in events):
        sys.exit(f"{as_of}: the WMT builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
    themes = retro_tool.load_taxonomy()["themes"]
    events = [e for e in events if themes[e["theme"]]["live_from"] <= as_of]      # a theme counts only from its live date
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is public yet")
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage
    h = {**h, "extended": ""}
    for p in prints:
        a = p.get("fy_actual")
        if a and str(a["fy"]) not in h["eps_normalized"]:          # the 10-K vintage, once out, wins
            y = str(a["fy"])
            h.update(fy_label=a["fy_label"],
                     eps_normalized={**h["eps_normalized"], y: a["eps_normalized"]},
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]},
                     diluted_shares_m={**h["diluted_shares_m"], y: a["diluted_shares_m"]},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_op_margin=a["op_margin"], prev_fy_op_margin_note=a["op_margin_note"],
                     prev_fy_gross_margin=a["gross_margin"], prev_fy_sales_growth=a["sales_growth"],
                     prev_fy_comps=a["comps_pct"], prev_fy_stores=a["stores"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     net_interest_b=a["net_interest_b"], net_interest_note=f'FY{y[2:]} interest, net ({p["source"]})',
                     fcf_b=a["fcf_b"], fcf_label=a["fy_label"], fcf_note=a["fcf_note"],
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    # a company figure for an earlier year of the history, first published in a later print ('restates': the Q4 FY11 release's FY10
    # underlying $3.67 as adjusted for the change in inventory accounting), replaces it from that print until a 10-K vintage published
    # after the print carries the year (each year from the latest filing that reports it; the SHW rule)
    for p in prints:
        if p.get("restates") and p["published"] > h["published"]:
            for yy, e in p["restates"].items():
                assert yy in h["eps_normalized"], (p["quarter"], yy, "restates a year outside the history")
                h.update(eps_normalized={**h["eps_normalized"], yy: e}, normalization=f'{h["normalization"]}; {p["restates_note"]}',
                         extended=f'{h["extended"]}, FY{yy[2:]} EPS from {p["source"]} ({p["published"]})')
    latest = prints[-1]
    # the previous quarter is the print published just before the latest one (in or out of the history's scope); before the
    # first print in the fact sheet, the vintage names it
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    i = public.index(latest)
    prev = (public[i - 1]["comps_pct"], public[i - 1]["quarter"]) if i > 0 else (h["prev_q_comps"], h["prev_q_label"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    cur_fy = max(eps_hist) + 1
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} FY{(latest['fy'] + (1 if nq == 4 else 0)) % 100:02d}"

    # ── guides for the current fiscal year, each field from the latest guide that states it ──
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    # a guide may withdraw named fields of its year ('withdrawn': the Q1 FY21 release withdraws the FY21 guidance, the SHW, LOW and AAPL
    # rule): each is void in every earlier guide for that year, so only a guide published on or after the withdrawal can state it again
    void = {}
    for g in guides:
        for k in g.get("withdrawn", []):
            void[k] = g["published"]
    wd = next((g for g in reversed(guides) if g.get("withdrawn")), None)
    stated = lambda k: next((g for g in reversed(guides) if k in g and g["published"] >= void.get(k, "")), None)
    ge, gr, gw = stated("eps_guide"), stated("rev_guide"), stated("fy_words")
    # an EPS guide stated as growth on the last full year ('eps_growth', the NKE rule; retro/README.md, "WMT 2021-2023"): the latest EPS
    # guide in either form stands
    gg = stated("eps_growth")
    if gg and (not ge or gg["published"] > ge["published"]):
        ge = gg
    eps_fig = lambda g: (f"EPS ${eps_rng(*g['eps_guide'])}" if "eps_guide" in g else
                         f"EPS {pct_range(*g['eps_growth'])} on FY{(cur_fy - 1) % 100:02d}'s ${money(eps_hist[cur_fy - 1])}")
    if gw and ge and gw["published"] < ge["published"]:
        gw = None                            # a later numeric range replaces words about an earlier one
    # net sales guided only in words or as a one-sided bound ('rev_words': "at least 3 percent", the PEP, UNP and LOW rule: no field),
    # shown while no later numeric net sales range replaces it
    grw = stated("rev_words")
    if grw and gr and grw["published"] < gr["published"]:
        grw = None
    qkey = lambda q: (int(q.split("FY")[1]), int(q[1]))
    later = lambda q: qkey(q) > (latest["fy"] % 100, nq)          # a next-quarter guide counts while its quarter is unreported
    gq = next((g for g in reversed(guides) if "q_guide" in g and later(g["q_guide"]["quarter"])), None)
    q = gq["q_guide"] if gq else None
    if ge and "eps_growth" in ge:            # growth on the last full year's EPS, at the midpoint of the range
        mid = sum(ge["eps_growth"]) / 2
        eps_now = round(eps_hist[cur_fy - 1] * (1 + mid / 100), 2)
        eps_label = (f"{fy_e} EPS, FY{(cur_fy - 1) % 100:02d}'s ${money(eps_hist[cur_fy - 1])} {mid:+g}%, the midpoint of the "
                     f"{ge['doc']}'s EPS growth guide")
    elif ge:
        eps_now = round(sum(ge["eps_guide"]) / 2, 3)
        eps_label = f"{fy_e} EPS, guide midpoint"
    else:                                    # no numeric EPS guide: the last full year's EPS stands (rollover rule)
        eps_now = eps_hist[cur_fy - 1]
        eps_label = (f"{fy_e}: guidance withdrawn ({wd['doc']}), FY{(cur_fy - 1) % 100:02d}'s ${money(eps_now)} stands" if wd else
                     f"{fy_e}: no numeric EPS guide yet, FY{(cur_fy - 1) % 100:02d}'s ${money(eps_now)} stands")
    if q and "sales" in q:                   # method r2: the next-quarter net sales guide
        qb = f" {q['sales_basis']}" if q.get("sales_basis") else ""
        fwd, fwd_label, fwd_short, fwd_period = q["sales"], f"{q['quarter']} net sales guide{qb}", f"{q['quarter'][:2]} guide", q["quarter"]
        fwd_kind = "next-quarter net sales guide"
    elif gr:                                 # no next-quarter guide in numbers: the fiscal-year net sales guide
        # a guide stated excluding currency ('rev_basis') is method r2's local-currency guide (the PEP rule; retro/README.md, "WMT 2015-2017")
        basis = f" {gr['rev_basis']}" if gr.get("rev_basis") else ""
        fwd, fwd_label, fwd_short, fwd_period = gr["rev_guide"], f"{fy_now} net sales guide{basis}", f"{fy_now} guide", fy_now
        fwd_kind = f"fiscal-year net sales guide{basis} (no next-quarter guide in numbers)"
    elif latest.get("lc_pct") is not None:   # no net sales guide in numbers: the latest quarter at constant currency (NKE, PEP, SHW)
        fwd = [latest["lc_pct"]] * 2
        fwd_label = f"no {fy_now} net sales guide in numbers, {latest['quarter']} net sales at constant currency"
        fwd_short, fwd_period = f"{latest['quarter'][:2]} ex-FX", latest["quarter"]
        fwd_kind = (f"no net sales guide in numbers: {latest['quarter']} growth {latest['sales_pct']:+.1f}% excluding the currency effect "
                    f"the release states ({latest['lc_pct']:+.1f}% at constant currency)")
    else:                                    # no net sales guide in numbers: the latest quarter's growth as reported (LOW, SHW)
        fwd = [latest["sales_pct"]] * 2
        fwd_label = f"no {fy_now} net sales guide in numbers, {latest['quarter']} net sales"
        fwd_short, fwd_period = f"{latest['quarter'][:2]} sales", latest["quarter"]
        fwd_kind = f"no net sales guide in numbers: {latest['quarter']} growth as reported (the release states no currency effect)"
    fy_rev = gr["rev_guide"] if gr else fwd
    fy_rev_label = (f"{fy_now} net sales guide" + (f" {gr['rev_basis']}" if gr.get("rev_basis") else "") if gr else
                    f"{fwd_label}, applied to the year" if q and "sales" in q else
                    f"{latest['quarter']} net sales growth at constant currency applied to the year (no {fy_now} net sales guide in numbers)"
                    if fwd_short.endswith("ex-FX") else
                    f"{latest['quarter']} net sales growth applied to the year (no {fy_now} net sales guide in numbers)")
    if guides:
        gnote = ge.get("eps_guide_note", ge.get("eps_growth_note")) if ge else None
        bits = ([eps_fig(ge) + (f" ({gnote}; {ge['doc']})" if gnote else f" ({ge['doc']})")]
                if ge else [f"no {fy_now} EPS range: the {wd['doc']} withdrew the guidance ('{wd['withdrawn_quote']}')"] if wd else
                [f"no {fy_now} EPS range yet"]) + \
               ([f"{gw['fy_words']} ({gw['doc']}; " + ("the range stands)" if ge else "words, no range)")] if gw else []) + \
               ([f"net sales {grw['rev_words']} ({grw['doc']}; no range)"] if grw else []) + \
               ([f"net sales {pct_range(*gr['rev_guide'])}" + (f" {gr['rev_basis']}" if gr.get("rev_basis") else "")
                 + (f" ({gr['rev_guide_note']})" if gr.get("rev_guide_note") else "")] if gr else []) + \
               ([f"{q['quarter']}: " + ", ".join(
                   ([f"net sales {pct_range(*q['sales'])}" + (f" {q['sales_basis']}" if q.get("sales_basis") else "")] if "sales" in q else []) +
                   ([f"U.S. comps {pct_range(*q['comps'])}"] if "comps" in q else []) +
                   ([q["comps_text"]] if "comps_text" in q else []) +
                   ([f"EPS ${eps_rng(*q['eps'])}"] if "eps" in q else []))] if q else [])
        guide_text = f"{fy_now} guide ({', '.join(dict.fromkeys(g['doc'] for g in guides))}): " + "; ".join(bits)
    else:
        guide_text = f"{fy_now}: no guide yet"
    margin_guided = False                          # no margin guide in numbers: no guided step
    fy_margin_base = h["prev_fy_op_margin"]

    # ── dividend: the latest declared rate ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts["dividends"] if d["published"] <= as_of]
    divs.append((h.get("dividend_published", h["published"]), h["dividend_annual"], h["dividend_note"], None))
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

    # ── era-dependent text, from facts only: which disruption theme has dated evidence on AS_OF ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
    key_tail = ("General economic conditions drive demand, by the company's own account; the bear\n"
                "  needs fuel, labor and health-care costs to keep rising while comps fall.")
    theme_summary = "no disruption theme has dated evidence"
    why = h["why"]
    if h.get("why_theme_tail"):                    # from the FY2014 vintage the theme clause follows the theme's status on AS_OF
        why += "; no disruption theme is live for it"
    for e in [e for e in events if e["kind"] == "ecommerce_company_acknowledged"][-1:]:
        # ECOMMERCE is live from 2015-01-01 and scoped to physical retail, grocery included; the latest 10-K's competition risk factor puts
        # it on the watch list (the ACN CLOUD rule, as for LOW: company-acknowledged, no market read). The factor pair nets to zero and the
        # theme signal stays at 2/4, so only text changes. The registry's market-pricing event (2017-06-16) names no company, so it is quoted
        # from its date and re-files nothing (the LOW and PEP reading); re-filing needs dated evidence of market pricing for Walmart
        th = themes[e["theme"]]
        mp = [x for x in th["pit_evidence"] if x["date"] <= as_of]
        mp_txt = (f" The theme registry dates the market's pricing of e-commerce to {mp[-1]['date']} ({mp[-1]['event']}), evidence that "
                  "names no company." if mp else "")
        val_word = "a premium" if pe_now_pctl >= 70 else "a discount to its own history" if pe_now_pctl <= 30 else "near its own median"
        stage = "ecommerce"
        watch = [{"theme": "ECOMMERCE", "status": "live, company-acknowledged; no market read",
                  "reason": (f"Live: Walmart's own {e['doc']} says '{e['risk_quote']}' At the same time {e['offering']}. "
                             f"The stock trades at {close / eps_now:.1f}x {fy_e_s} — {val_word}.{mp_txt} Re-file as DISRUPTION_EXPOSED "
                             "(ECOMMERCE) only if dated evidence shows the market pricing online substitution of Walmart's store "
                             "sales specifically.")}]
        factors = [(f"Omni-channel: {e['offering_short']} — Walmart sells online itself", 0.2, 0.10),
                   (f"Online competition ({e['doc']}): {e['risk_short']}", -0.2, 0.10)]
        sig_name = "E-commerce: net effect on store sales"
        trigger = "Online and multi-channel rivals take share faster than Walmart's own e-commerce sales grow"
        theme_summary = "e-commerce competition is live and company-acknowledged; no dated evidence ties the multiple to it"
        assert h.get("why_theme_tail"), "a vintage before FY2014 states that no theme is live"
        why = h["why"] + ("; ECOMMERCE is live (from 2015-01-01) and its competition risk factor puts it on the watch list: "
                          "company-acknowledged, with no dated evidence that the market prices it for Walmart")
    cat3 = (f"(3) {fy_now} {eps_fig(ge)} guide ({ge['doc']})" if ge and "eps_growth" in ge else
            f"(3) {fy_now} EPS guide ${eps_rng(*ge['eps_guide'])} ({ge['doc']})" if ge else
            f"(3) A numeric {fy_now} EPS guide again — the {wd['doc']} withdrew it" if wd else
            f"(3) A numeric {fy_now} EPS guide — none yet")
    cat4 = (f"(4) Operating margin — {latest['op_margin']:.2f}% in {latest['quarter']} ({latest['op_margin_bp']:+.1f}bp): "
            "where expense deleverage on low comps shows first")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    same_day = [p for p in prints if p["published"] == as_of]     # only a release made before the open can meet AS_OF's close
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, released before the open)"

    renames = [n for n in facts.get("company_names", []) if h["published"] < n["published"] <= as_of]
    company = renames[-1]["name"] if renames else h["company"]
    exchange = h["exchange"]
    # a renamed reporting line takes the new name from the first print that uses it (the ACN service-line rule)
    line_names = {}
    for p in public:
        line_names.update(p.get("renames", {}))
    groups = [(line_names.get(n, n), v, g) for n, v, g in h["groups"]]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])] + [g["source"] for g in guides]
           + ([dividend_src] if dividend_src else []) + split_ids + [n["source"] for n in renames]
           + [p["source"] for p in public if p.get("renames")] + [e["id"] for e in events])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "WM0", "published": as_of, "title": "Yahoo Finance daily prices, WMT and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/WMT/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "comps_pct", "gross_margin", "gross_margin_bp", "op_margin",
                   "op_margin_bp", "inventory_pct", "inventory_gap_pp", "eps_q", "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    eps_note = (f"; operating margin {latest['op_margin_note']}" if latest.get("op_margin_note") else "") + \
               (f"; EPS {latest['eps_note']}" if latest.get("eps_note") else "")
    segs = ", ".join(f"{n} ${b:.2f}B {g:+.1f}%" for n, b, g in latest["segments"])
    fx_txt = (f"; currency: {latest['currency_note']}" + (f", {latest['lc_pct']:+.1f}% at constant currency" if latest.get("lc_pct") is not None else "")
              if latest.get("currency_note") else "")
    volumes = (f"Segment net sales: {segs}; comps: {latest['comps_note']}; inventory ${latest['raw']['inv_m'] / 1000:.2f}B "
               f"{latest['inventory_pct']:+.1f}% year on year{fx_txt}{eps_note}")
    stores_txt = h["prev_fy_stores"] or "no year-end store count in the Q4 release"
    R = repr
    head = f'''#!/usr/bin/env python3
"""
WMT Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: WMT)  ·  {h["business_line"]}
Generated by retro/build_wmt.py from retro/facts/WMT.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "WMT"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); discount-retail signals")
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
CURRENT_PRICE   = {close:.2f}   # USD, {exchange} close {as_of}, as traded (Yahoo's split-adjusted close x{fx:g})
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
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # operating margin, {h["prev_fy_op_margin_note"]}
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
NET_INTEREST_B = {h["net_interest_b"]}   # {h["net_interest_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_COMPS      = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # {fwd_kind}
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no margin guide in numbers, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {rev[max(rev)] * (1 + sum(fy_rev) / 2 / 100):.2f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R([tuple(g) for g in groups])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} net sales {h['prev_fy_sales_growth']:+.1f}% on U.S. comps {h['prev_fy_comps']:+.1f}%, {stores_txt}; {latest['quarter'].split()[0]} gross margin {latest['gross_margin']:.2f}% ({latest['gross_margin_bp']:+.1f}bp)")}
BALANCE_TEXT    = {R(f"Cash ${latest['cash_b']:.2f}B at {latest['period_end']}, {h['fcf_label']} free cash flow ${h['fcf_b']:.2f}B, dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/WMT)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("WMT"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<34}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
