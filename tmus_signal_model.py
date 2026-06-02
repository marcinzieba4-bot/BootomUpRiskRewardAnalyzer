"""
T-Mobile US, Inc. (NASDAQ: TMUS) — Bottom-Up Risk/Reward Signal Model
BottomUp Risk/Reward Analyzer · veerock framework
Date: 2026-06-02

NOTE: TMUS is a FCF compounder trading 29% below its March 2025 all-time high ($266.80).
Fundamentals are ACCELERATING (+8% service rev FY2025, +11% Q1 2026 YoY), yet the market
prices the stock near BASE/BEAR — implying concern over cable MVNO structural shift and $83B
net debt. The 2.5 GHz mid-band spectrum position (110 MHz depth vs 40-60 MHz for peers) is
an irreplaceable decade-long moat that cannot be replicated without a multi-billion
spectrum acquisition. FWA adds ~2M/yr at near-zero incremental capex = structural margin
expansion. $18.2B in shareholder returns authorized for 2026 alone.
"""

# ── PRICE & MARKET DATA ───────────────────────────────────────────────────────
TICKER           = "TMUS"
COMPANY          = "T-Mobile US, Inc."
SECTOR           = "Wireless · Fixed Wireless Access · 5G · Fiber (Lumos JV) · NASDAQ: TMUS"
DATE             = "2026-06-02"
CURRENT_PRICE    = 187.53
VOL_52W_LOW      = 181.36
VOL_52W_HIGH     = 261.56    # All-time high close $266.80, March 3, 2025; currently -29.6%
SHARES_OUT_M     = 1086.0    # Diluted, March 31, 2026; -3.59% YoY from buybacks
ANNUAL_DIV       = 4.08      # $1.02/quarter; 2.2% yield; initiated Q4 2023; ~10%/yr growth target

# ── FIXED WIRELESS ACCESS — THE STRUCTURAL GROWTH ENGINE ─────────────────────
# T-Mobile owns ~60% of all US fixed wireless subscribers — effectively a cable
# broadband alternative built entirely on spectrum already deployed for cellular.
# Incremental revenue at near-zero capex = structurally accretive to margins.
FWA_SUBS_YE2025_M     = 8.5     # Up from 6.4M YE2024 (+1.9M net adds in FY2025)
FWA_ADDS_Q1_2026      = 0.500   # >500K broadband net adds Q1 2026 (accelerating)
FWA_TARGET_2030_M     = 15.0    # Management target raised from 12M by 2028 → 15M by 2030
FWA_MARKET_SHARE      = 0.60    # ~60% of all US FWA subscribers (Verizon ~30%, others ~10%)
FWA_ARPU_MONTHLY      = 55.0    # Estimated monthly ARPU for FWA; ~$660/yr
# At 15M subs × $660/yr ARPU = $9.9B incremental service revenue vs near-zero added capex

# ── WIRELESS SUBSCRIBERS ─────────────────────────────────────────────────────
POSTPAID_PHONE_ADDS_FY2024 = 3.077   # Organic postpaid phone net adds FY2024
POSTPAID_PHONE_ADDS_FY2025 = 3.3     # Organic FY2025 (ex-UScellular); ~3.287M UScellular added Q3 2025
POSTPAID_CHURN_FY2024      = 0.0086  # 0.86% — best full-year in company history
POSTPAID_ARPA_Q1_2026      = 151.93  # +3.9% YoY Q1 2026
TOTAL_CUSTOMERS_YE2025_M   = 142.4   # Total customers YE2025 (incl. UScellular; #2 US carrier)

# ── USCELLULAR ACQUISITION ────────────────────────────────────────────────────
# Closed August 1, 2025. Adds Midwest/rural coverage + 600 MHz and AWS spectrum.
USCELLULAR_CLOSED    = "August 1, 2025"
USCELLULAR_PRICE_B   = 4.4     # Total consideration
USCELLULAR_POSTPAID_PHONE_M = 3.287  # Postpaid phone customers acquired in Q3 2025

# ── LUMOS FIBER JOINT VENTURE ─────────────────────────────────────────────────
# T-Mobile + EQT acquired Lumos Networks (April 2025) — first T-Mobile fiber footprint.
# Complements FWA in dense urban markets where fiber economics are superior.
LUMOS_HOMES_NOW_M    = 0.475   # Existing homes passed at close
LUMOS_HOMES_2028_M   = 3.5     # Target homes passed by end-2028
LUMOS_STATUS         = "T-Mobile Fiber launched to 500K+ households post-close"

# ── SPRINT MERGER SYNERGIES ───────────────────────────────────────────────────
# The Sprint merger delivered T-Mobile's defining structural asset: 2.5 GHz spectrum.
SPRINT_SYNERGIES_TARGET_B   = 7.5   # Original annual run-rate target
SPRINT_SYNERGIES_ACTUAL_B   = 8.0   # Actual run-rate delivered (exceeded)
SPRINT_SYNERGIES_NPV_ORIG_B = 43.0  # Original NPV estimate
SPRINT_SYNERGIES_NPV_REV_B  = 70.0  # Revised NPV (>63% upgrade over original)
SPRINT_INTEGRATION_STATUS   = "Substantially complete (Q2 2024)"

# ── SPECTRUM POSITION ─────────────────────────────────────────────────────────
# T-Mobile's 2.5 GHz is the key structural differentiator vs AT&T and Verizon.
# More MHz depth = more capacity = faster speeds = better FWA economics.
TMUS_MIDBAND_MHZ     = 110    # Up to 110 MHz of 2.5 GHz in dense markets (Sprint legacy)
VZN_MIDBAND_MHZ      = 60     # Verizon C-band (3.7 GHz); shorter propagation range
ATT_MIDBAND_MHZ      = 40     # AT&T C-band + 3.45 GHz; more limited
UC5G_COVERAGE_M      = 300    # Americans covered by Ultra Capacity (mid-band) 5G
# Starlink satellite-to-cellular partnership: backup coverage for dead zones

