#!/usr/bin/env python3
"""
SAP Signal Model  v2
──────────────────────
SAP SE (NYSE: SAP)  ·  Enterprise Software
Trough year: 2022 (rate-shock; enterprise software de-rate)

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 181.79
REQUIRED_RETURN  = 0.15
HORIZON_YEARS    = 2
EUR_USD          = 1.12

SCENARIOS = {
    "BEAR":  ( 6.0,  18,  108, "Cloud decelerates to 10%; Joule fails; migration stalls"),
    "BASE":  ( 9.0,  25,  225, "Cloud 23-25%; ECC wave executes; Joule 10%+ adoption"),
    "BULL":  (12.0,  30,  360, "Cloud 30%+; Joule monetisation begins; buyback accretive"),
    "XBULL": (15.0,  35,  525, "ECC surge + Joule premium pricing + EUR/USD tailwind"),
}

# ── STRUCTURAL DEMAND CALCULATOR (SAP-specific) ───────────────────────────────
ECC_TOTAL_CUSTOMERS     = 35_000
ECC_MIGRATED_PCT        = 0.39
ECC_ACTIVE_PROJECTS_PCT = 0.25
AVG_MIGRATION_ACV_EUR_M = 0.8
ECC_MAINSTREAM_END      = 2027

def migration_pipeline():
    remaining     = ECC_TOTAL_CUSTOMERS * (1 - ECC_MIGRATED_PCT)
    active        = remaining * ECC_ACTIVE_PROJECTS_PCT
    uncommitted   = remaining * (1 - ECC_ACTIVE_PROJECTS_PCT)
    active_acv    = active * AVG_MIGRATION_ACV_EUR_M / 1000
    potential_acv = uncommitted * AVG_MIGRATION_ACV_EUR_M / 1000
    return remaining, active, uncommitted, active_acv, potential_acv

# ── SIGNALS ───────────────────────────────────────────────────────────────────
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("ServiceNow rev growth YoY",      "% YoY",
      4.0,  10.0,  15.0,  25.0,  22.0, True,
     "Enterprise IT freeze; ServiceNow/SAP budgets cut together"),

    ("SAP cloud backlog growth CC",    "% CC",
      5.0,  10.0,  20.0,  30.0,  25.0, True,
     "ECC migration stalls; customers defer cloud contract signing"),

    ("ECC migration urgency",          "/4 scale",
      1.0,   1.0,   2.0,   4.0,   3.0, True,
     "ECC deadline extended again; urgency collapses; migrations pause"),

    ("Enterprise software spend YoY",  "% YoY",
      0.0,   5.0,  10.0,  15.0,  14.7, True,
     "IT budget freeze; CIOs defer ERP renewal to protect cash"),

    ("EUR/USD rate (inverse)",         "EUR/USD",
      1.30,  1.05,  1.10,  1.20,   1.12, False,
     "EUR surges >1.30; USD EPS compressed 10pp vs CC growth"),

    ("Joule AI production adoption",   "%",
      0.5,   1.0,   5.0,  15.0,   3.0, True,
     "Enterprise AI budgets shift to OpenAI/Copilot; Joule loses pilots"),
]
WEIGHTS = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("ECC 2027 deadline — captive 21K pipeline",      1.5, 0.30),
    ("EUR/USD structural reporting headwind",         -0.5, 0.20),
    ("Joule monetisation timeline uncertainty",       -0.8, 0.20),
    ("S/4HANA migration complexity discount",         -0.5, 0.15),
    ("86% ARR-quality revenue base resilience",        0.8, 0.15),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
EPP_TODAY_EPS    = 9.00    # FY2025E non-GAAP EPS in USD (~EUR 8.0 × 1.12 EUR/USD)
EPP_MIN_PE       = 18.0    # min viable P/E at maximum pessimism (enterprise ERP floor;
                           # raised from 12x: SaaS transition raises defensibility of revenue)
EPP_HISTORICAL   = 150.0   # historical EPP v1 (approx)

# ── CONSERVATIVE GROWTH (2-yr, base-minus) ───────────────────────────────────
CONS_SIGNALS = [
    ("ServiceNow rev growth",   12.0, "+12%/yr (vs +22%; enterprise IT spending slows)"),
    ("SAP cloud backlog",       10.0, "+10% CC (vs +25%; migration pace decelerates)"),
    ("ECC migration",            2.0, "Score 2/4 (vs 3; urgency builds but slowly)"),
    ("Enterprise software",      5.0, "+5% (vs +15%; IT budgets flat in slowdown)"),
    ("EUR/USD rate",             1.10, "1.10 (vs 1.12; modest EUR strengthening)"),
    ("Joule AI",                 2.0, "2% adoption (vs 3%; monetisation still early)"),
]
CONS_EPS_CAGR = 0.10     # 10%/yr conservative (vs consensus 15%+)
CONS_EXIT_PE  = 22.0     # 22x exit (de-rate from current ~25x)
CONS_DIVIDEND = 2.20     # approx $2.20 USD (~EUR 2.00 dividend)

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.22    # 2yr realized annualized vol
VOL_BETA       = 0.75    # beta vs S&P 500
VOL_52W_LOW    = 158.58  # 52-week low
VOL_52W_HIGH   = 313.28  # 52-week high
VOL_DIVIDEND   = 2.20

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
print(f"  SAP  ·  SAP SE  ·  ${CURRENT_PRICE:.2f}  ·  Enterprise Software")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

# ── ① SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print(f"\n  ① SIGNAL DASHBOARD")
print(f"  {'Signal':<32}  {'BEAR':>7}  {'BASE≥':>7}  {'BULL≥':>7}  {'XBULL≥':>7}  {'NOW':>8}  Score")
print("  " + "─" * (W-2))
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u = unit.split()[0] if unit else ""
    bv_s  = f"{bv:+.0f}{u}" if hib else f">{bv:.1f}{u}"
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
print(f"\n  KEY TRIGGER: Cloud backlog deceleration to <10% CC + Joule AI fails enterprise")
print(f"  adoption → SAP loses transformation premium, re-rates to 18x on stable-but-")
print(f"  not-growing ECC maintenance business. JOINT event: each alone doesn't bear.")

# ── ③ UPDATED EPP ────────────────────────────────────────────────────────────
print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS:          ${EPP_TODAY_EPS:.2f}  (FY2025E non-GAAP, USD)")
print(f"  Min viable P/E at panic:          {EPP_MIN_PE:.0f}x  [enterprise ERP floor; raised from 12x: SaaS raises defensibility]")
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
print(f"\n  Even at conservative 10% EPS growth and 22x exit, SAP reaches ${cons_price_2yr:.0f} in 2yr.")
print(f"  The 21,000 ECC customers MUST migrate by 2027 — captive demand is the floor.")

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
print(f"  SAP's EUR-denominated earnings create FX vol overlay not captured in USD beta.")
print(f"  EUR/USD 1.30+ would compress USD EPS ~10pp vs CC growth — a tail risk for US holders.")

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
