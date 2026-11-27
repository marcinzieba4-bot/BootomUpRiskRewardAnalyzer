#!/usr/bin/env python3
"""Extend retro/facts/NEE.json with 2018-2021 (filings accepted 2018-01-01 to 2021-12-31), asserting that every earlier fact is
unchanged. The discipline of gen_nee_1417.py (retro/README.md, "NEE 2014-2017"): each figure from its own row by label under an
anchored heading, the segment columns (FPL, Gulf Power from 2019, NEER, Corporate and Other) asserted to sum to NextEra Energy's
total, every growth rate, margin and margin change computed, every quote asserted present in its own filing, and a verbatim checklist
written. New in 2018-2021 (retro/README.md, "NEE 2018-2021"): the releases no longer tabulate FPL's energy sales or customer
accounts (from the Q4 2017 release; asserted), so those figures are None (n/r); the FY2020 10-K omits Item 6, so its vintage takes
2018-2020 from its statements; the four-for-one split effective 2020-10-27 is a 'splits' record from the 8-K that states it. Run:

    python3 retro/tools/edgar.py index 753308 <dir>
    python3 retro/tools/edgar.py fetch 753308 <dir> --from 2018-01-01 --to 2021-12-31 --forms 8-K 8-K/A 10-K 10-K/A
    python3 retro/tools/edgar.py fetch 753308 <dir> --from 2011-01-01 --to 2014-12-31 \\
        --acc 0000753308-11-000025 0000753308-12-000025 0000753308-13-000023 0000753308-14-000025   # first-year share counts
    python3 -I retro/generators/nee/gen_nee_1821.py --filings <dir> [--facts-in <2008-2017 sheet>] [--out retro/facts/NEE.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_nee_1821.json

--facts-in is the 2008-2017 sheet (default: retro/facts/NEE.json, which must then hold 2008-2017 only; the generator refuses a sheet
that already holds a 2018 fact). It only appends.
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
_ap.add_argument("--facts-in", help="the 2008-2017 fact sheet to extend (default retro/facts/NEE.json)")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/NEE.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_nee_1821.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402

ET = ZoneInfo("America/New_York")
CUT = "2021-12-31"
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
assert max(p["published"] for p in old["prints"]) < "2018-01-01", "the input sheet already holds 2018 facts"
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
TENK = {2017: "0000753308-18-000013", 2018: "0000753308-19-000039", 2019: "0000753308-20-000021", 2020: "0000753308-21-000014"}
REL = {"Q4 2017": "0000753308-18-000003", "Q1 2018": "0000753308-18-000079", "Q2 2018": "0000753308-18-000112",
       "Q3 2018": "0000753308-18-000156", "Q4 2018": "0000753308-19-000007", "Q1 2019": "0000753308-19-000115",
       "Q2 2019": "0000753308-19-000162", "Q3 2019": "0000753308-19-000201", "Q4 2019": "0000753308-20-000009",
       "Q1 2020": "0000753308-20-000110", "Q2 2020": "0000753308-20-000146", "Q3 2020": "0000753308-20-000182",
       "Q4 2020": "0000753308-21-000007", "Q1 2021": "0000753308-21-000106", "Q2 2021": "0000753308-21-000143",
       "Q3 2021": "0000753308-21-000164"}
# the first year of each new vintage's ten: its diluted shares from the earliest 10-K whose income statement reports it (the
# earlier vintages' encoding), already in the sheet as sources
FIRST_SHARES = {2017: (2008, "NE33", "0000753308-11-000025"), 2018: (2009, "NE34", "0000753308-12-000025"),
                2019: (2010, "NE35", "0000753308-13-000023"), 2020: (2011, "NE66", "0000753308-14-000025")}
K_SRC = {fy: source(acc, f"NextEra Energy FY{fy} Form 10-K", FILINGS[acc][4],
                    f"FY{fy} annual report (combined filing with Florida Power & Light Company)") for fy, acc in TENK.items()}
R_SRC = {}
for q, acc in REL.items():
    R_SRC[q] = source(acc, f"NextEra Energy {q} results (8-K, Exhibit 99)", fname(doc(acc, "EX-99")),
                      f"{q} earnings release: segment statements of income, earnings per share, outlook")
SPLIT_ACC = "0000753308-20-000165"
SPLIT_SRC = source(SPLIT_ACC, "NextEra Energy 8-K of 2020-09-14 (Items 7.01 and 8.01)", FILINGS[SPLIT_ACC][4],
                   "the four-for-one stock split (Item 8.01); the next year's adjusted earnings per share expectations (Item 7.01)")
# the source ids run in publication order within each kind (10-Ks, releases, the split 8-K)

# ── prints ───────────────────────────────────────────────────────────────────────────────────────────────────────────────
HEAD = re.compile(r"^(Three|Twelve) Months Ended (\w+ \d+, (\d{4})) \| (.*)$")
FPL_COL = ("FPL", "FloridaPower&Light", "FPLSegment")


def statement(path, kind, year):
    """One segment statement of income ('Three' or 'Twelve' months ended in `year`): NextEra Energy's figures and FPL's, Gulf
    Power's (from 2019) and NEER's net income, read row by row between its header and its weighted-average share count. The columns
    are read by name: FPL (or 'Florida Power & Light', 'FPL Segment'), Gulf Power, NEER, Corporate and Other, NextEra Energy."""
    L = lines(path)
    hs = [i for i, x in enumerate(L) if HEAD.match(x) and HEAD.match(x).group(1) == kind and HEAD.match(x).group(3) == str(year)
          and L[i + 1].startswith("Operating Revenues |")]                # the statement of income, not the cash flows
    assert len(hs) == 1, (path, kind, year, hs)
    h = hs[0]
    cols = [re.sub(r"\(\w+\)", "", c).replace(" ", "") for c in L[h].split("|")[1:]]
    assert cols[0] in FPL_COL and cols[-1].startswith("NextEraEnergy") and cols[-2].startswith("Corporate") and "NEER" in cols \
        and set(cols[1:-2]) <= {"GulfPower", "NEER"}, (path, cols)
    gi = cols.index("GulfPower") if "GulfPower" in cols else None
    ni_ = cols.index("NEER")
    CHECK.setdefault(path, []).append(L[h])
    end, _ = first(path, h, len(L), lambda x: x.startswith("Weighted-average shares outstanding (assuming dilution) |"))
    g = lambda test: vals(path, first(path, h, end, test)[1])
    rev = g(lambda x: x.startswith("Operating Revenues |"))
    opi = g(lambda x: re.match(r"Operating Income( \(Loss\))? \|", x))
    pre = g(lambda x: re.match(r"Income( \(Loss\))?( from Continuing Operations)? before Income Taxes \|", x))
    tax = g(lambda x: re.match(r"Income Tax(es| Expense( \(Benefit\))?) \|", x))
    ni = g(lambda x: re.match(r"Net Income( \(Loss\))? \|", x))
    att = [x for x in lines(path)[h:end] if re.match(r"Net Income( \(Loss\))? Attributable to NextEra Energy, Inc\. \|", x)]
    na = vals(path, att[0]) if att else ni
    for v in (rev, opi, pre, tax, ni, na):
        assert len(v) == len(cols) and abs(sum(v[:-1]) - v[-1]) <= 1, (path, "segments must sum to the total", v)
    ie, eps_row = first(path, h, end, lambda x: x.startswith("Earnings") and "Per Share" in x and "(assuming dilution)" in x)
    ia, adj_row = first(path, ie, end, lambda x: x.startswith("Adjusted Earnings") and "Per Share |" in x)
    items = []
    for x in lines(path)[ie + 1:ia]:
        if "|" in x and not x.startswith("Adjustments"):
            v = vals(path, x)
            items.append((re.sub(r"\(\d\)", "", x.split("|")[0]).strip(), v[-1]))
    sh = vals(path, lines(path)[end])
    assert len(sh) == 1
    return dict(rev=rev[-1], opinc=opi[-1], pretax=pre[-1], tax=tax[-1], fpl_ni=ni[0], gulf_ni=None if gi is None else ni[gi],
                neer_ni=na[ni_], ni=na[-1], eps=vals(path, eps_row)[-1], adj=vals(path, adj_row)[-1], items=items, shares=sh[0],
                nci=bool(att), cols=cols)


def no_stats(path):
    """From the Q4 2017 release the releases no longer carry FPL's statistics table (energy sales, customer accounts): asserted."""
    t = " ".join(lines(path))
    assert "Statistics" not in lines(path) and "Energy sales (million kWh)" not in t and "Average customer accounts" not in t, path


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
    no_stats(path)
    raw = dict(rev_m=s["rev"], rev_prior_m=sp["rev"], opinc_m=s["opinc"], opinc_prior_m=sp["opinc"], seg_m=s["fpl_ni"],
               seg_prior_m=sp["fpl_ni"], kwh_m=None, kwh_prior_m=None, ni_m=s["ni"], ni_prior_m=sp["ni"], fple_m=s["neer_ni"],
               fple_prior_m=sp["neer_ni"], cust_k=None, cust_prior_k=None)
    if s["gulf_ni"] is not None:                    # Gulf Power (acquired 2019-01-01): display only, as the release shows it
        raw.update(gulf_m=s["gulf_ni"], gulf_prior_m=sp["gulf_ni"])
    m, m0 = raw["opinc_m"] / raw["rev_m"] * 100, raw["opinc_prior_m"] / raw["rev_prior_m"] * 100
    gp = lambda a, b: r1(pct(a, b)) if a > 0 else r1((b - a) / abs(a) * 100)
    nq = qn % 4 + 1
    p = dict(quarter=q, fy=fy, q=qn, published=pub, filed=filed, release_time="before the open", release=pub, source=R_SRC[q], raw=raw,
             sales_b=round(raw["rev_m"] / 1000, 3), sales_pct=r1(pct(raw["rev_prior_m"], raw["rev_m"])),
             kwh_pct=None, seg_pct=gp(raw["seg_prior_m"], raw["seg_m"]),
             margin=r2(m), margin_prior=r2(m0), margin_bp=r1((m - m0) * 100),
             eps_q=s["eps"], eps_q_prior=sp["eps"], eps_pct=gp(sp["eps"], s["eps"]), eps_basis="GAAP", eps_gaap=s["eps"],
             eps_gaap_prior=sp["eps"], eps_adj=s["adj"], eps_adj_prior=sp["adj"], diluted_shares_m=s["shares"], resources_name="NEER",
             eps_note=eps_words(s, sp),
             next_print=f"Q{nq} {fy + (1 if qn == 4 else 0)} print ({when(year_ago_release(fy + (1 if qn == 4 else 0), nq))})")
    if qn == 4:
        y, y0 = statement(path, "Twelve", fy), statement(path, "Twelve", fy - 1)
        lab = f"FY{fy % 100:02d}"
        mm = y["opinc"] / y["rev"] * 100
        p["fy_actual"] = dict(
            fy=fy, fy_label=lab, eps_normalized=y["eps"], revenue_usd_b=round(y["rev"] / 1000, 3), diluted_shares_m=y["shares"],
            normalization_note=(f"{lab} ${y['eps']:.2f} from the {q} release ({R_SRC[q]}): diluted EPS as reported; the release's "
                                f"adjusted ${y['adj']:.2f} also removes recurring mark-to-market items, so GAAP stands; the 10-K's "
                                "figure replaces it"),
            margin=r2(mm), margin_note=f"{lab} operating margin {mm:.2f}%: operating income ${y['opinc']:,.0f}M on ${y['rev']:,.0f}M ({R_SRC[q]})",
            check_pretax_margin=r2(y["pretax"] / y["rev"] * 100),
            check_pretax_note=f"{lab} income before income taxes ${y['pretax']:,.0f}M on ${y['rev']:,.0f}M ({R_SRC[q]}; display only)",
            tax_rate=round(y["tax"] / y["pretax"], 3), tax_note=f"{lab} income taxes ${y['tax']:,.0f}M on pre-tax ${y['pretax']:,.0f}M (display only)",
            sales_growth=r1(pct(y0["rev"], y["rev"])), kwh_pct=None, seg_pct=r1(pct(y0["fpl_ni"], y["fpl_ni"])),
            customers_k=None, customers_pct=None,
            raw=dict(rev_m=y["rev"], rev_prior_m=y0["rev"], opinc_m=y["opinc"], pretax_m=y["pretax"], tax_m=y["tax"], seg_m=y["fpl_ni"],
                     seg_prior_m=y0["fpl_ni"], kwh_m=None, kwh_prior_m=None, eps_adj=y["adj"], cust_k=None, cust_prior_k=None))
    new_prints.append(p)

