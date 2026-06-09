"""
Uber Technologies, Inc. (NYSE: UBER) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.90×  |  EPP Gap: +171.6%
=======================================================================
THE DEMAND AGGREGATOR OF GLOBAL URBAN MOBILITY: Uber owns the demand side
of ridesharing and food delivery in 70+ countries — 170M+ monthly active
platform consumers, 7.6B+ annual trips, a two-sided marketplace flywheel
with deepening network effects. The central question is NOT whether Uber
grows; it is whether autonomous vehicles disrupt the supply side faster
than Uber can become the distribution layer FOR them.
"""

# ── Model identity ───────────────────────────────────────────────────────────
TICKER         = "UBER"
COMPANY        = "Uber Technologies, Inc."
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Technology · Ridesharing / Food Delivery / Freight · Two-Sided Marketplace Platform · NYSE: UBER"
SECTOR_GROUP   = "Technology"

# ── Price & share data ───────────────────────────────────────────────────────
CURRENT_PRICE  = 88.00           # USD — mid-2026, ~40% up from 52-wk low, approaching ATH range
ANNUAL_DIV     = 0.00            # no dividend; capital returned via buybacks ($7B authorization)
SHARES_OUT_B   = 2.080           # billions (diluted, post-SBC)

FW52_HIGH      = 100.00
FW52_LOW       = 62.00

# ── Scenario prices ──────────────────────────────────────────────────────────
# BEAR  — autonomous vehicle disruption accelerates: Waymo/Tesla capture 15-25%
#         rideshare share in key US metros by 2028, take rates compress, driver
#         supply-side advantage erodes, regulatory pressure on gig classification
#         → multiple compression on slowing growth + margin deterioration
# BASE  — steady-state platform compounding: AV threat real but slow, Uber
#         becomes AV distribution partner (Waymo deal scales), ad revenue
#         grows to $2B+, Delivery expands grocery/retail verticals, FCF
#         accelerates; market prices 25× on $3.80 2026E EPS → $88 fair value
# BULL  — AV fleet operator narrative takes hold: Uber as the OS for autonomous
#         urban transport, ad business $3B+ at 70%+ margins, membership
#         (Uber One) at 50M+ subscribers; market re-rates to 35× growing EPS
# XBULL — global category dominance: AV economics halve supply costs (no driver
#         share), gross margin expands 800bps, FCF doubles, FCF yield compresses
BEAR           = 52.0
BASE           = 88.0
BULL           = 128.0
XBULL          = 165.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: GAAP trough in adverse macro + moderate AV disruption scenario —
# Uber still earns $1.80/sh as platform take rate compresses but volume holds
# PE_TROUGH: 18× reflects platform resilience floor even in disruption scenario
EPS_TROUGH     = 1.80
PE_TROUGH      = 18.0
EPP            = EPS_TROUGH * PE_TROUGH     # $32.40

# ── Conservative 2-year price estimate ───────────────────────────────────────
# 2026E GAAP EPS ~$3.80 × 24× conservative platform multiple + $0 div
# Conservative case is roughly at current price — stock is fairly valued,
# not deeply cheap; upside requires narrative expansion (AV, ads, Uber One)
PE_CONSERVATIVE  = 24.0
EPS_FY2026E      = 3.80
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $91.20

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
    ("global_two_sided_marketplace_flywheel_and_network_effects",          4.0, 0.22),
    ("autonomous_vehicle_disruption_risk_waymo_tesla_robotaxi_timeline",   1.5, 0.20),
    ("advertising_platform_and_uber_one_membership_monetization",          3.5, 0.17),
    ("food_delivery_grocery_and_adjacency_expansion_runway",               3.0, 0.16),
    ("international_expansion_and_emerging_market_growth",                 3.0, 0.14),
    ("driver_courier_classification_and_regulatory_cost_risk",             2.0, 0.11),
]

