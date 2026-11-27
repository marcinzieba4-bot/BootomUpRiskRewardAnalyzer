#!/usr/bin/env python3
"""Extend retro/facts/NEM.json with 2010-2013 (filings accepted 2010-01-01 to 2013-12-31), asserting that every earlier fact is
unchanged. Same discipline as gen_nem.py: each raw figure is read from its own row by label (the row text is kept in the fact), every
rate, margin and change is computed, every quote is asserted present in its own filing word for word, and a verbatim checklist is
written. Only filings accepted on or before 2013-12-31 are read. The downloads (keep them outside the repo, e.g. the scratchpad):

    python3 retro/tools/edgar.py index 1164727 <dir>
    python3 retro/tools/edgar.py fetch 1164727 <dir> --from 2009-12-01 --to 2013-12-31 --forms 8-K 8-K/A 10-K 10-K/A 10-Q

    python3 -I retro/generators/nem/gen_nem_1013.py --filings <dir> [--facts-in <2008-2009 sheet>] [--out retro/facts/NEM.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_nem_1013.json

--facts-in is the 2008-2009 sheet gen_nem.py writes (default: retro/facts/NEM.json, which must then hold 2008-2009 only).
"""
import argparse
import copy
import datetime as dt
import glob
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
_ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("--filings", required=True)
_ap.add_argument("--facts-in")
_ap.add_argument("--out")
_ap.add_argument("--checklist")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402

ET = ZoneInfo("America/New_York")
START, CUT = "2010-01-01", "2013-12-31"
CIK = 1164727
ROWS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("NEM")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
FACTS = A.out or os.path.join(REPO, "retro", "facts", "NEM.json")
old = json.load(open(A.facts_in or os.path.join(REPO, "retro", "facts", "NEM.json"), encoding="utf-8"))
assert all(s["published"] <= "2009-12-31" for s in old["sources"].values()), "--facts-in must be the 2008-2009 sheet"
f = copy.deepcopy(old)
CHECK = {}
TEXT = {}
norm = lambda s: re.sub(r"\s+", " ", s).strip()


def path(acc, pat):
    hits = glob.glob(os.path.join(SP, "*", acc, pat))
    assert len(hits) == 1, (acc, pat, hits)
    return hits[0]


def lines(p):
    if p not in TEXT:
        TEXT[p] = [norm(x) for x in open(p, encoding="utf-8", errors="replace").read().split("\n")]
    return TEXT[p]


def quote(p, s):
    assert norm(s) in norm(" ".join(lines(p))), (os.path.basename(p), s[:120])
    CHECK.setdefault(p, []).append(s)
    return s


def num(t):
    t = t.replace("$", "").replace(",", "").replace("%", "").strip()
    if t in ("—", "-", "–", ""):
        return 0.0
    neg = t.startswith("(") and t.endswith(")")
    return -float(t.strip("()")) if neg else float(t)


def isnum(t):
    try:
        num(t)
        return t.strip() not in ("",)
    except ValueError:
        return False


def find(p, pat, after=0, nth=0, before=None):
    """Index of the nth line at or after `after` (and before `before`) that matches the regex pat at its start."""
    L = lines(p)
    hits = [i for i in range(after, before if before is not None else len(L)) if re.match(pat, L[i])]
    assert len(hits) > nth, (os.path.basename(p), pat, after)
    return hits[nth]


def cells(p, i):
    """The numeric cells of line i (after its label), or of line i+1 when the label wraps onto it; and the row text."""
    L = lines(p)
    for j in (i, i + 1):
        c = [x.strip() for x in L[j].split("|")]
        v = [num(x) for x in c[1:] if isnum(x)]
        if v:
            return v, (L[i] + " " + L[j] if j > i else L[i])
    raise AssertionError((os.path.basename(p), L[i]))


def row(p, pat, after=0, nth=0, n=None, before=None):
    i = find(p, pat, after, nth, before)
    v, t = cells(p, i)
    assert n is None or len(v) == n, (os.path.basename(p), t, n)
    return v, t


def bare(p, i, n):
    """An unlabeled row of n figures (a total) at line i."""
    c = [x.strip() for x in lines(p)[i].split("|")]
    assert len(c) == n and all(isnum(x) for x in c), (os.path.basename(p), lines(p)[i])
    return [num(x) for x in c], lines(p)[i]


def pub(acc):
    """The acceptance-time rule (gen_nem.py's): ET; at or after 16:00, the next trading day."""
    r = ROWS[acc]
    t = dt.datetime.fromisoformat(r[1].replace("Z", "+00:00")).astimezone(ET)
    day = t.date().isoformat()
    if (t.hour, t.minute) >= (16, 0):
        day = min(d for d in TDAYS if d > day)
        when = f"accepted {t:%Y-%m-%d %H:%M} ET, after the close: counts from {day}"
    elif (t.hour, t.minute) < (9, 30):
        when = f"accepted {t:%Y-%m-%d %H:%M} ET, before the open"
    else:
        when = f"accepted {t:%Y-%m-%d %H:%M} ET, during the session"
    assert START <= day <= CUT, (acc, day)
    return day, when


SOURCES = f["sources"]
NEXT_ID = [28]


def src(acc, title, supports):
    sid = f"NM{NEXT_ID[0]}"
    NEXT_ID[0] += 1
    day, when = pub(acc)
    SOURCES[sid] = {"published": day, "filed": when, "title": title,
                    "url": f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc.replace('-', '')}/{acc}.txt", "supports": supports}
    return sid


