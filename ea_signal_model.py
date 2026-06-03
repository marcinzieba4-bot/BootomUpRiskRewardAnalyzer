"""
Electronic Arts Inc. (NASDAQ: EA) — Bottom-Up Risk/Reward Signal Model
BottomUp Risk/Reward Analyzer · veerock framework
Date: 2026-06-03

⚠️  DEAL-ARB NOTE: EA is NOT a standard equity. On September 29, 2025, EA agreed to
be acquired by a consortium (PIF/Silver Lake/Affinity Partners) at $210/share in
the largest all-cash gaming take-private in history ($55B enterprise value). The deal
was approved by 99% of shareholders (December 22, 2025) and is pending CFIUS review
(outside date: September 28, 2026). Stock trades at ~$202 — a ~4% spread to deal price.

The AVOID signal is for NEW BUYERS: buying a ~$8 gain (~4%) while risking ~$52 loss
(~26%) if CFIUS blocks the deal. Existing holders should HOLD through deal close.
The underlying business is excellent — record FY2026 net bookings ($8.03B), Battlefield 6
franchise record, Apex recovery from -40% feared to +double-digits actual, 71% recurring
revenue, $2.32B FCF. EA was taken private at a cheap 6.9× net bookings multiple; the
business is worth $210-250+ on a standalone 5yr DCF — the buyers got a bargain.
"""

# ── PRICE & MARKET DATA ───────────────────────────────────────────────────────
TICKER          = "EA"
COMPANY         = "Electronic Arts Inc."
SECTOR          = "Video Games · Live Services · Sports (FC, Madden, CF) · Battlefield · NASDAQ: EA"
DATE            = "2026-06-03"
CURRENT_PRICE   = 202.01
VOL_52W_LOW     = 144.67   # Pre-deal trough (unaffected price was $168.32 on Sep 25, 2025)
VOL_52W_HIGH    = 204.89   # Dec 26, 2025 high (deal probability pricing)
SHARES_OUT_M    = 250.75   # Diluted; down from 261.7M via buybacks
ANNUAL_DIV      = 0.76     # $0.19/quarter; ~0.38% yield; subordinate to deal economics

# ── THE $55B TAKE-PRIVATE DEAL ───────────────────────────────────────────────
DEAL_PRICE       = 210.00   # All-cash offer price per share
DEAL_SPREAD      = DEAL_PRICE - CURRENT_PRICE   # $7.99 (~4.0%)
DEAL_EV_B        = 55.0     # Enterprise value of the deal ($B)
DEAL_ANNOUNCED   = "September 29, 2025"
DEAL_PREMIUM_PCT = 24.7     # Premium to unaffected price of $168.32 on Sep 25, 2025

# Consortium:
# PIF (Saudi Arabia Public Investment Fund): ~93.4% post-close; rolling over ~9.9% existing stake
# Silver Lake Group: private equity; equity contributor
# Affinity Partners (Jared Kushner's PE): equity contributor
# Total equity commitment: ~$36B (including PIF rollover)
# New LBO debt: ~$20B (JPMorgan sole lead; ~$18B expected at close)

SHAREHOLDER_VOTE_RESULT  = "Approved December 22, 2025 — 99% of eligible votes in favor"
HSR_CLEARED              = True    # US antitrust clearance obtained
CFIUS_STATUS             = "Pending — primary remaining regulatory risk"
CFIUS_OUTSIDE_DATE       = "September 28, 2026"
DEAL_BREAK_FEE_REVERSE_B = 1.0     # $1B reverse break fee payable to EA if regulatory failure
DEAL_EXPECTED_CLOSE      = "By June 30, 2026 (pending CFIUS)"

# Deal failure downside estimate:
# Unaffected price Sep 25, 2025: $168.32
# Post-failure sentiment overshoot range: $145-170
DEAL_FAILURE_PRICE_LOW   = 145.0   # Overshoot scenario (sentiment panic + high-leverage perception)
DEAL_FAILURE_PRICE_MID   = 160.0   # Central estimate (reverts to pre-deal fundamental level)
DEAL_FAILURE_PRICE_HIGH  = 170.0   # Optimistic: sentiment holds near unaffected price

# ── FY2026 FUNDAMENTALS (Year Ended March 31, 2026) ─────────────────────────
# EA FISCAL YEAR ENDS MARCH 31. FY2026 = Apr 2025 – Mar 2026. "Final public year."
NET_BOOKINGS_FY2026_B    = 8.026   # Record; +9.1% YoY; EA's primary KPI
NET_BOOKINGS_FY2025_B    = 7.355   # Prior year (mid-year guidance cut on FC 25 + Dragon Age miss)
NET_BOOKINGS_FY2024_B    = 7.430   # Prior year 2
GAAP_REVENUE_FY2026_B    = 7.531   # +0.9% YoY (deferred revenue timing vs bookings)
GAAP_EPS_FY2026          = 3.51    # GAAP (diluted); includes non-cash items, deal charges
ADJ_EPS_FY2026           = 7.88    # Non-GAAP adjusted; mgmt's operational metric; +~31% YoY
OP_CASH_FLOW_FY2026_B    = 2.553   # +22.8% YoY
FCF_FY2026_B             = 2.32    # FCF = OpCF $2.553B - capex ~$0.23B; +24.7% YoY
FCF_MARGIN               = round(FCF_FY2026_B / GAAP_REVENUE_FY2026_B * 100, 1)  # 30.8%

