"""
Halliburton Company (NYSE: HAL)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◉ BUY  |  Ratio B: 0.73×  |  EPP Gap: +180.0%

A TECHNOLOGY-LEADING OILFIELD SERVICES GIANT TRADING AT A GENUINE CYCLICAL-TROUGH PRICE
Trading at $25.20 (52-week range $18.40-32.10, roughly a quarter up its range — a name that
has been cyclically de-rated alongside the broader oilfield-services complex into what looks
like a genuine trough entry point) on the back of
a genuinely durable technology and execution moat: Halliburton remains one of only two truly
global, full-spectrum oilfield-services majors, with a #1-or-#2 competitive position across
the large majority of its product lines, a Completion & Production (C&P) segment that
continues to lead on completions technology and efficiency (frac fleet electrification,
digital/automation platforms), and a Drilling & Evaluation (D&E) segment with genuine
technology differentiation (LOGIX automation, iCruise rotary steerable systems, Sperry
Drilling). The balance sheet is investment-grade and shareholder returns (dividend +
buybacks) remain a stated capital-allocation priority even through the current downcycle.

The honest tension: Halliburton is structurally the most North-America-levered of the
oilfield-services majors — and North American land activity (rig counts, completions
intensity) has been in a genuine cyclical downturn through 2025-26 as E&P operators
prioritize capital discipline and shareholder returns over production growth. That activity
softness has compressed both revenue and margins in HAL's largest, highest-margin segment at
exactly the moment international and offshore activity — historically HAL's diversification
ballast — has been only modestly offsetting. At ~11-12x depressed forward earnings, the
stock is pricing in continued North American softness without much credit for either a
cyclical recovery or HAL's genuine technology leadership.

Conviction: MODERATE-HIGH on the structural technology-and-scale thesis (Halliburton's
completions-technology leadership and full-spectrum global platform are genuinely durable
competitive advantages that have repeatedly proven their worth coming out of prior cycles);
MODERATE on near-term timing given North American activity remains the dominant swing factor
and shows no clear inflection yet — but Ratio B lands solidly in BUY territory, reflecting a
name whose downside is already meaningfully compressed (an investment-grade balance sheet,
a price near a cyclical trough, and technology moats that survive any cycle) against an
upside that would be sharply asymmetric the moment North American activity even stabilizes,
let alone inflects.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "HAL"
COMPANY         = "Halliburton Company"
SECTOR          = "Oilfield Services & Equipment · Completion & Production / Drilling & Evaluation · Global Full-Spectrum Services Major · NYSE: HAL"
SECTOR_GROUP    = "Energy"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 25.20    # June 2026, roughly a quarter up the 52-week range — cyclically de-rated
ANNUAL_DIV      = 0.68     # $0.17/qtr quarterly dividend; yield ~2.7%
SHARES_OUT_B    = 0.845    # ~845mm shares outstanding
MARKET_CAP_B    = 21.3     # CURRENT_PRICE × SHARES_OUT_B
FW52_HIGH       = 32.10
FW52_LOW        = 18.40

# ── FY2025 FULL-YEAR FINANCIALS ─────────────────────────────────────────────
REVENUE_FY2025_B           = 21.6
ADJ_NET_INCOME_FY2025_B    = 1.95
ADJ_EPS_FY2025             = 2.31
OCF_FY2025_B               = 3.55
FCF_FY2025_B               = 1.95
ADJ_OPERATING_MARGIN_PCT   = 14.5
ADJ_EPS_YOY_PCT            = -16    # NAM activity softness compressed both revenue and margins YoY

# ── SEGMENT MIX / NORTH AMERICA EXPOSURE ─────────────────────────────────────
NAM_REVENUE_SHARE_PCT       = 39.0   # Most North-America-levered of the OFS majors
INTERNATIONAL_REVENUE_SHARE_PCT = 61.0
NAM_ACTIVITY_NOTE           = "North American land activity (rig counts, completions intensity) has been in a genuine cyclical downturn through 2025-26 as E&P operators prioritize capital discipline and shareholder returns over production growth — compressing both revenue and margins in HAL's largest, highest-margin segment"
INTERNATIONAL_OFFSET_NOTE   = "International and offshore activity has been only modestly offsetting NAM softness so far — though it represents the larger and structurally more stable share of the portfolio, with multi-year project visibility in the Middle East, Latin America, and deepwater basins"

# ── COMPLETION & PRODUCTION (C&P) — TECHNOLOGY LEADERSHIP ───────────────────
CP_REVENUE_SHARE_PCT        = 56.0
FRAC_FLEET_ELECTRIFICATION_NOTE = "Halliburton continues to lead the shift toward electric and dual-fuel frac fleets — a genuine efficiency and emissions-profile advantage that increasingly differentiates win-rates in a capital-disciplined NAM completions market"
CP_TECH_NOTE                = "Digital and automation platforms (Halliburton iEnergy, ZEUS electric fleet platform) extend a multi-year completions-technology lead that has repeatedly proven durable across prior cyclical troughs"

# ── DRILLING & EVALUATION (D&E) — TECHNOLOGY LEADERSHIP ──────────────────────
DE_REVENUE_SHARE_PCT        = 44.0
LOGIX_NOTE                  = "LOGIX autonomous drilling platform and iCruise/iCruise-X rotary-steerable systems extend genuine, multi-generation technology differentiation in directional drilling and formation evaluation — a moat that compounds as wells get longer and more complex"
SPERRY_DRILLING_NOTE        = "Sperry Drilling and Halliburton's formation-evaluation/wireline franchise maintain #1-or-#2 competitive positioning across the large majority of D&E product lines globally"

# ── CAPITAL RETURN & BALANCE SHEET ────────────────────────────────────────────
NET_DEBT_B                  = 6.6
NET_DEBT_TO_EBITDA          = 1.4
CREDIT_RATING_NOTE          = "Investment-grade balance sheet (A-/A3 range) — among the strongest in the oilfield-services peer group, providing genuine resilience through a multi-year activity downcycle"
BUYBACK_PROGRAM_NOTE        = "Management has continued to prioritize returning the large majority of FCF to shareholders via dividends plus opportunistic buybacks even through the current downcycle — a signal of confidence in the through-cycle earnings power of the platform"

# ── ANALYST CONSENSUS ────────────────────────────────────────────────────────
EPS_FY2026E             = 2.45     # Consensus reflects a modest NAM-activity stabilization, not a sharp recovery
TRAILING_PE             = 10.9
FORWARD_PE              = 10.3
CONSENSUS_PT            = 29.0     # Average target ~$29 (range $22-38)
PT_LOW                  = 22.0
PT_HIGH                 = 38.0
CONSENSUS_RATING        = "Hold / Buy (mixed)"
ANALYST_RATING_NOTE     = "~13 Buy / 14 Hold / 2 Sell of ~29 analysts; consensus PT ~$29 (range $22-38) — genuinely split on the timing of a North American activity inflection"

# ── SCENARIOS ────────────────────────────────────────────────────────────────
# BEAR  $18: A prolonged North American land-activity trough — rig counts and completions
#            intensity stay depressed for multiple additional quarters as capital-disciplined
#            E&P operators continue prioritizing buybacks over drilling programs, AND
#            international/offshore activity fails to pick up the slack, compressing margins
#            further and triggering a renewed multiple-compression episode characteristic of
#            OFS names in a deep-trough scenario. Roughly the lower quarter of the 52-week
#            range — the investment-grade balance sheet provides real ballast (this is not a
#            solvency story), but a genuine multi-quarter earnings air-pocket nonetheless.
#
# BASE  $25: Roughly where the stock sits today — North American activity stabilizes at
#            roughly current (depressed) levels without a clear inflection, international and
#            offshore activity continues its modest, multi-year-project-driven growth, C&P
#            and D&E technology platforms continue gaining share within a flat-to-modestly-
#            growing addressable market, and the market continues to apply a deep cyclical-
#            trough discount to the stock. "Consensus PT ~$29" only partially realized.
#
# BULL  $35: North American activity inflects — rig counts and completions intensity begin a
#            genuine recovery as commodity prices firm and E&P capital budgets normalize
#            upward, international/offshore project activity accelerates on multi-year
#            backlogs, AND the market begins to re-rate HAL's technology leadership
#            (electrification, automation, LOGIX) as a genuine share-gain driver rather than
#            simply a cyclical-survival tool — a re-rating OFS majors have repeatedly
#            captured coming out of prior troughs.
#
# XBULL $44: Full structural-recovery thesis — North American activity recovers sharply,
#            international mega-projects (Middle East, deepwater Latin America/West Africa)
#            move into peak-activity phases simultaneously, HAL's technology platforms drive
#            genuine market-share gains AND margin expansion, AND the market grants the
#            "best-positioned major coming out of the trough" a structural premium multiple —
#            the scenario in which "technology-leading global OFS major at trough multiples"
#            finally gets the re-rating its prior-cycle history argues for. Requires several
#            cyclical and structural tailwinds to align simultaneously — high-conviction,
#            lower-probability outcome.
BEAR    = 18.0
BASE    = 25.0
BULL    = 35.0
XBULL   = 44.0

# ── EPP (EARNINGS POWER PRICE) ───────────────────────────────────────────────
# Trough scenario: oilfield-services names are among the most cyclically violent in all of
# energy — Halliburton itself has seen adjusted EPS compress to near-breakeven levels during
# severe prior downcycles (2015-16, 2020 COVID collapse) despite its scale and technology
# advantages. EPS_TROUGH reflects a severe, multi-quarter NAM-activity-trough scenario, well
# below the FY2025 print of $2.31, and PE_TROUGH reflects the deep-discount multiple
# cyclical OFS names receive in a genuine trough — even a technology-leading global major.
EPS_TROUGH  = 0.75
PE_TROUGH   = 12.0
EPP         = EPS_TROUGH * PE_TROUGH   # = $9.00

# ── SCA: STRUCTURAL COMPETITIVE ADVANTAGE ───────────────────────────────────
# HAL's moat blends genuine, multi-generation technology leadership in both of its core
# segments (completions efficiency/electrification in C&P, autonomous drilling/formation
# evaluation in D&E), a truly global full-spectrum platform that few peers can match in
# scale and breadth, and an investment-grade balance sheet that provides real resilience
# through cyclical troughs. The offsets: structural North-America concentration leaves it
# more cyclically exposed than more internationally-weighted peers, and OFS economics remain
# fundamentally a function of E&P capital-spending cycles the company does not control.

SCA_FACTORS = {
    # Factor                                            : (score,  weight)
    "completions_technology_and_electrification_lead"  : (+0.35,  0.17),  # C&P technology leadership (electrification, automation, ZEUS) — durable, multi-cycle-proven moat
    "drilling_evaluation_technology_differentiation"   : (+0.30,  0.16),  # LOGIX/iCruise/Sperry — genuine, compounding multi-generation technology lead
    "global_full_spectrum_scale_and_breadth"           : (+0.25,  0.15),  # One of only two truly global, full-spectrum OFS majors — #1-or-#2 across most product lines
    "investment_grade_balance_sheet_resilience"        : (+0.25,  0.14),  # A-/A3-range credit — among the strongest in the OFS peer group, genuine through-cycle ballast
    "shareholder_aligned_capital_return_through_cycle" : (+0.15,  0.12),  # Continued dividend + opportunistic buybacks even through the downcycle — confidence signal
    "north_american_activity_concentration_risk"       : (-0.35,  0.14),  # Most NAM-levered of the OFS majors — directly exposed to the current land-activity downcycle
    "e_and_p_capex_cycle_dependency"                   : (-0.20,  0.12),  # OFS economics are fundamentally a function of E&P capital-spending cycles the company does not control
}

SCA_NET  = sum(score * weight for score, weight in SCA_FACTORS.values())
# SCA_NET = 0.35×0.17 + 0.30×0.16 + 0.25×0.15 + 0.25×0.14 + 0.15×0.12 + (-0.35)×0.14 + (-0.20)×0.12
# SCA_NET ≈ 0.0595 + 0.048 + 0.0375 + 0.035 + 0.018 - 0.049 - 0.024 = 0.125

SCA_SCALE = 0.45  # Fixed framework parameter

# ── 6 PROXY SIGNALS ──────────────────────────────────────────────────────────
# Signal   (score 1–4, weight)
# 1=BEAR, 1.5=BEAR+, 2=BASE, 2.5=BASE+, 3=BULL, 3.5=BULL+, 4=XBULL

SIGNALS = {
    # Halliburton continues to lead the shift toward electric and dual-fuel frac fleets and
    # digital/automation completions platforms (ZEUS, iEnergy) — a genuine, multi-cycle-
    # proven efficiency and win-rate advantage that has repeatedly differentiated the company
    # even in capital-disciplined, activity-constrained NAM markets.
    "completions_technology_and_electrification_lead": (3.0, 0.18),

    # LOGIX autonomous drilling, iCruise/iCruise-X rotary-steerable systems, and the Sperry
    # Drilling/formation-evaluation franchise extend genuine, compounding, multi-generation
    # technology differentiation — a moat that strengthens as wells get longer, more complex,
    # and more automation-dependent across both NAM and international markets.
    "drilling_evaluation_technology_differentiation": (3.0, 0.16),

    # The current North American land-activity downturn is real, structural to the cycle (not
    # company-specific), and directly compresses HAL's largest and highest-margin segment —
    # the dominant, unresolved swing factor for both earnings and the stock, with no clear
    # inflection signal yet visible in rig-count or completions-intensity data.
    "north_american_activity_downcycle_headwind": (1.5, 0.20),

    # International and offshore activity — historically HAL's diversification ballast —
    # represents the larger, structurally more stable ~61% of the portfolio, with genuine
    # multi-year project visibility in the Middle East, Latin America, and deepwater basins,
    # though it has so far only modestly offset NAM softness rather than fully compensating.
    "international_offshore_diversification_ballast": (2.5, 0.15),

    # The investment-grade balance sheet (A-/A3-range, net debt/EBITDA ~1.4x) and continued
    # commitment to dividends plus opportunistic buybacks even through the downcycle reflect
    # genuine financial strength and management confidence in the platform's through-cycle
    # earnings power — a meaningful margin of safety relative to past OFS-sector troughs.
    "balance_sheet_strength_and_capital_return_signal": (2.5, 0.16),

    # At ~10-11x depressed forward earnings — near the low end of HAL's historical multiple
    # range — the stock prices in continued North American softness with little credit for
    # either a cyclical activity inflection or the company's genuine technology leadership,
    # leaving room for a sharp re-rating whenever that inflection becomes visible.
    "valuation_at_cyclical_trough_multiple": (2.5, 0.15),
}

# ── COMPOSITE CALCULATION ─────────────────────────────────────────────────────
def softmax_weights(composite, scenarios, T=0.60):
    centers = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
    raw = {s: math.exp(-abs(composite - centers[s]) / T) for s in scenarios}
    total = sum(raw.values())
    return {s: raw[s] / total for s in scenarios}

PROXY_COMPOSITE = sum(score * weight for score, weight in SIGNALS.values())
ADJ_COMPOSITE   = PROXY_COMPOSITE + SCA_SCALE * SCA_NET * 0.5

scenarios = {"BEAR": BEAR, "BASE": BASE, "BULL": BULL, "XBULL": XBULL}
weights   = softmax_weights(ADJ_COMPOSITE, scenarios)

EV = sum(weights[s] * (scenarios[s] + ANNUAL_DIV) for s in scenarios)

DOWNSIDE_PCT = (CURRENT_PRICE - BEAR) / CURRENT_PRICE * 100
UPSIDE_PCT   = (BULL - CURRENT_PRICE) / CURRENT_PRICE * 100
RATIO_B      = DOWNSIDE_PCT / UPSIDE_PCT

if RATIO_B < 0.75:
    SIGNAL_TEXT  = "◉ BUY"
    SIGNAL_SHORT = "BUY"
    SIGNAL_COLOR = "#4ade80"
elif RATIO_B < 1.10:
    SIGNAL_TEXT  = "◎ ACCUMULATE"
    SIGNAL_SHORT = "ACCUMULATE"
    SIGNAL_COLOR = "#f0b429"
elif RATIO_B < 1.75:
    SIGNAL_TEXT  = "◌ WATCHLIST"
    SIGNAL_SHORT = "WATCHLIST"
    SIGNAL_COLOR = "#60a5fa"
else:
    SIGNAL_TEXT  = "✕ AVOID"
    SIGNAL_SHORT = "AVOID"
    SIGNAL_COLOR = "#f87171"

EPP_GAP_PCT   = (CURRENT_PRICE - EPP) / EPP * 100

# Market composite: back-solve c such that softmax EV = CURRENT_PRICE × 1.15²
TARGET_MARKET = CURRENT_PRICE * (1.15 ** 2)
def ev_at_c(c):
    w = softmax_weights(c, scenarios)
    return sum(w[s] * (scenarios[s] + ANNUAL_DIV) for s in scenarios)

lo, hi = 1.0, 4.0
for _ in range(60):
    mid = (lo + hi) / 2
    if ev_at_c(mid) > TARGET_MARKET:
        hi = mid
    else:
        lo = mid
MARKET_COMPOSITE = (lo + hi) / 2
ADJ_VS_MARKET = ADJ_COMPOSITE - MARKET_COMPOSITE

# Conservative 2yr: FY2026E EPS (consensus, reflecting modest NAM-activity stabilization, not
# a sharp recovery) × a multiple roughly in line with the current ~10.3x forward — pure
# compounding/stabilization test, no cyclical-recovery re-rating credit required
PE_CONSERVATIVE = 10.0
PRICE_2YR_CONSV = EPS_FY2026E * PE_CONSERVATIVE + 2 * ANNUAL_DIV
RETURN_2YR      = (PRICE_2YR_CONSV - CURRENT_PRICE) / CURRENT_PRICE * 100
RETURN_ANN      = (((PRICE_2YR_CONSV / CURRENT_PRICE) ** 0.5) - 1) * 100

if __name__ == "__main__":
    SEP = "═" * 76
    sep = "─" * 76

    print(SEP)
    print(f"  {TICKER} — {COMPANY}")
    print(f"  {SECTOR}")
    print(f"  Analysis: {ANALYSIS_DATE}  |  Price: ${CURRENT_PRICE:.2f}  |  52W: ${FW52_LOW:.2f}–${FW52_HIGH:.2f}")
    print(SEP)

    print(f"\n  SIGNAL:  {SIGNAL_TEXT}   Ratio B: {RATIO_B:.2f}×   EPP Gap: {EPP_GAP_PCT:+.1f}%")
    print(f"  EV(model): ${EV:.2f}   Upside: +{UPSIDE_PCT:.1f}%   Downside: -{DOWNSIDE_PCT:.1f}%\n")

    print(sep)
    print("  FY2025 FINANCIALS")
    print(sep)
    print(f"  Revenue:           ${REVENUE_FY2025_B:.1f}B  |  Adj. net income: ${ADJ_NET_INCOME_FY2025_B:.2f}B  |  Adj. EPS: ${ADJ_EPS_FY2025:.2f}  ({ADJ_EPS_YOY_PCT:+d}% YoY)")
    print(f"  OCF / FCF:         ${OCF_FY2025_B:.2f}B / ${FCF_FY2025_B:.2f}B  |  Adj. operating margin: ~{ADJ_OPERATING_MARGIN_PCT:.1f}%")

    print(f"\n{sep}")
    print("  SEGMENT MIX & NORTH AMERICA EXPOSURE")
    print(sep)
    print(f"  NAM revenue share: ~{NAM_REVENUE_SHARE_PCT:.0f}%  |  International revenue share: ~{INTERNATIONAL_REVENUE_SHARE_PCT:.0f}%")
    print(f"  {NAM_ACTIVITY_NOTE}")
    print(f"  {INTERNATIONAL_OFFSET_NOTE}")

    print(f"\n{sep}")
    print("  COMPLETION & PRODUCTION (C&P) — TECHNOLOGY LEADERSHIP")
    print(sep)
    print(f"  Segment revenue share: ~{CP_REVENUE_SHARE_PCT:.0f}%")
    print(f"  {FRAC_FLEET_ELECTRIFICATION_NOTE}")
    print(f"  {CP_TECH_NOTE}")

    print(f"\n{sep}")
    print("  DRILLING & EVALUATION (D&E) — TECHNOLOGY LEADERSHIP")
    print(sep)
    print(f"  Segment revenue share: ~{DE_REVENUE_SHARE_PCT:.0f}%")
    print(f"  {LOGIX_NOTE}")
    print(f"  {SPERRY_DRILLING_NOTE}")

    print(f"\n{sep}")
    print("  CAPITAL RETURN & BALANCE SHEET")
    print(sep)
    print(f"  Net debt: ${NET_DEBT_B:.1f}B  |  Net debt/EBITDA: ~{NET_DEBT_TO_EBITDA:.1f}x")
    print(f"  {CREDIT_RATING_NOTE}")
    print(f"  {BUYBACK_PROGRAM_NOTE}")

    print(f"\n{sep}")
    print("  ANALYST CONSENSUS")
    print(sep)
    print(f"  FY2026E EPS: ${EPS_FY2026E:.2f}  |  Trailing P/E ~{TRAILING_PE:.1f}x, Forward P/E ~{FORWARD_PE:.1f}x")
    print(f"  Rating: {CONSENSUS_RATING}  |  Price targets: consensus ${CONSENSUS_PT:.0f} (range ${PT_LOW:.0f}-${PT_HIGH:.0f})")
    print(f"  {ANALYST_RATING_NOTE}")

    print(f"\n{sep}")
    print("  6 PROXY SIGNALS")
    print(sep)
    labels = {
        "completions_technology_and_electrification_lead": "Completions technology & electrification lead",
        "drilling_evaluation_technology_differentiation":  "Drilling & evaluation technology differentiation",
        "north_american_activity_downcycle_headwind":      "North American activity downcycle headwind",
        "international_offshore_diversification_ballast":  "International / offshore diversification ballast",
        "balance_sheet_strength_and_capital_return_signal":"Balance-sheet strength & capital-return signal",
        "valuation_at_cyclical_trough_multiple":           "Valuation at cyclical trough multiple",
    }
    for k, (score, weight) in SIGNALS.items():
        bar = "█" * int(score * 5)
        print(f"  {labels[k]:<54}  {score:.1f}  wt={weight:.2f}  {bar}")
    print(f"  {'PROXY COMPOSITE':<54}  {PROXY_COMPOSITE:.2f}")

    print(f"\n{sep}")
    print("  SCA — STRUCTURAL COMPETITIVE ADVANTAGE")
    print(sep)
    sca_labels = {
        "completions_technology_and_electrification_lead": "Completions technology & electrification lead",
        "drilling_evaluation_technology_differentiation":  "Drilling & evaluation technology differentiation",
        "global_full_spectrum_scale_and_breadth":          "Global full-spectrum scale & breadth",
        "investment_grade_balance_sheet_resilience":       "Investment-grade balance-sheet resilience",
        "shareholder_aligned_capital_return_through_cycle":"Shareholder-aligned capital return through cycle",
        "north_american_activity_concentration_risk":      "North American activity concentration risk",
        "e_and_p_capex_cycle_dependency":                  "E&P capex-cycle dependency",
    }
    for k, (score, weight) in SCA_FACTORS.items():
        print(f"  {sca_labels[k]:<54}  {score:+.2f} × {weight:.2f} = {score*weight:+.4f}")
    print(f"  {'SCA_NET':<54}  {SCA_NET:+.4f}")
    print(f"  ADJ contribution (+0.45 × SCA_NET × 0.5): {SCA_SCALE * SCA_NET * 0.5:+.4f}")

    print(f"\n{sep}")
    print("  COMPOSITE SCORES")
    print(sep)
    print(f"  PROXY_COMPOSITE:    {PROXY_COMPOSITE:.4f}")
    print(f"  ADJ_COMPOSITE:      {ADJ_COMPOSITE:.4f}")
    print(f"  MARKET_COMPOSITE:   {MARKET_COMPOSITE:.4f}  (back-solved from ${CURRENT_PRICE}×1.15²=${TARGET_MARKET:.2f})")
    print(f"  ADJ_VS_MARKET:      {ADJ_VS_MARKET:+.4f}  → {'SIGNIFICANTLY UNDERVALUED' if ADJ_VS_MARKET > 0.5 else 'MODESTLY UNDERVALUED' if ADJ_VS_MARKET > 0.1 else 'FAIRLY VALUED' if ADJ_VS_MARKET > -0.1 else 'MODESTLY OVERVALUED'}")

    print(f"\n{sep}")
    print("  SCENARIO WEIGHTS (softmax at ADJ_COMPOSITE)")
    print(sep)
    for s, price in scenarios.items():
        print(f"  {s:<6}: ${price:>6.0f}  |  P={weights[s]:.4f}  |  contribution: ${weights[s]*(price+ANNUAL_DIV):.2f}")
    print(f"  EV(model) = ${EV:.2f}  vs  current ${CURRENT_PRICE:.2f}  (model premium: {(EV/CURRENT_PRICE-1)*100:+.1f}%)")

    print(f"\n{sep}")
    print("  SIGNAL DETERMINATION")
    print(sep)
    print(f"  Downside to BEAR ({BEAR:.0f}):  -{DOWNSIDE_PCT:.1f}%")
    print(f"  Upside to BULL ({BULL:.0f}):    +{UPSIDE_PCT:.1f}%")
    print(f"  Ratio B = {RATIO_B:.4f} → {SIGNAL_TEXT}")
    print(f"  EPP floor: EPS_T ${EPS_TROUGH:.2f} × PE_T {PE_TROUGH:.1f}× = ${EPP:.2f}  (gap: {EPP_GAP_PCT:+.1f}%)")

    print(f"\n{sep}")
    print("  CONSERVATIVE 2-YEAR RETURN ESTIMATE")
    print(sep)
    print(f"  FY2026E EPS (consensus, reflecting modest NAM-activity stabilization, not a sharp recovery): ${EPS_FY2026E:.2f}")
    print(f"  Conservative PE applied:                                            {PE_CONSERVATIVE:.1f}× (roughly in line with the ~10.3x forward — no cyclical-recovery re-rating assumed)")
    print(f"  Target price 2yr:                                                   ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.1f}× + ${2*ANNUAL_DIV:.2f} div = ${PRICE_2YR_CONSV:.2f}")
    print(f"  2-year return:                                                      {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  Note: this is the 'North American activity stays roughly where it is, no cyclical inflection,")
    print(f"  and the market keeps applying a trough multiple' floor case — BULL/XBULL require either a NAM")
    print(f"  activity recovery OR the market starting to credit HAL's technology leadership with a re-rating.")

    print(f"\n{sep}")
    print("  WHY THIS IS A ◉ BUY, NOT A ◌ WATCHLIST OR ◎ ACCUMULATE")
    print(sep)
    print("""
  Halliburton is, at its core, one of only two truly global, full-spectrum oilfield-services
  majors — with genuine, multi-generation technology leadership in both of its core segments
  (completions efficiency/electrification in C&P, autonomous drilling/formation evaluation in
  D&E) and an investment-grade balance sheet that has repeatedly proven its worth coming out
  of prior cyclical troughs. It is ALSO, structurally, the most North-America-levered of the
  OFS majors — and that exposure is a genuine, currently-unresolved headwind. But the price
  has already moved to reflect that headwind: at roughly a quarter up its 52-week range, near
  a genuine cyclical-trough multiple (~10-11x depressed forward earnings), the stock's
  downside is already meaningfully compressed while the upside to even a modest activity
  stabilization is sharply asymmetric — Ratio B lands solidly in BUY territory.

  WHAT THE MARKET ALREADY PRICES IN (at $25.20, lower-quarter on the 52-week band):
  • North American land activity stays roughly at current (depressed) levels without a clear
    near-term inflection — essentially a "things stay bad" assumption baked into the price
  • International/offshore activity continues its modest, multi-year-project-driven growth,
    only partially offsetting NAM softness
  • The market applies a deep cyclical-trough discount (~10-11x depressed forward earnings)
    that gives little to no credit for either recovery or HAL's genuine technology leadership

  WHAT COULD MAKE THIS MORE THAN FAIRLY PRICED:
  1. North American land activity inflects — rig counts and completions intensity begin a
     genuine recovery as commodity prices firm and E&P capital budgets normalize upward,
     directly re-accelerating HAL's largest and highest-margin segment
  2. International/offshore mega-projects (Middle East, deepwater Latin America/West Africa)
     move into peak-activity phases, providing a structural offset that finally outpaces NAM
     softness rather than merely cushioning it
  3. The market begins to re-rate HAL's technology platforms (electrification, automation,
     LOGIX) as durable share-gain drivers rather than simply cyclical-survival tools — a
     re-rating OFS majors have repeatedly captured coming out of prior troughs
  4. Continued buybacks at depressed multiples meaningfully reduce the share count, amplifying
     the eventual recovery's per-share impact — compounding returns for patient buyers today

  THE RISK (the honest read on where this sits):
  • Halliburton is structurally the most North-America-levered of the OFS majors — and that
    exposure is a genuine, currently-unresolved headwind with no clear inflection signal yet
  • OFS economics remain fundamentally a function of E&P capital-spending cycles the company
    does not control — capital discipline by E&P operators could persist longer than consensus
    currently assumes, and a deepening trough would compress earnings (and the stock) further
  • International activity, while structurally more stable, has so far only modestly offset
    NAM softness rather than fully compensating for it

  WHAT MAKES THIS A BUY RATHER THAN MERELY A WATCHLIST:
  • The price has already done much of the de-rating work: at a genuine cyclical-trough
    multiple and roughly a quarter up the 52-week range, the bad news is largely in the price
    — this is "buy the technology leader near the trough," not "chase the recovery story"
  • The investment-grade balance sheet (A-/A3-range, net debt/EBITDA ~1.4x) means this is a
    multi-quarter earnings-air-pocket story, not a solvency risk — real downside ballast
  • The technology moats (completions electrification, autonomous drilling) are genuinely
    durable and multi-cycle-proven — they have repeatedly translated into share gains and
    margin outperformance on the way out of past troughs, a pattern likely to repeat
  • Even the EPP-floor and conservative-2yr math (NAM flat, trough multiple, zero recovery
    credit) produces a modestly positive expected return — the setup doesn't require a
    cyclical inflection to work, only patience for one that history says is likely to come

  POSITION SIZING GUIDANCE:
  • BUY — a name to build a full position in at current levels; the asymmetry (compressed
    downside near a cyclical trough vs. sharply convex upside to any activity stabilization)
    is exactly the kind of setup this framework is designed to flag
  • Watch for: NAM rig-count and completions-intensity trends (the dominant swing factor and
    the signal that would accelerate the re-rating), international/offshore project award
    activity, technology-platform adoption/share-gain commentary, and management's capital-
    return cadence as a read on confidence in the through-cycle earnings outlook
