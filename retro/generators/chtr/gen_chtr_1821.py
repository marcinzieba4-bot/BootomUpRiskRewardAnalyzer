#!/usr/bin/env python3
"""Extend retro/facts/CHTR.json with 2018-2021 (filings accepted 2017-12-30 to 2021-12-31), asserting that every earlier fact is unchanged.

The discipline of the earlier sheets (gen_chtr.py, gen_chtr_1417.py; retro/README.md, "CHTR 2018-2021"): each figure from its own row by
label under an anchored heading, each quoted sentence asserted present in its own filing, every derived figure (growth, margin, one-off
test, rule-T value) computed, and a verbatim checklist written. This batch is the first whose dates pass the gate: FY2017 ($34.09 with
the approximately $9.3 billion Tax Reform benefit) is excluded by the mirror of the AAPL FY2002 test, and FY2018 ($5.22 GAAP, published
with the Q4 2018 release and the FY2018 10-K on the morning of 2019-01-31) is the first full year that anchors a P/E. So the sheet now
holds what a model needs: the FY2017-FY2020 10-K vintages (gate periods and model fields), the Q4 2017 release's year (inert: its 10-K
came the same morning), the prints Q3 2018 to Q3 2021 (Q3 2018 only as the previous print of the first date), the 10-Ks' streaming
words, and the rule-T values of the decade of the FY2018 10-K (the vintage public on the first date), the Successor's years only. Run:

    python3 retro/tools/edgar.py index 1091667 <dir>
    python3 retro/tools/edgar.py fetch 1091667 <dir> --from 2010-02-01 --to 2021-12-31 --forms 10-K
    python3 retro/tools/edgar.py fetch 1091667 <dir> --from 2018-01-01 --to 2021-12-31 --forms 8-K 8-K/A
    python3 -I retro/generators/chtr/gen_chtr_1821.py --filings <dir> [--facts-in <2008-2017 sheet>] [--out retro/facts/CHTR.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_chtr_1821.json

--facts-in is the 2008-2017 sheet (default retro/facts/CHTR.json, which must then hold no fact published after 2017-12-29). It only appends.
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
_ap.add_argument("--facts-in", help="the 2008-2017 fact sheet to extend (default retro/facts/CHTR.json)")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/CHTR.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_chtr_1821.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402

ET = ZoneInfo("America/New_York")
PREV_CUT, CUT = "2017-12-29", "2021-12-31"
CIK = 1091667
FILINGS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("^GSPC")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
CHECK, TEXT = {}, {}
IN = A.facts_in or os.path.join(REPO, "retro", "facts", "CHTR.json")
old = json.load(open(IN, encoding="utf-8"))
assert all(s["published"] <= PREV_CUT for s in old["sources"].values()), "the input sheet already holds a fact after 2017-12-29"
f = copy.deepcopy(old)
CCI = "Charter Communications, Inc."


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
    c = c.strip().replace(",", "").replace("$", "")
    if c in ("--", "—", "-"):
        return 0.0
    neg = c.startswith("(") and c.endswith(")")
    return -float(c.strip("()")) if neg else float(c.strip("()"))


def cells(x):
    """A row's numeric cells, the percentage-change cells and the open-parenthesis halves of '(12.3 | )%' left out."""
    out = []
    for c in x.split("|")[1:]:
        c = c.strip()
        if not c or c.endswith("%") or c in (")", ")%", "NM", "ppts", ") ppts") or c.startswith("(") and not c.endswith(")"):
            continue
        out.append(num(c))
    return out


def row(p, label, after=None, n=None, start=0):
    """The first row whose first cell is `label` (after the first line containing `after`), as numbers; it goes on the checklist."""
    ls = lines(p)
    i0 = next(i for i, x in enumerate(ls) if i >= start and after in x) if after else start
    for i in range(i0, len(ls)):
        x = ls[i]
        if x.split("|")[0].strip() == label:
            v = cells(x)
            assert n is None or len(v) >= n, (p, label, v)
            CHECK.setdefault(p, []).append(x)
            return v, i
    raise AssertionError((p, label, after))


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


# ── the 10-K vintages FY2017-FY2020 (Item 6, five years each; every period a year of the priced shares) ─────────────────────────────
TENK = [("CH21", "0001091667-18-000025", "10-K__chtr12312017-10k.rows.txt", "Charter FY2017 10-K", 2017),
        ("CH23", "0001091667-19-000029", "10-K__chtr12312018-10k.rows.txt", "Charter FY2018 10-K", 2018),
        ("CH25", "0001091667-20-000024", "10-K__chtr12312019-10k.rows.txt", "Charter FY2019 10-K", 2019),
        ("CH27", "0001091667-21-000022", "10-K__chtr-20201231.rows.txt", "Charter FY2020 10-K", 2020)]
