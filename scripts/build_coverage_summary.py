#!/usr/bin/env python3
"""
Builds the Research-tab Coverage Summary (static/summary/data.json) plus a
markdown twin from the classified ticker JSONs.

    python3 scripts/build_coverage_summary.py --signals DIR --out-json PATH [--out-md PATH]
                                              [--notes reports/summary_notes.json]

All lists are computed from the data (class + a ranking score), so the file can
be regenerated every morning.  The narrative layer — intro, per-ticker notes,
sector reads, dangers — comes from an optional notes overlay written by the
daily classification-review routine; where a note is missing the ticker's
quality_note is used, so the page is never empty.

Notes overlay format (reports/summary_notes.json):
  {"date": "YYYY-MM-DD",
   "intro": "...optional paragraph appended to the auto intro...",
   "notes": {"TMUS": "...", ...},
   "sectors": {"Finance": "...", ...},
   "dangers": ["...", "..."]}
"""
import argparse
import collections
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quality_classify as qc  # noqa: E402

TODAY = datetime.date.today().isoformat()
SECTORS = ["Finance", "Technology", "Consumer Discretionary", "Healthcare", "Industrials", "Utilities",
           "Consumer Staples", "Energy", "Telecoms/Media", "Materials", "Basic Resources", "Bonds"]
RICH = {"QUALITY, PRICED FOR PERFECTION", "TOO MUCH CYCLE RISK", "AI-EXPOSED, NOT CHEAP", "STRUCTURAL RISK, NOT CHEAP"}
STRUCT = ("CHEAP, BUT STRUCTURAL RISK", "STRUCTURAL RISK, NOT CHEAP", "TURNAROUND BET", "SPECIAL SITUATION",
          "AI-EXPOSED, NEUTRALLY VALUED", "AI-EXPOSED, NOT CHEAP")


def score(c):
    """Higher = better risk/reward for a long: model-vs-market gap, asymmetry,
    conservative 2-yr, distance to floor, obsolescence risk."""
    adj = c["_adj"] if c["_adj"] is not None else {
        "UNDERVALUED": 0.6, "MODESTLY UNDERVALUED": 0.3, "FAIRLY VALUED": 0.0,
        "MODESTLY OVERVALUED": -0.3, "OVERVALUED": -0.7}.get(c["_verdict"], 0.0)
    rb = min(c["_rb"], 3.0)
    epp = c["_epp"] or 0.0
    cons = c["_cons"]
    return (adj + (1 - rb) + (cons / 100 if cons is not None else 0)
            - 0.25 * (c["obsolescence_risk"] - 1) - max(0.0, epp - 40) / 200)


def item(e, notes):
    return {"t": e["ticker"], "s": e["_c"]["quality_class"],
            "x": notes.get(e["ticker"]) or e["_c"]["quality_note"]}


def pick(entries, classes, notes, limit=None, reverse=True, offset=0):
    es = [e for e in entries if e["_c"]["quality_class"] in classes]
    es.sort(key=lambda e: score(e["_c"]), reverse=reverse)
    es = es[offset: offset + limit] if limit else es[offset:]
    return [item(e, notes) for e in es]


