#!/usr/bin/env python3
"""
Build MSFT retrospective models from the dated fact sheet (retro/facts/MSFT.json).

The MSFT sibling of build_pep.py: the same frozen rules (retro method r2), the same weekly dates and the same market
statistics, with software signals (retro/templates/msft_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints, guides and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, on the AS_OF share basis (Microsoft last split
     on 2003-02-18, so for every date from then Yahoo's split-adjusted series is the price as traded; the split restates the
     per-share facts published before it),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Microsoft's fiscal year ends on June 30. Every release of the period guides the next quarter and the fiscal year in numbers:
revenue, operating income and diluted EPS ranges, in dollars. The method r2 inputs map with the rules decided before any MSFT
date was built or scored (retro/README.md, "MSFT"):
  - current-FY EPS: the midpoint of the latest fiscal-year EPS range for the current year (the ACN rule); a release that guides
    only the next quarter leaves the last range standing (the ACN Q3 FY08 rule); before a year's first range, the last full
    year's EPS stands (the rollover rule),
  - forward revenue growth: the latest next-quarter revenue range, read as growth on the same quarter a year earlier from its
    own filing, rounded to 0.1, as published (the AAPL rule; the 2011 rule),
  - guided margin step: none (the operating income ranges are dollar levels, display only: no margin is derived from two guided
    figures); the margin signal uses the latest quarter's change.
EPS is diluted EPS before the cumulative effect of accounting changes, each year from the latest 10-K that reports it, and a
company-published figure excluding one-offs only replaces it (the ACN rule). The technology guarantee and pre-shipment
deferrals of fiscal 2007 (revenue moved from the second quarter to the third) are revenue recognition, not a one-off (the AAPL
Q4 FY08 rule), so the quarters stay as reported and the company's "as adjusted" figures go in the notes.

From the Q2 FY09 release Microsoft guides only operating expenses (display only), and from the Q1 FY14 release only on its
conference call, which is not a filing; with no next-quarter revenue guide, BASE takes the latest quarter's revenue growth
excluding currency (a total effect stated only in dollars is taken off the quarter's revenue; retro/README.md, "MSFT 2012-2014").
A Q4 print may restate an earlier year's EPS to a company figure excluding only one-offs first published in it ('restates').
CLOUD (live from 2012-10-30 in retro/taxonomy_eras.json) joins the watch list from its live date with the latest 10-K's own words.
From the Q1 FY16 release the company's non-GAAP figures also remove the Windows 10 revenue deferrals (revenue recognition), so GAAP
stands. The 8-K of 2017-08-03 re-presents FY2016-FY2017 under the new revenue and lease standards: a vintage of its own that keeps
the FY2017 10-K's wording and CLOUD event ('text_published'); the Q1 FY18 print has no year-ago unearned revenue on the new basis in
any filing, so it is not comparable ('unearned_prior_m' null: the engine's not-reported path; retro/README.md, "MSFT 2015-2017").

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings
release, where it is the first trading day after it. Most Microsoft earnings 8-Ks were accepted after the close (the webcast
at 2:30 p.m. Pacific), so a print is dated the next trading day; a Friday print is that week's date and meets its close, public
before the open (release_time; the AAPL 2011 and AVGO 2021-2023 rules); a print dated earlier in the week dates its week the next
trading day (Q2 FY09 and Q2 FY11 were public on a Thursday, Q4 FY14-FY16 on a Wednesday, Q2 FY15 on a Tuesday).

Output goes to staging/retrospective/MSFT until the series is added to the archive (--out archive/retrospective/MSFT).

Usage
  python3 retro/build_msft.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_msft.py 2008-01-25
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/MSFT/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "MSFT.json")
ENGINE = os.path.join(HERE, "templates", "msft_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "MSFT")
# the guide fields this builder has an encoding for: 'eps_guide' (a fiscal-year diluted EPS range: the current-FY EPS input),
# 'q_guide' (the next quarter's ranges: its 'sales_usd_b' against 'prior_sales_b' is BASE and the growth factor), the fiscal-year
# revenue range (the segment bridge's total, display only), the operating income ranges (display only), the fiscal-year operating
# expense ranges of 2009-2011 ('opex_guide_usd_b', display only) and a withdrawal ('withdrawn' with its 'quote': it voids every earlier
# guide for its fiscal year, and the no-guide rules apply; the LOW 2020 rule). Any other field needs its encoding first
GUIDE_KEYS = {"fy", "published", "source", "doc", "eps_guide", "rev_guide_usd_b", "op_income_guide_usd_b", "q_guide", "note",
              "opex_guide_usd_b", "withdrawn", "quote"}
Q_GUIDE_KEYS = {"quarter", "sales_usd_b", "op_income_usd_b", "eps", "eps_words", "prior_sales_b", "prior_source", "prior_label"}
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"unearned": (-35, -9, 17, 104), "gross_margin": (-1020, -460, 90, 270), "revenue": (2, 8, 14, 29),
                     "receivables_gap": (41, 29, 16, -12), "op_margin": (-1000, -510, -30, 1210)}
RULE_T_KEYS = {"unearned": (1, False), "gross_margin": (10, False), "revenue": (1, False), "receivables_gap": (1, True),
               "op_margin": (10, False)}           # (rounding unit, lower is better)


def fiscal_year_end(n):
    """Microsoft's fiscal year n ends on June 30 of year n."""
    return dt.date(n, 6, 30)


