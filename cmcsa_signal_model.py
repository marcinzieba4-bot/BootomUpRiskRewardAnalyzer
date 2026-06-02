"""
Comcast Corporation (NASDAQ: CMCSA) — Bottom-Up Risk/Reward Signal Model
BottomUp Risk/Reward Analyzer · veerock framework
Date: 2026-06-01

NOTE: CMCSA is a deep-value FCF story misread as a secular-decline play. At $29.59 the stock
trades BELOW EPP (earnings power floor) — a rare signal that the market is pricing in sustained
EPS deterioration that the cash flow statement directly contradicts. Adjusted EPS is used
throughout; GAAP EPS is distorted by D&A on $69B NBCUniversal / Sky acquisition intangibles.
"""

# ── PRICE & MARKET DATA ───────────────────────────────────────────────────────
TICKER            = "CMCSA"
COMPANY           = "Comcast Corporation"
SECTOR            = "Cable & Broadband · NBCUniversal · Peacock · Sky Europe · NASDAQ: CMCSA"
DATE              = "2026-06-01"
CURRENT_PRICE     = 29.59
VOL_52W_LOW       = 24.35
VOL_52W_HIGH      = 34.66
SHARES_OUT_M      = 3617.0    # Diluted, Q1 2026; reduced via $6.8B buybacks in FY2025
ANNUAL_DIV        = 1.32      # $0.33/quarter; ~4.73% yield; 15-year consecutive growth streak

# ── VERSANT SPINOFF (COMPLETED JANUARY 2, 2026) ───────────────────────────────
# Comcast spun off 'Versant Media Group' (ticker: VSNT) — cable TV networks
# SPUN OFF → Versant: CNBC, MSNBC, Bravo, USA, Oxygen, E!, Syfy, Golf Channel + Fandango/Rotten Tomatoes
# RETAINED  → Comcast: NBC, Telemundo, Universal Pictures, DreamWorks, Peacock, Sky
# Structure: shareholders received 1 VSNT share per 25 CMCSA shares (tax-free)
# Estimated Versant value: ~$7B; opened at $45.17/share, fell below $40 on debut
# Revenue impact: removes ~$7B cable network revenue from Comcast consolidated
VERSANT_REVENUE_B      = 7.0    # Removed from Comcast consolidated on Jan 2, 2026
VERSANT_EBITDA_B       = 1.5    # Estimated EBITDA removed (low-margin declining cable nets)

# ── CONNECTIVITY & CABLE (XFINITY) ───────────────────────────────────────────
# Broadband
BROADBAND_TOTAL_M      = 31.255  # Total broadband customers, end-2025
BROADBAND_RESI_M       = 28.71   # Residential
BROADBAND_BUSI_M       =  2.53   # Business
BROADBAND_LOST_FY2025  =  0.711  # Net subscriber losses in FY2025 (711K)
BROADBAND_LOST_Q1_26   =  0.065  # Q1 2026 net losses = 65K (best since Q4 2020; -117K YoY)
# Competitive threat: AT&T Fiber, T-Mobile FWA, Verizon FiOS/FWA
# Response: DOCSIS 4.0 upgrade (multi-gig symmetrical), simplified pricing, Xfinity Mobile bundle

# Wireless (Xfinity Mobile — MVNO on Verizon network)
WIRELESS_LINES_M       =  9.305  # End-2025 total wireless lines
WIRELESS_ADDS_FY2025   =  1.5    # Record 1.5M net adds in FY2025
WIRELESS_PENETRATION   =  0.15   # 15% of residential broadband base (85% upside remaining)

# Video
VIDEO_SUBS_M           = 13.0    # Approx residential video subscribers (declining ~5M/yr)
# Video cable TV losses are a feature, not a bug — low-margin drag being shed naturally

# ── NBCUNIVERSAL SEGMENT ─────────────────────────────────────────────────────
# Theme Parks
PARKS_REV_Q2_2025_B    = 2.349   # Q2 2025 theme parks revenue (+19% YoY)
PARKS_EBITDA_Q2_2025_B = 1.035   # Q2 2025 theme parks EBITDA (+23.5%; first $1B+ quarter)
PARKS_REV_Q1_2026_B    = 2.44    # Q1 2026 theme parks revenue (+24% YoY)
EPIC_UNIVERSE_OPENED   = "May 22, 2025"   # Universal Orlando's 5th theme park
EPIC_UNIVERSE_UK       = "Bedford, England; construction 2026, opening 2031"
# Epic Universe: Wizarding World, Nintendo, Epic Universes of Fear, Celestial Park, HTTYD
# Less cannibalization than feared; driving longer stays, higher per-cap spend

# Peacock Streaming
PEACOCK_SUBS_M         = 46.0    # Q1 2026 paid subscribers (+12% YoY, +2M QoQ)
PEACOCK_REV_Q1_26_B    = 2.0     # Q1 2026 revenue (>$2B for first time; +71% YoY)
PEACOCK_LOSS_Q1_26_B   = 0.432   # Q1 2026 EBITDA loss ($432M, elevated from NBA rights cost)
PEACOCK_PROFITABILITY  = "Q2 2026E (management guidance)"
# NFL Sunday Night Football, NBA, Olympics (2026 Milan, 2028 LA), WWE, Premier League

# ── SKY EUROPE ───────────────────────────────────────────────────────────────
SKY_MARKETS        = "UK, Germany, Italy"
SKY_REV_APPROX_B   = 19.0    # Estimated FY2025 Sky segment revenue (includes FX)
# Sky faces: streaming disruption, Premier League rights costs, FX headwinds (GBP/EUR vs USD)

