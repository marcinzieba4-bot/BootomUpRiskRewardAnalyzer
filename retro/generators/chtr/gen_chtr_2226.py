#!/usr/bin/env python3
"""Extend retro/facts/CHTR.json with 2022-2026 (filings accepted 2022-01-01 to 2026-11-22), asserting that every earlier fact is unchanged.

The discipline of the earlier sheets (gen_chtr.py, gen_chtr_1417.py, gen_chtr_1821.py; retro/README.md, "CHTR 2022-2026"): each figure
from its own row by label under an anchored heading, each quoted sentence asserted present in its own filing, every derived figure
(growth, margin, one-off test) computed, and a verbatim checklist written. What this batch adds:

  - the FY2021-FY2025 10-K vintages. Item 6 is "[Reserved]" from the FY2021 10-K, so each vintage takes three years from its own
    statements of operations (revenues, income from operations, income before income taxes, net income attributable to Charter
    shareholders, diluted EPS and diluted shares) and the earlier years from the latest earlier vintage, as that vintage printed them
    (the SCHW, NEE and LLY 2022 rule; `carried_from` names the vintage); the one-off test of each new year on the MD&A statement of
    operations' items outside the recurring operating lines (the 2018-2021 encoding); the 10-K model fields as before, with the AI
    words of the FY2023-FY2025 10-Ks quoted (text only: GENAI's scope names no cable operator, the UNH `ai_words` encoding);
  - the prints Q4 2021 to Q3 2026 (the earnings releases, 8-K exhibit 99.1). From Q2 2022 the releases' statement of operations is the
    GAAP statement (REVENUES, no Adjusted EBITDA row), so Adjusted EBITDA comes from the addendum's reconciliation of non-GAAP measures
    (equal to the statement's row where both exist: asserted); from Q3 2026 the release adds pro forma columns for the Cox Transactions
    (closed 2026-08-19): the actual columns are read, Cox in as published, and the year-ago customer relationships come from the
    addendum's actual summary of operating statistics, as the first table's year-ago column is pro forma (the CB, SCHW and LLY pro forma
    rule: pro forma figures unused);
  - each 10-K's streaming words (STREAMING, company-acknowledged, the CMCSA encoding), listing and no-dividend sentences.
No filing of 2022-2026 guides revenue, EPS or a margin in numbers (the capital expenditure outlooks are a cost component, display only;
the Cox synergy and savings targets are cost components too, unencoded). Run:

    python3 retro/tools/edgar.py index 1091667 <dir>
    python3 retro/tools/edgar.py fetch 1091667 <dir> --from 2021-01-01 --to 2026-11-27 --forms 10-K 10-K/A
    python3 retro/tools/edgar.py fetch 1091667 <dir> --from 2021-12-01 --to 2026-11-27 --forms 8-K 8-K/A
    python3 -I retro/generators/chtr/gen_chtr_2226.py --filings <dir> [--facts-in <2008-2021 sheet>] [--out retro/facts/CHTR.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_chtr_2226.json

--facts-in is the 2008-2021 sheet (default retro/facts/CHTR.json, which must then hold no fact published after 2021-12-31). It only appends.
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
_ap.add_argument("--filings", required=True, help="folder edgar.py wrote (allrows.json, tenk/, eightk/); keep it outside the repo")
_ap.add_argument("--facts-in", help="the 2008-2021 fact sheet to extend (default retro/facts/CHTR.json)")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/CHTR.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_chtr_2226.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402

ET = ZoneInfo("America/New_York")
PREV_CUT, CUT = "2021-12-31", "2026-11-22"
CIK = 1091667
FILINGS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("^GSPC")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
CHECK, TEXT = {}, {}
IN = A.facts_in or os.path.join(REPO, "retro", "facts", "CHTR.json")
old = json.load(open(IN, encoding="utf-8"))
assert all(s["published"] <= PREV_CUT for s in old["sources"].values()), "the input sheet already holds a fact after 2021-12-31"
f = copy.deepcopy(old)
CCI = "Charter Communications, Inc."


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def path(acc, pattern):
    hits = [p for sub in ("tenk", "eightk", "tenq", "other") for p in glob.glob(os.path.join(SP, sub, acc, pattern))]
    assert len(hits) == 1, (acc, pattern, hits)
    return hits[0]


def lines(p):
    if p not in TEXT:
        with open(p, encoding="utf-8", errors="replace") as fh:
            TEXT[p] = [norm(x) for x in fh.read().split("\n")]
    return TEXT[p]


def quote(p, s):
    assert norm(s) in norm(" ".join(lines(p))), (p, s[:120])
    CHECK.setdefault(p, []).append(s)
    return s


def num(c):
    c = c.strip().replace(",", "").replace("$", "")
    if c in ("--", "—", "-"):
        return 0.0
    neg = c.startswith("(") and c.endswith(")")
    return -float(c.strip("()")) if neg else float(c.strip("()"))


def cells(x):
    """A row's numeric cells, the percentage-change cells and the open-parenthesis halves of '(12.3 | )%' left out."""
    out = []
    for c in x.split("|")[1:]:
        c = c.strip()
        if not c or c.endswith("%") or c in (")", ")%", "NM", "n/a", "ppts", ") ppts") or c.startswith("(") and not c.endswith(")"):
            continue
        out.append(num(c))
    return out