# ── vintages: the FY2017-FY2020 10-Ks ──────────────────────────────────────────────────────────────────────────────────────
SEG_NAME = {"FPL": "FPL", "GulfPower": "Gulf Power", "NEER": "NextEra Energy Resources", "Corp.andOther": "Corporate and Other"}


def segments(path, fy):
    """The segment note's operating revenues by segment for the three years, by column name: {year: [(segment, $M), ...]}. The
    FY2017 and FY2018 10-Ks give one row for the three years; from the FY2019 10-K each year has its own table (Gulf Power in 2019-2020)."""
    L = lines(path)
    s = max(i for i, x in enumerate(L) if re.match(r"^\d+\. Segment Information$", x))
    out = {}
    if re.match(r"^20\d\d(\(\w\))? \| 20\d\d(\(\w\))? \| 20\d\d(\(\w\))?$", L[s + 7]) or any(
            re.match(r"^20\d\d(\(\w\))? \| 20\d\d(\(\w\))? \| 20\d\d(\(\w\))?$", L[i]) for i in range(s, s + 9)):
        i, hy = first(path, s, s + 9, lambda x: re.match(r"^20\d\d(\(\w\))? \| 20\d\d(\(\w\))? \| 20\d\d(\(\w\))?$", x))
        years = [int(t[:4]) for t in hy.split(" | ")]
        cols = [re.sub(r"\(\w\)", "", c).replace(" ", "").replace("-", "") for c in L[i + 1].split(" | ")]
        r = vals(path, first(path, i, i + 4, lambda x: x.startswith("Operating revenues |"))[1])
        CHECK.setdefault(path, []).extend([hy, L[i + 1]])
        assert len(cols) == len(r) == 12, (fy, cols)
        for k, yv in enumerate(years):
            out[yv] = list(zip(cols[4 * k:4 * k + 4], r[4 * k:4 * k + 4]))
    else:
        for yv in range(fy, fy - 3, -1):
            i, _ = first(path, s, len(L), lambda x, yv=yv: re.match(rf"^{yv}(\(\w\))?$", x))
            cols = [re.sub(r"\(\w\)", "", c).replace(" ", "") for c in L[i + 1].split(" | ")]
            r = vals(path, first(path, i, i + 4, lambda x: x.startswith("Operating revenues |"))[1])
            CHECK.setdefault(path, []).append(L[i + 1])
            assert len(cols) == len(r), (fy, yv, cols)
            out[yv] = list(zip(cols, r))
    for yv, row in out.items():
        names = [c for c, _ in row]
        assert names[0] == "FPL" and names[-1].startswith("NEEConsol") and names[-2] == "Corp.andOther", (fy, yv, names)
        assert sum(v for _, v in row[:-1]) == row[-1][1], (fy, yv, "segment revenues sum")
    return out


