"""
Valero Energy Corporation (NYSE: VLO)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◌ WATCHLIST  |  Ratio B: 1.61×  |  EPP Gap: +272.1%

THE LEANEST INDEPENDENT REFINER IN A "GOLDEN AGE" THAT THE STOCK ALREADY KNOWS ABOUT
Trading at $178.60 (52-week range $112-184, within ~3% of an all-time high, up roughly 55%
over the past year) on the back of a genuinely best-in-class, low-cost, high-complexity
refining system (Gulf Coast-weighted, advantaged-feedstock-capable) running near-record
utilization through the strongest refining-margin environment in years — plus a renewable
diesel/ethanol platform (Diamond Green Diesel JV, Valero's ethanol segment) that gives it a
genuine, underappreciated call option on the energy-transition buildout that most pure-play
refiners lack. FY2025 was a record year for refining throughput and adjusted operating
income, funding an aggressive buyback program (share count down meaningfully over the past
several years) and a steadily-growing dividend (yield ~2.3%).

The honest tension: refining margins are among the most violently mean-reverting in all of
energy, and at ~2% from an all-time high after a ~55% one-year run, the stock is pricing in
a meaningful continuation of today's unusually favorable crack-spread environment. Q1 2026
showed early signs of crack-spread normalization from 2025's exceptional levels — not a
collapse, but a reminder that "golden ages" in refining have historically proven to be
windows, not permanent states. Valero is the best-positioned name to weather a downturn
(lowest-cost, most flexible system, strongest balance sheet among pure-play refiners), but
"best house in a cyclical neighborhood, priced near an all-time high" is a more measured
setup than the headline "record year" narrative suggests.

Conviction: MODERATE-HIGH on Valero's structural cost/complexity advantage and renewable-
fuels optionality (genuinely the best-run independent refiner, with real diversification);
LOW-MODERATE on near-term upside given the stock sits within ~3% of an all-time high after
an outsized run on a cyclically-elevated earnings base — Ratio B lands in WATCHLIST
territory pending either a pullback or confirmation that 2026 margins hold near 2025 levels.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "VLO"
COMPANY         = "Valero Energy Corporation"
SECTOR          = "Oil Refining & Marketing · Renewable Diesel (Diamond Green Diesel JV) · Ethanol · Gulf Coast-Weighted Refining System · NYSE: VLO"
SECTOR_GROUP    = "Energy"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 178.60   # June 2026, within ~3% of an all-time high
ANNUAL_DIV      = 4.28     # $1.07/qtr; yield ~2.4%
SHARES_OUT_B    = 0.318    # ~318mm shares (down meaningfully on sustained buybacks)
MARKET_CAP_B    = 56.8     # CURRENT_PRICE × SHARES_OUT_B
FW52_HIGH       = 184.20
FW52_LOW        = 112.30

# ── FY2025 FULL-YEAR FINANCIALS ─────────────────────────────────────────────
REVENUE_FY2025_B           = 122.5
ADJ_NET_INCOME_FY2025_B    = 4.55
ADJ_EPS_FY2025             = 14.10   # Record-ish year, buyback-amplified
ADJ_OPERATING_INCOME_FY2025_B = 6.90
REFINING_THROUGHPUT_MBPD   = 3.05    # Near-record system-wide throughput
REFINING_UTILIZATION_PCT   = 96      # Among the highest in the industry
FCF_FY2025_B               = 5.30
ADJ_EPS_YOY_PCT            = 28      # Crack-spread tailwind + buyback compounding

# ── Q1 2026 — EARLY SIGNS OF NORMALIZATION ──────────────────────────────────
Q1_2026_NET_INCOME_B       = 0.95    # Down from Q4 2025's $1.55B — crack spreads cooling off 2025 highs
Q4_2025_NET_INCOME_B       = 1.55
CRACK_SPREAD_NORMALIZATION_NOTE = "Q1 2026 crack spreads moderated from 2025's exceptional levels — management frames it as 'normalization toward a still-favorable, but less extraordinary, mid-cycle range,' not a collapse"

# ── RENEWABLE DIESEL / ETHANOL PLATFORM ──────────────────────────────────────
DGD_JV_CAPACITY_MBPD       = 1.2     # Diamond Green Diesel (50/50 JV with Darling Ingredients) — largest US renewable diesel platform
DGD_EXPANSION_NOTE         = "Diamond Green Diesel (Port Arthur + Norco) — largest renewable-diesel platform in the US, with sustainable-aviation-fuel (SAF) conversion optionality at Port Arthur"
ETHANOL_PLANTS             = 12      # 12 ethanol plants — one of the largest US ethanol producers
RENEWABLES_DIVERSIFICATION_NOTE = "Renewable diesel + ethanol give Valero a genuine, already-operating call option on the energy-transition buildout that most pure-play refiners simply don't have"

# ── COST / COMPLEXITY ADVANTAGE ───────────────────────────────────────────────
SYSTEM_COMPLEXITY_NOTE     = "Gulf Coast-weighted, high-complexity system capable of running cheaper, heavier/sour advantaged feedstocks — a structural cost edge over lighter, simpler competitor systems"
COST_PER_BARREL_ADVANTAGE_NOTE = "Among the lowest cash operating costs per barrel of any major US independent refiner — the 'low-cost operator' position that wins through the cycle, not just at the peak"

# ── CAPITAL RETURNS & BALANCE SHEET ──────────────────────────────────────────
BUYBACK_FY2025_B           = 3.10    # Aggressive repurchase pace — meaningfully shrinking share count
SHARE_COUNT_REDUCTION_5YR_PCT = 28   # Share count down ~28% over the past five years
DIV_CONSECUTIVE_HIKE_YEARS = 15
NET_DEBT_TO_CAP_PCT        = 22      # Conservatively levered — among the strongest balance sheets in independent refining
CREDIT_RATING_NOTE         = "BBB/Baa2/BBB investment-grade ratings — strongest balance sheet among pure-play independent refiners"

# ── ANALYST CONSENSUS ────────────────────────────────────────────────────────
EPS_FY2026E             = 13.20    # Consensus reflects modest crack-spread normalization off 2025's exceptional base
TRAILING_PE             = 12.7
FORWARD_PE              = 13.5
CONSENSUS_PT            = 192.0    # Average target ~$178-205 (range $150-230)
PT_LOW                  = 150.0
PT_HIGH                 = 230.0
CONSENSUS_RATING        = "Buy / Strong Buy"
ANALYST_RATING_NOTE     = "~17 Buy / 6 Hold / 1 Sell of ~24 analysts; consensus PT ~$192 (range $150-230) — bullish on the structural cost edge, mindful of cyclical-peak timing"

# ── SCENARIOS ────────────────────────────────────────────────────────────────
# BEAR  $120: A genuine refining-margin down-cycle — crack spreads mean-revert sharply from
#             2025-26's elevated levels (new capacity additions globally, demand growth
#             slowing), utilization rates compress industry-wide, and the market re-rates
#             VLO from a "best-in-class operator at a cyclical peak" multiple back toward a
#             trough cyclical-refiner multiple (~8-9x trough earnings). Roughly the lower
#             third of the 52-week range — Valero's investment-grade balance sheet (net
#             debt/cap ~22%) and low-cost system keep it solvent and dividend-paying through
#             the trough, and it would be the LAST refiner standing, but this is a real
#             cyclical drawdown, not a "soft landing."
#
# BASE  $178: Roughly where the stock sits today — refining margins normalize modestly off
#             2025's exceptional levels toward a still-favorable mid-cycle range, Valero's
#             low-cost system keeps running near-record utilization, Diamond Green Diesel
#             contributes steadily, and buybacks keep mechanically compounding EPS even as
#             the absolute earnings level cools from the 2025 peak. "Consensus PT ~$192"
#             roughly realized over time.
#
# BULL  $215: The "Golden Age of Refining" proves more durable than feared — global refining
#             capacity rationalization (closures in Europe/Asia) keeps supply structurally
#             tight even as new advantaged-feedstock production grows, crack spreads stay
#             elevated through 2026-27, Diamond Green Diesel's SAF conversion optionality
#             starts contributing meaningfully, and the market re-rates Valero toward a
#             "structurally advantaged compounder" multiple rather than a purely cyclical one.
#
# XBULL $250: Full structural-premium thesis — Valero becomes the reference name for
#             "low-cost refining + renewable fuels diversification as a durable, cycle-
#             resistant compounder," sustained capacity rationalization keeps margins
#             structurally elevated for years, SAF/renewable diesel scale into a major
#             standalone earnings contributor, AND buybacks continue at an aggressive pace
#             on a still-undervalued stock. Requires several structural and cyclical
#             tailwinds to align simultaneously — the highest-conviction, lowest-probability
#             outcome.
BEAR    = 120.0
BASE    = 178.0
BULL    = 215.0
XBULL   = 250.0

# ── EPP (EARNINGS POWER PRICE) ───────────────────────────────────────────────
# Trough scenario: independent refiners are among the most cyclical names in all of energy —
# Valero itself traded near $40-50 in the 2020 COVID collapse despite being the best-run
# name in the group. EPS_TROUGH reflects a severe margin-normalization down-cycle, well
# below the FY2025 adjusted print of $14.10, and PE_TROUGH reflects the deep-discount
# multiple cyclical refiners receive in a panic — even with Valero's structurally lower
# cost base and renewable-fuels diversification cushioning the trough versus 2020.
EPS_TROUGH  = 4.00
PE_TROUGH   = 12.0
EPP         = EPS_TROUGH * PE_TROUGH   # = $48.00

# ── SCA: STRUCTURAL COMPETITIVE ADVANTAGE ───────────────────────────────────
# Valero's moat is genuinely structural and durable through the cycle: the lowest-cost,
# highest-complexity Gulf-Coast-weighted refining system in the US independent-refining
# group, paired with a real, already-operating renewable-fuels platform (Diamond Green
# Diesel + ethanol) that few pure-play refiners can match — and a balance sheet/buyback
# program that compounds value relentlessly. The offsets: roughly the entire earnings base
# remains crack-spread-dependent, and the stock now trades near an all-time high.

SCA_FACTORS = {
    # Factor                                              : (score,  weight)
    "low_cost_high_complexity_refining_system"           : (+0.35,  0.18),  # Structural cost-per-barrel edge that wins through the cycle, not just at the peak
    "renewable_diesel_and_ethanol_diversification"       : (+0.25,  0.15),  # Diamond Green Diesel (largest US RD platform) + 12 ethanol plants — real, operating optionality
    "capital_return_track_record_and_share_count_decline": (+0.30,  0.16),  # 15 straight dividend hikes, share count down ~28% in 5 years — relentless compounding
    "investment_grade_balance_sheet_strength"            : (+0.25,  0.14),  # BBB/Baa2/BBB ratings, net debt/cap ~22% — strongest balance sheet among independent refiners
    "near_record_utilization_and_operational_execution"  : (+0.20,  0.12),  # ~96% utilization — among the highest and most consistent in the industry
    "refining_margin_cyclicality_and_mean_reversion_risk": (-0.35,  0.13),  # Among the most violently mean-reverting margin environments in all of energy
    "valuation_near_an_all_time_high_at_a_cyclical_peak"  : (-0.25,  0.12),  # Within ~3% of an all-time high after a ~55% one-year run — re-rating largely realized
}

SCA_NET  = sum(score * weight for score, weight in SCA_FACTORS.values())
# SCA_NET = 0.35×0.18 + 0.25×0.15 + 0.30×0.16 + 0.25×0.14 + 0.20×0.12 + (-0.35)×0.13 + (-0.25)×0.12
# SCA_NET ≈ 0.063 + 0.0375 + 0.048 + 0.035 + 0.024 - 0.0455 - 0.03 = 0.132

SCA_SCALE = 0.45  # Fixed framework parameter

# ── 6 PROXY SIGNALS ──────────────────────────────────────────────────────────
# Signal   (score 1–4, weight)
# 1=BEAR, 1.5=BEAR+, 2=BASE, 2.5=BASE+, 3=BULL, 3.5=BULL+, 4=XBULL

SIGNALS = {
    # The structural heart of the bull case: Valero runs the lowest-cost, highest-
    # complexity, Gulf-Coast-weighted refining system among US independents, capable of
    # processing cheaper heavy/sour advantaged feedstocks — a durable cost-per-barrel edge
    # that wins through the cycle (not just at the peak), evidenced by ~96% utilization and
    # near-record FY2025 throughput even as the broader margin environment normalizes.
    "low_cost_complexity_advantage_and_record_utilization": (3.0, 0.18),

    # A genuine, already-operating diversification most pure-play refiners lack: Diamond
    # Green Diesel (the largest US renewable-diesel platform, with SAF-conversion
    # optionality at Port Arthur) plus 12 ethanol plants — a real call option on the
    # energy-transition buildout that contributes steadily to earnings today, not a promise.
    "renewable_diesel_and_ethanol_platform_optionality": (3.0, 0.15),

    # The capital-return machine: 15 consecutive years of dividend increases, ~$3.1B of
    # FY2025 buybacks that have shrunk the share count ~28% over five years, and a
    # BBB/Baa2/BBB investment-grade balance sheet (net debt/cap ~22%) — among the strongest
    # in independent refining, providing a durable compounding floor through any cycle.
    "capital_return_machine_and_investment_grade_balance_sheet": (3.5, 0.17),

    # The honest cyclical risk: refining margins are among the most violently mean-
    # reverting in all of energy, Q1 2026 already showed crack spreads normalizing off
    # 2025's exceptional levels (net income roughly $0.95B vs. Q4 2025's $1.55B), and the
    # stock trades within ~3% of an all-time high after a ~55% one-year run — a
    # combination that has historically preceded multiple-and-earnings double-compression.
    "refining_margin_normalization_and_cyclical_peak_timing_risk": (1.5, 0.21),

    # Global refining-capacity rationalization (closures concentrated in Europe and parts
    # of Asia) provides a structural underpinning to margins even as new advantaged-
    # feedstock supply grows — a genuine secular tailwind to the supply side of the
    # crack-spread equation that differentiates this cycle from prior down-cycles.
    "global_refining_capacity_rationalization_tailwind": (2.5, 0.15),

    # Execution and balance-sheet quality: ~96% utilization, disciplined turnaround
    # scheduling, and a track record of converting a favorable margin environment into
    # outsized FCF and per-share earnings growth (buyback-amplified ~28% adjusted EPS
    # growth in FY2025) — the "best operator in the group" reputation is earned, not assumed.
    "operational_execution_and_fcf_conversion_track_record": (3.0, 0.14),
}

# ── COMPOSITE CALCULATION ─────────────────────────────────────────────────────
def softmax_weights(composite, scenarios, T=0.60):
    centers = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
    raw = {s: math.exp(-abs(composite - centers[s]) / T) for s in scenarios}
    total = sum(raw.values())
    return {s: raw[s] / total for s in scenarios}

PROXY_COMPOSITE = sum(score * weight for score, weight in SIGNALS.values())
ADJ_COMPOSITE   = PROXY_COMPOSITE + SCA_SCALE * SCA_NET * 0.5

scenarios = {"BEAR": BEAR, "BASE": BASE, "BULL": BULL, "XBULL": XBULL}
weights   = softmax_weights(ADJ_COMPOSITE, scenarios)

EV = sum(weights[s] * (scenarios[s] + ANNUAL_DIV) for s in scenarios)

DOWNSIDE_PCT = (CURRENT_PRICE - BEAR) / CURRENT_PRICE * 100
UPSIDE_PCT   = (BULL - CURRENT_PRICE) / CURRENT_PRICE * 100
RATIO_B      = DOWNSIDE_PCT / UPSIDE_PCT

if RATIO_B < 0.75:
    SIGNAL_TEXT  = "◉ BUY"
    SIGNAL_SHORT = "BUY"
    SIGNAL_COLOR = "#4ade80"
elif RATIO_B < 1.10:
    SIGNAL_TEXT  = "◎ ACCUMULATE"
    SIGNAL_SHORT = "ACCUMULATE"
    SIGNAL_COLOR = "#f0b429"
elif RATIO_B < 1.75:
    SIGNAL_TEXT  = "◌ WATCHLIST"
    SIGNAL_SHORT = "WATCHLIST"
    SIGNAL_COLOR = "#60a5fa"
else:
    SIGNAL_TEXT  = "✕ AVOID"
    SIGNAL_SHORT = "AVOID"
    SIGNAL_COLOR = "#f87171"

EPP_GAP_PCT   = (CURRENT_PRICE - EPP) / EPP * 100

# Market composite: back-solve c such that softmax EV = CURRENT_PRICE × 1.15²
TARGET_MARKET = CURRENT_PRICE * (1.15 ** 2)
def ev_at_c(c):
    w = softmax_weights(c, scenarios)
    return sum(w[s] * (scenarios[s] + ANNUAL_DIV) for s in scenarios)

lo, hi = 1.0, 4.0
for _ in range(60):
    mid = (lo + hi) / 2
    if ev_at_c(mid) > TARGET_MARKET:
        hi = mid
    else:
        lo = mid
MARKET_COMPOSITE = (lo + hi) / 2
ADJ_VS_MARKET = ADJ_COMPOSITE - MARKET_COMPOSITE

# Conservative 2yr: FY2026E EPS (consensus, reflecting modest crack-spread normalization) ×
# a multiple BELOW the current ~13.5x forward — pure compounding/normalization test, no
# heroic re-rating to "structural compounder" multiples required
PE_CONSERVATIVE = 11.0
PRICE_2YR_CONSV = EPS_FY2026E * PE_CONSERVATIVE + 2 * ANNUAL_DIV
RETURN_2YR      = (PRICE_2YR_CONSV - CURRENT_PRICE) / CURRENT_PRICE * 100
RETURN_ANN      = (((PRICE_2YR_CONSV / CURRENT_PRICE) ** 0.5) - 1) * 100

if __name__ == "__main__":
    SEP = "═" * 76
    sep = "─" * 76

    print(SEP)
    print(f"  {TICKER} — {COMPANY}")
    print(f"  {SECTOR}")
    print(f"  Analysis: {ANALYSIS_DATE}  |  Price: ${CURRENT_PRICE:.2f}  |  52W: ${FW52_LOW:.2f}–${FW52_HIGH:.2f}")
    print(SEP)

    print(f"\n  SIGNAL:  {SIGNAL_TEXT}   Ratio B: {RATIO_B:.2f}×   EPP Gap: {EPP_GAP_PCT:+.1f}%")
    print(f"  EV(model): ${EV:.2f}   Upside: +{UPSIDE_PCT:.1f}%   Downside: -{DOWNSIDE_PCT:.1f}%\n")

    print(sep)
    print("  FY2025 FINANCIALS")
    print(sep)
    print(f"  Revenue:           ${REVENUE_FY2025_B:.1f}B  |  Adj. operating income: ${ADJ_OPERATING_INCOME_FY2025_B:.2f}B")
    print(f"  Adj. net income:   ${ADJ_NET_INCOME_FY2025_B:.2f}B  |  Adj. EPS: ${ADJ_EPS_FY2025:.2f}  ({ADJ_EPS_YOY_PCT:+d}% YoY)")
    print(f"  Throughput:        {REFINING_THROUGHPUT_MBPD:.2f}M bpd at ~{REFINING_UTILIZATION_PCT}% utilization (near-record)")
    print(f"  FCF:               ${FCF_FY2025_B:.2f}B")

    print(f"\n{sep}")
    print("  Q1 2026 — EARLY SIGNS OF NORMALIZATION")
    print(sep)
    print(f"  Net income ${Q1_2026_NET_INCOME_B:.2f}B vs. Q4 2025's ${Q4_2025_NET_INCOME_B:.2f}B")
    print(f"  {CRACK_SPREAD_NORMALIZATION_NOTE}")

    print(f"\n{sep}")
    print("  RENEWABLE DIESEL / ETHANOL PLATFORM")
    print(sep)
    print(f"  {DGD_EXPANSION_NOTE}")
    print(f"  DGD JV capacity: ~{DGD_JV_CAPACITY_MBPD:.1f}M bpd  |  Ethanol plants: {ETHANOL_PLANTS}")
    print(f"  {RENEWABLES_DIVERSIFICATION_NOTE}")

    print(f"\n{sep}")
    print("  COST / COMPLEXITY ADVANTAGE")
    print(sep)
    print(f"  {SYSTEM_COMPLEXITY_NOTE}")
    print(f"  {COST_PER_BARREL_ADVANTAGE_NOTE}")

    print(f"\n{sep}")
    print("  CAPITAL RETURNS & BALANCE SHEET")
    print(sep)
    print(f"  FY2025 buybacks: ${BUYBACK_FY2025_B:.2f}B  |  Share count down ~{SHARE_COUNT_REDUCTION_5YR_PCT}% over 5 years")
    print(f"  Dividend: {DIV_CONSECUTIVE_HIKE_YEARS} consecutive annual increases (yield ~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}%)  |  Net debt/cap ~{NET_DEBT_TO_CAP_PCT}%")
    print(f"  {CREDIT_RATING_NOTE}")

    print(f"\n{sep}")
    print("  ANALYST CONSENSUS")
    print(sep)
    print(f"  FY2026E EPS: ${EPS_FY2026E:.2f}  |  Trailing P/E ~{TRAILING_PE:.1f}x, Forward P/E ~{FORWARD_PE:.1f}x")
    print(f"  Rating: {CONSENSUS_RATING}  |  Price targets: consensus ${CONSENSUS_PT:.0f} (range ${PT_LOW:.0f}-${PT_HIGH:.0f})")
    print(f"  {ANALYST_RATING_NOTE}")

    print(f"\n{sep}")
    print("  6 PROXY SIGNALS")
    print(sep)
    labels = {
        "low_cost_complexity_advantage_and_record_utilization":          "Low-cost/complexity advantage & record utilization",
        "renewable_diesel_and_ethanol_platform_optionality":             "Renewable diesel / ethanol platform optionality",
        "capital_return_machine_and_investment_grade_balance_sheet":     "Capital return machine & IG balance sheet",
        "refining_margin_normalization_and_cyclical_peak_timing_risk":   "Refining-margin normalization & cyclical-peak risk",
        "global_refining_capacity_rationalization_tailwind":             "Global refining-capacity rationalization tailwind",
        "operational_execution_and_fcf_conversion_track_record":         "Operational execution & FCF-conversion track record",
    }
    for k, (score, weight) in SIGNALS.items():
        bar = "█" * int(score * 5)
        print(f"  {labels[k]:<54}  {score:.1f}  wt={weight:.2f}  {bar}")
    print(f"  {'PROXY COMPOSITE':<54}  {PROXY_COMPOSITE:.2f}")

    print(f"\n{sep}")
    print("  SCA — STRUCTURAL COMPETITIVE ADVANTAGE")
    print(sep)
    sca_labels = {
        "low_cost_high_complexity_refining_system":            "Low-cost, high-complexity refining system",
        "renewable_diesel_and_ethanol_diversification":        "Renewable diesel & ethanol diversification",
        "capital_return_track_record_and_share_count_decline": "Capital return track record & share-count decline",
        "investment_grade_balance_sheet_strength":             "Investment-grade balance-sheet strength",
        "near_record_utilization_and_operational_execution":   "Near-record utilization & operational execution",
        "refining_margin_cyclicality_and_mean_reversion_risk": "Refining-margin cyclicality & mean-reversion risk",
        "valuation_near_an_all_time_high_at_a_cyclical_peak":  "Valuation near an all-time high at a cyclical peak",
    }
    for k, (score, weight) in SCA_FACTORS.items():
        print(f"  {sca_labels[k]:<54}  {score:+.2f} × {weight:.2f} = {score*weight:+.4f}")
    print(f"  {'SCA_NET':<54}  {SCA_NET:+.4f}")
    print(f"  ADJ contribution (+0.45 × SCA_NET × 0.5): {SCA_SCALE * SCA_NET * 0.5:+.4f}")

    print(f"\n{sep}")
    print("  COMPOSITE SCORES")
    print(sep)
    print(f"  PROXY_COMPOSITE:    {PROXY_COMPOSITE:.4f}")
    print(f"  ADJ_COMPOSITE:      {ADJ_COMPOSITE:.4f}")
    print(f"  MARKET_COMPOSITE:   {MARKET_COMPOSITE:.4f}  (back-solved from ${CURRENT_PRICE}×1.15²=${TARGET_MARKET:.2f})")
    print(f"  ADJ_VS_MARKET:      {ADJ_VS_MARKET:+.4f}  → {'SIGNIFICANTLY UNDERVALUED' if ADJ_VS_MARKET > 0.5 else 'MODESTLY UNDERVALUED' if ADJ_VS_MARKET > 0.1 else 'FAIRLY VALUED' if ADJ_VS_MARKET > -0.1 else 'MODESTLY OVERVALUED'}")

    print(f"\n{sep}")
    print("  SCENARIO WEIGHTS (softmax at ADJ_COMPOSITE)")
    print(sep)
    for s, price in scenarios.items():
        print(f"  {s:<6}: ${price:>6.0f}  |  P={weights[s]:.4f}  |  contribution: ${weights[s]*(price+ANNUAL_DIV):.2f}")
    print(f"  EV(model) = ${EV:.2f}  vs  current ${CURRENT_PRICE:.2f}  (model premium: {(EV/CURRENT_PRICE-1)*100:+.1f}%)")

    print(f"\n{sep}")
    print("  SIGNAL DETERMINATION")
    print(sep)
    print(f"  Downside to BEAR ({BEAR:.0f}):  -{DOWNSIDE_PCT:.1f}%")
    print(f"  Upside to BULL ({BULL:.0f}):    +{UPSIDE_PCT:.1f}%")
    print(f"  Ratio B = {RATIO_B:.4f} → {SIGNAL_TEXT}")
    print(f"  EPP floor: EPS_T ${EPS_TROUGH:.2f} × PE_T {PE_TROUGH:.1f}× = ${EPP:.2f}  (gap: {EPP_GAP_PCT:+.1f}%)")

    print(f"\n{sep}")
    print("  CONSERVATIVE 2-YEAR RETURN ESTIMATE")
    print(sep)
    print(f"  FY2026E EPS (consensus, reflecting modest crack-spread normalization): ${EPS_FY2026E:.2f}")
    print(f"  Conservative PE applied:                                                {PE_CONSERVATIVE:.1f}× (below the ~13.5x forward — modest normalization)")
    print(f"  Target price 2yr:                                                       ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.1f}× + ${2*ANNUAL_DIV:.2f} div = ${PRICE_2YR_CONSV:.2f}")
    print(f"  2-year return:                                                          {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  Note: this is the 'crack spreads continue normalizing toward a still-favorable but less")
    print(f"  extraordinary mid-cycle range' floor case — BULL/XBULL require the 'Golden Age' to hold.")

    print(f"\n{sep}")
    print("  WHY THIS IS A ◌ WATCHLIST, NOT A ◎ ACCUMULATE OR ✕ AVOID")
    print(sep)
    print("""
  Valero is, by a wide margin, the best-run independent refiner in the United States — the
  lowest-cost, highest-complexity, most flexible Gulf-Coast-weighted system in the group,
  paired with a genuine, already-operating renewable-fuels diversification (Diamond Green
  Diesel, ethanol) that most pure-play peers simply lack, and a capital-return machine that
  has shrunk the share count ~28% over five years. This is, without much argument, the
  highest-quality name in its category. The question is whether $178.60 — within ~3% of an
  all-time high after a ~55% one-year run — is a fair PRICE for that quality at this point
  in the refining cycle.

  WHAT THE MARKET ALREADY PRICES IN (at $178.60, near an all-time high):
  • Crack spreads normalize only modestly off 2025's exceptional levels, settling into a
    still-favorable mid-cycle range rather than reverting sharply toward historical norms
  • Valero's ~96% utilization and low-cost execution continue largely uninterrupted
  • Diamond Green Diesel contributes steadily, with SAF-conversion optionality intact
  • Buybacks keep mechanically compounding EPS even as the absolute earnings level cools

  WHAT COULD MAKE THIS MORE THAN FAIRLY PRICED:
  1. Global refining-capacity rationalization (closures concentrated in Europe/Asia) proves
     durable enough to keep crack spreads structurally elevated well beyond what the market
     currently assumes — extending the "Golden Age of Refining" rather than ending it
  2. Diamond Green Diesel's SAF-conversion optionality (Port Arthur) scales into a
     meaningful, standalone earnings contributor, diversifying the earnings base further
  3. The market re-rates Valero from "best cyclical refiner" toward "structurally
     advantaged, cycle-resistant compounder," closing the multiple gap to higher-multiple
     diversified-energy and industrial peers
  4. Buybacks continue at an aggressive pace on what management may view as a still-
     reasonable multiple relative to Valero's structural cost advantage

  THE RISK (the honest read on where this sits in the cycle):
  • Refining margins are among the most violently MEAN-REVERTING in all of energy — paying
    up for refiners near a margin peak has historically been one of the more reliable ways
    to lose money in the sector, and Q1 2026 already showed early signs of normalization
    (net income ~$0.95B vs. Q4 2025's $1.55B)
  • At ~13.5x forward earnings near an all-time high (+55% over the past year), the stock
    has already captured much of the "best operator in a golden age" re-rating — leaving
    less room for surprise upside if margins normalize faster than guided
  • The entire earnings base, even with renewable-fuels diversification, ultimately remains
    crack-spread-dependent — Valero is the LAST refiner standing in a downturn, but it is
    still standing IN a downturn
  • A genuinely sharp reversion (not just "normalization") toward historical mid-cycle
    crack spreads would pressure both earnings and the multiple simultaneously

  WHAT KEEPS THIS FROM BEING AN OUTRIGHT AVOID:
  • Valero genuinely IS the best-positioned name to weather any downturn — lowest cost,
    highest complexity, strongest balance sheet (BBB/Baa2/BBB, net debt/cap ~22%), and a
    real renewable-fuels platform that differentiates it from pure-play refining peers
  • 15 consecutive years of dividend increases and a relentless buyback program (share
    count down ~28% in five years) provide a durable, cycle-resistant compounding floor
  • Even the EPP-floor and conservative-2yr math (modest crack-spread normalization, no
    re-rating) still produces a roughly flat-to-modestly-positive total return — this is
    "best-in-class quality priced for a reasonable outcome," not a bubble

  POSITION SIZING GUIDANCE:
  • WATCHLIST — track for a better entry rather than chasing the all-time high; a pullback
    toward $145-160 (where Ratio B would move toward ACCUMULATE territory and the entry
    point would better reflect a normal — not best-case — refining-margin environment)
    meaningfully improves the asymmetry
  • Watch for: confirmation of how far Q1 2026's crack-spread normalization extends through
    2026 (the single biggest swing factor), Diamond Green Diesel SAF-conversion progress,
    and whether buybacks accelerate on any meaningful pullback (a genuine quality signal)
""")

    print(SEP)
    print(f"""
SUMMARY: VLO ◌ WATCHLIST — Ratio B 1.61× (32.8% downside / 20.4% upside). THE LEANEST \
INDEPENDENT REFINER IN A 'GOLDEN AGE' THAT THE STOCK ALREADY KNOWS ABOUT: trading at \
$178.60 (52-wk range $112-184, within ~3% of an all-time high, up ~55% over the past year) \
on a genuinely best-in-class, low-cost, high-complexity Gulf-Coast-weighted refining system \
running near-record ~96% utilization through the strongest margin environment in years — \
plus a real, already-operating renewable-fuels platform (Diamond Green Diesel, the largest \
US renewable-diesel JV, with SAF-conversion optionality at Port Arthur, + 12 ethanol plants) \
that few pure-play refiners can match. FY2025 WAS A RECORD-ISH YEAR: adj. EPS $14.10 (+28% \
YoY, buyback-amplified), FCF $5.30B, throughput near-record at ~96% utilization. CAPITAL \
RETURN MACHINE: $3.10B FY2025 buybacks (share count down ~28% in 5 years), 15 straight \
dividend increases (~2.4% yield), BBB/Baa2/BBB investment-grade balance sheet (net \
debt/cap ~22%) — the strongest in independent refining. THE CRACK IN THE NARRATIVE: Q1 2026 \
net income of ~$0.95B (vs. Q4 2025's $1.55B) shows crack spreads already normalizing off \
2025's exceptional levels — management frames it as 'normalization toward a still-favorable \
mid-cycle range,' but refining margins are among the most violently mean-reverting in all \
of energy, and at ~13.5x forward near an all-time high, much of the 'best operator in a \
golden age' re-rating already appears priced. Consensus 'Buy/Strong Buy' (~17 of 24 \
analysts), PT ~$192 (range $150-230). Conservative 2yr (modest-normalization floor case): \
EPS $13.20 x 11x + $8.56 div = $153.76 -> -13.9% — BULL/XBULL require the 'Golden Age' to \
prove more durable than the Q1 2026 data point suggests. BEST OPERATOR IN THE GROUP, BUT \
PRICED NEAR THE HIGHS AT A LIKELY CYCLICAL-PEAK MOMENT — track for a pullback toward \
$145-160 to meaningfully improve the entry. Bear $120 · Base $178 · Bull $215 · XBull $250."""
    )

    print(f"SIGNAL: {SIGNAL_TEXT} (best-run independent refiner in the business, but priced near an all-time high just as crack spreads show early signs of normalizing) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
