#!/usr/bin/env python3
"""Extend retro/facts/NEM.json with 2022-2026 (filings accepted 2022-01-01 to 2026-11-27), asserting that every earlier fact is
unchanged. Same discipline as gen_nem_1821.py: each raw figure is read from its own row by label (the row text is kept in the fact), every
rate, margin and change is computed, every quote is asserted present in its own filing word for word, and a verbatim checklist is
written. Only filings accepted on or before 2026-11-27 are read. The downloads (keep them outside the repo, e.g. the scratchpad):

    python3 retro/tools/edgar.py index 1164727 <dir>
    python3 retro/tools/edgar.py fetch 1164727 <dir> --from 2022-01-01 --to 2026-11-28 --forms 8-K 8-K/A 10-K 10-K/A 10-Q

    python3 -I retro/generators/nem/gen_nem_2226.py --filings <dir> [--facts-in <2008-2021 sheet>] [--out retro/facts/NEM.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_nem_2226.json

--facts-in is the 2008-2021 sheet gen_nem_1821.py writes (default: retro/facts/NEM.json, which must then hold 2008-2021 only).
Two release layouts are read: to Q4 2023 the statements give the quarter, the year-ago quarter and (Q2-Q4) the two year-to-dates; from
Q1 2024 they give the prior year's four quarters and its year, then the current year's quarters and its year to date (the balance sheets
the quarter-ends), so each figure is read from its column by the quarter's position, asserted against the header. From the Q4 2025
release the costs applicable to sales per ounce reconciliation gives only the by-product figure, so the co-product figure (the series'
line) is read from the release's 'Summary of Results' table, asserted equal to the earlier releases' reconciliations where they overlap.
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
START, CUT = "2022-01-01", "2026-11-27"
CIK = 1164727
ROWS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("NEM")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
FACTS = A.out or os.path.join(REPO, "retro", "facts", "NEM.json")
old = json.load(open(A.facts_in or os.path.join(REPO, "retro", "facts", "NEM.json"), encoding="utf-8"))
assert all(s["published"] <= "2021-12-31" for s in old["sources"].values()), "--facts-in must be the 2008-2021 sheet"
f = copy.deepcopy(old)
CHECK = {}
TEXT = {}
ZW = "​"
norm = lambda s: re.sub(r"\s+", " ", s.replace(ZW, " ")).strip()      # noqa: E731


def path(acc, pat):
    hits = glob.glob(os.path.join(SP, "*", acc, pat))
    assert len(hits) == 1, (acc, pat, hits)
    return hits[0]


def lines(p):
    """The rows of a converted filing, with the zero-width cells dropped."""
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
NEXT_ID = [98]
assert max(int(k[2:]) for k in SOURCES) == 97


def src(acc, title, supports):
    sid = f"NM{NEXT_ID[0]}"
    NEXT_ID[0] += 1
    day, when = pub(acc)
    SOURCES[sid] = {"published": day, "filed": when, "title": title,
                    "url": f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc.replace('-', '')}/{acc}.txt", "supports": supports}
    return sid


pct = lambda a, b: round((b / a - 1) * 100 + 0.0, 2)          # noqa: E731
pct1 = lambda a, b: round((b / a - 1) * 100 + 0.0, 1)         # noqa: E731
fmt = lambda x: f"${x:.2f}" if x >= 0 else f"$({-x:.2f})"      # noqa: E731

# ── the history vintages: the FY2021-FY2025 10-Ks, each reserving Item 6, so each takes its three years from the statements of
# operations (the FY2020 and ACN FY21 rule) and keeps the earlier years as the previous vintage holds them; each holding the ten fiscal
# years to the latest one. The 10-K/A of 2022-07-28 re-files only Item 8 to amend NGM's auditor's report ("there have been no changes to
# the Company’s financial statements"), and the 8-K of 2023-07-20 recasts the FY2022 10-K's Items 1, 2, 7 and 8 for the new segments with
# the statements of operations unchanged (asserted below): neither changes a figure the models read, so neither is a vintage ───────────
K = {2021: ("0001164727-22-000007", "10-K__nem-20211231.rows.txt"), 2022: ("0001164727-23-000011", "10-K__nem-20221231.rows.txt"),
     2023: ("0001164727-24-000016", "10-K__nem-20231231.rows.txt"), 2024: ("0001164727-25-000011", "10-K__nem-20241231.rows.txt"),
     2025: ("0001164727-26-000010", "10-K__nem-20251231.rows.txt")}
KP = {y: path(a, fn) for y, (a, fn) in K.items()}
KID = {}
for y, (a, _) in K.items():
    assert any(re.match(r"^ITEM 6\.( \|)? RESERVED", x) for x in lines(KP[y])), (y, "Item 6 is reserved")
    KID[y] = src(a, f"Newmont FY{y} 10-K", f"history vintage FY{y} (the statements, as Item 6 is reserved; the results and highlights "
                 "table); the 'why'")
LEAD = ("Newmont is the world’s leading gold company",)
WHY2 = {y: ("Our business is dependent on the prices of gold, silver, copper, zinc and lead, which fluctuate on a daily basis and are "
            "affected by numerous factors beyond our control.") if y <= 2022 else
           ("Our business is dependent on the prices of gold, copper, silver, lead and zinc, which fluctuate on a daily basis and are "
            "affected by numerous factors beyond our control.") for y in K}
WHY_RISK = {y: ("A substantial or extended decline in gold, silver, copper, zinc or lead prices would have a material adverse effect on us."
                if y <= 2022 else
                "A substantial or extended decline in gold, copper, silver, lead or zinc prices would have a material adverse effect on us.")
            for y in K}
CYCL = "The metals markets are cyclical"
CLIMATE = {y: ("Policy and regulatory risk related to actual and proposed changes in climate- and water-related laws, regulations and "
               "taxes developed to regulate the transition to a low-carbon economy may result in increased costs for our operations, "
               "venture partners and our suppliers, including increased energy, capital equipment, environmental monitoring and reporting "
               "and other costs to comply with such regulations.") for y in K}
CLIMATE[2025] = CLIMATE[2024].replace("climate- and water-related", "climate-, nature-, and water-related")
CLIMATE[2023] = CLIMATE[2023].replace(" such regulations.", "")       # the FY2023 10-K breaks the sentence at a page end
CRYPTO = ("Changing investor or consumer sentiment, including in connection with transition to a low-carbon economy, investor interest in "
          "crypto currencies and other investment alternatives")
AI = {2023: "new technology that could result in greater operational efficiency, such as our use of artificial intelligence, fleet "
            "electrification, and autonomous vehicles",
      2024: "the adoption of emerging technologies such as artificial intelligence (AI), automation, and cloud-based platforms",
      2025: "the adoption of emerging technologies such as artificial intelligence (AI), automation, and cloud-based platforms"}


def why(y, p=None):
    """The 'why' and the kind, as gen_nem_1821.py: the lead sentence, the price-dependence sentence and the gold-price risk factor, and
    the business section's 'The metals markets are cyclical' (CYCLICAL, the CB rule), asserted in every vintage."""
    p = p or KP[y]
    txt = " ".join(lines(p))
    lead = [x for x in lines(p) if x.startswith(LEAD)][0].split(". ")[0].rstrip(".") + "."
    q = [quote(p, lead), quote(p, WHY2[y]), quote(p, WHY_RISK[y])]
    assert CYCL in txt, (y, "cyclical")
    q.append(quote(p, CYCL))
    return ("CYCLICAL", " ".join(f"'{x}'" for x in q) + f" (the FY{y} 10-K's own words; it calls the metals markets it sells into cyclical, "
            "so CYCLICAL, the CB rule)")


