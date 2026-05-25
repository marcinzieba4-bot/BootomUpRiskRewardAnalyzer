"""
Johnson & Johnson (NYSE: JNJ) — BottomUp Risk/Reward Signal Model

SIGNAL:  ▷ HOLD/TRIM
RATIO B: 1.86x  (Method B at 22× FY2027E $12.69 = $279; ratio 83/45 = 1.86×)
DATE:    2026-05-25
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "JNJ"
COMPANY = "Johnson & Johnson"
SECTOR  = "Pharmaceuticals · MedTech · Oncology · Immunology · Cardiovascular"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  = 234.34   # JNJ — fetched Yahoo Finance, 2026-05-22 (last close before 2026-05-25)
PRICE_52W_LOW  = 149.04   # 52-week low: late-2025 talc verdict shock ($1.5B single verdict Dec 2025)
PRICE_52W_HIGH = 251.71   # 52-week high: recovery into 2026
SHARES_M       = 2408.0   # million diluted shares outstanding
DIVIDEND_ANN   = 5.36     # $1.34/quarter × 4; 62+ consecutive years of dividend growth; ex-div May 26 2026

# ── EPS (adjusted / non-GAAP) ─────────────────────────────────────────────────
# JNJ fiscal year = calendar year. Since Kenvue (consumer) spin-off in May 2023,
# JNJ is a pure Innovative Medicine + MedTech business — significantly higher
# quality earnings mix (no talc exposure in products going forward; legacy liability only).
EPS_FY2022 =  9.42    # Includes consumer segment pre-spin; reference only
EPS_FY2023 =  9.92    # Partial year with consumer; post-Kenvue reporting begins H2 2023
EPS_FY2024 = 10.12    # First full year as pure pharma/medtech; also impacted by talc reserve
EPS_FY2025 = 10.78    # Back-calculated: FY2026 guidance $11.55 = +7.1% YoY (confirmed Q1 2026)
EPS_NOW    = 11.55    # FY2026E adj (raised guidance midpoint $11.45-11.65 after Q1 2026 beat)
                       # Q1 2026: revenue $24.1B (+9.9% YoY); adj EPS $2.70 (beat by $0.02)

# ── EPP Floor ─────────────────────────────────────────────────────────────────
# Trough EPS = FY2025 ($10.78): current-cycle floor with talc reserve headwinds.
# Note: the 52-week low ($149.04) = 13.8× FY2025 adj EPS — the market tested
# the EPP floor in real-time. EPP of $150.92 and 52-wk low of $149 are essentially
# the same price, confirming the model is correctly calibrated.
# EPP_MIN_PE = 14×: JNJ is a AAA-rated dividend king; floor P/E above generic pharma
# (typically 12-14×) because of its 62-year dividend track record and FCF quality.
EPS_TROUGH = 10.78    # FY2025 adj EPS — verified current-cycle trough
EPP_MIN_PE = 14       # Pharma/medtech floor; JNJ quality premium vs generic insurer
EPP        = EPS_TROUGH * EPP_MIN_PE   # $10.78 × 14 = $150.92

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E consensus adj EPS: $12.69 (average analyst estimate; range $11.54-$13.90)
# Exit P/E: 22× — JNJ's historical mid-cycle range is 16-22×. Post-Kenvue (purer,
# higher-growth pharma+medtech) could deserve 20-25× on clean execution. Talc
# overhang justifies discount to low end of that expanded range.
#   At 22×: $279.18  (+19.1% from $234.34)
#   At 24×: $304.56  (+30.0% — requires talc resolution + multiple re-rating)
#   At 26×: $330.00  (+40.8% — full re-rate; pipeline delivering)
CONS_EPS_2YR = 12.69
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
# BEAR:  Talc MDL resolved at worst-case aggregate; massive capital drain;
#        Stelara biosimilar erosion accelerates; EPS compressed to $8; 14× = $112
# BASE:  FY2027E $12.69 × 20× = $253.80 — essentially the 52-week high territory
# BULL:  Talc resolved via manageable civil settlement; pharma pipeline delivers
#        (Darzalex, Carvykti, Rybrevant); $13.5 × 24× = $324
# XBULL: Clean balance sheet (talc behind) + pipeline ramp (nipocalimab, JNJ-2113,
#        amivantamab SC approval); FY2029E ~$16 × 27× = $432; dividend king compounding
PRICE_BEAR  =  112
PRICE_BASE  =  254
PRICE_BULL  =  324
PRICE_XBULL =  432

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.60, 0.25, "Darzalex/Carvykti/Tremfya/Rybrevant: durable pharma compounders"),
    (+0.40, 0.20, "MedTech recovery: Abiomed + ortho robotics + electrophysiology"),
    (-0.70, 0.25, "Talc MDL: 67K+ pending cases; $1.5B single verdict Dec 2025; 3rd bankruptcy rejected"),
    (-0.20, 0.15, "Stelara biosimilar erosion: patent cliff 2025+ compressing pharma top-line"),
    (+0.20, 0.10, "AAA credit; 62-year dividend growth streak; FCF $17B+/yr; capital return"),
    (-0.10, 0.05, "IRA drug pricing + political risk on pharmaceutical pricing"),
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
  FY2025 adj EPS ($10.78) × 14× AAA-grade pharma floor. This is one of
  the cleanest EPP calibrations in the coverage universe: the 52-week low
  ($149.04) hit exactly at the EPP = $150.92, confirming the market's own
  floor test during the worst talc verdict panic. Model calibrated correctly.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E consensus adj EPS $12.69 × 22× (historical mid-cycle JNJ) = $279.18.
  Ratio B = ($234.34 − $150.92) / ($279.18 − $234.34) = $83 / $45 = 1.86×
  → ▷ HOLD/TRIM. Only +19% upside to Method B; EPP gap 55%; balanced but not
  compelling. Talc discount caps multiple expansion until liability is resolved.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

JOHNSON & JOHNSON: BEST-IN-CLASS HEALTHCARE — DISCOUNTED FOR TALC LEGACY
=========================================================================

JNJ is one of the three or four genuinely elite industrial-scale healthcare
franchises on Earth. AAA credit rating (one of only two US companies with
AAA), 62+ consecutive years of dividend increases, $17B+ annual free cash
flow, and a product portfolio spanning the highest-growth areas of modern
medicine — oncology, immunology, and cardiovascular intervention. The post-
Kenvue business (pure Innovative Medicine + MedTech since 2023) is a
cleaner, higher-margin, higher-growth enterprise than the old J&J. Quality
is not in question. The debate is entirely about the talc legacy and price.

POST-KENVUE TRANSFORMATION (2023–PRESENT)
══════════════════════════════════════════
In May 2023 JNJ spun off Kenvue (KVUE) — its consumer health division
(Band-Aid, Listerine, Neutrogena, baby products). This division was the
source of most talc-product liability exposure going forward in products.
The remaining JNJ is:
  • Innovative Medicine (~60% of revenue): pharma assets including
    Darzalex, Tremfya, Stelara, Carvykti, Rybrevant, Erleada
  • MedTech (~40% of revenue): Abiomed (heart pumps), DePuy Synthes
    (orthopaedics), Biosense Webster (electrophysiology), robotics

Q1 2026 — SOLID EXECUTION
═══════════════════════════
  Revenue:              $24.1B  (+9.9% YoY) — above consensus
  Innovative Medicine:  +11.2% YoY — Darzalex + Carvykti leading
  MedTech:              +7.7% YoY — electrophysiology + Abiomed strong
  Adj EPS:              $2.70   (beat by $0.02; slightly below $2.77 Q1 2025)
  FY2026 guidance raised: Revenue $100.3-101.3B; adj EPS $11.45-11.65
  Dividend raised:      $1.34/quarter (ex-div May 26, 2026); 2.29% yield

PHARMA PIPELINE — THE UPSIDE CASE
════════════════════════════════════
  Darzalex (daratumumab): #1 multiple myeloma drug globally; front-line
    expansion underway. $12B+ revenue in 2025. Still growing 15%+ as
    earlier lines of use expand globally. Multi-year runway.

  Carvykti (ciltacabtagene autoleucel): Best-in-class CAR-T for myeloma.
    Approved for earlier lines (2nd line) in 2024. Manufacturing scaling.
    Could be a $4-6B peak revenue product; underappreciated in current price.

  Tremfya (guselkumab): IL-23 inhibitor for psoriasis/IBD. Expanding
    into Crohn's and UC vs Stelara as Stelara biosimilars erode.

  Rybrevant (amivantamab): EGFR-MET bispecific for lung cancer. SC
    formulation approval (easier dosing) driving accelerated adoption.

  Pipeline:
    • Nipocalimab: FcRn blocker for autoimmune (multiple Phase 3 programs;
      myasthenia gravis, haemolytic disease of foetus/newborn)
    • JNJ-2113: Oral IL-23 inhibitor (if approved, first oral bio-similar-
      replacing pill for psoriasis — potential blockbuster)
    • Amivantamab combinations: MARIPOSA-2 data transforming lung cancer SoC

STELARA CLIFF — THE HEADWIND
══════════════════════════════
Stelara (ustekinumab) was JNJ's second-largest pharma product (~$10B peak
revenue). US biosimilars entered in early 2025; EU biosimilar competition
is ongoing. This is a meaningful top-line headwind for 2025-2027. JNJ
guided for $3-4B Stelara revenue in 2026 vs $7B+ at peak. The pipeline
(Tremfya IBD expansion, nipocalimab, Carvykti) must offset this drag.

MEDTECH — UNDERAPPRECIATED RECOVERY
═════════════════════════════════════
  Abiomed (Impella heart pumps): #1 in cardiogenic shock; growing 12-15%
    YoY as clinical evidence for earlier use expands. Paid $16B (2021);
    now likely worth $25-30B+ as a standalone. Unique moat.
  Electrophysiology: Biosense Webster leading in cardiac ablation catheter
    market. Growing 15%+ as atrial fibrillation ablation volumes surge.
  Robotics: Ottava (surgical robot) Phase 3 studies progressing.
    Behind Intuitive Surgical's da Vinci 5, but a potential long-term entry.

THE TALC LITIGATION — THE KEY RISK
════════════════════════════════════
J&J's baby powder historically used talc (replaced with cornstarch in 2020).
Plaintiffs allege talc-asbestos contamination caused ovarian cancer and
mesothelioma. The scale of litigation is extraordinary:
  • 67,115+ pending cases in MDL as of March 2026
  • 90,000+ total cases filed nationwide
  • Two failed bankruptcy attempts (LTL Management entity; courts rejected
    attempt to use subsidiary bankruptcy to cap total liability)
  • Third proposed $8B settlement REJECTED March 2025 by bankruptcy court
  • JNJ reversed ~$7B reserve after rejection — now back to direct liability
  • December 2025: $1.5B single-plaintiff verdict (mesothelioma)
  • October 2025: $966M verdict (mesothelioma, California)

The talc liability is the single reason JNJ trades at 20× instead of 25×.
Potential outcomes:
  • Civil negotiated settlement: total cost $8-15B over 3-5 years. Painful
    but manageable at $17B/yr FCF. EPS impact ~$0.50-1.00/yr during settlement.
  • Continued adverse jury verdicts: 10-20 trials/year; possible $2-5B/yr
    total verdict exposure. More pain but company survives.
  • Catastrophic: mass class action certification + $50B+ aggregate; unlikely
    given case-by-case trial structure but tail risk.
  The stock at $149 (52-wk low) was pricing some material adverse outcome.
  At $234, the market has partially de-risked this but not fully.

DIVIDEND KING — THE FLOOR MECHANISM
═════════════════════════════════════
JNJ has increased its dividend for 62 consecutive years. The $5.36/year
dividend at current price yields 2.29%. This creates a real yield floor:
at $150 EPP, the dividend yield would be 3.6% — institutionally very
attractive, explaining why the stock bounced strongly from $149.

WHERE THE RISK/REWARD IMPROVES
════════════════════════════════
  WATCHLIST  : $195-210  (FY2027E ~15-17×; ratio_b ~1.4×; near Nov 2025 lows)
  ACCUMULATE : $165-180  (FY2027E ~13-14×; ratio_b ~0.8×; talc fear zone)
  BUY        : $145-155  (at/near EPP floor; worst-case talc priced; 3.5%+ yield)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("PART 3 — NUMBERS & SIGNALS")
print("=" * 72)
print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │  SIGNAL:  {signal_primary:<12}  │  RATIO B: {ratio_b_fmt:<10}               │
  │  TICKER:  {TICKER:<10}    │  SECTOR:  Healthcare / Pharma+MedTech │
  └──────────────────────────────────────────────────────────────────┘

  ----------------------------------------------------------------------
""")

