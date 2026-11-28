#!/usr/bin/env python3
"""Extend retro/facts/FANG.json with 2018-2021 (filings accepted 2017-12-30 to 2021-12-31), asserting every earlier fact is unchanged.

The discipline of gen_fang.py and gen_fang_1417.py (retro/README.md, "FANG 2018-2021"): each figure from its own row by label under an
anchored heading, each quoted sentence asserted present in its own filing, every derived figure (growth rate, margin, one-off test)
computed here, and a verbatim checklist written. This batch appends the FY2017-FY2020 10-K vintages (model fields; the FY2020 10-K
reserves Item 6, so its three statement years stand and earlier years are carried from the latest earlier vintage), the prints Q4 2017
to Q3 2021 (each Q4 release's full year with its one-off test), and the dividend rates, each from the release that first states it.
Rule T is not re-derived: it stays on the filings public on the first built date (2014-02-21; "FANG 2014-2017"). Run:

    python3 retro/tools/edgar.py index 1539838 <dir>
    python3 retro/tools/edgar.py fetch 1539838 <dir> --from 2017-10-01 --to 2021-12-31 --forms 10-K 10-K/A 8-K 8-K/A
    python3 -I retro/generators/fang/gen_fang_1821.py --filings <dir> [--facts-in <the 2008-2017 sheet>] [--out retro/facts/FANG.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_fang_1821.json

--facts-in is the 2008-2017 sheet (default retro/facts/FANG.json; facts published after 2017-12-29 are dropped first, so a re-run on
the extended sheet regenerates it byte for byte). It only appends.
"""
import argparse
import copy
import datetime as dt
import glob
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
_ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("--filings", required=True, help="folder edgar.py wrote (allrows.json, tenk/, eightk/); keep it outside the repo")
_ap.add_argument("--facts-in", help="the 2008-2017 fact sheet to extend (default retro/facts/FANG.json)")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/FANG.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_fang_1821.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402

ET = ZoneInfo("America/New_York")
PREV_CUT, CUT = "2017-12-29", "2021-12-31"
CIK = 1539838
FILINGS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("^GSPC")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
CHECK, TEXT = {}, {}
IN = A.facts_in or os.path.join(REPO, "retro", "facts", "FANG.json")
f = copy.deepcopy(json.load(open(IN, encoding="utf-8")))
# a re-run on the extended sheet: keep only the facts published by 2017-12-29 (this batch's own facts are all later)
later = {k for k, s in f["sources"].items() if s["published"] > PREV_CUT}
f["sources"] = {k: v for k, v in f["sources"].items() if k not in later}
f["history_vintages"] = [v for v in f["history_vintages"] if v["source"] not in later]
f["prints"] = [p for p in f["prints"] if p["source"] not in later]
f["dividends"] = [d for d in f["dividends"] if d["source"] not in later]
f["amendments"] = [a for a in f.get("amendments", []) if a["published"] <= PREV_CUT]
f["_doc"] = f["_doc"].split(" | 2018-2021:")[0]
OLD_IDS = set(f["sources"])
assert OLD_IDS == {f"FG{i}" for i in range(1, 11)} | {f"FG{i}" for i in range(20, 37)}, sorted(OLD_IDS)
assert not f["dividends"] and not f["guides"] and not f["events"] and not f["splits"]
OLD_SNAPSHOT = json.dumps(f, sort_keys=True)


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


def row(p, labels, after=None, n=None, start=0, stop=None):
    """The first row whose first cell is one of `labels` (from the first line at or after `start` that contains `after`), as numbers;
    the row goes on the checklist."""
    labels = (labels,) if isinstance(labels, str) else labels
    ls = lines(p)
    i0 = next(i for i, x in enumerate(ls) if i >= start and after.lower() in x.lower()) if after else start
    for i in range(i0, len(ls) if stop is None else stop):
        x = ls[i]
        if x.split("|")[0].strip() in labels:
            v = cells(x)
            assert n is None or len(v) >= n, (p, labels, v)
            CHECK.setdefault(p, []).append(x)
            return v, i
    raise AssertionError((p, labels, after))


def check_line(p, i, want):
    assert lines(p)[i] == want, (p, i, lines(p)[i], want)
    CHECK.setdefault(p, []).append(want)


def published(acc):
    """The acceptance-time rule: accepted at or after 16:00 ET, the next trading day; otherwise that day."""
    r = FILINGS[acc]
    t = dt.datetime.fromisoformat(r[1].replace("Z", "+00:00")).astimezone(ET)
    day = t.date().isoformat()
    if t.hour >= 16 or day not in TDAYS:
        day = next(d for d in TDAYS if d > day)
    assert PREV_CUT < r[0] <= CUT, acc
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
FANG_INC = "Diamondback Energy, Inc."
EARLIER = {v["source"]: v for v in f["history_vintages"] if "eps_normalized" in v}
V16 = EARLIER["FG10"]

