#!/usr/bin/env python3
"""
Build SHW retrospective models from the dated fact sheet (retro/facts/SHW.json).

The SHW sibling of build_low.py and build_xom.py: the same frozen rules (retro method r2), the same weekly dates and the same
market statistics, with paint and coatings signals (retro/templates/shw_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints, guides and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, on the AS_OF share basis (Yahoo's split-adjusted
     series times the splits after AS_OF: the three-for-one split of 2021-04-01 for every date before it; the 1997 split
     precedes every per-share fact in the fact sheet),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Sherwin-Williams' fiscal year is the calendar year. Each earnings release (and an outlook 8-K between releases) guides the
next quarter and the fiscal year: diluted EPS ranges in numbers (from Q1 2016 the company's figure excluding the Valspar acquisition
costs, as published beside GAAP); net sales in numbers in some releases (Q2-Q3 2007, most of 2009 and 2011, the first two of 2012, every
one from Q1 2013 to Q2 2015), otherwise in words. Guides are therefore their own dated list, as for LOW, and each field comes from the latest guide for the
current fiscal year that states it. The method r2 inputs map as follows (retro/README.md, "SHW"):
  - current-FY EPS: the fiscal-year EPS guide midpoint (no numeric EPS guide: the last full year's EPS stands),
  - forward revenue growth: the next-quarter net sales guide for a quarter not yet reported (none in numbers: the fiscal-year
    net sales guide; none either: the latest quarter's net sales growth excluding the currency effect the release states, the
    NKE and PEP rule, or as reported when the release states none),
  - guided margin step: none (no margin guide in numbers); the margin signal takes the latest quarter's pre-tax margin change.
Words ('fy_words', a quarter's 'words') are shown in the guide line and feed no input (the UNP 2016 rule). A later print may publish
an earlier year's company figure on a new basis ('restates': the Q1 2017 release's FY2016 $12.85); it replaces the year from that print
until a 10-K vintage published after it carries the year (retro/README.md, "SHW 2015-2017"). A guide may withdraw named fields of its
year ('withdrawn': the Q1 2020 release's FY2020 net sales range), which voids them in every earlier guide for that year (the AAPL and LOW
2020 rule; retro/README.md, "SHW 2018-2020").

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release,
where it is the first trading day after it. The earnings 8-Ks of 2007-2020 were accepted before the open or during the session on the
release day; a release on the week's last trading day (Thursday 2011-04-21 and 2014-04-17, before Good Friday; Friday 2013-10-25) counts
for that close, by an 8-K accepted before the open or during the session (the UNP 2014 rule).

Output goes to staging/retrospective/SHW until the series is added to the archive (--out archive/retrospective/SHW).

Usage
  python3 retro/build_shw.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_shw.py --weekly 2009-01-05 2011-12-31
  python3 retro/build_shw.py --weekly 2012-01-02 2014-12-31
  python3 retro/build_shw.py --weekly 2015-01-05 2017-12-31
  python3 retro/build_shw.py --weekly 2018-01-01 2020-12-31
  python3 retro/build_shw.py 2008-01-30
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/SHW/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "SHW.json")
ENGINE = os.path.join(HERE, "templates", "shw_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "SHW")
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"comps": (-7, -1, 4, 14), "gross_margin": (-290, -130, 30, 180), "sales": (-10, -3, 4, 18),
                     "consumer": (-20, -9, 2, 21), "pretax_margin": (-220, -110, 0, 160)}
RULE_T_KEYS = {"comps": (1, False), "gross_margin": (10, False), "sales": (1, False), "consumer": (1, False),
               "pretax_margin": (10, False)}           # (rounding unit, lower is better)


def fiscal_year_end(n):
    """Sherwin-Williams' fiscal year n is the calendar year n."""
    return dt.date(n, 12, 31)


def fiscal_year(day):
    return dt.date.fromisoformat(day).year


def eps_rng(lo, hi):
    """an EPS range: '4.70-4.75', a loss in parentheses ('(0.05)-0.15')"""
    m = lambda x: f"({money(-x)})" if x < 0 else money(x)
    return m(lo) if lo == hi else f"{m(lo)}-{m(hi)}"


def rule_t(rt):
    """Rule T thresholds from the annual values: XBULL best, BULL median, BASE worst, BEAR one median-to-worst step beyond
    the worst; rounded half up to whole percent and to 10 bp."""
    out = {}
    for k, (unit, lower) in RULE_T_KEYS.items():
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


