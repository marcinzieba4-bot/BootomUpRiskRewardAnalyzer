"""
Verizon Communications, Inc. (NYSE: VZ) — Bottom-Up Risk/Reward Signal Model
BottomUp Risk/Reward Analyzer · veerock framework
Date: 2026-06-02

NOTE: VZ is the cheapest large-cap US telecom on forward P/E (9.4×) and EV/EBITDA (7.2×).
The investment thesis is a three-layer compounding yield: (1) 5.9% dividend yield (22
consecutive increases; FCF payout only 56%); (2) accelerating EPS growth (+7.6% Q1 2026,
best since 2021) driven by declining capex; (3) Frontier fiber optionality — 30M passings
creating a national fiber operator to compete with AT&T. The primary risks are $110B net
debt (2.6× EBITDA post-Frontier, above the 2.0–2.25× target), the cable MVNO structural
headwind, and Frontier integration execution. ACCUMULATE for income; add more on weakness.
"""

# ── PRICE & MARKET DATA ───────────────────────────────────────────────────────
TICKER          = "VZ"
COMPANY         = "Verizon Communications, Inc."
SECTOR          = "Wireless · Fios Fiber · Frontier Fiber · 5G FWA · NYSE: VZ"
DATE            = "2026-06-02"
CURRENT_PRICE   = 47.81
VOL_52W_LOW     = 38.39
VOL_52W_HIGH    = 51.68
SHARES_OUT_M    = 4180.0    # As of June 2026
ANNUAL_DIV      = 2.83      # $0.7075/quarter; raised Jan 30, 2026 (+2.5%); ~5.92% yield
# 22 consecutive annual increases (since 2004); Dividend King in 3 more years
# FCF payout ratio: $11.2B div / $20.1B FCF = 56% → well covered; ~$8.9B free after dividends

# ── FRONTIER ACQUISITION ──────────────────────────────────────────────────────
# Closed January 20, 2026. Transforms VZ from a regional NE fiber player to a
# national fiber operator competing with AT&T in 31 states.
FRONTIER_CLOSE_DATE       = "January 20, 2026"
FRONTIER_TOTAL_VALUE_B    = 20.0      # ~$9.9B equity + $12.9B assumed debt (~$20B total)
FRONTIER_FIBER_PASSINGS_M = 12.0      # ~12M new fiber homes/businesses added
COMBINED_FIBER_PASSINGS_M = 30.0      # VZ Fios ~15M + Frontier ~12M + expansion = ~30M total
FRONTIER_STATES           = 25        # States added (Midwest/Southeast/Southwest complement NE Fios)
FRONTIER_SYNERGY_TARGET_B = 1.0       # Raised from $500M to $1B+ run-rate by 2028
FRONTIER_INTEGRATION_STATUS = "On track per Q1 2026 management commentary"
# Post-Frontier: VZ is #2/3 US broadband provider (16.8M total subs Q1 2026)
# AT&T fiber comparison: 29.5M passings, 10.1M subs at 40% penetration;
# VZ combined fiber will take 3-5 years to approach AT&T's penetration depth

# ── WIRELESS SUBSCRIBERS ──────────────────────────────────────────────────────
# Q1 2025 TROUGH → Q4 2025 RECOVERY → Q1 2026 FIRST POSITIVE SPRING IN 13 YEARS
# Quarter | Phone Net Adds
# Q1 2025 | -289,000  (competitive pressure trough)
# Q2 2025 |   -9,000
# Q3 2025 |  +44,000
# Q4 2025 | +616,000  (best since Q4 2019; beat AT&T's +421K for first time in over a year)
# Q1 2026 |  +55,000  (first positive Q1 since 2013 — structural inflection)
POSTPAID_PHONE_ADDS_FY2025 = 362000  # Net total FY2025 (sum of quarters)
POSTPAID_PHONE_ADDS_Q1_2026 = 55000  # Q1 2026
POSTPAID_CHURN_FY2025      = 0.0092  # ~0.92% average; slightly above T-Mobile 0.86%
TOTAL_WIRELESS_RETAIL_M    = 145.0   # Total wireless retail connections (approx)
POSTPAID_ARPA_Q3_2025      = 147.91  # Consumer postpaid ARPA; +2.0% YoY

# ── FIXED WIRELESS ACCESS (FWA / 5G HOME INTERNET) ───────────────────────────
# C-band (3.7 GHz): 230M+ POPs covered; FWA priority shifting to Frontier fiber markets
FWA_SUBS_Q1_2026_M    = 6.0     # Surpassed 6M in Q1 2026
FWA_NET_ADDS_FY2025   = 1.17    # Net adds FY2025 (+308K Q1, +278K Q2, +261K Q3, +319K Q4)
FWA_NET_ADDS_Q1_2026  = 0.214   # Q1 2026 — decelerating as focus shifts to fiber
FWA_TARGET_2028_M     = 8.5     # Management target 8-9M by 2028
# T-Mobile comparison: T-Mobile 8.5M FWA end-2025 (60% US market share); TMUS 2.5GHz gives
# better propagation than VZ's C-band 3.7GHz → VZ must deploy more towers per FWA subscriber

# ── FIOS FIBER BROADBAND ──────────────────────────────────────────────────────
FIOS_TOTAL_SUBS_M     = 7.5     # Approx end-2025 (pre-Frontier)
FIOS_NET_ADDS_FY2025  = 0.250   # ~250K net adds FY2025 (+45K Q1, +60K Q2, +61K Q3, +67K Q4)
# Q4 2025 Fios net adds +67K = best Q4 since 2020
# Post-Frontier (Q1 2026): +127K fiber net adds (Fios + Frontier combined)
TOTAL_BROADBAND_Q1_2026_M = 16.8  # Total broadband subs Q1 2026 (FWA + Fios + Frontier fiber)
TOTAL_BROADBAND_ADDS_Q1_2026 = 341000  # Q1 2026 (214K FWA + 127K fiber)

