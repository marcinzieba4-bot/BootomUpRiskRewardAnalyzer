#!/usr/bin/env python3
"""
COIN Signal Model
──────────────────
Same framework as avgo_signal_model.py applied to Coinbase.

Key structural difference from AVGO:
  ~60% transaction revenue  — highly volatile, driven by BTC price and volume
  ~40% subscription/services — growing, recurring floor (USDC, staking, Coinbase One)

The market-implied vs proxy gap tells you whether the stock fairly
reflects available leading data, or is mis-pricing a recovery/decline.

Run: python coin_signal_model.py
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 194.0
REQUIRED_RETURN = 0.15        # annual cost of equity; 2yr discount = 1.32x
HORIZON_YEARS   = 2

# Scenario 2-year price targets (FY2027 EPS × exit multiple)
# Exit multiples: crypto exchange stocks compress sharply when growth slows.
# Coinbase's multiple also reflects optionality on stablecoin/Base/regulatory.
SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  ( 2.0,   12,    24,  "BTC stays $60-75K; extended crypto winter; volumes -40%"),
    "BASE":  (10.0,   22,   220,  "BTC recovers $120-140K; stablecoin bill passes; sub rev $4B+"),
    "BULL":  (18.0,   25,   450,  "BTC $160K+; USDC $150B; Base L2 significant DeFi revenue"),
    "XBULL": (28.0,   28,   784,  "BTC $200K+; USDC = global payments layer; regulatory goldilocks"),
}

# ── REVENUE FLOOR CALCULATOR (unique to COIN — not in AVGO model) ─────────
# Subscription/services revenue is largely independent of BTC price.
# Shows minimum survivable revenue even in bear scenario.
USDC_MARKET_CAP_B    = 75.0    # current USDC market cap ($B)
USDC_YIELD           = 0.04    # approximate reserve yield (Fed funds rate)
COINBASE_USDC_SHARE  = 0.50    # Coinbase's share of USDC reserve income
STAKING_ANNUAL_B     = 0.72    # FY2025 staking revenue ($B)
COINBASE_ONE_SUBS_M  = 0.95    # Coinbase One subscribers (millions)
COINBASE_ONE_ARPU    = 29.99   # monthly subscription fee ($)

def sub_revenue_floor():
    usdc_rev  = USDC_MARKET_CAP_B * USDC_YIELD * COINBASE_USDC_SHARE
    coinb1_rev = COINBASE_ONE_SUBS_M * COINBASE_ONE_ARPU * 12 / 1000  # $B
    return usdc_rev + STAKING_ANNUAL_B + coinb1_rev

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
# Chosen because they are available BEFORE Coinbase reports and directly
# drive one of its two revenue buckets.
#
# (name, value, unit, base_floor, bull_floor, xbull_floor, higher_is_better,
#  what_it_drives_in_COIN)
SIGNALS = [
    # BTC price YoY change — primary driver of retail/institutional trading volume
    # and overall crypto sentiment. 70%+ correlation with Coinbase transaction revenue.
    # Current: BTC $77K vs May 2025 avg $103K → -26% YoY
    ("Bitcoin price — YoY change",      -26.0, "% YoY",   -30, 20,  80, True,
     "transaction revenue (70%+ corr); market sentiment; retail engagement"),

    # Bitcoin spot ETF monthly net flows — institutional demand; leads retail
    # by 1-2 months. April 2026: $2.44B — strongest month since Oct 2025.
    ("BTC spot ETF flows (monthly)",      2.44, "$B/mo",     0,  1,   3, True,
     "institutional on-ramp; leads retail trading vol; OTC desk revenue"),

    # USDC market cap — Coinbase earns ~50% of USDC reserve interest.
    # At $75B USDC × 4% yield × 50% = ~$1.5B annual revenue.
    # This is the anti-cyclical anchor of the subscription segment.
    ("USDC market cap",                  75.0,  "$B",       30, 60,  90, True,
     "direct stablecoin revenue (~$1.5B annual at current levels)"),

    # Global crypto spot volume YoY — leads Coinbase transaction revenue.
    # Fell ~48% from Oct 2025 peak. Coinbase transaction rev expected -25 to -34% YoY.
    ("Global crypto spot vol — YoY",    -30.0, "% YoY",   -40, -10, 30, True,
     "transaction revenue floor; retail + institutional trading activity"),

    # US crypto regulatory clarity — scored 1-4 based on legislative progress.
    # Current: stablecoin bill bipartisan, moving through Congress → BULL.
    # XBULL would require comprehensive market structure law + SEC clarity.
    # Scored as ordinal: 1=hostile, 2=status quo, 3=stablecoin bill passing, 4=full framework
    ("US crypto regulation clarity",      3.0,  "/4",        1,  2,   4, True,
     "enables USDC payments, institutional custody, Base L2 DeFi; expands TAM"),

    # Subscription/services QoQ trend — Coinbase's own recurring revenue.
    # Q4 2025 est ~$720M; Q1 2026 guided $550-630M (mid $590M) → -18% QoQ.
    # Decline driven by lower ETH staking rates + lower USDC yield (rate cuts).
    # Bear signal for near-term but structural ceiling, not collapse.
    ("Sub/services revenue — QoQ",      -18.0, "% QoQ",   -10,  5,  15, True,
     "recurring revenue floor; USDC + staking + Coinbase One; margin anchor"),
]
WEIGHTS = [0.30, 0.20, 0.15, 0.15, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("US crypto regulatory clarity improving",        1.0, 0.30),
    ("BTC single-driver revenue concentration",      -0.8, 0.25),
    ("Exchange commoditisation / fee compression",   -0.5, 0.20),
    ("Base L2 ecosystem optionality",                 0.5, 0.15),
    ("Institutional custody moat",                    0.3, 0.10),
]


FLOOR_DATA = {
    "trough_2022":        33.0,
    "cum_fcf_per_share":  22.9,
    "debt_delta":         -12.5,   # +ve = debt grew (floor lower); -ve = balance sheet improved
    "reflation":           0.17,   # cumul. US CPI Jan 2022 - May 2026
}

def worst_case_floor():
    t, refl = FLOOR_DATA["trough_2022"], FLOOR_DATA["reflation"]
    fcf, ddt = FLOOR_DATA["cum_fcf_per_share"], FLOOR_DATA["debt_delta"]
    ref_adj = t * (1 + refl)
    floor   = ref_adj + fcf - ddt
    bear_p  = SCENARIOS["BEAR"][2]
    gap_pct = (floor - CURRENT_PRICE) / CURRENT_PRICE * 100
    bvf_pct = (bear_p - floor) / floor * 100
    return ref_adj, floor, gap_pct, bear_p, bvf_pct

# ── SCORING ───────────────────────────────────────────────────────────────
def score_signal(val, base_f, bull_f, xbull_f, hib):
    if hib:
        if val >= xbull_f: return 4
        if val >= bull_f:  return 3
        if val >= base_f:  return 2
        return 1
    else:
        if val <= base_f:  return 4
        if val <= bull_f:  return 3
        if val <= xbull_f: return 2
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

# ── MAIN ──────────────────────────────────────────────────────────────────
W = 72

scored = [(name, val, unit, score_signal(val, bf, bull_f, xf, hib), w, rt)
          for (name, val, unit, bf, bull_f, xf, hib, rt), w in zip(SIGNALS, WEIGHTS)]
proxy_composite  = sum(s * w for *_, s, w, _ in scored)
sca              = sum(s * w for _, s, w in STRUCTURAL_FACTORS)
adj_composite    = proxy_composite + sca
proxy_probs      = softmax_probs(proxy_composite)
proxy_ev         = expected_price(proxy_probs)

market_target_ev  = CURRENT_PRICE * ((1 + REQUIRED_RETURN) ** HORIZON_YEARS)
mkt_composite, mkt_probs = market_implied_composite(market_target_ev)
mkt_ev = expected_price(mkt_probs) if mkt_probs else market_target_ev

floor = sub_revenue_floor()

print()
print("═" * W)
print("  COIN SIGNAL MODEL  —  proxy vs. market-implied probability")
print("═" * W)

# Revenue floor
print(f"\n  SUBSCRIPTION REVENUE FLOOR  (holds regardless of BTC price)")
print("  " + "─" * (W-2))
print(f"  USDC revenue  ({USDC_MARKET_CAP_B:.0f}B × {USDC_YIELD*100:.0f}% yield × {COINBASE_USDC_SHARE*100:.0f}% share)   ${USDC_MARKET_CAP_B*USDC_YIELD*COINBASE_USDC_SHARE:.2f}B / yr")
print(f"  Staking revenue (FY2025 run-rate)                   ${STAKING_ANNUAL_B:.2f}B / yr")
print(f"  Coinbase One  ({COINBASE_ONE_SUBS_M*1000:.0f}K subs × ${COINBASE_ONE_ARPU:.0f}/mo)          ${COINBASE_ONE_SUBS_M*COINBASE_ONE_ARPU*12/1000:.2f}B / yr")
print(f"  ─────────────────────────────────────────────────────")
print(f"  Total recurring floor                               ${floor:.2f}B / yr")
print(f"  As % of FY2025 total revenue ($7.18B):              {floor/7.18*100:.0f}%")
print(f"  → Even in bear scenario, ~${floor:.1f}B/yr is structurally anchored.")

# Signal scorecard
print(f"\n  PROXY SIGNAL SCORECARD")
print(f"  {'Signal':<38}{'Value':>9}  Wt   Score")
print("  " + "─" * (W-2))
for name, val, unit, s, w, rt in scored:
    bar = "█" * s + "░" * (4 - s)
    print(f"  {name:<38}{val:>+7.1f}{unit[0]}  {w*100:.0f}%  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:   {proxy_composite:.2f} / 4.00")
if mkt_composite:
    print(f"  Market composite:  {mkt_composite:.2f} / 4.00  "
          f"(back-solved from ${CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% reqd return)")
    gap = proxy_composite - mkt_composite
    sign = "+" if gap >= 0 else ""
    print(f"  Gap (proxy − mkt): {sign}{gap:.2f}  ← the trade")

# Structural overlay
print(f"\n  STRUCTURAL RISK OVERLAY  (analyst-assessed; beyond proxy signals)")
print("  " + "─" * (W-2))
print(f"  {'Factor':<44}  {'Score':>5}  {'Wt':>3}   {'Adj':>5}")
for desc, score, wt in STRUCTURAL_FACTORS:
    adj_c = score * wt
    arrow = "▲" if score > 0 else "▼"
    print(f"  {desc:<44}  {score:>+5.1f}  {wt*100:>3.0f}%  {adj_c:>+5.2f}  {arrow}")
print(f"  {'─'*68}")
print(f"  Structural adj. (SCA):     {sca:>+6.2f}")
print(f"  Adjusted composite:         {adj_composite:.2f}  "
      f"(proxy {proxy_composite:.2f} {'+' if sca >= 0 else ''}{sca:.2f})")
if mkt_composite:
    adj_gap = adj_composite - mkt_composite
    if   adj_gap >  0.50: _verdict = "UNDERVALUED"
    elif adj_gap >  0.20: _verdict = "MODESTLY UNDERVALUED"
    elif adj_gap > -0.20: _verdict = "FAIRLY VALUED"
    elif adj_gap > -0.50: _verdict = "MODESTLY OVERVALUED"
    else:                 _verdict = "OVERVALUED"
    print(f"  Market composite:          {mkt_composite:.2f}")
    print(f"  ADJUSTED GAP:             {adj_gap:>+6.2f}  ← {_verdict}")

# Probability table
print(f"\n  {'Scenario':<10}  {'Proxy':>8}  {'Market':>8}  {'Gap':>8}  "
      f"{'EPS':>6}  {'Mult':>5}  {'Price':>7}  Narrative")
print("  " + "─" * (W-2))
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    eps, mult, price, narr = SCENARIOS[k]
    pp  = proxy_probs[k]
    mp  = mkt_probs[k] if mkt_probs else 0
    gap_pp = pp - mp
    sign = "+" if gap_pp >= 0 else ""
    short_narr = narr[:28] + "…"
    print(f"  {k:<10}  {pp*100:>7.1f}%  {mp*100:>7.1f}%  "
          f"{sign}{gap_pp*100:>6.1f}pp  ${eps:>5}  {mult:>4}x  ${price:<6}  {short_narr}")

print(f"\n  Prob-weighted 2yr:  proxy ${proxy_ev:.0f}  /  market ${mkt_ev:.0f}")
print(f"  Current price: ${CURRENT_PRICE:.0f}")

# Downside floor
_ref_adj, _floor, _gap_pct, _bear_p, _bvf = worst_case_floor()
_t   = FLOOR_DATA["trough_2022"]
_fcf = FLOOR_DATA["cum_fcf_per_share"]
_ddt = FLOOR_DATA["debt_delta"]
print(f"\n  DOWNSIDE FLOOR  (why the 2022 low cannot recur at same nominal price)")
print("  " + "─" * (W-2))
print(f"  2022 reference trough:                  ${_t:.0f}")
print(f"    + Reflation (+17% cumul. CPI since 2022):  +${_t*0.17:.0f}  \u2192  ${_t*1.17:.0f}")
print(f"    + Cumul. FCF earned FY2023-2025:           +${_fcf:.0f}  \u2192  ${_t*1.17+_fcf:.0f}")
if _ddt > 0:
    print(f"    - Net debt increase since 2022 / share:    -${_ddt:.0f}  \u2192  ${_floor:.0f}  (leverage drag)")
else:
    print(f"    + Balance sheet improvement / share:       +${-_ddt:.0f}  \u2192  ${_floor:.0f}")
print(f"  {chr(32)*4}{chr(45)*62}")
print(f"  ANALYTICAL FLOOR (2026 equiv.):         ${_floor:.0f}")
print(f"  Current price:                          ${CURRENT_PRICE:.0f}   downside to floor: {_gap_pct:+.0f}%")
if _bvf >= 0:
    print(f"  BEAR scenario (${_bear_p:.0f}):   BEAR is +{_bvf:.0f}% above floor  \u2713  adequate cushion")
else:
    print(f"  BEAR scenario (${_bear_p:.0f}):   BEAR is {_bvf:.0f}% BELOW floor  \u2190 structural break scenario")
print(f"  \u2192 The 2022 low (${_t:.0f}) cannot recur: ${_fcf:.0f}/share FCF already locked in,")
print(f"    17% inflation raised every nominal anchor. Floor ratchets up each year.")

# Verdict
print(f"\n  WHAT THE GAP MEANS")
print("  " + "─" * (W-2))
gap = (proxy_composite - mkt_composite) if mkt_composite else 0
print(f"""  Proxy composite {proxy_composite:.2f}  vs  market-implied {mkt_composite:.2f}.
  Gap = {gap:+.2f}  (vs AVGO's gap of +1.41 — COIN signals are FAR more mixed).

  The small gap means: the market is approximately pricing what the
  proxy signals justify. No obvious mispricing from public data.

  THE REAL THESIS IS BINARY — it's almost entirely BTC price:

    BTC stays $60-80K   → transaction revenue stays depressed,
                          EPS ~$2-4, stock drifts toward $50-100.
                          Sub/services floor ($3B) prevents collapse.

    BTC recovers $130K+ → transaction volumes recover, EPS $10+,
                          regulatory tailwind accelerates stablecoin rev,
                          stock re-rates toward $200-300.

    BTC $160K+ (BULL)   → USDC demand explodes, Base L2 earns real fees,
                          Coinbase One crosses 2M subs, EPS $18+, $400+.

  WHAT MAKES COIN DIFFERENT FROM AVGO:
    • Proxy signals are mixed (2.35) not extreme-bullish (3.55)
    • 6 independent signals collapse into 1 underlying driver: BTC price
    • The subscription floor ($3B/yr) limits downside but not enough to
      support $194 if BTC enters multi-year bear market
    • Regulatory optionality (stablecoin bill) is the one genuinely
      non-consensus, not-yet-priced asymmetric upside catalyst

  WHAT WOULD MOVE THE NEEDLE:
    • BTC ETF flows crossing $4B+/month (institutional FOMO signal)
    • USDC crossing $100B market cap (stablecoin revenue jumps ~33%)
    • Stablecoin/Clarity Act Senate passage (re-rates the whole segment)
    • Base L2 transaction fees becoming material (currently near-zero)""")
print()
print("═" * W)
