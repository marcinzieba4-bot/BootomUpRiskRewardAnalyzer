"""
The Kraft Heinz Company (NASDAQ: KHC) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.88×  |  EPP Gap: +93.9%
=======================================================================
THE ICONIC BRANDS THAT 3G CAPITAL NEARLY DESTROYED — AND BERKSHIRE
STILL OWNS: Kraft Heinz is the most complicated major consumer staples
company in the world. It owns genuinely extraordinary brands — Heinz
ketchup (~40% global share, the default condiment in 140+ countries),
Philadelphia cream cheese (category-defining in multiple markets), Kraft
Mac & Cheese (a cultural institution), Oscar Mayer, Velveeta, Jell-O,
Planters — and it has spent a decade systematically underinvesting in
them. 3G Capital's zero-based budgeting philosophy stripped out costs
but also stripped out the brand-building spend, the innovation pipeline,
and the organizational capability that makes consumer brands durable.
The 2019 reckoning was brutal: a $15.4B goodwill impairment, an SEC
investigation, and a dividend cut from $2.50 to $1.60/yr that signaled
the model was broken. What remains is a genuinely interesting question:
can Heinz ketchup, Philadelphia, and Kraft Mac & Cheese — brands with
decades of household penetration and emotional equity — be rebuilt by
new management without the 3G playbook? Berkshire Hathaway's 26% stake
(and Warren Buffett's public acknowledgment that he overpaid) provides
a financial backstop and prevents distressed asset disposition but also
signals the ceiling on strategic optionality.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "KHC"
COMPANY        = "The Kraft Heinz Company"
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Consumer Staples · Packaged Foods / Condiments / Dairy & Refrigerated · NASDAQ: KHC"
SECTOR_GROUP   = "Consumer Staples"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 32.00           # USD — mid-2026; persistent underperformance vs staples peers
ANNUAL_DIV     = 1.60            # USD/yr (~5.0% yield); cut from $2.50 in 2019
SHARES_OUT_B   = 1.22            # billions

FW52_HIGH      = 40.00
FW52_LOW       = 26.00

# ── Scenario prices ───────────────────────────────────────────────────────────
# BEAR  — brand irrelevance accelerates: private label captures another 5-10%
#         share across KHC's core categories; organic revenue turns negative;
#         further goodwill impairment required on remaining $30B+ balance sheet;
#         dividend cut again to preserve cash; Berkshire exits stake; stock
#         re-rates as deep value trap with no clear catalyst at 8-9× EPS
# BASE  — turnaround credibility: Abrams-Rivera rebuilds brand investment,
#         Heinz and Philadelphia stabilize share, Kraft Mac & Cheese holds;
#         organic growth returns to +1-2%/yr; adj EPS ~$2.80 × 12× + div → ~$35
# BULL  — brand renaissance: meaningful innovation in Heinz adjacent categories
#         (hot sauce, premium condiments), Philadelphia expands snacking formats,
#         Lunchables reformulation addresses school nutrition; adj EPS $3.50+
#         × 14-15×; Berkshire stake prevents hostile action, enables patience
# XBULL — strategic transaction: acquiree or meaningful divesting of
#         underperforming brands (Velveeta, Jell-O) to fund reinvestment;
#         or Berkshire reduces stake enabling corporate action at premium
BEAR           = 18.0
BASE           = 32.0
BULL           = 48.0
XBULL          = 62.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: organic decline + further impairments + private label erosion;
# still earns ~$1.50 — Heinz ketchup global condiment share does not go to
# zero even in the worst scenario; the brands have real residual value
# PE_TROUGH: 11× reflects a packaged food company with confirmed structural
# challenges but not bankruptcy risk; Berkshire stake provides a floor bid
EPS_TROUGH     = 1.50
PE_TROUGH      = 11.0
EPP            = EPS_TROUGH * PE_TROUGH    # $16.50

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E adj EPS ~$2.80 × 12× conservative multiple + $1.60 div
PE_CONSERVATIVE  = 12.0
EPS_FY2026E      = 2.80
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV  # $35.20

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
    ("heinz_ketchup_40pct_global_share_and_condiment_category_leadership",             3.5, 0.20),
    ("berkshire_hathaway_26pct_stake_financial_backstop_and_strategic_patience",       3.0, 0.15),
    ("philadelphia_kraft_mac_oscar_mayer_household_name_brand_equity",                 2.5, 0.18),
    ("private_label_share_capture_and_3g_brand_underinvestment_decade_long_legacy",   1.5, 0.25),
    ("goodwill_impairment_risk_30b_plus_balance_sheet_and_organic_growth_stagnation",  1.5, 0.22),
]

# ── Structural Competitive Advantage (SCA) factors ─────────────────────────────
SCA_FACTORS = {
    "heinz_ketchup_40pct_global_share_140_plus_countries_genuine_condiment_default":   +0.14,
    "philadelphia_cream_cheese_and_kraft_mac_category_defining_household_penetration": +0.10,
    "berkshire_hathaway_26pct_stake_prevents_distressed_sale_and_enables_patience":    +0.08,
    "decade_of_3g_zero_based_budgeting_brand_underinvestment_relevance_erosion":       -0.14,
    "private_label_capturing_share_across_condiments_dairy_and_refrigerated_meats":   -0.12,
    "30b_plus_goodwill_impairment_risk_and_sec_investigation_management_credibility":  -0.10,
    "organic_revenue_persistently_flat_or_negative_volume_mix_structural_headwind":   -0.08,
}
SCA_NET = sum(SCA_FACTORS.values())   # -0.12

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"KHC ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.2f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE ICONIC BRANDS THAT 3G CAPITAL NEARLY DESTROYED — AND BERKSHIRE STILL OWNS: Kraft Heinz "
    "owns genuinely extraordinary brands — Heinz ketchup (~40% global share, the default condiment "
    "in 140+ countries), Philadelphia cream cheese (category-defining), Kraft Mac & Cheese (cultural "
    "institution), Oscar Mayer, Velveeta, Planters — and spent a decade systematically underinvesting "
    "in them. 3G Capital's zero-based budgeting stripped costs but also stripped brand investment, "
    "innovation pipeline, and organizational capability. The 2019 reckoning: $15.4B goodwill "
    "impairment, SEC investigation, dividend cut from $2.50 to $1.60/yr. "
    "WHAT MAKES THIS AN ACCUMULATE NOT AN AVOID: Heinz ketchup's 40% global share is real and "
    "durable — condiments have higher brand loyalty than most food categories; Berkshire Hathaway's "
    "26% stake prevents distressed asset disposition and provides patience for a multi-year "
    "turnaround; at $32 (~11× forward earnings) the market is pricing in continued deterioration "
    "and the 5% yield compensates for waiting. "
    "SCA_NET = -0.12 — the only negative SCA in the model universe: KHC's structural headwinds "
    "(private label gaining share, organic decline, goodwill overhang) genuinely exceed its "
    "competitive advantages at current brand investment levels. This is a turnaround bet, not a "
    "compounder. "
    "THE HONEST RISK: WCS 2.30 is the lowest in the universe — the conviction on execution is "
    "genuinely low; private label has taken permanent share in Oscar Mayer cold cuts, Velveeta, "
    "and Jell-O categories; the brand rehabilitation requires 5+ years of reinvestment that "
    "will compress near-term earnings before it improves long-term ones; Berkshire's 26% stake "
    "is a ceiling, not a floor — Buffett publicly acknowledged overpaying. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}%. "
    "Sized small: accumulate for the yield and turnaround optionality; do not average down "
    f"aggressively without evidence of organic growth stabilization. "
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
    print("  WHY THIS IS AN ◎ ACCUMULATE, NOT A ◌ WATCHLIST OR ✕ AVOID")
    print()
    print("  NOT ✕ AVOID (despite negative SCA) because:")
    print("  • Heinz ketchup is genuinely irreplaceable: 40% global share in")
    print("    a condiment category where brand loyalty is unusually high —")
    print("    people use the same ketchup brand their parents used and teach")
    print("    their children to do the same; no private label product has")
    print("    meaningfully eroded Heinz's core ketchup share despite being")
    print("    40-50% cheaper for decades")
    print("  • The 5.0% yield at $32 is real income while waiting: at ~53%")
    print("    payout on $2.80 adj EPS, the dividend is covered and KHC's")
    print("    cash generation is sufficient to maintain it without a second")
    print("    cut in a base-case scenario")
    print("  • Berkshire's 26% stake prevents the worst outcomes: Buffett's")
    print("    presence prevents distressed asset fire sales, hostile bids at")
    print("    unfair prices, and the kind of financial engineering that would")
    print("    hollow out remaining brand equity; it provides the patience that")
    print("    brand rehabilitation requires")
    print("  • At 11× forward earnings the downside scenario is substantially")
    print("    priced: a business with Heinz, Philadelphia, and Kraft Mac should")
    print("    not trade at 11× unless the market expects continued decline —")
    print("    that pessimism creates the asymmetric setup")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The Ratio B 0.88× — 43.8% downside / 50.0% upside — is the")
    print("    widest asymmetry in the Consumer Staples universe in this model;")
    print("    the upside scenarios reflect genuine brand equity that could be")
    print("    unlocked with sustained reinvestment, not hope")
    print("  • The new CEO (Abrams-Rivera, 2024) has a mandate to rebuild brand")
    print("    investment and has explicitly renounced the 3G cost-only playbook;")
    print("    early evidence (increased A&P spending, innovation in Heinz hot")
    print("    sauce and Philadelphia snacking formats) is directionally correct")
    print("  • WCS 2.30 is the lowest in the universe but the risk/reward at")
    print("    0.88× still justifies accumulation at small position size")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Kraft Heinz is a cautionary tale that became a value opportunity.")
    print("  The 3G Capital playbook extracted cash at the cost of brand equity,")
    print("  the 2019 impairment was the reckoning, and now at $32 the stock")
    print("  prices in continued failure. Heinz ketchup's 40% global share and")
    print("  Philadelphia cream cheese's category leadership are real assets")
    print("  that have not been destroyed — they have been neglected. The 5%")
    print("  yield pays you to wait, Berkshire prevents the worst outcomes, and")
    print("  Abrams-Rivera's reinvestment mandate is the catalyst watch. Size")
    print("  small — SCA_NET = -0.12 and WCS = 2.30 are honest signals that")
    print("  this is a turnaround bet, not a compounder. Do not average down")
    print("  without evidence that organic growth has stabilized.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