ITEM6 = "Item 6. Selected Financial Data."
vintages, P10K = [], {}
for sid, acc, fname, title, fy in TENK:
    p = path(acc, fname)
    P10K[fy] = p
    ls = lines(p)
    i6 = max(i for i, x in enumerate(ls) if x == ITEM6)          # the Item 6 heading itself, not the table of contents
    years = tuple(range(fy, fy - 5, -1))
    header = " | ".join(str(y) for y in years)
    assert header in ls[i6:i6 + 6], (sid, "Item 6 header")
    CHECK.setdefault(p, []).append(header)
    eps_l = "Income (loss) per common share, diluted" if fy <= 2018 else "Income per common share, diluted"
    if fy == 2020:
        eps_l = "Earnings (loss) per common share attributable to Charter shareholders, diluted" if any(
            x.startswith("Earnings (loss) per common share attributable to Charter shareholders, diluted") for x in ls[i6:i6 + 40]) else eps_l
    eps_l = next(x.split("|")[0].strip() for x in ls[i6:i6 + 40] if x.split("|")[0].strip().endswith("diluted")
                 and "per common share" in x.split("|")[0] and "Weighted" not in x)
    sh_l = next(x.split("|")[0].strip() for x in ls[i6:i6 + 40] if x.startswith("Weighted average shares outstanding, diluted"))
    ni_l = next(x.split("|")[0].strip() for x in ls[i6:i6 + 40] if x.startswith("Net income") and "Charter shareholders" in x)
    io_l = next(x.split("|")[0].strip() for x in ls[i6:i6 + 40] if x.startswith("Income from operations"))
    rev, _ = row(p, "Revenues", ITEM6, 5, start=i6)
    io, _ = row(p, io_l, ITEM6, 5, start=i6)
    eps, _ = row(p, eps_l, ITEM6, 5, start=i6)
    sh, _ = row(p, sh_l, ITEM6, 5, start=i6)
    ni, _ = row(p, ni_l, ITEM6, 5, start=i6)
    pti_l = next((x.split("|")[0].strip() for x in ls[i6:i6 + 40] if x.startswith("Income (loss) before income taxes")
                  or x.startswith("Income before income taxes")), None)
    pti = row(p, pti_l, ITEM6, 5, start=i6)[0] if pti_l else None
    periods = {}
    for i, y in enumerate(years):
        periods[str(y)] = {"issuer": CCI, "start": f"{y}-01-01", "end": f"{y}-12-31", "months": 12, "revenue_m": rev[i],
                           "eps_diluted": eps[i], "eps_continuing": eps[i], "diluted_shares_m": round(sh[i] / 1e6, 3),
                           "net_income_m": ni[i], "income_from_operations_m": io[i]}
        if pti:
            periods[str(y)]["pretax_income_m"] = pti[i]
    day, filed, _ = source(sid, acc, p, title, f"Item 6, Selected Financial Data: revenues, income from operations, net income attributable "
                           f"to Charter shareholders, diluted EPS ({eps_l!r}) and diluted weighted average shares for "
                           f"{', '.join(str(y) for y in years)}; the statements, the MD&A's revenues by service offering, Items 1 and 1A")
    vintages.append({"published": day, "source": sid, "fy_label": f"FY{fy % 100:02d}", "periods": periods, "priced_issuers": [CCI],
                     "eps_basis": "diluted EPS as the Item 6 table prints it (no discontinued operations in the years shown)"})
V = {fy: v for (_, _, _, _, fy), v in zip(TENK, vintages)}

# ── the one-off tests (the AAPL FY2002 test and its mirror; method r2) ──────────────────────────────────────────────────────────────
p17 = P10K[2017]
ni17 = V[2017]["periods"]["2017"]["net_income_m"]
assert ni17 == 9895
TAX_REFORM_M = 9300   # "approximately $9.3 billion", as the FY2017 10-K and the Q4 2017 release state it
test17 = {
    "fy": 2017, "kind": "benefit", "income_attributable_m": ni17, "items_after_tax_m": TAX_REFORM_M,
    "income_without_m": ni17 - TAX_REFORM_M, "distorted": TAX_REFORM_M > ni17 - TAX_REFORM_M, "figure_without_published": None,
    "item": "the remeasurement of the net deferred tax liabilities at the 21% rate of the Tax Cuts & Jobs Act (Tax Reform), an income tax "
            "benefit of approximately $9.3 billion",
    "quote_amount": quote(p17, "The change in tax law required us to remeasure existing net deferred tax liabilities using the lower rate in "
                               "the period of enactment resulting in an income tax benefit of approximately $9.3 billion to reflect these "
                               "changes in the year ended December 31, 2017."),
    "note": (f"net income attributable to Charter shareholders ${ni17:,.0f}M; without the ${TAX_REFORM_M:,}M Tax Reform benefit "
             f"${ni17 - TAX_REFORM_M:,.0f}M, so the listed benefit exceeds the year's income without it and reported EPS is more than double "
             "the EPS without it (the mirror of the AAPL FY2002 test); no filing publishes a figure excluding only it"),
}
assert test17["distorted"]
# FY2016's test carries into every later vintage that still prints the year (the FY2016 10-K's figures; the test is unchanged)
test16 = old["history_vintages"][-1]["one_off_tests"]["2016"]


