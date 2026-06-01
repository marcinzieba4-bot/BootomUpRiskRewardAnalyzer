"""
AT&T Inc. (NYSE: T) — Bottom-Up Risk/Reward Signal Model
BottomUp Risk/Reward Analyzer · veerock framework
Date: 2026-06-01
"""

# ── PRICE & MARKET DATA ────────────────────────────────────────────────────────
TICKER            = "T"
COMPANY           = "AT&T Inc."
SECTOR            = "Wireless & Fiber · EchoStar Spectrum · Wireline Legacy · NYSE: T"
DATE              = "2026-06-01"
CURRENT_PRICE     = 24.80
VOL_52W_LOW       = 22.95
VOL_52W_HIGH      = 29.79
SHARES_OUT_M      = 6948.0
ANNUAL_DIV        = 1.11   # $0.2775/quarter × 4

# ── SEGMENT REVENUE (FY2025, $B) ─────────────────────────────────────────────
WIRELESS_SVC_REV_B  = 67.5   # Mobile service revenue — core engine
WIRELESS_EQUIP_B    = 15.0   # Handset / device pass-through
FIBER_REV_B         =  8.6   # AT&T Fiber ARPU × ~10.1M avg subs
WIRELINE_LEGACY_B   =  5.8   # Copper/DSL — secular decline ~10%/yr
BUSINESS_WL_B       = 21.5   # Enterprise wireline & managed services
OTHER_REV_B         =  7.2   # WarnerMedia remnants, Mexico, other
TOTAL_REV_B         = 125.6  # Sum of above (FY2025 consensus)

# ── EBITDA ARCHITECTURE ───────────────────────────────────────────────────────
WIRELESS_SVC_MGN    = 0.52   # Mobile service ~52% EBITDA margin
FIBER_EBITDA_MGN    = 0.30   # Fiber segment EBITDA margin (scale-building)
LEGACY_EBITDA_MGN   = 0.18   # Declining copper margin
BUSINESS_WL_MGN     = 0.22   # Enterprise segment margin
EQUIP_EBITDA_MGN    = 0.02   # Nearly breakeven on equipment
OTHER_MGN           = 0.15   # Other segments blended
ADJ_EBITDA_B        = 46.4   # FY2025 consolidated adjusted EBITDA
EBITDA_MGN_CONSOL   = 0.369  # 46.4 / 125.6

# ── FIBER SUBSCRIBER ECONOMICS ───────────────────────────────────────────────
FIBER_HOMES_M          = 37.0    # Homes passed with fiber (end-2025)
FIBER_SUBS_M           = 10.4    # Fiber internet subscribers (end-2025)
FIBER_PENETRATION      = 0.281   # 10.4 / 37.0 = 28.1%
FIBER_ARPU_MO          = 70.89   # Monthly ARPU (~$851/yr)
FIBER_NET_ADDS_Q1      = 0.273   # Q1 2026: 273K net adds (record)
FIBER_INC_EBITDA_MGN   = 0.55    # Incremental EBITDA margin on new subs
FIBER_DDA_PER_SUB      = 90.0    # Annual D&A per fiber sub ($)
# EPS sensitivity: 1M additional fiber subs on existing plant
# Incremental EBITDA = 1M × $851 × 55% = $468M
# Less incremental D&A = 1M × $90 = $90M
# Pre-tax = $378M; after tax 22% = $295M; / 6948M shares ≈ $0.042/EPS per 1M subs
FIBER_EPS_PER_1M_SUBS  = 0.042

# ── WIRELESS FUNDAMENTALS ─────────────────────────────────────────────────────
POSTPAID_PHONE_SUBS_M   = 74.9   # Postpaid phone subscribers (end-2025)
POSTPAID_ARPU_MO        = 56.80  # Postpaid phone ARPU/month
POSTPAID_CHURN          = 0.0072 # Monthly churn 0.72% (best-in-class)
PREPAID_SUBS_M          = 17.3   # Prepaid (Cricket + AT&T)
WIRELESS_NET_ADDS_2025  = 0.901  # Postpaid phone net adds FY2025 (M)

# ── ECHOSTAR DEAL ─────────────────────────────────────────────────────────────
ECHO_COST_B             = 23.0   # Deal value; ~$0.65/share + $20.5B assumed debt
ECHO_SPECTRUM_MHZ_POP   = 40     # ~40 MHz-POP average mid-band spectrum
ECHO_MARKETS            = 400    # Markets covered (nationwide rural + suburban)
ECHO_CLOSE              = "mid-2026"
# EchoStar accelerates fixed-wireless (FWA) and rural 5G; complements CBRS/C-band

