"""
Baker Hughes Company (NASDAQ: BKR)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◎ ACCUMULATE  |  Ratio B: 1.09×  |  EPP Gap: +267.4%

THE OILFIELD-SERVICES NAME THAT QUIETLY BECAME AN ENERGY-TECHNOLOGY / DATA-CENTER-POWER COMPANY
Trading at $48.50 (52-week range $32.10–50.85, near recent highs but well off a "priced for
perfection" multiple) on a genuine structural transformation: roughly half of Baker Hughes'
business — Industrial & Energy Technology (IET) — is now a gas-turbines/compression/LNG-
equipment franchise riding TWO simultaneous secular waves: (1) the global LNG buildout
(record orders, multi-year backlog converting to revenue through 2027-2028), and (2) the
data-center power crunch, where utilities and hyperscalers are turning to gas turbines and
on-site generation as grid interconnection queues stretch years — Baker Hughes' NovaLT/
turbomachinery order book has swelled on exactly this demand. Layer onto that a still-solid,
higher-margin, more digital Oilfield Services & Equipment (OFSE) segment that has weathered
the 2025 rig-count downturn better than peers, and a balance sheet that has funded record
buybacks and a steadily-growing dividend (9 consecutive increases). FY2025 was a record year
for orders and adjusted EBITDA margin even as legacy oilfield activity software-landed.

The honest tension: at ~17-18x forward earnings near a multi-year high, the stock has begun
to re-rate toward an "industrial/technology" multiple rather than a discounted "oilfield
services" one — some of the structural good news is already in the price. But unlike SLB
(re-rated to ~25x trailing near its highs on a still-shrinking earnings base), Baker Hughes'
re-rating is being validated by an actually-GROWING earnings base (IET backlog conversion +
buybacks compounding EPS), which keeps the asymmetry tilted constructively rather than merely
"priced for a soft landing."

Conviction: MODERATE-HIGH on the structural IET/data-center-power and LNG-cycle thesis (this
is a genuine multi-year demand inflection, not a story stock); MODERATE on near-term upside
given the stock already trades near 52-week highs — Ratio B sits at the ACCUMULATE/WATCHLIST
boundary, tilting toward ACCUMULATE on the strength of a growing (not shrinking) earnings base.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "BKR"
COMPANY         = "Baker Hughes Company"
SECTOR          = "Energy Technology · Industrial & Energy Technology (Gas Turbines, LNG Equipment, Compression) · Oilfield Services & Equipment · Data-Center Power · NASDAQ: BKR"
SECTOR_GROUP    = "Energy"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 48.50    # June 2026, near multi-year highs
ANNUAL_DIV      = 0.92     # $0.23/qtr after a 9th consecutive annual hike; yield ~1.9%
SHARES_OUT_B    = 0.955    # ~955mm shares outstanding (post sustained buybacks)
MARKET_CAP_B    = 46.3     # CURRENT_PRICE × SHARES_OUT_B
FW52_HIGH       = 50.85
FW52_LOW        = 32.10

# ── FY2025 FULL-YEAR FINANCIALS ─────────────────────────────────────────────
REVENUE_FY2025_B          = 28.85   # Roughly flat-to-modestly-up YoY despite OFSE softness
ADJ_EPS_FY2025            = 2.62    # Up ~12% YoY — buyback + IET margin expansion offsetting OFSE softness
ADJ_EBITDA_MARGIN_FY2025_PCT = 19.8 # Record adjusted EBITDA margin
NET_INCOME_FY2025_B       = 2.45
OCF_FY2025_B              = 4.05
FCF_FY2025_B              = 2.55
ADJ_EPS_YOY_PCT           = 12
ORDERS_FY2025_B           = 30.4   # Record order intake — book-to-bill > 1
RIG_COUNT_DOWNTURN_NOTE   = "Global rig count down ~6-8% YoY in 2025 — OFSE held margins via cost actions and a richer technology mix"

# ── INDUSTRIAL & ENERGY TECHNOLOGY (IET) — THE GROWTH ENGINE ────────────────
IET_REVENUE_FY2025_B       = 12.6    # ~44% of total revenue and growing share
IET_ORDERS_FY2025_B        = 14.9    # Record — gas tech + LNG equipment driving the beat
IET_BACKLOG_B              = 33.5    # Multi-year backlog converting to revenue through 2027-28
LNG_EQUIPMENT_ORDER_NOTE   = "Multiple large LNG liquefaction-train equipment awards (US Gulf Coast, Qatar, Mozambique-class projects) underpin a multi-year LNG-equipment supercycle"
GAS_TURBINE_DATACENTER_NOTE = "NovaLT/turbomachinery order book swelling on data-center on-site power demand — utilities and hyperscalers turning to gas generation as grid-interconnection queues stretch 4-7 years"
NEW_ENERGY_ORDERS_M        = 850     # Hydrogen, CCUS, geothermal, emissions-management orders — small but compounding

# ── OILFIELD SERVICES & EQUIPMENT (OFSE) ─────────────────────────────────────
OFSE_REVENUE_FY2025_B      = 16.25
OFSE_MARGIN_RESILIENCE_NOTE = "OFSE margins held up better than peers through the 2025 downturn via a richer subsea/digital/chemicals mix and disciplined cost actions"
INTL_OFFSHORE_NOTE         = "International and offshore activity (Middle East, Brazil, Guyana-adjacent) outgrowing North America — a more contract-backed, less-volatile base"

# ── CAPITAL RETURNS & BALANCE SHEET ──────────────────────────────────────────
BUYBACK_FY2025_B           = 1.7     # Record annual repurchase pace
DIV_CONSECUTIVE_HIKES      = 9
TOTAL_SHAREHOLDER_RETURN_TARGET_PCT = 80   # Targeting >80% of FCF returned to shareholders through the cycle
NET_DEBT_TO_EBITDA         = 0.9     # Investment-grade, conservatively levered
CREDIT_RATING_NOTE         = "A-/A3 investment-grade ratings — among the strongest balance sheets in oilfield services/energy-technology"

# ── ANALYST CONSENSUS ────────────────────────────────────────────────────────
EPS_FY2026E             = 3.05     # Consensus ~$2.95-3.15, reflecting IET backlog conversion + buybacks
TRAILING_PE             = 18.5
FORWARD_PE              = 15.9
CONSENSUS_PT            = 53.0     # Average target ~$48-58 (range $40-65)
PT_LOW                  = 40.0
PT_HIGH                 = 65.0
CONSENSUS_RATING        = "Buy / Strong Buy"
ANALYST_RATING_NOTE     = "~21 Buy / 5 Hold / 1 Sell of ~27 analysts; consensus PT ~$53 (range $40-65) — skewed bullish on the IET/data-center-power re-rating thesis"

# ── SCENARIOS ────────────────────────────────────────────────────────────────
# BEAR  $36: A 2026-27 industrial-orders air-pocket — LNG FID timing slips, data-center
#            gas-turbine demand proves more "story" than near-term revenue (long lead times,
#            permitting delays), AND the OFSE downcycle deepens as E&P capex stays cautious;
#            the market re-rates BKR back toward a discounted "legacy oilfield services"
#            multiple (~12-13x trough earnings) rather than an industrial-technology one.
#            Roughly the lower third of the 52-week range — balance sheet (net debt/EBITDA
#            ~0.9x, A-/A3 ratings) keeps the dividend and buyback intact through the trough.
#
# BASE  $50: Roughly where the stock sits today — IET backlog ($33.5B) converts to revenue
#            on schedule through 2027-28, gas-turbine/data-center orders continue at a
#            healthy (not explosive) clip, OFSE holds its margin-resilient course through
#            a still-soft rig-count environment, and buybacks keep mechanically compounding
#            EPS at a high-single-digit pace. "Consensus PT ~$53" realized.
#
# BULL  $60: The data-center power crunch becomes an acknowledged multi-year supercycle —
#            BKR's NovaLT/turbomachinery order book inflects sharply higher, the LNG
#            equipment supercycle adds a second wave of large train awards, and the market
#            re-rates BKR from "oilfield services with an industrial arm" to "energy-
#            technology / power-infrastructure compounder," closing the multiple gap to
#            higher-multiple industrials/power-equipment peers (GE Vernova, Vertiv-style).
#
# XBULL $72: Full re-rating thesis — IET becomes the clear majority of revenue and earnings,
#            data-center/grid power generation becomes a structurally-scarce, multi-decade
#            growth category that BKR is positioned at the center of (turbines + LNG +
#            new-energy optionality all compounding together), AND a genuine international/
#            offshore E&P upcycle lifts the legacy OFSE base simultaneously. Requires
#            multiple structural waves to crest together — high-conviction, lower-probability.
BEAR    = 36.0
BASE    = 50.0
BULL    = 60.0
XBULL   = 72.0

# ── EPP (EARNINGS POWER PRICE) ───────────────────────────────────────────────
# Trough scenario: oilfield-services-adjacent names can fall hard in a genuine industry
# downcycle (BKR itself traded near $17-20 in the 2020 collapse and the low-$20s in 2015-16).
# EPS_TROUGH reflects a severe simultaneous OFSE-downcycle / IET-orders-air-pocket scenario,
# well below the FY2025 adjusted print of $2.62, and PE_TROUGH reflects the deep-discount
# multiple cyclical energy-services names receive in a panic — even with a larger, more
# durable industrial-technology base cushioning the trough relative to 2015-16/2020.
EPS_TROUGH  = 1.10
PE_TROUGH   = 12.0
EPP         = EPS_TROUGH * PE_TROUGH   # = $13.20

# ── SCA: STRUCTURAL COMPETITIVE ADVANTAGE ───────────────────────────────────
# Baker Hughes' moat has shifted meaningfully: from "one of three big oilfield-services
# majors" toward "a genuine energy-technology / power-infrastructure franchise (gas
# turbines, LNG equipment, compression) riding the data-center-power and LNG-buildout
# supercycles" layered on top of a still-resilient, higher-margin legacy OFSE business.
# The structural offset: roughly half the business remains a cyclical, capex-of-customers
# dependent oilfield-services operation, and IET project timing/lead times can disappoint.

SCA_FACTORS = {
    # Factor                                          : (score,  weight)
    "iet_gas_turbine_lng_equipment_franchise"         : (+0.35,  0.18),  # Genuine technology leadership in gas turbines, LNG trains, compression — record $33.5B backlog
    "data_center_power_secular_demand_inflection"     : (+0.30,  0.15),  # On-site gas generation emerging as the practical answer to grid-interconnection bottlenecks
    "ofse_margin_resilience_and_technology_mix"       : (+0.20,  0.14),  # Held margins through the 2025 downturn better than peers via subsea/digital/chemicals mix
    "capital_return_and_balance_sheet_strength"       : (+0.25,  0.15),  # A-/A3 ratings, net debt/EBITDA ~0.9x, record buybacks, 9 straight dividend hikes
    "diversified_earnings_base_vs_pure_oilfield_peers": (+0.20,  0.13),  # ~44% IET mix gives BKR a structurally different (less purely cyclical) earnings profile than SLB/HAL
    "cyclical_oilfield_services_exposure_remaining"   : (-0.30,  0.12),  # Still ~half the business is capex-of-customers-dependent OFSE — genuine cyclicality remains
    "iet_project_timing_and_lead_time_risk"           : (-0.20,  0.13),  # Large turbine/LNG-train projects have multi-year lead times — order-to-revenue conversion can slip
}

SCA_NET  = sum(score * weight for score, weight in SCA_FACTORS.values())
# SCA_NET = 0.35×0.18 + 0.30×0.15 + 0.20×0.14 + 0.25×0.15 + 0.20×0.13 + (-0.30)×0.12 + (-0.20)×0.13
# SCA_NET ≈ 0.063 + 0.045 + 0.028 + 0.0375 + 0.026 - 0.036 - 0.026 = 0.1375

SCA_SCALE = 0.45  # Fixed framework parameter

# ── 6 PROXY SIGNALS ──────────────────────────────────────────────────────────
# Signal   (score 1–4, weight)
# 1=BEAR, 1.5=BEAR+, 2=BASE, 2.5=BASE+, 3=BULL, 3.5=BULL+, 4=XBULL

SIGNALS = {
    # The structural heart of the bull case: Industrial & Energy Technology now ~44% of
    # revenue, riding TWO simultaneous secular waves — the global LNG-equipment buildout
    # (record $14.9B of FY2025 orders, multiple large liquefaction-train awards) and the
    # data-center power crunch (NovaLT/turbomachinery order book swelling as utilities and
    # hyperscalers turn to on-site gas generation amid multi-year grid-interconnection queues).
    "iet_lng_and_data_center_power_supercycle": (3.5, 0.20),

    # A genuine $33.5B multi-year order backlog converting to revenue through 2027-2028 —
    # this is not a "story stock" promise but contracted, book-to-bill-positive revenue
    # visibility that materially de-risks the next 2-3 years of earnings growth.
    "record_backlog_and_revenue_visibility": (3.0, 0.16),

    # OFSE held up better than peers through the 2025 rig-count downturn (down ~6-8% YoY
    # globally) via a richer subsea/digital/chemicals technology mix and disciplined cost
    # actions — international/offshore (Middle East, Brazil, Guyana-adjacent) activity
    # continues to outgrow North America, providing a more contract-backed revenue base.
    "ofse_resilience_and_international_offshore_mix": (3.0, 0.15),

    # A genuine capital-return story on an investment-grade balance sheet: record $1.7B of
    # FY2025 buybacks, a 9th consecutive annual dividend increase, A-/A3 ratings, and
    # net debt/EBITDA near 0.9x — a durable compounding floor that doesn't depend on any
    # single quarter's commodity prices or order intake cooperating.
    "capital_return_and_investment_grade_balance_sheet": (3.0, 0.15),

    # The honest near-term risk: roughly half the business remains capex-of-customers-
    # dependent oilfield services, large IET projects carry multi-year lead times that can
    # slip (order-to-revenue conversion risk), and the stock now trades near a multi-year
    # high on a re-rated multiple (~16x forward) — some of the good news is already priced.
    "ofse_cyclicality_and_iet_project_timing_risk": (1.5, 0.20),

    # New-energy optionality (hydrogen, CCUS, geothermal, emissions management — ~$850mm of
    # FY2025 orders) remains small in absolute terms but compounding, giving BKR a genuine,
    # underwritten call option on the broader energy-transition / decarbonization buildout
    # without betting the whole franchise on it.
    "new_energy_and_decarbonization_optionality": (2.5, 0.14),
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

# Conservative 2yr: FY2026E EPS (consensus, reflecting backlog conversion + buybacks) ×
# a multiple roughly in line with-to-modestly-below the current ~16x forward — pure
# compounding test, no heroic re-rating to "industrial/technology" multiples required
PE_CONSERVATIVE = 15.0
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
    print(f"  Revenue:           ${REVENUE_FY2025_B:.2f}B  |  Adj. EBITDA margin: {ADJ_EBITDA_MARGIN_FY2025_PCT:.1f}% (record)")
    print(f"  Adj. EPS:          ${ADJ_EPS_FY2025:.2f}  ({ADJ_EPS_YOY_PCT:+d}% YoY)  |  Net Income: ${NET_INCOME_FY2025_B:.2f}B")
    print(f"  OCF / FCF:         ${OCF_FY2025_B:.2f}B / ${FCF_FY2025_B:.2f}B")
    print(f"  Orders:            ${ORDERS_FY2025_B:.1f}B (record — book-to-bill > 1)")
    print(f"  {RIG_COUNT_DOWNTURN_NOTE}")

    print(f"\n{sep}")
    print("  INDUSTRIAL & ENERGY TECHNOLOGY (IET) — THE GROWTH ENGINE")
    print(sep)
    print(f"  Revenue ${IET_REVENUE_FY2025_B:.1f}B (~{IET_REVENUE_FY2025_B/REVENUE_FY2025_B*100:.0f}% of total)  |  Orders ${IET_ORDERS_FY2025_B:.1f}B (record)  |  Backlog ${IET_BACKLOG_B:.1f}B (converts through 2027-28)")
    print(f"  {LNG_EQUIPMENT_ORDER_NOTE}")
    print(f"  {GAS_TURBINE_DATACENTER_NOTE}")
    print(f"  New-energy/decarbonization orders: ~${NEW_ENERGY_ORDERS_M}mm (hydrogen, CCUS, geothermal, emissions mgmt)")

    print(f"\n{sep}")
    print("  OILFIELD SERVICES & EQUIPMENT (OFSE)")
    print(sep)
    print(f"  Revenue ${OFSE_REVENUE_FY2025_B:.2f}B (~{OFSE_REVENUE_FY2025_B/REVENUE_FY2025_B*100:.0f}% of total)")
    print(f"  {OFSE_MARGIN_RESILIENCE_NOTE}")
    print(f"  {INTL_OFFSHORE_NOTE}")

    print(f"\n{sep}")
    print("  CAPITAL RETURNS & BALANCE SHEET")
    print(sep)
    print(f"  FY2025 buybacks: ${BUYBACK_FY2025_B:.1f}B (record pace)  |  Dividend: {DIV_CONSECUTIVE_HIKES} consecutive annual increases (yield ~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}%)")
    print(f"  Target: >{TOTAL_SHAREHOLDER_RETURN_TARGET_PCT}% of FCF returned through the cycle  |  Net debt/EBITDA ~{NET_DEBT_TO_EBITDA:.1f}x")
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
        "iet_lng_and_data_center_power_supercycle":           "IET / LNG-equipment / data-center power supercycle",
        "record_backlog_and_revenue_visibility":              "Record $33.5B backlog & revenue visibility",
        "ofse_resilience_and_international_offshore_mix":     "OFSE resilience & international/offshore mix",
        "capital_return_and_investment_grade_balance_sheet":  "Capital return & investment-grade balance sheet",
        "ofse_cyclicality_and_iet_project_timing_risk":       "OFSE cyclicality & IET project-timing risk",
        "new_energy_and_decarbonization_optionality":         "New-energy / decarbonization optionality",
    }
    for k, (score, weight) in SIGNALS.items():
        bar = "█" * int(score * 5)
        print(f"  {labels[k]:<52}  {score:.1f}  wt={weight:.2f}  {bar}")
    print(f"  {'PROXY COMPOSITE':<52}  {PROXY_COMPOSITE:.2f}")

    print(f"\n{sep}")
    print("  SCA — STRUCTURAL COMPETITIVE ADVANTAGE")
    print(sep)
    sca_labels = {
        "iet_gas_turbine_lng_equipment_franchise":          "IET gas-turbine / LNG-equipment franchise",
        "data_center_power_secular_demand_inflection":      "Data-center power secular demand inflection",
        "ofse_margin_resilience_and_technology_mix":        "OFSE margin resilience & technology mix",
        "capital_return_and_balance_sheet_strength":        "Capital return & balance-sheet strength",
        "diversified_earnings_base_vs_pure_oilfield_peers": "Diversified earnings base vs. pure-oilfield peers",
        "cyclical_oilfield_services_exposure_remaining":    "Cyclical oilfield-services exposure remaining",
        "iet_project_timing_and_lead_time_risk":            "IET project timing & lead-time risk",
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
    print(f"  FY2026E EPS (consensus, reflecting backlog conversion + buybacks): ${EPS_FY2026E:.2f}")
    print(f"  Conservative PE applied:                                            {PE_CONSERVATIVE:.1f}× (modestly below the ~16x forward — no re-rating required)")
    print(f"  Target price 2yr:                                                   ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.1f}× + ${2*ANNUAL_DIV:.2f} div = ${PRICE_2YR_CONSV:.2f}")
    print(f"  2-year return:                                                      {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  Note: this is the 'multiple stays roughly where it is, earnings simply compound via")
    print(f"  backlog conversion + buybacks' floor case — BULL/XBULL require an industrial-tech re-rating.")

    print(f"\n{sep}")
    print("  WHY THIS IS A ◎ ACCUMULATE, NOT A ◌ WATCHLIST OR ◉ BUY")
    print(sep)
    print("""
  Baker Hughes has quietly transformed from "one of three big oilfield-services majors"
  into something structurally different: roughly 44% of its revenue now comes from
  Industrial & Energy Technology — a genuine gas-turbine / LNG-equipment / compression
  franchise riding TWO simultaneous secular waves (the global LNG buildout and the
  data-center power crunch) — layered on top of a still-resilient, higher-margin legacy
  oilfield-services business that held its ground through the 2025 downturn.

  WHAT THE MARKET ALREADY PRICES IN (at $48.50, near a multi-year high):
  • IET backlog ($33.5B) converts to revenue roughly on schedule through 2027-2028
  • Gas-turbine/data-center-power orders continue at a healthy, steady clip
  • OFSE holds its margin-resilient course through a still-soft rig-count environment
  • Buybacks keep mechanically compounding EPS at a high-single-digit pace

  WHAT COULD MAKE THIS MORE THAN FAIRLY PRICED:
  1. The data-center power crunch becomes an acknowledged, structurally-scarce, multi-year
     supercycle — BKR's NovaLT/turbomachinery order book inflects sharply higher as
     hyperscalers and utilities commit to on-site gas generation at scale
  2. A second wave of large LNG liquefaction-train awards (beyond the current record
     order intake) extends the equipment supercycle visibility out toward the early 2030s
  3. The market re-rates BKR from "oilfield services with an industrial arm" toward
     "energy-technology / power-infrastructure compounder," closing the multiple gap to
     higher-multiple industrial/power-equipment peers
  4. International/offshore E&P activity (Middle East, Brazil, Guyana-adjacent) extends
     its outgrowth of North America, lifting the legacy OFSE base alongside IET

  THE RISK (the honest read on where this sits):
  • Roughly half the business remains capex-of-customers-dependent oilfield services —
    genuine cyclicality has not been engineered away, only diversified against
  • Large IET projects (turbines, LNG trains) carry multi-year lead times — order-to-
    revenue conversion can slip on permitting, financing, or customer-side delays
  • At ~16x forward earnings near a multi-year high, some of the structural good news
    is already in the price — this is no longer a "discounted oilfield services" multiple
  • A genuine global E&P capex downturn (not just the mild 2025 softness) would pressure
    BOTH segments simultaneously — IET orders are not fully insulated from the energy cycle

  WHAT MAKES THIS AN ACCUMULATE RATHER THAN MERELY A WATCHLIST:
  • Unlike pure oilfield-services peers re-rating on a SHRINKING earnings base, BKR's
    re-rating is being validated by a GROWING one — record orders, record backlog, record
    buybacks, and adjusted EPS up ~12% YoY even through a soft 2025 rig-count environment
  • A-/A3 investment-grade ratings, net debt/EBITDA ~0.9x, and >80%-of-FCF shareholder-
    return targets provide real downside ballast even in a genuine industry air-pocket
  • The $33.5B backlog provides 2-3 years of contracted revenue visibility — this isn't
    a story stock asking investors to underwrite a forecast; much of it is already booked

  POSITION SIZING GUIDANCE:
  • ACCUMULATE — add on any pullback toward $40-44 (where Ratio B would move firmly into
    BUY territory and the entry point would better reflect the structural growth already
    underway, rather than requiring further re-rating)
  • Watch for: IET order-intake deceleration (the single biggest swing factor), confirmation
    that data-center gas-turbine demand converts from "pipeline" to "shipped/recognized"
    revenue, and whether OFSE margins continue to hold as the rig-count cycle bottoms
