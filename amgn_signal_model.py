"""
Amgen Inc. (NASDAQ: AMGN) — BottomUp Risk/Reward Signal Model

SIGNAL:  ▷ HOLD/TRIM
RATIO B: 2.02x  (Method B at 16× FY2027E $24.50 = $392.00; ratio 121.7/60.3 = 2.02×)
DATE:    2026-05-25
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "AMGN"
COMPANY = "Amgen Inc."
SECTOR  = "Biotechnology · Inflammation/Oncology · Rare Disease (Horizon) · Obesity Pipeline (MariTide)"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  = 331.70   # AMGN — Yahoo Finance, 2026-05-22; +27% from 52-wk low; -15% from 52-wk high
PRICE_52W_LOW  = 261.43   # 52-week low (May 14, 2025; LOE fears + Horizon debt overhang)
PRICE_52W_HIGH = 391.29   # 52-week high (March 2, 2026; MariTide Phase 2 enthusiasm)
SHARES_M       = 537.0    # million diluted shares (~$177.8B market cap / $331.70)
DIVIDEND_ANN   =   9.20   # ~$2.30/quarter; ~2.77% yield; meaningful income with a growing EPS base

# ── EPS (non-GAAP adjusted) ────────────────────────────────────────────────────
# AMGN FY = calendar year. The EPS arc reflects two key events:
# (1) Horizon Therapeutics acquisition closed Oct 6, 2023 for $27.8B (~$116.50/share).
#     Horizon added rare disease franchises: Tepezza (thyroid eye disease),
#     Krystexxa (gout), Uplizna (neuromyelitis optica). FY2024+ are the first
#     full-year comparables including Horizon revenue and associated interest expense.
# (2) Enbrel biosimilar erosion: Enbrel was ~$4.5B/yr at peak; FY2025 $2.23B
#     (-50% from peak). Biosimilars entered the US market in 2019. Decline is
#     ongoing but the rate is slowing as substitution is nearly complete.
EPS_FY2022 = 17.00    # est; pre-Horizon; inflammation + oncology + Enbrel; legacy Amgen
EPS_FY2023 = 17.69    # actual; Horizon closes Oct 2023; Q4 2023 partial Horizon contribution
EPS_FY2024 = 18.65    # actual; first full year Horizon; +5.4% YoY; debt drag absorbed
EPS_FY2025 = 19.84    # actual; second full year Horizon; +6.4% YoY; Repatha/Evenity growing
EPS_NOW    = 22.40    # FY2026E midpoint (guidance raised to $21.70-$23.10 post-Q1 2026)
                       # Q1 2026: revenue $8.62B; adj EPS $5.15; beat consensus
                       # Tepezza +24% YoY; Repatha +22%; R&D +16% (MariTide Phase 3 investment)

# ── EPP Floor ─────────────────────────────────────────────────────────────────
# EPS_TROUGH = Enbrel erosion fully complete ($2.23B → ~$0) + Otezla LOE Feb 2028
# + Horizon product pressure + recession. Starting from FY2024 $18.65, a severe
# combo of LOE cliffs + macro recession could compress EPS ~20% to ~$15.00.
# Calibration: 52-wk low $261.43 ÷ $15.00 = 17.4× — the market bottomed at
# 17.4× stress EPS. At EPP (14× structural floor), $15 × 14 = $210 represents
# a true panic/capitulation level (e.g., MariTide fails Phase 3 + deep recession).
# EPP_MIN_PE = 14: diverse biopharma with Horizon rare disease + robust oncology
# pipeline and growing Repatha/Evenity warrants 14× as an absolute floor, not 10-11×.
EPS_TROUGH = 15.00    # Enbrel to zero + Otezla LOE + recession; ~20% below FY2024 trough
EPP_MIN_PE = 14       # diversified biopharma floor: Horizon rare disease + oncology + pipeline
EPP        = EPS_TROUGH * EPP_MIN_PE   # $15.00 × 14 = $210.00

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E ~$24.50: FY2026E $22.40 × 9.4% growth. Growth drivers:
#   • Repatha (PCSK9): +22% Q1 2026; expanding label (high-CV-risk patients);
#     biosimilar competition eventually but not until 2026-2028 in key markets
#   • Evenity (romosozumab): +strong growth; osteoporosis; Japan/US/EU expansion
#   • Tepezza: +24% Q1 2026; rare disease; Horizon integration synergies
#   • MariTide: R&D investment = EPS headwind now, but Phase 3 optionality in value
#   • Tezspire: mild growth; partnered with AstraZeneca (50/50 split)
#   • Cost discipline: $700M+ cost saves by 2027 partially offsetting LOE
# Exit P/E: 16× — Amgen trades 14-18× non-GAAP in normal conditions. At 16×,
# the market discounts Horizon debt ($28B), LOE overhang, and MariTide uncertainty
# but still assigns growth-biotech-quality premium to the pipeline.
#   At 16×: $392.00  (+18.2% from $331.70) — consensus; Ratio B = 2.02× → HOLD/TRIM
#   At 19×: $465.50  (+40.3%) — MariTide Phase 3 positive; multiple re-rate
#   At 22×: $539.00  (+62.5%) — MariTide approval + obesity franchise emerging
CONS_EPS_2YR = 24.50
CONS_EXIT_PE = 16

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
# BEAR:  MariTide Phase 3 failure + Otezla LOE 2028 hits hard + recession.
#        Enbrel erosion complete; debt servicing on $28B Horizon constrains FCF.
#        EPS stabilises near $14.50; market applies 13.1× = $190. -43% from current.
# BASE:  Managed LOE via cost cuts + pipeline; MariTide Phase 3 positive but modest
#        initial uptake; EPS grows 8-10%/yr through 2027. $24.50 × 15.1× = $370.
# BULL:  MariTide Phase 3 strong data + label obtained late 2028; multiple expansion
#        to 19× as obesity market opportunity ($50B+ TAM) re-rated. $24.50 × 20× = $490
#        + peak obesity pipeline premium.
# XBULL: MariTide becomes #2 obesity drug globally (monthly dosing vs weekly Ozempic
#        wins adherence); $15-20B annual revenue by 2032; FY2028-29E ~$30 × 22× = $660.
PRICE_BEAR  =  190
PRICE_BASE  =  370
PRICE_BULL  =  500
PRICE_XBULL =  680

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.40, 0.25, "MariTide Phase 3 (obesity): ~20% wt loss; monthly dosing vs weekly GLP-1"),
    (+0.30, 0.20, "Oncology pipeline quality: Lumakras, Blincyto, IMDELLTRA, Xgeva"),
    (+0.20, 0.15, "Horizon rare disease: Tepezza +24% Q1 2026; Krystexxa growing; synergies"),
    (-0.30, 0.20, "Enbrel biosimilar erosion: $2.23B FY2025 vs $4.5B+ peak; ongoing decline"),
    (-0.35, 0.20, "Otezla LOE Feb 2028 + Horizon debt $28B: LOE cliff + FCF constraints"),
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
  Stress EPS ($15.00) × 14× diversified biopharma floor. EPS_TROUGH is set
  ~20% below FY2024 actual ($18.65), representing Enbrel fully eroding to
  zero, Otezla LOE hitting in 2028, and a simultaneous recession. At 14×,
  the market is applying a distressed-but-not-broken multiple — appropriate
  for a company with a diversified oncology/rare disease pipeline and the
  financial capacity to service the Horizon debt.
  EPP = $210.00.
  Calibration: 52-wk low $261.43 ÷ $15.00 = 17.4× stress EPS — the market
  has already stress-tested AMGN at 17.4× trough, well above the EPP floor,
  confirming 14× as a genuine structural floor reserved for capitulation.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E ~$24.50 (FY2026E $22.40 × 9.4% growth; Repatha/Evenity/Tepezza
  scaling; cost savings offsetting LOE; MariTide R&D investment ongoing) ×
  16× consensus exit = $392.00.
  Ratio B = ($331.70 − $210.00) / ($392.00 − $331.70) = $121.70 / $60.30 = 2.02×
  → ▷ HOLD/TRIM. At 14.8× FY2026E, Amgen is fairly priced for its current
  earnings trajectory — not expensive, but not compelling without MariTide
  data or a significant price correction.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AMGEN: WAITING FOR MARITIDE — FAIRLY PRICED WHILE THE CLOCK TICKS
===================================================================

Amgen is the original biotechnology company — founded 1980, first products
(EPO, G-CSF) approved in 1989. Today it is a $178B diversified biopharmaceutical
with major franchises in inflammation, oncology, osteoporosis, and (via the
Horizon acquisition) rare disease. The pipeline is genuinely deep: 40+
molecules in development, with MariTide as the potential generational catalyst.
The thesis for holding is intact. The thesis for buying now requires either
(a) a meaningful price correction toward $270-300, or (b) positive MariTide
Phase 3 interim data that re-rates the multiple — neither has occurred yet.

Q1 2026 — SOLID BEAT; GUIDANCE RAISED; MARITIDE INVESTEMENT ACCELERATING
==========================================================================
  Revenue:                $8.62B   (+9% YoY; beat consensus)
  Adjusted EPS:           $5.15    (+13% YoY; beat)
  FY2026 guidance raised: adj EPS $21.70-$23.10 (midpoint $22.40; raised)
  Tepezza (Horizon):      +24% YoY — thyroid eye disease; pricing power
  Repatha (PCSK9):        +22% YoY — label expansion; market penetration
  Evenity (osteoporosis): growing strongly; Japan/US dual-market driver
  Enbrel:                 -13% YoY — biosimilar erosion continues; manageable
  R&D expenses:           +16% YoY driven by MariTide Phase 3 enrolment

KEY PRODUCTS — THE CURRENT REVENUE BASE
=========================================
  Repatha ($3.02B FY2025, growing +22% Q1 2026):
    PCSK9 inhibitor for hypercholesterolaemia and cardiovascular risk.
    Primary differentiation from statins: works in statin-intolerant patients
    and in high-risk CV patients who cannot reach LDL targets on statins alone.
    Long-term FOURIER outcome data (37% CV event reduction) is expanding
    prescriber comfort. The biosimilar competition window is still 2-3 years
    out in most markets. At $3+ billion and growing, Repatha has become the
    single most important near-term revenue engine.

  Evenity ($2.10B FY2025, growing):
    Romosozumab, an anti-sclerostin antibody for osteoporosis. Unique mechanism:
    builds new bone (anabolic) while inhibiting bone resorption — the only drug
    of its kind. 12-month treatment course; not a continuous therapy. Strong
    growth in Japan (first market), US, and EU. LOE not imminent (discovery
    protection to early 2030s). Growing AMGN conviction driver.

  Tepezza ($2B+ FY2025, from Horizon, +24% Q1 2026):
    Teprotumumab; approved for thyroid eye disease (TED). Only FDA-approved
    treatment for TED. Rare disease premium pricing ($20,000+ per infusion;
    ~$250K+ per course). Horizon paid $27.8B for this and Krystexxa; Tepezza
    growth confirms the strategic rationale. Long-term LOE runway.

  Enbrel ($2.23B FY2025, declining -13%/yr):
    Etanercept (TNF inhibitor) for RA, psoriasis, psoriatic arthritis.
    US biosimilar competition entered 2019; penetration has been gradual
    but ongoing. FY2025 $2.23B vs $4.5B+ peak represents a ~50% erosion
    over 6 years. The rate of decline is slowing — from 15-20%/yr in
    2021-2023 to ~12-13% in 2025 — as the substituted patient pool
    shrinks. Manageable, not catastrophic, but adds to LOE overhang anxiety.

  Otezla ($2B+ est, patent to Feb 2028):
    Apremilast (PDE4 inhibitor) for psoriasis and psoriatic arthritis.
    Amgen acquired Otezla in 2019 from Celgene for $13.4B. US patent expires
    February 2028. This is a known, approaching cliff — no surprise, but
    $2B+ revenue at risk in 2028-2029 is material. Management is aware and
    has structured cost savings accordingly.

  Tezspire ($1.48B FY2025, partnered with AstraZeneca):
    Tezepelumab; severe asthma; TSLP inhibitor. AZ + AMGN 50/50 partnership.
    Growing asthma franchise. Less upside to AMGN vs standalone because of
    the 50/50 economics, but adds diversification and cash flow.

MARITIDE — THE OPTION THE MARKET IS PAYING A MILD PREMIUM FOR
==============================================================
MariTide (AMG-133) is Amgen's obesity candidate: a GIP receptor antagonist /
GLP-1 receptor agonist conjugated to a long-acting half-life extender. Phase 2
results (52-week):
  • Without T2D: ~20% mean body weight loss — competitive with tirzepatide
  • With T2D: ~17% mean body weight loss — comparable to semaglutide
  • Dosing: monthly or less frequent (vs weekly for Ozempic/Wegovy/Mounjaro)
    This is the KEY differentiator. Adherence in GLP-1s is poor (~40-50% at
    1 year). Monthly or bimonthly dosing could substantially improve adherence,
    which is the primary commercial differentiator if efficacy is confirmed.
  • Phase 3 (MARITIME studies): actively enrolling in 2026
    MARITIME-1: Chronic weight management (CWM) — primary endpoint
    MARITIME-CV: Cardiovascular outcomes (like SURMOUNT-CVOT for tirzepatide)
    MARITIME-HF: Heart failure
    MARITIME-OSA: Obstructive sleep apnea
  • First potential approval: ~2028-2029 (if Phase 3 data by mid-2027)
  • TAM: obesity drug market projected $50B+ by 2030

Investment view on MariTide: this is a genuine option that the market is
partially pricing in (AMGN rallied to $391.29 in March 2026 on MariTide
enthusiasm). At current $331.70, the stock has given back ~15% from that
high — reflecting uncertainty about Phase 3 vs Phase 2 translation and
competition from Novo Nordisk + Lilly. Phase 2 at 52 weeks is promising
but not conclusive for Phase 3 at scale. The market is right to be cautious.

HORIZON ACQUISITION — INTEGRATION COMPLETE; DEBT THE ONGOING OVERHANG
=======================================================================
Amgen acquired Horizon Therapeutics in October 2023 for $27.8B ($116.50/share).
  • Tepezza: $2B+ revenue; thyroid eye disease; rare disease pricing power
  • Krystexxa: refractory gout; growing; niche but premium-priced
  • Uplizna: neuromyelitis optica spectrum disorders (NMOSD); small but growing
  • Vijoice: PIK3CA-related disorders; small

Integration is essentially complete. Management commentary in Q1 2026:
Horizon synergies running ahead of schedule. The product P&L is accretive.

The Horizon DEBT ($28B gross; ~$24-25B net): Amgen's credit rating was
downgraded at acquisition. Interest expense is ~$1.5B+/yr. This is a
persistent headwind on FCF conversion and financial flexibility. The market
rightly applies a debt discount to AMGN's multiple vs. a debt-free biotech.
Positive: FCF generation is strong (~$10B+/yr projected FY2026-2027) and
debt paydown is progressing. By 2028-2029, net leverage should be manageable.

LOE SUMMARY — THE MAP TO NAVIGATE
===================================
  Now:          Enbrel $2.23B declining ~12-13%/yr (already in numbers)
  Feb 2028:     Otezla $2B+ enters generic competition
  Post-2028:    Repatha biosimilar competition in some markets
  2030+:        Aranesp, Neulasta, older franchises largely biosimilar

Offset by: Tepezza (rare disease exclusivity ~2028+), Evenity (2030+ LOE),
Repatha US protection ~2027+, Tezspire, MariTide (if approved 2028-2029),
IMDELLTRA (bispecific T-cell engager, DLL3/CD3, for small cell lung cancer
— recently approved; early $500M+ revenue potential), and pipeline ADCs.

IMDELLTRA — WORTH WATCHING
============================
IMDELLTRA (tarlatamab) received FDA accelerated approval in 2024 for
relapsed/refractory small cell lung cancer (SCLC). SCLC is a notoriously
difficult-to-treat malignancy with almost no good second-line options.
Revenue in 2025: ~$500M (estimate); growing strongly. Confirmatory trial
ongoing (full approval expected 2026-2027). This is an underappreciated
near-term revenue driver.

BALANCE SHEET AND CASH FLOW
=============================
  FY2025 non-GAAP EPS:      $19.84 (actual)
  FY2026E non-GAAP EPS:     $22.40 (midpoint; guided)
  FCF generation:           ~$9-10B/yr (strong; funding Horizon debt paydown)
  Net debt:                 ~$24-25B (post-Horizon; declining at ~$3B/yr)
  Dividend:                 $9.20/yr (~$2.30/quarter); ~2.77% yield
  Buybacks:                 paused/minimal while paying down Horizon debt

WHERE RISK/REWARD IMPROVES
============================
  WATCHLIST          : $295-330  (stock approaches 52-wk midpoint; ratio_b ~1.4-1.7×)
  ACCUMULATE         : $270-295  (near/approaching 52-wk low territory; ratio_b ~1.0-1.3×)
  BUY                : $250-270  (at/below 52-wk low; structural trough; ratio_b <1.0×)
  HOLD current       : $330-370  (fair value range; await MariTide Phase 3 data)
  TRIM               : $375-400  (approaching 52-wk high; ratio_b >2.5×; MariTide priced)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("PART 3 — NUMBERS & SIGNALS")
print("=" * 72)
print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │  SIGNAL:  {signal_primary:<12}  │  RATIO B: {ratio_b_fmt:<10}               │
  │  TICKER:  {TICKER:<10}    │  SECTOR:  Healthcare / Biotechnology  │
  └──────────────────────────────────────────────────────────────────┘

  ----------------------------------------------------------------------
""")

