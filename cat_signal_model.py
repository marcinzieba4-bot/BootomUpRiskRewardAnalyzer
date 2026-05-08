#!/usr/bin/env python3
"""
CAT Signal Model  v2
──────────────────────
Caterpillar Inc. (NYSE: CAT)  ·  Industrial / Construction Equipment
Trough year: 2020 (COVID / oil crash)

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 305.0
REQUIRED_RETURN  = 0.15
HORIZON_YEARS    = 2

SCENARIOS = {
    "BEAR":  (12.0,  14,  168, "Recession; construction -20%; mining bust; tariff hit"),
    "BASE":  (18.0,  17,  306, "Moderate recovery; infra steady; mining stable; restock"),
    "BULL":  (23.0,  19,  437, "Construction upcycle; copper boom; data center wave"),
    "XBULL": (28.0,  21,  588, "Full supercycle: infra + mining + energy transition + AI"),
}

# ── DEALER INVENTORY CYCLE CALCULATOR (CAT-specific) ─────────────────────────
DEALER_MONTHS_CURRENT   = 2.7
DEALER_MONTHS_NORMAL    = 3.0
DEALER_MONTHS_PEAK      = 4.2
REVENUE_PER_MONTH_SWING = 1_600
ANNUAL_RESTOCK_WINDOW   = 2

def dealer_cycle():
    vs_normal    = DEALER_MONTHS_CURRENT - DEALER_MONTHS_NORMAL
    restock_need = max(0, DEALER_MONTHS_NORMAL - DEALER_MONTHS_CURRENT)
    tailwind_m   = restock_need * REVENUE_PER_MONTH_SWING
    tailwind_ann = tailwind_m / ANNUAL_RESTOCK_WINDOW
    peak_headwind = (DEALER_MONTHS_PEAK - DEALER_MONTHS_CURRENT) * REVENUE_PER_MONTH_SWING
    return vs_normal, restock_need, tailwind_ann, peak_headwind

# ── SIGNALS ───────────────────────────────────────────────────────────────────
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("Architecture Billings Index",      "ABI",
     43.0,  49.0,  52.0,  56.0,  50.8, True,
     "Recession; architecture billings collapse; no new projects"),

    ("Copper price — YoY change",         "% YoY",
    -15.0,   0.0,  10.0,  20.0,   8.0, True,
     "Copper crash; mining CapEx canceled; Resource Industries frozen"),

    ("Global mining CapEx YoY",          "% YoY",
    -10.0,   5.0,  10.0,  18.0,  10.0, True,
     "Commodity downcycle; mine capex cut; CAT large equipment orders dry up"),

    ("Baker Hughes US rig count — YoY",  "% YoY",
    -20.0,  -5.0,   5.0,  15.0,  -3.0, True,
     "Oil price crash; E&P capex collapse; CAT energy segment evaporates"),

    ("CAT dealer inventory (months, inv)", "months",
      4.5,   3.5,   3.0,   2.5,   2.7, False,
     "Demand shock; dealers cancel orders; CAT production halted"),

    ("Data center construction YoY",     "% YoY",
      0.0,  15.0,  30.0,  55.0,  48.0, True,
     "AI capex pause; data center buildout stalls; power gen orders drop"),
]
WEIGHTS = [0.25, 0.20, 0.15, 0.15, 0.15, 0.10]

STRUCTURAL_FACTORS = [
    ("3,800-dealer global distribution moat",         0.8, 0.25),
    ("Steel / component tariff cost exposure",       -0.8, 0.30),
    ("Construction / mining cyclicality risk",       -0.5, 0.25),
    ("Data center power generation new TAM",          0.8, 0.10),
    ("Strong balance sheet net cash",                 0.5, 0.10),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
# CAT: EPS-based EPP is correct — no net debt complexity like pipelines.
# Trough P/E × today's normalized EPS = floor at maximum pessimism.
EPP_TODAY_EPS    = 18.00   # FY2025E non-GAAP EPS
EPP_MIN_PE       = 14.0    # min viable P/E (industrial trough multiple)
EPP_HISTORICAL   = 230.0   # historical EPP v1 (from floor formula, 2020 trough)
EPP_REGIME_NOTE  = "(trough P/E; construction/mining cycle trough; infra spending creates demand floor)"

# ── CONSERVATIVE GROWTH (2-yr, base-minus) ───────────────────────────────────
CONS_SIGNALS = [
    ("Architecture Billings",  49.0, "ABI 49 (vs 50.8; just above contraction)"),
    ("Copper price",            2.0, "+2%/yr (vs +8%; copper corrects but holds)"),
    ("Global mining CapEx",     5.0, "+5%/yr (vs +10%; mining caution from tariffs)"),
    ("Baker Hughes",           -5.0, "-5% (vs -3%; oil/gas capex stays weak)"),
    ("CAT dealer inventory",    3.0, "3.0 months (vs 2.7; normalises, no restock boom)"),
    ("Data center",            20.0, "+20%/yr (vs +48%; AI capex moderates)"),
]
CONS_EPS_CAGR = 0.05     # 5%/yr conservative (tariff headwinds; construction cycle)
CONS_EXIT_PE  = 16.0     # 16x exit (modest premium to bear; cycle recovers)
CONS_DIVIDEND = 5.96     # $5.96/yr dividend (growing ~8%/yr historically)

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.30    # moderate-high vol; cyclical industrial
VOL_BETA       = 1.10    # slightly above market
VOL_52W_LOW    = 225.0
VOL_52W_HIGH   = 390.0
VOL_DIVIDEND   = 5.96

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

vs_normal, restock_need, tailwind_ann, peak_headwind = dealer_cycle()

# Updated EPP (EPS-based; CAT has no net debt complexity — EPS × min P/E is correct)
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
print(f"  CAT  ·  Caterpillar Inc.  ·  ${CURRENT_PRICE:.2f}  ·  Industrial Equipment")
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
print(f"\n  KEY TRIGGER: ABI falls below 45 (construction recession) + mining capex cut")
print(f"  (commodity downcycle) + tariff-driven cost inflation simultaneously → EPS falls")
print(f"  to $12-13 vs current $18; re-rates to 14x. JOINT probability required for bear.")

# ── ③ UPDATED EPP ────────────────────────────────────────────────────────────
print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS:          ${EPP_TODAY_EPS:.2f}  (FY2025E non-GAAP)")
print(f"  Min viable P/E at panic:          {EPP_MIN_PE:.0f}x  {EPP_REGIME_NOTE}")
print(f"  Note: EPS × min P/E is correct for CAT — no net debt complexity like pipelines.")
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
print(f"\n  Dealer restock tailwind (~${tailwind_ann/1000:.1f}B/yr) not assumed in conservative case.")
print(f"  Data center power generation secular driver adds optionality not priced in base.")

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
print(f"  Cyclical industrials exhibit earnings volatility larger than price volatility.")
print(f"  Tariff escalation (25% steel tariff = ~$600-750M COGS hit = ~$3-4 EPS) is key tail risk.")

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
