"""
GILD  ·  Gilead Sciences, Inc.  ·  NASDAQ: GILD
Bottom-up signal model  ·  HIV (Biktarvy/Lenacapavir-Yeztugo) / Oncology (Trodelvy/Kite/Arcellx) / Liver Disease / Veklury
Date: 2026-08-04
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "GILD"
COMPANY       = "Gilead Sciences, Inc."
SECTOR        = "Biopharma · HIV (Biktarvy/Lenacapavir-Yeztugo) · Oncology (Trodelvy/Kite/Arcellx) · Liver Disease · NASDAQ: GILD"
CURRENT_PRICE = 131.15      # USD; close 2026-08-03
VOL_52W_LOW   = 108.46      # USD
VOL_52W_HIGH  = 157.29      # USD
SHARES_OUT_M  = 1_240.0     # millions
ANNUAL_DIV    = 3.28        # $/share; steadily growing dividend

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# ⚠ Q2 2026 earnings report TONIGHT (Aug 4, after close, 4:30pm ET call) — not yet public.
# This model is built on Q1 2026 data and FY2026 guidance raised with Q1: total product
# sales $30.0-30.4B (up $400M); HIV sales growth ~8% (up from 6%). Yeztugo (lenacapavir PrEP)
# guidance was raised to $1B for 2026 — a genuine blockbuster-in-year-one confirmation.
# IMPORTANT: headline FY2026 EPS guidance shows a LOSS of ($1.05)-($0.65) due to ~$11.5B of
# acquired IPR&D charges from 2026 M&A (Arcellx, Ouro Medicines, Tubulis, ~$16B deployed
# total) — that is a GAAP/non-GAAP optical distortion, NOT a change in the underlying
# business, whose non-GAAP guidance is unchanged at $8.45-8.85. This model uses that
# underlying figure, not the headline loss. FDA accepted the NDA for the bictegravir/
# lenacapavir (BIC/LEN) combo with priority review — PDUFA Aug 27, 2026, just three weeks away.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("HIV - Biktarvy",                        14.5, 13.2, 15.2, "World's top-selling HIV regimen; durable share leader but nearing peak ahead of ~2033 patent cliff"),
    ("HIV - Lenacapavir/Yeztugo (PrEP+treat)",  1.0,  0.6,  2.8, "Guided to $1B in 2026 — a genuine blockbuster-in-year-one confirmation, not just early promise"),
    ("HIV - Descovy/other legacy",              2.0,  1.6,  2.2, "Descovy for PrEP cannibalized by lenacapavir over time; modest legacy decline"),
    ("Oncology (Trodelvy/Kite/Arcellx pipeline)", 6.5, 5.5,  7.8, "Trodelvy + Kite cell therapy growth, plus the newly-acquired Arcellx cell-therapy pipeline"),
    ("Liver Disease (Vemlidy/Hepcludex/HCV)",   2.3,  2.0,  2.5, "Stable HBV/HDV franchise; modest growth from Hepcludex international expansion"),
    ("Veklury (COVID antiviral)",               1.4,  0.6,  1.6, "Highly volatile, demand-driven by COVID hospitalization rates; structurally declining"),
    ("Other (inflammation, Ouro/Tubulis pipeline)", 2.5, 2.0, 3.0, "Newly-acquired Ouro Medicines/Tubulis pipeline assets plus legacy other products"),
]

# Net-margin-based bridge
NET_MARGIN_CURR = 0.3552   # FY2026E underlying business (ex-IPR&D acquisition charges)
NET_MARGIN_BEAR = 0.3161   # BEAR: lenacapavir launch stalls, Biktarvy erosion, IPR&D drag continues
NET_MARGIN_BULL = 0.4063   # BULL: lenacapavir scales rapidly, BIC/LEN approval, high-margin mix shift

# ── LENACAPAVIR/BIC-LEN LAUNCH TRACKER (the Gilead-specific angle) ────────────
YEZTUGO_2026_GUIDANCE_B     = 1.0    # $B, raised FY2026 Yeztugo (lenacapavir PrEP) guidance
FY2026_PRODUCT_SALES_RANGE  = "30.0-30.4"  # $B, raised guidance range
FY2026_UNDERLYING_EPS_RANGE = "8.45-8.85"  # $ non-GAAP, underlying business (ex-IPR&D charges)
IPR_AND_D_CHARGES_B         = 11.5   # $B, acquired IPR&D charges distorting headline EPS
MA_SPEND_2026_B             = 16.0   # $B, total 2026 M&A deployed (Arcellx, Ouro Medicines, Tubulis)
BIC_LEN_PDUFA_DATE          = "2026-08-27"  # just three weeks away
Q2_EARNINGS_DATE            = "2026-08-04 (TONIGHT, after close)"
STOCK_MOVE_FROM_JUNE_LOW_PCT = round((CURRENT_PRICE - 108.50) / 108.50 * 100, 1)  # move since last refresh

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 8.65        # FY2026E underlying non-GAAP EPS ($8.45-8.85 guidance midpoint, ex-IPR&D charges)
PE_PESSIMISTIC = 10.0        # pessimistic P/E: below the current ~15.2× multiple; patent-cliff-discount floor
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (6.50, 10,   65, "Lenacapavir/Yeztugo launch stalls despite the raised guide; Biktarvy faces earlier competitive erosion; 2026 M&A integration proves costly; EPS $6.50 → 10× = $65"),
    "BASE":  (8.65, 15.16, 131, "Yeztugo tracks its raised $1B guide; Biktarvy holds share near-term; Trodelvy/Kite/Arcellx grow steadily; EPS $8.65 → 15.2× = $131"),
    "BULL":  (11.50, 16,  184, "BIC/LEN combo approved (PDUFA Aug 27) and adds a second lenacapavir franchise; Yeztugo scales past $1B; oncology beats on Arcellx integration; EPS $11.50 → 16× = $184"),
    "XBULL": (14.00, 19,  266, "Lenacapavir achieves blockbuster-of-blockbusters status across PrEP and treatment, effectively replacing Biktarvy's eventual decline 1-for-1; Kite/Trodelvy/Arcellx reach new-franchise scale; EPS $14.00 → 19× = $266"),
}

# ── SOFTMAX PROBABILITY FUNCTION ─────────────────────────────────────────────
CENTERS = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
T = 0.60

def softmax_probs(c):
    raw = {s: math.exp(-abs(c - CENTERS[s]) / T) for s in CENTERS}
    tot = sum(raw.values())
    return {s: raw[s] / tot for s in raw}

def expected_value(c):
    p = softmax_probs(c)
    return sum(p[s] * SCENARIOS[s][2] for s in SCENARIOS)

def back_solve_market_composite(price, tol=0.001):
    target = price * (1.15 ** 2)
    lo, hi = 1.0, 4.0
    for _ in range(80):
        m = (lo + hi) / 2
        if expected_value(m) < target:
            lo = m
        else:
            hi = m
    return round((lo + hi) / 2, 2)

# ── 6 PROXY SIGNALS ───────────────────────────────────────────────────────────
# Scores: 1=BEAR  2=BASE  3=BULL  4=XBULL
SIGNALS = [
    {
        "name":       "Lenacapavir/Yeztugo PrEP launch trajectory",
        "weight":     0.30,
        "thresholds": ("uptake stalls", "slow but building", "ramping to multi-$B run rate", "blockbuster (>$5B) trajectory confirmed"),
        "now":        "$1B guided in year one",
        "score":      3,
        "comment":    "Management RAISED 2026 Yeztugo guidance to $1B — a genuine blockbuster-in-year-one confirmation, not just early promise",
    },
    {
        "name":       "Biktarvy revenue durability vs patent cliff (~2033)",
        "weight":     0.20,
        "thresholds": ("declining now", "flat/low-single-digit growth", "mid-single-digit growth", "share gains accelerating"),
        "now":        "+low single digit",
        "score":      2,
        "comment":    "Biktarvy remains the dominant HIV regimen with continued share gains, but growth is decelerating as the franchise approaches peak",
    },
    {
        "name":       "Oncology (Trodelvy/Kite/Arcellx) growth",
        "weight":     0.15,
        "thresholds": ("<3%",  "≥6%",  "≥12%",   "≥20%"),
        "now":        "+9%",
        "score":      2,
        "comment":    "Trodelvy label expansions and Kite cell therapy growth, now joined by the newly-acquired Arcellx pipeline",
    },
    {
        "name":       "Veklury (COVID antiviral) revenue trend",
        "weight":     0.10,
        "thresholds": ("rising/volatile upside", "stable", "declining as expected", "collapsing faster than modeled"),
        "now":        "declining as expected",
        "score":      2,
        "comment":    "Veklury continues its structural decline as COVID hospitalizations normalize",
    },
    {
        "name":       "Pipeline depth + 2026 M&A (BIC/LEN, Arcellx, Ouro, Tubulis)",
        "weight":     0.10,
        "thresholds": ("thin",  "1-2 readouts","3-4 readouts","5+ readouts/approvals"),
        "now":        "BIC/LEN PDUFA imminent + $16B M&A expansion",
        "score":      3,
        "comment":    "BIC/LEN combo NDA accepted with priority review (PDUFA Aug 27, three weeks away), plus ~$16B deployed on Arcellx/Ouro Medicines/Tubulis expanding the pipeline meaningfully",
    },
    {
        "name":       "Balance sheet strength / capital return capacity",
        "weight":     0.15,
        "thresholds": ("<BBB+", "BBB+/A-", "A",   "A+/AA-"),
        "now":        "A, post-$16B M&A spend",
        "score":      2,
        "comment":    "Still investment-grade, but the heavy 2026 M&A deployment (~$16B) reduces near-term balance sheet flexibility versus a year ago",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Lenacapavir/Yeztugo optionality — now guided to $1B in year one; the addressable global PrEP market remains massive and underserved", +0.7, 0.25),
    ("-", "Biktarvy concentration risk — single product remains a large share of revenue; 2033 patent cliff is a real long-dated overhang", -0.5, 0.20),
    ("+", "Cash-generative HIV franchise provides a durable floor, though the ~$16B 2026 M&A spend has reduced near-term balance sheet flexibility", +0.3, 0.20),
    ("-", "Veklury volatility — COVID-driven revenue remains unpredictable and structurally shrinking, creating near-term EPS noise", -0.3, 0.10),
    ("+", "Oncology diversification (Trodelvy/Kite) plus the new Arcellx cell-therapy pipeline broadens beyond single-franchise HIV concentration", +0.4, 0.15),
    ("-", "Execution/access risk on lenacapavir global rollout remains, though the raised $1B guide meaningfully de-risks the near-term launch curve", -0.3, 0.10),
]
SCA = sum(score * weight for _, _, score, weight in SCA_FACTORS)
ADJ_COMPOSITE = round(PROXY_COMPOSITE + SCA, 3)

MARKET_COMPOSITE = back_solve_market_composite(CURRENT_PRICE)
ADJ_GAP = round(ADJ_COMPOSITE - MARKET_COMPOSITE, 2)

if ADJ_GAP > 0.20:
    valuation_label = "UNDERVALUED"
elif ADJ_GAP > -0.20:
    valuation_label = "FAIRLY VALUED"
else:
    valuation_label = "OVERVALUED"

# ── RATIO B ───────────────────────────────────────────────────────────────────
bear_price   = SCENARIOS["BEAR"][2]
bull_price   = SCENARIOS["BULL"][2]
downside_pct = (CURRENT_PRICE - bear_price) / CURRENT_PRICE
upside_pct   = (bull_price - CURRENT_PRICE) / CURRENT_PRICE
ratio_b      = round(downside_pct / upside_pct, 2) if upside_pct > 0 else float("inf")

if ratio_b != float("inf") and ratio_b < 0.75:
    signal_short, signal_full = "BUY",       "◉ BUY"
elif ratio_b != float("inf") and ratio_b < 1.10:
    signal_short, signal_full = "ACCUMULATE","◎ ACCUMULATE"
elif ratio_b != float("inf") and ratio_b < 1.75:
    signal_short, signal_full = "WATCHLIST", "◐ WATCHLIST"
else:
    signal_short, signal_full = "AVOID",     "✕ AVOID"

ratio_b_str = f"{ratio_b:.2f}x" if ratio_b != float("inf") else "N/A"

# ── CONSERVATIVE GROWTH (2-yr) ────────────────────────────────────────────────
CONS_EPS_2YR  = 10.20   # FY2028E conservative: ~8.5%/yr off FY2026E, lenacapavir continuing to ramp
CONS_PE_2YR   = 13      # a modest re-rate from the current ~15.2×
cons_equity   = CONS_EPS_2YR * CONS_PE_2YR
cons_divs     = ANNUAL_DIV * 2
cons_total    = cons_equity + cons_divs
cons_return   = round((cons_total - CURRENT_PRICE) / CURRENT_PRICE * 100, 1)
cons_annual   = round(cons_return / 2, 1)

# ─────────────────────────────────────────────────────────────────────────────
#  OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
W = 72

def hr(): print("  " + "─" * W)
def bar(score):
    return "█" * score + "░" * (4 - score)

print()
print("═" * (W + 4))
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  HIV (Biktarvy/Lenacapavir-Yeztugo) / Oncology / Liver Disease")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<46}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<46}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<46}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  FY2026 guidance: total product sales ${FY2026_PRODUCT_SALES_RANGE}B; Yeztugo raised to ${YEZTUGO_2026_GUIDANCE_B:.1f}B")
print(f"  ⚠ Q2 2026 earnings report {Q2_EARNINGS_DATE} — the next confirmation point for this model")
print()

# EPS bridge (net-margin based)
shares    = SHARES_OUT_M / 1000
curr_net  = curr_total * NET_MARGIN_CURR
curr_eps  = round(curr_net / shares, 2)

bull_net     = bull_total * NET_MARGIN_BULL
bull_eps_imp = round(bull_net / shares, 2)

bear_net     = bear_total * NET_MARGIN_BEAR
bear_eps_imp = round(bear_net / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {NET_MARGIN_CURR*100:.2f}% net margin")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (underlying guidance ${EPS_FY2026E:.2f} midpoint  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {NET_MARGIN_BULL*100:.2f}% net margin")
print(f"  ÷ {shares:.3f}B shares  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {NET_MARGIN_BEAR*100:.2f}% net margin (launch stalls + IPR&D drag persists)")
print(f"  ÷ {shares:.3f}B shares  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# LENACAPAVIR/BIC-LEN TRACKER
print()
print(f"  LENACAPAVIR/BIC-LEN LAUNCH TRACKER  (the Gilead-specific angle):")
print(f"  Yeztugo (lenacapavir PrEP) 2026 guidance:      ${YEZTUGO_2026_GUIDANCE_B:.1f}B  (raised — blockbuster in year one)")
print(f"  FY2026 underlying non-GAAP EPS guidance:        ${FY2026_UNDERLYING_EPS_RANGE}  (ex-IPR&D charges)")
print(f"  Acquired IPR&D charges (headline EPS distortion): ${IPR_AND_D_CHARGES_B:.1f}B")
print(f"  Total 2026 M&A deployed (Arcellx/Ouro/Tubulis):  ${MA_SPEND_2026_B:.0f}B")
print(f"  BIC/LEN combo PDUFA date:                        {BIC_LEN_PDUFA_DATE}  (~3 weeks away)")
print(f"  Stock move since last refresh (Jun 10):          +{STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}%")
print()
print(f"  IMPORTANT: GILD's headline FY2026 EPS guidance shows a LOSS due to ~$11.5B of acquired")
print(f"  IPR&D charges from this year's M&A spree — that is pure accounting noise from the deals,")
print(f"  not a change in the underlying business, whose non-GAAP guidance actually held steady at")
print(f"  ${FY2026_UNDERLYING_EPS_RANGE}. This model uses that underlying figure throughout.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = 1.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at {NET_MARGIN_CURR*100:.1f}% margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*15.16:.2f}/share at 15.2× P/E")
print(f"  1pp net margin expansion (mix/scale):        +${curr_total*0.01/shares:.3f}/EPS  = +${curr_total*0.01/shares*15.16:.2f}/share at 15.2× P/E")
print(f"  Every 1 turn of P/E:                          ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Lenacapavir launch / Biktarvy durability / Oncology / Veklury / Pipeline+M&A / Balance sheet)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>5}  {'BASE':>5}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>6}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>5}  {ths[1]:>5}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>6}  {lbl}  {b}")
    print(f"    {s['comment']}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15% hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:72]:<72}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<52}  {'Current':>16}  {'Bear val':>9}  Trigger")
hr()
bear_triggers = [
    ("Lenacapavir/Yeztugo launch trajectory", "$1B guided",   "uptake stalls", "Payer access/pricing friction stunts the launch curve despite the raised guide"),
    ("Biktarvy revenue trend",                "+low-sd",      "declining now", "Earlier-than-expected competitive/generic pressure erodes Biktarvy share"),
    ("Oncology (Trodelvy/Kite/Arcellx) growth", "+9%",         "<3%",   "Trodelvy/Kite lose ground to competitive ADCs/CAR-Ts; Arcellx integration disappoints"),
    ("Veklury revenue",                       "declining as expected", "collapsing faster", "COVID hospitalizations fall faster than modeled"),
    ("BIC/LEN PDUFA outcome",                 "pending (Aug 27)", "CRL/delay", "FDA issues a complete response letter or delays the priority review decision"),
    ("Net margin",                            "35.5%",        "<30%",  "IPR&D-related and integration costs from the $16B M&A spree persist longer than modeled"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>16}  {bear_v:>9}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Lenacapavir/Yeztugo's launch stalls despite the raised $1B guide, Biktarvy begins")
print(f"  facing earlier-than-expected competitive erosion, and the BIC/LEN combo receives a complete")
print(f"  response letter instead of approval. EPS falls to ~$6.50 → 10× trough P/E (patent-cliff floor).")
print(f"  Note: ${bear_price} is NOT permanent impairment — Gilead's HIV franchise remains highly")
print(f"  cash-generative with an A-rated balance sheet and growing dividend (${ANNUAL_DIV:.2f}/share).")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E underlying EPS estimate: ${EPS_FY2026E:.2f}  (${FY2026_UNDERLYING_EPS_RANGE} guidance midpoint, ex-IPR&D charges)")
print(f"  Pessimistic P/E:                  {PE_PESSIMISTIC:.0f}×  (below the current ~15.2× multiple; patent-cliff-discount floor)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  GILD trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E underlying EPS ${EPS_FY2026E:.2f} — a real re-rating from its")
print(f"  historical single-digit trough, reflecting genuine confidence in the lenacapavir franchise")
print(f"  after the $1B Yeztugo guide raise. The BIC/LEN PDUFA decision on {BIC_LEN_PDUFA_DATE} is the")
print(f"  next near-term catalyst, alongside tonight's Q2 print.")
print(f"  At 16× mid-cycle P/E (BIC/LEN approved, lenacapavir scaling): ${EPS_FY2026E:.2f} × 16 = ${EPS_FY2026E*16:.0f}  — {(EPS_FY2026E*16/CURRENT_PRICE-1)*100:+.0f}% vs current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: lenacapavir continues ramping, modest re-rate)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (~8.5%/yr off FY2026E)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (a modest re-rate from the current ~15.2×)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: the lenacapavir/Yeztugo story just got real confirmation via the raised")
print(f"  $1B guide, and BIC/LEN's PDUFA decision is only weeks away. The stock has already re-rated")
print(f"  meaningfully since June to reflect this — the conservative case is modest but positive.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.22
beta        = 0.50
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock is up {STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}% since the last refresh (Jun 10) on the Yeztugo guide raise")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  steadily growing payout)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (moderate; defensive HIV franchise offset by launch/M&A headlines)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (low-beta defensive large-cap biopharma)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (significant; lenacapavir-launch-stall + BIC/LEN-rejection tail scenario)")
print(f"  → Tonight's Q2 print AND the BIC/LEN PDUFA decision ({BIC_LEN_PDUFA_DATE}) are THE KEY near-term catalysts.")
print(f"  → Biktarvy quarterly trends and Yeztugo's actual ramp vs the $1B guide are the KEY ongoing signals.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $115  |  Trim above $150")

# ─── ⑦ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print()
print("  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
hr()
probs_mkt = softmax_probs(MARKET_COMPOSITE)
print(f"  {'Scenario':<10}  {'Price':>7}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>7}  Description")
hr()
for s in ["BEAR","BASE","BULL","XBULL"]:
    pp  = probs_proxy[s] * 100
    pm  = probs_mkt[s]   * 100
    gap = pp - pm
    pr  = SCENARIOS[s][2]
    desc = SCENARIOS[s][3][:46]
    print(f"  {s:<10}  ${pr:>6}  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): ${ev_adj:.0f}  /  Proxy EV: ${ev_prx:.0f}  /  Market EV: ${ev_mkt:.0f}  /  Current: ${CURRENT_PRICE:.0f}")
hr()
print(f"  Downside  (→ Bear ${bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull ${bull_price}):  {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b_str}")
print(f"  Signal    :  {signal_full}")
print()
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is")
print(f"  {'ABOVE' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'BELOW'} the model's adj composite ({ADJ_COMPOSITE:.3f}). The gap ({ADJ_GAP:+.2f}) indicates the stock is")
print(f"  {valuation_label.lower()} by model standards. In plain terms: the lenacapavir story just crossed from")
print(f"  'promising launch' to 'guided $1B franchise,' and BIC/LEN's approval decision is weeks away —")
print(f"  tonight's Q2 print is the next data point.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q2 2026 earnings — {Q2_EARNINGS_DATE}")
print(f"  (2) BIC/LEN combo PDUFA decision — {BIC_LEN_PDUFA_DATE}, priority review")
print(f"  (3) Lenacapavir/Yeztugo quarterly ramp — tracking vs the raised $1B guide")
print(f"  (4) Biktarvy revenue trend — durability of share leadership ahead of ~2033 patent cliff")
print(f"  (5) 2026 M&A integration — Arcellx, Ouro Medicines, Tubulis (~$16B deployed)")
print(f"  (6) Dividend growth — ${ANNUAL_DIV:.2f}/share payout; capital return capacity from HIV cash flows")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $115  |  Trim above $150")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}")
print("═" * (W + 4))
print()

# ── EXPORT ────────────────────────────────────────────────────────────────────
RESULT = {
    "ticker":            TICKER,
    "signal":            signal_full,
    "signal_short":      signal_short,
    "price":             CURRENT_PRICE,
    "epp_gap_pct":       epp_gap_pct,
    "ratio_b":           ratio_b if ratio_b != float("inf") else None,
    "ratio_b_fmt":       ratio_b_str,
    "adj_composite":     ADJ_COMPOSITE,
    "market_composite":  MARKET_COMPOSITE,
    "adj_gap":           ADJ_GAP,
    "valuation":         valuation_label,
    "cons_return_2yr":   cons_return,
}

if __name__ == "__main__":
    pass
