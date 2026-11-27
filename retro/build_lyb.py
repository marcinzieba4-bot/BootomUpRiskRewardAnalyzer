#!/usr/bin/env python3
"""
Build LYB retrospective models from the dated fact sheet (retro/facts/LYB.json).

The LYB sibling of build_kmi.py's new-listing builder: the same frozen rules (retro method r2), the same weekly dates and the same
market statistics, with chemical and refining signals (retro/templates/lyb_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF, from the listing (the listing rule of method r2),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

LyondellBasell Industries N.V.'s shares were issued on 2010-04-30, when the company emerged from bankruptcy as the new parent of
LyondellBasell AF's businesses, were quoted on the Pink Sheets to 2010-10-13 and listed on the NYSE as LYB from 2010-10-14 (FY2010 10-K,
Item 5); its own P/E exists only from the first of those days (retro/README.md, "LYB"). No LYB share existed in 2008-2009, so no date of
those years can be built. 2010 is two periods (the Predecessor to April 30 and the Successor from May 1, after fresh-start accounting),
with EPS only for the Successor's eight months, so it is not a year of EPS (the KMI 2011 and CTVA 2017 rule) and is excluded: its days
leave the P/E window. The first full year of EPS is 2011, so no date can be built before the Q4 2011 release (8-K accepted 2012-02-10
10:09 ET, during the session, on a Friday: the first weekly date is that day). EPS is GAAP diluted EPS from continuing operations where
the filing reports it, each year from the latest filing that reports it; a release that republishes a year on a new basis (the Q2 2012
release: the Berre refinery in discontinued operations) restates it until the next 10-K ('restates' on the print). The combined
Successor and Predecessor 2010, which each 10-K's MD&A prints and calls the year, is a year of revenues (never of EPS).

LyondellBasell guides no revenue, EPS or margin in numbers in any filing of the period, so:
  - current-FY EPS: the last full year's GAAP EPS stands (the PFE rule for a year with no reported-EPS guide),
  - BASE growth and the growth factor: the latest quarter's revenue growth as reported (the SO, UNP and KMI no-guide rule),
  - guided margin step: none; the margin signal uses the latest quarter's change.

Signals (each against the year-ago quarter as the release shows it): O&P-Americas and Intermediates & Derivatives operating income
growth (the two segments with the largest operating income in the FY2010 10-K, the last 10-K before the first date; segment operating
income is the measure the releases tabulate by segment), revenue growth, the operating margin change and the pre-tax margin change, from
the release's Tables 1, 8 and 11. Growth against a year-ago loss is measured over the loss's absolute value (the CAT and SO rule).

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. A release on the week's last trading day (a Friday) meets that day's close if its 8-K was accepted
before the open or during the session (the UNP Good Friday rule, "released during the session").

Output goes to staging/retrospective/LYB until the series is added to the archive (--out archive/retrospective/LYB).

Usage
  python3 retro/build_lyb.py --weekly 2012-02-06 2013-12-31      # 99 dates, 2012-02-10 .. 2013-12-31
  python3 retro/build_lyb.py 2012-02-10
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/LYB/<AS_OF>
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

FACTS = os.path.join(HERE, "facts", "LYB.json")
ENGINE = os.path.join(HERE, "templates", "lyb_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "LYB")
SYMBOL = "LYB"
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"opa": (-299, 36, 371, 707), "ind": (-41, 29, 98, 168), "revenue": (-108, -39, 30, 196),
                     "op_margin": (-480, 70, 610, 1270), "pretax_margin": (-3290, -1530, 230, 3550)}
RULE_T_KEYS = {"opa": (1, False), "ind": (1, False), "revenue": (1, False), "op_margin": (10, False), "pretax_margin": (10, False)}
PRINT_KEYS = {"quarter", "fy", "q", "published", "source", "release", "release_time", "period_end", "raw", "sales_b", "sales_pct",
              "opm", "opm_bp", "ptm", "ptm_bp", "eps_q", "eps_q_prior", "diluted_shares_m", "opa_pct", "ind_pct", "seg_note",
              "sales_note", "margin_note", "eps_note", "cash_note", "next_print", "fy_actual", "restates"}
FY_KEYS = {"fy", "fy_label", "eps_normalized", "excluded_note", "revenue_usd_b", "diluted_shares_m", "normalization_note", "op_margin",
           "op_margin_note", "sales_growth", "check_pretax_margin", "check_pretax_note", "tax_rate", "tax_note", "one_off_test"}
RESTATE_KEYS = {"eps_normalized", "revenue_usd_b", "note"}


def fiscal_year_end(n):
    """LyondellBasell's fiscal year n is the calendar year n."""
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
    # growth on the year-ago figure; against a year-ago loss, over the loss's absolute value (the CAT 2014-2017 and SO 2018-2021 rule)
    pct = lambda a, b: round((b / a - 1) * 100, 1) if a > 0 else round((b - a) / abs(a) * 100, 1) if a < 0 else None
    mg = lambda x, rev: round(x / rev * 100 + 0.0, 2)
    want = {"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": pct(r["rev_prior_m"], r["rev_m"]),
            "opm": mg(r["oi_m"], r["rev_m"]), "opm_bp": round((mg(r["oi_m"], r["rev_m"]) - mg(r["oi_prior_m"], r["rev_prior_m"])) * 100, 1),
            "ptm": mg(r["pti_m"], r["rev_m"]), "ptm_bp": round((mg(r["pti_m"], r["rev_m"]) - mg(r["pti_prior_m"], r["rev_prior_m"])) * 100, 1),
            "eps_q": r["eps_q"], "eps_q_prior": r["eps_q_prior"], "diluted_shares_m": r["dil_sh_m"],
            "opa_pct": pct(r["opa_prior_m"], r["opa_m"]), "ind_pct": pct(r["ind_prior_m"], r["ind_m"])}
    for k, v in want.items():
        assert p[k] == v or (v is not None and abs(p[k] - v) < 1e-9), (p["quarter"], k, p[k], v)
    for y, rs in p.get("restates", {}).items():
        assert set(rs) == RESTATE_KEYS and int(y) < p["fy"], (p["quarter"], y, "a restatement field with no encoding yet")
    a = p.get("fy_actual")
    if a:
        assert set(a) <= FY_KEYS, (p["quarter"], sorted(set(a) - FY_KEYS), "a full-year field with no encoding yet; decide one first")
        t = a["one_off_test"]
        kept = a["eps_normalized"] is not None
        # a year is kept at GAAP unless it is a loss or its listed one-off charges (after tax) exceed its income attributable to the Company
        assert t["distorted"] == (t["items_after_tax_m"] > t["income_attributable_m"]), (p["quarter"], "the one-off test")
        assert kept == (not t["distorted"] and a["eps_normalized"] > 0), (p["quarter"], "the year's EPS and the one-off test disagree")


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    listing = facts["listing"]
    first_day = listing["first_trading_day"]
    if as_of < first_day:
        sys.exit(f"{as_of}: LyondellBasell Industries N.V.'s shares were first issued and traded on {first_day}; no LYB share and no P/E "
                 "of its own exists before it (the listing rule; retro/README.md, \"LYB\")")
    chart = retro_tool.chart(SYMBOL)
    assert not chart.get("events", {}).get("splits") and not facts["distributions"], "a split or distribution needs its encoding first"
    # Yahoo's series starts on 2010-04-28, two days before the capital was issued (FY2010 10-K, Item 5): those points are left out
    assert min(raw) < first_day and min(raw) >= "2010-04-28", ("the price data's first day moved", min(raw))
    px = {d: v for d, v in raw.items() if d >= first_day}   # no split or distribution: Yahoo's close is the price as traded
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no annual history of LyondellBasell Industries N.V. is public yet")
    for v in vintages:                                 # the fiscal calendar the filings state must match the rule
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
    assert not [g for g in facts["guides"] if g["published"] <= as_of], "a guide needs its encoding first (no LYB filing of 2010-2013 gives one)"
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
        sys.exit(f"{as_of}: the LYB builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
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
    # a release that republishes an earlier year on a new basis restates it from its own date until a 10-K published after it (the
    # LMT, PFE and CB print-level rule): the Q2 2012 release's FY2011 from continuing operations (the Berre refinery discontinued)
    restated = []
    for p in public:
        for y, rs in p.get("restates", {}).items():
            if p["published"] > vintages[-1]["published"] and y in h["eps_normalized"]:
                h.update(eps_normalized={**h["eps_normalized"], y: rs["eps_normalized"]},
                         revenue_usd_b={**h["revenue_usd_b"], y: rs["revenue_usd_b"]},
                         normalization=f'{h["normalization"]}; {rs["note"]} ({p["source"]}, {p["published"]})')
                restated.append(p["source"])
    for k in ("prev_fy_op_margin", "check_pretax_margin", "tax_rate"):
        assert h[k] is not None, (as_of, k, "the vintage's last year needs its Q4 print's full-year figures")
    latest = prints[-1]
    i = public.index(latest)
    prev_seg = (public[i - 1]["opa_pct"], public[i - 1]["quarter"]) if i > 0 else (None, "no earlier print")
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    excluded = {int(k): v for k, v in h.get("eps_excluded", {}).items()}
    if not eps_hist:                                   # 2010 is two periods: no full year, no P/E
        sys.exit(f"{as_of}: no full year of LyondellBasell's EPS is public yet, so the stock has no P/E of its own (method r2)")
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)        # the last full year in the history: cur_fy - 1 unless that year is excluded
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── current-FY EPS: no guide in numbers, so the last full year's EPS stands (the PFE rule) ──
    excluded_tail = "".join(f" (FY{y % 100:02d} is excluded: {excluded[y]})" for y in range(last_fy + 1, cur_fy))
    eps_now = eps_hist[last_fy]
    eps_label = (f"{fy_e}: no reported (GAAP) EPS guide, FY{last_fy % 100:02d}'s ${money(eps_now)} stands" + excluded_tail)
    fwd = [latest["sales_pct"]] * 2
    fwd_label, fwd_short, fwd_period = (f"no {fy_now} revenue guide in numbers, {latest['quarter']} revenues as reported",
                                        f"{latest['quarter'][:2]} revenues", latest["quarter"])
    guide_text = (f"{fy_now}: no revenue, EPS or margin guide in numbers (BASE takes {latest['quarter']} revenue growth as reported); "
                  "the releases' outlook is in words")
    margin_guided = False                          # no margin guide: no guided step
    fy_margin_base = h["prev_fy_op_margin"]

    # ── dividend: the latest declared interim rate (special dividends are not a rate) ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts["dividends"] if d["published"] <= as_of]
    divs.append((h["published"], h["dividend_annual"], h["dividend_note"], None))
    _, dividend, dividend_note, dividend_src = max(divs, key=lambda x: x[0])
    bbs = [b for b in facts["buyback_programs"] if b["published"] <= as_of]      # the latest program announced by AS_OF (display only)
    bb = bbs[-1] if bbs else None
    cash_return = h["cash_return_text"] + (f"; {bb['text']} ({bb['source']})" if bb else "")

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
    # an excluded year's own days leave the window (2010, two periods)
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

    # ── era-dependent text, from facts only: no disruption theme in the registry is live for a chemicals and refining company ──
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none in scope", "No live disruption theme covers chemicals and refining"
    theme_summary = "no theme in the registry is live for a chemicals and refining company on this date; none has dated evidence"
    key_tail = ("By the company's own account its businesses are highly cyclical;\n"
                "  the bear needs margins to fall across the segments, not one quarter's.")
    why = h["why"]
    # from CLOUD's live date (2012-10-30) every live theme is quoted with its registered scope (the CB 2014-2017, UNH and SCHW wording)
    live = sorted(((t["live_from"], k, t["scope"]) for k, t in retro_tool.load_taxonomy()["themes"].items() if t["live_from"] <= as_of))
    live_k = [k for _, k, _ in live]
    if live_k != ["OFFSHORE"]:
        assert live_k == ["OFFSHORE", "CLOUD"], (as_of, "a live theme the LYB 10-Ks were not searched for", live_k)
        scopes = ", ".join(f"{k} {'is scoped to' if i == 0 else 'to'} '{sc}'" for i, (_, k, sc) in enumerate(live))
        head = why.split("; no theme in taxonomy_eras.json is live")[0]
        assert head != why, (as_of, "the vintage's why lost its theme clause")
        why = (head + "; no disruption theme in taxonomy_eras.json is live for a chemicals and refining company on this date (of the live "
               f"themes, {scopes}: none names chemicals or refining, and no 10-K names cloud or offshore delivery), so the watch list is "
               "empty and these words stay here (the PEP obesity rule)")
    kind, pit_risk = h["kind"], 2
    cat3 = f"(3) The {fy_now} outlook — no revenue, EPS or margin guide in numbers (the releases' outlook is in words)"
    cat4 = f"(4) Free cash flow — {h['fcf_label']} {h['fcf_note']}"

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    # a print dated AS_OF occurs only in a week with no trading day after it; it meets AS_OF's close only if it was public before that
    # close: an 8-K accepted before the open or during market hours (the UNP Good Friday 2014 and SCHW rule)
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        rt = same_day[-1].get("release_time", "")
        early = "(before the open)" in rt
        assert early or "(during market hours)" in rt, (as_of, same_day[-1]["quarter"], "not public before the close")
        tag = (f"(day of the {same_day[-1]['quarter']} print, public before the open)" if early else
               f"(day of the {same_day[-1]['quarter']} print, released during the session)")

    company, exchange, listed = h["company"], h["exchange"], h["symbol"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]]] + [public[i - 1]["source"]] + [listing["source"]]
           + ([dividend_src] if dividend_src else []) + restated + ([bb["source"]] if bb else []))
    sources = [dict(id=i, **{k: v for k, v in facts["sources"][i].items()}) for i in dict.fromkeys(ids)]
    sources.append({"id": "A0", "published": as_of,
                    "title": f"Yahoo Finance daily prices, {company} ordinary shares ({exchange}: {listed}) and S&P 500, truncated at AS_OF",
                    "url": f"https://finance.yahoo.com/quote/{SYMBOL}/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E distribution "
                                f"since the shares were issued on {first_day}"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "opm", "opm_bp", "ptm", "ptm_bp", "eps_q", "eps_q_prior",
                   "opa_pct", "ind_pct")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    activity = (f"Activity: {latest['sales_note']}; segments: {latest['seg_note']}; {latest['margin_note']}; {latest['cash_note']}; "
                f"EPS {latest['eps_note']}")
    fy_rev = rev[max(rev)] * (1 + sum(fwd) / 2 / 100)
    fy_rev_label = f"{fwd_label}, applied to the year (no {fy_now} revenue guide)"
    franchise_q = f"{latest['quarter'].split()[0]} operating margin {latest['opm']:.2f}% ({latest['opm_bp']:+.0f}bp)"
    fcf_text = f"${h['fcf_b']:.2f}B" if h["fcf_b"] >= 0 else f"$({-h['fcf_b']:.2f})B"
    LATEST = {k: latest.get(k) for k in latest_keys}
    R = repr
    head = f'''#!/usr/bin/env python3
"""
{listed} Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: {listed})  ·  {h["business_line"]}
Generated by retro/build_lyb.py from retro/facts/LYB.json: the constants below are the facts public on
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
               "derived from dated facts by frozen rules (retro/README.md); chemical and refining signals")
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
REVENUE_HIST  = {R(rev)}   # sales and other operating revenues, USD bn; {h["revenue_note"]}
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
BALANCE_TEXT    = {R(f"{h['fcf_label']} free cash flow {fcf_text}, dividend ${dividend:.2f} a year, {cash_return}")}
ACTIVITY_TEXT   = {R(activity)}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/LYB)")
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
