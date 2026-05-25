"""
Caterpillar Inc. (NYSE: CAT) — BottomUp Risk/Reward Signal Model

SIGNAL:  ✕ AVOID
RATIO B: N/A (Method B at 22× FY2027E = $610 — 31% BELOW current price $880)
DATE:    2026-05-25
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "CAT"
COMPANY = "Caterpillar Inc."
SECTOR  = "Heavy Equipment · Construction · Mining · Power & Energy (Gas Turbines / Data Center)"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  = 880.00   # CAT — closed $879.89 on May 22, 2026; fetched Investing.com 2026-05-25
PRICE_52W_LOW  = 302.18   # 52-week low: April 30, 2025 (post Q1 2025 earnings; construction weak)
PRICE_52W_HIGH = 931.35   # 52-week high (intraday); closing ATH $926.93 May 6, 2026
SHARES_M       = 492.0    # million diluted shares (buybacks reducing ~3%/yr)

# ── EPS (Adjusted Profit Per Share — CAT's own non-GAAP metric) ───────────────
# CAT fiscal year = calendar year (Jan–Dec).
EPS_FY2020 =  6.44    # COVID trough — construction collapse + oil crash
EPS_FY2021 = 10.26    # Recovery
EPS_FY2022 = 13.84    # Infrastructure + commodity upcycle
EPS_FY2023 = 19.95    # Record at the time; multi-year equipment supercycle
EPS_FY2024 = 21.90    # Second consecutive record
EPS_FY2025 = 19.06    # FY2025 — construction downcycle; Q1=$4.25, Q2=$4.72, Q3=$4.95, Q4≈$5.14
EPS_TROUGH = 19.06    # FY2025 adj — most recent annual trough; 52-wk low was $302 this year
EPS_NOW    = 22.50    # FY2026E adj (Q1 2026 actual = $5.54; annualising + back-half acceleration)
EPP_MIN_PE = 14       # Industrial premium trough P/E (CAT commands above generic industrial 12×)
EPP        = EPS_TROUGH * EPP_MIN_PE   # $19.06 × 14 = $266.84

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E consensus adj EPS = $27.73 (Zacks/analyst consensus, May 2026)
# Exit P/E: CAT historical range 15-22×. Using generous 22× as ceiling.
#   At 22×: $610.06 — 31% BELOW current → N/A → AVOID
#   At 28×: $776.44 — still below current → N/A → AVOID
#   At 35×: $970.55 → ratio_b 6.77× → AVOID
CONS_EPS_2YR = 27.73
CONS_EXIT_PE = 22

# ── Computed signals ──────────────────────────────────────────────────────────
price_b = CONS_EPS_2YR * CONS_EXIT_PE

if price_b <= CURRENT_PRICE:
    ratio_b     = None
    ratio_b_fmt = "N/A"
    signal_primary = "✕ AVOID"
else:
    ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
    if   ratio_b < 0:    signal_primary = "◉ BUY"
    elif ratio_b < 0.75: signal_primary = "◉ BUY"
    elif ratio_b < 1.1:  signal_primary = "◎ ACCUMULATE"
    elif ratio_b < 1.75: signal_primary = "◐ WATCHLIST"
    elif ratio_b < 2.5:  signal_primary = "▷ HOLD/TRIM"
    else:                signal_primary = "✕ AVOID"
    ratio_b_fmt = f"{ratio_b:.2f}x"

epp_gap_pct = (CURRENT_PRICE - EPP) / EPP * 100

# ── Scenario prices ───────────────────────────────────────────────────────────
# BEAR: Construction + mining recession; EPS reset to ~$14; 18× trough
# BASE: FY2027E $27.73 × 22× fair industrial = $610
# BULL: Power & Energy re-rating sustains; market re-rates to 35× FY2027E = $970
# XBULL: CAT = dominant AI infrastructure power supplier; FY2029E $38 × 40× = $1,520
PRICE_BEAR  = 252
PRICE_BASE  = 610
PRICE_BULL  = 970
PRICE_XBULL = 1520

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.70, 0.30, "Power & Energy: data center turbines/generators (+41% Q1 2026)"),
    (+0.30, 0.20, "US construction recovery: mega projects + infrastructure bill"),
    (+0.20, 0.15, "Mining cycle: copper/lithium demand for energy transition"),
    (-0.50, 0.15, "China construction weakness (Evergrande; structural slowdown)"),
    (-0.30, 0.10, "Rate environment: high rates suppress construction starts"),
    (-0.20, 0.10, "USD strength headwind (50%+ revenue from non-US markets)"),
]
sca_raw = sum(s * w for s, w, _ in SCA_FACTORS)
sca_adj = sca_raw / 2.0

# ── Composite inference ───────────────────────────────────────────────────────
CENTRES = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
T       = 0.60

def _logit(c, x): return -((x - c) ** 2) / T
def softmax_weights(composite):
    raw = {k: math.exp(_logit(v, composite)) for k, v in CENTRES.items()}
    tot = sum(raw.values())
    return {k: v / tot for k, v in raw.items()}

def expected_price(composite):
    w = softmax_weights(composite)
    prices = {"BEAR": PRICE_BEAR, "BASE": PRICE_BASE,
              "BULL": PRICE_BULL, "XBULL": PRICE_XBULL}
    return sum(w[k] * prices[k] for k in prices)

def infer_composite(target_price, lo=1.0, hi=4.0, iters=60):
    for _ in range(iters):
        mid = (lo + hi) / 2
        if expected_price(mid) < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

market_composite = infer_composite(CURRENT_PRICE)
adj_composite    = market_composite + sca_adj

def composite_label(c):
    if   c < 1.625: return "BEAR"
    elif c < 2.375: return "BASE"
    elif c < 3.25:  return "BULL"
    else:           return "XBULL"

market_label = composite_label(market_composite)
adj_label    = composite_label(adj_composite)

# ══════════════════════════════════════════════════════════════════════════════
print("=" * 72)
print(f"  {TICKER}  —  {COMPANY}")
print(f"  {SECTOR}")
print("=" * 72)

print("""
PART 1 — FRAMEWORK OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EPP (Earnings Power Price) — structural floor
  = EPS_TROUGH × EPP_MIN_PE
  FY2025 adjusted EPS ($19.06) × 14× floor multiple. The actual 52-week low
  ($302.18) was ~16× FY2025 trough EPS — market kept a small premium above
  the pure EPP floor, consistent with CAT's quality and buyback support.
  EPP = $266.84 sits below that trough, as expected.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E consensus $27.73 × 22× (generous upper-bound for an industrial) =
  $610.06 — 31% BELOW the current price of $880. At 28× exit: $776 still
  below. Only at 35× (no precedent in CAT history at cycle mid) does Method B
  clear $880. Signal: N/A → ✕ AVOID.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CATERPILLAR: THE WORLD'S BEST INDUSTRIAL — PRICED AT 39× CURRENT-YEAR EPS
