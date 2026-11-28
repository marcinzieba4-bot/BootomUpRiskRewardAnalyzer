#!/usr/bin/env python3
"""Extend retro/facts/NEM.json with 2018-2021 (filings accepted 2018-01-01 to 2021-12-31), asserting that every earlier fact is
unchanged. Same discipline as gen_nem.py: each raw figure is read from its own row by label (the row text is kept in the fact), every
rate, margin and change is computed, every quote is asserted present in its own filing word for word, and a verbatim checklist is
written. Only filings accepted on or before 2021-12-31 are read. The downloads (keep them outside the repo, e.g. the scratchpad):

    python3 retro/tools/edgar.py index 1164727 <dir>
    python3 retro/tools/edgar.py fetch 1164727 <dir> --from 2017-12-01 --to 2021-12-31 --forms 8-K 8-K/A 10-K 10-K/A 10-Q

    python3 -I retro/generators/nem/gen_nem_1821.py --filings <dir> [--facts-in <2008-2017 sheet>] [--out retro/facts/NEM.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_nem_1821.json

--facts-in is the 2008-2017 sheet gen_nem_1417.py writes (default: retro/facts/NEM.json, which must then hold 2008-2017 only).
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
START, CUT = "2018-01-01", "2021-12-31"
CIK = 1164727
ROWS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("NEM")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
FACTS = A.out or os.path.join(REPO, "retro", "facts", "NEM.json")
old = json.load(open(A.facts_in or os.path.join(REPO, "retro", "facts", "NEM.json"), encoding="utf-8"))
assert all(s["published"] <= "2017-12-31" for s in old["sources"].values()), "--facts-in must be the 2008-2017 sheet"
f = copy.deepcopy(old)
CHECK = {}
TEXT = {}
ZW = "​"
norm = lambda s: re.sub(r"\s+", " ", s.replace(ZW, " ")).strip()


def path(acc, pat):
    hits = glob.glob(os.path.join(SP, "*", acc, pat))
    assert len(hits) == 1, (acc, pat, hits)
    return hits[0]


def lines(p):
    """The rows of a converted filing, with the zero-width cells (FY2019 10-K) dropped."""
    if p not in TEXT:
        out = []
        for x in open(p, encoding="utf-8", errors="replace").read().split("\n"):
            c = [norm(y) for y in x.split("|")]
            out.append(" | ".join(y for y in c if y) if "|" in x else norm(x))
        TEXT[p] = out
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
NEXT_ID = [74]


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

# ── the history vintages: the FY2017-FY2020 10-Ks and the 8-K of 2018-04-26 re-filing the FY2017 10-K's Items 1, 2, 6, 7 and 8 (the
# ASU 2016-15 cash flow reclassification and the correction of immaterial errors in the reclamation and remediation liabilities; a
# vintage of its own, the MU and MSFT recast rule, as the 8-Ks of 2009-09-15 and 2014-06-13), each year from the latest filing that
# reports it (earlier years from the latest earlier vintage), each holding the ten fiscal years to the latest one ──────────────────
K = {2017: ("0001558370-18-000894", "10-K__nem-20171231x10k.rows.txt"), 2018: ("0001558370-19-000806", "10-K__nem-20181231x10k.rows.txt"),
     2019: ("0001558370-20-001041", "10-K__nem-20191231x10k047aaa.rows.txt"), 2020: ("0001164727-21-000027", "10-K__nem-20201231.rows.txt")}
KP = {y: path(a, fn) for y, (a, fn) in K.items()}
KID = {}
for y, (a, _) in K.items():
    KID[y] = src(a, f"Newmont FY{y} 10-K", f"history vintage FY{y} ({'the statements, as Item 6 is omitted' if y == 2020 else 'Item 6 selected data, the statements'}, "
                 "the results and highlights table); the 'why'; Q4 quarterly data (diluted shares)")
RC_ACC = "0001558370-18-003282"
RCP = path(RC_ACC, "EX-99.1__*.rows.txt")
RCID = src(RC_ACC, "Newmont 8-K of 2018-04-26 (the FY2017 10-K's Items 1, 2, 6, 7 and 8 re-filed: ASU 2016-15, reclamation liability corrections)",
           "history vintage FY2017 recast (Item 6 selected data, the statements, the results and highlights table)")
LEAD = ("Newmont is one of the world’s largest gold producers", "Newmont is the world’s leading gold company")
WHY2 = {2017: "Our business is dependent on the prices of gold and copper, which fluctuate on a daily basis and are affected by numerous factors beyond our control.",
        2018: "Our business is dependent on the prices of gold and copper, which fluctuate on a daily basis and are affected by numerous factors beyond our control.",
        2019: "Our business is dependent on the prices of gold, silver, copper, zinc and lead, which fluctuate on a daily basis and are affected by numerous factors beyond our control.",
        2020: "Our business is dependent on the prices of gold, silver, copper, zinc and lead, which fluctuate on a daily basis and are affected by numerous factors beyond our control."}
WHY_RISK = {2017: "A substantial or extended decline in gold or copper prices would have a material adverse effect on Newmont.",
            2018: "A substantial or extended decline in gold or copper prices would have a material adverse effect on Newmont.",
            2019: "A substantial or extended decline in gold, silver, copper, zinc or lead prices would have a material adverse effect on us.",
            2020: "A substantial or extended decline in gold, silver, copper, zinc or lead prices would have a material adverse effect on us."}
CYCL = "The metals markets are cyclical"
CLIMATE = {2017: "Regulations and pending legislation governing issues involving climate change could result in increased operating costs which "
                 "could have a material adverse effect on our business.",
           2018: "Regulations and pending legislation governing issues involving climate change could result in increased operating costs which "
                 "could have a material adverse effect on our business.",
           2019: "Legislation and increased regulation and requirements regarding climate change are resulting in increased costs on us, our "
                 "venture partners and our suppliers, including increased energy, capital equipment, environmental monitoring and reporting "
                 "and other costs to comply with such regulations.",
           2020: "Policy and regulatory risk related to actual and proposed changes in climate- and water-related laws, regulations and taxes "
                 "developed to regulate the transition to a low-carbon economy may result in increased costs for our operations, venture "
                 "partners and our suppliers, including increased energy, capital equipment, environmental monitoring and reporting and other "
                 "costs to comply with such regulations."}
CRYPTO = "Changing investor or consumer sentiment, including in connection with transition to a low-carbon economy, investor interest in crypto currencies and other investment alternatives"


def why(y, p=None):
    """The 'why' and the kind: the lead sentence, the price-dependence sentence and the gold-price risk factor; from the FY2018 10-K the
    business section also says 'The metals markets are cyclical', the company's own words on its markets, so CYCLICAL (the CB rule:
    'historically cyclical' markets); the FY2017 10-K does not call the business or its markets cyclical, so DURABLE (the MU rule)."""
    p = p or KP[y]
    txt = " ".join(lines(p))
    lead = [x for x in lines(p) if x.startswith(LEAD)][0].split(". ")[0].rstrip(".") + "."
    q = [quote(p, lead), quote(p, WHY2[y]), quote(p, WHY_RISK[y])]
    if "cyclical" in txt.lower():
        assert y >= 2018 and CYCL in txt, (y, "cyclical")
        q.append(quote(p, CYCL))
        return ("CYCLICAL", " ".join(f"'{x}'" for x in q) + f" (the FY{y} 10-K's own words; it calls the metals markets it sells into cyclical, "
                "so CYCLICAL, the CB rule)")
    return "DURABLE", " ".join(f"'{x}'" for x in q) + f" (the FY{y} 10-K's own words; it does not call the business cyclical, so DURABLE, the MU rule)"


def item6(p):
    """Item 6: revenues (sales), diluted EPS from continuing operations, five years (latest first); '—' is 0.00."""
    i6 = [i for i, x in enumerate(lines(p)) if re.match(r"^ITEM 6\.( \| | )?SELECTED FINANCIAL DATA \(dollars", x)][-1]
    rev, rrow = row(p, r"^Sales \|", i6, n=5)
    dl = find(p, r"^Diluted:( \|)?$", i6)
    eps, erow = row(p, r"^Continuing operations \|", dl, n=5)
    div, drow = row(p, r"^Dividends declared per common share \|", i6, n=5)
    return rev, eps, div, [rrow, "Diluted: " + erow, drow]


def statements(p):
    """No Item 6 (the FY2020 10-K): the consolidated statements of operations' three years (the ACN FY21 and LLY rule)."""
    st = find(p, r"^CONSOLIDATED STATEMENTS OF OPERATIONS$", 0)
    rev, rrow = row(p, r"^Sales( \(Note \d+\))? \|", st, n=3)
    dl = find(p, r"^Diluted:$", st)
    eps, erow = row(p, r"^Continuing operations \|", dl, n=3)
    div, drow = row(p, r"^Regular cash dividends declared per common share for the period ended December 31 \|", 0, n=3)
    return rev, eps, div, ["Statements of operations: " + rrow, "Diluted: " + erow, drow]