def check_print(p):
    """Re-derive a print's growth, margins and local-currency growth from its raw published figures (they must match)."""
    r = p["raw"]
    m, m0 = (r["ns_k"] - r["cogs_k"]) / r["ns_k"] * 100, (r["ns_prior_k"] - r["cogs_prior_k"]) / r["ns_prior_k"] * 100
    t, t0 = r["pretax_k"] / r["ns_k"] * 100, r["pretax_prior_k"] / r["ns_prior_k"] * 100
    sales_pct = round((r["ns_k"] / r["ns_prior_k"] - 1) * 100, 1)
    want = {"sales_b": round(r["ns_k"] / 1e6, 3), "sales_pct": sales_pct, "gross_margin": round(m, 2),
            "gross_margin_bp": round((m - m0) * 100, 1), "pretax_margin": round(t, 2), "pretax_margin_bp": round((t - t0) * 100, 1),
            "diluted_shares_m": r["diluted_shares"] / 1e6,
            "lc_pct": round(sales_pct - p["currency_pp"], 1) if p["currency_pp"] is not None else None}
    for k, v in want.items():
        assert p[k] == v or (v is not None and abs(p[k] - v) < 1e-9), (p["quarter"], k, p[k], v)


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    # every price of the window on the AS_OF share basis: Yahoo's split-adjusted series times the splits after AS_OF
    chart = retro_tool.chart("SHW")
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
    # no disruption theme in taxonomy_eras.json is live for a paint and coatings maker in 2008 (ECOMMERCE, scoped to physical
    # retail, from 2015-01-01); the builder refuses events until a theme encoding is decided
    events = [e for e in facts["events"] if e["published"] <= as_of]
    if events:
        sys.exit(f"{as_of}: the SHW builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
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
                     prev_fy_pretax_margin=a["pretax_margin"], prev_fy_pretax_margin_note=a["pretax_margin_note"],
                     prev_fy_gross_margin=a["gross_margin"], prev_fy_sales_growth=a["sales_growth"],
                     prev_fy_comps=a["comps_pct"], prev_fy_consumer_pct=a["consumer_pct"], prev_fy_stores=a["stores"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    # a company figure for an earlier year of the history, first published in a later print ('restates': the Q1 2017 release's FY2016
    # $12.85 excluding only the Valspar acquisition costs, the basis of its FY2017 guide), replaces it from that print until a 10-K
    # vintage published after the print carries the year (each year from the latest filing that reports it; the XOM 'restates')
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
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── guides for the current fiscal year, each field from the latest guide that states it ──
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    # a guide may withdraw named fields of its year ('withdrawn': the Q1 2020 release replaces the FY2020 net sales range of +2% to 4%
    # with words and says the range no longer holds, the AAPL 2020-02-17 and LOW 2020 rule): the field is void in every earlier guide
    # for that year, so only a guide published on or after the withdrawal can state it again
    void = {}
    for g in guides:
        for k in g.get("withdrawn", []):
            void[k] = g["published"]
    stated = lambda k: next((g for g in reversed(guides) if k in g and g["published"] >= void.get(k, "")), None)
    ge, gr, gw = stated("eps_guide"), stated("rev_guide"), stated("fy_words")
    qkey = lambda q: (int(q.split()[1]), int(q[1]))
    later = lambda q: qkey(q) > (latest["fy"], nq)                 # a next-quarter guide counts while its quarter is unreported
    gq = next((g for g in reversed(guides) if "q_guide" in g and later(g["q_guide"]["quarter"])), None)
    # each field of the next quarter's guide from the latest guide that states it for that quarter (an outlook 8-K that updates only
    # the quarter's EPS, 2012-04-09, leaves the release's net sales range standing)
    q = None
    if gq:
        q = {}
        for g in guides:
            if g.get("q_guide", {}).get("quarter") == gq["q_guide"]["quarter"]:
                q.update(g["q_guide"])
    if ge:
        eps_now = round(sum(ge["eps_guide"]) / 2, 3)
        eps_label = f"{fy_e} EPS, guide midpoint"
    else:                                    # no numeric EPS guide: the last full year's EPS stands (rollover rule)
        eps_now = eps_hist[cur_fy - 1]
        eps_label = f"{fy_e}: no numeric EPS guide yet, FY{(cur_fy - 1) % 100:02d}'s ${money(eps_now)} stands"
    if q and "sales" in q:                   # method r2: the next-quarter net sales guide
        fwd, fwd_label, fwd_short, fwd_period = q["sales"], f"{q['quarter']} net sales guide", f"{q['quarter'][:2]} guide", q["quarter"]
        fwd_kind = "next-quarter net sales guide"
    elif gr:                                 # no next-quarter guide in numbers: the fiscal-year net sales guide
        fwd, fwd_label, fwd_short, fwd_period = gr["rev_guide"], f"{fy_now} net sales guide", f"{fy_now} guide", fy_now
        fwd_kind = "fiscal-year net sales guide (no next-quarter guide in numbers)"
    elif latest["lc_pct"] is not None:       # no net sales guide in numbers: the latest quarter excluding currency (NKE, PEP)
        fwd = [latest["lc_pct"]] * 2
        fwd_label = f"no {fy_now} net sales guide in numbers, {latest['quarter']} net sales ex-currency"
        fwd_short, fwd_period = f"{latest['quarter'][:2]} ex-FX", latest["quarter"]
        cx = latest["currency_pp"]
        fwd_kind = (f"no net sales guide in numbers: {latest['quarter']} growth {latest['sales_pct']:+.1f}% "
                    + (f"less the {cx:.1f}pp currency effect the release states" if cx >= 0 else
                       f"plus the {-cx:.1f}pp currency drag the release states"))
    else:                                    # ... as reported when the release states no currency effect
        fwd = [latest["sales_pct"]] * 2
        fwd_label = f"no {fy_now} net sales guide in numbers, {latest['quarter']} net sales"
        fwd_short, fwd_period = f"{latest['quarter'][:2]} sales", latest["quarter"]
        fwd_kind = f"no net sales guide in numbers: {latest['quarter']} growth as reported (no currency effect stated)"
    fy_rev = gr["rev_guide"] if gr else fwd
    fy_rev_label = f"{fy_now} net sales guide" if gr else f"{fwd_label}, applied to the year (no {fy_now} net sales guide in numbers)"
    if guides:
        bits = ([f"EPS ${eps_rng(*ge['eps_guide'])}" + (f" ({ge['eps_guide_note']})" if ge.get("eps_guide_note") else "")] if ge else []) + \
               ([f"net sales {pct_range(*gr['rev_guide'])}"] if gr else []) + \
               ([f"net sales in words: '{gw['fy_words']}'"] if gw and (not gr or gw["published"] > gr["published"]) else []) + \
               ([f"{q['quarter']}: " + ", ".join(
                   ([f"net sales {pct_range(*q['sales'])}"] if "sales" in q else []) +
                   ([f"net sales in words: '{q['words']}'"] if "words" in q else []) +
                   ([f"EPS ${eps_rng(*q['eps'])}"] if "eps" in q else []))] if q else []) + \
               ([gq["note"]] if gq and gq.get("note") else [])
        guide_text = f"{fy_now} guide ({', '.join(dict.fromkeys(g['doc'] for g in guides))}): " + "; ".join(bits)
    else:
        guide_text = f"{fy_now}: no guide yet"
    margin_guided = False                          # no margin guide in numbers: no guided step
    fy_margin_base = h["prev_fy_pretax_margin"]

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
    key_tail = ("Housing drives demand, by the company's own account; the bear needs raw\n"
                "  material costs to stay up while volumes fall.")
    theme_summary = "no disruption theme has dated evidence"
    cat3 = (f"(3) {fy_now} EPS guide ${eps_rng(*ge['eps_guide'])} ({ge['doc']})" if ge else
            f"(3) A numeric {fy_now} EPS guide — none yet")
    cat4 = (f"(4) Pre-tax margin — {latest['pretax_margin']:.2f}% in {latest['quarter']} ({latest['pretax_margin_bp']:+.1f}bp): "
            "where store and selling costs deleverage on falling comps")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    # a print dated AS_OF meets AS_OF's close only if it was public before it: before the open, or (a release on the Thursday
    # before Good Friday, when no trading day followed it in its week) by an 8-K accepted during the session (the UNP 2014 rule)
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        rt = same_day[-1].get("release_time", "")
        assert "before the open" in rt or "before the close" in rt, (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the close")
        tag = (f"(day of the {same_day[-1]['quarter']} print, public before the open)" if "before the open" in rt else
               f"(day of the {same_day[-1]['quarter']} print, released during the session)")

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
           + [p["source"] for p in public if p.get("renames")])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "W0", "published": as_of, "title": "Yahoo Finance daily prices, SHW and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/SHW/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "lc_pct", "comps_pct", "consumer_pct", "gross_margin",
                   "gross_margin_bp", "pretax_margin", "pretax_margin_bp", "eps_q", "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    eps_note = f"; EPS {latest['eps_note']}" if latest.get("eps_note") else ""
    fx_txt = (f"currency {latest['currency_pp']:+.1f}pp ('{latest['currency_note']}')" if latest["currency_pp"] is not None
              else latest["currency_note"])
    volumes = (f"Comparable-store sales: '{latest['comps_note']}'; Consumer Group: '{latest['consumer_note']}'; {fx_txt}; "
               f"{latest['acq_note']}{eps_note}")
    R = repr
    head = f'''#!/usr/bin/env python3
"""
SHW Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: SHW)  ·  {h["business_line"]}
Generated by retro/build_shw.py from retro/facts/SHW.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "SHW"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); paint and coatings signals")
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
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # net sales, USD bn
SHARES_HIST   = {R({y: round(v, 3) for y, v in shares.items()})}   # diluted, millions
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_pretax_margin"]}   # pre-tax margin, {h["prev_fy_pretax_margin_note"]}
CHECK_PRETAX_MARGIN = {h["prev_fy_pretax_margin"]}   # the same, for the EPS check
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
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
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} net sales {h['prev_fy_sales_growth']:+.1f}% on Paint Stores comps {h['prev_fy_comps']:+.1f}%, {h['prev_fy_stores']:,} paint stores; {latest['quarter'].split()[0]} gross margin {latest['gross_margin']:.2f}% ({latest['gross_margin_bp']:+.1f}bp)")}
BALANCE_TEXT    = {R(f"{h['fy_label']} year-end cash ${h['cash_b']:.3f}B, {h['fcf_label']} free cash flow ${h['fcf_b']:.2f}B, dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/SHW)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("SHW"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<34}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