def fiscal_year(day):
    """The fiscal year a calendar day belongs to."""
    d = dt.date.fromisoformat(day)
    return d.year + 1 if d.month >= 7 else d.year


def rule_t(rt):
    """Rule T thresholds from the ten annual values: XBULL best, BULL median, BASE worst, BEAR one median-to-worst step beyond
    the worst; rounded half up to whole percent or points and to 10 bp."""
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
    """Re-derive a print's margins, growth and gaps from its raw published figures (they must match the fact sheet)."""
    r = p["raw"]
    pct = lambda a, b: (b / a - 1) * 100
    r2 = lambda x: round(x + 0.0, 2)
    gm, gm0 = (r["sales_m"] - r["cogs_m"]) / r["sales_m"] * 100, (r["sales_prior_m"] - r["cogs_prior_m"]) / r["sales_prior_m"] * 100
    om, om0 = r["op_m"] / r["sales_m"] * 100, r["op_prior_m"] / r["sales_prior_m"] * 100
    sales = pct(r["sales_prior_m"], r["sales_m"])
    ar = pct(r["ar_prior_m"], r["ar_m"])
    want = {"sales_b": r["sales_m"] / 1000, "sales_pct": round(sales, 1), "gross_margin": r2(gm), "gross_margin_bp": round((gm - gm0) * 100, 1),
            "op_margin": r2(om), "op_margin_bp": round((om - om0) * 100, 1), "unearned_b": r["unearned_m"] / 1000,
            # no year-ago balance on the print's own basis in any filing (Q1 FY18, the new revenue standard): not comparable
            "unearned_pct": None if r["unearned_prior_m"] is None else round(pct(r["unearned_prior_m"], r["unearned_m"]), 1),
            "receivables_b": r["ar_m"] / 1000, "receivables_pct": round(ar, 1), "receivables_gap_pp": round(ar - sales, 1)}
    for k, v in want.items():
        assert (p[k] is None) == (v is None) and (v is None or abs(p[k] - v) < 1e-9), (p["quarter"], k, p[k], v)
    if "fx_impact_m" in r:     # a total currency effect stated only in dollars (Q1 and Q2 FY12): growth excluding currency is
        # (revenue - effect) / year-ago revenue - 1, rounded half up to a whole percent, as the release states growth
        lc = math.floor((r["sales_m"] - r["fx_impact_m"]) / r["sales_prior_m"] * 100 - 100 + 0.5)
        assert p["lc_pct"] == lc, (p["quarter"], "lc_pct", p["lc_pct"], lc)