# ── FINANCIALS ────────────────────────────────────────────────────────────────
# FY2025 (ended December 31, 2025 — full year including Versant pre-spinoff)
REVENUE_FY2025_B       = 123.7   # Flat vs $123.7B in 2024 (Versant included through Dec 31)
ADJ_EPS_FY2025         = 4.30    # Q1 $1.09 + Q2 $1.25 + Q3 $1.12 + Q4 $0.84
FCF_FY2025_B           = 17.5    # Estimate; Q1-Q3 YTD $14.8B + Q4 ~$2.7B
CAPITAL_RETURN_FY2025_B= 11.7    # $6.8B buybacks + $4.9B dividends

# FY2026E (post-Versant Comcast; Versant deconsolidated from Jan 2, 2026)
ADJ_EPS_FY2026E        = 4.14    # Analyst consensus (depressed by Versant removal)
FCF_FY2026E_B          = 15.0    # Conservative estimate post-Versant

# Balance sheet (Q1 2026, March 31)
TOTAL_DEBT_B           = 94.6    # Total debt (LT $89.2B + current ~$5.4B)
CASH_B                 =  9.5    # Cash and equivalents
NET_DEBT_B             = 85.1    # = 94.6 - 9.5
# Post-Versant adj EBITDA estimate: ~$36-37B → Net debt / EBITDA ≈ 2.3×
ADJ_EBITDA_FY2026E_B   = 36.5    # Post-Versant consolidated
LEVERAGE_MULTIPLE      = round(NET_DEBT_B / ADJ_EBITDA_FY2026E_B, 2)   # ≈ 2.33×

# ── EPP (EARNINGS POWER PRICE) ────────────────────────────────────────────────
# KEY SIGNAL: STOCK IS TRADING BELOW THE EARNINGS FLOOR
EPS_TROUGH     = 3.80   # Conservative FY2026E adj EPS (ARPU pressure + Versant removal)
PE_TROUGH      = 9      # Cable/media trough P/E (levered media company stress multiple)
EPP            = EPS_TROUGH * PE_TROUGH   # = $34.20
EPP_GAP_PCT    = round((CURRENT_PRICE / EPP - 1) * 100, 1)   # = -13.5%
# NEGATIVE EPP GAP means the stock is BELOW the earnings floor.
# This is an extreme buy signal: the market is pricing in ongoing EPS erosion
# that the free cash flow trajectory directly contradicts ($15B+ FCF/yr).

# ── SCENARIO ASSUMPTIONS ─────────────────────────────────────────────────────
# (adj_eps, exit_pe, target_price, rationale)
SCENARIOS = {
    "BEAR":  (2.50, 8, 20,
              "Broadband loses 1M+/yr; ARPU -5%/yr from competition; Peacock delays profitability "
              "to 2028; Sky underperforms. EPS compressed to $2.50 × 8× distress P/E → $20."),
    "BASE":  (4.00, 10, 38,
              "Broadband losses stabilize at 200-300K/yr; Peacock profitable H2 2026; "
              "Epic Universe steady; Sky stable. EPS $4.00 × 9.5× → $38."),
    "BULL":  (4.50, 12, 54,
              "Broadband net sub losses turn positive via DOCSIS 4.0 + mobile bundle; "
              "Peacock scales to 60M subs; Epic UK opens ahead of 2031. EPS $4.50 × 12× → $54."),
    "XBULL": (5.50, 13, 70,
              "Re-rate on FCF/infrastructure story; Xfinity Mobile 15M+ lines; Peacock cash flow "
              "positive; EPS $5.50 × 13× → $71.5 ≈ $70. Cable REIT-like re-rating."),
}

# ── SOFTMAX SIGNAL MODEL ──────────────────────────────────────────────────────
PROXY_SIGNALS = [
    # (name, value [1-4], weight, description)
    ("broadband_stabilization",   3.0, 0.30,
     "Q1 2026 losses narrowed to 65K (best since Q4 2020; -117K YoY). DOCSIS 4.0 upgrades. "
     "Simplified pricing + free mobile bundling addresses churn. Losses should be near floor."),
    ("xfinity_mobile_growth",     3.0, 0.20,
     "9.305M lines end-2025; +1.5M record in FY2025; 15% penetration = 85% of broadband base "
     "untapped. MVNO on Verizon; ~$40/mo ARPU; powerful churn reducer and ARPU booster."),
    ("theme_parks_epic_universe", 3.0, 0.20,
     "Epic Universe opened May 2025; Q2 2025 parks revenue +19%, EBITDA first $1B+ quarter. "
     "Q1 2026 parks +24%. Less cannibalization than feared. UK park 2031 = next catalyst."),
    ("peacock_inflection",        3.0, 0.15,
     "46M paid subs; Q1 2026 revenue $2B+ (+71% YoY). $432M Q1 loss = NBA/Olympics peak cost. "
     "Management guiding Q2 2026 approach profitability. Path is visible and credible."),
    ("fcf_capital_return",        2.0, 0.10,
     "$15B+ annual FCF; $11.7B returned in FY2025 ($6.8B buybacks + $4.9B div). "
     "Dividend $1.32/yr (+4.7% yield). Buybacks at 7.8× earnings = high IRR. "
     "But net debt $85B (2.3× EBITDA) limits re-rating speed."),
    ("versant_portfolio_clarity", 2.0, 0.05,
     "Versant completed Jan 2, 2026. Comcast is now: broadband + wireless + NBCUniversal (NBC, "
     "Universal, Peacock, parks) + Sky. Clean story. But ARPU pressure ongoing in 2026."),
]

