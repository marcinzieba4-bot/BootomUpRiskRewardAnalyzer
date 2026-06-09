"""
HCA Healthcare Inc. (NYSE: HCA) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.95×  |  EPP Gap: +72.2%
=======================================================================
THE HOSPITAL NETWORK THAT PRINTS CASH AND BUYS ITSELF BACK: HCA is the
largest for-profit hospital operator in the United States — 186 hospitals,
2,000+ ambulatory care sites, and ~$70B in annual revenue. The scale moat
is real: HCA's purchasing power with device makers, pharma suppliers, and
staffing agencies is structurally unavailable to a 10-hospital regional
system. The capital return story is extraordinary — HCA has reduced its
diluted share count by nearly 50% since 2011 through buybacks funded by
consistent free cash flow, meaning each remaining share represents an
ever-growing claim on the same hospital earnings stream. The Sun Belt
concentration (Florida, Texas, Tennessee, the Southeast) is not a
geographic accident — it is a deliberate positioning in the fastest-
growing, youngest-demographic, highest-volume markets in American
healthcare. The ambulatory surgery center buildout converts expensive
inpatient volume to high-margin outpatient procedures, raising returns
while lowering the fixed-cost base per procedure.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "HCA"
COMPANY        = "HCA Healthcare Inc."
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Healthcare · Hospital Systems & Acute Care / Ambulatory Surgery / Health Services · NYSE: HCA"
SECTOR_GROUP   = "Healthcare"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 310.00          # USD — mid-2026
ANNUAL_DIV     = 2.60            # USD/yr (~0.8% yield); buyback-first capital return policy
SHARES_OUT_B   = 0.245           # billions; down ~50% from 2011 through buybacks

FW52_HIGH      = 368.00
FW52_LOW       = 238.00

# ── Scenario prices ───────────────────────────────────────────────────────────
# BEAR  — Medicaid catastrophe: Congressional cuts to Medicaid reimbursement
#         (25-30M enrolled in HCA states) reduce revenue 10-15%; simultaneous
#         labor cost spike (travel nurse shortages, minimum wage legislation);
#         uninsured rate rises as coverage mandate weakens; multiples compress
#         to 11-12× on uncertainty; stock revisits COVID-era trough levels
# BASE  — Steady state: Sun Belt volume growth 2-3%/yr, pricing 3-4%/yr,
#         ambulatory mix shift improves margins; Medicaid status quo holds;
#         adj EPS $23.00 × 14× + div → ~$325; buybacks continue reducing float
# BULL  — Volume acceleration + Medicaid stable: GLP-1-deferred procedures
#         begin flowing through (bariatric, joint replacement, cardiac);
#         AI-driven clinical decision support improves utilization and length-
#         of-stay management; ASC expansion reaches scale; adj EPS $27+
# XBULL — Healthcare consolidation wave: HCA acquires distressed regional
#         systems at attractive prices as non-profits face balance sheet stress;
#         value-based care contracting premium pricing; adj EPS $32+ by 2029
BEAR           = 205.0
BASE           = 310.0
BULL           = 420.0
XBULL          = 520.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: severe Medicaid cuts + labor inflation simultaneously; on a
# ~$70B revenue base a 30-35% earnings decline gets to ~$15/sh — more
# defensible than historical trough (~$12 in 2019 on $51B revenue base)
# PE_TROUGH: 12× reflects for-profit hospital under genuine policy stress;
# consistent with 10-13× range in prior stressed periods (2015-16, 2018)
EPS_TROUGH     = 15.00
PE_TROUGH      = 12.0
EPP            = EPS_TROUGH * PE_TROUGH    # $180.00

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E adj EPS ~$23.00 × 14× conservative multiple + $2.60 div
PE_CONSERVATIVE  = 14.0
EPS_FY2026E      = 23.00
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV  # $324.60

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
    ("scale_purchasing_power_and_186_hospital_network_cost_structure_moat",          3.5, 0.22),
    ("sun_belt_geographic_positioning_high_growth_markets_and_demographic_tailwind", 4.0, 0.20),
    ("ambulatory_surgery_center_expansion_and_outpatient_mix_shift_margin_driver",   3.5, 0.18),
    ("share_buyback_compounding_50_pct_float_reduction_since_2011_per_share_growth", 4.0, 0.17),
    ("medicaid_policy_risk_government_reimbursement_dependence_and_political_cycle", 2.0, 0.13),
    ("labor_cost_inflation_nursing_staffing_and_wage_pressure_structural_headwind",  2.5, 0.10),
]

# ── Structural Competitive Advantage (SCA) factors ─────────────────────────────
SCA_FACTORS = {
    "186_hospitals_2000_plus_sites_purchasing_scale_unavailable_to_regional_peers":    +0.16,
    "sun_belt_florida_texas_tennessee_fastest_demographic_growth_in_us_healthcare":    +0.14,
    "asc_ambulatory_buildout_higher_margin_outpatient_shift_reduces_fixed_cost_base":  +0.10,
    "buyback_discipline_50_pct_float_reduction_since_2011_per_share_earnings_growth":  +0.12,
    "medicaid_reimbursement_policy_risk_25_to_30m_enrolled_in_hca_state_footprint":    -0.16,
    "labor_inflation_structural_nursing_shortage_and_travel_nurse_cost_volatility":    -0.10,
    "uninsured_self_pay_exposure_and_bad_debt_risk_in_economic_downturn":              -0.06,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.20

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"HCA ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap, bear ${BEAR:.0f} is only 14% above EPP floor — thin cushion) | "
    "THE HOSPITAL NETWORK THAT PRINTS CASH AND BUYS ITSELF BACK: HCA is the largest for-profit "
    "hospital operator in the US — 186 hospitals, 2,000+ ambulatory sites, ~$70B revenue. "
    "The scale moat is real: HCA's purchasing power with device makers, pharma suppliers, and "
    "staffing agencies is structurally unavailable to regional peers. THE SUN BELT BET IS A "
    "STRUCTURAL ADVANTAGE: Florida, Texas, Tennessee, and the Southeast are the fastest-growing, "
    "youngest-demographic, highest-volume healthcare markets in America — HCA is not in these "
    "markets by accident, it has invested decades building the dominant network in states where "
    "population is growing fastest. THE BUYBACK MACHINE: HCA has reduced diluted shares by ~50% "
    "since 2011 — each remaining share owns a larger fraction of the same hospital earnings "
    "stream; at $23+ adj EPS and 14× PE the cash generation funds continued float reduction. "
    "THE AMBULATORY SHIFT: HCA's ASC buildout converts expensive inpatient volume to "
    "high-margin outpatient procedures, lowering the fixed-cost base per procedure while "
    "improving margins and patient convenience. "
    "THE HONEST RISK: Medicaid is the existential policy risk — 25-30 million people in HCA's "
    "state footprint are Medicaid-enrolled, and Congressional reimbursement cuts would hit "
    "revenue directly with minimal ability to offset; this is a political risk that cannot be "
    "modeled with precision and is the primary reason HCA trades at 13-15× despite consistent "
    "execution. Labor cost inflation is structural: the nursing shortage worsened post-COVID and "
    "travel nurse rates, while declining from peak, remain elevated; wage competition with "
    "Amazon and retail healthcare (CVS, Walgreens) for clinical support staff is new and "
    "persistent. GLP-1 drugs present both risk (reduced obesity-related procedures long-term) "
    "and opportunity (deferred procedures re-enter the system as patients get healthier). "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — "
    "modest upside on the base; add aggressively on Medicaid-fear selloffs toward $240-255 "
    f"where Ratio B approaches ◉ BUY territory. "
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
    print("  • Medicaid is a permanent overhang that cannot be resolved:")
    print("    25-30M people in HCA's state footprint are Medicaid-enrolled;")
    print("    any Congress can cut reimbursement rates with minimal notice;")
    print("    the political cycle means this risk re-prices the stock every")
    print("    2-4 years regardless of HCA's operational execution quality")
    print("  • Labor cost inflation is structural, not cyclical: the nursing")
    print("    shortage that emerged post-COVID reflects a pipeline problem")
    print("    (nursing school capacity, burn-out attrition) that takes a")
    print("    decade to resolve; travel nurse costs, while below 2022 peak,")
    print("    remain structurally higher than pre-COVID; HCA cannot fully")
    print("    offset wage inflation with pricing given reimbursement constraints")
    print("  • Conservative 2yr return (+4.7%) is thin — essentially fair value")
    print("    on the base case; the bull case requires either Medicaid stability")
    print("    plus volume acceleration, or buybacks compressing the float further")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • Sun Belt demographic positioning is a 20-year tailwind: Florida")
    print("    adds ~1,000 net new residents per day; Texas is the second-most-")
    print("    populated state growing at 2×+ the national rate; the population")
    print("    aging into peak healthcare consumption years is moving to HCA's")
    print("    markets — this is not a bet on HCA's execution, it is a bet on")
    print("    US internal migration and it is already happening")
    print("  • The buyback compounding is genuinely exceptional: HCA has reduced")
    print("    shares outstanding by ~50% since 2011 — a $310 stock today would")
    print("    be ~$155/sh worth of earnings on the 2011 share count; as long as")
    print("    HCA generates $4-5B+ in free cash flow annually (it does), the")
    print("    per-share earnings growth from buybacks alone exceeds most peers'")
    print("    total earnings growth")
    print("  • Scale purchasing is a durable cost advantage: HCA buys more")
    print("    stents, knees, hips, and pharmaceuticals than any other hospital")
    print("    system in the US — suppliers give pricing concessions unavailable")
    print("    to regional competitors, creating a structural cost floor advantage")
    print("  • Ratio B 0.95× — 33.9% downside / 35.5% upside — modestly")
    print("    asymmetric; Medicaid fear selloffs are the entry opportunity")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  HCA is the best-managed for-profit hospital operator in the US,")
    print("  positioned in the fastest-growing healthcare markets in America,")
    print("  with a buyback machine that has halved the share count since 2011.")
    print("  At $310 — 33.9% from bear, 35.5% from bull — you are paying a")
    print("  fair price for a genuinely advantaged business with one legitimate")
    print("  existential risk: government reimbursement policy. That risk is")
    print("  real, it is permanent, and it is why HCA trades at 13-15× instead")
    print("  of 18-20×. But it is also why the stock periodically sells off on")
    print("  Medicaid headlines, creating accumulation opportunities. Accumulate")
    print("  steadily; add aggressively on policy-fear selloffs toward $240-255.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