def statements(p):
    """Item 6 is reserved: the consolidated statements of operations' three years (the ACN FY21 and LLY rule); the regular dividends
    declared from the results and highlights table."""
    st = find(p, r"^CONSOLIDATED STATEMENTS OF OPERATIONS$", find(p, r"^ITEM 8\.", 0))
    rev, rrow = row(p, r"^Sales( \(Note \d+\))? \|", st, n=3)
    dl = find(p, r"^Diluted:( \(\d+\))?$", st)
    eps, erow = row(p, r"^Continuing operations \|", dl, n=3)
    div, drow = row(p, r"^Regular cash dividends declared per common share \|", find(p, r"^Financial Results:$", 0), n=3)
    return rev, eps, div, ["Statements of operations: " + rrow, "Diluted: " + erow, "Results and highlights: " + drow]


V = f["history_vintages"]
prev = V[-1]
assert prev["fy_label"] == "FY20" and set(prev["eps_excluded"]) == {"2011", "2013", "2015", "2016", "2017", "2018", "2019"}


def vintage(y, p, sid, title, excl_new, drop_before, kind_why, company, business_line, climate):
    """One vintage: the statements' three years and the results and highlights table's, excluded years (texts by year) carried and
    added; the ten fiscal years to the latest one."""
    global prev
    kind, why_text = kind_why
    rev, eps, div, rows = statements(p)
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
        assert e.get(yy, v_e) == v_e, (y, yy, e.get(yy), v_e, "a restated year needs its note")
        e[yy], es[yy] = v_e, sid
    st = find(p, r"^CONSOLIDATED STATEMENTS OF OPERATIONS$", find(p, r"^ITEM 8\.", 0))
    dil = find(p, r"^Diluted \| [\d,]+ \| [\d,]+ \| [\d,]+$", st)
    sh, shrow = cells(p, dil)
    s, ss = dict(prev["diluted_shares_m"]), dict(prev["shares_sources"])
    for k, v in zip(years[:3], sh):
        s[k], ss[k] = v, sid
    for d in (e, es, r, rs, s, ss, excl):                   # the ten fiscal years to the latest one: earlier years leave the history
        for k in [k for k in d if int(k) < drop_before]:
            del d[k]
    yrs = sorted(set(e) | set(excl))
    assert int(yrs[-1]) == y and int(yrs[0]) == drop_before, (y, yrs)
    pt, ptrow = row(p, r"^Income \(loss\) before income and mining tax and other items \|", st, n=3)
    tx, txrow = row(p, r"^Income and mining tax (benefit \(expense\)|expense)( \(Note \d+\))? \|(?!.*%)", st, n=3)
    cx, cxrow = row(p, r"^Additions to property, plant and mine development \|", st, n=3)
    ca, carow = row(p, r"^Cash and cash equivalents \|", find(p, r"^CONSOLIDATED BALANCE SHEETS$", st), n=2)
    fr = find(p, r"^Financial Results:$", 0)              # the results and highlights table (financial, then operating results)
    gold, grow = row(p, r"^Gold \|", fr, n=3)
    cf, cfrow = row(p, r"^Net cash provided by \(used in\) operating activities of continuing operations \|", fr, n=3)
    orr = find(p, r"^Operating Results:$", 0)
    oz, ozrow = row(p, r"^Sold \|", find(p, r"^Consolidated gold ounces \(thousands\):$", orr), n=3)
    cs, csrow = row(p, r"^Gold \(per ounce\) \|", find(p, r"^Consolidated costs applicable to sales:", orr), n=3)
    assert find(p, r"^Consolidated costs applicable to sales:", orr) < find(p, r"^All-in sustaining costs:", orr)
    lab = f"FY{y % 100:02d}"
    doc = title.replace("Newmont ", "")
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
         "dividend_annual": div[0], "dividend_note": f"regular dividends declared per common share ${div[0]:.3f} in FY{y} (the results and "
                                                      "highlights table); the quarterly rate in force is the latest one a filing states",
         "cash_b": ca[0] / 1000, "fcf_b": round((cf[0] + cx[0]) / 1000, 3), "fcf_label": lab,
         "fcf_note": f"net cash provided by (used in) operating activities of continuing operations ${cf[0]:,.0f}M less additions to "
                     f"property, plant and mine development ${-cx[0]:,.0f}M ({doc})",
         "cash_return_text": f"dividends declared ${div[0]:.2f} a share in FY{y} (regular); share repurchases text only",
         "groups": [["Gold", gold[0] / 1000, pct1(gold[1], gold[0])],
                    ["Other metals", round((rev[0] - gold[0]) / 1000, 3), pct1(rev[1] - gold[1], rev[0] - gold[0])]],
         "groups_basis": f"{lab} sales by metal ({doc}; other metals as sales less gold)", "why": why_text,
         "climate_words": climate,
         "crypto_words": f"'{quote(p, CRYPTO)}' (the {doc}'s list of factors that move the gold price)"}
    if y in AI:
        v["ai_words"] = f"'{quote(p, AI[y])}' (the {doc}'s cybersecurity risk words)"
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


