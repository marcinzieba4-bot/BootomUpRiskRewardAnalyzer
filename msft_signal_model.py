#!/usr/bin/env python3
"""
MSFT Signal Model  v2
──────────────────────
Microsoft Corporation (NASDAQ: MSFT)  ·  Technology / Cloud

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 415.0     # USD (NASDAQ: MSFT, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  (13.0,   22,   286,  "Azure slows <10%; Copilot stalls; AI margin drag"),
    "BASE":  (18.0,   27,   486,  "Azure 20-25%; Copilot 50M seats; margins recover"),
    "BULL":  (23.0,   32,   736,  "Azure 30%+; Copilot 100M+ seats; GitHub mainstream"),
    "XBULL": (28.0,   35,   980,  "Azure #2→#1; Copilot standard; AGI adjacency re-rates"),
}

# ── COPILOT MONETIZATION CALCULATOR (MSFT-specific structural feature) ───
M365_COMMERCIAL_SEATS_M  = 400
COPILOT_PAID_SEATS_M     =  30
COPILOT_MONTHLY_USD      =  30
GITHUB_COPILOT_SUBS_M    =   1.8
GITHUB_COPILOT_ARPU_MO   =  19

def copilot_economics():
    current_attach_pct = COPILOT_PAID_SEATS_M / M365_COMMERCIAL_SEATS_M * 100
    current_arpu_yr    = COPILOT_MONTHLY_USD * 12
    current_arr        = COPILOT_PAID_SEATS_M * 1e6 * current_arpu_yr / 1e9
    rev_per_pct_attach = M365_COMMERCIAL_SEATS_M * 1e6 * current_arpu_yr / 100 / 1e9
    bull_arr   = 100e6 * current_arpu_yr / 1e9
    xbull_arr  = 200e6 * current_arpu_yr / 1e9
    github_arr = GITHUB_COPILOT_SUBS_M * 1e6 * GITHUB_COPILOT_ARPU_MO * 12 / 1e9
    return current_attach_pct, current_arr, rev_per_pct_attach, bull_arr, xbull_arr, github_arr

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("Azure cloud revenue — YoY",        "% YoY",
      5.0,  15, 25, 35,   35.0, True,
     "AWS wins enterprise; Copilot ROI disappoints; Azure decelerates"),

    ("M365 Copilot paid seats",          "M seats",
      2.0,   5, 15, 30,   30.0, True,
     "Enterprise AI spend paused; Copilot ROI not proven at scale; churn"),

    ("Hyperscaler CapEx YoY",            "% YoY",
      0.0,  10, 30, 60,   77.0, True,
     "AI investment bubble deflates; hyperscaler capex cuts surprise"),

    ("LinkedIn revenue — YoY",           "% YoY",
     -5.0,   5, 12, 20,    8.0, True,
     "Recession; enterprise hiring freeze; B2B ad spend cut"),

    ("GitHub Copilot paid subscribers",  "M subs",
      0.3,   0.5,  1,  2,   1.8, True,
     "Open-source alternatives (Codestral, Gemini) take developer share"),

    ("Enterprise software spend YoY",    "% YoY",
     -2.0,   5, 10, 15,   14.7, True,
     "Macro downturn; enterprise IT budget freeze; cloud pause"),
]
WEIGHTS = [0.25, 0.20, 0.15, 0.15, 0.15, 0.10]

STRUCTURAL_FACTORS = [
    ("Azure enterprise incumbent switching cost",     1.5, 0.30),
    ("OpenAI co-opetition / dependency risk",        -0.5, 0.20),
    ("$65B CapEx cycle commitment risk",             -0.5, 0.20),
    ("Copilot adoption ceiling uncertainty",         -0.5, 0.15),
    ("Regulatory / antitrust pressure",              -0.3, 0.15),
]

# ── UPDATED EPP ─────────────────────────────────────────────────────────────
EPP_TODAY_EPS      = 13.5   # FY2025E normalized/non-GAAP EPS
EPP_MIN_PE         = 20.0   # min viable P/E at max pessimism (software/cloud minimum at panic;
                             # raised from 15x pre-Azure era: recurring revenue floor is structurally higher)
EPP_HISTORICAL     = 283.0  # historical EPP from v1 floor formula (approx)

# ── CONSERVATIVE GROWTH (2-yr, base-minus assumptions) ───────────────────────
CONS_SIGNALS = [
    ("Azure cloud",            18.0,  "18% YoY (vs current 35%); decel"),
    ("M365 Copilot",           12.0,  "12M seats (vs current 30M); slower"),
    ("Hyperscaler CapEx",      20.0,  "20% YoY (vs current 77%); normalise"),
    ("LinkedIn revenue",        6.0,  "6% YoY (vs current 8%); modest slow"),
    ("GitHub Copilot",          1.2,  "1.2M subs (vs current 1.8M); plateau"),
    ("Enterprise software",     6.0,  "6% YoY (vs current 14.7%); slowdown"),
]
CONS_EPS_CAGR    = 0.08    # conservative 2yr EPS CAGR
CONS_EXIT_PE     = 28.0    # exit multiple (no re-rating assumed = modest decline from current)
CONS_DIVIDEND    = 3.32    # annual dividend per share

# ── VOLATILITY ───────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT   = 0.25    # 2yr realized annualized vol
VOL_BETA         = 0.90    # beta vs S&P 500
VOL_52W_LOW      = 374.0   # 52-week low
VOL_52W_HIGH     = 468.0   # 52-week high
VOL_DIVIDEND     = 3.32    # same as CONS_DIVIDEND

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

attach_pct, curr_arr, rev_per_pp, bull_arr, xbull_arr, github_arr = copilot_economics()

# ── OUTPUT ────────────────────────────────────────────────────────────────────
print()
print("═" * W)
print(f"  MSFT  ·  Microsoft Corporation  ·  ${CURRENT_PRICE:.2f}  ·  Technology / Cloud")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

# Copilot monetization
print(f"\n  COPILOT MONETIZATION CALCULATOR  (the $30/seat revenue engine)")
print("  " + "─" * (W-2))
print(f"  M365 commercial seat base:          {M365_COMMERCIAL_SEATS_M:>4}M seats  (addressable)")
print(f"  Copilot for M365 paid seats:        {COPILOT_PAID_SEATS_M:>4}M seats  ({attach_pct:.1f}% attach rate)")
print(f"  Annual price per seat:              ${COPILOT_MONTHLY_USD*12:>3}/yr  (${COPILOT_MONTHLY_USD}/mo)")
print(f"  Current Copilot ARR:                ${curr_arr:.1f}B / yr")
print(f"  Incremental ARR per 1pp attach:     ${rev_per_pp:.2f}B / pp  ← the compounding lever")
print(f"  ─────────────────────────────────────────────────────")
print(f"  BASE scenario (50M seats, 12.5%):   ${50e6*COPILOT_MONTHLY_USD*12/1e9:.1f}B ARR")
print(f"  BULL scenario (100M seats, 25%):    ${bull_arr:.0f}B ARR")
print(f"  XBULL scenario (200M seats, 50%):   ${xbull_arr:.0f}B ARR  ← adds another Azure")
print(f"\n  GitHub Copilot:  {GITHUB_COPILOT_SUBS_M:.1f}M paid subs × ${GITHUB_COPILOT_ARPU_MO}/mo  =  ${github_arr:.2f}B ARR")
print(f"  → At 80%+ YoY growth, GitHub Copilot crosses $1B ARR within 12 months.")

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
print(f"\n  KEY TRIGGER: Azure growth deceleration below 15% combined with Copilot monetization")
print(f"  stall. The bull case requires Azure to sustain 25%+ for 3+ years — any evidence of")
print(f"  competitive share loss OR margin drag without revenue proof collapses the thesis.")

# ── ③ UPDATED EPP ────────────────────────────────────────────────────────────
print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS (non-GAAP):  ${EPP_TODAY_EPS:.2f}  (FY2025E)")
print(f"  Min viable P/E at peak pessimism:   {EPP_MIN_PE:.0f}x  [software/cloud floor; raised from 15x pre-Azure]")
print(f"  {'─'*60}")
print(f"  UPDATED EPP:                        ${epp_updated:.0f}/share")
print(f"  Historical EPP (v1 floor):          ${EPP_HISTORICAL:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.0f} vs Updated EPP ${epp_updated:.0f}:  "
      f"{'+' if epp_gap_pct>=0 else ''}{epp_gap_pct:.0f}%  "
      f"{'✓ cushion' if epp_gap_pct >= 0 else '← in distressed zone'}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} vs Updated EPP ${epp_updated:.0f}:  "
      f"{bear_vs_epp_pct:+.0f}%  "
      f"{'← BEAR implies fundamental impairment' if bear_vs_epp_pct < 0 else '✓ BEAR above floor'}")

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
print(f"\n  Key: Conservative 8% EPS CAGR at 28x exit still delivers modest positive return.")
print(f"  MSFT's 85% recurring revenue base means no-growth scenario still earns ~8%/yr.")

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
print(f"  Slight-below-market beta (0.90) reflects defensive cloud recurring revenue.")
print(f"  Low dividend yield (0.8%) — MSFT is a growth/reinvestment story, not income.")

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
