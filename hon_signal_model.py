"""
Honeywell International Inc. (NASDAQ: HON)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.98×  |  EPP Gap: +115.0%

A DIVERSIFIED INDUSTRIAL CONGLOMERATE EXECUTING A STRUCTURAL TRANSFORMATION —
VALUE UNLOCK IN PROGRESS AS SEPARATION INTO PURE-PLAY LEADERS ADVANCES
Trading at $218.00 (52-week range $176-243, roughly a third up its range — a stock
that has lagged the broader industrials re-rating as investors have applied a persistent
conglomerate discount while awaiting the execution of Honeywell's announced structural
transformation: separating its portfolio into focused pure-play leaders in Aerospace
Technologies, Industrial/Building Automation, and Advanced Materials) on the back of
four genuinely high-quality business franchises housed under one roof. The core
aerospace portfolio (avionics, propulsion controls, defense/space, business aviation)
is a top-three player in most categories it competes in. Process automation (Experion
DCS, Sensing & IoT, UOP refining/petrochemical technology licensing) is the backbone
of the global process industry's control and optimization infrastructure. Building
automation (fire safety, security, building management systems) is a recurring-revenue
compounder largely immune to the economic cycle. And the Advanced Materials segment
— notably the Solstice family of low-global-warming-potential refrigerants and
propellants, which are the mandated replacements for high-GWP legacy HFC refrigerants
under global regulatory phase-out schedules — is arguably the most undervalued piece,
an effective structural monopoly on the regulatory-driven replacement cycle.

The honest tension: Honeywell has been a conglomerate for so long — and has guided,
retracted, and re-guided portfolio-simplification plans so many times — that investors
have learned to discount announced transformation timelines significantly. The separation
plan announced in late 2024 is the most credible and detailed yet, but execution risk
on multi-entity corporate separations is real (dis-synergies, stranded-cost unwinding,
tax complexity, management bandwidth), and in the meantime the stock trades at a blended
multiple that discounts all four businesses relative to what each would command
individually as a pure-play.

Conviction: MODERATE-HIGH on the underlying franchise quality (each of the four
business segments would trade at premium multiples as a standalone — the conglomerate
discount is a temporary valuation artifact, not a reflection of business quality);
MODERATE on the execution of the transformation itself — the cases for and against
timely, value-creative separation are evenly balanced — which is precisely what
produces a Ratio B close to 1.0×, a balanced setup for a name that rewards patience.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "HON"
COMPANY         = "Honeywell International Inc."
SECTOR          = "Diversified Industrials · Aerospace Technologies / Process & Building Automation / Advanced Materials · NASDAQ: HON"
SECTOR_GROUP    = "Industrials"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 218.00   # June 2026 — conglomerate discount vs. pure-play peers
ANNUAL_DIV      = 4.52     # Quarterly $1.13; 41 consecutive years of dividend increases
SHARES_OUT_B    = 0.645    # Billion shares (declining via active buyback program)
FW52_HIGH       = 243.00   # Recent ceiling as separation execution updates lift sentiment
FW52_LOW        = 176.00   # Trough on macro uncertainty + conglomerate-discount widening

# ── FY2025 REPORTED / FY2026 ESTIMATES ──────────────────────────────────────
# HON FY2025 actuals (pro-forma, including businesses under separation):
#   Net revenue: ~$38.4B (+5% organic)
#   Adjusted EPS: ~$10.15 (+8% YoY)
#   FCF: ~$5.1B
#   Total order backlog: ~$35B (aerospace + long-cycle automation)
# FY2026 consensus (June 2026):
#   Adjusted EPS: ~$11.10-11.50
#   FCF: ~$5.5-6.0B
# Portfolio transformation timeline:
#   Advanced Materials spin-off: completed Q1 2026 (listed as HON-AM / provisional ticker)
#     — Solstice HFO refrigerants/propellants, fluorine products, specialty chemicals
#   Automation separation: announced target ~H2 2026 / H1 2027
#     — Industrial Automation (Process Solutions, Sensing & IoT) and Building Automation
#     — remain to be structured as a separate entity from Aerospace Technologies
# Aerospace Technologies (~$15.5B revenue): avionics (cockpit displays, navigation, TCAS),
#   propulsion control (engine controls, APU), defense/space (satellites, electronic warfare),
#   business aviation (Honeywell Engines, Garrett Motion linkage dissolved post-spin)
# Process & Building Automation (~$16B combined): Experion distributed control system,
#   Sensing & IoT (pressure/temp/flow instruments), fire safety, building management
# Advanced Materials (~$4.8B at spin, now separate): Solstice HFO (dominant, near-sole-
#   source on regulatory-mandated HFC replacement cycle globally), specialty chemicals
# Balance sheet: net debt ~$7.5B (manageable for the scale; declining post-AM spin proceeds)
# Dividend: $4.52/yr; 41-year streak; commitment to maintain through separation
# Buyback: ~$2-3B/year authorization

# ── SCENARIO ARCHITECTURE ────────────────────────────────────────────────────
#
# BEAR = $162 | "Separation stumbles, conglomerate discount widens, cycle turns"
#   • Automation separation encounters significant dis-synergies, stranded-cost
#     overruns, or regulatory hurdles that delay and dilute the value unlock
#   • Aerospace cycle weakens: business aviation demand contracts, defense program
#     delays, commercial aerospace softens as air travel demand disappoints
#   • Process automation bookings soften with oil/gas/chemical capex cycles;
#     building automation faces rate-sensitivity headwinds in commercial construction
#   • Conglomerate discount widens further as investors lose patience with the
#     timeline; blended multiple compresses toward ~14-15x trough EPS → $162
#
# BASE = $218 | "Separation executes, franchises compound steadily"
#   • Automation separation proceeds roughly on schedule (H2 2026/H1 2027);
#     post-separation Aerospace Technologies pure-play begins trading at ~22-24x
#   • Honeywell's four core businesses deliver their guided ~5-7% organic growth;
#     aerospace backlog converts steadily, automation margins hold at ~21-23%
#   • Blended multiple stays at ~19-20x as investors await separation completion;
#     stock roughly fairly valued at $218
#
# BULL = $275 | "Separations unlock full value, pure-play re-ratings materialize"
#   • Automation separation completes faster than expected; Aerospace Technologies
#     trades at 25-27x (in line with GE Aerospace premium peers) once separated
#   • Advanced Materials (Solstice) re-rates to specialty-chemicals premium as
#     investors model the near-sole-source regulatory replacement cycle
#   • Process/Building Automation trades at high-teens/20x as a focused
#     software-and-services industrial compounder — premium to blended HON
#   • Combined entity-level value at $275+ within 2-3 years of full separation
#
# XBULL = $320 | "Best-case: elite compounder status for all three pure-plays"
#   • Aerospace Technologies re-rates to GE/RTX premium tier (27-30x)
#   • Automation separation beats all synergy and margin targets; acquired by a
#     strategic or PE buyer at a premium to market after separation
#   • Solstice Advanced Materials proves to be the "Intel Inside" of the global
#     HFC replacement cycle — terminal value far above current modeling
#   • Full sum-of-parts value realized at $320 in best-case scenario
#
SCENARIOS = {
    "BEAR":  162.0,
    "BASE":  218.0,
    "BULL":  275.0,
    "XBULL": 320.0,
}

BEAR  = SCENARIOS["BEAR"]
BASE  = SCENARIOS["BASE"]
BULL  = SCENARIOS["BULL"]
XBULL = SCENARIOS["XBULL"]

# ── EARNINGS POWER PRICE (EPP) ────────────────────────────────────────────────
# Trough EPS = $7.80 (deep recession: all four segments contract simultaneously,
#   separation costs peak, dis-synergies materialize, commercial aerospace weakens)
# Trough PE  = 13.0× — cyclical floor for a diversified industrial in a deep recession
# EPP = $101.40 — stock at $218 is +115.0% above this floor; the recurring-revenue
#   mix (aerospace aftermarket + automation services + building automation) provides
#   genuine earnings resilience that limits the magnitude of any trough scenario
EPS_TROUGH      = 7.80
PE_TROUGH       = 13.0
EPP             = EPS_TROUGH * PE_TROUGH   # $101.40

# ── SCA (STRUCTURAL COMPETITIVE ADVANTAGE) FACTORS ───────────────────────────
SCA_FACTORS = {
    # (+) AEROSPACE AVIONICS AND SYSTEMS FRANCHISE
    #   — top-3 in cockpit avionics, flight management, navigation, and propulsion
    #   controls on virtually every business jet and a significant share of commercial;
    #   certification barriers to entry are among the highest in all of industrials
    "aerospace_avionics_and_defense_systems_franchise":          +0.16,

    # (+) PROCESS AUTOMATION INSTALLED BASE AND EXPERION ECOSYSTEM
    #   — Experion DCS (distributed control system) is installed at thousands of
    #   refineries, petrochemical plants, and industrial facilities worldwide;
    #   switching costs are extremely high (10+ year replacement cycles, safety
    #   certification requirements, operator re-training); a genuine "sticky" annuity
    "process_automation_installed_base_and_switching_costs":     +0.15,

    # (+) SOLSTICE HFO NEAR-SOLE-SOURCE REGULATORY REPLACEMENT CYCLE
    #   — Solstice (HFO refrigerants/propellants) is the dominant product in the
    #   regulatory-mandated replacement of high-GWP HFC refrigerants globally;
    #   Honeywell and Chemours are the only two scaled HFO producers; regulatory
    #   phase-out schedules in the EU (F-Gas Regulation) and US (AIM Act) create
    #   a multi-decade, structurally-growing demand curve that doesn't depend on
    #   economic cycles — driven purely by regulation
    "solstice_hfo_near_sole_source_regulatory_replacement":      +0.14,

    # (+) BUILDING AUTOMATION RECURRING-REVENUE PLATFORM
    #   — fire safety, security, and building management systems are largely
    #   maintenance/subscription-based; long-duration, sticky customer relationships
    #   with hospitals, airports, data centers, and commercial real estate that
    #   generate predictable, low-volatility recurring cash flows
    "building_automation_recurring_revenue_and_stickiness":      +0.12,

    # (-) CONGLOMERATE STRUCTURE DISCOUNT AND TRANSFORMATION EXECUTION RISK
    #   — the blended multiple persistently discounts each segment below what it
    #   would command as a standalone pure-play; and corporate separation is
    #   genuinely complex — dis-synergies, stranded costs, tax structuring, and
    #   management bandwidth risks are real and historically have been underestimated
    "conglomerate_discount_and_separation_execution_risk":       -0.15,

    # (-) BALANCE SHEET AND CAPITAL-ALLOCATION OPTIONALITY CONSTRAINTS
    #   — net debt ~$7.5B post-AM spin is manageable but limits M&A firepower;
    #   separation costs (legal, advisory, TSA, stranded costs) will consume FCF
    #   for 2-3 years, reducing capital-return flexibility vs. simpler peers
    "net_debt_and_separation_cost_cash_flow_constraints":        -0.11,

    # (-) CYCLICAL EXPOSURE ACROSS MULTIPLE SECTORS SIMULTANEOUSLY
    #   — Honeywell's four segments span aerospace, oil & gas, chemicals,
    #   commercial construction, and general industrial — in a broad macro downturn,
    #   all four can soften simultaneously, with limited natural hedging (unlike
    #   a pure-play that can be explicitly long or short a single cycle)
    "multi_sector_cyclical_exposure_and_limited_natural_hedging": -0.09,
}

SCA_NET   = sum(SCA_FACTORS.values())
SCA_SCALE = 0.45

# ── SIX PROXY SIGNALS ─────────────────────────────────────────────────────────
SIGNALS = {
    # 3.5 — The separation thesis is credible and advancing: Advanced Materials (Solstice)
    #   already spun off, Automation separation announced — each pure-play should trade
    #   above the current blended conglomerate multiple once separated; sum-of-parts
    #   math is clearly above current price
    "portfolio_separation_and_sum_of_parts_value_unlock":
        {"score": 3.5, "weight": 0.19},

    # 3.0 — Aerospace Technologies is a genuine top-3 franchise: avionics (cockpit
    #   displays, FMS, TCAS), propulsion controls, defense/space, and business aviation
    #   systems — all with high certification barriers, multi-year program contracts,
    #   and a growing aftermarket annuity as the installed fleet ages
    "aerospace_technologies_franchise_and_aftermarket_annuity":
        {"score": 3.0, "weight": 0.18},

    # 3.0 — Process automation (Experion DCS) + Sensing & IoT + Building Automation
    #   collectively generate ~60% recurring/aftermarket revenue with high switching
    #   costs; steady 5-7% organic growth track record across cycles; software content
    #   is increasing (Forge cloud platform, connected building solutions)
    "process_and_building_automation_recurring_revenue_quality":
        {"score": 3.0, "weight": 0.17},

    # 3.0 — 41 consecutive years of dividend increases (Dividend Aristocrat), FCF
    #   conversion ratio >90%, investment-grade balance sheet, and active buyback
    #   program — capital discipline that is genuinely above-average for a conglomerate
    "dividend_track_record_and_capital_discipline":
        {"score": 3.0, "weight": 0.16},

    # 2.0 — Separation execution is the dominant uncertainty: timeline has slipped
    #   before, dis-synergy estimates are always understated in announcements, and
    #   the blended-multiple discount persists until investors see standalone trading
    #   prices for each entity — the "show me" factor is real
    "separation_execution_timeline_and_dis_synergy_risk":
        {"score": 2.0, "weight": 0.16},

    # 2.5 — At ~19-20x forward, HON is not obviously cheap for a conglomerate in
    #   transformation — but it's not expensive either; the case is "transformation
    #   unlocks value that the blended multiple doesn't yet reflect," not "cheap
    #   on current-year earnings" — requires patience and a 2-3 year horizon
    "valuation_relative_to_peer_industrials_and_transformation_premium":
        {"score": 2.5, "weight": 0.14},
}

# ── SOFTMAX SCENARIO WEIGHTER ─────────────────────────────────────────────────
def softmax_weights(composite, centers=None, T=0.60):
    if centers is None:
        centers = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
    raw = {k: math.exp(-((composite - v) ** 2) / (2 * T ** 2))
           for k, v in centers.items()}
    total = sum(raw.values())
    return {k: v / total for k, v in raw.items()}

# ── COMPOSITE SCORE CALCULATION ───────────────────────────────────────────────
PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS.values())
ADJ_COMPOSITE   = PROXY_COMPOSITE + SCA_SCALE * SCA_NET * 0.5

TARGET_EV = CURRENT_PRICE * (1.15 ** 2)

def ev_from_composite(c):
    w = softmax_weights(c)
    return (w["BEAR"] * BEAR + w["BASE"] * BASE
            + w["BULL"] * BULL + w["XBULL"] * XBULL)

lo, hi = 1.0, 4.0
for _ in range(60):
    mid = (lo + hi) / 2
    if ev_from_composite(mid) < TARGET_EV:
        lo = mid
    else:
        hi = mid
MARKET_COMPOSITE = (lo + hi) / 2
MARKET_WEIGHTS   = softmax_weights(MARKET_COMPOSITE)
EV_MODEL         = ev_from_composite(MARKET_COMPOSITE)

# ── SIGNAL DETERMINATION ──────────────────────────────────────────────────────
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

EPP_GAP_PCT     = (CURRENT_PRICE - EPP) / EPP * 100
PE_CONSERVATIVE = 19.0
EPS_FY2026E     = 11.10
CONSERVATIVE_PRICE = EPS_FY2026E * PE_CONSERVATIVE + 2 * ANNUAL_DIV
RETURN_2YR = (CONSERVATIVE_PRICE - CURRENT_PRICE) / CURRENT_PRICE * 100
RETURN_ANN  = ((1 + RETURN_2YR / 100) ** 0.5 - 1) * 100

# ── REPORT ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    SEP = "━" * 78
    sep = "─" * 78

    print(SEP)
    print(f"  HONEYWELL INTERNATIONAL INC. (NASDAQ: HON) — BOTTOM-UP RISK/REWARD SIGNAL")
    print(f"  {ANALYSIS_DATE}  |  Price: ${CURRENT_PRICE:.2f}  |  52-wk: ${FW52_LOW:.0f}–${FW52_HIGH:.0f}")
    print(SEP)

    print(f"""
  COMPANY:  {COMPANY}
  SECTOR:   {SECTOR}
