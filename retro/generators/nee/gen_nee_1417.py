#!/usr/bin/env python3
"""Extend retro/facts/NEE.json with 2014-2017 (filings accepted 2014-01-01 to 2017-12-31), asserting that every earlier fact is
unchanged. The discipline of the 2008-2013 sheet (retro/README.md, "NEE", "NEE 2010-2013"): each figure from its own row by label
under an anchored heading, the segment columns asserted to sum to NextEra Energy's total, every growth rate, margin and margin change
computed, every quote asserted present in its own filing, and a verbatim checklist written. Run:

    python3 retro/tools/edgar.py index 753308 <dir>
    python3 retro/tools/edgar.py fetch 753308 <dir> --from 2014-01-01 --to 2017-12-31 --forms 8-K 8-K/A 10-K 10-K/A
    python3 retro/tools/edgar.py fetch 753308 <dir> --from 2007-01-01 --to 2010-12-31 \\
        --acc 0000753308-07-000016 0000753308-08-000003 0000753308-09-000025 0000753308-10-000025   # first-year share counts
    python3 -I retro/generators/nee/gen_nee_1417.py --filings <dir> [--facts-in <2008-2013 sheet>] [--out retro/facts/NEE.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_nee_1417.json

--facts-in is the 2008-2013 sheet (default: retro/facts/NEE.json, which must then hold 2008-2013 only; the generator refuses a sheet
that already holds a 2014 fact). The 2008-2013 generator was not committed; this one only appends.
"""
import argparse
import copy
import datetime as dt
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))       # retro/generators/nee -> the repository
_ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("--filings", required=True, help="folder edgar.py wrote (allrows.json, tenk/, eightk/); keep it outside the repo")
_ap.add_argument("--facts-in", help="the 2008-2013 fact sheet to extend (default retro/facts/NEE.json)")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/NEE.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_nee_1417.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402

ET = ZoneInfo("America/New_York")
CUT = "2017-12-31"
FILINGS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("NEE")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
CHECK = {}
TEXT = {}
norm = lambda s: re.sub(r"\s+", " ", s).strip()
FACTS = A.out or os.path.join(REPO, "retro", "facts", "NEE.json")
old = json.load(open(A.facts_in or os.path.join(REPO, "retro", "facts", "NEE.json"), encoding="utf-8"))
assert max(p["published"] for p in old["prints"]) < "2014-01-01", "the input sheet already holds 2014 facts"
f = copy.deepcopy(old)


def doc(acc, prefix):
    for d in ("tenk", "tenq", "eightk"):
        p = os.path.join(SP, d, acc)
        if os.path.isdir(p):
            hits = sorted(x for x in os.listdir(p) if x.startswith(prefix) and x.endswith(".rows.txt"))
            assert hits, (acc, prefix)
            return os.path.join(p, max(hits, key=lambda x: os.path.getsize(os.path.join(p, x))))
    raise AssertionError(acc)


def lines(path):
    if path not in TEXT:
        TEXT[path] = [norm(x) for x in open(path, encoding="utf-8", errors="replace").read().split("\n")]
    return TEXT[path]


def quote(path, s):
    assert norm(s) in norm(" ".join(lines(path))), (path, s[:120])
    CHECK.setdefault(path, []).append(s)
    return s


def find(path, pattern):
    """The first match of a regular expression in the filing's text (rows joined), recorded for verbatim.py."""
    m = re.search(pattern, " ".join(lines(path)))
    assert m, (path, pattern)
    return quote(path, m.group(0))


def num(tok):
    t = tok.strip().replace("$", "").replace(",", "").strip()
    if t in ("—", "-", "–", ""):
        return 0.0
    neg = t.startswith("(")
    v = float(t.strip("() "))
    return -v if neg else v


def safe(t):
    try:
        return num(t)
    except ValueError:
        return None


def strip_pct(x):
    """Drop the percentage cells of a statistics row: '3.9%', '—%' and the split negatives '(5.2 | )%'."""
    x = re.sub(r"\|\s*\(\s*[\d.,]+\s*\|\s*\)%", "", x)
    return re.sub(r"\|\s*[-\d.,—–]*%", "", x)


def vals(path, x, pct=False):
    CHECK.setdefault(path, []).append(x)
    v = [safe(t) for t in (strip_pct(x) if pct else x).split("|")[1:]]
    assert None not in v, (path, x)
    return v


def first(path, start, stop, test):
    L = lines(path)
    for i in range(start, stop):
        if test(L[i]):
            return i, L[i]
    raise AssertionError((path, start, stop))


def published(acc):
    r = FILINGS[acc]
    t = dt.datetime.fromisoformat(r[1].replace("Z", "+00:00")).astimezone(ET)
    d = t.date().isoformat()
    assert d <= CUT, acc
    hm = t.strftime("%H:%M")
    if hm >= "16:00":
        return min(x for x in TDAYS if x > d), f"{d} {hm} ET (after the close)"
    if hm < "09:30":
        return d, f"{d} {hm} ET (before the open)"
    return d, f"{d} {hm} ET (during the session)"