V = f["history_vintages"]
prev = V[-1]
assert prev["fy_label"] == "FY16" and set(prev["eps_excluded"]) == {"2007", "2011", "2013", "2015", "2016"}


def vintage(y, p, sid, title, excl_new, drop_before, kind_why, company, business_line, climate):
    """One vintage: Item 6's five years (or the statements' three), the results and highlights table's three, excluded years (texts by
    year) carried and added."""
    global prev
    kind, why_text = kind_why
    rev, eps, div, rows = (statements if y == 2020 else item6)(p)
    years = [str(y - k) for k in range(len(rev))]
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
    dil = [i for i, x in enumerate(lines(p)) if re.match(r"^Diluted( \(\d+\))? \| \d{3} \| \d{3} \| \d{3}$", x)]
    sh, shrow = cells(p, dil[0])
    s, ss = dict(prev["diluted_shares_m"]), dict(prev["shares_sources"])
    for k, v in zip(years[:3], sh):
        s[k], ss[k] = v, sid
    for d in (e, es, r, rs, s, ss, excl):                   # the ten fiscal years to the latest one: earlier years leave the history
        for k in [k for k in d if int(k) < drop_before]:
            del d[k]
    yrs = sorted(set(e) | set(excl))
    assert int(yrs[-1]) == y and int(yrs[0]) == drop_before, (y, yrs)
    st = find(p, r"^(CONSOLIDATED STATEMENTS OF OPERATIONS|.*CONSOLIDATED STATEMENTS OF OPERATIONS)$", find(p, r"^ITEM 8\.", 0))
    pt, ptrow = row(p, r"^Income \(loss\) before income and mining tax and other items \|", st, n=3)
    tx, txrow = row(p, r"^Income and mining tax (benefit \(expense\)|expense)( \(Note \d+\))? \|(?!.*%)", st, n=3)
    cx, cxrow = row(p, r"^Additions to property, plant and mine development \|", st, n=3)
    ca, carow = row(p, r"^Cash and cash equivalents \|", find(p, r"^(NEWMONT [A-Z ]+ )?CONSOLIDATED BALANCE SHEETS$", st), n=2)
    fr = find(p, r"^Financial Results:$", 0)              # the results and highlights table (financial, then operating results)
    gold, grow = row(p, r"^Gold \|", fr, n=3)
    cf, cfrow = row(p, r"^Net cash provided by \(used in\) operating activities of continuing operations \|", fr, n=3)
    orr = find(p, r"^Operating Results:$", 0)
    oz, ozrow = row(p, r"^Sold \|", find(p, r"^Consolidated gold (ounces \(thousands\)|\(thousand ounces\)):$", orr), n=3)
    cs, csrow = row(p, r"^Gold \(per ounce\) \|", find(p, r"^Consolidated costs applicable to sales:", orr), n=3)
    assert find(p, r"^Consolidated costs applicable to sales:", orr) < find(p, r"^All-in sustaining costs:", orr)
    lab = f"FY{y % 100:02d}"
    doc = title.replace("Newmont ", "")
    other = "Copper" if y < 2019 else "Other metals"
    v = {**{k: prev[k] for k in ("exchange", "margin_signal_name")}, "company": company, "business_line": business_line, "kind": kind,
         "published": SOURCES[sid]["published"], "sources": [sid] + [x for x in dict.fromkeys(list(es.values()) + list(rs.values())
                                                                                              + list(ss.values())) if x != sid],
         "fy_label": lab, "eps_normalized": dict(sorted(e.items())), "eps_sources": dict(sorted(es.items())),
         "eps_excluded": dict(sorted(excl.items())), "eps_first_excluded": {},
         "revenue_usd_b": dict(sorted(r.items())), "revenue_sources": dict(sorted(rs.items())),
         "diluted_shares_m": dict(sorted(s.items())), "shares_sources": dict(sorted(ss.items())),
         "pe_window_start": None, "rows": rows + [shrow, ptrow, txrow, cfrow, cxrow, carow, grow, ozrow, csrow],
         "prev_fy_margin": round(pt[0] / rev[0] * 100, 2),
         "prev_fy_margin_note": f"{lab} income (loss) before income and mining tax and other items ${pt[0]:,.0f}M / sales ${rev[0]:,.0f}M ({doc})",
         "tax_rate": round(-tx[0] / pt[0] if tx[0] < 0 or "benefit (expense)" in txrow else tx[0] / pt[0], 4),
         "tax_note": f"{lab} income and mining tax ${abs(tx[0]):,.0f}M / pre-tax ${pt[0]:,.0f}M ({doc})",
         "prev_fy_sales_growth": pct1(rev[1], rev[0]), "prev_fy_oz_k": oz[0], "prev_fy_oz_pct": pct1(oz[1], oz[0]), "prev_fy_cas": cs[0],
         "prev_fy_cas_pct": pct1(cs[1], cs[0]), "franchise_source": doc,
         "dividend_annual": div[0], "dividend_note": f"{'regular ' if y == 2020 else ''}dividends declared per common share ${div[0]:.3f} in FY{y} "
                                                      f"({'the results and highlights table' if y == 2020 else 'Item 6'}"
                                                      f"{'; the $0.88 special dividend of 2019 included' if y == 2019 else ''}); the quarterly "
                                                      "rate in force is the latest one a filing states",
         "cash_b": ca[0] / 1000, "fcf_b": round((cf[0] + cx[0]) / 1000, 3), "fcf_label": lab,
         "fcf_note": f"net cash provided by (used in) operating activities of continuing operations ${cf[0]:,.0f}M less additions to "
                     f"property, plant and mine development ${-cx[0]:,.0f}M ({doc})",
         "cash_return_text": f"dividends declared ${div[0]:.2f} a share in FY{y}" + (" (regular)" if y == 2020 else "")
                             + ("" if y == 2017 else "; share repurchases text only"),
         "groups": [["Gold", gold[0] / 1000, pct1(gold[1], gold[0])],
                    [other, round((rev[0] - gold[0]) / 1000, 3), pct1(rev[1] - gold[1], rev[0] - gold[0])]],
         "groups_basis": f"{lab} sales by metal ({doc}; {other.lower()} as sales less gold)", "why": why_text,
         "climate_words": climate}
    yrs_e = sorted(v["eps_normalized"])
    src_list = sorted({SOURCES[x]["title"] for x in v["eps_sources"].values()})
    v["normalization"] = (
        "GAAP diluted EPS from continuing operations before the cumulative effect of accounting changes, each year from the latest "
        f"filing that reports it ({yrs_e[0]}-{yrs_e[-1]}: {'; '.join(src_list)}; seams, as published); the releases' adjusted net income "
        "also removes items that recur in every period it tabulates (impairments and write-downs of assets, gains on asset sales, changes "
        "in the fair value of investments, reclamation charges, tax items), so GAAP stands (the PEP 2008 core rule)")
    V.append(v)
    prev = v
    return v, eps, pt, tx