# ── DEUTSCHE TELEKOM SITUATION ────────────────────────────────────────────────
DT_OWNERSHIP_PCT     = 53     # Deutsche Telekom owns ~53% of TMUS
DT_MARKET_CAP_B      = 135    # DT Frankfurt ~€135B market cap; >70% is TMUS value
DT_MERGER_STATUS     = ("Early-stage talks (April 21-22, 2026) for full all-share combination "
                         "via new neutral holding company (Ireland structure, Linde/Praxair model). "
                         "Combined entity: ~$300B+ market cap, 200M+ mobile subs, world's largest telecom.")
CEO_CHANGE           = "Mike Sievert retired Nov 2025; Srini Gopalan (ex-DT Germany CEO, TMUS COO) appointed"

# ── FINANCIALS ────────────────────────────────────────────────────────────────
# FY2025 Full Year (reported February 10, 2026)
SERVICE_REV_FY2025_B       = 71.3    # +8% YoY; first year above $70B
CORE_ADJ_EBITDA_FY2025_B   = 33.9    # +7% YoY
ADJ_FCF_FY2025_B           = 18.0    # +6% YoY; 25% FCF margin (AT&T ~14%, VZ ~13%)
NET_INCOME_FY2025_B        = 11.0
GAAP_EPS_FY2025            = 9.72
NET_CASH_FROM_OPS_FY2025_B = 28.0    # +25% YoY

# Q1 2026 (most recent quarter, reported April 28-29, 2026)
SERVICE_REV_Q1_2026_B      = 18.8    # +11% YoY — accelerating from FY2025's +8%
CORE_ADJ_EBITDA_Q1_2026_B  = 9.2     # +12% YoY — positive operating leverage
ADJ_FCF_Q1_2026_B          = 4.6     # +5% YoY

# FY2026 Guidance (raised after Q1 2026 beat)
SERVICE_REV_FY2026E_B      = 77.0    # +8% guidance
CORE_ADJ_EBITDA_FY2026E_B  = 37.3    # Midpoint of $37.1–$37.5B
ADJ_FCF_FY2026E_B          = 18.4    # Midpoint of $18.1–$18.7B

# Consensus EPS estimates
ADJ_EPS_FY2026E    = 10.60    # Wall Street consensus ~$10.51–$10.70
ADJ_EPS_FY2028E    = 17.25    # 3-year forward consensus

# Capital returns
BUYBACK_AUTH_2026_B         = 18.2   # Board raised to $18.2B for 2026 (Feb 2026 CMD)
TOTAL_RETURNS_SINCE_2024_B  = 20.0   # >$20B since Capital Markets Day 2024 ($34.7B buybacks + $7B div since inception)

# Balance sheet (Q4 2025)
TOTAL_DEBT_EX_TOWERS_B = 88.6
CASH_B                 = 5.6
NET_DEBT_B             = 83.0    # = 88.6 - 5.6
LEVERAGE               = round(NET_DEBT_B / CORE_ADJ_EBITDA_FY2025_B, 2)   # ≈ 2.45×
# Covenant max 4.5×; Verizon ~3.2×; AT&T ~3.0× — T-Mobile is least leveraged major carrier
FCF_YIELD              = round(ADJ_FCF_FY2025_B / (CURRENT_PRICE * SHARES_OUT_M / 1000) * 100, 1)
# ≈ 8.9% — one of highest FCF yields in large-cap US equities

# ── EPP (EARNINGS POWER PRICE) ────────────────────────────────────────────────
# Trough case: cable MVNO pressure accelerates, ARPU growth stalls, FWA growth disappoints.
# EPS stays flat/declines slightly from FY2025 $9.72 GAAP EPS.
# T-Mobile at distress still earns growing EBITDA ($30B+ even in bear) → trough P/E 13×.
EPS_TROUGH   = 8.50    # FY2025 $9.72; trough assumes ARPU -3%/yr + market saturation
PE_TROUGH    = 13      # T-Mobile floor multiple; wireless duopoly economics even in bear
EPP          = EPS_TROUGH * PE_TROUGH    # = $110.50
EPP_GAP_PCT  = round((CURRENT_PRICE / EPP - 1) * 100, 1)   # +69.6%
# Positive EPP gap: stock is 70% ABOVE the floor → real downside to EPP in bear scenario
# Unlike CMCSA (below floor), TMUS is above EPP — investment case is ASYMMETRIC UPSIDE

# ── SCENARIO ASSUMPTIONS ─────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (9.00, 13, 120,
              "Cable MVNOs capture 60%+ of phone adds; FWA growth stalls at 10M; DT merger "
              "collapses; rates stay elevated → refinancing pressure on $83B debt; EPS flat "
              "at $9.00 (no growth from FY2025 $9.72). At 13× trough P/E: $117 → $120."),
    "BASE":  (12.50, 20, 250,
              "FWA grows to 13M by 2028; service revenue +8-9%/yr; EBITDA margin expands to "
              "48-50%; EPS $12.50 FY2027E × 20× → $250. Tracks analyst consensus PT range."),
    "BULL":  (15.00, 22, 330,
              "FWA on track for 15M by 2030; Lumos fiber JV accretive; DT merger catalyst; "
              "cable MVNO wholesale revenue offsets retail cannibalization; "
              "EPS $15.00 FY2028E × 22× → $330."),
    "XBULL": (18.00, 25, 450,
              "DT full combination completed (new holding company); T-Mobile part of "
              "200M-sub global telecom; FWA 15M; Lumos 3.5M fiber homes; "
              "EPS $18.00 × 25× → $450."),
}

