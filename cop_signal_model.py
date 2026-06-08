"""
ConocoPhillips (NYSE: COP)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.88×  |  EPP Gap: +261.2%

THE PURE-PLAY E&P TITAN — MARATHON SYNERGIES BEATING, WILLOW HALFWAY BUILT, LOWEST COST OF SUPPLY
Trading at $117 (52-week range $86–136, off a +46% one-year rally) on:
  (1) Marathon Oil integration running far ahead of plan — run-rate synergies DOUBLED to
      >$1B (vs. the original $500M target) plus ~$1B of one-time benefits captured in 2025,
      >2.5 BBOE of resource added (vs. the 2 BBOE deal target), and ~30% fewer rigs/frac
      crews now delivering MORE combined production than the two companies separately
  (2) Willow (Alaska) ~50% complete after a successful winter construction season — the
      single largest new conventional oil project in the US, targeted for ~180 Mbbl/d
  (3) Industry-leading ~$40/bbl cost-of-supply breakeven — the structural cushion that
      lets COP keep returning capital and growing through a cycle that has bears
      warning a drop toward $60/bbl WTI "would eviscerate the investment case"

At $117 the stock trades at ~19.9× trailing earnings — a premium multiple for an E&P
posting only modest (~2.4%/yr) revenue growth, which is exactly why several houses rate
it a "Hold" with price targets trailing the post-rally price. But this read undersells
what changed: COP is no longer a leveraged commodity-cycle trade — it is the lowest-cost,
best-capitalized pure-play E&P in the business, with Marathon synergies still running
ahead of schedule and Willow/LNG project optionality not yet contributing a barrel.

Conviction: MODERATE-HIGH on the base case (Marathon integration completes, Willow comes
online on schedule, capital returns keep compounding at ~45% of operating cash flow);
HIGHER on the structural cost-of-supply advantage that should let COP keep growing
production and cash flow even in a "lower for longer" oil-price world that would
genuinely hurt higher-cost peers.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "COP"
COMPANY         = "ConocoPhillips"
SECTOR          = "Pure-Play Exploration & Production · Lower 48 Unconventional (Permian/Eagle Ford/Bakken) · Alaska (Willow) · LNG (Qatar, Port Arthur) · NYSE: COP"
SECTOR_GROUP    = "Energy"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 117.40   # June 7, 2026
ANNUAL_DIV      = 3.36     # $0.84/quarter ordinary dividend
SHARES_OUT_B    = 1.215    # ~1.215B shares (market cap / price)
MARKET_CAP_B    = 142.7
FW52_HIGH       = 135.87
FW52_LOW        = 85.57
ONE_YEAR_RALLY_PCT = 46    # Stock up ~46% over the trailing year

# ── FY2025 FULL-YEAR FINANCIALS (ESTIMATED FROM QUARTERLY RUN-RATE) ─────────
REVENUE_FY2025_B          = 62.0
ADJ_NET_INCOME_FY2025_B   = 7.5
ADJ_EPS_FY2025            = 6.20
GAAP_NET_INCOME_FY2025_B  = 7.1
GAAP_EPS_FY2025           = 5.85
FCF_FY2025_B              = 9.5
OCF_FY2025_B              = 21.0
TTM_PE                    = 19.9   # Trailing P/E — a premium multiple bears flag vs. ~2.4%/yr revenue growth

# ── Q1 2026 SNAPSHOT (vs. Q1 2025) ───────────────────────────────────────────
Q1_REVENUE_B            = 15.76    # vs $16.52B Q1'25
Q1_GAAP_NET_INCOME_B    = 2.2
Q1_GAAP_EPS             = 1.78     # vs $2.23 Q1'25
Q1_ADJ_NET_INCOME_B     = 2.3
Q1_ADJ_EPS              = 1.89     # Beat consensus $1.66; vs $2.09 Q1'25
Q1_OCF_B                = 5.4
Q1_FCF_B                = 2.4
Q1_YOY_DRIVER_NOTE      = "YoY decline driven by lower realized commodity prices + Qatar/Mideast-conflict-related downtime — not a structural deterioration"

# ── DIVIDEND & CAPITAL RETURNS ───────────────────────────────────────────────
QUARTERLY_DIV               = 0.84
RETURN_OF_CFO_TARGET_PCT    = 45    # 2026 target: return ~45% of cash from operations to shareholders
Q1_2026_TOTAL_RETURNS_B     = 2.0
Q1_2026_BUYBACK_B           = 1.0
Q1_2026_DIV_B               = 1.0

# ── BALANCE SHEET (as of 3/31/2026) ──────────────────────────────────────────
TOTAL_DEBT_B            = 23.3     # $1.07B short-term + $22.26B long-term
CASH_B                  = 5.9
NET_DEBT_B              = 17.5
TOTAL_ASSETS_B          = 122.7
CREDIT_RATING_NOTE      = "Investment-grade (A-tier) — among the strongest balance sheets of any pure-play E&P"

# ── PRODUCTION (Q1 2026 / FY2025 / 2026 GUIDANCE) ───────────────────────────
TOTAL_PRODUCTION_FY2025_MBOED = 2375   # In line with guidance
TOTAL_PRODUCTION_Q1_2026_MBOED = 2309
PRODUCTION_GUIDANCE_2026_LOW_MMBOED  = 2.33
PRODUCTION_GUIDANCE_2026_HIGH_MMBOED = 2.36
LOWER48_MBOED           = 1453
DELAWARE_MBOED          = 698
MIDLAND_MBOED           = 200
EAGLE_FORD_MBOED        = 367
BAKKEN_MBOED            = 183

# ── WILLOW (ALASKA) & LNG PORTFOLIO ──────────────────────────────────────────
WILLOW_PCT_COMPLETE     = 50       # ~50% complete after a successful winter construction season
WILLOW_TARGET_MBBLD     = 180      # Targeted peak production — largest new conventional US oil project
LNG_PORTFOLIO_NOTE      = "Equity stakes advancing in Qatar (NFE / North Field South expansion) and Port Arthur LNG (US Gulf Coast)"
QATAR_DISRUPTION_NOTE   = "Qatar operations hit by Middle East-conflict-related downtime in Q1 2026 — geopolitical, not structural"

# ── MARATHON OIL INTEGRATION (CLOSED NOVEMBER 2024) ──────────────────────────
DEAL_CLOSE                  = "November 2024"
SYNERGY_TARGET_ORIGINAL_M   = 500
SYNERGY_REALIZED_RUNRATE_M  = 1000   # DOUBLED vs. original target — captured in 2025
ONE_TIME_BENEFIT_B          = 1.0
RESOURCE_TARGET_BBOE        = 2.0
RESOURCE_ADDED_BBOE         = 2.5    # Beat the deal's own resource target
RIG_FRAC_CREW_REDUCTION_PCT = 30     # ~30% fewer rigs/frac crews delivering MORE combined production
ADDITIONAL_2026_SYNERGY_TARGET_B = 1.0  # Incremental run-rate cost reduction/margin enhancement target by YE2026
INTEGRATION_FOCUS_NOTE      = "Integration largely complete; 2026 focus shifting to non-core asset pruning + high-return barrel concentration"

# ── CAPITAL DISCIPLINE ────────────────────────────────────────────────────────
CAPEX_2026_B            = 12.0
ADJ_OPERATING_COSTS_2026_B = 10.2
COST_OF_SUPPLY_BREAKEVEN_BBL = 40   # Industry-leading — the structural cushion through the cycle

# ── ANALYST CONSENSUS ────────────────────────────────────────────────────────
EPS_FY2026E             = 6.20     # Roughly flat vs FY2025 — softer realized prices offset by Marathon synergies + production growth
CONSENSUS_PT            = 141.0    # S&P Global poll of 27 analysts: avg $142.88; other aggregates ~$140
PT_BEAR_CASE            = 104.93
PT_RATING_SPLIT         = "20 buy / 2 sell (of 27 analysts)"
ANALYST_NOTE            = "Some houses rate 'Hold' — price target trailing the price after a +46% one-year rally; bulls cite Marathon execution + cost-of-supply edge"

# ── 2020 COVID TROUGH (HISTORICAL ANCHOR) ───────────────────────────────────
COVID_LOW_PRICE         = 22.67    # March 18, 2020 — fell ~66% from the Jan 2020 high of $66.48 (WTI briefly went negative)
COVID_LOW_DATE          = "March 18, 2020"
PRICE_VS_TROUGH_MULTIPLE = CURRENT_PRICE / COVID_LOW_PRICE   # ≈ 5.2×

# ── SCENARIOS ────────────────────────────────────────────────────────────────
# BEAR  $80:  Oil price breaks down toward $60/bbl WTI (OPEC+ share war, demand-shock
#             recession) — bears explicitly warn this level "would eviscerate the
#             investment case" for premium-multiple E&Ps. Even COP's $40/bbl cost-of-
#             supply cushion compresses margins sharply; the ~19.9× multiple de-rates
#             toward 11-12× on a falling-EPS base; buybacks slow as discretionary FCF
#             shrinks. Roughly the lower portion of the 52-week range — NOT a 2020-style
#             solvency event (net debt only $17.5B against $122.7B of assets).
#
# BASE  $135: Oil holds in a constructive $65-75/bbl range; Marathon integration
#             completes on schedule with synergies sustained near the doubled $1B
#             run-rate; production grows toward the top of 2026 guidance (2.36 MMboe/d);
#             capital returns continue at ~45% of CFO; Willow construction proceeds on
#             budget. Roughly the top of the current 52-week range / consensus PT zone.
#
# BULL  $160: Marathon synergies beat AGAIN (as the doubled-target pattern suggests they
#             might) with the additional >$1B 2026 target achieved; Willow crosses 75%+
#             complete with a credible 2027-28 first-oil line of sight; Qatar/Port Arthur
#             LNG capacity additions begin contributing; oil holds $75-85 on continued
#             underinvestment in new global supply; multiple re-rates toward 16-17× on
#             de-risked, lower-cost growth visibility (vs. ~20× priced for modest growth today).
#
# XBULL $190: Full "lowest-cost E&P compounder" thesis — Willow comes online ahead of
#             schedule near its 180 Mbbl/d target, LNG equity volumes ramp meaningfully,
#             Marathon integration unlocks even more than the 2.5 BBOE already added, AND
#             a genuine oil supercycle (structural underinvestment + geopolitical supply
#             shocks) pushes WTI toward $90-100+. Requires multiple structural tailwinds
#             to align — the highest-conviction, lowest-probability outcome.
BEAR    = 80.0
BASE    = 135.0
BULL    = 160.0
XBULL   = 190.0

# ── EPP (EARNINGS POWER PRICE) ───────────────────────────────────────────────
# Trough scenario: a severe commodity downcycle (2020-COVID-style demand collapse, when
# WTI briefly went negative and COP fell to $22.67) drags adjusted EPS down sharply even
# for the lowest-cost pure-play E&P. Trough PE reflects how E&Ps re-rate in deep cyclical
# troughs — typically 11-14× on a depressed earnings base, with COP earning a modest
# premium for its industry-leading $40/bbl cost-of-supply cushion and IG balance sheet.
EPS_TROUGH  = 2.50
PE_TROUGH   = 13.0
EPP         = EPS_TROUGH * PE_TROUGH   # = $32.50

# ── SCA: STRUCTURAL COMPETITIVE ADVANTAGE ───────────────────────────────────
# COP's moat is its position as the lowest-cost, best-diversified pure-play E&P — a
# globally diversified Lower 48 + Alaska + LNG portfolio with an industry-leading
# ~$40/bbl cost-of-supply, now turbocharged by a Marathon integration running well
# ahead of plan. The structural offset is that — unlike integrated majors — COP has
# no downstream/chemicals cushion: it is a leveraged, undiluted bet on the commodity.

SCA_FACTORS = {
    # Factor                              : (score,  weight)
    "lowest_cost_of_supply_in_industry"   : (+0.30,  0.16),  # ~$40/bbl breakeven — industry-leading structural cushion
    "marathon_integration_execution"      : (+0.35,  0.18),  # Synergies doubled vs. target; resource added beat target; fewer rigs, more output
    "diversified_lower48_plus_growth_optionality" : (+0.25, 0.15),  # Permian/Eagle Ford/Bakken + Willow + LNG — multiple growth vectors, not one basin
    "investment_grade_balance_sheet"      : (+0.20,  0.15),  # Net debt $17.5B vs $122.7B assets — IG ratings, real but not "fortress" like XOM
    "capital_return_discipline"           : (+0.20,  0.13),  # ~45% of CFO returned; programmatic buybacks + ordinary dividend
    "pure_play_commodity_leverage"        : (-0.30,  0.12),  # No downstream/chemicals cushion — undiluted, leveraged bet on the oil price
    "premium_multiple_modest_growth_risk" : (-0.20,  0.11),  # ~19.9x trailing P/E for ~2.4%/yr revenue growth — re-rating risk if growth disappoints
}

SCA_NET  = sum(score * weight for score, weight in SCA_FACTORS.values())
# SCA_NET = 0.30×0.16 + 0.35×0.18 + 0.25×0.15 + 0.20×0.15 + 0.20×0.13 + (-0.30)×0.12 + (-0.20)×0.11
# SCA_NET ≈ 0.048 + 0.063 + 0.0375 + 0.030 + 0.026 - 0.036 - 0.022 = 0.1465 → (+0.152 incl. rounding)

SCA_SCALE = 0.45  # Fixed framework parameter

# ── 6 PROXY SIGNALS ──────────────────────────────────────────────────────────
# Signal   (score 1–4, weight)
# 1=BEAR, 1.5=BEAR+, 2=BASE, 2.5=BASE+, 3=BULL, 3.5=BULL+, 4=XBULL

SIGNALS = {
    # FY2025 production landed in line with guidance at 2,375 Mboe/d (Q1 2026: 2,309
    # Mboe/d), with 2026 guided to 2.33-2.36 MMboe/d. Lower 48 unconventional (Delaware
    # 698, Eagle Ford 367, Bakken 183, Midland 200 Mboe/d) provides a diversified base
    # that is genuinely growing — not a depleting legacy E&P treading water.
    "production_growth_diversified_base": (3.0, 0.18),

    # THE standout execution story. Run-rate synergies DOUBLED to >$1B (vs. the original
    # $500M target) plus ~$1B of one-time benefits captured in 2025; resource added
    # >2.5 BBOE (vs. the 2 BBOE deal target); ~30% fewer rigs/frac crews now delivering
    # MORE combined production. An additional >$1B incremental target is guided for 2026.
    # This is the "beat-and-raise" pattern that should keep compounding the cost advantage.
    "marathon_oil_synergy_realization": (3.5, 0.20),

    # Disciplined, programmatic capital returns: ~45% of operating cash flow targeted
    # for distribution, $2.0B returned in Q1 2026 alone ($1.0B buybacks + $1.0B ordinary
    # dividend), at a $0.84/qtr ($3.36/yr, ~2.9% yield) payout. A durable, formula-driven
    # mechanism — not a discretionary "good year only" program.
    "capital_return_discipline": (3.0, 0.16),

    # The honest bear case, in the bears' own words: a drop toward $60/bbl WTI "would
    # eviscerate the investment case" for a stock trading at ~19.9× trailing earnings —
    # a premium multiple for only ~2.4%/yr revenue growth. Q1 2026 already showed the
    # YoY earnings compression that comes with softer realized prices (EPS $1.89 adj.
    # vs $2.09 a year ago) — a preview of what a real downturn would do to the print.
    "oil_price_and_premium_multiple_risk": (2.0, 0.18),

    # Genuinely investment-grade: net debt of just $17.5B against $122.7B of total
    # assets, with $5.9B of cash on hand. Not the AA-/Aa2 "fortress" of an integrated
    # major (no downstream cushion), but a real structural advantage that — combined
    # with the ~$40/bbl cost-of-supply — lets COP keep returning capital and investing
    # in growth (Willow, LNG) through commodity cycles that would stress higher-cost peers.
    "investment_grade_balance_sheet_cost_cushion": (3.0, 0.14),

    # Willow (Alaska) is ~50% complete after a successful winter construction season —
    # the largest new conventional US oil project, targeted at ~180 Mbbl/d — alongside
    # equity LNG stakes advancing in Qatar (NFE/North Field South) and Port Arthur. Q1
    # 2026 Qatar volumes were hit by Middle East-conflict-related downtime — a real but
    # geopolitical (not structural) drag that masks the underlying growth optionality.
    "willow_and_lng_growth_optionality": (2.5, 0.14),
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

# Conservative 2yr: EPS FY2026E (roughly flat vs FY2025) × modest PE + 2yr dividends
# (no heroic multiple expansion — pure compounding test, deliberately ignoring the
# ~19.9x multiple the market currently assigns)
PE_CONSERVATIVE = 17.5
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
    print("  FY2025 FINANCIALS (estimated from quarterly run-rate)")
    print(sep)
    print(f"  Revenue:           ${REVENUE_FY2025_B:.1f}B")
    print(f"  Adj. Net Income:   ${ADJ_NET_INCOME_FY2025_B:.1f}B  (${ADJ_EPS_FY2025:.2f}/sh)")
    print(f"  GAAP Net Income:   ${GAAP_NET_INCOME_FY2025_B:.1f}B  (${GAAP_EPS_FY2025:.2f}/sh)")
    print(f"  FCF: ${FCF_FY2025_B:.1f}B   |   OCF: ${OCF_FY2025_B:.1f}B   |   Trailing P/E: {TTM_PE:.1f}× (premium multiple bears flag vs ~2.4%/yr revenue growth)")

    print(f"\n  Q1 2026 vs Q1 2025:")
    print(f"    Revenue ${Q1_REVENUE_B:.2f}B (vs $16.52B)  |  GAAP EPS ${Q1_GAAP_EPS:.2f} (vs $2.23)  |  Adj. EPS ${Q1_ADJ_EPS:.2f} (beat consensus $1.66; vs $2.09)")
    print(f"    OCF ${Q1_OCF_B:.1f}B  |  FCF ${Q1_FCF_B:.1f}B")
    print(f"    {Q1_YOY_DRIVER_NOTE}")

    print(f"\n{sep}")
    print("  BALANCE SHEET")
    print(sep)
    print(f"  Total Debt: ${TOTAL_DEBT_B:.1f}B  |  Cash: ${CASH_B:.1f}B  |  Net Debt: ${NET_DEBT_B:.1f}B  |  Total Assets: ${TOTAL_ASSETS_B:.1f}B")
    print(f"  {CREDIT_RATING_NOTE}")
    print(f"  2020 COVID stress test: stock fell to ${COVID_LOW_PRICE:.2f} ({COVID_LOW_DATE}) as WTI briefly went negative —")
    print(f"    today's price is ~{PRICE_VS_TROUGH_MULTIPLE:.1f}× that trough on a vastly larger, lower-cost, higher-FCF company.")

    print(f"\n{sep}")
    print("  CAPITAL RETURNS")
    print(sep)
    print(f"  Dividend: ${QUARTERLY_DIV:.2f}/qtr (${ANNUAL_DIV:.2f}/yr) — yield ~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}%")
    print(f"  2026 target: return ~{RETURN_OF_CFO_TARGET_PCT}% of cash from operations to shareholders")
    print(f"  Q1 2026: ${Q1_2026_TOTAL_RETURNS_B:.1f}B total returned (${Q1_2026_BUYBACK_B:.1f}B buybacks + ${Q1_2026_DIV_B:.1f}B ordinary dividend)")

    print(f"\n{sep}")
    print("  PRODUCTION — DIVERSIFIED LOWER 48 + ALASKA + LNG")
    print(sep)
    print(f"  FY2025: {TOTAL_PRODUCTION_FY2025_MBOED:,} Mboe/d (in line with guidance)  |  Q1 2026: {TOTAL_PRODUCTION_Q1_2026_MBOED:,} Mboe/d")
    print(f"  2026 guidance: {PRODUCTION_GUIDANCE_2026_LOW_MMBOED:.2f}-{PRODUCTION_GUIDANCE_2026_HIGH_MMBOED:.2f} MMboe/d")
    print(f"  Lower 48 ({LOWER48_MBOED:,} Mboe/d):  Delaware {DELAWARE_MBOED} | Eagle Ford {EAGLE_FORD_MBOED} | Bakken {BAKKEN_MBOED} | Midland {MIDLAND_MBOED}  (Mboe/d)")

    print(f"\n{sep}")
    print("  GROWTH OPTIONALITY — WILLOW (ALASKA) & LNG")
    print(sep)
    print(f"  Willow: ~{WILLOW_PCT_COMPLETE}% complete (successful winter construction season)  →  targeted ~{WILLOW_TARGET_MBBLD} Mbbl/d — largest new conventional US oil project")
    print(f"  LNG: {LNG_PORTFOLIO_NOTE}")
    print(f"       {QATAR_DISRUPTION_NOTE}")

    print(f"\n{sep}")
    print("  MARATHON OIL INTEGRATION — RUNNING AHEAD OF PLAN")
    print(sep)
    print(f"  Deal closed {DEAL_CLOSE}")
    print(f"  Synergies: ${SYNERGY_REALIZED_RUNRATE_M}mm run-rate realized — DOUBLED vs ${SYNERGY_TARGET_ORIGINAL_M}mm original target, plus ~${ONE_TIME_BENEFIT_B:.1f}B one-time benefits in 2025")
    print(f"  Resource added: {RESOURCE_ADDED_BBOE:.1f} BBOE (vs {RESOURCE_TARGET_BBOE:.1f} BBOE deal target)  |  ~{RIG_FRAC_CREW_REDUCTION_PCT}% fewer rigs/frac crews delivering MORE combined output")
    print(f"  2026: additional >${ADDITIONAL_2026_SYNERGY_TARGET_B:.1f}B incremental run-rate target  |  {INTEGRATION_FOCUS_NOTE}")

    print(f"\n{sep}")
    print("  CAPITAL DISCIPLINE")
    print(sep)
    print(f"  2026 capex: ${CAPEX_2026_B:.1f}B  |  Adj. operating costs: ${ADJ_OPERATING_COSTS_2026_B:.1f}B")
    print(f"  Cost-of-supply breakeven: ~${COST_OF_SUPPLY_BREAKEVEN_BBL}/bbl — industry-leading structural cushion through the cycle")

    print(f"\n{sep}")
    print("  ANALYST CONSENSUS")
    print(sep)
    print(f"  FY2026E EPS: ${EPS_FY2026E:.2f}  |  Rating split: {PT_RATING_SPLIT}")
    print(f"  Price targets: consensus ${CONSENSUS_PT:.2f}  |  bear-case target ${PT_BEAR_CASE:.2f}")
    print(f"  {ANALYST_NOTE}")

    print(f"\n{sep}")
    print("  6 PROXY SIGNALS")
    print(sep)
    labels = {
        "production_growth_diversified_base":           "Production growth / diversified base",
        "marathon_oil_synergy_realization":             "Marathon Oil synergy realization",
        "capital_return_discipline":                    "Capital return discipline",
        "oil_price_and_premium_multiple_risk":          "Oil price & premium multiple risk",
        "investment_grade_balance_sheet_cost_cushion":  "IG balance sheet / cost-of-supply cushion",
        "willow_and_lng_growth_optionality":            "Willow & LNG growth optionality",
    }
    for k, (score, weight) in SIGNALS.items():
        bar = "█" * int(score * 5)
        print(f"  {labels[k]:<44}  {score:.1f}  wt={weight:.2f}  {bar}")
    print(f"  {'PROXY COMPOSITE':<44}  {PROXY_COMPOSITE:.2f}")

    print(f"\n{sep}")
    print("  SCA — STRUCTURAL COMPETITIVE ADVANTAGE")
    print(sep)
    sca_labels = {
        "lowest_cost_of_supply_in_industry":            "Lowest cost-of-supply in industry (~$40/bbl)",
        "marathon_integration_execution":               "Marathon integration execution",
        "diversified_lower48_plus_growth_optionality":  "Diversified Lower 48 + growth optionality",
        "investment_grade_balance_sheet":               "Investment-grade balance sheet",
        "capital_return_discipline":                    "Capital return discipline (programmatic)",
        "pure_play_commodity_leverage":                 "Pure-play commodity leverage (no downstream)",
        "premium_multiple_modest_growth_risk":          "Premium multiple / modest growth risk",
    }
    for k, (score, weight) in SCA_FACTORS.items():
        print(f"  {sca_labels[k]:<44}  {score:+.2f} × {weight:.2f} = {score*weight:+.4f}")
    print(f"  {'SCA_NET':<44}  {SCA_NET:+.4f}")
    print(f"  ADJ contribution (+0.45 × SCA_NET × 0.5): {SCA_SCALE * SCA_NET * 0.5:+.4f}")

    print(f"\n{sep}")
    print("  COMPOSITE SCORES")
    print(sep)
    print(f"  PROXY_COMPOSITE:    {PROXY_COMPOSITE:.4f}")
    print(f"  ADJ_COMPOSITE:      {ADJ_COMPOSITE:.4f}")
    print(f"  MARKET_COMPOSITE:   {MARKET_COMPOSITE:.4f}  (back-solved from ${CURRENT_PRICE}×1.15²=${TARGET_MARKET:.2f})")
    print(f"  ADJ_VS_MARKET:      {ADJ_VS_MARKET:+.4f}  → {'SIGNIFICANTLY UNDERVALUED' if ADJ_VS_MARKET > 0.5 else 'MODESTLY UNDERVALUED' if ADJ_VS_MARKET > 0.1 else 'FAIRLY VALUED'}")

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
    print(f"  FY2026E EPS (roughly flat vs FY2025):  ${EPS_FY2026E:.2f}")
    print(f"  Conservative PE applied:               {PE_CONSERVATIVE:.1f}× (below the current ~{TTM_PE:.1f}× trailing multiple — deliberately ignoring today's premium)")
    print(f"  Target price 2yr:                      ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.1f}× + ${2*ANNUAL_DIV:.2f} div = ${PRICE_2YR_CONSV:.2f}")
    print(f"  2-year return:                         {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  Note: this is the 'multiple normalizes toward peer levels' floor case — BASE/BULL assume the market keeps")
    print(f"  crediting COP's structural cost-of-supply edge AND Marathon/Willow/LNG growth ramps materialize on schedule.")

    print(f"\n{sep}")
    print("  WHY THIS IS AN ◎ ACCUMULATE, NOT A ◉ BUY OR ✕ AVOID")
    print(sep)
    print("""
  ConocoPhillips is the lowest-cost, best-executing pure-play E&P in the business —
  trading off a +46% one-year rally at a premium ~19.9× trailing multiple that some
  houses already flag as a "Hold." This is NOT a deep-value dislocation; it is a
  high-quality compounder that has re-rated and now needs to grow into its multiple.

  WHAT THE MARKET ALREADY PRICES IN (at $117, well off the 52-week low):
  • Marathon integration completes smoothly with synergies sustained near the doubled
    $1B run-rate (no further beats required to hold the current multiple)
  • Production grows toward the top of 2026 guidance (2.36 MMboe/d) on a steady cadence
  • Capital returns continue at ~45% of CFO — dividend + buybacks compounding as guided
  • Willow and LNG remain "under construction" stories — not yet contributing barrels

  WHAT COULD MAKE THIS MORE THAN FAIRLY PRICED:
  1. Marathon synergies beat AGAIN — the pattern so far (target doubled, resource target
     beaten, 30% fewer rigs delivering more output) suggests management under-promises
  2. Willow crosses the halfway mark toward a credible 2027-28 first-oil timeline,
     and the market starts crediting ~180 Mbbl/d of NEW production not in today's base
  3. Qatar/Port Arthur LNG equity volumes begin ramping — diversifying COP's currently
     100%-oil-and-gas-price-exposed cash flow toward contracted, fee-like LNG economics
  4. The ~$40/bbl cost-of-supply edge widens COP's relative advantage if a "lower for
     longer" oil environment forces higher-cost peers to cut capex and production

  THE RISK (in the bears' own words):
  • A drop toward $60/bbl WTI "would eviscerate the investment case" — COP remains a
    pure-play, undiluted bet on the commodity with NO downstream/chemicals cushion
  • At ~19.9× trailing earnings for ~2.4%/yr revenue growth, the multiple has very
    little room for disappointment — a premium-multiple E&P is a crowded, contested trade
  • Q1 2026 already showed the YoY compression a softer-price environment produces
    (adj. EPS $1.89 vs $2.09 a year ago) — a preview, not yet a crisis
  • Geopolitical exposure is real and immediate: Qatar volumes were ALREADY hit by
    Middle East-conflict-related downtime in Q1 2026

  WHAT MAKES THE DOWNSIDE GENUINELY MANAGEABLE (why this isn't a coin-flip):
  • Net debt of just $17.5B against $122.7B of assets and an investment-grade balance
    sheet — even in a real downturn this is a multiple-compression event, not a
    solvency event (today's price is already ~5.2× the 2020 COVID trough of $22.67,
    on a vastly larger, lower-cost, higher-FCF company than existed back then)
  • The ~$40/bbl cost-of-supply means COP keeps generating real free cash flow at
    price levels that would force higher-cost peers into survival mode

  POSITION SIZING GUIDANCE:
  • This is a "own the best-executing pure-play E&P and let Marathon/Willow/LNG compound"
    name — appropriate as a core energy holding, sized for genuine commodity-price beta
  • Add on weakness toward $95-105 (where Ratio B moves toward BUY territory and the
    ~19.9× multiple compresses to a level that prices in real margin of safety)
  • Willow's path to first oil (2027-28) is the catalyst that should re-rate this from
    "premium-multiple Hold debate" to "structurally growing low-cost compounder"
""")

    print(SEP)
    print(f"""
SUMMARY: COP ◎ ACCUMULATE — Ratio B 0.88× (31.9% downside / 36.3% upside). PURE-PLAY E&P \
TITAN OFF A +46% RALLY: trading at $117 (52-wk range $86-136) at a premium ~19.9x trailing \
P/E that some houses already flag as a 'Hold' — this is a high-quality compounder that has \
re-rated and now needs to grow into its multiple, not a deep-value dislocation. MARATHON \
INTEGRATION RUNNING AHEAD OF PLAN: run-rate synergies DOUBLED to >$1B (vs $500mm original \
target) plus ~$1B one-time benefits in 2025; resource added 2.5 BBOE (beat the 2.0 BBOE deal \
target); ~30% fewer rigs/frac crews delivering MORE combined output; additional >$1B \
incremental target guided for 2026. GROWTH OPTIONALITY NOT YET IN THE PRICE: Willow (Alaska) \
~50% complete (targeting ~180 Mbbl/d — largest new conventional US oil project) plus equity \
LNG stakes ramping in Qatar/Port Arthur. FY2025: revenue $62B, adj. net income $7.5B \
($6.20/sh), FCF $9.5B. INDUSTRY-LEADING COST CUSHION: ~$40/bbl cost-of-supply breakeven; IG \
balance sheet (net debt $17.5B vs $122.7B assets) — current price ~5.2x the 2020 COVID trough \
($22.67) on a vastly larger, lower-cost, higher-FCF company. Capital returns: ~45% of CFO \
targeted, $2.0B returned in Q1 2026 ($1.0B buybacks + $1.0B dividend, ~2.9% yield). Consensus \
PT $141 (20 buy / 2 sell of 27 analysts; bear-case target $104.93). Conservative 2yr (multiple- \
normalization floor case): EPS $6.20 x 17.5x + $6.72 div = $115.92 -> -1.3% — BASE/BULL diverge \
as Marathon/Willow/LNG growth materializes. KEY RISK: bears warn $60/bbl WTI 'would eviscerate \
the investment case' for a pure-play, undiluted commodity bet with no downstream cushion. Add \
on weakness toward $95-105. Bear $80 · Base $135 · Bull $160 · XBull $190.
""")

    print(f"SIGNAL: {SIGNAL_TEXT} (lowest-cost pure-play E&P, Marathon synergies beating, Willow/LNG optionality not priced) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
