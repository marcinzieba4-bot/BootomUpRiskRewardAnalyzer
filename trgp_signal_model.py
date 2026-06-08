"""
Targa Resources Corp. (NYSE: TRGP)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◌ WATCHLIST  |  Ratio B: 1.35×  |  EPP Gap: +339.8%

THE PERMIAN NGL TOLL-ROAD COMPOUNDER — A GREAT BUSINESS, BUT THE MARKET ALREADY KNOWS IT
Trading at $192.40 (52-week range $130-201, near an all-time high, up roughly 45% over the
past year) on the back of a genuinely dominant, vertically-integrated Permian Basin
gathering-processing-NGL-fractionation-export franchise: record gas processing volumes,
a swelling multi-year growth-project backlog (Permian Midstream expansions, Train 11/12
fractionators, Daytona NGL pipeline ramping), and a capital-allocation story that has
pivoted decisively from "growth capex sponge" to "growing dividend + opportunistic buyback"
machine — the dividend has been raised aggressively for several consecutive years running
(management has guided to ~33% average annual increases through 2027) on a balance sheet
that has been de-levered into investment-grade territory.

The honest tension: this re-rating from "commodity-exposed midstream" toward "premium
fee-based/contracted infrastructure compounder" has been the single most consensus, most
profitable midstream trade of the last three years — and at ~17-19x forward earnings and
roughly 11-12x EV/EBITDA near an all-time high, the multiple has expanded to reflect a
durable structural premium rather than a discounted cyclical-energy one. Volumes and
backlog conversion still have real room to run, but a meaningful fraction of the next
several years of growth already appears underwritten in the price.

Conviction: MODERATE-HIGH on the structural Permian-NGL-toll-road thesis (genuinely the
best-positioned integrated NGL franchise in the basin, with real multi-year project
visibility); LOW-MODERATE on near-term upside from current levels given the stock sits
within ~4% of an all-time high after an outsized run — Ratio B lands in WATCHLIST
territory pending either a pullback or confirmation that the growth backlog converts to
EBITDA fast enough to keep outrunning an already-rich multiple.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "TRGP"
COMPANY         = "Targa Resources Corp."
SECTOR          = "Midstream Energy · Permian Basin Gathering & Processing · NGL Fractionation, Logistics & Export (LPG/Daytona) · NYSE: TRGP"
SECTOR_GROUP    = "Energy"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 192.40   # June 2026, near an all-time high
ANNUAL_DIV      = 4.60     # $1.15/qtr after consecutive aggressive hikes; yield ~2.4%
SHARES_OUT_B    = 0.218    # ~218mm shares outstanding
MARKET_CAP_B    = 41.9     # CURRENT_PRICE × SHARES_OUT_B
FW52_HIGH       = 201.00
FW52_LOW        = 130.30

# ── FY2025 FULL-YEAR FINANCIALS ─────────────────────────────────────────────
REVENUE_FY2025_B          = 20.9
ADJ_EBITDA_FY2025_B       = 5.36    # Record — up double digits YoY
ADJ_EBITDA_YOY_PCT        = 14
NET_INCOME_FY2025_B       = 1.56
ADJ_EPS_FY2025            = 7.05
GROWTH_CAPEX_FY2025_B     = 2.7     # Bulk of capex now toward de-risked, contracted growth projects
PERMIAN_VOLUMES_RECORD_NOTE = "Record Permian Basin natural gas inlet volumes — Permian Midstream segment averaging well above 6.0 Bcf/d gathered, with continued sequential growth"

# ── FY2026 GUIDANCE ──────────────────────────────────────────────────────────
ADJ_EBITDA_GUIDANCE_LOW_B  = 5.7
ADJ_EBITDA_GUIDANCE_HIGH_B = 6.1
GUIDANCE_NOTE              = "Guidance assumes continued Permian producer activity at a moderate (not torrid) pace, with incremental EBITDA weighted to 2H26 as new projects ramp"

# ── GROWTH PROJECT BACKLOG ───────────────────────────────────────────────────
TRAIN_PROJECTS_NOTE        = "Train 11 (in service) and Train 12 fractionator (under construction, Mont Belvieu) add ~150+ Mbbl/d of incremental NGL fractionation capacity"
DAYTONA_PIPELINE_NOTE      = "Daytona NGL Pipeline (Permian-to-Mont-Belvieu, ~600 Mbbl/d capacity, expandable) ramping toward full utilization — a long-haul, fee-based backbone asset"
PERMIAN_MIDSTREAM_EXPANSION_NOTE = "Multiple new Permian gas processing plants (Bull Moose, Wildcat, and successors) coming online through 2026-2028 — each backed by long-term, largely fee-based/MVC contracts"
GROWTH_BACKLOG_CAPITAL_B   = 5.0   # Multi-year identified growth-capital program, largely already sanctioned/under construction

# ── CAPITAL ALLOCATION & BALANCE SHEET ───────────────────────────────────────
DIV_GROWTH_GUIDANCE_PCT    = 33    # Management guidance: ~33% average annual dividend growth through 2027
DIV_CONSECUTIVE_HIKE_YEARS = 4
BUYBACK_AUTHORIZATION_B    = 1.0
NET_DEBT_TO_EBITDA         = 3.4   # Targeting structurally lower leverage (3.0-3.5x) as EBITDA grows into it
CREDIT_RATING_NOTE         = "Upgraded to investment grade across all three major agencies (BBB-/Baa3/BBB-) — a structural re-rating catalyst in its own right"
FEE_BASED_CONTRACT_MIX_PCT = 90    # Approx. share of gross margin that is fee-based/percent-of-proceeds/contracted, not direct commodity exposure

# ── ANALYST CONSENSUS ────────────────────────────────────────────────────────
EPS_FY2026E             = 9.10     # Consensus ~$8.60-9.60, reflecting backlog conversion + buybacks
TRAILING_PE             = 27.3
FORWARD_PE              = 21.1
EV_EBITDA_MULTIPLE      = 11.5
CONSENSUS_PT            = 205.0    # Average target ~$190-220 (range $165-245)
PT_LOW                  = 165.0
PT_HIGH                 = 245.0
CONSENSUS_RATING        = "Buy / Strong Buy"
ANALYST_RATING_NOTE     = "~19 Buy / 5 Hold / 1 Sell of ~25 analysts; consensus PT ~$205 (range $165-245) — broadly bullish but with a wide band reflecting valuation-vs-growth debate"

# ── SCENARIOS ────────────────────────────────────────────────────────────────
# BEAR  $135: A 2026-27 Permian activity slowdown — producer capex discipline deepens on
#             softer oil/gas prices, new-plant ramps slip behind schedule, and the market
#             re-rates TRGP from a "premium fee-based infrastructure compounder" multiple
#             (~11-12x EV/EBITDA) back toward a more typical midstream multiple (~8-9x) on
#             flat-to-modestly-growing EBITDA. Roughly the lower third of the 52-week range —
#             the now-investment-grade balance sheet and ~90% fee-based mix keep the dividend
#             growth program intact (perhaps decelerating from 33% toward high-single-digits),
#             but this is a real multiple-compression drawdown, not a "soft landing."
#
# BASE  $192: Roughly where the stock sits today — Permian volumes keep setting records at a
#             moderate pace, Train 12 and the new processing plants come online roughly on
#             schedule, Daytona keeps ramping toward full utilization, and the dividend keeps
#             growing at a healthy (if decelerating from the initial 33% guide) clip funded by
#             EBITDA growth and a de-levering balance sheet. "Consensus PT ~$205" roughly realized.
#
# BULL  $235: The growth backlog converts faster and at better-than-guided returns — Permian
#             gas/NGL volumes accelerate on continued associated-gas growth and LNG-feedgas-
#             driven demand pull, Daytona and the new fractionators run at full utilization
#             ahead of schedule, and the market further re-rates TRGP toward the multiples
#             enjoyed by the highest-quality, most-integrated midstream peers (mid-teens
#             EV/EBITDA), rewarding the now-investment-grade, ~90% fee-based franchise.
#
# XBULL $270: Full structural-premium thesis — TRGP becomes THE reference name for "Permian
#             NGL infrastructure as a structurally scarce, irreplaceable toll road," LNG-
#             export-driven NGL/condensate demand pulls volumes sharply higher for years,
#             buybacks accelerate alongside the dividend program, and the multiple converges
#             with the most expensive infrastructure/utility-like compounders in the market.
#             Requires several structural and cyclical tailwinds to align simultaneously —
#             the highest-conviction, lowest-probability outcome.
BEAR    = 135.0
BASE    = 192.0
BULL    = 235.0
XBULL   = 270.0

# ── EPP (EARNINGS POWER PRICE) ───────────────────────────────────────────────
# Trough scenario: midstream names with real commodity-price/volume sensitivity can still
# fall hard in a genuine industry downcycle (TRGP itself traded near $25-30 in the 2020
# COVID collapse, before its de-leveraging/re-rating transformation). EPS_TROUGH reflects a
# severe Permian-activity-slowdown scenario, well below the FY2025 print of $7.05, and
# PE_TROUGH reflects the discount multiple cyclical/levered midstream names receive in a
# panic — even with today's much-improved, ~90% fee-based, investment-grade profile.
EPS_TROUGH  = 3.50
PE_TROUGH   = 12.5
EPP         = EPS_TROUGH * PE_TROUGH   # = $43.75

# ── SCA: STRUCTURAL COMPETITIVE ADVANTAGE ───────────────────────────────────
# TRGP's moat is genuinely structural: the most vertically-integrated gathering-processing-
# fractionation-export franchise in the highest-growth basin (Permian) in North American
# energy, now layered with an investment-grade balance sheet and a credible multi-year
# capital-return program. The offsets are real too: the stock has already re-rated hard to
# reflect this, and a meaningful (though shrinking) slice of margin remains commodity-linked.

SCA_FACTORS = {
    # Factor                                            : (score,  weight)
    "permian_vertical_integration_and_scale"           : (+0.35,  0.18),  # Dominant gathering-processing-fractionation-export footprint in the premier US basin
    "fee_based_contracted_revenue_mix_now_investment_grade": (+0.30,  0.16),  # ~90% fee-based/contracted margin + freshly investment-grade across all 3 agencies
    "growth_project_backlog_visibility"                : (+0.25,  0.15),  # Train 12, Daytona ramp, new processing plants — multi-year, largely sanctioned/de-risked
    "capital_return_program_credibility"               : (+0.25,  0.14),  # ~33% guided annual dividend growth through 2027 + buyback authorization, funded by FCF
    "lng_export_and_petrochemical_demand_pull"         : (+0.15,  0.12),  # Structural NGL/condensate export demand growth provides a multi-year volume tailwind
    "valuation_already_reflecting_the_premium_thesis"  : (-0.30,  0.13),  # ~17-19x forward / ~11-12x EV/EBITDA near an all-time high — re-rating largely realized
    "residual_commodity_and_producer_capex_sensitivity": (-0.20,  0.12),  # The remaining ~10% of margin (and producer-activity-driven volumes) keeps real cyclicality
}

SCA_NET  = sum(score * weight for score, weight in SCA_FACTORS.values())
# SCA_NET = 0.35×0.18 + 0.30×0.16 + 0.25×0.15 + 0.25×0.14 + 0.15×0.12 + (-0.30)×0.13 + (-0.20)×0.12
# SCA_NET ≈ 0.063 + 0.048 + 0.0375 + 0.035 + 0.018 - 0.039 - 0.024 = 0.1385

SCA_SCALE = 0.45  # Fixed framework parameter

# ── 6 PROXY SIGNALS ──────────────────────────────────────────────────────────
# Signal   (score 1–4, weight)
# 1=BEAR, 1.5=BEAR+, 2=BASE, 2.5=BASE+, 3=BULL, 3.5=BULL+, 4=XBULL

SIGNALS = {
    # The structural heart of the bull case: TRGP is the most vertically-integrated
    # gathering-processing-fractionation-export franchise in the Permian — record FY2025
    # gas processing volumes, with Permian Midstream gathered volumes well above 6.0 Bcf/d
    # and continued sequential growth as producers keep drilling the highest-return basin
    # in North America regardless of moderate near-term oil-price swings.
    "permian_dominance_and_record_volumes": (3.0, 0.18),

    # A genuinely de-risked, multi-year growth backlog converting on schedule: Train 12
    # fractionator under construction, the Daytona NGL pipeline ramping toward full
    # utilization, and a pipeline of new Permian processing plants (Bull Moose, Wildcat,
    # successors) backed by long-term, largely fee-based/MVC contracts — ~$5B of
    # identified, largely-sanctioned growth capital with clear multi-year EBITDA visibility.
    "growth_backlog_conversion_and_de_risked_capex_program": (3.0, 0.17),

    # The capital-allocation transformation is real and underwritten: the dividend has
    # been raised aggressively for 4 consecutive years (management guiding to ~33% average
    # annual growth through 2027), backed by a freshly-investment-grade balance sheet
    # (BBB-/Baa3/BBB- across all three agencies) and a $1B buyback authorization.
    "capital_return_program_and_investment_grade_balance_sheet": (3.5, 0.17),

    # The honest near-term risk: at ~17-19x forward earnings / ~11-12x EV/EBITDA near an
    # all-time high (up ~45% over the past year), the stock has already re-rated hard from
    # a discounted cyclical-midstream multiple toward a premium infrastructure-compounder
    # one — a meaningful fraction of the next several years' growth already appears priced.
    "valuation_already_reflects_the_re_rating_thesis": (1.5, 0.20),

    # Structural NGL/condensate export demand (Gulf Coast LPG export terminals,
    # petrochemical feedstock growth, and broader LNG-adjacent gas demand) provides a
    # multi-year volume tailwind that is increasingly contract-backed rather than purely
    # spot-commodity-driven — a genuine structural demand pull, not just a Permian story.
    "lng_petrochemical_and_ngl_export_demand_tailwind": (3.0, 0.14),

    # Residual cyclicality: roughly 10% of gross margin remains commodity-price-linked, and
    # producer activity (and therefore gathered volumes) still ultimately depends on the
    # E&P capex cycle — a genuine, if shrinking and increasingly well-hedged, exposure that
    # keeps this from being a pure, all-weather toll-road business.
    "residual_commodity_and_producer_activity_cyclicality": (2.0, 0.14),
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

# Conservative 2yr: FY2026E EPS (consensus, reflecting backlog conversion) × a multiple
# BELOW the current ~21x forward — pure compounding/multiple-normalization test, no
# further heroic re-rating toward "premium infrastructure" multiples required
PE_CONSERVATIVE = 17.0
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
    print(f"  Revenue:           ${REVENUE_FY2025_B:.1f}B  |  Adj. EBITDA: ${ADJ_EBITDA_FY2025_B:.2f}B (record, {ADJ_EBITDA_YOY_PCT:+d}% YoY)")
    print(f"  Net Income:        ${NET_INCOME_FY2025_B:.2f}B  |  Adj. EPS: ${ADJ_EPS_FY2025:.2f}")
    print(f"  Growth capex:      ${GROWTH_CAPEX_FY2025_B:.1f}B (bulk toward de-risked, contracted projects)")
    print(f"  {PERMIAN_VOLUMES_RECORD_NOTE}")

    print(f"\n  FY2026 guidance: Adj. EBITDA ${ADJ_EBITDA_GUIDANCE_LOW_B:.1f}-{ADJ_EBITDA_GUIDANCE_HIGH_B:.1f}B")
    print(f"  {GUIDANCE_NOTE}")

    print(f"\n{sep}")
    print("  GROWTH PROJECT BACKLOG")
    print(sep)
    print(f"  {TRAIN_PROJECTS_NOTE}")
    print(f"  {DAYTONA_PIPELINE_NOTE}")
    print(f"  {PERMIAN_MIDSTREAM_EXPANSION_NOTE}")
    print(f"  Identified growth-capital program: ~${GROWTH_BACKLOG_CAPITAL_B:.1f}B (largely sanctioned / under construction)")

    print(f"\n{sep}")
    print("  CAPITAL ALLOCATION & BALANCE SHEET")
    print(sep)
    print(f"  Dividend: {DIV_CONSECUTIVE_HIKE_YEARS} consecutive years of aggressive increases; guided to ~{DIV_GROWTH_GUIDANCE_PCT}% avg. annual growth through 2027 (yield ~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}%)")
    print(f"  Buyback authorization: ${BUYBACK_AUTHORIZATION_B:.1f}B  |  Net debt/EBITDA ~{NET_DEBT_TO_EBITDA:.1f}x (targeting 3.0-3.5x)")
    print(f"  {CREDIT_RATING_NOTE}")
    print(f"  Fee-based / contracted share of gross margin: ~{FEE_BASED_CONTRACT_MIX_PCT}%")

    print(f"\n{sep}")
    print("  ANALYST CONSENSUS")
    print(sep)
    print(f"  FY2026E EPS: ${EPS_FY2026E:.2f}  |  Trailing P/E ~{TRAILING_PE:.1f}x, Forward P/E ~{FORWARD_PE:.1f}x, EV/EBITDA ~{EV_EBITDA_MULTIPLE:.1f}x")
    print(f"  Rating: {CONSENSUS_RATING}  |  Price targets: consensus ${CONSENSUS_PT:.0f} (range ${PT_LOW:.0f}-${PT_HIGH:.0f})")
    print(f"  {ANALYST_RATING_NOTE}")

    print(f"\n{sep}")
    print("  6 PROXY SIGNALS")
    print(sep)
    labels = {
        "permian_dominance_and_record_volumes":                       "Permian dominance & record processing volumes",
        "growth_backlog_conversion_and_de_risked_capex_program":      "Growth backlog conversion & de-risked capex program",
        "capital_return_program_and_investment_grade_balance_sheet":  "Capital return program & investment-grade balance sheet",
        "valuation_already_reflects_the_re_rating_thesis":            "Valuation already reflects the re-rating thesis",
        "lng_petrochemical_and_ngl_export_demand_tailwind":           "LNG / petrochemical / NGL export demand tailwind",
        "residual_commodity_and_producer_activity_cyclicality":       "Residual commodity & producer-activity cyclicality",
    }
    for k, (score, weight) in SIGNALS.items():
        bar = "█" * int(score * 5)
        print(f"  {labels[k]:<56}  {score:.1f}  wt={weight:.2f}  {bar}")
    print(f"  {'PROXY COMPOSITE':<56}  {PROXY_COMPOSITE:.2f}")

    print(f"\n{sep}")
    print("  SCA — STRUCTURAL COMPETITIVE ADVANTAGE")
    print(sep)
    sca_labels = {
        "permian_vertical_integration_and_scale":                "Permian vertical integration & scale",
        "fee_based_contracted_revenue_mix_now_investment_grade": "Fee-based/contracted mix, now investment grade",
        "growth_project_backlog_visibility":                     "Growth-project backlog visibility",
        "capital_return_program_credibility":                    "Capital-return program credibility",
        "lng_export_and_petrochemical_demand_pull":              "LNG-export & petrochemical demand pull",
        "valuation_already_reflecting_the_premium_thesis":       "Valuation already reflecting the premium thesis",
        "residual_commodity_and_producer_capex_sensitivity":     "Residual commodity & producer-capex sensitivity",
    }
    for k, (score, weight) in SCA_FACTORS.items():
        print(f"  {sca_labels[k]:<56}  {score:+.2f} × {weight:.2f} = {score*weight:+.4f}")
    print(f"  {'SCA_NET':<56}  {SCA_NET:+.4f}")
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
    print(f"  FY2026E EPS (consensus, reflecting backlog conversion):  ${EPS_FY2026E:.2f}")
    print(f"  Conservative PE applied:                                 {PE_CONSERVATIVE:.1f}× (below the ~21x forward — modest multiple normalization)")
    print(f"  Target price 2yr:                                        ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.1f}× + ${2*ANNUAL_DIV:.2f} div = ${PRICE_2YR_CONSV:.2f}")
    print(f"  2-year return:                                           {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  Note: this is the 'multiple normalizes modestly off an all-time high toward a still-premium")
    print(f"  (but less rich) infrastructure multiple' floor case — BULL/XBULL require the backlog to")
    print(f"  convert fast enough, and at high enough returns, to keep outrunning today's rich starting multiple.")

    print(f"\n{sep}")
    print("  WHY THIS IS A ◌ WATCHLIST, NOT A ◎ ACCUMULATE OR ✕ AVOID")
    print(sep)
    print("""
  Targa Resources is, by a wide margin, the most dominant, vertically-integrated
  gathering-processing-fractionation-export franchise in the Permian Basin — the highest-
  growth, lowest-cost basin in North American energy — and it has executed a genuinely
  rare transformation: from a levered, commodity-exposed midstream operator into a
  freshly investment-grade, ~90% fee-based infrastructure compounder with a credible,
  guided multi-year dividend-growth program. This is a great business. The question is
  whether $192 — within ~4% of an all-time high, up ~45% over the past year — is a great
  PRICE for it.

  WHAT THE MARKET ALREADY PRICES IN (at $192.40, near an all-time high):
  • Permian volumes keep setting records at a healthy, continuing pace
  • Train 12, Daytona, and the new processing plants come online roughly on schedule
  • The dividend keeps growing at a strong (if decelerating from the initial 33% guide) clip
  • The investment-grade re-rating is durable and the multiple holds near today's levels

  WHAT COULD MAKE THIS MORE THAN FAIRLY PRICED:
  1. The $5B+ growth backlog converts faster and at better-than-guided returns as Permian
     associated-gas growth and LNG-feedgas-driven demand pull volumes higher than guided
  2. Daytona and the new fractionators ramp to full utilization ahead of schedule, pulling
     forward EBITDA growth that the market currently has spread over several years
  3. The multiple continues to re-rate toward the most-integrated, highest-quality midstream
     peers (mid-teens EV/EBITDA) as the investment-grade transformation gets fully credited
  4. Buybacks accelerate alongside the dividend program as FCF outpaces the growth-capital plan

  THE RISK (the honest read on where this sits):
  • At ~17-19x forward earnings / ~11-12x EV/EBITDA near an all-time high (+45% over the
    past year), TRGP has ALREADY captured most of the "re-rating from cyclical-midstream-
    discount to premium-infrastructure-compounder" trade — this was arguably THE consensus
    midstream trade of the last three years, and consensus trades that have worked leave
    less room for surprise upside from here
  • Roughly 10% of gross margin (and a chunk of volume growth) remains genuinely linked to
    commodity prices and producer capex decisions — a real, if shrinking, cyclical exposure
  • Net debt/EBITDA at ~3.4x is healthy but not pristine — a sharp EBITDA disappointment
    would pressure both the multiple and the leverage ratio simultaneously
  • A broad Permian activity slowdown (oil <$60 sustained) would slow the very volume growth
    that today's premium multiple is underwriting

  WHAT KEEPS THIS FROM BEING AN OUTRIGHT AVOID:
  • The structural transformation is REAL and largely already executed, not promised: ~90%
    fee-based margin, investment-grade ratings across all three agencies, record EBITDA, and
    a $5B+ backlog that is largely sanctioned and under construction — this is not a story
  • The dividend-growth program (4 consecutive years of aggressive hikes, guided ~33%
    average annual growth through 2027) provides a real, growing income floor
  • Even the EPP-floor and conservative-2yr math (a modest multiple normalization off an
    all-time high) still produces a roughly flat-to-modestly-positive total return —
    this is a "good business priced for a good outcome," not a bubble

  POSITION SIZING GUIDANCE:
  • WATCHLIST — track for a better entry rather than chasing the all-time high; a pullback
    toward $155-170 (where Ratio B would move toward ACCUMULATE territory and the multiple
    would better reflect a normal — not best-case — pace of backlog conversion) meaningfully
    improves the asymmetry
  • Watch for: Train 12 / Daytona ramp updates (the biggest near-term EBITDA swing factors),
    confirmation that the dividend-growth program holds near the 33% guide through 2026-27,
    and whether net debt/EBITDA continues trending toward the 3.0x target as EBITDA scales