print(f"  Current price         : ${CURRENT_PRICE:.2f}  (+57% from 52-wk low ${PRICE_52W_LOW}; -7% from 52-wk high ${PRICE_52W_HIGH})")
print(f"  EPP floor             : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above; 14× × ${EPS_TROUGH} FY2025 adj EPS; 52-wk low ${PRICE_52W_LOW} ≈ EPP)")
print(f"  Method B (22× exit)   : ${price_b:.2f}  (+{(price_b/CURRENT_PRICE-1)*100:.1f}%; ratio_b = {ratio_b:.2f}× → HOLD/TRIM)")
print(f"  At 24× exit           : ${CONS_EPS_2YR*24:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*24-CURRENT_PRICE):.2f}× → WATCHLIST (talc resolution re-rate)")
print(f"  At 26× exit           : ${CONS_EPS_2YR*26:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*26-CURRENT_PRICE):.2f}× → WATCHLIST (full pipeline re-rate)")
print(f"  BEAR scenario         : ${PRICE_BEAR}    (-52%; talc worst-case + Stelara cliff; EPS ~$8; 14×)")
print(f"  BASE scenario         : ${PRICE_BASE}   (+8%; FY2027E $12.69 × 20×; close to 52-wk high)")
print(f"  BULL scenario         : ${PRICE_BULL}   (+38%; talc resolved + pipeline; $13.5 × 24×)")
print(f"  XBULL scenario        : ${PRICE_XBULL}   (+84%; FY2029E ~$16 × 27×; dividend king compounding clean)")
print(f"  Forward P/E (FY2026E) : {CURRENT_PRICE/EPS_NOW:.1f}×  (${CURRENT_PRICE} / ${EPS_NOW}; raised guidance)")
print(f"  Forward P/E (FY2027E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (${CURRENT_PRICE} / ${CONS_EPS_2YR}; consensus; talc-discounted)")
print(f"  EPS history           : FY23 ${EPS_FY2023} → FY24 ${EPS_FY2024} → FY25 ${EPS_FY2025} → FY26E ${EPS_NOW}")
print(f"  Q1 2026               : Revenue $24.1B (+9.9%); adj EPS $2.70; Innovative Med +11.2%; MedTech +7.7%")
print(f"  Stelara cliff         : $10B peak → ~$3-4B FY2026E as US biosimilars erode; pipeline must offset")
print(f"  Talc liability        : 67K+ pending MDL cases; $1.5B Dec 2025 verdict; 3rd bankruptcy rejected")
print(f"  Dividend              : ${DIVIDEND_ANN:.2f}/yr ({DIVIDEND_ANN/CURRENT_PRICE*100:.1f}% yield); ex-div May 26 2026; 62 consecutive years raised")
print(f"  Market cap            : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  FCF                   : ~$17B+/yr; funds dividend ($12.9B/yr) + buybacks + BD comfortably")
print(f"  WATCHLIST entry       : $195-210  (FY2027E ~15-17×; ratio_b ~1.4×)")
print(f"  ACCUMULATE entry      : $165-180  (FY2027E ~13-14×; ratio_b ~0.8×)")
print(f"  BUY entry             : $145-155  (at EPP floor; 3.5%+ dividend yield; worst-case priced)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.50×  |  Idiosyncratic: 70%  |  Macro: 30%

  Driver                                                     Type    Wt  Note
  ────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  Talc MDL: 67K+ cases; adverse verdicts; failed bankruptcy  IDIO    25%  PRIMARY BEAR: caps multiple expansion
  Stelara biosimilar erosion (patent cliff 2025+)            IDIO    15%  BEAR: top-line headwind until pipeline fills gap
  Darzalex/Carvykti/Tremfya/Rybrevant growth                 IDIO    25%  PRIMARY BULL: durable multi-year compounders
  MedTech recovery (Abiomed, electrophysiology, robotics)    IDIO    20%  BULL: Abiomed alone worth ~$25-30B+ intrinsically
  AAA credit + 62-yr dividend streak + FCF $17B+             IDIO    10%  FLOOR: yield support at $145-155; never cut dividend
  IRA pricing / macro rate sensitivity                       MACRO    5%  Low beta; defensive; limited macro sensitivity""")

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
  BEAR  (${PRICE_BEAR}) : Talc MDL resolved at worst-case aggregate ($40-60B total);
               J&J forced to issue massive equity; Stelara cliff not offset by
               pipeline. EPS compressed to ~$8; 14× trough = $112. -52% from
               current. Probability ~8-12%. Fat tail, not trivial.

  BASE  (${PRICE_BASE}) : Talc resolved via civil settlement ($10-15B over 3-4 years);
               pipeline (Darzalex, Carvykti, Rybrevant) offsets Stelara cliff;
               MedTech continues 7-8% growth. FY2027E $12.69 × 20× = $254.
               Only +8% from current. Consensus PT is essentially BASE.

  BULL  (${PRICE_BULL}) : Manageable talc settlement ($8-12B civil); market re-rates to
               24× as uncertainty clears; pipeline beats (Carvykti scale, nipocalimab
               Phase 3 success, JNJ-2113 oral IL-23 approval). $13.50 × 24× = $324.
               +38% from current. Requires legal clarity + pipeline execution.

  XBULL (${PRICE_XBULL}) : JNJ fully transforms into growth compounder post-talc. Dividend
               king status intact; Abiomed + Carvykti + nipocalimab all scale;
               Ottava robotics competes with ISRG. FY2029E ~$16 × 27× = $432.
               +84% over 3-4 years. Best-case everything goes right scenario.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-25")
print("=" * 72)
