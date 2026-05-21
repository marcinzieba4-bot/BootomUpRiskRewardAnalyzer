"""
Broadcom Inc. (AVGO) — BottomUp Risk/Reward Signal Model
Hyperscaler custom AI silicon (XPU) + VMware infrastructure software;
~$75B revenue; #1 custom ASIC, #1 hyperscaler ethernet switching, #1 server virtualisation
Three-Part Publication Format

FISCAL YEAR NOTE: Broadcom's fiscal year ends in late October / early November.
  FY2023 = Nov 2022 – Oct 2023  (pre-VMware close; pre-AI-XPU ramp; non-GAAP EPS ~$4.27 post-split)
  FY2024 = Nov 2023 – Nov 2024  (VMware closed Nov 22 2023; partial synergy yr; EPS ~$4.86)
  FY2025 = Nov 2024 – Nov 2025  (first full VMware yr; AI XPU ramp yr 1; EPS $6.82)
  FY2026 = Nov 2025 – Nov 2026  (current; Q1 actual EPS $2.05; Q2 rev guide $22B +47% YoY)
  FY2027 = Nov 2026 – Nov 2027  (2-year exit horizon; consensus non-GAAP EPS ~$12.72)

STOCK SPLIT NOTE: 10-for-1 split effective July 15, 2024.
  All pre-split EPS figures divided by 10 throughout this model.
  Historical price references quoted on post-split basis.
"""
import math

# ── LIVE PRICE (fetched via web search, 2026-05-21) ──────────────────────────
CURRENT_PRICE = 417.76   # AVGO — web search (intraday), NASDAQ, 2026-05-21

# ── EPP FLOOR CALIBRATION ────────────────────────────────────────────────────
# FY2023 (Nov 2022 – Oct 2023): last full year before VMware close (Nov 22 2023)
# and before AI XPU revenue inflection. Quarterly non-GAAP EPS (post-split):
#   Q1 FY2023 $10.33/10=$1.033 | Q2 $10.32/10=$1.032 | Q3 $10.54/10=$1.054
#   Q4 FY2023 ~$11.51/10=$1.151  →  FY2023 total ~$4.27
# Stock trough: Oct 2022 bear-market low ~$440 pre-split = $44 post-split
# (high-rate environment; pure semi multiple; no VMware software quality premium)
# EPP validation: $4.27 trough EPS x 16x (above 10-13x observed bear-mkt low;
# VMware software recurring revenue warrants franchise premium) -> EPP_NOW uses EPS_NOW
EPS_TROUGH       = 4.27   # FY2023 non-GAAP diluted post-split; pre-VMware/pre-XPU inflection
EPS_TROUGH_YEAR  = 2023
EPS_TROUGH_PRICE = 44.0   # AVGO post-split equiv; Oct 2022 bear-mkt low (~$440 pre-split / 10)
EPP_MIN_PE       = 16     # min-viable trough PE; VMware software moat above observed 10-13x floor

# ── CURRENT FUNDAMENTALS ─────────────────────────────────────────────────────
EPS_NOW           = 6.82   # FY2025 non-GAAP diluted (Q1 $1.60 + Q2 $1.58 + Q3 $1.69 + Q4 $1.95)
EPS_FWD_CONSENSUS = 9.39   # FY2026E consensus; Q1 actual $2.05 (beat $1.88); Q2 guide implies ~$2.50+
CONS_EPS_2YR      = 12.72  # FY2027E consensus (~42 analysts; $12.72 mean)
CONS_EPS_CAGR     = 0.366  # ~36.6%/yr (FY2025 $6.82 -> FY2027E $12.72); AI XPU + VMware compounding
CONS_EXIT_PE      = 28     # conservative 2-yr exit P/E; semi-software hybrid; below current 32.8x FY2027E
BETA              = 1.25   # elevated; AI/semiconductor exposure; VMware software buffer vs pure semi

# ── SCENARIO TABLE ───────────────────────────────────────────────────────────
SCENARIOS = [
    ("BEAR",  "Hyperscaler AI capex pause; in-house silicon displaces XPU contracts; China restrictions expand",   7.00, 14,   98),
    ("BASE",  "XPU ramp holds with 5-6 hypers; VMware synergies reach $8.5B; AI networking stable",              12.72, 30,  382),
    ("BULL",  "AVGO wins 2+ new XPU contracts; VMware beats synergy target; AI networking share gains",           18.00, 38,  684),
    ("XBULL", "AI silicon supercycle; AVGO = #2 AI chip company; XPU TAM $150B+; exceptional EPS path",          26.00, 48, 1248),
]

