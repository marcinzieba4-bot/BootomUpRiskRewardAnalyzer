"""
Kinder Morgan, Inc. (NYSE: KMI)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◎ ACCUMULATE  |  Ratio B: 1.06×  |  EPP Gap: +201.9%

THE NATURAL-GAS TOLL ROAD AT THE FRONT EDGE OF A STRUCTURAL DEMAND INFLECTION
Trading at $31.70 (52-week range $25.60–34.81, roughly 70% up the range) on:
  (1) A genuinely new, structural demand driver showing up in the backlog: ~70% of
      future U.S. data-center power demand under development sits in states KMI serves,
      and management is "in various stages of development" on projects that could serve
      >10 Bcf/d of incremental gas demand from power generation alone — a multi-decade
      tailwind that didn't exist in the company's plan even three years ago
  (2) LNG feedgas exposure scaling fast: 8 Bcf/d contracted today, growing to 12 Bcf/d
      by end-2028, against an industry backdrop where total U.S. LNG feedgas demand is
      projected to roughly double from ~19.8 Bcf/d (2026) to >34 Bcf/d by 2030 — KMI
      sits astride one of the most durable secular growth curves in North American energy
  (3) A $10.1B project backlog (up from $9.3B a year ago) that is ~92% natural gas and
      ~60% tied to power-generation/LDC demand — overwhelmingly fee-based / take-or-pay,
      the "toll road" model that generates highly visible, contracted cash flows largely
      insulated from commodity price swings

At $31.70 — roughly 70% up its 52-week range and not far from its all-time highs — KMI
is no longer a deep-value name; it is a structurally advantaged "own the pipes that the
AI/data-center buildout needs" compounder trading at a fair-to-full price. The honest
counterweight: leverage is drifting UP (3.6x → guided 3.8x net debt/EBITDA by YE2026) as
growth capex ramps to fund that $10.1B backlog, and the multiple (~23x forward earnings)
leaves less room for disappointment than it did at the 2024 lows. Ratio B sits just inside
ACCUMULATE territory — the downside is genuinely cushioned by contracted, fee-based cash
flows and a newly-upgraded investment-grade balance sheet (Baa1/BBB+), while the upside
(data-center gas demand + LNG feedgas growth + backlog conversion) is real, underwritten
by signed contracts, and arguably still under-appreciated relative to its multi-decade length.

Conviction: MODERATE-HIGH on the base case (steady toll-road compounding via dividend
growth + backlog conversion into EBITDA); HIGHER on the structural re-rating case if the
data-center/LNG demand inflection proves as durable and large as management's own pipeline
of opportunities (>10 Bcf/d) suggests — a thesis that is increasingly underwritten by
signed, long-term, fee-based contracts rather than narrative.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "KMI"
COMPANY         = "Kinder Morgan, Inc."
SECTOR          = "Midstream Energy · Natural Gas Pipelines & Storage · LNG Feedgas · Power-Generation Demand Infrastructure · NYSE: KMI"
SECTOR_GROUP    = "Energy"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 31.70    # Early June 2026
ANNUAL_DIV      = 1.19     # 2026 declared dividend (+2% vs 2025; 9th straight annual increase)
SHARES_OUT_B    = 2.22     # ~2.22B shares outstanding
MARKET_CAP_B    = 70.4     # CURRENT_PRICE × SHARES_OUT_B
FW52_HIGH       = 34.81
FW52_LOW        = 25.60

# ── FY2025 FULL-YEAR FINANCIALS ─────────────────────────────────────────────
REVENUE_FY2025_B          = 16.9    # +12.2% YoY
ADJ_EBITDA_FY2025_B       = 8.4
ADJ_EPS_FY2025_GROWTH_PCT = 13      # Adjusted EPS +13% YoY
NET_INCOME_GROWTH_PCT     = 17      # Net income to KMI +17% YoY
REPORTED_DILUTED_EPS      = 1.37

# ── Q1 2026 SNAPSHOT ─────────────────────────────────────────────────────────
Q1_ADJ_EBITDA_M           = 2539    # +18% YoY
Q1_ADJ_EPS                = 0.48    # +41% YoY
Q1_NET_INCOME_M           = 1063    # +39% YoY

# ── FY2026 GUIDANCE ──────────────────────────────────────────────────────────
ADJ_EBITDA_GUIDANCE_FY2026_B = 8.6   # +2.5% YoY
ADJ_EPS_GUIDANCE_FY2026      = 1.36  # +5% YoY
ADJ_NET_INCOME_GROWTH_GUIDE_PCT = 5

# ── BALANCE SHEET / CREDIT ───────────────────────────────────────────────────
NET_DEBT_B                = 31.8
NET_DEBT_TO_EBITDA        = 3.6     # Q1 2026; budgeted to drift to ~3.8x by YE2026 as growth capex ramps
NET_DEBT_TO_EBITDA_GUIDE  = 3.8
CREDIT_RATING_NOTE        = "Upgraded by Moody's to Baa1 — now equivalent to BBB+ at all three major agencies"

# ── PROJECT BACKLOG ──────────────────────────────────────────────────────────
BACKLOG_B                 = 10.1    # End-Q1 2026, up $145mm from Q4 2025 (was $9.3B a year prior)
BACKLOG_NATGAS_PCT        = 92      # ~92% natural-gas projects
BACKLOG_POWERGEN_LDC_PCT  = 60      # ~60% tied to power-generation / LDC demand growth

# ── DATA CENTER / POWER DEMAND TAILWIND ──────────────────────────────────────
DATA_CENTER_DEMAND_SHARE_PCT = 70   # ~70% of future US data-center power demand under dev. sits in states KMI serves
INCREMENTAL_GAS_DEMAND_POTENTIAL_BCFD = 10  # Projects in development could serve >10 Bcf/d of incremental gas demand from power gen

# ── LNG FEEDGAS EXPOSURE ─────────────────────────────────────────────────────
LNG_FEEDGAS_CONTRACTED_TODAY_BCFD = 8
LNG_FEEDGAS_CONTRACTED_2028_BCFD  = 12
US_LNG_FEEDGAS_DEMAND_2026_BCFD   = 19.8   # +19% YoY — record level
US_LNG_FEEDGAS_DEMAND_2030_BCFD   = 34.0   # Roughly doubling industry-wide by 2030

# ── BUSINESS MODEL ───────────────────────────────────────────────────────────
BUSINESS_MODEL_NOTE = "Overwhelmingly fee-based / take-or-pay — the 'natural-gas toll road' — minimal direct commodity price exposure"

# ── ANALYST CONSENSUS ────────────────────────────────────────────────────────
EPS_FY2026E             = 1.36     # Management's own budgeted adjusted EPS guidance
FORWARD_PE_IMPLIED      = 23.3     # Implied at $31.70 / $1.36
CONSENSUS_PT            = 35.0
PT_LOW                  = 26.0
PT_HIGH                 = 43.0
CONSENSUS_RATING        = "Buy (mixed)"
ANALYST_RATING_NOTE     = "Roughly 12 Buy / 10 Hold / 1 Sell; consensus/median PT ~$35 (range $26-43, S&P Global avg $35.33 across 23 analysts)"

# ── SCENARIOS ────────────────────────────────────────────────────────────────
# BEAR  $24: Natural gas demand growth disappoints (data-center buildout slows or
#            relocates, LNG export project delays push feedgas contracting later than
#            guided); leverage overshoots the 3.8x guide as growth capex outpaces EBITDA
#            delivery, pressuring the credit profile and capping multiple expansion;
#            multiple compresses from ~23x toward 16-17x on a "growth story stalls"
#            re-rate. Roughly the 52-week-low zone ($25.60) — even here, the fee-based/
#            take-or-pay contract base (BBB+/Baa1) keeps the dividend intact; this
#            remains a multiple/sentiment correction, not a cash-flow crisis.
#
# BASE  $33: Backlog converts on schedule into EBITDA-accretive, contracted projects;
#            adjusted EBITDA grows toward the $8.6B 2026 guide and beyond; leverage
#            drifts to ~3.8x as guided but stabilizes; dividend keeps growing at its
#            steady ~2-3%/yr clip (10th consecutive increase); LNG feedgas contracting
#            advances toward the 12 Bcf/d 2028 target on schedule. Roughly "consensus
#            PT ~$35" realized with a modest haircut for leverage/valuation caution.
#
# BULL  $39: The data-center/power-generation gas demand inflection proves larger and
#            faster than guided — KMI converts a meaningful share of the >10 Bcf/d
#            opportunity set into signed, long-term contracts, expanding the backlog
#            well past $10.1B; LNG feedgas contracting accelerates toward (or past) the
#            12 Bcf/d 2028 target; credit profile stabilizes near 3.5x as EBITDA growth
#            outpaces capex — the market starts re-rating KMI from "steady toll road"
#            toward "structural beneficiary of the AI/power-demand supercycle."
#
# XBULL $46: Full "structural demand supercycle" thesis — data-center gas demand
#            converts at scale (multiple >10 Bcf/d projects sanctioned and contracted),
#            LNG feedgas volumes overshoot the 2030 industry doubling, backlog swells
#            toward $15B+, AND continued credit upgrades lower KMI's cost of capital
#            further, compounding the re-rating. Requires multiple structural tailwinds
#            to align simultaneously — the highest-conviction, lowest-probability outcome.
BEAR    = 24.0
BASE    = 33.0
BULL    = 39.0
XBULL   = 46.0

# ── EPP (EARNINGS POWER PRICE) ───────────────────────────────────────────────
# Trough scenario: a severe demand-shock or balance-sheet-stress downcycle (echoing
# KMI's own 2015-16 dividend-cut episode) drags adjusted EPS toward levels last seen
# in that period. PE_TROUGH reflects the modest premium a fee-based, contracted
# midstream "toll road" still commands even in a panic — well above what a pure
# commodity-price-taker E&P would get, owing to the visibility of take-or-pay cash flows.
EPS_TROUGH  = 0.70
PE_TROUGH   = 15.0
EPP         = EPS_TROUGH * PE_TROUGH   # = $10.50

# ── SCA: STRUCTURAL COMPETITIVE ADVANTAGE ───────────────────────────────────
# KMI's moat is its irreplaceable, permitted natural-gas pipeline/storage network —
# a genuine toll road that the data-center and LNG-export buildouts need to access —
# plus a fee-based/take-or-pay contract base and a newly-upgraded IG credit profile.
# The structural offsets are real: leverage is drifting up as growth capex ramps, and
# the company remains exposed (indirectly, via volumes and regulatory/permitting
# dynamics) to the broader natural-gas price and policy environment.

SCA_FACTORS = {
    # Factor                                       : (score,  weight)
    "irreplaceable_natural_gas_pipeline_network"   : (+0.35,  0.18),  # Permitted, built-out network — a genuine toll road, not easily replicated
    "fee_based_contracted_cash_flows"              : (+0.30,  0.16),  # Overwhelmingly take-or-pay / fee-based — minimal direct commodity exposure
    "data_center_lng_secular_demand_tailwind"      : (+0.35,  0.16),  # >10 Bcf/d incremental opportunity set; LNG feedgas doubling industry-wide by 2030
    "investment_grade_credit_bbb_plus"             : (+0.25,  0.14),  # Newly upgraded to Baa1/BBB+ at all three agencies — lowering cost of capital
    "dividend_growth_track_record"                 : (+0.20,  0.13),  # 9 consecutive annual dividend increases; steady ~2-3%/yr compounding
    "rising_leverage_amid_growth_capex"            : (-0.25,  0.12),  # Net debt/EBITDA drifting from 3.6x toward a guided 3.8x as backlog capex ramps
    "natural_gas_price_and_regulatory_exposure"    : (-0.20,  0.11),  # Indirect commodity/volume exposure plus pipeline permitting & regulatory risk
}

SCA_NET  = sum(score * weight for score, weight in SCA_FACTORS.values())
# SCA_NET = 0.35×0.18 + 0.30×0.16 + 0.35×0.16 + 0.25×0.14 + 0.20×0.13 + (-0.25)×0.12 + (-0.20)×0.11
# SCA_NET ≈ 0.063 + 0.048 + 0.056 + 0.035 + 0.026 - 0.03 - 0.022 = 0.176

SCA_SCALE = 0.45  # Fixed framework parameter

# ── 6 PROXY SIGNALS ──────────────────────────────────────────────────────────
# Signal   (score 1–4, weight)
# 1=BEAR, 1.5=BEAR+, 2=BASE, 2.5=BASE+, 3=BULL, 3.5=BULL+, 4=XBULL

SIGNALS = {
    # A genuinely new, structural demand driver: ~70% of future US data-center power
    # demand under development sits in states KMI serves, and management is actively
    # developing projects that could serve >10 Bcf/d of incremental gas demand from
    # power generation alone — a multi-decade tailwind that simply did not exist in
    # the company's plan even a few years ago, and is now showing up in a growing backlog.
    "data_center_power_demand_inflection": (3.5, 0.20),

    # LNG feedgas exposure scaling fast and on contract: 8 Bcf/d contracted today,
    # growing to 12 Bcf/d by end-2028, against an industry backdrop where total US LNG
    # feedgas demand is projected to roughly double from ~19.8 Bcf/d (2026, +19% YoY)
    # to >34 Bcf/d by 2030 — KMI sits astride one of the most durable secular growth
    # curves in North American energy, and the $10.1B backlog (92% natural gas) is the
    # tangible evidence of that exposure converting into contracted projects.
    "lng_feedgas_growth_contracted_backlog": (3.5, 0.18),

    # The "toll road" itself: KMI's business is overwhelmingly fee-based / take-or-pay,
    # generating highly visible, contracted cash flows largely insulated from commodity
    # price swings — the durable mechanism that funds steady dividend growth (9 straight
    # annual increases) regardless of where natural gas prices sit in any given quarter.
    "fee_based_take_or_pay_business_model": (3.5, 0.16),

    # The honest near-term risk: leverage is drifting UP (3.6x → guided 3.8x net
    # debt/EBITDA) as growth capex ramps to fund the backlog, and at ~23x forward
    # earnings near the top of its 52-week range, KMI is no longer a deep-value name —
    # there is real room for multiple compression if the demand-growth narrative cools
    # even modestly or if backlog conversion runs behind schedule.
    "rising_leverage_and_full_valuation_risk": (2.0, 0.18),

    # A genuine, durable capital-return mechanism: 9 consecutive annual dividend
    # increases (2026's +2% the latest), a ~3.7-3.8% yield, and a freshly-upgraded
    # investment-grade credit profile (Baa1/BBB+ at all three agencies) — lowering
    # KMI's cost of capital precisely as it ramps growth investment into a generational
    # demand opportunity.
    "dividend_growth_and_credit_upgrade": (3.0, 0.14),

    # A real, if manageable, structural offset: converting a $10.1B backlog into
    # EBITDA on schedule requires sustained execution (cost discipline, timeline
    # adherence) plus navigating the permitting/regulatory environment for new
    # natural-gas pipeline and LNG-feedgas infrastructure — the same friction that
    # has slowed midstream buildouts industry-wide for the past decade.
    "project_execution_and_regulatory_permitting_risk": (2.0, 0.14),
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

# Conservative 2yr: management's own FY2026E adjusted EPS guidance × a multiple BELOW
# the current ~23x implied forward + 2yr dividends — pure compounding test, no heroic
# re-rating required
PE_CONSERVATIVE = 20.0
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
    print("  FY2025 FINANCIALS & FY2026 GUIDANCE")
    print(sep)
    print(f"  Revenue: ${REVENUE_FY2025_B:.1f}B (+12.2% YoY)  |  Adj. EBITDA: ${ADJ_EBITDA_FY2025_B:.1f}B")
    print(f"  Adj. EPS +{ADJ_EPS_FY2025_GROWTH_PCT}% YoY | Net income to KMI +{NET_INCOME_GROWTH_PCT}% YoY | Reported diluted EPS ${REPORTED_DILUTED_EPS:.2f}")
    print(f"  2026 guide: Adj. EBITDA ${ADJ_EBITDA_GUIDANCE_FY2026_B:.1f}B (+2.5%) | Adj. EPS ${ADJ_EPS_GUIDANCE_FY2026:.2f} (+{ADJ_EPS_FY2025_GROWTH_PCT-8}%) | Adj. net income +{ADJ_NET_INCOME_GROWTH_GUIDE_PCT}%")

    print(f"\n  Q1 2026 snapshot:")
    print(f"    Adj. EBITDA ${Q1_ADJ_EBITDA_M:,}mm (+18% YoY) | Adj. EPS ${Q1_ADJ_EPS:.2f} (+41% YoY) | Net income ${Q1_NET_INCOME_M:,}mm (+39% YoY)")

    print(f"\n{sep}")
    print("  BALANCE SHEET / CREDIT")
    print(sep)
    print(f"  Net debt: ${NET_DEBT_B:.1f}B  |  Net debt/EBITDA: {NET_DEBT_TO_EBITDA:.1f}x (Q1'26) → guided to ~{NET_DEBT_TO_EBITDA_GUIDE:.1f}x by YE2026 as growth capex ramps")
    print(f"  {CREDIT_RATING_NOTE}")

    print(f"\n{sep}")
    print("  PROJECT BACKLOG — THE TANGIBLE EVIDENCE OF THE DEMAND INFLECTION")
    print(sep)
    print(f"  Backlog: ${BACKLOG_B:.1f}B (up $145mm QoQ)  |  ~{BACKLOG_NATGAS_PCT}% natural gas  |  ~{BACKLOG_POWERGEN_LDC_PCT}% tied to power-gen / LDC demand growth")
    print(f"  {BUSINESS_MODEL_NOTE}")

    print(f"\n{sep}")
    print("  GROWTH ENGINE #1 — DATA CENTER / POWER-GENERATION GAS DEMAND")
    print(sep)
    print(f"  ~{DATA_CENTER_DEMAND_SHARE_PCT}% of future US data-center power demand under development sits in states KMI serves")
    print(f"  Projects in development could serve >{INCREMENTAL_GAS_DEMAND_POTENTIAL_BCFD} Bcf/d of incremental gas demand from power generation alone")

    print(f"\n{sep}")
    print("  GROWTH ENGINE #2 — LNG FEEDGAS EXPOSURE")
    print(sep)
    print(f"  Contracted feedgas: {LNG_FEEDGAS_CONTRACTED_TODAY_BCFD} Bcf/d today → {LNG_FEEDGAS_CONTRACTED_2028_BCFD} Bcf/d by end-2028")
    print(f"  US LNG feedgas demand: {US_LNG_FEEDGAS_DEMAND_2026_BCFD:.1f} Bcf/d in 2026 (+19% YoY, record) → >{US_LNG_FEEDGAS_DEMAND_2030_BCFD:.0f} Bcf/d by 2030 (~doubling industry-wide)")

    print(f"\n{sep}")
    print("  ANALYST CONSENSUS")
    print(sep)
    print(f"  FY2026E adj. EPS (mgmt guide): ${EPS_FY2026E:.2f}  |  Implied forward P/E: ~{FORWARD_PE_IMPLIED:.1f}x")
    print(f"  Rating: {CONSENSUS_RATING}  |  Price targets: consensus ${CONSENSUS_PT:.0f} (range ${PT_LOW:.0f}-${PT_HIGH:.0f})")
    print(f"  {ANALYST_RATING_NOTE}")

    print(f"\n{sep}")
    print("  6 PROXY SIGNALS")
    print(sep)
    labels = {
        "data_center_power_demand_inflection":              "Data center / power-gen demand inflection",
        "lng_feedgas_growth_contracted_backlog":            "LNG feedgas growth / contracted backlog",
        "fee_based_take_or_pay_business_model":             "Fee-based / take-or-pay business model",
        "rising_leverage_and_full_valuation_risk":          "Rising leverage / full valuation risk",
        "dividend_growth_and_credit_upgrade":               "Dividend growth & credit upgrade",
        "project_execution_and_regulatory_permitting_risk": "Project execution / regulatory-permitting risk",
    }
    for k, (score, weight) in SIGNALS.items():
        bar = "█" * int(score * 5)
        print(f"  {labels[k]:<48}  {score:.1f}  wt={weight:.2f}  {bar}")
    print(f"  {'PROXY COMPOSITE':<48}  {PROXY_COMPOSITE:.2f}")

    print(f"\n{sep}")
    print("  SCA — STRUCTURAL COMPETITIVE ADVANTAGE")
    print(sep)
    sca_labels = {
        "irreplaceable_natural_gas_pipeline_network":  "Irreplaceable natural-gas pipeline network",
        "fee_based_contracted_cash_flows":             "Fee-based / contracted cash flows",
        "data_center_lng_secular_demand_tailwind":     "Data-center / LNG secular demand tailwind",
        "investment_grade_credit_bbb_plus":            "Investment-grade credit (Baa1/BBB+)",
        "dividend_growth_track_record":                "Dividend growth track record (9yr)",
        "rising_leverage_amid_growth_capex":           "Rising leverage amid growth capex",
        "natural_gas_price_and_regulatory_exposure":   "Nat-gas price & regulatory exposure",
    }
    for k, (score, weight) in SCA_FACTORS.items():
        print(f"  {sca_labels[k]:<48}  {score:+.2f} × {weight:.2f} = {score*weight:+.4f}")
    print(f"  {'SCA_NET':<48}  {SCA_NET:+.4f}")
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
    print(f"  FY2026E adj. EPS (mgmt guidance): ${EPS_FY2026E:.2f}")
    print(f"  Conservative PE applied:          {PE_CONSERVATIVE:.1f}× (below the ~{FORWARD_PE_IMPLIED:.0f}x implied forward multiple — no re-rating credit)")
    print(f"  Target price 2yr:                 ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.1f}× + ${2*ANNUAL_DIV:.2f} div = ${PRICE_2YR_CONSV:.2f}")
    print(f"  2-year return:                    {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  Note: this is the 'multiple compresses modestly off today's ~23x' floor case — BASE/BULL")
    print(f"  diverge as the data-center/LNG demand inflection converts backlog into EBITDA and re-rates the multiple.")

    print(f"\n{sep}")
    print("  WHY THIS IS AN ◎ ACCUMULATE, NOT A ◉ BUY OR ✕ AVOID")
    print(sep)
    print("""
  Kinder Morgan is the natural-gas "toll road" sitting at the front edge of arguably the
  most durable demand inflection in North American energy — but at $31.70, roughly 70%
  up its 52-week range, the stock is no longer a deep-value name. This is a structurally
  advantaged compounder trading at a fair-to-full price, not a dislocation.

  WHAT THE MARKET ALREADY PRICES IN (at $31.70, well off the 52-week low):
  • Steady toll-road compounding: ~2-5% EBITDA/EPS growth and continued dividend increases
  • The $10.1B backlog converts on a normal timeline into contracted, fee-based EBITDA
  • Leverage drifts to the guided ~3.8x net debt/EBITDA and stabilizes there
  • LNG feedgas contracting advances toward 12 Bcf/d by 2028 roughly as guided

  WHAT COULD MAKE THIS MORE THAN FAIRLY PRICED:
  1. The data-center/power-generation gas demand opportunity (>10 Bcf/d in development,
     ~70% of future US data-center power demand in KMI's footprint) converts into signed,
     long-term contracts FASTER and LARGER than guided — expanding the backlog meaningfully
  2. LNG feedgas contracting accelerates past the 12 Bcf/d 2028 target as the industry-wide
     doubling toward >34 Bcf/d by 2030 pulls forward
  3. Continued credit upgrades (already Baa1/BBB+ at all three agencies) lower KMI's cost
     of capital further, making growth capex more accretive and supporting a re-rating
  4. Backlog conversion runs AHEAD of the 3.8x leverage guide (EBITDA growth outpacing
     capex), easing the market's single biggest near-term concern about the credit profile

  THE RISK (the honest read on where this sits):
  • Leverage is genuinely drifting UP — 3.6x today, guided to ~3.8x by YE2026 — as growth
    capex ramps to fund the backlog; this is the central swing factor for the credit story
  • At ~23x implied forward earnings near the top of its 52-week range, KMI offers less
    margin of safety than it did at the 2024-25 lows; multiple compression is a real risk
    if the demand-growth narrative cools or backlog conversion runs behind schedule
  • Pipeline/LNG-feedgas infrastructure carries genuine permitting and regulatory risk —
    the same friction that has slowed midstream buildouts industry-wide for a decade
  • KMI remains indirectly exposed to natural gas prices and volumes despite its
    overwhelmingly fee-based / take-or-pay contract structure

  WHAT MAKES THE DOWNSIDE GENUINELY CUSHIONED (why this isn't a coin-flip):
  • The "toll road" model — overwhelmingly fee-based / take-or-pay cash flows — means
    the dividend (9 consecutive annual increases, ~3.7-3.8% yield) is durable through
    a demand-growth digestion period, not at risk; this is a multiple/sentiment
    correction scenario in the bear case, not a cash-flow crisis
  • A freshly-upgraded investment-grade credit profile (Baa1/BBB+ at all three agencies)
    gives KMI real headroom to fund growth capex without genuine balance-sheet stress

  POSITION SIZING GUIDANCE:
  • This is a "own the pipes the AI/data-center/LNG buildout needs and let the toll road
    compound" name — a core energy-infrastructure holding, not a leveraged cyclical trade
  • Add on weakness toward $26-28 (where Ratio B moves toward BUY territory and the
    yield approaches ~4.2-4.6%)
  • Backlog conversion confirming >$10.1B and leverage stabilizing AT (not past) 3.8x
    are the catalysts that should re-rate this from "steady toll road" toward "structural
    beneficiary of the AI/power-demand supercycle"
""")

    print(SEP)
    print(f"""
SUMMARY: KMI ◎ ACCUMULATE — Ratio B 1.06× (24.3% downside / 23.0% upside). NATURAL-GAS \
TOLL ROAD AT THE FRONT EDGE OF A STRUCTURAL DEMAND INFLECTION: trading at $31.70 (52-wk \
range $25.60-34.81, ~70% up the range — fair-to-full, not deep value) on a genuinely new \
demand driver showing up in a growing $10.1B backlog (92% natural gas, 60% tied to \
power-gen/LDC demand) — ~70% of future US data-center power demand under development sits \
in states KMI serves, and management is developing projects that could serve >10 Bcf/d of \
incremental gas demand from power generation alone. LNG FEEDGAS SCALING ON CONTRACT: 8 \
Bcf/d today growing to 12 Bcf/d by end-2028, against an industry backdrop where US LNG \
feedgas demand roughly doubles from ~19.8 Bcf/d (2026) to >34 Bcf/d by 2030. THE TOLL ROAD \
ITSELF: overwhelmingly fee-based/take-or-pay cash flows funding 9 consecutive annual \
dividend increases (~3.7-3.8% yield) on a freshly-upgraded IG credit profile (Baa1/BBB+ at \
all three agencies). FY2025: revenue $16.9B (+12.2%), adj. EBITDA $8.4B; 2026 guide adj. \
EBITDA $8.6B, adj. EPS $1.36. THE HONEST RISK: net debt/EBITDA drifting from 3.6x toward a \
guided 3.8x as growth capex ramps, and at ~23x implied forward earnings near the top of its \
52-week range, there's less margin of safety than at the 2024-25 lows. Consensus 'Buy \
(mixed)' (~12 Buy/10 Hold/1 Sell), PT ~$35 (range $26-43). Conservative 2yr (modest \
multiple-compression floor case): EPS $1.36 x 20x + $2.38 div = $29.58 -> -6.7% — BASE/BULL \
diverge as the data-center/LNG demand inflection converts backlog into EBITDA and re-rates \
the multiple. Fee-based toll-road model + IG balance sheet make the downside genuinely \
cushioned — add on weakness toward $26-28. Bear $24 · Base $33 · Bull $39 · XBull $46."""
    )

    print(f"SIGNAL: {SIGNAL_TEXT} (irreplaceable gas pipeline toll road + data-center/LNG demand inflection, fee-based cash flows) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