V = []
prev = old["history_vintages"][-1]
for fy, acc in TENK.items():
    path = doc(acc, "10-K")
    L = lines(path)
    sid = K_SRC[fy]
    pub = SRC[sid]["published"]
    s6 = max(i for i, x in enumerate(L) if x == "Item 6. Selected Financial Data")
    s7, _ = first(path, s6, len(L), lambda x: x.startswith("Item 7."))
    # the NEE statement of income (the first OPERATING REVENUES row of the filing), its diluted EPS and the EPS note's shares
    io, x = first(path, s7, len(L), lambda x: x.startswith("OPERATING REVENUES |"))
    rev3 = vals(path, x)
    ie3, _ = first(path, io, len(L), lambda x: x == "Earnings per share attributable to NEE:")
    end_is, x = first(path, ie3, ie3 + 3, lambda x: x.startswith("Assuming dilution |"))
    eps3 = vals(path, x)
    opinc = vals(path, first(path, io, end_is, lambda x: x.startswith("OPERATING INCOME |"))[1])
    pretax = vals(path, first(path, io, end_is, lambda x: x.startswith("INCOME BEFORE INCOME TAXES |"))[1])
    tax = vals(path, first(path, io, end_is, lambda x: re.match(r"INCOME TAX(ES| EXPENSE \(BENEFIT\)) \|", x))[1])
    _, x = first(path, end_is, len(L), lambda x: x.startswith("Weighted-average number of common shares outstanding - assuming dilution |"))
    shares = vals(path, x)
    sst = [i for i in range(end_is, end_is + 4) if L[i] == "Weighted-average number of common shares outstanding:"]
    if sst:                                                       # the statement's own count, where it prints one, agrees
        assert vals(path, first(path, sst[0], sst[0] + 3, lambda x: x.startswith("Assuming dilution |"))[1]) == shares, fy
    if L[s6 + 1] == "Omitted/Not Applicable":                     # the FY2020 10-K: no selected data, its statements' three years
        CHECK.setdefault(path, []).append(L[s6 + 1])
        years, sel_rev, sel_eps, sel_cont = list(range(fy, fy - 3, -1)), rev3, eps3, eps3
        basis = "its statements of income (Item 6 omitted)"
    else:
        i, hdr = first(path, s6, s7, lambda x: re.match(r"^20\d\d(\(\w\))?( \| 20\d\d(\(\w\))?){4}$", x))
        years = [int(t[:4]) for t in hdr.split(" | ")]
        assert years == list(range(fy, fy - 5, -1)), (fy, years)
        CHECK.setdefault(path, []).append(hdr)
        sel_rev = vals(path, first(path, s6, s7, lambda x: x.startswith("Operating revenues |"))[1])
        ih, xh = first(path, s6, s7, lambda x: re.match(r"^Earnings per share attributable to NEE - assuming dilution(\(\w\))*(:| \|)", x))
        if xh.endswith(":"):
            sel_eps = vals(path, first(path, ih, ih + 3, lambda x: x.startswith("Net income"))[1])
            sel_cont = vals(path, first(path, ih, ih + 3, lambda x: x.startswith("Continuing operations"))[1])
        else:
            sel_eps = sel_cont = vals(path, xh)
        basis = "its selected financial data"
        assert sel_rev[:3] == rev3 and sel_eps[:3] == eps3, (fy, "selected data and statements of income")
    # cash flows (the NEE statement after the income statement), then FPL's statement of income
    ic, _ = first(path, end_is, len(L), lambda x: x.startswith("Net cash provided by operating activities |"))
    ocf = vals(path, L[ic])
    ie_, _ = first(path, ic, len(L), lambda x: re.match(r"Cash(, cash equivalents and restricted cash| and cash equivalents) at end of year \|", x))
    cash = vals(path, L[ie_])
    CAPEX = ("Capital expenditures of FPL |", "Acquisition and capital expenditures of Gulf Power |",
             "Independent power and other investments of NEER |", "Nuclear fuel purchases |", "Other capital expenditures")
    ce_rows = [x for x in L[ic:ic + 14] if x.startswith(CAPEX)]
    assert len(ce_rows) == (5 if fy >= 2019 else 4), (fy, ce_rows)
    ce = [vals(path, x)[0] for x in ce_rows]
    ce_labels = [x.split(" |")[0] for x in ce_rows]
    _, xi = first(path, ic, ie_, lambda x: x.startswith("Issuances of common stock"))
    issu, issu_lab = vals(path, xi), xi.split(" |")[0]
    rep = [x for x in L[ic:ie_] if x.startswith("Repurchases of common stock |")]
    repv = vals(path, rep[0]) if rep else [0.0]
    divs = vals(path, first(path, ic, ie_, lambda x: x.startswith("Dividends on common stock |"))[1])
    ifpl, _ = first(path, ie_, len(L), lambda x: x.startswith("OPERATING REVENUES |"))
    fpl_ni3 = vals(path, first(path, ifpl, ifpl + 25, lambda x: x.startswith("NET INCOME"))[1])
    q4 = [p for p in new_prints if p["quarter"] == f"Q4 {fy}"][0]
    seg = segments(path, fy)
    assert [seg[y][-1][1] for y in (fy, fy - 1, fy - 2)] == rev3, (fy, "segment revenues and the statement")
    assert eps3[0] == q4["fy_actual"]["eps_normalized"] and rev3[0] == q4["fy_actual"]["raw"]["rev_m"], (fy, "Q4 release vs 10-K")
    # ten fiscal years to the latest: the new 10-K's years, the earlier years as the previous vintage holds them
    keep = [y for y in range(fy - 9, fy + 1) if y not in years]
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
    carried_disc = [y for y in keep if y == 2013]                  # 2013 on net income, as the FY2013-FY2017 vintages record it
    v = dict(published=pub, sources=list(dict.fromkeys([sid] + [es[y] for y in eps] + [s0])), company="NextEra Energy, Inc.",
             exchange="NYSE",
             business_line=(prev["business_line"] if fy < 2018 else
                            "Florida Power & Light and Gulf Power, the rate-regulated Florida utilities, and NextEra Energy Resources' "
                            "competitive energy business"),
             fy_label=lab, fiscal_year_ends={y: f"{y}-12-31" for y in eps}, eps_normalized=eps, eps_sources=es, eps_published=ep,
             normalization=(f"GAAP diluted EPS before the cumulative effect of accounting changes, each year from the latest 10-K that "
                            f"reports it ({fy}-{years[-1]} from {basis}): {eps_text}"
                            + (f". {', '.join(map(str, disc))}: EPS on net income attributable to NEE, the gain from discontinued "
                               "operations in (the 10-K's continuing operations figure"
                               + "".join(f" for {y} is ${c:.2f}" for y, a, c in zip(years, sel_eps, sel_cont) if a != c)
                               + ", display only; the NEE rule's line is before the cumulative effect, which discontinued operations "
                               "sit above)" if disc else "")
                            + (". 2013: EPS on net income attributable to NEE, the gain from discontinued operations in, as the "
                               "earlier vintages record it" if carried_disc else "")
                            + (". 2017 and 2018: GAAP, their listed one-off benefits (the tax reform items, the FiberNet gain, the NEP "
                               "investment gains) under the year's income without them, so the mirror of the AAPL FY2002 test is not met "
                               "and no figure excluding only them is published" if fy >= 2018 else
                               ". 2017: GAAP, its listed one-off benefits (the tax reform gain, the FiberNet gain) under the year's income "
                               "without them, so the mirror of the AAPL FY2002 test is not met and no figure excluding only them is published")
                            + ". From 2001 the company's figures without its listed items also remove the mark-to-market effect of "
                            "non-qualifying hedges, a recurring item, so GAAP stands (the PEP 2008 core rule)"),
             revenue_usd_b=rev, revenue_sources=rs, diluted_shares_m={str(y0): first_sh, str(fy): shares[0]},
             shares_published={str(y0): old["sources"][s0]["published"], str(fy): pub},
             shares_note=(f"{y0}: {first_sh:,}M ({s0}, the income statement's diluted weighted-average shares); {fy}: {shares[0]:,}M diluted "
                          f"({sid}, the EPS note)"),
             pe_window_start=None, prev_fy_margin=r2(opinc[0] / rev3[0] * 100),
             prev_fy_margin_note=(f"{lab} operating margin {opinc[0] / rev3[0] * 100:.2f}%: operating income ${opinc[0]:,.0f}M on "
                                  f"operating revenues ${rev3[0]:,.0f}M ({sid})"),
             check_pretax_margin=r2(pretax[0] / rev3[0] * 100),
             check_pretax_note=f"{lab} income before income taxes ${pretax[0]:,.0f}M on ${rev3[0]:,.0f}M ({sid}; display only)",
             tax_rate=round(tax[0] / pretax[0], 3), tax_note=f"{lab} income taxes ${tax[0]:,.0f}M on pre-tax ${pretax[0]:,.0f}M ({sid}; display only)",
             prev_fy_sales_growth=r1(pct(rev3[1], rev3[0])), prev_fy_kwh_pct=None,
             prev_fy_seg_pct=r1(pct(fpl_ni3[1], fpl_ni3[0])), prev_fy_customers_k=None, prev_fy_customers_pct=None,
             dividend_annual=round(rate * 4, 4), dividend_note=f"'{dq}' ({sid})", cash_b=round(cash[0] / 1000, 3),
             fcf_b=round((ocf[0] + sum(ce)) / 1000, 3), fcf_label=lab,
             fcf_note=(f"net cash provided by operating activities ${ocf[0]:,.0f}M less the cash flow statement's "
                       + ", ".join(x[0].lower() + x[1:] for x in ce_labels)
                       + f" (${-sum(ce):,.0f}M, their sum) ({sid})"),
             cash_return_text=(f"{issu_lab[0].lower() + issu_lab[1:]} ${issu[0]:,.0f}M, "
                               + (f"repurchases of common stock ${-repv[0]:,.0f}M and " if repv[0] else "no repurchases of common stock and ")
                               + f"dividends on common stock ${-divs[0]:,.0f}M in {fy} ({sid} cash flows): the dividend is most of the return"),
             groups=[[SEG_NAME[c], round(r / 1000, 3),
                      (r1(pct(dict(seg[fy - 1])[c], r)) if c in dict(seg[fy - 1]) else None)] for c, r in seg[fy][:-1]],
             groups_basis=f"{lab} operating revenues by segment ({sid}, segment information)",
             margin_signal_name="Operating margin change", why=why,
             raw=dict(kwh=None, seg=[fpl_ni3[1], fpl_ni3[0]], opinc=opinc[0], rev=rev3[0], pretax=pretax[0], tax=tax[0], ocf=ocf[0],
                      capex=ce, cash=cash[0], segrev={str(y): [[SEG_NAME.get(c, "NEE"), r] for c, r in seg[y]] for y in seg}, customers=None),
             franchise_note=(f"FPL's energy sales and customer accounts n/r: neither the FY{fy} 10-K nor the Q4 {fy} release "
                             f"({q4['source']}) tabulates them"))
    assert -repv[0] < -divs[0], fy
    # ENERGY_TRANSITION (live from 2015-12-12): the company's own words on its gas reserves and the GHG limits
    v["reserves_quote"] = find(path, r"NEER's oil and gas production assets,? represent(ing|ed) approximately [^.]*\.")
    v["transition_quote"] = find(path, r"While NEE's and FPL's electric generati\w+ (units emit|portfolio emits) greenhouse gases at a lower "
                                 r"rate of emissions than most of the U\.S\. electric generation sector, the results of operations of NEE "
                                 r"and FPL could be materially adversely affected to the extent that new federal or state laws or "
                                 r"regulations impose any new greenhouse gas emission limits\.")
    V.append(v)
    prev = v