# ── CROSS-READ SIGNALS ───────────────────────────────────────────────────────
CROSS_READS = [
    ("Hyperscaler AI capex  (Google+Meta+MSFT+Amazon combined annual spend, $B)", "Primary AVGO AI XPU + networking demand driver; hyper CapEx rising rapidly",   "$B",  150, 300, 500,  900, 280, 0.30),
    ("AVGO AI semiconductor revenue run rate  ($B annualised; Q x 4)",            "XPU + AI networking; Q1 FY2026 $8.4B x 4 = $33.6B; FY2026E consensus $40B+",  "$B",   15,  40,  65,  120,33.6, 0.25),
    ("VMware cloud subscription ARR growth  (%YoY; perpetual->SaaS conversion)",  "Software moat proxy; $8.5B cost synergy target FY2027; confirms recurring FCF", "%",   -5,  15,  30,   50,  20, 0.20),
    ("Custom ASIC / XPU active hyperscaler customers  (# with active tape-outs)", "Customer diversification; Google Meta Apple ByteDance + 2 others = 6",          "#",    2,   5,   8,   12,   6, 0.15),
    ("AVGO non-AI semiconductor revenue growth  (broadband/storage/wireless %)",  "Cyclical semi base; DOCSIS 4.0, enterprise storage recovery",                  "%",  -20,   5,  15,   25,   5, 0.10),
]

# ── STRUCTURAL COMPOSITE ADJUSTMENT ─────────────────────────────────────────
STRUCTURAL_FACTORS = [
    ("Custom ASIC / XPU near-monopoly  (AVGO+Marvell >95% of hyperscaler custom silicon; multi-yr locked)",  +1.2, 0.30),
    ("VMware software moat  (~50% revenue; 80%+ FCF margin; SaaS conversion = durable recurring cash flow)",  +0.9, 0.25),
    ("Hyperscaler customer concentration  (Google+Meta+Apple ~35-40% of AI revenue; execution/renewal risk)", -0.8, 0.20),
    ("Export controls / China risk  (non-AI semi ~15% China exposure; policy escalation threat)",             -0.6, 0.15),
    ("AI networking structural tailwind  (Tomahawk/Jericho: >70% hyperscaler ethernet switching share)",      +0.6, 0.10),
]

# ── EPS QUALITY DECOMPOSITION ────────────────────────────────────────────────
# EPS grew from FY2023 pre-inflection baseline $4.27 to FY2025 $6.82: +$2.55
# Two structural catalysts (VMware SaaS + AI XPU) + two cyclical components
EPS_DECOMP = [
    ("VMware subscription conversion & operating synergy  (~$8.5B cost-out target FY2027)",  0.40, True),
    ("AI custom XPU ramp  (Google TPU v5 / Meta MTIA v2; multi-year contracted programs)",   0.35, True),
    ("AI networking upgrade cycle  (Tomahawk/Jericho; hyperscaler ethernet CapEx wave)",     0.15, False),
    ("Broadband / cable / industrial semiconductor recovery  (DOCSIS 4.0 / HDD upcycle)",   0.10, False),
]

# ── IDIOSYNCRATIC vs MACRO DECOMPOSITION ─────────────────────────────────────
IDIO = {
    "idio_pct":  50,
    "macro_pct": 50,
    "beta":      1.25,
    "drivers": [
        ("Custom XPU design wins & hyperscaler contract depth",        "IDIO",  0.20, "Unique 2-3yr design-to-tape-out moat; locked multi-yr production commitments"),
        ("VMware SaaS conversion execution & cost synergy capture",    "IDIO",  0.15, "Integration track; $8.5B synergy by FY2027; Q1 FY2026 on schedule"),
        ("AI networking switching position  (Tomahawk vs InfiniBand)", "IDIO",  0.15, "Ethernet at 100K+ GPU pod scale; AVGO leads ethernet hyperscaler fabric"),
        ("Semiconductor sector capex & inventory cycle",               "MACRO", 0.20, "WFE / end-market demand cycles; non-AI semi inventory risk"),
        ("US-China technology export controls escalation",             "MACRO", 0.15, "Semi revenue at risk; custom ASIC potentially caught in next tranche"),
        ("Hyperscaler AI CapEx cycle  (Google Meta MSFT Amazon)",      "MACRO", 0.15, "Primary AI silicon demand; subject to ROI & capex budget discipline"),
    ],
}

