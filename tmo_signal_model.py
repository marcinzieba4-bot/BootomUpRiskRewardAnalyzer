"""
Thermo Fisher Scientific Inc. (NYSE: TMO) — BottomUp Risk/Reward Signal Model

SIGNAL:  ◎ ACCUMULATE
RATIO B: 0.85x  (Method B at 22× FY2027E $27.50 = $605.00; ratio 133/157 = 0.85×)
DATE:    2026-05-25
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "TMO"
COMPANY = "Thermo Fisher Scientific Inc."
SECTOR  = "Life Sciences Tools · Instruments · Bioproduction · CRO Services · Lab Supplies"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  = 448.28   # TMO — fetched Yahoo Finance, 2026-05-22; -30% from 52-wk high
PRICE_52W_LOW  = 385.46   # June 2025 (NIH funding panic + tariff fears + instrument cycle lows)
PRICE_52W_HIGH = 643.99   # January 22, 2026 (pre-NIH-cut announcement)
SHARES_M       = 390.0    # million diluted shares outstanding
DIVIDEND_ANN   =   1.76   # ~$0.44/quarter; ~0.4% yield at current price (minimal)

# ── EPS (non-GAAP adjusted) ────────────────────────────────────────────────────
# TMO FY = calendar year. Peaked at $23.24 during COVID (testing/vaccine production
# boom), then normalized as COVID revenue collapsed FY2023. Recovery has been slow:
# NIH funding cuts (~$500M revenue) + tariff headwinds (~$400M) + China academic
# weakness + instrument down-cycle continue to pressure growth. ~60% of revenues
# are consumables/services (recurring); ~40% instruments/equipment (cyclical).
EPS_FY2022 = 23.24    # COVID boom peak: testing, PPE, vaccine production; exceptional
EPS_FY2023 = 21.55    # COVID normalization: testing revenue collapsed; -7.3% YoY
EPS_FY2024 = 21.86    # Slow recovery: pharma R&D resilient; instruments still soft; +1%
EPS_FY2025 = 22.87    # Bioproduction acceleration; +4.6% YoY; adj EPS $22.87
EPS_NOW    = 24.88    # FY2026E midpoint guidance ($24.64-$25.12); Q1 2026: $5.44 adj EPS
                       # Q1 2026: revenue $11.01B (+6% YoY; +1% organic, +3% M&A, +2% FX)

# ── EPP Floor ─────────────────────────────────────────────────────────────────
# EPS_TROUGH = extended NIH/academic funding cuts + tariff escalation + recession.
# Base: $500M NIH (~$1.28/share) + $400M tariffs (~$1.03/share) + broader recession
# (-$3-4/share via volume/pricing pressure). Starting from $22.87 FY2025:
# $22.87 - $1.28 - $1.03 - $3.50 ≈ $17.06 → use $17.50 conservative stress floor.
# FY2023 was $21.55 with COVID normalization alone; adding recession + NIH could reach
# $17-18. Note: 52-wk low ($385.46) ÷ $21.86 FY2024 = 17.6× — the market bottomed
# at ~17.6× trailing, close to the 18× EPP floor assumed here.
EPS_TROUGH = 17.50    # extended stress: NIH cuts + tariffs + recession; ~24% below FY2025
EPP_MIN_PE = 18       # life sciences tools leader; ~60% recurring revenue; premium vs pure pharma
EPP        = EPS_TROUGH * EPP_MIN_PE   # $17.50 × 18 = $315.00

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E non-GAAP consensus: ~$27.50 (extrapolating from FY2026E $24.88 at 10-11%
# CAGR; mgmt guiding 6-8% EPS growth for 2026; Simply Wall St analysts: +11.6%/yr).
# Exit P/E: 22× — discounted from historical 25-35× range. TMO de-rated from 35×
# (COVID peak) to ~18-20× (2025 lows). Recovery to 22× by 2027 is conservative:
# assumes NIH headwinds partially persist, no full re-rating.
#   At 22×: $605.00  (+35.0% from $448.28) — conservative
#   At 25×: $687.50  (+53.4%) — base case if NIH resolves and instrument cycle turns
#   At 28×: $770.00  (+71.8%) — bull case: bioproduction boom + AI drug discovery
CONS_EPS_2YR = 27.50
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
# BEAR:  Prolonged NIH cuts; tariff escalation; recession; instrument cycle stays
#        depressed 3+ years; $17.50 EPS × 15× = $262.50 → $260
# BASE:  NIH partially resolved; tariffs manageable; bioproduction steady growth;
#        FY2027E $27.50 × 21× = $577.50 → $578
# BULL:  NIH headwinds resolve; instrument supercycle inflects; AI drug discovery
#        drives tool demand; M&A adds value. FY2027E $27.50 × 26× = $715.
# XBULL: TMO becomes AI/genomics picks-and-shovels platform; biopharma boom;
#        FY2029E ~$35 × 27× = $945.
PRICE_BEAR  =  260
PRICE_BASE  =  578
PRICE_BULL  =  715
PRICE_XBULL =  945

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.40, 0.25, "Bioproduction structural growth: pharma outsourcing + mRNA/gene therapy"),
    (-0.60, 0.30, "NIH cuts $500M + tariffs $400M: $900M combined headwind; academic ~20% sales"),
    (+0.30, 0.20, "Market leader moat: #1 lab tools + instruments + CRO; extreme switching costs"),
    (-0.30, 0.15, "China academic weakness + geopolitical instrument risk; export controls"),
    (+0.25, 0.10, "AI drug discovery picks-and-shovels: proteomics, genomics, HTS instruments"),
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
  Stress EPS ($17.50) × 18× quality-moat floor. EPS_TROUGH reflects an
  extended NIH/academic funding cut scenario (~$1.28/share) layered onto
  tariff headwinds (~$1.03/share) and a mild recession (~$3.50/share
  operating leverage impact) — about 24% below FY2025 $22.87.
  EPP = $315.00.
  Calibration: 52-wk low $385.46 ÷ FY2024 $21.86 = 17.6× — the market
  bottomed within the EPP P/E band during peak NIH/tariff fear in June 2025.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E non-GAAP ~$27.50 (10-11% CAGR from FY2026E $24.88) × 22× exit
  = $605.00. At 22×: +35.0% from current $448.
  Ratio B = ($448.28 − $315.00) / ($605.00 − $448.28) = $133 / $157 = 0.85×
  → ◎ ACCUMULATE. Trading 30% off its 52-wk high; NIH/tariff headwinds
  already largely in the price; quality franchise with durable moat.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THERMO FISHER: THE PICKS-AND-SHOVELS KING — TEMPORARILY HEADWIND-BOUND
=======================================================================

Thermo Fisher is the dominant infrastructure provider for life sciences
research, pharmaceutical manufacturing, and clinical diagnostics globally.
If a scientist anywhere in the world sets up an experiment, runs an assay,
sequences a genome, or manufactures a biologic drug — there is a high
probability that TMO equipment, reagents, or services are involved. This
is not an exaggeration: TMO's product catalogue spans 1M+ SKUs. The
company commands #1 or #2 positions across analytical instruments, clinical
diagnostics, life science tools, lab supply distribution, and contract
research/manufacturing (CRO/CDMO) services. Switching costs are enormous:
scientists rely on validated protocols tied to specific instruments and
reagent lots.

The stock is off 30% from its January 2026 high of $643.99. Three headwinds
converged: (1) NIH funding cuts ($500M revenue at risk), (2) tariff impacts
($400M), and (3) a China academic spending slowdown. All three are
identifiable, quantifiable, and — critically — not structural impairments
to the business model.

Q1 2026 — SOLID DESPITE HEADWINDS
════════════════════════════════════
  Revenue:           $11.01B  (+6% YoY; +1% organic, +3% acquisition, +2% FX)
  Adjusted EPS:      $5.44    (+6% YoY; beat by $0.13 from operational outperformance)
  Clario acquisition: closed late March 2026; $30M revenue, $0.01 EPS in Q1
  Updated FY2026 guidance: revenue $47.3B-$48.1B; adj EPS $24.64-$25.12 (8-10% growth)
  Organic growth guidance: 3-4% for full year 2026

NIH FUNDING CUTS — THE HEADWIND IN DETAIL
══════════════════════════════════════════
The Trump administration's NIH funding changes (February 2026 indirect
cost cap at 15%) and academic/government lab spending freezes drove
approximately $500M of expected revenue at risk for TMO in 2026. This
primarily affects the analytical instruments and lab supply distribution
segments. Academic and government customers represent ~20% of TMO sales.

Key nuance: TMO management described customers who "feel better" about
stable NIH funding — suggesting the freeze was near peak panic by Q3 2025.
The 52-week low in June 2025 ($385.46) likely reflected the worst-case
NIH scenario; since then the stock has recovered +16% as the headwind is
better understood and partially absorbed.

Additionally, ~$200M of vaccine and gene therapy studies were canceled or
put on hold — a one-time blow to high-margin life sciences tools revenue.

TARIFF HEADWINDS — $400M IMPACT
════════════════════════════════
Pharmaceutical import tariffs translate into ~$400M of revenue headwind
for TMO (customers absorbing higher manufacturing costs → cut tool budgets).
TMO also faces incremental cost pressures on instrument components made in
China. The company is managing via supply chain optimization and pricing,
but the full 2026 tariff impact was embedded in the raised guidance of
$24.64-$25.12 — meaning guidance holds even with tariffs.

BIOPRODUCTION — THE STRUCTURAL WINNER
══════════════════════════════════════
TMO's bioproduction segment (part of Life Sciences Solutions, ~23% of
revenues) is the brightest spot:
  • Q4 2025: Life Sciences Solutions +13% YoY (led by bioproduction)
  • mRNA platform: Moderna, BioNTech, and 50+ other clients use TMO
    manufacturing infrastructure for mRNA drug production
  • Cell & gene therapy: viral vector production and cell culture media
    are proprietary TMO products; no easy substitute
  • Biologics CDMO: pharma outsourcing megatrend accelerating; GLP-1
    manufacturers (Novo, Lilly) need more production capacity → more TMO

Bioproduction is the primary bull case thesis: the shift toward biologics
and advanced therapies is secular, not cyclical.

INSTRUMENT CYCLE — INFLECTION COMING?
═══════════════════════════════════════
Analytical instruments (17% of revenues) have been soft since 2024:
  • Academic/government: NIH cuts reduced capital equipment purchases
  • China: government-directed spending pauses hit instrument sales
  • Biopharma: capacity rationalization post-COVID delayed new systems
Q4 2025: Analytical Instruments +1% YoY organically — flat, not growing.
Q1 2026: management guided instrument recovery in H2 2026 as academic
budgets normalize. Chromatography and mass spectrometry orders turning up.
The instrument cycle historically recovers 12-18 months after the trough
order rate — suggesting H2 2026 / H1 2027 inflection.

CLARIO ACQUISITION (Q1 2026)
══════════════════════════════
TMO closed its acquisition of Clario (clinical data technology and eClinical
solutions for pharmaceutical trials) in late March 2026. Clario adds:
  • ~$600-700M annual revenue in clinical trial data management
  • Deepens TMO's CRO/clinical services platform
  • Adds $0.01 EPS in Q1 2026; expected to be accretive in 2027+
This follows TMO's M&A playbook: acquire businesses with complementary
customer bases in pharmaceutical R&D services, then cross-sell TMO's
instrument and reagent portfolio.

AI DRUG DISCOVERY — THE OPTIONALITY
══════════════════════════════════════
AI-driven drug discovery companies (Recursion, Isomorphic, Exscientia,
BenevolentAI) are scaling their biology infrastructure at a rapid pace.
Every protein structure determination, every high-throughput screening
campaign, every genomic sequencing run uses TMO instruments and reagents.
As AI drug discovery moves from virtual screening to wet-lab validation,
TMO is the primary infrastructure supplier. This is not in FY2027 numbers;
it is 2028-2030 optionality. But it is real.

VALUATION — WHY IT'S ATTRACTIVE NOW
══════════════════════════════════════
  At $448.28 vs 52-wk high $643.99: -30% drawdown
  Forward P/E at $448 / FY2026E $24.88 = 18.0× (at the low end of TMO's
  historical 20-35× range; COVID was 35×; 2023 normalization floor was ~18×)
  EV/EBITDA: ~22× on 2026E — below the 5-year average of ~26×
  Free cash flow yield: ~3.5% on 2026E estimates

The current 18× is essentially the same P/E at which the market bottomed
in 2023 (COVID normalization). The difference: this time the headwinds
(NIH, tariffs) are externally imposed policy risks, not secular demand
destruction. Once policy stabilizes, the multiple should recover to 22-28×.

WHERE THE RISK/REWARD IMPROVES
════════════════════════════════
  WATCHLIST  : $415-440  (slight pullback; ratio_b ~0.9-1.0×; near autumn lows)
  ACCUMULATE : $370-395  (near/below 52-wk low; ratio_b ~0.6-0.7×; fear zone)
  BUY        : $310-340  (near EPP floor; NIH + recession fully priced)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("PART 3 — NUMBERS & SIGNALS")
print("=" * 72)
print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │  SIGNAL:  {signal_primary:<12}  │  RATIO B: {ratio_b_fmt:<10}               │
  │  TICKER:  {TICKER:<10}    │  SECTOR:  Healthcare / Life Sciences  │
  └──────────────────────────────────────────────────────────────────┘

  ----------------------------------------------------------------------
""")

