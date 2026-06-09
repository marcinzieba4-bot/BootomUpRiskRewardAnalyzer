"""
Trane Technologies plc (NYSE: TT) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.88×  |  EPP Gap: +125.0%
=======================================================================
THE CLIMATE CONTROL FRANCHISE AT THE INTERSECTION OF DATA CENTER COOLING
AND BUILDING DECARBONIZATION: Trane Technologies owns the #1 North American
commercial HVAC brand (Trane) and the world's leading refrigerated transport
platform (Thermo King) at the convergence of two independent secular demand
cycles: AI/cloud data centers generating unprecedented heat loads requiring
precision cooling, and the global building decarbonization mandate driving a
multi-decade HVAC electrification and efficiency replacement cycle.
"""

# ── Model identity ────────────────────────────────────────────────────────────
TICKER         = "TT"
COMPANY        = "Trane Technologies plc"
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Industrial Climate Control · Commercial & Residential HVAC / Refrigerated Transport · NYSE: TT"
SECTOR_GROUP   = "Industrials"

# ── Price & share data ────────────────────────────────────────────────────────
CURRENT_PRICE  = 360.00          # USD — mid-2026; re-rated on data center cooling + decarbonization
ANNUAL_DIV     = 3.52            # USD/yr (~1.0% yield); growing dividend, 14+ consecutive increases
SHARES_OUT_B   = 0.229           # billions (consistent buybacks; share count down meaningfully)

FW52_HIGH      = 405.00
FW52_LOW       = 282.00

# ── Scenario prices ───────────────────────────────────────────────────────────
# BEAR  — data center cooling narrative normalizes: hyperscaler capex cycle
#         pauses, liquid cooling alternatives (CDUs, immersion) commoditize
#         the opportunity; residential HVAC turns down with housing; IRA
#         incentives roll back; commercial construction activity softens;
#         multiple compresses from growth-industrial to mid-cycle
# BASE  — steady secular compounder: data center cooling sustains 20%+ growth
#         in that vertical, commercial HVAC replacement cycle steady, Thermo
#         King electric refrigeration ramp continues; 2026E EPS ~$13.00 at
#         27× → ~$360 fair value on quality premium
# BULL  — AI cooling supercycle: hyperscaler data center cooling contracts
#         sustain multi-year revenue visibility; IRA heat pump incentives
#         accelerate residential replacement; Thermo King electric TK ramp;
#         European building efficiency mandates drive international growth
# XBULL — category dominance: Trane established as the data center cooling
#         standard; building electrification legislation expands globally;
#         services/digital subscription revenue streams at SaaS multiples
BEAR           = 245.0
BASE           = 360.0
BULL           = 490.0
XBULL          = 600.0

# ── Earnings Power Price (EPP) floor ──────────────────────────────────────────
# EPS_TROUGH: commercial HVAC cycle trough with data center cooling absent —
# still earns ~$8.00/sh on service parts annuity and Thermo King
# PE_TROUGH: 20× reflects premium HVAC franchise floor (switching costs,
# brand, service network that never goes to zero demand)
EPS_TROUGH     = 8.00
PE_TROUGH      = 20.0
EPP            = EPS_TROUGH * PE_TROUGH     # $160.00

# ── Conservative 2-year price estimate ────────────────────────────────────────
# 2026E EPS ~$13.00 × 25× conservative quality-industrial multiple + $3.52 div
# Conservative case -8.5% — modest downside; quality franchise limits damage
PE_CONSERVATIVE  = 25.0
EPS_FY2026E      = 13.00
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $328.52

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
# (name, conviction 1-5, weight)
SIGNALS = [
    ("ai_data_center_precision_cooling_demand_cycle_and_hyperscaler_capex",  4.0, 0.22),
    ("building_decarbonization_heat_pump_electrification_and_ira_incentives", 3.5, 0.20),
    ("commercial_hvac_installed_base_service_parts_and_recurring_annuity",   3.5, 0.17),
    ("premium_valuation_27_30x_forward_and_cycle_normalization_risk",        2.0, 0.16),
    ("thermo_king_refrigerated_transport_and_electric_tk_platform_ramp",     3.0, 0.14),
    ("residential_hvac_cyclicality_and_housing_market_sensitivity",          2.5, 0.11),
]

