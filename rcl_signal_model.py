#!/usr/bin/env python3
"""
RCL Signal Model  v2
─────────────────────
Royal Caribbean Group (NYSE: RCL)  ·  Cruise / Leisure

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 235.0
REQUIRED_RETURN  = 0.15
HORIZON_YEARS    = 2

SCENARIOS = {
    "BEAR":  (12.0,  12,  144, "Recession; consumer pullback; debt servicing squeeze"),
    "BASE":  (20.0,  14,  280, "Steady demand; private dest ramp; debt falls to $15B"),
    "BULL":  (25.0,  17,  425, "Yield growth 7%+; private dest at scale; China opens"),
    "XBULL": (30.0,  20,  600, "Supercycle: pricing power + private dest + China boom"),
}

# ── PRIVATE DESTINATION ECONOMICS CALCULATOR (RCL-specific) ───────────────────
COCCOCAY_ANNUAL_VISITORS     = 4_200_000
RBC_NASSAU_ANNUAL_VISITORS   = 2_400_000
PRIVATE_DEST_YIELD_PREMIUM   =       170
STANDARD_PORT_NPCCD          =       130
FLEET_CAPACITY_APCD_M        =        95

def private_dest_economics():
    total_private_pax  = COCCOCAY_ANNUAL_VISITORS + RBC_NASSAU_ANNUAL_VISITORS
    annual_premium_rev = total_private_pax * PRIVATE_DEST_YIELD_PREMIUM / 1e9
    pct_of_capacity    = total_private_pax / (FLEET_CAPACITY_APCD_M * 1e6) * 100
    npccd_lift         = (total_private_pax * PRIVATE_DEST_YIELD_PREMIUM) / (FLEET_CAPACITY_APCD_M * 1e6)
    future_premium     = annual_premium_rev * 2.5
    return total_private_pax, annual_premium_rev, pct_of_capacity, npccd_lift, future_premium

# ── SIGNALS ───────────────────────────────────────────────────────────────────
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("US consumer confidence index",  "pts",
      70.0,  90.0, 100.0, 115.0,  93.0, True,
     "Recession; cruise discretionary bookings collapse"),

    ("Cruise net yield per APCD YoY", "% YoY",
      -5.0,   3.0,   6.0,  10.0,   7.5, True,
     "Yield war; overcapacity + demand destruction"),

    ("Fwd 12M booking price premium", "% YoY",
      -3.0,   3.0,   7.0,  12.0,   8.0, True,
     "Forward book collapses; recession cancellations accelerate"),

    ("Caribbean resort ADR YoY",      "% YoY",
      -2.0,   2.0,   6.0,  10.0,   5.0, True,
     "Land alternatives cheap; cruise value proposition weakens"),

    ("US leisure travel spend YoY",   "% YoY",
      -3.0,   2.0,   5.0,   9.0,   4.0, True,
     "Leisure travel contracts; RCL loses TAM share"),

    ("Fleet load factor",             "%",
      88.0, 100.0, 106.0, 110.0, 108.0, True,
     "COVID-variant outbreak; mass cancellations; load below 100%"),
]
WEIGHTS = [0.20, 0.20, 0.15, 0.15, 0.15, 0.15]

STRUCTURAL_FACTORS = [
    ("Private destination captive revenue moat",      1.0, 0.25),
    ("Industry overcapacity (8-10 new ships 25-27)", -0.8, 0.25),
    ("$20B gross debt financial constraint",         -0.8, 0.20),
    ("Royal Caribbean / Celebrity brand premium",     0.5, 0.15),
    ("Fuel / LNG transition capital cost",           -0.3, 0.15),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
EPP_TODAY_EBITDA_B  = 7.0    # FY2025E EBITDA ($B)
EPP_MIN_EV_EBITDA   = 6.0    # min viable EV/EBITDA at panic (raised from COVID 3x floor)
EPP_NET_DEBT_B      = 18.0   # current net debt ($B)
EPP_SHARES_M        = 267.0  # diluted shares (M)
EPP_HISTORICAL      = 62.0   # historical EPP v1 (from 2020 floor)
EPP_REGIME_NOTE     = "(raised from 3x COVID panic floor; private destinations = recurring asset)"

# ── CONSERVATIVE GROWTH ───────────────────────────────────────────────────────
CONS_SIGNALS = [
    ("US consumer",    88.0,  "88 pts (vs current 93; mild recession anxiety)"),
    ("Cruise net",      4.0,  "+4% YoY (vs current +7.5%; capacity absorbs demand)"),
    ("Fwd 12M",         3.5,  "+3.5% YoY (vs current +8%; bookings normalise)"),
    ("Caribbean",       3.0,  "+3% YoY (vs current +5%; hotel pricing moderates)"),
    ("US leisure",      2.5,  "+2.5% YoY (vs current +4%; consumer cautious)"),
    ("Fleet load",    104.0,  "104% (vs current 108%; new capacity absorbs demand)"),
]
CONS_EBITDA_CAGR    = 0.08   # 8%/yr conservative (strong bookings; Wave season)
CONS_EV_EBITDA      = 8.0    # 8x exit EV/EBITDA (no premium re-rating)
CONS_DEBT_PAYDOWN_B = 2.5    # $2.5B/yr debt repayment (aggressive FCF allocation)
CONS_DIVIDEND       = 0.0    # no dividend (suspended; capital to debt)

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.45    # high vol; discretionary + leverage
VOL_BETA       = 1.80    # high beta; macro sensitive
VOL_52W_LOW    = 150.0
VOL_52W_HIGH   = 290.0
VOL_DIVIDEND   = 0.0

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

def market_implied_composite(target_ev, tolerance=2.0):
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

total_pax, premium_rev, pct_cap, npccd_lift, future_premium = private_dest_economics()

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
print(f"  RCL  ·  Royal Caribbean Group  ·  ${CURRENT_PRICE:.2f}  ·  Cruise / Leisure")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

# Private destination economics (keep before ① as RCL-specific feature)
print(f"\n  PRIVATE DESTINATION ECONOMICS  (the structural yield driver)")
print("  " + "─" * (W-2))
print(f"  Perfect Day at CocoCay (visitors/yr):  {COCCOCAY_ANNUAL_VISITORS/1e6:.1f}M")
print(f"  Royal Beach Club Nassau (visitors/yr): {RBC_NASSAU_ANNUAL_VISITORS/1e6:.1f}M  (opened 2025)")
print(f"  Total private destination traffic:     {total_pax/1e6:.1f}M pax/yr  ({pct_cap:.0f}% of fleet APCD)")
print(f"  Net yield premium vs regular port:     ${PRIVATE_DEST_YIELD_PREMIUM}/passenger")
print(f"  {'─'*60}")
print(f"  Annual revenue premium over std ports: ${premium_rev:.2f}B / yr")
print(f"  Fleet-wide NPCCD structural lift:      +${npccd_lift:.1f} / APCD")
print(f"  If 2 additional private dests added:   ~${future_premium:.1f}B / yr premium (2028E)")

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
print(f"\n  KEY TRIGGER: Consumer confidence falls below 80 (recession) + a health scare")
print(f"  (COVID variant) simultaneously → bookings collapse 40%+. With $18B net debt,")
print(f"  EBITDA below $3B makes debt service precarious. JOINT PROBABILITY event.")

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
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:     ${cons_equity_2yr:.0f}  "
      f"({'▲' if cons_equity_2yr > CURRENT_PRICE else '▼'}{abs(cons_equity_2yr - CURRENT_PRICE):.0f} from ${CURRENT_PRICE:.0f})")
print(f"  Conservative total return:  {cons_total_ret:+.0f}% over 2yr  = {cons_annual_ret:+.0f}%/yr")
print(f"\n  Key: debt re-rating catalyst at 2.5x ND/EBITDA triggers multiple expansion.")
print(f"  Private destination EBITDA is sticky — conservative case preserves this floor.")

# ── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        ${VOL_52W_LOW:.0f}  –  ${VOL_52W_HIGH:.0f}")
print(f"  Annual dividend:      ${VOL_DIVIDEND:.2f}/share  (suspended; capital to debt repayment)")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized")
print(f"  Beta vs S&P 500:      {VOL_BETA:.2f}  (high beta; macro + consumer sensitive)")
print(f"  1-sigma range (1yr):  ${vol_low_1yr:.0f}  –  ${vol_high_1yr:.0f}  "
      f"(${CURRENT_PRICE:.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  2-sigma range (1yr):  ${CURRENT_PRICE - 2*sigma_1yr:.0f}  –  "
      f"${CURRENT_PRICE + 2*sigma_1yr:.0f}")
print(f"  {'─'*60}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} requires:  "
      f"~{sigma_needed_bear:.1f}σ price move  "
      f"{'(unusual — requires fundamental break)' if sigma_needed_bear > 1.5 else '(within normal range)'}")
print(f"  No dividend buffer — all FCF directed to debt repayment.")
print(f"  → High-beta discretionary. Position sizing must account for {VOL_ANNUAL_PCT*100:.0f}% annualized vol.")

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