def loss_text(fig, doc, adj):
    return (f"a loss: {fmt(fig)} a diluted share from continuing operations ({doc}); {adj}, so no figure excludes only its one-offs; "
            "excluded as the latest year (the NKE FY2018 and XOM FY2020 rule), its own days leave the P/E window, and it stays a gap")


def rec(acc, cont_lab=r"^Net income \(loss\) attributable to Newmont stockholders from continuing operations \|"):
    """A Q4 release's adjusted net income reconciliation for the year: every listed item (each row between the continuing-operations
    line and 'Adjusted net income (loss)'), the year's column (the third of four, or the fourth of six with per-share columns)."""
    p = path(acc, "EX-99.1__*rows.txt")
    i0 = find(p, r"^Management uses Adjusted net income", 0)
    c0 = find(p, cont_lab, i0)
    c1 = find(p, r"^Adjusted net income \(loss\)( \(\d+\))? \|", c0)
    col = lambda v: v[2] if len(v) == 4 else v[3]
    cont, crow = cells(p, c0)
    items, rows_ = {}, [crow]
    for i in range(c0 + 1, c1):
        vv, t = cells(p, i)
        items[re.sub(r"\s*\(\d+\)$", "", t.split(" | ")[0])] = col(vv)
        rows_.append(t)
    adj, arow = cells(p, c1)
    rows_.append(arow)
    assert round(col(cont) + sum(items.values())) == col(adj), (acc, col(cont), sum(items.values()), col(adj))
    return p, col(cont), items, col(adj), rows_