""")

    print(sep)
    print("  FY2025 FINANCIALS & FY2026 CONSENSUS")
    print(sep)
    print(f"""
  Net revenue (FY2025A):        ~$38.4B         (+5% organic)
  Adjusted EPS (FY2025A):       ~$10.15/share   (+8% YoY)
  FCF (FY2025A):                ~$5.1B          (>90% FCF conversion; strong quality)
  Total backlog:                ~$35B           (aerospace long-cycle + automation orders)
  Net debt (post-AM spin):      ~$7.5B          (investment-grade; Baa1/BBB+ equivalent)
  Dividend:                     ${ANNUAL_DIV:.2f}/share/yr  (41 consecutive annual increases — Dividend Aristocrat)
  Shares outstanding:           ~{SHARES_OUT_B:.3f}B         (declining via $2-3B/yr buyback)

  FY2026 Consensus (adj. EPS):  ~$11.10-11.50   (organic growth + separation tailwind)
  FY2026 Consensus (FCF):       ~$5.5-6.0B      (improving as separation costs ramp)

  Portfolio transformation status (June 2026):
    Advanced Materials spin:    Completed Q1 2026 — Solstice HFO, fluorine products, specialty
    Automation separation:      Announced H2 2026 / H1 2027 target; Industrial + Building Automation
    Aerospace Technologies:     Will remain as the "RemainCo" anchor after Automation separation

  Segment revenue breakdown (FY2025, pre-separation basis):
    Aerospace Technologies:     ~$15.5B         (~40%; avionics, propulsion, defense, biz-av)
    Industrial Automation:      ~$10.5B         (~27%; Experion DCS, Sensing & IoT, UOP)
    Building Automation:        ~$7.5B          (~20%; fire/security, BMS, facilities mgmt)
    Advanced Materials:         ~$4.8B          (~13%; Solstice HFO, fluorine, specialty chem)
