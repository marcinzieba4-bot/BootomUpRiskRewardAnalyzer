"""
Merck & Co., Inc. (NYSE: MRK) — BottomUp Risk/Reward Signal Model

SIGNAL:  ▷ HOLD/TRIM
RATIO B: 1.91x  (Method B at 15× FY2027E $9.50 = $142.50; ratio 38/20 = 1.91×)
DATE:    2026-05-25
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "MRK"
COMPANY = "Merck & Co., Inc."
SECTOR  = "Pharmaceuticals · Oncology (Keytruda) · Cardiovascular · Vaccines · Animal Health"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  = 122.55   # MRK — fetched Yahoo Finance, 2026-05-24; near 52-wk high
PRICE_52W_LOW  =  75.40   # 52-week low: mid-2025 (Keytruda cliff + IRA pricing fears at peak)
PRICE_52W_HIGH = 125.14   # 52-week high: May 2026 recovery; stock -2% from ATH recovery high
SHARES_M       = 2535.0   # million diluted shares outstanding
DIVIDEND_ANN   =   3.08   # ~$0.77/quarter; ~2.5% yield at current price

# ── EPS (non-GAAP adjusted, excluding acquired IPR&D one-time charges) ─────────
# MRK FY = calendar year. Keytruda approval 2014 transformed MRK into the dominant
# oncology franchise globally. The Keytruda patent cliff (US 2028) is the defining
# risk for the next 5 years. Q1 2026 included a ~$9B Cidara acquisition IPR&D
# charge which depresses GAAP/reported EPS; model uses clean non-GAAP throughout.
EPS_FY2022 =  7.48    # Strong Keytruda growth; Lagevrio COVID antiviral contribution
EPS_FY2023 =  8.98    # Record non-GAAP; Lagevrio waning but Keytruda $25B+ annualised
EPS_FY2024 =  9.01    # Keytruda $29.5B FY revenue; animal health resilient; IRA risk priced
EPS_FY2025 =  9.72    # Keytruda ~$33B+; Winrevair launch; Gardasil headwinds (China)
EPS_NOW    =  8.90    # FY2026E non-GAAP excl. acquired IPR&D (guidance: $5.04-5.16 INCL.
                       # ~$3.56/share Cidara IPR&D charge → clean non-GAAP ~$8.60-9.20)
                       # Q1 2026: revenue $16.29B (+4.9% YoY); Keytruda $8.03B (+12%)

# ── EPP Floor ─────────────────────────────────────────────────────────────────
# EPS_TROUGH = post-Keytruda-cliff stress scenario (2029-2030): if Keytruda US
# revenue falls ~50% from ~$37B peak to ~$18B (biosimilars), and pipeline provides
# ~$8-10B offset (Winrevair + Cidara + oncology pipeline), net impact is ~$15-19B
# revenue loss. At 38% non-GAAP margin: ~$6-7B earnings reduction → EPS ~$6.50.
# This is the structural floor that EPP must anchor to.
# Key calibration: the 52-week low ($75.40) ≈ $6.50 × 11.6× — the market tested
# a trough P/E near EPP during peak cliff panic.
EPS_TROUGH = 6.50     # post-cliff stress floor: Keytruda -50% + limited pipeline offset
EPP_MIN_PE = 13       # Pharma floor; Merck quality but cliff risk warrants discount vs JNJ's 14×
EPP        = EPS_TROUGH * EPP_MIN_PE   # $6.50 × 13 = $84.50

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E non-GAAP consensus: ~$9.50 (pre-cliff peak; Keytruda still growing;
# Winrevair accelerating; but market will apply cliff discount to P/E by 2027)
# Exit P/E: 15× — cliff-discounted from historical 16-20× range. As 2028
# approaches, market will compress the multiple, as it did with AbbVie pre-2023.
# AbbVie traded 10-14× in 2022-2023; MRK may hold 13-16× given SC Keytruda
# extension strategy + harder-to-biosimilar IV formulation.
#   At 15×: $142.50  (+16.3% from $122.55) — conservative
#   At 16×: $152.00  (+24.0%) — base case if pipeline partially de-risks cliff
#   At 18×: $171.00  (+39.5%) — requires material pipeline execution
CONS_EPS_2YR = 9.50
CONS_EXIT_PE = 15

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
# BEAR:  Keytruda biosimilar aggressive entry; pipeline fails; EPS $5; 10× = $50
# BASE:  Keytruda gradual decline offset by Winrevair + pipeline; EPS maintains
#        ~$9.50 FY2027 but market discounts cliff; $9.50 × 14× = $133
# BULL:  SC Keytruda (Qlex) extends market exclusivity 2-3 years; Winrevair
#        ~$5B+ by 2028; new indications; $10.50 × 18× = $189
# XBULL: Pipeline delivers $20B+ in new revenue; cliff managed; FY2029E $11 × 22× = $242
PRICE_BEAR  =   50
PRICE_BASE  =  133
PRICE_BULL  =  189
PRICE_XBULL =  242

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.50, 0.30, "Keytruda $8B/qtr growing 12% YoY; 40+ approved indications; dominant PD-1"),
    (+0.40, 0.20, "Winrevair $525M/qtr growing 88% YoY; PAH franchise; potential HF expansion"),
    (-0.70, 0.25, "Keytruda US patent cliff 2028: $35B+ revenue at risk; biosimilars confirmed"),
    (+0.20, 0.15, "Pipeline: 80+ late-stage readouts; Cidara $9B (antifungal); SC Keytruda (Qlex)"),
    (-0.30, 0.10, "IRA pricing: Keytruda negotiated under Medicare; Gardasil China headwind"),
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
  Post-Keytruda-cliff stress EPS ($6.50) × 13× pharma floor. EPS_TROUGH
  is NOT the current or recent EPS — it anchors to the post-2028 scenario
  where Keytruda US revenue falls ~50% from peak ($37B → ~$18B) and the
  pipeline provides partial ($8-10B) offset. EPP = $84.50.
  Note: the 52-week low ($75.40) = ~11.6× stress EPS — the market tested
  near EPP during peak Keytruda-cliff panic in mid-2025.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E non-GAAP EPS ~$9.50 (pre-cliff peak) × 15× cliff-discounted P/E
  = $142.50. At 15×: +16.3% from current.
  Ratio B = ($122.55 − $84.50) / ($142.50 − $122.55) = $38 / $20 = 1.91×
  → ▷ HOLD/TRIM. Near 52-week high; limited upside at conservative multiple;
  EPP gap 45% reflects real post-cliff downside.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MERCK: KEYTRUDA STILL COMPOUNDING — BUT THE CLOCK IS TICKING TO 2028
======================================================================

Merck transformed itself around a single asset: Keytruda (pembrolizumab),
the world's best-selling medicine. Keytruda works by blocking the PD-1
receptor, releasing the immune system to fight cancer — a mechanism so
broadly active that it now spans 40+ approved indications across 17 tumour
types. There is no drug in history that has been this dominant, this broadly
applicable, and this deeply entrenched in oncology practice. Merck built an
empire around it — companion diagnostics, combination trials, first-line
positions. The problem: US patent exclusivity ends in 2028. What happens
then defines Merck for the next decade.

Q1 2026 — SOLID EXECUTION
═══════════════════════════
  Revenue:              $16.29B (+4.9% YoY) — beat consensus
  Keytruda:             $8.03B  (+12% YoY) — $32B+ annualised run rate
  Winrevair (sotatercept): $525M (+88% YoY) — PAH franchise scaling fast
  Keytruda SC (Qlex):   $128M   (injectable version; first quarter of launch)
  FY2026 guidance:      Revenue $65.8-67B (+1-3%); adj EPS includes $9B
                        Cidara IPR&D charge (clean non-GAAP est. ~$8.90)

KEYTRUDA: THE ASSET AND THE CLIFF
═══════════════════════════════════
Keytruda's trajectory:
  FY2022: ~$21B → FY2023: ~$25B → FY2024: ~$29.5B → FY2025: ~$33B
  FY2026E: ~$34-36B → FY2027E: ~$37-39B (peak)
  FY2028: US patent cliff begins. Biosimilar manufacturers confirmed.

Why it's harder to biosimilar than Humira:
  1. IV infusion (vs Humira subcutaneous): complex manufacturing
  2. PD-1 monoclonal antibody: protein structure more complex to replicate
  3. Companion diagnostics: PD-L1 testing pathways favour established brand
  4. Combination trials: Keytruda as backbone of 1,000+ ongoing studies
  5. Subcutaneous Keytruda (Qlex): launched 2026; SC formulation creates
     a new patent estate extending exclusivity 2-3 years on that product

Despite these advantages, biosimilar entry will happen. The AbbVie/Humira
analogy (even a slower erosion) is instructive: Humira dropped 55% in US
revenue in year 1. If Keytruda drops 30-40% by 2029, that's $11-16B in
annual revenue disappearing. No pipeline fills that gap in one year.

WINREVAIR — THE NEXT GROWTH ENGINE
════════════════════════════════════
Winrevair (sotatercept) is Merck's most strategically important new asset.
Approved March 2024 for pulmonary arterial hypertension (PAH):
  • $525M in Q1 2026 (+88% YoY) = $2B+ annualised run rate already
  • PAH is a devastating disease; sotatercept has a unique mechanism
    (activin receptor ligand trap) that complements existing therapies
  • Phase 3 STELLAR data showed mortality benefit — rare for PAH drugs
  • Potential expansion into heart failure with preserved ejection fraction
    (HFpEF) — a massive unmet need affecting 30M+ patients
  If HFpEF indication approved, Winrevair could be a $5-10B product by 2029.
  This is the most important offsetting asset to the Keytruda cliff.

THE CIDARA ACQUISITION ($9B, Q1 2026)
═══════════════════════════════════════
Merck acquired Cidara Therapeutics for ~$9B, bringing:
  • Rezafungin: IV echinocandin antifungal (once-weekly dosing advantage)
    — approved 2023; targeting invasive candidiasis, invasive aspergillosis
  • CD388 (long-acting antifungal): novel mechanism; first-in-class potential
  The $9B acquisition price is expensed as acquired IPR&D in Q1 2026 GAAP.
  Strategic rationale: antifungal resistance is a growing global health crisis;
  once-weekly dosing vs daily Cancidas (existing standard) is a meaningful
  clinical advantage in hospital settings.

PIPELINE: 80+ LATE-STAGE READOUTS
════════════════════════════════════
Merck has 80+ Phase 3 / late-stage readouts expected through 2028. Key ones:
  • Keytruda combinations: every major oncology readout extends Keytruda's
    use; each positive combo study = new line of revenue even post-cliff
  • MK-1654 (RSV antibody): potential paediatric/infant protection market
  • MK-4995: oral HPV drug (if oral Gardasil concept works)
  • V940 (mRNA cancer vaccine + Keytruda): personalised cancer vaccine
    Phase 3; Merck/Moderna partnership; early data compelling
  • Sotatercept HFpEF: pivotal trial ongoing — largest potential
  The management claim: "our pipeline will double the $35B Keytruda consensus
  sales by 2028." That's an extraordinary claim — but the 80+ readout slate
  gives statistical probability of multiple successes.

GARDASIL / ANIMAL HEALTH — HEADWINDS
══════════════════════════════════════
  Gardasil (HPV vaccine): China headwind (government-driven demand decline);
    ex-China growing but not offsetting. Revenue declined in 2025.
  Animal Health (Merck Animal Health): resilient, lower-multiple segment;
    grows 4-6%/yr; not a swing factor.

IRA DRUG PRICING IMPACT
═════════════════════════
Keytruda was selected for Medicare drug price negotiation under the IRA.
CMS announced a negotiated price reduction effective 2026. This is already
partially embedded in FY2026 guidance. The price cut is real but managed;
volume growth offsets it. Future rounds of IRA negotiation are a continued
headwind.

WHERE THE RISK/REWARD IMPROVES
════════════════════════════════
  WATCHLIST  : $100-108  (FY2027E ~10.5-11.4×; ratio_b ~1.3×; near Sept 2025 lows)
  ACCUMULATE : $88-95    (FY2027E ~9.3-10×; ratio_b ~0.8×; post-cliff fears priced)
  BUY        : $75-85    (at/near EPP floor; cliff scenario fully discounted)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("PART 3 — NUMBERS & SIGNALS")
print("=" * 72)
print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │  SIGNAL:  {signal_primary:<12}  │  RATIO B: {ratio_b_fmt:<10}               │
  │  TICKER:  {TICKER:<10}    │  SECTOR:  Healthcare / Pharma         │
  └──────────────────────────────────────────────────────────────────┘

  ----------------------------------------------------------------------
""")