pct = lambda a, b: round((b / a - 1) * 100 + 0.0, 2)
pct1 = lambda a, b: round((b / a - 1) * 100 + 0.0, 1)

# ── the 10-Ks: four history vintages (each year from the latest filing that reports it; earlier years from the latest earlier
# vintage, the established encoding) ──────────────────────────────────────────────────────────────────────────────────────────────
K = {2009: ("0000950123-10-016613", "10-K__d70495e10vk.rows.txt"), 2010: ("0000950123-11-017350", "10-K__d79003e10vk.rows.txt"),
     2011: ("0001193125-12-075918", "10-K__d263670d10k.rows.txt"), 2012: ("0001193125-13-070256", "10-K__d462654d10k.rows.txt")}
KP = {y: path(a, fn) for y, (a, fn) in K.items()}
KID = {}
for y, (a, _) in K.items():
    KID[y] = src(a, f"Newmont FY{y} 10-K", f"history vintage FY{y} (Item 6 selected data, the statements, the MD&A key results); "
                 "the 'why'" + ("; Q4 quarterly data (sales, diluted EPS from continuing operations, diluted shares)" if y >= 2010 else ""))
WHY2 = {2009: "Our business is dependent on the price of gold and copper, which are affected by numerous factors beyond our control.",
        2010: "Our business is dependent on the prices of gold and copper, which fluctuate on a daily basis and are affected by numerous "
              "factors beyond our control."}
WHY_RISK = "A substantial or extended decline in gold or copper prices would have a material adverse effect on Newmont."


def why(y):
    p = KP[y]
    assert "cyclical" not in " ".join(lines(p)).lower(), (y, "DURABLE needs the company not to call its business cyclical (the MU rule)")
    lead = [x for x in lines(p) if x.startswith("Newmont is one of the world’s largest gold producers")][0].split(". ")[0] + "."
    q = [quote(p, lead), quote(p, WHY2[min(y, 2010)]), quote(p, WHY_RISK)]
    return " ".join(f"'{x}'" for x in q) + (f" (the FY{y} 10-K's own words; it does not call the business cyclical, so DURABLE, the MU rule)")


def selected(y):
    """Item 6: revenues (sales), diluted EPS from continuing operations, five years (latest first)."""
    p = KP[y]
    i6 = find(p, r"^ITEM 6\. \| SELECTED FINANCIAL DATA \(dollars", 0)
    rev, rrow = row(p, r"^(Revenues|Sales) \|", i6, n=5)
    dl = find(p, r"^Diluted:$", i6)
    eps, erow = row(p, r"^Continuing operations \|", dl, n=5)
    div, drow = row(p, r"^Dividends declared per common share \|", i6, n=5)
    return rev, eps, div, [rrow, "Diluted: " + erow, drow]


EXCL07 = ("a loss with no figure excluding only its one-offs: $(2.18) a diluted share from continuing operations ({src}); the Q4 2007 "
          "release lists $1,544M of after-tax charges in continuing operations ('Write-down of Exploration goodwill' $1,122M, 'Loss on "
          "settlement of gold contracts' $358M, marketable securities $39M, the Batu Hijau minority loan $25M) against its $963M loss, "
          "but publishes no per-share figure without them; excluded as the latest year (the NKE FY2018 and XOM FY2020 rule), its own "
          "days leave the P/E window, and it stays a gap")
DIV_NOTE = "dividends declared per common share ${:.2f} in FY{} (Item 6); the quarterly rate in force is the latest one a filing states"
V = f["history_vintages"]
prev = V[-1]


