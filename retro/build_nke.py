#!/usr/bin/env python3
"""
Build NKE retrospective models from the dated fact sheet (retro/facts/NKE.json).

The NKE sibling of build_aapl.py: the same frozen rules (retro method r2), the same weekly dates and the same market
statistics, with athletic footwear and apparel signals (retro/templates/nke_engine.py.tmpl). For each as-of date the
builder
  1. selects only the history vintage, prints, guides and events whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, as traded on each day (Yahoo's
     split-adjusted series with the later splits undone), so the price and the per-share facts share one basis,
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

NIKE's fiscal year ends on May 31. NIKE gave no revenue, EPS or pre-tax margin guide in numbers in any filing of 2007-2011:
the outlook on its calls (transcripts furnished by 8-K) is in words, and words are not figures (the UNP 2016 rule); its
gross-margin statements in basis points are display only (the AAPL rule). The method r2 inputs map with the fallbacks
decided before any NKE date was built or scored:
  - current-FY EPS: no EPS guide in numbers, so the last full year's EPS stands (the rollover rule),
  - forward revenue growth: no revenue guide in numbers, so the latest quarter's revenue growth excluding currency changes
    (lc_pct: the release's growth less the currency effect it states, or from Q3 FY09 the growth excluding currency changes
    it states; the method's local-currency basis),
  - guided margin step: none; the margin signal uses the latest quarter's change in pre-tax margin (NIKE evaluates its
    segments on pre-tax income).
The latest call's outlook words for the current fiscal year are shown in the guide line and feed no input.
A stock split restates, from its effective date, every per-share fact published before it (divided by the ratio) and
every share count (multiplied by it); the prices of the whole window are on the AS_OF share basis.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings
release, where it is the first trading day after it. NIKE released after the close, so a print is dated the next
trading day (its 8-K's acceptance time) and the week's date is the trading day after that.

Output goes to staging/retrospective/NKE until the series is added to the archive (--out archive/retrospective/NKE).

Usage
  python3 retro/build_nke.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_nke.py --weekly 2009-01-05 2011-12-31
  python3 retro/build_nke.py 2008-06-27
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/NKE/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "NKE.json")
ENGINE = os.path.join(HERE, "templates", "nke_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "NKE")
# the guide fields this builder has an encoding for; any other field (a number) needs its encoding decided first
GUIDE_KEYS = {"fy", "published", "source", "doc", "words"}
# rule T, the engine's signal thresholds: (rule_t key, BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"futures": (-31, -13, 5, 12), "gross_margin": (-780, -360, 60, 250), "revenue": (-23, -8, 7, 15),
                     "inventory_gap": (46, 21, -4, -8), "pretax_margin": (-1520, -730, 70, 170)}


def fiscal_year_end(n):
    """NIKE's fiscal year n ends on May 31 of year n."""
    return dt.date(n, 5, 31)


def fiscal_year(day):
    """The fiscal year a calendar day belongs to."""
    d = dt.date.fromisoformat(day)
    return d.year if d <= fiscal_year_end(d.year) else d.year + 1


