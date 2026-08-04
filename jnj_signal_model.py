"""
JNJ  ·  Johnson & Johnson  ·  NYSE: JNJ
Bottom-up signal model  ·  Innovative Medicine (Oncology/Immunology) / MedTech (Abiomed/EP/Ortho) / Talc Litigation
Date: 2026-08-04
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "JNJ"
COMPANY       = "Johnson & Johnson"
SECTOR        = "Pharma · Innovative Medicine (Darzalex/Carvykti/Tremfya) · MedTech (Abiomed/Varipulse/Ortho) · NYSE: JNJ"
CURRENT_PRICE = 254.41      # USD; close 2026-08-03
VOL_52W_LOW   = 166.64      # USD
VOL_52W_HIGH  = 274.90      # USD
SHARES_OUT_M  = 2_410.0     # millions
ANNUAL_DIV    = 5.36        # $/share; Dividend King (62+ yrs of increases)

# ── PRODUCT REVENUE BRIDGE (company-specific calculator, FY2027E) ────────────
# Q2 2026 actual (reported ~Jul 16): revenue $25.31B (+6.6% YoY, beat); adj EPS $2.90 (beat).
# FY2026 guidance: revenue ~$101.1-101.3B (first-ever $100B+ year), adj EPS ~$11.62-11.68.
# FY2027 consensus: revenue ~$108.4B, EPS ~$12.77.
# THE HEADLINE EVENT: on Jul 27, 2026, JNJ announced a $5.5B talc/ovarian-cancer litigation
# settlement covering ~69,000 federal MDL claims plus related state cases (~99.75% of all
# remaining claims), needing 95% claimant opt-in. First payment of up to $3B in 2027, none
# before 2028. This ends a decade-long overhang after three failed bankruptcy-strategy attempts
# — and is the direct cause of the stock's ~57% re-rating since this model's last refresh.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Oncology (Darzalex/Carvykti/Erleada)",       27.0, 22.0, 31.0, "Darzalex run-rate growth continuing; Carvykti CAR-T scaling off capacity expansion"),
    ("Immunology (Tremfya/Stelara biosim.)",       19.0, 15.0, 22.0, "Stelara biosimilar erosion largely lapping by FY2027; Tremfya + icotrokinra (ICP) launches driving net immunology growth"),
    ("Neuroscience/Pulmonary/Infectious Disease/Other Pharma", 16.0, 13.5, 19.0, "Spravato, Tremfya in IBD, smaller franchises; mixed growth"),
    ("MedTech - Cardiovascular (Abiomed/EP)",      18.0, 15.0, 22.0, "Abiomed Impella + Varipulse (PFA electrophysiology) — high-growth swing factor"),
    ("MedTech - Ortho/Surgery/Vision",             16.0, 14.0, 18.0, "Orthopedics stabilizing; Surgery/Vision steady mid-single-digit growth"),
    ("MedTech - Interventional Solutions/Other",   12.4, 10.5, 14.5, "Electrophysiology, interventional cardiology adjacencies"),
]

# Net-margin-based bridge
NET_MARGIN_CURR = 0.2839   # FY2027E normalized; litigation reserve drag largely behind
NET_MARGIN_BEAR = 0.2678   # BEAR: Stelara erosion outpaces offsets, settlement costs still weigh
NET_MARGIN_BULL = 0.2896   # BULL: Innovative Medicine mix shift + pipeline delivery expand margin

# ── TALC SETTLEMENT / STELARA TRANSITION TRACKER (the JNJ-specific angle) ────
Q2_2026_REVENUE_B          = 25.31   # $B, Q2 2026 actual reported revenue
Q2_2026_ADJ_EPS            = 2.90    # $ adjusted EPS, Q2 2026 (beat)
TALC_SETTLEMENT_B          = 5.5     # $B, total settlement announced Jul 27, 2026
TALC_CLAIMS_COVERED_PCT    = 99.75   # % of remaining claims covered
TALC_OPT_IN_REQUIRED_PCT   = 95      # % claimant opt-in required for settlement to proceed
FIRST_PAYMENT_MAX_B        = 3.0     # $B, maximum first payment (2027; none before 2028)
STOCK_MOVE_FROM_JUNE_LOW_PCT = round((CURRENT_PRICE - 162.50) / 162.50 * 100, 1)  # move since last refresh

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 12.77       # FY2027E EPS (consensus)
PE_PESSIMISTIC = 15.0        # trough P/E: now that talc is largely resolved, a higher floor than the old litigation-discount 13x
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (10.00, 15,  150, "Stelara erosion outpaces Tremfya/Carvykti ramp; MedTech growth stalls; opt-in threshold complications resurface litigation risk; EPS $10.00 → 15× = $150"),
    "BASE":  (12.77, 19.9, 254, "Stelara erosion offset by Tremfya/Darzalex/Carvykti growth; MedTech grows mid-to-high single digits; talc settlement proceeds as announced; EPS $12.77 → 19.9× = $254"),
    "BULL":  (15.20, 22,  334, "Carvykti capacity expansion + icotrokinra launch drive Innovative Medicine reacceleration; Varipulse PFA gains share; talc overhang fully behind; EPS $15.20 → 22× = $334"),
    "XBULL": (17.50, 25,  438, "Pipeline becomes a new growth engine; MedTech re-rates on Abiomed/EP momentum; multiple expands toward healthcare growth peers; EPS $17.50 → 25× = $438"),
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
        "name":       "Darzalex/Carvykti oncology revenue YoY growth",
        "weight":     0.25,
        "thresholds": ("<8%",   "≥15%",  "≥22%",   "≥30%"),
        "now":        "+16%",
        "score":      2,
        "comment":    "Darzalex run-rate growth continuing; Carvykti CAR-T scaling with capacity expansions; oncology remains core growth engine",
    },
    {
        "name":       "Stelara biosimilar erosion vs Tremfya/ICP offset",
        "weight":     0.25,
        "thresholds": ("erosion>offset", "roughly even", "Tremfya offsets", "net immunology growth"),
        "now":        "Tremfya +28%, Stelara -35%",
        "score":      3,
        "comment":    "Stelara erosion pace is slowing as it laps; Tremfya and icotrokinra (ICP) launches are now offsetting it at the segment level",
    },
    {
        "name":       "MedTech cardiovascular growth (Abiomed/Varipulse PFA)",
        "weight":     0.20,
        "thresholds": ("<3%",   "≥6%",   "≥10%",   "≥15%"),
        "now":        "+9%",
        "score":      2,
        "comment":    "Abiomed Impella steady growth; Varipulse PFA gaining traction in competitive electrophysiology market",
    },
    {
        "name":       "Talc litigation resolution progress",
        "weight":     0.15,
        "thresholds": ("escalating/unresolved", "ongoing/uncertain", "settlement framework progressing", "resolved at modest cost"),
        "now":        "resolved at modest cost",
        "score":      4,
        "comment":    "$5.5B settlement announced Jul 27, 2026 covers ~99.75% of remaining claims; ends a decade-long overhang, pending 95% claimant opt-in",
    },
    {
        "name":       "Pipeline productivity (icotrokinra, bispecifics, ortho)",
        "weight":     0.10,
        "thresholds": ("none",  "1 readout","2-3 readouts","4+ readouts"),
        "now":        "2-3",
        "score":      3,
        "comment":    "Icotrokinra (oral IL-23) progressing in psoriasis/IBD; oncology bispecifics advancing; ortho stabilization ongoing",
    },
    {
        "name":       "Balance sheet strength / capital return capacity",
        "weight":     0.05,
        "thresholds": ("<AA-",  "AA",  "AA+",   "AAA"),
        "now":        "AAA",
        "score":      4,
        "comment":    "One of only two AAA-rated US corporates; Dividend King (62+ consecutive years of increases)",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Talc litigation resolved via $5.5B settlement (Jul 2026) — a decade-long overhang removed, pending claimant opt-in", +0.5, 0.20),
    ("+", "AAA balance sheet + Dividend King — 62+ yr dividend growth streak provides downside floor and capital flexibility", +0.6, 0.20),
    ("-", "Stelara erosion still a drag even as the pace narrows; Tremfya/ICP offset not yet fully proven at scale",           -0.3, 0.15),
    ("+", "Diversification — Innovative Medicine + MedTech dual-engine model reduces single-franchise concentration risk vs peers", +0.4, 0.15),
    ("+", "Carvykti/Abiomed/Varipulse — multiple credible growth vectors across oncology, cell therapy, and cardiovascular MedTech", +0.3, 0.15),
    ("-", "Stock has already re-rated ~57% since June on the settlement news — much of that good news is now priced in",       -0.4, 0.15),
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
CONS_EPS_2YR  = 14.90   # FY2029E conservative: ~8%/yr off the FY2027E base
CONS_PE_2YR   = 19      # roughly flat vs. the BASE-case ~19.9× multiple
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Innovative Medicine (Oncology/Immunology) / MedTech / Talc Settlement")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2027E, normalized  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<44}  {'FY2027E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<44}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<44}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  Q2 2026 actual: revenue ${Q2_2026_REVENUE_B:.2f}B (+6.6% YoY, beat), adj EPS ${Q2_2026_ADJ_EPS:.2f} (beat)")
print()

# EPS bridge (net-margin based)
shares    = SHARES_OUT_M / 1000
curr_net  = curr_total * NET_MARGIN_CURR
curr_eps  = round(curr_net / shares, 2)

bull_net     = bull_total * NET_MARGIN_BULL
bull_eps_imp = round(bull_net / shares, 2)

bear_net     = bear_total * NET_MARGIN_BEAR
bear_eps_imp = round(bear_net / shares, 2)

print(f"  FY2027E EPS check:  ${curr_total:.1f}B rev × {NET_MARGIN_CURR*100:.2f}% net margin")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2027E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {NET_MARGIN_BULL*100:.2f}% net margin")
print(f"  ÷ {shares:.3f}B shares  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {NET_MARGIN_BEAR*100:.2f}% net margin (erosion outpaces offset, opt-in complications)")
print(f"  ÷ {shares:.3f}B shares  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# TALC SETTLEMENT TRACKER
print()
print(f"  TALC SETTLEMENT / STELARA TRANSITION TRACKER  (the JNJ-specific angle):")
print(f"  Talc settlement announced (Jul 27, 2026):     ${TALC_SETTLEMENT_B:.1f}B total")
print(f"  Claims covered:                                {TALC_CLAIMS_COVERED_PCT:.2f}% of remaining claims")
print(f"  Claimant opt-in required:                      {TALC_OPT_IN_REQUIRED_PCT}%  (settlement condition)")
print(f"  First payment (2027, none before 2028):         up to ${FIRST_PAYMENT_MAX_B:.1f}B")
print(f"  Stock move since last refresh (Jun 10):        +{STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}%")
print()
print(f"  This is the single biggest catalyst in this refresh: a $5.5B settlement that ends three")
print(f"  failed bankruptcy-strategy attempts and roughly a decade of talc litigation overhang. The")
print(f"  stock's +{STOCK_MOVE_FROM_JUNE_LOW_PCT:.0f}% move since June is a rational re-rating of a real risk removed — the open")
print(f"  question now is whether the 95% opt-in threshold is met, and how much of the good news is")
print(f"  already reflected at ${CURRENT_PRICE:.2f}, near the top of the 52-week range.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = 1.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at {NET_MARGIN_CURR*100:.1f}% margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*19.9:.2f}/share at 19.9× P/E")
print(f"  1pp net margin expansion (mix/scale):        +${curr_total*0.01/shares:.3f}/EPS  = +${curr_total*0.01/shares*19.9:.2f}/share at 19.9× P/E")
print(f"  Every 1 turn of P/E:                          ±${EPS_FY2027E:.2f}/share  ({EPS_FY2027E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Oncology / Immunology transition / MedTech / Talc litigation framework)")
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
    ("Darzalex/Carvykti oncology growth",  "+16%",   "<8%",    "Competitive entrants (bispecifics) pressure multiple myeloma share"),
    ("Stelara erosion vs Tremfya offset",  "Tremfya offsets", "erosion widens", "Tremfya/ICP launches underwhelm; immunology segment shrinks net"),
    ("MedTech cardiovascular growth",      "+9%",    "<3%",    "Varipulse PFA loses share to Boston Scientific/Medtronic"),
    ("Talc settlement completion",         "Resolved", "Opt-in fails", "95% claimant opt-in threshold not met, reopening litigation risk"),
    ("Pipeline readouts",                  "2-3",    "none",   "Icotrokinra/bispecific readouts disappoint or delay"),
    ("Net margin",                         "28.4%",  "<25%",   "Mix shift to lower-margin MedTech/generics-pressured immunology"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>16}  {bear_v:>9}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the 95% claimant opt-in threshold for the talc settlement is NOT met, reopening")
print(f"  the litigation overhang the market just re-rated the stock to remove — combined with Stelara")
print(f"  erosion outpacing Tremfya/icotrokinra offset and Varipulse losing ground to larger EP competitors.")
print(f"  Note: ${bear_price} is NOT permanent impairment — AAA balance sheet + Dividend King (${ANNUAL_DIV:.2f}/share)")
print(f"  provide a durable earnings floor even in this scenario.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           ${EPS_FY2027E:.2f}  (consensus)")
print(f"  Pessimistic P/E:                 {PE_PESSIMISTIC:.0f}×  (post-settlement trough; AAA-rated pharma floor, no longer talc-discounted to 12-13×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  JNJ trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a meaningfully higher multiple than")
print(f"  its talc-discounted ~14-15× seen through mid-2026, reflecting the settlement removing the")
print(f"  market's biggest single overhang. The open question is no longer 'will talc resolve' but")
print(f"  'how much of that resolution is already paid for' at current levels.")
print(f"  At {CONS_PE_2YR}× mid-cycle P/E: ${EPS_FY2027E:.2f} × {CONS_PE_2YR} = ${EPS_FY2027E*CONS_PE_2YR:.0f}  — roughly in line with current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: settlement proceeds as announced, multiple roughly flat)")
hr()
print(f"  Conservative FY2029E EPS:        ${CONS_EPS_2YR:.2f}  (~8%/yr off the FY2027E base; Stelara erosion fully lapped)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (roughly flat from the ~19.9× BASE-case multiple)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; Dividend King)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: with talc largely resolved, JNJ's remaining open questions are the pace of")
print(f"  Stelara erosion versus Tremfya/icotrokinra offset, and whether Carvykti/Abiomed/Varipulse keep")
print(f"  compounding. The conservative case is modestly positive but leans more on EPS growth than on")
print(f"  further multiple re-rating, since much of that re-rating already happened in July.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.16
beta        = 0.55
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock is up {STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}% since the last refresh (Jun 10) on the talc settlement")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  Dividend King, 62+ yrs of increases)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (still low; defensive AAA-rated healthcare staple)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (highly defensive; among lowest-beta large caps)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (a settlement opt-in failure or Stelara-erosion shock)")
print(f"  → 95% claimant opt-in confirmation is THE KEY near-term binary for the settlement to hold.")
print(f"  → Carvykti scaling + Varipulse PFA share gains are the KEY bull catalysts.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $220  |  Trim above $275")

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
print(f"  {valuation_label.lower()} by model standards. In plain terms: the talc settlement is a genuine, structural")
print(f"  positive — but the market has already paid up meaningfully for it, leaving a more balanced")
print(f"  risk/reward than the pre-settlement discount offered.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Talc settlement claimant opt-in — confirmation of the 95% threshold being met")
print(f"  (2) Stelara biosimilar erosion trajectory — pace vs Tremfya/icotrokinra immunology offset")
print(f"  (3) Carvykti capacity expansion — CAR-T manufacturing scale-up and share gains")
print(f"  (4) Varipulse PFA adoption — electrophysiology share gains vs Boston Scientific/Medtronic")
print(f"  (5) Icotrokinra (oral IL-23) Phase 3 readouts — psoriasis/IBD pipeline productivity")
print(f"  (6) Dividend sustainability — ${ANNUAL_DIV:.2f}/share payout; 62+ yr increase streak (Dividend King)")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $220  |  Trim above $275")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2027E EPS: ${EPS_FY2027E:.2f}")
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