URL = lambda acc, fn: f"https://www.sec.gov/Archives/edgar/data/753308/{acc.replace('-', '')}/{fn}"
SRC = {}
nid = [1 + max(int(k[2:]) for k in old["sources"])]


def source(acc, title, fn, supports):
    p, filed = published(acc)
    sid = f"NE{nid[0]}"
    nid[0] += 1
    SRC[sid] = dict(published=p, filed=filed, title=title, url=URL(acc, fn), supports=supports)
    return sid


fname = lambda path: path.split("__", 1)[1][: -len(".rows.txt")]
r1 = lambda x: round(x + 0.0, 1)
r2 = lambda x: round(x + 0.0, 2)
pct = lambda a, b: (b / a - 1) * 100

# ── filings, in publication order ───────────────────────────────────────────────────────────────────────────────────────
TENK = {2013: "0000753308-14-000025", 2014: "0000753308-15-000079", 2015: "0000753308-16-000337", 2016: "0000753308-17-000060"}
REL = {"Q4 2013": "0000753308-14-000003", "Q1 2014": "0000753308-14-000031", "Q2 2014": "0000753308-14-000069",
       "Q3 2014": "0000753308-14-000096", "Q4 2014": "0000753308-15-000006", "Q1 2015": "0000753308-15-000163",
       "Q2 2015": "0000753308-15-000203", "Q3 2015": "0000753308-15-000246", "Q4 2015": "0000753308-16-000277",
       "Q1 2016": "0000753308-16-000369", "Q2 2016": "0000753308-16-000400", "Q3 2016": "0000753308-16-000437",
       "Q4 2016": "0000753308-17-000003", "Q1 2017": "0000753308-17-000079", "Q2 2017": "0000753308-17-000106",
       "Q3 2017": "0000753308-17-000139"}
# the first year of each new vintage's ten: its diluted shares from the earliest 10-K whose income statement reports it (the
# earlier vintages' encoding: 2003 from the FY2005 10-K), already in the sheet as sources
FIRST_SHARES = {2013: (2004, "NE9", "0000753308-07-000016"), 2014: (2005, "NE10", "0000753308-08-000003"),
                2015: (2006, "NE11", "0000753308-09-000025"), 2016: (2007, "NE32", "0000753308-10-000025")}
K_SRC = {fy: source(acc, f"NextEra Energy FY{fy} Form 10-K", FILINGS[acc][4],
                    f"FY{fy} annual report (combined filing with Florida Power & Light Company)") for fy, acc in TENK.items()}
R_SRC = {}
for q, acc in REL.items():
    R_SRC[q] = source(acc, f"NextEra Energy {q} results (8-K, Exhibit 99)", fname(doc(acc, "EX-99")),
                      f"{q} earnings release: segment statements of income, earnings per share, FPL statistics, outlook")
G8K = {"2014-06-19": "0000753308-14-000053", "2014-09-02": "0000753308-14-000083", "2015-03-11": "0000753308-15-000086",
       "2015-03-31": "0000753308-15-000126", "2015-06-16": "0000753308-15-000195", "2015-09-28": "0000753308-15-000239",
       "2016-03-02": "0000753308-16-000341"}
G_SRC = {d: source(acc, f"NextEra Energy 8-K of {d} (Item 7.01)", FILINGS[acc][4],
                   "adjusted earnings per share expectations (Regulation FD disclosure)") for d, acc in G8K.items()}
# the source ids run in publication order within each kind, as in the 2010-2013 sheet (10-Ks, releases, guidance 8-Ks)

# ── prints ───────────────────────────────────────────────────────────────────────────────────────────────────────────────
HEAD = re.compile(r"^(Three|Twelve) Months Ended (\w+ \d+, (\d{4})) \| (Florida Power|FPL \|)")