# =============================================================================
# PART 1 — REUSABLE ENGINE
# =============================================================================

def softmax_probs(composite, scenarios, T=0.60):
    centres = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    labels  = [s[0] for s in scenarios]
    logits  = [-(composite - centres[l])**2 / T for l in labels]
    mx      = max(logits)
    exps    = [math.exp(x - mx) for x in logits]
    total   = sum(exps)
    return [e / total for e in exps]

def rfmt(r):
    return f"{r:.2f}x" if r != float('inf') else "N/A"

def infer_composite(target_price, scenarios, T=0.60):
    lo, hi = 1.0, 4.0
    for _ in range(60):
        mid   = (lo + hi) / 2
        probs = softmax_probs(mid, scenarios, T)
        ev    = sum(p * s[4] for p, s in zip(probs, scenarios))
        if ev < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

def signal_from_ratio(r):
    if r == float('inf') or r is None:
        return "✕ AVOID"
    if r < 0.75:
        return "◉ BUY"
    if r < 1.10:
        return "◎ ACCUMULATE"
    if r < 1.75:
        return "◐ WATCHLIST"
    if r < 2.50:
        return "◑ HOLD / TRIM"
    return "✕ AVOID"

# ── derived quantities ────────────────────────────────────────────────────────
epp_now          = EPS_NOW * EPP_MIN_PE
epp_gap_pct      = (CURRENT_PRICE - epp_now) / epp_now * 100
price_b          = CONS_EPS_2YR * CONS_EXIT_PE
ratio_b          = (CURRENT_PRICE - epp_now) / (price_b - CURRENT_PRICE) if price_b > CURRENT_PRICE else float('inf')
signal           = signal_from_ratio(ratio_b)

sca_raw          = sum(r * w for _, r, w in STRUCTURAL_FACTORS)
sca_adj          = sca_raw / 2.0

market_composite = infer_composite(CURRENT_PRICE, SCENARIOS)
adj_composite    = market_composite + sca_adj

probs            = softmax_probs(adj_composite, SCENARIOS)
proxy_ev         = sum(p * s[4] for p, s in zip(probs, SCENARIOS))
mkt_probs        = softmax_probs(market_composite, SCENARIOS)

# EPS decomp anchored to FY2023 pre-inflection baseline
PRE_INFLECTION_EPS = EPS_TROUGH   # $4.27 FY2023; pre-VMware close / pre-XPU ramp
eps_g_total        = EPS_NOW - PRE_INFLECTION_EPS
cyclical_dollar    = PRE_INFLECTION_EPS * sum(sh for _, sh, is_s in EPS_DECOMP if not is_s)
struct_dollar      = eps_g_total - cyclical_dollar

trailing_pe      = CURRENT_PRICE / EPS_NOW
forward_pe       = CURRENT_PRICE / EPS_FWD_CONSENSUS
cons_ret_ann     = ((price_b / CURRENT_PRICE) ** (1/2) - 1) * 100

# =============================================================================
# PART 2 — ANALYST COMMENTARY
# =============================================================================

print()
print("=" * 72)
print("  BROADCOM INC. (AVGO)  |  BottomUp Risk/Reward Signal Model")
print("=" * 72)
print(f"  Signal  : {signal}   |   Ratio B : {rfmt(ratio_b)}")
print(f"  Price   : ${CURRENT_PRICE:.2f}  |   EPP Floor : ${epp_now:.2f}  (+{epp_gap_pct:.1f}% above)")
print(f"  Date    : 2026-05-21  |   Sector  : Semiconductors · AI Infrastructure · Enterprise Software")
print("=" * 72)
print()
print("-" * 72)
print("  PART 2 — ANALYST COMMENTARY")
print("-" * 72)
print()