def vintage(y, extra_excl=None, drop_before=None):
    global prev
    p = KP[y]
    rev, eps, div, rows = selected(y)
    years = [str(y - k) for k in range(5)]
    assert abs(eps[[i for i, yy in enumerate(years) if yy == "2007"][0]] + 2.18) < 1e-9 if "2007" in years else True
    e = {k: v for k, v in prev["eps_normalized"].items()}
    es = dict(prev["eps_sources"])
    r = dict(prev["revenue_usd_b"])
    rs = dict(prev["revenue_sources"])
    for yy, v_e, v_r in zip(years, eps, rev):
        r[yy], rs[yy] = v_r / 1000, KID[y]
        if yy == "2007":
            continue
        e[yy], es[yy] = v_e, KID[y]
    excl = {"2007": EXCL07.format(src=f"FY{min(y, 2011)} 10-K")}
    if extra_excl:
        excl.update(extra_excl)
        for k in extra_excl:
            e.pop(k, None)
            es.pop(k, None)
    # diluted weighted shares, the statement's three years
    ws = find(p, r"^Weighted average common shares \(millions\):", 0)
    sh, shrow = row(p, r"^Diluted \|", ws, n=3)
    s = dict(prev["diluted_shares_m"])
    ss = dict(prev["shares_sources"])
    for k, v in zip(years[:3], sh):
        s[k], ss[k] = v, KID[y]
    first_excl = dict(prev["eps_first_excluded"])
    window = prev["pe_window_start"]
    if drop_before:                            # the ten fiscal years to the latest one: earlier years leave the history
        for d in (e, es, r, rs, s, ss):
            for k in [k for k in d if int(k) < drop_before]:
                del d[k]
        first_excl, window = {}, None
    yrs = sorted(set(e) | set(excl))
    assert int(yrs[-1]) == y and len(range(int(yrs[0]), y + 1)) <= 10, (y, yrs)
    # the year's statement lines for the display fields
    i8 = [i for i in range(len(lines(p))) if re.match(r"^Income (\(loss\) )?(from continuing operations )?before income (and mining )?tax"
                                                    r"( expense)? and other items \| [\d,()]+ \| [\d,()]+ \| [\d,()]+$", lines(p)[i])]
    pt, ptrow = cells(p, i8[0])
    tx, txrow = row(p, r"^Income (and mining )?tax expense( \(Note \d+\))? \| \(", i8[0], n=3)
    cf, cfrow = row(p, r"^Net cash provided from continuing operations \|", 0, n=3)
    cx, cxrow = row(p, r"^Additions to property, plant and mine development \| \(", 0, n=3)
    ca, carow = row(p, r"^Cash and cash equivalents \|", 0, n=2)
    gs = find(p, r"^Consolidated gold sales:$", 0)
    gold, grow = row(p, r"^Net \|", gs, n=3)
    if y == 2009:
        oz, ozrow = row(p, r"^Consolidated gold ounces sold \(thousands\)\(2\) \|", 0, n=3)
    else:
        oz, ozrow = row(p, r"^Consolidated \|", find(p, r"^Gold ounces sold \(thousands\)$", 0), n=3)
    cs, csrow = row(p, r"^Gold \(per ounce\) \|", find(p, r"^Costs applicable to sales\(\d\)$", 0), n=3)
    lab = f"FY{y % 100:02d}"
    v = {**{k: prev[k] for k in ("company", "exchange", "business_line", "margin_signal_name", "kind")},
         "published": SOURCES[KID[y]]["published"], "sources": [KID[y]] + [x for x in dict.fromkeys(list(es.values()) + list(rs.values())
                                                                                                 + list(ss.values())) if x != KID[y]],
         "fy_label": lab, "eps_normalized": dict(sorted(e.items())), "eps_sources": dict(sorted(es.items())),
         "eps_excluded": dict(sorted(excl.items())), "eps_first_excluded": first_excl,
         "revenue_usd_b": dict(sorted(r.items())), "revenue_sources": dict(sorted(rs.items())),
         "diluted_shares_m": dict(sorted(s.items())), "shares_sources": dict(sorted(ss.items())),
         "pe_window_start": window, "rows": rows + [shrow, ptrow, txrow, cfrow, cxrow, carow, grow, ozrow, csrow],
         "prev_fy_margin": round(pt[0] / rev[0] * 100, 2),
         "prev_fy_margin_note": f"{lab} income before income tax and other items ${pt[0]:,.0f}M / sales ${rev[0]:,.0f}M (FY{y} 10-K)",
         "tax_rate": round(-tx[0] / pt[0], 4), "tax_note": f"{lab} income and mining tax expense ${-tx[0]:,.0f}M / pre-tax ${pt[0]:,.0f}M "
                                                           f"(FY{y} 10-K)",
         "prev_fy_sales_growth": pct1(rev[1], rev[0]), "prev_fy_oz_k": oz[0], "prev_fy_oz_pct": pct1(oz[1], oz[0]), "prev_fy_cas": cs[0],
         "prev_fy_cas_pct": pct1(cs[1], cs[0]), "franchise_source": f"FY{y} 10-K",
         "dividend_annual": div[0], "dividend_note": DIV_NOTE.format(div[0], y),
         "cash_b": ca[0] / 1000, "fcf_b": round((cf[0] + cx[0]) / 1000, 3), "fcf_label": lab,
         "fcf_note": f"net cash provided from continuing operations ${cf[0]:,.0f}M less additions to property, plant and mine development "
                     f"${-cx[0]:,.0f}M (FY{y} 10-K)",
         "cash_return_text": f"dividends declared ${div[0]:.2f} a share in FY{y}; no repurchase program in the FY{y} 10-K",
         "groups": [["Gold", gold[0] / 1000, pct1(gold[1], gold[0])],
                    ["Copper", round((rev[0] - gold[0]) / 1000, 3), pct1(rev[1] - gold[1], rev[0] - gold[0])]],
         "groups_basis": f"{lab} sales by metal, net (FY{y} 10-K; copper as sales less gold)", "why": why(y)}
    yrs_e = sorted(v["eps_normalized"])
    src_list = sorted({SOURCES[x]["title"] for x in v["eps_sources"].values()})
    v["normalization"] = (
        "GAAP diluted EPS from continuing operations before the cumulative effect of accounting changes, each year from the latest "
        f"filing that reports it ({yrs_e[0]}-{yrs_e[-1]}: {'; '.join(src_list)}; seams, as published); the releases' adjusted net income "
        "also removes items that recur in every period it tabulates (impairments and write-downs of assets, gains on asset sales, tax "
        "planning items), so GAAP stands (the PEP 2008 core rule)")
    V.append(v)
    prev = v
    return v