def row(p, label, after=None, n=None, start=0, stop=None):
    """The first row whose first cell is `label` (one of `label` if a tuple), from `start` (after the first line containing `after`)
    and before `stop`, as numbers; it goes on the checklist."""
    labels = label if isinstance(label, tuple) else (label,)
    ls = lines(p)
    i0 = next(i for i, x in enumerate(ls) if i >= start and after in x) if after else start
    for i in range(i0, stop if stop is not None else len(ls)):
        x = ls[i]
        if x.split("|")[0].strip() in labels and cells(x):
            v = cells(x)
            assert n is None or len(v) >= n, (p, label, v)
            CHECK.setdefault(p, []).append(x)
            return v, i
    raise AssertionError((p, label, after, start))


def published(acc):
    """The acceptance-time rule: accepted at or after 16:00 ET, the next trading day; otherwise that day."""
    r = FILINGS[acc]
    t = dt.datetime.fromisoformat(r[1].replace("Z", "+00:00")).astimezone(ET)
    day = t.date().isoformat()
    if t.hour >= 16 or day not in TDAYS:
        day = next(d for d in TDAYS if d > day)
    assert PREV_CUT < r[0] <= CUT, acc
    when = "after the close" if t.hour >= 16 else ("before the open" if (t.hour, t.minute) < (9, 30) else "during the session")
    return day, f"{t:%Y-%m-%d %H:%M} ET ({when})", when


def url(acc, p):
    return f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc.replace('-', '')}/{os.path.basename(p).split('__', 1)[1].replace('.rows.txt', '')}"


def source(sid, acc, p, title, supports):
    assert sid not in f["sources"], sid
    day, filed, when = published(acc)
    f["sources"][sid] = {"published": day, "filed": filed, "accession": acc, "title": title, "url": url(acc, p), "supports": supports}
    return day, filed, when


pct = lambda a, b: round((b / a - 1) * 100, 2)
mg = lambda x, rev: round(x / rev * 100, 2)

# ── the 10-K vintages FY2021-FY2025: three years from the statements of operations, earlier years from the latest earlier vintage ──
TENK = [("CH43", "0001091667-22-000024", "10-K__chtr-20211231.rows.txt", "Charter FY2021 10-K", 2021),
        ("CH44", "0001091667-23-000024", "10-K__chtr-20221231.rows.txt", "Charter FY2022 10-K", 2022),
        ("CH45", "0001091667-24-000028", "10-K__chtr-20231231.rows.txt", "Charter FY2023 10-K", 2023),
        ("CH46", "0001091667-25-000034", "10-K__chtr-20241231.rows.txt", "Charter FY2024 10-K", 2024),
        ("CH47", "0001091667-26-000017", "10-K__chtr-20251231.rows.txt", "Charter FY2025 10-K", 2025)]
P10K = {}


def statements(p, fy):
    """The consolidated statements of operations (three years): the heading line, then '(dollars in millions, ...' and the years."""
    ls = lines(p)
    s0 = next(i for i, x in enumerate(ls) if x == "CONSOLIDATED STATEMENTS OF OPERATIONS" and ls[i + 1].startswith("(dollars in millions"))
    years = tuple(range(fy, fy - 3, -1))
    hdr = " | ".join(str(y) for y in years)
    assert ls[s0 + 3] == hdr, (p, ls[s0 + 3])
    CHECK.setdefault(p, []).append(hdr)
    e = next(i for i in range(s0, len(ls)) if ls[i].startswith("Weighted average common shares outstanding, diluted")) + 1
    rev, _ = row(p, "REVENUES", start=s0, stop=e)
    io, _ = row(p, "Income from operations", start=s0, stop=e)
    pti, _ = row(p, "Income before income taxes", start=s0, stop=e)
    ni, _ = row(p, "Net income attributable to Charter shareholders", start=s0, stop=e)
    ep = next(i for i in range(s0, e) if ls[i].startswith("EARNINGS PER COMMON SHARE ATTRIBUTABLE TO CHARTER SHAREHOLDERS"))
    eps, _ = row(p, "Diluted", start=ep, stop=e)
    sh, _ = row(p, "Weighted average common shares outstanding, diluted", start=s0, stop=e)
    return years, {y: {"revenue_m": rev[i], "income_from_operations_m": io[i], "pretax_income_m": pti[i], "net_income_m": ni[i],
                       "eps_diluted": eps[i], "diluted_shares_m": round(sh[i] / 1e6, 3)} for i, y in enumerate(years)}


