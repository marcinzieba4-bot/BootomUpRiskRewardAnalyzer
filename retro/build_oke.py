#!/usr/bin/env python3
"""
Build OKE retrospective models from the dated fact sheet (retro/facts/OKE.json).

ONEOK, Inc., NYSE: OKE (CIK 1039684). The KMI sibling for a gas distributor that is also the general partner of a consolidated
midstream partnership: the same frozen rules (retro method r2), the same weekly dates and the same market statistics, with ONEOK's
own signals and rule-T thresholds (retro/templates/oke_engine.py.tmpl). For each as-of date the builder
  1. selects only the history vintage, prints, EPS guides and dividends whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF (Yahoo's OKE series times its factors after AS_OF, which
     gives the close as traded; the only factor inside the P/E window's reach is the 2:1 split of 2001-06-12, before its start),
  3. writes <OUT>/<AS_OF>/model.py = those facts + the frozen engine, which derives every scenario input by rule.

ONEOK's fiscal year is the calendar year from 2000 (fiscal 1997-1999 ended August 31; the four months to December 31, 1999 were a
transition period). The method r2 inputs map as follows (retro/README.md, "OKE"; decided before any OKE model was built or scored):
  - EPS: diluted EPS from continuing operations (before the 2003 cumulative effect), each year from the latest filing that reports it,
    at the company's figure excluding only one-offs where a filing prints it (2005 $2.53 and 2006 $2.40 without the gains on sale,
    the FY2006 10-K; the ACN rule), GAAP otherwise. FY2001 fails the AAPL FY2002 test on the latest filing that reports it (the OCC
    ruling and the Enron bankruptcy, $72.0M of listed items, against $43.5M of income from continuing operations), so the history and
    the P/E window start with FY2002 ('pe_window_start' 2002-01-01; the August fiscal years and the transition period stay out);
  - current-FY EPS: the midpoint of the latest 'net income guidance' range per diluted share for the year (the releases and the
    Item 7.01 guidance 8-Ks), GAAP; with none, the last full year's EPS (the rollover rule);
  - forward revenue growth: no filing guides revenue, so the latest quarter's revenue growth as reported stands in (the UNP rule);
    the segment operating income guides (Exhibit A of the guidance 8-Ks and releases) are components (the MSFT segment rule): no field;
  - guided margin step: none (no margin guide); the margin signal uses the latest quarter's pre-tax margin change;
  - dividend: the latest declared quarterly rate from the first filing that states it (the dividend 8-Ks), else the vintage's.
The kind is DURABLE: no ONEOK 10-K of FY2006-FY2008 calls its business cyclical (the word appears only in its billing cycle). No
disruption theme in taxonomy_eras.json is live for a gas utility and midstream company in 2008-2009 (OFFSHORE is scoped to IT services),
so the builder refuses events, and any other live theme, until an encoding is decided. ONEOK Partners, L.P. (NYSE: OKS) is a separate
listed entity: its units' prices and per-unit figures are never used; what ONEOK's own filings consolidate is in as published.

Weekly dates (--weekly START END): one per ISO week, the week's last trading day, except in a week with an earnings release, where it
is the first trading day after it. Every earnings 8-K of 2007-2009 was accepted after the close and counts from the next trading day.
Each Q4 print came one trading day before its 10-K, and no weekly date falls between them (the builder asserts the vintage is public).

From 2010 (retro/README.md, "OKE 2010-2013"):
  - the 2012 two-for-one split is the 'splits' record (effective 2012-06-04, Yahoo's split date): on or after it the per-share facts
    published before it are halved and share counts doubled (the shared on_basis of build_unp.py, each vintage year by its own
    publication date, 'eps_published' and 'shares_published'); prices as traded; the builder refuses dates from 2014-02-03 (Yahoo's
    ONE Gas factor) until it is encoded;
  - ONEOK guides net income in dollars from 2010, with no per-share figure: current-FY EPS is the latest range's midpoint over the
    diluted shares of the latest print public on the guide's date (its own release's where it is in one; the KMI rule), 'ni_guide_m' and
    'shares_print'; a guide restated in words ('words') keeps the last range;
  - Q4 2009 comes from the FY2009 10-K (the release files no earnings tables): 'source_10k' and 'sources_extra' (the NEM encoding);
  - from CLOUD's 2012-10-30 the 'why' quotes every live theme's registered scope (the UNH, CB and NEE wording).

From 2014 (retro/README.md, "OKE 2014-2017"):
  - the ONE Gas separation (one ONE Gas share for every four ONEOK shares, after the close on 2014-01-31) is the 'distributions' record:
    Yahoo books it as an 11422:10000 split on 2014-02-03, so from that date its factor is undone for the days before it and every price
    stays as traded (the MAR, PFE, BMY, SO, CMCSA and SPGI 'distributions' rule; the window's earlier days with ONE Gas, the SO Mirant
    reading); per-share facts are not restated, and the history keeps the distribution business until the FY2014 10-K restates it;
  - from the Q1 2014 release the natural gas distribution and energy services businesses are discontinued operations and no release
    reports a Distribution segment: 'dist_pct' is None (n/r), which the engine scores at BASE; from the Q4 2015 release the statement of
    income prints no net margin line, so net margin is revenues less cost of sales and fuel ('cost_m', ONEOK's own definition);
  - ONEOK gives net income attributable to ONEOK in its guidance tables only, as midpoints or approximately: a point guide ('ni_guide_m'
    with lo = hi, 'ni_guide_note'), over the latest print's diluted shares (the KMI rule); the FY2017 range of the 8-K of 2017-02-02
    assumes the pending acquisition of ONEOK Partners effective Jan. 1, 2017 ('pro_forma_ni_m', text only: a pending deal adds nothing);
  - from ECOMMERCE's, STREAMING's and ENERGY_TRANSITION's live dates the 'why' quotes their scopes; ENERGY_TRANSITION is out of scope
    (the TRGP and BKR reading: ONEOK Partners holds no reserves), with the vintage's own GHG and reserves words quoted (text only).

From 2018 (retro/README.md, "OKE 2018-2021"):
  - ONEOK guides net income in dollars and, from the 2020 guidance, diluted EPS too: the per-share range where stated ('eps_guide';
    a per-share midpoint alone is a point, lo = hi), else net income over the latest print's diluted shares (the KMI rule); a range
    with a note ('ni_guide_note', e.g. the Q1 2020 outlook given as the release withdraws the February guidance) shows the note;
  - EV (live 2020-01-01) and CRYPTO (2020-10-21) are out of scope (fuel retail, payments and banks): no FY2017-FY2020 10-K names
    electric vehicles or crypto ('theme_absent', asserted by the generator; text only); after the ONEOK Partners merger the
    ENERGY_TRANSITION reading names ONEOK as the holder of no reserves ('theme_holder'), and from the FY2019 10-K its climate-demand
    risk factor is quoted ('ENERGY_TRANSITION_demand', text only).

From 2022 (retro/README.md, "OKE 2022-2026"):
  - every numeric guide states diluted EPS, a range or a stated midpoint alone (a point, lo = hi; 'eps_guide'), one-offs in as
    published; a guide that includes an acquisition pending on its date is not used (the Q3 2024 consolidated midpoint, in the note);
  - GENAI (live 2022-11-30) and GLP1 (2023-08-08) are out of scope (software, services and content; food and devices): the FY2021-
    FY2024 10-Ks name no artificial intelligence and none names a GLP-1 drug ('theme_absent', asserted by the generator), the FY2025
    10-K's one AI sentence is its own computing policy ('GENAI_words', text only); the FY2023-FY2025 10-Ks' cloud words are its own
    cybersecurity vendors ('CLOUD_vendor', text only); the climate-demand risk factor is gone from the FY2021 10-K and its climate risk
    factor heading is quoted instead ('ENERGY_TRANSITION_esg', text only).

Output goes to staging/retrospective/OKE until the series is added to the archive (--out archive/retrospective/OKE).

Usage
  python3 retro/build_oke.py --weekly 2008-01-01 2009-12-31
  python3 retro/build_oke.py --weekly 2010-01-01 2013-12-31
  python3 retro/build_oke.py --weekly 2014-01-01 2017-12-31
  python3 retro/build_oke.py --weekly 2018-01-01 2021-12-31
  python3 retro/build_oke.py --weekly 2022-01-01 2026-11-27
  python3 retro/build_oke.py 2008-02-27
Then: python3 retro/retro_tool.py --archive staging/retrospective run staging/retrospective/OKE/<AS_OF>
"""
import argparse
import datetime as dt
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import retro_tool  # noqa: E402
from build_acn import MONTHS, load_series, minus_years, weekly_dates  # noqa: E402
from build_unp import money, on_basis  # noqa: E402