""")

    print(sep)
    print("  SCENARIO NOTES")
    print(sep)
    print(f"""
  BEAR  ${BEAR:>6.1f}  Separation stumbles (dis-synergies, stranded costs, timeline slips);
               aerospace cycle weakens; automation bookings soften; blended multiple
               compresses to ~14-15x trough EPS as patience runs out.

  BASE  ${BASE:>6.1f}  Automation separation executes roughly on schedule; franchises compound
               at guided 5-7% organically; blended multiple holds ~19-20x; stock fairly
               valued during the execution window.

  BULL  ${BULL:>6.1f}  Separations unlock full sum-of-parts value; Aerospace Technologies re-rates
               toward GE/RTX peer multiple (25-27x standalone); Automation pure-play
               trades at 20-22x; Solstice re-rates to specialty-chemical premium.

  XBULL ${XBULL:>6.1f}  All three entities re-rate to elite-compounder tier; Automation acquired by
               strategic/PE buyer at premium; Solstice proves near-monopoly economics.
""")

    print(sep)
    print("  SEGMENT HIGHLIGHTS")
    print(sep)
    print(f"""
  Aerospace Technologies (~$15.5B, ~40% of revenue):
    • Avionics leadership: Primus cockpit systems, IntuVue radar, SmartPath ILS on
      thousands of commercial and business aircraft worldwide; primary cockpit displays
      on Airbus A220/A320, Boeing 737/777, and virtually every business jet category
    • Propulsion controls: engine FADEC and fuel management on GE/P&W/RR engines,
      APU (auxiliary power unit) in ~90%+ of commercial aircraft globally
    • Defense/Space: electronic warfare, ISR (intelligence/surveillance/recon), space
      products (satellite components, sensor systems); growing segment with F-35 content
    • Business Aviation: Honeywell engines (HTF7000/HTF7000L) in multiple platforms;
      avionics dominant across citation-class through large-cabin
    • Aftermarket (40-45% of segment): high-margin MRO, upgrades, and services
      generating recurring cash flow on the massive installed base

  Industrial Automation (~$10.5B, ~27%):
    • Experion PKS/ORION: the #2 DCS platform globally (behind Emerson DeltaV/DCS);
      installed in 70%+ of global refining and over half of LNG facilities worldwide;
      10+ year replacement cycles with near-zero voluntary churn
    • Sensing & IoT: 100M+ sensors shipped annually; pressure, temperature, flow,
      humidity sensors used in virtually every industrial, HVAC, and automotive application
    • UOP (Universal Oil Products): licensor of refining, petrochemical, and gas
      processing technologies; ~90% of world's clean fuels produced with UOP technology
      at some stage; pure-licensing/engineering-services model, highly capital-light

  Building Automation (~$7.5B, ~20%):
    • Fire safety: Notifier (fire detection/alarm); ~40% global market share in
      commercial and life-safety fire alarm systems; code-mandated inspection/servicing
    • Security: Galaxy, Pro-Watch access control; Vindicator (critical infrastructure)
    • Building Management Systems: EBI/WIN-PAK; integration platform for HVAC, lighting,
      access, fire across large commercial, healthcare, and government facilities

  Advanced Materials (spun off Q1 2026, now separate entity):
    • Solstice HFO (Hydrofluoroolefin): the dominant replacement refrigerant for HFCs
      being phased out under EU F-Gas Regulation (recast 2024) and US AIM Act;
      Honeywell and Chemours are the only two scaled producers — effective duopoly
      on a regulatory-mandated, multi-decade demand curve that only grows stronger