==========================================================================

Caterpillar is the undisputed global leader in heavy construction and mining
equipment. Its brand, global dealer network (5,500+ dealers), $10B+/yr
aftermarket parts & service revenue, and multi-decade customer relationships
constitute one of the deepest moats in industrials. This is not a quality
debate — CAT is elite. The debate is entirely about price.

THE RE-RATING CATALYST: POWER & ENERGY
════════════════════════════════════════
AI data centres require enormous, always-on power. Caterpillar's industrial
gas turbines, large diesel/gas generators, and backup power systems are being
ordered at record rates by hyperscalers and co-location operators. Power &
Energy (part of the Energy & Transportation segment) grew +41% YoY in Q1 2026.
The market has re-rated CAT as a physical AI infrastructure company — the pick-
and-shovel supplier of the data centre power plant buildout.

Q1 2026 — EXCEPTIONAL RESULTS (REPORTED APRIL 30, 2026)
════════════════════════════════════════════════════════
  Revenue:           $17.4B (+22% YoY)   — crushed consensus
  Adjusted EPS:      $5.54 (+30% YoY)   — beat by ~19%
  Total backlog:     $63B (record)
  Capital returns:   $5.7B in Q1 alone  (buybacks + dividends)
  Power & Energy:    +41% YoY
  Operating cash:    $1.9B

These are extraordinary results. +22% revenue growth for a company with
$65B+ in revenue is deeply unusual for a cyclical heavy equipment maker.

BUSINESS SEGMENT CONTEXT
═════════════════════════
  Construction Industries (~40% revenue):
    US holding up (infrastructure bill, commercial construction); India
    growing (mega-project pipeline strong); Europe mixed; China structurally
    impaired. The FY2025 downturn was primarily China + European weakness.
    Now recovering with the US construction mini-upcycle.

  Resource Industries (~25% revenue — mining):
    Copper demand for AI data centre cooling + EV batteries structurally
    elevated. Lithium and nickel mine expansions multi-year. This is a durable
    tailwind, though mining capex is inherently volatile.

  Energy & Transportation — Power & Energy (and growing):
    Gas turbines + generators = data centre critical infrastructure. CAT's
    gas turbines power the physical AI buildout. Record backlog ($63B) gives
    2-3 years of revenue visibility. This is the franchise-changing segment.