PROXY_COMPOSITE = sum(v * w for _, v, w, _ in PROXY_SIGNALS)
# = 3.0×0.30 + 3.0×0.20 + 3.0×0.20 + 3.0×0.15 + 2.0×0.10 + 2.0×0.05
# = 0.90 + 0.60 + 0.60 + 0.45 + 0.20 + 0.10 = 2.85

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
    ("+", "Xfinity broadband infrastructure: near-monopoly in 40 states; high switching costs; "
          "DOCSIS 4.0 = multi-gig symmetric; HFC cheaper to upgrade than build fiber from scratch", +0.7, 0.25),
    ("-", "Broadband competitive disruption: AT&T Fiber + T-Mobile FWA + Verizon accelerating; "
          "sub losses 711K in 2025; ARPU pressure from simplified pricing + free mobile bundles",  -0.6, 0.20),
    ("+", "Universal Theme Parks + IP: Epic Universe, Jurassic World, Wizarding World, Mario, "
          "DreamWorks; UK park 2031; parks EBITDA $4B+/yr and growing; moat vs Disney in Orlando",  +0.7, 0.20),
    ("+", "Xfinity Mobile flywheel: MVNO with Verizon; 9.3M lines; 15% penetration → 85% runway; "
          "mobile bundle reduces broadband churn; structural convergence advantage",                 +0.5, 0.15),
    ("-", "Secular video cord-cutting: ~13M video subs declining; Versant removes cable nets but "
          "CMCSA still has programming costs; legacy video still ~$5B revenue headwind/yr",          -0.4, 0.10),
    ("+", "Peacock sports rights: NFL Sunday Night Football, NBA, Olympics 2026/2028, Premier "
          "League; approaching profitability; 46M subs; sports = OTT moat vs Netflix",              +0.5, 0.07),
    ("-", "Sky Europe execution: FX headwinds (GBP/EUR/USD); streaming disruption; sports rights "
          "inflation (Premier League); political/regulatory risk in UK post-Brexit",                 -0.3, 0.03),
]
# SCA = Σ(score × weight)
# = 0.7×0.25 + (-0.6)×0.20 + 0.7×0.20 + 0.5×0.15 + (-0.4)×0.10 + 0.5×0.07 + (-0.3)×0.03
# = 0.175 - 0.120 + 0.140 + 0.075 - 0.040 + 0.035 - 0.009 = +0.256

SCA_NET      = 0.256
SCA_SCALE    = 0.45
ADJ_COMPOSITE = round(PROXY_COMPOSITE + SCA_SCALE * SCA_NET * 0.5, 2)
# = 2.85 + 0.45 × 0.256 × 0.5 = 2.85 + 0.058 = 2.91

# ── MARKET COMPOSITE (back-solved) ───────────────────────────────────────────
# Market implies EV(c_market) = CURRENT_PRICE × 1.15²  (2yr, 15%/yr expected return)
# Back-solve from EV including 2yr dividends ($2.64):
# c_market ≈ 1.90 — market pricing between BASE/BEAR, consistent with "Hold" consensus
# at 26 analysts and deeply depressed multiple (7.8× adj EPS)
MARKET_COMPOSITE  = 1.90
ADJ_VS_MARKET     = round(ADJ_COMPOSITE - MARKET_COMPOSITE, 2)  # = +1.01 → SIGNIFICANTLY UNDERVALUED

# ── RATIO B ───────────────────────────────────────────────────────────────────
BEAR_TARGET  = SCENARIOS["BEAR"][2]    # $20
BULL_TARGET  = SCENARIOS["BULL"][2]    # $54
DOWNSIDE_PCT = (CURRENT_PRICE - BEAR_TARGET) / CURRENT_PRICE * 100    # 32.4%
UPSIDE_PCT   = (BULL_TARGET   - CURRENT_PRICE) / CURRENT_PRICE * 100  # 82.5%
RATIO_B      = round(DOWNSIDE_PCT / UPSIDE_PCT, 2)    # 0.39

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
# Even at trough P/E on below-consensus EPS, the stock has upside
CONSERVATIVE_EPS       = 4.00    # FY2027E conservative (below consensus; ARPU pressure)
CONSERVATIVE_PE        = 9       # Trough cable P/E
CONSERVATIVE_PRICE     = CONSERVATIVE_EPS * CONSERVATIVE_PE   # = $36.00
CONSERVATIVE_DIV_2YR   = ANNUAL_DIV * 2     # = $2.64
CONSERVATIVE_RETURN    = ((CONSERVATIVE_PRICE + CONSERVATIVE_DIV_2YR) / CURRENT_PRICE - 1) * 100
# = (36.00 + 2.64) / 29.59 - 1 = 38.64 / 29.59 - 1 = +30.6%
# STRONG conservative case because even trough P/E is above current market price

# ─────────────────────────────────────────────────────────────────────────────
# REPORT
# ─────────────────────────────────────────────────────────────────────────────