ADJ17 = ("the Q4 2017 release's adjusted net income ($1.46 a diluted share) also removes items that recur (reclamation charges, asset "
         "sales, impairments, the Tax Cuts and Jobs Act re-measurement and restructuring, valuation allowances: the PEP 2008 core rule)")
# FY2017: a loss in every vintage that reports it (the Tax Cuts and Jobs Act charges)
P17, c17, it17, a17, rows17 = rec("0001157523-18-000390")
assert (c17, a17) == (-60, 780), (c17, a17)
COMPANY0 = "Newmont Mining Corporation"
v17, eps17, _, _ = vintage(2017, KP[2017], KID[2017], "Newmont FY2017 10-K", {"2017": loss_text(-0.11, "FY2017 10-K", ADJ17)}, 2008, why(2017),
                           COMPANY0, "gold producer (the Batu Hijau copper and gold mine in Indonesia sold in 2016)", f"'{quote(KP[2017], CLIMATE[2017])}' (the FY2017 10-K's risk factor)")
v17["rows"] += rows17
assert eps17[:2] == [-0.11, -0.41] and eps17[3] == 1.30, eps17
# FY2015 in the FY2017 10-K: '—' ($0.00, no P/E, the F rule) as in the FY2016 vintage; the recast and later vintages print $(0.02)
EXCL15 = v17["eps_excluded"]["2015"]
EXCL15r = EXCL15.replace("the FY2016 10-K restates it to $0.00 from continuing operations (Batu Hijau discontinued), which has no P/E either (the F rule)",
                         "the FY2016 10-K restates it to $0.00 from continuing operations (Batu Hijau discontinued), which has no P/E either (the F "
                         "rule), and the 8-K of 2018-04-26 recasting the FY2017 10-K to $(0.02), a loss")
assert EXCL15r != EXCL15
# the recast of 2018-04-26: Items 1, 2, 6, 7 and 8 (Item 1A stands), so the 'why' is the FY2017 10-K's with the re-filed Item 1's lead
kw = why(2017)
vr, epsr, _, _ = vintage(2017, RCP, RCID, "Newmont 8-K of 2018-04-26 (FY2017 10-K Items 1, 2, 6, 7 and 8 recast)",
                         {"2015": EXCL15r, "2017": loss_text(-0.14, "the 8-K of 2018-04-26 recasting the FY2017 10-K", ADJ17),
                          "2016": v17["eps_excluded"]["2016"].replace("$(0.41)", "$(0.42)").replace("(FY2016 10-K)", "(the 8-K of 2018-04-26 recasting the FY2017 10-K)")},
                         2008, (kw[0], kw[1].replace("(the FY2017 10-K's own words;", "(the FY2017 10-K's own words, which the 8-K of 2018-04-26 "
                                                     "re-filing its Items 1, 2, 6, 7 and 8 leaves standing;")),
                         COMPANY0, v17["business_line"], v17["climate_words"].replace("(the FY2017 10-K's risk factor)", "(the FY2017 10-K's risk "
                                                                                       "factor, which the 8-K of 2018-04-26 leaves standing)"))
assert epsr[:4] == [-0.14, -0.42, -0.02, 1.28], epsr
# FY2018: the AAPL FY2002 test, the FY2011 and FY2015 encoding. The Q4 2018 release's listed items in continuing operations, every one
# summed with the tax effect and tax lines (recurring ones included), exceed the year's income from continuing operations attributable to
# Newmont, so reported EPS is under half the year's EPS without them; the adjusted net income also removes items that recur
# (impairments, asset sales, changes in the fair value of investments, reclamation charges, tax items), so no figure excludes only the
# one-offs: excluded as the latest year, then a gap.
P18, c18, it18, a18, rows18 = rec("0001157523-19-000406")
items18 = sum(it18.values())
assert c18 == 280 and items18 > c18 and a18 == 718, (c18, items18, a18)


def items_text(it):
    return ", ".join(f"{k[:2].lower() + k[2:] if k.startswith('(') else k[0].lower() + k[1:] if not k.startswith(('Nevada', 'Goldcorp', 'Emigrant', 'La Quinua', 'Tax Cuts', 'COVID')) else k} "
                     f"{'$' if v >= 0 else '$('}{abs(v):,.0f}{'M' if v >= 0 else ')M'}" for k, v in it.items() if v != 0)


EXCL18 = ("the AAPL FY2002 test (the FY2011 and FY2015 encoding): the Q4 2018 release's listed items in continuing operations (" + items_text(it18)
          + f"; ${items18:,.0f}M net after the tax lines) exceed the year's ${c18:,.0f}M of income from continuing operations attributable "
          f"to Newmont, so reported EPS ($0.53 diluted, FY2018 10-K) is under half the year's EPS without them; the release's adjusted net "
          f"income (${a18:,.0f}M, $1.34 a diluted share) also removes items that recur (impairments, asset sales, changes in the fair value "
          "of investments, reclamation charges, tax items: the PEP 2008 core rule), so no figure excludes only the one-offs; excluded as the "
          "latest year, its own days leave the P/E window, and it stays a gap")
