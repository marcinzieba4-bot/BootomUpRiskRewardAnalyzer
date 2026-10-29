#!/usr/bin/env python3
"""
Build LOW retrospective models from the dated fact sheet (retro/facts/LOW.json).

The LOW sibling of build_acn.py and build_unp.py: the same frozen rules (retro method r2), the same weekly dates and the
same market statistics, with home-improvement retail signals (retro/templates/low_engine.py.tmpl). For each as-of date
the builder
  1. selects only the history vintage, prints, guides, dividend and events whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, as traded on each day (Yahoo's
     split-adjusted series with the later splits undone), so the price and the per-share facts share one basis,
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Lowe's fiscal year N ends on the Friday nearest January 31 of N+1 (fiscal 2007 ended 2008-02-01). Each earnings release
carries a "Business Outlook" for the next quarter and the fiscal year (total sales growth, comparable store sales, the
operating-margin change in basis points, EPS); an 8-K may restate it between releases. Guides are therefore their own
dated list, as for UNP, and each field comes from the latest guide for the current fiscal year that states it. The
method r2 inputs map as for ACN:
  - current-FY EPS: the fiscal-year EPS guide midpoint (no numeric EPS guide: the last full year's EPS stands),
  - forward revenue growth: the next-quarter total sales guide for a quarter not yet reported (none: the fiscal-year
    sales guide; none either: the latest quarter's sales growth),
  - guided margin step: the fiscal-year operating-margin guide in basis points, stepped from the previous year's margin
    on the definition the guide states.
A guide that withdraws the year's outlook (the Q1 FY20 release) voids the earlier guides for that year; the no-guide rules
apply until the company guides again.
A stock split restates, from its effective date, every per-share fact published before it (divided by the ratio) and
every share count (multiplied by it); the prices of the whole window are on the AS_OF share basis.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings
release, where it is the first trading day after it.

Output goes to staging/retrospective/LOW until the series is added to the archive (--out archive/retrospective/LOW).

Usage
  python3 retro/build_low.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_low.py 2008-02-26
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/LOW/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "LOW.json")
ENGINE = os.path.join(HERE, "templates", "low_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "LOW")


def fiscal_year_end(n):
    """Lowe's fiscal year n ends on the Friday nearest January 31 of n + 1."""
    jan31 = dt.date(n + 1, 1, 31)
    d = (4 - jan31.weekday()) % 7
    return jan31 + dt.timedelta(days=d if d <= 3 else d - 7)


def fiscal_year(day):
    """The fiscal year a calendar day belongs to."""
    d = dt.date.fromisoformat(day)
    return d.year if d > fiscal_year_end(d.year - 1) else d.year - 1


def eps_rng(lo, hi):
    """an EPS guide: '1.75-1.85', or one figure for a point ('approximately $1.64')"""
    return money(lo) if lo == hi else f"{money(lo)}-{money(hi)}"


def pct_level(lo, hi):
    return f"{lo:g}%" if lo == hi else f"{lo:g}-{hi:g}%"