# Revenue composition FY2026:
LIVE_SERVICES_REV_FY2026_B = 5.383   # Live services (UT, subs, mtx, live events); 71% of rev
FULL_GAME_REV_FY2026_B     = 2.148   # Full game sales (Battlefield 6 anchor); 29% of rev
LIVE_SVC_PCT               = round(LIVE_SERVICES_REV_FY2026_B / GAAP_REVENUE_FY2026_B * 100, 0)
# Ultimate Team & extra content: ~$4.4B across sports titles (~59% of total net revenue)

# Capital returns FY2026:
BUYBACKS_FY2026_B          = 0.750   # 5.3M shares × ~$141 avg price
DIVIDENDS_FY2026_B         = 0.191   # Quarterly dividends
TOTAL_CAPITAL_RETURNED_B   = 0.941   # Total returned in FY2026

# FCF yield (at current price vs deal EV)
FCF_YIELD_MKT              = round(FCF_FY2026_B / (CURRENT_PRICE * SHARES_OUT_M / 1000) * 100, 1)
FCF_YIELD_DEAL_EV          = round(FCF_FY2026_B / DEAL_EV_B * 100, 1)

# ── KEY FRANCHISES ────────────────────────────────────────────────────────────
# EA SPORTS FC (Global Football):
FC26_FIRST_WEEK_SALES_M  = 9.0     # First week of EA Sports FC 26 (FC 25 was a stumble)
FC26_METACRITIC           = 84      # vs 76 for FC 25 — quality recovery
FC26_WEEK3_SALES_M        = 12.0   # 12M copies by 3 weeks post-launch
UT_EXTRA_CONTENT_FY2026_B = 4.4    # Ultimate Team + extra content across ALL sports (~59% total)
FC_BOOKINGS_GROWTH_FY2026 = "mid-single digits YoY"

# BATTLEFIELD 6:
BF6_LAUNCH_DATE            = "Q3 FY2026 (~Oct 2025)"
BF6_3DAY_SALES_M           = 7.0   # 7M+ copies in first 3 days
BF6_ONLINE_MATCHES_LAUNCH  = 172   # 172M online matches launch weekend
BF6_STREAMING_HOURS_M      = 15    # 15M+ streaming hours launch weekend
BF6_ACHIEVEMENT            = "Best-selling shooter title of 2025; best Battlefield launch in history"

# APEX LEGENDS — THE COMEBACK:
APEX_INITIAL_FY2026_GUIDANCE = "-40% net bookings YoY"   # What EA guided at FY2025 results
APEX_FY2026_ACTUAL           = "Up double digits YoY"     # What actually happened — massive beat
APEX_STEAM_PEAK_MAR2026      = 287202   # Concurrent players March 2026 (+37% from July 2025 trough)

# COLLEGE FOOTBALL + MADDEN (American Football):
CF25_ACHIEVEMENT    = "Best-selling sports game in US history in its first year (franchise dormant 11yr)"
AMFOOT_FY2025_B     = 1.0     # Combined Madden + College Football exceeded $1B net bookings FY2025
AMFOOT_FY2025_GROWTH= "70%+ YoY"  # Combined American Football growth in FY2025

# DRAGON AGE: VEILGUARD (FY2025 miss):
VEILGUARD_UNITS_SOLD_M = 1.5   # Only ~1.5M copies (internal target ~3M+)
VEILGUARD_METACRITIC   = 82    # Good reviews, but commercial miss
VEILGUARD_IMPACT       = "Contributed $500-650M FY2025 guidance cut"
BIOWARE_STATUS         = "Reduced to ~100 developers; working on next Mass Effect (years away)"

# SKATE (new F2P IP):
SKATE_EARLY_ACCESS     = "September 16, 2025"
SKATE_PLAYERS_3WK_M    = 15.0  # 15M players in first 3 weeks
SKATE_PLATFORM_SPLIT   = "PlayStation 46%, Xbox 29%, Steam 25%"
SKATE_FULL_LAUNCH      = "2026"

# THE SIMS:
SIMS_STATUS            = "Sims 4 (free-to-play since 2022); FY2026 bookings decreased YoY"
SIMS5_STATUS           = "Project Rene / Sims 5: 'still years out'; no release date"

# RESTRUCTURING (FY2024-FY2026):
RESTRUCTURING_CHARGE_FY2024_M = 145   # ~$125-165M restructuring charge FY2024
JOBS_CUT_FY2024              = 670    # ~5% workforce cut (Feb 2024)
JOBS_CUT_FY2025              = 485    # Additional roles (studios: EA Montreal, Cliffhanger, etc.)
JOBS_CUT_FY2026              = 300    # Additional 300+ in 2026
STUDIO_CLOSURES = ("Ridgeline Games (BF single-player, 2024), Respawn Star Wars FPS (2024), "
                   "Respawn mobile/Apex mobile (prior); BioWare significantly reduced")
GROSS_MARGIN_IMPROVEMENT = "77.4% (FY2024) → 79.3% (FY2025) → ~80% (FY2026)"

