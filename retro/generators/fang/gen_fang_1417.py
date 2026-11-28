#!/usr/bin/env python3
"""Extend retro/facts/FANG.json with 2014-2017 (filings accepted 2013-11-05 to 2017-12-29), asserting every earlier fact is unchanged.

The discipline of gen_fang.py (retro/README.md, "FANG 2014-2017"): each figure from its own row by label under an anchored heading,
each quoted sentence asserted present in its own filing, every derived figure (growth rate, margin, one-off test, rule-T value)
computed here, and a verbatim checklist written. This batch is the first whose dates pass the gate: FY2013 ($1.29 GAAP diluted EPS,
the FY2013 10-K and the Q4 2013 release, both accepted 2014-02-19 after the close) is the first full year of Diamondback's own EPS.
The sheet now holds what a model needs: the FY2013-FY2016 10-K vintages (gate periods and model fields), the prints Q3 2013 (only as
the previous print of the first date) to Q3 2017, each Q4 release's full year, the 10-Ks' own words for the durability call and the
energy-transition watch list, and the rule-T values of the filings public on the first date (the FY2013 10-K, with the FY2012 10-K for
the years it alone reports). Run:

    python3 retro/tools/edgar.py index 1539838 <dir>
    python3 retro/tools/edgar.py fetch 1539838 <dir> --from 2013-04-01 --to 2017-12-31 --forms 10-K 10-K/A 10-Q 10-Q/A 8-K 8-K/A
    python3 retro/tools/edgar.py fetch 1539838 <dir> --from 2013-02-01 --to 2013-03-31 --acc 0001539838-13-000004
    python3 -I retro/generators/fang/gen_fang_1417.py --filings <dir> [--facts-in <the 2008-2013 sheet>] [--out retro/facts/FANG.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_fang_1417.json

--facts-in is the 2008-2013 sheet (default retro/facts/FANG.json, which must then hold no fact published after 2013-12-31). It only appends.
"""
import argparse
import copy
import datetime as dt
import glob
import json
import math
import os
import re
import sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
_ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("--filings", required=True, help="folder edgar.py wrote (allrows.json, tenk/, eightk/); keep it outside the repo")
_ap.add_argument("--facts-in", help="the 2008-2013 fact sheet to extend (default retro/facts/FANG.json)")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/FANG.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_fang_1417.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402

ET = ZoneInfo("America/New_York")
PREV_CUT, CUT = "2013-12-31", "2017-12-29"
CIK = 1539838
FILINGS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("^GSPC")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
CHECK, TEXT = {}, {}
IN = A.facts_in or os.path.join(REPO, "retro", "facts", "FANG.json")
old = json.load(open(IN, encoding="utf-8"))
if all(s["published"] <= PREV_CUT for s in old["sources"].values()):
    f = copy.deepcopy(old)
else:                                                # re-running on the extended sheet: start from its 2008-2013 part
    f = copy.deepcopy(old)
    keep = {k for k, s in f["sources"].items() if s["published"] <= PREV_CUT and k in {"FG1", "FG2", "FG3", "FG4", "FG5", "FG6"}}
    f["sources"] = {k: v for k, v in f["sources"].items() if k in keep}
    f["history_vintages"] = [v for v in f["history_vintages"] if v["source"] in keep]
    for k in ("prints", "guides", "dividends", "events", "company_names", "splits"):
        f[k] = []
    for k in ("rule_t", "no_dividend_later", "release_notes_later"):
        f.pop(k, None)
    f["no_dividend"] = [d for d in f["no_dividend"] if d["source"] in keep]
OLD_IDS = set(f["sources"])
assert OLD_IDS == {"FG1", "FG2", "FG3", "FG4", "FG5", "FG6"}, OLD_IDS
OLD_SNAPSHOT = json.dumps({k: f[k] for k in ("sources", "history_vintages", "listings", "no_dividend", "release_notes", "amendments")},
                          sort_keys=True)


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def path(acc, pattern):
    hits = [p for sub in ("tenk", "eightk", "tenq", "other") for p in glob.glob(os.path.join(SP, sub, acc, pattern))]
    assert len(hits) == 1, (acc, pattern, hits)
    return hits[0]


def lines(p):
    if p not in TEXT:
        with open(p, encoding="utf-8", errors="replace") as fh:
            TEXT[p] = [norm(x) for x in fh.read().split("\n")]
    return TEXT[p]


def quote(p, s):
    assert norm(s) in norm(" ".join(lines(p))), (p, s[:120])
    CHECK.setdefault(p, []).append(s)
    return s


