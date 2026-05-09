#!/usr/bin/env python3
"""
ISRG Signal Model  v1
──────────────────────
Intuitive Surgical, Inc. (NASDAQ: ISRG)  ·  Surgical Robotics / Medical Devices
EPP anchor: 2022 trough  (rate-shock; MedTech de-rate; China lockdowns)
Valuation date: May 2026

Unique sections for ISRG:
  ⓪  EPP 2022 anchor — what it takes to return to 2022 multiples & likelihood
  ①  Signal dashboard
  ②  Bear case anatomy
  ③  Updated EPP (May 2026)
  ④  EPS inflation decomposition  (2022 → 2025: real growth vs. price/inflation)
  ⑤  Conservative 2-year growth trajectory
  ⑥  Attractiveness ratio  Δ(current → EPP) / Δ(current → 2yr-reflated)
  ⑦  Volatility context
  ⑧  Scenario probabilities
"""
import math

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
CURRENT_PRICE   = 530.0    # ISRG May 2026  (est.; last firm data ~$490 Aug-2025)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

SCENARIOS = {
    #           EPS    mult   price   narrative
    "BEAR":  ( 8.20,  42,    344,   "China ban + GLP-1 volume erosion + hospital capex freeze"),
    "BASE":  (11.50,  58,    667,   "DV5 global rollout; Ion scaling; steady share gains"),
    "BULL":  (13.50,  65,    878,   "Ion mainstream; new indications (colorectal, cardiac)"),
    "XBULL": (16.00,  72,   1152,   "Surgical AI platform; international re-acceleration"),
}

# ══════════════════════════════════════════════════════════════════════════════
# ⓪  EPP 2022 ANCHOR
# ══════════════════════════════════════════════════════════════════════════════
EPP_2022_EPS        = 4.96    # FY2022 actual non-GAAP EPS
EPP_2022_MIN_PE     = 40.0    # trough multiple paid at EPP (monopoly quality floor)
EPP_2022_PRICE      = EPP_2022_EPS * EPP_2022_MIN_PE   # = $198
EPP_2022_TROUGH_ACT = 197.0   # actual 52-week low 2022

# What triggered the 2022 de-rate:
DE_RATE_TRIGGERS_2022 = [
    ("Rate shock (Fed +525bp)",          "P/E compression 70x → 40x  (all growth stocks re-rated)"),
    ("China COVID lockdowns",            "Shanghai lockdown cut ISRG China revenue ~40% in Q2 2022"),
    ("Post-COVID OR normalization",      "Procedure backlog cleared; growth rate 'normalized' optics"),
    ("General MedTech de-rate",          "Sector P/E contracted; hospital capex uncertainty"),
    ("No growth catalyst in sight",      "DV5 not yet announced; Ion still early; pipeline opaque"),
]

# What it would take NOW to return to 40x P/E  (same trough)
RETURN_TO_2022_PE   = 40.0
RETURN_TO_2022_PRICE = None   # computed below using TODAY's EPS

# ══════════════════════════════════════════════════════════════════════════════
# PROXY SIGNALS
# ══════════════════════════════════════════════════════════════════════════════
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("da Vinci system placements YoY",   "% YoY",
       0.0,   5.0,  12.0,  20.0,  14.0, True,
      "Hospitals freeze capital; DV5 sticker-shock; budget cuts"),

    ("Total procedure volume YoY",       "% YoY",
       2.0,   8.0,  14.0,  20.0,  17.0, True,
      "GLP-1 cuts bariatric/hernia volumes; elective freeze"),

    ("Ion platform procedures YoY",      "% YoY",
       5.0,  30.0,  60.0, 100.0,  75.0, True,
      "Reimbursement denied; Veran/Olympus bronchoscopy adopted"),

    ("International revenue growth YoY", "% YoY",
       0.0,   8.0,  15.0,  22.0,  13.0, True,
      "China ban (trade war); EU hospital austerity wave"),

    ("Hospital capital spending YoY",    "% YoY",
      -5.0,   3.0,   7.0,  12.0,   5.0, True,
      "CMS reimbursement cuts; hospital CFO capex freeze"),

    ("China procedure volume YoY",       "% YoY",
     -30.0,   0.0,  10.0,  20.0,   8.0, True,
      "Trade war escalates; NMPA restricts US medtech licenses"),
]
WEIGHTS = [0.25, 0.25, 0.15, 0.15, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("da Vinci installed base switching cost moat",      1.5, 0.25),
    ("No credible full-system competitor (2026)",        1.0, 0.20),
    ("China / geopolitical revenue concentration",      -1.0, 0.20),
    ("GLP-1 obesity drugs → bariatric volume overhang", -0.5, 0.15),
    ("da Vinci 5 upgrade cycle still early innings",     0.8, 0.20),
]