# ── the 10-K vintages FY2017-FY2020 ─────────────────────────────────────────────────────────────────────────────────────────────────
# FY2017-FY2019: Item 6, five years (the FY2019 10-K in rounded millions); FY2020: Item 6 "[Reserved.]", so the statements of operations'
# three years. Each year from the latest filing that reports it; earlier years carried from the latest earlier vintage (ten years).
TENK = [("FG11", "0001539838-18-000014", "10-K__diamondback201710-k.rows.txt", 2017),
        ("FG12", "0001539838-19-000008", "10-K__diamondback201810-k.rows.txt", 2018),
        ("FG13", "0001539838-20-000021", "10-K__diamondback201910-k.rows.txt", 2019),
        ("FG14", "0001539838-21-000015", "10-K__fang-20201231.rows.txt", 2020)]
BUSINESS = ("We are an independent oil and natural gas company focused on the acquisition, development, exploration and exploitation of "
            "unconventional, onshore oil and natural gas reserves in the Permian Basin in West Texas.")
CYCLICAL = ("The oil and natural gas industry is cyclical, which can result in shortages of drilling rigs, equipment, raw materials "
            "(particularly sand and other proppants), supplies and personnel.")
PRICES = ("Our revenues, operating results, profitability, future rate of growth and the carrying value of our oil and natural gas "
          "properties depend significantly upon the prevailing prices for oil and natural gas.")
# the energy-transition words: the risk factor heading in the FY2017-FY2019 10-Ks; the FY2020 10-K drops it, and its Item 1 climate
# section's sentence (in every 10-K of the batch) is quoted instead
TRANSITION = {2017: "Regulation of greenhouse gas emissions could result in increased operating costs and reduced demand for the oil and natural gas we produce.",
              2020: "Restrictions on emissions of methane or carbon dioxide that may be imposed could adversely impact the demand for, price of, and value of our products and reserves."}
TRANSITION[2018] = TRANSITION[2019] = TRANSITION[2017]
CONSERVATION = "Conservation measures and technological advances could reduce demand for oil and natural gas."
FUEL = ("Fuel conservation measures, alternative fuel requirements, increasing consumer demand for alternatives to oil and natural gas, "
        "technological advances in fuel economy and energy generation devices could reduce demand for oil and natural gas.")
DIV_10K = {2017: "On February 13, 2018, we announced that we are initiating an annual cash dividend in the amount of $0.50 per share of our common stock payable quarterly beginning with the first quarter of 2018.",
           2018: "On February 13, 2018, we announced the initiation of an annual cash dividend in the amount of $0.50 per share of our common stock payable quarterly which began with the first quarter of 2018.",
           2019: "Additionally, beginning with the fourth quarter of 2019, the annual cash dividend was increased to $1.50 per share of our common stock",
           2020: "Although we have paid cash dividends on our common stock in the past, our board of directors may determine not to declare dividends in the future or may reduce the amount of dividends paid in the future."}