# ── C-BAND SPECTRUM ───────────────────────────────────────────────────────────
CBAND_INVESTMENT_B      = 45.0    # ~$45B — largest spectrum investment in US telecom history
CBAND_POPS_COVERED_M    = 230.0   # 230M+ Americans covered (Phase 1 + Phase 2 partial)
CBAND_BAND              = "3.7–3.98 GHz"
CBAND_SPECTRUM_MHZ      = 60      # ~60 MHz vs T-Mobile 2.5GHz 110MHz
# C-band disadvantage for FWA: higher frequency = shorter range = more towers per sq mi
# Verizon acknowledges this by deprioritizing FWA in areas where Frontier fiber is available

# ── FINANCIALS ────────────────────────────────────────────────────────────────
# FY2025 Full Year (reported January 30, 2026)
TOTAL_REVENUE_FY2025_B      = 138.2   # +2.5% YoY
WIRELESS_SVC_REV_FY2025_B   = 83.8    # ~$83-84B; +~2.5% YoY (Q4: $21.0B; Q3: $21.0B)
ADJ_EBITDA_FY2025_B         = 50.0    # +2.5% YoY
ADJ_FCF_FY2025_B            = 20.1    # +1.5% YoY; up from $14.1B in 2022 (+43% in 3yr)
ADJ_EPS_FY2025              = 4.72    # Implied from Q1 2026 +7.6% growth to $1.28
ANNUAL_DIV_OUTLAY_B         = 11.2    # $2.83 × 4.18B shares = ~$11.2B

# Q1 2026 (reported April 27, 2026 — most recent quarter)
TOTAL_REV_Q1_2026_B         = 34.44   # +2.9% YoY
WIRELESS_SVC_REV_Q1_2026_B  = 20.6    # -1.0% YoY (credits/promo amortization);
                                       # Mobility+Broadband service rev: $22.9B (+1.6% YoY)
ADJ_EBITDA_Q1_2026_B        = 13.4    # +6.7% YoY — BEST EBITDA GROWTH SINCE 2021
ADJ_FCF_Q1_2026_B           = 3.8     # +4% YoY
ADJ_EPS_Q1_2026             = 1.28    # +7.6% YoY — BEST EPS GROWTH SINCE 2021

# FY2026 Guidance (Raised after Q1 2026 beat)
ADJ_EPS_GROWTH_FY2026_PCT   = 5.5     # Raised to 5–6% YoY after Q1 beat
ADJ_EPS_FY2026E             = round(ADJ_EPS_FY2025 * (1 + ADJ_EPS_GROWTH_FY2026_PCT/100), 2)
CAPEX_FY2026E_B             = 16.25   # $16.0–$16.5B — DOWN from $17.5–18.5B (FCF tailwind)
ADJ_FCF_FY2026E_B           = 21.5    # $21.5B+ (highest since 2020; $1.4B YoY improvement)
CASH_FROM_OPS_FY2026E_B     = 37.75   # $37.5–$38.0B midpoint
# FY2027 consensus: EPS ~$5.20–5.40; FCF ~$22–23B

# Capital returns
BUYBACK_AUTH_B              = 25.0    # $25B new 3-year buyback authorized Jan 30, 2026
BUYBACK_2026_MIN_B          = 3.0     # At least $3B in 2026
FCF_AFTER_DIV_FY2025_B      = round(ADJ_FCF_FY2025_B - ANNUAL_DIV_OUTLAY_B, 1)
# = $20.1B - $11.2B = ~$8.9B free after dividends (available for buybacks + debt paydown)

# Balance sheet (end FY2025 / post-Frontier close Jan 2026)
TOTAL_UNSECURED_DEBT_B      = 131.1   # End FY2025 (pre-Frontier; Frontier adds ~$12.9B)
NET_UNSECURED_DEBT_B        = 110.1   # End FY2025 (pre-Frontier)
# Post-Frontier (Jan 2026): assumed $12.9B Frontier debt; issued $11B new bonds
# Post-Frontier net leverage ~2.6×; management target: 2.0–2.25× by 2027
LEVERAGE_POST_FRONTIER      = 2.6     # Net unsecured debt / EBITDA post-Frontier close
LEVERAGE_TARGET             = 2.125   # Management target midpoint
EV_APPROX_B                 = 356.0   # ~$199.6B mkt cap + ~$110-123B net debt (adj.)
EV_EBITDA_APPROX            = round(EV_APPROX_B / ADJ_EBITDA_FY2025_B, 1)  # ~7.1×

FCF_YIELD                   = round(ADJ_FCF_FY2025_B / (CURRENT_PRICE * SHARES_OUT_M / 1000) * 100, 1)
# = $20.1B / $199.6B = ~10.1%

# ── EPP (EARNINGS POWER PRICE) ────────────────────────────────────────────────
# Trough scenario: ARPU -3%/yr + Frontier integration costs overshoot + cable MVNO erodes
EPS_TROUGH   = 4.00    # Conservative trough on FY2025 $4.72: ~15% decline (rate + integration)
PE_TROUGH    = 9       # Telecom distress multiple; dividend yield floor ~9% at $31.50
EPP          = EPS_TROUGH * PE_TROUGH    # = $36.00
EPP_GAP_PCT  = round((CURRENT_PRICE / EPP - 1) * 100, 1)   # +32.8%
# Stock 33% above EPP floor → REAL DOWNSIDE EXISTS in bear; upside more than compensates
# Dividend yield at EPP floor ($36): $2.83 / $36 = 7.9% (historically strong floor)