def listed_items(p, fy, anchor):
    """The statement of operations' items outside income from operations' recurring lines, each pre-tax and taken whole (the CB FY2005
    netting): other operating expenses, net, loss on extinguishment of debt, gain (loss) on financial instruments, other pension benefits
    (costs) and other expense, net; returned as (net charges, gross charges, rows) for the year `fy` (the first column)."""
    items = {}
    for lab in ("Other operating expenses, net", "Loss on extinguishment of debt", "Gain (loss) on financial instruments, net",
                "Other pension benefits", "Other pension benefits (costs), net", "Other expense, net", "Other income (expense), net",
                "Other expenses, net"):
        try:
            v, _ = row(p, lab, anchor)
        except AssertionError:
            continue
        sign = -1 if lab.startswith("Other operating") else 1      # an operating expense row is printed positive
        items[lab] = sign * v[0]
    return items


tests = {}
for fy in (2018, 2019, 2020):
    p = P10K[fy]
    anchor = "Consolidated Statements of Operations" if fy == 2018 else "Results of Operations"
    anc = next(x for x in lines(p) if "The following table sets forth the consolidated statements of operations for the periods presented" in x)
    items = listed_items(p, fy, anc)
    ni = V[fy]["periods"][str(fy)]["net_income_m"]
    net = -sum(items.values())                     # net charges (positive) or net benefits (negative), pre-tax
    gross_ch = -sum(v for v in items.values() if v < 0)
    gross_be = sum(v for v in items.values() if v > 0)
    tests[str(fy)] = {"fy": fy, "kind": "charges" if net > 0 else "benefits", "income_attributable_m": ni, "items_pre_tax_m": items,
                      "net_charges_m": net, "gross_charges_m": gross_ch, "gross_benefits_m": gross_be,
                      "distorted": gross_ch > ni or gross_be > ni - gross_be, "figure_without_published": None,
                      "note": (f"the listed items outside operations, each pre-tax and whole: {', '.join(f'{k} {v:+,.0f}' for k, v in items.items())} "
                               f"($M); charges ${gross_ch:,.0f}M against net income attributable of ${ni:,.0f}M (the AAPL FY2002 test), "
                               f"benefits ${gross_be:,.0f}M against ${ni - gross_be:,.0f}M without them (its mirror): neither is met, so the "
                               "year is kept at GAAP")}
    assert not tests[str(fy)]["distorted"], fy
V[2017]["one_off_tests"] = {"2016": test16, "2017": test17}
V[2018]["one_off_tests"] = {"2016": test16, "2017": test17, "2018": tests["2018"]}
V[2019]["one_off_tests"] = {"2016": test16, "2017": test17, "2018": tests["2018"], "2019": tests["2019"]}
V[2020]["one_off_tests"] = {"2016": test16, "2017": test17, "2018": tests["2018"], "2019": tests["2019"], "2020": tests["2020"]}

# ── the Q4 2017 release's year (the same morning as its 10-K: inert, recorded for the vintage rule) ──────────────────────────────────
pq17 = path("0001091667-18-000024", "EX-99.1__chtrexhibit991earningsrele.rows.txt")
ls = lines(pq17)
s0 = next(i for i, x in enumerate(ls) if x == "Three Months Ended December 31, | Year Ended December 31,")
assert ls[s0 - 2] == "UNAUDITED CONSOLIDATED STATEMENTS OF OPERATIONS AND OPERATING DATA"
r_rev, _ = row(pq17, "Total Revenue", start=s0)
r_eps, _ = row(pq17, "Diluted", start=s0)
r_ni, _ = row(pq17, "Net income attributable to Charter shareholders", start=s0)
day, filed, _ = source("CH22", "0001091667-18-000024", pq17, "Charter Q4 2017 earnings release (8-K exhibit 99.1)",
                       "the addendum's statement of operations (actual basis): FY2017 revenues, net income attributable to Charter shareholders "
                       "and diluted EPS; the Tax Reform benefit")
q4_17 = {"published": day, "source": "CH22", "fy": 2017,
         "period": {"issuer": CCI, "start": "2017-01-01", "end": "2017-12-31", "months": 12, "revenue_m": r_rev[2], "eps_diluted": r_eps[2],
                    "eps_continuing": r_eps[2], "net_income_m": r_ni[2]},
         "one_off_test": {**{k: test17[k] for k in ("fy", "kind", "income_attributable_m", "items_after_tax_m", "income_without_m",
                                                     "distorted", "figure_without_published", "item")},
                          "quote_amount": quote(pq17, "The increase was primarily driven by a non-cash GAAP3 tax benefit of $9.3 billion from a "
                                                      "reduction in the deferred tax liability as a result of the enactment of the Tax Cuts and "
                                                      "Jobs Act (\"Federal tax reform\") by Congress in December, which reduced the Federal tax "
                                                      "rate from 35% to 21%."),
                          "note": test17["note"]}}
