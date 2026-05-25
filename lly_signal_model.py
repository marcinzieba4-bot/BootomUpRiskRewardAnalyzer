"""
Eli Lilly and Company (NYSE: LLY) — BottomUp Risk/Reward Signal Model

SIGNAL:  ✕ AVOID
RATIO B: 4.73x  (Method B at 28× FY2027E = $1,232 — high but price is $1,065
                  and EPP floor is only $274; the risk premium is asymmetric)
DATE:    2026-05-25
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "LLY"
COMPANY = "Eli Lilly and Company"
SECTOR  = "Pharmaceuticals · GLP-1 Obesity/Diabetes · Oncology · Neuroscience"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  = 1065.00  # LLY — fetched from Yahoo Finance, 2026-05-25; 52-wk high $1,133.95
PRICE_52W_LOW  =  750.00  # approx. late-2024 / early-2025 trough (GLP-1 demand scare)
PRICE_52W_HIGH = 1133.95  # 52-week intraday high
SHARES_M       =  951.0   # million diluted shares outstanding

# ── EPS (non-GAAP / adjusted — LLY's own reported metric) ────────────────────
# LLY fiscal year = calendar year (Jan–Dec).
# Pre-GLP-1-explosion history (context for the trough floor):
EPS_FY2022 =  8.19    # FDA approval of Mounjaro (tirzepatide); revenue ramp beginning
EPS_FY2023 =  6.32    # GAAP impacted by acquired IPR&D; non-GAAP ~$6.32; Mounjaro still ramping
EPS_FY2024 = 13.73    # First full ramp year: Mounjaro + Zepbound launch; revenue ~$45B
EPS_FY2025 = 22.00    # FY2025 non-GAAP; original guidance $20.78-22.28; confirmed at midpoint
                       # Q4 2025 non-GAAP EPS was $7.54
EPS_NOW    = 36.25    # FY2026E non-GAAP; raised guidance $35.50-37.00 after Q1 2026 beat
                       # Q1 2026: revenue $19.8B (+56% YoY); non-GAAP EPS $8.55 (+156% YoY)

# ── EPP Floor ─────────────────────────────────────────────────────────────────
# Trough EPS = FY2024 ($13.73): the last "anchored" year before the GLP-1 explosion.
# If tirzepatide demand disappoints structurally (competition, pricing, saturation),
# EPS could reset toward this level as growth moderates.
# Min-viable P/E = 20×: LLY is a best-in-class Big Pharma with deep pipeline;
# even in a bear scenario it would not trade below 18-20× on normalized earnings.
EPS_TROUGH = 13.73    # FY2024 non-GAAP — trough anchor before GLP-1 ramp
EPP_MIN_PE = 20       # Pharma quality floor; LLY minimum viable trough multiple
EPP        = EPS_TROUGH * EPP_MIN_PE   # $13.73 × 20 = $274.60

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E consensus non-GAAP EPS ~$44 (raised after Q1 2026 beat; range $42-46)
# Exit P/E: 28× — a blend between large-pharma (20-25×) and growth-pharma (35-40×).
# Assumes GLP-1 growth moderates by 2027 as Novo, Amgen and Roche compete;
# but LLY retains category leadership and justifies a modest premium.
#   At 28×: $1,232  (+15.7% upside from $1,065)
#   At 35×: $1,540  (+44.6% upside — requires sustained 40%+ GLP-1 growth)
#   At 40×: $1,760  (+65.3% — requires retatrutide approval + Alzheimer's ramp)
CONS_EPS_2YR = 44.00
CONS_EXIT_PE = 28

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
# BEAR:  GLP-1 demand shock + pricing legislation; EPS reset to ~$18-20 range;
#        market de-rates to 18× on uncertainty — approaching prior pharma trough
# BASE:  FY2027E $44 × 27× (competitive growth pharma; slight premium to sector)
# BULL:  Retatrutide Phase 3 success + oral orforglipron approval; $44 × 37×
# XBULL: LLY adds donanemab (Alzheimer's), CVD outcomes, full retatrutide;
#         FY2029E ~$70 × 40× = $2,800; transforms into the defining biopharma franchise
PRICE_BEAR  =  360
PRICE_BASE  = 1200
PRICE_BULL  = 1630
PRICE_XBULL = 2800

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.70, 0.30, "Mounjaro/Zepbound GLP-1 dominance; Novo rivalry but LLY leads on efficacy"),
    (+0.50, 0.20, "Pipeline depth: retatrutide (triple agonist), orforglipron (oral), donanemab"),
    (+0.30, 0.15, "$27B manufacturing capex 2024-2026 — scaling supply ahead of demand"),
    (-0.50, 0.15, "IRA drug pricing (Medicare negotiation) + EU reference pricing pressure"),
    (-0.30, 0.10, "GLP-1 competition: Novo, Amgen, Roche, Pfizer all in late-stage development"),
    (-0.30, 0.10, "Valuation risk: 29× FY2026E — all visible growth already discounted"),
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
  FY2024 non-GAAP EPS ($13.73) × 20× minimum pharma floor multiple.
  FY2024 was the last "anchored" year before the GLP-1 explosion. If
  tirzepatide demand disappoints structurally (IRA pricing, competition),
  EPS could revert toward this level. EPP = $274.60.
  The 52-week low (~$750) was ~55× FY2024 EPS — the market never allowed
  LLY to test the EPP floor, reflecting pipeline optionality premium.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E consensus non-GAAP EPS $44 × 28× conservative exit P/E = $1,232.
  At 28×: +15.7% upside from current $1,065.
  At 35×: $1,540 (+44.6%); at 40×: $1,760 (+65.3%).
  Ratio B = ($1,065 − $274.60) / ($1,232 − $1,065) = $790 / $167 = 4.73×
  → ✕ AVOID. The downside to EPP ($790) dwarfs the upside to Method B ($167).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ELI LILLY: THE BEST DRUG FRANCHISE IN THE WORLD — BUT WHAT'S THE PRICE?
=========================================================================

LLY is, without question, the most powerful biopharma franchise of this
decade. Tirzepatide (Mounjaro for type-2 diabetes; Zepbound for obesity)
is the best-in-class dual GIP/GLP-1 agonist, demonstrating superior weight
loss and glycaemic control versus semaglutide in head-to-head trials. The
company is now the most valuable pharmaceutical company on Earth. The debate
is not about quality — the debate is entirely about the price you pay.

Q1 2026 — EXCEPTIONAL RESULTS (REPORTED APRIL 30, 2026)
════════════════════════════════════════════════════════
  Revenue:              $19.8B (+56% YoY) — beat consensus by 12.5%
  Non-GAAP EPS:         $8.55 (+156% YoY) — beat consensus by 22.7%
  Mounjaro + Zepbound:  $12.8B combined   (the GLP-1 duopoly in a single company)
  FY2026 guidance raised: Revenue $82-85B (+28% midpoint); EPS $35.50-37.00
  Pre-market reaction:  +5.96%

The 156% EPS growth in a single quarter is staggering for a mega-cap.
Manufacturing is finally scaling to meet structural demand.

THE GLP-1 MEGA-CYCLE: CONTEXT
══════════════════════════════
The obesity epidemic affects ~1 billion adults globally. GLP-1 agonists
represent a paradigm shift: the first drug class that works for the
majority of patients at scale. Additional indications in clinical trials:
  • Cardiovascular risk reduction (SURPASS-CVOT completed)
  • Sleep apnea (FDA approved for Zepbound, 2025)
  • NASH/metabolic liver disease (SYNERGY-NASH study ongoing)
  • Alzheimer's disease (TRAILBLAZER-ALZ studies for donanemab)
  • Retatrutide: GIP/GLP-1/glucagon triple agonist — Phase 3 ongoing;
    early data showed 24% average weight loss at 48 weeks (superior to
    any approved agent including semaglutide 2.4mg and tirzepatide)

If retatrutide is approved, LLY potentially has the market's best drug,
then an even better drug ready to follow — an unprecedented compounding moat.

THE $27 BILLION MANUFACTURING BET
═══════════════════════════════════
LLY committed $27B in manufacturing capex (2024-2026) to scale injectable
GLP-1 production globally: Ireland, Indiana (multiple sites), Germany,
Singapore, North Carolina. Supply constraints were the primary FY2025
headwind; Q1 2026 revenue growth (+56%) confirms those constraints are
lifting. This is the most aggressive manufacturing expansion in pharma history.

COMPETITIVE LANDSCAPE — THE RISK
══════════════════════════════════
Novo Nordisk holds ~60% of the current GLP-1 market (semaglutide/Ozempic/
Wegovy). Competition in late-stage development includes:
  • Amgen (AMG 133): Phase 3; differentiated mechanism
  • Roche/Zealand (CT-388): Phase 3; injectable triple agonist
  • AstraZeneca/Eccogene (AZD9550): oral GLP-1; Phase 3
  • Pfizer: oral danuglipron; Phase 3 (earlier version failed; restarted)
The oral market is the key frontier — LLY's orforglipron (oral GLP-1) is
in Phase 3 and will be pivotal; if successful, it opens the market to the
~60-70% of patients who refuse injections.

IRA PRICING RISK
══════════════════
The Inflation Reduction Act Medicare drug negotiation targeted semaglutide
and tirzepatide for the 2026-2027 negotiation list. CMS negotiated price
reductions of 40-65% for Medicare Part D. This headwind is embedded in
FY2026 guidance ("lower realized prices" were noted as a 13% headwind to
Q1 revenue growth, partially offset by volume). Further IRA negotiation
rounds remain a structural overhang.

VALUATION: THE CORE PROBLEM
═════════════════════════════
At $1,065 / $36.25 FY2026E non-GAAP EPS = 29.4× forward P/E.
Historical LLY P/E ranges:
  Pre-GLP-1 (2018-2022):   20-30×   (growth pharma with pipeline premium)
  GLP-1 ramp (2023):       35-55×   (explosive growth; narrative-driven)
  Post-peak (2024-2025):   25-38×   (demand concerns, IRA, supply issues)
  Current:                 29.4×    — fair for a 28% growth year, but:

The problem: FY2028+ growth is expected to slow as the GLP-1 market matures.
If EPS growth slows to 15-20% by FY2028-2029, the stock likely de-rates to
20-25×. At $70 FY2029E EPS × 22× = $1,540 — only ~45% upside over 4 years.
That's 10%/yr — below what the risk warrants at a 29× entry.

WHERE THE RISK/REWARD IMPROVES
════════════════════════════════
  WATCHLIST  : $820-880   (FY2027E 19-20×; ratio_b ~1.6×; near-bear zone)
  ACCUMULATE : $680-740   (FY2027E ~15-17×; ratio_b ~0.9×; trough P/E zone)
  BUY        : $450-550   (approaching EPP + pipeline optionality floor)

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

print(f"  Current price         : ${CURRENT_PRICE:.2f}  (+42% from 52-wk low ~${PRICE_52W_LOW}; -6% from 52-wk high ${PRICE_52W_HIGH})")
print(f"  EPP floor             : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above; 20× × ${EPS_TROUGH} FY2024 non-GAAP trough)")
print(f"  Method B (28× exit)   : ${price_b:.2f}  (ratio_b = {ratio_b:.2f}× → ✕ AVOID)")
print(f"  At 35× exit           : ${CONS_EPS_2YR*35:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*35-CURRENT_PRICE):.2f}× → WATCHLIST (still expensive)")
print(f"  At 40× exit           : ${CONS_EPS_2YR*40:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*40-CURRENT_PRICE):.2f}× → WATCHLIST (requires ~40× exit)")
print(f"  BEAR scenario         : ${PRICE_BEAR}   (-66%; GLP-1 demand shock; EPS ~$20; 18×)")
print(f"  BASE scenario         : ${PRICE_BASE}  (+13%; FY2027E $44 × 27×; modest premium to large pharma)")
print(f"  BULL scenario         : ${PRICE_BULL}  (+53%; FY2027E $44 × 37×; retatrutide Phase 3 success)")
print(f"  XBULL scenario        : ${PRICE_XBULL}  (+163%; FY2029E ~$70 × 40×; multi-franchise dominant)")
print(f"  Forward P/E (FY2026E) : {CURRENT_PRICE/EPS_NOW:.1f}×  (${CURRENT_PRICE} / ${EPS_NOW}; fair for 28% growth)")
print(f"  Forward P/E (FY2027E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (${CURRENT_PRICE} / ${CONS_EPS_2YR}; priced for continued 30%+ growth)")
print(f"  EPS history           : FY22 ${EPS_FY2022} → FY23 ${EPS_FY2023} → FY24 ${EPS_FY2024} → FY25 ${EPS_FY2025} → FY26E ${EPS_NOW}")
print(f"  Q1 2026               : Rev $19.8B (+56% YoY); non-GAAP EPS $8.55 (+156% YoY)")
print(f"  Mounjaro + Zepbound   : $12.8B Q1 2026 combined revenue; supply finally scaling")
print(f"  IRA pricing headwind  : -13% realized price impact vs volume +65% in Q1 2026")
print(f"  Market cap            : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  Dividend yield        : ~0.6% at current price (yield compressed by rally)")
print(f"  WATCHLIST entry       : $820-880  (FY2027E ~19-20×; ratio_b ~1.6×)")
print(f"  ACCUMULATE entry      : $680-740  (FY2027E ~15-17×; ratio_b ~0.9×; trough P/E territory)")
print(f"  BUY entry             : $450-550  (approaching EPP floor + pipeline optionality)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.35×  |  Idiosyncratic: 80%  |  Macro: 20%

  Driver                                                     Type    Wt  Note
  ────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  Mounjaro/Zepbound GLP-1 dominance (best-in-class data)    IDIO    30%  PRIMARY: volume +65% YoY; $12.8B Q1 alone
  Pipeline optionality (retatrutide, orforglipron, donanemab) IDIO  20%  Retatrutide = potential best drug ever approved
  Manufacturing scale-up ($27B capex resolved supply crunch) IDIO  15%  Q1 confirms supply no longer the bottleneck
  IRA drug pricing / Medicare negotiation pressure           IDIO    15%  KEY BEAR: -13% price headwind already; more rounds ahead
  GLP-1 competition (Novo, Amgen, Roche, AZ)                IDIO    10%  Timeline: 2027-2029; LLY has 2+ year lead
  Macro / interest rates / USD strength                      MACRO   10%  Low beta; mostly idiosyncratic pharma story""")

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
  BEAR  (${PRICE_BEAR}) : IRA negotiation rounds slash tirzepatide price 60%+;
               competition launches competitive agents by 2027; EPS reset to
               ~$18-20. Market de-rates to 18× = $360. –66% from current.
               Low near-term probability but severe if it occurs — the asymmetry
               of a 29× entry is painful in a bear scenario.

  BASE  (${PRICE_BASE}) : FY2027E $44 non-GAAP EPS × 27× (competitive growth pharma
               premium). GLP-1 market grows but competition takes share. Retatrutide
               approved but priced aggressively under IRA. +13% upside from current.
               Disappointing for 2-year holding period.

  BULL  (${PRICE_BULL}) : Retatrutide Phase 3 succeeds with best-ever weight-loss data;
               orforglipron oral GLP-1 approved; donanemab shows durable Alzheimer's
               benefit. Market assigns 37× FY2027E = $1,630. +53% upside. Requires
               multiple pipeline catalysts to all succeed simultaneously.

  XBULL (${PRICE_XBULL}) : LLY becomes the defining biopharma franchise of the 2030s —
               obesity, diabetes, Alzheimer's, and cardiovascular all dominated by LLY
               compounds. FY2029E ~$70 × 40× = $2,800. +163%. A 5-year hold,
               not a 2-year thesis. Very high risk of partial failure on any leg.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-25")
print("=" * 72)