# ── guides: every expectation of 2018-2021 is adjusted earnings per share (display only, the PEP 2008 core rule) ──────────────
UNUSED = ("an outlook on the adjusted basis, which also removes the mark-to-market effect of non-qualifying hedges and the unrealized "
          "gains and losses on equity securities and OTTI in NEER's nuclear decommissioning funds, recurring items (the PEP 2008 core "
          "rule): no field, so the last full year's EPS stands")
G = [  # (fy, published, the quote: the current year's sentence or clause only; an earlier year may be named as a base, no later one)
    (2018, "Q4 2017", "Based on the tax reform benefit, which is expected to be approximately 45 cents in 2018, NextEra Energy is increasing "
                      "its financial expectations ranges and now expects adjusted earnings per share to be in the range of $7.45 to $7.95 for 2018"),
    (2018, "Q1 2018", "NextEra Energy continues to expect adjusted earnings per share to be in the range of $7.45 to $7.95 for 2018"),
    (2018, "Q2 2018", "NextEra Energy expects adjusted earnings per share to be in the range of $7.45 to $7.95 for 2018 and is targeting "
                      "the midpoint of $7.70 per share"),
    (2018, "Q3 2018", "NextEra Energy continues to expect adjusted earnings per share to be in the range of $7.45 to $7.95 for 2018 and is "
                      "targeting the midpoint of $7.70 per share"),
    (2019, "Q4 2018", "NextEra Energy continues to expect adjusted earnings per share to be in the range of $8.00 to $8.50 for 2019"),
    (2019, "Q1 2019", "In 2019, NextEra Energy continues to expect adjusted earnings per share to be at or near the top of our previously "
                      "disclosed compound annual growth rate of 6% to 8%, off the 2018 base of $7.70 per share"),
    (2019, "Q2 2019", "In 2019, NextEra Energy continues to expect adjusted earnings per share to be at or near the top of its previously "
                      "disclosed compound annual growth rate of 6% to 8%, off the 2018 base of $7.70 per share"),
    (2019, "Q3 2019", "In 2019, NextEra Energy continues to expect adjusted earnings per share to be at or near the top of its previously "
                      "disclosed compound annual growth rate of 6% to 8%, off the 2018 base of $7.70 per share, which, if achieved, would "
                      "result in adjusted earnings per share of $8.32"),
    (2020, "Q4 2019", "For 2020, NextEra Energy continues to expect its adjusted earnings per share to be in the range of $8.70 to $9.20"),
    (2020, "Q1 2020", "For 2020, NextEra Energy continues to expect its adjusted earnings per share to be in the range of $8.70 to $9.20"),
    (2020, "Q2 2020", "For 2020, NextEra Energy continues to expect its adjusted earnings per share to be in the range of $8.70 to $9.20"),
    (2020, "Q3 2020", "In 2020, the company now expects adjusted earnings per share to be in the range of $2.18 to $2.30"),
    (2021, "Q4 2020", "For 2021, NextEra Energy expects adjusted earnings per share to be in the range of $2.40 to $2.54"),
    (2021, "Q1 2021", "For 2021, NextEra Energy expects adjusted earnings per share to be in the range of $2.40 to $2.54"),
    (2021, "Q2 2021", "For 2021, NextEra Energy expects adjusted earnings per share to be in the range of $2.40 to $2.54"),
    (2021, "Q3 2021", "For 2021, NextEra Energy expects adjusted earnings per share to be in the range of $2.40 to $2.54"),
]
new_guides = []
for fy, key, text in G:
    acc, sid, d = REL[key], R_SRC[key], f"{key} release"
    path = doc(acc, "EX-99")
    quote(path, text)
    later = {int(y) for y in re.findall(r"\b(20\d\d)\b", text)} - set(range(2000, fy + 1))
    assert not later, (key, "a guide quote names a later year", later)
    disp = f"'{text}'"
    if key == "Q3 2020":          # the release restates the 2020 range on the post-split share basis, a week before the split
        disp += (" (the release's own sentence before it: 'As a result of the four-for-one stock split, NextEra Energy updated its "
                 "adjusted earnings per share financial expectations ranges to reflect the increase in outstanding shares.')")
        quote(path, "As a result of the four-for-one stock split, NextEra Energy updated its adjusted earnings per share financial "
                    "expectations ranges to reflect the increase in outstanding shares.")
    new_guides.append(dict(fy=fy, published=SRC[sid]["published"], source=sid, doc=d, display=disp, unused=UNUSED))