vp = V[2017]["periods"]["2017"]
assert (q4_17["period"]["revenue_m"], q4_17["period"]["eps_diluted"], q4_17["period"]["net_income_m"]) == (vp["revenue_m"], vp["eps_diluted"],
                                                                                                         vp["net_income_m"])
assert q4_17["published"] == V[2017]["published"]   # the same morning: the release extends no vintage

# ── the prints, Q3 2018 to Q3 2021 (the earnings releases, 8-K exhibit 99.1) ─────────────────────────────────────────────────────────
PRINTS = [("CH30", "0001091667-18-000102", 2018, 3), ("CH31", "0001091667-19-000027", 2018, 4), ("CH32", "0001091667-19-000083", 2019, 1),
          ("CH33", "0001091667-19-000096", 2019, 2), ("CH34", "0001091667-19-000111", 2019, 3), ("CH35", "0001091667-20-000023", 2019, 4),
          ("CH36", "0001091667-20-000103", 2020, 1), ("CH37", "0001091667-20-000159", 2020, 2), ("CH38", "0001091667-20-000194", 2020, 3),
          ("CH39", "0001091667-21-000020", 2020, 4), ("CH40", "0001091667-21-000082", 2021, 1), ("CH41", "0001091667-21-000132", 2021, 2),
          ("CH42", "0001091667-21-000161", 2021, 3)]
QEND = {1: "March 31", 2: "June 30", 3: "September 30", 4: "December 31"}
QWORD = {1: "first", 2: "second", 3: "third", 4: "fourth"}
pct = lambda a, b: round((b / a - 1) * 100, 2)
mg = lambda x, rev: round(x / rev * 100, 2)
prints = []
for sid, acc, fy, q in PRINTS:
    p = path(acc, "EX-99.1__*.rows.txt")
    ls = lines(p)
    # the statement of operations (actual basis): three months this year and last, then the year-to-date columns
    s0 = next(i for i, x in enumerate(ls) if x == "UNAUDITED CONSOLIDATED STATEMENTS OF OPERATIONS AND OPERATING DATA"
              or x == "UNAUDITED CONSOLIDATED STATEMENTS OF OPERATIONS")
    hdr = next(x for x in ls[s0:s0 + 6] if x.startswith(f"Three Months Ended {QEND[q]},"))
    CHECK.setdefault(p, []).append(hdr)
    rev, _ = row(p, "Total Revenue", start=s0)
    ebitda, _ = row(p, "Adjusted EBITDA", start=s0)
    oi, _ = row(p, "Income from operations", start=s0)
    pti, _ = row(p, "Income before income taxes", start=s0)
    eps, _ = row(p, "Diluted", start=s0)
    sh, _ = row(p, "Weighted average common shares outstanding, diluted", start=s0)
    c0 = next(i for i, x in enumerate(ls) if x == "CASH FLOWS FROM INVESTING ACTIVITIES:")
    capex, _ = row(p, "Purchases of property, plant and equipment", start=c0)
    cfo, _ = row(p, "Net cash flows from operating activities", start=c0 - 40)
    # the customer table: the first 'Total Customer Relationships' after the key operating results' column header (this quarter's end,
    # then the year-ago quarter's, as the release shows it)
    k0 = next(i for i, x in enumerate(ls) if x == "Key Operating Results")
    kh = next(x for x in ls[k0:k0 + 4] if x.startswith(f"{QEND[q]}, {fy}"))
    cols = [re.sub(r"( \([a-z]\))+$", "", c.strip().replace(")(", ") (")) for c in kh.split("|")]
    assert cols[0] == f"{QEND[q]}, {fy}" and cols[1] == f"{QEND[q]}, {fy - 1}", (sid, kh)
    CHECK.setdefault(p, []).append(kh)
    rel, _ = row(p, "Total Customer Relationships", start=k0)
    # the release's own sentence on share repurchases in the quarter (display)
    bb = next(x for x in ls[:k0] if "Charter purchased approximately" in x)
    bb_s = re.search(r"(During the [a-z]+ quarter(?: of 20\d\d)?, Charter purchased approximately .*?for approximately \$[0-9.]+ (?:billion|million))", bb)
    assert bb_s, (sid, bb[:200])
    bb_s = quote(p, bb_s.group(1))
    day, filed, when = source(sid, acc, p, f"Charter Q{q} {fy} earnings release (8-K exhibit 99.1)",
                              f"Q{q} {fy} against Q{q} {fy - 1}: total revenue, Adjusted EBITDA, income from operations, income before income "
                              "taxes, diluted EPS and shares (statement of operations), purchases of property, plant and equipment (statement of "
                              "cash flows), total customer relationships (key operating results)")
    raw = {"rev_m": rev[0], "rev_prior_m": rev[1], "ebitda_m": ebitda[0], "ebitda_prior_m": ebitda[1], "oi_m": oi[0], "oi_prior_m": oi[1],
           "pti_m": pti[0], "pti_prior_m": pti[1], "capex_m": -capex[0], "capex_prior_m": -capex[1], "cfo_m": cfo[0],
           "rel_k": rel[0], "rel_prior_k": rel[1], "eps_q": eps[0], "eps_q_prior": eps[1], "dil_sh_m": round(sh[0] / 1e6, 3)}
    pr = {"quarter": f"Q{q} {fy}", "fy": fy, "q": q, "published": day, "source": sid, "release": day, "release_time": filed, "raw": raw,
          "sales_b": round(rev[0] / 1000, 3), "sales_pct": pct(rev[1], rev[0]), "rel_pct": pct(rel[1], rel[0]),
          "ocf_margin": mg(ebitda[0], rev[0]), "ocf_margin_bp": round((mg(ebitda[0], rev[0]) - mg(ebitda[1], rev[1])) * 100, 1),
          "op_margin": mg(oi[0], rev[0]), "op_margin_bp": round((mg(oi[0], rev[0]) - mg(oi[1], rev[1])) * 100, 1),
          "capex_pct": mg(-capex[0], rev[0]), "capex_bp": round((mg(-capex[0], rev[0]) - mg(-capex[1], rev[1])) * 100, 1),
          "eps_q": eps[0], "eps_q_prior": eps[1], "diluted_shares_m": round(sh[0] / 1e6, 3), "cash_note": bb_s,
          "next_print": f"Q{q % 4 + 1} {fy + (1 if q == 4 else 0)} print"}
    # capital expenditure outlooks in words (display only: no revenue, EPS or margin guide; the CMCSA capex-guide rule)
    cx = [s for s in re.findall(r"Charter currently expects [^.]*(?:\.\d[^.]*)*\.", " ".join(ls)) if "capital expenditures" in s]
    if cx:
        pr["capex_outlook"] = quote(p, cx[0])
    prints.append(pr)

