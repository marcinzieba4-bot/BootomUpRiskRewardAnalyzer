#!/usr/bin/env python3
"""
Build MAR retrospective models from the dated fact sheet (retro/facts/MAR.json).

The MAR sibling of build_rcl.py: the same frozen rules (retro method r2), the same weekly dates and the same market statistics,
with hotel signals (retro/templates/mar_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints, guides, dividends and splits whose 'published' (a split: 'applies') date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, on the AS_OF share basis (Yahoo's split-adjusted series
     times the splits after AS_OF: the 2006 two-for-one split and the 2009 stock dividends), from the 1998-03-27 spinoff on;
     Yahoo also books the 2011-11-21 spin-off of Marriott Vacations Worldwide as a 1.061 split, and that factor is undone
     ('distributions'), so every price is as traded,
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Marriott's fiscal year ends on the Friday nearest to December 31 (52 or 53 weeks; FY2002 and FY2008 had 53), and from FY2013 on
December 31 (a calendar year, quarters of calendar months; earlier periods not restated). Each earnings release
guides the next quarter and the year: diluted EPS (the company's figure excluding synthetic fuel and named one-offs), total fee
revenue (base management, franchise and incentive fees) in dollars, sometimes with its growth stated, and RevPAR in words and numbers.
The method r2 inputs map as follows (retro/README.md, "MAR"):
  - current-FY EPS: the fiscal-year EPS guide midpoint, each field from the latest guide that states it (the Q3 2009 release gives no
    fiscal-year EPS, so the Q2 2009 range stands),
  - forward revenue growth: the next-quarter total fee revenue guide as growth on the year-ago quarter's fees: the release's own
    percentage where it states one, else the dollar range against the year-ago quarter's fees from that quarter's own release (the
    AVGO rule); else the fiscal year's fee guide; else the latest quarter's fee growth,
  - guided margin step: none (the company guides house profit margins, a property-level measure, not its own margin); the margin
    signal takes the latest quarter's operating-margin change.
RevPAR guides, the outlook's other lines and its words are shown in the guide line and feed no input.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. Every MAR earnings release of 2007-2009 and of Q4 2009-Q1 2010 was accepted before the open;
from Q2 2010 every one was accepted after the close, so it is dated the next trading day (the AVGO rule).

Output goes to staging/retrospective/MAR until the series is added to the archive (--out archive/retrospective/MAR).

Usage
  python3 retro/build_mar.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_mar.py --weekly 2009-01-01 2009-12-31
  python3 retro/build_mar.py 2008-01-31
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/MAR/<AS_OF>
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
from build_unp import money, pct_range  # noqa: E402

FACTS = os.path.join(HERE, "facts", "MAR.json")
ENGINE = os.path.join(HERE, "templates", "mar_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "MAR")
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"revpar": (-27, -10, 6, 10), "fees": (-38, -12, 13, 19), "sales": (-14, -2, 11, 26),
                     "occupancy": (-1300, -670, -40, 140), "op_margin": (-880, -420, 40, 280)}
RULE_T_KEYS = {"revpar": (1, False), "fees": (1, False), "sales": (1, False), "occupancy": (10, False), "op_margin": (10, False)}
r1, r2 = (lambda x: round(x + 1e-12, 1)), (lambda x: round(x + 1e-12, 2))


def fiscal_year_end(n):
    """Marriott's fiscal year n ends on the Friday nearest to December 31 of year n; from 2013 on December 31 (the board's change
    to a calendar fiscal year, 8-K of 2012-05-08: fiscal 2013 began on December 29, 2012)."""
    d = dt.date(n, 12, 31)
    if n >= 2013:
        return d
    back = (d.weekday() - 4) % 7                 # days back to the previous Friday (0 if Dec 31 is a Friday)
    return d - dt.timedelta(days=back) if back <= 3 else d + dt.timedelta(days=7 - back)


def fiscal_year(day):
    d = dt.date.fromisoformat(day)
    return d.year if d <= fiscal_year_end(d.year) else d.year + 1


def eps_rng(lo, hi):
    """an EPS range: '1.88-1.90', a loss in parentheses, one figure for a point"""
    m = lambda x: f"({money(-x)})" if x < 0 else money(x)
    return m(lo) if lo == hi else f"{m(lo)}-{m(hi)}"


def rt_value(rt, k, y):
    """one rule-T value re-derived from the raw figures of the filing(s) it comes from"""
    s, y0 = rt["raw"][rt["from"][k][y]], str(int(y) - 1)
    sf = lambda key, t: rt["raw"][rt["sf_from"][t]][key][t] if t in rt["sf_from"] else 0
    if k == "revpar":
        return s["revpar"][y]
    if k == "occupancy":
        return r1(s["occ_pts"][y] * 100)
    if k == "fees":
        return r2((s["fees_m"][y] / s["fees_m"][y0] - 1) * 100)
    if k == "sales" and "sales_m" in s:                       # 1997-1999: each filing's own sales basis
        return r2((s["sales_m"][y] / s["sales_m"][y0] - 1) * 100)
    rev = lambda t: s["rev_m"][t] - sf("sf_rev_m", t)        # revenues excluding the synthetic fuel line
    if k == "sales":
        return r2((rev(y) / rev(y0) - 1) * 100)
    m = lambda t: (s["opinc_m"][t] - sf("sf_rev_m", t) + sf("sf_exp_m", t)) / rev(t) * 100
    return r2((m(y) - m(y0)) * 100)


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


def check_print(p):
    """Re-derive a print's values from its raw published figures (they must match)."""
    r = p["raw"]
    rv, rv0 = r["rev_total_m"] - r.get("sf_rev_m", 0), r["rev_total_prior_m"] - r.get("sf_rev_prior_m", 0)
    f, f0 = r["base_m"] + r["fran_m"] + r["inc_m"], r["base_prior_m"] + r["fran_prior_m"] + r["inc_prior_m"]
    m, m0 = r["opinc_m"] / rv * 100, r["opinc_prior_m"] / rv0 * 100
    want = {"sales_b": round(rv / 1000, 3), "sales_pct": r1((rv / rv0 - 1) * 100), "fees_m": f, "fees_prior_m": f0,
            "fees_pct": r1((f / f0 - 1) * 100), "op_margin": r2(m), "op_margin_bp": r1((m - m0) * 100),
            "occupancy_bp": r1(p["occupancy_pts"] * 100), "diluted_shares_m": r["diluted_shares_m"], "cash_b": round(r["cash_m"] / 1000, 3)}
    for k, v in want.items():
        assert p[k] == v or abs(p[k] - v) < 1e-9, (p["quarter"], k, p[k], v)
    a = p.get("fy_actual")
    if a:
        ra = a["raw"]
        want = {"revenue_usd_b": ra["rev_m"] / 1000, "op_margin": r2(ra["opinc_m"] / ra["rev_adj_m"] * 100),
                "sales_growth": r1((ra["rev_m"] / ra["rev_prior_m"] - 1) * 100), "fees_pct": r1((ra["fees_m"] / ra["fees_prior_m"] - 1) * 100),
                "other_expense_b": round((ra["opinc_m"] - ra["pretax_m"]) / 1000, 4), "tax_rate": round(ra["tax_m"] / ra["pretax_m"], 4),
                "cash_b": round(ra["cash_m"] / 1000, 3)}
        for k, v in want.items():
            assert a[k] == v or abs(a[k] - v) < 1e-9, (p["quarter"], "fy_actual", k, a[k], v)
        assert abs(sum(g[1] for g in a["groups"]) * 1000 - ra["rev_m"]) < 1e-6, (p["quarter"], "segments sum to the year's revenues")


