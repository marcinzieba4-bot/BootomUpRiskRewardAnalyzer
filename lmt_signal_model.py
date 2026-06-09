"""
Lockheed Martin Corporation (NYSE: LMT) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.86×  |  EPP Gap: +65.6%
=======================================================================
THE ESSENTIAL ARSENAL OF DEMOCRACY — F-35, HIMARS, PAC-3, AND NATO'S
REARMAMENT DECADE: Lockheed Martin is the world's largest defense
contractor by revenue, the sole-source producer of the F-35 (the largest
defense program in history — $1.7T lifetime value across 17 nations),
and the manufacturer of the precision-fires systems (HIMARS, GMLRS,
PAC-3, THAAD) that NATO allies are re-ordering at record pace post-Ukraine.
A geopolitical era of sustained elevated defense spending is the tailwind;
the question is whether domestic budget politics or program execution risk
disrupts the compounding.
"""

# ── Model identity ─────────────────────────────────────────────────────────────
TICKER         = "LMT"
COMPANY        = "Lockheed Martin Corporation"
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Aerospace & Defense · Fighter Aircraft / Missiles / Rotary Wing / Space · NYSE: LMT"
SECTOR_GROUP   = "Industrials"

# ── Price & share data ─────────────────────────────────────────────────────────
CURRENT_PRICE  = 510.00          # USD — mid-2026; solid performer on NATO spending tailwind
ANNUAL_DIV     = 12.60           # USD/yr (~2.5% yield); 22+ consecutive years of dividend growth
SHARES_OUT_B   = 0.234           # billions — aggressive buybacks shrinking float steadily

FW52_HIGH      = 580.00
FW52_LOW       = 430.00

# ── Scenario prices ────────────────────────────────────────────────────────────
# BEAR  — US defense budget cuts materialize: reconciliation bill reduces
#         DoD topline, DOGE efficiency mandates compress contract margins,
#         F-35 TR-3 upgrade delays extend and cost overruns widen, some
#         international orders deferred; multiple compresses toward trough
# BASE  — steady-state compounder: defense budgets hold roughly flat in real
#         terms, F-35 production at ~150/yr, NATO allies continuing multi-year
#         order commitments, HIMARS/PAC-3 backlog executing, capital returns
#         sustain; market prices $27-28 EPS at 18× → ~$510 fair value
# BULL  — NATO 3% GDP spending commitment realized: European allies accelerate
#         F-35, HIMARS, Patriot orders; hypersonics/next-gen programs (NGAD,
#         PCA) award wins; Sikorsky CH-53K ramp; space/SBIRS/GPS III scale
# XBULL — generational rearmament decade confirmed: US + allied defense
#         spending at post-Cold War highs for a decade; major new platform wins;
#         LMT re-rates toward premium compounder multiple on sustained growth
BEAR           = 390.0
BASE           = 510.0
BULL           = 650.0
XBULL          = 775.0

# ── Earnings Power Price (EPP) floor ───────────────────────────────────────────
# EPS_TROUGH: budget-cut scenario — sequestration-level cuts compress margins;
# ~$22/sh reflects genuine downturn but not program cancellation (F-35 is
# politically, strategically, and contractually entrenched)
# PE_TROUGH: 14× reflects defense compounder floor (LMT never traded below
# 12-13× even in worst budget environments)
EPS_TROUGH     = 22.00
PE_TROUGH      = 14.0
EPP            = EPS_TROUGH * PE_TROUGH     # $308.00

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E EPS ~$27.50 × 18× conservative defense multiple + $12.60 div
# Conservative case essentially flat — stock is fairly valued, not cheap;
# upside requires NATO spending acceleration or new platform wins
PE_CONSERVATIVE  = 18.0
EPS_FY2026E      = 27.50
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $507.60

# ── Signal computation ──────────────────────────────────────────────────────────
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
    ("f35_program_sole_source_dominance_and_1p7t_lifetime_value",          4.5, 0.25),
    ("record_nato_ally_rearmament_and_allied_defense_spending_cycle",       4.0, 0.20),
    ("missiles_himars_pac3_thaad_precision_fires_record_backlog",           3.5, 0.18),
    ("us_defense_budget_doge_fiscal_constraint_and_sequestration_risk",     2.0, 0.17),
    ("sikorsky_rotary_wing_space_and_next_generation_platform_pipeline",    3.0, 0.12),
    ("f35_tr3_block_upgrade_production_delays_and_execution_risk",          2.5, 0.08),
]

