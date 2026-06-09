"""
Colgate-Palmolive Company (NYSE: CL) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.92×  |  EPP Gap: +109.1%
=======================================================================
THE ORAL CARE MONOPOLY AND THE PET NUTRITION GEM: Colgate holds ~40% of
global toothpaste market share — the highest single-brand share in any
major consumer staples category worldwide. That number has held for three
decades through private label, regional brands, electric toothbrush
disruption, and every health trend imaginable. Hill's Pet Nutrition —
the vet-endorsed prescription and therapeutic pet food brand — is the
underappreciated second act: $4B+ in revenue growing double-digits,
built on a moat that Purina and Mars find genuinely difficult to replicate
because Hill's is prescribed, not purchased impulsively. Together, oral
care and Hill's generate ~60%+ of CL's operating profit at margins that
most consumer companies would consider aspirational.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "CL"
COMPANY        = "Colgate-Palmolive Company"
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Consumer Staples · Oral Care / Personal Care / Home Care / Pet Nutrition · NYSE: CL"
SECTOR_GROUP   = "Consumer Staples"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 92.00           # USD — mid-2026; EM FX drag and Hill's competition discount
ANNUAL_DIV     = 1.96            # USD/yr (~2.1% yield); 62nd consecutive annual increase (Dividend King)
SHARES_OUT_B   = 0.83            # billions

FW52_HIGH      = 102.00
FW52_LOW       = 78.00

# ── Scenario prices ─────────────────────────────────────────────────────────
# BEAR  — EM currency crisis + Hill's competitive break: multiple EM currency
#         crises (Brazil, Argentina, Turkey, Nigeria) simultaneously compress
#         USD revenue; Hill's loses vet-channel exclusivity as Purina/Mars
#         expand prescription ranges; private label oral care gains meaningful
#         share in Europe; multiple compresses toward 18-19× on organic growth
#         deceleration driven by volume pressure, not pricing
# BASE  — steady compounder: oral care pricing normalizes at 2-3% with volume
#         recovery; Hill's sustains double-digit growth; EM volume recovers
#         as local currencies stabilize; EPS $3.72 at 24× + $1.96 div → flat
# BULL  — Hill's re-rating + EM volume inflection: Hill's recognized as a
#         standalone premium pet nutrition asset at 30%+ EBIT margins;
#         EM volume growth accelerates in India, Africa, Southeast Asia;
#         oral care multiple expands on innovation (whitening, sensitivity);
#         CL re-rates toward 28-30× on blended high-quality growth
# XBULL — Hill's spin or partial IPO: Hill's valued separately at 25-30×
#         EBITDA crystallizes $20B+ of hidden value; oral care franchise
#         at full premium; EPS $5+ by 2028
BEAR           = 68.0
BASE           = 92.0
BULL           = 118.0
XBULL          = 142.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: severe EM FX + volume declines; core oral care + Hill's still
# earns ~$2.20/sh at genuine trough
# PE_TROUGH: 20× even at trough for Dividend King with essential oral care
EPS_TROUGH     = 2.20
PE_TROUGH      = 20.0
EPP            = EPS_TROUGH * PE_TROUGH     # $44.00

# ── Conservative 2-year price estimate ───────────────────────────────────────
# FY2027E adj EPS ~$3.72 × 24× conservative multiple + $1.96 div
# Conservative case essentially flat (-0.8%) — oral care at fair value
PE_CONSERVATIVE  = 24.0
EPS_FY2026E      = 3.72
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $91.24

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
    ("colgate_brand_40pct_global_toothpaste_share_three_decade_oral_care_dominance",      4.0, 0.22),
    ("hills_pet_nutrition_vet_endorsed_prescription_therapeutic_4b_plus_revenue",         4.0, 0.20),
    ("emerging_markets_50pct_revenue_brazil_india_mexico_africa_long_duration_growth",    3.5, 0.18),
    ("pricing_power_oral_care_and_pet_food_category_inelasticity_2022_2024_demonstrated", 3.5, 0.15),
    ("dividend_king_62_consecutive_increases_and_capital_return_consistency",             3.0, 0.13),
    ("em_fx_headwinds_hills_competition_and_24_26x_valuation_with_limited_upside",        2.5, 0.12),
]

# ── Structural Competitive Advantage (SCA) factors ───────────────────────────
SCA_FACTORS = {
    "colgate_40pct_global_toothpaste_share_highest_single_brand_share_in_major_category": +0.18,
    "hills_vet_endorsed_prescription_diet_moat_vet_recommendation_is_specification_lock": +0.14,
    "emerging_markets_50pct_revenue_with_local_manufacturing_and_distribution_density":  +0.10,
    "oral_care_category_inelasticity_essential_hygiene_habitual_repeat_purchase":         +0.08,
    "em_fx_headwinds_50pct_em_revenue_usd_reporting_structural_currency_drag":            -0.10,
    "hills_competition_intensifying_mars_purina_blue_buffalo_prescription_range_expansion":-0.06,
    "24_26x_valuation_multiple_limits_upside_on_3_4pct_organic_revenue_growth":          -0.06,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.28

# ── Weighted conviction score ─────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ────────────────────────────────────────────────────────────
SUMMARY = (
    f"CL ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE ORAL CARE MONOPOLY AND THE PET NUTRITION GEM: Colgate holds ~40% of global "
    "toothpaste market share — the highest single-brand share in any major consumer "
    "staples category worldwide, held for three decades through every competitive "
    "challenge. Hill's Pet Nutrition — vet-endorsed prescription and therapeutic pet "
    "food — is the underappreciated second act: $4B+ revenue growing double-digits, "
    "built on a moat Purina and Mars find genuinely difficult to replicate because "
    "Hill's is prescribed, not purchased impulsively. "
    "ORAL CARE IS THE FLOOR: toothpaste is the most habitual consumer purchase in "
    "personal care — bought every 4-6 weeks regardless of economic conditions, "
    "price-insensitive at the category level, and specification-locked by taste "
    "memory in ways that make switching genuinely uncomfortable; the Colgate consumer "
    "who has brushed with the same product for 20 years is not switching for private "
    "label even at 30% savings. "
    "HILL'S IS THE GROWTH ASSET: veterinarians recommend Hill's Science Diet and "
    "Hill's Prescription Diet because they have prescribed it for 80 years — the vet "
    "channel creates a recommendation moat that Mars/Purina cannot easily replicate; "
    "pet humanization and premiumization trends are secular tailwinds; therapeutic "
    "diets (kidney, diabetes, weight management) face virtually no private label "
    "competition because the SKU complexity and vet relationships are prohibitive. "
    "THE HONEST RISK: ~50% of revenue from emerging markets creates structural USD "
    "headwind every time EM currencies weaken — Brazil, Argentina, Turkey, Nigeria "
    "all matter; Hill's competition from Mars Veterinary Health and Purina Pro Plan "
    "Veterinary Diets is intensifying in the vet channel; the 24-26× multiple at "
    "3-4% organic growth leaves thin margin of safety. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — "
    "essentially flat; BULL requires Hill's re-rating and EM volume inflection. "
    f"Add on EM-fear or currency-driven pullbacks toward $78-83 where Ratio B "
    f"approaches ◉ BUY territory. "
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
    print("  • EM FX is a structural headwind, not a transient one: with")
    print("    ~50% of revenue from emerging markets, every meaningful EM")
    print("    currency depreciation compresses CL's reported USD revenue")
    print("    even as local-currency performance is strong; this is a tax")
    print("    on the EM growth story that does not go away and limits the")
    print("    rate at which EPS compounds in USD terms")
    print("  • Hill's competition is genuinely intensifying: Mars Veterinary")
    print("    Health (Royal Canin + Hills-competitive ranges) and Purina")
    print("    Pro Plan Veterinary Diets are investing heavily in the vet")
    print("    channel; the prescription diet moat is strong but not absolute")
    print("    — it can be eroded over 5-10 years if competitors build the")
    print("    same vet relationships and clinical trial backing")
    print("  • Conservative 2yr is -0.8%: at 24-26× forward earnings on")
    print("    3-4% organic growth, the base case is fair value, not upside;")
    print("    you need either Hill's multiple re-rating or EM volume inflection")
    print("    to generate returns meaningfully above the dividend yield")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • 40% global toothpaste share is the most concentrated single-")
    print("    brand dominance in any major consumer staples category: P&G")
    print("    has 25% oral care share across multiple brands; Colgate has")
    print("    40% with one brand across 200+ countries — this is specification-")
    print("    locked habitual consumption that has resisted every challenger")
    print("    for 80+ years; the consumer who tastes Colgate in childhood")
    print("    in Brazil or India is buying Colgate until they die")
    print("  • Hill's prescription diet moat is genuinely hard to replicate:")
    print("    the vet recommendation is the specification lock; each vet")
    print("    trained on Hill's clinical data becomes a lifetime prescriber;")
    print("    the switching cost is measured in years of clinical credibility,")
    print("    not just shelf placement; therapeutic diets (kidney, diabetes)")
    print("    face virtually no private label competition because the SKU")
    print("    complexity, vet relationships, and clinical trial requirements")
    print("    are economically prohibitive for anyone without Hill's scale")
    print("  • The EM exposure that creates FX headwinds also creates the")
    print("    growth option: India, Africa, and Southeast Asia are at early")
    print("    stages of oral care premiumization — as incomes rise, the")
    print("    transition from local brands to Colgate is a generational")
    print("    compounding event; this is not an immediate catalyst but it")
    print("    is a structural tailwind that does not reverse")
    print("  • 62 consecutive dividend increases: the oral care cash flows")
    print("    are predictable enough to commit to increasing the dividend")
    print("    every year for six consecutive decades — that is a statement")
    print("    about earnings quality that most companies cannot make")
    print("  • Ratio B 0.92× — 26.1% downside / 28.3% upside — modestly")
    print("    favorable; the oral care floor is the put, Hill's growth")
    print("    is the call")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Colgate owns the most concentrated brand dominance in consumer")
    print("  staples — 40% global toothpaste share, held for 30 years — and")
    print("  a prescription pet nutrition business (Hill's) that vets have")
    print("  recommended for 80 years and competitors cannot quickly replicate.")
    print("  The EM FX headwind is structural but so is the EM volume growth")
    print("  opportunity. At $92 — 26.1% from bear, 28.3% from bull — the")
    print("  oral care monopoly and the Hill's gem are modestly attractively")
    print("  priced. Accumulate steadily; add on EM-fear or currency-driven")
    print("  pullbacks toward $78-83.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
