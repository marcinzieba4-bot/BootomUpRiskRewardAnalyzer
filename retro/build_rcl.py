#!/usr/bin/env python3
"""
Build RCL retrospective models from the dated fact sheet (retro/facts/RCL.json).

The RCL sibling of build_shw.py and build_wmt.py: the same frozen rules (retro method r2), the same weekly dates and the same
market statistics, with cruise-line signals (retro/templates/rcl_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints, guides and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, on the AS_OF share basis (Yahoo's split-adjusted
     series times the splits after AS_OF; Royal Caribbean's only split, two-for-one on 1998-08-03, precedes every date and every
     per-share fact in the fact sheet, so the series is the price as traded),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Royal Caribbean's fiscal year is the calendar year. Each earnings release guides the next quarter and the year in numbers: diluted
EPS, capacity (APCD) and Net Yields (net revenue per APCD), from the Q1 2009 release also Net Yields on a constant dollar basis; Net
Cruise Costs and fuel are guided too and are shown only. Guides are their own dated list, as for SHW and WMT, and each field comes
from the latest guide for the current fiscal year that states it. The method r2 inputs map as follows (retro/README.md, "RCL"):
  - current-FY EPS: the fiscal-year EPS guide midpoint (a single figure, 'around $1.40', is a point),
  - forward revenue growth: the net revenue the next-quarter guide implies, (1 + Net Yields) x (1 + capacity) - 1, Net Revenues
    being Net Yields times APCD by the company's own definition; on a constant-currency basis where the guide states one, else the
    fiscal year's on a constant-currency basis (the ACN fallback, per print), else the next quarter's as published (no guide on a
    constant-currency basis, the SHW and MSFT reading), else the fiscal year's as published,
  - guided margin step: none (no margin guide in numbers); the margin signal takes the latest quarter's operating-margin change.
A guide given including and excluding an acquisition (2007: 'Including Pullmantur' and 'Comparable') keeps the consolidated figure;
the other goes in the note (the ACN rule). Words (a quarter's 'mid-single digits') and the Net Cruise Cost and fuel guides are shown
in the guide line and feed no input.
From 2010 (retro/README.md, "RCL 2010-2013"): a later print may publish earlier years' EPS on a new basis ('restates': the Q2 2011
release's interest expense revision of FY2009 and FY2010), which replaces them until a 10-K carries them (the SHW rule); a fiscal-year
EPS guide stated only as adjusted EPS ('eps_guide_note', Q3 2013) is used as the company's figure excluding the item (the ACN rule); and
a release that states a quarter's Net Yield or Net Cruise Cost change only at constant currency leaves the as-reported cross-check to
its per-APCD table.
From 2014 (retro/README.md, "RCL 2014-2017"): Net Yields and Net Cruise Costs are the company's own as-reported figures, re-derived from
the statement rows less the lines its reconciliation excludes ('nr_x_k', 'nc_x_k': businesses held for sale or divested before their
sale, other initiative costs, the net gain on the Pullmantur sale); every EPS guide is the company's Adjusted EPS ('eps_guide_note').

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release,
where it is the first trading day after it. A release accepted after the close (Q2 2008, 2008-07-21 18:30 ET) is dated the next
trading day (the AVGO rule), so its week's date is the trading day after that.

Output goes to staging/retrospective/RCL until the series is added to the archive (--out archive/retrospective/RCL).

Usage
  python3 retro/build_rcl.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_rcl.py --weekly 2009-01-05 2009-12-31
  python3 retro/build_rcl.py --weekly 2010-01-04 2013-12-31
  python3 retro/build_rcl.py --weekly 2014-01-06 2017-12-31
  python3 retro/build_rcl.py 2008-01-31
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/RCL/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "RCL.json")
ENGINE = os.path.join(HERE, "templates", "rcl_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "RCL")
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"ny": (-20, -9, 1, 9), "ncc": (7, 6, 6, -2), "sales": (-17, -3, 10, 43), "occupancy": (-560, -260, 40, 290),
                     "op_margin": (-1140, -540, 70, 290)}
RULE_T_KEYS = {"ny": (1, False), "ncc": (1, True), "sales": (1, False), "occupancy": (10, False), "op_margin": (10, False)}
r1, r2 = (lambda x: round(x + 1e-12, 1)), (lambda x: round(x + 1e-12, 2))


def fiscal_year_end(n):
    """Royal Caribbean's fiscal year n is the calendar year n."""
    return dt.date(n, 12, 31)


