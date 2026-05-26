"""
Bristol-Myers Squibb Company (NYSE: BMY) — BottomUp Risk/Reward Signal Model

SIGNAL:  ▷ HOLD/TRIM
RATIO B: 2.23x  (Method B at 12× FY2027E $6.00 = $72.00; ratio 27.96/12.54 = 2.23×)
DATE:    2026-05-26
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "BMY"
COMPANY = "Bristol-Myers Squibb Company"
SECTOR  = "Large-Cap Pharma · Oncology (Opdivo/Opdualag) · Cardiovascular (Eliquis/Camzyos) · Immunology · Haematology"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  =  59.46   # BMY — Yahoo Finance, 2026-05-22; +39% from 52-wk low; near 52-wk high
PRICE_52W_LOW  =  42.52   # 52-week low (Oct 2025; LOE overhang + pipeline scepticism)
PRICE_52W_HIGH =  62.89   # 52-week high (Apr 2026; Eliquis beat + pipeline readout optimism)
SHARES_M       = 2050.0   # million diluted shares (~$121.9B market cap / $59.46)
DIVIDEND_ANN   =   2.52   # $2.52/yr (4.25% yield; 17 consecutive annual increases)

# ── EPS (non-GAAP adjusted) ────────────────────────────────────────────────────
# BMY FY = calendar year. EPS arc reflects peak at FY2023 followed by
# structural decline from Revlimid LOE (full genericization Jan 31, 2026)
# and approaching Eliquis patent cliff (US generics ~Apr 2028). The growth
# portfolio (Breyanzi, Reblozyl, Opdualag, Sotyktu, Camzyos, Cobenfy) is
# growing rapidly (+40%+ aggregate) but is not yet large enough to fully
# offset the Eliquis USD ~$1.5-2B step-down coming in 2027-2028.
EPS_FY2022 =  7.44    # actual; peak operating leverage; Revlimid still at volume-limited LOE
EPS_FY2023 =  7.51    # actual; EPS peak; Revlimid declining; Opdivo/Eliquis growth offsets
EPS_FY2024 =  7.22    # actual; Revlimid accelerating generic erosion; growth portfolio ramp
EPS_FY2025 =  6.85    # actual; Revlimid fully genericized Q1 2026; LOE accelerates
EPS_NOW    =  6.20    # FY2026E midpoint (guidance $6.05-$6.35; Q1 2026 beat $1.58 vs $1.43)
                       # Q1 2026: Revenue $11.49B (+2.6% YoY); adj EPS $1.58 (+10.5% beat)
                       # Growth portfolio 2025: ~$2B+ Reblozyl; Camzyos $1B+; Breyanzi scaling
                       # Eliquis: +10-15% 2026; EU patent expired May 2026; US generics ~Apr 2028

# ── EPP Floor ─────────────────────────────────────────────────────────────────
# EPS_TROUGH = full Eliquis LOE ($1.5-2B revenue headwind in US alone in 2028)
# + Revlimid fully gone + recession cutting oncology volumes. From FY2026E
# $6.20: severe LOE scenario takes EPS down ~44% to ~$3.50. At that trough,
# BMY still has Opdivo ($8B+ revenue) + Camzyos (HCM rare disease monopoly)
# + Breyanzi CAR-T + Reblozyl (MDS/beta-thal) + growth pipeline to support
# a floor. Pharma companies with this profile historically don't trade below
# 8-10× trough EPS. Calibration: 52-wk low $42.52 ÷ $3.50 = 12.1× —
# the market bottomed at 12× stress EPS. Even in pure LOE panic, the floor
# held well above EPP. Using EPP_MIN_PE=9× as absolute catastrophic floor
# (pharma skeleton with zero pipeline credit).
EPS_TROUGH = 3.50     # Full Eliquis LOE + full Revlimid gone + recession; ~-44% from FY2026E
EPP_MIN_PE = 9        # Absolute floor P/E: pharma with reliable Opdivo base + Camzyos
EPP        = EPS_TROUGH * EPP_MIN_PE   # $3.50 × 9 = $31.50

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E ~$6.00: EPS troughs as Eliquis US generic pressure begins to be felt
# in net price erosion (actual generics not until Apr 2028 but pricing risk
# begins 2027). Growth portfolio partially offsets: Reblozyl $2.5B+, Camzyos
# $1.5B+, Opdualag scale, Sotyktu (psoriasis + lupus expansion), Cobenfy
# (schizophrenia commercializing 2025-2026; Alzheimer's psychosis readout 2026).
# milvexian (oral factor XI inhibitor): pivotal data in AF + secondary stroke
# prevention 2026 — a blockbuster catalyst if positive ($5B+ peak potential).
# Iberdomide (MM): FDA priority review decision August 2026.
# Exit P/E: 12× — market applies ~10× trough P/E to LOE fears today (9.6× FY2026E
# on pre-Q1 2026 basis). 12× assumes mild pipeline re-rating (milvexian positive;
# Cobenfy gaining share; Iberd approval); conservative re-rate without blockbuster.
# At 12×: $72.00  (+21% from $59.46) — modest upside; ratio_b = 2.23× → HOLD/TRIM
# At 14×: $84.00  (+41%) — milvexian positive + Cobenfy scale scenario
# At 16×: $96.00  (+61%) — full pipeline re-rate (growth portfolio transitions LOE)
CONS_EPS_2YR = 6.00
CONS_EXIT_PE = 12

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
# BEAR:  milvexian fails (Phase 3); Cobenfy underwhelms (schizophrenia
#        competitive saturation); Eliquis US erosion begins 6-12 months early
#        due to price concessions; Sotyktu competition from IL-17s; recession.
#        EPS troughs at ~$3.20; market applies 10× = $32. -46% from current.
# BASE:  milvexian shows positive AF signal (secondary stroke readout mid-2026);
#        Cobenfy reaches $1B by 2027; Eliquis holds through 2027 (US generics
#        Apr 2028 on schedule); growth portfolio offsets Revlimid. FY2027E
#        $6.00 × 11.3× = $68. +14% from current. LOE transition managed.
# BULL:  milvexian gains AF + stroke approval (replaces Eliquis + warfarin;
#        $5B+ peak potential); Iberdomide approved August 2026; Cobenfy adds
#        Alzheimer's psychosis indication; multiple expands to 15×. $6.50 × 13.8×
#        = $90. +51%. Pipeline finally lifts the LOE discount.
# XBULL: milvexian becomes blockbuster; CAR-T platform (Breyanzi/BMS-986393)
#        achieves first-line haematology; Sotyktu dominates SLE (lupus) beyond
#        psoriasis; Camzyos expands to HFpEF (SEQUOIA trial). FY2028-29E ~$7.00
#        × 17.1× = $120. +102%. Full LOE-to-growth transition.
PRICE_BEAR  =  32
PRICE_BASE  =  68
PRICE_BULL  =  90
PRICE_XBULL = 120

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.35, 0.20, "Growth portfolio: Reblozyl/Camzyos/Opdualag/Sotyktu +40%+; $2B+ 2025"),
    (+0.30, 0.20, "Pipeline: milvexian AF+stroke; Cobenfy Alzheimer's; Iberdomide MM FDA Aug 2026"),
    (-0.40, 0.25, "Eliquis LOE: EU patent expired May 2026; US generics ~Apr 2028; $1.5-2B cliff"),
    (-0.30, 0.20, "Revlimid: fully genericized Jan 31 2026; -63% Q1; full-year drag"),
    (-0.20, 0.15, "Net debt $34B (gross $45.1B - cash $11.1B); limits capital allocation"),
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
  Stress EPS ($3.50) × 9× catastrophic pharma floor. EPS_TROUGH of $3.50
  represents full Eliquis US LOE (~$1.5-2B revenue step-down) + full
  Revlimid gone + recession cutting oncology volumes — a simultaneous
  triple hit. At that trough BMY still has Opdivo ($8B+ revenue), Camzyos
  (rare disease monopoly in HCM), Breyanzi (CAR-T), Reblozyl (MDS/beta-
  thal), and a deep pipeline. 9× is the absolute catastrophic floor for
  a pharma skeleton — below typical sector floor of 10-12×.
  EPP = $31.50.
  Calibration: 52-wk low $42.52 ÷ $3.50 = 12.1× stress EPS — the market
  bottomed at 12× during peak LOE panic, well ABOVE the EPP floor. This
  confirms BMY's franchise assets and dividend (4.25% yield, 17 consecutive
  increases) provide a support floor that prevents EPP-level distress.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E ~$6.00 (growth portfolio partially offsets Revlimid; Eliquis
  US still intact in 2027; milvexian and Cobenfy early contributions)
  × 12× exit P/E (mild pipeline re-rating from current 9.6×; conservative
  — requires only milvexian positive signal + Cobenfy traction to achieve)
  = $72.00.
  Ratio B = ($59.46 − $31.50) / ($72.00 − $59.46) = $27.96 / $12.54 = 2.23×
  → ▷ HOLD/TRIM. The stock is near its 52-week HIGH after a +39% recovery
  from the $42.52 low. Risk/reward is now balanced-to-unfavourable at
  current prices — the LOE discount is partially priced in but the multiple
  expansion (from 9.6× to 12×) requires pipeline catalysts that haven't yet
  delivered. Trim above $60; re-enter below $50 or on milvexian positive data.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BRISTOL-MYERS SQUIBB: MANAGING TWO PATENT CLIFFS SIMULTANEOUSLY
================================================================

Bristol-Myers Squibb is a $121B large-cap pharmaceutical company with
leading franchises in oncology (Opdivo, Opdualag, Breyanzi), cardiovascular
(Eliquis, Camzyos), and haematology (Revlimid, Reblozyl, Iberdomide). BMY
is the world's #1 oncology-focused pharma by revenue, with Opdivo alone
generating ~$8B+ in annual global revenue.

The investment thesis is defined by two converging LOE cliffs:
  1. Revlimid: fully genericized as of January 31, 2026. Q1 2026 revenue
     already -63% YoY ($349M vs $947M prior year). The full-year 2026 drag
     is ~$2-2.5B in lost revenue vs 2024. This cliff was known and priced in.
  2. Eliquis: the $10B+ anticoagulant co-promoted with Pfizer. EU patent
     expired May 2026. US generics expected ~April 2028 (subject to litigation).
     This is the LARGER and more consequential cliff — US Eliquis alone is
     ~$5.5B to BMY's P&L. A $1.5-2B step-down in BMY's share beginning in
     2028 is the primary reason the market applies a 9.6× forward P/E.

The question is: can the growth portfolio and pipeline bridge the gap?

Q1 2026 — SOLID BEAT; LOE TRANSITION ON TRACK
===============================================
  Revenue:              $11.49B  (+2.6% YoY; beat $10.88B consensus)
  Adjusted EPS:         $1.58    (beat $1.43 by 10.5%; +15% YoY; strong operating leverage)
  FY2026 adj EPS guide: $6.05-$6.35  (midpoint $6.20; raised upper end from prior $6.25)
  FY2026 revenue guide: $46.0-$47.5B  (maintained)
  Net debt:             $34B  ($45.1B gross; $11.1B cash; $10B paydown COMPLETED ahead of plan)
  Dividend:             $2.52/yr  (4.25% yield; 17 consecutive annual increases)

The Q1 beat was meaningful: $0.15 above consensus EPS suggests growth portfolio
momentum is stronger than feared. Revlimid decline ($349M; -63%) is exactly
on-plan. Eliquis still growing (+10-15% in 2026 before EU generics start).
The capital allocation story improved — $10B debt paydown completed early.

THE GROWTH PORTFOLIO — BMY'S BRIDGE STRATEGY
=============================================
BMY's "new product portfolio" — launched 2019-2024 — is now generating
~$2-3B annually and growing at 40%+:

  Reblozyl (luspatercept):
    MDS (myelodysplastic syndromes) + beta-thalassaemia + sickle cell disease.
    $2B+ in 2025. Growing 30-40%/yr. First-line MDS approval (COMMANDS trial).
    Long-duration therapy; high patient retention. Pfizer partnership (milestone
    payments but BMY retains majority economics). This is a $3B+ peak opportunity.

  Camzyos (mavacamten):
    Only approved oral therapy for obstructive hypertrophic cardiomyopathy (HCM).
    First-in-class myosin inhibitor. $1B+ in 2025. REMS program (LVOT monitoring)
    limits prescriber base but also creates a moat — safety protocols reduce
    generic substitution risk. HFpEF opportunity (SEQUOIA trial underway) could
    triple the addressable population. Peak sales: $3-4B+.

  Opdualag (nivolumab + relatlimab):
    First LAG-3 checkpoint combo. Melanoma 1L + expansion into NSCLC, MSS-CRC.
    Growing rapidly from a smaller base. Differentiated from pure PD-1 story.

  Sotyktu (deucravacitinib):
    TYK2 inhibitor for moderate-to-severe psoriasis. Approved 2022. Market share
    gaining vs Otezla (J&J, after Amgen divested). Phase 3 in lupus underway.
    Significant lupus market ($5-8B globally; few approved oral therapies).

  Breyanzi (lisocabtagene maraleucel):
    CD19-directed CAR-T for large B-cell lymphoma + CLL + follicular lymphoma.
    Now approved in multiple indications. Scaling from $500M to $1-2B+ trajectory.
    BMS-986393 (GPRC5D-targeting CAR-T) in myeloma: Phase 1/2; strong early data.

  Cobenfy (xanomeline-trospium):
    First-in-class muscarinic agonist for schizophrenia (acquired via Karuna $14B,
    2024). Approved Sep 2024. Commercial launch underway. Different MOA from D2
    antagonists (antipsychotics) — avoids metabolic side effects. Alzheimer's
    psychosis pivotal readout in 2026 — the REAL expansion opportunity ($10B+ TAM).
    If Alzheimer's psychosis approved: Cobenfy becomes a $3-5B+ franchise.

PIPELINE CATALYSTS IN 2026
============================
Six pivotal catalysts in 2026 — any one of which could materially re-rate BMY:

  milvexian (oral factor XI inhibitor):
    Atrial fibrillation: Phase 3 LIBREXIA-AF (primary readout mid-2026).
    Secondary stroke prevention: Phase 3 LIBREXIA-STROKE (data 2026).
    Factor XI inhibitors (over warfarin + DOACs): lower bleeding, equal efficacy.
    Market: Eliquis is the current standard — milvexian developed by BMS/J&J.
    If successful: milvexian could REPLACE Eliquis in AF/stroke, effectively
    extending BMY's cardiovascular dominance PAST the Eliquis patent cliff.
    This is the single most important catalyst for BMY's 2026-2030 outlook.
    Positive data = 15-20% re-rate in the stock. Failed data = multiple stays
    compressed at 9-10×.

  Iberdomide (CC-220, cereblon modulator for myeloma):
    FDA priority review. Decision expected August 2026. Phase 3 EXCALIBER-RRMM
    data support accelerated approval. A next-gen cereblon modulator targeting
    Revlimid/Pomalidomide resistant patients. If approved, helps fill the
    Revlimid revenue gap in haematology.

  Cobenfy in Alzheimer's psychosis:
    Phase 3 readout 2026. If positive: indication expansion doubles the market.
    Alzheimer's psychosis (agitation, delusions, hallucinations in AD) is a
    $10B+ TAM with no approved cholinergic treatment. Aducanumab etc. target
    amyloid — not psychosis. Cobenfy's MOA is ideally suited. Pivotal moment.

  Mezigdomide, BMS-986393, RYZ101:
    Three additional myeloma/haematology pivotal readouts in 2026. BMY is
    building a post-Revlimid haematology franchise with next-gen CelMoDs
    and CAR-T. Deep bench reduces single-point failure risk.

THE ELIQUIS CLIFF — PRICING IN THE RISK
=========================================
  Eliquis (apixaban) facts:
    BMY's share: ~40% of $13.5B global revenue = ~$5.4B to BMY (2025E)
    EU patent:    expired May 2026 → EU generic competition begins now
    US patent:    ~April 2028 (multiple litigation stays; could be earlier)
    BMY share of US Eliquis: ~$5.5B pre-genericization
    Expected step-down: ~$1.5-2.0B hit to BMY in the US in first 12 months
    Pfizer retains ~60% of US commercial rights; BMY's economics exposed

  The $42.52 lows in late 2025 reflected peak Eliquis panic pricing. From
  those levels, the stock recovered +39% as investors recognised: (a) US
  generics are still 2 years away; (b) growth portfolio is real; (c) Q1 2026
  beat demonstrated operating leverage. At $59.46 (9.6× FY2026E), BMY is
  cheap on an absolute basis — but the UPSIDE without a pipeline catalyst
  is capped at ~$68-72 (Method B). The entry at $42-48 was significantly
  better; at current levels the risk/reward has normalised.

BALANCE SHEET AND CASH FLOW
=============================
  FY2026E adj EPS:      $6.20 (guided midpoint; Q1 $1.58 beat suggests upside)
  Dividend:             $2.52/yr (4.25% yield; 17 consecutive annual increases)
  Gross debt:           $45.1B
  Cash:                 $11.1B
  Net debt:             ~$34B
  Debt paydown:         $10B completed ahead of schedule; FCF committed to debt reduction
  FCF generation:       ~$10-12B/yr (adj; before D&A and one-times)
  Investment grade:     Yes (BBB stable; rating supported by FCF coverage)

  The $34B net debt is manageable at current FCF but limits buyback capacity
  and M&A flexibility until Eliquis LOE is behind them. BMY has stated debt
  reduction is the capital allocation priority through 2027.

WHERE RISK/REWARD IMPROVES
============================
  RE-ENTER              : $48-52   (LOE pricing below Method B; ratio_b ~1.5-1.8×)
  ACCUMULATE            : $52-57   (LOE largely priced; pipeline optionality cheap; ratio_b ~1.8-2.0×)
  HOLD current           : $57-63   (milvexian/Cobenfy optionality at fair price; ratio_b 2.0-2.3×)
  TRIM above             : $63-72   (above current 52-wk high; approaching Method B ceiling)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("PART 3 — NUMBERS & SIGNALS")
print("=" * 72)
print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │  SIGNAL:  {signal_primary:<12}  │  RATIO B: {ratio_b_fmt:<10}               │
  │  TICKER:  {TICKER:<10}    │  SECTOR:  Healthcare / Large-Cap Pharma  │
  └──────────────────────────────────────────────────────────────────┘

  ----------------------------------------------------------------------
""")