# ── SOFTMAX SIGNAL MODEL ──────────────────────────────────────────────────────
PROXY_SIGNALS = [
    # (name, value [1=BEAR/2=BASE/3=BULL/4=XBULL], weight, description)
    ("fwa_secular_growth",         3.0, 0.25,
     "8.5M FWA subscribers (60% US market share); Q1 2026 adds >500K (accelerating from "
     "FY2025's 1.9M); target 15M by 2030. Zero incremental capex — spectrum already deployed. "
     "Pure incremental EBITDA. FWA ARPU ~$55/mo × 15M = ~$9.9B annual revenue optionality."),
    ("service_revenue_acceleration", 3.0, 0.25,
     "Service revenue +8% FY2025, +11% Q1 2026 YoY (acceleration). EBITDA +12% Q1 2026. "
     "FY2026 guidance raised: EBITDA $37.1-37.5B, FCF $18.1-18.7B. Positive operating leverage "
     "emerging. Postpaid ARPA $151.93 (+3.9% YoY) — pricing power confirmed in soft market."),
    ("capital_return_flywheel",    3.0, 0.20,
     "$18.2B buyback authorization in 2026 alone (~9% of market cap). Shares declining "
     "3.6%/yr compounding. Dividend $4.08/yr growing ~10%/yr (started Q4 2023). "
     "8.9% FCF yield. $18B FCF self-funds returns + deleveraging simultaneously."),
    ("postpaid_momentum_vs_cable_mvno_risk", 2.0, 0.15,
     "Organic postpaid phone adds ~3.3M/yr (#1 in US). Churn record-low 0.86%. "
     "UScellular closed Aug 1, 2025 (+3.3M postpaid phones + Midwest spectrum). "
     "RISK: cable MVNOs (Xfinity/Spectrum Mobile) took ~45% of 2025 industry adds on "
     "T-Mobile's own network — T-Mobile earns wholesale but loses higher-margin retail. "
     "Structural headwind; organic growth is decelerating. BASE signal."),
    ("spectrum_5g_moat",           3.0, 0.10,
     "2.5GHz: up to 110MHz depth vs 40-60MHz for Verizon (C-band) and AT&T — 2× capacity "
     "advantage. Ultra Capacity 5G covers 300M+ Americans. Sprint synergies >$8B run-rate "
     "(exceeded $7.5B target); NPV revised $43B → $70B+. Starlink satellite-to-cell "
     "partnership extends coverage. Structural: peers cannot replicate without ~$40B+ deal."),
    ("leverage_trajectory",        2.0, 0.05,
     "$83B net debt (2.45× EBITDA; improving). ≤4.5× covenant; ample headroom. "
     "Verizon 3.2×, AT&T 3.0× — T-Mobile least leveraged major US carrier. "
     "But $83B absolute is large; interest ~$3.5B/yr; rising rates = refinancing pressure. "
     "FCF ($18B) comfortably covers returns + debt amortization. BASE signal."),
]

PROXY_COMPOSITE = sum(v * w for _, v, w, _ in PROXY_SIGNALS)
# = 3.0×0.25 + 3.0×0.25 + 3.0×0.20 + 2.0×0.15 + 3.0×0.10 + 2.0×0.05
# = 0.75 + 0.75 + 0.60 + 0.30 + 0.30 + 0.10 = 2.80

import math

SCENARIO_CENTERS = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
TEMP = 0.60

def softmax_weights(composite):
    raw = {s: math.exp(-abs(composite - c) / TEMP)
           for s, c in SCENARIO_CENTERS.items()}
    total = sum(raw.values())
    return {s: v / total for s, v in raw.items()}

# ── SCA (STRUCTURAL COMPETITIVE ADVANTAGE) ───────────────────────────────────
SCA_FACTORS = [
    ("+", "2.5GHz spectrum depth (110MHz) — Sprint legacy; 2.75× more mid-band than Verizon "
          "(60MHz C-band) and AT&T (40MHz). Better building penetration, longer range, lower "
          "capex per covered person. A decade-long moat peers cannot replicate cheaply.",            +0.80, 0.25),
    ("+", "FWA first-mover scale (8.5M subs; 60% US market share): cable-grade broadband "
          "at zero incremental capex on built-out spectrum. Secular broadband substitution. "
          "Growing to 15M = ~$10B incremental annual revenue at ~50%+ EBITDA margin.",              +0.65, 0.20),
    ("+", "Post-Sprint cost structure: >$8B run-rate synergies; 25% FCF margin vs AT&T 14%, "
          "VZ 13%. Industry-leading efficiency ratios. Network fully integrated (Q2 2024). "
          "Scale advantages compound as subscriber base grows without proportional cost growth.", +0.55, 0.15),
    ("+", "Un-carrier brand + loyalty (0.86% churn, record): value positioning, price lock "
          "guarantees, J.D. Power #1 wireless network quality. Customer-first brand creates "
          "switching friction in an otherwise commoditized market.",                                 +0.35, 0.10),
    ("-", "Cable MVNO structural threat: Xfinity Mobile (Comcast) and Spectrum Mobile (Charter) "
          "jointly took ~45% of 2025 industry postpaid phone net adds — on T-Mobile's own "
          "network. T-Mobile earns MVNO wholesale but foregoes higher-margin branded retail.",       -0.60, 0.15),
    ("-", "$83B net debt — absolute level is largest telecom debt after Verizon; constrains "
          "M&A flexibility and increases rate sensitivity. ~$3.5B/yr interest expense headwind.",   -0.35, 0.10),
    ("-", "CEO transition risk: Srini Gopalan (former DT Germany CEO) is untested in US "
          "competitive wireless; transition coincides with potential DT merger complexity.",          -0.20, 0.05),
]
# SCA_NET = +0.80×0.25 + 0.65×0.20 + 0.55×0.15 + 0.35×0.10
#           + (-0.60)×0.15 + (-0.35)×0.10 + (-0.20)×0.05
# = 0.200 + 0.130 + 0.083 + 0.035 - 0.090 - 0.035 - 0.010 = +0.313

SCA_NET       = 0.313
SCA_SCALE     = 0.45
ADJ_COMPOSITE = round(PROXY_COMPOSITE + SCA_SCALE * SCA_NET * 0.5, 2)
# = 2.80 + 0.45 × 0.313 × 0.5 = 2.80 + 0.0704 = 2.87

