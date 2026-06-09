"""
Ecolab Inc. (NYSE: ECL) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.92×  |  EPP Gap: +148.0%
=======================================================================
THE WATER AND HYGIENE COMPANY THAT IS EMBEDDED IN YOUR CUSTOMERS: Ecolab's
moat is not a chemical formula or a patent — it is the Ecolab field
engineer who shows up at your Marriott, your Tyson Foods plant, or your
hospital every week to test water, adjust chemistry, and prevent the
problem that would cost you ten times the Ecolab contract. The "Circle
the Customer, Circle the Globe" model means Ecolab sells not products
but outcomes: the hotel that doesn't have a Legionella outbreak, the
food processor that doesn't have a line shutdown, the semiconductor fab
that doesn't lose a wafer batch to impure process water. This on-site
service creates switching costs that compound over decades — the customer
who has had an Ecolab engineer on-site for 15 years is not switching to
save 5% on chemistry.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "ECL"
COMPANY        = "Ecolab Inc."
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Materials · Specialty Chemicals / Water Treatment / Hygiene & Infection Prevention · NYSE: ECL"
SECTOR_GROUP   = "Materials"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 248.00          # USD — mid-2026; premium multiple on water scarcity + recurring model
ANNUAL_DIV     = 2.28            # USD/yr (~0.9% yield); 33rd consecutive annual increase
SHARES_OUT_B   = 0.285           # billions

FW52_HIGH      = 278.00
FW52_LOW       = 208.00

# ── Scenario prices ─────────────────────────────────────────────────────────
# BEAR  — industrial downturn + regulatory rollback: hospitality, food &
#         beverage, and light industrial volumes decline in global recession;
#         water regulation rollback reduces compliance-driven demand in some
#         US industrial segments; ChampionX oilfield exposure amplifies
#         earnings cyclicality; premium multiple compresses sharply on
#         growth deceleration toward 24-26× from 34-38×
# BASE  — steady compounder: institutional and industrial volumes grow
#         2-3%; water scarcity regulatory backdrop supports pricing;
#         healthcare/life sciences accelerates; EPS $7.25 at 34× + $2.28
#         div → essentially flat; premium multiple requires growth delivery
# BULL  — water scarcity premium + industrial upcycle: water scarcity
#         legislation drives mandatory industrial water efficiency programs;
#         data center cooling water treatment becomes material new segment;
#         healthcare/pharma life sciences accelerates; margin recovery from
#         input cost normalization; multiple re-rates toward 40× on secular
# XBULL — water becomes the defining ESG infrastructure investment: Ecolab
#         re-rated as water infrastructure alongside utilities; M&A in
#         water analytics; new semiconductor/data center water categories
BEAR           = 182.0
BASE           = 248.0
BULL           = 320.0
XBULL          = 388.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPP = pessimistic_PE × current EPS — what is this business worth at a
# de-rated multiple on what it actually earns today?
# PE_PESSIMISTIC: 14× — water treatment franchise under industrial recession;
# essential service for food safety / compliance retains a premium floor even
# at trough; applied to current adj EPS $7.25/sh (the actual business earnings)
EPS_FY2026E    = 7.25
PE_PESSIMISTIC = 14.0
EPP            = PE_PESSIMISTIC * EPS_FY2026E    # 14 × $7.25 = $101.50

# ── Conservative 2-year price estimate ───────────────────────────────────────
# FY2027E adj EPS ~$7.25 × 34× conservative multiple + $2.28 div
# Conservative case essentially flat (+0.3%) — water tech at fair value
PE_CONSERVATIVE  = 34.0
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $248.78

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
    ("on_site_service_model_engineers_embedded_at_customers_switching_costs_compound",    4.0, 0.22),
    ("nalco_water_industrial_water_treatment_essential_process_reliability_regulatory",    3.5, 0.20),
    ("institutional_hygiene_hospitality_food_service_healthcare_recurring_revenue",       3.5, 0.17),
    ("value_based_selling_customer_saves_10x_ecolab_cost_in_water_energy_outcomes",      3.5, 0.17),
    ("water_scarcity_secular_tailwind_industrial_water_efficiency_imperative",            3.0, 0.13),
    ("premium_34_38x_valuation_industrial_downturn_and_championx_cyclicality_risk",      2.5, 0.11),
]

# ── Structural Competitive Advantage (SCA) factors ───────────────────────────
SCA_FACTORS = {
    "on_site_service_engineer_embedded_at_customer_switching_cost_compounds_15yr_plus":   +0.18,
    "nalco_water_essential_industrial_process_water_treatment_regulatory_and_reliability": +0.14,
    "value_based_selling_roi_justified_10x_return_on_ecolab_contract_cost":              +0.12,
    "water_scarcity_global_secular_tailwind_industrial_water_efficiency_imperative":      +0.08,
    "premium_34_38x_pe_any_growth_deceleration_compresses_multiple_sharply":             -0.10,
    "industrial_downturn_f_and_b_hospitality_industrial_volumes_cycle_sensitive":         -0.08,
    "championx_acquisition_adds_oilfield_cyclicality_and_integration_complexity":         -0.06,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.28

# ── Weighted conviction score ─────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ────────────────────────────────────────────────────────────
SUMMARY = (
    f"ECL ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE WATER AND HYGIENE COMPANY EMBEDDED IN YOUR CUSTOMERS: Ecolab's moat is the "
    "field engineer who shows up at your Marriott, Tyson Foods plant, or hospital every "
    "week to test water, adjust chemistry, and prevent the problem that costs ten times "
    "the Ecolab contract. 'Circle the Customer, Circle the Globe' — selling outcomes, "
    "not products. The hotel that doesn't have a Legionella outbreak, the food processor "
    "that doesn't have a line shutdown, the semiconductor fab with no impure process "
    "water. On-site service creates switching costs that compound over decades. "
    "NALCO WATER IS THE INDUSTRIAL BACKBONE: industrial water treatment for Fortune 500 "
    "manufacturers — cooling towers, boilers, process water — is essential infrastructure; "
    "a water treatment failure can mean a plant shutdown costing millions per day; "
    "Nalco's engineers have been managing these systems at the same plants for decades "
    "and the institutional knowledge is not transferable without significant disruption. "
    "WATER SCARCITY IS THE SECULAR TAILWIND: industrial water efficiency is transitioning "
    "from a cost item to a regulatory and strategic imperative; data center cooling water "
    "treatment is an emerging high-growth segment; semiconductor fab water purity is "
    "non-negotiable; Ecolab is positioned at the intersection of every major industrial "
    "water challenge. "
    "THE HONEST RISK: at 34-38× forward earnings, any growth deceleration compresses "
    "the multiple sharply — the conservative 2yr case (+0.3%) requires perfect execution; "
    "industrial volume exposure (F&B, hospitality) creates genuine cyclicality; "
    "ChampionX oilfield segment adds commodity sensitivity; the ROI selling model "
    "faces pushback when customer CFOs cut discretionary budgets. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — "
    "essentially flat; BULL requires water scarcity premium and multiple re-rate. "
    f"Add on industrial-fear pullbacks toward $208-218 where Ratio B improves materially. "
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
    print(f"  PE Pessimistic:                                    {PE_PESSIMISTIC:>8.1f}×")
    print(f"  EPP (Pessimistic PE × current EPS):             ${EPP:>8.2f}")
    print(f"  EPP (Earnings Power Price):                        ${EPP:>8.2f}")
    print(f"  EPP Gap (current vs. EPP floor):              {EPP_GAP_PCT:>+8.1f}%")
    print()
    print(f"  Conservative Price ({EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}×):          ${CONSERVATIVE_PRICE:>8.2f}  ({CONS_RETURN:>+.1f}%)")
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
    print("  • 34-38× forward earnings leaves virtually no margin of safety:")
    print("    the conservative 2yr case is +0.3% — you need both earnings")
    print("    delivery and multiple stability simultaneously; any growth miss")
    print("    (a hospitality downturn, industrial capex cut) will compress")
    print("    both the EPS and the multiple at the same time, doubling the")
    print("    downside impact")
    print("  • Industrial cyclicality is underappreciated: Ecolab's largest")
    print("    customers are food & beverage processors and industrial")
    print("    manufacturers; in a recession, these customers cut operating")
    print("    budgets and defer non-essential service upgrades — Ecolab's")
    print("    'essential' positioning has limits when a CFO needs to hit")
    print("    a cost target and the Ecolab contract is the line item")
    print("  • ChampionX adds oilfield exposure that was not part of the")
    print("    classic Ecolab thesis: oilfield water treatment is genuinely")
    print("    cyclical (tied to oil prices and drilling activity) and adds")
    print("    earnings volatility that a 34× premium multiple should not carry")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The switching cost model is one of the strongest in B2B:")
    print("    an Ecolab field engineer who has been servicing a plant for")
    print("    15 years holds institutional knowledge about that facility's")
    print("    water chemistry, equipment quirks, and compliance history that")
    print("    cannot be transferred to a competitor without 2-3 years of")
    print("    on-site learning; the customer who switches saves 5% on chemistry")
    print("    and risks a food safety incident or a regulatory finding —")
    print("    the risk/reward of switching is genuinely unfavorable")
    print("  • Water scarcity is a structural secular force: the World Resources")
    print("    Institute identifies water stress as a critical risk for $500B+")
    print("    in corporate revenue annually; industrial water efficiency is")
    print("    transitioning from optional to mandatory in many jurisdictions;")
    print("    Ecolab's water analytics business (Ecolab Water for Climate)")
    print("    is being written into corporate ESG mandates globally")
    print("  • Data center and semiconductor water treatment is an emerging")
    print("    high-growth segment: hyperscale data centers require millions")
    print("    of gallons of cooling water treated to precise purity specs;")
    print("    semiconductor fabs require ultrapure water at extraordinary")
    print("    specification; both are growing rapidly and neither can afford")
    print("    a water treatment failure — these are Ecolab's ideal customers")
    print("  • The ROI selling model is genuinely differentiated: Ecolab")
    print("    demonstrates to each customer the exact dollar value of water")
    print("    saved, energy reduced, and compliance incidents avoided;")
    print("    this value-based contract structure makes the Ecolab expense")
    print("    the last thing a rational CFO cuts because it demonstrably")
    print("    saves more than it costs")
    print("  • Ratio B 0.92× — 26.6% downside / 29.0% upside — modestly")
    print("    favorable; the essential water treatment floor is the put,")
    print("    the water scarcity premium is the call")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Ecolab embeds its engineers in your facility, learns your water")
    print("  chemistry, and prevents the food safety incident or regulatory")
    print("  finding that would cost you ten times its contract. That embedded")
    print("  service model creates switching costs that compound over decades.")
    print("  Water scarcity is making industrial water efficiency a strategic")
    print("  imperative — and data centers, semiconductor fabs, and pharma")
    print("  manufacturers are Ecolab's fastest-growing customers. At $248 —")
    print("  26.6% from bear, 29.0% from bull — accumulate the water moat.")
    print("  Add on industrial-fear pullbacks toward $208-218.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