def fiscal_year(day):
    return dt.date.fromisoformat(day).year


def eps_rng(lo, hi):
    """an EPS range: '2.80-2.85', a loss in parentheses ('(0.35)-(0.30)'), one figure for a point"""
    m = lambda x: f"({money(-x)})" if x < 0 else money(x)
    return m(lo) if lo == hi else f"{m(lo)}-{m(hi)}"


def rt_value(rt, k, y):
    """one rule-T value re-derived from the raw figures of the filing it comes from"""
    s, y0 = rt["raw"][rt["from"][k][y]], str(int(y) - 1)
    if k == "sales":
        return r2((s["rev_k"][y] / s["rev_k"][y0] - 1) * 100)
    if k == "op_margin":
        m = lambda t: s["opinc_k"][t] / s["rev_k"][t] * 100
        return r2((m(y) - m(y0)) * 100)
    if k == "occupancy":
        return r1((s["occ"][y] - s["occ"][y0]) * 100)
    if y in s.get(f"{k}_stated", {}):                      # the filing's own percentage (2001-2002)
        return s[f"{k}_stated"][y]
    num = s["net_rev_k"] if k == "ny" else s["ncc_k"]
    return r2((num[y] / s["apcd"][y] / (num[y0] / s["apcd"][y0]) - 1) * 100)


def rule_t(rt):
    """Rule T thresholds from the annual values: XBULL best, BULL median, BASE worst, BEAR one median-to-worst step beyond
    the worst; rounded half up to whole percent and to 10 bp. The values are first re-derived from the raw figures."""
    out = {}
    for k, (unit, lower) in RULE_T_KEYS.items():
        assert (rt[k]["unit"], rt[k]["lower_is_better"]) == (unit, lower), (k, "the fact sheet's unit or direction differs")
        assert rt[k]["values"] == {y: rt_value(rt, k, y) for y in rt["from"][k]}, (k, "values differ from the raw figures")
        v = sorted(rt[k]["values"].values())
        assert len(v) >= 2, (k, "rule T needs at least two annual values")
        n = len(v)
        med = v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
        worst, best = (v[-1], v[0]) if lower else (v[0], v[-1])
        r = lambda x: math.floor(x / unit + 0.5) * unit
        out[k] = (r(worst + (worst - med)), r(worst), r(med), r(best))
        assert tuple(rt[k]["thresholds"][s] for s in ("BEAR", "BASE", "BULL", "XBULL")) == out[k], (k, "stored thresholds differ")
    return out


def derived(r):
    """a quarter's or year's values from its raw figures (thousands; APCD in days; occupancy in percent)"""
    rv, rv0 = r["rev_k"], r["rev_prior_k"]
    # a print's Net Revenues by the company's own definition: from 2014 the releases exclude the divested Pullmantur businesses and
    # 'other initiative costs' and print the lines they exclude ('nr_x_k', 'nr_x_prior_k'; zero before 2014)
    nr = r.get("net_rev_k", rv - r.get("comm_k", 0) - r.get("onboard_k", 0) - r.get("nr_x_k", 0))
    nr0 = r.get("net_rev_prior_k", rv0 - r.get("comm_prior_k", 0) - r.get("onboard_prior_k", 0) - r.get("nr_x_prior_k", 0))
    ny, ny0 = nr * 1000 / r["apcd"], nr0 * 1000 / r["apcd_prior"]
    return rv, rv0, ny, ny0


