#!/usr/bin/env python3
"""Extend retro/facts/FANG.json with 2022-2026 (filings accepted 2022-01-01 to 2026-11-27), asserting every earlier fact is unchanged.

The discipline of gen_fang_1417.py and gen_fang_1821.py (retro/README.md, "FANG 2022-2026"): each figure from its own row by label under
an anchored heading, each quoted sentence asserted present in its own filing, every derived figure (growth rate, margin, one-off test)
computed here, and a verbatim checklist written. This batch appends the FY2021-FY2025 10-K vintages (Item 6 is reserved in each, so each
takes its statements' three years and carries the earlier years from the latest earlier vintage), the prints Q4 2021 to Q3 2026 (each
Q4 release's full year with its one-off test and its restated prior year), and the base dividend rates, each from the filing that first
states it. Rule T is not re-derived: it stays on the filings public on the first built date (2014-02-21; "FANG 2014-2017"). Run:

    python3 retro/tools/edgar.py index 1539838 <dir>
    python3 retro/tools/edgar.py fetch 1539838 <dir> --from 2021-12-01 --to 2026-11-28 --forms 10-K 10-K/A 8-K 8-K/A
    python3 -I retro/generators/fang/gen_fang_2226.py --filings <dir> [--facts-in <the 2008-2021 sheet>] [--out retro/facts/FANG.json]
    python3 -I retro/tools/verbatim.py <dir>/checklist_fang_2226.json

--facts-in is the 2008-2021 sheet (default retro/facts/FANG.json; facts published after 2021-12-31 are dropped first, so a re-run on
the extended sheet regenerates it byte for byte; gen_fang_1821.py run on the 2008-2017 sheet gives the 2008-2021 one). It only appends.
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
_ap.add_argument("--facts-in", help="the 2008-2021 fact sheet to extend (default retro/facts/FANG.json)")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/FANG.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_fang_2226.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402

ET = ZoneInfo("America/New_York")
PREV_CUT, CUT = "2021-12-31", "2026-11-27"
CIK = 1539838
FILINGS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("^GSPC")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
CHECK, TEXT = {}, {}
IN = A.facts_in or os.path.join(REPO, "retro", "facts", "FANG.json")
f = copy.deepcopy(json.load(open(IN, encoding="utf-8")))
# a re-run on the extended sheet: keep only the facts published by 2021-12-31 (this batch's own facts are all later)
later = {k for k, s in f["sources"].items() if s["published"] > PREV_CUT}
f["sources"] = {k: v for k, v in f["sources"].items() if k not in later}
f["history_vintages"] = [v for v in f["history_vintages"] if v["source"] not in later]
f["prints"] = [p for p in f["prints"] if p["source"] not in later]
f["dividends"] = [d for d in f["dividends"] if d["source"] not in later]
f["amendments"] = [a for a in f.get("amendments", []) if a["published"] <= PREV_CUT]
f["_doc"] = f["_doc"].split(" | 2022-2026:")[0]
OLD_IDS = set(f["sources"])
assert OLD_IDS == {f"FG{i}" for i in range(1, 15)} | {f"FG{i}" for i in range(20, 53)}, sorted(OLD_IDS)
assert len(f["dividends"]) == 6 and not f["guides"] and not f["events"] and not f["splits"]
OLD_SNAPSHOT = json.dumps(f, sort_keys=True)


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
    c = c.strip().replace(",", "").replace("$", "").replace(" ", "")
    if c in ("--", "—", "-", "―", "–"):
        return 0.0
    neg = c.startswith("(") and c.endswith(")")
    return -float(c.strip("()")) if neg else float(c.strip("()"))


def cells(x):
    out = []
    for c in x.split("|")[1:]:
        c = c.strip()
        if not c or c.endswith("%"):
            continue
        out.append(num(c))
    return out


def row(p, labels, after=None, n=None, start=0, stop=None):
    """The first row whose first cell is one of `labels` (from the first line at or after `start` that contains `after`), as numbers;
    the row goes on the checklist."""
    labels = (labels,) if isinstance(labels, str) else labels
    ls = lines(p)
    i0 = next(i for i, x in enumerate(ls) if i >= start and after.lower() in x.lower()) if after else start
    for i in range(i0, len(ls) if stop is None else stop):
        x = ls[i]
        if x.split("|")[0].strip() in labels:
            v = cells(x)
            assert n is None or len(v) >= n, (p, labels, v)
            CHECK.setdefault(p, []).append(x)
            return v, i
    raise AssertionError((p, labels, after))


def check_line(p, i, want):
    assert lines(p)[i] == want, (p, i, lines(p)[i], want)
    CHECK.setdefault(p, []).append(want)


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
FANG_INC = "Diamondback Energy, Inc."
EARLIER = {v["source"]: v for v in f["history_vintages"] if "eps_normalized" in v}
V20 = EARLIER["FG14"]

# ── the 10-K vintages FY2021-FY2025 ─────────────────────────────────────────────────────────────────────────────────────────────────
# Item 6 is "[Reserved]" in each, so each 10-K takes its statements of operations' three years; earlier years are carried from the
# latest earlier vintage (ten fiscal years to the latest, the FY2020 encoding of "FANG 2018-2021").
TENK = [("FG15", "0001539838-22-000008", "10-K__fang-20211231.rows.txt", 2021),
        ("FG16", "0001539838-23-000022", "10-K__fang-20221231.rows.txt", 2022),
        ("FG17", "0001539838-24-000019", "10-K__fang-20231231.rows.txt", 2023),
        ("FG18", "0001539838-25-000021", "10-K__fang-20241231.rows.txt", 2024),
        ("FG19", "0001539838-26-000010", "10-K__fang-20251231.rows.txt", 2025)]
BUSINESS = {y: ("We are an independent oil and natural gas company focused on the acquisition, development, exploration and exploitation of "
                "unconventional, onshore oil and natural gas reserves " + ("primarily " if y >= 2023 else "") + "in the Permian Basin in West Texas.")
            for y in range(2021, 2026)}
CYCLICAL = ("The oil and natural gas industry is cyclical, which can result in shortages of drilling rigs, equipment, raw materials "
            "(particularly sand and other proppants), supplies and personnel.")
PRICES = ("Our revenues, operating results, profitability, future rate of growth and the carrying value of our oil and natural gas "
          "properties depend significantly upon the prevailing prices for oil and natural gas.")
TRANSITION = ("Restrictions on emissions of methane or carbon dioxide that may be imposed could adversely impact the demand for, price of, "
              "and value of our products and reserves.")
CONSERVATION = "Conservation measures and technological advances could reduce demand for oil and natural gas."
FUEL = ("Fuel conservation measures, alternative fuel requirements, increasing consumer demand for alternatives to oil and natural gas, "
        "technological advances in fuel economy and energy generation devices could reduce demand for oil and natural gas.")
# EV's own words: none in the FY2021 10-K; from the FY2022 10-K the climate section names electric vehicles among the lower-emission
# products whose demand could reduce demand for oil and gas (the FY2025 10-K drops the two conservation sentences)
EV_WORDS = "lower-emission products and services (including electric vehicles and renewable residential and commercial power supplies)"
# the 10-Ks' AI words (GENAI, live 2022-11-30): none to the FY2023 10-K; identity fraud (FY2024) and AI in operations (FY2025), cyber risks
AI_WORDS = {2024: ("More recently, advancements in artificial intelligence (“AI”) may pose serious risks for many of the traditional tools used "
                   "to identify individuals, including voice recognition (whether by machine or the human ear), facial recognition or "
                   "screening questions to confirm identities."),
            2025: ("Additionally, the development, deployment and use of artificial intelligence (“AI”) and machine learning in our operations "
                   "and those of our service providers and partners could introduce new risks, including increased exposure to cybersecurity "
                   "threats and social engineering, inadvertent disclosure or misuse of confidential, proprietary or personal information, "
                   "errors, bias or other unexpected outcomes in AI outputs used for operational decision‑making, and evolving and "
                   "potentially divergent regulatory requirements that may restrict certain uses of AI or increase compliance costs.")}
GENAI_WORDS = {2024: "In addition, generative AI systems may also be used by malicious actors to create more sophisticated cyber-attacks (i.e., more realistic phishing or other attacks).",
               2025: "In addition, generative AI systems are increasingly used by malicious actors to create more sophisticated cyber-attacks (i.e., more realistic phishing or other attacks) and to circumvent controls, evade detection and even remove forensic evidence, rendering incident detection and remediation more challenging."}
DIV_10K = {2021: "Our capital return program is currently focused on our sustainable and growing base dividend and a combination of stock repurchases and variable dividends.",
           2025: "Our capital return program is currently focused on a sustainable and growing base dividend and opportunistic stock repurchases."}
DIV_10K[2022] = DIV_10K[2023] = DIV_10K[2021]
DIV_10K[2024] = "Our capital return program is currently focused on our sustainable base dividend and a combination of stock repurchases and variable dividends."
STMT_HDR = "(In millions, except per share amounts, shares in thousands)"
vintages, TENK_INFO = [], {}
for sid, acc, fname, fy in TENK:
    p = path(acc, fname)
    ls = lines(p)
    iso = next(i for i, x in enumerate(ls) if x in ("Consolidated Statements of Operations",
                                                     "Consolidated Statements of Operations and Comprehensive Income") and i > 1000
               and ls[i + 1] == "Year Ended December 31,")
    check_line(p, iso + 2, f"{fy} | {fy - 1} | {fy - 2}")
    check_line(p, iso + 3, STMT_HDR)
    i6 = max(i for i, x in enumerate(ls) if x.upper().startswith("ITEM 6. [RESERVED"))
    CHECK.setdefault(p, []).append(ls[i6])
    yrs, s0, nrow = [fy, fy - 1, fy - 2], iso, 3
    rev, _ = row(p, "Total revenues", start=s0, n=nrow)
    pti, _ = row(p, "Income (loss) before income taxes", start=s0, n=nrow)
    tax, _ = row(p, "Provision for (benefit from) income taxes", start=s0, n=nrow)
    ni, _ = row(p, "Net income (loss) attributable to Diamondback Energy, Inc.", start=s0, n=nrow)
    ie = next(i for i, x in enumerate(ls) if i > s0 and x == "Earnings (loss) per common share:")
    eps, _ = row(p, "Diluted", start=ie, n=nrow)
    iw = next(i for i, x in enumerate(ls) if i > s0 and x == "Weighted average common shares outstanding:")
    sh, _ = row(p, "Diluted", start=iw, n=nrow)
    def sales(lbl):
        v, _ = row(p, lbl, start=iso, stop=iso + 12, n=3)
        return v[:2]
    oil_s, gas_s, ngl_s = sales("Oil sales"), sales("Natural gas sales"), sales("Natural gas liquid sales")
    icf = next(i for i, x in enumerate(ls) if i > iso and x == "Consolidated Statements of Cash Flows" and ls[i + 1] == "Year Ended December 31,")
    ocf, _ = row(p, "Net cash provided by (used in) operating activities", start=icf, n=3)
    capex_l = ("Drilling, completions and infrastructure additions to oil and natural gas properties",
               "Drilling, completions, infrastructure and midstream additions to oil and natural gas properties",
               "Additions to oil and natural gas properties")
    capex = row(p, capex_l, start=icf, n=3)[0][0]
    whole = " ".join(ls).lower()
    quotes = {"business_quote": quote(p, BUSINESS[fy]), "cyclical_quote": quote(p, CYCLICAL), "prices_quote": quote(p, PRICES),
              "transition_quote": quote(p, TRANSITION), "dividend_quote": quote(p, DIV_10K[fy]),
              "conservation_quote": quote(p, CONSERVATION) if fy < 2025 else None,
              "fuel_quote": quote(p, FUEL) if fy < 2025 else None,
              "ev_quote": quote(p, EV_WORDS) if fy >= 2022 else None,
              "ai_words": [quote(p, AI_WORDS[fy]), quote(p, GENAI_WORDS[fy])] if fy in AI_WORDS else None}
    if fy == 2025:
        assert CONSERVATION.lower() not in whole and "fuel conservation measures, alternative fuel" not in whole, sid
    if fy == 2021:
        assert "electric vehicle" not in whole, sid
    if fy not in AI_WORDS:
        assert "artificial intelligence" not in whole, (sid, "AI words")
    if fy not in GENAI_WORDS:
        assert "generative" not in whole, (sid, "generative")
    for w in ("crypto", "blockchain", "bitcoin", "glp-1", "obesity"):   # CRYPTO's and GLP1's own words: none
        assert w not in whole, (sid, w)
    day, filed, _ = source(sid, acc, p, f"Diamondback FY{fy} 10-K",
                           f"the statements of operations, {fy - 2}-{fy} (Item 6 is reserved): total revenues, income (loss) before income "
                           "taxes, the provision for income taxes, net income (loss) attributable to Diamondback, diluted EPS and diluted "
                           "weighted average shares; the statements of operations (oil, natural gas and natural gas liquid sales) and cash "
                           "flows (net cash provided by operating activities, additions to oil and natural gas properties); Items 1, 1A and 5")
    periods = {}
    for i, y in enumerate(yrs):
        periods[str(y)] = {"issuer": FANG_INC, "start": f"{y}-01-01", "end": f"{y}-12-31", "months": 12,
                           "revenue_m": rev[i], "pretax_m": pti[i], "net_income_m": ni[i],
                           "eps_diluted": eps[i], "eps_pro_forma": None, "diluted_shares_m": round(sh[i] / 1000, 3), "tax_m": tax[i]}
    TENK_INFO[fy] = {"ocf_m": ocf[0], "capex_m": capex, "groups": (oil_s, ngl_s, gas_s)}
    v = {"published": day, "source": sid, "kind": "10-K", "fy_label": f"FY{fy % 100:02d}", "periods": periods,
         "eps_basis": ("GAAP diluted EPS as the statement of operations prints it, on net income (loss) attributable to Diamondback "
                       "Energy, Inc. (no discontinued operations in the years shown)" + ("; computed by the two-class method from the "
                       "FY2022 10-K, which restates 2021 and 2020" if fy >= 2022 else "")),
         "units": "USD millions", **quotes}
    vintages.append(v)
V = {fy: v for (_, _, _, fy), v in zip(TENK, vintages)}
assert [V[fy]["periods"][str(fy)]["eps_diluted"] for fy in V] == [12.30, 24.61, 17.34, 15.53, 5.73]
# the restatements: the FY2022 10-K restates 2021 ($12.30 to $12.24) and 2020 ($(28.59) to $(28.61)) by the two-class method; no other
# 10-K of the batch restates an earlier vintage's EPS (asserted)
RESTATED = {(2022, "2021"): (12.30, 12.24), (2022, "2020"): (-28.59, -28.61)}
for fy in V:
    for y, per in V[fy]["periods"].items():
        for v_ in [V20] + [V[g] for g in V if g < fy]:
            if y in v_["periods"] and v_["periods"][y]["eps_diluted"] is not None:
                old = v_["periods"][y]["eps_diluted"]
                if (fy, y) in RESTATED and v_ is (V20 if y == "2020" else V[2021]):
                    assert (old, per["eps_diluted"]) == RESTATED[(fy, y)], (fy, y)
                else:
                    assert old == per["eps_diluted"] or ((g := [g for g in RESTATED if g[1] == y]) and per["eps_diluted"] == RESTATED[g[0]][1]), (fy, y, old, per["eps_diluted"])
for fy in V:
    if fy > 2022:
        assert V[fy]["periods"].get("2021", {}).get("eps_diluted", 12.24) == 12.24
V[2022]["restates"] = {"2021": {"from": 12.30, "to": 12.24}, "2020": {"from": -28.59, "to": -28.61},
                       "note": quote(path("0001539838-23-000018", "EX-99.1__*.rows.txt"),
                                     "The Company’s earnings (loss) per diluted share amount has been computed using the two-class method in accordance with GAAP.")
                               + " (the Q4 2022 release's footnote; its prior-year column and the FY2022 10-K print 2021 at $12.24)"}


# ── the prints: each release's statement of operations and selected operating data, three months against the year-ago quarter ────
PRINTS = [  # quarter, fy, q, accession
    ("Q4 2021", 2021, 4, "0001193125-22-048650"), ("Q1 2022", 2022, 1, "0001539838-22-000054"),
    ("Q2 2022", 2022, 2, "0001539838-22-000127"), ("Q3 2022", 2022, 3, "0001539838-22-000163"),
    ("Q4 2022", 2022, 4, "0001539838-23-000018"), ("Q1 2023", 2023, 1, "0001539838-23-000042"),
    ("Q2 2023", 2023, 2, "0001539838-23-000098"), ("Q3 2023", 2023, 3, "0001539838-23-000129"),
    ("Q4 2023", 2023, 4, "0001539838-24-000013"), ("Q1 2024", 2024, 1, "0001539838-24-000088"),
    ("Q2 2024", 2024, 2, "0001539838-24-000147"), ("Q3 2024", 2024, 3, "0001539838-24-000195"),
    ("Q4 2024", 2024, 4, "0001539838-25-000016"), ("Q1 2025", 2025, 1, "0001539838-25-000063"),
    ("Q2 2025", 2025, 2, "0001539838-25-000124"), ("Q3 2025", 2025, 3, "0001539838-25-000144"),
    ("Q4 2025", 2025, 4, "0001539838-26-000006"), ("Q1 2026", 2026, 1, "0001539838-26-000073"),
    ("Q2 2026", 2026, 2, "0001539838-26-000137"), ("Q3 2026", 2026, 3, "0001539838-26-000180")]
# the Item 2.02 8-Ks without a release (each quarter's realized prices, derivatives and share counts; the 2022-04-07 cash settlement note;
# the operational updates of 2024-10-01 and 2025-04-16; the preliminary Q4 2023 operating results of 2024-02-12): no revenue, earnings or
# margin figure, so none is a print (the 8-K of 2021-04-12 encoding); asserted below
NOT_PRINTS = ["0001539838-22-000050", "0001539838-23-000034", "0001539838-23-000095", "0001539838-23-000126", "0001539838-24-000009",
              "0001140361-24-006881", "0001539838-24-000075", "0001539838-24-000144", "0001539838-24-000188", "0001539838-24-000191",
              "0001539838-25-000003", "0001539838-25-000058", "0001539838-25-000120", "0001539838-25-000141", "0001539838-26-000003",
              "0001539838-26-000070", "0001539838-26-000134", "0001539838-26-000177"]
rel_acc = {x[3] for x in PRINTS}
for r in FILINGS.values():
    if r[2].startswith("8-K") and PREV_CUT < r[0] <= CUT and "2.02" in (r[5] or ""):
        assert r[3] in rel_acc or r[3] in NOT_PRINTS, ("an Item 2.02 8-K not encoded", r[3])
for acc in NOT_PRINTS:
    docs = [q for sub in ("eightk",) for q in glob.glob(os.path.join(SP, sub, acc, "*.rows.txt")) if "R1" not in q]
    txt = " ".join(" ".join(lines(q)) for q in docs)
    for w in ("Total revenues", "Income (loss) before income taxes", "per diluted share", "Earnings (loss) per common share"):
        assert w not in txt, (acc, w)
PTI_L = ("Income (loss) before income taxes",)
EPS_H = ("Earnings (loss) per common share:",)
NEXT = {1: ("Q2", "early August"), 2: ("Q3", "early November"), 3: ("Q4", "February"), 4: ("Q1", "early May")}
MONTH_END = {1: "March 31", 2: "June 30", 3: "September 30", 4: "December 31"}
# The one-off test (the AAPL FY2002 test and its mirror), on the items each Q4 release's adjusted net income table removes besides the
# non-cash derivative marks (which recur, the NEE and PEP 2008 core rule), each at its twelve-month amount: from the statement of
# operations' line where the table is three months only (Q4 2021-Q4 2023) and the line exists, else the table's own three-month figure;
# from the table's year column where it has one (Q4 2024, Q4 2025). Charges and benefits pre-tax against income before income taxes.
ONE_OFFS = {
    2021: {"items": [("Merger and integration expense", "charge", "stmt", "Merger and integration expense"),
                     ("(Gain) loss on extinguishment of debt", "charge", "stmt", "Gain (loss) on extinguishment of debt"),
                     ("(Gain) loss on sale of property, plant and equipment", "benefit", "table3", None)]},
    2022: {"items": [("(Gain) loss on extinguishment of debt", "charge", "stmt", "Gain (loss) on extinguishment of debt"),
                     ("Merger and integration expense", "charge", "stmt", "Merger and integration expense"),
                     ("Other non-cash transactions", "charge", "table3", None)]},
    2023: {"items": [("Other non-cash transactions", "charge", "table3", None)]},
    2024: {"items": [("(Gain) loss on extinguishment of debt", "benefit", "table12", None),
                     ("Merger and integration expense", "charge", "table12", None),
                     ("Other non-cash transactions", "benefit", "table12", None)]},
    2025: {"items": [("(Gain) loss on extinguishment of debt", "benefit", "table12", None),
                     ("Impairment of oil and natural gas properties", "charge", "table12", None),
                     ("Other non-cash transactions", "benefit", "table12", None)]},
}
MARK = "Non-cash (gain) loss on derivative instruments, net"


def test_of(fy, pretax_m, charges_m, benefits_m, ni_m, eps, source_txt, items):
    loss = eps is not None and eps <= 0
    distorted = charges_m > pretax_m if charges_m >= benefits_m else benefits_m > pretax_m - benefits_m
    return {"fy": fy, "pretax_m": pretax_m, "listed_charges_m": charges_m, "listed_benefits_m": benefits_m,
            "income_attributable_m": ni_m, "eps_gaap": eps, "loss": loss, "distorted": bool(distorted and not loss),
            "kept": not loss and not distorted, "source": source_txt, "items": items}


prints = []
for k_, (quarter, fy, q, acc) in enumerate(PRINTS):
    p = path(acc, "EX-99.1__*.rows.txt")
    ls = lines(p)
    iso = next(i for i, x in enumerate(ls) if x in ("Consolidated Statements of Operations", "Condensed Consolidated Statements of Operations"))
    u = ls[iso + 1]
    assert u.startswith("(unaudited") and "in millions" in u, (quarter, u)
    CHECK.setdefault(p, []).append(u)
    ncol = 4 if q > 1 else 2
    rev, _ = row(p, "Total revenues", start=iso, n=ncol)
    pti, _ = row(p, PTI_L, start=iso, n=ncol)
    ie = next(i for i in range(iso, iso + 60) if ls[i] in EPS_H)
    eps, _ = row(p, "Diluted", start=ie, n=ncol)
    iw = next(i for i in range(ie, ie + 6) if ls[i] == "Weighted average common shares outstanding:")
    sh, _ = row(p, "Diluted", start=iw, n=ncol)
    iop = next(i for i, x in enumerate(ls) if x == "Selected Operating Data")
    ipd = next(i for i in range(iop, iop + 8) if ls[i] == "Production Data:")
    hdr = " | ".join(ls[iop + 2:ipd])
    for x in ls[iop + 2:ipd]:
        CHECK.setdefault(p, []).append(x)
    assert hdr.startswith("Three Months Ended") and (("Year Ended" in hdr) == (q == 4)), (quarter, hdr)
    yago = 1 if q == 4 else 2      # Q4: three months, year-ago quarter, the two years; Q1-Q3: this quarter, the last, the year-ago one
    if q != 4:
        assert hdr.count(str(fy - 1)) >= 1 and hdr.endswith(f"{MONTH_END[q]}, {fy - 1}"), (quarter, hdr)
    boe, _ = row(p, "Combined volumes (MBOE)(1)", start=iop, n=3)
    oil, _ = row(p, "Oil (MBbls)", start=iop, n=3)
    ic = next(i for i in range(ipd, ipd + 40) if ls[i] in ("Average Costs per BOE:", "Average Cash Costs ($/BOE):"))
    CHECK.setdefault(p, []).append(ls[ic])
    loe, _ = row(p, "Lease operating expenses", start=ic, stop=ic + 3, n=3)
    day, filed, when = source(f"FG{53 + k_}", acc, p, f"Diamondback {quarter} earnings release (8-K, exhibit 99.1)",
                              "Consolidated statements of operations (revenues, income before income taxes, diluted EPS and shares, three "
                              "months against the year-ago quarter) and selected operating data (oil and oil-equivalent production, lease "
                              "operating expense per BOE)" + ("; the twelve months and the adjusted net income table" if q == 4 else "")
                              + "; the dividend declaration")
    raw = {"rev_m": rev[0], "rev_prior_m": rev[1], "pti_m": pti[0], "pti_prior_m": pti[1], "eps_q": eps[0], "eps_q_prior": eps[1],
           "dil_sh_m": round(sh[0] / 1000, 3), "boe_k": boe[0], "boe_prior_k": boe[yago], "oil_k": oil[0], "oil_prior_k": oil[yago],
           "loe_boe": loe[0], "loe_boe_prior": loe[yago]}
    ptm, ptm_p = raw["pti_m"] / raw["rev_m"] * 100, raw["pti_prior_m"] / raw["rev_prior_m"] * 100
    nq, nmonth = NEXT[q]
    pr = {"quarter": quarter, "fy": fy, "q": q, "published": day, "source": f"FG{53 + k_}",
          "release": day, "release_time": f"accepted {filed}", "raw": raw, "sales_b": round(raw["rev_m"] / 1000, 4),
          "sales_pct": round(pct(raw["rev_prior_m"], raw["rev_m"]), 1),
          "production_pct": round(pct(raw["boe_prior_k"], raw["boe_k"]), 1), "oil_pct": round(pct(raw["oil_prior_k"], raw["oil_k"]), 1),
          "loe_boe_pct": round(pct(raw["loe_boe_prior"], raw["loe_boe"]), 1),
          "pretax_margin": round(ptm, 2), "pretax_margin_bp": round((ptm - ptm_p) * 100, 1),
          "next_print": f"{nq} {fy + (1 if q == 4 else 0)} release ({nmonth})"}
    if q == 4:   # the release's twelve months: the year joins the history from the release until the 10-K
        ni, _ = row(p, "Net income (loss) attributable to Diamondback Energy, Inc.", start=iso, n=4)
        ia = max(i for i, x in enumerate(ls) if x == "Adjusted Net Income" and i > iso)
        th = " | ".join(ls[ia + 2:ia + 4]) if ls[ia + 2] == "Three Months Ended | Year Ended" else ls[ia + 2]
        CHECK.setdefault(p, []).append(ls[ia + 2])
        twelve = "Year Ended" in th
        items, ch, be = [], 0.0, 0.0
        for lbl, kind, how, arg in ONE_OFFS[fy]["items"]:
            tv, _ = row(p, lbl, start=ia)                     # the table lists it
            if how == "stmt":                                 # the statement of operations' twelve-month line
                assert not twelve, quarter
                v_, _ = row(p, arg, start=iso, n=4)
                amt = abs(v_[2])
                sgn = v_[2] if "Gain (loss)" in arg else -v_[2]  # an expense line is a charge when positive
                assert (sgn < 0) == (kind == "charge"), (quarter, lbl)
            elif how == "table12":
                assert twelve, (quarter, "a twelve-month table")
                amt = abs(tv[2])
                assert (tv[2] > 0) == (kind == "charge"), (quarter, lbl, tv)   # an add-back is a charge, a deduction a benefit
            else:                                             # table3: the table's own three-month figure (no statement line)
                assert not twelve, quarter
                amt = abs(tv[0])
                assert (tv[0] > 0) == (kind == "charge"), (quarter, lbl, tv)
            items.append({"item": lbl, "kind": kind, "usd_m": round(amt, 3),
                          "basis": {"stmt": "twelve months, statement of operations",
                                    "table12": "twelve months, adjusted net income table",
                                    "table3": "three months, adjusted net income table (no twelve-month figure)"}[how]})
            ch, be = (ch + amt, be) if kind == "charge" else (ch, be + amt)
        row(p, MARK, start=ia)
        items.append({"item": MARK, "kind": "mark (recurring, left out)"})
        t = test_of(fy, pti[2], round(ch, 3), round(be, 3), ni[2], eps[2],
                    f"{quarter} release: the items its adjusted net income table removes besides the non-cash marks", items)
        pr["fy_actual"] = {"fy": fy, "eps_gaap": eps[2], "revenue_m": rev[2], "diluted_shares_m": round(sh[2] / 1000, 3),
                           "pretax_m": pti[2], "net_income_m": ni[2], "one_off_test": t,
                           "revenue_usd_b": round(rev[2] / 1000, 4), "pretax_margin": round(pti[2] / rev[2] * 100, 2),
                           "sales_growth": round(pct(rev[3], rev[2]), 1), "prior_eps_gaap": eps[3]}
    prints.append(pr)
P = {pr["quarter"]: pr for pr in prints}
for fy in (2021, 2022, 2023, 2024, 2025):        # the Q4 releases' years agree with the 10-Ks that follow them
    a, per = P[f"Q4 {fy}"]["fy_actual"], V[fy]["periods"][str(fy)]
    assert (a["eps_gaap"], a["revenue_m"], a["pretax_m"]) == (per["eps_diluted"], per["revenue_m"], per["pretax_m"]), (fy, a, per)
for fy in (2022, 2023, 2024, 2025):              # each Q4 release's prior year: the vintage public before it, or the restatement
    a, prev = P[f"Q4 {fy}"]["fy_actual"], V[fy - 1]["periods"][str(fy - 1)]
    assert abs(a["sales_growth"] - pct(prev["revenue_m"], a["revenue_m"])) < 0.06, fy
    assert a["prior_eps_gaap"] == (12.24 if fy == 2022 else prev["eps_diluted"]), fy
TESTS = {fy: P[f"Q4 {fy}"]["fy_actual"]["one_off_test"] for fy in (2021, 2022, 2023, 2024, 2025)}
assert [(TESTS[y]["kept"], TESTS[y]["loss"], TESTS[y]["distorted"]) for y in (2021, 2022, 2023, 2024, 2025)] == \
    [(True, False, False)] * 4 + [(False, False, True)], TESTS

EXCL = dict(V20["eps_excluded"])
EXCL_2020_RESTATED = ("a GAAP loss, $(28.61) diluted as the FY2022 10-K restates it by the two-class method ($(28.59) before), after "
                      "$6,021M of full cost ceiling impairments; no figure excludes only the one-offs (the company's adjusted net income "
                      "also removes the non-cash derivative marks; the loss rule)")
EXCL["2025"] = ("distorted: the $3,652M full cost ceiling impairment ($3,652M of listed one-off charges, against $532M of listed benefits: "
                "the debt extinguishment gain and other non-cash transactions) exceeds its $1,874M income before income taxes (the AAPL "
                "FY2002 test); the company's adjusted $13.37 also removes the non-cash derivative marks, which recur, so no figure "
                "excludes only the one-offs")
ALL_TESTS = {**{int(y): t for y, t in V20["one_off_tests"].items()}, **TESTS}

# ── each vintage's model fields: ten fiscal years to the latest, each year from the latest filing public on the vintage's date ──────
chain = [V20] + [V[fy] for fy in sorted(V)]
for n_, fy in enumerate(sorted(V), start=1):
    v = V[fy]
    prev = chain[n_ - 1]
    rev, eps_k, shares = {}, {}, {}
    for y, r in prev["revenue_usd_b"].items():
        rev[int(y)] = r
    for y, e in prev["eps_normalized"].items():
        eps_k[int(y)] = e
    for y, s in prev["diluted_shares_m"].items():
        shares[int(y)] = s
    for y, per in v["periods"].items():
        y = int(y)
        rev[y] = round(per["revenue_m"] / 1000, 4)
        shares[y] = per["diluted_shares_m"]
        if ALL_TESTS[y]["kept"]:
            eps_k[y] = per["eps_diluted"]
        else:
            eps_k.pop(y, None)
    keep = lambda d: {str(y): d[y] for y in sorted(d) if y > fy - 10}
    per = v["periods"]
    last_kept = max(y for y in eps_k)
    lk = (per.get(str(last_kept)) or next(c["periods"][str(last_kept)] for c in reversed(chain[:n_]) if str(last_kept) in c["periods"]))
    info = TENK_INFO[fy]
    (o, ng, g) = info["groups"]
    excl = {y: (EXCL_2020_RESTATED if y == "2020" and fy >= 2022 else t) for y, t in EXCL.items() if fy - 10 < int(y) <= fy}
    v.update({
        "eps_normalized": keep(eps_k),
        "eps_excluded": excl,
        "revenue_usd_b": keep(rev),
        "diluted_shares_m": keep(shares),
        "normalization": ("GAAP diluted EPS on net income attributable to Diamondback; " + "; ".join(
            f"FY{y[2:]} excluded: {t}" for y, t in excl.items())),
        "revenue_note": (f"total revenues, each year from the latest filing that reports it ({min(y for y in rev if y > fy - 10)}-{fy - 3} "
                         f"carried from earlier vintages; {fy - 2}-{fy} from the FY{fy} 10-K's statements of operations, Item 6 being "
                         "reserved)"),
        "shares_note": "diluted weighted average shares, M, each year from the latest filing",
        "carried_from": f"the years this 10-K does not report, from the {prev['fy_label']} vintage ({prev['source']}), each from the latest filing that reported it",
        "prev_fy_pretax_margin": round(per[str(fy)]["pretax_m"] / per[str(fy)]["revenue_m"] * 100, 2),
        "check_year": last_kept,
        "check_pretax_margin": round(lk["pretax_m"] / lk["revenue_m"] * 100, 2),
        "tax_rate": round(lk["tax_m"] / lk["pretax_m"], 4),
        "prev_fy_sales_growth": round(pct(rev[fy - 1] * 1000, rev[fy] * 1000), 1),
        "groups": [["Oil sales", round(o[0] / 1000, 4), round(pct(o[1], o[0]), 1)],
                   ["Natural gas liquid sales", round(ng[0] / 1000, 4), round(pct(ng[1], ng[0]), 1)],
                   ["Natural gas sales", round(g[0] / 1000, 4), round(pct(g[1], g[0]), 1)]],
        "groups_basis": f"{fy} oil, natural gas liquid and natural gas sales (the statement of operations)",
        "fcf_b": round((info["ocf_m"] + info["capex_m"]) / 1000, 4),
        "fcf_note": (f"(net cash provided by operating activities ${info['ocf_m'] / 1000:.3f}B less additions to oil and natural gas "
                     f"properties ${-info['capex_m'] / 1000:.3f}B; acquisitions and midstream additions not deducted)"),
        "fcf_label": f"FY{fy % 100:02d}",
        "one_off_tests": {str(y): ALL_TESTS[y] for y in sorted(ALL_TESTS) if fy - 10 < y <= fy},
    })

# ── dividends: each annual base rate from the filing that first states it; the variable dividends (from Q1 2022, each set on the prior
# quarter's free cash flow) are not a rate (the LYB and NEM specials rule) ────────────────────────────────────────────────────────────
DIVS = [("Q4 2021", 2.40, "Increasing annual dividend by 20.0% to $2.40 per share; declared Q4 2021 cash dividend of $0.60 per share payable on March 11, 2022"),
        ("Q1 2022", 2.80, "Increasing annual base dividend by 17% to $2.80 per share; declared Q1 2022 base cash dividend of $0.70 per share payable on May 23, 2022"),
        ("Q2 2022", 3.00, "As previously announced, increasing annual base dividend by 7% to $3.00 per share; declared Q2 2022 base cash dividend of $0.75 per share payable on August 23, 2022"),
        ("Q4 2022", 3.20, "Increasing annual base dividend by 7% to $3.20 per share; declared Q4 2022 base cash dividend of $0.80 per share payable on March 10, 2023"),
        ("Q2 2023", 3.36, "Increasing annual base dividend by 5% to $3.36 per share; declared Q2 2023 base cash dividend of $0.84 per share payable on August 17, 2023"),
        ("FG73", 3.60, "Diamondback today also announced that the Company’s Board of Directors will approve a 7% increase to its base dividend to $3.60 per share annually ($0.90 per share quarterly), effective for the fourth quarter of 2023."),
        ("Q4 2024", 4.00, "Increased annual base dividend by 11% to $4.00 per share; declared Q4 2024 base cash dividend of $1.00 per share payable on March 13, 2025"),
        ("Q4 2025", 4.20, "Increased annual base dividend by 5% to $4.20 per share; declared Q4 2025 base cash dividend of $1.05 per share payable on March 12, 2026"),
        ("FG74", 4.40, "Today, we are increasing our base dividend by 5% to $4.40 per share annually, now up 10% this year."),
        ("Q3 2026", 4.72, "Increased annual base dividend by 7.3% to $4.72 per share")]
# the two dividend statements outside a release's exhibit 99.1: the Endeavor merger 8-K's exhibit 99.2 (2024-02-12, before the open) and
# the Q1 2026 release 8-K's exhibit 99.2, the stockholder letter
p73 = path("0001140361-24-006881", "EX-99.2__*.rows.txt")
source("FG73", "0001140361-24-006881", p73, "Diamondback 8-K of 2024-02-12 (a merger announcement), exhibit 99.2",
       "the base dividend increase to $3.60 a year (and, in Item 2.02, preliminary Q4 2023 operating results: no revenue, earnings or margin)")
p74 = path("0001539838-26-000073", "EX-99.2__*.rows.txt")
source("FG74", "0001539838-26-000073", p74, "Diamondback Q1 2026 stockholder letter (8-K, exhibit 99.2)",
       "the base dividend increase to $4.40 a year")
DPATH = {"FG73": p73, "FG74": p74}
NOTE = {"FG73": "merger 8-K of 2024-02-12", "FG74": "Q1 2026 stockholder letter"}
dividends = []
for key, annual, qt in DIVS:
    if key in DPATH:
        sid, p, pub, where = key, DPATH[key], f["sources"][key]["published"], NOTE[key]
    else:
        pr = P[key]
        sid, p, pub, where = pr["source"], path(PRINTS[[x[0] for x in PRINTS].index(key)][3], "EX-99.1__*.rows.txt"), pr["published"], f"{key} release"
    dividends.append({"published": pub, "source": sid, "annual": annual, "quarterly": round(annual / 4, 4),
                      "quote": quote(p, qt), "note": f"${annual:.2f} a year (${annual / 4:.4g} a quarter, base), the {where}"})
assert all(", the " not in d["note"].split(", the ", 1)[1] for d in dividends)
# the base rate in force agrees with each release's base declaration; the variable dividends are declared beside it (not a rate)
for qq, s in (("Q3 2022", "base cash dividend of $0.75"), ("Q1 2023", "base cash dividend of $0.80"), ("Q4 2023", "base cash dividend of $0.90 per share and a variable cash dividend of $2.18 per share"),
              ("Q3 2024", "base cash dividend of $0.90"), ("Q2 2026", "base cash dividend of $1.10 per common share")):
    quote(path(PRINTS[[x[0] for x in PRINTS].index(qq)][3], "EX-99.1__*.rows.txt"), s)

# ── write ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
f["history_vintages"] += vintages
f["prints"] += prints
f["dividends"] = f["dividends"] + sorted(dividends, key=lambda d: d["published"])
f["_doc"] = (f["_doc"] + " | 2022-2026: extended by retro/generators/fang/gen_fang_2226.py with the FY2021-FY2025 10-K vintages, the "
             "prints Q4 2021-Q3 2026 with each Q4 release's year, its one-off test and its prior year, and the base dividend rates "
             "(retro/README.md, \"FANG 2022-2026\").")
new = json.loads(json.dumps(f))
old = json.loads(OLD_SNAPSHOT)
for kk in old:                                   # every earlier fact unchanged: only appended
    if isinstance(old[kk], list):
        assert new[kk][:len(old[kk])] == old[kk], kk
    elif isinstance(old[kk], dict):
        assert all(new[kk][x] == old[kk][x] for x in old[kk]), kk
    elif kk != "_doc":
        assert new[kk] == old[kk], kk
for s in f["sources"].values():
    assert s["published"] <= CUT
out = A.out or os.path.join(REPO, "retro", "facts", "FANG.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(f, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_fang_2226.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump({p: sorted(set(v)) for p, v in CHECK.items()}, fh, ensure_ascii=False, indent=1)
print(f"{out}: {len(vintages)} vintages, {len(prints)} prints, {len(dividends)} dividends; checklist {ck}: "
      f"{sum(len(set(v)) for v in CHECK.values())} strings")
for pr in prints:
    print(pr["quarter"], pr["published"], pr["release_time"], pr["sales_pct"], pr["production_pct"], pr["oil_pct"], pr["loe_boe_pct"],
          pr["pretax_margin"], pr["pretax_margin_bp"], pr["raw"]["eps_q"], pr["raw"]["eps_q_prior"], pr["raw"]["dil_sh_m"])
for fy, t in TESTS.items():
    print(fy, {k: t[k] for k in ("pretax_m", "listed_charges_m", "listed_benefits_m", "eps_gaap", "kept", "distorted", "loss")})
for v in vintages:
    print(v["source"], v["published"], v["eps_normalized"], list(v["eps_excluded"]), v["revenue_usd_b"], v["diluted_shares_m"],
          v["tax_rate"], v["check_year"], v["fcf_b"], v["prev_fy_sales_growth"])
for d in dividends:
    print(d["published"], d["annual"], d["source"])
