#!/usr/bin/env python3
"""Extend retro/facts/SCHW.json with 2010-2013 (filings accepted 2010-01-01 to 2013-12-31), asserting that every earlier fact is
unchanged. Same discipline as gen_schw.py: each figure from its own row by label, every rate computed, every quote asserted present
in its own filing, a verbatim checklist written. Run:

    python3 -I retro/generators/schw/gen_schw_1013.py --filings <dir> [--facts-in <2008-2009 sheet>] [--out retro/facts/SCHW.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_schw_1013.json

--facts-in is the 2008-2009 sheet gen_schw.py writes (default: retro/facts/SCHW.json, which must then hold 2008-2009 only).
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
_ap.add_argument("--facts-in", help="the 2008-2009 fact sheet to extend (default retro/facts/SCHW.json)")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/SCHW.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_schw_1013.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402

ET = ZoneInfo("America/New_York")
CUT = "2013-12-31"
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
nid = [24]


def source(acc, title, fn, supports):
    p, filed = published(acc)
    sid = f"SCHW{nid[0]}"
    nid[0] += 1
    SRC[sid] = dict(published=p, filed=filed, title=title, url=URL(acc, fn), supports=supports)
    return sid


r1 = lambda x: round(x + 0.0, 1)
r2 = lambda x: round(x + 0.0, 2)
pct = lambda a, b: (b / a - 1) * 100

# ── filings, in publication order ───────────────────────────────────────────────────────────────────────────────────────
REL = {"Q4 2009": "0001193125-10-008163", "Q1 2010": "0001193125-10-084322", "Q2 2010": "0001193125-10-160170",
       "Q3 2010": "0001193125-10-230201", "Q4 2010": "0001193125-11-009126", "Q1 2011": "0001193125-11-099713",
       "Q2 2011": "0001193125-11-190197", "Q3 2011": "0001193125-11-272753", "Q4 2011": "0001193125-12-015306",
       "Q1 2012": "0001193125-12-164387", "Q2 2012": "0001193125-12-304623", "Q3 2012": "0001193125-12-423260",
       "Q4 2012": "0001193125-13-014486", "Q1 2013": "0001193125-13-154790", "Q2 2013": "0001193125-13-291696",
       "Q3 2013": "0001193125-13-399896"}
TENQ = {"Q1 2010": "0001193125-10-112442", "Q2 2010": "0001193125-10-178096", "Q3 2010": "0001193125-10-252000",
        "Q1 2011": "0001193125-11-130249", "Q2 2011": "0001193125-11-211971", "Q3 2011": "0001193125-11-299704",
        "Q1 2012": "0001193125-12-214602", "Q2 2012": "0001193125-12-337436", "Q3 2012": "0001193125-12-453877",
        "Q1 2013": "0001193125-13-203772", "Q2 2013": "0000316709-13-000013", "Q3 2013": "0000316709-13-000020"}
TENK = {"FY09": "0001193125-10-040444", "FY10": "0001193125-11-046932", "FY11": "0001193125-12-077926", "FY12": "0001193125-13-071646"}
K8_0420 = "0001181431-10-022140"
FREL = {q: doc(a, "EX-99.1") for q, a in REL.items()}
FK = {k: doc(a, "10-K__") for k, a in TENK.items()}
FQ = {q: doc(a, "10-Q__") for q, a in TENQ.items()}
F0420 = doc(K8_0420, "EX-99.1")

S = {}
order = [("Q4 2009", "rel"), ("FY09", "10k"), ("Q1 2010", "rel"), ("8K0420", "8k"), ("Q1 2010 10-Q", "10q"), ("Q2 2010", "rel"),
         ("Q3 2010", "rel"), ("Q4 2010", "rel"), ("FY10", "10k"), ("Q1 2011", "rel"), ("Q2 2011", "rel"), ("Q3 2011", "rel"),
         ("Q4 2011", "rel"), ("FY11", "10k"), ("Q1 2012", "rel"), ("Q2 2012", "rel"), ("Q3 2012", "rel"), ("Q4 2012", "rel"),
         ("FY12", "10k"), ("Q1 2013", "rel"), ("Q2 2013", "rel"), ("Q3 2013", "rel")]
for k, kind in order:
    if kind == "rel":
        S[k] = source(REL[k], f"Schwab {k} earnings release (8-K exhibit 99.1)", os.path.basename(FREL[k]).split("__")[1].replace(".rows.txt", ".htm"),
                      f"{k}" + (f" and FY{k[3:]}" if k.startswith("Q4") else "") + " statement of income, financial and operating "
                      "highlights, client assets and trades")
    elif kind == "10k":
        y = 2000 + int(k[2:])
        S[k] = source(TENK[k], f"The Charles Schwab Corporation FY{y} 10-K", os.path.basename(FK[k]).split("__")[1].replace(".rows.txt", ".htm"),
                      f"selected financial and operating data {y - 4}-{y}, the {y - 2}-{y} client activity metrics and statements of "
                      f"income: the FY{k[2:]} history vintage; Items 1, 1A and 5" + ("; the transfer of the listing to the NYSE" if y == 2009 else ""))
    elif kind == "8k":
        S[k] = source(K8_0420, "Schwab 8-K of 2010-04-20 (exhibit 99.1): the YieldPlus class action settlement and the added Q1 2010 reserve",
                      os.path.basename(F0420).split("__")[1].replace(".rows.txt", ".htm"),
                      "the $172 million pre-tax increase in the contingency reserve that reduces first quarter 2010 results")
    else:
        S[k] = source(TENQ["Q1 2010"], "The Charles Schwab Corporation Q1 2010 10-Q", os.path.basename(FQ["Q1 2010"]).split("__")[1].replace(".rows.txt", ".htm"),
                      "Q1 2010 statement of income as restated for the YieldPlus settlement reserve")

# ── the listing: Nasdaq to the NYSE, from the FY2009 10-K that states it, effective on its stated date (the PEP encoding) ──
LIST_Q = ("On February 22, 2010, CSC announced that it is transferring the listing of its common stock to the New York Stock Exchange "
          "(NYSE). CSC expects its common stock to begin trading on the NYSE on March 5, 2010, using its current symbol.")
quote(FK["FY09"], LIST_Q)
quote(FREL["Q1 2010"], "The Charles Schwab Corporation (NYSE: SCHW)")
listings = [dict(published=SRC[S["FY09"]]["published"], effective="2010-03-05", exchange="NYSE", source=S["FY09"],
                 note=f"'{LIST_Q}' (FY2009 10-K, Item 5); Nasdaq before the date it states")]
LIST10 = "CSC’s common stock is listed on The New York Stock Exchange under the ticker symbol SCHW."
for k in ("FY10", "FY11", "FY12"):
    quote(FK[k], LIST10)
quote(FK["FY09"], "CSC’s common stock is listed on The Nasdaq Stock Market under the ticker symbol SCHW.")

# ── history vintages FY09-FY12: the five-year selected data; earlier years from the latest earlier vintage ─────────────────
DEV = "Developments in the business, economic, and geopolitical environment could negatively impact the Company’s business."
COMP = "The Company’s industry is characterized by aggressive price competition."
SEG = "The Company provides financial services to individuals and institutional clients through two segments – Investor Services and Institutional Services."
OLD_DUR = old["history_vintages"][-1]["why"].split(" (FY2008 10-K); ")[1]
prev_v = old["history_vintages"][-1]
V = []


def sel_bounds(path):
    i0 = line_no(path, "Selected Financial and Operating Data")
    i1 = min(i for i, x in enumerate(lines(path)) if i > i0 and x.startswith("Item 7. |"))
    return i0, i1


def overview_bounds(path):
    i0 = sel_bounds(path)[1]
    i1 = min(i for i, x in enumerate(lines(path)) if i > i0 and x.startswith("• | Net new client assets"))
    return i0, i1


for k in ("FY09", "FY10", "FY11", "FY12"):
    fp, y = FK[k], 2000 + int(k[2:])
    years = list(range(y, y - 5, -1))
    b = sel_bounds(fp)
    re_, ve = row_any(fp, ["Income from continuing operations per share — diluted |",
                           "Income from continuing operations per common share — diluted |"], *b, n=5)
    rr_, vr = row(fp, "Net revenues |", *b, n=5)
    rs_, vs = row(fp, "Weighted-average common shares outstanding — diluted |", *b, n=5)
    eps = {**prev_v["eps_normalized"], **{str(a): v for a, v in zip(years, ve)}}
    rev = {**prev_v["revenue_usd_b"], **{str(a): round(v / 1000, 3) for a, v in zip(years, vr)}}
    sh = {**prev_v["diluted_shares_m"], **{str(a): v for a, v in zip(years, vs)}}
    srcs = {**prev_v["eps_sources"], **{str(a): S[k] for a in years}}
    # every year a later 10-K reports equals the earlier vintage's figure (EPS, revenue, diluted shares)
    for a in years[1:]:
        if str(a) in prev_v["eps_normalized"]:
            assert (prev_v["eps_normalized"][str(a)], prev_v["revenue_usd_b"][str(a)], prev_v["diluted_shares_m"][str(a)]) == \
                (eps[str(a)], rev[str(a)], sh[str(a)]), (k, a)
    keep = sorted(eps)[-10:]                       # the ten fiscal years to the latest one
    eps, rev, sh, srcs = ({a: d[a] for a in keep} for d in (eps, rev, sh, srcs))
    # the statement of income: components, pre-tax income and taxes (three years, most recent first)
    L = lines(fp)
    i0 = [i for i, x in enumerate(L) if x.startswith("Asset management and administration fees |") and len(x.split("|")) == 4][0]
    comp = {}
    for lab in ("Asset management and administration fees", "Net interest revenue", "Trading revenue"):
        r_, v_ = row(fp, lab + " |", i0, i0 + 8, n=3)
        comp[lab] = (r_, v_)
    rt_, vt_ = row(fp, "Total net revenues |", i0, i0 + 14, n=3)
    ri_, vi_ = row_any(fp, ["Income from continuing operations before taxes on income |", "Income before taxes on income |"], i0, i0 + 32, n=3)
    rx_, vx_ = row(fp, "Taxes on income |", i0, i0 + 34, n=3)
    assert vt_[0] == vr[0] and vt_[1] == vr[1], (k, "statement total vs selected data")
    other = [vt_[j] - sum(c[1][j] for c in comp.values()) for j in range(2)]
    groups = [[n, round(c[1][0] / 1000, 3), r1(pct(c[1][1], c[1][0]))] for n, c in comp.items()] + \
             [["Other (net of the provision for loan losses and impairment losses)", round(other[0] / 1000, 3), r1(pct(other[1], other[0]))]]
    pre, tax = vi_[0], abs(vx_[0])
    ob = overview_bounds(fp)
    rca, vca = row(fp, "Client assets (in billions, at year end) |", *ob, n=3)
    rnn, vnn = row_any(fp, ["Net new client assets (in billions)", "Net new client assets (1) (in billions)"], *ob, n=3)
    item1 = quote(fp, re.search(r"engages, through its subsidiaries[^.]*\.", " ".join(L)).group(0))
    for s_ in (DEV, COMP, SEG):
        quote(fp, s_)
    assert "cyclic" not in " ".join(L).lower() and "cloud" not in " ".join(L).lower() and "offshore" not in " ".join(L).lower(), k
    lab = f"FY{y % 100:02d}"
    why = f"'The Charles Schwab Corporation (CSC) ... {item1}' '{DEV}' '{COMP}' (FY{y} 10-K); {OLD_DUR}"
    m = r2(pre / vr[0] * 100)
    v = dict(
        published=SRC[S[k]]["published"], sources=list(dict.fromkeys([S[k]] + [srcs[a] for a in keep])), fy_label=lab, kind="DURABLE",
        why=why, eps_normalized=eps, eps_sources=srcs, eps_excluded={}, eps_first_excluded=prev_v["eps_first_excluded"],
        revenue_usd_b=rev, revenue_sources=srcs, diluted_shares_m=sh, shares_sources=srcs, margin_signal_name="Pre-tax margin change",
        prev_fy_op_margin=m, prev_fy_op_margin_note=f"{lab} income before taxes on income ${pre:,.0f}M / net revenues ${vr[0]:,.0f}M",
        prev_fy_pretax_margin=m, prev_fy_pretax_margin_note=f"{lab} income before taxes on income ${pre:,.0f}M / net revenues ${vr[0]:,.0f}M",
        prev_fy_sales_growth=r1(pct(vr[1], vr[0])), prev_fy_client_assets_b=vca[0], prev_fy_client_assets_growth=r1(pct(vca[1], vca[0])),
        prev_fy_nna_b=vnn[0], tax_rate=round(tax / pre, 4), tax_note=f"{lab} taxes on income ${tax:,.0f}M on pre-tax ${pre:,.0f}M",
        dividend_annual=None, dividend_note=None,
        business_line="securities brokerage, banking and related financial services: Investor Services and Institutional Services "
                      "(two segments)",
        groups=groups, groups_basis=f"{lab} net revenues by component (asset management and administration fees, net interest revenue, "
                                    f"trading revenue, other net of the provision for loan losses and net impairment losses on "
                                    f"securities; {lab} growth)",
        company="The Charles Schwab Corporation", exchange=("Nasdaq" if k == "FY09" else "NYSE"), pe_window_start="2003-01-01",
        fiscal_year="year ended December 31,", rows=[re_, rr_, rs_, rt_, ri_, rx_, rca, rnn] + [c[0] for c in comp.values()],
        normalization=("diluted EPS from continuing operations (no discontinued operation after 2008), each year from the latest filing "
                       "that reports it, GAAP: the releases' figures excluding charges are net income in dollars, never per share, so "
                       "no filing publishes an EPS without them; no year from FY2003 meets the AAPL FY2002 test (FY2010's $482M of "
                       "listed charges before tax, $321M after, the largest, against its $454M net income); FY02 is excluded"))
    V.append(v)
    prev_v = v

# ── prints Q4 2009 - Q3 2013 ─────────────────────────────────────────────────────────────────────────────────────────────
Q_END = {1: "March", 2: "June", 3: "September", 4: "December"}
PE = {1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"}
Q110 = ("If rates remain at current levels – and excluding any YieldPlus bond fund related effects, which remain uncertain – the "
        "company should achieve revenue growth at least in the low single digits, limit expense growth to about 4%, and deliver a "
        "pre-tax profit margin of at least 25%.")
Q313 = ("we expect our 2013 revenue growth will outpace expenses by approximately 100 to 200 basis points, helping us to achieve a "
        "pre-tax profit margin of at least 30% and earnings per share in the mid-$.70s for the year.")
Q313b = "Additionally, we are aiming for a gap of approximately 300 to 500 basis points between revenue and expense growth in 2014."
OUTLOOK = {
    "Q1 2010": dict(outlook_fy=2010, outlook_words=Q110,
                    outlook_reading="one-sided bounds ('at least') and a cost component (the UNH and SPGI bound rule)"),
    "Q3 2013": dict(outlook_fy=2013, outlook_words=Q313, eps_words="earnings per share in the mid-$.70s",
                    outlook_reading="'mid-$.70s' is words, not a range or a level (the SPGI 'high single-digit' rule), 'at least 30%' a "
                                    "one-sided bound and the revenue-expense gap a component"),
}
UNFILED = {"Q4 2009": "These results are consistent with the outlook expressed in the company’s press release dated December 14, 2009.",
           "Q1 2013": "These results are consistent with the outlook expressed in the company’s press release dated March 14, 2013."}
NOTES = {
    "Q4 2009": ["Money market fund fee waivers caused by declining rates rose to $110 million in the fourth quarter, bringing the "
                "full-year total to $224 million"],
    "Q1 2010": ["Our first quarter expenses include an $11 million pre-tax charge relating to pending litigation involving the Schwab "
                "YieldPlus ultra-short bond fund."],
    "Q3 2010": ["Schwab’s third quarter net income was $218 million prior to the inclusion of previously announced charges totaling "
                "$94 million after-tax."],
    "Q4 2010": ["The company’s 2010 net income prior to the inclusion of charges relating to YieldPlus and other previously disclosed "
                "matters totaled $775 million."],
    "Q3 2011": ["Third quarter 2011 results include non-recurring costs relating to the acquisition of optionsXpress Holdings, Inc. "
                "totaling $10 million after-tax."],
    "Q2 2012": ["The company’s financial results for both the second quarter and first half of 2012 include a pre-tax gain of $70 "
                "million, or approximately $44 million after-tax, relating to the previously disclosed resolution of a vendor dispute."],
    "Q3 2012": ["The company’s third quarter and year-to-date financial results include a non-recurring state tax benefit of "
                "approximately $20 million."],
    "Q3 2013": ["In third quarter of 2013, the Company reduced its reported totals for overall client assets and retirement plan "
                "participants by $24.7 billion and 317,000, respectively"],
}
NOTE_TXT = {
    "Q4 2009": "GAAP; the release's outlook reference is to a press release of December 14, 2009 that was not filed (unused, the CRM rule)",
    "Q1 2010": "GAAP as released; the YieldPlus settlement reserve added after the release restates the quarter (below)",
    "Q3 2010": "GAAP: the money market fund and credit card program charges stay in (the releases' figures excluding them are net "
               "income in dollars, not per share)",
    "Q4 2010": "GAAP: FY10 $0.38 with the YieldPlus, money market fund and credit card charges in ($321M after tax); the figure without "
               "them is net income in dollars, not per share",
    "Q3 2011": "optionsXpress (acquired 2011-09-01 for shares) is in the figures as published",
    "Q2 2012": "GAAP: the vendor-dispute gain stays in",
    "Q3 2012": "GAAP: the state tax benefit stays in",
    "Q3 2013": "client assets as published: the quarter's total is reduced by 4.7B for the retirement plan recordkeeping "
               "consolidation, the year-ago total is not (a seam in the client assets signal)",
    "Q1 2013": "GAAP; the release's outlook reference is to a press release of March 14, 2013 that was not filed (unused, the CRM rule)",
}
new_prints = []
qs = list(REL)
for q in qs:
    fp = FREL[q]
    qn, fy = int(q[1]), int(q[3:])
    L = lines(fp)
    h0 = line_no(fp, "Financial and Operating Highlights")
    c0 = [i for i, x in enumerate(L) if x.startswith("Growth in Client Assets and Accounts")][-1]
    rr, vr = row(fp, "Total net revenues |", h0, c0, n=5)
    re_, ve = row(fp, "Total expenses excluding interest |", h0, c0, n=5)
    rp, vp = row_any(fp, ["Income before taxes on income |", "Income from continuing operations before taxes on income |"], h0, c0, n=5)
    rd, vd = row(fp, "Revenue trades (", h0, c0, n=5)
    rsh, vsh = row_any(fp, ["Weighted-average common shares outstanding", "Weighted-average common sharesoutstanding"], h0, c0, n=5)
    reps, veps = row_any(fp, ["Diluted earnings per share from continuing operations |", "Diluted earnings per share |",
                              "Diluted earnings per common share |"], h0, c0, n=5)
    rc, vc = row(fp, "Total client assets |", c0, c0 + 45, n=5)
    rn, vn = row_any(fp, ["Total net new assets |", "Total net new client assets |"], c0, c0 + 70, n=5)
    assert not any("discontinued operations" in x.lower() and re.search(r"\| \(?\.\d", x) and not x.endswith("| —")
                   for x in L[h0:c0] if x.startswith("Income from discontinued") or x.startswith("Loss from discontinued")) or q == "Q4 2009", q
    eps_q, eps_q0 = veps[0], veps[4]
    if q in FQ:                     # the 10-Q reports the same quarter: revenue, expenses, pre-tax income, trades, client assets
        Lq = lines(FQ[q])

        def qrow(labs):
            for lab in labs:
                h = [x for x in Lq if x.startswith(lab)]
                if h:
                    return [num(t) for t in h[0].split("|")[1:3]]
            return None
        assert qrow(["Total net revenues |"]) == [vr[0], vr[4]], (q, "10-Q revenue")
        qx = qrow(["Total expenses excluding interest |"])
        qp = qrow(["Income before taxes on income |", "Income from continuing operations before taxes on income |"])
        if q == "Q1 2010":
            assert (qx, qp) == ([965.0, 756.0], [13.0, 355.0]), (qx, qp)          # the restated quarter (below)
        else:
            assert qx == [ve[0], ve[4]] and qp == [vp[0], vp[4]], (q, qx, qp, ve, vp)
        qd = qrow(["Daily average revenue trades (in thousands) (1) |", "Daily average revenue trades (1) (in thousands) |"])
        assert qd is None or qd == [vd[0], vd[4]], (q, "10-Q trades", qd)
        assert qrow(["Client assets (in billions, at quarter end) |", "Client assets (2) (in billions, at quarter end) |"]) ==             [vc[0], vc[4]], (q, "10-Q client assets")
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
    if NOTES.get(q):
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
             eps_note=f"diluted EPS ${eps_q:.2f} vs ${eps_q0:.2f}, GAAP" + (" (per common share, after preferred dividends)" if fy >= 2012 else ""),
             shares_note=f"diluted shares {vsh[0]:,.0f}M; expenses excluding interest ${ve[0]:,.0f}M vs ${ve[4]:,.0f}M",
             next_print=f"Q{qn % 4 + 1} {fy + (1 if qn == 4 else 0)} print (the quarter ends in {Q_END[qn % 4 + 1]})", note=note)
    if q in OUTLOOK:
        quote(fp, OUTLOOK[q]["outlook_words"])
        p.update(OUTLOOK[q])
        if q == "Q3 2013":
            quote(fp, Q313b)
    if q == "Q1 2010":
        # restated twice, each from its own filing (the JPM Q1 2012 encoding): the 8-K of 2010-04-20 adds the $172M pre-tax reserve
        # it states to the release's expenses and pre-tax income; the Q1 2010 10-Q of 2010-05-07 reports the quarter as finally booked
        R8 = ("Based on the preliminary settlement agreement, the company has increased the contingency reserve previously established in "
              "connection with the litigation by $172 million pre-tax, which is net of expected insurance coverage and will reduce "
              "first quarter 2010 net income by approximately $105 million, or $0.09 per share.")
        quote(F0420, R8)
        raw8 = {**raw, "expense_m": raw["expense_m"] + 172, "pretax_m": raw["pretax_m"] - 172}
        Q10 = ("For the quarter ended March 31, 2010, the Company has accrued a reserve of $196 million in connection with the lawsuit, "
               "reflecting the preliminary settlement of plaintiffs’ state and federal claims and expected insurance coverage")
        quote(FQ[q], Q10)
        Lq = lines(FQ[q])
        st = line_no(FQ[q], "Total expenses excluding interest |")          # the statement of income: its first rows
        rq_x, vq_x = row(FQ[q], "Total expenses excluding interest |", st, st + 1, n=2)
        rq_p, vq_p = row(FQ[q], "Income before taxes on income |", st, st + 3, n=2)
        rq_e, vq_e = row(FQ[q], "Earnings Per Share — Diluted |", st, st + 12, n=2)
        rawq = {**raw, "expense_m": vq_x[0], "pretax_m": vq_p[0]}
        assert vq_x[1] == raw["expense_prior_m"] and vq_p[1] == raw["pretax_prior_m"]
        p["restated"] = [
            dict(published=SRC[S["8K0420"]]["published"], source=S["8K0420"], raw=raw8, **derive(raw8), eps_q=round(eps_q - 0.09, 2),
                 eps_note=f"diluted EPS about ${eps_q - 0.09:.2f} vs ${eps_q0:.2f} (the release's ${eps_q:.2f} less the 8-K's "
                          "'approximately ... $0.09 per share'), GAAP",
                 shares_note=f"diluted shares {vsh[0]:,.0f}M; expenses excluding interest ${raw8['expense_m']:,.0f}M (the release's "
                             f"${raw['expense_m']:,.0f}M and the 8-K's $172M) vs ${ve[4]:,.0f}M",
                 note=f"restated by the 8-K of 2010-04-20 ('{R8}')", rows={"8k": R8}),
            dict(published=SRC[S["Q1 2010 10-Q"]]["published"], source=S["Q1 2010 10-Q"], raw=rawq, **derive(rawq), eps_q=vq_e[0],
                 eps_note=f"diluted EPS ${vq_e[0]:.2f} vs ${vq_e[1]:.2f}, GAAP (Q1 2010 10-Q)",
                 shares_note=f"diluted shares {vsh[0]:,.0f}M; expenses excluding interest ${rawq['expense_m']:,.0f}M vs ${ve[4]:,.0f}M "
                             "(Q1 2010 10-Q)",
                 note=f"restated by the Q1 2010 10-Q ('{Q10}')", rows={"exp": rq_x, "pre": rq_p, "eps": rq_e})]
    if qn == 4:
        s0 = line_no(fp, "Consolidated Statements of Income")
        rfr, vfr = row(fp, "Total net revenues |", s0, h0)
        rfp, vfp = row_any(fp, ["Income before taxes on income |", "Income from continuing operations before taxes on income |"], s0, h0)
        rft, vft = row(fp, "Taxes on income |", s0, h0)
        rfs, vfs = row_any(fp, ["Weighted-Average Common Shares Outstanding — Diluted |"], s0, h0, n=4)
        e0 = [i for i, x in enumerate(L[s0:h0]) if re.match(r"Earnings Per (Common )?Share [—–-] Diluted", x)]
        assert e0, q
        hd = L[s0 + e0[0]]
        if "|" in hd:               # a single row: quarter, year-ago quarter, year, year before
            rfe, vfe = hd, [num(t) for t in hd.split("|")[1:]]
            CHECK.setdefault(fp, []).append(hd)
        else:
            rfe, vfe = row(fp, "Income from continuing operations |", s0 + e0[0], s0 + e0[0] + 3)
        rev_y, pre_y, tax_y, sh_y, eps_y = vfr[2], vfp[2], abs(vft[2]), vfs[2], vfe[2]
        want = {2009: 0.68, 2010: 0.38, 2011: 0.70, 2012: 0.69}[fy]
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
        if v:
            y = str(a["fy"])
            assert (v[0]["eps_normalized"][y], v[0]["revenue_usd_b"][y], v[0]["diluted_shares_m"][y]) == \
                (a["eps_normalized"], a["revenue_usd_b"], a["diluted_shares_m"]), (p["quarter"], "Q4 vs 10-K")
# the 2013-06-24 segment recast of the FY2012 10-K changes no figure the history uses (adds nothing)
F0624 = doc("0001193125-13-268973", "EX-99.1")
assert row(F0624, "Net revenues | 4% | 4,883 |", n=3)[1] == [4883, 4691, 4248]
quote(doc("0001193125-13-268973", "8-K__"), "conforming certain of its historical segment information")

# ── assemble: the earlier facts unchanged ────────────────────────────────────────────────────────────────────────────────
for k in SRC:
    assert k not in f["sources"]
f["sources"].update(SRC)
f["history_vintages"] += V
f["prints"] += new_prints
f["listings"] = listings
f["_doc"] = old["_doc"]
for key in ("sources", "history_vintages", "prints"):
    n_old = len(old[key])
    got = list(f[key].items())[:n_old] if key == "sources" else f[key][:n_old]
    want = list(old[key].items()) if key == "sources" else old[key]
    assert got == want, key
for key in ("rule_t", "dividends", "guides", "events", "company_names", "splits", "fiscal_calendar", "price_basis", "ticker"):
    assert f[key] == old[key], key
assert [p["published"] for p in f["prints"]] == sorted(p["published"] for p in f["prints"])
with open(FACTS, "w", encoding="utf-8") as fh:
    json.dump(f, fh, ensure_ascii=False, indent=1)
with open(A.checklist or os.path.join(SP, "checklist_schw_1013.json"), "w", encoding="utf-8") as fh:
    json.dump(CHECK, fh, ensure_ascii=False, indent=1)
print(len(SRC), "sources,", len(V), "vintages,", len(new_prints), "prints;", sum(len(v) for v in CHECK.values()), "checklist strings")
for p in new_prints:
    print(p["quarter"], p["published"], p["sales_pct"], p["ca_pct"], p["expense_gap_pp"], p["dart_pct"], p["pretax_margin_bp"], p["eps_q"],
          [(r["published"], r["expense_gap_pp"], r["pretax_margin_bp"]) for r in p.get("restated", [])])
for v in V:
    print(v["published"], v["fy_label"], v["eps_normalized"], v["prev_fy_op_margin"], v["groups"], v["prev_fy_client_assets_b"], v["prev_fy_nna_b"])
for k, s in SRC.items():
    print(k, s["published"], s["filed"], s["title"][:60])