print("  1. BUSINESS QUALITY & COMPETITIVE MOAT")
print("  -----------------------------------------------------------------")
print("""
  Broadcom is the defining example of a semiconductor-to-software
  conglomerate: three decades of disciplined M&A have assembled a
  portfolio of near-monopoly franchises in infrastructure-critical
  markets. The company operates two segments that today contribute
  roughly equally to revenue:

  SEMICONDUCTOR SOLUTIONS (~50% of revenue, ~$38B FY2025)
  The semiconductor portfolio spans custom AI silicon (XPUs), AI
  networking (Tomahawk Ethernet switches, Jericho routers), wireless
  (WiFi 7/Bluetooth), broadband (DOCSIS 4.0), server storage
  (SAS/RAID HBA), and industrial I/O. The crown jewel is the custom
  ASIC business: Broadcom is the dominant partner for hyperscalers
  building their own AI accelerator chips. Together with Marvell
  Technology, AVGO controls >95% of the custom ASIC market for
  hyperscalers. Current active tape-out customers: Google (TPU v5/v6),
  Meta (MTIA v2), Apple (Neural Engine ML chip), ByteDance, and at
  least two additional hyperscalers per Q1 FY2026 management comments.
  Benchmark upgraded to Buy in May 2026 citing "accelerated XPU
  ramps across six customers."

  The AI networking franchise — Tomahawk Ethernet switching and
  Jericho routing — holds >70% of hyperscaler ethernet fabric share.
  As AI training clusters scale beyond 100K GPU pods, the industry
  is migrating toward Ethernet-based interconnects (lower cost, open
  ecosystem) over InfiniBand. AVGO is the primary beneficiary.

  INFRASTRUCTURE SOFTWARE (~50% of revenue, ~$37B FY2025)
  The VMware acquisition (closed November 22, 2023; ~$69B total
  consideration) transformed Broadcom into a hybrid. VMware Cloud
  Foundation is the dominant enterprise virtualisation platform with
  >300K enterprise customers and a $28B+ perpetual license base being
  systematically converted to subscription. Management's FY2027
  synergy target is $8.5B in annual operating cost savings. Progress
  is ahead of schedule: Q1 FY2026 adj EBITDA margin = 68%.

  Complementing VMware: CA Technologies (mainframe software running
  ~70% of Fortune 500 transactions), Symantec Enterprise (endpoint
  security), and Brocade (SAN storage networking). These legacy
  platforms generate extraordinary FCF with minimal reinvestment.

  LATEST RESULTS: Q1 FY2026 (ended Feb 2026; reported March 4 2026)
    Revenue     : $19,311M  (+29% YoY)
    AI revenue  : $8,395M  (+106% YoY)  <-- new quarterly record
    Non-GAAP EPS: $2.05    (beat consensus $1.88 by +9%)
    EBITDA margin: 68% of revenue
    Q2 FY2026 guide: revenue ~$22,000M (+47% YoY); EBITDA ~68%
    Q2 AI revenue guide: $10,700M (management guided explicitly)

  The 106% YoY AI revenue growth and the Q2 guide imply a full-year
  FY2026 AI semiconductor revenue run rate of approximately $40B+ —
  up from ~$12B in FY2024. This acceleration is driven by production
  depth with existing XPU customers, not yet new tape-outs.
""")

