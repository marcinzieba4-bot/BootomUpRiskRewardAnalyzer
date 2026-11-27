#!/usr/bin/env python3
"""Extend retro/facts/SCHW.json with 2022-2026 (filings accepted 2022-01-01 to 2026-11-20), asserting that every earlier fact is
unchanged. Same discipline as gen_schw.py, gen_schw_1013.py, gen_schw_1417.py and gen_schw_1821.py: each figure from its own row by label, every rate
computed, every quote asserted present in its own filing, a verbatim checklist written. Run:

    python3 retro/tools/edgar.py fetch 316709 <dir> --from 2022-01-01 --to 2026-11-20 --forms 8-K 8-K/A 10-Q 10-K
    python3 -I retro/generators/schw/gen_schw_2226.py --filings <dir> [--facts-in <2008-2021 sheet>] [--out retro/facts/SCHW.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_schw_2226.json

--facts-in is the 2008-2021 sheet gen_schw_1821.py writes (default: retro/facts/SCHW.json, which must then hold 2008-2021 only).
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
_ap.add_argument("--facts-in", help="the 2008-2021 fact sheet to extend (default retro/facts/SCHW.json)")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/SCHW.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_schw_2226.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402

ET = ZoneInfo("America/New_York")
CUT = "2026-11-20"
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
nid = [88]


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
# ── filings, in publication order ───────────────────────────────────────────────────────────────────────────────────────
REL = {"Q4 2021": "0000316709-22-000005", "Q1 2022": "0000316709-22-000014", "Q2 2022": "0000316709-22-000025",
       "Q3 2022": "0000316709-22-000032", "Q4 2022": "0000316709-23-000004", "Q1 2023": "0000316709-23-000022",
       "Q2 2023": "0000316709-23-000033", "Q3 2023": "0000316709-23-000047", "Q4 2023": "0000316709-24-000011",
       "Q1 2024": "0000316709-24-000041", "Q2 2024": "0000316709-24-000056", "Q3 2024": "0000316709-24-000066",
       "Q4 2024": "0000316709-25-000005", "Q1 2025": "0000316709-25-000019", "Q2 2025": "0000316709-25-000033",
       "Q3 2025": "0000316709-25-000046", "Q4 2025": "0000316709-26-000004", "Q1 2026": "0000316709-26-000016",
       "Q2 2026": "0000316709-26-000027", "Q3 2026": "0000316709-26-000035"}
TENQ = {"Q1 2022": "0000316709-22-000018", "Q2 2022": "0000316709-22-000028", "Q3 2022": "0000316709-22-000045",
        "Q1 2023": "0000316709-23-000026", "Q2 2023": "0000316709-23-000037", "Q3 2023": "0000316709-23-000062",
        "Q1 2024": "0000316709-24-000044", "Q2 2024": "0000316709-24-000060", "Q3 2024": "0000316709-24-000069",
        "Q1 2025": "0000316709-25-000023", "Q2 2025": "0000316709-25-000039", "Q3 2025": "0000316709-25-000051",
        "Q1 2026": "0000316709-26-000019", "Q2 2026": "0000316709-26-000031", "Q3 2026": "0000316709-26-000038"}
TENK = {"FY21": "0000316709-22-000009", "FY22": "0000316709-23-000009", "FY23": "0000316709-24-000018",
        "FY24": "0000316709-25-000010", "FY25": "0000316709-26-000009"}
FREL = {q: doc(a, "EX-99.1") for q, a in REL.items()}
FK = {k: doc(a, "10-K__") for k, a in TENK.items()}
FQ = {q: doc(a, "10-Q__") for q, a in TENQ.items()}
DIV_DECL = {"FY21": "January 26, 2022", "FY22": "January 26, 2023", "FY24": "January 29, 2025", "FY25": "January 29, 2026"}

S = {}
order = [("Q4 2021", "rel"), ("FY21", "10k"), ("Q1 2022", "rel"), ("Q2 2022", "rel"), ("Q2 2022 10-Q", "10q"), ("Q3 2022", "rel"),
         ("Q4 2022", "rel"), ("FY22", "10k"), ("Q1 2023", "rel"), ("Q2 2023", "rel"), ("Q3 2023", "rel"), ("Q4 2023", "rel"),
         ("FY23", "10k"), ("Q1 2024", "rel"), ("Q2 2024", "rel"), ("Q3 2024", "rel"), ("Q4 2024", "rel"), ("FY24", "10k"),
         ("Q1 2025", "rel"), ("Q2 2025", "rel"), ("Q3 2025", "rel"), ("Q4 2025", "rel"), ("FY25", "10k"),
         ("Q1 2026", "rel"), ("Q2 2026", "rel"), ("Q3 2026", "rel")]
for k, kind in order:
    if kind == "rel":
        S[k] = source(REL[k], f"Schwab {k} earnings release (8-K exhibit 99.1)", os.path.basename(FREL[k]).split("__")[1].replace(".rows.txt", ".htm"),
                      f"{k}" + (f" and FY{k[3:]}" if k.startswith("Q4") else "") + " statement of income, financial and operating "
                      "highlights, client assets and trades")
    elif kind == "10k":
        y = 2000 + int(k[2:])
        S[k] = source(TENK[k], f"The Charles Schwab Corporation FY{y} 10-K", os.path.basename(FK[k]).split("__")[1].replace(".rows.txt", ".htm"),
                      f"the MD&A overview's {y - 2}-{y} client metrics and financial information and the {y - 2}-{y} statements of "
                      f"income (Item 6 reserved): the FY{k[2:]} history vintage; Items 1, 1A and 5" +
                      (f"; the quarterly dividend rate declared on {DIV_DECL[k]}" if k in DIV_DECL else ""))
    else:
        S[k] = source(TENQ["Q2 2022"], "The Charles Schwab Corporation Q2 2022 10-Q", os.path.basename(FQ["Q2 2022"]).split("__")[1].replace(".rows.txt", ".htm"),
                      "the quarterly dividend rate declared on July 27, 2022")

# ── the listing stays the NYSE (no move in 2022-2026) ───────────────────────────────────────────────────────────────────
LIST10 = "CSC’s common stock is listed on The New York Stock Exchange under the ticker symbol SCHW."
for k in FK:
    quote(FK[k], LIST10)

# ── history vintages FY21-FY25: Item 6 is reserved, so each 10-K gives three years (the MD&A overview and the statements of
# income); earlier years keep the latest earlier vintage (the JPM 2022-2026 reading) ──────────────────────────────────────
DEV = "Developments in the business, economic, and geopolitical environment could negatively impact our business."
SEG = "Schwab provides financial services to individuals and institutional clients through two segments – Investor Services and Advisor Services."
CLOUD = "Cloud technologies are critical to the operation of our systems and platforms and our reliance on cloud technologies is growing."
AI_CYBER = ("Information security risks for financial institutions are increasing, in part because of the use of the internet and mobile "
            "and cloud technologies to conduct financial transactions, and the increased sophistication and activities, including the use "
            "of artificial intelligence technologies, of organized crime, activists, hackers and other external parties, including foreign "
            "state actors.")
AI_TREND = "Industry and competitive trends including artificial intelligence, digital assets, private company securities and other alternative investments;"
CRYPTO_OWN = ("In 2026, the Company anticipates it will begin offering expanded client access to trading in digital assets including spot "
              "trading in select cryptocurrencies.")
OLD_DUR = old["history_vintages"][-1]["why"].split(" 10-K); ", 1)[1]
prev_v = old["history_vintages"][-1]
V = []


def overview_bounds(path):
    i0 = line_no(path, "OVERVIEW")
    i1 = line_no(path, "Non-GAAP Financial Measures", after=i0)
    return i0, i1


def stmt_bounds(path):
    L = lines(path)
    i0 = [i for i, x in enumerate(L) if x == "Consolidated Statements of Income"][0]
    i1 = line_no(path, "Consolidated Statements of Comprehensive Income", after=i0)
    return i0, i1


NORM = {
    2021: ("the releases' adjusted diluted EPS also excludes the amortization of acquired intangible assets, which 'will continue in "
           "future periods over their remaining useful lives', a recurring item, so it is not a figure excluding only one-offs (the NKE "
           "FY2007, AVGO, PFE and V rule); no filing publishes an EPS without only the acquisition and integration-related costs"),
    2022: ("the releases' adjusted diluted EPS also excludes the recurring amortization of acquired intangible assets (the NKE FY2007, "
           "AVGO, PFE and V rule); no filing publishes an EPS without only the acquisition and integration-related costs"),
    2023: ("the releases' adjusted diluted EPS excludes the restructuring and acquisition and integration-related costs together with "
           "the recurring amortization of acquired intangible assets (the NKE FY2007, AVGO, PFE and V rule), and keeps the FDIC special "
           "assessment; no filing publishes an EPS without only the one-offs"),
    2024: ("the releases' adjusted diluted EPS excludes the restructuring and acquisition and integration-related costs together with "
           "the recurring amortization of acquired intangible assets (the NKE FY2007, AVGO, PFE and V rule); no filing publishes an EPS "
           "without only the one-offs"),
    2025: ("the releases' adjusted diluted EPS excludes only the recurring amortization of acquired intangible assets in 2025 (the NKE "
           "FY2007, AVGO, PFE and V rule)"),
}
AAPL = {}                     # filled from each Q4 release's reconciliation: the listed one-offs before tax against net income
for k in ("FY21", "FY22", "FY23", "FY24", "FY25"):
    fp, y = FK[k], 2000 + int(k[2:])
    years = [y, y - 1, y - 2]
    ob, sb = overview_bounds(fp), stmt_bounds(fp)
    re_, ve = row(fp, "Earnings per common share — diluted", *ob, n=3)
    rr_, vr = row(fp, "Total net revenues |", *ob, n=3)
    rs_, vs = sub_row(fp, "Weighted-Average Common Shares Outstanding", "Diluted |", *sb, n=3)
    rse, vse = sub_row(fp, "Earnings Per Common Share", "Diluted |", *sb, n=3)
    rst, vst = row(fp, "Total net revenues |", *sb, n=3)
    assert (ve, vr) == (vse, vst), (k, "overview vs statements of income")
    eps = {**prev_v["eps_normalized"], **{str(a): v for a, v in zip(years, ve)}}
    rev = {**prev_v["revenue_usd_b"], **{str(a): round(v / 1000, 3) for a, v in zip(years, vr)}}
    sh = {**prev_v["diluted_shares_m"], **{str(a): v for a, v in zip(years, vs)}}
    srcs = {**prev_v["eps_sources"], **{str(a): S[k] for a in years}}
    # every year a later 10-K reports equals the earlier vintage's figure (EPS, revenue, diluted shares): no restatement
    for a in years[1:]:
        assert (prev_v["eps_normalized"][str(a)], prev_v["revenue_usd_b"][str(a)], prev_v["diluted_shares_m"][str(a)]) == \
            (eps[str(a)], rev[str(a)], sh[str(a)]), (k, a)
    keep = sorted(eps)[-10:]                       # the ten fiscal years to the latest one
    eps, rev, sh, srcs = ({a: d[a] for a in keep} for d in (eps, rev, sh, srcs))
    L = lines(fp)
    comp = {}
    for lab in ("Asset management and administration fees", "Net interest revenue", "Trading revenue"):
        comp[lab] = row_any(fp, [lab + " |", lab + " (1) |", lab + " (2) |"], *sb, n=3)
    ri_, vi_ = row(fp, "Income before taxes on income |", *sb, n=3)
    rx_, vx_ = row_any(fp, ["Taxes on income |", "Taxes on income (1) |", "Taxes on income (2) |"], *sb, n=3)
    other = [vst[j] - sum(c[1][j] for c in comp.values()) for j in range(2)]
    oth_name = "Other (bank deposit account fees and other revenue)"
    groups = [[n, round(c[1][0] / 1000, 3), r1(pct(c[1][1], c[1][0]))] for n, c in comp.items()] + \
             [[oth_name, round(other[0] / 1000, 3), r1(pct(other[1], other[0]))]]
    pre, tax = vi_[0], abs(vx_[0])
    rca, vca = row(fp, "Client assets (in billions, at year end) |", *ob, n=3)
    rnn, vnn = row_any(fp, ["Net new client assets (in billions) (1) |", "Net new client assets (in billions) |"], *ob, n=3)
    item1 = quote(fp, re.search(r"engages, through its subsidiaries[^.]*\.", " ".join(L)).group(0))
    comp_s = quote(fp, re.search(r"Our industry is (?:highly competitive and )?characterized by aggressive price competition\.", " ".join(L)).group(0))
    for s_ in (DEV, SEG, CLOUD):
        quote(fp, s_)
    low = " ".join(L).lower()
    for w in ("offshore", "e-commerce", "ecommerce", "streaming", "electric vehicle", "decarbon", "glp-1", "obesity", "generative"):
        assert w not in low, (k, w)
    assert low.count("cyclical") == low.count("countercyclical"), (k, "cyclical")      # only the countercyclical capital buffer
    assert low.count("climate") == low.count("unprecedented climate"), (k, "climate")  # FY2021: 'amidst an unprecedented climate'
    crypto_w = [w for w in ("crypto", "digital asset", "bitcoin", "blockchain", "distributed ledger") if w in low]
    assert (crypto_w != []) == (y == 2025), (k, crypto_w)      # the FY2025 10-K is the first to name crypto or digital assets
    ai = low.count("artificial intelligence")
    assert (ai > 0) == (y >= 2023), (k, "artificial intelligence")
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
        fiscal_year="year ended December 31,", rows=[re_, rr_, rs_, rse, rst, ri_, rx_, rca, rnn] + [c[0] for c in comp.values()],
        normalization=None)
    # (SCHW 2022-2026) the 10-Ks name cloud technologies as a service Schwab's own systems rely on, not as a way its business is
    # delivered or displaced ('cloud_words' with 'cloud_reading'; the UNH 'cloud_words' reading)
    v["cloud_words"] = CLOUD
    v["cloud_reading"] = "names cloud technologies only as a service its own systems rely on"
    if y >= 2023:      # artificial intelligence, in the cyber risk factor (FY2023 on) and among competitive trends (FY2025): text only
        v["ai_words"] = [quote(fp, AI_CYBER)] + ([quote(fp, AI_TREND)] if y == 2025 else [])
    if y == 2025:      # CRYPTO: digital assets among competitive trends, and the Company's own planned crypto trading (the V encoding)
        v["crypto_quote"] = quote(fp, AI_TREND)
        v["crypto_own_quote"] = quote(fp, CRYPTO_OWN)
    V.append(v)
    prev_v = v

# ── dividends: the latest declared quarterly rate, each from the first filing that states it ─────────────────────────────
D22 = "In addition, on January 26, 2022, the Board of Directors of the Company declared a two cent, or 11%, increase in the quarterly cash dividend to $0.20 per common share."
D22b = "On July 27, 2022, the Board of Directors of CSC declared a two cent, or 10%, increase in the quarterly cash dividend to $.22 per common share."
D23 = "In addition, on January 26, 2023, the Board of Directors of the Company declared a three cent, or 14%, increase in the quarterly cash dividend to $.25 per common share."
D25 = "In addition, on January 29, 2025, the Board of Directors of the Company declared a two cent, or 8%, increase in the quarterly cash dividend to $.27 per common share."
D26 = "In addition, on January 29, 2026, the Board of Directors of the Company declared a five cent, or 19%, increase in the quarterly cash dividend to $.32 per common share."
quote(FK["FY21"], D22)
quote(FQ["Q2 2022"], D22b)
quote(FK["FY22"], D23)
quote(FK["FY24"], D25)
quote(FK["FY25"], D26)
assert "increase in the quarterly cash dividend" not in " ".join(lines(FK["FY23"])), "FY23: no new rate declared in January 2024"
for q in ("Q1 2024", "Q2 2024", "Q3 2024"):    # no new rate in 2024
    assert "increase in the quarterly cash dividend" not in " ".join(lines(FQ[q])), q
assert SRC[S["Q2 2022"]]["published"] < "2022-07-27" < SRC[S["Q2 2022 10-Q"]]["published"]
for q in REL:                                   # no release states a new rate before its filing
    t = " ".join(lines(FREL[q]))
    assert "increase in the quarterly cash dividend" not in t, q
new_divs = [dict(published=SRC[S["FY21"]]["published"], quarterly=0.20, source=S["FY21"], note=f"$0.20 a quarter: '{D22}' (FY2021 10-K)"),
            dict(published=SRC[S["Q2 2022 10-Q"]]["published"], quarterly=0.22, source=S["Q2 2022 10-Q"],
                 note=f"$0.22 a quarter: '{D22b}' (Q2 2022 10-Q)"),
            dict(published=SRC[S["FY22"]]["published"], quarterly=0.25, source=S["FY22"], note=f"$0.25 a quarter: '{D23}' (FY2022 10-K)"),
            dict(published=SRC[S["FY24"]]["published"], quarterly=0.27, source=S["FY24"], note=f"$0.27 a quarter: '{D25}' (FY2024 10-K)"),
            dict(published=SRC[S["FY25"]]["published"], quarterly=0.32, source=S["FY25"], note=f"$0.32 a quarter: '{D26}' (FY2025 10-K)")]

# ── prints Q4 2021 - Q3 2026 ─────────────────────────────────────────────────────────────────────────────────────────────
Q_END = {1: "March", 2: "June", 3: "September", 4: "December"}
PE = {1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"}
ADJ = "Amortization of acquired intangible assets will continue in future periods over their remaining useful lives."


def update_sentence(path):
    """The release's business-update sentence: the outlooks given there were never filed (the CRM rule)."""
    m = re.search(r"The company (?:has scheduled a|will host its) \w+ Business Update for institutional investors[^.]*\.",
                  " ".join(lines(path)))
    assert m, path
    return quote(path, m.group(0))


