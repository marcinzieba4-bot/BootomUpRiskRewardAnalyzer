"""
Costco Wholesale Corporation (NYSE: COST) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.89×  |  EPP Gap: +135.7%
=======================================================================
THE MEMBERSHIP FLYWHEEL THAT PRINTS MONEY REGARDLESS OF MACRO: Costco is
not a retailer. It is a membership club that sells merchandise at near-cost
(1-2% product gross margin) so that the annual membership fee — $65/$130/yr
flowing through at nearly 100% — becomes the entire profit engine. 92-93%
North American renewal rates mean the membership base compounds like a
subscription. Every new warehouse, every fee increase, every new member
compounds the profit engine permanently. The most defensible business model
in global retail.
"""

# ── Model identity ────────────────────────────────────────────────────────────
TICKER         = "COST"
COMPANY        = "Costco Wholesale Corporation"
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Consumer Staples · Membership Warehouse Club / Value Retail / Private Label · NASDAQ: COST"
SECTOR_GROUP   = "Consumer Staples"

# ── Price & share data ────────────────────────────────────────────────────────
CURRENT_PRICE  = 990.00          # USD — mid-2026; perennially expensive, perennially justified
ANNUAL_DIV     = 4.64            # USD/yr regular dividend (~0.5% yield); periodic special dividends extra
SHARES_OUT_B   = 0.444           # billions

FW52_HIGH      = 1080.00
FW52_LOW       = 820.00

# ── Scenario prices ────────────────────────────────────────────────────────────
# BEAR  — recession + valuation compression: consumer spending contracts,
#         some membership cancellations (though historically resilient),
#         premium 50-55× multiple compresses toward 35-40× as growth slows;
#         international rollout pauses; no special dividend to support stock
# BASE  — steady compounder: 5-6% new warehouse openings, membership fee
#         increases every 5-7 years (next likely 2029-2030), executive
#         membership penetration growing (~46% → 50%+), international
#         (China, Europe) accelerating; ~$19.50 FY2026E EPS at ~50× → ~$990
# BULL  — membership flywheel accelerates: China warehouse opening cadence
#         doubles, US executive membership crosses 50%+, Costco Travel and
#         ancillary services grow, fee increase in 2028-29 adds $500M+
#         pure profit; multiple holds at 52× on compounding EPS growth
# XBULL — global dominance: 1,000+ warehouses by 2028, China/India/SE Asia
#         proving out; membership model extends to new verticals; market
#         prices permanent compound at 55-60× on quality premium
BEAR           = 680.0
BASE           = 990.0
BULL           = 1340.0
XBULL          = 1650.0

# ── Earnings Power Price (EPP) floor ──────────────────────────────────────────
# EPS_TROUGH: recession scenario — some membership attrition, lower traffic,
# still earns ~$14/sh as the membership base only partially unwinds
# PE_TROUGH: 30× reflects Costco's structural floor — even in severe recession
# the membership model deserves a premium because renewal rates hold at 85%+
EPS_TROUGH     = 14.00
PE_TROUGH      = 30.0
EPP            = EPS_TROUGH * PE_TROUGH     # $420.00

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E EPS ~$19.50 × 45× conservative-but-still-premium multiple + div
# Conservative case -10.9% — even at 45× this is below current; reflects
# genuine risk of paying 50× for a 10-12% EPS grower
PE_CONSERVATIVE  = 45.0
EPS_FY2026E      = 19.50
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $882.14

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
    ("membership_flywheel_92_93pct_renewal_and_fee_increase_compounding",     5.0, 0.25),
    ("value_proposition_recession_resilience_and_trade_down_beneficiary",     4.0, 0.20),
    ("international_expansion_china_europe_and_new_warehouse_growth_runway",  3.5, 0.18),
    ("premium_50_55x_forward_valuation_and_perfection_required_risk",         2.0, 0.17),
    ("kirkland_signature_private_label_and_treasure_hunt_traffic_flywheel",   4.0, 0.12),
    ("e_commerce_digital_and_costco_travel_ancillary_revenue_growth",         3.0, 0.08),
]

