"""
Abbott Laboratories (NYSE: ABT) — BottomUp Risk/Reward Signal Model

SIGNAL:  ◉ BUY
RATIO B: 0.62x  (Method B at 20× FY2027E $6.25 = $125.00; ratio 23/38 = 0.62×)
DATE:    2026-05-25
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "ABT"
COMPANY = "Abbott Laboratories"
SECTOR  = "MedTech · Diagnostics · Nutrition · FreeStyle Libre CGM · Cologuard · Established Pharma"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  =  87.41   # ABT — fetched Yahoo Finance, 2026-05-22; near 52-wk low
PRICE_52W_LOW  =  83.50   # est. ~May 2026 (pre-Q1 earnings trough; NEC verdict + Exact Sciences fear)
PRICE_52W_HIGH = 139.06   # June 24, 2025
SHARES_M       = 1741.0   # million diluted shares (~$152B market cap / $87.41)
DIVIDEND_ANN   =   2.52   # $0.63/quarter; 2.88% yield at current; Dividend King 52+ yrs consecutive

# ── EPS (non-GAAP adjusted) ────────────────────────────────────────────────────
# ABT FY = calendar year. Post-COVID normalization drove the 2022→2023 EPS drop:
# COVID rapid testing was a ~$2B/yr revenue line that evaporated. The business
# since has recovered on MedTech (FreeStyle Libre CGM, Structural Heart, Neuro)
# and diagnostics. FY2026 adj EPS guidance includes ~$0.20 dilution from the
# $21B Exact Sciences acquisition (closed March 2026).
EPS_FY2022 =  5.34    # COVID rapid testing peak; exceptional one-time demand
EPS_FY2023 =  4.44    # COVID normalization trough; real operating floor ex-COVID
EPS_FY2024 =  4.67    # Recovery began: MedTech growth offsetting testing decline; +5%
EPS_FY2025 =  5.15    # "Double-digit earnings growth" (Abbott newsroom); +10% YoY
EPS_NOW    =  5.48    # FY2026E midpoint guidance ($5.38-$5.58), raised post-Q1 2026
                       # Q1 2026: revenue $11.16B (+~7% YoY); adj EPS beat consensus
                       # Includes -$0.20/share Exact Sciences (Cologuard) dilution
                       # Ex-dilution underlying EPS growth: ~14% YoY

# ── EPP Floor ─────────────────────────────────────────────────────────────────
# EPS_TROUGH = NEC litigation reserve year + mild recession + Exact Sciences
# integration pressure. Starting from FY2023's $4.44 COVID-normalization trough:
#   NEC: 782 MDL cases; if $1.5-2B reserve over 2-3 years → ~$0.19-0.38/share/yr
#   Recession: volume pressure -$0.15-0.25/share
#   Floor estimate: $4.44 - $0.20 (NEC) - $0.20 (recession) ≈ $4.04 → use $4.00
# Calibration: 52-wk low ~$83.50 ÷ FY2025 $5.15 = 16.2× — market bottomed at
# exactly the EPP floor P/E of 16×, confirming anchor accuracy.
EPS_TROUGH = 4.00     # NEC reserve + recession stress; ~22% below FY2025; FY2023 was $4.44
EPP_MIN_PE = 16       # diversified healthcare (MedTech + diagnostics + nutrition); premium vs pure pharma
EPP        = EPS_TROUGH * EPP_MIN_PE   # $4.00 × 16 = $64.00

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E non-GAAP consensus: ~$6.25 (10% growth from FY2026E $5.48 + partial
# Exact Sciences dilution recovery as integration synergies build in year 2).
# Exit P/E: 20× — conservative discount from ABT's historical 22-28× range.
# NEC litigation overhang and Exact Sciences integration risk justify discount.
#   At 20×: $125.00  (+43.0% from $87.41) — conservative; NEC overhang persists
#   At 24×: $150.00  (+71.6%) — NEC settling; Cologuard re-rating begins
#   At 27×: $168.75  (+93.1%) — full re-rate; NEC resolved; CGM + Cologuard compounding
CONS_EPS_2YR = 6.25
CONS_EXIT_PE = 20

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
# BEAR:  NEC liability $3-4B (full MDL adverse outcomes); recession; Cologuard
#        integration fails; EPS resets to ~$4; 13× = $52.
# BASE:  NEC settles ~$1.5B total (partially reserved); Exact Sciences accretive
#        by 2028; FreeStyle Libre sustains 15%+ growth. FY2027E $6.25 × 18× = $113.
# BULL:  NEC resolved; FreeStyle Libre Type 2 CMS reimbursement = US market
#        expansion; Cologuard grows 20%+/yr; $6.25 × 25× = $156.
# XBULL: ABT becomes the dominant multi-franchise healthcare compounder;
#        FY2028-29E ~$7.80 × 28× = $218. CGM + Cologuard + Structural Heart
#        all firing simultaneously.
PRICE_BEAR  =   52
PRICE_BASE  =  113
PRICE_BULL  =  156
PRICE_XBULL =  218

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.60, 0.30, "FreeStyle Libre CGM: 60%+ global market; CMS Type 2 expansion; secular diabetes"),
    (-0.70, 0.30, "NEC lawsuits: 782 MDL cases; $70M April verdict; $495M MO; August 2026 trial"),
    (+0.40, 0.20, "Exact Sciences/Cologuard: #1 non-invasive colon cancer screen; 20M+ addressable"),
    (+0.20, 0.10, "Dividend King 52+ yrs; EPD emerging markets; Ensure nutrition; defensive moat"),
    (-0.30, 0.10, "Exact Sciences $0.20/share EPS dilution 2026-2027; $21B debt-funded; integration risk"),
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
  Stress EPS ($4.00) × 16× diversified healthcare floor. EPS_TROUGH
  anchors to the FY2023 COVID-normalization trough ($4.44) minus NEC
  litigation reserve charges (~$0.20/share/yr for 2-3 years) and a mild
  recession (~$0.20). This is a severe-but-plausible scenario, not the
  base case. EPP = $64.00.
  Calibration: 52-wk low ~$83.50 ÷ FY2025 $5.15 = 16.2× — the market
  bottomed at precisely the EPP floor P/E. Excellent calibration.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E ~$6.25 (10% growth + partial Exact Sciences dilution recovery)
  × 20× NEC-discounted exit = $125.00. At 20×: +43% from current.
  Ratio B = ($87.41 − $64.00) / ($125.00 − $87.41) = $23 / $38 = 0.62×
  → ◉ BUY. At 37% below 52-wk high, Abbott trades at a trough multiple
  (16× FY2026E) pricing in NEC tail risk. FreeStyle Libre + Cologuard
  undervalued at these levels.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ABBOTT: WORLD-CLASS FRANCHISE AT A LITIGATION DISCOUNT
=======================================================

Abbott Laboratories is one of the most diversified healthcare companies
on earth — MedTech, diagnostics, nutrition, and pharmaceutical segments
operating across 160 countries with ~$43B in annual revenue. The company
has raised its dividend for 52 consecutive years (Dividend King), sports
best-in-class franchises in continuous glucose monitoring (FreeStyle Libre,
the global CGM leader with 60%+ market share), cardiac rhythm management,
structural heart devices, and — as of March 2026 — colorectal cancer
screening (Cologuard, acquired via Exact Sciences for $21B).

The stock is down 37% from its June 2025 high of $139.06. The culprit is
not the business — it is the escalating NEC (necrotizing enterocolitis)
baby formula litigation against Similac. At $87.41, Abbott trades at 16×
FY2026E adjusted EPS — a trough multiple not seen since the COVID testing
normalization of 2023. The market is pricing NEC as a larger liability than
the fundamentals warrant.

Q1 2026 — BEAT AND RAISE
══════════════════════════
  Revenue:               $11.16B  (+~7% YoY) — beat consensus
  Adjusted EPS:          Beat estimates; management raised FY2026 guidance
  Medical Devices:       +13.2% YoY — FreeStyle Libre CMS reimbursement expansion
  FY2026 guidance (raised): adj EPS $5.38-$5.58 (midpoint $5.48); 8-10% growth
  Stock reaction:        +3.18% to $87.16 on earnings day — yet still near lows

The beat-and-raise shows the underlying business is healthy. The stock
barely responded because NEC litigation fear continues to dominate sentiment.

FREESTYLE LIBRE — THE CROWN JEWEL
════════════════════════════════════
FreeStyle Libre is Abbott's most valuable asset and the thesis anchor:
  • Global #1 CGM (continuous glucose monitoring) with 60%+ market share
  • 7M+ users worldwide; growing rapidly with Type 2 diabetes adoption
  • January 2025: CMS expanded reimbursement for Type 2 on basal insulin
    — this opened the ~6M Medicare/Medicaid Type 2 population in the US,
    dramatically enlarging the addressable market
  • Q1 2026: +13.2% medical devices growth driven by Libre momentum
  • Clinical data: FreeDM2 trial (2026) — FreeStyle Libre use reduced HbA1c
    by 0.6% and increased time-in-range by 2.5 hrs/day vs fingerstick
  • Competition: Dexcom has CGM share in Type 1; but Abbott's FreeStyle Libre
    wins on ease of use, cost, and Type 2 positioning
  • Runway: ~500M diabetics globally; CGM penetration still <10% overall

FreeStyle Libre alone is likely worth $50-70B in a sum-of-parts — implying
the rest of Abbott (Diagnostics, Nutrition, Pharma, Cologuard) is essentially
"free" at current prices. This is the core BUY thesis.

EXACT SCIENCES / COLOGUARD ($21B ACQUISITION, MARCH 2026)
══════════════════════════════════════════════════════════
This was Abbott's biggest deal since Alere (2017). What they acquired:
  • Cologuard: the only FDA-approved non-invasive colorectal cancer screening
    test; stool DNA-based; sensitivity 93% for Stage I-III colon cancer
  • Oncotype DX (Exact Sciences precision oncology): genomic tests guiding
    breast cancer treatment; $1B+ revenue
  • Multi-cancer early detection (MCED): next-gen liquid biopsy pipeline

Why the deal is strategically logical:
  1. Cologuard is growing 20%+ annually; ~4M tests/yr vs ~20M addressable
  2. Abbott's global distribution + brand adds international expansion
  3. Diagnostics synergies: Abbott's lab infrastructure + Cologuard test kits
  4. Preventive care megatrend: early cancer detection is the next major
     healthcare growth platform alongside CGM

Short-term: $0.20/share EPS dilution in 2026-2027 (integration costs, debt
service). Long-term: if Cologuard grows to $3B+ annual revenue by 2028,
Exact Sciences adds $0.50-0.80/share to ABT EPS when fully integrated.

NEC BABY FORMULA LITIGATION — THE BEAR RISK
════════════════════════════════════════════
This is the primary reason ABT trades at a 37% discount to its 52-wk high:
  • Necrotizing enterocolitis (NEC): devastating intestinal disease in
    premature infants; plaintiffs claim cow's milk-based Similac Special Care
    formula causes or contributes to NEC in premature neonates
  • MDL 3026 (N.D. Illinois): 782 pending federal cases as of April 2026
  • Key verdicts:
    - April 2026: $70M verdict (4 families; Chicago jury; $53M actual + $17M punitive)
    - July 2024: $495M verdict (Missouri state court)
    - March 2024: $60M verdict (Illinois state court)
  • Next bellwether trial: August 2026 (second wave of federal MDL trials)

Why the liability may be more manageable than the market prices:
  1. Mixed science: no FDA black box warning on premature infant formulas;
     major pediatric society guidelines still endorse use in NICUs where
     donor breast milk is unavailable. Abbott contests causation vigorously.
  2. Scale: 782 MDL cases + state courts. If average settlement is $1-3M
     (well below trial verdicts but more realistic for settlement): total
     $0.8-2.3B over 3-5 years = $0.16-0.46B/year = $0.09-0.26/share/yr.
     Very manageable on $5+ EPS.
  3. MDL process: the large Missouri and Chicago verdicts were outliers;
     bellwether settlements often come in significantly lower.
  4. Abbott's response: contesting all verdicts; believes science is on their
     side. No settlement discussions confirmed publicly.

Bear case: if verdicts continue at $70-495M scale × 782 cases = existential.
That scenario requires courts to sustain every verdict — extraordinarily
unlikely given the contested science and Abbott's deep-pocketed legal team.

Most likely outcome: MDL settles for $2-4B total over 3-5 years (Abbott
can fund this from free cash flow without impairing the dividend or M&A
capacity). This is less than one year of Abbott's operating cash flow.

SEGMENTS OVERVIEW
══════════════════
  MedTech (~40% revenue): FreeStyle Libre, Structural Heart (MitraClip),
    Cardiac Rhythm Mgmt, Electrophysiology, Neuromodulation. The growth
    engine. Q1 2026: +13.2% YoY.
  Diagnostics (~25% revenue): rapid testing, immunoassay, molecular;
    post-COVID normalization complete. Core Lab stable; molecular growing.
  Nutrition (~15% revenue): Similac (infant), Pediasure, Pedialyte, Ensure
    (adult). Mature, stable cash flow; NEC exposure sits here.
  Established Pharmaceuticals (~20% revenue): branded generics in emerging
    markets (India, China, Brazil, Russia). 4-6%/yr organic growth; low-
    capital intensity; supports the dividend.

THE DIVIDEND KING ANGLE
═════════════════════════
ABT has raised its dividend for 52 consecutive years — one of only ~50
companies in the S&P 500 to earn the "Dividend King" designation. At
$87.41, yield = 2.88% ($2.52/yr). The dividend is covered 2× by free
cash flow and has zero risk of being cut absent an extreme NEC outcome.
At trough valuation levels with 52-year dividend track record: income
investors who are patient will be well-compensated waiting for the thesis.

WHERE THE RISK/REWARD NOW
══════════════════════════
  BUY now        : $78-90   (current territory; EPP floor visible; NEC fear peak)
  Strong BUY add : $74-82   (if August 2026 trial verdict drives further panic selling)
  ACCUMULATE above: $91-102 (if stock recovers post-trial; ratio_b 0.7-1.0×)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("PART 3 — NUMBERS & SIGNALS")
print("=" * 72)
print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │  SIGNAL:  {signal_primary:<12}  │  RATIO B: {ratio_b_fmt:<10}               │
  │  TICKER:  {TICKER:<10}    │  SECTOR:  Healthcare / MedTech        │
  └──────────────────────────────────────────────────────────────────┘

  ----------------------------------------------------------------------
""")

