#!/usr/bin/env python3
"""Extend retro/facts/SCHW.json with 2018-2021 (filings accepted 2018-01-01 to 2021-12-31), asserting that every earlier fact is
unchanged. Same discipline as gen_schw.py, gen_schw_1013.py and gen_schw_1417.py: each figure from its own row by label, every rate
computed, every quote asserted present in its own filing, a verbatim checklist written. Run:

    python3 retro/tools/edgar.py fetch 316709 <dir> --from 2018-01-01 --to 2021-12-31 --forms 8-K 8-K/A 10-Q 10-K
    python3 -I retro/generators/schw/gen_schw_1821.py --filings <dir> [--facts-in <2008-2017 sheet>] [--out retro/facts/SCHW.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_schw_1821.json

--facts-in is the 2008-2017 sheet gen_schw_1417.py writes (default: retro/facts/SCHW.json, which must then hold 2008-2017 only).
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
_ap.add_argument("--facts-in", help="the 2008-2017 fact sheet to extend (default retro/facts/SCHW.json)")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/SCHW.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_schw_1821.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402

ET = ZoneInfo("America/New_York")
CUT = "2021-12-31"
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
nid = [67]


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
REL = {"Q4 2017": "0000316709-18-000004", "Q1 2018": "0000316709-18-000019", "Q2 2018": "0000316709-18-000036",
       "Q3 2018": "0000316709-18-000047", "Q4 2018": "0000316709-19-000004", "Q1 2019": "0000316709-19-000012",
       "Q2 2019": "0000316709-19-000030", "Q3 2019": "0000316709-19-000048", "Q4 2019": "0000316709-20-000005",
       "Q1 2020": "0000316709-20-000016", "Q2 2020": "0000316709-20-000036", "Q3 2020": "0000316709-20-000050",
       "Q4 2020": "0000316709-21-000005", "Q1 2021": "0000316709-21-000024", "Q2 2021": "0000316709-21-000057",
       "Q3 2021": "0000316709-21-000072"}
TENQ = {"Q1 2018": "0000316709-18-000024", "Q2 2018": "0000316709-18-000040", "Q3 2018": "0000316709-18-000054",
        "Q1 2019": "0000316709-19-000017", "Q2 2019": "0000316709-19-000039", "Q3 2019": "0000316709-19-000052",
        "Q1 2020": "0000316709-20-000021", "Q2 2020": "0000316709-20-000045", "Q3 2020": "0000316709-20-000054",
        "Q1 2021": "0000316709-21-000029", "Q2 2021": "0000316709-21-000062", "Q3 2021": "0000316709-21-000081"}
TENK = {"FY17": "0000316709-18-000009", "FY18": "0000316709-19-000008", "FY19": "0000316709-20-000012", "FY20": "0000316709-21-000012"}
FREL = {q: doc(a, "EX-99.1") for q, a in REL.items()}
FK = {k: doc(a, "10-K__") for k, a in TENK.items()}
FQ = {q: doc(a, "10-Q__") for q, a in TENQ.items()}
DIV_DECL = {"FY17": "January 25, 2018", "FY18": "January 30, 2019", "FY19": "January 30, 2020"}

S = {}
order = [("Q4 2017", "rel"), ("FY17", "10k"), ("Q1 2018", "rel"), ("Q2 2018", "rel"), ("Q2 2018 10-Q", "10q"), ("Q3 2018", "rel"),
         ("Q4 2018", "rel"), ("FY18", "10k"), ("Q1 2019", "rel"), ("Q2 2019", "rel"), ("Q3 2019", "rel"), ("Q4 2019", "rel"),
         ("FY19", "10k"), ("Q1 2020", "rel"), ("Q2 2020", "rel"), ("Q3 2020", "rel"), ("Q4 2020", "rel"), ("FY20", "10k"),
         ("Q1 2021", "rel"), ("Q2 2021", "rel"), ("Q3 2021", "rel")]
for k, kind in order:
    if kind == "rel":
        S[k] = source(REL[k], f"Schwab {k} earnings release (8-K exhibit 99.1)", os.path.basename(FREL[k]).split("__")[1].replace(".rows.txt", ".htm"),
                      f"{k}" + (f" and FY{k[3:]}" if k.startswith("Q4") else "") + " statement of income, financial and operating "
                      "highlights, client assets and trades")
    elif kind == "10k":
        y = 2000 + int(k[2:])
        S[k] = source(TENK[k], f"The Charles Schwab Corporation FY{y} 10-K", os.path.basename(FK[k]).split("__")[1].replace(".rows.txt", ".htm"),
                      f"selected financial and operating data {y - 4}-{y}, the {y - 2}-{y} client metrics and statements of "
                      f"income: the FY{k[2:]} history vintage; Items 1, 1A and 5" + (f"; the quarterly dividend rate declared on "
                                                                                     f"{DIV_DECL[k]}" if k in DIV_DECL else ""))
    else:
        S[k] = source(TENQ["Q2 2018"], "The Charles Schwab Corporation Q2 2018 10-Q", os.path.basename(FQ["Q2 2018"]).split("__")[1].replace(".rows.txt", ".htm"),
                      "the quarterly dividend rate declared on July 25, 2018")

# ── the listing stays the NYSE (no move in 2018-2021) ───────────────────────────────────────────────────────────────────
LIST10 = "CSC’s common stock is listed on The New York Stock Exchange under the ticker symbol SCHW."
for k in FK:
    quote(FK[k], LIST10)

# ── history vintages FY17-FY20: the five-year selected data; earlier years from the latest earlier vintage ─────────────────
DEV = "Developments in the business, economic, and geopolitical environment could negatively impact our business."
SEG = "Schwab provides financial services to individuals and institutional clients through two segments – Investor Services and Advisor Services."
OLD_DUR = old["history_vintages"][-1]["why"].split(" 10-K); ", 1)[1]
prev_v = old["history_vintages"][-1]
V = []


def sel_bounds(path):
    i0 = line_no(path, "Selected Financial and Operating Data")
    i1 = min(i for i, x in enumerate(lines(path)) if i > i0 and x.startswith("Item 7."))
    return i0, i1


def overview_bounds(path):
    i0 = line_no(path, "OVERVIEW", after=sel_bounds(path)[1])
    i1 = line_no(path, "Company Financial Metrics", after=i0)
    return i0, i1


def sub_any(path, headers, label, start=0, stop=None, n=None):
    for hd in headers:
        if any(x.lower().startswith(hd.lower()) for x in lines(path)[start:stop]):
            return sub_row(path, hd, label, start, stop, n)
    raise AssertionError((path, headers))


NORM = {
    2017: ("the Q4 2017 release states the tax reform legislation's one-time tax expense ('a one-time tax expense of approximately $46 million "
           "decreased earnings per share by $0.03'), never an EPS without it"),
    2018: ("the Q4 2017 release states the tax reform legislation's one-time tax expense as '$0.03' of EPS, never an EPS without it; no release "
           "of 2018 lists an item"),
    2019: ("the Q3 and Q4 2019 releases state the severance charges ('reduced earnings per share by $.04') and the acquisition-related "
           "expenses ('reduced fourth quarter and full-year earnings per share by $.01'), never an EPS without them"),
    2020: ("from Q2 2020 the releases' adjusted diluted EPS also excludes the amortization of acquired intangible assets, which 'will "
           "continue in future periods over their remaining useful lives', a recurring item, so it is not a figure excluding only "
           "one-offs (the NKE FY2007, AVGO, PFE and V rule)"),
}
AAPL_NOTE = {2017: "FY2010's $321M of listed charges after tax against its $454M net income is the nearest",
             2018: "FY2010's $321M of listed charges after tax against its $454M net income is the nearest",
             2019: "FY2010's $321M of listed charges after tax against its $454M net income is the nearest",
             2020: "FY2020's $442M of acquisition and integration-related costs before tax against its $3,299M net income is the nearest"}
for k in ("FY17", "FY18", "FY19", "FY20"):
    fp, y = FK[k], 2000 + int(k[2:])
    years = list(range(y, y - 5, -1))
    b = sel_bounds(fp)
    re_, ve = sub_row(fp, "Earnings per common share:", "Diluted |", *b, n=5)
    rs_, vs = sub_any(fp, ["Weighted average common shares outstanding:", "Weighted-average common shares outstanding:"], "Diluted |", *b, n=5)
    rr_, vr = row_any(fp, ["Net revenues |", "Total net revenues |"], *b, n=5)
    eps = {**prev_v["eps_normalized"], **{str(a): v for a, v in zip(years, ve)}}
    rev = {**prev_v["revenue_usd_b"], **{str(a): round(v / 1000, 3) for a, v in zip(years, vr)}}
    sh = {**prev_v["diluted_shares_m"], **{str(a): v for a, v in zip(years, vs)}}
    srcs = {**prev_v["eps_sources"], **{str(a): S[k] for a in years}}
    # every year a later 10-K reports equals the earlier vintage's figure (EPS, revenue, diluted shares)
    for a in years[1:]:
        if str(a) in prev_v["eps_normalized"]:
            assert (prev_v["eps_normalized"][str(a)], prev_v["revenue_usd_b"][str(a)], prev_v["diluted_shares_m"][str(a)]) == \
                (eps[str(a)], rev[str(a)], sh[str(a)]), (k, a)
    keep = sorted(eps)[-10:]                       # the ten fiscal years to the latest one (FY2007 leaves with the FY2017 10-K)
    eps, rev, sh, srcs = ({a: d[a] for a in keep} for d in (eps, rev, sh, srcs))
    # the statement of income: components, pre-tax income and taxes (three years, most recent first); net interest revenue
    # comes before the fees from the FY2017 10-K
    L = lines(fp)
    i0 = [i for i, x in enumerate(L) if re.match(r"Asset management and administration fees( \(\d\))? \|", x) and len(x.split("|")) == 4][0]
    comp = {}
    for lab, a0, a1 in (("Asset management and administration fees", i0, i0 + 1), ("Net interest revenue", i0 - 6, i0),
                        ("Trading revenue", i0, i0 + 4)):
        r_, v_ = row_any(fp, [lab + " |", lab + " (1) |", lab + " (2) |"], a0, a1, n=3)
        comp[lab] = (r_, v_)
    rt_, vt_ = row(fp, "Total net revenues |", i0, i0 + 8, n=3)
    ri_, vi_ = row(fp, "Income before taxes on income |", i0, i0 + 30, n=3)
    rx_, vx_ = row_any(fp, ["Taxes on income |", "Taxes on income (2) |"], i0, i0 + 32, n=3)
    assert vt_[0] == vr[0] and vt_[1] == vr[1], (k, "statement total vs selected data")
    other = [vt_[j] - sum(c[1][j] for c in comp.values()) for j in range(2)]
    oth_name = ("Other (bank deposit account fees from TD Ameritrade's insured deposit account agreement, and other revenue)" if y == 2020
                else "Other (net of the provision for loan losses)" if y == 2017 else "Other")
    groups = [[n, round(c[1][0] / 1000, 3), r1(pct(c[1][1], c[1][0]))] for n, c in comp.items()] + \
             [[oth_name, round(other[0] / 1000, 3), r1(pct(other[1], other[0]))]]
    pre, tax = vi_[0], abs(vx_[0])
    ob = overview_bounds(fp)
    rca, vca = row_any(fp, ["Client assets (in billions, at year end) |", "Client assets (2) (in billions, at year end) |",
                            "Client assets (in billions, at year end) (2) |"], *ob, n=3)
    rnn, vnn = row_any(fp, ["Net new client assets (in billions) |", "Net new client assets (1) (in billions) |",
                            "Net new client assets (in billions) (1) |", "Core net new client assets (in billions) |"], *ob, n=3)
    item1 = quote(fp, re.search(r"engages, through its subsidiaries[^.]*\.", " ".join(L)).group(0))
    comp_s = quote(fp, re.search(r"Our industry is (?:highly competitive and )?characterized by aggressive price competition\.", " ".join(L)).group(0))
    for s_ in (DEV, SEG):
        quote(fp, s_)
    low = " ".join(L).lower()
    for w in ("offshore", "e-commerce", "ecommerce", "streaming", "electric vehicle", "decarbon", "cryptocurrenc", "crypto",
              "digital asset", "bitcoin", "blockchain", "distributed ledger", "artificial intelligence"):
        assert w not in low, (k, w)
    assert low.count("cyclical") == low.count("countercyclical"), (k, "cyclical")      # only the countercyclical capital buffer
    assert low.count("climate") == low.count("unprecedented climate"), (k, "climate")  # FY2020: 'amidst an unprecedented climate'
    # cloud: only in the accounting standard for implementation costs in a cloud computing arrangement (ASU 2018-15), FY2018-FY2020
    assert low.count("cloud") == low.count("cloud computing arrangement"), k
    cloud = None
    if "cloud" in low:
        cloud = quote(fp, re.search(r"ASU 2018-15, “Intangibles–\s?Goodwill and Other–Internal-Use Software \(Subtopic 350-40\): Customer’s "
                                    r"Accounting for Implementation Costs Incurred in a Cloud Computing Arrangement That Is a Service "
                                    r"Contract \(a consensus of the FASB Emerging Issues Task Force\)”", " ".join(L)).group(0))
    lab = f"FY{y % 100:02d}"
    why = f"'The Charles Schwab Corporation (CSC) ... {item1}' '{DEV}' '{comp_s}' (FY{y} 10-K); {OLD_DUR}"
    m = r2(pre / vr[0] * 100)
    v = dict(
        published=SRC[S[k]]["published"], sources=list(dict.fromkeys([S[k]] + [srcs[a] for a in keep])), fy_label=lab, kind="DURABLE",
        why=why, eps_normalized=eps, eps_sources=srcs, eps_excluded={}, eps_first_excluded={},
        revenue_usd_b=rev, revenue_sources=srcs, diluted_shares_m=sh, shares_sources=srcs, margin_signal_name="Pre-tax margin change",
        prev_fy_op_margin=m, prev_fy_op_margin_note=f"{lab} income before taxes on income ${pre:,.0f}M / net revenues ${vr[0]:,.0f}M",
        prev_fy_pretax_margin=m, prev_fy_pretax_margin_note=f"{lab} income before taxes on income ${pre:,.0f}M / net revenues ${vr[0]:,.0f}M",
        prev_fy_sales_growth=r1(pct(vr[1], vr[0])), prev_fy_client_assets_b=vca[0], prev_fy_client_assets_growth=r1(pct(vca[1], vca[0])),
        prev_fy_nna_b=vnn[0], tax_rate=round(tax / pre, 4), tax_note=f"{lab} taxes on income ${tax:,.0f}M on pre-tax ${pre:,.0f}M",
        dividend_annual=None, dividend_note=None,
        business_line="securities brokerage, banking and related financial services: Investor Services and Advisor Services "
                      "(two segments)",
        groups=groups, groups_basis=f"{lab} net revenues by component (asset management and administration fees, net interest revenue, "
                                    f"trading revenue, other; {lab} growth, each component as the {lab} 10-K reports both years)",
        company="The Charles Schwab Corporation", exchange="NYSE", pe_window_start="2003-01-01",
        fiscal_year="year ended December 31,", rows=[re_, rr_, rs_, rt_, ri_, rx_, rca, rnn] + [c[0] for c in comp.values()],
        normalization=("diluted EPS (no discontinued operation after 2008), each year from the latest filing that reports it, GAAP: no "
                       f"filing publishes an EPS without the items the releases list ({NORM[y]}), and no year meets the AAPL FY2002 "
                       f"test ({AAPL_NOTE[y]})"))
    if y == 2020:
        v["acquisition_note"] = ("TD Ameritrade from its acquisition on October 6, 2020 (and USAA's Investment Management Company from "
                                 "May 26, 2020) in the figures as published; nothing is made pro forma")
    if cloud:
        v["cloud_words"] = cloud
    V.append(v)
    prev_v = v

# ── dividends: the latest declared quarterly rate, each from the first filing that states it ─────────────────────────────
D18 = "On January 25, 2018, the Board of Directors of the Company declared a two cent, or 25% increase in the quarterly cash dividend to $0.10 per common share."
D18b = "On July 25, 2018, the Board of Directors of the Company declared a three cent, or 30%, increase in the quarterly cash dividend to $.13 per common share."
D19 = "On January 30, 2019, CSC publicly announced that its Board of Directors authorized a new Share Repurchase Program to repurchase up to $4.0 billion of common stock, and declared a four cent, or 31%, increase in the quarterly cash dividend to $0.17 per common share."
D20 = "On January 30, 2020, the Board of Directors of the Company declared a one cent, or 6%, increase in the quarterly cash dividend to $0.18 per common share."
quote(FK["FY17"], D18)
quote(FQ["Q2 2018"], D18b)
quote(FK["FY18"], D19)
quote(FK["FY19"], "In addition, o" + D20[1:])
# the Q1 2018 10-Q repeats the $0.10 increase after the FY2017 10-K; the $0.13 increase (July 25, 2018) follows the Q2 2018 release
assert published(TENQ["Q1 2018"])[0] > SRC[S["FY17"]]["published"] and SRC[S["Q2 2018"]]["published"] < "2018-07-25"
for q in ("Q1 2021", "Q2 2021", "Q3 2021"):      # no new rate in 2021 (the FY2020 10-K states none either)
    assert "increase in the quarterly cash dividend" not in " ".join(lines(FQ[q])), q
assert "2021, the Board of Directors of the Company declared" not in " ".join(lines(FK["FY20"])), "FY20"
for q in REL:                                   # no release states a new rate before its filing
    t = " ".join(lines(FREL[q]))
    if re.search(r"increase in the quarterly cash dividend to \$0?\.1", t):   # Q3 2018 repeats the July increase, after its 10-Q
        assert q == "Q3 2018" and SRC[S[q]]["published"] > SRC[S["Q2 2018 10-Q"]]["published"], q
new_divs = [dict(published=SRC[S["FY17"]]["published"], quarterly=0.10, source=S["FY17"], note=f"$0.10 a quarter: '{D18}' (FY2017 10-K)"),
            dict(published=SRC[S["Q2 2018 10-Q"]]["published"], quarterly=0.13, source=S["Q2 2018 10-Q"],
                 note=f"$0.13 a quarter: '{D18b}' (Q2 2018 10-Q)"),
            dict(published=SRC[S["FY18"]]["published"], quarterly=0.17, source=S["FY18"], note=f"$0.17 a quarter: '{D19}' (FY2018 10-K)"),
            dict(published=SRC[S["FY19"]]["published"], quarterly=0.18, source=S["FY19"], note=f"$0.18 a quarter: '{D20}' (FY2019 10-K)")]

# ── prints Q4 2017 - Q3 2021 ─────────────────────────────────────────────────────────────────────────────────────────────
Q_END = {1: "March", 2: "June", 3: "September", 4: "December"}
PE = {1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"}
ADJ = ("Amortization of acquired intangible assets will continue in future periods over their remaining useful lives.")
UNFILED = {
    "Q4 2017": "The company has scheduled a Business Update for institutional investors on Tuesday, February 6, 2018.",
    "Q1 2018": "While these factors contributed to outlays that were a bit above our initial expectations, the expense scenario we shared at our Winter Business Update incorporated slightly elevated quarterly comparisons during the first half of 2018.",
    "Q2 2018": "The company’s year-to-date balance sheet growth of nearly 8% is tracking with the expectation we laid out in February of at least 15% growth for 2018.",
    "Q4 2018": "The company has scheduled a Business Update for institutional investors on Tuesday, February 5, 2019.",
    "Q4 2019": "which was just shy of the range we outlined at the beginning of the year.",
    "Q2 2020": "largely consistent with the expectations we laid out during our Spring Business Update.",
    "Q3 2020": "The company has scheduled a Fall Business Update for institutional investors on Thursday, October 29, 2020.",
    "Q4 2020": "The company has scheduled a Winter Business Update for institutional investors on Tuesday, February 2, 2021.",
}
NOTES = {
    "Q4 2017": ["a one-time tax expense of approximately $46 million decreased earnings per share by $0.03."],
    "Q3 2019": ["The pre-tax severance charges related to position eliminations, which reduced earnings per share by $.04, are included in Compensation and benefits expense."],
    "Q4 2019": ["These expenses reduced fourth quarter and full-year earnings per share by $.01, and are primarily included in professional services expense.",
                "Effective October 7, 2019, CS&Co eliminated online trading commissions for U.S. and Canadian-listed stocks and ETFs, as well as the base charge on options."],
    "Q1 2020": ["expenses totaling approximately $27 million, or $.02 per share, relating to certain actions taken in response to the COVID-19 pandemic."],
    "Q2 2021": ["Approximate impact of the $200 million regulatory matter charge, included in other expense, on results for the three months ended June 30, 2021 is as"],
}
NOTE_TXT = {
    "Q4 2017": "GAAP: FY17 $1.61 with the tax reform legislation's one-time tax expense in (no filing publishes an EPS without it)",
    "Q3 2019": "GAAP: the severance charges stay in (no filing publishes an EPS without them)",
    "Q4 2019": "GAAP: FY19 $2.67 with the severance charges and the acquisition-related expenses in; from Q4 2019 revenue trades fall as "
               "online trade commissions end (as published)",
    "Q1 2020": "GAAP: the COVID-19 expenses and the acquisition-related expenses stay in; from this release the activity table prints "
               "clients' daily average trades (DATs) only, not revenue trades, so the trades signal is not reported (n/r, BASE)",
    "Q2 2021": "GAAP: the $200 million regulatory matter charge stays in (its per-share effect, $.10, is stated, not an EPS without it)",
}
for q in ("Q2 2020", "Q3 2020", "Q4 2020", "Q1 2021", "Q2 2021", "Q3 2021"):
    NOTE_TXT[q] = ((NOTE_TXT[q] + "; ") if q in NOTE_TXT else "GAAP: ") + (
        "the release's adjusted diluted EPS also excludes the amortization of acquired intangible assets, a recurring item ('" + ADJ +
        "'), so GAAP stands")
for q in ("Q4 2020", "Q1 2021", "Q2 2021", "Q3 2021"):
    NOTE_TXT[q] += "; TD Ameritrade (acquired on October 6, 2020) in the figures as published, nothing made pro forma"
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
    has_rt = any(x.startswith("Revenue trades (") for x in L[h0:c0])
    if has_rt:
        rd, vd = row(fp, "Revenue trades (", h0, c0, n=5)
        dart, dart0 = vd[0], vd[4]
    else:                           # from Q1 2020 the releases print clients' daily average trades (DATs) only
        rd, vd = row(fp, "Clients’ Daily Average Trades (DATs) (in thousands) |", h0, c0, n=5)
        dart, dart0 = None, None
    reps, veps = sub_row(fp, "Earnings per common share", "Diluted |", h0, c0, n=5)
    rsh, vsh = sub_row(fp, "Weighted-average common shares outstanding:", "Diluted |", h0, c0, n=5)
    rc, vc = row(fp, "Total client assets |", c0, c0 + 45, n=5)
    rn, vn = row_any(fp, ["Total net new assets |", "Total net new client assets |"], c0, c0 + 70, n=5)
    eps_q, eps_q0 = veps[0], veps[4]
    if q in FQ:                     # the 10-Q reports the same quarter: revenue, expenses, pre-tax income, trades, client assets
        Fq = FQ[q]
        qcheck(Fq, ["Total net revenues |"], vr[0], vr[4])
        qcheck(Fq, ["Total expenses excluding interest |"], ve[0], ve[4])
        qcheck(Fq, ["Income before taxes on income |"], vp[0], vp[4])
        qcheck(Fq, ["Client assets (in billions, at quarter end) |", "Client assets (2) (in billions, at quarter end) |",
                    "Client assets (in billions, at quarter end) (2) |", "Client assets (in billions, at quarter end) (1) |",
                    "Total client assets |", "Total client assets (in billions, at quarter end) |"], vc[0], vc[4])
    raw = dict(revenue_m=vr[0], revenue_prior_m=vr[4], revenue_prev_q_m=vr[1], expense_m=ve[0], expense_prior_m=ve[4], pretax_m=vp[0],
               pretax_prior_m=vp[4], client_assets_b=vc[0], client_assets_prior_b=vc[4], dart_k=dart, dart_prior_k=dart0, nna_b=vn[0])

    def derive(rw):
        pm, pm0 = rw["pretax_m"] / rw["revenue_m"] * 100, rw["pretax_prior_m"] / rw["revenue_prior_m"] * 100
        return dict(sales_pct=r1(pct(rw["revenue_prior_m"], rw["revenue_m"])), seq_pct=r1(pct(rw["revenue_prev_q_m"], rw["revenue_m"])),
                    pretax_margin=r2(pm), pretax_margin_bp=r1((pm - pm0) * 100), expense_pct=r1(pct(rw["expense_prior_m"], rw["expense_m"])),
                    expense_gap_pp=r1(pct(rw["expense_prior_m"], rw["expense_m"]) - pct(rw["revenue_prior_m"], rw["revenue_m"])),
                    ca_pct=r1(pct(rw["client_assets_prior_b"], rw["client_assets_b"])),
                    dart_pct=None if rw["dart_k"] is None else r1(pct(rw["dart_prior_k"], rw["dart_k"])))
    d = derive(raw)
    pub, filed = SRC[S[q]]["published"], SRC[S[q]]["filed"]
    rel_date = dt.date.fromisoformat(pub)
    note = NOTE_TXT.get(q, "")
    for s_ in NOTES.get(q, []):
        quote(fp, s_)
    if NOTES.get(q):
        note += " (" + " ".join(f"'{s_}'" for s_ in NOTES[q]) + ")"
    if q in ("Q2 2020", "Q3 2020", "Q4 2020", "Q1 2021", "Q2 2021", "Q3 2021"):
        quote(fp, ADJ)
    if q in UNFILED:
        quote(fp, UNFILED[q])
        note = (note + "; " if note else "") + (f"an outlook given only at a business update or in commentary the company did not file is "
                                                f"unused (the CRM rule): '{UNFILED[q]}'")
    trades_txt = (f"daily average revenue trades {vd[0]:,.1f}K vs {vd[4]:,.1f}K" if has_rt else
                  f"daily average revenue trades not reported (clients' daily average trades, DATs, {vd[0]:,.1f}K vs {vd[4]:,.1f}K, display only)")
    p = dict(quarter=q, fy=fy, q=qn, published=pub, source=S[q], release=f"{rel_date:%b} {rel_date.day}",
             release_time=f"8-K {filed}; no filing states the release time", period_end=f"{fy}-{PE[qn]}", raw=raw,
             rows=dict(rev=rr, exp=re_, pre=rp, dart=rd, ca=rc, nna=rn, eps=reps, shares=rsh),
             sales_b=round(vr[0] / 1000, 3), ca_b=vc[0], dart_k=dart, nna_b=vn[0], **d, eps_q=eps_q, eps_q_prior=eps_q0,
             diluted_shares_m=vsh[0],
             sales_note=f"net revenues ${vr[0]:,.0f}M vs ${vr[4]:,.0f}M a year earlier, ${vr[1]:,.0f}M the quarter before",
             client_note=f"client assets ${vc[0]:,.1f}B vs ${vc[4]:,.1f}B a year earlier; net new client assets ${vn[0]:,.1f}B in the "
                         f"quarter; {trades_txt}",
             eps_note=f"diluted EPS ${eps_q:.2f} vs ${eps_q0:.2f}, GAAP (per common share, after preferred dividends)",
             shares_note=f"diluted shares {vsh[0]:,.0f}M; expenses excluding interest ${ve[0]:,.0f}M vs ${ve[4]:,.0f}M",
             next_print=f"Q{qn % 4 + 1} {fy + (1 if qn == 4 else 0)} print (the quarter ends in {Q_END[qn % 4 + 1]})", note=note)
    if not has_rt:
        p["dats_k"], p["dats_prior_k"] = vd[0], vd[4]
    if qn == 4:
        s0 = line_no(fp, "Consolidated Statements of Income")
        rfr, vfr = row(fp, "Total net revenues |", s0, h0)
        rfp, vfp = row(fp, "Income before taxes on income |", s0, h0)
        rft, vft = row_any(fp, ["Taxes on income |", "Taxes on income (1) |", "Taxes on income (2) |"], s0, h0)
        rfs, vfs = sub_row(fp, "Weighted-Average Common Shares Outstanding", "Diluted |", s0, h0, n=4)
        rfe, vfe = sub_row(fp, "Earnings Per Common Share", "Diluted |", s0, h0, n=4)
        rev_y, pre_y, tax_y, sh_y, eps_y = vfr[2], vfp[2], abs(vft[2]), vfs[2], vfe[2]
        want = {2017: 1.61, 2018: 2.45, 2019: 2.67, 2020: 2.12}[fy]
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
# the Q4 2017 print's year-ago figures are Q4 2016's as published in the Q4 2016 release (the series joins)
q16 = [p for p in old["prints"] if p["quarter"] == "Q4 2016"][0]["raw"]
assert (new_prints[0]["raw"]["revenue_prior_m"], new_prints[0]["raw"]["client_assets_prior_b"]) == (q16["revenue_m"], q16["client_assets_b"])


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
with open(A.checklist or os.path.join(SP, "checklist_schw_1821.json"), "w", encoding="utf-8") as fh:
    json.dump(CHECK, fh, ensure_ascii=False, indent=1)
print(len(SRC), "sources,", len(V), "vintages,", len(new_prints), "prints,", len(new_divs), "dividends;",
      sum(len(v) for v in CHECK.values()), "checklist strings")
for p in new_prints:
    print(p["quarter"], p["published"], p["sales_pct"], p["ca_pct"], p["expense_gap_pp"], p["dart_pct"], p["pretax_margin_bp"], p["eps_q"])
for v in V:
    print(v["published"], v["fy_label"], v["eps_normalized"], v["prev_fy_op_margin"], v["groups"], v["prev_fy_client_assets_b"], v["prev_fy_nna_b"])
for k, s in SRC.items():
    print(k, s["published"], s["filed"], s["title"][:60])
