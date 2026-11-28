#!/usr/bin/env python3
"""Generate retro/facts/TRGP.json (2012-02-24 to 2013-12-31) from Targa Resources Corp.'s own filings (edgar.py's rows).

Every raw figure is read from its own labelled row (the row is kept for the verbatim checklist), every rate, margin, tax rate
and rule-T value is computed, every quoted sentence is asserted present in its own filing. Only filings accepted on or before
2013-12-31 are read (the FY2010-FY2012 10-Ks, the earnings releases of Q3 2011 to Q3 2013, the outlook 8-K of 2012-10-17).
The downloads (keep them outside the repository):

    python3 retro/tools/edgar.py index 1389170 <dir>
    python3 retro/tools/edgar.py fetch 1389170 <dir> --from 2010-09-01 --to 2014-03-31 --forms 10-K 10-Q 8-K 10-K/A 8-K/A 10-Q/A 424B1

Run:
    python3 -I retro/generators/trgp/gen_trgp.py --filings <dir> [--out retro/facts/TRGP.json] [--checklist <dir>/checklist_trgp.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_trgp.json
"""
import argparse
import datetime as dt
import json
import math
import os
import re
import sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))       # retro/generators/trgp -> the repository
_ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("--filings", required=True, help="folder edgar.py wrote (allrows.json, tenk/, tenq/, eightk/, other/)")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/TRGP.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_trgp.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402  (the repo's own tool: trading days from the Yahoo cache)

ET = ZoneInfo("America/New_York")
CUT = "2013-12-31"
CIK = 1389170
FILINGS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("TRGP")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
CHECK = {}


def norm(s):
    return re.sub(r"\s+", " ", s.replace(" ", " ")).strip()


def doc(acc, prefix):
    for sub in ("tenk", "tenq", "eightk", "other"):
        d = os.path.join(SP, sub, acc)
        if os.path.isdir(d):
            hits = sorted(f for f in os.listdir(d) if f.startswith(prefix) and f.endswith(".rows.txt"))
            assert len(hits) == 1, (acc, prefix, hits)
            return os.path.join(d, hits[0])
    raise AssertionError(acc)


TEXT = {}


def lines(path):
    if path not in TEXT:
        with open(path, encoding="utf-8", errors="replace") as fh:
            TEXT[path] = [norm(x) for x in fh.read().split("\n")]
    return TEXT[path]


def quote(path, s):
    """Assert a sentence or fragment is in its filing, word for word; add it to the checklist."""
    full = norm(" ".join(lines(path)))
    assert norm(s) in full, (path, s[:120])
    CHECK.setdefault(path, []).append(s)
    return s


def num(tok):
    t = tok.strip().replace("$", "").replace(",", "").strip()
    if t in ("—", "-", "–", ""):
        return 0.0
    neg = t.startswith("(") and t.endswith(")")
    v = float(t.strip("()%"))
    return -v if neg else v


DASH = lambda t: t.replace("—", "-").replace("–", "-").replace(" - ", " - ")


def row(path, labels, start=0, stop=None):
    """The unique row in lines[start:stop] whose first cell is one of `labels` (dashes normalized); (row, numeric values)."""
    labels = [labels] if isinstance(labels, str) else labels
    key = lambda x: re.sub(r"\s*-\s*", "-", DASH(x.split(" |")[0].strip()))
    want = {re.sub(r"\s*-\s*", "-", DASH(lb)) for lb in labels}
    L = lines(path)[start:stop]
    hits = [x for x in L if "|" in x and key(x) in want]
    assert len(hits) == 1, (path, labels, len(hits), hits[:3], start, stop)
    r = hits[0]
    vals = [num(t) for t in r.split("|")[1:] if t.strip()]
    CHECK.setdefault(path, []).append(r)
    return r, vals


def line_no(path, pred, start=0):
    L = lines(path)
    return next(i for i in range(start, len(L)) if pred(L[i]))


def next_tday(d):
    return min(x for x in TDAYS if x > d)


def published(acc):
    """Publication date from EDGAR's acceptance time (UTC -> ET); at or after the 16:00 ET close, the next trading day."""
    r = FILINGS[acc]
    t = dt.datetime.fromisoformat(r[1].replace("Z", "+00:00")).astimezone(ET)
    d = t.date().isoformat()
    hm = t.strftime("%H:%M")
    if hm >= "16:00":
        return next_tday(d), f"accepted {d} {hm} ET (after the close), so dated the next trading day"
    if d not in TDAYS:
        return next_tday(d), f"accepted {d} {hm} ET (not a trading day), so dated the next trading day"
    if hm < "09:30":
        return d, f"accepted {d} {hm} ET (before the open)"
    return d, f"accepted {d} {hm} ET (during market hours)"


URL = lambda acc, fn: f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc.replace('-', '')}/{fn}"
SRC = {}