def statement(path, kind, year):
    """One segment statement of income ('Three' or 'Twelve' months ended in `year`): NextEra Energy's figures and FPL's and NEER's
    net income, read row by row between its header and its weighted-average share count."""
    L = lines(path)
    hs = [i for i, x in enumerate(L) if HEAD.match(x) and HEAD.match(x).group(1) == kind and HEAD.match(x).group(3) == str(year)
          and L[i + 1].startswith("Operating Revenues |")]                # the statement of income, not the cash flows
    assert len(hs) == 1, (path, kind, year, hs)
    h = hs[0]
    cols = [c.strip() for c in L[h].split("|")[1:]]
    assert (cols[0].startswith("Florida Power") or cols[0] == "FPL") and cols[1] == "NEER" and cols[2].startswith("Corporate") and \
        cols[3].replace(" ", "").startswith("NextEraEnergy"), (path, cols)
    CHECK.setdefault(path, []).append(L[h])
    end, _ = first(path, h, len(L), lambda x: x.startswith("Weighted-average shares outstanding (assuming dilution) |"))
    g = lambda test: vals(path, first(path, h, end, test)[1])
    rev = g(lambda x: x.startswith("Operating Revenues |"))
    opi = g(lambda x: re.match(r"Operating Income( \(Loss\))? \|", x))
    pre = g(lambda x: re.match(r"Income( \(Loss\))?( from Continuing Operations)? before Income Taxes \|", x))
    tax = g(lambda x: re.match(r"Income Tax(es| Expense \(Benefit\)) \|", x))
    ni = g(lambda x: re.match(r"Net Income( \(Loss\))? \|", x))
    att = [x for x in lines(path)[h:end] if re.match(r"Net Income( \(Loss\))? Attributable to NextEra Energy, Inc\. \|", x)]
    na = vals(path, att[0]) if att else ni
    for v in (rev, opi, pre, tax, ni, na):
        assert len(v) == 4 and abs(v[0] + v[1] + v[2] - v[3]) <= 1, (path, "segments must sum to the total", v)
    ie, eps_row = first(path, h, end, lambda x: x.startswith("Earnings") and "Per Share" in x and "(assuming dilution)" in x)
    ia, adj_row = first(path, ie, end, lambda x: x.startswith("Adjusted Earnings") and "Per Share |" in x)
    items = []
    for x in lines(path)[ie + 1:ia]:
        if "|" in x and not x.startswith("Adjustments"):
            v = vals(path, x)
            items.append((re.sub(r"\(\d\)", "", x.split("|")[0]).strip(), v[-1]))
    sh = vals(path, lines(path)[end])
    assert len(sh) == 1
    return dict(rev=rev[3], opinc=opi[3], pretax=pre[3], tax=tax[3], fpl_ni=ni[0], neer_ni=na[1], ni=na[3],
                eps=vals(path, eps_row)[3], adj=vals(path, adj_row)[3], items=items, shares=sh[0], nci=bool(att))


def stats(path):
    """FPL's statistics table: energy sales 'Total' (million kWh) and average customer accounts 'Total' (thousands), the quarter's
    and the year-ago quarter's, and for a Q4 release the year to date too."""
    L = lines(path)
    s, _ = first(path, 0, len(L), lambda x: x == "Statistics")
    e, _ = first(path, s, len(L), lambda x: x == "Energy sales (million kWh)")
    i, _ = first(path, e, len(L), lambda x: x.startswith("Interchange power sales |"))
    kwh = vals(path, L[i + 1], pct=True)
    assert L[i + 1].startswith("Total |") and vals(path, L[i - 1], pct=True)[0] + vals(path, L[i], pct=True)[0] + \
        vals(path, L[i - 2], pct=True)[0] == kwh[0], (path, "energy sales: retail + electric utilities + interchange = total")
    c, _ = first(path, e, len(L), lambda x: x == "Average customer accounts (000s)")
    _, crow = first(path, c, c + 8, lambda x: x.startswith("Total |"))
    return kwh, vals(path, crow, pct=True)


def year_ago_release(fy, q):
    """The release date of the same quarter a year earlier (old sheet or this one): when the next print is likely due."""
    for p in old["prints"] + new_prints:
        if p["fy"] == fy - 1 and p["q"] == q:
            return p["release"]
    raise AssertionError((fy, q))


def when(day):
    d = int(day[8:])
    return f"{'early' if d <= 10 else 'mid' if d <= 20 else 'late'} {dt.date.fromisoformat(day).strftime('%B')}"


usd = lambda v: f"-${-v:.2f}" if v < 0 else f"${v:.2f}"


def eps_words(s, sp):
    """The note on the EPS signal: GAAP as reported, and what the release's adjusted figure removes, as its reconciliation lists it."""
    listed = []
    for (lab, v), (_, v0) in zip(s["items"], sp["items"]) if [a for a, _ in s["items"]] == [a for a, _ in sp["items"]] else []:
        if v or v0:
            listed.append(f"{lab} {usd(v)} and {usd(v0)}")
    if not listed:
        listed = [f"{lab} {usd(v)}" for lab, v in s["items"] if v] + [f"{lab} {usd(v)} a year earlier" for lab, v in sp["items"] if v]
    return (f"diluted EPS as reported ${s['eps']:.2f} vs ${sp['eps']:.2f}; the release's adjusted EPS (${s['adj']:.2f} vs "
            f"${sp['adj']:.2f}) removes, per share, {'; '.join(listed)}; as it also removes the mark-to-market effect of non-qualifying "
            "hedges, a recurring item, GAAP stands (the PEP 2008 core rule)")