prev_v = max(old["history_vintages"], key=lambda v: v["published"])      # the FY2020 10-K vintage (CH27)
assert prev_v["source"] == "CH27"
vintages, V = [], {}
for sid, acc, fname, title, fy in TENK:
    p = path(acc, fname)
    P10K[fy] = p
    ls = lines(p)
    assert quote(p, "Item 6. [Reserved]") and "Not applicable." in ls[ls.index("Item 6. [Reserved]") + 1]
    years, st = statements(p, fy)
    periods = {}
    for k, per in prev_v["periods"].items():           # the earlier years, as the latest earlier vintage printed them
        if int(k) not in years:
            periods[k] = {**copy.deepcopy(per), "carried_from": per.get("carried_from", prev_v["source"])}
    for y in sorted(years):
        periods[str(y)] = {"issuer": CCI, "start": f"{y}-01-01", "end": f"{y}-12-31", "months": 12, "revenue_m": st[y]["revenue_m"],
                           "eps_diluted": st[y]["eps_diluted"], "eps_continuing": st[y]["eps_diluted"],
                           "diluted_shares_m": st[y]["diluted_shares_m"], "net_income_m": st[y]["net_income_m"],
                           "income_from_operations_m": st[y]["income_from_operations_m"], "pretax_income_m": st[y]["pretax_income_m"]}
    periods = {k: periods[k] for k in sorted(periods)}
    day, filed, _ = source(sid, acc, p, title, f"Item 6 [Reserved]; the consolidated statements of operations: revenues, income from "
                           f"operations, income before income taxes, net income attributable to Charter shareholders, diluted EPS and "
                           f"diluted weighted average shares for {', '.join(str(y) for y in years)}; the statements of cash flows and "
                           "balance sheets, the MD&A's statement of operations and revenues by service offering, Items 1, 1A and 5")
    v = {"published": day, "source": sid, "fy_label": f"FY{fy % 100:02d}", "periods": periods, "priced_issuers": [CCI],
         "eps_basis": ("diluted EPS as the statements of operations print it, three years (Item 6 is reserved); the earlier years as the "
                       "latest earlier vintage printed them ('carried_from'); no discontinued operations in the years shown"),
         "statement_years": list(years)}
    vintages.append(v)
    V[fy] = v
    prev_v = v

# ── the one-off tests (the AAPL FY2002 test and its mirror; method r2), each new year in its own 10-K ───────────────────────────────


def listed_items(p, fy):
    """The MD&A statement of operations' items outside the recurring operating lines, each pre-tax and taken whole (the CB FY2005
    netting): other operating (income) expenses, net, and every row between income from operations and income before income taxes
    except net interest expense, the first column (the year `fy`); each row goes on the checklist."""
    ls = lines(p)
    a = next(i for i, x in enumerate(ls) if "The following table sets forth the consolidated statements of operations for the periods presented" in x)
    assert ls[a + 2] == f"{fy} | {fy - 1}", (p, ls[a + 2])
    io = next(i for i in range(a, len(ls)) if ls[i].startswith("Income from operations |"))
    pt = next(i for i in range(io, len(ls)) if ls[i].startswith("Income before income taxes |"))
    items = {}
    oo = next(x for x in ls[a:io] if re.match(r"Other operating (\(income\) )?expenses?, net \|", x))
    CHECK.setdefault(p, []).append(oo)
    items[oo.split("|")[0].strip()] = -cells(oo)[0]     # an operating expense row is printed positive, an income in parentheses
    for x in ls[io + 1:pt]:
        lab = x.split("|")[0].strip()
        if not lab or re.fullmatch(r"[()0-9,.—-]+", lab) or lab.startswith("Interest expense") or lab.startswith("Other Income") \
                or not cells(x):
            continue
        CHECK.setdefault(p, []).append(x)
        items[lab] = cells(x)[0]
    return items