FACTS = os.path.join(HERE, "facts", "OKE.json")
ENGINE = os.path.join(HERE, "templates", "oke_engine.py.tmpl")
OUT = os.path.join(ROOT, "staging", "retrospective", "OKE")
SYMBOL = "OKE"
# rule T, the engine's signal thresholds: (BEAR, BASE, BULL, XBULL); the builder checks the fact sheet against them
ENGINE_THRESHOLDS = {"nm": (-8, 5, 17, 38), "dist": (-88, -42, 3, 57), "revenue": (-38, -6, 26, 261),
                     "op_margin": (-1350, -720, -100, 430), "pretax_margin": (-1150, -590, -30, 620)}
RULE_T_KEYS = {"nm": (1, False), "dist": (1, False), "revenue": (1, False), "op_margin": (10, False), "pretax_margin": (10, False)}
PRINT_KEYS = {"quarter", "fy", "q", "published", "source", "release", "release_time", "raw", "rows", "sales_b", "sales_pct", "nm_pct",
              "dist_pct", "opm", "opm_bp", "ptm", "ptm_bp", "eps_q", "eps_q_prior", "diluted_shares_m", "sales_note", "nm_note",
              "dist_note", "margin_note", "eps_note", "cash_note", "next_print", "source_title",
              "source_10k", "sources_extra"}                 # (OKE 2010-2013) Q4 2009 from the FY2009 10-K: the NEM 'source_10k' encoding
RAW_KEYS = {"rev_m", "rev_prior_m", "nm_m", "nm_prior_m", "oi_m", "oi_prior_m", "pti_m", "pti_prior_m", "dist_m", "dist_prior_m", "eps_q",
            "eps_q_prior", "dil_sh_m", "cost_m", "cost_prior_m"}   # (OKE 2014-2017) cost of sales and fuel, where no net margin line
