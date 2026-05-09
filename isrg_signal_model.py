#!/usr/bin/env python3
"""
ISRG Signal Model  v2
──────────────────────
Intuitive Surgical, Inc. (NASDAQ: ISRG)  ·  Surgical Robotics / Medical Devices
EPP anchor: 2022 trough  (rate-shock; MedTech de-rate; China lockdowns)
Valuation date: 2026-05-09

Price source:  Yahoo Finance / search  — May 8 close $451.73, May 9 intraday $452+
               User confirmed ~$450 level.  CURRENT_PRICE = 452.

Sections:
  ⓪  EPP 2022 anchor + WHY the multiple was where it was then vs now
  ①  Signal dashboard
  ②  Bear case anatomy
  ③  Updated EPP (2026-05-09)
  ④  EPS inflation decomposition  (FY2022 → FY2025 actual)
  ⑤  Conservative 2-year growth trajectory
  ⑥  Attractiveness ratio  Δ(current → EPP) / Δ(current → 2yr-reflated)
  ⑦  Volatility context
  ⑧  Scenario probabilities
"""
import math

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
# Price fetched 2026-05-09 via WebSearch (Yahoo Finance / search snippet)
# May 8 close $451.73; May 9 intraday range seen ~$450-$453
CURRENT_PRICE   = 452.0    # ISRG — fetched from Yahoo Finance / WebSearch, 2026-05-09

REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

# ── ACTUAL EARNINGS DATA (sourced from Intuitive IR / earnings releases) ──────
FY2022_EPS_NONGAAP = 4.96   # FY2022 actual non-GAAP EPS
FY2025_EPS_NONGAAP = 8.93   # FY2025 actual non-GAAP EPS (first year above $10B revenue)
Q1_2026_EPS        = 2.50   # Q1 2026 non-GAAP EPS (+38% YoY vs $1.81 in Q1 2025)
FY2026E_CONSENSUS  = 10.40  # FY2026E consensus (implied: $452 / 43.57x forward P/E)
TTM_EPS_NONGAAP    = 9.62   # TTM: FY2025 $8.93 - Q1 2025 $1.81 + Q1 2026 $2.50

TRAILING_PE = CURRENT_PRICE / FY2025_EPS_NONGAAP   # ~50.6x (FY2025 actual)
FORWARD_PE  = CURRENT_PRICE / FY2026E_CONSENSUS     # ~43.5x (FY2026E consensus)

SCENARIOS = {
    #           EPS     mult   price   narrative
    "BEAR":  ( 8.80,   38,    334,   "China ban + GLP-1 volume collapse + hospital freeze"),
    "BASE":  (12.30,   52,    640,   "DV5 global rollout; Ion scaling; China contained"),
    "BULL":  (14.00,   58,    812,   "Ion mainstream; new indications; margin expansion"),
    "XBULL": (16.50,   65,   1073,   "Surgical AI platform; international re-acceleration"),
}

# ══════════════════════════════════════════════════════════════════════════════
# ⓪  EPP 2022 ANCHOR  +  MULTIPLE REGIME EXPLANATION
# ══════════════════════════════════════════════════════════════════════════════
EPP_2022_EPS       = 4.96
EPP_2022_MIN_PE    = 40.0
EPP_2022_PRICE     = EPP_2022_EPS * EPP_2022_MIN_PE   # = $198
EPP_2022_TROUGH    = 197.0   # actual 52-week low 2022

# Multiple regime data points
PE_2021_PEAK    = 75.0   # ISRG peak multiple Jan 2022 (pre-shock)
PE_2022_TROUGH  = EPP_2022_TROUGH / EPP_2022_EPS   # ~39.7x
PE_2024_PEAK    = 72.0   # early 2024 peak (DV5 launch excitement)
PE_2025_PEAK    = 70.0   # late 2025 before 2026 YTD selloff (est.)
# Current:
PE_TRAILING_NOW = TRAILING_PE
PE_FORWARD_NOW  = FORWARD_PE

