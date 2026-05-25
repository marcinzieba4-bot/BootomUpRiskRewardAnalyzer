"""
Boston Scientific Corporation (NYSE: BSX) — BottomUp Risk/Reward Signal Model

SIGNAL:  ◉ BUY
RATIO B: 0.14x  (Method B at 25× FY2027E $4.00 = $100.00; ratio 5.78/42.22 = 0.14×)
DATE:    2026-05-25
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "BSX"
COMPANY = "Boston Scientific Corporation"
SECTOR  = "MedTech · Cardiovascular · Electrophysiology (Farapulse) · WATCHMAN · Neurovascular"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  =  57.78   # BSX — stockanalysis.com / CNBC, 2026-05-24; -47% from 52-wk high
PRICE_52W_LOW  =  52.52   # 52-week low (May 2026; EP competition panic + Penumbra dilution fears)
PRICE_52W_HIGH = 109.50   # 52-week high (Dec 2025; Farapulse euphoria)
SHARES_M       = 1461.0   # million diluted shares (~$84.5B market cap / $57.78)
DIVIDEND_ANN   =   0.00   # BSX pays no dividend; returns capital via M&A + buybacks

# ── EPS (non-GAAP adjusted) ────────────────────────────────────────────────────
# BSX FY = calendar year. The EPS arc reflects sustained 12-16%/yr non-GAAP
# growth fuelled by device innovation (Farapulse PFA, WATCHMAN LAA, ACURATE TAVR),
# geographic expansion, and bolt-on M&A (Nalu Medical, pending Penumbra $14.5B).
# FY2026 EPS growth slows to 9-11% due to EP headwinds (J&J Varipulse competition),
# WATCHMAN softness post-February 2026, and Urology commercial disruption.
EPS_FY2022 =  1.89    # actual; ~$1.86-1.93 midpoint guidance; pre-Farapulse growth
EPS_FY2023 =  2.37    # est; ~15% growth; Farapulse CE-mark Europe launch; WATCHMAN scaling
EPS_FY2024 =  2.72    # est; ~15% growth; Farapulse US launch (~$1B first-year); Q4 = $0.70
EPS_FY2025 =  3.07    # actual; Q1 $0.75 + Q2 $0.75 + H2 est ~$1.57; Farapulse full year +73%
EPS_NOW    =  3.37    # FY2026E midpoint (guided $3.34-$3.41; +9-11% YoY; raised to $3.37 midpt)
                       # Q1 2026: revenue $5.203B (+11.6%); adj EPS $0.80 (+6.7%); met high-end
                       # Guidance cut from 10-11% → 6.5-8% organic; EP + WATCHMAN + Urology weak

# ── EPP Floor ─────────────────────────────────────────────────────────────────
# EPS_TROUGH = EP competition intensifies + WATCHMAN structural softness + Urology
# stagnates + Penumbra integration adds interest drag + recession. From FY2026E
# $3.37: a severe scenario cuts EPS ~23% to ~$2.60. BSX's diversified 20+
# product lines (cardiovascular, EP, neuromod, urology, endoscopy) provide
# resilience — a true trough requires multiple concurrent headwinds.
# Calibration: 52-wk low $52.52 ÷ $2.60 = 20.2× — the market bottomed at
# almost exactly 20× stress EPS, confirming EPP_MIN_PE = 20× is precise.
# The stock nearly TOUCHED the EPP floor — an extremely rare event for a quality
# medtech compounder growing 9-11% adj EPS in the current year.
EPS_TROUGH = 2.60     # EP + WATCHMAN structural + Penumbra drag + recession; ~-23% from FY2026E
EPP_MIN_PE = 20       # high-quality diversified medtech floor; strong FCF; 20+ product lines
EPP        = EPS_TROUGH * EPP_MIN_PE   # $2.60 × 20 = $52.00

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E ~$4.00: management explicitly guided for "acceleration" in 2027.
# Growth drivers:
#   • Farapulse PFA: Q4 2025 +35% even WITH Varipulse competition; EP market
#     growing 18-20%; Farapulse is the global PFA share leader; clinical data
#     continues to build (ADVANTAGE trial). With Varipulse overhang digested,
#     re-acceleration to 25%+ growth expected as new CARTO integration modules ship.
#   • WATCHMAN: softness post-Feb 2026 is a timing/competitive response issue;
#     WATCHMAN remains the only FDA-approved left atrial appendage closure (LAAC)
#     device. Lux-Dx and other LAA competitors are nascent. 2027 recovery.
#   • Penumbra acquisition ($14.5B, H2 2026 close): Penumbra had ~$1B+ revenue
#     growing 15-20%/yr in mechanical thrombectomy (PE, stroke, DVT) + embolization.
#     First full-year contribution in 2027: accretive net of interest expense.
#   • Urology: new product launches in H2 2026 stabilise business; 2027 recovery.
#   • Total: $3.37 × ~19% = $4.01 ≈ $4.00 FY2027E.
# Exit P/E: 25× — BSX historically trades 30-40× adj EPS. At 25×, the market
# is still deeply sceptical about EP, Penumbra integration, and litigation.
# Even 25× is below BSX's 5-year average multiple.
#   At 25×: $100.00  (+73% from $57.78) — conservative re-rate; Ratio B = 0.14×
#   At 30×: $120.00  (+108%) — historical average multiple restored
#   At 35×: $140.00  (+142%) — full BULL scenario re-rating
CONS_EPS_2YR = 4.00
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
# BEAR:  Farapulse loses substantial share to Varipulse (CARTO integration
#        proves decisive); WATCHMAN faces structural LAA competition; Penumbra
#        closes but integrates poorly (revenue growth disappoints + interest
#        expense drag without synergy offset); Urology stays weak; recession.
#        EPS stabilises near $2.20; market applies 17.3× = $38. -34% from current.
# BASE:  Farapulse re-accelerates as BSX ships CARTO-compatible modules;
#        WATCHMAN normalises Q3-Q4 2026 after mid-Feb softness; Urology recovers
#        with new products in H2 2026; Penumbra adds ~$0.10+ EPS in 2027.
#        FY2027E $4.00 × 22.5× = $90. +56% from current.
# BULL:  Farapulse becomes the dominant global PFA system (>50% share);
#        WATCHMAN re-accelerates to 20%+ growth; Penumbra transforms BSX into
#        the leading stroke/PE intervention company; securities litigation
#        settled below $500M. $4.50 × 28.9× = $130. +125%.
# XBULL: BSX becomes the dominant cardiovascular + neurovascular medtech platform;
#        Farapulse + WATCHMAN + Penumbra triple compound; FY2028-29E ~$5.50
#        × 30× = $165. +186%. Requires Penumbra scale + EP moat preservation.
PRICE_BEAR  =  38
PRICE_BASE  =  90
PRICE_BULL  = 130
PRICE_XBULL = 165

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.40, 0.25, "Farapulse PFA: $1B+ first year; +35% Q4 2025 in 18-20% market"),
    (+0.35, 0.20, "WATCHMAN: only FDA-approved LAA closure device; temp softness"),
    (+0.25, 0.15, "Penumbra $14.5B: stroke + PE thrombectomy platform; 15-20%/yr"),
    (-0.40, 0.25, "J&J Varipulse on CARTO platform: EP competitive intensity risk"),
    (-0.30, 0.15, "Securities litigation + guidance credibility: class action filed"),
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
  Stress EPS ($2.60) × 20× diversified medtech floor. EPS_TROUGH is set
  ~23% below FY2026E guided $3.37, representing EP competitive collapse,
  WATCHMAN structural decline, Penumbra integration drag, and a recession.
  BSX's 20+ product lines across five device categories provide resilience
  that justifies 20× as the true structural floor P/E.
  EPP = $52.00.
  Calibration: 52-week low $52.52 ÷ $2.60 = 20.2× stress EPS. The market
  nearly touched the EPP floor exactly — an extraordinarily rare event for
  a quality medtech compounder with 9-11% adj EPS growth guidance in the
  CURRENT year. When a world-class business trades at its EPP floor, the
  risk/reward is asymmetric by definition.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E ~$4.00 (management guided "acceleration" in 2027; Farapulse
  re-rates; WATCHMAN normalises; Penumbra first full-year contribution;
  Urology recovery with new products) × 25× exit P/E (well below BSX's
  historical 30-40× — still discounting EP litigation, Penumbra risk,
  and competitive intensity) = $100.00.
  Ratio B = ($57.78 − $52.00) / ($100.00 − $57.78) = $5.78 / $42.22 = 0.14×
  → ◉ BUY. At 17.1× FY2026E, BSX is trading at its lowest forward multiple
  in over a decade — a multiple only justified if the EP franchise is
  permanently impaired, which current data does not support.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BOSTON SCIENTIFIC: TRADING AT ITS EPP FLOOR WITH 9-11% EPS GROWTH
===================================================================

Boston Scientific is the world's second-largest pure-play cardiovascular
device company (after Medtronic), with $20.7B in 2025 revenue and products
spanning electrophysiology (Farapulse, Rhythmia), structural heart
(WATCHMAN, ACURATE neo2), coronary intervention (Synergy, ImageCross),
peripheral intervention (Vercise, Ranger, Eluvia), endoscopy (Exalt, AXIOS),
and neuromodulation (Spectra WaveWriter, WaveWriter Alpha). The $14.5B
Penumbra acquisition (announced Jan 2026) will add mechanical thrombectomy
(stroke, pulmonary embolism, DVT) to the portfolio, creating a complete
cardiovascular + neurovascular platform.

The stock at $57.78 is -47% from its December 2025 high of $109.50. This
is NOT a business impairment — it is a guidance reset, a litigation event,
and investor anger at management credibility, compounding into a panic-
level selloff. The business continues to grow revenue at 11.6% and adj
EPS at 6-7% even in the down quarter. At 17.1× FY2026E, the market is
pricing maximum pessimism for a company growing well above GDP.

Q1 2026 — STILL GROWING; GUIDANCE RESET IS THE STORY
======================================================
  Revenue:              $5.203B  (+11.6% reported; +9.4% organic)
  Adjusted EPS:         $0.80    (+6.7% YoY; met HIGH END of guidance $0.78-$0.80)
  Cardiovascular rev:   $3.503B  — EP + structural heart strong in absolute terms
  MedSurg rev:          $1.701B  — Urology continues to drag; Endoscopy stable
  FY2026 adj EPS guide: $3.34-$3.41  (midpoint $3.375; prior guidance not disclosed
                                       but implies reset from prior ~$3.50-3.55)
  FY2026 organic growth: 6.5%-8%  (cut from 10%-11%; the single largest driver of decline)
  Q2 2026 guidance:     adj EPS $0.82-$0.84  (+6% YoY midpoint; recovery starting)

The guidance cut is painful (prior 10-11% → 6.5-8% organic) but context matters:
9-11% adj EPS growth is still faster than virtually every large-cap industrial or
pharma company. The market is punishing a deceleration, not a decline.

WHY BSX FELL -47% IN FIVE MONTHS
==================================
The selloff has three distinct legs:

1. FY2025 EARNINGS + 2026 GUIDANCE MISS (Feb 4, 2026 — stock -18% that day):
   Boston Scientific reported strong FY2025 results (Farapulse +73% for the year;
   WATCHMAN $535M in Q4) but simultaneously guided FY2026 below consensus
   expectations. Investors who had priced in continued 15%+ organic growth
   were blindsided by the slowdown. The stock fell 18% in a single session.
   This alone was the biggest single catalyst.

2. SECURITIES CLASS ACTION + EP LITIGATION (March 2026 — stock -9% on March 30):
   Multiple securities lawsuits allege that management made misleading disclosures
   about electrophysiology growth between July 23, 2025, and February 3, 2026 —
   the exact period during which expectations for EP were set sky-high. The
   lawsuits allege that BSX management knew about Varipulse competitive pressure
   earlier than disclosed. A separate day saw -5.8% when EP litigation news
   shadowed positive FARAPULSE trial data. The legal overhang compounds existing
   investor anger over the guidance miss.

3. Q1 2026 EARNINGS RE-CONFIRMATION (Apr 22, 2026 — stock -13%):
   Despite Q1 revenue +11.6% and EPS $0.80 meeting the HIGH END of guidance,
   the market reacted negatively because:
   • Full-year guidance was maintained (not raised) despite the Q1 beat
   • WATCHMAN Q1 +19.2% YoY was below expectations
   • Management tone on EP competitive dynamics remained cautious
   The stock fell 13% on a beat-and-maintain — a sign of extreme investor
   scepticism and potentially institutional capitulation.

FARAPULSE — STILL THE DOMINANT PFA SYSTEM
===========================================
Farapulse is Boston Scientific's pulsed field ablation (PFA) technology for
treating atrial fibrillation (AF). It uses irreversible electroporation to
ablate cardiac tissue without the thermal injury (esophageal damage) risk of
radiofrequency (RF) ablation. Key data:

  FY2025 Farapulse revenue:  $1B+ (first commercial year; +73% growth)
  Q4 2025 growth:            +35% YoY — still the FASTEST growing named PFA system
  BSX estimate of PFA market growth Q4 2025: 18-20% — Farapulse growing FASTER
  Varipulse market share:    gaining, but CARTO integration advantage is workflow,
                              not efficacy; data shows similar clinical outcomes
  ADVANTAGE trial:           ongoing confirmatory study; positive data builds prescriber
                              base independent of mapping platform preference

The competitive threat: J&J Varipulse is natively integrated into the CARTO EP
mapping platform, which is used in ~50% of EP labs. Electrophysiologists who use
CARTO face workflow friction when using Farapulse (requires a separate mapping
catheter or switching to Rhythmia). This is a real competitive constraint.

The counterpoint: (1) BSX is working on CARTO compatibility modules; (2) Rhythmia
(BSX's own mapping system) is gaining share; (3) Farapulse is still growing faster
than the market; (4) the EP market is large enough (~$5-7B globally) that two
strong platforms can coexist; (5) PFA penetration is still <20% of ablations
globally — the growth is in conversion from RF, not share battles.

WATCHMAN — LEFT ATRIAL APPENDAGE CLOSURE
==========================================
WATCHMAN is the world's leading LAAC (left atrial appendage closure) device,
offering patients with non-valvular AF an alternative to lifelong anticoagulants
(blood thinners). WATCHMAN FLX is the current generation.

  Q4 2025 revenue:           $535M (+29.4% YoY)
  Q1 2026 revenue:           $506M (+19.2% YoY — below expectations; softness from mid-Feb)
  Total WATCHMAN implants:   cumulative 300,000+; 3,500+ training centres globally

Why it softened: mid-February 2026 saw volumes decline below trend. Management
cited seasonal patterns, competitive dynamics, and possible physician behaviour
shifts post-guidance cut. No direct competitive threat — WATCHMAN remains the
ONLY FDA-approved LAAC device. The softness is unexplained and thus frightening
to investors, but the structural demand driver (AF population + anticoagulant
side effects) is unchanged.

PENUMBRA ACQUISITION — THE NEUROVASCULAR HOMECOMING
=====================================================
Announced January 15, 2026. $14.5B enterprise value ($374/share, cash + stock).
  • Cash: ~$11B (BSX taking on ~$10B new debt + existing cash)
  • Stock: ~27% of consideration (~3.9 BSX shares per Penumbra share)
  • Close expected: H2 2026 (subject to regulatory approval, shareholder vote)

Penumbra's business:
  • Mechanical thrombectomy: Indigo aspiration system for pulmonary embolism (PE),
    deep vein thrombosis (DVT), and peripheral arterial occlusion
  • Neurovascular: clot retrieval for ischemic stroke (ACE aspiration, JET 7)
  • Embolization: Ruby coils + PED for brain aneurysms; Oculus and Balt
  • Revenue: ~$1.1-1.2B+ at ~20% annual growth; high-margin consumables model
  • Margin profile: gross margin ~70%; EBITDA margin ~20% pre-synergies

Strategic fit: BSX sold its neurovascular division to Stryker in 2011. Penumbra
is essentially BSX "buying back" neurovascular at scale, 15 years later, with a
far stronger business. Thrombectomy is a $2-3B market growing 15-20%/yr driven
by aging populations and stroke intervention rates rising globally.

Key risk: $14.5B is BSX's largest deal ever. Net leverage post-close will be
elevated (~3.5-4× EBITDA). Interest expense adds $400-500M/yr headwind on EPS.
The deal adds +$0.05-0.10 to EPS in the first full year (2027) net of interest
and amortization — modest accretion but large long-term optionality.

SECURITIES LITIGATION — SIZED AND MANAGEABLE
=============================================
Class action alleged misleading disclosures on EP growth (July 2025 - Feb 2026).
This type of securities class action in medtech typically settles for $100-350M
(proportional to market cap loss and strength of disclosure claims).
At $350M settlement (conservative): ~$0.12/share EPS impact over 2-3 years.
Management credibility is the more lasting concern — but results speak for
themselves: revenue still growing double digits, EPS beating guidance.

BALANCE SHEET AND CASH FLOW
=============================
  FY2025 adj EPS:      $3.07 (actual; FY2025 Farapulse first full year)
  FY2026E adj EPS:     $3.37 (guided midpoint; +9-11% growth)
  FCF generation:      ~$3-3.5B/yr (12-15% FCF margin on ~$21B revenue)
  Net debt (pre-Penumbra): ~$8B; post-Penumbra: ~$18B
  Interest coverage:   ~6-7× post-Penumbra (manageable; investment grade rated)
  No dividend:         BSX returns capital exclusively through M&A + buybacks

WHERE RISK/REWARD IMPROVES
============================
  BUY now             : $52-65   (at/near EPP floor; 17× FY2026E; ratio_b 0.1-0.3×)
  ACCUMULATE          : $65-78   (recovery confirmed; ratio_b 0.3-0.6×)
  WATCHLIST           : $78-90   (Farapulse re-rate underway; ratio_b 0.6-1.0×)
  BASE fair value     : $90-100  (FY2027 acceleration delivering; 22-25× FY2027E)

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

print(f"  Current price         : ${CURRENT_PRICE:.2f}  (-47% from 52-wk high ${PRICE_52W_HIGH}; near 52-wk low ${PRICE_52W_LOW})")
print(f"  EPP floor             : ${EPP:.2f}   (+{epp_gap_pct:.1f}% above; 20× × ${EPS_TROUGH} stress EPS; 52-wk low ${PRICE_52W_LOW} ÷ $2.60 = 20.2×)")
print(f"  Method B (25× exit)   : ${price_b:.2f}  (+{(price_b/CURRENT_PRICE-1)*100:.1f}%; ratio_b = {ratio_b:.2f}× → BUY)")
print(f"  At 30× exit           : ${CONS_EPS_2YR*30:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*30-CURRENT_PRICE):.2f}× → BUY (historical average multiple)")
print(f"  At 35× exit           : ${CONS_EPS_2YR*35:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*35-CURRENT_PRICE):.2f}× → BUY (bull re-rate)")
print(f"  BEAR scenario         : ${PRICE_BEAR}    (-34%; Farapulse market share loss + Penumbra drag; EPS $2.20 × 17.3×)")
print(f"  BASE scenario         : ${PRICE_BASE}    (+56%; FY2027 acceleration; Penumbra contributes; Farapulse stabilises)")
print(f"  BULL scenario         : ${PRICE_BULL}   (+125%; Farapulse dominant PFA; WATCHMAN re-rates 20%+; Penumbra transforms)")
print(f"  XBULL scenario        : ${PRICE_XBULL}   (+186%; full cardiovascular + neurovascular platform; FY2028-29E ~$5.50 × 30×)")
print(f"  Forward P/E (FY2026E) : {CURRENT_PRICE/EPS_NOW:.1f}×   (${CURRENT_PRICE} / ${EPS_NOW}; lowest fwd P/E in 10+ years; pricing permanent impairment)")
print(f"  Forward P/E (FY2027E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×   (${CURRENT_PRICE} / ${CONS_EPS_2YR}; 25× consensus exit; 45% below historical 30-40×)")
print(f"  EPS history           : FY22 ${EPS_FY2022} → FY23 ~${EPS_FY2023} → FY24 ~${EPS_FY2024} → FY25 ${EPS_FY2025} → FY26E ${EPS_NOW}")
print(f"  Q1 2026               : Revenue $5.203B (+11.6%); adj EPS $0.80 (+6.7%); met high-end guidance")
print(f"  FY2026 guidance       : adj EPS $3.34-$3.41; organic growth 6.5-8% (cut from 10-11%)")
print(f"  Farapulse (PFA)       : $1B+ first year; +73% FY2025; +35% Q4 2025 (fastest in market growing 18-20%)")
print(f"  WATCHMAN (LAAC)       : Q4 2025 $535M (+29.4%); Q1 2026 $506M (+19.2%; below expectations)")
print(f"  Urology               : commercial turnover disruption; new hires/products in H2 2026")
print(f"  Penumbra acquisition  : $14.5B (Jan 2026); thrombectomy + neurovascular; H2 2026 close; $11B cash")
print(f"  Competition           : J&J Varipulse on CARTO platform (EP workflow advantage; ~50% of labs)")
print(f"  Securities litigation : class action (July 2025-Feb 2026 class period); EP disclosures")
print(f"  No dividend           : BSX returns capital via M&A + buybacks; FCF ~$3-3.5B/yr")
print(f"  Market cap            : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  BUY zone              : $52-65   (at/near EPP floor; 52-wk low $52.52; ratio_b 0.1-0.3×)")
print(f"  ACCUMULATE            : $65-78   (recovery confirmed by data; ratio_b 0.3-0.6×)")
print(f"  WATCHLIST             : $78-90   (Farapulse re-rate underway; ratio_b 0.6-1.0×)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.80×  |  Idiosyncratic: 75%  |  Macro: 25%

  Driver                                                      Type    Wt  Note
  ─────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  Farapulse PFA: $1B+ yr1; +35% Q4 even with competition   IDIO  25%  PRIMARY BULL: EP market still growing 18-20%
  WATCHMAN: only FDA-approved LAA closure; temp softness    IDIO  20%  FRANCHISE: no direct competitor; AF aging driver
  J&J Varipulse: CARTO integration workflow advantage       IDIO  25%  BEAR: competitive headwind; BSX working on fix
  Penumbra $14.5B: neurovascular + thrombectomy platform    IDIO  20%  OPTION: stroke/PE TAM $2-3B growing 15-20%
  Macro/rates: device cycle; hospital capital spending      MACRO 10%  MODERATE: rates falling = hospital budget relief""")

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
  BEAR  (${PRICE_BEAR}) : Farapulse permanently loses EP market share to Varipulse —
               CARTO workflow proves decisive and BSX cannot close the gap.
               WATCHMAN faces a structural competitor (EU device approved).
               Penumbra closes but integration fails (cost overruns, talent
               flight, $400M+ interest expense without revenue upside). Urology
               stays broken. EPS near $2.20; market applies 17.3× = $38.
               -34% from current. Requires 3 simultaneous impairments.

  BASE  (${PRICE_BASE}) : BSX ships CARTO-compatible Farapulse module (H2 2026-2027);
               WATCHMAN normalises from Q3 2026 as seasonal patterns clear;
               Urology recovers with new product launches in H2 2026; Penumbra
               closes and contributes ~$0.10 adj EPS in 2027; securities
               litigation settled for $200-350M (one-time charge). FY2027E
               $4.00 × 22.5× = $90. +56% from current.

  BULL  (${PRICE_BULL}) : Farapulse re-establishes PFA leadership globally (+40%/yr);
               WATCHMAN re-accelerates to 20%+ growth as AF population ages
               into LAAC eligibility; Penumbra becomes BSX's fastest-growing
               segment (mechanical thrombectomy market penetration); litigation
               settled below $250M. Multiple expands to 29× on acceleration.
               $4.50 × 28.9× = $130. +125%.

  XBULL (${PRICE_XBULL}) : BSX establishes the dominant cardiac + neurovascular platform:
               Farapulse + WATCHMAN + Penumbra triple-compound at 15-20%/yr;
               EP market grows faster than expected as PFA converts RF users;
               Penumbra generates $2.5B revenue by 2029; stroke intervention
               rates double. FY2028-29E ~$5.50 × 30× = $165. +186%.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-25")
print("=" * 72)
