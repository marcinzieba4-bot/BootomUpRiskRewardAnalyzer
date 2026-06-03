"""
Charter Communications, Inc. (NASDAQ: CHTR)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-03

SIGNAL: ◉ BUY  |  Ratio B: 0.29×  |  EPP Gap: +90.4%

HIGH-LEVERAGE DEEP VALUE
Stock fell 67% from May 2025 high ($437 → $143) as market prices in:
  (1) broadband sub losses (~120K/quarter, no sign of near-term reversal)
  (2) Cox Communications full-company merger (announced May 16, 2025) — leverage spike fear
  (3) Capex cycle peak ($11.7B in 2025, $11.4B guided 2026)

At $143: EV/EBITDA 5.0× (cable traded 8-10× historically), P/E 3.9×, FCF yield 25%+.
The market is pricing in NO capex inflection, NO broadband stabilization, NO Cox synergies.
Our model says: all three will materialize — capex falls below $8B by 2028, FCF inflects to $8-9B.
At that point, the stock is pricing itself at 1.7-2.0× FCF — effectively free.

NOT a comfortable BUY. This is a high-leverage, high-reward turnaround with a real bear case near $75.
Conviction level: MODERATE-HIGH on the inflection thesis, LOW on near-term sub trends.

Cox merger context: announced May 16, 2025 (same day as 52-week high); stock fell 67% as
leverage fears overwhelmed the strategic rationale. Cox adds ~6.5M subs + $5B EBITDA;
combined leverage ~4.3× → target 3.5-3.75× within 3 years post-close.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "CHTR"
COMPANY         = "Charter Communications, Inc."
SECTOR          = "Cable & Broadband · Spectrum Mobile · Cox Merger · NASDAQ: CHTR"
SECTOR_GROUP    = "Telecoms/Media"
ANALYSIS_DATE   = "2026-06-03"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 142.79   # June 3, 2026
ANNUAL_DIV      = 1.40     # Newly initiated quarterly dividend: $0.35/Q (Q2 2026+)
SHARES_OUT_M    = 127.23   # Diluted shares outstanding (Q1 2026: 126.85M)
MARKET_CAP_B    = 19.75    # $19.75B market cap
FW52_HIGH       = 437.06   # May 16, 2025 (day of Cox merger announcement)
FW52_LOW        = 136.63   # January 29, 2026

# ── FY2025 FULL-YEAR FINANCIALS ─────────────────────────────────────────────
REVENUE_FY2025_B       = 54.8    # Down 0.6% YoY
EBITDA_FY2025_B        = 22.7    # Adj. EBITDA; up 0.6% YoY
FCF_FY2025_B           = 5.0     # Up from $4.3B in FY2024 (+16%)
GAAP_EPS_FY2025        = 36.21   # Diluted (consolidated entity; Q4 $10.34)
NET_INCOME_ATTR_FY2025 = 2.518   # $2.518B attributable to Charter shareholders
CAPEX_FY2025_B         = 11.7    # Including $3.9B line extensions

# ── Q1 2026 RESULTS ─────────────────────────────────────────────────────────
REVENUE_Q1_2026_B  = 13.6   # Down 1% YoY
EBITDA_Q1_2026_B   = 5.6    # Down 2.2% YoY (Q1 challenging vs political ad comp)
FCF_Q1_2026_B      = 1.4    # Annualizing ~$5.6B
GAAP_EPS_Q1_2026   = 9.17   # Missed consensus $10.32
CAPEX_Q1_2026_B    = 2.9    # High; peak capex period

# ── SUBSCRIBER BASE ──────────────────────────────────────────────────────────
BROADBAND_SUBS_Q1_2026_M  = 29.6   # End Q1 2026 (peak was ~30.7M circa 2023)
BROADBAND_NET_Q1_2025     = -60000
BROADBAND_NET_Q2_2025     = -117000
BROADBAND_NET_Q3_2025     = -109000
BROADBAND_NET_Q4_2025     = -119000
BROADBAND_NET_Q1_2026     = -120000  # Worsening YoY from -60K Q1 2025; no bottom yet
BROADBAND_FY2025_NET      = -403000  # Full year 2025 net losses

VIDEO_SUBS_Q1_2026_M      = 12.5    # Q1 2026 loss: 51K (vs 167K Q1 2025 — big improvement)
MOBILE_LINES_Q1_2026_M    = 12.134  # End Q1 2026; 11.8M end of 2025
MOBILE_NET_Q4_2025        = 428000
MOBILE_NET_Q1_2026        = 368000  # Slight deceleration but still strong
MOBILE_YOY_GROWTH_PCT     = 17.1    # 17.1% YoY growth in mobile lines

# ── BALANCE SHEET ───────────────────────────────────────────────────────────
TOTAL_DEBT_B          = 94.3    # Q1 2026
LEVERAGE_RATIO        = 4.15    # Net Debt / LTM Adj. EBITDA (Q1 2026)
INTEREST_EXPENSE_ANN  = 4.9     # Annual interest; nearly equal to FCF
VARIABLE_RATE_PCT     = 13.0    # 13% of total debt at floating rates (~$12.2B)
FIXED_RATE_PCT        = 87.0    # 87% fixed — mitigates rate-rise risk

# ── CAPEX CYCLE AND FCF INFLECTION ──────────────────────────────────────────
CAPEX_FY2026_GUIDANCE  = 11.4   # Billion — modest decline from 2025
CAPEX_TARGET_2028      = 8.0    # Management targets <$8B post-network evolution
FCF_TARGET_2027_2028   = 8.5    # Management guidance: $8-9B FCF by 2027-2028
FCF_PER_SHARE_2025     = 39.30  # $5.0B / 127.23M shares = $39.30/share
FCF_YIELD_CURRENT      = 27.5   # 25%+ FCF yield at current price (FY2025 FCF basis)

# ── NETWORK EVOLUTION ────────────────────────────────────────────────────────
NETWORK_PCT_COMPLETE      = 50    # ~50% complete by end 2025
NETWORK_COMPLETE_YEAR     = 2026  # Remaining upgrades targeted for 2026
WIFI7_ROLLOUT_TARGET      = 2027  # Full footprint WiFi 7 + symmetrical multi-gig
DOCSIS_SPEED_GBPS         = 25    # Broadcom/Charter/Comcast 25Gbps chipset joint dev
NETWORK_SPEC              = "Invincible WiFi: WiFi 7 + 5G backup + battery backup"

# ── COX MERGER ───────────────────────────────────────────────────────────────
COX_ANNOUNCED             = "May 16, 2025"
COX_BROADBAND_SUBS_M      = 6.5     # Cox residential broadband subscribers
COX_REVENUE_B             = 12.0    # Approximate Cox annual revenue
COX_EBITDA_B              = 5.0     # Approximate Cox adjusted EBITDA
COMBINED_EBITDA_PRO_FORMA = 27.7    # Charter $22.7B + Cox $5.0B
LEVERAGE_TARGET_POST_COX  = 3.625   # Midpoint of 3.5-3.75× target within 3yr
COX_DEAL_STATUS           = "Pending regulatory approval; buybacks suspended Aug 2025"

# ── SPECTRUM MOBILE ──────────────────────────────────────────────────────────
MOBILE_PROFITABILITY      = "Profitable on pre-SAC basis (CEO confirmed)"
MVNO_PROVIDER             = "Verizon Wireless (10+ year MVNO agreement)"
WIFI_OFFLOAD_ADVANTAGE    = "Owned WiFi infrastructure reduces Verizon MVNO cost/GB"
CBRS_STATUS               = "CBRS spectrum deployment underway — further reduces MVNO costs"
MOBILE_BUNDLE_REQUIREMENT = "Must subscribe to Spectrum Internet (broadband retention multiplier)"

# ── ANALYST CONSENSUS ────────────────────────────────────────────────────────
FY2026_EPS_CONSENSUS      = 42.5    # Mid-range $41.78-$43.57
FY2026_REVENUE_CONSENSUS  = 54.5    # $54.3-54.7B
CONSENSUS_PT              = 295.0   # Midpoint of $283-$307 range
PT_LOW                    = 160.0   # Low-end analyst target
PT_HIGH                   = 500.0   # Bull-end analyst target
ANALYST_RATING_BUY        = 26      # Buy ratings
ANALYST_RATING_HOLD       = 25      # Hold ratings
ANALYST_RATING_SELL       = 4       # Sell ratings

# ── SCENARIOS ────────────────────────────────────────────────────────────────
# BEAR  $75:  Broadband losses persist at 400K+/yr; Cox adds debt, synergies disappoint;
#             EBITDA erodes to $20.5B; EV/EBITDA stays at 4.8× (leverage fear);
#             combined net debt ~$97B; equity value ~$2-5B → stock $15-40.
#             Use $75 as practical BEAR (market stops well above zero as debt is manageable).
#             Probability assigned by softmax at PROXY ~2.53.
#
# BASE  $240: Cox merger closes 2026; broadband losses slow to -50K/quarter by Q3 2026
#             (mobile bundling + network upgrades providing retention lift); capex declining
#             as guided; FCF reaches $6.5B in 2027; EV/EBITDA re-rates to 5.5×;
#             stock retraces toward analyst consensus low end.
#
# BULL  $380: Full capex inflection: FCF $8-9B by 2027-2028 as expected;
#             broadband returns to modest growth (Cox + rural BEAD + network evolution);
#             buybacks resume post-Cox close; EV/EBITDA 7× (cable historical average);
#             convergence story (broadband + mobile) fully valued.
#
# XBULL $550: Transformative Cox execution (synergies exceed $2B); Charter becomes
#             dominant US cable operator (36M+ broadband + 12M+ mobile);
#             FCF $10B+; leverages DOCSIS 4.0 to hold pricing power vs fiber;
#             EV/EBITDA 8× (pre-crisis Charter multiple); aggressive buybacks at current levels.
BEAR    = 75.0
BASE    = 240.0
BULL    = 380.0
XBULL   = 550.0

# ── EPP (EARNINGS POWER PRICE) ───────────────────────────────────────────────
# Trough scenario: high leverage + EBITDA erosion + elevated capex all at once.
# EPS trough uses: GAAP $36.21 but assume $15 in a true stress scenario
# (broadband ARPU erosion + Cox integration costs + higher interest on variable debt).
# Trough PE: 5× (cable operator in leverage distress; peers like Altice USA trade 2-4×).
EPS_TROUGH  = 15.00
PE_TROUGH   = 5.0
EPP         = EPS_TROUGH * PE_TROUGH   # = $75.00

# ── SCA: STRUCTURAL COMPETITIVE ADVANTAGE ───────────────────────────────────
# Charter has strong physical infrastructure moats but these are being challenged
# by FWA (T-Mobile, Verizon) and fiber overbuilders (AT&T, Frontier, Google Fiber).
# The DOCSIS 4.0 upgrade is Charter's answer — returning cable to technology leadership.

SCA_FACTORS = {
    # Factor                     : (score,  weight)
    "pricing_power"              : (+0.10,  0.12),  # Near-monopoly in footprint, but FWA capping pricing
    "switching_costs"            : (+0.15,  0.15),  # Broadband+mobile bundle, but customers ARE leaving
    "network_effects"            : ( 0.00,  0.10),  # Cable has minimal network effects
    "cost_efficiency_programming": (+0.25,  0.20),  # Programming cost decline as video exits; efficiency rising
    "scale_national"             : (+0.30,  0.15),  # 2nd-largest US cable; $55B revenue; post-Cox #1
    "franchise_territory_moat"   : (+0.10,  0.13),  # Historical franchise territories still provide density
    "infrastructure_asset_moat"  : (+0.35,  0.15),  # ~$100B of cable plant impossible to replicate; DOCSIS 4.0
}

SCA_NET  = sum(score * weight for score, weight in SCA_FACTORS.values())
# SCA_NET = 0.10×0.12 + 0.15×0.15 + 0×0.10 + 0.25×0.20 + 0.30×0.15 + 0.10×0.13 + 0.35×0.15
# SCA_NET ≈ 0.012 + 0.023 + 0 + 0.050 + 0.045 + 0.013 + 0.053 = 0.196

SCA_SCALE = 0.45  # Fixed framework parameter

# ── 6 PROXY SIGNALS ──────────────────────────────────────────────────────────
# Signal   (score 1–4, weight)
# 1=BEAR, 1.5=BEAR+, 2=BASE, 2.5=BASE+, 3=BULL, 3.5=BULL+, 4=XBULL

SIGNALS = {
    # The most critical near-term driver. Charter lost 403K broadband subs in FY2025
    # and 120K in Q1 2026 — worsening YoY. FWA capacity: T-Mobile+Verizon have room
    # for 32M FWA subs (currently 15.5M combined). Fiber overbuilds expanding.
    # BUT: mobile bundling is improving retention; network upgrades will restore speeds;
    # cable sector forecast to return to broadband growth in 2026; ACP headwind clearing.
    "broadband_subscriber_trajectory": (2.0, 0.25),

    # THE dominant risk. $94.3B total debt at 4.15× EBITDA. Interest expense $4.9B/year
    # ≈ full annual FCF. Cox merger adds debt spike before synergies. 13% variable rate
    # ($12.2B exposure). BUT: 87% fixed; management targets 3.5-3.75× within 3yr;
    # FCF covers interest comfortably; Cox adds $5B EBITDA (de-levers on pro-forma basis).
    "leverage_and_cox_deal_risk": (1.5, 0.25),

    # THE bull thesis. CapEx $11.7B→$11.4B→<$8B (2028) = $3.7B+ annual FCF release.
    # FCF already inflecting: $4.3B (2024)→$5.0B (2025)→$5.6B annualized Q1 2026.
    # At $8B FCF / ~120M shares = $66.67/share FCF; at 5× P/FCF = $333/share.
    # Network evolution capex cliff is one of the most powerful re-rating catalysts in US telecom.
    "fcf_inflection_capex_peak": (3.5, 0.20),

    # 12.1M mobile lines, +17% YoY, 368K Q1 2026 adds. Profitable pre-SAC.
    # Bundle requirement (must have Spectrum Internet) = broadband retention force multiplier.
    # WiFi offload reduces Verizon MVNO cost/GB. CBRS deployment adds own spectrum.
    # Comcast comparison: Charter 12.1M vs Comcast 9.3M — Charter winning mobile.
    "spectrum_mobile_retention_engine": (3.0, 0.15),

    # DOCSIS 4.0 + WiFi 7 = "Invincible WiFi": symmetrical multi-gig, 5G backup, battery.
    # 25Gbps chipset (Broadcom/Charter/Comcast joint development). 50% complete end 2025;
    # full footprint by 2027. This is Charter's answer to fiber — DOCSIS 4.0 at 25Gbps
    # will match or exceed GPON fiber on speed AND exceed it on latency.
    "network_evolution_docsis40": (3.0, 0.10),

    # EV/EBITDA 5.0× vs historical 8-10×. P/E 3.9×. FCF yield 25%+.
    # Analyst consensus PT $295 (2.1× current). 52-week high was $437 (3.1× current).
    # AT&T trades 6.5×, Comcast 6.8×, T-Mobile 11×. Charter at 5× prices in catastrophe.
    "valuation_historical_discount": (4.0, 0.05),
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

# Conservative 2yr: EPS FY2026E × moderate PE + 2yr dividends (no heroic multiple expansion)
EPS_FY2026E     = 42.5
PE_CONSERVATIVE = 5.5   # Only modest expansion from current 3.9× (charter-specific credit)
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
    print(f"  Revenue:        ${REVENUE_FY2025_B:.1f}B  (YoY: -0.6%)")
    print(f"  Adj. EBITDA:    ${EBITDA_FY2025_B:.1f}B  (YoY: +0.6%)")
    print(f"  Free Cash Flow: ${FCF_FY2025_B:.1f}B  (YoY: +16%)")
    print(f"  GAAP EPS:       ${GAAP_EPS_FY2025:.2f}")
    print(f"  CapEx:          ${CAPEX_FY2025_B:.1f}B  (including $3.9B line extensions)")
    print(f"  Interest Exp.:  ${INTEREST_EXPENSE_ANN:.1f}B/yr  (87% fixed / 13% variable)")

    print(f"\n  Q1 2026:")
    print(f"    Revenue: ${REVENUE_Q1_2026_B:.1f}B  |  EBITDA: ${EBITDA_Q1_2026_B:.1f}B (-2.2% YoY)")
    print(f"    EPS: ${GAAP_EPS_Q1_2026:.2f} (missed $10.32E)  |  FCF: ${FCF_Q1_2026_B:.1f}B  |  CapEx: ${CAPEX_Q1_2026_B:.1f}B")

    print(f"\n{sep}")
    print("  SUBSCRIBER TRENDS")
    print(sep)
    print(f"  Broadband (end Q1 2026): {BROADBAND_SUBS_Q1_2026_M:.1f}M subs")
    print(f"    Q1 2025: {BROADBAND_NET_Q1_2025:+,}  |  Q2 2025: {BROADBAND_NET_Q2_2025:+,}")
    print(f"    Q3 2025: {BROADBAND_NET_Q3_2025:+,}  |  Q4 2025: {BROADBAND_NET_Q4_2025:+,}  |  Q1 2026: {BROADBAND_NET_Q1_2026:+,}")
    print(f"    FY2025 net: {BROADBAND_FY2025_NET:+,}  — no sign of stabilization yet")
    print(f"  Video (Q1 2026): {VIDEO_SUBS_Q1_2026_M:.1f}M  (Q1 loss: 51K vs 167K year-ago — big improvement)")
    print(f"  Mobile lines (Q1 2026): {MOBILE_LINES_Q1_2026_M:.3f}M  (+{MOBILE_YOY_GROWTH_PCT:.1f}% YoY)")
    print(f"    Q4 2025: +{MOBILE_NET_Q4_2025:,}  |  Q1 2026: +{MOBILE_NET_Q1_2026:,}")
    print(f"    Charter LEADS Comcast: 12.1M vs 9.3M mobile lines")

    print(f"\n{sep}")
    print("  BALANCE SHEET & LEVERAGE")
    print(sep)
    print(f"  Total Debt:         ${TOTAL_DEBT_B:.1f}B")
    print(f"  Leverage:           {LEVERAGE_RATIO:.2f}× Net Debt/EBITDA  (target: {LEVERAGE_TARGET_POST_COX:.3f}× within 3yr post-Cox)")
    print(f"  Interest Expense:   ${INTEREST_EXPENSE_ANN:.1f}B/yr  (coverage ratio: {EBITDA_FY2025_B/INTEREST_EXPENSE_ANN:.1f}×)")
    print(f"  Variable Rate Debt: {VARIABLE_RATE_PCT:.0f}% of total (${TOTAL_DEBT_B * VARIABLE_RATE_PCT/100:.1f}B floating exposure)")

    print(f"\n{sep}")
    print("  CAPEX CYCLE & FCF INFLECTION — THE BULL THESIS")
    print(sep)
    print(f"  FY2025 CapEx:  ${CAPEX_FY2025_B:.1f}B  (cycle peak)")
    print(f"  FY2026 CapEx:  ${CAPEX_FY2026_GUIDANCE:.1f}B  (guided)")
    print(f"  2028 CapEx:    <${CAPEX_TARGET_2028:.1f}B  (management target)")
    print(f"  CapEx delta:   -${CAPEX_FY2025_B - CAPEX_TARGET_2028:.1f}B release → adds ${CAPEX_FY2025_B - CAPEX_TARGET_2028:.1f}B to FCF")
    print(f"  FCF target 2027-2028: ${FCF_TARGET_2027_2028:.1f}B  (vs $5.0B in 2025)")
    print(f"  FCF/share (normalized 2028): ~${FCF_TARGET_2027_2028*1000/SHARES_OUT_M:.0f}/share")
    print(f"  At current price: P/FCF(2028E) = {CURRENT_PRICE/(FCF_TARGET_2027_2028*1000/SHARES_OUT_M):.1f}×  (EXTREME value)")

    print(f"\n{sep}")
    print("  COX MERGER")
    print(sep)
    print(f"  Announced: {COX_ANNOUNCED} (stock was at $437 — same-day high)")
    print(f"  Cox broadband: ~{COX_BROADBAND_SUBS_M:.1f}M subs  |  Revenue: ~${COX_REVENUE_B:.0f}B  |  EBITDA: ~${COX_EBITDA_B:.0f}B")
    print(f"  Combined EBITDA (pro-forma): ${COMBINED_EBITDA_PRO_FORMA:.1f}B")
    print(f"  Combined entity: {BROADBAND_SUBS_Q1_2026_M + COX_BROADBAND_SUBS_M:.1f}M broadband subs = #1 US cable operator")
    print(f"  Status: {COX_DEAL_STATUS}")
    print(f"  Leverage on pro-forma combined EBITDA: debt ${TOTAL_DEBT_B:.1f}B+ / EBITDA ${COMBINED_EBITDA_PRO_FORMA:.1f}B")
    print(f"  = ~{TOTAL_DEBT_B/COMBINED_EBITDA_PRO_FORMA:.2f}× pro-forma (much less alarming than 4.15× Charter-standalone)")

    print(f"\n{sep}")
    print("  NETWORK EVOLUTION (DOCSIS 4.0)")
    print(sep)
    print(f"  Status: ~{NETWORK_PCT_COMPLETE}% complete by end 2025; remaining work 2026")
    print(f"  {NETWORK_SPEC}")
    print(f"  Speed: {DOCSIS_SPEED_GBPS}Gbps chipset (joint dev w/ Comcast & Broadcom)")
    print(f"  Full WiFi 7 footprint: {WIFI7_ROLLOUT_TARGET}")
    print(f"  Symmetric multi-gig = MATCHES fiber on upload (cable's historic weakness)")

    print(f"\n{sep}")
    print("  6 PROXY SIGNALS")
    print(sep)
    labels = {
        "broadband_subscriber_trajectory": "Broadband sub trajectory",
        "leverage_and_cox_deal_risk":       "Leverage & Cox deal risk",
        "fcf_inflection_capex_peak":        "FCF inflection / capex peak",
        "spectrum_mobile_retention_engine": "Spectrum Mobile retention",
        "network_evolution_docsis40":       "Network Evolution DOCSIS 4.0",
        "valuation_historical_discount":    "Valuation vs. historical",
    }
    for k, (score, weight) in SIGNALS.items():
        bar = "█" * int(score * 5)
        print(f"  {labels[k]:<35}  {score:.1f}  wt={weight:.2f}  {bar}")
    print(f"  {'PROXY COMPOSITE':<35}  {PROXY_COMPOSITE:.2f}")

    print(f"\n{sep}")
    print("  SCA — STRUCTURAL COMPETITIVE ADVANTAGE")
    print(sep)
    sca_labels = {
        "pricing_power":               "Pricing power (FWA limiting)",
        "switching_costs":             "Switching costs (bundle stickiness)",
        "network_effects":             "Network effects",
        "cost_efficiency_programming": "Cost efficiency (video exit)",
        "scale_national":              "Scale (2nd-largest → #1 post-Cox)",
        "franchise_territory_moat":    "Franchise territory moat",
        "infrastructure_asset_moat":   "Infrastructure asset (~$100B plant)",
    }
    for k, (score, weight) in SCA_FACTORS.items():
        print(f"  {sca_labels[k]:<38}  {score:+.2f} × {weight:.2f} = {score*weight:+.4f}")
    print(f"  {'SCA_NET':<38}  {SCA_NET:+.4f}")
    print(f"  ADJ contribution (+0.45 × SCA_NET × 0.5): {SCA_SCALE * SCA_NET * 0.5:+.4f}")

    print(f"\n{sep}")
    print("  COMPOSITE SCORES")
    print(sep)
    print(f"  PROXY_COMPOSITE:    {PROXY_COMPOSITE:.4f}")
    print(f"  ADJ_COMPOSITE:      {ADJ_COMPOSITE:.4f}")
    print(f"  MARKET_COMPOSITE:   {MARKET_COMPOSITE:.4f}  (back-solved from ${CURRENT_PRICE}×1.15²=${TARGET_MARKET:.2f})")
    print(f"  ADJ_VS_MARKET:      {ADJ_VS_MARKET:+.4f}  → {'SIGNIFICANTLY UNDERVALUED' if ADJ_VS_MARKET > 0.5 else 'MODERATELY UNDERVALUED' if ADJ_VS_MARKET > 0.2 else 'FAIRLY VALUED'}")

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
    print(f"  FY2026E EPS consensus:  ${EPS_FY2026E:.2f}")
    print(f"  Conservative PE applied: {PE_CONSERVATIVE:.1f}× (no heroic multiple expansion required)")
    print(f"  Target price 2yr:       ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.1f}× + ${2*ANNUAL_DIV:.2f} div = ${PRICE_2YR_CONSV:.2f}")
    print(f"  2-year return:          {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  Note: Only needs PE to expand from 3.9× → 5.5× (consensus ~7×).")
    print(f"  At consensus 7× PE: EPS $42.5 × 7 + $2.80 = $300.30 → +110%/2yr = +44%/yr")

    print(f"\n{sep}")
    print("  WHY THIS IS A HIGH-RISK ◉ BUY")
    print(sep)
    print("""
  Charter is not a comfortable BUY — it is a LEVERAGED TURNAROUND BUY.
  The stock fell 67% for valid reasons: broadband sub losses are real,
  the Cox deal adds debt before synergies, and capex is still elevated.

  BUT at $143, the market is ALREADY pricing in ALL of these negatives:

  WHAT THE MARKET PRICES IN (at $143):
  • Broadband sub losses NEVER stabilize (perpetual -120K/quarter)
  • Cox deal has NO synergies and INCREASES leverage
  • Capex NEVER declines (network evolution fails)
  • FCF stays at $5B forever (no $8-9B target achieved)
  • PE stays at 3.9× forever (permanent multiple depression)

  WHY EACH OF THOSE IS WRONG:
  1. Mobile convergence (12.1M lines, +17% YoY) provides broadband floor
  2. Cox combined EBITDA $27.7B → pro-forma leverage is 3.4×, NOT 4.15×
  3. Management capex path: $11.7B → $11.4B → <$8B = confirmed declining
  4. FCF: $4.3B (2024) → $5.0B (2025) = ALREADY inflecting; $8-9B is 2yr away
  5. At $66/share FCF by 2028, ANY multiple above 3× justifies $200+ stock

  THE RISK:
  • EBITDA erodes below $21B while Cox adds $97B→$120B+ debt before close
  • Variable rate debt (13%) = $12.2B exposed to rate spikes
  • Regulatory rejection of Cox deal (unlikely but non-zero)
  • FWA absorbs 30M+ subscribers, structurally impairs cable broadband
  • In a true bear, equity value approaches zero (EV/EBITDA 4.7× on $20B EBITDA = $94B EV vs $97B debt)

  POSITION SIZING GUIDANCE:
  • This warrants a SMALLER position than CMCSA or VZ given leverage risk
  • CMCSA (ratio B 0.39×, EPP gap -13.5%, 2.33× leverage) is LOWER RISK
  • CHTR (ratio B 0.29×, higher reward but 4.15× leverage) is HIGHER RISK
  • Conviction BUY below $125 (where standalone FCF yield exceeds 30%)
  • At $142: BUY, but size for the leverage risk
