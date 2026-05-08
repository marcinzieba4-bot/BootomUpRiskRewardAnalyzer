#!/usr/bin/env python3
"""
Oracle Signal Model  v2
────────────────────────
Oracle Corporation (NYSE: ORCL)  ·  Enterprise Software / Cloud

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 175.0     # USD (NYSE: ORCL, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  ( 8.0,   18,   144,  "OCI growth stalls; OpenAI diversifies; $90B miss"),
    "BASE":  (11.0,   22,   242,  "OCI 50%+ to FY2027; $90B achieved; stable debt service"),
    "BULL":  (14.0,   25,   350,  "OCI 70%+; multicloud DB expands; 4th hyperscaler status"),
    "XBULL": (18.0,   28,   504,  "OCI = primary AI cloud; RPO converts; $100B+ run-rate"),
}

# ── RPO CONCENTRATION CALCULATOR (Oracle-specific structural feature) ────
TOTAL_RPO_B         = 553.0
OPENAI_RPO_B        = 300.0
OTHER_AI_RPO_B      =  83.0
TRADITIONAL_RPO_B   = 170.0
FY2026E_REVENUE_B   =  66.0
FY2027_TARGET_B     =  90.0
ANNUAL_RPO_BURN_PCT =  0.12

def rpo_analysis():
    openai_pct      = OPENAI_RPO_B / TOTAL_RPO_B
    ai_total_pct    = (OPENAI_RPO_B + OTHER_AI_RPO_B) / TOTAL_RPO_B
    annual_burn     = TOTAL_RPO_B * ANNUAL_RPO_BURN_PCT
    fy2027_gap      = FY2027_TARGET_B - FY2026E_REVENUE_B
    fy2027_growth   = (FY2027_TARGET_B / FY2026E_REVENUE_B - 1) * 100
    incremental_conv_needed = fy2027_gap / TOTAL_RPO_B
    return openai_pct, ai_total_pct, annual_burn, fy2027_gap, fy2027_growth, incremental_conv_needed

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("OCI / IaaS revenue YoY",           "% YoY",
     12.0,  20, 50, 75,   84.0, True,
     "Hyperscalers price OCI out; enterprise AI workloads route to AWS/Azure"),

    ("Oracle RPO — sequential change",   "$B/Q",
      2.0,   5, 15, 25,   30.0, True,
     "OpenAI diversifies cloud; new RPO signings dry up"),

    ("NVIDIA data center rev (qtly)",    "$B/Q",
      5.0,   8, 20, 35,   35.6, True,
     "AI capex pause; data center buildout freezes; OCI capacity idle"),

    ("Hyperscaler CapEx YoY",            "% YoY",
      5.0,  10, 30, 60,   77.0, True,
     "AI winter; cloud CapEx collapses; OCI demand destroyed"),

    ("Oracle multi-cloud DB YoY",        "% YoY",
     25.0,  50,150,400,  531.0, True,
     "AWS/Azure reject Oracle@Cloud agreements; multi-cloud growth halts"),

    ("Frontier AI CapEx signal",         "/4 scale",
      1.0,   1,  2,  4,    3.0, True,
     "OpenAI cuts OCI spend; frontier labs move compute in-house"),
]
WEIGHTS = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("Oracle DB ecosystem switching cost moat",       1.0, 0.25),
    ("OpenAI 54% RPO concentration risk",            -1.8, 0.30),
    ("~$95B net debt — financial flexibility",        -0.8, 0.20),
    ("$90B FY2027 target credibility risk",           -0.8, 0.15),
    ("10GW power delivery timeline risk",             -0.5, 0.10),
]

# ── UPDATED EPP ─────────────────────────────────────────────────────────────
EPP_TODAY_EPS    = 6.00    # FY2025E non-GAAP EPS
EPP_MIN_PE       = 18.0    # min viable P/E (DB subscription floor; OCI capex risk limits compression)
EPP_HISTORICAL   = 144.0   # historical EPP v1 (use bear scenario price as proxy; ORCL was not at panic in 2022)
EPP_REGIME_NOTE  = "(OCI secular demand + DB subscription moat raises panic floor from 12x to 18x)"

# ── CONSERVATIVE GROWTH (2-yr, base-minus assumptions) ───────────────────────
CONS_SIGNALS = [
    ("OCI / IaaS",             30.0, "+30%/yr (vs +84%; growth normalization)"),
    ("Oracle RPO",              8.0,  "$8B/Q (vs $30B/Q; no new mega deals)"),
    ("NVIDIA data",            20.0,  "$20B/Q (vs $35.6B; AI capex plateaus)"),
    ("Hyperscaler CapEx",      25.0,  "+25%/yr (vs +77%; capex normalization)"),
    ("Oracle multi-cloud",     80.0,  "+80%/yr (vs +531%; base effect cools)"),
    ("Frontier AI",             2.0,  "2.0/4 (vs 3.0; mixed frontier signals)"),
]
CONS_EPS_CAGR    = 0.08    # 8%/yr conservative (vs consensus 15%+)
CONS_EXIT_PE     = 20.0    # 20x exit (de-rate from current 29x; OCI slowdown)
CONS_DIVIDEND    = 1.60    # $1.60/yr dividend

# ── VOLATILITY ───────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT   = 0.30    # moderate vol
VOL_BETA         = 1.05    # ~market beta
VOL_52W_LOW      = 140.0   # approx
VOL_52W_HIGH     = 198.0   # approx
VOL_DIVIDEND     = 1.60

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

def market_implied_composite(target_ev, tolerance=1.0):
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

openai_pct, ai_total_pct, annual_burn, fy2027_gap, fy2027_growth, incr_conv = rpo_analysis()

# ── OUTPUT ────────────────────────────────────────────────────────────────────
print()
print("═" * W)
print(f"  ORCL  ·  Oracle Corporation  ·  ${CURRENT_PRICE:.2f}  ·  Enterprise Software / Cloud")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

# RPO concentration analysis
print(f"\n  RPO CONCENTRATION ANALYSIS  (the structural risk and opportunity)")
print("  " + "─" * (W-2))
print(f"  Total RPO (Q3 FY2026):                      ${TOTAL_RPO_B:>7.0f}B")
print(f"  ├─ OpenAI (est.):          ${OPENAI_RPO_B:.0f}B  ({openai_pct*100:.0f}% of total) ← concentration risk")
print(f"  ├─ Other AI customers:      ${OTHER_AI_RPO_B:.0f}B  ({OTHER_AI_RPO_B/TOTAL_RPO_B*100:.0f}% of total)")
print(f"  └─ Traditional cloud/apps: ${TRADITIONAL_RPO_B:.0f}B  ({TRADITIONAL_RPO_B/TOTAL_RPO_B*100:.0f}% of total)")
print(f"  AI as % of total RPO:                       {ai_total_pct*100:.0f}%")
print()
print(f"  FY2027 revenue target:                      ${FY2027_TARGET_B:.0f}B  (+{fy2027_growth:.0f}% vs FY2026E)")
print(f"  FY2026E revenue:                            ${FY2026E_REVENUE_B:.0f}B")
print(f"  Incremental revenue needed in FY2027:       ${fy2027_gap:.0f}B")
print(f"  % of total RPO that must convert (incr.):  {incr_conv*100:.1f}%  of $553B")
print(f"  Estimated annual RPO burn rate (~{ANNUAL_RPO_BURN_PCT*100:.0f}%):      ${annual_burn:.0f}B / yr")

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
print(f"\n  KEY TRIGGER: OCI growth slows to <30% (hyperscalers route AI workloads to AWS/Azure)")
print(f"  + OpenAI diversifies away from MSFT/ORCL cloud. The $90B RPO story breaks; investors")
print(f"  realize contracted backlog was one customer concentrated.")

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
print(f"  At {CONS_EXIT_PE:.0f}x P/E (conservative):  ${cons_price_2yr:.0f}/share")
if CONS_DIVIDEND > 0:
    print(f"  + Cumul. dividends (2yr):  +${cons_div_2yr:.2f}/share  (${CONS_DIVIDEND:.2f} growing 3%/yr)")
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:    ${cons_price_2yr:.0f}  "
      f"({'▲' if cons_price_2yr > CURRENT_PRICE else '▼'}{abs(cons_price_2yr - CURRENT_PRICE):.0f} "
      f"from ${CURRENT_PRICE:.0f})")
print(f"  Conservative total return: {cons_total_ret:+.0f}% over 2yr  "
      f"= {cons_annual_ret:+.0f}%/yr  (incl. dividend)")
print(f"\n  Oracle's DB subscription base provides a hard floor — ~20M installed databases create")
print(f"  mandatory maintenance/cloud migration revenue. Conservative EPS at 20x still implies")
print(f"  ~${cons_price_2yr:.0f} in 2yr, leaving limited margin of safety at ${CURRENT_PRICE:.0f} entry.")

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
print(f"  Near-market beta ({VOL_BETA:.2f}) with concentrated RPO risk — vol spikes on any OpenAI news.")
print(f"  Dividend (${VOL_DIVIDEND:.2f}/yr, {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}% yield) provides minimal cushion vs {VOL_ANNUAL_PCT*100:.0f}% annual vol.")

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
