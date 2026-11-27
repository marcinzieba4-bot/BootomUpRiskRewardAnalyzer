#!/usr/bin/env python3
"""Extend retro/facts/NEE.json with 2022-2026 (filings accepted 2022-01-01 to 2026-11-22), asserting that every earlier fact is
unchanged. The discipline of gen_nee_1821.py (retro/README.md, "NEE 2018-2021"): each figure from its own row by label under an
anchored heading, the segment columns (FPL, Gulf Power in 2021, NEER, Corporate and Other) asserted to sum to NextEra Energy's
total, every growth rate, margin and margin change computed, every quote asserted present in its own filing, and a verbatim checklist
written. New in 2022-2026 (retro/README.md, "NEE 2022-2026"): the FY2021-FY2025 10-Ks reserve Item 6, so each vintage takes its
three years from its statements of income; each Q4 release's after-tax table of the items its adjusted earnings remove is read for the
AAPL FY2002 test and its mirror (asserted not met for FY2021-FY2025); the current-year adjusted EPS ranges of the Item 7.01 8-Ks
(the 2022, 2024 and 2025 investor conferences and the 8-K of 2026-01-02) are display-only guides like the releases'. Run:

    python3 retro/tools/edgar.py index 753308 <dir>
    python3 retro/tools/edgar.py fetch 753308 <dir> --from 2022-01-01 --to 2026-11-22 --forms 8-K 8-K/A 10-K 10-K/A
    python3 retro/tools/edgar.py fetch 753308 <dir> --from 2015-01-01 --to 2019-12-31 \\
        --acc 0000753308-15-000079 0000753308-16-000337 0000753308-17-000060 0000753308-18-000013 0000753308-19-000039   # first-year shares
    python3 -I retro/generators/nee/gen_nee_2226.py --filings <dir> [--facts-in <2008-2021 sheet>] [--out retro/facts/NEE.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_nee_2226.json

--facts-in is the 2008-2021 sheet (default: retro/facts/NEE.json, which must then hold 2008-2021 only; the generator refuses a sheet
that already holds a 2022 fact). It only appends.
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
_ap.add_argument("--facts-in", help="the 2008-2021 fact sheet to extend (default retro/facts/NEE.json)")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/NEE.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_nee_2226.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402

ET = ZoneInfo("America/New_York")
CUT = "2026-11-22"
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
assert max(p["published"] for p in old["prints"]) < "2022-01-01", "the input sheet already holds 2022 facts"
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
TENK = {2021: "0000753308-22-000014", 2022: "0000753308-23-000019", 2023: "0000753308-24-000008", 2024: "0000753308-25-000011",
        2025: "0000753308-26-000015"}
REL = {"Q4 2021": "0000753308-22-000007", "Q1 2022": "0000753308-22-000030", "Q2 2022": "0000753308-22-000052",
       "Q3 2022": "0000753308-22-000076", "Q4 2022": "0000753308-23-000009", "Q1 2023": "0000753308-23-000029",
       "Q2 2023": "0000753308-23-000042", "Q3 2023": "0000753308-23-000053", "Q4 2023": "0000753308-24-000002",
       "Q1 2024": "0000753308-24-000021", "Q2 2024": "0000753308-24-000048", "Q3 2024": "0000753308-24-000055",
       "Q4 2024": "0000753308-25-000003", "Q1 2025": "0000753308-25-000021", "Q2 2025": "0000753308-25-000039",
       "Q3 2025": "0000753308-25-000055", "Q4 2025": "0000753308-26-000007", "Q1 2026": "0000753308-26-000028",
       "Q2 2026": "0000753308-26-000058", "Q3 2026": "0000753308-26-000077"}
# the first year of each new vintage's ten: its diluted shares from the earliest 10-K whose income statement reports it (the
# earlier vintages' encoding), already in the sheet as sources
FIRST_SHARES = {2021: (2012, "NE67", "0000753308-15-000079"), 2022: (2013, "NE68", "0000753308-16-000337"),
                2023: (2014, "NE69", "0000753308-17-000060"), 2024: (2015, "NE93", "0000753308-18-000013"),
                2025: (2016, "NE94", "0000753308-19-000039")}
K_SRC = {fy: source(acc, f"NextEra Energy FY{fy} Form 10-K", FILINGS[acc][4],
                    f"FY{fy} annual report (combined filing with Florida Power & Light Company)") for fy, acc in TENK.items()}
R_SRC = {}
for q, acc in REL.items():
    R_SRC[q] = source(acc, f"NextEra Energy {q} results (8-K, Exhibit 99)", fname(doc(acc, "EX-99")),
                      f"{q} earnings release: segment statements of income, earnings per share, outlook")
# the Item 7.01 8-Ks that state the current year's adjusted EPS range outside a release (display only, like the releases' ranges)
FD = {"2022-06-14": "0000753308-22-000045", "2024-06-11": "0000753308-24-000035", "2025-12-08": "0000753308-25-000064",
      "2026-01-02": "0000753308-26-000004"}
FD_SRC = {k: source(acc, f"NextEra Energy 8-K of {k} (Item 7.01)", FILINGS[acc][4],
                    "the adjusted earnings per share expectations (Item 7.01)") for k, acc in FD.items()}
# the source ids run in publication order within each kind (10-Ks, releases, the Item 7.01 8-Ks)

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


RECURRING = ("Net losses (gains) associated with non-qualifying hedges",
             "Change in unrealized losses (gains) on equity securities held in NEER's nuclear decommissioning")


def aftertax(path, year):
    """The footnote table '(b) After tax impact ... is as follows' under the twelve months' statement of `year`: each item the
    adjusted earnings remove, after tax, NextEra Energy's column ($M). The one-off items are those other than the mark-to-market
    effect of non-qualifying hedges and the nuclear decommissioning funds' unrealized gains and losses and OTTI, which recur."""
    L = lines(path)
    hs = [i for i, x in enumerate(L) if HEAD.match(x) and HEAD.match(x).group(1) == "Twelve" and HEAD.match(x).group(3) == str(year)
          and L[i + 1].startswith("Operating Revenues |")]
    h = hs[0]
    ib, x = first(path, h, h + 90, lambda x: x.startswith("(b) | After tax impact"))
    CHECK.setdefault(path, []).append(x)
    out = []
    for x in L[ib + 2:ib + 12]:
        if x.startswith("(c)") or "|" not in x or re.match(r"^\d+$", x):
            break
        v = vals(path, x)
        out.append((x.split(" |")[0].strip(), v[-2]))
    assert out and out[0][0].startswith(RECURRING[0]), (path, out)
    return out


