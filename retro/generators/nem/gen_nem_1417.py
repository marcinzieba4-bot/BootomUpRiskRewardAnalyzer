#!/usr/bin/env python3
"""Extend retro/facts/NEM.json with 2014-2017 (filings accepted 2014-01-01 to 2017-12-31), asserting that every earlier fact is
unchanged. Same discipline as gen_nem.py: each raw figure is read from its own row by label (the row text is kept in the fact), every
rate, margin and change is computed, every quote is asserted present in its own filing word for word, and a verbatim checklist is
written. Only filings accepted on or before 2017-12-31 are read. The downloads (keep them outside the repo, e.g. the scratchpad):

    python3 retro/tools/edgar.py index 1164727 <dir>
    python3 retro/tools/edgar.py fetch 1164727 <dir> --from 2013-12-01 --to 2017-12-31 --forms 8-K 8-K/A 10-K 10-K/A 10-Q

    python3 -I retro/generators/nem/gen_nem_1417.py --filings <dir> [--facts-in <2008-2013 sheet>] [--out retro/facts/NEM.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_nem_1417.json

--facts-in is the 2008-2013 sheet gen_nem_1013.py writes (default: retro/facts/NEM.json, which must then hold 2008-2013 only).
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
START, CUT = "2014-01-01", "2017-12-31"
CIK = 1164727
ROWS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("NEM")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
FACTS = A.out or os.path.join(REPO, "retro", "facts", "NEM.json")
old = json.load(open(A.facts_in or os.path.join(REPO, "retro", "facts", "NEM.json"), encoding="utf-8"))
assert all(s["published"] <= "2013-12-31" for s in old["sources"].values()), "--facts-in must be the 2008-2013 sheet"
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
NEXT_ID = [50]


def src(acc, title, supports):
    sid = f"NM{NEXT_ID[0]}"
    NEXT_ID[0] += 1
    day, when = pub(acc)
    SOURCES[sid] = {"published": day, "filed": when, "title": title,
                    "url": f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc.replace('-', '')}/{acc}.txt", "supports": supports}
    return sid


pct = lambda a, b: round((b / a - 1) * 100 + 0.0, 2)
pct1 = lambda a, b: round((b / a - 1) * 100 + 0.0, 1)

fmt = lambda x: f"${x:.2f}" if x >= 0 else f"$({-x:.2f})"          # noqa: E731

# ── the history vintages: the FY2013-FY2016 10-Ks and the 8-K of 2014-06-13 recasting the FY2013 10-K (segments, the deferred tax
# asset and stockpile revisions; a vintage of its own, the MU and MSFT recast rule, as the 8-K of 2009-09-15), each year from the latest
# filing that reports it (earlier years from the latest earlier vintage), each holding the ten fiscal years to the latest one ──────────
K = {2013: ("0001193125-14-061205", "10-K__d653301d10k.rows.txt"), 2014: ("0001564590-15-000777", "10-K__nem-10k_20141231.rows.txt"),
     2015: ("0001558370-16-003258", "10-K__nem-20151231x10k.rows.txt"), 2016: ("0001558370-17-000729", "10-K__nem-20161231x10k.rows.txt")}
KP = {y: path(a, fn) for y, (a, fn) in K.items()}
KID = {}
for y, (a, _) in K.items():
    KID[y] = src(a, f"Newmont FY{y} 10-K", f"history vintage FY{y} (Item 6 selected data, the statements, the MD&A key results); "
                 "the 'why'; Q4 quarterly data (diluted shares)")
RC_ACC = "0001193125-14-236178"
RCP = path(RC_ACC, "EX-99.1__*.rows.txt")
RCID = src(RC_ACC, "Newmont 8-K of 2014-06-13 (the FY2013 10-K's Items 6-8 recast: segments, deferred tax assets, stockpiles)",
           "history vintage FY2013 recast (Item 6 selected data, the statements, the MD&A key results)")
WHY2 = "Our business is dependent on the prices of gold and copper, which fluctuate on a daily basis and are affected by numerous factors beyond our control."
WHY_RISK = "A substantial or extended decline in gold or copper prices would have a material adverse effect on Newmont."
CLIMATE = ("Regulations and pending legislation governing issues involving climate change could result in increased operating costs which "
           "could have a material adverse effect on our business.")


def why(y):
    p = KP[y]
    assert "cyclical" not in " ".join(lines(p)).lower(), (y, "DURABLE needs the company not to call its business cyclical (the MU rule)")
    lead = [x for x in lines(p) if x.startswith("Newmont is one of the world’s largest gold producers")][0].split(". ")[0].rstrip(".") + "."
    q = [quote(p, lead), quote(p, WHY2), quote(p, WHY_RISK)]
    return " ".join(f"'{x}'" for x in q) + (f" (the FY{y} 10-K's own words; it does not call the business cyclical, so DURABLE, the MU rule)")


def selected(p):
    """Item 6: revenues (sales), diluted EPS from continuing operations, five years (latest first); '—' is 0.00."""
    i6 = [i for i, x in enumerate(lines(p)) if re.match(r"^ITEM 6\.( \| | )?SELECTED FINANCIAL DATA \(dollars", x)][-1]
    rev, rrow = row(p, r"^Sales \|", i6, n=5)
    dl = find(p, r"^Diluted:$", i6)
    eps, erow = row(p, r"^Continuing operations \|", dl, n=5)
    div, drow = row(p, r"^Dividends declared per common share \|", i6, n=5)
    return rev, eps, div, [rrow, "Diluted: " + erow, drow]


V = f["history_vintages"]
prev = V[-1]
assert prev["fy_label"] == "FY12" and set(prev["eps_excluded"]) == {"2007", "2011"}


def vintage(y, p, sid, title, excl_new, drop_before, why_text, business_line=None):
    """One vintage: Item 6's five years, the statements' three, excluded years (texts by year) carried and added."""
    global prev
    rev, eps, div, rows = selected(p)
    years = [str(y - k) for k in range(5)]
    e, es = dict(prev["eps_normalized"]), dict(prev["eps_sources"])
    r, rs = dict(prev["revenue_usd_b"]), dict(prev["revenue_sources"])
    excl = dict(prev["eps_excluded"])
    excl.update(excl_new)
    for yy, v_e, v_r in zip(years, eps, rev):
        r[yy], rs[yy] = v_r / 1000, sid
        if yy in excl:
            e.pop(yy, None)
            es.pop(yy, None)
            continue
        assert v_e > 0, (y, yy, v_e, "a year without positive EPS must be excluded")
        e[yy], es[yy] = v_e, sid
    ws = find(p, r"^Weighted average common shares \(millions\):", 0)
    sh, shrow = row(p, r"^Diluted \|", ws, n=3)
    s, ss = dict(prev["diluted_shares_m"]), dict(prev["shares_sources"])
    for k, v in zip(years[:3], sh):
        s[k], ss[k] = v, sid
    for d in (e, es, r, rs, s, ss, excl):                   # the ten fiscal years to the latest one: earlier years leave the history
        for k in [k for k in d if int(k) < drop_before]:
            del d[k]
    yrs = sorted(set(e) | set(excl))
    assert int(yrs[-1]) == y and int(yrs[0]) == drop_before, (y, yrs)
    i8 = [i for i in range(len(lines(p))) if re.match(r"^Income \(loss\) before income and mining tax and other items \| [\d,()]+ \| "
                                                    r"[\d,()]+ \| [\d,()]+$", lines(p)[i])]
    pt, ptrow = cells(p, i8[0])
    tx, txrow = row(p, r"^Income and mining tax (benefit \(expense\)|expense)( \(Note \d+\))? \|(?!.*%)", i8[0], n=3)
    cf, cfrow = row(p, r"^Net cash provided (from|by) (continuing operations|operating activities of continuing operations|continuing operating activities) \|", 0, n=3)
    cx, cxrow = row(p, r"^Additions to property, plant and mine development \| \(", 0, n=3)
    ca, carow = row(p, r"^Cash and cash equivalents \|", 0, n=2)
    gs = find(p, r"^Consolidated gold sales:$", 0)
    gold, grow = row(p, r"^Net \|", gs, n=3)
    if any(re.match(r"^Gold ounces sold \(thousands\)$", x) for x in lines(p)):
        oz, ozrow = row(p, r"^Consolidated \|", find(p, r"^Gold ounces sold \(thousands\)$", 0), n=3)
    else:
        oz, ozrow = row(p, r"^Consolidated gold ounces sold \(thousands\)(\(1\))?:? \|", gs, n=3)
    cs, csrow = row(p, r"^Gold \(per ounce\) \|", find(p, r"^(Consolidated costs applicable to sales: (\(\d\))+|Costs applicable to "
                                                       r"sales(\(\d\))?)$", 0), n=3)
    lab = f"FY{y % 100:02d}"
    doc = title.replace("Newmont ", "")
    v = {**{k: prev[k] for k in ("company", "exchange", "business_line", "margin_signal_name", "kind")},
         "published": SOURCES[sid]["published"], "sources": [sid] + [x for x in dict.fromkeys(list(es.values()) + list(rs.values())
                                                                                              + list(ss.values())) if x != sid],
         "fy_label": lab, "eps_normalized": dict(sorted(e.items())), "eps_sources": dict(sorted(es.items())),
         "eps_excluded": dict(sorted(excl.items())), "eps_first_excluded": {},
         "revenue_usd_b": dict(sorted(r.items())), "revenue_sources": dict(sorted(rs.items())),
         "diluted_shares_m": dict(sorted(s.items())), "shares_sources": dict(sorted(ss.items())),
         "pe_window_start": None, "rows": rows + [shrow, ptrow, txrow, cfrow, cxrow, carow, grow, ozrow, csrow],
         "prev_fy_margin": round(pt[0] / rev[0] * 100, 2),
         "prev_fy_margin_note": f"{lab} income (loss) before income and mining tax and other items ${pt[0]:,.0f}M / sales ${rev[0]:,.0f}M ({doc})",
         "tax_rate": round(-tx[0] / pt[0], 4), "tax_note": f"{lab} income and mining tax ${-tx[0]:,.0f}M / pre-tax ${pt[0]:,.0f}M ({doc})",
         "prev_fy_sales_growth": pct1(rev[1], rev[0]), "prev_fy_oz_k": oz[0], "prev_fy_oz_pct": pct1(oz[1], oz[0]), "prev_fy_cas": cs[0],
         "prev_fy_cas_pct": pct1(cs[1], cs[0]), "franchise_source": doc,
         "dividend_annual": div[0], "dividend_note": f"dividends declared per common share ${div[0]:.3f} in FY{y} (Item 6); the quarterly "
                                                      "rate in force is the latest one a filing states",
         "cash_b": ca[0] / 1000, "fcf_b": round((cf[0] + cx[0]) / 1000, 3), "fcf_label": lab,
         "fcf_note": f"net cash provided by continuing operations ${cf[0]:,.0f}M less additions to property, plant and mine development "
                     f"${-cx[0]:,.0f}M ({doc})",
         "cash_return_text": f"dividends declared ${div[0]:.3f} a share in FY{y}; no repurchase program in the {doc}",
         "groups": [["Gold", gold[0] / 1000, pct1(gold[1], gold[0])],
                    ["Copper", round((rev[0] - gold[0]) / 1000, 3), pct1(rev[1] - gold[1], rev[0] - gold[0])]],
         "groups_basis": f"{lab} sales by metal, net ({doc}; copper as sales less gold)", "why": why_text}
    if business_line:
        v["business_line"] = business_line
    yrs_e = sorted(v["eps_normalized"])
    src_list = sorted({SOURCES[x]["title"] for x in v["eps_sources"].values()})
    v["normalization"] = (
        "GAAP diluted EPS from continuing operations before the cumulative effect of accounting changes, each year from the latest "
        f"filing that reports it ({yrs_e[0]}-{yrs_e[-1]}: {'; '.join(src_list)}; seams, as published); the releases' adjusted net income "
        "also removes items that recur in every period it tabulates (impairments and write-downs of assets, gains on asset sales, tax "
        "items), so GAAP stands (the PEP 2008 core rule)")
    V.append(v)
    prev = v
    return v, eps, pt, tx


def loss_text(fig, doc, adj):
    return (f"a loss: {fmt(fig)} a diluted share from continuing operations ({doc}); {adj}, so no figure excludes only its one-offs; "
            "excluded as the latest year (the NKE FY2018 and XOM FY2020 rule), its own days leave the P/E window, and it stays a gap")


ADJ13 = ("the Q4 2013 release's adjusted net income ($1.40 a share) also removes items that recur (impairments, asset sales, a tax "
         "valuation allowance: the PEP 2008 core rule)")
# FY2013: a loss in every vintage that reports it
v13, eps13, _, _ = vintage(2013, KP[2013], KID[2013], "Newmont FY2013 10-K", {"2013": loss_text(-5.06, "FY2013 10-K", ADJ13)}, 2004, why(2013))
assert eps13[0] == -5.06
# the recast of 2014-06-13: Items 6-8 only (Item 1A stands), so the 'why' is the FY2013 10-K's
vr, epsr, _, _ = vintage(2013, RCP, RCID, "Newmont 8-K of 2014-06-13 (FY2013 10-K Items 6-8 recast)",
                         {"2013": loss_text(-5.21, "the 8-K of 2014-06-13 recasting the FY2013 10-K", ADJ13)}, 2004,
                         v13["why"].replace("(the FY2013 10-K's own words;", "(the FY2013 10-K's own words, which the 8-K of 2014-06-13 recasting "
                                            "its Items 6-8 leaves standing;"))
assert epsr[0] == -5.21 and epsr[1] == 3.76
# FY2014: GAAP $1.10; the Q4 2014 release's listed after-tax items in continuing operations net to a small figure (the AAPL FY2002 test
# and its mirror both pass)
R14 = path("0001157523-15-000640", "EX-99.1__*rows.txt")
rc = find(R14, r".*reconciled to Adjusted net income", 0)
it14 = {lab: row(R14, rf"^{re.escape(lab)} \|", rc, n=4)[0][2] for lab in (
    "Impairments and loss provisions", "Tax valuation allowance", "Restructuring and other", "Asset Sales", "Reclamation Settlement",
    "Abnormal production costs at Batu Hijau")}
cont14 = 548.0
assert abs(sum(it14.values())) < cont14 / 2, it14
v14, eps14, _, _ = vintage(2014, KP[2014], KID[2014], "Newmont FY2014 10-K",
                           {"2013": loss_text(-5.21, "FY2014 10-K", ADJ13)}, 2005, why(2014))
assert eps14[0] == 1.10
# FY2015: the AAPL FY2002 test. The Q4 2015 release's listed after-tax items in continuing operations exceed the year's income from
# continuing operations attributable to Newmont, so reported EPS is under half the year's EPS without them, and the adjusted net income
# also removes items that recur (impairments of investments and long-lived assets, asset sales, tax adjustments), so no figure excludes
# only the one-offs: excluded as the latest year (the FY2011 encoding), then a gap.
R15 = path("0001157523-16-004624", "EX-99.1__*rows.txt")
rc = find(R15, r".*reconciled to Adjusted net income", 0)
LAB15 = ("Impairment of investments (2)", "Impairment of long-lived assets (3)", "Restructuring and other (4)", "Acquisition costs (5)",
         "Loss (gain) on asset and investment sales (6)", "Gain on deconsolidation of TMAC (7)", "Reclamation charges (8)",
         "Ghana Investment Agreement (9)", "Tax adjustments (11)")
it15, rows15 = {}, []
for lab in LAB15:
    vv, t = row(R15, rf"^{re.escape(lab)} \|", rc, n=4)
    it15[lab.rsplit(" (", 1)[0]], _ = vv[2], rows15.append(t)
ni15, ni15row = row(R15, r"^Continuing operations \|", find(R15, r"^Net income \(loss\) attributable to Newmont stockholders:$", 0), n=4)
cont15 = ni15[2]
items15 = sum(it15.values())
assert cont15 == 193 and items15 > cont15, (cont15, items15)
adj15, adj15row = row(R15, r"^Adjusted net income \(loss\) per share, basic \|", rc, n=4)
quote(R15, "GAAP net income attributable to shareholders from continuing operations was $193 million or $0.38 per share")
EXCL15 = ("the AAPL FY2002 test: the Q4 2015 release's listed after-tax items in continuing operations (" + ", ".join(
    f"{k.lower() if not k.startswith(('TMAC', 'Ghana')) else k} ${v:,.0f}M" for k, v in it15.items()) + f"; ${items15:,.0f}M net) exceed "
    f"the year's ${cont15:,.0f}M of income from continuing operations attributable to Newmont, so reported EPS ($0.38 diluted, FY2015 10-K) "
    f"is under half the year's EPS without them; the release's adjusted net income (${adj15[2]:.2f} basic) also removes items that recur "
    "(impairments of investments and long-lived assets, asset sales, tax adjustments: the PEP 2008 core rule), so no figure excludes only "
    "the one-offs; excluded as the latest year (the FY2011 encoding), its own days leave the P/E window, and it stays a gap")
v15, eps15, _, _ = vintage(2015, KP[2015], KID[2015], "Newmont FY2015 10-K",
                           {"2013": loss_text(-5.21, "FY2015 10-K", ADJ13), "2015": EXCL15}, 2006, why(2015))
v15["rows"] += rows15 + [ni15row, adj15row]
assert eps15[0] == 0.38
# FY2016: a loss from continuing operations (Batu Hijau discontinued, sold 2016-11-02); the FY2016 10-K restates 2012-2015 without it,
# FY2015 to $0.00 (no P/E, the F rule) and FY2014 to $1.30
ADJ16 = ("the Q4 2016 release's adjusted net income ($1.16 a diluted share) also removes items that recur (impairments of long-lived "
         "assets, asset sales, reclamation charges, tax adjustments: the PEP 2008 core rule)")
EXCL15b = EXCL15.replace("excluded as the latest year (the FY2011 encoding), its own days leave the P/E window, and it stays a gap",
                         "excluded, a gap; the FY2016 10-K restates it to $0.00 from continuing operations (Batu Hijau discontinued), "
                         "which has no P/E either (the F rule)")
v16, eps16, _, _ = vintage(2016, KP[2016], KID[2016], "Newmont FY2016 10-K",
                           {"2013": loss_text(-4.71, "FY2016 10-K", ADJ13), "2015": EXCL15b,
                            "2016": loss_text(-0.41, "FY2016 10-K", ADJ16)}, 2007, why(2016),
                           business_line="gold producer (the Batu Hijau copper and gold mine in Indonesia sold in 2016)")
assert eps16[:3] == [-0.41, 0.0, 1.30], eps16
for v in (v13, vr, v14, v15, v16) if 0 else ():
    print(v["published"], v["fy_label"], v["eps_normalized"], sorted(v["eps_excluded"]), v["prev_fy_margin"], v["tax_rate"],
          v["prev_fy_oz_k"], v["prev_fy_cas"], v["dividend_annual"], v["fcf_b"])

# ── the prints Q4 2013 - Q3 2017: the earnings releases (8-K exhibit 99.1), each figure against the year-ago quarter as the release
# shows it; diluted shares (display) from the 10-Q filed with the release, Q4 from the 10-K's quarterly data ──
PR = f["prints"]
NEXT = {1: "Q2 print (late July)", 2: "Q3 print (late October)", 3: "Q4 and full-year print with the 10-K (February)",
        4: "Q1 print (late April)"}
TENQ = {(2014, 1): "0001193125-14-158041", (2014, 2): "0001193125-14-285190", (2014, 3): "0001564590-14-004746",
        (2015, 1): "0001564590-15-002819", (2015, 2): "0001558370-15-001173", (2015, 3): "0001558370-15-001997",
        (2016, 1): "0001558370-16-004743", (2016, 2): "0001558370-16-006685", (2016, 3): "0001558370-16-008756",
        (2017, 1): "0001558370-17-002832", (2017, 2): "0001558370-17-005290", (2017, 3): "0001558370-17-007562"}
REL = {(2013, 4): ("0001157523-14-000721", "Feb 20"), (2014, 1): ("0001157523-14-001585", "Apr 24"),
       (2014, 2): ("0001157523-14-003083", "Jul 29"), (2014, 3): ("0001157523-14-004243", "Oct 30"),
       (2014, 4): ("0001157523-15-000640", "Feb 19"), (2015, 1): ("0001157523-15-001283", "Apr 23"),
       (2015, 2): ("0001157523-15-002445", "Jul 22"), (2015, 3): ("0001157523-15-003506", "Oct 28"),
       (2015, 4): ("0001157523-16-004624", "Feb 17"), (2016, 1): ("0001157523-16-005152", "Apr 20"),
       (2016, 2): ("0001157523-16-006130", "Jul 20"), (2016, 3): ("0001157523-16-007034", "Oct 26"),
       (2016, 4): ("0001157523-17-000559", "Feb 21"), (2017, 1): ("0001157523-17-001143", "Apr 24"),
       (2017, 2): ("0001157523-17-002051", "Jul 25"), (2017, 3): ("0001157523-17-002806", "Oct 26")}
RP = {k: path(a, "EX-99.1__*rows.txt") for k, (a, _) in REL.items()}
RID = {}


def ytd_pretax(p, st=0):
    """The statement's pre-tax line (current quarter, year-ago quarter, then the year to date and its year-ago)."""
    return cells(p, find(p, r"^Income (\(loss\) )?before income and mining tax ?and other items \|", st))