def check_print(p):
    """Re-derive a print's values from its raw published figures (they must match), and check the derived Net Yields and Net
    Cruise Costs changes against the ones the release states (within the release's own rounding of its per-APCD figures)."""
    r = p["raw"]
    rv, rv0, ny, ny0 = derived(r)
    nc = r["opex_k"] + r["msa_k"] - r["comm_k"] - r["onboard_k"] - r.get("nc_x_k", 0)             # the company's exclusions, as for
    nc0 = r["opex_prior_k"] + r["msa_prior_k"] - r["comm_prior_k"] - r["onboard_prior_k"] - r.get("nc_x_prior_k", 0)   # Net Revenues
    ncc, ncc0 = nc * 1000 / r["apcd"], nc0 * 1000 / r["apcd_prior"]
    m, m0 = r["opinc_k"] / rv * 100, r["opinc_prior_k"] / rv0 * 100
    want = {"sales_b": round(rv / 1e6, 3), "sales_pct": r1((rv / rv0 - 1) * 100), "ny": r2(ny), "ny_prior": r2(ny0),
            "ny_pct": r1((ny / ny0 - 1) * 100), "ncc": r2(ncc), "ncc_prior": r2(ncc0), "ncc_pct": r1((ncc / ncc0 - 1) * 100),
            "capacity_pct": r1((r["apcd"] / r["apcd_prior"] - 1) * 100), "occupancy": r["occ"],
            "occupancy_bp": r1((r["occ"] - r["occ_prior"]) * 100), "op_margin": r2(m), "op_margin_bp": r1((m - m0) * 100),
            "diluted_shares_m": r["diluted_shares_k"] / 1000, "cash_b": round(r["cash_k"] / 1e6, 3)}
    for k, v in want.items():
        assert p[k] == v or abs(p[k] - v) < 1e-9, (p["quarter"], k, p[k], v)
    for k in ("ny", "ncc"):                # a change the release states as reported (from 2011 some state only constant currency)
        if p.get(f"{k}_stated_pct") is not None:
            assert abs(p[f"{k}_pct"] - p[f"{k}_stated_pct"]) <= 0.1, (p["quarter"], k, "stated")
    a = p.get("fy_actual")
    if a:
        ra = a["raw"]
        rv, rv0, ny, ny0 = derived(ra)
        nc, nc0 = ra["ncc_k"] * 1000 / ra["apcd"], ra["ncc_prior_k"] * 1000 / ra["apcd_prior"]
        want = {"revenue_usd_b": rv / 1e6, "op_margin": r2(ra["opinc_k"] / rv * 100), "sales_growth": r1((rv / rv0 - 1) * 100),
                "ny_pct": r2((ny / ny0 - 1) * 100), "ncc_pct": r2((nc / nc0 - 1) * 100), "occupancy": ra["occ"],
                "capacity_pct": r1((ra["apcd"] / ra["apcd_prior"] - 1) * 100), "other_expense_b": round(-ra["other_k"] / 1e6, 4),
                "cash_b": round(ra["cash_k"] / 1e6, 3), "fcf_b": round((ra["cfo_k"] - ra["capex_k"]) / 1e6, 3)}
        for k, v in want.items():
            assert a[k] == v or abs(a[k] - v) < 1e-9, (p["quarter"], "fy_actual", k, a[k], v)


def check_vintage(v):
    """Re-derive a vintage's last-year values from its raw figures."""
    r = v["vintage_raw"]
    rv, rv0, ny, ny0 = derived(r)
    nc, nc0 = r["ncc_k"] * 1000 / r["apcd"], r["ncc_prior_k"] * 1000 / r["apcd_prior"]
    want = {"prev_fy_op_margin": r2(r["opinc_k"] / rv * 100), "prev_fy_sales_growth": r1((rv / rv0 - 1) * 100),
            "prev_fy_ny_pct": r2((ny / ny0 - 1) * 100), "prev_fy_ncc_pct": r2((nc / nc0 - 1) * 100),
            "prev_fy_capacity_pct": r1((r["apcd"] / r["apcd_prior"] - 1) * 100), "other_expense_b": round(-r["other_k"] / 1e6, 4),
            "cash_b": round(r["cash_k"] / 1e6, 3), "fcf_b": round((r["cfo_k"] - r["capex_k"]) / 1e6, 3)}
    for k, x in want.items():
        assert v[k] == x or abs(v[k] - x) < 1e-9, (v["published"], k, v[k], x)
    last = max(v["revenue_usd_b"])
    assert abs(v["revenue_usd_b"][last] * 1e6 - rv) < 1e-3, (v["published"], "last year's revenue")


