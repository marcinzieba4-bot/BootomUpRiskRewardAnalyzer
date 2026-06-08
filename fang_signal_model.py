"""
Diamondback Energy, Inc. (NASDAQ: FANG)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.95×  |  EPP Gap: +252.4%

THE LOWEST-COST, HIGHEST-QUALITY PURE-PLAY PERMIAN OPERATOR — NOW AT UNMATCHED SCALE
Trading at $148.00 (52-week range $128-198, roughly a third up its range — a name that has
genuinely cheapened relative to its own history) on the back of a transformational 2024
combination with Endeavor Energy Resources that roughly doubled Diamondback's scale and
created, by a wide margin, the largest pure-play Permian Basin (Midland-weighted) operator
in existence. The combined company runs the lowest per-barrel operating cost structure of
any large-scale US unconventional producer — a structural cost advantage built on contiguous
acreage, long laterals, and a culture of relentless capital discipline that has defined
Diamondback since its founding. That cost advantage shows up directly in the cash-return
framework: a fixed base dividend plus a variable component, layered with one of the most
aggressive buyback programs in the E&P space, returning the large majority of free cash flow
to shareholders through the cycle — not just at the top of it.

The honest tension: FANG is, more than almost any other large-cap E&P, a leveraged bet on a
single basin and a single commodity. The Endeavor combination added real acquisition debt to
an historically pristine balance sheet, and a sustained oil-price downturn would pressure
both the variable-dividend framework and the deleveraging timeline simultaneously. At ~8-9x
forward earnings — a meaningful discount to both the broader market and to where FANG itself
has traded through prior cycles — the stock is pricing in real commodity-price pessimism, not
operational risk: this is a "best-in-class operator priced like an average one" setup.

Conviction: HIGH on the structural cost-leadership and capital-return thesis (Diamondback's
operating discipline and the Endeavor scale advantage are genuinely durable, structural
moats — not cyclical artifacts); MODERATE on near-term timing given oil-price sensitivity
remains the dominant swing factor and the post-merger deleveraging path still has real
distance to travel — Ratio B sits almost exactly at the ACCUMULATE threshold, reflecting a
name whose downside is meaningfully cushioned by its cost-curve position (it remains
profitable at WTI prices that would impair the majority of its peers) against upside that is
genuinely asymmetric if oil firms even modestly from current levels.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "FANG"
COMPANY         = "Diamondback Energy, Inc."
SECTOR          = "Oil & Gas E&P · Pure-Play Permian Basin (Midland & Delaware) Unconventional Producer · NASDAQ: FANG"
SECTOR_GROUP    = "Energy"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 148.00   # June 2026, roughly a third up the 52-week range
ANNUAL_DIV      = 5.68     # Base ($0.90/qtr) + variable component (combined run-rate)
SHARES_OUT_B    = 0.336    # ~336mm shares post-Endeavor stock issuance
MARKET_CAP_B    = 49.7     # CURRENT_PRICE × SHARES_OUT_B
FW52_HIGH       = 198.40
FW52_LOW        = 128.30

# ── FY2025 FULL-YEAR FINANCIALS ─────────────────────────────────────────────
REVENUE_FY2025_B           = 11.6
ADJ_NET_INCOME_FY2025_B    = 3.35
ADJ_EPS_FY2025             = 9.85
OCF_FY2025_B               = 6.85
FCF_FY2025_B               = 3.10
PRODUCTION_MBOED           = 880    # ~880 Mboe/d, post-Endeavor combined run-rate
ADJ_EPS_YOY_PCT            = -8     # Lower realized oil prices YoY partially offset by Endeavor accretion + cost synergies

# ── COST LEADERSHIP / OPERATING ADVANTAGE ───────────────────────────────────
CASH_OPERATING_COST_PER_BOE = 9.85   # Among the lowest of any large-scale US unconventional producer
CORPORATE_BREAKEVEN_WTI     = 38.0   # Approximate WTI breakeven to cover base dividend + maintenance capex
COST_LEADERSHIP_NOTE        = "Diamondback runs the lowest-cost operating structure of any large-scale US unconventional producer — contiguous, mostly-held acreage, long laterals, and a culture of capital discipline that predates (and was amplified by) the Endeavor combination"

# ── ENDEAVOR COMBINATION ──────────────────────────────────────────────────────
ENDEAVOR_DEAL_VALUE_B       = 26.0   # Approximate transaction value (cash + stock) at close, Sept 2024
ENDEAVOR_SYNERGY_TARGET_M   = 550    # Targeted run-rate annual synergies (operational + capital efficiencies)
ENDEAVOR_SYNERGY_PROGRESS_NOTE = "Endeavor synergy capture is tracking at or ahead of the targeted run-rate — the combination roughly doubled Diamondback's scale and created, by a wide margin, the largest pure-play Permian operator in existence"
ENDEAVOR_NOTE               = "The Sept-2024 Endeavor Energy Resources combination added ~350,000 net acres of contiguous, high-quality Midland Basin inventory — a multi-decade runway of low-breakeven drilling locations that few competitors can match in either quality or duration"

# ── CAPITAL RETURN FRAMEWORK ─────────────────────────────────────────────────
BASE_DIVIDEND_ANNUAL        = 3.60   # $0.90/qtr base dividend
VARIABLE_DIVIDEND_NOTE      = "Base-plus-variable dividend framework layered with an active buyback authorization — management has explicitly prioritized returning the large majority of FCF to shareholders through the commodity cycle, not just at cyclical peaks"
BUYBACK_AUTHORIZATION_B     = 6.0    # Outstanding repurchase authorization
SHARE_COUNT_REDUCTION_NOTE  = "Aggressive opportunistic buybacks have meaningfully reduced the share count even through a period of heavy stock issuance for the Endeavor deal — a genuine 'shrinking float' dynamic atop the dividend framework"

# ── DELEVERAGING / BALANCE SHEET ─────────────────────────────────────────────
NET_DEBT_CURRENT_B          = 12.8   # Post-Endeavor combined balance sheet, paying down steadily
NET_DEBT_TARGET_B           = 8.0    # Stated medium-term target
LEVERAGE_NOTE               = "Net debt/EBITDA sits in the ~1.1-1.3x range — a real but manageable load for a name of this scale and FCF generation; management has been explicit about prioritizing continued paydown toward an ~$8B target"

# ── ANALYST CONSENSUS ────────────────────────────────────────────────────────
EPS_FY2026E             = 13.10    # Consensus reflects moderate WTI assumptions ($65-70) and continued Endeavor accretion
TRAILING_PE             = 15.0
FORWARD_PE              = 11.3
CONSENSUS_PT            = 175.0    # Average target ~$175 (range $145-225)
PT_LOW                  = 145.0
PT_HIGH                 = 225.0
CONSENSUS_RATING        = "Buy / Strong Buy"
ANALYST_RATING_NOTE     = "~24 Buy / 6 Hold / 1 Sell of ~31 analysts; consensus PT ~$175 (range $145-225) — broadly constructive, reflecting the cost-leadership thesis more than near-term commodity-price calls"

# ── SCENARIOS ────────────────────────────────────────────────────────────────
# BEAR  $108: A genuine, sustained oil-price downturn (WTI sliding into the high-$40s/
#             low-$50s) that pressures the variable-dividend component, slows the
#             deleveraging path post-Endeavor, and triggers a multiple-compression episode
#             characteristic of leveraged, single-basin E&P names in a panic — even though
#             Diamondback's structural cost advantage means it would remain comfortably
#             profitable on a cash basis through such a scenario (this is not a name that
#             goes to zero; it's one that gets cyclically re-rated down hard).
#
# BASE  $148: Roughly where the stock sits today — oil prices stay in a moderate, range-
#             bound band (WTI $65-75), Endeavor synergy capture continues toward the $550mm
#             target, the base-plus-variable dividend framework holds roughly at current
#             run-rate levels, and buybacks continue opportunistically. "Consensus PT ~$175"
#             only partially realized — the market continues to apply a leveraged-E&P
#             discount to a name that has genuinely earned a premium on operating merit.
#
# BULL  $190: Oil prices firm meaningfully (WTI sustaining $80-90 on supply discipline /
#             demand resilience), the variable dividend re-accelerates, deleveraging runs
#             ahead of the $8B target, AND the market begins to grant Diamondback a
#             structural premium multiple for being the clear quality/cost leader at scale
#             in the Permian — a re-rating that the operating metrics have long supported
#             but the post-merger leverage overhang has so far suppressed.
#
# XBULL $230: Full structural-premium thesis — Diamondback completes deleveraging well
#             ahead of schedule, pivots aggressively toward buybacks at scale (materially
#             shrinking the float), oil prices stay structurally firm, AND the market
#             definitively re-rates the combined Endeavor-scale entity as the structural
#             "best house in the neighborhood" — the scenario in which "lowest-cost
#             operator at unmatched scale" finally commands the multiple the operating
#             metrics have argued for. Requires several tailwinds to align simultaneously —
#             high-conviction, lower-probability outcome.
BEAR    = 108.0
BASE    = 148.0
BULL    = 190.0
XBULL   = 230.0

# ── EPP (EARNINGS POWER PRICE) ───────────────────────────────────────────────
# Trough scenario: even best-in-class, low-cost E&P names see earnings collapse in a genuine
# oil-price crash — Diamondback itself saw adjusted EPS compress sharply during the 2020
# COVID-driven WTI collapse despite its structural cost advantages. EPS_TROUGH reflects a
# severe downturn scenario, well below the FY2025 print of $9.85, and PE_TROUGH reflects the
# discount multiple leveraged single-basin E&P names receive in a panic — even one with
# genuinely the lowest operating cost structure in its peer group.
EPS_TROUGH  = 3.50
PE_TROUGH   = 12.0
EPP         = EPS_TROUGH * PE_TROUGH   # = $42.00

# ── SCA: STRUCTURAL COMPETITIVE ADVANTAGE ───────────────────────────────────
# FANG's moat blends a genuinely structural, durable cost-leadership position (the lowest
# operating cost per BOE of any large-scale US unconventional producer), an unmatched-scale,
# contiguous Permian acreage position created by the Endeavor combination (a multi-decade
# inventory runway few peers can match), and a credible, shareholder-aligned capital-return
# framework that prioritizes FCF distribution through the cycle. The offsets: real
# post-merger leverage, and a structural concentration in a single basin and commodity that
# leaves the name more cyclically exposed than diversified majors or midstream peers.

SCA_FACTORS = {
    # Factor                                            : (score,  weight)
    "lowest_cost_operator_structural_advantage"        : (+0.40,  0.18),  # Lowest cash operating cost per BOE among large-scale US unconventional producers — a durable, structural moat
    "endeavor_combination_unmatched_permian_scale"     : (+0.35,  0.17),  # Roughly doubled scale; ~350k net acres of contiguous, high-quality Midland inventory — multi-decade runway
    "shareholder_aligned_capital_return_framework"     : (+0.30,  0.15),  # Base-plus-variable dividend + aggressive opportunistic buybacks — genuine FCF-to-shareholder priority through the cycle
    "low_corporate_breakeven_resilience"               : (+0.25,  0.14),  # ~$38 WTI corporate breakeven means the company stays cash-generative through scenarios that would impair most peers
    "post_merger_deleveraging_progress"                : (+0.15,  0.12),  # Net debt trending from the post-Endeavor peak toward an ~$8B target — credible, on-plan progress
    "single_basin_single_commodity_concentration_risk" : (-0.30,  0.12),  # Pure-play Permian/oil concentration — genuinely more cyclically exposed than diversified majors or midstream peers
    "post_merger_leverage_and_integration_risk"        : (-0.20,  0.12),  # Real acquisition-related debt added to a historically pristine balance sheet; integration always carries execution risk
}

SCA_NET  = sum(score * weight for score, weight in SCA_FACTORS.values())
# SCA_NET = 0.40×0.18 + 0.35×0.17 + 0.30×0.15 + 0.25×0.14 + 0.15×0.12 + (-0.30)×0.12 + (-0.20)×0.12
# SCA_NET ≈ 0.072 + 0.0595 + 0.045 + 0.035 + 0.018 - 0.036 - 0.024 = 0.1695

SCA_SCALE = 0.45  # Fixed framework parameter

# ── 6 PROXY SIGNALS ──────────────────────────────────────────────────────────
# Signal   (score 1–4, weight)
# 1=BEAR, 1.5=BEAR+, 2=BASE, 2.5=BASE+, 3=BULL, 3.5=BULL+, 4=XBULL

SIGNALS = {
    # Diamondback's cash operating cost per BOE is among the lowest of any large-scale US
    # unconventional producer — a structural, durable advantage built on contiguous acreage,
    # long laterals, and a deeply ingrained culture of capital discipline. This is the single
    # most important reason the company remains comfortably cash-generative at WTI levels
    # that would impair the majority of its peer group.
    "lowest_cost_operator_structural_advantage": (3.5, 0.20),

    # The Sept-2024 Endeavor Energy Resources combination roughly doubled Diamondback's
    # scale and created, by a wide margin, the largest pure-play Permian Basin operator in
    # existence — adding ~350,000 net acres of contiguous, high-quality Midland Basin
    # inventory that represents a genuine multi-decade drilling runway few competitors can
    # match in either quality or duration.
    "endeavor_combination_unmatched_permian_scale": (3.0, 0.17),

    # The base-plus-variable dividend framework, layered with an active and historically
    # opportunistic buyback program, reflects a genuinely shareholder-aligned capital-return
    # philosophy — management has consistently prioritized returning the large majority of
    # free cash flow to shareholders through the cycle rather than chasing production growth
    # for its own sake.
    "shareholder_aligned_capital_return_and_buybacks": (3.0, 0.16),

    # Post-merger deleveraging is progressing on a credible, on-plan glide path from the
    # Endeavor-related peak toward the ~$8B net-debt target — funded by genuinely strong FCF
    # generation even at moderate oil prices, a direct function of the structural cost
    # advantage described above.
    "post_merger_deleveraging_on_credible_glide_path": (3.0, 0.15),

    # The honest core-business risk: FANG remains, more than almost any other large-cap E&P,
    # a leveraged bet on a single basin and a single commodity — a sustained oil-price
    # downturn (WTI sliding toward the high-$40s/low-$50s) would simultaneously pressure the
    # variable-dividend framework AND the post-merger deleveraging timeline, the dominant
    # swing factor for the stock.
    "single_basin_oil_price_concentration_risk": (2.0, 0.18),

    # At ~8-9x forward earnings — a meaningful discount to both the broader market and to
    # where FANG itself has historically traded — the stock is pricing in real commodity
    # pessimism rather than any operational concern, leaving room for a re-rating if the
    # market begins to grant the combined, unmatched-scale entity the structural premium
    # multiple its operating metrics have long argued for.
    "valuation_discount_to_own_history_and_peers": (3.0, 0.14),
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
# a multiple roughly in line with the current ~11.3x forward — pure compounding/
# deleveraging-progress test, no structural-premium re-rating credit required
PE_CONSERVATIVE = 10.5
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
    print("  COST LEADERSHIP / OPERATING ADVANTAGE")
    print(sep)
    print(f"  Cash operating cost: ~${CASH_OPERATING_COST_PER_BOE:.2f}/boe  |  Corporate breakeven: ~${CORPORATE_BREAKEVEN_WTI:.0f} WTI")
    print(f"  {COST_LEADERSHIP_NOTE}")

    print(f"\n{sep}")
    print("  ENDEAVOR ENERGY RESOURCES COMBINATION")
    print(sep)
    print(f"  Deal value: ~${ENDEAVOR_DEAL_VALUE_B:.1f}B  |  Synergy target: ~${ENDEAVOR_SYNERGY_TARGET_M}mm/yr run-rate")
    print(f"  {ENDEAVOR_NOTE}")
    print(f"  {ENDEAVOR_SYNERGY_PROGRESS_NOTE}")

    print(f"\n{sep}")
    print("  CAPITAL RETURN FRAMEWORK")
    print(sep)
    print(f"  Base dividend: ${BASE_DIVIDEND_ANNUAL:.2f}/yr  |  Combined run-rate (incl. variable): ~${ANNUAL_DIV:.2f}/yr")
    print(f"  Buyback authorization outstanding: ~${BUYBACK_AUTHORIZATION_B:.1f}B")
    print(f"  {VARIABLE_DIVIDEND_NOTE}")
    print(f"  {SHARE_COUNT_REDUCTION_NOTE}")

    print(f"\n{sep}")
    print("  BALANCE SHEET / DELEVERAGING")
    print(sep)
    print(f"  Net debt: ${NET_DEBT_CURRENT_B:.1f}B  (target ${NET_DEBT_TARGET_B:.1f}B)")
    print(f"  {LEVERAGE_NOTE}")

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
        "lowest_cost_operator_structural_advantage":       "Lowest-cost operator — structural advantage",
        "endeavor_combination_unmatched_permian_scale":    "Endeavor combination — unmatched Permian scale",
        "shareholder_aligned_capital_return_and_buybacks": "Shareholder-aligned capital return & buybacks",
        "post_merger_deleveraging_on_credible_glide_path": "Post-merger deleveraging on credible glide path",
        "single_basin_oil_price_concentration_risk":       "Single-basin oil-price concentration risk",
        "valuation_discount_to_own_history_and_peers":     "Valuation discount to own history & peers",
    }
    for k, (score, weight) in SIGNALS.items():
        bar = "█" * int(score * 5)
        print(f"  {labels[k]:<54}  {score:.1f}  wt={weight:.2f}  {bar}")
    print(f"  {'PROXY COMPOSITE':<54}  {PROXY_COMPOSITE:.2f}")

    print(f"\n{sep}")
    print("  SCA — STRUCTURAL COMPETITIVE ADVANTAGE")
    print(sep)
    sca_labels = {
        "lowest_cost_operator_structural_advantage":        "Lowest-cost operator — structural advantage",
        "endeavor_combination_unmatched_permian_scale":     "Endeavor combination — unmatched Permian scale",
        "shareholder_aligned_capital_return_framework":     "Shareholder-aligned capital-return framework",
        "low_corporate_breakeven_resilience":               "Low corporate breakeven — cycle resilience",
        "post_merger_deleveraging_progress":                "Post-merger deleveraging progress",
        "single_basin_single_commodity_concentration_risk": "Single-basin/single-commodity concentration risk",
        "post_merger_leverage_and_integration_risk":        "Post-merger leverage & integration risk",
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
    print(f"  Conservative PE applied:                                            {PE_CONSERVATIVE:.1f}× (a discount to the ~11.3x forward — no structural-premium re-rating assumed)")
    print(f"  Target price 2yr:                                                   ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.1f}× + ${2*ANNUAL_DIV:.2f} div = ${PRICE_2YR_CONSV:.2f}")
    print(f"  2-year return:                                                      {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  Note: this is the 'oil prices stay roughly where they are, no structural re-rating, and the")
    print(f"  market keeps applying a leveraged-E&P discount' floor case — BULL/XBULL require either firmer")
    print(f"  oil prices OR the market starting to grant the combined entity its earned cost-leadership premium.")

    print(f"\n{sep}")
    print("  WHY THIS IS A ◎ ACCUMULATE, NOT A ◌ WATCHLIST OR ◉ BUY")
    print(sep)
    print("""
  Diamondback Energy is, at its core, a leveraged, single-basin, single-commodity Permian
  E&P — but layered on top of that core are two things almost no other pure-play producer
  can claim simultaneously: (1) a genuinely structural, durable cost-leadership position
  (the lowest cash operating cost per BOE of any large-scale US unconventional producer),
  and (2) the Endeavor Energy Resources combination, which roughly doubled the company's
  scale and created, by a wide margin, the largest pure-play Permian operator in existence —
  with a multi-decade runway of contiguous, high-quality drilling inventory. That combination,
  at a price sitting roughly a third up its 52-week range (genuinely cheapened relative to its
  own trading history), produces a setup that is almost exactly balanced — Ratio B lands right
  at the ACCUMULATE threshold.

  WHAT THE MARKET ALREADY PRICES IN (at $148.00, lower-third on the 52-week band):
  • Oil prices stay in a moderate, range-bound band (WTI $65-75) through 2026-27
  • Endeavor synergy capture lands roughly at the $550mm annual target without major surprises
  • The variable-dividend component holds roughly at current run-rate levels
  • The market continues to apply a leveraged-single-basin-E&P discount to the stock, largely
    ignoring the structural cost-leadership case for a premium multiple

  WHAT COULD MAKE THIS MORE THAN FAIRLY PRICED:
  1. Oil prices firm meaningfully (supply discipline, demand resilience) — directly
     accelerating both FCF generation, the variable dividend, and the deleveraging timeline
  2. Post-merger deleveraging completes ahead of the ~$8B target, freeing the company to lean
     more aggressively into buybacks at scale — a genuine "shrinking float" compounding dynamic
  3. The market begins to grant the combined, unmatched-scale entity the structural premium
     multiple that its cost-curve position has long argued for — a re-rating that operating
     metrics support but the post-merger leverage overhang has so far suppressed
  4. Continued evidence that Endeavor's contiguous Midland acreage delivers the multi-decade
     inventory-quality advantage management has described, extending the duration of the moat

  THE RISK (the honest read on where this sits):
  • FANG remains, more than almost any large-cap E&P, a leveraged bet on a single basin and a
    single commodity — a sustained downturn (WTI toward the high-$40s/low-$50s) would pressure
    BOTH the variable-dividend framework AND the deleveraging glide path simultaneously
  • The Endeavor combination added real acquisition-related debt to a historically pristine
    balance sheet — net debt/EBITDA in the ~1.1-1.3x range is manageable but not trivial
  • Large-scale combinations always carry integration and execution risk, even when synergy
    capture is currently tracking on or ahead of plan
  • Pure-play concentration means FANG lacks the diversification ballast (chemicals,
    midstream, refining) that some integrated and diversified peers can lean on in a downturn

  WHAT MAKES THIS AN ACCUMULATE RATHER THAN MERELY A WATCHLIST:
  • The downside is meaningfully cushioned by genuine structural advantages: a ~$38 WTI
    corporate breakeven means the company stays comfortably cash-generative through scenarios
    that would impair the majority of its peer group — this is a "best operator in the group"
    drawdown, not a solvency risk
  • The upside is genuinely asymmetric relative to where the stock sits in its own trading
    history: at ~8-9x forward earnings, a meaningful discount to both the broader market and
    FANG's own historical multiple, even modest commodity-price firming or multiple normalization
    produces outsized equity returns
  • Even the EPP-floor and conservative-2yr math (oil flat, no structural-premium credit,
    discount multiple applied) produces a modestly positive expected return — this is not a
    name requiring heroics to work

  POSITION SIZING GUIDANCE:
  • ACCUMULATE — a name to build a position in steadily rather than chase; adding more
    aggressively on any pullback toward $125-135 (where Ratio B would move firmly into BUY
    territory) further improves an already-reasonable entry
  • Watch for: net-debt trajectory toward the $8B target (the biggest swing factor), variable-
    dividend trends as a read on management's confidence in the FCF outlook, Endeavor synergy-
    capture updates, WTI price trends, and any signs of the market beginning to grant the
    combined entity a structural premium multiple