def num(c):
    c = c.strip().replace(",", "").replace("$", "").replace(" ", "")
    if c in ("--", "—", "-", "―", "–"):
        return 0.0
    neg = c.startswith("(") and c.endswith(")")
    return -float(c.strip("()")) if neg else float(c.strip("()"))


def cells(x):
    out = []
    for c in x.split("|")[1:]:
        c = c.strip()
        if not c or c.endswith("%"):
            continue
        out.append(num(c))
    return out


def row(p, labels, after=None, n=None, start=0):
    """The first row whose first cell is one of `labels` (from the first line at or after `start` that contains `after`, compared
    case-insensitively), as numbers; the row goes on the checklist."""
    labels = (labels,) if isinstance(labels, str) else labels
    ls = lines(p)
    i0 = next(i for i, x in enumerate(ls) if i >= start and after.lower() in x.lower()) if after else start
    for i in range(i0, len(ls)):
        x = ls[i]
        if x.split("|")[0].strip() in labels:
            v = cells(x)
            assert n is None or len(v) >= n, (p, labels, v)
            CHECK.setdefault(p, []).append(x)
            return v, i
    raise AssertionError((p, labels, after))


def published(acc):
    """The acceptance-time rule: accepted at or after 16:00 ET, the next trading day; otherwise that day."""
    r = FILINGS[acc]
    t = dt.datetime.fromisoformat(r[1].replace("Z", "+00:00")).astimezone(ET)
    day = t.date().isoformat()
    if t.hour >= 16 or day not in TDAYS:
        day = next(d for d in TDAYS if d > day)
    assert r[0] <= CUT, acc
    when = "after the close" if t.hour >= 16 else ("before the open" if (t.hour, t.minute) < (9, 30) else "during the session")
    return day, f"{t:%Y-%m-%d %H:%M} ET ({when})", when


def url(acc, p):
    return f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc.replace('-', '')}/{os.path.basename(p).split('__', 1)[1].replace('.rows.txt', '')}"


def source(sid, acc, p, title, supports):
    assert sid not in f["sources"], sid
    day, filed, when = published(acc)
    f["sources"][sid] = {"published": day, "filed": filed, "accession": acc, "title": title, "url": url(acc, p), "supports": supports}
    return day, filed, when


pct = lambda a, b: round((b / a - 1) * 100, 2)
COMB = "Diamondback Energy, Inc. with the Predecessors to 2012-10-11 (combined)"
PRED = "the Predecessors (Windsor Permian LLC and Windsor UT LLC)"
FANG_INC = "Diamondback Energy, Inc."

# ── the FY2012 10-K again (already source FG3): the production table for 2010-2012, used only by rule T (2011's changes) ─────────
p12 = path("0001539838-13-000004", "10-K__a12311210-k.rows.txt")
i12 = next(i for i, x in enumerate(lines(p12)) if x == "Production and Price History")
assert "2012 | 2011 | 2010" in lines(p12)[i12:i12 + 6]
CHECK.setdefault(p12, []).append("2012 | 2011 | 2010")
boe12, _ = row(p12, "Combined volumes (BOE)", start=i12, n=3)
oil12, _ = row(p12, "Oil (Bbls)", start=i12, n=3)
loe12, _ = row(p12, "Lease operating expense", "Average Costs (per BOE)", n=3, start=i12)

# ── the 10-K vintages FY2013-FY2016 (Item 6, five years each; the statements, the MD&A's production table) ───────────────────────
TENK = [("FG7", "0001539838-14-000007", "10-K__a12311310-k.rows.txt", 2013),
        ("FG8", "0001539838-15-000005", "10-K__a12311410-k.rows.txt", 2014),
        ("FG9", "0001539838-16-000129", "10-K__diamondback201510-k.rows.txt", 2015),
        ("FG10", "0001539838-17-000009", "10-K__diamondback201610-k.rows.txt", 2016)]
BUSINESS = {2013: "We are an independent oil and natural gas company currently focused on the acquisition, development, exploration and "
                  "exploitation of unconventional, onshore oil and natural gas reserves in the Permian Basin in West Texas.",
            2014: None, 2015: "We are an independent oil and natural gas company focused on the acquisition, development, exploration and "
                              "exploitation of unconventional, onshore oil and natural gas reserves in the Permian Basin in West Texas.",
            2016: None}
BUSINESS[2014], BUSINESS[2016] = BUSINESS[2013], BUSINESS[2015]
CYCLICAL = ("The oil and natural gas industry is cyclical, which can result in shortages of drilling rigs, equipment, raw materials "
            "(particularly sand and other proppants), supplies and personnel.")