print(f"  Current price         : ${CURRENT_PRICE:.2f}  (-37% from 52-wk high ${PRICE_52W_HIGH}; near 52-wk low ~${PRICE_52W_LOW})")
print(f"  EPP floor             : ${EPP:.2f}   (+{epp_gap_pct:.1f}% above; 16× × ${EPS_TROUGH} stress EPS; 52-wk low ${PRICE_52W_LOW} ≈ 16.2× FY2025)")
print(f"  Method B (20× exit)   : ${price_b:.2f}  (+{(price_b/CURRENT_PRICE-1)*100:.1f}%; ratio_b = {ratio_b:.2f}× → BUY)")
print(f"  At 24× exit           : ${CONS_EPS_2YR*24:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*24-CURRENT_PRICE):.2f}× → BUY (NEC settling; Cologuard inflecting)")
print(f"  At 27× exit           : ${CONS_EPS_2YR*27:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*27-CURRENT_PRICE):.2f}× → BUY (NEC resolved; CGM + Cologuard re-rate)")
print(f"  BEAR scenario         : ${PRICE_BEAR}    (-40%; NEC $3-4B liability + recession; EPS $4 × 13×)")
print(f"  BASE scenario         : ${PRICE_BASE}   (+29%; NEC settled $1.5B; Exact Sciences accretive; $6.25 × 18.1×)")
print(f"  BULL scenario         : ${PRICE_BULL}   (+79%; NEC resolved; FreeStyle Libre Type 2 boom; $6.25 × 25×)")
print(f"  XBULL scenario        : ${PRICE_XBULL}   (+149%; CGM + Cologuard compounding; FY2028-29E $7.80 × 28×)")
print(f"  Forward P/E (FY2026E) : {CURRENT_PRICE/EPS_NOW:.1f}×  (${CURRENT_PRICE} / ${EPS_NOW}; trough multiple; 5-yr low)")
print(f"  Forward P/E (FY2027E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (${CURRENT_PRICE} / ${CONS_EPS_2YR}; compelling on normalized earnings)")
print(f"  EPS history           : FY22 ${EPS_FY2022} → FY23 ${EPS_FY2023} → FY24 ${EPS_FY2024} → FY25 ${EPS_FY2025} → FY26E ~${EPS_NOW}")
print(f"  Q1 2026               : Revenue $11.16B (+7% YoY); Medical Devices +13.2%; guidance raised")
print(f"  FY2026 guidance       : adj EPS $5.38-5.58 (midpoint $5.48); incl. -$0.20 Exact Sciences dilution")
print(f"  FreeStyle Libre       : Global #1 CGM; CMS Type 2 reimbursement expansion Jan 2025; 60%+ share")
print(f"  Exact Sciences        : $21B deal closed March 2026; Cologuard #1 non-invasive colon screen")
print(f"  NEC litigation        : 782 MDL cases; $70M April 2026 verdict; August 2026 next bellwether")
print(f"  Dividend              : ${DIVIDEND_ANN:.2f}/yr ({DIVIDEND_ANN/CURRENT_PRICE*100:.1f}% yield); Dividend King 52+ consecutive yrs; safe FCF coverage")
print(f"  Market cap            : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  BUY zone              : $78-90   (current territory; EPP floor visible)")
print(f"  Strong add on fear    : $74-82   (August 2026 trial panic; ratio_b ~0.3-0.5×)")
print(f"  ACCUMULATE (recovery) : $91-102  (post-trial bounce; ratio_b ~0.7-1.0×)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.60×  |  Idiosyncratic: 65%  |  Macro: 35%

  Driver                                                      Type    Wt  Note
  ─────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  NEC litigation (Similac): 782 MDL; $70M April verdict        IDIO    30%  PRIMARY BEAR: August 2026 trial is key binary
  FreeStyle Libre CGM: global #1; CMS Type 2 expansion         IDIO    30%  PRIMARY BULL: secular diabetes megatrend
  Exact Sciences / Cologuard: $21B deal; EPS dilution now      IDIO    20%  BULL: accretive 2028+; dilutive 2026-27
  MedTech devices: Structural Heart, EP, Neuromodulation        IDIO    10%  BULL: steady 8-12%/yr organic growth
  Dividend King / income: 52-yr streak; 2.9% yield             IDIO    10%  DEFENSIVE: floor support during litigation""")

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
  BEAR  (${PRICE_BEAR}) : MDL verdicts continue at $70-495M scale; 782 cases create
               $3-4B+ total liability; Abbott forced to reserve aggressively;
               recession compounds pressure. EPS resets to ~$4 × 13× = $52.
               -40% from current. Requires courts to sustain outlier verdicts
               across every case — unlikely but cannot be dismissed.

  BASE  (${PRICE_BASE}) : MDL settles ~$1.5-2B over 3-5 years (industry norm for
               complex product liability MDLs). Exact Sciences adds $0.30/share
               by 2028 (synergies). FreeStyle Libre grows 15%/yr. FY2027E
               $6.25 × 18.1× = $113. +29% from current. Most likely outcome.

  BULL  (${PRICE_BULL}) : NEC litigation resolved via early settlement; Cologuard
               reaches $2.5B+ annual revenue by 2027; FreeStyle Libre Type 2
               US penetration accelerates; MedTech re-rates. $6.25 × 25× = $156.
               +79% from current. Requires NEC clarity + Cologuard inflection.

  XBULL (${PRICE_XBULL}) : CGM + Cologuard simultaneously become dominant platforms;
               Abbott becomes the #1 preventive care franchise (diabetes +
               colon cancer). FY2028-29E ~$7.80 × 28× = $218. +149%.
               Dividend at 3%+ yield would attract new income-growth buyers.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-25")
print("=" * 72)
