"""
GE Aerospace (NYSE: GE)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◎ ACCUMULATE  |  Ratio B: 1.03×  |  EPP Gap: +296.6%

A PURE-PLAY JET-ENGINE DUOPOLY WITH A MULTI-DECADE INSTALLED-BASE ANNUITY — A PREMIUM FRANCHISE AT A FAIR-TO-ATTRACTIVE PRICE
Trading at $232.00 (52-week range $172-268, roughly two-thirds up its range — a name that has
re-rated meaningfully as the post-spin "GE Aerospace" pure-play story has taken hold) on the
back of what is, structurally, one of the best businesses in all of industrials: a duopoly
(with Pratt & Whitney/RTX) in widebody and narrowbody commercial jet engines, anchored by the
CFM International joint venture (with Safran) — whose LEAP engine is the sole or dominant
powerplant on the best-selling Boeing 737 MAX and Airbus A320neo families — plus the GE9X on
the Boeing 777X and a deep US/allied military-engine franchise (F404/F414/F110/XA100/T901).
The real moat isn't the engines themselves — it's the multi-decade aftermarket services
annuity that comes with each one: spare parts, overhauls, and long-term service agreements
that generate high-margin, highly recurring cash flow for 20-30+ years per installed engine,
on a base of tens of thousands of engines in service and a record order backlog.

The honest surprise: despite a strong multi-year re-rating that has lifted the stock roughly
two-thirds up its 52-week range, the bottom-up math still comes out close to balanced — the
bull-case upside (CFM/LEAP duopoly economics compounding through a record backlog, the
aftermarket-services annuity maturing into its highest-margin years, and continued disciplined
execution under CEO Larry Culp) roughly matches the bear-case downside (a cyclical air-travel
demand shock, persistent titanium/forging/casting supply bottlenecks, or simply a "great
company, full price" multiple-compression episode). That balance — for a business this
structurally advantaged — is what tips this from a "wait for a pullback" name into a genuine
ACCUMULATE: the moat is not only intact but arguably strengthening (the installed base keeps
growing, and the services annuity gets more valuable, not less, with every engine delivered),
and the price does not yet demand a "flawless execution forever" scenario to be made whole.

Conviction: MODERATE-HIGH on the structural moat thesis (the engine-plus-services annuity
model, duopoly economics, and CFM/military franchise are genuinely durable, multi-decade
competitive advantages that few industrial businesses can match) AND on the entry point —
Ratio B sits just above parity (roughly balanced risk/reward), which for a franchise of this
quality is an attractive place to be building a position rather than waiting on the sidelines
for a deeper pullback that may not come.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "GE"
COMPANY         = "GE Aerospace"
SECTOR          = "Aerospace & Defense · Commercial & Military Jet Engines (CFM/LEAP, GE9X, F-Series Military Engines) · Aftermarket Services Annuity · NYSE: GE"
SECTOR_GROUP    = "Industrials"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 232.00   # June 2026, roughly two-thirds up the 52-week range — post-spin pure-play re-rating
ANNUAL_DIV      = 1.28     # $0.32/qtr quarterly dividend; yield ~0.6%
SHARES_OUT_B    = 1.085    # ~1.085B shares outstanding post-spinoffs (GE Vernova, GE HealthCare)
MARKET_CAP_B    = 251.7    # CURRENT_PRICE × SHARES_OUT_B
FW52_HIGH       = 268.00
FW52_LOW        = 172.00

# ── FY2025 FULL-YEAR FINANCIALS ─────────────────────────────────────────────
REVENUE_FY2025_B           = 40.2
ADJ_NET_INCOME_FY2025_B    = 7.85
ADJ_EPS_FY2025             = 7.25
OCF_FY2025_B               = 8.45
FCF_FY2025_B               = 7.65
ADJ_OPERATING_MARGIN_PCT   = 23.5
ADJ_EPS_YOY_PCT            = 24    # Strong services mix shift + commercial engine deliveries growth + cost discipline

# ── ENGINE FRANCHISE / INSTALLED BASE ─────────────────────────────────────────
INSTALLED_BASE_ENGINES_K    = 45     # ~45,000 commercial and military engines in service globally
CFM_LEAP_NOTE               = "CFM International (50/50 JV with Safran) and its LEAP engine are the sole or dominant powerplant on the Boeing 737 MAX and Airbus A320neo — the two best-selling commercial aircraft families in history — giving GE Aerospace genuine duopoly economics (with Pratt & Whitney/RTX) in the narrowbody engine market"
GE9X_WIDEBODY_NOTE          = "The GE9X (exclusive powerplant on the Boeing 777X) and GEnx (787/747-8) anchor a leading widebody position, while a deep US/allied military-engine franchise (F404/F414, F110, XA100 adaptive-cycle, T901 helicopter engine) provides genuine, multi-decade defense-program visibility"
ORDER_BACKLOG_B             = 175    # Commercial + defense backlog — record levels
BACKLOG_NOTE                = "A record order backlog (~$175B commercial + defense) provides multi-year revenue visibility rarely seen at this scale in industrials"

# ── AFTERMARKET SERVICES ANNUITY — THE REAL MOAT ─────────────────────────────
SERVICES_REVENUE_SHARE_PCT  = 70.0   # Services/aftermarket as a share of commercial-engine segment revenue
SERVICES_MARGIN_PREMIUM_NOTE = "Spare parts, overhauls, and long-term service agreements (LTSAs) generate structurally higher, more stable margins than original-equipment sales — and because each engine generates 20-30+ years of service revenue, the installed base functions as a multi-decade, highly recurring cash-flow annuity that compounds with every delivery"
SERVICES_ANNUITY_NOTE       = "The 'razor-and-blades' engine-plus-services model is, structurally, one of the best businesses in all of industrials — the larger the installed base grows, the larger and more durable the aftermarket annuity becomes, a flywheel that strengthens with time rather than erodes"

# ── EXECUTION / OPERATING MODEL ───────────────────────────────────────────────
LEAN_OPERATING_MODEL_NOTE   = "CEO Larry Culp's lean operating-model discipline (post-GE-breakup focus, simplified portfolio, de-levered balance sheet) has driven a multi-year run of margin expansion and execution credibility that the market has rewarded with a substantially re-rated multiple"
SUPPLY_CHAIN_NOTE           = "Commercial aerospace remains supply-chain-constrained — titanium, forgings, and castings bottlenecks have periodically gated engine and spare-parts deliveries across the industry, a structural risk that affects GE Aerospace alongside every OEM and supplier in the value chain"

# ── BALANCE SHEET ─────────────────────────────────────────────────────────────
NET_DEBT_B                  = -5.5   # Net cash position post-spinoffs and debt paydown
CREDIT_RATING_NOTE          = "A meaningfully de-levered, net-cash balance sheet (A-range ratings) post-spinoff — a dramatic transformation from the heavily-indebted, multi-segment conglomerate of a decade ago, and a genuine source of strategic flexibility"

# ── ANALYST CONSENSUS ────────────────────────────────────────────────────────
EPS_FY2026E             = 8.55     # Consensus reflects continued services-mix shift and commercial engine delivery growth
TRAILING_PE             = 32.0
FORWARD_PE              = 27.1
CONSENSUS_PT            = 255.0    # Average target ~$255 (range $210-300)
PT_LOW                  = 210.0
PT_HIGH                 = 300.0
CONSENSUS_RATING        = "Buy / Strong Buy"
ANALYST_RATING_NOTE     = "~21 Buy / 7 Hold / 1 Sell of ~29 analysts; consensus PT ~$255 (range $210-300) — broadly enthusiastic about the structural moat, genuinely split on how much further the premium multiple can expand from here"

# ── SCENARIOS ────────────────────────────────────────────────────────────────
# BEAR  $172: A meaningful air-travel demand shock (macro recession, fuel-price spike, or
#             geopolitical disruption) combined with a deepening supply-chain bottleneck that
#             delays narrowbody build-rate ramps and defers services revenue recognition,
#             triggering a sharp multiple-compression episode characteristic of premium-priced
#             industrials when the cycle turns — even though the installed-base annuity means
#             services cash flow would prove far more resilient than new-unit deliveries.
#             Roughly the lower quarter of the 52-week range — this is a "premium multiple
#             meets a cyclical air-pocket" drawdown, not a structural-moat-impairment story.
#
# BASE  $232: Roughly where the stock sits today — narrowbody build rates continue their
#             gradual recovery toward pre-pandemic-plus levels, the services/aftermarket mix
#             continues its structural shift higher, defense programs deliver on schedule, and
#             the market continues to apply a premium "best industrial franchise" multiple that
#             largely already reflects the current trajectory. "Consensus PT ~$255" partially
#             realized over time, with the multiple itself doing little further expansion.
#
# BULL  $290: Narrowbody build rates accelerate meaningfully (Boeing/Airbus production-rate
#             ramps land closer to plan, supply-chain bottlenecks ease), the services annuity
#             compounds faster than expected as the installed base ages into its highest-margin
#             overhaul years, defense-program wins (XA100, next-gen platforms) add genuine
#             multi-decade visibility, AND the market extends the "structurally the best
#             industrial franchise in the market" premium even further — a continuation of the
#             re-rating trajectory of the past several years.
#
# XBULL $330: Full structural-premium thesis — GE Aerospace becomes recognized as a genuine
#             "compounder" on par with the market's highest-quality industrial and aerospace
#             franchises, narrowbody and widebody delivery cycles both accelerate
#             simultaneously, the services annuity scales toward record margins as the
#             installed base reaches critical mass, defense programs expand materially, AND
#             the market assigns a structural-premium multiple that fully prices in 20-30
#             years of visible, compounding aftermarket cash flow — the scenario in which
#             "best business in industrials" finally commands the multiple of the market's
#             very best compounders. Requires several structural and cyclical tailwinds to
#             align simultaneously — high-conviction, lower-probability outcome.
BEAR    = 172.0
BASE    = 232.0
BULL    = 290.0
XBULL   = 330.0

# ── EPP (EARNINGS POWER PRICE) ───────────────────────────────────────────────
# Trough scenario: even the highest-quality aerospace franchises see earnings compress sharply
# in a genuine demand shock — the 2020 COVID-driven air-travel collapse drove GE's predecessor
# aviation segment to a fraction of its prior earnings power despite the durability of the
# services annuity. EPS_TROUGH reflects a severe, multi-quarter demand-shock scenario, well
# below the FY2025 print of $7.25, and PE_TROUGH reflects the still-elevated multiple a
# best-in-class franchise commands even in a downturn (the market rarely lets a true
# structural-moat business trade down to a true "cyclical trough" multiple).
EPS_TROUGH  = 4.50
PE_TROUGH   = 13.0
EPP         = EPS_TROUGH * PE_TROUGH   # = $58.50

# ── SCA: STRUCTURAL COMPETITIVE ADVANTAGE ───────────────────────────────────
# GE Aerospace's moat blends genuine duopoly economics in commercial jet engines (CFM/LEAP on
# the best-selling narrowbody platforms, GE9X on the 777X), a multi-decade aftermarket-
# services annuity that compounds with every engine delivered, a deep and durable military-
# engine franchise with genuine multi-decade program visibility, and a meaningfully
# de-levered, net-cash balance sheet under a credible operating-model culture. The offsets:
# the stock has already re-rated to a premium multiple that leaves less room for multiple
# expansion, and the business remains genuinely exposed to commercial-aerospace cyclicality
# and persistent supply-chain constraints that are largely outside its direct control.

SCA_FACTORS = {
    # Factor                                            : (score,  weight)
    "engine_duopoly_and_cfm_leap_platform_position"    : (+0.40,  0.18),  # Genuine duopoly economics; LEAP is sole/dominant on the best-selling narrowbody families in history
    "multi_decade_aftermarket_services_annuity"        : (+0.40,  0.17),  # The real moat — 20-30yr recurring, high-margin cash flow per engine, compounding with the installed base
    "military_engine_franchise_and_program_visibility" : (+0.25,  0.14),  # Deep US/allied defense-engine franchise with genuine multi-decade program visibility
    "delevered_balance_sheet_and_operating_model_culture": (+0.25,  0.13),  # Net-cash position + Culp operating-model credibility — a transformed, disciplined organization
    "record_backlog_and_multi_year_revenue_visibility" : (+0.20,  0.13),  # ~$175B record backlog provides multi-year visibility rarely seen at this scale
    "premium_valuation_limits_further_multiple_expansion": (-0.30,  0.13),  # Stock has already re-rated substantially; less room for the multiple itself to do the work from here
    "commercial_aerospace_cyclicality_and_supply_chain_risk": (-0.25,  0.12),  # Genuinely exposed to air-travel demand cycles and persistent titanium/forging/casting bottlenecks
}

SCA_NET  = sum(score * weight for score, weight in SCA_FACTORS.values())
# SCA_NET = 0.40×0.18 + 0.40×0.17 + 0.25×0.14 + 0.25×0.13 + 0.20×0.13 + (-0.30)×0.13 + (-0.25)×0.12
# SCA_NET ≈ 0.072 + 0.068 + 0.035 + 0.0325 + 0.026 - 0.039 - 0.030 = 0.1645

SCA_SCALE = 0.45  # Fixed framework parameter

# ── 6 PROXY SIGNALS ──────────────────────────────────────────────────────────
# Signal   (score 1–4, weight)
# 1=BEAR, 1.5=BEAR+, 2=BASE, 2.5=BASE+, 3=BULL, 3.5=BULL+, 4=XBULL

SIGNALS = {
    # CFM International's LEAP engine holds a sole-or-dominant position on the Boeing 737 MAX
    # and Airbus A320neo — the two best-selling commercial aircraft families in history — and
    # the GE9X is the exclusive powerplant on the Boeing 777X, giving GE Aerospace genuine
    # duopoly economics in commercial jet engines that few industrial businesses can rival.
    "engine_duopoly_and_platform_exclusivity": (3.5, 0.19),

    # The real moat is the aftermarket services annuity: each engine delivered generates
    # 20-30+ years of high-margin spare-parts, overhaul, and long-term-service-agreement
    # revenue — a structurally compounding, highly recurring cash-flow flywheel that
    # strengthens as the ~45,000-engine installed base ages into its highest-margin years.
    "aftermarket_services_annuity_compounding_flywheel": (3.5, 0.18),

    # A record ~$175B commercial-and-defense order backlog provides multi-year revenue
    # visibility rarely matched at this scale in industrials, while a deep US/allied
    # military-engine franchise (F404/F414, F110, XA100, T901) adds genuine multi-decade
    # defense-program durability largely insulated from commercial-cycle swings.
    "record_backlog_and_defense_program_durability": (3.0, 0.15),

    # CEO Larry Culp's lean operating-model discipline has driven a multi-year run of margin
    # expansion, portfolio simplification, and balance-sheet de-leveraging (now net-cash) — a
    # genuine organizational transformation that has earned real execution credibility with
    # both customers and the market.
    "operating_model_execution_and_balance_sheet_strength": (3.0, 0.15),

    # The honest near-term risk: at ~27x forward earnings — a clear premium multiple that has
    # already re-rated substantially over the past several years — the stock leaves
    # meaningfully less room for further multiple expansion, and sits roughly two-thirds up
    # its own 52-week range, raising the bar for what "more than fairly priced" looks like.
    "premium_valuation_limits_near_term_upside": (2.0, 0.18),

    # Commercial aerospace remains a genuinely cyclical, supply-chain-constrained industry —
    # persistent titanium/forging/casting bottlenecks have periodically gated engine and
    # spare-parts deliveries industry-wide, and a macro-driven air-travel demand shock would
    # directly pressure both new-unit deliveries and the services growth the market now expects.
    "supply_chain_and_commercial_cycle_exposure": (2.0, 0.15),
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

# Conservative 2yr: FY2026E EPS (consensus, reflecting continued services-mix shift and
# delivery growth) × a multiple modestly below the current ~27x forward — a mild
# multiple-compression test, no further premium-expansion credit required
PE_CONSERVATIVE = 24.0
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
    print("  ENGINE FRANCHISE & INSTALLED BASE")
    print(sep)
    print(f"  Installed base: ~{INSTALLED_BASE_ENGINES_K}K engines  |  Order backlog: ~${ORDER_BACKLOG_B}B")
    print(f"  {CFM_LEAP_NOTE}")
    print(f"  {GE9X_WIDEBODY_NOTE}")
    print(f"  {BACKLOG_NOTE}")

    print(f"\n{sep}")
    print("  AFTERMARKET SERVICES ANNUITY — THE REAL MOAT")
    print(sep)
    print(f"  Services share of commercial-engine revenue: ~{SERVICES_REVENUE_SHARE_PCT:.0f}%")
    print(f"  {SERVICES_MARGIN_PREMIUM_NOTE}")
    print(f"  {SERVICES_ANNUITY_NOTE}")

    print(f"\n{sep}")
    print("  EXECUTION / OPERATING MODEL & BALANCE SHEET")
    print(sep)
    print(f"  Net debt: ${NET_DEBT_B:.1f}B (net-cash position)")
    print(f"  {LEAN_OPERATING_MODEL_NOTE}")
    print(f"  {SUPPLY_CHAIN_NOTE}")
    print(f"  {CREDIT_RATING_NOTE}")

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
        "engine_duopoly_and_platform_exclusivity":              "Engine duopoly & platform exclusivity (CFM/LEAP, GE9X)",
        "aftermarket_services_annuity_compounding_flywheel":    "Aftermarket services annuity — compounding flywheel",
        "record_backlog_and_defense_program_durability":        "Record backlog & defense-program durability",
        "operating_model_execution_and_balance_sheet_strength": "Operating-model execution & balance-sheet strength",
        "premium_valuation_limits_near_term_upside":            "Premium valuation limits near-term upside",
        "supply_chain_and_commercial_cycle_exposure":           "Supply-chain & commercial-cycle exposure",
    }
    for k, (score, weight) in SIGNALS.items():
        bar = "█" * int(score * 5)
        print(f"  {labels[k]:<54}  {score:.1f}  wt={weight:.2f}  {bar}")
    print(f"  {'PROXY COMPOSITE':<54}  {PROXY_COMPOSITE:.2f}")

    print(f"\n{sep}")
    print("  SCA — STRUCTURAL COMPETITIVE ADVANTAGE")
    print(sep)
    sca_labels = {
        "engine_duopoly_and_cfm_leap_platform_position":          "Engine duopoly & CFM/LEAP platform position",
        "multi_decade_aftermarket_services_annuity":              "Multi-decade aftermarket services annuity",
        "military_engine_franchise_and_program_visibility":       "Military engine franchise & program visibility",
        "delevered_balance_sheet_and_operating_model_culture":    "De-levered balance sheet & operating-model culture",
        "record_backlog_and_multi_year_revenue_visibility":       "Record backlog & multi-year revenue visibility",
        "premium_valuation_limits_further_multiple_expansion":    "Premium valuation limits further multiple expansion",
        "commercial_aerospace_cyclicality_and_supply_chain_risk": "Commercial-aerospace cyclicality & supply-chain risk",
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
    print(f"  FY2026E EPS (consensus, reflecting continued services-mix shift and delivery growth): ${EPS_FY2026E:.2f}")
    print(f"  Conservative PE applied:                                            {PE_CONSERVATIVE:.1f}× (a modest compression from the ~27.1x forward — no further premium-expansion assumed)")
    print(f"  Target price 2yr:                                                   ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.1f}× + ${2*ANNUAL_DIV:.2f} div = ${PRICE_2YR_CONSV:.2f}")
    print(f"  2-year return:                                                      {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  Note: this is the 'services annuity compounds as expected, but the multiple itself does not")
    print(f"  expand further — and may even compress slightly' floor case — BULL/XBULL require either an")
    print(f"  acceleration in delivery/services growth OR continued multiple expansion toward 'elite compounder' levels.")

    print(f"\n{sep}")
    print("  WHY THIS IS AN ◎ ACCUMULATE, NOT A ◌ WATCHLIST OR ◉ BUY")
    print(sep)
    print("""
  GE Aerospace is, structurally, one of the best businesses in all of industrials — a genuine
  duopoly in commercial jet engines (CFM/LEAP dominant on the best-selling narrowbody families
  in history, GE9X exclusive on the 777X), wrapped around a multi-decade aftermarket-services
  annuity that compounds with every engine delivered, backed by a deep military-engine
  franchise, a record ~$175B backlog, and a meaningfully de-levered, net-cash balance sheet.
  Despite a multi-year re-rating that has taken the stock to roughly two-thirds up its 52-week
  range at ~27x forward earnings, the bottom-up math still lands close to balanced — Ratio B
  of 1.03x means the bear-case downside and bull-case upside are now roughly mirror images of
  each other. For a franchise this structurally advantaged, "roughly balanced risk/reward" is
  an attractive place to be adding, not waiting.

  WHAT THE MARKET ALREADY PRICES IN (at $232.00, two-thirds up the 52-week band, ~27x forward):
  • Narrowbody build rates continue their gradual recovery toward elevated, multi-year-high
    delivery levels, with supply-chain bottlenecks easing gradually rather than persisting
  • The services/aftermarket revenue mix continues its structural shift higher, compounding
    the installed-base annuity roughly as currently modeled
  • Defense programs (F-series, XA100, T901) deliver on schedule without major disruption
  • The market continues to apply a "best industrial franchise" premium multiple that already
    reflects a good chunk of the next 1-2 years of expected execution

  WHAT COULD MAKE THIS MORE THAN FAIRLY PRICED (the case for adding here rather than waiting):
  1. Narrowbody build-rate ramps accelerate meaningfully beyond current expectations as
     supply-chain bottlenecks ease faster than the market assumes — directly re-accelerating
     both new-unit deliveries and the multi-decade services tail that follows each one
  2. The services annuity compounds faster than modeled as the installed base ages into its
     highest-margin overhaul years — a flywheel effect that strengthens, not weakens, with time
  3. New defense-program wins (next-generation engine competitions, allied export programs)
     extend the multi-decade visibility of the military franchise even further
  4. The market continues to extend the "elite industrial compounder" premium, recognizing the
     durability of the engine-plus-services model as deserving of a structurally higher
     multiple than traditional cyclical industrials — the multi-year re-rate keeps going

  THE RISK (the honest read on where this sits):
  • The stock has already re-rated substantially — at ~27x forward earnings and roughly
    two-thirds up its 52-week range, there is genuinely less margin of safety than at any
    point in the post-spinoff "GE Aerospace" pure-play story to date
  • Commercial aerospace remains a genuinely cyclical, supply-chain-constrained industry —
    persistent titanium/forging/casting bottlenecks have periodically gated deliveries
    industry-wide, a structural risk largely outside the company's direct control
  • A meaningful air-travel demand shock (macro recession, fuel-price spike, geopolitical
    disruption) would directly pressure both new-unit deliveries and the services growth the
    market now expects — and premium-multiple stocks tend to compress hardest when cycles turn

  WHAT MAKES THIS AN ACCUMULATE RATHER THAN MERELY A WATCHLIST:
  • The bottom-up math is genuinely close to balanced (Ratio B 1.03x) — this isn't a "wait for
    a much better price" setup, it's a "the price already roughly reflects a fair trade-off
    between the bull and bear cases for one of the best franchises in industrials" setup
  • The structural moat is not just intact but arguably strengthening — the
    engine-plus-services annuity model gets MORE valuable as the installed base grows, and the
    record ~$175B backlog provides multi-year visibility most industrials simply lack
  • The de-levered, net-cash balance sheet and Culp operating-model credibility provide real
    downside ballast — this is "great business near a fair price," not "fragile business that
    merely looks cheap"
  • Even the EPP-floor and conservative-2yr math (multiple holds roughly flat to modestly
    compressed, services compound as expected) keeps the downside case to "underperform for a
    while at a still-strong business," not "permanent capital impairment" — exactly the kind of
    risk profile that justifies building a position now rather than waiting on the sidelines

  POSITION SIZING GUIDANCE:
  • ACCUMULATE — a name to build a position in steadily here, adding more aggressively on any
    pullback toward $195-215 (where Ratio B would move toward the BUY range) rather than
    waiting for that pullback to materialize before starting
  • Watch for: narrowbody build-rate trajectories and supply-chain commentary (the dominant
    near-term swing factor), services/aftermarket revenue-mix trends (the long-term
    compounding signal), defense-program updates, and any broad-market multiple-compression
    episode that would offer an even better entry into a genuinely durable franchise