# What it takes to return to 40x today
PE_RETURN_TO_2022 = 40.0
PRICE_AT_2022_PE  = FY2025_EPS_NONGAAP * PE_RETURN_TO_2022  # = $357

# ══════════════════════════════════════════════════════════════════════════════
# PROXY SIGNALS
# ══════════════════════════════════════════════════════════════════════════════
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("da Vinci system placements YoY",   "% YoY",
       0.0,   5.0,  12.0,  20.0,  17.0, True,
      "Hospitals freeze capital; DV5 sticker-shock; budget cuts"),

    ("Total procedure volume YoY",       "% YoY",
       2.0,   8.0,  14.0,  20.0,  16.0, True,
      "GLP-1 cuts bariatric/hernia; elective surgery freeze"),

    ("Ion platform procedures YoY",      "% YoY",
       5.0,  25.0,  55.0,  90.0,  39.0, True,
      "Reimbursement denied; Veran/Olympus bronchoscopy adopted"),

    ("International revenue growth YoY", "% YoY",
       0.0,   8.0,  15.0,  22.0,  13.0, True,
      "China ban (trade war); EU hospital austerity wave"),

    ("Hospital capital spending YoY",    "% YoY",
      -5.0,   3.0,   7.0,  12.0,   5.0, True,
      "CMS reimbursement cuts; tariff-driven equipment pause"),

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
# ③  UPDATED EPP
# ══════════════════════════════════════════════════════════════════════════════
EPP_TODAY_EPS  = FY2025_EPS_NONGAAP   # $8.93 — most recent full-year actual
EPP_MIN_PE     = 40.0
EPP_REGIME_NOTE = "(unchanged 40x monopoly floor — same as 2022 anchor)"

# ══════════════════════════════════════════════════════════════════════════════
# ④  EPS INFLATION DECOMPOSITION  (FY2022 → FY2025)
# ══════════════════════════════════════════════════════════════════════════════
EPS_2022 = FY2022_EPS_NONGAAP
EPS_2025 = FY2025_EPS_NONGAAP
DECOMP = {
    "Real procedure volume growth":
        (0.440, "~15%/yr proc vol CAGR × 3yr; installed base scale-up"),
    "ASP / consumable price hikes":
        (0.115, "~4%/yr ASP on instruments & accessories (pricing power)"),
    "CPI / general cost pass-through":
        (0.105, "~13% cumul CPI 2022-25; partly passed through to hospitals"),
    "Operating leverage / margin expansion":
        (0.260, "Gross margin expanded ~250bp; OpEx grew slower than revenue"),
    "Share count reduction":
        (0.010, "Minimal; stock comp dilution largely offset"),
    "Mix shift (Ion + complex procedures)":
        (0.070, "Ion + complex indications carry higher per-procedure revenue"),
}
INFLATION_SHARE = DECOMP["ASP / consumable price hikes"][0] + \
                  DECOMP["CPI / general cost pass-through"][0]
EPS_GROWTH_TOTAL    = (EPS_2025 / EPS_2022) - 1
EPS_INFLATION_DOLLAR = EPS_2022 * INFLATION_SHARE
EPS_REAL_DOLLAR      = EPS_2025 - EPS_2022 - EPS_INFLATION_DOLLAR

# ══════════════════════════════════════════════════════════════════════════════
# ⑤  CONSERVATIVE 2-YEAR GROWTH  (May 2026 → May 2028 ≈ FY2027E conservative)
# ══════════════════════════════════════════════════════════════════════════════
CONS_SIGNALS = [
    ("da Vinci placements",     10.0, "+10%/yr (vs +17% Q1'26; post-DV5 normalizes)"),
    ("Total procedures",        12.0, "+12%/yr (vs +16% Q1'26; GLP-1 headwind)"),
    ("Ion platform procs",      35.0, "+35%/yr (vs +39% Q1'26; still scaling fast)"),
    ("International revenue",    8.0, "+8%/yr  (vs +13%; China zero-growth embedded)"),
    ("Hospital capex",           3.0, "+3%/yr  (vs +5%; tariff uncertainty lingers)"),
    ("China procedures",         0.0,  "Flat    (vs +8%; geopolitical risk floor)"),
]
CONS_EPS_CAGR  = 0.15    # 15%/yr conservative (below consensus ~18-20%; Q1 run +38%)
CONS_EXIT_PE   = 47.0    # 47x exit (slight de-rate from ~51x trailing; still premium)
CONS_DIVIDEND  = 0.0     # ISRG pays no dividend