tests = dict(copy.deepcopy(old["history_vintages"][-1]["one_off_tests"]))   # 2016-2020, unchanged
for sid, acc, fname, title, fy in TENK:
    items = listed_items(P10K[fy], fy)
    ni = V[fy]["periods"][str(fy)]["net_income_m"]
    net = -sum(items.values())
    gross_ch = -sum(v for v in items.values() if v < 0)
    gross_be = sum(v for v in items.values() if v > 0)
    tests[str(fy)] = {"fy": fy, "kind": "charges" if net > 0 else "benefits", "income_attributable_m": ni, "items_pre_tax_m": items,
                      "net_charges_m": net, "gross_charges_m": gross_ch, "gross_benefits_m": gross_be,
                      "distorted": gross_ch > ni or gross_be > ni - gross_be, "figure_without_published": None,
                      "note": (f"the listed items outside operations, each pre-tax and whole: {', '.join(f'{k} {v:+,.0f}' for k, v in items.items())} "
                               f"($M); charges ${gross_ch:,.0f}M against net income attributable of ${ni:,.0f}M (the AAPL FY2002 test), "
                               f"benefits ${gross_be:,.0f}M against ${ni - gross_be:,.0f}M without them (its mirror): neither is met, so the "
                               "year is kept at GAAP")}
    assert not tests[str(fy)]["distorted"], fy
    V[fy]["one_off_tests"] = {k: copy.deepcopy(t) for k, t in tests.items() if k in V[fy]["periods"]}

# ── the prints, Q4 2021 to Q3 2026 (the earnings releases, 8-K exhibit 99.1) ─────────────────────────────────────────────────────────
PRINTS = [("CH50", "0001091667-22-000022", 2021, 4), ("CH51", "0001091667-22-000064", 2022, 1), ("CH52", "0001091667-22-000088", 2022, 2),
          ("CH53", "0001091667-22-000114", 2022, 3), ("CH54", "0001091667-23-000022", 2022, 4), ("CH55", "0001091667-23-000082", 2023, 1),
          ("CH56", "0001091667-23-000107", 2023, 2), ("CH57", "0001091667-23-000141", 2023, 3), ("CH58", "0001091667-24-000027", 2023, 4),
          ("CH59", "0001091667-24-000084", 2024, 1), ("CH60", "0001091667-24-000103", 2024, 2), ("CH61", "0001091667-24-000121", 2024, 3),
          ("CH62", "0001091667-25-000033", 2024, 4), ("CH63", "0001091667-25-000098", 2025, 1), ("CH64", "0001091667-25-000126", 2025, 2),
          ("CH65", "0001091667-25-000167", 2025, 3), ("CH66", "0001091667-26-000016", 2025, 4), ("CH67", "0001091667-26-000027", 2026, 1),
          ("CH68", "0001091667-26-000051", 2026, 2), ("CH69", "0001091667-26-000072", 2026, 3)]