vintages, TENK_INFO = [], {}
for sid, acc, fname, fy in TENK:
    p = path(acc, fname)
    ls = lines(p)
    iso = next(i for i, x in enumerate(ls) if x == "Consolidated Statements of Operations" and i > 1000
               and ls[i + 1] == "Year Ended December 31,")
    check_line(p, iso + 2, f"{fy} | {fy - 1} | {fy - 2}")
    unit_m = ls[iso + 3].startswith("(In millions")
    k = 1.0 if unit_m else 1 / 1000
    if fy < 2020:
        i6 = max(i for i, x in enumerate(ls) if x == "ITEM 6. SELECTED FINANCIAL DATA")
        yrs = list(range(fy, fy - 5, -1))
        hdr = next(x for x in ls[i6:i6 + 8] if x.startswith(("(In thousands, except per share amounts) |",
                                                                "(In millions, except per share amounts, shares in thousands) |")))
        assert [int(c.strip()[:4]) for c in hdr.split("|")[1:]] == yrs, (sid, hdr)
        assert hdr.startswith("(In millions") == unit_m, sid
        CHECK.setdefault(p, []).append(hdr)
        s0, nrow = i6, 5
    else:
        assert "[Reserved.]" in lines(p)[max(i for i, x in enumerate(ls) if x == "ITEM 6. SELECTED FINANCIAL DATA") + 1]
        CHECK.setdefault(p, []).append("[Reserved.]")
        yrs = [fy, fy - 1, fy - 2]
        s0, nrow = iso, 3
    rev, _ = row(p, "Total revenues", start=s0, n=nrow)
    pti, _ = row(p, ("Income (loss) before income taxes", "Income before income taxes"), start=s0, n=nrow)
    tax, _ = row(p, ("Provision for (benefit from) income taxes", "Provision for income taxes"), start=s0, n=nrow)
    ni, _ = row(p, ("Net income (loss) attributable to Diamondback Energy, Inc.", "Net income attributable to Diamondback Energy, Inc."),
                start=s0, n=nrow)
    ie = next(i for i, x in enumerate(ls) if i > s0 and x in ("Earnings per common share", "Earnings per common share:",
                                                               "Earnings (loss) per common share:"))
    eps, _ = row(p, "Diluted", start=ie, n=nrow)
    iw = next(i for i, x in enumerate(ls) if i > s0 and x in ("Weighted average common shares outstanding",
                                                               "Weighted average common shares outstanding:"))
    sh, _ = row(p, "Diluted", start=iw, n=nrow)
    # the statement of operations' sales lines (this year and last) and the statement of cash flows
    def sales(lbl):
        v, _ = row(p, lbl, start=iso, stop=iso + 12, n=3)
        return [x * k for x in v[:2]]
    oil_s, gas_s, ngl_s = sales("Oil sales"), sales("Natural gas sales"), sales("Natural gas liquid sales")
    icf = next(i for i, x in enumerate(ls) if i > iso and x == "Consolidated Statements of Cash Flows")
    ocf, _ = row(p, ("Net cash provided by operating activities", "Net cash provided by (used in) operating activities"), start=icf, n=3)
    capex_l = (("Additions to oil and natural gas properties",) if fy < 2019 else
               ("Drilling, completions and non-operated additions to oil and natural gas properties",
                "Infrastructure additions to oil and natural gas properties"))
    capex = sum(row(p, lbl, start=icf, n=3)[0][0] for lbl in capex_l)
    quotes = {"business_quote": quote(p, BUSINESS), "cyclical_quote": quote(p, CYCLICAL), "prices_quote": quote(p, PRICES),
              "transition_quote": quote(p, TRANSITION[fy]), "conservation_quote": quote(p, CONSERVATION),
              "fuel_quote": quote(p, FUEL), "dividend_quote": quote(p, DIV_10K[fy])}
    for w in ("electric vehicle", "crypto", "blockchain", "bitcoin"):      # EV's and CRYPTO's own words: none in any 10-K of the batch
        assert w not in " ".join(ls).lower(), (sid, w)
    day, filed, _ = source(sid, acc, p, f"Diamondback FY{fy} 10-K",
                           (f"Item 6, Selected Financial Data, {fy - 4}-{fy}" if fy < 2020 else
                            f"the statements of operations, {fy - 2}-{fy} (Item 6 is reserved)")
                           + ": total revenues, income (loss) before income taxes, the provision for income taxes, net income (loss) "
                             "attributable to Diamondback, diluted EPS and diluted weighted average shares; the statements of operations "
                             "(oil, natural gas and natural gas liquid sales) and cash flows (net cash provided by operating activities, "
                             "additions to oil and natural gas properties); Items 1, 1A and 5")
    periods = {}
    for i, y in enumerate(yrs):
        periods[str(y)] = {"issuer": FANG_INC, "start": f"{y}-01-01", "end": f"{y}-12-31", "months": 12,
                           "revenue_m": round(rev[i] * k, 3), "pretax_m": round(pti[i] * k, 3), "net_income_m": round(ni[i] * k, 3),
                           "eps_diluted": eps[i], "eps_pro_forma": None, "diluted_shares_m": round(sh[i] / 1000, 3),
                           "tax_m": round(tax[i] * k, 3)}
    TENK_INFO[fy] = {"ocf_m": ocf[0] * k, "capex_m": capex * k, "groups": (oil_s, ngl_s, gas_s)}
    v = {"published": day, "source": sid, "kind": "10-K", "fy_label": f"FY{fy % 100:02d}", "periods": periods,
         "eps_basis": ("GAAP diluted EPS as " + ("Item 6" if fy < 2020 else "the statement of operations") + " prints it, on net income "
                       "(loss) attributable to Diamondback Energy, Inc. (no discontinued operations in the years shown)"),
         "units": "USD millions" if unit_m else "USD thousands", **quotes}
    vintages.append(v)
V = {fy: v for (_, _, _, fy), v in zip(TENK, vintages)}
assert [V[fy]["periods"][str(fy)]["eps_diluted"] for fy in V] == [4.94, 8.06, 1.47, -28.59]
for fy in V:                       # no 10-K of the batch restates an EPS of an earlier vintage
    for y, per in V[fy]["periods"].items():
        for v_ in [V16] + [V[g] for g in V if g < fy]:
            if y in v_["periods"] and v_["periods"][y]["eps_diluted"] is not None:
                assert v_["periods"][y]["eps_diluted"] == per["eps_diluted"], (fy, y)


