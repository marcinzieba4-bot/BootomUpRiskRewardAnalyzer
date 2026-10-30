#!/usr/bin/env python3
"""
Build AAPL retrospective models from the dated fact sheet (retro/facts/AAPL.json).

The AAPL sibling of build_low.py: the same frozen rules (retro method r2), the same weekly dates and the same market
statistics, with personal-computer and consumer-electronics signals (retro/templates/aapl_engine.py.tmpl). For each
as-of date the builder
  1. selects only the history vintage, prints, guides and events whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, as traded on each day (Yahoo's
     split-adjusted series with the later splits undone), so the price and the per-share facts share one basis,
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

Apple's fiscal year is the 52 or 53-week period that ends on the last Saturday of September. Apple guides one quarter at
a time: each release gives the next quarter's revenue, a dollar level, and diluted EPS. Guides are a dated list, as for
UNP and LOW, and each field comes from the latest guide for the current fiscal year that states it. The method r2 inputs
map as for LOW, with the fallbacks decided before any AAPL date was built or scored:
  - current-FY EPS: the fiscal-year EPS guide midpoint; Apple gave none, so the last full year's EPS stands (the
    rollover rule); a quarter's EPS guide is shown in the guide line and feeds no input (the UNP 2008 rule),
  - forward revenue growth: the next-quarter revenue guide for a quarter not yet reported, read as growth against the
    same quarter a year earlier (prior_sales_b, from that quarter's own release); none: the latest quarter's growth,
  - guided margin step: none, since no filing gives an operating-margin guide; the margin signal then uses the latest
    quarter's change (the ACN "no margin guide" rule). A gross-margin expectation (a 10-Q or 10-K) is shown in the guide
    line and feeds no input: the method's margin is the operating margin, and no figure is derived from another.
A stock split restates, from its effective date, every per-share fact published before it (divided by the ratio) and
every share count (multiplied by it); the prices of the whole window are on the AS_OF share basis.
A filing that re-presents a 10-K is a vintage of its own (the UNP rule): the FY2009 10-K/A of 2010-01-26 revises FY2007-FY2009
for the accounting principles adopted retrospectively in Q1 FY10. A dollar revenue guide is read against the year-ago quarter on
the guide's own accounting basis (prior_sales_b: the revised FY2009 quarters for the guides of fiscal 2010).
From the Q1 FY13 release a guide is a list: revenue and gross-margin ranges, operating expenses, other income/(expense) and a
tax rate, for the next quarter, and no EPS; the last three are shown in the guide line and feed no input (an operating margin
derived from them would be a figure derived from others; a quarter's tax rate is not the year's). Dividends are the latest
declared rate; catalyst (5) shows the latest statement of the capital return program (capital_return).
From Q1 FY19 Apple reports net sales by category only, with no unit sales: the Mac unit signal has no value and scores BASE (the
engine), and Mac and iPhone net sales growth (mac_sales_pct, iphone_sales_pct) are shown instead. A filing that revises a quarter's
guide with new numbers (the letter of 2019-01-02) is a guide of its own: each field it states replaces the earlier one. A filing that
says a field will not hold and gives no number (the update of 2020-02-17: "we do not expect to meet the revenue guidance") withdraws
it: the field is void in every earlier guide for that quarter, and the no-guide rule applies to it (the LOW withdrawal rule). From the
Q2 FY20 release Apple gives no outlook at all, so the no-guide rules hold to the end of 2023.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings
release, where it is the first trading day after it. Apple released after the close, so a print is dated the next
trading day (its 8-K's acceptance time) and the week's date is the trading day after that.

Output goes to staging/retrospective/AAPL until the series is added to the archive (--out archive/retrospective/AAPL).

Usage
  python3 retro/build_aapl.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_aapl.py 2008-01-24
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/AAPL/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "AAPL.json")
ENGINE = os.path.join(HERE, "templates", "aapl_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "AAPL")
# the guide fields this builder has an encoding for; any other field needs its encoding decided first
GUIDE_KEYS = {"fy", "published", "source", "doc", "quote", "q_guide", "q_guide_note", "gm_guide_pct"}
Q_GUIDE_KEYS = {"quarter", "sales_usd_b", "eps", "prior_sales_b", "prior_source", "prior_label", "gm_pct", "opex_usd_b", "oie_usd_b", "tax_pct",
                "withdrawn"}


def fiscal_year_end(n):
    """Apple's fiscal year n ends on the last Saturday of September of year n."""
    d = dt.date(n, 9, 30)
    return d - dt.timedelta(days=(d.weekday() - 5) % 7)


