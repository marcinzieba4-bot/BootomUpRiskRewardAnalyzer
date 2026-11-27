#!/usr/bin/env python3
"""Extend retro/facts/SCHW.json with 2014-2017 (filings accepted 2014-01-01 to 2017-12-31), asserting that every earlier fact is
unchanged. Same discipline as gen_schw.py and gen_schw_1013.py: each figure from its own row by label, every rate computed, every
quote asserted present in its own filing, a verbatim checklist written. Run:

    python3 retro/tools/edgar.py fetch 316709 <dir> --from 2014-01-01 --to 2017-12-31 --forms 8-K 8-K/A 10-Q 10-K
    python3 -I retro/generators/schw/gen_schw_1417.py --filings <dir> [--facts-in <2008-2013 sheet>] [--out retro/facts/SCHW.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_schw_1417.json

--facts-in is the 2008-2013 sheet gen_schw_1013.py writes (default: retro/facts/SCHW.json, which must then hold 2008-2013 only).
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
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))       # retro/generators/schw -> the repository
_ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("--filings", required=True, help="folder edgar.py wrote (allrows.json, tenk/, tenq/, eightk/); keep it outside the repo")
_ap.add_argument("--facts-in", help="the 2008-2013 fact sheet to extend (default retro/facts/SCHW.json)")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/SCHW.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_schw_1417.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402

ET = ZoneInfo("America/New_York")
CUT = "2017-12-31"
FILINGS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("SCHW")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
CHECK = {}
TEXT = {}
norm = lambda s: re.sub(r"\s+", " ", s).strip()
FACTS = A.out or os.path.join(REPO, "retro", "facts", "SCHW.json")
old = json.load(open(A.facts_in or os.path.join(REPO, "retro", "facts", "SCHW.json"), encoding="utf-8"))
f = copy.deepcopy(old)


def doc(acc, prefix):
    for d in ("tenk", "tenq", "eightk"):
        p = os.path.join(SP, d, acc)
        if os.path.isdir(p):
            hits = sorted(x for x in os.listdir(p) if x.startswith(prefix) and x.endswith(".rows.txt"))
            assert hits, (acc, prefix)
            return os.path.join(p, hits[0])
    raise AssertionError(acc)


def lines(path):
    if path not in TEXT:
        TEXT[path] = [norm(x) for x in open(path, encoding="utf-8", errors="replace").read().split("\n")]
    return TEXT[path]


def quote(path, s):
    assert norm(s) in norm(" ".join(lines(path))), (path, s[:120])
    CHECK.setdefault(path, []).append(s)
    return s


def num(tok):
    t = tok.strip().replace("$", "").replace(",", "").strip()
    if t in ("—", "-", "–", ""):
        return 0.0
    neg = t.startswith("(") and (t.endswith(")") or t.endswith(")%"))
    v = float(t.strip("()%"))
    return -v if neg else v


def safe(t):
    try:
        return num(t)
    except ValueError:
        return None


def row(path, label, start=0, stop=None, n=None):
    L = lines(path)[start:stop]
    hits = list(dict.fromkeys(x for x in L if x.startswith(label)))      # a row repeated word for word counts once
    assert len(hits) == 1, (path, label, len(hits), hits[:3])
    vals = [safe(t) for t in hits[0].split("|")[1:]]
    out = vals[-n:] if n else vals
    assert None not in out, (path, label, hits[0])
    CHECK.setdefault(path, []).append(hits[0])
    return hits[0], out


def row_any(path, labels, start=0, stop=None, n=None):
    L = lines(path)[start:stop]
    for lab in labels:
        if any(x.startswith(lab) for x in L):
            return row(path, lab, start, stop, n)
    raise AssertionError((path, labels))


def line_no(path, startswith, nth=0, after=0):
    idx = [i for i, x in enumerate(lines(path)) if x.startswith(startswith) and i >= after]
    return idx[nth]


def next_tday(d):
    return min(x for x in TDAYS if x > d)


def published(acc):
    r = FILINGS[acc]
    t = dt.datetime.fromisoformat(r[1].replace("Z", "+00:00")).astimezone(ET)
    d = t.date().isoformat()
    assert d <= CUT, acc
    hm = t.strftime("%H:%M")
    if hm >= "16:00":
        return next_tday(d), f"accepted {d} {hm} ET (after the close), so dated the next trading day"
    if hm < "09:30":
        return d, f"accepted {d} {hm} ET (before the open)"
    return d, f"accepted {d} {hm} ET (during market hours)"


URL = lambda acc, fn: f"https://www.sec.gov/Archives/edgar/data/316709/{acc.replace('-', '')}/{fn}"
SRC = {}
nid = [46]


def source(acc, title, fn, supports):
    p, filed = published(acc)
    sid = f"SCHW{nid[0]}"
    nid[0] += 1
    SRC[sid] = dict(published=p, filed=filed, title=title, url=URL(acc, fn), supports=supports)
    return sid


r1 = lambda x: round(x + 0.0, 1)
r2 = lambda x: round(x + 0.0, 2)
pct = lambda a, b: (b / a - 1) * 100

def sub_row(path, header, label, start=0, stop=None, n=None, span=4):
    """A row under a header line ('Earnings per common share:' then 'Diluted |'), inside [start, stop)."""
    L = lines(path)
    stop = len(L) if stop is None else stop
    idx = [i for i in range(start, stop) if L[i].lower().startswith(header.lower())]
    assert idx, (path, header)
    return row(path, label, idx[0], min(idx[0] + span, stop), n)


def qcheck(path, labels, a, b):
    """The 10-Q reports the quarter's figure and the year-ago one: some row under one of the labels holds a then b as consecutive
    figures (percentage cells left out; the 10-Q layout changes from Q2 2015)."""
    for x in lines(path):
        if any(x.startswith(lab) for lab in labels):
            v = [safe(t) for t in x.split("|")[1:] if not t.strip().endswith("%")]
            if any(v[i] == a and v[i + 1] == b for i in range(len(v) - 1)):
                return True
    raise AssertionError((path, labels, a, b))


# ── filings, in publication order ───────────────────────────────────────────────────────────────────────────────────────
REL = {"Q4 2013": "0001193125-14-013017", "Q1 2014": "0001193125-14-144150", "Q2 2014": "0001193125-14-270260",
       "Q3 2014": "0000316709-14-000029", "Q4 2014": "0000316709-15-000005", "Q1 2015": "0000316709-15-000018",
       "Q2 2015": "0000316709-15-000036", "Q3 2015": "0000316709-15-000051", "Q4 2015": "0000316709-16-000063",
       "Q1 2016": "0000316709-16-000071", "Q2 2016": "0000316709-16-000090", "Q3 2016": "0000316709-16-000097",
       "Q4 2016": "0000316709-17-000004", "Q1 2017": "0000316709-17-000014", "Q2 2017": "0000316709-17-000031",
       "Q3 2017": "0000316709-17-000043"}
TENQ = {"Q1 2014": "0000316709-14-000012", "Q2 2014": "0000316709-14-000024", "Q3 2014": "0000316709-14-000039",
        "Q1 2015": "0000316709-15-000023", "Q2 2015": "0000316709-15-000043", "Q3 2015": "0000316709-15-000056",
        "Q1 2016": "0000316709-16-000078", "Q2 2016": "0000316709-16-000093", "Q3 2016": "0000316709-16-000101",
        "Q1 2017": "0000316709-17-000020", "Q2 2017": "0000316709-17-000034", "Q3 2017": "0000316709-17-000061"}
TENK = {"FY13": "0000316709-14-000005", "FY14": "0000316709-15-000014", "FY15": "0000316709-16-000067", "FY16": "0000316709-17-000010"}
FREL = {q: doc(a, "EX-99.1") for q, a in REL.items()}
FK = {k: doc(a, "10-K__") for k, a in TENK.items()}
FQ = {q: doc(a, "10-Q__") for q, a in TENQ.items()}

S = {}
order = [("Q4 2013", "rel"), ("FY13", "10k"), ("Q1 2014", "rel"), ("Q2 2014", "rel"), ("Q3 2014", "rel"), ("Q4 2014", "rel"),
         ("FY14", "10k"), ("Q1 2015", "rel"), ("Q2 2015", "rel"), ("Q3 2015", "rel"), ("Q4 2015", "rel"), ("FY15", "10k"),
         ("Q1 2016", "rel"), ("Q1 2016 10-Q", "10q"), ("Q2 2016", "rel"), ("Q3 2016", "rel"), ("Q4 2016", "rel"), ("FY16", "10k"),
         ("Q1 2017", "rel"), ("Q2 2017", "rel"), ("Q3 2017", "rel")]
for k, kind in order:
    if kind == "rel":
        S[k] = source(REL[k], f"Schwab {k} earnings release (8-K exhibit 99.1)", os.path.basename(FREL[k]).split("__")[1].replace(".rows.txt", ".htm"),
                      f"{k}" + (f" and FY{k[3:]}" if k.startswith("Q4") else "") + " statement of income, financial and operating "
                      "highlights, client assets and trades")
    elif kind == "10k":
        y = 2000 + int(k[2:])
        S[k] = source(TENK[k], f"The Charles Schwab Corporation FY{y} 10-K", os.path.basename(FK[k]).split("__")[1].replace(".rows.txt", ".htm"),
                      f"selected financial and operating data {y - 4}-{y}, the {y - 2}-{y} client metrics and statements of "
                      f"income: the FY{k[2:]} history vintage; Items 1, 1A and 5" + ("; the quarterly dividend rate declared on "
                                                                                     "January 26, 2017" if y == 2016 else ""))
    else:
        S[k] = source(TENQ["Q1 2016"], "The Charles Schwab Corporation Q1 2016 10-Q", os.path.basename(FQ["Q1 2016"]).split("__")[1].replace(".rows.txt", ".htm"),
                      "the quarterly dividend rate declared on April 21, 2016")

# ── the listing stays the NYSE (no move in 2014-2017) ───────────────────────────────────────────────────────────────────
LIST10 = "CSC’s common stock is listed on The New York Stock Exchange under the ticker symbol SCHW."
for k in FK:
    quote(FK[k], LIST10)

# ── history vintages FY13-FY16: the five-year selected data; earlier years from the latest earlier vintage ─────────────────
DEV = "Developments in the business, economic, and geopolitical environment could negatively impact the Company’s business."
COMP = "The Company’s industry is characterized by aggressive price competition."
SEG = "The Company provides financial services to individuals and institutional clients through two segments – Investor Services and Advisor Services."
OLD_DUR = old["history_vintages"][-1]["why"].split(" (FY2012 10-K); ")[1]
prev_v = old["history_vintages"][-1]
V = []


def sel_bounds(path):
    i0 = line_no(path, "Selected Financial and Operating Data")
    i1 = min(i for i, x in enumerate(lines(path)) if i > i0 and x.startswith("Item 7. |"))
    return i0, i1


def overview_bounds(path):
    i0 = line_no(path, "OVERVIEW", after=sel_bounds(path)[1])
    i1 = line_no(path, "Company Financial Metrics:", after=i0)
    return i0, i1


for k in ("FY13", "FY14", "FY15", "FY16"):
    fp, y = FK[k], 2000 + int(k[2:])
    years = list(range(y, y - 5, -1))
    b = sel_bounds(fp)
    if any(x.startswith("Diluted earnings per common share |") for x in lines(fp)[b[0]:b[1]]):
        re_, ve = row(fp, "Diluted earnings per common share |", *b, n=5)
        rs_, vs = row(fp, "Weighted-average common shares outstanding — diluted |", *b, n=5)
    else:                           # from the FY2015 10-K: 'Earnings per common share:' then 'Diluted |'
        re_, ve = sub_row(fp, "Earnings per common share:", "Diluted |", *b, n=5)
        rs_, vs = sub_row(fp, "Weighted average common shares outstanding:", "Diluted |", *b, n=5)
    rr_, vr = row(fp, "Net revenues |", *b, n=5)
    eps = {**prev_v["eps_normalized"], **{str(a): v for a, v in zip(years, ve)}}
    rev = {**prev_v["revenue_usd_b"], **{str(a): round(v / 1000, 3) for a, v in zip(years, vr)}}
    sh = {**prev_v["diluted_shares_m"], **{str(a): v for a, v in zip(years, vs)}}
    srcs = {**prev_v["eps_sources"], **{str(a): S[k] for a in years}}
    # every year a later 10-K reports equals the earlier vintage's figure (EPS, revenue, diluted shares)
    for a in years[1:]:
        if str(a) in prev_v["eps_normalized"]:
            assert (prev_v["eps_normalized"][str(a)], prev_v["revenue_usd_b"][str(a)], prev_v["diluted_shares_m"][str(a)]) == \
                (eps[str(a)], rev[str(a)], sh[str(a)]), (k, a)
    keep = sorted(eps)[-10:]                       # the ten fiscal years to the latest one (FY2003 leaves with the FY2013 10-K)
    eps, rev, sh, srcs = ({a: d[a] for a in keep} for d in (eps, rev, sh, srcs))
    # the statement of income: components, pre-tax income and taxes (three years, most recent first)
    L = lines(fp)
    i0 = [i for i, x in enumerate(L) if re.match(r"Asset management and administration fees( \(\d\))? \|", x) and len(x.split("|")) == 4][0]
    comp = {}
    for lab in ("Asset management and administration fees", "Net interest revenue", "Trading revenue"):
        r_, v_ = row_any(fp, [lab + " |", lab + " (1) |"], i0, i0 + 8, n=3)
        comp[lab] = (r_, v_)
    rt_, vt_ = row(fp, "Total net revenues |", i0, i0 + 14, n=3)
    ri_, vi_ = row(fp, "Income before taxes on income |", i0, i0 + 32, n=3)
    rx_, vx_ = row(fp, "Taxes on income |", i0, i0 + 34, n=3)
    assert vt_[0] == vr[0] and vt_[1] == vr[1], (k, "statement total vs selected data")
    other = [vt_[j] - sum(c[1][j] for c in comp.values()) for j in range(2)]
    groups = [[n, round(c[1][0] / 1000, 3), r1(pct(c[1][1], c[1][0]))] for n, c in comp.items()] + \
             [["Other (net of the provision for loan losses and impairment losses)", round(other[0] / 1000, 3), r1(pct(other[1], other[0]))]]
    pre, tax = vi_[0], abs(vx_[0])
    ob = overview_bounds(fp)
    rca, vca = row_any(fp, ["Client assets (in billions, at year end) |", "Client assets (2) (in billions, at year end) |"], *ob, n=3)
    rnn, vnn = row_any(fp, ["Net new client assets (in billions) |", "Net new client assets (1) (in billions) |"], *ob, n=3)
    item1 = quote(fp, re.search(r"engages, through its subsidiaries[^.]*\.", " ".join(L)).group(0))
    for s_ in (DEV, COMP, SEG):
        quote(fp, s_)
    low = " ".join(L).lower()
    for w in ("cyclic", "offshore", "e-commerce", "ecommerce", "streaming", "electric vehicle", "decarbon", "climate", "cryptocurrenc",
              "artificial intelligence"):
        assert w not in low, (k, w)
    # cloud: only in the accounting standard for fees paid in a cloud computing arrangement (ASU 2015-05), FY2015 and FY2016 10-Ks
    assert low.count("cloud") == low.count("cloud computing arrangement"), k
    cloud = None
    if "cloud" in low:
        cloud = quote(fp, re.search(r"[^.]*clarifies customer(?:’s|s’) accounting for fees paid in a cloud computing arrangement\.", " ".join(L)).group(0).strip())
    lab = f"FY{y % 100:02d}"
    why = f"'The Charles Schwab Corporation (CSC) ... {item1}' '{DEV}' '{COMP}' (FY{y} 10-K); {OLD_DUR}"
    m = r2(pre / vr[0] * 100)
    v = dict(
        published=SRC[S[k]]["published"], sources=list(dict.fromkeys([S[k]] + [srcs[a] for a in keep])), fy_label=lab, kind="DURABLE",
        why=why, eps_normalized=eps, eps_sources=srcs, eps_excluded={},
        # FY2002's exclusion note leaves with FY2003 (the ten years from FY2004; the CB 2014-2017 reading)
        eps_first_excluded={},
        revenue_usd_b=rev, revenue_sources=srcs, diluted_shares_m=sh, shares_sources=srcs, margin_signal_name="Pre-tax margin change",
        prev_fy_op_margin=m, prev_fy_op_margin_note=f"{lab} income before taxes on income ${pre:,.0f}M / net revenues ${vr[0]:,.0f}M",
        prev_fy_pretax_margin=m, prev_fy_pretax_margin_note=f"{lab} income before taxes on income ${pre:,.0f}M / net revenues ${vr[0]:,.0f}M",
        prev_fy_sales_growth=r1(pct(vr[1], vr[0])), prev_fy_client_assets_b=vca[0], prev_fy_client_assets_growth=r1(pct(vca[1], vca[0])),
        prev_fy_nna_b=vnn[0], tax_rate=round(tax / pre, 4), tax_note=f"{lab} taxes on income ${tax:,.0f}M on pre-tax ${pre:,.0f}M",
        dividend_annual=None, dividend_note=None,
        business_line="securities brokerage, banking and related financial services: Investor Services and Advisor Services "
                      "(two segments)",
        groups=groups, groups_basis=f"{lab} net revenues by component (asset management and administration fees, net interest revenue, "
                                    f"trading revenue, other net of the provision for loan losses and net impairment losses on "
                                    f"securities; {lab} growth)",
        company="The Charles Schwab Corporation", exchange="NYSE", pe_window_start="2003-01-01",
        fiscal_year="year ended December 31,", rows=[re_, rr_, rs_, rt_, ri_, rx_, rca, rnn] + [c[0] for c in comp.values()],
        # the note names only filings public by the vintage's own date: the releases' per-share tables start with Q3 2015
        normalization=("diluted EPS (no discontinued operation after 2008), each year from the latest filing that reports it, GAAP: no "
                       "filing publishes an EPS without the items the releases list" +
                       (f" (the {'Q3 and Q4 2015' if y == 2015 else 'Q3 2015 to Q4 2016'} releases' 'EPS Impact of Certain "
                        "Non-Recurring Items' tables give each item's per-share effect, never an EPS without them)" if y >= 2015 else
                        " (the releases state their combined effect, such as 'approximately $23 million, or $0.01 per share' in Q3 2014, "
                        "never an EPS without them)" if y == 2014 else "") +
                       ", and no year meets the AAPL FY2002 test (FY2010's $321M of listed charges after tax against its $454M net "
                       "income is the nearest)"))
    if cloud:
        v["cloud_words"] = cloud
    V.append(v)
    prev_v = v

# ── dividends: the latest declared quarterly rate, each from the first filing that states it ─────────────────────────────
D16 = "On April 21, 2016, the Board of Directors of the Company declared a one cent, or 17%, increase in the quarterly cash dividend to $0.07 per common share."
D17 = "On January 26, 2017, the Board of Directors of the Company declared a one cent, or 14%, increase in the quarterly cash dividend to $0.08 per common share."
quote(FQ["Q1 2016"], D16)
quote(FK["FY16"], D17)
for q in ("Q1 2014", "Q2 2014", "Q3 2014", "Q1 2015", "Q2 2015", "Q3 2015"):      # no new rate before the Q1 2016 10-Q
    assert "increase in the quarterly cash dividend" not in " ".join(lines(FQ[q])), q
new_divs = [dict(published=SRC[S["Q1 2016 10-Q"]]["published"], quarterly=0.07, source=S["Q1 2016 10-Q"],
                 note=f"$0.07 a quarter: '{D16}' (Q1 2016 10-Q)"),
            dict(published=SRC[S["FY16"]]["published"], quarterly=0.08, source=S["FY16"], note=f"$0.08 a quarter: '{D17}' (FY2016 10-K)")]

# ── prints Q4 2013 - Q3 2017 ─────────────────────────────────────────────────────────────────────────────────────────────
Q_END = {1: "March", 2: "June", 3: "September", 4: "December"}
PE = {1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"}
Q115 = ("our expected overall expense growth remains at a modest pace of approximately 4% for 2015 and we are well positioned to "
        "translate business growth into improving financial performance as the year continues.")
OUTLOOK = {
    "Q1 2015": dict(outlook_fy=2015, outlook_words=Q115,
                    outlook_reading="a cost component (the Q1 2010 reading of 'limit expense growth to about 4%'), no field"),
}
UNFILED = {"Q1 2015": "These results lag the outlook expressed in the company’s press release dated March 13, 2015, primarily due to the "
                      "earlier timing of certain compensation expenses."}
NOTES = {
    "Q3 2014": ["Taken together, these two items reduced pre-tax income by approximately $23 million, or $0.01 per share."],
    "Q4 2014": ["Taken together, these items increased pre-tax income by approximately $20 million, or $0.01 per share."],
    "Q3 2015": ["EPS Impact of Certain Non-Recurring Items"],
    "Q4 2015": ["EPS Impact of Certain Non-Recurring Items (1)"],
    "Q4 2016": ["EPS Impact of Certain Non-Recurring Items"],
}
NOTE_TXT = {
    "Q3 2014": "GAAP: the insurance recovery and the geographic footprint charge stay in (no filing publishes an EPS without them)",
    "Q4 2014": "GAAP: FY14 $0.95 with the litigation proceeds, the securities losses, the insurance recovery and the footprint charge in",
    "Q1 2015": "GAAP; the release's outlook reference is to a press release of March 13, 2015 that was not filed (unused, the CRM rule)",
    "Q3 2015": "GAAP: the release's table gives each non-recurring item's per-share effect, not an EPS without them, so the items stay in",
    "Q4 2015": "GAAP: FY15 $1.03 with the litigation proceeds and the tax benefits in; the release's table gives each "
               "item's per-share effect, not an EPS without them",
    "Q4 2016": "GAAP: FY16 $1.31 with the litigation proceeds in; the release's table gives each item's per-share effect, not an EPS "
               "without them",
}
new_prints = []
for q in REL:
    fp = FREL[q]
    qn, fy = int(q[1]), int(q[3:])
    L = lines(fp)
    h0 = line_no(fp, "Financial and Operating Highlights")
    c0 = [i for i, x in enumerate(L) if x.startswith("Growth in Client Assets and Accounts")][-1]
    rr, vr = row(fp, "Total net revenues |", h0, c0, n=5)
    re_, ve = row(fp, "Total expenses excluding interest |", h0, c0, n=5)
    rp, vp = row(fp, "Income before taxes on income |", h0, c0, n=5)
    rd, vd = row(fp, "Revenue trades (", h0, c0, n=5)
    if any(x.startswith("Diluted earnings per common share |") for x in L[h0:c0]):
        reps, veps = row(fp, "Diluted earnings per common share |", h0, c0, n=5)
    else:
        reps, veps = sub_row(fp, "Earnings per common share:", "Diluted |", h0, c0, n=5)
    wl = sorted({x.split(" |")[0] for x in L[h0:c0] if re.match(r"weighted-average common shares ?outstanding ?[—–-] ?diluted", x.lower())})
    if wl:                          # 'outstanding — diluted', 'outstanding–diluted', 'outstanding - diluted' (to Q4 2014)
        assert len(wl) == 1, (q, wl)
        rsh, vsh = row(fp, wl[0] + " |", h0, c0, n=5)
    else:
        rsh, vsh = sub_row(fp, "Weighted-average common shares outstanding:", "Diluted |", h0, c0, n=5)
    rc, vc = row(fp, "Total client assets |", c0, c0 + 45, n=5)
    rn, vn = row_any(fp, ["Total net new assets |", "Total net new client assets |"], c0, c0 + 70, n=5)
    eps_q, eps_q0 = veps[0], veps[4]
    if q in FQ:                     # the 10-Q reports the same quarter: revenue, expenses, pre-tax income, trades, client assets
        Fq = FQ[q]
        qcheck(Fq, ["Total net revenues |"], vr[0], vr[4])
        qcheck(Fq, ["Total expenses excluding interest |"], ve[0], ve[4])
        qcheck(Fq, ["Income before taxes on income |"], vp[0], vp[4])
        qcheck(Fq, ["Client assets (in billions, at quarter end) |", "Client assets (2) (in billions, at quarter end) |"], vc[0], vc[4])
        if any(x.startswith("Daily average revenue trades") and "|" in x for x in lines(Fq)):
            qcheck(Fq, ["Daily average revenue trades"], vd[0], vd[4])
    raw = dict(revenue_m=vr[0], revenue_prior_m=vr[4], revenue_prev_q_m=vr[1], expense_m=ve[0], expense_prior_m=ve[4], pretax_m=vp[0],
               pretax_prior_m=vp[4], client_assets_b=vc[0], client_assets_prior_b=vc[4], dart_k=vd[0], dart_prior_k=vd[4], nna_b=vn[0])

    def derive(rw):
        pm, pm0 = rw["pretax_m"] / rw["revenue_m"] * 100, rw["pretax_prior_m"] / rw["revenue_prior_m"] * 100
        return dict(sales_pct=r1(pct(rw["revenue_prior_m"], rw["revenue_m"])), seq_pct=r1(pct(rw["revenue_prev_q_m"], rw["revenue_m"])),
                    pretax_margin=r2(pm), pretax_margin_bp=r1((pm - pm0) * 100), expense_pct=r1(pct(rw["expense_prior_m"], rw["expense_m"])),
                    expense_gap_pp=r1(pct(rw["expense_prior_m"], rw["expense_m"]) - pct(rw["revenue_prior_m"], rw["revenue_m"])),
                    ca_pct=r1(pct(rw["client_assets_prior_b"], rw["client_assets_b"])), dart_pct=r1(pct(rw["dart_prior_k"], rw["dart_k"])))
    d = derive(raw)
    pub, filed = SRC[S[q]]["published"], SRC[S[q]]["filed"]
    rel_date = dt.date.fromisoformat(pub)
    note = NOTE_TXT.get(q, "")
    for s_ in NOTES.get(q, []):
        quote(fp, s_)
    if NOTES.get(q) and q in ("Q3 2014", "Q4 2014"):
        note += " (" + " ".join(f"'{s_}'" for s_ in NOTES[q]) + ")"
    if q in UNFILED:
        quote(fp, UNFILED[q])
        note += f" ('{UNFILED[q]}')"
    p = dict(quarter=q, fy=fy, q=qn, published=pub, source=S[q], release=f"{rel_date:%b} {rel_date.day}",
             release_time=f"8-K {filed}; no filing states the release time", period_end=f"{fy}-{PE[qn]}", raw=raw,
             rows=dict(rev=rr, exp=re_, pre=rp, dart=rd, ca=rc, nna=rn, eps=reps, shares=rsh),
             sales_b=round(vr[0] / 1000, 3), ca_b=vc[0], dart_k=vd[0], nna_b=vn[0], **d, eps_q=eps_q, eps_q_prior=eps_q0,
             diluted_shares_m=vsh[0],
             sales_note=f"net revenues ${vr[0]:,.0f}M vs ${vr[4]:,.0f}M a year earlier, ${vr[1]:,.0f}M the quarter before",
             client_note=f"client assets ${vc[0]:,.1f}B vs ${vc[4]:,.1f}B a year earlier; net new client assets ${vn[0]:,.1f}B in the "
                         f"quarter; daily average revenue trades {vd[0]:,.1f}K vs {vd[4]:,.1f}K",
             eps_note=f"diluted EPS ${eps_q:.2f} vs ${eps_q0:.2f}, GAAP (per common share, after preferred dividends)",
             shares_note=f"diluted shares {vsh[0]:,.0f}M; expenses excluding interest ${ve[0]:,.0f}M vs ${ve[4]:,.0f}M",
             next_print=f"Q{qn % 4 + 1} {fy + (1 if qn == 4 else 0)} print (the quarter ends in {Q_END[qn % 4 + 1]})", note=note)
    if q in OUTLOOK:
        quote(fp, OUTLOOK[q]["outlook_words"])
        p.update(OUTLOOK[q])
    if qn == 4:
        s0 = line_no(fp, "Consolidated Statements of Income")
        rfr, vfr = row(fp, "Total net revenues |", s0, h0)
        rfp, vfp = row(fp, "Income before taxes on income |", s0, h0)
        rft, vft = row(fp, "Taxes on income |", s0, h0)
        if any(x.startswith("Weighted-Average Common Shares Outstanding — Diluted |") for x in L[s0:h0]):
            rfs, vfs = row(fp, "Weighted-Average Common Shares Outstanding — Diluted |", s0, h0, n=4)
            rfe, vfe = row(fp, "Earnings Per Common Share — Diluted |", s0, h0, n=4)
        else:
            rfs, vfs = sub_row(fp, "Weighted-Average Common Shares Outstanding:", "Diluted |", s0, h0, n=4)
            rfe, vfe = sub_row(fp, "Earnings Per Common Share:", "Diluted |", s0, h0, n=4)
        rev_y, pre_y, tax_y, sh_y, eps_y = vfr[2], vfp[2], abs(vft[2]), vfs[2], vfe[2]
        want = {2013: 0.78, 2014: 0.95, 2015: 1.03, 2016: 1.31}[fy]
        assert eps_y == want, (q, eps_y)
        m = r2(pre_y / rev_y * 100)
        lab = f"FY{fy % 100:02d}"
        p["fy_actual"] = dict(
            fy=fy, fy_label=lab, eps_normalized=eps_y, revenue_usd_b=round(rev_y / 1000, 3), diluted_shares_m=sh_y,
            normalization_note=f"{lab} ${eps_y:.2f}, diluted EPS, GAAP ({q} release)",
            op_margin=m, op_margin_note=f"{lab} income before taxes on income ${pre_y:,.0f}M / net revenues ${rev_y:,.0f}M ({q} release)",
            pretax_margin=m, pretax_margin_note=f"{lab} income before taxes on income ${pre_y:,.0f}M / net revenues ${rev_y:,.0f}M ({q} release)",
            sales_growth=r1(pct(vfr[3], vfr[2])), client_assets_b=vc[0], client_assets_growth=d["ca_pct"],
            tax_rate=round(tax_y / pre_y, 4), tax_note=f"{lab} taxes on income ${tax_y:,.0f}M on pre-tax ${pre_y:,.0f}M",
            rows=[rfr, rfp, rft, rfs, rfe])
    new_prints.append(p)

# ── checks against the vintages: each Q4 print's full year equals the 10-K that follows it ───────────────────────────────
for p in new_prints:
    a = p.get("fy_actual")
    if a:
        v = [x for x in V if x["fy_label"] == a["fy_label"]]
        assert v, p["quarter"]
        y = str(a["fy"])
        assert (v[0]["eps_normalized"][y], v[0]["revenue_usd_b"][y], v[0]["diluted_shares_m"][y]) == \
            (a["eps_normalized"], a["revenue_usd_b"], a["diluted_shares_m"]), (p["quarter"], "Q4 vs 10-K")
# the Q3 2014 print's year-ago client assets are Q3 2013's as published after the recordkeeping consolidation (the seam closes)
assert [p for p in new_prints if p["quarter"] == "Q3 2014"][0]["raw"]["client_assets_prior_b"] == old["prints"][-1]["raw"]["client_assets_b"]

# ── assemble: the earlier facts unchanged ────────────────────────────────────────────────────────────────────────────────
for k in SRC:
    assert k not in f["sources"]
f["sources"].update(SRC)
f["history_vintages"] += V
f["prints"] += new_prints
f["dividends"] += new_divs
f["_doc"] = old["_doc"]
for key in ("sources", "history_vintages", "prints", "dividends"):
    n_old = len(old[key])
    got = list(f[key].items())[:n_old] if key == "sources" else f[key][:n_old]
    want = list(old[key].items()) if key == "sources" else old[key]
    assert got == want, key
for key in ("rule_t", "guides", "events", "company_names", "splits", "listings", "fiscal_calendar", "price_basis", "ticker"):
    assert f[key] == old[key], key
assert [p["published"] for p in f["prints"]] == sorted(p["published"] for p in f["prints"])
with open(FACTS, "w", encoding="utf-8") as fh:
    json.dump(f, fh, ensure_ascii=False, indent=1)
with open(A.checklist or os.path.join(SP, "checklist_schw_1417.json"), "w", encoding="utf-8") as fh:
    json.dump(CHECK, fh, ensure_ascii=False, indent=1)
print(len(SRC), "sources,", len(V), "vintages,", len(new_prints), "prints,", len(new_divs), "dividends;",
      sum(len(v) for v in CHECK.values()), "checklist strings")
for p in new_prints:
    print(p["quarter"], p["published"], p["sales_pct"], p["ca_pct"], p["expense_gap_pp"], p["dart_pct"], p["pretax_margin_bp"], p["eps_q"])
for v in V:
    print(v["published"], v["fy_label"], v["eps_normalized"], v["prev_fy_op_margin"], v["groups"], v["prev_fy_client_assets_b"], v["prev_fy_nna_b"])
for k, s in SRC.items():
    print(k, s["published"], s["filed"], s["title"][:60])
