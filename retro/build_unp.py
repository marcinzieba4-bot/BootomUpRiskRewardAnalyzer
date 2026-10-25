#!/usr/bin/env python3
"""
Build UNP retrospective models from the dated fact sheet (retro/facts/UNP.json).

The UNP sibling of build_acn.py: the same frozen rules (retro method r2), the same weekly dates and the same market
statistics, with railroad signals (retro/templates/unp_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints, guides, dividend and events whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, as traded on each day (Yahoo's
     split-adjusted series with the later splits undone), so the price and the per-share facts share one basis,
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Union Pacific gives its numeric outlook in the 10-K and in occasional 8-Ks, not in the quarterly releases, so guides
are a dated list of their own. Fallbacks for what it does not guide (decided before any UNP outcome was computed):
  - no numeric EPS guide for the current year: the last full year's EPS stands (the rollover rule: days past the
    last guided year keep that year's EPS),
  - no numeric revenue guide: BASE growth and the growth factor use the latest quarter's commodity revenue growth,
  - no numeric operating-ratio guide (words, or a one-sided bound such as "below 80%"): no guided margin step, and
    the operating-ratio signal uses the latest quarter's year-on-year change.
A stock split restates, from its effective date, every per-share fact published before it (divided by the ratio) and
every share count (multiplied by it); the prices of the whole window are on the AS_OF share basis.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings
release, where it is the first trading day after it.

Output goes to staging/retrospective/UNP until the series is added to the archive (--out archive/retrospective/UNP).

Usage
  python3 retro/build_unp.py --weekly 2008-01-01 2008-03-30
  python3 retro/build_unp.py 2008-02-29
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/UNP/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "UNP.json")
ENGINE = os.path.join(HERE, "templates", "unp_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "UNP")


def pct_range(lo, hi):
    return f"{lo:+g}%" if lo == hi else f"+{lo:g}-{hi:g}%" if lo >= 0 else f"{lo:+g}% to {hi:+g}%"


def money(x):
    """$ amount with two decimals, three when a split leaves a half cent (7.75 / 2 = 3.875)."""
    t = f"{x:.3f}"
    return t[:-1] if t.endswith("0") else t


def on_basis(facts, as_of):
    """The fact sheet with every per-share fact on the AS_OF share basis: a split effective on or before AS_OF divides
    per-share values published before its effective date by its ratio and multiplies share counts by it."""
    f = copy.deepcopy(facts)
    splits = [s for s in f.get("splits", []) if s["effective"] <= as_of]
    k = lambda pub: math.prod(s["ratio"] for s in splits if pub < s["effective"])
    for v in f["history_vintages"]:
        # a vintage takes each year from the latest filing that reports it, so a year can predate a split the vintage
        # follows: eps_published / shares_published give such a year's own publication date (default: the vintage's)
        ke = {y: k(v.get("eps_published", {}).get(y, v["published"])) for y in v["eps_normalized"]}
        ks = {y: k(v.get("shares_published", {}).get(y, v["published"])) for y in v["diluted_shares_m"]}
        v["eps_normalized"] = {y: e / ke[y] for y, e in v["eps_normalized"].items()}
        v["diluted_shares_m"] = {y: n * ks[y] for y, n in v["diluted_shares_m"].items()}
        v["dividend_annual"] /= k(v["published"])
        hit = [s for s in splits if any(v.get("eps_published", {}).get(y, v["published"]) < s["effective"] for y in v["eps_normalized"])]
        if hit:
            restated = [y for y in sorted(ke) if ke[y] != 1]
            span = "" if len(restated) == len(ke) else f" on {restated[0]}-{restated[-1]} (published before it)"
            v["split_note"] = "; ".join(f"per share ÷{s['ratio']} for the {s['ratio']}-for-1 split effective {s['effective']} ({s['source']}){span}"
                                        for s in hit)
    for p in f["prints"]:
        r = k(p["published"])
        p["eps_q"], p["eps_q_prior"], p["diluted_shares_m"] = p["eps_q"] / r, p["eps_q_prior"] / r, p["diluted_shares_m"] * r
        if "fy_actual" in p:
            p["fy_actual"]["eps_normalized"] /= r
            p["fy_actual"]["diluted_shares_m"] *= r
    for g in f["guides"]:
        r = k(g["published"])
        if r != 1 and "eps_guide" in g:
            g["eps_guide_note"] = "; ".join(x for x in (g.get("eps_guide_note"), f"${money(g['eps_guide'][0])}-{money(g['eps_guide'][1])} before the split") if x)
            g["eps_guide"] = [e / r for e in g["eps_guide"]]
        if r != 1 and "q_eps_guide" in g:
            g["q_eps_guide"]["range"] = [e / r for e in g["q_eps_guide"]["range"]]
    for d in f["dividends"]:
        d["quarterly"] /= k(d["published"])
    return f, [s["source"] for s in splits]


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    # every price of the window on the AS_OF share basis: Yahoo's split-adjusted series times the splits after AS_OF,
    # so the AS_OF close is the price as traded and the per-share facts below share its basis
    fx = retro_tool.split_factor(retro_tool.chart("UNP"), as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + retro_tool.chart("UNP")["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat()
                    for v in retro_tool.chart("UNP").get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo_splits for s in facts.get("splits", [])), "a split's effective date must match the price data"
    facts, split_ids = on_basis(facts, as_of)
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    # prints published by AS_OF that report a fiscal year after the history (a Q4 print reports the year just ended,
    # so it stays in scope after the 10-K that follows it); events published since the vintage
    first_fy = max(int(k) for k in h["eps_normalized"]) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    prints = [p for p in facts["prints"] if p["published"] <= as_of and guide_fy(p) >= first_fy]
    events = [e for e in facts["events"] if e["published"] <= as_of and (h["published"] <= e["published"] or "doc" not in e)]
    if events:
        sys.exit(f"{as_of}: the UNP builder has no theme encoding yet; decide one before adding events")
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
                     prev_fy_op_margin=a["op_margin"], prev_fy_op_ratio=a["op_ratio"],
                     prev_fy_revenue_growth=a["revenue_growth"], prev_fy_carloads_pct=a["carloads_pct"],
                     net_interest_b=a["net_interest_b"], net_interest_note=f'FY{y[2:]} from {p["source"]}',
                     tax_rate=a["tax_rate"], tax_note=f'FY{y[2:]} effective rate; no tax-rate guide ({p["source"]})',
                     fcf_b=p.get("fcf_b", h.get("fcf_b")), fcf_label=a["fy_label"],
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    latest = prints[-1]
    prev = (prints[-2]["carloads_pct"], prints[-2]["quarter"]) if len(prints) > 1 else (h["prev_q_carloads_pct"], h["prev_q_label"])
    # a renamed reporting line takes the new name from the first print that uses it, otherwise the vintage's
    revenue_line = next((p["revenue_line"] for p in reversed(prints) if "revenue_line" in p), h["revenue_line"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}   # reported history only: the rules use this
    cur_fy = max(eps_hist) + 1
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = int(latest["quarter"][1])
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── guides for the current fiscal year, each field from the latest guide that states it ──
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    stated = lambda k: next((g for g in reversed(guides) if k in g), None)
    ge, gr, gv = stated("eps_guide"), stated("rev_guide"), stated("volume_guide")
    if ge:
        eps_now = round(sum(ge["eps_guide"]) / 2, 3)
        eps_label = f"{fy_e} EPS, guide midpoint"
    else:                                    # no numeric EPS guide: the last full year's EPS stands (rollover rule)
        eps_now = eps_hist[cur_fy - 1]
        eps_label = f"{fy_e}: no numeric EPS guide yet, FY{(cur_fy - 1) % 100:02d}'s ${money(eps_now)} stands"
    if gr:
        fwd, fwd_label, fwd_short = gr["rev_guide"], f"{fy_now} {gr['rev_guide_label']}", f"{fy_now} guide"
    else:                                    # no numeric revenue guide: the latest quarter's commodity revenue growth
        fwd = [latest["commodity_pct"]] * 2
        fwd_label, fwd_short = f"no {fy_now} revenue guide, {latest['quarter']} {revenue_line.lower()}", f"{latest['quarter']} revenue"
    if guides:
        # each field from the latest guide that states it; a quarter's EPS guide while that quarter is unreported
        later = lambda q: (int(q[3:]), int(q[1])) > (latest["fy"], nq)
        gq = next((g["q_eps_guide"] for g in reversed(guides) if "q_eps_guide" in g and later(g["q_eps_guide"]["quarter"])), None)
        bits = ([f"EPS ${money(ge['eps_guide'][0])}-{money(ge['eps_guide'][1])}" + (f" ({ge['eps_guide_note']})" if ge.get("eps_guide_note") else "")] if ge else []) + \
               ([f"{gr['rev_guide_label']} {pct_range(*gr['rev_guide'])}"] if gr else
                [f"revenue in words ('{g['rev_guide_text']}')" for g in [stated("rev_guide_text")] if g]) + \
               ([f"volume {pct_range(*gv['volume_guide'])}"] if gv else []) + \
               [f"fuel +{g['fuel_guide_pct'][0]}-{g['fuel_guide_pct'][1]}%" for g in [stated("fuel_guide_pct")] if g] + \
               [f"operating ratio: '{g['op_ratio_guide_text']}'" for g in [stated("op_ratio_guide_text")] if g] + \
               ([f"{gq['quarter'][:2]} EPS ${money(gq['range'][0])}-{money(gq['range'][1])} ({gq['note']})"] if gq else []) + \
               [f"full year in words: '{g['fy_words']}'" for g in [stated("fy_words")] if g]
        guide_text = f"{fy_now} guide ({', '.join(dict.fromkeys(g['doc'] for g in guides))}): " + "; ".join(bits)
    else:
        guide_text = f"{fy_now}: no numeric guide yet; the {latest['quarter']} release in words: '{latest['outlook_short']}'"
    # no numeric operating-ratio guide in any UNP guide so far: no margin step (words and one-sided bounds are not ranges)
    margin_guided, fy_margin_base = False, h["prev_fy_op_margin"]

    # ── dividend: the latest declared rate ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts["dividends"] if d["published"] <= as_of]
    # a vintage's rate is dated by the declaration it reports (dividend_published), so a later re-presentation of an
    # old 10-K (the 2010-10-25 recast) cannot override a newer declaration
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
    # fiscal year = calendar year; a day past the last year with EPS keeps that year's EPS
    fy = lambda d: min(int(d[:4]), cur_fy)
    window = [d for d in days if d > minus_years(as_of, 10) and (not h["pe_window_start"] or d >= h["pe_window_start"])]
    assert all(fy(d) in eps for d in window), (as_of, "P/E window needs EPS for every fiscal year")
    years = (dt.date.fromisoformat(as_of) - dt.date.fromisoformat(window[0])).days / 365.25
    window_label = "10-yr" if years > 9.9 else f"{years:.1f}-yr"
    pe = {d: px[d][2] / eps[fy(d)] for d in window}
    srt = sorted(pe.values())
    q = lambda p: round(srt[int(p * (len(srt) - 1))], 1)
    pctl = {"p5": q(.05), "p10": q(.10), "p25": q(.25), "median": q(.5), "p75": q(.75), "p90": q(.9), "max": round(srt[-1], 1)}
    pe_now_pctl = round(sum(v <= close / eps_now for v in srt) / len(srt) * 100)
    yearly = []
    for y in sorted({d[:4] for d in window}):
        dd = min((d for d in window if d.startswith(y)), key=lambda d: pe[d])
        yearly.append((y, round(pe[dd], 1), dd))
    ref = min(yr, key=lambda d: px[d][2])

    # ── era-dependent text: no disruption theme has dated evidence for a railroad in this fact sheet ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
    key_tail = ("A demand recession hits carloads first; the bear needs it\n"
                "  to reach pricing and the operating ratio as well.")
    theme_summary = "no disruption theme has dated evidence"
    cat3 = (f"(3) {fy_now} EPS guide ${money(ge['eps_guide'][0])}-{money(ge['eps_guide'][1])}"
            + (f" ({ge['eps_guide_note']})" if ge.get("eps_guide_note") else "") if ge else
            f"(3) A numeric {fy_now} guide — the {latest['quarter']} release gives words only ('{latest['outlook_short']}')")
    cat4 = (f"(4) Operating ratio — {latest['op_ratio']}% in {latest['quarter']} ({latest['op_ratio_pt']:+.1f} pt): "
            "where the fuel-surcharge lag and fixed costs would show first")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    same_day = [p for p in prints if p["published"] == as_of]     # only a release made before the open can meet AS_OF's close
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, released before the open)"

    renames = [n for n in facts.get("company_names", []) if h["published"] < n["published"] <= as_of]
    company = renames[-1]["name"] if renames else h["company"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])] + [g["source"] for g in guides]
           + ([dividend_src] if dividend_src else []) + split_ids + [e["id"] for e in events] + [n["source"] for n in renames])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "U0", "published": as_of, "title": "Yahoo Finance daily prices, UNP and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/UNP/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "revenue_b", "revenue_pct", "commodity_revenue_b", "commodity_pct", "carloads_k",
                   "carloads_pct", "arc", "arc_pct", "gtm_per_employee_pct", "op_ratio", "op_ratio_pt", "eps_q", "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    fcf = h.get("fcf_b")
    fcf_txt = f", {h.get('fcf_label', h['fy_label'])} free cash flow ${fcf:.2f}B" if fcf is not None else ""
    R = repr
    head = f'''#!/usr/bin/env python3
"""
UNP Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} (NYSE: UNP)  ·  {h["business_line"]}
Generated by retro/build_unp.py from retro/facts/UNP.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "UNP"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); railroad signals")
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
EPS_NORM      = {R(eps_hist)}   # reported, {h["normalization"]}{"; " + h["split_note"] if h.get("split_note") else ""}
REVENUE_HIST  = {R(rev)}   # operating revenue, USD bn
SHARES_HIST   = {R(shares)}   # diluted, millions
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # operating margin; operating ratio {h["prev_fy_op_ratio"]}%
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
NET_INTEREST_B = {h["net_interest_b"]}   # interest expense less other income, {h["net_interest_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}
REVENUE_LINE  = {R(revenue_line)}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_CARLOADS   = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # {"numeric revenue guide" if gr else "no numeric revenue guide: the latest quarter's commodity revenue growth"}
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fy_now)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no numeric operating-ratio guide, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {rev[max(rev)] * (1 + sum(fwd) / 2 / 100):.2f}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R([tuple(g) for g in latest["groups"]])}
GROUPS_BASIS    = {R(latest["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} operating ratio {h['prev_fy_op_ratio']}%, revenue {h['prev_fy_revenue_growth']:+d}% on carloads {h['prev_fy_carloads_pct']:+d}%; {latest['quarter'].split()[0]} revenue per car {latest['arc_pct']:+d}%")}
BALANCE_TEXT    = {R(f"Cash ${latest['cash_b']:.2f}B{fcf_txt}, {latest.get('cash_return_text', h['cash_return_text'])}")}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/UNP)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("UNP"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<32}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
