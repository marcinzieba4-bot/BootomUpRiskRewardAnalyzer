"""
Philip Morris International Inc. (NYSE: PM) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.91×  |  EPP Gap: +202.0%
=======================================================================
THE TOBACCO COMPANY THAT IS BECOMING A CONSUMER TECHNOLOGY COMPANY:
Philip Morris International is executing the most ambitious product
transition in consumer staples history — replacing combustible cigarettes
with smoke-free alternatives that are demonstrably better for adult nicotine
users and provably better for PM's economics. IQOS (heated tobacco, FDA
Modified Risk Tobacco Product authorization) has taken 30%+ market share in
Japan, 25%+ in Italy, and is growing in 70+ markets. ZYN (nicotine pouches,
Swedish Match acquisition 2022) is growing 40%+/yr in the US with an FDA
marketing authorization. Smoke-free products now exceed 50% of PM net
revenue — a milestone no tobacco company has reached before. The thesis is
not about cigarettes; it is about who owns the world's nicotine delivery
infrastructure as formats evolve.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "PM"
COMPANY        = "Philip Morris International Inc."
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Consumer Staples · Tobacco / Nicotine / Smoke-Free Products / IQOS / ZYN · NYSE: PM"
SECTOR_GROUP   = "Consumer Staples"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 148.00          # USD — mid-2026; re-rating in progress as smoke-free >50% of revenue
ANNUAL_DIV     = 5.40            # USD/yr (~3.6% yield); annual increases since 2008 spin-off
SHARES_OUT_B   = 1.55            # billions

FW52_HIGH      = 162.00
FW52_LOW       = 118.00

# ── Scenario prices ─────────────────────────────────────────────────────────
# BEAR  — regulatory clampdown + transition stalls: FDA restricts IQOS
#         marketing or mandates design changes; WHO Framework Convention
#         signatories tighten heated tobacco regulations globally; ZYN faces
#         youth access crackdown that limits US retail distribution; cigarette
#         volume decline accelerates beyond smoke-free conversion rate;
#         multiple compresses back toward traditional tobacco discount (12-14×)
# BASE  — transition on track: IQOS continues gaining share in Japan/Europe/
#         LatAm; ZYN sustains 30%+/yr growth in US; smoke-free reaches 60%+
#         of revenue by 2027; EPS $7.20 at 20× + $5.40 div → essentially flat
# BULL  — full re-rating to consumer staples: smoke-free >70% of revenue,
#         IQOS regulatory framework stabilizes globally, ZYN becomes the
#         default US nicotine pouch format; multiple re-rates toward 24-26×
#         as ESG-constrained capital re-enters the stock
# XBULL — category ownership: PM is re-rated as a smoke-free consumer
#         technology platform; new nicotine delivery products (inhalable
#         nicotine, next-gen IQOS ILUMA) open new categories; EPS $10+
BEAR           = 108.0
BASE           = 148.0
BULL           = 192.0
XBULL          = 232.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: severe regulatory crackdown + transition stall; residual
# cigarette business + some IQOS/ZYN still earns ~$3.50/sh at true trough
# PE_TROUGH: 14× reflects tobacco discount even under regulatory pressure
EPS_TROUGH     = 3.50
PE_TROUGH      = 14.0
EPP            = EPS_TROUGH * PE_TROUGH     # $49.00

# ── Conservative 2-year price estimate ───────────────────────────────────────
# FY2027E adj EPS ~$7.20 × 20× conservative multiple + $5.40 div
# Conservative case essentially flat (+0.9%) — transition at fair value
PE_CONSERVATIVE  = 20.0
EPS_FY2026E      = 7.20
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $149.40

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
    ("iqos_heated_tobacco_30pct_japan_25pct_italy_fda_mrtp_authorization_70_plus_markets", 4.0, 0.22),
    ("zyn_nicotine_pouches_40pct_annual_growth_fda_authorized_us_market_leadership",       4.0, 0.20),
    ("smoke_free_products_exceeding_50pct_net_revenue_milestone_and_re_rating_thesis",     3.5, 0.18),
    ("nicotine_addiction_economics_pricing_power_and_guaranteed_repeat_purchase",          3.5, 0.15),
    ("180_country_ex_us_geography_no_domestic_us_cigarette_regulatory_risk",              3.0, 0.12),
    ("fda_who_regulatory_risk_iqos_zyn_restrictions_and_youth_access_crackdown",          2.5, 0.13),
]

# ── Structural Competitive Advantage (SCA) factors ───────────────────────────
SCA_FACTORS = {
    "iqos_fda_mrtp_regulatory_moat_only_authorized_heated_tobacco_product_in_us":         +0.18,
    "zyn_first_mover_fda_authorized_nicotine_pouch_40pct_growth_us_market_share":         +0.14,
    "nicotine_addiction_economics_repeat_purchase_certainty_and_annual_pricing_power":    +0.12,
    "180_country_ex_us_distribution_no_domestic_us_cigarette_litigation_risk":            +0.08,
    "regulatory_risk_fda_who_global_frameworks_could_restrict_iqos_zyn_trajectory":      -0.14,
    "cigarette_volume_secular_decline_accelerating_must_outrun_it_with_smoke_free":       -0.08,
    "currency_headwinds_ex_us_revenues_usd_reporting_and_emerging_market_volatility":     -0.06,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.24

# ── Weighted conviction score ─────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ────────────────────────────────────────────────────────────
SUMMARY = (
    f"PM ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE TOBACCO COMPANY BECOMING A CONSUMER TECHNOLOGY COMPANY: PM is executing the "
    "most ambitious product transition in consumer staples history — replacing combustible "
    "cigarettes with smoke-free alternatives. IQOS (heated tobacco, FDA Modified Risk "
    "Tobacco Product authorization) holds 30%+ share in Japan, 25%+ in Italy, growing "
    "in 70+ markets. ZYN (nicotine pouches, Swedish Match 2022) grows 40%+/yr in the US "
    "with FDA marketing authorization. Smoke-free products now exceed 50% of PM net "
    "revenue — a milestone no tobacco company has reached. "
    "THE ECONOMICS ARE SUPERIOR: IQOS sticks (HEETS/TEREA) have ~70%+ gross margins "
    "vs. ~60% for cigarettes; ZYN has effectively no manufacturing cost relative to "
    "price; the smoke-free transition is not a sacrifice — it is a margin upgrade. "
    "The nicotine addiction economics (certainty of repeat purchase, low price "
    "sensitivity) provide pricing power that compounds across both formats. "
    "THE HONEST RISK: the entire thesis depends on regulatory stability; the FDA could "
    "restrict IQOS marketing authorization, mandate device changes, or block ZYN "
    "distribution on youth access grounds; the WHO Framework Convention on Tobacco "
    "Control is the regulatory framework for 180+ countries and its trajectory is "
    "toward restriction, not liberalization; cigarette volumes are declining faster "
    "in some markets than IQOS conversion can offset. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — "
    "essentially flat with 3.6% yield providing total return support. "
    "Accumulate; add on regulatory-fear pullbacks toward "
    f"$118-125 where Ratio B approaches ◉ BUY territory. "
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
    print("  • The regulatory risk is binary and unquantifiable: unlike most")
    print("    regulatory risks that are frictional, FDA withdrawal of IQOS")
    print("    MRTP authorization or WHO-driven global restrictions would be")
    print("    existential to the re-rating thesis — this is not a fine or a")
    print("    tax, it is a potential product ban in key markets; the entire")
    print("    multiple expansion story requires regulatory stability that no")
    print("    model can guarantee")
    print("  • Cigarette volume decline is accelerating: in most markets,")
    print("    cigarette industry volume is declining 4-7%/yr; PM must run")
    print("    its smoke-free conversion faster than cigarette attrition to")
    print("    maintain total volume; in markets where IQOS is not yet at")
    print("    scale, pure volume decline creates earnings pressure before")
    print("    the smoke-free products can offset")
    print("  • ESG exclusion suppresses the multiple: large institutional")
    print("    investors (pension funds, sovereign wealth, ESG-mandated")
    print("    funds) cannot own tobacco; this structurally limits the")
    print("    re-rating upside even if the smoke-free narrative is fully")
    print("    accepted — the buyer pool is constrained by mandate, not")
    print("    by conviction")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • IQOS has proven it works: 30%+ share in Japan (the most")
    print("    demanding test market — sophisticated consumers, regulatory")
    print("    scrutiny, cultural aversion to risk) — is not a pilot, it is")
    print("    a demonstrated product-market fit; 25%+ in Italy, growing in")
    print("    Korea, Eastern Europe, and Gulf states — this is a category")
    print("    transition that is happening, not hypothetical")
    print("  • ZYN is a genuine growth asset: FDA-authorized nicotine pouches")
    print("    growing 40%+/yr with essentially no manufacturing cost are a")
    print("    category-defining product; the US oral tobacco market is")
    print("    migrating from dip/chew to pouches and ZYN holds the #1")
    print("    position with a regulatory moat (FDA authorization) that")
    print("    competitors must spend 3-5 years replicating")
    print("  • The economics of the transition are genuinely superior: IQOS")
    print("    consumables (HEETS/TEREA) generate ~70%+ gross margins with")
    print("    a device attachment that creates switching costs; ZYN has")
    print("    near-zero variable cost relative to retail price; PM is not")
    print("    sacrificing margins to make the transition — it is upgrading")
    print("    them while creating a more defensible product architecture")
    print("  • The 3.6% yield provides income floor: at $148 with $5.40/yr")
    print("    dividend, income investors receive 3.6%/yr while the re-rating")
    print("    thesis plays out; the nicotine addiction economics guarantee")
    print("    the cash flows needed to sustain the dividend")
    print("  • Ratio B 0.91× — 27.0% downside / 29.7% upside — modestly")
    print("    favorable asymmetry; the smoke-free option is the call,")
    print("    the nicotine addiction floor is the put")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Philip Morris is running the most consequential product transition")
    print("  in consumer goods: replacing combustible cigarettes — which kill")
    print("  their consumers — with smoke-free alternatives that are demonstrably")
    print("  better and economically superior. IQOS at 30%+ in Japan and ZYN at")
    print("  40%+ growth in the US are not experiments; they are the future of")
    print("  the nicotine category, and PM owns the infrastructure. At $148 —")
    print("  27.0% from bear, 29.7% from bull — accumulate the transition thesis")
    print("  with a 3.6% yield as insurance. Add on regulatory-fear pullbacks.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