GAP = ("excluded as the latest year, its own days leave the P/E window, and it stays a gap", "excluded, a gap")


def rec(acc, cont_lab=r"^Net income \(loss\) attributable to Newmont stockholders from continuing operations( \(\d+\))? \|"):
    """A Q4 release's adjusted net income reconciliation for the year: every listed item (each row between the continuing-operations
    line and 'Adjusted net income (loss)'), the year's column (the fourth of six, with per-share columns)."""
    p = path(acc, "EX-99.1__*rows.txt")
    i0 = find(p, r"(?i)^Management uses Adjusted net income", 0)
    c0 = find(p, cont_lab, i0)
    c1 = find(p, r"^Adjusted net income \(loss\)( \(\d+\))? \|", c0)
    cont, crow = cells(p, c0)
    assert len(cont) == 6, (acc, crow)
    items, rows_ = {}, [crow]
    for i in range(c0 + 1, c1):
        vv, t = cells(p, i)
        items[re.sub(r"\s*\(\d+\)$", "", t.split(" | ")[0])] = vv[3]
        rows_.append(t)
    adj, arow = cells(p, c1)
    rows_.append(arow)
    assert round(cont[3] + sum(items.values())) == adj[3], (acc, cont[3], sum(items.values()), adj[3])
    return p, cont[3], items, adj[3], adj[5], rows_


def items_text(it):
    keep = ("Nevada", "Goldcorp", "Emigrant", "La Quinua", "Tax Cuts", "COVID", "Newcrest")
    return ", ".join(f"{k[:2].lower() + k[2:] if k.startswith('(') else k[0].lower() + k[1:] if not k.startswith(keep) else k} "
                     f"{'$' if v >= 0 else '$('}{abs(v):,.0f}{'M' if v >= 0 else ')M'}" for k, v in it.items() if v != 0)


RECUR = ("impairments, asset sales, changes in the fair value of investments, reclamation charges, tax items: the PEP 2008 core rule")
COMPANY = "Newmont Corporation"
BL0 = "gold producer with copper, silver, lead and zinc co-products (Nevada Gold Mines, 38.5%, from 2019-07-01)"
BL1 = "gold producer with copper, silver, lead and zinc co-products (Newcrest acquired on 2023-11-06; Nevada Gold Mines, 38.5%)"
CLIM = lambda y: f"'{quote(KP[y], CLIMATE[y])}{'...' if y == 2023 else ''}' (the FY{y} 10-K's risk factor)"   # noqa: E731

# FY2021: the AAPL FY2002 test (the FY2011, FY2015 and FY2018 encoding). The Q4 2021 release's listed items in continuing operations,
# every one summed with the tax effect and tax lines (recurring ones included), exceed the year's income from continuing operations
# attributable to Newmont, so reported EPS ($1.39) is under half the year's EPS without them; the adjusted net income also removes items
# that recur, so no figure excludes only the one-offs: excluded as the latest year, then a gap.
P21, c21, it21, a21, ae21, rows21 = rec("0001157523-22-000249")
items21 = sum(it21.values())
assert c21 == 1109 and items21 > c21 and a21 == 2371 and ae21 == 2.96, (c21, items21, a21, ae21)
EXCL21 = ("the AAPL FY2002 test (the FY2011, FY2015 and FY2018 encoding): the Q4 2021 release's listed items in continuing operations ("
          + items_text(it21) + f"; ${items21:,.0f}M net after the tax lines) exceed the year's ${c21:,.0f}M of income from continuing "
          f"operations attributable to Newmont, so reported EPS ($1.39 diluted, FY2021 10-K) is under half the year's EPS without them; the "
          f"release's adjusted net income (${a21:,.0f}M, ${ae21:.2f} a diluted share) also removes items that recur ({RECUR}), so no figure "
          f"excludes only the one-offs; {GAP[0]}")
v21, eps21, _, _ = vintage(2021, KP[2021], KID[2021], "Newmont FY2021 10-K", {"2021": EXCL21}, 2012, why(2021), COMPANY, BL0, CLIM(2021))
v21["rows"] += rows21
assert eps21 == [1.39, 3.31, 3.91], eps21
# FY2022: a loss (the impairments and the reclamation charges at Yanacocha)
P22, c22, it22, a22, ae22, rows22 = rec("0001157523-23-000340")
assert (c22, a22, ae22) == (-459, 1468, 1.85), (c22, a22, ae22)
ADJ = lambda q, a, e: (f"the {q} release's adjusted net income (${a:,.0f}M, ${e:.2f} a diluted share) also removes items that recur "   # noqa: E731
                       f"({RECUR})")