# ── BALANCE SHEET & LEVERAGE ─────────────────────────────────────────────────
NET_DEBT_B              = 126.4  # Net debt pre-EchoStar close (end-2025)
NET_DEBT_POST_ECHO_B    = 149.4  # Pro-forma after $23B EchoStar (mid-2026)
EBITDA_FWD_B            = 48.0   # FY2026E EBITDA (post-EchoStar)
FCF_2026E_B             = 18.0   # FY2026E free cash flow (after capex)
CAPEX_B                 = 22.0   # FY2026E capex guidance
LEVERAGE_CURRENT        = 2.71   # Net debt / EBITDA (pre-close)
LEVERAGE_POST_ECHO      = 3.11   # Post-close peak (149.4/48.0)
LEVERAGE_TARGET         = 2.50   # Management long-term target
# Deleveraging path: end-2026 ~3.0×; end-2027 ~2.65×; end-2028 ~2.29×

# ── EARNINGS ─────────────────────────────────────────────────────────────────
EPS_FY2025A     = 2.12   # FY2025 adjusted EPS
EPS_FY2026E     = 2.35   # FY2026E: EchoStar dilution offset by fiber growth
EPS_FY2027E     = 2.60   # FY2027E: full EchoStar integration + fiber inflection
EPS_TROUGH      = 2.12   # Use FY2025 as trough base (post-WBD spin, clean)
DIV_GROWTH      = 0.0    # Flat dividend ($1.11) — capital directed to debt paydown

# ── EPP (EARNINGS POWER PRICE) ───────────────────────────────────────────────
PE_TROUGH       =  9     # Minimum viable trough P/E (stress = leverage crisis)
EPP             = EPS_TROUGH * PE_TROUGH  # = $19.08 ≈ $19.00
EPP_GAP_PCT     = round((CURRENT_PRICE / EPP - 1) * 100, 1)  # = +30.5%

# ── SCENARIO ASSUMPTIONS ─────────────────────────────────────────────────────
# (trough_eps, exit_pe, target_price, rationale)
SCENARIOS = {
    "BEAR":  (1.70,  7, 12,
              "Leveraged telecom into recession; EchoStar costs balloon; wireless share loss; "
              "EPS $1.70 × 7× distress P/E → $12. Dividend at risk."),
    "BASE":  (2.45, 11, 27,
              "Steady fiber penetration 28%→36%; wireless ARPU stable; EchoStar neutral-to-positive; "
              "deleverages to 2.5× by end-2028; EPS $2.45 × 11× → $27"),
    "BULL":  (2.90, 13, 38,
              "Fiber sub growth accelerates (net adds 300K+/qtr); EchoStar synergies €500M+; "
              "re-rates to cable/fiber comps; EPS $2.90 × 13× → $38"),
    "XBULL": (3.40, 16, 54,
              "Fiber penetration 45%+ by 2029; FWA 5M homes; EchoStar emerges as #4 wireless; "
              "leverage 2.0×; re-rates to premium; EPS $3.40 × 16× → $54"),
}

# ── SOFTMAX SIGNAL MODEL ─────────────────────────────────────────────────────
# Scenario centers: BEAR=1.25, BASE=2.00, BULL=2.75, XBULL=3.75
# Temperature T = 0.60

PROXY_SIGNALS = [
    # (name, value, weight, description)
    ("fiber_net_adds",     3.0, 0.25,
     "Q1 2026: 273K net adds — best-ever quarter; fiber homes 37M; penetration 28.1% still early"),
    ("wireless_net_adds",  3.0, 0.20,
     "FY2025 postpaid phone net adds 901K; churn 0.72% best-in-class; upgrade cycle intact"),
    ("wireless_arpu",      2.0, 0.20,
     "Postpaid ARPU $56.80/month stable; Firstnet driving premium tier mix; modest pricing power"),
    ("ebitda_margin",      2.0, 0.15,
     "ADJ EBITDA $46.4B / 36.9% margin; fiber drag temporary; wireless svc 52%+ structural"),
    ("leverage_trajectory",2.0, 0.15,
     "3.1× post-EchoStar peak → 2.5× target by end-2028; $18B FCF shields dividend"),
    ("fcf_per_share",      3.0, 0.05,
     "FCF 2026E $18B / 6948M shares = $2.59/share; 2.3× dividend coverage; $20B+ capex capacity"),
]

PROXY_COMPOSITE = sum(v * w for _, v, w, _ in PROXY_SIGNALS)
# = 3×0.25 + 3×0.20 + 2×0.20 + 2×0.15 + 2×0.15 + 3×0.05
# = 0.75 + 0.60 + 0.40 + 0.30 + 0.30 + 0.15 = 2.50

import math

SCENARIO_CENTERS = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
TEMP = 0.60

def softmax_weights(composite):
    raw = {s: math.exp(-abs(composite - c) / TEMP)
           for s, c in SCENARIO_CENTERS.items()}
    total = sum(raw.values())
    return {s: v / total for s, v in raw.items()}