# ── SCENARIO ASSUMPTIONS ─────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (3.80, 8,  32,
              "Frontier integration disappoints (fiber churn >3%/yr; cable overbuilds); "
              "cable MVNO structural erosion accelerates wireless ARPU -2%/yr; "
              "leverage stays at 2.6×+ (rates elevated; Fitch 'A-' downgrade); "
              "EPS falls to $3.80 × 8× distress = $30 → ~$32 (7.9% div yield floor)."),
    "BASE":  (5.00, 11, 55,
              "Frontier executes $1B+ synergies by 2028; fiber penetration 25-30%; "
              "wireless adds 750K-1M phones (per 2026 guidance upper half); "
              "leverage returns to 2.25× by 2027; EPS $5.00 × 11× = $55. "
              "Analyst consensus territory."),
    "BULL":  (5.40, 13, 70,
              "Full Frontier synergy + 35%+ fiber penetration; convergence bundle drives "
              "ARPU +5%/yr; wireless share recovery from cable MVNO; $25B buyback reduces "
              "share count 12-15%; EPS $5.40 FY2027E × 13× = $70."),
    "XBULL": (6.00, 15, 90,
              "VZ re-rates as convergence company (European telco model: fiber+wireless bundle "
              "at scale). Frontier + Fios achieves 40% penetration at 40M homes. "
              "EPS $6.00 × 15× → $90. Multiple expansion requires proof of FCF acceleration."),
}

# ── SOFTMAX SIGNAL MODEL ──────────────────────────────────────────────────────
PROXY_SIGNALS = [
    # (name, value [1=BEAR/2=BASE/3=BULL/4=XBULL], weight, description)
    ("fcf_dividend_engine",         3.0, 0.25,
     "$20.1B FCF (FY2025); $21.5B+ guided FY2026. FCF payout only 56% ($11.2B div). "
     "$8.9B free after dividends for debt paydown + buybacks. 22 consecutive annual dividend "
     "increases; $2.83/yr (5.9% yield). FCF tripled from $6.9B in 2020 → $20.1B in 2025. "
     "Capex declining $16-16.5B vs $17.5-18.5B = structural FCF expansion."),
    ("wireless_subscriber_recovery", 2.0, 0.20,
     "Q1 2025 trough (-289K) → Q4 2025 record (+616K, best since 2019) → Q1 2026 +55K "
     "(first positive Q1 since 2013). Recovery trajectory is REAL and inflecting. "
     "BUT cable MVNO structural headwind persists (~45% of 2025 industry adds to Xfinity/Spectrum). "
     "Absolute level still modest vs AT&T (+421K Q4) and T-Mobile. BASE signal."),
    ("frontier_fiber_transformation", 3.0, 0.20,
     "Closed Jan 20, 2026; $20B total cost. Adds ~12M fiber passings → combined 30M nationally. "
     "$1B+ run-rate synergies by 2028 (raised from $500M). Q1 2026 fiber net adds 127K. "
     "Transforms VZ from NE-only Fios to national fiber competitor vs AT&T. "
     "32M passings targeted end-2026; 40-50M medium-term. BULL if executes."),
    ("fwa_broadband_platform",       2.0, 0.15,
     "6M+ FWA subs (Q1 2026); +1.17M in FY2025; target 8-9M by 2028. "
     "Total broadband 16.8M (Q1 2026); +341K net adds (214K FWA + 127K fiber). "
     "But FWA decelerating (214K Q1 2026 vs 319K Q4 2025) as Frontier fiber prioritized. "
     "C-band (60MHz at 3.7GHz) inferior FWA economics vs T-Mobile 2.5GHz (110MHz). BASE."),
    ("ebitda_eps_acceleration",      3.0, 0.15,
     "EBITDA +6.7% YoY Q1 2026 (best since 2021). EPS +7.6% (best since 2021). "
     "Declining capex ($16-16.5B vs $17.5-18.5B prior) = structural FCF/EPS expansion. "
     "FY2026 EPS guidance raised to +5-6% growth after Q1 beat. Positive op. leverage "
     "from Sprint-like 'do more with less' phase post-network buildout. BULL."),
    ("leverage_frontier_debt_risk",  1.0, 0.05,
     "Net debt $110.1B (pre-Frontier); post-Frontier leverage ~2.6× EBITDA — above 2.0-2.25× target. "
     "Near Fitch 'A-' downgrade sensitivity. $131.1B total unsecured debt. "
     "$11B new bonds issued for Frontier deal + $12.9B Frontier debt assumed. "
     "Management targets 2.0-2.25× by 2027 via $20B+ annual FCF. BEAR risk signal."),
]

PROXY_COMPOSITE = sum(v * w for _, v, w, _ in PROXY_SIGNALS)
# = 3.0×0.25 + 2.0×0.20 + 3.0×0.20 + 2.0×0.15 + 3.0×0.15 + 1.0×0.05
# = 0.75 + 0.40 + 0.60 + 0.30 + 0.45 + 0.05 = 2.55

import math

SCENARIO_CENTERS = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
TEMP = 0.60

def softmax_weights(composite):
    raw = {s: math.exp(-abs(composite - c) / TEMP)
           for s, c in SCENARIO_CENTERS.items()}
    total = sum(raw.values())
    return {s: v / total for s, v in raw.items()}