""")

    print(sep)
    print("  ANALYST CONSENSUS (JUNE 2026)")
    print(sep)
    print(f"""
  Coverage:    ~29 analysts
  Buy/Strong:  ~18 (62%)       Hold: ~9 (31%)       Sell: ~2 (7%)
  Price target: ~$238 consensus  (range: $195-275)
  Commentary:  strong consensus on the sum-of-parts value unlock thesis; debate is
               entirely around separation timeline and dis-synergy risk; most models
               see $250-270 as achievable within 24-36 months if separations execute;
               key watch: automation separation structure announcement and initial
               trading of spun-off entities
""")

    print(sep)
    print("  SIX PROXY SIGNALS")
    print(sep)
    for name, sig in SIGNALS.items():
        bar = "█" * int(sig["score"] * 5) + "░" * (20 - int(sig["score"] * 5))
        print(f"  {name[:50]:<50}  {sig['score']:.1f}/4  wt={sig['weight']:.2f}  [{bar}]")
    print(f"\n  PROXY_COMPOSITE = {PROXY_COMPOSITE:.3f}")

    print(f"\n{sep}")
    print("  SCA (STRUCTURAL COMPETITIVE ADVANTAGE) BREAKDOWN")
    print(sep)
    for name, val in SCA_FACTORS.items():
        sign = "+" if val > 0 else "−"
        bar = "█" * int(abs(val) * 60)
        print(f"  {sign}  {name[:54]:<54}  {val:+.2f}  [{bar}]")
    print(f"\n  SCA_NET = {SCA_NET:+.3f}   SCA_SCALE = {SCA_SCALE}")
    print(f"  ADJ_COMPOSITE = {ADJ_COMPOSITE:.3f}")

    print(f"\n{sep}")
    print("  COMPOSITE SCORES & SCENARIO WEIGHTS")
    print(sep)
    print(f"  PROXY_COMPOSITE  = {PROXY_COMPOSITE:.3f}")
    print(f"  ADJ_COMPOSITE    = {ADJ_COMPOSITE:.3f}")
    print(f"  MARKET_COMPOSITE = {MARKET_COMPOSITE:.3f}  (back-solved: EV = ${TARGET_EV:.2f})")
    print()
    for sc, w in MARKET_WEIGHTS.items():
        bar = "█" * int(w * 80)
        print(f"  {sc:<6} {SCENARIOS[sc]:>6.1f}  wt={w:.3f}  [{bar}]")

    print(f"\n{sep}")
    print("  SIGNAL DETERMINATION")
    print(sep)
    print(f"  EPP   = EPS_TROUGH ${EPS_TROUGH} × PE_TROUGH {PE_TROUGH}x = ${EPP:.2f}")
    print(f"  EPP Gap (current vs. EPP floor):                            {EPP_GAP_PCT:+.1f}%")
    print(f"  Downside to BEAR ${BEAR:.0f}:                                   -{DOWNSIDE_PCT:.1f}%")
    print(f"  Upside   to BULL ${BULL:.0f}:                                   +{UPSIDE_PCT:.1f}%")
    print(f"  Ratio B = {RATIO_B:.4f} → {SIGNAL_TEXT}")
    print(f"\n  SIGNAL:  {SIGNAL_TEXT}   Ratio B: {RATIO_B:.2f}×   EPP Gap: {EPP_GAP_PCT:+.1f}%")
    print(f"  EV(model): ${EV_MODEL:.2f}   Upside: +{UPSIDE_PCT:.1f}%   Downside: -{DOWNSIDE_PCT:.1f}%")

    print(f"\n{sep}")
    print("  CONSERVATIVE 2-YEAR RETURN (MULTIPLE-FLAT FLOOR CASE)")
    print(sep)
    print(f"  EPS_FY2026E:  ${EPS_FY2026E:.2f}  ×  PE_CONSERVATIVE: {PE_CONSERVATIVE:.1f}x  =  ${EPS_FY2026E * PE_CONSERVATIVE:.2f}")
    print(f"  + 2-year dividends:  2 × ${ANNUAL_DIV:.2f}  =  ${2 * ANNUAL_DIV:.2f}")
    print(f"  Conservative 2yr price target:  ${CONSERVATIVE_PRICE:.2f}")
    print(f"  2-year return:                                                      {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  Note: the floor case holds the multiple flat and assumes no value unlock from")
    print(f"  the separation — yet still produces a modest positive return. BULL/XBULL require")
    print(f"  the separation to unlock the sum-of-parts premium the market currently ignores.")

    print(f"\n{sep}")
    print("  WHY THIS IS AN ◎ ACCUMULATE, NOT A ◌ WATCHLIST OR ◉ BUY")
    print(sep)
    print("""
  Honeywell is, at its core, four genuinely excellent businesses — a top-3 aerospace
  avionics and systems franchise, a #2-globally installed-base DCS/automation platform
  with extreme switching costs, a recurring-revenue building-automation compounder, and
  what is effectively a near-sole-source on a regulatory-mandated HFO replacement cycle.
  The conglomerate structure has persistently discounted the aggregate value below what
  each business would command independently — and that's precisely the setup: Ratio B
  near 1.0× reflects a name where the underlying franchise quality and the sum-of-parts
  opportunity are clearly visible, but where the execution of the value unlock requires
  patience.

  WHAT THE MARKET ALREADY PRICES IN (at $218, ~1/3 up 52-wk range, ~19-20x forward):
  • Separation plan announced but unproven — investors are discounting the timeline
    vs. prior incomplete portfolio-simplification announcements
  • Organic growth continues at the guided 5-7% across the portfolio, with no
    meaningful acceleration or surprise in any single segment
  • Separation costs (advisory, legal, stranded-cost unwinding) consume FCF through
    2027, limiting capital-return flexibility vs. peers
  • Blended conglomerate multiple stays depressed until standalone pure-plays begin
    trading and their individual multiples are observed by the market

  WHAT COULD MAKE THIS MORE THAN FAIRLY PRICED (the ACCUMULATE case):
  1. Automation separation executes on (or ahead of) schedule — the market re-rates
     the RemainCo Aerospace Technologies at 25-27x (GE/RTX peer range) once free
     of the conglomerate discount; sum-of-parts math argues for $270-290 today
  2. Solstice HFO Advanced Materials (now separated) proves to be the "Intel Inside"
     of the global HFC replacement cycle — a durable near-monopoly on a regulatory
     tailwind that is insensitive to the economic cycle
  3. Aerospace Technologies aftermarket volume inflects as the post-COVID commercial
     fleet ages into its highest-maintenance years — a Honeywell-specific analog to
     the GE/Pratt services-annuity thesis
  4. UOP (process technology licensing) secures next-generation sustainable aviation
     fuel (SAF) and hydrogen processing contracts that re-rate the technology portfolio

  THE RISK (the honest read):
  • Separation execution is genuinely complex and historically underestimated by
    management teams — dis-synergies (shared IT, HR, legal, supply chain) take years
    to fully unwind; stranded cost estimates are always below the actual
  • The timeline has slipped before — Honeywell has discussed portfolio simplification
    for years; if the automation separation encounter regulatory or structural obstacles,
    the catalyst timeline extends and the patience required grows
  • A broad industrial recession hitting all four segments simultaneously — aerospace
    softening, automation bookings declining, construction slowing — removes the
    near-term earnings floor that the diversification provides

  WHAT MAKES THIS AN ACCUMULATE RATHER THAN MERELY A WATCHLIST:
  • Ratio B of 0.98× — nearly perfectly balanced risk/reward — for a business of this
    quality with a clear, credible value-unlock catalyst in progress is an attractive
    accumulation point; you're not overpaying for quality, and you're not waiting for
    a "more obvious" entry that may never come before the separation executes
  • The floor is well-defined: even in the bear case (separation stumbles), you own
    four genuinely good businesses at ~14-15x trough earnings — no permanent capital
    impairment scenario given the franchise quality, IG balance sheet, and 41-year
    dividend track record
  • The conservative 2-yr floor case (multiple flat, no separation premium) still
    produces a modest positive return — the dividend alone (~2.1% yield) provides a
    meaningful cushion while the transformation executes

  POSITION SIZING GUIDANCE:
  • ACCUMULATE — build a position steadily here, with patience for the 2-3 year
    separation timeline; add more aggressively on any pullback below $195-205
    (where Ratio B approaches BUY territory) that is driven by macro fear rather
    than any deterioration in the separation thesis or franchise quality
  • Watch for: (1) automation separation structure announcement — the key catalyst
    event; (2) quarterly backlog conversion in aerospace (the forward revenue visibility
    signal); (3) Solstice HFO demand commentary post-separation (the hidden-value signal);
    (4) any acceleration or delay to the automation separation timeline