GUIDE_BASE = {"fy", "published", "source", "doc", "quote"}
# one earnings field per guide: a per-share range (to 2009), a net income range in millions with the print whose diluted shares divide
# it (from 2010; the KMI rule), or words that restate the range (the last numeric range stands)
GUIDE_FIELDS = ({"eps_guide"}, {"eps_guide", "eps_guide_note"}, {"ni_guide_m", "shares_print"}, {"words"},
                {"ni_guide_m", "shares_print", "ni_guide_note"},         # (OKE 2014-2017) a point from the guidance tables
                {"pro_forma_ni_m", "pro_forma_note"})                     # (OKE 2014-2017) a guide on a pending deal: text only
YAHOO_FACTORS = {"1990-03-01": 2.0, "2001-06-12": 2.0, "2012-06-04": 2.0, "2014-02-03": 1.1422}
# (OKE 2014-2017) Yahoo's 11422:10000 factor of 2014-02-03 is the ONE Gas separation, a distribution: the 'distributions' record


def fiscal_year_end(n):
    """ONEOK's fiscal year n is the calendar year n (from 2000)."""
    return dt.date(n, 12, 31)


def fiscal_year(day):
    return dt.date.fromisoformat(day).year


def rule_t_value(k, r):
    """One annual rule-T value from its raw figures ((prior, current), thousands of dollars)."""
    pct = lambda a, b: round((b / a - 1) * 100 + 0.0, 2)
    if k == "revenue":
        return pct(*r["revenue_k"])
    if k == "nm":
        return pct(*r["net_margin_k"])
    if k == "dist":
        a, b = r["dist_oi_k"]
        return pct(a, b) if a > 0 else round((b - a) / abs(a) * 100 + 0.0, 2)
    (x0, x1), (s0, s1) = (r["oi_k"] if k == "op_margin" else r["pti_k"]), r["revenue_k"]
    return round((x1 / s1 - x0 / s0) * 10000 + 0.0, 1)


def rule_t(rt, keys=RULE_T_KEYS):
    """Rule T thresholds from the annual values (re-derived from the raw figures): XBULL best, BULL median, BASE worst, BEAR one
    median-to-worst step beyond the worst; rounded half up to whole percent and to 10 bp."""
    out = {}
    for k, (unit, lower) in keys.items():
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


def check_print(p):
    """Re-derive a print's growth rates and margins from its raw published figures (they must match the fact sheet)."""
    assert set(p) <= PRINT_KEYS, (p["quarter"], sorted(set(p) - PRINT_KEYS), "a print field with no encoding yet; decide one first")
    r = p["raw"]
    assert set(r) <= RAW_KEYS, (p["quarter"], sorted(set(r) - RAW_KEYS), "a raw field with no encoding yet")
    if "cost_m" in r:          # (OKE 2014-2017) net margin is revenues less cost of sales and fuel where the statement prints no line
        assert abs(r["nm_m"] - (r["rev_m"] - r["cost_m"])) < 1e-9 and abs(r["nm_prior_m"] - (r["rev_prior_m"] - r["cost_prior_m"])) < 1e-9
    # growth on the year-ago figure; against a year-ago loss, over the loss's absolute value (the CAT rule: the Distribution
    # segment's third quarters)
    g = lambda a, b: round((b / a - 1) * 100 + 0.0, 1) if a > 0 else round((b - a) / abs(a) * 100 + 0.0, 1)
    mg = lambda x, rev: round(x / rev * 100 + 0.0, 2)
    want = {"sales_b": round(r["rev_m"] / 1000, 3), "sales_pct": g(r["rev_prior_m"], r["rev_m"]), "nm_pct": g(r["nm_prior_m"], r["nm_m"]),
            "dist_pct": g(r["dist_prior_m"], r["dist_m"]) if r["dist_m"] is not None else None,   # n/r: no Distribution segment
            "opm": mg(r["oi_m"], r["rev_m"]), "opm_bp": round((mg(r["oi_m"], r["rev_m"]) - mg(r["oi_prior_m"], r["rev_prior_m"])) * 100, 1),
            "ptm": mg(r["pti_m"], r["rev_m"]), "ptm_bp": round((mg(r["pti_m"], r["rev_m"]) - mg(r["pti_prior_m"], r["rev_prior_m"])) * 100, 1),
            "eps_q": r["eps_q"], "eps_q_prior": r["eps_q_prior"], "diluted_shares_m": r["dil_sh_m"]}
    for k, v in want.items():
        assert p[k] == v or (v is not None and abs(p[k] - v) < 1e-9), (p["quarter"], k, p[k], v)


def shares_lit(x):
    """repr(x), with a digit separator where its four decimals would read as a calendar year (0.2092 is written 0.209_2; OKE 2010-2013:
    post-split share counts of 209 million), so the validator's year scan sees no false later year; the value is unchanged."""
    t = repr(x)
    return t[:-1] + "_" + t[-1] if re.fullmatch(r"0\.(19|20)\d\d", t) else t


