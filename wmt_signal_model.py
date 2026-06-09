"""
Walmart Inc. (NYSE: WMT) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.91×  |  EPP Gap: +150.0%
=======================================================================
THE WORLD'S LARGEST RETAILER BECOMING A PLATFORM: Walmart's $648B revenue
base — the largest of any company on earth — is being systematically
monetized beyond retail margins through three high-value overlays:
Walmart Connect (advertising, $4B+ growing 25%+/yr at near-100% margin),
Walmart+ membership (~50M households, Prime alternative with in-store
and delivery), and GoLocal fulfillment services (monetizing the supply
chain for third parties). The grocery leadership that Amazon cannot crack
(~25% US grocery share, 4,600+ stores within 10 miles of 90% of Americans)
is the foundation; the platform businesses are the re-rating catalyst.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "WMT"
COMPANY        = "Walmart Inc."
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Consumer Staples · Omnichannel Retail / Grocery / Membership Platform · NYSE: WMT"
SECTOR_GROUP   = "Consumer Staples"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 100.00          # USD — post 3-for-1 split (Feb 2024); reflects platform re-rating
ANNUAL_DIV     = 0.88            # USD/yr (~0.9% yield); 52nd consecutive annual dividend increase (Dividend King)
SHARES_OUT_B   = 8.02            # billions (post-split)

FW52_HIGH      = 110.00
FW52_LOW       = 75.00

# ── Scenario prices ─────────────────────────────────────────────────────────
# BEAR  — consumer spending collapse + tariff/supply chain shock: US recession
#         cuts discretionary spending sharply; tariff escalation compresses
#         gross margins on Chinese-sourced general merchandise; Amazon/Instacart
#         accelerate grocery share capture; advertising slowdown hits high-margin
#         overlay businesses; multiple compresses toward 25-28× on earnings
#         pressure; Flipkart valuation writedown adds headline noise
# BASE  — steady-state compounder: low-to-mid single-digit SSS growth driven
#         by grocery and e-commerce; advertising and Walmart+ revenue growing
#         25%+ but still small relative to total; EPS $2.78 at ~35× = $98 + div
# BULL  — platform monetization accelerates: advertising reaches $6-8B at
#         35%+ margins; Walmart+ hits 60M+ members with attach rate improvement;
#         Sam's Club comps accelerate vs. Costco; international (Walmex/Flipkart)
#         re-rated as standalone growth assets; multiple expands to 40-42×
# XBULL — platform inflection: advertising business valued separately like a
#         media company ($50B+); Walmart+ becomes the default American household
#         membership; Flipkart IPO crystallizes India value; EPS $3.50+ by 2028
BEAR           = 68.0
BASE           = 100.0
BULL           = 135.0
XBULL          = 165.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: recession + margin compression; still earns ~$1.60/sh on
# essential grocery and staples — the most recession-resistant retail
# PE_TROUGH: 25× reflects premium still warranted for #1 grocer / essential retailer
EPS_TROUGH     = 1.60
PE_TROUGH      = 25.0
EPP            = EPS_TROUGH * PE_TROUGH     # $40.00

# ── Conservative 2-year price estimate ───────────────────────────────────────
# FY2027E adj EPS ~$2.78 × 35× conservative multiple + $0.88 div
# Conservative case essentially flat (-1.8%) — platform at fair value
PE_CONSERVATIVE  = 35.0
EPS_FY2026E      = 2.78
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $98.18

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
    ("walmart_connect_advertising_platform_high_margin_25pct_growth_re_rating_catalyst",   3.5, 0.22),
    ("grocery_leadership_25pct_us_share_4600_stores_10mi_from_90pct_of_americans",         3.5, 0.20),
    ("walmart_plus_membership_50m_households_prime_alternative_attach_rate_expansion",     3.5, 0.17),
    ("sams_club_acceleration_membership_flywheel_and_comp_vs_costco_convergence",          3.0, 0.15),
    ("flipkart_india_and_walmex_underpenetrated_market_international_growth_optionality",  3.0, 0.13),
    ("35_40x_forward_pe_premium_valuation_no_margin_of_safety_in_conservative_case",       2.0, 0.13),
]

# ── Structural Competitive Advantage (SCA) factors ───────────────────────────
SCA_FACTORS = {
    "4600_us_stores_within_10_miles_of_90pct_americans_last_mile_grocery_moat":          +0.18,
    "walmart_connect_4b_plus_advertising_at_near_100pct_margin_growing_25pct_per_yr":    +0.13,
    "walmart_plus_prime_alternative_with_grocery_delivery_and_fuel_discount_ecosystem":  +0.10,
    "supply_chain_network_and_golocal_fulfillment_monetization_for_third_parties":       +0.08,
    "35_40x_forward_multiple_leaves_no_margin_of_safety_requires_bull_case_to_profit":   -0.12,
    "amazon_ecommerce_dominance_and_ongoing_discretionary_category_share_pressure":      -0.08,
    "thin_retail_operating_margins_2_3pct_make_any_cost_or_volume_shock_amplified":      -0.06,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.23

# ── Weighted conviction score ─────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ────────────────────────────────────────────────────────────
SUMMARY = (
    f"WMT ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE WORLD'S LARGEST RETAILER BECOMING A PLATFORM: Walmart's $648B revenue base is "
    "being systematically monetized beyond retail margins through three high-value overlays: "
    "Walmart Connect (advertising, $4B+ growing 25%+/yr at near-100% margin), Walmart+ "
    "membership (~50M households, Prime alternative with in-store and delivery), and GoLocal "
    "fulfillment services monetizing the supply chain for third parties. "
    "THE GROCERY MOAT IS IRREPLACEABLE: ~25% US grocery share, 4,600+ stores within 10 "
    "miles of 90% of Americans — Amazon has spent $20B+ on grocery (Whole Foods, Fresh, "
    "Go) and moved the needle modestly; the physical convenience advantage in perishables "
    "is structural, not temporary. "
    "SAM'S CLUB IS THE UNDERAPPRECIATED ASSET: accelerating membership growth, comp sales "
    "consistently matching or exceeding Costco, digital penetration (~30% of orders) "
    "outpacing the warehouse club format average — represents a Costco-quality flywheel "
    "at a Walmart valuation. "
    "THE HONEST RISK: WMT trades at 35-40× forward earnings — an extraordinary premium "
    "for a retailer that earns 2-3% operating margins; any deceleration in advertising "
    "growth, membership attach rates, or comp traffic would compress the multiple violently; "
    "tariff escalation on Chinese-sourced general merchandise could compress gross margins "
    "in ways the grocery segment cannot offset; the conservative 2yr case is essentially "
    "flat (-1.8%) — you need the platform monetization bull case to make money at $100. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — "
    "essentially flat; BULL/XBULL require advertising re-rating and membership acceleration. "
    "Accumulate steadily; add aggressively on tariff-driven pullbacks toward $82-88 where "
    f"Ratio B approaches ◉ BUY territory. "
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
    print("  • Premium valuation leaves no margin of safety: at 35-40×")
    print("    forward earnings, WMT is priced as a technology platform,")
    print("    not as a grocer; the conservative 2yr floor ($98) is -1.8%")
    print("    — virtually no downside protection on an earnings basis")
    print("  • The advertising business, while genuinely high-margin and")
    print("    growing, is $4B on $648B in revenue — it would need to")
    print("    triple to materially move consolidated operating margins")
    print("    above 5%; the re-rating requires a multi-year execution")
    print("    arc that has not yet been fully demonstrated")
    print("  • Tariff risk is asymmetric: general merchandise (toys,")
    print("    electronics, apparel) is ~30% of revenue but highly")
    print("    China-exposed; tariff escalation compresses these margins")
    print("    in ways the grocery segment cannot offset, and the low")
    print("    operating margin base (2-3%) means small cost shocks")
    print("    produce large EPS impacts")
    print("  • Amazon has not stopped trying: Fresh, Whole Foods, same-day")
    print("    delivery improvements, and Amazon's structural advantage in")
    print("    non-perishables creates ongoing pressure on the high-margin")
    print("    general merchandise categories")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The grocery moat is genuinely irreplaceable: Amazon has")
    print("    spent $20B+ on grocery and owns ~3% of US grocery share")
    print("    vs. Walmart's ~25% — the proximity advantage (4,600 stores")
    print("    within 10 miles of 90% of Americans) in fresh and perishables")
    print("    is structural, not temporal; this is the foundation that")
    print("    advertising, membership, and fulfillment are built on")
    print("  • Walmart Connect is a genuine asymmetric option: $4B in")
    print("    advertising at near-100% margin growing 25%+/yr represents")
    print("    a business that, if separated, would trade at 20-30× revenue")
    print("    ($80-120B standalone value); the market is still pricing it")
    print("    at the retail multiple — as it matures and becomes material,")
    print("    the blended multiple should expand")
    print("  • Sam's Club is the most underappreciated asset: consistently")
    print("    matching Costco on membership growth and comps with ~30%")
    print("    digital penetration; at $120B+ in revenue it would be a")
    print("    top-10 US retailer standalone — valued at zero premium today")
    print("  • Ratio B 0.91× — 32.0% downside / 35.0% upside — essentially")
    print("    balanced; the option value is in platform monetization")
    print("    acceleration, the floor is the grocery moat")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Walmart built the most resilient retail infrastructure in")
    print("  history — 4,600 US stores, $648B in revenue, 90% of Americans")
    print("  within 10 miles — and is now layering a $4B+ advertising")
    print("  platform, a 50M-member subscription business, and a third-party")
    print("  fulfillment network on top of it. The grocery moat that Amazon")
    print("  has spent a decade trying to crack is structurally intact.")
    print("  At $100 — 32.0% from bear, 35.0% from bull — the platform")
    print("  transition is priced in at the margin but not yet reflected")
    print("  in the multiple expansion that advertising maturity will")
    print("  deliver. Accumulate steadily; add on tariff-driven pullbacks.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