# ── the prints: each release's statement of operations and selected operating data, three months against the year-ago quarter ────
PRINTS = [  # quarter, fy, q, accession, the year-ago column of the operating data
    ("Q4 2017", 2017, 4, "0001539838-18-000011", 1), ("Q1 2018", 2018, 1, "0001539838-18-000052", 2),
    ("Q2 2018", 2018, 2, "0001539838-18-000091", 2), ("Q3 2018", 2018, 3, "0001539838-18-000114", 2),
    ("Q4 2018", 2018, 4, "0001539838-19-000006", 1), ("Q1 2019", 2019, 1, "0001539838-19-000055", 2),
    ("Q2 2019", 2019, 2, "0001539838-19-000092", 2), ("Q3 2019", 2019, 3, "0001539838-19-000115", 2),
    ("Q4 2019", 2019, 4, "0001539838-20-000006", 1), ("Q1 2020", 2020, 1, "0001539838-20-000050", 2),
    ("Q2 2020", 2020, 2, "0001539838-20-000090", 2), ("Q3 2020", 2020, 3, "0001539838-20-000108", 2),
    ("Q4 2020", 2020, 4, "0001539838-21-000004", 1), ("Q1 2021", 2021, 1, "0001539838-21-000063", 1),
    ("Q2 2021", 2021, 2, "0001539838-21-000111", 2), ("Q3 2021", 2021, 3, "0001539838-21-000121", 2)]
PTI_L = ("Income before income taxes", "Income (loss) before income taxes", "(Loss) income before income taxes")
EPS_H = ("Earnings per common share:", "(Loss) earnings per common share:", "Earnings (loss) per common share:")
NEXT = {1: ("Q2", "early August"), 2: ("Q3", "early November"), 3: ("Q4", "February"), 4: ("Q1", "early May")}
# The one-off test (the AAPL FY2002 test and its mirror), on the items each Q4 release's adjusted net income table removes besides the
# non-cash marks (the derivative marks and, from 2018, the revaluation of investments: marks to market that recur, the NEE and PEP 2008
# core rule). Each item at its twelve-month amount where the release's statement of operations prints a line for it, else the table's own
# figure (the Q4 2017 and Q4 2020 tables are three months only). Charges and benefits are pre-tax against income before income taxes,
# except the FY2017 tax benefit, which has no pre-tax amount (the CHTR encoding).
ONE_OFFS = {
    2017: {"charges": [], "benefits": [("Gain on sale of assets, net ($69 pretax)", "table3", 0.069),
                                       ("Income tax benefit relating to change in statutory tax rate and change in valuation allowance", "table3_aftertax", None)],
           "marks": ['Noncash mark-to-market "MTM" derivative losses, net ($93,605 pretax)']},
    2018: {"charges": [("Merger & integration", "stmt", "Merger & integration expense")],
           "benefits": [("Other income", "table12", None)],
           "marks": ["Non-cash gain on derivative instruments", "Loss on revaluation of investments"]},
    2019: {"charges": [("Impairment of oil and natural gas properties", "stmt", "Impairment of oil and natural gas properties"),
                       ("Loss on extinguishment of debt", "stmt", "Loss on extinguishment of debt")],
           "benefits": [], "marks": ["Non-cash gain on derivative instruments", "Gain on revaluation of investments"]},
    2020: {"charges": [("Impairment of oil and natural gas properties", "stmt", "Impairment of oil and natural gas properties")],
           "benefits": [], "marks": ["Non-cash loss on derivative instruments, net"]},
}


def test_of(fy, pretax_m, charges_m, benefits_m, ni_m, eps, source_txt, items):
    loss = eps is not None and eps <= 0
    distorted = charges_m > pretax_m if charges_m >= benefits_m else benefits_m > pretax_m - benefits_m
    return {"fy": fy, "pretax_m": pretax_m, "listed_charges_m": charges_m, "listed_benefits_m": benefits_m,
            "income_attributable_m": ni_m, "eps_gaap": eps, "loss": loss, "distorted": bool(distorted and not loss),
            "kept": not loss and not distorted, "source": source_txt, "items": items}