QEND = {1: "March 31", 2: "June 30", 3: "September 30", 4: "December 31"}
QWORD = {1: "first", 2: "second", 3: "third", 4: "fourth"}
COX_CLOSE = "2026-08-19"
prints = []
for sid, acc, fy, q in PRINTS:
    p = path(acc, "EX-99.1__*.rows.txt")
    ls = lines(p)
    # the statement of operations: the GAAP statement (Q2 2022 on; the actual one when pro forma statements follow it), or the earlier
    # statement 'AND OPERATING DATA' with its 'Total Revenue' and 'Adjusted EBITDA' rows (Q4 2021, Q1 2022)
    gaap = [i for i, x in enumerate(ls) if x == "UNAUDITED CONSOLIDATED STATEMENTS OF OPERATIONS"]
    s0 = gaap[0] if gaap else next(i for i, x in enumerate(ls) if x == "UNAUDITED CONSOLIDATED STATEMENTS OF OPERATIONS AND OPERATING DATA")
    hdr = next(x for x in ls[s0:s0 + 6] if x.startswith(f"Three Months Ended {QEND[q]},"))
    CHECK.setdefault(p, []).append(hdr)
    pro_forma = any(x.startswith("Pro Forma") for x in ls)
    if pro_forma:
        assert ls[s0 + 4] == "Actual | Actual | Actual | Actual", (sid, ls[s0 + 4])
        CHECK.setdefault(p, []).append(ls[s0 + 4])
    e = next(i for i in range(s0, len(ls)) if ls[i].startswith("Weighted average common shares outstanding, diluted")) + 1
    rev, _ = row(p, ("Total Revenue", "REVENUES"), start=s0, stop=e)
    oi, _ = row(p, ("Income from operations", "Income (loss) from operations"), start=s0, stop=e)
    pti, _ = row(p, ("Income before income taxes", "Income (loss) before income taxes"), start=s0, stop=e)
    eps, _ = row(p, "Diluted", start=s0, stop=e)
    sh, _ = row(p, "Weighted average common shares outstanding, diluted", start=s0, stop=e)
    # Adjusted EBITDA: the addendum's reconciliation of non-GAAP measures (its first block: the actual one), equal to the statement's
    # row where the statement prints one
    r0 = next(i for i, x in enumerate(ls) if x == "UNAUDITED RECONCILIATION OF NON-GAAP MEASURES TO GAAP MEASURES")
    if pro_forma:
        assert ls[r0 + 4].startswith("Actual | Actual"), (sid, ls[r0 + 4])
    eb_lab = next(x.split("|")[0].strip() for x in ls[r0:] if re.fullmatch(r"Adjusted EBITDA( \([a-z]\))?", x.split("|")[0].strip()))
    ebitda, _ = row(p, eb_lab, start=r0)
    if any(x.split("|")[0].strip() == "Adjusted EBITDA" for x in ls[s0:e]):
        eb_st = row(p, "Adjusted EBITDA", start=s0, stop=e)[0]
        assert eb_st[:2] == ebitda[:2], (sid, eb_st, ebitda)
    else:
        assert gaap, sid
    c0 = next(i for i, x in enumerate(ls) if x == "UNAUDITED CONSOLIDATED STATEMENTS OF CASH FLOWS")
    cfo, _ = row(p, "Net cash flows from operating activities", start=c0)
    i0 = next(i for i in range(c0, len(ls)) if ls[i] == "CASH FLOWS FROM INVESTING ACTIVITIES:")
    capex, _ = row(p, "Purchases of property, plant and equipment", start=i0)
    # total customer relationships against the year-ago quarter: the key operating results (this quarter's end, then the year-ago
    # quarter's, as the release shows it); when that table's year-ago column is pro forma (Q3 2026, the Cox Transactions), the addendum's
    # actual summary of operating statistics (this quarter's end and the year-ago quarter's, actual)
    if pro_forma:
        k0 = next(i for i, x in enumerate(ls) if x == "UNAUDITED SUMMARY OF OPERATING STATISTICS" and ls[i + 4] == "Actual")
        kh = ls[k0 + 3]
        cols = [re.sub(r"( \([a-z]\))+$", "", c.strip()) for c in kh.split("|")]
        assert cols[0] == f"{QEND[q]}, {fy}" and cols[-1] == f"{QEND[q]}, {fy - 1}", (sid, kh)
        CHECK.setdefault(p, []).extend([kh, "Actual"])
        relrow, _ = row(p, "Total Customer Relationships", start=k0)
        rel = [relrow[0], relrow[len(cols) - 1]]
        assert len(relrow) == len(cols), (sid, relrow)
    else:
        k0 = next(i for i, x in enumerate(ls) if x == "Key Operating Results")
        kh = next(x for x in ls[k0:k0 + 4] if x.startswith(f"{QEND[q]}, {fy}"))
        cols = [re.sub(r"( \([a-z]\))+$", "", c.strip().replace(")(", ") (")) for c in kh.split("|")]
        assert cols[0] == f"{QEND[q]}, {fy}" and cols[1] == f"{QEND[q]}, {fy - 1}", (sid, kh)
        CHECK.setdefault(p, []).append(kh)
        rel, _ = row(p, "Total Customer Relationships", start=k0)
    # the release's own sentence on share repurchases in the quarter (display): the 'Share Repurchases' section
    sr = next(i for i, x in enumerate(ls) if x == "Share Repurchases")
    bb_s = re.search(r"(During the (?:three months ended [A-Z][a-z]+ \d+, 20\d\d|[a-z]+ quarter(?: of 20\d\d)?), Charter purchased .*?"
                     r"for (?:approximately )?\$[0-9.,]+ (?:billion|million))", ls[sr + 1])
    assert bb_s, (sid, ls[sr + 1][:200])
    bb_s = quote(p, bb_s.group(1))
    day, filed, when = source(sid, acc, p, f"Charter Q{q} {fy} earnings release (8-K exhibit 99.1)",
                              f"Q{q} {fy} against Q{q} {fy - 1}: revenues, income from operations, income before income taxes, diluted EPS "
                              "and shares (statement of operations), Adjusted EBITDA (reconciliation of non-GAAP measures), purchases of "
                              "property, plant and equipment (statement of cash flows), total customer relationships ("
                              + ("the addendum's actual summary of operating statistics; actual columns, pro forma unused)" if pro_forma
                                 else "key operating results)"))
    raw = {"rev_m": rev[0], "rev_prior_m": rev[1], "ebitda_m": ebitda[0], "ebitda_prior_m": ebitda[1], "oi_m": oi[0], "oi_prior_m": oi[1],
           "pti_m": pti[0], "pti_prior_m": pti[1], "capex_m": -capex[0], "capex_prior_m": -capex[1], "cfo_m": cfo[0],
           "rel_k": rel[0], "rel_prior_k": rel[1], "eps_q": eps[0], "eps_q_prior": eps[1], "dil_sh_m": round(sh[0] / 1e6, 3)}
    pr = {"quarter": f"Q{q} {fy}", "fy": fy, "q": q, "published": day, "source": sid, "release": day, "release_time": filed, "raw": raw,
          "sales_b": round(rev[0] / 1000, 3), "sales_pct": pct(rev[1], rev[0]), "rel_pct": pct(rel[1], rel[0]),
          "ocf_margin": mg(ebitda[0], rev[0]), "ocf_margin_bp": round((mg(ebitda[0], rev[0]) - mg(ebitda[1], rev[1])) * 100, 1),
          "op_margin": mg(oi[0], rev[0]), "op_margin_bp": round((mg(oi[0], rev[0]) - mg(oi[1], rev[1])) * 100, 1),
          "capex_pct": mg(-capex[0], rev[0]), "capex_bp": round((mg(-capex[0], rev[0]) - mg(-capex[1], rev[1])) * 100, 1),
          "eps_q": eps[0], "eps_q_prior": eps[1], "diluted_shares_m": round(sh[0] / 1e6, 3), "cash_note": bb_s,
          "next_print": f"Q{q % 4 + 1} {fy + (1 if q == 4 else 0)} print"}
    # capital expenditure outlooks (display only: a cost component, no revenue, EPS or margin guide; the CMCSA capex-guide rule)
    cx = [s for s in re.findall(r"Charter currently expects [^.]*(?:\.\d[^.]*)*\.", " ".join(ls)) if "capital expenditures" in s]
    if cx:
        pr["capex_outlook"] = quote(p, cx[0])
    if pro_forma:   # the Cox Transactions in the actual figures as published (display)
        pr["basis_note"] = quote(p, "In this release, actual results reflect the operations of Charter for the three and nine months ended "
                                    "September 30, 2026 and Cox Communications for the period from August 20, 2026 through September 30, 2026.")
        assert day > COX_CLOSE
    prints.append(pr)
