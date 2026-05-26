"""
Elevance Health, Inc. (NYSE: ELV) — BottomUp Risk/Reward Signal Model

SIGNAL:  ▷ HOLD/TRIM
RATIO B: 2.15x  (Method B at 17× FY2027E $30.00 = $510.00; ratio 252.52/117.48 = 2.15×)
DATE:    2026-05-26
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "ELV"
COMPANY = "Elevance Health, Inc."
SECTOR  = "Managed Care · Commercial Insurance · Medicaid (Anthem) · Medicare Advantage · Carelon Health Services"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  = 392.52   # ELV — Yahoo Finance, 2026-05-25; +45% from 52-wk low; -14% from high
PRICE_52W_LOW  = 271.00   # 52-week low (Mar 2026; CMS sanctions notice + Medicaid trough fears)
PRICE_52W_HIGH = 458.75   # 52-week high (mid-2025; before severity of MA/Medicaid crisis emerged)
SHARES_M       = 218.0    # million diluted shares (~$85.6B market cap / $392.52)
DIVIDEND_ANN   =   6.88   # $1.72/quarter × 4 = $6.88/yr (~1.75% yield; consistent growth history)

# ── EPS (non-GAAP adjusted operating) ─────────────────────────────────────────
# ELV FY = calendar year. Adjusted EPS excludes acquired IPR&D, amortization
# of intangibles, and certain restructuring costs. The EPS arc shows a peak
# cycle from 2022-2024, then a severe 2025 trough driven by simultaneous
# Medicaid rate inadequacy (states not repricing fast enough vs medical cost
# inflation) and Medicare Advantage (MA) MLR deterioration as post-COVID
# utilization normalized higher than CMS rate assumptions. FY2026-2027 is
# management's guided recovery as Medicaid rates re-rate and MA stars/bidding
# improves.
EPS_FY2022 = 28.68    # est; strong MCO year; COVID backlog resolved; Medicaid redeterminations starting
EPS_FY2023 = 32.72    # est; peak; Medicaid issues beginning but not yet severe; commercial strong
EPS_FY2024 = 28.83    # est; first significant miss vs guidance; Medicaid margins compressing sharply
EPS_FY2025 = 20.70    # est; trough year; MA + Medicaid simultaneous crisis; stock -32% in 2025
EPS_NOW    = 26.75    # FY2026E (guided minimum ≥$26.75; raised from $25.50 after Q1 2026 beat)
                       # Q1 2026: Revenue $50.2B (+2.6%); adj EPS $12.58 (strong Q1 recovery vs prior)
                       # MLR Q1 2026: 86.8%; FY2026 target MLR: 90.2% (Medicaid still dilutive)
                       # $935M accrual for CMS risk adjustment data validation matter (GAAP impact)

# ── EPP Floor ─────────────────────────────────────────────────────────────────
# EPS_TROUGH = extreme scenario: CMS permanently suspends MA new enrollment;
# Medicaid rates remain inadequate for 3+ years; Commercial faces recession-
# driven membership losses; Carelon margin investment continues. From FY2026E
# $26.75: a ~-48% cut to ~$14.00. At trough, ELV still has $200B+ in annual
# revenue (~50% from stable Commercial segment), $5.5B+ in operating cash
# flow guidance for 2026, and a resilient diversified membership base.
# MCOs in genuine distress (ACA marketplaces early 2010s, HMO crisis 1990s)
# have traded as low as 6-8× earnings. 10× represents a quality floor for
# the largest not-for-profit-converted managed care company.
# EPP = $140.00.
# Calibration: 52-wk low $271.00 ÷ $14.00 = 19.4× stress EPS — the market
# bottomed at ~19× stress EPS during the CMS sanctions + Medicaid trough panic.
# This is well above EPP ($140), consistent with an MCO facing a cyclical
# earnings reset, not a structural franchise impairment.
EPS_TROUGH = 14.00    # CMS MA suspension + chronic Medicaid rate inadequacy + recession; -48% from FY2026E
EPP_MIN_PE = 10       # Quality managed care floor; $200B revenue + $5.5B OCF; not below sector floor
EPP        = EPS_TROUGH * EPP_MIN_PE   # $14.00 × 10 = $140.00

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E ~$30.00: Management guided "at least 12% adjusted EPS growth" off a
# $25.75 base = ≥$28.84. Using $30.00 (slightly above floor) assumes:
#   • Medicaid: state rate re-rates of 3-5% in 2026-2027 as CMS/FMAP funding
#     stabilises; Medicaid margins recover from -1.75% trough toward break-even
#     and then to long-term target (~2% by 2027). All 26+ state contracts re-priced.
#   • Medicare Advantage: CMS sanctions resolved H2 2026 (risk data submission
#     compliance restored); new enrollment resumes; MA stars rating improves with
#     quality investments. High-teens % MA membership loss in 2026 is the floor;
#     membership rebuild begins 2027 as ELV re-enters the market competitively.
#   • Commercial: stable ~$185/member/month premium yields; employer market
#     resilient through mild recession; ASO (self-funded) growing.
#   • Carelon: health services platform (behavioral health, pharmacy, analytics,
#     risk-based care management) growing toward $30B+ in services revenue
#     with expanding margins as scale improves. Carelon operating gain $1.1B Q1.
#   • $30.00 FY2027E = ~$5.9B adj net income / 218M shares; requires ~$3.50/qtr
#     average run-rate — achievable if Medicaid trough bottoms in H2 2026.
# Exit P/E: 17× — Elevance typically trades 14-18× forward earnings. UNH
# commands 18-22× given superior execution history. ELV at 17× reflects a
# partially-recovered company where Medicaid has passed trough but MA is still
# rebuilding. Below ELV's 2022-2023 peak multiple of 18-20×; conservative.
#   At 17×: $510.00  (+30% from $392.52) — conservative re-rate; ratio_b = 2.15×
#   At 18×: $540.00  (+38%) — full Medicaid recovery + MA stabilisation
#   At 20×: $600.00  (+53%) — Carelon-driven re-rate to UNH-parity multiple
CONS_EPS_2YR = 30.00
CONS_EXIT_PE = 17

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
# BEAR:  CMS formalises MA new enrollment suspension for 12-24 months; Medicaid
#        rate re-rates delayed to 2028 as states face budget shortfalls (post-
#        FMAP cliff); commercial recession drives layoffs and membership attrition;
#        Carelon margin investments continue without revenue scale. EPS stays near
#        $14-16; market applies 10× = $140. -64% from current.
# BASE:  Medicaid rates re-rated 3-5% in 2026-2027 — ELV exiting trough by H2
#        2026; MA sanctions resolved, new enrollment resumes 2027; Commercial
#        stable; Carelon approaching $30B revenue with improving margins. FY2027E
#        $30 × 17× = $510. +30% from current.
# BULL:  Medicaid normalised (margins back to +1% by 2027); MA re-enrollment
#        drives 10%+ membership growth 2027-2028; Carelon health services
#        competes directly with UnitedHealth Optum in behavioural + pharmacy;
#        multiple re-rates to 18.5× as franchise credibility restored. $32 ×
#        18.5× = $592. +51%.
# XBULL: ELV becomes the integrated care company for 2030: Carelon + commercial
#        + government all compounding; MA grows back to 2024 levels + new markets;
#        Medicaid rate reform eliminates chronic inadequacy; EPS $35 × 20× =
#        $700. +78%. Requires multi-year political + operational execution.
PRICE_BEAR  = 140
PRICE_BASE  = 510
PRICE_BULL  = 592
PRICE_XBULL = 700

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.30, 0.20, "Carelon: health services platform ~$30B revenue; behavioral + pharmacy + analytics"),
    (+0.25, 0.20, "Medicaid trough: state re-rates 2026-2027; Elevance guiding to trough in 2026"),
    (-0.40, 0.25, "CMS sanctions: MA new enrollment threat; high-teens % MA member loss guided 2026"),
    (-0.35, 0.20, "Medicaid MLR at -1.75% trough; FY2026 target MLR 90.2% vs 85-86% normal"),
    (-0.20, 0.15, "$935M CMS RADV accrual + GAAP EPS gap ($8.00 GAAP vs $12.58 adj in Q1)"),
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
  Stress EPS ($14.00) × 10× managed care floor. EPS_TROUGH represents
  simultaneous CMS MA enrollment suspension + multi-year Medicaid rate
  inadequacy + recession-driven Commercial attrition — a ~-48% EPS cut
  from FY2026E $26.75. Even at trough, ELV retains $200B+ in revenue,
  26+ state Medicaid contracts, and the Carelon health services platform
  generating $1.1B+/quarter in operating gain.
  EPP = $140.00.
  Calibration: 52-wk low $271.00 ÷ $14.00 = 19.4× stress EPS — the market
  bottomed at ~19× stress EPS during the CMS sanctions + Medicaid trough
  panic. Well above EPP, confirming this is a cyclical earnings reset, not
  a franchise impairment. The stock has since recovered +45% from $271 to
  $392 as investors price in the 2027 earnings recovery.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E ~$30.00 (management guided ≥12% EPS growth off $25.75 base =
  ≥$28.84; using $30 assumes Medicaid rate re-rates complete and MA
  re-enrollment begins) × 17× exit P/E (conservative; ELV historically
  14-20×; 17× assumes partial franchise credibility restoration but not
  full parity with UNH premium) = $510.00.
  Ratio B = ($392.52 − $140.00) / ($510.00 − $392.52) = $252.52 / $117.48 = 2.15×
  → ▷ HOLD/TRIM. The stock is +45% from its $271 low — the entry was the
  $271-310 range (ratio_b ~0.9-1.3×). At $392, the risk/reward has
  normalized. There is meaningful upside to Method B (+30%) but it requires
  executing the Medicaid trough exit AND MA recovery AND Carelon scale
  simultaneously. Compelling only for long-term holders with high conviction.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ELEVANCE: NAVIGATING THE SIMULTANEOUS MEDICAID + MEDICARE CRISIS
================================================================

Elevance Health (formerly Anthem) is the second-largest US health insurer,
with ~40M members across Commercial, Medicaid, and Medicare Advantage
segments, plus Carelon — a growing health services platform comparable to
UnitedHealth's Optum. FY2026 revenue: ~$200B (annualised from Q1 $50.2B).

The stock fell ~32% in 2025 and hit a low of $271 in early 2026 — a $120B
market cap implosion for a company generating $5.5B+ in annual operating
cash flow. The cause: a simultaneously-occurring cost crisis across two
government-funded segments that pushed EPS from $32.72 (FY2023 peak) to
an estimated $20.70 (FY2025 trough). By Q1 2026, adj EPS recovered to
$12.58 (the strongest Q1 in several years) and guidance was raised to
≥$26.75 for the full year.

This is a cyclical recovery story. The fundamental question is whether
the $30 FY2027E EPS and 17× exit P/E are achievable — and whether the
market will actually pay 17× for ELV once the headwinds pass.

Q1 2026 — RECOVERY CONFIRMED; GUIDANCE RAISED
===============================================
  Total revenue:          $50.2B  (+2.6% YoY; above the $49.5B operating revenue)
  Adj diluted EPS:        $12.58  (significant YoY improvement; raised FY guidance)
  GAAP diluted EPS:       $8.00   (includes $935M CMS RADV accrual = ~$4.30/share impact)
  MLR (Q1 2026):          86.8%   (below the 90.2% FY2026 target; Q1 seasonally favourable)
  MLR (FY2026 target):    90.2%   (Medicaid still dilutive; targeting trough in 2026)
  Carelon operating gain: $1.1B   (-3.8% YoY; lower health plan membership + services investment)
  FY2026 adj EPS guide:   ≥$26.75 (raised from ≥$25.50 after Q1 beat)
  FY2026 OCF guide:       ≥$5.5B  (includes potential CMS cash payments)
  FY2027 adj EPS guide:   ≥$28.84 (management guided ≥12% off $25.75 baseline)

The Q1 recovery was meaningful. An $12.58 adj EPS in Q1 alone suggests
the annual run-rate has stabilised above the FY2026 guide. The raise to
≥$26.75 (from ≥$25.50) was incremental but the direction of travel is
clearly upward after the 2025 trough.

THE MEDICAID CRISIS — THREE YEARS IN THE MAKING
================================================
US Medicaid is a federal-state partnership where states determine
reimbursement rates (with federal FMAP matching). The problem:

  The acuity-rate mismatch:
    After COVID, Medicaid "continuous enrollment" expanded the program by
    ~20M members (federal emergency provision). When redeterminations resumed
    in 2023, healthier members left (voluntary disenrollment). Sicker, higher-
    cost members remained. But states had set 2022-2023 premium rates based
    on the AVERAGE acuity of the expanded population — not the higher-acuity
    residual. This created a structural rate inadequacy.

  Elevance's exposure:
    ~26+ state Medicaid contracts (~10M Medicaid members). In 2025, Medicaid
    margins deteriorated to a guided -1.75% trough (effectively losing money
    per member per month on Medicaid). This is the worst MCO Medicaid margin
    performance in modern history.

  The fix (rate re-rates):
    States must file and receive CMS approval for rate increases. Most large
    states (CA, TX, FL, NY) have 12-18 month rate-setting cycles. ELV
    management guided that Medicaid would reach its TROUGH in 2026 and
    begin recovering in 2027 as re-rates catch up with acuity. This is the
    BASE scenario assumption — states have both fiscal and political incentive
    to keep Medicaid managed care viable (the alternative is directly managing
    care, which costs more).

  ACA marketplace:
    Elevance cited a "shift to bronze tier" in ACA plans — lower-premium
    plans attract sicker members who are price-sensitive but have high
    utilisation needs. MLR on bronze plans is elevated. Management has been
    reducing ACA market exposure in counties where the economics are unattractive.

THE CMS SANCTIONS AND MEDICARE ADVANTAGE CRISIS
=================================================
Medicare Advantage (MA) is where Elevance earns the highest per-member
margins (~$60-80/member/month vs ~$15-20 for Medicaid). In 2026:

  CMS sanctions notice (February 27, 2026):
    CMS threatened to suspend new Medicare Advantage enrollment for ELV
    starting March 31 over alleged non-compliance in submitting risk-adjustment
    data (RADV = Risk Adjustment Data Validation). Elevance accrued $935M
    to cover potential exposure. The sanctions are a risk-adjustment audit
    dispute — CMS alleges ELV overcoded diagnostic codes to inflate risk
    scores and receive higher premiums. This is an industry-wide issue
    (UNH, Humana, CVS all face similar scrutiny) but ELV was targeted first.

  Impact on 2026:
    ELV guided "high-teens percentage decline" in MA members in 2026. At
    roughly 2M MA members at peak, that's ~300-400K+ fewer members.
    At ~$1,200 avg annual profit contribution per MA member, this is ~$360-
    480M in lost annual operating gain — roughly $1.60-2.20/share headwind.

  The resolution path:
    ELV and CMS are in active negotiations. The industry consensus is that
    ELV will ultimately reach a settlement on the RADV matter (similar to
    how UNH settled its MA audit in 2024). Sanctions are a warning shot,
    not a permanent exclusion. Management guidance implies suspension is NOT
    formalised (≥$26.75 adj EPS assumes ongoing MA operations, just with
    fewer members).

CARELON — THE OPTUM ANALOGUE
==============================
Carelon is Elevance's health services division, comprising:
  • Carelon Behavioral Health: mental health + substance abuse management
  • Carelon Pharmacy: PBM services (formerly IngenioRx)
  • Carelon Digital Platforms: Sydney Health app + care navigation
  • Carelon Risk-Based Solutions: value-based care + analytics

Carelon operating gain in Q1 2026: $1.1B (-3.8% YoY). The decline reflects
lower health plan membership (fewer internal customers) and continued
investment in expanding risk-based capabilities. As a standalone business,
Carelon resembles early-stage Optum at UNH — a diversified health services
platform that will eventually command a premium multiple if it achieves
Optum-level scale and margin.

Key difference from Optum: Carelon is primarily internal to ELV's health
plans, whereas Optum derives ~30% of revenue from external clients. Carelon's
growth trajectory requires either: (a) growing the external services business,
or (b) winning back Medicaid and MA membership to expand the internal market.

BALANCE SHEET AND DIVIDENDS
=============================
  FY2026E adj EPS:      ≥$26.75 (guided minimum; Q1 beat implies upside)
  FY2026E GAAP EPS:     ≥$19.85 (includes $935M CMS RADV accrual ~$4.28/share)
  Operating cash flow:   ≥$5.5B (guided; includes potential CMS cash payments)
  Dividend:             $6.88/yr ($1.72/quarter; ~1.75% yield; consistent growth)
  Share repurchases:     $1.1B in Q1 2026 (3.7M shares at ~$297; ~$4-5B/yr pace)
  Debt-to-equity:        moderate; investment grade (BBB+ / Baa2)
  Net leverage:          ~1.5× EBITDA (manageable; well below distress threshold)

COMPARATIVE SECTOR CONTEXT (MCO PEER OVERVIEW)
===============================================
  UNH (UnitedHealth Group): premium MCO at 18-22× forward; Optum drives
    50%+ of operating earnings; higher-quality execution history.
  ELV (Elevance):  recovery story at 14-15× FY2026E; Carelon lags Optum;
    Medicaid/MA headwinds more severe than UNH; upside dependent on trough exit.
  CVS (Aetna):    struggling with Aetna MA losses; pharmacy margin compression;
    highly leveraged from Oak Street/Signify acquisitions.
  CI (Cigna):     commercial + Evernorth (PBM) focused; minimal MA exposure;
    cleaner earnings profile than ELV but smaller government segment.

WHERE RISK/REWARD IMPROVES
============================
  ACCUMULATE / BUY      : $310-345  (52-wk low zone; ratio_b ~1.3-1.8×; optimal entry)
  WATCHLIST             : $345-390  (below current; Medicaid trajectory visible; ratio_b ~1.8-2.1×)
  HOLD current           : $390-430  (recovery priced in; ratio_b 2.1-2.4×; hold positions)
  TRIM above             : $430-510  (approaching Method B; trim as MA/Medicaid optimism peaks)
  KEY CATALYST           : Medicaid rate re-rate confirmations (state filings 2026-2027) +
                           CMS RADV settlement announcement → re-enter up to $410

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("PART 3 — NUMBERS & SIGNALS")
print("=" * 72)
print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │  SIGNAL:  {signal_primary:<12}  │  RATIO B: {ratio_b_fmt:<10}               │
  │  TICKER:  {TICKER:<10}    │  SECTOR:  Healthcare / Managed Care   │
  └──────────────────────────────────────────────────────────────────┘

  ----------------------------------------------------------------------
""")

