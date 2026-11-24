#!/usr/bin/env python3
"""
Build UNH retrospective models from the dated fact sheet (retro/facts/UNH.json).

UnitedHealth Group Incorporated, NYSE: UNH (CIK 731766), the first health benefits company in the retrospectives. The CB sibling
for a managed-care company: the same frozen rules (retro method r2), the same weekly dates and the same market statistics, with a
health benefits company's signal set and UnitedHealth Group's own rule-T thresholds (retro/templates/unh_engine.py.tmpl). For each
as-of date the builder
  1. selects only the history vintage, prints, guides and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF (Yahoo's UNH series; its last split is 2005-05-31, so every
     2008-2013 close is the price as traded, and the window's earlier days are on the post-2005 share basis),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

UnitedHealth Group's fiscal year is the calendar year. The method r2 inputs map as follows (retro/README.md, "UNH"; decided before any
UNH model was built or scored):
  - EPS: diluted EPS, each year from the latest filing that reports it, at the company's figure excluding only one-offs where a filing on
    the same basis prints it (the ACN rule: 1998, 1999, 2000, 2007 and 2008), GAAP otherwise; each per-share figure on the basis of its
    own filing, restated for the 2000, 2003 and 2005 two-for-one splits that follow it ('splits', the shared on_basis helper);
  - current-FY EPS: the midpoint of the fiscal-year EPS range, at the company's figure where a guide is given with and without announced
    items (the ACN rule), GAAP otherwise; a range whose midpoint is a loss has no P/E (the r2 loss rule, the LLY encoding);
  - forward revenue growth: no next-quarter revenue guide (the company guides next-quarter EPS only), so method r2's fallback takes the
    fiscal-year revenue guide, in dollars, read as growth on the last full year's revenue in the history (the PFE, LOW, BMY and LLY
    dollar-level rule); with none, the latest quarter's revenue growth (the UNP rule);
  - guided margin step: the fiscal-year operating margin guide where a filing states one in numbers, or derives it from a guided
    consolidated earnings from operations (a point or a range's midpoint) and revenue (the KMI derived-guide rule), against the last
    full year's operating margin on the EPS basis; otherwise none, and the margin signal takes the latest quarter's operating margin
    change;
  - dividend: the latest annual rate public on AS_OF: the vintage's (declared once a year to 2010, quarterly from June 2010), or a later
    rate from the first filing that states it ('dividends': the Q2 2010-2017 releases).
The kind is DURABLE: no 10-K calls the business cyclical. No disruption theme in taxonomy_eras.json is live for a health benefits
company in 2008-2017: OFFSHORE is scoped to IT services, CLOUD (live from 2012-10-30) to on-premise hardware, storage, databases and
data-center outsourcing, ECOMMERCE (2015-01-01) to physical retail, STREAMING (2015-08-04) to pay-TV and ENERGY_TRANSITION (2015-12-12)
to fossil reserves and refining; no FY2006-FY2014 10-K names cloud or offshore delivery, and the FY2015 and FY2016 10-Ks name cloud only
among OptumInsight's solutions for care providers ('cloud_words' on the vintage, quoted from that date); from the first date on which a
theme other than OFFSHORE is live, the 'why' quotes every live theme's registered scope (the CB 2014-2017 wording). The builder refuses
events until a theme encoding is decided; it also refuses a change of company name or listing and a distribution, none of which occurs.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. Every earnings 8-K of 2007-2013 was accepted before the open on its release day.

Output goes to staging/retrospective/UNH until the series is added to the archive (--out archive/retrospective/UNH).

Usage
  python3 retro/build_unh.py --weekly 2008-01-01 2008-12-31
  python3 retro/build_unh.py --weekly 2009-01-05 2009-12-31
  python3 retro/build_unh.py --weekly 2010-01-04 2013-12-31
  python3 retro/build_unh.py --weekly 2014-01-06 2017-12-31
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/UNH/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "UNH.json")
with open(os.path.join(HERE, "taxonomy_eras.json"), encoding="utf-8") as _fh:
    TAXO = json.load(_fh)
ENGINE = os.path.join(HERE, "templates", "unh_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "UNH")
SYMBOL = "UNH"
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"prem": (-6, 6, 18, 56), "mcr": (630, 290, -60, -230), "fee": (-8, 2, 12, 31), "ocr": (160, 60, -50, -300),
                     "opm": (-1400, -650, 90, 510)}
RULE_T_KEYS = {"prem": (1, False), "mcr": (10, True), "fee": (1, False), "ocr": (10, True), "opm": (10, False)}   # (rounding unit, lower is better)
GUIDE_KEYS = {"fy", "published", "source", "doc", "quotes", "note", "eps_guide", "eps_guide_note", "eps_gaap", "rev_guide_usd_b",
              "rev_label", "op_margin_guide", "op_margin_note", "efo_guide_b"}


def fiscal_year(day):
    """UnitedHealth Group's fiscal year is the calendar year."""
    return int(day[:4])


