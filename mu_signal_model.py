"""
Micron Technology Inc. (NASDAQ: MU) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.88×  |  EPP Gap: +285.7%
=======================================================================
THE MEMORY CYCLICAL THAT BECAME AN AI INFRASTRUCTURE PLAY: Micron is
the only US-headquartered DRAM and NAND memory manufacturer — one of
three companies on earth (Samsung, SK Hynix, Micron) with the scale
and technology to produce leading-edge DRAM at volume. For most of its
history, Micron was the pure expression of commodity cyclicality: DRAM
pricing collapsed 60-80% in downturns, earnings went deeply negative
(adj EPS -$5.36 in FY2023), and the stock oscillated between 0.5× and
2.5× book value based on where the industry was in the supply/demand
cycle. HBM (High Bandwidth Memory) is changing this. HBM is the memory
architecture that sits between the GPU die and DRAM in AI accelerators
like NVIDIA's H100/H200/B200 — and it is not a commodity. HBM requires
extreme manufacturing precision (stacking 12+ DRAM dies with through-
silicon vias), is supplied under negotiated long-term agreements with
hyperscalers and NVIDIA, and commands 5-8× the ASP of standard DRAM.
SK Hynix is the current HBM leader supplying NVIDIA's highest-end chips;
Micron is ramping HBM3E aggressively and has qualified for Nvidia supply.
The strategic question: does HBM transform Micron from a commodity
cyclical into a partially-differentiated AI infrastructure supplier?
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "MU"
COMPANY        = "Micron Technology Inc."
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Technology · DRAM & NAND Memory / HBM AI Accelerator Memory / Data Center Storage · NASDAQ: MU"
SECTOR_GROUP   = "Technology"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 108.00          # USD — mid-2026; mid-cycle with HBM ramp in progress
ANNUAL_DIV     = 0.46            # USD/yr (~0.4% yield); capital return primarily buybacks
SHARES_OUT_B   = 1.11            # billions

FW52_HIGH      = 135.00
FW52_LOW       = 78.00

# ── Scenario prices ───────────────────────────────────────────────────────────
# BEAR  — memory cycle peaks and rolls over: PC/mobile DRAM oversupply
#         re-emerges as Samsung restarts aggressive capacity additions;
#         AI capex cycle pauses as hyperscalers digest infrastructure build;
#         HBM pricing compresses as SK Hynix and Samsung ramp capacity;
#         China export restriction expansion cuts Micron's China revenue
#         (~10% of sales); EPS turns negative again; stock approaches book
# BASE  — HBM ramp sustains: AI data center DRAM demand keeps utilization
#         high; Micron's HBM3E qualifies for NVIDIA B200/B300 supply;
#         NAND pricing recovers; adj EPS $9.00 × 12× + div → ~$108
# BULL  — HBM leadership narrows: Micron closes the gap with SK Hynix in
#         HBM capacity and quality; AI infrastructure spending sustains at
#         $200B+/yr; CHIPS Act fabs come online improving cost structure;
#         adj EPS $14+ × 13-14×; structural re-rating from commodity to
#         AI infrastructure supplier
# XBULL — memory becomes geopolitically strategic: US government actively
#         supports Micron as the only domestic DRAM supplier; HBM3E/HBM4
#         qualification across all major AI chip suppliers; adj EPS $18+ by 2028
BEAR           = 58.0
BASE           = 108.0
BULL           = 165.0
XBULL          = 215.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# NOTE: EPP framework is imperfect for deep cyclicals — Micron had adj EPS
# of -$5.36 in FY2023. The floor used here assumes HBM mix prevents a full
# commodity collapse; trough reflects a moderate cycle down with HBM providing
# a floor, not the FY2023-style structural bust scenario.
# EPS_TROUGH: moderate cycle down; HBM long-term agreements provide partial
# floor; data center DRAM does not collapse with commodity DRAM
# PE_TROUGH: 14× on trough — cyclicals often trade near book value at trough
# (~$50/sh); this floor is consistent with 0.5-0.6× book historical trough
EPS_TROUGH     = 2.00
PE_TROUGH      = 14.0
EPP            = EPS_TROUGH * PE_TROUGH    # $28.00

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E adj EPS ~$9.00 × 12× conservative cycle multiple + $0.46 div
# 12× reflects mid-cycle memory, not peak; conservative assumes no premium
PE_CONSERVATIVE  = 12.0
EPS_FY2026E      = 9.00
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV  # $108.46

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
    ("hbm3e_ramp_nvidia_qualification_and_ai_accelerator_memory_structural_demand",    4.0, 0.25),
    ("dram_three_supplier_oligopoly_rational_pricing_and_capacity_discipline",         3.5, 0.20),
    ("chips_act_us_manufacturing_strategic_positioning_and_government_support",        3.0, 0.15),
    ("memory_commodity_cycle_volatility_negative_eps_in_downturns_boom_bust_pattern",  2.0, 0.22),
    ("sk_hynix_hbm_leadership_gap_china_export_restrictions_geopolitical_risk",        2.0, 0.18),
]

# ── Structural Competitive Advantage (SCA) factors ─────────────────────────────
SCA_FACTORS = {
    "hbm_5_to_8x_asp_premium_and_long_term_supply_agreements_with_hyperscalers":       +0.16,
    "dram_oligopoly_only_3_suppliers_with_leading_edge_process_technology":            +0.14,
    "only_us_headquartered_dram_manufacturer_chips_act_and_geopolitical_tailwind":     +0.10,
    "memory_commodity_cycle_severe_downturns_negative_eps_destroys_equity_value":      -0.16,
    "sk_hynix_hbm_technology_leadership_and_entrenched_nvidia_supply_relationship":    -0.12,
    "china_export_restriction_risk_and_potential_expansion_to_broader_china_revenue":  -0.10,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.02

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"MU ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap — EPP framework limited for deep cyclicals; trough assumes "
    f"HBM floor; FY2023 actual adj EPS was -$5.36) | "
    "THE MEMORY CYCLICAL THAT BECAME AN AI INFRASTRUCTURE PLAY: Micron is the only US-"
    "headquartered DRAM and NAND manufacturer — one of three companies on earth (Samsung, "
    "SK Hynix, Micron) with the scale to produce leading-edge DRAM at volume. HBM is changing "
    "the business: High Bandwidth Memory for AI accelerators (NVIDIA H100/H200/B200) is not a "
    "commodity — it requires stacking 12+ DRAM dies with through-silicon vias, is priced at "
    "5-8× standard DRAM ASP, and is supplied under negotiated long-term agreements. Micron's "
    "HBM3E is qualifying for NVIDIA supply, closing the gap with SK Hynix. "
    "THE OLIGOPOLY FLOOR IS REAL: three suppliers (Samsung, SK Hynix, Micron) with hundreds "
    "of billions in fab investment create a structural capacity discipline that commodity "
    "markets with 10+ suppliers cannot achieve — rational pricing in the medium term is "
    "more achievable than in prior memory cycles. "
    "CHIPS ACT STRATEGIC POSITIONING: Micron is investing $40B+ in US fabs (Idaho HBM, "
    "New York NAND) backed by CHIPS Act grants — the geopolitical value of domestic US "
    "memory production is rising as semiconductor supply chains become strategic. "
    "THE HONEST RISK: memory remains deeply cyclical — Micron had adj EPS of -$5.36 in "
    "FY2023 and the stock fell to $50; if AI capex cycles peak and Samsung restarts "
    "aggressive DRAM capacity additions, pricing collapses; SK Hynix's HBM technology lead "
    "is real and entrenched at NVIDIA; China export restrictions (10%+ of revenue) could "
    "expand; EPP framework is imperfect here — the 'floor' in a genuine bust is near book "
    "value (~$50), not EPP. SCA_NET = +0.02: HBM premium barely offsets commodity cyclicality. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — essentially "
    "flat mid-cycle; position sizing must account for potential -46% bear scenario. "
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
    print(f"  EPS Trough:                         ${EPS_TROUGH:>8.2f}  (FY2023 actual: -$5.36)")
    print(f"  PE Trough:                                         {PE_TROUGH:>8.1f}×")
    print(f"  EPP (Earnings Power Price):                        ${EPP:>8.2f}  (limited for deep cyclicals)")
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
    print("  • Memory remains deeply cyclical and the downside is -46%:")
    print("    the bear case at $58 is not hypothetical — Micron traded at")
    print("    $50-60 in mid-2024 and at $50 in 2022; these are not tail")
    print("    events, they are recurring outcomes in a commodity cycle with")
    print("    long lead times, lumpy capacity additions, and no pricing power")
    print("    when supply exceeds demand by even a few percent")
    print("  • SK Hynix's HBM technology lead is real: SK Hynix supplies the")
    print("    bulk of NVIDIA's HBM for H100/H200/B200; Micron is qualifying")
    print("    for supply but is not yet the preferred vendor; if NVIDIA's AI")
    print("    GPU roadmap continues to demand SK Hynix-quality HBM for the")
    print("    highest-margin products, Micron remains in a secondary position")
    print("    in the most valuable segment of its addressable market")
    print("  • Conservative 2yr essentially flat (+0.4%): position sizing must")
    print("    account for the wide asymmetry and genuine negative EPS scenario")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • HBM is structurally different from commodity DRAM: 5-8× ASP")
    print("    premium, long-term supply agreements, and limited supplier count")
    print("    (only Samsung, SK Hynix, Micron can produce it at scale) means")
    print("    HBM revenue is not subject to the same spot-pricing collapse")
    print("    as standard DRAM; as AI infrastructure capex persists, HBM")
    print("    grows as a share of Micron's revenue and provides a structural")
    print("    earnings floor that prior cycles lacked")
    print("  • The oligopoly is getting more rational: post-2022 bust, all")
    print("    three DRAM suppliers have demonstrated more capacity discipline;")
    print("    Samsung's 2024 leadership change reinforced pricing rationality;")
    print("    three-supplier markets with $30B+ fab barriers to entry tend")
    print("    toward rational pricing over time")
    print("  • Geopolitical value is rising: Micron is the only US DRAM maker;")
    print("    CHIPS Act grants, DoD interest in domestic memory supply chains,")
    print("    and Taiwan risk in TSMC/SK Hynix supply chains make Micron's US")
    print("    manufacturing a strategic asset with government-supported floor")
    print("  • Ratio B 0.88× — 46.3% downside / 52.8% upside — is genuinely")
    print("    asymmetric; the wide absolute ranges reflect cyclical reality")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Micron is a cyclical commodity business being partially transformed")
    print("  by HBM — the AI accelerator memory that commands 5-8× standard")
    print("  DRAM pricing and is supplied under long-term agreements. At $108,")
    print("  you are buying a mid-cycle DRAM price with HBM ramp optionality,")
    print("  protected by a three-supplier oligopoly and CHIPS Act geopolitical")
    print("  tailwinds. SCA_NET = +0.02: the HBM premium and oligopoly barely")
    print("  offset the commodity cycle and China risks. Size for the -46%")
    print("  bear case being a real recurring outcome, not a tail event.")
    print("  Add aggressively if the stock approaches $72-82 on a cycle")
    print("  downturn — that is where Ratio B approaches ◉ BUY territory.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