# ── Structural Competitive Advantage (SCA) factors ─────────────────────────────
SCA_FACTORS = {
    "trane_no1_north_america_commercial_hvac_brand_and_contractor_switching_costs": +0.20,
    "data_center_precision_cooling_expertise_and_hyperscaler_relationships":        +0.16,
    "service_parts_annuity_on_massive_installed_base_recurring_revenue_floor":      +0.12,
    "building_decarbonization_heat_pump_30yr_electrification_secular_tailwind":     +0.10,
    "premium_27_30x_valuation_requires_continued_execution_without_pause":          -0.14,
    "commercial_hvac_cyclicality_and_non_residential_construction_sensitivity":     -0.10,
    "residential_cycle_sensitivity_and_housing_affordability_demand_headwind":      -0.07,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.27

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"TT ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE CLIMATE CONTROL FRANCHISE AT THE INTERSECTION OF DATA CENTER COOLING AND BUILDING "
    "DECARBONIZATION: Trane Technologies owns the #1 North American commercial HVAC brand "
    "(Trane) and world-leading refrigerated transport platform (Thermo King) at the convergence "
    "of two independent secular demand cycles. "
    "DATA CENTER COOLING IS STRUCTURAL: every AI server generates 2-3× the heat of a "
    "conventional server; liquid cooling, precision air handling, and chiller systems are not "
    "optional infrastructure — they are rate-limiting constraints on data center density; "
    "Trane has established direct hyperscaler relationships (Microsoft, Google, AWS) for "
    "large-scale cooling programs with multi-year visibility. "
    "BUILDING DECARBONIZATION IS A 30-YEAR CYCLE: IRA heat pump tax credits ($2,000/unit) "
    "accelerate US residential electrification; EU building efficiency directives (EPBD) "
    "mandate minimum energy performance upgrades across 35M European buildings; commercial "
    "building operators facing net-zero commitments are upgrading HVAC systems years ahead "
    "of code requirements — all pulling on the same Trane equipment. "
    "THE SERVICE ANNUITY FLOORS DOWNSIDE: Trane's multi-billion parts/service/controls "
    "business generates recurring revenue on the installed base regardless of new equipment "
    "cycles — a structural cash flow floor that persists through every construction downturn. "
    "THE HONEST RISK: at 27-30× forward EPS, TT is priced for continued outperformance; "
    "a hyperscaler capex pause, IRA rollback, or commercial construction slowdown could "
    "compress the multiple before earnings even move. "
    f"Conservative 2yr: EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}%. "
    "A WORLD-CLASS QUALITY COMPOUNDER AT A FAIR PRICE: accumulate steadily; add more "
    f"aggressively on any pullback toward $295-320. "
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
    print(f"  Conservative Price ({EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}×):        ${CONSERVATIVE_PRICE:>8.2f}  ({CONS_RETURN:>+.1f}%)")
    print()
    print(f"  Weighted Conviction Score:                         {WCS:>8.2f} / 5.0")
    print(f"  SCA Net:                                           {SCA_NET:>+8.2f}")
    print(f"  EV(model): ${EV_MODEL:>8.2f}   Upside: {(EV_MODEL-CURRENT_PRICE)/CURRENT_PRICE*100:>+.1f}%   Downside: -{DOWNSIDE_PCT*100:.1f}%")
    print()
    print(f"  SIGNAL:  {SIGNAL}   Ratio B: {RATIO_B:.2f}×   EPP Gap: {EPP_GAP_PCT:>+.1f}%")
    print(f"{'='*72}")
    print()

    print("  BOTTOM-UP SIGNAL FACTORS")
    print(f"  {'Factor':<62} {'Conv':>4}  {'Wt':>5}")
    print(f"  {'-'*72}")
    for name, conv, wt in SIGNALS:
        print(f"  {name:<62} {conv:>4.1f}  {wt:>5.0%}")
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
    print("  • At 27-30× forward EPS, TT is priced for continued execution without")
    print("    a stumble — a pause in hyperscaler cooling capex, an IRA rollback,")
    print("    or a commercial construction slowdown could compress the multiple 20-25%")
    print("    before earnings even change; the conservative floor (-8.5%) is modest")
    print("    but reflects a stock priced for perfection at current levels")
    print("  • Liquid cooling competition is real: direct liquid cooling (DLC),")
    print("    immersion cooling, and rear-door heat exchangers are attracting VC")
    print("    capital and hyperscaler R&D; if cooling technology commoditizes,")
    print("    Trane's premium positioning could face margin pressure")
    print("  • Residential HVAC is more cyclical than commercial: housing starts and")
    print("    existing home sales drive replacement demand, and affordability headwinds")
    print("    can extend replacement cycles — this segment adds volatility")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • Data center cooling is not discretionary: a server farm that overheats")
    print("    destroys $100M+ of equipment in hours; cooling systems are not value-")
    print("    engineered out of data center construction budgets — they are the")
    print("    rate-limiting constraint on compute density, and Trane's precision air")
    print("    handling and chiller expertise is recognized at the hyperscaler level")
    print("  • Building decarbonization is a 30-year mandate, not a 3-year trend:")
    print("    the EU EPBD requires all residential buildings to reach EPC class E")
    print("    by 2030 and D by 2033; US IRA incentives run through 2032; municipal")
    print("    net-zero commitments drive commercial HVAC upgrades city by city —")
    print("    Trane's heat pump portfolio benefits from every one of these mandates")
    print("  • The service and parts business is a structural floor: once a Trane")
    print("    system is installed in a commercial building, the customer is captive")
    print("    for 15-20 years of service contracts, parts, and controls upgrades —")
    print("    this annuity generates billions in high-margin recurring revenue through")
    print("    every construction cycle, providing genuine downside cushion")
    print("  • Thermo King electric refrigeration (TK) is an underappreciated option:")
    print("    cold chain electrification is mandated in California, advancing in the")
    print("    EU, and demanded by food/pharma ESG commitments; Thermo King is the")
    print("    global standard for refrigerated transport and the electrification")
    print("    transition replaces units faster than the standard replacement cycle")
    print("  • Ratio B 0.88× — downside 31.9% / upside 36.1% — the secular tailwinds")
    print("    create the asymmetry; the service annuity and brand create the floor")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Trane Technologies is a 100-year-old industrial franchise being repriced")
    print("  as a growth platform because two of the most powerful secular trends of")
    print("  the decade — AI infrastructure buildout and building decarbonization —")
    print("  both require more of its core product. Data centers need cooling that")
    print("  keeps servers alive; buildings need efficient HVAC systems that cut")
    print("  carbon emissions. Trane's brand, contractor relationships, and installed")
    print("  base service annuity mean neither of these tailwinds faces displacement")
    print("  from a new entrant without decades of friction. At $360 — 31.9% from")
    print("  bear, 36.1% from bull — accumulate steadily; add on cooling-narrative")
    print("  pullbacks toward $295-320.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
