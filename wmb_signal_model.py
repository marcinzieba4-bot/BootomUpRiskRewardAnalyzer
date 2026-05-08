#!/usr/bin/env python3
"""
WMB Signal Model  v2
─────────────────────
The Williams Companies, Inc. (NYSE: WMB)  ·  Midstream / Transco Pipeline

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 60.0
REQUIRED_RETURN  = 0.15
HORIZON_YEARS    = 2

SCENARIOS = {
    "BEAR":  ( 1.8,  15,   27, "Gas demand plateau; FERC rate review; vol flat"),
    "BASE":  ( 2.3,  22,   51, "Transco steady; LNG expansion; data center gas ramp"),
    "BULL":  ( 2.9,  25,   73, "AI/LNG supercycle; Transco expansions approved"),
    "XBULL": ( 3.5,  28,   98, "Gas as grid backbone; Transco utilisation record"),
}

# ── AI DATA CENTER GAS DEMAND CALCULATOR (WMB-specific structural feature) ────
AI_DC_PLANNED_GW         = 50.0
AI_DC_CAPACITY_FACTOR    = 0.65
GAS_POWER_SHARE          = 0.30
HEAT_RATE_MMBTU_PER_MWH  = 7.0
TRANSCO_CAPACITY_BCFD    = 10.4
TRANSCO_TARIFF_PER_DTHM  = 0.50

def ai_gas_demand():
    effective_gw      = AI_DC_PLANNED_GW * AI_DC_CAPACITY_FACTOR
    annual_twh        = effective_gw * 8_760 / 1_000
    gas_twh           = annual_twh * GAS_POWER_SHARE
    gas_mmbtu_yr      = gas_twh * 1e6 * HEAT_RATE_MMBTU_PER_MWH
    gas_bcf_yr        = gas_mmbtu_yr / 1e6
    gas_bcfd          = gas_bcf_yr / 365
    pct_transco       = gas_bcfd / TRANSCO_CAPACITY_BCFD * 100
    tariff_uplift_m   = gas_bcfd * 182.5
    return effective_gw, gas_bcfd, pct_transco, tariff_uplift_m

# ── SIGNALS ───────────────────────────────────────────────────────────────────
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("US natural gas production — YoY", "% YoY",
       0.0,   2.0,   5.0,   8.0,   4.0, True,
     "Gas oversupply; producers cut; Haynesville rig count drops"),

    ("LNG export facility utilisation",  "%",
      65.0,  80.0,  88.0,  95.0,  92.0, True,
     "LNG facility outage; Gulf Coast feed-gas demand collapses"),

    ("Nat gas power generation — YoY",  "% YoY",
      -2.0,   3.0,   8.0,  14.0,   9.0, True,
     "Renewables overshoot; gas power dispatch collapses"),

    ("AI data center power demand — YoY","% YoY",
       0.0,  10.0,  30.0,  50.0,  55.0, True,
     "AI capex pause; data center build freezes"),

    ("Transco expansion backlog",        "$B",
       0.5,   2.0,   4.0,   6.0,   5.5, True,
     "FERC rejection cascade; no new capacity approved"),

    ("EIA 2yr US gas demand outlook",   "% YoY",
       0.0,   2.0,   5.0,   9.0,   7.0, True,
     "EIA revises down; gas demand plateau thesis fails"),
]
WEIGHTS = [0.20, 0.20, 0.20, 0.15, 0.15, 0.10]

STRUCTURAL_FACTORS = [
    ("Transco interstate pipeline franchise moat",    1.5, 0.30),
    ("Gas-to-clean energy policy transition risk",   -0.8, 0.25),
    ("AI data center electricity demand tailwind",    1.0, 0.20),
    ("FERC regulatory rate review risk",             -0.5, 0.15),
    ("Balance sheet leverage (~$22B gross debt)",    -0.3, 0.10),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
EPP_TODAY_EBITDA_B  = 7.0     # FY2025E EBITDA ($B)
EPP_MIN_EV_EBITDA   = 7.5     # min viable EV/EBITDA (Transco franchise; similar to OKE's 7.5x)
EPP_NET_DEBT_B      = 22.0    # current net debt ($B)
EPP_SHARES_M        = 1220.0  # diluted shares (M)
EPP_HISTORICAL      = 55.0    # historical EPP v1 (from 2020 floor formula)
EPP_REGIME_NOTE     = "(Transco franchise = irreplaceable; AI/LNG raises floor from 7x to 7.5x)"

# ── CONSERVATIVE GROWTH ───────────────────────────────────────────────────────
CONS_SIGNALS = [
    ("US natural",    3.0,  "+3%/yr (vs +4%; conservative gas supply)"),
    ("LNG export",   85.0,  "85% (vs 92%; one terminal offline)"),
    ("Nat gas",       5.0,  "+5%/yr (vs +9%; partial AI/DC demand)"),
    ("AI data",      20.0,  "+20%/yr (vs +55%; AI build cools)"),
    ("Transco",       3.5,  "$3.5B (vs $5.5B; FERC delays)"),
    ("EIA 2yr",       4.0,  "+4%/yr (vs +7%; modest growth)"),
]
CONS_EBITDA_CAGR    = 0.05   # 5%/yr conservative
CONS_EV_EBITDA      = 9.0    # 9x exit (AI/LNG partial premium)
CONS_DEBT_PAYDOWN_B = 0.8    # $0.8B/yr debt repayment
CONS_DIVIDEND       = 1.90   # $1.90/yr dividend (growing 5%/yr)

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.22    # low vol; utility-like pipeline
VOL_BETA       = 0.65    # low beta; defensive income
VOL_52W_LOW    = 38.0
VOL_52W_HIGH   = 67.0
VOL_DIVIDEND   = 1.90

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

eff_gw, gas_bcfd, pct_transco, tariff_uplift = ai_gas_demand()

# Updated EPP (EBITDA-based)
epp_updated     = (EPP_TODAY_EBITDA_B * EPP_MIN_EV_EBITDA - EPP_NET_DEBT_B) * 1000 / EPP_SHARES_M
epp_gap_pct     = (CURRENT_PRICE - epp_updated) / epp_updated * 100
bear_vs_epp_pct = (SCENARIOS["BEAR"][2] - epp_updated) / epp_updated * 100

# Conservative growth
cons_ebitda_2yr  = EPP_TODAY_EBITDA_B * ((1 + CONS_EBITDA_CAGR) ** 2)
cons_debt_2yr    = EPP_NET_DEBT_B - CONS_DEBT_PAYDOWN_B * 2
cons_equity_2yr  = (cons_ebitda_2yr * CONS_EV_EBITDA - cons_debt_2yr) * 1000 / EPP_SHARES_M
cons_div_2yr     = CONS_DIVIDEND * (1 + 0.02) + CONS_DIVIDEND * (1 + 0.02) ** 2
cons_total_ret   = (cons_equity_2yr - CURRENT_PRICE + cons_div_2yr) / CURRENT_PRICE * 100
cons_annual_ret  = cons_total_ret / 2
cons_price_2yr   = cons_equity_2yr

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
print(f"  WMB  ·  Williams Companies  ·  ${CURRENT_PRICE:.2f}  ·  Midstream / Transco")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

# AI gas demand calculator (keep before ① as WMB-specific feature)
print(f"\n  AI DATA CENTER GAS DEMAND CALCULATOR  (the structural demand driver)")
print("  " + "─" * (W-2))
print(f"  Planned US AI data center capacity (2025-2027):  {AI_DC_PLANNED_GW:.0f} GW")
print(f"  Effective demand (@ {AI_DC_CAPACITY_FACTOR*100:.0f}% utilisation):       {eff_gw:.1f} GW")
print(f"  Annual power generation required:                {eff_gw * 8760 / 1000:.0f} TWh/yr")
print(f"  Gas-fired share ({GAS_POWER_SHARE*100:.0f}% of incremental):          {eff_gw*8760/1000*GAS_POWER_SHARE:.0f} TWh/yr")
print(f"  {'─'*60}")
print(f"  Incremental gas demand:                          {gas_bcfd:.2f} Bcf/day")
print(f"  As % of Transco capacity ({TRANSCO_CAPACITY_BCFD:.1f} Bcf/d):          {pct_transco:.0f}%")
print(f"  Estimated Transco tariff uplift:                ~${tariff_uplift:.0f}M/yr")
print(f"  → Even at 50% realisation, ~${tariff_uplift*0.5:.0f}M/yr incremental revenue.")

# ── ① SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print(f"\n  ① SIGNAL DASHBOARD")
print(f"  {'Signal':<30}  {'BEAR':>7}  {'BASE≥':>7}  {'BULL≥':>7}  {'XBULL≥':>7}  {'NOW':>7}  Score")
print("  " + "─" * (W-2))
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u = unit.split()[0] if unit else ""
    bv_s  = f"{bv:+.0f}{u}"  if hib else f">{bv:.0f}{u}"
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

print(f"\n  Bear composite:  {bear_composite:.2f}  →  Bear scenario price: "
      f"~${expected_price(bear_probs):.0f}  (model)  /  ${SCENARIOS['BEAR'][2]} (defined)")
print(f"  Bear probability (proxy model):  {proxy_probs['BEAR']*100:.1f}%")
print(f"\n  KEY TRIGGER: Gas demand growth flat-lines (AI capex pause + warm winter) +")
print(f"  FERC rate review cuts Transco tariffs 15%. With 95% fee-based revenue,")
print(f"  WMB becomes a 'utility' at 8x EBITDA = ~$28 price.")

# ── ③ UPDATED EPP ────────────────────────────────────────────────────────────
print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EBITDA:       ${EPP_TODAY_EBITDA_B:.1f}B  (FY2025E)")
print(f"  Min viable EV/EBITDA at panic:    {EPP_MIN_EV_EBITDA:.1f}x  {EPP_REGIME_NOTE}")
print(f"  → Trough EV:                     ${EPP_TODAY_EBITDA_B * EPP_MIN_EV_EBITDA:.1f}B")
print(f"  Less net debt:                  -${EPP_NET_DEBT_B:.0f}B")
print(f"  → Equity value:                  ${EPP_TODAY_EBITDA_B * EPP_MIN_EV_EBITDA - EPP_NET_DEBT_B:.1f}B  /  {EPP_SHARES_M:.0f}M shares")
print(f"  {'─'*60}")
print(f"  UPDATED EPP:                     ${epp_updated:.0f}/share")
print(f"  Historical EPP (v1):             ${EPP_HISTORICAL:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.0f} vs Updated EPP ${epp_updated:.0f}:  {epp_gap_pct:+.0f}%  "
      f"{'✓ cushion' if epp_gap_pct >= 0 else '← in distressed zone'}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} vs Updated EPP ${epp_updated:.0f}:  {bear_vs_epp_pct:+.0f}%  "
      f"{'← BEAR requires impairment' if bear_vs_epp_pct < 0 else '✓ bear is cyclical'}")

# ── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print(f"\n  ④ CONSERVATIVE GROWTH  (2-yr, all signals at BASE lower bound — no tailwinds)")
print("  " + "─" * (W-2))
print(f"  {'Signal':<30}  {'Conservative':>14}  vs Current  Rationale")
for sname, sval, srat in CONS_SIGNALS:
    cur = next(cv for name, _, __, ___, ____, _____, cv, ______, _______ in SIGNALS
               if name.lower().startswith(sname.split()[0].lower()))
    diff = sval - cur
    diff_s = f"{diff:+.0f}"
    print(f"  {sname:<30}  {sval:>14.1f}  {diff_s:>9}   {srat[:30]}")

print(f"\n  Conservative 2yr EBITDA:   ${EPP_TODAY_EBITDA_B:.1f}B × (1+{CONS_EBITDA_CAGR*100:.0f}%)² = ${cons_ebitda_2yr:.2f}B")
print(f"  Net debt (after paydown):  ${cons_debt_2yr:.1f}B  (-${CONS_DEBT_PAYDOWN_B:.0f}B/yr repayment)")
print(f"  At {CONS_EV_EBITDA:.0f}x EV/EBITDA:  EV ${cons_ebitda_2yr * CONS_EV_EBITDA:.1f}B  →  equity ${cons_equity_2yr:.0f}/share")
if CONS_DIVIDEND > 0:
    print(f"  + Cumul. dividends (2yr):  +${cons_div_2yr:.2f}/share  "
          f"(${CONS_DIVIDEND:.2f} growing 2%/yr)")
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:     ${cons_equity_2yr:.0f}  "
      f"({'▲' if cons_equity_2yr > CURRENT_PRICE else '▼'}{abs(cons_equity_2yr - CURRENT_PRICE):.0f} from ${CURRENT_PRICE:.0f})")
print(f"  Conservative total return:  {cons_total_ret:+.0f}% over 2yr  "
      f"= {cons_annual_ret:+.0f}%/yr  (incl. dividend)")
print(f"\n  Key: even conservative growth at 9x EBITDA with modest debt paydown")
print(f"  generates positive returns. Transco franchise protects the floor multiple.")

# ── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        ${VOL_52W_LOW:.0f}  –  ${VOL_52W_HIGH:.0f}")
print(f"  Annual dividend:      ${VOL_DIVIDEND:.2f}/share  "
      f"(yield {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized")
print(f"  Beta vs S&P 500:      {VOL_BETA:.2f}  (low beta; defensive income pipeline)")
print(f"  1-sigma range (1yr):  ${vol_low_1yr:.0f}  –  ${vol_high_1yr:.0f}  "
      f"(${CURRENT_PRICE:.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  2-sigma range (1yr):  ${CURRENT_PRICE - 2*sigma_1yr:.0f}  –  "
      f"${CURRENT_PRICE + 2*sigma_1yr:.0f}")
print(f"  {'─'*60}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} requires:  "
      f"~{sigma_needed_bear:.1f}σ price move  "
      f"{'(unusual — requires fundamental break)' if sigma_needed_bear > 1.5 else '(within normal range)'}")
print(f"  Dividend buffer:      ${VOL_DIVIDEND:.2f}/yr absorbs ~{VOL_DIVIDEND/CURRENT_PRICE*100:.1f}% "
      f"of annual price drawdown")
print(f"  → WMB is low-beta income. Buy on dividend yield expansion (>4% = attractive).")
print(f"  → WMB yield today: {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%.  "
      f"Attractive >4% = price <${VOL_DIVIDEND/0.04:.0f}.")

# ── ⑥ PROBABILITY DISTRIBUTION ───────────────────────────────────────────────
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

print(f"\n  Proxy EV (2yr): ${proxy_ev:.0f}  /  Market EV: ${mkt_ev:.0f}  /  "
      f"Current: ${CURRENT_PRICE:.0f}")
print(f"  Conservative EV (2yr, ④): ${cons_equity_2yr:.0f} + ${cons_div_2yr:.2f} divs = "
      f"${cons_equity_2yr + cons_div_2yr:.0f} total value")

print()
print("═" * W)