NOTES = {
    "Q2 2022": ["In addition, the company’s second quarter of 2021 included a charge of approximately $200 million, or $.10 per share, regarding a now settled regulatory matter."],
    "Q1 2023": ["bank deposit account revenue was down due in part to a $97 million one-time breakage fee relating to ending our arrangements with certain third-party banks ahead of the initial Ameritrade client transition group."],
    "Q3 2023": ["Beginning in the third quarter of 2023, these adjustments also include restructuring costs, which the Company began incurring in connection with its previously announced plans to streamline its operations to prepare for post-integration of TD Ameritrade."],
    "Q4 2023": ["Exclusive of these items, adjusted total expenses (1) increased by 6% to $11.0 billion, approximately 2% of which reflected the $172 million FDIC special assessment."],
    "Q1 2026": ["Closed Forge Global acquisition in early March"],
}
NOTE_TXT = {
    "Q2 2022": "the year-ago quarter keeps the regulatory matter charge, as published",
    "Q1 2023": "the one-time breakage fee stays in bank deposit account revenue (no filing publishes an EPS without it)",
    "Q3 2023": "the restructuring costs stay in (the adjusted EPS removes them with the recurring amortization)",
    "Q4 2023": "FY23 $2.54 with the restructuring costs, the acquisition and integration-related costs and the FDIC special assessment in "
               "(no filing publishes an EPS without only the one-offs)",
    "Q1 2026": "Forge Global (acquired on March 2, 2026, its 8-K) in the figures as published, nothing made pro forma",
}
for q in REL:
    NOTE_TXT[q] = "GAAP: " + ((NOTE_TXT[q] + "; ") if q in NOTE_TXT else "") + (
        "the release's adjusted diluted EPS also excludes the amortization of acquired intangible assets, a recurring item ('" + ADJ +
        "'), so GAAP stands")
