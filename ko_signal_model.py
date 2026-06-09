"""
The Coca-Cola Company (NYSE: KO) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 1.00×  |  EPP Gap: +75.0%
=======================================================================
THE GLOBAL DISTRIBUTION SYSTEM THAT TOOK 100 YEARS TO BUILD: Coca-Cola
is not a beverage company — it is a global distribution and brand-
licensing machine that happens to deliver beverages. The franchise bottler
system (FEMSA, CCEP, CCBA, and 200+ country partners) represents $100B+
in third-party capital deployed to build an asset that no competitor can
replicate in a generation. Coke Zero Sugar, Fairlife, Body Armor, Smartwater,
and Costa Coffee demonstrate that the distribution system is the moat, not
the sugar formula. The GLP-1 risk is real but overestimated — 40%+ of
Coca-Cola's volume is already zero/low calorie, and the category has been
adapting to health trends for 20 years.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "KO"
COMPANY        = "The Coca-Cola Company"
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Consumer Staples · Beverages / Non-Alcoholic / Global Distribution · NYSE: KO"
SECTOR_GROUP   = "Consumer Staples"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 70.00           # USD — mid-2026; steady compounder at fair value
ANNUAL_DIV     = 1.94            # USD/yr (~2.8% yield); 62nd consecutive annual increase (Dividend King)
SHARES_OUT_B   = 4.30            # billions

FW52_HIGH      = 76.00
FW52_LOW       = 58.00

# ── Scenario prices ─────────────────────────────────────────────────────────
# BEAR  — structural volume decline: GLP-1 adoption accelerates and sugar
#         consumption decline becomes measurable in sparkling volumes; sugar
#         tax regulation spreads to US federal level + more EU/EM markets;
#         emerging market currency crises compress USD revenue; private label
#         RTD water/zero-calorie beverages gain meaningful share; multiple
#         compresses toward 17-18× as growth narrative breaks
# BASE  — steady compounder: 3-4% organic revenue growth (price + emerging
#         market volume); Coke Zero/Fairlife/Body Armor offset sparkling
#         pressure; EPS $3.18 at 21× essentially flat; dividend grows 4-5%/yr
# BULL  — health pivot works + EM volume inflection: zero-sugar variants
#         capture health-conscious consumers; Africa and South/Southeast Asia
#         inflect on per-capita consumption growth; Body Armor/Fairlife become
#         $5B+ brands each; multiple re-rates to 24-25× as narrative shifts
# XBULL — category reinvention: KO is repriced as a diversified beverage
#         platform with multiple fast-growing premium brands beyond sparkling;
#         GLP-1 narrative fades; EPS $4+ by 2028 at 26-27× multiple
BEAR           = 52.0
BASE           = 70.0
BULL           = 88.0
XBULL          = 108.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: recession + volume decline + input cost spike; core distribution
# system still generates ~$2.00/sh through any scenario
# PE_TROUGH: 20× even at trough — Dividend King with irreplaceable distribution
EPS_TROUGH     = 2.00
PE_TROUGH      = 20.0
EPP            = EPS_TROUGH * PE_TROUGH     # $40.00

# ── Conservative 2-year price estimate ───────────────────────────────────────
# FY2027E adj EPS ~$3.18 × 21× conservative multiple + $1.94 div
# Conservative case -1.8% — essentially flat at fair value
PE_CONSERVATIVE  = 21.0
EPS_FY2026E      = 3.18
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $68.72

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
    ("global_200_country_franchise_bottler_distribution_system_irreplaceable_moat",       4.0, 0.22),
    ("coke_brand_and_portfolio_sprite_fanta_fairlife_body_armor_zero_sugar_pivot",        3.5, 0.20),
    ("pricing_power_5_7pct_annual_increases_with_volume_recovery_post_covid",             3.5, 0.18),
    ("dividend_king_62_consecutive_increases_2_8pct_yield_income_anchor",                 3.5, 0.15),
    ("africa_india_se_asia_per_capita_consumption_growth_underpenetrated_runway",         3.0, 0.15),
    ("glp1_sugar_tax_regulation_spreading_and_shifting_beverage_preferences_risk",        2.0, 0.10),
]

# ── Structural Competitive Advantage (SCA) factors ───────────────────────────
SCA_FACTORS = {
    "200_country_franchise_bottler_system_100yr_asset_impossible_to_replicate":           +0.20,
    "coca_cola_brand_strongest_consumer_brand_on_earth_irreplaceable_cultural_icon":      +0.16,
    "pricing_power_demonstrated_5_7pct_annual_increases_with_volume_resilience":          +0.10,
    "coke_zero_40pct_volume_fairlife_body_armor_health_pivot_already_in_progress":        +0.08,
    "glp1_drugs_structural_headwind_to_sugary_beverage_category_long_term_unknown":       -0.10,
    "sugar_tax_regulation_spreading_uk_mexico_europe_us_cities_regulatory_creep":         -0.06,
    "70pct_revenue_outside_us_currency_headwinds_and_emerging_market_volatility":         -0.06,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.32

# ── Weighted conviction score ─────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ────────────────────────────────────────────────────────────
SUMMARY = (
    f"KO ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE GLOBAL DISTRIBUTION SYSTEM THAT TOOK 100 YEARS TO BUILD: Coca-Cola is not a "
    "beverage company — it is a global distribution and brand-licensing machine. The "
    "franchise bottler system (FEMSA, CCEP, CCBA, and 200+ country partners) represents "
    "$100B+ in third-party capital deployed into an asset no competitor can replicate. "
    "THE MOAT IS THE DISTRIBUTION, NOT THE FORMULA: Coke Zero Sugar, Fairlife ($1B+ "
    "brand), Body Armor, Smartwater, and Costa Coffee all travel the same system — the "
    "formula is replaceable, the last-mile distribution into 200 countries is not; "
    "40%+ of Coca-Cola's volume is already zero/low calorie, the pivot has been "
    "running for 20 years. "
    "PRICING POWER AND DIVIDEND KING PEDIGREE: 5-7% annual price increases with "
    "volume resilience; 62 consecutive dividend increases — the income investor "
    "base is structurally captive; ~2.8% yield floors total return. "
    "THE HONEST RISK: GLP-1 drug adoption is a genuine long-term structural headwind "
    "to sugar consumption that is not fully priced by any model; sugar tax regulation "
    "has spread to UK, Mexico, and dozens of US cities and the trajectory is toward "
    "more; ~70% of revenue outside the US creates structural currency headwind that "
    "inflates reported revenue in EM upturns and depresses it in downturns; "
    "the conservative 2yr case ($69) is -1.8% — you are essentially buying the "
    "dividend and hoping for multiple stability. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — "
    "essentially flat; BULL requires zero-sugar pivot traction and EM inflection. "
    "Accumulate steadily; add meaningfully on GLP-1-fear-driven pullbacks toward "
    f"$58-62 where Ratio B enters ◉ BUY territory. "
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
    print("  • At 21-23× forward earnings, there is virtually no margin of")
    print("    safety — the conservative 2yr case is -1.8%, meaning you need")
    print("    the bull scenario (EM inflection + zero-sugar rerating) to")
    print("    generate meaningful returns; the dividend alone is 2.8%,")
    print("    which is not compelling on a risk-adjusted basis at this price")
    print("  • GLP-1 is a genuine structural uncertainty, not a transient")
    print("    headwind: drugs that reduce sugar cravings and food intake")
    print("    could structurally reduce per-capita sparkling beverage")
    print("    consumption over a 10-20yr horizon in a way that no amount")
    print("    of portfolio pivoting fully offsets; the market has not priced")
    print("    this scenario and neither has any consensus estimate")
    print("  • Sugar tax regulation is on a secular expansion path: the UK")
    print("    sugar levy, Mexico 10% tax, and 30+ US city/state measures")
    print("    are moving in one direction; the regulatory environment for")
    print("    sugary beverages in 2026 is meaningfully worse than in 2015")
    print("    and the trend has not reversed in any major jurisdiction")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The distribution system is the most powerful consumer moat")
    print("    on earth: 200 countries, 30M+ retail touchpoints, franchise")
    print("    bottlers who have invested $100B+ in infrastructure that")
    print("    takes Coke's product to every village in Africa, every")
    print("    convenience store in Asia, every restaurant in Latin America")
    print("    — this system is categorically irreplaceable on any timeline")
    print("    a private investor needs to worry about")
    print("  • The health pivot is 20 years old and working: Coke Zero was")
    print("    launched in 2005, Coke Zero Sugar reformulated in 2017;")
    print("    40%+ of Coca-Cola volume is now zero/low calorie; Fairlife")
    print("    (protein milk) is a $1B+ brand growing 20%+/yr; Body Armor")
    print("    (sports hydration) is competing with Gatorade — these are not")
    print("    defensive moves, they are offensive category expansions using")
    print("    the same distribution moat")
    print("  • Per-capita consumption in Africa and South/Southeast Asia")
    print("    remains a fraction of developed market levels: Sub-Saharan")
    print("    Africa at ~40 servings/yr vs. Mexico at ~600 — this is not")
    print("    a market share story, it is a category introduction story")
    print("    playing out over 30+ years with compounding volume tailwinds")
    print("  • 62 consecutive dividend increases: even in COVID (2020),")
    print("    even in the 2008 recession, KO raised its dividend — the")
    print("    $1.94/yr yield at 2.8% anchors institutional ownership and")
    print("    provides a total return floor that limits downside in practice")
    print("  • Ratio B 1.00× — perfectly symmetric 25.7%/25.7% — the moat")
    print("    quality justifies holding at this level; add on weakness")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Coca-Cola built the world's most extensive consumer distribution")
    print("  system over 100 years — 200 countries, 30M+ retail touchpoints,")
    print("  franchise bottlers who own the last mile. That system now carries")
    print("  Fairlife, Body Armor, Smartwater, and Coke Zero alongside the")
    print("  original formula. At $70 — perfectly symmetric 25.7% down and")
    print("  up — the brand and distribution are not in question. The honest")
    print("  uncertainty is GLP-1 and sugar regulation over a 10-20yr horizon.")
    print("  Accumulate steadily at $70; add meaningfully on any GLP-1-fear")
    print("  selloff toward $58-62 where the risk/reward becomes compelling.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