print(f"  Current price         : ${CURRENT_PRICE:.2f}  (+27% from 52-wk low ${PRICE_52W_LOW}; -15% from 52-wk high ${PRICE_52W_HIGH})")
print(f"  EPP floor             : ${EPP:.2f}   (+{epp_gap_pct:.1f}% above; 14× × ${EPS_TROUGH} stress EPS; 52-wk low ${PRICE_52W_LOW} ÷ $15 = 17.4×)")
print(f"  Method B (16× exit)   : ${price_b:.2f}  (+{(price_b/CURRENT_PRICE-1)*100:.1f}%; ratio_b = {ratio_b:.2f}× → HOLD/TRIM)")
print(f"  At 19× exit           : ${CONS_EPS_2YR*19:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*19-CURRENT_PRICE):.2f}× (MariTide Phase 3 positive re-rate)")
print(f"  At 22× exit           : ${CONS_EPS_2YR*22:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*22-CURRENT_PRICE):.2f}× (MariTide approval + obesity franchise)")
print(f"  BEAR scenario         : ${PRICE_BEAR}   (-43%; Phase 3 failure + Otezla LOE + recession; EPS $14.50 × 13.1×)")
print(f"  BASE scenario         : ${PRICE_BASE}   (+12%; managed LOE; EPS growth intact; $24.50 × 15.1×)")
print(f"  BULL scenario         : ${PRICE_BULL}   (+51%; MariTide Phase 3 success + approval pipeline; $24.50 × 20.4×)")
print(f"  XBULL scenario        : ${PRICE_XBULL}   (+105%; MariTide #2 obesity globally; FY2028-29E ~$30 × 22.0×)")
print(f"  Forward P/E (FY2026E) : {CURRENT_PRICE/EPS_NOW:.1f}×   (${CURRENT_PRICE} / ${EPS_NOW}; modest for quality biopharma with MariTide option)")
print(f"  Forward P/E (FY2027E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×   (${CURRENT_PRICE} / ${CONS_EPS_2YR}; 16× = consensus exit; fairly valued)")
print(f"  EPS history           : FY22 ~${EPS_FY2022} → FY23 ${EPS_FY2023} → FY24 ${EPS_FY2024} → FY25 ${EPS_FY2025} → FY26E ${EPS_NOW}")
print(f"  Q1 2026               : Revenue $8.62B (+9%); adj EPS $5.15 (+13%); guidance raised")
print(f"  Repatha               : $3.02B FY2025; +22% Q1 2026; PCSK9; expanding label")
print(f"  Evenity               : $2.10B FY2025; osteoporosis; unique anabolic mechanism; LOE 2030+")
print(f"  Tepezza               : $2B+ FY2025; +24% Q1 2026; thyroid eye disease; rare disease pricing")
print(f"  Enbrel                : $2.23B FY2025; -13% Q1 2026; biosimilar erosion; slowing decline rate")
print(f"  Otezla                : ~$2B+ est; patent to Feb 2028; psoriasis/PsA; LOE cliff visible")
print(f"  MariTide              : Phase 3 (MARITIME); ~20% wt loss; monthly dosing; approval ~2028-2029")
print(f"  IMDELLTRA             : tarlatamab; SCLC; FDA accelerated approval 2024; ~$500M+ growing")
print(f"  Horizon acquisition   : $27.8B (Oct 2023); Tepezza + Krystexxa + Uplizna; integrated")
print(f"  Horizon debt          : ~$24-25B net; ~$1.5B+/yr interest; paydown ~$3B/yr from FCF")
print(f"  Dividend              : ${DIVIDEND_ANN:.2f}/yr ({DIVIDEND_ANN/CURRENT_PRICE*100:.1f}% yield; growing annually; income anchor)")
print(f"  Market cap            : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  HOLD/TRIM zone        : $330-375  (current; await MariTide Phase 3 data or price correction)")
print(f"  WATCHLIST entry       : $295-330  (ratio_b ~1.4-1.7×; patience rewarded)")
print(f"  ACCUMULATE entry      : $270-295  (approaching structural support; ratio_b ~1.0-1.3×)")
print(f"  BUY zone              : $250-270  (at/below 52-wk low; ratio_b <1.0×; structural floor)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.55×  |  Idiosyncratic: 70%  |  Macro: 30%

  Driver                                                      Type    Wt  Note
  ─────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  MariTide Phase 3 (obesity): monthly dosing; 20% wt loss   IDIO  25%  OPTION: Phase 3 binary; 2027 readout
  Repatha/Evenity/Tepezza growth: +22%/+strong/+24% Q1 2026 IDIO  25%  BULL: core franchise compounding
  Enbrel erosion: -13%/yr; ~$2.23B; slowing decline         IDIO  20%  BEAR: persistent headwind; manageable
  Otezla LOE Feb 2028 + Horizon debt $28B                   IDIO  15%  RISK: known cliff; FCF to pay down debt
  Macro/rates: biotech multiple sensitivity; healthcare PBM  MACRO 15%  MODERATE: lower rates = multiple expansion""")

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
  BEAR  (${PRICE_BEAR}) : MariTide Phase 3 failure (loss of the obesity option) combined
               with Otezla LOE 2028 hitting hard and a simultaneous recession.
               Enbrel erosion complete; Horizon debt servicing constrains FCF.
               EPS stabilises near $14.50; market applies 13.1× distressed-
               quality multiple = $190. -43% from current. Low probability
               but not zero — Phase 3 failure in obesity is a real binary risk.

  BASE  (${PRICE_BASE}) : Managed LOE trajectory: Enbrel decline slows to $1.5B by 2027;
               cost saves ($700M+) partially offset Otezla cliff; Repatha
               and Evenity continue double-digit growth; Tepezza sustains
               rare disease premium. MariTide Phase 3 positive but uptake
               begins slowly (2028-2029 ramp). $24.50 × 15.1× = $370. +12%.

  BULL  (${PRICE_BULL}) : MariTide Phase 3 delivers strong positive data (2027 readout);
               monthly dosing wins adherence market vs weekly GLP-1s; FDA
               approves late 2028; management raises revenue guidance toward
               $3-5B by 2030. Multiple expands from 15-16× to 19-20×.
               $24.50 × 20.4× = $500. +51% from current.

  XBULL (${PRICE_XBULL}) : MariTide becomes the dominant obesity drug globally — the
               monthly/bimonthly injection convenience creates a structural
               adherence advantage that drives 60%+ of new obese patients
               to AMGN after label expansion to cardiovascular prevention.
               $15-20B annual MariTide revenue by 2032; FY2028-29E ~$30
               × 22.0× = $660. +105%. Requires Phase 3 excellence +
               commercial execution.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-25")
print("=" * 72)
