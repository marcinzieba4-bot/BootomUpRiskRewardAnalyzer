#!/usr/bin/env python3
"""Extend retro/facts/TRGP.json with 2014-2017 (filings accepted 2013-12-31 to 2017-12-31), asserting that every earlier fact is unchanged.

The discipline of the 2012-2013 sheet (gen_trgp.py; retro/README.md, "TRGP from the first full year"): each figure from its own row by
label under an anchored heading, each quoted sentence asserted present in its own filing, every rate, margin, tax rate and growth figure
computed, a verbatim checklist written. Read: the sixteen earnings releases from Q4 2013 to Q3 2017 (joint releases of Targa Resources
Partners LP and TRC to Q4 2015, TRC's own from Q1 2016, after TRC acquired the Partnership's public common units on 2016-02-17), the
FY2013-FY2016 10-Ks, the 8-K of 2016-05-23 recasting the FY2015 10-K's Items 1, 6, 7 and 8 for the two-segment reporting (a vintage of
its own), the 8-K of 2014-10-23 revising revenues for the NGL buy-sell transactions (a restatement of its own date), the 10-Qs of 2016-2017
(the releases from Q1 2016 print no EPS or share count; the 10-Q, or the FY2016 10-K's quarterly data for Q4 2016, gives them from its own
date) and the dividend outlooks of the 8-Ks of 2014-10-14 (the Atlas mergers) and 2015-11-03 (the buy-in), display only. Run:

    python3 retro/tools/edgar.py index 1389170 <dir>
    python3 retro/tools/edgar.py fetch 1389170 <dir> --from 2010-09-01 --to 2017-12-31 --forms 10-K 10-Q 8-K 10-K/A 8-K/A 10-Q/A 424B1
    python3 -I retro/generators/trgp/gen_trgp.py --filings <dir> --out <scratch>/TRGP_1213.json      # the 2012-2013 sheet
    python3 -I retro/generators/trgp/gen_trgp_1417.py --filings <dir> --facts-in <scratch>/TRGP_1213.json
    python3 -I retro/tools/verbatim.py <dir>/checklist_trgp_1417.json

--facts-in is the 2012-2013 sheet (default retro/facts/TRGP.json, which must then hold no fact published after 2013-12-31; the generator
refuses a sheet that already holds one). It only appends.
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
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))       # retro/generators/trgp -> the repository
_ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("--filings", required=True, help="folder edgar.py wrote (allrows.json, tenk/, tenq/, eightk/); keep it outside the repo")
_ap.add_argument("--facts-in", help="the 2012-2013 fact sheet to extend (default retro/facts/TRGP.json)")
_ap.add_argument("--out", help="fact sheet to write (default retro/facts/TRGP.json)")
_ap.add_argument("--checklist", help="verbatim checklist to write (default <filings>/checklist_trgp_1417.json)")
A = _ap.parse_args()
SP = os.path.abspath(A.filings)
sys.path.insert(0, os.path.join(REPO, "retro"))
import retro_tool  # noqa: E402  (the repo's own tool: trading days from the Yahoo cache)

ET = ZoneInfo("America/New_York")
START, CUT = "2013-12-31", "2017-12-31"
CIK = 1389170
FILINGS = {r[3]: r for r in json.load(open(os.path.join(SP, "allrows.json")))}
chart = retro_tool.chart("TRGP")
off = chart["meta"]["gmtoffset"]
TDAYS = sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})
CHECK = {}

FIN = A.facts_in or os.path.join(REPO, "retro", "facts", "TRGP.json")
with open(FIN, encoding="utf-8") as fh:
    facts = json.load(fh)
BEFORE = copy.deepcopy(facts)
_later = [p["published"] for k in ("prints", "history_vintages", "guides", "dividends") for p in facts[k] if p["published"] > START]
assert not _later, ("the input sheet already holds facts after 2013-12-31", _later[:3])


def norm(s):
    return re.sub(r"\s+", " ", s.replace(" ", " ")).strip()


def doc(acc, prefix):
    for sub in ("tenk", "tenq", "eightk", "other"):
        d = os.path.join(SP, sub, acc)
        if os.path.isdir(d):
            hits = sorted(f for f in os.listdir(d) if f.startswith(prefix) and f.endswith(".rows.txt"))
            assert len(hits) == 1, (acc, prefix, hits)
            return os.path.join(d, hits[0])
    raise AssertionError(acc)


TEXT, ORIG = {}, {}


def lines(path):
    if path not in TEXT:
        with open(path, encoding="utf-8", errors="replace") as fh:
            ORIG[path] = [norm(x) for x in fh.read().split("\n")]
        # the releases from Q2 2016 split a negative percentage over two cells: "(7 | %)" -> "(7%)" (the checklist keeps the original row)
        TEXT[path] = [re.sub(r"\((\d+) \| %\)", r"(\1%)", x) for x in ORIG[path]]
    return TEXT[path]


def quote(path, s):
    """Assert a sentence or fragment is in its filing, word for word; add it to the checklist."""
    full = norm(" ".join(lines(path)))
    assert norm(s) in full, (path, s[:120])
    CHECK.setdefault(path, []).append(s)
    return s


def num(tok):
    t = tok.strip().replace("$", "").replace(",", "").strip()
    if t in ("—", "-", "–", ""):
        return 0.0
    neg = t.startswith("(") and t.endswith(")")
    v = float(t.strip("()%"))
    return -v if neg else v


DASH = lambda t: t.replace("—", "-").replace("–", "-")


def row(path, labels, start=0, stop=None):
    """The unique row in lines[start:stop] whose first cell is one of `labels` (dashes normalized); (row, numeric values)."""
    labels = [labels] if isinstance(labels, str) else labels
    key = lambda x: re.sub(r"\s*-\s*", "-", DASH(x.split(" |")[0].strip()))
    want = {re.sub(r"\s*-\s*", "-", DASH(lb)) for lb in labels}
    L = lines(path)
    stop = len(L) if stop is None else stop
    hits = [k for k in range(start, min(stop, len(L))) if "|" in L[k] and key(L[k]) in want]
    assert len(hits) == 1, (path, labels, len(hits), [L[k] for k in hits[:3]], start, stop)
    r = L[hits[0]]
    vals = [None if t.strip() == "NM" else num(t) for t in r.split("|")[1:] if t.strip()]
    CHECK.setdefault(path, []).append(ORIG[path][hits[0]])
    return r, vals


def line_no(path, pred, start=0):
    L = lines(path)
    return next(i for i in range(start, len(L)) if pred(L[i]))


def next_tday(d):
    return min(x for x in TDAYS if x > d)


def published(acc):
    """Publication date from EDGAR's acceptance time (UTC -> ET); at or after the 16:00 ET close, the next trading day."""
    r = FILINGS[acc]
    t = dt.datetime.fromisoformat(r[1].replace("Z", "+00:00")).astimezone(ET)
    d = t.date().isoformat()
    hm = t.strftime("%H:%M")
    if hm >= "16:00":
        return next_tday(d), f"accepted {d} {hm} ET (after the close), so dated the next trading day"
    if d not in TDAYS:
        return next_tday(d), f"accepted {d} {hm} ET (not a trading day), so dated the next trading day"
    if hm < "09:30":
        return d, f"accepted {d} {hm} ET (before the open)"
    return d, f"accepted {d} {hm} ET (during market hours)"