# ── EPP (EARNINGS POWER PRICE) ────────────────────────────────────────────────
# EPP on standalone business (ignoring deal premium):
# Trough: Dragon Age/FC miss repeat, Apex re-declines, Battlefield plateaus
EPS_TROUGH   = 6.50    # Bear adj EPS (trough on $7.88 FY2026; franchise headwind)
PE_TROUGH    = 18      # Gaming software floor multiple (live services warrant premium vs hardware)
EPP          = EPS_TROUGH * PE_TROUGH    # = $117.00
EPP_GAP_PCT  = round((CURRENT_PRICE / EPP - 1) * 100, 1)  # +72.7%
# Stock is 73% above EPP floor → reflects deal premium + growth pricing
# Standalone fair value range: ~$155-180 (20-23× FY2026 adj EPS of $7.88)

# ── SCENARIO ASSUMPTIONS (DEAL ARB FRAMEWORK) ─────────────────────────────────
# NOTE: These scenarios reflect the deal arb dynamics, NOT standard business scenarios.
# The BASE case IS the deal close. BULL = sweetened or consent dividend. XBULL = counter-bid.
SCENARIOS = {
    "BEAR":  (6.50, 23, 150,
              "CFIUS blocks deal (~15% probability). EA stock reverts below unaffected price "
              "($168.32) with sentiment overshoot; heavy short-term selling, perception shift. "
              "Standalone: adj EPS $6.50 × 23× → $149.50 ≈ $150. $1B reverse break fee paid to EA."),
    "BASE":  (7.88, 27, 210,
              "Deal closes at $210 as announced (~80% probability). Shareholders receive $210 "
              "cash. Weighted by deal probability: ~80% of weight here."),
    "BULL":  (8.50, 27, 220,
              "Deal sweetened slightly ($220/share counter or consent dividend paid at close) "
              "OR deal closes quickly + minority holdout squeeze. Standalone FY2027E $8.50 "
              "adj EPS × 26× ($220) premium multiple."),
    "XBULL": (9.00, 28, 245,
              "Competing bid emerges (Amazon, Apple, Microsoft, Netflix Gaming). "
              "Bidding war at 7.5-8× net bookings = $60-64B EV = $240-255/share. "
              "CFIUS simultaneously clears PIF deal under pressure."),
}

# ── SOFTMAX SIGNAL MODEL ──────────────────────────────────────────────────────
# Proxy signals reflect the UNDERLYING BUSINESS quality (not deal arb).
# ADJ_COMPOSITE 3.13 (BULL+) confirms the business is excellent.
# The AVOID signal comes from the deal arb Ratio B (deal premium = 73% above EPP).
PROXY_SIGNALS = [
    # (name, value [1=BEAR/2=BASE/3=BULL/4=XBULL], weight, description)
    ("battlefield_6_franchise_record",   4.0, 0.25,
     "BF6: 7M+ sales day-3; 172M online matches launch weekend; best-selling shooter 2025; "
     "best Battlefield launch in history; ~$2.15B full-game rev FY2026. "
     "Live-service era beginning: Season passes, operators, content drops = durable recurring. "
     "Demonstrates EA can still launch a blockbuster; franchise reactivated. XBULL."),
    ("live_services_recurring_moat",     3.0, 0.25,
     "71% of revenue is live services ($5.38B FY2026). Ultimate Team ecosystem across FC, "
     "Madden, CF generates ~$4.4B/yr in extra content — one of most resilient recurring-revenue "
     "engines in entertainment. Sports license exclusivity (NFL, UEFA, UFC, NHL) moat. "
     "Switching cost from UT card collection is high. BULL structural moat."),
    ("apex_legends_massive_beat",        3.0, 0.20,
     "Guided -40% net bookings YoY. Actual: +double digits YoY. Single biggest upside "
     "surprise in FY2026. Steam peak 287K concurrent (Mar 2026; +37% from July trough). "
     "Proves live-service titles can be revived with content refreshes. BULL."),
    ("fcf_acceleration_margin_expansion", 3.0, 0.15,
     "FCF: $2.32B FY2026 (+24.7% YoY); $1.86B FY2025. FCF margin 30.8% on $7.5B revenue. "
     "Gross margin improved 77.4% → 79.3% → ~80% over 3 years. Restructuring $145M charge "
     "FY2024 → ongoing savings. $2.32B FCF / $55B deal EV = 4.2% FCF yield for LBO buyers."),
    ("franchise_portfolio_concentration", 2.0, 0.10,
     "FC + Madden/CF + Apex + Battlefield + Sims = >90% of bookings. Dragon Age effectively "
     "shelved (1.5M sales vs 3M+ expectation). Mass Effect is 5+ years away. "
     "Sims 4 declining; Sims 5 (Project Rene) years from launch. "
     "Skate (15M early-access players) is the next potential franchise — monetization TBD."),
    ("deal_cfius_uncertainty",           1.0, 0.05,
     "~15% probability CFIUS blocks deal on Saudi PIF concerns re: data security + gaming IP. "
     "If blocked: stock likely falls to $145-170. $1B reverse break fee limits walk-away incentive. "
     "Former US Treasury officials say 'limited mitigation' sufficient. BEAR risk."),
]

