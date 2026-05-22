"""
McDonald's Corporation (MCD) — BottomUp Risk/Reward Signal Model
95% franchised QSR operator; ~$27B revenue; 44,000+ restaurants globally;
real estate-backed royalty machine; Dividend Aristocrat (50+ consecutive annual raises)
Three-Part Publication Format

FISCAL YEAR NOTE: McDonald's fiscal year ends December 31 (calendar year).
  FY2019 = Jan-Dec 2019  (pre-pandemic baseline; adj EPS ~$8.00)
  FY2020 = Jan-Dec 2020  (COVID closures; adj EPS ~$6.26; pandemic trough)
  FY2021 = Jan-Dec 2021  (reopening recovery; adj EPS ~$9.77)
  FY2022 = Jan-Dec 2022  (strong pricing cycle; adj EPS ~$10.13)
  FY2023 = Jan-Dec 2023  (record year; adj EPS $11.94)
  FY2024 = Jan-Dec 2024  (E. coli scare + Middle East boycotts; adj EPS $11.72)
  FY2025 = Jan-Dec 2025  (recovery; comp sales +3.1% global; adj EPS $12.20)
  FY2026 = Jan-Dec 2026  (current; Q1 adj EPS $2.83 +6% YoY)
  FY2027 = Jan-Dec 2027  (2-year exit horizon; consensus adj EPS ~$13.50)

NO STOCK SPLIT. All per-share figures are unadjusted.
"""
import math

# ── LIVE PRICE (fetched via web search, 2026-05-21) ──────────────────────────
CURRENT_PRICE = 280.27   # MCD — web search (intraday $276.40-$281.02), NYSE, 2026-05-21

# ── EPP FLOOR CALIBRATION ────────────────────────────────────────────────────
# FY2024: adj EPS $11.72 (down 1.8% from FY2023 $11.94). Dual headwinds:
#   (1) Oct 2024 E. coli outbreak linked to Quarter Pounder slivered onions;
#       stock fell ~7% on the news, customer visits dropped 6.4% day-of
#   (2) Middle East boycott (Israel-Hamas conflict) pressuring international sales
# Stock trough: Oct 2024 ~$255 during E. coli crisis (pre-current 52-week window)
# Current 52-week range: $271.98 - $341.75; today $280.27 = near 52-week low
# EPP validation: $255 / $11.72 = 21.8x observed trough PE; EPP_MIN_PE = 20x
# (conservatively below observed trough; Dividend Aristocrat with 50+ yr raise streak)
EPS_TROUGH       = 11.72  # FY2024 adj diluted EPS; E. coli / boycott cycle low
EPS_TROUGH_YEAR  = 2024
EPS_TROUGH_PRICE = 255.0  # Oct 2024 crisis low (E. coli scare + boycott fear)
EPP_MIN_PE       = 20     # below observed 21.8x crisis trough; 95% franchise quality floor

# ── CURRENT FUNDAMENTALS ─────────────────────────────────────────────────────
EPS_NOW           = 12.20  # FY2025 adj diluted; global comp +3.1%; Q4 +5.7%; confirmed Feb 11 2026
EPS_FWD_CONSENSUS = 12.93  # FY2026E adj (~6% growth; Q1 actual $2.83 beat $2.74)
CONS_EPS_2YR      = 13.50  # FY2027E adj consensus (~5%/yr from $12.20; conservative mid-range)
CONS_EPS_CAGR     = 0.052  # ~5.2%/yr (FY2025 $12.20 -> FY2027E $13.50); defensive compounder
CONS_EXIT_PE      = 24     # mid of historical 22-27x range; franchise premium to market
BETA              = 0.65   # defensive; 95% franchise; real estate; global diversification

# ── SCENARIO TABLE ───────────────────────────────────────────────────────────
SCENARIOS = [
    ("BEAR",  "Consumer recession; GLP-1 accelerates; comp sales -5%; multiple compression",          9.50, 18,  171),
    ("BASE",  "Gradual recovery; global comps +3-4%; value menu holds; EPS compounds ~5%/yr",        13.50, 24,  324),
    ("BULL",  "Value menu wins QSR share; international acceleration; comps +7%+; AI personalisation", 16.50, 26, 429),
    ("XBULL", "Full QSR dominance; new formats at scale; China recovery; franchisee ROIC re-rates",   20.00, 28,  560),
]

