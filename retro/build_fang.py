#!/usr/bin/env python3
"""
FANG (Diamondback Energy, Inc.) retrospective builder: the buildability gate, then the models of the dates that pass it.

    python3 retro/build_fang.py --weekly 2008-01-01 2009-12-31        # every date refused, with its reason (retro/README.md, "FANG 2008-2009")
    python3 retro/build_fang.py --weekly 2010-01-01 2013-12-31        # every date refused, with its reason
    python3 retro/build_fang.py --weekly 2014-01-01 2017-12-31        # 7 refused (2014-01-03 .. 2014-02-14), 202 built (2014-02-21 .. 2017-12-29)
    python3 retro/build_fang.py --weekly 2018-01-01 2021-12-31        # 209 built (2018-01-05 .. 2021-12-31; retro/README.md, "FANG 2018-2021")
    python3 retro/build_fang.py --gate-md                             # rewrite staging/retrospective/FANG/GATE.md (every range)
    python3 retro/build_fang.py --check START END --json              # the dates that pass the gate as JSON (firewall.py's FANG gate test)
    python3 retro/build_fang.py --pro-forma --weekly START END        # sensitivity only: pro forma per-share figures counted as EPS (writes nothing)
    python3 retro/build_fang.py 2014-02-21                            # one date
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/FANG/<AS_OF>

The gate. Method r2 needs, on each as-of date, (1) a close of the stock as traded, and (2) the stock's own P/E: at least one full fiscal
year of positive EPS of the company whose shares are priced, as its own filings public on that date publish it (the listing rule of
AVGO, V, KMI, CTVA and LYB; the loss and gap rules of F, MU and CRM; a predecessor's history is never substituted: KMI, CTVA, LYB):
  (1) price: Yahoo's FANG series is Diamondback Energy, Inc.'s common stock from 2012-10-12, its first trading day (NASDAQ: FANG);
      no share of the issuer or of its predecessors (Windsor Permian LLC and Windsor UT LLC, limited liability companies) traded before;
  (2) anchor: the latest offering document or 10-K vintage public on the date; a period counts as a year only if it is twelve months
      (the CTVA 2017 rule), and only a positive per-share figure the filing publishes as the company's own EPS can anchor a P/E. The
      only per-share figures in any filing to 2013-12-31 are pro forma (2011 $(0.04), the six months of 2012 $1.07, 2012 $0.60), never
      used (the CTVA and CHTR rule). The FY2013 10-K (accepted 2014-02-19 17:29 ET, dated 2014-02-20) is the first with a GAAP year:
      FY2013 $1.29 diluted, so the first weekly date that passes is 2014-02-21 (the earnings-week rule: the day after the Q4 2013
      release, dated 2014-02-20 as it was accepted after the close).

The model (method r2, the LYB new-listing builder's code path; retro/README.md, "FANG 2014-2017"). For each date that passes the gate:
  1. the latest 10-K vintage public on AS_OF (FY2013-FY2020), the prints public on AS_OF that guide a year after it, and the Q4
     release's year from its release until the 10-K;
  2. every market statistic from Yahoo's daily prices truncated at AS_OF, from the listing (no split or distribution: the close is the
     price as traded); the P/E window runs from 2012-10-12, up to ten years, and an excluded year's own days leave it (2012: no GAAP EPS;
     2015 and 2016: GAAP losses after the full cost ceiling impairments);
  3. <OUT>/<AS_OF>/model.py = those facts + the frozen engine (retro/templates/fang_engine.py.tmpl).
EPS is GAAP diluted EPS on net income attributable to Diamondback (FY13 $1.29, FY14 $3.64); FY2015 $(8.74) and FY2016 $(2.20) are losses
with no figure excluding only one-offs (the company's adjusted net income also removes the non-cash derivative marks, which recur), so each
is excluded as the latest year and then a gap (the MU and NEM loss rule), and FY14's $3.64 is the anchor from the Q4 2014 print on.
From 2018 ("FANG 2018-2021"): FY17 $4.94 and FY18 $8.06 are kept; FY2019 ($1.47) is distorted (its listed impairment and debt charges
exceed its income before income taxes, the AAPL FY2002 test) and FY2020 ($(28.59)) a loss, each excluded as the latest year and then a
gap, so FY18's $8.06 is the anchor from the Q4 2018 print on; the dividend is the latest annual rate a release states.
Diamondback guides production, unit costs and capital spending, never revenue, EPS or a margin, in numbers, so the last full year's
EPS stands, BASE is the latest quarter's revenue growth as reported plus the net buyback (a share issuance: negative), and there is no
margin step. Weekly dates: one per ISO week, the week's last trading day, except in a week with an earnings release, where it is the
first trading day after its 'published' date (a release accepted after the close is dated the next trading day).
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
from build_acn import MONTHS, load_series, minus_years, weekly_dates as earnings_weeks  # noqa: E402
from build_unp import money  # noqa: E402

FACTS = os.path.join(HERE, "facts", "FANG.json")
ENGINE = os.path.join(HERE, "templates", "fang_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "FANG")
SYMBOL = "FANG"
GATE_RANGES = [("2008-01-01", "2009-12-31"), ("2010-01-01", "2013-12-31"), ("2014-01-01", "2017-12-31"), ("2018-01-01", "2021-12-31")]
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"production": (14, 46, 78, 148), "oil": (52, 60, 68, 167), "revenue": (-142, -30, 81, 177),
                     "loe_boe": (130, 58, -14, -44), "pretax_margin": (-8730, -3100, 2530, 49380)}
RULE_T_KEYS = {"production": (1, False), "oil": (1, False), "revenue": (1, False), "loe_boe": (1, True), "pretax_margin": (10, False)}
PRINT_KEYS = {"quarter", "fy", "q", "published", "source", "release", "release_time", "raw", "sales_b", "sales_pct", "production_pct",
              "oil_pct", "loe_boe_pct", "pretax_margin", "pretax_margin_bp", "next_print", "fy_actual"}


def trading_days(symbol):
    closes, _ = retro_tool.fetch_prices(symbol, as_traded=True)
    return closes


def weekly_dates(start, end, days):
    """The last trading day of each ISO week from START to END (inclusive): the gate's own weekly dates (no print moves them)."""
    weeks = {}
    for d in sorted(x for x in days if start <= x <= end):
        weeks[dt.date.fromisoformat(d).isocalendar()[:2]] = d
    return sorted(weeks.values())


