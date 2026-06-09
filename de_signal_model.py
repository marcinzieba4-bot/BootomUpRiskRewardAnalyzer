"""
Deere & Company (NYSE: DE) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.88×  |  EPP Gap: +102.0%
=======================================================================
THE WORLD'S MOST ADVANCED AGRICULTURAL TECHNOLOGY PLATFORM IN A CYCLICAL
DOWNTURN: Deere is no longer merely an equipment manufacturer — it is the
largest precision agriculture technology company on earth, deploying
autonomous tractors, computer-vision crop spraying (See & Spray: 77%
herbicide reduction), and a connected farm operations platform across
400M+ acres. The ag cycle has created a genuine entry point; the
precision ag software layer is the bull case the cycle obscures.
"""

# ── Model identity ────────────────────────────────────────────────────────────
TICKER         = "DE"
COMPANY        = "Deere & Company"
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Agricultural & Construction Equipment · Precision Agriculture Technology · John Deere Financial · NYSE: DE"
SECTOR_GROUP   = "Industrials"

# ── Price & share data ────────────────────────────────────────────────────────
CURRENT_PRICE  = 400.00          # USD — mid-2026; well off ~$470 2023 peak, ag cycle downturn
ANNUAL_DIV     = 7.00            # USD/yr (~1.75% yield); 25+ consecutive years of dividend growth
SHARES_OUT_B   = 0.278           # billions (aggressive buybacks: from 0.39B in 2015)

FW52_HIGH      = 460.00
FW52_LOW       = 330.00

# ── Scenario prices ───────────────────────────────────────────────────────────
# BEAR  — ag cycle extends through 2027-2028: corn/soy prices stay depressed,
#         farm income compressed further, used equipment inventory clears slowly,
#         industry volumes -25-30% from peak for a third consecutive year;
#         construction & forestry also soft; stock re-rates to trough multiple
# BASE  — cycle troughs late 2026, gradual recovery into 2027: North America
#         large-ag stabilizes, precision ag maintains pricing power, dealer
#         inventories normalize; market prices recovery EPS ~$21-23 at 17-18×
# BULL  — cycle recovery + precision ag monetization: See & Spray, autonomy,
#         and JD Operations Center begin generating meaningful SaaS-like revenue
#         ($1B+ recurring) → re-rate toward software-influenced multiple;
#         construction benefits from infrastructure spending
# XBULL — full recovery + autonomous tractor / precision ag re-rating: market
#         values the recurring precision ag revenue stream at SaaS multiples;
#         buyback-shrunken share count amplifies per-share EPS recovery
BEAR           = 285.0
BASE           = 400.0
BULL           = 530.0
XBULL          = 645.0

# ── Earnings Power Price (EPP) floor ──────────────────────────────────────────
# EPS_TROUGH: Deere at the genuine bottom of the ag equipment cycle —
# ~$16.50/sh reflects a severe demand contraction (but not 2009-scale crisis)
# given the structural precision-ag revenue floor and financial services
# PE_TROUGH: 12× is the cyclical equipment trough multiple (2009: ~11-12×)
EPS_TROUGH     = 16.50
PE_TROUGH      = 12.0
EPP            = EPS_TROUGH * PE_TROUGH     # $198.00

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E EPS ~$21 (near-trough, stabilizing) × 16× conservative mid-cycle
# multiple → reflects genuine risk that the market stays at trough multiples
# even as earnings begin recovering
PE_CONSERVATIVE  = 16.0
EPS_FY2026E      = 21.00
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $343.00

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

# ── Bottom-up signal factors ───────────────────────────────────────────────────
# (name, conviction 1-5, weight)
SIGNALS = [
    ("precision_agriculture_technology_leadership_and_software_moat",      4.0, 0.22),
    ("agricultural_equipment_cycle_depth_duration_and_recovery_timing",    2.0, 0.20),
    ("john_deere_brand_pricing_power_and_customer_switching_costs",        3.5, 0.17),
    ("global_dealer_network_parts_aftermarket_and_installed_base_annuity", 3.5, 0.16),
    ("construction_forestry_and_infrastructure_spending_exposure",         2.5, 0.14),
    ("john_deere_financial_credit_quality_and_cycle_risk",                 2.5, 0.11),
]