""")

    print(SEP)
    print(f"""
SUMMARY: GE ◎ ACCUMULATE — Ratio B 1.03× (25.9% downside / 25.0% upside, roughly balanced). \
A PURE-PLAY JET-ENGINE DUOPOLY WITH A MULTI-DECADE INSTALLED-BASE ANNUITY — A PREMIUM \
FRANCHISE AT A FAIR-TO-ATTRACTIVE PRICE: trading at $232.00 (52-wk range $172-268, roughly \
two-thirds up the range — meaningfully re-rated as the post-spin pure-play story has taken \
hold) on the back of genuine duopoly economics in commercial jet engines (CFM/LEAP dominant \
on the Boeing 737 MAX and Airbus A320neo — the best-selling aircraft families in history; \
GE9X exclusive on the 777X) wrapped around a multi-decade aftermarket-services annuity (~70% \
of commercial-engine revenue, 20-30+ years of high-margin recurring cash flow per engine \
across a ~45,000-engine installed base). RECORD VISIBILITY: ~$175B commercial-and-defense \
backlog, deep US/allied military-engine franchise (F404/F414, F110, XA100, T901), and a \
meaningfully de-levered, net-cash balance sheet under CEO Larry Culp's credible lean \
operating model. THE HONEST RISK: at ~27x forward earnings and roughly two-thirds up its \
52-week range, the stock has already re-rated substantially — leaving less margin of safety, \
while commercial aerospace remains genuinely cyclical and supply-chain-constrained \
(persistent titanium/forging/casting bottlenecks). Consensus 'Buy/Strong Buy' (~21 of 29 \
analysts), PT ~$255 (range $210-300). Conservative 2yr (modest-compression floor case): EPS \
$8.55 x 24.0x + $2.56 div = $207.76 -> -10.4% — BULL/XBULL require either accelerating \
delivery/services growth OR continued multiple expansion toward 'elite compounder' levels. \
THE BOTTOM-UP MATH IS GENUINELY CLOSE TO BALANCED FOR ONE OF THE BEST FRANCHISES IN \
INDUSTRIALS: build a position steadily here, adding more aggressively on any pullback toward \
$195-215. Bear $172 · Base $232 · Bull $290 · XBull $330."""
    )

    print(f"SIGNAL: {SIGNAL_TEXT} (pure-play jet-engine duopoly with a multi-decade aftermarket-services annuity, now trading at a premium multiple that already prices in a continuation of the current upcycle) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