def oneoff_test(fy, ni, items):
    """The AAPL FY2002 test (listed one-off charges larger than the year's net income) and its mirror (listed one-off benefits
    larger than the year's income without them), on the after-tax one-off items; both must fail for the year to stand at GAAP."""
    one = [(lab, v) for lab, v in items if not lab.startswith(RECURRING)]
    charges = sum(v for _, v in one if v > 0)
    benefits = -sum(v for _, v in one if v < 0)
    assert charges <= ni and benefits <= ni - benefits, (fy, "a distorted year: decide its encoding first", charges, benefits, ni)
    words = "; ".join(f"{lab} {'$' if v >= 0 else '-$'}{abs(v):,.0f}M" for lab, v in one)
    # only the filing's own figures are printed: the charges sum to under the year's net income, the benefits to under half of it
    return (f"{fy}: GAAP, its one-off items after tax as the Q4 {fy} release tabulates them ({words}): the charges among them sum to "
            f"less than its ${ni:,.0f}M net income and the benefits to less than half of it (less than its income without them), so "
            "neither the AAPL FY2002 test nor its mirror is met")


ONEOFF = {}


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
             eps_q=s["eps"], eps_q_prior=sp["eps"], eps_pct=None if sp["eps"] == 0 else gp(sp["eps"], s["eps"]), eps_basis="GAAP", eps_gaap=s["eps"],
             eps_gaap_prior=sp["eps"], eps_adj=s["adj"], eps_adj_prior=sp["adj"], diluted_shares_m=s["shares"], resources_name="NEER",
             eps_note=eps_words(s, sp) + ("; the year-ago $0.00 gives no growth rate (n/m), so the EPS signal scores BASE and "
                                          "prints n/r (the F rule)" if sp["eps"] == 0 else ""),
             next_print=f"Q{nq} {fy + (1 if qn == 4 else 0)} print ({when(year_ago_release(fy + (1 if qn == 4 else 0), nq))})")
    if qn == 4:
        y, y0 = statement(path, "Twelve", fy), statement(path, "Twelve", fy - 1)
        lab = f"FY{fy % 100:02d}"
        mm = y["opinc"] / y["rev"] * 100
        ONEOFF[fy] = oneoff_test(fy, y["ni"], aftertax(path, fy))
        p["fy_actual"] = dict(
            fy=fy, fy_label=lab, eps_normalized=y["eps"], revenue_usd_b=round(y["rev"] / 1000, 3), diluted_shares_m=y["shares"],
            normalization_note=(f"{lab} ${y['eps']:.2f} from the {q} release ({R_SRC[q]}): diluted EPS as reported; the release's "
                                f"adjusted ${y['adj']:.2f} also removes recurring mark-to-market items, so GAAP stands; the 10-K's "
                                f"figure replaces it. {ONEOFF[fy]}"),
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
    if any(L[i] == f"December 31, {fy}" and L[i + 1] == "FPL | NEER | Total" for i in range(s, s + 20)):
        # the FY2024-FY2025 10-Ks (the segment-expense standard adopted 2024-01-01): per year, the reportable segments' operating
        # revenues and their total, then Corporate and Other and the total consolidated revenues on rows of their own
        for yv in range(fy, fy - 3, -1):
            i, _ = first(path, s, len(L), lambda x, yv=yv: x == f"December 31, {yv}")
            assert L[i + 1] == "FPL | NEER | Total", (fy, yv)
            r = vals(path, first(path, i, i + 4, lambda x: x.startswith("Operating revenues |"))[1])
            j, x = first(path, i, i + 6, lambda x: x.startswith("Corporate and Other |"))
            c = vals(path, x)
            t = vals(path, first(path, j, j + 2, lambda x: x.startswith("Total consolidated revenues |"))[1])
            CHECK.setdefault(path, []).extend([L[i], L[i + 1]])
            assert len(r) == 3 and r[0] + r[1] == r[2] and len(c) == 1 and len(t) == 1 and r[2] + c[0] == t[0], (fy, yv, r, c, t)
            out[yv] = [("FPL", r[0]), ("NEER", r[1]), ("Corp.andOther", c[0]), ("NEEConsolidated", t[0])]
    elif re.match(r"^20\d\d(\(\w\))? \| 20\d\d(\(\w\))? \| 20\d\d(\(\w\))?$", L[s + 7]) or any(
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
        row[0] = ("FPL", row[0][1]) if row[0][0] == "FPLSegment" else row[0]     # the FY2021 10-K's "FPL Segment" column
        out[yv] = row
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
    s6 = max(i for i, x in enumerate(L) if x == "Item 6. Reserved")      # the FY2021-FY2025 10-Ks reserve Item 6
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
    _, x = first(path, end_is, len(L), lambda x: re.match(r"Weighted-average number of common shares outstanding [-–] assuming dilution \|", x))
    shares = vals(path, x)
    sst = [i for i in range(end_is, end_is + 4) if L[i] == "Weighted-average number of common shares outstanding:"]
    if sst:                                                       # the statement's own count, where it prints one, agrees
        assert vals(path, first(path, sst[0], sst[0] + 3, lambda x: x.startswith("Assuming dilution |"))[1]) == shares, fy
    CHECK.setdefault(path, []).append(L[s6])                      # no selected data: its statements' three years
    years, sel_rev, sel_eps, sel_cont = list(range(fy, fy - 3, -1)), rev3, eps3, eps3
    basis = "its statements of income (Item 6 reserved)"
    # cash flows (the NEE statement after the income statement), then FPL's statement of income
    ic, _ = first(path, end_is, len(L), lambda x: x.startswith("Net cash provided by operating activities |"))
    ocf = vals(path, L[ic])
    ie_, _ = first(path, ic, len(L), lambda x: re.match(r"Cash(, cash equivalents and restricted cash| and cash equivalents) at end of year \|", x))
    cash = vals(path, L[ie_])
    CAPEX = ("Capital expenditures of FPL |", "Capital expenditures of FPL Segment |", "Acquisition and capital expenditures of Gulf Power |",
             "Independent power and other investments of NEER |", "Nuclear fuel purchases |", "Other capital expenditures")
    ce_rows = [x for x in L[ic:ic + 14] if x.startswith(CAPEX)]
    assert len(ce_rows) == (5 if fy == 2021 else 4), (fy, ce_rows)   # Gulf Power merged into FPL on 2021-01-01
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
              r"primarily in the generation, (storage, )?transmission, distribution and sale of electric energy in Florida\.")
    nq_ = find(path, r"NEER produces the majority of its (electricity|energy) from clean and renewable sources|NEER’s strategic focus is "
                     r"centered on the development, construction and operation of long-term contracted generation facilities, including "
                     r"renewables, nuclear and natural gas, as well as battery storage facilities\.")    # the FY2025 10-K's wording
    rq = [find(path, r"NEE's and FPL's business, financial condition, results of operations and prospects may be (materially )?adversely affected by "
               r"the extensive regulation of their business\."),
          find(path, r"NEE's and FPL's business, financial condition, results of operations and prospects can be materially adversely "
               r"affected by weather conditions( and related impacts)?, including, but not limited to, the impact of severe weather\."),
          find(path, r"NEE's and FPL's business could be negatively affected by federal or state laws or regulations mandating new or "
               r"additional limits on the production of greenhouse gas emissions\.")]
    assert "cyclical" not in " ".join(L).lower(), (fy, "a 10-K calls the business cyclical: decide its encoding first")
    why = (f"NextEra Energy, Inc.: '{fq}' and '{nq_}'; among its risk factors, '{rq[0]}', '{rq[1]}' and '{rq[2]}' "
           f"(its own FY{fy} 10-K)")
    carried_disc = [y for y in keep if y == 2013]                  # 2013 on net income, as the FY2013-FY2017 vintages record it
    v = dict(published=pub, sources=list(dict.fromkeys([sid] + [es[y] for y in eps] + [s0])), company="NextEra Energy, Inc.",
             exchange="NYSE",
             business_line=(prev["business_line"] if "GulfPower" in dict(seg[fy]) else       # Gulf Power a segment to FY2021
                            "Florida Power & Light, the rate-regulated Florida utility, and NextEra Energy Resources' competitive "
                            "energy business"),
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
                            + "".join(f". {ONEOFF[int(y)]}" for y in eps if int(y) in ONEOFF)
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
    v["reserves_quote"] = find(path, r"NEER's (oil and gas|natural gas and oil) production assets,? represent(ing|ed) approximately [^.]*\.")
    v["transition_quote"] = find(path, r"(While NEE's and FPL's electric generati\w+ (units emit|portfolio emits) greenhouse gases at a lower "
                                 r"rate of emissions than most of the U\.S\. electric generation sector, the r|(?<![a-z,] )The r)esults of operations of NEE "
                                 r"and FPL could be materially adversely affected to the extent that new federal or state laws or "
                                 r"regulations impose any new greenhouse gas emission limits\.")
    V.append(v)
    prev = v

# ── guides: every expectation of 2022-2026 is adjusted earnings per share (display only, the PEP 2008 core rule) ──────────────
UNUSED = ("an outlook on the adjusted basis, which also removes the mark-to-market effect of non-qualifying hedges and the unrealized "
          "gains and losses on equity securities and OTTI in NEER's nuclear decommissioning funds, recurring items (the PEP 2008 core "
          "rule): no field, so the last full year's EPS stands")
# (fy, the release or Item 7.01 8-K, [quoted fragments], a note): the current year's sentence or clause only; a sentence that also gives
# later years' ranges is quoted in fragments that name none of them (asserted), the note saying which range is the current year's
G = [
    (2022, "Q4 2021", ["For 2022, NextEra Energy now expects adjusted earnings per share to be in the range of $2.75 to $2.85, up from its "
                       "prior range of $2.55 to $2.75"], ""),
    (2022, "Q1 2022", ["For 2022, NextEra Energy continues to expect adjusted earnings per share to be in the range of $2.75 to $2.85"], ""),
    (2022, "2022-06-14", ["NEE is increasing its adjusted earnings per share expectations for 2022", "to be in the range of $2.80 to $2.90"],
     " (the first of the four ranges the sentence lists, one a year: 2022's)"),
    (2022, "Q2 2022", ["For 2022, NextEra Energy continues to expect adjusted earnings per share to be in the range of $2.80 to $2.90"], ""),
    (2022, "Q3 2022", ["For 2022, NextEra Energy continues to expect adjusted earnings per share to be in the range of $2.80 to $2.90"], ""),
    (2023, "Q4 2022", ["NextEra Energy continues to expect adjusted earnings per share to be in the ranges of $2.98 to $3.13"],
     " (the sentence's first range, for 2023; the second is the next year's)"),
    (2023, "Q1 2023", ["NextEra Energy continues to expect adjusted earnings per share to be in the ranges of $2.98 to $3.13"],
     " (the sentence's first range, for 2023; the second is the next year's)"),
    (2023, "Q2 2023", ["NextEra Energy continues to expect adjusted earnings per share to be in the ranges of $2.98 to $3.13"],
     " (the sentence's first range, for 2023; the second is the next year's)"),
    (2023, "Q3 2023", ["NextEra Energy continues to expect adjusted earnings per share to be in the ranges of $2.98 to $3.13"],
     " (the sentence's first range, for 2023; the second is the next year's)"),
    (2024, "Q4 2023", ["For 2024, NextEra Energy continues to expect adjusted earnings per share to be in the range of $3.23 to $3.43"], ""),
    (2024, "Q1 2024", ["For 2024, NextEra Energy continues to expect adjusted earnings per share to be in the range of $3.23 to $3.43"], ""),
    (2024, "2024-06-11", ["NEE is reaffirming its adjusted earnings per share expectations for 2024", "to be in the range of $3.23 to $3.43"],
     " (the first of the three ranges the sentence lists, one a year: 2024's)"),
    (2024, "Q2 2024", ["For 2024, NextEra Energy continues to expect adjusted earnings per share to be in the range of $3.23 to $3.43"], ""),
    (2024, "Q3 2024", ["For 2024, NextEra Energy continues to expect adjusted earnings per share to be in the range of $3.23 to $3.43"], ""),
    (2025, "Q4 2024", ["For 2025, NextEra Energy continues to expect adjusted earnings per share to be in the range of $3.45 to $3.70"], ""),
    (2025, "Q1 2025", ["For 2025, NextEra Energy continues to expect adjusted earnings per share to be in the range of $3.45 to $3.70"], ""),
    (2025, "Q2 2025", ["For 2025, NextEra Energy continues to expect adjusted earnings per share to be in the range of $3.45 to $3.70"], ""),
    (2025, "Q3 2025", ["For 2025, NextEra Energy continues to expect adjusted earnings per share to be in the range of $3.45 to $3.70"], ""),
    (2025, "2025-12-08", ["NEE is updating its adjusted earnings per share expectations by tightening the 2025 range to the high end",
                          "to be between $3.62 and $3.70"], " (the sentence's first range, 2025's; the second is the next year's)"),
    (2025, "2026-01-02", ["NEE continues to expect adjusted earnings per share for 2025", "to be between $3.62 and $3.70"],
     " (the sentence's first range, 2025's; the second is the next year's)"),
    (2026, "Q4 2025", ["NextEra Energy continues to expect 2026 adjusted earnings per share to be in the range of $3.92 to $4.02"], ""),
    (2026, "Q1 2026", ["NextEra Energy continues to expect 2026 adjusted earnings per share to be in the range of $3.92 to $4.02 and is "
                       "targeting the high end of that range"], ""),
    (2026, "Q2 2026", ["NextEra Energy continues to expect 2026 adjusted earnings per share to be in the range of $3.92 to $4.02 and is "
                       "targeting the high end of that range"], ""),
    (2026, "Q3 2026", ["NextEra Energy continues to expect 2026 adjusted earnings per share to be in the range of $3.92 to $4.02 and is "
                       "targeting the high end of that range"], ""),
]
new_guides = []
for fy, key, frags, note in G:
    if key in REL:
        acc, sid, d = REL[key], R_SRC[key], f"{key} release"
        path = doc(acc, "EX-99")
    else:
        acc, sid, d = FD[key], FD_SRC[key], f"8-K of {key} (Item 7.01)"
        path = doc(acc, "8-K")
    for t in frags:
        quote(path, t)
        later = {int(y) for y in re.findall(r"\b(20\d\d)\b", t)} - set(range(2000, fy + 1))
        assert not later, (key, "a guide quote names a later year", later)
    disp = " ... ".join(f"'{t}'" for t in frags) + note
    new_guides.append(dict(fy=fy, published=SRC[sid]["published"], source=sid, doc=d, display=disp, unused=UNUSED))
new_guides.sort(key=lambda g: (g["published"], g["fy"]))
assert len({(g["published"], g["fy"]) for g in new_guides}) == len(new_guides)

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
for key in ("sources", "history_vintages", "prints", "guides"):
    n_old = len(old[key])
    got = list(f[key].items())[:n_old] if key == "sources" else f[key][:n_old]
    want = list(old[key].items()) if key == "sources" else old[key]
    assert got == want, key
for key in ("rule_t", "eps_guides", "dividends", "events", "company_names", "listings", "distributions", "price_basis", "ticker",
            "splits"):
    assert f[key] == old[key], key
f["_doc"] = old["_doc"] + (
    " 2022-2026 (retro/README.md, 'NEE 2022-2026') was appended by retro/generators/nee/gen_nee_2226.py from the filings accepted "
    "2022-01-01 to 2026-11-22 (sources NE114 on), every earlier fact unchanged: the FY2021-FY2025 vintages take their three years from "
    "the statements of income (Item 6 reserved); each Q4 release's after-tax items face the AAPL FY2002 test and its mirror (not met); "
    "the Q4 2021 print's year-ago EPS is $0.00, so its EPS growth is None (n/m); the current-year adjusted EPS ranges of four Item 7.01 "
    "8-Ks are display-only guides.")
with open(FACTS, "w", encoding="utf-8") as fh:
    json.dump(f, fh, ensure_ascii=False, indent=1)
with open(A.checklist or os.path.join(SP, "checklist_nee_2226.json"), "w", encoding="utf-8") as fh:
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