new_guides.sort(key=lambda g: (g["published"], g["fy"]))

# ── the four-for-one split of 2020 (prices as traded; the per-share facts published before it restated: on_basis) ─────────────
sp_path = doc(SPLIT_ACC, "8-K")
sq = quote(sp_path, "On September 14, 2020, NEE's board of directors approved a four-for-one split of NEE common stock, which is intended "
                    "to make stock ownership more accessible to a broader base of investors. Each NEE shareholder of record at the close of "
                    "business on October 19, 2020, will receive three additional shares of common stock for each then-held share, to be "
                    "distributed on October 26, 2020. Trading will begin on a stock split-adjusted basis on October 27, 2020.")
new_split = dict(effective="2020-10-27", ratio=4.0, source=SPLIT_SRC,
                 note=(f"'{sq}' ({SPLIT_SRC}); Yahoo's split date is 2020-10-27, the first trading day on the new basis. Per-share figures "
                       "published before 2020-10-27 are divided by 4 and share counts multiplied by 4 (on_basis); the Q4 2020 release and the "
                       "FY2020 10-K report on the new basis, and the Q3 2020 release (2020-10-21) already states its outlook on it"))

# ── checks: each Q4 print's full year equals the 10-K that follows it (EPS and revenue; shares to the release's rounding) ──────
for p in new_prints:
    a = p.get("fy_actual")
    if a:
        v = [x for x in V if x["fy_label"] == a["fy_label"]][0]
        y = str(a["fy"])
        assert (v["eps_normalized"][y], v["revenue_usd_b"][y]) == (a["eps_normalized"], a["revenue_usd_b"]), (p["quarter"], "Q4 vs 10-K")
        assert abs(v["diluted_shares_m"][y] - a["diluted_shares_m"]) <= 0.5, p["quarter"]