CHARGES = {}                   # each Q4 release's full-year reconciliation: the listed items before tax
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
    assert not any(x.startswith("Revenue trades (") for x in L[h0:c0]), q       # still DATs only (from Q1 2020)
    rd, vd = row(fp, "Clients’ Daily Average Trades (DATs) (in thousands) |", h0, c0, n=5)
    reps, veps = sub_row(fp, "Earnings per common share", "Diluted |", h0, c0, n=5)
    rsh, vsh = sub_row(fp, "Weighted-average common shares outstanding:", "Diluted |", h0, c0, n=5)
    rc, vc = row(fp, "Total client assets |", c0, c0 + 45, n=5)
    rn, vn = row_any(fp, ["Total net new assets |", "Total net new client assets |"], c0, c0 + 70, n=5)
    eps_q, eps_q0 = veps[0], veps[4]
    if q in FQ:                     # the 10-Q reports the same quarter: revenue, expenses, pre-tax income, client assets
        Fq = FQ[q]
        qcheck(Fq, ["Total net revenues |"], vr[0], vr[4])
        qcheck(Fq, ["Total expenses excluding interest |"], ve[0], ve[4])
        qcheck(Fq, ["Income before taxes on income |"], vp[0], vp[4])
        qcheck(Fq, ["Client assets (in billions, at quarter end) |"], vc[0], vc[4])
    raw = dict(revenue_m=vr[0], revenue_prior_m=vr[4], revenue_prev_q_m=vr[1], expense_m=ve[0], expense_prior_m=ve[4], pretax_m=vp[0],
               pretax_prior_m=vp[4], client_assets_b=vc[0], client_assets_prior_b=vc[4], dart_k=None, dart_prior_k=None, nna_b=vn[0])
    pm, pm0 = raw["pretax_m"] / raw["revenue_m"] * 100, raw["pretax_prior_m"] / raw["revenue_prior_m"] * 100
    d = dict(sales_pct=r1(pct(raw["revenue_prior_m"], raw["revenue_m"])), seq_pct=r1(pct(raw["revenue_prev_q_m"], raw["revenue_m"])),
             pretax_margin=r2(pm), pretax_margin_bp=r1((pm - pm0) * 100), expense_pct=r1(pct(raw["expense_prior_m"], raw["expense_m"])),
             expense_gap_pp=r1(pct(raw["expense_prior_m"], raw["expense_m"]) - pct(raw["revenue_prior_m"], raw["revenue_m"])),
             ca_pct=r1(pct(raw["client_assets_prior_b"], raw["client_assets_b"])), dart_pct=None)
    pub, filed = SRC[S[q]]["published"], SRC[S[q]]["filed"]
    rel_date = dt.date.fromisoformat(pub)
    note = NOTE_TXT[q]
    for s_ in NOTES.get(q, []):
        quote(fp, s_)
    if NOTES.get(q):
        note += " (" + " ".join(f"'{s_}'" for s_ in NOTES[q]) + ")"
    quote(fp, ADJ)
    upd = update_sentence(fp)
    note += (f"; an outlook given only at a business update or in commentary the company did not file is unused (the CRM rule): '{upd}'")
    trades_txt = (f"daily average revenue trades not reported (clients' daily average trades, DATs, {vd[0]:,.1f}K vs {vd[4]:,.1f}K, "
                  "display only)")
    p = dict(quarter=q, fy=fy, q=qn, published=pub, source=S[q], release=f"{rel_date:%b} {rel_date.day}",
             release_time=f"8-K {filed}; the 8-K's acceptance governs (the AVGO Q3 FY11 rule)" + (
                 "; the release hosts its business update 'this morning', so it went out before its 8-K, which is the dated filing"
                 if "this morning" in upd else "; no filing states the release time"), period_end=f"{fy}-{PE[qn]}", raw=raw,
             rows=dict(rev=rr, exp=re_, pre=rp, dart=rd, ca=rc, nna=rn, eps=reps, shares=rsh),
             sales_b=round(vr[0] / 1000, 3), ca_b=vc[0], dart_k=None, nna_b=vn[0], **d, eps_q=eps_q, eps_q_prior=eps_q0,
             diluted_shares_m=vsh[0],
             sales_note=f"net revenues ${vr[0]:,.0f}M vs ${vr[4]:,.0f}M a year earlier, ${vr[1]:,.0f}M the quarter before",
             client_note=f"client assets ${vc[0]:,.1f}B vs ${vc[4]:,.1f}B a year earlier; net new client assets ${vn[0]:,.1f}B in the "
                         f"quarter; {trades_txt}",
             eps_note=f"diluted EPS ${eps_q:.2f} vs ${eps_q0:.2f}, GAAP (per common share, after preferred dividends)",
             shares_note=f"diluted shares {vsh[0]:,.0f}M; expenses excluding interest ${ve[0]:,.0f}M vs ${ve[4]:,.0f}M",
             next_print=f"Q{qn % 4 + 1} {fy + (1 if qn == 4 else 0)} print (the quarter ends in {Q_END[qn % 4 + 1]})", note=note,
             dats_k=vd[0], dats_prior_k=vd[4])
    if qn == 4:
        s0 = line_no(fp, "Consolidated Statements of Income")
        rfr, vfr = row(fp, "Total net revenues |", s0, h0)
        rfp, vfp = row(fp, "Income before taxes on income |", s0, h0)
        rft, vft = row_any(fp, ["Taxes on income |", "Taxes on income (1) |", "Taxes on income (2) |"], s0, h0)
        rfn, vfn = row(fp, "Net Income |", s0, h0)
        rfs, vfs = sub_row(fp, "Weighted-Average Common Shares Outstanding", "Diluted |", s0, h0, n=4)
        rfe, vfe = sub_row(fp, "Earnings Per Common Share", "Diluted |", s0, h0, n=4)
        rev_y, pre_y, tax_y, sh_y, eps_y = vfr[2], vfp[2], abs(vft[2]), vfs[2], vfe[2]
        # the listed items of the year, before tax (the reconciliation of pre-tax income): the AAPL FY2002 test's one-offs are the
        # acquisition and integration-related costs and the restructuring costs; the amortization recurs
        r0 = [i for i, x in enumerate(L) if x.startswith("Income before taxes on income (GAAP), Pre-tax profit margin (GAAP)")][0]
        items = {}
        for lab_ in ("Acquisition and integration-related costs", "Restructuring costs", "Amortization of acquired intangible assets"):
            hit = [x for x in L[r0 + 1:r0 + 5] if x.startswith(lab_ + " |")]
            if hit:
                CHECK.setdefault(fp, []).append(hit[0])
                items[lab_] = num(hit[0].split("|")[5])
        CHARGES[fy] = dict(items=items, net_income=vfn[2])
        m = r2(pre_y / rev_y * 100)
        lab = f"FY{fy % 100:02d}"
        p["fy_actual"] = dict(
            fy=fy, fy_label=lab, eps_normalized=eps_y, revenue_usd_b=round(rev_y / 1000, 3), diluted_shares_m=sh_y,
            normalization_note=f"{lab} ${eps_y:.2f}, diluted EPS, GAAP ({q} release)",
            op_margin=m, op_margin_note=f"{lab} income before taxes on income ${pre_y:,.0f}M / net revenues ${rev_y:,.0f}M ({q} release)",
            pretax_margin=m, pretax_margin_note=f"{lab} income before taxes on income ${pre_y:,.0f}M / net revenues ${rev_y:,.0f}M ({q} release)",
            sales_growth=r1(pct(vfr[3], vfr[2])), client_assets_b=vc[0], client_assets_growth=d["ca_pct"],
            tax_rate=round(tax_y / pre_y, 4), tax_note=f"{lab} taxes on income ${tax_y:,.0f}M on pre-tax ${pre_y:,.0f}M",
            rows=[rfr, rfp, rft, rfn, rfs, rfe])
    new_prints.append(p)