def source(sid, acc, title, path, supports):
    p, filed = published(acc)
    assert p <= CUT, (sid, p)
    fn = os.path.basename(path).split("__", 1)[1].replace(".rows.txt", ".htm")
    SRC[sid] = dict(published=p, filed=filed, title=title, url=URL(acc, fn), supports=supports)
    return sid


usd_m = lambda v: f"${v:,.1f}M" if v >= 0 else f"$({-v:,.1f})M"
pct = lambda a, b: round((b / a - 1) * 100, 1) if a > 0 else round((b - a) / abs(a) * 100, 1) if a < 0 else None
mg = lambda x, rev: round(x / rev * 100 + 0.0, 2)

# ── filings ─────────────────────────────────────────────────────────────────────
K10, K11, K12 = "0001389170-11-000003", "0001389170-12-000007", "0001140361-13-008128"     # FY2010, FY2011, FY2012 10-Ks
F10, F11, F12 = doc(K10, "10-K__"), doc(K11, "10-K__"), doc(K12, "10-K__")
P424 = "0000950123-10-111598"                                                              # the IPO prospectus (424B1)
F424 = doc(P424, "424B1__")
REL = {"Q3 2011": "0001389170-11-000043", "Q4 2011": "0001193125-12-073926", "Q1 2012": "0001193125-12-206475",
       "Q2 2012": "0001193125-12-336213", "Q3 2012": "0001193125-12-445176", "Q4 2012": "0001193125-13-057497",
       "Q1 2013": "0001193125-13-197495", "Q2 2013": "0001193125-13-313890", "Q3 2013": "0001193125-13-425345"}
FREL = {q: doc(a, "EX-99.1__") for q, a in REL.items()}
OUTLOOK_8K = "0001193125-12-425975"
FOUT = doc(OUTLOOK_8K, "EX-99.1__")

# ── the listing and the two Targa entities (checked against the filings) ───────
LISTING_Q = quote(F10, "Our common stock has been listed on the New York Stock Exchange since December 7, 2010 under the symbol “TRGP.”")
NOMARKET_Q = quote(F424, "No public market currently exists for our common stock.")
NGLS_Q = quote(F424, "Targa Resources Partners LP (NYSE: NGLS), a publicly traded Delaware limited partnership")
NOEPS_Q = quote(F10, "For 2008 and 2009, there was no net income available to common shareholders as the preferred shareholders are "
                     "entitled to all undistributed earnings. As such, there were no earnings per share to our common shareholders "
                     "during 2008 and 2009.")
CONV_Q = quote(F10, "During 2010, in connection with the closing of the IPO, 6,409,697 shares of Series B Convertible Participating "
                    "Preferred Stock, plus accreted value, were converted into 35,356,698 shares of common stock.")
NOTPUB_Q = quote(F10, "As of June 30, 2010, the last day of the registrant’s most recently completed second quarter, the registrant’s "
                      "common stock was not publicly traded.")

# ── release tables ──────────────────────────────────────────────────────────────


def trc_block(path):
    """(start, stop) of TRC's consolidated statement of operations in a joint release (the Partnership's comes first)."""
    L = lines(path)
    i = next(i for i in range(len(L)) if L[i] == "CONSOLIDATED STATEMENTS OF OPERATIONS" and
             any(L[j].upper() == "TARGA RESOURCES CORP." for j in range(i - 3, i)))
    j = next(k for k in range(i + 1, len(L)) if L[k].upper() == "TARGA RESOURCES CORP.")
    return i, j


NI_TRC = ["NET INCOME (LOSS) ATTRIBUTABLE TO TARGA RESOURCES CORP.", "NET INCOME ATTRIBUTABLE TO TARGA RESOURCES CORP.",
          "Net income (loss) attributable to Targa Resources Corp.", "Net income attributable to Targa Resources Corp.",
          "NET INCOME AVAILABLE TO COMMON SHAREHOLDERS", "Net income available to common shareholders"]   # from Q2 2012 (no preferred)
EPS_D = ["Net income (loss) available per common share - diluted", "Net income available per common share - diluted",
         "Net income available per common share - basic and diluted"]
SH_D = ["Weighted average shares outstanding - diluted"]