print(f"  Current price         : ${CURRENT_PRICE:.2f}  (+63% from 52-wk low ${PRICE_52W_LOW}; -2% from 52-wk high ${PRICE_52W_HIGH})")
print(f"  EPP floor             : ${EPP:.2f}   (+{epp_gap_pct:.1f}% above; 13× × ${EPS_TROUGH} post-cliff stress EPS; 52-wk low ${PRICE_52W_LOW} ≈ EPP)")
print(f"  Method B (15× exit)   : ${price_b:.2f}  (+{(price_b/CURRENT_PRICE-1)*100:.1f}%; ratio_b = {ratio_b:.2f}× → HOLD/TRIM)")
print(f"  At 16× exit           : ${CONS_EPS_2YR*16:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*16-CURRENT_PRICE):.2f}× → WATCHLIST (pipeline de-risking cliff)")
print(f"  At 18× exit           : ${CONS_EPS_2YR*18:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*18-CURRENT_PRICE):.2f}× → WATCHLIST (Winrevair HFpEF + Qlex)")
print(f"  BEAR scenario         : ${PRICE_BEAR}    (-59%; cliff worse than expected; EPS $5; 10×)")
print(f"  BASE scenario         : ${PRICE_BASE}   (+9%; FY2027E $9.50 × 14×; cliff priced; Winrevair in-line)")
print(f"  BULL scenario         : ${PRICE_BULL}   (+54%; Qlex extends; Winrevair HFpEF; $10.50 × 18×)")
print(f"  XBULL scenario        : ${PRICE_XBULL}   (+97%; FY2029E ~$11 × 22×; pipeline fills cliff; mRNA cancer vaccine)")
print(f"  Forward P/E (FY2026E) : {CURRENT_PRICE/EPS_NOW:.1f}×  (${CURRENT_PRICE} / ${EPS_NOW} clean non-GAAP est; excl. Cidara IPR&D)")
print(f"  Forward P/E (FY2027E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (${CURRENT_PRICE} / ${CONS_EPS_2YR}; cheap on fwd — but cliff 1 year away)")
print(f"  EPS history           : FY22 ${EPS_FY2022} → FY23 ${EPS_FY2023} → FY24 ${EPS_FY2024} → FY25 ${EPS_FY2025} → FY26E ~${EPS_NOW}")
print(f"  Q1 2026               : Revenue $16.29B (+4.9%); Keytruda $8.03B (+12%); Winrevair $525M (+88%)")
print(f"  Keytruda Qlex (SC)    : $128M Q1 2026 (first quarter); SC formulation extends exclusivity")
print(f"  Keytruda cliff        : US patent expires 2028; $35B+ revenue at risk; biosimilars confirmed")
print(f"  Cidara acquisition    : $9B in Q1 2026; rezafungin (antifungal); expensed as acquired IPR&D")
print(f"  Dividend              : ${DIVIDEND_ANN:.2f}/yr ({DIVIDEND_ANN/CURRENT_PRICE*100:.1f}% yield at ${CURRENT_PRICE}); consistent grower")
print(f"  Market cap            : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  WATCHLIST entry       : $100-108  (FY2027E ~10.5-11.4×; ratio_b ~1.3×)")
print(f"  ACCUMULATE entry      : $88-95    (FY2027E ~9.3-10×; ratio_b ~0.8×)")
print(f"  BUY entry             : $75-85    (at/near EPP floor; cliff scenario priced)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.40×  |  Idiosyncratic: 80%  |  Macro: 20%

  Driver                                                     Type    Wt  Note
  ────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  Keytruda patent cliff 2028: $35B+ revenue at risk          IDIO    25%  PRIMARY BEAR: single biggest pharma cliff ever
  Keytruda current growth: $8B/qtr, +12% YoY, 40+ indications IDIO  30%  PRIMARY BULL: still 2+ years of peak ahead
  Winrevair growth: $525M/qtr, +88% YoY; PAH → HFpEF option  IDIO  20%  KEY BULL: if HFpEF approved = $5-10B peak
  Pipeline: 80+ late-stage; SC Keytruda (Qlex); mRNA vaccine  IDIO  15%  OPTION VALUE: Qlex extends exclusivity 2-3yr
  IRA pricing + Gardasil China headwind                       IDIO   10%  BEAR: incremental; manageable""")

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
  BEAR  (${PRICE_BEAR}) : Keytruda biosimilar aggressive entry in 2028; Winrevair
               HFpEF trial fails; pipeline delivers below expectations. EPS
               resets to ~$5; 10× trough = $50. -59% from current.
               Tail risk (~10%); AbbVie analog but larger revenue concentration.

  BASE  (${PRICE_BASE}) : Keytruda declines 30-40% post-2028 exclusivity; Winrevair
               reaches ~$4B by 2028; Qlex extends some exclusivity; pipeline
               delivers 2-3 meaningful products. FY2027E $9.50 × 14× = $133.
               +9% from current near the 52-week high. Unexciting return.

  BULL  (${PRICE_BULL}) : SC Keytruda (Qlex) extends effective exclusivity by 2-3 years;
               Winrevair HFpEF approved ($5-7B+ potential); mRNA cancer vaccine
               (V940 + Keytruda) Phase 3 positive. $10.50 × 18× = $189. +54%.
               Requires multiple simultaneous pipeline successes.

  XBULL (${PRICE_XBULL}) : Pipeline genuinely doubles the Keytruda sales base as management
               claims. Sotatercept becomes $8B+ drug; new oncology launches
               exceed $10B by 2029. FY2029E ~$11 × 22× = $242. +97%.
               Would establish MRK as post-Keytruda compounder.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-25")
print("=" * 72)