def fiscal_year(day):
    """The fiscal year a calendar day belongs to."""
    d = dt.date.fromisoformat(day)
    return d.year if d <= fiscal_year_end(d.year) else d.year + 1


def rng(lo, hi, unit=""):
    """'$1.42' or '$1.06-1.35'; 'about' is the company's word for a point guide"""
    return f"about ${money(lo)}{unit}" if lo == hi else f"${money(lo)}-{money(hi)}{unit}"


def usd_level(lo, hi):
    return f"about ${lo:.1f}B" if lo == hi else f"${lo:.1f}-{hi:.1f}B"


def gm_level(lo, hi):
    return f"about {lo:g}%" if lo == hi else f"{lo:g}-{hi:g}%"


def opex_level(lo, hi):
    return f"${lo:.2f}B" if lo == hi else f"${lo:.2f}-{hi:.2f}B"


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    # every price of the window on the AS_OF share basis: Yahoo's split-adjusted series times the splits after AS_OF,
    # so the AS_OF close is the price as traded and the per-share facts below share its basis
    chart = retro_tool.chart("AAPL")
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat()
                    for v in chart.get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo_splits for s in facts.get("splits", [])), "a split's effective date must match the price data"
    for v in facts["history_vintages"]:            # the fiscal calendar the filings state must match the rule above
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    for g in [g for g in facts["guides"] if g["published"] <= as_of]:      # a guide public on AS_OF may carry only encoded fields
        assert set(g) <= GUIDE_KEYS and set(g.get("q_guide", {})) <= Q_GUIDE_KEYS, (g["doc"], "a guide field with no encoding yet; decide one first")
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
    # no disruption theme in taxonomy_eras.json is live for a personal-computer and consumer-electronics maker in 2008
    # (CLOUD is live from 2012-10-30, OFFSHORE is scoped to IT services): any event needs its encoding decided first
    if events:
        sys.exit(f"{as_of}: the AAPL builder has no theme encoding yet; decide one before adding events")
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
                     prev_fy_gross_margin=a["gross_margin"], prev_fy_sales_growth=a["sales_growth"],
                     prev_fy_mac_units_k=a["mac_units_k"], prev_fy_mac_units_pct=a["mac_units_pct"],
                     other_income_b=a["other_income_b"], other_income_note=f'FY{y[2:]} from {p["source"]}',
                     tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     fcf_b=a.get("fcf_b", h.get("fcf_b")), fcf_label=a["fy_label"] if "fcf_b" in a else h.get("fcf_label"),
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    latest = prints[-1]
    prev = (prints[-2]["mac_units_pct"], prints[-2]["quarter"]) if len(prints) > 1 else (h["prev_q_mac_units_pct"], h["prev_q_label"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}   # reported history only: the rules use this
    cur_fy = max(eps_hist) + 1
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} FY{(latest['fy'] + (1 if nq == 4 else 0)) % 100:02d}"

    # ── guides for the current fiscal year, each field from the latest guide that states it ──
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    # a next-quarter guide counts while its quarter is unreported; each of its fields from the latest guide that states it
    qkey = lambda q: (int(q.split("FY")[1]), int(q[1]))
    later = lambda q: qkey(q) > (latest["fy"] % 100, nq)
    # a guide that withdraws fields of its quarter (the update of 2020-02-17: "we do not expect to meet the revenue guidance")
    # voids them in every earlier guide for that quarter, and the no-guide rule applies to them (the LOW withdrawal rule)
    void = lambda g, k: any(w.get("q_guide", {}).get("quarter") == g["q_guide"]["quarter"] and k in w["q_guide"].get("withdrawn", [])
                            for w in guides[guides.index(g) + 1:])
    q_field = lambda k: next((g for g in reversed(guides) if k in g.get("q_guide", {}) and later(g["q_guide"]["quarter"]) and not void(g, k)), None)
    gqw = next((g for g in reversed(guides) if "sales_usd_b" in g.get("q_guide", {}).get("withdrawn", []) and later(g["q_guide"]["quarter"])), None)
    gqs, gqe, gqm = q_field("sales_usd_b"), q_field("eps"), q_field("gm_pct")
    gqo, gqi, gqt = q_field("opex_usd_b"), q_field("oie_usd_b"), q_field("tax_pct")       # from Q1 FY13, display only
    ggm = next((g for g in reversed(guides) if "gm_guide_pct" in g), None)
    eps_now = eps_hist[cur_fy - 1]                 # no fiscal-year EPS guide: the last full year's EPS stands (rollover rule)
    eps_label = f"{fy_e}: no fiscal-year EPS guide, FY{(cur_fy - 1) % 100:02d}'s ${money(eps_now)} stands"
    if gqs:                                        # method r2: the next-quarter revenue guide, as growth on the year-ago quarter
        q = gqs["q_guide"]
        fwd = [round((v / q["prior_sales_b"] - 1) * 100, 1) for v in q["sales_usd_b"]]
        fwd_label, fwd_short, fwd_period = f"{q['quarter']} revenue guide", f"{q['quarter'][:2]} guide", q["quarter"]
    else:                                          # no next-quarter revenue guide: the latest quarter's net sales growth
        fwd = [latest["sales_pct"]] * 2
        fwd_label, fwd_short, fwd_period = f"no {next_q} revenue guide, {latest['quarter']} net sales", f"{latest['quarter']} sales", latest["quarter"]
    bits = []
    gqw = None if gqs else gqw                     # a revenue guide restated after a withdrawal would stand
    qs = {g["q_guide"]["quarter"] for g in (gqs, gqe, gqm, gqo, gqi, gqt, gqw) if g}
    assert len(qs) <= 1, (as_of, "next-quarter guide fields for different quarters", qs)
    qq = qs.pop() if qs else None
    if qq:
        qb = ([f"revenue {usd_level(*gqs['q_guide']['sales_usd_b'])} ({pct_range(*fwd)} on {gqs['q_guide']['prior_label']}'s "
               f"${gqs['q_guide']['prior_sales_b']:.2f}B)"] if gqs else
              [f"no revenue guide: the {gqw['doc']} withdrew it ('{gqw['quote']}')"] if gqw else []) + \
             ([f"EPS {rng(*gqe['q_guide']['eps'])}"] if gqe else []) + \
             ([f"gross margin {gm_level(*gqm['q_guide']['gm_pct'])} ({gqm['doc']})"] if gqm else []) + \
             ([f"operating expenses {opex_level(*gqo['q_guide']['opex_usd_b'])}"] if gqo else []) + \
             ([f"other income/(expense) ${gqi['q_guide']['oie_usd_b'][0] * 1000:,.0f}M"] if gqi else []) + \
             ([f"tax rate {gqt['q_guide']['tax_pct'][0]:g}%"] if gqt else [])
        bits.append(f"{qq}: " + ", ".join(qb) + (f" ({gqs['q_guide_note']})" if gqs and gqs.get("q_guide_note") else ""))
    if ggm:
        bits.append(f"{fy_now} gross margin {gm_level(*ggm['gm_guide_pct'])} ({ggm['doc']})")
    if guides and bits:
        guide_text = (f"{fy_now} guide ({', '.join(dict.fromkeys(g['doc'] for g in guides))}): " + "; ".join(bits)
                      + f"; no {fy_now} revenue, EPS or operating-margin guide")
    elif latest.get("outlook_short"):
        guide_text = f"{fy_now}: no guide in scope yet; the {latest['quarter']} release in words: '{latest['outlook_short']}'"
    else:                                          # from the Q2 FY20 release Apple gives no outlook, in numbers or in words
        guide_text = f"{fy_now}: no guide in scope; the {latest['quarter']} release gives none"
    # no operating-margin guide in any filing of the period: no guided step, and the margin signal uses the latest quarter
    margin_guided = False
    fy_margin_base = h["prev_fy_op_margin"]

    # ── dividend: the latest declared rate (none before the first declaration, the Q3 FY12 release) ──
    # a rate declared before a split was announced is divided from the split's effective date (on_basis): the note says so
    # then, never earlier (the $0.82 of 2020-04-30 predates the 4-for-1 split announced on 2020-07-30)
    split_txt = lambda pub: "".join(f", divided by {s['ratio']} for the {s['ratio']}-for-1 split effective {s['effective']}"
                                    for s in facts["splits"] if pub < s["published"] and s["effective"] <= as_of)
    divs = [(d["published"], d["quarterly"] * 4, d["note"] + split_txt(d["published"]), d["source"]) for d in facts["dividends"] if d["published"] <= as_of]
    divs.append((h.get("dividend_published", h["published"]), h["dividend_annual"], h["dividend_note"] + split_txt(h.get("dividend_published", h["published"])), None))
    _, dividend, dividend_note, dividend_src = max(divs, key=lambda x: x[0])
    # ── capital return: the latest statement of the program (display only, catalyst (5)) ──
    crs = [c for c in facts.get("capital_return", []) if c["published"] <= as_of]
    capital_return = crs[-1]["text"] if crs else "none so far (no dividend, no buyback)"

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
    # fiscal year of a day (ends on the last Saturday of September); a day past the last guided year keeps that year's EPS
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
    key_tail = ("A consumer-spending recession hits Mac and iPod demand first; the bear\n"
                "  needs it to reach gross margin and the iPhone ramp as well.")
    theme_summary = "no disruption theme has dated evidence"
    cat3 = (f"(3) {qq} guide — " + ", ".join(
                ([f"revenue {usd_level(*gqs['q_guide']['sales_usd_b'])}"] if gqs else []) + ([f"EPS {rng(*gqe['q_guide']['eps'])}"] if gqe else []))
            + f"; Apple guides one quarter at a time, no {fy_now} guide" if (gqs or gqe) else
            f"(3) {qq} guide — revenue withdrawn by the {gqw['doc']} ('{gqw['quote']}'); no {fy_now} guide" if gqw else
            f"(3) A {next_q} guide — the {latest['quarter']} release gives none ('{latest['outlook_short']}')" if latest.get("outlook_short") else
            f"(3) A {next_q} guide — the {latest['quarter']} release gives none")
    # iPad units from the Q3 FY10 print; no iPod units from the Q1 FY15 print; no unit sales at all from the Q1 FY19 print
    cat4 = (f"(4) iPhone and iPad — no unit sales reported in {latest['quarter']}: iPhone net sales {latest['iphone_sales_pct']:+.1f}%, "
            f"net sales other than Macs {latest['non_mac_pct']:+.1f}%" if latest["iphone_units_k"] is None else
            f"(4) iPod and iPhone — iPods {latest['ipod_units_pct']:+.1f}%, {latest['iphone_units_k']:,}K iPhones in {latest['quarter']}: "
            f"net sales other than Macs {latest['non_mac_pct']:+.1f}%" if latest.get("ipad_units_k") is None else
            f"(4) iPod, iPhone and iPad — iPods {latest['ipod_units_pct']:+.1f}%, {latest['iphone_units_k']:,}K iPhones and "
            f"{latest['ipad_units_k']:,}K iPads in {latest['quarter']}: net sales other than Macs {latest['non_mac_pct']:+.1f}%"
            if latest["ipod_units_k"] is not None else
            f"(4) iPhone and iPad — {latest['iphone_units_k']:,}K iPhones and {latest['ipad_units_k']:,}K iPads in {latest['quarter']} "
            f"(no iPod units reported): net sales other than Macs {latest['non_mac_pct']:+.1f}%")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    # only a print public before the open can meet AS_OF's close: Apple released after the previous day's close, so a print dated
    # AS_OF occurs only in a week with no trading day after it (the Thursday before Good Friday 2011)
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    renames = [n for n in facts.get("company_names", []) if h["published"] < n["published"] <= as_of]
    company = renames[-1]["name"] if renames else h["company"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])]
           + [x for g in guides for x in [g["source"], g.get("q_guide", {}).get("prior_source")] if x]
           + ([dividend_src] if dividend_src else []) + ([crs[-1]["source"]] if crs else [])
           + split_ids + [e["id"] for e in events] + [n["source"] for n in renames])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "A0", "published": as_of, "title": "Yahoo Finance daily prices, AAPL and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/AAPL/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "gross_margin", "gross_margin_bp", "op_margin", "op_margin_bp",
                   "mac_units_k", "mac_units_pct", "non_mac_pct", "ipod_units_k", "ipod_units_pct", "iphone_units_k",
                   "eps_q", "eps_q_prior", "deferred_iphone_b")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    fcf = h.get("fcf_b")
    fcf_txt = f", {h.get('fcf_label', h['fy_label'])} free cash flow ${fcf:.2f}B" if fcf is not None else ""
    # a Q4 release gives no full-year Mac units (its data sheet is the quarter's): the 10-K supplies them later
    macs_txt = (f"Mac units {h['prev_fy_mac_units_k']:,}K ({h['prev_fy_mac_units_pct']:+.1f}%)" if h["prev_fy_mac_units_k"] is not None
                else h.get("mac_units_note", "no full-year Mac units in the Q4 release"))
    ng = f"; {latest['quarter']} {latest['non_gaap_note']}" if latest.get("non_gaap_note") else ""
    # from Q1 FY10 there is no subscription deferral to show (the new accounting principles, adopted retrospectively)
    deferred_txt = (f"iPhone and Apple TV deferred revenue ${latest['deferred_iphone_b']:.2f}B at {latest['quarter']} (subscription accounting){ng}"
                    if latest["deferred_iphone_b"] is not None else f"No iPhone or Apple TV subscription deferral at {latest['quarter']}: {latest['deferred_note']}{ng}")
    # from FY2009 Apple also holds long-term marketable securities
    lt_txt = f" plus ${latest['lt_securities_b']:.2f}B of long-term marketable securities" if latest.get("lt_securities_b") is not None else ""
    R = repr
    head = f'''#!/usr/bin/env python3
"""
AAPL Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} (NASDAQ: AAPL)  ·  {h["business_line"]}
Generated by retro/build_aapl.py from retro/facts/AAPL.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "AAPL"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); personal-computer and consumer-electronics signals")
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
CURRENT_PRICE   = {close:.2f}   # USD, NASDAQ close {as_of}
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
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # operating margin, {h["prev_fy_op_margin_note"]}
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
OTHER_INCOME_B = {h["other_income_b"]}   # other income and expense (mostly interest income), {h["other_income_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} guide ──
LATEST          = {R({**{k: latest.get(k) for k in latest_keys}, **{k: latest[k] for k in ('mac_sales_pct', 'iphone_sales_pct') if k in latest}})}
PREV_MAC_UNITS  = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # {"next-quarter revenue guide, growth on the year-ago quarter" if gqs else "no next-quarter revenue guide: the latest quarter's net sales growth"}
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no operating-margin guide, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {rev[max(rev)] * (1 + sum(fwd) / 2 / 100):.2f}
FY_REVENUE_LABEL = {R(f"{fwd_label}, applied to the year (no {fy_now} revenue guide)")}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} net sales {h['prev_fy_sales_growth']:+.1f}%, {macs_txt}; {latest['quarter'].split()[0]} gross margin {latest['gross_margin']:.2f}% ({latest['gross_margin_bp']:+d}bp)")}
BALANCE_TEXT    = {R(f"Cash and short-term investments ${latest['cash_b']:.2f}B{lt_txt}{fcf_txt}, {latest.get('cash_return_text', h['cash_return_text'])}")}
DEFERRED_TEXT   = {R(deferred_txt)}
THEME_FACTORS   = {R(factors)}
THEME_SIGNAL_NAME    = {R(sig_name)}
THEME_SIGNAL_TRIGGER = {R(trigger)}
THEME_SUMMARY        = {R(theme_summary)}
KEY_TRIGGER_TAIL     = {R(key_tail)}
CATALYST_3      = {R(cat3)}
CATALYST_4      = {R(cat4)}
CAPITAL_RETURN  = {R(capital_return)}
'''
    os.makedirs(os.path.join(out, as_of), exist_ok=True)
    with open(os.path.join(out, as_of, "model.py"), "w", encoding="utf-8") as fh:
        fh.write(head + engine)
    return tag, latest["quarter"], stage


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dates", nargs="*")
    ap.add_argument("--weekly", nargs=2, metavar=("START", "END"))
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/AAPL)")
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    raw, spx = load_series("AAPL"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(raw), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, raw, spx, engine, os.path.abspath(a.out))
        print(f"{d}  {tag:<32}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