""")

    print(SEP)
    print(f"""
SUMMARY: CHTR ◉ BUY — Ratio B 0.29× (47.4% downside / 166.1% upside). HIGH-LEVERAGE \
DEEP VALUE: stock fell 67% from 52-week high ($437→$143) as market prices in broadband \
sub losses + Cox merger leverage fear. At $143: EV/EBITDA 5.0× (cable historical 8-10×), \
P/E 3.9×, FCF yield 25%+. FY2025: revenue $54.8B, EBITDA $22.7B, FCF $5.0B (+16%). \
Broadband: 29.6M subs, -120K/quarter (FWA + fiber); mobile: 12.1M lines (+17% YoY). \
CAPEX CLIFF: $11.7B→$11.4B→<$8B (2028) = FCF inflects to $8-9B by 2027-2028. \
Network Evolution: DOCSIS 4.0, WiFi 7, symmetrical multi-gig; 50% complete → 2026/2027 \
full rollout. Cox merger (May 2025): adds 6.5M subs + ~$5B EBITDA; pro-forma leverage \
~3.4× (much less alarming than standalone 4.15×); target 3.5-3.75× within 3yr post-close. \
$94.3B debt (4.15× EBITDA); buybacks suspended (was $5.4B in 2025). Analyst consensus PT \
$295 (2.1× current), range $160-$500. Conservative 2yr: EPS $42.5 × 5.5× + $2.80 div = \
$236 → +65.7% (+28.2%/yr). HIGH-RISK BUY: size smaller than CMCSA/VZ given leverage. \
Bear $75 · Base $240 · Bull $380 · XBull $550.
""")

    print(f"SIGNAL: {SIGNAL_TEXT} (high-leverage turnaround) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