def print_q(fy, q):
    acc, release = REL[(fy, q)]
    p = RP[(fy, q)]
    quarter = f"Q{q} {fy}"
    sid = src(acc, f"Newmont {quarter} results (8-K exhibit 99.1)",
              f"{quarter}: sales, consolidated gold ounces {'produced' if (fy, q) in ((2013, 4), (2014, 1)) else 'sold'}, costs applicable to sales per ounce, pre-tax income, diluted EPS from "
              "continuing operations, cash and debt")
    RID[(fy, q)] = sid
    day, when = pub(acc)
    rows = {}
    st = find(p, r"^(NEWMONT MINING CORPORATION ?)?(CONDENSED )?(CONSOLIDATED )?STATEMENTS OF (CONSOLIDATED )?(OPERATIONS|INCOME)", 0)
    rv, rows["rev"] = row(p, r"^Sales \|", st)
    pv, rows["pt"] = ytd_pretax(p, st)
    dl = find(p, r"^Diluted:$", st)
    ev, t = row(p, r"^Continuing operations \|", dl)
    rows["eps"] = "Diluted: " + t
    cav, rows["cash"] = row(p, r"^Cash and cash equivalents \|", st, n=2)
    li = find(p, r"^LIABILITIES$", st)
    curv, rows["cur"] = row(p, r"^(Current portion of debt|Debt) \|", li, n=2)
    ltdv, rows["ltd"] = row(p, r"^Debt \|", find(p, r"^(Current portion of debt|Debt) \|", li) + 1, n=2)
    # ounces: from Q2 2014 consolidated gold ounces sold, the costs applicable to sales reconciliation's 'Gold sold (thousand ounces)'
    # (the per-ounce denominator, against the year-ago quarter: rule T's line and the 2008-2009 prints'); before it, consolidated gold
    # ounces produced, the production table's total row (the row before the copper production header), as in 2010-2013
    gsold = [i for i, x in enumerate(lines(p)) if re.match(r"^Gold sold \(thousand ounces\) \|", x)]
    if gsold:
        ozv, rows["oz"] = cells(p, gsold[0])
        basis = "sold"
    else:
        cu = find(p, r"^Consolidated copper pounds produced \(millions\):$", 0)
        hdr = [i for i in range(cu) if re.match(r"^Consolidated (gold )?ounces ?produced \(thousands\):( \||$)|^Consolidated gold \| "
                                                r"Attributable gold$", lines(p)[i])]
        assert hdr, (quarter, "the consolidated gold ounces produced header")
        c = [x.strip() for x in lines(p)[cu - 1].split("|")]
        assert len(c) in (2, 4) and all(isnum(x) for x in c), (quarter, lines(p)[cu - 1])
        ozv, rows["oz"] = [num(x) for x in c], lines(p)[cu - 1]
        basis = "produced"
    # costs applicable to sales per ounce of gold: the reconciliation's per-ounce row, else the CAS table's consolidated average
    ci = [i for i, x in enumerate(lines(p)) if re.match(r"^Costs applicable to sales per ounce( ?\(\d+\))? \| [\d,]+ \|", x)]
    if ci:
        casv, rows["cas"] = cells(p, ci[0])
    else:
        cs = find(p, r"^(Gold )?Costs Applicable to Sales \(\$/ounce\)", 0)
        casv, rows["cas"] = row(p, r"^Average \|", cs)
    if q in (1, 2, 3):
        qp = path(TENQ[(fy, q)], "10-Q__*.rows.txt")
        shv, t = row(qp, r"^Diluted \|", find(qp, r"(?i)^Weighted average common shares( \(millions\))?:", 0))
        rows["sh"] = "Weighted average common shares (millions): " + t
        sh_src = f"the Q{q} {fy} 10-Q (filed the same day)"
        assert pub(TENQ[(fy, q)])[0] == day, (quarter, "the 10-Q is public the same day as the release")
        CHECK.setdefault(qp, [])
    else:
        kp = KP[fy]
        assert SOURCES[KID[fy]]["published"] == day, (quarter, "the 10-K is public the same day as the release")
        qd = [i for i, x in enumerate(lines(kp)) if re.match(r"^(Quarterly Data|QUARTERLY DATA)", x)]
        assert qd, (quarter, "quarterly data")
        t_cur = find(kp, rf"^{fy}$", qd[-1])
        d1, dr1 = row(kp, r"^Diluted \|", find(kp, r"^Weighted average common shares \(millions\):?$", t_cur), n=4)
        s1, r1 = row(kp, r"^Sales \|", t_cur, n=4)
        assert s1[3] == rv[0], (quarter, "the 10-K's Q4 sales equal the release's", s1, rv)
        shv, rows["sh"] = [d1[3]], f"FY{fy} 10-K quarterly data, {fy}: Weighted average common shares (millions) {dr1}"
        sh_src = f"the FY{fy} 10-K's quarterly data (filed the same day)"
        CHECK.setdefault(kp, [])
    rev, rev0, pt, pt0 = rv[0], rv[1], pv[0], pv[1]
    oz, oz0, cas, cas0, e, e0 = ozv[0], ozv[1], casv[0], casv[1], ev[0], ev[1]
    m, m0 = pt / rev * 100, pt0 / rev0 * 100
    g = lambda a, b: round((b / a - 1) * 100 + 0.0, 1) if a > 0 else round((b - a) / abs(a) * 100 + 0.0, 1)   # noqa: E731
    assert e0 != 0, (quarter, "a year-ago EPS of zero has no growth rate; it needs its encoding")
    d = {"quarter": quarter, "fy": fy, "q": q, "published": day, "release": release, "release_time": when, "source": sid,
         "raw": {"rev_m": rev, "rev_prior_m": rev0, "pretax_m": pt, "pretax_prior_m": pt0, "oz_k": oz, "oz_prior_k": oz0,
                 "cas": cas, "cas_prior": cas0},
         "rows": rows, "sales_b": round(rev / 1000, 3), "sales_pct": pct1(rev0, rev), "oz_pct": pct1(oz0, oz), "oz_basis": basis,
         "cas_pct": pct1(cas0, cas), "pretax_margin": round(m + 0.0, 2), "pretax_margin_prior": round(m0 + 0.0, 2),
         "margin_bp": round((m - m0) * 100 + 0.0, 1), "eps_q": e, "eps_q_prior": e0, "eps_pct": g(e0, e),
         "diluted_shares_m": shv[0], "shares_source": sh_src, "cash_b": round(cav[0] / 1000, 3),
         "debt_note": f"debt ${ltdv[0] + curv[0]:,.0f}M (long-term ${ltdv[0]:,.0f}M and current ${curv[0]:,.0f}M)",
         "rev_note": f"sales ${rev:,.0f}M vs ${rev0:,.0f}M a year earlier",
         "oz_note": f"consolidated gold ounces {basis} {oz:,.0f}K vs {oz0:,.0f}K",
         "cas_note": f"costs applicable to sales ${cas:,.0f} an ounce of gold vs ${cas0:,.0f}",
         "adj_note": None, "next_print": NEXT[q]}
    if q == 4:
        d["source_10k"] = KID[fy]
    d["eps_note"] = f"GAAP diluted EPS from continuing operations {fmt(e)} vs {fmt(e0)}" + (
        "; growth over the year-ago loss's absolute value (the CAT rule)" if e0 < 0 else "")
    tx = norm(" ".join(lines(p)))
    mm = re.search(r"[Aa]djusted net income\d?[^.;]{0,140}?\(?\$\d+\.\d\d per (basic |diluted )?share\)?", tx)
    if mm:
        d["adj_note"] = quote(p, mm.group(0))
    d["source_title"] = SOURCES[sid]["title"]
    PR.append(d)
    return p


