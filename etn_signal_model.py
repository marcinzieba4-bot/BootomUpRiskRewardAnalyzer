"""
Eaton Corporation plc (NYSE: ETN)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.89×  |  EPP Gap: +109.9%

THE ESSENTIAL INFRASTRUCTURE OF THE AI AND ENERGY-TRANSITION ERA —
A POWER MANAGEMENT FRANCHISE SITTING AT THE INTERSECTION OF EVERY MAJOR
SECULAR CAPEX CYCLE OF THE NEXT DECADE
Trading at $340.00 (52-week range $278-382, roughly a third up its range — the
stock has consolidated after a multi-year re-rating as investors assess how much of
the data-center and grid-modernization supercycle is already in the price) on the
back of what is structurally one of the most advantaged positions in the entire
industrial landscape: Eaton is the #1 or #2 supplier of electrical switchgear,
circuit breakers, power distribution units (PDUs), uninterruptible power supplies
(UPS), and busway systems — the unglamorous but absolutely mission-critical
infrastructure that every data center, every semiconductor fab, every EV factory,
and every grid-modernization project requires before a single server rack is
powered on, a single wafer is processed, or a single electron flows from a
renewable generator to the transmission network.

The structural convergence driving Eaton: five independent secular demand drivers
are pulling on the same electrical equipment capacity simultaneously — AI/cloud data
center construction (hyperscalers committed to $100B+ annual capex each through 2028),
grid modernization (aging US/European transmission and distribution infrastructure
being upgraded for EV charging, distributed generation, and resilience), US
manufacturing reshoring (CHIPS Act semiconductor fabs, IRA clean-energy factories,
USMCA-driven assembly plants — all requiring extensive power distribution buildouts),
the energy transition (wind/solar interconnect equipment, battery energy storage
systems, grid-scale UPS), and commercial and industrial building electrification.
Unlike a single-thesis trade, Eaton would need most of these five independent demand
drivers to simultaneously reverse before the structural growth story breaks.

The honest tension: at ~25x forward EPS, Eaton is already priced for above-average
execution. The data center capex cycle is the single largest driver of near-term
earnings upside — and it is inherently lumpy, concentrated in a handful of
hyperscaler customers, and subject to sudden deferral if AI spending priorities shift.
The premium valuation also limits the return if even one or two of the five secular
drivers disappoints, as investors at this multiple have low tolerance for even modest
execution shortfalls.

Conviction: HIGH on the structural positioning (the electrical infrastructure
capacity shortage is genuine, multi-year, and structural — Eaton has been citing
multi-year backlogs since 2023 and lead times remain extended through 2026-2027);
MODERATE on the near-term risk/reward at $340 given the multiple already embeds
most of the near-term data-center demand visibility. Ratio B of 0.88× reflects a
name where the bull case is clearly achievable but is not being offered at a discount.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "ETN"
COMPANY         = "Eaton Corporation plc"
SECTOR          = "Electrical Equipment & Power Management · Switchgear / UPS / PDU / Busway / Grid Infrastructure · NYSE: ETN"
SECTOR_GROUP    = "Industrials"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 340.00   # June 2026 — consolidated after multi-year re-rating
ANNUAL_DIV      = 3.76     # Quarterly $0.94; growing ~9-10%/yr; ~1.1% yield at $340
SHARES_OUT_B    = 0.400    # Billion shares (buybacks ongoing; ~400M shares)
FW52_HIGH       = 382.00   # Recent high; set during peak AI-capex-cycle enthusiasm
FW52_LOW        = 278.00   # Trough; macro deceleration fears and valuation debate

# ── FY2025 REPORTED / FY2026 ESTIMATES ──────────────────────────────────────
# ETN FY2025 actuals:
#   Revenue: ~$25.8B (+9% organic; data center + grid + reshoring all contributing)
#   Adjusted EPS: ~$11.85 (+14% YoY; operating leverage + price/cost improvement)
#   FCF: ~$3.9B (>100% conversion; clean cash generation)
#   Segment operating margins: Electrical Americas ~25%, Electrical Global ~18%
#   Order backlog: ~$14B (record; data center and utility orders dominant)
# FY2026 estimates (June 2026):
#   Adjusted EPS: ~$13.50 (+14% YoY; continued backlog conversion + pricing)
#   FCF: ~$4.5-5.0B
#   Revenue: ~$28-29B (+9-10% organic)
# Key segment breakdown (FY2025):
#   Electrical Americas: ~$13.8B (~54%); switchgear, PDUs, UPS, panelboards, busway
#   Electrical Global:   ~$7.2B  (~28%); European and Asia-Pacific electrical
#   Aerospace:           ~$3.3B  (~13%); aircraft fuel/hydraulic systems, connectors
#   Vehicle + eMobility: ~$1.5B  (~6%);  truck/commercial power mgmt, EV charging
# Data center exposure: ~30-35% of Electrical Americas; growing fastest
# Grid/utility exposure: ~20-25% of Electrical Americas; accelerating
# Industrial/commercial: ~40-45% of Electrical Americas; steady base
# Geographic mix: ~55% Americas, ~45% International (Europe/Asia)
# Dividend: $3.76/yr (quarterly $0.94); 16+ consecutive increases; ~1.1% yield
# Buyback: ~$1.5-2B/yr; modest share count reduction (~0.4%/yr) vs. peers
# Net debt: ~$6.5B (moderate; BBB+/A-; funding M&A and buybacks simultaneously)

# ── SCENARIO ARCHITECTURE ────────────────────────────────────────────────────
#
# BEAR = $262 | "Data center capex pauses + grid delays + industrial recession"
#   • Hyperscaler AI capex freezes for 6-12 months as enterprises slow AI
#     deployment spend — Eaton's fastest-growing and highest-margin demand driver
#     temporarily stalls; backlog converts more slowly than modeled
#   • Grid modernization projects face regulatory/permitting delays; utility capex
#     is deferred as rate cases are contested; renewable interconnect queue backs up
#   • Broad industrial recession reduces commercial construction and reshoring plant
#     orders; aerospace deliveries slow; Vehicle segment turns cyclically negative
#   • Operating margins compress from 25%+ back toward 20-21% as price/cost turns
#     negative and volume leverage reverses
#   • Multiple compresses to 20-21x trough EPS as "AI infrastructure bubble" fears
#     dominate sentiment → equity ~$262
#
# BASE = $248 | "Data center healthy, grid builds steadily, reshoring executes"
#   NOTE: BASE = CURRENT_PRICE = $340 (see SCENARIOS dict below)
#   • Hyperscaler capex grows 12-18%/yr through 2027-2028; Eaton captures its
#     share of power distribution buildout with continued multi-year backlogs
#   • Grid modernization accelerates modestly as the IRA spending ramps; utility
#     T&D capex grows at 8-10%/yr; renewable interconnect drives switchgear demand
#   • Reshoring capex converts into electrical orders on schedule; aerospace holds
#     steady; Vehicle segment flat to slightly down as EV transition mixes out
#   • Adj. EPS trajectory: ~$13.50 (FY2026) → ~$15.50 (FY2027) → ~$17.50 (FY2028)
#   • Multiple holds at ~24-25x; stock roughly fairly valued at $340
#
# BULL = $428 | "Capex supercycle accelerates + power-scarcity re-rate"
#   • Hyperscaler capex upgrades further: power availability becomes the critical
#     constraint on AI infrastructure buildout; Eaton's switchgear and UPS become
#     even more mission-critical — pricing power inflects; lead times extend to 3+yr
#   • Market recognizes Eaton as "the power toll of the AI era" — similar to how
#     NVDA chips are to compute, Eaton's switchgear is to power; re-rates to 28-30x
#   • Grid modernization adds another $3-5B of incremental electrical-equipment
#     demand as the IRA buildout converts to construction orders at scale
#   • EPS trajectory upgrades meaningfully; 2028 EPS approaches $20-22 → $428 at 28x
#
# XBULL = $510 | "Power scarcity recognized; elite infrastructure premium"
#   • Power availability is declared a national infrastructure priority; Eaton
#     becomes a strategic supplier across all US energy/data infrastructure
#   • Reshoring + data centers + grid modernization + energy transition all peak
#     simultaneously; 3-4 year multi-billion-dollar order visibility at record
#     backlogs; EPS approaching $25 by 2028-2029; 30x+ multiple → equity ~$510
#
SCENARIOS = {
    "BEAR":  262.0,
    "BASE":  340.0,
    "BULL":  428.0,
    "XBULL": 510.0,
}

BEAR  = SCENARIOS["BEAR"]
BASE  = SCENARIOS["BASE"]
BULL  = SCENARIOS["BULL"]
XBULL = SCENARIOS["XBULL"]

# ── EARNINGS POWER PRICE (EPP) ────────────────────────────────────────────────
# Trough EPS = $9.00 (severe AI-capex freeze + industrial recession + margin compression)
#   — data center orders stall for 12-18 months; industrial/commercial construction
#   weak; only grid/utility provides partial offset; worst-case scenario for all
#   five demand drivers simultaneously reversing
# Trough PE = 18.0× — above typical cyclical-industrial floor because the underlying
#   franchise (market leadership, long-term secular drivers) never truly goes away;
#   trough PE reflects that even in a downturn, investors price in the recovery
# EPP = $162.00 — stock at $340 is +109.9% above this floor; real franchise
#   value and the structural nature of the five secular tailwinds provide a meaningful
#   floor against permanent capital impairment
EPS_TROUGH      = 9.00
PE_TROUGH       = 18.0
EPP             = EPS_TROUGH * PE_TROUGH   # $162.00

# ── SCA (STRUCTURAL COMPETITIVE ADVANTAGE) FACTORS ───────────────────────────
SCA_FACTORS = {
    # (+) ELECTRICAL MARKET LEADERSHIP AND DATA CENTER SPECIFICATION WINS
    #   — #1 or #2 in switchgear, circuit breakers, PDUs, UPS, busway, panelboards
    #   in North America; "designed in" to virtually every major data center spec
    #   (hyperscaler, colo, enterprise); once Eaton equipment is spec'd into a campus
    #   build, the follow-on service/expansion relationships last 20-30 years
    "electrical_market_leadership_and_datacenter_specification_wins": +0.18,

    # (+) GRID MODERNIZATION AND ENERGY INFRASTRUCTURE POSITIONING
    #   — T&D switchgear, distribution transformers, and grid protection equipment
    #   in critical shortage as utilities race to modernize aging infrastructure;
    #   multi-year lead times signal structural, not cyclical, demand; Eaton's
    #   meter centers, reclosers, and smart-grid equipment are sole-sourced on
    #   many utility programs
    "grid_modernization_and_energy_infrastructure_positioning":      +0.16,

    # (+) MULTI-DRIVER STRUCTURAL DEMAND: CONVERGENCE OF FIVE CAPEX CYCLES
    #   — unlike a mono-thesis industrial, Eaton benefits from five independent
    #   secular demand drivers simultaneously: AI/cloud data centers, grid
    #   modernization, US manufacturing reshoring, energy transition, and
    #   commercial electrification; losing one or two does not break the thesis
    "five_independent_secular_capex_cycles_converging_simultaneously": +0.13,

    # (+) AEROSPACE POWER MANAGEMENT AND LONG-CYCLE DEFENSE EXPOSURE
    #   — Eaton's Aerospace segment supplies fuel/hydraulic/pneumatic systems to
    #   virtually every major commercial and military aircraft platform; long-cycle
    #   (15-20yr program lives), sole-source, high-margin, growing aftermarket;
    #   adds earnings stability and quality above the pure electrical cycle
    "aerospace_power_management_long_cycle_defense_exposure":        +0.11,

    # (-) PREMIUM VALUATION AND SENSITIVITY TO CAPEX CYCLE DECELERATION
    #   — at ~25x forward earnings, Eaton trades at a significant premium to the
    #   industrial universe; any perceived slowdown in hyperscaler AI capex spend
    #   or grid modernization timing directly impacts the multiple; premium stocks
    #   can compress quickly when single-driver narratives are challenged
    "premium_valuation_capex_cycle_sensitivity_and_deceleration_risk": -0.15,

    # (-) HYPERSCALER CUSTOMER CONCENTRATION AND LUMPINESS
    #   — top 5 data-center customers likely represent 20-25% of total electrical
    #   revenue; these customers have significant purchasing leverage and can
    #   defer or redistribute orders; capex cycles at hyperscalers are lumpy —
    #   a "pause quarter" can create significant order-intake volatility
    "hyperscaler_customer_concentration_and_order_lumpiness":        -0.12,

    # (-) INPUT COST AND SUPPLY CHAIN EXPOSURE (COPPER, STEEL, TRANSFORMER CORES)
    #   — switchgear, transformers, and UPS systems have significant raw-material
    #   content (copper, electrical steel, silicon); cost inflation can compress
    #   margins in periods of rapid commodity-price escalation; supply chain
    #   capacity (especially transformer cores and copper windings) has been the
    #   primary bottleneck, not customer demand — a risk for delivery timing
    "input_cost_and_transformer_supply_chain_capacity_risk":         -0.09,
}

SCA_NET   = sum(SCA_FACTORS.values())
SCA_SCALE = 0.45

# ── SIX PROXY SIGNALS ─────────────────────────────────────────────────────────
SIGNALS = {
    # 3.5 — Every major AI data center campus needs Eaton's switchgear, UPS, PDUs,
    #   and busway before a single server rack can be powered; demand is structural
    #   (not discretionary), multi-year backlogs confirm it, and Eaton's spec-in
    #   position makes it very difficult to substitute mid-project
    "ai_data_center_power_infrastructure_demand_cycle":
        {"score": 3.5, "weight": 0.20},

    # 3.5 — US grid is aging (average substation equipment >40 years old) and needs
    #   upgrading for EV charging, distributed solar/wind interconnect, and
    #   resilience; IRA funding is catalyzing multi-year utility T&D capex; extended
    #   lead times on distribution transformers confirm structural undersupply
    "grid_modernization_and_utility_td_capex_supercycle":
        {"score": 3.5, "weight": 0.18},

    # 3.0 — US manufacturing reshoring (CHIPS Act fabs, IRA clean-energy factories)
    #   and USMCA nearshoring (Mexican assembly plants) each require extensive
    #   electrical infrastructure buildout; Eaton is the specification-standard
    #   supplier for industrial electrical in North America
    "us_reshoring_and_industrial_electrification_capex":
        {"score": 3.0, "weight": 0.17},

    # 3.0 — #1 or #2 market position in switchgear and circuit breakers (North
    #   America); UPS market leader (Powerware); data center PDU and busway leader;
    #   switching costs are high — once an electrical distribution system is spec'd
    #   and installed, replacing it requires a full project shutdown and retrofit
    "electrical_products_market_leadership_and_switching_costs":
        {"score": 3.0, "weight": 0.16},

    # 2.0 — At ~25x forward EPS, much of the data-center demand optimism is priced
    #   in; a single quarterly order-intake disappointment from a hyperscaler pause
    #   can compress the stock 10-15% rapidly; the premium is the most significant
    #   near-term risk to total returns from this entry point
    "premium_valuation_hyperscaler_capex_concentration_risk":
        {"score": 2.0, "weight": 0.17},

    # 2.5 — Aerospace (~13% of revenue) is long-cycle, high-quality, and growing;
    #   Vehicle/eMobility (~6%) is transitioning but small; overall non-electrical
    #   segments provide diversification but not enough to offset a significant
    #   electrical-cycle downturn — limited natural hedge
    "aerospace_diversification_and_non_electrical_segment_balance":
        {"score": 2.5, "weight": 0.12},
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
PE_CONSERVATIVE = 25.0
EPS_FY2026E     = 13.50
CONSERVATIVE_PRICE = EPS_FY2026E * PE_CONSERVATIVE + 2 * ANNUAL_DIV
RETURN_2YR  = (CONSERVATIVE_PRICE - CURRENT_PRICE) / CURRENT_PRICE * 100
RETURN_ANN  = ((1 + RETURN_2YR / 100) ** 0.5 - 1) * 100

# ── REPORT ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    SEP = "━" * 78
    sep = "─" * 78

    print(SEP)
    print(f"  EATON CORPORATION PLC (NYSE: ETN) — BOTTOM-UP RISK/REWARD SIGNAL")
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
  Revenue (FY2025A):            ~$25.8B         (+9% organic; data center + grid + reshoring)
  Adjusted EPS (FY2025A):       ~$11.85/share   (+14% YoY; operating leverage + pricing)
  FCF (FY2025A):                ~$3.9B          (>100% adj. net-income conversion)
  Order backlog (FY2025A):      ~$14B           (record; data center + utility dominant)
  Net debt:                     ~$6.5B          (BBB+/A-; moderate; funding M&A + buybacks)
  Dividend:                     ${ANNUAL_DIV:.2f}/share/yr  (16+ consecutive increases; ~1.1% yield)
  Shares outstanding:           ~{SHARES_OUT_B:.3f}B         (buybacks ongoing; ~0.4%/yr reduction)

  FY2026 Consensus (adj. EPS):  ~$13.50/share   (+14% YoY; backlog conversion + pricing power)
  FY2026 Consensus (FCF):       ~$4.5-5.0B      (converting record backlog to cash)
  FY2026 Consensus (revenue):   ~$28-29B        (+9-10% organic)
  OR targets / guidance:        Electrical Americas margin ~26%+; sustained above 2024 levels

  Segment revenue breakdown (FY2025):
    Electrical Americas: ~$13.8B  (~54%): switchgear, PDUs, UPS, panelboards, busway
    Electrical Global:   ~$7.2B   (~28%): Europe + Asia-Pacific electrical
    Aerospace:           ~$3.3B   (~13%): aircraft fuel/hydraulic systems; long-cycle
    Vehicle + eMobility: ~$1.5B   (~6%):  truck power mgmt + EV charging solutions

  Key demand drivers and estimated revenue exposure (Electrical Americas):
    Data center (AI/cloud/colo):     ~30-35%   — fastest growing; multi-year backlogs
    Grid modernization (utilities):  ~20-25%   — accelerating; IRA-driven T&D capex
    Reshoring / industrial:          ~25-30%   — steady; CHIPS Act fabs, EV factories
    Commercial construction:         ~15-20%   — cyclical base; slower but resilient
""")

    print(sep)
    print("  SCENARIO NOTES")
    print(sep)
    print(f"""
  BEAR  ${BEAR:>6.1f}  Hyperscaler AI capex pauses; grid modernization delays; industrial
               recession; all five demand drivers soften simultaneously; margins
               compress; multiple falls to 20-21x trough EPS → equity ~$262.

  BASE  ${BASE:>6.1f}  Data center demand healthy; grid builds steadily; reshoring converts
               to electrical orders; adj. EPS ~$13.50 (FY26) → ~$15.50 (FY27);
               multiple holds ~24-25x; stock fairly valued at $340.

  BULL  ${BULL:>6.1f}  Power scarcity recognized as the AI constraint; Eaton re-rates to
               "power toll of the AI era" (~28-30x); grid + data center + reshoring
               all accelerate simultaneously; EPS approaches $20-22 by FY2028.

  XBULL ${XBULL:>6.1f}  Elite infrastructure premium (30x+); power declared a national
               priority; all five capex cycles peak simultaneously; EPS ~$25 by 2029.
""")

    print(sep)
    print("  PRODUCT FRANCHISE & SECULAR DEMAND DRIVERS")
    print(sep)
    print(f"""
  Electrical Americas (54% of revenue) — the growth engine:
    • Low-voltage switchgear and switchboards: the primary power-distribution
      "front door" of every commercial building, data center, factory, and
      utility substation; Eaton holds ~30-35% North American market share
    • Circuit breakers and panelboards: downstream from switchgear; Cutler-Hammer
      brand dominates commercial/industrial construction specification in North America
    • Power distribution units (PDUs): rack-level power distribution inside data
      centers; Eaton is the specification-standard PDU supplier for hyperscalers
    • Uninterruptible power supplies (UPS): Powerware brand — critical backup power
      for data centers; increasingly specified by hyperscalers for the entire campus
    • Busway (power busduct): distributes power from switchgear to rows of server
      racks; faster to install than conduit/wire; Eaton's busway is the most
      commonly specified in large data center build-outs
    • Meter centers and smart-grid equipment: utility-grade distribution automation;
      reclosers, sectionalizers, and smart sensors for grid modernization programs

  The Five Secular Demand Drivers (all pulling simultaneously):
    1. AI/Cloud Data Centers: MSFT Azure, AWS, Google, Meta each committing $100B+
       annual capex through 2028; every campus build requires 10s-100s of MW of
       Eaton electrical distribution equipment before a server is installed
    2. Grid Modernization: US grid average age >40 years; IRA provides $60B+
       for T&D upgrades; utilities increasing capex 8-10%/yr; transformer and
       switchgear lead times of 18-36 months signal structural, not cyclical, demand
    3. US Manufacturing Reshoring: CHIPS Act ($52B): TSMC, Intel, Samsung fabs in
       AZ/OH/TX — each requires 500-1,000 MW of new power infrastructure; IRA:
       EV factories, battery plants, and solar manufacturing all need extensive
       electrical buildouts; Eaton is the primary specification supplier for all
    4. Energy Transition: wind and solar interconnect equipment; battery energy
       storage systems; grid-scale UPS for frequency regulation; offshore-to-onshore
       HVDC connection equipment — a growing but early-stage contribution
    5. Commercial/Industrial Electrification: building codes mandating transition
       from gas to electric HVAC, cooking, and process heat; accelerating adoption
       of higher-density power infrastructure in retrofitted commercial buildings

  Aerospace Segment (13% of revenue — diversification and quality anchor):
    • Fuel, hydraulic, and pneumatic systems on commercial and military platforms
    • Boeing 737/777/787, Airbus A320/A350, F-35 (fuel systems), military transports
    • 15-20 year program lives; sole-source on most platforms; high-margin aftermarket
    • Provides earnings resilience and quality above the electrical capex cycle
""")

    print(sep)
    print("  ANALYST CONSENSUS (JUNE 2026)")
    print(sep)
    print(f"""
  Coverage:    ~28 analysts
  Buy/Strong:  ~21 (75%)       Hold: ~6 (21%)       Sell: ~1 (4%)
  Price target: ~$372 consensus  (range: $310-450)
  Commentary:  broad bullish consensus on data center and grid demand; primary debate
               is whether ~25x forward multiple adequately reflects the risk of a
               hyperscaler capex pause; bulls argue power scarcity is structural and
               re-rating to 28-30x is justified; bears cite lumpiness of large orders
               and concentration risk in the top 5 data center customers
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
    print(f"  Note: the floor case holds the multiple flat at 25x — a fair but not aggressive")
    print(f"  multiple for a premium electrical infrastructure franchise; the EPS growth alone")
    print(f"  (~14%/yr) drives a modest positive return even without any re-rating. BULL/XBULL")
    print(f"  require the power-scarcity thesis to manifest in a 'toll road of AI' re-rating.")

    print(f"\n{sep}")
    print("  WHY THIS IS AN ◎ ACCUMULATE, NOT A ◌ WATCHLIST OR ◉ BUY")
    print(sep)
    print("""
  Eaton is sitting at the intersection of five independent secular capex cycles —
  AI/cloud data centers, grid modernization, US manufacturing reshoring, the energy
  transition, and commercial electrification — all pulling on the same electrical
  switchgear, UPS, PDU, and busway capacity simultaneously. Unlike a single-thesis
  trade, you'd need most of these five drivers to reverse concurrently before the
  structural growth story breaks. Record ~$14B backlogs and multi-year lead times
  on distribution transformers and switchgear confirm this demand is structural.
  Ratio B of 0.88× reflects that the bull case is clearly achievable and the franchise
  quality is beyond dispute — but that you are not being offered this at a bargain.

  WHAT THE MARKET ALREADY PRICES IN (at $340, ~1/3 up 52-wk range, ~25x forward):
  • AI/cloud data center capex continues at current pace through 2027-2028; Eaton
    captures its share of every hyperscaler power distribution buildout
  • Grid modernization proceeds on IRA-funded timeline; utility T&D capex grows
    8-10%/yr; Eaton's switchgear lead times normalize gradually without demand loss
  • Reshoring (CHIPS Act, IRA factories) converts to electrical orders on schedule
  • Operating margins hold at ~25%+ Electrical Americas even as backlog converts
    and pricing normalizes slightly from recent elevated levels

  WHAT COULD MAKE THIS MORE THAN FAIRLY PRICED (the ACCUMULATE case):
  1. Hyperscaler capex upgrades — power availability confirmed as the binding
     constraint on AI infrastructure buildout, not compute or memory; Eaton's
     switchgear becomes "critical path" on every data center project schedule;
     pricing power inflects and lead times extend to 3+ years structurally
  2. Grid modernization accelerates beyond current IRA projections — extreme
     weather, blackout events, or policy push creates a step-change in utility
     T&D capex; transformer and switchgear undersupply becomes a multi-decade story
  3. Market re-rates Eaton as "the power toll of the AI era" (28-30x) recognizing
     that every dollar of AI compute capex requires ~$0.40-0.60 of electrical
     infrastructure — Eaton's total addressable market directly scales with AI spend
  4. Aerospace segment re-rates separately as commercial aviation and defense both
     enter prolonged upcycles; hidden value in a segment currently discounted by
     the electrical-heavy investor narrative

  THE RISK (the honest read):
  • Hyperscaler capex pauses — the single biggest near-term risk; if AWS/MSFT/Google
    pull back on data center spend for even 1-2 quarters, order intake disappoint
    materially; at 25x forward, the market has low tolerance for this scenario
  • Valuation premium limits return if execution merely meets guidance — at 25x,
    "in line" quarters don't generate alpha; you need beats or re-ratings to justify
    the entry point
  • Input cost inflation (copper, electrical steel) can compress margins at exactly
    the moment when the premium multiple is hardest to maintain

  WHAT MAKES THIS AN ACCUMULATE RATHER THAN MERELY A WATCHLIST:
  • Ratio B of 0.88× — meaningfully tilted in the investor's favor — for a franchise
    with five independent secular tailwinds is a genuine accumulation point; you are
    not overpaying for quality, and the structural demand drivers are real
  • Five independent secular tailwinds means the "bear case" requires a coordinated
    macro shock that simultaneously reverses all five demand drivers — less likely
    than any single driver disappointing
  • The conservative floor case (25x multiple flat) still produces a small positive
    return driven by EPS growth alone; the dividend (~1.1%) provides a modest cushion

  POSITION SIZING GUIDANCE:
  • ACCUMULATE — build a position steadily here; add more aggressively on any
    pullback below $305-315 (where Ratio B would approach BUY territory and the
    power-scarcity / grid-modernization thesis would be even more compelling vs.
    the multiple) — such pullbacks will likely be driven by macro fear, not by any
    deterioration in Eaton's structural positioning
  • Watch for: (1) quarterly order-intake data — the leading indicator of forward
    demand visibility; (2) hyperscaler capex guidance updates (the dominant near-term
    swing factor); (3) grid modernization utility capex announcements; (4) lead-time
    trends on switchgear and distribution transformers (the capacity constraint signal)
""")

    print(SEP)
    print(f"""
SUMMARY: ETN ◎ ACCUMULATE — Ratio B 0.88× (22.9% downside / 25.9% upside). THE \
ESSENTIAL INFRASTRUCTURE OF THE AI AND ENERGY-TRANSITION ERA: trading at $340.00 \
(52-wk range $278-382, roughly a third up the range — consolidated after multi-year \
re-rating; premium multiple reflecting genuine structural demand) as the #1-#2 supplier \
of electrical switchgear, circuit breakers, PDUs, UPS, and busway — the mission-critical \
power infrastructure every data center, semiconductor fab, and grid-modernization project \
requires. FIVE INDEPENDENT SECULAR TAILWINDS: (1) AI/cloud data center construction \
(hyperscalers committing $100B+ capex each through 2028); (2) grid modernization \
(IRA-funded US T&D upgrades; 40-yr-old infrastructure; 18-36 month lead times on \
transformers/switchgear confirm structural demand); (3) US reshoring (CHIPS Act fabs, \
IRA clean-energy factories); (4) energy transition (renewable interconnect, BESS); \
(5) commercial electrification. Record ~$14B backlog. Electrical Americas ~54% of \
revenue at ~25%+ operating margin; Aerospace ~13% (long-cycle, sole-source, growing \
aftermarket). FY2026E adj. EPS ~$13.50 (+14%); FCF ~$4.5-5.0B. Dividend $3.76/yr, \
16+ consecutive increases, ~1.1% yield. Net debt ~$6.5B (BBB+/A-). Consensus Buy (~21 \
of 28 analysts), PT ~$372 (range $310-450). Conservative 2yr (no re-rate, 25x flat): \
EPS $13.50 x 25x + $7.52 div = $345.02 -> +1.5% — BULL/XBULL require power-scarcity \
recognition and re-rate toward 28-30x "toll road of AI era." FIVE STRUCTURAL TAILWINDS \
MEETING PROVEN ELECTRICAL MARKET LEADERSHIP: accumulate steadily; add aggressively \
below $305-315. Bear $262 · Base $340 · Bull $428 · XBull $510."""
    )

    print(f"SIGNAL: {SIGNAL_TEXT} (electrical power management franchise at the intersection of AI data centers, grid modernization, US reshoring, and energy transition — five independent secular capex cycles pulling on the same equipment simultaneously) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