print(f"  Current price         : ${CURRENT_PRICE:.2f}  (+16% from 52-wk low ${PRICE_52W_LOW}; -30% from 52-wk high ${PRICE_52W_HIGH})")
print(f"  EPP floor             : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above; 18× × ${EPS_TROUGH} stress EPS; 52-wk low ${PRICE_52W_LOW} ≈ 17.6× FY2024)")
print(f"  Method B (22× exit)   : ${price_b:.2f}  (+{(price_b/CURRENT_PRICE-1)*100:.1f}%; ratio_b = {ratio_b:.2f}× → ACCUMULATE)")
print(f"  At 25× exit           : ${CONS_EPS_2YR*25:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*25-CURRENT_PRICE):.2f}× → BUY (NIH resolution + instrument inflection)")
print(f"  At 28× exit           : ${CONS_EPS_2YR*28:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*28-CURRENT_PRICE):.2f}× → BUY (full re-rating; bioproduction + AI tools)")
print(f"  BEAR scenario         : ${PRICE_BEAR}   (-42%; prolonged NIH + recession + instrument depression)")
print(f"  BASE scenario         : ${PRICE_BASE}   (+29%; FY2027E $27.50 × 21×; NIH partial resolution)")
print(f"  BULL scenario         : ${PRICE_BULL}   (+60%; NIH resolved; instrument supercycle; $27.50 × 26×)")
print(f"  XBULL scenario        : ${PRICE_XBULL}   (+111%; AI drug discovery boom; biopharma capex surge; FY2029E $35 × 27×)")
print(f"  Forward P/E (FY2026E) : {CURRENT_PRICE/EPS_NOW:.1f}×  (${CURRENT_PRICE} / ${EPS_NOW}; low end of historical 20-35× range)")
print(f"  Forward P/E (FY2027E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (${CURRENT_PRICE} / ${CONS_EPS_2YR}; attractive on recovery trajectory)")
print(f"  EPS history           : FY22 ${EPS_FY2022} → FY23 ${EPS_FY2023} → FY24 ${EPS_FY2024} → FY25 ${EPS_FY2025} → FY26E ~${EPS_NOW}")
print(f"  Q1 2026               : Revenue $11.01B (+6% YoY); adj EPS $5.44 (+6%); beat by $0.13")
print(f"  FY2026 guidance       : Revenue $47.3-48.1B; adj EPS $24.64-25.12 (8-10% growth)")
print(f"  Bioproduction         : Life Sciences Q4 2025 +13% YoY; mRNA/gene therapy structural")
print(f"  NIH headwind          : ~$500M revenue at risk; academic/gov ~20% of sales")
print(f"  Tariff impact         : ~$400M; pharma + instrument component cost pressures")
print(f"  Clario (M&A)          : eClinical CRO platform; closed Q1 2026; deepens pharma services")
print(f"  Dividend              : ${DIVIDEND_ANN:.2f}/yr ({DIVIDEND_ANN/CURRENT_PRICE*100:.1f}% yield at ${CURRENT_PRICE}; not the investment thesis)")
print(f"  Market cap            : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  WATCHLIST entry       : $415-440  (ratio_b ~0.9-1.0×; slight pullback from current)")
print(f"  ACCUMULATE entry      : $370-395  (near/below 52-wk low; ratio_b ~0.6-0.7×)")
print(f"  BUY entry             : $310-340  (near EPP floor; worst case priced)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.65×  |  Idiosyncratic: 60%  |  Macro: 40%

  Driver                                                      Type    Wt  Note
  ─────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  NIH funding cuts + academic spending freeze                  IDIO    20%  PRIMARY BEAR: $500M headwind; multi-yr if prolonged
  Bioproduction structural growth (mRNA, cell/gene therapy)    IDIO    25%  PRIMARY BULL: secular; pharma outsourcing megatrend
  Instrument cycle recovery (H2 2026 / H1 2027 inflection?)   IDIO    20%  KEY BULL: +1% organic Q4 2025 = near-trough signal
  China academic + government spending weakness                IDIO    15%  BEAR: geopolitical; export control overhang
  M&A compounding (Clario + future deals)                      IDIO    10%  BULL: capital allocation track record; EPS accretive
  AI drug discovery picks-and-shovels demand                   IDIO    10%  OPTION VALUE: 2028+ tailwind; not in consensus""")

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
  BEAR  (${PRICE_BEAR}) : NIH cuts persist 3+ years; tariff escalation; recession.
               Instrument cycle stays depressed; biopharma capex freeze.
               EPS floors at ~$17.50; market prices 14-15× = $245-260.
               -42% from current. Tail risk (~10%); requires policy to
               actively destroy the academic research funding base.

  BASE  (${PRICE_BASE}) : NIH headwinds partially resolved by late 2026; tariffs
               manageable; bioproduction steady growth; instrument recovery
               in H2 2026. FY2027E $27.50 × 21× = $578. +29% from current.
               The most likely outcome; multiple re-rates modestly from 18×.

  BULL  (${PRICE_BULL}) : NIH funding normalizes; instrument supercycle inflects
               (academic + pharma capex both recover); AI drug discovery
               drives incremental tool demand. $27.50 × 26× = $715. +60%.
               Requires policy + cycle + AI demand to all move favourably.

  XBULL (${PRICE_XBULL}) : TMO becomes the dominant AI/genomics infrastructure platform.
               Biopharma manufacturing boom driven by GLP-1, mRNA, cell/gene
               therapies. M&A adds $5-7B revenue. FY2029E ~$35 × 27× = $945.
               +111% from current. Requires 3-4 year re-rating cycle.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-25")
print("=" * 72)