def _year_txt(k, p):
    if p["eps_diluted"] is not None:
        return f"{k} {p['eps_diluted']:+.2f}"
    pf = f", pro forma {p['eps_pro_forma']:+.2f} not used" if p["eps_pro_forma"] is not None else ""
    return f"{k} no EPS (net income {p['net_income_m']:+,.1f}M{pf})"


def gate(as_of, facts, fang, pro_forma=False):
    """The reasons a date cannot be built (empty: it passes the gate). pro_forma=True is the sensitivity, never the rule."""
    why = []
    if as_of not in fang:
        why.append(f"no FANG close on {as_of}: Yahoo's FANG series starts on {facts['series_start']}, the first trading day of "
                   "Diamondback's common stock; no share of it or its predecessors traded before")
    vs = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vs:
        return why + [f"no offering document or 10-K of Diamondback in the fact sheet is public on {as_of} (the S-1 of 2012-02-14 "
                      "and its Amendments No. 1-5 were not read: every date before Amendment No. 6 precedes the listing)"]
    v = max(vs, key=lambda v: v["published"])
    years = {k: p for k, p in v["periods"].items() if p["months"] == 12}
    eps = lambda p: p["eps_diluted"] if p["eps_diluted"] is not None else (p["eps_pro_forma"] if pro_forma else None)
    kept = {k: eps(p) for k, p in years.items() if eps(p) is not None and eps(p) > 0}
    if not kept:
        part = ", ".join(f"{k} ({p['months']} months)" for k, p in sorted(v["periods"].items()) if p["months"] != 12)
        doc = f"{v['fy_label']} 10-K" if v["kind"] == "10-K" else v["fy_label"]
        why.append(f"no full year of positive EPS of Diamondback's own shares in the {doc} ({v['source']}, "
                   f"{v['published']}): years " + ", ".join(_year_txt(k, p) for k, p in sorted(years.items()))
                   + (f"; not years: {part}" if part else ""))
    return why