prints = []
for k_, (quarter, fy, q, acc, yago) in enumerate(PRINTS):
    p = path(acc, "EX-99.1__*.rows.txt")
    ls = lines(p)
    iso = next(i for i, x in enumerate(ls) if x in ("Consolidated Statements of Operations", "Condensed Consolidated Statements of Operations"))
    u = ls[iso + 1]
    assert u.startswith("(unaudited"), (quarter, u)
    unit = 1.0 if "in millions" in u else 1 / 1000
    CHECK.setdefault(p, []).append(u)
    ncol = 4 if q > 1 else 2
    rev, _ = row(p, "Total revenues", start=iso, n=ncol)
    pti, _ = row(p, PTI_L, start=iso, n=ncol)
    ie = next(i for i in range(iso, iso + 60) if ls[i] in EPS_H)
    eps, _ = row(p, "Diluted", start=ie, n=ncol)
    iw = next(i for i in range(ie, ie + 6) if ls[i] == "Weighted average common shares outstanding:")
    sh, _ = row(p, "Diluted", start=iw, n=ncol)
    iop = next(i for i, x in enumerate(ls) if x == "Selected Operating Data")
    hdr = ls[iop + 2]
    assert hdr.startswith("Three Months Ended") and (("Year Ended" in hdr) == (q == 4)), (quarter, hdr)
    CHECK.setdefault(p, []).append(hdr)
    if yago == 2:
        assert hdr.count("Three Months Ended") == 3, (quarter, hdr)
    boe, _ = row(p, ("Oil Equivalents (MBOE)(1)(2)", "Combined volumes (MBOE)(1)(2)", "Combined volumes (MBOE)(1)"), start=iop, n=2)
    oil, _ = row(p, ("Oil (MBbl)", "Oil (MBbls)"), start=iop, n=2)
    loe, _ = row(p, ("Lease operating expense", "Lease operating expenses"), "Average Costs per BOE", start=iop, n=2)
    day, filed, when = source(f"FG{37 + k_}", acc, p, f"Diamondback {quarter} earnings release (8-K, exhibit 99.1)",
                              "Consolidated statements of operations (revenues, income before income taxes, diluted EPS and shares, three "
                              "months against the year-ago quarter) and selected operating data (oil and oil-equivalent production, lease "
                              "operating expense per BOE)" + ("; the twelve months and the adjusted net income table" if q == 4 else "")
                              + "; the dividend declaration")
    raw = {"rev_m": round(rev[0] * unit, 3), "rev_prior_m": round(rev[1] * unit, 3), "pti_m": round(pti[0] * unit, 3),
           "pti_prior_m": round(pti[1] * unit, 3), "eps_q": eps[0], "eps_q_prior": eps[1], "dil_sh_m": round(sh[0] / 1000, 3),
           "boe_k": boe[0], "boe_prior_k": boe[yago], "oil_k": oil[0], "oil_prior_k": oil[yago], "loe_boe": loe[0], "loe_boe_prior": loe[yago]}
    ptm, ptm_p = raw["pti_m"] / raw["rev_m"] * 100, raw["pti_prior_m"] / raw["rev_prior_m"] * 100
    nq, nmonth = NEXT[q]
    pr = {"quarter": quarter, "fy": fy, "q": q, "published": day, "source": f"FG{37 + k_}",
          "release": day, "release_time": f"accepted {filed}", "raw": raw, "sales_b": round(raw["rev_m"] / 1000, 4),
          "sales_pct": round(pct(raw["rev_prior_m"], raw["rev_m"]), 1),
          "production_pct": round(pct(raw["boe_prior_k"], raw["boe_k"]), 1), "oil_pct": round(pct(raw["oil_prior_k"], raw["oil_k"]), 1),
          "loe_boe_pct": round(pct(raw["loe_boe_prior"], raw["loe_boe"]), 1),
          "pretax_margin": round(ptm, 2), "pretax_margin_bp": round((ptm - ptm_p) * 100, 1),
          "next_print": f"{nq} {fy + (1 if q == 4 else 0)} release ({nmonth})"}
    if q == 4:   # the release's twelve months: the year joins the history from the release until the 10-K
        ni, _ = row(p, ("Net income (loss) attributable to Diamondback Energy, Inc.", "Net income attributable to Diamondback Energy, Inc."),
                    start=iso, n=4)
        spec = ONE_OFFS[fy]
        ia = next(i for i, x in enumerate(ls) if x == "Adjusted Net Income" and i > iso)
        th = ls[ia + 2]
        CHECK.setdefault(p, []).append(th)
        twelve = "Year Ended" in th
        items, ch, be = [], 0.0, 0.0
        for kind, lst in (("charge", spec["charges"]), ("benefit", spec["benefits"])):
            for lbl, how, arg in lst:
                if how == "stmt":            # the statement of operations' twelve-month line
                    v_, _ = row(p, arg, start=iso, n=4)
                    amt = abs(v_[2]) * unit
                    row(p, lbl, start=ia)    # and the table lists it
                elif how == "table12":
                    assert twelve, (quarter, "a twelve-month table")
                    v_, _ = row(p, lbl, start=ia)
                    amt = abs(v_[2]) * unit
                elif how == "table3":        # the table's own figure (three months; pre-tax amount in the label)
                    row(p, lbl, start=ia)
                    amt = arg
                else:                        # table3_aftertax: an after-tax tax item (no pre-tax amount)
                    v_, _ = row(p, lbl, start=ia)
                    amt = abs(v_[0]) * unit
                items.append({"item": lbl, "kind": kind, "usd_m": round(amt, 3),
                              "basis": {"stmt": "twelve months, statement of operations", "table12": "twelve months, adjusted net income table",
                                        "table3": "three months, adjusted net income table (pre-tax, in its label; no twelve-month figure)",
                                        "table3_aftertax": "three months, adjusted net income table, after tax (a tax item; no twelve-month figure)"}[how]})
                ch, be = (ch + amt, be) if kind == "charge" else (ch, be + amt)
        for m in spec["marks"]:
            row(p, m, start=ia)
            items.append({"item": m, "kind": "mark (recurring, left out)"})
        t = test_of(fy, round(pti[2] * unit, 3), round(ch, 3), round(be, 3), round(ni[2] * unit, 3), eps[2],
                    f"{quarter} release: the items its adjusted net income table removes besides the non-cash marks", items)
        pr["fy_actual"] = {"fy": fy, "eps_gaap": eps[2], "revenue_m": round(rev[2] * unit, 3), "diluted_shares_m": round(sh[2] / 1000, 3),
                           "pretax_m": round(pti[2] * unit, 3), "net_income_m": round(ni[2] * unit, 3), "one_off_test": t,
                           "revenue_usd_b": round(rev[2] * unit / 1000, 4), "pretax_margin": round(pti[2] / rev[2] * 100, 2),
                           "sales_growth": round(pct(rev[3], rev[2]), 1)}
    prints.append(pr)