print(f"  Current price         : ${CURRENT_PRICE:.2f}  (+39% from 52-wk low ${PRICE_52W_LOW}; near 52-wk high ${PRICE_52W_HIGH})")
print(f"  EPP floor             : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above; 9× × ${EPS_TROUGH} stress EPS; 52-wk low ${PRICE_52W_LOW} ÷ $3.50 = 12.1×)")
print(f"  Method B (12× exit)   : ${price_b:.2f}  (+{(price_b/CURRENT_PRICE-1)*100:.1f}%; ratio_b = {ratio_b:.2f}× → HOLD/TRIM)")
print(f"  At 14× exit           : ${CONS_EPS_2YR*14:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*14-CURRENT_PRICE):.2f}× → HOLD/TRIM (milvexian positive scenario)")
print(f"  At 16× exit           : ${CONS_EPS_2YR*16:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*16-CURRENT_PRICE):.2f}× → WATCHLIST (full pipeline re-rate)")
print(f"  BEAR scenario         : ${PRICE_BEAR}    (-46%; milvexian fails; Eliquis early erosion; EPS ~$3.20 × 10×)")
print(f"  BASE scenario         : ${PRICE_BASE}    (+14%; milvexian positive signal; growth portfolio bridges LOE; $6.00 × 11.3×)")
print(f"  BULL scenario         : ${PRICE_BULL}    (+51%; milvexian + Cobenfy AD psychosis + Iberdomide; 15× FY2027E)")
print(f"  XBULL scenario        : ${PRICE_XBULL}   (+102%; milvexian blockbuster replaces Eliquis; HFpEF Camzyos; FY2028-29E $7.00 × 17.1×)")
print(f"  Forward P/E (FY2026E) : {CURRENT_PRICE/EPS_NOW:.1f}×   (${CURRENT_PRICE} / ${EPS_NOW}; LOE-discount multiple; sector floor pricing)")
print(f"  Forward P/E (FY2027E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×   (${CURRENT_PRICE} / ${CONS_EPS_2YR}; 12× Method B exit; requires pipeline re-rate)")
print(f"  EPS history           : FY22 ${EPS_FY2022} → FY23 ${EPS_FY2023} (peak) → FY24 ${EPS_FY2024} → FY25 ${EPS_FY2025} → FY26E ${EPS_NOW}")
print(f"  Q1 2026               : Revenue $11.49B (+2.6%); adj EPS $1.58 (beat $1.43; +10.5%)")
print(f"  FY2026 guidance       : Revenue $46.0-$47.5B; adj EPS $6.05-$6.35 (midpoint $6.20)")
print(f"  Revlimid LOE          : Q1 2026 -63% ($349M); fully genericized Jan 31 2026; full-year drag ~$2-2.5B")
print(f"  Eliquis               : +10-15% growth in 2026; EU patent expired May 2026; US generics ~Apr 2028")
print(f"  Growth portfolio      : Reblozyl $2B+ (+30-40%); Camzyos $1B+; Breyanzi scaling; Sotyktu/Opdualag")
print(f"  Cobenfy               : schizophrenia commercial launch 2025; AD psychosis pivotal readout 2026")
print(f"  milvexian             : oral factor XI; AF + secondary stroke readouts 2026; $5B+ peak if approved")
print(f"  Iberdomide            : FDA priority review; decision August 2026; EXCALIBER-RRMM data")
print(f"  Net debt              : ~$34B ($45.1B gross - $11.1B cash); $10B paydown completed ahead of plan")
print(f"  Dividend              : $2.52/yr ({DIVIDEND_ANN/CURRENT_PRICE*100:.1f}% yield; 17 consecutive annual increases)")
print(f"  Market cap            : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  HOLD zone             : $57-63   (current; pipeline optionality at fair price; near 52-wk high)")
print(f"  RE-ENTER below        : $48-52   (LOE panic pricing; ratio_b ~1.5-1.8×; better entry)")
print(f"  TRIM above            : $63-72   (approaching Method B ceiling; reduce if no catalyst)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.50×  |  Idiosyncratic: 80%  |  Macro: 20%

  Driver                                                      Type    Wt  Note
  ─────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  Eliquis LOE: EU May 2026; US ~Apr 2028; $1.5-2B cliff     IDIO  25%  PRIMARY BEAR: single largest headwind
  Revlimid LOE: fully generic; -63% Q1; full-year drag       IDIO  20%  KNOWN BEAR: fully priced in by market
  milvexian (oral FXI): AF + stroke readouts 2026            IDIO  20%  PIVOT: Eliquis replacement option
  Growth portfolio: Reblozyl/Camzyos/Cobenfy scaling         IDIO  20%  BRIDGE: $2-3B now; $6-8B target
  Macro/rates: pharma pricing + healthcare reform            MACRO 15%  MODERATE: drug pricing risk (IRA)""")

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
  BEAR  (${PRICE_BEAR}) : milvexian Phase 3 fails in both AF and stroke — the single
               most important 2026 binary catalyst misses. Eliquis US erosion
               begins 6-12 months early due to price concessions by Pfizer to
               PBMs. Cobenfy underwhelms in schizophrenia (D2-class inertia).
               Growth portfolio grows but cannot offset simultaneous LOE hits.
               EPS troughs near $3.20; market applies 10× = $32. -46% from current.

  BASE  (${PRICE_BASE}) : milvexian shows positive AF signal (non-inferior to apixaban,
               lower major bleeding); Eliquis US holds on schedule through 2027;
               Cobenfy gains 5%+ schizophrenia share; Iberdomide approved Aug 2026.
               Growth portfolio reaches ~$5B aggregate in 2026. Debt continues
               declining. FY2027E $6.00 × 11.3× = $68. +14% from current.

  BULL  (${PRICE_BULL}) : milvexian gains both AF and secondary stroke prevention
               approvals — effectively becoming the post-Eliquis anticoagulant.
               Cobenfy Alzheimer's psychosis positive readout 2026 unlocks the
               $10B+ TAM. Iberdomide approved; CelMoD franchise replaces Revlimid.
               Multiple expands from 9.6× to 15×. $6.50 × 13.8× = $90. +51%.

  XBULL (${PRICE_XBULL}) : milvexian becomes a blockbuster anticoagulant; Camzyos expands
               into HFpEF (SEQUOIA trial success) — tripling the addressable HCM
               market; Breyanzi + BMS-986393 establish BMY as CAR-T leader in MM
               and lymphoma; Sotyktu dominates lupus (SLE). By FY2028-29E, BMY
               transitions fully from LOE-driven to growth-driven. $7.00 × 17.1×
               = $120. +102%. Requires multiple simultaneous successes.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-26")
print("=" * 72)