# ── Structural Competitive Advantage (SCA) factors ────────────────────────────
SCA_FACTORS = {
    "precision_ag_autonomy_see_and_spray_and_operations_center_platform":    +0.22,
    "global_dealer_network_parts_aftermarket_and_deep_customer_lock_in":     +0.14,
    "john_deere_brand_and_multi_decade_pricing_power_across_cycles":         +0.12,
    "buyback_compounding_share_count_down_29_pct_since_2015":                +0.08,
    "agricultural_commodity_cycle_and_farm_income_compression_risk":         -0.18,
    "used_equipment_inventory_overhang_and_dealer_channel_clearing_lag":     -0.10,
    "competition_cnh_agco_and_potential_precision_ag_feature_commoditization": -0.08,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.20

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"DE ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE WORLD'S MOST ADVANCED AGRICULTURAL TECHNOLOGY PLATFORM IN A CYCLICAL DOWNTURN: "
    "Deere is no longer merely an equipment manufacturer — it is the largest precision "
    "agriculture technology company on earth, deploying autonomous tractors, computer-vision "
    "crop spraying (See & Spray: 77% herbicide reduction vs. broadcast), and a connected farm "
    "operations platform (John Deere Operations Center) across 400M+ acres. "
    "THE FRANCHISE IS EXCEPTIONAL: John Deere brand commands 10-15% pricing premiums vs. "
    "peers that have persisted for decades; ~19,000 global dealer touchpoints create a "
    "service/parts annuity that generates cash through every equipment downcycle; "
    "share count down 29% since 2015 (~0.39B → 0.278B) via disciplined buybacks — "
    "every recovery in EPS is amplified on a meaningfully smaller share count. "
    "THE PRECISION AG BULL CASE: See & Spray (computer vision identifies individual weeds, "
    "applies herbicide only where needed — 77% reduction in chemical use = ROI in <2 seasons); "
    "AutoPath autonomous guidance + self-driving tractor (fully autonomous 8R, no operator); "
    "JD Operations Center SaaS-like platform with fleet telematics, yield mapping, agronomic "
    "recommendations — a data moat deepening with every connected machine hour. "
    "THE HONEST RISK: the ag equipment cycle is in a genuine multi-year downturn — "
    "FY2025 guidance cut multiple times; large-ag North America volumes -20-25% from "
    "peak; used equipment values remain soft creating dealer inventory headwinds; "
    "farm income compressed as corn/soy prices normalized from post-Ukraine-war highs; "
    "John Deere Financial credit portfolio bears watching in a prolonged downcycle. "
    f"Conservative 2yr: FY2026E EPS ${EPS_FY2026E:.0f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.0f} div = ${CONSERVATIVE_PRICE:.0f} → {CONS_RETURN:.1f}% — "
    "BULL/XBULL require cycle recovery AND precision ag re-rate. "
    "A WORLD-CLASS FRANCHISE AT A CYCLICALLY ATTRACTIVE ENTRY: accumulate steadily, "
    "add more aggressively on any further downturn toward $330-355 where Ratio B "
    f"approaches ◉ BUY territory. Bear ${BEAR:.0f} · Base ${BASE:.0f} · "
    f"Bull ${BULL:.0f} · XBull ${XBULL:.0f}."
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
    print(f"  Conservative Price ({EPS_FY2026E:.0f} × {PE_CONSERVATIVE:.0f}×):           ${CONSERVATIVE_PRICE:>8.2f}  ({CONS_RETURN:>+.1f}%)")
    print()
    print(f"  Weighted Conviction Score:                         {WCS:>8.2f} / 5.0")
    print(f"  SCA Net:                                           {SCA_NET:>+8.2f}")
    print(f"  EV(model): ${EV_MODEL:>8.2f}   Upside: {(EV_MODEL-CURRENT_PRICE)/CURRENT_PRICE*100:>+.1f}%   Downside: -{DOWNSIDE_PCT*100:.1f}%")
    print()
    print(f"  SIGNAL:  {SIGNAL}   Ratio B: {RATIO_B:.2f}×   EPP Gap: {EPP_GAP_PCT:>+.1f}%")
    print(f"{'='*72}")
    print()

    print("  BOTTOM-UP SIGNAL FACTORS")
    print(f"  {'Factor':<62} {'Conv':>4}  {'Wt':>5}")
    print(f"  {'-'*72}")
    for name, conv, wt in SIGNALS:
        print(f"  {name:<62} {conv:>4.1f}  {wt:>5.0%}")
    print()

    print("  STRUCTURAL COMPETITIVE ADVANTAGE FACTORS")
    for k, v in SCA_FACTORS.items():
        print(f"  {k:<67} {v:>+.2f}")
    print(f"  {'SCA NET':<67} {SCA_NET:>+.2f}")
    print()

    print(f"{'='*72}")
    print()
    print("  WHY THIS IS AN ◎ ACCUMULATE, NOT A ◌ WATCHLIST OR ◉ BUY")
    print()
    print("  NOT ◉ BUY because:")
    print("  • The ag cycle downturn has not conclusively troughed: dealer inventories")
    print("    of used large-ag equipment remain elevated, compress new-unit pricing,")
    print("    and create a feedback loop where farmers defer purchases as used")
    print("    alternatives are cheap — this can persist 1-2 more years")
    print("  • Conservative 2yr floor (-14.3%) is genuinely below current price —")
    print("    a trough-multiple on trough EPS implies real downside if the cycle")
    print("    extends; this is a cyclical, and cyclicals can overshoot to the downside")
    print("  • At ~19× FY2026E EPS of ~$21, the stock is not priced at trough multiples;")
    print("    it is pricing in recovery — if recovery is delayed, the multiple")
    print("    compresses at the same time earnings miss estimates")
    print("  • John Deere Financial: $48B+ loan portfolio backed by depreciating")
    print("    collateral (used equipment values soft); extended cycle could produce")
    print("    credit losses in a segment investors discount in good times")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The precision agriculture technology moat is deepening through the")
    print("    downcycle, not eroding: See & Spray generates measurable ROI for farmers")
    print("    (77% herbicide cost reduction) that is cycle-agnostic; autonomous tractor")
    print("    capability reduces labor dependency — both are structural, not cyclical")
    print("  • Share count down 29% since 2015: every dollar of EPS recovery in the")
    print("    upcycle lands on 29% fewer shares; a stock that earns $30/sh in 2028")
    print("    on a 0.278B share count was earning $25/sh on 0.39B shares — the")
    print("    compounding math is structurally attractive")
    print("  • John Deere dealer network is not replicable: ~19,000 touchpoints, parts")
    print("    availability within hours globally, and the fact that a broken tractor")
    print("    at harvest costs $30,000/day in lost income creates inelastic demand for")
    print("    service and OEM parts regardless of equipment cycle")
    print("  • Ratio B 0.88× — downside 28.8% / upside 32.5% — is genuinely")
    print("    asymmetric; the cycle creates the discount, the franchise creates the floor")
    print("  • 25+ years of consecutive dividend increases; $7/yr (~1.75% yield) paid")
    print("    and grown through 2008-09 and 2015-16 downturns — management credibly")
    print("    committed to returning capital even through full ag cycles")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Deere is the only agricultural equipment company that has successfully")
    print("  transitioned from metal-bending to technology-enabling at scale. The")
    print("  autonomous 8R tractor, See & Spray, and the Operations Center platform")
    print("  represent a genuine software moat layered onto an already-dominant global")
    print("  equipment franchise — one that 150 years of the John Deere brand, 19,000")
    print("  dealer touchpoints, and a buyback-shrunken share count protect at the")
    print("  bottom. The ag cycle will turn; it always does. When it does, Deere will")
    print("  earn $28-35/sh on 0.26B shares and the precision ag narrative will re-rate")
    print("  the multiple toward 20-22×. At $400 — 28.8% from bear, 32.5% from bull —")
    print("  accumulate steadily. Add aggressively at $330-355.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
