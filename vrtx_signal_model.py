"""
Vertex Pharmaceuticals Incorporated (NASDAQ: VRTX) — BottomUp Risk/Reward Signal Model

SIGNAL:  ▷ HOLD/TRIM
RATIO B: 2.36x  (Method B at 27× FY2027E $20.00 = $540.00; ratio 253.00/107.00 = 2.36×)
DATE:    2026-05-26
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "VRTX"
COMPANY = "Vertex Pharmaceuticals Incorporated"
SECTOR  = "Large-Cap Biopharma · CF Monopoly (TRIKAFTA/ALYFTREK) · Pain (JOURNAVX) · Kidney (Povetacicept) · T1D Cell Therapy"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  = 433.00   # VRTX — Yahoo Finance, 2026-05-23; -15% from 52-wk high; +20% from low
PRICE_52W_LOW  = 362.50   # 52-week low (mid-2025; CF competition fears + suzetrigine acute pain ramp concerns)
PRICE_52W_HIGH = 507.92   # 52-week high (Jan 2026; povetacicept IgAN Phase 3 RAINIER data catalyst)
SHARES_M       = 254.0    # million diluted shares (~$110B market cap / $433)
DIVIDEND_ANN   =   0.00   # VRTX pays no dividend; returns capital exclusively via buybacks

# ── EPS (non-GAAP adjusted) ────────────────────────────────────────────────────
# VRTX FY = calendar year. Non-GAAP EPS excludes: stock-based compensation,
# intangible amortization (primarily from Alpine/CymaBay-type acquisitions),
# and acquired IPR&D. The EPS arc reflects Vertex's 10-15%/yr compound growth
# driven by expanding CF market penetration (TRIKAFTA → ALYFTREK upgrade
# cycle), price increases, and rising margins as R&D spending is spread over
# a larger revenue base. CF now covers 90% of ~88,000 CF patients in developed
# markets. Every new CFTR modulator approval adds another ~2-3% revenue uplift.
EPS_FY2022 = 11.86    # est; ~$8.93B revenue; ~34% non-GAAP net margin; CF gaining share
EPS_FY2023 = 13.04    # est; ~$9.86B revenue; TRIKAFTA global uptake; margins expanding
EPS_FY2024 = 15.15    # est; ~$10.77B revenue; CASGEVY launch (sickle cell + TDT); JOURNAVX NDA filed
EPS_FY2025 = 16.50    # est; ~$11.1B revenue; JOURNAVX (suzetrigine) approved Jan 2025; ALYFTREK launch
EPS_NOW    = 17.80    # FY2026E (Q1 2026 non-GAAP $4.47; annualised ~$17.88; FY guidance ~$17.80)
                       # Q1 2026: Revenue $2.99B (+8%); CF $2.92B; non-CF (CASGEVY+JOURNAVX) $72M
                       # FY2026 guidance: Revenue $12.95-$13.1B; non-CF revenue ≥$500M

# ── EPP Floor ─────────────────────────────────────────────────────────────────
# EPS_TROUGH = extreme scenario: Abbvie or another CFTR competitor launches
# a superior modulator that takes meaningful Biktarvy-equivalent market share;
# non-CF pipeline (suzetrigine, pove, VX-880 T1D) ALL fail; recession compresses
# healthcare utilization. From FY2026E $17.80: a ~-49% cut to ~$9.00.
# This is an almost impossible scenario in the near term — TRIKAFTA patents
# (key composition: ~2037; method of use: ~2038) mean no generic competition
# before 2037. Abbvie's CFTR program is at early clinical stage. No competitor
# has CF data anywhere near Vertex's.
# Floor P/E = 20×: even at catastrophic trough EPS, VRTX's CF monopoly
# (orphan disease + limited population + pricing power + no substitutes)
# supports 20× as the absolute minimum P/E. This is higher than most pharma
# because the CF franchise has no patent cliff for 10+ years.
# EPP = $180.00.
# Calibration: 52-wk low $362.50 ÷ $9.00 = 40.3× stress EPS — the market
# has NEVER tested the EPP floor. Even at the "depressed" $362 low, the stock
# was at 40× stress EPS. This reflects the CF franchise's extraordinary moat:
# effectively immune to generics for a decade+ and uncontested in its indication.
EPS_TROUGH = 9.00     # Extreme CF competition + all non-CF failures + recession; ~-49% from FY2026E
EPP_MIN_PE = 20       # CF orphan disease monopoly floor; no generics before 2037; inelastic demand
EPP        = EPS_TROUGH * EPP_MIN_PE   # $9.00 × 20 = $180.00

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E ~$20.00: Management guided $12.95-$13.1B in 2026 (+17% YoY), growing
# at 10-12%/yr thereafter. Drivers for 2027:
#   • CF franchise: ALYFTREK (next-gen triple modulator, approved 2025) driving
#     the upgrade cycle. Patients on TRIKAFTA switching to ALYFTREK for better
#     outcomes — approximately $200-300 higher net price per patient. CF revenue
#     could reach $13.5-14B by 2027 with price + modest volume growth.
#   • JOURNAVX (suzetrigine): FDA-approved Jan 2025 for acute pain. First-in-
#     class selective NaV1.8 inhibitor — no opioid mechanism, no addiction risk,
#     no sedation. DPN (diabetic peripheral neuropathy) Phase 3 PIVOTAL underway
#     (Breakthrough Therapy designation). If DPN approved: $3B+ peak potential.
#     First full commercial year in acute pain 2026; DPN approval possible 2027.
#   • Povetacicept (pove) IgAN: BLA filed H1 2026. Phase 3 RAINIER hit primary
#     endpoint (-52% proteinuria reduction vs +4.3% for placebo). IgA nephropathy
#     is a rare kidney disease (~130,000 US patients) with no disease-modifying
#     treatment. If approved: first-year revenue $300-500M; peak $2-3B+.
#     Also in Phase 3 for PMN (membranous nephropathy) and MG (myasthenia gravis).
#   • VX-880/VX-264 (T1D cell therapy): Vertex is running Phase 1/2 trials of
#     encapsulated islet cell replacement therapy. Early data: some patients
#     achieved insulin independence. If Phase 3 confirms: $5-10B+ TAM
#     (40M+ T1D patients globally). A potential "functional cure."
#   • Revenue ~$14.5B × ~38% non-GAAP net margin = ~$5.51B / 254M shares ≈ $21.70
#     (slightly above the $20.00 target — conservative estimate chosen)
# Exit P/E: 27× — Vertex typically trades 25-35× forward earnings given its
# high-quality growth profile. 27× is conservative (below the 30-32× average
# during peak CF growth years). Justified if non-CF ramp is slower than expected.
#   At 27×: $540.00  (+25% from $433.00) — conservative; ratio_b = 2.36×
#   At 30×: $600.00  (+39%) — historical average multiple fully restored
#   At 32×: $640.00  (+48%) — full re-rate with pove IgAN + suzetrigine DPN data
CONS_EPS_2YR = 20.00
CONS_EXIT_PE = 27

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
# BEAR:  Abbvie's CFTR modulator achieves superior Phase 3 data vs ALYFTREK
#        (highly unlikely before 2029-2031 but the hypothetical bear case) AND
#        earns FDA approval in ~2030 with best-in-class label. Meanwhile,
#        suzetrigine DPN Phase 3 fails; pove IgAN shows less-than-expected
#        real-world durable benefit; T1D cell therapy has immune rejection
#        issues. CF market shares shift. EPS contracts toward $9 × 18× = $162.
#        -63% from current. An extreme multi-decade scenario. Unlikely before 2031.
# BASE:  CF franchise grows 8-10%/yr (ALYFTREK driving upgrades + new patients
#        in EU/international expansion); JOURNAVX reaches $200-300M in acute
#        pain 2026; pove IgAN approved 2027 ($300-500M first-year revenue);
#        suzetrigine DPN Phase 3 reads out 2027 (positive assumed in BASE).
#        FY2027E $20 × 24× = $480. +11% from current. Modest re-rate.
# BULL:  Suzetrigine DPN approved 2027 (breakthrough therapy; Phase 3 strong);
#        pove approved in IgAN + PMN + MG (three indications 2027-2028);
#        ALYFTREK captures 70%+ of CF patients; T1D cell therapy Phase 3 initiation.
#        Multiple expands to 28.5×. $20 × 28.5× = $570. +32%.
# XBULL: VX-880/VX-264 T1D cell therapy achieves functional insulin independence
#        in >50% of Phase 3 participants — a paradigm shift for diabetes treatment.
#        Suzetrigine DPN becomes a $3B+ product (replacing gabapentinoids globally).
#        Pove establishes VRTX as the dominant renal immunology company. CF
#        extends to 2037+ with no competition. FY2028-29E ~$26 × 27.7× = $720.
#        +66%. Multi-franchise platform company at scale.
PRICE_BEAR  = 162
PRICE_BASE  = 480
PRICE_BULL  = 570
PRICE_XBULL = 720

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.35, 0.25, "CF monopoly: TRIKAFTA/ALYFTREK; 90% of CF patients; patent moat to 2037-38"),
    (+0.40, 0.20, "Povetacicept IgAN: Phase 3 RAINIER -52% proteinuria; BLA filed H1 2026"),
    (+0.25, 0.15, "JOURNAVX (suzetrigine): first NaV1.8; FDA approved Jan 2025; DPN BTD Phase 3"),
    (-0.25, 0.20, "CF competition risk: Abbvie CFTR early-stage; potential 2030+ entry"),
    (-0.20, 0.20, "Valuation: 24.3× FY2026E non-GAAP; -15% from $508 high; limited margin of safety"),
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
  Stress EPS ($9.00) × 20× CF monopoly floor. EPS_TROUGH assumes extreme
  CF competition from Abbvie plus ALL non-CF programs failing — a ~-49%
  EPS cut. Even then, TRIKAFTA patents protect the CF franchise through
  2037-2038 (key composition claims). No approved CF competitor exists or
  is expected before 2030. The 20× floor reflects irreplaceable orphan
  disease monopoly: no generics, inelastic demand, lifelong therapy.
  EPP = $180.00.
  Calibration: 52-wk low $362.50 ÷ $9.00 = 40.3× stress EPS — Vertex
  has NEVER traded near its EPP floor. Even at the cycle low, the market
  applied 40× stress EPS, confirming that investors assign near-zero
  probability to a true CF franchise impairment before the late 2030s.
  This is one of the strongest franchise moats in biopharma.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E ~$20.00 (CF compounding at 10%+ + pove IgAN revenue + suzetrigine
  DPN contribution + ALYFTREK upgrade cycle) × 27× exit P/E (conservative;
  below Vertex's historical 30-32× average — discounts non-CF execution
  risk and CF competition timeline creep) = $540.00.
  Ratio B = ($433.00 − $180.00) / ($540.00 − $433.00) = $253.00 / $107.00 = 2.36×
  → ▷ HOLD/TRIM. The stock is a world-class compounder trading at fair
  value — not cheap, not overvalued. The 52-wk low at $362.50 was the
  entry point (ratio_b ~1.0×, ACCUMULATE). At $433, the expected return
  to Method B is ~25%; the expected downside to EPP is ~-58%. HOLD current
  positions; trim on pops above $500; re-enter at $370-395 or on pove IgAN
  FDA approval (adds $2-3B NPV to price_b) or suzetrigine DPN data.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERTEX: THE RARE CASE OF A TRUE MONOPOLY — BUYING AT THE RIGHT PRICE
=====================================================================

Vertex Pharmaceuticals is the world's only commercial-stage company with
approved CFTR modulator therapies for cystic fibrosis — a rare genetic
lung disease affecting ~88,000 patients in developed markets. TRIKAFTA
(elexacaftor/tezacaftor/ivacaftor) and its next-generation successor
ALYFTREK (vanzacaftor/tezacaftor/deutivacaftor) treat the underlying
mutation in ~90% of CF patients, transforming a progressive fatal disease
into a manageable chronic condition. Revenue from this franchise: $13B+.
Annual revenue growth: 8-12%. Patent protection: ~2037-2038.

This is not a competitive industry — it is a de facto monopoly with
extraordinary pricing power ($300,000+/yr per patient), no substitute
products, and extraordinarily high patient retention (CF patients cannot
stop therapy without rapid disease progression). Vertex's challenge is NOT
protecting the CF franchise for the next decade — it is deploying the
massive cash flows into new therapeutic areas before the CF growth curve
flattens ~2030-2033 as market penetration approaches saturation.

Q1 2026 — BEAT-AND-MAINTAIN; NON-CF RAMP IS THE QUESTION
==========================================================
  Total revenue:          $2.99B  (+8% YoY; beat $2.95B consensus)
  CF revenue:             $2.92B  (+6% YoY; TRIKAFTA $2.35B; ALYFTREK $424M)
  Non-CF revenue:         $72M    (CASGEVY + JOURNAVX combined; growing from ~$0)
  Non-GAAP EPS:           $4.47   (beat $4.33 estimate by $0.14; +13% YoY vs Q1 2025)
  GAAP EPS:               $4.02
  FY2026 guidance:        Revenue $12.95-$13.1B; non-CF ≥$500M; maintained

The beat was modest but consistent: CF growing at the guided pace, and
non-CF beginning to contribute. The ≥$500M non-CF target is where the
narrative hinges — JOURNAVX (suzetrigine) and CASGEVY need to accelerate
meaningfully in H2 2026 to hit it.

THE CF FRANCHISE — UNDERSTANDING THE MOAT PRECISELY
=====================================================
  TRIKAFTA/KAFTRIO (elexacaftor/tezacaftor/ivacaftor):
    FDA-approved October 2019. Gold standard for CF patients with ≥1
    copy of F508del mutation (~90% of CF population). Revenue FY2025:
    ~$11B+ globally. Patient adherence: near-100% (discontinuing causes
    rapid FEV1 decline). No competing approved therapy. The key patents:
    elexacaftor composition: expires ~2037; method of use: ~2038.

  ALYFTREK (vanzacaftor/tezacaftor/deutivacaftor):
    FDA-approved June 2025 (EU 2025). Next-generation triple modulator
    with improved lung function outcomes (+10-15% FEV1 advantage over
    TRIKAFTA in head-to-head) and once-daily dosing vs twice-daily.
    FY2025 revenue: $424M (Q1 2026; first full commercial year). Upgrade
    cycle driving incremental revenue (+$200-300 net price premium) as
    patients and physicians transition from TRIKAFTA to ALYFTREK.
    Timeline to full penetration: 2026-2028. Potential to add ~$1-2B
    in incremental CF revenue as ALYFTREK replaces TRIKAFTA entirely.

  Competition timeline:
    AbbVie: CFTR modulator program in Phase 1/2 (2026). Not yet in
    Phase 3. Even if Phase 3 initiated in 2027 and succeeds, FDA
    approval would not precede 2030-2031 at the earliest. VRTX has
    7-10 years of uncontested CF dominance from today's analysis date.
    No other company has disclosed a credible competitor program.

JOURNAVX (SUZETRIGINE) — PAIN WITHOUT OPIOIDS
===============================================
Suzetrigine (JOURNAVX) is the first selective NaV1.8 sodium channel
inhibitor — a completely new mechanism for pain treatment. Unlike opioids
(which act via mu-opioid receptors in the brain, causing sedation and
addiction) or NSAIDs (COX inhibitors), suzetrigine blocks the peripheral
pain signal at its source in nociceptive neurons.

  FDA approval:         January 30, 2025 — first-in-class, landmark decision
  Indication:           Moderate-to-severe acute pain in adults
  Mechanism:            Selective NaV1.8 inhibitor; no CNS activity; no addiction
  Commercial status:    Launch underway; hospital formulary wins + surgical use

  ACUTE PAIN market: ~$3.5B annually (US). Dominated by opioids (~$2.4B,
  stigmatized) and IV morphine equivalents in hospital settings. Suzetrigine
  faces formulary friction (new drug; hospital P&T committees slow; payers)
  but has a compelling safety advantage: no respiratory depression, no
  addiction, no constipation. Surgeons are early adopters.

  DIABETIC PERIPHERAL NEUROPATHY (DPN):
    The far larger opportunity. 37M+ diabetics in the US; ~30-50% develop
    DPN (painful, burning, electric-shock nerve pain that current treatments
    fail to adequately control). Current options: gabapentinoids (duloxetine,
    pregabalin) that are only marginally effective and cause sedation.
    FDA Breakthrough Therapy Designation granted for suzetrigine in DPN.
    Phase 3 PIVOTAL trial ongoing. Data expected: 2027.
    If approved: addressable population ~7-10M US patients. Peak sales: $3B+.
    This is the single most important near-term pipeline catalyst for VRTX.

  Canada: NDA under regulatory review (2026). EU filing expected 2026.

POVETACICEPT (POVE) — KIDNEY DISEASE PIPELINE EMERGES
======================================================
Povetacicept is a fusion protein that blocks both BAFF and APRIL — two
cytokines that activate B cells, driving the production of aberrant IgA
antibodies in IgA nephropathy (IgAN).

  Phase 3 RAINIER (IgAN):
    Primary endpoint met: -52% UPCR (urine protein-creatinine ratio)
    reduction at 36 weeks vs +4.3% for placebo. Statistically significant
    and clinically meaningful. BLA filed 27 days after database lock (record
    speed). Regulatory decision expected 2026-2027. IgAN affects ~130,000
    patients in the US; current treatments (SGLT-2 inhibitors, low-dose
    steroids) only slow progression. Pove could be disease-modifying.
    First-year revenue estimate: $300-500M. Peak: $2-3B+.

  IgAN competitive context:
    Sparsentan (Travere, acquired by Chinook/AZ) was the prior leader.
    Iptacopan (Novartis, complement inhibitor) approved 2023.
    Povetacicept's -52% UPCR vs. sparsentan's -35-40% and iptacopan's
    ~38% suggests pove may be best-in-class. Vertex filed first; IgAN
    patient population is large enough for multiple products.

  Additional indications:
    Phase 3 in PMN (membranous nephropathy; ~20,000 US patients)
    Phase 3 in MG (myasthenia gravis; ~70,000 US patients)
    Each adds $1B+ potential if approved.

TYPE 1 DIABETES CELL THERAPY — THE LONG-RANGE MOONSHOT
======================================================
VX-880 (unprotected islet cells) and VX-264 (encapsulated islet cells):
Phase 1/2 studies of functional beta-cell replacement therapy for T1D.

  Early clinical data (VX-880):
    Patients in the trial who received adequate cell dose showed meaningful
    insulin production and some achieved partial or full insulin independence.
    VX-264 uses encapsulation to avoid the need for immunosuppression —
    the key barrier to scaling islet transplantation.

  The opportunity: 40M+ T1D patients globally, each requiring lifelong insulin
  therapy (~$10K-30K/yr). A one-time or semi-durable functional cure could
  command $300,000-500,000 per treatment (precedent: gene therapies). This
  is a $5-10B+ annual revenue opportunity if the technology works at scale.

  Timeline: Phase 3 initiation expected 2027-2028. Commercial approval if
  successful: 2030+. This is 4-5 years of development risk, but the option
  value is significant if Phase 1/2 data continues to strengthen.

CASGEVY — GENE EDITING ESTABLISHING SCIENCE CREDIBILITY
=========================================================
Casgevy (exagamglogene autotemcel) — a CRISPR-based gene editing therapy
co-developed with CRISPR Therapeutics — was approved in December 2023 for
sickle cell disease and transfusion-dependent beta-thalassaemia. It is the
world's FIRST approved CRISPR-based medicine.

  Revenue: $72M combined with JOURNAVX in Q1 2026 (early-stage ramp).
  Pricing: ~$2.2M per treatment in the US.
  Limitation: complex manufacturing (autologous; each treatment unique);
  patient eligibility is narrow (severe SCD/TDT); payer access is slow.
  Strategic value: CASGEVY establishes Vertex as a gene editing platform
  company and validates the CRISPR delivery approach for future indications.

BALANCE SHEET AND CASH FLOW
=============================
  FY2026E non-GAAP EPS:   ~$17.80 (Q1 annualised $17.88; guidance ~$17.80)
  Cash + investments:      ~$11.5B (as of Q1 2026; strong balance sheet)
  Net cash:                ~$10B  (minimal debt; pure cash-generating business)
  FCF margin:              ~40%+ of revenue (~$5B+ annual FCF)
  Buybacks:                active; ~$0.5-1B/yr; reducing share count modestly
  No dividend:             all capital returned via buybacks or invested in R&D
  R&D spending:            $5.65-$5.75B guidance for 2026 — extraordinarily high
                           (~43% of revenue); this is intentional as Vertex
                           invests aggressively to build post-CF franchises.

WHERE RISK/REWARD IMPROVES
============================
  RE-ENTER / ACCUMULATE   : $370-400  (52-wk low zone; ratio_b ~1.0-1.4×; entry was excellent)
  WATCHLIST               : $400-430  (just below current; quality compounder; ratio_b ~1.4-2.0×)
  HOLD current             : $430-475  (fair value; HOLD full positions; ratio_b ~2.0-2.5×)
  TRIM above               : $475-508  (near 52-wk high; approaching AVOID zone; ratio_b ~2.5-3.2×)
  CATALYST ADD             : pove IgAN FDA approval OR suzetrigine DPN Phase 3 positive →
                             re-enter up to $445 on the approval catalyst; adds $2-3B NPV

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("PART 3 — NUMBERS & SIGNALS")
print("=" * 72)
print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │  SIGNAL:  {signal_primary:<12}  │  RATIO B: {ratio_b_fmt:<10}               │
  │  TICKER:  {TICKER:<10}    │  SECTOR:  Healthcare / Biopharma      │
  └──────────────────────────────────────────────────────────────────┘

  ----------------------------------------------------------------------
""")

