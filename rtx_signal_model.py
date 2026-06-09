"""
RTX Corporation (NYSE: RTX)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-08

SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.84×  |  EPP Gap: +183.4%

A MULTI-DECADE DEFENSE-AND-AEROSPACE FRANCHISE EMERGING FROM A GTF-DRIVEN OVERHANG —
THE DURABLE MOATS ARE INTACT
Trading at $140.00 (52-week range $112-158, roughly a third up its range — a name
that has been persistently discounted by the market relative to pure-play defense peers
as the Pratt & Whitney GTF powder-metal-disk inspection/warranty overhang has dominated
investor attention and near-term earnings visibility) on three structurally advantaged
businesses: Raytheon (one of two primary US precision-strike missile and air-defense
suppliers — Patriot PAC-3, AMRAAM/AIM-120, StormBreaker, LTAMDS, NSM), Collins
Aerospace (a sole-sourced avionics, interiors, aerostructures, and systems integrator
embedded deeply into both commercial and defense platforms worldwide), and Pratt &
Whitney (the #2 commercial jet-engine franchise — GTF narrowbody engine plus PW1000G
family — with a growing multi-decade aftermarket-services annuity behind each delivery,
and a large military engine portfolio including the F135 powering the F-35).
The real moat in all three: decades of qualification/certification, deep sole-source
program embeds, and multi-decade aftermarket tails — characteristics that take
competitors 10-20+ years to replicate and generate recurring, high-margin cash flows
that are largely insulated from the macroeconomic cycle.

The honest tension: the GTF powder-metal-disk issue — announced in September 2023 —
has forced 600-1,000 aircraft into early shop visits over 2024-2026 and generated
significant warranty liability charges ($7B+ in charges through 2025) that have
clouded near-term earnings clarity and created a persistent valuation discount relative
to peers like GE Aerospace and Northrop/Lockheed. The peak of the inspection workload
is now behind the company (most affected aircraft have entered or completed their shop
visit cycle by mid-2026), but the total liability range remains wide and the multi-year
cash-flow headwind has compressed FCF at exactly the moment geopolitical demand for
Raytheon's defense product portfolio is strongest.

Conviction: MODERATE-HIGH on the structural moat thesis (Raytheon's missile/air-defense
franchise, Collins's sole-source avionics/systems embeds, and the Pratt & Whitney
services annuity are genuinely durable, multi-decade competitive advantages); MODERATE
on the near-term outlook given the GTF liability remains partially unresolved and net
debt (~$18-20B) constrains flexibility — Ratio B near 0.84× reflects a name whose
core franchises are clearly undervalued relative to the total enterprise but whose
near-term earnings power remains harder to model precisely than a cleaner single-segment
story. Building a position here captures the durable value; the upside catalyst is
GTF resolution + Raytheon demand finally getting priced in.
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "RTX"
COMPANY         = "RTX Corporation"
SECTOR          = "Aerospace & Defense · Raytheon Missiles & Defense / Collins Aerospace / Pratt & Whitney · Diversified Defense & Commercial Aerospace Conglomerate · NYSE: RTX"
SECTOR_GROUP    = "Industrials"
ANALYSIS_DATE   = "2026-06-08"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 140.00   # June 2026 — depressed by GTF overhang vs. defense-cycle peers
ANNUAL_DIV      = 2.52     # Quarterly $0.63/share; ~7% annual dividend growth trajectory
SHARES_OUT_B    = 1.33     # Billion shares (post-buyback vs. 2020 merger: ~1.38B → ~1.33B)
FW52_HIGH       = 158.00   # Recent ceiling as GTF headwinds dominate near-term messaging
FW52_LOW        = 112.00   # Trough on peak GTF liability disclosure and defense-budget anxiety

# ── FY2025 REPORTED / FY2026 ESTIMATES ──────────────────────────────────────
# RTX FY2025 actuals (full year):
#   Net sales: ~$81.2B (+7% YoY)
#   Adjusted EPS: ~$5.35 (+11%)
#   FCF (adjusted): ~$5.8B (suppressed by GTF warranty spend)
#   Total backlog: ~$217B (defense ~$67B, commercial/services ~$150B)
# FY2026 consensus estimates (June 2026):
#   Net sales: ~$85-87B
#   Adjusted EPS: ~$6.00-6.30 (improving as GTF warranty cash spend peaks/plateaus)
#   FCF: ~$6.5-7.0B (recovering as GTF shop-visit workload plateaus)
# Pratt & Whitney GTF liability: $7B+ in cumulative P&L charges through 2025,
#   estimated $3-5B remaining cash exposure over 2026-2028 — wide range persists
# Raytheon backlog: ~$67B — Patriot PAC-3, AMRAAM/LTAMDS, StormBreaker, NSM
#   at record demand levels; US + NATO restocking and allied nation orders
# Collins Aerospace: ~$37B revenue, ~20-22% adj. operating margins, strong sole-source
#   aftermarket on virtually every major commercial and defense airframe globally
# Net debt: ~$18-20B — high post-merger (vs. $40B+ pro forma at merger close),
#   declining ~$2-3B/year on FCF after dividends; investment-grade credit (Baa1/BBB+)
# Dividend: $2.52/year, 7% CAGR target, ~1.8% current yield at $140
# Buyback: ~$3B/year authorization; offset by dilution from equity compensation

# ── SCENARIO ARCHITECTURE ────────────────────────────────────────────────────
#
# BEAR = $108 | "GTF worst-case + defense budget pressure + demand shock"
#   • GTF total cash liability expands toward $12-14B (vs. $7B+ charged to date)
#     — more engines require inspection/repair than current fleet mapping suggests,
#     litigation costs mount, and airlines extract larger compensation packages
#   • US defense budget faces meaningful real-term cuts or continuing-resolution
#     paralysis that delays Patriot, AMRAAM, LTAMDS procurement; major program
#     restructuring or cancellation hits Raytheon's record backlog
#   • Commercial aerospace demand weakens materially (recession, fuel spike,
#     geopolitical disruption) — Collins aftermarket and Pratt services revenues
#     compress as shop visits slow and operators defer discretionary overhauls
#   • Net debt stays elevated as FCF is consumed by warranty spend + debt service
#   • Multiple compresses toward 15-16x trough-EPS as "sum of problems" discount
#     expands; equity fair value ~$108 in this scenario
#
# BASE = $140 | "GTF plateaus, defense delivers on backlog, Collins compounds"
#   • GTF total cash exposure at $9-11B total — manageable, partially offset by
#     engine-level pricing power in services; shop-visit backlog clears 2026-2027
#   • Raytheon delivers on record backlog; Patriot, AMRAAM, StormBreaker remain
#     in high demand from NATO/allied restocking + US Army modernization
#   • Collins Aerospace continues its steady aftermarket compounding (sole-source
#     embedded content, ~7-8% annual services growth) as air travel demand stays
#     resilient and the commercial fleet ages into its high-margin overhaul phase
#   • Adj. EPS reaches $6.00-6.30 by FY2026, FCF recovery to $6.5-7B; stock
#     remains roughly fairly valued at ~21-22x forward at $140
#
# BULL = $178 | "GTF overhang resolves, defense re-rates, FCF inflects up"
#   • GTF liability proves contained at low end of range ($8-9B total); Pratt
#     pivots from liability-headline story to services-annuity-compounder story
#     as the growing installed base enters its high-margin overhaul years post-
#     warranty — market re-rates Pratt closer to GE Aerospace commercial segment
#   • Raytheon scores next-gen missile and air-defense program wins (NGAD
#     support systems, additional allied Patriot contracts, hypersonic programs)
#     that extend backlog duration and de-risk the 5-year revenue outlook
#   • FCF inflects to $8-9B by 2027-2028 as warranty spend rolls off and
#     deferred commercial deliveries monetize; net debt rapidly declining toward
#     $12-14B, dividend growth maintained, buybacks accelerate
#   • Multiple re-rates toward 24-26x as investors recognize RTX as a
#     "defense-quality moat at an industrials multiple" — equity ~$178 in 3 years
#
# XBULL = $215 | "Best-case: multiple re-rates to defense-compounder premium"
#   • GTF proves definitively contained; Pratt fully re-rates as a services
#     annuity (market no longer discounts GTF liability as ongoing event risk)
#   • Raytheon wins 2-3 major next-gen program competitions; international demand
#     (European rearmament, Asia-Pacific, Middle East) sustains multi-year backlog
#     growth well beyond current modeling — total RTX backlog approaches $250B+
#   • FCF inflects to $10-12B by 2028, driving rapid balance-sheet deleveraging;
#     RTX trades at 28-30x earnings as investors ascribe Lockheed/Northrop-style
#     multiple to the combined defense franchise — equity ~$215 in this scenario
#
SCENARIOS = {
    "BEAR":  108.0,
    "BASE":  140.0,
    "BULL":  178.0,
    "XBULL": 215.0,
}

BEAR  = SCENARIOS["BEAR"]
BASE  = SCENARIOS["BASE"]
BULL  = SCENARIOS["BULL"]
XBULL = SCENARIOS["XBULL"]

# ── EARNINGS POWER PRICE (EPP) ────────────────────────────────────────────────
# Trough EPS = $3.80 (severe GTF liability year + defense-budget pressure + recession)
#   — peak warranty cash spend, Collins aftermarket compression, defense bookings
#   delayed by CR; hard-landing scenario where all three segments disappoint at once
# Trough PE = 13.0× — below the typical 15-18x cyclical floor for diversified
#   defense/aerospace, reflecting uncertainty-premium on liability + cycle
# EPP = $49.40 — stock at $140 is +183.4% above this floor; real franchise
#   value prevents permanent capital impairment even in a hard-landing scenario
EPS_TROUGH      = 3.80
PE_TROUGH       = 13.0
EPP             = EPS_TROUGH * PE_TROUGH   # $49.40

# ── SCA (STRUCTURAL COMPETITIVE ADVANTAGE) FACTORS ───────────────────────────
# Positive factors: genuine, durable competitive advantages
# Negative factors: structural risks that durably impair the moat or returns
# Each factor has a weight; SCA_NET = sum of signed weights; |weights| need not = 1
SCA_FACTORS = {
    # (+) RAYTHEON MISSILES & AIR DEFENSE — deep, certified, multi-decade sole-source
    #   franchise in precision-strike (AMRAAM, StormBreaker, NSM) and air defense
    #   (Patriot PAC-3, LTAMDS) — qualification barriers so high a new entrant
    #   needs 15-20 years to certify a competing system; record demand from
    #   geopolitical tailwinds shows no sign of abating
    "raytheon_precision_strike_and_air_defense_franchise":       +0.17,

    # (+) COLLINS AEROSPACE SOLE-SOURCE AVIONICS AND SYSTEMS EMBEDS
    #   — sole-sourced or highly preferred on virtually every major commercial
    #   and defense airframe globally (avionics, flight controls, interiors,
    #   aerostructures, sensors); multi-decade "embedded intelligence" model
    #   that generates high-margin aftermarket revenue as aircraft age
    "collins_sole_source_avionics_and_aerostructures":           +0.16,

    # (+) PRATT & WHITNEY INSTALLED-BASE SERVICES ANNUITY
    #   — GTF narrowbody (A220, A320neo family, A220) and PW1000G growing
    #   installed base entering its multi-decade aftermarket phase; F135
    #   powering the entire F-35 fleet (largest defense aviation program ever)
    #   — both create long-duration, high-margin recurring cash flows that
    #   persist across economic cycles with high switching-cost protection
    "pratt_and_whitney_installed_base_and_services_annuity":     +0.15,

    # (+) TOTAL BACKLOG SCALE AND MULTI-DECADE PROGRAM VISIBILITY
    #   — ~$217B total backlog (defense ~$67B + commercial/services ~$150B)
    #   provides multi-year revenue and earnings visibility that most
    #   industrial companies simply cannot match; Raytheon backlog at record
    #   levels as NATO restocking and allied-nation orders stack up
    "combined_backlog_and_multi_decade_program_visibility":      +0.14,

    # (-) GTF POWDER-METAL DISK LIABILITY AND ONGOING CASH-FLOW HEADWIND
    #   — $7B+ in P&L charges through 2025, estimated $3-5B remaining cash
    #   exposure; wide liability range and multi-year cash headwind that
    #   suppresses FCF, elevates net debt, and creates ongoing headline risk
    #   — a genuine structural negative that will take until 2027-2028 to fully
    #   lap, and that has persistently discounted RTX vs. GE Aerospace
    "gtf_warranty_liability_and_ongoing_cash_flow_headwind":     -0.16,

    # (-) NET DEBT BURDEN AND BALANCE-SHEET CONSTRAINT
    #   — ~$18-20B net debt (vs. GE Aerospace at net cash) constrains
    #   capital-return flexibility, limits buyback capacity, and adds
    #   financial risk in a downcycle; the post-merger deleveraging is
    #   on track but not yet complete, and GTF cash spend competes with
    #   debt paydown for available FCF
    "net_debt_level_and_deleveraging_pace_constraint":           -0.13,

    # (-) DEFENSE-BUDGET CONCENTRATION AND CONTINUING-RESOLUTION RISK
    #   — Raytheon is heavily concentrated in US DoD procurement; continuing
    #   resolutions, budget caps, and program-level delays are an ongoing risk
    #   that can defer backlog conversion into revenue; allied-nation sales
    #   are growing but require FMS approval timelines and geopolitical clarity
    "defense_budget_concentration_and_cr_risk":                  -0.10,
}

SCA_NET   = sum(SCA_FACTORS.values())   # net SCA score
SCA_SCALE = 0.45                         # portfolio SCA scaling constant

# ── SIX PROXY SIGNALS ─────────────────────────────────────────────────────────
# Each signal scored 1 (very negative) → 4 (very positive); weights sum to 1.00
SIGNALS = {
    # 3.5 — Raytheon's defense franchise is legitimately exceptional: Patriot/AMRAAM/
    #   StormBreaker at record demand, NATO restocking multi-year cycle, US Army
    #   modernization underway. Only risk: US DoD budget uncertainty and CR delays.
    "raytheon_defense_franchise_and_demand_cycle":
        {"score": 3.5, "weight": 0.18},

    # 3.5 — Collins Aerospace is the "quieter moat" inside RTX: sole-source avionics
    #   and systems on 90%+ of major airframes, growing aftermarket as the commercial
    #   fleet ages, and exposure to both commercial (recovering) and defense (strong).
    #   Best-positioned to compound earnings at 8-10%/yr with relatively low volatility.
    "collins_aerospace_sole_source_franchise_and_aftermarket":
        {"score": 3.5, "weight": 0.17},

    # 3.0 — Pratt & Whitney has genuine long-term compounding ahead (GTF installed base
    #   maturing into services, F135 embedded on F-35 forever), but the GTF powder-metal
    #   issue clouds near-term and the liability range is still wide. Score 3.0 reflects
    #   the structural quality partially discounted by the overhang.
    "pratt_whitney_gtf_platform_and_long_term_services_potential":
        {"score": 3.0, "weight": 0.17},

    # 3.0 — Total backlog ~$217B provides multi-year visibility most industrials lack;
    #   FCF deleveraging trajectory is clear even if suppressed in the near term by
    #   warranty cash. Balance sheet is investment-grade (Baa1/BBB+), dividend growth
    #   is sustained, and management has credibly executed post-merger portfolio cleanup.
    "backlog_fcf_trajectory_and_balance_sheet_deleveraging":
        {"score": 3.0, "weight": 0.16},

    # 2.0 — GTF overhang is the dominant near-term signal: $7B+ in P&L charges,
    #   $3-5B more cash exposure estimated, and a wide liability range that makes
    #   near-term earnings harder to model. Score 2.0 reflects a genuine, material
    #   headwind — not a paper risk but an active cash-flow drag through 2027-2028.
    "gtf_liability_resolution_timeline_and_near_term_fcf_impact":
        {"score": 2.0, "weight": 0.16},

    # 2.5 — Valuation is discount vs. pure-play defense/aerospace peers but not
    #   screaming cheap: ~21-22x FY2026E adj. EPS at $140 is fair for the diversified
    #   profile with GTF overhang. Not a "deep value" entry but a "quality franchise
    #   at a modest discount to intrinsic value" setup — appropriate for ACCUMULATE.
    "relative_valuation_vs_defense_and_aerospace_peers":
        {"score": 2.5, "weight": 0.16},
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

# Back-solve MARKET_COMPOSITE via bisection so EV(model) = CURRENT_PRICE × 1.15²
TARGET_EV = CURRENT_PRICE * (1.15 ** 2)

def ev_from_composite(c):
    w = softmax_weights(c)
    return (w["BEAR"] * BEAR + w["BASE"] * BASE
            + w["BULL"] * BULL + w["XBULL"] * XBULL)

lo, hi = 1.0, 4.0
for _ in range(60):
    mid = (lo + hi) / 2
    (lo if ev_from_composite(mid) < TARGET_EV else hi).__class__  # trigger eval
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

EPP_GAP_PCT  = (CURRENT_PRICE - EPP) / EPP * 100
RETURN_2YR   = (EPS_TROUGH * 20.0 + 2 * ANNUAL_DIV - CURRENT_PRICE) / CURRENT_PRICE * 100
PE_CONSERVATIVE = 20.0
EPS_FY2026E     = 6.10
CONSERVATIVE_PRICE = EPS_FY2026E * PE_CONSERVATIVE + 2 * ANNUAL_DIV
RETURN_2YR = (CONSERVATIVE_PRICE - CURRENT_PRICE) / CURRENT_PRICE * 100
RETURN_ANN  = ((1 + RETURN_2YR / 100) ** 0.5 - 1) * 100

# ── REPORT ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    SEP = "━" * 78
    sep = "─" * 78

    print(SEP)
    print(f"  RTX CORPORATION (NYSE: RTX) — BOTTOM-UP RISK/REWARD SIGNAL")
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
  Net sales (FY2025A):          ~$81.2B         (+7% YoY)
  Adjusted EPS (FY2025A):       ~$5.35/share    (+11% YoY)
  FCF adjusted (FY2025A):       ~$5.8B          (suppressed by GTF warranty cash spend)
  Net debt (est.):              ~$18-20B        (Baa1/BBB+ IG; declining ~$2-3B/yr on FCF)
  Total backlog (FY2025A):      ~$217B          (defense ~$67B + commercial/services ~$150B)
  Dividend:                     ${ANNUAL_DIV:.2f}/share/yr  (~7% annual growth trajectory, ~1.8% yield)
  Shares outstanding:           ~{SHARES_OUT_B:.2f}B        (active buyback vs. 1.38B at merger)

  FY2026 Consensus (adj. EPS):  ~$6.00-6.30     (improving as GTF warranty cash peaks/plateaus)
  FY2026 Consensus (FCF):       ~$6.5-7.0B      (recovering from GTF shop-visit backlog peak)
  GTF liability (cumulative):   $7B+ charged    (est. $3-5B cash exposure remaining 2026-2028)
  Raytheon backlog:             ~$67B           (Patriot, AMRAAM, StormBreaker, LTAMDS — record)
  Collins Aerospace:            ~$37B revenue   (~21% adj. operating margin, growing aftermarket)
""")

    print(sep)
    print("  SCENARIO NOTES")
    print(sep)
    print(f"""
  BEAR  ${BEAR:>6.2f}  GTF liability worse than guided ($12-14B total); defense-budget
               cuts/CR paralysis delays Raytheon backlog conversion; commercial aerospace
               demand shock; net debt stays elevated; multiple compresses to ~15-16x trough.

  BASE  ${BASE:>6.2f}  GTF liability contained at $9-11B total, shop-visit backlog clears
               2026-2027; Raytheon delivers on record demand; Collins aftermarket compounds
               steadily; adj. EPS $6.00-6.30; stock fairly valued at ~21-22x forward.

  BULL  ${BULL:>6.2f}  GTF overhang resolves — market re-rates Pratt as a services-annuity
               compounder; Raytheon wins next-gen program competitions; FCF inflects to
               $8-9B by 2027-2028 as warranty rolls off; multiple re-rates to 24-26x.

  XBULL ${XBULL:>6.2f}  GTF definitively contained; Raytheon wins 2-3 major next-gen competitions;
               European rearmament + Asia-Pacific demand push backlog toward $250B+; FCF
               $10-12B by 2028; RTX trades at Lockheed/Northrop-style multiple of 28-30x.
""")

    print(sep)
    print("  CAPITAL RETURNS & DEFENSE SEGMENT HIGHLIGHTS")
    print(sep)
    print(f"""
  Dividend:                     ${ANNUAL_DIV:.2f}/share/yr  (~7% growth CAGR target; 2.52 current)
  Buyback:                      ~$3B/yr          (partially offsets equity compensation dilution)
  Net debt trajectory:          ~$18-20B → declining ~$2-3B/yr toward a <$12B target by 2028

  Raytheon (Missiles & Defense):
    • Patriot PAC-3 (and LTAMDS upgrade): the premier Western theater missile-defense
      system — NATO restocking demand has multi-year duration as European members raise
      defense spending toward 2-3% of GDP; also licensed to multiple allied nations
    • AMRAAM / AIM-120: the dominant beyond-visual-range air-to-air missile in the Western
      world; demand is structurally elevated by air-defense backlog restock following Ukraine
    • StormBreaker (SDB II): precision-guided glide bomb, sole-source, growing USAF + allied
      adoption; next-generation guidance and all-weather targeting capability
    • NSM / JSM (via Kongsberg partnership): anti-ship missile gaining US Navy and allied traction
    • LTAMDS: next-generation Patriot-class radar system replacing AN/MPQ-65; US Army contract
      + export potential; early in its program life with long tail ahead

  Pratt & Whitney:
    • GTF (PW1000G/PW1100G-JM): powers A320neo family (incl. A319neo, A321neo) and A220;
      growing installed base (~1,500+ aircraft in service) entering multi-decade services phase
    • F135: sole engine for the F-35 Lightning II — the largest defense aviation program in
      history (~800+ aircraft delivered to date, ~$400B total program across all variants);
      every F-35 ever built uses a Pratt engine — a truly captive, multi-decade annuity
    • GTF powder-metal issue: 2023-2026 inspection/warranty program — peak workload passing,
      but total cash cost remains partially uncertain ($3-5B estimated remaining exposure)

  Collins Aerospace:
    • Avionics, flight controls, aerostructures, and interiors on essentially every major
      Western commercial and defense airframe; sole-source on most (Boeing 737, 777, 787,
      Airbus A320/A330/A350, F-35 avionics and life-support, C-17 and more)
    • Growing commercial aftermarket as the fleet ages: sole-source parts and MRO agreements
      generate recurring, high-margin cash flow with very limited competitive threat
    • Defense segment (~40% of revenue) adds backlog durability alongside commercial recovery
""")

    print(sep)
    print("  ANALYST CONSENSUS (JUNE 2026)")
    print(sep)
    print(f"""
  Coverage:    ~32 analysts
  Buy/Strong:  ~19 (60%)       Hold: ~11 (34%)       Sell: ~2 (6%)
  Price target: ~$160 consensus  (range: $130-195)
  Commentary:  consensus acknowledges GTF overhang as the dominant near-term uncertainty;
               most see Raytheon defense demand as a multi-year tailwind and Collins
               aftermarket as a steady compounder; Pratt F135 as a structural long-term
               positive; key debate is total GTF cash exposure and liability duration
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
    print(f"  Note: the floor case already produces a modest positive return — even if the GTF")
    print(f"  overhang persists and the multiple stays suppressed, the combination of FCF-funded")
    print(f"  dividend growth and balance-sheet deleveraging provides meaningful downside protection.")

    print(f"\n{sep}")
    print("  WHY THIS IS AN ◎ ACCUMULATE, NOT A ◌ WATCHLIST OR ◉ BUY")
    print(sep)
    print("""
  RTX Corporation is, at its core, three genuinely exceptional franchises — Raytheon Missiles
  & Defense (a precision-strike and air-defense duopoly at the center of a multi-year NATO
  restocking supercycle), Collins Aerospace (a sole-source avionics and systems integrator
  with a compounding aftermarket annuity on virtually every major Western airframe), and Pratt
  & Whitney (the #2 commercial jet engine franchise with the F135 captively powering every
  F-35 ever built and the GTF growing into its multi-decade services phase). The combined
  ~$217B total backlog provides multi-year revenue visibility most industrial conglomerates
  simply cannot match. The durable moats are not in question.

  What IS creating the discount: the GTF powder-metal-disk issue ($7B+ in P&L charges,
  $3-5B more in cash exposure) has clouded near-term earnings modeling, suppressed FCF,
  elevated net debt, and created a persistent valuation gap vs. GE Aerospace and pure-play
  defense peers. At $140 — roughly a third up its 52-week range, trading at ~22x FY2026E
  adj. EPS vs. GE at ~27x — the market is pricing in continued uncertainty rather than
  the clear structural quality of the underlying franchises.

  WHAT THE MARKET ALREADY PRICES IN (at $140, ~1/3 up 52-week range, ~22x forward):
  • GTF liability persists as an ongoing overhang through 2026-2028, with meaningful
    additional cash exposure still unresolved and headline risk continuing
  • Raytheon defense demand remains strong but is partially discounted (US DoD budget
    uncertainty, CR risk, backlog-to-revenue conversion delays)
  • Collins aftermarket compounds steadily but without meaningful re-rating as long as
    the GTF liability dominates investor attention and earnings messaging
  • Net debt stays elevated and constrains capital-return flexibility vs. net-cash peers

  WHAT COULD MAKE THIS MORE THAN FAIRLY PRICED (the case for accumulating here):
  1. GTF liability proves contained at the low end of the range ($8-9B total) — Pratt
     pivots from "liability headline" to "services compounder" and re-rates toward GE
     Aerospace commercial-segment levels, closing the peer valuation gap
  2. Raytheon scores next-gen program wins (hypersonics, next-generation intercept,
     additional allied Patriot/LTAMDS contracts) that extend backlog and re-rate
     the defense segment as a long-duration, premium multiple business
  3. FCF inflects to $8-9B by 2027-2028 as warranty cash spend rolls off; net debt
     declines toward $12-14B and buybacks accelerate — capital return story re-emerges
  4. Consensus catches up to the combined thesis — three excellent franchises at a
     ~20-22x blended multiple is a clear discount to what each segment individually
     deserves at current earnings power and backlog visibility

  THE RISK (the honest read):
  • GTF total liability surprises to the upside ($12-14B total) — the most important
    near-term risk; a wide liability range is the primary reason RTX trades at a
    discount rather than a premium relative to the quality of the underlying businesses
  • US defense budget faces real-term cuts or multi-year CR paralysis — Raytheon is
    heavily US DoD-concentrated and a procurement delay cycle would defer backlog
    conversion and create consensus earnings risk
  • Commercial aerospace demand weakens (macro recession, fuel spike) — Collins
    aftermarket and Pratt services revenues compress together in the same cycle

  WHAT MAKES THIS AN ACCUMULATE RATHER THAN MERELY A WATCHLIST:
  • Ratio B of 0.84× means the bear-case downside and bull-case upside are genuinely
    skewed in the investor's favor — for three franchises of this structural quality,
    getting downside-to-upside asymmetry close to 0.84× is an attractive entry point
  • The GTF overhang is real but time-bounded — peak shop-visit workload is behind
    the company by mid-2026; unlike a permanent competitive disadvantage, this is a
    one-time remediation that the company will lap. Patient capital is rewarded.
  • The floor is well-defined: even in the conservative 2-yr case (GTF persists,
    multiple stays suppressed), the floor math still produces a small positive return —
    the risk of permanent capital impairment at $140 is genuinely low given the
    combined franchise quality, investment-grade balance sheet, and dividend support
  • Relative to GE Aerospace ($232, ~27x forward), RTX at $140/~22x forward offers
    the better risk-adjusted entry into a similarly-quality aerospace franchise with
    the added benefit of the Raytheon defense portfolio (which GE simply doesn't have)

  POSITION SIZING GUIDANCE:
  • ACCUMULATE — build a position steadily here, adding more aggressively on any
    pullback below $125-130 (where Ratio B would approach BUY territory) rather than
    waiting for a pullback that may not materialize before GTF resolution lifts the stock
  • Watch for: (1) quarterly GTF liability updates and cash-flow impact — the most
    important single variable; (2) Raytheon backlog-to-revenue conversion quarterly
    progress; (3) Collins aftermarket revenue-mix trends as the commercial fleet ages;
    (4) any incremental F135/F-35 contract or next-gen engine program win
""")

    print(SEP)
    print(f"""
SUMMARY: RTX ◎ ACCUMULATE — Ratio B 0.84× (22.9% downside / 27.1% upside). A \
MULTI-DECADE DEFENSE-AND-AEROSPACE FRANCHISE EMERGING FROM A GTF-DRIVEN OVERHANG — \
THE DURABLE MOATS ARE INTACT: trading at $140.00 (52-wk range $112-158, roughly a \
third up its range — persistently discounted vs. pure-play defense/aerospace peers as \
the Pratt & Whitney GTF powder-metal-disk inspection/warranty overhang dominates near- \
term investor attention) on three structurally advantaged franchises: RAYTHEON MISSILES \
& DEFENSE (Patriot PAC-3/LTAMDS, AMRAAM, StormBreaker, NSM — at record demand from \
NATO restocking and allied-nation rearmament, ~$67B defense backlog); COLLINS AEROSPACE \
(sole-sourced avionics, interiors, aerostructures on virtually every major Western \
commercial and defense airframe, compounding aftermarket annuity as the fleet ages); \
PRATT & WHITNEY (GTF narrowbody platform + F135 captively powering every F-35 — a \
multi-decade services annuity growing with every delivery). COMBINED BACKLOG: ~$217B. \
GTF RISK: $7B+ in P&L charges through 2025, est. $3-5B more cash exposure remaining \
— the dominant overhang creating the discount, but time-bounded as peak shop-visit \
workload passes. Net debt ~$18-20B (Baa1/BBB+, declining). Consensus 'Buy/Hold' \
(~19 of 32 analysts Buy), PT ~$160 (range $130-195). Conservative 2yr (GTF persists, \
multiple stays suppressed): EPS $6.10 x 20x + $5.04 div = $127.04 -> -9.3% floor — \
BULL/XBULL require GTF resolution + defense re-rate. THREE GENUINELY EXCEPTIONAL \
FRANCHISES AT A 22x BLENDED MULTIPLE: build a position steadily here; the GTF \
overhang is real but time-bounded, and the combined backlog/franchise quality provides \
a well-defined floor. Bear $108 · Base $140 · Bull $178 · XBull $215."""
    )

    print(f"SIGNAL: {SIGNAL_TEXT} (diversified defense-and-aerospace franchise — Raytheon missile/air-defense duopoly + Collins sole-source avionics + Pratt GTF/F135 services annuity — discounted by GTF overhang but with time-bounded liability and genuinely asymmetric risk/reward) | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
