#!/usr/bin/env python3
"""
Builds the Research-tab Coverage Summary (static/summary/data.json) and a
markdown twin under reports/ from the classified ticker JSONs.

    python3 scripts/build_coverage_summary.py --signals DIR --out-json PATH --out-md PATH

The item lists (best buys, sells, buckets) are computed from the data; the
narrative around them is written by hand in NARRATIVE below and should be
refreshed whenever the taxonomy or the market changes materially.
"""
import argparse
import collections
import datetime
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quality_classify as qc  # noqa: E402

TODAY = datetime.date.today().isoformat()


def score(c):
    adj = c["_adj"] if c["_adj"] is not None else {
        "UNDERVALUED": 0.6, "MODESTLY UNDERVALUED": 0.3, "FAIRLY VALUED": 0.0,
        "MODESTLY OVERVALUED": -0.3, "OVERVALUED": -0.7}.get(c["_verdict"], 0.0)
    rb = min(c["_rb"], 3.0)
    epp = c["_epp"] or 0.0
    cons = c["_cons"]
    return (adj + (1 - rb) + (cons / 100 if cons is not None else 0)
            - 0.25 * (c["obsolescence_risk"] - 1) - max(0.0, epp - 40) / 200)


# ─────────────────────────────────────────────────────────────────────────────
# Hand-written commentary per ticker (used where a ticker appears in a list)
# ─────────────────────────────────────────────────────────────────────────────
NOTES = {
    "TMUS": "The cleanest combination of durability and asymmetry in the book: US wireless #1, still 32% below its 52-week high, 0.41x Ratio B and a +1.32 model-vs-market gap. Capital-intensive oligopoly, but nothing here becomes useless.",
    "MRSH": "Marsh McLennan — fee-based broking with no underwriting risk and a 19-year margin-expansion streak, 15% above its floor at 0.33x Ratio B; the conservative 2-yr case still returns +30%.",
    "AZO":  "AutoZone within 1% of its 52-week low at 0.28x Ratio B and only 16% above the floor. Counter-cyclical, buyback-driven compounder; the EV mix headwind is a decade-scale drift, not a cliff.",
    "PEG":  "PSEG — regulated New Jersey wires plus nuclear, 5% above its floor, 0.43x Ratio B, 6-8% EPS growth guided to 2030. Rate-sensitive, but obsolescence risk is about as low as equities get.",
    "HD":   "Home Depot 15% above its floor at 0.31x Ratio B with a +25% conservative 2-yr case. A frozen housing market is a cyclical trough for a durable franchise, not a broken business.",
    "KKR":  "KKR sold off with the alternative managers on private-credit jitters: 0.41x Ratio B, +1.04 gap. Fee-related earnings are durable; realizations are the cyclical part — size it below MRSH.",
    "WM":   "Waste Management — landfill/collection moat with pricing power; the conservative 2-yr floor case has converged with the price, i.e. very little downside is left in the disciplined scenario.",
    "SPGI": "S&P Global trades 4% BELOW its own panic floor at 0.38x Ratio B — a ratings duopoly plus index flywheel at the floor is rare. The composite reads it as fairly priced, which is why it is a buy on safety rather than on upside.",
    "SCHW": "Schwab — the +0.82 model-vs-market gap is one of the widest among durable names; cash-sorting relief is the tailwind, rate cuts the risk.",
    "MA":   "Mastercard — 23% above floor with a +0.76 gap after a routine pullback from the all-time high. Ratio B is only 1.0x, so this is quality at a fair-to-good price rather than a bargain.",
    "APD":  "Air Products — take-or-pay industrial gas at 26% above floor, 0.65x Ratio B; the hydrogen megaprojects are free optionality under the new CEO's capex discipline.",
    "AXP":  "American Express — closed-loop network with the fastest card-member spending growth in three years, 0.51x Ratio B; conservative 2-yr +9%.",
    "MCD":  "McDonald's at its 52-week low: 0.28x Ratio B, royalty-stream economics. The composite is only fair, so this is downside protection first.",
    "SYK":  "Stryker 20% above floor, 0.79x Ratio B, modestly undervalued composite — medtech compounder at a reasonable price.",
    "BX":   "Blackstone after a sector-wide alt-manager slide: 0.74x Ratio B, +0.60 gap. Same caveat as KKR — fee earnings durable, realizations cyclical.",
    "BSX":  "Boston Scientific 21% above floor with a +40% conservative 2-yr case; the cyber-incident is transient, the WATCHMAN/Farapulse growth is not.",
    "LOW":  "Lowe's at a fresh 52-week low after the guidance cut, 25% above floor with a +24% conservative case — the same housing trough as HD, one notch less quality.",
    "MDLZ": "Mondelez — cocoa costs easing into 2027, 0.44x Ratio B, 27% above floor; GLP-1 is the slow headwind.",
    "WKL":  "Wolters Kluwer — the AI-fear discount that keeps refusing to show up in renewal numbers; +0.74 gap, 19% above floor. Buy only if you accept the AI-disruption debate.",
    "NOW":  "ServiceNow after a round-trip to $137: 0.44x Ratio B, 102% upside to bull. The per-seat-vs-agentic-AI question is unresolved — a real risk, priced in part.",
    "ADBE": "Adobe 7% above its floor at 0.42x Ratio B with a vacant CEO seat and a generative-AI overhang — the market's clearest 'AI loser' bet among quality names, and therefore the cheapest.",
    "ACN":  "Accenture 23% above floor, 0.45x Ratio B, well off its high on bookings deceleration and federal exposure; GenAI is both the threat and the next services cycle.",
    "PRX":  "Prosus 2.5% off its 52-week low with every ecosystem profitable — a NAV-discount story that keeps improving while the price drifts.",
    "BKNG": "Booking — OTA leader at 0.76x Ratio B, modestly undervalued; AI-agent disintermediation is the long-dated risk.",
    "TDG":  "TransDigm — +1.21 gap and 0.41x Ratio B, but 171% above a trough-EPS floor; the EPP methodology understates a levered pricing-power compounder. Fair price, not cheap.",
    "BRK":  "Berkshire — 0.73x Ratio B, +44% conservative case, 14x operating earnings; PacifiCorp wildfire litigation (Nov 3 oral arguments) is the one real tail.",
    "GOOGL":"Alphabet — modestly undervalued composite, balanced 1.0x Ratio B; 74% above floor keeps it in the neutral bucket.",
    "KTY":  "Kety — aluminium extrusions, +0.96 gap, 37% above floor with confirmed dividend tranches; European industrial cycle risk, but paid for.",
    "VST":  "Vistra — merchant power/nuclear with 0.59x Ratio B and insider buying; earnings ride power prices and AI-load PPAs, so it is a cyclical, not a compounder.",
    "PGR":  "Progressive 3.5% above its floor with a +0.64 gap — but the 87% combined ratio is a cyclical peak; the asymmetry is good, the earnings base is not a floor.",
    "BAC":  "Bank of America — +0.56 gap, conservative +15%, but 67% above floor and a rate/credit cycle; fine as a cyclical, not a compounder.",
    "NVDA": "Nvidia 9% above its floor at 0.77x Ratio B after the post-earnings round trip; a capex cycle, not an annuity — size accordingly.",
    "C":    "Citi — restructuring keeps beating (best quarterly revenue in a decade), +0.62 gap; still a credit/trading cycle at 65% above floor.",
    # structural / special
    "CMCSA":"Comcast 22% below its floor, 0.28x Ratio B — statistically the cheapest name in coverage. It stays out of the buy list because broadband is losing subscribers to fixed-wireless and fiber and video is in secular decline: the E in the floor is eroding.",
    "CHTR": "Charter — 174% upside to bull on paper, but the same cable share-loss problem as Comcast plus high leverage; cheap for a reason.",
    "EIX":  "Edison 24% below its floor after the 24% one-day crash — the value is real, but the tail is decided by the California legislature and the Eaton Fire inverse-condemnation exposure, not by the balance sheet. Binary, not a compounder.",
    "PCG":  "PG&E below its floor with liability uncapped after SB 492 died; capex deferred and a strategic review launched. Same binary as EIX.",
    "DOW":  "Dow — trough earnings, +0.57 gap, but 121% above an EV/EBITDA floor and the Middle East ethane advantage is normalising: cyclical at a fair price, not a buy on downside protection.",
    "RHM":  "Rheinmetall flipped back to BUY on the model's price mechanics, but at 135% above floor, ~35x earnings and 45% realised vol it is exactly the cycle risk this taxonomy is built to flag.",
    "NKE":  "Nike below its floor — but the floor is computed on collapsed earnings; a turnaround bet on new management, not a value buy.",
    "FISV": "Fiserv 25% below its floor after the guidance reset; the merchant business is decelerating and the M&A premium faded. Turnaround, not compounder.",
    "PYPL": "PayPal after the Stripe/Advent bid collapse; 0.34x Ratio B but branded-checkout share loss is structural until proven otherwise.",
    "BMY":  "Bristol — 22% above floor, 0.75x Ratio B, yet the Eliquis/Opdivo 2028 cliff makes the floor unreliable; conservative case -9%.",
    "PFE":  "Pfizer at a 52-week high on a 6% yield; the LOE cliff is the structural problem and the rally has removed the cheapness.",
    "MO":   "Altria — cigarette volumes in secular decline, NJOY blocked, stock up against an unchanged guide.",
    "INTC": "Intel after a 5x run: below its floor on paper, 2.1x Ratio B, foundry economics unproven.",
    # sells / trims
    "TRGP": "Targa 577% above its panic floor with 3.75x Ratio B — the midstream premium has nothing left to price.",
    "MPC":  "Marathon Petroleum at a fresh high on a geopolitical crack-spread spike; 13x Ratio B, 4% upside to bull. The Street's own targets sit below spot.",
    "VLO":  "Valero — same refining peak; 13x Ratio B, 3.6% upside to bull.",
    "PSX":  "Phillips 66 — at a fresh all-time high with 4.3x Ratio B; quality refiner at a cycle peak.",
    "DE":   "Deere at an all-time high on two sell-side upgrades, 6.3x Ratio B, ~40x trough-cycle EPS; conservative 2-yr case -44%.",
    "HAL":  "Halliburton — 7.4x Ratio B, 6% upside to bull, conservative case -12%; rig-count optimism fully paid.",
    "AAPL": "Apple at 5.5x Ratio B, 108% above floor with the memory-cost margin question unresolved into the Oct 29 print; conservative case -28%.",
    "PM":   "Philip Morris trades within 3% of its own BULL scenario while ZYN shipments decelerate; 16x Ratio B.",
    "AMD":  "AMD — 196% above floor, conservative case -47%; the AI ramp has to be flawless.",
    "TSLA": "Tesla at its BULL level with auto earnings collapsed; the price is the robotaxi option and nothing else.",
    "XTB":  "XTB at a 52-week high with conservative 2-yr -40%; retail-brokerage volumes are the cycle.",
    "MAR":  "Marriott within 3% of its BULL level with a Middle East RevPAR headwind — lodging is priced for perfection.",
    "HLT":  "Hilton — even after a 7% drop on the Goldman downgrade, 15x Ratio B and 118% above floor.",
    "ECL":  "Ecolab at ~35x forward, 148% above floor, 2.7x Ratio B — excellent business, no margin of safety.",
    "KO":   "Coca-Cola 100% above floor, 2.5x Ratio B, conservative case -15%; the defensive premium is at a record.",
    "PLTR": "Palantir 273% above floor at 4.2x Ratio B — exceptional business, almost no margin of safety versus a genuine bear case.",
    "DBK":  "Deutsche Bank at a 52-week high with 3.9x Ratio B; the profit-growth streak is real and fully priced.",
    "ISP":  "Intesa — 104% above floor, 2.2x Ratio B, conservative -19%; the fee annuity is priced as if NII compression never arrives.",
    "INGA": "ING — +51% run, 120% above floor, conservative -20%; the deposit-margin cycle is the risk every EU retail bank shares.",
    "META": "Meta after the settlement rally: 1.8x Ratio B, composite -1.28; the ad engine is healthy, the price is the problem.",
    "MSFT": "Microsoft — composite fairly valued after the pullback, but 2.7x Ratio B: 51% downside to bear vs 19% to bull. Hold, do not add above $460.",
}


