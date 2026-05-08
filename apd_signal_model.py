#!/usr/bin/env python3
"""
APD Signal Model  v2
─────────────────────
Air Products & Chemicals, Inc. (NYSE: APD)  ·  Industrial Gases / Hydrogen

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 265.0
REQUIRED_RETURN  = 0.15
HORIZON_YEARS    = 2

SCENARIOS = {
    "BEAR":  (10.0,  18,  180, "H2 write-down; nat gas surge; volumes flat"),
    "BASE":  (14.0,  21,  294, "Core gas stable; NEOM first contribution 2027"),
    "BULL":  (17.0,  24,  408, "NEOM online; H2 premium; industrial recovery"),
    "XBULL": (21.0,  27,  567, "Full H2 scale; green premium; energy leadership"),
}

# ── HYDROGEN MEGAPROJECT NPV CALCULATOR (APD-specific structural feature) ─────
NEOM_NH3_CAPACITY_MT_YR  = 1.2     # million tonnes/yr green ammonia
NEOM_NH3_PRICE_USD_T     = 550     # $/tonne green ammonia (est. wholesale)
NEOM_CAPEX_B             = 8.5     # $B (APD 100% equity)
NEOM_EBIT_MARGIN         = 0.25    # EBIT margin on H2/NH3 operations
NEOM_DELAY_YRS           = 1       # years until first revenue (2027E)

LOUISIANA_REVENUE_M_YR   = 380     # $M/yr at full ramp (blue H2 + derivatives)
LOUISIANA_CAPEX_B        = 4.5     # $B
LOUISIANA_EBIT_MARGIN    = 0.28    # EBIT margin
LOUISIANA_DELAY_YRS      = 2       # years until first revenue (2028E)

SHARES_OUT_M             = 222     # shares outstanding (millions)
TOTAL_H2_CAPEX_B         = 13.5    # total committed H2 capex ($B)

def hydrogen_project_npv():
    neom_rev_m    = NEOM_NH3_CAPACITY_MT_YR * 1e6 * NEOM_NH3_PRICE_USD_T / 1e6
    neom_ebit     = neom_rev_m * NEOM_EBIT_MARGIN
    la_ebit       = LOUISIANA_REVENUE_M_YR * LOUISIANA_EBIT_MARGIN
    neom_npv_m    = (neom_ebit * 12) / (1 + REQUIRED_RETURN) ** NEOM_DELAY_YRS
    la_npv_m      = (la_ebit   * 12) / (1 + REQUIRED_RETURN) ** LOUISIANA_DELAY_YRS
    total_npv_m   = neom_npv_m + la_npv_m
    npv_per_share = total_npv_m / SHARES_OUT_M
    capex_per_shr = TOTAL_H2_CAPEX_B * 1000 / SHARES_OUT_M
    return neom_ebit, la_ebit, total_npv_m, npv_per_share, capex_per_shr

# ── SIGNALS ───────────────────────────────────────────────────────────────────
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("US industrial production — YoY",  "% YoY",
     -3.0,   0.0,   3.0,   6.0,   1.5, True,
     "Manufacturing recession; on-site O2/N2/Ar volume contracts"),

    ("Natural gas price — YoY change",  "% YoY",
      50.0,  10.0,   0.0, -15.0,  25.0, False,
     "COGS spike: gas 35-40% of APD cost; destroys H2 economics"),

    ("Green H2 project FIDs (GW/yr)",   "GW/yr",
       1.0,   3.0,  10.0,  20.0,   8.0, True,
     "H2 market stalls; NEOM/Louisiana offtake confidence collapses"),

    ("EU ETS carbon price ($/tonne)",   "$/t",
      15.0,  30.0,  55.0,  85.0,  45.0, True,
     "Green vs grey H2 spread inverts; H2 premium economics vanish"),

    ("Industrial gas demand — YoY",     "% YoY",
      -1.0,   1.0,   4.0,   7.0,   3.0, True,
     "Peer volume (Air Liquide/Linde) collapses; demand recession signal"),

    ("APD take-or-pay renewal rate",    "%",
      75.0,  85.0,  90.0,  96.0,  94.0, True,
     "Contract defection cascade; on-site moat eroding permanently"),
]
WEIGHTS = [0.20, 0.20, 0.15, 0.15, 0.15, 0.15]

STRUCTURAL_FACTORS = [
    ("Long-term take-or-pay gas contract moat",       0.8, 0.25),
    ("NEOM/Louisiana H2 megaproject execution risk", -1.2, 0.30),
    ("New CEO strategy reset uncertainty",           -0.8, 0.20),
    ("Energy transition secular H2 tailwind",         0.8, 0.15),
    ("Balance sheet leverage from H2 capex",         -0.5, 0.10),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
EPP_TODAY_EPS    = 10.50    # FY2025E non-GAAP EPS
EPP_MIN_PE       = 18.0     # min viable P/E (on-site take-or-pay = recurring cash flow floor)
EPP_HISTORICAL   = 198.0    # historical EPP v1 (from trough formula)
EPP_REGIME_NOTE  = "(on-site take-or-pay protects earnings floor; H2 optionality = upside)"

# ── CONSERVATIVE GROWTH (2-yr, base-minus) ────────────────────────────────────
CONS_SIGNALS = [
    ("US industrial",    0.5,  "+0.5% YoY (vs current +1.5%; sluggish manufacturing)"),
    ("Natural gas",     15.0,  "+15% YoY (vs current +25%; partial easing)"),
    ("Green H2",         4.0,  "4 GW/yr (vs current 8; H2 market cools)"),
    ("EU ETS",          35.0,  "$35/t (vs current $45; carbon market softens)"),
    ("Industrial gas",   1.5,  "+1.5% YoY (vs current +3%; sluggish peers)"),
    ("APD take",        88.0,  "88% (vs current 94%; one major renewal delay)"),
]
CONS_EPS_CAGR = 0.05     # 5%/yr conservative (H2 disappointments; vol sluggish)
CONS_EXIT_PE  = 20.0     # 20x exit (lower than current ~25x; H2 premium removed)
CONS_DIVIDEND = 7.72     # $7.72/yr dividend (growing 7%/yr historically)

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.22    # moderate vol; utility-like industrial gas
VOL_BETA       = 0.80    # below market
VOL_52W_LOW    = 220.0   # approx
VOL_52W_HIGH   = 310.0   # approx
VOL_DIVIDEND   = 7.72

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

neom_ebit, la_ebit, total_npv_m, npv_per_shr, capex_per_shr = hydrogen_project_npv()

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
print(f"  APD  ·  Air Products & Chemicals  ·  ${CURRENT_PRICE:.2f}  ·  Industrial Gases")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

# Hydrogen NPV calculator (keep before ① as APD-specific feature)
print(f"\n  HYDROGEN MEGAPROJECT NPV  (capex deployed vs. value created)")
print("  " + "─" * (W-2))
print(f"  NEOM Green H2 (1.2Mt/yr NH3 @ ${NEOM_NH3_PRICE_USD_T}/t):")
print(f"    Revenue at ramp:   ${NEOM_NH3_CAPACITY_MT_YR*1e6*NEOM_NH3_PRICE_USD_T/1e6:.0f}M/yr   EBIT: ${neom_ebit:.0f}M/yr")
print(f"    Capital deployed:  ${NEOM_CAPEX_B:.1f}B    Delay: +{NEOM_DELAY_YRS}yr (2027E)")
print(f"  Louisiana Clean H2 (750 TPD blue H2):")
print(f"    Revenue at ramp:   ${LOUISIANA_REVENUE_M_YR:.0f}M/yr       EBIT: ${la_ebit:.0f}M/yr")
print(f"    Capital deployed:  ${LOUISIANA_CAPEX_B:.1f}B    Delay: +{LOUISIANA_DELAY_YRS}yr (2028E)")
print(f"  {'─'*60}")
print(f"  Total H2 capex deployed:  ${TOTAL_H2_CAPEX_B:.1f}B  =  ${capex_per_shr:.0f}/share")
print(f"  NPV of H2 projects:       ${total_npv_m/1000:.1f}B   =  ${npv_per_shr:.0f}/share  (12x EBIT, discounted)")
print(f"  Value destruction gap:    ${(capex_per_shr - npv_per_shr):.0f}/share  (at current commodity prices)")

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
print(f"\n  KEY TRIGGER: H2 project write-down + natural gas price spike simultaneously")
print(f"  destroy APD's hydrogen economics and compress margins on O2/N2 via energy costs.")
print(f"  Capital deployed at poor ROIC gets impaired. This is a JOINT PROBABILITY event.")

# ── ③ UPDATED EPP ────────────────────────────────────────────────────────────
print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS:           ${EPP_TODAY_EPS:.2f}  (FY2025E non-GAAP)")
print(f"  Min viable P/E at max pessimism:   {EPP_MIN_PE:.0f}x  {EPP_REGIME_NOTE}")
print(f"  {'─'*60}")
print(f"  UPDATED EPP:                      ${epp_updated:.0f}/share")
print(f"  Historical EPP (v1):              ${EPP_HISTORICAL:.0f}/share")
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

print(f"\n  Conservative 2yr EPS:   ${EPP_TODAY_EPS:.2f} × (1+{CONS_EPS_CAGR*100:.0f}%)² = ${cons_eps_2yr:.2f}")
print(f"  At {CONS_EXIT_PE:.0f}x P/E (conservative):  ${cons_price_2yr:.0f}/share")
if CONS_DIVIDEND > 0:
    print(f"  + Cumul. dividends (2yr):  +${cons_div_2yr:.2f}/share")
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:     ${cons_price_2yr:.0f}  "
      f"({'▲' if cons_price_2yr > CURRENT_PRICE else '▼'}{abs(cons_price_2yr - CURRENT_PRICE):.0f} from ${CURRENT_PRICE:.0f})")
print(f"  Conservative total return:  {cons_total_ret:+.0f}% over 2yr  = {cons_annual_ret:+.0f}%/yr")
print(f"\n  Key: core gas business alone at 20x EPS floor justifies ~${cons_price_2yr:.0f}.")
print(f"  H2 projects are free optionality at this entry price.")

# ── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        ${VOL_52W_LOW:.0f}  –  ${VOL_52W_HIGH:.0f}")
print(f"  Annual dividend:      ${VOL_DIVIDEND:.2f}/share  "
      f"(yield {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized")
print(f"  Beta vs S&P 500:      {VOL_BETA:.2f}  (below market; utility-like industrial gas)")
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
print(f"  → APD is low-beta income + growth optionality. Core gas protects floor.")
print(f"  → APD yield today: {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%.  "
      f"Attractive >3% = price <${VOL_DIVIDEND/0.03:.0f}.")

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
print(f"  Conservative EV (2yr, ④): ${cons_price_2yr:.0f} + ${cons_div_2yr:.2f} divs = "
      f"${cons_price_2yr + cons_div_2yr:.0f} total value")

print()
print("═" * W)