P = {pr["quarter"]: pr for pr in prints}
for fy in (2017, 2018, 2019, 2020):              # the Q4 releases' years agree with the 10-Ks that follow them
    a, per = P[f"Q4 {fy}"]["fy_actual"], V[fy]["periods"][str(fy)]
    assert (a["eps_gaap"], round(a["revenue_m"]), round(a["pretax_m"])) == (per["eps_diluted"], round(per["revenue_m"]), round(per["pretax_m"])), (fy, a, per)
TESTS = {fy: P[f"Q4 {fy}"]["fy_actual"]["one_off_test"] for fy in (2017, 2018, 2019, 2020)}
assert [(TESTS[y]["kept"], TESTS[y]["loss"], TESTS[y]["distorted"]) for y in (2017, 2018, 2019, 2020)] == \
    [(True, False, False), (True, False, False), (False, False, True), (False, True, False)], TESTS
# the FY2017 10-K's own tax reconciliation (the year's figures behind the release's three-month item): kept on them too
p17 = path("0001539838-18-000014", "10-K__diamondback201710-k.rows.txt")
rate17, _ = row(p17, "Income tax benefit relating to change in statutory tax rate", n=3)
va17, _ = row(p17, "Change in valuation allowance", "A reconciliation of the statutory federal income tax amount", n=3)
tax_10k = round((-rate17[0] - va17[0]) / 1000, 3)
assert tax_10k < V[2017]["periods"]["2017"]["pretax_m"] - tax_10k
TESTS[2017]["tenk_check"] = {"tax_benefits_m": tax_10k, "kept": True,
                             "note": ("the FY2017 10-K's reconciliation of the statutory rate: 'Income tax benefit relating to change in "
                                      "statutory tax rate' $67.9M and 'Change in valuation allowance' $127.5M for the year; summed, under "
                                      "the year's income before income taxes less them, so the year is kept on them too")}
for fy in (2018, 2019, 2020):                    # each Q4 release's prior year agrees with the vintage public before it
    a = P[f"Q4 {fy}"]["fy_actual"]
    assert abs(a["sales_growth"] - pct(V[fy - 1]["periods"][str(fy - 1)]["revenue_m"], a["revenue_m"])) < 0.06, fy

EXCL = {"2012": V16["eps_excluded"]["2012"],
        "2015": "a GAAP loss, $(8.74) diluted, after the $814.8M full cost ceiling impairment; the company's adjusted net income ($1.81) "
                "also removes the non-cash derivative marks, which recur, so no figure excludes only the one-offs (the loss rule)",
        "2016": "a GAAP loss, $(2.20) diluted, after the $245.5M full cost ceiling impairment; the company's adjusted net income also "
                "removes the non-cash derivative marks, which recur, so no figure excludes only the one-offs (the loss rule)",
        "2019": "distorted: the $790M full cost ceiling impairment and the $56M loss on extinguishment of debt ($846M of listed one-off "
                "charges) exceed its $362M income before income taxes (the AAPL FY2002 test); the company's adjusted $6.93 also removes "
                "the non-cash derivative marks, which recur, so no figure excludes only the one-offs",
        "2020": "a GAAP loss, $(28.59) diluted, after $6,021M of full cost ceiling impairments; no figure excludes only the one-offs "
                "(the company's adjusted net income also removes the non-cash derivative marks; the loss rule)"}