new_prints = []
for q, acc in REL.items():
    path = doc(acc, "EX-99")
    qn, fy = int(q[1]), int(q[3:])
    pub, filed = published(acc)
    assert filed.endswith("(before the open)"), (q, filed)
    s, sp = statement(path, "Three", fy), statement(path, "Three", fy - 1)
    kwh, cust = stats(path)
    raw = dict(rev_m=s["rev"], rev_prior_m=sp["rev"], opinc_m=s["opinc"], opinc_prior_m=sp["opinc"], seg_m=s["fpl_ni"],
               seg_prior_m=sp["fpl_ni"], kwh_m=kwh[0], kwh_prior_m=kwh[1], ni_m=s["ni"], ni_prior_m=sp["ni"], fple_m=s["neer_ni"],
               fple_prior_m=sp["neer_ni"], cust_k=cust[0], cust_prior_k=cust[1])
    m, m0 = raw["opinc_m"] / raw["rev_m"] * 100, raw["opinc_prior_m"] / raw["rev_prior_m"] * 100
    gp = lambda a, b: r1(pct(a, b)) if a > 0 else r1((b - a) / abs(a) * 100)
    nq = qn % 4 + 1
    p = dict(quarter=q, fy=fy, q=qn, published=pub, filed=filed, release_time="before the open", release=pub, source=R_SRC[q], raw=raw,
             sales_b=round(raw["rev_m"] / 1000, 3), sales_pct=r1(pct(raw["rev_prior_m"], raw["rev_m"])),
             kwh_pct=r1(pct(raw["kwh_prior_m"], raw["kwh_m"])), seg_pct=gp(raw["seg_prior_m"], raw["seg_m"]),
             margin=r2(m), margin_prior=r2(m0), margin_bp=r1((m - m0) * 100),
             eps_q=s["eps"], eps_q_prior=sp["eps"], eps_pct=gp(sp["eps"], s["eps"]), eps_basis="GAAP", eps_gaap=s["eps"],
             eps_gaap_prior=sp["eps"], eps_adj=s["adj"], eps_adj_prior=sp["adj"], diluted_shares_m=s["shares"], resources_name="NEER",
             eps_note=eps_words(s, sp),
             next_print=f"Q{nq} {fy + (1 if qn == 4 else 0)} print ({when(year_ago_release(fy + (1 if qn == 4 else 0), nq))})")
    if qn == 4:
        y, y0 = statement(path, "Twelve", fy), statement(path, "Twelve", fy - 1)
        lab = f"FY{fy % 100:02d}"
        mm = y["opinc"] / y["rev"] * 100
        disc = [v for lab_, v in y["items"] if "discontinued" in lab_.lower() and v]
        p["fy_actual"] = dict(
            fy=fy, fy_label=lab, eps_normalized=y["eps"], revenue_usd_b=round(y["rev"] / 1000, 3), diluted_shares_m=y["shares"],
            normalization_note=(f"{lab} ${y['eps']:.2f} from the {q} release ({R_SRC[q]}): diluted EPS as reported"
                                + (f" (net income, the gain from discontinued operations of ${-disc[0]:.2f} a share in, as the "
                                   "release prints no EPS without it)" if disc else "")
                                + f"; the release's adjusted ${y['adj']:.2f} also removes recurring mark-to-market items, so GAAP "
                                "stands; the 10-K's figure replaces it"),
            margin=r2(mm), margin_note=f"{lab} operating margin {mm:.2f}%: operating income ${y['opinc']:,.0f}M on ${y['rev']:,.0f}M ({R_SRC[q]})",
            check_pretax_margin=r2(y["pretax"] / y["rev"] * 100),
            check_pretax_note=f"{lab} income before income taxes ${y['pretax']:,.0f}M on ${y['rev']:,.0f}M ({R_SRC[q]}; display only)",
            tax_rate=round(y["tax"] / y["pretax"], 3), tax_note=f"{lab} income taxes ${y['tax']:,.0f}M on pre-tax ${y['pretax']:,.0f}M (display only)",
            sales_growth=r1(pct(y0["rev"], y["rev"])), kwh_pct=r1(pct(kwh[3], kwh[2])), seg_pct=r1(pct(y0["fpl_ni"], y["fpl_ni"])),
            customers_k=cust[2], customers_pct=r1(pct(cust[3], cust[2])),
            raw=dict(rev_m=y["rev"], rev_prior_m=y0["rev"], opinc_m=y["opinc"], pretax_m=y["pretax"], tax_m=y["tax"], seg_m=y["fpl_ni"],
                     seg_prior_m=y0["fpl_ni"], kwh_m=kwh[2], kwh_prior_m=kwh[3], eps_adj=y["adj"], cust_k=cust[2], cust_prior_k=cust[3]))
    new_prints.append(p)

