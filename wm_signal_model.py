"""
Waste Management, Inc. (NYSE: WM) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.93×  |  EPP Gap: +98.3%
=======================================================================
THE LARGEST WASTE INFRASTRUCTURE MONOPOLY IN NORTH AMERICA — LANDFILLS
AS IRREPLACEABLE REGULATED ASSETS: Waste Management owns the largest
network of landfills, transfer stations, and collection routes in the US —
assets that took decades to permit and can never be replicated. Landfill
gate rates price above inflation every year because there is no
alternative. Stericycle (acquired 2024) adds premium-margin medical and
specialty waste to an already-exceptional collection of infrastructure
monopolies. This is the toll road of garbage disposal.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "WM"
COMPANY        = "Waste Management, Inc."
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Environmental Services · Solid Waste Collection / Landfill Disposal / Recycling / Medical Waste · NYSE: WM"
SECTOR_GROUP   = "Industrials"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 240.00          # USD — mid-2026; steady compounder, re-rated post-Stericycle
ANNUAL_DIV     = 3.20            # USD/yr (~1.3% yield); 20+ consecutive years of dividend growth
SHARES_OUT_B   = 0.400           # billions (consistent buybacks)

FW52_HIGH      = 265.00
FW52_LOW       = 195.00

# ── Scenario prices ──────────────────────────────────────────────────────────
# BEAR  — economic recession + recycling commodity collapse: construction
#         waste volumes fall 20%+, commercial waste down 10-15%, recycling
#         fiber/plastic prices hit multi-year lows, Stericycle integration
#         costs exceed plan; stock re-rates toward trough essential-services multiple
# BASE  — steady compounder: pricing +4-5%/yr above CPI continues,
#         Stericycle integration on track, recycling profitability improving
#         via tech investments; market prices $8.00 EPS at ~28-29× premium-
#         infrastructure multiple → ~$240 fair value
# BULL  — Stericycle fully integrated at WM margins: medical/specialty waste
#         premium-margins add $300M+ EBIT; recycling profitability inflects
#         on commodity prices and automation; sustainability premium re-rates
#         the landfill asset value; pricing power extends to 5-6%/yr
# XBULL — infrastructure re-rate: market values landfill network like toll
#         roads or pipelines (infrastructure multiples 35-40×); Stericycle
#         synergies exceed plan; recycling becomes a $1B+ EBITDA segment
BEAR           = 170.0
BASE           = 240.0
BULL           = 315.0
XBULL          = 385.0

# ── Earnings Power Price (EPP) floor ────────────────────────────────────────
# EPS_TROUGH: recession + recycling headwinds; WM's essential services
# nature limits downside — still earns ~$5.50/sh even in severe downturn
# PE_TROUGH: 22× reflects essential-infrastructure floor (people always
# produce garbage; landfill gate has no substitute)
EPS_TROUGH     = 5.50
PE_TROUGH      = 22.0
EPP            = EPS_TROUGH * PE_TROUGH     # $121.00

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E EPS ~$8.00 × 27× essential-infrastructure multiple + $3.20 div
# Conservative case -8.7% — limited downside for an essential services company
PE_CONSERVATIVE  = 27.0
EPS_FY2026E      = 8.00
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $219.20

# ── Signal computation ────────────────────────────────────────────────────────
DOWNSIDE_PCT   = (CURRENT_PRICE - BEAR) / CURRENT_PRICE
UPSIDE_PCT     = (BULL - CURRENT_PRICE) / CURRENT_PRICE
RATIO_B        = DOWNSIDE_PCT / UPSIDE_PCT

EPP_GAP_PCT    = (CURRENT_PRICE - EPP) / EPP * 100
CONS_RETURN    = (CONSERVATIVE_PRICE - CURRENT_PRICE) / CURRENT_PRICE * 100

if   RATIO_B < 0.75:  SIGNAL = "◉ BUY";        SIGNAL_COLOR = "#4ade80"
elif RATIO_B < 1.10:  SIGNAL = "◎ ACCUMULATE"; SIGNAL_COLOR = "#f0b429"
elif RATIO_B < 1.75:  SIGNAL = "◌ WATCHLIST";  SIGNAL_COLOR = "#60a5fa"
else:                 SIGNAL = "✕ AVOID";       SIGNAL_COLOR = "#f87171"

# ── Bottom-up signal factors ──────────────────────────────────────────────────
# (name, conviction 1-5, weight)
SIGNALS = [
    ("landfill_scarcity_irreplaceable_disposal_asset_network_and_pricing_power", 4.5, 0.25),
    ("collection_pricing_above_inflation_and_contractual_escalators",            4.0, 0.20),
    ("environmental_permitting_regulatory_moat_and_barrier_to_new_entry",        4.0, 0.15),
    ("stericycle_medical_waste_integration_and_premium_margin_expansion",        3.0, 0.17),
    ("recycling_technology_investment_and_commodity_price_sensitivity",          2.5, 0.13),
    ("economic_cycle_volume_sensitivity_and_construction_waste_exposure",        2.5, 0.10),
]

# ── Structural Competitive Advantage (SCA) factors ────────────────────────────
SCA_FACTORS = {
    "landfill_network_impossible_to_permit_irreplaceable_regional_monopolies":     +0.25,
    "collection_pricing_contractual_escalators_consistently_above_cpi":           +0.16,
    "environmental_permitting_regulatory_moat_and_20yr_barrier_to_new_supply":    +0.12,
    "stericycle_medical_specialty_waste_premium_margin_and_compliance_moat":      +0.10,
    "recycling_commodity_price_volatility_and_mrf_margin_sensitivity":            -0.10,
    "economic_cycle_volume_sensitivity_construction_commercial_waste":            -0.08,
    "stericycle_integration_execution_cost_and_leverage_reduction_timeline":      -0.07,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.38

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"WM ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE LARGEST WASTE INFRASTRUCTURE MONOPOLY IN NORTH AMERICA — LANDFILLS AS "
    "IRREPLACEABLE REGULATED ASSETS: Waste Management owns the largest network of "
    "landfills, transfer stations, and collection routes in the US — assets that took "
    "decades to permit under increasingly strict environmental regulations and can never "
    "be replicated. Every ton of solid waste produced in a WM service area has exactly "
    "one place to go: a WM landfill. Gate rates price above CPI every year because "
    "there is no alternative. "
    "THE PRICING POWER IS STRUCTURAL: WM raises collection and disposal rates 4-6%/yr "
    "via automatic CPI-plus escalators baked into multi-year municipal and commercial "
    "contracts; customers cannot switch without facing regulatory compliance issues, "
    "contract penalties, and service disruption — churn is structurally low. "
    "STERICYCLE ADDS A PREMIUM TIER: WM's 2024 acquisition of Stericycle (~$7.2B) "
    "adds regulated medical, pharmaceutical, and hazardous waste — a compliance-driven, "
    "higher-margin specialty segment (hospitals, clinics, pharma manufacturers MUST "
    "use certified handlers) being integrated onto WM's existing network infrastructure "
    "with $250M+ in targeted synergies. "
    "THE HONEST RISK: recycling is the volatile segment — fiber, plastic, and metal "
    "commodity prices can swing 30-50% and materially affect MRF economics; economic "
    "recessions reduce construction/commercial waste volumes (10-15% drawdown); "
    "Stericycle integration costs are real near-term headwinds. "
    f"Conservative 2yr: EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — "
    "essential services company with limited downside. 20+ years of consecutive dividend "
    "growth; FCF generation is durable through economic cycles. "
    "THE TOLL ROAD OF GARBAGE DISPOSAL: accumulate steadily; add on any recession-fear "
    f"or recycling-driven pullback toward $200-215. "
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
    print(f"  52-Week Range:                          ${FW52_LOW:.2f} – ${FW52_HIGH:.2f}")
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
    print(f"  EPS Trough:                                        ${EPS_TROUGH:>8.2f}")
    print(f"  PE Trough:                                         {PE_TROUGH:>8.1f}×")
    print(f"  EPP (Earnings Power Price):                        ${EPP:>8.2f}")
    print(f"  EPP Gap (current vs. EPP floor):              {EPP_GAP_PCT:>+8.1f}%")
    print()
    print(f"  Conservative Price ({EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}×):         ${CONSERVATIVE_PRICE:>8.2f}  ({CONS_RETURN:>+.1f}%)")
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
    print("  • At 28-30× forward EPS, WM is priced as a premium infrastructure")
    print("    compounder — fair value, not deep value; the landfill scarcity")
    print("    and pricing-power narrative is well-understood and consensus-priced")
    print("  • Conservative 2yr floor ($219) is -8.7% below current price; while")
    print("    limited, there IS real downside from a valuation multiple contraction")
    print("    in a rising-rate or risk-off environment")
    print("  • Stericycle integration is in its early stages: $7.2B acquisition")
    print("    with $250M+ synergy targets takes 2-3 years to fully realize; near-")
    print("    term integration costs pressure free cash flow and reported margins")
    print("  • Recycling segment remains a wildcard: fiber prices fell 60%+ in")
    print("    2022-23 and WM cannot fully hedge commodity exposure; a prolonged")
    print("    recycling commodity downturn adds earnings volatility to an otherwise")
    print("    predictable model")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The landfill moat is genuinely irreplaceable: the last major landfill")
    print("    to receive a new permit in a major US metropolitan area was decades ago;")
    print("    NIMBY opposition, EPA regulations, and state/local permitting make new")
    print("    large-scale landfill development essentially impossible; WM's existing")
    print("    network is a regulated monopoly that appreciates in value as remaining")
    print("    airspace becomes scarcer each year")
    print("  • Pricing power is contractually embedded: CPI-plus escalators baked")
    print("    into multi-year municipal and commercial contracts mean WM raises rates")
    print("    4-6%/yr virtually automatically; customers face switching costs (permit")
    print("    transfers, compliance recertification, service disruption risk) that")
    print("    make churn structurally low even when prices rise above market")
    print("  • Stericycle is a genuine value-creation opportunity: WM is applying its")
    print("    superior route density, logistics optimization, and compliance systems")
    print("    to a medical waste business that had been run sub-optimally as a")
    print("    standalone; $250M+ in synergies is conservative given WM's integration")
    print("    track record (Advanced Disposal, for example, outperformed targets)")
    print("  • Essential services recession-resilience: people produce garbage in")
    print("    recessions; hospitals generate medical waste regardless of GDP; the")
    print("    volume decline in a recession (-5-10% commercial/construction) is")
    print("    far less than the pricing power retention (+4-5%/yr) — WM's EBITDA")
    print("    is genuinely durable through economic cycles in a way few industrials are")
    print("  • Ratio B 0.93× — downside 29.2% / upside 31.3% — the asymmetry is")
    print("    real; the landfill monopoly creates the floor; Stericycle and pricing")
    print("    power create the upside")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Waste Management is the closest thing to a legally-sanctioned monopoly")
    print("  in American commerce: a regional landfill is a franchise that cannot be")
    print("  replicated, cannot be disrupted by technology, and gets more valuable")
    print("  every year as the remaining airspace depletes. The collection business")
    print("  has pricing power that compounds above inflation via contract. Stericycle")
    print("  adds a compliance-driven, premium-margin specialty tier that no hospital")
    print("  can opt out of. Twenty-plus years of dividend growth reflects a business")
    print("  that earns more cash every year regardless of economic cycle. At $240 —")
    print("  29.2% from bear, 31.3% from bull — accumulate steadily. The toll road")
    print("  of garbage disposal never closes.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