# ── Structural Competitive Advantage (SCA) factors ────────────────────────────
SCA_FACTORS = {
    "170m_plus_monthly_active_consumers_and_global_demand_aggregation":      +0.22,
    "advertising_and_membership_high_margin_layer_on_existing_supply":       +0.14,
    "cross_platform_flywheel_mobility_delivery_freight_one_super_app":       +0.11,
    "av_distribution_partnership_strategy_waymo_may_mobility_avride":        +0.09,
    "autonomous_vehicle_supply_side_disruption_risk_waymo_tesla":            -0.18,
    "driver_and_courier_classification_regulatory_exposure_globally":        -0.10,
    "take_rate_pressure_and_competitive_intensity_doordash_lyft_local":      -0.08,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.20

# ── Weighted conviction score ─────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ────────────────────────────────────────────────────────────
SUMMARY = (
    f"UBER ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE DEMAND AGGREGATOR OF GLOBAL URBAN MOBILITY: 170M+ monthly active platform consumers, "
    "7.6B+ annual trips, $44B+ gross bookings in 70+ countries — the most scaled two-sided "
    "marketplace in transportation history, now layering a high-margin advertising business "
    "($1.5B+ revenue, 70%+ incremental margin) and Uber One membership (~30M subscribers) "
    "onto the same infrastructure. "
    "THE AV QUESTION CUTS BOTH WAYS: Waymo/Tesla robotaxis threaten the driver supply side "
    "but Uber owns the demand aggregation layer that no AV company has independently replicated "
    "at scale; Uber is actively positioning as the distribution OS for AV fleets — Waymo "
    "partnership live in Austin/Atlanta/Phoenix, Avride, May Mobility, Cruise integrations; "
    "if AV supply costs halve (no driver share ~72% of fare), Uber's take rate economics "
    "expand dramatically rather than compress. "
    "FINANCIAL INFLECTION IS REAL: first GAAP annual profit in 2023; 2025 adj. EBITDA "
    "~$7.5B, FCF ~$6.0B+, $7B buyback authorization active; gross bookings growing "
    "15-20% organic; GAAP EPS ~$3.80 in 2026E. "
    "THE HONEST RISK: bear case is genuine — if Waymo/Tesla scale US robotaxi deployment "
    "faster than Uber deploys the AV partnership model, the supply-side advantage erodes "
    "before the distribution narrative takes hold; take rates face structural pressure from "
    "Lyft/DoorDash competition; driver/courier classification battles ongoing in EU, UK, CA. "
    f"Conservative 2yr: EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + $0 div = "
    f"${CONSERVATIVE_PRICE:.0f} → +{CONS_RETURN:.1f}% — essentially fair value; "
    "BULL/XBULL require AV partnership narrative or advertising re-rate. "
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
    print(f"  {'Factor':<62} {'Conv':>4}  {'Wt':>5}")
    print(f"  {'-'*72}")
    for name, conv, wt in SIGNALS:
        print(f"  {name:<62} {conv:>4.1f}  {wt:>5.0%}")
    print()

    print("  STRUCTURAL COMPETITIVE ADVANTAGE FACTORS")
    for k, v in SCA_FACTORS.items():
        print(f"  {k:<65} {v:>+.2f}")
    print(f"  {'SCA NET':<65} {SCA_NET:>+.2f}")
    print()

    print(f"{'='*72}")
    print()
    print("  WHY THIS IS AN ◎ ACCUMULATE, NOT A ◌ WATCHLIST OR ◉ BUY")
    print()
    print("  NOT ◉ BUY because:")
    print("  • The autonomous vehicle bear case is real and binary: if Waymo and Tesla")
    print("    independently scale urban robotaxi fleets without needing Uber's network,")
    print("    the driver supply-side advantage evaporates and take rates compress")
    print("    structurally — a scenario the market cannot fully price until it happens")
    print("  • At ~23× 2026E EPS, the stock is NOT cheap on near-term earnings; it is")
    print("    a 'show me' story at a fair-but-not-discounted multiple requiring the")
    print("    AV partnership / advertising / membership thesis to actually print")
    print("  • Conservative 2yr floor ($91) is essentially at current price — limited")
    print("    margin of safety; a multiple compression to 20× on AV fear alone")
    print("    (~$76) is plausible without a fundamental deterioration")
    print("  • $7B+ in annual stock-based compensation dilutes FCF-to-equity returns;")
    print("    'cash generation' is substantially offset by SBC before buybacks")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • 170M+ monthly active platform consumers represent the most valuable")
    print("    demand aggregation asset in transportation — no AV company has built")
    print("    anything approaching this distribution scale independently")
    print("  • The AV disruption thesis cuts BOTH ways: if Waymo removes driver costs")
    print("    (~72% of fare today), Uber's economics improve dramatically as fleet")
    print("    operator/distributor — this is why Waymo chose Uber as the partner")
    print("    for its consumer robotaxi expansion (not a competitor, a channel)")
    print("  • Advertising is an emerging, structurally high-margin business: Journey")
    print("    Ads, in-app sponsored listings, and out-of-home (tablet ads in vehicles)")
    print("    at $1.5B+ revenue growing ~80% YoY against near-zero marginal cost —")
    print("    a Google-search-like monetization layer on captive in-trip attention")
    print("  • Uber One (~30M subscribers, $9.99/month) drives 30-40% higher spend")
    print("    per member, reduces churn, and creates a Prime-like loyalty moat")
    print("    compounding with every new vertical (groceries, alcohol, pharmacy)")
    print("  • Ratio B 0.90× — downside 40.9% / upside 45.5% — the asymmetry is")
    print("    genuinely favorable; this is not a coin-flip")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Uber has solved the hardest problem in platform businesses — it owns both")
    print("  sides of a global, real-time, two-sided marketplace at scale in 70+")
    print("  countries. The AV era does not destroy this advantage; it restructures who")
    print("  owns the supply (human drivers → autonomous vehicles), while the demand")
    print("  aggregation layer — where consumers open the Uber app — remains Uber's.")
    print("  The company that cracked consumer behavior in rideshare is now layering")
    print("  advertising and membership on top, growing FCF, and buying back stock.")
    print("  At $88, the AV fear creates the entry; the demand flywheel creates the")
    print("  return. Initiate at ◎ ACCUMULATE; add on AV-driven pullbacks toward")
    print("  $68-75 where Ratio B would approach ◉ BUY territory.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