def check_vintage(v):
    """Re-derive a vintage's last-year values from its raw figures."""
    r = v["vintage_raw"]
    want = {"prev_fy_op_margin": r2(r["opinc_m"] / r["rev_m"] * 100),
            "prev_fy_sales_growth": r1((r.get("rev_reported_m", r["rev_m"]) / r["rev_prior_m"] - 1) * 100),
            "prev_fy_fees_pct": r1((r["fees_m"] / r["fees_prior_m"] - 1) * 100), "other_expense_b": round((r["opinc_m"] - r["pretax_m"]) / 1000, 4),
            "cash_b": round(r["cash_m"] / 1000, 3), "fcf_b": round((r["cfo_m"] - r["capex_m"]) / 1000, 3)}
    for k, x in want.items():
        assert v[k] == x or abs(v[k] - x) < 1e-9, (v["published"], k, v[k], x)
    last = max(v["revenue_usd_b"])
    assert abs(v["revenue_usd_b"][last] * 1000 - r.get("rev_reported_m", r["rev_m"])) < 1e-6, (v["published"], "last year's revenue")
    assert abs(sum(g[1] for g in v["groups"]) * 1000 - r.get("rev_reported_m", r["rev_m"])) < 1e-6, (v["published"], "segments sum")


def on_basis(facts, as_of):
    """The fact sheet with every per-share fact on the AS_OF share basis: a split (or stock dividend) that applies on or before AS_OF
    divides per-share values published before its effective (ex-) date by its ratio and multiplies share counts by it. A split
    applies from the later of its ex-date and the first filing that states it ('applies'), so its effect never precedes the fact."""
    f = copy.deepcopy(facts)
    splits = [s for s in f.get("splits", []) if applies(s) <= as_of]
    k = lambda pub: math.prod(s["ratio"] for s in splits if pub < s["effective"])
    for v in f["history_vintages"]:
        ke = {y: k(v.get("eps_published", {}).get(y, v["published"])) for y in v["eps_normalized"]}
        ks = {y: k(v.get("shares_published", {}).get(y, v["published"])) for y in v["diluted_shares_m"]}
        v["eps_normalized"] = {y: e / ke[y] for y, e in v["eps_normalized"].items()}
        v["diluted_shares_m"] = {y: n * ks[y] for y, n in v["diluted_shares_m"].items()}
        v["dividend_annual"] /= k(v["published"])
        pub = lambda y: v.get("eps_published", {}).get(y, v["published"])
        notes = []
        for s in splits:
            restated = [y for y in sorted(ke) if pub(y) < s["effective"]]
            if restated:
                span = "" if len(restated) == len(ke) else f" on {restated[0]}-{restated[-1]}"
                kind = f"{s['ratio']:g}-for-1 split" if s["ratio"] >= 1.5 else f"{(s['ratio'] - 1):.5f}-share stock dividend"
                notes.append(f"per share ÷{s['ratio']:g} for the {kind} effective {s['effective']} ({s['source']}){span}")
        if notes:
            v["split_note"] = "; ".join(notes)
    for p in f["prints"]:
        r = k(p["published"])
        p["eps_q"], p["eps_q_prior"], p["diluted_shares_m"] = p["eps_q"] / r, p["eps_q_prior"] / r, p["diluted_shares_m"] * r
        if "fy_actual" in p:
            p["fy_actual"]["eps_normalized"] /= r
            p["fy_actual"]["diluted_shares_m"] *= r
    for g in f["guides"]:
        r = k(g["published"])
        if r != 1 and "eps_guide" in g:
            g["eps_guide_note"] = "; ".join(x for x in (g.get("eps_guide_note"), f"${money(g['eps_guide'][0])}-{money(g['eps_guide'][1])} before the stock dividends") if x)
            g["eps_guide"] = [e / r for e in g["eps_guide"]]
        if r != 1 and "eps" in g.get("q_guide", {}):
            g["q_guide"]["eps"] = [e / r for e in g["q_guide"]["eps"]]
    for d in f["dividends"]:
        d["quarterly"] /= k(d["published"])
    return f, [s["source"] for s in splits]


