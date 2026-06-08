"""
Devon Energy Corporation (NYSE: DVN)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◉ BUY  |  Ratio B: 0.74×  |  EPP Gap: +199.0%

A MULTI-BASIN US SHALE CONSOLIDATOR, GENUINELY SHAREHOLDER-FIRST, TRADING NEAR A CYCLICAL TROUGH
Trading at $34.80 (52-week range $26.40-46.90, roughly a third up its range — a name that has
been cyclically de-rated alongside the broader US shale complex into a genuine value zone) on the back of a genuinely
diversified, multi-basin US onshore portfolio (Delaware Basin anchor, plus Eagle Ford,
Anadarko/STACK, Powder River, and Williston positions) assembled and high-graded through a
series of disciplined bolt-on combinations (most recently Grayson Mill and the earlier
WPX Energy merger). Devon was an early adopter — and remains a leading proponent — of the
"fixed-plus-variable" dividend framework that has become the template for US E&P shareholder
returns: a smaller, more durable base dividend topped up by a variable component tied
directly to free cash flow generation, layered with an active opportunistic buyback program.

The honest tension: DVN remains fundamentally a leveraged, multi-basin US oil & gas producer
whose earnings and cash-return capacity are directly geared to commodity prices it does not
control — and the variable-dividend framework, while shareholder-friendly on the way up,
mechanically shrinks distributions in a downturn exactly when income-oriented holders may
want them most. Multi-basin diversification reduces single-asset risk but does not eliminate
commodity-price risk, and at ~9-10x depressed forward earnings the stock trades at a genuine
discount to where best-in-class, single-basin Permian peers command premiums — a "good but
not best-in-class operator, priced accordingly" setup with real room for multiple normalization
if execution continues to track well.

Conviction: HIGH on the structural diversification-and-capital-discipline thesis (Devon's
multi-basin high-grading and shareholder-first framework are genuinely durable, proven across
multiple cycles — not promotional artifacts); MODERATE on near-term timing given oil-price
sensitivity remains the dominant swing factor — but Ratio B lands solidly in BUY territory,
reflecting a name whose downside is already meaningfully compressed (multi-basin
diversification, an investment-grade balance sheet, disciplined capital allocation, and a
price that has already absorbed much of the cyclical de-rating) against an upside that is
sharply asymmetric the moment commodity prices even stabilize, let alone firm.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "DVN"
COMPANY         = "Devon Energy Corporation"
SECTOR          = "Oil & Gas E&P · Multi-Basin US Onshore (Delaware, Eagle Ford, Anadarko/STACK, Powder River, Williston) · NYSE: DVN"
SECTOR_GROUP    = "Energy"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 34.80    # June 2026, roughly a third up the 52-week range
ANNUAL_DIV      = 1.32     # Fixed-plus-variable framework combined run-rate; yield ~3.8%
SHARES_OUT_B    = 0.635    # ~635mm shares outstanding
MARKET_CAP_B    = 22.1     # CURRENT_PRICE × SHARES_OUT_B
FW52_HIGH       = 46.90
FW52_LOW        = 26.40

# ── FY2025 FULL-YEAR FINANCIALS ─────────────────────────────────────────────
REVENUE_FY2025_B           = 16.4
ADJ_NET_INCOME_FY2025_B    = 2.55
ADJ_EPS_FY2025             = 4.05
OCF_FY2025_B               = 6.05
FCF_FY2025_B               = 2.35
PRODUCTION_MBOED           = 825   # ~825 Mboe/d, post-Grayson Mill combined run-rate
ADJ_EPS_YOY_PCT            = -11   # Lower realized commodity prices YoY partially offset by Grayson Mill accretion + cost discipline

# ── MULTI-BASIN PORTFOLIO ─────────────────────────────────────────────────────
DELAWARE_BASIN_SHARE_PCT    = 53.0   # Anchor asset — Delaware (Permian) production share
OTHER_BASINS_NOTE           = "Eagle Ford, Anadarko/STACK, Powder River, and Williston (post-Grayson Mill) round out a genuinely diversified multi-basin US onshore portfolio — reducing single-asset/single-basin concentration risk relative to pure-play peers"
PORTFOLIO_HIGH_GRADING_NOTE = "A series of disciplined bolt-on combinations and divestitures (the 2021 WPX Energy merger-of-equals, the 2024 Grayson Mill Williston acquisition, and ongoing non-core divestitures) has steadily high-graded the portfolio toward its highest-return inventory"

# ── FIXED-PLUS-VARIABLE DIVIDEND FRAMEWORK ───────────────────────────────────
FIXED_DIVIDEND_ANNUAL       = 0.96   # $0.24/qtr fixed/base dividend
VARIABLE_DIVIDEND_NOTE      = "Devon was an early architect of the 'fixed-plus-variable' dividend template that has become the standard for US E&P shareholder returns — a smaller, durable base payout topped up by a variable component paid directly out of quarterly free cash flow"
FRAMEWORK_RISK_NOTE         = "The mechanical honesty of the framework cuts both ways: distributions scale up attractively in strong commodity environments, but also mechanically shrink in downturns — precisely when income-oriented holders may most want stability"
BUYBACK_AUTHORIZATION_B     = 5.0    # Outstanding repurchase authorization
SHARE_COUNT_REDUCTION_NOTE  = "An active, opportunistic buyback program has steadily reduced the share count alongside the dividend framework — a genuine 'both levers' approach to capital return that few mid-cap E&P peers can match in consistency"

# ── BALANCE SHEET / CAPITAL DISCIPLINE ────────────────────────────────────────
NET_DEBT_B                  = 5.7
NET_DEBT_TO_EBITDA          = 0.7
CREDIT_RATING_NOTE          = "Investment-grade balance sheet (Baa2/BBB range, net debt/EBITDA ~0.7x) — among the strongest, least-levered in the mid-cap E&P peer group, providing genuine resilience through commodity-price cycles"
CAPITAL_DISCIPLINE_NOTE     = "Management has consistently prioritized maintenance-level capital programs and per-share value creation over production-growth-for-its-own-sake — a discipline that has repeatedly been validated across multiple commodity cycles"

# ── ANALYST CONSENSUS ────────────────────────────────────────────────────────
EPS_FY2026E             = 4.35     # Consensus reflects moderate WTI/Henry Hub assumptions and continued Grayson Mill accretion
TRAILING_PE             = 8.6
FORWARD_PE              = 8.0
CONSENSUS_PT            = 41.0     # Average target ~$41 (range $32-52)
PT_LOW                  = 32.0
PT_HIGH                 = 52.0
CONSENSUS_RATING        = "Buy / Hold (mixed)"
ANALYST_RATING_NOTE     = "~16 Buy / 11 Hold / 1 Sell of ~28 analysts; consensus PT ~$41 (range $32-52) — broadly constructive on execution, genuinely split on near-term commodity-price timing"

# ── SCENARIOS ────────────────────────────────────────────────────────────────
# BEAR  $25: A sustained oil-and-gas-price downturn (WTI sliding toward the high-$40s/
#            low-$50s, Henry Hub remaining structurally weak) that mechanically shrinks the
#            variable-dividend component toward the fixed-only floor, slows buyback pace, and
#            triggers a multiple-compression episode characteristic of leveraged, multi-basin
#            E&P names in a panic. Roughly the lower quarter of the 52-week range — the
#            investment-grade balance sheet (~0.7x net debt/EBITDA) provides real downside
#            ballast (this is not a name that goes to zero), but a genuine commodity-driven
#            drawdown nonetheless.
#
# BASE  $35: Roughly where the stock sits today — oil and gas prices stay in a moderate,
#            range-bound band (WTI $60-70, Henry Hub $3.00-3.75), Grayson Mill integration
#            and synergy capture continue roughly on plan, the fixed-plus-variable framework
#            pays out near its current combined run-rate, and the market continues to apply a
#            "good but not best-in-class operator" discount to the stock relative to premium
#            single-basin Permian peers. "Consensus PT ~$41" only partially realized.
#
# BULL  $48: Oil and gas prices firm meaningfully (WTI sustaining $75-85, Henry Hub above
#            $4.00 on LNG-driven demand growth), the variable dividend re-accelerates toward
#            prior-cycle highs, buybacks run at an elevated pace on management's view that the
#            stock remains undervalued, AND the market begins to grant the high-graded,
#            post-Grayson-Mill multi-basin portfolio a premium multiple closer to that of
#            best-in-class single-basin Permian peers — a re-rating the operating metrics have
#            increasingly supported but the "diversified-but-not-best" perception has so far
#            suppressed.
#
# XBULL $58: Full structural-premium thesis — Devon's multi-basin portfolio proves out as a
#            genuine structural advantage (smoother free-cash-flow generation through
#            commodity cycles than single-basin peers), oil and gas prices stay structurally
#            firm, buybacks at scale meaningfully shrink the float, AND the market definitively
#            re-rates the combined entity as "the multi-basin compounder that should command a
#            premium for diversification, not a discount" — the scenario in which the
#            shareholder-first framework finally earns the multiple its consistency has long
#            argued for. Requires several structural and cyclical tailwinds to align
#            simultaneously — high-conviction, lower-probability outcome.
BEAR    = 25.0
BASE    = 35.0
BULL    = 48.0
XBULL   = 58.0

# ── EPP (EARNINGS POWER PRICE) ───────────────────────────────────────────────
# Trough scenario: even disciplined, diversified multi-basin E&P names see earnings collapse
# in a genuine commodity-price crash — Devon itself saw adjusted earnings compress sharply
# during the 2020 COVID-driven WTI collapse and the 2015-16 downcycle despite its scale and
# capital discipline. EPS_TROUGH reflects a severe, multi-quarter commodity-downturn scenario,
# well below the FY2025 print of $4.05, and PE_TROUGH reflects the discount multiple leveraged
# multi-basin E&P names receive in a panic — even disciplined, investment-grade operators.
EPS_TROUGH  = 0.97
PE_TROUGH   = 12.0
EPP         = EPS_TROUGH * PE_TROUGH   # = $11.64

# ── SCA: STRUCTURAL COMPETITIVE ADVANTAGE ───────────────────────────────────
# DVN's moat blends genuine multi-basin diversification (smoother through-cycle cash flow than
# single-asset peers), a disciplined, repeatedly-validated high-grading and capital-allocation
# culture, an investment-grade balance sheet that is among the strongest in the mid-cap E&P
# peer group, and a genuinely shareholder-first, proven fixed-plus-variable capital-return
# framework that has become the industry template. The offsets: the variable-dividend
# mechanism mechanically amplifies cash-return cyclicality, and the portfolio — while
# diversified — still lacks the single-basin scale and cost-curve position of the very best
# pure-play Permian operators.

SCA_FACTORS = {
    # Factor                                            : (score,  weight)
    "multi_basin_diversification_and_high_grading"     : (+0.30,  0.17),  # Genuine multi-basin diversification reduces single-asset risk; repeated, disciplined high-grading via WPX/Grayson Mill
    "shareholder_first_fixed_plus_variable_framework"  : (+0.30,  0.16),  # Industry-template capital-return framework + active buybacks — proven across multiple cycles
    "investment_grade_balance_sheet_and_low_leverage"  : (+0.30,  0.15),  # ~0.7x net debt/EBITDA — among the strongest, least-levered in the mid-cap E&P peer group
    "disciplined_capital_allocation_culture"           : (+0.25,  0.14),  # Maintenance-level capital programs, per-share-value focus — repeatedly validated across cycles
    "valuation_discount_to_premium_permian_peers"      : (+0.15,  0.12),  # ~8-9x forward — genuine room for multiple normalization toward premium single-basin peer levels
    "variable_dividend_cash_return_cyclicality"        : (-0.25,  0.13),  # The framework mechanically shrinks distributions in downturns — precisely when holders may want stability most
    "commodity_price_and_multi_basin_execution_risk"   : (-0.20,  0.13),  # Genuinely geared to commodity prices it doesn't control; multi-basin operations carry real execution complexity
}

SCA_NET  = sum(score * weight for score, weight in SCA_FACTORS.values())
# SCA_NET = 0.30×0.17 + 0.30×0.16 + 0.30×0.15 + 0.25×0.14 + 0.15×0.12 + (-0.25)×0.13 + (-0.20)×0.13
# SCA_NET ≈ 0.051 + 0.048 + 0.045 + 0.035 + 0.018 - 0.0325 - 0.026 = 0.1385

SCA_SCALE = 0.45  # Fixed framework parameter

# ── 6 PROXY SIGNALS ──────────────────────────────────────────────────────────
# Signal   (score 1–4, weight)
# 1=BEAR, 1.5=BEAR+, 2=BASE, 2.5=BASE+, 3=BULL, 3.5=BULL+, 4=XBULL

SIGNALS = {
    # Devon's genuinely diversified multi-basin US onshore portfolio (Delaware anchor plus
    # Eagle Ford, Anadarko/STACK, Powder River, and Williston) reduces single-asset/single-
    # basin concentration risk relative to pure-play peers — and a series of disciplined
    # bolt-on combinations (WPX merger, Grayson Mill acquisition) has steadily high-graded the
    # portfolio toward its highest-return inventory.
    "multi_basin_diversification_and_portfolio_quality": (3.0, 0.18),

    # Devon was an early architect of the fixed-plus-variable dividend framework that has
    # become the industry template for US E&P shareholder returns, layered with an active,
    # opportunistic buyback program — a genuinely proven, "both levers" approach to capital
    # return that few mid-cap E&P peers can match in consistency across multiple cycles.
    "shareholder_first_capital_return_framework": (3.0, 0.16),

    # The investment-grade balance sheet (~0.7x net debt/EBITDA, Baa2/BBB-range ratings) is
    # among the strongest and least-levered in the mid-cap E&P peer group — a genuine
    # structural advantage that provides real resilience through commodity-price downturns
    # and funds continued capital returns even in softer environments.
    "investment_grade_balance_sheet_strength": (3.0, 0.15),

    # The honest core-business risk: DVN remains a leveraged, multi-basin US oil & gas
    # producer whose earnings and cash-return capacity are directly geared to commodity prices
    # it does not control — and the variable-dividend mechanism mechanically amplifies that
    # cyclicality, shrinking distributions in downturns exactly when holders may want stability.
    "commodity_price_exposure_and_variable_dividend_cyclicality": (2.0, 0.20),

    # At ~8-9x depressed forward earnings, Devon trades at a genuine discount to where
    # best-in-class, single-basin Permian peers command premiums — a "good but not
    # best-in-class operator, priced accordingly" setup that leaves real room for multiple
    # normalization if execution and portfolio high-grading continue to track well.
    "valuation_discount_to_premium_peers_normalization_potential": (3.0, 0.16),

    # Grayson Mill integration and the broader high-grading program continue to track on plan,
    # with management consistently demonstrating maintenance-capital discipline and a focus on
    # per-share value creation over growth-for-its-own-sake — a culture that has repeatedly
    # been validated across multiple commodity cycles and supports the through-cycle thesis.
    "execution_and_capital_discipline_track_record": (3.0, 0.15),
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

# Conservative 2yr: FY2026E EPS (consensus, reflecting moderate commodity-price assumptions) ×
# a multiple roughly in line with the current ~8.0x forward — pure compounding/execution test,
# no premium-multiple-normalization credit required
PE_CONSERVATIVE = 8.0
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
    print("  MULTI-BASIN PORTFOLIO")
    print(sep)
    print(f"  Delaware Basin production share: ~{DELAWARE_BASIN_SHARE_PCT:.0f}%")
    print(f"  {OTHER_BASINS_NOTE}")
    print(f"  {PORTFOLIO_HIGH_GRADING_NOTE}")

    print(f"\n{sep}")
    print("  FIXED-PLUS-VARIABLE DIVIDEND FRAMEWORK")
    print(sep)
    print(f"  Fixed dividend: ${FIXED_DIVIDEND_ANNUAL:.2f}/yr  |  Combined run-rate (incl. variable): ~${ANNUAL_DIV:.2f}/yr")
    print(f"  Buyback authorization outstanding: ~${BUYBACK_AUTHORIZATION_B:.1f}B")
    print(f"  {VARIABLE_DIVIDEND_NOTE}")
    print(f"  {FRAMEWORK_RISK_NOTE}")
    print(f"  {SHARE_COUNT_REDUCTION_NOTE}")

    print(f"\n{sep}")
    print("  BALANCE SHEET / CAPITAL DISCIPLINE")
    print(sep)
    print(f"  Net debt: ${NET_DEBT_B:.1f}B  |  Net debt/EBITDA: ~{NET_DEBT_TO_EBITDA:.1f}x")
    print(f"  {CREDIT_RATING_NOTE}")
    print(f"  {CAPITAL_DISCIPLINE_NOTE}")

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
        "multi_basin_diversification_and_portfolio_quality":           "Multi-basin diversification & portfolio quality",
        "shareholder_first_capital_return_framework":                  "Shareholder-first capital return framework",
        "investment_grade_balance_sheet_strength":                     "Investment-grade balance-sheet strength",
        "commodity_price_exposure_and_variable_dividend_cyclicality":  "Commodity exposure & variable-dividend cyclicality",
        "valuation_discount_to_premium_peers_normalization_potential": "Valuation discount to premium peers — normalization potential",
        "execution_and_capital_discipline_track_record":               "Execution & capital-discipline track record",
    }
    for k, (score, weight) in SIGNALS.items():
        bar = "█" * int(score * 5)
        print(f"  {labels[k]:<54}  {score:.1f}  wt={weight:.2f}  {bar}")
    print(f"  {'PROXY COMPOSITE':<54}  {PROXY_COMPOSITE:.2f}")

    print(f"\n{sep}")
    print("  SCA — STRUCTURAL COMPETITIVE ADVANTAGE")
    print(sep)
    sca_labels = {
        "multi_basin_diversification_and_high_grading":     "Multi-basin diversification & high-grading",
        "shareholder_first_fixed_plus_variable_framework":  "Shareholder-first fixed-plus-variable framework",
        "investment_grade_balance_sheet_and_low_leverage":  "Investment-grade balance sheet & low leverage",
        "disciplined_capital_allocation_culture":           "Disciplined capital-allocation culture",
        "valuation_discount_to_premium_permian_peers":      "Valuation discount to premium Permian peers",
        "variable_dividend_cash_return_cyclicality":        "Variable-dividend cash-return cyclicality",
        "commodity_price_and_multi_basin_execution_risk":   "Commodity price & multi-basin execution risk",
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
    print(f"  FY2026E EPS (consensus, reflecting moderate commodity-price assumptions): ${EPS_FY2026E:.2f}")
    print(f"  Conservative PE applied:                                            {PE_CONSERVATIVE:.1f}× (in line with the ~8.0x forward — no premium-multiple-normalization credit assumed)")
    print(f"  Target price 2yr:                                                   ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.1f}× + ${2*ANNUAL_DIV:.2f} div = ${PRICE_2YR_CONSV:.2f}")
    print(f"  2-year return:                                                      {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  Note: this is the 'commodity prices stay roughly where they are, no multiple normalization, and")
    print(f"  the market keeps applying a discount-to-premium-peers' floor case — BULL/XBULL require either")
    print(f"  firmer commodity prices OR the market starting to credit the high-graded portfolio with a premium.")

    print(f"\n{sep}")
    print("  WHY THIS IS A ◉ BUY, NOT A ◌ WATCHLIST OR ◎ ACCUMULATE")
    print(sep)
    print("""
  Devon Energy is, at its core, a leveraged, multi-basin US onshore E&P — but layered on top
  of that core are two things that genuinely differentiate it from many peers: (1) a real,
  proven multi-basin diversification (Delaware anchor plus Eagle Ford, Anadarko/STACK, Powder
  River, and Williston) that smooths through-cycle cash flow more than single-asset operators
  can, assembled and high-graded through a track record of disciplined combinations (WPX,
  Grayson Mill); and (2) a genuinely shareholder-first, industry-template fixed-plus-variable
  capital-return framework, backed by one of the strongest, least-levered balance sheets in
  the mid-cap E&P peer group. The price has already absorbed much of the cyclical de-rating —
  at roughly a third up its 52-week range and ~8-9x depressed forward earnings, a genuine
  discount to premium single-basin Permian peers, the setup is sharply asymmetric — Ratio B
  lands solidly in BUY territory.

  WHAT THE MARKET ALREADY PRICES IN (at $34.80, lower-third on the 52-week band):
  • Oil and gas prices stay in a moderate, range-bound band (WTI $60-70, Henry Hub $3.00-3.75)
  • Grayson Mill integration and portfolio high-grading continue roughly on plan
  • The fixed-plus-variable framework pays out near its current combined run-rate
  • The market continues to apply a "good but not best-in-class operator" discount relative to
    premium single-basin Permian peers — giving little credit for the diversification advantage

  WHAT COULD MAKE THIS MORE THAN FAIRLY PRICED:
  1. Oil and gas prices firm meaningfully (supply discipline, LNG-driven gas-demand growth) —
     directly re-accelerating the variable dividend, buyback pace, and FCF generation
  2. The market begins to recognize multi-basin diversification as a genuine structural
     advantage (smoother through-cycle cash flow) rather than a "lacks single-basin scale"
     knock — a re-rating that would close the gap to premium Permian-pure-play multiples
  3. Continued disciplined high-grading and bolt-on execution (in the Grayson Mill mold)
     extends the portfolio's average inventory quality and per-share value creation
  4. Buybacks at depressed multiples meaningfully reduce the share count, amplifying the
     eventual recovery's per-share impact — a genuine compounding dynamic atop the dividend

  THE RISK (the honest read on where this sits):
  • DVN remains fundamentally a leveraged, multi-basin US oil & gas producer geared directly
    to commodity prices it does not control — the dominant, unresolved swing factor
  • The variable-dividend mechanism mechanically amplifies cash-return cyclicality — payouts
    shrink toward the fixed-only floor in downturns, exactly when income-oriented holders may
    most want stability
  • Multi-basin operations carry genuine execution complexity that single-basin peers don't
    face — and the portfolio, while diversified, still lacks the single-basin scale and
    cost-curve position of the very best pure-play Permian operators
  • A sustained commodity downturn would compress earnings, slow buybacks, and pressure the
    multiple simultaneously — the kind of multi-factor squeeze leveraged E&P names have seen
    in past downcycles

  WHAT MAKES THIS A BUY RATHER THAN MERELY AN ACCUMULATE:
  • The downside is already meaningfully compressed: genuine multi-basin diversification, an
    investment-grade balance sheet (~0.7x net debt/EBITDA — among the strongest in the peer
    group), disciplined capital allocation, AND a price that has already absorbed much of the
    cyclical de-rating all combine to limit the realistic drawdown from here
  • The upside is sharply asymmetric relative to where the stock trades on its own multiple:
    at ~8-9x depressed forward earnings — a real discount to premium single-basin Permian
    peers — even modest commodity firming or multiple normalization toward peer levels
    produces outsized equity returns; this is "buy the discount before it closes," not
    "wait for confirmation that it's closing"
  • Even the EPP-floor and conservative-2yr math (commodity-flat, no premium-multiple credit,
    discount multiple applied) produces a solidly positive expected return — the setup
    doesn't require heroics, only patience for a normalization history says is likely

  POSITION SIZING GUIDANCE:
  • BUY — a name to build a full position in at current levels; the asymmetry (compressed
    downside near a cyclical trough vs. sharply convex upside to commodity stabilization or
    multiple normalization) is exactly the kind of setup this framework is designed to flag
  • Watch for: WTI/Henry Hub price trends (the dominant swing factor), variable-dividend
    trends as a read on management's confidence in the FCF outlook, Grayson Mill synergy-
    capture updates, buyback pace and pricing, and any signs of the market beginning to
    narrow the multiple gap to premium single-basin Permian peers
