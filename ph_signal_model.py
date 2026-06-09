"""
Parker Hannifin Corporation (NYSE: PH) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.94×  |  EPP Gap: +151.9%
=======================================================================
THE WORLD'S MOST DIVERSIFIED MOTION AND CONTROL FRANCHISE — NOW WITH
AEROSPACE: Parker Hannifin has quietly compounded at 15%+ total returns
for 30+ years through disciplined capital allocation, the relentless
margin-improvement "Win Strategy," and the most diversified portfolio of
motion/control/fluid technologies on earth — now augmented by Meggitt plc
(sole-sourced fuel systems, thermal management, sealing on every major
Western commercial and defense aircraft). 67+ consecutive years of
dividend growth. The Meggitt integration is the catalyst for the next
leg of margin and earnings expansion.
"""

# ── Model identity ─────────────────────────────────────────────────────────────
TICKER         = "PH"
COMPANY        = "Parker Hannifin Corporation"
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Diversified Industrials · Motion & Control / Aerospace Systems / Fluid Power · NYSE: PH"
SECTOR_GROUP   = "Industrials"

# ── Price & share data ─────────────────────────────────────────────────────────
CURRENT_PRICE  = 680.00          # USD — mid-2026; re-rated on Meggitt integration progress + aerospace
ANNUAL_DIV     = 6.80            # USD/yr (~1.0% yield); 67+ consecutive years of dividend growth
SHARES_OUT_B   = 0.128           # billions (consistent buybacks; high per-share earnings power)

FW52_HIGH      = 750.00
FW52_LOW       = 530.00

# ── Scenario prices ────────────────────────────────────────────────────────────
# BEAR  — industrial cycle downturn: global manufacturing capex falls 15-20%,
#         aerospace cycle softens (OEM production delays, defense budget pressure),
#         Meggitt integration costs linger longer than expected; multiple
#         compresses toward trough diversified-industrial valuation
# BASE  — Meggitt integration executing on plan: aerospace margins approaching
#         Parker's historical standards, industrial automation exposure steady,
#         Win Strategy targets progressing; market prices $28.50 EPS at ~23×
#         → ~$680 fair value on quality-industrial premium
# BULL  — aerospace re-rate + industrial upcycle: Meggitt fully integrated
#         at Parker margins (aerospace EBIT 25%+ vs. Meggitt's ~15%); commercial
#         aviation recovery drives aftermarket; US reshoring and electrification
#         drive industrial automation demand; multiple expands toward 28-30×
# XBULL — premium compounder re-rate: market recognizes Parker as a Danaher/
#         Roper-class quality industrial; 30%+ operating margins sustained;
#         dividend growth + buybacks compound at 12-15%/yr indefinitely
BEAR           = 455.0
BASE           = 680.0
BULL           = 920.0
XBULL          = 1100.0

# ── Earnings Power Price (EPP) floor ───────────────────────────────────────────
# EPS_TROUGH: industrial cycle trough + aerospace softness — Parker's
# diversification limits the downside; still earns ~$15/sh at the nadir
# PE_TROUGH: 18× reflects diversified-industrial-with-aerospace floor
EPS_TROUGH     = 15.00
PE_TROUGH      = 18.0
EPP            = EPS_TROUGH * PE_TROUGH     # $270.00

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E EPS ~$28.50 × 22× conservative quality-industrial multiple + $6.80 div
# Conservative case -6.8% — quality franchise limits downside meaningfully
PE_CONSERVATIVE  = 22.0
EPS_FY2026E      = 28.50
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $633.80

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

# ── Bottom-up signal factors ─────────────────────────────────────────────────────
# (name, conviction 1-5, weight)
SIGNALS = [
    ("aerospace_systems_meggitt_integration_and_sole_sourced_aircraft_content",  4.0, 0.24),
    ("win_strategy_margin_expansion_and_capital_allocation_compounding",          4.0, 0.20),
    ("diversified_industrial_automation_electrification_and_reshoring_exposure", 3.5, 0.18),
    ("67yr_dividend_growth_king_and_long_term_compounder_track_record",          4.0, 0.14),
    ("industrial_cycle_and_global_manufacturing_capex_sensitivity",              2.5, 0.14),
    ("meggitt_leverage_reduction_integration_execution_and_cost_synergies",      3.0, 0.10),
]