vintage(2009)
vintage(2010)
# FY2011: the Hope Bay write-down. The Q4 2011 release lists after-tax items in continuing operations against its $502M income from
# continuing operations attributable to Newmont: they exceed it (the AAPL FY2002 test), so reported EPS is under half the year's EPS
# without them; the release's adjusted net income also removes recurring items (other impairments and asset sales, tax planning),
# so no figure excludes only the one-offs, and the year is excluded as the latest year (the NKE FY2018 rule), then stays a gap.
R11 = path("0001144204-12-010697", "EX-99.1__*rows.txt")
rc = find(R11, r"^Net income attributable to Newmont stockholders is reconciled to Adjusted net income as follows:$", 0)
hb, hbrow = row(R11, r"^Impairment of Hope Bay assets \|", rc, n=4)
oi, oirow = row(R11, r"^Other impairments/asset sales \|", rc, n=4)
fa, farow = row(R11, r"^Fronteer acquisition costs \|", rc, n=4)
bc, bcrow = row(R11, r"^Boddington contingent consideration \|", rc, n=4)
tp, tprow = row(R11, r"^Income tax planning, net \|", rc, n=4)
cont11, controw = row(KP[2011], r"^Continuing operations \|", find(KP[2011], r"^Net income \(loss\) attributable to Newmont stockholders:$", 0), n=3)
items = hb[2] + oi[2] + fa[2] + bc[2] + tp[2]
assert items > cont11[0], (items, cont11[0])
quote(R11, "Income from continuing operations was impacted by $1.6 billion, or $3.24 per share, from the non-cash write-down of the "
      "Company's Hope Bay project in Canada.")
EXCL11 = (f"the AAPL FY2002 test: the Q4 2011 release's listed after-tax items in continuing operations (Hope Bay impairment ${hb[2]:,.0f}M, "
          f"other impairments and asset sales ${oi[2]:,.0f}M, Fronteer acquisition costs ${fa[2]:,.0f}M, Boddington contingent consideration "
          f"${bc[2]:,.0f}M, income tax planning ${tp[2]:,.0f}M; ${items:,.0f}M net) exceed the year's ${cont11[0]:,.0f}M of income from "
          "continuing operations attributable to Newmont, so reported EPS ($1.00 diluted, FY2011 10-K) is under half the year's EPS "
          "without them; the release's adjusted net income ($4.39 basic) also removes items that recur (other impairments and asset "
          "sales, tax planning: the PEP 2008 core rule), so no figure excludes only the one-offs; excluded as the latest year (the NKE "
          "FY2018 and XOM FY2020 rule), its own days leave the P/E window, and it stays a gap")
v11 = vintage(2011, extra_excl={"2011": EXCL11})
v11["rows"] += [hbrow, oirow, farow, bcrow, tprow, controw]
v12 = vintage(2012, extra_excl={"2011": EXCL11.replace("(FY2011 10-K)", "(FY2011 and FY2012 10-Ks)")}, drop_before=2003)

# ── the prints Q4 2009 - Q3 2013: the earnings releases (8-K exhibit 99.1), each figure against the year-ago quarter as the release
# shows it; diluted shares (display) from the 10-Q filed with the release, Q4 2010-Q4 2012 from the 10-K's quarterly data ──
PR = f["prints"]
NEXT = {1: "Q2 print (late July)", 2: "Q3 print (late October)", 3: "Q4 and full-year print with the 10-K (February)",
        4: "Q1 print (late April)"}
TENQ = {(2010, 1): "0000950123-10-038469", (2010, 2): "0000950123-10-068690", (2010, 3): "0000950123-10-098972",
        (2011, 1): "0000950123-11-037416", (2011, 2): "0000950123-11-069854", (2011, 3): "0000950123-11-092539",
        (2012, 1): "0001193125-12-186323", (2012, 2): "0001193125-12-317060", (2012, 3): "0001193125-12-446912",
        (2013, 1): "0001193125-13-183142", (2013, 2): "0001193125-13-303560", (2013, 3): "0001193125-13-421225"}
REL = {(2009, 4): ("0001144204-10-009810", "Feb 25"), (2010, 1): ("0001144204-10-022252", "Apr 27"),
       (2010, 2): ("0001144204-10-039660", "Jul 28"), (2010, 3): ("0001144204-10-056770", "Nov 2"),
       (2010, 4): ("0001144204-11-010573", "Feb 24"), (2011, 1): ("0001144204-11-023295", "Apr 21"),
       (2011, 2): ("0001144204-11-042706", "Jul 29"), (2011, 3): ("0001144204-11-059851", "Oct 27"),
       (2011, 4): ("0001144204-12-010697", "Feb 23"), (2012, 1): ("0001144204-12-024142", "Apr 26"),
       (2012, 2): ("0001144204-12-041246", "Jul 26"), (2012, 3): ("0001144204-12-059006", "Nov 1"),
       (2012, 4): ("0001144204-13-010569", "Feb 21"), (2013, 1): ("0001144204-13-024753", "Apr 29"),
       (2013, 2): ("0001157523-13-003605", "Jul 26"), (2013, 3): ("0001157523-13-005190", "Oct 31")}
RP = {k: path(a, "EX-99.1__*rows.txt") for k, (a, _) in REL.items()}
RID = {}


def ytd_pretax(p):
    """The release's pre-tax line (current quarter, year-ago quarter, then the year to date and its year-ago)."""
    L = lines(p)
    i = [j for j in range(len(L)) if re.match(r"^Income (\(loss\) )?(from continuing operations )?before income( and)?( mining)?( tax)?", L[j])
         and re.search(r"other items", L[j] + " " + L[j + 1])][0]
    return cells(p, i)