URL = lambda acc, fn: f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc.replace('-', '')}/{fn}"
SRC = facts["sources"]


def source(sid, acc, title, path, supports):
    assert sid not in SRC, sid
    p, filed = published(acc)
    assert START < p <= CUT, (sid, p)
    fn = os.path.basename(path).split("__", 1)[1].replace(".rows.txt", ".htm")
    SRC[sid] = dict(published=p, filed=filed, title=title, url=URL(acc, fn), supports=supports)
    return sid


usd_m = lambda v: f"${v:,.1f}M" if v >= 0 else f"$({-v:,.1f})M"
pct = lambda a, b: round((b / a - 1) * 100, 1) if a > 0 else round((b - a) / abs(a) * 100, 1) if a < 0 else None
mg = lambda x, rev: round(x / rev * 100 + 0.0, 2)
bp = lambda x, rev, x0, rev0: round((mg(x, rev) - mg(x0, rev0)) * 100, 1)
eps_s = lambda v: "n/r" if v is None else (f"${v:.2f}" if v >= 0 else f"$({-v:.2f})")

# ── filings ─────────────────────────────────────────────────────────────────────
REL = {"Q4 2013": "0001193125-14-049564", "Q1 2014": "0001193125-14-174497", "Q2 2014": "0001193125-14-290597",
       "Q3 2014": "0001193125-14-395016", "Q4 2014": "0001193125-15-048196", "Q1 2015": "0001193125-15-170129",
       "Q2 2015": "0001193125-15-275681", "Q3 2015": "0001193125-15-363317", "Q4 2015": "0001193125-16-476903",
       "Q1 2016": "0001564590-16-017060", "Q2 2016": "0001564590-16-022182", "Q3 2016": "0001564590-16-026838",
       "Q4 2016": "0001564590-17-001585", "Q1 2017": "0001564590-17-008555", "Q2 2017": "0001564590-17-015106",
       "Q3 2017": "0001564590-17-020974"}
FREL = {q: doc(a, "EX-99.1__") for q, a in REL.items()}
SID = {q: f"TG{40 + i}" for i, q in enumerate(REL)}
JOINT = [q for q in REL if (int(q[3:]), int(q[1])) <= (2015, 4)]        # joint releases with the Partnership to Q4 2015
K13, K14, K15, K16 = "0001140361-14-007923", "0001140361-15-006704", "0001140361-16-055579", "0001564590-17-001810"
R15 = "0001193125-16-598296"                                            # the 8-K of 2016-05-23 recasting the FY2015 10-K
REV8K = "0001193125-14-379565"                                          # the 8-K of 2014-10-23 revising revenues
ATLAS8K, BUYIN8K = "0001193125-14-370752", "0001193125-15-363295"
TENQ = {"Q1 2016": "0001564590-16-018893", "Q2 2016": "0001564590-16-022169", "Q3 2016": "0001564590-16-027687",
        "Q1 2017": "0001564590-17-008688", "Q2 2017": "0001564590-17-015398", "Q3 2017": "0001564590-17-021452"}

# ── release tables ──────────────────────────────────────────────────────────────


def trc_block(path):
    """(start, stop) of TRC's consolidated statement of operations in a joint release (the Partnership's comes first)."""
    L = lines(path)
    i = next(i for i in range(len(L)) if L[i] == "CONSOLIDATED STATEMENTS OF OPERATIONS" and
             any(L[j].upper() == "TARGA RESOURCES CORP." for j in range(i - 3, i)))
    j = next((k for k in range(i + 1, len(L)) if L[k].upper() == "TARGA RESOURCES CORP."), i + 45)
    return i, min(j, i + 45)


NI_TRC = ["NET INCOME AVAILABLE TO COMMON SHAREHOLDERS", "Net income available to common shareholders"]
EPS_D = ["Net income available per common share - diluted"]
SH_D = ["Weighted average shares outstanding - diluted"]
REV_L = ["REVENUES", "Total revenues"]
PTI_L = ["Income before income taxes", "Income (loss) before income taxes"]
NI_L = ["NET INCOME", "NET INCOME (LOSS)"]


def ops_joint(path):
    i, j = trc_block(path)
    vals = {}
    for k, labs in (("rev", REV_L), ("oi", ["INCOME FROM OPERATIONS"]), ("pti", PTI_L), ("ni", NI_L), ("nia", NI_TRC),
                    ("eps", EPS_D), ("sh", SH_D)):
        vals[k] = row(path, labs, i, j)[1]
    return vals


def ops_trc(path, yr):
    """TRC's own releases (from Q1 2016): the summary table at the top; income before income taxes is net income less the income tax
    line (the table prints no pre-tax row; the LYB 2018 derivation); no EPS or share count."""
    L = lines(path)
    i = line_no(path, lambda x: x.startswith("Total revenues |"))
    j = i + 40
    take = lambda v: (v[0], v[1], v[4], v[5]) if yr else (v[0], v[1])
    vals = {"rev": take(row(path, "Total revenues", i, j)[1]), "oi": take(row(path, "Income from operations", i, j)[1]),
            "ni": take(row(path, "Net income (loss)", i, j)[1]),
            "tax": take(row(path, "Income tax (expense) benefit", i, j)[1]),
            "nia": take(row(path, "Net income (loss) attributable to common shareholders", i, j)[1])}
    vals["pti"] = tuple(round(n - t, 1) for n, t in zip(vals["ni"], vals["tax"]))
    return vals


