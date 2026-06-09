"""
Micron Technology Inc. (NASDAQ: MU) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.99×  |  EPP Gap: +558.3%
=======================================================================
THE COMMODITY CYCLICAL THAT BECAME AN AI INFRASTRUCTURE GIANT: Micron
has completed one of the most dramatic business transformations in
semiconductor history. Q2 FY2026: $23.86B revenue (+196% YoY), $12.20
adj EPS per quarter, 74.9% gross margins — numbers that would have seemed
impossible 18 months ago when Micron was posting -$5.36 adj EPS in FY2023.
The driver: HBM4 (High Bandwidth Memory 4th generation) for AI accelerators.
Micron has completed agreements on price and volume for its entire
calendar 2026 HBM supply. The HBM TAM that was $35B in 2025 is now
forecast to reach $100B by 2028 — two years ahead of prior estimates.
Micron, SK Hynix, and Samsung are the only three companies on earth
capable of supplying HBM at volume; with AI infrastructure capex from
hyperscalers (Google, Microsoft, Meta, Amazon) and chip designers (NVIDIA,
AMD, Broadcom, Marvell) running at $200B+/year and accelerating, HBM
supply is perpetually tight. Micron's HBM4 now leads on performance and
power efficiency for key workloads. The company that used to be a
commodity memory cyclical is now an AI infrastructure critical-path
supplier with 74.9% gross margins and a near-trillion dollar market cap.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "MU"
COMPANY        = "Micron Technology Inc."
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Technology · HBM AI Accelerator Memory / DRAM & NAND / Data Center Infrastructure · NASDAQ: MU"
SECTOR_GROUP   = "Technology"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 948.00          # USD — June 2026; near-trillion market cap
ANNUAL_DIV     = 1.80            # USD/yr (~0.2% yield); capital return via buybacks
SHARES_OUT_B   = 1.03            # billions

FW52_HIGH      = 1080.00         # all-time high reached June 3, 2026
FW52_LOW       = 280.00          # approximate trough before AI-driven re-rating

# ── Scenario prices ───────────────────────────────────────────────────────────
# BEAR  — HBM cycle peaks and compresses: Samsung executes aggressive HBM
#         capacity additions 2027-2028; hyperscaler AI capex moderates from
#         peak levels; HBM pricing compresses 40-50% from peak; Micron's
#         EPS falls from $34 toward $8-12; multiple compresses to 18-22× on
#         cyclical fears; stock revisits pre-AI-boom levels in 2-year view
# BASE  — HBM sustains: entire 2026 supply contracted, 2027 supply agreements
#         being signed now; HBM TAM grows to $65-75B; FY2027E EPS $42-48;
#         multiple holds at 22-28× on AI infrastructure premium; ~$948
# BULL  — HBM TAM hits $100B early: AI inference scaling drives HBM demand
#         beyond training; Micron HBM4/HBM5 sustains technology leadership;
#         FY2028E EPS $60+; multiple 24× → ~$1,440
# XBULL — memory becomes as strategic as GPUs: HBM shortage persists through
#         2029; Micron's US manufacturing (CHIPS Act) commands government-
#         supported premium; EPS $80+ by FY2029; P/E re-rates to 28-30×
BEAR           = 480.0
BASE           = 948.0
BULL           = 1420.0
XBULL          = 1850.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPP = pessimistic_PE × current EPS — what is this business worth at a
# de-rated multiple on what it actually earns today?
# NOTE: EPP is imperfect for cyclicals — FY2023 actual adj EPS was -$5.36.
# Using current peak-cycle EPS $34 × a deeply pessimistic 5× = $170 reflects
# the floor near book value when the cycle fully inverts. HBM supply agreements
# dampen but don't eliminate the bust; genuine floor ~$120-150 (near book).
# A 5× multiple on current earnings is the honest cycle-inversion assumption.
PE_PESSIMISTIC = 5.0
EPS_FY2026E    = 34.00
EPP            = PE_PESSIMISTIC * EPS_FY2026E    # 5 × $34.00 = $170.00

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E adj EPS ~$34.00 × 28× conservative cycle-peak multiple + $1.80 div
# 28× is conservative for a company at cycle peak with HBM supply contracted
PE_CONSERVATIVE  = 28.0
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV  # $953.80

# ── Signal computation ─────────────────────────────────────────────────────────
DOWNSIDE_PCT   = (CURRENT_PRICE - BEAR) / CURRENT_PRICE
UPSIDE_PCT     = (BULL - CURRENT_PRICE) / CURRENT_PRICE
RATIO_B        = DOWNSIDE_PCT / UPSIDE_PCT

EPP_GAP_PCT    = (CURRENT_PRICE - EPP) / EPP * 100
CONS_RETURN    = (CONSERVATIVE_PRICE - CURRENT_PRICE) / CURRENT_PRICE * 100

if   RATIO_B < 0.75:  SIGNAL = "◉ BUY";        SIGNAL_COLOR = "#4ade80"
elif RATIO_B < 1.10:  SIGNAL = "◎ ACCUMULATE"; SIGNAL_COLOR = "#f0b429"
elif RATIO_B < 1.75:  SIGNAL = "◌ WATCHLIST";  SIGNAL_COLOR = "#60a5fa"
else:                 SIGNAL = "✕ AVOID";       SIGNAL_COLOR = "#f87171"

# ── Bottom-up signal factors ────────────────────────────────────────────────────
SIGNALS = [
    ("hbm4_leadership_entire_2026_supply_contracted_and_100b_tam_by_2028",             4.5, 0.25),
    ("74pct_gross_margins_23b_quarterly_revenue_and_ai_infrastructure_critical_path",  4.5, 0.22),
    ("three_supplier_oligopoly_rational_hbm_pricing_and_supply_agreement_visibility",  4.0, 0.18),
    ("memory_commodity_cycle_risk_samsung_capacity_and_hyperscaler_capex_moderation",  2.5, 0.20),
    ("chips_act_us_manufacturing_and_china_export_restriction_geopolitical_factor",    3.5, 0.15),
]

# ── Structural Competitive Advantage (SCA) factors ─────────────────────────────
SCA_FACTORS = {
    "hbm4_technology_leadership_and_entire_2026_supply_under_long_term_agreement":     +0.18,
    "74pct_gross_margins_confirming_hbm_premium_not_commodity_economics":              +0.14,
    "three_supplier_oligopoly_only_samsung_sk_hynix_micron_at_hbm_scale":             +0.12,
    "chips_act_us_fab_only_domestic_dram_maker_strategic_government_value":            +0.10,
    "memory_commodity_cycle_severe_downturns_fiveyear2023_adj_eps_minus_5_36":        -0.14,
    "samsung_capacity_risk_and_hyperscaler_ai_capex_cycle_peak_moderation":           -0.08,
    "25b_plus_annual_capex_requirement_capital_intensity_constrains_fcf_at_scale":    -0.06,
    "china_export_restrictions_potential_expansion_revenue_exposure":                  -0.08,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.18

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"MU ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap — EPP limited for cyclicals; genuine bust floor near book "
    f"~$150; FY2023 actual adj EPS was -$5.36) | "
    "THE COMMODITY CYCLICAL THAT BECAME AN AI INFRASTRUCTURE GIANT: Micron has transformed — "
    "Q2 FY2026: $23.86B revenue (+196% YoY), $12.20 adj EPS/quarter, 74.9% gross margins. "
    "HBM4 (High Bandwidth Memory 4th gen) is the driver: entire 2026 HBM supply contracted "
    "under long-term agreements; HBM TAM growing from $35B (2025) to $100B (2028, two years "
    "ahead of prior forecast). Only Samsung, SK Hynix, and Micron can supply HBM at volume — "
    "the oligopoly controls the memory layer of every AI accelerator on earth. "
    "MICRON NOW LEADS ON HBM4: HBM4 performance and power efficiency leadership confirmed; "
    "74.9% gross margins prove this is no longer commodity pricing. "
    "AI CAPEX CREATES MULTI-YEAR CONTRACTED VISIBILITY: hyperscalers (Google, Microsoft, "
    "Meta, Amazon) and chip designers (NVIDIA, AMD, Broadcom) running $200B+/yr AI infra "
    "capex; each H200/B200/B300 GPU requires HBM3E/HBM4; supply perpetually tight. "
    "THE HONEST RISK: memory remains cyclical at its core — Samsung's capacity decisions "
    "can flood HBM supply in 2027-2028; hyperscaler capex cycles have peaked before; "
    "the -49% bear case at $480 is not hypothetical (FY2023 Micron: -$5.36 adj EPS, "
    "stock at $50); EPP at $144 is a mid-cycle floor, not a bust floor. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — essentially "
    "flat at current peak cycle multiples; BULL requires HBM TAM trajectory to hold. "
    "Size for the -49% bear being a recurring cyclical outcome. "
    f"Bear ${BEAR:.0f} · Base ${BASE:.0f} · Bull ${BULL:.0f} · XBull ${XBULL:.0f}."
)

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{'='*72}")
    print(f"  {TICKER}  |  {COMPANY}")
    print(f"  {SECTOR}")
    print(f"{'='*72}")
    print(f"  Current Price:                                     ${CURRENT_PRICE:>8.2f}")
    print(f"  Annual Dividend:                                   ${ANNUAL_DIV:>8.2f}")
    print(f"  52-Week Range:                      ${FW52_LOW:.2f} – ${FW52_HIGH:.2f}")
    print()
    print(f"  Scenario Prices:")
    print(f"    Bear:                                            ${BEAR:>8.2f}")
    print(f"    Base:                                            ${BASE:>8.2f}")
    print(f"    Bull:                                            ${BULL:>8.2f}")
    print(f"    XBull:                                           ${XBULL:>8.2f}")
    print()
    print(f"  Downside (current → bear):                    {DOWNSIDE_PCT*100:>7.1f}%")
    print(f"  Upside   (current → bull):                    {UPSIDE_PCT*100:>7.1f}%")
    print(f"  Ratio B = {RATIO_B:.4f} → {SIGNAL}")
    print()
    print(f"  PE Pessimistic (cycle inversion):                  {PE_PESSIMISTIC:>8.1f}×")
    print(f"  EPP (Pessimistic PE × current EPS):             ${EPP:>8.2f}")
    print(f"  EPP (Earnings Power Price):                        ${EPP:>8.2f}  (limited for cyclicals)")
    print(f"  EPP Gap (current vs. EPP floor):              {EPP_GAP_PCT:>+8.1f}%")
    print()
    print(f"  Conservative Price ({EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}×):       ${CONSERVATIVE_PRICE:>8.2f}  ({CONS_RETURN:>+.1f}%)")
    print()
    print(f"  Weighted Conviction Score:                         {WCS:>8.2f} / 5.0")
    print(f"  SCA Net:                                           {SCA_NET:>+8.2f}")
    print(f"  EV(model): ${EV_MODEL:>8.2f}   Upside: {(EV_MODEL-CURRENT_PRICE)/CURRENT_PRICE*100:>+.1f}%   Downside: -{DOWNSIDE_PCT*100:.1f}%")
    print()
    print(f"  SIGNAL:  {SIGNAL}   Ratio B: {RATIO_B:.2f}×   EPP Gap: {EPP_GAP_PCT:>+.1f}%")
    print(f"{'='*72}")
    print()

    print("  BOTTOM-UP SIGNAL FACTORS")
    print(f"  {'Factor':<64} {'Conv':>4}  {'Wt':>5}")
    print(f"  {'-'*72}")
    for name, conv, wt in SIGNALS:
        print(f"  {name:<64} {conv:>4.1f}  {wt:>5.0%}")
    print()

    print("  STRUCTURAL COMPETITIVE ADVANTAGE FACTORS")
    for k, v in SCA_FACTORS.items():
        print(f"  {k:<68} {v:>+.2f}")
    print(f"  {'SCA NET':<68} {SCA_NET:>+.2f}")
    print()

    print(f"{'='*72}")
    print()
    print("  WHY THIS IS AN ◎ ACCUMULATE, NOT A ◌ WATCHLIST OR ◉ BUY")
    print()
    print("  NOT ◉ BUY because:")
    print("  • The -49% bear case is a real cyclical risk, not a tail event:")
    print("    Micron went from -$5.36 adj EPS in FY2023 to $34 annualized")
    print("    in FY2026 — the amplitude of memory cycles is extreme; Samsung")
    print("    has a history of absorbing losses to maintain market share and")
    print("    flooding capacity when pricing peaks; if Samsung executes an")
    print("    aggressive HBM ramp in 2027-2028, pricing compresses rapidly")
    print("  • Conservative 2yr +0.6% — stock is priced at peak cycle multiples:")
    print("    at $948 on $34 FY2026E EPS (28× forward), there is no margin")
    print("    of safety on a base-case scenario; you need the HBM TAM to")
    print("    continue tracking toward $100B AND Micron to maintain share")
    print("    AND hyperscaler AI capex to remain elevated — three variables")
    print("    that must all hold simultaneously")
    print("  • $25B+ annual capex burns most of the operating cash flow:")
    print("    at $25B capex and ~$40B in operating cash flow, free cash flow")
    print("    yield is relatively modest at current price; the bull case")
    print("    requires capex to eventually normalize relative to revenue")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • 74.9% gross margins confirm the structural transformation:")
    print("    commodity DRAM earns 30-40% gross margins at cycle peak;")
    print("    74.9% is AI infrastructure pricing — Micron is now on the")
    print("    critical path of every AI accelerator with essentially zero")
    print("    substitution risk in the 12-18 month window; this is not")
    print("    a temporary margin spike, it reflects contracted HBM pricing")
    print("  • Entire 2026 HBM supply is contracted — unusual visibility:")
    print("    memory companies historically had zero long-term pricing")
    print("    visibility; HBM supply agreements represent a fundamental")
    print("    change in the customer relationship from spot commodity to")
    print("    strategic infrastructure partnership")
    print("  • HBM TAM trajectory ($35B → $100B by 2028) is driven by AI")
    print("    scaling laws that are independent of Micron's execution —")
    print("    each next-generation GPU requires more HBM bandwidth; the")
    print("    demand is physics-driven, not market-driven")
    print("  • Ratio B 0.99× — 49.4% downside / 49.8% upside — balanced;")
    print("    the wide absolute range reflects the cyclical reality")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Micron has completed a business transformation that most analysts")
    print("  thought impossible: from -$5.36 EPS in FY2023 to $34 annualized")
    print("  EPS in FY2026, powered by HBM4 leadership and AI infrastructure")
    print("  demand. At $948, the stock prices in continued HBM TAM growth")
    print("  toward $100B by 2028 — a thesis supported by AI scaling laws")
    print("  and $200B+ annual hyperscaler capex. The bear case at $480 is")
    print("  a -49% drop that memory investors know is always possible when")
    print("  Samsung decides to defend market share with aggressive capacity.")
    print("  Accumulate. Size for the cycle risk. Add hard if Samsung-driven")
    print("  fears push the stock toward $650-720.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