THE VALUATION PROBLEM: NO PRECEDENT IN CAT HISTORY
════════════════════════════════════════════════════
At $880 / $22.50 FY2026E = 39.1× forward P/E. Historical CAT P/E ranges:
  Recession/trough:   12–15×   (COVID: bottomed ~12× fwd EPS)
  Mid-cycle fair:     18–22×   (most of the 2010s)
  Supercycle peak:    24–28×   (2021–2023 infrastructure boom)
  Current:            39×      ← zero historical precedent

The +191% rally from $302 to $880 decomposed:
  EPS upgrade (FY2025 $19 → FY2026E $22.50):   +18% contribution to price
  Multiple expansion (15× → 39×):             +160% contribution to price

The multiple re-rating dwarfs the actual earnings upgrade. Power & Energy
is real, but it would need to deliver 6-8 years of +40% YoY growth — while
Construction and Mining stay flat — to justify staying at 39× forever.

ANALYST CONSENSUS: WELL BELOW CURRENT
═══════════════════════════════════════
  Average 12-month target: $714–$778  (12–19% BELOW current price)
  High target:             $1,165
  Low target:              $380
  Consensus rating:        Buy — but most ratings were issued at $400–600

WHERE THE RISK/REWARD IMPROVES
════════════════════════════════
  WATCHLIST  : $620–660  (FY2027E 22-24×; ratio_b ~1.5×; near analyst avg)
  ACCUMULATE : $530–570  (FY2027E ~19-21×; ratio_b ~0.75×; mid-cycle P/E)
  BUY        : $350–400  (near 52-wk low zone; trough P/E; ratio_b <0.5×)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("PART 3 — NUMBERS & SIGNALS")
print("=" * 72)
print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │  SIGNAL:  {signal_primary:<12}  │  RATIO B: {ratio_b_fmt:<10}               │
  │  TICKER:  {TICKER:<10}    │  SECTOR:  Industrials                  │
  └──────────────────────────────────────────────────────────────────┘

  ----------------------------------------------------------------------
""")

print(f"  Current price       : ${CURRENT_PRICE:.2f}  (+191% from 52-wk low ${PRICE_52W_LOW}; -5% from ATH ${PRICE_52W_HIGH})")
print(f"  EPP floor           : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above; 14× × ${EPS_TROUGH} FY2025 trough adj EPS)")
print(f"  Method B (22× exit) : ${price_b:.2f}  ({(price_b/CURRENT_PRICE-1)*100:.0f}% BELOW current → N/A → AVOID)")
print(f"  At 28× exit         : ${CONS_EPS_2YR*28:.2f}  (still below current → N/A)")
print(f"  At 35× exit         : ${CONS_EPS_2YR*35:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*35-CURRENT_PRICE):.2f}× → still AVOID")
print(f"  BEAR scenario       : ${PRICE_BEAR}   (-71%; construction+mining recession; EPS ~$14; 18×)")
print(f"  BASE scenario       : ${PRICE_BASE}   (-31%; FY2027E ${CONS_EPS_2YR} × 22× — fair industrial; already well below current)")
print(f"  BULL scenario       : ${PRICE_BULL}   (+10%; Power & Energy re-rating to 35× FY2027E)")
print(f"  XBULL scenario      : ${PRICE_XBULL}  (+73%; FY2029E ~$38 × 40×; CAT = dominant AI power supplier)")
print(f"  Forward P/E (FY26E) : {CURRENT_PRICE/EPS_NOW:.1f}×  (${CURRENT_PRICE} / ${EPS_NOW}; no precedent in modern CAT history)")
print(f"  Forward P/E (FY27E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (${CURRENT_PRICE} / ${CONS_EPS_2YR}; vs 18-22× historic mid-cycle fair)")
print(f"  EPS history         : FY20 ${EPS_FY2020} → FY22 ${EPS_FY2022} → FY23 ${EPS_FY2023} → FY24 ${EPS_FY2024} → FY25 ${EPS_FY2025} (trough) → FY26E ${EPS_NOW}")
print(f"  Q1 2026             : Rev $17.4B (+22%); adj EPS $5.54 (+30%); backlog $63B (record)")
print(f"  Power & Energy      : +41% YoY Q1 2026; data centre turbines/generators driving backlog")
print(f"  Capital returns     : $5.7B returned in Q1 2026 alone (buybacks + dividends)")
print(f"  Dividend            : ~$5.96/share/year (~0.7% yield at ${CURRENT_PRICE}; yield compressed by rally)")
print(f"  Market cap          : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  Analyst avg target  : $714-778  (12-19% BELOW current; Buy ratings from $400-600 levels)")
print(f"  WATCHLIST entry     : $620-660  (22-24× FY2027E; ratio_b ~1.5×)")
print(f"  ACCUMULATE entry    : $530-570  (~19-21× FY2027E; ratio_b ~0.75×)")
print(f"  BUY entry           : $350-400  (trough P/E zone; ratio_b <0.5×)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~1.10×  |  Idiosyncratic: 45%  |  Macro: 55%

  Driver                                                     Type    Wt  Note
  ────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  Power & Energy: AI data centre turbines/generators        IDIO    30%  PRIMARY: $63B backlog; +41% Q1; 2-3yr visibility
  US construction recovery (mega projects, infra bill)      MACRO   20%  CHIPS Act fabs, LNG terminals, bridges = large equipment demand
  Mining cycle: copper/lithium for energy transition        MACRO   15%  Structural multi-year; CAT mining equipment dominant globally
  China construction weakness (structural; Evergrande)      MACRO   15%  KEY BEAR: China was 20%+ of historical demand; now impaired
  Rate environment: high rates suppress construction starts MACRO   10%  US resi still constrained; commercial mixed
  USD strength headwind (50%+ non-US revenue)               MACRO   10%  Strong USD = translation headwind on reported earnings""")