def run_model():
    weights = softmax_weights(ADJ_COMPOSITE)
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
    A(f"  Div: ${ANNUAL_DIV:.2f}/yr ({ANNUAL_DIV/CURRENT_PRICE*100:.1f}% yield)")
    A(f"  Net Debt: ${NET_DEBT_B:.1f}B  |  Net Debt / EBITDA: {LEVERAGE_MULTIPLE:.2f}×")
    A("")

    # ── SIGNAL DASHBOARD ────────────────────────────────────────────────────
    A("─" * 76)
    A("  SIGNAL DASHBOARD")
    A("─" * 76)
    A(f"  Signal      : {SIGNAL}")
    A(f"  Ratio B     : {RATIO_B:.2f}×  (downside {DOWNSIDE_PCT:.1f}% / upside {UPSIDE_PCT:.1f}%)")
    A(f"  EPP Gap     : {EPP_GAP_PCT:.1f}%  ← NEGATIVE: STOCK IS BELOW EPP FLOOR")
    A(f"              : EPP ${EPP:.2f} = ${EPS_TROUGH} trough adj EPS × {PE_TROUGH}× trough P/E")
    A(f"  Proxy Comp  : {PROXY_COMPOSITE:.2f}  |  ADJ: {ADJ_COMPOSITE:.2f}  |  Market: {MARKET_COMPOSITE:.2f}")
    A(f"  ADJ–Market  : {ADJ_VS_MARKET:+.2f}  →  SIGNIFICANTLY UNDERVALUED")
    A(f"  2yr EV      : ${ev:.2f}  (vs ${CURRENT_PRICE:.2f} current; includes div)")
    A(f"  Conserv.    : +{CONSERVATIVE_RETURN:.1f}% / +{CONSERVATIVE_RETURN/2:.1f}%/yr")
    A(f"              : (EPS ${CONSERVATIVE_EPS:.2f} × {CONSERVATIVE_PE}× trough P/E + ${CONSERVATIVE_DIV_2YR:.2f} div)")
    A("")
    A("  ★ RARE SIGNAL: Stock trades BELOW earnings power floor ($34.20). This")
    A("    occurs when the market prices in sustained deterioration that the")
    A("    free cash flow trajectory directly contradicts ($15B+ FCF/yr).")
    A("")

    # ── BUSINESS OVERVIEW ────────────────────────────────────────────────────
    A("─" * 76)
    A("  BUSINESS OVERVIEW — Comcast Corporation (Post-Versant)")
    A("─" * 76)
    A("  Comcast after the January 2, 2026 Versant spinoff is a four-segment company:")
    A("")
    A("  1. CONNECTIVITY (XFINITY): 31M broadband customers + 9.3M Xfinity Mobile")
    A("     lines. America's largest internet provider. Revenue ~$65B. The entire")
    A("     bear thesis is here — but broadband losses are narrowing and DOCSIS 4.0")
    A("     upgrades preserve the speed advantage vs fiber for 5+ years.")
    A("")
    A("  2. NBCUniversal: NBC/Telemundo broadcast + Universal Pictures/DreamWorks")
    A("     studios + Universal Theme Parks (Epic Universe launched May 2025).")
    A("     Revenue ~$24B. The theme parks are the crown jewel — $4B+ EBITDA/yr.")
    A("")
    A("  3. PEACOCK: 46M paid subs; >$2B quarterly revenue; approaching profitability")
    A("     Q2 2026. NFL Sunday Night Football, NBA, Olympics 2026/2028. Not a")
    A("     Netflix-killer — a sports-anchored cable bundle replacement.")
    A("")
    A("  4. SKY EUROPE: UK, Germany, Italy pay-TV + streaming. ~$19B revenue.")
    A("     Premier League, original drama, Sky News. FX and sports rights headwinds.")
    A("")
    A("  VERSANT (SPUN OFF): CNBC, MSNBC, Bravo, USA, Syfy, E!, Oxygen, Golf Channel")
    A("  → Comcast shareholders received 1 VSNT share per 25 CMCSA shares (Jan 2, 2026)")
    A("")

    # ── BROADBAND: THE CORE BUSINESS ──────────────────────────────────────────
    A("─" * 76)
    A("  BROADBAND — THE CORE BUSINESS (AND THE BEAR FEAR)")
    A("─" * 76)
    A(f"  Total broadband subs : {BROADBAND_TOTAL_M:.3f}M  ({BROADBAND_RESI_M:.2f}M resi + {BROADBAND_BUSI_M:.2f}M business)")
    A(f"  FY2025 net losses    : -{BROADBAND_LOST_FY2025*1000:.0f}K  (711K for the full year)")
    A(f"  Q1 2026 net losses   : -{BROADBAND_LOST_Q1_26*1000:.0f}K  (best quarter since Q4 2020)")
    A(f"  YoY improvement Q1   : +117K  (clear trend inflection)")
    A(f"  ARPU trend 2026      : Declining in early 2026 (simplified pricing + free wireless)")
    A("")
    A("  COMPETITION LANDSCAPE:")
    A("  • AT&T Fiber: 37M homes passed; 10.4M subs; accelerating (~273K/qtr)")
    A("  • T-Mobile FWA: 6M+ home internet customers; ~1M/qtr net adds")
    A("  • Verizon FiOS + FWA: competitive in Northeast markets")
    A("  • Charter Spectrum: indirect competition; same overbuilder threat")
    A("")
    A("  COMCAST'S RESPONSE:")
    A("  • DOCSIS 4.0: Multi-gig symmetrical speeds (4-6× faster upload); HFC upgrade")
    A("    costs ~$5-8B total vs AT&T's $150B fiber capex — massive structural advantage")
    A("  • Xfinity Mobile bundle: free wireless line with broadband = churn reduction")
    A("  • Multi-year price lock packages: winning back price-sensitive switchers")
    A("  • Q1 2026 sub losses narrowed to 65K → stabilization trend is intact")
    A("")
    A("  CONTEXT: Comcast has 31M broadband subs in a market of ~120M U.S. households.")
    A("  AT&T has 10.4M fiber subs. T-Mobile FWA has 6M. Even in a world where")
    A("  competitors triple, Comcast retains 20M+ subs at $80+ ARPU = $19B+ revenue.")
    A("")

    # ── XFINITY MOBILE: THE SECRET WEAPON ────────────────────────────────────
    A("─" * 76)
    A("  XFINITY MOBILE: THE SECRET WEAPON")
    A("─" * 76)
    A(f"  Lines (end-2025) : {WIRELESS_LINES_M:.3f}M  (record +{WIRELESS_ADDS_FY2025:.1f}M in FY2025)")
    A(f"  Penetration      : {WIRELESS_PENETRATION*100:.0f}% of residential broadband base")
    A(f"  Remaining runway : {(1-WIRELESS_PENETRATION)*100:.0f}% of broadband base untapped = ~26M lines potential")
    A("")
    A("  WHY XFINITY MOBILE MATTERS:")
    A("  • Bundled mobile lines reduce broadband churn by 30-40% (comparable to AT&T data)")
    A("  • Each mobile line = ~$40/mo ARPU on a near-zero marginal cost MVNO")
    A("  • 9.3M lines × $40/mo = ~$4.5B mobile revenue run-rate")
    A("  • 20M target (at 60% penetration) = $9.6B run-rate; incremental EBITDA $3-4B")
    A("  • T-Mobile grew from 9M to 100M+ lines over 10 years; Comcast is at equivalent T-Mo 2013")
    A("  • Comcast can leverage its 40M+ homes footprint for MVNO → eventually MNO via CBRS/spectrum")
    A("")

    # ── EPIC UNIVERSE & THEME PARKS ───────────────────────────────────────────
    A("─" * 76)
    A("  EPIC UNIVERSE & UNIVERSAL THEME PARKS — THE SURPRISE UPSIDE")
    A("─" * 76)
    A(f"  Epic Universe opened  : {EPIC_UNIVERSE_OPENED}  (Universal Orlando, 5th park)")
    A(f"  Q2 2025 parks revenue : ${PARKS_REV_Q2_2025_B:.3f}B  (+19% YoY)")
    A(f"  Q2 2025 parks EBITDA  : ${PARKS_EBITDA_Q2_2025_B:.3f}B  (+23.5%; first $1B+ quarter)")
    A(f"  Q1 2026 parks revenue : ${PARKS_REV_Q1_2026_B:.2f}B  (+24% YoY)")
    A(f"  UK expansion          : {EPIC_UNIVERSE_UK}")
    A("")
    A("  EPIC UNIVERSE THESIS:")
    A("  Universal now operates 5 parks in Orlando (vs Disney's 4). The Wizarding World,")
    A("  Nintendo World, and How to Train Your Dragon IP were expected to cannibalize")
    A("  Universal Studios Florida and Islands of Adventure. This has not materialized —")
    A("  Epic Universe is driving INCREMENTAL attendance and longer stays.")
    A("")
    A("  IP pipeline: Universal has Wicked (franchise), Minecraft (acquisition 2024),")
    A("  Illumination (Minions/Despicable Me), Jurassic World Evolution. Comcast's")
    A("  theme park IP library rivals Disney and will be even richer at Bedford (2031).")
    A("")
    A("  Parks EBITDA FY2025E: ~$4B (up from ~$2.9B FY2024). This single segment is")
    A("  worth $40-50B at Disney/Six Flags 10-12× EV/EBITDA — but is hidden inside the")
    A("  Comcast sum-of-parts that the market values at $107B enterprise for ALL segments.")
    A("")

    # ── PEACOCK ───────────────────────────────────────────────────────────────
    A("─" * 76)
    A("  PEACOCK — INFLECTING TOWARD PROFITABILITY")
    A("─" * 76)
    A(f"  Paid subscribers : {PEACOCK_SUBS_M:.0f}M  (Q1 2026; +12% YoY; +2M QoQ)")
    A(f"  Q1 2026 revenue  : >${PEACOCK_REV_Q1_26_B:.0f}B  (+71% YoY; first $2B quarter)")
    A(f"  Q1 2026 EBITDA   : -${PEACOCK_LOSS_Q1_26_B*1000:.0f}M  (NBA amortization peak; a known, temporary cost)")
    A(f"  Profitability    : {PEACOCK_PROFITABILITY}")
    A("")
    A("  PEACOCK IS NOT NETFLIX — AND THAT'S OK:")
    A("  Peacock's value comes from its sports bundle: NFL SNF (most-watched weekly show),")
    A("  NBA (multi-year rights), 2026 Milan Winter Olympics, 2028 LA Summer Olympics,")
    A("  and Premier League in the U.S. These rights are exclusivity moats that prevent")
    A("  subscriber churn and justify the $7-10/month price point.")
    A("")
    A("  The Q1 2026 $432M loss is a ONE-TIME NBA rights amortization spike, not a trend.")
    A("  Management visibility into Q2 profitability inflection is credible given the")
    A("  trajectory: Q4 2024 loss ~$400M → Q2 2025 loss $101M → Q2 2026E breakeven.")
    A("")

    # ── SUM-OF-PARTS CROSS-CHECK ──────────────────────────────────────────────
    A("─" * 76)
    A("  SUM-OF-PARTS CROSS-CHECK (EV/EBITDA PEER COMPARISONS)")
    A("─" * 76)
    segments_sop = [
        ("Cable Connectivity (EBITDA ~$23B)", 7.0,  "Charter: 7-8× EV/EBITDA", 161.0),
        ("Theme Parks (EBITDA ~$4.5B)",       12.0, "Disney Parks: 12-14×",      54.0),
        ("NBCUniversal Studios/Broadcast",     8.0,  "Fox Corp/Paramount avg: 7-9×",24.0),
        ("Peacock (pre-profitability)",         5.0,  "Discounted for loss stage",   10.0),
        ("Sky Europe (~$3.5B EBITDA)",          7.0,  "Sky historical: 7-8×",        24.5),
    ]
    A(f"  {'Segment':<38}  {'EV/EBITDA':>10}  {'Peer Basis':>24}  {'Segment EV $B':>14}")
    A(f"  {'─'*38}  {'─'*10}  {'─'*24}  {'─'*14}")
    total_sop = 0
    for name, mult, peer, seg_ev in segments_sop:
        A(f"  {name:<38}  {mult:>9.1f}×  {peer:>24}  ${seg_ev:>13.1f}B")
        total_sop += seg_ev
    A(f"  {'─'*38}  {'─'*10}  {'─'*24}  {'─'*14}")
    A(f"  {'TOTAL ENTERPRISE VALUE':<38}  {'':>10}  {'':>24}  ${total_sop:>13.1f}B")
    A(f"  {'Less: Net Debt':<38}  {'':>10}  {'':>24}  -${NET_DEBT_B:>13.1f}B")
    A(f"  {'EQUITY VALUE':<38}  {'':>10}  {'':>24}  ${total_sop-NET_DEBT_B:>13.1f}B")
    shares_b = SHARES_OUT_M / 1000
    A(f"  {'Per share ({:.1f}B shares)'.format(shares_b):<38}  {'':>10}  {'':>24}  ${(total_sop-NET_DEBT_B)/shares_b:>13.2f}")
    A("")
    A(f"  Current price ${CURRENT_PRICE:.2f} vs SOP intrinsic ${(total_sop-NET_DEBT_B)/shares_b:.2f}")
    A(f"  → SOP implies {((total_sop-NET_DEBT_B)/shares_b/CURRENT_PRICE-1)*100:.1f}% upside at conservative peer multiples")
    A("")

    # ── SIX PROXY SIGNALS ────────────────────────────────────────────────────
    A("─" * 76)
    A("  SIX PROXY SIGNALS  (BEAR=1 · BASE=2 · BULL=3 · XBULL=4)")
    A("─" * 76)
    for name, val, wt, desc in PROXY_SIGNALS:
        bar = "●" * int(val) + "○" * (4 - int(val))
        label = {1: "BEAR", 2: "BASE", 3: "BULL", 4: "XBULL"}.get(int(val), "?")
        A(f"  [{bar}] {label:<6}  wt={wt:.2f}  {name}")
        A(f"          {desc}")
        A("")
    A(f"  Composite  : {PROXY_COMPOSITE:.2f}  |  ADJ: {ADJ_COMPOSITE:.2f}  |  Market: {MARKET_COMPOSITE:.2f}")
    A(f"  SCA Adjust : {SCA_NET:+.3f}  (infrastructure moat + parks offset by broadband competition)")
    A("")

    # ── STRUCTURAL COMPETITIVE ADVANTAGE ─────────────────────────────────────
    A("─" * 76)
    A("  STRUCTURAL COMPETITIVE ADVANTAGE (SCA)")
    A("─" * 76)
    for direction, desc, score, weight in SCA_FACTORS:
        A(f"  [{direction}] {desc}")
        A(f"      Score: {score:+.1f}  Weight: {weight:.2f}  Contribution: {score*weight:+.3f}")
        A("")
    A(f"  Net SCA Score : {SCA_NET:+.3f}")
    A(f"  Interpretation: Moderately positive. Broadband infrastructure + theme parks IP")
    A(f"  are durable moats; competition risk is real but overstated by the market.")
    A("")

    # ── BEAR CASE ─────────────────────────────────────────────────────────────
    A("─" * 76)
    A("  BEAR CASE  (price target: $20 / composite signal: 1.25 / weight: "
      f"{weights['BEAR']*100:.0f}%)")
    A("─" * 76)
    A("  Scenario: Broadband sub losses accelerate to 1M+ per quarter as AT&T Fiber")
    A("  expands to 50M+ homes and T-Mobile FWA adds 2M subs/quarter. Price competition")
    A("  drives ARPU below $70. Peacock profitability delayed to 2028 as sports rights")
    A("  costs escalate. Sky Europe faces Premier League rights renewal at 50% premium.")
    A("  Epic Universe underperforms due to macro/discretionary spending pullback.")
    A("")
    A("  In this world, EPS falls from $4.14 to ~$2.50. Leverage ticks up from 2.3×")
    A("  to 3.5×+ on declining EBITDA. Dividend risk emerges ($1.32/yr = $4.8B/yr).")
    A("  Stock at $2.50 × 8× distress P/E = $20.")
    A("")
    A("  BEAR NOTE: Even at $20 the stock still yields 6.6% and has $15B+ FCF.")
    A("  The REAL bear case requires dividend cut AND leverage spiral — possible")
    A("  but would require 2008-scale demand collapse, not just normal competition.")
    A("")

    # ── EPP ───────────────────────────────────────────────────────────────────
    A("─" * 76)
    A("  EPP — EARNINGS POWER PRICE (FLOOR ANALYSIS)")
    A("─" * 76)
    A(f"  Trough adj EPS (FY2026E conservative) : ${EPS_TROUGH:.2f}")
    A(f"  Min-Viable Trough P/E                 : {PE_TROUGH}×  (leveraged media distress floor)")
    A(f"  EPP                                   : ${EPP:.2f}  (= ${EPS_TROUGH} × {PE_TROUGH}×)")
    A(f"  Current Price                         : ${CURRENT_PRICE:.2f}")
    A(f"  EPP Gap                               : {EPP_GAP_PCT:.1f}%  ← PRICE IS BELOW FLOOR")
    A("")
    A("  INTERPRETATION: A negative EPP gap is rare and typically short-lived.")
    A("  It means the market is pricing in EPS deterioration to the level where")
    A("  the stock is already at distress valuation. But Comcast's FCF ($15B+/yr)")
    A("  and dividend ($1.32/yr × 3.6B shares = $4.8B/yr, 32% of FCF) are NOT")
    A("  consistent with distress. The gap between earnings ($4.14E adj EPS)")
    A("  and stock price ($29.59 = 7.1× P/E) is the opportunity.")
    A("")
    A("  HISTORICAL CONTEXT: Charter (CHTR) traded at 7-8× EV/EBITDA for years")
    A("  before re-rating to 10×. AT&T troughed at 8× in 2023. Comcast at 7.1×")
    A("  adj EPS is pricing in a structural deterioration that hasn't materialized.")
    A("")

    # ── CONSERVATIVE GROWTH CHECK ─────────────────────────────────────────────
    A("─" * 76)
    A("  CONSERVATIVE GROWTH CHECK  (2-year floor scenario)")
    A("─" * 76)
    A(f"  EPS (FY2027E conservative) : ${CONSERVATIVE_EPS:.2f}  (below consensus ~$4.30)")
    A(f"  Applied P/E (trough)       : {CONSERVATIVE_PE}×  (same stressed multiple)")
    A(f"  Price target (conservative): ${CONSERVATIVE_PRICE:.2f}")
    A(f"  2yr cumulative dividend    : ${CONSERVATIVE_DIV_2YR:.2f}  ($1.32 × 2yr)")
    A(f"  Conservative total return  : +{CONSERVATIVE_RETURN:.1f}%  (+{CONSERVATIVE_RETURN/2:.1f}%/yr)")
    A("")
    A("  KEY INSIGHT: Even at trough P/E on below-consensus EPS, the CONSERVATIVE")
    A("  return is +30.6% over 2 years. This is the power of buying below EPP.")
    A("  The dividend alone covers 4.7%/yr while you wait for the re-rating.")
    A("")

    # ── VOLATILITY & TECHNICALS ───────────────────────────────────────────────
    A("─" * 76)
    A("  VOLATILITY & TECHNICAL CONTEXT")
    A("─" * 76)
    range_pct = (VOL_52W_HIGH - VOL_52W_LOW) / VOL_52W_LOW * 100
    vs_low    = (CURRENT_PRICE - VOL_52W_LOW) / VOL_52W_LOW * 100
    vs_high   = (CURRENT_PRICE - VOL_52W_HIGH) / VOL_52W_HIGH * 100
    A(f"  52-Week Range : ${VOL_52W_LOW} – ${VOL_52W_HIGH}  ({range_pct:.1f}% spread)")
    A(f"  vs 52W Low    : +{vs_low:.1f}%")
    A(f"  vs 52W High   : {vs_high:.1f}%")
    A(f"  Position in range: {(CURRENT_PRICE-VOL_52W_LOW)/(VOL_52W_HIGH-VOL_52W_LOW)*100:.0f}% of range")
    A("")
    A("  CMCSA hit $24.35 (52W low) in mid-2025 at peak broadband loss fear. The")
    A("  partial recovery to $29.59 coincides with Q1 2026 broadband improvement.")
    A("  Stock remains 14.7% below 52W high — held back by ARPU pressure narrative.")
    A("  Re-rating catalysts: Peacock profitability (Q2 2026), broadband adds")
    A("  turning positive (H2 2026?), Epic Universe H2 earnings call data.")
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
    A(f"  Bear Target  : ${BEAR_TARGET:>6.2f}  (EPS $2.50 × 8× distress = $20)")
    A(f"  Bull Target  : ${BULL_TARGET:>6.2f}  (EPS $4.50 × 12× re-rate = $54)")
    A(f"  Current Price: ${CURRENT_PRICE:>6.2f}")
    A(f"  Downside     : {DOWNSIDE_PCT:.1f}%  (${CURRENT_PRICE:.2f} → ${BEAR_TARGET:.2f})")
    A(f"  Upside       : {UPSIDE_PCT:.1f}%  (${CURRENT_PRICE:.2f} → ${BULL_TARGET:.2f})")
    A(f"  Ratio B      : {RATIO_B:.2f}×  =  {DOWNSIDE_PCT:.1f}% / {UPSIDE_PCT:.1f}%")
    A("")
    A("  SIGNAL THRESHOLDS:")
    A(f"  ◉ BUY        Ratio B < 0.75×   Floor gap dominated by upside  ← CMCSA at {RATIO_B:.2f}×")
    A("  ◎ ACCUMULATE Ratio B 0.75–1.10× Balanced; edge to upside")
    A("  ◐ WATCHLIST  Ratio B 1.10–1.75× Floor gap exceeds EPS upside")
    A("  ✕ AVOID      Ratio B > 1.75×   Growth fully priced in")
    A("")

    # ── FINAL SIGNAL ──────────────────────────────────────────────────────────
    A("═" * 76)
    A(f"  FINAL SIGNAL  :  {SIGNAL}")
    A(f"  RATIO B       :  {RATIO_B:.2f}×  ({DOWNSIDE_PCT:.1f}% downside / {UPSIDE_PCT:.1f}% upside)")
    A(f"  EPP GAP       :  {EPP_GAP_PCT:.1f}%  ← NEGATIVE: trading BELOW earnings power floor")
    A(f"  ADJ vs MARKET :  {ADJ_VS_MARKET:+.2f}  →  SIGNIFICANTLY UNDERVALUED")
    A(f"  COMPOSITE     :  {ADJ_COMPOSITE:.2f} adjusted  |  {MARKET_COMPOSITE:.2f} implied by market")
    A(f"  2yr EV        :  ${ev:.2f}  ({(ev/CURRENT_PRICE-1)*100:+.1f}% total return incl div)")
    A(f"  CONSERV.      :  +{CONSERVATIVE_RETURN:.1f}% / +{CONSERVATIVE_RETURN/2:.1f}%/yr at trough {CONSERVATIVE_PE}× P/E")
    A("")
    A("  INVESTMENT THESIS:")
    A("  Comcast at $29.59 is a FCF machine the market has misclassified as a")
    A("  declining cable company. The narrative is wrong. Here's what's actually")
    A("  happening:")
    A("")
    A("  ① BROADBAND LOSSES PEAKED: Q1 2026 losses narrowed to 65K — the best")
    A("    quarterly result since Q4 2020, -117K YoY improvement. DOCSIS 4.0")
    A("    maintains speed advantage vs fiber for years. Xfinity Mobile bundle")
    A("    (9.3M lines) reduces churn structurally.")
    A("")
    A("  ② EPIC UNIVERSE IS OUTPERFORMING: Parks EBITDA +23% in Q2 2025, +24%")
    A("    revenue in Q1 2026. UK park announced for 2031. The parks segment")
    A("    alone is worth $40-50B on a standalone basis.")
    A("")
    A("  ③ PEACOCK PROFITABILITY IS IMMINENT: 46M paid subs, $2B+ revenue/qtr.")
    A("    Q2 2026 profitability guided by management. NFL + NBA + Olympics make")
    A("    this a durable sports-anchored streaming platform, not an experiment.")
    A("")
    A("  ④ $15B FCF AT 7× P/E: Comcast returned $11.7B to shareholders in 2025")
    A("    ($6.8B buybacks + $4.9B dividends). Buying back stock at 7× earnings")
    A("    is extremely high IRR. Each 1% of shares retired adds ~$0.04/EPS.")
    A("")
    A("  ⑤ BELOW EPP: Stock at $29.59 is BELOW the earnings floor ($34.20).")
    A("    This creates a 'free option' — the downside floor is BELOW current")
    A("    price only in a severe deterioration scenario.")
    A("")
    A("  BUY with 4.7% dividend yield floor. Catalyst: Peacock Q2 profitability,")
    A("  broadband net adds turn positive, Epic Universe full-capacity reporting.")
    A("")
    A("  RISKS TO MONITOR:")
    A("  • Broadband losses re-accelerate above 200K/qtr in H2 2026")
    A("  • ARPU decline steeper than guided (competitive pricing pressure)")
    A("  • Peacock profitability delayed (NBA rights amortization schedule)")
    A("  • Sky Europe FX headwinds + Premier League rights renewal risk")
    A("  • Net debt $85B at risk if EBITDA declines meaningfully (leverage ratio)")
    A("  • Macro discretionary pullback hurting theme park attendance")
    A("═" * 76)

    return "\n".join(report)