for k in REL:
    print_q(*k)

# each Q4 print's full year equals the 10-K that comes with it (the vintage reports its year)
for fy in (2013, 2014, 2015, 2016):
    p = RP[(fy, 4)]
    st = find(p, r"^(NEWMONT MINING CORPORATION ?)?(CONDENSED )?(CONSOLIDATED )?STATEMENTS OF (CONSOLIDATED )?(OPERATIONS|INCOME)", 0)
    sv, _ = row(p, r"^Sales \|", st, n=4)
    dv, _ = row(p, r"^Continuing operations \|", find(p, r"^Diluted:$", st), n=4)
    rev, eps, _, _ = selected(KP[fy])
    assert (sv[2], dv[2]) == (rev[0], eps[0]), (fy, sv, dv, rev[0], eps[0])

# ── the 10-Ks' climate-change risk factor (text only): ENERGY_TRANSITION (live 2015-12-12) is scoped to 'decarbonisation strands oil,
# gas and coal reserves and refining'; Newmont holds no oil, gas or coal reserves and no refining, so the theme is read as out of scope,
# and the 10-K's own words on climate regulation (a cost) are quoted beside the reading, never a factor (the UNH cloud_words encoding) ──
for v, y in ((v13, 2013), (vr, 2013), (v14, 2014), (v15, 2015), (v16, 2016)):
    v["climate_words"] = (f"'{quote(KP[y], CLIMATE)}' (the FY{y} 10-K's risk factor" +
                          (", which the 8-K of 2014-06-13 leaves standing)" if v is vr else ")"))