def rule_t(rt):
    """Rule T thresholds from the ten annual values: XBULL best, BULL median, BASE worst, BEAR one median-to-worst step
    beyond the worst; rounded half up to whole percent or 10 bp."""
    out = {}
    for k, (key, unit, lower) in {"futures": ("futures", 1, False), "gross_margin": ("gross_margin", 10, False),
                                  "revenue": ("revenue", 1, False), "inventory_gap": ("inventory_gap", 1, True),
                                  "pretax_margin": ("pretax_margin", 10, False)}.items():
        v = sorted(rt[key]["values"].values())
        assert len(v) == 10, (k, "rule T needs ten annual values")
        med = (v[4] + v[5]) / 2
        worst, best = (v[-1], v[0]) if lower else (v[0], v[-1])
        bear = worst + (worst - med)
        r = lambda x: math.floor(x / unit + 0.5) * unit
        out[k] = (r(bear), r(worst), r(med), r(best))
    return out


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    # every price of the window on the AS_OF share basis: Yahoo's split-adjusted series times the splits after AS_OF,
    # so the AS_OF close is the price as traded and the per-share facts below share its basis
    chart = retro_tool.chart("NKE")
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat()
                    for v in chart.get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo_splits for s in facts.get("splits", [])), "a split's effective date must match the price data"
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    for g in [g for g in facts["guides"] if g["published"] <= as_of]:      # a guide public on AS_OF may carry only encoded fields
        assert set(g) <= GUIDE_KEYS, (g["doc"], "a guide field with no encoding yet; decide one first")
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
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
    # no disruption theme in taxonomy_eras.json is live for an athletic footwear and apparel brand in 2008-2011 (ECOMMERCE is
    # live from 2015 and scoped to physical retail, OFFSHORE to IT services): any event needs its encoding decided first
    if events:
        sys.exit(f"{as_of}: the NKE builder has no theme encoding yet; decide one before adding events")
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
                     prev_fy_futures_pct=a["futures_pct"], prev_fy_futures_note=f'{p["quarter"]} release',
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    latest = prints[-1]
    prev = (prints[-2]["futures_pct"], prints[-2]["quarter"]) if len(prints) > 1 else (h["prev_q_futures_pct"], h["prev_q_label"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}   # reported history only: the rules use this
    cur_fy = max(eps_hist) + 1
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} FY{(latest['fy'] + (1 if nq == 4 else 0)) % 100:02d}"

    # ── guides for the current fiscal year: words only, the latest call's replace the earlier ones; no input ──
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    eps_now = eps_hist[cur_fy - 1]                 # no EPS guide in numbers: the last full year's EPS stands (rollover rule)
    eps_label = f"{fy_e}: no EPS guide in numbers, FY{(cur_fy - 1) % 100:02d}'s ${money(eps_now)} stands"
    # no revenue guide in numbers: the latest quarter's revenue growth excluding currency changes (method r2's LC basis)
    fwd = [latest["lc_pct"]] * 2
    fwd_label, fwd_short, fwd_period = f"{latest['quarter']} revenue ex-currency", f"{latest['quarter'].split()[0]} rev ex-FX", latest["quarter"]
    if guides:
        g = guides[-1]
        guide_text = (f"{fy_now} outlook in words ({g['doc']}, display only): " + " ... ".join(f"'{w}'" for w in g["words"])
                      + f"; no {fy_now} revenue, EPS or margin guide in numbers")
    else:
        guide_text = f"{fy_now}: no outlook in scope yet; no {fy_now} revenue, EPS or margin guide in numbers"
    # no margin guide in any filing of the period: no guided step, and the margin signal uses the latest quarter
    margin_guided = False
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
    # fiscal year of a day (ends on May 31); a day past the last guided year keeps that year's EPS
    fy = lambda d: min(fiscal_year(d), cur_fy)
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
    key_tail = ("A consumer-spending recession shows up in futures orders first; the bear\n"
                "  needs it to reach gross margin and inventories as well.")
    theme_summary = "no disruption theme has dated evidence"
    cat3 = (f"(3) The outlook in words — {guides[-1]['doc']}: '{guides[-1]['words'][0]}'; no {fy_now} guide in numbers" if guides else
            f"(3) A {fy_now} outlook — none in scope yet, and no {fy_now} guide in numbers")
    cat4 = (f"(4) Inventories — {latest['inventory_pct']:+.1f}% against revenue {latest['sales_pct']:+.1f}% in {latest['quarter']} "
            f"({latest['inventory_gap_pp']:+.1f}pp): discounting follows if orders slow")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    # only a print public before the open can meet AS_OF's close: NIKE released after the previous day's close, so a print dated
    # AS_OF occurs only in a week with no trading day after it (the Thursday before Good Friday 2008)
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    renames = [n for n in facts.get("company_names", []) if h["published"] < n["published"] <= as_of]
    company = renames[-1]["name"] if renames else h["company"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])]
           + [g["source"] for g in guides] + ([dividend_src] if dividend_src else [])
           + split_ids + [e["id"] for e in events] + [n["source"] for n in renames])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "A0", "published": as_of, "title": "Yahoo Finance daily prices, NKE and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/NKE/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "lc_pct", "futures_pct", "futures_fx_pp", "futures_b",
                   "gross_margin", "gross_margin_bp", "pretax_margin", "pretax_margin_bp", "inventory_b", "inventory_pct",
                   "inventory_gap_pp", "eps_q", "eps_q_prior")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    eps_note = f"; {latest['eps_note']}" if latest.get("eps_note") else ""
    R = repr
    head = f'''#!/usr/bin/env python3
"""
NKE Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} (NYSE: NKE)  ·  {h["business_line"]}
Generated by retro/build_nke.py from retro/facts/NKE.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "NKE"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); athletic footwear and apparel signals")
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
EPS_NORM      = {R(eps_hist)}   # {h["normalization"]}{"; " + h["split_note"] if h.get("split_note") else ""}
REVENUE_HIST  = {R(rev)}   # revenues, USD bn
SHARES_HIST   = {R(shares)}   # diluted, millions
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_pretax_margin"]}   # pre-tax margin, {h["prev_fy_pretax_margin_note"]}
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} outlook ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_FUTURES    = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # no revenue guide in numbers: the latest quarter's revenue growth excluding currency changes
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
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenues {h['prev_fy_sales_growth']:+.1f}%, year-end futures orders {h['prev_fy_futures_pct']:+.0f}% ({h['prev_fy_futures_note']}); {latest['quarter'].split()[0]} gross margin {latest['gross_margin']:.2f}% ({latest['gross_margin_bp']:+.0f}bp)")}
BALANCE_TEXT    = {R(f"Cash and short-term investments ${latest['cash_b']:.2f}B, {h['fcf_label']} free cash flow ${h['fcf_b']:.2f}B, dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
FUTURES_TEXT    = {R(f"Futures: {latest['futures_note']}, {latest['futures_pct']:+.1f}% reported ({latest['futures_fx_pp']:+.0f}pp from currency{'; ' + latest['futures_fx_note'] if latest.get('futures_fx_note') else ''}); revenue {latest['sales_pct']:+.1f}% reported, {latest['lc_pct']:+.0f}% excluding currency ({latest['lc_note']}){eps_note}")}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/NKE)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("NKE"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<32}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