# ── Structural Competitive Advantage (SCA) factors ─────────────────────────────
SCA_FACTORS = {
    "f35_multi_decade_sole_source_production_and_17_nation_lifecycle_services": +0.25,
    "165b_plus_backlog_and_government_contract_revenue_visibility":              +0.14,
    "himars_pac3_thaad_gmlrs_in_record_demand_post_ukraine_nato_restocking":     +0.12,
    "sikorsky_black_hawk_ch53k_and_national_security_space_portfolio":           +0.09,
    "us_defense_budget_doge_and_fiscal_reconciliation_top_line_risk":            -0.12,
    "f35_tr3_upgrade_delays_cost_overruns_and_production_ramp_risk":             -0.08,
    "geopolitical_de_escalation_could_reduce_allied_order_urgency":              -0.06,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.34

# ── Weighted conviction score ────────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ────────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ────────────────────────────────────────────────────────────────
SUMMARY = (
    f"LMT ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE ESSENTIAL ARSENAL OF DEMOCRACY — F-35, HIMARS, PAC-3, AND NATO'S REARMAMENT DECADE: "
    "world's largest defense contractor by revenue; sole-source producer of the F-35 "
    "(3,300+ aircraft ordered across 17 nations, ~$1.7T lifetime program value — the largest "
    "defense program in history); manufacturer of HIMARS, GMLRS, PAC-3/LTAMDS, THAAD — "
    "the precision-fires systems NATO allies are re-ordering at record pace post-Ukraine. "
    "~$165B backlog = 2.5 years of revenue with near-certainty; Sikorsky Black Hawk, CH-53K "
    "marine heavy lift, GPS III/SBIRS national security satellites complete the portfolio. "
    "FINANCIAL COMPOUNDING IS EXCEPTIONAL: FY2026E EPS ~$27.50; 22+ consecutive dividend "
    f"increases (${ANNUAL_DIV:.2f}/yr, ~2.5% yield); aggressive buybacks shrinking share "
    "count from 0.29B → 0.234B; FCF conversion ~100%+ of net income. "
    "THE HONEST RISK: US defense budget politics are real — DOGE efficiency mandates, "
    "reconciliation bill top-line pressure, and potential program repricing create genuine "
    "near-term uncertainty; F-35 TR-3 block upgrade delays have already cost schedule slippage "
    "and margin pressure; any meaningful geopolitical de-escalation would reduce allied order "
    f"urgency. Conservative 2yr: EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.0f} → {CONS_RETURN:.1f}% — "
    "essentially fair value; BULL/XBULL require NATO spending acceleration or new platform wins. "
    "A WORLD-CLASS FRANCHISE AT A FAIR-TO-ATTRACTIVE PRICE: accumulate steadily; add "
    f"aggressively on any budget-fear pullback toward $445-470. "
    f"Bear ${BEAR:.0f} · Base ${BASE:.0f} · Bull ${BULL:.0f} · XBull ${XBULL:.0f}."
)

# ─────────────────────────────────────────────────────────────────────────────────
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
    print("  • At ~18-19× forward EPS, LMT is fairly valued — not cheap; the NATO")
    print("    rearmament tailwind is well-understood and substantially priced in")
    print("  • Conservative 2yr floor ($508) is essentially AT current price — the")
    print("    margin of safety is thin on a pure earnings-multiple basis")
    print("  • DOGE and fiscal reconciliation represent genuine top-line risk: defense")
    print("    is no longer exempt from budget scrutiny, and even flat-real spending")
    print("    growth constrains the bull case")
    print("  • F-35 TR-3 block upgrade (ALIS → ODIN software overhaul, advanced")
    print("    avionics suite) has already caused production pauses and margin pressure;")
    print("    further delays would compress near-term EPS and cash flow")
    print("  • Share count reduction (~0.29B → 0.234B) is impressive but decelerating")
    print("    as the stock price rises — buyback accretion diminishes at $510")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The F-35 program is the closest thing to guaranteed revenue in defense:")
    print("    17 partner nations, 3,300+ aircraft on order, ~45-year lifecycle of")
    print("    sustainment/upgrades, and political entrenchment so deep that no US")
    print("    administration has seriously threatened its continuation")
    print("  • NATO members committed to 3% GDP defense spending targets in 2024-25;")
    print("    European allies are accelerating F-35, Patriot/LTAMDS, and HIMARS orders")
    print("    — multi-year, government-to-government contracts with 5-10 year delivery")
    print("    timelines that create visible, durable revenue regardless of US politics")
    print("  • HIMARS/GMLRS proved itself on the battlefield in Ukraine; demand from")
    print("    Poland (~500 HIMARS), Romania, Germany, and Indo-Pacific allies represents")
    print("    a multi-billion, multi-year precision fires backlog building in real time")
    print("  • ~$165B backlog = 2.5 years of revenue already contracted; unlike")
    print("    commercial aerospace, defense contracts are highly unlikely to be")
    print("    cancelled after award — true revenue visibility is exceptional")
    print("  • Ratio B 0.85× — downside 23.5% / upside 27.5% — asymmetry genuinely")
    print("    favors the bull; 2.5% dividend yield while you wait")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Lockheed Martin is the irreplaceable armorer of the Western alliance at")
    print("  the moment the Western alliance has decided to rearm for a generation.")
    print("  The F-35 is not a product — it is a 50-year commitment: every aircraft")
    print("  delivered generates decades of training, parts, upgrades, and sustainment")
    print("  revenue that compounds long after the production line slows. HIMARS proved")
    print("  itself operationally; NATO allies are buying it as fast as LMT can build.")
    print("  The domestic budget risk is real and worth monitoring, but even in a")
    print("  sequestration scenario, the F-35 and allied-nation programs continue.")
    print("  At $510 — 23.5% from bear, 27.5% from bull, 2.5% yield — accumulate")
    print("  steadily. Add more aggressively on any budget-fear pullback to $445-470.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
