#!/usr/bin/env python3
"""Extend retro/facts/CHTR.json with 2014-2017 (filings accepted 2014-02-22 to 2017-12-31), asserting that every earlier fact is unchanged.

The discipline of the 2008-2013 sheet (gen_chtr.py; retro/README.md, "CHTR 2008-2009"): each figure from its own row by label under an
anchored heading, each quoted sentence asserted present in its own filing, every derived figure computed, and a verbatim checklist
written. The sheet still holds only what decides whether a date can be built under method r2: the 10-K vintages' Item 6 EPS history, the
Q4 releases' full-year EPS (public before their 10-K), the one-off test of the one positive year (FY2016), the listing record and the
Parent Merger's exchange ratio. No quarterly print, guide, signal or rule-T value is transcribed, because no date of 2014-2017 passes the
gate (retro/README.md, "CHTR 2014-2017"). Run (one CIK, 1091667, for Legacy Charter and, from the 2016-05-18 Parent Merger, the new
Charter Communications, Inc., which files under it):

    python3 retro/tools/edgar.py index 1091667 <dir>
    python3 retro/tools/edgar.py fetch 1091667 <dir> --from 2014-01-01 --to 2017-12-31 --forms 10-K 10-Q 8-K
    python3 -I retro/generators/chtr/gen_chtr_1417.py --filings <dir> [--facts-in <2008-2013 sheet>] [--out retro/facts/CHTR.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_chtr_1417.json

--facts-in is the 2008-2013 sheet (default retro/facts/CHTR.json, which must then hold no fact published after 2014-02-21; the generator
refuses a sheet that already holds one). It only appends.
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
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))       # retro/generators/chtr -> the repository
_ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("--filings", required=True, help="folder edgar.py wrote (allrows.json, tenk/, eightk/); keep it outside the repo")
_ap.add_argument("--facts-in", help="the 2008-2013 fact sheet to extend (default retro/facts/CHTR.json)")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/CHTR.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_chtr_1417.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402  (the repo's own tool: trading days from the Yahoo cache)

ET = ZoneInfo("America/New_York")
PREV_CUT, CUT = "2014-02-21", "2017-12-31"
CIK = 1091667
FILINGS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("^GSPC")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
CHECK = {}
TEXT = {}

IN = A.facts_in or os.path.join(REPO, "retro", "facts", "CHTR.json")
old = json.load(open(IN, encoding="utf-8"))
assert all(s["published"] <= PREV_CUT for s in old["sources"].values()), "the input sheet already holds a fact after 2014-02-21"
f = copy.deepcopy(old)


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
    """Assert a sentence is in its own filing and add it to the checklist."""
    assert norm(s) in norm(" ".join(lines(p))), (p, s[:120])
    CHECK.setdefault(p, []).append(s)
    return s


def num(c):
    c = c.strip().replace(",", "").replace("$", "")
    if c in ("--", "—"):
        return 0.0
    neg = c.startswith("(") and c.endswith(")")
    v = float(c.strip("()"))
    return -v if neg else v


def row(p, label, after=None, cols=None):
    """The first row whose first cell is `label` (after the line holding `after`), as numbers; the row goes on the checklist."""
    ls = lines(p)
    start = next(i for i, x in enumerate(ls) if after in x) if after else 0
    for x in ls[start:]:
        cells = [c.strip() for c in x.split("|")]
        if cells[0] == label:
            vals = [num(c) for c in cells[1:]]
            assert cols is None or len(vals) == cols, (p, label, vals)
            CHECK.setdefault(p, []).append(x)
            return vals
    raise AssertionError((p, label))


def published(acc):
    """The acceptance-time rule (edgar.py 'when'): accepted at or after 16:00 ET, the next trading day; otherwise that day."""
    r = FILINGS[acc]
    t = dt.datetime.fromisoformat(r[1].replace("Z", "+00:00")).astimezone(ET)
    day = t.date().isoformat()
    if t.hour >= 16 or day not in TDAYS:
        day = next(d for d in TDAYS if d > day)
    assert PREV_CUT < r[0] <= CUT, acc
    when = "after the close" if t.hour >= 16 else ("before the open" if (t.hour, t.minute) < (9, 30) else "during the session")
    return day, f"{t:%Y-%m-%d %H:%M} ET ({when})"


def url(acc, p):
    return f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc.replace('-', '')}/{os.path.basename(p).split('__', 1)[1].replace('.rows.txt', '')}"


def source(sid, acc, p, title, supports):
    assert sid not in f["sources"], sid
    day, filed = published(acc)
    f["sources"][sid] = {"published": day, "filed": filed, "accession": acc, "title": title, "url": url(acc, p), "supports": supports}
    return day


CCI = "Charter Communications, Inc."
Y = lambda y: (str(y), CCI, f"{y}-01-01", f"{y}-12-31", 12)
# The FY2014-FY2016 10-Ks print only the years after the 2009 emergence (2010 on) and name no Predecessor or Successor; the issuer is
# "Charter Communications, Inc." in each (from the FY2016 10-K the new Charter of the Parent Merger, which reports Legacy Charter's
# years as its own, the per-share figures recast for the Parent Merger Exchange Ratio). Every period these vintages hold is therefore
# a year of the shares the date prices ('priced_issuers').
VINTAGES = [
    ("CH15", "0001091667-15-000049", "10-K__chtr123114-10k.rows.txt", "Charter FY2014 10-K", "FY14",
     "2014 | 2013 | 2012 | 2011 | 2010", (2014, 2013, 2012, 2011, 2010),
     "Loss per common share, basic and diluted", "Weighted-average shares outstanding, basic and diluted", "Net loss"),
    ("CH16", "0001091667-16-000396", "10-K__chtr123115-10k.rows.txt", "Charter FY2015 10-K", "FY15",
     "2015 | 2014 | 2013 | 2012 | 2011", (2015, 2014, 2013, 2012, 2011),
     "Loss per common share, basic and diluted", "Weighted average shares outstanding, basic and diluted", "Net loss"),
    ("CH17", "0001091667-17-000030", "10-K__chtr123116-10k.rows.txt", "Charter FY2016 10-K", "FY16",
     "2016 | 2015 | 2014 | 2013 | 2012", (2016, 2015, 2014, 2013, 2012),
     "Income (loss) per common share, diluted", "Weighted average shares outstanding, diluted (a)",
     "Net income (loss) attributable to Charter shareholders"),
]
vintages = []
for sid, acc, fname, title, label, header, years, eps_l, sh_l, ni_l in VINTAGES:
    p = path(acc, fname)
    after = "Item 6. Selected Financial Data."
    i0 = next(i for i, x in enumerate(lines(p)) if x == after)
    assert header in lines(p)[i0:i0 + 6], (sid, "header")
    CHECK.setdefault(p, []).append(header)
    n = len(years)
    rev = row(p, "Revenues", after, n)
    eps = row(p, eps_l, after, n)
    sh = row(p, sh_l, after, n)
    ni = row(p, ni_l, after, n)
    periods = {}
    for i, y in enumerate(years):
        key, who, start, end, months = Y(y)
        periods[key] = {"issuer": who, "start": start, "end": end, "months": months, "revenue_m": rev[i], "eps_diluted": eps[i],
                        "eps_continuing": eps[i], "diluted_shares_m": round(sh[i] / 1e6, 3), "net_income_m": ni[i]}
    day = source(sid, acc, p, title, f"Item 6, Selected Financial Data: revenues, {ni_l.lower()}, diluted EPS ({eps_l!r}) and "
                 f"{sh_l.lower()} for {', '.join(str(y) for y in years)}")
    vintages.append({"published": day, "source": sid, "fy_label": label, "periods": periods, "priced_issuers": [CCI],
                     "eps_basis": "diluted EPS as the Item 6 table prints it (no discontinued operations in the years shown)"})
v16 = vintages[-1]
p16 = path("0001091667-17-000030", "10-K__chtr123116-10k.rows.txt")
v16["recast_quote"] = quote(p16, "Weighted average number of shares outstanding for all periods presented has been recast to reflect the "
                                 "application of the Parent Merger Exchange Ratio.")
# the FY2016 10-K's recast: 2012-2015 diluted EPS on the new basis (the FY2015 10-K's $(2.43) becomes $(2.68))
assert v16["periods"]["2015"]["eps_diluted"] == -2.68 and vintages[1]["periods"]["2015"]["eps_diluted"] == -2.43

# ── the one-off test of FY2016, the one positive year (the mirror of the AAPL FY2002 test; retro/README.md, method r2) ──────────
# the listed one-off: the reversal of Legacy Charter's valuation allowance, which the 10-K calls non-recurring
pretax = row(p16, "Income (loss) before income taxes", "The following table sets forth the consolidated statements of operations for the periods presented", 3)
tax = row(p16, "Income tax benefit (expense)", "The following table sets forth the consolidated statements of operations for the periods presented", 3)
nci = row(p16, "Less: Net income attributable to noncontrolling interests", "The following table sets forth the consolidated statements of operations for the periods presented", 3)
ni16 = row(p16, "Net income (loss) attributable to Charter shareholders", "The following table sets forth the consolidated statements of operations for the periods presented", 3)
assert (pretax[0], tax[0], nci[0], ni16[0]) == (820, 2925, -223, 3522) and pretax[0] + tax[0] + nci[0] == ni16[0]
va = row(p16, "Change in valuation allowance", "Income Tax Benefit (Expense)", 3)
oth = row(p16, "Merger and restructuring costs", "Other operating expenses, net. The changes", 2)
pen = row(p16, "Other pension benefits", "Other operating expenses, net. The changes", 2)
ext = row(p16, "Loss on extinguishment of debt", "The following table sets forth the consolidated statements of operations for the periods presented", 3)
BENEFIT_M = 3300     # "approximately $3.3 billion", as the 10-K and the Q4 2016 release state it
test16 = {
    "fy": 2016, "kind": "benefit",
    "income_attributable_m": ni16[0],
    "items_after_tax_m": BENEFIT_M,
    "income_without_m": ni16[0] - BENEFIT_M,
    "distorted": BENEFIT_M > ni16[0] - BENEFIT_M,
    "figure_without_published": None,
    "item": "the reversal of approximately $3.3 billion of Legacy Charter's valuation allowance on its deferred tax assets, recognized as "
            "an income tax benefit",
    "quote_nonrecurring": quote(p16, "absent non-recurring impacts such as the reversal of the income tax valuation allowance in the "
                                     "second quarter of 2016, we may incur net losses in the future."),
    "quote_amount": quote(p16, "As a result, Charter has reversed approximately $3.3 billion of its valuation allowance and recognized a "
                               "corresponding income tax benefit in the consolidated statements of operations for the year ended "
                               "December 31, 2016."),
    "note": (f"net income attributable to Charter shareholders ${ni16[0]:,.0f}M (income before income taxes ${pretax[0]:,.0f}M, income tax "
             f"benefit ${tax[0]:,.0f}M, noncontrolling interests ${-nci[0]:,.0f}M); without the ${BENEFIT_M:,}M valuation allowance reversal "
             f"${ni16[0] - BENEFIT_M:,.0f}M, so the listed benefit exceeds the year's income without it and reported EPS is more than "
             "double the EPS without it (the mirror of the AAPL FY2002 test); no filing publishes a figure excluding only it"),
    "readings": {   # the same test on the other readings of the 10-K's figures (display; each is met)
        "rate_reconciliation": {"items_after_tax_m": va[0], "income_without_m": ni16[0] - va[0], "distorted": va[0] > ni16[0] - va[0],
                                "note": "the tax note's change in valuation allowance"},
        "net_of_listed_charges": {"items_after_tax_m": BENEFIT_M + (-pen[0]) - oth[0] - (-ext[0]),
                                  "income_without_m": ni16[0] - (BENEFIT_M + (-pen[0]) - oth[0] - (-ext[0])),
                                  "distorted": (BENEFIT_M + (-pen[0]) - oth[0] - (-ext[0]))
                                  > ni16[0] - (BENEFIT_M + (-pen[0]) - oth[0] - (-ext[0])),
                                  "note": (f"the reversal plus the other pension benefits (${-pen[0]:,.0f}M) less the merger and restructuring "
                                           f"costs (${oth[0]:,.0f}M) and the loss on extinguishment of debt (${-ext[0]:,.0f}M), the pre-tax "
                                           "items taken whole, the CB FY2005 netting")}},
}
assert test16["distorted"] and all(r["distorted"] for r in test16["readings"].values())
v16["one_off_tests"] = {"2016": test16}

# ── the Q4 releases: each full year's EPS, public from the release (before its 10-K for FY2014 and FY2015) ─────────────────────
Q4 = [("CH18", "0001091667-15-000039", "EX-99.1__exhibit991earningsrelease1.rows.txt", "Charter Q4 2014 earnings release (8-K exhibit 99.1)",
       2014, "Diluted", "Net income (loss)"),
      ("CH19", "0001091667-16-000390", "EX-99.1__chtrexhibit991earningsrele.rows.txt", "Charter Q4 2015 earnings release (8-K exhibit 99.1)",
       2015, "LOSS PER COMMON SHARE, BASIC AND DILUTED", "Net loss"),
      ("CH20", "0001091667-17-000029", "EX-99.1__chtrexhibit991earningsrele.rows.txt", "Charter Q4 2016 earnings release (8-K exhibit 99.1)",
       2016, "Diluted", "Net income (loss) attributable to Charter shareholders")]
q4 = []
for sid, acc, fname, title, fy, eps_l, ni_l in Q4:
    p = path(acc, fname)
    ls = lines(p)
    # the addendum's first statement of operations is on the actual basis: three months and the year, this year and last
    s0 = next(i for i, x in enumerate(ls) if x == "Three Months Ended December 31, | Year Ended December 31,")
    assert ls[s0 - 2] == "UNAUDITED CONSOLIDATED STATEMENTS OF OPERATIONS AND OPERATING DATA", sid
    cells = lambda x: [num(c) for c in x.split("|")[1:] if not c.strip().endswith("%")]
    seg = ls[s0:s0 + 80]
    r_rev = next(x for x in seg if x.split("|")[0].strip() in ("Total Revenues", "Total Revenue"))
    r_eps = next(x for x in seg if x.split("|")[0].strip() == eps_l)
    r_ni = next(x for x in seg if x.split("|")[0].strip() == ni_l)
    for x in (ls[s0], r_rev, r_eps, r_ni):
        CHECK.setdefault(p, []).append(x)
    rev, eps, ni = cells(r_rev), cells(r_eps), cells(r_ni)
    assert len(rev) == len(eps) == len(ni) == 4, (sid, rev, eps, ni)
    day = source(sid, acc, p, title, f"the addendum's statement of operations (actual basis): FY{fy} revenues, {ni_l.lower()} and diluted EPS")
    q4.append({"published": day, "source": sid, "fy": fy,
               "period": {"issuer": CCI, "start": f"{fy}-01-01", "end": f"{fy}-12-31", "months": 12, "revenue_m": rev[2],
                          "eps_diluted": eps[2], "eps_continuing": eps[2], "net_income_m": ni[2]}})
# each Q4 release's year agrees with the 10-K that follows it
for a, v in zip(q4, vintages):
    vp = v["periods"][str(a["fy"])]
    assert (a["period"]["revenue_m"], a["period"]["eps_diluted"], a["period"]["net_income_m"]) == (vp["revenue_m"], vp["eps_diluted"],
                                                                                                    vp["net_income_m"]), a["source"]
p20 = path("0001091667-17-000029", "EX-99.1__chtrexhibit991earningsrele.rows.txt")
q4[-1]["one_off_test"] = {**{k: test16[k] for k in ("fy", "kind", "income_attributable_m", "items_after_tax_m", "income_without_m",
                                                      "distorted", "figure_without_published", "item")},
                          "quote_amount": quote(p20, "The increase in net income was primarily related to a $3.3 billion tax benefit "
                                                     "resulting from a reduction in Legacy Charter's preexisting valuation allowance on "
                                                     "deferred tax assets and higher income from operations as a result of the Transactions."),
                          "note": test16["note"]}
# the release's summary table: actual 2016 and 2015, then pro forma 2016 and 2015 (diluted EPS)
_pf = "Diluted | 15.94 | (2.68) | 3.91 | 0.58"
assert _pf in lines(p20)
CHECK.setdefault(p20, []).append(_pf)
PF_ROW = [num(c) for c in _pf.split("|")[1:]]
# the release's pro forma figure (the Transactions as of 2015-01-01): shown, never an anchor (pro forma figures are unused)
q4[-1]["pro_forma_note"] = {
    "eps_diluted_pro_forma": PF_ROW[2],
    "quote": quote(p20, "Pro forma net income per basic common share attributable to Charter shareholders totaled $3.97 for the year "
                        "ended December 31, 2016, compared to $0.59 during the same period last year."),
    "basis_quote": quote(p20, "Pro forma results reflect certain acquisitions of cable systems in 2016 as if they occurred as of the "
                              "earliest period presented."),
    "note": ("pro forma (Legacy TWC and Legacy Bright House as if acquired on 2015-01-01): not the company's figure excluding only "
             "one-offs, so unused (the CB, SCHW and LLY pro forma rule)")}

# ── the listing record and the Parent Merger ─────────────────────────────────────────────────────────────────────────────────────
lq = "Charter’s Class A common stock is listed on the NASDAQ Global Select Market under the symbol “CHTR.”"
for sid, fname in (("CH15", "10-K__chtr123114-10k.rows.txt"), ("CH16", "10-K__chtr123115-10k.rows.txt"), ("CH17", "10-K__chtr123116-10k.rows.txt")):
    acc = f["sources"][sid]["accession"]
    f["listings"].append({"published": f["sources"][sid]["published"], "source": sid, "issuer": CCI, "exchange": "NASDAQ Global Select Market",
                          "symbol": "CHTR", "quote": quote(path(acc, fname), lq)})
f["parent_merger"] = {
    "published": v16["published"], "source": "CH17", "effective": "2016-05-18",
    "exchange_ratio": 0.9042,
    "quote": quote(p16, "which was also the exchange ratio that was used to determine the number of shares of Charter Class A common stock "
                        "that Legacy Charter stockholders received per share of Legacy Charter Class A common stock."),
    "quote_ratio": quote(p16, "by 0.9042 (the “Parent Merger Exchange Ratio”)"),
    "note": ("each Legacy Charter Class A share became 0.9042 of a share of the new Charter's Class A common stock, still NASDAQ: CHTR; "
             "Yahoo's CHTR series records no split or other event for it, and the FY2016 10-K recasts every earlier per-share figure for "
             "the ratio. No date is built, so no encoding is chosen: a batch that builds a date whose P/E window holds days before "
             "2016-05-18 must decide one first (the splits and distributions rules)")}
f["no_dividend"].append({"published": v16["published"], "source": "CH17",
                         "quote": quote(p16, "Charter has not paid stock or cash dividends on any of its common stock.")})

f["history_vintages"] = sorted(f["history_vintages"] + vintages, key=lambda v: v["published"])
f["q4_actuals"] = q4
f["listings"] = sorted(f["listings"], key=lambda x: x["published"])
f["_doc"] = old["_doc"] + (" Extended with 2014-2017 by retro/generators/chtr/gen_chtr_1417.py: the FY2014-FY2016 10-K vintages, the Q4 "
                           "2014-2016 releases' full years ('q4_actuals'), the one-off test of FY2016 (the only positive year to 2016: "
                           "$15.94 diluted with the approximately $3.3 billion valuation allowance reversal, excluded by the mirror of the "
                           "AAPL FY2002 test), the listing and the Parent Merger's exchange ratio; still no print, guide, signal or rule-T "
                           "value, as no date of 2014-2017 passes the gate (retro/README.md, \"CHTR 2014-2017\").")
# every earlier fact unchanged
for k, v in old.items():
    if k in ("_doc", "sources", "history_vintages", "listings", "no_dividend"):
        continue
    assert f[k] == v, k
assert all(f["sources"][k] == v for k, v in old["sources"].items())
assert [v for v in f["history_vintages"] if v["published"] <= PREV_CUT] == old["history_vintages"]
assert [x for x in f["listings"] if x["published"] <= PREV_CUT] == old["listings"]
assert f["no_dividend"][:len(old["no_dividend"])] == old["no_dividend"]

out = A.out or os.path.join(REPO, "retro", "facts", "CHTR.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(f, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
cl = A.checklist or os.path.join(SP, "checklist_chtr_1417.json")
with open(cl, "w", encoding="utf-8") as fh:
    json.dump(CHECK, fh, indent=1, ensure_ascii=False)
print(f"{out}: {len(f['sources']) - len(old['sources'])} new sources, {len(vintages)} vintages, {len(q4)} Q4 actuals; checklist {cl}: "
      f"{sum(len(v) for v in CHECK.values())} strings")