def usd(lo, hi):
    """A dollar range in billions as published: '$15.6-16.1B'; a point is '$x B'."""
    return f"${lo:g}B" if lo == hi else f"${lo:g}-{hi:g}B"


def pct_range(lo, hi):
    return f"{lo:+.1f}%" if lo == hi else f"{lo:+.1f}% to {hi:+.1f}%"


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    chart = retro_tool.chart("MSFT")
    fx = retro_tool.split_factor(chart, as_of)
    assert fx == 1.0, "a split after 2003-02-18 needs its encoding first (prices on the AS_OF share basis, the UNP rule)"
    off = chart["meta"]["gmtoffset"]
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + off, dt.timezone.utc).date().isoformat()
                    for v in chart.get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo_splits for s in facts.get("splits", [])), "a split's effective date must match the price data"
    px = dict(raw)
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    for g in [g for g in facts["guides"] if g["published"] <= as_of]:      # a guide public on AS_OF may carry only encoded fields
        assert set(g) <= GUIDE_KEYS and set(g.get("q_guide", {})) <= Q_GUIDE_KEYS, (g["doc"], "a guide field with no encoding yet; decide one first")
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        check_print(p)
    facts, split_ids = on_basis(facts, as_of)      # the 2003 split: FY1998 EPS and the first year's diluted shares
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    # prints published by AS_OF that report a fiscal year after the history (a Q4 print reports the year just ended, so it
    # stays in scope after the 10-K that follows it)
    first_fy = max(int(k) for k in h["eps_normalized"]) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    prints = [p for p in facts["prints"] if p["published"] <= as_of and guide_fy(p) >= first_fy]
    # no disruption theme in taxonomy_eras.json is live for a software maker to 2012-10-29 (CLOUD from 2012-10-30, scoped to
    # on-premise IT; OFFSHORE to IT services; GENAI from 2022-11-30); the 10-K's open-source, software-as-a-service and cloud risks
    # stay in the durability 'why' (the PEP obesity rule). The one encoding decided (retro/README.md, "MSFT 2012-2014"): each 10-K's
    # cloud risk factor (cloud_company_acknowledged) puts CLOUD on the watch list from the theme's live date, with the latest 10-K's
    # words (a 10-K's wording is replaced by the next 10-K's; a vintage that re-presents a 10-K's years keeps that 10-K's words and
    # event: 'text_published', the 8-K of 2017-08-03). Any other event kind needs its encoding decided first
    text_from = h.get("text_published", h["published"])
    events = [e for e in facts["events"] if e["published"] <= as_of and (text_from <= e["published"] or "doc" not in e)]
    if any(e["kind"] != "cloud_company_acknowledged" for e in events):
        sys.exit(f"{as_of}: the MSFT builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
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
            # an earlier year's company figure excluding only one-offs, first published in this release ('restates': the Q4 FY12
            # release's FY11 $2.64), replaces it until the next 10-K vintage carries it (the ACN rule)
            eps_n = {**h["eps_normalized"], y: a["eps_normalized"]}
            for yy, e in a.get("restates", {}).items():
                assert yy in eps_n, (p["quarter"], yy, "restates a year outside the history")
                eps_n[yy] = e
            h.update(fy_label=a["fy_label"],
                     eps_normalized=eps_n,
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]},
                     diluted_shares_m={**h["diluted_shares_m"], y: a["diluted_shares_m"]},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_op_margin=a["op_margin"], prev_fy_op_margin_note=a["op_margin_note"],
                     prev_fy_pretax_margin=a["pretax_margin"], prev_fy_pretax_margin_note=a["pretax_margin_note"],
                     prev_fy_gross_margin=a["gross_margin"], prev_fy_sales_growth=a["sales_growth"],
                     prev_fy_unearned_pct=a["unearned_pct"], prev_fy_unearned_note=f'{p["quarter"]} release',
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    latest = prints[-1]
    # the previous quarter is the print published just before the latest one (in or out of the history's scope); before the
    # first print in the fact sheet, the vintage names it
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    i = public.index(latest)
    prev = (public[i - 1]["unearned_pct"], public[i - 1]["quarter"]) if i > 0 else (h["prev_q_unearned_pct"], h["prev_q_label"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    cur_fy = max(eps_hist) + 1
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} FY{(latest['fy'] + (1 if nq == 4 else 0)) % 100:02d}"

    # ── guides for the current fiscal year: each field from the latest guide that states it ──
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    # a withdrawal voids every earlier guide for its year (the Q2 FY09 release: "no longer able to offer quantitative revenue and EPS
    # guidance for the balance of this fiscal year"): only the guides from the latest withdrawal on count
    gw = next((i for i in range(len(guides) - 1, -1, -1) if guides[i].get("withdrawn")), None)
    if gw is not None:
        guides = guides[gw:]
    gw = guides[0] if gw is not None else None
    ge = next((g for g in reversed(guides) if "eps_guide" in g), None)
    if ge:                                         # the ACN rule: the midpoint of the latest fiscal-year EPS range
        eps_now = round(sum(ge["eps_guide"]) / 2, 3)
        eps_label = f"{fy_e} guide midpoint (${money(ge['eps_guide'][0])}-{money(ge['eps_guide'][1])}, {ge['doc']})"
    else:                                          # no range for the year: the last full year's EPS stands (rollover rule)
        eps_now = eps_hist[cur_fy - 1]
        eps_label = (f"{fy_e}: no EPS guide in numbers" + (f" (the {gw['doc']} withdrew it)" if gw else "") +
                     f", FY{(cur_fy - 1) % 100:02d}'s ${money(eps_now)} stands")
    # a next-quarter guide counts while its quarter is unreported
    qkey = lambda q: (int(q.split("FY")[1]), int(q[1]))
    later = lambda q: qkey(q) > (latest["fy"] % 100, nq)
    gq = next((g for g in reversed(guides) if "q_guide" in g and later(g["q_guide"]["quarter"])), None)
    if gq:                                         # method r2: the next-quarter revenue guide, as growth on the year-ago quarter
        q = gq["q_guide"]
        fwd = [round((v / q["prior_sales_b"] - 1) * 100, 1) for v in q["sales_usd_b"]]
        fwd_label, fwd_short, fwd_period = f"{q['quarter']} revenue guide", f"{q['quarter'][:2]} guide", q["quarter"]
    else:                                          # no next-quarter revenue guide: the latest quarter's revenue growth excluding
        # currency, method r2's local-currency basis (the NKE and PEP rule): the growth the release states less the currency effect
        # the release or the quarter's 10-Q states, the reported growth where no filing states it (lc_pct; from the Q2 FY09 print)
        fwd = [latest["lc_pct"]] * 2
        fwd_label, fwd_short, fwd_period = (f"no {next_q} revenue guide, {latest['quarter']} revenue ex-currency",
                                            f"{latest['quarter'][:2]} rev ex-FX", latest["quarter"])
    gr = next((g for g in reversed(guides) if "rev_guide_usd_b" in g), None)
    go = next((g for g in reversed(guides) if "op_income_guide_usd_b" in g), None)
    bits = []
    if ge:
        fy_bits = ([f"revenue {usd(*gr['rev_guide_usd_b'])}"] if gr else []) + \
                  ([f"operating income {usd(*go['op_income_guide_usd_b'])}"] if go else []) + \
                  [f"EPS ${money(ge['eps_guide'][0])}-{money(ge['eps_guide'][1])}"]
        bits.append(f"{fy_now} ({ge['doc']}): " + ", ".join(fy_bits) + (f" ({ge['note']})" if ge.get("note") else ""))
    if gq:
        q = gq["q_guide"]
        eq = q.get("eps_words") or f"${money(q['eps'][0])}-{money(q['eps'][1])}"
        bits.append(f"{q['quarter']} ({gq['doc']}): revenue {usd(*q['sales_usd_b'])} ({pct_range(*fwd)} on {q['prior_label']}'s "
                    f"${q['prior_sales_b']:.3f}B), operating income {usd(*q['op_income_usd_b'])}, EPS {eq}"
                    + (f" ({gq['note']})" if gq.get("note") and gq is not ge else ""))
    gx = next((g for g in reversed(guides) if "opex_guide_usd_b" in g), None)
    if gx:                                         # 2009-2011: operating expense ranges only, display only
        bits.append(f"{fy_now} operating expenses {usd(*gx['opex_guide_usd_b'])} ({gx['doc']}" + (f"; {gx['note']}" if gx.get("note") else "") + ")")
    if gw:
        bits.append(f"no {fy_now} revenue or EPS guide in numbers: the {gw['doc']} withdrew it ('{gw['quote']}')")
    elif gx and not ge:
        bits.append(f"no {fy_now} revenue or EPS guide in numbers")
    # from the Q1 FY14 release Microsoft gives its outlook only on the conference call, which is not a filing: nothing is entered,
    # and the last numeric range of the year, if any, stands (the AAPL 2020 and NKE rule)
    on_call = (f"the {latest['quarter']} release gives guidance only on its conference call ('{latest['guide_on_call']}'), not a filing"
               if latest.get("guide_on_call") else None)
    guide_text = ("Guide: " + "; ".join(bits) + ("; operating income ranges are display only (no margin guide)" if not gx else
                                                  "; operating expense ranges are display only (no margin guide)")
                  + (f"; {on_call}" if on_call else "")) if bits else \
                 (f"{fy_now}: no guide in a filing; {on_call}" if on_call else f"{fy_now}: no guide in scope yet")
    margin_guided = False                          # no operating-margin guide in numbers: no guided step
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
    key_tail = ("A demand recession hits PC shipments and consumer sales first; the bear needs\n"
                "  it to spread to enterprise licensing renewals as well.")
    theme_summary = "no disruption theme has dated evidence"
    for e in [e for e in events if e["kind"] == "cloud_company_acknowledged"][-1:]:
        # CLOUD is live from 2012-10-30 and scoped to on-premise software and hardware; the latest 10-K's cloud risk factor puts it on
        # the watch list (the ACN CLOUD rule, as for LOW, NKE, AVGO and PEP: company-acknowledged, no market read). The factor pair
        # nets to zero and the theme signal stays at 2/4, so only text changes; re-filing needs dated evidence of market pricing
        val_word = "a premium" if pe_now_pctl >= 70 else "a discount to its own history" if pe_now_pctl <= 30 else "near its own median"
        stage = "cloud"
        watch = [{"theme": "CLOUD", "status": "live, company-acknowledged; no market read",
                  "reason": (f"Live: Microsoft's own {e['doc']}, under '{e['heading']}', says '{e['risk_quote']}' and '{e['margin_quote']}' "
                             f"It competes with cloud services of its own: '{e['offering']}' The stock trades at {close / eps_now:.1f}x "
                             f"{fy_e_s} — {val_word}. Re-file as DISRUPTION_EXPOSED (CLOUD) only if dated evidence shows the market "
                             "pricing cloud substitution of Microsoft's licensed software specifically.")}]
        factors = [(f"Cloud services: {e['offering_short']} — Microsoft sells them as well", 0.2, 0.10),
                   (f"Cloud competition ({e['doc']}): {e['risk_short']}", -0.2, 0.10)]
        sig_name = "Cloud: net effect on licensed software and services"
        trigger = "Customers move to competitors' cloud services faster than Microsoft's own cloud revenue grows"
        theme_summary = "cloud is live and company-acknowledged; no dated evidence ties the multiple to it"
    cat3 = (f"(3) The {fy_now} guide — " + bits[0] if ge else
            f"(3) The {fy_now} guide — operating expenses {usd(*gx['opex_guide_usd_b'])} only ({gx['doc']}); no revenue or EPS guide in numbers"
            if gx else f"(3) A {fy_now} guide — none in a filing: {on_call}" if on_call else f"(3) A {fy_now} guide — none in scope yet")
    cat4 = (f"(4) Receivables — {latest['receivables_pct']:+.1f}% against revenue {latest['sales_pct']:+.1f}% in {latest['quarter']} "
            f"({latest['receivables_gap_pp']:+.1f}pp): volume licensing is billed ahead, collected later"
            + (f"; {latest['receivables_caveat']}" if latest.get("receivables_caveat") else ""))

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    # a print dated AS_OF meets AS_OF's close only if it was public before the open (the week's last trading day)
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    company = h["company"]
    exchange = h["exchange"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])]
           + [x for g in guides for x in [g["source"], g.get("q_guide", {}).get("prior_source")] if x]
           + ([dividend_src] if dividend_src else []) + split_ids + [e["id"] for e in events])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "A0", "published": as_of, "title": "Yahoo Finance daily prices, MSFT and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/MSFT/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "unearned_b", "unearned_pct", "receivables_b", "receivables_pct",
                   "receivables_gap_pp", "gross_margin", "gross_margin_bp", "op_margin", "op_margin_bp", "eps_q", "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    eps_note = f"; {latest['eps_note']}" if latest.get("eps_note") else ""
    unearned = f"{latest['unearned_pct']:+.1f}%" if latest["unearned_pct"] is not None else "not comparable"
    billings = (f"Billings: unearned revenue {unearned} ({latest['unearned_note']}); revenue "
                f"{latest['sales_pct']:+.1f}% as reported ({latest['sales_note']}); "
                + (f"'{latest['fx_note']}'" if latest["fx_note"] is not None else "no filing states the quarter's currency effect")
                + (f"; ex-currency {latest['lc_pct']:+.0f}% ({latest['lc_note']})" if not gq else "") + eps_note)
    fy_rev = sum(gr["rev_guide_usd_b"]) / 2 if gr else rev[max(rev)] * (1 + sum(fwd) / 2 / 100)
    fy_rev_label = (f"the {fy_now} revenue guide midpoint ({usd(*gr['rev_guide_usd_b'])}, {gr['doc']})" if gr else
                    f"{fwd_label}, applied to the year (no {fy_now} revenue guide in scope)")
    R = repr
    head = f'''#!/usr/bin/env python3
"""
MSFT Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: MSFT)  ·  {h["business_line"]}
Generated by retro/build_msft.py from retro/facts/MSFT.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "MSFT"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); software signals")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts and events above.
PIT_PROFILE = {{
    "kind": "DURABLE",
    "risk": 2,
    "why": {R(h["why"])},
    "theme_watch": {R(watch)},
    "evidence": {R(list(dict.fromkeys(e["id"] for e in events)))},
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
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}{"; " + h["split_note"] if h.get("split_note") else ""}
REVENUE_HIST  = {R(rev)}   # revenue, USD bn
SHARES_HIST   = {R({y: round(v, 1) for y, v in shares.items()})}   # diluted, millions, on the AS_OF share basis
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # operating margin, {h["prev_fy_op_margin_note"]}
CHECK_PRETAX_MARGIN = {h["prev_fy_pretax_margin"]}   # pre-tax margin, {h["prev_fy_pretax_margin_note"]} (the EPS check only)
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_UNEARNED   = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # {"next-quarter revenue guide, growth on the year-ago quarter" if gq else "no next-quarter revenue guide: the latest quarter's revenue growth excluding currency"}
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no margin guide, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {fy_rev:.2f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenue {h['prev_fy_sales_growth']:+.1f}%, unearned revenue {h['prev_fy_unearned_pct']:+.1f}% ({h['prev_fy_unearned_note']}); {latest['quarter'].split()[0]} gross margin {latest['gross_margin']:.2f}% ({latest['gross_margin_bp']:+.0f}bp)")}
BALANCE_TEXT    = {R(f"Cash and short-term investments ${latest['cash_b']:.2f}B, {h['fcf_label']} free cash flow ${h['fcf_b']:.2f}B, dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
BILLINGS_TEXT   = {R(billings)}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/MSFT)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("MSFT"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<34}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