print("  2. FINANCIAL ARCHITECTURE & EPP FLOOR")
print("  -----------------------------------------------------------------")
print(f"""
  EPP FLOOR MECHANICS
  EPS_TROUGH = ${EPS_TROUGH:.2f} (FY2023 non-GAAP post-split; last year before both
  VMware integration and AI XPU inflection). The Oct 2022 bear-market
  low of ${EPS_TROUGH_PRICE:.0f} post-split with trailing EPS ~$4.00 implies an observed
  trough multiple of ~10-11x. EPP_MIN_PE = {EPP_MIN_PE}x reflects the structural
  quality premium warranted by AVGO's post-VMware profile (50%
  recurring software, >60% FCF margins, investment-grade) above the
  bare 10-13x observed cyclical floor.

  EPP (current) = EPS_NOW ${EPS_NOW:.2f} x {EPP_MIN_PE}x = ${epp_now:.2f}
  EPP gap       = {epp_gap_pct:.1f}% above floor

  At {epp_gap_pct:.0f}%, the EPP gap is the second-highest in this coverage
  universe after TSLA. This does not reflect poor business quality —
  it reflects an extraordinary premium already assigned to the AI
  silicon and software compounding thesis. The EPP floor migrates:
  by FY2027E (EPS ~$12.72) EPP reaches ~$203; by FY2028E (EPS ~$17)
  it reaches ~$272. The floor is rising fast, but will not reach
  today's price for approximately 4-5 years at consensus EPS growth.

  EPS GROWTH QUALITY (FY2023 ${PRE_INFLECTION_EPS:.2f} -> FY2025 ${EPS_NOW:.2f} = +${eps_g_total:.2f})
  Structural : ${struct_dollar:.2f}  ({struct_dollar/eps_g_total*100:.0f}%)
  Cyclical   : ${cyclical_dollar:.2f}  ({cyclical_dollar/eps_g_total*100:.0f}%)

  The structural majority reflects two durable platform wins: VMware
  SaaS conversion (margin accretion from the perpetual-to-subscription
  migration) and AI XPU production ramp (multi-year contracted silicon
  programs). The cyclical portion (AI networking wave + broadband
  recovery) is real demand but more sensitive to hyperscaler CapEx
  timing and inventory normalisation.

  BALANCE SHEET
  AVGO carried ~$70B net debt post-VMware (Nov 2023). FY2025 FCF
  was ~$19-20B (~60% FCF margin). At this rate, the company
  deleverages ~$15-18B/year after dividends (~$10B/year), reaching
  target leverage by FY2028. Dividend yield at current price ~0.6%.
""")

print("  3. GROWTH CATALYST & VARIANT PERSPECTIVE")
print("  -----------------------------------------------------------------")
print(f"""
  PRIMARY CATALYST: HYPERSCALER XPU EXPANSION
  AVGO management guided at their March 2026 analyst day that the
  serviceable AI revenue opportunity from existing hyperscaler
  partners could reach $60-90B by FY2027. With FY2026E AI revenue
  ~$40B, this implies 50-125% upside to AI revenue in two years.
  The key driver is production depth (Google TPU v6 ramp, Meta MTIA
  v2 at scale, Apple inference chip proliferating) and breadth
  (Evercore ISI raised target to $582 May 2026, citing XPU pipeline).

  SECONDARY CATALYST: VMWARE SYNERGY OVER-DELIVERY
  The $8.5B cost synergy target is widely modelled; the under-
  appreciated dynamic is ARPU. Converting mid-market perpetual
  customers (~$500K/acct/yr) to full VCF subscriptions (~$2-5M+/
  acct/yr for strategic accounts) is an undermodelled revenue lever.

  THIRD CATALYST: AI NETWORKING SHARE LOCK-IN
  The industry shift from InfiniBand to Ethernet for large AI
  clusters benefits AVGO's Tomahawk 5 (51.2 Tbps) and upcoming
  Tomahawk 6 (2x bandwidth). NVIDIA's Spectrum-X development creates
  headline risk, but AVGO's installed base and roadmap lead should
  sustain leadership for the 3-5 year horizon.

  THE VARIANT DEBATE
  BULL: AVGO becomes the "picks and shovels" AI compounder. The XPU
  business is effectively a toll road on hyperscaler AI CapEx. At
  $18 EPS x 38x = $684 (BULL), upside from ${CURRENT_PRICE:.0f} is +64%.

  BEAR: The current price requires 33x FY2027E — in the top quintile
  of AVGO's historical range. A hyperscaler capex pause, acceleration
  of in-house silicon at Google or Meta, or VMware mid-market churn
  (many chose alternative hypervisors post-acquisition pricing hikes)
  could compress both EPS and multiple simultaneously. The BASE
  scenario ($382) is already below the current price. AVGO needs
  to execute the BULL path just to generate double-digit returns
  from today's level.
""")