# ── dividends: each rate from the first filing that states it as declared (not "subject to Board approval") ──
DV = [((2014, 1), 0.025, "Declared a second quarter dividend of $0.025 per share in accordance with the Company’s gold price-linked dividend policy"),
      ((2014, 2), 0.025, "Declared a third quarter dividend of $0.025 per share in accordance with the Company’s gold price-linked dividend policy"),
      ((2014, 3), 0.025, "Declared a fourth quarter dividend of $0.025 per share in accordance with the Company’s gold price-linked dividend policy"),
      ((2014, 4), 0.025, "Declared a fourth quarter dividend of $0.025 per share in accordance with the Company’s gold price-linked dividend policy"),
      ((2015, 1), 0.025, "Declared a first quarter dividend of $0.025 per share in accordance with the Company’s gold price-linked dividend policy"),
      ((2015, 2), 0.025, "Declared a second quarter dividend of $0.025 per share"),
      ((2015, 3), 0.025, "Maintained third quarter dividend of $0.025 per share"),
      ((2015, 4), 0.025, "Maintained fourth quarter dividend of $0.025 per share"),
      ((2016, 1), 0.025, "Maintained first quarter dividend of $0.025 per share"),
      ((2016, 2), 0.025, "Maintained second quarter dividend of $0.025 per share"),
      ((2016, 3), 0.05, "Doubled fourth quarter dividend to $0.05 per share"),
      ((2016, 4), 0.05, "Doubled the fourth quarter dividend to $0.05 per share, in line with Newmont’s improved gold price-linked dividend policy"),
      ((2017, 2), 0.075, "second quarter dividend triples from the prior year quarter to $0.075 per share"),
      ((2017, 3), 0.075, "third quarter dividend declared increased 50 percent from the prior year quarter to $0.075 per share")]
