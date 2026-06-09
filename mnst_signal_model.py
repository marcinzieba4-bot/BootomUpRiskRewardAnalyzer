"""
Monster Beverage Corporation (NASDAQ: MNST) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.91×  |  EPP Gap: +75.8%
=======================================================================
THE ENERGY DRINK COMPOUNDER WITH COCA-COLA'S DISTRIBUTION ARMY: Monster
Beverage is the #2 global energy drink brand — and it has something Red
Bull (private, family-controlled, self-distributing) does not: the full
weight of the Coca-Cola distribution system behind it. In 2015, Coca-Cola
acquired a ~20% strategic stake and transferred its energy drink portfolio
to Monster in exchange for Monster entering Coke's global distribution
network — 145+ countries, millions of retail touchpoints, the cold-chain
infrastructure and cooler space that defines beverage success. This is not
a minor advantage. Red Bull built its own distribution army over 40 years;
Monster inherited Coca-Cola's. The energy drink category is one of the
best-performing beverage segments globally: premium priced (3-4× regular
soft drink), impulse purchased, consumed by 18-35 demographics with high
brand loyalty, and dramatically underpenetrated outside North America and
Western Europe. Monster at ~37% US market share, 30%+ EBIT margins, and
an asset-light co-packing model is the pure-play vehicle on a category
that is still in the early innings globally.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "MNST"
COMPANY        = "Monster Beverage Corporation"
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Consumer Staples · Energy Drinks / Functional Beverages / Alcohol · NASDAQ: MNST"
SECTOR_GROUP   = "Consumer Staples"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 58.00           # USD — mid-2026
ANNUAL_DIV     = 0.00            # no dividend; all capital return via buybacks
SHARES_OUT_B   = 0.93            # billions; consistent buybacks reducing float

FW52_HIGH      = 72.00
FW52_LOW       = 46.00

# ── Scenario prices ───────────────────────────────────────────────────────────
# BEAR  — category deceleration: energy drink consumption plateaus in North
#         America as GLP-1 adoption reduces impulsive consumption; health/
#         wellness backlash against high-caffeine products intensifies;
#         FDA regulatory action on energy drink caffeine limits;
#         international expansion slower than expected; multiple compresses
#         to 22-24× on growth deceleration; adj EPS $1.55-1.65 at 24× → ~$38
# BASE  — steady international compounding: North America matures at low
#         single digits, international (EM, Europe) grows 10-15%/yr as
#         per capita consumption closes gap with US; adj EPS $2.00 × 30×
#         → ~$60; Coke partnership deepens distribution reach
# BULL  — international acceleration + The Beast (alcohol) scale: EMEA and
#         Asia-Pacific energy drink per capita approaches 50% of US levels;
#         The Beast Unleashed alcohol line achieves 1-2% share in FMB;
#         adj EPS $2.60+ × 32×; category tailwinds from gaming/esports
#         partnerships sustain youth demographic engagement
# XBULL — category leader consolidation: Monster acquires smaller brands
#         (Reign, Bang-successor) to defend channel space; international
#         adjacencies in functional hydration/sports; adj EPS $3.50+ by 2029
BEAR           = 38.0
BASE           = 58.0
BULL           = 80.0
XBULL          = 102.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPP = pessimistic_PE × current EPS — what is this business worth at a
# de-rated multiple on what it actually earns today?
# PE_PESSIMISTIC: 20× — premium beverage franchise with Coke distribution and
# 37% US share retains a premium floor multiple even under competitive pressure;
# applied to current adj EPS $2.00/sh which itself reflects a below-trend year
PE_PESSIMISTIC = 20.0
EPS_FY2026E    = 2.00
EPP            = PE_PESSIMISTIC * EPS_FY2026E    # 20 × $2.00 = $40.00

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E adj EPS ~$2.00 × 30× conservative multiple (no dividend)
PE_CONSERVATIVE  = 30.0
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV  # $60.00

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
    ("coca_cola_distribution_145_countries_and_20pct_strategic_stake_structural_moat", 4.0, 0.22),
    ("37pct_us_energy_drink_share_brand_loyalty_and_innovation_pipeline",              3.5, 0.20),
    ("asset_light_co_packing_30pct_plus_ebit_margins_and_buyback_capital_return",      3.5, 0.18),
    ("international_early_innings_em_europe_underpenetrated_10_to_15pct_growth",       3.5, 0.18),
    ("glp1_health_wellness_headwind_and_regulatory_caffeine_limit_risk",               2.5, 0.22),
]

# ── Structural Competitive Advantage (SCA) factors ─────────────────────────────
SCA_FACTORS = {
    "coca_cola_145_country_distribution_cold_chain_and_cooler_space_advantage":        +0.18,
    "37pct_us_share_and_monster_brand_identity_in_18_to_35_demographic":               +0.14,
    "asset_light_co_packing_model_30pct_plus_ebit_and_negative_working_capital":       +0.12,
    "international_per_capita_consumption_gap_vs_us_structural_multi_decade_runway":   +0.10,
    "glp1_health_wellness_trend_and_high_caffeine_regulatory_scrutiny_headwind":       -0.10,
    "international_margin_dilution_as_new_markets_require_investment_to_ramp":        -0.08,
    "red_bull_private_deep_pockets_and_category_creator_loyalty_competitive_threat":   -0.08,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.28

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"MNST ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.2f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE ENERGY DRINK COMPOUNDER WITH COCA-COLA'S DISTRIBUTION ARMY: Monster is the #2 global "
    "energy drink brand with something Red Bull lacks — the full Coca-Cola distribution system "
    "in 145+ countries. In 2015, KO acquired ~20% of MNST and transferred its energy portfolio "
    "to Monster in exchange for global distribution; Red Bull built its own distribution army "
    "over 40 years, Monster inherited Coca-Cola's. THE CATEGORY IS EARLY INNINGS GLOBALLY: "
    "energy drink per capita in India, Southeast Asia, and most of EM is 5-10% of US levels — "
    "every income step-up in these markets creates new category entrants; Monster is already "
    "on-shelf via Coke in these markets. ASSET-LIGHT MODEL GENERATES EXCEPTIONAL RETURNS: "
    "co-packing (no owned manufacturing) plus Coke distribution (no owned logistics) means "
    "Monster's capital intensity is near-zero — 30%+ EBIT margins on ~$7B revenue with FCF "
    "converted almost entirely to buybacks. US SHARE IS THE DEFENSIVE MOAT: 37% US share held "
    "against Red Bull, Celsius, and Reign for years through constant innovation (Ultra, Rehab, "
    "Java, Reign, The Beast alcohol line) — the brand architecture creates shelf space "
    "ownership that new entrants cannot easily displace. "
    "THE HONEST RISK: 30-35× PE leaves no earnings-basis margin of safety — any growth "
    "deceleration (North America maturation, GLP-1 reducing impulsive consumption, FDA caffeine "
    "regulation) compresses the multiple and earnings simultaneously; Celsius has demonstrated "
    "that the energy drink category is not as moat-protected as soft drinks and new entrants "
    "can take share quickly with the right brand positioning; international margins are "
    "structurally lower as new markets require investment before they generate returns. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× = "
    f"${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% (no dividend — all buybacks). "
    "BULL requires international acceleration confirming the global runway thesis. "
    f"Add on health/GLP-1/regulatory-fear selloffs toward $48-52. "
    f"Bear ${BEAR:.0f} · Base ${BASE:.0f} · Bull ${BULL:.0f} · XBull ${XBULL:.0f}."
)

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{'='*72}")
    print(f"  {TICKER}  |  {COMPANY}")
    print(f"  {SECTOR}")
    print(f"{'='*72}")
    print(f"  Current Price:                                     ${CURRENT_PRICE:>8.2f}")
    print(f"  Annual Dividend:                            {'none':>12}")
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
    print(f"  PE Pessimistic:                                    {PE_PESSIMISTIC:>8.1f}×")
    print(f"  EPP (Pessimistic PE × current EPS):             ${EPP:>8.2f}")
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
    print("  • 30-35× PE leaves essentially no margin of safety: Monster is")
    print("    priced for continued 10-15%+ earnings growth; any deceleration")
    print("    in North America — whether from GLP-1, health trends, or")
    print("    saturation — causes both earnings compression AND multiple")
    print("    de-rating simultaneously; the double hit is severe")
    print("  • Celsius proved the category is not fully moat-protected:")
    print("    from ~0% to ~11% US share in 3 years by repositioning energy")
    print("    drinks as health/fitness products — Monster's brand identity")
    print("    (extreme sports, gaming) is less defensible against wellness-")
    print("    positioned challengers than Coke is against cola challengers")
    print("  • Conservative 2yr (+3.4%, no dividend) is thin for the valuation")
    print("    risk carried — growth disappointment punishes harshly at 30×")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The Coca-Cola distribution advantage is genuinely structural:")
    print("    Coke has spent 100 years building cold-chain logistics, cooler")
    print("    placement contracts, and route-to-market relationships in 145+")
    print("    countries; Monster doesn't just get distribution — it gets")
    print("    priority shelf space, local market expertise, and a strategic")
    print("    partner that owns ~20% and is economically aligned with growth")
    print("  • International underpenetration is the decadal growth driver:")
    print("    energy drink per capita in India (~0.2L/yr) vs USA (~10L/yr)")
    print("    is a 50× gap — as income rises in EM and Monster lands on Coke")
    print("    trucks that already call on every retailer, this gap closes;")
    print("    Monster's international revenue is growing 15%+/yr from this base")
    print("  • Asset-light at 30%+ EBIT margins compounding with buybacks:")
    print("    Monster owns no factories, no trucks, no warehouses — the FCF")
    print("    conversion is exceptional and flows almost entirely to buybacks;")
    print("    the share count has declined meaningfully over a decade")
    print("  • Ratio B 0.91× — 34.5% downside / 37.9% upside — modestly")
    print("    asymmetric; add on health/regulatory fear selloffs")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Monster Beverage is an asset-light energy drink compounder with")
    print("  Coca-Cola's distribution system and a global category that is")
    print("  dramatically underpenetrated outside North America. The 30%+ EBIT")
    print("  margins fund buybacks while international volume compounds through")
    print("  the Coke network. At $58 — 34.5% from bear, 37.9% from bull —")
    print("  you are paying a premium price (30×) for a genuine growth asset;")
    print("  the conservative case (+3.4%) is thin and the valuation requires")
    print("  execution on international. Accumulate steadily; add aggressively")
    print("  on health-trend or regulatory-fear selloffs toward $48-52 where")
    print("  the risk/reward becomes compelling.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