LOSS17 = lambda doc: loss_text(-0.14, doc, ADJ17)
v18, eps18, _, _ = vintage(2018, KP[2018], KID[2018], "Newmont FY2018 10-K", {"2017": LOSS17("FY2018 10-K"), "2018": EXCL18}, 2009, why(2018),
                           COMPANY0, "gold producer (the Goldcorp acquisition agreed on 2019-01-14, pending)",
                           f"'{quote(KP[2018], CLIMATE[2018])}' (the FY2018 10-K's risk factor)")
v18["rows"] += rows18
assert eps18 == [0.53, -0.14, -0.42, -0.02, 1.28], eps18
# FY2019: the mirror of the AAPL FY2002 test (method r2, the AVGO FY2018 rule). The Q4 2019 release's listed items net to a benefit
# (the $2,390M gain on the formation of Nevada Gold Mines above all) larger than the year's income without them ($970M adjusted), so
# reported EPS ($3.91) is more than double the year's EPS without them, and the adjusted net income also removes recurring items: excluded
# as the latest year, then a gap.
P19, c19, it19, a19, rows19 = rec("0001157523-20-000234")
items19 = sum(it19.values())
assert c19 == 2877 and a19 == 970 and -items19 > a19, (c19, items19, a19)
EXCL19 = ("the mirror of the AAPL FY2002 test (method r2, the AVGO FY2018 rule): the Q4 2019 release's listed items in continuing operations ("
          + items_text(it19) + f"; ${-items19:,.0f}M of net benefits after the tax lines) exceed the year's ${a19:,.0f}M of income without "
          f"them, so reported EPS ($3.91 diluted, FY2019 10-K) is more than double the year's EPS without them ($1.32 adjusted, a diluted "
          "share); the adjusted net income also removes items that recur (changes in the fair value of investments, reclamation charges, "
          "asset sales, tax items: the PEP 2008 core rule), so no figure excludes only the one-offs; excluded as the latest year, its own "
          "days leave the P/E window, and it stays a gap")
COMPANY1 = "Newmont Corporation"
BL19 = ("gold producer with copper, silver, lead and zinc co-products (Goldcorp acquired on 2019-04-18; Nevada Gold Mines, 38.5%, "
        "from 2019-07-01)")
v19, eps19, _, _ = vintage(2019, KP[2019], KID[2019], "Newmont FY2019 10-K",
                           {"2017": LOSS17("FY2019 10-K"), "2018": EXCL18.replace("(the FY2011 and FY2015 encoding)", "(the FY2011 and FY2015 encoding), a gap"),
                            "2019": EXCL19}, 2010, why(2019), COMPANY1, BL19, f"'{quote(KP[2019], CLIMATE[2019])}' (the FY2019 10-K's risk factor)")
v19["rows"] += rows19
assert eps19 == [3.91, 0.53, -0.14, -0.42, -0.02], eps19
# FY2020: GAAP $3.31 kept. The Q4 2020 release's listed items net to a benefit of $526M against $2,140M of income without them, under
# half (the mirror is not met), and no charge outweighs the year; FY2020 anchors from the FY2020 10-K.
P20, c20, it20, a20, rows20 = rec("0001157523-21-000209")
items20 = sum(it20.values())
assert c20 == 2666 and a20 == 2140 and 0 < -items20 < a20, (c20, items20, a20)
v20, eps20, _, _ = vintage(2020, KP[2020], KID[2020], "Newmont FY2020 10-K",
                           {"2017": LOSS17("FY2020 10-K"), "2018": v19["eps_excluded"]["2018"], "2019": EXCL19.replace(
                               "excluded as the latest year, its own days leave the P/E window, and it stays a gap", "excluded, a gap")},
                           2011, why(2020), COMPANY1, BL19, f"'{quote(KP[2020], CLIMATE[2020])}' (the FY2020 10-K's risk factor)")
v20["rows"] += rows20
v20["normalization"] += "; " + (f"FY2020 kept at GAAP $3.31: the Q4 2020 release's listed items in continuing operations ({items_text(it20)}; "
                    f"${-items20:,.0f}M of net benefits after the tax lines) are under the year's ${a20:,.0f}M of income without them, so "
                    "neither the AAPL FY2002 test nor its mirror is met")
v20["crypto_words"] = (f"'{quote(KP[2020], CRYPTO)}' (the FY2020 10-K's list of factors that move the gold price)")
assert eps20 == [3.31, 3.91, 0.53], eps20
for v in (v17, vr, v18, v19, v20) if 0 else ():
    print(v["published"], v["fy_label"], v["eps_normalized"], sorted(v["eps_excluded"]), v["prev_fy_margin"], v["tax_rate"],
          v["prev_fy_oz_k"], v["prev_fy_cas"], v["dividend_annual"], v["fcf_b"], v["kind"])

# ── the prints Q4 2017 - Q3 2021: the earnings releases (8-K exhibit 99.1), each figure against the year-ago quarter as the release
# shows it; diluted shares (display) from the 10-Q filed with the release, Q4 from the 10-K's quarterly data (the release's adjusted net
# income table for Q4 2020: the FY2020 10-K has no quarterly data) ──
PR = f["prints"]
NEXT = {1: "Q2 print (late July)", 2: "Q3 print (late October)", 3: "Q4 and full-year print with the 10-K (February)",
        4: "Q1 print (late April)"}
TENQ = {(2018, 1): "0001558370-18-003287", (2018, 2): "0001558370-18-005735", (2018, 3): "0001558370-18-007843",
        (2019, 1): "0001558370-19-003261", (2019, 2): "0001558370-19-006289", (2019, 3): "0001558370-19-009890",
        (2020, 1): "0001164727-20-000132", (2020, 2): "0001164727-20-000178", (2020, 3): "0001164727-20-000228",
        (2021, 1): "0001164727-21-000114", (2021, 2): "0001164727-21-000194", (2021, 3): "0001164727-21-000235"}