def print_q(fy, q):
    acc, release = REL[(fy, q)]
    p = RP[(fy, q)]
    quarter = f"Q{q} {fy}"
    sid = src(acc, f"Newmont {quarter} results (8-K exhibit 99.1)",
              f"{quarter}: sales, consolidated gold ounces {'sold' if (fy, q) == (2009, 4) else 'produced'}, costs applicable to sales "
              "per ounce, pre-tax income, diluted EPS from continuing operations, cash and debt" + ("; the dividend rate it states" if 0 else ""))
    RID[(fy, q)] = sid
    day, when = pub(acc)
    rows, extra = {}, []
    st = find(p, r"^(Statements of Consolidated Income|Condensed Statements of Consolidated Income|CONDENSED CONSOLIDATED STATEMENTS OF "
                 r"INCOME|STATEMENTS OF CONSOLIDATED INCOME|NEWMONT MINING CORPORATION)", 0)
    annual_only = (fy, q) in ((2011, 4), (2012, 4))
    if (fy, q) == (2009, 4):
        i = find(p, r"^Sales - copper, net \|", 0)
        rv, rows["rev"] = bare(p, i + 1, 4)
    elif not annual_only:
        rv, rows["rev"] = row(p, r"^Sales \|", st)
    # pre-tax income
    pv, rows["pt"] = ytd_pretax(p)
    # diluted EPS from continuing operations
    if (fy, q) == (2010, 1):
        ev, rows["eps"] = row(p, r"^Income per common share, basic and diluted \|", st, n=2)
    elif (fy, q) == (2011, 1):
        ev, rows["eps"] = row(p, r"^Diluted \|", find(p, r"^Income per common share$", st), n=2)
    elif not annual_only:
        dl = find(p, r"^Diluted:$", st)
        ev, t = row(p, r"^Continuing operations \|", dl)
        rows["eps"] = "Diluted: " + t
    cav, rows["cash"] = row(p, r"^Cash and cash equivalents \|", st, n=2)
    li = find(p, r"^LIABILITIES$", st)
    curv, rows["cur"] = row(p, r"^(Current portion of debt|Debt) \|", li, n=2)
    ltdv, rows["ltd"] = row(p, r"^Debt \|", find(p, r"^(Current portion of debt|Debt) \|", li) + 1, n=2)
    # ounces: consolidated gold ounces sold (Q4 2009), then produced (the releases' company-wide line with a year-ago figure)
    hdr = r"^Consolidated ounces sold \(thousands\):$" if (fy, q) == (2009, 4) else r"^Consolidated (gold )?ounces produced \(thousands\):$"
    h = find(p, hdr, 0)
    cu = find(p, r"^(Copper|Consolidated copper pounds produced \(millions\):)$", h)
    ncol = 4 if q in (2, 3, 4) else 2
    ozv, rows["oz"] = bare(p, cu - 1, ncol)
    cs = find(p, r"^(Gold )?Costs Applicable to Sales \(\$/ounce\)", 0)
    casv, rows["cas"] = row(p, r"^Average \|", cs)
    # diluted shares (display)
    if (fy, q) == (2009, 4):
        shv, rows["sh"] = row(p, r"^Diluted weighted-average common shares outstanding \|", st, n=4)
        sh_src = sid
    elif q in (1, 2, 3):
        qp = path(TENQ[(fy, q)], "10-Q__*.rows.txt")
        shv, t = row(qp, r"^Diluted \|", find(qp, r"(?i)^Weighted average common shares( \(millions\))?:", 0))
        rows["sh"] = "Weighted average common shares (millions): " + t
        sh_src = f"the Q{q} {fy} 10-Q (filed the same day)"
        assert pub(TENQ[(fy, q)])[0] == day, (quarter, "the 10-Q is public the same day as the release")
        CHECK.setdefault(qp, [])
    # Q4 2010-Q4 2012: the 10-K's quarterly data (the 10-K is public the same day as the release)
    if q == 4 and fy >= 2010:
        kp = KP[fy]
        assert SOURCES[KID[fy]]["published"] == day, (quarter, "the 10-K is public the same day as the release")
        qd = [i for i, x in enumerate(lines(kp)) if x == "Quarterly Data"][-1]
        t_cur = find(kp, rf"^{fy}$", qd)
        t_pri = find(kp, rf"^{fy - 1}$", t_cur + 1)
        s1, r1 = row(kp, r"^Sales \|", t_cur, n=4)
        s0, r0 = row(kp, r"^Sales \|", t_pri, n=4)
        e1, er1 = row(kp, r"^Continuing operations \|", find(kp, r"^Diluted:$", t_cur), n=4)
        e0, er0 = row(kp, r"^Continuing operations \|", find(kp, r"^Diluted:$", t_pri), n=4)
        d1, dr1 = row(kp, r"^Diluted \|", find(kp, r"^Weighted average common shares \(millions\)$", t_cur), n=4)
        shv, rows["sh"] = [d1[3]], f"FY{fy} 10-K quarterly data, {fy}: Weighted average common shares (millions) {dr1}"
        sh_src = f"the FY{fy} 10-K's quarterly data (filed the same day)"
        if annual_only:
            rv = [s1[3], s0[3]]
            rows["rev"] = f"FY{fy} 10-K quarterly data, {fy}: {r1}; {fy - 1}: {r0}"
            ev = [e1[3], e0[3]]
            rows["eps"] = f"FY{fy} 10-K quarterly data, Diluted: {fy}: {er1}; {fy - 1}: {er0}"
            # pre-tax: the year (this release) less the nine months (the Q3 release), both years (the F and UNH rule)
            p3 = RP[(fy, 3)]
            nine, nrow = ytd_pretax(p3)
            assert len(pv) == 3 and len(nine) == 4, (quarter, pv, nine)
            rows["pt"] = f"year: {rows['pt']}; nine months (Q3 {fy} release): {nrow}"
            pv = [pv[0] - nine[2], pv[1] - nine[3]]
            # the release's own full year, against the 10-K's quarters
            fyv, fyrow = row(p, r"^Sales \|", st, n=3)
            assert abs(sum(s1) - fyv[0]) < 1.5 and abs(sum(s0) - fyv[1]) < 1.5, (quarter, s1, s0, fyv)
        else:
            assert (s1[3], e1[3]) == (rv[0], ev[0]) and (s0[3], e0[3]) == (rv[1], ev[1]), (quarter, "the 10-K's Q4 equals the release's")
        CHECK.setdefault(kp, [])
    rev, rev0, pt, pt0 = rv[0], rv[1], pv[0], pv[1]
    oz, oz0, cas, cas0, e, e0 = ozv[0], ozv[1], casv[0], casv[1], ev[0], ev[1]
    m, m0 = pt / rev * 100, pt0 / rev0 * 100
    g = lambda a, b: round((b / a - 1) * 100 + 0.0, 1) if a > 0 else round((b - a) / abs(a) * 100 + 0.0, 1)
    basis = "sold" if (fy, q) == (2009, 4) else "produced"
    d = {"quarter": quarter, "fy": fy, "q": q, "published": day, "release": release, "release_time": when, "source": sid,
         "raw": {"rev_m": rev, "rev_prior_m": rev0, "pretax_m": pt, "pretax_prior_m": pt0, "oz_k": oz, "oz_prior_k": oz0,
                 "cas": cas, "cas_prior": cas0},
         "rows": rows, "sales_b": round(rev / 1000, 3), "sales_pct": pct1(rev0, rev), "oz_pct": pct1(oz0, oz), "oz_basis": basis,
         "cas_pct": pct1(cas0, cas), "pretax_margin": round(m + 0.0, 2), "pretax_margin_prior": round(m0 + 0.0, 2),
         "margin_bp": round((m - m0) * 100 + 0.0, 1), "eps_q": e, "eps_q_prior": e0, "eps_pct": g(e0, e),
         "diluted_shares_m": shv[0], "shares_source": sh_src, "cash_b": round(cav[0] / 1000, 3),
         "debt_note": f"debt ${ltdv[0] + curv[0]:,.0f}M (long-term ${ltdv[0]:,.0f}M and current ${curv[0]:,.0f}M)",
         "rev_note": f"sales ${rev:,.0f}M vs ${rev0:,.0f}M a year earlier" + (" (the 10-K's quarterly data)" if annual_only else ""),
         "oz_note": f"consolidated gold ounces {basis} {oz:,.0f}K vs {oz0:,.0f}K",
         "cas_note": f"costs applicable to sales ${cas:,.0f} an ounce of gold vs ${cas0:,.0f}",
         "adj_note": None, "next_print": NEXT[q]}
    if q == 4 and fy >= 2010:
        d["source_10k"] = KID[fy]
    if annual_only:
        d["derived_note"] = ("the release's statements give the year only: sales and diluted EPS from continuing operations are the "
                             f"FY{fy} 10-K's fourth-quarter data (public the same day), pre-tax income the release's year less the Q3 "
                             f"{fy} release's nine months, both years (the F and UNH rule)")
    fmt = lambda x: f"${x:.2f}" if x >= 0 else f"$({-x:.2f})"
    d["eps_note"] = f"GAAP diluted EPS from continuing operations {fmt(e)} vs {fmt(e0)}" + (
        "; growth over the year-ago loss's absolute value (the CAT rule)" if e0 < 0 else "")
    tx = norm(" ".join(lines(p)))
    mm = re.search(r"[Aa]djusted net income[^.;]{0,140}?\(?\$\d+\.\d\d per (basic |diluted )?share\)?", tx)
    if mm:
        d["adj_note"] = quote(p, mm.group(0))
    d["source_title"] = SOURCES[sid]["title"]
    PR.append(d)
    return p


