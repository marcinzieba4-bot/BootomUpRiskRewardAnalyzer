#!/usr/bin/env python3
"""
XTB Signal Model  v2
─────────────────────
XTB S.A. (WSE: XTB)  ·  Retail CFD / Investment Broker

⚠  Prices and EPS are in PLN (Polish złoty). XTB trades on the Warsaw
   Stock Exchange; roughly PLN 4.1 = USD 1.0 (May 2026).

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 58.0      # PLN
REQUIRED_RETURN  = 0.15
HORIZON_YEARS    = 2

SCENARIOS = {
    "BEAR":  ( 2.5,   8,   20, "Low vol; crypto winter; margin pressure; client churn"),
    "BASE":  ( 4.5,  12,   54, "Moderate activity; steady client growth; ECB rates hold"),
    "BULL":  ( 7.0,  14,   98, "Elevated vol; crypto active; ETF platform growing fast"),
    "XBULL": (10.0,  16,  160, "Retail frenzy + crypto cycle + ETF re-rating to fintech"),
}

# ── CLIENT ECONOMICS CALCULATOR (XTB-specific structural feature) ──────────────
REGISTERED_CLIENTS_M     = 1.54
ACTIVE_CLIENTS_K         = 650
ACTIVATION_RATE          = ACTIVE_CLIENTS_K / (REGISTERED_CLIENTS_M * 1000)
REVENUE_PER_CLIENT_CURR  = 4_200
REVENUE_PER_CLIENT_NORM  = 2_200
NEW_CLIENTS_PER_YEAR_K   = 420
ETFINVEST_CLIENTS_K      = 380
ETFINVEST_AVG_AUM_PLN    = 8_500

def client_economics():
    floor_rev  = (ACTIVE_CLIENTS_K * 1000) * REVENUE_PER_CLIENT_NORM / 1e9
    curr_rev   = (ACTIVE_CLIENTS_K * 1000) * REVENUE_PER_CLIENT_CURR / 1e9
    etf_aum    = ETFINVEST_CLIENTS_K * 1000 * ETFINVEST_AVG_AUM_PLN / 1e9
    etf_rev    = etf_aum * 0.005
    future_k   = ACTIVE_CLIENTS_K + NEW_CLIENTS_PER_YEAR_K * 2 * ACTIVATION_RATE
    future_floor_rev = future_k * 1000 * REVENUE_PER_CLIENT_NORM / 1e9
    return floor_rev, curr_rev, etf_aum, etf_rev, future_k, future_floor_rev

# ── SIGNALS ───────────────────────────────────────────────────────────────────
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("VIX — CBOE Volatility Index",      "pts",
      10.0,  15.0,  22.0,  30.0,  22.0, True,
     "Low vol; retail traders inactive; no CFD spread revenue"),

    ("XTB active clients — YoY growth",  "% YoY",
       5.0,  20.0,  40.0,  65.0,  52.0, True,
     "Low vol drives client churn; no new registrations"),

    ("Crypto market cap — YoY",          "% YoY",
     -45.0, -25.0,   5.0,  40.0, -20.0, True,
     "Crypto bear; BTC/ETH CFD volumes collapse; retail disengages"),

    ("European equity trading vol YoY",  "% YoY",
      -5.0,   5.0,  15.0,  30.0,  15.0, True,
     "European vol dries; CFD demand from EU clients collapses"),

    ("ECB deposit rate",                 "%",
       0.5,   1.0,   2.5,   4.0,   2.5, True,
     "Rate cuts to zero; deposit interest income evaporates"),

    ("IG Group revenue — YoY",           "% YoY",
     -10.0,   0.0,  10.0,  25.0,  12.0, True,
     "Peer revenue falls; leading indicator of XTB Q decline"),
]
WEIGHTS = [0.25, 0.20, 0.15, 0.15, 0.15, 0.10]

STRUCTURAL_FACTORS = [
    ("ESMA leverage restriction / regulatory risk",  -0.8, 0.30),
    ("ETF / investment platform client stickiness",   0.5, 0.20),
    ("Bank and neobank competitive entry",           -0.3, 0.20),
    ("Net cash + high dividend yield",                0.5, 0.15),
    ("Warsaw listing / emerging-market discount",    -0.3, 0.15),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
EPP_TODAY_EPS    = 3.00     # FY2025E EPS (PLN; normalised from record FY2024)
EPP_MIN_PE       = 8.0      # min viable P/E (online broker at crypto/vol trough)
EPP_HISTORICAL   = 22.0     # historical EPP v1 (from 2022 floor)
EPP_REGIME_NOTE  = "(crypto vol + ETF stickiness raises floor from pure-CFD 6x to 8x)"

# ── CONSERVATIVE GROWTH (2-yr, base-minus) ────────────────────────────────────
CONS_SIGNALS = [
    ("VIX",                18.0,  "18 pts (vs 22; vol normalises lower)"),
    ("XTB active",         25.0,  "+25% YoY (vs +52%; growth decelerates)"),
    ("Crypto market",      -5.0,  "-5% YoY (vs -20%; crypto stabilises)"),
    ("European equity",     8.0,  "+8% YoY (vs +15%; trading vol moderates)"),
    ("ECB deposit",         2.0,  "2.0% (vs 2.5%; ECB cuts one more time)"),
    ("IG Group",            5.0,  "+5% YoY (vs +12%; peer growth cools)"),
]
CONS_EPS_CAGR = 0.08     # 8%/yr conservative (moderate vol environment)
CONS_EXIT_PE  = 11.0     # 11x exit (no re-rating; vol-dependent earnings)
CONS_DIVIDEND = 1.60     # XTB pays dividends; approx PLN 1.60/share (60% payout on PLN ~3 EPS)

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.45    # high vol; small-cap + crypto sensitive
VOL_BETA       = 1.40    # above market
VOL_52W_LOW    = 35.0    # PLN
VOL_52W_HIGH   = 75.0    # PLN
VOL_DIVIDEND   = 1.60    # PLN

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

def market_implied_composite(target_ev, tolerance=0.5):
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

floor_rev, curr_rev, etf_aum, etf_rev, future_k, future_floor_rev = client_economics()

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
print(f"  XTB  ·  XTB S.A.  ·  PLN {CURRENT_PRICE:.2f}  ·  CFD / Investment Broker  [PLN]")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)
print(f"  ⚠  All prices and EPS in PLN (Polish złoty).  PLN/USD ≈ 0.24")

# Client economics (keep before ① as XTB-specific feature)
print(f"\n  CLIENT ECONOMICS  (revenue = clients × activity × volatility)")
print("  " + "─" * (W-2))
print(f"  Total registered clients:                {REGISTERED_CLIENTS_M*1e6:>10,.0f}")
print(f"  Active clients (last 12M):               {ACTIVE_CLIENTS_K*1000:>10,.0f}  ({ACTIVATION_RATE*100:.0f}% activation rate)")
print(f"  New registrations per year (est.):       {NEW_CLIENTS_PER_YEAR_K*1000:>10,.0f}")
print(f"  Revenue/active client — current yr:      PLN {REVENUE_PER_CLIENT_CURR:>6,}  (elevated vol)")
print(f"  Revenue/active client — 10yr normal:     PLN {REVENUE_PER_CLIENT_NORM:>6,}  (normalised)")
print(f"  {'─'*60}")
print(f"  Floor revenue (current base × normal):   PLN {floor_rev:.1f}B / yr")
print(f"  In 2yrs at current acq pace, active:     ~{future_k:>6,.0f}K  (~{future_k/1000:.1f}M clients)")
print(f"  → 2yr floor (growing base × normal):     PLN {future_floor_rev:.1f}B / yr")
print(f"\n  ETF/savings platform clients: {ETFINVEST_CLIENTS_K*1000:,.0f}   AUM: PLN {etf_aum:.1f}B")
print(f"  Recurring fee-equivalent (~0.5% AUM):    PLN {etf_rev*1000:.0f}M / yr  (re-rating trigger)")

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
          f"(back-solved from PLN {CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% hurdle)")
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
      f"~PLN {expected_price(bear_probs):.0f}  (model)  /  PLN {SCENARIOS['BEAR'][2]} (defined)")
print(f"  Bear probability (proxy model):  {proxy_probs['BEAR']*100:.1f}%")
print(f"\n  KEY TRIGGER: VIX falls to 10 (extreme complacency) + crypto bear market")
print(f"  simultaneously. XTB spread revenue collapses; high fixed-cost base causes")
print(f"  operating leverage inversion. Net income falls 60%+.")

# ── ③ UPDATED EPP ────────────────────────────────────────────────────────────
print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS:           PLN {EPP_TODAY_EPS:.2f}  (FY2025E, normalised from record)")
print(f"  Min viable P/E at max pessimism:   {EPP_MIN_PE:.0f}x  {EPP_REGIME_NOTE}")
print(f"  {'─'*60}")
print(f"  UPDATED EPP:                      PLN {epp_updated:.0f}/share")
print(f"  Historical EPP (v1):              PLN {EPP_HISTORICAL:.0f}/share")
print(f"  Current PLN {CURRENT_PRICE:.0f} vs Updated EPP PLN {epp_updated:.0f}:  {epp_gap_pct:+.0f}%  "
      f"{'✓ cushion' if epp_gap_pct >= 0 else '← in distressed zone'}")
print(f"  Bear PLN {SCENARIOS['BEAR'][2]} vs Updated EPP PLN {epp_updated:.0f}:  {bear_vs_epp_pct:+.0f}%  "
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

print(f"\n  Conservative 2yr EPS:   PLN {EPP_TODAY_EPS:.2f} × (1+{CONS_EPS_CAGR*100:.0f}%)² = PLN {cons_eps_2yr:.2f}")
print(f"  At {CONS_EXIT_PE:.0f}x P/E (conservative):  PLN {cons_price_2yr:.0f}/share")
if CONS_DIVIDEND > 0:
    print(f"  + Cumul. dividends (2yr):  +PLN {cons_div_2yr:.2f}/share")
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:     PLN {cons_price_2yr:.0f}  "
      f"({'▲' if cons_price_2yr > CURRENT_PRICE else '▼'}{abs(cons_price_2yr - CURRENT_PRICE):.0f} from PLN {CURRENT_PRICE:.0f})")
print(f"  Conservative total return:  {cons_total_ret:+.0f}% over 2yr  = {cons_annual_ret:+.0f}%/yr")
print(f"\n  Key: even moderate vol environment generates 8%+/yr EPS growth as client")
print(f"  base compounds. ETF AUM growth is the re-rating catalyst to 14-16x.")

# ── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print(f"\n  ⑤ VOLATILITY CONTEXT  [all in PLN]")
print("  " + "─" * (W-2))
print(f"  52-week range:        PLN {VOL_52W_LOW:.0f}  –  PLN {VOL_52W_HIGH:.0f}")
print(f"  Annual dividend:      PLN {VOL_DIVIDEND:.2f}/share  "
      f"(yield {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%; 60% payout policy)")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized  (high; crypto + vol-sensitive)")
print(f"  Beta vs S&P 500:      {VOL_BETA:.2f}  (above market; small-cap cyclical)")
print(f"  1-sigma range (1yr):  PLN {vol_low_1yr:.0f}  –  PLN {vol_high_1yr:.0f}  "
      f"(PLN {CURRENT_PRICE:.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  2-sigma range (1yr):  PLN {max(0, CURRENT_PRICE - 2*sigma_1yr):.0f}  –  "
      f"PLN {CURRENT_PRICE + 2*sigma_1yr:.0f}")
print(f"  {'─'*60}")
print(f"  Bear PLN {SCENARIOS['BEAR'][2]} requires:  "
      f"~{sigma_needed_bear:.1f}σ price move  "
      f"{'(unusual — requires fundamental break)' if sigma_needed_bear > 1.5 else '(within normal range)'}")
print(f"  Dividend buffer:      PLN {VOL_DIVIDEND:.2f}/yr absorbs ~{VOL_DIVIDEND/CURRENT_PRICE*100:.1f}% "
      f"of annual price drawdown")
print(f"  → XTB yield today: {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%.  Compare to Polish gov bonds ~5.5%.")

# ── ⑥ PROBABILITY DISTRIBUTION ───────────────────────────────────────────────
print(f"\n  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
print("  " + "─" * (W-2))
print(f"  {'Scenario':<8}  {'Price':>7}  {'Proxy%':>7}  {'Market%':>8}  "
      f"{'Gap':>6}  Description")
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    eps, mult, price, narr = SCENARIOS[k]
    pp  = proxy_probs[k]
    mp  = mkt_probs[k] if mkt_probs else 0
    gap_pp = pp - mp
    print(f"  {k:<8}  PLN {price:>4}  {pp*100:>6.1f}%  {mp*100:>7.1f}%  "
          f"{gap_pp*100:>+6.1f}pp  {narr}")

print(f"\n  Proxy EV (2yr): PLN {proxy_ev:.0f}  /  Market EV: PLN {mkt_ev:.0f}  /  "
      f"Current: PLN {CURRENT_PRICE:.0f}")
print(f"  Conservative EV (2yr, ④): PLN {cons_price_2yr:.0f} + PLN {cons_div_2yr:.2f} divs = "
      f"PLN {cons_price_2yr + cons_div_2yr:.0f} total value")

print()
print("═" * W)