print("  4. RISK REGISTER")
print("  -----------------------------------------------------------------")
print(f"""
  Risk                                          Impact     Probability
  -----------------------------------------------------------------------
  Hyperscaler AI capex pause / recalibration    HIGH       LOW-MEDIUM
  In-house silicon acceleration (Google/Meta)   HIGH       LOW
  VMware mid-market customer churn              MEDIUM     MEDIUM
  Export controls expand to custom ASICs        HIGH       LOW-MEDIUM
  NVIDIA Spectrum-X Ethernet displaces AVGO     MEDIUM     LOW
  Rate-driven multiple compression              MEDIUM     LOW-MEDIUM
  Post-VMware integration complexity            MEDIUM     LOW
  -----------------------------------------------------------------------

  CONCENTRATION RISK
  Google, Meta, and Apple represent an estimated 35-40% of AVGO AI
  semiconductor revenue. Any single customer slowing XPU tape-outs
  or developing next-gen in-house would be material. Google has full
  internal ASIC capability; AVGO's value is engineering talent and
  speed. This risk is structural and cannot be diversified away at
  any valuation.

  EXPORT CONTROL ESCALATION
  Current AI XPU business (US-produced silicon for US hyperscalers)
  is not directly impacted by current China controls. However, non-AI
  semi still has ~15% China-derived revenue. Escalation categorising
  custom ASICs as dual-use technology could create compliance risk
  or force redesigns on future tape-outs.

  VALUATION ASYMMETRY
  At ${CURRENT_PRICE:.2f}, AVGO trades at:
    Trailing P/E : {trailing_pe:.1f}x  (FY2025 ${EPS_NOW:.2f})
    Forward P/E  : {forward_pe:.1f}x  (FY2026E ${EPS_FWD_CONSENSUS:.2f})
    2-Yr Fwd P/E : {CURRENT_PRICE/CONS_EPS_2YR:.1f}x  (FY2027E ${CONS_EPS_2YR:.2f})
  32.8x FY2027E is demanding for a business where 40% of recent EPS
  growth has cyclical roots (AI networking timing + semi recovery).
""")

print("  5. SIGNAL & POSITIONING")
print("  -----------------------------------------------------------------")
print(f"""
  SIGNAL: {signal}   |   Ratio B: {rfmt(ratio_b)}

  Method B target : ${price_b:.0f}  (FY2027E ${CONS_EPS_2YR:.2f} x {CONS_EXIT_PE}x exit PE)
  Current price   : ${CURRENT_PRICE:.2f}
  Method B gap    : ${CURRENT_PRICE - price_b:+.0f} ({(CURRENT_PRICE/price_b - 1)*100:+.1f}% above target)

  The Method B target of ${price_b:.0f} is {(CURRENT_PRICE/price_b - 1)*100:.1f}% below the current price
  even at a generous {CONS_EXIT_PE}x exit multiple. Ratio B is N/A (undefined)
  because price_B < current price. Signal = AVOID by construction.

  THE CORE TENSION
  Broadcom is an exceptional business. The SCA model composite
  ({adj_composite:.2f}) sits between BASE and BULL, and the model's proxy
  fair value (${proxy_ev:.0f}) is above current price — structural quality
  justifies a premium. But structural quality is not the same as
  attractive risk/reward.

  The EPP gap of {epp_gap_pct:.0f}% means reversion to the fundamental floor
  (not even BEAR — simply a re-rating to the trough multiple on
  current EPS) implies an {(1 - epp_now/CURRENT_PRICE)*100:.0f}% drawdown. The BEAR scenario
  ($98) is extreme but real: in 2022 AVGO traded at $44 post-split
  despite strong EPS growth. Combined multiple compression + EPS miss
  ($7 bear EPS x 14x) = exactly that level. Maximum pain: -77%.

  REVALUATION TRIGGERS (WHEN TO RE-EVALUATE)
  --------------------------------------------------------------
  Price < $300 : Method B (~$356) now >18% above current; EPP gap
    contracts to ~175%; Ratio B enters low-single-x range
    -> merit a WATCHLIST reassessment

  Price < $220 : Method B target above current; EPP gap ~100%
    -> ACCUMULATE territory if fundamentals unchanged

  Catalyst: 2+ additional hyperscaler XPU wins + VMware ARR >30%
    -> upgrade BULL scenario ceiling; raise CONS_EXIT_PE; revisit
  --------------------------------------------------------------

  AVGO is on the watchlist for price pullbacks. The business
  compounding story is intact; the risk/reward is not.
""")

# =============================================================================
# PART 3 — NUMBERS & SIGNALS
# =============================================================================

print()
print("-" * 72)
print("  PART 3 — NUMBERS & SIGNALS")
print("-" * 72)
print()