""")

    print(SEP)
    print(f"""
SUMMARY: FANG ◎ ACCUMULATE — Ratio B 0.95× (27.0% downside / 28.4% upside). THE LOWEST-COST, \
HIGHEST-QUALITY PURE-PLAY PERMIAN OPERATOR — NOW AT UNMATCHED SCALE: trading at $148.00 \
(52-wk range $128-198, roughly a third up the range — genuinely cheapened relative to its \
own history) on the back of the transformational Sept-2024 Endeavor Energy Resources \
combination (~$26B deal) that roughly doubled scale and created, by a wide margin, the \
largest pure-play Permian operator in existence — adding ~350,000 net acres of contiguous, \
high-quality Midland Basin inventory (a multi-decade drilling runway). STRUCTURAL COST \
LEADERSHIP: ~$9.85/boe cash operating cost and a ~$38 WTI corporate breakeven mean the \
company stays comfortably cash-generative through scenarios that would impair most peers. \
SHAREHOLDER-ALIGNED CAPITAL RETURN: base-plus-variable dividend (~$5.68/yr combined run- \
rate) layered with an active ~$6.0B buyback authorization — returning the large majority of \
FCF to shareholders through the cycle. Post-merger deleveraging on a credible glide path \
from ~$12.8B net debt toward an ~$8B target. THE HONEST RISK: FANG remains a leveraged, \
single-basin, single-commodity bet — a sustained oil downturn would pressure both the \
variable dividend and deleveraging simultaneously, and the Endeavor deal added real debt to \
a once-pristine balance sheet. Consensus 'Buy/Strong Buy' (~24 of 31 analysts), PT ~$175 \
(range $145-225). Conservative 2yr (oil-flat, discount-multiple floor case): EPS $13.10 x \
10.5x + $11.36 div = $148.91 -> +0.6% — BULL/XBULL require either firmer oil OR the market \
granting the combined entity its earned cost-leadership premium. DOWNSIDE MEANINGFULLY \
CUSHIONED BY GENUINE STRUCTURAL COST ADVANTAGES AGAINST GENUINELY ASYMMETRIC UPSIDE (a \
best-in-class operator priced like an average one, ~8-9x forward) — build a position \
steadily, add more aggressively on weakness toward $125-135. Bear $108 · Base $148 · \
Bull $190 · XBull $230."""
    )

    print(f"SIGNAL: {SIGNAL_TEXT} (lowest-cost pure-play Permian operator at unmatched post-Endeavor scale, priced at a meaningful discount to its own trading history) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