# ── the 10-K model fields: margins, tax rate, cash flow, revenue lines, customer relationships, the durability and streaming words ──
MODEL = {}
for sid, acc, fname, title, fy in TENK[1:]:
    p = P10K[fy]
    ls = lines(p)
    v = V[fy]
    anc = next(x for x in ls if "The following table sets forth the consolidated statements of operations for the periods presented" in x)
    pti, _ = row(p, "Income before income taxes", anc)
    tax_l = "Income tax benefit (expense)" if fy == 2018 else "Income tax expense"
    tax, _ = row(p, tax_l, anc)
    cfo, _ = row(p, "Net cash flows from operating activities", "CONSOLIDATED STATEMENTS OF CASH FLOWS")
    ppe, _ = row(p, "Purchases of property, plant and equipment", "CONSOLIDATED STATEMENTS OF CASH FLOWS")
    cash, _ = row(p, "Cash and cash equivalents", "CONSOLIDATED BALANCE SHEETS")
    y = v["periods"][str(fy)]
    rev_y, rev_p = y["revenue_m"], v["periods"][str(fy - 1)]["revenue_m"]
    # revenues by service offering (the MD&A table): the residential and commercial lines, advertising, mobile and other
    m0 = next(i for i, x in enumerate(ls) if x.startswith("Revenues by service offering were as follows"))
    groups = []
    for lab in ("Residential revenue", "Small and medium business", "Enterprise", "Advertising sales", "Mobile", "Other"):
        g, _ = row(p, lab, start=m0)
        groups.append([lab.replace(" revenue", ""), round(g[0] / 1000, 3), round((g[0] / g[1] - 1) * 100, 1) if g[1] else None])
    assert abs(sum(g[1] for g in groups) * 1000 - rev_y) < 1.5, (fy, "the revenue lines sum to the year's revenues")
    # Item 1's customer table: total customer relationships at this year-end and the last
    rel, _ = row(p, "Total Customer Relationships", "Customer Relationships")
    desc = next(x for x in ls if x.startswith("We are the second largest cable operator") or x.startswith("We are a leading broadband"))
    desc = quote(p, desc.split(". ")[0] + ".")
    cyc = quote(p, "Our business is subject to seasonal and cyclical variations.")
    cyc2 = quote(p, "Our revenue is subject to cyclical advertising patterns and changes in viewership levels.")
    sv = [s for s in re.findall(r"As the proliferation of online video services grows, however, [^.]*\.", " ".join(ls))]
    risk = quote(p, sv[0])
    own = quote(p, "Historically, we have generally viewed SVOD online video services as complementary to our own video offering, and we have "
                   + ("developed a cloud-based guide that is capable of incorporating video from many online video services currently offered in the "
                      "marketplace." if fy == 2018 else "developed a cloud-based guide that is capable of incorporating video from online video "
                                                         "services currently offered in the marketplace."))
    nodiv = quote(p, "Charter has not paid cash dividends on its common stock and does not intend to do so in the foreseeable future.")
    MODEL[fy] = {
        "pretax_margin": mg(pti[0], rev_y), "tax_rate": round(tax[0] * -1 / pti[0], 4), "op_margin": mg(y["income_from_operations_m"], rev_y),
        "sales_growth": round((rev_y / rev_p - 1) * 100, 1), "fcf_b": round((cfo[0] + ppe[0]) / 1000, 3), "cash_b": round(cash[0] / 1000, 3),
        "cfo_m": cfo[0], "ppe_m": -ppe[0], "groups": groups, "rel_k": rel[0], "rel_prior_k": rel[1], "rel_pct": pct(rel[1], rel[0]),
        "business_quote": desc, "cyclical_quote": cyc, "cyclical_quote2": cyc2, "streaming_risk_quote": risk, "own_offering_quote": own,
        "no_dividend_quote": nodiv}
    v["model"] = MODEL[fy]