""")

    print(SEP)
    print(f"""
SUMMARY: DVN ◉ BUY — Ratio B 0.74× (28.2% downside / 37.9% upside). A MULTI-BASIN US SHALE \
CONSOLIDATOR, GENUINELY SHAREHOLDER-FIRST, TRADING NEAR A CYCLICAL TROUGH: trading at $34.80 \
(52-wk range $26.40-46.90, roughly a third up the range — cyclically de-rated into a genuine \
value zone) on a genuinely diversified multi-basin US onshore portfolio (Delaware anchor \
~53% plus Eagle Ford, Anadarko/STACK, Powder River, and Williston) assembled and high-graded \
through disciplined combinations (WPX merger, Grayson Mill acquisition). SHAREHOLDER-FIRST \
FRAMEWORK: an early architect of the now-industry-template fixed-plus-variable dividend \
(combined run-rate ~$1.32/yr) layered with an active ~$5.0B buyback authorization — both \
levers, consistently pulled across cycles. INVESTMENT-GRADE STRENGTH: ~0.7x net debt/EBITDA \
— among the strongest, least-levered balance sheets in the mid-cap E&P peer group, funding \
continued returns even in softer environments. THE HONEST RISK: DVN remains a leveraged, \
multi-basin producer geared to commodity prices it doesn't control, and the variable- \
dividend mechanism mechanically shrinks payouts in downturns exactly when holders may want \
stability most — multi-basin operations also carry real execution complexity single-basin \
peers avoid. Consensus 'Buy/Hold (mixed)' (~16 of 28 analysts Buy), PT ~$41 (range $32-52). \
Conservative 2yr (commodity-flat, discount-multiple floor case): EPS $4.35 x 8.0x + $2.64 \
div = $37.44 -> +7.6% — BULL/XBULL require either firmer commodity prices OR the market \
narrowing the multiple gap to premium single-basin Permian peers. THE PRICE HAS ALREADY \
ABSORBED MUCH OF THE CYCLICAL DE-RATING: compressed downside (multi-basin diversification, \
investment-grade balance sheet, disciplined capital allocation) against sharply asymmetric \
upside (a good operator priced like an average one, ~8-9x forward) — build a full position \
at current levels. Bear $25 · Base $35 · Bull $48 · XBull $58."""
    )

    print(f"SIGNAL: {SIGNAL_TEXT} (multi-basin US shale consolidator with a genuinely shareholder-first fixed-plus-variable capital-return framework, trading at a discount to premium Permian peers) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