REL = {(2017, 4): ("0001157523-18-000390", "Feb 22"), (2018, 1): ("0001157523-18-000815", "Apr 26"),
       (2018, 2): ("0001157523-18-001534", "Jul 26"), (2018, 3): ("0001157523-18-002139", "Oct 25"),
       (2018, 4): ("0001157523-19-000406", "Feb 21"), (2019, 1): ("0001157523-19-000886", "Apr 25"),
       (2019, 2): ("0001157523-19-001578", "Jul 25"), (2019, 3): ("0001157523-19-002190", "Nov 5"),
       (2019, 4): ("0001157523-20-000234", "Feb 20"), (2020, 1): ("0001157523-20-000647", "May 5"),
       (2020, 2): ("0001157523-20-001062", "Jul 30"), (2020, 3): ("0001157523-20-001374", "Oct 29"),
       (2020, 4): ("0001157523-21-000209", "Feb 18"), (2021, 1): ("0001157523-21-000532", "Apr 29"),
       (2021, 2): ("0001157523-21-000900", "Jul 22"), (2021, 3): ("0001157523-21-001269", "Oct 28")}
RP = {k: path(a, "EX-99.1__*rows.txt") for k, (a, _) in REL.items()}
RID = {}
STMT = r"^(NEWMONT (MINING |GOLDCORP )?CORPORATION ?)?(CONDENSED )?(CONSOLIDATED )?STATEMENTS OF (CONSOLIDATED )?(OPERATIONS|INCOME)"


def print_q(fy, q):
    acc, release = REL[(fy, q)]
    p = RP[(fy, q)]
    quarter = f"Q{q} {fy}"
    sid = src(acc, f"Newmont {quarter} results (8-K exhibit 99.1)",
              f"{quarter}: sales, consolidated gold ounces sold, costs applicable to sales per ounce, pre-tax income, diluted EPS from "
              "continuing operations, cash and debt")
    RID[(fy, q)] = sid
    day, when = pub(acc)
    rows = {}
    st = find(p, STMT, 0)
    rv, rows["rev"] = row(p, r"^Sales( \(\d+\))? \|", st)
    pv, rows["pt"] = row(p, r"^Income (\(loss\) )?before income and mining tax ?and other items \|", st)
    dl = find(p, r"^Diluted:( \(\d+\))?$", st)
    ev, t = row(p, r"^Continuing operations \|", dl)
    rows["eps"] = "Diluted: " + t
    bs = find(p, r"^(NEWMONT (MINING |GOLDCORP )?CORPORATION )?(CONDENSED )?CONSOLIDATED BALANCE SHEETS", st)
    cav, rows["cash"] = row(p, r"^Cash and cash equivalents \|", bs, n=2)
    li = find(p, r"^LIABILITIES$", bs)
    cl = find(p, r"^(Total current liabilities|Current liabilities) \|", li)
    cur = [i for i in range(li, cl) if re.match(r"^(Current portion of debt|Debt)( \(\d+\))? \|", lines(p)[i])]
    curv, rows["cur"] = cells(p, cur[0]) if cur else ([0.0, 0.0], "no current debt line among the current liabilities")
    ltdv, rows["ltd"] = row(p, r"^Debt( \(\d+\))? \|", cl, n=2)
    # ounces: consolidated gold ounces sold, the costs applicable to sales reconciliation's 'Gold sold (thousand ounces)' (the per-ounce
    # denominator, against the year-ago quarter: rule T's line, as from Q2 2014)
    ozv, rows["oz"] = row(p, r"^Gold sold \(thousand ounces\) \|", find(p, r"^Costs applicable to sales per ounce$", 0))
    casv, rows["cas"] = row(p, r"^Costs applicable to sales per ounce( ?\(\d+\))? \|", find(p, r"^Gold sold \(thousand ounces\) \|", 0))
    if q in (1, 2, 3):
        qp = path(TENQ[(fy, q)], "10-Q__*.rows.txt")
        ws = find(qp, r"(?i)^Weighted average common shares( \(millions\))?:", 0)
        shv, t = row(qp, r"^Diluted( \(\d+\))? \|", ws)
        rows["sh"] = "Weighted average common shares (millions): " + t
        sh_src = f"the Q{q} {fy} 10-Q (filed the same day)"
        assert pub(TENQ[(fy, q)])[0] == day, (quarter, "the 10-Q is public the same day as the release")
        CHECK.setdefault(qp, [])
    else:
        kp = KP[fy]
        assert SOURCES[KID[fy]]["published"] == day, (quarter, "the 10-K is public the same day as the release")
        qd = [i for i, x in enumerate(lines(kp)) if re.match(r"^(Quarterly Data|QUARTERLY DATA)$", x)]
        if qd:
            t_cur = find(kp, rf"^{fy}$", qd[-1])
            d1, dr1 = row(kp, r"^Diluted( \(\d+\))? \|", find(kp, r"^Weighted average common shares \(millions\):?$", t_cur), n=4)
            s1, r1 = row(kp, r"^Sales \|", t_cur, n=4)
            assert s1[3] == rv[0], (quarter, "the 10-K's Q4 sales equal the release's", s1, rv)
            shv, rows["sh"] = [d1[3]], f"FY{fy} 10-K quarterly data, {fy}: Weighted average common shares (millions) {dr1}"
            sh_src = f"the FY{fy} 10-K's quarterly data (filed the same day)"
            CHECK.setdefault(kp, [])
        else:                                              # the FY2020 10-K has no quarterly data: the release's own table
            i0 = find(p, r"^Management uses Adjusted net income", 0)
            wv, t = row(p, r"^Weighted average common shares \(millions\):( \(\d+\))? \|", i0, n=4)
            shv, rows["sh"] = [wv[1]], "Adjusted net income table: " + t
            sh_src = f"the {quarter} release's adjusted net income table (the FY{fy} 10-K has no quarterly data)"
    rev, rev0, pt, pt0 = rv[0], rv[1], pv[0], pv[1]
    oz, oz0, cas, cas0, e, e0 = ozv[0], ozv[1], casv[0], casv[1], ev[0], ev[1]
    m, m0 = pt / rev * 100, pt0 / rev0 * 100
    g = lambda a, b: round((b / a - 1) * 100 + 0.0, 1) if a > 0 else round((b - a) / abs(a) * 100 + 0.0, 1)   # noqa: E731
    d = {"quarter": quarter, "fy": fy, "q": q, "published": day, "release": release, "release_time": when, "source": sid,
         "raw": {"rev_m": rev, "rev_prior_m": rev0, "pretax_m": pt, "pretax_prior_m": pt0, "oz_k": oz, "oz_prior_k": oz0,
                 "cas": cas, "cas_prior": cas0},
         "rows": rows, "sales_b": round(rev / 1000, 3), "sales_pct": pct1(rev0, rev), "oz_pct": pct1(oz0, oz), "oz_basis": "sold",
         "cas_pct": pct1(cas0, cas), "pretax_margin": round(m + 0.0, 2), "pretax_margin_prior": round(m0 + 0.0, 2),
         "margin_bp": round((m - m0) * 100 + 0.0, 1), "eps_q": e, "eps_q_prior": e0, "eps_pct": g(e0, e) if e0 != 0 else None,
         "diluted_shares_m": shv[0], "shares_source": sh_src, "cash_b": round(cav[0] / 1000, 3),
         "debt_note": f"debt ${ltdv[0] + curv[0]:,.0f}M (long-term ${ltdv[0]:,.0f}M and current ${curv[0]:,.0f}M)",
         "rev_note": f"sales ${rev:,.0f}M vs ${rev0:,.0f}M a year earlier",
         "oz_note": f"consolidated gold ounces sold {oz:,.0f}K vs {oz0:,.0f}K",
         "cas_note": f"costs applicable to sales ${cas:,.0f} an ounce of gold vs ${cas0:,.0f}",
         "adj_note": None, "next_print": NEXT[q]}
    if q == 4:
        d["source_10k"] = KID[fy]
    d["eps_note"] = f"GAAP diluted EPS from continuing operations {fmt(e)} vs {fmt(e0)}" + (
        "; growth over the year-ago loss's absolute value (the CAT rule)" if e0 < 0 else
        "; the year-ago quarter's $0.00 gives no growth rate (n/m, the F rule)" if e0 == 0 else "")
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
for fy in (2017, 2018, 2019, 2020):
    p = RP[(fy, 4)]
    st = find(p, STMT, 0)
    sv, _ = row(p, r"^Sales( \(\d+\))? \|", st, n=4)
    dv, _ = row(p, r"^Continuing operations \|", find(p, r"^Diluted:( \(\d+\))?$", st), n=4)
    rev, eps, _, _ = (statements if fy == 2020 else item6)(KP[fy])
    assert (sv[2], dv[2]) == (rev[0], eps[0]), (fy, sv, dv, rev[0], eps[0])