def bp_range(lo, hi):
    return f"{lo:+g}bp" if lo == hi else f"{lo:+g} to {hi:+g}bp"


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    # every price of the window on the AS_OF share basis: Yahoo's split-adjusted series times the splits after AS_OF,
    # so the AS_OF close is the price as traded and the per-share facts below share its basis
    chart = retro_tool.chart("LOW")
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat()
                    for v in chart.get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo_splits for s in facts.get("splits", [])), "a split's effective date must match the price data"
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    facts, split_ids = on_basis(facts, as_of)
    for g in facts["guides"]:                      # a next-quarter EPS guide is per share too (on_basis covers the rest)
        r = math.prod(s["ratio"] for s in facts["splits"] if g["published"] < s["effective"] <= as_of)
        if r != 1 and "eps" in g.get("q_guide", {}):
            g["q_guide"]["eps"] = [e / r for e in g["q_guide"]["eps"]]
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
    # the one theme encoding decided so far: a 10-K whose risk factors name online competition (ECOMMERCE, from the FY2015
    # 10-K) puts the theme on the watch list; any other kind of event needs its encoding decided first
    if any(e["kind"] != "ecommerce_company_acknowledged" for e in events):
        sys.exit(f"{as_of}: the LOW builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
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
                     prev_fy_margins=a["margins"], prev_fy_margins_note=a["margins_note"],
                     prev_fy_gross_margin=a["gross_margin"], prev_fy_sales_growth=a["sales_growth"],
                     prev_fy_comps=a["comps_pct"], prev_fy_stores=a["stores"],
                     net_interest_b=a["net_interest_b"], net_interest_note=f'FY{y[2:]} from {p["source"]}',
                     store_opening_b=a["store_opening_b"],
                     tax_rate=a["tax_rate"], tax_note=f'{a.get("tax_note", f"FY{y[2:]} effective rate")} ({p["source"]})',
                     fcf_b=a.get("fcf_b", h.get("fcf_b")), fcf_label=a["fy_label"] if "fcf_b" in a else h.get("fcf_label"),
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    latest = prints[-1]
    prev = (prints[-2]["comps_pct"], prints[-2]["quarter"]) if len(prints) > 1 else (h["prev_q_comps"], h["prev_q_label"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}   # reported history only: the rules use this
    cur_fy = max(eps_hist) + 1
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} FY{(latest['fy'] + (1 if nq == 4 else 0)) % 100:02d}"

    # ── guides for the current fiscal year, each field from the latest guide that states it ──
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    # a withdrawal (the Q1 FY20 release) voids every earlier guide for the year: the no-guide rules below apply until the
    # company guides again
    wd = next((g for g in reversed(guides) if g.get("withdrawn")), None)
    if wd:
        guides = guides[guides.index(wd) + 1:]
    stated = lambda k: next((g for g in reversed(guides) if k in g), None)
    ge, gr, gc = stated("eps_guide"), stated("rev_guide"), stated("comps_guide")
    # a numeric margin guide is one field in either form: a change in basis points (op_margin_guide_bp) or a level in
    # percent of sales (op_margin_guide_pct, a range; a point is lo = hi)
    gm = next((g for g in reversed(guides) if "op_margin_guide_bp" in g or "op_margin_guide_pct" in g), None)
    # a next-quarter guide counts while its quarter is unreported
    qkey = lambda q: (int(q.split("FY")[1]), int(q[1]))
    later = lambda q: qkey(q) > (latest["fy"] % 100, nq)
    gq = next((g for g in reversed(guides) if "q_guide" in g and later(g["q_guide"]["quarter"])), None)
    q = gq["q_guide"] if gq else None
    if ge:
        eps_now = round(sum(ge["eps_guide"]) / 2, 3)
        eps_label = f"{fy_e} EPS, guide midpoint"
    else:                                    # no numeric EPS guide: the last full year's EPS stands (rollover rule)
        eps_now = eps_hist[cur_fy - 1]
        eps_label = (f"{fy_e}: the {wd['doc']} withdrew the {fy_now} guide, FY{(cur_fy - 1) % 100:02d}'s ${money(eps_now)} stands" if wd else
                     f"{fy_e}: no numeric EPS guide yet, FY{(cur_fy - 1) % 100:02d}'s ${money(eps_now)} stands")
    if q and "sales" in q:                   # method r2: the next-quarter revenue guide
        fwd, fwd_label, fwd_short, fwd_period = q["sales"], f"{q['quarter']} sales guide", f"{q['quarter'][:2]} guide", q["quarter"]
    elif gr:                                 # no next-quarter guide: the fiscal-year sales guide
        fwd, fwd_label, fwd_short, fwd_period = gr["rev_guide"], f"{fy_now} sales guide", f"{fy_now} guide", fy_now
    else:                                    # no numeric sales guide: the latest quarter's sales growth
        fwd = [latest["sales_pct"]] * 2
        fwd_label, fwd_short, fwd_period = f"no {fy_now} sales guide, {latest['quarter']} sales", f"{latest['quarter']} sales", latest["quarter"]
    fy_rev = gr["rev_guide"] if gr else fwd
    # the fiscal-year margin guide (bp) is the guided margin step, stepped from the previous year's margin on the definition
    # the guide states (the ACN rule for a restated base): "operating margin" = gross margin less SG&A and depreciation
    # (guides to the Q3 FY07 release), "EBIT margin" = earnings before interest and taxes (from the Q4 FY07 release);
    # words give no step
    margin_guided = bool(gm)
    mdef = gm["margin_def"] if gm else h["margin_def"]
    # a guide whose step is measured from a base other than the history's margin says so (fy_margin_guide_base, the ACN
    # FY19 rule): LOW's Q3 FY16 guide includes the Q4 FY15 impairment, so it steps from FY15's GAAP margin, not the
    # adjusted one the history and the earlier FY16 guides use
    restated = gm.get("fy_margin_guide_base") if gm else None
    prev_margin = restated if restated is not None else h["prev_fy_margins"][mdef]
    prev_margin_comment = (f'{h["fy_label"]}: {h["prev_fy_margins_note"]}' if restated is None else
                           f'{h["fy_label"]} as the {fy_now} guide measures it ({gm["fy_margin_guide_note"]}); '
                           f'{h["prev_fy_margins"][mdef]} in the history: {h["prev_fy_margins_note"]}')
    fy_margin_base = (round(sum(gm["op_margin_guide_pct"]) / 2, 3) if gm and "op_margin_guide_pct" in gm else
                      round(prev_margin + sum(gm["op_margin_guide_bp"]) / 2 / 100, 3) if gm else prev_margin)
    latest = {**latest, "op_margin": latest["margins"][mdef][0], "op_margin_bp": latest["margins"][mdef][1]}
    # the operating-margin definition leaves out store opening costs (guided, else last year's); EBIT margin includes them
    gso = stated("store_opening_m")
    store_opening_b = 0.0 if mdef == "EBIT margin" else gso["store_opening_m"] / 1000 if gso else h["store_opening_b"]
    so_label = ("inside EBIT margin" if mdef == "EBIT margin" else
                f"store opening costs, {fy_now} guide" if gso else f"store opening costs, {h['fy_label']}")
    if guides:
        bits = ([f"EPS ${eps_rng(*ge['eps_guide'])}" + (f" ({ge['eps_guide_note']})" if ge.get("eps_guide_note") else "")] if ge else []) + \
               ([f"sales {pct_range(*gr['rev_guide'])}" + (f" ({gr['rev_guide_note']})" if gr.get("rev_guide_note") else "")] if gr else []) + \
               ([f"comps {pct_range(*gc['comps_guide'])}"] if gc else []) + \
               ([f"{gm['margin_def']} {bp_range(*gm['op_margin_guide_bp'])}" if "op_margin_guide_bp" in gm else
                 f"{gm['margin_def']} {pct_level(*gm['op_margin_guide_pct'])} of sales"] if gm else []) + \
               [f"{g['stores_guide']} stores" for g in [stated("stores_guide")] if g] + \
               ([f"{q['quarter']}: " + ", ".join(
                   ([f"sales {pct_range(*q['sales'])}"] if "sales" in q else []) + ([f"comps {pct_range(*q['comps'])}"] if "comps" in q else []) +
                   ([f"EPS ${eps_rng(*q['eps'])}"] if "eps" in q else []))] if q else []) + \
               [f"in words: '{g['fy_words']}'" for g in [stated("fy_words")] if g]
        guide_text = f"{fy_now} guide ({', '.join(dict.fromkeys(g['doc'] for g in guides))}): " + "; ".join(bits)
    if not guides or not bits:
        guide_text = f"{fy_now}: no numeric guide yet; the {latest['quarter']} release in words: '{latest['outlook_short']}'"
    if wd and not ge:                        # withdrawn, with no full-year EPS guide since
        guide_text = (f"{guide_text}; no full-year guide since the {wd['doc']}" if guides and bits else
                      f"{fy_now}: no numeric full-year guide; the {wd['doc']} withdrew it") + f": '{wd['withdrawn_quote']}'"

    # tax rate (display only, the EPS check): the latest tax-rate guide for the year (the ACN rule), else the last year's rate
    gt = stated("tax_rate_guide")
    tax_rate, tax_note = ((round(gt["tax_rate_guide"] / 100, 4), f"{fy_now} effective tax rate guide ({gt['doc']})") if gt else
                          (h["tax_rate"], h["tax_note"]))

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
    # fiscal year of a day (ends on the Friday nearest January 31); a day past the last guided year keeps that year's EPS
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

    # ── era-dependent text, from facts only: which disruption theme has dated evidence on AS_OF ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
    key_tail = ("A housing-led demand recession hits comps first; the bear needs it\n"
                "  to reach gross margin and expense leverage as well.")
    theme_summary = "no disruption theme has dated evidence"
    for e in [e for e in events if e["kind"] == "ecommerce_company_acknowledged"][-1:]:
        # ECOMMERCE is live from 2015-01-01; the first 10-K after that whose risk factors name online competition (FY2015)
        # puts it on the watch list (the ACN CLOUD rule: company-acknowledged, no market read). The factor pair nets to
        # zero and the theme signal stays at 2/4, so only text changes; re-filing needs dated evidence of market pricing.
        val_word = "a premium" if pe_now_pctl >= 70 else "a discount to its own history" if pe_now_pctl <= 30 else "near its own median"
        stage = "ecommerce"
        watch = [{"theme": "ECOMMERCE", "status": "live, company-acknowledged; no market read",
                  "reason": (f"Live: Lowe's own {e['doc']} says '{e['risk_quote']}' At the same time {e['offering']}. "
                             f"The stock trades at {close / eps_now:.1f}x {fy_e_s} — {val_word}. Re-file as DISRUPTION_EXPOSED "
                             "(ECOMMERCE) only if dated evidence shows the market pricing online substitution of Lowe's store "
                             "sales specifically.")}]
        factors = [(f"Omni-channel: {e['offering_short']} — Lowe's sells online itself", 0.2, 0.10),
                   (f"Online competition ({e['doc']}): {e['risk_short']}", -0.2, 0.10)]
        sig_name = "E-commerce: net effect on store sales"
        trigger = "Online and multi-channel rivals take share faster than Lowe's own online sales grow"
        theme_summary = "e-commerce competition is live and company-acknowledged; no dated evidence ties the multiple to it"
    cat3 = (f"(3) {fy_now} EPS guide ${eps_rng(*ge['eps_guide'])}"
            + (f" ({ge['eps_guide_note']})" if ge.get("eps_guide_note") else "") if ge else
            f"(3) A numeric {fy_now} guide again — the {wd['doc']} withdrew it" if wd else
            f"(3) A numeric {fy_now} guide — the {latest['quarter']} release gives words only ('{latest['outlook_short']}')")
    cat4 = (f"(4) Operating margin — {latest['op_margin']:.2f}% in {latest['quarter']} ({latest['op_margin_bp']:+d}bp): "
            "where fixed-cost deleverage on falling comps shows first")

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
    sources.append({"id": "L0", "published": as_of, "title": "Yahoo Finance daily prices, LOW and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/LOW/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "comps_pct", "gross_margin", "gross_margin_bp", "op_margin",
                   "op_margin_bp", "inventory_pct", "inventory_gap_pp", "eps_q", "eps_q_prior", "stores", "sq_ft_pct")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    fcf = h.get("fcf_b")
    fcf_txt = f", {h.get('fcf_label', h['fy_label'])} free cash flow ${fcf:.2f}B" if fcf is not None else ""
    # a Q4 release without a full-year comparable sales figure (Q4 FY18, Q4 FY19): the 10-K supplies it later
    comps_txt = f"on comps {h['prev_fy_comps']:+.1f}%" if h["prev_fy_comps"] is not None else "(no full-year comp in the Q4 release)"
    R = repr
    head = f'''#!/usr/bin/env python3
"""
LOW Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} (NYSE: LOW)  ·  {h["business_line"]}
Generated by retro/build_low.py from retro/facts/LOW.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "LOW"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); home-improvement retail signals")
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
REVENUE_HIST  = {R(rev)}   # net sales, USD bn
SHARES_HIST   = {R(shares)}   # diluted, millions
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {prev_margin}   # {mdef}, {prev_margin_comment}
TAX_RATE      = {tax_rate}   # {tax_note}
NET_INTEREST_B = {h["net_interest_b"]}   # interest, net, {h["net_interest_note"]}
STORE_OPENING_B = {store_opening_b:.3f}   # {so_label}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}
MARGIN_DEF    = {R(mdef)}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_COMPS      = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # {"next-quarter total sales guide" if fwd_period == next_q else "fiscal-year total sales guide (no next-quarter guide)" if gr and fwd == gr["rev_guide"] else "no numeric sales guide: the latest quarter's sales growth"}
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # {"True: numeric operating-margin guide, so BASE adds the guided margin step and the signal uses it" if margin_guided else "False: no numeric margin guide, so no guided step; the signal uses the latest quarter's change"}
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {rev[max(rev)] * (1 + sum(fy_rev) / 2 / 100):.2f}
FY_REVENUE_LABEL = {R(f"{fy_now} sales guide" if gr else fwd_label)}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} sales {h['prev_fy_sales_growth']:+.1f}% {comps_txt}, {h['prev_fy_stores']:,} stores; {latest['quarter'].split()[0]} gross margin {latest['gross_margin']:.2f}% ({latest['gross_margin_bp']:+d}bp)")}
BALANCE_TEXT    = {R(f"Cash and short-term investments ${latest['cash_b']:.2f}B{fcf_txt}, {latest.get('cash_return_text', h['cash_return_text'])}")}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/LOW)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("LOW"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<32}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
