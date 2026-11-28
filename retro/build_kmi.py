#!/usr/bin/env python3
"""
Build KMI retrospective models from the dated fact sheet (retro/facts/KMI.json).

The KMI sibling of build_ctva.py's new-listing builder: the same frozen rules (retro method r2), the same weekly dates and the same
market statistics, with pipeline signals (retro/templates/kmi_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints, guides and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, from the listing (the listing rule of method r2),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Kinder Morgan, Inc.'s Class P common stock began trading on the NYSE as KMI on 2011-02-11; its own P/E exists only from that day
(retro/README.md, "KMI"). Every filing from the Q1 2011 10-Q on computes EPS only from February 11, 2011, so 2011 is not a year of
EPS (the BKR 2017 and CTVA 2017 rule) and is excluded: its days leave the P/E window. The first full year of EPS is 2012, so no date
can be built before the Q4 2012 release (8-K accepted 2013-01-16 16:11 ET, public from 2013-01-17; the first weekly date is
2013-01-18). EPS is GAAP diluted EPS from continuing operations per Class P share, each year from the latest filing that reports it.

Kinder Morgan guides dividends and cash available to pay dividends, never revenue or a margin in numbers, so:
  - current-FY EPS: the last full year's GAAP EPS stands (the PFE rule for a year with no reported-EPS guide), until the 2021 budget
    (the Q4 2020 release) begins to guide GAAP earnings: from it, the guide's per-share figure where the release states one, else its
    net income attributable to KMI (midpoint, or the budget times the stated percentage) over the release's own diluted
    weighted-average shares (README, "KMI 2019-2022"),
  - BASE growth and the growth factor: the latest quarter's revenue growth as reported (the SO and UNP no-guide rule),
  - guided margin step: none; the margin signal uses the latest quarter's change.
The dividend, DCF and EBITDA outlooks are shown in the guide line, display only.

Signals (each against the year-ago quarter): total segment EBDA and Natural Gas Pipelines segment EBDA growth, from the release where
it tabulates the quarter, else from the quarter's 10-Q once that is public (the PEP servings_later rule; a fourth quarter, in no 10-Q,
is not reported until a release tabulates it); revenue growth, the operating margin change and the pre-tax margin change from the
release's statement of income. Growth against a year-ago loss is measured over the loss's absolute value (the CAT and SO rule).

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. Every earnings 8-K of the series was accepted after the close, so each print is dated the next
trading day and the week's date is the trading day after that (the AAPL rule).

Output goes to staging/retrospective/KMI until the series is added to the archive (--out archive/retrospective/KMI).

Usage
  python3 retro/build_kmi.py --weekly 2013-01-14 2014-12-31      # 103 dates, 2013-01-18 .. 2014-12-31
  python3 retro/build_kmi.py --weekly 2015-01-01 2018-12-31      # 210 dates, 2015-01-02 .. 2018-12-31 (README, "KMI 2015-2018")
  python3 retro/build_kmi.py --weekly 2019-01-01 2022-12-31      # 209 dates, 2019-01-04 .. 2022-12-30 (README, "KMI 2019-2022")
  python3 retro/build_kmi.py --weekly 2023-01-01 2026-11-15      # 202 dates, 2023-01-06 .. 2026-11-13 (README, "KMI 2023-2026")
  python3 retro/build_kmi.py 2013-01-18
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/KMI/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "KMI.json")
ENGINE = os.path.join(HERE, "templates", "kmi_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "KMI")
SYMBOL = "KMI"
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"seg": (-23, -9, 5, 18), "ngp": (-13, -7, -1, 5), "revenue": (-89, -41, 7, 26),
                     "op_margin": (-1340, -390, 550, 4000), "pretax_margin": (-2510, -960, 590, 3930)}
RULE_T_KEYS = {"seg": (1, False), "ngp": (1, False), "revenue": (1, False), "op_margin": (10, False), "pretax_margin": (10, False)}
PRINT_KEYS = {"quarter", "fy", "q", "published", "source", "release", "release_time", "period_end", "raw", "sales_b", "sales_pct",
              "opm", "opm_bp", "ptm", "ptm_bp", "eps_q", "eps_q_prior", "diluted_shares_m", "seg_pct", "ngp_pct", "seg_note",
              "seg_later", "sales_note", "margin_note", "eps_note", "cash_note", "next_print", "fy_actual"}
FY_KEYS = {"fy", "fy_label", "eps_normalized", "excluded_note", "revenue_usd_b", "diluted_shares_m", "normalization_note", "op_margin",
           "op_margin_note", "sales_growth", "check_pretax_margin", "check_pretax_note", "tax_rate", "tax_note", "one_off_test"}
GUIDE_KEYS = {"fy", "published", "source", "doc", "release_time", "display", "rev_none", "eps_guide", "ni_guide_m", "ni_budget_m",
              "ni_vs_budget_pct", "earnings_words"}
EARNINGS_KEYS = ("eps_guide", "ni_guide_m", "ni_budget_m")      # a GAAP earnings guide (from the 2021 budget, README "KMI 2019-2022")


def fiscal_year_end(n):
    """Kinder Morgan's fiscal year n is the calendar year n."""
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