print(f"""
  II. SIGNAL FACTORS (SCA Cross-Reads)
  ----------------------------------------------------------------------
  Factor                                              Score   Weight  Contrib
  ─────────────────────────────────────────────────  ──────  ──────  ───────""")
for score, weight, label in SCA_FACTORS:
    contrib = score * weight
    print(f"  {label[:50]:<50}  {score:+.1f}    {weight:.2f}    {contrib:+.3f}")
print(f"  {'':─<50}  {'':─<6}  {'':─<6}  {'':─<7}")
print(f"  {'SCA raw':50}                  {sca_raw:+.3f}")
print(f"  {'SCA adj (÷2.0)':50}                  {sca_adj:+.3f}")

print(f"""
  III. COMPOSITE INFERENCE
  ----------------------------------------------------------------------
  Market composite  : {market_composite:.3f}  ({market_label})
  Adj composite     : {adj_composite:.3f}  ({adj_label})
  Softmax weights at adj composite ({adj_composite:.3f}):""")
for k, w in softmax_weights(adj_composite).items():
    prices = {"BEAR": PRICE_BEAR, "BASE": PRICE_BASE,
              "BULL": PRICE_BULL, "XBULL": PRICE_XBULL}
    print(f"    {k:<6}: {w:.1%}  (${prices[k]})")
ep = expected_price(adj_composite)
print(f"  Expected price (adj): ${ep:.1f}  vs current ${CURRENT_PRICE}  (Δ {(ep-CURRENT_PRICE)/CURRENT_PRICE*100:+.1f}%)")

print(f"""
  IV. SCENARIOS SUMMARY
  ----------------------------------------------------------------------
  BEAR  (${PRICE_BEAR}) : US recession + China no-recovery + mining capex deferral.
               EPS resets to ~$14 (between FY2020 and FY2025 trough). At 18×
               trough P/E = $252. –71% from current. Low probability near-term
               but not negligible given 39× entry multiple.

  BASE  (${PRICE_BASE}) : FY2027E $27.73 × 22× fair industrial value = $610. Stock
               is 44% above BASE fair value today. 2-year price return: -31%.
               Dividend yield 0.7% provides minimal offset. Time loss + price
               loss = costly opportunity cost.

  BULL  (${PRICE_BULL}) : Power & Energy sustains 30%+ growth; Construction + Mining
               recover; market re-rates CAT to 35× FY2027E = $970. +10%.
               Requires everything to go right and multiple to break historical
               ceiling. Barely above current price for the bull case.

  XBULL (${PRICE_XBULL}) : CAT becomes the dominant AI infrastructure power supplier.
               FY2029E adj EPS ~$38 × 40× = $1,520. +73% over 2-3 years.
               Requires Power & Energy to sustain 35%+ CAGR through FY2029
               AND market to assign semi-like multiple to a machinery company.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-25")
print("=" * 72)
