"""
ExxonMobil Corporation (NYSE: XOM)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.84×  |  EPP Gap: +259.9%

THE FORTRESS SUPERMAJOR — GUYANA + PERMIAN GROWTH ENGINE, AA- BALANCE SHEET, COMPOUNDING MACHINE
Trading at $151 (52-week range $103–176, roughly mid-range) on:
  (1) Guyana ramping to a record >900,000 boe/d gross (XOM's 45% stake ≈ 405,000 boe/d net) —
      arguably the best new oil province discovered this century, at sub-$35/bbl breakevens
  (2) Pioneer Natural Resources integration delivering >$3B/yr synergies (50%+ above original
      guidance), with the combined Permian business growing 2.5× faster than pre-deal and
      guided toward 2.3 MMboe/d by 2030
  (3) Best-in-class balance sheet (AA-/Aa2, ~$17B net debt) funding a 43-year dividend growth
      streak ($4.12/yr, ~2.7% yield) plus ~$20B/yr buybacks — $9.2B returned to shareholders
      in Q1 2026 alone, against a payout of only ~31% of free cash flow

At $151 the stock sits roughly mid-range, with 2026 guidance calling for earnings "roughly
flat" as the 2025 oil-price spike (briefly >$110/bbl) normalizes — before Guyana, Permian,
Golden Pass LNG and the China chemicals complex re-accelerate growth into 2027-2028. This is
a "own the best balance sheet in the sector and let Guyana/Permian compound" name, not a
deep-value dislocation — but Ratio B sits just inside ACCUMULATE territory because the
downside is genuinely cushioned (fortress balance sheet, 31%-of-FCF payout, irreplaceable
low-cost barrels) while the upside (Guyana ramp + Pioneer synergy beats + capital
return machine) is real and underwritten by execution already in hand, not narrative.

Conviction: MODERATE-HIGH on the base case (steady compounding through dividend growth +
buybacks + Guyana/Permian volume ramp); HIGHER on the multi-year structural growth runway
(Guyana, Golden Pass, China chemicals, Pioneer 2.3 MMboe/d 2030 target) that the market is
not yet fully crediting at a "flat 2026" guide.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "XOM"
COMPANY         = "ExxonMobil Corporation"
SECTOR          = "Integrated Oil & Gas · Upstream (Permian/Pioneer, Guyana) · Downstream & Chemicals · Low Carbon Solutions · NYSE: XOM"
SECTOR_GROUP    = "Energy"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 151.17   # June 5, 2026
ANNUAL_DIV      = 4.12     # $1.03/quarter
SHARES_OUT_B    = 6.0      # ~6.0B shares (down from ~6.4B pre-buybacks)
MARKET_CAP_B    = 907.0    # CURRENT_PRICE × SHARES_OUT_B
FW52_HIGH       = 176.41
FW52_LOW        = 102.68

# ── FY2025 FULL-YEAR FINANCIALS ─────────────────────────────────────────────
REVENUE_FY2025_B          = 332.0
ADJ_NET_INCOME_FY2025_B   = 45.0
ADJ_EPS_FY2025            = 7.50
GAAP_NET_INCOME_FY2025_B  = 40.8
GAAP_EPS_FY2025           = 6.80
FCF_FY2025_B              = 26.1
DIVIDENDS_PAID_FY2025_B   = 17.2
PAYOUT_PCT_OF_FCF         = 31     # Dividend = only ~31% of FCF — huge coverage cushion
STRUCTURAL_SAVINGS_CUM_B  = 15.1   # Cumulative structural cost savings since 2019
STRUCTURAL_SAVINGS_TARGET_2030_B = 20

# ── Q1 2026 SNAPSHOT ─────────────────────────────────────────────────────────
Q1_REVENUE_B            = 85.1     # +5% YoY
Q1_GAAP_NET_INCOME_B    = 4.2
Q1_GAAP_EPS             = 1.00
Q1_ADJ_EPS              = 1.16     # Beat consensus $1.0074 by ~15%
Q1_DERIVATIVE_LOSS_B    = 3.88     # Mark-to-market derivative loss distorting GAAP earnings
Q1_MIDEAST_DISRUPTION_M = 706      # One-off Mideast operational disruption charge
Q1_FCF_B                = 2.7
Q1_OCF_B                = 8.7
Q4_2025_FCF_B           = 5.6

# ── DIVIDEND & CAPITAL RETURNS ───────────────────────────────────────────────
QUARTERLY_DIV           = 1.03
DIV_STREAK_YEARS        = 43       # On track for "Dividend King" (50 yrs) ~early 2030s
BUYBACK_ANNUAL_PACE_B   = 20       # ~$20B/yr pace continuing into 2026 (from $20B in 2025)
Q1_2026_TOTAL_RETURNS_B = 9.2
Q1_2026_DIV_B           = 4.3
Q1_2026_BUYBACK_B       = 4.9

# ── BALANCE SHEET ────────────────────────────────────────────────────────────
TOTAL_DEBT_B            = 42.0     # $9.2B short-term + $32.8B long-term
CASH_B                  = 25.0
NET_DEBT_B              = 17.0
TOTAL_ASSETS_B          = 449.0
TOTAL_EQUITY_B          = 259.0
CREDIT_RATING_SP        = "AA-"
CREDIT_RATING_MOODYS    = "Aa2"
RATING_NOTE             = "Among the strongest balance sheets of any oil major — both ratings affirmed post-Pioneer (2024)"

# ── UPSTREAM GROWTH: GUYANA ──────────────────────────────────────────────────
GUYANA_GROSS_PROD_KBOED = 900      # Record gross production, Q1 2026 (Stabroek block)
XOM_GUYANA_STAKE_PCT    = 45
XOM_GUYANA_NET_KBOED    = 405      # XOM's attributable net production
GUYANA_BREAKEVEN_BBL    = 35       # Sub-$35/bbl breakeven — among lowest-cost barrels globally
GUYANA_VESSELS_OPERATING = 4       # FPSOs operating/ramping (Liza, Liza Unity, Prosperity, ONE GUYANA)

# ── UPSTREAM GROWTH: PERMIAN / PIONEER INTEGRATION ──────────────────────────
PIONEER_DEAL_CLOSE      = "May 2024"
PIONEER_SYNERGY_TARGET_ORIGINAL_B = 2.0
PIONEER_SYNERGY_REALIZED_B        = 3.0   # >$3B/yr — 50%+ above original guidance
PERMIAN_GROWTH_MULTIPLE = 2.5      # Combined entity growing at 2.5× pre-Pioneer pace
PERMIAN_2030_TARGET_MMBOED = 2.3   # Guided production target by 2030

# ── DOWNSTREAM / GROWTH PROJECTS (2027-2028 RAMP) ───────────────────────────
GOLDEN_PASS_LNG_STATUS  = "Under construction; first LNG expected 2027 — ~18 MTPA capacity (XOM 30% stake via joint venture)"
CHINA_CHEMICAL_COMPLEX_STATUS = "Huizhou, Guangdong — large-scale petrochemical complex ramping 2027-2028"
PLAN_2030_NOTE          = "'2030 Plan' raised Dec 2025: 2026 earnings guided roughly FLAT (post normalization off the ~$110/bbl 2025 spike), reaccelerating 2027-28 as Guyana/Permian/Golden Pass/China chemicals ramp"

# ── VENEZUELA / GEOPOLITICAL ─────────────────────────────────────────────────
VENEZUELA_FIELDS_IN_TALKS    = 6
VENEZUELA_COMPENSATION_OWED_B = 1.0   # Court-ordered compensation still owed to XOM
VENEZUELA_STATUS             = "Advanced talks to regain rights to up to six Venezuelan oil fields — slow-moving optionality, not yet in consensus numbers"

# ── ANALYST CONSENSUS ────────────────────────────────────────────────────────
EPS_FY2026E             = 7.55     # Roughly flat vs FY2025 per management's own "flat 2026" guide
CONSENSUS_PT            = 165.0
PT_LOW                  = 130.0
PT_HIGH                 = 185.0
CONSENSUS_RATING        = "Moderate Buy / Buy"
ANALYST_RATING_NOTE     = "Argus raised target to $169 (May 2026) citing Permian/Guyana strength; consensus average ~$162-170"

# ── 2020 COVID TROUGH (HISTORICAL ANCHOR) ───────────────────────────────────
COVID_LOW_PRICE         = 30.11    # March 23, 2020 — stock fell ~41% in 2020
COVID_LOW_DATE          = "March 23, 2020"
COVID_DEBT_PEAK_B       = 68.8     # Debt ballooned from $47.1B (Q3-19) as dividend was maintained through the shortfall

# ── SCENARIOS ────────────────────────────────────────────────────────────────
# BEAR  $110: Oil price collapse (WTI sub-$50, OPEC+ share war or demand-shock recession);
#             "flat 2026" guidance proves optimistic as the 2025 spike fully reverses;
#             Guyana/Permian volumes still grow but at depressed realizations; multiple
#             compresses toward 10-11×. Even here, the AA- balance sheet (net debt $17B,
#             payout only 31% of FCF) means the dividend is NOT at risk — this is a price/
#             multiple correction, not a solvency event (unlike 2020, when debt ballooned
#             to $68.8B). Roughly the 52-week-low zone.
#
# BASE  $165: Consensus realized — oil normalizes to a constructive $65-75/bbl range;
#             Guyana net production grows toward ~450-500K boe/d; Pioneer synergies hold
#             at ~$3B/yr; dividend keeps growing (~4-5%/yr) and buybacks continue at
#             ~$20B/yr; "flat 2026" gives way to renewed growth in 2027 as Golden Pass
#             LNG and China chemicals begin contributing. Essentially "consensus PT $165"
#             realized plus modest drift.
#
# BULL  $200: Guyana ramps faster than guided (5th+ FPSO sanctioned, net production
#             pushing toward 600K+ boe/d); Permian synergies beat again (as DCP-style
#             beats have become the pattern across the sector); Golden Pass LNG and
#             China chemicals come online on schedule and contribute meaningfully;
#             oil holds in an $80+ structurally tight range on continued underinvestment
#             in new supply; multiple re-rates toward 16-17× on de-risked growth visibility.
#
# XBULL $240: Full "fortress supermajor" thesis — Guyana becomes a >700K boe/d cash
#             machine, Pioneer integration pushes Permian past the 2.3 MMboe/d 2030
#             target early, Venezuela talks yield access to new low-cost fields plus
#             the ~$1B compensation recovery, AND a genuine oil supercycle (structural
#             underinvestment + geopolitical supply shocks push WTI toward $100+).
#             Requires multiple structural tailwinds to align simultaneously — the
#             highest-conviction, lowest-probability outcome.
BEAR    = 110.0
BASE    = 165.0
BULL    = 200.0
XBULL   = 240.0

# ── EPP (EARNINGS POWER PRICE) ───────────────────────────────────────────────
# Trough scenario: a severe commodity downcycle (2015-16-style oil crash, or a 2020-COVID-
# style demand collapse) drags adjusted EPS down sharply even for the best-capitalized major.
# Trough PE reflects the modest premium XOM commands over peers in panics — the market's
# perceived "flight to quality" within the sector (best balance sheet, lowest leverage,
# longest dividend streak) — slightly above the 11-13× a typical major gets at the bottom.
EPS_TROUGH  = 3.00
PE_TROUGH   = 14.0
EPP         = EPS_TROUGH * PE_TROUGH   # = $42.00

# ── SCA: STRUCTURAL COMPETITIVE ADVANTAGE ───────────────────────────────────
# XOM's moat rests on scale + integration (upstream-to-chemicals), the best balance sheet
# of any major (AA-/Aa2), and genuinely irreplaceable low-cost growth assets (Guyana,
# Permian post-Pioneer). The structural offset is that it remains fundamentally a
# commodity price-taker, plus the long-run secular energy-transition overhang.

SCA_FACTORS = {
    # Factor                              : (score,  weight)
    "integrated_supermajor_scale"         : (+0.35,  0.18),  # Largest US major; upstream-to-chemicals integration smooths cyclicality
    "guyana_world_class_low_cost_basin"   : (+0.40,  0.18),  # Sub-$35/bbl breakevens, 45% of arguably the best new basin this century
    "pioneer_permian_integration"         : (+0.30,  0.15),  # Synergies running 50%+ above guidance; 2.3 MMboe/d 2030 target
    "fortress_balance_sheet"              : (+0.30,  0.15),  # AA-/Aa2 — strongest of any major; net debt only $17B
    "capital_return_track_record"         : (+0.25,  0.15),  # 43-yr dividend growth streak + ~$20B/yr buybacks; payout 31% of FCF
    "commodity_price_taker_exposure"      : (-0.30,  0.10),  # Fundamentally cannot control its own realized price; GAAP swings on derivatives/oil
    "secular_energy_transition_overhang"  : (-0.20,  0.09),  # Long-run demand/ESG headwind to traditional E&P; Low Carbon bets unproven at scale
}

SCA_NET  = sum(score * weight for score, weight in SCA_FACTORS.values())
# SCA_NET = 0.35×0.18 + 0.40×0.18 + 0.30×0.15 + 0.30×0.15 + 0.25×0.15 + (-0.30)×0.10 + (-0.20)×0.09
# SCA_NET ≈ 0.063 + 0.072 + 0.045 + 0.045 + 0.0375 - 0.03 - 0.018 = 0.2145

SCA_SCALE = 0.45  # Fixed framework parameter

# ── 6 PROXY SIGNALS ──────────────────────────────────────────────────────────
# Signal   (score 1–4, weight)
# 1=BEAR, 1.5=BEAR+, 2=BASE, 2.5=BASE+, 3=BULL, 3.5=BULL+, 4=XBULL

SIGNALS = {
    # Record gross production >900K boe/d (XOM net ~405K boe/d at 45%) on sub-$35/bbl
    # breakeven barrels — arguably the best new offshore oil province discovered this
    # century. Four FPSOs operating/ramping (Liza, Liza Unity, Prosperity, ONE GUYANA),
    # with more sanctioned. This is THE structural growth engine the market is still
    # under-crediting relative to a "flat 2026" headline guide.
    "guyana_production_ramp": (3.5, 0.20),

    # Pioneer Natural Resources integration delivering >$3B/yr synergies — 50%+ above
    # the original ~$2B guidance — with the combined Permian business growing at 2.5×
    # the pre-deal pace and a 2030 target of 2.3 MMboe/d. The DCP-style "beat-and-raise"
    # synergy pattern that has become a hallmark of well-executed energy M&A.
    "pioneer_permian_synergy_realization": (3.5, 0.18),

    # Best-in-class capital returns: 43-year dividend growth streak ($4.12/yr, ~2.7%
    # yield, on track for "Dividend King" status ~2030), ~$20B/yr buyback pace, $9.2B
    # total shareholder returns in Q1 2026 alone — and a payout of only ~31% of FCF,
    # leaving enormous coverage cushion through any cycle. A durable compounding
    # mechanism that does not depend on the oil price cooperating.
    "capital_return_compounding_machine": (3.0, 0.18),

    # The honest near-term risk: 2026 guidance calls for earnings roughly FLAT as the
    # 2025 oil-price spike (briefly >$110/bbl) normalizes, and Q1 2026 GAAP earnings
    # were distorted by a $3.88B mark-to-market derivative loss plus a $706M Mideast
    # disruption charge. The market has to look through near-term GAAP noise to the
    # underlying growth ramp — a real source of multiple compression risk if it doesn't.
    "oil_price_normalization_and_gaap_noise_risk": (2.0, 0.18),

    # Genuinely the strongest balance sheet of any oil major: AA- (S&P) / Aa2 (Moody's),
    # ~$17B net debt against ~$259B equity, ~1.7× financial leverage. This is what
    # allowed XOM to keep raising its dividend straight through the 2020 COVID collapse
    # (when debt ballooned to $68.8B) — the downside in this name is a price/multiple
    # correction, not a solvency event, which materially de-risks the BEAR scenario.
    "fortress_balance_sheet_lowest_leverage": (3.5, 0.13),

    # A slow-moving but real source of optionality: advanced talks to regain rights to
    # up to six Venezuelan oil fields, plus recovery of the ~$1B in court-ordered
    # compensation still owed. Not yet in consensus numbers — a genuine (if uncertain
    # and politically fraught) call option that could meaningfully expand the resource
    # base if it resolves favorably.
    "venezuela_geopolitical_optionality": (2.0, 0.13),
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

# Conservative 2yr: EPS FY2026E (management's own "flat 2026" guide) × modest PE +
# 2yr dividends (no heroic multiple expansion — pure compounding test)
PE_CONSERVATIVE = 18.0
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
    print(f"  Revenue:           ${REVENUE_FY2025_B:.1f}B")
    print(f"  Adj. Net Income:   ${ADJ_NET_INCOME_FY2025_B:.1f}B  (${ADJ_EPS_FY2025:.2f}/sh)")
    print(f"  GAAP Net Income:   ${GAAP_NET_INCOME_FY2025_B:.1f}B  (${GAAP_EPS_FY2025:.2f}/sh)")
    print(f"  Free Cash Flow:    ${FCF_FY2025_B:.1f}B   |   Dividends paid ${DIVIDENDS_PAID_FY2025_B:.1f}B = only {PAYOUT_PCT_OF_FCF}% of FCF (huge cushion)")
    print(f"  Structural cost savings: ${STRUCTURAL_SAVINGS_CUM_B:.1f}B cumulative since 2019 (targeting ${STRUCTURAL_SAVINGS_TARGET_2030_B}B by 2030)")

    print(f"\n  Q1 2026 snapshot:")
    print(f"    Revenue ${Q1_REVENUE_B:.1f}B (+5% YoY) | GAAP net income ${Q1_GAAP_NET_INCOME_B:.1f}B (${Q1_GAAP_EPS:.2f}/sh) | Adj. EPS ${Q1_ADJ_EPS:.2f} (beat consensus by ~15%)")
    print(f"    GAAP distorted by ${Q1_DERIVATIVE_LOSS_B:.2f}B mark-to-market derivative loss + ${Q1_MIDEAST_DISRUPTION_M}mm Mideast disruption charge")
    print(f"    OCF ${Q1_OCF_B:.1f}B | FCF ${Q1_FCF_B:.1f}B (vs ${Q4_2025_FCF_B:.1f}B in Q4 2025)")

    print(f"\n{sep}")
    print("  BALANCE SHEET — THE FORTRESS")
    print(sep)
    print(f"  Total Debt: ${TOTAL_DEBT_B:.1f}B  |  Cash: ${CASH_B:.1f}B  |  Net Debt: ${NET_DEBT_B:.1f}B")
    print(f"  Total Assets ${TOTAL_ASSETS_B:.0f}B / Equity ${TOTAL_EQUITY_B:.0f}B  →  ~{TOTAL_ASSETS_B/TOTAL_EQUITY_B:.2f}× financial leverage")
    print(f"  Credit Ratings: {CREDIT_RATING_SP} (S&P) / {CREDIT_RATING_MOODYS} (Moody's) — {RATING_NOTE}")
    print(f"  2020 COVID stress test: stock fell to ${COVID_LOW_PRICE:.2f} ({COVID_LOW_DATE}); debt peaked at ${COVID_DEBT_PEAK_B:.1f}B —")
    print(f"    yet the dividend was MAINTAINED and grown straight through. Today's balance sheet is far stronger.")

    print(f"\n{sep}")
    print("  CAPITAL RETURNS — THE COMPOUNDING MACHINE")
    print(sep)
    print(f"  Dividend: ${QUARTERLY_DIV:.2f}/qtr (${ANNUAL_DIV:.2f}/yr) — yield ~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}%  |  {DIV_STREAK_YEARS}-year growth streak (Dividend Aristocrat → 'King' ~2030)")
    print(f"  Buybacks: ~${BUYBACK_ANNUAL_PACE_B}B/yr pace  |  Q1 2026 total shareholder returns: ${Q1_2026_TOTAL_RETURNS_B:.1f}B (${Q1_2026_DIV_B:.1f}B div + ${Q1_2026_BUYBACK_B:.1f}B buybacks)")

    print(f"\n{sep}")
    print("  UPSTREAM GROWTH ENGINE #1 — GUYANA (STABROEK BLOCK)")
    print(sep)
    print(f"  Gross production: {GUYANA_GROSS_PROD_KBOED:,}K boe/d (record, Q1 2026)  |  XOM net ({XOM_GUYANA_STAKE_PCT}% stake): ~{XOM_GUYANA_NET_KBOED:,}K boe/d")
    print(f"  Breakeven: sub-${GUYANA_BREAKEVEN_BBL}/bbl — among the lowest-cost barrels in the world")
    print(f"  {GUYANA_VESSELS_OPERATING} FPSOs operating/ramping (Liza, Liza Unity, Prosperity, ONE GUYANA) — more sanctioned")

    print(f"\n{sep}")
    print("  UPSTREAM GROWTH ENGINE #2 — PERMIAN / PIONEER INTEGRATION")
    print(sep)
    print(f"  Deal closed {PIONEER_DEAL_CLOSE}  |  Synergies: ${PIONEER_SYNERGY_REALIZED_B:.1f}B/yr realized vs ${PIONEER_SYNERGY_TARGET_ORIGINAL_B:.1f}B original target (+{(PIONEER_SYNERGY_REALIZED_B/PIONEER_SYNERGY_TARGET_ORIGINAL_B-1)*100:.0f}% beat)")
    print(f"  Combined Permian business growing at {PERMIAN_GROWTH_MULTIPLE:.1f}× the pre-Pioneer pace  →  2030 target: {PERMIAN_2030_TARGET_MMBOED:.1f} MMboe/d")

    print(f"\n{sep}")
    print("  2027-2028 GROWTH RAMP & GEOPOLITICAL OPTIONALITY")
    print(sep)
    print(f"  Golden Pass LNG:        {GOLDEN_PASS_LNG_STATUS}")
    print(f"  China chemicals:        {CHINA_CHEMICAL_COMPLEX_STATUS}")
    print(f"  '2030 Plan':            {PLAN_2030_NOTE}")
    print(f"  Venezuela:              {VENEZUELA_STATUS}")
    print(f"                          (~{VENEZUELA_FIELDS_IN_TALKS} fields in talks; ~${VENEZUELA_COMPENSATION_OWED_B:.1f}B compensation still owed)")

    print(f"\n{sep}")
    print("  ANALYST CONSENSUS")
    print(sep)
    print(f"  FY2026E EPS: ${EPS_FY2026E:.2f}  |  Rating: {CONSENSUS_RATING}")
    print(f"  Price targets: consensus ${CONSENSUS_PT:.2f} (range ${PT_LOW:.0f}-${PT_HIGH:.0f})")
    print(f"  {ANALYST_RATING_NOTE}")

    print(f"\n{sep}")
    print("  6 PROXY SIGNALS")
    print(sep)
    labels = {
        "guyana_production_ramp":                       "Guyana production ramp",
        "pioneer_permian_synergy_realization":          "Pioneer/Permian synergy realization",
        "capital_return_compounding_machine":           "Capital return compounding machine",
        "oil_price_normalization_and_gaap_noise_risk":  "Oil price normalization / GAAP noise risk",
        "fortress_balance_sheet_lowest_leverage":       "Fortress balance sheet (lowest leverage)",
        "venezuela_geopolitical_optionality":           "Venezuela geopolitical optionality",
    }
    for k, (score, weight) in SIGNALS.items():
        bar = "█" * int(score * 5)
        print(f"  {labels[k]:<42}  {score:.1f}  wt={weight:.2f}  {bar}")
    print(f"  {'PROXY COMPOSITE':<42}  {PROXY_COMPOSITE:.2f}")

    print(f"\n{sep}")
    print("  SCA — STRUCTURAL COMPETITIVE ADVANTAGE")
    print(sep)
    sca_labels = {
        "integrated_supermajor_scale":        "Integrated supermajor scale",
        "guyana_world_class_low_cost_basin":  "Guyana world-class low-cost basin",
        "pioneer_permian_integration":        "Pioneer / Permian integration",
        "fortress_balance_sheet":             "Fortress balance sheet (AA-/Aa2)",
        "capital_return_track_record":        "Capital return track record (43yr)",
        "commodity_price_taker_exposure":     "Commodity price-taker exposure",
        "secular_energy_transition_overhang": "Secular energy transition overhang",
    }
    for k, (score, weight) in SCA_FACTORS.items():
        print(f"  {sca_labels[k]:<42}  {score:+.2f} × {weight:.2f} = {score*weight:+.4f}")
    print(f"  {'SCA_NET':<42}  {SCA_NET:+.4f}")
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
    print(f"  FY2026E EPS (mgmt 'flat 2026' guide): ${EPS_FY2026E:.2f}")
    print(f"  Conservative PE applied:              {PE_CONSERVATIVE:.1f}× (modest premium reflecting de-risked Guyana/Permian growth visibility)")
    print(f"  Target price 2yr:                     ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.1f}× + ${2*ANNUAL_DIV:.2f} div = ${PRICE_2YR_CONSV:.2f}")
    print(f"  2-year return:                        {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  Note: this is the PURE 'flat 2026' compounding test — no credit for Guyana/Permian/Golden Pass")
    print(f"  ramping into 2027-28, which is where the BASE/BULL scenarios diverge from this floor case.")

    print(f"\n{sep}")
    print("  WHY THIS IS AN ◎ ACCUMULATE, NOT A ◉ BUY OR ✕ AVOID")
    print(sep)
    print("""
  ExxonMobil is the highest-quality balance sheet in the energy sector trading at
  roughly the MID-POINT of its 52-week range — not a deep-value dislocation, and not
  an expensive momentum name either.

  WHAT THE MARKET ALREADY PRICES IN (at $151, ~mid-range):
  • Oil normalizes off the 2025 spike; 2026 earnings come in roughly flat (per guidance)
  • Guyana and Permian keep growing at a steady, unspectacular pace
  • Capital returns continue compounding (dividend growth + ~$20B/yr buybacks)
  • Golden Pass LNG / China chemicals are a 2027-28 story, not yet in the 2026 numbers

  WHAT COULD MAKE THIS MORE THAN FAIRLY PRICED:
  1. Guyana keeps beating its own ramp schedule — gross production already at a record
     >900K boe/d with more FPSOs sanctioned; net 405K boe/d could approach 600K+ by 2028
  2. Pioneer integration synergies keep beating guidance (already +50% above the original
     target) — the same "beat-and-raise" pattern other recent energy M&A has shown
  3. Golden Pass LNG and the China chemicals complex come online on schedule (2027) and
     the market starts crediting the 2027-28 reacceleration BEFORE it shows up in the print
  4. Venezuela talks resolve favorably — up to 6 fields plus ~$1B compensation recovery
     would be a genuine, uncredited expansion of the resource base

  THE RISK:
  • XOM remains fundamentally a commodity price-taker — a sustained oil price collapse
    (OPEC+ share war, demand-shock recession) compresses earnings and the multiple
  • Q1 2026 GAAP earnings were distorted by a $3.88B derivative mark-to-market loss —
    a reminder that headline numbers can swing sharply independent of operational reality
  • The long-run secular energy-transition overhang is real, even if XOM is better
    positioned than peers (lower-cost barrels, Low Carbon Solutions optionality)
  • "Flat 2026" guidance means the next 12 months may simply be a digestion period —
    patience is required for the 2027-28 growth ramp to show up in the numbers

  WHAT MAKES THE DOWNSIDE GENUINELY CUSHIONED (why this isn't a coin-flip):
  • AA-/Aa2 — net debt of just $17B against $259B of equity. Even in 2020 (COVID demand
    collapse, debt ballooned to $68.8B), XOM kept raising its dividend. Today's balance
    sheet is dramatically stronger. The downside here is a PRICE correction, not a
    SOLVENCY event — which is precisely what keeps Ratio B inside ACCUMULATE territory
    despite the stock sitting mid-range rather than near a 52-week low.

  POSITION SIZING GUIDANCE:
  • This is a "own the best balance sheet in the sector and let Guyana/Permian compound"
    name — a core long-term holding, not a leveraged cyclical trade
  • Add on weakness toward $130-140 (where Ratio B moves toward BUY territory and the
    dividend yield approaches ~3%)
  • The 2027-28 Guyana/Permian/Golden Pass ramp is the catalyst that should re-rate this
    from "flat 2026 digestion" to "structural growth compounder" — patience is the trade
""")

    print(SEP)
    print(f"""
SUMMARY: XOM ◎ ACCUMULATE — Ratio B 0.84× (27.2% downside / 32.3% upside). FORTRESS \
SUPERMAJOR AT MID-RANGE: trading at $151 (52-wk range $103-176) with 2026 guidance calling \
for earnings roughly FLAT as the 2025 oil-price spike (briefly >$110/bbl) normalizes — before \
a multi-year growth ramp (Guyana, Golden Pass LNG, China chemicals) reaccelerates into \
2027-28. TWO IRREPLACEABLE GROWTH ENGINES: Guyana at a record >900K boe/d gross (XOM net \
~405K boe/d at 45%, sub-$35/bbl breakevens, 4 FPSOs operating/ramping) and Pioneer/Permian \
integration delivering >$3B/yr synergies (+50% above original guidance, 2.3 MMboe/d 2030 \
target, growing at 2.5x the pre-deal pace). FY2025: revenue $332B, adj. net income $45B \
($7.50/sh), FCF $26.1B with dividends at only 31% of FCF — enormous coverage cushion. \
BALANCE SHEET IS THE MOAT: AA-/Aa2 — strongest of any major, net debt just $17B. In 2020 \
(debt ballooned to $68.8B on COVID demand collapse) XOM still raised its dividend; today's \
sheet is far stronger, meaning the downside here is a PRICE correction, not a solvency event. \
CAPITAL RETURNS: 43-yr dividend growth streak ($4.12/yr, ~2.7% yield, 'Dividend King' ~2030), \
~$20B/yr buybacks, $9.2B total Q1 2026 shareholder returns. Consensus PT $165 (range \
$130-185) — Argus raised to $169 (May 2026). Conservative 2yr ('flat 2026' floor case): EPS \
$7.55 x 18x + $8.24 div = $144.14 -> -4.7% (-2.4%/yr) — the BASE/BULL cases diverge from this \
floor as Guyana/Permian/Golden Pass ramp into 2027-28. Optionality: Venezuela talks (6 fields, \
~$1B compensation owed). FORTRESS BALANCE SHEET MAKES DOWNSIDE GENUINELY CUSHIONED — add on \
weakness toward $130-140. Bear $110 · Base $165 · Bull $200 · XBull $240.
""")

    print(f"SIGNAL: {SIGNAL_TEXT} (fortress balance sheet + Guyana/Permian growth engines, mid-range entry) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
