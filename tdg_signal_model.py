"""
TransDigm Group Incorporated (NYSE: TDG) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.94×  |  EPP Gap: +218.2%
=======================================================================
THE AEROSPACE AFTERMARKET PRICING MACHINE — SOLE-SOURCED COMPONENTS WITH
PERMANENT PRICING POWER: TransDigm acquires sole-sourced, FAA-certified
proprietary aerospace components businesses; installs value-based pricing
(charging what the market will bear for a certified part with no approved
substitute); extracts 50%+ EBITDA margins; uses the FCF to acquire more
sole-sourced businesses; repeats. The DOD calls this pricing "excessive."
The commercial aftermarket — 75%+ of revenue — has no such constraint.
60+ acquisitions since 1993. The most controversial, and most profitable,
model in aerospace.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "TDG"
COMPANY        = "TransDigm Group Incorporated"
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Aerospace & Defense · Sole-Sourced Proprietary Components / Aftermarket Parts / MRO · NYSE: TDG"
SECTOR_GROUP   = "Industrials"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 1400.00         # USD — mid-2026; long-term 20%+ CAGR compounder
ANNUAL_DIV     = 0.00            # no regular dividend; periodic special dividends (funded by leverage)
SHARES_OUT_B   = 0.057           # billions — minimal dilution; acquisition currency is debt, not equity

FW52_HIGH      = 1550.00
FW52_LOW       = 1100.00

# ── Scenario prices ───────────────────────────────────────────────────────────
# BEAR  — dual shock: (1) DoD pricing reform legislation passes, capping
#         sole-sourced defense part margins; (2) commercial aviation enters
#         a demand recession (RPM -15%+); leverage (~7-8× EBITDA) amplifies
#         earnings downside; multiple compresses toward 20× on FCF concerns
# BASE  — steady compounder: commercial aftermarket grows 8-10%/yr with
#         global air traffic, acquisition pipeline continues, defense headwinds
#         manageable; market prices ~$46 adj EPS at ~30× → ~$1,400
# BULL  — commercial aviation upcycle + acquisition acceleration: RPM
#         growth above trend drives MRO demand; TDG deploys $3-4B/yr in
#         accretive acquisitions; adj EPS $55+ by 2028; re-rates toward 35×
# XBULL — full pricing/commercial/M&A tailwind: no DoD reform, commercial
#         aviation supercycle, capital allocation excellence sustained;
#         30-year CAGR continues; re-rates toward premium aerospace platform
BEAR           = 875.0
BASE           = 1400.0
BULL           = 1960.0
XBULL          = 2400.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: DoD pricing headwinds + commercial downturn + leverage cost;
# TDG still earns ~$22/sh adj at trough on sole-sourced commercial content
# PE_TROUGH: 20× reflects aerospace components floor even in adversity
# (specification lock-in means earnings don't go to zero in any scenario)
EPS_TROUGH     = 22.00
PE_TROUGH      = 20.0
EPP            = EPS_TROUGH * PE_TROUGH     # $440.00

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E adj EPS ~$46 × 28× conservative aerospace-compounder multiple
# Conservative case -8.0% — high-quality compounder floors the downside
PE_CONSERVATIVE  = 28.0
EPS_FY2026E      = 46.00
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $1,288.00

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

# ── Bottom-up signal factors ───────────────────────────────────────────────────
# (name, conviction 1-5, weight)
SIGNALS = [
    ("sole_sourced_faa_certified_aftermarket_pricing_power_and_certification_lock", 4.5, 0.25),
    ("commercial_aviation_recovery_and_aftermarket_mro_demand_growth",             4.0, 0.20),
    ("dod_defense_pricing_scrutiny_congressional_reform_and_regulatory_risk",      2.0, 0.18),
    ("acquisition_machine_60_plus_deals_and_serial_value_creation_track_record",   4.0, 0.15),
    ("extreme_leverage_20b_net_debt_7_8x_ebitda_and_interest_rate_sensitivity",    2.0, 0.12),
    ("premium_valuation_amortization_earnings_quality_and_crowding_risk",          2.5, 0.10),
]

# ── Structural Competitive Advantage (SCA) factors ────────────────────────────
SCA_FACTORS = {
    "sole_sourced_faa_certified_parts_specification_lock_in_zero_approved_substitutes": +0.28,
    "commercial_aftermarket_75pct_revenue_unconstrained_value_based_pricing":           +0.18,
    "60_plus_acquisition_compounding_model_since_1993_and_proven_playbook":             +0.14,
    "dod_pricing_scrutiny_congressional_investigations_and_potential_reform_risk":      -0.18,
    "extreme_leverage_20b_plus_net_debt_7_8x_ebitda_and_rising_rate_sensitivity":      -0.14,
    "amortization_heavy_income_statement_earnings_quality_and_reported_eps_debate":    -0.08,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.20

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"TDG ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE AEROSPACE AFTERMARKET PRICING MACHINE — SOLE-SOURCED COMPONENTS WITH PERMANENT "
    "PRICING POWER: TransDigm acquires sole-sourced, FAA-certified proprietary aerospace "
    "components; installs value-based pricing on parts with no approved substitute; extracts "
    "~50%+ EBITDA margins; deploys the FCF into the next acquisition. 60+ deals since 1993. "
    "~20%+ annualized total return since IPO. The commercial aftermarket (~75% of revenue) "
    "is structurally unconstrained: when an airline needs a certified replacement part for "
    "an aircraft in service, it pays what TDG charges — there is no alternative, no "
    "competitive tender, and no delay acceptable in commercial aviation maintenance. "
    "THE CERTIFICATION MOAT IS PERMANENT: each FAA Part Manufacturing Approval (PMA) "
    "locks a specific TDG part onto a specific aircraft type for its entire service life "
    "(20-30+ years); generating PMA approvals for alternatives costs competitors millions "
    "and takes 3-5 years — by which time TDG has raised the price again. "
    "THE ACQUISITION FLYWHEEL: TDG identifies sole-sourced businesses, acquires at "
    "reasonable prices, implements the proprietary cost/pricing playbook, and immediately "
    "generates IRRs that justify the leverage; $3-4B/yr of deployment capacity at "
    "~15-20% target returns has compounded shareholder value for three decades. "
    "THE HONEST RISK: DoD pricing reform is real — the Pentagon has documented TDG "
    "parts at 3,000-9,000% markups; bipartisan congressional pressure for spare parts "
    "pricing legislation represents a genuine, if slow-moving, regulatory risk to the "
    "~25% of revenue from defense aftermarket; extreme leverage (~$20B net debt, "
    f"~7-8× EBITDA) means any earnings shortfall amplifies to the equity. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.0f} × {PE_CONSERVATIVE:.0f}× = "
    f"${CONSERVATIVE_PRICE:.0f} → {CONS_RETURN:.1f}% — high-quality compounder "
    "floors the downside; BULL/XBULL require commercial aviation upcycle and "
    "continued M&A accretion. Accumulate steadily; add on DoD-fear pullbacks "
    f"toward $1,175-1,250. "
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
    print(f"  Conservative Price ({EPS_FY2026E:.0f} × {PE_CONSERVATIVE:.0f}×):       ${CONSERVATIVE_PRICE:>8.2f}  ({CONS_RETURN:>+.1f}%)")
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
    print("  • DoD pricing reform is the asymmetric risk: bipartisan congressional")
    print("    support for spare parts pricing legislation is growing — DoD audits")
    print("    have documented TDG parts at 3,000-9,000% markups; if legislation")
    print("    caps sole-sourced defense part margins at cost-plus, it directly")
    print("    impairs ~25% of revenue at disproportionately high margins")
    print("  • ~$20B net debt at ~7-8× EBITDA means the equity is highly levered:")
    print("    a 15% EBITDA decline doubles the equity impairment; rising interest")
    print("    rates directly hit FCF via floating-rate debt refinancing; the")
    print("    leverage is managed expertly but it is genuinely extreme")
    print("  • Conservative 2yr floor ($1,288) is -8.0% below current — modest")
    print("    downside for a quality compounder, but the leverage amplifies any")
    print("    earnings surprise to the downside meaningfully")
    print("  • Reported EPS is substantially below adj EPS due to ~$1.5-2B/yr in")
    print("    amortization of acquired intangibles; the earnings quality debate")
    print("    is legitimate and limits the investor universe")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The FAA certification moat is as permanent as any moat in investing:")
    print("    once a TDG part is on an aircraft's maintenance manual, it stays there")
    print("    for the aircraft's entire service life; generating a PMA alternative")
    print("    costs $3-5M and 3-5 years — by which time TDG has raised the price")
    print("    twice; the commercial aftermarket earns these returns legally and")
    print("    with complete ethical clarity (airlines accept the pricing because")
    print("    grounding a plane costs $100,000+/day)")
    print("  • The acquisition model has compounded for 30 years without a failed")
    print("    deal thesis: TDG acquires sole-sourced businesses at reasonable prices,")
    print("    extracts cost savings, installs pricing discipline, and generates")
    print("    20%+ IRRs consistently; the pipeline of acquirable aerospace component")
    print("    businesses remains large, and TDG's cost of capital advantage means")
    print("    it outbids any financial buyer for these assets")
    print("  • Commercial aviation is a structural growth market: global air traffic")
    print("    grows ~4-5%/yr long-term; every RPM generates MRO demand; the global")
    print("    commercial fleet is aging (average age 12+ years), driving accelerating")
    print("    aftermarket spending per aircraft; TDG participates in this growth at")
    print("    ~50% EBITDA margins with no capital intensity")
    print("  • Ratio B 0.94× — downside 37.5% / upside 40.0% — the specification")
    print("    lock-in and acquisition flywheel create the asymmetry; the DoD risk")
    print("    and leverage create the downside that makes it 0.94×, not 0.70×")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  TransDigm has spent 30 years building the most defensible revenue stream")
    print("  in aerospace: 50%+ EBITDA margins on sole-sourced parts that airlines")
    print("  MUST buy because no alternative is FAA-certified and a grounded aircraft")
    print("  costs more per day than the part costs per year. The model is controversial")
    print("  — the DoD audit findings are real and the defense pricing risk is not")
    print("  trivial — but the commercial aftermarket is 75% of revenue and entirely")
    print("  unconstrained. Thirty years of 20%+ annual compounding is not an accident;")
    print("  it is the systematic exploitation of a structural advantage that no")
    print("  competitor has found a way around. At $1,400 — 37.5% from bear, 40.0%")
    print("  from bull — accumulate. Add on DoD-fear pullbacks to $1,175-1,250.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
