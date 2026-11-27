#!/usr/bin/env python3
"""
Build NEE retrospective models from the dated fact sheet (retro/facts/NEE.json).

The NEE sibling of build_so.py (the electric utility builder) with UNP's split encoding and SPGI's listed symbol: the same frozen
rules (retro method r2), the same weekly dates and the same market statistics, with FPL Group's own utility signals
(retro/templates/nee_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints, guides and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, as traded (Yahoo's split-adjusted series times the
     splits after AS_OF: the 4-for-1 split of 2020-10-27; the 2-for-1 split of 2005-03-16 restates the per-share facts published
     before it through the fact sheet's 'splits', the shared on_basis of build_unp.py),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

The company of 2008-2009 is FPL Group, Inc., listed on the NYSE as FPL (NextEra Energy, Inc. and NYSE: NEE from 2010). NEE is the
series key (TICKER, the folder, the index) and the symbol under which Yahoo serves the price history; every printed line names
the listing of the date (LISTED_SYMBOL = "FPL"; the SPGI and BKR encoding; retro/README.md, "NEE").

FPL Group's fiscal year is the calendar year. Every EPS guide of 2007-2009 is a range of 'adjusted earnings per share', which
also excludes the mark-to-market effect of non-qualifying hedges (and, from 2008, other than temporary impairment losses on the
nuclear decommissioning funds), recurring items: a guide on that basis gives no field (the PEP 2008 core rule), so the guides are
display only and the no-guide rules of method r2 apply on every date (retro/README.md, "NEE"):
  - current-FY EPS: the last full year's EPS stands (the rollover rule),
  - forward revenue growth: the latest quarter's total operating revenue growth, as reported (the UNP rule),
  - guided margin step: none; the margin signal uses the latest quarter's change in the operating margin.
EPS is GAAP diluted EPS before the cumulative effect of accounting changes, each year from the latest 10-K that reports it,
except 1999 and 2000 at the company's figures excluding only one-offs (the FY2002 10-K's $3.98 and $4.38, before the split: the
ACN and JPM FY2017 rules); from 2001 the company's figures also exclude the recurring mark-to-market item, so GAAP stands. A Q4
release comes weeks before its 10-K, so a Q4 print carries the year's actuals (fy_actual) until the 10-K. No disruption theme in
taxonomy_eras.json is live for an electric utility in 2008-2009 (ENERGY_TRANSITION from 2015-12-12), so the watch list is empty
and the builder refuses events until an encoding is decided.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. Every release came before the open; those of 2007-2009 on a weekday with a next trading day in its
week, while six of 2010-2013 came on a Friday (2010-07-23, 2010-10-29, 2011-04-29, 2011-11-04, 2012-01-27, 2013-11-01), so those weeks
are dated the release day and the print meets that day's close ("day of the print, public before the open").

NEE 2010-2013 (retro/README.md): the change of name to NextEra Energy, Inc. applies from the 8-K of 2010-05-24 that states it until a
vintage carries it ('company_names'), and NYSE: NEE from its announced effective date, 2010-06-23 ('listings', the SPGI encoding);
from CLOUD's live date (2012-10-30) the 'why' quotes every live theme's registered scope (the UNH and CB wording), none of which names
an electric utility; the Q1 2013 release's EPS includes a gain from discontinued operations, kept as published (its note says so).

NEE 2014-2017 (retro/README.md): from ENERGY_TRANSITION's live date (2015-12-12) the FY2014-FY2016 10-Ks' own words on NEER's oil
and gas production assets and the greenhouse gas limits put the theme on the watch list, company-acknowledged, with no market read (the
XOM and SO rule; 'reserves_quote', 'transition_quote'); no factor pair, so only text changes. A vintage's 'franchise_note' says where
the franchise line's FPL figures come from when its 10-K no longer tabulates them (FY2016). Three releases came on a Friday (2014-10-31,
2017-01-27, 2017-04-21) and date their own weeks.

NEE 2018-2021 (retro/README.md): from the Q4 2017 release the releases no longer tabulate FPL's energy sales or customer accounts,
and no 10-K of the period does, so those figures are None: the energy sales signal scores BASE and prints n/r through the None-tolerant
copy of the engine (nee2_engine.py.tmpl, the BKR bkr3, SPGI spgi2 and SCHW schw2 encoding), which is the engine with the n/r edits of
nr_engine() below; Gulf Power (acquired 2019-01-01) is in the figures as published, its net income display only. The four-for-one
split effective 2020-10-27 is the second 'splits' record: prices as traded, the per-share facts published before it divided by 4 (on_basis),
and a note or dividend sentence published before it says its figures are on the earlier basis. Five releases came on a Friday
(2018-01-26, 2019-01-25, 2020-01-24, 2020-07-24, 2021-07-23) and date their own weeks.

Output goes to staging/retrospective/NEE until the series is added to the archive (--out archive/retrospective/NEE).

Usage
  python3 retro/build_nee.py --weekly 2008-01-01 2009-12-31
  python3 retro/build_nee.py 2008-01-31
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/NEE/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "NEE.json")
ENGINE = os.path.join(HERE, "templates", "nee_engine.py.tmpl")
ENGINE2 = os.path.join(HERE, "templates", "nee2_engine.py.tmpl")   # (NEE 2018-2021) the None-tolerant copy: nr_engine(ENGINE)
OUT = os.path.join(ROOT, "staging", "retrospective", "NEE")
SYMBOL = "NEE"                     # the series key and Yahoo's symbol; the listing of each date comes from 'listings'
# rule T, the engine's signal thresholds over 1997-2006 (the FY2006 10-K, the vintage public on 2008-01-04): (BEAR, BASE, BULL, XBULL);
# the builder re-derives them from the fact sheet's raw figures
ENGINE_THRESHOLDS = {"kwh": (-5, -1, 2, 8), "segment": (-16, -6, 3, 12), "revenue": (-15, -3, 8, 33), "eps": (-31, -13, 5, 38),
                     "margin": (-840, -450, -60, 320)}
RULE_T_KEYS = {"kwh": (1, False), "segment": (1, False), "revenue": (1, False), "eps": (1, False),
               "margin": (10, False)}           # (rounding unit, lower is better)
GUIDE_KEYS = {"fy", "published", "source", "doc", "display", "unused"}


def fiscal_year_end(n):
    """FPL Group's fiscal year n is the calendar year n."""
    return dt.date(n, 12, 31)