# ── vintages: the FY2013-FY2016 10-Ks ──────────────────────────────────────────────────────────────────────────────────────
V = []
prev = old["history_vintages"][-1]
for fy, acc in TENK.items():
    path = doc(acc, "10-K")
    L = lines(path)
    sid = K_SRC[fy]
    pub = SRC[sid]["published"]
    s6 = max(i for i, x in enumerate(L) if x == "Item 6. Selected Financial Data")
    s7, _ = first(path, s6, len(L), lambda x: x.startswith("Item 7."))
    i, hdr = first(path, s6, s7, lambda x: re.match(r"^20\d\d \| 20\d\d \| 20\d\d \| 20\d\d \| 20\d\d$", x))
    years = [int(t) for t in hdr.split(" | ")]
    assert years == list(range(fy, fy - 5, -1)), (fy, years)
    CHECK.setdefault(path, []).append(hdr)
    sel_rev = vals(path, first(path, s6, s7, lambda x: x.startswith("Operating revenues |"))[1])
    ih, _ = first(path, s6, s7, lambda x: re.match(r"^Earnings per share .*assuming dilution:$", x))
    sel_eps = vals(path, first(path, ih, ih + 3, lambda x: x.startswith("Net income"))[1])
    ihc, _ = first(path, ih, ih + 3, lambda x: x.startswith("Continuing operations"))
    sel_cont = vals(path, lines(path)[ihc])
    # the NEE statements of income, cash flows; then FPL's statement of income
    io, x = first(path, s7, len(L), lambda x: x.startswith("OPERATING REVENUES |"))
    rev3 = vals(path, x)
    end_is, _ = first(path, io, len(L), lambda x: x.startswith("Weighted-average number of common shares outstanding:"))
    opinc = vals(path, first(path, io, end_is, lambda x: x.startswith("OPERATING INCOME |"))[1])
    pretax = vals(path, first(path, io, end_is, lambda x: re.match(r"INCOME (FROM CONTINUING OPERATIONS )?BEFORE INCOME TAXES \|", x))[1])
    tax = vals(path, first(path, io, end_is, lambda x: x.startswith("INCOME TAXES |"))[1])
    shares = vals(path, first(path, end_is, end_is + 3, lambda x: x.startswith("Assuming dilution |"))[1])
    ic, _ = first(path, end_is, len(L), lambda x: x.startswith("Net cash provided by operating activities |"))
    ocf = vals(path, L[ic])
    ce = [vals(path, first(path, ic, ic + 12, lambda x, lab=lab: x.startswith(lab))[1])[0] for lab in
          ("Capital expenditures of FPL |", "Independent power and other investments of NEER |", "Nuclear fuel purchases |",
           "Other capital expenditures and other investments |")]
    ie_, _ = first(path, ic, len(L), lambda x: x.startswith("Cash and cash equivalents at end of year |"))
    cash = vals(path, L[ie_])
    issu = vals(path, first(path, ic, ie_, lambda x: x.startswith("Issuances of common stock - net |"))[1])
    rep = [x for x in L[ic:ie_] if x.startswith("Repurchases of common stock |")]
    repv = vals(path, rep[0]) if rep else [0.0]
    divs = vals(path, first(path, ic, ie_, lambda x: x.startswith("Dividends on common stock |"))[1])
    ifpl, _ = first(path, ie_, len(L), lambda x: x.startswith("OPERATING REVENUES |"))
    fpl_ni3 = vals(path, first(path, ifpl, ifpl + 25, lambda x: x.startswith("NET INCOME"))[1])
    # FPL's selected data: net income, energy sales and average customer accounts (the FY2016 10-K no longer tabulates them)
    fs = [i for i in range(s6, s7) if L[i].startswith("SELECTED DATA OF FPL")]
    q4 = [p for p in new_prints if p["quarter"] == f"Q4 {fy}"][0]
    if fs:
        kwh = vals(path, first(path, fs[0], s7, lambda x: x.startswith("Energy sales (kWh) |"))[1])
        fni = vals(path, first(path, fs[0], s7, lambda x: x.startswith("Net income |"))[1])
        ia_, _ = first(path, fs[0], s7, lambda x: x.startswith("Average number of customer accounts"))
        cus = vals(path, first(path, ia_, ia_ + 8, lambda x: x.startswith("Total |"))[1])
        assert fni[:2] == fpl_ni3[:2], (fy, "FPL's net income: selected data and statement")
        kwh_src, kwh_note = sid, ""
    else:
        a = q4["fy_actual"]["raw"]
        kwh, cus, fni = [a["kwh_m"], a["kwh_prior_m"]], [a["cust_k"], a["cust_prior_k"]], fpl_ni3
        kwh_src = q4["source"]
        kwh_note = (f"; the FY{fy} 10-K no longer tabulates FPL's energy sales or customer accounts, so they come from the Q4 {fy} "
                    f"release ({kwh_src})")
    # the segment note: operating revenues by segment for three years (FPL, NEER, Corporate and Other, NEE)
    _, sg = first(path, s7, len(L), lambda x: x.startswith("Operating revenues |") and len(x.split("|")) == 13
                  and safe(x.split("|")[1]) not in (None, 0.0))
    seg = vals(path, sg)
    for k in range(3):
        assert seg[4 * k] + seg[4 * k + 1] + seg[4 * k + 2] == seg[4 * k + 3] == rev3[k], (fy, "segment revenues sum", k)
    assert rev3[:2] == sel_rev[:2] and opinc and sel_eps[0] == q4["fy_actual"]["eps_normalized"], fy
    # ten fiscal years to the latest: the new 10-K's five, the earlier years as the previous vintage holds them
    keep = [y for y in range(fy - 9, fy - 4)]
    eps = {str(y): prev["eps_normalized"][str(y)] for y in keep}
    eps.update({str(y): v for y, v in zip(years, sel_eps)})
    eps = dict(sorted(eps.items()))
    rev = {str(y): prev["revenue_usd_b"][str(y)] for y in keep}
    rev.update({str(y): round(v / 1000, 3) for y, v in zip(years, sel_rev)})
    rev = dict(sorted(rev.items()))
    es = {str(y): prev["eps_sources"][str(y)] for y in keep} | {str(y): sid for y in years}
    ep = {str(y): prev["eps_published"][str(y)] for y in keep} | {str(y): pub for y in years}
    rs = {str(y): prev["revenue_sources"][str(y)] for y in keep} | {str(y): sid for y in years}
    y0, s0, acc0 = FIRST_SHARES[fy]
    p0 = doc(acc0, "10-K")
    j, _ = first(p0, 0, len(lines(p0)), lambda x: x == "Weighted-average number of common shares outstanding:")
    sh0 = vals(p0, first(p0, j, j + 3, lambda x: x.startswith("Assuming dilution |"))[1])
    first_sh = sh0[2]                                              # the third column: the year two before that 10-K's
    assert y0 == fy - 9 and old["sources"][s0]["published"] < pub
    lab = f"FY{fy % 100:02d}"
    disc = [y for y, a, b in zip(years, sel_eps, sel_cont) if a != b]
    eps_text = "; ".join(f"{y} ${eps[y]:.2f} ({es[y]})" for y in eps)
    # the dividend sentence, the business and risk-factor quotes, the energy-transition quotes
    dq = find(path, r"In February " + str(fy + 1) + r", NEE announced that it would increase its quarterly dividend on its common stock "
              r"from \$[\d.]+ per share to \$[\d.]+ per share\.")
    rate = float(re.findall(r"\$([\d.]+) per share\.", dq)[0])
    fq = find(path, r"(FPL was incorporated under the laws of Florida in 1925 and )?(FPL )?is a rate-regulated electric utility engaged "
              r"primarily in the generation, transmission, distribution and sale of electric energy in Florida\.")
    nq_ = find(path, r"NEER produces the majority of its electricity from clean and renewable sources(, including wind and solar\.)?")
    rq = [find(path, r"NEE's and FPL's business, financial condition, results of operations and prospects may be (materially )?adversely affected by "
               r"the extensive regulation of their business\."),
          find(path, r"NEE's and FPL's business, financial condition, results of operations and prospects can be materially adversely "
               r"affected by weather conditions, including, but not limited to, the impact of severe weather\."),
          find(path, r"NEE's and FPL's business could be negatively affected by federal or state laws or regulations mandating new or "
               r"additional limits on the production of greenhouse gas emissions\.")]
    assert "cyclical" not in " ".join(L).lower(), (fy, "a 10-K calls the business cyclical: decide its encoding first")
    why = (f"NextEra Energy, Inc.: '{fq}' and '{nq_}'; among its risk factors, '{rq[0]}', '{rq[1]}' and '{rq[2]}' "
           f"(its own FY{fy} 10-K)")
    v = dict(published=pub, sources=list(dict.fromkeys([sid] + [es[y] for y in eps] + [s0])), company="NextEra Energy, Inc.",
             exchange="NYSE", business_line=prev["business_line"], fy_label=lab,
             fiscal_year_ends={y: f"{y}-12-31" for y in eps}, eps_normalized=eps, eps_sources=es, eps_published=ep,
             normalization=(f"GAAP diluted EPS before the cumulative effect of accounting changes, each year from the latest 10-K that "
                            f"reports it: {eps_text}"
                            + (f". {', '.join(map(str, disc))}: EPS on net income attributable to NEE, the gain from discontinued "
                               "operations in (the 10-K's continuing operations figure"
                               + "".join(f" for {y} is ${c:.2f}" for y, a, c in zip(years, sel_eps, sel_cont) if a != c)
                               + ", display only; the NEE rule's line is before the cumulative effect, which discontinued operations "
                               "sit above)" if disc else "")
                            + ". From 2001 the company's figures without its listed items also remove the mark-to-market effect of "
                            "non-qualifying hedges, a recurring item, so GAAP stands (the PEP 2008 core rule)"),
             revenue_usd_b=rev, revenue_sources=rs, diluted_shares_m={str(y0): first_sh, str(fy): shares[0]},
             shares_published={str(y0): old["sources"][s0]["published"], str(fy): pub},
             shares_note=(f"{y0}: {first_sh}M ({s0}, the income statement's diluted weighted-average shares); {fy}: {shares[0]}M diluted "
                          f"({sid})"),
             pe_window_start=None, prev_fy_margin=r2(opinc[0] / rev3[0] * 100),
             prev_fy_margin_note=(f"{lab} operating margin {opinc[0] / rev3[0] * 100:.2f}%: operating income ${opinc[0]:,.0f}M on "
                                  f"operating revenues ${rev3[0]:,.0f}M ({sid})"),
             check_pretax_margin=r2(pretax[0] / rev3[0] * 100),
             check_pretax_note=f"{lab} income before income taxes ${pretax[0]:,.0f}M on ${rev3[0]:,.0f}M ({sid}; display only)",
             tax_rate=round(tax[0] / pretax[0], 3), tax_note=f"{lab} income taxes ${tax[0]:,.0f}M on pre-tax ${pretax[0]:,.0f}M ({sid}; display only)",
             prev_fy_sales_growth=r1(pct(rev3[1], rev3[0])), prev_fy_kwh_pct=r1(pct(kwh[1], kwh[0])),
             prev_fy_seg_pct=r1(pct(fni[1], fni[0])), prev_fy_customers_k=cus[0], prev_fy_customers_pct=r1(pct(cus[1], cus[0])),
             dividend_annual=round(rate * 4, 4), dividend_note=f"'{dq}' ({sid})", cash_b=round(cash[0] / 1000, 3),
             fcf_b=round((ocf[0] + sum(ce)) / 1000, 3), fcf_label=lab,
             fcf_note=(f"net cash provided by operating activities ${ocf[0]:,.0f}M less the cash flow statement's capital expenditures of "
                       f"FPL, independent power and other investments of NEER, nuclear fuel purchases and other capital expenditures "
                       f"(${-sum(ce):,.0f}M, their sum) ({sid})"),
             cash_return_text=(f"issuances of common stock ${issu[0]:,.0f}M, "
                               + (f"repurchases of common stock ${-repv[0]:,.0f}M and " if repv[0] else "no repurchases of common stock and ")
                               + f"dividends on common stock ${-divs[0]:,.0f}M in {fy} ({sid} cash flows): the dividend is most of the return"),
             groups=[["FPL", round(seg[0] / 1000, 3), r1(pct(seg[4], seg[0]))],
                     ["NextEra Energy Resources", round(seg[1] / 1000, 3), r1(pct(seg[5], seg[1]))],
                     ["Corporate and Other", round(seg[2] / 1000, 3), r1(pct(seg[6], seg[2]))]],
             groups_basis=f"{lab} operating revenues by segment ({sid}, segment information)",
             margin_signal_name="Operating margin change", why=why,
             raw=dict(kwh=[kwh[1], kwh[0]], seg=[fni[1], fni[0]], opinc=opinc[0], rev=rev3[0], pretax=pretax[0], tax=tax[0], ocf=ocf[0],
                      capex=ce, cash=cash[0], segrev=seg, customers=[cus[0], cus[1]]))
    assert -repv[0] < -divs[0], fy
    if kwh_note:                  # display only: the franchise line says where FPL's energy sales and customers come from
        v["franchise_note"] = kwh_note[2:]
    if fy >= 2014:      # ENERGY_TRANSITION (live from 2015-12-12): the company's own words on its gas reserves and the GHG limits
        v["reserves_quote"] = find(path, r"NEER's oil and gas production assets, representing approximately [^.]*\.")
        v["transition_quote"] = find(path, r"While NEE's and FPL's electric generati\w+ units emit greenhouse gases at a lower rate of "
                                     r"emissions than most of the U\.S\. electric generation sector, the results of operations of NEE "
                                     r"and FPL could be materially adversely affected to the extent that new federal or state laws or "
                                     r"regulations impose any new greenhouse gas emission limits\.")
    V.append(v)
    prev = v