TRANSITION = "The adoption of climate change legislation by Congress could result in increased operating costs and reduced demand for the oil and natural gas we produce."
PRICES = ("Our revenues, operating results, profitability, future rate of growth and the carrying value of our oil and natural gas "
          "properties depend significantly upon the prevailing prices for oil and natural gas.")
NO_DIV = "We have not paid any cash dividends since our inception."
vintages, P10K, TENK_INFO = [], {}, {}
for sid, acc, fname, fy in TENK:
    p = path(acc, fname)
    P10K[fy] = p
    ls = lines(p)
    i6 = max(i for i, x in enumerate(ls) if x == "ITEM 6. SELECTED FINANCIAL DATA")
    yrs = list(range(fy, fy - 5, -1))
    hdr = next(x for x in ls[i6:i6 + 8] if x.startswith("(In thousands, except per share amounts) |"))
    assert [int(c.strip()[:4]) for c in hdr.split("|")[1:]] == yrs, (sid, hdr)
    CHECK.setdefault(p, []).append(hdr)
    rev, _ = row(p, "Total revenues", start=i6, n=5)
    pti, _ = row(p, ("Income (loss) before income taxes", "Income before income taxes"), start=i6, n=5)
    ni_l = ("Net income (loss)",) if fy == 2013 else ("Net income (loss) attributable to Diamondback Energy, Inc.",)
    ni, _ = row(p, ni_l, start=i6, n=5)
    ie = next(i for i, x in enumerate(ls) if i > i6 and x == "Earnings per common share")
    eps, _ = row(p, "Diluted", start=ie)
    iw = next(i for i, x in enumerate(ls) if i > i6 and x == "Weighted average common shares outstanding")
    sh, _ = row(p, "Diluted", start=iw)
    ocf, _ = row(p, "Net cash provided by operating activities", start=i6, n=5)
    n_eps = fy - 2012                                   # the years with a GAAP EPS: 2013 on
    assert len(eps) == n_eps and len(sh) == n_eps, (sid, eps, sh)
    # the statement of operations (the first full statement after the F-pages index) and the statement of cash flows
    iso = next(i for i, x in enumerate(ls) if i > i6 + 200 and x in ("Combined Consolidated Statements of Operations",
                                                                       "Consolidated Statements of Operations"))
    def prod_sum(prefix):
        tot = None
        for x in ls[iso:iso + 30]:
            c0 = x.split("|")[0].strip()
            if c0 in (prefix, prefix + " - related party"):
                v = cells(x)
                CHECK.setdefault(p, []).append(x)
                tot = v if tot is None else [a + b for a, b in zip(tot, v)]
        assert tot is not None, (sid, prefix)
        return tot
    oil_s, gas_s, ngl_s = prod_sum("Oil sales"), prod_sum("Natural gas sales"), prod_sum("Natural gas liquid sales")
    tax, _ = row(p, ("Provision for income taxes", "Provision for (benefit from) income taxes"), start=i6, n=5)
    icf = next(i for i, x in enumerate(ls) if i > i6 + 200 and x == "Cash flows from investing activities:")
    capex = sum(row(p, lbl, start=icf, n=1)[0][0] for lbl in ("Additions to oil and natural gas properties",
                                                              "Additions to oil and natural gas properties-related party"))
    # the production table (Item 2's "Production and Price History"): combined volumes, oil, lease operating expense per BOE
    ipp = next(i for i, x in enumerate(ls) if x == "Production and Price History")
    boe, _ = row(p, "Combined volumes (BOE)", start=ipp, n=3)
    oil, _ = row(p, "Oil (Bbls)", start=ipp, n=3)
    loe, _ = row(p, "Lease operating expense", start=ipp, n=3)
    day, filed, _ = source(sid, acc, p, f"Diamondback FY{fy} 10-K",
                           f"Item 6, Selected Financial Data: total revenues, income (loss) before income taxes, the provision for income taxes, "
                           f"net income (loss) attributable to Diamondback, diluted EPS and diluted weighted average shares, net cash provided by "
                           f"operating activities for {fy - 4}-{fy}; the statements of operations (oil, natural gas and natural gas liquid "
                           f"sales) and cash flows (additions to oil and natural gas properties); Item 2's production and price history; Items "
                           f"1, 1A and 5")
    periods = {}
    for i, y in enumerate(yrs):
        e = eps[i] if i < n_eps else None
        periods[str(y)] = {"issuer": FANG_INC if y >= 2013 else (COMB if y == 2012 else PRED), "start": f"{y}-01-01",
                           "end": f"{y}-12-31", "months": 12, "revenue_m": round(rev[i] / 1000, 3), "pretax_m": round(pti[i] / 1000, 3),
                           "net_income_m": round(ni[i] / 1000, 3), "eps_diluted": e,
                           "eps_pro_forma": 0.6 if y == 2012 else None}
        if i < n_eps:
            periods[str(y)]["diluted_shares_m"] = round(sh[i] / 1000, 3)
            periods[str(y)]["tax_m"] = round(tax[i] / 1000, 3)
    TENK_INFO[fy] = {"ocf_m": ocf[0] / 1000, "capex_m": capex / 1000, "groups": (oil_s[:2], ngl_s[:2], gas_s[:2]),
                     "boe": boe, "oil": oil, "loe": loe}
    v = {"published": day, "source": sid, "kind": "10-K", "fy_label": f"FY{fy % 100:02d}", "periods": periods,
         "eps_basis": "GAAP diluted EPS as Item 6 prints it, on net income (loss) attributable to Diamondback Energy, Inc. (no discontinued "
                      "operations in the years shown); 2012 and earlier print no GAAP EPS (pro forma only, never used)",
         "business_quote": quote(p, BUSINESS[fy]), "cyclical_quote": quote(p, CYCLICAL), "prices_quote": quote(p, PRICES),
         "no_dividend_quote": quote(p, NO_DIV)}
    v["transition_quote"] = quote(p, TRANSITION)
    vintages.append(v)
