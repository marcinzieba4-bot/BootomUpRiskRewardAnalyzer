#!/usr/bin/env python3
"""
Build PEP retrospective models from the dated fact sheet (retro/facts/PEP.json).

The PEP sibling of build_nke.py: the same frozen rules (retro method r2), the same weekly dates and the same market
statistics, with beverage and convenient-food signals (retro/templates/pep_engine.py.tmpl). For each as-of date the
builder
  1. selects only the history vintage, prints, guides and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, as traded on each day (PepsiCo has not split
     since 1996, before every fact in the fact sheet, so Yahoo's series is the price as traded),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

PepsiCo's fiscal year ends on the last Saturday of December (52 weeks, 53 every five or six years); the first three quarters
have 12 weeks and the fourth 16 (17). The method r2 inputs map with the rules decided before any PEP date was built or scored
(retro/README.md, "PEP"):
  - current-FY EPS: an EPS guide in numbers on a usable basis when the latest guide for the year states one; PepsiCo's guides
    of 2007-2010 are a one-sided bound ("at least $3.72", the UNP and LOW rule: no field), words ("mid- to high-single-digit",
    the UNP 2016 rule) or a range on its "core" basis, which also removes the commodity mark-to-market net impact, a recurring
    item (the 2008 core rule below): none gives a field, so the last full year's EPS stands (the rollover rule) and every guide
    is shown in the guide line only,
  - forward revenue growth: no revenue guide in numbers, so the latest quarter's net revenue growth excluding currency
    (lc_pct: the growth the release states less the currency effect the release or the quarter's 10-Q states, or the growth on
    a constant-currency basis the release states; the reported growth where no filing states the quarter's currency effect),
  - guided margin step: none (no operating-margin guide in numbers); the margin signal uses the latest quarter's change.
EPS is diluted EPS from continuing operations, each year from the latest 10-K that reports it, and a company-published figure
excluding one-offs only replaces it (the ACN rule). PepsiCo's "core" figures from 2008 also exclude the mark-to-market net
impact on commodity hedges, which recurs in every period and is "subsequently reflected in division results" (a timing basis,
not a one-off: the AAPL subscription-accounting and NKE FY2007 rule), so from 2008 they do not replace GAAP; nothing is derived.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings
release, where it is the first trading day after it. Every PepsiCo earnings 8-K of the period was accepted before the close
on its release day (the conference call at 11 a.m. or 9 a.m. ET), so a print is dated its release day; a print released on
the week's last trading day meets its close only when it was public before the open (release_time), the AAPL 2011 rule.

Output goes to staging/retrospective/PEP until the series is added to the archive (--out archive/retrospective/PEP).

Usage
  python3 retro/build_pep.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_pep.py 2008-02-08
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/PEP/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "PEP.json")
ENGINE = os.path.join(HERE, "templates", "pep_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "PEP")
# the guide fields this builder has an encoding for: every PepsiCo guide of the period is display only ('display': the figures
# as published, 'unused': why no input takes them); any other field (a number an input would read) needs its encoding first
GUIDE_KEYS = {"fy", "published", "source", "doc", "display", "unused"}
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"servings": (3, 4, 5, 7), "gross_margin": (-260, -130, 0, 150), "revenue": (-26, -10, 6, 10), "inventory_gap": (65, 32, -1, -17), "op_margin": (-300, -130, 40, 230)}
RULE_T_KEYS = {"servings": (1, False), "gross_margin": (10, False), "revenue": (1, False), "inventory_gap": (1, True),
               "op_margin": (10, False)}           # (rounding unit, lower is better)


def fiscal_year_end(n):
    """PepsiCo's fiscal year n ends on the last Saturday of December of year n."""
    d = dt.date(n, 12, 31)
    return d - dt.timedelta(days=(d.weekday() - 5) % 7)


def fiscal_year(day):
    """The fiscal year a calendar day belongs to."""
    d = dt.date.fromisoformat(day)
    return d.year if d <= fiscal_year_end(d.year) else d.year + 1