def trc_ops(path):
    i, j = trc_block(path)
    vals = {}
    for k, labs in (("rev", ["REVENUES", "Revenues"]), ("oi", ["INCOME FROM OPERATIONS", "Income from operations"]),
                    ("pti", ["Income before income taxes"]), ("ni", ["NET INCOME", "Net income"]), ("nia", NI_TRC),
                    ("eps", EPS_D), ("sh", SH_D)):
        vals[k] = row(path, labs, i, j)[1]
    return vals


SEGS = ("Field Gathering and Processing", "Coastal Gathering and Processing", "Logistics Assets", "Marketing and Distribution")


def seg_om(path):
    """The four segments' operating margin rows, in order, after the release's 'Review of Segment Performance'."""
    L = lines(path)
    i0 = line_no(path, lambda x: "Review of Segment Performance" in x)
    idx = [k for k in range(i0, len(L)) if L[k].startswith("Operating margin |")][:4]
    out = []
    for name, k in zip(SEGS, idx):
        head = next(m for m in range(k, i0, -1) if L[m].startswith(name))       # the segment's own heading above the row
        assert k - head < 15, (path, name)
        _, v = row(path, "Operating margin", k, k + 1)
        out.append(v)
    return out


def sentence(path, pattern):
    full = norm(" ".join(lines(path)))
    m = re.search(pattern, full)
    assert m, (path, pattern)
    return quote(path, m.group(0))


