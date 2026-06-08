"""
Phillips 66 (NYSE: PSX)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.93×  |  EPP Gap: +177.4%

INTEGRATED ENERGY NEAR HIGHS — REFINING SUPERCYCLE + MIDSTREAM SCALING + ACTIVIST CATALYST
Trading near 52-week highs ($183 vs $191 high, up from $111 low) on:
  (1) Refining margin surge — realized margin $10.11/bbl in Q1 2026 vs $6.81/bbl Q1 2025 (+48% YoY)
      on structural capacity tightness (~550K bpd of US refinery closures within 18 months;
      Dec 2025 utilization hit 94.8% — well above the ~90% historical average)
  (2) Midstream scaling toward a $4.5B EBITDA target by 2027 (DCP Midstream synergies running
      at $500M realized vs the original $300M target — a ~67% beat)
  (3) Elliott Management's activist campaign ($2.5B stake, "Streamline66" thesis claiming up to
      $40B of value unlock from separating Midstream/Chemicals) remains a live, binary catalyst
      after a split 2-2 board vote (May 2025) and a governance détente (Mar 2026)

At $183: consensus analyst price target is $180.95 — essentially "fairly priced" — on a forward
PE of ~13.2× against FY2026E consensus EPS of $13.88. This is NOT a deep-value situation like
CHTR; it is a quality integrated energy compounder trading close to fair value, with embedded
optionality: if Elliott (or the market) eventually forces a structural separation of Midstream
and/or Chemicals at peer multiples, the re-rating could be substantial.

Conviction: MODERATE on the base case (steady compounding via dividend growth + buybacks +
midstream EBITDA ramp); HIGHER on the asymmetric Elliott catalyst (a $40B gap that someone —
activist, management, or an acquirer — eventually has incentive to close).
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "PSX"
COMPANY         = "Phillips 66"
SECTOR          = "Refining · Midstream (DCP) · Chemicals (CPChem JV) · Marketing & Specialties · NYSE: PSX"
SECTOR_GROUP    = "Energy"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 183.08   # Early June 2026
ANNUAL_DIV      = 5.08     # $1.27/quarter, raised +7% in Feb 2026 (from $1.20)
SHARES_OUT_M    = 403.7    # ~$2.6B adj. earnings / $6.44 adj. EPS
MARKET_CAP_B    = 73.4
FW52_HIGH       = 190.61
FW52_LOW        = 111.37

# ── FY2025 FULL-YEAR FINANCIALS ─────────────────────────────────────────────
REVENUE_FY2025_B        = 145.5   # Total revenue & other income
ADJ_EARNINGS_FY2025_B   = 2.6     # Includes $964mm pre-tax accelerated D&A (LA refinery closure)
ADJ_EPS_FY2025          = 6.44
GAAP_NET_INCOME_FY2025_B = 4.4
GAAP_EPS_FY2025         = 10.90   # $4.4B / 403.7M shares
MIDSTREAM_EBITDA_FY2025_B = 3.8   # Record NGL transport/fractionation volumes in Q4
ROCE_10YR_AVG_PCT       = 5.4     # Company-disclosed 10-yr average ROCE
CROIC_PCT               = 13.2    # Cash return on invested capital — ~2× peer average
PEER_CROIC_PCT          = 9.3

# ── Q4 2025 / Q1 2026 SNAPSHOT ──────────────────────────────────────────────
Q4_2025_NET_INCOME_B    = 2.9     # $7.17/sh GAAP
Q4_2025_ADJ_EARNINGS_B  = 1.0
Q4_2025_ADJ_EBITDA_B    = 2.5     # +124% YoY
Q4_2025_OCF_B           = 2.8     # +129% YoY
Q1_2026_REFMARGIN_BBL   = 10.11   # Realized refining margin, $/bbl
Q1_2025_REFMARGIN_BBL   = 6.81    # Year-ago comparison (+48% YoY improvement)
CRACK_SPREAD_YOY_PCT    = 73      # US 3-2-1 crack spread, average YoY increase into Q1 2026
Q1_2026_UTILIZATION_PCT = 95
FY2026_UTIL_GUIDANCE    = "low 90% range"
DEC_2025_INDUSTRY_UTIL_PCT = 94.8 # US industry-wide utilization (17.0M bpd throughput)

# ── BALANCE SHEET ───────────────────────────────────────────────────────────
GROSS_DEBT_B            = 27.1    # ~$8.4B short-term + ~$18.7B long-term (Q1 2026 10-Q)
LIQUIDITY_B             = 6.0
CREDIT_RATING_MOODYS    = "Baa2"
CREDIT_RATING_SP        = "BBB-"
NEAR_TERM_MATURITY      = "Oct 2026 (3.550% senior notes); staggered through 2027-2029, out to 2055"

# ── CAPITAL ALLOCATION & 2026 CAPEX ─────────────────────────────────────────
QUARTERLY_DIV           = 1.27    # Raised from $1.20 (+7%) in Feb 2026
DIV_RAISE_PCT           = 7
BUYBACK_Q1_2026_M       = 269     # $269mm repurchased in Q1 2026 alone
CUMULATIVE_RETURNS_SINCE_2012_B = 43   # Cumulative shareholder returns since 2012 spin-off
RETURN_POLICY_OCF_PCT   = 50      # Stated policy: return >50% of operating cash flow
CAPEX_2026_TOTAL_B      = 2.4     # Up from $2.1B in 2025
CAPEX_2026_SUSTAINING_B = 1.1
CAPEX_2026_GROWTH_B     = 1.3
CAPEX_MIDSTREAM_B       = 1.1     # $400mm sustaining + $700mm growth
CAPEX_REFINING_B        = 1.1     # $590mm sustaining + $520mm growth
CAPEX_CHEMICALS_B       = 0.68    # CPChem JV proportionate share (self-funded)

# ── REFINING SEGMENT ────────────────────────────────────────────────────────
REFINING_CAPACITY_MBD   = 2200    # ~2.2 million bpd net crude capacity, 13 refineries
LA_REFINERY_CLOSURE_MBD = 138.7   # Phased 2025 closure — ~17% of CA refining capacity
US_CAPACITY_EXIT_MBD    = 550     # Industry-wide permanent US closures within ~18 months
                                  # (PES Philadelphia 335, LyondellBasell Houston 264,
                                  #  PSX LA 138.7, Valero Benicia 170 — partial overlap/phasing)
REFINING_SWING_Q1_2026_M = 208    # Adj. earnings swing: -$937mm (Q1'25 loss) -> +$208mm (Q1'26)

# ── MIDSTREAM / DCP INTEGRATION ─────────────────────────────────────────────
DCP_SYNERGY_TARGET_M     = 300    # Original synergy target on full DCP ownership (2023)
DCP_SYNERGY_REALIZED_M   = 500    # Realized — ~67% above original target
MIDSTREAM_EBITDA_TARGET_2027_B = 4.5   # Management run-rate target by year-end 2027
MIDSTREAM_GROWTH_PROJECTS = "Coastal Bend acquisition (2025); Dos Picos II Permian gas-processing expansion (ahead of schedule, on budget)"
CPCHEM_NET_INCOME_Q1_2026_M = 228 # CPChem (50/50 Chevron JV) Q1 2026 net income

# ── ELLIOTT MANAGEMENT ACTIVIST CAMPAIGN ────────────────────────────────────
ELLIOTT_CAMPAIGN_START   = "November 2023"
ELLIOTT_STAKE_B          = 2.5    # ~5.7% — one of PSX's five largest holders
ELLIOTT_STAKE_PCT        = 5.7
STREAMLINE66_UNLOCK_B    = 40     # Elliott's claimed value-unlock potential ($/share ≈ $99 on 403.7M sh)
PROXY_VOTE_DATE          = "May 21, 2025"
PROXY_VOTE_RESULT        = "Split 2-2: Elliott nominees Cornelius & Heim elected; PSX's Pease & Hearne retained; Lowe & Ungerleider lost seats"
RETAIL_DIVESTITURES      = "Sold 65% of Germany/Austria JET retail (~1,270 sites, closed Dec 2025); exited Coop Mineraloel AG and Gulf Coast Express Pipeline stake"
SETTLEMENT_STATUS        = "Détente reached Mar 2026 (2 new independent directors + supportive Elliott statement) — core Midstream/Chemicals separation ask remains UNRESOLVED"

# ── ANALYST CONSENSUS ────────────────────────────────────────────────────────
FY2026_EPS_CONSENSUS     = 13.88
FY2026_REVENUE_CONSENSUS_B = 150.1
CONSENSUS_PT             = 180.95   # ~= current price -> "fairly priced" per consensus
PT_LOW                   = 138.0
PT_HIGH                  = 213.0
PT_2027_AVG              = 161.70   # 2027 average PT trend (lower — moderation expected)
ANALYST_RATING_NOTE      = "Goldman $186 (Neutral), UBS $212, Morgan Stanley $174 (Overweight), Jefferies $158, Mizuho raised but Neutral"

# ── SCENARIOS ────────────────────────────────────────────────────────────────
# BEAR  $135: Refining margin reversion (the ~$945mm one-off gain proves non-recurring;
#             Brent falls $5-8/bbl as Iran/Russia sanctions ease, compressing crack spreads
#             back toward the historical 3.3% margin regime); Elliott campaign loses momentum
#             post-détente with no structural action; multiple compresses toward 10-11×.
#             Diversified earnings (midstream $3.8B+ EBITDA, CPChem, marketing) provide a
#             floor well above a pure-play refiner's bear case — hence not below $130.
#
# BASE  $190: Consensus scenario — realized near 52-week highs. Refining margins moderate
#             but stay constructive on continued capacity tightness; Midstream EBITDA grows
#             toward ~$4.2B (just shy of the $4.5B/2027 target); dividend keeps compounding
#             at ~7%/yr; buybacks continue at ~$1B/yr pace; Elliott détente holds without
#             a structural separation. Essentially "consensus PT $181" realized + drift.
#
# BULL  $235: Refining supercycle persists through 2027 (sustained ~550K bpd of permanent
#             US/EU closures, no major new capacity, EIA's 21-day jet-fuel supply low);
#             Midstream hits the $4.5B EBITDA target on schedule; Elliott pressure forces a
#             PARTIAL structural step (e.g., Midstream carve-out filing or JV restructuring)
#             that re-rates the segment toward pure-play NGL/midstream multiples (8-10× EBITDA
#             vs. ~6× embedded today).
#
# XBULL $290: Full "Streamline66" thesis realized — Midstream and/or Chemicals separated at
#             peer multiples, unlocking a meaningful share of Elliott's claimed ~$40B
#             ($40B / 403.7M sh ≈ $99/share before execution discount); refining supercycle
#             and capital-return compounding continue in parallel. Requires real structural
#             action — the highest-conviction, lowest-probability outcome.
BEAR    = 135.0
BASE    = 190.0
BULL    = 235.0
XBULL   = 290.0

# ── EPP (EARNINGS POWER PRICE) ───────────────────────────────────────────────
# Trough scenario: a severe refining downcycle (2020-COVID-style demand collapse, or a
# 2023-style margin compression) drags consolidated EPS down sharply even with Midstream/
# Chemicals diversification cushioning the blow. Trough PE reflects how integrated energy
# names re-rate in deep cyclical troughs (10-12×, slightly above pure refiners given the
# diversified, more annuity-like Midstream/Marketing earnings stream).
EPS_TROUGH  = 6.00
PE_TROUGH   = 11.0
EPP         = EPS_TROUGH * PE_TROUGH   # = $66.00

# ── SCA: STRUCTURAL COMPETITIVE ADVANTAGE ───────────────────────────────────
# PSX's moat rests on integration (refining + midstream + chemicals + marketing smooths
# segment-level cyclicality) and Gulf Coast scale/infrastructure — but it is a maturing,
# capital-intensive industry facing a real long-run secular demand headwind from EVs, and
# governance is currently contested (Elliott overhang cuts both ways).

SCA_FACTORS = {
    # Factor                            : (score,  weight)
    "integrated_value_chain"            : (+0.30,  0.18),  # Refining+Midstream+Chemicals+Marketing smooths cyclicality
    "gulf_coast_scale_advantage"        : (+0.30,  0.16),  # 2.2M bpd, 13 refineries, export infrastructure, cheap feedstock
    "midstream_infrastructure_moat"     : (+0.35,  0.15),  # DCP "wellhead-to-market" NGL network — high replication barriers
    "cpchem_petrochemical_scale"        : (+0.20,  0.12),  # 50/50 Chevron JV; Golden Triangle Polymers buildout
    "capital_discipline_track_record"   : (+0.05,  0.13),  # CROIC 13.2% (2x peers) but 10-yr avg ROCE only 5.4% — mixed
    "governance_activist_overhang"      : (-0.05,  0.12),  # Elliott forces discipline/pruning, but creates distraction & uncertainty
    "secular_demand_transition_exposure": (-0.15,  0.14),  # EV adoption structurally erodes long-run gasoline demand
}

SCA_NET  = sum(score * weight for score, weight in SCA_FACTORS.values())
# SCA_NET = 0.30×0.18 + 0.30×0.16 + 0.35×0.15 + 0.20×0.12 + 0.05×0.13 + (-0.05)×0.12 + (-0.15)×0.14
# SCA_NET ≈ 0.054 + 0.048 + 0.0525 + 0.024 + 0.0065 - 0.006 - 0.021 = 0.1575

SCA_SCALE = 0.45  # Fixed framework parameter

# ── 6 PROXY SIGNALS ──────────────────────────────────────────────────────────
# Signal   (score 1–4, weight)
# 1=BEAR, 1.5=BEAR+, 2=BASE, 2.5=BASE+, 3=BULL, 3.5=BULL+, 4=XBULL

SIGNALS = {
    # Realized refining margin nearly doubled YoY ($6.81 -> $10.11/bbl) on structural
    # capacity tightness: ~550K bpd of permanent US closures within 18 months, December
    # 2025 industry utilization at 94.8% (vs ~90% historical average), EIA forecasting
    # jet-fuel supply at the lowest days-of-cover since 1963. Strong tailwind, but cyclical
    # — a chunk of the Q1 2026 beat reflects a one-off ~$945mm gain whose durability is
    # genuinely debated by sell-side (Goldman flagged Brent downside risk of $5-8/bbl).
    "refining_margin_supercycle_tightness": (3.0, 0.20),

    # THE structural growth engine. DCP Midstream synergies running at $500mm realized —
    # 67% above the original $300mm target — with management guiding to $4.5B run-rate
    # Midstream EBITDA by year-end 2027 (vs. $3.8B FY2025). Coastal Bend acquisition and
    # Dos Picos II Permian expansion both ahead of schedule and on budget. This is the
    # segment management is "doubling down" on — and the one Elliott wants to monetize.
    "midstream_dcp_growth_engine": (3.5, 0.20),

    # A genuinely binary, asymmetric catalyst. Elliott built a $2.5B (~5.7%) stake, ran a
    # full proxy contest (May 2025, ended split 2-2), and published a 138-page "Streamline66"
    # thesis claiming up to $40B (~$99/share) of value is unlockable via Midstream/Chemicals
    # separation. A March 2026 governance détente (2 new independent directors, supportive
    # Elliott statement) cooled tensions WITHOUT resolving the core structural ask — keeping
    # the option alive that Elliott (or a future activist) re-escalates if the discount persists.
    "elliott_streamline66_catalyst": (3.0, 0.15),

    # The honest bear case: a meaningful share of the Q1 2026 refining beat reflects a
    # one-time ~$945mm gain rather than a durable re-rating of margins; Goldman models
    # Brent falling $5-8/bbl if Iran/Russia sanctions ease, which would compress crack
    # spreads sharply; several houses (Goldman, Mizuho) raised price targets but kept
    # NEUTRAL ratings — signalling the recent run is substantially priced in already.
    "refining_margin_reversion_risk": (2.0, 0.15),

    # Best-in-class capital returns: dividend raised +7% to $5.08/yr (~2.8% yield, ~10%
    # CAGR since early 2025), $269mm of buybacks in Q1 2026 alone, $43B cumulative returns
    # since the 2012 spin-off, and CROIC of 13.2% — roughly DOUBLE the 9.3% peer average.
    # Stated policy of returning >50% of operating cash flow to shareholders is a durable
    # compounding mechanism independent of the cycle.
    "capital_return_compounding_machine": (3.5, 0.20),

    # Long-run structural headwind: EVs displaced ~3.5% of US gasoline demand in 2024,
    # projected ~7.1% by 2030 (CA gasoline already down ~13% since 2017). This directly
    # forced the LA refinery's phased closure and Rodeo's conversion to renewable fuels.
    # PSX is repositioning toward distillate/diesel/jet/petrochemicals (less EV-exposed),
    # but the secular arc for traditional gasoline refining is unmistakably down over the
    # next decade — a real ceiling on the size of the long-term bull case.
    "secular_ev_demand_transition_risk": (2.0, 0.10),
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

# Conservative 2yr: EPS FY2026E × modest PE + 2yr dividends (no heroic multiple expansion)
EPS_FY2026E     = 13.88
PE_CONSERVATIVE = 13.5   # Modest expansion from ~13.2× current forward multiple
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
    print(f"  Adj. Earnings:     ${ADJ_EARNINGS_FY2025_B:.1f}B  (${ADJ_EPS_FY2025:.2f}/sh — incl. $964mm LA refinery accel. D&A charge)")
    print(f"  GAAP Net Income:   ${GAAP_NET_INCOME_FY2025_B:.1f}B  (${GAAP_EPS_FY2025:.2f}/sh)")
    print(f"  Midstream EBITDA:  ${MIDSTREAM_EBITDA_FY2025_B:.1f}B  (record NGL transport/fractionation volumes Q4)")
    print(f"  ROCE (10yr avg):   {ROCE_10YR_AVG_PCT:.1f}%   |   CROIC: {CROIC_PCT:.1f}% (vs. peer avg {PEER_CROIC_PCT:.1f}% — ~2× best-in-class)")

    print(f"\n  Q4 2025 / Q1 2026:")
    print(f"    Q4'25 net income ${Q4_2025_NET_INCOME_B:.1f}B | adj. EBITDA ${Q4_2025_ADJ_EBITDA_B:.1f}B (+124% YoY) | OCF ${Q4_2025_OCF_B:.1f}B (+129% YoY)")
    print(f"    Realized refining margin: ${Q1_2026_REFMARGIN_BBL:.2f}/bbl (Q1'26) vs ${Q1_2025_REFMARGIN_BBL:.2f}/bbl (Q1'25) — +48% YoY")
    print(f"    US 3-2-1 crack spread averaged +{CRACK_SPREAD_YOY_PCT}% YoY; refining swung from -$937mm to +${REFINING_SWING_Q1_2026_M}mm adj. earnings")
    print(f"    Utilization: {Q1_2026_UTILIZATION_PCT}% (Q1'26); FY2026 guided to '{FY2026_UTIL_GUIDANCE}'; industry-wide Dec'25 at {DEC_2025_INDUSTRY_UTIL_PCT:.1f}%")

    print(f"\n{sep}")
    print("  BALANCE SHEET")
    print(sep)
    print(f"  Gross Debt:      ${GROSS_DEBT_B:.1f}B   |   Liquidity: ${LIQUIDITY_B:.1f}B")
    print(f"  Credit Ratings:  {CREDIT_RATING_MOODYS} (Moody's) / {CREDIT_RATING_SP} (S&P) — low investment grade")
    print(f"  Maturities:      {NEAR_TERM_MATURITY}")

    print(f"\n{sep}")
    print("  CAPITAL ALLOCATION & 2026 CAPEX")
    print(sep)
    print(f"  Dividend:        ${QUARTERLY_DIV:.2f}/qtr (${ANNUAL_DIV:.2f}/yr, +{DIV_RAISE_PCT}% raise Feb 2026) — yield ~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}%")
    print(f"  Buybacks:        ${BUYBACK_Q1_2026_M}mm in Q1 2026 alone")
    print(f"  Track record:    ${CUMULATIVE_RETURNS_SINCE_2012_B}B cumulative shareholder returns since 2012 spin-off")
    print(f"  Policy:          Return >{RETURN_POLICY_OCF_PCT}% of operating cash flow to shareholders")
    print(f"  2026 Capex:      ${CAPEX_2026_TOTAL_B:.1f}B total (${CAPEX_2026_SUSTAINING_B:.1f}B sustaining + ${CAPEX_2026_GROWTH_B:.1f}B growth)")
    print(f"    Midstream ${CAPEX_MIDSTREAM_B:.1f}B | Refining ${CAPEX_REFINING_B:.1f}B | Chemicals (CPChem, proportionate) ${CAPEX_CHEMICALS_B:.2f}B")

    print(f"\n{sep}")
    print("  REFINING SEGMENT — STRUCTURAL TIGHTNESS")
    print(sep)
    print(f"  Capacity: ~{REFINING_CAPACITY_MBD:,} Mbpd across 13 refineries (US Gulf Coast / Central / West Coast / international)")
    print(f"  LA refinery phased closure: {LA_REFINERY_CLOSURE_MBD:.1f} Mbpd (~17% of CA refining capacity)")
    print(f"  Industry-wide US closures within 18 months: ~{US_CAPACITY_EXIT_MBD} Mbpd (PES Philadelphia, LyondellBasell Houston,")
    print(f"    PSX LA, Valero Benicia) — pushing capacity below the 2023 EIA baseline of 18.06M bpd")
    print(f"  EIA forecasts US jet-fuel days-of-supply falling to ~21 days in 2026 — lowest since 1963")

    print(f"\n{sep}")
    print("  MIDSTREAM — THE GROWTH ENGINE (DCP INTEGRATION)")
    print(sep)
    print(f"  FY2025 EBITDA: ${MIDSTREAM_EBITDA_FY2025_B:.1f}B  →  2027 target: ${MIDSTREAM_EBITDA_TARGET_2027_B:.1f}B run-rate")
    print(f"  DCP synergies: ${DCP_SYNERGY_REALIZED_M}mm realized vs ${DCP_SYNERGY_TARGET_M}mm original target (+{(DCP_SYNERGY_REALIZED_M/DCP_SYNERGY_TARGET_M-1)*100:.0f}% beat)")
    print(f"  Growth projects: {MIDSTREAM_GROWTH_PROJECTS}")
    print(f"  CPChem (50/50 Chevron JV) Q1 2026 net income: ${CPCHEM_NET_INCOME_Q1_2026_M}mm")

    print(f"\n{sep}")
    print("  ELLIOTT MANAGEMENT ACTIVIST CAMPAIGN — THE BINARY CATALYST")
    print(sep)
    print(f"  Campaign start: {ELLIOTT_CAMPAIGN_START}  |  Stake: ~${ELLIOTT_STAKE_B:.1f}B (~{ELLIOTT_STAKE_PCT:.1f}%)")
    print(f"  'Streamline66' thesis: up to ${STREAMLINE66_UNLOCK_B}B unlock via Midstream/Chemicals separation")
    print(f"    (≈ ${STREAMLINE66_UNLOCK_B*1000/SHARES_OUT_M:.0f}/share on {SHARES_OUT_M:.1f}M shares — before execution discount)")
    print(f"  Proxy vote ({PROXY_VOTE_DATE}): {PROXY_VOTE_RESULT}")
    print(f"  Portfolio pruning: {RETAIL_DIVESTITURES}")
    print(f"  Status: {SETTLEMENT_STATUS}")

    print(f"\n{sep}")
    print("  ANALYST CONSENSUS")
    print(sep)
    print(f"  FY2026E: EPS ${FY2026_EPS_CONSENSUS:.2f}  |  Revenue ${FY2026_REVENUE_CONSENSUS_B:.1f}B")
    print(f"  Price targets: consensus ${CONSENSUS_PT:.2f} (range ${PT_LOW:.0f}-${PT_HIGH:.0f})  |  2027 avg trend ${PT_2027_AVG:.2f}")
    print(f"  {ANALYST_RATING_NOTE}")

    print(f"\n{sep}")
    print("  6 PROXY SIGNALS")
    print(sep)
    labels = {
        "refining_margin_supercycle_tightness": "Refining margin supercycle/tightness",
        "midstream_dcp_growth_engine":          "Midstream / DCP growth engine",
        "elliott_streamline66_catalyst":        "Elliott 'Streamline66' catalyst",
        "refining_margin_reversion_risk":       "Refining margin reversion risk",
        "capital_return_compounding_machine":   "Capital return compounding machine",
        "secular_ev_demand_transition_risk":    "Secular EV demand transition risk",
    }
    for k, (score, weight) in SIGNALS.items():
        bar = "█" * int(score * 5)
        print(f"  {labels[k]:<38}  {score:.1f}  wt={weight:.2f}  {bar}")
    print(f"  {'PROXY COMPOSITE':<38}  {PROXY_COMPOSITE:.2f}")

    print(f"\n{sep}")
    print("  SCA — STRUCTURAL COMPETITIVE ADVANTAGE")
    print(sep)
    sca_labels = {
        "integrated_value_chain":             "Integrated value chain (4 segments)",
        "gulf_coast_scale_advantage":         "Gulf Coast scale & export infra.",
        "midstream_infrastructure_moat":      "Midstream infrastructure (DCP) moat",
        "cpchem_petrochemical_scale":         "CPChem petrochemical JV scale",
        "capital_discipline_track_record":    "Capital discipline track record",
        "governance_activist_overhang":       "Governance / activist overhang",
        "secular_demand_transition_exposure": "Secular demand transition exposure",
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
    print(f"  FY2026E EPS consensus:   ${EPS_FY2026E:.2f}")
    print(f"  Conservative PE applied: {PE_CONSERVATIVE:.1f}× (modest expansion from ~13.2× current forward multiple)")
    print(f"  Target price 2yr:        ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.1f}× + ${2*ANNUAL_DIV:.2f} div = ${PRICE_2YR_CONSV:.2f}")
    print(f"  2-year return:           {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  Note: this assumes NO structural separation — pure compounding via dividend + buybacks + midstream ramp.")
    print(f"  If Elliott's 'Streamline66' thesis is even partially realized, upside is materially larger (see XBULL).")

    print(f"\n{sep}")
    print("  WHY THIS IS AN ◎ ACCUMULATE, NOT A ◉ BUY")
    print(sep)
    print("""
  Phillips 66 is a quality integrated energy compounder trading close to FAIR VALUE —
  not a deep-value dislocation like CHTR, and not a stressed turnaround like WBD.

  WHAT THE MARKET ALREADY PRICES IN (at $183, near the 52-week high):
  • Refining margins stay elevated near current levels (consensus PT $181 ≈ spot price)
  • Midstream growth toward $4.5B EBITDA proceeds roughly on schedule
  • Capital returns continue compounding at the current pace (dividend + buybacks)
  • Elliott situation stays in "détente" — no major structural action priced in

  WHAT COULD MAKE THIS MORE THAN FAIRLY VALUED:
  1. Refining supercycle proves more durable than skeptics expect — ~550K bpd of US/EU
     closures with no major new capacity is a multi-year structural setup, not a blip
  2. Midstream actually hits (or beats, like DCP synergies did) its $4.5B EBITDA target,
     and the market starts according it pure-play NGL/midstream multiples (8-10× EBITDA)
  3. Elliott's $40B "Streamline66" thesis gets even partially realized — the campaign
     achieved board seats and a portfolio-pruning wave already; a structural step on
     Midstream/Chemicals remains the single largest unresolved catalyst in the name
  4. CROIC of 13.2% (2× peer average) keeps compounding at a rate that, sustained,
     justifies a higher multiple than the ~13× forward PE the market currently assigns

  THE RISK:
  • A meaningful share of the recent refining beat may be a one-off (~$945mm gain);
    Goldman models $5-8/bbl of Brent downside if Iran/Russia sanctions ease
  • EV adoption is a real, structural, multi-decade headwind to gasoline demand
  • Elliott's détente could simply mean the campaign fizzles with NOTHING structural
    happening — leaving the $40B "gap" as a permanent, unrealized narrative
  • At a 13× forward multiple near the 52-week high, there is limited margin of safety
    if the refining cycle turns down faster than the bull case assumes

  POSITION SIZING GUIDANCE:
  • This is a "own it and let it compound" name, not a leveraged-turnaround swing trade
  • Add on weakness toward $150-160 (where Ratio B would approach BUY territory)
  • The Elliott catalyst is what separates this from a plain-vanilla refiner — it is
    the single biggest source of optionality-driven upside in the name