""")

    print(SEP)
    print(f"""
SUMMARY: BKR ◎ ACCUMULATE — Ratio B 1.09× (25.8% downside / 23.7% upside). THE OILFIELD- \
SERVICES NAME THAT QUIETLY BECAME AN ENERGY-TECHNOLOGY / DATA-CENTER-POWER COMPANY: trading \
at $48.50 (52-wk range $32-51, near multi-year highs but on a still-reasonable ~16x forward \
multiple) with ~44% of revenue now from Industrial & Energy Technology — a genuine gas- \
turbine/LNG-equipment/compression franchise riding TWO secular waves simultaneously: the \
global LNG-equipment buildout (record $14.9B FY2025 orders, multiple large liquefaction-train \
awards) and the data-center power crunch (NovaLT/turbomachinery orders swelling as \
hyperscalers turn to on-site gas generation amid multi-year grid-interconnection queues). \
RECORD $33.5B BACKLOG converts to revenue through 2027-28 — genuine, contracted visibility, \
not a story-stock promise. OFSE (legacy oilfield services, ~56% of revenue) held margins \
better than peers through the 2025 rig-count downturn via a richer technology mix. CAPITAL \
RETURNS: record $1.7B FY2025 buybacks, 9 consecutive annual dividend increases, A-/A3 \
investment-grade ratings, net debt/EBITDA ~0.9x. THE HONEST RISK: roughly half the business \
remains capex-of-customers-dependent, large IET projects carry multi-year lead times that \
can slip, and at ~16x forward near a multi-year high, some good news is already priced in. \
Consensus 'Buy/Strong Buy' (~21 of 27 analysts), PT ~$53 (range $40-65). Conservative 2yr \
(no-re-rating floor case): EPS $3.05 x 15x + $1.84 div = $47.59 -> -1.9% — BULL/XBULL require \
the data-center-power thesis to fully play out and the multiple to re-rate toward industrial- \
technology peers. UNLIKE PURE OILFIELD-SERVICES PEERS RE-RATING ON A SHRINKING EARNINGS BASE, \
BKR'S RE-RATING IS VALIDATED BY A GROWING ONE — add on weakness toward $40-44 to improve the \
entry. Bear $36 · Base $50 · Bull $60 · XBull $72."""
    )

    print(f"SIGNAL: {SIGNAL_TEXT} (energy-technology / data-center-power transformation validated by a growing earnings base, trading near highs on a still-reasonable multiple) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
