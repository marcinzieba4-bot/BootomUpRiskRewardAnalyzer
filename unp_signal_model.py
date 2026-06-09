"""
Union Pacific Corporation (NYSE: UNP)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.90×  |  EPP Gap: +82.4%

A PERMANENT WESTERN-US RAIL DUOPOLY COMPOUNDING QUIETLY BEHIND AN
OPERATING-RATIO TRANSFORMATION — THE TOLL ROAD YOU CANNOT REPLICATE AT ANY PRICE
Trading at $248.00 (52-week range $214-272, roughly a third up its range — a name
that has lagged the broader market's re-rating of "infrastructure-like compounders"
because investors are still watching Jim Vena's PSR (Precision Scheduled Railroading)
execution play out quarter by quarter) on the back of what is, structurally, one of
the most durable infrastructure monopolies in the American economy: a 32,000-mile
rail network spanning 23 states across the western two-thirds of the US that took
150+ years and the full power of 19th-century capital markets to build and that
cannot be replicated at any price today. Union Pacific and BNSF (owned by Berkshire
Hathaway) are the only two Class I railroads serving the western US — a regulated
natural duopoly on the movement of bulk commodities, industrial goods, intermodal
containers, and automotive products across the most economically productive and
fastest-growing geography in the continental United States.

The real compounding engine: pricing power. Because Union Pacific is the sole viable
rail carrier across most of its network, it can grow revenue per unit (yield) at
3-5% per year regardless of volume changes — and with Jim Vena's PSR efficiency
program simultaneously reducing the cost to move each unit, the operating leverage
on incremental pricing flows almost entirely to the bottom line. Add a
structurally-growing secular tailwind from US-Mexico USMCA near-shoring (Union
Pacific's gateway routes into Mexico make it the essential carrier for manufacturing
reshoring from Asia to Mexico, a multi-decade demand trend that is just beginning)
and a management team actively reducing the share count at ~3-4% per year, and you
have the ingredients for a durable mid-teens EPS CAGR even in a sluggish macro.

The honest tension: Union Pacific is not cheap on a current-year basis (~20x forward
EPS) and carries real exposure to the economic cycle — industrial volumes, agricultural
exports, and especially the intermodal container cycle all soften in recessions. The
secular coal decline (from ~14% to now ~10-11% of revenue, still declining) is a
persistent headwind. And PSR execution, while credibly underway, requires multi-year
patience before the full operating-ratio improvement appears in earnings.

Conviction: HIGH on the structural franchise (the western-US rail duopoly is
permanent — you cannot build a railroad, regulatory or otherwise, to compete with
it); MODERATE-HIGH on the PSR execution trajectory under Jim Vena; MODERATE on
near-term volumes given macro sensitivity. Ratio B of 0.90× reflects a franchise
whose near-term entry point is genuinely attractive without demanding a deep-value
discount that this quality of asset has never historically offered.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "UNP"
COMPANY         = "Union Pacific Corporation"
SECTOR          = "Transportation · Class I Railroad · Western US Rail Duopoly (32,000 miles / 23 states) · NYSE: UNP"
SECTOR_GROUP    = "Industrials"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 248.00   # June 2026 — PSR execution monitored; below recent highs
ANNUAL_DIV      = 5.36     # Quarterly $1.34/share; ~2.2% yield; 16 consecutive increases
SHARES_OUT_B    = 1.32     # Billion shares (declining ~3-4%/yr via active buyback)
FW52_HIGH       = 272.00   # Recent ceiling; limited by macro-sensitivity perception
FW52_LOW        = 214.00   # Trough on industrial-cycle softness and volume concerns

# ── FY2025 REPORTED / FY2026 ESTIMATES ──────────────────────────────────────
# UNP FY2025 actuals:
#   Revenue: ~$24.1B (+4% YoY; volume recovery + pricing)
#   Adjusted EPS: ~$11.35 (+8% YoY; operating leverage + buybacks)
#   FCF: ~$6.4B (capex ~$3.4B; high-quality conversion)
#   Operating ratio: ~64.5% (improving from 66% — PSR in early innings)
#   Total carloads: ~8.7M (bulk, industrial, premium segments)
# FY2026 estimates (June 2026):
#   Adjusted EPS: ~$12.20-12.60 (pricing + PSR efficiency + buyback amplification)
#   FCF: ~$6.8-7.2B
#   Operating ratio target: ~62-63% (CEO Vena's multi-year PSR goal: sub-60%)
# Key metrics context:
#   Revenue/carload yield growth: consistently ~4-5%/yr; pricing power is structural
#   Share count declining ~3-4%/yr; adds ~1.5-2% to EPS growth "for free"
#   Coal decline: ~10-11% of revenue and falling ~5-7%/yr by volume — headwind
#   USMCA/Mexico: cross-border volumes growing double-digits; multi-decade tailwind
#   Intermodal: ~24% of revenue; most cyclically sensitive but highest long-run growth
#   Bulk (ag/fertilizer/coal): ~38% of revenue; defensive, slow-growth
#   Industrial (chemicals/metals/energy): ~38% of revenue; leveraged to US output

# ── SCENARIO ARCHITECTURE ────────────────────────────────────────────────────
#
# BEAR = $192 | "Recession + volume collapse + PSR stalls"
#   • US recession drives a meaningful industrial and intermodal volume decline
#     (-12-15% in intermodal, -8-10% in industrial) — directly compressing carloads
#     and revenue even as pricing remains positive
#   • Coal accelerates to near-zero contribution faster than modeled (utility
#     coal retirements accelerate) without an offsetting volume gain elsewhere
#   • PSR execution hits operational headwinds — locomotive productivity gains are
#     offset by service-quality issues (historically the PSR tension): customers
#     divert traffic to trucks or BNSF; yield growth slows below 3%
#   • Operating ratio fails to improve toward target; EPS growth stalls in the
#     $10.50-11.00 range; multiple compresses to 17-18x trough → equity ~$192
#
# BASE = $248 | "Moderate growth, PSR delivers, buybacks compound"
#   • US economy grows at 2-2.5%; intermodal volumes recover modestly (+3-5%);
#     industrial volumes track GDP; ag exports hold steady
#   • PSR execution on track: operating ratio reaches 62-63% by FY2027;
#     yield/revenue-per-carload grows at 4-5% consistently
#   • FCF of ~$7B supports $5.36/yr dividend (growing ~6-7%/yr) + ~$4-4.5B/yr
#     buybacks (share count declining ~3%/yr) → EPS CAGR of ~8-10%
#   • Multiple holds at ~20x FY2026E; stock broadly fairly valued at $248
#
# BULL = $310 | "PSR inflects + USMCA surge + infrastructure re-rate"
#   • PSR operating ratio hits 60% target by FY2027; market recognizes UNP as an
#     infrastructure compounder (toll-road economics) and re-rates toward 22-24x
#   • USMCA near-shoring volumes accelerate meaningfully: automotive + manufacturing
#     cross-border traffic grows 10-15%/yr as supply chains restructure from Asia;
#     UNP's Mexico gateway position captures the bulk of this incremental demand
#   • Intermodal reprices higher as truck capacity tightens and ELD enforcement
#     raises trucking costs; modal shift toward rail accelerates
#   • Share count below 1.25B by FY2027; EPS approaching $14-15; equity ~$310
#
# XBULL = $370 | "Elite toll-road status + volume inflection + M&A optionality"
#   • Market fully re-rates UNP to "regulated infrastructure compounder" tier
#     (25-27x) — similar to how Visa/Mastercard were re-rated from "payment
#     processor" to "toll road" over 2010-2020; permanent duopoly recognized
#   • USMCA proves to be a decade-long volume and yield tailwind; UNP's
#     intermodal + automotive cross-border volumes double from 2026 levels
#   • STB regulatory environment remains benign; no forced rate caps or
#     open-access mandates that would structurally impair pricing power
#   • EPS trajectory reaches $17-18 by 2028-2029; equity ~$370 at 22x
#
SCENARIOS = {
    "BEAR":  192.0,
    "BASE":  248.0,
    "BULL":  310.0,
    "XBULL": 370.0,
}

BEAR  = SCENARIOS["BEAR"]
BASE  = SCENARIOS["BASE"]
BULL  = SCENARIOS["BULL"]
XBULL = SCENARIOS["XBULL"]

# ── EARNINGS POWER PRICE (EPP) ────────────────────────────────────────────────
# Trough EPS = $8.50 (severe recession, volumes down 15%, coal near-zero, PSR stalls)
#   — hard-landing scenario where all segments weaken simultaneously; still profitable
#   because rail infrastructure is largely fixed-cost at the network level
# Trough PE = 16.0× — railroads command above-average trough multiples because
#   the franchise value (the network itself) never goes to zero and earnings recover
#   sharply; 16x is consistent with Class I railroad trough history
# EPP = $136.00 — stock at $248 is +82.4% above this floor; the permanent duopoly
#   franchise means the risk of permanent capital impairment is genuinely low
EPS_TROUGH      = 8.50
PE_TROUGH       = 16.0
EPP             = EPS_TROUGH * PE_TROUGH   # $136.00

# ── SCA (STRUCTURAL COMPETITIVE ADVANTAGE) FACTORS ───────────────────────────
SCA_FACTORS = {
    # (+) PERMANENT WESTERN US RAIL NETWORK — CANNOT BE REPLICATED
    #   — 32,000 miles of right-of-way across 23 states built over 150 years;
    #   the combination of land rights, regulatory approvals, physical construction,
    #   and terminal/port access cannot be replicated at any price; the STB
    #   (Surface Transportation Board) has effectively closed the door on new
    #   Class I network construction — this is a permanent infrastructure moat
    "permanent_western_us_rail_network_unreplicable_infrastructure":  +0.20,

    # (+) STRUCTURAL PRICING POWER IN A REGULATED DUOPOLY
    #   — as the sole (or dominant) rail carrier in most corridor pairs, UNP
    #   sets prices with a degree of autonomy that few industries can match;
    #   revenue per carload (yield) has grown 3-5% per year through economic
    #   cycles for two decades; pricing is "above inflation" structurally
    "structural_pricing_power_and_yield_growth_above_inflation":      +0.17,

    # (+) PSR OPERATING EFFICIENCY AND MARGIN EXPANSION TRAJECTORY
    #   — Jim Vena (ex-CN Railway; one of the original PSR architects) is
    #   applying proven PSR principles: longer trains, faster velocity, lower
    #   dwell time, locomotive productivity — the operating ratio improvement
    #   from ~66% toward 60% target is worth ~$1.5-2B in EBITDA at current scale
    "psr_operating_efficiency_and_margin_expansion_trajectory":       +0.14,

    # (+) USMCA NEAR-SHORING AND MEXICO GATEWAY SECULAR TAILWIND
    #   — UNP's gateway routes into Mexico (via Laredo, Eagle Pass, El Paso)
    #   position it as the essential carrier for the near-shoring of manufacturing
    #   from Asia to Mexico — a multi-decade demand trend driven by USMCA, supply-
    #   chain resilience priorities, and US tariff policy; cross-border automotive
    #   and industrial volumes are growing double-digits annually
    "usmca_near_shoring_and_mexico_gateway_secular_tailwind":         +0.13,

    # (+) FCF MACHINE WITH DISCIPLINED SHAREHOLDER RETURNS
    #   — $6-7B annual FCF; $3.4B capex is largely maintenance of the existing
    #   network (not "growth" capex requiring incremental returns); remaining FCF
    #   supports 16-year consecutive dividend growth streak + ~$4-4.5B/yr buybacks
    #   → share count declining ~3-4%/yr, mechanically amplifying per-share EPS growth
    "fcf_generation_and_disciplined_shareholder_capital_returns":     +0.12,

    # (-) COAL SECULAR DECLINE — persistent headwind
    #   — utility coal volumes declining ~5-8%/yr as natural gas and renewables
    #   displace coal in power generation; coal is still ~10-11% of revenue and
    #   contributes disproportionately to bulk-segment margin; the structural
    #   decline is predictable but the pace can accelerate (e.g., cold-weather
    #   demand normalization, utility coal retirements ahead of schedule)
    "coal_secular_decline_and_utility_power_mix_shift":               -0.13,

    # (-) CYCLICAL VOLUME EXPOSURE AND RECESSION SENSITIVITY
    #   — intermodal (~24% of revenue) is the most macro-sensitive segment;
    #   industrial volumes track US industrial production directly; in a genuine
    #   recession, total carloads can decline 8-12% — directly compressing
    #   revenue before any cost offsets, since the rail network's fixed costs
    #   are largely inelastic to short-term volume changes
    "cyclical_volume_exposure_and_recession_sensitivity":             -0.11,

    # (-) STB REGULATORY RISK AND OPEN-ACCESS POLICY UNCERTAINTY
    #   — the Surface Transportation Board regulates railroad rates and access;
    #   politically-driven proposals for "reciprocal switching" (mandatory third-
    #   party access to UNP's network) resurface periodically; while no forced
    #   access mandate has been enacted, the regulatory risk is permanent and
    #   creates a ceiling on how premium a multiple the market will ascribe
    "stb_regulatory_risk_and_open_access_policy_overhang":           -0.08,
}

SCA_NET   = sum(SCA_FACTORS.values())
SCA_SCALE = 0.45

# ── SIX PROXY SIGNALS ─────────────────────────────────────────────────────────
SIGNALS = {
    # 4.0 — The western US rail duopoly is arguably the single most durable
    #   infrastructure moat in the American economy: you cannot build a competing
    #   railroad, the regulated structure prevents entry, and the network grows
    #   more valuable as US-Mexico trade and western-US economic activity expand
    "western_us_rail_duopoly_and_permanent_infrastructure_moat":
        {"score": 4.0, "weight": 0.22},

    # 3.5 — Revenue per carload (yield) consistently grows 3-5%/yr through cycles;
    #   PSR operating-ratio improvement from ~66% toward 60% target generates
    #   operating leverage that flows almost entirely to EPS; the combination of
    #   pricing + efficiency is a self-reinforcing EPS compounder
    "pricing_power_plus_psr_operating_leverage_compounding":
        {"score": 3.5, "weight": 0.20},

    # 3.0 — Near-shoring (USMCA cross-border) is a genuine multi-decade secular
    #   tailwind: manufacturing supply chains are actively restructuring from Asia
    #   to Mexico, and UNP's gateway routes position it to capture the bulk of
    #   incremental cross-border automotive/industrial traffic; early innings
    "usmca_near_shoring_and_cross_border_volume_secular_growth":
        {"score": 3.0, "weight": 0.18},

    # 3.0 — ~$6-7B FCF, 16-year consecutive dividend growth streak, ~$4-4.5B/yr
    #   buybacks reducing share count ~3-4%/yr; capital allocation is disciplined
    #   and consistent — a multi-decade track record of returning capital above
    #   the rate of earnings growth
    "fcf_conversion_dividend_growth_and_share_count_reduction":
        {"score": 3.0, "weight": 0.17},

    # 2.0 — Coal secular decline (~10-11% of revenue, declining) + intermodal
    #   cyclicality + general industrial cycle sensitivity constrain near-term
    #   volume upside; the macro environment is the primary swing factor on
    #   whether UNP delivers 6% or 12% EPS growth in any given year
    "volume_cyclicality_coal_decline_and_macro_sensitivity":
        {"score": 2.0, "weight": 0.12},

    # 2.5 — ~20x FY2026E is not cheap for a cyclically-exposed industrial,
    #   but for a regulated infrastructure compounder with a permanent moat and
    #   a clear PSR-driven margin expansion story, it's arguably below intrinsic
    #   value; the re-rating catalyst is OR improvement + USMCA volumes building
    "valuation_relative_to_infrastructure_and_industrial_peers":
        {"score": 2.5, "weight": 0.11},
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
PE_CONSERVATIVE = 20.0
EPS_FY2026E     = 12.30
CONSERVATIVE_PRICE = EPS_FY2026E * PE_CONSERVATIVE + 2 * ANNUAL_DIV
RETURN_2YR  = (CONSERVATIVE_PRICE - CURRENT_PRICE) / CURRENT_PRICE * 100
RETURN_ANN  = ((1 + RETURN_2YR / 100) ** 0.5 - 1) * 100

# ── REPORT ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    SEP = "━" * 78
    sep = "─" * 78

    print(SEP)
    print(f"  UNION PACIFIC CORPORATION (NYSE: UNP) — BOTTOM-UP RISK/REWARD SIGNAL")
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
  Revenue (FY2025A):            ~$24.1B         (+4% YoY; volume recovery + yield growth)
  Adjusted EPS (FY2025A):       ~$11.35/share   (+8% YoY; operating leverage + buybacks)
  FCF (FY2025A):                ~$6.4B          (capex ~$3.4B; >90% OCF conversion)
  Operating ratio (FY2025A):    ~64.5%          (improving from 66%; PSR in early innings)
  Total carloads (FY2025A):     ~8.7M           (bulk + industrial + premium segments)
  Net debt:                     ~$25B           (investment-grade; BBB+/Baa1; rail-normal)
  Dividend:                     ${ANNUAL_DIV:.2f}/share/yr  (16 consecutive annual increases; ~2.2% yield)
  Shares outstanding:           ~{SHARES_OUT_B:.2f}B         (declining ~3-4%/yr via ~$4-4.5B/yr buybacks)

  FY2026 Consensus (adj. EPS):  ~$12.20-12.60   (pricing + PSR efficiency + buyback amplification)
  FY2026 Consensus (FCF):       ~$6.8-7.2B      (capex roughly flat; incremental FCF flows to returns)
  Operating ratio target:       ~60%            (CEO Vena multi-year PSR goal; current ~64.5%)

  Revenue segment mix (FY2025):
    Bulk (ag/fertilizer/coal):  ~38%    (+2% vol YoY; coal -6% offset by ag/fertilizer growth)
    Industrial (chem/metals):   ~38%    (+4% vol YoY; chemicals strong, energy recovering)
    Premium (intermodal/auto):  ~24%    (+7% vol YoY; intermodal benefiting from near-shoring)

  CEO Jim Vena (joined 2023): former CN Railway COO; one of the original PSR architects;
    key metrics improving — train length +8%, locomotive productivity +6%, dwell time -9%
""")

    print(sep)
    print("  SCENARIO NOTES")
    print(sep)
    print(f"""
  BEAR  ${BEAR:>6.1f}  Recession: intermodal -12-15%, industrial -8-10%; coal accelerates to
               near-zero; PSR hits service headwinds; OR rises to 67-68%; multiple
               compresses to 17-18x trough EPS → equity ~$192.

  BASE  ${BASE:>6.1f}  Moderate 2-2.5% GDP growth; intermodal +3-5%; OR reaches 62-63%;
               yield +4-5%/yr; FCF ~$7B; ~$4.5B buybacks; EPS ~$12.30-12.60;
               ~20x forward fairly values the stock at $248.

  BULL  ${BULL:>6.1f}  PSR hits 60% OR target ahead of schedule; USMCA cross-border volumes
               surge (+10-15%/yr); market re-rates UNP as infrastructure compounder
               at 22-24x; EPS trajectory toward $14-15 by FY2028 → equity ~$310.

  XBULL ${XBULL:>6.1f}  Elite toll-road status (25-27x); near-shoring volumes double; coal
               fully replaced by intermodal/industrial; EPS $17-18 by 2029 → $370.
""")

    print(sep)
    print("  NETWORK & FRANCHISE HIGHLIGHTS")
    print(sep)
    print(f"""
  The Network (Why It Cannot Be Replicated):
    • 32,000 route-miles across 23 states — the backbone of western US commerce
    • 8 of the 10 largest US cities in the West are served exclusively or primarily
      by UNP; no alternative rail carrier can credibly replicate these routes
    • The original transcontinental railroad (completed 1869); built with land grants
      that today's right-of-way holders couldn't replicate at any cost
    • 50+ ports/gateways served: Los Angeles/Long Beach (US #1 port complex), Oakland,
      Seattle/Tacoma, Gulf Coast (Houston/New Orleans), and 6 Mexico border crossings

  Key Corridors and Growth Drivers:
    • Los Angeles Basin ↔ Chicago/Midwest: the core intermodal lane; Asia imports
      converted to domestic ground movement; ~40% of UNP intermodal volumes
    • US ↔ Mexico (USMCA Gateway): Laredo (#1 US-Mexico land port by value),
      Eagle Pass, El Paso — UNP handles the majority of US-Mexico rail traffic;
      automotive (GMM Silao, BMW San Luis Potosí, Tesla supplier chain) and
      manufactured goods volumes growing double-digits; near-shoring in early innings
    • Gulf Coast ↔ Midwest: chemicals (TDI/MDI), plastics, and fertilizers;
      Permian/Eagle Ford energy products; chemical corridor is the highest-margin
      industrial lane in the network
    • Agricultural corridor: Pacific Northwest grain (wheat, corn, soybeans) to
      Pacific Export Terminals; steady/defensive, weather-dependent

  PSR (Precision Scheduled Railroading) Under Jim Vena:
    • Operating ratio improvement from ~66% (pre-Vena) toward 60% target
      represents ~$1.5-2B of annual EBITDA improvement at current revenue scale
    • Key PSR metrics: train length (+8% YoY), locomotive productivity (+6%),
      car velocity (+4%), dwell time at yards (-9%) — all moving in the right direction
    • Historical precedent: CN Railway (Vena's prior employer) went from 70%+ OR
      to sub-60% over 5 years under PSR — a direct blueprint for what UNP is executing

  Coal Secular Decline (the managed headwind):
    • Coal declined from ~14% of revenue (2020) to ~10-11% (2025) — on track for
      ~7-8% by 2028 as utility retirements continue
    • Each 1% of revenue lost to coal (~$240M) has historically been replaced by
      intermodal and industrial growth within 12-18 months at the current growth rate
    • The coal decline has been "priced in" by the market for years — it is not a
      surprise, not accelerating beyond expectations, and not existential

  Capital Returns:
    • Dividend: $5.36/yr (quarterly $1.34); 16 consecutive annual increases;
      growing ~6-8%/yr; ~2.2% current yield at $248
    • Buybacks: ~$4-4.5B/yr authorization; share count ~1.32B → targeting <1.20B
      by FY2028; each 1% share count reduction adds ~$0.11-0.12 to EPS
    • Net debt ~$25B is investment-grade and rail-normal (the network itself has
      >$300B of replacement-cost value; leverage is asset-backed, not cash-burn)
""")

    print(sep)
    print("  ANALYST CONSENSUS (JUNE 2026)")
    print(sep)
    print(f"""
  Coverage:    ~31 analysts
  Buy/Strong:  ~20 (65%)       Hold: ~10 (32%)       Sell: ~1 (3%)
  Price target: ~$272 consensus  (range: $235-320)
  Commentary:  strong consensus on franchise quality and PSR trajectory; debate on
               the pace of OR improvement (optimists: 60% by FY2027; skeptics: 62%
               by FY2028); USMCA near-shoring cited as the emerging differentiated
               bull case; key watch: quarterly OR progress and intermodal volumes
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
    print(f"  Note: the floor case holds the multiple flat at 20x — a fair multiple for a")
    print(f"  permanent infrastructure duopoly; even without any re-rating, EPS growth and")
    print(f"  dividends compound toward ~{CONSERVATIVE_PRICE:.0f}. BULL/XBULL add the PSR-driven OR")
    print(f"  improvement and USMCA volume acceleration on top of this earnings growth base.")

    print(f"\n{sep}")
    print("  WHY THIS IS AN ◎ ACCUMULATE, NOT A ◌ WATCHLIST OR ◉ BUY")
    print(sep)
    print("""
  Union Pacific is the western US's irreplaceable rail infrastructure backbone —
  32,000 miles built over 150 years, serving 8 of the 10 largest western US cities,
  with gateway routes into Mexico that no trucking company, no competing railroad, and
  no government policy could realistically replicate. The regulated duopoly with BNSF
  is permanent. Pricing power of 3-5% per year is structural. And Jim Vena's PSR
  program — operating ratio declining from 66% toward a 60% target — is generating
  operating leverage on every incremental revenue dollar that flows almost entirely
  to earnings per share. At Ratio B of 0.90×, the risk/reward tilts modestly in the
  investor's favor for a franchise that has never historically been cheap.

  WHAT THE MARKET ALREADY PRICES IN (at $248, ~1/3 up 52-week range, ~20x forward):
  • PSR executing but requiring multi-year patience (60% OR target not yet achieved)
  • Intermodal volumes recovering at a moderate pace consistent with GDP growth
  • Coal secular decline (~10-11% of revenue) continuing at its historical ~5-7%/yr
  • USMCA near-shoring is a real tailwind but still in early innings — not yet
    visible in a way that the consensus is giving full credit to
  • ~20x forward already reflects that this is a high-quality business, not a value stock

  WHAT COULD MAKE THIS MORE THAN FAIRLY PRICED (the ACCUMULATE case):
  1. PSR operating ratio hits 60% ahead of schedule — every 100bps of OR improvement
     at $24B revenue scale is ~$240M of EBITDA; at 20x EPS this adds ~$3-4/share to
     fair value; consensus is modeling 62-63% by FY2027, not 60%
  2. USMCA near-shoring volumes accelerate materially — the automotive and
     manufactured goods cross-border flows that are early-stage today could become
     the dominant volume growth story of the next decade; UNP's position is unique
  3. Intermodal reprices higher as the ELD (electronic logging device) era permanently
     shifts more long-haul freight from truck to rail — each 1% modal shift is worth
     ~$500M in incremental intermodal revenue at current market share
  4. Market re-rates UNP as a "regulated infrastructure compounder" (toll-road tier)
     rather than an industrial cyclical — a permanent re-rating from ~20x to 24-26x,
     similar to how pipeline and utility franchises re-rated over 2010-2020

  THE RISK (the honest read):
  • A US recession compresses industrial and intermodal volumes simultaneously —
    the most direct near-term risk; UNP has ~35% cyclical revenue exposure that
    can decline 8-12% in a genuine recession
  • STB open-access proposals ("reciprocal switching") resurface periodically;
    a mandatory open-access mandate would structurally impair pricing power and
    the regulated-monopoly premium that underpins the valuation framework
  • PSR service quality tension — pushing harder on train length and velocity can
    degrade service reliability; customers diverting to BNSF or truck is the
    historical PSR downside risk when efficiency is pursued too aggressively

  WHAT MAKES THIS AN ACCUMULATE RATHER THAN MERELY A WATCHLIST:
  • Ratio B of 0.90× — meaningfully tilted in the investor's favor — for a
    permanent infrastructure duopoly whose franchise genuinely cannot be replicated
    is an attractive accumulation point; you're getting the toll road at a discount
    to what it should be worth at any reasonable long-term valuation framework
  • The conservative floor case (multiple flat at 20x, no PSR acceleration) already
    generates a positive 2-year return — the dividend alone (~2.2%) provides a
    meaningful cushion even if PSR execution disappoints modestly
  • The EPP gap (+82.4%) and the network's replacement-cost value (>$300B) mean
    the downside here is "underperform during a recession," not "permanent capital
    impairment" — the franchise persists through any macro cycle

  POSITION SIZING GUIDANCE:
  • ACCUMULATE — build a position steadily here; add more aggressively on any
    pullback below $225-230 (where Ratio B would approach BUY territory and
    the combined yield + EPS compounding would become compelling on any 3-5yr view)
  • Watch for: (1) quarterly OR progress — the key execution signal; (2) USMCA
    cross-border volumes and automotive near-shoring indicators; (3) STB regulatory
    developments; (4) any coal-retirement acceleration that tests the coal-decline
    management thesis
""")

    print(SEP)
    print(f"""
SUMMARY: UNP ◎ ACCUMULATE — Ratio B 0.90× (22.6% downside / 25.0% upside). A \
PERMANENT WESTERN-US RAIL DUOPOLY COMPOUNDING QUIETLY BEHIND AN OPERATING-RATIO \
TRANSFORMATION: trading at $248.00 (52-wk range $214-272, roughly a third up the \
range — the PSR-execution "show me" discount meeting a franchise whose infrastructure \
moat is permanent) on 32,000 miles of irreplaceable western-US rail network serving \
8 of the 10 largest western cities. PRICING POWER IS STRUCTURAL: revenue per carload \
grows 3-5%/yr regardless of volume through cycles — a regulated-duopoly toll on the \
movement of bulk commodities, industrial goods, intermodal containers, and automotive \
products across the most economically productive geography in the US. PSR IN PROGRESS: \
CEO Jim Vena (ex-CN Railway) targeting OR from 64.5% toward 60%; every 100bps = \
~$240M EBITDA at current scale. USMCA SECULAR TAILWIND: UNP's Mexico gateway \
routes (Laredo/Eagle Pass/El Paso) position it as the essential carrier for the \
manufacturing near-shoring from Asia to Mexico — cross-border automotive/industrial \
volumes growing double-digits; early innings of a multi-decade trend. CAPITAL RETURNS: \
$4-4.5B/yr buybacks (share count ~1.32B → sub-1.20B by 2028), 16-year consecutive \
dividend growth streak ($5.36/yr, ~2.2% yield), FCF ~$6.8-7.2B. Coal secular decline \
(~10-11% revenue, -6%/yr vol) is manageable and priced in. Net debt ~$25B (IG; \
asset-backed against >$300B replacement-cost network). Consensus 'Buy' (~20 of 31 \
analysts), PT ~$272 (range $235-320). Conservative 2yr (no PSR re-rate, multiple \
flat at 20x): EPS $12.30 x 20x + $10.72 div = $257.72 -> +3.9% floor — BULL/XBULL \
require PSR hitting 60% OR target and USMCA volumes inflecting. THE TOLL ROAD YOU \
CANNOT BUILD: accumulate steadily here; add on weakness toward $225-230. Bear $192 · \
Base $248 · Bull $310 · XBull $370."""
    )

    print(f"SIGNAL: {SIGNAL_TEXT} (permanent western-US rail duopoly — 32,000-mile irreplaceable network — with structural pricing power, PSR operating-ratio improvement underway, and USMCA near-shoring as a multi-decade secular tailwind) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
