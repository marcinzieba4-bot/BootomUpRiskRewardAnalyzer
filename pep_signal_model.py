"""
PepsiCo, Inc. (NASDAQ: PEP) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 1.09×  |  EPP Gap: +73.3%
=======================================================================
THE SNACK EMPIRE THAT BEVERAGES BUILT: PepsiCo's underappreciated truth
is that Frito-Lay — Lay's, Doritos, Cheetos, Fritos, Tostitos, Ruffles —
is the actual crown jewel. Frito-Lay generates ~45% of PepsiCo's operating
profit at margins (25%+) that most consumer staples companies would trade
their entire portfolio for, while holding US salty snack share north of
40% for three consecutive decades. The beverage business (Pepsi, Mountain
Dew, Gatorade, Lipton, Starry) is a strong second act. At $162, PEP is
discounted relative to its snack/beverage peer set on persistent GLP-1
and North America volume concerns that are real but overstated as permanent
structural breaks.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "PEP"
COMPANY        = "PepsiCo, Inc."
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Consumer Staples · Beverages & Snack Foods / Frito-Lay / Gatorade / Quaker · NASDAQ: PEP"
SECTOR_GROUP   = "Consumer Staples"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 162.00          # USD — mid-2026; discount to historical multiple on GLP-1/BevNA volume concerns
ANNUAL_DIV     = 5.42            # USD/yr (~3.3% yield); 52nd consecutive annual increase (Dividend King)
SHARES_OUT_B   = 1.38            # billions

FW52_HIGH      = 178.00
FW52_LOW       = 138.00

# ── Scenario prices ─────────────────────────────────────────────────────────
# BEAR  — GLP-1 snack impact materializes + BevNA secular decline: GLP-1
#         adoption accelerates and salty snack consumption structurally
#         declines 3-5% annually; PepsiCo Beverages NA volumes continue
#         declining as consumers shift to water/RTD coffee/energy; Quaker
#         reputational damage proves sticky; multiple compresses to 14-15×
#         as growth narrative for the snack category breaks
# BASE  — modest recovery: Frito-Lay volumes stabilize after 2023-24 price
#         fatigue; BevNA sequential improvement; Gatorade holds share vs.
#         Body Armor; EPS $8.65 at 18× + $5.42 div → flat
# BULL  — snack resilience confirmed + international inflection: GLP-1 snack
#         impact proves modest; Frito-Lay international (India, China, LatAm)
#         accelerates; Gatorade Zero captures health-conscious sports market;
#         multiple re-rates to 22× as snack category premium is restored
# XBULL — Frito-Lay re-rated as standalone: market separately values the
#         snack business at 25-28× EBITDA; international snacking category
#         builds in Asia/Africa become material; EPS $10+ by 2028
BEAR           = 115.0
BASE           = 162.0
BULL           = 205.0
XBULL          = 248.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: recession + volume declines + GLP-1 headwind; Frito-Lay and
# Gatorade still earn ~$5.50/sh through most scenarios
# PE_TROUGH: 17× reflects diversified snack + beverage at genuine distress
EPS_TROUGH     = 5.50
PE_TROUGH      = 17.0
EPP            = EPS_TROUGH * PE_TROUGH     # $93.50

# ── Conservative 2-year price estimate ───────────────────────────────────────
# FY2027E adj EPS ~$8.65 × 18× conservative multiple + $5.42 div
# Conservative case essentially flat (-0.5%) — snack/bev at fair value
PE_CONSERVATIVE  = 18.0
EPS_FY2026E      = 8.65
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $161.12

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
    ("frito_lay_40pct_us_salty_snack_share_doritos_lays_cheetos_three_decade_leadership", 4.0, 0.22),
    ("gatorade_70pct_sports_hydration_share_g2_zero_and_gatorlyte_health_pivot",          3.5, 0.18),
    ("pricing_power_snack_and_bev_category_inelasticity_demonstrated_2022_2024",          3.5, 0.17),
    ("dividend_king_52_consecutive_increases_3_3pct_yield_income_anchor",                 3.5, 0.15),
    ("frito_lay_international_india_china_latam_underpenetrated_snack_category_builds",   3.0, 0.15),
    ("glp1_snack_impact_bevna_volume_weakness_and_quaker_recall_overhang",                2.0, 0.13),
]

# ── Structural Competitive Advantage (SCA) factors ───────────────────────────
SCA_FACTORS = {
    "frito_lay_40pct_salty_snack_share_doritos_lays_cheetos_fritos_tostitos_ruffles":     +0.18,
    "gatorade_70pct_sports_hydration_share_proprietary_electrolyte_formulation":          +0.12,
    "snack_pricing_power_category_inelasticity_and_habitual_repeat_purchase_behavior":    +0.10,
    "frito_lay_international_snack_category_build_emerging_markets_long_runway":          +0.08,
    "glp1_drugs_could_structurally_reduce_snack_consumption_more_acutely_than_beverages": -0.12,
    "bevna_volume_declines_2023_2024_consumer_value_perception_gap_premium_resistance":   -0.08,
    "quaker_foods_recall_reputational_damage_and_manufacturing_quality_overhang":         -0.04,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.24

# ── Weighted conviction score ─────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ────────────────────────────────────────────────────────────
SUMMARY = (
    f"PEP ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE SNACK EMPIRE THAT BEVERAGES BUILT: Frito-Lay — Lay's, Doritos, Cheetos, Fritos, "
    "Tostitos, Ruffles — is the actual crown jewel, generating ~45% of PepsiCo's operating "
    "profit at 25%+ margins while holding US salty snack share above 40% for three "
    "consecutive decades. Gatorade commands ~70% of sports hydration. The beverage "
    "business (Pepsi, Mountain Dew, Lipton, Starry) is a strong second act. "
    "FRITO-LAY IS THE STRUCTURAL MOAT: salty snacks are habitual, impulsive, and "
    "experiential — the Doritos consumer is not reading nutrition labels at the "
    "vending machine; the Lay's consumer has a sensory memory built over decades; "
    "category switching costs are low but switching behavior is lower; Frito-Lay has "
    "held 40%+ US share through every recession, health trend, and private label wave "
    "since the 1980s. "
    "GLP-1 IS THE HONEST OVERHANG: more acute for PEP than KO — drugs that reduce "
    "appetite and snack cravings represent a more direct threat to Frito-Lay than "
    "to Coke Zero; BevNA volume has been declining; Quaker recall (2024) added "
    "reputational noise; but GLP-1 penetration at scale requires economics and "
    "adherence that remain challenging for most consumers. "
    "DIVIDEND KING PEDIGREE: 52 consecutive increases, ~3.3% yield — meaningfully "
    "higher than KO or PG and the best yield in the peer group. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — "
    "essentially flat; BULL requires Frito-Lay volume recovery + international inflection. "
    "Accumulate; add meaningfully on GLP-1-driven pullbacks toward "
    f"$138-145 where Ratio B enters ◉ BUY territory. "
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
    print("  • GLP-1 is more acute for PEP than for any other consumer")
    print("    staples company: drugs that reduce appetite and snack cravings")
    print("    are a more direct structural threat to Doritos and Cheetos than")
    print("    to Tide or Coke Zero; if GLP-1 adherence scales beyond the")
    print("    current ~2-3% of US adults to 10-15%, the Frito-Lay volume")
    print("    thesis weakens in a way that 'Frito-Lay has held share for")
    print("    30 years' does not address")
    print("  • BevNA has been structurally weak: North America beverage volumes")
    print("    declined in 2023 and 2024 as consumers pushed back on pricing;")
    print("    the value perception gap vs. private label RTDs has widened;")
    print("    the Pepsi brand does not command the same premium to category")
    print("    as Coca-Cola Classic does in its segment")
    print("  • Conservative 2yr is essentially flat (-0.5%): at $162, with a")
    print("    3.3% yield, the total 2yr return on the conservative case is")
    print("    +6.2% including dividends — acceptable but not compelling versus")
    print("    the risk of GLP-1 narrative acceleration")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • Frito-Lay's 40%+ salty snack share across three decades is")
    print("    the most durable category leadership in consumer staples: it")
    print("    survived Atkins, the low-fat craze, keto, clean eating, and")
    print("    every other health trend since 1985; the Doritos consumer is")
    print("    habitual in a way that is genuinely difficult to dislodge —")
    print("    the question about GLP-1 is how many habitual snackers are")
    print("    willing to pay $1,200/month and inject themselves weekly to")
    print("    stop eating chips; the answer is: fewer than feared")
    print("  • Gatorade's 70% sports hydration share is a genuine moat:")
    print("    endorsed by every major US sports organization, specification-")
    print("    locked into NFL/NBA/MLB sidelines, and protected by proprietary")
    print("    electrolyte formulations; Body Armor has grown but Gatorade")
    print("    Zero and Gatorlyte are responding; this is a business with")
    print("    structural advantages that a PepsiCo-scale distributor protects")
    print("  • The 3.3% yield is the highest in the Big Three staples (PG,")
    print("    KO, PEP): at $162, income investors have a genuine entry point")
    print("    that anchors valuation and provides a total return floor;")
    print("    52 consecutive dividend increases means the commitment is real")
    print("  • At 18-19× forward earnings, PEP trades at a discount to its")
    print("    10yr average (21-22×) and at a discount to KO and PG despite")
    print("    owning the #1 snack business on earth — the discount is the")
    print("    GLP-1 fear premium that is at least partially already priced in")
    print("  • Ratio B 1.09× — 29.0% downside / 26.5% upside — modestly")
    print("    unfavorable but firmly within ◎ ACCUMULATE range")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  PepsiCo owns the #1 US salty snack franchise (40%+ share, 30+")
    print("  years), the #1 sports hydration brand (Gatorade, 70% share),")
    print("  and a beverage portfolio with structural pricing power. The")
    print("  2023-2024 volume weakness is real but cyclical — price fatigue")
    print("  after 5-7% annual increases, not a structural brand break. GLP-1")
    print("  is the genuine uncertainty: if snack consumption declines 2-3%")
    print("  annually at scale, the Frito-Lay thesis gets more complicated.")
    print("  At $162 — 18-19× forward earnings, 3.3% yield, 52-year Dividend")
    print("  King — the GLP-1 fear is largely in the price. Accumulate here;")
    print("  add aggressively toward $138-145 where Ratio B enters BUY range.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