""")

    print(SEP)
    print(f"""
SUMMARY: HON ◎ ACCUMULATE — Ratio B 0.98× (25.7% downside / 26.1% upside, roughly \
balanced). A DIVERSIFIED INDUSTRIAL CONGLOMERATE EXECUTING A STRUCTURAL \
TRANSFORMATION — VALUE UNLOCK IN PROGRESS: trading at $218.00 (52-wk range \
$176-243, roughly a third up the range — the persistent conglomerate discount \
meeting an actively-executing separation thesis) on four genuinely high-quality \
franchises: AEROSPACE TECHNOLOGIES (~$15.5B: top-3 avionics/navigation/propulsion- \
controls on virtually every business and commercial aircraft; 40-45% aftermarket mix); \
INDUSTRIAL AUTOMATION (~$10.5B: Experion DCS #2 globally, ~10-yr replacement cycles, \
UOP technology licensing in ~90% of global clean-fuels production); BUILDING AUTOMATION \
(~$7.5B: Notifier fire safety, EBI building management, code-mandated recurring \
inspection/service); ADVANCED MATERIALS (spun off Q1 2026: Solstice HFO near-sole- \
source on regulatory-mandated HFC replacement cycle globally). TRANSFORMATION: \
Advanced Materials separated Q1 2026; Industrial + Building Automation separation \
targeted H2 2026/H1 2027 — unlocking pure-play Aerospace Technologies RemainCo at \
25-27x (vs. blended ~19-20x today). Dividend Aristocrat: 41 consecutive increases, \
$4.52/yr, ~2.1% yield; FCF ~$5-6B. Consensus 'Buy' (~18 of 29 analysts), PT ~$238 \
(range $195-275). Conservative 2yr (no separation premium, multiple flat): EPS $11.10 \
x 19x + $9.04 div = $220.14 -> +1.0% — BULL/XBULL require separations to unlock \
the sum-of-parts premium. THE FOUR FRANCHISES ARE WORTH MORE APART THAN TOGETHER: \
accumulate steadily here, add on weakness toward $195-205. Bear $162 · Base $218 · \
Bull $275 · XBull $320."""
    )

    print(f"SIGNAL: {SIGNAL_TEXT} (diversified industrial conglomerate with four high-quality franchises — aerospace avionics/Experion DCS/building automation/Solstice HFO — executing a credible separation into pure-play leaders; conglomerate discount creates accumulation opportunity) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