# ── rule T: the decade of the FY2018 10-K (the vintage public on the first buildable date, 2019-02-01), the Successor's years ──────────
# each change from the latest 10-K published by 2019-02-01 that reports both years (the F and BKR 2019 rule; the Successor's years
# only, from 2010, the BKR 2018 rule, so the first change is 2011's); a measure the filings tabulate for fewer years takes the changes
# they give (the AVGO rule): total customer relationships are tabulated from the FY2015 10-K (the FY2013-FY2014 10-Ks give residential
# and commercial relationships with no total; no sum is formed)
OLD10K = {2011: ("CH11", "0001091667-12-000026", "10-K__chtr12312011-10k.rows.txt"), 2012: ("CH12", "0001091667-13-000020", "10-K__chtr123112-10k.rows.txt"),
          2013: ("CH13", "0001091667-14-000080", "10-K__chtr123113-10k.rows.txt"), 2014: ("CH15", "0001091667-15-000049", "10-K__chtr123114-10k.rows.txt"),
          2015: ("CH16", "0001091667-16-000396", "10-K__chtr123115-10k.rows.txt"), 2016: ("CH17", "0001091667-17-000030", "10-K__chtr123116-10k.rows.txt"),
          2017: ("CH21", "0001091667-18-000025", "10-K__chtr12312017-10k.rows.txt"), 2018: ("CH23", "0001091667-19-000029", "10-K__chtr12312018-10k.rows.txt")}
K = {fy: path(acc, fn) for fy, (_, acc, fn) in OLD10K.items()}
SRC = {fy: sid for fy, (sid, _, _) in OLD10K.items()}
for fy in OLD10K:
    if SRC[fy] in old["sources"]:
        assert old["sources"][SRC[fy]]["accession"] == OLD10K[fy][1], fy


def item6(fy):
    """{year: (revenues, income from operations)} from the 10-K's Item 6 (five years; the FY2011-FY2013 tables also print the 2009 periods)."""
    p = K[fy]
    ls = lines(p)
    i6 = max(i for i, x in enumerate(ls) if x.startswith("Item 6. Selected Financial Data"))
    if fy >= 2014:
        years = list(range(fy, fy - 5, -1))
        hdr = " | ".join(str(y) for y in years)
        assert hdr in ls[i6:i6 + 6], fy
        CHECK.setdefault(p, []).append(hdr)
        rev, _ = row(p, "Revenues", start=i6)
        io_l = next(x.split("|")[0].strip() for x in ls[i6:i6 + 30] if x.startswith("Income from operations"))
        io, _ = row(p, io_l, start=i6)
        return {y: (rev[i], io[i]) for i, y in enumerate(years)}
    raise AssertionError(fy)


def mdna(fy):
    """{year: (revenues, Adjusted EBITDA)} from the MD&A's Adjusted EBITDA table and the statement of operations (three years)."""
    p = K[fy]
    ls = lines(p)
    years = list(range(fy, fy - 3, -1))
    hdr = " | ".join(str(y) for y in years)
    # the statement of operations' revenues (three years, the Successor's: FY2011 prints 2011, 2010 and the Successor's December 2009)
    s0 = next(i for i, x in enumerate(ls) if x == "CONSOLIDATED STATEMENTS OF OPERATIONS")
    assert ls[s0 + 3] == hdr, (fy, "the statement's three years")
    CHECK.setdefault(p, []).append(hdr)
    rev, _ = row(p, "REVENUES", start=s0)
    a0 = next(i for i, x in enumerate(ls) if x.startswith("Adjusted EBITDA is defined as"))
    eb, ie = row(p, "Adjusted EBITDA", start=a0)
    hh = next(x for x in reversed(ls[a0:ie]) if re.fullmatch(r"\d{4}( \| \d{4})+", x))
    assert hh.startswith(hdr), (fy, hh)
    CHECK.setdefault(p, []).append(hh)
    return {y: (rev[i], eb[i]) for i, y in enumerate(years)}, s0


