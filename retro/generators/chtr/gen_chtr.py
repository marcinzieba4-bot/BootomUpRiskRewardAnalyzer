#!/usr/bin/env python3
"""Generate retro/facts/CHTR.json (the 2008-2013 setup) from Charter Communications, Inc.'s own filings (edgar.py's converted rows).

Every raw figure is read from its own row by label (the row is kept and checked), every quoted sentence is asserted present in its
own filing, and a verbatim checklist is written for retro/tools/verbatim.py. Only filings accepted on or before 2014-02-21 (the FY2013
10-K) are read. The fact sheet holds what decides whether a date can be built under method r2: the annual EPS history of each 10-K
vintage (selected financial data), the listing record of the Class A common stock and the price basis. No print, guide or signal is
transcribed: no date of 2008-2013 can be built (retro/README.md, "CHTR 2008-2009"). Run (the downloads, CIK 1091667, one CIK for
the Predecessor and the Successor):

    edgar.py index 1091667 <dir>
    edgar.py fetch 1091667 <dir> --from 2004-01-01 --to 2014-03-31 --acc 0000950137-04-001876 0001091667-07-000015 0001091667-08-000004 \
        0001091667-09-000038 0001091667-10-000019 0001091667-11-000029 0001091667-12-000026 0001091667-13-000020 \
        0001091667-14-000080 0001091667-08-000083 0001091667-09-000054 0001354457-09-000102 0001091667-09-000201 0001091667-10-000170
    python3 -I retro/generators/chtr/gen_chtr.py --filings <dir> [--out retro/facts/CHTR.json] [--checklist <dir>/checklist_chtr.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_chtr.json
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
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))       # retro/generators/chtr -> the repository
_ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("--filings", required=True, help="folder edgar.py wrote (allrows.json, tenk/, eightk/, other/); keep it outside the repo")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/CHTR.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_chtr.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402  (the repo's own tool: trading days from the Yahoo cache)

ET = ZoneInfo("America/New_York")
CUT = "2014-02-21"
CIK = 1091667
FILINGS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("^GSPC")            # the trading calendar (Yahoo serves no CHTR close before 2010-01-05)
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
CHECK = {}


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


TEXT = {}


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
    if c in ("--", "—"):          # a dash: none (the statements print it for a period without the item)
        return 0.0
    neg = c.startswith("(") and c.endswith(")")
    v = float(c.strip("()"))
    return -v if neg else v


def row(p, label, after=None, cols=None):
    """The first row whose first cell is `label` (after the line holding `after`), as numbers; the row goes on the checklist."""
    ls = lines(p)
    start = 0
    if after:
        start = next(i for i, x in enumerate(ls) if after in x)
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


# ── the 10-K vintages: Item 6, Selected Financial Data (one basis per vintage, as published) ─────────────────────────────────────
# columns: (key, issuer, start, end, months); the Predecessor's 2009 is eleven months, the Successor's first period one month
P11 = ("2009-01-01..2009-11-30", "Predecessor", "2009-01-01", "2009-11-30", 11)
S1 = ("2009-12-01..2009-12-31", "Successor", "2009-12-01", "2009-12-31", 1)
Y = lambda y, who: (str(y), who, f"{y}-01-01", f"{y}-12-31", 12)
CCI = "Charter Communications, Inc."   # the issuer as the filings before the 2009-11-30 emergence name it (no Predecessor/Successor yet)
VINTAGES = [
    # sid, accession, file, title, fy label, header row, columns, EPS row, continuing-EPS row, shares row
    ("CH1", "0000950137-04-001876", "10-K__c83767e10vk.rows.txt", "Charter FY2003 10-K", "FY03",
     "2003 | 2002 (a) | 2001 (a) | 2000 (a) | 1999 (a)", [Y(y, CCI) for y in (2003, 2002, 2001, 2000, 1999)],
     "Loss per common share, basic and diluted", None, "Weighted-average common shares outstanding"),
    ("CH14", "0001091667-07-000015", "10-K__body.rows.txt", "Charter FY2006 10-K", "FY06",
     "2006 | 2005 | 2004 | 2003 | 2002", [Y(y, CCI) for y in (2006, 2005, 2004, 2003, 2002)],
     "Basic and diluted loss per common share",
     "Basic and diluted loss from continuing operations before cumulative effect of accounting change per common share",
     "Weighted-average shares outstanding, basic and diluted"),
    ("CH2", "0001091667-08-000004", "10-K__body.rows.txt", "Charter FY2007 10-K", "FY07",
     "2007 | 2006 | 2005 | 2004 | 2003", [Y(y, CCI) for y in (2007, 2006, 2005, 2004, 2003)],
     "Basic and diluted loss per common share",
     "Basic and diluted loss from continuing operations before cumulative effect of accounting change per common share",
     "Weighted-average shares outstanding, basic and diluted"),
    ("CH3", "0001091667-09-000038", "10-K__body.rows.txt", "Charter FY2008 10-K", "FY08",
     "2008 | 2007 | 2006 | 2005 | 2004", [Y(y, CCI) for y in (2008, 2007, 2006, 2005, 2004)],
     "Basic and diluted loss per common share",
     "Basic and diluted loss from continuing operations before cumulative effect of accounting change per common share",
     "Weighted-average shares outstanding, basic and diluted"),
    ("CH8", "0001091667-10-000019", "10-K__body.rows.txt", "Charter FY2009 10-K", "FY09",
     "2009 | 2009 | 2008 (a) | 2007 (a) | 2006 (a)(b) | 2005 (a)(b)", [S1, P11] + [Y(y, "Predecessor") for y in (2008, 2007, 2006, 2005)],
     "Diluted earnings (loss) per common share", "Diluted earnings (loss) from continuing operations per common share",
     "Weighted-average shares outstanding, diluted"),
    ("CH10", "0001091667-11-000029", "10-K__body.rows.txt", "Charter FY2010 10-K", "FY10",
     "2010 | 2009 | 2009 | 2008 (a) | 2007 (a) | 2006 (a)", [Y(2010, "Successor"), S1, P11] + [Y(y, "Predecessor") for y in (2008, 2007, 2006)],
     "Diluted earnings (loss) per common share", "Diluted earnings (loss) from continuing operations per common share",
     "Weighted-average shares outstanding, diluted"),
    ("CH11", "0001091667-12-000026", "10-K__chtr12312011-10k.rows.txt", "Charter FY2011 10-K", "FY11",
     "2011 | 2010 | 2009 | 2009 | 2008 (a) | 2007 (a)", [Y(2011, "Successor"), Y(2010, "Successor"), S1, P11] + [Y(y, "Predecessor") for y in (2008, 2007)],
     "Diluted earnings (loss) per common share", None, "Weighted-average shares outstanding, diluted"),
    ("CH12", "0001091667-13-000020", "10-K__chtr123112-10k.rows.txt", "Charter FY2012 10-K", "FY12",
     "2012 | 2011 | 2010 | 2009 | 2009 | 2008 (a)", [Y(y, "Successor") for y in (2012, 2011, 2010)] + [S1, P11, Y(2008, "Predecessor")],
     "Diluted earnings (loss) per common share", None, "Weighted-average shares outstanding, diluted"),
    ("CH13", "0001091667-14-000080", "10-K__chtr123113-10k.rows.txt", "Charter FY2013 10-K", "FY13",
     "2013 | 2012 | 2011 | 2010 | 2009 | 2009", [Y(y, "Successor") for y in (2013, 2012, 2011, 2010)] + [S1, P11],
     "Diluted earnings (loss) per common share", None, "Weighted-average shares outstanding, diluted"),
]

vintages = []
for sid, acc, fname, title, label, header, cols, eps_l, cont_l, sh_l in VINTAGES:
    p = path(acc, fname)
    after = "Item 6. Selected Financial Data."
    assert any(x == header for x in lines(p)[next(i for i, x in enumerate(lines(p)) if after in x):][:12]), (sid, "header")
    CHECK.setdefault(p, []).append(header)
    n = len(cols)
    rev = row(p, "Revenues", after, n)
    eps = row(p, eps_l, after, n)
    cont = row(p, cont_l, after, n) if cont_l else None
    sh = row(p, sh_l, after, n)
    periods = {}
    for i, (key, who, start, end, months) in enumerate(cols):
        periods[key] = {"issuer": who, "start": start, "end": end, "months": months, "revenue_m": rev[i], "eps_diluted": eps[i],
                        "eps_continuing": cont[i] if cont else eps[i], "diluted_shares_m": round(sh[i] / 1e6, 3)}
    day = source(sid, acc, p, title, f"Item 6, Selected Financial Data: revenues, diluted EPS ({eps_l!r})"
                 + (f" and from continuing operations ({cont_l!r})" if cont_l else "") + f" and {sh_l.lower()} for {', '.join(c[0] for c in cols)}")
    vintages.append({"published": day, "source": sid, "fy_label": label, "periods": periods,
                     "eps_basis": "diluted EPS as the Item 6 table prints it (basic equals diluted wherever a loss makes options antidilutive)"})

# the FY2009 vintage: the Predecessor's eleven months carry the Plan and fresh start gains; the Successor is not comparable
p9 = path("0001091667-10-000019", "10-K__body.rows.txt")
gain_plan = row(p9, "Gain due to Plan effects", "CONSOLIDATED STATEMENTS OF OPERATIONS", 4)
gain_fresh = row(p9, "Gain due to fresh start accounting adjustments", "CONSOLIDATED STATEMENTS OF OPERATIONS", 4)
pretax = row(p9, "Income (loss) before income taxes", "CONSOLIDATED STATEMENTS OF OPERATIONS", 4)
assert (gain_plan[1], gain_fresh[1], pretax[1]) == (6818, 5659, 9748)
v9 = next(v for v in vintages if v["source"] == "CH8")
v9["one_offs_note"] = (f"the Predecessor's eleven months to 2009-11-30: income before income taxes ${pretax[1]:,.0f}M includes the gain due to "
                       f"Plan effects (${gain_plan[1]:,.0f}M) and the gain due to fresh start accounting adjustments (${gain_fresh[1]:,.0f}M); "
                       f"without the ${gain_plan[1] + gain_fresh[1]:,.0f}M of gains it is a loss of ${gain_plan[1] + gain_fresh[1] - pretax[1]:,.0f}M "
                       "before taxes (the mirror of the AAPL FY2002 test)")
v9["not_comparable_quote"] = quote(p9, "Because our consolidated financial statements reflect fresh start accounting adjustments made upon emergence "
                                       "from bankruptcy, and because of the effects of the transactions that became effective pursuant to the Plan, "
                                       "financial information in the post-emergence financial statements is not comparable to our financial "
                                       "information from prior periods.")

# ── the listing record of the Class A common stock ───────────────────────────────────────────────────────────────────────────────
listings = []
p7 = path("0001091667-08-000004", "10-K__body.rows.txt")
listings.append({"published": SOURCES["CH2"]["published"], "source": "CH2", "issuer": CCI, "exchange": "NASDAQ Global Select Market",
                 "symbol": "CHTR", "quote": quote(p7, "Charter’s Class A common stock is quoted on the NASDAQ Global Select Market under the symbol “CHTR.”")})
p = path("0001091667-08-000083", "EX-99.1__exhibit99_1.rows.txt")
day = source("CH4", "0001091667-08-000083", p, "Charter 8-K of 2008-04-18 (Item 3.01, exhibit 99.1)", "the NASDAQ minimum bid price notice")
listings.append({"published": day, "source": "CH4", "issuer": CCI, "kind": "listing_notice",
                 "quote": quote(p, "its Class A common stock had closed below $1.00 per share for 30 consecutive business days")})
p = path("0001091667-09-000054", "8-K__body.rows.txt")
day = source("CH5", "0001091667-09-000054", p, "Charter 8-K of 2009-03-31 (Item 3.01)", "the NASDAQ delisting notice after the Chapter 11 petitions")
listings.append({"published": day, "source": "CH5", "issuer": CCI, "kind": "delisting_notice",
                 "quote": quote(p, "the Company's securities will be delisted by NASDAQ and that trading of the Company's Class A common stock will "
                                   "be suspended at the opening of business on April 7, 2009")})
p = path("0001354457-09-000102", "EX-99.25__chtrdelistreason.txt")
day = source("CH6", "0001354457-09-000102", p, "NASDAQ Form 25-NSE of 2009-04-22 (exhibit)", "the removal from listing")
listings.append({"published": day, "source": "CH6", "issuer": CCI, "kind": "delisted",
                 "quote": quote(p, "the Staff determination to delist the Company became final on April 7, 2009.")})
p = path("0001091667-09-000201", "15-12G__body.rows.txt")
day = source("CH7", "0001091667-09-000201", p, "Charter Form 15-12G of 2009-12-02", "the cancellation of the Old Common Stock")
listings.append({"published": day, "source": "CH7", "issuer": CCI, "kind": "cancelled",
                 "quote": quote(p, "(1) the Old Common Stock issued and outstanding immediately prior to the Effective Date was cancelled")})
listings.append({"published": SOURCES["CH8"]["published"], "source": "CH8", "issuer": "Successor", "exchange": "OTC Bulletin Board", "symbol": "CCMM",
                 "quote": quote(p9, "Charter’s Class A common stock is quoted on the OTC Bulletin Board under the symbol “CCMM.” The stock began "
                                    "being quoted on the Bulletin Board in December 2009 following our emergence from Chapter 11 proceedings."),
                 "quote_predecessor": quote(p9, "Prior to April 6, 2009, Predecessor common stock traded on the NASDAQ Global Select Market. From "
                                                "April 7, 2009 through the Effective Date, shares of common stock of Predecessor traded on the OTC "
                                                "Bulletin Board or in the “Pink Sheets.” On the Effective Date, all of the outstanding common stock "
                                                "and all other outstanding equity securities of Predecessor were cancelled pursuant to the terms of the Plan.")})
p = path("0001091667-10-000170", "8-A12B__body.rows.txt")
day = source("CH9", "0001091667-10-000170", p, "Charter Form 8-A12B of 2010-09-13 (accepted 2010-09-13 18:53 ET)", "the registration on NASDAQ")
listings.append({"published": day, "source": "CH9", "issuer": "Successor", "kind": "registration",
                 "quote": quote(p, "Class A Common Stock, par value $0.001 per share | The NASDAQ Stock Market LLC")})
p10 = path("0001091667-11-000029", "10-K__body.rows.txt")
listings.append({"published": SOURCES["CH10"]["published"], "source": "CH10", "issuer": "Successor", "exchange": "NASDAQ Global Select Market",
                 "symbol": "CHTR", "effective": "2010-09-14",
                 "quote": quote(p10, "The Successor’s common stock was quoted on the OTC Bulletin Board from the Effective Date until the stock was "
                                     "listed on the NASDAQ Global Select Market on September 14, 2010.")})

facts = {
    "_doc": ("Point-in-time fact sheet for CHTR (Charter Communications, Inc., CIK 1091667), generated by retro/generators/chtr/gen_chtr.py "
             "from the filings; every value is tied to a source and becomes visible only on or after its 'published' date (EDGAR's "
             "acceptance time in ET: accepted at or after 16:00, the next trading day). It holds what decides whether a date can be built "
             "under method r2, and nothing else: each 10-K vintage's Item 6 EPS history, the listing record and the price basis. Every "
             "period of 1999-2013 is a loss per share except the Predecessor's eleven months to 2009-11-30 (the Plan and fresh start "
             "gains) and the Successor's first month (December 2009), neither of them a year, so no date of 2008-2013 has a full year of "
             "positive EPS to anchor a P/E and none is built (retro/README.md, \"CHTR 2008-2009\"). No print, guide, dividend, signal or "
             "theme event is transcribed: no CHTR stock paid a dividend in these years (the FY2009 10-K restricts it), and the builder "
             "refuses any date that passes the gate until they are."),
    "ticker": "CHTR",
    "company": "Charter Communications, Inc.",
    "price_basis": ("Yahoo's CHTR series is the Successor's Class A common stock from its first point, 2010-01-05 (firstTradeDate; the "
                    "stock quoted on the OTC Bulletin Board as CCMM from December 2009 and listed on NASDAQ as CHTR from 2010-09-14). Yahoo "
                    "serves no close of the Predecessor's Class A common stock (NASDAQ: CHTR to 2009-04-06, then the OTC Bulletin Board or "
                    "the Pink Sheets to its cancellation on 2009-11-30) under CHTR or any other symbol read (CHTRQ, CCMM: not found)."),
    "series_start": "2010-01-05",
    "sources": SOURCES,
    "history_vintages": sorted(vintages, key=lambda v: v["published"]),
    "listings": sorted(listings, key=lambda x: x["published"]),
    "prints": [], "guides": [], "dividends": [], "events": [], "company_names": [], "splits": [],
}
out = A.out or os.path.join(REPO, "retro", "facts", "CHTR.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(facts, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
cl = A.checklist or os.path.join(SP, "checklist_chtr.json")
with open(cl, "w", encoding="utf-8") as fh:
    json.dump(CHECK, fh, indent=1, ensure_ascii=False)
print(f"{out}: {len(SOURCES)} sources, {len(vintages)} vintages, {len(listings)} listing facts; checklist {cl}: "
      f"{sum(len(v) for v in CHECK.values())} strings")