# ══════════════════════════════════════════════════════════════════════════════
# ③  UPDATED EPP  (May 2026)
# ══════════════════════════════════════════════════════════════════════════════
EPP_TODAY_EPS  = 8.00    # FY2025 full-year non-GAAP EPS (normalized)
EPP_MIN_PE     = 40.0    # same monopoly-quality floor as 2022 anchor
EPP_REGIME_NOTE = "(unchanged 40x — surgical monopoly moat; no credible competitor changes floor)"

# ══════════════════════════════════════════════════════════════════════════════
# ④  EPS INFLATION DECOMPOSITION  (2022 → 2025)
# ══════════════════════════════════════════════════════════════════════════════
EPS_2022 = 4.96
EPS_2025 = 8.00
# 3-year EPS CAGR:  (8.00/4.96)^(1/3) - 1 = 17.3%/yr
# Break it down:
DECOMP = {
    # (label, pct_contribution_to_eps_growth, note)
    "Real procedure volume growth":
        (0.460, "~15.5%/yr proc vol CAGR × 3yr → +46% real vol contribution"),
    "ASP / consumable price hikes":
        (0.120, "~4%/yr ASP increase on instruments & accessories"),
    "CPI / general cost pass-through":
        (0.110, "~13% cumul. CPI 2022-25; partially passed to hospitals"),
    "Operating leverage / margin expansion":
        (0.240, "Gross margin expanded ~200bp; OpEx leverage on fixed cost"),
    "Share count reduction":
        (0.015, "Minimal; ISRG does limited buybacks, stock comp dilution offset"),
    "Mix shift (higher-value procedures)":
        (0.055, "Ion + complex indications carry higher per-procedure revenue"),
}
# Inflation-attributable EPS:  ASP hikes + CPI pass-through
INFLATION_SHARE_OF_EPS_GROWTH = DECOMP["ASP / consumable price hikes"][0] + \
                                  DECOMP["CPI / general cost pass-through"][0]
EPS_GROWTH_TOTAL = (EPS_2025 / EPS_2022) - 1
EPS_INFLATION_DOLLAR = EPS_2022 * INFLATION_SHARE_OF_EPS_GROWTH
EPS_REAL_DOLLAR = EPS_2025 - EPS_2022 - EPS_INFLATION_DOLLAR

# ══════════════════════════════════════════════════════════════════════════════
# ⑤  CONSERVATIVE 2-YEAR GROWTH  (May 2026 → May 2028)
# ══════════════════════════════════════════════════════════════════════════════
CONS_SIGNALS = [
    ("da Vinci placements",      8.0,  "+8%/yr  (vs +14%; DV5 adoption normalizes at scale)"),
    ("Procedure volume",        10.0,  "+10%/yr (vs +17%; GLP-1 headwind baked in)"),
    ("Ion platform procs",      45.0,  "+45%/yr (vs +75%; scaling from still-small base)"),
    ("International revenue",    8.0,  "+8%/yr  (vs +13%; China caution structurally embedded)"),
    ("Hospital capex",           3.0,  "+3%/yr  (vs +5%; CFOs remain cautious)"),
    ("China procedures",         0.0,   "Flat    (vs +8%; geopolitical risk; zero growth assumed)"),
]
CONS_EPS_CAGR  = 0.14    # 14%/yr  (vs consensus ~18-20%; meaningful haircut)
CONS_EXIT_PE   = 55.0    # de-rate from current ~66x; still premium for monopoly quality
CONS_DIVIDEND  = 0.0     # ISRG pays no dividend

# FY2027E at conservative:
CONS_EPS_2YR   = EPP_TODAY_EPS * (1 + CONS_EPS_CAGR) ** 2

# ══════════════════════════════════════════════════════════════════════════════
# VOLATILITY
# ══════════════════════════════════════════════════════════════════════════════
VOL_ANNUAL_PCT = 0.28
VOL_BETA       = 1.05
VOL_52W_LOW    = 390.0
VOL_52W_HIGH   = 570.0

# ══════════════════════════════════════════════════════════════════════════════
# SCORING / MATH ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def score_signal(val, base_f, bull_f, xbull_f, hib):
    if hib:
        if val >= xbull_f: return 4
        if val >= bull_f:  return 3
        if val >= base_f:  return 2
        return 1
    else:
        if val <= xbull_f: return 4
        if val <= bull_f:  return 3
        if val <= base_f:  return 2
        return 1