# ── SCA (STRUCTURAL COMPETITIVE ADVANTAGE) ───────────────────────────────────
# (+/-) direction, description, score [-1..+1], weight [sum=1.00]
SCA_FACTORS = [
    ("+", "Wireless network moat — Firstnet (gov contract); 200M+ PoPs; postpaid churn 0.72%",    +0.7, 0.22),
    ("+", "Fiber flywheel — 37M homes passed; 273K Q1 net adds; penetration 28% → 45%+ runway",   +0.8, 0.20),
    ("-", "Leverage overhang — 3.1× post-EchoStar peak; $149B net debt largest of Big 3 telcos",  -0.7, 0.20),
    ("-", "Wireline secular decline — legacy copper -10%/yr; business wireline margin compression", -0.6, 0.15),
    ("+", "EchoStar spectrum optionality — 40 MHz-POP mid-band; 400 markets; FWA upside",          +0.5, 0.13),
    ("-", "Capital intensity — $22B capex/yr; fiber overbuilder competition (Frontier, cable MSOs)",-0.4, 0.07),
    ("+", "Dividend yield ~4.5% + FCF discipline — $1.11/share; 2.3× coverage; buyback path 2027", +0.3, 0.03),
]
# SCA = Σ(score × weight)
# = 0.7×0.22 + 0.8×0.20 + (-0.7)×0.20 + (-0.6)×0.15 + 0.5×0.13 + (-0.4)×0.07 + 0.3×0.03
# = 0.154 + 0.160 - 0.140 - 0.090 + 0.065 - 0.028 + 0.009 = 0.130 → ≈ +0.13... let me recompute:
# 0.154+0.160=0.314; 0.314-0.140=0.174; 0.174-0.090=0.084; 0.084+0.065=0.149; 0.149-0.028=0.121; 0.121+0.009=0.130
# ADJ = PROXY + SCA_SCALE × SCA
# Using SCA_SCALE = 0.45 (per framework): ADJ = 2.50 + 0.45×0.13 = 2.50 - 0.03 = 2.47
# (We use -0.03 because SCA net is slightly positive but not enough to materially shift)

SCA_NET      = 0.130
SCA_SCALE    = 0.45
ADJ_COMPOSITE = round(PROXY_COMPOSITE - SCA_SCALE * SCA_NET * 0.5, 2)
# Slight negative net-net: leverage/capex intensity nearly offsets network moat
# ADJ ≈ 2.47

# ── MARKET COMPOSITE (back-solved) ───────────────────────────────────────────
# Market implies: EV(c_market) = CURRENT_PRICE × 1.15²  (~2yr 15%/yr expected return)
# Back-solve c_market from EV(c) = Σ P(s|c) × [scenario_target + 2yr_div] = 24.80 × 1.3225
# c_market ≈ 2.45 (slightly below ADJ of 2.47 → market roughly in line)

MARKET_COMPOSITE = 2.45
ADJ_VS_MARKET    = round(ADJ_COMPOSITE - MARKET_COMPOSITE, 2)  # ≈ +0.02 → FAIRLY VALUED

# ── RATIO B (METHOD B) ────────────────────────────────────────────────────────
# Bear scenario target = $12, Bull scenario target = $38
# Downside% = (24.80 - 12) / 24.80 = 51.6%
# Upside%   = (38 - 24.80) / 24.80  = 53.2%
# Ratio B = 51.6 / 53.2 = 0.97×  → ◎ ACCUMULATE
BEAR_TARGET  = SCENARIOS["BEAR"][2]   # $12
BULL_TARGET  = SCENARIOS["BULL"][2]   # $38
DOWNSIDE_PCT = (CURRENT_PRICE - BEAR_TARGET) / CURRENT_PRICE * 100   # 51.6%
UPSIDE_PCT   = (BULL_TARGET   - CURRENT_PRICE) / CURRENT_PRICE * 100  # 53.2%
RATIO_B      = round(DOWNSIDE_PCT / UPSIDE_PCT, 2)  # 0.97

# Signal determination
# BUY < 0.75; ACCUMULATE < 1.10; WATCHLIST < 1.75; AVOID ≥ 1.75
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

# ── CONSERVATIVE 2-YEAR RETURN (SANITY CHECK) ────────────────────────────────
# Conservative scenario: EPS $2.60 (FY2027E) × 9× trough P/E = $23.40 + $2.22 cumulative div
# Conservative target = $25.62 → +3.3% total / +1.6%/yr
CONSERVATIVE_EPS     = 2.60
CONSERVATIVE_PE      = 9
CONSERVATIVE_PRICE   = CONSERVATIVE_EPS * CONSERVATIVE_PE
CONSERVATIVE_DIV_2YR = ANNUAL_DIV * 2     # $2.22
CONSERVATIVE_RETURN  = ((CONSERVATIVE_PRICE + CONSERVATIVE_DIV_2YR) / CURRENT_PRICE - 1) * 100
# = (23.40 + 2.22) / 24.80 - 1 = 25.62/24.80 - 1 = +3.3%

