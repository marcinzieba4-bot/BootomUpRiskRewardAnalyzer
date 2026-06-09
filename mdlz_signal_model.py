"""
Mondelez International Inc. (NASDAQ: MDLZ) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.91×  |  EPP Gap: +76.1%
=======================================================================
THE GLOBAL SNACKING EMPIRE WITH A COCOA PROBLEM: Mondelez is the world's
largest snacking company — Oreo, Cadbury, Toblerone, Milka, Chips Ahoy!,
Ritz, belVita, Triscuit — and the dominant player in the two most
profitable snack categories on earth: chocolate and biscuits. The brand
portfolio is extraordinary: Oreo is the world's best-selling cookie for
a reason that has nothing to do with taste and everything to do with the
ritual — twist, lick, dunk — that parents teach children in 100 countries.
Cadbury is the emotional memory of British childhood; Toblerone is the
airport purchase that signals "I was thinking of you." These are not
brands — they are cultural artifacts with pricing power that has survived
every cost spike, every diet trend, and every private label challenge for
decades. The honest problem in 2026 is cocoa: prices hit generational
highs in 2024-2025 due to West African crop failures, and Mondelez's
hedging programs can delay but not eliminate the pass-through to consumers
or the compression of margins while new price points are established.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "MDLZ"
COMPANY        = "Mondelez International Inc."
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Consumer Staples · Snacking / Chocolate & Confectionery / Biscuits & Crackers · NASDAQ: MDLZ"
SECTOR_GROUP   = "Consumer Staples"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 62.00           # USD — mid-2026
ANNUAL_DIV     = 1.70            # USD/yr (~2.7% yield); consistent grower
SHARES_OUT_B   = 1.33            # billions

FW52_HIGH      = 74.00
FW52_LOW       = 52.00

# ── Scenario prices ───────────────────────────────────────────────────────────
# BEAR  — cocoa cost crisis sustained: West African production failures
#         persist 2-3 more years; Mondelez must choose between passing
#         through 25-35% chocolate price increases (volume destruction) or
#         absorbing margin compression (earnings destruction); GLP-1 adoption
#         accelerates in North America/Europe reducing indulgent snack volume;
#         EM FX deterioration on USD strength compounds revenue headwinds
# BASE  — cocoa normalizes: West African crops recover 2026-2027, hedges roll
#         at lower cost, pricing sticks from 2024-2025 increases; organic
#         growth resumes 3-4%/yr; adj EPS $3.30 × 19× + div → ~$64
# BULL  — premiumization + EM volume: cocoa cost normalization drops to
#         margin expansion; emerging market middle class chocolate consumption
#         growth re-accelerates; GLP-1 impacts less severe than feared in
#         portion-controlled premium formats; adj EPS $4.00+ × 21×
# XBULL — pricing power confirmation + EM acceleration: MDLZ demonstrates
#         that premium chocolate consumers are price-inelastic even at new
#         levels; India/Southeast Asia volume inflects; adj EPS $5+ by 2029
BEAR           = 42.0
BASE           = 62.0
BULL           = 84.0
XBULL          = 104.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: sustained cocoa spike + volume declines; still earns ~$2.20
# on the brand portfolio — Oreo/Ritz/belVita biscuit margins are insulated
# from cocoa and provide an earnings floor even in a chocolate margin crisis
# PE_TROUGH: 16× reflects premium snack franchise even at trough — these
# brands don't become value businesses, the multiple floor is higher than
# a commodity food company
EPS_TROUGH     = 2.20
PE_TROUGH      = 16.0
EPP            = EPS_TROUGH * PE_TROUGH    # $35.20

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E adj EPS ~$3.30 × 19× conservative multiple + $1.70 div
PE_CONSERVATIVE  = 19.0
EPS_FY2026E      = 3.30
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV  # $64.40

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
SIGNALS = [
    ("oreo_cadbury_toblerone_category_defining_cultural_brand_portfolio_moat",       4.0, 0.22),
    ("emerging_markets_150_country_distribution_and_local_plus_global_brand_mix",    3.5, 0.20),
    ("snacking_occasion_growth_premiumization_and_chocolate_category_resilience",    3.0, 0.18),
    ("cocoa_price_volatility_west_africa_crop_failure_and_margin_compression_risk",  2.0, 0.20),
    ("glp1_demand_risk_for_indulgent_categories_and_portion_size_reduction_trend",   2.5, 0.20),
]

# ── Structural Competitive Advantage (SCA) factors ─────────────────────────────
SCA_FACTORS = {
    "oreo_world_best_selling_cookie_ritual_moat_twist_lick_dunk_100_country_reach":    +0.18,
    "cadbury_toblerone_milka_emotional_memory_brands_price_inelastic_premium_buyers":  +0.14,
    "150_country_distribution_emerging_market_middle_class_chocolate_volume_growth":   +0.10,
    "cocoa_price_generational_highs_2024_2025_hedging_lag_and_volume_destruction":     -0.14,
    "glp1_adoption_accelerating_in_indulgent_snack_categories_demand_headwind":        -0.10,
    "em_fx_structural_headwind_75pct_non_north_america_revenue_usd_translation_drag":  -0.08,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.10

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"MDLZ ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.2f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE GLOBAL SNACKING EMPIRE WITH A COCOA PROBLEM: Mondelez is the world's largest snacking "
    "company — Oreo, Cadbury, Toblerone, Milka, Chips Ahoy!, Ritz, belVita — dominant in "
    "chocolate and biscuits across 150 countries. THE BRAND MOAT IS CULTURAL, NOT FUNCTIONAL: "
    "Oreo is the world's best-selling cookie because of the twist-lick-dunk ritual that parents "
    "teach children in 100 countries — not the taste; Cadbury is the emotional memory of British "
    "childhood; Toblerone is the airport purchase that signals 'I was thinking of you.' These are "
    "cultural artifacts with pricing power that has survived every diet trend and private label "
    "challenge for decades. THE EMERGING MARKET GROWTH STORY IS STRUCTURAL: 75%+ of revenue "
    "outside North America means every new member of the global middle class in India, Southeast "
    "Asia, or Africa who buys their first Cadbury bar is a new customer for a generation — "
    "chocolate consumption per capita in EM is 10-20× below Western Europe, and the gap closes "
    "with income growth. THE COCOA PROBLEM IS REAL AND NEAR-TERM: West African crop failures "
    "drove cocoa to generational price highs in 2024-2025; Mondelez's hedging programs delay "
    "but cannot eliminate the choice between passing costs to consumers (volume risk) or "
    "absorbing margin compression (earnings risk); this is the reason MDLZ has underperformed "
    "staples peers and why the entry price today is more attractive than 2 years ago. "
    "THE GLP-1 RISK IS REAL BUT OVERSTATED: GLP-1 drugs reduce appetite for indulgent snacks, "
    "but premium chocolate and ritualistic biscuit consumption is less price- and appetite-elastic "
    "than calorie-dense snacking; the Oreo consumer is not stopping for GLP-1 reasons. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — "
    "modest upside; BULL requires cocoa normalization confirming margin recovery. "
    "Add on cocoa-fear or GLP-1-fear selloffs toward $54-57. "
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
    print(f"  Conservative Price ({EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}×):           ${CONSERVATIVE_PRICE:>8.2f}  ({CONS_RETURN:>+.1f}%)")
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
    print("  • The cocoa cost crisis is not resolved: West African production")
    print("    failures drove cocoa to $10,000+/tonne in 2024-2025 — a 3×")
    print("    increase from historical norms; Mondelez's multi-year hedging")
    print("    program can defer cost recognition but eventually rolls to spot;")
    print("    the 2026-2027 hedge book reflects meaningfully higher costs than")
    print("    2023 — this is an ongoing earnings headwind, not a cleared event")
    print("  • GLP-1 is a genuine long-term demand headwind: as GLP-1 adoption")
    print("    expands beyond obesity to weight management broadly, impulsive")
    print("    snacking behavior is measurably reduced; Mondelez's categories")
    print("    (chocolate, biscuits) are more discretionary than Colgate")
    print("    toothpaste or Coca-Cola hydration — the demand risk is real")
    print("  • Conservative 2yr (+3.9%) is thin — largely a 'collect the")
    print("    dividend and wait for cocoa to normalize' story at current price")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The brand moat is cultural, not functional — and therefore")
    print("    durable: Oreo's twist-lick-dunk ritual is taught by parents to")
    print("    children in 100 countries; Cadbury is childhood memory in the")
    print("    UK, India, Australia; Toblerone is the universal gift purchase;")
    print("    these associations took generations to build and cannot be")
    print("    displaced by a cheaper alternative or a GLP-1 drug")
    print("  • The EM growth runway is a multi-decade structural tailwind:")
    print("    chocolate consumption per capita in India is ~200g/yr vs 8kg+")
    print("    in Switzerland — every $1,000 increase in Indian per capita")
    print("    income historically correlates with a step-up in chocolate")
    print("    consumption; Mondelez is already the distribution infrastructure")
    print("    in place to capture that growth")
    print("  • The cocoa problem is cyclical, not structural: West African crop")
    print("    failures are weather-driven events, not permanent capacity loss;")
    print("    supply response (new plantings, yield improvement) and demand")
    print("    destruction at $10,000/tonne cocoa will bring prices back toward")
    print("    long-run equilibrium; Mondelez's pricing sticks when costs fall")
    print("  • At $62 — ~20% below the 2023 highs — the cocoa headwind is")
    print("    partially priced; you are buying the brand portfolio at a")
    print("    discount to normalized earnings")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Mondelez owns the snacking brands that are cultural rituals in")
    print("  100 countries — and they are currently on sale because cocoa")
    print("  prices hit a generational high and GLP-1 fears are real but")
    print("  overstated for premium ritualistic categories. At $62 — 32.3%")
    print("  from bear, 35.5% from bull — you are buying Oreo, Cadbury, and")
    print("  Toblerone at a discount to what they are worth when West African")
    print("  crops normalize. The conservative case is thin (+3.9%); the")
    print("  bull case requires cocoa normalization unlocking margin recovery.")
    print("  Accumulate on cocoa-fear and GLP-1-fear pullbacks toward $54-57.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