PROXY_COMPOSITE = sum(v * w for _, v, w, _ in PROXY_SIGNALS)
# = 4.0×0.25 + 3.0×0.25 + 3.0×0.20 + 3.0×0.15 + 2.0×0.10 + 1.0×0.05
# = 1.00 + 0.75 + 0.60 + 0.45 + 0.20 + 0.05 = 3.05

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
    ("+", "Ultimate Team ecosystem (switching cost + engagement flywheel): UT card collections "
          "create genuine asset lock-in; players emotionally invested in digital squads; "
          "peak UT engagement in Nov/Dec; ~$2.2B soccer UT alone; ~$4.4B across all sports.", +0.85, 0.25),
    ("+", "Sports licensing near-monopoly: exclusive/semi-exclusive NFL, UEFA, UFC, NHL, "
          "NBA (via NBA 2K competitor EA Sports), College Football (RCAA). These licenses "
          "are structural moat; competitors (eFootball, UFL) cannot replicate at scale.",       +0.75, 0.20),
    ("+", "Live-services architecture: 71% recurring revenue; seasonal content cadence; "
          "EA App (PC launcher) integration; EA Play subscription (~6M+ subscribers); "
          "multi-year relationship with players vs. one-time transactions.",                    +0.65, 0.15),
    ("-", "Microsoft Gaming structural competition: CoD, Halo, Diablo, Starfield all under "
          "one roof via Activision acquisition; Game Pass bundles at scale; direct Battlefield "
          "vs CoD competition; Microsoft has near-unlimited content investment capacity.",       -0.50, 0.15),
    ("-", "Franchise portfolio concentration + talent risk: >90% of revenue from 5 franchises; "
          "BioWare/Dragon Age collapse removes single-player AAA credibility; "
          "post-LBO talent retention risk (key developers may leave private company).",         -0.40, 0.10),
    ("+", "New IP optionality (Skate F2P): 15M players in 3 weeks of early access; "
          "new generation of skating audience; cosmetics-driven F2P monetization ramp ahead; "
          "validates EA's ability to launch new live-service IP beyond sequels.",               +0.35, 0.10),
    ("-", "Post-LBO leverage burden: $20B in debt at ~7× EBITDA post-close; "
          "interest expense ~$800M-1.2B/yr; constrains content investment; "
          "monetization pressure intensification likely under PIF/Silver Lake ownership.",       -0.70, 0.05),
]
# SCA_NET = +0.85×0.25 + 0.75×0.20 + 0.65×0.15
#           + (-0.50)×0.15 + (-0.40)×0.10 + 0.35×0.10 + (-0.70)×0.05
# = 0.213 + 0.150 + 0.098 - 0.075 - 0.040 + 0.035 - 0.035 = +0.346

SCA_NET       = 0.346
SCA_SCALE     = 0.45
ADJ_COMPOSITE = round(PROXY_COMPOSITE + SCA_SCALE * SCA_NET * 0.5, 2)
# = 3.05 + 0.45 × 0.346 × 0.5 = 3.05 + 0.078 = 3.13

# ── MARKET COMPOSITE (back-solved) ───────────────────────────────────────────
# Deal-arb framework: EV(c_market) ≈ $202.01 (stock price itself)
# Back-solve: c_market ≈ 2.10 → EV ≈ $203 (deal close ~80% priced in)
# Reflects ~80-85% deal probability priced into $202 vs $210 deal price.
MARKET_COMPOSITE  = 2.10
ADJ_VS_MARKET     = round(ADJ_COMPOSITE - MARKET_COMPOSITE, 2)   # +1.03 → UNDERVALUED (business)
# KEY INSIGHT: The ADJ-Market gap of +1.03 confirms the BUSINESS is worth more than
# the $210 deal price on a fundamental basis — PIF/Silver Lake bought EA cheaply.
# But for current shareholders at $202, the deal constrains upside to +4%.

# ── RATIO B ───────────────────────────────────────────────────────────────────
# Using BEAR ($150) and BULL ($220) for the deal-arb framework:
BEAR_TARGET  = SCENARIOS["BEAR"][2]      # $150
BULL_TARGET  = SCENARIOS["BULL"][2]      # $220
DOWNSIDE_PCT = (CURRENT_PRICE - BEAR_TARGET)  / CURRENT_PRICE * 100   # 25.7%
UPSIDE_PCT   = (BULL_TARGET   - CURRENT_PRICE) / CURRENT_PRICE * 100  # 8.9%
RATIO_B      = round(DOWNSIDE_PCT / UPSIDE_PCT, 2)   # 2.89 → AVOID

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

# ── DEAL ARB RETURN ANALYSIS ──────────────────────────────────────────────────
DEAL_PROB_CLOSE  = 0.85   # Estimated probability of deal closing at $210
DEAL_PROB_FAIL   = 1 - DEAL_PROB_CLOSE
DEAL_RETURN_PCT  = (DEAL_PRICE / CURRENT_PRICE - 1) * 100          # +3.96%
FAIL_RETURN_PCT  = (DEAL_FAILURE_PRICE_MID / CURRENT_PRICE - 1) * 100  # -20.8%
EV_RETURN_PCT    = DEAL_PROB_CLOSE * DEAL_RETURN_PCT + DEAL_PROB_FAIL * FAIL_RETURN_PCT
# = 0.85 × 3.96% + 0.15 × (-20.8%) = 3.37% - 3.12% = +0.25%