def applies(s):
    """the date a split starts to apply: its 'applies' date, else the later of its ex-date and its own publication date"""
    return s.get("applies") or max(s["effective"], s.get("published", s["effective"]))


def usd_b(x):
    """a dollar amount in billions, the sign before the dollar sign"""
    return f"-${-x:.2f}B" if x < 0 else f"${x:.2f}B"


def fee_growth(fg, as_of, sources):
    """a fee guide's growth: the release's own percentage where it states one, else the dollar range on the prior period's fees
    from that period's own filing (public by AS_OF); None where neither exists"""
    if fg.get("pct" if "pct" in fg else "fees_pct"):
        return list(fg.get("pct") or fg.get("fees_pct")), "stated"
    lvl, prior = fg.get("level_m") or fg.get("fees_m"), fg.get("prior_m")
    if lvl and prior and sources[fg["prior_source"]]["published"] <= as_of:
        return [r2((x / prior - 1) * 100) for x in lvl], "derived"
    return None, None


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    # every price of the window on the AS_OF share basis: Yahoo's split-adjusted series times the splits after AS_OF
    chart = retro_tool.chart("MAR")
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat()
                    for v in chart.get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo_splits for s in facts.get("splits", [])), "a split's effective date must match the price data"
    # a distribution (the 2011 spin-off of Marriott Vacations Worldwide) is not a split: Yahoo books it as one, so its factor is
    # undone for the days before its ex-date and every price stays as traded (the ex-date drop stays in the series)
    for x in facts.get("distributions", []):
        ev = [v for v in chart.get("events", {}).get("splits", {}).values()
              if dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat() == x["effective"]]
        assert len(ev) == 1 and ev[0]["numerator"] / ev[0]["denominator"] == x["yahoo_factor"], (x["effective"], "Yahoo's factor")
        if x["effective"] <= as_of:
            px = {d: (tuple(v * x["yahoo_factor"] for v in hlc) if d < x["effective"] else hlc) for d, hlc in px.items()}
    assert all(s["applies"] >= s["effective"] and s["applies"] >= facts["sources"][s["source"]]["published"]
               for s in facts["splits"] if "applies" in s), "a split applies from the later of its ex-date and its filing"
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
        if v["published"] <= as_of:
            check_vintage(v)
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        check_print(p)
    facts, split_ids = on_basis(facts, as_of)
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    reported = lambda h: {int(k) for k in h["eps_normalized"]}
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    prints = [p for p in facts["prints"] if p["published"] <= as_of and guide_fy(p) >= first_fy]
    # no disruption theme in taxonomy_eras.json is live for a hotel company in 2008-2009; the builder refuses events until a theme
    # encoding is decided
    events = [e for e in facts["events"] if e["published"] <= as_of]
    if events:
        sys.exit(f"{as_of}: the MAR builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is public yet")
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage
    h = {**h, "extended": ""}
    for p in prints:
        a = p.get("fy_actual")
        if a and a["fy"] not in reported(h):                           # the 10-K vintage, once out, wins
            y = str(a["fy"])
            h.update(fy_label=a["fy_label"], eps_normalized={**h["eps_normalized"], y: a["eps_normalized"]},
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]},
                     diluted_shares_m={**h["diluted_shares_m"], y: a["diluted_shares_m"]},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_op_margin=a["op_margin"], prev_fy_op_margin_note=a["op_margin_note"],
                     prev_fy_sales_growth=a["sales_growth"], prev_fy_fees_pct=a["fees_pct"],
                     prev_fy_revpar_pct=a["revpar_pct"], prev_fy_occupancy=a["occupancy"], prev_fy_occ_pts=a["occupancy_pts"],
                     other_expense_b=a["other_expense_b"], other_note=f'{a["fy_label"]} operating income less income before taxes ({p["source"]})',
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})', cash_b=a["cash_b"], cash_note=f'cash balances at year-end ({p["source"]})',
                     groups=a["groups"], groups_basis=f'{a["fy_label"]} revenues by segment ({a["doc"]})',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    latest = prints[-1]
    # the previous quarter is the print published just before the latest one; before the first print, the vintage names it
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    i = public.index(latest)
    prev = (public[i - 1]["revpar_pct"], public[i - 1]["quarter"]) if i > 0 else (h["prev_q_revpar"], h["prev_q_label"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── guides for the current fiscal year, each field from the latest guide that states it ──
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    stated = lambda k: next((g for g in reversed(guides) if k in g), None)
    ge, gf, gd, gw, gn = stated("eps_guide"), stated("fy_fees"), stated("fy_display"), stated("words"), stated("note")
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
        eps_now = round(sum(ge["eps_guide"]) / 2, 4)
        eps_label = f"{fy_e} EPS, guide midpoint" if ge["eps_guide"][0] != ge["eps_guide"][1] else f"{fy_e} EPS, guided figure"
    else:                                    # no numeric EPS guide: the last full year's EPS stands (rollover rule)
        eps_now = eps_hist[last_fy]
        eps_label = f"{fy_e}: no numeric EPS guide yet, FY{last_fy % 100:02d}'s ${money(eps_now)} stands"
    qg, qbasis = fee_growth(q, as_of, facts["sources"]) if q else (None, None)
    fg, fbasis = fee_growth(gf["fy_fees"], as_of, facts["sources"]) if gf else (None, None)
    if qg:                                    # method r2: the next-quarter revenue guide (total fee revenue)
        fwd, fwd_period = qg, q["quarter"]
        fwd_label, fwd_short = f"{q['quarter']} fee revenue guide", f"{q['quarter'][:2]} fee guide"
        lvl = f"${q['fees_m'][0]:,}M-{q['fees_m'][1]:,}M" if "fees_m" in q else None
        fwd_kind = (f"next-quarter total fee revenue guide, {pct_range(*qg)} as the release states it" + (f" ({lvl})" if lvl else "")
                    if qbasis == "stated" else
                    f"next-quarter total fee revenue guide, {lvl} against {q['prior_label']} fees of ${q['prior_m']:,}M ({q['prior_source']})")
    elif fg:                                  # no next-quarter fee guide: the fiscal year's (the ACN fallback)
        fwd, fwd_period = fg, fy_now
        fwd_label, fwd_short = f"{fy_now} fee revenue guide", f"{fy_now} fee guide"
        fwd_kind = f"no next-quarter fee guide: the {fy_now} total fee revenue guide, {pct_range(*fg)}"
    else:                                     # no guide at all: the latest quarter's fee growth as reported
        fwd, fwd_period = [latest["fees_pct"]] * 2, latest["quarter"]
        fwd_label, fwd_short = f"no {fy_now} fee guide, {latest['quarter']} fees", f"{latest['quarter'][:2]} fees"
        fwd_kind = f"no fee guide in numbers: {latest['quarter']} total fee growth as reported"
    if fg:
        fy_rev, fy_rev_label = fg, f"{fy_now} total fee revenue guide, applied to total revenues"
    else:
        fy_rev, fy_rev_label = fwd, f"{fwd_label}, applied to the year (no {fy_now} fee guide in numbers)"
    if guides:
        fees_txt = None
        if gf:
            lv = gf["fy_fees"]["level_m"]
            fees_txt = (f"fees ${lv[0]:,}M-{lv[1]:,}M" if lv else "fees") + (f" ({pct_range(*fg)})" if fg else "")
        bits = ([f"EPS ${eps_rng(*ge['eps_guide'])}" + (f" ({ge['eps_guide_note']})" if ge.get("eps_guide_note") else "")] if ge else []) + \
               ([fees_txt] if fees_txt else []) + ([gd["fy_display"]] if gd else []) + \
               ([f"{q['quarter']}: " + ", ".join(
                   ([f"fees ${q['fees_m'][0]:,}M-{q['fees_m'][1]:,}M"] if "fees_m" in q else []) +
                   ([f"fees {pct_range(*qg)}"] if qg else []) +
                   ([f"EPS ${eps_rng(*q['eps'])}"] if "eps" in q else []) +
                   ([f"RevPAR {q['revpar']}"] if "revpar" in q else []))] if q else []) + \
               ([gn["note"]] if gn else []) + ([f"in words: '{gw['words']}'"] if gw else [])
        guide_text = f"{fy_now} guide ({', '.join(dict.fromkeys(g['doc'] for g in guides))}): " + "; ".join(bits)
    else:
        guide_text = f"{fy_now}: no guide yet"
    margin_guided = False                          # no margin guide in numbers: no guided step
    fy_margin_base = h["prev_fy_op_margin"]

    # ── dividend: the latest declared cash rate ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts["dividends"] if d["published"] <= as_of]
    divs.append((h["published"], h["dividend_annual"], h["dividend_note"], None))
    _, dividend, dividend_note, dividend_src = max(divs, key=lambda x: x[0])

    # ── market statistics, prices truncated at AS_OF, from the spinoff on ──
    days = sorted(d for d in px if d <= as_of and d >= h["pe_window_start"])
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
    window = [d for d in days if d > minus_years(as_of, 10)]
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
    key_tail = ("Fees follow the hotels' revenues and profits through the economy, by the\n"
                "  company's own account; the bear needs incentive fees to vanish faster than units grow.")
    theme_summary = "no disruption theme has dated evidence"
    cat3 = (f"(3) {fy_now} EPS guide ${eps_rng(*ge['eps_guide'])} ({ge['doc']})" if ge else f"(3) A numeric {fy_now} EPS guide — none yet")
    cat4 = f"(4) Total fee revenue — {latest['fees_pct']:+.1f}% in {latest['quarter']}: incentive fees against unit growth"

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        rt = same_day[-1].get("release_time", "")
        assert "before the open" in rt or "during the session" in rt, (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the close")
        tag = (f"(day of the {same_day[-1]['quarter']} print, public before the open)" if "before the open" in rt else
               f"(day of the {same_day[-1]['quarter']} print, released during the session)")

    renames = [n for n in facts.get("company_names", []) if h["published"] < n["published"] <= as_of]
    company = renames[-1]["name"] if renames else h["company"]
    # a listing moved to another exchange counts from its effective date (the PEP 2017 encoding; display only)
    listing = [x for x in facts.get("listings", []) if x["published"] <= as_of and x["effective"] <= as_of]
    exchange = listing[-1]["exchange"] if listing else h["exchange"]
    groups = [tuple(g) for g in h["groups"]]
    qprior = [q["prior_source"]] if q and qbasis == "derived" else []
    fprior = [gf["fy_fees"]["prior_source"]] if gf and fbasis == "derived" else []
    ids = (list(h["sources"]) + [p["source"] for p in prints] + qprior + fprior
           + [g["source"] for g in guides] + ([dividend_src] if dividend_src else []) + split_ids + [n["source"] for n in renames]
           + [i for x in facts.get("distributions", []) if x["effective"] <= as_of for i in (x["announced"], x["source"])]
           + [x["source"] for x in listing])
    sources = [dict(id=i, **{k: v for k, v in facts["sources"][i].items() if k != "accepted"}) for i in dict.fromkeys(ids)]
    sources.append({"id": "W0", "published": as_of, "title": "Yahoo Finance daily prices, MAR and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/MAR/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "fees_m", "fees_pct", "revpar_pct", "occupancy", "occupancy_bp",
                   "op_margin", "op_margin_bp", "eps_q", "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    volumes = (f"'{latest['ww_revpar_note']}'; EPS {latest['eps_note']}; {latest['quarter']} basis: {latest['basis_note']}")
    R = repr
    head = f'''#!/usr/bin/env python3
"""
MAR Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: MAR)  ·  {h["business_line"]}
Generated by retro/build_mar.py from retro/facts/MAR.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "MAR"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); hotel signals")
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
WINDOW_LABEL    = {R(window_label)}   # P/E window: {window[0]} .. AS_OF (from {h["pe_window_note"]})
YEARLY_MIN_PE   = {R(yearly)}   # (calendar year, lowest P/E, date)
VOL_ANNUAL_PCT  = {vol:.3f}   # 1-yr realized, daily log returns
VOL_BETA        = {beta:.2f}    # 1-yr beta vs S&P 500
VOL_52W_LOW     = {low52:.2f}
VOL_52W_HIGH    = {high52:.2f}
REF_LOW         = {px[ref][2]:.2f}   # lowest close of the last 52 weeks, {ref}
REF_LOW_LABEL   = {R(MONTHS[int(ref[5:7]) - 1])}

# ── FACTS: company history ({", ".join(h["sources"])}, vintage {h["published"]}{h["extended"]}) ──
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}{"; " + h["split_note"] if h.get("split_note") else ""}
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # revenues excluding synthetic fuel, USD bn
SHARES_HIST   = {R({y: round(v, 3) for y, v in shares.items()})}   # diluted, millions
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # operating margin, {h["prev_fy_op_margin_note"]}
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
NET_INTEREST_B = {h["other_expense_b"]}   # {h["other_note"]}, for the EPS check
CONS_DIVIDEND = {dividend:.4f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_REVPAR     = {R(prev)}
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
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} North American RevPAR {h['prev_fy_revpar_pct']:+.1f}%, occupancy {h['prev_fy_occupancy']:.1f}%, fees {h['prev_fy_fees_pct']:+.1f}%; {latest['quarter']} RevPAR {latest['revpar_pct']:+.1f}%, occupancy {latest['occupancy']:.1f}%")}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/MAR)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("MAR"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<34}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