def fiscal_year(day):
    return dt.date.fromisoformat(day).year


def rule_t_value(k, raw):
    if k == "margin":
        (o0, r0), (o1, r1) = raw
        return round((o1 / r1 - o0 / r0) * 10000, 1)
    a, b = raw
    return round((b / a - 1) * 100, 2)


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


# (NEE 2018-2021) the n/r edits that make the engine None-tolerant for FPL's energy sales, exact and each asserted once (the
# engine already scores a None value BASE and prints it n/r in its tables)
NR_EDITS = [
    ("# (its business segments) and the report wording differ.\n",
     "# (its business segments) and the report wording differ.\n"
     "# This copy is the one used when the latest release does not report FPL's energy sales (from the Q4 2017\n"
     "# release NextEra Energy's releases carry no FPL statistics table): a figure the release does not report\n"
     "# stays None, scores BASE and prints \"n/r\" (not reported). Rules, thresholds and weights are those of\n"
     "# nee_engine.py.tmpl, line for line (the BKR bkr3, SPGI spgi2 and SCHW schw2 encoding; retro/README.md,\n"
     "# \"NEE 2018-2021\").\n"),
    ("def _now(v, u):\n    return \"n/r\" if v is None else f\"{v:+.1f}{u}\"   # n/r: not reported (no figure in the filings public on AS_OF)\n",
     "def _now(v, u):\n    return \"n/r\" if v is None else f\"{v:+.1f}{u}\"   # n/r: not reported (no figure in the filings public on AS_OF)\n\n"
     "def _f(v):\n    return None if v is None else float(v)              # a figure the release does not report stays None\n"),
    ('float(LATEST["kwh_pct"])', '_f(LATEST["kwh_pct"])'),
    ("to {L['kwh_pct']:+.1f}% ({L['quarter']})\"", "to {_now(L['kwh_pct'], '%')} ({L['quarter']})\""),
    ("f\"FPL energy sales {L['kwh_pct']:+.1f}%; FPL net income", "f\"FPL energy sales {_now(L['kwh_pct'], '%')}; FPL net income"),
    ("— the next read on FPL's energy sales ({L['kwh_pct']:+.1f}% now); no sales guide in numbers to read it against",
     "— FPL's energy sales {_now(L['kwh_pct'], '%')} now (the releases no longer tabulate them), FPL net income {L['seg_pct']:+.1f}%; no sales guide in numbers"),
    ("+ f\"FPL energy sales {L['kwh_pct']:+.1f}% in {L['quarter']}\"", "+ f\"FPL energy sales {_now(L['kwh_pct'], '%')} in {L['quarter']}\""),
]