V = {fy: v for (_, _, _, fy), v in zip(TENK, vintages)}
assert [V[fy]["periods"][str(fy)]["eps_diluted"] for fy in V] == [1.29, 3.64, -8.74, -2.20]
assert all(V[fy]["periods"][str(y)]["eps_diluted"] == V[2016]["periods"][str(y)]["eps_diluted"]
           for fy in V for y in range(2013, fy + 1)), "a later 10-K restates an EPS (none expected)"


# ── the one-off tests (the AAPL FY2002 test and its mirror; method r2) on each year's own figures ───────────────────────────────────
# The listed items are those the releases' adjusted net income removes besides the non-cash derivative marks, which recur every
# quarter (the NEE and PEP 2008 core rule: hedge marks are not one-offs): the impairment of oil and gas properties (the full cost
# ceiling test), the loss on extinguishment of debt and the (gain) loss on sale of assets. Pre-tax, against income before income taxes (the CHTR encoding; the releases
# give one tax adjustment for all the items together, the marks included, so no item has its own after-tax figure).
def test_of(fy, pretax_m, charges_m, benefits_m, ni_m, eps, source_txt):
    loss = eps is not None and eps <= 0
    distorted = charges_m > pretax_m if charges_m >= benefits_m else benefits_m > pretax_m - benefits_m
    return {"fy": fy, "pretax_m": pretax_m, "listed_charges_m": charges_m, "listed_benefits_m": benefits_m,
            "income_attributable_m": ni_m, "eps_gaap": eps, "loss": loss, "distorted": bool(distorted and not loss),
            "kept": not loss and not distorted, "source": source_txt}


def adj_items(p, col):
    """The twelve-month column of the release's adjusted net income table: impairment, loss on extinguishment of debt (one charge:
    impairment and the debt loss are summed) and (gain) loss on sale of assets."""
    i0 = next(i for i, x in enumerate(lines(p)) if x.startswith("Adjusted net income is a performance measure"))
    imp = sale = 0.0
    for x in lines(p)[i0:i0 + 25]:
        c0 = x.split("|")[0].strip()
        if c0.startswith("Impairment of oil and") or c0 == "Loss on extinguishment of debt":
            imp += cells(x)[col]; CHECK.setdefault(p, []).append(x)
        if c0.startswith("(Gain) loss on sale of assets"):
            sale = cells(x)[col]; CHECK.setdefault(p, []).append(x)
    return imp, sale