ICONS = {4: "★ XBULL", 3: "▲ BULL", 2: "◦ BASE", 1: "⚠ BEAR"}

def softmax_probs(composite, T=0.60):
    centres = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    raw = {k: math.exp(-abs(composite - c) / T) for k, c in centres.items()}
    tot = sum(raw.values())
    return {k: v / tot for k, v in raw.items()}

def expected_price(probs):
    return sum(probs[k] * SCENARIOS[k][2] for k in probs)

def market_implied_composite(target_ev, tolerance=5.0):
    for c in [x / 100 for x in range(100, 401)]:
        if abs(expected_price(softmax_probs(c)) - target_ev) < tolerance:
            return round(c, 2), softmax_probs(c)
    return None, None

# ── COMPUTE ───────────────────────────────────────────────────────────────────
W = 78

scored = [
    (name, unit, bv, bf, blf, xf, cv, hib, narr,
     score_signal(cv, bf, blf, xf, hib), w)
    for (name, unit, bv, bf, blf, xf, cv, hib, narr), w
    in zip(SIGNALS, WEIGHTS)
]
proxy_composite = sum(s * w for *_, s, w in scored)
bear_composite  = sum(score_signal(bv, bf, blf, xf, hib) * w
                      for (_, __, bv, bf, blf, xf, ___, hib, ____), w
                      in zip(SIGNALS, WEIGHTS))
sca             = sum(s * w for _, s, w in STRUCTURAL_FACTORS)
adj_composite   = proxy_composite + sca
proxy_probs     = softmax_probs(proxy_composite)
bear_probs      = softmax_probs(bear_composite)
proxy_ev        = expected_price(proxy_probs)

market_target_ev            = CURRENT_PRICE * ((1 + REQUIRED_RETURN) ** HORIZON_YEARS)
mkt_composite, mkt_probs    = market_implied_composite(market_target_ev)
mkt_ev = expected_price(mkt_probs) if mkt_probs else market_target_ev

# Updated EPP
epp_updated     = EPP_TODAY_EPS * EPP_MIN_PE
epp_gap_pct     = (CURRENT_PRICE - epp_updated) / epp_updated * 100
bear_vs_epp_pct = (SCENARIOS["BEAR"][2] - epp_updated) / epp_updated * 100

# 2022 → today multiple bridge
current_pe      = CURRENT_PRICE / EPP_TODAY_EPS
pe_2022_trough  = EPP_2022_TROUGH_ACT / EPP_2022_EPS
RETURN_TO_2022_PRICE = EPP_TODAY_EPS * RETURN_TO_2022_PE  # price if P/E compressed to 40x

# Conservative 2-yr
cons_price_2yr  = CONS_EPS_2YR * CONS_EXIT_PE
cons_total_ret  = (cons_price_2yr - CURRENT_PRICE) / CURRENT_PRICE * 100
cons_annual_ret = cons_total_ret / 2

# ⑥  ATTRACTIVENESS RATIO
# -- Method A: EPS-tracking  (price grows proportionally with EPS, same multiple)
eps_growth_2yr        = (CONS_EPS_2YR / EPP_TODAY_EPS) - 1
price_reflated_same_pe = CURRENT_PRICE * (1 + eps_growth_2yr)   # price if multiple held

# -- Method B: Multiple × forward EPS  (conservative exit multiple)
price_reflated_cons_pe = CONS_EPS_2YR * CONS_EXIT_PE            # = cons_price_2yr

# -- Method C: Base-case scenario price (most likely outcome from model)
price_reflated_base    = SCENARIOS["BASE"][2]

dist_to_epp    = CURRENT_PRICE - epp_updated                     # downside to floor
dist_A         = price_reflated_same_pe - CURRENT_PRICE          # upside A
dist_B         = price_reflated_cons_pe - CURRENT_PRICE          # upside B
dist_C         = price_reflated_base    - CURRENT_PRICE          # upside C

ratio_A = dist_to_epp / dist_A if dist_A > 0 else float("inf")
ratio_B = dist_to_epp / dist_B if dist_B > 0 else float("inf")
ratio_C = dist_to_epp / dist_C if dist_C > 0 else float("inf")

# Volatility
sigma_1yr         = CURRENT_PRICE * VOL_ANNUAL_PCT
sigma_needed_bear = (CURRENT_PRICE - SCENARIOS["BEAR"][2]) / sigma_1yr