def nr_engine(engine):
    """The None-tolerant engine: `engine` with the n/r edits (the sensitivity variants of an engine carry over)."""
    for old, new in NR_EDITS:
        assert engine.count(old) == 1, ("an n/r edit must match the engine once", old)
        engine = engine.replace(old, new)
    return engine


def check_print(p):
    """Re-derive a print's growth rates, margins and EPS growth from its raw published figures (they must match the fact sheet)."""
    r = p["raw"]
    pct = lambda a, b: round((b / a - 1) * 100, 1)
    # growth against a year-ago loss is measured over the loss's absolute value (the CAT rule); every base of the range is positive
    gpct = lambda a, b: pct(a, b) if a > 0 else round((b - a) / abs(a) * 100, 1)
    m, m0 = r["opinc_m"] / r["rev_m"] * 100, r["opinc_prior_m"] / r["rev_prior_m"] * 100
    want = {"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": pct(r["rev_prior_m"], r["rev_m"]),
            "kwh_pct": None if r["kwh_m"] is None else pct(r["kwh_prior_m"], r["kwh_m"]), "seg_pct": gpct(r["seg_prior_m"], r["seg_m"]),
            "margin": round(m, 2), "margin_prior": round(m0, 2), "margin_bp": round((m - m0) * 100, 1),
            "eps_pct": gpct(p["eps_q_prior"], p["eps_q"])}
    for k, v in want.items():
        assert p[k] == v or (p[k] is not None and v is not None and abs(p[k] - v) < 1e-9), (p["quarter"], k, p[k], v)
    # the EPS signal's basis: GAAP diluted EPS (the adjusted figure removes the recurring mark-to-market item: the PEP 2008 core rule)
    assert p["eps_basis"] == "GAAP" and (p["eps_q"], p["eps_q_prior"]) == (p["eps_gaap"], p["eps_gaap_prior"]), (p["quarter"], "EPS basis")
    assert p["eps_q_prior"] != 0, (p["quarter"], "a zero year-ago EPS needs its encoding first")


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    et = retro_tool.load_taxonomy()["themes"]["ENERGY_TRANSITION"]
    chart = retro_tool.chart(SYMBOL)
    off = chart["meta"]["gmtoffset"]
    ydate = lambda v: dt.datetime.fromtimestamp(v["date"] + off, dt.timezone.utc).date().isoformat()
    yahoo = {ydate(v): v["numerator"] / v["denominator"] for v in chart.get("events", {}).get("splits", {}).values()}
    # a split record must sit on a split date of the price data, and every split of the price data on or before AS_OF needs one
    # (on_basis restates the per-share facts published before it); the splits after AS_OF put the window on the AS_OF share basis
    assert all(s["effective"] in yahoo for s in facts["splits"]), "a split's effective date must match the price data"
    assert all(yahoo[s["effective"]] == s["ratio"] for s in facts["splits"] if s["effective"] <= as_of), "a split's ratio must match"
    assert {d for d in yahoo if d <= as_of} <= {s["effective"] for s in facts["splits"]}, (as_of, "an unencoded split")
    assert not facts.get("distributions"), "the NEE builder has no distribution encoding"
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    assert not [g for g in facts.get("eps_guides", []) if g["published"] <= as_of], "an EPS guide with a field needs its encoding first"
    for g in [g for g in facts["guides"] if g["published"] <= as_of]:   # a guide public on AS_OF: display only
        assert set(g) == GUIDE_KEYS, (g["doc"], "a guide field the builder has no encoding for", set(g) ^ GUIDE_KEYS)
    events = [e for e in facts["events"] if e["published"] <= as_of]
    if events:
        sys.exit(f"{as_of}: the NEE builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    for p in public:                               # a print public on AS_OF must match its raw figures
        check_print(p)
    later_splits = [s for s in facts["splits"] if s["effective"] <= as_of]
    basis_note = lambda pub: "".join(f" (per-share figures in this text before the {s['ratio']:g}-for-1 split effective {s['effective']})"
                                     for s in later_splits if pub < s["effective"])
    facts, split_ids = on_basis(facts, as_of)
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["q"] == 4 else 0)
    prints = [p for p in public if guide_fy(p) >= first_fy]
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is public yet")
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage
    h = {**h, "extended": ""}
    for p in prints:
        a = p.get("fy_actual")
        if a and a["fy"] not in reported(h):                      # the 10-K vintage, once out, wins
            y = str(a["fy"])
            h.update(fy_label=a["fy_label"], eps_normalized={**h["eps_normalized"], y: a["eps_normalized"]},
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]},
                     diluted_shares_m={**h["diluted_shares_m"], y: a["diluted_shares_m"]},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_margin=a["margin"], prev_fy_margin_note=a["margin_note"],
                     check_pretax_margin=a["check_pretax_margin"], check_pretax_note=a["check_pretax_note"],
                     prev_fy_sales_growth=a["sales_growth"], prev_fy_kwh_pct=a["kwh_pct"], prev_fy_seg_pct=a["seg_pct"],
                     prev_fy_customers_pct=a["customers_pct"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     sources=h["sources"] + [p["source"]], extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    latest = prints[-1]
    i = public.index(latest)
    assert i > 0, "the previous quarter must be in the fact sheet"
    prev = (public[i - 1]["kwh_pct"], public[i - 1]["quarter"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    excluded = {int(k): v for k, v in h.get("eps_excluded", {}).items()}
    assert not excluded, "no year of the range is excluded (an exclusion needs its encoding first)"
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── guides: every EPS guide is an adjusted range (display only); the last full year's EPS stands (the rollover rule) ──
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    eps_now = eps_hist[last_fy]
    eps_label = (f"{fy_e}: no EPS guide in numbers on a usable basis (the adjusted ranges also remove recurring mark-to-market "
                 f"items), FY{last_fy % 100:02d}'s ${money(eps_now)} (GAAP) stands")
    fwd = [latest["sales_pct"]] * 2
    fwd_label, fwd_short, fwd_period = (f"no {next_q} revenue guide, {latest['quarter']} revenue as reported",
                                        f"{latest['quarter'][:2]} revenue", latest["quarter"])
    if guides:
        g = guides[-1]
        guide_text = (f"{fy_now}: adjusted EPS outlook ({g['doc']}, {g['published']}, display only): {g['display']} — {g['unused']}; "
                      f"no revenue or margin guide in numbers (BASE takes {latest['quarter']} revenue growth)")
    else:
        g = None
        guide_text = (f"{fy_now}: no EPS, revenue or margin guide in numbers in scope (BASE takes {latest['quarter']} revenue growth)")
    margin_guided = False
    fy_margin_base = h["prev_fy_margin"]

    # ── dividend: the latest declared regular rate ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts["dividends"] if d["published"] <= as_of]
    divs.append((h["published"], h["dividend_annual"], h["dividend_note"], None))
    div_pub, dividend, dividend_note, dividend_src = max(divs, key=lambda x: x[0])
    dividend_note += basis_note(div_pub)

    # ── the listing of the date: from its effective date, once published (NYSE: NEE from 2010-06-23) ──
    lst = [x for x in facts["listings"] if x["published"] <= as_of and x["effective"] <= as_of]
    assert lst, (as_of, "no listing in scope")
    exchange, listed = lst[-1]["exchange"], lst[-1]["symbol"]

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
    eps = {**eps_hist, cur_fy: eps_now}
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

    # ── era text: no disruption theme in the registry is live for an electric utility on these dates (the text names none) ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live for a utility", "No disruption theme is live for an electric utility"
    theme_summary = "no disruption theme is live for an electric utility on this date"
    live = sorted(((t["live_from"], k, t["scope"]) for k, t in retro_tool.load_taxonomy()["themes"].items() if t["live_from"] <= as_of))
    if et["live_from"] <= as_of:
        # ENERGY_TRANSITION is live from 2015-12-12 and scoped to oil, gas and coal reserves and refining; NextEra Energy's FY2014-FY2016
        # 10-Ks say NEER holds oil and gas production assets, and their greenhouse gas risk factor puts the theme on the watch list (the
        # XOM and SO rule: company-acknowledged, no market read). No factor pair is added, so only text changes; re-filing needs dated
        # evidence of market pricing for NextEra Energy (retro/README.md, "NEE 2014-2017"). Dates before the live date keep the text below
        assert h.get("transition_quote") and h.get("reserves_quote"), (as_of, "the vintage needs its own 10-K words for the watch list")
        val_word = ("a premium" if pe_now_pctl >= 70 else "a discount to its own history" if pe_now_pctl <= 30 else "near its own median")
        stage = "transition"
        watch = [{"theme": "ENERGY_TRANSITION", "status": "live, company-acknowledged; no market read",
                  "reason": (f"Live: NextEra Energy's own FY20{h['fy_label'][2:]} 10-K says '{h['reserves_quote']}' and, of greenhouse "
                             f"gas limits on its fossil-fuelled units, '{h['transition_quote']}' The stock trades at {close / eps_now:.1f}x "
                             f"{fy_e_s} — {val_word}. Re-file as DISRUPTION_EXPOSED (ENERGY_TRANSITION) only if dated evidence shows the "
                             "market pricing decarbonisation of NextEra Energy's gas reserves and fossil units specifically.")}]
        sig_name = "Energy transition: GHG limits on gas reserves and fossil units"
        trigger = "Greenhouse gas limits strand NEER's oil and gas production assets and fossil units faster than rates and contracts recover them"
        theme_summary = "the energy transition is live and company-acknowledged; no dated evidence ties the multiple to it"
        others = [(lf, k, sc) for lf, k, sc in live if k != "ENERGY_TRANSITION"]
        scopes = ", ".join(f"{k} {'is scoped to' if i == 0 else 'to'} '{sc}'" for i, (_, k, sc) in enumerate(others))
        why = h["why"] + (f"; ENERGY_TRANSITION is live (from {et['live_from']}, scoped to '{et['scope']}'): NEER holds oil and gas "
                          "production assets and the greenhouse gas risk factor puts the theme on the watch list, company-acknowledged, "
                          "with no dated evidence that the market prices it for NextEra Energy (the XOM and SO rule); of the other live "
                          f"themes, {scopes}: none names an electric utility")
    elif [k for _, k, _ in live] == ["OFFSHORE"]:
        why = h["why"] + ("; no disruption theme in the registry is live for an electric utility on this date, so the watch list is empty and "
                          "the 10-K's words on climate change stay here (the PEP obesity rule)")
    else:   # from CLOUD's 2012-10-30: every live theme with its registered scope (the UNH and CB 2014-2017 wording; NEE 2010-2013)
        scopes = ", ".join(f"{k} {'is scoped to' if i == 0 else 'to'} '{sc}'" for i, (_, k, sc) in enumerate(live))
        why = h["why"] + ("; no disruption theme in the registry is live for an electric utility on this date (of the live themes, "
                          f"{scopes}: none names an electric utility), so the watch list is empty and the 10-K's words on climate change "
                          "and greenhouse gas emissions stay here (the PEP obesity rule)")
    kind, pit_risk = "DURABLE", 2
    if g:
        cat3 = (f"(3) The {fy_now} adjusted EPS outlook ({g['doc']}) — display only: the adjusted basis also removes recurring "
                f"mark-to-market items, so FY{last_fy % 100:02d}'s GAAP ${money(eps_now)} anchors the multiple")
    else:
        cat3 = f"(3) A {fy_now} earnings guide in numbers on a usable basis — none in any filing"
    cat4 = (f"(4) FPL's net income — {latest['seg_pct']:+.1f}% in {latest['quarter']} (${latest['raw']['seg_m']:,.0f}M vs "
            f"${latest['raw']['seg_prior_m']:,.0f}M): customers, usage and base rates against O&M and depreciation")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        rt = same_day[-1].get("release_time", "")
        assert "before the open" in rt or "during the session" in rt, (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the close")
        tag = (f"(day of the {same_day[-1]['quarter']} print, public before the open)" if "before the open" in rt else
               f"(day of the {same_day[-1]['quarter']} print, released during the session)")

    # a name changed since the vintage applies from its publication, until a later vintage carries it (the SPGI encoding)
    renames = [n for n in facts["company_names"] if h["published"] < n["published"] <= as_of]
    company = renames[-1]["name"] if renames else h["company"]
    ids = (list(h["sources"]) + [p["source"] for p in prints] + [public[i - 1]["source"]] + ([dividend_src] if dividend_src else [])
           + [lst[-1]["source"]] + split_ids + ([g["source"]] if g else []) + [n["source"] for n in renames])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "W0", "published": as_of, "title": f"Yahoo Finance daily prices, {listed} and S&P 500, truncated at AS_OF",
                    "url": f"https://finance.yahoo.com/quote/{SYMBOL}/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "margin", "margin_bp", "kwh_pct", "seg_pct",
                   "eps_q", "eps_q_prior", "eps_pct", "eps_basis")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    rw = latest["raw"]
    resources = latest["resources_name"]          # the competitive segment as the release names it (NextEra Energy Resources from Q4 2008)
    if latest["kwh_pct"] is None:      # (NEE 2018-2021) the release has no FPL statistics table
        kwh_text = ("FPL energy sales n/r and FPL average customer accounts n/r (the release has no FPL statistics table, and no filing "
                    "of the period tabulates them); ")
    else:
        kwh_text = (f"FPL energy sales {latest['kwh_pct']:+.1f}% ({rw['kwh_prior_m']:,.0f} to {rw['kwh_m']:,.0f} million kWh, the "
                    "statistics table's total: retail, sales to electric utilities, interchange and the change in unbilled sales); "
                    f"FPL average customer accounts {rw['cust_prior_k']:,.0f} to {rw['cust_k']:,.0f} thousand; ")
    gulf_text = ("" if "gulf_m" not in rw else
                 f"Gulf Power net income ${rw['gulf_m']:,.0f}M (acquired 2019-01-01, no year-ago quarter; display only); "
                 if rw["gulf_prior_m"] is None else
                 f"Gulf Power net income ${rw['gulf_prior_m']:,.0f}M to ${rw['gulf_m']:,.0f}M (display only); ")
    volumes = (kwh_text +
               f"FPL net income {latest['seg_pct']:+.1f}% (${rw['seg_prior_m']:,.0f}M to ${rw['seg_m']:,.0f}M); " + gulf_text +
               f"{resources} net income ${rw['fple_prior_m']:,.0f}M to ${rw['fple_m']:,.0f}M (display only); "
               f"revenue {latest['sales_pct']:+.1f}% as reported (${rw['rev_prior_m']:,.0f}M to ${rw['rev_m']:,.0f}M); "
               f"operating income ${rw['opinc_prior_m']:,.0f}M to ${rw['opinc_m']:,.0f}M; EPS: {latest['eps_note']}"
               + basis_note(latest["published"]))
    fy_rev = rev[max(rev)] * (1 + sum(fwd) / 2 / 100)
    fy_rev_label = f"{fwd_label}, applied to the year (no {fy_now} revenue guide)"
    dil_note = f"the release's weighted-average diluted shares ({latest['quarter']}; display only)"
    R = repr
    head = f'''#!/usr/bin/env python3
"""
{listed} Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: {listed})  ·  {h["business_line"]}
Generated by retro/build_nee.py from retro/facts/NEE.json: the constants below are the facts public on
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
               "derived from dated facts by frozen rules (retro/README.md); electric utility signals on FPL Group's own lines")
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
WINDOW_LABEL    = {R(window_label)}   # P/E window: {window[0]} .. AS_OF, on the AS_OF share basis
YEARLY_MIN_PE   = {R(yearly)}   # (calendar year, lowest P/E, date)
VOL_ANNUAL_PCT  = {vol:.3f}   # 1-yr realized, daily log returns
VOL_BETA        = {beta:.2f}    # 1-yr beta vs S&P 500
VOL_52W_LOW     = {low52:.2f}
VOL_52W_HIGH    = {high52:.2f}
REF_LOW         = {px[ref][2]:.2f}   # lowest close of the last 52 weeks, {ref}
REF_LOW_LABEL   = {R(MONTHS[int(ref[5:7]) - 1])}

# ── FACTS: company history ({", ".join(dict.fromkeys(h["sources"]))}, vintage {h["published"]}{h["extended"]}) ──
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}{("; " + h["split_note"]) if h.get("split_note") else ""}
REVENUE_HIST  = {R(rev)}   # FPL Group operating revenues, USD bn
SHARES_HIST   = {R({y: round(v, 1) for y, v in shares.items()})}   # diluted, millions ({h["shares_note"]}; on the AS_OF share basis)
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_margin"]}   # {h["prev_fy_margin_note"]}
CHECK_MARGIN_PCT = {h["check_pretax_margin"]}   # pre-tax margin, for the EPS check: {h["check_pretax_note"]}
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_KWH        = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # no revenue guide: the latest quarter's revenue growth, as reported
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no margin guide, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {fy_rev:.2f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}   # {dil_note}
GROUPS          = {R([tuple(g_) for g_ in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenue {h['prev_fy_sales_growth']:+.1f}%, FPL energy sales {'n/r' if h['prev_fy_kwh_pct'] is None else format(h['prev_fy_kwh_pct'], '+.1f') + '%'}, FPL net income {h['prev_fy_seg_pct']:+.1f}%, FPL customer accounts {'n/r' if h['prev_fy_customers_pct'] is None else format(h['prev_fy_customers_pct'], '+.1f') + '%'}{(' (' + h['franchise_note'] + ')') if h.get('franchise_note') else ''}; {latest['quarter']} operating margin {latest['margin']:.1f}% ({latest['margin_bp']:+.1f}bp)")}
BALANCE_TEXT    = {R(f"{h['fy_label']} year-end cash ${h['cash_b']:.3f}B, {h['fcf_label']} free cash flow ${h['fcf_b']:.2f}B ({h['fcf_note']}), dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
VOLUMES_TEXT    = {R(volumes)}
CAPITAL_RETURN  = {R(h["cash_return_text"])}
THEME_FACTORS   = {R(factors)}
THEME_SIGNAL_NAME    = {R(sig_name)}
THEME_SIGNAL_TRIGGER = {R(trigger)}
THEME_SUMMARY        = {R(theme_summary)}
CATALYST_3      = {R(cat3)}
CATALYST_4      = {R(cat4)}
'''
    os.makedirs(os.path.join(out, as_of), exist_ok=True)
    with open(os.path.join(out, as_of, "model.py"), "w", encoding="utf-8") as fh:
        fh.write(head + (nr_engine(engine) if latest["kwh_pct"] is None else engine))
    return tag, latest["quarter"], stage


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dates", nargs="*")
    ap.add_argument("--weekly", nargs=2, metavar=("START", "END"))
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/NEE)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    with open(ENGINE2, encoding="utf-8") as fh:        # the committed None-tolerant copy must be nr_engine(ENGINE), line for line
        assert fh.read() == nr_engine(engine), "nee2_engine.py.tmpl must equal nr_engine(nee_engine.py.tmpl)"
    raw, spx = load_series(SYMBOL), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<34}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