assert EXCL["2015"] == V16["eps_excluded"]["2015"] and EXCL["2016"] == V16["eps_excluded"]["2016"]
ALL_TESTS = {**{int(y): t for y, t in V16["one_off_tests"].items()}, **TESTS}

# ── each vintage's model fields: ten fiscal years to the latest, each year from the latest filing public on the vintage's date ──────
chain = [V16] + [V[fy] for fy in sorted(V)]
for n_, fy in enumerate(sorted(V), start=1):
    v = V[fy]
    prev = chain[n_ - 1]
    rev, eps_k, shares, src = {}, {}, {}, {}
    for y, r in prev["revenue_usd_b"].items():
        rev[int(y)] = r; src[int(y)] = prev["source"]
    for y, e in prev["eps_normalized"].items():
        eps_k[int(y)] = e
    for y, s in prev["diluted_shares_m"].items():
        shares[int(y)] = s
    for y, per in v["periods"].items():
        y = int(y)
        rev[y] = round(per["revenue_m"] / 1000, 4); src[y] = v["source"]
        shares[y] = per["diluted_shares_m"]
        if ALL_TESTS[y]["kept"]:
            eps_k[y] = per["eps_diluted"]
        else:
            eps_k.pop(y, None)
    keep = lambda d: {str(y): d[y] for y in sorted(d) if y > fy - 10}
    per = v["periods"]
    last_kept = max(y for y in eps_k)
    lk = (per.get(str(last_kept)) or next(c["periods"][str(last_kept)] for c in reversed(chain[:n_]) if str(last_kept) in c["periods"]))
    carried = prev["source"]
    info = TENK_INFO[fy]
    (o, ng, g) = info["groups"]
    excl = {y: EXCL[y] for y in EXCL if int(y) <= fy}
    v.update({
        "eps_normalized": keep(eps_k),
        "eps_excluded": {y: t for y, t in excl.items() if int(y) > fy - 10},
        "revenue_usd_b": keep(rev),
        "diluted_shares_m": keep(shares),
        "normalization": ("GAAP diluted EPS on net income attributable to Diamondback; " + "; ".join(
            f"FY{y[2:]} excluded: {t}" for y, t in excl.items())),
        "revenue_note": (f"total revenues, each year from the latest filing that reports it ({min(y for y in rev if y > fy - 10)}-2011 the "
                         "Predecessors, 2012 combined, as the 10-Ks' selected financial data present them; "
                         + ("the FY2019 10-K's rounded millions from 2015" if fy == 2019 else
                            "2018-2020 from the FY2020 10-K's statements of operations, Item 6 being reserved" if fy == 2020 else
                            f"{fy - 4}-{fy} from this 10-K") + ")"),
        "shares_note": "diluted weighted average shares, M (2013 on; no GAAP share count before), each year from the latest filing",
        "carried_from": f"the years this 10-K does not report, from the {prev['fy_label']} vintage ({carried}), each from the latest filing that reported it",
        "prev_fy_pretax_margin": round(per[str(fy)]["pretax_m"] / per[str(fy)]["revenue_m"] * 100, 2),
        "check_year": last_kept,
        "check_pretax_margin": round(lk["pretax_m"] / lk["revenue_m"] * 100, 2),
        "tax_rate": round(lk["tax_m"] / lk["pretax_m"], 4),
        "prev_fy_sales_growth": round(pct(rev[fy - 1] * 1000, rev[fy] * 1000), 1),
        "groups": [["Oil sales", round(o[0] / 1000, 4), round(pct(o[1], o[0]), 1)],
                   ["Natural gas liquid sales", round(ng[0] / 1000, 4), round(pct(ng[1], ng[0]), 1)],
                   ["Natural gas sales", round(g[0] / 1000, 4), round(pct(g[1], g[0]), 1)]],
        "groups_basis": f"{fy} oil, natural gas liquid and natural gas sales (the statement of operations)",
        "fcf_b": round((info["ocf_m"] + info["capex_m"]) / 1000, 4),
        "fcf_note": (f"(net cash provided by operating activities ${info['ocf_m'] / 1000:.3f}B less additions to oil and natural gas "
                     f"properties ${-info['capex_m'] / 1000:.3f}B; acquisitions and midstream additions not deducted)"),
        "fcf_label": f"FY{fy % 100:02d}",
        "one_off_tests": {str(y): ALL_TESTS[y] for y in sorted(ALL_TESTS) if fy - 10 < y <= fy},
    })