SEGS4 = ("Field Gathering and Processing", "Coastal Gathering and Processing", "Logistics Assets", "Marketing and Distribution")


def seg_joint(path):
    """The four segments' operating margin rows, in order, after the release's 'Review of Segment Performance'."""
    L = lines(path)
    i0 = line_no(path, lambda x: "Review of Segment Performance" in x and "|" not in x and len(x) < 80)
    idx = [k for k in range(i0, len(L)) if L[k].startswith("Operating margin |")][:4]
    out = []
    for name, k in zip(SEGS4, idx):
        head = next(m for m in range(k, i0, -1) if L[m].startswith(name))       # the segment's own heading above the row
        assert k - head < 15, (path, name)
        out.append(row(path, "Operating margin", k, k + 1)[1])
    return (out[0][0] + out[1][0], out[0][1] + out[1][1]), (out[2][0] + out[3][0], out[2][1] + out[3][1])


def seg_trc(path):
    """From Q1 2016 the two segments (the former divisions): each one's first 'Operating margin' row under its own heading."""
    out = []
    for name in ("Gathering and Processing Segment", "Logistics and Marketing Segment"):
        h = line_no(path, lambda x: x == name)
        k = line_no(path, lambda x: x.startswith("Operating margin |"), h)
        assert k - h < 15, (path, name)
        v = row(path, "Operating margin", k, k + 1)[1]
        out.append((v[0], v[1]))
    return out[0], out[1]


def sentence(path, pattern):
    full = norm(" ".join(lines(path)))
    m = re.search(pattern, full)
    assert m, (path, pattern)
    return quote(path, m.group(0))