# ── guides: every expectation of 2014-2017 is adjusted earnings per share (display only, the PEP 2008 core rule) ──────────────
UNUSED = old["guides"][-1]["unused"]
G = [  # (fy, published, source, doc, the quote: the current year's sentence or clause only)
    (2014, "Q4 2013", "NextEra Energy expects adjusted earnings per share for 2014 to be in the range of $5.05 to $5.45"),
    (2014, "Q1 2014", "NextEra Energy continues to expect adjusted earnings per share for 2014 to be in the range of $5.05 to $5.45"),
    (2014, "2014-06-19", "reaffirmed its previously disclosed 2014 adjusted earnings per share expectations of $5.05 to $5.45"),
    (2014, "Q2 2014", "NextEra Energy now expects adjusted earnings per share for 2014 to be in the range of $5.15 to $5.35"),
    (2014, "2014-09-02", "reaffirmation of its previously disclosed 2014 adjusted earnings per share expectations of $5.15 to $5.35"),
    (2014, "Q3 2014", "NextEra Energy continues to expect full-year 2014 adjusted earnings per share to be in the range of $5.15 to $5.35"),
    (2015, "Q3 2014", "For 2015, the company expects full-year adjusted earnings per share to be in the range of $5.40 to $5.70"),
    (2015, "Q4 2014", "NextEra Energy continues to expect full-year 2015 adjusted earnings per share to be in the range of $5.40 to $5.70"),
    (2015, "2015-03-11", "2015 | $5.40 - $5.70"),
    (2015, "2015-03-31", "2015 | $5.40 - $5.70"),
    (2015, "Q1 2015", "NextEra Energy continues to expect full-year 2015 adjusted earnings per share to be in the range of $5.40 to $5.70"),
    (2015, "2015-06-16", "2015 | $5.40 - $5.70"),
    (2015, "Q2 2015", "NextEra Energy continues to expect full-year 2015 adjusted earnings per share to be in the range of $5.40 to $5.70"),
    (2015, "2015-09-28", "2015 | $5.40 - $5.70"),
    (2015, "Q3 2015", "NextEra Energy expects full-year 2015 adjusted earnings per share to be in the upper half of the range of $5.40 to $5.70"),
    (2016, "Q4 2015", "NextEra Energy continues to expect adjusted earnings per share to be in the range of $5.85 to $6.35 for 2016"),
    (2016, "2016-03-02", "2016 | $5.85 - $6.35"),
    (2016, "Q1 2016", "NextEra Energy continues to expect adjusted earnings per share to be in the range of $5.85 to $6.35 for 2016"),
    (2016, "Q2 2016", "NextEra Energy continues to expect adjusted earnings per share to be in the range of $5.85 to $6.35 for 2016"),
    (2016, "Q3 2016", "NextEra Energy continues to expect adjusted earnings per share to be in the range of $5.85 to $6.35 for 2016"),
    (2017, "Q4 2016", "NextEra Energy expects adjusted earnings per share to be in the range of $6.35 to $6.85 for 2017"),
    (2017, "Q1 2017", "NextEra Energy continues to expect adjusted earnings per share to be in the range of $6.35 to $6.85 for 2017"),
    (2017, "Q2 2017", "NextEra Energy continues to expect adjusted earnings per share to be in the range of $6.35 to $6.85 for 2017"),
    (2017, "Q3 2017", "NextEra Energy continues to expect adjusted earnings per share to be in the range of $6.35 to $6.85 for 2017"),
]
new_guides = []
for fy, key, text in G:
    if key in REL:
        acc, sid, d = REL[key], R_SRC[key], f"{key} release"
        path = doc(acc, "EX-99")
    else:
        acc, sid, d = G8K[key], G_SRC[key], f"8-K of {key}"
        path = doc(acc, "8-K")
    quote(path, text)
    other = {int(y) for y in re.findall(r"\b(20\d\d)\b", text)} - {fy}
    assert not other, (key, "a guide quote names another year", other)
    disp = f"'{text}'" if "|" not in text else f"the table row '{text}' (adjusted earnings per share expectations for {fy})"
    new_guides.append(dict(fy=fy, published=SRC[sid]["published"], source=sid, doc=d, display=disp, unused=UNUSED))