LOSS22 = lambda doc: loss_text(-0.58, doc, ADJ("Q4 2022", a22, ae22))                                                  # noqa: E731
v22, eps22, _, _ = vintage(2022, KP[2022], KID[2022], "Newmont FY2022 10-K",
                           {"2021": EXCL21.replace(GAP[0], GAP[1]), "2022": LOSS22("FY2022 10-K")}, 2013, why(2022), COMPANY, BL0,
                           CLIM(2022))
v22["rows"] += rows22
assert eps22 == [-0.58, 1.39, 3.31], eps22
# the 8-K of 2023-07-20 recasting the FY2022 10-K for the new segments: its statements of operations are the FY2022 10-K's (asserted)
RC_ACC = "0001164727-23-000035"
RCP = path(RC_ACC, "EX-99.1__*rows.txt")
assert row(RCP, r"^Sales( \(Note \d+\))? \|", 0, n=3)[0] == statements(KP[2022])[0]
assert row(RCP, r"^Continuing operations \|", find(RCP, r"^Diluted:( \(\d+\))?$", 0), n=3)[0] == eps22
quote(RCP, "in order to give effect to a change in segment reporting")
# FY2023: a loss (the impairments, the reclamation charges and the Newcrest transaction costs). The Q4 2023 release (2024-02-22) comes a
# week before the 10-K (2024-02-29) and is preliminary ("subject to completion of our annual audit procedures"): its year, $(2.97), is
# the print's full-year actual until the 10-K, which restates it to $(3.00) ('fy_actual' below)
P23, c23, it23, a23, ae23, rows23 = rec("0001164727-24-000006", r"^Net income \(loss\) attributable to Newmont stockholders from continuing operations( \(\d+\))? \|")
assert (c23, a23, ae23) == (-2501, 1358, 1.61), (c23, a23, ae23)
hl23 = row(KP[2023], r"^Adjusted net income \(loss\) per share, diluted( \(\d+\))? \|", find(KP[2023], r"^Financial Results:$", 0), n=3)[0]
an23 = row(KP[2023], r"^Adjusted net income \(loss\)( \(\d+\))? \|", find(KP[2023], r"^Financial Results:$", 0), n=3)[0]
assert (an23[0], hl23[0]) == (1324, 1.57), (an23, hl23)
ADJ23K = (f"the FY2023 10-K's adjusted net income (${an23[0]:,.0f}M, ${hl23[0]:.2f} a diluted share; the Q4 2023 release's ${a23:,.0f}M and "
          f"${ae23:.2f}) also removes items that recur ({RECUR})")
LOSS23 = lambda doc: loss_text(-3.00, doc, ADJ23K)                                                                       # noqa: E731
v23, eps23, _, _ = vintage(2023, KP[2023], KID[2023], "Newmont FY2023 10-K",
                           {"2022": LOSS22("FY2022 10-K").replace(GAP[0], GAP[1]), "2023": LOSS23("FY2023 10-K")}, 2014, why(2023),
                           COMPANY, BL1, CLIM(2023))
v23["rows"] += rows23
assert eps23 == [-3.00, -0.58, 1.39], eps23
# FY2024: GAAP $2.86 kept. The Q4 2024 release's listed items net to charges of $711M against $3,280M of income, under half; no benefit
# outweighs the year (the mirror is not met)
P24, c24, it24, a24, ae24, rows24 = rec("0001164727-25-000008")
items24 = sum(it24.values())
assert c24 == 3280 and a24 == 3991 and 0 < items24 < c24, (c24, items24, a24)
v24, eps24, _, _ = vintage(2024, KP[2024], KID[2024], "Newmont FY2024 10-K", {"2023": LOSS23("FY2023 10-K").replace(GAP[0], GAP[1])}, 2015,
                           why(2024), COMPANY, BL1, CLIM(2024))
v24["rows"] += rows24
assert eps24 == [2.86, -3.00, -0.58], eps24
KEPT24 = (f"FY2024 kept at GAAP $2.86: the Q4 2024 release's listed items in continuing operations ({items_text(it24)}; ${items24:,.0f}M "
          f"net after the tax lines) are under the year's ${c24:,.0f}M of income from continuing operations attributable to Newmont, so "
          "neither the AAPL FY2002 test nor its mirror is met")
v24["normalization"] += "; " + KEPT24
# FY2025: GAAP $6.39 kept (no discontinued operations in 2025: the reconciliation starts from net income attributable to Newmont)
P25, c25, it25, a25, ae25, rows25 = rec("0001164727-26-000009", r"^Net income \(loss\) attributable to Newmont stockholders \|")
items25 = sum(it25.values())
assert c25 == 7085 and a25 == 7634 and 0 < items25 < c25, (c25, items25, a25)
v25, eps25, _, _ = vintage(2025, KP[2025], KID[2025], "Newmont FY2025 10-K", {}, 2016, why(2025), COMPANY, BL1, CLIM(2025))
v25["rows"] += rows25
assert eps25 == [6.39, 2.86, -3.00], eps25
v25["normalization"] += "; " + KEPT24 + "; " + (
    f"FY2025 kept at GAAP $6.39: the Q4 2025 release's listed items ({items_text(it25)}; ${items25:,.0f}M net after the tax lines) are "
    f"under the year's ${c25:,.0f}M of income attributable to Newmont (no discontinued operations), so neither test is met")

