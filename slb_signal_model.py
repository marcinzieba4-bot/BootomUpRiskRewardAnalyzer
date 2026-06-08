"""
SLB Limited (NYSE: SLB) — formerly Schlumberger
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◌ WATCHLIST  |  Ratio B: 1.45×  |  EPP Gap: +355.0%

THE OILFIELD-SERVICES TECH PLATFORM AT A 52-WEEK HIGH — REAL TRANSFORMATION STORY,
BUT THE PRICE ALREADY REFLECTS MOST OF IT
Trading at $57 (52-week range $32–59, near the top of the range) on:
  (1) A genuine multi-year transformation from "commodity oilfield services" toward a
      higher-margin technology/digital platform business — Lumi/Delfi digital ARR at
      ~$1.0B (+15% YoY), Digital Operations revenue +87%, and a fresh NVIDIA partnership
      on industrial AI / DSX data-center infrastructure (UBS values the Lumi+Delfi stack
      alone at $6-16B)
  (2) The ChampionX acquisition (closed July 2025) running on plan — already contributing
      $1.5B of revenue in Q1 2026 at accretive margins, on track for $400M of annual
      run-rate synergies by 2027 — plus a fast-emerging Data Center Solutions adjacency
      (+140% YoY) leveraging thermal-management/power expertise for AI infrastructure
  (3) A capital-return program committing >$4B to shareholders in 2026 (dividend raised
      3.5% + ~$2.4B buyback), funded by an investment-grade balance sheet (Debt/Equity ~0.42)

But at $57 — within ~3% of the 52-week high of $58.82 and up roughly 80% from the 52-week
low — the stock has ALREADY re-rated to reflect much of this transformation story. FY2025
results show the cyclical reality underneath: revenue -2%, adjusted EPS -14%, net income
-24% YoY, and 2026 guidance is built on a cautious Brent assumption (high-$50s to low-$60s)
with North America capex discipline and a Q1 2026 guidance cut already flagging $0.06-0.09
of EPS pressure. This is a "real transformation, priced for a soft landing" situation —
the asymmetry simply isn't compelling enough at these levels for ACCUMULATE/BUY.

Conviction: MODERATE on the structural digital/AI re-rating thesis (Lumi/Delfi, ChampionX,
data-center optionality are real and underwritten by execution); LOW-MODERATE on near-term
upside from here given the stock is already pricing in a constructive scenario at a
cyclical high — Ratio B sits in WATCHLIST territory pending a better entry point or
confirmation that the digital mix-shift can offset oilfield-services cyclicality.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "SLB"
COMPANY         = "SLB Limited"
SECTOR          = "Oilfield Services & Equipment · Digital/AI (Lumi, Delfi) · Production Systems (ChampionX) · Data Center Solutions · NYSE: SLB"
SECTOR_GROUP    = "Energy"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 56.87    # June 2026, near the 52-week high
ANNUAL_DIV      = 1.12     # $0.28/qtr after a 3.5% hike (Jan 2026); yield ~2.0%
SHARES_OUT_B    = 1.495    # ~1.495B shares (Q1 2026 10-Q)
MARKET_CAP_B    = 85.0     # CURRENT_PRICE × SHARES_OUT_B
FW52_HIGH       = 58.82
FW52_LOW        = 31.64

# ── FY2025 FULL-YEAR FINANCIALS ─────────────────────────────────────────────
REVENUE_FY2025_B          = 35.71   # Down ~2% YoY
GAAP_EPS_FY2025           = 2.35    # Down ~24%
ADJ_EPS_FY2025            = 2.93    # Down ~14% (ex charges/credits)
NET_INCOME_FY2025_B       = 3.37    # Down ~24% YoY
OCF_FY2025_B              = 6.49
FCF_FY2025_B              = 4.11    # Includes $276M acquisition-related payments
REVENUE_YOY_PCT           = -2
ADJ_EPS_YOY_PCT           = -14
NET_INCOME_YOY_PCT        = -24

# ── FY2026 GUIDANCE ──────────────────────────────────────────────────────────
ADJ_EBITDA_GUIDANCE_LOW_B  = 8.6
ADJ_EBITDA_GUIDANCE_HIGH_B = 9.1
GUIDANCE_BRENT_NOTE        = "Built on a cautious Brent assumption in the high-$50s to low-$60s/bbl"
Q1_2026_GUIDANCE_CUT_LOW   = 0.06   # EPS hit flagged from softer-than-expected revenue
Q1_2026_GUIDANCE_CUT_HIGH  = 0.09

# ── CHAMPIONX ACQUISITION ────────────────────────────────────────────────────
CHAMPIONX_CLOSE_DATE         = "July 2025"
CHAMPIONX_Q1_REVENUE_B       = 1.5     # Contributed in Q1 2026, accretive margins
PRODUCTION_SYSTEMS_GROWTH_PCT = 23     # Revenue +23% YoY, driven by the ChampionX deal
CHAMPIONX_SYNERGY_TARGET_2027_M = 400  # $400M annual run-rate synergies targeted by 2027

# ── DIGITAL / AI (LUMI, DELFI) ───────────────────────────────────────────────
DIGITAL_REVENUE_Q1_M       = 640   # +9% YoY
DIGITAL_OPERATIONS_GROWTH_PCT = 87
DIGITAL_ARR_B              = 1.02  # +15% YoY
LUMI_DELFI_VALUATION_LOW_B  = 6.1   # UBS valuation range for the Lumi+Delfi platform stack
LUMI_DELFI_VALUATION_HIGH_B = 16.1
NVIDIA_PARTNERSHIP_NOTE    = "Industrial-AI partnership with NVIDIA; named modular design partner for NVIDIA DSX AI factories"

# ── DATA CENTER / NEW ENERGY OPTIONALITY ─────────────────────────────────────
DATA_CENTER_REVENUE_M       = 331   # Recent quarter, +140% YoY
DATA_CENTER_GROWTH_PCT      = 140
NEW_ENERGY_NOTE             = "Geothermal / energy-storage and thermal-management expertise repurposed for AI data-center cooling and power"

# ── INTERNATIONAL / OFFSHORE ─────────────────────────────────────────────────
INTL_VS_NA_NOTE             = "Middle East / international activity outpacing North America; management expects the gap to extend through 2026"
NA_RIG_COUNT_RANGE          = "679-733 (Baker Hughes, early 2026) — operators setting conservative capex budgets"
OFFSHORE_WIN_NOTE           = "Major Kaiping 18-1 subsea contract win (China) — bull-case catalyst for the Production Systems backlog"

# ── CAPITAL RETURNS & BALANCE SHEET ──────────────────────────────────────────
TOTAL_SHAREHOLDER_RETURN_2026_TARGET_B = 4.0   # Committed >$4B in 2026
BUYBACK_2026_TARGET_B       = 2.4
DIV_HIKE_PCT                = 3.5
TOTAL_ASSETS_B              = 54.5
CURRENT_RATIO               = 1.34
DEBT_TO_EQUITY              = 0.42

# ── ANALYST CONSENSUS ────────────────────────────────────────────────────────
EPS_FY2026E             = 2.65     # Zacks consensus ~$2.62-2.74 (down ~6-11% YoY)
TRAILING_PE             = 24.6
FORWARD_PE              = 20.0     # Range ~18.8-21.7x across sources
CONSENSUS_PT            = 60.0     # Average target ~$58-62 (range $43-71)
PT_LOW                  = 43.0
PT_HIGH                 = 71.0
CONSENSUS_RATING        = "Strong Buy / Buy"
ANALYST_RATING_NOTE     = "~25 Buy / 2 Hold / 2 Sell of ~28 analysts; consensus PT ~$58-62 (range $43-71) — a wide dispersion reflecting cyclical uncertainty"

# ── SCENARIOS ────────────────────────────────────────────────────────────────
# BEAR  $35: A 2026 oilfield-services downcycle — Brent slips below the cautious
#            high-$50s/low-$60s guidance baseline, North America capex cuts deepen,
#            and the digital/ChampionX growth narrative stalls against falling
#            legacy-segment volumes; multiple compresses from ~25x trailing toward
#            12-14x on trough earnings. Roughly the 52-week-low zone ($32) — the
#            balance sheet (D/E ~0.42, current ratio 1.34) keeps the dividend intact,
#            but this remains a real cyclical drawdown, not a "soft landing."
#
# BASE  $58: Roughly where the stock sits today — international (Middle East) activity
#            keeps outgrowing North America as guided, ChampionX integration proceeds
#            on schedule (~$400M synergies by 2027), digital ARR keeps compounding at
#            mid-teens, and 2026 plays out within the company's own cautious Brent
#            assumption. "Consensus PT ~$58-60" realized — a continuation of today's
#            multiple on roughly flat-to-modestly-growing earnings.
#
# BULL  $72: International/offshore activity (Kaiping-style wins) accelerates, digital/
#            AI mix-shift re-rates the multiple as Lumi/Delfi prove out UBS's $6-16B
#            platform valuation, Data Center Solutions scales meaningfully (continuing
#            its +140% YoY trajectory), and ChampionX synergies beat the $400M target —
#            the market starts pricing SLB as a "tech platform with an oilfield-services
#            balance sheet" rather than a cyclical commodity-services name.
#
# XBULL $88: Full re-rating thesis — digital/AI revenue crosses a critical mass that
#            structurally lifts margins and smooths cyclicality, data-center power/
#            cooling becomes a multi-billion-dollar segment in its own right, AND a
#            genuine offshore/international upcycle (oil >$80, deepwater capex
#            reacceleration) lifts legacy volumes simultaneously. Requires multiple
#            structural and cyclical tailwinds to align — the highest-conviction,
#            lowest-probability outcome.
BEAR    = 35.0
BASE    = 58.0
BULL    = 72.0
XBULL   = 88.0

# ── EPP (EARNINGS POWER PRICE) ───────────────────────────────────────────────
# Trough scenario: oilfield services is among the most cyclical sub-sectors in energy —
# in the 2020 COVID collapse SLB itself fell to roughly $11. EPS_TROUGH reflects a severe
# downcycle (well below the post-ChampionX/digital-mix-adjusted FY2025 print of $2.93
# adjusted), and PE_TROUGH reflects the deep-discount multiple cyclical services names
# get in a panic — even with a stronger digital/recurring-revenue mix than in 2020.
EPS_TROUGH  = 1.00
PE_TROUGH   = 12.5
EPP         = EPS_TROUGH * PE_TROUGH   # = $12.50

# ── SCA: STRUCTURAL COMPETITIVE ADVANTAGE ───────────────────────────────────
# SLB's moat is shifting from pure technology/scale leadership in oilfield services
# toward a genuine digital-platform business (Lumi/Delfi, recurring ARR) plus
# diversification into adjacent high-growth verticals (ChampionX production chemicals,
# data-center power/cooling). The structural offset remains real: this is still
# fundamentally a cyclical, capex-of-customers-dependent services business with
# concentrated North America exposure to rig-count and commodity-price swings.

SCA_FACTORS = {
    # Factor                                        : (score,  weight)
    "oilfield_services_scale_and_tech_leadership"   : (+0.30,  0.16),  # Largest/most technologically advanced OFS player globally
    "digital_ai_platform_moat_lumi_delfi"           : (+0.30,  0.16),  # Recurring ARR ~$1.0B (+15%), UBS values platform stack at $6-16B
    "champion_x_integration_execution"              : (+0.20,  0.14),  # On-plan integration; $400M synergy target by 2027; accretive margins already
    "international_contract_backed_revenue_mix"     : (+0.25,  0.15),  # Middle East/international outgrowing NA — more stable, contract-backed base
    "capital_return_track_record"                   : (+0.20,  0.13),  # >$4B committed to 2026 shareholder returns; dividend raised, IG balance sheet
    "cyclical_oilfield_services_exposure"           : (-0.35,  0.13),  # Fundamentally a capex-of-customers-dependent cyclical business — FY2025 already declining
    "north_america_capex_volatility"                : (-0.25,  0.13),  # NA rig count swings + Q1 2026 guidance cut underscore near-term earnings risk
}

SCA_NET  = sum(score * weight for score, weight in SCA_FACTORS.values())
# SCA_NET = 0.30×0.16 + 0.30×0.16 + 0.20×0.14 + 0.25×0.15 + 0.20×0.13 + (-0.35)×0.13 + (-0.25)×0.13
# SCA_NET ≈ 0.048 + 0.048 + 0.028 + 0.0375 + 0.026 - 0.0455 - 0.0325 = 0.1095

SCA_SCALE = 0.45  # Fixed framework parameter

# ── 6 PROXY SIGNALS ──────────────────────────────────────────────────────────
# Signal   (score 1–4, weight)
# 1=BEAR, 1.5=BEAR+, 2=BASE, 2.5=BASE+, 3=BULL, 3.5=BULL+, 4=XBULL

SIGNALS = {
    # The ChampionX deal (closed July 2025) is on plan — already contributing $1.5B of
    # revenue in Q1 2026 at accretive margins (Production Systems +23% YoY), tracking
    # toward $400M of annual run-rate synergies by 2027 — while the Lumi/Delfi digital
    # platform compounds ARR at mid-teens (~$1.0B, +15% YoY) and partners with NVIDIA
    # on industrial AI / DSX data-center infrastructure (UBS values the stack at $6-16B).
    "champion_x_integration_and_digital_ai_mix_shift": (3.0, 0.18),

    # International — especially Middle East — activity continues to outgrow North
    # America, providing a more stable, contract-backed revenue base; management expects
    # this gap to extend through 2026, and a major Kaiping 18-1 subsea win in China
    # underscores the offshore/Production Systems backlog momentum.
    "international_middle_east_outgrowing_north_america": (3.0, 0.18),

    # A genuine capital-return program: >$4B committed to shareholders in 2026
    # ($2.4B buyback + a 3.5%-higher dividend), funded by an investment-grade balance
    # sheet (Debt/Equity ~0.42, current ratio 1.34) — a durable income/buyback floor
    # that does not depend on the oil price cooperating in any given quarter.
    "capital_return_program_scale": (3.0, 0.15),

    # The honest near-term risk: 2026 guidance is built on a cautious Brent assumption
    # (high-$50s to low-$60s/bbl), North America rig counts have been volatile (679-733,
    # operators setting conservative capex budgets), and Q1 2026 results already
    # included a guidance cut flagging $0.06-0.09 of EPS pressure from softer revenue.
    "north_america_capex_caution_and_oil_price_sensitivity_risk": (1.5, 0.20),

    # A fast-emerging adjacency: Data Center Solutions revenue +140% YoY (~$331M in a
    # recent quarter), leveraging SLB's thermal-management/power expertise — plus a new
    # NVIDIA partnership (modular design partner for DSX AI factories) and geothermal/
    # energy-storage optionality. Small in absolute terms today, but a genuine new
    # growth vector the market has only begun to credit.
    "data_center_power_and_new_energy_optionality": (3.0, 0.13),

    # The cyclical reality underneath the transformation story: FY2025 revenue fell ~2%,
    # adjusted EPS fell ~14%, and net income fell ~24% YoY — a reminder that even the
    # best-positioned oilfield-services name remains exposed to the capex cycle of its
    # E&P customers, and that "transformation" doesn't yet fully offset cyclicality.
    "cyclical_margin_pressure_and_fy2025_earnings_decline": (2.0, 0.16),
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

# Conservative 2yr: FY2026E EPS (consensus, already down ~6-11% YoY) × a multiple BELOW
# the current ~25x trailing (and below the ~20x forward) + 2yr dividends — pure
# compounding test, no heroic re-rating required
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
    print(f"  Revenue:           ${REVENUE_FY2025_B:.2f}B  ({REVENUE_YOY_PCT:+d}% YoY)")
    print(f"  GAAP EPS:          ${GAAP_EPS_FY2025:.2f}  |  Adj. EPS: ${ADJ_EPS_FY2025:.2f}  ({ADJ_EPS_YOY_PCT:+d}% YoY)")
    print(f"  Net Income:        ${NET_INCOME_FY2025_B:.2f}B  ({NET_INCOME_YOY_PCT:+d}% YoY)")
    print(f"  OCF / FCF:         ${OCF_FY2025_B:.2f}B / ${FCF_FY2025_B:.2f}B  (FCF incl. $276mm acquisition-related payments)")

    print(f"\n  FY2026 guidance:")
    print(f"    Adj. EBITDA ${ADJ_EBITDA_GUIDANCE_LOW_B:.1f}-{ADJ_EBITDA_GUIDANCE_HIGH_B:.1f}B | {GUIDANCE_BRENT_NOTE}")
    print(f"    Q1 2026 guidance cut flagged ${Q1_2026_GUIDANCE_CUT_LOW:.2f}-${Q1_2026_GUIDANCE_CUT_HIGH:.2f} EPS hit from softer-than-expected revenue")

    print(f"\n{sep}")
    print("  CHAMPIONX ACQUISITION & DIGITAL/AI PLATFORM")
    print(sep)
    print(f"  ChampionX: closed {CHAMPIONX_CLOSE_DATE}  |  Q1 2026 revenue contribution ${CHAMPIONX_Q1_REVENUE_B:.1f}B (accretive margins)")
    print(f"  Production Systems revenue +{PRODUCTION_SYSTEMS_GROWTH_PCT}% YoY  |  Synergy target: ${CHAMPIONX_SYNERGY_TARGET_2027_M}mm/yr run-rate by 2027")
    print(f"  Digital (Lumi/Delfi): Q1 revenue ${DIGITAL_REVENUE_Q1_M}mm (+9% YoY) | Digital Operations +{DIGITAL_OPERATIONS_GROWTH_PCT}% | ARR ${DIGITAL_ARR_B:.2f}B (+15% YoY)")
    print(f"  UBS platform valuation: ${LUMI_DELFI_VALUATION_LOW_B:.1f}-{LUMI_DELFI_VALUATION_HIGH_B:.1f}B  |  {NVIDIA_PARTNERSHIP_NOTE}")

    print(f"\n{sep}")
    print("  DATA CENTER / NEW ENERGY OPTIONALITY")
    print(sep)
    print(f"  Data Center Solutions revenue: ~${DATA_CENTER_REVENUE_M}mm (+{DATA_CENTER_GROWTH_PCT}% YoY)")
    print(f"  {NEW_ENERGY_NOTE}")

    print(f"\n{sep}")
    print("  INTERNATIONAL / OFFSHORE & NORTH AMERICA")
    print(sep)
    print(f"  {INTL_VS_NA_NOTE}")
    print(f"  NA rig count: {NA_RIG_COUNT_RANGE}")
    print(f"  {OFFSHORE_WIN_NOTE}")

    print(f"\n{sep}")
    print("  CAPITAL RETURNS & BALANCE SHEET")
    print(sep)
    print(f"  2026 target: >${TOTAL_SHAREHOLDER_RETURN_2026_TARGET_B:.0f}B to shareholders (${BUYBACK_2026_TARGET_B:.1f}B buyback + dividend raised {DIV_HIKE_PCT:.1f}%)")
    print(f"  Yield ~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}%  |  Total assets ${TOTAL_ASSETS_B:.1f}B | Current ratio {CURRENT_RATIO:.2f} | Debt/Equity {DEBT_TO_EQUITY:.2f}")

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
        "champion_x_integration_and_digital_ai_mix_shift":              "ChampionX integration / digital-AI mix shift",
        "international_middle_east_outgrowing_north_america":           "International (Middle East) outgrowing N. America",
        "capital_return_program_scale":                                 "Capital return program scale",
        "north_america_capex_caution_and_oil_price_sensitivity_risk":   "N. America capex caution / oil-price sensitivity risk",
        "data_center_power_and_new_energy_optionality":                 "Data center power / new energy optionality",
        "cyclical_margin_pressure_and_fy2025_earnings_decline":         "Cyclical margin pressure / FY2025 earnings decline",
    }
    for k, (score, weight) in SIGNALS.items():
        bar = "█" * int(score * 5)
        print(f"  {labels[k]:<52}  {score:.1f}  wt={weight:.2f}  {bar}")
    print(f"  {'PROXY COMPOSITE':<52}  {PROXY_COMPOSITE:.2f}")

    print(f"\n{sep}")
    print("  SCA — STRUCTURAL COMPETITIVE ADVANTAGE")
    print(sep)
    sca_labels = {
        "oilfield_services_scale_and_tech_leadership":   "Oilfield services scale & tech leadership",
        "digital_ai_platform_moat_lumi_delfi":           "Digital/AI platform moat (Lumi/Delfi)",
        "champion_x_integration_execution":              "ChampionX integration execution",
        "international_contract_backed_revenue_mix":     "International contract-backed revenue mix",
        "capital_return_track_record":                   "Capital return track record",
        "cyclical_oilfield_services_exposure":           "Cyclical oilfield-services exposure",
        "north_america_capex_volatility":                "North America capex volatility",
    }
    for k, (score, weight) in SCA_FACTORS.items():
        print(f"  {sca_labels[k]:<52}  {score:+.2f} × {weight:.2f} = {score*weight:+.4f}")
    print(f"  {'SCA_NET':<52}  {SCA_NET:+.4f}")
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
    print(f"  FY2026E EPS (consensus, already down ~6-11% YoY): ${EPS_FY2026E:.2f}")
    print(f"  Conservative PE applied:                          {PE_CONSERVATIVE:.1f}× (below the ~25x trailing and ~20x forward multiples)")
    print(f"  Target price 2yr:                                 ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.1f}× + ${2*ANNUAL_DIV:.2f} div = ${PRICE_2YR_CONSV:.2f}")
    print(f"  2-year return:                                    {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  Note: this is the 'multiple normalizes off a 52-week high toward a more typical cyclical-services")
    print(f"  multiple' floor case — BASE/BULL require the digital/ChampionX mix-shift to keep the premium intact.")

    print(f"\n{sep}")
    print("  WHY THIS IS A ◌ WATCHLIST, NOT A ◎ ACCUMULATE OR ✕ AVOID")
    print(sep)
    print("""
  SLB is in the middle of a genuine, well-underwritten transformation — from a commodity
  oilfield-services name toward a higher-margin digital/AI platform business with real
  diversification (ChampionX, data-center power) — but the stock is trading within ~3%
  of its 52-week high, having already risen roughly 80% off its 52-week low. The price
  has caught up to (and arguably gotten ahead of) the story.

  WHAT THE MARKET ALREADY PRICES IN (at $57, near the 52-week high):
  • The ChampionX integration lands roughly on plan, with synergies building toward $400M
  • Digital/AI ARR keeps compounding at a mid-teens clip and the Lumi/NVIDIA story matures
  • International (Middle East) activity continues to outgrow North America as guided
  • 2026 plays out within management's own cautious Brent assumption (high-$50s/low-$60s)

  WHAT COULD MAKE THIS MORE THAN FAIRLY PRICED:
  1. The Lumi/Delfi platform stack starts trading toward UBS's $6-16B valuation range as
     digital ARR crosses a critical mass and the market re-rates SLB as a tech platform
  2. Data Center Solutions (+140% YoY off a small base) scales into a multi-billion-dollar
     standalone segment, leveraging the NVIDIA DSX partnership and thermal-management edge
  3. ChampionX synergies beat the $400M target — echoing the "beat-and-raise" pattern other
     well-executed energy M&A has shown (Pioneer/XOM, Marathon/COP, Hess/CVX)
  4. International/offshore activity (Kaiping-style wins) accelerates into a genuine
     deepwater capex upcycle, lifting legacy segment volumes alongside the digital mix-shift

  THE RISK (the honest read on where this sits in the cycle):
  • FY2025 already showed the cyclical reality: revenue -2%, adjusted EPS -14%, net
    income -24% YoY — even the best-positioned OFS name is exposed to its customers' capex
  • 2026 guidance is built on a CAUTIOUS Brent assumption (high-$50s/low-$60s), and Q1 2026
    already saw a guidance cut flagging $0.06-0.09 of EPS pressure from softer revenue
  • North America rig counts remain volatile (679-733) with operators setting conservative
    budgets — a genuine near-term headwind to the legacy (non-digital, non-international) mix
  • At ~25x trailing / ~20x forward earnings near a 52-week high, there is real room for
    multiple compression if the transformation narrative cools even modestly

  WHAT KEEPS THIS FROM BEING AN OUTRIGHT AVOID:
  • The transformation IS real and underwritten by execution already in hand (ChampionX
    accretive from day one, digital ARR genuinely compounding, NVIDIA partnership signed)
  • An investment-grade balance sheet (D/E ~0.42, current ratio 1.34) and >$4B of committed
    2026 shareholder returns provide a real floor under the downside scenario
  • Consensus remains "Strong Buy/Buy" (~25 of 28 analysts), with a wide PT range ($43-71)
    that reflects genuine two-sided uncertainty rather than one-sided bearishness

  POSITION SIZING GUIDANCE:
  • WATCHLIST, not AVOID — this is a name to track closely for a better entry, not to write off
  • A pullback toward $40-46 (where Ratio B would move toward ACCUMULATE territory and the
    yield approaches ~2.4-2.8%) would meaningfully improve the asymmetry
  • The catalysts to watch: digital ARR crossing $1.5-2B, Data Center Solutions becoming a
    reportable segment in its own right, and ChampionX synergies confirmed at/above $400M
