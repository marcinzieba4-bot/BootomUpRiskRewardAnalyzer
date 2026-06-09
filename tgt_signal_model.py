"""
Target Corporation (NYSE: TGT) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.93×  |  EPP Gap: +46.9%
=======================================================================
THE DISCRETIONARY DEPARTMENT STORE HIDING INSIDE A DISCOUNT RETAILER:
Target is not Walmart. That sentence explains most of Target's last five
years — and most of its opportunity. Where Walmart's ~60% grocery/essentials
mix insulates it from consumer sentiment, Target's ~50% discretionary
exposure (apparel, home, electronics, beauty) means it wins big when
consumers feel flush and loses traffic when they feel squeezed. The core
Target guest — household income $75-100K, college-educated, brand-conscious
but value-oriented, suburban — is the most coveted demographic in American
retail. The store experience, the private label portfolio (50+ owned brands
including Good & Gather, Cat & Jack, All in Motion, Threshold), and the
Drive Up same-day convenience have built genuine loyalty. The problem in
2022-2026 has been external: first an inventory glut miscalculation, then
discretionary softness as the consumer traded down, then political/boycott
headwinds, then tariff exposure on Chinese-sourced discretionary goods.
None of these are permanent structural impairments — the guest, the stores,
and the brands are intact. The question is whether execution and the macro
environment turn at the same time.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "TGT"
COMPANY        = "Target Corporation"
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Consumer Staples · General Merchandise / Discount Retail / Omnichannel · NYSE: TGT"
SECTOR_GROUP   = "Consumer Staples"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 105.00          # USD — mid-2026; multi-year low relative to earnings power
ANNUAL_DIV     = 4.48            # USD/yr (~4.3% yield); 55+ consecutive years of growth
SHARES_OUT_B   = 0.455           # billions; consistent buybacks over cycle

FW52_HIGH      = 130.00
FW52_LOW       = 85.00

# ── Scenario prices ───────────────────────────────────────────────────────────
# BEAR  — structural share loss confirmed: Walmart/Amazon permanently capture
#         the value-seeking Target guest; discretionary recession cuts apparel
#         and home spending by 15-20%; tariff pass-through destroys pricing
#         power on Chinese-sourced goods; boycott headwinds persist; adj EPS
#         drops below $6; multiple compresses to 11-12× on loss-of-relevance fears
# BASE  — stabilization and slow recovery: tariff uncertainty resolves,
#         discretionary sentiment improves with lower rates, Drive Up and
#         Target Circle loyalty programs rebuild traffic; adj EPS $8.50 × 13×
#         + div → ~$115; Dividend King streak intact at 55+ years
# BULL  — guest returns + private label expansion: core $75-100K household
#         income demographic re-engages as consumer sentiment recovers;
#         new private label launches in food/beverage drive basket size;
#         adj EPS $10.50+ × 15×; discount to Walmart multiple narrows
# XBULL — Target reinvention: smaller format urban stores succeed, same-day
#         services become meaningful revenue, brand partnerships (Ulta,
#         Apple, Disney) drive traffic and basket; adj EPS $13+ by 2029
BEAR           = 68.0
BASE           = 105.0
BULL           = 145.0
XBULL          = 182.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: genuine recession + permanent share loss scenario; still earns
# ~$5.50 on 1,950 stores, Drive Up infrastructure, and food/essentials base
# PE_TROUGH: 13× reflects a Dividend King discount retailer at trough —
# not a distressed business, still generating cash, multiple floor is higher
# than a pure discretionary; 55-year dividend streak provides support
EPS_TROUGH     = 5.50
PE_TROUGH      = 13.0
EPP            = EPS_TROUGH * PE_TROUGH    # $71.50

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E adj EPS ~$8.50 × 13× conservative multiple + $4.48 div
PE_CONSERVATIVE  = 13.0
EPS_FY2026E      = 8.50
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV  # $114.98

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
    ("50_plus_owned_brands_private_label_and_guest_loyalty_differentiation",         3.0, 0.22),
    ("drive_up_same_day_services_and_target_circle_100m_member_omnichannel_moat",    3.0, 0.20),
    ("55yr_dividend_king_streak_and_4pct_plus_yield_income_floor_at_current_price",  3.5, 0.18),
    ("walmart_amazon_market_share_pressure_and_discretionary_traffic_headwinds",     2.0, 0.22),
    ("tariff_exposure_discretionary_imports_and_boycott_reputational_overhang",      2.0, 0.18),
]

# ── Structural Competitive Advantage (SCA) factors ─────────────────────────────
SCA_FACTORS = {
    "50_plus_owned_brands_and_75_to_100k_household_income_guest_loyalty":              +0.12,
    "drive_up_same_day_and_target_circle_digital_convenience_infrastructure":          +0.10,
    "1950_store_physical_footprint_and_suburban_location_density_advantage":           +0.08,
    "discretionary_50pct_mix_creates_traffic_volatility_vs_grocery_anchored_peers":   -0.10,
    "walmart_and_amazon_structurally_outcompeting_on_price_and_selection_breadth":    -0.12,
    "tariff_exposure_on_chinese_sourced_discretionary_and_reputational_headwinds":    -0.08,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.00

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"TGT ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.2f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE DISCRETIONARY DEPARTMENT STORE HIDING INSIDE A DISCOUNT RETAILER: Target is not "
    "Walmart — ~50% discretionary mix (apparel, home, electronics, beauty) means Target wins "
    "when consumers feel flush and loses traffic when they feel squeezed. THE CORE GUEST IS "
    "GENUINELY VALUABLE: the $75-100K household income, college-educated, brand-conscious "
    "but value-oriented suburban shopper is the most coveted demographic in American retail — "
    "and Target has built real loyalty through 50+ owned brands (Good & Gather, Cat & Jack, "
    "All in Motion, Threshold), Drive Up same-day convenience, and Target Circle (100M+ members). "
    "THE HEADWINDS OF 2022-2026 ARE REAL BUT NOT STRUCTURAL: inventory miscalculation, "
    "discretionary softness, political/boycott noise, and tariff exposure on Chinese-sourced "
    "goods are all cyclical or manageable headwinds — not permanent competitive impairments; "
    "the stores, the guest, and the private label brands are intact. "
    "THE HONEST RISK: Walmart and Amazon are structurally better positioned on price and "
    "selection — Target's differentiation (style, experience, owned brands) requires the "
    "consumer to value those attributes enough to pay the implied premium; when consumers "
    "trade down, they trade to Walmart, not to Target; the ~4.3% dividend yield at current "
    "price reflects genuine market skepticism about earnings recovery. "
    "SCA_NET = 0.00 — the competitive moats and structural headwinds are in genuine balance; "
    "this is a turnaround story, not a compounding franchise. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — "
    "reasonable upside if earnings stabilize; BULL requires macro improvement and "
    "share recapture from boycott headwinds. Add on further discretionary-fear or "
    f"macro selloffs toward $88-95. "
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
    print("  • SCA_NET = 0.00 — this is the only model in the universe where")
    print("    competitive moats and structural headwinds are in exact balance;")
    print("    there is no clear durable advantage that Walmart and Amazon")
    print("    cannot match or exceed over time; Target's differentiation")
    print("    (style, owned brands, experience) requires the consumer to")
    print("    actively choose to pay a slight premium for it — and when")
    print("    budgets tighten, they don't")
    print("  • The earnings recovery is not yet visible: adj EPS has been")
    print("    declining or flat since the $13.56 peak in FY2022; four years")
    print("    of underperformance vs. the market and vs. Walmart suggests")
    print("    structural, not just cyclical, challenges; the market at ~12×")
    print("    forward earnings is pricing in continued disappointment")
    print("  • Tariff exposure on discretionary imports is real: ~30-35% of")
    print("    Target's general merchandise assortment is China-sourced; the")
    print("    choice between absorbing margin compression or passing costs to")
    print("    the price-sensitive guest is painful in either direction")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The 55-year Dividend King streak at a 4.3% yield is a real")
    print("    return floor: Target has raised its dividend through the 2008")
    print("    crisis, the 2013 data breach, the 2022 inventory disaster, and")
    print("    the 2023-2024 boycott headwinds; the payout ratio at ~$4.48")
    print("    on ~$8.50 EPS is ~53% — covered, growing, and credible")
    print("  • The owned brand portfolio is genuinely differentiated: Good &")
    print("    Gather ($3B+ revenue), Cat & Jack (leading children's apparel),")
    print("    All in Motion (activewear), Threshold (home) — these are not")
    print("    generic private labels; they have design identity and guest")
    print("    loyalty that creates basket stickiness unavailable at Walmart")
    print("  • Drive Up is a structural convenience moat: Target Circle plus")
    print("    Drive Up/Order Pickup creates same-day convenience at a scale")
    print("    that smaller retailers cannot match; 100M+ Circle members")
    print("    represent real behavioral data and promotional effectiveness")
    print("  • At $105 — ~45% below the 2021 high of $190 — the stock is")
    print("    pricing in sustained mediocrity on a business that earned $13.56")
    print("    EPS four years ago; mean reversion to $8.50+ is conservative")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Target is a high-quality retailer that has been through four")
    print("  consecutive years of self-inflicted and external wounds — and it")
    print("  is currently priced as if the damage is permanent. At $105 with")
    print("  a 4.3% dividend yield and a 55-year growth streak, you are paid")
    print("  to wait for earnings to stabilize around $8-9 and the multiple")
    print("  to re-rate from 12× toward 14-16× as evidence accumulates that")
    print("  the core guest has not defected permanently. SCA_NET = 0.00 is")
    print("  the honest assessment: this is a turnaround story, not a")
    print("  compounding franchise — size accordingly and add on further")
    print("  macro or discretionary-fear selloffs toward $88-95.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