new_guides.sort(key=lambda g: (g["published"], g["fy"]))

# ── checks: each Q4 print's full year equals the 10-K that follows it (EPS and revenue; shares to the release's rounding) ──────
for p in new_prints:
    a = p.get("fy_actual")
    if a:
        v = [x for x in V if x["fy_label"] == a["fy_label"]][0]
        y = str(a["fy"])
        assert (v["eps_normalized"][y], v["revenue_usd_b"][y]) == (a["eps_normalized"], a["revenue_usd_b"]), (p["quarter"], "Q4 vs 10-K")
        assert abs(v["diluted_shares_m"][y] - a["diluted_shares_m"]) < 0.5, p["quarter"]
assert [p["published"] for p in old["prints"] + new_prints] == sorted(p["published"] for p in old["prints"] + new_prints)

# ── assemble: the earlier facts unchanged ────────────────────────────────────────────────────────────────────────────────
for k in SRC:
    assert k not in f["sources"]
f["sources"].update(SRC)
f["history_vintages"] += V
f["prints"] += new_prints
f["guides"] += new_guides
for key in ("sources", "history_vintages", "prints", "guides"):
    n_old = len(old[key])
    got = list(f[key].items())[:n_old] if key == "sources" else f[key][:n_old]
    want = list(old[key].items()) if key == "sources" else old[key]
    assert got == want, key