# ── SCA (STRUCTURAL COMPETITIVE ADVANTAGE) ───────────────────────────────────
SCA_FACTORS = [
    ("+", "National fiber infrastructure (30M passings post-Frontier): VZ transforms from "
          "NE-only Fios to national fiber operator. Geographic complement to AT&T fiber. "
          "HFC-free network — fiber all the way; no copper legacy in new build footprint.",         +0.60, 0.25),
    ("+", "Dividend franchise (22yr streak; 56% FCF payout; FCF grew 43% in 3yr): VZ is one "
          "of the most reliable income stocks in US large-cap. Dividend sustainability underpins "
          "institutional ownership and provides valuation floor at ~7-8% yield.",                  +0.70, 0.20),
    ("+", "Enterprise/government wireless relationships: VZ historically leads in enterprise, "
          "IoT, and government accounts. Premium plan mix drives ARPA premium vs AT&T/TMUS. "
          "FirstNet competitor; dedicated enterprise SLA; M2M/IoT growing.",                       +0.50, 0.15),
    ("-", "Cable MVNO structural headwind (no MVNO offset for VZ): Xfinity/Spectrum Mobile "
          "run primarily on T-Mobile's network — VZ loses retail wireless subs to cable with "
          "NO wholesale revenue offset. Structural: cable bundles wireless cheaply.",               -0.65, 0.20),
    ("-", "C-band spectrum inferior for FWA (60MHz at 3.7GHz vs TMUS 110MHz at 2.5GHz): "
          "Shorter propagation = more towers/km² for FWA coverage. Higher capex per FWA sub. "
          "VZ rationally pivoting to Frontier fiber in markets where available.",                   -0.40, 0.10),
    ("-", "Frontier integration execution risk: $20B acquisition with systems complexity "
          "(legacy copper, DSL, billing). Cable overbuilders (Comcast/Charter) compete in "
          "Frontier markets. Synergy target raised to $1B — ambitious in year 1.",                 -0.30, 0.07),
    ("+", "Brand premium + ARPU leadership: VZ average ARPA $147.91 (+2% YoY); customers "
          "choose VZ for reliability. 'Never settle' premium positioning supports pricing.",        +0.35, 0.03),
]
# SCA_NET = +0.60×0.25 + 0.70×0.20 + 0.50×0.15
#           + (-0.65)×0.20 + (-0.40)×0.10 + (-0.30)×0.07 + 0.35×0.03
# = 0.150 + 0.140 + 0.075 - 0.130 - 0.040 - 0.021 + 0.011 = +0.185

SCA_NET       = 0.185
SCA_SCALE     = 0.45
ADJ_COMPOSITE = round(PROXY_COMPOSITE + SCA_SCALE * SCA_NET * 0.5, 2)
# = 2.55 + 0.45 × 0.185 × 0.5 = 2.55 + 0.042 = 2.59

# ── MARKET COMPOSITE (back-solved) ───────────────────────────────────────────
# EV(c_market) = CURRENT_PRICE × 1.15² (2yr, 15%/yr discount)
# Target EV ≈ $47.81 × 1.3225 ≈ $63.20
# With BEAR=$32, BASE=$55, BULL=$70, XBULL=$90 + $5.66 div:
# Back-solve: c_market ≈ 2.20 → EV ≈ $62.90 ≈ $63.20 ✓
# Market pricing slightly above BASE — consistent with modest analyst upside ($50-51 PT)
# and 9.4× forward P/E (10-yr avg ~11-12×; slight discount to history).
MARKET_COMPOSITE = 2.20
ADJ_VS_MARKET    = round(ADJ_COMPOSITE - MARKET_COMPOSITE, 2)  # +0.39 → MODERATELY UNDERVALUED

# ── RATIO B ───────────────────────────────────────────────────────────────────
BEAR_TARGET  = SCENARIOS["BEAR"][2]     # $32
BULL_TARGET  = SCENARIOS["BULL"][2]     # $70
DOWNSIDE_PCT = (CURRENT_PRICE - BEAR_TARGET)  / CURRENT_PRICE * 100   # 33.1%
UPSIDE_PCT   = (BULL_TARGET   - CURRENT_PRICE) / CURRENT_PRICE * 100  # 46.4%
RATIO_B      = round(DOWNSIDE_PCT / UPSIDE_PCT, 2)   # 0.71 → BUY

if RATIO_B < 0.75:
    SIGNAL_SHORT = "BUY"
    SIGNAL       = "◉ BUY"
elif RATIO_B < 1.10:
    SIGNAL_SHORT = "ACCUMULATE"
    SIGNAL       = "◎ ACCUMULATE"
elif RATIO_B < 1.75:
    SIGNAL_SHORT = "WATCHLIST"
    SIGNAL       = "◐ WATCHLIST"
else:
    SIGNAL_SHORT = "AVOID"
    SIGNAL       = "✕ AVOID"

# ── CONSERVATIVE 2-YEAR RETURN ────────────────────────────────────────────────
# Income stock conservatism: FY2026E EPS at below-consensus multiple
CONSERVATIVE_EPS     = 5.00    # FY2026E guidance midpoint; very achievable
CONSERVATIVE_PE      = 10      # Conservative; below 10-yr avg 11-12×; implies modest re-rate
CONSERVATIVE_PRICE   = CONSERVATIVE_EPS * CONSERVATIVE_PE    # $50.00
CONSERVATIVE_DIV_2YR = ANNUAL_DIV * 2                         # $5.66
CONSERVATIVE_RETURN  = ((CONSERVATIVE_PRICE + CONSERVATIVE_DIV_2YR) / CURRENT_PRICE - 1) * 100
# = (50.00 + 5.66) / 47.81 - 1 = $55.66 / $47.81 - 1 = +16.4% (+8.2%/yr)
# Income investor framework: 5.9% div yield + 2-3% EPS growth + modest re-rating = 8-10%/yr