# ── the prints Q4 2021 - Q3 2026: the earnings releases (8-K exhibit 99.1), each figure against the year-ago quarter as the release
# shows it; diluted shares from the release's own statement of operations ──
PR = f["prints"]
NEXT = {1: "Q2 print (late July)", 2: "Q3 print (late October)", 3: "Q4 and full-year print (February)", 4: "Q1 print (late April)"}
REL = {(2021, 4): "0001157523-22-000249", (2022, 1): "0001157523-22-000461", (2022, 2): "0001157523-22-000888",
       (2022, 3): "0001157523-22-001452", (2022, 4): "0001157523-23-000340", (2023, 1): "0001157523-23-000631",
       (2023, 2): "0001157523-23-001113", (2023, 3): "0001157523-23-001555", (2023, 4): "0001164727-24-000006",
       (2024, 1): "0001164727-24-000025", (2024, 2): "0001164727-24-000035", (2024, 3): "0001164727-24-000057",
       (2024, 4): "0001164727-25-000008", (2025, 1): "0001164727-25-000018", (2025, 2): "0001164727-25-000033",
       (2025, 3): "0001164727-25-000044", (2025, 4): "0001164727-26-000009", (2026, 1): "0001164727-26-000017",
       (2026, 2): "0001164727-26-000034", (2026, 3): "0001164727-26-000041"}
RP = {k: path(a, "EX-99.1__*rows.txt") for k, a in REL.items()}
RID = {}
STMT = r"^(NEWMONT CORPORATION( \| | )?)?(CONDENSED )?(CONSOLIDATED )?STATEMENTS OF (CONSOLIDATED )?(OPERATIONS|INCOME)\b(?! and)"
BS = r"^(NEWMONT CORPORATION( \| | )?)?(CONDENSED )?CONSOLIDATED BALANCE SHEETS\b"
MON = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}


def layout(p, at, q, fy):
    """('old', None) for the quarter | year-ago (| year-to-dates) layout; ('multi', header) for the quarterly-column layout (from Q1
    2024), the header asserted: the prior year's Q1..Q4 and FY, then the current year's quarters, or the quarter-ends of both years."""
    L = lines(p)
    for j in range(at + 1, at + 5):
        if L[j].startswith(("Q1 | Q2 | Q3 | Q4 | FY | Q1", "MAR | JUN | SEP | DEC | MAR")):
            yrs = re.findall(r"\b(20\d\d)\b", L[j - 1])
            assert yrs == [str(fy - 1), str(fy)], (os.path.basename(p), L[j - 1], fy)
            return "multi", L[j - 1] + " / " + L[j]
    return "old", None


def ops(p, st, pat, q, fy, after=None, n_old=None):
    """A statement-of-operations row: (current, year-ago, row text)."""
    kind, hdr = layout(p, st, q, fy)
    v, t = row(p, pat, st if after is None else after)
    if kind == "multi":
        if len(v) == 5 + q + 2 and t.endswith("%"):             # the summary table's year-on-year 'Change' column (Q4 2025)
            v = v[:-1]
        assert len(v) == 5 + q + 1, (os.path.basename(p), t, q)
        return v[5 + q - 1], v[q - 1], t + f" [columns: {hdr}]"
    assert n_old is None or len(v) == n_old, (os.path.basename(p), t)
    return v[0], v[1], t


def bal(p, b, pat, q, fy, after=None, before=None):
    """A balance-sheet row's quarter-end value (the current column)."""
    kind, hdr = layout(p, b, q, fy)
    v, t = row(p, pat, b if after is None else after, before=before)
    if kind == "multi":
        assert len(v) == 4 + q, (os.path.basename(p), t, q)
        return v[4 + q - 1], t + f" [columns: {hdr}]"
    assert len(v) == 2, (os.path.basename(p), t)
    return v[0], t


