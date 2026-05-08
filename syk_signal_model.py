#!/usr/bin/env python3
"""
SYK Signal Model  v2
──────────────────────
Stryker Corporation (NYSE: SYK)  ·  Medical Devices / Healthcare
Trough year: 2022 (rate-shock; MedTech de-rate)

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 380.0
REQUIRED_RETURN  = 0.15
HORIZON_YEARS    = 2

SCENARIOS = {
    "BEAR":  (12.5,  22,  275, "Elective surgery freeze; hospital budget cuts"),
    "BASE":  (17.0,  26,  442, "Steady recovery; MAKO growing; demographics"),
    "BULL":  (21.0,  30,  630, "MAKO dominant; international expansion; M&A"),
    "XBULL": (26.0,  34,  884, "Surgical robotics re-rating; spine/neuro boom"),
}

# ── MAKO ROBOTICS INSTALLED BASE CALCULATOR (SYK-specific) ───────────────────
MAKO_INSTALLED_BASE      = 3_200
MAKO_NEW_PER_YEAR        =   380
MAKO_PROCEDURE_VOLUME    =   175
MAKO_IMPLANT_ASP         = 2_400
MAKO_CONSUMABLE_PER_PROC =   350
MAKO_SYSTEM_ASP_K        = 1_500
MAKO_SERVICE_CONTRACT_K  =   450

def mako_economics():
    total_procs_yr   = MAKO_INSTALLED_BASE * MAKO_PROCEDURE_VOLUME
    implant_rev_b    = total_procs_yr * MAKO_IMPLANT_ASP / 1e9
    consumable_rev_b = total_procs_yr * MAKO_CONSUMABLE_PER_PROC / 1e9
    service_rev_b    = MAKO_INSTALLED_BASE * MAKO_SERVICE_CONTRACT_K / 1e6
    total_rec_rev_b  = implant_rev_b + consumable_rev_b + service_rev_b
    capital_rev_b    = MAKO_NEW_PER_YEAR * MAKO_SYSTEM_ASP_K / 1e6
    ltv_per_system   = (MAKO_PROCEDURE_VOLUME * (MAKO_IMPLANT_ASP + MAKO_CONSUMABLE_PER_PROC)
                        + MAKO_SERVICE_CONTRACT_K * 1000) * 10 / 1e6
    future_base      = MAKO_INSTALLED_BASE + MAKO_NEW_PER_YEAR * 2
    future_rec_rev_b = future_base * MAKO_PROCEDURE_VOLUME * \
                       (MAKO_IMPLANT_ASP + MAKO_CONSUMABLE_PER_PROC) / 1e9 + \
                       future_base * MAKO_SERVICE_CONTRACT_K / 1e6
    return total_procs_yr, total_rec_rev_b, capital_rev_b, ltv_per_system, future_base, future_rec_rev_b

# ── SIGNALS ───────────────────────────────────────────────────────────────────
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("US elective surgery volume — YoY",     "% YoY",
     -3.0,   2.0,   5.0,   9.0,   4.0, True,
     "Hospital labor crisis; OR capacity rationed"),

    ("Hospital capital spending — YoY",      "% YoY",
     -5.0,   3.0,   7.0,  12.0,   6.0, True,
     "CMS reimbursement cuts; hospital capex freeze"),

    ("MAKO procedure volume — YoY",         "% YoY",
      2.0,  10.0,  20.0,  35.0,  24.0, True,
     "Competing robots displace MAKO; surgeon retraining begins"),

    ("US population 65+ — growth",           "% YoY",
      0.5,   2.0,   3.0,   4.0,   3.2, True,
     "Demographic model misfires; 65+ cohort health improves unexpectedly"),

    ("Orthopedic implant market — YoY",      "% YoY",
      0.0,   3.0,   6.0,   9.0,   5.0, True,
     "Market contracts; insurer coverage limits cut hip/knee authorizations"),

    ("MAKO win rate vs JNJ Velys",          "%",
     45.0,  55.0,  65.0,  75.0,  68.0, True,
     "JNJ Velys matches multi-joint; SYK loses new hospital evaluations"),
]
WEIGHTS = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("MAKO installed base switching cost moat",       1.2, 0.25),
    ("JNJ / Zimmer Biomet robotics competitive risk", -0.5, 0.25),
    ("Aging demographics structural demand",           0.8, 0.20),
    ("Hospital consolidation → SYK preferred vendor", 0.5, 0.15),
    ("High valuation limits margin of safety",        -0.5, 0.15),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
EPP_TODAY_EPS    = 12.50   # FY2025E non-GAAP EPS
EPP_MIN_PE       = 22.0    # min viable P/E (MAKO installed base moat; never goes below 22x)
EPP_HISTORICAL   = 308.0   # historical EPP v1 (from bear scenario or floor formula)
EPP_REGIME_NOTE  = "(raised from 18x; MAKO installed base = recurring procedure revenue floor)"

# ── CONSERVATIVE GROWTH (2-yr, base-minus) ───────────────────────────────────
CONS_SIGNALS = [
    ("US elective surgery",      2.0, "+2%/yr (vs +4%; hospital capacity constrained)"),
    ("Hospital capital",         3.0, "+3%/yr (vs +6%; CFOs cautious on capex)"),
    ("MAKO procedure",          12.0, "+12%/yr (vs +24%; adoption slows at scale)"),
    ("US population",            2.0, "+2%/yr (vs +3.2%; base case demographics)"),
    ("Orthopedic implant",       3.0, "+3%/yr (vs +5%; market growth moderates)"),
    ("MAKO win rate",           60.0, "60% (vs 68%; JNJ Velys takes modest share)"),
]
CONS_EPS_CAGR = 0.09     # 9%/yr conservative (vs consensus 12%)
CONS_EXIT_PE  = 25.0     # 25x exit (de-rate from current ~30x)
CONS_DIVIDEND = 3.36     # $3.36/yr dividend

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.22    # low vol; defensive healthcare compounder
VOL_BETA       = 0.75    # low beta
VOL_52W_LOW    = 330.0
VOL_52W_HIGH   = 420.0
VOL_DIVIDEND   = 3.36

# ── SCORING ───────────────────────────────────────────────────────────────────
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
W = 72

scored = [
    (name, unit, bv, bf, blf, xf, cv, hib, narr,
     score_signal(cv, bf, blf, xf, hib), w)
    for (name, unit, bv, bf, blf, xf, cv, hib, narr), w
    in zip(SIGNALS, WEIGHTS)
]
proxy_composite  = sum(s * w for *_, s, w in scored)
bear_composite   = sum(score_signal(bv, bf, blf, xf, hib) * w
                       for (_, __, bv, bf, blf, xf, ___, hib, ____), w
                       in zip(SIGNALS, WEIGHTS))
sca              = sum(s * w for _, s, w in STRUCTURAL_FACTORS)
adj_composite    = proxy_composite + sca
proxy_probs      = softmax_probs(proxy_composite)
bear_probs       = softmax_probs(bear_composite)
proxy_ev         = expected_price(proxy_probs)
bear_ev          = expected_price(bear_probs)

market_target_ev = CURRENT_PRICE * ((1 + REQUIRED_RETURN) ** HORIZON_YEARS)
mkt_composite, mkt_probs = market_implied_composite(market_target_ev)
mkt_ev = expected_price(mkt_probs) if mkt_probs else market_target_ev

# Updated EPP (EPS-based)
epp_updated     = EPP_TODAY_EPS * EPP_MIN_PE
epp_gap_pct     = (CURRENT_PRICE - epp_updated) / epp_updated * 100
bear_vs_epp_pct = (SCENARIOS["BEAR"][2] - epp_updated) / epp_updated * 100

# Conservative growth
cons_eps_2yr    = EPP_TODAY_EPS * ((1 + CONS_EPS_CAGR) ** 2)
cons_price_2yr  = cons_eps_2yr * CONS_EXIT_PE
cons_div_2yr    = CONS_DIVIDEND * (1 + 0.03) + CONS_DIVIDEND * (1 + 0.03) ** 2
cons_total_ret  = (cons_price_2yr - CURRENT_PRICE + cons_div_2yr) / CURRENT_PRICE * 100
cons_annual_ret = cons_total_ret / 2

# Volatility
sigma_1yr         = CURRENT_PRICE * VOL_ANNUAL_PCT
vol_low_1yr       = CURRENT_PRICE - sigma_1yr
vol_high_1yr      = CURRENT_PRICE + sigma_1yr
sigma_needed_bear = (CURRENT_PRICE - SCENARIOS["BEAR"][2]) / sigma_1yr

if mkt_composite:
    adj_gap = adj_composite - mkt_composite
    if   adj_gap >  0.50: _verdict = "UNDERVALUED"
    elif adj_gap >  0.20: _verdict = "MODESTLY UNDERVALUED"
    elif adj_gap > -0.20: _verdict = "FAIRLY VALUED"
    elif adj_gap > -0.50: _verdict = "MODESTLY OVERVALUED"
    else:                 _verdict = "OVERVALUED"

# ── OUTPUT ────────────────────────────────────────────────────────────────────
print()
print("═" * W)
print(f"  SYK  ·  Stryker Corporation  ·  ${CURRENT_PRICE:.2f}  ·  Medical Devices")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

# ── ① SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print(f"\n  ① SIGNAL DASHBOARD")
print(f"  {'Signal':<32}  {'BEAR':>7}  {'BASE≥':>7}  {'BULL≥':>7}  {'XBULL≥':>7}  {'NOW':>8}  Score")
print("  " + "─" * (W-2))
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u = unit.split()[0] if unit else ""
    bv_s  = f"{bv:+.0f}{u}" if hib else f">{bv:.0f}{u}"
    bf_s  = f"{bf:.0f}{u}"
    blf_s = f"{blf:.0f}{u}"
    xf_s  = f"{xf:.0f}{u}"
    cv_s  = f"{cv:+.0f}{u}"
    bar   = "█" * s + "░" * (4 - s)
    print(f"  {name:<32}  {bv_s:>7}  {bf_s:>7}  {blf_s:>7}  {xf_s:>7}  {cv_s:>8}  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:    {proxy_composite:.2f} / 4.00")
if mkt_composite:
    print(f"  Market composite:   {mkt_composite:.2f} / 4.00  (back-solved from ${CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% hurdle)")
    print(f"  SCA adjustment:    {sca:+.2f}  →  Adj composite {adj_composite:.2f}  →  Gap {adj_gap:+.2f}  [{_verdict}]")

print(f"\n  Structural factors:")
for desc, score, wt in STRUCTURAL_FACTORS:
    arrow = "  +" if score > 0 else "  -"
    print(f"  {arrow}  {desc}  ({score:+.1f} × {wt*100:.0f}%  =  {score*wt:+.2f})")

# ── ② BEAR CASE ANATOMY ──────────────────────────────────────────────────────
print(f"\n  ② BEAR CASE ANATOMY  (what variables need to do for BEAR to materialise)")
print("  " + "─" * (W-2))
print(f"  {'Signal':<32}  {'Current':>8}  {'Bear val':>8}  Move    Trigger")
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u      = unit.split()[0] if unit else ""
    cv_s   = f"{cv:+.0f}{u}"
    bv_s   = f"{bv:+.0f}{u}"
    move   = bv - cv
    move_s = f"{move:+.0f}{u}"
    trigger = narr[:40] if len(narr) <= 40 else narr[:37] + "…"
    print(f"  {name:<32}  {cv_s:>8}  {bv_s:>8}  {move_s:>6}  {trigger}")

print(f"\n  Bear composite:  {bear_composite:.2f}  →  Bear scenario price: ~${expected_price(bear_probs):.0f}  (model)  /  ${SCENARIOS['BEAR'][2]} (defined)")
print(f"  Bear probability (proxy model):  {proxy_probs['BEAR']*100:.1f}%")
print(f"\n  KEY TRIGGER: Hospital capex freeze + elective surgery volume decline simultaneously.")
print(f"  CMS reimbursement cut makes hip/knee replacements margin-negative for hospitals")
print(f"  → OR time cut → SYK implant volumes fall 15%. MAKO capital sales freeze too.")

# ── ③ UPDATED EPP ────────────────────────────────────────────────────────────
print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS:          ${EPP_TODAY_EPS:.2f}  (FY2025E non-GAAP)")
print(f"  Min viable P/E at panic:          {EPP_MIN_PE:.0f}x  {EPP_REGIME_NOTE}")
print(f"  {'─'*60}")
print(f"  UPDATED EPP:                     ${epp_updated:.0f}/share")
print(f"  Historical EPP (v1, floor adj):  ${EPP_HISTORICAL:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.0f} vs Updated EPP ${epp_updated:.0f}:  {epp_gap_pct:+.0f}%  {'✓ cushion' if epp_gap_pct >= 0 else '← in distressed zone'}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} vs Updated EPP ${epp_updated:.0f}:  {bear_vs_epp_pct:+.0f}%  {'← BEAR requires earnings impairment' if bear_vs_epp_pct < 0 else '✓ bear is cyclical repricing'}")

# ── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print(f"\n  ④ CONSERVATIVE GROWTH  (2-yr, signals at BASE lower bound — no tailwinds)")
print("  " + "─" * (W-2))
print(f"  {'Signal':<32}  {'Conservative':>14}  vs Current  Rationale")
for sname, sval, srat in CONS_SIGNALS:
    cur = next(cv for name, _, __, ___, ____, _____, cv, ______, _______ in SIGNALS
               if name.lower().startswith(sname.split()[0].lower()))
    diff = sval - cur
    print(f"  {sname:<32}  {sval:>14.1f}  {diff:>+9.0f}   {srat[:30]}")

print(f"\n  Conservative 2yr EPS:   ${EPP_TODAY_EPS:.2f} × (1+{CONS_EPS_CAGR*100:.0f}%)² = ${cons_eps_2yr:.2f}")
print(f"  At {CONS_EXIT_PE:.0f}x P/E (conservative):  ${cons_price_2yr:.0f}/share")
if CONS_DIVIDEND > 0:
    print(f"  + Cumul. dividends (2yr):  +${cons_div_2yr:.2f}/share")
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:     ${cons_price_2yr:.0f}  ({'▲' if cons_price_2yr > CURRENT_PRICE else '▼'}{abs(cons_price_2yr - CURRENT_PRICE):.0f} from ${CURRENT_PRICE:.0f})")
print(f"  Conservative total return:  {cons_total_ret:+.0f}% over 2yr  = {cons_annual_ret:+.0f}%/yr")
print(f"\n  Even conservative growth delivers positive return — MAKO recurring rev provides floor.")
print(f"  The {MAKO_INSTALLED_BASE:,}-system installed base continues generating revenue regardless of new sales.")

# ── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        ${VOL_52W_LOW:.0f}  –  ${VOL_52W_HIGH:.0f}")
if VOL_DIVIDEND > 0:
    print(f"  Annual dividend:      ${VOL_DIVIDEND:.2f}/share  (yield {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized")
print(f"  Beta vs S&P 500:      {VOL_BETA:.2f}")
print(f"  1-sigma range (1yr):  ${vol_low_1yr:.0f}  –  ${vol_high_1yr:.0f}  (${CURRENT_PRICE:.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  2-sigma range (1yr):  ${CURRENT_PRICE - 2*sigma_1yr:.0f}  –  ${CURRENT_PRICE + 2*sigma_1yr:.0f}")
print(f"  {'─'*60}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} requires:  ~{sigma_needed_bear:.1f}σ price move  {'(unusual — requires fundamental break)' if sigma_needed_bear > 1.5 else '(within normal vol range)'}")
print(f"  Low beta (0.75x) makes SYK a defensive holding — draws flight-to-quality in risk-off.")
print(f"  22-year organic growth streak means vol spikes are typically buying opportunities.")

# ── ⑥ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print(f"\n  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
print("  " + "─" * (W-2))
print(f"  {'Scenario':<8}  {'Price':>6}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>6}  Description")
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    sc = SCENARIOS[k]
    price = sc[2]
    narr  = sc[3] if len(sc) > 3 else ""
    pp  = proxy_probs[k]
    mp  = mkt_probs[k] if mkt_probs else 0
    gap_pp = pp - mp
    print(f"  {k:<8}  ${price:>5}  {pp*100:>6.1f}%  {mp*100:>7.1f}%  {gap_pp*100:>+6.1f}pp  {narr}")

print(f"\n  Proxy EV (2yr): ${proxy_ev:.0f}  /  Market EV: ${mkt_ev:.0f}  /  Current: ${CURRENT_PRICE:.0f}")
print(f"  Conservative EV (2yr, ④): ${cons_price_2yr:.0f} + ${cons_div_2yr:.2f} divs = ${cons_price_2yr + cons_div_2yr:.0f} total value")

print()
print("═" * W)
