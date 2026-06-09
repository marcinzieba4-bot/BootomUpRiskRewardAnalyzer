"""
Ferguson Enterprises Inc. (NYSE: FERG) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.95×  |  EPP Gap: +60.2%
=======================================================================
THE INVISIBLE INFRASTRUCTURE GIANT: Ferguson is America's largest
plumbing, HVAC, and waterworks distributor — a $30B+ revenue business
that most investors have never heard of because it sits between the
manufacturer and the contractor, moving $1 of manufacturer product for
every $1.25 Ferguson charges. The moat is scale: Ferguson's purchasing
power with suppliers (Carrier, Trane, Bradford White, Kohler), its branch
density (1,700+ locations across the US), and its private-label Wolseley
brand create a cost and service advantage that regional distributors cannot
match. Critically, ~50% of Ferguson revenue comes from repair and remodel
(R&R) — the leaky pipe does not wait for the housing market to recover.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "FERG"
COMPANY        = "Ferguson Enterprises Inc."
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Industrials · Wholesale Distribution / Plumbing & HVAC / Waterworks / Fire Protection · NYSE: FERG"
SECTOR_GROUP   = "Industrials"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 205.00          # USD — mid-2026; post-NYSE primary listing; housing cycle discount
ANNUAL_DIV     = 3.60            # USD/yr (~1.8% yield); regular + special dividend; consistent grower
SHARES_OUT_B   = 0.205           # billions

FW52_HIGH      = 235.00
FW52_LOW       = 168.00

# ── Scenario prices ─────────────────────────────────────────────────────────
# BEAR  — housing starts collapse + industrial capex cut: US housing starts
#         fall below 900K on sustained high interest rates; commercial
#         construction (office, retail) continues declining; data center
#         buildout pauses on AI capex rationalization; Ferguson's ~25% new
#         construction revenue compresses; pricing deflation in PVF products
#         as supply chains normalize; multiple re-rates toward 13-14× trough
# BASE  — steady compounder: R&R demand resilient; non-res construction
#         (data centers, healthcare, industrial) sustains Ferguson's growth;
#         housing market gradually improves as rates normalize; EPS $11.50
#         at 18× + $3.60 div → modest positive return
# BULL  — construction cycle recovery + non-res acceleration: housing starts
#         recover to 1.4M+; data center and healthcare non-res construction
#         at elevated run-rate; Wolseley private label gains share; margin
#         expansion from digital ordering and pricing analytics; 20-22× re-rate
# XBULL — platform re-rating: Ferguson's digital B2B ordering platform
#         recognized as a distribution technology asset; acquisitions deepen
#         HVAC/fire protection; EPS $16+ by FY2028 at 22× multiple
BEAR           = 148.0
BASE           = 205.0
BULL           = 265.0
XBULL          = 325.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: severe housing + construction downturn; R&R provides floor
# — Ferguson still earns ~$8.00/sh even at genuine trough on R&R demand
# PE_TROUGH: 16× reflects distribution at cycle trough with R&R backstop
EPS_TROUGH     = 8.00
PE_TROUGH      = 16.0
EPP            = EPS_TROUGH * PE_TROUGH     # $128.00

# ── Conservative 2-year price estimate ───────────────────────────────────────
# FY2027E adj EPS ~$11.50 × 18× conservative multiple + $3.60 div
# Conservative case +2.7% — distribution at modest discount to fair value
PE_CONSERVATIVE  = 18.0
EPS_FY2026E      = 11.50
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $210.60

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
    ("number_one_us_plumbing_hvac_distributor_30b_revenue_scale_purchasing_power",        4.0, 0.22),
    ("repair_and_remodel_50pct_revenue_non_discretionary_leaky_pipes_dont_wait",          3.5, 0.20),
    ("non_residential_data_center_healthcare_industrial_secular_construction_tailwind",    3.5, 0.18),
    ("private_label_wolseley_and_digital_ordering_platform_margin_expansion",             3.0, 0.15),
    ("waterworks_fire_protection_essential_infrastructure_replacement_demand",             3.0, 0.13),
    ("housing_starts_sensitivity_interest_rate_new_construction_cycle_risk",              2.5, 0.12),
]

# ── Structural Competitive Advantage (SCA) factors ───────────────────────────
SCA_FACTORS = {
    "number_one_us_plumbing_hvac_distributor_scale_purchasing_terms_and_1700_branches":   +0.18,
    "repair_remodel_demand_non_discretionary_floor_leaks_hvac_failures_cannot_wait":      +0.12,
    "private_label_wolseley_higher_margin_and_digital_b2b_ordering_platform_stickiness":  +0.10,
    "non_residential_data_center_healthcare_industrial_secular_construction_tailwind":     +0.08,
    "housing_starts_new_construction_sensitivity_interest_rate_cycle_meaningful_exposure": -0.10,
    "distribution_fragmented_regional_competitors_and_amazon_business_potential_threat":  -0.06,
    "pvf_product_price_deflation_risk_as_supply_chains_normalize_post_cycle":             -0.04,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.28

# ── Weighted conviction score ─────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ────────────────────────────────────────────────────────────
SUMMARY = (
    f"FERG ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE INVISIBLE INFRASTRUCTURE GIANT: Ferguson is America's largest plumbing, HVAC, "
    "and waterworks distributor — a $30B+ revenue business that sits between manufacturer "
    "and contractor, moving 1,700+ locations across the US. THE SCALE MOAT: purchasing "
    "power with Carrier, Trane, Bradford White, Kohler creates supplier terms no regional "
    "distributor can match; Wolseley private label generates higher margins; digital B2B "
    "ordering platform creates contractor stickiness through order history and integration. "
    "THE R&R FLOOR IS STRUCTURAL: ~50% of Ferguson revenue is repair and remodel — "
    "leaking pipes, failing HVAC, broken fixtures do not wait for housing market recovery "
    "or interest rate cycles; this creates a demand floor that makes Ferguson's earnings "
    "more resilient than its construction exposure suggests. "
    "NON-RESIDENTIAL IS THE GROWTH ENGINE: data center construction (requiring massive "
    "HVAC and fire suppression), healthcare facility buildout, and industrial "
    "manufacturing reshoring are secular tailwinds that do not depend on housing. "
    "THE HONEST RISK: ~25% of revenue is new construction — genuinely sensitive to "
    "housing starts and commercial construction cycles; at 1.15M housing starts in "
    "2025-26, the new construction segment is below potential and any rate-driven "
    "improvement would be a meaningful tailwind; conversely, sustained high rates "
    "would extend the drag; regional distributors are fragmented but Amazon Business "
    "is a long-term threat in lower-complexity SKUs. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — "
    "modest positive; BULL requires new construction recovery + non-res acceleration. "
    f"Add on housing-fear pullbacks toward $168-178 where Ratio B enters ◉ BUY territory. "
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
    print("  • New construction sensitivity is real and present: at ~1.15M")
    print("    US housing starts (well below the ~1.5M normalized pace),")
    print("    Ferguson's new construction segment is running below potential;")
    print("    sustained high interest rates maintaining this level would")
    print("    extend the earnings drag before the R&R floor fully offsets")
    print("  • Multiple at ~18× forward earnings is fair, not cheap: the")
    print("    conservative 2yr return is only +2.7% — not enough to excite")
    print("    without the housing cycle improvement materializing; investors")
    print("    need the new construction recovery OR non-res acceleration")
    print("    to generate compelling returns from this starting point")
    print("  • Amazon Business is a credible long-term distribution threat:")
    print("    for low-complexity, commodity plumbing SKUs, Amazon's B2B")
    print("    platform offers price transparency and speed that erodes")
    print("    Ferguson's value proposition at the low end of the product mix")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The R&R demand floor is structural and underappreciated:")
    print("    America's housing stock is the oldest it has ever been —")
    print("    the median US home was built in 1980; pipes, HVAC systems,")
    print("    and water heaters in these homes are failing at an accelerating")
    print("    rate; this is not discretionary spending, it is essential")
    print("    maintenance; Ferguson's ~50% R&R exposure means the business")
    print("    earns through every housing construction cycle ever observed")
    print("  • Scale purchasing creates a genuine cost moat: Ferguson buys")
    print("    more Carrier HVAC equipment, more Bradford White water heaters,")
    print("    and more Kohler fixtures than any other single buyer in the")
    print("    US; the supplier terms this generates — pricing, inventory")
    print("    priority, promotional support — are not replicable by the")
    print("    next 10 distributors combined")
    print("  • Non-residential secular tailwinds are multi-year: data center")
    print("    construction requires extraordinary HVAC (cooling) and fire")
    print("    suppression infrastructure; healthcare facility buildout")
    print("    continues regardless of housing; industrial reshoring (chips,")
    print("    EVs, pharma) requires significant plumbing and process piping;")
    print("    these are 5-10yr buildout cycles, not quarters")
    print("  • Wolseley private label is a margin expansion engine: as")
    print("    contractors adopt Wolseley-branded products for commodity")
    print("    applications, Ferguson captures the manufacturer's margin")
    print("    and builds brand preference that reinforces contractor loyalty")
    print("  • Ratio B 0.95× — 27.8% downside / 29.3% upside — modestly")
    print("    favorable; the R&R floor is the put, the construction cycle")
    print("    recovery is the call")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Ferguson distributes plumbing, HVAC, and waterworks products")
    print("  to contractors from 1,700+ US branches — the largest such")
    print("  network in the country. The R&R demand floor (leaking pipes,")
    print("  failing HVAC) provides earnings resilience through any construction")
    print("  cycle. Scale purchasing from manufacturers creates a cost advantage")
    print("  regional competitors cannot match. Non-residential construction")
    print("  (data centers, healthcare) provides secular growth independent")
    print("  of housing. At $205 — 27.8% from bear, 29.3% from bull — the")
    print("  invisible infrastructure giant is modestly attractively priced.")
    print("  Add on housing-fear pullbacks toward $168-178.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
