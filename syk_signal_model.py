"""
Stryker Corporation (NYSE: SYK) — BottomUp Risk/Reward Signal Model

SIGNAL:  ◉ BUY
RATIO B: 0.64x  (Method B at 26× FY2027E $16.80 = $436.80; ratio 76.48/120.32 = 0.64×)
DATE:    2026-05-26
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "SYK"
COMPANY = "Stryker Corporation"
SECTOR  = "MedTech · Orthopedics (Mako Robotics) · MedSurg · Neurotechnology · Emergency Care"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  = 316.48   # SYK — stockanalysis.com / CNBC, 2026-05-23; -22% from 52-wk high
PRICE_52W_LOW  = 281.00   # 52-week low (cyberattack earnings miss + tariff fears)
PRICE_52W_HIGH = 404.87   # 52-week high (Dec 2025; strong FY2025 Mako + MedSurg momentum)
SHARES_M       = 420.0    # million diluted shares (~$132.9B market cap / $316.48)
DIVIDEND_ANN   =   3.44   # ~$0.86/quarter; ~1.09% yield; 14+ consecutive years of increases

# ── EPS (non-GAAP adjusted) ────────────────────────────────────────────────────
# SYK FY = calendar year. The EPS arc reflects 10-13% annual non-GAAP growth
# sustained for 10+ years, driven by Mako robotics installed base expansion,
# MedSurg product cycles (LIFEPAK 35, ProCuity beds, Vocera), and disciplined
# bolt-on M&A. FY2026 EPS growth guided at 9-11% despite Q1 cyberattack miss.
EPS_FY2022 =  9.90    # est; ~11% growth; pre-Mako supercycle; demographics building
EPS_FY2023 = 10.95    # est; ~10.6% growth; Mako installed base 2,500+; int'l expansion
EPS_FY2024 = 12.19    # est; ~11.3% growth; Mako + MedSurg both accelerating
EPS_FY2025 = 13.63    # actual (+11.8% YoY); full-year revenue $25.12B; organic +10.3%
                       # Q4 2025: adj EPS $4.47 (+11.5%); revenue $7.2B (+11.4%)
EPS_NOW    = 15.00    # FY2026E midpoint (guided $14.90-$15.10; maintained post-cyberattack)
                       # Q1 2026: adj EPS $2.60 vs $2.98 est (-13%); revenue $6.0B (+2.6%)
                       # Miss = cyberattack (Iran-linked Handala; ~3 wks manufacturing shutdown)
                       # $310M Q1 revenue miss; recovery expected Q2-Q4; guidance maintained

# ── EPP Floor ─────────────────────────────────────────────────────────────────
# EPS_TROUGH = global recession + extended cyberattack disruption + tariff headwinds
# + healthcare spending contraction. From FY2024 $12.19: a severe scenario compresses
# EPS ~18% to $10.00 — requiring three simultaneous shocks to a business that has
# grown EPS every year for 10+ consecutive years across 20+ product lines.
# Calibration: 52-wk low $281.00 ÷ $10.00 = 28.1× stress EPS — the market bottomed
# at 28× stress EPS, comfortably above EPP $240. SYK has never traded below 22-24×
# adj EPS in any recession, including COVID 2020. EPP floor has never been breached.
EPS_TROUGH = 10.00    # recession + cyber + tariffs; ~18% below FY2024 actual
EPP_MIN_PE = 24       # premium diversified medtech floor; 10-yr EPS consistency; IG rated
EPP        = EPS_TROUGH * EPP_MIN_PE   # $10.00 × 24 = $240.00

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E ~$16.80: FY2026E $15.00 × 12% growth. Stryker has delivered 10-13%
# adj EPS growth consistently for 10+ years, driven by:
#   • Mako robotics: 3,000+ installations; used in 2/3 of SYK US knee procedures
#     and 1/3 of US hip procedures; <30% global TKA penetration — long runway;
#     Mako RPS handheld launched Jan 2026, expands to smaller hospitals + ASCs
#   • MedSurg + Neurotechnology: LIFEPAK 35 global rollout (hospital refresh cycle
#     7-10 years; prior gen LIFEPAK 15 widely deployed); ProCuity smart beds;
#     Inari Medical (VTE, acquired FY2025; $500M growing 25-30%/yr); Vocera
#   • Q1 2026 cyber shortfall ($310M revenue): expected to recover Q2-Q4 2026
#     as order book held and manufacturing is fully restored
# Exit P/E: 26× — SYK historically trades 27-32× non-GAAP adj EPS. At 26×,
# the market is applying a discount to the cyber/tariff overhang while still
# recognising the structural Mako + MedSurg compounding franchise.
#   At 26×: $436.80  (+38% from $316.48) — conservative; Ratio B = 0.64×
#   At 29×: $487.20  (+54%) — historical average re-rate
#   At 32×: $537.60  (+70%) — BULL scenario; Mako supercycle + LIFEPAK 35 cycle
CONS_EPS_2YR = 16.80
CONS_EXIT_PE = 26

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
# BEAR:  Second cyberattack, or Q1 recovery stalls; tariffs worsen; recession
#        reduces elective surgical volumes 10-15%. EPS compresses to $10.00;
#        market applies 24× EPP floor = $240. -24% from current.
#        BEAR and EPP floor converge at this level.
# BASE:  Q1 shortfall recovered Q2-Q4 2026; FY2026 $15.00 delivered; Mako RPS
#        expands installed base; Inari integrates; FY2027E $16.80 × 25× = $420.
# BULL:  Mako supercycle (RPS to 5,000+ ASCs; 45%+ US TKA penetration);
#        LIFEPAK 35 hospital refresh cycle adds $500M+; Inari $1B by 2027.
#        $18.50 × 28.6× = $530. +67%.
# XBULL: SYK dominant global medtech platform; Mako extends to shoulder + spine;
#        LIFEPAK 35 global standard; neurovascular compounds. $21 × 32.4× = $680.
PRICE_BEAR  =  240
PRICE_BASE  =  420
PRICE_BULL  =  530
PRICE_XBULL =  680

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.40, 0.25, "Mako robotics: 3,000+ installs; <30% global TKA penetration; RPS"),
    (+0.30, 0.20, "LIFEPAK 35 + MedSurg: hospital refresh cycle; Inari Medical VTE"),
    (+0.20, 0.15, "Cyber recovery: one-time event; mfg restored; full-yr guidance held"),
    (-0.40, 0.25, "Tariff exposure: global mfg + supply chain; ~$80-120M FY2026 hit"),
    (-0.20, 0.15, "Cyberattack overhang: data extraction claimed; repeat risk"),
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
  Stress EPS ($10.00) × 24× premium medtech compounder floor. EPS_TROUGH
  is set ~18% below FY2024 actual ($12.19), representing a concurrent
  recession, extended cyberattack disruption, and tariff headwinds — three
  simultaneous shocks to a business with 10+ consecutive years of EPS growth
  across 20+ product lines in 5 diversified healthcare categories.
  EPP = $240.00.
  Calibration: 52-wk low $281.00 ÷ $10.00 = 28.1× stress EPS — the market
  bottomed at 28× stress EPS, well above the EPP floor, confirming that even
  at maximum fear investors assigned a 24× structural quality premium.
  SYK has NEVER traded below 22-24× adj EPS in any recession, including
  COVID (2020). The EPP floor at $240 has never been approached, let alone
  breached, in 15+ years of unbroken earnings growth.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E ~$16.80 (FY2026E $15.00 × 12% growth; Mako RPS + LIFEPAK 35 cycle
  + Inari Medical integration + Q1 cyber shortfall recovered) × 26× exit P/E
  (below SYK's historical 27-32× — still discounting cyber/tariff overhang)
  = $436.80.
  Ratio B = ($316.48 − $240.00) / ($436.80 − $316.48) = $76.48 / $120.32 = 0.64×
  → ◉ BUY. At 21.1× FY2026E, Stryker is at its lowest forward multiple
  since 2020 — pricing a permanent impairment of the growth trajectory that
  one quarter of cyberattack-disrupted data does not support.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STRYKER: A DECADE-LONG COMPOUNDER DISRUPTED BY A ONE-TIME CYBER EVENT
======================================================================

Stryker is one of the world's largest and most diversified medical technology
companies ($25.1B in FY2025 revenue), operating across two segments:
  • MedSurg & Neurotechnology ($15.7B FY2025; ~62% of revenue; +16% YoY):
    surgical equipment, endoscopy, emergency care (LIFEPAK defibrillators),
    neurovascular, hospital beds and communications (Vocera), and the newly
    acquired Inari Medical (venous thromboembolism).
  • Orthopaedics ($9.4B FY2025; ~38% of revenue; +8.9% YoY):
    total knee and hip replacement, trauma, spine, and the Mako SmartRobotics
    platform — the dominant robotic joint replacement system globally.

The investment thesis is simple: an aging population drives secular demand for
joint replacement and cardiovascular procedures. Stryker dominates both with
differentiated technology (Mako robotics) and sticky installed-base products
(LIFEPAK, ProCuity hospital beds). At 21.1× FY2026E, the company is priced
as if the Iran-linked cyberattack that hit in March 2026 permanently impaired
the business. It did not. The order book held. Procedures were deferred,
not cancelled. Manufacturing is fully restored.

Q1 2026 — THE CYBERATTACK QUARTER
===================================
  Revenue (reported):    $6.02B   (+2.6% YoY; organic +2.4%)
  Adjusted EPS:          $2.60    (-8.5% YoY; missed $2.98 consensus by 13%)
  Revenue miss:          ~$310M   (three weeks of manufacturing shutdown)
  MedSurg & Neurotech:   $3.2B    (+5.0% YoY; relatively resilient)
  Orthopaedics:          $2.8B    (~flat; most impacted by supply disruption)
  FY2026 EPS guidance:   $14.90-$15.10  MAINTAINED despite Q1 miss
  FY2026 organic growth: 8.0%-9.5%      MAINTAINED

The critical data point: full-year guidance was maintained despite a $310M
revenue miss in Q1. This means Q2-Q4 must deliver adj EPS of ~$12.30-$12.50
combined (avg ~$4.10/quarter) vs Q4 2025's $4.47. The guidance is conservative
— management is allowing for some residual disruption while still committing
to 9-11% adj EPS growth for the full year.

THE CYBERATTACK — WHAT HAPPENED AND WHY IT IS A ONE-TIME EVENT
================================================================
In late March 2026, an Iran-linked hacking group called Handala attacked:
  • Wiped Microsoft Windows systems across Stryker's global network
  • Handala claims: 200,000+ devices wiped; 50TB data extracted
    (company is investigating; has not confirmed data theft)
  • Manufacturing shutdown: ~3 weeks globally
  • Revenue loss: ~$310M in Q1 2026 — largest one-quarter operational
    disruption in Stryker's history
  • Recovery: CEO Kevin Lobo — "I am pleased with our team's ability
    to recover quickly from the cyber incident"

Why this is a one-time event, not a structural impairment:
  1. Manufacturing is back. Fully operational by end of April 2026.
  2. Order book held. Customers deferred, did not cancel.
  3. Procedure volumes held. Hospitals continued booking surgeries during
     the manufacturing outage — demand is deferred, not destroyed.
  4. Cybersecurity insurance: Stryker carries coverage for events of
     this type; partial revenue/margin recovery expected.
  5. Remediation: significant post-attack investment in IT infrastructure
     hardening. Repeat attack risk is elevated but declining.

Residual risks: (1) data extraction by Handala if confirmed — HIPAA
exposure, regulatory investigations, litigation; (2) repeat attack risk
before remediation is complete; (3) management credibility on IT security.
These are real but quantifiable, not existential.

MAKO SMARTROBOTICS — THE COMPOUNDING MOAT
==========================================
Mako is Stryker's robotic arm-assisted surgical platform for joint
replacement, and the most commercially successful surgical robot outside
laparoscopic surgery:
  • 3,000+ active system installations (across 45+ countries)
  • 1.5 million+ Mako procedures performed globally
  • Used in 2/3 of all Stryker US knee replacement procedures
  • Used in 1/3 of all Stryker US hip replacement procedures
  • Global robotic TKA penetration: <30% — structural long runway

Why Mako creates a durable economic moat:
  1. IMPLANT PULL-THROUGH: every Mako procedure uses proprietary Stryker
     implants (knee/hip components). Installing Mako locks in implant revenue
     for 7-15 years per system. The recurring consumables + implant economics
     dwarf the initial robot capital sale.
  2. SWITCHING COSTS: Mako surgeon and OR staff training is extensive.
     Switching to a competitor (Zimmer Biomet Rosa, DePuy Velys) requires
     a full retraining program that surgeons resist. Re-tender cycle 7-10 yrs.
  3. OUTCOMES DATA: 10+ years of real-world clinical outcomes showing improved
     precision vs. manual surgery. Competitors cannot replicate this data asset
     overnight.
  4. COMPETITIVE MOAT vs. JNJ Velys: JNJ's robotic knee system is growing
     but lacks multi-joint capability. Mako covers knee, hip, and (via Mako
     RPS) expanding further. No competitor has matched Mako's installed base
     or clinical dataset.

MAKO RPS — EXPANDING THE ADDRESSABLE MARKET
=============================================
Announced late 2025, first cases January 2026. Mako RPS (Robotic Platform
System) is a handheld robotic guidance system for total knee arthroplasty:
  • Lower cost than full Mako arm → addressable to ASCs (ambulatory surgery
    centres) and smaller hospitals that cannot justify the full system
  • Real-time haptic feedback and bone registration without a robotic arm
  • US market: ~5,000 ASCs and smaller hospitals not currently addressed
  • Strategic: blocks competitor entry into the handheld robotic space
    (Zimmer, DePuy both developing handheld guidance systems)

LIFEPAK 35 — THE HOSPITAL REFRESH CYCLE
==========================================
LIFEPAK is Stryker's emergency cardiac care platform, deployed in hospitals
and ambulances. LIFEPAK 35 is the latest generation:
  • 7-10 year replacement cycle: hospitals refreshing LIFEPAK 15 → LIFEPAK 35
  • International: cleared in most global markets; commercial rollout underway
  • Revenue driver: part of Emergency Care sub-segment within MedSurg
  • Structural: defibrillators are not discretionary; hospital regulation
    requires periodic technology refresh regardless of budget conditions

INARI MEDICAL (VTE — VENOUS THROMBOEMBOLISM)
=============================================
Acquired in FY2025, Inari added mechanical clot removal for venous conditions:
  • ClotTriever: catheter-based DVT (deep vein thrombosis) clot removal
  • FlowTriever: aspiration thrombectomy for pulmonary embolism (PE)
  • Revenue: ~$500M at acquisition, growing 25-30%/yr
  • VTE is the third-most-common cardiovascular disease globally; severe under-
    penetration of mechanical intervention vs. pharmacological treatment
  • Integration into MedSurg & Neurotechnology segment; expected accretive 2026+
  • Parallel to BSX's Penumbra acquisition in same market — confirms strategic
    importance and depth of the mechanical thrombectomy opportunity

BALANCE SHEET AND CASH FLOW
=============================
  FY2025 revenue:       $25.12B  (+11.2%; organic +10.3%)
  FY2025 adj EPS:       $13.63   (+11.8%)
  FCF generation:       ~$3.5-4.0B/yr  (~14-16% FCF margin)
  Net debt:             ~$9-10B (manageable; investment grade Baa1/BBB+)
  Tariff headwind:      ~$80-120M FY2026; partially offset by cost actions
  Dividend:             $3.44/yr ($0.86/quarter); 14+ consecutive annual increases
  Capital allocation:   M&A (Inari, bolt-ons) + buybacks; no special dividends

WHERE RISK/REWARD IMPROVES
============================
  BUY now             : $280-320  (at/near 52-wk low; 21× FY2026E; ratio_b 0.6-0.8×)
  ACCUMULATE          : $320-360  (recovery data builds; ratio_b 0.8-1.1×)
  WATCHLIST           : $360-400  (approaching 52-wk high; ratio_b 1.1-1.5×)
  TRIM                : $440-470  (above Method B ceiling; ratio_b >1.75×)

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

print(f"  Current price         : ${CURRENT_PRICE:.2f}  (-22% from 52-wk high ${PRICE_52W_HIGH}; +13% from 52-wk low ${PRICE_52W_LOW})")
print(f"  EPP floor             : ${EPP:.2f}   (+{epp_gap_pct:.1f}% above; 24× × ${EPS_TROUGH} stress EPS; 52-wk low ${PRICE_52W_LOW} ÷ $10 = 28.1×)")
print(f"  Method B (26× exit)   : ${price_b:.2f}  (+{(price_b/CURRENT_PRICE-1)*100:.1f}%; ratio_b = {ratio_b:.2f}× → BUY)")
print(f"  At 29× exit           : ${CONS_EPS_2YR*29:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*29-CURRENT_PRICE):.2f}× (historical average multiple)")
print(f"  At 32× exit           : ${CONS_EPS_2YR*32:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*32-CURRENT_PRICE):.2f}× (BULL re-rate)")
print(f"  BEAR scenario         : ${PRICE_BEAR}   (-24%; EPP floor; cyber + tariff + recession; $10 × 24×)")
print(f"  BASE scenario         : ${PRICE_BASE}   (+33%; cyber recovered; FY2027E $16.80 × 25×)")
print(f"  BULL scenario         : ${PRICE_BULL}   (+67%; Mako supercycle + Inari + LIFEPAK 35; $18.50 × 28.6×)")
print(f"  XBULL scenario        : ${PRICE_XBULL}   (+115%; dominant global medtech; Mako shoulder+spine; $21 × 32.4×)")
print(f"  Forward P/E (FY2026E) : {CURRENT_PRICE/EPS_NOW:.1f}×   (${CURRENT_PRICE} / ${EPS_NOW}; lowest since 2020 COVID; pricing permanent impairment)")
print(f"  Forward P/E (FY2027E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×   (${CURRENT_PRICE} / ${CONS_EPS_2YR}; 26× exit vs historical 27-32×)")
print(f"  EPS history           : FY22 ~${EPS_FY2022} → FY23 ~${EPS_FY2023} → FY24 ~${EPS_FY2024} → FY25 ${EPS_FY2025} → FY26E ${EPS_NOW}")
print(f"  Q1 2026               : Revenue $6.02B (+2.6%); adj EPS $2.60 (-8.5%); $310M miss from cyberattack")
print(f"  FY2026 guidance       : adj EPS $14.90-$15.10; organic 8-9.5% — MAINTAINED post-cyberattack")
print(f"  Cyberattack           : Iran-linked Handala; late March 2026; 3-wk mfg shutdown; $310M Q1 miss")
print(f"  Mako robotics         : 3,000+ installs; 1.5M+ procedures; <30% global TKA penetration")
print(f"  Mako RPS              : handheld version launched Jan 2026; targets 5,000+ ASCs + smaller hospitals")
print(f"  LIFEPAK 35            : hospital defibrillator refresh cycle (7-10 yr); global rollout underway")
print(f"  Inari Medical         : acquired FY2025; ~$500M VTE revenue growing 25-30%; ClotTriever + FlowTriever")
print(f"  FY2025 revenue        : $25.12B (+11.2%); organic +10.3%; MedSurg 62% / Ortho 38%")
print(f"  Q4 2025               : adj EPS $4.47 (+11.5%); revenue $7.2B (+11.4%); strong pre-cyber momentum")
print(f"  Tariffs               : ~$80-120M FY2026 headwind; partially offset via pricing + supply actions")
print(f"  Dividend              : ${DIVIDEND_ANN:.2f}/yr ({DIVIDEND_ANN/CURRENT_PRICE*100:.1f}% yield; 14+ consecutive annual increases)")
print(f"  Market cap            : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  BUY zone              : $280-320  (near/at 52-wk low; 21× FY2026E; cyber panic priced in)")
print(f"  ACCUMULATE            : $320-360  (recovery confirmation; ratio_b 0.8-1.1×)")
print(f"  WATCHLIST             : $360-400  (approaching 52-wk high; ratio_b 1.1-1.5×)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.75×  |  Idiosyncratic: 70%  |  Macro: 30%

  Driver                                                      Type    Wt  Note
  ─────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  Mako robotics: 3,000+ installs; <30% global TKA penetration  IDIO  25%  MOAT: installed base → implant pull-through
  LIFEPAK 35 + MedSurg refresh: Inari VTE; Vocera; ProCuity   IDIO  20%  MULTI-YR: hospital capex cycle; recurring
  Cyber recovery: mfg restored; order book held; guidance held IDIO  15%  ONE-TIME: insurance; remediation invested
  Tariff exposure: global mfg + China supply chain             MACRO 20%  HEADWIND: $80-120M FY2026; partly offset
  Elective surgical volume: aging pop + rate-cut tailwind      MACRO 20%  SECULAR: aging demographics; rate relief""")

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
  BEAR  (${PRICE_BEAR}) : A second cyberattack hits before remediation is complete,
               OR Q1 2026 cyber recovery stalls and management fails to deliver
               maintained full-year guidance. Tariffs worsen and cannot be
               offset by pricing or supply chain actions. A mild recession
               reduces elective surgical volumes 10-15%. EPS compresses to
               $10.00; market applies 24× EPP structural floor = $240.
               -24% from current. Requires three concurrent shocks.

  BASE  (${PRICE_BASE}) : Q1 2026 $310M revenue shortfall is recovered in Q2-Q4 as
               manufacturing runs at full capacity and deferred orders ship.
               FY2026 guidance of $15.00 adj EPS delivered. Mako RPS begins
               expanding into ASCs; Inari Medical integrates and grows 20%+;
               LIFEPAK 35 international rollout adds incremental revenue.
               FY2027E $16.80 × 25× = $420. +33% from current.

  BULL  (${PRICE_BULL}) : Mako supercycle accelerates — RPS expands to 5,000+ ASCs;
               Mako penetration reaches 45-50% of all US TKA procedures;
               international traction (Europe + Asia) surges post-RPS. LIFEPAK
               35 multi-year hospital refresh cycle adds $500M+ incremental
               revenue. Inari reaches $1B revenue by 2027. Multiple expands
               to 29× as cyber overhang clears. $18.50 × 28.6× = $530. +67%.

  XBULL (${PRICE_XBULL}) : SYK becomes the dominant global medtech platform across
               4 categories — Mako platform extended to shoulder + spine
               (regulatory approval 2027-2028); LIFEPAK 35 becomes the
               global hospital standard; Inari/VTE compounds at 25%+/yr;
               neurovascular grows through acquisitions. 10+ consecutive
               years of 12-15% EPS growth re-rate to 32× premium.
               FY2028-29E ~$21.00 × 32.4× = $680. +115%.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-26")
print("=" * 72)
