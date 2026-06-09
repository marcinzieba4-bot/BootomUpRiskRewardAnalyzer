"""
Procter & Gamble Co. (NYSE: PG) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 1.05×  |  EPP Gap: +54.5%
=======================================================================
THE CONSUMER STAPLES COMPOUNDER WITH 68 YEARS OF DIVIDEND GROWTH: P&G's
portfolio — Tide, Pampers, Gillette, Oral-B, Crest, Head & Shoulders,
Pantene, Bounty, Charmin, Dawn, Febreze, SK-II, Olay, Always — represents
50+ years of brand equity compounding in 10 focus categories across 180+
countries. The 2022-2024 pricing cycle demonstrated that consumers absorb
5-8% annual price increases before switching to private label at meaningful
scale; the question at $170 is not whether the moat is real — it is
whether the premium valuation (22-24× forward earnings) is justified by
2-3% organic volume growth. The honest answer is: mostly yes, but the
margin of safety is thin.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "PG"
COMPANY        = "Procter & Gamble Co."
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Consumer Staples · Household & Personal Care / Beauty / Baby & Family / Healthcare · NYSE: PG"
SECTOR_GROUP   = "Consumer Staples"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 170.00          # USD — mid-2026; steady compounder near fair value
ANNUAL_DIV     = 4.04            # USD/yr (~2.4% yield); 68th consecutive annual increase in 2025
SHARES_OUT_B   = 2.35            # billions

FW52_HIGH      = 185.00
FW52_LOW       = 148.00

# ── Scenario prices ─────────────────────────────────────────────────────────
# BEAR  — volume capitulation + GLP-1 structural headwind: consumers trade
#         down to private label after 3 years of price increases; GLP-1 drugs
#         structurally reduce consumption in snacking-adjacent and obesity-
#         linked categories; China beauty recovery stalls (SK-II exposure);
#         multiple compresses toward 18-20× on decelerating organic growth
# BASE  — steady compounder: 2-3% organic volume growth, 1-2% pricing, EPS
#         $7.85 at 22× → $173 + $4 div → essentially flat; the base case
#         at this valuation IS "approximately fair"
# BULL  — emerging markets acceleration + premiumization: India, Africa, and
#         Middle East markets inflect; Tide PODS/premium tier gains share in
#         developed markets; SK-II recovery in China; EPS $9+ by 2028 at 24×
# XBULL — structural share consolidation: private label structural weakness
#         on quality gaps + P&G innovation leads to sustained volume recovery;
#         multiple re-rates to 26-28× as investors price the pricing power
BEAR           = 128.0
BASE           = 170.0
BULL           = 210.0
XBULL          = 250.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: severe recession + commodity spike + volume decline; core
# Tide/Pampers/Gillette still earn ~$5.50/sh at trough
# PE_TROUGH: 20× reflects premium maintained even in distress for a Dividend King
EPS_TROUGH     = 5.50
PE_TROUGH      = 20.0
EPP            = EPS_TROUGH * PE_TROUGH     # $110.00

# ── Conservative 2-year price estimate ───────────────────────────────────────
# FY2027E adj EPS ~$7.85 × 22× conservative multiple + $4.04 div
# Conservative case +3.9% — modest positive return; fair value
PE_CONSERVATIVE  = 22.0
EPS_FY2026E      = 7.85
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $176.74

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
    ("tide_pampers_gillette_oral_b_brand_equity_50yr_consumer_specification_lock_in",     4.0, 0.22),
    ("pricing_power_5_8pct_annual_increases_2022_2024_with_limited_volume_defection",     3.5, 0.20),
    ("emerging_markets_india_africa_middle_east_underpenetrated_long_cycle_growth",       3.5, 0.18),
    ("dividend_king_68_consecutive_increases_capital_allocation_and_buyback_consistency", 3.5, 0.15),
    ("premiumization_innovation_pods_sk2_olay_premium_and_oral_b_io_toothbrush",          3.0, 0.15),
    ("glp1_private_label_trade_down_and_22_24x_valuation_with_2_3pct_organic_growth",    2.0, 0.10),
]

# ── Structural Competitive Advantage (SCA) factors ───────────────────────────
SCA_FACTORS = {
    "tide_pampers_gillette_brand_equity_50yr_compounding_household_specification":        +0.18,
    "pricing_power_demonstrated_repeated_5_8pct_increases_without_sustained_share_loss": +0.14,
    "emerging_market_underpenetration_india_africa_middle_east_50pct_revenue_exposure":  +0.10,
    "68_consecutive_dividend_increases_and_systematic_share_buybacks_capital_return":    +0.08,
    "glp1_drugs_potential_structural_volume_decline_in_several_pg_categories":           -0.06,
    "private_label_trade_down_risk_after_3yr_of_price_increases_consumer_fatigue":       -0.08,
    "22_24x_forward_pe_premium_valuation_limits_upside_on_2_3pct_organic_growth":        -0.08,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.28

# ── Weighted conviction score ─────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ────────────────────────────────────────────────────────────
SUMMARY = (
    f"PG ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE CONSUMER STAPLES COMPOUNDER WITH 68 YEARS OF DIVIDEND GROWTH: P&G's portfolio "
    "— Tide, Pampers, Gillette, Oral-B, Crest, Head & Shoulders, Pantene, Bounty, Charmin, "
    "Dawn, Febreze, SK-II, Olay — represents 50+ years of brand equity in 10 focus "
    "categories across 180+ countries. "
    "THE PRICING POWER IS REAL AND DEMONSTRATED: 2022-2024 pricing cycle delivered 5-8% "
    "annual price increases across nearly every category with limited volume defection — "
    "this is not hypothetical moat, it is observed consumer behavior; the Tide/Ariel "
    "consumer has absorbed three consecutive years of increases and is still in the "
    "category, which tells you what the brand equity is actually worth. "
    "EMERGING MARKETS ARE THE LONG-DURATION OPTION: ~50% of P&G revenue comes from "
    "outside North America/Europe; India, Africa, and Middle East are underpenetrated "
    "in Pampers, Oral-B, and premium fabric care — each percentage point of penetration "
    "gain in a market with 1.4B people is a multi-year compounding event. "
    "THE HONEST RISK: at 22-24× forward earnings, the base case is essentially priced in; "
    "GLP-1 drugs may structurally reduce consumption in obesity-adjacent categories; "
    "private label has gained 2-3% category share across US grocery in 2022-2024 as "
    "consumers absorb the price increases — the elasticity ceiling is unclear; "
    "SK-II China exposure adds geopolitical risk; the conservative 2yr case ($177) is "
    "only +3.9% — not enough to excite anyone. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — "
    "modest positive return; BULL/XBULL require emerging market volume inflection. "
    "Accumulate steadily; add meaningfully on any macro-driven pullbacks toward "
    f"$148-155 where Ratio B approaches ◉ BUY territory. "
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
    print("  • At 22-24× forward earnings, the moat is priced in: P&G's")
    print("    brand equity is not a secret — every institutional investor")
    print("    owns it, and the premium multiple reflects that consensus;")
    print("    the base case 2yr return is only +3.9%, which is below")
    print("    the cost of equity for most investors")
    print("  • Organic volume growth has been 2-3% for most of P&G's recent")
    print("    history — not bad for a $400B+ market cap company, but not")
    print("    enough to drive upside from a 22-24× starting point without")
    print("    meaningful multiple expansion or EPS acceleration")
    print("  • GLP-1 drug adoption is a genuine structural uncertainty: drugs")
    print("    that reduce obesity and change eating/consumption behavior have")
    print("    unknown long-term category implications for personal care,")
    print("    health, and home care; the category impact analysis is still")
    print("    early and the worst case is not captured in consensus estimates")
    print("  • Private label gained share in the 2022-2024 pricing cycle:")
    print("    US private label grocery share went from ~18% to ~21% — the")
    print("    question is whether this reverses (moat holding) or continues")
    print("    (moat erosion); the data is ambiguous and the risk is real")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The pricing power demonstration in 2022-2024 was exceptional:")
    print("    5-8% annual price increases across virtually every category")
    print("    with the consumer absorbing them — this is the clearest live")
    print("    demonstration of brand equity since the 2008-2010 cycle; a")
    print("    company that can pass through inflation and maintain share")
    print("    has a moat that transcends economic cycle analysis")
    print("  • Tide, Pampers, and Gillette are not just brands — they are")
    print("    specifications: the Tide consumer has a sensory memory of")
    print("    what 'clean' smells like; the Pampers parent has established")
    print("    a trust relationship with their child's comfort; the Gillette")
    print("    user has a learned ritual — these are habitual behaviors that")
    print("    take genuine disruption to dislodge, not just price pressure")
    print("  • Emerging markets represent 20+ years of compounding ahead:")
    print("    India has 1.4B people with Pampers penetration still in the")
    print("    teens; Africa has 1.4B people where premium fabric care is")
    print("    barely introduced; these are not incremental opportunities,")
    print("    they are generational category builds")
    print("  • 68 consecutive dividend increases is a capital allocation")
    print("    statement: management is contractually obligated (by investor")
    print("    expectation) to grow the dividend every year, which imposes")
    print("    a discipline on capital allocation that most companies lack")
    print("  • Ratio B 1.05× — 24.7% downside / 23.5% upside — modestly")
    print("    unfavorable but within ◎ ACCUMULATE range; the EPP floor")
    print("    at $110 represents the genuine distress scenario")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  P&G has been raising its dividend for 68 consecutive years —")
    print("  through recessions, pandemics, and commodity spikes — because")
    print("  the consumer keeps buying Tide, Pampers, and Gillette regardless")
    print("  of what the macro is doing. The 2022-2024 pricing cycle proved")
    print("  the moat is structural, not nostalgic. At $170, the premium is")
    print("  real and the upside is modest — this is not a deep-value entry.")
    print("  But for an investor who wants compounding consumer franchise")
    print("  exposure with 2.4% yield and 68-year dividend growth pedigree,")
    print("  accumulate steadily and add meaningfully on any pullback toward")
    print("  $148-155 where the risk/reward materially improves.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