# ── names (the CB and SPGI encoding: the name from the filing that states it until a later vintage carries it) ──
NM = [("0001104659-19-022663", "Newmont Goldcorp Corporation", "8-K__*rows.txt",
       "The Company amended its certificate of incorporation to change its name from Newmont Mining Corporation to Newmont Goldcorp Corporation"),
      ("0001104659-20-001511", "Newmont Corporation", "8-K__*rows.txt",
       "Effective January 6, 2020, Newmont Corporation, formerly known as Newmont Goldcorp Corporation, a Delaware corporation")]
for acc, name, pat, s_ in NM:
    p = path(acc, pat)
    sid = src(acc, f"Newmont 8-K of {ROWS[acc][2]} (the change of name to {name})", "the company name")
    f["company_names"].append({"published": SOURCES[sid]["published"], "name": name, "source": sid,
                               "note": f"'{quote(p, s_)}' ({SOURCES[sid]['filed']}); NYSE: NEM throughout"})

# ── dividends: each rate from the first filing that states it as declared (not 'subject to Board approval', not a plan; the $0.88
# special dividend of 2019 is not a rate) ──
DV = [((2017, 4), 0.14, "fourth quarter dividend declared raised to $0.14 per share"),
      ((2018, 1), 0.14, "a first quarter dividend declared of $0.14 per share"),
      ((2018, 2), 0.14, "a quarterly dividend declared of $0.14 per share"),
      ((2018, 3), 0.14, "a quarterly dividend declared of $0.14 per share"),
      ((2018, 4), 0.14, "declared dividends of $0.56 per share"),
      ((2019, 1), 0.14, "declared a first quarter dividend of $0.14 per share"),
      ((2019, 2), 0.14, "declared a second quarter dividend of $0.14 per share"),
      ((2019, 3), 0.14, "declared a third quarter dividend of $0.14 per share"),
      ((2020, 1), 0.25, "Declared first quarter dividend of $0.25 per share"),
      ((2020, 2), 0.25, "Declared second quarter dividend of $0.25 per share"),
      ((2020, 3), 0.40, "Declared third quarter dividend of $0.40 per share"),
      ((2020, 4), 0.55, "declared fourth quarter dividend of $0.55 per share"),
      ((2021, 1), 0.55, "Declared first quarter dividend of $0.55 per share"),
      ((2021, 2), 0.55, "Declared second quarter dividend of $0.55 per share"),
      ((2021, 3), 0.55, "Declared third quarter dividend of $0.55 per share")]
