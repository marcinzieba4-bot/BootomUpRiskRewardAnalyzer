"""
3M Company (NYSE: MMM) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.96×  |  EPP Gap: +160.4%
=======================================================================
THE SCIENCE-BASED INDUSTRIAL FRANCHISE EMERGING FROM A LITIGATION-DRIVEN
DISCOUNT: 3M's extraordinary portfolio — 50,000+ patents, materials
science across 60 technology platforms, market leadership in abrasives,
adhesives, filtration, and safety — has been fundamentally discounted by
two extraordinary litigation events (PFAS contamination, Combat Arms
earplugs) now substantially resolved. With CEO Bill Brown (ex-L3
Technologies) driving operational discipline and the Solventum healthcare
spinoff creating a cleaner industrial story, the technology franchise is
being repriced as the litigation discount fades.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "MMM"
COMPANY        = "3M Company"
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Diversified Industrials · Materials Science / Safety & Industrial / Transportation & Electronics / Consumer · NYSE: MMM"
SECTOR_GROUP   = "Industrials"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 125.00          # USD — mid-2026; recovering from litigation trough, turnaround in progress
ANNUAL_DIV     = 2.80            # USD/yr (~2.2% yield); reset from $6.00 in 2023 to fund PFAS settlement
SHARES_OUT_B   = 0.554           # billions

FW52_HIGH      = 145.00
FW52_LOW       = 98.00

# ── Scenario prices ───────────────────────────────────────────────────────────
# BEAR  — litigation tail risk re-emerges: new PFAS class actions in Europe
#         or undiscovered domestic claims breach settlement scope; Bill Brown
#         operational turnaround fails to restore organic growth; structural
#         market share losses during litigation distraction prove permanent;
#         dividend cut again; multiple compresses toward distressed industrial
# BASE  — turnaround delivers: PFAS/Combat Arms settlements hold, Brown's
#         operational discipline restores margins toward historical peaks,
#         Safety & Industrial and T&E return to low-single-digit organic
#         growth; market prices $7.50 adj EPS at ~16× + yield support → ~$125
# BULL  — full rehabilitation: litigation discount fully removed, organic
#         growth re-accelerates to 4-5%/yr, margin recovery toward 22-24%+,
#         multiple re-rates toward pre-litigation levels of 18-22×;
#         adj EPS $9-10+ by 2028
# XBULL — 3M renaissance: Brown executes the Danaher-like operational
#         improvement playbook; materials science portfolio re-valued at
#         premium; electronics/semiconductor exposure re-rates on AI capex
BEAR           = 80.0
BASE           = 125.0
BULL           = 172.0
XBULL          = 215.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: new litigation emerges + restructuring costs; still earns
# ~$4.00/sh on the core materials science and safety businesses
# PE_TROUGH: 12× reflects diversified industrial at genuine distress level
EPS_TROUGH     = 4.00
PE_TROUGH      = 12.0
EPP            = EPS_TROUGH * PE_TROUGH     # $48.00

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E adj EPS ~$7.50 × 16× conservative multiple + $2.80 div
# Conservative case essentially flat (-1.8%) — turnaround at fair value
PE_CONSERVATIVE  = 16.0
EPS_FY2026E      = 7.50
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $122.80

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
    ("pfas_and_combat_arms_litigation_resolution_and_residual_tail_risk",         2.5, 0.22),
    ("bill_brown_operational_turnaround_cost_discipline_and_margin_recovery",      3.5, 0.20),
    ("50k_patent_technology_portfolio_and_materials_science_platform_moat",        3.5, 0.18),
    ("safety_industrial_and_transportation_electronics_organic_growth_recovery",   3.0, 0.17),
    ("dividend_reset_capital_allocation_and_balance_sheet_restoration",            3.0, 0.13),
    ("solventum_separation_completion_and_residual_obligations_execution",         2.5, 0.10),
]

# ── Structural Competitive Advantage (SCA) factors ─────────────────────────────
SCA_FACTORS = {
    "50000_plus_patents_and_materials_science_across_60_technology_platforms":       +0.18,
    "safety_industrial_adhesives_abrasives_filtration_entrenched_market_leadership": +0.14,
    "bill_brown_operational_discipline_and_lean_manufacturing_turnaround_credibility": +0.10,
    "pfas_combat_arms_substantially_resolved_removing_existential_uncertainty":      +0.10,
    "residual_pfas_liability_tail_risk_international_and_undiscovered_claims":       -0.18,
    "organic_revenue_decline_and_share_loss_during_litigation_distraction_years":    -0.10,
    "dividend_cut_2023_ended_64yr_streak_and_investor_trust_deficit_to_rebuild":     -0.08,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.16

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"MMM ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE SCIENCE-BASED INDUSTRIAL FRANCHISE EMERGING FROM A LITIGATION-DRIVEN DISCOUNT: "
    "3M's extraordinary portfolio — 50,000+ patents, materials science across 60 technology "
    "platforms, entrenched market leadership in abrasives, adhesives, filtration, and safety "
    "— has been discounted for five years by two extraordinary litigation events now "
    "substantially resolved: PFAS water supplier settlement (~$10.3B, 2023) and Combat Arms "
    "earplug settlement (~$6B, 2023). "
    "THE TECHNOLOGY MOAT IS INTACT: 3M's materials science platform generates ~3,000 new "
    "patents/year across electronics, healthcare, safety, and transportation — the Scotch, "
    "Post-it, Scotchgard, Filtrete, Peltor, and 3M Automotive brands represent franchise "
    "value that litigation could not erode; the Safety & Industrial and Transportation & "
    "Electronics segments serve industrial markets with genuine switching costs and "
    "specification-driven demand. "
    "BILL BROWN IS THE CATALYST: new CEO (May 2024, ex-L3 Technologies) with a proven "
    "operational discipline track record; early actions — organizational simplification, "
    "manufacturing footprint reduction, SG&A rationalization — mirror the L3 playbook; "
    "the margin recovery from trough (~17-18% adj EBIT) toward historical peaks (~22-24%) "
    "represents $500M+ in potential EBIT recovery on a $22B revenue base. "
    "THE HONEST RISK: PFAS is not fully resolved — international litigation (Europe, Canada) "
    "and potentially undiscovered domestic claim categories remain outside the US water "
    "supplier settlement scope; the dividend cut from $6.00 to $2.80/yr (2023) ended 3M's "
    "64-year Dividend King streak and created a trust deficit with income investors that "
    "takes years to rebuild; organic growth recovery is not yet confirmed. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — "
    "essentially flat; BULL/XBULL require margin recovery and litigation discount removal. "
    "Accumulate steadily as turnaround evidence accumulates; add on any PFAS headline-driven "
    f"pullbacks toward $100-108 where Ratio B approaches ◉ BUY territory. "
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
    print("  • PFAS tail risk is not fully resolved: the US water supplier")
    print("    settlement covers domestic public water systems, but European")
    print("    PFAS litigation is nascent and growing; Canada, Australia, and")
    print("    other jurisdictions have not settled; the true total liability")
    print("    universe remains unknown — this is not a cleared runway, it is")
    print("    a substantially reduced but still present existential risk")
    print("  • The dividend cut destroyed 64 years of Dividend King credibility:")
    print("    income investors who owned MMM for the yield are structurally")
    print("    less likely to return; rebuilding the shareholder base on a")
    print("    $2.80/yr dividend takes years and limits the re-rating speed")
    print("  • Organic growth is not yet restored: revenue has declined or")
    print("    stagnated for multiple years during the litigation distraction;")
    print("    market share losses in key categories (especially to Asian")
    print("    abrasive and adhesive competitors) may prove structural, not")
    print("    temporary — Brown must show organic recovery, not just cost cuts")
    print("  • Conservative 2yr floor ($123) is essentially flat — virtually no")
    print("    margin of safety at current levels on an earnings basis")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The materials science moat is genuinely extraordinary: 50,000+")
    print("    patents across 60 technology platforms is not a marketing claim —")
    print("    it is the output of 120 years of compounding R&D investment that")
    print("    produces ~3,000 new patents/year; the Scotch, Post-it, Filtrete,")
    print("    Peltor, and 3M Automotive brands have specification advantages")
    print("    in their markets that took decades to build and cannot be quickly")
    print("    displaced regardless of litigation noise")
    print("  • The PFAS/Combat Arms settlements removed the existential risk:")
    print("    the ~$16B in combined settlements are real cash costs, but they")
    print("    have put a defined dollar figure on what was previously an open-")
    print("    ended unknown; bounded liability is fundamentally different from")
    print("    unbounded liability in terms of equity valuation")
    print("  • Bill Brown has a specific, proven playbook: at L3 Technologies he")
    print("    compressed SG&A from 11% to 8% of revenue, improved EBIT margins")
    print("    400bps, and rebuilt investor confidence in 3 years; the same levers")
    print("    (org simplification, footprint consolidation, pricing discipline)")
    print("    exist at 3M at scale; early evidence (headcount reduction, plant")
    print("    rationalization) suggests execution is on track")
    print("  • At 16× forward earnings with PFAS substantially resolved, MMM is")
    print("    priced as a mediocre industrial, not as the technology platform it is;")
    print("    a re-rate to 19-20× on margin recovery alone gets you to $150+")
    print("  • Ratio B 0.96× — downside 36.0% / upside 37.6% — essentially")
    print("    balanced but modestly asymmetric to the upside; the litigation")
    print("    discount removal is the option, the technology moat is the floor")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  3M is a 120-year-old materials science company that spent five years")
    print("  being priced as a litigation liability rather than a technology asset.")
    print("  The settlements have been painful, real, and expensive — but they were")
    print("  defined, funded, and largely finalized, which converts an open-ended")
    print("  existential risk into a bounded historical cost. Bill Brown's arrival")
    print("  brings an operational discipline that 3M's conglomerate culture")
    print("  historically lacked. At $125 — 36.0% from bear, 37.6% from bull —")
    print("  with 50,000 patents still generating revenue and PFAS no longer an")
    print("  existential unknown, accumulate steadily. This is not a screaming buy;")
    print("  the residual tail risk earns the caution. But the moat is real.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