def num_lit(x, as_of):
    """repr(x), with a digit separator where a number reads as a calendar year after AS_OF's (2095.0 is written 2_095.0; OKE 2022-2026:
    Q1 2023's operating margin change of +2,095bp), so the validator's year scan sees no false later year; the value is unchanged."""
    t = repr(x)
    m = re.fullmatch(r"()((?:19|20)\d\d)(\.\d+)?", t)   # a minus sign already stops the scan if isinstance(x, (int, float)) and not isinstance(x, bool) else None
    return f"{m.group(1)}{m.group(2)[0]}_{m.group(2)[1:]}{m.group(3) or ''}" if m and m.group(2) > as_of[:4] else t


def build(as_of, facts, raw, spx, engine, out):
    if as_of not in raw:
        sys.exit(f"{as_of} is not a trading day")
    chart = retro_tool.chart(SYMBOL)
    off = chart["meta"]["gmtoffset"]
    yahoo = {dt.datetime.fromtimestamp(v["date"] + off, dt.timezone.utc).date().isoformat(): v["numerator"] / v["denominator"]
             for v in chart.get("events", {}).get("splits", {}).values()}
    assert {d: round(x, 4) for d, x in yahoo.items()} == YAHOO_FACTORS, (as_of, "Yahoo's factors differ from the encoded ones")
    # the 2012 two-for-one split is the 'splits' record (OKE 2010-2013): on or after its effective date the per-share facts published
    # before it are halved and share counts doubled (the shared on_basis helper of build_unp.py); every factor after AS_OF multiplies
    # Yahoo's close, which gives the price as traded on AS_OF's share basis. The 1990 and 2001 splits precede the window and every
    # per-share fact (asserted below)
    splits = facts.get("splits", [])
    dists = facts.get("distributions", [])
    assert all(s["effective"] in yahoo for s in splits), "a split's effective date must match the price data"
    assert all(yahoo[s["effective"]] == s["ratio"] for s in splits if s["effective"] <= as_of), "a split's ratio must match"
    encoded = {s["effective"] for s in splits} | {x["effective"] for x in dists}
    assert {d for d in yahoo if "2002-01-01" <= d <= as_of} <= encoded, (as_of, "an unencoded split or distribution")
    fx = retro_tool.split_factor(chart, as_of)
    px = {d: tuple(v * fx for v in hlc) for d, hlc in raw.items()}   # Yahoo's close times the later factors: the price as traded
    # (OKE 2014-2017) a distribution (the ONE Gas separation, one ONE Gas share for every four ONEOK shares) is not a split: Yahoo books
    # it as an 11422:10000 split on 2014-02-03, so from that date its factor is undone for the days before it and every price stays as
    # traded (the MAR, PFE, BMY, SO, CMCSA and SPGI 'distributions' rule; the drop stays in the series); per-share facts are not restated
    for x in [x for x in dists if x["effective"] <= as_of]:
        assert yahoo.get(x["effective"]) == x["yahoo_factor"], (x["effective"], "Yahoo's distribution factor")
        px = {d: (tuple(v * x["yahoo_factor"] for v in hlc) if d < x["effective"] else hlc) for d, hlc in px.items()}
    pre = [p for p in facts["prints"] if p["published"] <= as_of]
    for p in pre:                                      # a print public on AS_OF must match its raw (as published) figures
        check_print(p)
    live_splits = [s for s in splits if s["effective"] <= as_of]
    k_basis = lambda pub: math.prod(s["ratio"] for s in live_splits if pub < s["effective"])
    basis_note = lambda pub: "".join(f" (per-share figures in this text before the {s['ratio']:g}-for-1 split effective {s['effective']})"
                                     for s in live_splits if pub < s["effective"])
    shares_raw = {p["quarter"]: p["diluted_shares_m"] for p in pre}
    facts, split_ids = on_basis({**facts, "guides": facts["eps_guides"]}, as_of)
    facts = {**facts, "eps_guides": facts["guides"], "guides": []}
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    for v in vintages:                                 # the fiscal calendar the vintages state must match the rule
        for y, end in v.get("fiscal_year_ends", {}).items():
            assert fiscal_year_end(int(y)).isoformat() == end, (y, end)
        assert not {d for d in yahoo if v["pe_window_start"] <= d <= as_of} - encoded, \
            (as_of, "an unencoded split or distribution inside the P/E window")
        assert all(pub > "2001-06-12" for pub in (list(v.get("eps_published", {}).values()) or [v["published"]])), \
            "a per-share fact before the 2001 split"
    for g in [g for g in facts["eps_guides"] if g["published"] <= as_of]:
        assert GUIDE_BASE <= set(g) and set(g) - GUIDE_BASE in GUIDE_FIELDS, (g["doc"], "a guide field with no encoding yet; decide one first")
    assert not [n for n in facts["company_names"] if n["published"] <= as_of], "a change of company name needs its encoding first"
    assert rule_t(facts["rule_t"]) == ENGINE_THRESHOLDS, "the engine's thresholds must follow rule T on the fact sheet's values"
    public = [p for p in facts["prints"] if p["published"] <= as_of]
    h = vintages[-1]                                   # latest annual history public on AS_OF
    reported = lambda h: {int(k) for k in h["eps_normalized"]} | {int(k) for k in h.get("eps_excluded", {})}
    first_fy = max(reported(h)) + 1
    guide_fy = lambda p: p["fy"] + (1 if p["q"] == 4 else 0)
    prints = [p for p in public if guide_fy(p) >= first_fy]
    for p in prints:                                   # a Q4 print in scope came a trading day before its 10-K: no weekly date between
        assert p["q"] != 4 or p["fy"] in reported(h), (as_of, p["quarter"], "a Q4 print ahead of its 10-K needs full-year actuals")
    events = [e for e in facts["events"] if e["published"] <= as_of]
    if events:
        sys.exit(f"{as_of}: the OKE builder has no encoding for event kinds {sorted({e['kind'] for e in events})}; decide one first")
    if not prints:
        sys.exit(f"{as_of}: no quarterly print after FY{first_fy - 1} is in the fact sheet for this date")
    latest = prints[-1]
    i = public.index(latest)
    assert i > 0, (as_of, "the fact sheet needs the print before the latest one")
    prev_seg = (public[i - 1]["nm_pct"], public[i - 1]["quarter"])
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}
    excluded = {int(k): v for k, v in h.get("eps_excluded", {}).items()}
    cur_fy = max(reported(h)) + 1
    last_fy = max(eps_hist)        # the last full year in the history: cur_fy - 1 unless that year is excluded
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"
    nq = latest["q"]
    next_q = f"Q{nq % 4 + 1} {latest['fy'] + (1 if nq == 4 else 0)}"

    # ── current-FY EPS: the latest net income guidance range per diluted share for the year (midpoint), else the last full year ──
    egs_all = [g for g in facts["eps_guides"] if g["published"] <= as_of and g["fy"] == cur_fy]
    egs = [g for g in egs_all if "words" not in g and "pro_forma_ni_m" not in g]
    pro_forma = [g for g in egs_all if "pro_forma_ni_m" in g]
    excluded_tail = "".join(f" (FY{y % 100:02d} is excluded: {excluded[y]})" for y in range(last_fy + 1, cur_fy))
    if egs:
        eg = egs[-1]
        guide_ids = [eg["source"]]
        if "eps_guide" in eg:
            lo, hi = eg["eps_guide"]
            eps_now = round((lo + hi) / 2, 3)
            how = f"the {eg['doc']}'s ${money(lo)}-{money(hi)} a diluted share, midpoint" + (
                f" ({eg['eps_guide_note']})" if eg.get("eps_guide_note") else "")
            if lo == hi:     # (OKE 2018-2021) a per-share midpoint stated alone: a point
                how = f"the {eg['doc']}'s ${money(lo)} a diluted share ({eg['eps_guide_note']})"
        else:
            # (OKE 2010-2013) from 2010 ONEOK guides net income attributable to ONEOK in dollars, with no per-share figure: the midpoint
            # over the diluted shares of the latest print public on the guide's date (its own release's where it is in one; the KMI rule)
            lo, hi = eg["ni_guide_m"]
            sp = [p for p in public if p["quarter"] == eg["shares_print"]]
            assert len(sp) == 1 and sp[0]["published"] <= eg["published"], (eg["doc"], "the shares' print must be public by the guide")
            assert not [p for p in public if sp[0]["published"] < p["published"] <= eg["published"]], (eg["doc"], "not the latest print")
            sh = sp[0]["diluted_shares_m"]
            eps_now = round((lo + hi) / 2 / sh, 3)
            sh_txt = (f"{sh:,.1f}M diluted shares ({eg['shares_print']}'s {shares_raw[eg['shares_print']]:,.3f}M, on the AS_OF basis)"
                      if sh != shares_raw[eg["shares_print"]] else f"{sh:,.3f}M diluted shares ({eg['shares_print']})")
            how = (f"the {eg['doc']}'s ${lo:,.0f}-{hi:,.0f} million (midpoint ${(lo + hi) / 2:,.1f} million"
                   + (f"; {eg['ni_guide_note']}" if eg.get("ni_guide_note") else "") + f") / {sh_txt}" if lo != hi else
                   f"the {eg['doc']}'s ${lo:,.0f} million ({eg['ni_guide_note']}) / {sh_txt}")     # (OKE 2014-2017) a point
            guide_ids.append(sp[0]["source"])
        eps_label = f"{fy_e}: GAAP net income guidance, {how} = ${money(eps_now)}" + excluded_tail
        words = [g for g in egs_all if "words" in g and g["published"] > eg["published"]]
        if words:
            eps_label += f"; restated in words: '{words[-1]['quote']}' ({words[-1]['doc']}; the last range stands)"
            guide_ids.append(words[-1]["source"])
        pf = [g for g in pro_forma if g["published"] > eg["published"]]
    else:
        eg = None
        eps_now = eps_hist[last_fy]
        how = None
        eps_label = f"{fy_e}: no EPS guide in scope yet, FY{last_fy % 100:02d}'s ${money(eps_now)} stands" + excluded_tail
        guide_ids = []
        pf = pro_forma
    if pf:      # (OKE 2014-2017) a net income guide that assumes a pending deal: shown, unused (the XOM XTO and PFE rule)
        lo, hi = pf[-1]["pro_forma_ni_m"]
        eps_label += f"; the {pf[-1]['doc']}'s ${lo:,.0f}-{hi:,.0f} million is not used: {pf[-1]['pro_forma_note']}"
        guide_ids.append(pf[-1]["source"])
    fwd = [latest["sales_pct"]] * 2
    fwd_label, fwd_short, fwd_period = (f"no {fy_now} revenue guide in numbers, {latest['quarter']} revenues as reported",
                                        f"{latest['quarter'][:2]} revenues", latest["quarter"])
    guide_text = (f"{fy_now}: no revenue or margin guide in numbers (BASE takes {latest['quarter']} revenue growth as reported); "
                  + (f"EPS ${money(eps_now)} from the {eg['doc']}: '{eg['quote']}'{basis_note(eg['published']) if 'eps_guide' in eg else ''}"
                     if eg else "no EPS guide for the year yet"))
    margin_guided = False                          # no margin guide: no guided step
    fy_margin_base = h["prev_fy_op_margin"]

    # ── dividend: the latest declared rate ──
    divs = [(d["published"], d["quarterly"] * 4, d["note"], d["source"]) for d in facts["dividends"] if d["published"] <= as_of]
    divs.append((h["published"], h["dividend_annual"], h["dividend_note"], None))
    dpub, dividend, dividend_note, dividend_src = max(divs, key=lambda x: x[0])
    dividend_note += basis_note(dpub)

    # ── listing (display): NYSE: OKE ──
    listing = [x for x in facts["listings"] if x["published"] <= as_of and x["effective"] <= as_of]
    assert listing, (as_of, "no listing in scope")
    exchange, listed = listing[-1]["exchange"], listing[-1]["symbol"]

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
    # the window: up to ten years, from the day after the distorted FY2001 that took the years before it
    window = [d for d in days if d > minus_years(as_of, 10) and d >= h["pe_window_start"]]
    gone = sorted({fy(d) for d in window} & set(excluded))       # an excluded year's own days leave the window
    window = [d for d in window if fy(d) not in excluded]
    assert all(fy(d) in eps for d in window), (as_of, "P/E window needs EPS for every fiscal year")
    years = (dt.date.fromisoformat(as_of) - dt.date.fromisoformat(window[0])).days / 365.25
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

    # ── era-dependent text, from facts only: no disruption theme in the registry is live for a gas distributor and midstream
    # partnership's general partner on these dates (OFFSHORE is scoped to IT services) ──
    live = sorted(((t["live_from"], k, t["scope"]) for k, t in retro_tool.load_taxonomy()["themes"].items() if t["live_from"] <= as_of))
    assert [k for _, k, _ in live] in (["OFFSHORE"], ["OFFSHORE", "CLOUD"], ["OFFSHORE", "CLOUD", "ECOMMERCE"],
                                       ["OFFSHORE", "CLOUD", "ECOMMERCE", "STREAMING"],
                                       ["OFFSHORE", "CLOUD", "ECOMMERCE", "STREAMING", "ENERGY_TRANSITION"],
                                       ["OFFSHORE", "CLOUD", "ECOMMERCE", "STREAMING", "ENERGY_TRANSITION", "EV"],      # (OKE 2018-2021)
                                       ["OFFSHORE", "CLOUD", "ECOMMERCE", "STREAMING", "ENERGY_TRANSITION", "EV", "CRYPTO"],
                                       ["OFFSHORE", "CLOUD", "ECOMMERCE", "STREAMING", "ENERGY_TRANSITION", "EV", "CRYPTO", "GENAI"],
                                       ["OFFSHORE", "CLOUD", "ECOMMERCE", "STREAMING", "ENERGY_TRANSITION", "EV", "CRYPTO", "GENAI",
                                        "GLP1"]), \
        (as_of, "a live theme needs its scope reading for OKE first", live)
    stage, watch, factors = "none", [], []
    sig_name, trigger = "Disruption theme: none in scope", "No live disruption theme covers gas utilities or midstream"
    theme_summary = "no theme in the registry is live for a gas distributor and midstream company on this date; none has dated evidence"
    key_tail = ("Regulated distribution rates and fee-based pipelines carry part of the cash, NGL spreads\n"
                "  and storage margins the rest; the bear needs both to give way.")
    if dists and dists[0]["effective"] <= as_of:   # (OKE 2014-2017) after the ONE Gas separation: no regulated distribution business
        key_tail = ("Fee-based NGL, gathering and pipeline services carry part of the cash, commodity-priced\n"
                    "  processing margins and NGL spreads the rest; the bear needs both to give way.")
    why = h["why"]
    if len(live) > 1:   # (OKE 2010-2013) from CLOUD's 2012-10-30: every live theme with its registered scope (the UNH, CB and NEE wording)
        scopes = ", ".join(f"{k} {'is scoped to' if i == 0 else 'to'} '{sc}'" for i, (_, k, sc) in enumerate(live))
        who = "a midstream company" if dists and dists[0]["effective"] <= as_of else "a gas distributor and midstream company"
        why += (f"; no disruption theme in the registry is live for {who} on this date (of the live "
                f"themes, {scopes}: none names gas distribution or midstream), so the watch list is empty")
        theme_summary = "no theme in the registry is live for a gas distributor and midstream company on this date (CLOUD and OFFSHORE are scoped to IT)"
    if len(live) > 2:   # (OKE 2014-2017) ECOMMERCE and STREAMING name no midstream business; ENERGY_TRANSITION is read as out of scope
        tq, keys = h.get("theme_quotes", {}), [k for _, k, _ in live]
        if "ENERGY_TRANSITION" in keys:
            assert "ENERGY_TRANSITION_ghg" in tq and "ENERGY_TRANSITION_reserves" in tq, (as_of, "the vintage's GHG and reserves words")
            holder = h.get("theme_holder", "ONEOK Partners")     # (OKE 2018-2021) after the merger, ONEOK itself
            why += (f"; ENERGY_TRANSITION's reserves and refining are out of scope (the TRGP and BKR reading): {holder} holds no "
                    f"reserves of its own and refines nothing ('{tq['ENERGY_TRANSITION_reserves']}'); its greenhouse gas risk factor: "
                    f"'{tq['ENERGY_TRANSITION_ghg']}' (text only)")
            if "ENERGY_TRANSITION_demand" in tq:    # (OKE 2018-2021) the FY2019 and FY2020 10-Ks' climate-demand risk factor, text only
                why += f"; its climate-demand risk factor: '{tq['ENERGY_TRANSITION_demand']}' (text only: the volumes are its producers')"
            if "ENERGY_TRANSITION_esg" in tq:       # (OKE 2022-2026) the FY2021-FY2025 10-Ks' climate risk factor heading, text only
                why += f"; its climate risk factor: '{tq['ENERGY_TRANSITION_esg']}' (text only)"
        if "EV" in keys:        # (OKE 2018-2021) EV's fuel retail and CRYPTO's payments and banks name no midstream business
            assert {"electric vehicle"} | ({"crypto"} if "CRYPTO" in keys else set()) <= set(h.get("theme_absent", [])), \
                (as_of, "the vintage must say which theme words its 10-K does not use")
            why += ("; " + ("EV and CRYPTO are" if "CRYPTO" in keys else "EV is") + " out of scope: the 10-K names "
                    + ("neither electric vehicles nor crypto" if "CRYPTO" in keys else "no electric vehicles") + " (text only)")
        if "GENAI" in keys:     # (OKE 2022-2026) GENAI's software, services and content and GLP1's food and devices name no midstream business
            assert "GENAI_words" in tq or "artificial intelligence" in h.get("theme_absent", []), (as_of, "the vintage's AI words")
            why += ("; GENAI" + (" and GLP1 are" if "GLP1" in keys else " is") + " out of scope: "
                    + (f"the 10-K's AI words are its own computing policy ('{tq['GENAI_words']}')" if "GENAI_words" in tq
                       else "the 10-K names no artificial intelligence")
                    + (" and it names no GLP-1 drug" if "GLP1" in keys else "") + " (text only)")
            if "GLP1" in keys:
                assert "GLP-1" in h.get("theme_absent", []), (as_of, "the vintage must say its 10-K names no GLP-1 drug")
        if "CLOUD_words" in tq:
            why += f"; the 10-K's one cloud sentence is an accounting standard: '{tq['CLOUD_words']}' (text only)"
        if "CLOUD_vendor" in tq:    # (OKE 2022-2026) the FY2023-FY2025 10-Ks' cloud words are ONEOK's own cybersecurity vendors
            why += f"; the 10-K's cloud words are its own cybersecurity vendors: '{tq['CLOUD_vendor']}' (text only)"
        theme_summary = ("no theme in the registry is live for a midstream company on this date (CLOUD and OFFSHORE are scoped to IT, "
                         "ECOMMERCE to retail, STREAMING to TV" + (", ENERGY_TRANSITION to reserves and refining" if "ENERGY_TRANSITION" in keys
                                                                    else "") + (", EV to fuel retail" if "EV" in keys else "")
                         + (", CRYPTO to payments and banks" if "CRYPTO" in keys else "")
                         + (", GENAI to software, services and content" if "GENAI" in keys else "")
                         + (", GLP1 to food and devices" if "GLP1" in keys else "") + ")")
    kind, pit_risk = "DURABLE", 2
    cat3 = (f"(3) The {fy_now} outlook — GAAP EPS ${money(eps_now)} ({how}); no revenue or margin guide in numbers" if eg else
            f"(3) The {fy_now} outlook — none yet: ONEOK guides net income per diluted share, not revenue or a margin")
    cat4 = f"(4) Free cash flow — {h['fcf_label']} {h['fcf_note']}"

    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{next_q} print)"
    same_day = [p for p in prints if p["published"] == as_of]
    if same_day:
        rt = same_day[-1].get("release_time", "")
        assert "before the open" in rt or f"after the close: counts from {as_of}" in rt, (as_of, same_day[-1]["quarter"],
                                                                                         "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, public before the open)"

    company = h["company"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"], p.get("source_10k")] + p.get("sources_extra", []) if x]
           + [public[i - 1]["source"]] + guide_ids + ([dividend_src] if dividend_src else []) + [listing[-1]["source"]] + split_ids
           + [x["source"] for x in dists if x["effective"] <= as_of])
    sources = [dict(id=x, **facts["sources"][x]) for x in dict.fromkeys(ids)]
    sources.append({"id": "Y0", "published": as_of,
                    "title": f"Yahoo Finance daily prices, {company} common stock ({exchange}: {listed}) and S&P 500, truncated at AS_OF",
                    "url": f"https://finance.yahoo.com/quote/{SYMBOL}/history",
                    "supports": f"close ${close:.2f} as traded on AS_OF, 52-week range, realized vol, beta, the {window_label} P/E "
                                f"distribution from {window[0]}" + "".join(f" (days before {x['effective']} as traded, with ONE Gas)"
                                                                           for x in dists if x["effective"] <= as_of)})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "sales_b", "sales_pct", "opm", "opm_bp", "ptm", "ptm_bp", "eps_q", "eps_q_prior", "nm_pct",
                   "dist_pct")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    first_excl = "; ".join(f"FY{int(y) % 100:02d} {t}" for y, t in sorted(h.get("eps_first_excluded", {}).items()))
    activity = (f"Activity: {latest['sales_note']}; {latest['nm_note']}; {latest['dist_note']}; {latest['margin_note']}; "
                f"{latest['cash_note']}; EPS {latest['eps_note']}{basis_note(latest['published'])}")
    fy_rev = rev[max(rev)] * (1 + sum(fwd) / 2 / 100)
    fy_rev_label = f"{fwd_label}, applied to the year (no {fy_now} revenue guide)"
    bp_txt = f"{latest['opm_bp']:+.0f}"
    if re.fullmatch(r"\+(19|20)\d\d", bp_txt) and bp_txt[1:] > as_of[:4]:     # (OKE 2022-2026) +2095bp would read as a later year
        bp_txt = f"{latest['opm_bp']:+,.0f}"
    franchise_q = f"{latest['quarter'].split()[0]} net margin {latest['nm_pct']:+.1f}%, operating margin {latest['opm']:.2f}% ({bp_txt}bp)"
    fcf_text = f"${h['fcf_b']:.2f}B" if h["fcf_b"] >= 0 else f"$({-h['fcf_b']:.2f})B"
    LATEST = {k: latest.get(k) for k in latest_keys}
    R = repr
    head = f'''#!/usr/bin/env python3
"""
{listed} Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
{company} ({exchange}: {listed})  ·  {h["business_line"]}
Generated by retro/build_oke.py from retro/facts/OKE.json: the constants below are the facts public on
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
               "derived from dated facts by frozen rules (retro/README.md); gas distribution and midstream "
               "signals with ONEOK's rule-T thresholds")
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
EXCHANGE        = {R(exchange)}   # display only; {listing[-1]["note"]}
CURRENT_PRICE   = {close:.2f}   # USD, {exchange} close {as_of}, as traded
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

# ── FACTS: company history ({", ".join(h["sources"])}, vintage {h["published"]}) ──
EPS_NORM      = {R({y: round(v, 4) for y, v in eps_hist.items()})}   # {h["normalization"]}{"; " + h["split_note"] if h.get("split_note") else ""}
EPS_FIRST_EXCLUDED = {R(first_excl)}
REVENUE_HIST  = {R({y: round(v, 6) for y, v in rev.items()})}   # revenues, USD bn
SHARES_HIST   = {R({y: round(v, 3) for y, v in shares.items()})}   # {h["shares_note"]}
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {h["prev_fy_op_margin"]}   # {h["prev_fy_op_margin_note"]}
CHECK_PRETAX_MARGIN = {h["check_pretax_margin"]}   # {h["check_pretax_note"]}
TAX_RATE      = {h["tax_rate"]}   # {h["tax_note"]}
CONS_DIVIDEND = {dividend:.2f}   # {dividend_note}
VOL_DIVIDEND  = CONS_DIVIDEND
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}
KIND_TEXT     = {R(h["kind_text"])}

# ── FACTS: latest print ({latest["source"]}, published {latest["published"]}) and {fy_now} outlook ──
LATEST          = {"{" + ", ".join(f"{k!r}: {num_lit(v, as_of)}" for k, v in LATEST.items()) + "}"}
PREV_SEG        = {R(prev_seg)}   # the previous print's net margin growth
EPP_TODAY_EPS   = {eps_now}   # {eps_label}
EPS_LABEL       = {R(eps_label)}
FWD_GUIDE       = {R(tuple(fwd))}   # no revenue guide in numbers: the latest quarter's revenue growth as reported
FWD_GUIDE_LABEL, FWD_PERIOD, FWD_BASIS_SHORT = {R(fwd_label)}, {R(fwd_period)}, {R(fwd_short)}
GUIDE_TEXT      = {R(guide_text)}
MARGIN_GUIDED   = {margin_guided}   # False: no margin guide, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {fy_rev:.2f}
FY_REVENUE_LABEL = {R(fy_rev_label)}
SHARES_DIL_B    = {shares_lit(round(latest["diluted_shares_m"] / 1000, 4))}   # diluted shares, bn
GROUPS          = {R([tuple(g) for g in h["groups"]])}
GROUPS_BASIS    = {R(h["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Franchise: {h['fy_label']} revenues {h['prev_fy_sales_growth']:+.1f}%; {franchise_q}")}
BALANCE_TEXT    = {R(f"{h['fcf_label']} free cash flow {fcf_text} (consolidated), dividend ${dividend:.2f} a year, {h['cash_return_text']}")}
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
    ap.add_argument("--out", default=OUT, help="output folder (default staging/retrospective/OKE)")
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