for k, q_, s_ in DV:
    f["dividends"].append({"published": SOURCES[RID[k]]["published"], "quarterly": q_, "source": RID[k],
                           "note": f"${q_:.3f}".rstrip("0").rstrip(".") + f" a quarter (${q_ * 4:.2f} a year): '{quote(RP[k], s_)}' "
                                   f"(the Q{k[1]} {k[0]} release)"})

# ── outlooks (display only: attributable gold production and costs applicable to sales or all-in sustaining costs per ounce; method r2
# has no volume input and none for cost components, the XOM production and MSFT segment rules), one quote a release, cut to its year ──
UNUSED = ("a production and unit-cost outlook: method r2 has no input for a production guide (the XOM rule) or for cost components "
          "(the MSFT segment rule), so no field; no filing guides revenue, EPS or a margin")
G = f["guides"]


def guide(fy, key_or_acc, doc, s_, pat="EX-99.1__*rows.txt"):
    if isinstance(key_or_acc, tuple):
        sid, p = RID[key_or_acc], RP[key_or_acc]
    else:
        p = path(key_or_acc, pat)
        sid = src(key_or_acc, doc, "a display-only outlook (guide line)")
    G.append({"fy": fy, "published": SOURCES[sid]["published"], "source": sid, "doc": doc, "display": quote(p, s_), "unused": UNUSED})