for key in ("rule_t", "eps_guides", "dividends", "events", "company_names", "splits", "listings", "distributions", "price_basis", "ticker"):
    assert f[key] == old[key], key
f["_doc"] = old["_doc"] + (
    " 2014-2017 (retro/README.md, 'NEE 2014-2017') was appended by retro/generators/nee/gen_nee_1417.py from the filings accepted "
    "2014-01-01 to 2017-12-31 (sources NE66 on), every earlier fact unchanged; from ENERGY_TRANSITION's live date the FY2014-FY2016 "
    "vintages carry their 10-K's words on NEER's oil and gas production assets and the greenhouse gas limits ('reserves_quote', "
    "'transition_quote').")
with open(FACTS, "w", encoding="utf-8") as fh:
    json.dump(f, fh, ensure_ascii=False, indent=1)
with open(A.checklist or os.path.join(SP, "checklist_nee_1417.json"), "w", encoding="utf-8") as fh:
    json.dump(CHECK, fh, ensure_ascii=False, indent=1)
print(len(SRC), "sources,", len(V), "vintages,", len(new_prints), "prints,", len(new_guides), "guides;",
      sum(len(v) for v in CHECK.values()), "checklist strings")
for p in new_prints:
    print(p["quarter"], p["published"], p["sales_pct"], p["kwh_pct"], p["seg_pct"], p["margin_bp"], p["eps_q"], p["eps_q_prior"],
          p["eps_pct"], p["diluted_shares_m"], p["next_print"], p.get("fy_actual", {}).get("eps_normalized"))
for v in V:
    print(v["published"], v["fy_label"], v["eps_normalized"], v["prev_fy_margin"], v["groups"], v["dividend_annual"], v["diluted_shares_m"])
for k, s in SRC.items():
    print(k, s["published"], s["filed"], s["title"][:60])
