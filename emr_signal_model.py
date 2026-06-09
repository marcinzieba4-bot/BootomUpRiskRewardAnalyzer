"""
Emerson Electric Co. (NYSE: EMR) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.94×  |  EPP Gap: +114.3%
=======================================================================
THE PROCESS AUTOMATION BACKBONE OF THE GLOBAL ENERGY AND INDUSTRIAL
TRANSITION: Emerson Electric is completing a strategic transformation from
diversified conglomerate into a pure-play industrial automation company.
DeltaV DCS is the process control backbone for half the world's LNG
terminals, refineries, and chemical plants. NI adds semiconductor/EV test
& measurement. AspenTech adds process optimization software. The
convergence of LNG export build-out, energy transition, and manufacturing
reshoring creates a multi-year automation demand cycle — at the moment
Emerson's portfolio is precisely positioned for all three.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "EMR"
COMPANY        = "Emerson Electric Co."
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Industrial Automation & Technology · Process Control / DCS / Test & Measurement / Software · NYSE: EMR"
SECTOR_GROUP   = "Industrials"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 135.00          # USD — mid-2026; re-rated on automation/LNG/NI integration thesis
ANNUAL_DIV     = 2.10            # USD/yr (~1.6% yield); 47+ consecutive years of dividend growth (Dividend King)
SHARES_OUT_B   = 0.585           # billions

FW52_HIGH      = 150.00
FW52_LOW       = 108.00

# ── Scenario prices ───────────────────────────────────────────────────────────
# BEAR  — energy capex cycle turns down: oil/gas customers reduce automation
#         spending 15-20%, LNG project delays, NI integration underperforms,
#         AspenTech growth slows; transformation discount re-emerges; multiple
#         compresses toward trough diversified-industrial valuation
# BASE  — transformation delivers: DeltaV maintains LNG/refinery specification,
#         NI integration on plan ($165M synergies), AspenTech growing ~10%+/yr,
#         reshoring drives process automation orders; 2026E adj EPS ~$5.50 at
#         ~24× → ~$135 quality-industrial fair value
# BULL  — automation supercycle: LNG export capex sustains multi-year elevated
#         orders, NI integration exceeds synergy targets, AspenTech re-rates
#         on ARR growth; manufacturing reshoring drives brownfield automation;
#         adj EPS $7+ by 2028; multiple expands toward 28-30×
# XBULL — pure-play automation re-rate: market prices EMR as software-enriched
#         automation platform (DeltaV + AspenTech + NI); NI/AspenTech software
#         ARR generates premium SaaS-like multiple on 30%+ of revenue
BEAR           = 90.0
BASE           = 135.0
BULL           = 183.0
XBULL          = 230.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: energy capex down + NI integration costs; DeltaV installed-
# base service revenue provides a durable floor; still earns ~$3.50/sh adj
# PE_TROUGH: 18× reflects process-automation-with-software floor
EPS_TROUGH     = 3.50
PE_TROUGH      = 18.0
EPP            = EPS_TROUGH * PE_TROUGH     # $63.00

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E adj EPS ~$5.50 × 22× conservative quality-industrial multiple + div
# Conservative case -8.8% — quality franchise limits the downside
PE_CONSERVATIVE  = 22.0
EPS_FY2026E      = 5.50
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $123.10

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
    ("deltav_dcs_process_automation_leadership_and_lng_energy_infrastructure",   4.0, 0.22),
    ("lng_export_buildout_and_energy_transition_automation_demand_cycle",         3.5, 0.20),
    ("aspentech_process_optimization_software_and_high_margin_recurring_revenue", 3.5, 0.17),
    ("national_instruments_ni_integration_ev_semiconductor_test_measurement",     3.0, 0.16),
    ("energy_capex_cycle_oil_gas_customer_concentration_and_project_risk",        2.5, 0.14),
    ("47yr_dividend_king_and_portfolio_transformation_execution_credibility",      3.5, 0.11),
]

# ── Structural Competitive Advantage (SCA) factors ────────────────────────────
SCA_FACTORS = {
    "deltav_dcs_no1_global_process_automation_platform_and_deep_switching_costs":  +0.20,
    "lng_export_measurement_control_specification_lock_in_and_project_backlog":    +0.14,
    "aspentech_process_optimization_software_high_margin_arr_and_saas_trajectory": +0.12,
    "47_consecutive_dividend_growth_years_dividend_king_and_fcf_discipline":       +0.10,
    "energy_capex_cycle_oil_gas_concentration_and_project_timing_risk":            -0.14,
    "ni_integration_execution_risk_and_test_measurement_end_market_cyclicality":   -0.10,
    "transformation_execution_risk_and_portfolio_complexity_discount":             -0.07,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.25

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"EMR ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE PROCESS AUTOMATION BACKBONE OF THE GLOBAL ENERGY AND INDUSTRIAL TRANSITION: "
    "Emerson Electric is completing its transformation from diversified conglomerate into "
    "a pure-play industrial automation company — selling Climate Technologies ($14B to "
    "Blackstone), acquiring National Instruments ($8.2B, test & measurement), and retaining "
    "its ~55% stake in AspenTech (process optimization software). "
    "DELTAV DCS IS THE CROWN JEWEL: Emerson's DeltaV distributed control system is the "
    "process automation backbone for half the world's LNG terminals, refineries, chemical "
    "plants, and pharmaceutical manufacturing sites — specification-locked for the life of "
    "the facility (20-40 years), with deep switching costs from instrument calibration, "
    "operator training, and safety system integration; once DeltaV is installed, the "
    "service/upgrade annuity compounds for decades. "
    "LNG IS THE NEAR-TERM CATALYST: the US LNG export build-out (Plaquemines, Port Arthur 2, "
    "Lake Charles, CP2, Corpus Christi Stage 3 — $150B+ in sanctioned projects) requires "
    "Emerson measurement, control, and safety systems at every stage; each LNG train "
    "generates $50-150M of instrumentation and automation content for EMR. "
    "ASPENTECH + NI ADD SOFTWARE BREADTH: AspenTech (~55% stake, $10B+ market cap) "
    "provides process optimization SaaS at 60%+ EBITDA margins; NI adds semiconductor, "
    "EV, and aerospace test & measurement — both diversify EMR beyond energy capex. "
    "THE HONEST RISK: oil/gas customer concentration is real; a sustained energy capex "
    "downturn (-15-20%) would compress orders before DeltaV installed-base service offsets; "
    "NI integration ($165M synergy target) is in execution; 47 consecutive dividend "
    f"increases will continue. Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × "
    f"{PE_CONSERVATIVE:.0f}× + ${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → "
    f"{CONS_RETURN:.1f}%. Accumulate steadily; add on energy-cycle-fear "
    f"pullbacks toward $110-118. "
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
    print("  • Energy capex concentration is a genuine risk: oil/gas customers")
    print("    represent ~45-50% of EMR revenue; a sustained energy capex")
    print("    downturn (-15-20%) would compress orders 2-3 quarters before")
    print("    the DeltaV installed-base service revenue provides full offset")
    print("  • NI integration is in early execution: $165M synergy target over")
    print("    3 years requires cost rationalization, sales force integration,")
    print("    and R&D portfolio alignment — operational complexity at this")
    print("    stage of transformation adds execution risk")
    print("  • Conservative 2yr floor ($123) is -8.8% below current price;")
    print("    the transformation story commands a premium multiple that")
    print("    could compress if execution falters")
    print("  • AspenTech stake (~55%) introduces mark-to-market exposure;")
    print("    AspenTech's own customer concentration in energy and chemicals")
    print("    means both EMR and AZPN move together in an energy downcycle")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • DeltaV DCS switching costs are among the deepest in industrial")
    print("    automation: changing the distributed control system of a refinery")
    print("    or LNG terminal requires recertifying every instrument loop,")
    print("    retraining every operator, and re-validating every safety interlock")
    print("    — a 2-5 year project costing $50-200M in a facility worth $5B+;")
    print("    customers simply do not switch; once specified, DeltaV generates")
    print("    service/upgrade revenue for the life of the facility")
    print("  • The LNG buildout is a confirmed, contracted, multi-year order cycle:")
    print("    $150B+ in sanctioned US LNG export projects (Plaquemines, Port")
    print("    Arthur 2, CP2, Lake Charles, Corpus Christi Stage 3) will each")
    print("    require $50-150M of Emerson instrumentation and control content;")
    print("    this backlog is FID-approved and cannot be cancelled without")
    print("    losing billions in project economics")
    print("  • AspenTech is an underappreciated hidden asset: ~55% of a $10B+")
    print("    market-cap process optimization software company (60%+ EBITDA")
    print("    margins, 90%+ gross margins, growing ARR) embedded in EMR's")
    print("    balance sheet at a carrying value below public market value;")
    print("    the software revenue layer is what separates EMR from pure")
    print("    hardware automation peers")
    print("  • 47 consecutive dividend growth years is a Dividend King benchmark")
    print("    that reflects FCF durability through every industrial cycle;")
    print("    management has never cut the dividend and never will")
    print("  • Ratio B 0.93× — downside 33.3% / upside 35.6% — the LNG and")
    print("    automation tailwinds create the asymmetry; DeltaV switching costs")
    print("    and dividend consistency create the floor")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Emerson Electric spent 2022-2024 transforming itself from a sprawling")
    print("  conglomerate into a focused automation platform — selling Climate")
    print("  Technologies, buying National Instruments, deepening AspenTech. The")
    print("  result is a company whose DeltaV DCS is specification-locked into half")
    print("  the world's LNG terminals and refineries, whose AspenTech software")
    print("  optimizes those same facilities, and whose NI equipment tests the")
    print("  semiconductors and EV batteries going into the next industrial cycle.")
    print("  At $135 — 33.3% from bear, 35.6% from bull, 47-year dividend growth")
    print("  as the floor — accumulate steadily. Add on energy-fear pullbacks to")
    print("  $110-118.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