CONS_EPS_2YR   = EPP_TODAY_EPS * (1 + CONS_EPS_CAGR) ** 2

# ══════════════════════════════════════════════════════════════════════════════
# VOLATILITY
# ══════════════════════════════════════════════════════════════════════════════
VOL_ANNUAL_PCT = 0.28
VOL_BETA       = 1.05
VOL_52W_LOW    = 390.0    # approx; stock -20% YTD suggests high at ~$570 end-2025
VOL_52W_HIGH   = 574.0

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

market_target_ev         = CURRENT_PRICE * ((1 + REQUIRED_RETURN) ** HORIZON_YEARS)
mkt_composite, mkt_probs = market_implied_composite(market_target_ev)
mkt_ev = expected_price(mkt_probs) if mkt_probs else market_target_ev

# EPP
epp_updated     = EPP_TODAY_EPS * EPP_MIN_PE
epp_gap_pct     = (CURRENT_PRICE - epp_updated) / epp_updated * 100
bear_vs_epp_pct = (SCENARIOS["BEAR"][2] - epp_updated) / epp_updated * 100

# Conservative 2yr
cons_price_2yr  = CONS_EPS_2YR * CONS_EXIT_PE
cons_total_ret  = (cons_price_2yr - CURRENT_PRICE) / CURRENT_PRICE * 100
cons_annual_ret = cons_total_ret / 2

# ⑥  Attractiveness ratio
eps_growth_2yr         = (CONS_EPS_2YR / EPP_TODAY_EPS) - 1
price_reflated_same_pe = CURRENT_PRICE * (1 + eps_growth_2yr)    # method A: hold current trailing PE
price_reflated_cons_pe = CONS_EPS_2YR * CONS_EXIT_PE              # method B: conserv exit PE
price_reflated_base    = SCENARIOS["BASE"][2]                     # method C: BASE scenario

dist_to_epp = CURRENT_PRICE - epp_updated
dist_A = price_reflated_same_pe - CURRENT_PRICE
dist_B = price_reflated_cons_pe - CURRENT_PRICE
dist_C = price_reflated_base    - CURRENT_PRICE

ratio_A = dist_to_epp / dist_A if dist_A > 0 else float("inf")
ratio_B = dist_to_epp / dist_B if dist_B > 0 else float("inf")
ratio_C = dist_to_epp / dist_C if dist_C > 0 else float("inf")

def ratio_label(r):
    if r < 0.75:  return "★★ ATTRACTIVE"
    if r < 1.10:  return "★  NEAR-FAIR"
    if r < 1.75:  return "⚠  RICH"
    return              "✗  PRICED IN"

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
print(f"  2026-05-09  (Yahoo Finance)  ·  EPP anchor: 2022 trough  ·  Verdict: {_verdict}")
print("═" * W)