# ── the prints: each release's statement of operations and selected operating data, three months against the year-ago quarter ────
PRINTS = [  # quarter, fy, q, accession, the year-ago column of the operating data (1, or 2 where the release adds the prior quarter)
    ("Q3 2013", 2013, 3, "0001539838-13-000089", 1), ("Q4 2013", 2013, 4, "0001539838-14-000010", 1),
    ("Q1 2014", 2014, 1, "0001539838-14-000050", 1), ("Q2 2014", 2014, 2, "0001539838-14-000076", 1),
    ("Q3 2014", 2014, 3, "0001539838-14-000112", 1), ("Q4 2014", 2014, 4, "0001539838-15-000002", 1),
    ("Q1 2015", 2015, 1, "0001539838-15-000014", 1), ("Q2 2015", 2015, 2, "0001539838-15-000035", 1),
    ("Q3 2015", 2015, 3, "0001539838-15-000069", 1), ("Q4 2015", 2015, 4, "0001539838-16-000127", 1),
    ("Q1 2016", 2016, 1, "0001539838-16-000167", 1), ("Q2 2016", 2016, 2, "0001539838-16-000207", 1),
    ("Q3 2016", 2016, 3, "0001539838-16-000251", 1), ("Q4 2016", 2016, 4, "0001539838-17-000007", 1),
    ("Q1 2017", 2017, 1, "0001539838-17-000071", 1), ("Q2 2017", 2017, 2, "0001539838-17-000103", 1),
    ("Q3 2017", 2017, 3, "0001539838-17-000125", 2)]
REV_L = ("Total revenues", "Oil and natural gas revenues", "Oil, natural gas liquids and natural gas",
         "Oil, natural gas and natural gas liquids revenues")
PTI_L = ("Net income before income tax", "Income before income taxes", "Income (loss) before income taxes", "Income (loss) before income tax",
         "Loss before income taxes")
NEXT = {1: "Q2", 2: "Q3", 3: "Q4", 4: "Q1"}
prints = []
for k, (quarter, fy, q, acc, yago) in enumerate(PRINTS):
    p = path(acc, "EX-99.1__*.rows.txt")
    ls = lines(p)
    iso = next(i for i, x in enumerate(ls) if x == "Consolidated Statements of Operations")
    # total revenues where the statement adds lines (2017: lease bonus, midstream services), else its one revenue line
    tot = [i for i in range(iso, iso + 12) if ls[i].split("|")[0].strip() == "Total revenues"]
    rev, _ = row(p, "Total revenues" if tot else REV_L, start=iso, n=2)
    pti, _ = row(p, PTI_L, start=iso, n=2)
    ie = next((i for i in range(iso, iso + 50) if ls[i] == "Earnings per common share:"), None)
    if ie is not None:
        eps, _ = row(p, "Diluted", start=ie)
        iw = next(i for i in range(ie, ie + 6) if ls[i] == "Weighted average common shares outstanding:")
        sh, _ = row(p, "Diluted", start=iw)
    else:
        eps, _ = row(p, ("Diluted earnings per common share", "Diluted earnings per common share(1)"), start=iso)
        if quarter in ("Q3 2013", "Q4 2013", "Q1 2014"):   # the second "basic" row is the diluted count (a label slip in these releases)
            ib = next(i for i in range(iso, iso + 60) if ls[i].startswith("Weighted average number of basic"))
            assert ls[ib + 1].startswith("Weighted average number of basic shares outstanding"), (quarter, "the label slip moved")
            sh, _ = row(p, "Weighted average number of basic shares outstanding", start=ib + 1)
        else:
            sh, _ = row(p, "Weighted average number of diluted shares outstanding", start=iso)
    sh_m = sh[0] / 1e6 if sh[0] > 1e6 else sh[0] / 1000
    iop = next(i for i, x in enumerate(ls) if x == "Selected Operating Data")
    boe, _ = row(p, ("Oil Equivalents (1)(2) (MBOE)", "Oil Equivalents (MBOE)(1)(2)"), start=iop, n=2)
    oil, _ = row(p, "Oil (MBbl)", start=iop, n=2)
    loe, _ = row(p, ("Lease operating expenses", "Lease operating expense"), "Average costs per BOE", start=iop, n=2)
    # the year-ago diluted EPS: the statement's second column, where printed (Q3 and Q4 2013 have none: 2012 had pro forma only)
    n_cols = 4 if q > 1 else 2
    eps_prior = None if quarter in ("Q3 2013", "Q4 2013") else eps[1]
    assert quarter in ("Q3 2013", "Q4 2013") or len(eps) == n_cols, (quarter, eps)
    day, filed, when = source(f"FG{20 + k}", acc, p, f"Diamondback {quarter} earnings release (8-K, exhibit 99.1)",
                              "Consolidated statements of operations (revenues, income before income taxes, diluted EPS and shares, three "
                              "months against the year-ago quarter) and selected operating data (oil and oil-equivalent production, lease "
                              "operating expense per BOE)" + ("; the twelve months" if q == 4 else ""))
    raw = {"rev_m": rev[0] / 1000, "rev_prior_m": rev[1] / 1000, "pti_m": pti[0] / 1000, "pti_prior_m": pti[1] / 1000,
           "eps_q": eps[0], "eps_q_prior": eps_prior, "dil_sh_m": round(sh_m, 3), "boe_k": boe[0], "boe_prior_k": boe[yago],
           "oil_k": oil[0], "oil_prior_k": oil[yago], "loe_boe": loe[0], "loe_boe_prior": loe[yago]}
    ptm, ptm_p = raw["pti_m"] / raw["rev_m"] * 100, raw["pti_prior_m"] / raw["rev_prior_m"] * 100
    pr = {"quarter": quarter, "fy": fy, "q": q, "published": day, "source": f"FG{20 + k}",
          "release": dt.date.fromisoformat(day).strftime("%Y-%m-%d"), "release_time": f"accepted {filed}",
          "raw": raw, "sales_b": round(raw["rev_m"] / 1000, 4), "sales_pct": round(pct(raw["rev_prior_m"], raw["rev_m"]), 1),
          "production_pct": round(pct(raw["boe_prior_k"], raw["boe_k"]), 1), "oil_pct": round(pct(raw["oil_prior_k"], raw["oil_k"]), 1),
          "loe_boe_pct": round(pct(raw["loe_boe_prior"], raw["loe_boe"]), 1),
          "pretax_margin": round(ptm, 2), "pretax_margin_bp": round((ptm - ptm_p) * 100, 1),
          "next_print": f"{NEXT[q]} {fy + (1 if q == 4 else 0)} release (early {['May', 'August', 'November', 'February'][q % 4 - 1 if q < 4 else 3]})"}
    if q == 4:   # the release's twelve months: the year joins the history from the release until the 10-K
        fy_rev, _ = row(p, "Total revenues" if tot else REV_L, start=iso, n=4)
        assert len(eps) >= 2
        fy_eps = eps[1] if quarter == "Q4 2013" else eps[2]
        fy_sh = (sh[1] if quarter == "Q4 2013" else sh[2])
        fy_sh_m = fy_sh / 1e6 if fy_sh > 1e6 else fy_sh / 1000
        ni_l = ("Net income (loss)",) if fy == 2013 else ("Net income attributable to Diamondback Energy, Inc.",
                                                          "Net income (loss) attributable to Diamondback Energy, Inc.")
        ni, _ = row(p, ni_l, start=iso, n=4)
        imp, sale = (0.0, 0.0) if fy == 2013 else adj_items(p, 2)
        t = test_of(fy, pti[2] / 1000, max(imp, 0) / 1000 + max(sale, 0) / 1000, max(-sale, 0) / 1000, ni[2] / 1000, fy_eps,
                    f"{quarter} release: the adjusted net income table's impairment, loss on extinguishment of debt and (gain) loss on sale of assets, twelve months")
        pr["fy_actual"] = {"fy": fy, "eps_gaap": fy_eps, "revenue_m": fy_rev[2] / 1000, "diluted_shares_m": round(fy_sh_m, 3),
                           "pretax_m": pti[2] / 1000, "net_income_m": ni[2] / 1000, "one_off_test": t,
                           # the figures a model derives from the release's year, stored on the release (the leak scan's tokens)
                           "revenue_usd_b": round(fy_rev[2] / 1e6, 4), "pretax_margin": round(pti[2] / fy_rev[2] * 100, 2),
                           "sales_growth": round(pct(fy_rev[3], fy_rev[2]), 1)}
    prints.append(pr)