assert [p["published"] for p in prints] == sorted(p["published"] for p in prints)
# each Q4 release came the same morning as its 10-K, so no Q4 release extends a vintage (the 'q4_actuals' rule has nothing to add)
for pr in prints:
    if pr["q"] == 4:
        v = V[pr["fy"]]
        assert pr["published"] == v["published"], (pr["quarter"], pr["published"], v["published"])
        assert pr["raw"]["eps_q"] is not None

# ── the 10-K model fields: margins, tax rate, cash flow, revenue lines, customer relationships, the durability, streaming and AI words ─
GROUP_LABELS = {2021: ("Residential revenue", "Small and medium business", "Enterprise", "Advertising sales", "Mobile", "Other"),
                2022: ("Residential revenue", "Small and medium business", "Enterprise", "Advertising sales", "Mobile", "Other"),
                2023: ("Residential revenue", "Small and medium business", "Enterprise", "Advertising sales", "Other"),
                2024: ("Residential revenue", "Small and medium business", "Enterprise", "Advertising sales", "Other"),
                2025: ("Residential revenue", "Small business", "Mid-market & large business", "Advertising sales", "Other")}
STREAM_RISK = {2021: "As the proliferation of online video services grows, however, services from V-MVPDs and direct to consumer offerings, as "
                     "well as piracy and password sharing, negatively impact the number of customers purchasing our video product.",
               2022: "As the proliferation of online video services grows, however, services from vMVPDs and direct to consumer offerings, as "
                     "well as piracy and password sharing, negatively impact the number of customers purchasing our video product.",
               2023: "However, services from virtual MVPDs and DTC offerings, as well as piracy and password sharing, negatively impact the number "
                     "of customers purchasing our video product.",
               2024: "However, services from virtual MVPDs and programmer streaming applications, as well as piracy and password sharing, "
                     "negatively impact the number of customers purchasing our video product.",
               2025: "However, services from virtual MVPDs and programmer streaming applications, as well as piracy and password sharing, "
                     "negatively impact the number of customers purchasing our video product."}