""")

    print(SEP)
    print(f"""
SUMMARY: PSX ◎ ACCUMULATE — Ratio B 0.93× (26.3% downside / 28.4% upside). INTEGRATED \
ENERGY NEAR HIGHS: trading at $183 (near 52-wk high $191, up from $111 low) as refining \
margins surged ($10.11/bbl Q1'26 vs $6.81 Q1'25, +48% YoY) on structural capacity tightness \
(~550K bpd of US refinery closures within 18 months). Midstream scaling toward $4.5B EBITDA \
target by 2027 (DCP synergies $500mm realized vs $300mm target, +67% beat); CPChem JV and \
Marketing & Specialties add diversification. FY2025: revenue $145.5B, adj. earnings $2.6B \
($6.44/sh, incl. $964mm LA-refinery D&A charge), GAAP EPS $10.90, CROIC 13.2% (2x peer avg). \
Balance sheet: $27.1B gross debt, Baa2/BBB- ratings. Capital returns: $5.08/yr dividend \
(+7% raise, ~2.8% yield), $269mm Q1 buybacks, $43B cumulative since 2012 spin-off, policy to \
return >50% of OCF. KEY CATALYST: Elliott Management ($2.5B stake, 'Streamline66' $40B \
unlock thesis) won 2 board seats in a split May-2025 proxy vote; March-2026 détente reached \
but core Midstream/Chemicals separation ask remains UNRESOLVED — a live, binary catalyst. \
Consensus PT $180.95 (range $138-213) ≈ current price = essentially fairly priced. \
Conservative 2yr: EPS $13.88 × 13.5x + $10.16 div = $197.54 → +7.9% (+3.9%/yr) on pure \
compounding (excludes Elliott-driven re-rating upside). QUALITY COMPOUNDER, NOT DEEP VALUE: \
add on weakness toward $150-160. Bear $135 · Base $190 · Bull $235 · XBull $290.
""")

    print(f"SIGNAL: {SIGNAL_TEXT} (quality compounder, fairly priced + activist optionality) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