# ── MARKET COMPOSITE (back-solved) ───────────────────────────────────────────
# EV(c_market) = CURRENT_PRICE × 1.15² (2yr, 15%/yr discount rate) + 2yr dividend
# Target EV = $187.53 × 1.3225 + $8.16 = $248.10 + $8.16 = $256.26
# Back-solve: c_market ≈ 1.90 → EV ≈ $247–$248
# Consistent with 29% drawdown from ATH while consensus PTs are $251-261.
# Market pricing between BEAR/BASE — implies cable MVNO fear + debt concern dominate.
MARKET_COMPOSITE  = 1.90
ADJ_VS_MARKET     = round(ADJ_COMPOSITE - MARKET_COMPOSITE, 2)   # +0.97 → SIGNIFICANTLY UNDERVALUED

# ── RATIO B ───────────────────────────────────────────────────────────────────
BEAR_TARGET  = SCENARIOS["BEAR"][2]     # $120
BULL_TARGET  = SCENARIOS["BULL"][2]     # $330
DOWNSIDE_PCT = (CURRENT_PRICE - BEAR_TARGET)  / CURRENT_PRICE * 100   # 36.0%
UPSIDE_PCT   = (BULL_TARGET   - CURRENT_PRICE) / CURRENT_PRICE * 100  # 76.0%
RATIO_B      = round(DOWNSIDE_PCT / UPSIDE_PCT, 2)   # 0.47

if RATIO_B < 0.75:
    SIGNAL_SHORT = "BUY"
    SIGNAL       = "◉ BUY"
elif RATIO_B < 1.10:
    SIGNAL_SHORT = "ACCUMULATE"
    SIGNAL       = "◎ ACCUMULATE"
elif RATIO_B < 1.75:
    SIGNAL_SHORT = "WATCHLIST"
    SIGNAL       = "◐ WATCHLIST"
else:
    SIGNAL_SHORT = "AVOID"
    SIGNAL       = "✕ AVOID"

# ── CONSERVATIVE 2-YEAR RETURN ────────────────────────────────────────────────
# Using FY2027E consensus EPS at a modest conservative P/E below the current 19×.
CONSERVATIVE_EPS     = 12.50    # FY2027E consensus-tracking; service rev + EBITDA guide
CONSERVATIVE_PE      = 17       # Conservative; slight multiple compression from 19× current
CONSERVATIVE_PRICE   = CONSERVATIVE_EPS * CONSERVATIVE_PE   # $212.50
CONSERVATIVE_DIV_2YR = ANNUAL_DIV * 2                        # $8.16
CONSERVATIVE_RETURN  = ((CONSERVATIVE_PRICE + CONSERVATIVE_DIV_2YR) / CURRENT_PRICE - 1) * 100
# = (212.50 + 8.16) / 187.53 - 1 = 220.66 / 187.53 - 1 = +17.7% (+8.9%/yr)

# EV/EBITDA cross-check:
# Bear:  $30B EBITDA × 6.5× = $195B EV - $83B debt = $112B / 1.086B = ~$103 ≈ $120 (close)
# Base:  $37.3B × 8.0× = $298.4B - $83B = $215.4B / 1.086B = ~$198 (current EV ≈ fair)
# Bull:  $42B × 10× = $420B - $83B = $337B / 1.086B = ~$310 ≈ $330 (close)
# XBull: $50B × 12× = $600B - $83B = $517B / 1.086B = ~$476 ≈ $450 (DT re-rate)

# ─────────────────────────────────────────────────────────────────────────────
# REPORT
# ─────────────────────────────────────────────────────────────────────────────

