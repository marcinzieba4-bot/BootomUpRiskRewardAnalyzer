"""
DSV A/S (Nasdaq Copenhagen: DSV) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.89×  |  EPP Gap: +188.9%
=======================================================================
NOTE: All prices in Danish Krone (DKK). DSV trades on Nasdaq Copenhagen.
=======================================================================
THE SERIAL ACQUISITION MACHINE THAT KEEPS OUTPERFORMING: DSV has compounded
shareholder value for two decades by acquiring underperforming freight
forwarders — PANALPINA (2019, CHF 4.6B), Agility GIL (2021, $4.2B), DB
Schenker (2025, €14.3B) — and applying its ruthlessly efficient operating
model to close the margin gap. Each time, the market underestimated the
integration; each time, DSV delivered above target. DB Schenker brings
~€20B in revenue, a pan-European road network, and a contract logistics
business running at 5-6% EBIT margins — versus DSV's 8-10%+ target. The
margin gap is the thesis; the track record is the conviction.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "DSV"
COMPANY        = "DSV A/S"
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Industrials · Freight Forwarding / Contract Logistics / Road & Air & Sea · Nasdaq Copenhagen: DSV (Prices in DKK)"
SECTOR_GROUP   = "Industrials"
CURRENCY       = "DKK"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 1300.00         # DKK — post-DB Schenker (closed Jan 2025); integration discount persists
ANNUAL_DIV     = 7.00            # DKK/yr (~0.5% yield); DSV is a growth compounder, not an income stock
SHARES_OUT_B   = 0.200           # billions

FW52_HIGH      = 1480.00
FW52_LOW       = 1020.00

# ── Scenario prices (DKK) ────────────────────────────────────────────────────
# BEAR  — integration disappointment + freight downcycle: DB Schenker margins
#         stall at 5-6% (fail to close gap to DSV target); global trade volumes
#         contract on tariff escalation; leverage from €14.3B acquisition
#         becomes uncomfortable; multiple re-rates toward 14-15× trough
# BASE  — integration on track: Schenker EBIT margins migrate from 5-6% toward
#         7-8% by 2027; freight cycle normalizes; EPS DKK 68 × 19× + DKK 7 div
# BULL  — playbook repeats: Schenker margins reach 9%+ ahead of schedule; air &
#         sea volumes recover strongly; DSV takes market share; multiple re-rates
#         to 22-23× as the market prices the earnings power
# XBULL — DSV becomes the world's undisputed #1 freight forwarder: another
#         acquisition or Schenker delivering above-target margins; DHL Global
#         Forwarding or Kuehne+Nagel market share capture; EPS DKK 110+ by 2028
BEAR           = 900.0
BASE           = 1300.0
BULL           = 1750.0
XBULL          = 2200.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: freight downcycle + integration costs; core DSV + Schenker still
# earns ~DKK 30/sh on essential logistics flows; trough cycle
# PE_TROUGH: 15× for proven serial acquirer even in distress
EPS_TROUGH     = 30.00
PE_TROUGH      = 15.0
EPP            = EPS_TROUGH * PE_TROUGH     # DKK 450.00

# ── Conservative 2-year price estimate ───────────────────────────────────────
# FY2027E adj EPS ~DKK 68 × 19× conservative multiple + DKK 7 div
# Conservative case essentially flat (-0.1%) — Schenker integration at fair value
PE_CONSERVATIVE  = 19.0
EPS_FY2026E      = 68.00
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # DKK 1,299.00

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

# ── Bottom-up signal factors ─────────────────────────────────────────────────
# (name, conviction 1-5, weight)
SIGNALS = [
    ("db_schenker_margin_uplift_thesis_5_6pct_to_8_10pct_ebit_proven_dsv_playbook",       4.0, 0.22),
    ("serial_acquisition_machine_panalpina_agility_schenker_each_integration_beat",       4.0, 0.20),
    ("asset_light_freight_forwarding_high_roce_and_operating_leverage_on_volume_recovery",3.5, 0.17),
    ("european_road_freight_network_density_and_contract_logistics_switching_costs",       3.0, 0.17),
    ("freight_cycle_normalization_from_2023_24_trough_air_sea_rate_recovery",             3.0, 0.14),
    ("eur14b_schenker_debt_load_integration_complexity_and_freight_cycle_sensitivity",    2.5, 0.10),
]

# ── Structural Competitive Advantage (SCA) factors ───────────────────────────
SCA_FACTORS = {
    "serial_acquisition_compounding_three_major_integrations_all_beating_targets":        +0.18,
    "asset_light_high_roce_model_freight_forwarding_capital_efficiency":                  +0.14,
    "db_schenker_margin_gap_5_6pct_vs_8_10pct_target_represents_large_value_unlock":     +0.12,
    "european_road_network_density_and_long_term_contract_logistics_customer_stickiness": +0.08,
    "eur14b_schenker_leverage_and_integration_complexity_in_freight_downcycle":           -0.14,
    "freight_forwarding_cyclicality_volume_and_rate_sensitivity_to_global_trade":         -0.10,
    "integration_execution_risk_at_scale_largest_deal_in_dsv_history":                   -0.06,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.22

# ── Weighted conviction score ─────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ────────────────────────────────────────────────────────────
SUMMARY = (
    f"DSV ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor DKK {EPP:.0f} vs. price DKK {CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | All prices in DKK (Nasdaq Copenhagen). "
    "THE SERIAL ACQUISITION MACHINE THAT KEEPS OUTPERFORMING: DSV has built the world's "
    "largest freight forwarding empire by acquiring underperformers — PANALPINA (2019, "
    "CHF 4.6B), Agility GIL (2021, $4.2B), DB Schenker (2025, €14.3B) — and applying "
    "its ruthlessly efficient operating model to close the margin gap. Each time, the "
    "market underestimated the integration; each time, DSV delivered above target. "
    "THE DB SCHENKER THESIS: ~€20B revenue, pan-European road network, contract logistics "
    "— currently running at 5-6% EBIT margins vs. DSV's 8-10%+ target; the margin gap "
    "is the thesis, the track record is the conviction. Schenker also brings road freight "
    "density in Europe that DSV previously lacked — a strategic capability, not just a "
    "margin uplift story. "
    "ASSET-LIGHT AND HIGH-ROCE: freight forwarding requires minimal fixed capital — "
    "DSV buys and sells capacity rather than owning planes, ships, or trucks at scale; "
    "this delivers high returns on capital and operating leverage when volumes recover. "
    "THE HONEST RISK: €14.3B is the largest deal in DSV history, funded with significant "
    "debt — the leverage constrains optionality and amplifies any freight cycle downturn; "
    "freight forwarding is inherently cyclical (air & sea rates collapsed 60-70% from "
    "2022 peak to 2023 trough); integration at Schenker's scale (~45,000 employees) is "
    "operationally complex; a global trade slowdown on tariff escalation would compress "
    "volumes and rates simultaneously with elevated leverage. "
    f"Conservative 2yr: adj EPS DKK {EPS_FY2026E:.0f} × {PE_CONSERVATIVE:.0f}× + "
    f"DKK {ANNUAL_DIV:.0f} div = DKK {CONSERVATIVE_PRICE:.0f} → {CONS_RETURN:.1f}% — "
    "essentially flat; BULL/XBULL require Schenker margin convergence. "
    "Add on freight-cycle-driven pullbacks toward DKK 1,050-1,100 where Ratio B "
    f"approaches ◉ BUY territory. "
    f"Bear DKK {BEAR:.0f} · Base DKK {BASE:.0f} · Bull DKK {BULL:.0f} · XBull DKK {XBULL:.0f}."
)

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    C = "DKK"
    print(f"\n{'='*72}")
    print(f"  {TICKER}  |  {COMPANY}")
    print(f"  {SECTOR}")
    print(f"{'='*72}")
    print(f"  Current Price:                              {C} {CURRENT_PRICE:>10.2f}")
    print(f"  Annual Dividend:                            {C} {ANNUAL_DIV:>10.2f}")
    print(f"  52-Week Range:                  {C} {FW52_LOW:.2f} – {C} {FW52_HIGH:.2f}")
    print()
    print(f"  Scenario Prices ({C}):")
    print(f"    Bear:                                       {C} {BEAR:>10.2f}")
    print(f"    Base:                                       {C} {BASE:>10.2f}")
    print(f"    Bull:                                       {C} {BULL:>10.2f}")
    print(f"    XBull:                                      {C} {XBULL:>10.2f}")
    print()
    print(f"  Downside (current → bear):                    {DOWNSIDE_PCT*100:>7.1f}%")
    print(f"  Upside   (current → bull):                    {UPSIDE_PCT*100:>7.1f}%")
    print(f"  Ratio B = {RATIO_B:.4f} → {SIGNAL}")
    print()
    print(f"  EPS Trough:                                 {C} {EPS_TROUGH:>10.2f}")
    print(f"  PE Trough:                                         {PE_TROUGH:>8.1f}×")
    print(f"  EPP (Earnings Power Price):                 {C} {EPP:>10.2f}")
    print(f"  EPP Gap (current vs. EPP floor):              {EPP_GAP_PCT:>+8.1f}%")
    print()
    print(f"  Conservative Price ({EPS_FY2026E:.0f} × {PE_CONSERVATIVE:.0f}×):   {C} {CONSERVATIVE_PRICE:>10.2f}  ({CONS_RETURN:>+.1f}%)")
    print()
    print(f"  Weighted Conviction Score:                         {WCS:>8.2f} / 5.0")
    print(f"  SCA Net:                                           {SCA_NET:>+8.2f}")
    print(f"  EV(model): {C} {EV_MODEL:>8.2f}   Upside: {(EV_MODEL-CURRENT_PRICE)/CURRENT_PRICE*100:>+.1f}%   Downside: -{DOWNSIDE_PCT*100:.1f}%")
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
    print("  • €14.3B is real leverage at a real price: DSV's balance sheet")
    print("    went from near-net-cash to significant net debt to fund")
    print("    Schenker; in a freight downcycle (which happens every 5-7")
    print("    years), this leverage constrains capital allocation and")
    print("    amplifies earnings volatility in ways that compress the")
    print("    multiple before the integration can demonstrate its value")
    print("  • Schenker integration complexity is unprecedented: at ~45,000")
    print("    employees and €20B+ revenue, this is not a repeat of")
    print("    PANALPINA (smaller, simpler) — IT migration, customer")
    print("    contract renegotiation, and cultural integration at this")
    print("    scale introduce material execution risk that prior deals did")
    print("    not have in the same degree")
    print("  • Freight cycle is inherently volatile: air & sea rates")
    print("    collapsed 60-70% from 2022 peak to 2023-24 trough; any")
    print("    recurrence — driven by tariff escalation, demand slowdown,")
    print("    or capacity additions — compresses DSV earnings before the")
    print("    Schenker margin improvement can be realized")
    print("  • Conservative 2yr floor (DKK 1,299) is essentially flat:     ")
    print("    virtually no margin of safety on a forward earnings basis")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The track record is extraordinary: PANALPINA integration")
    print("    delivered above-target margins within 18 months; Agility GIL")
    print("    was similarly ahead of schedule; the market consistently")
    print("    underestimates DSV's ability to impose its operating model")
    print("    on acquired businesses — this is the most consistent")
    print("    acquisition execution record in the freight forwarding sector")
    print("  • The Schenker margin gap is large and demonstrable: 5-6% EBIT")
    print("    vs. 8-10%+ target on €20B+ revenue represents €400-800M in")
    print("    incremental EBIT at full convergence — this is not a hope,")
    print("    it is the documented gap between two companies' operating")
    print("    models applied to similar freight flows")
    print("  • Road freight network is a strategic capability unlock: prior")
    print("    to Schenker, DSV was primarily air & sea + solutions; the")
    print("    European road density adds a third leg to the stool and")
    print("    creates cross-sell synergies that pure margin math understates")
    print("  • Asset-light means ROCE recovers quickly: as Schenker margins")
    print("    improve, free cash flow generation accelerates and debt")
    print("    paydown de-risks the balance sheet on a 2-3yr horizon")
    print("  • Ratio B 0.89× — 30.8% downside / 34.6% upside — modestly")
    print("    asymmetric to the upside; the Schenker margin story is the")
    print("    call option, the road network density is the floor")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  DSV has done this three times — PANALPINA, Agility GIL, and")
    print("  now DB Schenker — and each time the market doubted the margin")
    print("  convergence thesis, and each time DSV delivered above targets.")
    print("  DB Schenker brings €20B in revenue running at 5-6% EBIT")
    print("  margins; DSV's operating model targets 8-10%+. The gap is")
    print("  €400-800M in incremental annual EBIT. At DKK 1,300 — 30.8%")
    print("  from bear, 34.6% from bull — with the track record intact and")
    print("  the margin gap visible, accumulate steadily. Add aggressively")
    print("  on freight-cycle-driven pullbacks toward DKK 1,050-1,100.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