def build(entries, notes_doc):
    notes = notes_doc.get("notes", {})
    for e in entries:
        e["_c"] = qc.classify(e)
    counts = collections.Counter(e["_c"]["quality_class"] for e in entries)
    n = len(entries)
    by_sector = collections.defaultdict(list)
    for e in entries:
        by_sector[e["sector_group"]].append(e)

    best = pick(entries, {"COMPOUNDER AT LOW PRICE"}, notes, limit=10)
    second = pick(entries, {"COMPOUNDER AT LOW PRICE"}, notes, limit=10, offset=10)
    ai_fear = pick(entries, {"AI-FEAR BASKET"}, notes)
    near = [i for i in pick(entries, {"QUALITY, NEUTRALLY VALUED"}, notes, limit=6)
            if next(e for e in entries if e["ticker"] == i["t"])["_c"]["_adj"] is not None
            and next(e for e in entries if e["ticker"] == i["t"])["_c"]["_adj"] >= 0.2][:5]
    cyc_ok = pick(entries, {"CYCLICAL, RISK PRICED IN"}, notes)
    removed = [item(e, notes) for e in entries
               if qc.legacy_tier(e) == "BUY"
               and e["_c"]["quality_class"] not in ("COMPOUNDER AT LOW PRICE", "AI-FEAR BASKET", "CYCLICAL, RISK PRICED IN")]
    turn = pick(entries, {"TURNAROUND BET", "CHEAP, BUT STRUCTURAL RISK", "STRUCTURAL RISK, NOT CHEAP",
                          "AI-EXPOSED, NEUTRALLY VALUED", "AI-EXPOSED, NOT CHEAP"}, notes)
    sells = pick(entries, RICH, notes, limit=20, reverse=False)

    struct_n = sum(counts[k] for k in STRUCT)

    sector_items = []
    for sec in SECTORS:
        es = by_sector.get(sec)
        if not es:
            continue
        c = collections.Counter(e["_c"]["quality_class"] for e in es)
        auto = "; ".join(f"{v} {k.lower()}" for k, v in c.most_common())
        low = sorted(e["ticker"] for e in es if e["_c"]["quality_class"] in ("COMPOUNDER AT LOW PRICE", "AI-FEAR BASKET"))
        auto = (f"{auto}." + (f" Cheap and durable: {', '.join(low)}." if low else " No compounder at a low price."))
        text = notes_doc.get("sectors", {}).get(sec) or auto
        sector_items.append({"h": f"{sec} ({len(es)})", "x": text})

    dangers = notes_doc.get("dangers") or [
        f"Crowding at highs. {counts['QUALITY, PRICED FOR PERFECTION']} quality names and {counts['TOO MUCH CYCLE RISK']} cyclicals are priced for perfection or at a cycle peak — {round(100 * (counts['QUALITY, PRICED FOR PERFECTION'] + counts['TOO MUCH CYCLE RISK']) / n)}% of coverage. The largest single risk remains buying good companies at the top of their ranges.",
        f"Cheap-for-a-reason. {counts['CHEAP, BUT STRUCTURAL RISK'] + counts['TURNAROUND BET'] + counts['SPECIAL SITUATION']} names screen cheap while the E in their floor is contested (structural decline, turnaround, binary outcome). They are labelled as such instead of promoted.",
        f"AI disruption. {counts['AI-FEAR BASKET']} names sit in the AI-fear basket: durable-looking franchises the market is pricing as generative-AI losers. The numbers keep refusing the bear case, but this is the one group where 'becoming useless' is a non-zero scenario — own as a basket, not as single convictions.",
    ]

    intro = (
        f"{n} names under coverage, classified on two axes. Axis 1 is business durability — how likely the business "
        "is to become useless (reviewed per ticker by the daily classification routine: durable franchise, cyclical, "
        "AI-exposed, structurally challenged, turnaround, special situation). Axis 2 is price — downside room and "
        "asymmetry from the model's own numbers (Ratio B, distance to the EPP panic floor, adjusted-vs-market "
        "composite, conservative 2-yr case). "
        f"Today: {counts['COMPOUNDER AT LOW PRICE']} compounders at a low price, {counts['AI-FEAR BASKET']} in the AI-fear basket, "
        f"{counts['QUALITY, NEUTRALLY VALUED']} quality names neutrally valued, {counts['QUALITY, PRICED FOR PERFECTION']} priced for perfection, "
        f"{counts['TOO MUCH CYCLE RISK']} with too much cycle risk, {counts['CYCLICAL, RISK PRICED IN'] + counts['CYCLICAL, NEUTRALLY VALUED']} "
        f"cyclicals at a fair or discounted price, and {struct_n} structural, turnaround or special situations. "
        "Everything below is a model output, not a price target."
    )
    if notes_doc.get("intro"):
        intro += " " + notes_doc["intro"].strip()

    data = {
        "title": "Coverage Summary",
        "updated": TODAY,
        "intro": intro,
        "stats": [
            {"label": "Coverage", "value": str(n)},
            {"label": "Compounder at low price", "value": str(counts["COMPOUNDER AT LOW PRICE"])},
            {"label": "AI-fear basket", "value": str(counts["AI-FEAR BASKET"])},
            {"label": "Quality, neutral", "value": str(counts["QUALITY, NEUTRALLY VALUED"])},
            {"label": "Priced for perfection", "value": str(counts["QUALITY, PRICED FOR PERFECTION"])},
            {"label": "Too much cycle risk", "value": str(counts["TOO MUCH CYCLE RISK"])},
        ],
        "sections": [
            {"heading": "Best buys — durable businesses with limited downside",
             "body": ["Downside limited by the model's own floor and asymmetry, AND low-to-neutral risk of the business becoming useless. Ranked by a blend of model-vs-market gap, Ratio B, conservative 2-yr return, distance to floor and obsolescence risk. Buys at today's prices, not on a further pullback."],
             "items": best},
            {"heading": "Second line — same quality, slightly less asymmetry",
             "body": ["Also compounders at a low price; buy after the first group."],
             "items": second},
            {"heading": "The AI-fear basket — cheap because the market is pricing disruption",
             "body": ["Franchises with a live generative-AI substitution debate (software, IT services, information, search, mobility). Kept OUT of the compounder list on purpose: the discount is real and the reported numbers keep refusing the bear case, but this is the one group where 'becoming useless' is a non-zero scenario. Own as a basket, sized as one position, not as single convictions."],
             "items": ai_fear},
            {"heading": "Almost there — quality at a neutral price worth adding on weakness",
             "items": near},
            {"heading": "Cyclicals where the cycle risk is already in the price",
             "body": ["Good businesses whose earnings are the cycle, at prices that already discount it. Fine to own, sized as cyclicals."],
             "items": cyc_ok},
            {"heading": "The model's own BUYs we keep out of the buy list",
             "body": ["Rated BUY by the valuation model; cheap by the numbers but not downside-limited compounders."],
             "items": removed},
            {"heading": "Turnarounds and structural risk — cheap is not enough",
             "items": turn},
            {"heading": "Sell / trim — priced for perfection or at a cycle peak",
             "body": ["The twenty worst risk/reward setups in coverage: trim into strength, no new money."],
             "items": sells},
            {"heading": "Sector reads", "items": sector_items},
            {"heading": "Main dangers across the book", "body": dangers},
        ],
        "footer": ("Generated from the live model catalog · classes = business durability (model-reviewed daily) × "
                   "price/asymmetry (Ratio B, EPP-floor distance, adjusted-vs-market composite, conservative 2-yr) · "
                   "not financial advice."),
    }
    if notes_doc.get("date"):
        data["footer"] = f"Narrative reviewed {notes_doc['date']} · " + data["footer"]
    return data, counts


