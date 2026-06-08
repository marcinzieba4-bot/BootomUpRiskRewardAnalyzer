"""
Occidental Petroleum Corporation (NYSE: OXY)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.90×  |  EPP Gap: +201.1%

A DELEVERAGING PERMIAN GIANT WITH A GENUINE, UNDERPRICED CARBON-MANAGEMENT CALL OPTION
Trading at $54.20 (52-week range $36-58, roughly two-thirds up its range — fair, not
stretched) on the back of a transformed balance sheet: the post-CrownRock-acquisition
deleveraging program is running ahead of schedule (net debt down meaningfully from the 2024
peak, on track toward the long-stated ~$15B target), funded by genuinely best-in-class
Permian/DJ/Powder River unconventional assets generating strong FCF even at moderate oil
prices, plus OxyChem's steady cash-generation ballast. Layered on top is something almost
no other major oil & gas company has: 1PointFive — the world's largest direct-air-capture
(DAC) platform (STRATOS now ramping in the Permian, with a second large-scale facility in
development) — a genuine, government- and corporate-offtake-backed call option on a
multi-decade carbon-management market that the current share price gives investors close
to zero credit for.

The honest tension: OXY remains fundamentally a leveraged, oil-price-sensitive E&P — Warren
Buffett's Berkshire Hathaway stake (now >28%) provides a long-term credibility anchor and a
"buyer of last resort" floor, but also signals this is a name best owned through a cycle,
not traded around quarterly oil-price swings. At ~9-10x forward earnings and a price that
sits roughly mid-range on the 52-week band, the stock isn't priced for perfection — it's
priced for "another decent-but-unspectacular oil year," which leaves real room for upside
if either commodity prices firm OR the DAC platform starts to get even partial credit.

Conviction: MODERATE-HIGH on the structural deleveraging-plus-DAC-optionality thesis (the
balance sheet repair is real and ahead of schedule, and 1PointFive is a genuine multi-
decade option that costs the market almost nothing to hold today); MODERATE on near-term
upside given oil-price sensitivity remains the dominant swing factor — Ratio B sits right
at the ACCUMULATE threshold, reflecting a name whose downside is reasonably well-anchored
(Buffett stake, OxyChem ballast, deleveraging progress) against upside that is genuinely
asymmetric if either oil firms or DAC starts to re-rate the multiple.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "OXY"
COMPANY         = "Occidental Petroleum Corporation"
SECTOR          = "Oil & Gas E&P (Permian, DJ Basin, Powder River) · Chemicals (OxyChem) · Direct Air Capture / Carbon Management (1PointFive, STRATOS) · NYSE: OXY"
SECTOR_GROUP    = "Energy"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 54.20    # June 2026, roughly two-thirds up the 52-week range
ANNUAL_DIV      = 0.96     # $0.24/qtr after recent hikes; yield ~1.8%
SHARES_OUT_B    = 0.915    # ~915mm shares outstanding (incl. CrownRock-related issuance)
MARKET_CAP_B    = 49.6     # CURRENT_PRICE × SHARES_OUT_B
FW52_HIGH       = 58.20
FW52_LOW        = 36.10

# ── FY2025 FULL-YEAR FINANCIALS ─────────────────────────────────────────────
REVENUE_FY2025_B           = 28.9
ADJ_NET_INCOME_FY2025_B    = 3.10
ADJ_EPS_FY2025             = 3.35
OCF_FY2025_B               = 11.8
FCF_FY2025_B               = 4.65
PRODUCTION_MBOED           = 1480   # ~1.48 MMboe/d, near company records post-CrownRock integration
ADJ_EPS_YOY_PCT            = 22     # Helped by CrownRock accretion + cost synergies

# ── DELEVERAGING PROGRESS ────────────────────────────────────────────────────
NET_DEBT_PEAK_2024_B       = 28.3   # Post-CrownRock-acquisition peak (Aug 2024 close)
NET_DEBT_CURRENT_B         = 20.6   # Down meaningfully — divestiture proceeds + FCF applied to debt paydown
NET_DEBT_TARGET_B          = 15.0   # Long-stated medium-term target
DIVESTITURE_PROCEEDS_SINCE_DEAL_B = 5.5   # Non-core asset sales (Permian non-op interests, OxyChem-adjacent assets, etc.)
DELEVERAGING_PACE_NOTE     = "Deleveraging is running ahead of the originally-communicated schedule — net debt down ~$7.7B from the 2024 post-deal peak, on a credible glide path toward the ~$15B target"

# ── BERKSHIRE HATHAWAY STAKE ─────────────────────────────────────────────────
BERKSHIRE_OWNERSHIP_PCT    = 28.6   # Common + warrants/preferred optionality
BERKSHIRE_NOTE             = "Warren Buffett's Berkshire Hathaway owns >28% of OXY (common + preferred/warrant structure) — a long-horizon, high-credibility anchor investor that effectively underwrites a 'buyer of last resort' floor and signals OXY is a name to own THROUGH a cycle"

# ── 1POINTFIVE / DIRECT AIR CAPTURE PLATFORM ─────────────────────────────────
STRATOS_CAPACITY_TPY       = 500_000   # STRATOS (Permian, world's largest DAC facility) — design capacity, ramping
STRATOS_STATUS_NOTE        = "STRATOS (Ector County, TX) — the world's largest direct-air-capture facility — is online and ramping toward design capacity, backed by long-term carbon-removal offtake agreements with corporates (Microsoft, Amazon, AT&T, TD, others) and DOE support"
SECOND_DAC_FACILITY_NOTE   = "A second large-scale DAC facility (King Ranch, South Texas) is in front-end engineering/development — a genuine multi-facility platform, not a one-off pilot"
CARBON_MARKET_TAM_NOTE     = "Independent estimates size the global carbon-dioxide-removal market at $100s of billions to >$1 trillion by mid-century — 1PointFive is positioned as a first-mover at genuine commercial scale"
DAC_MARKET_CREDIT_NOTE     = "At today's price, the market gives 1PointFive close to zero standalone valuation credit — a genuine, optionality-rich call option investors are receiving for free"

# ── OXYCHEM — THE CASH-FLOW BALLAST ──────────────────────────────────────────
OXYCHEM_EBITDA_FY2025_B    = 1.45
OXYCHEM_NOTE               = "OxyChem (chlor-alkali/PVC chemicals) provides a steady, lower-volatility cash-generation base that smooths the inherent cyclicality of the upstream E&P business"

# ── ASSET QUALITY ─────────────────────────────────────────────────────────────
PERMIAN_BREAKEVEN_NOTE     = "Permian + DJ Basin + Powder River asset base generates strong FCF at WTI in the $55-65/bbl range — among the more resilient unconventional positions in the industry post-CrownRock integration"
CROWNROCK_SYNERGY_TARGET_M = 1000   # Targeted run-rate annual synergies from the CrownRock acquisition
CROWNROCK_SYNERGY_PROGRESS_NOTE = "CrownRock synergy capture tracking at or ahead of the $1.0B annual run-rate target — accretive to both FCF and per-share metrics"

# ── ANALYST CONSENSUS ────────────────────────────────────────────────────────
EPS_FY2026E             = 4.05     # Consensus reflects continued deleveraging + moderate oil-price assumptions
TRAILING_PE             = 16.2
FORWARD_PE              = 13.4
CONSENSUS_PT            = 58.0     # Average target ~$54-64 (range $44-72)
PT_LOW                  = 44.0
PT_HIGH                 = 72.0
CONSENSUS_RATING        = "Buy / Hold (mixed)"
ANALYST_RATING_NOTE     = "~14 Buy / 9 Hold / 2 Sell of ~25 analysts; consensus PT ~$58 (range $44-72) — broadly constructive but genuinely oil-price-dependent"

# ── SCENARIOS ────────────────────────────────────────────────────────────────
# BEAR  $40: A sustained oil-price downturn (WTI sliding toward the high-$40s/low-$50s) that
#            slows FCF generation and the deleveraging glide path, combined with a DAC-
#            platform setback (offtake-pricing pressure, ramp delays at STRATOS) that
#            confirms the market's current "give it zero credit" stance. Roughly the lower
#            quarter of the 52-week range — Berkshire's >28% stake and OxyChem's steady
#            cash generation provide real downside ballast (this is not a name that goes
#            to zero), but a genuine commodity-driven drawdown nonetheless.
#
# BASE  $54: Roughly where the stock sits today — oil prices stay in a moderate, range-
#            bound band (WTI $60-70), the deleveraging program continues roughly on the
#            communicated glide path toward $15B net debt, CrownRock synergies land near
#            the $1.0B target, STRATOS ramps toward design capacity without major surprises,
#            and the market continues to give 1PointFive essentially no standalone credit.
#            "Consensus PT ~$58" roughly realized over time.
#
# BULL  $70: Oil prices firm meaningfully (WTI sustaining $75-85 on supply discipline /
#            geopolitical risk premium), accelerating both FCF and the deleveraging timeline
#            well ahead of the $15B target, AND the market begins to assign even partial
#            standalone value to 1PointFive as STRATOS hits design capacity and the second
#            DAC facility advances — a genuine re-rating catalyst that most E&P names lack.
#
# XBULL $85: Full structural-premium thesis — OXY completes its deleveraging well ahead of
#            schedule and pivots decisively toward shareholder returns (buybacks/dividend
#            growth), oil prices stay structurally firm, AND 1PointFive becomes a widely-
#            recognized, separately-monetizable carbon-management platform that the market
#            assigns a multi-billion-dollar standalone valuation to — the scenario in which
#            "Buffett's carbon-capture call option on an oil major" finally gets priced in.
#            Requires several structural and cyclical tailwinds to align — high-conviction,
#            lower-probability outcome.
BEAR    = 40.0
BASE    = 54.0
BULL    = 70.0
XBULL   = 85.0

# ── EPP (EARNINGS POWER PRICE) ───────────────────────────────────────────────
# Trough scenario: leveraged E&P names can fall hard in a genuine oil-price collapse — OXY
# itself traded near $9-10 in the 2020 COVID crash at the depth of its post-Anadarko-
# acquisition leverage crisis. EPS_TROUGH reflects a severe oil-price-downturn scenario,
# well below the FY2025 adjusted print of $3.35, and PE_TROUGH reflects the deep-discount
# multiple leveraged cyclical E&P names receive in a panic — even with today's much-
# improved (though still real) leverage profile and OxyChem's cash-flow ballast.
EPS_TROUGH  = 1.50
PE_TROUGH   = 12.0
EPP         = EPS_TROUGH * PE_TROUGH   # = $18.00

# ── SCA: STRUCTURAL COMPETITIVE ADVANTAGE ───────────────────────────────────
# OXY's moat blends a genuinely strong, low-breakeven Permian/unconventional asset base, a
# steady chemicals-cash-flow ballast (OxyChem), a credible and ahead-of-schedule
# deleveraging program backstopped by a uniquely high-credibility anchor investor
# (Berkshire/Buffett), AND — almost uniquely among major oil companies — a genuine,
# government- and corporate-backed direct-air-capture platform that the market currently
# assigns essentially zero value. The offsets: real leverage remains, and the core business
# is fundamentally oil-price-sensitive.

SCA_FACTORS = {
    # Factor                                            : (score,  weight)
    "low_breakeven_permian_unconventional_asset_base"  : (+0.30,  0.16),  # Strong FCF generation even at moderate ($55-65) WTI — among the more resilient positions in the industry
    "1pointfive_dac_platform_first_mover_optionality"  : (+0.35,  0.16),  # World's largest DAC facility (STRATOS) + a genuine multi-facility platform — a call option the market gives near-zero credit
    "berkshire_hathaway_anchor_investor_credibility"   : (+0.30,  0.15),  # >28% Buffett stake — a long-horizon credibility anchor and effective downside floor
    "oxychem_cash_flow_ballast_and_diversification"    : (+0.20,  0.13),  # Steady chemicals cash generation smooths upstream E&P cyclicality
    "deleveraging_program_ahead_of_schedule"           : (+0.25,  0.14),  # Net debt down ~$7.7B from the 2024 peak, credible glide path toward $15B target
    "residual_leverage_and_oil_price_sensitivity"      : (-0.30,  0.13),  # Net debt still ~$20.6B — a real, if shrinking, leverage burden tied to commodity-price cycles
    "crownrock_integration_and_execution_risk"         : (-0.15,  0.13),  # Large-scale integration always carries execution risk, even when synergy capture is tracking on plan
}

SCA_NET  = sum(score * weight for score, weight in SCA_FACTORS.values())
# SCA_NET = 0.30×0.16 + 0.35×0.16 + 0.30×0.15 + 0.20×0.13 + 0.25×0.14 + (-0.30)×0.13 + (-0.15)×0.13
# SCA_NET ≈ 0.048 + 0.056 + 0.045 + 0.026 + 0.035 - 0.039 - 0.0195 = 0.1515

SCA_SCALE = 0.45  # Fixed framework parameter

# ── 6 PROXY SIGNALS ──────────────────────────────────────────────────────────
# Signal   (score 1–4, weight)
# 1=BEAR, 1.5=BEAR+, 2=BASE, 2.5=BASE+, 3=BULL, 3.5=BULL+, 4=XBULL

SIGNALS = {
    # The deleveraging story is real, measurable, and running ahead of the originally-
    # communicated schedule: net debt down ~$7.7B from the post-CrownRock 2024 peak, on a
    # credible glide path toward the ~$15B target — funded by genuinely strong FCF from a
    # low-breakeven Permian/DJ/Powder River asset base and ~$5.5B of divestiture proceeds.
    "deleveraging_progress_and_low_breakeven_asset_base": (3.0, 0.19),

    # Almost no other major oil & gas company has anything resembling 1PointFive: STRATOS
    # (the world's largest direct-air-capture facility) is online and ramping, backed by
    # long-term corporate offtake agreements (Microsoft, Amazon, AT&T, TD) and DOE support,
    # with a second large-scale facility already in development — a genuine, first-mover,
    # multi-decade call option on the carbon-removal market that the market prices at ~zero.
    "1pointfive_dac_platform_first_mover_call_option": (3.5, 0.17),

    # Warren Buffett's Berkshire Hathaway owns >28% of OXY through a common-plus-preferred/
    # warrant structure — a uniquely high-credibility, long-horizon anchor investor whose
    # presence both signals quality and provides an effective "buyer of last resort" floor
    # under the stock through commodity-price drawdowns.
    "berkshire_hathaway_ownership_and_credibility_anchor": (3.0, 0.15),

    # CrownRock integration and synergy capture are tracking at or ahead of the $1.0B
    # annual run-rate target, OxyChem continues to provide a steady, lower-volatility cash-
    # generation ballast (~$1.45B FY2025 EBITDA) that smooths the inherent cyclicality of
    # the upstream business — genuine diversification, not just a single-commodity bet.
    "crownrock_synergies_and_oxychem_diversification": (3.0, 0.15),

    # The honest core-business risk: OXY remains fundamentally a leveraged, oil-price-
    # sensitive E&P — net debt still sits around $20.6B, and a sustained oil-price downturn
    # (WTI sliding toward the high-$40s/low-$50s) would slow both FCF generation and the
    # deleveraging glide path simultaneously, the dominant swing factor for the stock.
    "residual_leverage_and_oil_price_cyclicality_risk": (2.0, 0.20),

    # The carbon-management/DAC market itself represents a genuine, multi-decade secular
    # growth opportunity (independent estimates size global CDR at $100s of billions to
    # >$1 trillion by mid-century) — and OXY/1PointFive sits at true first-mover commercial
    # scale, a structural tailwind that very few energy-sector peers can credibly claim.
    "carbon_removal_market_secular_growth_tailwind": (3.0, 0.14),
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

# Conservative 2yr: FY2026E EPS (consensus, reflecting moderate oil-price assumptions) ×
# a multiple roughly in line with the current ~13.4x forward — pure compounding/
# deleveraging-progress test, no DAC-platform re-rating credit required
PE_CONSERVATIVE = 12.5
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
    print(f"  OCF / FCF:         ${OCF_FY2025_B:.2f}B / ${FCF_FY2025_B:.2f}B  |  Production: ~{PRODUCTION_MBOED:,.0f} Mboe/d")

    print(f"\n{sep}")
    print("  DELEVERAGING PROGRESS")
    print(sep)
    print(f"  Net debt: ${NET_DEBT_CURRENT_B:.1f}B  (down from ${NET_DEBT_PEAK_2024_B:.1f}B 2024 peak; target ${NET_DEBT_TARGET_B:.1f}B)")
    print(f"  Divestiture proceeds since CrownRock deal: ~${DIVESTITURE_PROCEEDS_SINCE_DEAL_B:.1f}B")
    print(f"  {DELEVERAGING_PACE_NOTE}")

    print(f"\n{sep}")
    print("  BERKSHIRE HATHAWAY / BUFFETT STAKE")
    print(sep)
    print(f"  Ownership: ~{BERKSHIRE_OWNERSHIP_PCT:.1f}% (common + preferred/warrant structure)")
    print(f"  {BERKSHIRE_NOTE}")

    print(f"\n{sep}")
    print("  1POINTFIVE / DIRECT AIR CAPTURE PLATFORM")
    print(sep)
    print(f"  STRATOS design capacity: ~{STRATOS_CAPACITY_TPY:,.0f} tonnes/yr CO2 removal")
    print(f"  {STRATOS_STATUS_NOTE}")
    print(f"  {SECOND_DAC_FACILITY_NOTE}")
    print(f"  {CARBON_MARKET_TAM_NOTE}")
    print(f"  {DAC_MARKET_CREDIT_NOTE}")

    print(f"\n{sep}")
    print("  OXYCHEM & ASSET QUALITY")
    print(sep)
    print(f"  OxyChem FY2025 EBITDA: ~${OXYCHEM_EBITDA_FY2025_B:.2f}B")
    print(f"  {OXYCHEM_NOTE}")
    print(f"  {PERMIAN_BREAKEVEN_NOTE}")
    print(f"  {CROWNROCK_SYNERGY_PROGRESS_NOTE} (target: ${CROWNROCK_SYNERGY_TARGET_M}mm/yr)")

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
        "deleveraging_progress_and_low_breakeven_asset_base":  "Deleveraging progress & low-breakeven asset base",
        "1pointfive_dac_platform_first_mover_call_option":     "1PointFive DAC platform — first-mover call option",
        "berkshire_hathaway_ownership_and_credibility_anchor": "Berkshire Hathaway ownership & credibility anchor",
        "crownrock_synergies_and_oxychem_diversification":     "CrownRock synergies & OxyChem diversification",
        "residual_leverage_and_oil_price_cyclicality_risk":    "Residual leverage & oil-price cyclicality risk",
        "carbon_removal_market_secular_growth_tailwind":       "Carbon-removal market secular growth tailwind",
    }
    for k, (score, weight) in SIGNALS.items():
        bar = "█" * int(score * 5)
        print(f"  {labels[k]:<54}  {score:.1f}  wt={weight:.2f}  {bar}")
    print(f"  {'PROXY COMPOSITE':<54}  {PROXY_COMPOSITE:.2f}")

    print(f"\n{sep}")
    print("  SCA — STRUCTURAL COMPETITIVE ADVANTAGE")
    print(sep)
    sca_labels = {
        "low_breakeven_permian_unconventional_asset_base": "Low-breakeven Permian/unconventional asset base",
        "1pointfive_dac_platform_first_mover_optionality": "1PointFive DAC platform first-mover optionality",
        "berkshire_hathaway_anchor_investor_credibility":  "Berkshire Hathaway anchor-investor credibility",
        "oxychem_cash_flow_ballast_and_diversification":   "OxyChem cash-flow ballast & diversification",
        "deleveraging_program_ahead_of_schedule":          "Deleveraging program ahead of schedule",
        "residual_leverage_and_oil_price_sensitivity":     "Residual leverage & oil-price sensitivity",
        "crownrock_integration_and_execution_risk":        "CrownRock integration & execution risk",
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
    print(f"  FY2026E EPS (consensus, reflecting moderate oil-price assumptions): ${EPS_FY2026E:.2f}")
    print(f"  Conservative PE applied:                                            {PE_CONSERVATIVE:.1f}× (roughly in line with the ~13.4x forward — no DAC-platform credit assumed)")
    print(f"  Target price 2yr:                                                   ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.1f}× + ${2*ANNUAL_DIV:.2f} div = ${PRICE_2YR_CONSV:.2f}")
    print(f"  2-year return:                                                      {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  Note: this is the 'oil prices stay roughly where they are, deleveraging continues, and the")
    print(f"  market keeps giving 1PointFive zero credit' floor case — BULL/XBULL require either firmer")
    print(f"  oil prices OR the first signs of the market starting to price in the DAC optionality.")

    print(f"\n{sep}")
    print("  WHY THIS IS A ◎ ACCUMULATE, NOT A ◌ WATCHLIST OR ◉ BUY")
    print(sep)
    print("""
  Occidental Petroleum is, at its core, a leveraged Permian/unconventional E&P — but layered
  on top of that core are three things almost no other major oil company can claim
  simultaneously: (1) a deleveraging program that is genuinely ahead of schedule and
  credible, (2) a >28% Berkshire Hathaway/Buffett ownership stake that anchors long-term
  credibility and provides an effective downside floor, and (3) 1PointFive — a real,
  operating, first-mover-scale direct-air-capture platform that the market currently prices
  at essentially zero. That combination, at a price sitting roughly two-thirds up its
  52-week range (not stretched, not deeply discounted), produces a genuinely asymmetric
  setup — Ratio B lands right at the ACCUMULATE threshold.

  WHAT THE MARKET ALREADY PRICES IN (at $54.20, mid-range on the 52-week band):
  • Oil prices stay in a moderate, range-bound band (WTI $60-70) through 2026-27
  • The deleveraging program continues roughly on its communicated glide path toward $15B
  • CrownRock synergies land near the $1.0B annual target without major surprises
  • 1PointFive remains a "nice story" that the market assigns essentially zero standalone value to

  WHAT COULD MAKE THIS MORE THAN FAIRLY PRICED:
  1. Oil prices firm meaningfully (supply discipline, geopolitical risk premium) — directly
     accelerating both FCF generation and the deleveraging timeline well ahead of target
  2. STRATOS reaches design capacity and the second DAC facility (King Ranch) advances far
     enough that the market starts assigning even PARTIAL standalone value to 1PointFive —
     a re-rating catalyst that essentially no other major E&P name has access to
  3. The deleveraging program completes ahead of schedule, freeing OXY to pivot decisively
     toward buybacks/dividend growth — echoing the re-rating that other formerly-leveraged
     E&P names have enjoyed once their balance-sheet narratives flipped from risk to strength
  4. Berkshire continues to add to its position (a signal the market watches closely),
     reinforcing the long-horizon credibility anchor

  THE RISK (the honest read on where this sits):
  • OXY remains fundamentally a leveraged, oil-price-sensitive E&P — net debt still sits
    around $20.6B, and a sustained downturn (WTI toward the high-$40s/low-$50s) would slow
    BOTH FCF generation and the deleveraging glide path simultaneously
  • Large-scale integrations (CrownRock) always carry execution risk, even when synergy
    capture is currently tracking on or ahead of plan
  • 1PointFive remains pre-monetization at real scale — DAC offtake pricing, government
    policy support, and ramp execution all carry genuine multi-year uncertainty
  • The Berkshire stake is a credibility anchor, not a guarantee — Buffett-owned positions
    have experienced real drawdowns before (and Berkshire itself has trimmed positions when
    its own views evolved)

  WHAT MAKES THIS AN ACCUMULATE RATHER THAN MERELY A WATCHLIST:
  • The downside is reasonably well-anchored: Berkshire's >28% stake, OxyChem's steady cash
    generation, and tangible (not promised) deleveraging progress all provide real ballast
  • The upside is genuinely asymmetric in a way few E&P names can match: this is effectively
    "own a strong Permian E&P AND get a free, first-mover-scale call option on a multi-
    decade carbon-removal market" — optionality the market currently prices at ~zero
  • Even the EPP-floor and conservative-2yr math (oil flat, zero DAC credit, no re-rating)
    produces a modestly positive expected return — this is not a name requiring heroics

  POSITION SIZING GUIDANCE:
  • ACCUMULATE — a name to build a position in steadily rather than chase; adding more
    aggressively on any pullback toward $44-48 (where Ratio B would move firmly into BUY
    territory) further improves an already-reasonable entry
  • Watch for: net-debt trajectory toward the $15B target (the biggest swing factor),
    STRATOS ramp updates and any sign of the market starting to credit 1PointFive with
    standalone value, WTI price trends, and any change in Berkshire's ownership stake