P = {pr["quarter"]: pr for pr in prints}
# the Q4 releases' years agree with the 10-Ks that follow them
for fy in (2013, 2014, 2015, 2016):
    a, per = P[f"Q4 {fy}"]["fy_actual"], V[fy]["periods"][str(fy)]
    assert (a["eps_gaap"], round(a["revenue_m"], 3), round(a["pretax_m"], 3)) == (per["eps_diluted"], per["revenue_m"], per["pretax_m"]), (fy, a, per)

# ── the one-off test on each 10-K year and the model fields of each vintage ──────────────────────────────────────────────────────
TESTS = {fy: P[f"Q4 {fy}"]["fy_actual"]["one_off_test"] for fy in (2013, 2014, 2015, 2016)}
assert [TESTS[y]["kept"] for y in (2013, 2014, 2015, 2016)] == [True, True, False, False]
assert TESTS[2015]["loss"] and TESTS[2016]["loss"]
EXCL = {"2012": "no GAAP EPS of Diamondback's shares for the year (the Company with the Predecessors; pro forma $0.60 only, unused), and "
                "the $54.1M first-day deferred tax charge of the Merger exceeds its $18.4M income before income taxes (the AAPL FY2002 test)",
        "2015": "a GAAP loss, $(8.74) diluted, after the $814.8M full cost ceiling impairment; the company's adjusted net income ($1.81) "
                "also removes the non-cash derivative marks, which recur, so no figure excludes only the one-offs (the loss rule)",
        "2016": "a GAAP loss, $(2.20) diluted, after the $245.5M full cost ceiling impairment; the company's adjusted net income also "
                "removes the non-cash derivative marks, which recur, so no figure excludes only the one-offs (the loss rule)"}