def rule_t(rt):
    """Rule T thresholds from the annual values the filings report (ten, seven for servings; the AVGO formula on fewer than
    ten): XBULL best, BULL median, BASE worst, BEAR one median-to-worst step beyond the worst; rounded half up to whole percent
    or points and to 10 bp."""
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
    inv = pct(r["inventory_prior_m"], r["inventory_m"])
    want = {"sales_pct": round(sales, 1), "gross_margin": r2(gm), "gross_margin_bp": round((gm - gm0) * 100, 1),
            "op_margin": r2(om), "op_margin_bp": round((om - om0) * 100, 1), "inventory_pct": round(inv, 1),
            "inventory_gap_pp": round(inv - sales, 1)}
    for k, v in want.items():
        assert abs(p[k] - v) < 1e-9, (p["quarter"], k, p[k], v)


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    chart = retro_tool.chart("PEP")
    fx = retro_tool.split_factor(chart, as_of)
    assert fx == 1.0, "PepsiCo has not split since 1996: a split factor other than 1 needs its encoding first"
    px = dict(raw)
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    for g in [g for g in facts["guides"] if g["published"] <= as_of]:      # a guide public on AS_OF may carry only encoded fields
        assert set(g) <= GUIDE_KEYS, (g["doc"], "a guide field with no encoding yet; decide one first")
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        check_print(p)
    facts, split_ids = on_basis(facts, as_of)      # no split in the fact sheet: an identity, kept for the shared shape
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    # prints published by AS_OF that report a fiscal year after the history (a Q4 print reports the year just ended, so it
    # stays in scope after the 10-K that follows it)
    first_fy = max(int(k) for k in h["eps_normalized"]) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    prints = [p for p in facts["prints"] if p["published"] <= as_of and guide_fy(p) >= first_fy]
    # no disruption theme in taxonomy_eras.json is live for a beverage and convenient-food company in 2008-2010 (GLP1 from
    # 2023-08-08; OFFSHORE is scoped to IT services, ECOMMERCE to physical retail, the others to other industries): any event
    # needs its encoding decided first
    events = [e for e in facts["events"] if e["published"] <= as_of]
    if events:
        sys.exit(f"{as_of}: the PEP builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
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
                     prev_fy_pretax_margin=a["pretax_margin"], prev_fy_pretax_margin_note=a["pretax_margin_note"],
                     prev_fy_gross_margin=a["gross_margin"], prev_fy_sales_growth=a["sales_growth"],
                     prev_fy_servings_pct=a["servings_pct"], prev_fy_servings_note=f'{p["quarter"]} release',
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    latest = prints[-1]
    prev = (prints[-2]["servings_pct"], prints[-2]["quarter"]) if len(prints) > 1 else (h["prev_q_servings_pct"], h["prev_q_label"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    cur_fy = max(eps_hist) + 1
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── guides for the current fiscal year: display only (bounds, words, core ranges); no input ──
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    eps_now = eps_hist[cur_fy - 1]                 # no usable EPS guide: the last full year's EPS stands (rollover rule)
    eps_label = f"{fy_e}: no EPS guide in numbers on a usable basis, FY{(cur_fy - 1) % 100:02d}'s ${money(eps_now)} stands"
    if guides:
        g = guides[-1]
        guide_text = f"{fy_now} outlook ({g['doc']}, display only): {g['display']} — {g['unused']}"
    else:
        guide_text = f"{fy_now}: no outlook in scope yet"
    # no revenue guide in numbers: the latest quarter's net revenue growth excluding currency (method r2's LC basis)
    fwd = [latest["lc_pct"]] * 2
    fwd_label, fwd_short, fwd_period = (f"{latest['quarter']} net revenue ex-currency", f"{latest['quarter'].split()[0]} rev ex-FX",
                                        latest["quarter"])
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

    # ── era-dependent text: no disruption theme is live for this business on any date of the period ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
    key_tail = ("Commodity inflation shows up in gross margin first; the bear needs\n"
                "  servings to fall as pricing rises.")
    theme_summary = "no disruption theme has dated evidence"
    cat3 = (f"(3) The outlook — {guides[-1]['doc']}: {guides[-1]['display']} (display only)" if guides else
            f"(3) A {fy_now} outlook — none in scope yet")
    cat4 = (f"(4) Inventories — {latest['inventory_pct']:+.1f}% against net revenue {latest['sales_pct']:+.1f}% in {latest['quarter']} "
            f"({latest['inventory_gap_pp']:+.1f}pp): commodity costs and acquisitions sit in them")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    # a print dated AS_OF meets AS_OF's close only if it was public before the open (the week's last trading day)
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    company = h["company"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])]
           + [g["source"] for g in guides] + ([dividend_src] if dividend_src else []) + split_ids)
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "A0", "published": as_of, "title": "Yahoo Finance daily prices, PEP and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/PEP/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "lc_pct", "servings_pct", "gross_margin", "gross_margin_bp",
                   "op_margin", "op_margin_bp", "inventory_b", "inventory_pct", "inventory_gap_pp", "eps_q", "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    eps_note = f"; {latest['eps_note']}" if latest.get("eps_note") else ""
    vol_text = (f"Volume: servings {latest['servings_pct']:+.1f}% ({latest['servings_note']}); net revenue {latest['sales_pct']:+.1f}% "
                f"reported, {latest['lc_pct']:+.1f}% excluding currency ({latest['lc_note']}){eps_note}")
    R = repr
    head = f'''#!/usr/bin/env python3
"""
PEP Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} (NYSE: PEP)  ·  {h["business_line"]}
Generated by retro/build_pep.py from retro/facts/PEP.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "PEP"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); beverage and convenient-food signals")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts and events above.
PIT_PROFILE = {{
    "kind": "DURABLE",
    "risk": 2,
    "why": {R(h["why"])},
    "theme_watch": {R(watch)},
    "evidence": [],
}}

# ── FACTS: market (prices truncated at AS_OF, as traded on each day) ──────────
CURRENT_PRICE   = {close:.2f}   # USD, NYSE close {as_of}
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
EPS_NORM      = {R(eps_hist)}   # {h["normalization"]}
REVENUE_HIST  = {R(rev)}   # net revenue, USD bn
SHARES_HIST   = {R(shares)}   # diluted, millions
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # operating margin, {h["prev_fy_op_margin_note"]}
CHECK_PRETAX_MARGIN = {h["prev_fy_pretax_margin"]}   # pre-tax margin, {h["prev_fy_pretax_margin_note"]} (the EPS check only)
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} outlook ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_SERVINGS   = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # no revenue guide in numbers: the latest quarter's net revenue growth excluding currency
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no margin guide, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {rev[max(rev)] * (1 + sum(fwd) / 2 / 100):.2f}
FY_REVENUE_LABEL = {R(f"{fwd_label}, applied to the year (no {fy_now} revenue guide in numbers)")}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} net revenue {h['prev_fy_sales_growth']:+.1f}%, servings {h['prev_fy_servings_pct']:+.1f}% ({h['prev_fy_servings_note']}); {latest['quarter'].split()[0]} gross margin {latest['gross_margin']:.2f}% ({latest['gross_margin_bp']:+.0f}bp)")}
BALANCE_TEXT    = {R(f"Cash and short-term investments ${latest['cash_b']:.2f}B, {h['fcf_label']} free cash flow ${h['fcf_b']:.2f}B, dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
VOLUME_TEXT     = {R(vol_text)}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/PEP)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("PEP"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<34}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