STREAM_OWN = {2021: ("Historically, we have generally viewed SVOD online video services as complementary to our own video offering, and we have "
                     "developed a cloud-based guide that is capable of incorporating video from online video services currently offered in the "
                     "marketplace.", "a cloud-based guide incorporating online video services"),
              2022: ("Historically, we have generally viewed SVOD online video services as complementary to our own video offering.",
                     "SVOD services viewed as complementary to its own video offering"),
              2023: ("Historically, we have generally viewed SVOD online video services as complementary to our own video offering and, in the "
                     "case of programmer DTC offerings, have begun to package the DTC services with the linear offerings.",
                     "programmer DTC services packaged with its linear offerings"),
              2024: ("Historically, we have generally viewed SVOD online video services as complementary to our own video offering and, in the "
                     "case of programmer streaming applications, we are packaging with the linear offerings.",
                     "programmer streaming applications packaged with its linear offerings"),
              2025: ("Historically, we have generally viewed SVOD online video services as complementary to our own video offering and, in the "
                     "case of programmer streaming applications, we are packaging with the linear offerings.",
                     "programmer streaming applications packaged with its linear offerings")}
AI_Q = ("A failure to effectively anticipate or adapt to new technologies (including those that use artificial intelligence ({q}AI{r})) and "
        "changes in customer expectations and behavior could significantly adversely affect our competitive position with respect to the "
        "leisure time and discretionary spending of our customers and, as a result, affect our business and results of operations.")
MODEL = {}
for sid, acc, fname, title, fy in TENK:
    p = P10K[fy]
    ls = lines(p)
    v = V[fy]
    anc = next(x for x in ls if "The following table sets forth the consolidated statements of operations for the periods presented" in x)
    pti, _ = row(p, "Income before income taxes", anc)
    tax, _ = row(p, "Income tax expense", anc)
    cf0 = next(i for i, x in enumerate(ls) if x == "CONSOLIDATED STATEMENTS OF CASH FLOWS" and ls[i + 1].startswith("(dollars in millions"))
    cfo, _ = row(p, "Net cash flows from operating activities", start=cf0)
    ppe, _ = row(p, "Purchases of property, plant and equipment", start=cf0)
    bs0 = next(i for i, x in enumerate(ls) if x == "CONSOLIDATED BALANCE SHEETS" and ls[i + 1].startswith("(dollars in millions"))
    cash, _ = row(p, "Cash and cash equivalents", start=bs0)
    y = v["periods"][str(fy)]
    rev_y, rev_p = y["revenue_m"], v["periods"][str(fy - 1)]["revenue_m"]
    assert pti[0] == y["pretax_income_m"]
    m0 = next(i for i, x in enumerate(ls) if x.startswith("Revenues by service offering were as follows"))
    groups = []
    for lab in GROUP_LABELS[fy]:
        g, _ = row(p, lab, start=m0)
        groups.append([lab.replace(" revenue", ""), round(g[0] / 1000, 3), round((g[0] / g[1] - 1) * 100, 1) if g[1] else None])
    assert abs(sum(g[1] for g in groups) * 1000 - rev_y) < 1.5, (fy, "the revenue lines sum to the year's revenues")
    rel, _ = row(p, "Total Customer Relationships", "Customer Relationships")
    desc = next(x for x in ls if x.startswith("We are a leading broadband"))
    desc = quote(p, desc.split(". ")[0] + ".")
    cyc = quote(p, "Our business is subject to seasonal and cyclical variations.")
    cyc2 = quote(p, "Our revenue is subject to cyclical advertising patterns and changes in viewership levels.")
    risk = quote(p, STREAM_RISK[fy])
    own, own_short = STREAM_OWN[fy]
    own = quote(p, own)
    nodiv = quote(p, "Charter has not paid cash dividends on its common stock and does not intend to do so in the foreseeable future.")
    MODEL[fy] = {
        "pretax_margin": mg(pti[0], rev_y), "tax_rate": round(tax[0] * -1 / pti[0], 4), "op_margin": mg(y["income_from_operations_m"], rev_y),
        "sales_growth": round((rev_y / rev_p - 1) * 100, 1), "fcf_b": round((cfo[0] + ppe[0]) / 1000, 3), "cash_b": round(cash[0] / 1000, 3),
        "cfo_m": cfo[0], "ppe_m": -ppe[0], "groups": groups, "rel_k": rel[0], "rel_prior_k": rel[1], "rel_pct": pct(rel[1], rel[0]),
        "business_quote": desc, "cyclical_quote": cyc, "cyclical_quote2": cyc2, "streaming_risk_quote": risk, "own_offering_quote": own,
        "own_offering_short": own_short, "no_dividend_quote": nodiv}
    if fy >= 2023:   # the AI words (GENAI, live from 2022-11-30, scoped to substitution of software, services and content: text only)
        a = AI_Q.format(q="\"" if fy == 2023 else "“", r="\"" if fy == 2023 else "”")
        MODEL[fy]["ai_quote"] = quote(p, a)
    else:
        assert not any("artificial intelligence" in x for x in ls), fy
    v["model"] = MODEL[fy]