def print_q(fy, q):
    acc = REL[(fy, q)]
    p = RP[(fy, q)]
    quarter = f"Q{q} {fy}"
    sid = src(acc, f"Newmont {quarter} results (8-K exhibit 99.1)",
              f"{quarter}: sales, consolidated gold ounces sold, costs applicable to sales per ounce, pre-tax income, diluted EPS from "
              "continuing operations, diluted shares, cash and debt")
    RID[(fy, q)] = sid
    day, when = pub(acc)
    t_acc = dt.datetime.fromisoformat(ROWS[acc][1].replace("Z", "+00:00")).astimezone(ET)
    release = f"{t_acc:%b} {t_acc.day}"
    rows = {}
    st = find(p, STMT, 0)
    rev, rev0, rows["rev"] = ops(p, st, r"^Sales( \(\d+\))? \|", q, fy)
    pt, pt0, rows["pt"] = ops(p, st, r"^Income (\(loss\) )?before income and mining tax ?and other items \|", q, fy)
    bs = find(p, BS, st)
    dl = [i for i in range(st, bs) if re.match(r"^Diluted:( \(\d+\))?$", lines(p)[i])]
    if dl:                                                         # diluted EPS from continuing operations
        e, e0, t = ops(p, st, r"^Continuing operations \|", q, fy, after=dl[0])
        rows["eps"] = "Diluted: " + t
        eps_basis = "from continuing operations"
    else:                                                          # 2026: no discontinued operations, one diluted EPS line
        ps = find(p, r"^Net income \(loss\) attributable to Newmont stockholders per common share:$", st, before=bs)
        assert not any(re.match(r"^Continuing operations \|", lines(p)[i]) for i in range(st, bs)), (quarter, "no continuing line")
        e, e0, t = ops(p, st, r"^Diluted \|", q, fy, after=ps)
        rows["eps"] = "Net income (loss) attributable to Newmont stockholders per common share: " + t
        eps_basis = "(no discontinued operations: the release's one diluted EPS line)"
    ws = find(p, r"^Weighted average common shares \(millions\):$", st, before=bs)
    sh, _, t = ops(p, st, r"^Diluted \|", q, fy, after=ws)
    rows["sh"] = "Weighted average common shares (millions): " + t
    cav, rows["cash"] = bal(p, bs, r"^Cash and cash equivalents \|", q, fy)
    li = find(p, r"^LIABILITIES$", bs)
    cl = find(p, r"^(Total current liabilities|Current liabilities) \|", li)
    cur = [i for i in range(li, cl) if re.match(r"^(Current portion of debt|Debt)( \(\d+\))? \|", lines(p)[i])]
    if cur:
        curv, rows["cur"] = bal(p, bs, r"^(Current portion of debt|Debt)( \(\d+\))? \|", q, fy, after=cur[0], before=cl)
    else:
        curv, rows["cur"] = 0.0, "no current debt line among the current liabilities"
    ltdv, rows["ltd"] = bal(p, bs, r"^Debt( \(\d+\))? \|", q, fy, after=cl)
    # ounces and costs applicable to sales per ounce (co-product): the reconciliation's 'Gold sold (thousand ounces)' and the per-ounce
    # row under it, against the year-ago quarter; from the Q4 2025 release the reconciliation gives the by-product figure only, so the
    # co-product figure comes from the 'Summary of Results' table ('Gold Co-Product CAS ($/oz)', its columns by quarter) and the ounces
    # from the 'Total Newmont' by-product reconciliation's 'Gold sold (thousand ounces)' (the same consolidated ounces)
    L = lines(p)
    pairs = [i for i in range(len(L) - 1) if re.match(r"^Gold sold \(thousand ounces\) \|", L[i])
             and re.match(r"^Costs applicable to sales per ounce( ?\(\d+\))? \|", L[i + 1])]
    if pairs:
        ozv, rows["oz"] = cells(p, pairs[0])
        casv, rows["cas"] = cells(p, pairs[0] + 1)
        oz, oz0, cas, cas0 = ozv[0], ozv[1], casv[0], casv[1]
        cas_src = "the costs applicable to sales per ounce reconciliation"
    else:
        tn = find(p, r"^Total Newmont Consolidated Gold By-product Unit Costs$", 0)
        ozv, rows["oz"] = row(p, r"^Gold sold \(thousand ounces\) \|", tn)
        oz, oz0 = ozv[0], ozv[1]
        sm = find(p, r"^Summary of Results$", 0)
        cas, cas0, rows["cas"] = ops(p, sm, r"^Gold Co-Product CAS \(\$/oz\)", q, fy)
        cas_src = "the 'Summary of Results' table's co-product line (the reconciliation gives the by-product figure only)"
        byp = row(p, r"^Total Gold CAS per ounce \(by-product\)( ?\(\d+\))+ \|", tn)
        rows["cas_byproduct"] = byp[1]
        ago = [x for x in PR if (x["fy"], x["q"]) == (fy - 1, q)]
        if ago and ago[0].get("cas_source", "").startswith("the costs applicable"):     # the overlap: the same co-product figure
            assert ago[0]["raw"]["cas"] == cas0, (quarter, ago[0]["raw"]["cas"], cas0)
    assert ROWS[acc][2] == "8-K"
    m, m0 = pt / rev * 100, pt0 / rev0 * 100
    g = lambda a, b: round((b / a - 1) * 100 + 0.0, 1) if a > 0 else round((b - a) / abs(a) * 100 + 0.0, 1)   # noqa: E731
    d = {"quarter": quarter, "fy": fy, "q": q, "published": day, "release": release, "release_time": when, "source": sid,
         "raw": {"rev_m": rev, "rev_prior_m": rev0, "pretax_m": pt, "pretax_prior_m": pt0, "oz_k": oz, "oz_prior_k": oz0,
                 "cas": cas, "cas_prior": cas0},
         "rows": rows, "sales_b": round(rev / 1000, 3), "sales_pct": pct1(rev0, rev), "oz_pct": pct1(oz0, oz), "oz_basis": "sold",
         "cas_pct": pct1(cas0, cas), "pretax_margin": round(m + 0.0, 2), "pretax_margin_prior": round(m0 + 0.0, 2),
         "margin_bp": round((m - m0) * 100 + 0.0, 1), "eps_q": e, "eps_q_prior": e0, "eps_pct": g(e0, e) if e0 != 0 else None,
         "diluted_shares_m": sh, "shares_source": f"the {quarter} release's statement of operations",
         "cas_source": cas_src, "cash_b": round(cav / 1000, 3),
         "debt_note": f"debt ${ltdv + curv:,.0f}M (long-term ${ltdv:,.0f}M and current ${curv:,.0f}M)",
         "rev_note": f"sales ${rev:,.0f}M vs ${rev0:,.0f}M a year earlier",
         "oz_note": f"consolidated gold ounces sold {oz:,.0f}K vs {oz0:,.0f}K",
         "cas_note": f"costs applicable to sales ${cas:,.0f} an ounce of gold vs ${cas0:,.0f}" + (
             "" if pairs else " (co-product, the release's summary table)"),
         "adj_note": None, "next_print": NEXT[q]}
    d["eps_note"] = f"GAAP diluted EPS {eps_basis} {fmt(e)} vs {fmt(e0)}" + (
        "; growth over the year-ago loss's absolute value (the CAT rule)" if e0 < 0 else
        "; the year-ago quarter's $0.00 gives no growth rate (n/m, the F rule)" if e0 == 0 else "")
    tx = norm(" ".join(L))
    mm = re.search(r"[Aa]djusted [Nn]et [Ii]ncome( \(ANI\))?\d?[^.;]{0,140}?\(?\$\d+\.\d\d per (basic |diluted )?share\)?", tx)
    if mm:
        d["adj_note"] = quote(p, mm.group(0))
    d["source_title"] = SOURCES[sid]["title"]
    PR.append(d)
    return d


for k in REL:
    print_q(*k)

