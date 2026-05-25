"""
AbbVie Inc. (NYSE: ABBV) — BottomUp Risk/Reward Signal Model

SIGNAL:  ◐ WATCHLIST
RATIO B: 1.30x  (Method B at 18× FY2027E $16 = $288; ratio 94/72 = 1.30×)
DATE:    2026-05-25
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "ABBV"
COMPANY = "AbbVie Inc."
SECTOR  = "Pharmaceuticals · Immunology · Oncology · Neuroscience · Aesthetics"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  = 215.70   # ABBV — fetched from Yahoo Finance / Google Finance, 2026-05-22
PRICE_52W_LOW  = 158.00   # approx 52-week low (late-2024 / early-2025 Humira erosion trough)
PRICE_52W_HIGH = 244.81   # 52-week high
SHARES_M       = 1768.0   # million diluted shares (~$381B market cap / $215.70)
DIVIDEND_ANN   =   6.92   # $1.73/quarter × 4; 3.21% yield at current price

# ── EPS (adjusted / non-GAAP) ─────────────────────────────────────────────────
# AbbVie FY = calendar year. Spun off from Abbott in 2013.
# The post-Humira narrative: Humira biosimilars entered 2023 (US); AbbVie guided
# $8-9B peak annual erosion. Skyrizi + Rinvoq are the replacement engine.
EPS_FY2022 = 13.77    # Pre-biosimilar peak; Humira still at $21B revenue
EPS_FY2023 = 11.21    # Biosimilar entry: US Humira revenue ~$14B (-33%); Skyrizi/Rinvoq offset partial
EPS_FY2024 = 10.12    # TROUGH: Humira erosion at maximum (~$9B US); Skyrizi $10.4B, Rinvoq $6.0B
EPS_FY2025 = 12.12    # Recovery begins: Skyrizi $15.2B + Rinvoq $10.7B = $25.9B combined
                       # Already exceed AbbVie's own 2027 combined guidance by $500M ahead of schedule
EPS_NOW    = 14.18    # FY2026E adj (raised guidance midpoint $14.08-14.28 after Q1 beat)
                       # Q1 2026: net revenues $15.0B (+12.4% YoY); adj EPS $2.65
                       # Includes -$0.41 unfavorable IPR&D/milestone impact YTD

# ── EPP Floor ─────────────────────────────────────────────────────────────────
# Trough EPS = FY2024 ($10.12): the verified Humira-erosion floor before
# Skyrizi/Rinvoq fully took over. AbbVie carries significant Allergan debt
# (~$14B net) from the 2020 $63B acquisition, so a 12× floor P/E (vs JNJ's
# 14×) reflects that leverage risk at the trough.
EPS_TROUGH = 10.12    # FY2024 adj EPS — Humira-cliff trough; verified
EPP_MIN_PE = 12       # Leveraged specialty pharma floor; lower than pure-pharma 14× due to Allergan debt
EPP        = EPS_TROUGH * EPP_MIN_PE   # $10.12 × 12 = $121.44

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E consensus adj EPS: ~$16 (per analyst consensus; AbbVie itself says
# upside to this — Skyrizi alone expected to beat $33B sell-side peak estimate).
# Exit P/E: 18× — AbbVie has historically traded at 10-22× depending on
# Humira cliff fear. As the cliff is absorbed and Skyrizi/Rinvoq dominance
# becomes clear, multiple should re-rate from current 13.5× toward 18-20×.
# Using 18× as conservative target; upside via multiple expansion.
#   At 18×: $288.00  (+33.5% from $215.70)
#   At 20×: $320.00  (+48.4% — achievable on clean cliff absorption + pipeline)
#   At 22×: $352.00  (+63.2% — full re-rate: would make ABBV ACCUMULATE territory)
CONS_EPS_2YR = 16.00
CONS_EXIT_PE = 18

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
# BEAR:  Skyrizi/Rinvoq clinical setback (safety signal or class-effect label
#        change) + neuroscience pipeline fails; Allergan debt amplifies risk;
#        EPS resets to ~$10; 11× = $110
# BASE:  Humira erosion fully absorbed; Skyrizi/Rinvoq in-line with consensus;
#        FY2027E $16 × 17× = $272 (flat multiple from today); modest re-rate
# BULL:  Skyrizi beats consensus ($35B+ peak); emraclidine approval (schizophrenia);
#        tavapadon approval (Parkinson's); leverage ratio improves; $17 × 21× = $357
# XBULL: Full pipeline delivery + leverage reduction re-rating; Skyrizi $40B+;
#        FY2029E $21 × 24× = $504; dividend king compounding
PRICE_BEAR  =  110
PRICE_BASE  =  272
PRICE_BULL  =  357
PRICE_XBULL =  504

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.70, 0.30, "Skyrizi $4.5B/qtr + Rinvoq $2.1B/qtr; beat own 2027 guidance early"),
    (+0.50, 0.20, "Humira cliff 70%+ absorbed; annualized erosion decelerating fast"),
    (+0.30, 0.15, "Neuroscience pipeline: emraclidine (schizophrenia Ph3), tavapadon (Parkinson's)"),
    (-0.30, 0.15, "Allergan debt legacy: ~$14B net debt; $2B+/yr interest; limits capital return"),
    (-0.30, 0.10, "Skyrizi/Rinvoq US patent expiry ~2030-2032; next cliff visible on horizon"),
    (-0.20, 0.10, "IRA drug pricing: IL-23/JAK classes at risk of future negotiation rounds"),
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
  FY2024 adj EPS ($10.12) × 12× leveraged specialty pharma floor. FY2024 was
  the Humira-biosimilar trough: US Humira revenue had collapsed ~55% from peak
  while Skyrizi + Rinvoq were still ramping to full offset capacity. The
  12× floor (vs JNJ's 14×) reflects Allergan debt leverage (~$14B net debt).
  EPP = $121.44.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E consensus adj EPS $16 × 18× conservative re-rate = $288.00.
  Ratio B = ($215.70 − $121.44) / ($288 − $215.70) = $94 / $72 = 1.30×
  → ◐ WATCHLIST. Meaningful upside (+33%) at a conservative exit multiple;
  Skyrizi/Rinvoq beating consensus adds further optionality.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ABBVIE: HUMIRA CLIFF ABSORBED — SKYRIZI/RINVOQ TAKE COMMAND
=============================================================

AbbVie is one of the most dramatic post-patent-cliff recovery stories in
modern pharmaceutical history. Humira (adalimumab) was the world's top-
selling drug for a decade — peak US revenue ~$18B. US biosimilars entered
in January 2023, and the market feared an EPS collapse. That fear drove
AbbVie to a trough near $155-160 in 2024. What actually happened: Skyrizi
and Rinvoq absorbed the Humira erosion and then kept growing. By 2025,
the two drugs combined reached $25.9B — already above AbbVie's own 2027
combined target set years earlier. The Humira cliff story is largely over;
the new story is whether AbbVie can be a $20+ EPS compounder by 2029.

THE HUMIRA REPLACEMENT ENGINE: SKYRIZI + RINVOQ
═════════════════════════════════════════════════
  Skyrizi (risankizumab) — IL-23 inhibitor:
    Q1 2026 revenue: $4.483B  (annualised >$18B run rate)
    Indications: plaque psoriasis (global leader), PsA, Crohn's, UC
    CEO statement Q1 2026 call: "Sell-side peak for Skyrizi at $33B; we
      expect it to exceed that." Management consistently beats own guidance.
    IBD (Crohn's + UC) approved indications are the key growth driver for
    2026-2030 as prevalence is high and Skyrizi data is best-in-class.

  Rinvoq (upadacitinib) — JAK1 inhibitor:
    Q1 2026 revenue: $2.119B  (annualised >$8.5B run rate)
    Indications: RA, PsA, AS, UC, AD, Crohn's — broadest approved indication
      set of any JAK inhibitor globally
    Black-box warning (class effect on JAK inhibitors) creates some HCP
    hesitation vs biologics but premium safety data vs older JAKs supports use.

Q1 2026 — STRONG BEAT
═══════════════════════
  Net revenues:           $15.0B   (+12.4% YoY) — beat consensus
  Adjusted EPS:           $2.65    (beat by $0.06)
  Skyrizi + Rinvoq:       $6.6B combined in one quarter (+32% YoY combined)
  FY2026 guidance raised: Revenue ~$67B (+9.5% YoY); adj EPS $14.08-$14.28
  Note: guidance includes $0.41/share headwind from acquired IPR&D / milestones

ALLERGAN LEGACY: THE DEBT BURDEN
══════════════════════════════════
AbbVie acquired Allergan in May 2020 for $63B, adding:
  • Botox (aesthetic + therapeutic): ~$5B/yr revenue, highly cash generative
  • Juvederm, Vraylar (psychiatry), Ubrelvy (migraine), Qulipta (migraine)
  • $35B+ in gross debt at acquisition; now ~$50B+ gross / ~$14B net
The debt generates ~$2B+/year in interest expense, reducing FCF available
for buybacks. As FCF grows (FY2026E FCF ~$17-18B), the company is deleveraging
naturally. By FY2027-2028, leverage ratio could fall below 1.5× EBITDA,
potentially enabling a buyback acceleration.

NEUROSCIENCE PIPELINE — THE OPTIONALITY
═════════════════════════════════════════
  Emraclidine (M4 muscarinic agonist — schizophrenia):
    • Phase 3 ongoing. Mechanism is entirely different from existing
      antipsychotics (no D2 antagonism = no weight gain, metabolic syndrome).
    • If Phase 3 replicates Phase 2 (positive signal), could be a $3-5B peak
      drug in a $15B+ annual market chronically under-treated.
    • Key read-out: 2026. Single largest binary catalyst for ABBV in 2026.

  Tavapadon (D1/D5 partial agonist — Parkinson's disease):
    • Phase 3 complete; NDA submitted. Differentiated from levodopa
      (no dyskinesia). If approved, initial $1-2B peak, building over time.

  Atogepant (Qulipta): CGRP antagonist migraine prevention; growing well.

  Vraylar: bipolar depression + schizophrenia; growing double-digit.

HUMIRA PATENT CLIFF — LESSONS AND NEXT CLIFF AWARENESS
════════════════════════════════════════════════════════
The Humira lesson: AbbVie's stock was discounted for 3 years on cliff fears
that proved manageable because of Skyrizi/Rinvoq depth. Now investors are
starting to price the NEXT cliff: Skyrizi and Rinvoq US patents expire
around 2030-2032. AbbVie has 6-7 years to build a next-generation replacement
engine. Emraclidine + tavapadon + Botox + Allergan therapeutics are part
of that bridge. The key question is whether 2027-2030 delivers sufficient
pipeline before the next IP cycle turns.

DIVIDEND — 3.2% YIELD WITH GROWTH
════════════════════════════════════
  Annual dividend: $6.92/share (3.21% yield at $215.70)
  AbbVie has raised the dividend every year since its 2013 inception
  (inherited Abbott's 40+ year streak before that).
  Payout ratio: ~49% on FY2026E adj EPS — very sustainable; room to grow.
  At EPP ($121.44), dividend yield would be 5.7% — institutional floor support.

WHERE THE RISK/REWARD IMPROVES
════════════════════════════════
  ACCUMULATE : $178-188  (FY2027E ~11-12×; ratio_b ~0.9×; near 52-wk low zone)
  BUY        : $140-155  (at/near EPP floor; 4.5%+ dividend yield)

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

print(f"  Current price         : ${CURRENT_PRICE:.2f}  (+37% from 52-wk low ~${PRICE_52W_LOW}; -12% from 52-wk high ${PRICE_52W_HIGH})")
print(f"  EPP floor             : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above; 12× × ${EPS_TROUGH} FY2024 Humira-trough adj EPS)")
print(f"  Method B (18× exit)   : ${price_b:.2f}  (+{(price_b/CURRENT_PRICE-1)*100:.1f}%; ratio_b = {ratio_b:.2f}× → WATCHLIST)")
print(f"  At 20× exit           : ${CONS_EPS_2YR*20:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*20-CURRENT_PRICE):.2f}× → ACCUMULATE (Humira cliff absorbed re-rate)")
print(f"  At 22× exit           : ${CONS_EPS_2YR*22:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*22-CURRENT_PRICE):.2f}× → ACCUMULATE (full re-rate; emraclidine catalyst)")
print(f"  BEAR scenario         : ${PRICE_BEAR}    (-49%; Skyrizi/Rinvoq setback + pipeline fails; EPS ~$10; 11×)")
print(f"  BASE scenario         : ${PRICE_BASE}   (+26%; FY2027E $16 × 17×; flat multiple; Skyrizi in-line)")
print(f"  BULL scenario         : ${PRICE_BULL}   (+66%; Skyrizi >$35B; emraclidine approval; $17 × 21×)")
print(f"  XBULL scenario        : ${PRICE_XBULL}   (+134%; FY2029E ~$21 × 24×; full pipeline + deleverage)")
print(f"  Forward P/E (FY2026E) : {CURRENT_PRICE/EPS_NOW:.1f}×  (${CURRENT_PRICE} / ${EPS_NOW}; raised guidance; cheap for growth rate)")
print(f"  Forward P/E (FY2027E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (${CURRENT_PRICE} / ${CONS_EPS_2YR}; one of cheapest big pharma on fwd EPS)")
print(f"  EPS history           : FY22 ${EPS_FY2022} → FY23 ${EPS_FY2023} → FY24 ${EPS_FY2024} (trough) → FY25 ${EPS_FY2025} → FY26E ${EPS_NOW}")
print(f"  Q1 2026               : Revenues $15.0B (+12.4%); adj EPS $2.65; Skyrizi $4.5B + Rinvoq $2.1B")
print(f"  Skyrizi 2025 combined : $25.9B Skyrizi+Rinvoq — already beat own 2027 target by $500M")
print(f"  CEO on consensus      : 'We see upside to consensus for Skyrizi, Rinvoq, and neuroscience'")
print(f"  Net debt              : ~$14B; interest ~$2B/yr; FCF FY2026E ~$17-18B; delevering naturally")
print(f"  Dividend              : ${DIVIDEND_ANN:.2f}/yr ({DIVIDEND_ANN/CURRENT_PRICE*100:.2f}% yield); raised every year since 2013 spin-off")
print(f"  Market cap            : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  (~{SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  Emraclidine read-out  : 2026 — key binary catalyst; schizophrenia PhIII data")
print(f"  ACCUMULATE entry      : $178-188  (FY2027E ~11-12×; ratio_b ~0.9×)")
print(f"  BUY entry             : $140-155  (at/near EPP floor; 4.5%+ yield)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.45×  |  Idiosyncratic: 75%  |  Macro: 25%

  Driver                                                     Type    Wt  Note
  ────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  Skyrizi $18B+ annualised run rate; beating own 2027 target IDIO   30%  PRIMARY BULL: CEO says consensus too low
  Humira erosion 70%+ absorbed; decelerating; fear peak past IDIO   20%  BULL: cliff story is over; re-rating ahead
  Neuroscience: emraclidine (schizophrenia), tavapadon (PD)  IDIO   15%  KEY OPTION: emraclidine PhIII read-out 2026
  Allergan debt: ~$14B net; $2B/yr interest; limits buyback   IDIO   15%  BEAR: leverage amplifies downside; caps re-rate
  Skyrizi/Rinvoq patent cliff 2030-2032                      IDIO   10%  FORWARD RISK: next cycle visible; 6 yrs away
  IRA pricing + macro rate / risk appetite                   MACRO   10%  Low beta; mainly idiosyncratic pharma story""")

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
  BEAR  (${PRICE_BEAR}) : Skyrizi or Rinvoq suffer a safety signal or class-effect label
               change restricting use (e.g. JAK black-box expanded). Allergan
               debt amplifies downside; EPS resets to ~$10; 11× = $110. -49%.
               Low probability (~8%) but Allergan leverage makes it more severe.

  BASE  (${PRICE_BASE}) : Skyrizi/Rinvoq deliver per consensus; Humira erosion fully
               absorbed by 2027; emraclidine misses Phase 3. FY2027E $16 × 17×
               = $272. +26% from current. Most likely 2-year scenario.
               Multiple stays flat as market waits for next pipeline catalyst.

  BULL  (${PRICE_BULL}) : Skyrizi exceeds $35B peak (CEO guided above $33B sell-side);
               emraclidine Phase 3 positive — new schizophrenia paradigm;
               leverage below 1.5× by 2027; multiple re-rates to 21×. $17 × 21×
               = $357. +66%. Requires Skyrizi outperformance + neuro success.

  XBULL (${PRICE_XBULL}) : Full pipeline delivery: Skyrizi $40B+, Rinvoq $15B+, emraclidine
               + tavapadon approved, Botox aesthetics sustaining. FY2029E adj
               EPS ~$21 × 24× = $504. +134%. Allergan debt fully repaid;
               pristine balance sheet; compounding at 15%+ EPS growth rate.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-25")
print("=" * 72)