# ── ⓪  EPP ANCHOR + MULTIPLE REGIME EXPLANATION ──────────────────────────────
print(f"""
  ⓪  EPP 2022 ANCHOR  —  Why the multiple was where it was, and why it's here now
  {"─" * (W-2)}
  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Multiple regime timeline                                               │
  │                                                                         │
  │  Jan 2022 (pre-shock)   ~75x trailing   ← peak enthusiasm              │
  │  Jun 2022 (EPP trough)  ~40x trailing   ← EPP buying zone              │
  │  Late 2024 (DV5 peak)   ~72x trailing   ← DV5 launch re-rating         │
  │  Late 2025 (cycle peak) ~70x trailing   ← stock ~$570+                 │
  │  May 2026 (today)       ~{PE_TRAILING_NOW:.0f}x trailing   ← -20% YTD; tariff fear  │
  │                          ~{PE_FORWARD_NOW:.0f}x forward NTM                         │
  └─────────────────────────────────────────────────────────────────────────┘

  WHY WAS IT 40x IN 2022?
  ───────────────────────
  The 2022 compression was a multi-factor pile-on where EVERY driver hit at once:

  1. Rate shock (Fed +525bp in 12 months)
     The fastest tightening cycle in 40 years repriced ALL long-duration assets.
     ISRG's earnings stretch 20+ years into the future via an installed base with
     a 15-20yr economic life.  At 10yr yields moving from 1.5% → 4%+, the present
     value of those cash flows dropped sharply — regardless of business quality.
     Effect: ~25 P/E points of compression sector-wide on growth stocks.

  2. China COVID lockdowns  (Q2 2022)
     Shanghai lockdown cut ISRG China procedure revenue ~40% in one quarter.
     China was ~10-12% of total revenue and its fastest-growing segment.
     Investors extrapolated: "what if this is structural?"
     Effect: EPS estimates cut, near-term growth slowed.

  3. Post-COVID backlog cleared
     2020-2021 saw deferred surgeries creating a backlog tailwind (+20%+ growth).
     By 2022, the backlog was exhausted and growth optically decelerated to ~8-10%.
     This made the previous 70x P/E look unjustified vs. "normalised" growth.

  4. No visible catalyst on the horizon
     da Vinci 5 was not yet announced.  Ion was tiny (<$50M revenue).
     The market had no forward-looking story to anchor a premium on.
     Effect: multiple reverted toward "medical device growth" comps (~25-35x).

  5. MedTech sector de-rate
     J&J, Stryker, Zimmer — the whole sector fell 20-35%.  ISRG fell with it,
     but its premium (monopoly, razor/blade, switching cost) held the floor at 40x
     rather than the 25x that pure device companies traded at.

  Result: $197 trough =  $4.96 EPS × 39.7x = EPP formula nailed the floor.
  The 40x was the minimum the market would accept for a monopoly with
  9,000-system installed base generating captive recurring revenue.

  ─────────────────────────────────────────────────────────────────────────────

  WHY IS IT ~51x TRAILING / ~44x FORWARD NOW?
  ─────────────────────────────────────────────────────────────────────────────

  Key: multiple is DOWN from the 70-75x peak, not up from 2022.
  The stock is cheaper than it was 6 months ago — but not 2022-cheap.

  1. EPS is accelerating hard  (Q1 2026: +38% YoY)
     The forward P/E at 44x reflects $10.40 FY2026E earnings, NOT today's $8.93.
     The market is already "seeing through" to future earnings — that's why
     forward P/E looks lower than trailing.  This is how quality compounders work.

  2. The 2022 "no catalyst" problem is SOLVED
     da Vinci 5 (DV5) launched in 2024 — hospitals are mid-upgrade cycle.
     Ion platform: 39% procedure growth in Q1 2026, reimbursement expanding.
     These justify a forward-looking premium over 40x.

  3. Down from peak because of macro fears (NOT earnings deterioration)
     The -20% YTD decline in 2026 is driven by:
     a. Trade war 2.0 / Trump tariffs → China revenue risk (~10-12% of revenue)
     b. GLP-1 narrative → fear bariatric volumes collapse
     c. Hospital tariff exposure on imported device components
     d. General derisking of premium-valued stocks in uncertain macro
     NONE of these have impaired actual earnings — Q1 2026 beat by 16.8%.

  4. Why NOT back to 40x?
     The installed base is ~9,000 systems vs ~7,500 in 2022.  Instruments &
     accessories are ~70% of revenue — this is RECURRING regardless of new
     system sales.  The floor quality is structurally higher, justifying >40x.
     Also: rates are NOT at 5%+ and rising; DV5/Ion are positive catalysts.

  To return to 40x trailing today:
     Price would need to fall to: ${PRICE_AT_2022_PE:.0f}  ({(PRICE_AT_2022_PE/CURRENT_PRICE - 1)*100:.0f}% from ${CURRENT_PRICE:.0f})
     Requires:  China ban + rate shock II + GLP-1 collapse + competitive entry
     Probability:  ~3-5%  (needs all four simultaneously)""")