def cashflow(fy):
    """{year: (revenues, purchases of property, plant and equipment)} from the statements of operations and cash flows (three years)."""
    p = K[fy]
    ls = lines(p)
    years = list(range(fy, fy - 3, -1))
    _, s0 = mdna(fy)
    rev, _ = row(p, "REVENUES", start=s0)
    c0 = next(i for i, x in enumerate(ls) if x.startswith("CONSOLIDATED STATEMENTS OF CASH FLOWS") and i > s0)
    ppe, _ = row(p, "Purchases of property, plant and equipment", start=c0)
    return {y: (rev[i], -ppe[i]) for i, y in enumerate(years)}


def latest_with(y, fn, fys):
    """The latest of the 10-Ks `fys` (published by 2019-02-01) whose table `fn` reports years y-1 and y."""
    for fy in sorted(fys, reverse=True):
        t = fn(fy)
        if y in t and y - 1 in t:
            return fy, t
    raise AssertionError(y)


RT = {"relationships": {"unit": 1, "lower_is_better": False, "values": {}, "sources": {}},
      "revenue": {"unit": 1, "lower_is_better": False, "values": {}, "sources": {}},
      "ocf_margin": {"unit": 10, "lower_is_better": False, "values": {}, "sources": {}},
      "capex": {"unit": 10, "lower_is_better": True, "values": {}, "sources": {}},
      "op_margin": {"unit": 10, "lower_is_better": False, "values": {}, "sources": {}}}
for y in range(2011, 2019):
    fy, t = latest_with(y, item6, [x for x in OLD10K if x >= 2014])
    RT["revenue"]["values"][str(y)] = pct(t[y - 1][0], t[y][0])
    RT["revenue"]["sources"][str(y)] = f"{SRC[fy]}: revenues {t[y - 1][0]:,.0f} -> {t[y][0]:,.0f}"
    RT["op_margin"]["values"][str(y)] = round((mg(t[y][1], t[y][0]) - mg(t[y - 1][1], t[y - 1][0])) * 100, 1)
    RT["op_margin"]["sources"][str(y)] = (f"{SRC[fy]}: income from operations {t[y - 1][1]:,.0f} / {t[y - 1][0]:,.0f} -> "
                                          f"{t[y][1]:,.0f} / {t[y][0]:,.0f}")
    fy, t = latest_with(y, lambda x: mdna(x)[0], list(OLD10K))
    RT["ocf_margin"]["values"][str(y)] = round((mg(t[y][1], t[y][0]) - mg(t[y - 1][1], t[y - 1][0])) * 100, 1)
    RT["ocf_margin"]["sources"][str(y)] = f"{SRC[fy]}: Adjusted EBITDA {t[y - 1][1]:,.0f} / {t[y - 1][0]:,.0f} -> {t[y][1]:,.0f} / {t[y][0]:,.0f}"
    fy, t = latest_with(y, cashflow, list(OLD10K))
    RT["capex"]["values"][str(y)] = round((mg(t[y][1], t[y][0]) - mg(t[y - 1][1], t[y - 1][0])) * 100, 1)
    RT["capex"]["sources"][str(y)] = (f"{SRC[fy]}: purchases of property, plant and equipment {t[y - 1][1]:,.0f} / {t[y - 1][0]:,.0f} -> "
                                      f"{t[y][1]:,.0f} / {t[y][0]:,.0f}")
for fy in (2015, 2016, 2017, 2018):
    p = K[fy]
    r, _ = row(p, "Total Customer Relationships", "Customer Relationships")
    RT["relationships"]["values"][str(fy)] = pct(r[1], r[0])
    RT["relationships"]["sources"][str(fy)] = f"{SRC[fy]}: Item 1 total customer relationships {r[1]:,.0f}K -> {r[0]:,.0f}K"


def rule_t(rt):
    unit, lower = rt["unit"], rt["lower_is_better"]
    v = sorted(rt["values"].values())
    n = len(v)
    med = v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
    worst, best = (v[-1], v[0]) if lower else (v[0], v[-1])
    r = lambda x: math.floor(x / unit + 0.5) * unit
    return {"BEAR": r(worst + (worst - med)), "BASE": r(worst), "BULL": r(med), "XBULL": r(best)}


for k in RT:
    RT[k]["thresholds"] = rule_t(RT[k])