""")

    print(SEP)
    print(f"""
SUMMARY: SLB ◌ WATCHLIST — Ratio B 1.45× (38.5% downside / 26.6% upside). OILFIELD-SERVICES \
TECH PLATFORM NEAR A 52-WEEK HIGH: trading at $57 (52-wk range $32-59, within ~3% of the \
high, up ~80% off the low) on a genuine transformation toward a higher-margin digital/AI \
platform business — Lumi/Delfi digital ARR ~$1.0B (+15% YoY), Digital Operations +87%, and a \
fresh NVIDIA partnership on industrial AI / DSX data-center infrastructure (UBS values the \
Lumi+Delfi stack at $6-16B). CHAMPIONX INTEGRATION ON PLAN: closed July 2025, already \
contributing $1.5B of Q1 2026 revenue at accretive margins (Production Systems +23% YoY), \
on track for $400M of annual synergies by 2027 — plus a fast-emerging Data Center Solutions \
adjacency (+140% YoY). CAPITAL RETURNS: >$4B committed to shareholders in 2026 ($2.4B \
buyback + dividend raised 3.5%, ~2.0% yield) on an investment-grade balance sheet (D/E \
~0.42). THE HONEST RISK: FY2025 revenue -2%, adjusted EPS -14%, net income -24% YoY — even \
the best-positioned OFS name remains exposed to its customers' capex cycle, 2026 guidance \
assumes a cautious Brent (high-$50s/low-$60s), and Q1 2026 already saw a guidance cut \
flagging $0.06-0.09 of EPS pressure. Consensus 'Strong Buy/Buy' (~25 of 28 analysts), PT ~$60 \
(range $43-71). Conservative 2yr (multiple-normalization floor case): EPS $2.65 x 18x + \
$2.24 div = $49.94 -> -12.2% — BASE/BULL require the digital/ChampionX mix-shift to keep the \
multiple intact. REAL TRANSFORMATION, BUT PRICED FOR A SOFT LANDING NEAR THE HIGHS — wait \
for a pullback toward $40-46 to improve the asymmetry. Bear $35 · Base $58 · Bull $72 · \
XBull $88."""
    )

    print(f"SIGNAL: {SIGNAL_TEXT} (real digital/AI transformation story, but priced near 52-week highs with limited margin of safety) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