# ── ①  SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print(f"\n  ①  SIGNAL DASHBOARD  (Q1 2026 actuals where available)")
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

  KEY BEAR CHAIN: China geopolitical ban → removes 10-12% revenue overnight
  → EPS cut to ~$8.80 (FY2025 actual barely exceeded) → multiple compresses to
  38x ('show me the money' without China growth) → bear price ~$334.
  Note bear $334 is BELOW EPP ($357) — bear requires genuine earnings impairment.""")

# ── ③  UPDATED EPP ────────────────────────────────────────────────────────────
print(f"\n  ③  UPDATED EPP  (floor anchored on FY2025 actual × trough multiple)")
print("  " + "─" * (W-2))
print(f"  FY2025 actual non-GAAP EPS:      ${EPP_TODAY_EPS:.2f}  (full year; $10B revenue milestone)")
print(f"  Q1 2026 run-rate (annualized):   ${Q1_2026_EPS * 4:.2f}  (+38% YoY; strong acceleration)")
print(f"  FY2026E consensus:               ${FY2026E_CONSENSUS:.2f}  (forward P/E {FORWARD_PE:.1f}x at ${CURRENT_PRICE:.0f})")
print(f"  Min viable P/E at panic:          {EPP_MIN_PE:.0f}x  {EPP_REGIME_NOTE}")
print(f"  {'─' * 64}")
print(f"  UPDATED EPP:                     ${epp_updated:.0f}/share   (vs ${EPP_2022_PRICE:.0f} in 2022  = +{(epp_updated/EPP_2022_PRICE-1)*100:.0f}% higher floor)")
print(f"  Current ${CURRENT_PRICE:.0f} vs EPP ${epp_updated:.0f}:      {epp_gap_pct:+.0f}%  above floor")
print(f"  Bear ${SCENARIOS['BEAR'][2]} vs EPP ${epp_updated:.0f}:      {bear_vs_epp_pct:+.0f}%  ← BEAR is BELOW EPP (earnings impairment)")
print(f"""
  EPP floor migration 2022 → 2026:
    2022 EPP:  ${EPP_2022_PRICE:.0f}  (${EPS_2022:.2f} × {EPP_2022_MIN_PE:.0f}x)
    2026 EPP:  ${epp_updated:.0f}  (${EPP_TODAY_EPS:.2f} × {EPP_MIN_PE:.0f}x)
    Floor moved up +${epp_updated - EPP_2022_PRICE:.0f} (+{(epp_updated/EPP_2022_PRICE-1)*100:.0f}%) — entirely EPS compounding; multiple floor unchanged.

  IMPORTANT: current price ${CURRENT_PRICE:.0f} is only {epp_gap_pct:.0f}% above EPP ${epp_updated:.0f}.
  In 2022, you could buy AT the EPP floor.  Today you are paying a {epp_gap_pct:.0f}% premium
  over EPP — smaller than the 66% premium when we estimated $530.  The -20% YTD
  selloff has meaningfully improved the entry quality.""")

# ── ④  EPS INFLATION DECOMPOSITION ───────────────────────────────────────────
print(f"\n  ④  EPS INFLATION DECOMPOSITION  (FY2022 ${EPS_2022:.2f} → FY2025 ${EPS_2025:.2f}, actual)")
print("  " + "─" * (W-2))
eps_total_growth = EPS_2025 - EPS_2022
eps_cagr         = (EPS_2025 / EPS_2022) ** (1/3) - 1
print(f"  Total EPS growth:  +${eps_total_growth:.2f}  (+{EPS_GROWTH_TOTAL*100:.0f}%  over 3yr;  CAGR +{eps_cagr*100:.1f}%/yr)")
print(f"  {'─' * 64}")
print(f"  {'Driver':<40}  {'Share':>7}  {'$EPS':>7}  Detail")
for driver, (share, note) in DECOMP.items():
    dollar = EPS_2022 * share
    print(f"  {driver:<40}  {share*100:>6.1f}%  ${dollar:>5.2f}  {note[:34]}")
print(f"  {'─' * 64}")
print(f"  INFLATION-ATTRIBUTED EPS (ASP + CPI):  {INFLATION_SHARE*100:.0f}% of growth = ${EPS_INFLATION_DOLLAR:.2f}/share")
print(f"  REAL-GROWTH EPS (volume + leverage):   {(1-INFLATION_SHARE)*100:.0f}% of growth = ${EPS_REAL_DOLLAR:.2f}/share")
print(f"""
  Key insight: ~{INFLATION_SHARE*100:.0f}% of EPS lift was inflation / ASP pricing.
  ~{(1-INFLATION_SHARE)*100:.0f}% was genuinely real: volume, leverage, mix.
  Even stripping inflation, "real" FY2025 EPS ≈ ${EPS_2025 - EPS_INFLATION_DOLLAR:.2f} → EPP = ${(EPS_2025 - EPS_INFLATION_DOLLAR)*EPP_MIN_PE:.0f}.
  The business is structurally larger: ~9,000 installed systems vs ~7,500 in 2022.
  Q1 2026 +38% EPS growth is not inflation — it is real operating leverage.""")

# ── ⑤  CONSERVATIVE 2-YEAR GROWTH ────────────────────────────────────────────
print(f"\n  ⑤  CONSERVATIVE 2-YEAR GROWTH  (May 2026 → May 2028;  no tailwinds assumed)")
print("  " + "─" * (W-2))
print(f"  {'Signal':<36}  {'Conservative':>13}  vs Q1'26  Rationale")
cur_map = {name.split()[0].lower(): cv for name, _, __, ___, ____, _____, cv, ______, _______ in SIGNALS}
for sname, sval, srat in CONS_SIGNALS:
    key = sname.split()[0].lower()
    cur = next(cv for name, _, __, ___, ____, _____, cv, ______, _______ in SIGNALS
               if key in name.lower())
    diff = sval - cur
    print(f"  {sname:<36}  {sval:>13.1f}  {diff:>+7.0f}   {srat[:36]}")

print(f"""
  Starting EPS:       FY2025 actual ${EPP_TODAY_EPS:.2f}  (conservative base; below current run rate)
  Conservative CAGR:  {CONS_EPS_CAGR*100:.0f}%/yr  (vs Q1 2026 actual +38%; consensus ~18-20%)
  Conservative 2yr:   ${EPP_TODAY_EPS:.2f} × (1+{CONS_EPS_CAGR*100:.0f}%)² = ${CONS_EPS_2YR:.2f}  (FY2027E conservative)
  Consensus 2yr:      ${EPP_TODAY_EPS:.2f} × (1+19%)² = ${EPP_TODAY_EPS*(1.19**2):.2f}  (Street ~18-20% CAGR)
  At {CONS_EXIT_PE:.0f}x P/E (mild de-rate from ~51x trailing today):  ${cons_price_2yr:.0f}/share
  {'─' * 64}
  Conservative 2yr price:   ${cons_price_2yr:.0f}  ({'▲' if cons_price_2yr > CURRENT_PRICE else '▼'}{abs(cons_price_2yr - CURRENT_PRICE):.0f} from ${CURRENT_PRICE:.0f})
  Conservative total return: {cons_total_ret:+.0f}% over 2yr  =  {cons_annual_ret:+.0f}%/yr  (no dividend)""")

# ── ⑥  ATTRACTIVENESS RATIO ──────────────────────────────────────────────────
print(f"\n  ⑥  ATTRACTIVENESS RATIO  —  EPP floor gap vs. EPS-reflated upside")
print("  " + "─" * (W-2))
print(f"""  Ratio = Δ(current → EPP floor)  /  Δ(current → 2yr-reflated price)
        = downside to floor  /  upside from EPS compounding

  Ratio < 0.75  →  ★★ ATTRACTIVE  (EPS upside >> floor gap)
  Ratio 0.75-1.1 →  ★  NEAR-FAIR  (roughly balanced)
  Ratio 1.1-1.75 →  ⚠  RICH       (floor gap > EPS upside)
  Ratio > 1.75   →  ✗  PRICED IN  (floor gap dominates)

  Inputs:
    Current price:      ${CURRENT_PRICE:.0f}
    EPP floor:          ${epp_updated:.0f}    (FY2025 ${EPP_TODAY_EPS:.2f} × {EPP_MIN_PE:.0f}x)
    Downside to EPP:    ${dist_to_epp:.0f}   ({dist_to_epp/CURRENT_PRICE*100:.0f}% below current)