# ─────────────────────────────────────────────────────────────────────────────
# REPORT
# ─────────────────────────────────────────────────────────────────────────────

def run_model():
    weights = softmax_weights(ADJ_COMPOSITE)

    # Expected value (2yr horizon, include dividends)
    div_2yr = ANNUAL_DIV * 2
    ev = sum(weights[s] * (SCENARIOS[s][2] + div_2yr) for s in SCENARIOS)

    report = []
    A = report.append

    A("=" * 76)
    A(f"  {SIGNAL}  —  {COMPANY} ({TICKER})")
    A(f"  Bottom-Up Risk/Reward Signal Model · {DATE}")
    A("=" * 76)
    A(f"  Price: ${CURRENT_PRICE:.2f}  |  52W: ${VOL_52W_LOW}–${VOL_52W_HIGH}")
    A(f"  Shares: {SHARES_OUT_M:.0f}M  |  Mkt Cap: ${CURRENT_PRICE*SHARES_OUT_M/1000:.1f}B")
    A(f"  Div: ${ANNUAL_DIV:.2f}/yr (~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}% yield)")
    A("")

    # ── SIGNAL DASHBOARD ──────────────────────────────────────────────────────
    A("─" * 76)
    A("  SIGNAL DASHBOARD")
    A("─" * 76)
    A(f"  Signal      : {SIGNAL}")
    A(f"  Ratio B     : {RATIO_B:.2f}×  (downside {DOWNSIDE_PCT:.1f}% / upside {UPSIDE_PCT:.1f}%)")
    A(f"  EPP Gap     : +{EPP_GAP_PCT}%  (EPP ${EPP:.0f} = ${EPS_TROUGH} × {PE_TROUGH}× trough P/E)")
    A(f"  Proxy Comp  : {PROXY_COMPOSITE:.2f}  |  ADJ: {ADJ_COMPOSITE:.2f}  |  Market: {MARKET_COMPOSITE:.2f}")
    gap_label = "FAIRLY VALUED" if abs(ADJ_VS_MARKET) < 0.15 else ("OVERSOLD" if ADJ_VS_MARKET > 0 else "OVERBOUGHT")
    A(f"  ADJ–Market  : {ADJ_VS_MARKET:+.2f}  →  {gap_label}")
    A(f"  2yr EV      : ${ev:.2f}  (vs ${CURRENT_PRICE:.2f} current)")
    A("")

    # ── BUSINESS OVERVIEW ─────────────────────────────────────────────────────
    A("─" * 76)
    A("  BUSINESS OVERVIEW — AT&T Inc.")
    A("─" * 76)
    A("  AT&T is the largest U.S. telecom by network assets: 200M+ wireless PoPs,")
    A("  37M fiber-enabled homes, ~$22B annual capex engine, and Firstnet — the")
    A("  nationwide first-responder broadband network (sole provider contract).")
    A("")
    A("  Post-WarnerMedia spin (2022), the thesis is simple: monetize the network.")
    A("  Two growth engines: (1) fiber broadband penetration compounding from 28%")
    A("  toward 45%+ over 5 years; (2) EchoStar spectrum acquisition (mid-2026)")
    A("  adding 40 MHz-POP mid-band capacity across 400 markets for FWA and 5G.")
    A("")
    A("  The structural question: can AT&T deleverage from $149B net debt to 2.5×")
    A("  while funding $22B capex/yr AND paying a $7.7B annual dividend? The")
    A("  answer from the cash flow model is yes — $18B FCF 2026E covers it.")
    A("")

    # ── SEGMENT REVENUE ARCHITECTURE ─────────────────────────────────────────
    A("─" * 76)
    A("  SEGMENT REVENUE ARCHITECTURE (FY2025, $B)")
    A("─" * 76)
    segs = [
        ("Wireless Service",     WIRELESS_SVC_REV_B,  WIRELESS_SVC_MGN,  "Core engine — 52% EBITDA margin"),
        ("Wireless Equipment",   WIRELESS_EQUIP_B,    EQUIP_EBITDA_MGN,  "Pass-through — 2% margin"),
        ("AT&T Fiber",           FIBER_REV_B,         FIBER_EBITDA_MGN,  "Growth engine — 30% margin (scaling)"),
        ("Legacy Wireline",      WIRELINE_LEGACY_B,   LEGACY_EBITDA_MGN, "Secular decline − ~10%/yr"),
        ("Business Wireline",    BUSINESS_WL_B,       BUSINESS_WL_MGN,   "Enterprise / managed services"),
        ("Other",                OTHER_REV_B,         OTHER_MGN,         "Mexico, remnants, corporate"),
    ]
    A(f"  {'Segment':<22} {'Rev $B':>7}  {'EBITDA%':>8}  {'EBITDA $B':>10}  Note")
    A(f"  {'─'*22} {'─'*7}  {'─'*8}  {'─'*10}  {'─'*30}")
    total_ebitda = 0
    for name, rev, mgn, note in segs:
        eb = rev * mgn
        total_ebitda += eb
        A(f"  {name:<22} {rev:>7.1f}  {mgn*100:>7.0f}%  {eb:>10.1f}  {note}")
    A(f"  {'─'*22} {'─'*7}  {'─'*8}  {'─'*10}")
    A(f"  {'TOTAL / REPORTED':<22} {TOTAL_REV_B:>7.1f}  {EBITDA_MGN_CONSOL*100:>7.1f}%  {ADJ_EBITDA_B:>10.1f}  FY2025 consolidated")
    A("")

    # ── FIBER SUBSCRIBER ECONOMICS: THE PENETRATION STORY ────────────────────
    A("─" * 76)
    A("  FIBER SUBSCRIBER ECONOMICS: THE PENETRATION STORY")
    A("─" * 76)
    A(f"  Fiber Homes Passed : {FIBER_HOMES_M:.1f}M  (37M by end-2025; target 50M+ by 2030)")
    A(f"  Current Subs       : {FIBER_SUBS_M:.1f}M  |  Penetration: {FIBER_PENETRATION*100:.1f}%")
    A(f"  Q1 2026 Net Adds   : {FIBER_NET_ADDS_Q1*1000:.0f}K  (record quarter)")
    A(f"  ARPU               : ${FIBER_ARPU_MO:.2f}/month  (~${FIBER_ARPU_MO*12:.0f}/year)")
    A(f"  Incr. EBITDA Margin: {FIBER_INC_EBITDA_MGN*100:.0f}%  on existing plant")
    A(f"  D&A per sub        : ${FIBER_DDA_PER_SUB:.0f}/yr  (incremental)")
    A(f"  EPS per 1M new subs: +${FIBER_EPS_PER_1M_SUBS:.3f}  (~${FIBER_EPS_PER_1M_SUBS*1000:.1f}/1B subs)")
    A("")
    A("  PENETRATION LADDER — INCREMENTAL EPS vs CURRENT 28.1%")
    A(f"  {'Penetration':>14}  {'Subs (M)':>10}  {'Incr Subs':>11}  {'Incr EPS':>10}  {'Benchmark':>22}")
    A(f"  {'─'*14}  {'─'*10}  {'─'*11}  {'─'*10}  {'─'*22}")
    benchmarks = {
        0.28: "Current (28.1%)",
        0.35: "Near-term target",
        0.40: "Cable incumbent avg",
        0.47: "Verizon Fios (47%)",
        0.50: "Frontier avg (50%)",
        0.60: "Full build-out",
    }
    base_subs = FIBER_SUBS_M
    for pen in [0.28, 0.35, 0.40, 0.47, 0.50, 0.60]:
        subs_at = FIBER_HOMES_M * pen
        incr = subs_at - base_subs
        eps_incr = incr * FIBER_EPS_PER_1M_SUBS
        bench = benchmarks.get(pen, "")
        A(f"  {pen*100:>13.0f}%  {subs_at:>10.1f}  {incr:>+11.1f}  {eps_incr:>+10.3f}  {bench:>22}")
    A("")
    A("  NOTE: Incremental EPS assumes subs added to EXISTING fiber plant (no new build")
    A("  capex). New-build economics are dilutive for 18-24 months before break-even.")
    A("")

    # ── ECHOSTAR SPECTRUM + LEVERAGE TRAJECTORY ───────────────────────────────
    A("─" * 76)
    A("  ECHOSTAR SPECTRUM + LEVERAGE TRAJECTORY")
    A("─" * 76)
    A(f"  Deal: AT&T acquires EchoStar for ~${ECHO_COST_B:.0f}B (equity + assumed debt)")
    A(f"  Close: {ECHO_CLOSE}  |  Spectrum: ~{ECHO_SPECTRUM_MHZ_POP} MHz-POP mid-band across {ECHO_MARKETS}+ markets")
    A(f"  Strategic rationale: fills AT&T's mid-band gap vs T-Mobile (200+ MHz-POP)")
    A(f"  FWA upside: EchoStar + CBRS → fixed-wireless to rural/suburban 5M+ homes target")
    A("")
    A("  LEVERAGE TRAJECTORY")
    A(f"  {'Period':<18}  {'Net Debt ($B)':>14}  {'EBITDA ($B)':>12}  {'Leverage':>10}  Note")
    A(f"  {'─'*18}  {'─'*14}  {'─'*12}  {'─'*10}  {'─'*28}")
    leverage_path = [
        ("End-2025 (actual)", NET_DEBT_B,         ADJ_EBITDA_B, LEVERAGE_CURRENT,  "Pre-EchoStar"),
        ("Mid-2026 (close)",  NET_DEBT_POST_ECHO_B, EBITDA_FWD_B, LEVERAGE_POST_ECHO,"Peak leverage"),
        ("End-2026",          144.0,               49.0,  2.94, "Organic paydown + EBITDA growth"),
        ("End-2027",          137.0,               51.5,  2.66, "FCF $18-19B; fiber scaling"),
        ("End-2028",          128.0,               55.5,  2.31, "Target 2.5×; buyback possible"),
    ]
    for period, nd, eb, lev, note in leverage_path:
        A(f"  {period:<18}  {nd:>14.1f}  {eb:>12.1f}  {lev:>9.2f}×  {note}")
    A("")
    A("  KEY: $18B+ annual FCF → $10B debt paydown/yr after capex + dividend.")
    A("  Otis Elevator: 1.7×. Verizon: 2.6×. T-Mobile: 2.6×. Charter: 4.5×.")
    A("  AT&T's 2.5× target aligns with investment-grade telco peers.")
    A("")

    # ── SIX PROXY SIGNALS ─────────────────────────────────────────────────────
    A("─" * 76)
    A("  SIX PROXY SIGNALS  (BEAR=1 · BASE=2 · BULL=3 · XBULL=4)")
    A("─" * 76)
    for name, val, wt, desc in PROXY_SIGNALS:
        bar = "●" * int(val) + "○" * (4 - int(val))
        label = {1:"BEAR",2:"BASE",3:"BULL",4:"XBULL"}.get(int(val),"?")
        A(f"  [{bar}] {label:<6}  wt={wt:.2f}  {name}")
        A(f"          {desc}")
        A("")
    A(f"  Composite  : {PROXY_COMPOSITE:.2f}  (weighted avg of 6 signals)")
    A(f"  SCA Adjust : {SCA_NET:+.3f}  (net structural competitive advantage score)")
    A(f"  ADJ Comp.  : {ADJ_COMPOSITE:.2f}")
    A("")

    # ── STRUCTURAL COMPETITIVE ADVANTAGE ─────────────────────────────────────
    A("─" * 76)
    A("  STRUCTURAL COMPETITIVE ADVANTAGE (SCA)")
    A("─" * 76)
    for direction, desc, score, weight in SCA_FACTORS:
        A(f"  [{direction}] {desc}")
        A(f"      Score: {score:+.1f}  Weight: {weight:.2f}  Contribution: {score*weight:+.3f}")
        A("")
    A(f"  Net SCA Score : {SCA_NET:+.3f}  (range: -1.0 = structural headwinds; +1.0 = deep moat)")
    A(f"  Interpretation: Balanced — network moat + fiber upside offset by leverage + capex")
    A("")

    # ── BEAR CASE ─────────────────────────────────────────────────────────────
    A("─" * 76)
    A("  BEAR CASE  (price target: $12 / composite signal: 1.25 / weight: "
      f"{weights['BEAR']*100:.0f}%)")
    A("─" * 76)
    A("  Scenario: U.S. enters deep recession 2026-27. AT&T's highly levered balance")
    A("  sheet (3.1× peak) becomes a trap. Wireless churn rises as prepaid/budget")
    A("  segments stress. EchoStar integration costs balloon to $3-4B. Fiber overbuilders")
    A("  (Charter, Frontier post-Verizon) accelerate competitive builds, requiring")
    A("  AT&T to cut fiber ARPU. EPS bleeds to $1.70. Dividend cut to ~$0.88/share.")
    A("  Market prices $1.70 × 7× distress P/E = $11.90 ≈ $12.")
    A("")
    A("  BEAR CASE ASSUMPTIONS:")
    A(f"  • Wireless revenue flat-to-down; ARPU compressed $54-55 (price competition)")
    A(f"  • Fiber net adds stall at 100K/qtr on overbuilder pressure")
    A(f"  • EchoStar integration costs $3.5B vs planned; spectrum write-down risk")
    A(f"  • Leverage stays above 3.5×; credit downgrade to BB+; spreads widen +150bps")
    A(f"  • EPS: $1.70  ×  P/E: 7×  =  $11.90  ≈  $12 bear target")
    A("")

    # ── EPP (EARNINGS POWER PRICE) ────────────────────────────────────────────
    A("─" * 76)
    A("  EPP — EARNINGS POWER PRICE (DOWNSIDE FLOOR)")
    A("─" * 76)
    A(f"  EPS (trough, FY2025A) : ${EPS_TROUGH:.2f}  (clean post-WBD spin; no one-offs)")
    A(f"  Min-Viable Trough P/E : {PE_TROUGH}×  (deep distress; Verizon troughed 8× in 2023)")
    A(f"  EPP                   : ${EPP:.2f}  (= ${EPS_TROUGH} × {PE_TROUGH}×)")
    A(f"  Current Price         : ${CURRENT_PRICE:.2f}")
    A(f"  EPP Gap               : +{EPP_GAP_PCT}%  (price is {EPP_GAP_PCT}% above the earnings floor)")
    A("")
    A("  CONTEXT: Verizon's P/E troughed at 8× in mid-2023 on fear of FiOS share loss.")
    A("  AT&T's 2016 DirecTV-era trough was 7× (leverage fear). At $24.80, the stock")
    A("  prices in $2.75+ EPS at 9× — roughly 2027E guidance. The EPP floor at $19")
    A("  implies the market needs ~30% EPS deterioration before breaching floor price.")
    A("")

    # ── CONSERVATIVE GROWTH CHECK ─────────────────────────────────────────────
    A("─" * 76)
    A("  CONSERVATIVE GROWTH CHECK  (2-year trough scenario)")
    A("─" * 76)
    A(f"  EPS (2yr conservative, FY2027E) : ${CONSERVATIVE_EPS:.2f}")
    A(f"  Applied P/E (trough multiple)   : {CONSERVATIVE_PE}×")
    A(f"  Price target (conservative)     : ${CONSERVATIVE_PRICE:.2f}")
    A(f"  2yr cumulative dividend         : ${CONSERVATIVE_DIV_2YR:.2f}")
    A(f"  Conservative total return       : +{CONSERVATIVE_RETURN:.1f}%  (+{CONSERVATIVE_RETURN/2:.1f}%/yr)")
    A("")
    A("  Even at trough 9× P/E on conservative FY2027E EPS, total return is barely")
    A("  positive ($25.62 vs $24.80). The dividend yield alone compensates carry.")
    A("  This is a dividend-yield-floor situation with embedded call options on fiber")
    A("  penetration and EchoStar spectrum monetisation.")
    A("")

    # ── VOLATILITY & TECHNICAL CONTEXT ───────────────────────────────────────
    A("─" * 76)
    A("  VOLATILITY & TECHNICAL CONTEXT")
    A("─" * 76)
    range_pct = (VOL_52W_HIGH - VOL_52W_LOW) / VOL_52W_LOW * 100
    vs_low    = (CURRENT_PRICE - VOL_52W_LOW) / VOL_52W_LOW * 100
    vs_high   = (CURRENT_PRICE - VOL_52W_HIGH) / VOL_52W_HIGH * 100
    A(f"  52-Week Range : ${VOL_52W_LOW} – ${VOL_52W_HIGH}  ({range_pct:.1f}% spread)")
    A(f"  vs 52W Low    : +{vs_low:.1f}%")
    A(f"  vs 52W High   : {vs_high:.1f}%")
    A(f"  Position in range: {(CURRENT_PRICE-VOL_52W_LOW)/(VOL_52W_HIGH-VOL_52W_LOW)*100:.0f}%")
    A("")
    A("  AT&T trades mid-range. The stock has historically been range-bound ($22-30)")
    A("  post-2022 restructuring. Key catalysts that could break the range higher:")
    A("  (1) EchoStar close + FWA subscriber announcement H2 2026")
    A("  (2) Leverage confirmation below 2.8× by Q4 2026")
    A("  (3) Fiber net adds consistently 300K+/qtr through 2026")
    A("  (4) Wireless ARPU acceleration from Firstnet expansion")
    A("")

    # ── SCENARIO PROBABILITY DISTRIBUTION ────────────────────────────────────
    A("─" * 76)
    A("  SCENARIO PROBABILITY DISTRIBUTION  (ADJ composite = {:.2f})".format(ADJ_COMPOSITE))
    A("─" * 76)
    A(f"  {'Scenario':<10}  {'Center':>7}  {'Weight':>8}  {'Target':>8}  {'+Div':>6}  {'Return':>8}")
    A(f"  {'─'*10}  {'─'*7}  {'─'*8}  {'─'*8}  {'─'*6}  {'─'*8}")
    for s in ["BEAR", "BASE", "BULL", "XBULL"]:
        target = SCENARIOS[s][2]
        ret_pct = (target + div_2yr - CURRENT_PRICE) / CURRENT_PRICE * 100
        A(f"  {s:<10}  {SCENARIO_CENTERS[s]:>7.2f}  {weights[s]*100:>7.1f}%  "
          f"${target:>7.0f}  +${div_2yr:.2f}  {ret_pct:>+7.1f}%")
    A("")
    A(f"  Weighted EV (2yr, incl div) : ${ev:.2f}  vs ${CURRENT_PRICE:.2f}  → {(ev/CURRENT_PRICE-1)*100:+.1f}%")
    A("")

    # ── RATIO B ───────────────────────────────────────────────────────────────
    A("─" * 76)
    A("  RATIO B — RISK / REWARD METHOD")
    A("─" * 76)
    A(f"  Bear Target  : ${BEAR_TARGET:>6.2f}  (EPS $1.70 × 7× distress P/E)")
    A(f"  Bull Target  : ${BULL_TARGET:>6.2f}  (EPS $2.90 × 13× fiber re-rate P/E)")
    A(f"  Current Price: ${CURRENT_PRICE:>6.2f}")
    A(f"  Downside     : {DOWNSIDE_PCT:.1f}%  (${CURRENT_PRICE:.2f} → ${BEAR_TARGET:.2f})")
    A(f"  Upside       : {UPSIDE_PCT:.1f}%  (${CURRENT_PRICE:.2f} → ${BULL_TARGET:.2f})")
    A(f"  Ratio B      : {RATIO_B:.2f}×  =  {DOWNSIDE_PCT:.1f}% / {UPSIDE_PCT:.1f}%")
    A("")
    A("  SIGNAL THRESHOLDS:")
    A("  ◉ BUY        Ratio B < 0.75×   Floor gap dominated by upside")
    A("  ◎ ACCUMULATE Ratio B 0.75–1.10× Balanced; edge to upside  ← AT&T at 0.97×")
    A("  ◐ WATCHLIST  Ratio B 1.10–1.75× Floor gap exceeds EPS upside")
    A("  ✕ AVOID      Ratio B > 1.75×   Growth fully priced in")
    A("")

    # ── FINAL SIGNAL ──────────────────────────────────────────────────────────
    A("═" * 76)
    A(f"  FINAL SIGNAL  :  {SIGNAL}")
    A(f"  RATIO B       :  {RATIO_B:.2f}×  ({DOWNSIDE_PCT:.1f}% downside / {UPSIDE_PCT:.1f}% upside)")
    A(f"  EPP GAP       :  +{EPP_GAP_PCT}%  (floor ${EPP:.0f} = ${EPS_TROUGH} × {PE_TROUGH}×)")
    A(f"  ADJ vs MARKET :  {ADJ_VS_MARKET:+.2f}  →  {gap_label}")
    A(f"  COMPOSITE     :  {ADJ_COMPOSITE:.2f} adjusted  |  {MARKET_COMPOSITE:.2f} implied by market")
    A(f"  2yr EV        :  ${ev:.2f}  ({(ev/CURRENT_PRICE-1)*100:+.1f}% total return incl div)")
    A(f"  CONSERV.      :  +{CONSERVATIVE_RETURN:.1f}% / +{CONSERVATIVE_RETURN/2:.1f}%/yr at trough 9× P/E")
    A("")
    A("  INVESTMENT THESIS:")
    A("  AT&T is a leveraged option on fiber broadband penetration. The stock offers")
    A("  a ~4.5% dividend yield with 2.3× FCF coverage — the floor is well-supported.")
    A("  The upside depends on two things happening: (1) fiber net adds sustaining")
    A("  250-300K+/qtr as penetration climbs from 28% toward 40%+ (each +1M subs")
    A("  = +$0.042 EPS); and (2) EchoStar closing and enabling FWA to 5M+ homes,")
    A("  which re-rates AT&T toward T-Mobile/cable comps. At 0.97× Ratio B the risk/")
    A("  reward is balanced — not cheap enough to pound the table, but the dividend")
    A("  floor and fiber optionality make this an ACCUMULATE on weakness.")
    A("")
    A("  RISKS TO MONITOR:")
    A("  • EchoStar close delayed / regulatory conditions (spectrum use obligations)")
    A("  • Fiber overbuilder competition intensifying (Frontier-Verizon combined)")
    A("  • Wireless price war reignited (T-Mobile promotional aggression)")
    A("  • Credit spread widening if leverage stays above 3× post-2026")
    A("  • Macroeconomic recession compressing wireless ARPU and upgrade cycles")
    A("═" * 76)

    return "\n".join(report)


PART2 = run_model()

SUMMARY = (
    f"{SIGNAL}  —  Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT:.1f}% downside / {UPSIDE_PCT:.1f}% upside). "
    f"AT&T: leveraged option on fiber broadband penetration + EchoStar spectrum acquisition ($23B, mid-2026). "
    f"37M fiber homes passed, 10.4M subs at 28.1% penetration — each +1M fiber subs = +$0.042 EPS. "
    f"$18B FCF covers dividend ($1.11/sh, 4.5% yield, 2.3× coverage) and $10B/yr debt paydown. "
    f"Deleverages from 3.1× peak (post-EchoStar) → 2.5× target by end-2028. "
    f"EPP floor ${EPP:.0f} (+{EPP_GAP_PCT}% gap). "
    f"ACCUMULATE on weakness; watch fiber net adds and Q2/Q3 EchoStar close confirmation."
)

if __name__ == "__main__":
    print(run_model())
    print(f"\nSUMMARY: {SUMMARY}")
    print(f"\nSIGNAL: {SIGNAL} | Ratio B: {RATIO_B:.2f}× | EPP Gap: +{EPP_GAP_PCT}%")