f["rule_t"] = {**RT, "_doc": ("Rule T over the decade of the FY2018 10-K (2009-2018), the vintage public on 2019-02-01, the first buildable date: "
                              "the Successor's years only (2010 on), so the changes are 2011-2018; each from the latest 10-K published by then that "
                              "reports both years, as reported (the Transactions of 2016 in, as published). Values in % (relationships, revenue) "
                              "and bp (the margins and capital intensity, lower is better). XBULL = best year, BULL = median, BASE = worst year, "
                              "BEAR = one median-to-worst step beyond the worst; rounded half up to whole percent and to 10 bp.")}

# ── the streaming words of each 10-K (STREAMING, live from 2015-08-04: company-acknowledged, the CMCSA encoding) ────────────────────
events = []
for sid, acc, fname, title, fy in TENK[1:]:
    m = MODEL[fy]
    events.append({"id": f"{sid}-STREAM", "published": V[fy]["published"], "source": sid, "kind": "streaming_company_acknowledged",
                   "theme": "STREAMING", "doc": f"FY{fy} 10-K", "risk_quote": m["streaming_risk_quote"],
                   "risk_short": m["streaming_risk_quote"].split("however, ")[1].rstrip("."),
                   "offering": "the same 10-K says it has " + m["own_offering_quote"].split("and we have ")[1].rstrip(".")
                               + ", having viewed SVOD online video services as complementary to its own video offering",
                   "offering_short": "a cloud-based guide incorporating online video services"})

lq = "Charter’s Class A common stock is listed on the NASDAQ Global Select Market under the symbol “CHTR.”"
for sid, acc, fname, title, fy in TENK:
    f["listings"].append({"published": V[fy]["published"], "source": sid, "issuer": CCI, "exchange": "NASDAQ Global Select Market",
                          "symbol": "CHTR", "quote": quote(P10K[fy], lq)})
f["history_vintages"] = sorted(f["history_vintages"] + vintages, key=lambda v: v["published"])
f["q4_actuals"] = f["q4_actuals"] + [q4_17]
f["prints"] = prints
f["events"] = events
f["no_dividend"] += [{"published": V[fy]["published"], "source": sid, "quote": MODEL[fy]["no_dividend_quote"]} for sid, _, _, _, fy in TENK[1:]]
f["history_start"] = {"fy": 2018, "published": V[2018]["published"],
                      "note": ("FY2017 is a distorted year with no figure excluding only its one-off benefit; once FY2018 is in the history it is "
                               "not the latest year, so the history and the P/E window start after it (method r2, 'A distorted year with no "
                               "published adjusted figure': the ACN FY02, AAPL FY2002 and CMCSA 2003 rule), at 2018 and 2018-01-01")}
f["_doc"] = old["_doc"] + (" Extended with 2018-2021 by retro/generators/chtr/gen_chtr_1821.py: the FY2017-FY2020 10-K vintages with their "
                           "one-off tests (FY2017's $34.09 with the approximately $9.3 billion Tax Reform benefit excluded by the mirror test; "
                           "FY2018-FY2020 kept at GAAP), the Q4 2017 release's year (inert), the prints Q3 2018-Q3 2021, the 10-Ks' streaming "
                           "words and rule T over the FY2018 10-K's decade (the Successor's 2011-2018 changes); the first buildable date is "
                           "2019-02-01 (retro/README.md, \"CHTR 2018-2021\").")
for k, v in old.items():
    if k in ("_doc", "sources", "history_vintages", "no_dividend", "q4_actuals", "prints", "events", "listings"):
        continue
    assert f[k] == v, k
assert old["prints"] == [] and old["events"] == []
assert all(f["sources"][k] == v for k, v in old["sources"].items())
assert [v for v in f["history_vintages"] if v["published"] <= PREV_CUT] == old["history_vintages"]
assert f["q4_actuals"][:len(old["q4_actuals"])] == old["q4_actuals"]
assert f["no_dividend"][:len(old["no_dividend"])] == old["no_dividend"]
assert f["listings"][:len(old["listings"])] == old["listings"]
out = A.out or os.path.join(REPO, "retro", "facts", "CHTR.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(f, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
cl = A.checklist or os.path.join(SP, "checklist_chtr_1821.json")
with open(cl, "w", encoding="utf-8") as fh:
    json.dump(CHECK, fh, indent=1, ensure_ascii=False)
print(f"{out}: {len(f['sources']) - len(old['sources'])} new sources, {len(vintages)} vintages, {len(prints)} prints; checklist {cl}: "
      f"{sum(len(v) for v in CHECK.values())} strings")
for k, v in RT.items():
    print(f"  rule T {k:<14} {v['values']} -> {v['thresholds']}")
for p in prints:
    print(f"  {p['quarter']} {p['published']} {p['release_time']}: rev {p['sales_pct']:+.2f}% rel {p['rel_pct']:+.2f}% ocf {p['ocf_margin_bp']:+.1f}bp "
          f"capex {p['capex_bp']:+.1f}bp op {p['op_margin_bp']:+.1f}bp eps {p['eps_q']} vs {p['eps_q_prior']}")