def usd_b(x):
    """a dollar amount in billions, the sign before the dollar sign"""
    return f"-${-x:.2f}B" if x < 0 else f"${x:.2f}B"


def net_rev(ny, cap):
    """the net revenue growth a Net Yields guide and a capacity guide imply (Net Revenues = Net Yields x APCD)"""
    return [r2(((1 + n / 100) * (1 + cap / 100) - 1) * 100) for n in ny]


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    # every price of the window on the AS_OF share basis: Yahoo's split-adjusted series times the splits after AS_OF
    chart = retro_tool.chart("RCL")
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat()
                    for v in chart.get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo_splits for s in facts.get("splits", [])), "a split's effective date must match the price data"
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
        if v["published"] <= as_of:
            check_vintage(v)
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        check_print(p)
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
    # no disruption theme in taxonomy_eras.json is live for a cruise company in 2008-2013; the builder refuses events until a
    # theme encoding is decided
    events = [e for e in facts["events"] if e["published"] <= as_of]
    if events:
        sys.exit(f"{as_of}: the RCL builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
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
                     prev_fy_sales_growth=a["sales_growth"], prev_fy_ny_pct=a["ny_pct"], prev_fy_ncc_pct=a["ncc_pct"],
                     prev_fy_occupancy=a["occupancy"], prev_fy_capacity_pct=a["capacity_pct"],
                     other_expense_b=a["other_expense_b"], other_expense_note=f'FY{y[2:]} other income (expense) ({p["source"]})',
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     cash_b=a["cash_b"], fcf_b=a["fcf_b"], fcf_label=a["fy_label"], groups=a["groups"],
                     groups_basis=f'{a["fy_label"]} revenues by type ({a["doc"]}; one reportable segment)',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    # a company figure for an earlier year of the history, first published in a later print ('restates': the Q2 2011 release's FY2009
    # $0.71 and FY2010 $2.37 after the interest expense revision), replaces it from that print until a 10-K vintage published after the
    # print carries the year (each year from the latest filing that reports it; the SHW rule)
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
    prev = (public[i - 1]["ny_pct"], public[i - 1]["quarter"]) if i > 0 else (h["prev_q_ny"], h["prev_q_label"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    cur_fy = max(eps_hist) + 1
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── guides for the current fiscal year, each field from the latest guide that states it ──
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    stated = lambda k: next((g for g in reversed(guides) if k in g), None)
    ge, gr = stated("eps_guide"), stated("fy_rev")
    qkey = lambda q: (int(q.split()[1]), int(q[1]))
    later = lambda q: qkey(q) > (latest["fy"], nq)                 # a next-quarter guide counts while its quarter is unreported
    gq = next((g for g in reversed(guides) if "q_guide" in g and later(g["q_guide"]["quarter"])), None)
    q = None
    if gq:                                    # each field of the next quarter's guide from the latest guide that states it
        q = {}
        for g in guides:
            if g.get("q_guide", {}).get("quarter") == gq["q_guide"]["quarter"]:
                q.update(g["q_guide"])
    if ge:
        eps_now = round(sum(ge["eps_guide"]) / 2, 3)
        eps_label = f"{fy_e} EPS, guide midpoint" if ge["eps_guide"][0] != ge["eps_guide"][1] else f"{fy_e} EPS, guided figure"
    else:                                    # no numeric EPS guide: the last full year's EPS stands (rollover rule)
        eps_now = eps_hist[cur_fy - 1]
        eps_label = f"{fy_e}: no numeric EPS guide yet, FY{(cur_fy - 1) % 100:02d}'s ${money(eps_now)} stands"
    fr = gr["fy_rev"] if gr else None
    has_q = q is not None and "ny" in q and "capacity" in q
    if has_q and "ny_cc" in q:               # method r2: the next-quarter guide on a constant-currency basis
        fwd, fwd_period = net_rev(q["ny_cc"], q["capacity"]), q["quarter"]
        fwd_label, fwd_short = f"{q['quarter']} net revenue guide at constant currency", f"{q['quarter'][:2]} cc guide"
        fwd_kind = (f"next-quarter guide at constant currency: Net Yields {pct_range(*q['ny_cc'])} on capacity {q['capacity']:+.1f}% "
                    "(Net Revenues = Net Yields x APCD)")
    elif fr and "ny_cc" in fr:               # no next-quarter guide at constant currency: the fiscal year's (the ACN fallback)
        fwd, fwd_period = net_rev(fr["ny_cc"], fr["capacity"]), fy_now
        fwd_label, fwd_short = f"{fy_now} net revenue guide at constant currency", f"{fy_now} cc guide"
        fwd_kind = (f"no next-quarter guide at constant currency: the {fy_now} guide, Net Yields {pct_range(*fr['ny_cc'])} on capacity "
                    f"{fr['capacity']:+.1f}% (Net Revenues = Net Yields x APCD)")
    elif has_q:                               # no guide at constant currency: the next quarter's as published
        fwd, fwd_period = net_rev(q["ny"], q["capacity"]), q["quarter"]
        fwd_label, fwd_short = f"{q['quarter']} net revenue guide", f"{q['quarter'][:2]} guide"
        fwd_kind = (f"next-quarter guide as published (none at constant currency): Net Yields {pct_range(*q['ny'])} on capacity "
                    f"{q['capacity']:+.1f}% (Net Revenues = Net Yields x APCD)")
    elif fr:                                  # ... else the fiscal year's as published
        fwd, fwd_period = net_rev(fr["ny"], fr["capacity"]), fy_now
        fwd_label, fwd_short = f"{fy_now} net revenue guide", f"{fy_now} guide"
        fwd_kind = (f"no next-quarter guide in numbers: the {fy_now} guide, Net Yields {pct_range(*fr['ny'])} on capacity "
                    f"{fr['capacity']:+.1f}% (Net Revenues = Net Yields x APCD)")
    else:                                     # no guide at all: the latest quarter's revenue growth as reported
        fwd, fwd_period = [latest["sales_pct"]] * 2, latest["quarter"]
        fwd_label, fwd_short = f"no {fy_now} guide in numbers, {latest['quarter']} revenues", f"{latest['quarter'][:2]} revenues"
        fwd_kind = f"no guide in numbers: {latest['quarter']} total revenue growth as reported"
    if fr:
        fy_basis = "ny_cc" if "ny_cc" in fr else "ny"
        fy_rev = net_rev(fr[fy_basis], fr["capacity"])
        fy_rev_label = f"{fy_now} net revenue guide{' at constant currency' if fy_basis == 'ny_cc' else ''}, applied to total revenues"
    else:
        fy_rev, fy_rev_label = fwd, f"{fwd_label}, applied to the year (no {fy_now} guide in numbers)"
    if guides:
        fyr = (([f"Net Yields {pct_range(*fr['ny'])}"] + ([f"{pct_range(*fr['ny_cc'])} at constant currency"] if "ny_cc" in fr else [])
                + [f"capacity {fr['capacity']:+.1f}%"]) if fr else [])
        bits = ([f"EPS ${eps_rng(*ge['eps_guide'])}" + (f" ({ge['eps_guide_note']})" if ge.get("eps_guide_note") else "")] if ge else []) + fyr + \
               ([gr["fy_display"]] if gr and gr.get("fy_display") else []) + \
               ([f"{q['quarter']}: " + ", ".join(
                   ([f"Net Yields {pct_range(*q['ny'])}"] if "ny" in q else []) +
                   ([f"{pct_range(*q['ny_cc'])} at constant currency"] if "ny_cc" in q else []) +
                   ([f"capacity {q['capacity']:+.1f}%"] if "capacity" in q else []) +
                   ([f"EPS ${eps_rng(*q['eps'])}"] if "eps" in q else []))] if q else []) + \
               ([guides[-1]["note"]] if guides[-1].get("note") else [])
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

    # ── era-dependent text, from facts only: no disruption theme has dated evidence on AS_OF ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
    key_tail = ("Demand follows the economies the ships sell into, by the company's own\n"
                "  account; the bear needs yields to fall faster than running costs can be cut.")
    theme_summary = "no disruption theme has dated evidence"
    cat3 = (f"(3) {fy_now} EPS guide ${eps_rng(*ge['eps_guide'])} ({ge['doc']})" if ge else
            f"(3) A numeric {fy_now} EPS guide — none yet")
    cat4 = (f"(4) Net Cruise Costs per APCD — {latest['ncc_pct']:+.1f}% in {latest['quarter']}: fuel and running costs "
            "against yields")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    # a print dated AS_OF meets AS_OF's close only if it was public before it: before the open, or by an 8-K accepted during
    # the session (the UNP 2014 rule)
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        rt = same_day[-1].get("release_time", "")
        assert "before the open" in rt or "during the session" in rt, (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the close")
        tag = (f"(day of the {same_day[-1]['quarter']} print, public before the open)" if "before the open" in rt else
               f"(day of the {same_day[-1]['quarter']} print, released during the session)")

    renames = [n for n in facts.get("company_names", []) if h["published"] < n["published"] <= as_of]
    company = renames[-1]["name"] if renames else h["company"]
    exchange = h["exchange"]
    groups = [tuple(g) for g in h["groups"]]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])] + [g["source"] for g in guides]
           + ([dividend_src] if dividend_src else []) + split_ids + [n["source"] for n in renames])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "W0", "published": as_of, "title": "Yahoo Finance daily prices, RCL and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/RCL/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "ny", "ny_pct", "ny_cc_pct", "ncc", "ncc_pct", "capacity_pct",
                   "occupancy", "occupancy_bp", "op_margin", "op_margin_bp", "eps_q", "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    volumes = (f"Net Yields: '{latest['ny_note']}'; Net Cruise Costs: '{latest['ncc_note']}'; capacity {latest['capacity_pct']:+.1f}%"
               + (f"; fuel: '{latest['fuel_note']}'" if latest["fuel_note"] else "")
               + (f"; EPS {latest['eps_note']}" if latest.get("eps_note") else ""))
    R = repr
    head = f'''#!/usr/bin/env python3
"""
RCL Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: RCL)  ·  {h["business_line"]}
Generated by retro/build_rcl.py from retro/facts/RCL.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "RCL"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); cruise-line signals")
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
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}{"; " + h["split_note"] if h.get("split_note") else ""}
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # total revenues, USD bn
SHARES_HIST   = {R({y: round(v, 3) for y, v in shares.items()})}   # diluted, millions
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # operating margin, {h["prev_fy_op_margin_note"]}
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
NET_INTEREST_B = {h["other_expense_b"]}   # {h["other_expense_note"]}, for the EPS check
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_NY         = {R(prev)}
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
GROUPS          = {R(groups)}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} Net Yields {h['prev_fy_ny_pct']:+.1f}% on capacity {h['prev_fy_capacity_pct']:+.1f}%, occupancy {h['prev_fy_occupancy']:.1f}%; {latest['quarter']} Net Yields {latest['ny_pct']:+.1f}%, occupancy {latest['occupancy']:.1f}%")}
BALANCE_TEXT    = {R(f"{h['fy_label']} year-end cash ${h['cash_b']:.3f}B, {h['fcf_label']} free cash flow {usd_b(h['fcf_b'])}, dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/RCL)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("RCL"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<34}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