# ── dividends: each annual rate from the release that first states it (the Q4 2018 release's "As previously announced" refers to no
# earlier filing: the January 2019 investor presentation was posted to the website, not filed) ─────────────────────────────────────────
DIVS = [("Q4 2017", 0.50, "Initiating annual cash dividend of $0.50 per common share to be payable quarterly beginning with Q1 2018"),
        ("Q4 2018", 0.75, "As previously announced, increasing annual cash dividend by 50% to $0.75 per common share to be payable quarterly beginning with Q1 2019 subject to Board approval"),
        ("Q4 2019", 1.50, "Approved a 100% increase in the annual cash dividend policy to $1.50 per common share starting with Q4 2019 payment, subject to discretion of the Board"),
        ("Q4 2020", 1.60, "Diamondback announced today that the Company's Board of Directors approved a 6.7% increase to the Company's annual dividend to $1.60 per share from $1.50 previously and declared a cash dividend of $0.40 per common share for the fourth quarter of 2020"),
        ("Q2 2021", 1.80, "Increasing annual dividend by 12.5% to $1.80 per share; declared Q2 2021 cash dividend of $0.45 per share"),
        ("Q3 2021", 2.00, "Increasing annual dividend by 11.1% to $2.00 per share; declared Q3 2021 cash dividend of $0.50 per share")]
dividends = []
for qq, annual, qt in DIVS:
    pr = P[qq]
    p = path(PRINTS[[x[0] for x in PRINTS].index(qq)][3], "EX-99.1__*.rows.txt")
    dividends.append({"published": pr["published"], "source": pr["source"], "annual": annual, "quarterly": round(annual / 4, 4),
                      "quote": quote(p, qt), "note": f"${annual:.2f} a year (${annual / 4:.4g} a quarter), the {qq} release"})
# each release's per-quarter declaration agrees with the rate in force
for qq, cents in (("Q1 2018", "Q1 2018 cash dividend of $0.125 per share"), ("Q1 2019", "18.75 cents per common share"),
                  ("Q1 2021", "declared a cash dividend of $0.40 per common share for the first quarter of 2021")):
    quote(path(PRINTS[[x[0] for x in PRINTS].index(qq)][3], "EX-99.1__*.rows.txt"), cents)

# ── write ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
f["history_vintages"] += vintages
f["prints"] += prints
f["dividends"] = dividends
f["amendments"] = f.get("amendments", []) + [{
    "published": published("0001539838-19-000030")[0], "accession": "0001539838-19-000030", "form": "10-K/A",
    "note": quote(path("0001539838-19-000030", "10-K_A__*.rows.txt"),
                  "is being filed solely to include a report of Ryder Scott Company, L.P., the Company’s independent oil and gas consultants (“Ryder Scott”), with respect to estimates of proved reserves, as of December 31, 2018, of Energen Corporation (“Energen”)")
            + " (FY2018 10-K/A: a reserve report only, not a vintage)"}]
f["_doc"] = (f["_doc"] + " | 2018-2021: extended by retro/generators/fang/gen_fang_1821.py with the FY2017-FY2020 10-K vintages, the "
             "prints Q4 2017-Q3 2021 with each Q4 release's year and its one-off test, and the dividend rates (retro/README.md, "
             "\"FANG 2018-2021\").")
new = json.loads(json.dumps(f))
old = json.loads(OLD_SNAPSHOT)
for kk in old:                                   # every earlier fact unchanged: only appended
    if isinstance(old[kk], list):
        assert new[kk][:len(old[kk])] == old[kk], kk
    elif isinstance(old[kk], dict):
        assert all(new[kk][x] == old[kk][x] for x in old[kk]), kk
    elif kk != "_doc":
        assert new[kk] == old[kk], kk
for s in f["sources"].values():
    assert s["published"] <= CUT
out = A.out or os.path.join(REPO, "retro", "facts", "FANG.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(f, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_fang_1821.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump({p: sorted(set(v)) for p, v in CHECK.items()}, fh, ensure_ascii=False, indent=1)
print(f"{out}: {len(vintages)} vintages, {len(prints)} prints, {len(dividends)} dividends; checklist {ck}: "
      f"{sum(len(set(v)) for v in CHECK.values())} strings")
for pr in prints:
    print(pr["quarter"], pr["published"], pr["release_time"], pr["sales_pct"], pr["production_pct"], pr["oil_pct"], pr["loe_boe_pct"],
          pr["pretax_margin"], pr["pretax_margin_bp"], pr["raw"]["eps_q"], pr["raw"]["eps_q_prior"], pr["raw"]["dil_sh_m"])
for fy, t in TESTS.items():
    print(fy, {k: t[k] for k in ("pretax_m", "listed_charges_m", "listed_benefits_m", "eps_gaap", "kept", "distorted", "loss")})
for v in vintages:
    print(v["source"], v["published"], v["eps_normalized"], list(v["eps_excluded"]), v["revenue_usd_b"], v["diluted_shares_m"],
          v["tax_rate"], v["check_year"], v["fcf_b"], v["prev_fy_sales_growth"])
for d in dividends:
    print(d["published"], d["annual"], d["source"])
