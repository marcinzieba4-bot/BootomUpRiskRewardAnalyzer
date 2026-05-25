"""
Danaher Corporation (NYSE: DHR) — BottomUp Risk/Reward Signal Model

SIGNAL:  ◉ BUY
RATIO B: 0.61x  (Method B at 25× FY2027E $9.75 = $243.75; ratio 43/71 = 0.61×)
DATE:    2026-05-25
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "DHR"
COMPANY = "Danaher Corporation"
SECTOR  = "Life Sciences Tools · Bioprocessing (Cytiva/Pall) · Diagnostics (Cepheid) · DBS Compounder"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  = 172.93   # DHR — Yahoo Finance, 2026-05-22; -29% from 52-wk high
PRICE_52W_LOW  = 160.93   # 52-week low (bioprocessing hangover + NIH fears at peak)
PRICE_52W_HIGH = 242.80   # 52-week high (Jan 2026; pre-guidance-reset)
SHARES_M       = 708.0    # million diluted shares (~$122.4B market cap / $172.93)
DIVIDEND_ANN   =   1.08   # ~$0.27/quarter; ~0.6% yield; DHR returns capital via M&A, not dividends

# ── EPS (non-GAAP adjusted) ────────────────────────────────────────────────────
# DHR FY = calendar year. The 2022-2024 EPS arc reflects two distinct events:
# (1) COVID bioprocessing boom (2021-2022): biopharma over-ordered bioreactors/media
#     for mRNA vaccine manufacturing; Cytiva + Pall revenues surged dramatically.
# (2) Post-pandemic destocking (2022-2024): biopharma burned down excess inventory;
#     Cytiva/Pall equipment orders fell sharply for 7+ consecutive quarters.
# Note: Veralto (environmental/water quality) was spun off Sept 30, 2023. FY2022
# and FY2023 H1-H3 included Veralto; FY2024+ are clean comparable post-spinoff.
EPS_FY2022 = 10.30    # est; peak incl. Veralto + COVID bioprocessing boom; not fully comparable
EPS_FY2023 =  8.40    # est; includes Veralto Q1-Q3; bioprocessing destocking begins; transition yr
EPS_FY2024 =  7.48    # actual; clean post-Veralto; destocking trough; DBS holding margins
EPS_FY2025 =  7.80    # actual; early recovery; bioprocessing inventory normalization complete
EPS_NOW    =  8.45    # FY2026E midpoint (raised guidance $8.35-$8.55 post-Q1 2026)
                       # Q1 2026: revenue $6.0B (+3.5%); adj EPS $2.06 (+9.5%)
                       # Biotech segment +11.5% total; bioprocessing equipment orders +30% YoY
                       # (first positive YoY orders growth in ~2 years)

# ── EPP Floor ─────────────────────────────────────────────────────────────────
# EPS_TROUGH = second bioprocessing downturn + recession + NIH cuts. Starting from
# FY2024 trough ($7.48): a further destocking + academic/government spending
# contraction + macro recession could compress EPS by additional ~13% to ~$6.50.
# Calibration: 52-wk low $160.93 ÷ FY2024 $7.48 = 21.5× — the market bottomed
# at 21.5× the actual trough year. At EPP: $160.93 ÷ $6.50 = 24.8× stress EPS,
# consistent with DHR's quality commanding a premium even at extremes.
EPS_TROUGH = 6.50     # further destocking + recession; ~13% below FY2024 measured trough
EPP_MIN_PE = 20       # premium compounder floor: DBS system; ~60% recurring consumables; best-in-class FCF
EPP        = EPS_TROUGH * EPP_MIN_PE   # $6.50 × 20 = $130.00

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E ~$9.75: FY2026E $8.45 × 15.4% growth. The 15% CAGR is driven by:
# bioprocessing equipment orders +30% in Q1 2026 (equipment revenue lags orders
# by 2-4 quarters) converting to 2026-2027 revenue; Cytiva consumables recovery
# as bioreactor utilisation climbs; DBS operating leverage on recovering volumes.
# Exit P/E: 25× — DHR historically trades 30-45× during growth phases and
# 20-25× at cycle troughs. At 25×, the market is acknowledging bioprocessing
# recovery but not fully re-rating to bull-cycle multiples.
#   At 25×: $243.75  (+40.9% from $172.93) — bioprocessing recovery underway
#   At 30×: $292.50  (+69.1%) — full recovery; DBS compounding at historical pace
#   At 35×: $341.25  (+97.3%) — bull market re-rate; bioprocessing supercycle peak
CONS_EPS_2YR = 9.75
CONS_EXIT_PE = 25

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
# BEAR:  Bioprocessing stalls again; NIH cuts hit academic instruments; recession.
#        EPS stays near $7.00; market applies 17.9× = $125.
# BASE:  Bioprocessing recovery proceeds steadily; Cepheid respiratory normalises;
#        DBS delivers margin expansion. FY2027E $9.75 × 23.4× = $228.
# BULL:  Bioprocessing supercycle: Cytiva equipment + consumables both grow 15-20%;
#        Masimo adds diagnostics platform; DBS compounds. $9.75 × 30.3× = $295.
# XBULL: DHR becomes the dominant AI-bioprocessing infrastructure platform;
#        FY2028-29E ~$12 × 33.3× = $400.
PRICE_BEAR  =  125
PRICE_BASE  =  228
PRICE_BULL  =  295
PRICE_XBULL =  400

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.60, 0.30, "Bioprocessing supercycle: Cytiva orders +30% Q1 2026; first positive in 2 yrs"),
    (-0.30, 0.20, "NIH/academic funding cuts: life sciences instruments exposed; same TMO headwind"),
    (+0.50, 0.25, "DBS quality moat: Danaher Business System; ~60% recurring; best FCF convertor"),
    (-0.40, 0.15, "Diagnostics/Cepheid softness: core -4% Q1 2026; respiratory normalisation"),
    (+0.20, 0.10, "Masimo acquisition ($9.9B, H2 2026 close): pulse oximetry + patient monitoring"),
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
  Stress EPS ($6.50) × 20× DBS-quality floor. EPS_TROUGH is set ~13%
  below the FY2024 actual trough ($7.48), representing a second downturn
  layered onto a recession — a severe but calibrated stress test.
  EPP = $130.00.
  Calibration: 52-wk low $160.93 ÷ $6.50 = 24.8× stress EPS — consistent
  with DHR's quality premium. The market has never tested EPP on Danaher
  because DBS-driven FCF and recurring consumables ~60% of revenue create
  a natural floor well above structural trough P/E.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E ~$9.75 (bioprocessing equipment orders +30% Q1 2026 converts to
  revenue 2-4 quarters later; 15% EPS CAGR from FY2026E $8.45) × 25×
  recovery-cycle exit = $243.75.
  Ratio B = ($172.93 − $130.00) / ($243.75 − $172.93) = $43 / $71 = 0.61×
  → ◉ BUY. At 20.5× FY2026E, DHR is at the low end of its post-spinoff
  range, pricing in minimal bioprocessing recovery — while orders confirm
  the supercycle has begun.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DANAHER: THE BIOPROCESSING SUPERCYCLE HAS STARTED — FEW ARE WATCHING
======================================================================

Danaher is the premier life sciences tool and diagnostics compounder,
operating through three segments: Biotechnology (Cytiva + Pall, ~50%
of revenue), Life Sciences (Leica, SCIEX, Beckman Coulter LS, ~25%),
and Diagnostics (Cepheid, Beckman Coulter DX, Radiometer, ~25%). The
unifying thread is the Danaher Business System (DBS) — a proprietary
continuous improvement philosophy (kaizen, policy deployment, value-
stream mapping) applied to every acquisition, generating consistent
margin expansion and cash flow compounding over 30+ years.

The stock is down 29% from its January 2026 high of $242.80. The reason:
investors worried the bioprocessing hangover (destocking 2022-2024) would
extend further. Q1 2026 data demolished that thesis: bioprocessing
equipment orders grew +30% year-over-year — the first positive growth
in nearly two years. This is the starting gun for the next capex cycle.

Q1 2026 — INFLECTION CONFIRMED
════════════════════════════════
  Revenue:                $6.0B    (+3.5% YoY; core +0.5%)
  Adjusted EPS:           $2.06    (+9.5% YoY; beat consensus)
  FY2026 guidance raised: adj EPS $8.35-$8.55 (from $8.35-$8.50)
  Biotechnology segment:  +11.5% total; +7.0% core; orders +30% YoY
  Life Sciences segment:  +3.5% total; +0.5% core (instruments soft)
  Diagnostics segment:    -1.5% total; -4.0% core (Cepheid respiratory)
  Stock reaction:         +5-6% on earnings day despite YTD underperformance

THE BIOPROCESSING CYCLE — WHY THIS IS A BUY SIGNAL
════════════════════════════════════════════════════
Danaher's Biotechnology segment (Cytiva + Pall) is the dominant provider
of equipment and consumables for biologic drug manufacturing. Understanding
the cycle is critical to understanding the investment thesis:

2020-2022: COVID bioprocessing BOOM
  mRNA vaccine manufacturers (Moderna, BioNTech, Pfizer) ordered massive
  capacity: bioreactors, filtration systems, tangential flow filtration,
  chromatography columns, cell culture media. Cytiva + Pall revenue surged
  50-70% above trend. DHR EPS compounded at 25%+/yr.

2022-2024: Post-COVID BUST (destocking)
  COVID vaccine demand fell sharply. Biopharma had over-ordered. Customers
  stopped buying new equipment and burned down existing inventory.
  Cytiva/Pall equipment orders fell for 7+ consecutive quarters.
  DHR EPS compressed: $10.30 (FY2022) → $7.48 (FY2024) trough.

2025-2026+: RECOVERY AND SUPERCYCLE BEGINS
  Destocking is over. Customers have consumed excess inventory.
  New biologic drugs (GLP-1 analogues, ADCs, cell/gene therapy, CAR-T,
  next-gen mRNA vaccines) require fresh capital investment.
  Q1 2026: equipment orders +30% YoY — this converts to revenue with a
  2-4 quarter lag. Revenue growth of 15-20% in bioprocessing is expected
  through 2027-2028 as these orders ship and consumables ramp.

Why orders matter: equipment orders are the leading indicator for
consumables revenue. Once a biopharma installs new bioreactors, they
purchase recurring media, filters, and reagents from Cytiva/Pall for
the life of the instrument (7-15+ years). Equipment orders in 2025-2026
= sustained consumables revenue in 2027-2035.

CYTIVA + PALL — THE FRANCHISES
════════════════════════════════
  Cytiva (formerly GE Healthcare Life Sciences, acquired 2019 for $21B):
    • Single-use bioreactors: industry standard for mRNA + biologics
    • Akta chromatography systems: protein purification gold standard
    • Xuri wave bioreactor + cell culture media: cell therapy expansion
    • AI integration: optimization of yield prediction and process control
    • ~$3.5B+ annual revenue; growing 15%+ as cycle recovers

  Pall Corporation (acquired 2015 for $13.8B):
    • Filtration systems for pharmaceutical + biopharmaceutical processing
    • Crossflow filtration, depth filtration, virus filtration
    • ~$2.5B annual revenue in biopharma + industrial
    • High margin (~30%+ operating margin); mostly consumables

CEPHEID — DIAGNOSTICS WILDCARD
════════════════════════════════
  Cepheid (acquired 2016 for $4B): modular PCR rapid diagnostic systems.
  GeneXpert platform runs 400+ tests: respiratory (COVID, flu, RSV, TB),
  STI, oncology, microbiology. Installed in 33,000+ labs globally.
  • The recurring model: GeneXpert instruments → perpetual cartridge pull
  • FY2026 challenge: COVID/flu/RSV testing normalising post-pandemic
  • Core revenue -4% in Q1 2026 — lighter respiratory season
  • Long-term: molecular diagnostics remain secular growth (~10%/yr)
    especially in emerging markets where TB, STI testing is underserved

MASIMO ACQUISITION ($9.9B, H2 2026 CLOSE)
═══════════════════════════════════════════
  Announced February 17, 2026. $180/share cash offer for Masimo.
  Masimo is a specialty diagnostics company known for:
  • Pulse oximetry innovation: non-invasive blood oxygen monitoring
  • SET technology: accuracy in motion/low perfusion (hospital standard)
  • Hospital automation and patient monitoring platforms
  • ~$2B+ annual revenue; commercial + hospital + consumer segments

  Strategic rationale for DHR: adds a hospital diagnostics platform that
  complements Beckman Coulter DX and Cepheid. DBS can extract significant
  margin from Masimo's consumer health business over-investment. Expected
  EBITDA of $530M+ by 2027 under DBS management.
  Risk: Masimo acquisition price appears rich at ~5× revenue; DBS needs
  to deliver on turnaround. Integration risk in 2026-2027.

DANAHER BUSINESS SYSTEM (DBS) — THE MOAT
══════════════════════════════════════════
DBS is the structural competitive advantage that most investors
underestimate. It is not a generic "operational excellence" programme —
it is a deeply embedded culture of continuous improvement that:
  1. Applies kaizen/lean principles to every function, not just operations
  2. Uses "policy deployment" (hoshin kanri) to align strategy → tactics
  3. Drives 50-100 bps operating margin improvement per year, sustainably
  4. Creates M&A optionality: any mid-size life sciences tools company
     acquired by DHR gets DBS installed and generates 30%+ ROIC within 3-5 yr

Over 30 years, DBS has compounded book value ~20%/yr. The system works
in both growth and downturn phases — the destocking period (2022-2024)
was managed without a dividend cut or destructive dilutive equity raise.

BALANCE SHEET AND CASH FLOW
════════════════════════════
  FY2025 free cash flow: $5.3B (per annual report reference)
  Net debt: manageable; Masimo acquisition ($9.9B) will add ~$8-9B debt
  FCF yield: $5.3B / $122.4B market cap = 4.3% — attractive for quality
  Dividend: $1.08/yr ($0.27/quarter); minimal (DHR returns via M&A + buybacks)

WHERE RISK/REWARD IMPROVES
═══════════════════════════
  BUY now        : $165-185  (current zone; 20-22× FY2026E; bioprocessing cycle starting)
  Strong BUY add : $155-165  (near/at 52-wk low; ratio_b ~0.4-0.5×; fear extreme)
  ACCUMULATE     : $185-210  (moderate recovery; ratio_b 0.7-1.0×; bioprocessing data builds)

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

print(f"  Current price         : ${CURRENT_PRICE:.2f}  (-29% from 52-wk high ${PRICE_52W_HIGH}; near 52-wk low ${PRICE_52W_LOW})")
print(f"  EPP floor             : ${EPP:.2f}   (+{epp_gap_pct:.1f}% above; 20× × ${EPS_TROUGH} stress EPS; 52-wk low ${PRICE_52W_LOW} ÷ $6.50 = 24.8×)")
print(f"  Method B (25× exit)   : ${price_b:.2f}  (+{(price_b/CURRENT_PRICE-1)*100:.1f}%; ratio_b = {ratio_b:.2f}× → BUY)")
print(f"  At 30× exit           : ${CONS_EPS_2YR*30:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*30-CURRENT_PRICE):.2f}× → BUY (full bioprocessing re-rate)")
print(f"  At 35× exit           : ${CONS_EPS_2YR*35:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*35-CURRENT_PRICE):.2f}× → BUY (supercycle peak multiple)")
print(f"  BEAR scenario         : ${PRICE_BEAR}   (-28%; second destocking + recession; EPS $7.00 × 17.9×)")
print(f"  BASE scenario         : ${PRICE_BASE}   (+32%; bioprocessing recovery; DBS delivers; $9.75 × 23.4×)")
print(f"  BULL scenario         : ${PRICE_BULL}   (+71%; Cytiva + Pall supercycle; Masimo DBS turnaround; $9.75 × 30.3×)")
print(f"  XBULL scenario        : ${PRICE_XBULL}   (+131%; AI bioprocessing platform leader; FY2028-29E $12 × 33.3×)")
print(f"  Forward P/E (FY2026E) : {CURRENT_PRICE/EPS_NOW:.1f}×   (${CURRENT_PRICE} / ${EPS_NOW}; post-Veralto trough-range multiple)")
print(f"  Forward P/E (FY2027E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×   (${CURRENT_PRICE} / ${CONS_EPS_2YR}; pricing in minimal bioprocessing recovery)")
print(f"  EPS history           : FY22 ~${EPS_FY2022} → FY23 ~${EPS_FY2023} → FY24 ${EPS_FY2024} → FY25 ${EPS_FY2025} → FY26E ${EPS_NOW}")
print(f"  Q1 2026               : Revenue $6.0B (+3.5%); adj EPS $2.06 (+9.5%); bioprocessing orders +30%")
print(f"  Bioprocessing         : Cytiva + Pall; equipment orders +30% Q1 2026; first positive in 2 yrs")
print(f"  Cepheid/Diagnostics   : -4.0% core Q1 2026; respiratory normalisation; long-term secular")
print(f"  Masimo acquisition    : $9.9B offer (Feb 2026); $180/share cash; H2 2026 close expected")
print(f"  Veralto spinoff       : Sept 2023; EPS comparability: FY2024+ are clean post-spinoff")
print(f"  DBS (Danaher Business System): 30-yr compounding; kaizen culture; 50-100 bps/yr margin lift")
print(f"  FCF yield             : ~$5.3B FY2025 FCF / ~$122.4B mkt cap = 4.3%")
print(f"  Dividend              : ${DIVIDEND_ANN:.2f}/yr ({DIVIDEND_ANN/CURRENT_PRICE*100:.1f}% yield; minimal — DHR returns via M&A + buybacks)")
print(f"  Market cap            : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  BUY zone              : $165-185  (current territory; 20-22× FY2026E)")
print(f"  Strong BUY add        : $155-165  (near/at 52-wk low; ratio_b ~0.4-0.5×)")
print(f"  ACCUMULATE            : $185-210  (early recovery; ratio_b 0.7-1.0×)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.70×  |  Idiosyncratic: 65%  |  Macro: 35%

  Driver                                                      Type    Wt  Note
  ─────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  Bioprocessing cycle: Cytiva/Pall orders +30%; supercycle start  IDIO  35%  PRIMARY BULL: 2-4 qtr lag → revenue 2026-2027
  Diagnostics/Cepheid: respiratory softness; -4% core Q1 2026     IDIO  20%  BEAR: normalisation headwind; long-term secular
  DBS quality compounding: 30-yr track record; 60% recurring      IDIO  25%  QUALITY ANCHOR: structural margin protection
  NIH/academic funding cuts: instruments segment headwind          MACRO 10%  SAME AS TMO: $400-500M segment exposure
  Masimo ($9.9B) integration: DBS can turn it; deal at 5× rev     IDIO  10%  OPTION: $0.53B EBITDA by 2027; integration risk""")

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
  BEAR  (${PRICE_BEAR}) : Bioprocessing stalls — Q1 2026 orders were a false start;
               NIH/academic cuts deepen instruments weakness; Masimo
               integration disappoints. EPS stabilises near $7; multiple
               compresses to 17.9× = $125. -28% from current.
               Unlikely given order data, but cycle reversals have happened.

  BASE  (${PRICE_BASE}) : Bioprocessing recovery proceeds at 10-12% growth annually;
               Cepheid respiratory normalises and grows 6%+ on non-COVID;
               DBS drives 50-75 bps operating margin expansion; Masimo
               contributes $530M EBITDA by 2027. FY2027E $9.75 × 23.4× = $228.
               +32% from current. Most likely outcome.

  BULL  (${PRICE_BULL}) : Full bioprocessing supercycle: Cytiva equipment + consumables
               grow 15-20% through 2027; cell/gene therapy + GLP-1 biologic
               manufacturing demand surges; Masimo DBS turnaround ahead of
               schedule. $9.75 × 30.3× = $295. +71% from current.

  XBULL (${PRICE_XBULL}) : DHR becomes the AI-driven bioprocessing infrastructure
               platform — Cytiva AI tools embedded in 80%+ of biologic
               manufacturing worldwide; recurring model at massive scale.
               FY2028-29E ~$12 × 33.3× = $400. +131%.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-25")
print("=" * 72)