def write_gate_md(secs, path):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("# FANG: the buildability gate\n\nGenerated by `retro/build_fang.py --gate-md` (retro/README.md, \"FANG 2008-2009\" and "
                 "\"FANG 2014-2017\" and \"FANG 2018-2021\"). Each weekly date and the reason method r2 cannot build it, or that it passes the gate (its model is "
                 "in this folder). 2008-2013 take each ISO week's last trading day; from 2014 the dates are the builder's (in an earnings "
                 "week, the first trading day after the release).\n\n```\n")
        for sec in secs:
            for d, why in sec:
                fh.write(f"{d}  " + ("passes the gate (built)" if not why else "not built: " + "; ".join(why)) + "\n")
            n_pass = sum(1 for _, w in sec if not w)
            fh.write(f"{len(sec)} dates: {n_pass} pass the gate, {sum(1 for _, w in sec if w)} refused"
                     + ("; nothing written\n" if not n_pass else "\n"))
        fh.write("```\n")


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
    pct = lambda a, b: round(round((b / a - 1) * 100, 2), 1)
    m = lambda x, rev: x / rev * 100
    want = {"sales_b": round(r["rev_m"] / 1000, 4), "sales_pct": pct(r["rev_prior_m"], r["rev_m"]),
            "production_pct": pct(r["boe_prior_k"], r["boe_k"]), "oil_pct": pct(r["oil_prior_k"], r["oil_k"]),
            "loe_boe_pct": pct(r["loe_boe_prior"], r["loe_boe"]), "pretax_margin": round(m(r["pti_m"], r["rev_m"]), 2),
            "pretax_margin_bp": round((m(r["pti_m"], r["rev_m"]) - m(r["pti_prior_m"], r["rev_prior_m"])) * 100, 1)}
    for k, v in want.items():
        assert abs(p[k] - v) < 1e-9, (p["quarter"], k, p[k], v)
    assert r["rev_prior_m"] > 0 and r["boe_prior_k"] > 0, (p["quarter"], "growth on a year-ago zero or loss needs its encoding first")
    a = p.get("fy_actual")
    if a:
        t = a["one_off_test"]
        # a year is kept at GAAP unless it is a loss or its listed one-off charges exceed its income before income taxes, or, where
        # the listed items are a net benefit, the benefit exceeds the income without it (the mirror test)
        ch, be, pti = t["listed_charges_m"], t["listed_benefits_m"], t["pretax_m"]
        assert t["loss"] == (a["eps_gaap"] <= 0) and t["distorted"] == ((ch > pti if ch >= be else be > pti - be) and not t["loss"]), p["quarter"]
        assert t["kept"] == (not t["loss"] and not t["distorted"]), p["quarter"]


