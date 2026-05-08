#!/usr/bin/env python3
"""
PYPL Signal Model  v2
─────────────────────
PayPal Holdings, Inc. (NASDAQ: PYPL)  ·  Payments / Fintech

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 78.0
REQUIRED_RETURN  = 0.15
HORIZON_YEARS    = 2

SCENARIOS = {
    "BEAR":  ( 3.0,  13,   39, "Apple Pay/AI wallets structurally displace PYPL checkout"),
    "BASE":  ( 6.0,  17,  102, "Chriss executes; take rate stabilises; Venmo monetises"),
    "BULL":  ( 9.0,  21,  189, "Branded checkout revival; ads platform grows; Venmo at scale"),
    "XBULL": (12.0,  25,  300, "PayPal = primary wallet for AI-native commerce; re-rates to fintech"),
}

# ── TAKE RATE DECOMPOSITION (PYPL-specific structural feature) ────────────────
TOTAL_TPV_T         = 1.65
BRANDED_MIX_PCT     = 46
BRANDED_TAKE_RATE   = 2.30
UNBRANDED_TAKE_RATE = 0.72
PEAK_BRANDED_MIX    = 55

def take_rate_economics():
    unbranded_mix    = 100 - BRANDED_MIX_PCT
    blended          = (BRANDED_MIX_PCT * BRANDED_TAKE_RATE +
                        unbranded_mix * UNBRANDED_TAKE_RATE) / 100
    current_rev      = TOTAL_TPV_T * 1e12 * blended / 100 / 1e9
    take_rate_prem   = BRANDED_TAKE_RATE - UNBRANDED_TAKE_RATE
    rev_per_pp_shift = TOTAL_TPV_T * 1e12 * (take_rate_prem / 100) * 0.01 / 1e9
    recovery_blend   = (55 * BRANDED_TAKE_RATE + 45 * UNBRANDED_TAKE_RATE) / 100
    recovery_rev     = TOTAL_TPV_T * 1e12 * recovery_blend / 100 / 1e9
    mix_recovery_upside = recovery_rev - current_rev
    return blended, current_rev, take_rate_prem, rev_per_pp_shift, mix_recovery_upside

# ── SIGNALS ───────────────────────────────────────────────────────────────────
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("US e-commerce sales YoY",          "% YoY",
       0.0,   4.0,   8.0,  14.0,   7.0, True,
     "E-commerce contraction; consumer recessionary behavior"),

    ("PayPal transactions / active acct", "TPA",
      48.0,  55.0,  65.0,  75.0,  62.0, True,
     "User disengagement; Apple/Google Wallet displaces PayPal"),

    ("Shopify GMV YoY",                  "% YoY",
       3.0,  10.0,  20.0,  30.0,  23.0, True,
     "SMB e-commerce collapses; PYPL loses checkout partner volume"),

    ("PYPL blended take rate change",    "pp YoY",
      -0.30, -0.15,  0.00,  0.10, -0.03, True,
     "Braintree structural displacement; take rate compression accelerates"),

    ("Global cross-border e-commerce",   "% YoY",
       2.0,   8.0,  15.0,  22.0,  15.0, True,
     "Cross-border contracts; premium take-rate segment shrinks"),

    ("BNPL industry volume YoY",         "% YoY",
       2.0,  10.0,  20.0,  35.0,  22.0, True,
     "BNPL fades; Pay Later adoption stalls; checkout frequency falls"),
]
WEIGHTS = [0.25, 0.20, 0.15, 0.15, 0.15, 0.10]

STRUCTURAL_FACTORS = [
    ("Apple/Google OS-native checkout displacement", -1.0, 0.40),
    ("Venmo 90M user network effect moat",            0.5, 0.20),
    ("Chriss turnaround execution (18M record)",      0.3, 0.20),
    ("$7B net cash — balance sheet strength",         0.3, 0.10),
    ("US fintech regulatory tailwind",                0.2, 0.10),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
EPP_TODAY_EPS    = 4.50     # FY2025E non-GAAP EPS (Chriss execution in progress)
EPP_MIN_PE       = 13.0     # min viable P/E (network of 430M accounts = floor)
EPP_HISTORICAL   = 58.0     # historical EPP v1 (from 2022 floor)
EPP_REGIME_NOTE  = "(account network + Venmo = durable floor; branded checkout recovery = upside)"

# ── CONSERVATIVE GROWTH (2-yr, base-minus) ────────────────────────────────────
CONS_SIGNALS = [
    ("US e-commerce",   5.0,  "+5% YoY (vs +7%; consumer cautious)"),
    ("PayPal",         58.0,  "58 TPA (vs 62; engagement plateaus)"),
    ("Shopify",        12.0,  "+12% YoY (vs +23%; SMB growth moderates)"),
    ("PYPL blended",  -0.08,  "-0.08pp (vs -0.03; Braintree drag continues)"),
    ("Global cross",   10.0,  "+10% YoY (vs +15%; cross-border moderates)"),
    ("BNPL industry",  12.0,  "+12% YoY (vs +22%; BNPL growth normalises)"),
]
CONS_EPS_CAGR = 0.08     # 8%/yr conservative (cost cuts + modest TPV growth)
CONS_EXIT_PE  = 15.0     # 15x exit (no re-rating; market stays skeptical)
CONS_DIVIDEND = 0.0      # no dividend

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.40    # high vol; execution risk + sector overhang
VOL_BETA       = 1.20    # above market
VOL_52W_LOW    = 55.0
VOL_52W_HIGH   = 97.0
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

blended_tr, curr_rev, tr_prem, rev_per_pp, mix_upside = take_rate_economics()

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
print(f"  PYPL  ·  PayPal Holdings  ·  ${CURRENT_PRICE:.2f}  ·  Payments / Fintech")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

# Take rate decomposition (keep before ① as PYPL-specific feature)
print(f"\n  TAKE RATE DECOMPOSITION  (the entire Chriss thesis in one table)")
print("  " + "─" * (W-2))
print(f"  Total TPV (FY2025E):                         ${TOTAL_TPV_T:.2f}T")
print(f"  Branded checkout mix:                        {BRANDED_MIX_PCT}%  (take rate {BRANDED_TAKE_RATE:.2f}%)")
print(f"  Unbranded / Braintree mix:                   {100-BRANDED_MIX_PCT}%  (take rate {UNBRANDED_TAKE_RATE:.2f}%)")
print(f"  Blended take rate (current):                 {blended_tr:.3f}%")
print(f"  {'─'*60}")
print(f"  Revenue uplift per 1pp branded mix gain:     ${rev_per_pp:.2f}B / yr  ← the leverage")
print(f"  Full recovery to {PEAK_BRANDED_MIX}% branded → +${mix_upside:.1f}B annual revenue uplift")

# ── ① SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print(f"\n  ① SIGNAL DASHBOARD")
print(f"  {'Signal':<30}  {'BEAR':>7}  {'BASE≥':>7}  {'BULL≥':>7}  {'XBULL≥':>7}  {'NOW':>7}  Score")
print("  " + "─" * (W-2))
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u = unit.split()[0] if unit else ""
    bv_s  = f"{bv:+.2f}{u}" if "pp" in unit else (f"{bv:+.0f}{u}" if hib else f">{bv:.0f}{u}")
    bf_s  = f"{bf:.2f}{u}" if "pp" in unit else f"{bf:.0f}{u}"
    blf_s = f"{blf:.2f}{u}" if "pp" in unit else f"{blf:.0f}{u}"
    xf_s  = f"{xf:.2f}{u}" if "pp" in unit else f"{xf:.0f}{u}"
    cv_s  = f"{cv:+.2f}{u}" if "pp" in unit else f"{cv:+.0f}{u}"
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
    if "pp" in unit:
        cv_s   = f"{cv:+.2f}{u}"
        bv_s   = f"{bv:+.2f}{u}"
        move_s = f"{bv-cv:+.2f}{u}"
    else:
        cv_s   = f"{cv:+.0f}{u}"
        bv_s   = f"{bv:+.0f}{u}"
        move_s = f"{bv-cv:+.0f}{u}"
    trigger = narr[:38] if len(narr) <= 38 else narr[:35] + "…"
    print(f"  {name:<30}  {cv_s:>8}  {bv_s:>8}  {move_s:>6}  {trigger}")

print(f"\n  Bear composite:  {bear_composite:.2f}  →  Bear scenario price: "
      f"~${expected_price(bear_probs):.0f}  (model)  /  ${SCENARIOS['BEAR'][2]} (defined)")
print(f"  Bear probability (proxy model):  {proxy_probs['BEAR']*100:.1f}%")
print(f"\n  KEY TRIGGER: Apple Pay + Shopify Pay structural displacement of branded")
print(f"  checkout → TPV share falls from 40% to 30% → Braintree/unbranded margin")
print(f"  compression. No path to EPS acceleration; re-rates to 13x.")

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
    diff_s = f"{diff:+.2f}" if abs(diff) < 1 else f"{diff:+.0f}"
    print(f"  {sname:<30}  {sval:>14.2f}  {diff_s:>9}   {srat[:30]}")

print(f"\n  Conservative 2yr EPS:   ${EPP_TODAY_EPS:.2f} × (1+{CONS_EPS_CAGR*100:.0f}%)² = ${cons_eps_2yr:.2f}")
print(f"  At {CONS_EXIT_PE:.0f}x P/E (conservative):  ${cons_price_2yr:.0f}/share")
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:     ${cons_price_2yr:.0f}  "
      f"({'▲' if cons_price_2yr > CURRENT_PRICE else '▼'}{abs(cons_price_2yr - CURRENT_PRICE):.0f} from ${CURRENT_PRICE:.0f})")
print(f"  Conservative total return:  {cons_total_ret:+.0f}% over 2yr  = {cons_annual_ret:+.0f}%/yr")
print(f"\n  Key: Chriss cost cuts + buybacks alone deliver EPS growth even without")
print(f"  revenue re-acceleration. The conservative case doesn't require branded recovery.")

# ── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        ${VOL_52W_LOW:.0f}  –  ${VOL_52W_HIGH:.0f}")
print(f"  Annual dividend:      none  ($7B net cash used for buybacks)")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized")
print(f"  Beta vs S&P 500:      {VOL_BETA:.2f}  (above market; execution + sector risk)")
print(f"  1-sigma range (1yr):  ${vol_low_1yr:.0f}  –  ${vol_high_1yr:.0f}  "
      f"(${CURRENT_PRICE:.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  2-sigma range (1yr):  ${max(0, CURRENT_PRICE - 2*sigma_1yr):.0f}  –  "
      f"${CURRENT_PRICE + 2*sigma_1yr:.0f}")
print(f"  {'─'*60}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} requires:  "
      f"~{sigma_needed_bear:.1f}σ price move  "
      f"{'(unusual — requires fundamental break)' if sigma_needed_bear > 1.5 else '(within normal range)'}")
print(f"  No dividend buffer — $7B buyback program partially offsets drawdown.")
print(f"  → Structural displacement risk (Apple/AI) is slow-moving but persistent.")

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