# ── the vintages' normalization: GAAP, no year meets the AAPL FY2002 test (from the Q4 releases' reconciliations) ──────────
for v in V:
    y = 2000 + int(v["fy_label"][2:])
    c = CHARGES[y]
    one = sum(x for k_, x in c["items"].items() if k_ != "Amortization of acquired intangible assets")
    assert one < c["net_income"] / 2, (y, "the AAPL FY2002 test")
    lst = " and ".join(f"${x:,.0f}M of {k_[0].lower() + k_[1:]}" for k_, x in c["items"].items()
                       if k_ != "Amortization of acquired intangible assets" and x)
    test = (f"FY{y}'s {lst} before tax against its ${c['net_income']:,.0f}M net income" if lst else
            f"FY{y} lists no one-off, only the recurring amortization")
    v["normalization"] = ("diluted EPS (no discontinued operation after 2008), each year from the latest filing that reports it, GAAP: no "
                          f"filing publishes an EPS without only the items the releases list ({NORM[y]}), and no year meets the AAPL "
                          f"FY2002 test ({test})")
    if y == 2023:
        v["normalization"] += "; the $172 million FDIC special assessment (Q4 2023) stays in, as in the company's adjusted figures"

# ── checks against the vintages: each Q4 print's full year equals the 10-K that follows it ───────────────────────────────
for p in new_prints:
    a = p.get("fy_actual")
    if a:
        v = [x for x in V if x["fy_label"] == a["fy_label"]]
        assert v, p["quarter"]
        y = str(a["fy"])
        assert (v[0]["eps_normalized"][y], v[0]["revenue_usd_b"][y], v[0]["diluted_shares_m"][y]) == \
            (a["eps_normalized"], a["revenue_usd_b"], a["diluted_shares_m"]), (p["quarter"], "Q4 vs 10-K")