print(f"  Current price         : ${CURRENT_PRICE:.2f}  (-15% from 52-wk high ${PRICE_52W_HIGH}; +20% from 52-wk low ${PRICE_52W_LOW})")
print(f"  EPP floor             : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above; 20× × ${EPS_TROUGH} stress EPS; 52-wk low ${PRICE_52W_LOW} ÷ $9.00 = 40.3×)")
print(f"  Method B (27× exit)   : ${price_b:.2f}  (+{(price_b/CURRENT_PRICE-1)*100:.1f}%; ratio_b = {ratio_b:.2f}× → HOLD/TRIM)")
print(f"  At 30× exit           : ${CONS_EPS_2YR*30:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*30-CURRENT_PRICE):.2f}× → HOLD/TRIM (historical average multiple)")
print(f"  At 32× exit           : ${CONS_EPS_2YR*32:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*32-CURRENT_PRICE):.2f}× → WATCHLIST (pove IgAN + suzetrigine DPN re-rate)")
print(f"  BEAR scenario         : ${PRICE_BEAR}   (-63%; Abbvie CFTR early approval; all non-CF fails; EPS $9 × 18×; 2030+ extreme)")
print(f"  BASE scenario         : ${PRICE_BASE}   (+11%; CF 8%/yr + pove IgAN approved; suzetrigine DPN positive; FY2027 $20 × 24×)")
print(f"  BULL scenario         : ${PRICE_BULL}   (+32%; suzetrigine DPN approved; pove IgAN+PMN; ALYFTREK dominant; $20 × 28.5×)")
print(f"  XBULL scenario        : ${PRICE_XBULL}   (+66%; T1D cell therapy transformational; suzetrigine DPN $3B+; FY2028-29 $26 × 27.7×)")
print(f"  Forward P/E (FY2026E) : {CURRENT_PRICE/EPS_NOW:.1f}×   (${CURRENT_PRICE} / ${EPS_NOW}; CF monopoly justified premium; non-CF ramp priced in)")
print(f"  Forward P/E (FY2027E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×   (${CURRENT_PRICE} / ${CONS_EPS_2YR}; 27× Method B exit; conservative vs 30-32× historical)")
print(f"  EPS history (non-GAAP): FY22 ${EPS_FY2022} → FY23 ${EPS_FY2023} → FY24 ${EPS_FY2024} → FY25 ${EPS_FY2025} → FY26E ${EPS_NOW}")
print(f"  Q1 2026               : Revenue $2.99B (+8%); non-GAAP EPS $4.47 (beat +$0.14; +13%); CF solid")
print(f"  FY2026 guidance       : Revenue $12.95-$13.1B; non-CF ≥$500M (JOURNAVX + CASGEVY ramp)")
print(f"  CF franchise          : TRIKAFTA $2.35B + ALYFTREK $424M (Q1 2026); upgrade cycle ongoing; patents ~2037")
print(f"  JOURNAVX (suzetrigine): FDA approved Jan 2025; acute pain launched; DPN BTD Phase 3 underway (data 2027)")
print(f"  Povetacicept (pove)   : IgAN Phase 3 RAINIER: -52% proteinuria; BLA filed H1 2026; PMN + MG also Phase 3")
print(f"  CASGEVY               : First CRISPR therapy (SCD + TDT); $2.2M/patient; early commercial ramp")
print(f"  T1D cell therapy      : VX-880/VX-264 Phase 1/2; insulin independence data; Phase 3 ~2027-28")
print(f"  CF competition        : Abbvie CFTR Phase 1/2 only; no competition expected before 2030-2031")
print(f"  No dividend           : $10B+ net cash; all capital reinvested in R&D + buybacks")
print(f"  Market cap            : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  ACCUMULATE zone       : $370-400  (52-wk low zone; ratio_b ~1.0-1.4×; excellent entry)")
print(f"  HOLD zone             : $430-475  (current; fair value; ratio_b 2.0-2.5×)")
print(f"  TRIM above            : $475-508  (approaching 52-wk high; AVOID zone begins)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.40×  |  Idiosyncratic: 90%  |  Macro: 10%

  Driver                                                      Type    Wt  Note
  ─────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  CF monopoly: TRIKAFTA + ALYFTREK; patents 2037; no comp   IDIO  25%  CORE: unassailable for 10+ years
  Pove IgAN: RAINIER -52% proteinuria; BLA filed H1 2026    IDIO  20%  NEAR-TERM: FDA decision 2026-27; $2-3B peak
  JOURNAVX DPN: NaV1.8; BTD; Phase 3 data 2027             IDIO  15%  PIVOT: $3B+ if DPN approved
  CF competition: Abbvie CFTR Phase 1/2 (2030+ earliest)   IDIO  20%  BEAR: 7-10yr tail risk; negligible now
  Valuation: 24.3× forward; -15% from high; limited upside  IDIO  20%  CONSTRAINT: price limits near-term return""")

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
  BEAR  (${PRICE_BEAR}) : Abbvie CFTR modulator achieves unexpected Phase 3 superiority
               data vs ALYFTREK ~2029-2030 AND earns accelerated FDA approval
               by 2031, capturing 20%+ of new CF patients. Simultaneously:
               suzetrigine DPN Phase 3 fails primary endpoint (NaV1.8 mechanism
               does not translate to neuropathic pain in Phase 3); povetacicept
               shows durable benefit weaker than expected in real-world IgAN
               treatment (breakthrough but not dominant). T1D cell therapy
               abandoned due to immune rejection. EPS declines toward $9 by
               2031. Market applies 18× = $162. -63%. Requires multiple
               simultaneous failures over a 5+ year horizon.

  BASE  (${PRICE_BASE}) : CF franchise compounds at 8-10%/yr with ALYFTREK upgrade
               cycle completing 2026-2028. Povetacicept approved in IgAN by
               early 2027 (BLA filed H1 2026; no safety surprises); first-year
               revenue $300-500M. Suzetrigine acute pain ramps to $150M+ in
               2026 and DPN Phase 3 is positive (BTD expedites path). ALYFTREK
               completes the TRIKAFTA switchover with +$200 net price uplift.
               FY2027E $20 × 24× = $480. +11% from current.

  BULL  (${PRICE_BULL}) : Suzetrigine DPN Phase 3 strong positive (2027) — rapid label
               expansion to the ~7M US DPN patients; suzetrigine becomes the
               preferred DPN therapy over gabapentinoids. Pove approved in
               IgAN + PMN (2027-2028), establishing VRTX as a renal immunology
               platform. ALYFTREK achieves 80%+ of CF patients by end-2027.
               Multiple expands to 28.5×. $20 × 28.5× = $570. +32%.

  XBULL (${PRICE_XBULL}) : VX-264 (encapsulated T1D cell therapy) Phase 3 shows >50%
               functional insulin independence at 2 years — a potential
               paradigm shift for 40M T1D patients globally. FDA grants
               Breakthrough Therapy designation and accelerated approval path.
               Suzetrigine DPN achieves $1B+ in Year 2 post-approval. Pove
               achieves 3 approvals (IgAN + PMN + MG) by 2028. CF compounds
               at 8%/yr uncontested through 2031. FY2028-29E ~$26 × 27.7×
               = $720. +66%. Multi-franchise transformation.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-26")
print("=" * 72)