for k in REL:
    print_q(*k)

# each Q4 print's full year equals the 10-K that comes with it (the vintage reports its year)
for fy in (2009, 2010, 2011, 2012):
    p = RP[(fy, 4)]
    st = find(p, r"^(Statements of Consolidated Income|STATEMENTS OF CONSOLIDATED INCOME)", 0)
    if fy in (2011, 2012):
        sv, _ = row(p, r"^Sales \|", st, n=3)
        dv, _ = row(p, r"^Continuing operations \|", find(p, r"^Diluted:$", st), n=3)
        fy_rev, fy_eps = sv[0], dv[0]
    elif fy == 2009:
        fy_rev = bare(p, find(p, r"^Sales - copper, net \|", 0) + 1, 4)[0][2]
        fy_eps = row(p, r"^Continuing operations \|", find(p, r"^Diluted:$", st), n=4)[0][2]
    else:
        fy_rev = row(p, r"^Sales \|", st, n=4)[0][2]
        fy_eps = row(p, r"^Continuing operations \|", find(p, r"^Diluted:$", st), n=4)[0][2]
    vv = [v for v in V if v["fy_label"] == f"FY{fy % 100:02d}"][0]
    assert abs(vv["revenue_usd_b"][str(fy)] * 1000 - fy_rev) < 0.5, (fy, fy_rev)
    assert fy_eps == selected(fy)[1][0], (fy, fy_eps)

