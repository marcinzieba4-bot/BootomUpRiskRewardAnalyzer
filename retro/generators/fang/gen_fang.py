#!/usr/bin/env python3
"""Generate retro/facts/FANG.json (the 2008-2013 setup) from Diamondback Energy, Inc.'s own filings (edgar.py's converted rows).

Every raw figure is read from its own row by label (the row is kept and checked), every quoted sentence is asserted present in its
own filing, and a verbatim checklist is written for retro/tools/verbatim.py. Only filings accepted on or before 2013-12-31 are read
(the last one is the FY2012 10-K/A of 2013-04-10). The fact sheet holds what decides whether a date can be built under method r2:
the annual history of each offering document and 10-K vintage (selected financial data, with the per-share figures each prints and
whether they are pro forma), the FY2012 "first day" tax charge, the listing record, the no-dividend statement and the price basis.
No print, guide or signal is transcribed: no date of 2008-2013 can be built (retro/README.md, "FANG 2008-2009"). Run (the
downloads, CIK 1539838):

    edgar.py index 1539838 <dir>
    edgar.py fetch 1539838 <dir> --from 2012-10-01 --to 2013-04-30 --acc 0001193125-12-419254 0001193125-12-420871 \
        0001193125-12-423496 0001193125-13-074801 0001539838-13-000004 0001539838-13-000013
    python3 -I retro/generators/fang/gen_fang.py --filings <dir> [--out retro/facts/FANG.json] [--checklist <dir>/checklist_fang.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_fang.json
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))       # retro/generators/fang -> the repository
_ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("--filings", required=True, help="folder edgar.py wrote (allrows.json, tenk/, eightk/, other/); keep it outside the repo")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/FANG.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_fang.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402  (the repo's own tool: trading days from the Yahoo cache)

ET = ZoneInfo("America/New_York")
CUT = "2013-12-31"
CIK = 1539838
FILINGS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("^GSPC")            # the trading calendar (Yahoo serves no FANG close before 2012-10-12)
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
CHECK = {}
TEXT = {}


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def path(acc, pattern):
    hits = [p for sub in ("tenk", "eightk", "other") for p in glob.glob(os.path.join(SP, sub, acc, pattern))]
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
    if c in ("--", "—"):          # a dash: none (the tables print it for a period without the item)
        return 0.0
    neg = c.startswith("(") and c.endswith(")")
    v = float(c.strip("()"))
    return -v if neg else v


def start_at(p, exact):
    """The index of the first line equal to `exact` (a section heading, not its table-of-contents entry)."""
    return next(i for i, x in enumerate(lines(p)) if x == exact)


def row(p, label, start=0, cols=None):
    """The first row from line `start` whose first cell is `label`, as numbers; the row goes on the checklist."""
    for x in lines(p)[start:]:
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
    assert r[0] <= CUT
    when = "after the close" if t.hour >= 16 else ("before the open" if (t.hour, t.minute) < (9, 30) else "during the session")
    return day, f"{t:%Y-%m-%d %H:%M} ET ({when})"


def url(acc, p):
    return f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc.replace('-', '')}/{os.path.basename(p).split('__', 1)[1].replace('.rows.txt', '')}"


SOURCES = {}


def source(sid, acc, p, title, supports):
    day, filed = published(acc)
    SOURCES[sid] = {"published": day, "filed": filed, "accession": acc, "title": title, "url": url(acc, p), "supports": supports}
    return day


WP = "Windsor Permian LLC"                               # the offering documents' issuer of record for 2007-2012 (an LLC: no shares)
PRED = "the Predecessors (Windsor Permian LLC and Windsor UT LLC)"
COMB = "Diamondback Energy, Inc. with the Predecessors to 2012-10-11 (combined)"

# ── the offering documents: Selected Historical Consolidated Financial Data (Windsor Permian LLC, the issuer's predecessor) ─────────
# columns: six months 2012, six months 2011, 2011, 2010, 2009, 2008, the period from inception (2007-10-23) to 2007-12-31
OFFER_COLS = [("2012-01-01..2012-06-30", "2012-01-01", "2012-06-30", 6), ("2011-01-01..2011-06-30", "2011-01-01", "2011-06-30", 6),
              ("2011", "2011-01-01", "2011-12-31", 12), ("2010", "2010-01-01", "2010-12-31", 12), ("2009", "2009-01-01", "2009-12-31", 12),
              ("2008", "2008-01-01", "2008-12-31", 12), ("2007-10-23..2007-12-31", "2007-10-23", "2007-12-31", 2)]
OFFERINGS = [("FG1", "0001193125-12-419254", "S-1_A__d295327ds1a.rows.txt", "Diamondback S-1/A, Amendment No. 6 (the last before the listing)",
              "S-1/A No. 6"),
             ("FG2", "0001193125-12-423496", "424B4__d295327d424b4.rows.txt", "Diamondback 424B4 prospectus", "424B4 prospectus")]
PF_EPS = "Pro forma income (loss) per common share — basic and diluted(2)"
PF_SH = "Weighted average pro forma shares outstanding — basic and diluted(2)"
vintages = []
for sid, acc, fname, title, label in OFFERINGS:
    p = path(acc, fname)
    s0 = start_at(p, "SELECTED HISTORICAL CONSOLIDATED FINANCIAL DATA")
    header = "2012 | 2011 | 2011 | 2010 | 2009 | 2008"
    assert header in lines(p)[s0:s0 + 6], (sid, "header")
    CHECK.setdefault(p, []).append(header)
    rev = row(p, "Oil and natural gas revenues", s0, 7)
    oth = row(p, "Other revenues", s0, 7)
    ni = row(p, "Net income (loss)", s0, 7)
    pf = row(p, PF_EPS, s0, 2)                            # the six months 2012 and 2011 only (the table's first and third columns)
    pfs = row(p, PF_SH, s0, 2)
    assert pf == [1.07, -0.04] and pfs == [14e6, 14e6], (sid, pf, pfs)
    periods = {}
    for i, (key, start, end, months) in enumerate(OFFER_COLS):
        periods[key] = {"issuer": WP, "start": start, "end": end, "months": months, "revenue_m": round((rev[i] + oth[i]) / 1e6, 3),
                        "net_income_m": round(ni[i] / 1e6, 3), "eps_diluted": None, "eps_pro_forma": None}
    periods["2012-01-01..2012-06-30"]["eps_pro_forma"] = pf[0]
    periods["2011"]["eps_pro_forma"] = pf[1]
    day = source(sid, acc, p, title, "Selected Historical Consolidated Financial Data: oil and natural gas revenues, other revenues, "
                 "net income (loss) and the pro forma income (loss) per common share and pro forma shares (six months 2012, 2011)")
    vintages.append({
        "published": day, "source": sid, "kind": "offering", "fy_label": label, "periods": periods,
        "eps_basis": ("no per-share figure for any period of the issuer's predecessor (a limited liability company with membership "
                      "interests, not shares); the only per-share figures are pro forma, as if the shares to be issued in the merger "
                      "had been outstanding"),
        "pro_forma_quote": quote(p, "The unaudited pro forma data presented gives effect to income taxes assuming that the Company "
                                    "operated as a taxable corporation throughout the periods presented."),
    })

# ── the FY2012 10-K: Item 6, Selected Financial Data (the Company with the Predecessors, combined under common control) ─────────────
K12 = "0001539838-13-000004"
pk = path(K12, "10-K__a12311210-k.rows.txt")
s6 = start_at(pk, "ITEM 6. SELECTED FINANCIAL DATA")
header = "2012(1) | 2011(2) | 2010(2) | 2009 | 2008"
assert lines(pk)[s6:s6 + 8].count(header) == 1, "header"
CHECK.setdefault(pk, []).append(header)
rev = row(pk, "Total revenues", s6, 5)
pretax = row(pk, "Income (loss) before income taxes", s6, 5)
ni = row(pk, "Net income (loss)", s6, 5)
spf = next(i for i, x in enumerate(lines(pk)) if i > s6 and x == "Pro forma earnings per common share(4)")
pf_dil = row(pk, "Diluted", spf, 1)[0]
pf_ni = row(pk, "Pro forma net income", s6, 1)[0]
sst = next(i for i, x in enumerate(lines(pk)) if x == "Pro forma weighted average common shares outstanding")
pf_sh = row(pk, "Diluted", sst, 1)[0]
charge = row(pk, "Deferred recognized at date of Merger - change in tax status of Predecessors", 0, 1)[0]
assert (pf_dil, pf_ni, pf_sh, charge, ni[0], pretax[0]) == (0.60, 11_829_000, 19_723_774, 54_142_000, -36_521_000, 18_382_000)
periods = {}
for i, y in enumerate((2012, 2011, 2010, 2009, 2008)):
    periods[str(y)] = {"issuer": COMB if y == 2012 else PRED, "start": f"{y}-01-01", "end": f"{y}-12-31", "months": 12,
                       "revenue_m": round(rev[i] / 1e6, 3), "pretax_m": round(pretax[i] / 1e6, 3), "net_income_m": round(ni[i] / 1e6, 3),
                       "eps_diluted": None, "eps_pro_forma": None}
periods["2012"]["eps_pro_forma"] = pf_dil
periods["2012"]["pro_forma_net_income_m"] = round(pf_ni / 1e6, 3)
periods["2012"]["pro_forma_diluted_shares_m"] = round(pf_sh / 1e6, 6)
day = source("FG3", K12, pk, "Diamondback FY2012 10-K", "Item 6, Selected Financial Data: total revenues, income (loss) before income "
             "taxes, net income (loss) and the pro forma diluted earnings per common share for 2008-2012; the statements' pro forma "
             "weighted average diluted shares; the income tax note's deferred tax recognized at the date of the Merger; Item 5 (the "
             "listing and the dividend policy); notes 1 and 7 (the Merger, the IPO, the first trading day)")
first_day = quote(pk, "On the date of the merger, a corresponding “first day” tax expense to net income from continuing operations was "
                      "recorded to establish a net deferred tax liability for differences between the tax and book basis of "
                      "Diamondback’s assets and liabilities. This charge was $54,142,000.")
vintages.append({
    "published": day, "source": "FG3", "kind": "10-K", "fy_label": "FY12", "periods": periods,
    "eps_basis": ("the statements of operations print net income (loss) and no GAAP earnings per share for any year; the only per-share "
                  "figure is 2012's unaudited pro forma earnings per common share (a pro forma income tax provision as if the Company "
                  "and the Predecessors had been subject to income taxes since 2011-12-31, on shares as if those issued upon the Merger "
                  "had been outstanding for the entire year)"),
    "pro_forma_quote": quote(pk, "The Company’s pro forma basic earnings per share amounts have been computed based on the "
                                 "weighted-average number of shares of common stock outstanding for the period, as if the common shares "
                                 "issued upon the Merger were outstanding for the entire year."),
    "one_offs_note": (f"2012: net loss ${-ni[0] / 1e6:,.3f}M after the ${charge / 1e6:,.3f}M first-day deferred tax charge of the Merger "
                      f"(the deferred income tax provision on the statement of operations), against ${pretax[0] / 1e6:,.3f}M of income "
                      "before income taxes: the charge exceeds the year's income before it (the AAPL FY2002 test), and no filing "
                      "publishes a per-share figure excluding only it (the pro forma figure also replaces it with a full year's "
                      "hypothetical tax and an as-if share count)"),
    "first_day_quote": first_day,
    "llc_quote": quote(pk, "The operations of Windsor Permian and Windsor UT, as limited liability companies, were not subject to federal "
                           "income taxes."),
})

# the FY2012 10-K/A: Part III only (no figure changes, so not a vintage)
pka = path("0001539838-13-000013", "10-K_A__a12311210-ka.rows.txt")
source("FG5", "0001539838-13-000013", pka, "Diamondback FY2012 10-K/A (Amendment No. 1)", "Part III only; no financial statement changes")
amend_quote = quote(pka, "to incorporate information previously omitted from Part III, Items 10, 11, 12, 13 and 14 and to amend and "
                         "restate the Exhibit Index.")

# the Q4 2012 release: prints no per-share figure for any period
pr = path("0001193125-13-074801", "EX-99.1__d491219dex991.rows.txt")
source("FG4", "0001193125-13-074801", pr, "Diamondback Q4 2012 release (8-K of 2013-02-25, exhibit 99.1)",
       "the fourth quarter and full year 2012 results; no per-share earnings figure for any period")
assert not any(re.search(r"(earnings|income|loss) per (common |diluted )?share", x, re.I) for x in lines(pr))
q4_quote = quote(pr, "The Company’s pro forma net loss after the non-cash income tax charge to earnings for Q4 2012 and full year 2012 "
                     "was a ($51.4) million loss and a ($29.8) million loss, respectively.")

# ── the listing record ──────────────────────────────────────────────────────────────────────────────────────────────────────────
listings = []
p1 = path("0001193125-12-419254", "S-1_A__d295327ds1a.rows.txt")
listings.append({"published": SOURCES["FG1"]["published"], "source": "FG1", "kind": "offering", "issuer": "Diamondback Energy, Inc.",
                 "quote": quote(p1, "This is the initial public offering of our common stock. Prior to this offering, there has been no "
                                    "public market for our common stock.")})
p8 = path("0001193125-12-420871", "8-A12B__d423586d8a12b.rows.txt")
day = source("FG6", "0001193125-12-420871", p8, "Diamondback Form 8-A12B of 2012-10-11", "the registration of the common stock on NASDAQ")
listings.append({"published": day, "source": "FG6", "kind": "registration", "issuer": "Diamondback Energy, Inc.",
                 "quote": quote(p8, "Common Stock, par value $0.01 per share | The NASDAQ Stock Market LLC")})
p2 = path("0001193125-12-423496", "424B4__d295327d424b4.rows.txt")
listings.append({"published": SOURCES["FG2"]["published"], "source": "FG2", "kind": "offering", "issuer": "Diamondback Energy, Inc.",
                 "quote": quote(p2, "We have been approved to list our common stock on The NASDAQ Global Select Market under the symbol “FANG.”")})
listings.append({"published": SOURCES["FG3"]["published"], "source": "FG3", "kind": "listing", "issuer": "Diamondback Energy, Inc.",
                 "exchange": "NASDAQ Global Select Market", "symbol": "FANG", "effective": "2012-10-12",
                 "quote": quote(pk, "As of June 30, 2012, the last business day of the registrant’s most recently completed second fiscal "
                                    "quarter, there was no public market for the registrant’s common stock. The registrant’s common stock "
                                    "began trading on the NASDAQ Global Select Market on October 12, 2012."),
                 "quote_note7": quote(pk, "On October 11, 2012, the Company priced 12,500,000 shares of common stock in the IPO at $17.50 per "
                                          "share, and on October 12, 2012, shares of the Company’s common stock began trading on the Nasdaq "
                                          "Global Select Market under the symbol “FANG”.")})

facts = {
    "_doc": ("Point-in-time fact sheet for FANG (Diamondback Energy, Inc., CIK 1539838), generated by retro/generators/fang/gen_fang.py "
             "from the filings; every value is tied to a source and becomes visible only on or after its 'published' date (EDGAR's "
             "acceptance time in ET: accepted at or after 16:00, the next trading day). It holds what decides whether a date can be built "
             "under method r2, and nothing else: each offering document's and 10-K's annual history, the FY2012 first-day tax charge, "
             "the listing record, the no-dividend statement and the price basis. No share of Diamondback traded before 2012-10-12; the "
             "predecessors were limited liability companies with no shares, and no filing to 2013-12-31 prints a GAAP earnings per share "
             "for any full year (2012's only per-share figure is pro forma), so no date of 2008-2013 has a full year of the company's own "
             "EPS to anchor a P/E and none is built (retro/README.md, \"FANG 2008-2009\"). No print, guide, signal or theme event is "
             "transcribed, and the builder refuses any date that passes the gate until they are."),
    "ticker": "FANG",
    "company": "Diamondback Energy, Inc.",
    "price_basis": ("Yahoo's FANG series is Diamondback Energy, Inc.'s common stock (NASDAQ: FANG) from its first point, 2012-10-12 "
                    "(firstTradeDate), the first trading day the FY2012 10-K states; Yahoo's series records no split. No share of the issuer or its predecessors traded before it (the predecessors were limited liability "
                    "companies controlled by Wexford Capital LP)."),
    "series_start": "2012-10-12",
    "sources": SOURCES,
    "history_vintages": sorted(vintages, key=lambda v: v["published"]),
    "listings": sorted(listings, key=lambda x: x["published"]),
    "no_dividend": [{"published": SOURCES["FG3"]["published"], "source": "FG3",
                     "quote": quote(pk, "We have not paid any cash dividends since our inception.")}],
    "release_notes": [{"published": SOURCES["FG4"]["published"], "source": "FG4", "quote": q4_quote,
                       "note": "the Q4 2012 release prints no per-share earnings figure for any period"}],
    "amendments": [{"published": SOURCES["FG5"]["published"], "source": "FG5", "quote": amend_quote,
                    "note": "Part III only: not a vintage (no figure the gate reads changes)"}],
    "prints": [], "guides": [], "dividends": [], "events": [], "company_names": [], "splits": [],
}
out = A.out or os.path.join(REPO, "retro", "facts", "FANG.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(facts, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
cl = A.checklist or os.path.join(SP, "checklist_fang.json")
with open(cl, "w", encoding="utf-8") as fh:
    json.dump(CHECK, fh, indent=1, ensure_ascii=False)
print(f"{out}: {len(SOURCES)} sources, {len(vintages)} vintages, {len(listings)} listing facts; checklist {cl}: "
      f"{sum(len(v) for v in CHECK.values())} strings")