if mkt_composite:
    adj_gap = adj_composite - mkt_composite
    if   adj_gap >  0.50: _verdict = "UNDERVALUED"
    elif adj_gap >  0.20: _verdict = "MODESTLY UNDERVALUED"
    elif adj_gap > -0.20: _verdict = "FAIRLY VALUED"
    elif adj_gap > -0.50: _verdict = "MODESTLY OVERVALUED"
    else:                 _verdict = "OVERVALUED"
else:
    adj_gap, _verdict = 0.0, "N/A"

# ══════════════════════════════════════════════════════════════════════════════
# OUTPUT
# ══════════════════════════════════════════════════════════════════════════════
print()
print("═" * W)
print(f"  ISRG  ·  Intuitive Surgical  ·  ${CURRENT_PRICE:.0f}  ·  Surgical Robotics / Medical Devices")
print(f"  May 2026  ·  EPP anchor: 2022 trough  ·  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

# ── ⓪  EPP 2022 ANCHOR ────────────────────────────────────────────────────────
print(f"""
  ⓪  EPP 2022 ANCHOR  —  What it takes to return to 2022 multiples
  {"─" * (W-2)}
  The 2022 EPP was marked when ISRG hit trough from a perfect storm of
  simultaneous de-rating triggers.  Reconstructing that regime today:

  2022 trough data:
    FY2022 non-GAAP EPS:         ${EPS_2022:.2f}
    Actual 52-wk low (2022):     ${EPP_2022_TROUGH_ACT:.0f}
    Implied trough P/E:          {pe_2022_trough:.1f}x
    EPP formula (EPS × 40x):     ${EPP_2022_PRICE:.0f}   ← model floor matched reality well

  May 2026 current:
    FY2025 non-GAAP EPS:         ${EPP_TODAY_EPS:.2f}   (+{EPS_GROWTH_TOTAL*100:.0f}% from 2022)
    Current price:               ${CURRENT_PRICE:.0f}
    Current P/E:                 {current_pe:.1f}x   (vs 40x trough; +{current_pe - pe_2022_trough:.0f}pt P/E expansion)
    Updated EPP (EPS×40x):       ${epp_updated:.0f}

  To return to 40x trough P/E on today's EPS (${EPP_TODAY_EPS:.2f}):
    Required price:              ${RETURN_TO_2022_PRICE:.0f}   ({(RETURN_TO_2022_PRICE/CURRENT_PRICE-1)*100:+.0f}% from ${CURRENT_PRICE:.0f})
    Sigma distance:              {(CURRENT_PRICE - RETURN_TO_2022_PRICE)/sigma_1yr:.1f}σ  (requires {(CURRENT_PRICE - RETURN_TO_2022_PRICE)/CURRENT_PRICE*100:.0f}% drawdown)

  What triggered 2022  (40x):""")
for trigger, desc in DE_RATE_TRIGGERS_2022:
    print(f"    ✗  {trigger:<35}  {desc}")

print(f"""
  What would trigger a return to 40x TODAY:
    ✗  All 5 conditions below must coincide  (none is sufficient alone):
       1.  China permanent ban or 50%+ revenue cut  (removes ~10-12% of revenue)
       2.  GLP-1 procedure collapse  (bariatric -50%+ → hernia/colorectal follow)
       3.  US hospital capex recession  (-10% spending YoY for 2+ quarters)
       4.  Federal Reserve rate shock II  (10yr yields back to 5%+ and rising)
       5.  DV5 competitive threat materializes  (e.g., J&J Ottava gets FDA clearance)

  Likelihood of returning to 40x P/E:  ~3-5%
    Rationale: Installed base of 9,000+ da Vinci systems creates structural
    recurring revenue (instruments/accessories ~70% of revenue) that did NOT
    exist at the same scale in 2022.  Floor quality is HIGHER now, not lower.
    China + GLP-1 are real risks but each individually insufficient.
    The monopoly moat (switching cost, surgeon training, FDA clearances) means
    any competitor is at minimum 5 years from threatening the installed base.
    A 40x re-rating is a 'financial crisis + fundamental break' event simultaneously.""")

# ── ①  SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print(f"\n  ①  SIGNAL DASHBOARD")
print(f"  {'Signal':<36}  {'BEAR':>7}  {'BASE≥':>7}  {'BULL≥':>7}  {'XBULL≥':>7}  {'NOW':>8}  Score")
print("  " + "─" * (W-2))
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u     = unit.split()[0] if unit else ""
    bv_s  = f"{bv:+.0f}{u}" if hib else f">{bv:.0f}{u}"
    bf_s  = f"{bf:.0f}{u}"
    blf_s = f"{blf:.0f}{u}"
    xf_s  = f"{xf:.0f}{u}"
    cv_s  = f"{cv:+.0f}{u}"
    bar   = "█" * s + "░" * (4 - s)
    print(f"  {name:<36}  {bv_s:>7}  {bf_s:>7}  {blf_s:>7}  {xf_s:>7}  {cv_s:>8}  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:    {proxy_composite:.2f} / 4.00")
if mkt_composite:
    print(f"  Market composite:   {mkt_composite:.2f} / 4.00  (back-solved from ${CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% hurdle)")
    print(f"  SCA adjustment:    {sca:+.2f}  →  Adj composite {adj_composite:.2f}  →  Gap {adj_gap:+.2f}  [{_verdict}]")

print(f"\n  Structural factors:")
for desc, score, wt in STRUCTURAL_FACTORS:
    arrow = "  +" if score > 0 else "  -"
    print(f"  {arrow}  {desc}  ({score:+.1f} × {wt*100:.0f}%  =  {score*wt:+.2f})")

# ── ②  BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print(f"\n  ②  BEAR CASE ANATOMY  (what variables need to do for BEAR to materialise)")
print("  " + "─" * (W-2))
print(f"  {'Signal':<36}  {'Current':>8}  {'Bear':>8}  Move    Trigger")
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u      = unit.split()[0] if unit else ""
    cv_s   = f"{cv:+.0f}{u}"
    bv_s   = f"{bv:+.0f}{u}"
    move_s = f"{bv - cv:+.0f}{u}"
    trigger = narr[:42] if len(narr) <= 42 else narr[:39] + "…"
    print(f"  {name:<36}  {cv_s:>8}  {bv_s:>8}  {move_s:>6}  {trigger}")

print(f"""
  Bear composite:  {bear_composite:.2f}  →  Bear price: ~${expected_price(bear_probs):.0f} (model) / ${SCENARIOS['BEAR'][2]} (defined)
  Bear probability (proxy model):  {proxy_probs['BEAR']*100:.1f}%

  KEY BEAR CHAIN: China geopolitical ban (most plausible single trigger) → removes
  10-12% revenue overnight → consensus EPS cut from $11.50 to ~$8.20 → multiple
  compresses from 66x to 42x (investors question growth rate) → bear price ~$344.
  GLP-1 risk is a slow-bleed, not acute; hospital capex freeze is cyclical, not structural.""")

# ── ③  UPDATED EPP ────────────────────────────────────────────────────────────
print(f"\n  ③  UPDATED EPP  (floor anchored on today's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS:          ${EPP_TODAY_EPS:.2f}  (FY2025 non-GAAP)")
print(f"  Min viable P/E at panic:          {EPP_MIN_PE:.0f}x  {EPP_REGIME_NOTE}")
print(f"  {'─' * 64}")
print(f"  UPDATED EPP:                     ${epp_updated:.0f}/share   (vs ${EPP_2022_PRICE:.0f} in 2022  = +{(epp_updated/EPP_2022_PRICE-1)*100:.0f}% higher floor)")
print(f"  Current ${CURRENT_PRICE:.0f} vs Updated EPP ${epp_updated:.0f}:   {epp_gap_pct:+.0f}%  ← above EPP floor")
print(f"  Bear ${SCENARIOS['BEAR'][2]} vs Updated EPP ${epp_updated:.0f}:   {bear_vs_epp_pct:+.0f}%  ← BEAR requires earnings impairment")
print(f"""
  EPP floor migration 2022 → 2026:
    2022 EPP:  ${EPP_2022_PRICE:.0f}  (${EPS_2022:.2f} × {EPP_2022_MIN_PE:.0f}x)
    2026 EPP:  ${epp_updated:.0f}  (${EPP_TODAY_EPS:.2f} × {EPP_MIN_PE:.0f}x)
    Floor moved up +${epp_updated - EPP_2022_PRICE:.0f} (+{(epp_updated/EPP_2022_PRICE-1)*100:.0f}%) in 3 years — entirely from EPS growth.
    The multiple floor is UNCHANGED.  The quality floor is EPS compounding.""")

# ── ④  EPS INFLATION DECOMPOSITION ───────────────────────────────────────────
print(f"\n  ④  EPS INFLATION DECOMPOSITION  (FY2022 ${EPS_2022:.2f} → FY2025 ${EPS_2025:.2f})")
print("  " + "─" * (W-2))
eps_total_growth   = EPS_2025 - EPS_2022
eps_cagr_realized  = (EPS_2025 / EPS_2022) ** (1/3) - 1
print(f"  Total EPS growth:  +${eps_total_growth:.2f}  (+{EPS_GROWTH_TOTAL*100:.0f}%  over 3yr;  CAGR +{eps_cagr_realized*100:.1f}%/yr)")
print(f"  {'─' * 64}")
print(f"  {'Driver':<40}  {'Share of growth':>16}  {'$EPS':>7}  Detail")
running = 0.0
for driver, (share, note) in DECOMP.items():
    dollar = EPS_2022 * share
    running += dollar
    bar = "█" * round(share * 40)
    print(f"  {driver:<40}  {share*100:>14.1f}%  ${dollar:>5.2f}  {note[:34]}")

print(f"  {'─' * 64}")
print(f"  INFLATION-ATTRIBUTED EPS (ASP + CPI):  {INFLATION_SHARE_OF_EPS_GROWTH*100:.0f}% of growth"
      f"  = ${EPS_INFLATION_DOLLAR:.2f}/share")
print(f"  REAL-GROWTH EPS (volume + leverage):   {(1-INFLATION_SHARE_OF_EPS_GROWTH)*100:.0f}% of growth"
      f"  = ${EPS_REAL_DOLLAR:.2f}/share")
print(f"""
  Interpretation:
    ~23% of the EPS lift from 2022 → 2025 came from pricing / inflation pass-through.
    ~77% was real: procedure volume growth, operating leverage, and mix shift.
    This is a healthy decomposition — ISRG did NOT inflate its EPS artificially.
    The business IS genuinely larger: ~9,000 installed systems vs ~7,500 in 2022.
    Stripping out inflation, "real" EPS in 2025 would be ~${EPS_2025 - EPS_INFLATION_DOLLAR:.2f} at 2022 dollars.
    Even that strips-out EPS still justifies EPP = ${(EPS_2025 - EPS_INFLATION_DOLLAR)*EPP_MIN_PE:.0f} (vs ${epp_updated:.0f} nominal).""")

# ── ⑤  CONSERVATIVE 2-YEAR GROWTH ────────────────────────────────────────────
print(f"\n  ⑤  CONSERVATIVE 2-YEAR GROWTH  (May 2026 → May 2028;  no tailwinds assumed)")
print("  " + "─" * (W-2))
print(f"  {'Signal':<36}  {'Conservative':>13}  vs Current  Rationale")
for sname, sval, srat in CONS_SIGNALS:
    key = sname.split()[0].lower()
    cur = next(cv for name, _, __, ___, ____, _____, cv, ______, _______ in SIGNALS
               if key in name.lower())
    diff = sval - cur
    print(f"  {sname:<36}  {sval:>13.1f}  {diff:>+9.0f}   {srat[:36]}")

print(f"""
  Conservative 2yr EPS:    ${EPP_TODAY_EPS:.2f} × (1+{CONS_EPS_CAGR*100:.0f}%)² = ${CONS_EPS_2YR:.2f}  (FY2027E conservative)
  Consensus 2yr EPS:       ${EPP_TODAY_EPS:.2f} × (1+19%)² = ${EPP_TODAY_EPS*(1.19**2):.2f}  (Street ~18-20% CAGR)
  At {CONS_EXIT_PE:.0f}x P/E (conservative exit, mild de-rate):  ${cons_price_2yr:.0f}/share
  {'─' * 64}
  Conservative 2yr price:  ${cons_price_2yr:.0f}  ({'▲' if cons_price_2yr > CURRENT_PRICE else '▼'}{abs(cons_price_2yr - CURRENT_PRICE):.0f} from ${CURRENT_PRICE:.0f})
  Conservative total return: {cons_total_ret:+.0f}% over 2yr  =  {cons_annual_ret:+.0f}%/yr  (no dividend)

  Key 2yr growth drivers (conservative):
    →  DV5 global rollout continues but slows as early adopters saturate
    →  Ion platform: reimbursement expanding (CMS favorable); 45%/yr still conservative
    →  China: flat assumption embeds trade war risk without assuming full ban
    →  Margin: modest operating leverage; no step-change assumed
    →  New indications (colorectal cancer, cardiac) NOT in conservative (option value)""")

# ── ⑥  ATTRACTIVENESS RATIO ──────────────────────────────────────────────────
print(f"\n  ⑥  ATTRACTIVENESS RATIO  —  EPP floor gap vs. EPS-reflated upside")
print("  " + "─" * (W-2))
print(f"""  Logic:
    Ratio = Δ(current → EPP floor)  /  Δ(current → 2yr-reflated price)
          = downside to floor       /  upside from EPS compounding

    Ratio < 1.0  →  more upside from EPS than gap to floor  →  ATTRACTIVE
    Ratio = 1.0  →  upside = gap to floor  →  NEUTRAL
    Ratio > 1.0  →  floor gap exceeds EPS upside  →  RICH / RISKY
    Ratio > 2.0  →  deeply pricing in growth; multiple expansion fully baked

  Inputs:
    Current price:             ${CURRENT_PRICE:.0f}
    Updated EPP floor:         ${epp_updated:.0f}
    Floor gap (downside):      ${dist_to_epp:.0f}  ({dist_to_epp/CURRENT_PRICE*100:.0f}% below current)""")

print(f"""
  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Method              2yr Target  Upside $   Upside %  Ratio   Signal   │
  ├─────────────────────────────────────────────────────────────────────────┤
  │  A: EPS-tracking     ${price_reflated_same_pe:>6.0f}      ${dist_A:>6.0f}    {dist_A/CURRENT_PRICE*100:>5.0f}%  {ratio_A:>5.2f}x  {'★ OK' if ratio_A < 1.5 else '⚠ RICH' if ratio_A < 2.5 else '✗ PRICED IN'}  │
  │     (same P/E × conserv EPS; multiple held constant)                   │
  │  B: Conserv exit PE  ${price_reflated_cons_pe:>6.0f}      ${dist_B:>6.0f}    {dist_B/CURRENT_PRICE*100:>5.0f}%  {ratio_B:>5.2f}x  {'★ OK' if ratio_B < 1.5 else '⚠ RICH' if ratio_B < 2.5 else '✗ PRICED IN'}  │
  │     ({CONS_EXIT_PE:.0f}x P/E on ${CONS_EPS_2YR:.2f} EPS; mild multiple compression)           │
  │  C: Base scenario    ${price_reflated_base:>6.0f}      ${dist_C:>6.0f}    {dist_C/CURRENT_PRICE*100:>5.0f}%  {ratio_C:>5.2f}x  {'★ OK' if ratio_C < 1.5 else '⚠ RICH' if ratio_C < 2.5 else '✗ PRICED IN'}  │
  │     (model BASE case: ${SCENARIOS['BASE'][1]}x × ${SCENARIOS['BASE'][0]:.2f} EPS)                          │
  └─────────────────────────────────────────────────────────────────────────┘""")

print(f"""
  Reading:
    Method A ({ratio_A:.2f}x):  If you hold the current {current_pe:.0f}x P/E, EPS growth
      alone produces +{dist_A/CURRENT_PRICE*100:.0f}% upside vs {dist_to_epp/CURRENT_PRICE*100:.0f}% floor gap.  {'Downside exceeds upside.' if ratio_A > 1 else 'Upside exceeds downside.'}

    Method B ({ratio_B:.2f}x):  At a de-rated {CONS_EXIT_PE:.0f}x exit (rate normalization),
      upside shrinks to +{dist_B/CURRENT_PRICE*100:.0f}%.  Floor gap to EPP ({dist_to_epp/CURRENT_PRICE*100:.0f}%) {'significantly exceeds earnings upside.' if ratio_B > 1.2 else 'roughly matches earnings upside.'}

    Method C ({ratio_C:.2f}x):  The BASE scenario implies +{dist_C/CURRENT_PRICE*100:.0f}% upside,
      {'almost offsetting' if ratio_C < 1.1 else 'which is' if ratio_C < 1.3 else 'but that still leaves'} the floor gap {'as roughly matched.' if ratio_C < 1.1 else 'below the floor gap.' if ratio_C > 1.0 else ''}.

  OVERALL ATTRACTIVENESS (May 2026 @ ${CURRENT_PRICE:.0f}):
    ISRG is priced for excellence.  The EPS compounder IS working —
    but at {current_pe:.0f}x earnings, the stock needs:  (1) no multiple compression,
    AND (2) EPS growth at BASE case or better.  The floor (EPP ${epp_updated:.0f}) is
    ~${dist_to_epp:.0f} ({dist_to_epp/CURRENT_PRICE*100:.0f}%) below.  Risk/reward is asymmetric ONLY if you
    are confident in 18%+ EPS CAGR with no multiple de-rate.
    At conservative assumptions (Method B), you earn ~{cons_annual_ret:+.0f}%/yr —
    {'below' if cons_annual_ret < 15 else 'at'} the 15% hurdle rate.  NOT a compelling entry at ${CURRENT_PRICE:.0f}.""")

# ── ⑦  VOLATILITY CONTEXT ────────────────────────────────────────────────────
print(f"\n  ⑦  VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        ${VOL_52W_LOW:.0f}  –  ${VOL_52W_HIGH:.0f}")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized")
print(f"  Beta vs S&P 500:      {VOL_BETA:.2f}")
print(f"  1-sigma range (1yr):  ${CURRENT_PRICE - sigma_1yr:.0f}  –  ${CURRENT_PRICE + sigma_1yr:.0f}  (${CURRENT_PRICE:.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  2-sigma range (1yr):  ${CURRENT_PRICE - 2*sigma_1yr:.0f}  –  ${CURRENT_PRICE + 2*sigma_1yr:.0f}")
print(f"  {'─' * 64}")
print(f"  EPP floor ${epp_updated:.0f}:     {(CURRENT_PRICE - epp_updated)/sigma_1yr:.1f}σ  below current  (requires fundamental break)")
print(f"  Bear ${SCENARIOS['BEAR'][2]}:        {sigma_needed_bear:.1f}σ  below current  "
      f"{'(unusual — fundamental event required)' if sigma_needed_bear > 1.5 else '(within 1-sigma range)'}")
print(f"  Volatility note:  China headline risk is the primary vol driver; can cause")
print(f"  -15% to -25% drawdowns on news alone, even without EPS revision.")

# ── ⑧  SCENARIO PROBABILITIES ────────────────────────────────────────────────
print(f"\n  ⑧  SCENARIO PROBABILITIES  (proxy model vs market-implied)")
print("  " + "─" * (W-2))
print(f"  {'Scenario':<8}  {'EPS':>6}  {'P/E':>5}  {'Price':>6}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>6}  Narrative")
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    sc  = SCENARIOS[k]
    eps_, pe_, price_, narr_ = sc
    pp  = proxy_probs[k]
    mp  = mkt_probs[k] if mkt_probs else 0
    print(f"  {k:<8}  ${eps_:>5.2f}  {pe_:>4}x  ${price_:>5}  {pp*100:>6.1f}%  {mp*100:>7.1f}%  {(pp-mp)*100:>+6.1f}pp  {narr_[:36]}")

print(f"\n  Proxy EV (2yr):      ${proxy_ev:.0f}")
print(f"  Market EV (implied): ${mkt_ev:.0f}  (what ${CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% hurdle requires)")
print(f"  Conservative EV:     ${cons_price_2yr:.0f}  (Method B; {CONS_EXIT_PE:.0f}x × ${CONS_EPS_2YR:.2f})")

print()
print("═" * W)
print(f"""  SUMMARY  /  INVESTMENT FRAMEWORK (May 2026 @ ${CURRENT_PRICE:.0f})

  The 2022 EPP trade (buying at $197 = 40x trough) has compounded at:
    Price return: +{(CURRENT_PRICE/EPP_2022_TROUGH_ACT - 1)*100:.0f}% from trough to today
    EPS return:   +{EPS_GROWTH_TOTAL*100:.0f}% of that came from real earnings growth

  Today's setup is DIFFERENT.  In 2022 you were buying AT the EPP floor.
  Today you are ${dist_to_epp:.0f} ({dist_to_epp/CURRENT_PRICE*100:.0f}%) ABOVE the updated EPP floor.

  The attractiveness ratio (Ratio B = {ratio_B:.2f}x) says:
    For every $1 of upside from conservative EPS growth, you are
    absorbing ${ratio_B:.2f} of floor gap risk.  That's not catastrophic —
    the business IS excellent — but it means you need BULL-case execution
    to earn the 15% hurdle rate from this entry.

  Best entry framework:
    →  Accumulate at ${epp_updated + (CURRENT_PRICE - epp_updated)*0.25:.0f}–${epp_updated + (CURRENT_PRICE - epp_updated)*0.45:.0f}  (Ratio B approaching 1.0x)
    →  Full position at ${epp_updated:.0f}–${epp_updated + 50:.0f}  (AT the EPP floor; 2022 style entry quality)
    →  China headline selloff is the most probable path to better entry""")
print("═" * W)
print()