# each Q4 print's year: with the 10-K the same day (Q4 2021, 2022, 2024, 2025), the print's full year equals the 10-K's and the 10-K
# cites it ('source_10k'); the Q4 2023 release comes a week before its 10-K, so its year is the print's full-year actual ('fy_actual')
for fy in (2021, 2022, 2023, 2024, 2025):
    p = RP[(fy, 4)]
    pr = [x for x in PR if (x["fy"], x["q"]) == (fy, 4)][0]
    st = find(p, STMT, 0)
    kind, _ = layout(p, st, 4, fy)
    col = (lambda v: v[9]) if kind == "multi" else (lambda v: v[2])
    sv, _ = row(p, r"^Sales( \(\d+\))? \|", st)
    dv, _ = row(p, r"^Continuing operations \|", find(p, r"^Diluted:( \(\d+\))?$", st))
    rev, eps, _, _ = statements(KP[fy])
    if fy != 2023:
        assert SOURCES[KID[fy]]["published"] == pr["published"], (fy, "the 10-K is public the same day as the release")
        assert (col(sv), col(dv)) == (rev[0], eps[0]), (fy, sv, dv, rev[0], eps[0])
        pr["source_10k"] = KID[fy]
        continue
    assert SOURCES[KID[fy]]["published"] > pr["published"] and col(sv) == rev[0] and col(dv) != eps[0], (fy, col(dv), eps[0])
    pv, ptrow = row(p, r"^Income \(loss\) before income and mining tax and other items \|", st, n=4)
    txv, txrow = row(p, r"^Income and mining tax benefit \(expense\) \|", st, n=4)
    shv, shrow = row(p, r"^Diluted \|", find(p, r"^Weighted average common shares \(millions\):$", st), n=4)
    L = lines(p)
    i = [j for j in range(len(L) - 1) if re.match(r"^Gold sold \(thousand ounces\) \|", L[j])
         and re.match(r"^Costs applicable to sales per ounce( ?\(\d+\))? \|", L[j + 1])][0]
    ozv, ozrow = cells(p, i)
    csv_, csrow = cells(p, i + 1)
    prelim = quote(p, "Newmont’s actual consolidated financial results remain subject to completion of our annual audit procedures for the "
                      "year ended December 31, 2023")
    pr["fy_actual"] = {
        "fy": 2023, "fy_label": "FY23", "eps": col(dv), "revenue_usd_b": col(sv) / 1000, "diluted_shares_m": shv[2],
        "eps_excluded": loss_text(col(dv), "the Q4 2023 release, preliminary", ADJ("Q4 2023", a23, ae23)),
        "margin": round(pv[2] / col(sv) * 100, 2),
        "margin_note": f"FY23 income (loss) before income and mining tax and other items $({-pv[2]:,.0f})M / sales ${col(sv):,.0f}M (the Q4 2023 release)",
        "tax_rate": round(-txv[2] / pv[2], 4), "tax_note": f"FY23 income and mining tax ${abs(txv[2]):,.0f}M / pre-tax $({-pv[2]:,.0f})M (the Q4 2023 release)",
        "sales_growth": pct1(sv[3], sv[2]), "oz_k": ozv[2], "oz_pct": pct1(ozv[3], ozv[2]), "cas": csv_[2],
        "cas_pct": pct1(csv_[3], csv_[2]), "rows": [ptrow, txrow, shrow, ozrow, csrow],
        "note": f"the Q4 2023 release's full year, used until the year's 10-K is public; the release is preliminary: '{prelim}'"}
    assert pv[2] < 0 and pr["fy_actual"]["eps"] == -2.97 and pr["fy_actual"]["sales_growth"] == pct1(11915, 11812)

# ── dividends: each rate from the first filing that states it as declared (not a payout range, a framework or a plan) ──
DV = [((2021, 4), 0.55, "Declared fourth quarter dividend of $0.55 per share"),
      ((2022, 1), 0.55, "Declared first quarter dividend of $0.55 per share"),
      ((2022, 2), 0.55, "Declared second quarter dividend of $0.55 per share"),
      ((2022, 3), 0.55, "Declared third quarter dividend of $0.55 per share"),
      ((2022, 4), 0.40, "Declared fourth quarter 2022 dividend of $0.40 per share"),
      ((2023, 1), 0.40, "declared a dividend of $0.40 per share of common stock for the first quarter of 2023"),
      ((2023, 2), 0.40, "declared a dividend of $0.40 per share of common stock for the second quarter of 2023"),
      ((2023, 3), 0.40, "declared a dividend of $0.40 per share of common stock for the third quarter of 2023"),
      ("FY2023 10-K", 0.25, "In February 2024, the Board declared a dividend of $0.25 per share"),
      ((2024, 1), 0.25, "declared a dividend of $0.25 per share of common stock for the first quarter of 2024"),
      ((2024, 2), 0.25, "declared a dividend of $0.25 per share of common stock for the second quarter of 2024"),
      ((2024, 3), 0.25, "declared a dividend of $0.25 per share of common stock for the third quarter of 2024"),
      ((2024, 4), 0.25, "declared a dividend of $0.25 per share of common stock for the fourth quarter of 2024"),
      ((2025, 1), 0.25, "declared a dividend of $0.25 per share of common stock for the first quarter of 2025"),
      ((2025, 2), 0.25, "declared a dividend of $0.25 per share of common stock for the second quarter of 2025"),
      ((2025, 3), 0.25, "declared a dividend of $0.25 per share of common stock for the third quarter of 2025"),
      ((2025, 4), 0.26, "declared a dividend of $0.26 per share of common stock for the fourth quarter of 2025"),
      ((2026, 1), 0.26, "declared a dividend of $0.26 per share of common stock for the first quarter of 2026"),
      ((2026, 2), 0.26, "declared a dividend of $0.26 per share of common stock for the second quarter of 2026"),
      ((2026, 3), 0.26, "declared a dividend of $0.26 per share of common stock for the third quarter of 2026")]
for k, q_, s_ in DV:
    if k == "FY2023 10-K":
        sid, p, doc = KID[2023], KP[2023], "the FY2023 10-K; the Q4 2023 release states no rate"
    else:
        sid, p, doc = RID[k], RP[k], f"the Q{k[1]} {k[0]} release"
    f["dividends"].append({"published": SOURCES[sid]["published"], "quarterly": q_, "source": sid,
                           "note": f"${q_:.2f} a quarter (${q_ * 4:.2f} a year): '{quote(p, s_)}' ({doc})"})
