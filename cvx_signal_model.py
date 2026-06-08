"""
Chevron Corporation (NYSE: CVX)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.89×  |  EPP Gap: +177.5%

THE HESS-SUPERCHARGED SUPERMAJOR — LOWEST COST-OF-SUPPLY IN THE INDUSTRY, INTEGRATION RUNNING AHEAD OF PLAN
Trading at $187 (52-week range $140–215, comfortably above the midpoint) on:
  (1) The ~$55B Hess acquisition (closed July 2025) running AHEAD of its synergy plan —
      >$1.5B of a $2B structural cost-synergy target already realized by March 2026, with
      $3-4B in structural cost cuts on track for year-end 2026, plus first oil at Yellowtail
      and FID reached on Hammerhead (Stabroek block, Guyana) — assets the market has barely
      begun to credit in CVX's numbers
  (2) Legacy organic growth firing on both cylinders: Permian Basin production has
      surpassed 1 million boe/d (+12% YoY) and the Tengiz (Kazakhstan) expansion added
      ~260,000 b/d in 2025 — both running at the lowest cost-of-supply in the supermajor
      peer group (~$30/bbl companywide breakeven)
  (3) A capital-return machine returning $6.0B to shareholders in Q1 2026 alone ($2.5B
      buybacks + $3.5B dividends) on a ~3.8% yield, backed by an investment-grade balance
      sheet (net debt/CFFO ~1.0x) — even after a sharp 2025 earnings reset (net income
      fell from $17.7B in 2024 to $12.3B in 2025 as oil prices normalized off the 2025 spike)

At $187 the stock sits well above its 52-week low of $140 — this is NOT a deep-value
dislocation, but a "own the lowest-cost integrated major and let Hess/Permian/Tengiz
compound" name. The trailing P/E (~33×) looks rich only because 2025/early-2026 earnings
were temporarily depressed by lower realized oil prices; on a normalized/forward basis
(consensus 2026E EPS ~$13.86, ~13-14× forward) the multiple is squarely in-line with peers.
Ratio B sits just inside ACCUMULATE territory because the downside is genuinely cushioned
(lowest-cost barrels in the industry, IG balance sheet, ~3.8% yield with room to grow)
while the upside (Hess synergies beating + Guyana ramp + Permian/Tengiz growth) is real
and increasingly underwritten by execution already in hand.

Conviction: MODERATE-HIGH on the base case (capital-return compounding + Permian/Tengiz
volume growth + Hess synergy realization on schedule); HIGHER on the multi-year structural
re-rating case if Hess/Guyana keeps beating (echoing the XOM/Pioneer "beat-and-raise"
pattern) and oil holds in a constructive $70-80/bbl range rather than the EIA's softer
$79-89/bbl 2026-27 forecast path.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "CVX"
COMPANY         = "Chevron Corporation"
SECTOR          = "Integrated Oil & Gas · Upstream (Permian, Tengiz, Guyana via Hess) · Downstream & Chemicals · LNG · NYSE: CVX"
SECTOR_GROUP    = "Energy"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 187.31   # June 7, 2026
ANNUAL_DIV      = 7.12     # ~3.8% yield; quarterly raises through the year
SHARES_OUT_B    = 1.98     # ~1.98B weighted avg shares (Q1 2026 10-Q)
MARKET_CAP_B    = 371.0    # CURRENT_PRICE × SHARES_OUT_B
FW52_HIGH       = 214.71
FW52_LOW        = 139.69

# ── FY2025 FULL-YEAR FINANCIALS ─────────────────────────────────────────────
NET_INCOME_FY2025_B       = 12.3   # Down sharply from $17.7B (2024) and $21.4B (2023)
NET_INCOME_FY2024_B       = 17.7
NET_INCOME_FY2023_B       = 21.4
FCF_FY2024_B              = 19.8
FCF_9M_FY2025_B           = 13.8
FCF_TARGET_FY2026_B       = 12.5   # Raised from $10B at Hess close
INCREMENTAL_FCF_AT_70BRENT_B = 10.0  # Incremental annual FCF from legacy portfolio at $70 Brent
INCREMENTAL_FCF_AT_60BRENT_B = 9.0

# ── Q1 2026 SNAPSHOT ─────────────────────────────────────────────────────────
Q1_REVENUE_B            = 48.6     # vs $47.6B Q1 2025
Q1_NET_INCOME_B         = 2.21
Q1_DILUTED_EPS          = 1.11     # vs $2.00 (Q1 2025) — earnings still under pressure
Q1_2025_NET_INCOME_B    = 3.50
Q1_2025_DILUTED_EPS     = 2.00
Q1_TOTAL_RETURNS_B      = 6.0      # $2.5B buybacks + $3.5B dividends

# ── HESS ACQUISITION ─────────────────────────────────────────────────────────
HESS_DEAL_SIZE_B            = 55.0
HESS_CLOSE_DATE             = "July 2025"
HESS_SYNERGY_TARGET_ORIGINAL_B  = 1.0   # Original ~$1B run-rate target
HESS_STRUCTURAL_TARGET_B        = 2.0   # $2B structural cost-synergy target
HESS_STRUCTURAL_REALIZED_B      = 1.5   # >$1.5B realized as of March 2026 — ahead of schedule
HESS_STRUCTURAL_CUTS_2026_LOW_B = 3.0   # $3-4B structural cost cuts on track by YE 2026
HESS_STRUCTURAL_CUTS_2026_HIGH_B = 4.0
HESS_ASSETS_NOTE            = "Brought Guyana (Stabroek block), Bakken, and Malaysia assets"
HESS_CEO_QUOTE_NOTE         = "CEO told employees the deal is 'outperforming targets' (March 2026)"

# ── GUYANA / STABROEK (VIA HESS) ─────────────────────────────────────────────
GUYANA_YELLOWTAIL_STATUS    = "First oil achieved — 4th Stabroek development online"
GUYANA_HAMMERHEAD_STATUS    = "FID reached — 7th Stabroek development sanctioned"
GUYANA_NOTE                 = "Arguably the best new offshore oil province discovered this century — now flowing into CVX's numbers via Hess"

# ── LEGACY UPSTREAM GROWTH ───────────────────────────────────────────────────
PERMIAN_PROD_MMBOED         = 1.0    # Surpassed 1 million boe/d, +12% YoY (Q4 2025)
PERMIAN_DJ_BAKKEN_KBOED     = 600    # Combined DJ Basin / Bakken production
TENGIZ_EXPANSION_ADDED_KBPD = 260    # Tengiz (Kazakhstan) expansion added ~260,000 b/d in 2025
COST_OF_SUPPLY_BBL          = 30     # Companywide breakeven — lowest in the industry (Motley Fool, Sept 2025)

# ── DIVIDEND & CAPITAL RETURNS ───────────────────────────────────────────────
DIV_YIELD_PCT               = 3.78
NET_DEBT_TO_CFFO            = 1.0
NET_DEBT_RATIO_PCT          = 15.6
BUYBACK_Q1_B                = 2.5
DIVIDEND_Q1_B               = 3.5

# ── ANALYST CONSENSUS ────────────────────────────────────────────────────────
EPS_FY2026E             = 13.86    # Consensus (range $8.33-$18.97 — wide commodity dispersion)
TRAILING_PE             = 32.8
FORWARD_PE              = 13.5
CONSENSUS_PT            = 216.0
PT_LOW                  = 170.0
PT_HIGH                 = 236.0
CONSENSUS_RATING        = "Buy"
ANALYST_RATING_NOTE     = "~18 Buy / 6 Hold / 1 Sell of ~25 analysts; consensus PT ~$216 implies ~13-15% upside"
REVENUE_FY2026E_B       = 210.2    # Revised up from ~$202.7B

# ── BEAR/BULL FRAMEWORK ANCHORS (from research) ─────────────────────────────
BEAR_OIL_SCENARIO_NOTE  = "EIA forecasts Brent falling to ~$89/bbl in Q4 2026 and ~$79/bbl in 2027 as Mideast supply normalizes — bear-case price near $149 (~21% downside from $187)"
BULL_OIL_SCENARIO_NOTE  = "Bull case keyed to Brent holding >$90/bbl through 2027 plus Hess synergies accelerating past the $4B aspiration — price target near $214 (top of consensus range)"

# ── SCENARIOS ────────────────────────────────────────────────────────────────
# BEAR  $145: A "lower for longer" oil environment (Brent grinds toward $79-89/bbl per EIA's
#             2026-27 path as Mideast supply normalizes); Hess integration stalls or proves
#             more costly than guided; multiple compresses toward 11-12× normalized earnings.
#             Roughly the 52-week-low zone ($140) — the ~$30/bbl cost-of-supply and IG
#             balance sheet (net debt/CFFO ~1.0x) mean the dividend is not at risk even here;
#             this is a price/multiple correction, not a solvency event.
#
# BASE  $205: Oil holds in a constructive ~$70-80/bbl range; Hess structural synergies land
#             at the high end of the $3-4B 2026 target; Permian holds >1 MMboe/d and Tengiz
#             output stabilizes at the higher post-expansion run-rate; Guyana (Yellowtail/
#             Hammerhead) ramps on schedule; dividend keeps growing (~5-6%/yr, Aristocrat
#             streak intact) and buybacks continue near the $2.5B/qtr pace. Roughly
#             "consensus PT $216" realized with a modest haircut for commodity uncertainty.
#
# BULL  $235: Hess synergies beat again (echoing the Pioneer/XOM "beat-and-raise" pattern) —
#             structural cuts exceed the $4B aspiration; Guyana net production via Hess's
#             Stabroek stake ramps faster than guided; Permian/Tengiz volumes keep growing;
#             Brent holds firmly >$85/bbl on continued underinvestment in new global supply;
#             multiple re-rates from "digesting a mega-deal" toward "structural growth major."
#
# XBULL $270: Full "Hess-supercharged supermajor" thesis — Guyana becomes a major net
#             contributor to group production, Hess structural + one-time synergies clear
#             $5B combined, Permian/Tengiz/DJ-Bakken all running above guidance, AND a
#             genuine oil supercycle (structural underinvestment + geopolitical supply
#             shocks push Brent toward $100+). Requires multiple structural tailwinds to
#             align simultaneously — the highest-conviction, lowest-probability outcome.
BEAR    = 145.0
BASE    = 205.0
BULL    = 235.0
XBULL   = 270.0

# ── EPP (EARNINGS POWER PRICE) ───────────────────────────────────────────────
# Trough scenario: a severe commodity downcycle (2015-16-style oil crash, or a 2020-COVID-
# style demand collapse) drags EPS down sharply even for the lowest-cost major. Trough PE
# reflects the modest premium CVX commands in panics — slightly above the 11-13× a typical
# major gets at the bottom, owing to its best-in-class cost-of-supply and IG balance sheet.
EPS_TROUGH  = 5.00
PE_TROUGH   = 13.5
EPP         = EPS_TROUGH * PE_TROUGH   # = $67.50

# ── SCA: STRUCTURAL COMPETITIVE ADVANTAGE ───────────────────────────────────
# CVX's moat rests on having the lowest cost-of-supply in the supermajor peer group
# (~$30/bbl companywide breakeven), an investment-grade balance sheet, a long capital-
# return track record, and — newly — the Hess/Guyana/Bakken/Malaysia asset base. The
# structural offsets are integration-execution risk on a $55B mega-deal and the same
# commodity price-taker exposure and energy-transition overhang every major carries.

SCA_FACTORS = {
    # Factor                                : (score,  weight)
    "integrated_supermajor_scale"           : (+0.30,  0.17),  # Top-3 US major; upstream-to-chemicals integration smooths cyclicality
    "hess_acquisition_execution"            : (+0.30,  0.16),  # $55B deal closed July 2025; synergies tracking AHEAD of schedule
    "lowest_cost_of_supply_in_industry"     : (+0.40,  0.17),  # ~$30/bbl companywide breakeven — best in the supermajor peer group
    "investment_grade_balance_sheet"        : (+0.30,  0.15),  # Net debt/CFFO ~1.0x, net debt ratio ~15.6%
    "capital_return_track_record"           : (+0.25,  0.15),  # Decades-long dividend growth streak (Aristocrat); ~$6B/qtr total returns
    "commodity_price_taker_exposure"        : (-0.30,  0.10),  # Cannot control its own realized price; 2025 net income fell ~30% on price normalization
    "secular_energy_transition_overhang"    : (-0.20,  0.10),  # Long-run secular demand/ESG headwind common to all integrated majors
}

SCA_NET  = sum(score * weight for score, weight in SCA_FACTORS.values())
# SCA_NET = 0.30×0.17 + 0.30×0.16 + 0.40×0.17 + 0.30×0.15 + 0.25×0.15 + (-0.30)×0.10 + (-0.20)×0.10
# SCA_NET ≈ 0.051 + 0.048 + 0.068 + 0.045 + 0.0375 - 0.03 - 0.02 = 0.1995

SCA_SCALE = 0.45  # Fixed framework parameter

# ── 6 PROXY SIGNALS ──────────────────────────────────────────────────────────
# Signal   (score 1–4, weight)
# 1=BEAR, 1.5=BEAR+, 2=BASE, 2.5=BASE+, 3=BULL, 3.5=BULL+, 4=XBULL

SIGNALS = {
    # The $55B Hess acquisition (closed July 2025) is running AHEAD of its synergy plan:
    # >$1.5B of a $2B structural cost-synergy target already realized by March 2026, with
    # $3-4B in structural cost cuts guided for year-end 2026 and management telling
    # employees the deal is "outperforming targets." This is the single biggest swing
    # factor in the bull case — and it's tracking better than guided, not worse.
    "hess_integration_synergy_beat": (3.5, 0.20),

    # Legacy organic growth firing on both cylinders: Permian Basin production has
    # surpassed 1 million boe/d (+12% YoY), the DJ Basin/Bakken add another ~600K boe/d,
    # and the Tengiz (Kazakhstan) expansion added ~260,000 b/d in 2025 — durable,
    # low-decline volume growth that doesn't depend on the Hess deal landing perfectly.
    "permian_tengiz_production_growth": (3.0, 0.18),

    # A genuine capital-return machine: $6.0B returned to shareholders in Q1 2026 alone
    # ($2.5B buybacks + $3.5B dividends), a ~3.8% yield, and a multi-decade dividend
    # growth streak (Dividend Aristocrat) — a durable compounding mechanism that does
    # not depend on the oil price cooperating in any given quarter.
    "capital_return_scale": (3.0, 0.16),

    # The honest near-term risk, laid bare in the numbers: FY2025 net income fell to
    # $12.3B from $17.7B (2024) and $21.4B (2023) as the 2025 oil-price spike normalized;
    # Q1 2026 EPS of $1.11 was roughly half of Q1 2025's $2.00. The EIA's own forecast
    # path (~$89/bbl Q4 2026, ~$79/bbl 2027) argues for continued earnings compression —
    # the market has to look through this "digestion year" to the structural growth case.
    "oil_price_normalization_and_earnings_reset_risk": (2.0, 0.18),

    # Genuinely the lowest-cost barrels in the supermajor peer group: ~$30/bbl companywide
    # breakeven, an investment-grade balance sheet (net debt/CFFO ~1.0x, net debt ratio
    # ~15.6%). This is what allows CVX to keep generating real free cash flow — and keep
    # raising the dividend — through a cycle that would force higher-cost peers to retrench.
    "lowest_cost_of_supply_balance_sheet": (3.5, 0.14),

    # A slow-burn but real source of optionality flowing in via Hess: first oil achieved
    # at Yellowtail (4th Stabroek development) and FID reached on Hammerhead (7th). Guyana
    # is arguably the best new offshore oil province discovered this century, and CVX now
    # owns a piece of it — an asset base the market has barely begun to price into CVX.
    "guyana_stabroek_optionality_via_hess": (2.5, 0.14),
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

# Conservative 2yr: FY2026E EPS (consensus) × a multiple BELOW the current ~33x trailing
# (and roughly in line with the ~13-14x forward) + 2yr dividends — pure compounding test,
# no heroic re-rating required
PE_CONSERVATIVE = 13.0
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
    print(f"  Net Income FY2025:  ${NET_INCOME_FY2025_B:.1f}B  (vs ${NET_INCOME_FY2024_B:.1f}B in 2024, ${NET_INCOME_FY2023_B:.1f}B in 2023 — sharp normalization)")
    print(f"  FCF FY2024:         ${FCF_FY2024_B:.1f}B   |   9M-2025 FCF: ${FCF_9M_FY2025_B:.1f}B")
    print(f"  2026 FCF target:    ${FCF_TARGET_FY2026_B:.1f}B (raised from $10B at Hess close)")
    print(f"  Incremental FCF:    ~${INCREMENTAL_FCF_AT_70BRENT_B:.0f}B/yr from legacy portfolio at $70 Brent (~${INCREMENTAL_FCF_AT_60BRENT_B:.0f}B at $60 Brent)")

    print(f"\n  Q1 2026 snapshot:")
    print(f"    Revenue ${Q1_REVENUE_B:.1f}B (vs ${Q1_REVENUE_B-1.0:.1f}B Q1'25) | Net income ${Q1_NET_INCOME_B:.2f}B (${Q1_DILUTED_EPS:.2f}/sh diluted)")
    print(f"    vs Q1 2025: net income ${Q1_2025_NET_INCOME_B:.2f}B (${Q1_2025_DILUTED_EPS:.2f}/sh) — earnings still under pressure as oil normalizes")
    print(f"    Total shareholder returns: ${Q1_TOTAL_RETURNS_B:.1f}B (${BUYBACK_Q1_B:.1f}B buybacks + ${DIVIDEND_Q1_B:.1f}B dividends)")

    print(f"\n{sep}")
    print("  THE HESS ACQUISITION — INTEGRATION RUNNING AHEAD OF PLAN")
    print(sep)
    print(f"  Deal: ${HESS_DEAL_SIZE_B:.0f}B, closed {HESS_CLOSE_DATE}  |  {HESS_ASSETS_NOTE}")
    print(f"  Synergies: >${HESS_STRUCTURAL_REALIZED_B:.1f}B of ${HESS_STRUCTURAL_TARGET_B:.1f}B structural target realized by March 2026 (orig. run-rate target was ${HESS_SYNERGY_TARGET_ORIGINAL_B:.1f}B)")
    print(f"  ${HESS_STRUCTURAL_CUTS_2026_LOW_B:.0f}-{HESS_STRUCTURAL_CUTS_2026_HIGH_B:.0f}B in structural cost cuts on track by year-end 2026  |  {HESS_CEO_QUOTE_NOTE}")
    print(f"  Guyana (Stabroek, via Hess): {GUYANA_YELLOWTAIL_STATUS}; {GUYANA_HAMMERHEAD_STATUS}")
    print(f"  {GUYANA_NOTE}")

    print(f"\n{sep}")
    print("  LEGACY UPSTREAM GROWTH — PERMIAN / TENGIZ")
    print(sep)
    print(f"  Permian: {PERMIAN_PROD_MMBOED:.1f} MMboe/d (surpassed, +12% YoY)  |  DJ Basin/Bakken: ~{PERMIAN_DJ_BAKKEN_KBOED:,}K boe/d combined")
    print(f"  Tengiz (Kazakhstan): expansion added ~{TENGIZ_EXPANSION_ADDED_KBPD:,} b/d in 2025")
    print(f"  Companywide cost-of-supply: ~${COST_OF_SUPPLY_BBL}/bbl — lowest breakeven in the supermajor peer group")

    print(f"\n{sep}")
    print("  CAPITAL RETURNS & BALANCE SHEET")
    print(sep)
    print(f"  Dividend yield: ~{DIV_YIELD_PCT:.2f}%  (${ANNUAL_DIV:.2f}/yr)  |  Q1 2026 total returns: ${Q1_TOTAL_RETURNS_B:.1f}B")
    print(f"  Net debt/CFFO: ~{NET_DEBT_TO_CFFO:.1f}x  |  Net debt ratio: ~{NET_DEBT_RATIO_PCT:.1f}%  — investment-grade, ample headroom through a cycle")

    print(f"\n{sep}")
    print("  ANALYST CONSENSUS")
    print(sep)
    print(f"  FY2026E EPS: ${EPS_FY2026E:.2f}  (range ${8.33:.2f}-${18.97:.2f})  |  Trailing P/E ~{TRAILING_PE:.1f}x, Forward P/E ~{FORWARD_PE:.1f}x")
    print(f"  Rating: {CONSENSUS_RATING}  |  Price targets: consensus ${CONSENSUS_PT:.0f} (range ${PT_LOW:.0f}-${PT_HIGH:.0f})")
    print(f"  {ANALYST_RATING_NOTE}")
    print(f"  2026E revenue: ~${REVENUE_FY2026E_B:.1f}B (revised up from ~$202.7B)")
    print(f"  Bear anchor: {BEAR_OIL_SCENARIO_NOTE}")
    print(f"  Bull anchor: {BULL_OIL_SCENARIO_NOTE}")

    print(f"\n{sep}")
    print("  6 PROXY SIGNALS")
    print(sep)
    labels = {
        "hess_integration_synergy_beat":                     "Hess integration synergy beat",
        "permian_tengiz_production_growth":                  "Permian / Tengiz production growth",
        "capital_return_scale":                              "Capital return scale",
        "oil_price_normalization_and_earnings_reset_risk":   "Oil price normalization / earnings reset risk",
        "lowest_cost_of_supply_balance_sheet":               "Lowest cost-of-supply / balance sheet",
        "guyana_stabroek_optionality_via_hess":              "Guyana / Stabroek optionality (via Hess)",
    }
    for k, (score, weight) in SIGNALS.items():
        bar = "█" * int(score * 5)
        print(f"  {labels[k]:<46}  {score:.1f}  wt={weight:.2f}  {bar}")
    print(f"  {'PROXY COMPOSITE':<46}  {PROXY_COMPOSITE:.2f}")

    print(f"\n{sep}")
    print("  SCA — STRUCTURAL COMPETITIVE ADVANTAGE")
    print(sep)
    sca_labels = {
        "integrated_supermajor_scale":        "Integrated supermajor scale",
        "hess_acquisition_execution":         "Hess acquisition execution",
        "lowest_cost_of_supply_in_industry":  "Lowest cost-of-supply in industry",
        "investment_grade_balance_sheet":     "Investment-grade balance sheet",
        "capital_return_track_record":        "Capital return track record",
        "commodity_price_taker_exposure":     "Commodity price-taker exposure",
        "secular_energy_transition_overhang": "Secular energy transition overhang",
    }
    for k, (score, weight) in SCA_FACTORS.items():
        print(f"  {sca_labels[k]:<46}  {score:+.2f} × {weight:.2f} = {score*weight:+.4f}")
    print(f"  {'SCA_NET':<46}  {SCA_NET:+.4f}")
    print(f"  ADJ contribution (+0.45 × SCA_NET × 0.5): {SCA_SCALE * SCA_NET * 0.5:+.4f}")

    print(f"\n{sep}")
    print("  COMPOSITE SCORES")
    print(sep)
    print(f"  PROXY_COMPOSITE:    {PROXY_COMPOSITE:.4f}")
    print(f"  ADJ_COMPOSITE:      {ADJ_COMPOSITE:.4f}")
    print(f"  MARKET_COMPOSITE:   {MARKET_COMPOSITE:.4f}  (back-solved from ${CURRENT_PRICE}×1.15²=${TARGET_MARKET:.2f})")
    print(f"  ADJ_VS_MARKET:      {ADJ_VS_MARKET:+.4f}  → {'SIGNIFICANTLY UNDERVALUED' if ADJ_VS_MARKET > 0.5 else 'MODESTLY UNDERVALUED' if ADJ_VS_MARKET > 0.1 else 'FAIRLY VALUED'}")

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
    print(f"  FY2026E EPS (consensus):           ${EPS_FY2026E:.2f}")
    print(f"  Conservative PE applied:           {PE_CONSERVATIVE:.1f}× (below the ~33x trailing multiple, roughly in line with the ~13-14x forward)")
    print(f"  Target price 2yr:                  ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.1f}× + ${2*ANNUAL_DIV:.2f} div = ${PRICE_2YR_CONSV:.2f}")
    print(f"  2-year return:                     {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  Note: this is the 'multiple stays roughly where the forward P/E already implies' floor case —")
    print(f"  BASE/BULL diverge as Hess synergies/Guyana/Permian/Tengiz growth re-rate the multiple higher.")

    print(f"\n{sep}")
    print("  WHY THIS IS AN ◎ ACCUMULATE, NOT A ◉ BUY OR ✕ AVOID")
    print(sep)
    print("""
  Chevron is the lowest-cost integrated major in the business, trading at $187 — well
  above its 52-week low of $140 and roughly 65% of the way up its 52-week range. This is
  NOT a deep-value dislocation; it is a high-quality compounder digesting a transformative
  $55B acquisition that, so far, is running ahead of plan.

  WHAT THE MARKET ALREADY PRICES IN (at $187, well off the 52-week low):
  • Hess integration completes on a normal timeline, with synergies landing inside guidance
  • Permian holds >1 MMboe/d and Tengiz stabilizes near its post-expansion run-rate
  • Capital returns continue at the current ~$6B/quarter pace (dividend + buybacks)
  • Guyana (via Hess) remains a "still ramping" story — not yet a major group contributor

  WHAT COULD MAKE THIS MORE THAN FAIRLY PRICED:
  1. Hess synergies beat AGAIN — the pattern so far ($1.5B of $2B realized well ahead of
     schedule, CEO calling the deal "outperforming targets") echoes the Pioneer/XOM
     "beat-and-raise" playbook seen elsewhere in recent energy M&A
  2. Guyana (Yellowtail/Hammerhead, now flowing through Hess) ramps faster than guided and
     the market starts crediting genuinely new barrels not in today's base numbers
  3. Permian (>1 MMboe/d) and Tengiz (+260K b/d in 2025) keep compounding at low decline
     rates, widening CVX's already-best-in-class ~$30/bbl cost-of-supply advantage
  4. Oil holds in a constructive $80+ range (vs. the EIA's softer $79-89/bbl 2026-27 path)
     on continued underinvestment in new global supply — re-rating the multiple toward 16-17x

  THE RISK:
  • CVX remains fundamentally a commodity price-taker — FY2025 net income already fell
    from $17.7B to $12.3B as 2025's oil-price spike normalized, and Q1 2026 EPS of $1.11
    was roughly HALF of Q1 2025's $2.00; the EIA's own forecast (Brent ~$89 in Q4'26,
    ~$79 in 2027) argues for continued near-term earnings compression
  • A $55B acquisition carries real integration-execution risk — "outperforming targets"
    in month eight is encouraging, but mega-deals can still surprise to the downside later
  • The trailing P/E (~33x) looks rich at first glance — though this largely reflects
    temporarily depressed trailing earnings rather than a genuinely expensive multiple
    (forward P/E is a much more reasonable ~13-14x)
  • The long-run secular energy-transition overhang is real, as it is for every major

  WHAT MAKES THE DOWNSIDE GENUINELY MANAGEABLE (why this isn't a coin-flip):
  • The lowest cost-of-supply in the supermajor peer group (~$30/bbl companywide breakeven)
    means CVX keeps generating real free cash flow at price levels that would force
    higher-cost peers into retrenchment — and an investment-grade balance sheet (net
    debt/CFFO ~1.0x, net debt ratio ~15.6%) means even a real downturn here is a
    multiple-compression event, not a solvency event
  • A ~3.8% dividend yield, backed by a multi-decade growth streak (Dividend Aristocrat),
    provides a real income floor while the Hess thesis plays out

  POSITION SIZING GUIDANCE:
  • This is a "own the lowest-cost integrated major and let Hess/Permian/Tengiz/Guyana
    compound" name — appropriate as a core energy holding, sized for genuine commodity beta
  • Add on weakness toward $155-165 (where Ratio B moves toward BUY territory and the
    yield approaches ~4.3-4.6%)
  • Hess synergies clearing the $2B structural target — and Guyana volumes showing up in
    the group production numbers — are the catalysts that should re-rate this from
    "digesting a mega-deal" to "structurally compounding low-cost supermajor"
""")

    print(SEP)
    print(f"""
SUMMARY: CVX ◎ ACCUMULATE — Ratio B 0.89× (22.6% downside / 25.5% upside). LOWEST-COST \
SUPERMAJOR DIGESTING A MEGA-DEAL THAT'S RUNNING AHEAD OF PLAN: trading at $187 (52-wk range \
$140-215, well off the lows) on the back of the ~$55B Hess acquisition (closed July 2025) \
already realizing >$1.5B of its $2B structural synergy target — well ahead of schedule, with \
the CEO calling it 'outperforming targets' — plus first oil at Yellowtail and FID on \
Hammerhead (Stabroek/Guyana, via Hess). LEGACY GROWTH FIRING ON BOTH CYLINDERS: Permian \
surpassed 1 MMboe/d (+12% YoY), Tengiz expansion added ~260K b/d in 2025, all running at the \
lowest cost-of-supply (~$30/bbl breakeven) in the supermajor peer group. CAPITAL RETURN \
MACHINE: $6.0B returned to shareholders in Q1 2026 alone ($2.5B buybacks + $3.5B dividends, \
~3.8% yield, multi-decade Dividend Aristocrat streak) on an investment-grade balance sheet \
(net debt/CFFO ~1.0x). THE HONEST RISK: FY2025 net income fell to $12.3B from $17.7B (2024) \
as the 2025 oil-price spike normalized — Q1 2026 EPS $1.11 was roughly half of Q1 2025's \
$2.00, and the EIA sees Brent drifting toward $79-89/bbl through 2027. Consensus PT $216 \
(range $170-236; ~18 Buy / 6 Hold / 1 Sell of ~25 analysts). Conservative 2yr (multiple- \
roughly-flat floor case): EPS $13.86 x 13x + $14.24 div = $194.42 -> +3.8% — BASE/BULL diverge \
as Hess/Guyana/Permian/Tengiz growth materializes and the multiple re-rates. Lowest cost-of- \
supply + IG balance sheet make the downside genuinely manageable — add on weakness toward \
$155-165. Bear $145 · Base $205 · Bull $235 · XBull $270.
""")

    print(f"SIGNAL: {SIGNAL_TEXT} (lowest cost-of-supply supermajor + Hess integration beating plan, Guyana/Permian/Tengiz growth) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