# ── dividends: each rate from the first filing that states it as declared or approved (not "subject to Board approval") ──
DV = [((2010, 2), 0.15, "In addition, Newmont announced that its Board of Directors approved an increase in the Company's regular "
       "quarterly dividend from $0.10 per share of common stock to $0.15 per share of common stock, payable on September 29, 2010 to "
       "holders of record at the close of business on September 8, 2010."),
      ((2011, 1), 0.20, "the Board has approved a second quarter 2011 gold price-linked dividend of $0.20 per share"),
      ((2011, 2), 0.30, "Newmont's Board of Directors approved a third quarter 2011 gold price-linked dividend of $0.30 per share"),
      ((2011, 3), 0.35, "Newmont's Board of Directors approved a fourth quarter 2011 gold price-linked dividend of $0.35 per share"),
      ((2011, 4), 0.35, "Approved Q1 2012 dividend payable of $0.35 per share;"),
      ((2012, 1), 0.35, "Newmont's Board of Directors approved a second quarter 2012 gold price-linked dividend of $0.35 per share"),
      ((2012, 2), 0.35, "Newmont's Board of Directors approved a third quarter gold price-linked dividend payable of $0.35 per share"),
      ((2012, 3), 0.35, "Newmont's Board of Directors approved a fourth quarter gold price-linked dividend payable of $0.35 per share"),
      ((2012, 4), 0.425, "Approved Q1 2013 dividend payable of $0.425 per share;"),
      ((2013, 1), 0.35, "Newmont's Board of Directors approved a second quarter gold price-linked dividend in accordance with the "
                        "Company's gold price-linked dividend policy of $0.35 per share"),
      ((2013, 2), 0.25, "Newmont’s Board of Directors approved a third quarter gold price-linked dividend of $0.25 per share"),
      ((2013, 3), 0.20, "Newmont’s Board of Directors approved a fourth quarter dividend in accordance with the Company’s gold "
                        "price-linked dividend policy of $0.20 per share")]
f["dividends"] = [{"published": SOURCES[RID[k]]["published"], "quarterly": q_, "source": RID[k],
                   "note": f"${q_:.3f}".rstrip("0").rstrip(".") + f" a quarter (${q_ * 4:.2f} a year): '{quote(RP[k], s)}' ({k[1] if 0 else ''}"
                           f"Q{k[1]} {k[0]} release)"} for k, q_, s in DV]
for d in f["dividends"]:
    d["note"] = d["note"].replace("(Q", "(the Q")
# the 8-K of 2011-04-07 (the gold price-linked dividend policy) states a policy, not a declared rate: text only
POL = path("0000950123-11-033503", "EX-99.3__*.rows.txt")
quote(POL, "Subject to Board approval, the first quarterly dividend under this policy is expected to be payable on June 29, 2011 to "
      "shareholders of record on June 16, 2011.")

# ── outlooks (display only: equity or attributable gold production and costs applicable to sales per ounce; method r2 has no
# volume input and none for cost components, the XOM production and MSFT segment rules) ──
UNUSED = ("a production and unit-cost outlook: method r2 has no input for a production guide (the XOM rule) or for cost components "
          "(the MSFT segment rule), so no field; no filing guides revenue, EPS or a margin")
G = f["guides"]


def guide(fy, key_or_acc, doc, s, pat="EX-99.1__*rows.txt"):
    if isinstance(key_or_acc, tuple):
        sid, p = RID[key_or_acc], RP[key_or_acc]
    else:
        p = path(key_or_acc, pat)
        sid = src(key_or_acc, doc, "a display-only outlook (guide line)")
    G.append({"fy": fy, "published": SOURCES[sid]["published"], "source": sid, "doc": doc, "display": quote(p, s), "unused": UNUSED})


guide(2010, (2009, 4), "Q4 2009 release", "Equity gold production is expected to increase slightly to between 5.3 and 5.5 million ounces, "
      "primarily as a result of the continuing 12-month ramp-up to full production of Boddington, partially offset by lower production "
      "from Nevada and Yanacocha, as described below.")
guide(2010, (2010, 1), "Q1 2010 release", "The Company is maintaining its previously announced 2010 outlook for equity gold production of "
      "5.3 to 5.5 million ounces and costs applicable to sales of between $450 and $480 per ounce on a co-product basis")
guide(2010, (2010, 2), "Q2 2010 release", "we are maintaining our previously announced 2010 outlook for equity gold production of 5.3 to "
      "5.5 million ounces at a slightly narrower range of costs applicable to sales of between $460 and $480 per ounce on a co-product basis.")
guide(2010, (2010, 3), "Q3 2010 release", "With three quarters of production completed, the Company is narrowing its previously announced "
      "2010 outlook for equity gold production from 5.3 to 5.5 million ounces to 5.3 to 5.4 million ounces.")
guide(2011, (2010, 4), "Q4 2010 release", "2011 attributable gold production is expected to be approximately 5.1 million to 5.3 million "
      "ounces, with attributable copper production of 190 to 220 million pounds.")
guide(2011, (2011, 1), "Q1 2011 release", "The Company is maintaining its previously announced 2011 Outlook for attributable gold production "
      "of 5.1 to 5.3 million ounces with costs applicable to sales of $560 to $590 per ounce on a co-product basis")