def history(as_of, facts):
    """The latest 10-K vintage with its model fields public on AS_OF, extended by the Q4 releases' years until their 10-K."""
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of and "eps_normalized" in v]
    assert vintages, (as_of, "the gate passed with no 10-K vintage holding a GAAP year")
    h = dict(vintages[-1])
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h["eps_excluded"]}
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    for p in public:
        check_print(p)
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["q"] == 4 else 0)
    prints = [p for p in public if guide_fy(p) >= first_fy]
    h["extended"] = ""
    for p in prints:
        a = p.get("fy_actual")
        if a and a["fy"] not in reported(h):          # the 10-K vintage, once out, wins
            y, t = str(a["fy"]), a["one_off_test"]
            if t["kept"]:
                h["eps_normalized"] = {**h["eps_normalized"], y: a["eps_gaap"]}
                h["check_year"] = a["fy"]
                h["check_pretax_margin"] = round(a["pretax_m"] / a["revenue_m"] * 100, 2)
            elif t["loss"]:
                h["eps_excluded"] = {**h["eps_excluded"], y: (f"a GAAP loss, ${a['eps_gaap']:.2f} diluted, in the {p['quarter']} release "
                                                              "(the 10-K's figures replace it); no figure excludes only the one-offs")}
            else:                                      # distorted (the AAPL FY2002 test or its mirror), from 2018
                h["eps_excluded"] = {**h["eps_excluded"], y: (
                    f"distorted in the {p['quarter']} release (the 10-K's figures replace it): ${t['listed_charges_m']:,.0f}M of listed "
                    f"one-off charges against ${t['pretax_m']:,.0f}M of income before income taxes (GAAP ${a['eps_gaap']:.2f} diluted); "
                    "no figure excludes only the one-offs")}
            assert (a["revenue_usd_b"], a["pretax_margin"]) == (round(a["revenue_m"] / 1000, 4), round(a["pretax_m"] / a["revenue_m"] * 100, 2))
            rv = dict(h["revenue_usd_b"]); rv[y] = a["revenue_usd_b"]
            h["revenue_usd_b"] = {k: v for k, v in rv.items() if int(k) > a["fy"] - 10}
            h["diluted_shares_m"] = {**h["diluted_shares_m"], y: a["diluted_shares_m"]}
            h["prev_fy_pretax_margin"] = a["pretax_margin"]
            h["prev_fy_sales_growth"] = a["sales_growth"]     # the release's own year against its own prior year
            h["fy_label"] = f"FY{a['fy'] % 100:02d}"
            h["extended"] += f", FY{y[2:]} from {p['source']} ({p['published']})"
    return h, public, prints


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    first_day = facts["series_start"]
    chart = retro_tool.chart(SYMBOL)
    assert not chart.get("events", {}).get("splits") and not facts["splits"], "a split needs its encoding first"
    assert min(raw) == first_day
    px = raw                                            # no split or distribution: Yahoo's close is the price as traded
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    assert not [g for g in facts["guides"] if g["published"] <= as_of], "a guide needs its encoding first"
    assert not [e for e in facts["events"] if e["published"] <= as_of], "an event needs its encoding first"
    # the dividend: the latest annual rate a release states (from the Q4 2017 release's initiation, 2018-02-14; "FANG 2018-2021")
    divs = [d for d in facts["dividends"] if d["published"] <= as_of]
    div = max(divs, key=lambda d: d["published"]) if divs else None
    h, public, prints = history(as_of, facts)
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after the {h['fy_label']} 10-K is in the fact sheet for this date")
    latest = prints[-1]
    i = public.index(latest)
    prev_seg = (public[i - 1]["production_pct"], public[i - 1]["quarter"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    excluded = {int(k): v for k, v in h["eps_excluded"].items()}
    cur_fy = max(set(eps_hist) | set(excluded)) + 1
    last_fy = max(eps_hist)        # the last full year in the history: cur_fy - 1 unless that year is excluded
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── current-FY EPS: no guide in numbers, so the last full year's EPS stands ──
    excluded_tail = "".join(f" (FY{y % 100:02d} is excluded: {excluded[y]})" for y in range(last_fy + 1, cur_fy))
    eps_now = eps_hist[last_fy]
    eps_label = f"{fy_e}: no EPS guide, FY{last_fy % 100:02d}'s GAAP ${money(eps_now)} stands" + excluded_tail
    fwd = [latest["sales_pct"]] * 2
    fwd_label, fwd_short, fwd_period = (f"no {fy_now} revenue guide in numbers, {latest['quarter']} revenues as reported",
                                        f"{latest['quarter'][:2]} revenues", latest["quarter"])
    guide_text = (f"{fy_now}: no revenue, EPS or margin guide in numbers (BASE takes {latest['quarter']} revenue growth as reported); "
                  "the releases guide production, unit costs and capital spending only (display only)")

    # ── market statistics, prices truncated at AS_OF, from the listing (the listing rule) ──
    days = sorted(d for d in px if first_day <= d <= as_of)
    close = px[as_of][2]
    assert minus_years(as_of, 1) >= first_day, (as_of, "less than a year since the listing")
    yr = [d for d in days if d > minus_years(as_of, 1)]
    low52, high52 = min(px[d][1] for d in yr), max(px[d][0] for d in yr)
    common = [d for d in yr if d in spx]
    ra = [math.log(px[common[k]][2] / px[common[k - 1]][2]) for k in range(1, len(common))]
    rm = [math.log(spx[common[k]][2] / spx[common[k - 1]][2]) for k in range(1, len(common))]
    ma, mm = sum(ra) / len(ra), sum(rm) / len(rm)
    vol = (sum((x - ma) ** 2 for x in ra) / len(ra)) ** 0.5 * 252 ** 0.5
    beta = (sum((x - ma) * (y - mm) for x, y in zip(ra, rm)) / len(ra)) / (sum((y - mm) ** 2 for y in rm) / len(rm))
    eps = {**eps_hist, cur_fy: eps_now}
    fy = lambda d: min(int(d[:4]), cur_fy)          # a day past the last reported year keeps the current year's EPS
    window = [d for d in days if d > minus_years(as_of, 10)]
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

    # ── durability and themes, from the vintage's own words ──
    why = (f"{h['fy_label']} 10-K: '{h['business_quote']}' Risk factors: '{h['cyclical_quote']}' and '{h['prices_quote']}' The kind is "
           "CYCLICAL on the 10-K's own word for its industry (the CB and LYB rule): the earnings are the oil price")
    live = sorted(((t["live_from"], k, t["scope"]) for k, t in retro_tool.load_taxonomy()["themes"].items() if t["live_from"] <= as_of))
    live_k = [k for _, k, _ in live]
    assert [k for k in live_k if k != "ENERGY_TRANSITION"] == ["OFFSHORE", "CLOUD", "ECOMMERCE", "STREAMING", "EV", "CRYPTO"][:len(live_k) - ("ENERGY_TRANSITION" in live_k)], \
        (as_of, "a live theme the FANG 10-Ks were not read for", live_k)
    out_live = [x for x in live if x[1] != "ENERGY_TRANSITION"]
    scopes = ", ".join(f"{k} {'is scoped to' if n == 0 else 'to'} '{sc}'" for n, (_, k, sc) in enumerate(out_live))
    why += f"; of the live disruption themes, {scopes}: none names an oil and gas producer"
    if "EV" in live_k:   # from 2020-01-01: EV's scope names ICE powertrains, auto parts suppliers and fuel retail ("FANG 2018-2021")
        assert h.get("conservation_quote"), (as_of, "EV is live: the vintage needs its own 10-K's demand words")
        why += ("; EV's 'fuel retail' names no Diamondback business (it produces and sells crude oil, natural gas and NGLs, and has "
                f"no retail outlets), and the {h['fy_label']} 10-K's '{h['conservation_quote']}' is the demand risk ENERGY_TRANSITION "
                "already carries on the watch list")
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none in scope", "No live disruption theme covers an onshore oil and gas producer"
    theme_summary = "no theme in the registry is live for an oil and gas producer on this date; none has dated evidence"
    et = retro_tool.load_taxonomy()["themes"]["ENERGY_TRANSITION"]
    if et["live_from"] <= as_of:
        # ENERGY_TRANSITION is live from 2015-12-12 and scoped to oil, gas and coal reserves; Diamondback's reserves are oil and gas, and
        # each 10-K's risk factor heading says climate legislation could reduce demand for them, so the theme goes on the watch list
        # (the XOM, KMI and LYB rule: company-acknowledged, no market read; text and labels only, no factor pair)
        val_word = ("a premium" if pe_now_pctl >= 70 else "a discount to its own history" if pe_now_pctl <= 30 else "near its own median")
        stage = "transition"
        watch = [{"theme": "ENERGY_TRANSITION", "status": "live, company-acknowledged; no market read",
                  "reason": (f"Live: Diamondback's own {h['fy_label']} 10-K says '{h['transition_quote']}' The stock trades at "
                             f"{close / eps_now:.1f}x {fy_e_s} — {val_word}. Re-file as DISRUPTION_EXPOSED (ENERGY_TRANSITION) only if "
                             "dated evidence shows the market pricing decarbonisation of Diamondback's oil and gas reserves specifically.")}]
        sig_name = "Energy transition: oil and gas demand"
        trigger = "Climate legislation raises costs and cuts demand for the oil and gas Diamondback produces"
        theme_summary = "the energy transition is live and company-acknowledged; no dated evidence ties the multiple to it"
        why += (f"; ENERGY_TRANSITION is live (from {et['live_from']}, scoped to '{et['scope']}'): Diamondback's reserves are oil and gas "
                "and its climate legislation risk factor puts the theme on the watch list, company-acknowledged, with no dated evidence "
                "that the market prices it for Diamondback")
    key_tail = ("By the company's own account the oil and natural gas industry is cyclical;\n"
                "  the bear needs prices to fall and stay down, not one quarter's.")
    cat3 = f"(3) The {fy_now} outlook — no revenue, EPS or margin guide in numbers (production, unit cost and capital spending guides only)"
    cat4 = (f"(4) Free cash flow — {h['fcf_label']} " + (f"${h['fcf_b']:.2f}B" if h["fcf_b"] >= 0 else f"$({-h['fcf_b']:.2f})B")
            + f" {h['fcf_note']}: " + ("the drilling program outspends operating cash flow" if h["fcf_b"] < 0 else
                                       "operating cash flow covers the drilling program"))

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:   # a print dated AS_OF: public before that close (before the open, during the session, or after the previous close)
        rt = same_day[-1]["release_time"]
        assert "(before the open)" in rt or "(during the session)" in rt or "(after the close)" in rt, (as_of, same_day[-1]["quarter"])
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the close)"

    company = facts["company"]
    if div:
        div_line = (f"CONS_DIVIDEND = {div['annual']:.2f}   # the latest annual rate: '{div['quote']}' ({div['source']}, {div['published']})")
        balance_tail = (f", dividend ${div['annual']:.2f} a year (the {div['note'].split(', the ')[1]}); the net change in the share count "
                        "(issuance for acquisitions, repurchases) is in BASE")
        capital_return = f"a dividend of ${div['annual']:.2f} a year; the share count's net change is in BASE"
    else:
        div_line = f"CONS_DIVIDEND = 0.00   # no dividend: '{h['no_dividend_quote']}' ({h['fy_label']} 10-K)"
        balance_tail = ", no dividend, no share repurchases (shares issued for acquisitions and offerings)"
        capital_return = "no dividend and no share repurchases; equity offerings fund acquisitions"
    vint_src = h["source"]
    listing_ids = [x["source"] for x in facts["listings"] if x["published"] <= as_of]
    ids = [vint_src] + [p["source"] for p in prints] + [public[i - 1]["source"]] + listing_ids + ([div["source"]] if div else [])
    sources = [dict(id=x, **facts["sources"][x]) for x in dict.fromkeys(ids)]
    sources.append({"id": "Y0", "published": as_of,
                    "title": "Yahoo Finance daily prices, Diamondback Energy, Inc. common stock (NASDAQ: FANG) and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/FANG/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E "
                                f"distribution from the listing ({first_day})"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "production_pct", "oil_pct", "loe_boe_pct", "pretax_margin",
                   "pretax_margin_bp")
    LATEST = {k: latest[k] for k in latest_keys}
    LATEST["eps_q"], LATEST["eps_q_prior"] = latest["raw"]["eps_q"], latest["raw"]["eps_q_prior"]
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    r_ = latest["raw"]
    activity = (f"Activity: total revenues ${r_['rev_m']:,.1f}M vs ${r_['rev_prior_m']:,.1f}M; production {r_['boe_k']:,.0f} MBOE vs "
                f"{r_['boe_prior_k']:,.0f}, oil {r_['oil_k']:,.0f} MBbl vs {r_['oil_prior_k']:,.0f}; LOE ${r_['loe_boe']:.2f}/BOE vs "
                f"${r_['loe_boe_prior']:.2f}; income before income taxes ${r_['pti_m']:,.1f}M vs ${r_['pti_prior_m']:,.1f}M; EPS GAAP, diluted")
    fy_rev = rev[max(rev)] * (1 + sum(fwd) / 2 / 100)
    fy_rev_label = f"{fwd_label}, applied to the year (no {fy_now} revenue guide)"
    franchise_q = f"{latest['quarter'].split()[0]} production {latest['production_pct']:+.1f}%, pre-tax margin {latest['pretax_margin']:.1f}%"
    R = repr
    norm_note = h["normalization"] + (f"; extended{h['extended']}" if h["extended"] else "")
    head = f'''#!/usr/bin/env python3
"""
FANG Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} (NASDAQ: FANG)  ·  Onshore oil and natural gas exploration and production, Permian Basin
Generated by retro/build_fang.py from retro/facts/FANG.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "{SYMBOL}"
LISTED_SYMBOL = "FANG"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md); oil and gas producer signals")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts above.
PIT_PROFILE = {{
    "kind": "CYCLICAL",
    "risk": 2,
    "why": {R(why)},
    "theme_watch": {R(watch)},
    "evidence": [],
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

# ── FACTS: company history ({vint_src}, vintage {h["published"]}{h["extended"]}) ──
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {norm_note}
REVENUE_HIST  = {R(rev)}   # total revenues, USD bn; {h["revenue_note"]}
SHARES_HIST   = {R({y: round(v, 1) for y, v in shares.items()})}   # {h["shares_note"]}
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_pretax_margin"]}   # pre-tax margin of {h["fy_label"]} (income before income taxes on total revenues)
CHECK_PRETAX_MARGIN = {h["check_pretax_margin"]}   # FY{h["check_year"] % 100:02d}'s pre-tax margin, the last year in the EPS history
TAX_RATE      = {h["tax_rate"]}   # the provision on income before income taxes of the vintage's last year in the EPS history
{div_line}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = "Pre-tax margin change"
KIND_TEXT     = "A cyclical onshore oil and gas producer"

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} outlook ──
LATEST          = {R(LATEST)}
PREV_SEG        = {R(prev_seg)}
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # no revenue guide in numbers: the latest quarter's revenue growth as reported
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = False   # no margin guide: no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {h["prev_fy_pretax_margin"]}
FY_REVENUE_B    = {fy_rev:.4f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {round(latest["raw"]["dil_sh_m"] / 1000, 5)!r}   # diluted shares, bn ({latest["quarter"]})
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenues {h['prev_fy_sales_growth']:+.1f}%; {franchise_q}")}
BALANCE_TEXT    = {R(f"{h['fcf_label']} free cash flow " + (f"${h['fcf_b']:.2f}B" if h['fcf_b'] >= 0 else f"$({-h['fcf_b']:.2f})B") + balance_tail)}
ACTIVITY_TEXT   = {R(activity)}
CAPITAL_RETURN  = "{capital_return}"
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
    ap.add_argument("--check", nargs=2, metavar=("START", "END"), help="report which weekly dates pass the gate")
    ap.add_argument("--json", action="store_true", help="with --check: print the passing dates as a JSON list only")
    ap.add_argument("--gate-md", action="store_true", help="write GATE.md: the gate's result on every weekly date of each range")
    ap.add_argument("--pro-forma", action="store_true", help="sensitivity: count pro forma per-share figures as EPS (writes nothing)")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    fang, spx = trading_days("FANG"), trading_days("^GSPC")
    assert min(fang) == facts["series_start"], (min(fang), "Yahoo's FANG series no longer starts where the fact sheet says")
    raw, spx3 = load_series(SYMBOL), load_series("^GSPC")
    g = lambda d: gate(d, facts, {k: c for k, c in fang.items() if k <= d}, a.pro_forma)
    # 2008-2013: the gate's own weekly dates (no FANG model can exist there); from 2014 the builder's earnings-week dates
    wk = lambda r0, r1: (weekly_dates(r0, r1, spx) if r1 < "2014-01-01" else earnings_weeks(r0, r1, sorted(spx), facts["prints"]))
    if a.gate_md:
        assert not a.pro_forma, "GATE.md is the rule's result, never the sensitivity's"
        secs = [[(d, g(d)) for d in wk(r0, r1)] for r0, r1 in GATE_RANGES]
        os.makedirs(a.out, exist_ok=True)
        write_gate_md(secs, os.path.join(a.out, "GATE.md"))
        print(f"{os.path.join(a.out, 'GATE.md')}: {sum(len(x) for x in secs)} dates, {sum(1 for x in secs for _, w in x if w)} refused")
        return
    rng = a.check or a.weekly
    dates = list(a.dates)
    if rng:
        r0, r1 = rng
        dates += (wk(r0, min(r1, "2013-12-31")) if r0 < "2014-01-01" else []) + (wk(max(r0, "2014-01-01"), r1) if r1 >= "2014-01-01" else [])
    dates = sorted(set(dates))
    for d in dates:
        if d not in spx:
            sys.exit(f"{d} is not a trading day")
    passing, refused = [], {}
    for d in dates:
        why = g(d)
        (refused.__setitem__(d, why) if why else passing.append(d))
    if a.check and a.json:
        print(json.dumps(passing))
        return
    built = 0
    for d in dates:
        if d in refused:
            print(f"{d}  not built: " + "; ".join(refused[d]))
        elif a.check or a.pro_forma:
            print(f"{d}  passes the gate")
        else:
            tag, q, stage = build(d, facts, raw, spx3, engine, os.path.abspath(a.out))
            built += 1
            print(f"{d}  {tag:<44}  latest print {q:<8}  theme evidence: {stage}")
    print(f"{len(dates)} dates: {len(passing)} pass the gate, {len(refused)} refused; {built} built"
          + (" (sensitivity: pro forma per-share figures counted as EPS)" if a.pro_forma else ""))


if __name__ == "__main__":
    main()