# ── CROSS-READ SIGNALS ───────────────────────────────────────────────────────
CROSS_READS = [
    ("Global comparable store sales growth  (%YoY; all segments combined)",        "Broadest demand proxy; Q1 2026 = +3.8%; Q4 2025 = +5.7%; trend improving",  "%",   -5,   3,   7,  12, 3.8, 0.30),
    ("US comparable store sales  (%YoY; ~35% of operating income)",                "Home-market bellwether; Q1 2026 = +3.9%; value menu + breakfast drive",      "%",   -5,   3,   8,  15, 3.9, 0.25),
    ("MCD value perception vs. QSR peers  (composite score; 100 = parity)",        "Key competitive metric; value wars vs. BK/Wendy's/Chick-fil-A; $5 bundle",  "idx",  20,  50,  70,  90,  55, 0.20),
    ("Net global restaurant additions  (new openings less closures, annual)",       "Franchisee confidence proxy; development pipeline; FY2025 net +750 est",    "#",  -200, 500,1500,2500, 750, 0.15),
    ("US consumer confidence  (Conference Board index; 100 = long-term avg)",      "Macro demand signal; low-income diner cohort most rate-sensitive",           "idx",   60, 100, 120, 135,  90, 0.10),
]

# ── STRUCTURAL COMPOSITE ADJUSTMENT ─────────────────────────────────────────
STRUCTURAL_FACTORS = [
    ("95% franchised asset-light model  (royalties + rent; extraordinary FCF quality; repeatable)",   +1.0, 0.30),
    ("Real estate portfolio  ($8.2B annual rent income; captive franchisees; below-market leases)",   +0.8, 0.25),
    ("Value competition headwinds  (Wendy's/BK/Chick-fil-A/Taco Bell; value-menu price wars)",       -0.7, 0.20),
    ("GLP-1 / health behaviour risk  (long-term dietary shift; QSR TAM headwind; structural drag)",   -0.5, 0.15),
    ("Global brand scale / pricing power  (44K+ restaurants; #1 QSR brand; menu price discipline)",  +0.4, 0.10),
]

# ── EPS QUALITY DECOMPOSITION ────────────────────────────────────────────────
# EPS grew from pre-pandemic FY2019 ~$8.00 to FY2025 $12.20: +$4.20 total
# Decompose to show structural vs. cyclical portion of current earnings base
PRE_COVID_EPS = 8.00   # FY2019 adj diluted EPS; pre-pandemic, pre-refranchising completion
EPS_DECOMP = [
    ("Refranchising completion  (80% -> 95% franchise; eliminated company op losses; margin step-up)",  0.35, True),
    ("Systematic menu price increases  (avg 3-5%/yr since 2020; above food-cost inflation through 2023)", 0.25, True),
    ("International Operated Markets compounding  (IOM: France, UK, Germany, Australia growth)",       0.15, True),
    ("Post-pandemic demand normalisation  (traffic recovery; pent-up dining out; value surge 2021-22)", 0.17, False),
    ("Share buyback accretion  (~15% net share count reduction FY2019-FY2025)",                        0.08, True),
]

