#!/usr/bin/env python3
"""
COIN Signal Model  v2
─────────────────────
Coinbase Global, Inc. (NASDAQ: COIN)  ·  Crypto Exchange / Infrastructure

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 194.0
REQUIRED_RETURN  = 0.15
HORIZON_YEARS    = 2

SCENARIOS = {
    "BEAR":  ( 2.0,  12,   24, "BTC stays $60-75K; extended crypto winter; volumes -40%"),
    "BASE":  (10.0,  22,  220, "BTC recovers $120-140K; stablecoin bill passes; sub rev $4B+"),
    "BULL":  (18.0,  25,  450, "BTC $160K+; USDC $150B; Base L2 significant DeFi revenue"),
    "XBULL": (28.0,  28,  784, "BTC $200K+; USDC = global payments layer; regulatory goldilocks"),
}

# ── SUBSCRIPTION REVENUE FLOOR CALCULATOR (COIN-specific) ─────────────────────
USDC_MARKET_CAP_B    = 75.0
USDC_YIELD           = 0.04
COINBASE_USDC_SHARE  = 0.50
STAKING_ANNUAL_B     = 0.72
COINBASE_ONE_SUBS_M  = 0.95
COINBASE_ONE_ARPU    = 29.99

def sub_revenue_floor():
    usdc_rev  = USDC_MARKET_CAP_B * USDC_YIELD * COINBASE_USDC_SHARE
    coinb1_rev = COINBASE_ONE_SUBS_M * COINBASE_ONE_ARPU * 12 / 1000
    return usdc_rev + STAKING_ANNUAL_B + coinb1_rev

# ── SIGNALS ───────────────────────────────────────────────────────────────────
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("Bitcoin price — YoY change",      "% YoY",
     -50.0,  -30.0,  20.0,  80.0,  -26.0, True,
     "Crypto winter; BTC falls to $40K; retail exits platform"),

    ("BTC spot ETF flows (monthly)",    "$B/mo",
      -3.0,    0.0,   1.0,   3.0,    2.44, True,
     "ETF redemptions; institutional exodus from crypto"),

    ("USDC market cap",                 "$B",
      15.0,   30.0,  60.0,  90.0,   75.0, True,
     "Stablecoin bill fails; USDC reserve income collapses"),

    ("Global crypto spot vol — YoY",   "% YoY",
     -60.0,  -40.0, -10.0,  30.0,  -30.0, True,
     "Transaction revenue floor: retail+institutional activity drops"),

    ("US crypto regulation clarity",   "/4",
       1.0,    1.0,   2.0,   4.0,    3.0, True,
     "Regulatory reversal; exchange operation uncertainty returns"),

    ("Sub/services revenue — QoQ",     "% QoQ",
     -30.0,  -10.0,   5.0,  15.0,  -18.0, True,
     "Staking rates + USDC yield both collapse; recurring floor erodes"),
]
WEIGHTS = [0.30, 0.20, 0.15, 0.15, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("US crypto regulatory clarity improving",        1.0, 0.30),
    ("BTC single-driver revenue concentration",      -0.8, 0.25),
    ("Exchange commoditisation / fee compression",   -0.5, 0.20),
    ("Base L2 ecosystem optionality",                 0.5, 0.15),
    ("Institutional custody moat",                    0.3, 0.10),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
EPP_TODAY_EPS    = 3.00     # FY2025E EPS (crypto vol-dependent; conservative)
EPP_MIN_PE       = 12.0     # min viable P/E (exchange floor even in crypto winter)
EPP_HISTORICAL   = 39.0     # historical EPP v1 (from 2022 FTX crash floor)
EPP_REGIME_NOTE  = "(regulatory clarity post-2024 elections raises crypto platform floor P/E)"

# ── CONSERVATIVE GROWTH (2-yr, base-minus) ────────────────────────────────────
CONS_SIGNALS = [
    ("Bitcoin price",   -15.0, "-15% YoY (vs -26%; BTC stabilises near $80K)"),
    ("BTC spot",          0.5, "$0.5B/mo (vs $2.44B; institutional cautious)"),
    ("USDC market",      50.0, "$50B (vs $75B; stablecoin growth moderate)"),
    ("Global crypto",   -20.0, "-20% YoY (vs -30%; volumes partially recover)"),
    ("US crypto",         2.5, "2.5/4 (vs 3.0; regulatory progress slows)"),
    ("Sub/services",     -5.0, "-5% QoQ (vs -18%; subscription floor holds)"),
]
CONS_EPS_CAGR = 0.15     # 15%/yr conservative (subscription rev growing)
CONS_EXIT_PE  = 20.0     # 20x exit (regulated exchange premium)
CONS_DIVIDEND = 0.0      # no dividend

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.75    # extremely high vol; crypto-correlated
VOL_BETA       = 2.50    # very high beta; leveraged crypto play
VOL_52W_LOW    = 130.0
VOL_52W_HIGH   = 345.0
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

floor = sub_revenue_floor()

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
print(f"  COIN  ·  Coinbase Global  ·  ${CURRENT_PRICE:.2f}  ·  Crypto Exchange")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

# Subscription revenue floor (keep before ① as COIN-specific feature)
print(f"\n  SUBSCRIPTION REVENUE FLOOR  (holds regardless of BTC price)")
print("  " + "─" * (W-2))
print(f"  USDC revenue  ({USDC_MARKET_CAP_B:.0f}B × {USDC_YIELD*100:.0f}% yield × {COINBASE_USDC_SHARE*100:.0f}% share)   ${USDC_MARKET_CAP_B*USDC_YIELD*COINBASE_USDC_SHARE:.2f}B / yr")
print(f"  Staking revenue (FY2025 run-rate)                   ${STAKING_ANNUAL_B:.2f}B / yr")
print(f"  Coinbase One  ({COINBASE_ONE_SUBS_M*1000:.0f}K subs × ${COINBASE_ONE_ARPU:.0f}/mo)          ${COINBASE_ONE_SUBS_M*COINBASE_ONE_ARPU*12/1000:.2f}B / yr")
print(f"  {'─'*60}")
print(f"  Total recurring floor                               ${floor:.2f}B / yr")
print(f"  → Even in bear scenario, ~${floor:.1f}B/yr is structurally anchored.")

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
print(f"\n  KEY TRIGGER: BTC falls below $50K (on-chain liquidations cascade) +")
print(f"  stablecoin bill fails (regulatory uncertainty returns). Coinbase loses")
print(f"  60% of transaction volume; subscription rev alone cannot cover fixed costs.")

# ── ③ UPDATED EPP ────────────────────────────────────────────────────────────
print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS:           ${EPP_TODAY_EPS:.2f}  (FY2025E, conservative)")
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
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:     ${cons_price_2yr:.0f}  "
      f"({'▲' if cons_price_2yr > CURRENT_PRICE else '▼'}{abs(cons_price_2yr - CURRENT_PRICE):.0f} from ${CURRENT_PRICE:.0f})")
print(f"  Conservative total return:  {cons_total_ret:+.0f}% over 2yr  = {cons_annual_ret:+.0f}%/yr")
print(f"\n  Key: subscription revenue floor (${floor:.1f}B) protects downside.")
print(f"  EPS growth from subscription expansion is the conservative base case.")

# ── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        ${VOL_52W_LOW:.0f}  –  ${VOL_52W_HIGH:.0f}")
print(f"  Annual dividend:      none")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized  (extremely high; crypto-linked)")
print(f"  Beta vs S&P 500:      {VOL_BETA:.2f}  (very high beta; leveraged BTC proxy)")
print(f"  1-sigma range (1yr):  ${vol_low_1yr:.0f}  –  ${vol_high_1yr:.0f}  "
      f"(${CURRENT_PRICE:.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  2-sigma range (1yr):  ${max(0, CURRENT_PRICE - 2*sigma_1yr):.0f}  –  "
      f"${CURRENT_PRICE + 2*sigma_1yr:.0f}")
print(f"  {'─'*60}")
if sigma_needed_bear > 0:
    print(f"  Bear ${SCENARIOS['BEAR'][2]} requires:  "
          f"~{sigma_needed_bear:.1f}σ price move  "
          f"{'(unusual — requires fundamental break)' if sigma_needed_bear > 1.5 else '(within normal range)'}")
else:
    print(f"  Bear ${SCENARIOS['BEAR'][2]}: already realized — current price is above bear target.")
print(f"  No dividend buffer — position sizing critical given {VOL_ANNUAL_PCT*100:.0f}% vol.")
print(f"  → COIN is a high-conviction bet on BTC cycle + regulatory thesis. Size appropriately.")

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