rev_all = {}
for y, per in V[2013]["periods"].items():
    pass
# each year's revenue from the latest filing public on the vintage's date that reports it (2008 from the FY2012 10-K)
fg3 = next(v for v in f["history_vintages"] if v["source"] == "FG3")
for fy, v in V.items():
    revs = {int(y): p_["revenue_m"] for y, p_ in fg3["periods"].items()}
    for fy2 in range(2013, fy + 1):
        revs.update({int(y): p_["revenue_m"] for y, p_ in V[fy2]["periods"].items()})
    revs = {y: r for y, r in revs.items() if y > fy - 10}
    per = v["periods"]
    kept = {y: per[y]["eps_diluted"] for y in per if per[y]["eps_diluted"] is not None and TESTS[int(y)]["kept"]}
    last_kept = max(int(y) for y in kept)
    lk = per[str(last_kept)]
    info = TENK_INFO[fy]
    (o, ng, g) = info["groups"]
    v.update({
        "eps_normalized": kept,
        "eps_excluded": {y: EXCL[y] for y in EXCL if int(y) <= fy and y in per},
        "revenue_usd_b": {str(y): round(r / 1000, 4) for y, r in sorted(revs.items())},
        "diluted_shares_m": {y: per[y]["diluted_shares_m"] for y in per if "diluted_shares_m" in per[y]},
        "normalization": ("GAAP diluted EPS on net income attributable to Diamondback; " + "; ".join(
            f"FY{y[2:]} excluded: {EXCL[y]}" for y in EXCL if int(y) <= fy and y in per)),
        "revenue_note": (f"total revenues as each year's latest filing reports it ({min(revs)}-2011 the Predecessors, 2012 combined, as "
                         "the 10-Ks' selected financial data present them; 2008 from the FY2012 10-K)"),
        "shares_note": "diluted weighted average shares, M (2013 on; no GAAP share count before)",
        "prev_fy_pretax_margin": round(per[str(fy)]["pretax_m"] / per[str(fy)]["revenue_m"] * 100, 2),
        "check_year": last_kept,
        "check_pretax_margin": round(lk["pretax_m"] / lk["revenue_m"] * 100, 2),
        "tax_rate": round(lk["tax_m"] / lk["pretax_m"], 4),
        "prev_fy_sales_growth": round(pct(revs[fy - 1], revs[fy]), 1),
        "groups": [["Oil sales", round(o[0] / 1e6, 4), round(pct(o[1], o[0]), 1)],
                   ["Natural gas liquid sales", round(ng[0] / 1e6, 4), round(pct(ng[1], ng[0]), 1)],
                   ["Natural gas sales", round(g[0] / 1e6, 4), round(pct(g[1], g[0]), 1)]],
        "groups_basis": f"{fy} oil, natural gas liquid and natural gas sales (related-party sales included)",
        "fcf_b": round((info["ocf_m"] + info["capex_m"]) / 1000, 4),
        "fcf_note": (f"(net cash provided by operating activities ${info['ocf_m'] / 1000:.3f}B less additions to oil and natural gas "
                     f"properties ${-info['capex_m'] / 1000:.3f}B; acquisitions not deducted)"),
        "fcf_label": f"FY{fy % 100:02d}",
        "one_off_tests": {str(y): TESTS[y] for y in TESTS if y <= fy},
    })