# the Q4 2021 print's year-ago figures are Q4 2020's as published in the Q4 2020 release (the series joins)
q20 = [p for p in old["prints"] if p["quarter"] == "Q4 2020"][0]["raw"]
assert (new_prints[0]["raw"]["revenue_prior_m"], new_prints[0]["raw"]["client_assets_prior_b"]) == (q20["revenue_m"], q20["client_assets_b"])


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
with open(A.checklist or os.path.join(SP, "checklist_schw_2226.json"), "w", encoding="utf-8") as fh:
    json.dump(CHECK, fh, ensure_ascii=False, indent=1)
print(len(SRC), "sources,", len(V), "vintages,", len(new_prints), "prints,", len(new_divs), "dividends;",
      sum(len(v) for v in CHECK.values()), "checklist strings")
for p in new_prints:
    print(p["quarter"], p["published"], p["sales_pct"], p["ca_pct"], p["expense_gap_pp"], p["pretax_margin_bp"], p["eps_q"], p["diluted_shares_m"])
for v in V:
    print(v["published"], v["fy_label"], v["eps_normalized"], v["prev_fy_op_margin"], v["groups"], v["prev_fy_client_assets_b"], v["prev_fy_nna_b"])
    print("   ", v["normalization"][-200:])
for k, s in SRC.items():
    print(k, s["published"], s["filed"], s["title"][:60])