for k, q_, s_ in DV:
    f["dividends"].append({"published": SOURCES[RID[k]]["published"], "quarterly": q_, "source": RID[k],
                           "note": f"${q_:.3f}".rstrip("0").rstrip(".") + f" a quarter (${q_ * 4:.2f} a year): '{quote(RP[k], s_)}' "
                                   f"(the Q{k[1]} {k[0]} release" + ("; the year's four quarters" if k == (2018, 4) else "") + ")"})
quote(RP[(2019, 1)], "declared a one-time special dividend of $0.88 per share")             # not a rate (the LYB rule): text only
quote(RP[(2019, 4)], "Announced plan to increase annual divided by 79 percent to $1.00 per share; effective upon approval and declaration of Q1 2020 dividend in April 2020")

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


guide(2018, (2017, 4), "Q4 2017 release", "Attributable gold production is expected to be between 4.9 and 5.4 million ounces in 2018")
guide(2018, (2018, 1), "Q1 2018 release", "CAS remains unchanged at between $700 and $750 per ounce in 2018.")
guide(2018, (2018, 2), "Q2 2018 release", "CAS remains unchanged at between $700 and $750 per ounce in 2018.")
guide(2018, (2018, 3), "Q3 2018 release", "Outlook: Improved 2018 corporate-level AISC per ounce and narrowed production outlook")
guide(2019, "0001157523-18-002530", "8-K of 2018-12-06 (2019 and longer-term outlook)", "announced its 2019 outlook1 with attributable gold "
      "production guidance of 5.2 million ounces at AISC2 of $935 per ounce.")
guide(2019, (2018, 4), "Q4 2018 release", "Outlook: Attributable production at 5.2 million ounces, CAS at $710 per ounce and AISC at $935 per "
      "ounce, unchanged from December 2018")
guide(2019, (2019, 1), "Q1 2019 release", "Attributable gold production is expected to be 5.2 million ounces in 2019")
guide(2019, (2019, 2), "Q2 2019 release", "Outlook: 2019 attributable production at 6.5 million ounces, CAS at $735 per ounce and AISC at $975 per ounce")
guide(2019, (2019, 3), "Q3 2019 release", "Outlook: 2019 attributable production of 6.3 million ounces, CAS at $715 per ounce and AISC at $965 per ounce")
guide(2020, (2019, 4), "Q4 2019 release", "Stable production outlook of 6.4 million ounces in 2020")
guide(2020, (2020, 1), "Q1 2020 release", "On March 23, the Company withdrew its full-year 2020 guidance")
guide(2020, (2020, 2), "Q2 2020 release", "Newmont's 2020 attributable gold production remains at approximately 6.0 million ounces and the "
      "Company expects to produce approximately 1.0 million gold equivalent ounces from co-products.")
guide(2020, (2020, 3), "Q3 2020 release", "Newmont's 2020 attributable gold production is unchanged at approximately 6.0 million ounces and "
      "the Company expects to produce approximately 1.0 million gold equivalent ounces from co-products.")
guide(2021, (2020, 4), "Q4 2020 release", "Announced 2021 outlook of 6.5 million ounces for 2021")
guide(2021, (2021, 1), "Q1 2021 release", "Full-year production continues to be back-half weighted, in line with 2021 guidance")
guide(2021, (2021, 2), "Q2 2021 release", "Full-year results continue to be back-half weighted, in line with guidance ranges")
guide(2021, (2021, 3), "Q3 2021 release", "Updated full-year guidance of 6.0 million ounces of attributable gold production, $790 per ounce of "
      "CAS and $1,050 per ounce of AISC")

# ── assemble: the earlier facts unchanged ──
for k in ("sources", "history_vintages", "prints", "guides", "dividends", "company_names"):
    o = old[k]
    n = f[k]
    if isinstance(o, dict):
        assert all(n[x] == o[x] for x in o), k
    else:
        assert n[:len(o)] == o, k
for x in ("rule_t", "listings", "events", "splits", "distributions", "eps_guides"):
    assert f[x] == old[x], x
assert all(s["published"] <= CUT for s in SOURCES.values())
f["sources"] = dict(sorted(SOURCES.items(), key=lambda kv: int(kv[0][2:])))
f["_doc"] = old["_doc"].replace("gen_nem.py (2008-2009), gen_nem_1013.py (2010-2013) and gen_nem_1417.py (2014-2017) from the filings",
                                "gen_nem.py (2008-2009), gen_nem_1013.py (2010-2013), gen_nem_1417.py (2014-2017) and gen_nem_1821.py "
                                "(2018-2021) from the filings")
assert f["_doc"] != old["_doc"]
with open(FACTS, "w", encoding="utf-8") as fh:
    json.dump(f, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_nem_1821.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump({k: v for k, v in CHECK.items() if v}, fh, ensure_ascii=False, indent=1)
print(f"{FACTS}: {len(V)} vintages, {len(PR)} prints, {len(G)} guides, {len(f['dividends'])} dividends, {len(SOURCES)} sources; "
      f"{sum(len(v) for v in CHECK.values())} quotes in {ck}")
for p in PR[-16:]:
    print(p["quarter"], p["published"], p["release_time"][-40:], p["sales_pct"], p["oz_pct"], p["cas_pct"], p["eps_q"],
          p["eps_q_prior"], p["eps_pct"], p["margin_bp"], p["diluted_shares_m"])
for v in V[-5:]:
    print(v["published"], v["fy_label"], v["kind"], v["eps_normalized"], sorted(v["eps_excluded"]), v["prev_fy_margin"], v["tax_rate"],
          v["prev_fy_oz_k"], v["prev_fy_oz_pct"], v["prev_fy_cas"], v["groups"], v["fcf_b"], v["cash_b"])