print("  A. EPS & PRICE HISTORY (post-split; 10-for-1 split Jul 15 2024)")
print("  -----------------------------------------------------------------")
print(f"""
  FY2023 (trough)  : Non-GAAP EPS ~$4.27  |  Low price ~$44  |  Min PE ~10x
  FY2024 (VMw ramp): Non-GAAP EPS ~$4.86  |  Range $44-$185  |  VMware partial yr
  FY2025 (actual)  : Non-GAAP EPS  $6.82  |  Range $125-$250 |  VMware first full yr
  FY2026E (current): Non-GAAP EPS ~$9.39  |  Current: ${CURRENT_PRICE:.2f}    |  Q1 $2.05 beat
  FY2027E (2-yr)   : Non-GAAP EPS ~$12.72 |  Method B target: ${price_b:.0f}
""")

print("  B. EPP FLOOR & RATIO B")
print("  -----------------------------------------------------------------")
print(f"""
  EPS_NOW    = ${EPS_NOW:.2f}   (FY2025 non-GAAP diluted)
  EPP_MIN_PE = {EPP_MIN_PE}x       (above 10-13x observed bear floor; VMware quality uplift)
  EPP_NOW    = ${epp_now:.2f}  (= ${EPS_NOW:.2f} x {EPP_MIN_PE}x)
  EPP_gap    = +{epp_gap_pct:.1f}% above floor

  CONS_EPS_2YR = ${CONS_EPS_2YR:.2f}  (FY2027E consensus)
  CONS_EXIT_PE = {CONS_EXIT_PE}x       (generous; semi-software hybrid; below current 32.8x FY2027E)
  Price_B      = ${price_b:.2f}  (= ${CONS_EPS_2YR:.2f} x {CONS_EXIT_PE}x)
  Ratio_B      = {rfmt(ratio_b)}     (price_B < current -> undefined -> AVOID)
""")

print("  C. SCENARIO TABLE")
print("  -----------------------------------------------------------------")
print(f"  {'Scenario':<8}  {'EPS':>6}  {'Exit PE':>7}  {'Target':>8}  {'vs Current':>10}")
print("  " + "-" * 48)
for s in SCENARIOS:
    delta = (s[4] / CURRENT_PRICE - 1) * 100
    print(f"  {s[0]:<8}  ${s[2]:>5.2f}  {s[3]:>6}x  ${s[4]:>7.0f}  {delta:>+9.0f}%")
print()

print("  D. PROBABILITY DISTRIBUTION")
print("  -----------------------------------------------------------------")
print(f"""
  Market composite (inferred)  : {market_composite:.2f}
  SCA raw / adjusted           : {sca_raw:.3f} / {sca_adj:.3f}
  Model adj composite          : {adj_composite:.2f}
  Proxy EV (adj composite)     : ${proxy_ev:.0f}  ({(proxy_ev/CURRENT_PRICE-1)*100:+.1f}% vs current ${CURRENT_PRICE:.2f})
""")
labels = [s[0] for s in SCENARIOS]
print(f"  {'':8}  {'Mkt (raw)':>12}  {'Model (adj)':>12}")
print("  " + "-" * 36)
for i, lbl in enumerate(labels):
    print(f"  {lbl:<8}  {mkt_probs[i]*100:>10.1f}%  {probs[i]*100:>10.1f}%")
print()

print("  E. CROSS-READ SIGNALS (5 indicators -> composite)")
print("  -----------------------------------------------------------------")
header = f"  {'Signal':<42}  {'Wt':>4}  {'Bear':>6}  {'Base':>6}  {'Bull':>6}  {'XBull':>6}  {'Curr':>7}  {'Score':>5}"
print(header)
print("  " + "-" * (len(header) - 2))

def score_signal(bear, base, bull, xbull, current):
    pts = [(bear, 1.25), (base, 2.0), (bull, 2.75), (xbull, 3.75)]
    pts.sort(key=lambda x: x[0])
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    if current <= xs[0]:  return ys[0]
    if current >= xs[-1]: return ys[-1]
    for k in range(len(xs) - 1):
        if xs[k] <= current <= xs[k+1]:
            t = (current - xs[k]) / (xs[k+1] - xs[k])
            return ys[k] + t * (ys[k+1] - ys[k])
    return ys[-1]

