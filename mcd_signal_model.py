"""
McDonald's Corporation (NYSE: MCD) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.94×  |  EPP Gap: +98.1%
=======================================================================
THE FRANCHISE MACHINE AND REAL ESTATE EMPIRE: McDonald's is simultaneously
the world's largest restaurant franchisor and one of the largest commercial
real estate operators on earth. 95%+ of its 40,000+ locations are franchised
— McDonald's collects royalties (~5% of sales) and, critically, owns or
controls the land under a significant portion of those locations, creating
an embedded real estate asset that compounds independently of restaurant
economics. The 2024 E. coli outbreak (onion contamination, ~75 cases) was
a headline event, not a structural break — the brand has survived far worse
and consumer memory in QSR is short. At $305, the digital loyalty platform
(100M+ active users), the value-platform tailwind from consumer stress, and
the asset-light royalty model compound at a premium multiple that is earned.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "MCD"
COMPANY        = "McDonald's Corporation"
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Consumer Discretionary · Quick Service Restaurant / Franchise / Real Estate · NYSE: MCD"
SECTOR_GROUP   = "Consumer Discretionary"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 305.00          # USD — mid-2026; post-E. coli recovery, digital loyalty ramp
ANNUAL_DIV     = 7.08            # USD/yr (~2.3% yield); 48th consecutive annual increase
SHARES_OUT_B   = 0.72            # billions (reduced by decades of buybacks)

FW52_HIGH      = 330.00
FW52_LOW       = 255.00

# ── Scenario prices ─────────────────────────────────────────────────────────
# BEAR  — consumer boycott + GLP-1 structural traffic decline: E. coli brand
#         damage proves stickier than historical QSR incidents; GLP-1 adoption
#         measurably reduces QSR visit frequency among heavy users; deep
#         recession causes consumers to cook at home rather than trade down
#         to QSR; franchisee stress from negative real wage growth compresses
#         system sales; multiple re-rates toward 17-18× on traffic decline
# BASE  — steady compounder: US comps recover post-E. coli; digital loyalty
#         drives visit frequency; value platform (McValue menu) captures
#         consumer stress tailwind; international markets (Europe, LatAm)
#         grow steadily; EPS $13 at 23× + $7.08 div → essentially flat
# BULL  — digital flywheel accelerates: 100M+ loyalty users drive +2-3%
#         comps premium; international expansion continues; drive-thru + kiosk
#         automation improves throughput and margins; multiple re-rates to 26×
#         as market prices the tech-enabled restaurant platform premium
# XBULL — platform re-rating: McDonald's is repriced as a tech-enabled
#         franchise platform + real estate investment; AI-driven personalization
#         + autonomous drive-thru creates structural margin uplift; $15+ EPS
BEAR           = 225.0
BASE           = 305.0
BULL           = 390.0
XBULL          = 465.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: severe recession; franchisee royalties compress but don't
# disappear — ~$7.00/sh even in a deep downturn given real estate backstop
# PE_TROUGH: 22× reflects franchise + real estate hybrid even at trough
EPS_TROUGH     = 7.00
PE_TROUGH      = 22.0
EPP            = EPS_TROUGH * PE_TROUGH     # $154.00

# ── Conservative 2-year price estimate ───────────────────────────────────────
# FY2027E adj EPS ~$13.00 × 23× conservative multiple + $7.08 div
# Conservative case essentially flat (+0.4%) — franchise at fair value
PE_CONSERVATIVE  = 23.0
EPS_FY2026E      = 13.00
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $306.08

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
    ("franchise_model_95pct_franchised_royalty_stream_asset_light_capital_efficiency",    4.0, 0.22),
    ("real_estate_land_ownership_under_franchisee_locations_embedded_property_value",     3.5, 0.18),
    ("digital_loyalty_100m_plus_active_users_personalization_and_repeat_visit_frequency", 3.5, 0.18),
    ("value_platform_qsr_downturn_resilience_mcvalue_menu_consumer_stress_tailwind",      3.5, 0.15),
    ("40000_plus_restaurants_100_plus_countries_international_growth_runway",             3.0, 0.15),
    ("ecoli_2024_brand_overhang_glp1_qsr_traffic_and_high_leverage_balance_sheet",        2.5, 0.12),
]

# ── Structural Competitive Advantage (SCA) factors ───────────────────────────
SCA_FACTORS = {
    "franchise_model_95pct_franchised_royalty_on_sales_asset_light_capital_efficiency":   +0.18,
    "real_estate_land_control_under_franchisee_locations_independent_compounding_asset":  +0.14,
    "mcdonalds_brand_most_recognized_qsr_globally_drive_thru_and_value_perception":       +0.12,
    "digital_loyalty_100m_active_users_personalization_visit_frequency_data_moat":        +0.08,
    "ecoli_2024_brand_damage_and_slow_us_comp_recovery_taking_longer_than_prior_events":  -0.06,
    "glp1_and_health_consciousness_qsr_traffic_frequency_structural_headwind":            -0.06,
    "negative_book_equity_from_buybacks_and_high_leverage_constrains_financial_flex":     -0.06,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.34

# ── Weighted conviction score ─────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ────────────────────────────────────────────────────────────
SUMMARY = (
    f"MCD ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE FRANCHISE MACHINE AND REAL ESTATE EMPIRE: McDonald's is simultaneously the "
    "world's largest restaurant franchisor and one of the largest commercial real estate "
    "operators — 95%+ of 40,000+ locations are franchised, royalties collected at ~5% "
    "of system sales, and McDonald's owns or controls the land under a significant "
    "portion of those locations. "
    "THE REAL ESTATE IS THE HIDDEN ASSET: McDonald's typically owns the land or long-"
    "term lease and subleases to franchisees at a markup — creating a rent-collecting "
    "real estate business layered under the royalty stream; the combined model generates "
    "~45%+ operating margins on $25B+ system royalties and rent. "
    "DIGITAL LOYALTY IS THE GROWTH LEVER: 100M+ active loyalty users drive measurably "
    "higher visit frequency and average check; personalized offers reduce price "
    "sensitivity; the data asset compounds with every order — this is not a loyalty "
    "program, it is a behavioral dataset monetized through precision marketing. "
    "QSR IS THE RECESSION WINNER: in consumer stress, casual dining loses to QSR; "
    "McDonald's value platform (McValue menu) captures trade-down from sit-down "
    "restaurants and even from grocery; the 2008 and 2020 recessions both proved "
    "McDonald's is a beneficiary of consumer stress, not a victim. "
    "THE HONEST RISK: the 2024 E. coli outbreak (onion contamination) has proven "
    "stickier than historical QSR incidents — US comps recovery has been slower; "
    "GLP-1 adoption reducing visit frequency among heavy users is a real but "
    "modest structural headwind; leverage is high and book equity is negative from "
    "decades of buybacks, constraining financial flexibility. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — "
    "essentially flat; BULL requires digital flywheel acceleration. "
    f"Add on E. coli-overhang pullbacks toward $255-270 where Ratio B enters ◉ BUY. "
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
    print("  • At 23-24× forward earnings, the franchise premium is priced in:")
    print("    the conservative 2yr case is +0.4% — you need digital flywheel")
    print("    acceleration or international inflection to generate real returns")
    print("    from this starting point; the dividend yield (2.3%) is lower")
    print("    than PEP or PM and provides less total return support")
    print("  • The 2024 E. coli recovery has been slower than prior incidents:")
    print("    past QSR contamination events (Jack in the Box 1993, Chipotle")
    print("    2015-2016) showed recovery timelines of 12-18 months; MCD's US")
    print("    comp trajectory suggests the brand damage is real and the")
    print("    consumer is not fully back — this is an ongoing headwind, not")
    print("    a resolved one")
    print("  • Negative book equity and high leverage constrain flexibility:")
    print("    decades of buybacks have created a technically insolvent balance")
    print("    sheet (negative book equity); while this is a deliberate capital")
    print("    allocation choice for a franchise model, it limits capacity to")
    print("    respond to unexpected shocks without accessing debt markets")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The franchise + real estate model is structurally superior to")
    print("    any other restaurant model: McDonald's collects ~5% of system")
    print("    sales as royalty regardless of food costs, labor costs, or")
    print("    energy prices — the franchisee absorbs all operating risk while")
    print("    McDonald's retains the brand equity and the real estate; at")
    print("    40,000+ locations, the scale of this royalty stream is without")
    print("    peer in the restaurant industry")
    print("  • The land ownership is genuinely underappreciated: McDonald's")
    print("    typically owns the freehold or long-lease on prime commercial")
    print("    real estate at locations selected 30-50 years ago at cost basis")
    print("    a fraction of current market value; this embedded real estate")
    print("    asset is not marked to market and represents substantial hidden")
    print("    value that anchors the downside in ways EPS analysis misses")
    print("  • Digital loyalty is working: 100M+ active users generating 30%+")
    print("    of US system sales through digital channels; personalized offers")
    print("    demonstrably drive incremental visits; the behavioral data")
    print("    compounds with every order — MCD now has a moat that competitors")
    print("    cannot replicate quickly because it requires scale to be useful")
    print("  • QSR benefits from consumer stress: in every recession since the")
    print("    1970s, McDonald's has outperformed the restaurant industry as")
    print("    consumers trade down; the McValue menu launch is the playbook")
    print("    that worked in 2008-2009 and will work again")
    print("  • Ratio B 0.94× — 26.2% downside / 27.9% upside — modestly")
    print("    favorable; the franchise royalty floor is the put,")
    print("    the digital loyalty flywheel is the call")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  McDonald's franchises restaurants and owns the land they sit on —")
    print("  a royalty + real estate model that generates ~45%+ operating margins")
    print("  on $25B+ in system revenue regardless of who makes the burgers.")
    print("  100M+ digital loyalty users compound visit frequency. The 2024")
    print("  E. coli overhang is real but temporary; GLP-1 is a modest headwind,")
    print("  not a structural break. At $305 — 26.2% from bear, 27.9% from bull")
    print("  — accumulate the franchise machine. Add aggressively on E. coli-")
    print("  overhang pullbacks toward $255-270.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