def check_print(p):
    """Re-derive a print's growth rates and margins from its raw published figures (they must match the fact sheet)."""
    assert set(p) <= PRINT_KEYS, (p["quarter"], sorted(set(p) - PRINT_KEYS), "a print field with no encoding yet; decide one first")
    r = p["raw"]
    # growth on the year-ago figure; against a year-ago loss, over the loss's absolute value (the CAT 2014-2017 and SO 2018-2021 rule,
    # first needed for KMI in Q2 2021, whose year-ago Natural Gas Pipelines EBDA is a loss)
    pct = lambda a, b: round((b / a - 1) * 100, 1) if a > 0 else round((b - a) / abs(a) * 100, 1) if a < 0 else None
    mg = lambda x, rev: round(x / rev * 100 + 0.0, 2)
    want = {"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": pct(r["rev_prior_m"], r["rev_m"]),
            "opm": mg(r["oi_m"], r["rev_m"]), "opm_bp": round((mg(r["oi_m"], r["rev_m"]) - mg(r["oi_prior_m"], r["rev_prior_m"])) * 100, 1),
            "ptm": mg(r["pti_m"], r["rev_m"]), "ptm_bp": round((mg(r["pti_m"], r["rev_m"]) - mg(r["pti_prior_m"], r["rev_prior_m"])) * 100, 1),
            "eps_q": r["eps_q"], "eps_q_prior": r["eps_q_prior"], "diluted_shares_m": r["dil_sh_m"]}
    for k, v in want.items():
        assert p[k] == v or (v is not None and abs(p[k] - v) < 1e-9), (p["quarter"], k, p[k], v)
    if "seg_m" in r:                        # a release that tabulates segment EBDA (from Q4 2014): the growth from its own rows
        assert (p["seg_pct"], p["ngp_pct"]) == (pct(r["seg_prior_m"], r["seg_m"]), pct(r["ngp_prior_m"], r["ngp_m"])), p["quarter"]
    sl = p.get("seg_later")                 # segment EBDA absent from the release: the quarter's 10-Q, on its own date
    if sl:
        assert p["seg_pct"] is None and set(sl) == {"seg_pct", "ngp_pct", "published", "source", "note"}, p["quarter"]
        assert sl["published"] >= p["published"], (p["quarter"], "a 10-Q cannot precede its release")
    a = p.get("fy_actual")
    if a:
        assert set(a) <= FY_KEYS, (p["quarter"], sorted(set(a) - FY_KEYS), "a full-year field with no encoding yet; decide one first")
        t = a["one_off_test"]
        kept = a["eps_normalized"] is not None
        # a year is kept at GAAP unless it is a loss or its listed one-off charges (after tax) exceed its income attributable to KMI
        assert t["distorted"] == (t["items_after_tax_m"] > t["income_attributable_m"]), (p["quarter"], "the one-off test")
        assert kept == (not t["distorted"] and a["eps_normalized"] > 0), (p["quarter"], "the year's EPS and the one-off test disagree")


