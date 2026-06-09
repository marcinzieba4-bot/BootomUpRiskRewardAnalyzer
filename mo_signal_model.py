"""
Altria Group Inc. (NYSE: MO) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.94×  |  EPP Gap: +65.1%
=======================================================================
THE CIGARETTE ROYALTY THAT HAS OUTLIVED EVERY DEATH NOTICE: Altria owns
Marlboro, which holds ~43% of the US cigarette market — the single largest
brand share in any mature consumer staples category in America, held for
five consecutive decades through every anti-tobacco campaign, every tax
increase, every competitive challenge, and every regulatory threat.
The business model is deceptively simple: cigarette volume declines 5-7%
per year, Altria raises price 8-10% per year, net revenue grows 2-4%,
and the extraordinary free cash flow funds a dividend that has grown for
55 consecutive years. The math is reliable because Marlboro smokers are
among the most brand-loyal consumers on earth — the adult smoker who has
been buying Marlboro Reds since age 18 is not switching to a generic for
$0.50/pack savings. The honest question is not whether this model works
(it does, demonstrably), but for how many more years it works — and
whether NJOY and On! oral nicotine pouches can build a second act before
the cigarette annuity becomes genuinely terminal.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "MO"
COMPANY        = "Altria Group Inc."
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Consumer Staples · Tobacco / Oral Nicotine / Smokeless · NYSE: MO"
SECTOR_GROUP   = "Consumer Staples"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 52.00           # USD — mid-2026
ANNUAL_DIV     = 4.08            # USD/yr (~7.8% yield); 55 consecutive years of growth
SHARES_OUT_B   = 1.72            # billions

FW52_HIGH      = 60.00
FW52_LOW       = 42.00

# ── Scenario prices ───────────────────────────────────────────────────────────
# BEAR  — FDA menthol ban implemented and upheld: menthol represents ~35%
#         of US cigarette volume; a menthol ban accelerates illicit trade,
#         accelerates switching to oral nicotine, and removes Marlboro's
#         most defensible premium segment; NJOY fails to gain share against
#         ZYN (PMI) and On!; volume declines accelerate to 8-10%/yr;
#         pricing power weakens as smokers can't afford increases; dividend
#         cut becomes necessary; stock re-rates to 8-9× on impaired earnings
# BASE  — Status quo: menthol ban delayed/litigation-blocked, pricing power
#         holds at 7-8%/yr offsetting 5-6% volume declines, NJOY grows
#         modestly, On! nicotine pouch stake performs; adj EPS $5.00 × 10×
#         + div → ~$54; dividend sustainable and growing at 3-4%/yr
# BULL  — Smoke-free second act: NJOY achieves meaningful US oral nicotine
#         share (10-15%), On! nicotine pouches grow to $1B+ revenue, FDA
#         menthol ban permanently blocked; adj EPS $5.80+ × 12×; stock
#         re-rates as smoke-free transition credibility established
# XBULL — Regulatory clarity + smoke-free scale: FDA provides durable
#         authorization framework; Altria's smoke-free portfolio generates
#         $3B+ revenue; buybacks funded by cigarette FCF; adj EPS $7+
BEAR           = 35.0
BASE           = 52.0
BULL           = 70.0
XBULL          = 88.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: menthol ban implemented + illicit trade acceleration + pricing
# power erosion; still earns ~$3.50 on the Marlboro franchise even impaired —
# the brand and distribution infrastructure retain value in any scenario
# PE_TROUGH: 9× reflects a business with a confirmed terminal trajectory;
# tobacco at genuine distress trades 8-10×; 9× is the honest floor
EPS_TROUGH     = 3.50
PE_TROUGH      = 9.0
EPP            = EPS_TROUGH * PE_TROUGH    # $31.50

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E adj EPS ~$5.00 × 10× conservative multiple + $4.08 div
PE_CONSERVATIVE  = 10.0
EPS_FY2026E      = 5.00
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV  # $54.08

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
    ("marlboro_43pct_us_share_pricing_power_and_revenue_per_stick_growth",           4.0, 0.25),
    ("dividend_yield_7_to_9pct_and_55yr_consecutive_growth_income_floor",            3.5, 0.20),
    ("njoy_on_oral_nicotine_smoke_free_portfolio_pivot_and_fda_authorization",       3.0, 0.18),
    ("fda_menthol_flavor_ban_regulatory_risk_and_litigation_timeline_uncertainty",   2.0, 0.20),
    ("structural_cigarette_volume_decline_5_to_7pct_per_year_and_illicit_trade",     2.0, 0.17),
]

# ── Structural Competitive Advantage (SCA) factors ─────────────────────────────
SCA_FACTORS = {
    "marlboro_43pct_us_market_share_held_5_decades_strongest_brand_loyalty_in_staples": +0.20,
    "pricing_power_8_to_10pct_annual_increases_absorbed_with_minimal_volume_loss":      +0.16,
    "55yr_dividend_growth_streak_and_7_to_9pct_yield_income_investor_demand_floor":     +0.10,
    "njoy_fda_authorized_e_vapor_and_on_nicotine_pouch_stake_smoke_free_optionality":   +0.08,
    "structural_cigarette_volume_decline_5_to_7pct_per_year_irreversible_trajectory":   -0.16,
    "fda_menthol_ban_risk_35pct_of_us_volume_and_regulatory_environment_uncertainty":   -0.12,
    "illicit_trade_and_counterfeit_product_capturing_legitimate_market_share":          -0.08,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.18

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"MO ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.2f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE CIGARETTE ROYALTY THAT HAS OUTLIVED EVERY DEATH NOTICE: Altria owns Marlboro — ~43% "
    "of the US cigarette market held for five decades through every anti-tobacco campaign, tax "
    "increase, and regulatory threat. The business model is deliberately simple: volume declines "
    "5-7%/yr, price rises 8-10%/yr, net revenue grows 2-4%, and the extraordinary FCF funds a "
    "dividend grown for 55 consecutive years (~7.8% yield at current price). "
    "MARLBORO LOYALTY IS THE MOAT: the adult smoker who has used the same brand since 18 is "
    "not switching for $0.50/pack savings — brand loyalty in tobacco is the highest in all of "
    "consumer staples; Altria has demonstrated pricing power through every recession, every "
    "excise tax increase, and every competitive launch for 50+ years. "
    "THE SMOKE-FREE PIVOT IS REAL BUT EARLY: NJOY (FDA-authorized e-vapor, acquired 2023) and "
    "the On! nicotine pouch stake give Altria exposure to the fastest-growing nicotine categories; "
    "neither is yet at sufficient scale to replace cigarette earnings, but they represent the "
    "option value on a second act — the same 'Circle the Customer' retention logic that built "
    "Marlboro can potentially be applied to non-combustible nicotine if execution is disciplined. "
    "THE HONEST RISK: this is a terminal business on a long glide path — cigarette volumes will "
    "decline to zero eventually, the question is the time horizon and the FCF extracted before "
    "that point; the FDA menthol ban (35% of US volume, pending/litigated) is the acute "
    "regulatory risk that could compress the timeline and impair the dividend; illicit trade "
    "from counterfeit and cross-border smuggling is growing and eating legitimate share; GLP-1 "
    "drugs may accelerate quitting rates among obese smokers who are also higher-consumption users. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — "
    "modest upside; the 7.8% dividend yield does the heavy lifting on total return. "
    "Accumulate for the yield; size appropriately for a terminal business with regulatory tail. "
    f"Add on FDA-fear selloffs toward $42-45 where total yield exceeds 9%. "
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
    print("  • This is a terminal business — cigarette volumes will decline")
    print("    to zero eventually; the question is whether the smoke-free")
    print("    portfolio (NJOY, On!) builds sufficient scale before the")
    print("    cigarette annuity becomes genuinely impaired; at current NJOY")
    print("    and On! scale, Altria is not yet a smoke-free company with a")
    print("    cigarette tail — it is a cigarette company with smoke-free")
    print("    options, and that distinction matters for terminal value")
    print("  • The FDA menthol ban is the acute binary risk: menthol is ~35%")
    print("    of US cigarette volume and a disproportionate share of Marlboro")
    print("    premium volume; a successful ban would compress earnings more")
    print("    quickly than the base case volume decline trajectory and could")
    print("    force a dividend cut — ending the 55-year growth streak")
    print("  • WCS of 2.98 is the lowest in the model universe — reflects")
    print("    genuine uncertainty about whether the smoke-free pivot succeeds")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The 7.8% dividend yield on a 55-year growth streak is a real")
    print("    return floor: Altria generates $7B+ in FCF annually to fund a")
    print("    $4.08/sh dividend on 1.72B shares ($7.0B total) — the coverage")
    print("    is real and the streak demonstrates management commitment to")
    print("    income investors through multiple regulatory crises")
    print("  • Marlboro pricing power is empirically demonstrated and durable:")
    print("    50 years of price increases absorbing volume declines is not a")
    print("    theory — it is the observed outcome through oil shocks, recessions,")
    print("    excise tax doubling, health warnings, plain packaging pushes, and")
    print("    e-cigarette disruption; the loyalty is genuinely exceptional")
    print("  • The regulatory risk is largely known and partially priced: MO")
    print("    has traded at 9-12× for a decade precisely because the market")
    print("    already discounts the terminal trajectory — you are buying the")
    print("    yield on a discounted price, not paying full price for growth")
    print("  • Ratio B 0.94× — 32.7% downside / 34.6% upside — modestly")
    print("    asymmetric; the dividend yield provides a real return floor")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Altria is a 55-year cash machine selling an addictive product")
    print("  with the best brand loyalty in consumer staples. The business")
    print("  is on a confirmed terminal trajectory — cigarettes will keep")
    print("  declining — but the FCF generation funds a ~7.8% yield while")
    print("  the smoke-free pivot (NJOY, On!) attempts a second act. At $52,")
    print("  you are paid to wait: accumulate for the yield, size for the")
    print("  terminal risk, and add aggressively on FDA-fear selloffs where")
    print("  the yield exceeds 9%. This is not a forever holding — it is a")
    print("  disciplined yield harvest with a defined expiration date that")
    print("  is further away than the bears believe.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
