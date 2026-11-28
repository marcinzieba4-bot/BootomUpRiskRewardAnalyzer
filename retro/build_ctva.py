#!/usr/bin/env python3
"""
Build CTVA retrospective models from the dated fact sheet (retro/facts/CTVA.json).

The CTVA sibling of build_bkr.py's new-listing builder (build_bhge): the same frozen rules (retro method r2), the same weekly dates and
the same market statistics, with seed and crop protection signals (retro/templates/ctva_engine.py.tmpl). For each as-of date the
builder
  1. selects only the history vintage, prints, guides and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, from the listing (the listing rule of method r2), each close
     as traded (the 'distributions' rule below),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Corteva, Inc. was distributed by DowDuPont on 2019-06-01 and began regular-way trading on the NYSE as CTVA on 2019-06-03; its own P/E
exists only from that day (retro/README.md, "CTVA"). EPS is GAAP diluted EPS from continuing operations: the company's Operating EPS
excludes the amortization of intangibles and non-operating pension and OPEB benefits, which recur, so it does not exclude only one-offs
(the NKE FY2007, AVGO 2009, PFE and BMY rule) and is shown in the guide line only. 2018 and 2019 are losses with no figure excluding only
one-offs, so they are excluded; 2017 is reported only as two periods; the first full year of EPS is 2020, so no date can be built before
the Q4 2020 release (8-K accepted 2021-02-03 17:08 ET, public from 2021-02-04; the first weekly date is 2021-02-05).

Corteva guides fiscal-year net sales in dollars and Operating EBITDA and Operating EPS (non-GAAP), never a quarter and never GAAP EPS, so:
  - current-FY EPS: the last full year's GAAP EPS stands (the PFE rule for a year with no reported-EPS guide),
  - BASE growth and the growth factor: the latest fiscal-year net sales guide, read against the last year's net sales (the AAPL and PFE
    dollar-level rule); a year with no net sales guide in numbers (FY2026) takes the latest quarter's net sales growth as reported,
  - guided margin step: none (no margin guide on the GAAP basis); the margin signal uses the latest quarter's change.
The Operating EBITDA and Operating EPS ranges are shown in the guide line, display only.

Prices: Yahoo books the 2026-10-01 distribution of the seed business as a 6665:1000 split. It is a distribution, so its factor is undone
for the days before it and every close is the price as traded (the MAR, PFE, BMY and SO 'distributions' rule). No date on or after it is
built: from that day the listed company's history is the crop protection carve-out of a reverse spin-off, with pro forma EPS only, and
building it needs a rule the owner has not set (retro/README.md, "CTVA").

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it is
the first trading day after it. Every earnings 8-K of the series was accepted after the close, so each print is dated the next trading
day and the week's date is the trading day after that (the AAPL rule); a print dated on the week's last trading day meets that day's
close (release_time).

Output goes to staging/retrospective/CTVA until the series is added to the archive (--out archive/retrospective/CTVA).

Usage
  python3 retro/build_ctva.py --weekly 2021-02-01 2026-09-25      # 295 dates, 2021-02-05 .. 2026-09-25
  python3 retro/build_ctva.py 2021-02-05
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/CTVA/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "CTVA.json")
ENGINE = os.path.join(HERE, "templates", "ctva_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "CTVA")
SYMBOL = "CTVA"
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"seed_org": (-4, -1, 3, 6), "cp_org": (-4, 1, 6, 11), "price": (-1, 0, 2, 3),
                     "gross_margin": (-70, 210, 490, 770), "pretax_margin": (-440, 130, 700, 4540)}
RULE_T_KEYS = {"seed_org": (1, False), "cp_org": (1, False), "price": (1, False), "gross_margin": (10, False), "pretax_margin": (10, False)}
PRINT_KEYS = {"quarter", "fy", "q", "published", "source", "release", "release_time", "period_end", "raw", "sales_b", "sales_pct",
              "seed_org_pct", "cp_org_pct", "price_pct", "vol_pct", "fx_pct", "org_pct", "seed_pct", "cp_pct", "gross_margin",
              "gross_margin_bp", "ptm", "ptm_bp", "eps_q", "eps_q_prior", "diluted_shares_m", "cash_b", "sales_note", "segments_note",
              "margin_note", "eps_note", "cash_note", "next_print", "fy_actual", "prev_seed_org"}
FY_KEYS = {"fy", "fy_label", "eps_normalized", "excluded_note", "revenue_usd_b", "diluted_shares_m", "normalization_note", "op_margin",
           "op_margin_note", "sales_growth", "seed_growth", "cp_growth", "seed_org_pct", "cp_org_pct", "org_pct", "check_pretax_margin",
           "check_pretax_note", "tax_rate", "tax_note", "groups", "groups_basis", "one_off_test"}
GUIDE_KEYS = {"fy", "published", "source", "doc", "release_time", "rev_guide_m", "rev_guide_note", "display", "rev_none"}


def fiscal_year_end(n):
    """Corteva's fiscal year n is the calendar year n."""
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
    pct = lambda a, b: (b / a - 1) * 100
    gm = lambda rev, c: (rev - c) / rev * 100
    g1, g0 = gm(r["rev_m"], r["cogs_m"]), gm(r["rev_prior_m"], r["cogs_prior_m"])
    m1, m0 = r["pti_m"] / r["rev_m"] * 100, r["pti_prior_m"] / r["rev_prior_m"] * 100
    want = {"sales_b": round(r["rev_m"] / 1000, 4), "sales_pct": round(pct(r["rev_prior_m"], r["rev_m"]), 1),
            "seed_pct": round(pct(r["seed_prior_m"], r["seed_m"]), 1), "cp_pct": round(pct(r["cp_prior_m"], r["cp_m"]), 1),
            "gross_margin": round(g1 + 0.0, 2), "gross_margin_bp": round((g1 - g0) * 100, 1),
            "ptm": round(m1 + 0.0, 2), "ptm_bp": round((m1 - m0) * 100, 1),
            "seed_org_pct": r["pvc_seed"]["org_pct"], "cp_org_pct": r["pvc_cp"]["org_pct"], "price_pct": r["pvc_total"]["price_pct"],
            "cash_b": round((r["cash_m"] + r["mkt_sec_m"]) / 1000, 3)}
    for k, v in want.items():
        assert abs(p[k] - v) < 1e-9, (p["quarter"], k, p[k], v)
    for s in ("", "_prior"):                       # the two segments make net sales (rounded figures: within 1)
        assert abs(r["seed" + s + "_m"] + r["cp" + s + "_m"] - r["rev" + s + "_m"]) <= 1, (p["quarter"], "segments", s)
    a = p.get("fy_actual")
    if a:
        assert set(a) <= FY_KEYS, (p["quarter"], sorted(set(a) - FY_KEYS), "a full-year field with no encoding yet; decide one first")
        t = a["one_off_test"]
        kept = a["eps_normalized"] is not None
        # a year is kept at GAAP unless it is a loss or its listed one-off charges (after tax) exceed its income from continuing operations
        assert t["distorted"] == (t["items_after_tax_m"] > t["income_cont_attributable_m"]), (p["quarter"], "the one-off test")
        assert kept == (not t["distorted"] and a["eps_normalized"] > 0), (p["quarter"], "the year's EPS and the one-off test disagree")


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    listing = facts["listing"]
    first_day = listing["first_trading_day"]
    if as_of < first_day:
        sys.exit(f"{as_of}: Corteva's common stock began regular-way trading on {first_day}; no P/E of its own exists before it (the listing rule)")
    assert listing["published"] <= as_of
    chart = retro_tool.chart(SYMBOL)
    off = chart["meta"]["gmtoffset"]
    ydate = lambda v: dt.datetime.fromtimestamp(v["date"] + off, dt.timezone.utc).date().isoformat()
    dist = {x["effective"]: x for x in facts["distributions"]}
    splits = list(chart.get("events", {}).get("splits", {}).values())
    assert all(ydate(v) in dist for v in splits) and not facts.get("splits"), "a split needs its encoding first (the UNP rule)"
    px = dict(raw)
    # a distribution is not a split: Yahoo's factor is undone for the days before it, so every close is the price as traded (the MAR, PFE,
    # BMY and SO 'distributions' rule); no date on or after the 2026 distribution is built (the reverse spin-off: see the module note)
    for day, x in dist.items():
        ev = [v for v in splits if ydate(v) == day]
        num, den = x["yahoo_ratio"]
        assert len(ev) == 1 and (ev[0]["numerator"], ev[0]["denominator"]) == (num, den), (day, "Yahoo's factor")
        if as_of >= day:
            sys.exit(f"{as_of}: from {day} the listed company is the crop protection carve-out of a reverse spin-off, whose only per-share "
                     "history is pro forma; no date on or after it is built (retro/README.md, 'CTVA')")
        px = {d: (tuple(v * num / den for v in hlc) if d < day else hlc) for d, hlc in px.items()}
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no annual history of Corteva is public yet")
    for v in vintages:                                 # the fiscal calendar the filings state must match the rule
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    for g in [g for g in facts["guides"] if g["published"] <= as_of]:
        assert set(g) <= GUIDE_KEYS, (g["doc"], "a guide field with no encoding yet; decide one first")
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
        sys.exit(f"{as_of}: the CTVA builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
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
                     prev_fy_sales_growth=a["sales_growth"], prev_fy_seed_growth=a["seed_growth"], prev_fy_cp_growth=a["cp_growth"],
                     check_pretax_margin=a["check_pretax_margin"], check_pretax_note=a["check_pretax_note"],
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     groups=a["groups"], groups_basis=a["groups_basis"],
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    latest = prints[-1]
    prev = tuple(latest["prev_seed_org"]) if latest["prev_seed_org"] else (None, "no earlier print")
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    excluded = {int(k): v for k, v in h.get("eps_excluded", {}).items()}
    if not eps_hist:                                   # 2018 and 2019 are losses: no P/E, no model
        sys.exit(f"{as_of}: no full year of Corteva's EPS is public yet, so the stock has no P/E of its own (method r2)")
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)        # the last full year in the history: cur_fy - 1 unless that year is excluded
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── no GAAP EPS guide: the last full year's EPS stands (the PFE rule); Operating EPS and EBITDA guides are display only ──
    eps_now = eps_hist[last_fy]
    eps_label = (f"{fy_e}: no reported (GAAP) EPS guide, FY{last_fy % 100:02d}'s ${money(eps_now)} stands" + "".join(
        f" (FY{y % 100:02d} is excluded: {excluded[y]})" for y in range(last_fy + 1, cur_fy)))
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    gr = next((g for g in reversed(guides) if "rev_guide_m" in g), None)      # the latest net sales guide in numbers for the year
    gl = guides[-1] if guides else None                                        # the latest guide of any kind (display)
    rev_last = {int(k): v for k, v in h["revenue_usd_b"].items()}
    if gr:
        assert cur_fy - 1 in rev_last, (as_of, "the guide needs the last year's net sales")
        fwd = [round((x / 1000 / rev_last[cur_fy - 1] - 1) * 100, 1) for x in gr["rev_guide_m"]]
        fwd_label = (f"FY{cur_fy} net sales guide ${gr['rev_guide_m'][0] / 1000:.1f}-{gr['rev_guide_m'][1] / 1000:.1f}B ({gr['doc']}) on "
                     f"FY{(cur_fy - 1) % 100:02d} ${rev_last[cur_fy - 1]:.3f}B, no {next_q} guide")
        fwd_short, fwd_period = f"FY{cur_fy % 100:02d} net sales guide", f"FY{cur_fy}"
        guide_text = (f"{fy_now}: net sales guided in the {gr['doc']}: {gr['rev_guide_note']} (BASE takes the guide's growth on "
                      f"FY{(cur_fy - 1) % 100:02d} net sales; no GAAP EPS or margin guide)")
    else:
        fwd = [latest["sales_pct"]] * 2
        fwd_label, fwd_short, fwd_period = (f"no {fy_now} net sales guide in numbers, {latest['quarter']} net sales as reported",
                                            f"{latest['quarter'][:2]} net sales", latest["quarter"])
        guide_text = f"{fy_now}: no net sales guide in numbers (BASE takes {latest['quarter']} net sales growth as reported)"
    if gl:
        guide_text += f"; the {gl['doc']} guides {gl['display']}"
    margin_guided = False                          # no margin guide on the GAAP basis: no guided step
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
    # an excluded year's own days leave the window (2019, a loss)
    gone = sorted({fy(d) for d in window} & set(excluded))
    window = [d for d in window if fy(d) not in excluded]
    assert all(fy(d) in eps for d in window), (as_of, "P/E window needs EPS for every fiscal year")
    years = (dt.date.fromisoformat(as_of) - dt.date.fromisoformat(window[0])).days / 365.25
    assert years >= 1, (as_of, "a window under a year needs the trading-day label first (the AVGO encoding)")
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

    # ── era-dependent text, from facts only: no disruption theme in the registry covers seed and crop protection ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none in scope", "No live disruption theme covers seed and crop protection"
    theme_summary = ("no theme in the registry covers seed and crop protection (GLP1 is scoped to snacks, beverages and devices, "
                     "ENERGY_TRANSITION to oil, gas and coal reserves and refining); none has dated evidence")
    key_tail = ("Planted area, farm income and the channel drive sales, by the company's own account;\n"
                "  the bear needs them to fall, not one quarter's timing.")
    why = h["why"]
    if h.get("why_theme_tail"):
        why += ("; no disruption theme in the registry covers seed and crop protection (GLP1 is scoped to snacks, beverages and devices, "
                "ENERGY_TRANSITION to oil, gas and coal reserves and refining), so the weather and climate wording stays here")
    kind, pit_risk = "DURABLE", 2
    cat3 = (f"(3) The {fy_now} guide — " + (f"{gr['rev_guide_note']} ({gr['doc']})" if gr else "no net sales guide in numbers")
            + (f"; {gl['display']}" if gl else ""))
    cat4 = f"(4) Free cash flow — {h['fcf_label']} {h['fcf_note']}"

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"
    same_guide = [g for g in guides if g["published"] == as_of and "release_time" in g]
    for g in same_guide:
        assert "before the open" in g["release_time"], (as_of, g["doc"], "released on AS_OF, not before the open")

    company, exchange, listed = h["company"], h["exchange"], h["symbol"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]]] + [listing["source"]]
           + ([dividend_src] if dividend_src else []) + ([gr["source"]] if gr else []) + ([gl["source"]] if gl else []))
    sources = [dict(id=i, **{k: v for k, v in facts["sources"][i].items()}) for i in dict.fromkeys(ids)]
    sources.append({"id": "A0", "published": as_of,
                    "title": f"Yahoo Finance daily prices, {company} common stock ({exchange}: {listed}) and S&P 500, truncated at AS_OF",
                    "url": f"https://finance.yahoo.com/quote/{SYMBOL}/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution "
                                f"since the listing on {first_day}"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "seed_org_pct", "cp_org_pct", "price_pct", "gross_margin",
                   "gross_margin_bp", "ptm", "ptm_bp", "eps_q", "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    activity = (f"Activity: {latest['sales_note']}; by segment: {latest['segments_note']}; {latest['margin_note']}; "
                f"EPS {latest['eps_note']}")
    fy_rev = rev[max(rev)] * (1 + sum(fwd) / 2 / 100)
    fy_rev_label = f"{fwd_label}, applied to the year (no {fy_now} net sales guide)" if not gr else f"{fwd_label}: the guide's midpoint"
    franchise_q = f"{latest['quarter'].split()[0]} gross margin {latest['gross_margin']:.2f}% ({latest['gross_margin_bp']:+.0f}bp)"
    fcf_text = f"${h['fcf_b']:.2f}B" if h["fcf_b"] >= 0 else f"$({-h['fcf_b']:.2f})B"
    R = repr
    head = f'''#!/usr/bin/env python3
"""
{listed} Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: {listed})  ·  {h["business_line"]}
Generated by retro/build_ctva.py from retro/facts/CTVA.json: the constants below are the facts public on
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
               "derived from dated facts by frozen rules (retro/README.md); seed and crop protection signals")
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
REVENUE_HIST  = {R(rev)}   # net sales, USD bn
SHARES_HIST   = {R({y: round(v, 1) for y, v in shares.items()})}   # {h["shares_note"]}
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # pre-tax margin, {h["prev_fy_op_margin_note"]}
CHECK_PRETAX_MARGIN = {h["check_pretax_margin"]}   # {h["check_pretax_note"]}
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}
KIND_TEXT     = {R(h["kind_text"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_SEED       = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # the fiscal-year net sales guide's growth, else the latest quarter's net sales growth as reported
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no margin guide on the GAAP basis, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {fy_rev:.2f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} net sales {h['prev_fy_sales_growth']:+.1f}%, Seed {h['prev_fy_seed_growth']:+.1f}%, Crop Protection {h['prev_fy_cp_growth']:+.1f}%; {franchise_q}")}
BALANCE_TEXT    = {R(f"Cash and marketable securities ${latest['cash_b']:.2f}B, {h['fcf_label']} free cash flow {fcf_text}, dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/CTVA)")
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