# ── Structural Competitive Advantage (SCA) factors ──────────────────────────────
SCA_FACTORS = {
    "aerospace_sole_sourced_content_meggitt_plus_original_ph_aviation_portfolio":   +0.22,
    "win_strategy_culture_margin_expansion_and_25_pct_plus_operating_income_target": +0.16,
    "9000_plus_product_lines_and_diversification_across_motion_control_fluid_power": +0.12,
    "67_consecutive_dividend_increases_and_disciplined_buyback_compounding":         +0.10,
    "industrial_cycle_exposure_and_global_manufacturing_capex_sensitivity":          -0.12,
    "meggitt_integration_costs_debt_leverage_and_execution_risk_residual":           -0.08,
    "premium_23_25x_valuation_and_quality_compounder_crowding_risk":                 -0.08,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.32

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"PH ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE WORLD'S MOST DIVERSIFIED MOTION AND CONTROL FRANCHISE — NOW WITH AEROSPACE: "
    "Parker Hannifin has compounded at 15%+ total returns for 30+ years through disciplined "
    "capital allocation, the relentless 'Win Strategy' margin improvement culture, and 9,000+ "
    "product lines across motion/control/fluid/thermal/filtration technologies — now "
    "augmented by Meggitt plc (~$8.8B, 2021) adding sole-sourced fuel systems, thermal "
    "management, sealing, and sensing on every major Western commercial and defense aircraft. "
    "AEROSPACE SYSTEMS IS THE HIDDEN CATALYST: Meggitt is being integrated at Parker's "
    "operating margin standards (~25%+ target vs. Meggitt's ~15% standalone) — every 100bps "
    "of margin improvement on Meggitt's ~$2.5B revenue adds ~$25M EBIT; full integration "
    "represents $250M+ in incremental EBIT yet to be recognized; aerospace aftermarket "
    "(OEM + MRO) is recurring, specification-driven, and sole-sourced — no competitive "
    "threat without a 5-10yr recertification process. "
    "THE WIN STRATEGY COMPOUNDS RELENTLESSLY: 67+ consecutive years of dividend growth "
    f"(${ANNUAL_DIV:.2f}/yr); Parker has expanded operating margins from ~10% (2015) toward "
    "25%+ (2026 target) through lean manufacturing, portfolio pruning, and pricing discipline "
    "— a management culture proven across multiple industrial cycles. "
    "THE HONEST RISK: industrial cycles are real; Parker's broad manufacturing exposure "
    "means a global capex downturn (10-15% decline) compresses earnings before the "
    "aerospace annuity fully cushions; at 23-25× forward EPS the stock is priced for "
    "quality, not deep value. "
    f"Conservative 2yr: EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — "
    "quality franchise with genuine downside cushion. "
    "A DANAHER-CLASS COMPOUNDER AT A FAIR PRICE: accumulate steadily; add on any "
    f"industrial-cycle-fear pullback toward $575-615. "
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
    print(f"  {'Factor':<63} {'Conv':>4}  {'Wt':>5}")
    print(f"  {'-'*72}")
    for name, conv, wt in SIGNALS:
        print(f"  {name:<63} {conv:>4.1f}  {wt:>5.0%}")
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
    print("  • At 23-25× forward EPS, Parker is priced as a quality compounder —")
    print("    fair value, not deep value; the Meggitt integration catalyst is")
    print("    well-understood and substantially reflected in consensus estimates")
    print("  • Industrial cycles are real and Parker has broad exposure: a 15-20%")
    print("    decline in global manufacturing capex (e.g., 2015-16 or 2019 type")
    print("    downturn) would compress earnings 15-20% before the aerospace annuity")
    print("    provides full cushion — the conservative floor (-6.8%) is modest but real")
    print("  • Meggitt integration is largely behind them but not complete: residual")
    print("    IT system integration, supplier qualification, and plant consolidation")
    print("    create execution risk that could delay the full margin realization")
    print("  • Share price is in high-absolute-dollar territory ($680); with only")
    print("    128M shares outstanding, even modest institutional selling can create")
    print("    meaningful price impact — liquidity matters at this price level")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The Meggitt acquisition transformed Parker's aerospace content:")
    print("    fuel systems (actuates every fuel valve on a commercial aircraft),")
    print("    thermal management (cooling for engines, avionics, cabin), sealing")
    print("    and sensing across every Western commercial and defense platform —")
    print("    these are sole-sourced components that cannot be changed mid-program")
    print("    without 3-5 years of FAA/EASA recertification; pricing power is permanent")
    print("  • Win Strategy is not a slogan — it is a proven, 20-year compounding machine:")
    print("    Parker expanded operating margins from ~10% in 2015 to ~25%+ by 2026")
    print("    through lean transformation, pricing discipline, and SG&A leverage;")
    print("    this same playbook is being applied to Meggitt's ~15% margins")
    print("    — representing $250M+ in incremental EBIT still ahead")
    print("  • 67 consecutive years of dividend growth through recessions, wars,")
    print("    pandemics, and industrial cycles is not an accident — it reflects a")
    print("    management culture and FCF generation profile that compounds regardless")
    print("    of economic environment")
    print("  • 9,000+ product lines across motion, control, fluid power, thermal,")
    print("    filtration, and sealing means no single end-market can impair the")
    print("    franchise; diversification is structural, not accidental")
    print("  • Ratio B 0.94× — downside 33.1% / upside 35.3% — asymmetry favors")
    print("    the bull; aerospace content and Win Strategy create the upside;")
    print("    9,000-product diversification and 67-year dividend record create the floor")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Parker Hannifin is the industrial company that has been hiding in plain")
    print("  sight for decades — too diversified to attract a simple narrative, too")
    print("  consistent to generate excitement, too disciplined to make dramatic")
    print("  mistakes. The Meggitt acquisition changed the story: Parker is now a")
    print("  diversified industrial AND a premium aerospace content provider, with a")
    print("  management culture proven across every cycle to extract more margin from")
    print("  every acquired asset than the previous owner ever did. At $680 — 33.1%")
    print("  from bear, 35.3% from bull, with 67 consecutive dividend increases as the")
    print("  floor — accumulate steadily. Add on industrial-fear pullbacks to $575-615.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