def segments(p, as_of):
    """A print's segment EBDA growth on AS_OF: its release's; else, once public, the quarter's 10-Q (the PEP servings_later rule)."""
    sl = p.get("seg_later")
    if p["seg_pct"] is None and sl and sl["published"] <= as_of:
        return sl["seg_pct"], sl["ngp_pct"], sl["note"], sl["source"]
    return p["seg_pct"], p["ngp_pct"], p["seg_note"], None      # nothing about a filing not yet public may show (the firewall)


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    listing = facts["listing"]
    first_day = listing["first_trading_day"]
    if as_of < first_day:
        sys.exit(f"{as_of}: Kinder Morgan's Class P common stock began trading on {first_day}; no P/E of its own exists before it (the listing rule)")
    chart = retro_tool.chart(SYMBOL)
    assert not chart.get("events", {}).get("splits") and not facts["distributions"], "a split or distribution needs its encoding first"
    assert min(raw) == first_day, ("the price data must start on the listing day", min(raw), first_day)
    px = dict(raw)                                     # no split or distribution: Yahoo's close is the price as traded
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no annual history of Kinder Morgan, Inc. is public yet")
    for v in vintages:                                 # the fiscal calendar the filings state must match the rule
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    for g in [g for g in facts["guides"] if g["published"] <= as_of]:
        assert set(g) <= GUIDE_KEYS, (g["doc"], "a guide field with no encoding yet; decide one first")
        assert g.get("rev_none") and "rev_guide_m" not in g, (g["doc"], "a revenue guide in numbers needs its encoding first")
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    for p in public:                                   # a print public on AS_OF must match its raw figures
        check_print(p)
    h = vintages[-1]                                   # latest annual history public on AS_OF
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    prints = [p for p in public if guide_fy(p) >= first_fy]
    events = [e for e in facts["events"] if e["published"] <= as_of]
    if events:
        sys.exit(f"{as_of}: the KMI builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
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
                     diluted_shares_m={**h["diluted_shares_m"], y: a["diluted_shares_m"]},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_op_margin=a["op_margin"], prev_fy_op_margin_note=a["op_margin_note"],
                     prev_fy_sales_growth=a["sales_growth"],
                     check_pretax_margin=a["check_pretax_margin"], check_pretax_note=a["check_pretax_note"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    latest = prints[-1]
    i = public.index(latest)
    seg_pct, ngp_pct, seg_note, seg_src = segments(latest, as_of)
    prev_seg = (segments(public[i - 1], as_of)[0], public[i - 1]["quarter"]) if i > 0 else (None, "no earlier print")
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    excluded = {int(k): v for k, v in h.get("eps_excluded", {}).items()}
    if not eps_hist:                                   # 2011 covers February 11 to December 31 only: no full year, no P/E
        sys.exit(f"{as_of}: no full year of Kinder Morgan's EPS is public yet, so the stock has no P/E of its own (method r2)")
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)        # the last full year in the history: cur_fy - 1 unless that year is excluded
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── current-FY EPS; the dividend, DCF and EBITDA outlooks are display only ──
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    gl = guides[-1] if guides else None                                        # the latest outlook for the year (display)
    excluded_tail = "".join(f" (FY{y % 100:02d} is excluded: {excluded[y]})" for y in range(last_fy + 1, cur_fy))
    # ── a GAAP earnings guide (from the 2021 budget): current-FY EPS is its per-share figure where the release states one, else its net
    # income attributable to KMI (midpoint; a percentage on the budget's figure where it is stated that way) divided by the release's own
    # diluted weighted-average Class P shares; an earnings outlook in words keeps the last figure (the ACN rule). With none, the last full
    # year's EPS stands (the PFE rule) ──
    eg = next((g for g in reversed(guides) if any(k in g for k in EARNINGS_KEYS)), None)
    if eg:
        rel = [p for p in public if p["source"] == eg["source"]]
        assert len(rel) == 1, (eg["doc"], "an earnings guide must come with its release's print")
        if "eps_guide" in eg:
            eps_now = round(sum(eg["eps_guide"]) / 2, 3)
            how = f"the {eg['doc']}'s ${eg['eps_guide'][0]:.2f} a share" if eg["eps_guide"][0] == eg["eps_guide"][1] else \
                f"the {eg['doc']}'s ${eg['eps_guide'][0]:.2f}-{eg['eps_guide'][1]:.2f} a share, midpoint"
        else:
            if "ni_guide_m" in eg:
                lo, hi = eg["ni_guide_m"]
                ni = (lo + hi) / 2
                ni_txt = f"${lo / 1000:.1f} billion" if lo == hi else f"${lo / 1000:.1f}-{hi / 1000:.1f} billion (midpoint ${ni / 1000:.1f} billion)"
            else:
                ni = eg["ni_budget_m"] * (1 + eg["ni_vs_budget_pct"] / 100)
                ni_txt = (f"${ni / 1000:.3f} billion (the ${eg['ni_budget_m'] / 1000:.1f} billion budget "
                          f"{eg['ni_vs_budget_pct']:+g}%)")
            sh = rel[0]["diluted_shares_m"]
            eps_now = round(ni / sh, 3)
            how = f"the {eg['doc']}'s net income attributable to KMI of {ni_txt} / {sh:,.0f}M diluted shares"
        eps_label = f"{fy_e}: GAAP earnings guide, {how} = ${money(eps_now)}" + excluded_tail
        if eg.get("earnings_words"):
            eps_label += f"; restated in words: '{eg['earnings_words']}' (the last figure stands)"
    else:
        eps_now = eps_hist[last_fy]
        eps_label = (f"{fy_e}: no reported (GAAP) EPS guide, FY{last_fy % 100:02d}'s ${money(eps_now)} stands" + excluded_tail)
    fwd = [latest["sales_pct"]] * 2
    fwd_label, fwd_short, fwd_period = (f"no {fy_now} revenue guide in numbers, {latest['quarter']} revenues as reported",
                                        f"{latest['quarter'][:2]} revenues", latest["quarter"])
    if eg:
        guide_text = (f"{fy_now}: no revenue or margin guide in numbers (BASE takes {latest['quarter']} revenue growth as reported); "
                      f"GAAP EPS ${money(eps_now)} from the {eg['doc']}'s earnings guide")
    else:
        guide_text = f"{fy_now}: no revenue, EPS or margin guide in numbers (BASE takes {latest['quarter']} revenue growth as reported)"
    if gl:
        guide_text += f"; the {gl['doc']}'s {gl['display']}"
    margin_guided = False                          # no margin guide: no guided step
    fy_margin_base = h["prev_fy_op_margin"]

    # ── dividend: the latest declared rate ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts["dividends"] if d["published"] <= as_of]
    divs.append((h["published"], h["dividend_annual"], h["dividend_note"], None))
    _, dividend, dividend_note, dividend_src = max(divs, key=lambda x: x[0])

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
    # an excluded year's own days leave the window (2011, the IPO period)
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

    # ── era-dependent text, from facts only: no disruption theme in the registry is live for a pipeline company on these dates ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none in scope", "No live disruption theme covers pipelines and terminals"
    theme_summary = "no theme in the registry is live for a pipeline company on this date; none has dated evidence"
    key_tail = ("Contracted transport and storage fees drive most of the cash, by the company's own account;\n"
                "  the bear needs volumes and rates to fall, not one quarter's commodity prices.")
    why = h["why"]
    # ENERGY_TRANSITION is live from 2015-12-12 and scoped to oil, gas and coal reserves and refining; Kinder Morgan's 10-Ks say its CO2
    # segment owns working interests in oil fields (SACROC, Yates, ...) and their greenhouse gas risk factor names the theme, so it goes on
    # the watch list (the XOM and SO rule: company-acknowledged, no market read). No factor pair is added, so only text changes; re-filing
    # needs dated evidence of market pricing for Kinder Morgan (retro/README.md, "KMI 2015-2018"). Dates before the live date keep the text above
    et = retro_tool.load_taxonomy()["themes"]["ENERGY_TRANSITION"]
    if et["live_from"] <= as_of:
        assert h.get("transition_quote") and h.get("reserves_quote"), (as_of, "the vintage needs its own 10-K words for the watch list")
        val_word = ("a premium" if pe_now_pctl >= 70 else "a discount to its own history" if pe_now_pctl <= 30 else "near its own median")
        stage = "transition"
        watch = [{"theme": "ENERGY_TRANSITION", "status": "live, company-acknowledged; no market read",
                  "reason": (f"Live: Kinder Morgan's own FY20{h['fy_label'][2:]} 10-K says '{h['reserves_quote']}' and, of greenhouse gas "
                             f"laws and regulations, '{h['transition_quote']}' The stock trades at {close / eps_now:.1f}x {fy_e_s} — "
                             f"{val_word}. Re-file as DISRUPTION_EXPOSED (ENERGY_TRANSITION) only if dated evidence shows the market "
                             "pricing decarbonisation of Kinder Morgan's oil reserves and the hydrocarbons its pipelines carry specifically.")}]
        sig_name = "Energy transition: oil reserves and hydrocarbon demand"
        trigger = "Greenhouse gas rules cut hydrocarbon demand and strand the CO2 segment's oil reserves"
        theme_summary = "the energy transition is live and company-acknowledged; no dated evidence ties the multiple to it"
        why += ("; ENERGY_TRANSITION is live (from " + et["live_from"] + "): the CO2 segment owns working interests in oil fields and the "
                "greenhouse gas risk factor puts the theme on the watch list, company-acknowledged, with no dated evidence that the market "
                "prices it for Kinder Morgan")
    kind, pit_risk = "DURABLE", 2
    cat3 = ((f"(3) The {fy_now} outlook — GAAP EPS ${money(eps_now)} ({how}); no revenue or margin guide in numbers" if eg else
             f"(3) The {fy_now} outlook — no revenue, EPS or margin guide in numbers")
            + (f"; {gl['display']}" if gl else "; no dividend outlook for the year yet"))
    cat4 = f"(4) Free cash flow — {h['fcf_label']} {h['fcf_note']}"

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    company, exchange, listed = h["company"], h["exchange"], h["symbol"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]]] + [listing["source"]]
           + ([dividend_src] if dividend_src else []) + ([gl["source"]] if gl else []) + ([seg_src] if seg_src else [])
           + [s for p in prints for s in [segments(p, as_of)[3]] if s and p is not latest])
    sources = [dict(id=i, **{k: v for k, v in facts["sources"][i].items()}) for i in dict.fromkeys(ids)]
    sources.append({"id": "A0", "published": as_of,
                    "title": f"Yahoo Finance daily prices, {company} Class P common stock ({exchange}: {listed}) and S&P 500, truncated at AS_OF",
                    "url": f"https://finance.yahoo.com/quote/{SYMBOL}/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution "
                                f"since the listing on {first_day}"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "opm", "opm_bp", "ptm", "ptm_bp", "eps_q", "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    activity = (f"Activity: {latest['sales_note']}; segment EBDA: {seg_note}; {latest['margin_note']}; {latest['cash_note']}; "
                f"EPS {latest['eps_note']}")
    fy_rev = rev[max(rev)] * (1 + sum(fwd) / 2 / 100)
    fy_rev_label = f"{fwd_label}, applied to the year (no {fy_now} revenue guide)"
    franchise_q = f"{latest['quarter'].split()[0]} operating margin {latest['opm']:.2f}% ({latest['opm_bp']:+.0f}bp)"
    fcf_text = f"${h['fcf_b']:.2f}B" if h["fcf_b"] >= 0 else f"$({-h['fcf_b']:.2f})B"
    LATEST = {**{k: latest.get(k) for k in latest_keys}, "seg_pct": seg_pct, "ngp_pct": ngp_pct}
    R = repr
    head = f'''#!/usr/bin/env python3
"""
{listed} Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: {listed})  ·  {h["business_line"]}
Generated by retro/build_kmi.py from retro/facts/KMI.json: the constants below are the facts public on
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
               "derived from dated facts by frozen rules (retro/README.md); pipeline signals")
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
REVENUE_HIST  = {R(rev)}   # revenues, USD bn
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
SHARES_DIL_B    = {round(latest["diluted_shares_m"] / 1000, 4)!r}   # diluted shares, bn
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenues {h['prev_fy_sales_growth']:+.1f}%; {franchise_q}")}
BALANCE_TEXT    = {R(f"{h['fcf_label']} free cash flow {fcf_text} (consolidated), dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
ACTIVITY_TEXT   = {R(activity)}
CAPITAL_RETURN  = {R(h["cash_return_text"])}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/KMI)")
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