guide(2011, (2011, 2), "Q2 2011 release", "The Company is maintaining its previously announced 2011 outlook for attributable gold production "
      "of 5.1 to 5.3 million ounces at CAS of between $560 and $590 per ounce (on a co-product basis)")
guide(2011, (2011, 3), "Q3 2011 release", "Newmont is maintaining its previously announced 2011 Outlook for attributable gold production of "
      "5.1 to 5.3 million ounces at CAS of between $560 and $590 per ounce (on a co-product basis).")
guide(2012, "0001193125-12-013134", "8-K of 2012-01-17 (preliminary 2011 operating highlights, 2012 outlook)", "The Company announced that "
      "it anticipates 2012 attributable gold and copper production of approximately 5.0 to 5.2 million ounces and 150 to 170 million "
      "pounds, respectively, at CAS of approximately $625 to $675 per ounce and $1.80 to $2.20 per pound, respectively.")
guide(2012, (2011, 4), "Q4 2011 release", "2012 attributable gold production is expected to be approximately 5.0 million to 5.2 million "
      "ounces, with attributable copper production of 150 to 170 million pounds.")
guide(2012, (2012, 1), "Q1 2012 release", "Newmont is maintaining its previously announced 2012 outlook for attributable gold and copper "
      "production of 5.0 to 5.2 million ounces and 150 to 170 million pounds at CAS of between $625 and $675 per ounce (on a co-product "
      "basis) and $1.80 and $2.20 per pound, respectively.")
guide(2012, (2012, 2), "Q2 2012 release", "Newmont is narrowing its previously announced 2012 outlook for attributable gold production to "
      "5.0 to 5.1 million ounces (from 5.0 to 5.2 million ounces), and narrowing its outlook on attributable copper production to 145 to "
      "165 million pounds (from 150 to 170 million pounds).")
guide(2012, (2012, 3), "Q3 2012 release", "Newmont now expects to be at the low end of its previously announced 2012 outlook for attributable "
      "gold and copper production of 5.0 to 5.1 million ounces and 145 to 165 million pounds, and at the high end of its narrower CAS "
      "outlook range of between $650 and $675 per ounce (on a co-product basis)")
guide(2013, "0001144204-13-003476", "8-K of 2013-01-22 (preliminary 2012 operating highlights, 2013 outlook)", "Attributable 2013 gold and "
      "copper production are expected to be approximately 4.8 to 5.1 million ounces and 150 to 170 million pounds, respectively, at costs "
      "applicable to sales of approximately $675 to $750 per ounce and $2.25 to $2.50 per pound, respectively.")
guide(2013, (2012, 4), "Q4 2012 release", "2013 attributable gold production is expected to be approximately 4.8 million to 5.1 million "
      "ounces, with attributable copper production of 150 to 170 million pounds.")
guide(2013, (2013, 1), "Q1 2013 release", "The Company continues to expect full year 2013 attributable gold and copper production of 4.8 – "
      "5.1 million ounces and 150 – 170 million pounds, respectively.")
guide(2013, (2013, 2), "Q2 2013 release", "Maintaining full year 2013 attributable gold and copper production outlook5 of 4.8 – 5.1 million "
      "ounces and 150 – 170 million pounds, respectively;")
guide(2013, (2013, 3), "Q3 2013 release", "As previously announced, Newmont has maintained its 2013 attributable gold production outlook of "
      "4.8 to 5.1 million ounces and has revised its attributable copper production outlook to 135 to 145 million pounds.")

# ── assemble: the earlier facts unchanged ──
for k in ("sources", "history_vintages", "prints", "guides"):
    o = old[k]
    n = f[k]
    if isinstance(o, dict):
        assert all(n[x] == o[x] for x in o), k
    else:
        assert n[:len(o)] == o, k
for x in ("rule_t", "listings", "events", "company_names", "splits", "distributions", "eps_guides"):
    assert f[x] == old[x], x
assert all(s["published"] <= CUT for s in SOURCES.values())
f["sources"] = dict(sorted(SOURCES.items(), key=lambda kv: int(kv[0][2:])))
for p in PR:
    p.setdefault("oz_basis", "sold")
f["_doc"] = old["_doc"].replace("retro/generators/nem/gen_nem.py from the filings",
                                "retro/generators/nem/gen_nem.py (2008-2009) and gen_nem_1013.py (2010-2013) from the filings")
f["price_basis"] = old["price_basis"].replace("(2002-01-01)", "(2002-01-01, then the ten years to AS_OF)")
with open(FACTS, "w", encoding="utf-8") as fh:
    json.dump(f, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_nem_1013.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump({k: v for k, v in CHECK.items() if v}, fh, ensure_ascii=False, indent=1)
print(f"{FACTS}: {len(V)} vintages, {len(PR)} prints, {len(G)} guides, {len(f['dividends'])} dividends, {len(SOURCES)} sources; "
      f"{sum(len(v) for v in CHECK.values())} quotes in {ck}")
for p in PR[-16:]:
    print(p["quarter"], p["published"], p["sales_pct"], p["oz_pct"], p["cas_pct"], p["eps_q"], p["eps_q_prior"], p["eps_pct"], p["margin_bp"],
          p["diluted_shares_m"])
for v in V[-4:]:
    print(v["published"], v["fy_label"], v["eps_normalized"], sorted(v["eps_excluded"]), v["prev_fy_margin"], v["tax_rate"])