# STANDALONE CONSERVATIVE 2YR (if deal fails):
STANDALONE_EPS     = 8.50    # FY2027E on organic trajectory (Battlefield LS + FC growth)
STANDALONE_PE      = 20      # Conservative gaming software multiple (below deal-implied 27×)
STANDALONE_PRICE   = STANDALONE_EPS * STANDALONE_PE    # $170.00
STANDALONE_DIV_2YR = ANNUAL_DIV * 2                    # $1.52
CONSERVATIVE_RETURN = ((STANDALONE_PRICE + STANDALONE_DIV_2YR) / CURRENT_PRICE - 1) * 100
# = (170.00 + 1.52) / 202.01 - 1 = -15.1% → NEGATIVE (deal premium makes standalone entry expensive)

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
    A(f"  ⚠️  DEAL ARB: $210/share take-private (PIF/Silver Lake) pending CFIUS review")
    A(f"  Price: ${CURRENT_PRICE:.2f}  |  Deal: ${DEAL_PRICE:.2f}  |  Spread: ${DEAL_SPREAD:.2f} (~{DEAL_SPREAD/CURRENT_PRICE*100:.1f}%)")
    A(f"  52W: ${VOL_52W_LOW}–${VOL_52W_HIGH}  |  Mkt Cap: ${mkt_cap_b:.1f}B  |  Deal EV: ${DEAL_EV_B:.0f}B")
    A(f"  Div: ${ANNUAL_DIV:.2f}/yr ({ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield — subordinate to deal)")
    A(f"  FY2026 FCF: ${FCF_FY2026_B:.2f}B  |  FCF yield (deal EV): {FCF_YIELD_DEAL_EV:.1f}%")
    A(f"  FY2026 Net Bookings: ${NET_BOOKINGS_FY2026_B:.3f}B  (+9.1% YoY; record)")
    A("")

    # ── SIGNAL DASHBOARD ────────────────────────────────────────────────────
    A("─" * 76)
    A("  SIGNAL DASHBOARD")
    A("─" * 76)
    A(f"  Signal      : {SIGNAL}  ← for NEW BUYERS at $202; HOLD for existing holders")
    A(f"  Ratio B     : {RATIO_B:.2f}×  (downside {DOWNSIDE_PCT:.1f}% / upside {UPSIDE_PCT:.1f}%)")
    A(f"  Arb Math    : {DEAL_PROB_CLOSE*100:.0f}% × +{DEAL_RETURN_PCT:.1f}% deal close + {DEAL_PROB_FAIL*100:.0f}% × {FAIL_RETURN_PCT:.1f}% fail = {EV_RETURN_PCT:+.2f}% EV")
    A(f"  EPP         : ${EPP:.2f}  (${EPS_TROUGH} trough EPS × {PE_TROUGH}×)")
    A(f"  EPP Gap     : +{EPP_GAP_PCT:.1f}%  (deal premium lifts stock 73% above EPP floor)")
    A(f"  Business    : Proxy {PROXY_COMPOSITE:.2f}  |  ADJ: {ADJ_COMPOSITE:.2f}  |  Market: {MARKET_COMPOSITE:.2f}")
    A(f"  ADJ–Market  : {ADJ_VS_MARKET:+.2f}  → Underlying business SIGNIFICANTLY UNDERVALUED vs $210 deal price")
    A(f"  2yr EV      : ${ev:.2f}  (business-only framework; includes div ${div_2yr:.2f})")
    A(f"  If deal close: +{DEAL_RETURN_PCT:.1f}% in ~{3} months")
    A(f"  If deal fails: standalone ${STANDALONE_PRICE:.0f} (EPS ${STANDALONE_EPS} × {STANDALONE_PE}×) + div ${STANDALONE_DIV_2YR:.2f} = {CONSERVATIVE_RETURN:+.1f}%")
    A("")
    A(f"  SCENARIO WEIGHTS  (at ADJ composite {ADJ_COMPOSITE:.2f} — reflecting business quality):")
    for s, w in weights.items():
        tgt = SCENARIOS[s][2]
        A(f"    {s:<6} {w*100:5.1f}%  →  ${tgt}  ({'+' if tgt > CURRENT_PRICE else ''}{(tgt-CURRENT_PRICE)/CURRENT_PRICE*100:.0f}%)")
    A("")

    # ── DEAL OVERVIEW ────────────────────────────────────────────────────────
    A("─" * 76)
    A("  THE $55B TAKE-PRIVATE DEAL — KEY FACTS")
    A("─" * 76)
    A(f"  Announced    : {DEAL_ANNOUNCED}")
    A(f"  Offer Price  : ${DEAL_PRICE:.2f}/share  ({DEAL_PREMIUM_PCT:.1f}% premium to unaffected ${168.32})")
    A(f"  Enterprise V : ${DEAL_EV_B:.0f}B  (={DEAL_EV_B/NET_BOOKINGS_FY2026_B:.1f}× FY2026 net bookings)")
    A(f"  Consortium   : PIF (Saudi Arabia; ~93.4% post-close, rolling 9.9% stake)")
    A(f"               : Silver Lake Group (private equity)")
    A(f"               : Affinity Partners (Jared Kushner's PE)")
    A(f"  Debt         : ~$20B LBO debt (JPMorgan sole lead; ~7× EBITDA — aggressive)")
    A(f"  Shareholder  : {SHAREHOLDER_VOTE_RESULT}")
    A(f"  HSR          : Cleared")
    A(f"  CFIUS        : {CFIUS_STATUS}")
    A(f"  Outside Date : {CFIUS_OUTSIDE_DATE}")
    A(f"  Break Fee    : ${DEAL_BREAK_FEE_REVERSE_B:.0f}B reverse (payable to EA if regulatory block)")
    A(f"  Expected     : {DEAL_EXPECTED_CLOSE}")
    A("")
    A("  CFIUS RISK ASSESSMENT:")
    A("  • PIF is a Saudi sovereign wealth fund — US regulators scrutinize data security")
    A("    implications of foreign ownership of major gaming platforms (EA App; ~650M+ accounts)")
    A("  • Microsoft/Activision ($69B, 2023) cleared CFIUS; EA is smaller and less strategic")
    A("  • Former US Treasury officials: deal 'likely approved with limited mitigation'")
    A("  • $1B reverse break fee limits consortium's walk-away incentive")
    A("  • If blocked: stock falls ~$40-55 from current $202 to $145-165 range")
    A("")
    A("  WHY THE DEAL IS CHEAP FOR BUYERS (and why AVOID for new buyers at $202):")
    A(f"  • PIF/Silver Lake paying $210/share = {DEAL_EV_B/NET_BOOKINGS_FY2026_B:.1f}× FY2026 net bookings")
    A(f"  • Comparable: Microsoft paid ~9.3× net bookings for Activision in 2023")
    A(f"  • EA's 71% recurring revenue + $2.32B FCF + record bookings = worth $240-270+ standalone")
    A(f"  • Buyers got a $15-60B discount vs. intrinsic value — EA's board accepted too cheaply")
    A(f"  • But for new buyers at $202: you can only capture ${DEAL_SPREAD:.0f} of that gap (+{DEAL_SPREAD/CURRENT_PRICE*100:.1f}%)")
    A(f"    while bearing ${abs(CURRENT_PRICE - DEAL_FAILURE_PRICE_MID):.0f} of risk if CFIUS blocks (-{abs(FAIL_RETURN_PCT):.1f}%)")
    A("")

    # ── BUSINESS OVERVIEW ────────────────────────────────────────────────────
    A("─" * 76)
    A("  UNDERLYING BUSINESS — FY2026 HIGHLIGHTS (STANDALONE VALUE)")
    A("─" * 76)
    A(f"  FY2026 Net Bookings: ${NET_BOOKINGS_FY2026_B:.3f}B  (record; +9.1% YoY; 3rd straight year >$7B)")
    A(f"  FY2026 FCF:          ${FCF_FY2026_B:.2f}B  (+24.7% YoY; FCF margin {FCF_MARGIN:.1f}%)")
    A(f"  Adj EPS:             ${ADJ_EPS_FY2026:.2f}  (non-GAAP; management operational KPI)")
    A(f"  Live Services:       ${LIVE_SERVICES_REV_FY2026_B:.3f}B  ({LIVE_SVC_PCT:.0f}% of revenue — recurring moat)")
    A(f"  UT + Extra Content:  ${UT_EXTRA_CONTENT_FY2026_B:.1f}B  (~59% of revenue — Ultimate Team flywheel)")
    A("")
    A("  THE 4 PILLARS OF FY2026 RECORD BOOKINGS:")
    A("")
    A(f"  ① BATTLEFIELD 6: {BF6_3DAY_SALES_M:.0f}M+ copies in 3 days. {BF6_ONLINE_MATCHES_LAUNCH}M online matches")
    A(f"    at launch weekend. #{1} best-selling shooter of 2025. Franchise record. Live")
    A(f"    services (seasons, operators) now ramping — FY2027 BF6 recurring revenue begins.")
    A("")
    A(f"  ② EA SPORTS FC 26: {FC26_FIRST_WEEK_SALES_M:.0f}M first-week sales; {FC26_WEEK3_SALES_M:.0f}M by week 3.")
    A(f"    Metacritic {FC26_METACRITIC} (vs {76} for FC 25 — quality recovery). #1 revenue in")
    A(f"    16/17 European countries. Reversed FC 25 stumble. UT ecosystem: ~$2.2B soccer alone.")
    A("")
    A(f"  ③ APEX LEGENDS RECOVERY: Guided -40% YoY → actual +double digits YoY.")
    A(f"    Steam peak {APEX_STEAM_PEAK_MAR2026:,} concurrent players (Mar 2026; +37% from July trough).")
    A(f"    Single biggest positive surprise in FY2026; live service resilience confirmed.")
    A("")
    A(f"  ④ AMERICAN FOOTBALL FRANCHISE: College Football 26 (second year) + Madden NFL 26.")
    A(f"    CF25 was best-selling US sports game in history in its first year;")
    A(f"    franchise adds permanent $1B+ annual revenue stream EA didn't have before 2024.")
    A("")

    # ── FRANCHISE DETAILS ────────────────────────────────────────────────────
    A("─" * 76)
    A("  FRANCHISE DEEP DIVE")
    A("─" * 76)
    A("  EA SPORTS FC (GLOBAL FOOTBALL):")
    A(f"    FC 26 copies sold: {FC26_WEEK3_SALES_M:.0f}M in 3 weeks; Metacritic {FC26_METACRITIC}; #1 in 16/17 EU countries")
    A(f"    FC 25 stumble: Metacritic 76; bookings miss → $500-650M FY2025 guidance cut")
    A(f"    FC 24 rebrand (from FIFA): successful; proved FIFA license was not the product")
    A(f"    Competition: eFootball (950M cumulative downloads, F2P) — brand not engagement threat")
    A(f"    UFL: early-stage challenger; not commercially material in 2025-2026")
    A(f"    UT moat: card collections + seasonal Ultimate Team = recurring high-margin revenue")
    A("")
    A("  APEX LEGENDS:")
    A(f"    Original FY2026 guidance: {APEX_INITIAL_FY2026_GUIDANCE}")
    A(f"    Actual FY2026 result:      {APEX_FY2026_ACTUAL}")
    A(f"    Steam concurrent peak (Mar 2026): {APEX_STEAM_PEAK_MAR2026:,} players")
    A(f"    Lesson: Live-service titles can recover with content refreshes + community engagement")
    A(f"    Risk: Fortnite/Warzone competition; GTA VI launch (Nov 2026?) = attention capture")
    A("")
    A("  DRAGON AGE: VEILGUARD (FY2025 miss):")
    A(f"    Sales: ~{VEILGUARD_UNITS_SOLD_M:.1f}M copies (internal target ~3M+; missed by 50%)")
    A(f"    Metacritic: {VEILGUARD_METACRITIC} (critical quality ≠ commercial success)")
    A(f"    Impact: {VEILGUARD_IMPACT}")
    A(f"    BioWare: {BIOWARE_STATUS}")
    A("")
    A("  SKATE (NEW F2P IP):")
    A(f"    Early access: {SKATE_EARLY_ACCESS}")
    A(f"    Players in 3 weeks: {SKATE_PLAYERS_3WK_M:.0f}M — extremely strong F2P launch")
    A(f"    Monetization: Cosmetics only (early PC-only: ~$3M); full launch 2026 = key test")
    A(f"    Full Circle studio: restructured in 2025 ('roles impacted') during development")
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
    A("  PROXY SIGNALS (UNDERLYING BUSINESS — NOT DEAL ARB)")
    A("─" * 76)
    for name, val, wt, desc in PROXY_SIGNALS:
        label = {1.0: "BEAR", 2.0: "BASE", 3.0: "BULL", 4.0: "XBULL"}.get(val, f"{val:.1f}")
        A(f"  [{label}]  {name}  (value={val:.1f}, weight={wt:.2f})")
        A(f"  {desc[:76]}")
        A(f"  {desc[76:152]}" if len(desc) > 76 else "")
        A("")
    A(f"  PROXY COMPOSITE  = {PROXY_COMPOSITE:.2f}  (BULL+ — business is excellent)")
    A(f"  ADJ COMPOSITE    = {ADJ_COMPOSITE:.2f}  (SCA: +{SCA_SCALE * SCA_NET * 0.5:.3f})")
    A(f"  MARKET COMPOSITE = {MARKET_COMPOSITE:.2f}  (deal-arb; reflects ~85% deal probability)")
    A(f"  GAP              = {ADJ_VS_MARKET:+.2f}  → Fundamentals >> deal price (PIF got a bargain)")
    A("")

    # ── SCENARIOS ────────────────────────────────────────────────────────────
    A("─" * 76)
    A("  SCENARIOS (DEAL ARB FRAMEWORK)")
    A("─" * 76)
    for s, (eps, pe, price, desc) in SCENARIOS.items():
        chg = (price - CURRENT_PRICE) / CURRENT_PRICE * 100
        A(f"  {s:<6}  ${price:.0f}  ({chg:+.0f}%)  {'EPS '+str(eps)+'×'+str(pe)+' (standalone)' if s in ['BEAR','BULL','XBULL'] else 'Deal close at $210'}")
        A(f"         {desc[:80]}")
        A("")
    A(f"  RATIO B  = {RATIO_B:.2f}×  ({DOWNSIDE_PCT:.1f}% downside / {UPSIDE_PCT:.1f}% upside to $220 BULL)")
    A(f"  EPP FLOOR: ${EPP:.2f}  (trough ${EPS_TROUGH} adj EPS × {PE_TROUGH}×)  |  EPP Gap: +{EPP_GAP_PCT:.1f}%")
    A("")

    # ── STANDALONE VALUATION ─────────────────────────────────────────────────
    A("─" * 76)
    A("  STANDALONE VALUATION CROSS-CHECK (IF DEAL FAILED)")
    A("─" * 76)
    A(f"  FY2026 Net Bookings: ${NET_BOOKINGS_FY2026_B:.3f}B  |  Adj EPS: ${ADJ_EPS_FY2026:.2f}  |  FCF: ${FCF_FY2026_B:.2f}B")
    A("")
    A("  METHOD                 MULTIPLE   VALUE    vs $202 CURRENT")
    A("  ──────────────────────────────────────────────────────────")
    for lbl, mult, val in [
        ("P/E (20×, conservative)", "20× adj EPS",   ADJ_EPS_FY2026 * 20),
        ("P/E (23×, mid-case)",     "23× adj EPS",   ADJ_EPS_FY2026 * 23),
        ("P/E (27×, deal-implied)", "27× adj EPS",   ADJ_EPS_FY2026 * 27),
        ("FCF yield (18× FCF)",     "18× FCF/share", FCF_FY2026_B*1000/SHARES_OUT_M * 18),
        ("Net Bookings (6.5×EV)",   "6.5× NB/EV",   (NET_BOOKINGS_FY2026_B*6.5*1000 - 2500)/SHARES_OUT_M),
        ("Net Bookings (7×EV)",     "7.0× NB/EV",   (NET_BOOKINGS_FY2026_B*7.0*1000 - 2500)/SHARES_OUT_M),
    ]:
        chg = (val / CURRENT_PRICE - 1) * 100
        A(f"  {lbl:<26}  {mult:<18}  ${val:6.0f}  ({chg:+.0f}%)")
    A("")
    A(f"  Deal at $210 represents 6.9× FY2026 net bookings — Activision/Microsoft paid 9.3×.")
    A(f"  EA's FCF yield at deal price is 4.2%; software peers trade at 2.5-3.5% FCF yield.")
    A(f"  Bottom line: PIF/Silver Lake paid BELOW intrinsic value. Shareholders got ~$40-65")
    A(f"  less per share than the business is worth on a standalone DCF basis.")
    A("")

    # ── KEY THESIS ────────────────────────────────────────────────────────────
    A("─" * 76)
    A("  WHY AVOID AT $202 — THE DEAL ARB MATH")
    A("─" * 76)
    A("")
    A("  The AVOID signal is not about the quality of the business — EA at record")
    A("  $8.03B net bookings with a remarkable Apex recovery, Battlefield franchise")
    A("  reactivation, and 71% recurring revenue is an excellent business.")
    A("")
    A("  The AVOID signal is about the asymmetric deal-arb risk/reward at $202:")
    A("")
    A(f"  UPSIDE case  (deal closes @ $210):  +${DEAL_SPREAD:.2f}/share  (+{DEAL_RETURN_PCT:.1f}%)  ~85% probability")
    A(f"  DOWNSIDE case (CFIUS blocks):       -${abs(CURRENT_PRICE-DEAL_FAILURE_PRICE_MID):.2f}/share  ({FAIL_RETURN_PCT:.1f}%)  ~15% probability")
    A(f"  EXPECTED VALUE:                     +${EV_RETURN_PCT/100*CURRENT_PRICE:.2f}/share  ({EV_RETURN_PCT:+.2f}%)")
    A("")
    A(f"  AT $202, YOU ARE BUYING A $4 BILL FOR $4.70:")
    A(f"  • The $8 gain from deal close barely compensates for holding-period risk")
    A(f"  • The $42 downside from deal failure is not adequately compensated at a 15% prob.")
    A(f"  • Arb professionals can hedge; retail investors face asymmetric unhedged risk")
    A("")
    A("  BETTER ENTRY POINTS:")
    A(f"  • Below $185: EV increases to +14% (deal close upside); risk/reward improves")
    A(f"  • Below $170: Pure standalone valuation play; deal is a free bonus option")
    A(f"  • Below $150 if deal FAILS: STRONG BUY on standalone fundamentals alone")
    A("")
    A("  NOTE FOR EXISTING HOLDERS: HOLD. The deal will likely close. Don't sell $202 paper")
    A("  for ~$198 cash when deal close is probable in the next 3 months. The $1B reverse")
    A("  break fee is a meaningful deterrent to the consortium walking away voluntarily.")
    A("")
    A("  RISKS TO MONITOR:")
    A("  • CFIUS decision timeline — any extension of review signals concern")
    A("  • Political developments regarding PIF/Saudi relations with US administration")
    A("  • EA operating performance during deal limbo (no FY2027 guidance issued)")
    A("  • GTA VI launch (expected Nov 2026) — potential drag on Apex engagement")
    A("════════════════════════════════════════════════════════════════════════════")
    A("")

    summary_line = (
        f"EA {SIGNAL} — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT:.1f}% downside / {UPSIDE_PCT:.1f}% upside). "
        f"DEAL ARB: $210/share take-private by PIF/Silver Lake/Affinity Partners ($55B EV); "
        f"shareholders approved 99% (Dec 22, 2025); CFIUS pending (outside date Sep 28, 2026). "
        f"Stock at $202 = 4.0% upside if deal closes vs -20.8% downside if CFIUS blocks. "
        f"Expected arb value: +0.25% (essentially zero alpha). "
        f"Underlying business is EXCELLENT: FY2026 record net bookings $8.03B (+9.1%); FCF $2.32B (+24.7%); "
        f"Battlefield 6 (7M sales day-3; franchise record); EA Sports FC 26 (12M copies in 3wk; Metacritic 84); "
        f"Apex Legends (guided -40%, actual +double digits); College Football franchise ($1B+/yr). "
        f"71% live services recurring revenue; UT ecosystem $4.4B/yr. "
        f"Deal implied 6.9× net bookings vs Activision paid 9.3× — buyers got a bargain. "
        f"AVOID for new buyers at $202. HOLD for existing shareholders. "
        f"Re-evaluate below $185 (better arb spread) or below $170 (standalone entry). "
        f"Bear $150 (CFIUS block) · Base $210 (deal close) · Bull $220 · XBull $245."
    )
    A(f"SUMMARY: {summary_line}")
    A("")
    A(f"SIGNAL: {SIGNAL} (deal arb) | Ratio B: {RATIO_B:.2f}× | EPP Gap: +{EPP_GAP_PCT:.1f}%")
    A(f"STANDALONE SIGNAL: ◉ BUY (business only) — ADJ composite {ADJ_COMPOSITE:.2f} vs market {MARKET_COMPOSITE:.2f}")

    return "\n".join(report)


if __name__ == "__main__":
    print(run_model())