quote(RP[(2022, 4)], "Annualized dividend payout range of $1.40 to $1.80 per share")          # a range, not a declared rate: text only

# ── outlooks (display only: attributable gold production and costs applicable to sales or all-in sustaining costs per ounce; method r2
# has no volume input and none for cost components, the XOM production and MSFT segment rules), one quote a release, cut to its year ──
UNUSED = ("a production and unit-cost outlook: method r2 has no input for a production guide (the XOM rule) or for cost components "
          "(the MSFT segment rule), so no field; no filing guides revenue, EPS or a margin")
G = f["guides"]
GQ = [(2022, (2021, 4), "Announced 2022 attributable production outlook of 6.2 million gold ounces"),
      (2022, (2022, 1), "Remain on track to achieve full-year guidance ranges"),
      (2022, (2022, 2), "Updated full-year guidance of 6.0 million ounces of attributable gold production, CAS of $900 per ounce and AISC of "
                        "$1,150 per ounce"),
      (2022, (2022, 3), "On track to achieve full-year guidance of 6.0 million ounces of attributable gold production with Gold CAS of $900 "
                        "per ounce and Gold AISC of $1,150 per ounce"),
      (2023, (2022, 4), "As previously signaled, 2023 production guidance is expected to be between 5.7 and 6.3 million gold ounces"),
      (2023, (2023, 1), "On track to achieve full-year guidance of between 5.7 and 6.3 million ounces of attributable gold production with "
                        "Gold AISC between $1,150 and $1,250 per ounce"),
      (2023, (2023, 2), "On track to achieve full-year guidance of between 5.7 and 6.3 million ounces of attributable gold production with "
                        "Gold AISC between $1,150 and $1,250 per ounce"),
      (2023, (2023, 3), "Revised 2023 outlook for the standalone Newmont portfolio to 5.3 million ounces of attributable production, CAS per "
                        "ounce** of $1,000 and AISC per ounce** of $1,400"),
      (2024, (2023, 4), "2024 production guidance is expected to be approximately 6.9 million gold ounces for the Total Newmont portfolio"),
      (2024, (2024, 1), "Firmly on track to deliver 2024 guidance for production, costs and capital spend"),
      (2024, (2024, 2), "On track to deliver 2024 guidance for production, costs and capital spend"),
      (2024, (2024, 3), "Positioned to meet Newmont's 2024 production guidance"),
      (2025, (2024, 4), "Attributable production for 2025 is expected to be approximately 5.9 million gold ounces"),
      (2025, (2025, 1), "On track to meet Newmont's 2025 guidance"),
      (2025, (2025, 2), "On track to meet Newmont's 2025 guidance"),
      (2025, (2025, 3), "Improved Newmont's 2025 cost and capital guidance through continued progress on cost savings initiatives and a shift "
                        "in the timing of capital spend"),
      (2026, (2025, 4), "Attributable production for 2026 is expected to be approximately 5.3 million gold ounces"),
      (2026, (2026, 1), "On track to meet Newmont's full year 2026 production guidance"),
      (2026, (2026, 2), "On track to meet Newmont's full year 2026 production guidance"),
      (2026, (2026, 3), "On track to meet Newmont's full-year 2026 production guidance")]
for fy, k, s_ in GQ:
    assert not [y for y in re.findall(r"\b20\d\d\b", s_) if int(y) != fy], (k, "a quote names another year")
    G.append({"fy": fy, "published": SOURCES[RID[k]]["published"], "source": RID[k], "doc": f"Q{k[1]} {k[0]} release",
              "display": quote(RP[k], s_), "unused": UNUSED})

# ── assemble: the earlier facts unchanged ──
for k in ("sources", "history_vintages", "prints", "guides", "dividends", "company_names"):
    o = old[k]
    n = f[k]
    if isinstance(o, dict):
        assert all(n[x] == o[x] for x in o), k
    else:
        assert n[:len(o)] == o, k
for x in ("rule_t", "listings", "events", "splits", "distributions", "eps_guides", "company_names"):
    assert f[x] == old[x], x
assert all(s["published"] <= CUT for s in SOURCES.values())
f["sources"] = dict(sorted(SOURCES.items(), key=lambda kv: int(kv[0][2:])))
f["_doc"] = old["_doc"].replace("gen_nem_1417.py (2014-2017) and gen_nem_1821.py (2018-2021) from the filings",
                                "gen_nem_1417.py (2014-2017), gen_nem_1821.py (2018-2021) and gen_nem_2226.py (2022-2026) from the filings")
assert f["_doc"] != old["_doc"]
with open(FACTS, "w", encoding="utf-8") as fh:
    json.dump(f, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_nem_2226.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump({k: v for k, v in CHECK.items() if v}, fh, ensure_ascii=False, indent=1)
print(f"{FACTS}: {len(V)} vintages, {len(PR)} prints, {len(G)} guides, {len(f['dividends'])} dividends, {len(SOURCES)} sources; "
      f"{sum(len(v) for v in CHECK.values())} quotes in {ck}")
for p in PR[-20:]:
    print(p["quarter"], p["published"], p["release_time"][-42:], p["sales_pct"], p["oz_pct"], p["cas_pct"], p["eps_q"],
          p["eps_q_prior"], p["eps_pct"], p["margin_bp"], p["diluted_shares_m"], p["cash_b"], p["debt_note"])
for v in V[-5:]:
    print(v["published"], v["fy_label"], v["kind"], v["eps_normalized"], sorted(v["eps_excluded"]), v["prev_fy_margin"], v["tax_rate"],
          v["prev_fy_oz_k"], v["prev_fy_oz_pct"], v["prev_fy_cas"], v["groups"], v["fcf_b"], v["cash_b"], v["dividend_annual"])