# ── prints ──────────────────────────────────────────────────────────────────────
QDATE = {1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"}
prints, dividends = [], []
for q, acc in REL.items():
    f = FREL[q]
    qn, fy = int(q[1]), int(q[3:])
    joint = q in JOINT
    if joint:
        o = ops_joint(f)
        gp, lm = seg_joint(f)
    else:
        o = ops_trc(f, qn == 4)
        gp, lm = seg_trc(f)
    call = sentence(f, r"will host a (?:joint )?conference call for (?:investors and analysts|the investment community) at [^.]*? (a\.m\.|p\.m\.) Eastern [Tt]ime")
    pub, filed = published(acc)
    title = (f"Targa Resources Partners LP and Targa Resources Corp. {q} results (8-K, Exhibit 99.1)" if joint else
             f"Targa Resources Corp. {q} results (8-K, Exhibit 99.1)")
    source(SID[q], acc, title, f, ("Targa Resources Corp.'s consolidated statement of operations (revenues, income from operations, "
                                   "income before income taxes, net income available to common shareholders, diluted EPS and shares) "
                                   "and the Partnership's segment operating margins" if joint else
                                   "Targa Resources Corp.'s consolidated results (revenues, income from operations, net income and the "
                                   "income tax line, net income attributable to common shareholders; no EPS or share count) and its "
                                   "two segments' operating margins") +
           ", each with the year-ago quarter as this release shows it; the TRC dividend declared")
    eps, eps0, sh = (o["eps"][0], o["eps"][1], o["sh"][0]) if joint else (None, None, None)
    raw = {"rev_m": o["rev"][0], "rev_prior_m": o["rev"][1], "oi_m": o["oi"][0], "oi_prior_m": o["oi"][1],
           "pti_m": o["pti"][0], "pti_prior_m": o["pti"][1], "eps_q": eps, "eps_q_prior": eps0,
           "dil_sh_m": sh, "gp_m": round(gp[0], 1), "gp_prior_m": round(gp[1], 1), "lm_m": round(lm[0], 1),
           "lm_prior_m": round(lm[1], 1), "nia_m": o["nia"][0]}
    segname = (("Natural Gas Gathering and Processing (Field and Coastal) operating margin", "Logistics and Marketing (Logistics Assets "
                "and Marketing and Distribution)", "(the Partnership's segments, consolidated by TRC)") if joint else
               ("Gathering and Processing segment operating margin", "Logistics and Marketing segment",
                "(TRC's two segments from 2016, the former divisions; the year-ago quarter as the release recasts it)"))
    pr = {"quarter": q, "fy": fy, "q": qn, "published": pub, "source": SID[q],
          "release": dt.date.fromisoformat(pub).strftime("%b %-d"),
          "release_time": f"8-K {filed}; {call}", "period_end": f"{fy}-{QDATE[qn]}", "raw": raw,
          "sales_b": round(raw["rev_m"] / 1000, 3), "sales_pct": pct(raw["rev_prior_m"], raw["rev_m"]),
          "opm": mg(raw["oi_m"], raw["rev_m"]), "opm_bp": bp(raw["oi_m"], raw["rev_m"], raw["oi_prior_m"], raw["rev_prior_m"]),
          "ptm": mg(raw["pti_m"], raw["rev_m"]), "ptm_bp": bp(raw["pti_m"], raw["rev_m"], raw["pti_prior_m"], raw["rev_prior_m"]),
          "eps_q": eps, "eps_q_prior": eps0, "diluted_shares_m": sh,
          "gp_pct": pct(raw["gp_prior_m"], raw["gp_m"]), "lm_pct": pct(raw["lm_prior_m"], raw["lm_m"]),
          "seg_note": f"{segname[0]} {usd_m(gp[0])} vs {usd_m(gp[1])}, {segname[1]} {usd_m(lm[0])} vs {usd_m(lm[1])} {segname[2]}",
          "sales_note": f"revenues {usd_m(raw['rev_m'])} vs {usd_m(raw['rev_prior_m'])}",
          "margin_note": (f"income from operations {usd_m(raw['oi_m'])} vs {usd_m(raw['oi_prior_m'])}; income before income taxes "
                          f"{usd_m(raw['pti_m'])} vs {usd_m(raw['pti_prior_m'])}" +
                          ("" if joint else " (net income less the income tax line)")),
          "eps_note": (f"GAAP, diluted, {eps_s(eps)} against {eps_s(eps0)} a year earlier" if joint else
                       "GAAP, diluted: not in the release (TRC's releases from Q1 2016 print no per-share figure); net income "
                       f"attributable to common shareholders {usd_m(o['nia'][0])} vs {usd_m(o['nia'][1])}"),
          "next_print": f"the Q{qn % 4 + 1} {fy + (1 if qn == 4 else 0)} release"}
    full = norm(" ".join(lines(f)))
    m = (re.search(r"The Company’s distributable cash flow for the (?:fourth|third|second|first) quarter \d{4} was \$([\d.]+) million", full)
         or re.search(r"The Company reported distributable cash flow for the (?:fourth|third|second|first) quarter of \d{4} of "
                      r"\$([\d.]+) million", full))
    assert m, (q, "TRC distributable cash flow")
    quote(f, m.group(0))
    pr["cash_note"] = f"TRC distributable cash flow ${float(m.group(1)):.1f}M (non-GAAP, display only)"
    dm = re.search(r"TRC declared a quarterly dividend of (\$[\d.]+) per share of its common stock for the three months ended "
                   r"[A-Za-z]+ \d+, \d{4}", full)
    assert dm, (q, "dividend")
    quote(f, dm.group(0))
    rate = float(dm.group(1).strip("$"))
    dividends.append({"published": pub, "source": SID[q], "quarterly": round(rate, 5),
                      "note": f"${rate:.5f}".rstrip("0").rstrip(".") + f" a quarter, declared for {q} (the {q} release)",
                      "quote": dm.group(0)})
    if qn == 4:                                   # the year: the release's year columns
        yr = {k: v[2] for k, v in o.items()}
        yr0 = {k: v[3] for k, v in o.items()}
        tax = round(yr["pti"] - yr["ni"], 1)
        if fy == 2013:
            quote(f, "The increase in other income was attributable to the elimination of the contingent consideration associated with "
                     "the Badlands acquisition, reflecting management’s current assessment that the stipulated volumetric thresholds "
                     "will not be met.")
            i, j = trc_block(f)
            lo = row(f, "Loss on debt redemption and early debt extinguishments", i, j)[1][2]
            ot = row(f, "Other expenses", i, j)[1][2]
            items = round(-lo - ot, 1)                 # the Partnership's $14.7M loss on redemptions less the $15.3M gain: a net benefit
            note = ("the release lists no one-off item of TRC's; the Partnership's $14.7 million of losses on debt redemptions and its "
                    "$15.3 million gain from eliminating the Badlands contingent consideration (pre-tax, before the noncontrolling "
                    "interests) net to a $0.6 million benefit, far under the year's net income available to common shareholders")
        elif fy == 2014:
            quote(f, "Other expense in 2014 was primarily attributable to transaction costs related to the pending Atlas Mergers.")
            quote(f, "The redemption resulted in a $12.4 million loss on debt redemption, including premiums paid and non-cash write-offs "
                     "of unamortized debt issue costs.")
            i, j = trc_block(f)
            lo = row(f, "Gain (loss) on debt redemption and amendments", i, j)[1][2]
            ot = row(f, "Other", i, j)[1][2]
            items = round(-lo - ot, 1)
            note = ("the release lists no one-off item of TRC's; the Partnership's $12.4 million loss on the redemption of its 7 7/8% "
                    "notes and the year's $8.0 million of other expense, 'primarily attributable to transaction costs related to the "
                    "pending Atlas Mergers', even all credited to TRC (pre-tax, before the noncontrolling interests), are under the "
                    "year's net income available to common shareholders")
        elif fy == 2015:
            g = quote(f, "For the full year 2015, net income attributable to common shareholders before impairment of goodwill was "
                         "$83.9 million compared to $102.3 million for 2014.")
            before = float(re.search(r"before impairment of goodwill was \$([\d.]+) million", g).group(1))
            items = round(before - yr["nia"], 1)       # TRC's own figure without the goodwill impairment: its effect on TRC's income
            quote(f, "During 2015, we recognized a provisional loss of $290.0 million associated with the impairment of goodwill in our "
                     "Field and Gathering segment.")
            note = ("the release lists one item on TRC's basis, the $290.0 million provisional goodwill impairment (the Partnership's), "
                    f"whose effect on TRC is {usd_m(items)}: TRC's net income attributable to common shareholders before impairment of "
                    f"goodwill, $83.9 million, less the {usd_m(yr['nia'])} reported; the Partnership's other items (a $32.6 million "
                    "impairment charged to depreciation, Atlas merger costs in other expense, a $30.6 million gain on the redemption "
                    "value of the joint ventures' preferred interests) are before the noncontrolling interests, with no TRC share stated")
        else:                                       # FY2016: TRC's own release, a loss
            quote(f, "For the full year 2016, net income (loss) attributable to Targa Resources Corp. was ($187.3) million compared to "
                     "$58.3 million for 2015.")
            items = 207.0
            quote(TENK16 := doc(K16, "10-K__"), "Includes a goodwill impairment of $183.0 million in the fourth quarter of 2016.")
            note = ("a loss: net loss attributable to common shareholders of $(278.1) million after the Series A preferred dividends (the "
                    "release prints no per-share figure); its $207.0 million of goodwill impairments ($24.0 million in the first "
                    "quarter, $183.0 million in the fourth) are pre-tax and listed for completeness: a loss year has no P/E either way")
        kept = yr["nia"] > 0 and (yr.get("eps", 1) or 0) > 0
        fa = {"fy": fy, "fy_label": f"FY{fy % 100:02d}", "eps_normalized": yr["eps"] if kept else None,
              "excluded_note": None if kept else (
                  f"a loss: net loss attributable to common shareholders of {usd_m(yr['nia'])} for {fy} (the {q} release, which prints "
                  "no per-share figure), so no P/E (the F, MU and CRM loss rule)"),
              "revenue_usd_b": round(yr["rev"] / 1000, 4), "diluted_shares_m": yr.get("sh"),
              "normalization_note": (f"FY{fy % 100:02d} ${yr['eps']:.2f} diluted, GAAP, from the {q} release ({pub}) until the 10-K" if kept
                                     else f"FY{fy % 100:02d} a loss to common shareholders, from the {q} release ({pub}) until the 10-K"),
              "op_margin": mg(yr["pti"], yr["rev"]),
              "op_margin_note": f"FY{fy % 100:02d} income before income taxes {usd_m(yr['pti'])} / revenues {usd_m(yr['rev'])} ({q} release)",
              "sales_growth": pct(yr0["rev"], yr["rev"]), "check_pretax_margin": mg(yr["pti"], yr["rev"]),
              "check_pretax_note": (f"FY{fy % 100:02d} income before income taxes / revenues ({q} release), before the noncontrolling "
                                    "interests" + (" (the Partnership's other unitholders), so the check overstates TRC's own EPS" if joint
                                                   else "")),
              "tax_rate": round(tax / yr["pti"], 3),
              "tax_note": f"FY{fy % 100:02d} effective rate: income tax {usd_m(tax)} (income before income taxes less net income) on {usd_m(yr['pti'])}",
              "one_off_test": {"items_after_tax_m": items, "income_attributable_m": yr["nia"],
                               "distorted": ((-items > yr["nia"] + items) if items < 0 else (items > yr["nia"])),
                               "kind": "benefits" if items < 0 else "charges", "note": note}}
        if not kept:
            fa["eps_gaap"] = None
        assert kept == (fy != 2016) and not (kept and fa["one_off_test"]["distorted"]), (q, "the year's EPS and the one-off test")
        if fa["diluted_shares_m"] is None:
            del fa["diluted_shares_m"]
        pr["fy_actual"] = fa
    prints.append(pr)
PQ = {p["quarter"]: p for p in prints}


def rederive(pr, raw):
    """A print's derived fields from (revised) raw figures."""
    return {"sales_b": round(raw["rev_m"] / 1000, 3), "sales_pct": pct(raw["rev_prior_m"], raw["rev_m"]),
            "opm": mg(raw["oi_m"], raw["rev_m"]), "opm_bp": bp(raw["oi_m"], raw["rev_m"], raw["oi_prior_m"], raw["rev_prior_m"]),
            "ptm": mg(raw["pti_m"], raw["rev_m"]), "ptm_bp": bp(raw["pti_m"], raw["rev_m"], raw["pti_prior_m"], raw["rev_prior_m"])}


# ── the 8-K of 2014-10-23: revenues revised for the NGL buy-sell transactions (net basis) ──
FREV = doc(REV8K, "8-K__")
source("TG60", REV8K, "Targa Resources Corp. 8-K of 2014-10-23, Revision of Previously Reported Revenues and Product Purchases", FREV,
       "revenues of 2011-2013 and of the quarters of 2013 and the first half of 2014 revised to report NGL buy-sell transactions on a "
       "net basis (no effect on income)")
REV_Q = quote(FREV, "Accordingly, Revenues and Product Purchases reported in its Form 10-K filed on February 14, 2014 and in previous quarterly "
                    "reports on Form 10-Q for 2014 and 2013 will be reduced by equal amounts as presented in the following tables. There is no "
                    "impact on previously reported net income, cash flows, financial position or other profitability measures.")
L8 = lines(FREV)
ia = line_no(FREV, lambda x: x == "As Revised:")
ry = row(FREV, "Revenues", ia, ia + 2)[1]                                # 2013, 2012, 2011
iq = line_no(FREV, lambda x: x == "As Revised:", ia + 1)
rq = row(FREV, "Revenues", iq, iq + 2)[1]       # Q3 2013, Q2 2014, Q2 2013, Q1 2014, Q1 2013, 9M 2013, 6M 2014, 6M 2013
hq = line_no(FREV, lambda x: x.startswith("2013 | 2014 | 2013 | 2014 | 2013 | 2013 | 2014 | 2013"))
assert hq < ia + 30 and len(rq) == 8
revision_8k = {"published": SRC["TG60"]["published"], "source": "TG60",
               "revenue_usd_b": {"2013": round(ry[0] / 1000, 4), "2012": round(ry[1] / 1000, 4), "2011": round(ry[2] / 1000, 4)},
               "note": ("2011-2013 revenues revised to the net basis of NGL buy-sell transactions by the 8-K of 2014-10-23 (TG60): '"
                        + REV_Q.split(". There")[0] + ".'; 2010 and earlier as first published until a later 10-K revises them (a seam)")}
for q, (now_i, prior_i) in (("Q1 2014", (3, 4)), ("Q2 2014", (1, 2))):
    p = PQ[q]
    raw = {**p["raw"], "rev_m": rq[now_i], "rev_prior_m": rq[prior_i]}
    p["restated"] = [{"published": SRC["TG60"]["published"], "source": "TG60", "raw": raw, **rederive(p, raw),
                      "sales_note": f"revenues {usd_m(raw['rev_m'])} vs {usd_m(raw['rev_prior_m'])} (revised to the net basis of NGL "
                                    "buy-sell transactions, the 8-K of 2014-10-23)"}]

# ── EPS and diluted shares of TRC's own releases (from Q1 2016): each 10-Q from its own date; Q4 2016 from the FY2016 10-K ──
for i, (q, acc) in enumerate(TENQ.items()):
    f = doc(acc, "10-Q__")
    sid = f"TG{61 + i}"
    source(sid, acc, f"Targa Resources Corp. {q} 10-Q", f, "the quarter's diluted EPS and weighted-average diluted shares, with the year-ago "
           "quarter (the release prints neither)")
    n = line_no(f, lambda x: x == "CONSOLIDATED STATEMENTS OF OPERATIONS")
    e = row(f, "Net income (loss) per common share - diluted", n, n + 45)[1]
    s = row(f, "Weighted average shares outstanding - diluted", n, n + 45)[1]
    nia = row(f, "Net income (loss) attributable to common shareholders", n, n + 45)[1]
    p = PQ[q]
    assert abs(nia[0] - p["raw"]["nia_m"]) < 1e-9, (q, "the 10-Q's income = the release's")
    raw = {**p["raw"], "eps_q": e[0], "eps_q_prior": e[1], "dil_sh_m": s[0]}
    p["restated"] = [{"published": SRC[sid]["published"], "source": sid, "raw": raw, "eps_q": e[0], "eps_q_prior": e[1],
                      "diluted_shares_m": s[0],
                      "eps_note": f"GAAP, diluted, {eps_s(e[0])} against {eps_s(e[1])} a year earlier (the {q} 10-Q of {SRC[sid]['published']}; "
                                  "the release prints no per-share figure)"}]

# ── history vintages ────────────────────────────────────────────────────────────


def sel(path, years_n=5):
    """Item 6, Selected Financial Data: the year header and the rows the models read."""
    L = lines(path)
    i = max(k for k in range(len(L)) if re.sub(r" \| ", " ", L[k]).startswith("Item 6. Selected Financial Data") and "|" not in L[k][-6:])
    yi = next(k for k in range(i, i + 8) if re.fullmatch(r"(20\d\d \| ){4}20\d\d", L[k]))
    years = [int(y) for y in L[yi].split(" | ")]
    stop = i + 40
    rev = row(path, ["Revenues", "Revenues(1)"], i, stop)[1]
    epsr = row(path, ["Net income (loss) per common share - diluted", "Net income per common share - diluted"], i, stop)
    return years, dict(zip(years, rev)), dict(zip(years, epsr[1])), epsr[0]


def stmt(path):
    """The consolidated statement of operations (last three years) and the statement of cash flows."""
    i0 = line_no(path, lambda x: x == "CONSOLIDATED STATEMENTS OF OPERATIONS")
    hdr = next(k for k in range(i0, i0 + 6) if re.fullmatch(r"20\d\d \| 20\d\d \| 20\d\d", lines(path)[k]))
    yrs = [int(y) for y in lines(path)[hdr].split(" | ")]
    pti = row(path, PTI_L, i0, i0 + 40)[1]
    ni = row(path, ["Net income", "Net income (loss)"], i0, i0 + 40)[1]
    nia = row(path, ["Net income available to common shareholders", "Net income (loss) attributable to common shareholders"], i0, i0 + 40)[1]
    sh = row(path, "Weighted average shares outstanding - diluted", i0, i0 + 40)[1]
    eps = row(path, ["Net income available per common share - diluted", "Net income (loss) per common share - diluted"], i0, i0 + 40)[1]
    c0 = line_no(path, lambda x: x == "CONSOLIDATED STATEMENTS OF CASH FLOWS", i0)
    cfo = row(path, "Net cash provided by operating activities", c0, c0 + 80)[1]
    capex = row(path, "Outlays for property, plant and equipment", c0, c0 + 80)[1]
    dl = ["Dividends to common and common equivalent shareholders", "Dividends to common shareholders",
          "Dividends paid to common and preferred shareholders"]
    divr, divs = row(path, dl, c0, c0 + 80)
    return yrs, pti, ni, nia, sh, eps, cfo, capex, divs, divr.split(" |")[0]


def groups4(path):
    """The segment note's operating margin by segment for the latest year (four segments to the FY2015 10-K; display only)."""
    L = lines(path)
    n = max(k for k in range(len(L)) if re.match(r"Note \d+ . Segment Information$", L[k]))
    k = line_no(path, lambda x: x.startswith("Operating margin |"), n)
    v = row(path, "Operating margin", k, k + 1)[1]
    assert len(v) == 8 and abs(sum(v[:7]) - v[7]) < 0.15, (path, v)
    return [[s, round(x / 1000, 4), None] for s, x in zip(SEGS4, v[:4])], "'Other', the hedges, and TRC Non-Partnership left out"


def groups2(path):
    """The two segments from 2016 (the recast of 2016-05-23 and the FY2016 10-K): the segment note's first operating margin row."""
    L = lines(path)
    n = max(k for k in range(len(L)) if re.match(r"Note \d+ . Segment Information$", L[k]))
    k = line_no(path, lambda x: x.startswith("Operating margin |"), n)
    v = row(path, "Operating margin", k, k + 1)[1]
    assert abs(sum(v[:-1]) - v[-1]) < 0.15, (path, v)
    return ([[s, round(x / 1000, 4), None] for s, x in zip(("Gathering and Processing", "Logistics and Marketing"), v[:2])],
            "'Other', the hedges, and Corporate and Eliminations left out")


COMMODITY = {
    "it": "The Partnership’s primary natural gas gathering and processing arrangements that expose it to commodity price risk are its percent-of-proceeds arrangements.",
    "us": "Our primary natural gas gathering and processing arrangements that expose us to commodity price risk are our percent-of-proceeds arrangements."}
CYCLE = {"it": ("even if the Partnership’s business experiences fluctuations in its cash from operations due to seasonal and cyclical "
                "factors"),
         "us": "even if our business experiences fluctuations in cash from operations due to seasonal and cyclical factors"}
RISK = {"it": "Our cash flow is dependent upon the ability of the Partnership to make cash distributions to us.",
        "us": ("Our cash flow is affected by supply and demand for natural gas and NGL products and by natural gas, NGL, crude oil and "
               "condensate prices, and decreases in these prices could adversely affect our results of operations and financial condition.")}
GHG = {"it": "The adoption of climate change legislation or regulations restricting emissions of GHGs could result in increased operating "
             "costs and reduced demand for the products and services the Partnership provides.",
       "us": "The adoption and implementation of climate change legislation or regulations restricting emissions of GHGs could result in "
             "increased operating costs and reduced demand for the products and services we provide."}
SPLITTER = ("long-term, fee-based agreement (“Splitter Agreement”) under which Targa Terminals will build and operate a 35,000 barrel per "
            "day crude and condensate splitter")
REFSERV = {"it": "In the Partnership’s refinery services business, it typically provides NGL balancing services via contractual arrangements "
                 "with refiners to purchase and/or market propane and to supply butanes.",
           "us": "In our refinery services business, we typically provide NGL balancing services via contractual arrangements with refiners "
                 "to purchase and/or market propane and to supply butanes."}

VS = [(K13, "TG4", "10-K__", "Targa Resources Corp. FY2013 10-K", "it", groups4),
      (K14, "TG5", "10-K__", "Targa Resources Corp. FY2014 10-K", "it", groups4),
      (K15, "TG6", "10-K__", "Targa Resources Corp. FY2015 10-K", "it", groups4),
      (R15, "TG8", "EX-99.1__", "Targa Resources Corp. 8-K of 2016-05-23 (Exhibit 99.1, the FY2015 10-K's Items 1, 6, 7 and 8 recast "
       "for the two segments)", "it", groups2),
      (K16, "TG7", "10-K__", "Targa Resources Corp. FY2016 10-K", "us", groups2)]
prev = facts["history_vintages"][-1]
vintages = []
for acc, sid, prefix, title, voice, grp_fn in VS:
    f = doc(acc, prefix)
    years, rev, eps, epsrow = sel(f)
    last = years[0]
    source(sid, acc, title, f, "Item 6 (selected financial data: revenues and EPS), the statements of operations and cash flows, the segment "
           "note and the risk factors" + ("; recast for the two segments reported from 2016 and ASU 2015-03 (no figure the models read "
                                          "changes but the segments)" if acc == R15 else ""))
    yrs, pti, ni, nia, sh, eps3, cfo, capex, divs, divlab = stmt(f)
    assert yrs[0] == last and all(abs(eps3[k] - eps[yrs[k]]) < 1e-9 for k in range(3)), (sid, "statement EPS = Item 6 EPS")
    tax = round(pti[0] - ni[0], 1)
    grp, left_out = grp_fn(f)
    own = {str(y): eps[y] for y in sorted(eps, reverse=True) if y >= 2011 and eps[y] > 0}
    eps_norm = {**own, **{y: v for y, v in prev["eps_normalized"].items() if y not in own and int(y) < min(eps)}}   # earlier years carried
    for y in years:
        assert y < 2010 or (eps[y] > 0) == (y != 2010 and y != 2016), (sid, y)   # 2010 and 2016 are the losses (2009: no EPS to common)
    excl = dict(prev["eps_excluded"])
    if 2016 in eps:
        excl["2016"] = (f"$(1.80) a diluted share for 2016 (net loss attributable to common shareholders of {usd_m(nia[0])} after "
                        "$72.6M of Series A preferred dividends and $18.2M of deemed dividends, on 154.4M weighted shares): a loss, so no "
                        "P/E (the F, MU and CRM loss rule); its days leave the window")
        assert eps[2016] == -1.80 and nia[0] == -278.1
        quote(f, "Deemed dividends on Series A preferred stock | 18.2 | — | —")
    qf = doc(K15, "10-K__") if acc == R15 else f      # the recast reprints Items 1, 6, 7 and 8 only: the quoted words stay the 10-K's
    qtitle = "Targa Resources Corp. FY2015 10-K" if acc == R15 else title
    for k in (COMMODITY, CYCLE, RISK, GHG, REFSERV):
        quote(qf, k[voice])
    if acc in (K15, R15, K16):
        quote(qf, SPLITTER if acc != K16 else SPLITTER.replace("Targa Terminals will build", "we will build").replace(
            "crude and condensate", "crude oil and condensate"))
    revs = {**prev["revenue_usd_b"], **{str(y): round(rev[y] / 1000, 4) for y in years}}
    rsrc = {**prev["revenue_sources"], **{str(y): sid for y in years}}
    keep = sorted(revs, key=int)[-10:]                       # the ten fiscal years to the latest one (2006 leaves with the FY2016 10-K)
    revs = {y: revs[y] for y in sorted(revs, key=int, reverse=True) if y in keep}
    rsrc = {y: rsrc[y] for y in revs}
    shares = {**prev["diluted_shares_m"], **{str(y): s for y, s in zip(yrs, sh) if y >= 2011}}
    for y, s in shares.items():                              # each Q4 release's count matches the 10-K's
        p = next((p for p in prints if p.get("fy_actual") and p["fy_actual"]["fy"] == int(y)), None)
        assert p is None or "diluted_shares_m" not in p["fy_actual"] or p["fy_actual"]["diluted_shares_m"] == s, (sid, y)
    srcs = [sid] + [s for s in dict.fromkeys(rsrc.values()) if s != sid]
    buyin = acc == K16
    v = {**{k: prev[k] for k in ("company", "exchange", "symbol", "pe_window_start", "kind", "margin_signal_name")},
         "kind_text": ("A midstream natural gas and NGL company (owner of all of Targa Resources Partners LP's common units since February "
                       "17, 2016)" if buyin else prev["kind_text"]),
         "business_line": ("Natural gas gathering and processing, NGL logistics and marketing (Targa Resources Partners LP, wholly owned "
                           "but for its preferred units)" if buyin else prev["business_line"]),
         "normalization": prev["normalization"],
         "published": SRC[sid]["published"], "sources": srcs,
         "fy_label": f"FY{last % 100:02d}", "fiscal_year_ends": {str(last): f"{last}-12-31"},
         "eps_normalized": eps_norm, "eps_excluded": excl,
         "revenue_usd_b": revs, "revenue_sources": rsrc,
         "revenue_note": ("consolidated revenues (the Partnership in, as TRC consolidates it); each year from the latest 10-K that reports it"
                          "; the ten fiscal years to the latest one"),
         "diluted_shares_m": {y: shares[y] for y in sorted(shares, key=int, reverse=True)},
         "shares_note": (prev["shares_note"] + ("; 2016 includes the 104.5M shares issued for the Partnership's public common units on "
                                                "February 17, 2016 (the buy-in, in the figures as published)" if buyin else "")),
         "prev_fy_op_margin": mg(pti[0], rev[last]),
         "prev_fy_op_margin_note": f"FY{last % 100:02d} income before income taxes {usd_m(pti[0])} / revenues {usd_m(rev[last])} ({title})",
         "prev_fy_sales_growth": pct(rev[years[1]], rev[last]),
         "check_pretax_margin": mg(pti[0], rev[last]),
         "check_pretax_note": (f"FY{last % 100:02d} income before income taxes / revenues ({title}), before the noncontrolling interests"
                               + ("" if buyin else " (the Partnership's other unitholders), so the check overstates TRC's own EPS")),
         "tax_rate": round(tax / pti[0], 3),
         "tax_note": f"FY{last % 100:02d} effective rate: income tax {usd_m(tax)} (income before income taxes less net income) on {usd_m(pti[0])} ({title})",
         "dividend_annual": None, "dividend_note": None,
         "fcf_b": round((cfo[0] + capex[0]) / 1000, 3), "fcf_label": f"FY{last % 100:02d}",
         "fcf_note": (f"consolidated net cash provided by operating activities {usd_m(cfo[0])} less outlays for property, plant and "
                      f"equipment {usd_m(-capex[0])} ({title}" + ("" if buyin else "; the Partnership's, mostly") + ")"),
         "cash_return_text": f"{usd_m(-divs[0])} of {divlab[0].lower() + divlab[1:]} in FY{last % 100:02d}".replace(
             "of dividends paid to", "of dividends paid to").replace("of dividends to", "of dividends to"),
         "groups": grp, "groups_basis": f"FY{last % 100:02d} segment operating margin, USD bn ({title}'s segment note; {left_out})",
         "why": (f"Commodity exposure ({qtitle}): {COMMODITY[voice]} Distribution policy: '{CYCLE[voice]}' (the boilerplate of the "
                 f"{'cash distribution' if voice == 'it' else 'dividend'} policy, not a statement that the business is cyclical: the CHTR "
                 f"reading). Risk factor: '{RISK[voice]}'; no theme in taxonomy_eras.json is live for a midstream natural gas company on "
                 "this date"),
         "ghg_quote": GHG[voice], "refinery_quote": REFSERV[voice], "tenk_label": qtitle}
    if acc in (K15, R15, K16):
        v["splitter_quote"] = SPLITTER if acc != K16 else SPLITTER.replace("Targa Terminals will build", "we will build").replace(
            "crude and condensate", "crude oil and condensate")
    vintages.append(v)
    prev = v

# ── Q4 2016's EPS from the FY2016 10-K's selected quarterly data (Note 27), from the 10-K's date ──
F16 = doc(K16, "10-K__")
nq = max(k for k, x in enumerate(lines(F16)) if x.startswith("Note 27") and "Selected Quarterly Financial Data" in x)
q16 = row(F16, "Net income (loss) per common share - diluted", nq, nq + 11)[1]          # Q1-Q4 2016, total
y15 = line_no(F16, lambda x: x == "2015", nq)
q15 = row(F16, "Net income per common share - diluted", y15, y15 + 8)[1]                # Q1-Q4 2015, total
n16 = row(F16, "Net income (loss) attributable to common shareholders", nq, nq + 11)[1]
p = PQ["Q4 2016"]
assert abs(n16[3] - p["raw"]["nia_m"]) < 1e-9 and q16[4] == -1.80, ("Q4 2016", "the 10-K's quarter = the release's")
raw = {**p["raw"], "eps_q": q16[3], "eps_q_prior": q15[3]}
p["restated"] = [{"published": SRC["TG7"]["published"], "source": "TG7", "raw": raw, "eps_q": q16[3], "eps_q_prior": q15[3],
                  "eps_note": f"GAAP, diluted, {eps_s(q16[3])} against {eps_s(q15[3])} a year earlier (the FY2016 10-K's selected quarterly "
                              f"data, {SRC['TG7']['published']}; the release prints no per-share figure)"}]

# ── dividend outlooks (display only; no revenue, EPS or margin guide in any filing of 2014-2017) ──
FAT = doc(ATLAS8K, "EX-99.1__")
source("TG31", ATLAS8K, "Targa Resources Corp. and Targa Resources Partners LP, the Atlas mergers (8-K of 2014-10-14, Exhibit 99.1)", FAT,
       "TRC's 2015 pro forma dividend growth estimate (display only)")
OUT31 = quote(FAT, "Assuming a first quarter close and 11 – 13% distribution growth at the Partnership, the Company estimates full year "
                   "2015 pro forma dividend growth over full year 2014 of approximately 35%.")
FBI = doc(BUYIN8K, "EX-99.1__")
source("TG32", BUYIN8K, "Targa Resources Corp. to acquire the Partnership's common units (8-K of 2015-11-03, Exhibit 99.1)", FBI,
       "TRC's 2016 dividend growth expectation after the buy-in (display only)")
OUT32 = sentence(FBI, r"Following this transaction, TRC expects dividend growth of 15% for 2016 and greater than 10% compound annual "
                      r"dividend growth through 2018[^.]*\.")
OUT17 = quote(FREL["Q4 2016"], "For full year 2017, Targa expects dividend coverage to exceed 1.0 times assuming a $3.64 per common share 2017 "
                                "dividend.")
guides = [{"fy": 2015, "published": SRC["TG31"]["published"], "source": "TG31", "rev_none": True,
           "display": f"TRC 2015 dividend outlook (pro forma for the Atlas mergers): '{OUT31}'; no revenue, EPS or margin guide (display only)"},
          {"fy": 2016, "published": SRC["TG32"]["published"], "source": "TG32", "rev_none": True,
           "display": f"TRC 2016 dividend outlook (with the buy-in): '{OUT32}'; no revenue, EPS or margin guide (display only)"},
          {"fy": 2017, "published": PQ["Q4 2016"]["published"], "source": SID["Q4 2016"], "rev_none": True,
           "display": f"TRC 2017 dividend outlook: '{OUT17}'; no revenue, EPS or margin guide (the 2017 guidance is volumes and capital "
                      "spending; display only)"}]

# ── append ──────────────────────────────────────────────────────────────────────
facts["history_vintages"] += vintages
facts["prints"] += prints
facts["guides"] += guides
facts["dividends"] += dividends
facts["revenue_restatements"] = [revision_8k]
for k in ("history_vintages", "prints", "guides", "dividends"):
    n = len(BEFORE[k])
    assert facts[k][:n] == BEFORE[k], (k, "an earlier fact changed")
assert {k: v for k, v in facts["sources"].items() if k in BEFORE["sources"]} == BEFORE["sources"]
assert facts["rule_t"] == BEFORE["rule_t"], "rule T stays frozen at 2012-02-24"
facts["_doc"] = BEFORE["_doc"] + (" 2014-2017 appended by retro/generators/trgp/gen_trgp_1417.py from the same filings' rows, every earlier "
                                  "fact asserted unchanged.")
out = A.out or os.path.join(REPO, "retro", "facts", "TRGP.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(facts, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
ck = A.checklist or os.path.join(SP, "checklist_trgp_1417.json")
with open(ck, "w", encoding="utf-8") as fh:
    json.dump(CHECK, fh, ensure_ascii=False, indent=1)
print(out, len(prints), "prints", len(vintages), "vintages", len(dividends), "dividends", sum(len(v) for v in CHECK.values()), "checked strings")
for p in prints:
    print(p["quarter"], p["published"], p["sales_pct"], p["gp_pct"], p["lm_pct"], p["opm_bp"], p["ptm_bp"], p["eps_q"],
          p.get("fy_actual", {}).get("eps_normalized", "-"), [r["published"] for r in p.get("restated", [])])
for v in vintages:
    print(v["fy_label"], v["published"], v["eps_normalized"], v["diluted_shares_m"], v["revenue_usd_b"], v["tax_rate"], v["groups"])