# ── Structural Competitive Advantage (SCA) factors ────────────────────────────
SCA_FACTORS = {
    "membership_model_92_93pct_renewal_fee_at_100pct_margin_is_the_business":    +0.28,
    "value_proposition_impossible_to_displace_and_recession_trade_down_anchor":  +0.18,
    "kirkland_signature_brand_and_treasure_hunt_experience_create_loyalty":      +0.12,
    "international_warehouse_flywheel_and_fee_base_compounding_across_markets":  +0.10,
    "premium_50_55x_forward_pe_leaves_no_room_for_execution_error":              -0.18,
    "grocery_delivery_ecommerce_competitive_pressure_amazon_walmart_target":     -0.08,
    "warehouse_expansion_pace_limited_by_site_selection_zoning_and_permitting":  -0.05,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.37

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"COST ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE MEMBERSHIP FLYWHEEL THAT PRINTS MONEY REGARDLESS OF MACRO: Costco is not a retailer "
    "— it is a membership club that sells merchandise at near-cost (1-2% product gross margin) "
    "so that the annual fee ($65/$130/yr, ~$4.6B revenue at near-100% flow-through) becomes "
    "the entire profit engine. 92-93% North American renewal rates mean the membership base "
    "compounds like the best subscription business in the world. "
    "THE ECONOMICS ARE UNIQUE: Costco's ~875 warehouses generate ~$250-270K in membership "
    "fee revenue each per year at essentially zero marginal cost; every new warehouse opened "
    "creates a self-funding annuity; every fee increase (raised to $65/$130 in Sept 2024, "
    "first increase since 2017) drops almost entirely to the bottom line — a $5 fee increase "
    "on 130M+ cardholders globally generates $650M+ in pure incremental profit. "
    "THE VALUE PROPOSITION IS RECESSION-PROOF: Costco members feel compelled to shop "
    "frequently to 'get their money's worth'; in recessions, consumers trade down TO Costco "
    "from traditional retailers and restaurants — membership renewal rates have never dropped "
    "below 85% even in the 2008-09 financial crisis; Kirkland Signature (the most beloved "
    "private label in retail) deepens the lock-in. "
    "INTERNATIONAL IS THE DECADE-LONG GROWTH RUNWAY: China (now 10+ warehouses, each "
    "generating extraordinary volumes on opening day); UK, Japan, Korea, Australia all "
    "mature and growing; Spain, France, Sweden expanding; India and SE Asia are the next "
    "frontier — each new market replicates the proven membership flywheel at scale. "
    "THE HONEST RISK: at 50-55× forward EPS, Costco is priced for perfection permanently; "
    "any EPS miss, membership growth slowdown, or multiple normalization compresses the "
    "stock 20-25% before fundamentals change; at $990 the conservative floor ($882) is "
    f"-10.9% — real downside for a quality compounder. "
    f"Conservative 2yr: EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.0f} → {CONS_RETURN:.1f}%. "
    "THE BEST BUSINESS MODEL IN RETAIL — ALWAYS EXPENSIVE, ALWAYS WORTH IT: "
    "accumulate on any pullback; the membership flywheel never stops compounding. "
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
    print("  • At 50-55× forward EPS, Costco is pricing in compound perfection")
    print("    indefinitely; a multiple normalization to 40× (still premium) on")
    print("    unchanged earnings produces a -20% drawdown with no fundamental")
    print("    deterioration — valuation risk is the primary bear case, not")
    print("    business deterioration")
    print("  • Conservative 2yr floor at 45× ($882) is -10.9% below current price;")
    print("    even paying a significant premium to market, you lose money in the")
    print("    conservative case — you need the bull multiple to persist AND compound")
    print("  • Grocery delivery and e-commerce competition is intensifying: Amazon")
    print("    Fresh, Walmart+, and Instacart are training a new generation of")
    print("    consumers to shop online rather than drive to a warehouse; Costco's")
    print("    e-commerce remains a small share of total and its fulfillment")
    print("    cost structure is not optimized for small-order delivery")
    print("  • Warehouse expansion is constrained by real estate: finding and")
    print("    permitting 160,000+ sq ft sites in desirable suburban locations")
    print("    takes years; growth is inherently limited to 20-30 new warehouses/yr")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The membership model is the most defensible in retail: 92-93% annual")
    print("    renewal rates in North America mean that once a household joins,")
    print("    they stay for life; Costco has studied member cancellation and finds")
    print("    that most who quit rejoin within 2-3 years; the compounding effect")
    print("    of a growing, nearly-permanent membership base is what justifies")
    print("    the premium multiple — this is not a P/E story, it is a DCF story")
    print("    on a near-perpetual cash flow stream")
    print("  • Every fee increase is pure profit: raising the annual fee by $5")
    print("    on 130M+ cardholders generates $650M+ in incremental pre-tax income")
    print("    with zero incremental cost; the Sept 2024 increase to $65/$130")
    print("    added ~$500M to the bottom line; the next increase (likely 2029-30)")
    print("    will add another $500-700M; this is the highest-quality revenue growth")
    print("    mechanism in consumer")
    print("  • Kirkland Signature is a $60B+ annual revenue brand at 30%+ gross")
    print("    margins — larger than most Fortune 500 consumer goods companies —")
    print("    and it is exclusive to Costco membership; it creates a reason to")
    print("    both join and to keep renewing that no competitor can replicate")
    print("  • Costco is recession-proof by design: consumers facing economic")
    print("    pressure trade DOWN to bulk buying at warehouse prices; the value")
    print("    proposition strengthens in recessions, not weakens; same-store")
    print("    sales grew through 2008-09 while most retailers declined")
    print("  • International expansion is a multi-decade runway: 875+ warehouses")
    print("    today vs. the potential for 2,000+ globally; China, India, SE Asia,")
    print("    and Eastern Europe are essentially untapped; each new market replicates")
    print("    the membership flywheel with proven economics")
    print("  • Ratio B 0.91× — downside 31.3% / upside 35.4% — asymmetry favors")
    print("    the bull; the membership moat creates the floor; fee increases and")
    print("    international expansion create the upside")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Costco has built the most elegant business model in retail: charge")
    print("  members an annual fee, then sell them everything at cost, so the fee")
    print("  IS the profit. The genius is that this creates an unbreakable loyalty")
    print("  loop — members feel obligated to shop frequently to justify the fee,")
    print("  which makes the shopping experience feel like winning, which makes")
    print("  them renew, which compounds the membership base year after year after")
    print("  year at a 92-93% renewal rate. At $990 you are paying 50× earnings")
    print("  for what is arguably the best-designed membership subscription business")
    print("  in the world. It is never cheap. It has always been worth it.")
    print("  Accumulate on any pullback — especially toward $820-880.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