# ── the streaming words of each 10-K (STREAMING, live from 2015-08-04: company-acknowledged, the CMCSA encoding) ────────────────────
events = []
for sid, acc, fname, title, fy in TENK:
    m = MODEL[fy]
    rq = m["streaming_risk_quote"]
    short = rq.split("however, ")[1] if "however, " in rq else rq.split("However, ")[1][0].lower() + rq.split("However, ")[1][1:]
    own = m["own_offering_quote"]
    offering = ("the same 10-K says it has " + own.split("and we have ")[1].rstrip(".") + ", having viewed SVOD online video services as "
                "complementary to its own video offering") if "and we have " in own else \
        ("the same 10-K says it has generally viewed SVOD online video services as complementary to its own video offering"
         + (", " + own.split("offering and, ")[1].rstrip(".").replace("we are packaging", "it is packaging them").replace(
             "have begun to package", "it has begun to package") if "offering and, " in own else ""))
    events.append({"id": f"{sid}-STREAM", "published": V[fy]["published"], "source": sid, "kind": "streaming_company_acknowledged",
                   "theme": "STREAMING", "doc": f"FY{fy} 10-K", "risk_quote": rq, "risk_short": short.rstrip("."),
                   "offering": offering, "offering_short": m["own_offering_short"]})

lq = "Charter’s Class A common stock is listed on the NASDAQ Global Select Market under the symbol “CHTR.”"
for sid, acc, fname, title, fy in TENK:
    f["listings"].append({"published": V[fy]["published"], "source": sid, "issuer": CCI, "exchange": "NASDAQ Global Select Market",
                          "symbol": "CHTR", "quote": quote(P10K[fy], lq)})
f["history_vintages"] = sorted(f["history_vintages"] + vintages, key=lambda v: v["published"])
f["prints"] = old["prints"] + prints
f["events"] = old["events"] + events
f["no_dividend"] += [{"published": V[fy]["published"], "source": sid, "quote": MODEL[fy]["no_dividend_quote"]} for sid, _, _, _, fy in TENK]
f["_doc"] = old["_doc"] + (" Extended with 2022-2026 by retro/generators/chtr/gen_chtr_2226.py: the FY2021-FY2025 10-K vintages (Item 6 "
                           "reserved: three years from each 10-K's statements of operations, earlier years carried from the latest earlier "
                           "vintage) with their one-off tests (every year kept at GAAP), the prints Q4 2021-Q3 2026 (Adjusted EBITDA from the "
                           "reconciliation of non-GAAP measures; the Cox Transactions in the Q3 2026 actual figures as published, pro forma "
                           "unused), the 10-Ks' streaming and AI words (retro/README.md, \"CHTR 2022-2026\").")
for k, v in old.items():
    if k in ("_doc", "sources", "history_vintages", "no_dividend", "prints", "events", "listings"):
        continue
    assert f[k] == v, k
assert all(f["sources"][k] == v for k, v in old["sources"].items())
assert [v for v in f["history_vintages"] if v["published"] <= PREV_CUT] == old["history_vintages"]
for k in ("no_dividend", "listings", "prints", "events"):
    assert f[k][:len(old[k])] == old[k], k
out = A.out or os.path.join(REPO, "retro", "facts", "CHTR.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(f, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
cl = A.checklist or os.path.join(SP, "checklist_chtr_2226.json")
with open(cl, "w", encoding="utf-8") as fh:
    json.dump(CHECK, fh, indent=1, ensure_ascii=False)
print(f"{out}: {len(f['sources']) - len(old['sources'])} new sources, {len(vintages)} vintages, {len(prints)} prints; checklist {cl}: "
      f"{sum(len(v) for v in CHECK.values())} strings")
for v in vintages:
    print(f"  {v['fy_label']} {v['published']}: " + ", ".join(f"{k} {p['eps_diluted']:.2f}" for k, p in v["periods"].items()))
for k in sorted(tests):
    if int(k) >= 2021:
        print(f"  test {k}: {tests[k]['note'][:200]}")
for p in prints:
    print(f"  {p['quarter']} {p['published']} {p['release_time']}: rev {p['sales_pct']:+.2f}% rel {p['rel_pct']:+.2f}% ocf {p['ocf_margin_bp']:+.1f}bp "
          f"capex {p['capex_bp']:+.1f}bp op {p['op_margin_bp']:+.1f}bp eps {p['eps_q']} vs {p['eps_q_prior']}")
