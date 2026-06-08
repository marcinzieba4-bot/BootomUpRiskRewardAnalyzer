"""
Marathon Petroleum Corporation (NYSE: MPC)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ✕ AVOID  |  Ratio B: 2.02×  |  EPP Gap: +394.3%

THE REFINING GIANT AT AN ALL-TIME HIGH — A REAL "GOLDEN AGE," BUT THE PRICE HAS
ALREADY BANKED IT AND THEN SOME
Trading at $266.91 (52-week range $158–272, within ~2% of its all-time high, +51% YTD
in 2026 alone) on:
  (1) A genuine "Golden Age of Refining" — industry-wide capacity rationalization
      (European/Atlantic Basin plant closures) has kept crack spreads structurally
      elevated since 2022, and MPC has converted that into record results: FY2025
      net income $4.0B ($13.22/sh, vs $10.08 in 2024), adjusted EBITDA $12.0B, and
      free cash flow of $8.3B — up an extraordinary 389% YoY
  (2) A genuine "capital return powerhouse": that record FCF is funding an aggressive
      buyback program (authorization increased by $5.0B in May 2026, $3.63B remaining
      as of Q1) that has shrunk the share count dramatically and mechanically lifted
      EPS — plus a growing, fee-based MPLX midstream cash-flow stream (bolt-on deals
      like Northwind Midstream) that diversifies away from pure refining-margin exposure
  (3) Strong operating execution: ~95% crude utilization, ~3.0 million bpd throughput,
      Q4 2025 adjusted EBITDA of $3.5B (vs $2.1B a year earlier)

But here is the honest tension: Q1 2026 net income of just $511M — a fraction of Q4
2025's $1.5B — is the first real crack in the "Golden Age" narrative, exactly the kind
of margin-normalization signal that tends to show up just as a cyclical peak registers
in the share price. At $266.91, MPC sits within 2% of its all-time high after a +51%
YTD run, on a trailing P/E near 20x (vs. a historically much cheaper refiner multiple)
and a FY2026 EPS estimate range so wide ($15-21) that the market is visibly struggling
to underwrite the next leg. This is a "great business, terrible entry point" situation —
Ratio B sits in AVOID territory because the downside (a return to more "normal" crack
spreads, which the Q1 print already hints at) is large relative to the upside that
remains once a record year is already mostly priced in.

Conviction: MODERATE-HIGH that the underlying franchise (scale, MPLX optionality,
capital-return discipline) is genuinely excellent; LOW conviction that today's price
offers an attractive entry — refining is a brutally cyclical business, and buying the
best operator at an all-time high, just as the segment's own results show the first
signs of normalization, is precisely the setup that has burned investors in past cycles.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "MPC"
COMPANY         = "Marathon Petroleum Corporation"
SECTOR          = "Oil Refining & Marketing · Midstream (MPLX) · Renewable Fuels (Martinez, Dickinson) · Retail · NYSE: MPC"
SECTOR_GROUP    = "Energy"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 266.91   # June 8, 2026 — within ~2% of the all-time high ($272.46)
ANNUAL_DIV      = 4.00     # $1.00/qtr; yield ~1.5%
SHARES_OUT_B    = 0.385    # Heavily reduced via buybacks (was ~409M in 2023; sub-400M now)
MARKET_CAP_B    = 102.8    # CURRENT_PRICE × SHARES_OUT_B
FW52_HIGH       = 272.46
FW52_LOW        = 158.00
YTD_GAIN_PCT    = 51       # Up ~51% YTD in 2026 alone

# ── FY2025 FULL-YEAR FINANCIALS ─────────────────────────────────────────────
NET_INCOME_FY2025_B       = 4.0
EPS_FY2025                = 13.22   # Diluted, vs $10.08 in 2024 (+31% — largely buyback-driven)
EPS_FY2024                = 10.08
ADJ_EBITDA_FY2025_B       = 12.0    # vs $11.3B in 2024
OCF_FY2025_B              = 8.3
FCF_FY2025_B              = 8.3     # Up 389% YoY — extraordinary, largely margin-driven
FCF_GROWTH_YOY_PCT        = 389
CRUDE_UTILIZATION_PCT     = 95
THROUGHPUT_MMBPD          = 3.0

# ── Q4 2025 vs Q1 2026 — THE CRACK IN THE NARRATIVE ──────────────────────────
Q4_2025_REVENUE_B         = 33.42
Q4_2025_NET_INCOME_B      = 1.5
Q4_2025_EPS               = 5.12
Q4_2025_ADJ_EBITDA_B      = 3.5
Q4_2024_ADJ_EBITDA_B      = 2.1
Q1_2026_REVENUE_B         = 34.57
Q1_2026_NET_INCOME_M      = 511     # Sharply below Q4 2025's $1.5B — first sign of margin normalization
SEQUENTIAL_DECLINE_NOTE   = "Q1 2026 net income of $511mm was roughly 1/3 of Q4 2025's $1.5B — exactly the kind of margin-normalization signal that tends to show up near a cyclical peak"

# ── CAPITAL RETURNS ──────────────────────────────────────────────────────────
BUYBACK_AUTH_INCREASE_2026_B = 5.0   # New authorization added May 2026
BUYBACK_REMAINING_Q1_B       = 3.63  # As of March 31, 2026 (down from $4.4B at YE2025)
Q4_2025_TOTAL_RETURNS_B      = 1.3
QUARTERLY_DIV                = 1.00
DEBT_TO_EQUITY               = 1.31
CREDIT_RATING_SP             = "BBB"

# ── MPLX / MIDSTREAM ──────────────────────────────────────────────────────────
MPLX_NOTE                = "Continues bolt-on midstream growth (e.g., Northwind Midstream acquisition, 2025) — a growing, fee-based cash-flow stream that diversifies away from pure refining-margin exposure"

# ── RENEWABLE DIESEL / MARTINEZ ──────────────────────────────────────────────
RENEWABLE_DIESEL_EBITDA_Q4_2025_M = 7    # Down sharply from $28mm in Q4 2024
RENEWABLE_DIESEL_EBITDA_Q4_2024_M = 28
RENEWABLE_DIESEL_NOTE             = "Renewable Diesel segment EBITDA fell to $7mm (from $28mm a year earlier) — softer near-term economics, though positioned for LCFS/RFS credit growth as low-carbon fuel standards spread state by state"

# ── ANALYST CONSENSUS ────────────────────────────────────────────────────────
EPS_FY2026E_LOW         = 15.46
EPS_FY2026E_HIGH        = 21.0
EPS_FY2026E             = 17.0     # Rough midpoint of a genuinely wide consensus range
TRAILING_PE             = 20.2     # CURRENT_PRICE / EPS_FY2025
CONSENSUS_PT            = 245.0    # Roughly midpoint of the $223-265 range cited across sources
PT_LOW                  = 170.0
PT_HIGH                 = 331.0
CONSENSUS_RATING        = "Buy / Moderate Buy"
ANALYST_RATING_NOTE     = "~8-10 Buy / 5-7 Hold / 1 Sell of ~18-19 analysts; PT range $170-331 (Wells Fargo) is unusually wide — a sign of genuine disagreement on how durable today's margins are"

# ── REFINING MARGIN ENVIRONMENT ──────────────────────────────────────────────
GOLDEN_AGE_NOTE          = "'Golden Age of Refining' (since 2022) persists into 2026 but is moderating — tight global capacity from older-plant closures in Europe/Atlantic Basin has supported crack spreads, but Q1 2026 results already show normalization from the Q4 2025 peak"
GEOPOLITICAL_RISK_NOTE   = "Part of the bull case for elevated 2026 EPS estimates ($15-21 range) rests on a Middle East geopolitical risk premium (e.g., Strait of Hormuz tension) — a tailwind that is inherently unstable and could reverse sharply"

# ── SCENARIOS ────────────────────────────────────────────────────────────────
# BEAR  $180: Crack spreads normalize meaningfully from "Golden Age" extremes — Q1
#             2026's sequential earnings collapse ($511mm vs $1.5B) proves to be the
#             start of a real down-cycle rather than a one-quarter blip; EPS reverts
#             toward $9-11 as margins compress; the market re-rates MPC from "compounding
#             machine" back toward a "normal cyclical refiner" multiple (10-12x).
#             Roughly the lower-middle of the 52-week range — even here, MPLX's
#             fee-based cash flows and the buyback program (BBB balance sheet) cushion
#             the dividend, but this is a real earnings reset, not just sentiment.
#
# BASE  $255: Crack spreads moderate from peak but stay constructive (the rationalization
#             thesis partially holds); EPS settles near the low-to-mid end of the
#             $15-21 consensus range; buybacks continue shrinking the share count and
#             MPLX keeps growing its fee-based contribution. Roughly "today's price with
#             a modest multiple normalization" — essentially a sideways-to-down outcome
#             from here, reflecting that a great year is already mostly in the price.
#
# BULL  $310: The "Golden Age of Refining" proves more durable than skeptics expect —
#             industry capacity stays structurally tight, crack spreads hold near 2025
#             levels, EPS comes in at the high end of consensus (~$20-21), buybacks
#             keep compounding EPS mechanically, and MPLX/renewable-fuels optionality
#             contributes meaningfully. Multiple holds near today's ~16-18x on 2026E.
#
# XBULL $355: A genuine supply-shock scenario — geopolitical disruption (Strait of
#             Hormuz-style event) or accelerated global refining-capacity closures push
#             crack spreads to NEW highs, MPC's scale and complexity advantages let it
#             capture outsized margin, buybacks accelerate further on even-higher FCF,
#             AND MPLX/renewables contribute more than guided. Requires multiple
#             structural and event-driven tailwinds to align — the highest-conviction,
#             lowest-probability outcome, and inherently unstable if realized.
BEAR    = 180.0
BASE    = 255.0
BULL    = 310.0
XBULL   = 355.0

# ── EPP (EARNINGS POWER PRICE) ───────────────────────────────────────────────
# Trough scenario: refining is among the most brutally cyclical sub-sectors in energy —
# in a genuine down-cycle (weak demand + ample capacity, the mirror image of today's
# "Golden Age"), MPC's EPS could revert sharply below even its pre-rally normalized
# level. PE_TROUGH reflects the deep-discount multiple cyclical refiners get when the
# market correctly prices in mean-reversion of crack spreads.
EPS_TROUGH  = 4.50
PE_TROUGH   = 12.0
EPP         = EPS_TROUGH * PE_TROUGH   # = $54.00

# ── SCA: STRUCTURAL COMPETITIVE ADVANTAGE ───────────────────────────────────
# MPC's moat rests on scale and refining complexity (able to process advantaged
# crudes at high utilization), a genuinely valuable MPLX midstream stake that
# diversifies cash flow, and a best-in-class capital-return discipline. The
# structural offsets are severe: refining margins are brutally cyclical and mean-
# reverting, the long-run secular demand-destruction/EV-transition overhang is real,
# and — uniquely among the names in this framework — the CURRENT VALUATION itself
# is a structural risk: buying the best operator at an all-time high, just as its
# own results show the first signs of normalization, is a a pattern that has
# burned investors across past refining cycles.

SCA_FACTORS = {
    # Factor                                            : (score,  weight)
    "scale_and_refining_complexity_advantage"           : (+0.30,  0.17),  # Able to run advantaged crudes at ~95% utilization, ~3.0 MMbpd
    "mplx_integrated_midstream_optionality"             : (+0.25,  0.15),  # Growing, fee-based cash-flow stream diversifying away from pure crack-spread exposure
    "capital_return_powerhouse_track_record"            : (+0.30,  0.15),  # Record FCF funding aggressive buybacks ($5B new authorization) + dividend
    "investment_grade_balance_sheet"                    : (+0.20,  0.13),  # BBB rating; D/E ~1.31 — manageable, if not pristine
    "cyclical_refining_margin_exposure"                 : (-0.40,  0.15),  # Brutally mean-reverting crack spreads — Q1 2026 already shows the turn
    "secular_demand_destruction_ev_transition_overhang" : (-0.25,  0.13),  # Long-run gasoline-demand headwind common to all refiners
    "valuation_at_cyclical_peak_risk"                   : (-0.30,  0.12),  # Trading within 2% of an all-time high, +51% YTD — the price itself is the risk
}

SCA_NET  = sum(score * weight for score, weight in SCA_FACTORS.values())
# SCA_NET = 0.30×0.17 + 0.25×0.15 + 0.30×0.15 + 0.20×0.13 + (-0.40)×0.15 + (-0.25)×0.13 + (-0.30)×0.12
# SCA_NET ≈ 0.051 + 0.0375 + 0.045 + 0.026 - 0.06 - 0.0325 - 0.036 = 0.031

SCA_SCALE = 0.45  # Fixed framework parameter

# ── 6 PROXY SIGNALS ──────────────────────────────────────────────────────────
# Signal   (score 1–4, weight)
# 1=BEAR, 1.5=BEAR+, 2=BASE, 2.5=BASE+, 3=BULL, 3.5=BULL+, 4=XBULL

SIGNALS = {
    # The "Golden Age of Refining" is real — industry-wide capacity rationalization
    # (European/Atlantic Basin closures) has kept crack spreads structurally elevated
    # since 2022, and MPC's FY2025 results (record EBITDA, record FCF) are the direct
    # evidence of that tailwind converting into cash. The open question is durability.
    "golden_age_of_refining_margin_tailwind": (3.0, 0.16),

    # A genuine "capital return powerhouse": $8.3B of FCF (+389% YoY) funding an
    # aggressive buyback program ($5.0B new authorization in May 2026, $3.63B
    # remaining), which has shrunk the share count dramatically and mechanically
    # lifted EPS — a durable compounding mechanism, though one that depends on the
    # underlying cash generation continuing at something near today's elevated pace.
    "record_fcf_and_buyback_powered_compounding": (3.5, 0.16),

    # MPLX continues to grow as a fee-based, contracted midstream cash-flow stream
    # (bolt-on deals like the 2025 Northwind Midstream acquisition) — genuine
    # diversification away from pure refining-margin exposure that should smooth
    # MPC's earnings profile across the cycle, even if it remains a minority of the mix.
    "mplx_fee_based_midstream_cash_flow_growth": (3.0, 0.14),

    # The honest near-term risk, laid bare in the numbers: Q1 2026 net income of just
    # $511mm was roughly a third of Q4 2025's $1.5B — exactly the kind of margin-
    # normalization signal that tends to register near a cyclical peak. The stock
    # sits within 2% of its all-time high, +51% YTD, on a trailing P/E near 20x — a
    # combination that has preceded sharp drawdowns in past refining cycles.
    "crack_spread_normalization_and_cyclical_peak_risk": (1.5, 0.22),

    # Renewable Diesel (Martinez, Dickinson) — the supposed "next leg" of MPC's
    # diversification story — actually went the WRONG way in the most recent
    # quarter: segment EBITDA fell to $7mm from $28mm a year earlier. A reminder
    # that "energy transition" optionality at MPC remains immature and uneven.
    "renewable_diesel_transition_softness": (2.0, 0.12),

    # Operationally, MPC is executing at a genuinely high level: ~95% crude
    # utilization, ~3.0 MMbpd throughput, Q4 2025 adjusted EBITDA of $3.5B (vs
    # $2.1B a year earlier). This is a best-in-class operator — the question is
    # whether "best-in-class operator at an all-time high" is a good entry point.
    "refining_utilization_and_operational_execution": (3.0, 0.20),
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

# Conservative 2yr: a midpoint FY2026E EPS × a multiple BELOW the current ~20x
# trailing (reflecting the cyclical-normalization risk the Q1 print already hints
# at) + 2yr dividends — a deliberately cautious, "don't extrapolate the peak" test
PE_CONSERVATIVE = 12.0
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
    print("  FY2025 FINANCIALS — A RECORD YEAR")
    print(sep)
    print(f"  Net Income: ${NET_INCOME_FY2025_B:.1f}B (${EPS_FY2025:.2f}/sh, vs ${EPS_FY2024:.2f} in 2024 — +{(EPS_FY2025/EPS_FY2024-1)*100:.0f}%, largely buyback-driven)")
    print(f"  Adj. EBITDA: ${ADJ_EBITDA_FY2025_B:.1f}B (vs $11.3B in 2024)  |  OCF/FCF: ${OCF_FY2025_B:.1f}B / ${FCF_FY2025_B:.1f}B (+{FCF_GROWTH_YOY_PCT}% YoY — extraordinary)")
    print(f"  Crude utilization {CRUDE_UTILIZATION_PCT}%  |  Throughput ~{THROUGHPUT_MMBPD:.1f} MMbpd")

    print(f"\n{sep}")
    print("  THE CRACK IN THE NARRATIVE — Q4 2025 vs Q1 2026")
    print(sep)
    print(f"  Q4 2025: revenue ${Q4_2025_REVENUE_B:.2f}B | net income ${Q4_2025_NET_INCOME_B:.1f}B (${Q4_2025_EPS:.2f}/sh) | adj. EBITDA ${Q4_2025_ADJ_EBITDA_B:.1f}B (vs ${Q4_2024_ADJ_EBITDA_B:.1f}B Q4'24)")
    print(f"  Q1 2026: revenue ${Q1_2026_REVENUE_B:.2f}B | net income ${Q1_2026_NET_INCOME_M}mm")
    print(f"  {SEQUENTIAL_DECLINE_NOTE}")

    print(f"\n{sep}")
    print("  CAPITAL RETURNS & BALANCE SHEET")
    print(sep)
    print(f"  Buyback: +${BUYBACK_AUTH_INCREASE_2026_B:.1f}B new authorization (May 2026); ${BUYBACK_REMAINING_Q1_B:.2f}B remaining as of Q1; Q4 2025 alone returned ${Q4_2025_TOTAL_RETURNS_B:.1f}B")
    print(f"  Dividend ${QUARTERLY_DIV:.2f}/qtr (${ANNUAL_DIV:.2f}/yr, ~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}% yield)  |  Credit: {CREDIT_RATING_SP} (S&P)  |  Debt/Equity ~{DEBT_TO_EQUITY:.2f}")

    print(f"\n{sep}")
    print("  MPLX / MIDSTREAM & RENEWABLE FUELS")
    print(sep)
    print(f"  MPLX: {MPLX_NOTE}")
    print(f"  Renewable Diesel: {RENEWABLE_DIESEL_NOTE}")

    print(f"\n{sep}")
    print("  REFINING MARGIN ENVIRONMENT")
    print(sep)
    print(f"  {GOLDEN_AGE_NOTE}")
    print(f"  {GEOPOLITICAL_RISK_NOTE}")

    print(f"\n{sep}")
    print("  ANALYST CONSENSUS")
    print(sep)
    print(f"  FY2026E EPS: ${EPS_FY2026E_LOW:.2f}-${EPS_FY2026E_HIGH:.2f} (using ~${EPS_FY2026E:.2f} midpoint)  |  Trailing P/E ~{TRAILING_PE:.1f}x")
    print(f"  Rating: {CONSENSUS_RATING}  |  Price targets: ~${CONSENSUS_PT:.0f} (range ${PT_LOW:.0f}-${PT_HIGH:.0f})")
    print(f"  {ANALYST_RATING_NOTE}")

    print(f"\n{sep}")
    print("  6 PROXY SIGNALS")
    print(sep)
    labels = {
        "golden_age_of_refining_margin_tailwind":             "'Golden Age of Refining' margin tailwind",
        "record_fcf_and_buyback_powered_compounding":         "Record FCF / buyback-powered compounding",
        "mplx_fee_based_midstream_cash_flow_growth":          "MPLX fee-based midstream cash-flow growth",
        "crack_spread_normalization_and_cyclical_peak_risk":  "Crack-spread normalization / cyclical-peak risk",
        "renewable_diesel_transition_softness":               "Renewable diesel / transition softness",
        "refining_utilization_and_operational_execution":     "Refining utilization & operational execution",
    }
    for k, (score, weight) in SIGNALS.items():
        bar = "█" * int(score * 5)
        print(f"  {labels[k]:<50}  {score:.1f}  wt={weight:.2f}  {bar}")
    print(f"  {'PROXY COMPOSITE':<50}  {PROXY_COMPOSITE:.2f}")

    print(f"\n{sep}")
    print("  SCA — STRUCTURAL COMPETITIVE ADVANTAGE")
    print(sep)
    sca_labels = {
        "scale_and_refining_complexity_advantage":            "Scale & refining complexity advantage",
        "mplx_integrated_midstream_optionality":              "MPLX integrated midstream optionality",
        "capital_return_powerhouse_track_record":             "Capital return powerhouse track record",
        "investment_grade_balance_sheet":                     "Investment-grade balance sheet (BBB)",
        "cyclical_refining_margin_exposure":                  "Cyclical refining-margin exposure",
        "secular_demand_destruction_ev_transition_overhang":  "Secular demand-destruction / EV overhang",
        "valuation_at_cyclical_peak_risk":                    "Valuation at cyclical-peak risk",
    }
    for k, (score, weight) in SCA_FACTORS.items():
        print(f"  {sca_labels[k]:<50}  {score:+.2f} × {weight:.2f} = {score*weight:+.4f}")
    print(f"  {'SCA_NET':<50}  {SCA_NET:+.4f}")
    print(f"  ADJ contribution (+0.45 × SCA_NET × 0.5): {SCA_SCALE * SCA_NET * 0.5:+.4f}")

    print(f"\n{sep}")
    print("  COMPOSITE SCORES")
    print(sep)
    print(f"  PROXY_COMPOSITE:    {PROXY_COMPOSITE:.4f}")
    print(f"  ADJ_COMPOSITE:      {ADJ_COMPOSITE:.4f}")
    print(f"  MARKET_COMPOSITE:   {MARKET_COMPOSITE:.4f}  (back-solved from ${CURRENT_PRICE}×1.15²=${TARGET_MARKET:.2f})")
    print(f"  ADJ_VS_MARKET:      {ADJ_VS_MARKET:+.4f}  → {'SIGNIFICANTLY UNDERVALUED' if ADJ_VS_MARKET > 0.5 else 'MODESTLY UNDERVALUED' if ADJ_VS_MARKET > 0.1 else 'FAIRLY VALUED' if ADJ_VS_MARKET > -0.1 else 'MODESTLY OVERVALUED' if ADJ_VS_MARKET > -0.5 else 'SIGNIFICANTLY OVERVALUED'}")

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
    print(f"  FY2026E EPS (consensus midpoint, deliberately cautious):  ${EPS_FY2026E:.2f}")
    print(f"  Conservative PE applied:                                   {PE_CONSERVATIVE:.1f}× (well below the ~{TRAILING_PE:.0f}x trailing — pricing in mean-reversion of crack spreads)")
    print(f"  Target price 2yr:                                          ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.1f}× + ${2*ANNUAL_DIV:.2f} div = ${PRICE_2YR_CONSV:.2f}")
    print(f"  2-year return:                                             {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  Note: this is the 'crack spreads mean-revert toward historical norms' floor case — BASE/BULL")
    print(f"  require the 'Golden Age of Refining' to prove durable enough to sustain today's elevated multiple.")

    print(f"\n{sep}")
    print("  WHY THIS IS A ✕ AVOID, NOT A ◌ WATCHLIST OR ◎ ACCUMULATE")
    print(sep)
    print("""
  Marathon Petroleum is, by the numbers, the best-executing refiner in the business —
  but at $266.91, within 2% of its all-time high after a +51% YTD run, the stock is
  asking investors to underwrite the CONTINUATION of an unusually favorable cycle at
  exactly the moment its own results show the first signs that the cycle is turning.

  WHAT THE MARKET ALREADY PRICES IN (at $266.91, near an all-time high):
  • The "Golden Age of Refining" persists largely intact through 2026 and beyond
  • Buybacks keep mechanically compounding EPS at something near today's record pace
  • MPLX and renewable fuels contribute smoothly, with no real missteps
  • Crack spreads stay structurally elevated rather than reverting toward historical norms

  WHAT WOULD HAVE TO GO RIGHT FOR THIS TO STILL WORK FROM HERE:
  1. Q1 2026's sharp sequential earnings decline ($511mm vs $1.5B) proves to be a
     one-quarter blip (seasonal turnarounds, timing) rather than the start of a real
     down-cycle — and crack spreads re-accelerate back toward 2025's elevated levels
  2. Industry-wide refining-capacity rationalization continues fast enough to keep
     global supply structurally tight even as MPC and peers run near full utilization
  3. The Middle East geopolitical risk premium embedded in bullish 2026 EPS estimates
     ($15-21 range) persists or intensifies rather than fading (which would be its
     own kind of bad news for the world, even if "good" for MPC's near-term earnings)
  4. MPLX and renewable fuels (currently shrinking, not growing — Renewable Diesel
     EBITDA fell from $28mm to $7mm YoY) start contributing meaningfully to diversify
     the earnings base away from pure crack-spread exposure

  THE RISK (the case for why this likely does NOT work from here):
  • Refining margins are among the most brutally MEAN-REVERTING in all of energy — and
    Q1 2026 already shows the reversion beginning, just as the stock prints a new high
  • A trailing P/E near 20x is HIGH for a cyclical refiner — historically, paying up for
    refiners near a margin peak has been one of the more reliable ways to lose money in
    energy investing; the wide $170-331 analyst PT dispersion reflects genuine uncertainty
    about whether today's earnings power is durable or a peak print
  • The long-run secular demand-destruction/EV-transition overhang is real and gradual
  • "Energy transition" optionality (renewable diesel) is currently moving the WRONG way

  WHAT KEEPS THIS FROM BEING A ZERO (why it's AVOID, not a short-sale thesis):
  • MPC genuinely is the best-executing refiner — scale, complexity, ~95% utilization,
    and a real, growing MPLX midstream optionality that should smooth future cycles
  • A BBB balance sheet and substantial buyback firepower provide real downside support
    even in a margin-normalization scenario — this is not a broken business

  POSITION SIZING GUIDANCE:
  • AVOID at today's price — not because MPC is a bad company, but because "best operator
    at an all-time high, just as results show the cycle turning" is a poor entry point
  • Revisit on weakness toward $190-210 (where Ratio B would move toward WATCHLIST/
    ACCUMULATE territory and the trailing multiple would compress to a more typical
    cyclical-refiner level) — or after 2-3 quarters confirm whether Q1 2026 was a blip
    or the start of a genuine margin down-cycle
  • The Q1 2026 sequential earnings collapse is the single most important data point in
    this entire analysis — it is the market telling you the cycle may already be turning
""")

    print(SEP)
    print(f"""
SUMMARY: MPC ✕ AVOID — Ratio B 2.02× (32.6% downside / 16.1% upside). REFINING GIANT AT \
AN ALL-TIME HIGH WITH THE CYCLE ALREADY SHOWING SIGNS OF TURNING: trading at $266.91 \
(52-wk range $158-272, within ~2% of the all-time high, +51% YTD in 2026 alone) — best- \
executing refiner in the business, but the price is asking investors to underwrite \
CONTINUATION of an unusually favorable cycle exactly as its own results show the first \
cracks. FY2025 WAS A RECORD YEAR: net income $4.0B ($13.22/sh), adj. EBITDA $12.0B, FCF \
$8.3B (+389% YoY) at 95% crude utilization — funding an aggressive buyback program ($5.0B \
new authorization May 2026, $3.63B remaining) that has mechanically compounded EPS. THE \
CRACK IN THE NARRATIVE: Q1 2026 net income of just $511mm was roughly a THIRD of Q4 2025's \
$1.5B — exactly the kind of margin-normalization signal that tends to register near a \
cyclical peak. MPLX keeps growing as a fee-based diversifier, but Renewable Diesel \
actually went the WRONG way (segment EBITDA fell from $28mm to $7mm YoY). Trailing P/E \
~20x is HIGH for a cyclical refiner — paying up for refiners near a margin peak has \
historically been one of the more reliable ways to lose money in energy investing (the \
unusually wide $170-331 analyst PT dispersion reflects genuine disagreement on durability). \
Conservative 2yr (mean-reversion floor case): EPS $17 x 12x + $8.00 div = $212.00 -> -20.6% \
— BASE/BULL require the 'Golden Age of Refining' to prove durable enough to sustain \
today's elevated multiple. AVOID at today's price — revisit on weakness toward $190-210 \
or after 2-3 quarters confirm whether Q1 2026 was a blip or a genuine down-cycle. Bear \
$180 · Base $255 · Bull $310 · XBull $355."""
    )

    print(f"SIGNAL: {SIGNAL_TEXT} (best-executing refiner, but priced at an all-time high just as the cycle shows signs of turning — poor entry point, not a broken business) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
