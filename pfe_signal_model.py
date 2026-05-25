"""
Pfizer Inc. (NYSE: PFE) — BottomUp Risk/Reward Signal Model

SIGNAL:  ◎ ACCUMULATE
RATIO B: 0.86x  (Method B at 11× FY2027E $3.00 = $33.00; ratio 6.1/7.1 = 0.86×)
DATE:    2026-05-25
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "PFE"
COMPANY = "Pfizer Inc."
SECTOR  = "Pharmaceuticals · Oncology (Seagen ADCs) · Vaccines · Obesity · Established Drugs"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  =  25.90   # PFE — confirmed May 25, 2026; range $25.76-26.15 intraday
PRICE_52W_LOW  =  22.88   # 52-week low (LOE cliff fear + EPS compression)
PRICE_52W_HIGH =  28.75   # 52-week high
SHARES_M       = 5700.0   # million diluted shares (~$147.6B market cap / $25.90)
DIVIDEND_ANN   =   1.71   # ~$0.4275/quarter; 6.6% yield at current; one of highest in S&P 500

# ── EPS (non-GAAP adjusted) ────────────────────────────────────────────────────
# PFE FY = calendar year. COVID created a temporary +$30B/yr revenue peak (Paxlovid
# + Comirnaty) followed by a catastrophic normalization in 2023: $5.5B inventory
# write-offs + $3.5B Paxlovid reversal compressed adjusted EPS to $1.84 (-72% YoY).
# FY2024-2025 represent the recovery, but a new structural headwind now arrives:
# Eliquis (2026) and Ibrance (March 2027) LOE, putting ~$17-18B annual revenue at
# risk by 2028. The company is re-investing in oncology (Seagen $43B) and obesity
# (Metsera $7B) to fill the gap.
EPS_FY2022 =  6.58    # COVID peak: Paxlovid ~$18.9B + Comirnaty ~$37.8B; extraordinary
EPS_FY2023 =  1.84    # Trough: COVID normalization; $5.5B inventory write-offs; -72%
EPS_FY2024 =  3.11    # Recovery: Seagen oncology contributing; cost cuts; +69% YoY
EPS_FY2025 =  3.10    # Essentially flat: base business growing but COVID fades further
EPS_NOW    =  2.90    # FY2026E midpoint guidance ($2.80-$3.00); reaffirmed post-Q1 2026
                       # Q1 2026: revenue $14.45B (+5%); adj EPS $0.75 (beat $0.72)
                       # Ex-COVID portfolio: +7% operational; launched/acquired +22%
                       # Includes ~$1.5B LOE revenue headwind already embedded

# ── EPP Floor ─────────────────────────────────────────────────────────────────
# EPS_TROUGH = structural LOE cliff nadir + recession. Eliquis (~$6B US) and
# Ibrance (~$4B) lose exclusivity 2026-2027. Total LOE impact: ~$17-18B revenue
# by 2028 → ~$2.10-2.52/share EPS loss at 12% net margin. Cost cuts ($4B+ by
# 2027 = ~$0.70/share) partially offset. In recession, more segments compress.
# Stress floor: $2.90 (FY2026E) - $1.70 (full LOE) + $0.70 (cost cuts) = $1.90.
# But add recession (-$0.15) + pipeline delay = $1.70-1.80. Use $1.80.
# Calibration: 52-wk low $22.88 ÷ FY2024 $3.11 = 7.4× — extreme fear multiple.
# $22.88 ÷ $1.80 stress EPS = 12.7× — consistent with EPP floor P/E.
EPS_TROUGH = 1.80     # LOE cliff peak impact + recession; below FY2023 trough EPS ($1.84)
EPP_MIN_PE = 11       # mega-cap pharma with heavy LOE cliff and M&A debt; discount vs diversified peers
EPP        = EPS_TROUGH * EPP_MIN_PE   # $1.80 × 11 = $19.80

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E non-GAAP: ~$3.00. The math: FY2026E $2.90 - $0.70 (LOE midpoint impact
# from Eliquis/Ibrance) + $0.70 (cost cuts maturing: $4B+ savings by 2027) +
# $0.10 (Seagen ADC portfolio scaling, Padcev +22% Q1 2026) = $3.00.
# LOE and cost cuts roughly cancel; Seagen provides modest accretion.
# Exit P/E: 11× — LOE cliff + heavy M&A debt warrant compressed multiple vs
# historical 12-16×. The $29 analyst mean target implies ~10× FY2026E.
#   At 11×: $33.00  (+27.4% from $25.90) — conservative; LOE peak still unfolding
#   At 13×: $39.00  (+50.6%) — pipeline begins de-risking LOE valley
#   At 15×: $45.00  (+73.7%) — obesity drug approved; Seagen blockbusters emerge
CONS_EPS_2YR = 3.00
CONS_EXIT_PE = 11

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
# BEAR:  LOE cliff hits max; obesity pipeline fails; recession; debt stress.
#        EPS resets near $1.80 trough; at 10× = $18.
# BASE:  LOE absorbed by cost cuts + Seagen; flat EPS through valley. FY2027E
#        $3.00 × 10× = $30. +16% from current. Modest return for patience.
# BULL:  PF'3944 obesity Phase III positive; LOE offset materializes faster.
#        $3.50 × 11.4× = $40 by 2027. +54%. Requires obesity catalyst.
# XBULL: Obesity + Seagen both become $5B+ franchises; LOE valley over by 2029.
#        FY2028-29E ~$4.00 × 14.5× = $58. +124%. Long-duration optionality.
PRICE_BEAR  =   18
PRICE_BASE  =   30
PRICE_BULL  =   40
PRICE_XBULL =   58

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.50, 0.25, "Seagen oncology ADCs: Padcev +20% Q1 2026; Tukysa, Adcetris growing; 20 pivotals"),
    (-0.70, 0.30, "LOE cliff $17-18B: Eliquis 2026, Ibrance 2027; EPS compression 2026-2028"),
    (+0.30, 0.20, "Cost cuts $4B+ by 2027 (~$0.70/share); Pfizer Reallocate to Win; Seagen synergies"),
    (+0.40, 0.15, "Obesity optionality: PF'3944 Phase IIb positive; Metsera $7B; 10 Phase III 2026"),
    (-0.40, 0.10, "M&A debt: Seagen $43B + Metsera $7B; heavy balance sheet; dividend sustainability"),
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
  Stress EPS ($1.80) × 11× heavily-leveraged-mega-pharma floor. EPS_TROUGH
  anchors to the LOE cliff nadir (2027-2028): full Eliquis + Ibrance revenue
  loss (~$10B) with partial cost cut / Seagen offset, plus a mild recession.
  At $1.80, this is marginally below the FY2023 COVID trough ($1.84).
  EPP = $19.80.
  Calibration: 52-wk low $22.88 ÷ $1.80 = 12.7× — the market bottomed
  above EPP floor P/E of 11×, as expected for a company still generating
  significant cash flow and paying a 6.6% dividend.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E ~$3.00 (LOE impact offset by cost cuts + Seagen growth) × 11×
  LOE-discounted exit = $33.00. At 11×: +27% from current $25.90.
  Ratio B = ($25.90 − $19.80) / ($33.00 − $25.90) = $6.10 / $7.10 = 0.86×
  → ◎ ACCUMULATE. At 8.9× FY2026E, the LOE risk is deeply discounted.
  The 6.6% dividend yield provides income while the thesis plays out.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PFIZER: NAVIGATING THE LOE VALLEY WITH SEAGEN AND OBESITY AS LIFELINES
=======================================================================

Pfizer is the world's second-largest pharmaceutical company by revenue
($62.6B in FY2025), with a portfolio spanning oncology, vaccines, rare
diseases, inflammation, and internal medicine. Post-COVID, Pfizer has
deployed the windfall from Paxlovid and Comirnaty (~$100B in COVID revenue
over 2021-2023) into two of the most expensive acquisitions in pharma
history: Seagen ($43B, oncology ADCs, late 2023) and Metsera ($7B, obesity
GLP-1/amylin, November 2025). The thesis: Seagen's antibody-drug conjugate
(ADC) technology becomes the backbone of a dominant oncology franchise;
Metsera's PF'3944 becomes Pfizer's answer to Ozempic/Wegovy.

The stock is range-bound at $22-29 because the market is pricing the near-
certain LOE cliff ($17-18B revenue at risk by 2028) against deeply uncertain
pipeline upside. At 8.9× FY2026E adjusted EPS, Pfizer is the cheapest it
has been on forward earnings outside of the 2023 COVID trough crisis.

Q1 2026 — BEAT AND REAFFIRM
═════════════════════════════
  Revenue:                $14.45B  (+5% YoY; beat $13.92B consensus)
  Adjusted EPS:           $0.75    (beat $0.72 consensus)
  Ex-COVID revenue:       +7% operational — core business outperforming
  Launched/acquired products: +22% operationally YoY (Seagen + recent launches)
  Seagen products:        +20% operational
  FY2026 guidance reaffirmed: revenue $59.5-62.5B; adj EPS $2.80-$3.00

THE LOE CLIFF — THE PRIMARY BEAR CASE
═══════════════════════════════════════
This is the defining challenge for Pfizer over the next 3-4 years:

  Eliquis (apixaban): ~$6B US revenue annually. Core patents expire 2026.
    BMS/Pfizer co-market. Generics entering late 2026. Revenue ~50%+ erosion
    by end of 2027. Impact: ~$3B/yr annual revenue loss by 2027-2028.

  Ibrance (palbociclib): CDK4/6 inhibitor for breast cancer, ~$4.0B FY2025.
    US patent expires March 2027. Verzenio (Eli Lilly) and biosimilars already
    exist. Revenue erosion will be swift; palbociclib is small-molecule generic.
    Impact: ~$2-3B/yr revenue loss by 2028.

  Other LOE: Xtandi (prostate cancer), Prevnar 13, Nurtec ODT, Xeljanz
    all facing erosion or competition.

  Total revenue at risk: ~$17-18B by 2028. That's ~27-29% of FY2025 revenue.

  The LOE impact on EPS: at 12% net margin, $17-18B = ~$2.04-2.16/share.
  This is the core reason the market assigns a 9× multiple to current EPS —
  it already expects a step-down in 2027-2028.

  Pfizer's offsetting measures:
  1. Cost cuts: $4B+ by 2027 ("Pfizer Reallocate to Win") = ~$0.70/share
  2. Seagen growth: ADC portfolio scaling toward $5B+ by 2028
  3. New launches: Abrysvo (RSV vaccine), Ngenla, etc.

SEAGEN — THE $43B BET ON ONCOLOGY ADCs
════════════════════════════════════════
Seagen brought Pfizer four approved antibody-drug conjugate (ADC) products:
  • Padcev (enfortumab vedotin): urothelial cancer (bladder); with Keytruda
    combo, ~$2B+ annual run rate and growing strongly; +20% Q1 2026
  • Tukysa (tucatinib): HER2+ breast cancer; growing breast cancer franchise
  • Adcetris (brentuximab vedotin): Hodgkin lymphoma and other CD30+ cancers
  • Tivdak (tisotumab vedotin): cervical cancer

ADCs are the hottest technology in oncology — they combine targeted antibody
precision with cytotoxic drug delivery, allowing cancer-killing payloads to
be delivered specifically to tumor cells. AZ/Daiichi Sankyo's Enhertu has
proven the ADC concept at blockbuster scale. Seagen's pipeline includes 20+
ADC programs across multiple tumor types.

Critical question: can Seagen generate $8-10B+ annually by 2028 to offset
LOE? Analysts say $5-6B is likely; $10B requires multiple new approvals.

METSERA / PF'3944 — THE OBESITY WILDCARD
══════════════════════════════════════════
Pfizer exited the oral GLP-1 race in April 2025 when it discontinued
danuglipron (side effects too severe). The Metsera acquisition in November
2025 represented a re-entry with better assets:
  • PF'3944: injectable GLP-1 receptor agonist (monthly dosing); Phase IIb
    VESPER-3 data showed "robust weight loss with no plateau at week 28"
    at 4× monthly dose equivalent. Strong tolerability profile.
  • 10 Phase III studies of PF'3944 planned in 2026 spanning obesity +
    comorbidities. First potential approval targeted: 2028.
  • YaoPharma license: YP05002 oral small-molecule GLP-1 (Chinese biotech).
  • Total obesity pipeline: 20+ studies across 4 programs by end of 2026.

The obesity market is projected at $130B by 2030. Pfizer lost ground by
abandoning danuglipron; Metsera attempts a comeback. If PF'3944 works in
Phase III, it is a $5-10B+ product. That would transform Pfizer's earnings
trajectory from 2029 onwards. This is pure optionality — it is NOT priced
in at the current 8.9× multiple.

FINANCIAL STRUCTURE — DIVIDEND RISK ANALYSIS
══════════════════════════════════════════════
At $1.71/share annually (6.6% yield), the dividend is the primary reason
most income investors hold PFE. Is it safe?
  FY2026E adj EPS: $2.90 → payout ratio: 59% (covered)
  FY2027 stress ($3.00): payout ratio: 57% (still covered)
  At trough EPS $1.80: payout ratio: 95% (razor thin)
  Free cash flow has been $8-10B/yr recently — dividend costs ~$9.7B/yr.
  The dividend is AT RISK in the bear scenario. Pfizer management has been
  explicit that "protecting the dividend is a top priority" — but that is
  exactly what companies say before they cut it.

The dividend suspension risk is the key tail risk for income investors.
At $25.90, you're paid 6.6%/yr to wait. If the dividend is cut 50%, you
get 3.3% and the stock likely falls 15-20% as income sellers exit.

COST EFFICIENCY PROGRAM ("PFIZER REALLOCATE TO WIN")
══════════════════════════════════════════════════════
  $3.5B in "Reallocate to Win" savings announced 2024; $1.7B Seagen
  synergies → total $5.2B+ in targeted savings by 2027.
  This program eliminates ~25,000 employees (10% of workforce over 2 yrs).
  Savings of $4B+ = ~$0.70/share adj EPS lift.
  Critical: without these cuts, FY2027 EPS would be materially worse.

THE BULL CASE IN 20 WORDS
══════════════════════════
  9× cheap; 6.6% yield; Seagen ADCs; obesity option; cost cuts work.
  Market prices zero probability of pipeline success.

WHERE RISK/REWARD IMPROVES
═══════════════════════════
  ACCUMULATE now : $22-28  (current range; 8-9× fwd P/E; collect 6.6% while waiting)
  BUY on panic   : $20-23  (near EPP floor; LOE worst case priced; near 52-wk low)
  Trim / reduce  : $31-35  (approaching Method B ceiling; reduce risk vs reward)

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

print(f"  Current price         : ${CURRENT_PRICE:.2f}  (52-wk range: ${PRICE_52W_LOW}-${PRICE_52W_HIGH}; -10% from 52-wk high)")
print(f"  EPP floor             : ${EPP:.2f}   (+{epp_gap_pct:.1f}% above; 11× × ${EPS_TROUGH} stress EPS; 52-wk low ${PRICE_52W_LOW} ÷ $1.80 = 12.7×)")
print(f"  Method B (11× exit)   : ${price_b:.2f}   (+{(price_b/CURRENT_PRICE-1)*100:.1f}%; ratio_b = {ratio_b:.2f}× → ACCUMULATE)")
print(f"  At 13× exit           : ${CONS_EPS_2YR*13:.2f}   ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*13-CURRENT_PRICE):.2f}× → BUY (pipeline de-risking LOE)")
print(f"  At 15× exit           : ${CONS_EPS_2YR*15:.2f}   ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*15-CURRENT_PRICE):.2f}× → BUY (obesity Phase III positive)")
print(f"  BEAR scenario         : ${PRICE_BEAR}    (-31%; full LOE + pipeline fail + recession; $1.80 EPS × 10×)")
print(f"  BASE scenario         : ${PRICE_BASE}    (+16%; LOE absorbed by cuts; Seagen scaling; $3.00 × 10×)")
print(f"  BULL scenario         : ${PRICE_BULL}    (+54%; PF'3944 Phase III positive; Seagen accelerating; $3.50 × 11.4×)")
print(f"  XBULL scenario        : ${PRICE_XBULL}    (+124%; obesity + Seagen both block; FY2028-29E $4.00 × 14.5×)")
print(f"  Forward P/E (FY2026E) : {CURRENT_PRICE/EPS_NOW:.1f}×   (${CURRENT_PRICE} / ${EPS_NOW}; cheapest since FY2023 COVID trough)")
print(f"  Forward P/E (FY2027E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×   (${CURRENT_PRICE} / ${CONS_EPS_2YR}; pricing zero pipeline success)")
print(f"  EPS history           : FY22 ${EPS_FY2022} → FY23 ${EPS_FY2023} → FY24 ${EPS_FY2024} → FY25 ${EPS_FY2025} → FY26E ${EPS_NOW}")
print(f"  Q1 2026               : Revenue $14.45B (+5%); adj EPS $0.75 (beat); ex-COVID +7%; Seagen +20%")
print(f"  LOE cliff             : Eliquis US LOE 2026; Ibrance LOE March 2027; ~$17-18B at risk by 2028")
print(f"  Seagen (ADCs)         : Padcev, Tukysa, Adcetris, Tivdak; +20% Q1 2026; 20+ ADC programs")
print(f"  Obesity pipeline      : Metsera ($7B, Nov 2025); PF'3944 Phase IIb positive; 10 Phase III 2026")
print(f"  Cost cuts             : $4B+ by 2027 (~$0.70/share EPS lift); Pfizer Reallocate to Win")
print(f"  Dividend              : ${DIVIDEND_ANN:.2f}/yr ({DIVIDEND_ANN/CURRENT_PRICE*100:.1f}% yield); covered at 59% payout; at risk in bear scenario")
print(f"  Market cap            : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  ACCUMULATE zone       : $22-28  (current; 8-9× fwd P/E; collect 6.6% yield)")
print(f"  BUY on panic          : $20-23  (near EPP floor; ratio_b ~0.3-0.5×; LOE worst priced)")
print(f"  Trim / reduce         : $31-35  (approaching Method B ceiling; ratio_b ~1.5-1.7×)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.55×  |  Idiosyncratic: 70%  |  Macro: 30%

  Driver                                                      Type    Wt  Note
  ─────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  LOE cliff: Eliquis 2026, Ibrance 2027 (~$17-18B at risk)    IDIO    30%  PRIMARY BEAR: defining 2026-2028 headwind
  Seagen oncology ADCs: Padcev +20%; 20+ programs              IDIO    25%  PRIMARY BULL: $5-6B by 2028; secular ADC leader
  PF'3944 obesity: Phase IIb positive; 10 Phase III 2026       IDIO    20%  OPTION VALUE: $5-10B if approved; 2028+
  Cost cuts $4B+: Pfizer Reallocate to Win by 2027             IDIO    15%  BULL: $0.70/share EPS buffer vs LOE
  Dividend 6.6%: largest yield in large-cap pharma              IDIO    10%  ANCHOR: income buyers floor; dividend risk in bear""")

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
  BEAR  (${PRICE_BEAR}) : LOE hits full force; Seagen disappoints; PF'3944 fails
               Phase III; recession. EPS resets to ~$1.80; market applies
               10× = $18. -31% from current. Dividend at serious risk.
               Most concerning: ABT/Humira showed market can price 6× on
               LOE stocks before recovery thesis materialises.

  BASE  (${PRICE_BASE}) : LOE absorbed (cost cuts offset ~$0.70/share); Seagen scales
               to $4-5B; obesity Phase III data in 2027 uncertain but
               pipeline not dead. EPS holds near $3.00; 10× = $30. +16%.
               Investors collect 6.6%/yr waiting for pipeline. Uninspiring
               but positive: the 6.6% yield makes "collecting income" viable.

  BULL  (${PRICE_BULL}) : PF'3944 Phase III readout in 2027 is positive; Seagen ADC
               Padcev + new programs exceed $5B combined; obesity market
               share builds ahead of 2028 approval. EPS ramps to $3.50;
               multiple expands to 11.4× on LOE de-risking. +54%.

  XBULL (${PRICE_XBULL}) : PF'3944 approved 2028 and captures 15%+ of obesity market;
               Seagen becomes a $8-10B platform; LOE valley is over by 2029.
               FY2028-29E ~$4.00 × 14.5× = $58. +124%. Requires Pfizer to
               execute on two parallel platform transformations simultaneously.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-25")
print("=" * 72)