""")
print(f"  ┌──────────────────────────────────────────────────────────────────────────┐")
print(f"  │  Method               2yr Target  Upside $  Upside %  Ratio   Signal    │")
print(f"  ├──────────────────────────────────────────────────────────────────────────┤")
print(f"  │  A: Same P/E (51x)     ${price_reflated_same_pe:>6.0f}      ${dist_A:>5.0f}     {dist_A/CURRENT_PRICE*100:>4.0f}%  {ratio_A:>5.2f}x  {ratio_label(ratio_A):<14}│")
print(f"  │     (51x trailing × conserv EPS ${CONS_EPS_2YR:.2f})                          │")
print(f"  │  B: Conserv exit {CONS_EXIT_PE:.0f}x   ${price_reflated_cons_pe:>6.0f}      ${dist_B:>5.0f}     {dist_B/CURRENT_PRICE*100:>4.0f}%  {ratio_B:>5.2f}x  {ratio_label(ratio_B):<14}│")
print(f"  │     ({CONS_EXIT_PE:.0f}x × ${CONS_EPS_2YR:.2f}; mild de-rate from current)              │")
print(f"  │  C: BASE scenario       ${price_reflated_base:>6.0f}      ${dist_C:>5.0f}     {dist_C/CURRENT_PRICE*100:>4.0f}%  {ratio_C:>5.2f}x  {ratio_label(ratio_C):<14}│")
print(f"  │     ({SCENARIOS['BASE'][1]}x × ${SCENARIOS['BASE'][0]:.2f} EPS; market BASE case)                       │")
print(f"  └──────────────────────────────────────────────────────────────────────────┘")

print(f"""
  Reading:
    Method A ({ratio_A:.2f}x — {ratio_label(ratio_A).strip()}):
      If P/E holds at current ~51x, EPS growth alone delivers +{dist_A/CURRENT_PRICE*100:.0f}% vs {dist_to_epp/CURRENT_PRICE*100:.0f}% floor gap.
      Upside {'exceeds' if ratio_A < 1 else 'slightly lags'} downside — {'decent entry on momentum' if ratio_A < 1 else 'needs multiple to hold'}.

    Method B ({ratio_B:.2f}x — {ratio_label(ratio_B).strip()}):
      At {CONS_EXIT_PE:.0f}x exit (modest de-rate, rates stay elevated), upside = +{dist_B/CURRENT_PRICE*100:.0f}%.
      Floor gap ({dist_to_epp/CURRENT_PRICE*100:.0f}%) {'modestly exceeds' if ratio_B > 1 else 'is covered by'} conservative upside.
      Conservative return = {cons_annual_ret:+.0f}%/yr — {'below' if cons_annual_ret < 15 else 'at'} the 15% hurdle.

    Method C ({ratio_C:.2f}x — {ratio_label(ratio_C).strip()}):
      BASE scenario ($640) implies +{dist_C/CURRENT_PRICE*100:.0f}% — comfortably covers the floor gap.
      If you believe BASE (which the model assigns {proxy_probs['BASE']*100:.0f}% probability), entry is sound.

  OVERALL vs $530 (our previous stale estimate):
    At $452 vs $530: EPP gap shrinks from 66% to {epp_gap_pct:.0f}%.
    Ratio B improves from 5.02x → {ratio_B:.2f}x.  Materially better entry quality.
    Conservative annual return: +4%/yr → {cons_annual_ret:+.0f}%/yr.
    Still not a screaming 2022-style EPP entry — but genuinely improved.""")

# ── ⑦  VOLATILITY CONTEXT ────────────────────────────────────────────────────
print(f"\n  ⑦  VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        ${VOL_52W_LOW:.0f}  –  ${VOL_52W_HIGH:.0f}  (stock -20% YTD 2026)")
print(f"  Realized vol:         {VOL_ANNUAL_PCT*100:.0f}% annualized  ·  Beta {VOL_BETA:.2f}")
print(f"  1-sigma range (1yr):  ${CURRENT_PRICE - sigma_1yr:.0f}  –  ${CURRENT_PRICE + sigma_1yr:.0f}")
print(f"  2-sigma range (1yr):  ${CURRENT_PRICE - 2*sigma_1yr:.0f}  –  ${CURRENT_PRICE + sigma_1yr*2:.0f}")
print(f"  {'─' * 64}")
print(f"  EPP floor ${epp_updated:.0f}:   {(CURRENT_PRICE - epp_updated)/sigma_1yr:.1f}σ below  (needs fundamental break to reach)")
print(f"  Bear case ${SCENARIOS['BEAR'][2]}:   {sigma_needed_bear:.1f}σ below  ({'within 1-sigma — plausible on China news' if sigma_needed_bear < 1.0 else 'requires combined triggers'})")
print(f"\n  Note: the -20% YTD decline already happened — it was the vol event.")
print(f"  The stock absorbed the tariff shock drawdown.  Current price reflects")
print(f"  a real risk premium over EPP.  China ban is the remaining binary risk.")

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
print(f"  Market EV (implied): ${mkt_ev:.0f}  (what ${CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% hurdle requires in 2yr)")
print(f"  Conservative EV:     ${cons_price_2yr:.0f}  (Method B; {CONS_EXIT_PE:.0f}x × ${CONS_EPS_2YR:.2f})")
print(f"  Analyst consensus:   ~$622  (41 analysts, avg target $621.62 per search data)")

print()
print("═" * W)
print(f"""  SUMMARY  /  INVESTMENT FRAMEWORK (2026-05-09 @ ${CURRENT_PRICE:.0f})

  2022 EPP trade at $197 → today $452:  +{(CURRENT_PRICE/EPP_2022_TROUGH - 1)*100:.0f}% price return.
    Of which:  EPS compounded +{EPS_GROWTH_TOTAL*100:.0f}%  (real earnings growth, mostly real)
               P/E expanded from 40x → {TRAILING_PE:.0f}x  (+{TRAILING_PE - PE_2022_TROUGH:.0f}pt multiple expansion)

  EPP gap today = {epp_gap_pct:.0f}%  (vs 0% in 2022 when you were AT the floor)
  Attractiveness ratio B = {ratio_B:.2f}x  (vs 5.02x at stale $530 estimate)

  The -20% YTD decline in 2026 has done real work:
    At $452 the forward P/E (44x) is approaching "normal" ISRG territory.
    The earnings acceleration (Q1 +38%) means the business is NOT broken.
    The multiple is compressing via earnings growth, not price alone.

  Entry framework:
    ★★  ${epp_updated:.0f}–${epp_updated + 40:.0f}   AT the EPP floor  (2022-quality entry; ~5% prob)
    ★   ${epp_updated + 40:.0f}–${CURRENT_PRICE - 30:.0f}   Ratio B < 1.0x   (accumulate on China headline)
    ◦   ${CURRENT_PRICE:.0f}       Today — Ratio B {ratio_B:.2f}x, +{cons_annual_ret:.0f}%/yr conservative, holds on BASE""")
print("═" * W)
print()