guide(2014, "0001157523-14-000327", "8-K/A of 2014-01-31 (preliminary 2013 operating results, 2014 outlook; it amends the 8-K of 2014-01-30's "
      "outlook footnotes)", "Newmont expects consolidated 2014 gold and copper production to be approximately 5.0 to 5.3 million ounces and "
      "160 to 175 thousand tonnes, respectively, at CAS of approximately $740 to $790 per ounce and $2.00 to $2.25 per pound.")
guide(2014, (2013, 4), "Q4 2013 release", "In 2014, all-in sustaining costs are anticipated to be between $1,075 and $1,175 per gold ounce "
      "and $2.75 to $2.95 per copper pound of production.")
guide(2014, (2014, 1), "Q1 2014 release", "The Company continues to expect total attributable gold production of between 4.6 to 4.9 million "
      "ounces at CAS of $740 to $790 per ounce and AISC of $1,075 to $1,175 per ounce.")
guide(2014, (2014, 2), "Q2 2014 release", "Increased attributable gold production outlook by two percent to 4.7 to 5.0 million ounces in 2014;")
guide(2014, (2014, 3), "Q3 2014 release", "For 2014, we expect costs at the low end of our cost guidance and we remain on track to meet our "
      "production outlook")
guide(2015, (2014, 4), "Q4 2014 release", "expect attributable gold production of between 4.6 to 4.9 million ounces in 2015, at CAS of between "
      "$660 and $710 per ounce and AISC of between $960 and $1,020 per ounce in 2015")
