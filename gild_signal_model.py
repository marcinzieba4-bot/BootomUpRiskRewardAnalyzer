"""
Gilead Sciences, Inc. (NASDAQ: GILD) — BottomUp Risk/Reward Signal Model

SIGNAL:  ▷ HOLD/TRIM
RATIO B: 2.17x  (Method B at 18× FY2027E $9.50 = $171.00; ratio 79.36/36.64 = 2.17×)
DATE:    2026-05-26
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "GILD"
COMPANY = "Gilead Sciences, Inc."
SECTOR  = "Large-Cap Biopharma · HIV (Biktarvy/Lenacapavir) · Oncology (Trodelvy/Yescarta) · Virology (Veklury) · Liver Disease"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  = 134.36   # GILD — Yahoo Finance, 2026-05-25; -15% from 52-wk high; +44% from low
PRICE_52W_LOW  =  93.37   # 52-week low (mid-2025; HIV competition fears + CymaBay dilution concerns)
PRICE_52W_HIGH = 157.29   # 52-week high (Jan 2026; lenacapavir PrEP PURPOSE trial euphoria)
SHARES_M       = 1241.0   # million diluted shares (~$166.6B market cap / $134.36)
DIVIDEND_ANN   =   3.28   # $0.82/quarter × 4 = $3.28/yr (~2.44% yield; 11 consecutive annual increases)

# ── EPS (non-GAAP adjusted, excl. acquired IPR&D charges) ──────────────────────
# GILD FY = calendar year. Non-GAAP EPS excludes: acquired IPR&D charges (large
# one-time costs from M&A: CymaBay $4.3B in 2024; Arcellx + Ouro + Tubulis
# ~$11.5B in 2026), stock-based comp, amortization of intangibles.
# The underlying EPS arc reflects the Veklury (remdesivir) post-COVID normalisation
# and subsequent recovery driven by HIV franchise growth + oncology build-out.
# FY2024 reported non-GAAP was $4.62 (incl. CymaBay IPR&D ~$2.85/share);
# underlying excl. IPR&D was ~$7.47. Similarly, FY2026 GAAP EPS will be negative
# (-$0.65 to -$1.05) due to $11.5B Arcellx/Ouro/Tubulis charges — the $8.65
# guidance is the correct operational metric.
EPS_FY2022 =  7.43    # actual; COVID Veklury still elevated ($3.2B); HIV growing
EPS_FY2023 =  6.72    # actual; Veklury collapsed to ~$1.1B; HIV growth partially offsets
EPS_FY2024 =  7.47    # underlying (reported non-GAAP $4.62 incl. CymaBay IPR&D ~$2.85/sh)
EPS_FY2025 =  7.90    # actual; guidance $7.70-$8.10 midpoint; Biktarvy $12B+; oncology scaling
EPS_NOW    =  8.65    # FY2026E midpoint ($8.45-$8.85 guided); +9.5% YoY; excl. $11.5B IPR&D
                       # Q1 2026: Revenue $7.0B (+4% YoY); non-GAAP EPS ~$1.78 (beat by ~$0.13)
                       # Beat driven by HIV portfolio + Trodelvy growth + Livdelzi momentum
                       # FY2026: Revenue $30.0-$30.4B; three new acquisitions closing H2 2026

# ── EPP Floor ─────────────────────────────────────────────────────────────────
# EPS_TROUGH = full Veklury revenue collapse (→ $0) + HCV decline complete
# (~$650M → $0) + Biktarvy generic threat if patents fail earlier than expected
# + recession. From FY2026E $8.65: severe scenario cuts EPS ~36% to ~$5.50.
# Even at trough, Gilead retains Biktarvy's durable patent protection (key
# patents to 2033-2038), lenacapavir royalties, Trodelvy/Yescarta oncology
# revenue, and a $3.28 annual dividend with 11 consecutive increases.
# A pharma company of this quality does not trade below 10× trough EPS.
# Calibration: 52-wk low $93.37 ÷ $5.50 = 17.0× stress EPS — the market
# bottomed at 17× stress EPS during peak HIV competition and dilution fears.
# EPP at $55 represents the true catastrophic floor — never tested in practice.
EPS_TROUGH =  5.50    # Veklury + HCV gone; Biktarvy competition; recession; ~-36% from FY2026E
EPP_MIN_PE = 10       # HIV pharma floor: durable patents + dividend + free cash flow
EPP        = EPS_TROUGH * EPP_MIN_PE   # $5.50 × 10 = $55.00

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E ~$9.50: Management guided FY2026 $8.65 non-GAAP. For 2027, three
# new acquisitions (Arcellx, Ouro, Tubulis) begin contributing, lenacapavir oral
# combo ramps, and HIV + oncology continue growing. Key drivers:
#   • Lenacapavir twice-yearly injection (PrEP): FDA-approved; PURPOSE-1 and
#     PURPOSE-2 trials showed ZERO infections in ~5,000 women/men at high risk.
#     Potentially the defining public health HIV prevention breakthrough since
#     condoms. Global scale-up (US, sub-Saharan Africa via licensing). First full
#     commercial year ramp in 2026-2027.
#   • Lenacapavir + bictegravir oral daily combo: FDA Priority Review granted.
#     NDA submitted for virologically suppressed patients. First-in-class
#     capsid inhibitor + INSTI daily combo — potential to replace Biktarvy with
#     a more potent once-daily regimen. Commercial launch late 2026/early 2027.
#   • Biktarvy ($12B+ in 2025): growing 5-8%/yr with lenacapavir combo ADDING
#     new patients / expanding indications rather than purely cannibalising.
#   • Trodelvy: ASCENT-04 data (1L TNBC + pembrolizumab) approved; expansion
#     into urothelial cancer and potentially HER2-low breast cancer. $1.5B+ 2025.
#   • Arcellx (GPRC5D CAR-T for myeloma): transformational CAR-T with superior
#     efficacy vs existing therapies. Fully owned. Peak sales $2-3B+ potential.
#   • FY2027E ~$9.50 = $8.65 × ~10% growth (operational + acquisitions accreting).
# Exit P/E: 18× — HIV franchise premium justified by lenacapavir PrEP optionality
# + oncology growth + durable patent moat (Biktarvy to 2033-38). 18× is below
# the 20-22× GILD traded during the Harvoni/Sovaldi HCV supercycle peak.
#   At 18×: $171.00  (+27% from $134.36) — Base target; ratio_b = 2.17×
#   At 20×: $190.00  (+41%) — lenacapavir commercial ramp exceeds expectations
#   At 22×: $209.00  (+56%) — full Arcellx/oncology platform re-rate
CONS_EPS_2YR = 9.50
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
# BEAR:  Lenacapavir oral combo cannibalises Biktarvy (revenue-neutral at best);
#        Arcellx GPRC5D CAR-T shows inferior real-world efficacy vs J&J/BMS
#        competition; Trodelvy stalls in TNBC 2L; Veklury falls to zero faster
#        than expected; all three 2026 acquisitions delayed/dilutive.
#        EPS stabilises near $5.00-5.50; market applies 11× = $55. -59% from
#        current. Matches EPP floor — an extreme scenario requiring simultaneous
#        HIV + oncology disappointment.
# BASE:  Lenacapavir injection PrEP drives 100K+ new US patients by 2027;
#        oral combo adds 200K+ switches from Biktarvy (net ARPU-neutral to
#        positive); Trodelvy ASCENT-04 grows TNBC franchise; Arcellx contributes
#        $0.10-0.15 EPS in first year; HIV $12B+ with stable growth. FY2027E
#        $9.50 × 17× = $162. +21% from current.
# BULL:  Lenacapavir injection becomes global HIV prevention standard; PEPFAR-
#        scale rollout with milestone payments; Arcellx GPRC5D achieves
#        first-line myeloma approval (the largest myeloma indication); Trodelvy
#        + Yescarta drive oncology to 25%+ of revenue. Multiple re-rates to 21×.
#        $9.50 × 21× = $200. +49%.
# XBULL: GILD becomes the first company to demonstrate functional HIV cure
#        (lenacapavir + bNAbs Phase 2 data breakthrough); Arcellx data redefines
#        myeloma treatment; oral lenacapavir combo replaces Biktarvy as global
#        HIV standard-of-care across all major markets. FY2028-29E ~$11.00
#        × 21.8× = $240. +79%.
PRICE_BEAR  =  55
PRICE_BASE  = 162
PRICE_BULL  = 200
PRICE_XBULL = 240

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.40, 0.25, "Lenacapavir PrEP: PURPOSE trials 0 HIV infections; FDA-approved; global rollout"),
    (+0.30, 0.20, "Trodelvy ASCENT-04 TNBC + Yescarta CAR-T; oncology ~15-20% of revenue growing"),
    (-0.30, 0.20, "Three 2026 acquisitions ($11.5B IPR&D): Arcellx + Ouro + Tubulis; execution risk"),
    (-0.25, 0.20, "Lenacapavir oral replaces Biktarvy; cannibalization risk without net revenue gain"),
    (-0.20, 0.15, "Veklury + HCV structural decline: $1-1.5B combined shrinking 10-20%/yr"),
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
  Stress EPS ($5.50) × 10× HIV pharma floor. EPS_TROUGH represents full
  Veklury (~$0) + HCV (~$0) collapse + Biktarvy competitive pressure
  + recession — a ~-36% EPS cut from FY2026E $8.65. Even at trough, GILD
  retains Biktarvy patents (2033-2038), lenacapavir royalties, oncology
  revenue (Trodelvy/Yescarta/Arcellx), and $3.28/yr dividend.
  10× is the floor P/E for a cash-generative HIV pharma with irreplaceable
  treatment franchise and 11 consecutive dividend increases.
  EPP = $55.00.
  Calibration: 52-wk low $93.37 ÷ $5.50 = 17.0× stress EPS — the market
  bottomed at 17× during peak HIV competition fears + CymaBay dilution
  concerns, well above EPP. EPP represents the never-visited catastrophic
  floor, not a target entry point.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E ~$9.50 (Biktarvy + lenacapavir oral combo launch + oncology scale
  + Arcellx early contribution; +~10% from FY2026E $8.65) × 18× exit P/E
  (HIV franchise premium; lenacapavir PrEP optionality; below the 20-22×
  GILD traded at the HCV supercycle peak — conservative) = $171.00.
  Ratio B = ($134.36 − $55.00) / ($171.00 − $134.36) = $79.36 / $36.64 = 2.17×
  → ▷ HOLD/TRIM. The stock is +44% from its $93.37 low and -15% from its
  $157.29 high. At 15.5× FY2026E (non-GAAP), the market is pricing in moderate
  lenacapavir optionality but not a full platform re-rate. Current price fairly
  reflects the HIV franchise quality. HOLD; re-enter below $105 or on a
  lenacapavir oral combo approval + Arcellx pivotal data.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GILEAD: THE LENACAPAVIR MOMENT — AND WHETHER IT'S IN THE PRICE
================================================================

Gilead Sciences is the world's dominant HIV treatment company, generating
~$30B in annual revenue with Biktarvy (bictegravir/FTC/TAF) as the #1
prescribed complete HIV regimen globally ($12B+ in 2025 revenue, ~40% of
total). The company is at a strategic inflection point: lenacapavir, a
first-in-class HIV capsid inhibitor, is transforming both HIV treatment AND
prevention — and the market is debating whether to pay for that optionality
at 15.5× FY2026E or wait for proof of commercialization at scale.

The stock at $134.36 is +44% from its mid-2025 low ($93.37) but -15% from
its January 2026 peak ($157.29). The $93 lows represented maximum pessimism
about HIV competition; the $157 peak represented lenacapavir PrEP euphoria
after PURPOSE-1/2 trial data. Current price is the equilibrium between
"lenacapavir is real but already discounted" and "three acquisitions create
$11.5B in one-time charges that depress GAAP EPS for 2 years."

Q1 2026 — SOLID EXECUTION; ACQUISITIONS DOMINATE THE NARRATIVE
================================================================
  Total revenue:          $7.0B  (+4% YoY; beat consensus)
  HIV revenue:            ~$5.2B  (+7% YoY; Biktarvy $3.1B; lenacapavir PrEP scaling)
  Oncology revenue:       ~$0.9B  (Trodelvy $0.5B+; Yescarta/Tecartus growing)
  Veklury revenue:        ~$0.4B  (-20%+ YoY; COVID normalised; steady decline)
  HCV revenue:            ~$0.4B  (-15% YoY; structural erosion continues)
  Non-GAAP EPS:           ~$1.78  (beat by ~$0.13; +13% YoY; strong operating leverage)
  GAAP EPS:               $1.61   (before 2026 IPR&D charges; positive in Q1)
  FY2026 guidance:        Revenue $30.0-$30.4B; non-GAAP EPS $8.45-$8.85
  FY2026 GAAP EPS guide:  (-$1.05)-(-$0.65)  due to $11.5B IPR&D from 3 acquisitions
  Net debt:               ~$5-8B  (conservative balance sheet; investment grade)

The TIKR headline "Beat Q1 2026 but still down 17%" reflects investor
frustration: strong underlying results, but three new acquisitions within
months of each other create integration risk and GAAP loss confusion.

LENACAPAVIR — THE POTENTIAL HIV PREVENTION BREAKTHROUGH
========================================================
Lenacapavir (LEN) is Gilead's capsid inhibitor — the first new HIV drug
mechanism in decades. It works differently from all existing HIV antivirals,
with a unique intracellular half-life enabling twice-yearly dosing (2 shots
per year). Key datasets:

  PURPOSE-1 (Sub-Saharan Africa, women):
    2,134 women; 5,338 person-years of follow-up.
    LEN arm: 0 (ZERO) HIV infections.
    Cabotegravir arm: 0.21 per 100 person-years.
    Background rate arm: 2.41 per 100 person-years.
    100% efficacy vs. background; superior to cabotegravir (ViiV/GSK).
    FDA approved lenacapavir for PrEP in June 2025.

  PURPOSE-2 (Multi-country, cisgender men, transgender):
    ~3,200 participants across 6 countries.
    LEN arm: 2 infections in ~5,000 person-years = 0.03 per 100 PY.
    Background rate: ~2.4 per 100 PY. Efficacy >99%.
    The data are historic — arguably the most significant HIV prevention
    advance since the introduction of oral PrEP (Truvada in 2012).

  PrEP market context:
    Current oral PrEP (Descovy/Truvada): ~$2.4B market. Adherence is the
    limiting factor — daily dosing fails in real-world settings. Twice-yearly
    injections solve the adherence problem. Gilead estimates the US PrEP-
    eligible population at 1.2M+ people. At $4,000-6,000/yr for LEN injections
    (vs $20K+ for cabotegravir), Gilead has a competitive PrEP pricing strategy.
    Ramp will be slow (new patient acquisition, reimbursement logistics) but
    has a very long runway: 1.2M US potential + 35M globally at high risk.

  Lenacapavir + bictegravir oral daily combo:
    FDA Priority Review granted. NDA submitted. Potential approval late 2026/
    early 2027. A once-daily single-tablet combining bictegravir (INSTI, core
    of Biktarvy) + lenacapavir (capsid inhibitor) — potentially more potent
    and resistance-resilient than Biktarvy alone. When approved, this REPLACES
    Biktarvy's label as the preferred first-line regimen for new virologically
    suppressed patients. The key question: does this cannibalize Biktarvy
    revenue or grow the total HIV treatment market? Management says net-neutral
    to positive: new patients + switches without meaningful price change.

THREE 2026 ACQUISITIONS — THE OVERHANG EXPLAINED
==================================================
Gilead announced THREE acquisitions in the first 5 months of 2026, totalling
~$18B in deal value with ~$11.5B in upfront IPR&D charges to GAAP earnings:

  1. Arcellx ($3.3B, announced 2026):
     GPRC5D-targeting CAR-T (anito-cel, axicabtagene ciloleucel) for
     relapsed/refractory multiple myeloma. GPRC5D is a novel myeloma target
     with strong Phase 2 data showing deep, durable responses. Multiple
     myeloma is a ~$20B global market. Key competition: J&J's teclistamab
     (BCMA BiTE) and BMS's idecabtagene vicleucel (BCMA CAR-T). Arcellx
     uniquely targets GPRC5D, which doesn't lose expression after BCMA
     therapy — making it the perfect second-line therapy after BCMA failure.
     Phase 3 (MAGNITUDE) underway. Revenue potential: $2-3B+ at peak.

  2. Ouro Medicines (HIV prevention, ~$2-3B):
     Novel HIV prevention compound (details proprietary). Focused on
     expanding the prevention pipeline beyond lenacapavir.

  3. Tubulis ($4.5B, announced April 2026):
     ADC (antibody-drug conjugate) platform company. Tubulis has a next-
     generation linker-payload technology that may offer superior therapeutic
     index vs. first-gen ADCs (less off-target toxicity). Adds an ADC
     platform to complement Trodelvy's success in TNBC/urothelial.
     ADC market growing from $4B (2024) to estimated $17B+ by 2030.

The combined ~$11.5B IPR&D charge makes FY2026 GAAP EPS negative (-$0.65
to -$1.05). This is entirely non-cash and non-operational. The non-GAAP
EPS ($8.45-$8.85) is the correct operating metric. However, the rapid
pace of dealmaking (3 acquisitions, ~$18B, in 5 months) raises valid
concerns: management bandwidth, integration complexity, and whether Gilead
is being opportunistic or undisciplined.

HIV FRANCHISE — BIKTARVY'S REMAINING MOAT
==========================================
  Biktarvy (bictegravir 50/FTC 200/TAF 25mg):
    FY2025 revenue: $12.1B+  (~41% of total GILD revenue)
    Market share:   ~55% of new virologically suppressed patients in the US
    Patient tenure: average 7+ years per patient; very high switching costs
    Patent expiry:  bictegravir US composition patent: 2033; method of use: 2038
    Competition:    ViiV GSK (Dovato, Cabenuva); Merck (Islatravir combo)
    Durability:     The patent moat is stronger than any other HIV regimen.
                    A generic challenge would face significant litigation.
    Tailwind:       ~$6B ex-US HIV market growing at 3-5%/yr as access expands.

  Caveat — lenacapavir cannibalisation risk:
    If lenacapavir oral daily combo is approved, patients and physicians may
    prefer the "better" drug. At similar pricing (management guidance), this
    is revenue-neutral. But if pricing pressure from PBMs forces LEN/BIC
    below Biktarvy's net price, the transition creates a short-term revenue
    headwind before the volume expansion compensates.

ONCOLOGY — BUILDING THE SECOND FRANCHISE
==========================================
  Trodelvy (sacituzumab govitecan):
    ADC for triple-negative breast cancer (TNBC) + urothelial cancer.
    FY2025: $1.5B revenue; growing 20-25%/yr.
    ASCENT-04 (1L TNBC + pembrolizumab): FDA approval for first-line
    TNBC treatment — significantly expands the addressable patient population.
    Urothelial: approved 2L; Phase 3 in 1L ongoing (TROPHY-U-02).
    Potential: $3B+ peak in breast cancer alone; $4B+ with bladder/other.

  Yescarta (axicabtagene ciloleucel) + Tecartus (brexucabtagene autoleucel):
    CAR-T for large B-cell lymphoma + MCL (mantle cell lymphoma).
    FY2025: $1.5B+ combined; growing 10-15%/yr.
    Competition: BMS Breyanzi (lisocabtagene maraleucel) in LBCL.
    Differentiator: Yescarta's first-in-class 2L and now frontline data
    (ZUMA-7) maintain a strong position in relapsed/refractory LBCL.

  Arcellx (Anito-cel for myeloma):
    If Phase 3 MAGNITUDE succeeds, this becomes Gilead's third major
    CAR-T product and potentially the most commercially significant — myeloma
    is 3-5× larger than lymphoma as a CAR-T target. GPRC5D advantage over
    BCMA: usable after BCMA failure (2nd or 3rd line). Approval: 2027-2028E.

BALANCE SHEET AND CASH FLOW
=============================
  FY2026E non-GAAP EPS:   $8.65 (guided midpoint; excl. $11.5B IPR&D)
  FY2026E GAAP EPS:        (-$0.65)-(-$1.05) (incl. $11.5B IPR&D; one-time non-cash)
  Dividend:                $3.28/yr ($0.82/quarter; 11 consecutive annual increases)
  FCF generation:          ~$8-10B/yr (strong; ~28-33% FCF margin)
  Net debt:                ~$5-8B (conservative; investment grade; BBB stable)
  Capital allocation:      Dividend first; M&A (3 deals in 2026); limited buybacks
  Balance sheet headroom:  ~$15-20B capacity for additional deals before credit stress

WHERE RISK/REWARD IMPROVES
============================
  ACCUMULATE              : $105-115  (lenacapavir commercial ramp; ratio_b ~1.5-1.8×)
  WATCHLIST               : $115-130  (recovery confirmed; lenacapavir data solid; ratio_b ~1.8-2.0×)
  HOLD current             : $130-145  (fairly priced; acquisitions not yet proven; ratio_b ~2.0-2.3×)
  TRIM above               : $145-171  (approaching Method B; trim without lenacapavir oral approval)
  ADD/BUY on catalyst      : lenacapavir oral BIC NDA approval (late 2026/early 2027) →
                             re-enter up to $140 on the approval catalyst

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

print(f"  Current price         : ${CURRENT_PRICE:.2f}  (+44% from 52-wk low ${PRICE_52W_LOW}; -15% from 52-wk high ${PRICE_52W_HIGH})")
print(f"  EPP floor             : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above; 10× × ${EPS_TROUGH} stress EPS; 52-wk low ${PRICE_52W_LOW} ÷ $5.50 = 17.0×)")
print(f"  Method B (18× exit)   : ${price_b:.2f}  (+{(price_b/CURRENT_PRICE-1)*100:.1f}%; ratio_b = {ratio_b:.2f}× → HOLD/TRIM)")
print(f"  At 20× exit           : ${CONS_EPS_2YR*20:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*20-CURRENT_PRICE):.2f}× → HOLD/TRIM (lenacapavir oral launch ramp)")
print(f"  At 22× exit           : ${CONS_EPS_2YR*22:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*22-CURRENT_PRICE):.2f}× → HOLD/TRIM (full oncology platform re-rate)")
print(f"  BEAR scenario         : ${PRICE_BEAR}    (-59%; LEN oral cannibalises Biktarvy; acquisitions dilutive; EPS trough $5.00 × 11×)")
print(f"  BASE scenario         : ${PRICE_BASE}   (+21%; LEN oral approved; Biktarvy stable; oncology growing; FY2027 $9.50 × 17×)")
print(f"  BULL scenario         : ${PRICE_BULL}   (+49%; LEN PrEP global rollout; Arcellx myeloma approval; Trodelvy 1L TNBC dominant)")
print(f"  XBULL scenario        : ${PRICE_XBULL}   (+79%; LEN cure trial breakthrough; oral combo standard-of-care; Arcellx 1L myeloma)")
print(f"  Forward P/E (FY2026E) : {CURRENT_PRICE/EPS_NOW:.1f}×   (${CURRENT_PRICE} / ${EPS_NOW}; non-GAAP excl. $11.5B IPR&D; fair for quality HIV pharma)")
print(f"  Forward P/E (FY2027E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×   (${CURRENT_PRICE} / ${CONS_EPS_2YR}; 18× Method B exit; conservative for LEN platform)")
print(f"  EPS history (non-GAAP): FY22 ${EPS_FY2022} → FY23 ${EPS_FY2023} → FY24 ${EPS_FY2024} (underlying) → FY25 ${EPS_FY2025} → FY26E ${EPS_NOW}")
print(f"  Q1 2026               : Revenue $7.0B (+4%); non-GAAP EPS ~$1.78 (beat; +13%); HIV +7%, oncology growing")
print(f"  FY2026 guidance       : Revenue $30.0-$30.4B; non-GAAP EPS $8.45-$8.85; GAAP EPS (~-$0.85) incl. IPR&D")
print(f"  HIV franchise         : Biktarvy $12B+ (+5-8%/yr); LEN PrEP injection scaling; oral LEN/BIC NDA priority review")
print(f"  Lenacapavir PrEP      : PURPOSE-1 0/2,134 infections; PURPOSE-2 >99% efficacy; 1.2M+ US eligible population")
print(f"  Oncology              : Trodelvy $1.5B+ TNBC+urothelial; Yescarta/Tecartus $1.5B+ CAR-T; Arcellx GPRC5D myeloma")
print(f"  2026 acquisitions     : Arcellx $3.3B (myeloma CAR-T); Ouro Medicines (HIV prev.); Tubulis $4.5B (ADC platform)")
print(f"  Declining revenue     : Veklury ~$400M (-20%/yr); HCV ~$400M (-15%/yr); structural headwinds")
print(f"  Dividend              : $3.28/yr ({DIVIDEND_ANN/CURRENT_PRICE*100:.1f}% yield; 11 consecutive annual increases)")
print(f"  Market cap            : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  HOLD zone             : $130-145  (fairly priced; pipeline optionality reasonable; ratio_b 2.0-2.3×)")
print(f"  ACCUMULATE            : $105-115  (lenacapavir commercial traction; ratio_b ~1.5-1.8×)")
print(f"  TRIM above            : $145-171  (approaching Method B; reduce without oral LEN/BIC approval)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.45×  |  Idiosyncratic: 85%  |  Macro: 15%

  Driver                                                      Type    Wt  Note
  ─────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  Lenacapavir PrEP: PURPOSE data; 0 infections; FDA-approved IDIO  25%  PRIMARY BULL: HIV prevention paradigm shift
  Trodelvy ASCENT-04 TNBC 1L + Yescarta CAR-T scaling        IDIO  20%  GROWTH: oncology ~15-20% of revenue
  Three 2026 M&A: $11.5B IPR&D; Arcellx + Ouro + Tubulis    IDIO  20%  RISK: execution + dilution overhang
  LEN oral BIC combo: cannibalizes Biktarvy or grows market?  IDIO  20%  BINARY: net-neutral vs. net-negative
  Macro/IRA/pricing: US drug pricing reform risk              MACRO 15%  MODERATE: HIV pricing politically sensitive""")

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
  BEAR  (${PRICE_BEAR}) : Lenacapavir oral daily combo gains FDA approval but PBMs
               force net pricing below Biktarvy (revenue cannibalization without
               volume offset). Arcellx GPRC5D Phase 3 misses primary endpoint
               (inferior to BCMA bispecific competition from J&J/BMS). Tubulis
               ADC platform fails to produce clinical-stage compounds. Veklury
               and HCV revenue collapse faster than modelled. EPS troughs ~$5.00;
               market applies 11× = $55. -59% from current. Matches EPP floor.

  BASE  (${PRICE_BASE}) : Lenacapavir oral BIC combo approved late 2026/early 2027;
               100K+ new HIV patients reach lenacapavir-based regimens by 2027;
               Biktarvy transitions smoothly (net-neutral pricing); Trodelvy 1L
               TNBC drives oncology to $2B+ revenue; Arcellx Phase 3 endpoints
               met; Veklury/HCV offset by HIV growth. FY2027E $9.50 × 17× = $162.
               +21% from current. Modest re-rate on execution confirmation.

  BULL  (${PRICE_BULL}) : Lenacapavir injection PrEP achieves 300K+ US patients by end
               2027; PEPFAR global rollout adds milestone payments; Arcellx
               achieves 2nd-line myeloma approval (FDA standard path); Trodelvy
               gains in urothelial cancer 1L; multiple expands to 21× on HIV
               franchise scarcity premium + growth portfolio. $9.50 × 21× = $200.
               +49% from current.

  XBULL (${PRICE_XBULL}) : Lenacapavir + broadly neutralizing antibodies (bNAbs) Phase 2
               data shows functional HIV cure potential (viral suppression off
               ART in 50%+ of participants) — breakthrough therapy designation.
               Arcellx anito-cel gains first-line myeloma approval (MAGNITUDE-1L
               trial positive). Oral lenacapavir combo becomes global HIV standard
               of care. Tubulis ADC generates Phase 2 breakthrough data. GILD
               re-rates to 22×. FY2028-29E ~$11.00 × 21.8× = $240. +79%.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-26")
print("=" * 72)