""")

    print(SEP)
    print(f"""
SUMMARY: TRGP ◌ WATCHLIST — Ratio B 1.35× (29.8% downside / 22.1% upside). THE PERMIAN NGL \
TOLL-ROAD COMPOUNDER NEAR AN ALL-TIME HIGH: trading at $192.40 (52-wk range $130-201, within \
~4% of the high, up ~45% over the past year) on a genuinely dominant, vertically-integrated \
Permian gathering-processing-fractionation-export franchise — record FY2025 Adj. EBITDA \
$5.36B (+14% YoY), Permian Midstream gathered volumes well above 6.0 Bcf/d and still \
climbing. GROWTH BACKLOG LARGELY DE-RISKED: Train 12 fractionator under construction, \
Daytona NGL Pipeline (~600 Mbbl/d) ramping toward full utilization, and a pipeline of new \
Permian processing plants backed by long-term, largely fee-based/MVC contracts (~$5B \
identified growth-capital program). CAPITAL ALLOCATION TRANSFORMATION IS REAL: 4 \
consecutive years of aggressive dividend hikes (guided ~33% average annual growth through \
2027, ~2.4% yield), $1B buyback authorization, and a freshly investment-grade balance sheet \
(BBB-/Baa3/BBB- across all three agencies, ~90% fee-based margin mix). THE HONEST RISK: at \
~17-19x forward / ~11-12x EV/EBITDA near an all-time high, the stock has already captured \
most of the 'cyclical-midstream-discount to premium-infrastructure-compounder' re-rating — \
arguably THE consensus midstream trade of the last three years — leaving less room for \
surprise upside, plus ~10% of margin remains genuinely commodity-linked and net debt/EBITDA \
sits at ~3.4x. Consensus 'Buy/Strong Buy' (~19 of 25 analysts), PT ~$205 (range $165-245). \
Conservative 2yr (modest multiple-normalization floor case): EPS $9.10 x 17x + $9.20 div = \
$163.90 -> -14.8% — BULL/XBULL require the backlog to convert fast enough to keep outrunning \
today's rich starting multiple. A GREAT BUSINESS, BUT THE MARKET ALREADY KNOWS IT — track \
for a pullback toward $155-170 to meaningfully improve the entry. Bear $135 · Base $192 · \
Bull $235 · XBull $270."""
    )

    print(f"SIGNAL: {SIGNAL_TEXT} (dominant, now-investment-grade Permian NGL infrastructure franchise — but trading near an all-time high after capturing most of its re-rating already) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