guide(2015, (2015, 1), "Q1 2015 release", "Maintaining full year 2015 outlook5 between 4.6 and 4.9 million attributable ounces of gold, at CAS "
      "between $660 and $710 per ounce and AISC between $960 and $1,020 per ounce")
guide(2015, (2015, 2), "Q2 2015 release", "new guidance forecasts attributable gold production of between 4.7 and 5.1 million ounces, AISC of "
      "between $920 and $980 per ounce, and CAS of between $630 and $680 per ounce")
guide(2015, (2015, 3), "Q3 2015 release", "expect AISC of between $880 and $940 per ounce, and CAS of between $620 and $660 per ounce; "
      "attributable gold production maintained at between 4.7 and 5.1 million ounces")
guide(2016, "0001157523-15-003960", "8-K of 2015-12-02 (updated operating and financial outlook)", "Attributable gold production3 is "
      "expected to increase from between 4.8 and 5.3 million ounces in 2016")
guide(2016, (2015, 4), "Q4 2015 release", "Attributable gold production is expected to increase from between 4.8 and 5.3 million ounces in 2016")
guide(2016, (2016, 1), "Q1 2016 release", "Attributable gold production is expected to increase from between 4.8 and 5.3 million ounces in 2016")
guide(2016, (2016, 2), "Q2 2016 release", "Attributable gold production is expected to increase from between 4.7 and 5.0 million ounces in 2016")
guide(2016, (2016, 3), "Q3 2016 release", "Attributable gold production is expected to be between 4.8 and 5.0 million ounces in 2016.")
guide(2017, (2016, 4), "Q4 2016 release", "Attributable gold production — Outlook is in line with previously published five-year guidance and "
      "expected to increase to between 4.9 and 5.4 million ounces in 2017")