def eps_rng(lo, hi):
    """an EPS range: '3.95-4.00'; a point: '3.15'; a loss in parentheses"""
    m = lambda v: f"({money(-v)})" if v < 0 else money(v)
    return m(lo) if lo == hi else f"{m(lo)}-{m(hi)}"


def usd_rng(lo, hi):
    b = lambda v: f"{v:.1f}" if round(v, 1) == v else f"{v:.2f}"
    return f"about ${b(lo)}B" if lo == hi else f"${b(lo)}-{b(hi)}B"


def rule_t_value(k, r):
    """One annual rule-T value from its raw figures ((prior, current); $ millions)."""
    pct = lambda a, b: (b / a - 1) * 100
    if k == "prem":
        return round(pct(*r["prem_m"]) + 0.0, 2)
    if k == "fee":
        return round(pct(*r["fee_m"]) + 0.0, 2)
    if k == "mcr":
        (p0, p1), (m0, m1) = r["prem_m"], r["mc_m"]
        return round((m1 / p1 - m0 / p0) * 10000 + 0.0, 1)
    if k == "ocr":
        (a0, a1), (o0, o1) = r["rev_m"], r["oc_m"]
        return round((o1 / a1 - o0 / a0) * 10000 + 0.0, 1)
    (a0, a1), (e0, e1) = r["rev_m"], r["efo_m"]
    return round((e1 / a1 - e0 / a0) * 10000 + 0.0, 1)


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


def derived(r):
    """A print's growth rates, ratios and margins from its raw published figures ($ millions; ratios in %)."""
    pct = lambda a, b: (b / a - 1) * 100
    r1 = lambda x: round(x + 0.0, 1)
    r2 = lambda x: round(x + 0.0, 2)
    m, m0 = r["mc_m"] / r["prem_m"] * 100, r["mc_prior_m"] / r["prem_prior_m"] * 100
    o, o0 = r["oc_m"] / r["rev_m"] * 100, r["oc_prior_m"] / r["rev_prior_m"] * 100
    e, e0 = r["efo_m"] / r["rev_m"] * 100, r["efo_prior_m"] / r["rev_prior_m"] * 100
    return dict(sales_b=round(r["rev_m"] / 1000, 3), sales_pct=r1(pct(r["rev_prior_m"], r["rev_m"])),
                seq_pct=r1(pct(r["rev_prev_q_m"], r["rev_m"])), prem_pct=r1(pct(r["prem_prior_m"], r["prem_m"])),
                fee_pct=r1(pct(r["fee_prior_m"], r["fee_m"])), mcr=r2(m), mcr_bp=r1((m - m0) * 100), ocr=r2(o), ocr_bp=r1((o - o0) * 100),
                op_margin=r2(e), op_margin_bp=r1((e - e0) * 100), inv_pct=r1(pct(r["inv_prior_m"], r["inv_m"])))


def check_print(p, as_of):
    """Re-derive a print's (and each of its restatements public on AS_OF) growth rates and ratios from its raw figures; they must
    match."""
    for x in [p] + [r for r in p.get("restated", []) if r["published"] <= as_of]:
        for k, v in derived(x["raw"]).items():
            assert x[k] == v, (p["quarter"], x["source"], k, x[k], v)
        assert x["published"] >= p["published"], (p["quarter"], "a restatement precedes its print")