PART2 = run_model()

SUMMARY = (
    f"{SIGNAL}  —  Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT:.1f}% downside / {UPSIDE_PCT:.1f}% upside). "
    f"RARE SIGNAL: stock trades BELOW EPP floor (${EPP:.0f}; gap {EPP_GAP_PCT:.1f}%). "
    f"FCF machine misread as secular-decline cable company: $15B+ FCF/yr at 7.1× adj EPS. "
    f"Versant cable networks spun off Jan 2, 2026 (CNBC/MSNBC/USA/Syfy/E!/Bravo → VSNT). "
    f"Broadband: 31.255M subs; Q1 2026 losses narrowed to 65K (best since Q4 2020, -117K YoY). "
    f"Xfinity Mobile: 9.3M lines (+1.5M record in 2025); 15% penetration = 85% runway. "
    f"Epic Universe (May 2025): parks revenue +19% Q2, +24% Q1 2026; EBITDA first $1B+ quarter. "
    f"Peacock: 46M paid subs; $2B+ quarterly revenue; Q2 2026 profitability guided. "
    f"FY2025 capital return $11.7B ($6.8B buybacks + $4.9B dividend). Dividend $1.32/yr (4.7% yield). "
    f"Net debt $85B (2.33× EBITDA). SOP intrinsic ~$52/share at conservative peer multiples. "
    f"Conservative 2yr: EPS $4.00 × 9× trough P/E + $2.64 div = $38.64 → +{CONSERVATIVE_RETURN:.1f}%. "
    f"Bear $20 (broadband collapse) · Base $38 · Bull $54 · XBull $70. BUY; 4.7% yield floor."
)

if __name__ == "__main__":
    print(run_model())
    print(f"\nSUMMARY: {SUMMARY}")
    print(f"\nSIGNAL: {SIGNAL} | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:.1f}%")
