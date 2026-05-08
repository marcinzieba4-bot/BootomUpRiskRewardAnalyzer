#!/usr/bin/env python3
"""
PM Signal Model  v2
──────────────────
Philip Morris International Inc. (NYSE: PM)  ·  Consumer Staples

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 175.0     # USD (NYSE: PM, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  ( 7.0,   13,    91,  "Regulatory setback; IQOS stall; ZYN FDA issue"),
    "BASE":  ( 9.0,   18,   162,  "Steady transformation; ZYN 50% share; IQOS 45M"),
    "BULL":  (11.5,   22,   253,  "IQOS 55M users; ZYN US #1; multiple re-rates"),
    "XBULL": (14.0,   25,   350,  "Full transformation; PM = smoke-free standard globally"),
}

# ── IQOS USER ECONOMICS CALCULATOR (PM-specific structural feature) ───────
IQOS_REGISTERED_USERS_M      = 40.0
HTU_ANNUAL_REV_PER_USER_USD   = 280
HTU_GROSS_MARGIN              = 0.70
COMBUSTIBLE_REV_PER_USER_USD  = 190
COMBUSTIBLE_GROSS_MARGIN      = 0.65
IQOS_DEVICE_ASP               = 95
IQOS_DEVICE_REPLACE_YRS       = 3

ZYN_US_SHIPMENTS_M_TINS       = 700
ZYN_NET_REV_PER_TIN           = 3.80
ZYN_GROSS_MARGIN              = 0.60
ZYN_GROWTH_YOY                = 0.40

def iqos_economics():
    rev_uplift_per_user  = HTU_ANNUAL_REV_PER_USER_USD - COMBUSTIBLE_REV_PER_USER_USD
    device_rev_annual    = IQOS_DEVICE_ASP / IQOS_DEVICE_REPLACE_YRS
    iqos_gp_per_user     = HTU_ANNUAL_REV_PER_USER_USD * HTU_GROSS_MARGIN + device_rev_annual
    comb_gp_per_user     = COMBUSTIBLE_REV_PER_USER_USD * COMBUSTIBLE_GROSS_MARGIN
    gp_uplift_per_user   = iqos_gp_per_user - comb_gp_per_user
    total_rev_uplift_b   = IQOS_REGISTERED_USERS_M * rev_uplift_per_user / 1000
    total_gp_uplift_b    = IQOS_REGISTERED_USERS_M * gp_uplift_per_user  / 1000
    zyn_rev_b            = ZYN_US_SHIPMENTS_M_TINS * ZYN_NET_REV_PER_TIN / 1000
    zyn_gp_b             = zyn_rev_b * ZYN_GROSS_MARGIN
    future_iqos_m        = IQOS_REGISTERED_USERS_M * (1.15 ** 2)
    future_zyn_rev_b     = zyn_rev_b * (1 + ZYN_GROWTH_YOY) ** 2
    return (rev_uplift_per_user, device_rev_annual, gp_uplift_per_user,
            total_rev_uplift_b, total_gp_uplift_b,
            zyn_rev_b, zyn_gp_b, future_iqos_m, future_zyn_rev_b)

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("IQOS registered user growth — YoY",   "% YoY",
      3.0,   8, 15, 25,   15.0, True,
     "FDA bans IQOS in key market; HTU volumes collapse"),

    ("ZYN US shipment volume — YoY",        "% YoY",
      5.0,  15, 35, 55,   40.0, True,
     "FDA issues marketing denial; ZYN pulled from US"),

    ("Smoke-free gross profit mix",         "%",
     30.0,  40, 50, 65,   52.0, True,
     "Combustible decline accelerates; SF margin squeeze"),

    ("HTU (heated tobacco unit) vol — YoY", "% YoY",
      2.0,   8, 15, 25,   18.0, True,
     "Competitor device gains share; IQOS ecosystem leaks"),

    ("Combustible volume decline",          "% YoY",
     -9.0,  -6, -3, -1,   -4.0, True,
     "Excise shock or illicit trade surge; volumes collapse"),

    ("Regulatory authorisation depth (IQOS)", "/4",
      1.5,   2,  3,  4,    3.2, True,
     "FDA reverses MRTP authorization; regulatory setback"),
]
WEIGHTS = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("IQOS device + ecosystem user switching cost",   1.2, 0.25),
    ("Regulatory re-classification / ban risk",      -0.8, 0.25),
    ("Combustible secular terminal decline risk",    -0.5, 0.20),
    ("HTU pricing premium / excise architecture",     0.8, 0.15),
    ("Swedish Match debt ($16B acquisition)",        -0.3, 0.15),
]

# ── UPDATED EPP ─────────────────────────────────────────────────────────────
# If maximum pessimism struck TODAY, what would the stock price be?
# Method: today's normalized EPS × minimum viable P/E at peak panic
EPP_TODAY_EPS      = 7.50   # FY2025E normalized/non-GAAP EPS
EPP_MIN_PE         = 13.0   # min viable P/E at max pessimism (smoke-free regime: raised from 10x combustible-only)
EPP_HISTORICAL     = 113.0  # historical EPP from v1 floor formula (approx)
EPP_REGIME_NOTE    = "(raised from 10x 2015-era floor; smoke-free mix justifies higher panic floor)"

# ── CONSERVATIVE GROWTH (2-yr, base-minus assumptions) ───────────────────────
CONS_SIGNALS = [
    ("IQOS registered",    10.0,  "+10%/yr (vs 15%; scaling at 40M base)"),
    ("ZYN US shipment",    20.0,  "+20%/yr (vs 40%; shelf space + FDA risk)"),
    ("Smoke-free gross",   48.0,  "48% (vs 52%; SF gains vs combustible math)"),
    ("HTU (heated",        10.0,  "+10% (vs 18%; maturing user base)"),
    ("Combustible volume", -5.0,  "-5%/yr (vs -4%; slightly worse)"),
    ("Regulatory authorisation",     3.0,  "3.0/4 (no new MRTP grants in 2yr)"),
]
CONS_EPS_CAGR    = 0.07    # 7%/yr conservative (vs consensus 10%+)
CONS_EXIT_PE     = 18.0    # modest de-rate from current 23x; market still values transformation
CONS_DIVIDEND    = 5.30    # $5.30/yr dividend (current, growing ~5%/yr)

# ── VOLATILITY ───────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT   = 0.18    # low vol; staples characteristic
VOL_BETA         = 0.60    # low beta; defensive income
VOL_52W_LOW      = 141.0   # approx
VOL_52W_HIGH     = 186.0   # approx
VOL_DIVIDEND     = 5.30

# ── SCORING ───────────────────────────────────────────────────────────────
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

def market_implied_composite(target_ev, tolerance=3.0):
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

# Updated EPP
epp_updated     = EPP_TODAY_EPS * EPP_MIN_PE
epp_gap_pct     = (CURRENT_PRICE - epp_updated) / epp_updated * 100
bear_vs_epp_pct = (SCENARIOS["BEAR"][2] - epp_updated) / epp_updated * 100

# Conservative growth
cons_eps_2yr    = EPP_TODAY_EPS * ((1 + CONS_EPS_CAGR) ** 2)
cons_price_2yr  = cons_eps_2yr * CONS_EXIT_PE
cons_div_2yr    = CONS_DIVIDEND * (1 + 0.02) + CONS_DIVIDEND * (1 + 0.02) ** 2
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

(rev_uplift, dev_rev_ann, gp_uplift, tot_rev_b, tot_gp_b,
 zyn_rev_b, zyn_gp_b, fut_iqos_m, fut_zyn_rev_b) = iqos_economics()

# ── OUTPUT ────────────────────────────────────────────────────────────────────
print()
print("═" * W)
print(f"  PM  ·  Philip Morris International  ·  ${CURRENT_PRICE:.2f}  ·  Consumer Staples")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

# IQOS user economics
print(f"\n  IQOS USER ECONOMICS  (the transformation revenue engine)")
print("  " + "─" * (W-2))
print(f"  Registered IQOS users globally:         {IQOS_REGISTERED_USERS_M:.0f}M")
print(f"  HTU net revenue per user per year:       ${HTU_ANNUAL_REV_PER_USER_USD}/yr")
print(f"  Combustible revenue per smoker per yr:   ${COMBUSTIBLE_REV_PER_USER_USD}/yr")
print(f"  Revenue uplift per converted user:       +${rev_uplift}/yr")
print(f"  Device revenue (annualised):             +${dev_rev_ann:.0f}/yr  (${IQOS_DEVICE_ASP} / {IQOS_DEVICE_REPLACE_YRS}-yr cycle)")
print(f"  Gross profit uplift per converted user:  +${gp_uplift:.0f}/yr  "
      f"(HTU {HTU_GROSS_MARGIN*100:.0f}% GM vs cig {COMBUSTIBLE_GROSS_MARGIN*100:.0f}% GM)")
print(f"  ─────────────────────────────────────────────────────")
print(f"  Total portfolio revenue uplift:          +${tot_rev_b:.1f}B / yr")
print(f"  Total gross profit uplift:               +${tot_gp_b:.1f}B / yr  ← incremental vs if all smoked")
print(f"\n  ZYN US Oral Nicotine:")
print(f"  Shipments FY2024:                        {ZYN_US_SHIPMENTS_M_TINS:.0f}M tins")
print(f"  Net revenue to PM:                       ${zyn_rev_b:.2f}B / yr  (@ ${ZYN_NET_REV_PER_TIN}/tin)")
print(f"  Gross profit:                            ${zyn_gp_b:.2f}B / yr  ({ZYN_GROSS_MARGIN*100:.0f}% GM)")
print(f"\n  2-year forward (at current growth rates):")
print(f"  IQOS users (15%/yr):                     {fut_iqos_m:.1f}M")
print(f"  ZYN US revenue (40%/yr):                 ${fut_zyn_rev_b:.2f}B / yr")
print(f"  → Smoke-free GP mix reaches ~60-65% by FY2027 — full multiple re-rating territory.")

# ── ① SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print(f"\n  ① SIGNAL DASHBOARD")
print(f"  {'Signal':<30}  {'BEAR':>7}  {'BASE≥':>7}  {'BULL≥':>7}  {'XBULL≥':>7}  {'NOW':>7}  Score")
print("  " + "─" * (W-2))
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u = unit.split()[0] if unit else ""
    bv_s  = f"{bv:+.0f}{u}"  if hib else f">{bv:.1f}{u}"
    bf_s  = f"{bf:.0f}{u}"
    blf_s = f"{blf:.0f}{u}"
    xf_s  = f"{xf:.0f}{u}"
    cv_s  = f"{cv:+.0f}{u}"
    bar   = "█" * s + "░" * (4 - s)
    print(f"  {name:<30}  {bv_s:>7}  {bf_s:>7}  {blf_s:>7}  {xf_s:>7}  {cv_s:>7}  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:    {proxy_composite:.2f} / 4.00")
if mkt_composite:
    print(f"  Market composite:   {mkt_composite:.2f} / 4.00  "
          f"(back-solved from ${CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% hurdle)")
    print(f"  SCA adjustment:    {sca:+.2f}  →  Adj composite {adj_composite:.2f}  "
          f"→  Gap {adj_gap:+.2f}  [{_verdict}]")

print(f"\n  Structural factors:")
for desc, score, wt in STRUCTURAL_FACTORS:
    arrow = "  +" if score > 0 else "  -"
    print(f"  {arrow}  {desc}  ({score:+.1f} × {wt*100:.0f}%  =  {score*wt:+.2f})")

# ── ② BEAR CASE ANATOMY ──────────────────────────────────────────────────────
print(f"\n  ② BEAR CASE ANATOMY  (what variables need to do for BEAR to materialise)")
print("  " + "─" * (W-2))
print(f"  {'Signal':<30}  {'Current':>8}  {'Bear val':>8}  Move    Trigger")
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u      = unit.split()[0] if unit else ""
    cv_s   = f"{cv:+.0f}{u}"
    bv_s   = f"{bv:+.0f}{u}"
    move   = bv - cv
    move_s = f"{move:+.0f}{u}"
    trigger = narr[:38] if len(narr) <= 38 else narr[:35] + "…"
    print(f"  {name:<30}  {cv_s:>8}  {bv_s:>8}  {move_s:>6}  {trigger}")

bear_model_price = expected_price(bear_probs)
print(f"\n  Bear composite:  {bear_composite:.2f}  →  Bear scenario price: "
      f"~${bear_model_price:.0f}  (model)  /  ${SCENARIOS['BEAR'][2]} (defined)")
print(f"  Bear probability (proxy model):  {proxy_probs['BEAR']*100:.1f}%")
print(f"\n  KEY TRIGGER: ZYN FDA action + IQOS regulatory rollback simultaneously destroys the transformation")
print(f"  thesis — PM becomes a pure declining combustible company repricing to 10-12x EPS.")

# ── ③ UPDATED EPP ────────────────────────────────────────────────────────────
print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS:          ${EPP_TODAY_EPS:.2f}  (FY2025E non-GAAP)")
print(f"  Min viable P/E at panic:          {EPP_MIN_PE:.0f}x  {EPP_REGIME_NOTE}")
print(f"  {'─'*60}")
print(f"  UPDATED EPP:                     ${epp_updated:.0f}/share")
print(f"  Historical EPP (v1, floor adj):  ${EPP_HISTORICAL:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.0f} vs Updated EPP ${epp_updated:.0f}:  {epp_gap_pct:+.0f}%  {'✓ cushion' if epp_gap_pct >= 0 else '← in distressed zone'}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} vs Updated EPP ${epp_updated:.0f}:  {bear_vs_epp_pct:+.0f}%  {'← BEAR requires earnings impairment' if bear_vs_epp_pct < 0 else '✓ bear is cyclical'}")

# ── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print(f"\n  ④ CONSERVATIVE GROWTH  (2-yr, signals at BASE lower bound — no tailwinds)")
print("  " + "─" * (W-2))
print(f"  {'Signal':<30}  {'Conservative':>14}  vs Current  Rationale")
for sname, sval, srat in CONS_SIGNALS:
    cur = next(cv for name, _, __, ___, ____, _____, cv, ______, _______ in SIGNALS
               if name.lower().startswith(sname.split()[0].lower()))
    diff = sval - cur
    diff_s = f"{diff:+.0f}"
    print(f"  {sname:<30}  {sval:>14.1f}  {diff_s:>9}   {srat[:30]}")

print(f"\n  Conservative 2yr EPS:   ${EPP_TODAY_EPS:.2f} × "
      f"(1+{CONS_EPS_CAGR*100:.0f}%)² = ${cons_eps_2yr:.2f}")
print(f"  At {CONS_EXIT_PE:.0f}x P/E (no multiple expansion):  ${cons_price_2yr:.0f}/share")
if CONS_DIVIDEND > 0:
    print(f"  + Cumul. dividends (2yr):  +${cons_div_2yr:.2f}/share  (${CONS_DIVIDEND:.2f} growing 2%/yr)")
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:    ${cons_price_2yr:.0f}  "
      f"({'▲' if cons_price_2yr > CURRENT_PRICE else '▼'}{abs(cons_price_2yr - CURRENT_PRICE):.0f} "
      f"from ${CURRENT_PRICE:.0f})")
print(f"  Conservative total return: {cons_total_ret:+.0f}% over 2yr  "
      f"= {cons_annual_ret:+.0f}%/yr  (incl. dividend)")
print(f"\n  Even at conservative EPS + modest multiple de-rate, dividend yield >3% provides return floor.")
print(f"  Transformation premium compression is the main risk.")

# ── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        ${VOL_52W_LOW:.0f}  –  ${VOL_52W_HIGH:.0f}")
if VOL_DIVIDEND > 0:
    print(f"  Annual dividend:      ${VOL_DIVIDEND:.2f}/share  "
          f"(yield {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%)")
else:
    print(f"  Dividend:             None")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized")
print(f"  Beta vs S&P 500:      {VOL_BETA:.2f}")
print(f"  1-sigma range (1yr):  ${vol_low_1yr:.0f}  –  ${vol_high_1yr:.0f}  "
      f"(${CURRENT_PRICE:.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  2-sigma range (1yr):  ${CURRENT_PRICE - 2*sigma_1yr:.0f}  –  "
      f"${CURRENT_PRICE + 2*sigma_1yr:.0f}")
print(f"  {'─'*60}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} requires:  "
      f"~{sigma_needed_bear:.1f}σ price move  "
      f"{'(unusual — requires fundamental break)' if sigma_needed_bear > 1.5 else '(within normal range)'}")
print(f"  PM is a low-volatility, high-dividend defensive — 18% annual vol reflects stable cash flows.")
print(f"  Bear scenario (${SCENARIOS['BEAR'][2]}) requires ~{sigma_needed_bear:.1f}σ move from current, highly unusual without a major regulatory shock.")

# ── ⑥ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print(f"\n  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
print("  " + "─" * (W-2))
print(f"  {'Scenario':<8}  {'Price':>6}  {'Proxy%':>7}  {'Market%':>8}  "
      f"{'Gap':>6}  Description")
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    eps, mult, price, narr = SCENARIOS[k]
    pp  = proxy_probs[k]
    mp  = mkt_probs[k] if mkt_probs else 0
    gap_pp = pp - mp
    print(f"  {k:<8}  ${price:>5}  {pp*100:>6.1f}%  {mp*100:>7.1f}%  "
          f"{gap_pp*100:>+6.1f}pp  {narr}")

print(f"\n  Proxy EV (2yr): ${proxy_ev:.0f}  /  Market EV: ${mkt_ev:.0f}  /  Current: ${CURRENT_PRICE:.0f}")
print(f"  Conservative EV (2yr, ④): ${cons_price_2yr:.0f} + ${cons_div_2yr:.2f} divs = "
      f"${cons_price_2yr + cons_div_2yr:.0f} total value")

print()
print("═" * W)