def view(p, as_of):
    """A print as public on AS_OF: the latest restatement public by then replaces its figures (the GOOG and JPM 10-Q rule)."""
    rs = [r for r in p.get("restated", []) if r["published"] <= as_of]
    if not rs:
        return p
    r = rs[-1]
    return {**p, **{k: v for k, v in r.items() if k not in ("published", "source", "note")},
            "restated_by": r["source"], "restated_note": r["note"], "restated_published": r["published"]}


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    chart = retro_tool.chart(SYMBOL)
    fx = retro_tool.split_factor(chart, as_of)
    assert fx == 1.0, "a split after AS_OF needs an encoding (none follows 2005)"
    px = raw
    yahoo_splits = {dt.datetime.fromtimestamp(v["date"] + chart["meta"]["gmtoffset"], dt.timezone.utc).date().isoformat()
                    for v in chart.get("events", {}).get("splits", {}).values()}
    assert all(s["effective"] in yahoo_splits for s in facts.get("splits", [])), "a split's effective date must match the price data"
    for kind in ("events", "company_names", "distributions"):
        if [x for x in facts.get(kind, []) if x.get("published", x.get("effective", "")) <= as_of]:
            sys.exit(f"{as_of}: the UNH builder has no encoding for {kind}; decide one first")
    for g in [g for g in facts["guides"] if g["published"] <= as_of]:   # a guide public on AS_OF: only fields with an encoding
        assert set(g) <= GUIDE_KEYS, (g["doc"], "a guide field the builder has no encoding for", set(g) - GUIDE_KEYS)
    for p in [p for p in facts["prints"] if p["published"] <= as_of]:  # a print public on AS_OF must match its raw figures
        check_print(p, as_of)
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    for v in facts["history_vintages"]:
        assert v["fiscal_year"] == "the calendar year"
    # on_basis (the shared split helper) divides every Q4 print's full-year EPS; an excluded year has none, so a NaN stands in for it
    # there and None comes back after (the LLY and BMY encoding; no UNH year is excluded in 2008-2009)
    held = {p["quarter"] for p in facts["prints"] if "fy_actual" in p and p["fy_actual"]["eps_normalized"] is None}
    facts = {**facts, "prints": [{**p, "fy_actual": {**p["fy_actual"], "eps_normalized": math.nan}} if p["quarter"] in held else p
                                 for p in facts["prints"]]}
    # the 'dividends' facts are annual rates (the shared helper restates quarterly ones): each follows the last split, so none
    # needs restating, and they pass around it unchanged
    annual_divs = facts.get("dividends", [])
    assert all("annual" in d and all(d["published"] >= s["effective"] for s in facts.get("splits", [])) for d in annual_divs), \
        "a dividend rate published before a split needs the basis helper"
    facts, split_ids = on_basis({**facts, "dividends": []}, as_of)          # every per-share fact on the AS_OF share basis
    facts["dividends"] = annual_divs
    for p in facts["prints"]:
        if p["quarter"] in held:
            p["fy_actual"]["eps_normalized"] = None
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["quarter"].startswith("Q4") else 0)
    public = [view(p, as_of) for p in facts["prints"] if p["published"] <= as_of]
    prints = [p for p in public if guide_fy(p) >= first_fy]
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is public yet")
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage
    h = {**h, "extended": ""}
    for p in prints:
        a = p.get("fy_actual")
        if a and a["fy"] not in reported(h):          # the 10-K vintage, once out, wins
            y = str(a["fy"])
            assert a["eps_normalized"] is not None and a["eps_normalized"] > 0, (p["quarter"], "an excluded year needs an encoding first")
            h.update(fy_label=a["fy_label"], eps_normalized={**h["eps_normalized"], y: a["eps_normalized"]},
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]},
                     diluted_shares_m={**h["diluted_shares_m"], y: a["diluted_shares_m"]},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_op_margin=a["op_margin"], prev_fy_op_margin_note=a["op_margin_note"],
                     prev_fy_pretax_margin=a["pretax_margin"], prev_fy_pretax_margin_note=a["pretax_margin_note"],
                     prev_fy_mcr=a["mcr"], prev_fy_ocr=a["ocr"], prev_fy_sales_growth=a["sales_growth"],
                     prev_fy_premium_growth=a["premium_growth"], tax_rate=a["tax_rate"], tax_note=f'{a["tax_note"]} ({p["source"]})',
                     extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    # between a Q4 print and its 10-K the history holds eleven years: the vintage's ten and the print's (the CB and JPM builders)
    latest = prints[-1]
    i = public.index(latest)
    assert i > 0, (as_of, "the fact sheet needs the print before the latest one")
    prev = (public[i - 1]["sales_pct"], public[i - 1]["quarter"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    last_rev = rev[max(rev)]
    fy_prev_s = f"FY{max(rev) % 100:02d}"

    # ── guides for the current fiscal year: each field from the latest guide public on AS_OF that states it ──
    guides = [g for g in facts["guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    stated = lambda *ks: next((g for g in reversed(guides) if any(g.get(k) is not None for k in ks)), None)
    ge, gr, gm = stated("eps_guide"), stated("rev_guide_usd_b"), stated("op_margin_guide", "efo_guide_b")
    gg = next((g for g in reversed(guides) if g.get("eps_gaap") is not None and g is ge), None)
    loss_guide = bool(ge) and sum(ge["eps_guide"]) / 2 <= 0
    if ge and not loss_guide:
        eps_now = round(sum(ge["eps_guide"]) / 2, 4)
        eps_label = f"{fy_e} EPS, guide midpoint (${eps_rng(*ge['eps_guide'])}, {ge['doc']}: {ge['eps_guide_note']})"
        eps_label_short = f"{fy_e} EPS, guide midpoint (${eps_rng(*ge['eps_guide'])}, {ge['doc']})"
    else:      # no numeric EPS guide yet, or a guided loss (no P/E): the last full year's EPS stands (the rollover rule)
        eps_now = eps_hist[last_fy]
        why = (f"the EPS guide (${eps_rng(*ge['eps_guide'])}, {ge['doc']}) is a loss, which has no P/E" if loss_guide
               else "no numeric EPS guide yet")
        eps_label = eps_label_short = f"{fy_e}: {why}, FY{last_fy % 100:02d}'s ${money(eps_now)} stands"
    if gr:                     # fiscal-year revenue guide in dollars, read as growth on the last full year
        fwd = [round((v / last_rev - 1) * 100, 1) for v in gr["rev_guide_usd_b"]]
        fwd_label, fwd_short, fwd_period = f"{fy_now} revenue guide", f"{fy_now} guide", fy_now
        fwd_kind = (f"fiscal-year {gr['rev_label']} guide {usd_rng(*gr['rev_guide_usd_b'])} ({gr['doc']}) on {fy_prev_s}'s "
                    f"${last_rev:.3f}B (no next-quarter revenue guide)")
        fy_rev_b, fy_rev_label = sum(gr["rev_guide_usd_b"]) / 2, f"{fy_now} revenue guide midpoint ({gr['doc']})"
    else:                      # no revenue guide in numbers: the latest quarter's revenue growth stands in (the UNP rule)
        fwd = [latest["sales_pct"]] * 2
        fwd_label, fwd_short, fwd_period = f"{latest['quarter']} revenue growth (no {fy_now} guide)", f"{latest['quarter'][:2]} revenue YoY", latest["quarter"]
        fwd_kind = f"no revenue guide in numbers: {latest['quarter']} revenue growth"
        fy_rev_b, fy_rev_label = last_rev * (1 + latest["sales_pct"] / 100), f"the {fwd_label}, applied to the year"
    if gm:                     # a guided operating margin: stated, or derived from guided earnings from operations and revenue
        if gm.get("op_margin_guide") is not None:
            m_lo, m_hi = gm["op_margin_guide"]
            m_txt = f"operating margin {m_lo:g}%" + ("" if m_lo == m_hi else f"-{m_hi:g}%") + f" ({gm['doc']})"
        else:
            rr, efo = gm.get("rev_guide_usd_b"), gm["efo_guide_b"]
            assert rr is not None, (gm["doc"], "a derived margin needs the same guide's revenue")
            efo_mid = sum(efo) / 2 if isinstance(efo, list) else efo          # a range: its midpoint (the Q1 2011 schedule)
            m_lo = m_hi = round(efo_mid / (sum(rr) / 2) * 100, 2)
            efo_txt = f"${efo[0]:g}-{efo[1]:g}B (midpoint ${efo_mid:g}B)" if isinstance(efo, list) else f"about ${efo:g}B"
            m_txt = (f"operating margin {m_lo:.2f}%, derived: earnings from operations of {efo_txt} on revenues of "
                     f"{usd_rng(*rr)} ({gm['doc']})")
        margin_guided, fy_margin_base = True, round((m_lo + m_hi) / 2, 3)
    else:
        margin_guided, fy_margin_base, m_txt = False, h["prev_fy_op_margin"], None
    if guides:
        bits = ([f"EPS ${eps_rng(*ge['eps_guide'])} ({ge['doc']}: {ge['eps_guide_note']})" + (" (a loss: no P/E, so not used)" if loss_guide else "")]
                if ge else ["no EPS range in numbers"]) + \
               ([f"{gr['rev_label']} {usd_rng(*gr['rev_guide_usd_b'])} ({pct_range(*fwd)} on {fy_prev_s}'s ${last_rev:.2f}B; {gr['doc']})"]
                if gr else ["no revenue guide in numbers"]) + \
               ([f"{m_txt}: a guided step from {fy_prev_s}'s {h['prev_fy_op_margin']:.2f}%"] if m_txt else ["no operating margin guide in numbers"]) + \
               ([g["note"] for g in guides[-1:] if g.get("note")])
        guide_text = f"{fy_now} guide ({', '.join(dict.fromkeys(g['doc'] for g in guides))}): " + "; ".join(bits)
    else:
        guide_text = f"{fy_now}: no guide yet; the latest quarter's revenue growth stands in (the UNP rule)"
    cat3 = (f"(3) The {fy_now} EPS guide — ${eps_rng(*ge['eps_guide'])} ({ge['doc']})" + (f"; GAAP ${eps_rng(*gg['eps_gaap'])}" if gg else "")
            if ge else f"(3) A numeric {fy_now} EPS guide — none yet")

    # ── dividend: the latest annual rate public on AS_OF: the vintage's (each 10-K), or a later rate from the first filing that
    # states it ('dividends': the Q2 2010-2013 releases) ──
    divs = [(d["published"], d["annual"] if "annual" in d else d["quarterly"] * 4, d["note"], d["source"])
            for d in facts.get("dividends", []) if d["published"] <= as_of]
    divs.append((h["published"], h["dividend_annual"], h["dividend_note"], None))
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

    # ── era-dependent text, from facts only: no disruption theme is live for a health benefits company on AS_OF ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
    key_tail = ("Medical cost trends that outrun premium rates show up in the medical care ratio first;\n"
                "  charges land in operating costs.")
    theme_summary = "no disruption theme has dated evidence"
    live = sorted(((t["live_from"], k, t["scope"]) for k, t in TAXO["themes"].items() if t["live_from"] <= as_of))
    if [k for _, k, _ in live] != ["OFFSHORE"]:      # from CLOUD's 2012-10-30: every live theme with its registered scope (CB 2014-2017)
        scopes = ", ".join(f"{k} {'is scoped to' if i == 0 else 'to'} '{sc}'" for i, (_, k, sc) in enumerate(live))
        # from the FY2015 10-K, the first to name cloud, in one of OptumInsight's offerings ('cloud_words'; README "UNH 2014-2017")
        tenk = ("no 10-K names cloud or offshore delivery" if not h.get("cloud_words") else
                f"no 10-K names offshore delivery; the {h['fy_label']} 10-K names cloud only among OptumInsight's own solutions for "
                f"care providers ('{h['cloud_words']}'), not as a substitute for UnitedHealth Group's business")
        why = (h["why"] + "; no disruption theme in taxonomy_eras.json is live for a health benefits company on this date (of the live "
               f"themes, {scopes}: none names health benefits, and {tenk}), so the watch list is empty "
               "and these words stay here (the PEP obesity rule)")
    else:
        why = (h["why"] + "; no disruption theme in taxonomy_eras.json is live for a health benefits company on this date (OFFSHORE is "
               "scoped to IT services), so the watch list is empty and these words stay here (the PEP obesity rule)")
    cat4 = (f"(4) Operating costs — operating cost ratio {latest['ocr']:.2f}% in {latest['quarter']} ({latest['ocr_bp']:+.1f}bp YoY): "
            "where legal, restructuring and other charges land")

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{latest['next_print'].split(' print')[0]} print)"
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        rt = same_day[-1].get("release_time", "")
        assert "before the open" in rt, (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    restate_ids = [p["restated_by"] for p in public if p.get("restated_by") and (p is latest or p is public[i - 1])]
    ids = (list(h["sources"]) + [p["source"] for p in prints] + [g["source"] for g in guides]
           + [public[i - 1]["source"]] + restate_ids + ([dividend_src] if dividend_src else []) + split_ids)
    sources = [dict(id=x, **facts["sources"][x]) for x in dict.fromkeys(ids)]
    sources.append({"id": "Y0", "published": as_of, "title": "Yahoo Finance daily prices, UNH and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/UNH/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E "
                                f"distribution from {window[0]}"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "seq_pct", "prem_pct", "fee_pct", "mcr", "mcr_bp", "ocr", "ocr_bp",
                   "op_margin", "op_margin_bp", "eps_q", "eps_q_prior")
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    restated_txt = (f"; {latest['quarter']} as restated by {latest['restated_by']} ({latest['restated_published']}): {latest['restated_note']}"
                    if latest.get("restated_by") else "")
    rev_text = (f"Revenue: {latest['sales_note']}; {latest['mix_note']}; {latest['eps_note']}; {latest['shares_note']}"
                + (f"; {latest['note']}" if latest.get("note") else "") + restated_txt)
    cash_return = f"dividend {dividend_note}; {latest['shares_note']}"
    split_note = h.get("split_note")
    R = repr
    head = f'''#!/usr/bin/env python3
"""
UNH Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{h["company"]} ({h["exchange"]}: UNH)  ·  {h["business_line"]}
Generated by retro/build_unh.py from retro/facts/UNH.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "UNH"
LISTED_SYMBOL = "UNH"
COMPANY     = {R(h["company"])}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); premium revenue, medical care ratio, "
               "fee revenue, operating cost ratio and operating margin signals with UnitedHealth Group's rule-T thresholds")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts above.
PIT_PROFILE = {{
    "kind": {R(h["kind"])},
    "risk": 2,
    "why": {R(why)},
    "theme_watch": {R(watch)},
    "evidence": [],
}}

# ── FACTS: market (prices truncated at AS_OF, as traded) ─────────────────────
EXCHANGE        = {R(h["exchange"])}   # display only
CURRENT_PRICE   = {close:.2f}   # USD, {h["exchange"]} close {as_of}, as traded (no split follows 2005)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2
PE_PCTL         = {R(pctl)}   # current-FY P/E over the window below
PE_NOW_PCTL     = {pe_now_pctl}    # share of those daily P/Es at or below the AS_OF one
WINDOW_LABEL    = {R(window_label)}   # P/E window: {window[0]} .. AS_OF ({len(window)} trading days; earlier days on the post-2005 share basis)
YEARLY_MIN_PE   = {R(yearly)}   # (calendar year, lowest P/E, date)
VOL_ANNUAL_PCT  = {vol:.3f}   # 1-yr realized, daily log returns
VOL_BETA        = {beta:.2f}    # 1-yr beta vs S&P 500
VOL_52W_LOW     = {low52:.2f}
VOL_52W_HIGH    = {high52:.2f}
REF_LOW         = {px[ref][2]:.2f}   # lowest close of the last 52 weeks, {ref}
REF_LOW_LABEL   = {R(MONTHS[int(ref[5:7]) - 1])}

# ── FACTS: company history ({", ".join(h["sources"])}, vintage {h["published"]}{h["extended"]}) ──
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}{f"; {split_note}" if split_note else ""}
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # revenues, USD bn
SHARES_HIST   = {R({y: round(v, 3) for y, v in shares.items()})}   # diluted, millions (on the AS_OF share basis)
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # operating margin, {h["prev_fy_op_margin_note"]}
CHECK_PRETAX_MARGIN = {h["prev_fy_pretax_margin"]}   # pre-tax margin for the EPS check (display), {h["prev_fy_pretax_margin_note"]}
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and the {fy_now} guide ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_SALES      = {R(prev)}
EPP_TODAY_EPS   = {round(eps_now, 6)}   # {eps_label}
EPS_LABEL       = {R(eps_label_short)}
FWD_GUIDE       = {R(tuple(fwd))}   # {fwd_kind}
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # {"True: a guided operating margin, stepped from the last full year's" if margin_guided else "False: no operating margin guide in numbers, so no guided step; the signal uses the latest quarter's change"}
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {fy_rev_b:.4f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenues {h['prev_fy_sales_growth']:+.1f}%, premiums {h['prev_fy_premium_growth']:+.1f}%, medical care ratio {h['prev_fy_mcr']:.2f}%; {latest['quarter'].split()[0]} medical care ratio {latest['mcr']:.2f}% ({latest['mcr_bp']:+.0f}bp YoY)")}
BALANCE_TEXT    = {R(f"{h['fy_label']} cash and investments ${h['cash_inv_b']:.2f}B, cash flows from operations ${h['cfo_b']:.2f}B, debt-to-total-capital {h['debt_to_cap']:.1f}%, dividend ${dividend:.2f} a year")}
REVENUE_TEXT    = {R(rev_text)}
CAPITAL_RETURN  = {R(cash_return)}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/UNH)")
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
        print(f"{d}  {tag:<40}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