guide(2017, (2017, 1), "Q1 2017 release", "Outlook for 2017 remains at between 4.9 and 5.4 million ounces")
guide(2017, (2017, 2), "Q2 2017 release", "attributable production guidance improves to between 5.0 and 5.4 million ounces of gold; CAS guidance "
      "improves to between $675 and $715 per ounce")
guide(2017, (2017, 3), "Q3 2017 release", "Maintained company production, cost and capital outlook for 2017")
guide(2018, "0001157523-17-003191", "8-K of 2017-12-06 (2018 and longer-term outlook)", "increasing attributable gold production guidance to "
      "between 4.9 and 5.4 million ounces and improving AISC2 to between $965 and $1,025 per ounce, compared to previous 2018 guidance")

# ── assemble: the earlier facts unchanged ──
for k in ("sources", "history_vintages", "prints", "guides", "dividends"):
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
f["_doc"] = old["_doc"].replace("gen_nem.py (2008-2009) and gen_nem_1013.py (2010-2013) from the filings",
                                "gen_nem.py (2008-2009), gen_nem_1013.py (2010-2013) and gen_nem_1417.py (2014-2017) from the filings")
with open(FACTS, "w", encoding="utf-8") as fh:
    json.dump(f, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_nem_1417.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump({k: v for k, v in CHECK.items() if v}, fh, ensure_ascii=False, indent=1)
print(f"{FACTS}: {len(V)} vintages, {len(PR)} prints, {len(G)} guides, {len(f['dividends'])} dividends, {len(SOURCES)} sources; "
      f"{sum(len(v) for v in CHECK.values())} quotes in {ck}")
for p in PR[-16:]:
    print(p["quarter"], p["published"], p["release_time"][-40:], p["sales_pct"], p["oz_basis"], p["oz_pct"], p["cas_pct"], p["eps_q"],
          p["eps_q_prior"], p["eps_pct"], p["margin_bp"], p["diluted_shares_m"])
for v in V[-5:]:
    print(v["published"], v["fy_label"], v["eps_normalized"], sorted(v["eps_excluded"]), v["prev_fy_margin"], v["tax_rate"])