# ── prints ──────────────────────────────────────────────────────────────────────
QDATE = {1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"}
SID = {q: f"TG{10 + i}" for i, q in enumerate(REL)}
prints, dividends = [], []
for q, acc in REL.items():
    f = FREL[q]
    qn, fy = int(q[1]), int(q[3:])
    o = trc_ops(f)
    s = seg_om(f)
    gp, gp0 = s[0][0] + s[1][0], s[0][1] + s[1][1]
    lm, lm0 = s[2][0] + s[3][0], s[2][1] + s[3][1]
    call = sentence(f, r"will host a joint conference call for investors and analysts at [^.]*? (a\.m\.|p\.m\.) Eastern Time")
    pub, filed = published(acc)
    title = f"Targa Resources Partners LP and Targa Resources Corp. {q} results (8-K, Exhibit 99.1)"
    source(SID[q], acc, title, f, "Targa Resources Corp.'s consolidated statement of operations (revenues, income from operations, "
           "income before income taxes, net income attributable to TRC, diluted EPS and shares) and the Partnership's segment "
           "operating margins, each with the year-ago quarter as this release shows it; the TRC dividend declared")
    raw = {"rev_m": o["rev"][0], "rev_prior_m": o["rev"][1], "oi_m": o["oi"][0], "oi_prior_m": o["oi"][1],
           "pti_m": o["pti"][0], "pti_prior_m": o["pti"][1], "eps_q": o["eps"][0], "eps_q_prior": o["eps"][1],
           "dil_sh_m": o["sh"][0], "gp_m": round(gp, 1), "gp_prior_m": round(gp0, 1), "lm_m": round(lm, 1),
           "lm_prior_m": round(lm0, 1), "nia_m": o["nia"][0]}
    eps_prior = o["eps"][1]
    pr = {"quarter": q, "fy": fy, "q": qn, "published": pub, "source": SID[q],
          "release": dt.date.fromisoformat(pub).strftime("%b %-d"),
          "release_time": f"8-K {filed}; {call}", "period_end": f"{fy}-{QDATE[qn]}", "raw": raw,
          "sales_b": round(raw["rev_m"] / 1000, 3), "sales_pct": pct(raw["rev_prior_m"], raw["rev_m"]),
          "opm": mg(raw["oi_m"], raw["rev_m"]),
          "opm_bp": round((mg(raw["oi_m"], raw["rev_m"]) - mg(raw["oi_prior_m"], raw["rev_prior_m"])) * 100, 1),
          "ptm": mg(raw["pti_m"], raw["rev_m"]),
          "ptm_bp": round((mg(raw["pti_m"], raw["rev_m"]) - mg(raw["pti_prior_m"], raw["rev_prior_m"])) * 100, 1),
          "eps_q": raw["eps_q"], "eps_q_prior": eps_prior, "diluted_shares_m": raw["dil_sh_m"],
          "gp_pct": pct(raw["gp_prior_m"], raw["gp_m"]), "lm_pct": pct(raw["lm_prior_m"], raw["lm_m"]),
          "seg_note": (f"Natural Gas Gathering and Processing (Field and Coastal) operating margin {usd_m(gp)} vs {usd_m(gp0)}, "
                       f"Logistics and Marketing (Logistics Assets and Marketing and Distribution) {usd_m(lm)} vs {usd_m(lm0)} "
                       "(the Partnership's segments, consolidated by TRC)"),
          "sales_note": f"revenues {usd_m(raw['rev_m'])} vs {usd_m(raw['rev_prior_m'])}",
          "margin_note": (f"income from operations {usd_m(raw['oi_m'])} vs {usd_m(raw['oi_prior_m'])}; income before income taxes "
                          f"{usd_m(raw['pti_m'])} vs {usd_m(raw['pti_prior_m'])}"),
          "eps_note": (f"GAAP, diluted, ${raw['eps_q']:.2f} against " +
                       (f"${eps_prior:.2f}" if eps_prior >= 0 else f"$({-eps_prior:.2f})") + " a year earlier" +
                       (" (the year-ago quarter before the IPO's conversion of the Series B preferred stock, on 13.2M weighted shares)"
                        if q == "Q4 2011" else "")),
          "next_print": f"the Q{qn % 4 + 1} {fy + (1 if qn == 4 else 0)} release"}
    m = re.search(r"(?:the Company’s|The Company’s) distributable cash flow for the (?:fourth|third|second|first) quarter \d{4} "
                  r"(?:of|was) \$([\d.]+) million", norm(" ".join(lines(f))))
    assert m, (q, "TRC distributable cash flow")
    quote(f, m.group(0))
    pr["cash_note"] = f"TRC distributable cash flow ${float(m.group(1)):.1f}M (non-GAAP, display only)"
    # the TRC dividend declared with the release (quarterly rate); the Q3 2011 release says "the Company announced"
    dm = re.search(r"(?:TRC declared|the Company announced) a quarterly dividend of (\$[\d.]+|[\d.]+¢) per share of its common stock "
                   r"for the three months ended [A-Za-z]+ \d+, \d{4}", norm(" ".join(lines(f))))
    assert dm, (q, "dividend")
    quote(f, dm.group(0))
    rate = float(dm.group(1).strip("$¢")) / (100 if dm.group(1).endswith("¢") else 1)
    dividends.append({"published": pub, "source": SID[q], "quarterly": round(rate, 5),
                      "note": f"${rate:.5f}".rstrip("0").rstrip(".") + f" a quarter, declared for {q} (the {q} release)",
                      "quote": dm.group(0)})
    if qn == 4:                                   # the year: the release's year columns
        yr = {k: v[2] for k, v in o.items()}
        yr0 = {k: v[3] for k, v in o.items()}
        tax = round(yr["pti"] - yr["ni"], 1)
        kept = yr["eps"] > 0
        notes = {2011: ("the release lists no one-off item of TRC's; the Partnership's $7.2 million of non-cash charges related to "
                        "derivative instruments (pre-tax, before the noncontrolling interests) recur and, even all credited to TRC, "
                        "are under the year's net income attributable to TRC"),
                 2012: ("the release's only listed item is 'approximately $6 million of transaction costs related to the Badlands "
                        "acquisition' in the fourth quarter (the Partnership's, pre-tax); even all credited to TRC it is under the "
                        "year's net income attributable to TRC")}
        items = {2011: 7.2, 2012: 6.0}[fy]
        if fy == 2011:
            quote(f, "Net income for the full year 2011 and 2010 included $7.2 million and $6.4 million in non-cash charges related to "
                     "derivative instruments, respectively.")
        if fy == 2012:
            quote(f, "Net income and adjusted EBITDA for the fourth quarter of 2012 included approximately $6 million of transaction "
                     "costs related to the Badlands acquisition.")
        pr["fy_actual"] = {
            "fy": fy, "fy_label": f"FY{fy % 100:02d}", "eps_normalized": yr["eps"] if kept else None, "excluded_note": None,
            "revenue_usd_b": round(yr["rev"] / 1000, 4), "diluted_shares_m": yr["sh"],
            "normalization_note": f"FY{fy % 100:02d} ${yr['eps']:.2f} diluted, GAAP, from the {q} release ({pub}) until the 10-K",
            "op_margin": mg(yr["pti"], yr["rev"]),
            "op_margin_note": f"FY{fy % 100:02d} income before income taxes {usd_m(yr['pti'])} / revenues {usd_m(yr['rev'])} ({q} release)",
            "sales_growth": pct(yr0["rev"], yr["rev"]), "check_pretax_margin": mg(yr["pti"], yr["rev"]),
            "check_pretax_note": (f"FY{fy % 100:02d} income before income taxes / revenues ({q} release), before the noncontrolling "
                                  "interests (the Partnership's other unitholders), so the check overstates TRC's own EPS"),
            "tax_rate": round(tax / yr["pti"], 3),
            "tax_note": f"FY{fy % 100:02d} effective rate: income tax expense {usd_m(tax)} (income before income taxes less net income) on {usd_m(yr['pti'])}",
            "one_off_test": {"items_after_tax_m": items, "income_attributable_m": yr["nia"], "distorted": items > yr["nia"],
                             "kind": "charges", "note": notes[fy]}}
        assert kept and not pr["fy_actual"]["one_off_test"]["distorted"]
    prints.append(pr)

# ── history vintages (10-Ks) ────────────────────────────────────────────────────


def sel(path):
    """Item 6, Selected Financial Data: the year header and the rows the models read."""
    L = lines(path)
    i = max(k for k in range(len(L)) if re.sub(r" \| ", " ", L[k]).startswith("Item 6. Selected Financial Data") and "|" not in L[k][-6:])
    yi = next(k for k in range(i, i + 8) if re.fullmatch(r"(20\d\d \| ){4}20\d\d", L[k]))
    years = [int(y) for y in L[yi].split(" | ")]
    stop = i + 40
    rev = row(path, ["Revenues", "Revenues(1)"], i, stop)[1]
    oi = row(path, "Income from operations", i, stop)[1]
    nia = row(path, "Net income (loss) attributable to Targa Resources Corp.", i, stop)[1]
    epsr = row(path, ["Net loss per common share - diluted", "Net income (loss) per common share - diluted",
                      "Net loss per common share - Basic and diluted"], i, stop)
    return years, dict(zip(years, rev)), dict(zip(years, oi)), dict(zip(years, nia)), epsr


def stmt(path):
    """The consolidated statement of operations (last three years) and the statement of cash flows."""
    L = lines(path)
    i0 = next(k for k in range(len(L)) if L[k] == "CONSOLIDATED STATEMENTS OF OPERATIONS")
    pti = row(path, "Income before income taxes", i0, i0 + 40)[1]
    ni = row(path, "Net income", i0, i0 + 40)[1]
    i = i0
    c0 = line_no(path, lambda x: x == "CONSOLIDATED STATEMENTS OF CASH FLOWS", i)
    cfo = row(path, "Net cash provided by operating activities", c0, c0 + 80)[1]
    capex = row(path, "Outlays for property, plant and equipment", c0, c0 + 80)[1]
    divs = row(path, "Dividends to common and common equivalent shareholders", c0, c0 + 80)[1]
    return pti, ni, cfo, capex, divs


def groups(path, year):
    """The segment note's operating margin by segment for the latest year (its first 'Operating margin' row; display only)."""
    L = lines(path)
    n = max(k for k in range(len(L)) if re.match(r"Note \d+ . Segment Information$", L[k]))
    k = line_no(path, lambda x: x.startswith("Operating margin |"), n)
    _, v = row(path, "Operating margin", k, k + 1)
    assert len(v) == 8 and abs(sum(v[:7]) - v[7]) < 0.15, (path, v)
    return [[s, round(x / 1000, 4), None] for s, x in zip(SEGS, v[:4])], v[7]


WHY_COMMODITY = {
    K10: "The Partnership’s primary natural gas gathering and processing arrangements that expose it to commodity price risk are its percent-of-proceeds arrangements.",
    K11: "The Partnership’s primary natural gas gathering and processing arrangements that expose it to commodity price risk are its percent-of-proceeds arrangements.",
    K12: "The Partnership’s primary natural gas gathering and processing arrangements that expose it to commodity price risk are its percent-of-proceeds arrangements.",
}
WHY_CYCLE = ("even if the Partnership’s business experiences fluctuations in its cash from operations due to seasonal and cyclical "
             "factors")
WHY_DEP = "Our cash flow is dependent upon the ability of the Partnership to make cash distributions to us."

vintages = []
VSID = {K10: "TG1", K11: "TG2", K12: "TG3"}
VF = {K10: F10, K11: F11, K12: F12}
prev_rev = {}
for acc in (K10, K11, K12):
    f = VF[acc]
    years, rev, oi, nia, (epsrow, epsv) = sel(f)
    last = years[0]
    title = f"Targa Resources Corp. FY{last} 10-K"
    source(VSID[acc], acc, title, f, "Item 6 (selected financial data: revenues and EPS), the statements of operations and cash "
           "flows, the segment note, Item 5 and the risk factors")
    pti, ni, cfo, capex, divs = stmt(f)
    tax = round(pti[0] - ni[0], 1)
    grp, cons = groups(f, last)
    eps = dict(zip(years, epsv))
    eps_norm = {str(y): eps[y] for y in years if y >= 2011 and eps[y] > 0}
    excl = {"2010": ("$(30.94) a diluted share for 2010 (net loss available to common shareholders of $(202.3)M on 6.5M weighted "
                     "shares, after $9.5M of Series B dividends and $177.8M of dividends on common equivalents, the April 2010 special "
                     "distribution): a loss, so no P/E; 2008 and 2009 have no EPS to common shareholders (the preferred shareholders "
                     "were entitled to all undistributed earnings) and 2006-2007 are pre-IPO common shares")}
    assert eps[2010] == -30.94
    quote(f, WHY_COMMODITY[acc])
    quote(f, WHY_CYCLE)
    quote(f, WHY_DEP)
    revs = {**prev_rev, **{str(y): round(rev[y] / 1000, 4) for y in years}}
    rsrc = {**(dict(vintages[-1]["revenue_sources"]) if vintages else {}), **{str(y): VSID[acc] for y in years}}
    prev_rev = revs
    shares = {}
    if last >= 2011:
        for p in prints:                              # the diluted counts of the Q4 releases' years, as each 10-K's EPS note states them
            a = p.get("fy_actual")
            if a and a["fy"] <= last:
                shares[str(a["fy"])] = a["diluted_shares_m"]
    v = {"company": "Targa Resources Corp.", "exchange": "NYSE", "symbol": "TRGP", "pe_window_start": "2010-12-07",
         "kind": "DURABLE", "kind_text": "A midstream natural gas and NGL company (the parent of Targa Resources Partners LP)",
         "business_line": "Natural gas gathering and processing, NGL logistics and marketing (through Targa Resources Partners LP)",
         "margin_signal_name": "Pre-tax margin change",
         "normalization": ("diluted EPS, GAAP, each year from the latest filing that reports it; the history starts with 2011, the first "
                           "full year as a listed company (2010 a loss per share, 2008-2009 no EPS to common shareholders)"),
         "published": SRC[VSID[acc]]["published"], "sources": [VSID[acc]] + ([] if acc == K10 else ["TG1"]),
         "fy_label": f"FY{last % 100:02d}", "fiscal_year_ends": {str(last): f"{last}-12-31"},
         "eps_normalized": eps_norm, "eps_excluded": excl,
         "revenue_usd_b": revs, "revenue_sources": rsrc,
         "revenue_note": "consolidated revenues (the Partnership in, as TRC consolidates it); each year from the latest 10-K that reports it",
         "diluted_shares_m": shares,
         "shares_note": ("diluted weighted-average shares of the statements of operations, from 2011 (2010's 6.5M is a weighted average of "
                         "the pre-IPO common shares, before the Series B preferred converted into 35.4M shares on December 10, 2010)"),
         "prev_fy_op_margin": mg(pti[0], rev[last]),
         "prev_fy_op_margin_note": f"FY{last % 100:02d} income before income taxes {usd_m(pti[0])} / revenues {usd_m(rev[last])} ({title})",
         "prev_fy_sales_growth": pct(rev[years[1]], rev[last]),
         "check_pretax_margin": mg(pti[0], rev[last]),
         "check_pretax_note": (f"FY{last % 100:02d} income before income taxes / revenues ({title}), before the noncontrolling interests "
                               "(the Partnership's other unitholders), so the check overstates TRC's own EPS"),
         "tax_rate": round(tax / pti[0], 3),
         "tax_note": f"FY{last % 100:02d} effective rate: income tax expense {usd_m(tax)} (income before income taxes less net income) on {usd_m(pti[0])} ({title})",
         "dividend_annual": None, "dividend_note": None,
         "fcf_b": round((cfo[0] + capex[0]) / 1000, 3), "fcf_label": f"FY{last % 100:02d}",
         "fcf_note": (f"consolidated net cash provided by operating activities {usd_m(cfo[0])} less outlays for property, plant and "
                      f"equipment {usd_m(-capex[0])} ({title}; the Partnership's, mostly)"),
         "cash_return_text": f"{usd_m(-divs[0])} of dividends to common and common equivalent shareholders in FY{last % 100:02d}",
         "groups": grp, "groups_basis": f"FY{last % 100:02d} segment operating margin, USD bn ({title}'s segment note; 'Other', the hedges, and TRC Non-Partnership left out)",
         "why": (f"Commodity exposure ({title}): {WHY_COMMODITY[acc]} Distribution policy: '{WHY_CYCLE}' (the boilerplate of the "
                 f"cash distribution policy, not a statement that the business is cyclical: the CHTR reading). Risk factor: '{WHY_DEP}'"
                 "; no theme in taxonomy_eras.json is live for a midstream natural gas company on this date")}
    if acc == K10:
        assert not eps_norm
    vintages.append(v)

# ── the outlook 8-K and the releases' dividend outlooks (display only) ──────────
OUT_Q1 = quote(FOUT, "Based on the estimated range of Adjusted EBITDA for 2013 and assuming generally stable broader market conditions, "
                     "the Partnership expects to be in a position to increase distributions per common unit by 10% to 12% in 2013 compared "
                     "to 2012, subject to approval of the board of directors of the Partnership’s general partner.")
OUT_Q2 = quote(FOUT, "The Partnership estimates that Adjusted EBITDA for 2013 will be approximately $540 million to $570 million.")
full_out = norm(" ".join(lines(FOUT)))
m = re.search(r"Given the Partnership’s expected distribution growth[^.]*TRC expects to be in a position to increase dividends by 25% to 30%\+ in 2013 compared to 2012[^.]*\.", full_out)
OUT_TRC = quote(FOUT, m.group(0).strip()) if m else None
source("TG30", OUTLOOK_8K, "Targa Resources Provides Update on Financial Outlook (8-K of 2012-10-17, Exhibit 99.1)", FOUT,
       "the Partnership's 2013 Adjusted EBITDA estimate and distribution growth, TRC's 2013 dividend outlook (display only)")
g3 = FREL["Q3 2013"]
OUT_Q3 = quote(g3, "Given the Partnership’s expected distribution growth of 7% to 9% in 2014, TRC expects to be in a position to increase "
                   "dividends in excess of 25% compared to 2013, subject to the approval of the board of directors of TRC.")
guides = [{"fy": 2013, "published": SRC["TG30"]["published"], "source": "TG30", "rev_none": True,
           "display": ("TRC 2013 dividend outlook: " + (f"'{OUT_TRC}'" if OUT_TRC else "") +
                       f" (the Partnership: '{OUT_Q2}'); no revenue, EPS or margin guide (display only)")},
          {"fy": 2014, "published": prints[-1]["published"], "source": SID["Q3 2013"], "rev_none": True,
           "display": f"TRC 2014 dividend outlook: '{OUT_Q3}'; no revenue, EPS or margin guide (display only)"}]
assert OUT_TRC, "the 8-K's TRC dividend sentence"

# ── rule T (the filings public on the first date, 2012-02-24: the FY2010 10-K and the Q4 2011 release) ──
_, rev10, oi10, _, _ = sel(F10)
f4 = FREL["Q4 2011"]
o4 = trc_ops(f4)
rev = {**rev10, 2011: o4["rev"][2]}
rev_for_2011 = o4["rev"][3]                       # 2010 as the Q4 2011 release restates it
oi = {**oi10, 2011: o4["oi"][2]}
L10 = lines(F10)
pti_i = max(k for k in range(len(L10)) if L10[k].startswith("Income before income taxes |") and len(L10[k].split("|")) == 4)
pti10 = row(F10, "Income before income taxes", pti_i, pti_i + 1)[1]
pti = {2010: pti10[0], 2009: pti10[1], 2008: pti10[2], 2011: o4["pti"][2]}
revenue_changes = {str(y): pct(rev[y - 1], rev[y]) for y in (2007, 2008, 2009, 2010)}
revenue_changes["2011"] = pct(rev_for_2011, rev[2011])
opm = {y: mg(oi[y], rev[y]) for y in (2006, 2007, 2008, 2009, 2010)}
op_changes = {str(y): round((opm[y] - opm[y - 1]) * 100, 1) for y in (2007, 2008, 2009, 2010)}
op_changes["2011"] = round((mg(o4["oi"][2], o4["rev"][2]) - mg(o4["oi"][3], o4["rev"][3])) * 100, 1)
ptm = {y: mg(pti[y], rev[y]) for y in (2008, 2009, 2010)}
pt_changes = {str(y): round((ptm[y] - ptm[y - 1]) * 100, 1) for y in (2009, 2010)}
pt_changes["2011"] = round((mg(o4["pti"][2], o4["rev"][2]) - mg(o4["pti"][3], o4["rev"][3])) * 100, 1)
# the division operating margins: the FY2010 10-K's MD&A by segment (2008-2010), the Q4 2011 release (2011 against 2010)
segv = {}
L = lines(F10)
for name in SEGS:
    i = line_no(F10, lambda x: x == name, line_no(F10, lambda x: x.startswith("Results of Operations of the Partnership")))
    segv[name] = row(F10, "Operating margin", i, i + 8)[1][:3]            # 2010, 2009, 2008
s4 = seg_om(f4)
yrs = {2010: 0, 2009: 1, 2008: 2}
gp = {y: segv[SEGS[0]][k] + segv[SEGS[1]][k] for y, k in yrs.items()}
lm = {y: segv[SEGS[2]][k] + segv[SEGS[3]][k] for y, k in yrs.items()}
assert abs(s4[0][3] + s4[1][3] - gp[2010]) < 0.05 and abs(s4[2][3] + s4[3][3] - lm[2010]) < 0.05, "the release's 2010 = the 10-K's"
gp[2011], lm[2011] = s4[0][2] + s4[1][2], s4[2][2] + s4[3][2]
gp_changes = {str(y): pct(gp[y - 1], gp[y]) for y in (2009, 2010, 2011)}
lm_changes = {str(y): pct(lm[y - 1], lm[y]) for y in (2009, 2010, 2011)}


def thresholds(values, unit):
    v = sorted(values.values())
    n = len(v)
    med = v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
    worst, best = v[0], v[-1]
    r = lambda x: math.floor(x / unit + 0.5) * unit
    return dict(zip(("BEAR", "BASE", "BULL", "XBULL"), (r(worst + (worst - med)), r(worst), r(med), r(best))))


def rt(values, unit, srcs, note):
    return {"values": values, "sources": srcs, "unit": unit, "lower_is_better": False, "thresholds": thresholds(values, unit),
            "note": note}


rule_t = {
    "gp": rt(gp_changes, 1, {"2009": "TG1", "2010": "TG1", "2011": "TG11"},
             "Field plus Coastal Gathering and Processing operating margin (the Partnership's segments, common control basis): "
             "2008-2010 from the FY2010 10-K's results by segment, 2011 against 2010 from the Q4 2011 release"),
    "lm": rt(lm_changes, 1, {"2009": "TG1", "2010": "TG1", "2011": "TG11"},
             "Logistics Assets plus Marketing and Distribution operating margin, the same sources"),
    "revenue": rt(revenue_changes, 1, {"2007": "TG1", "2008": "TG1", "2009": "TG1", "2010": "TG1", "2011": "TG11"},
                  "2006-2010 from the FY2010 10-K's selected financial data; 2011 against 2010 as the Q4 2011 release restates it"),
    "op_margin": rt(op_changes, 10, {"2007": "TG1", "2008": "TG1", "2009": "TG1", "2010": "TG1", "2011": "TG11"},
                    "income from operations on revenues"),
    "pretax_margin": rt(pt_changes, 10, {"2009": "TG1", "2010": "TG1", "2011": "TG11"},
                        "income before income taxes on revenues; the FY2010 10-K's statements give 2008-2010"),
}

facts = {
    "_doc": ("Targa Resources Corp. (NYSE: TRGP), point-in-time facts for retro/build_trgp.py. Every value carries its source and the "
             "source's publication date (EDGAR acceptance time; at or after the 16:00 ET close it counts from the next trading day). "
             "Generated by retro/generators/trgp/gen_trgp.py from the filings' converted rows: each figure is read from its labelled "
             "row, the row is asserted present in its own filing, and every rate, margin, tax rate and rule-T value is computed. "
             "Targa Resources Partners LP (NYSE: NGLS), which TRC consolidates, is a separate listed partnership: its unit prices and "
             "per-unit figures are never used."),
    "ticker": "TRGP",
    "sources": SRC,
    "listing": {"first_trading_day": "2010-12-07", "exchange": "NYSE", "symbol": "TRGP", "published": SRC["TG1"]["published"],
                "source": "TG1",
                "note": (f"FY2010 10-K, Item 5: '{LISTING_Q}' The IPO prospectus (424B1 of 2010-12-07): '{NOMARKET_Q}' The FY2010 10-K's "
                         f"cover: '{NOTPUB_Q}' The P/E exists only from the first trading day (the listing rule of method r2); Yahoo's "
                         "TRGP series starts on 2010-12-07 and records no split or distribution"),
                "partnership": f"'{NGLS_Q}' (the IPO prospectus): a different security, not substituted",
                "eps_note": f"'{NOEPS_Q}' '{CONV_Q}' (FY2010 10-K)"},
    "distributions": [],
    "history_vintages": vintages,
    "prints": prints,
    "guides": guides,
    "dividends": dividends,
    "events": [],
    "company_names": [],
    "buyback_programs": [],
    "rule_t": rule_t,
}
out = A.out or os.path.join(REPO, "retro", "facts", "TRGP.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(facts, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_trgp.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump(CHECK, fh, ensure_ascii=False, indent=1)
print(out, len(prints), "prints", len(vintages), "vintages", sum(len(v) for v in CHECK.values()), "checked strings")
for k, v in rule_t.items():
    print(k, v["values"], v["thresholds"])