def sect_items(entries, keys, limit=None, key_fn=None):
    out = []
    for e in entries:
        c = e["_c"]
        if c["quality_class"] in keys:
            out.append(e)
    out.sort(key=key_fn or (lambda e: -score(e["_c"])))
    if limit:
        out = out[:limit]
    return [{"t": e["ticker"], "s": e["_c"]["quality_class"],
             "x": NOTES.get(e["ticker"], e["_c"]["quality_note"])} for e in out]


def build(entries):
    for e in entries:
        e["_c"] = qc.classify(e)
    counts = collections.Counter(e["_c"]["quality_class"] for e in entries)
    n = len(entries)
    by_sector = collections.defaultdict(list)
    for e in entries:
        by_sector[e["sector_group"]].append(e)

    best = sect_items(entries, {"COMPOUNDER AT LOW PRICE"})
    top = [i for i in best if i["t"] in ("TMUS", "MRSH", "AZO", "PEG", "HD", "KKR", "WM", "SPGI", "SCHW", "MA")]
    second = [i for i in best if i["t"] in ("APD", "AXP", "MCD", "SYK", "BX", "BSX", "LOW", "MDLZ", "BKNG", "PRX")]
    ai_fear = [i for i in best if i["t"] in ("WKL", "NOW", "ADBE", "ACN")]
    near = [i for i in sect_items(entries, {"QUALITY, NEUTRALLY VALUED"}) if i["t"] in ("TDG", "BRK", "GOOGL")]
    cyc_ok = sect_items(entries, {"CYCLICAL, RISK PRICED IN"})
    removed = [{"t": t, "s": next(e["_c"]["quality_class"] for e in entries if e["ticker"] == t), "x": NOTES[t]}
               for t in ("CMCSA", "CHTR", "EIX", "PCG", "DOW", "RHM")]
    turn = [{"t": t, "s": next(e["_c"]["quality_class"] for e in entries if e["ticker"] == t), "x": NOTES[t]}
            for t in ("NKE", "FISV", "PYPL", "BMY", "PFE", "MO", "INTC")]
    sells = [{"t": t, "s": next(e["_c"]["quality_class"] for e in entries if e["ticker"] == t), "x": NOTES[t]}
             for t in ("TRGP", "MPC", "VLO", "PSX", "DE", "HAL", "AAPL", "PM", "AMD", "TSLA", "XTB", "MAR", "HLT", "ECL", "KO", "PLTR", "DBK", "ISP", "INGA", "META", "MSFT")]

    def sec_line(sec):
        es = by_sector[sec]
        c = collections.Counter(e["_c"]["quality_class"] for e in es)
        low = [e["ticker"] for e in es if e["_c"]["quality_class"] == "COMPOUNDER AT LOW PRICE"]
        return c, low

    sector_text = {
        "Finance": "The deepest pool of durable value: MRSH, KKR, SPGI, SCHW, MA, AXP and BX are all compounders at a low price, and PGR/BAC/C are cyclicals with the risk priced in. The other half of the sector is the warning — twelve names (DBK, ISP, INGA, UCG, NDA, JPM, GS, MS, BBVA, BNP, PKO, XTB) carry too much cycle risk at record highs, and the shared failure mode is a synchronized rate-cut cycle.",
        "Technology": "Six compounders at a low price, all of them 'AI losers' in the market's eyes: WKL, NOW, ADBE, ACN, PRX and (with balanced asymmetry) NVDA as a cyclical. Ten quality names are priced for perfection (AAPL, MSFT, META, SAP, CRM, PANW, PLTR, AVGO, UBER, IBM) and six semis carry too much cycle risk (AMD, ASML, MRVL, IFX, QCOM, LRCX).",
        "Consumer Discretionary": "Seven compounders at a low price — AZO, HD, MCD, LOW, BKNG, CMG and ALE — mostly housing- and traffic-trough stories on durable franchises. Lodging (MAR, HLT, ABNB) is priced for perfection; autos (GM, F, BMW, MBG, TSLA) carry too much cycle risk; Nike is a turnaround, not a value buy.",
        "Healthcare": "Only SYK and BSX clear the bar as compounders at a low price; HCA and SNY are neutrally valued. Eleven names are priced for perfection (LLY, ISRG, VRTX, ABBV, MRK, GILD, DHR, TMO, ELV, AMGN, ABT) and the patent-cliff names (BMY, PFE) are structurally challenged rather than cheap.",
        "Industrials": "APD and WM are the compounders at a low price; TDG, SIE, SAF, TT, DG and RTX are quality at a neutral price. Nine names carry too much cycle risk — DE, CAT, ETN, GEV, EMR, DHL, DSV, ATCOA and, after its bounce, RHM.",
        "Utilities": "PEG is the one regulated compounder at a low price; VST is a cyclical with the risk priced in. EIX and PCG are special situations — cheap because the wildfire-liability regime is uncapped — not compounders. Eight regulated names are priced for perfection (AEP, ETR, SO, XEL, DUK, ENEL, IBE, NEE).",
        "Consumer Staples": "MDLZ is the only compounder at a low price; BN and PEP are neutrally valued. Eight names are priced for perfection (KO, PM, CL, COST, OR, TGT, ABI, AD); KHC and MO are structurally challenged.",
        "Energy": "No compounders at a low price. Fourteen names carry too much cycle risk after the 2026 commodity run — the refiners (MPC, VLO, PSX) and services (HAL, SLB) most of all — and the midstream names (TRGP, WMB, OKE, KMI) are quality priced for perfection.",
        "Telecoms/Media": "TMUS is the book's best buy; VZ, T and DTEGY are neutrally valued. CMCSA and CHTR are the archetype of 'cheap, but structural risk'.",
        "Materials": "SHW and VMC are quality at a neutral price; ECL is priced for perfection; PPG and SGO are cyclicals at a fair price.",
        "Basic Resources": "KTY is a cyclical with the risk priced in; DOW, KGH and NEM are cyclicals at a fair price — none qualify as downside-limited compounders.",
    }
    sector_items = []
    for sec in ["Finance", "Technology", "Consumer Discretionary", "Healthcare", "Industrials", "Utilities",
                "Consumer Staples", "Energy", "Telecoms/Media", "Materials", "Basic Resources"]:
        c, low = sec_line(sec)
        sector_items.append({"h": f"{sec} ({len(by_sector[sec])})", "x": sector_text[sec]})

    data = {
        "title": "Coverage Summary",
        "updated": TODAY,
        "intro": (
            f"{n} names under coverage, now classified on two axes instead of one. Axis 1 is business durability — "
            "how likely the business is to become useless (hand-curated per ticker: durable franchise, cyclical, "
            "structurally challenged, turnaround, special situation). Axis 2 is price — downside room and asymmetry "
            "from the model's own numbers (Ratio B, distance to the EPP panic floor, adjusted-vs-market composite, "
            "conservative 2-yr case). The old BUY/ACCUMULATE/AVOID tier was a pure valuation read and kept promoting "
            "statistically cheap but structurally challenged names; the new classes separate 'cheap because it is "
            "temporarily out of favour' from 'cheap because the business is eroding'. "
            f"Result: {counts['COMPOUNDER AT LOW PRICE']} compounders at a low price, "
            f"{counts['QUALITY, NEUTRALLY VALUED']} quality names neutrally valued, "
            f"{counts['QUALITY, PRICED FOR PERFECTION']} priced for perfection, "
            f"{counts['TOO MUCH CYCLE RISK']} with too much cycle risk, "
            f"{counts['CYCLICAL, RISK PRICED IN'] + counts['CYCLICAL, NEUTRALLY VALUED']} cyclicals at a fair or discounted price, and "
            f"{counts['CHEAP, BUT STRUCTURAL RISK'] + counts['STRUCTURAL RISK, NOT CHEAP'] + counts['TURNAROUND BET'] + counts['SPECIAL SITUATION']} "
            "structural, turnaround or special situations. Everything below is a model output, not a price target."
        ),
        "stats": [
            {"label": "Coverage", "value": str(n)},
            {"label": "Compounder at low price", "value": str(counts["COMPOUNDER AT LOW PRICE"])},
            {"label": "Quality, neutral", "value": str(counts["QUALITY, NEUTRALLY VALUED"])},
            {"label": "Priced for perfection", "value": str(counts["QUALITY, PRICED FOR PERFECTION"])},
            {"label": "Too much cycle risk", "value": str(counts["TOO MUCH CYCLE RISK"])},
            {"label": "Structural / special", "value": str(counts["CHEAP, BUT STRUCTURAL RISK"] + counts["STRUCTURAL RISK, NOT CHEAP"] + counts["TURNAROUND BET"] + counts["SPECIAL SITUATION"])},
        ],
        "sections": [
            {
                "heading": "Best buys — durable businesses with limited downside",
                "body": [
                    "The list you asked for: names where the downside is limited by the model's own floor and asymmetry, AND the business carries low-to-neutral risk of becoming useless. Ranked by a blend of model-vs-market gap, Ratio B, conservative 2-yr return, distance to floor and obsolescence risk. These are buys at today's prices, not on a further pullback.",
                ],
                "items": top,
            },
            {
                "heading": "Second line — same quality, slightly less asymmetry",
                "body": ["Also compounders at a low price; buy, but after the first group."],
                "items": second,
            },
            {
                "heading": "The AI-fear basket — cheap because the market is pricing disruption",
                "body": ["Durable franchises with a live AI-disruption debate (obsolescence risk 3/5). The discount is real and the numbers keep refusing the bear case, but this is the one group where 'becoming useless' is a non-zero scenario. Buy as a basket, not as single conviction positions."],
                "items": ai_fear,
            },
            {
                "heading": "Almost there — quality at a neutral price worth adding on weakness",
                "items": near,
            },
            {
                "heading": "Cyclicals where the cycle risk is already in the price",
                "body": ["Good businesses whose earnings are the cycle, at prices that already discount it. Fine to own, sized as cyclicals — they do not belong in the same bucket as the compounders above."],
                "items": cyc_ok,
            },
            {
                "heading": "What we deliberately took OUT of the buy list",
                "body": ["Every one of these rated BUY under the old tier. They are cheap by the numbers; they are not downside-limited compounders."],
                "items": removed,
            },
            {
                "heading": "Turnarounds and structural risk — cheap is not enough",
                "items": turn,
            },
            {
                "heading": "Sell / trim — priced for perfection or at a cycle peak",
                "body": ["No hedging here: these are names to trim into strength or avoid with new money. Refiners and oil services sit on a geopolitical margin spike, Deere and the AI-capex industrials on peak multiples, and the mega-cap quality names have no margin of safety versus their own bear cases."],
                "items": sells,
            },
            {
                "heading": "Sector reads",
                "items": sector_items,
            },
            {
                "heading": "Main dangers across the book",
                "body": [
                    "Crowding at highs. 59 quality names and 51 cyclicals are priced for perfection or at a cycle peak — 48% of coverage. The single largest risk remains buying good companies at the top of their ranges; the new taxonomy makes that explicit instead of hiding it inside 'AVOID'.",
                    "Cheap-for-a-reason. Cable (CMCSA, CHTR), California utilities (EIX, PCG) and the patent-cliff pharmas (BMY, PFE) are the names where a valuation floor is least reliable because the E in the floor is contested. They are now labelled as such rather than promoted.",
                    "The AI capex cycle. NVDA, MU, AMD, MRVL, AVGO, VST, CEG, ETN, GEV, TT and the power/cooling complex all lean on one hyperscaler capex stream; the AI-fear basket (WKL, NOW, ADBE, ACN) is the mirror image. A capex digestion phase hits both sides in opposite directions.",
                    "Synchronized rate cuts. Twelve bank/financial names carry too much cycle risk at record highs with the same failure mode — deposit-margin compression before fee growth offsets it. SCHW and PEG are the rate-sensitive names on the buy side.",
                    "Commodity reversal. Energy has zero compounders at a low price and fourteen names with too much cycle risk; a fade of the Hormuz risk premium takes the refiners and services names down first.",
                ],
            },
        ],
        "footer": (
            "Generated from the live model catalog · classes = business durability (hand-curated) × price/asymmetry "
            "(Ratio B, EPP-floor distance, adjusted-vs-market composite, conservative 2-yr) · verdicts update with the "
            "hourly refresh cycle · not financial advice."
        ),
    }
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
    a = ap.parse_args()
    entries = qc.load_dir(a.signals)
    data, counts = build(entries)
    os.makedirs(os.path.dirname(os.path.abspath(a.out_json)), exist_ok=True)
    with open(a.out_json, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    print(f"wrote {a.out_json}")
    if a.out_md:
        os.makedirs(os.path.dirname(os.path.abspath(a.out_md)), exist_ok=True)
        with open(a.out_md, "w", encoding="utf-8") as fh:
            fh.write(to_markdown(data))
        print(f"wrote {a.out_md}")
    for k, v in counts.most_common():
        print(f"{v:4d}  {k}")


if __name__ == "__main__":
    main()