def to_markdown(data):
    out = [f"# {data['title']}\n", f"_updated {data['updated']}_\n", data["intro"], ""]
    out.append("| " + " | ".join(s["label"] for s in data["stats"]) + " |")
    out.append("|" + "---|" * len(data["stats"]))
    out.append("| " + " | ".join(s["value"] for s in data["stats"]) + " |\n")
    for sec in data["sections"]:
        out.append(f"## {sec['heading']}\n")
        for b in sec.get("body", []):
            out.append(b + "\n")
        for it in sec.get("items", []):
            if "h" in it:
                out.append(f"- **{it['h']}** — {it['x']}")
            else:
                out.append(f"- **{it['t']}** · _{it['s']}_ — {it['x']}")
        out.append("")
    out.append(f"_{data['footer']}_")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--signals", required=True)
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--out-md")
    ap.add_argument("--notes", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reports", "summary_notes.json"))
    a = ap.parse_args()
    notes_doc = {}
    if a.notes and os.path.exists(a.notes):
        with open(a.notes, encoding="utf-8") as fh:
            notes_doc = json.load(fh)
    entries = qc.load_dir(a.signals)
    data, counts = build(entries, notes_doc)
    os.makedirs(os.path.dirname(os.path.abspath(a.out_json)), exist_ok=True)
    with open(a.out_json, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    print(f"wrote {a.out_json} (notes: {notes_doc.get('date', 'none')})")
    if a.out_md:
        os.makedirs(os.path.dirname(os.path.abspath(a.out_md)), exist_ok=True)
        with open(a.out_md, "w", encoding="utf-8") as fh:
            fh.write(to_markdown(data))
        print(f"wrote {a.out_md}")
    for k, v in counts.most_common():
        print(f"{v:4d}  {k}")


if __name__ == "__main__":
    main()
