"""
United Parcel Service, Inc. (NYSE: UPS) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.96×  |  EPP Gap: +104.9%
=======================================================================
THE GLOBAL PACKAGE DELIVERY DUOPOLY IN A STRATEGIC RESET: UPS is the
world's most profitable package delivery company, executing a painful but
necessary transition from peak Amazon dependency toward a higher-margin
SMB/healthcare/B2B mix. The Teamsters contract creates a fixed cost base
requiring volume leverage; the Amazon insourcing is a genuine structural
headwind. But the UPS network — 125,000+ vehicles, 570+ aircraft, 220+
countries — is not replicable at any price, and a 5.5% dividend yield
compensates shareholders while the reset plays out.
"""

# ── Model identity ────────────────────────────────────────────────────────────
TICKER         = "UPS"
COMPANY        = "United Parcel Service, Inc."
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Transportation · Global Package Delivery / Logistics / Supply Chain Solutions · NYSE: UPS"
SECTOR_GROUP   = "Industrials"

# ── Price & share data ────────────────────────────────────────────────────────
CURRENT_PRICE  = 118.00          # USD — mid-2026; ~40% off 2021-22 peak on structural headwind concerns
ANNUAL_DIV     = 6.52            # USD/yr (~5.5% yield); strong cash generation; dividend maintained
SHARES_OUT_B   = 0.835           # billions (modest buybacks; capital allocation balanced with dividend)

FW52_HIGH      = 145.00
FW52_LOW       = 92.00

# ── Scenario prices ───────────────────────────────────────────────────────────
# BEAR  — structural deterioration: Amazon continues insourcing toward 70%+
#         self-delivery, UPS loses another 5-7% of volume; Teamsters contract
#         cost base prevents margin recovery; pricing power erodes vs. FedEx
#         and regional last-mile entrants; dividend cut accelerates de-rating
# BASE  — strategic reset progresses: SMB/healthcare volume mix improves
#         margins, Amazon volume losses stabilize, international segment steady,
#         cost efficiency program delivers; dividend maintained at ~5.5% yield;
#         market prices ~$7.20 EPS at 14× + yield support → ~$118
# BULL  — mix shift accelerates: UPS Healthcare scales to $20B+ revenue,
#         B2B/SMB pricing power restored, Teamsters contract renegotiation
#         or productivity gains improve cost trajectory; earnings recover
#         toward $10-11/sh; volume leverage drives margin expansion
# XBULL — full strategic transformation: healthcare logistics becomes
#         a premium-multiple segment ($25B+); e-commerce stabilizes;
#         AI route optimization drives structural cost improvements;
#         multiple re-rates toward historical 18-20×
BEAR           = 74.0
BASE           = 118.0
BULL           = 164.0
XBULL          = 200.0

# ── Earnings Power Price (EPP) floor ──────────────────────────────────────────
# EPS_TROUGH: Amazon insourcing + cost base + volume pressure; UPS still
# earns ~$4.80/sh at the genuine trough on network utilization and B2B/intl
# PE_TROUGH: 12× reflects logistics compounder floor (network irreplaceable)
EPS_TROUGH     = 4.80
PE_TROUGH      = 12.0
EPP            = EPS_TROUGH * PE_TROUGH     # $57.60

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E EPS ~$7.20 × 14× conservative logistics multiple + $6.52 div
# Conservative case -9.0% — modest downside; dividend yield (~5.5%) provides
# meaningful support against further de-rating
PE_CONSERVATIVE  = 14.0
EPS_FY2026E      = 7.20
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $107.32

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
# (name, conviction 1-5, weight)
SIGNALS = [
    ("global_package_network_irreplaceability_125k_vehicles_570_aircraft",  3.5, 0.22),
    ("amazon_insourcing_structural_volume_displacement_and_mix_headwind",   1.5, 0.20),
    ("ups_healthcare_marken_cold_chain_and_clinical_trials_growth",         3.5, 0.17),
    ("smb_and_b2b_higher_margin_mix_improvement_and_pricing_power",         3.0, 0.16),
    ("teamsters_2023_contract_fixed_cost_base_and_operating_leverage_risk", 2.0, 0.15),
    ("international_segment_resilience_and_cross_border_trade_exposure",    3.0, 0.10),
]