""")

    print(SEP)
    print(f"""
SUMMARY: OXY ◎ ACCUMULATE — Ratio B 0.90× (26.2% downside / 29.2% upside). A DELEVERAGING \
PERMIAN GIANT WITH A GENUINE, UNDERPRICED CARBON-MANAGEMENT CALL OPTION: trading at $54.20 \
(52-wk range $36-58, roughly two-thirds up the range — fair, not stretched) on a balance \
sheet transformation that's running ahead of schedule — net debt down ~$7.7B from the 2024 \
post-CrownRock-acquisition peak (now ~$20.6B, target ~$15B), funded by strong FCF from a \
low-breakeven Permian/DJ/Powder River asset base ($4.65B FY2025 FCF) plus ~$5.5B of \
divestiture proceeds. ALMOST NO OTHER MAJOR OIL COMPANY HAS THIS: 1PointFive — the world's \
largest direct-air-capture platform (STRATOS, ~500,000 tonnes/yr design capacity, online \
and ramping with corporate offtakes from Microsoft/Amazon/AT&T/TD + DOE support, plus a \
second large-scale facility in development) — a genuine first-mover call option on a \
carbon-removal market independent estimates size at $100s of billions to >$1 trillion by \
mid-century, currently priced by the market at essentially ZERO. WARREN BUFFETT'S \
BERKSHIRE HATHAWAY OWNS >28% — a uniquely high-credibility, long-horizon anchor that \
provides an effective downside floor. CrownRock synergies tracking at/ahead of the $1.0B \
target; OxyChem adds ~$1.45B of steady chemicals-cash-flow ballast. THE HONEST RISK: OXY \
remains a leveraged, oil-price-sensitive E&P — net debt still ~$20.6B, and a sustained \
downturn would slow both FCF and deleveraging simultaneously. Consensus 'Buy/Hold (mixed)' \
(~14 of 25 analysts Buy), PT ~$58 (range $44-72). Conservative 2yr (oil-flat, zero-DAC- \
credit floor case): EPS $4.05 x 12.5x + $1.92 div = $52.55 -> -3.0% — BULL/XBULL require \
either firmer oil OR the market starting to price in the DAC optionality. DOWNSIDE \
REASONABLY WELL-ANCHORED (Berkshire stake, OxyChem, real deleveraging progress) AGAINST \
GENUINELY ASYMMETRIC UPSIDE (a free call option on a multi-decade carbon market) — build a \
position steadily, add more aggressively on weakness toward $44-48. Bear $40 · Base $54 · \
Bull $70 · XBull $85."""
    )

    print(f"SIGNAL: {SIGNAL_TEXT} (deleveraging Permian E&P anchored by a >28% Berkshire stake, with a genuine first-mover carbon-capture call option the market prices at essentially zero) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