print(f"  Current price         : ${CURRENT_PRICE:.2f}  (+45% from 52-wk low ${PRICE_52W_LOW}; -14% from 52-wk high ${PRICE_52W_HIGH})")
print(f"  EPP floor             : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above; 10× × ${EPS_TROUGH} stress EPS; 52-wk low ${PRICE_52W_LOW} ÷ $14 = 19.4×)")
print(f"  Method B (17× exit)   : ${price_b:.2f}  (+{(price_b/CURRENT_PRICE-1)*100:.1f}%; ratio_b = {ratio_b:.2f}× → HOLD/TRIM)")
print(f"  At 18× exit           : ${CONS_EPS_2YR*18:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*18-CURRENT_PRICE):.2f}× → HOLD/TRIM (Medicaid trough confirmed)")
print(f"  At 20× exit           : ${CONS_EPS_2YR*20:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*20-CURRENT_PRICE):.2f}× → WATCHLIST (Carelon re-rate to Optum parity)")
print(f"  BEAR scenario         : ${PRICE_BEAR}   (-64%; CMS formalises MA suspension; Medicaid rates stuck; EPS $14 × 10×)")
print(f"  BASE scenario         : ${PRICE_BASE}   (+30%; Medicaid trough exits 2026; MA re-enrollment 2027; Carelon grows; $30 × 17×)")
print(f"  BULL scenario         : ${PRICE_BULL}   (+51%; Medicaid +1% margin; MA stars improve; Carelon competes externally; $32 × 18.5×)")
print(f"  XBULL scenario        : ${PRICE_XBULL}   (+78%; integrated care platform; Medicaid reform; MA rebuilt; $35 × 20×)")
print(f"  Forward P/E (FY2026E) : {CURRENT_PRICE/EPS_NOW:.1f}×   (${CURRENT_PRICE} / ${EPS_NOW}; historically cheap for MCO; Medicaid/MA discount)")
print(f"  Forward P/E (FY2027E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×   (${CURRENT_PRICE} / ${CONS_EPS_2YR}; 17× Method B exit; below sector average at peak)")
print(f"  EPS history (adj):      FY22 ${EPS_FY2022} → FY23 ${EPS_FY2023} (peak) → FY24 ${EPS_FY2024} → FY25 ${EPS_FY2025} (trough) → FY26E ${EPS_NOW}")
print(f"  Q1 2026               : Revenue $50.2B (+2.6%); adj EPS $12.58 (strong recovery); GAAP $8.00 (-$935M RADV)")
print(f"  FY2026 guidance       : Adj EPS ≥$26.75 (raised); OCF ≥$5.5B; MLR target 90.2% (Medicaid still dilutive)")
print(f"  FY2027 guidance       : ≥12% adj EPS growth off $25.75 base = ≥$28.84")
print(f"  Medicaid (26+ states) : ~10M members; -1.75% margin trough; rate re-rates 2026-2027 are THE key macro driver")
print(f"  Medicare Advantage    : CMS sanctions (RADV data validation); high-teens % member loss 2026; recovery 2027+")
print(f"  Commercial            : stable; employer market; ASO (self-funded) growing; ACA exposure being managed down")
print(f"  Carelon               : health services ($1.1B Q1 gain); behavioral + pharmacy + analytics platform; Optum-like aspiration")
print(f"  CMS RADV matter       : $935M accrual; risk adjustment data validation audit; settlement expected")
print(f"  Dividend              : ${DIVIDEND_ANN}/yr ({DIVIDEND_ANN/CURRENT_PRICE*100:.1f}% yield; $1.72/quarter; consistent growth)")
print(f"  Buybacks              : $1.1B Q1 2026 (3.7M shares); active capital return program")
print(f"  Market cap            : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  ACCUMULATE zone       : $310-345  (52-wk low zone; ratio_b ~1.3-1.8×; optimal entry was here)")
print(f"  HOLD zone             : $390-430  (current; recovery priced in; ratio_b 2.1-2.4×)")
print(f"  TRIM above            : $430-510  (approaching Method B; reduce as optimism peaks)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.60×  |  Idiosyncratic: 70%  |  Macro: 30%

  Driver                                                      Type    Wt  Note
  ─────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  Medicaid rate re-rates: 26+ states; trough guided 2026     MACRO 25%  PRIMARY RECOVERY: politics + CMS timing
  CMS RADV sanctions: MA enrollment threat; $935M accrual    IDIO  25%  PRIMARY RISK: regulatory overhang
  Carelon platform: behavioral + pharmacy + analytics scale  IDIO  20%  GROWTH: Optum-like aspiration
  Commercial stability: employer market; ASO growth          IDIO  15%  ANCHOR: 50%+ of operating gain
  ACA/healthcare reform: IRA drug pricing; Medicaid FMAP     MACRO 15%  MODERATE: political tail risk""")

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
  BEAR  (${PRICE_BEAR}) : CMS formalises Medicare Advantage new enrollment suspension
               for ELV through 2026-2027 (12-24 months); Medicaid rate re-rates
               fail as states face post-FMAP-cliff budget shortfalls (federal
               Medicaid matching reduced in 2026 budget reconciliation); commercial
               recession drives layoffs and employer-sponsored insurance attrition.
               Carelon margin investment continues without revenue scale. EPS
               stabilises near $14-16; market applies 10× = $140. -64% from
               current. Requires persistent multi-year regulatory AND fiscal AND
               macro headwinds simultaneously.

  BASE  (${PRICE_BASE}) : Medicaid rates re-rated 3-5% across 15+ major state contracts
               in H2 2026 and H1 2027; Medicaid margins recover from -1.75%
               to break-even by Q4 2026 and positive in 2027. CMS RADV matter
               settled H2 2026 (~$1-1.5B total; manageable). MA sanctions not
               formalised; new enrollment resumes with 2027 plan year. Carelon
               gains external services clients. Commercial stable. FY2027E
               $30 × 17× = $510. +30% from current.

  BULL  (${PRICE_BULL}) : Medicaid margins fully normalised at +1-2% by mid-2027
               (faster than modelled); MA sanctions resolved with minimal
               settlement and CMS concedes RADV methodology was flawed;
               MA re-enrollment drives 8-10% membership growth in 2027.
               Carelon wins 3+ external health system clients (Optum model).
               Multiple re-rates to 18.5× as franchise credibility restored.
               $32 × 18.5× = $592. +51%.

  XBULL (${PRICE_XBULL}) : ELV becomes the integrated care company for 2030: Carelon
               achieves Optum-level external revenue ($20B+ from non-ELV clients);
               Medicaid rate reform (CMS value-based Medicaid waiver) eliminates
               the chronic rate inadequacy cycle; MA grows back to prior peak
               members + expands into new geographies; ACA markets profitable
               at bronze tier. EPS $35 × 20× = $700. +78%. Requires 4-5 year
               political + operational convergence.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-26")
print("=" * 72)
