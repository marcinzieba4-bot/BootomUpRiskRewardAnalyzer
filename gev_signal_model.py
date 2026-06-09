"""
GE Vernova Inc. (NYSE: GEV) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.91×  |  EPP Gap: +288.9%
=======================================================================
THE ESSENTIAL POWER INFRASTRUCTURE OF THE AI AND ENERGY-TRANSITION ERA:
GE Vernova owns the two things the world needs most right now — (1) the
most efficient gas turbines on earth (HA-class, 64%+ thermal efficiency)
at a moment of unprecedented demand from AI data centers, LNG export
facilities, and grid reliability imperatives; and (2) the grid equipment
(transformers, high-voltage switchgear) that every megawatt of new
generation and every data center MUST connect through — equipment that is
in a structural 2-3 year shortage with no near-term relief.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "GEV"
COMPANY        = "GE Vernova Inc."
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Energy Technology · Gas Turbines / Grid Equipment / Wind Energy · Power Generation & Electrification · NYSE: GEV"
SECTOR_GROUP   = "Industrials"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 420.00          # USD — mid-2026; up ~250% from $120 April 2024 IPO on AI power demand
ANNUAL_DIV     = 0.00            # no regular dividend; capital allocation to growth and buybacks
SHARES_OUT_B   = 0.272           # billions

FW52_HIGH      = 480.00
FW52_LOW       = 295.00

# ── Scenario prices ──────────────────────────────────────────────────────────
# BEAR  — AI data center power demand normalizes faster than expected; gas
#         turbine orders plateau; offshore wind legacy contract losses
#         re-emerge; electrification margins compress; multiple collapses
#         from narrative peak back toward traditional industrials valuation
# BASE  — gas power backlog executes (HA turbine orders through 2028-2029),
#         wind losses fully contained via contract exits and repricing,
#         electrification grid equipment backlog converts; 2026E EPS ~$13.50
#         at 30× growth-industrial multiple → ~$420 fair value
# BULL  — AI power supercycle extends: hyperscaler direct power purchase
#         agreements (Microsoft, Google, Amazon signing gas-backed PPAs);
#         grid equipment backlog re-rates as transformer shortage confirmed
#         structural; offshore wind reaches breakeven by 2027; FCF inflects
# XBULL — GEV re-rates as the essential power infrastructure platform:
#         gas + grid as the "picks and shovels" of the AI buildout; onshore
#         wind profitable; offshore optionality recognized; 35-40× multiple
BEAR           = 265.0
BASE           = 420.0
BULL           = 590.0
XBULL          = 730.0

# ── Earnings Power Price (EPP) floor ────────────────────────────────────────
# EPS_TROUGH: demand normalization + offshore wind losses + gas turbine
# order plateau; still earns ~$6/sh on services annuity and grid equipment
# PE_TROUGH: 18× reflects energy infrastructure floor even in adversity
EPS_TROUGH     = 6.00
PE_TROUGH      = 18.0
EPP            = EPS_TROUGH * PE_TROUGH     # $108.00

# ── Conservative 2-year price estimate ───────────────────────────────────────
# 2026E EPS ~$13.50 × 24× conservative industrial multiple + $0 div
# Conservative case -22.8% below current — reflects genuine risk that the
# AI narrative-driven premium (currently ~30-35× forward) normalizes
PE_CONSERVATIVE  = 24.0
EPS_FY2026E      = 13.50
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $324.00

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
    ("gas_power_ha_turbine_supercycle_and_ai_data_center_power_demand",    4.0, 0.25),
    ("electrification_grid_transformer_shortage_and_switchgear_backlog",   4.0, 0.20),
    ("wind_offshore_legacy_loss_exits_and_onshore_margin_recovery",        2.0, 0.18),
    ("gas_as_bridge_fuel_and_energy_transition_20_year_positioning",       3.5, 0.15),
    ("management_execution_scott_strazik_and_margin_expansion_trajectory", 3.5, 0.12),
    ("premium_valuation_30_35x_forward_and_narrative_concentration_risk",  2.0, 0.10),
]

# ── Structural Competitive Advantage (SCA) factors ────────────────────────────
SCA_FACTORS = {
    "ha_class_gas_turbines_worlds_most_efficient_and_7000_unit_services_annuity": +0.22,
    "grid_equipment_transformer_switchgear_structural_shortage_multi_year_backlog": +0.16,
    "gas_power_installed_base_and_sticky_long_term_parts_services_revenue":        +0.12,
    "energy_transition_bridge_fuel_positioning_and_20yr_gas_demand_runway":        +0.10,
    "offshore_wind_legacy_contract_losses_and_execution_risk_remaining":           -0.15,
    "premium_30_35x_narrative_valuation_vulnerable_to_demand_normalization":       -0.12,
    "wind_segment_structural_profitability_uncertainty_onshore_and_offshore":      -0.08,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.25

# ── Weighted conviction score ─────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ────────────────────────────────────────────────────────────
SUMMARY = (
    f"GEV ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE ESSENTIAL POWER INFRASTRUCTURE OF THE AI AND ENERGY-TRANSITION ERA: GE Vernova owns "
    "the two scarce resources the world needs most — (1) the most efficient gas turbines on "
    "earth (HA-class, 64%+ thermal efficiency, world #1 market share) at a moment of "
    "unprecedented demand from AI data centers, LNG export facilities, and grid reliability "
    "imperatives; gas turbine orders booked through 2028-2029; (2) grid equipment (power "
    "transformers, high-voltage switchgear, GridOS software) that every megawatt of new "
    "generation and every data center must connect through — transformer delivery lead times "
    "now 2-3 years, a structural shortage with no near-term relief. "
    "THE GAS POWER FLYWHEEL: ~7,000 GE turbines in service globally generate a $15B+ annual "
    "parts/services/upgrades annuity that compounds with every new unit delivered; HA-class "
    "orders from hyperscalers (Microsoft, Google, Amazon signing direct gas-backed PPAs) and "
    "LNG developers represent a multi-year, high-margin backlog executing now. "
    "THE HONEST RISK: offshore wind remains the scarred legacy — billions in losses on "
    "fixed-price contracts (Haliade-X, Vineyard Wind delays); while CEO Scott Strazik has "
    "credibly exited or repriced most of the worst contracts, execution risk persists; "
    "at 30-35× forward earnings GEV is priced for continued outperformance, not a pause — "
    "any demand normalization or earnings miss could compress the multiple sharply. "
    f"Conservative 2yr: EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× = "
    f"${CONSERVATIVE_PRICE:.0f} → {CONS_RETURN:.1f}% — genuine downside if the AI power "
    "narrative cools; BULL/XBULL require sustained hyperscaler gas demand and grid "
    "equipment re-rate. Add on narrative-driven pullbacks toward $340-370 where the "
    "risk/reward approaches ◉ BUY territory. "
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
    print("  • At 30-35× forward EPS, GEV is priced for continued perfection —")
    print("    the AI data center power narrative is fully reflected; any sign of")
    print("    hyperscaler capex moderation or gas turbine order normalization")
    print("    could compress the multiple 25-30% before earnings even move")
    print("  • Conservative 2yr floor ($324) is -22.8% below current price —")
    print("    genuine and material downside risk if the narrative cools")
    print("  • Offshore wind is not fully resolved: remaining Haliade-X commitments,")
    print("    permitting delays in Europe, and onshore wind margin recovery is still")
    print("    a 'show me' story; a surprise offshore loss would reset sentiment sharply")
    print("  • GEV has only been a public company since April 2024 — limited track")
    print("    record as an independent entity; execution under standalone pressure")
    print("    (IT systems, supply chains, capital allocation) is still being proven")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The gas turbine demand cycle is structural, not cyclical: AI data")
    print("    centers need 24/7 dispatchable power that solar and wind cannot provide;")
    print("    every new hyperscaler campus (Microsoft, Google, Amazon, Meta) is signing")
    print("    10-20 year gas-backed PPAs — GE HA turbines are the preferred platform")
    print("    because no competitor matches the 64%+ thermal efficiency")
    print("  • Transformer shortage is a genuine multi-year bottleneck: US grid")
    print("    transformer lead times have extended from 12 months to 36+ months;")
    print("    GEV's electrification segment has pricing power and a multi-year")
    print("    backlog that provides earnings visibility regardless of gas power timing")
    print("  • The 7,000-turbine installed base is a compounding annuity: every GE")
    print("    turbine ever installed is a recurring parts/services revenue stream")
    print("    — maintenance, upgrades, fuel efficiency improvements — that does not")
    print("    depend on new orders and generates ~$15B/yr in high-margin services")
    print("  • CEO Scott Strazik has demonstrated genuine operational discipline:")
    print("    exited uneconomic offshore wind contracts, improved gas power margins,")
    print("    and focused capital allocation — the early spin-off execution is credible")
    print("  • Ratio B 0.94× — downside 36.9% / upside 40.5% — the asymmetry is")
    print("    real; the AI/grid narrative creates the upside; the franchise creates")
    print("    the floor that makes the downside manageable")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  GE Vernova sits at the exact intersection of the two most powerful")
    print("  secular demand forces of this decade: AI infrastructure buildout (which")
    print("  needs reliable, dispatchable gas power NOW, not in 10 years when renewables")
    print("  plus storage scale) and grid modernization (which needs transformers and")
    print("  switchgear faster than they can be manufactured). The company is not a")
    print("  speculative bet on these themes — it is already the market leader in both,")
    print("  with a 7,000-turbine services annuity providing a durable earnings floor.")
    print("  The wind legacy is the drag; Strazik is fixing it. At $420 — with the")
    print("  narrative multiple already elevated but the fundamental backlog real —")
    print("  initiate at ◎ ACCUMULATE. Add aggressively on any pullback to $340-370.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