def run_model():
    weights = softmax_weights(ADJ_COMPOSITE)
    div_2yr = ANNUAL_DIV * 2
    ev = sum(weights[s] * (SCENARIOS[s][2] + div_2yr) for s in SCENARIOS)
    mkt_cap_b = CURRENT_PRICE * SHARES_OUT_M / 1000

    report = []
    A = report.append

    A("=" * 76)
    A(f"  {SIGNAL}  —  {COMPANY} ({TICKER})")
    A(f"  Bottom-Up Risk/Reward Signal Model · {DATE}")
    A("=" * 76)
    A(f"  Price: ${CURRENT_PRICE:.2f}  |  52W: ${VOL_52W_LOW}–${VOL_52W_HIGH}  (ATH ${VOL_52W_HIGH:.2f}; -29.6%)")
    A(f"  Shares: {SHARES_OUT_M:.0f}M  |  Mkt Cap: ${mkt_cap_b:.1f}B")
    A(f"  Div: ${ANNUAL_DIV:.2f}/yr ({ANNUAL_DIV/CURRENT_PRICE*100:.1f}% yield; ~10%/yr growth target)")
    A(f"  Net Debt: ${NET_DEBT_B:.1f}B  |  Net Debt / EBITDA: {LEVERAGE:.2f}×")
    A(f"  FCF Yield: {FCF_YIELD:.1f}%  (${ADJ_FCF_FY2025_B:.1f}B FCF / ${mkt_cap_b:.1f}B mkt cap)")
    A("")

    # ── SIGNAL DASHBOARD ────────────────────────────────────────────────────
    A("─" * 76)
    A("  SIGNAL DASHBOARD")
    A("─" * 76)
    A(f"  Signal      : {SIGNAL}")
    A(f"  Ratio B     : {RATIO_B:.2f}×  (downside {DOWNSIDE_PCT:.1f}% / upside {UPSIDE_PCT:.1f}%)")
    A(f"  EPP         : ${EPP:.2f}  (${EPS_TROUGH} trough EPS × {PE_TROUGH}× trough P/E)")
    A(f"  EPP Gap     : +{EPP_GAP_PCT:.1f}%  (stock is {EPP_GAP_PCT:.0f}% ABOVE EPP floor)")
    A(f"              : Real downside to ${EPP:.0f} exists in BEAR; upside more than compensates")
    A(f"  Proxy Comp  : {PROXY_COMPOSITE:.2f}  |  ADJ: {ADJ_COMPOSITE:.2f}  |  Market: {MARKET_COMPOSITE:.2f}")
    A(f"  ADJ–Market  : {ADJ_VS_MARKET:+.2f}  →  SIGNIFICANTLY UNDERVALUED")
    A(f"  2yr EV      : ${ev:.2f}  (vs ${CURRENT_PRICE:.2f} current; includes ${div_2yr:.2f} div)")
    A(f"  Conserv.    : +{CONSERVATIVE_RETURN:.1f}% / +{CONSERVATIVE_RETURN/2:.1f}%/yr")
    A(f"              : EPS ${CONSERVATIVE_EPS:.2f} × {CONSERVATIVE_PE}× + ${CONSERVATIVE_DIV_2YR:.2f} div = ${CONSERVATIVE_PRICE + CONSERVATIVE_DIV_2YR:.2f}")
    A("")
    A(f"  SCENARIO WEIGHTS  (at ADJ composite {ADJ_COMPOSITE:.2f}):")
    for s, w in weights.items():
        tgt = SCENARIOS[s][2]
        A(f"    {s:<6} {w*100:5.1f}%  →  ${tgt}  ({'+' if tgt > CURRENT_PRICE else ''}{(tgt-CURRENT_PRICE)/CURRENT_PRICE*100:.0f}%)")
    A("")

    # ── BUSINESS OVERVIEW ────────────────────────────────────────────────────
    A("─" * 76)
    A("  BUSINESS OVERVIEW — T-Mobile US, Inc.")
    A("─" * 76)
    A("  T-Mobile is the #2 US wireless carrier by subscribers (142.4M customers) and")
    A("  #1 in organic postpaid net adds for multiple consecutive years. The company is")
    A("  built on three compounding growth engines:")
    A("")
    A("  ① WIRELESS: 3.3M organic postpaid phone net adds/yr; 0.86% churn (record low);")
    A(f"    ARPA ${POSTPAID_ARPA_Q1_2026:.2f} (+3.9% YoY Q1 2026). UScellular (+3.3M phones,")
    A("    Aug 2025) expands rural/Midwest coverage. Cable MVNOs (Xfinity/Spectrum) use")
    A("    T-Mobile's own network — earning wholesale but losing retail — the key risk.")
    A("")
    A(f"  ② FIXED WIRELESS (FWA): {FWA_SUBS_YE2025_M}M subscribers (60% US market share);")
    A(f"    target {FWA_TARGET_2030_M}M by 2030. Built on spectrum already deployed — each")
    A("    incremental subscriber adds ~$660/yr in service revenue at near-zero capex.")
    A(f"    At 15M subs: ~$9.9B additional annual revenue → EBITDA expansion machine.")
    A("")
    A("  ③ SPECTRUM MOAT (2.5 GHz): Up to 110 MHz of contiguous mid-band vs 40-60 MHz")
    A("    for Verizon (C-band) and AT&T. Sprint legacy spectrum is irreplaceable.")
    A("    Enables both FWA economics AND faster mobile speeds simultaneously.")
    A("")
    A("  STRATEGIC OPTIONALITY — Deutsche Telekom (53% owner) in early-stage talks for")
    A("  full combination via new holding company. If completed, would create the world's")
    A("  largest telecom by market cap (~$300B+). Not priced into current valuation.")
    A("")

    # ── FWA: STRUCTURAL GROWTH ENGINE ─────────────────────────────────────────
    A("─" * 76)
    A("  FIXED WIRELESS ACCESS — THE INCREMENTAL MARGIN ENGINE")
    A("─" * 76)
    A(f"  FWA Subscribers (YE2025) : {FWA_SUBS_YE2025_M}M  (target: {FWA_TARGET_2030_M}M by 2030)")
    A(f"  FWA Net Adds (FY2025)    : +{FWA_ADDS_Q1_2026*1000:.0f}K Q1 2026 adds (accelerating YoY)")
    A(f"  US Market Share          : ~{FWA_MARKET_SHARE*100:.0f}%  (Verizon ~30%, others ~10%)")
    A(f"  Estimated ARPU           : ~${FWA_ARPU_MONTHLY:.0f}/mo (~$660/yr)")
    A(f"  Revenue at 15M target    : ~$9.9B/yr  (at $660/yr ARPU)")
    A("")
    A("  THE FWA ECONOMICS ARGUMENT:")
    A("  • Spectrum deployed: T-Mobile has already built the 5G network for wireless.")
    A("    Each FWA sub is served by the SAME towers at MARGINAL additional cost.")
    A("  • This is structurally different from fiber (AT&T: $150B capex) or cable")
    A("    (DOCSIS 4.0 upgrades): T-Mobile's capex is already sunk into the network.")
    A("  • Incremental EBITDA margin on FWA adds is ~50%+ (high-drop-through revenue)")
    A(f"  • Verizon FWA comparison: Verizon's C-band (60 MHz, 3.7 GHz) has shorter")
    A(f"    propagation than 2.5 GHz → more towers needed per FWA customer → higher cost")
    A("")
    A("  LONG-TERM TARGET MATH (15M FWA subs):")
    A(f"  15M × $660/yr ARPU = $9.9B annual service revenue")
    A(f"  At ~50% EBITDA margin = ~$5.0B incremental EBITDA")
    A(f"  At 8× EV/EBITDA = ~$40B EV uplift → ~$37/share additional value")
    A("  (vs. $0 incremental capex beyond already-committed network investment)")
    A("")

    # ── SPECTRUM MOAT ────────────────────────────────────────────────────────
    A("─" * 76)
    A("  2.5 GHz SPECTRUM MOAT — THE IRREPLACEABLE STRUCTURAL ADVANTAGE")
    A("─" * 76)
    A(f"  T-Mobile 2.5 GHz   : Up to {TMUS_MIDBAND_MHZ} MHz in major markets (Sprint legacy)")
    A(f"  Verizon C-band     : ~{VZN_MIDBAND_MHZ} MHz at 3.7 GHz (shorter range, higher capex/km²)")
    A(f"  AT&T mid-band      : ~{ATT_MIDBAND_MHZ} MHz (C-band + 3.45 GHz; most limited)")
    A(f"  Ultra Capacity 5G  : {UC5G_COVERAGE_M}M+ Americans covered (no peer equivalent)")
    A("")
    A("  WHY 2.5 GHz IS BETTER THAN C-BAND FOR FWA:")
    A("  • 2.5 GHz has ~30% better propagation than 3.7 GHz (C-band)")
    A("  • Each tower covers more area = fewer towers per FWA customer served")
    A("  • Better building penetration = fewer outdoor CPE devices needed")
    A("  • More MHz = more capacity = can serve more FWA subs per tower")
    A("  • Carrier aggregation with 600 MHz low-band = additional propagation boost")
    A("")
    A(f"  SPRINT MERGER SYNERGIES:")
    A(f"  • Target : ${SPRINT_SYNERGIES_TARGET_B}B/yr run-rate  |  Actual: ${SPRINT_SYNERGIES_ACTUAL_B}B/yr (exceeded)")
    A(f"  • NPV revised from ${SPRINT_SYNERGIES_NPV_ORIG_B}B → ${SPRINT_SYNERGIES_NPV_REV_B}B+ (+{(SPRINT_SYNERGIES_NPV_REV_B/SPRINT_SYNERGIES_NPV_ORIG_B-1)*100:.0f}% upgrade)")
    A(f"  • Integration: {SPRINT_INTEGRATION_STATUS}")
    A("")

    # ── FINANCIALS ────────────────────────────────────────────────────────────
    A("─" * 76)
    A("  FINANCIALS — FY2025 RESULTS & FY2026 GUIDANCE")
    A("─" * 76)
    A(f"  FY2025 Service Revenue : ${SERVICE_REV_FY2025_B:.1f}B  (+8% YoY)")
    A(f"  FY2025 Adj EBITDA      : ${CORE_ADJ_EBITDA_FY2025_B:.1f}B  (+7% YoY;  25% FCF margin)")
    A(f"  FY2025 Adj FCF         : ${ADJ_FCF_FY2025_B:.1f}B  (+6% YoY;  8.9% FCF yield)")
    A(f"  FY2025 GAAP EPS        : ${GAAP_EPS_FY2025:.2f}")
    A(f"  Q1 2026 Service Rev    : ${SERVICE_REV_Q1_2026_B:.1f}B  (+11% YoY — ACCELERATING)")
    A(f"  Q1 2026 Adj EBITDA     : ${CORE_ADJ_EBITDA_Q1_2026_B:.1f}B  (+12% YoY — positive op. leverage)")
    A("")
    A(f"  FY2026 GUIDANCE (Raised Post-Q1):")
    A(f"    Service Revenue : ~${SERVICE_REV_FY2026E_B:.1f}B  (+8%)")
    A(f"    Adj EBITDA      : $37.1–$37.5B  (midpoint ${CORE_ADJ_EBITDA_FY2026E_B:.1f}B)")
    A(f"    Adj FCF         : $18.1–$18.7B  (midpoint ${ADJ_FCF_FY2026E_B:.1f}B)")
    A("")
    A(f"  CONSENSUS EPS ESTIMATES:")
    A(f"    FY2026E: ~${ADJ_EPS_FY2026E:.2f}  |  FY2028E: ~${ADJ_EPS_FY2028E:.2f}")
    A(f"    FY2025 GAAP EPS ${GAAP_EPS_FY2025} → FY2026E ${ADJ_EPS_FY2026E} → FY2028E ${ADJ_EPS_FY2028E}")
    A(f"    Implies ~33% EPS growth FY2025→FY2028 (4yr CAGR ~12% adj EPS)")
    A("")
    A(f"  CAPITAL RETURNS:")
    A(f"    2026 Buyback Authorization : ${BUYBACK_AUTH_2026_B:.1f}B  (~9% of current market cap)")
    A(f"    Dividend                   : ${ANNUAL_DIV:.2f}/yr  growing ~10%/yr")
    A(f"    Shares Outstanding         : {SHARES_OUT_M:.0f}M  (declining ~3-4%/yr via buybacks)")
    A(f"    Since CMD 2024             : >${TOTAL_RETURNS_SINCE_2024_B:.0f}B total returned to shareholders")
    A("")
    A(f"  BALANCE SHEET:")
    A(f"    Net Debt         : ${NET_DEBT_B:.1f}B  ({LEVERAGE:.2f}× EBITDA; improving)")
    A(f"    Covenant Max     : 4.5× leverage  |  Current: {LEVERAGE:.2f}×  |  Headroom: {4.5-LEVERAGE:.2f}×")
    A(f"    vs. Peers        : VZ ~3.2×, AT&T ~3.0× — T-Mobile least leveraged major carrier")
    A("")

    # ── CAPITAL RETURN MATH ────────────────────────────────────────────────────
    A("─" * 76)
    A("  CAPITAL RETURN MATH — WHY $187 AT 8.9% FCF YIELD IS COMPELLING")
    A("─" * 76)
    A(f"  Annual FCF          : ${ADJ_FCF_FY2025_B:.1f}B  (growing)")
    A(f"  2026 Return Auth    : ${BUYBACK_AUTH_2026_B:.1f}B  (~9.2% of market cap retired in 1yr)")
    A(f"  Buyback at $187.53  : 97M shares/yr at $18.2B ÷ $187.53 = -8.9% share count")
    A(f"  EPS accretion (1yr) : +$0.87 from buybacks alone (at current EPS × 8.9% dilution)")
    A(f"  Dividend growth     : $4.08/yr × 10%/yr = $5.50/yr by FY2029E")
    A("")
    A("  The flywheel: high FCF → buybacks at cheap multiple → EPS grows faster than")
    A("  business → P/E falls further → more accretive buybacks → repeat.")
    A(f"  At 19× P/E (current): each $1B in buybacks = +$0.52 EPS next year.")
    A("")

    # ── COMPETITIVE DYNAMICS ─────────────────────────────────────────────────
    A("─" * 76)
    A("  COMPETITIVE DYNAMICS — THE CABLE MVNO STRUCTURAL SHIFT")
    A("─" * 76)
    A("  The most important competitive development in US wireless is the cable MVNO")
    A("  surge. Charter's Spectrum Mobile and Comcast's Xfinity Mobile collectively")
    A("  accounted for ~45% of 2025 industry postpaid phone net adds — more than any")
    A("  single facilities-based carrier. Both run on T-Mobile's network.")
    A("")
    A("  THE DOUBLE-EDGED SWORD:")
    A("  • T-Mobile EARNS wholesale MVNO revenue from every Xfinity/Spectrum sub")
    A("  • But cable MVNOs price mobile as a bundle attachment (~$15-25/mo) vs")
    A("    T-Mobile's branded retail (~$50-65/mo) — T-Mobile loses the margin premium")
    A("  • July 2025: T-Mobile expanded MVNO agreements for 5G Business services")
    A("    (Comcast + Charter launching 2026) — wholesale revenue growing")
    A("  • NET: T-Mobile is building an infrastructure business, not just retail")
    A("")
    A("  AT&T FIBER THREAT TO FWA:")
    A("  • AT&T passing 37M homes with fiber; ~273K subs/qtr; ARPU premium vs FWA")
    A("  • FWA churn increases where AT&T fiber is available — acknowledged by T-Mobile")
    A("  • However: AT&T fiber covers ~30% of TMUS's FWA addressable market maximum")
    A("  • Most FWA growth is in suburban/exurban markets where fiber economics are poor")
    A("")
    A("  VERIZON FWA:")
    A("  • Verizon is #2 FWA at ~3M subs; growing but losing share to T-Mobile")
    A("  • C-band economics worse than 2.5 GHz → Verizon's FWA more capex-intensive")
    A("  • T-Mobile delivers >50% faster FWA median download speeds (Ookla Q1 2026)")
    A("")

    # ── DT MERGER OPTIONALITY ──────────────────────────────────────────────────
    A("─" * 76)
    A("  DEUTSCHE TELEKOM MERGER — UNPRICED OPTIONALITY")
    A("─" * 76)
    A(f"  DT Ownership         : {DT_OWNERSHIP_PCT}%  (TMUS is >70% of DT's ~€135B market cap)")
    A(f"  CEO Transition       : {CEO_CHANGE}")
    A(f"  Merger Status        : {DT_MERGER_STATUS}")
    A("")
    A("  DEAL RATIONALE:")
    A("  • DT Frankfurt shares are essentially a T-Mobile wrapper at a holding co. discount")
    A("  • A full combination eliminates the 15-20% holding co. discount for DT shareholders")
    A("  • Combined entity: $300B+ market cap, 200M+ subs, world's largest telecom")
    A("  • All-share structure; no debt increase; new holding co. listed US + Europe")
    A("")
    A("  RISKS:")
    A("  • US political scrutiny (foreign control of critical telecom infrastructure)")
    A("  • German government (~28% stake in DT via KfW) must approve dilution")
    A("  • Early stage — could collapse; not a base case")
    A("  • OPTION VALUE: if deal announced, TMUS stock likely re-rates +20-30% on premium")
    A("")

    # ── SCA BREAKDOWN ────────────────────────────────────────────────────────
    A("─" * 76)
    A("  STRUCTURAL COMPETITIVE ADVANTAGE (SCA) FACTORS")
    A("─" * 76)
    for sign, desc, score, wt in SCA_FACTORS:
        contrib = score * wt
        A(f"  {sign}  wt={wt:.2f}  score={score:+.2f}  contrib={contrib:+.3f}")
        A(f"     {desc[:75]}")
        A("")
    A(f"  SCA_NET = {SCA_NET:.3f}  |  Contribution to composite: +{SCA_SCALE * SCA_NET * 0.5:.3f}")
    A("")

    # ── PROXY SIGNALS ────────────────────────────────────────────────────────
    A("─" * 76)
    A("  PROXY SIGNALS")
    A("─" * 76)
    for name, val, wt, desc in PROXY_SIGNALS:
        scenario_label = {1.0: "BEAR", 2.0: "BASE", 3.0: "BULL", 4.0: "XBULL"}.get(val, f"{val:.1f}")
        A(f"  [{scenario_label}]  {name}  (value={val:.1f}, weight={wt:.2f})")
        A(f"  {desc[:75]}")
        A(f"  {desc[75:150]}" if len(desc) > 75 else "")
        A("")
    A(f"  PROXY COMPOSITE  = {PROXY_COMPOSITE:.2f}")
    A(f"  ADJ COMPOSITE    = {ADJ_COMPOSITE:.2f}  (adds SCA benefit)")
    A(f"  MARKET COMPOSITE = {MARKET_COMPOSITE:.2f}  (implied by current $${CURRENT_PRICE:.2f})")
    A(f"  GAP              = {ADJ_VS_MARKET:+.2f}  (model vs market)")
    A("")

    # ── SCENARIOS ────────────────────────────────────────────────────────────
    A("─" * 76)
    A("  SCENARIOS")
    A("─" * 76)
    for s, (eps, pe, price, desc) in SCENARIOS.items():
        chg = (price - CURRENT_PRICE) / CURRENT_PRICE * 100
        A(f"  {s:<6}  ${price:.0f}  ({chg:+.0f}%)  EPS ${eps:.2f} × {pe}× P/E")
        A(f"         {desc[:80]}")
        A("")
    A(f"  RATIO B  = {RATIO_B:.2f}×  ({DOWNSIDE_PCT:.1f}% downside / {UPSIDE_PCT:.1f}% upside to BULL)")
    A(f"  EPP FLOOR: ${EPP:.2f}  (trough ${EPS_TROUGH} EPS × {PE_TROUGH}× P/E)  |  EPP Gap: +{EPP_GAP_PCT:.1f}%")
    A("")

    # ── SUM-OF-PARTS CROSS-CHECK ──────────────────────────────────────────────
    A("─" * 76)
    A("  EV/EBITDA SUM-OF-PARTS CROSS-CHECK (2026E)")
    A("─" * 76)
    A(f"  2026E Adj EBITDA        : ${CORE_ADJ_EBITDA_FY2026E_B:.1f}B")
    A("")
    A("  SCENARIO           EV/EBITDA  EV ($B)  Equity ($B)  Per Share")
    A("  ─────────────────────────────────────────────────────────────")
    for lbl, mult, bear_label in [
        ("Bear  (stress)",     6.5, "BEAR"),
        ("Base  (8× current)", 8.0, "BASE"),
        ("Bull  (FWA re-rate)",10.0, "BULL"),
        ("XBull (DT merger)", 12.0, "XBULL"),
    ]:
        ev_b   = CORE_ADJ_EBITDA_FY2026E_B * mult
        eq_b   = ev_b - NET_DEBT_B
        per_sh = eq_b * 1000 / SHARES_OUT_M
        A(f"  {lbl:<20}  {mult:.1f}×    ${ev_b:.0f}B   ${max(eq_b,0):.0f}B      ${per_sh:.0f}")
    A("")
    A("  The Base case EV/EBITDA (8×) implies equity value ~$198/share — essentially")
    A("  CURRENT PRICE. At 10× (FWA fully valued), intrinsic rises to ~$310.")
    A("  The market is at 8× EV/EBITDA on FY2026E while FWA adds $5B+ EBITDA by 2030.")
    A("")

    # ── KEY INSIGHT ────────────────────────────────────────────────────────────
    A("─" * 76)
    A("  INVESTMENT THESIS — WHY THE MARKET IS WRONG AT $187.53")
    A("─" * 76)
    A("")
    A("  The market is pricing T-Mobile as a saturating wireless carrier facing cable")
    A("  MVNO structural erosion and carrying $83B in debt. That narrative is partially")
    A("  right — but it misses five compounding factors:")
    A("")
    A("  ① FWA IS STRUCTURALLY UNDERVALUED: 8.5M at $660/yr = $5.6B FWA revenue at")
    A("    ~50% margin. Growing to 15M = $9.9B revenue. At 8× EV/EBITDA, FWA alone")
    A("    is worth $37/share additional VALUE vs zero incremental capex. The market")
    A("    values FWA at cellular tower multiples (6-7×), not cable broadband (8-10×).")
    A("")
    A("  ② CABLE MVNO IS GOOD FOR T-MOBILE TOO: Yes, Xfinity/Spectrum Mobile are")
    A("    taking retail share — but every Xfinity Mobile sub pays T-Mobile MVNO")
    A("    fees. T-Mobile is becoming an INFRASTRUCTURE business: retail OR wholesale.")
    A("    July 2025 5G Business expansion shows T-Mobile embracing this model.")
    A("")
    A("  ③ $18.2B IN BUYBACKS IN 2026 ALONE: At $187.53, T-Mobile is buying back")
    A(f"    ~97M shares/yr. That's 8.9% of the float at 19× P/E — exceptional IRR.")
    A("    Each year of buybacks adds $0.87+ to EPS from share count reduction alone.")
    A("")
    A("  ④ SPECTRUM MOAT IS REAL AND DURABLE: Verizon spent $45B on C-band spectrum")
    A("    (30MHz-60MHz); T-Mobile has 110MHz at 2.5GHz from Sprint. To match T-Mobile,")
    A("    Verizon/AT&T would need to acquire similar spectrum depth — unavailable.")
    A("")
    A("  ⑤ DT MERGER OPTIONALITY: Not priced in. If DT announces a full combination,")
    A("    TMUS stock re-rates +20-30% on merger premium alone. Zero cost option at")
    A("    current price since it's not in the base case assumptions.")
    A("")
    A("  BUY with 2.2% dividend floor and growing buyback yield. Catalyst: FWA hits")
    A("  10M+ subs; Q2/Q3 2026 guidance raise; DT merger announcement.")
    A("")
    A("  RISKS TO MONITOR:")
    A("  • Cable MVNO share of phone adds exceeds 50% consistently → structural drag")
    A("  • FWA net adds slow materially below 1.5M/yr → growth thesis degraded")
    A("  • Rate cuts delayed or reversed → refinancing on $83B debt becomes costly")
    A("  • DT merger fails to materialize; CEO transition causes strategy drift")
    A("  • AT&T fiber reaches 50M+ homes → meaningful FWA addressable market shrinks")
    A("════════════════════════════════════════════════════════════════════════════")
    A("")

    summary_line = (
        f"TMUS {SIGNAL} — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT:.1f}% downside / {UPSIDE_PCT:.1f}% upside). "
        f"FCF machine at 8.9% yield ($18B annual FCF) trading 29.6% below ATH ($266.80). "
        f"Service revenue accelerating: +8% FY2025, +11% Q1 2026 YoY. FWA at 8.5M subs (60% US market share); "
        f"target 15M by 2030 — pure incremental margin (zero added capex). 2.5GHz: 110MHz depth vs "
        f"40-60MHz for Verizon/AT&T — irreplaceable spectrum moat from Sprint merger. Sprint synergies "
        f"exceeded: $8B actual vs $7.5B target; NPV upgraded $43B → $70B+. $18.2B buyback authorization "
        f"in 2026 alone (~9% of float). Dividend $4.08/yr (2.2%; growing 10%/yr). Net debt $83B (2.45× EBITDA; "
        f"lowest leverage among major US carriers). Cable MVNO risk: Xfinity/Spectrum took ~45% of 2025 industry "
        f"phone adds on T-Mobile's own network. DT (53% owner) in early-stage merger talks — optionality not "
        f"priced in. EV/EBITDA cross-check: Base 8× = $198/share (current); Bull 10× = $310. "
        f"Analyst consensus $251-261 (+34-39%). Bear $120 · Base $250 · Bull $330 · XBull $450."
    )
    A(f"SUMMARY: {summary_line}")
    A("")
    A(f"SIGNAL: {SIGNAL} | Ratio B: {RATIO_B:.2f}× | EPP Gap: +{EPP_GAP_PCT:.1f}%")

    return "\n".join(report)


if __name__ == "__main__":
    print(run_model())