# ── IDIOSYNCRATIC vs MACRO DECOMPOSITION ─────────────────────────────────────
IDIO = {
    "idio_pct":  40,
    "macro_pct": 60,
    "beta":      0.65,
    "drivers": [
        ("Menu innovation & value platform  ($5 Meal Deal; MyMcDonald's loyalty)",  "IDIO",  0.15, "Loyalty 175M+ active; personalisation drives frequency & ticket"),
        ("Operational execution & franchisee relations",                              "IDIO",  0.15, "Franchisee profitability tied to system; rent/royalty levers"),
        ("New restaurant development pipeline & CosMc's concept",                    "IDIO",  0.10, "Net adds 750+/yr; CosMc's small-format beverage test"),
        ("US consumer confidence & low-income spending",                             "MACRO", 0.20, "Low-income diner most rate-sensitive; key traffic risk in recession"),
        ("Global FX fluctuations  (~60% revenue ex-US)",                             "MACRO", 0.20, "USD strength compresses IOM & IDL in constant currency vs reported"),
        ("Food commodity costs  (beef, chicken, potatoes, packaging)",               "MACRO", 0.20, "Input cost inflation limits margin; franchisee pass-through dynamic"),
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

eps_g_total      = EPS_NOW - PRE_COVID_EPS
cyclical_dollar  = PRE_COVID_EPS * sum(sh for _, sh, is_s in EPS_DECOMP if not is_s)
struct_dollar    = eps_g_total - cyclical_dollar

trailing_pe      = CURRENT_PRICE / EPS_NOW
forward_pe       = CURRENT_PRICE / EPS_FWD_CONSENSUS
cons_ret_ann     = ((price_b / CURRENT_PRICE) ** (1/2) - 1) * 100
div_yield        = (1.86 * 4) / CURRENT_PRICE * 100  # $1.86/qtr declared Mar 2026

# =============================================================================
# PART 2 — ANALYST COMMENTARY
# =============================================================================

print()
print("=" * 72)
print("  McDONALD'S CORPORATION (MCD)  |  BottomUp Risk/Reward Signal Model")
print("=" * 72)
print(f"  Signal  : {signal}   |   Ratio B : {rfmt(ratio_b)}")
print(f"  Price   : ${CURRENT_PRICE:.2f}  |   EPP Floor : ${epp_now:.2f}  (+{epp_gap_pct:.1f}% above)")
print(f"  Date    : 2026-05-21  |   Sector  : QSR · Franchise Model · Consumer Staple-Like")
print("=" * 72)
print()
print("-" * 72)
print("  PART 2 — ANALYST COMMENTARY")
print("-" * 72)
print()

print("  1. BUSINESS QUALITY & COMPETITIVE MOAT")
print("  -----------------------------------------------------------------")
print("""
  McDonald's is the world's largest restaurant company by system
  revenues, operating 44,000+ locations across 100+ countries with
  ~$130B in annual systemwide sales. The business model is one of
  the most capital-efficient in global consumer: 95% of restaurants
  are operated by independent franchisees who own the equipment,
  staff, and inventory — McDonald's provides the brand, real estate,
  supply chain, and systems. The company receives royalties (~4-5%
  of sales) and rental income (8-15% of sales) under 20-year
  franchise agreements. This structure generates extraordinary FCF
  at low capital intensity.

  THE REAL ESTATE MOAT
  Less visible than the brand, but arguably more durable: McDonald's
  owns or controls the real estate under ~55% of its franchised
  restaurants and leases it to franchisees at rents tied to
  restaurant performance. This generates ~$8.2B in annual rental
  income — essentially a captive REIT embedded inside a QSR. In a
  recession, this rental income is partly protected because
  franchisees have 20-year commitments and cannot walk away without
  significant financial penalty. It also creates an inflation hedge:
  rent escalates with sales.

  THE BRAND MOAT
  McDonald's is the #1 QSR brand globally by recognition. The value
  is structural: in every economic downturn, McDonald's benefits from
  trade-down as consumers shift from casual dining to QSR. The Golden
  Arches are one of a handful of truly global consumer brands with
  near-universal recognition. The MyMcDonald's loyalty program has
  175M+ active users across 50 markets, driving repeat visits and
  data-enabled personalisation.

  FRANCHISE ECONOMICS
  A typical McDonald's franchisee earns approximately $175K-$300K
  per year in operating profit per restaurant (on ~$4M in annual
  sales), with a roughly 20-year franchise agreement providing
  earnings visibility. The franchisee's cost structure means
  McDonald's royalty and rent is generally the last payment
  cut in a downturn — creating a built-in defensive layer for
  MCD's income statement even in consumer recessions.

  LATEST RESULTS: Q1 2026 (ended March 31, 2026; reported May 7 2026)
    Net revenue       : $6.52B  (+9% YoY; beat $6.47B estimate)
    Systemwide sales  : up 11% (6% in constant currency)
    Non-GAAP EPS      : $2.83   (beat $2.74 estimate, +6% YoY)
    US comp sales     : +3.9%   (4th consecutive positive quarter)
    Global comp sales : +3.8%   (~in line with +3.7% consensus)
    FY2026 outlook    : operating margin expansion from 46.9% FY2025 base

  Q1 comp sales growth of +3.8% is notable: it is the fourth
  consecutive positive quarter after a painful 2024 that included the
  E. coli scare (October 2024) and persistent Middle East boycott
  headwinds. The $5 Meal Deal value platform and McValue menu
  launched in late 2024 are gaining traction; US ticket per visit
  is rising even as traffic stabilises.
""")

print("  2. FINANCIAL ARCHITECTURE & EPP FLOOR")
print("  -----------------------------------------------------------------")
print(f"""
  EPP FLOOR MECHANICS
  EPS_TROUGH = ${EPS_TROUGH:.2f} (FY2024 adj; the most recent cycle trough caused by
  the October 2024 E. coli scare linked to Quarter Pounder slivered
  onions and simultaneous Middle East boycotts affecting
  international sales). At the October 2024 crisis low of
  ~${EPS_TROUGH_PRICE:.0f}/share, trailing EPS was ${EPS_TROUGH:.2f}, implying a trough PE
  of {EPS_TROUGH_PRICE/EPS_TROUGH:.1f}x. EPP_MIN_PE = {EPP_MIN_PE}x is conservatively below this
  observed floor, reflecting maximum bear scenario pricing for a
  company with 50+ consecutive years of annual dividend increases.

  EPP (current) = EPS_NOW ${EPS_NOW:.2f} x {EPP_MIN_PE}x = ${epp_now:.2f}
  EPP gap       = {epp_gap_pct:.1f}% above floor

  At {epp_gap_pct:.1f}%, the EPP gap is the LOWEST in this coverage universe —
  even lower than HD (17.2%). The stock at ${CURRENT_PRICE:.2f} is only ${CURRENT_PRICE - epp_now:.0f}
  above its structural earnings floor. This is exactly the kind of
  low-gap, high-quality entry point the EPP framework is designed
  to identify.

  EPS GROWTH QUALITY (FY2019 ${PRE_COVID_EPS:.2f} -> FY2025 ${EPS_NOW:.2f} = +${eps_g_total:.2f})
  Structural : ${struct_dollar:.2f}  ({struct_dollar/eps_g_total*100:.0f}%)
  Cyclical   : ${cyclical_dollar:.2f}  ({cyclical_dollar/eps_g_total*100:.0f}%)

  The structural majority reflects the completion of McDonald's
  refranchising (from 80% to 95% franchised), systematic pricing
  power, and international market development. The cyclical portion
  reflects the post-COVID dining normalisation wave.

  DIVIDEND: MCD is a Dividend Aristocrat with 50+ consecutive annual
  dividend increases. Current quarterly dividend: $1.86/share.
  Annual: $7.44/share. Yield at current price: {div_yield:.1f}%. This
  provides meaningful income while waiting for the price recovery.
  FCF payout ratio: ~65%, leaving room for continued raises.

  FREE CASH FLOW: FY2025 FCF ~$7.5-8.0B (operating cash ~$10B less
  capex ~$2.5B). After dividends ~$4.8B, remaining FCF ~$3B
  deployed to buybacks. Net debt ~$35-37B is managed within the
  franchise model's stable FCF; investment-grade rated.
""")

print("  3. GROWTH CATALYST & VARIANT PERSPECTIVE")
print("  -----------------------------------------------------------------")
print(f"""
  PRIMARY CATALYST: VALUE MENU RECOVERY + TRAFFIC NORMALISATION
  After 8 consecutive quarters of negative comparable sales
  (2023-2024), the comp sales trajectory has turned: Q4 2025 +5.7%
  global, Q1 2026 +3.8%. The $5 Meal Deal and McValue menu are
  driving frequency among the critical low-to-middle income consumer
  cohort. The key question is whether this recovery is durable or
  merely a base effect. The Polymarket consensus for Q1 2026 EPS
  (non-GAAP >$2.75) closed near 90% probability — suggesting broad
  market confidence in the recovery.

  SECONDARY CATALYST: INTERNATIONAL NORMALISATION
  The Middle East boycott effect peaked in early 2025 and has been
  gradually fading. The International Developmental Licensed (IDL)
  segment — which includes GCC markets — returned to positive comps
  in Q4 2025 (+4.6% for full year 2025). Recovery in the Middle East
  and ongoing international unit growth provide EPS tailwind.

  THIRD CATALYST: LOYALTY + AI PERSONALISATION
  175M+ active loyalty members across 50 markets. McDonald's is
  deploying AI-driven ordering (digital menu boards with dynamic
  pricing/upsell) in drive-thrus across the US. This is an
  underappreciated ticket driver: personalised upsell on a $6-8
  transaction at scale. FY2025 saw digital orders exceed 40% of
  systemwide sales in top 6 markets.

  THE VARIANT DEBATE
  BULL CASE: McDonald's at ~23x trailing P/E is cheap for a Dividend
  Aristocrat that historically trades 24-28x. The franchise moat is
  genuinely resistant to disruption; GLP-1 headwinds are real but
  slow-moving (5-10 year horizon, not 12-18 months). At BASE
  recovery ($324), total return including dividend is ~20% from
  current levels over 18-24 months.

  BEAR CASE: Consumer discretionary pressure on low-income cohort
  is structural in a high-rate environment. If rates stay elevated
  and unemployment rises 1-2%, MCD could see negative comps again.
  The E. coli scare showed how quickly traffic can reverse. At $9.50
  EPS x 18x in a severe recession = $171 — a -39% drawdown. This
  is the worst-case scenario, not the base, but it is real.

  CURRENT PRICE NOTE: ${CURRENT_PRICE:.2f} is only ${CURRENT_PRICE - 271.98:.2f} above the 52-week low
  of $271.98. The stock has been range-bound near multi-year lows
  while the business has re-accelerated. This technical setup
  (low price / improving fundamentals) supports the ACCUMULATE
  signal.
""")

print("  4. RISK REGISTER")
print("  -----------------------------------------------------------------")
print(f"""
  Risk                                          Impact     Probability
  -----------------------------------------------------------------------
  Consumer recession / low-income trade-down    HIGH       MEDIUM
  Food-borne illness / brand crisis reoccur     HIGH       LOW
  GLP-1 / health trend accelerates MSD          MEDIUM     LOW-MED
  Middle East / geopolitical boycott re-ignite  MEDIUM     LOW-MED
  USD strength compresses international EPS     MEDIUM     MEDIUM
  Value competition (BK/Wendy's) intensifies    MEDIUM     MEDIUM
  Commodity cost (beef/chicken) spike           MEDIUM     LOW-MED
  -----------------------------------------------------------------------

  LOW-INCOME CONSUMER SENSITIVITY
  McDonald's traffic is highly concentrated in the 18-34 age group
  and household incomes below $45K. In the post-pandemic period,
  low-income households have been squeezed by cumulative food/rent
  inflation. When this cohort cuts back, McDonald's visits are
  among the first discretionary spend to fall — even though QSR
  is a "trading down" destination from casual dining. If the US
  unemployment rate rises above 5%, comp sales pressure would
  likely return.

  FOOD SAFETY TAIL RISK
  The October 2024 E. coli outbreak (linked to slivered onions) was
  a reminder that food safety incidents are an always-present tail
  risk. McDonald's supply chain involves hundreds of suppliers and
  thousands of franchisees. While the company has strong traceability
  systems, a major food safety event can crater short-term traffic
  and require significant marketing investment to restore trust.
  The 2024 incident cost an estimated $0.20-0.30 in EPS from one
  quarter of traffic disruption and brand recovery spend.

  GLP-1 STRUCTURAL RISK (LONG-TERM)
  GLP-1 drugs (Ozempic, Wegovy, Zepbound) reduce appetite and are
  associated with healthier food choices over time. Long-term
  penetration into the mass market could structurally reduce QSR
  traffic. This is a 5-10 year horizon risk, not a 12-18 month
  concern, but it warrants monitoring. Current penetration in the
  US adult population is ~3-5%, not yet material to traffic data.

  VALUATION NOTE
  At ${CURRENT_PRICE:.2f}, MCD trades at:
    Trailing P/E  : {trailing_pe:.1f}x  (FY2025 ${EPS_NOW:.2f})
    Forward P/E   : {forward_pe:.1f}x  (FY2026E ${EPS_FWD_CONSENSUS:.2f})
    2-Yr Fwd P/E  : {CURRENT_PRICE/CONS_EPS_2YR:.1f}x  (FY2027E ${CONS_EPS_2YR:.2f})
    Div yield     : {div_yield:.1f}%  ($7.44 annualised)
  All three multiples are at or below the bottom of McDonald's
  historical 22-27x trading range for a stable P/E compounder.
  Forward multiple compression is the key risk; the dividend provides
  income support while waiting for re-rating.
""")

print("  5. SIGNAL & POSITIONING")
print("  -----------------------------------------------------------------")
print(f"""
  SIGNAL: {signal}   |   Ratio B: {rfmt(ratio_b)}

  Method B target : ${price_b:.0f}  (FY2027E ${CONS_EPS_2YR:.2f} x {CONS_EXIT_PE}x exit PE)
  Current price   : ${CURRENT_PRICE:.2f}
  Potential upside: +${price_b - CURRENT_PRICE:.0f} (+{(price_b/CURRENT_PRICE - 1)*100:.1f}%)

  THE ACCUMULATE THESIS
  McDonald's at ${CURRENT_PRICE:.2f} is as cheap as it has been in years relative
  to its own earnings power. The EPP gap of {epp_gap_pct:.1f}% is the lowest in
  this coverage universe, meaning the stock is the closest to its
  structural support floor of any name under analysis. From this
  level:
    1. Downside to EPP floor : -${CURRENT_PRICE - epp_now:.0f} (-{(1 - epp_now/CURRENT_PRICE)*100:.0f}%) — well-cushioned
    2. Upside to BASE target : +${price_b - CURRENT_PRICE:.0f} (+{(price_b/CURRENT_PRICE - 1)*100:.0f}%) over 24 months
    3. Dividend income       : +{div_yield:.1f}%/yr while waiting
    4. Total return (BASE)   : ~{(price_b/CURRENT_PRICE - 1)*100 + div_yield*2:.0f}% over 2 years (incl. dividends)

  The model composite ({adj_composite:.2f}) is essentially at BASE (2.0),
  consistent with a business where Q1 2026 comps are recovering
  (+3.8%) but consumer confidence is still below average (Conference
  Board index ~90). The structural quality assessment (SCA +{sca_adj:.3f})
  supports a slight premium above the market's current pricing.
  Proxy fair value: ${proxy_ev:.0f} — {(proxy_ev/CURRENT_PRICE - 1)*100:.0f}% above current.

  SIZING CONSIDERATIONS
  Given {div_yield:.1f}% dividend yield and the lowest EPP gap in coverage,
  MCD is suitable for a full core position. Risk of further near-term
  weakness is limited given:
    (a) already near 52-week low ($271.98 vs $280.27 current)
    (b) comp sales recovery is demonstrably underway (4 positive qtrs)
    (c) E. coli crisis anniversary effect has passed (Oct 2025)

  UPGRADE TRIGGER TO BUY: Price below $265 (EPP gap < 8.6%; Ratio B
  < 0.75) — this would represent a true panic entry below the October
  2024 crisis low, creating exceptional risk/reward.
""")

# =============================================================================
# PART 3 — NUMBERS & SIGNALS
# =============================================================================

print()
print("-" * 72)
print("  PART 3 — NUMBERS & SIGNALS")
print("-" * 72)
print()

print("  A. EPS & PRICE HISTORY (calendar year; no stock split)")
print("  -----------------------------------------------------------------")
print(f"""
  FY2019 (pre-COVID)   : Adj EPS ~$8.00  |  Price ~$190-210  |  PE ~25x
  FY2020 (COVID trough): Adj EPS ~$6.26  |  Low ~$124        |  COVID panic
  FY2021 (recovery)    : Adj EPS ~$9.77  |  Range $200-$270  |  Reopening
  FY2022 (strong cycle): Adj EPS ~$10.13 |  Range $225-$280  |  Pricing power
  FY2023 (record yr)   : Adj EPS  $11.94 |  Range $252-$300  |  Peak earnings
  FY2024 (E. coli low) : Adj EPS  $11.72 |  Low ~$255        |  Trough EPS
  FY2025 (recovery)    : Adj EPS  $12.20 |  Range $270-$342  |  Comp turns +
  FY2026E (current)    : Adj EPS ~$12.93 |  Current: ${CURRENT_PRICE:.2f}   |  Q1 $2.83 beat
  FY2027E (2-yr)       : Adj EPS ~$13.50 |  Method B target: ${price_b:.0f}
""")

print("  B. EPP FLOOR & RATIO B")
print("  -----------------------------------------------------------------")
print(f"""
  EPS_NOW    = ${EPS_NOW:.2f}   (FY2025 adj diluted; confirmed Feb 11 2026)
  EPP_MIN_PE = {EPP_MIN_PE}x       (below observed 21.8x Oct 2024 crisis floor; conservative)
  EPP_NOW    = ${epp_now:.2f}  (= ${EPS_NOW:.2f} x {EPP_MIN_PE}x)
  EPP_gap    = +{epp_gap_pct:.1f}% above floor  <-- LOWEST in coverage universe

  CONS_EPS_2YR = ${CONS_EPS_2YR:.2f}  (FY2027E adj consensus)
  CONS_EXIT_PE = {CONS_EXIT_PE}x       (mid of 22-27x historical range; franchise premium)
  Price_B      = ${price_b:.2f}  (= ${CONS_EPS_2YR:.2f} x {CONS_EXIT_PE}x)
  Ratio_B      = {rfmt(ratio_b)}  -> {signal}
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

print("  G. EPS QUALITY DECOMP  (FY2019 ${:.2f} -> FY2025 ${:.2f} = +${:.2f})".format(
    PRE_COVID_EPS, EPS_NOW, eps_g_total))
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
  52-week range          : $271.98 - $341.75  (currently near 52-week LOW)
  EPP floor              : ${epp_now:.2f}   (downside to floor: -{(1 - epp_now/CURRENT_PRICE)*100:.0f}%)
  Method B target        : ${price_b:.0f}     (upside: +{(price_b/CURRENT_PRICE - 1)*100:.0f}%)
  Dividend yield         : {div_yield:.1f}%   ($7.44/yr; 50+ consecutive annual raises)
  Ratio B                : {rfmt(ratio_b)}  -> {signal}
  Beta                   : {BETA:.2f}x  ({IDIO['idio_pct']}% idio / {IDIO['macro_pct']}% macro)
  Trailing P/E           : {trailing_pe:.1f}x  (FY2025 ${EPS_NOW:.2f}; at low end of 22-27x hist range)
  Forward P/E            : {forward_pe:.1f}x  (FY2026E ${EPS_FWD_CONSENSUS:.2f})
  2-Yr Forward P/E       : {CURRENT_PRICE/CONS_EPS_2YR:.1f}x  (FY2027E ${CONS_EPS_2YR:.2f})
  Implied 2-yr ann return: {cons_ret_ann:+.1f}%/yr  (price only; +{div_yield:.1f}%/yr div = ~{cons_ret_ann + div_yield:+.1f}%/yr total)
  Upgrade to BUY trigger : < $265  (EPP gap < 8.6%; Ratio B < 0.75)
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
print("  END OF REPORT -- MCD  |  Generated 2026-05-21")
print("=" * 72)