""")

    print(SEP)
    print(f"""
SUMMARY: HAL ◉ BUY — Ratio B 0.73× (28.6% downside / 38.9% upside). A TECHNOLOGY-LEADING \
OILFIELD SERVICES GIANT TRADING AT A GENUINE CYCLICAL-TROUGH PRICE: trading at $25.20 \
(52-wk range $18.40-32.10, roughly a quarter up the range — cyclically de-rated into what \
looks like a genuine trough entry point) as North American land activity remains in a \
genuine, unresolved cyclical downturn (rig counts and completions intensity depressed) that \
has compressed HAL's largest, highest-margin segment — the most North-America-levered of \
the OFS majors (~39% of revenue). GENUINE TECHNOLOGY MOATS: completions electrification/ \
automation leadership (ZEUS electric fleets, iEnergy) in C&P (~56% of revenue) and \
autonomous-drilling/formation-evaluation differentiation (LOGIX, iCruise, Sperry Drilling) \
in D&E (~44%) — durable, multi-cycle-proven advantages that have repeatedly translated into \
share gains coming out of past troughs. INVESTMENT-GRADE RESILIENCE: A-/A3-range balance \
sheet (net debt ~$6.6B, ~1.4x EBITDA) and continued dividend-plus-buyback capital returns \
even through the downcycle signal genuine financial strength. THE HONEST RISK: NAM activity \
shows no clear inflection yet, international/offshore activity (~61% of revenue) has only \
modestly offset the softness, and OFS economics remain fundamentally a function of E&P capex \
cycles HAL doesn't control. Consensus 'Hold/Buy (mixed)' (~13 of 29 analysts Buy), PT ~$29 \
(range $22-38). Conservative 2yr (NAM-flat, trough-multiple floor case): EPS $2.45 x 10.0x \
+ $1.36 div = $25.86 -> +2.6% — BULL/XBULL require either a NAM activity inflection OR the \
market crediting HAL's technology leadership with a re-rating. THE PRICE ALREADY REFLECTS \
THE BAD NEWS: compressed downside near a cyclical-trough multiple against sharply asymmetric \
upside to any activity stabilization — build a full position at current levels. \
Bear $18 · Base $25 · Bull $35 · XBull $44."""
    )

    print(f"SIGNAL: {SIGNAL_TEXT} (technology-leading global oilfield-services major caught in a North American activity downcycle, trading at a depressed cyclical-trough multiple) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