scores = []
for cr in CROSS_READS:
    name, _, unit, bear, base, bull, xbull, current, weight = cr
    s = score_signal(bear, base, bull, xbull, current)
    scores.append((s, weight))
    short = name[:42]
    print(f"  {short:<42}  {weight:>4.0%}  {bear:>6}  {base:>6}  {bull:>6}  {xbull:>6}  {current:>7}  {s:>5.2f}")

weighted_composite = sum(s * w for s, w in scores)
print(f"\n  Weighted signal composite : {weighted_composite:.2f}  "
      f"(market inferred: {market_composite:.2f};  delta: {market_composite - weighted_composite:+.2f})")
print()

print("  F. STRUCTURAL COMPOSITE ADJUSTMENT (SCA)")
print("  -----------------------------------------------------------------")
print(f"  {'Factor':<60}  {'Rating':>6}  {'Wt':>4}")
print("  " + "-" * 74)
for name, rating, weight in STRUCTURAL_FACTORS:
    print(f"  {name:<60}  {rating:>+6.1f}  {weight:>4.0%}")
print(f"\n  SCA raw = {sca_raw:.3f}   SCA adj (div 2) = {sca_adj:.3f}")
print(f"  Market composite {market_composite:.2f}  +  SCA {sca_adj:.3f}  =  Model composite {adj_composite:.2f}")
print()

print("  G. EPS QUALITY DECOMP  (FY2023 ${:.2f} -> FY2025 ${:.2f} = +${:.2f})".format(
    PRE_INFLECTION_EPS, EPS_NOW, eps_g_total))
print("  -----------------------------------------------------------------")
print(f"  {'Component':<60}  {'Share':>5}  {'Type':>10}")
print("  " + "-" * 79)
for name, sh, is_s in EPS_DECOMP:
    kind = "Structural" if is_s else "Cyclical"
    print(f"  {name:<60}  {sh:>5.0%}  {kind:>10}")
print(f"\n  Structural : ${struct_dollar:.2f}  ({struct_dollar/eps_g_total*100:.0f}%)")
print(f"  Cyclical   : ${cyclical_dollar:.2f}  ({cyclical_dollar/eps_g_total*100:.0f}%)")
print(f"  Total      : ${eps_g_total:.2f}")
print()

print("  H. RISK / RETURN SUMMARY")
print("  -----------------------------------------------------------------")
print(f"""
  Current price          : ${CURRENT_PRICE:.2f}
  EPP floor              : ${epp_now:.2f}   (downside to floor: {(epp_now/CURRENT_PRICE - 1)*100:.0f}%)
  Method B target        : ${price_b:.0f}     (upside: {(price_b/CURRENT_PRICE - 1)*100:+.0f}% = N/A -- below current)
  Ratio B                : {rfmt(ratio_b)}  -> {signal}
  Beta                   : {BETA:.2f}x  ({IDIO['idio_pct']}% idio / {IDIO['macro_pct']}% macro)
  Trailing P/E           : {trailing_pe:.1f}x  (FY2025 ${EPS_NOW:.2f})
  Forward P/E            : {forward_pe:.1f}x  (FY2026E ${EPS_FWD_CONSENSUS:.2f})
  2-Yr Forward P/E       : {CURRENT_PRICE/CONS_EPS_2YR:.1f}x  (FY2027E ${CONS_EPS_2YR:.2f})
  Implied 2-yr ann return: {cons_ret_ann:+.1f}%/yr  (to Method B ${price_b:.0f})
  Re-evaluate below      : $300  (Method B>current; EPP gap ~175%; Ratio B enters single digits)
""")

print("  I. IDIOSYNCRATIC vs MACRO DRIVERS")
print("  -----------------------------------------------------------------")
print(f"  Beta: {IDIO['beta']:.2f}x  |  Idiosyncratic: {IDIO['idio_pct']}%  |  Macro: {IDIO['macro_pct']}%\n")
print(f"  {'Driver':<50}  {'Type':>5}  {'Wt':>4}  Note")
print("  " + "-" * 90)
for driver, kind, wt, note in IDIO["drivers"]:
    print(f"  {driver:<50}  {kind:>5}  {wt:>4.0%}  {note}")
print()
print("=" * 72)
print("  END OF REPORT -- AVGO  |  Generated 2026-05-21")
print("=" * 72)