# ── rule T: the annual changes the filings public on the first date (2014-02-21) report, each from the latest filing that reports both
# years (the FY2013 10-K; the FY2012 10-K for 2011's changes in production and unit costs and for 2009's revenue and margin) ─────────
k13 = V[2013]["periods"]
prod13, oil13, loe13 = TENK_INFO[2013]["boe"], TENK_INFO[2013]["oil"], TENK_INFO[2013]["loe"]
rt_vals = {
    "production": {"2011": pct(boe12[2], boe12[1]), "2012": pct(prod13[2], prod13[1]), "2013": pct(prod13[1], prod13[0])},
    "oil": {"2011": pct(oil12[2], oil12[1]), "2012": pct(oil13[2], oil13[1]), "2013": pct(oil13[1], oil13[0])},
    "revenue": {"2009": pct(fg3["periods"]["2008"]["revenue_m"], fg3["periods"]["2009"]["revenue_m"]),
                **{str(y): pct(k13[str(y - 1)]["revenue_m"], k13[str(y)]["revenue_m"]) for y in (2010, 2011, 2012, 2013)}},
    "loe_boe": {"2011": pct(loe12[2], loe12[1]), "2012": pct(loe13[2], loe13[1]), "2013": pct(loe13[1], loe13[0])},
}
ptm_ = lambda per: per["pretax_m"] / per["revenue_m"] * 100
rt_vals["pretax_margin"] = {"2009": round((ptm_(fg3["periods"]["2009"]) - ptm_(fg3["periods"]["2008"])) * 100, 1),
                            **{str(y): round((ptm_(k13[str(y)]) - ptm_(k13[str(y - 1)])) * 100, 1) for y in (2010, 2011, 2012, 2013)}}
RT_KEYS = {"production": (1, False), "oil": (1, False), "revenue": (1, False), "loe_boe": (1, True), "pretax_margin": (10, False)}
rule_t = {}
for k_, (unit, lower) in RT_KEYS.items():
    v_ = sorted(rt_vals[k_].values())
    n = len(v_)
    med = v_[n // 2] if n % 2 else (v_[n // 2 - 1] + v_[n // 2]) / 2
    worst, best = (v_[-1], v_[0]) if lower else (v_[0], v_[-1])
    r = lambda x: math.floor(x / unit + 0.5) * unit
    rule_t[k_] = {"unit": unit, "lower_is_better": lower, "values": rt_vals[k_],
                  "thresholds": {"BEAR": r(worst + (worst - med)), "BASE": r(worst), "BULL": r(med), "XBULL": r(best)}}
rule_t["_doc"] = ("Rule T over the annual changes the filings public on 2014-02-21 (the first built date) report, each from the latest "
                  "filing that reports both years: the FY2013 10-K (Item 2's production and price history for 2011-2013, Item 6 for "
                  "2009-2013) and the FY2012 10-K (2010's production and unit cost, 2008's revenue and income before income taxes); "
                  "the Predecessors' years as the 10-Ks present them (combined under common control). Lease operating expense per BOE "
                  "is on each 10-K's own basis (the FY2013 10-K moves ad valorem taxes out of it and corporate overhead into it).")

# ── write ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
f["history_vintages"] += vintages
f["prints"] = prints
f["rule_t"] = rule_t
f["no_dividend"] += [{"published": V[fy]["published"], "source": V[fy]["source"], "quote": V[fy]["no_dividend_quote"]} for fy in V]
f["_doc"] = (f["_doc"].split(" | 2014-2017:")[0] + " | 2014-2017: extended by retro/generators/fang/gen_fang_1417.py with the FY2013-"
             "FY2016 10-K vintages (gate periods and model fields), the prints Q3 2013-Q3 2017 with each Q4 release's year and its "
             "one-off test, and the rule-T values; FY2013 is the first full year of Diamondback's own EPS (retro/README.md, \"FANG 2014-2017\").")
assert json.dumps({k: [v for v in f[k] if v.get("source") in OLD_IDS] if isinstance(f[k], list) else {kk: vv for kk, vv in f[k].items() if kk in OLD_IDS}
                   for k in ("sources", "history_vintages", "no_dividend")}, sort_keys=True) == json.dumps(
    {k: json.loads(OLD_SNAPSHOT)[k] for k in ("sources", "history_vintages", "no_dividend")}, sort_keys=True), "an earlier fact changed"
for s in f["sources"].values():
    assert s["published"] <= CUT
out = A.out or os.path.join(REPO, "retro", "facts", "FANG.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(f, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_fang_1417.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump({p: sorted(set(v)) for p, v in CHECK.items()}, fh, ensure_ascii=False, indent=1)
print(f"{out}: {len(vintages)} vintages, {len(prints)} prints; checklist {ck}: {sum(len(set(v)) for v in CHECK.values())} strings")
for pr in prints:
    print(pr["quarter"], pr["published"], pr["release_time"], pr["sales_pct"], pr["production_pct"], pr["oil_pct"], pr["loe_boe_pct"],
          pr["pretax_margin"], pr["pretax_margin_bp"], pr["raw"]["eps_q"], pr["raw"]["eps_q_prior"], pr["raw"]["dil_sh_m"])
for k_, v_ in rule_t.items():
    if k_ != "_doc":
        print(k_, v_["values"], v_["thresholds"])
for fy, t in TESTS.items():
    print(fy, t)