assert [p["published"] for p in old["prints"] + new_prints] == sorted(p["published"] for p in old["prints"] + new_prints)

# ── assemble: the earlier facts unchanged ────────────────────────────────────────────────────────────────────────────────
for k in SRC:
    assert k not in f["sources"]
f["sources"].update(SRC)
f["history_vintages"] += V
f["prints"] += new_prints
f["guides"] += new_guides
f["splits"] = old["splits"] + [new_split]
for key in ("sources", "history_vintages", "prints", "guides", "splits"):
    n_old = len(old[key])
    got = list(f[key].items())[:n_old] if key == "sources" else f[key][:n_old]
    want = list(old[key].items()) if key == "sources" else old[key]
    assert got == want, key
for key in ("rule_t", "eps_guides", "dividends", "events", "company_names", "listings", "distributions", "price_basis", "ticker"):
    assert f[key] == old[key], key
f["_doc"] = old["_doc"] + (
    " 2018-2021 (retro/README.md, 'NEE 2018-2021') was appended by retro/generators/nee/gen_nee_1821.py from the filings accepted "
    "2018-01-01 to 2021-12-31 (sources NE93 on), every earlier fact unchanged: from the Q4 2017 release the releases no longer tabulate "
    "FPL's energy sales or customer accounts, so those fields are None (n/r); the FY2020 vintage takes 2018-2020 from its statements "
    "(Item 6 omitted); the four-for-one split effective 2020-10-27 is the second 'splits' record.")
with open(FACTS, "w", encoding="utf-8") as fh:
    json.dump(f, fh, ensure_ascii=False, indent=1)
with open(A.checklist or os.path.join(SP, "checklist_nee_1821.json"), "w", encoding="utf-8") as fh:
    json.dump(CHECK, fh, ensure_ascii=False, indent=1)
print(len(SRC), "sources,", len(V), "vintages,", len(new_prints), "prints,", len(new_guides), "guides;",
      sum(len(v) for v in CHECK.values()), "checklist strings")
for p in new_prints:
    print(p["quarter"], p["published"], p["sales_pct"], p["seg_pct"], p["margin_bp"], p["eps_q"], p["eps_q_prior"],
          p["eps_pct"], p["diluted_shares_m"], p["next_print"], p.get("fy_actual", {}).get("eps_normalized"), p["raw"].get("gulf_m"))
for v in V:
    print(v["published"], v["fy_label"], v["eps_normalized"], v["prev_fy_margin"], v["groups"], v["dividend_annual"], v["diluted_shares_m"])
for k, s in SRC.items():
    print(k, s["published"], s["filed"], s["title"][:60])