# ── Structural Competitive Advantage (SCA) factors ─────────────────────────────
SCA_FACTORS = {
    "global_network_125k_vehicles_570_aircraft_220_countries_not_replicable":  +0.20,
    "ups_healthcare_cold_chain_marken_clinical_trials_pharma_distribution":    +0.12,
    "b2b_high_density_route_economics_and_smb_customer_pricing_power":         +0.10,
    "5p5_pct_dividend_yield_and_strong_fcf_generation_supporting_capital_return": +0.08,
    "amazon_logistics_network_self_delivery_insourcing_structural_headwind":   -0.18,
    "teamsters_contract_2023_2028_rigid_cost_base_limiting_margin_flexibility": -0.12,
    "residential_ecommerce_unit_economics_disadvantage_vs_b2b_density":        -0.08,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.12

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"UPS ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE GLOBAL PACKAGE DELIVERY DUOPOLY IN A STRATEGIC RESET: UPS is the world's most "
    "profitable package delivery company, executing a painful but necessary transition from "
    "peak Amazon dependency toward higher-margin SMB/healthcare/B2B volumes. "
    "THE NETWORK IS IRREPLACEABLE: 125,000+ vehicles, 570+ aircraft, 220+ country reach, "
    "next-day and 2-day infrastructure built over 115 years — Amazon has spent $50B+ and "
    "a decade building its own logistics network and still relies on UPS/USPS for a "
    "meaningful share of deliveries; no new entrant could replicate UPS's density economics. "
    "UPS HEALTHCARE IS THE HIDDEN BULL CASE: cold-chain pharmaceutical distribution, "
    "Marken clinical trial logistics (the global leader, serving 19 of top 20 pharma "
    "companies), UPS Healthcare solutions — a $10B+ and growing segment at meaningfully "
    "higher margins than residential parcel, insulated from Amazon competition. "
    "THE HONEST RISK: Amazon insourcing is structural and accelerating — Amazon now "
    "self-delivers ~60%+ of its own packages vs. ~20% in 2018; every point of "
    "further insourcing removes high-density residential volume from UPS while leaving "
    "the fixed cost base intact; the 2023 Teamsters contract (through 2028) locks in "
    "wage/benefit cost increases with limited flexibility regardless of volume; "
    "Carol Tomé's 'Better Not Bigger' strategy cost UPS volume share it is still "
    "working to recover. "
    f"Conservative 2yr: EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}%; "
    "a 5.5% dividend yield provides real return and downside support while the "
    "reset plays out. ACCUMULATE at current levels; this is a ◎ not a ◉ BUY "
    "because the structural headwinds require the healthcare/SMB thesis to execute — "
    "the network floor is real but the earnings recovery is not yet certain. "
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
    print(f"  Conservative Price ({EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}×):        ${CONSERVATIVE_PRICE:>8.2f}  ({CONS_RETURN:>+.1f}%)")
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
        print(f"  {k:<68} {v:>+.2f}")
    print(f"  {'SCA NET':<68} {SCA_NET:>+.2f}")
    print()

    print(f"{'='*72}")
    print()
    print("  WHY THIS IS AN ◎ ACCUMULATE, NOT A ◌ WATCHLIST OR ◉ BUY")
    print()
    print("  NOT ◉ BUY because:")
    print("  • The Amazon insourcing headwind is structural, not cyclical: Amazon")
    print("    has invested $50B+ in its own logistics network and will continue to")
    print("    shift volume in-house; every point of incremental self-delivery removes")
    print("    dense residential volume from UPS while leaving the fixed cost base")
    print("    intact — operating leverage works sharply against UPS in this dynamic")
    print("  • The 2023 Teamsters contract runs through 2028 with meaningful wage/")
    print("    benefit escalation baked in — there is no cost flexibility if volumes")
    print("    disappoint; this is not a lease or supply contract you can renegotiate")
    print("  • Conservative 2yr floor ($107) is -9.0% below current price; the margin")
    print("    of safety is thin even after a ~40% decline from the 2022 peak")
    print("  • The strategic pivot to healthcare/SMB is the right move but takes time:")
    print("    UPS Healthcare is ~$10B revenue vs. $87B total — the mix shift required")
    print("    to materially change the earnings profile is a multi-year, not multi-")
    print("    quarter, journey")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The UPS network is genuinely irreplaceable: 125,000+ ground vehicles,")
    print("    570+ aircraft (one of the world's largest airlines), presence in 220+")
    print("    countries, next-day and 2-day infrastructure built over 115 years —")
    print("    the economics of a national package delivery network are driven by density")
    print("    that takes decades to build, not billions of dollars alone")
    print("  • UPS Healthcare is an underappreciated moat: Marken is the #1 global")
    print("    clinical trials logistics provider (serving 19 of the top 20 pharma")
    print("    companies), cold-chain pharma distribution requires regulatory certifica-")
    print("    tions, specialized facilities, and GDP-compliant handling that Amazon")
    print("    cannot replicate in residential delivery infrastructure")
    print("  • A 5.5% dividend yield on a company with strong FCF generation (~$5-6B)")
    print("    is real cash returning to shareholders today — you are paid to wait")
    print("    for the strategic reset to show up in earnings")
    print("  • B2B density economics are significantly better than residential: a")
    print("    commercial stop delivering 20 packages takes the same time as a")
    print("    residential stop delivering 1; UPS's deliberate shift toward SMB and")
    print("    B2B improves per-stop economics structurally as the Amazon mix fades")
    print("  • Ratio B 0.96× — downside 37.3% / upside 39.0% — is meaningfully")
    print("    asymmetric; the dividend yield compresses the effective downside further")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  UPS is a world-class logistics network being repriced as a structurally")
    print("  impaired business because Amazon — one customer — is building its own")
    print("  delivery capability. The market is right that Amazon insourcing is real")
    print("  and ongoing; it is wrong that UPS's network becomes worthless as a result.")
    print("  Every SMB that ships a package, every pharma company running a clinical")
    print("  trial, every B2B customer receiving a pallet — none of them have an")
    print("  Amazon Logistics option. UPS's healthcare and B2B businesses are growing")
    print("  into the Amazon gap, and a 5.5% yield compensates holders while they do.")
    print("  At $118, accumulate steadily. This is not a screaming buy; it is a")
    print("  mispriced-for-the-wrong-reasons franchise paying you to wait.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