# ─────────────────────────────────────────────────────────────────────────────
# REPORT
# ─────────────────────────────────────────────────────────────────────────────

def run_model():
    weights = softmax_weights(ADJ_COMPOSITE)
    div_2yr = ANNUAL_DIV * 2
    ev = sum(weights[s] * (SCENARIOS[s][2] + div_2yr) for s in SCENARIOS)
    mkt_cap_b = CURRENT_PRICE * SHARES_OUT_M / 1000

    report = []
    A = report.append

    A("=" * 76)
    A(f"  {SIGNAL}  —  {COMPANY} ({TICKER})")
    A(f"  Bottom-Up Risk/Reward Signal Model · {DATE}")
    A("=" * 76)
    A(f"  Price: ${CURRENT_PRICE:.2f}  |  52W: ${VOL_52W_LOW}–${VOL_52W_HIGH}")
    A(f"  Shares: {SHARES_OUT_M:.0f}M  |  Mkt Cap: ${mkt_cap_b:.1f}B")
    A(f"  Div: ${ANNUAL_DIV:.2f}/yr ({ANNUAL_DIV/CURRENT_PRICE*100:.1f}% yield; 22 consecutive annual increases)")
    A(f"  Net Debt: ~${NET_UNSECURED_DEBT_B:.1f}B (post-Frontier ~${NET_UNSECURED_DEBT_B+12.9:.0f}B)  |  Leverage: ~{LEVERAGE_POST_FRONTIER:.1f}× EBITDA")
    A(f"  FCF Yield: {FCF_YIELD:.1f}%  (${ADJ_FCF_FY2025_B:.1f}B FCF / ${mkt_cap_b:.1f}B mkt cap)")
    A(f"  EV/EBITDA: ~{EV_EBITDA_APPROX:.1f}×  |  Forward P/E: ~9.4×  (cheapest in telecom peer group)")
    A("")

    # ── SIGNAL DASHBOARD ────────────────────────────────────────────────────
    A("─" * 76)
    A("  SIGNAL DASHBOARD")
    A("─" * 76)
    A(f"  Signal      : {SIGNAL}")
    A(f"  Ratio B     : {RATIO_B:.2f}×  (downside {DOWNSIDE_PCT:.1f}% / upside {UPSIDE_PCT:.1f}%)")
    A(f"  EPP         : ${EPP:.2f}  (${EPS_TROUGH} trough EPS × {PE_TROUGH}× trough P/E)")
    A(f"  EPP Gap     : +{EPP_GAP_PCT:.1f}%  (stock {EPP_GAP_PCT:.0f}% above floor; div yield floor ~8% at $36)")
    A(f"  Proxy Comp  : {PROXY_COMPOSITE:.2f}  |  ADJ: {ADJ_COMPOSITE:.2f}  |  Market: {MARKET_COMPOSITE:.2f}")
    A(f"  ADJ–Market  : {ADJ_VS_MARKET:+.2f}  →  MODERATELY UNDERVALUED")
    A(f"  2yr EV      : ${ev:.2f}  (vs ${CURRENT_PRICE:.2f} current; includes ${div_2yr:.2f} div)")
    A(f"  Conserv.    : +{CONSERVATIVE_RETURN:.1f}% / +{CONSERVATIVE_RETURN/2:.1f}%/yr")
    A(f"              : EPS ${CONSERVATIVE_EPS:.2f} × {CONSERVATIVE_PE}× + ${CONSERVATIVE_DIV_2YR:.2f} div = ${CONSERVATIVE_PRICE + CONSERVATIVE_DIV_2YR:.2f}")
    A("")
    A(f"  SCENARIO WEIGHTS  (at ADJ composite {ADJ_COMPOSITE:.2f}):")
    for s, w in weights.items():
        tgt = SCENARIOS[s][2]
        A(f"    {s:<6} {w*100:5.1f}%  →  ${tgt}  ({'+' if tgt > CURRENT_PRICE else ''}{(tgt-CURRENT_PRICE)/CURRENT_PRICE*100:.0f}%)")
    A("")

    # ── BUSINESS OVERVIEW ────────────────────────────────────────────────────
    A("─" * 76)
    A("  BUSINESS OVERVIEW — Verizon Communications, Inc.")
    A("─" * 76)
    A("  VZ is the largest US wireless carrier by revenue (~$138B total revenue FY2025),")
    A("  with three distinct business segments post-Frontier:")
    A("")
    A("  ① WIRELESS (CORE): ~145M total connections; ~$84B wireless service revenue.")
    A("    Consumer + Business + IoT. Entering 2026 with subscriber momentum: Q4 2025")
    A(f"    +616K postpaid phone (best since 2019); Q1 2026 +55K (first positive Q1 in 13 yr).")
    A("    Cable MVNO headwind: Xfinity/Spectrum took ~45% of industry adds in 2025.")
    A("")
    A(f"  ② FIOS + FRONTIER FIBER: Combined {COMBINED_FIBER_PASSINGS_M:.0f}M passings in 31 states + DC.")
    A(f"    Q1 2026: +127K fiber net adds (first full quarter post-Frontier).")
    A(f"    Frontier synergy target: ${FRONTIER_SYNERGY_TARGET_B:.1f}B+ run-rate by 2028.")
    A(f"    AT&T fiber comparison: 29.5M passings, ~40% penetration, ~10M subs.")
    A("    VZ's fiber penetration will ramp over 3-5 years post-acquisition.")
    A("")
    A(f"  ③ FIXED WIRELESS (FWA): {FWA_SUBS_Q1_2026_M:.1f}M+ subs; target {FWA_TARGET_2028_M:.1f}M by 2028.")
    A("    C-band (3.7 GHz, 230M+ POPs) is the network backbone. Decelerating adds")
    A("    as Frontier fiber displaces FWA in overlap markets. Rational trade-up.")
    A("")

    # ── FRONTIER: THE TRANSFORMATIVE BET ─────────────────────────────────────
    A("─" * 76)
    A("  FRONTIER ACQUISITION — THE NATIONAL FIBER TRANSFORMATION")
    A("─" * 76)
    A(f"  Close Date     : {FRONTIER_CLOSE_DATE}")
    A(f"  Total Cost     : ~${FRONTIER_TOTAL_VALUE_B:.0f}B  (${9.9:.1f}B equity + ${12.9:.1f}B assumed debt)")
    A(f"  New Passings   : ~{FRONTIER_FIBER_PASSINGS_M:.0f}M homes/businesses  ({FRONTIER_STATES} new states)")
    A(f"  Combined Total : {COMBINED_FIBER_PASSINGS_M:.0f}M passings  (VZ Fios + Frontier + expansion)")
    A(f"  Synergy Target : ${FRONTIER_SYNERGY_TARGET_B:.1f}B+ run-rate by 2028  (raised from $500M)")
    A(f"  Status         : {FRONTIER_INTEGRATION_STATUS}")
    A("")
    A("  PRE-FRONTIER VZ: Regional fiber (~15M Fios passings) concentrated in NY/NJ/PA/CT/MA.")
    A("  POST-FRONTIER VZ: National fiber operator in 31 states — Midwest, Southeast,")
    A("  Southwest, Plains — geographically complementing the NE Fios footprint.")
    A("")
    A("  THE STRATEGIC LOGIC:")
    A("  • Fiber convergence: broadband + wireless bundle reduces churn and drives ARPU")
    A("  • AT&T's fiber-mobile bundle (AT&T Fiber + Unlimited Premium) is winning customers")
    A("    in its markets; VZ needs fiber nationally to replicate this model")
    A("  • FWA is inferior to fiber for high-usage households (100GB+/month); fiber wins")
    A("    the premium segment; FWA wins the rural/coverage gap")
    A("  • Frontier's network is 100% fiber (no copper legacy) — modern plant")
    A("")
    A("  RISKS:")
    A("  • Cable overbuilders (Comcast, Charter) compete in Frontier's markets")
    A("  • Fiber-on-fiber competition + promotional pricing = lower initial ARPU")
    A("  • $12.9B acquired debt + $11B new bonds adds $24B to balance sheet")
    A(f"  • Half of Frontier debt retired by Q1 2026 — management acting quickly")
    A("")

    # ── FINANCIALS ────────────────────────────────────────────────────────────
    A("─" * 76)
    A("  FINANCIALS — FY2025 RESULTS & FY2026 GUIDANCE")
    A("─" * 76)
    A(f"  FY2025 Total Revenue       : ${TOTAL_REVENUE_FY2025_B:.1f}B  (+2.5% YoY)")
    A(f"  FY2025 Wireless Svc Rev    : ~${WIRELESS_SVC_REV_FY2025_B:.1f}B  (+~2.5% YoY)")
    A(f"  FY2025 Adj EBITDA          : ${ADJ_EBITDA_FY2025_B:.1f}B  (+2.5% YoY)")
    A(f"  FY2025 Adj FCF             : ${ADJ_FCF_FY2025_B:.1f}B  ({FCF_YIELD:.1f}% FCF yield)")
    A(f"  FY2025 Adj EPS             : ${ADJ_EPS_FY2025:.2f}")
    A(f"  Q1 2026 Adj EBITDA         : ${ADJ_EBITDA_Q1_2026_B:.1f}B  (+6.7% YoY — BEST SINCE 2021)")
    A(f"  Q1 2026 Adj EPS            : ${ADJ_EPS_Q1_2026:.2f}  (+7.6% YoY — BEST SINCE 2021)")
    A("")
    A(f"  FY2026 GUIDANCE (Raised Post-Q1):")
    A(f"    Adj EPS Growth : +5–6% YoY  (→ ~${ADJ_EPS_FY2026E:.2f}E)")
    A(f"    Adj FCF        : ${ADJ_FCF_FY2026E_B:.1f}B+ (highest since 2020; +$1.4B YoY)")
    A(f"    Capex          : ${CAPEX_FY2026E_B:.2f}B  (DOWN from $17.5–18.5B — FCF tailwind)")
    A(f"    Postpaid Phones: Upper half of 750K–1.0M range")
    A("")
    A(f"  DIVIDEND MATH:")
    A(f"    Annual div outlay : ${ANNUAL_DIV_OUTLAY_B:.1f}B  (${ANNUAL_DIV:.2f}/share × {SHARES_OUT_M:.0f}M shares)")
    A(f"    FCF payout ratio  : {ANNUAL_DIV_OUTLAY_B/ADJ_FCF_FY2025_B*100:.0f}%  (very conservative for a utility-like stock)")
    A(f"    Free after divs   : ${FCF_AFTER_DIV_FY2025_B:.1f}B  (for debt paydown + buybacks)")
    A(f"    2026 free after   : ~${ADJ_FCF_FY2026E_B - ANNUAL_DIV_OUTLAY_B:.1f}B  (growing)")
    A("")
    A(f"  CAPITAL RETURNS:")
    A(f"    $25B buyback authorized over 3 years (Jan 2026); at least ${BUYBACK_2026_MIN_B:.0f}B in 2026")
    A(f"    Combined ~$55B in buybacks + dividends through 2028")
    A(f"    At $47.81: $3B/yr in buybacks = ~63M shares/yr = -1.5% share count")
    A("")

    # ── WIRELESS SUBSCRIBER RECOVERY ─────────────────────────────────────────
    A("─" * 76)
    A("  WIRELESS SUBSCRIBER RECOVERY — THE TURNAROUND STORY")
    A("─" * 76)
    A("  Postpaid Phone Net Adds — quarterly trajectory:")
    A("")
    A("  Q1 2025  -289,000  ← TROUGH  (competitive promotions + cable MVNO surge)")
    A("  Q2 2025    -9,000  ← Stabilizing")
    A("  Q3 2025   +44,000  ← Turning positive")
    A("  Q4 2025  +616,000  ← BEST SINCE Q4 2019; beat AT&T's +421K for first time in a year")
    A("  Q1 2026   +55,000  ← FIRST POSITIVE Q1 SINCE 2013 (structural inflection signal)")
    A("")
    A("  CONTEXT: The full-year 2025 result (+362K net adds) is modest but the trajectory")
    A("  matters more than the absolute level. The Q4 2025 recovery was driven by:")
    A("  • 'myPlan' pricing tiers: more flexible vs old unlimited plans; reduced churn")
    A("  • Convergence bundle: wireless + Fios/FWA loyalty discounts")
    A("  • Trade-in promotions (Q4 seasonal strength)")
    A("  • Q1 2026 +55K is the first proof that Q4 recovery was not purely seasonal")
    A("")
    A("  CABLE MVNO THREAT — THE STRUCTURAL CHALLENGE:")
    A("  • Xfinity Mobile + Spectrum Mobile took ~45% of industry phone adds in 2025")
    A("  • Unlike T-Mobile (which earns MVNO wholesale from cable), VZ gets NO offset —")
    A("    cable MVNOs use T-Mobile's network, not Verizon's, competing directly vs VZ")
    A("  • The myPlan convergence bundle (wireless + fiber) is VZ's structural response")
    A("  • Long-term, Frontier fiber gives VZ a national convergence platform to compete")
    A("")

    # ── SCA BREAKDOWN ────────────────────────────────────────────────────────
    A("─" * 76)
    A("  STRUCTURAL COMPETITIVE ADVANTAGE (SCA) FACTORS")
    A("─" * 76)
    for sign, desc, score, wt in SCA_FACTORS:
        contrib = score * wt
        A(f"  {sign}  wt={wt:.2f}  score={score:+.2f}  contrib={contrib:+.3f}")
        A(f"     {desc[:75]}")
        A("")
    A(f"  SCA_NET = {SCA_NET:.3f}  |  Contribution to composite: +{SCA_SCALE * SCA_NET * 0.5:.3f}")
    A("")

    # ── PROXY SIGNALS ────────────────────────────────────────────────────────
    A("─" * 76)
    A("  PROXY SIGNALS")
    A("─" * 76)
    for name, val, wt, desc in PROXY_SIGNALS:
        label = {1.0: "BEAR", 2.0: "BASE", 3.0: "BULL", 4.0: "XBULL"}.get(val, f"{val:.1f}")
        A(f"  [{label}]  {name}  (value={val:.1f}, weight={wt:.2f})")
        A(f"  {desc[:76]}")
        A(f"  {desc[76:152]}" if len(desc) > 76 else "")
        A("")
    A(f"  PROXY COMPOSITE  = {PROXY_COMPOSITE:.2f}")
    A(f"  ADJ COMPOSITE    = {ADJ_COMPOSITE:.2f}  (SCA benefit: +{SCA_SCALE * SCA_NET * 0.5:.3f})")
    A(f"  MARKET COMPOSITE = {MARKET_COMPOSITE:.2f}  (implied by ${CURRENT_PRICE:.2f}; analyst PT $50-51)")
    A(f"  GAP              = {ADJ_VS_MARKET:+.2f}  → MODERATELY UNDERVALUED")
    A("")

    # ── SCENARIOS ────────────────────────────────────────────────────────────
    A("─" * 76)
    A("  SCENARIOS")
    A("─" * 76)
    for s, (eps, pe, price, desc) in SCENARIOS.items():
        chg = (price - CURRENT_PRICE) / CURRENT_PRICE * 100
        A(f"  {s:<6}  ${price:.0f}  ({chg:+.0f}%)  EPS ${eps:.2f} × {pe}× P/E")
        A(f"         {desc[:80]}")
        A("")
    A(f"  RATIO B  = {RATIO_B:.2f}×  ({DOWNSIDE_PCT:.1f}% downside / {UPSIDE_PCT:.1f}% upside to BULL)")
    A(f"  EPP FLOOR: ${EPP:.2f}  (${EPS_TROUGH} trough EPS × {PE_TROUGH}×)  |  EPP Gap: +{EPP_GAP_PCT:.1f}%")
    A(f"  NOTE: At $32 BEAR, div yield = 8.8% — historically strong income floor for VZ")
    A("")

    # ── EV/EBITDA CROSS-CHECK ─────────────────────────────────────────────────
    A("─" * 76)
    A("  EV/EBITDA CROSS-CHECK (2026E EBITDA ~$53B including Frontier)")
    A("─" * 76)
    ebitda_2026e = 53.0   # Post-Frontier consolidated estimate
    net_debt_pf  = 122.0  # Post-Frontier net debt estimate
    A(f"  2026E Adj EBITDA (post-Frontier) : ~${ebitda_2026e:.0f}B")
    A(f"  Net Debt (post-Frontier)         : ~${net_debt_pf:.0f}B")
    A("")
    A("  SCENARIO           EV/EBITDA  EV ($B)  Equity ($B)  Per Share")
    A("  ─────────────────────────────────────────────────────────────")
    for lbl, mult in [
        ("Bear  (6.0×)",   6.0),
        ("Base  (7.5×)",   7.5),
        ("Bull  (9.0×)",   9.0),
        ("XBull (11.0×)", 11.0),
    ]:
        ev_b   = ebitda_2026e * mult
        eq_b   = ev_b - net_debt_pf
        per_sh = max(eq_b, 0) * 1000 / SHARES_OUT_M
        A(f"  {lbl:<20}  {mult:.1f}×    ${ev_b:.0f}B   ${max(eq_b,0):.0f}B       ${per_sh:.0f}")
    A("")
    A(f"  At current 7.1× EV/EBITDA (FY2025 $50B), equity value ≈ ${(50.0*7.1-110.1)*1000/SHARES_OUT_M:.0f}/share ≈ current price.")
    A(f"  Any EBITDA growth (post-Frontier adds ~$3B/yr) + modest multiple expansion = upside.")
    A("")

    # ── KEY INVESTMENT THESIS ─────────────────────────────────────────────────
    A("─" * 76)
    A("  INVESTMENT THESIS — THREE-LAYER YIELD COMPOUNDING")
    A("─" * 76)
    A("")
    A("  VZ at $47.81 offers income investors three simultaneous return drivers:")
    A("")
    A(f"  ① DIVIDEND YIELD (5.9%): 22 consecutive annual increases; $2.83/yr covered")
    A(f"    at 56% of FCF. $8.9B free after dividends. Dividend NOT at risk unless FCF")
    A(f"    falls below $15B — a 25% decline from current $20.1B. Management has called")
    A(f"    the dividend streak 'iron-clad'. Growing ~2.5%/yr; by 2028 ~$3.00+/share.")
    A("")
    A(f"  ② EPS GROWTH ACCELERATION (5-6% guidance): Q1 2026 EPS +7.6% is the best")
    A(f"    print since 2021. Declining capex (${CAPEX_FY2026E_B:.1f}B vs $17.5-18.5B prior) creates")
    A(f"    structural FCF/EPS expansion without needing revenue acceleration. FCF guided")
    A(f"    ${ADJ_FCF_FY2026E_B:.1f}B+ in 2026 = highest since 2020. EPS re-rating from 9.4× toward")
    A(f"    historical 11-12× adds $10-20/share in multiple expansion at consensus EPS.")
    A("")
    A(f"  ③ FRONTIER FIBER OPTIONALITY: The $20B acquisition is not yet in the price.")
    A(f"    Each percentage point of incremental fiber penetration at {COMBINED_FIBER_PASSINGS_M:.0f}M passings")
    A(f"    = 300K new fiber subscribers × ~$70/mo = $252M revenue. At 10% incremental")
    A(f"    penetration above current: +$2.5B annual revenue → +$0.30 EPS → +$3.30/share.")
    A(f"    Full AT&T-like 40% penetration at 30M homes = 12M fiber subs = BULL scenario.")
    A("")
    A("  ACCUMULATE at current levels. Add more below $44 (6.4% yield, 9× P/E).")
    A("  Full BUY below $40 (7.1% yield, EPP floor territory). Patient income investors")
    A("  collect 5.9% while waiting for re-rating. Total return framework:")
    A(f"  5.9% div + 5-6% EPS growth + potential 0-2%/yr buyback = 11-14% annual return.")
    A("")
    A("  RISKS TO MONITOR:")
    A(f"  • Frontier fiber penetration stalls below 20% (cable overbuild pressure)")
    A(f"  • Net debt stays >2.4× EBITDA beyond 2027 → multiple compression")
    A(f"  • Cable MVNO share of industry adds exceeds 55% → wireless ARPU under pressure")
    A(f"  • Interest rate re-acceleration → $131B debt refinancing cost headwind")
    A(f"  • Wireless ARPA decelerates or declines (myPlan promotional costs ongoing)")
    A("════════════════════════════════════════════════════════════════════════════")
    A("")

    summary_line = (
        f"VZ {SIGNAL} — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT:.1f}% downside / {UPSIDE_PCT:.1f}% upside). "
        f"Cheapest US telecom: 9.4× forward P/E, 7.1× EV/EBITDA, {FCF_YIELD:.1f}% FCF yield. "
        f"5.9% dividend yield (22 consecutive annual increases; 56% FCF payout). $8.9B free after dividends. "
        f"Q1 2026: EPS +7.6% YoY (best since 2021); EBITDA +6.7%; first positive Q1 phone subs in 13 years (+55K). "
        f"Frontier acquisition closed Jan 20, 2026 ($20B; 30M fiber passings nationally; $1B+ synergy target). "
        f"FWA: {FWA_SUBS_Q1_2026_M:.0f}M+ subs; target {FWA_TARGET_2028_M:.0f}M by 2028; total broadband 16.8M. "
        f"Capital return: $25B buyback authorized; $21.5B+ FCF guided 2026. "
        f"Risk: net debt ~$123B post-Frontier (2.6× EBITDA; target 2.0-2.25× by 2027). "
        f"Cable MVNO headwind (Xfinity/Spectrum on T-Mobile network → no MVNO offset for VZ). "
        f"C-band 230M+ POPs covered; $45B investment. Conservative 2yr: EPS $5.00 × 10× + $5.66 div = $55.66 → +16.4%. "
        f"Analyst consensus $50-51 (+5-7%); Morningstar FV $53. Bear $32 · Base $55 · Bull $70 · XBull $90."
    )
    A(f"SUMMARY: {summary_line}")
    A("")
    A(f"SIGNAL: {SIGNAL} | Ratio B: {RATIO_B:.2f}× | EPP Gap: +{EPP_GAP_PCT:.1f}%")

    return "\n".join(report)


if __name__ == "__main__":
    print(run_model())
