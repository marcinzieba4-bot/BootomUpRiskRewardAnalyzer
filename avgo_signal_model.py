#!/usr/bin/env python3
"""
AVGO Signal Model — v2
────────────────────────
Core question: what does the current stock price ($417) EMBED, and do
proxy signals justify a different distribution?

The gap between (market-implied score) and (proxy score) is the trade.
NOT the gap between proxy signals and last quarter's reported data.

Run: python avgo_signal_model.py
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 417.0
REQUIRED_RETURN  = 0.15        # annual cost of equity; 2yr discount = 1.32x
HORIZON_YEARS    = 2

# Scenario 2-year price targets  (EPS × exit multiple)
# Exit multiples compress at higher EPS scenarios — AVGO won't get 40x when
# growing at 15% vs 40x when growing at 35%. This is the key discipline.
SCENARIOS = {
    #           EPS    mult   price
    "BEAR":  ( 8.50,  22,    187),
    "BASE":  (17.55,  30,    526),   # consensus FY2028E at 30x
    "BULL":  (22.00,  35,    770),
    "XBULL": (27.00,  33,   891),   # 33x not 40x — growth decelerating even in XBULL
}

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
#  (name, value, unit, base_floor, bull_floor, xbull_floor, higher_is_better, read-through)
SIGNALS = [
    ("Hyperscaler CapEx YoY",       77.0, "% YoY",       10,  30,  60, True,
     "upstream order flow for AI ASICs; 1-2Q lead"),
    ("TSMC HPC % of revenue",       61.0, "% of rev",    50,  57,  62, True,
     "actual fab utilisation; AVGO N3/N5 ASIC slots"),
    ("Arista Networks rev YoY",     35.1, "% YoY",       15,  25,  35, True,
     "AI cluster Ethernet; AVGO Jericho/Tomahawk volume"),
    ("Nutanix ARR YoY (inverse)",   18.0, "% inv",       10,  20,  30, False,
     "VMware churn proxy — low NTNX growth = VMware sticky"),
    ("Super Micro rev YoY",        123.0, "% YoY",       20,  60, 100, True,
     "GPU rack deployments; AI capex flowing"),
    ("CDW commercial YoY",           9.6, "% YoY",        0,   5,  10, True,
     "enterprise IT health; VMware channel + non-AI semi"),
]
WEIGHTS = [0.30, 0.20, 0.15, 0.15, 0.10, 0.10]

# ── STRUCTURAL RISK OVERLAY ──────────────────────────────────────────────
STRUCTURAL_FACTORS = [
    ("Custom ASIC switching cost moat",               1.5, 0.20),
    ("Hyperscaler CapEx flow-through uncertainty",   -1.0, 0.40),
    ("Hock Tan capital allocation record",             1.0, 0.15),
    ("China / export control exposure",               -0.5, 0.15),
    ("VMware integration execution",                   0.5, 0.10),
]


FLOOR_DATA = {
    "trough_year":        2022,
    "trough_price":       44.0,
    "cum_fcf_per_share":  11.9,
    "debt_delta":         5.7,     # +ve = debt grew (EPP lower); -ve = improved
    "structural_delta":   15.0,  # +ve = fundamentals improved; -ve = weaker today
    "cpi_since_trough":   0.17,     # cumul. US CPI from trough_year to May 2026
}

def worst_case_floor():
    yr     = FLOOR_DATA["trough_year"]
    t      = FLOOR_DATA["trough_price"]
    cpi    = FLOOR_DATA["cpi_since_trough"]
    fcf    = FLOOR_DATA["cum_fcf_per_share"]
    ddt    = FLOOR_DATA["debt_delta"]
    sdelta = FLOOR_DATA["structural_delta"]
    ref_adj = t * (1 + cpi)
    epp     = ref_adj + fcf - ddt + sdelta
    bear_p  = SCENARIOS["BEAR"][2]
    gap_pct = (CURRENT_PRICE - epp) / epp * 100   # +ve = above EPP; -ve = below
    bvf_pct = (bear_p - epp) / epp * 100
    return ref_adj, epp, gap_pct, bear_p, bvf_pct

# ── SCORING ───────────────────────────────────────────────────────────────
def score_signal(val, base_f, bull_f, xbull_f, hib):
    if hib:
        if val >= xbull_f: return 4
        if val >= bull_f:  return 3
        if val >= base_f:  return 2
        return 1
    else:  # inverse: lower is better; thresholds are ceilings
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

# ── MARKET-IMPLIED SCORE ──────────────────────────────────────────────────
# Back-solve: find the composite score whose probability-weighted price
# equals what $417 implies after applying the required return discount.
# Market EV (undiscounted 2-yr) = current_price × (1 + r)^n
def market_implied_composite(target_ev, tolerance=0.5):
    for c in [x / 100 for x in range(100, 401)]:   # 1.00 to 4.00
        probs = softmax_probs(c)
        ev = expected_price(probs)
        if abs(ev - target_ev) < tolerance:
            return round(c, 2), probs
    return None, None

# ── MAIN ──────────────────────────────────────────────────────────────────
W = 70

# Proxy scoring
scored = [(name, val, unit, score_signal(val, bf, bull_f, xf, hib), w, rt)
          for (name, val, unit, bf, bull_f, xf, hib, rt), w in zip(SIGNALS, WEIGHTS)]
proxy_composite  = sum(s * w for *_, s, w, _ in scored)
sca           = sum(s * w for _, s, w in STRUCTURAL_FACTORS)
adj_composite = proxy_composite + sca
proxy_probs      = softmax_probs(proxy_composite)
proxy_ev         = expected_price(proxy_probs)

# Market-implied
discount_factor   = (1 + REQUIRED_RETURN) ** HORIZON_YEARS
market_target_ev  = CURRENT_PRICE * discount_factor
mkt_composite, mkt_probs = market_implied_composite(market_target_ev)
mkt_ev = expected_price(mkt_probs) if mkt_probs else market_target_ev

print()
print("═" * W)
print("  AVGO SIGNAL MODEL  —  proxy vs. market-implied probability")
print("═" * W)

# Signal scorecard
print(f"\n  {'Signal':<35}{'Value':>9}  Wt   Score")
print("  " + "─" * (W-2))
for name, val, unit, s, w, rt in scored:
    bar = "█" * s + "░" * (4 - s)
    print(f"  {name:<35}{val:>7.1f}{unit[0]}  {w*100:.0f}%  {ICONS[s]}  {bar}")
print(f"\n  Proxy composite:   {proxy_composite:.2f} / 4.00")
if mkt_composite:
    print(f"  Market composite:  {mkt_composite:.2f} / 4.00  "
          f"(back-solved from ${CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% reqd return)")
    gap = proxy_composite - mkt_composite
    print(f"  Gap (proxy − mkt): {gap:+.2f}  ← this is the trade")

# Probability comparison
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

print(f"\n  {'Scenario':<10}  {'Proxy':>8}  {'Market':>8}  {'Gap':>8}  "
      f"{'EPS':>6}  {'Multiple':>8}  {'Price':>7}")
print("  " + "─" * (W-2))
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    eps, mult, price = SCENARIOS[k]
    pp  = proxy_probs[k]
    mp  = mkt_probs[k] if mkt_probs else 0
    gap = pp - mp
    sign = "+" if gap >= 0 else ""
    print(f"  {k:<10}  {pp*100:>7.1f}%  {mp*100:>7.1f}%  "
          f"{sign}{gap*100:>6.1f}pp  ${eps:>5.2f}  {mult:>6}x      ${price}")

print(f"\n  Prob-weighted 2yr price:  proxy ${proxy_ev:.0f}  /  market ${mkt_ev:.0f}")
print(f"  Current price: ${CURRENT_PRICE:.0f}")

# The answer to the user's question
# Equivalent Pessimism Price
_ref_adj, _epp, _gap_pct, _bear_p, _bvf = worst_case_floor()
_yr     = FLOOR_DATA["trough_year"]
_t      = FLOOR_DATA["trough_price"]
_cpi    = FLOOR_DATA["cpi_since_trough"]
_fcf    = FLOOR_DATA["cum_fcf_per_share"]
_ddt    = FLOOR_DATA["debt_delta"]
_sdelta = FLOOR_DATA["structural_delta"]
print(f"\n  EQUIV. PESSIMISM PRICE  (if {_yr} pessimism returned today, price would be:)")
print("  " + "─" * (W-2))
print(f"  {_yr} pessimism trough:                  ${_t:.0f}")
print(f"    + Reflation (+{_cpi*100:.0f}% cumul. CPI {_yr}→2026):   +${_t*_cpi:.0f}  \u2192  ${_t*(1+_cpi):.0f}")
print(f"    + Cumul. FCF earned since {_yr}:              +${_fcf:.0f}  \u2192  ${_t*(1+_cpi)+_fcf:.0f}")
if _ddt > 0:
    print(f"    - Net debt increase since {_yr} / share:    -${_ddt:.0f}  \u2192  ${_t*(1+_cpi)+_fcf-_ddt:.0f}  (leverage drag)")
else:
    print(f"    + Balance sheet improvement / share:        +${-_ddt:.0f}  \u2192  ${_t*(1+_cpi)+_fcf-_ddt:.0f}")
if _sdelta > 0:
    print(f"    + Structural improvement since {_yr}:       +${_sdelta:.0f}  \u2192  ${_epp:.0f}  (moat/earnings-power \u2191)")
elif _sdelta < 0:
    print(f"    - Structural deterioration since {_yr}:     -${-_sdelta:.0f}  \u2192  ${_epp:.0f}  (weaker business today)")
print(f"  {chr(32)*4}{chr(45)*62}")
print(f"  EQUIV. PESSIMISM PRICE (EPP, 2026):     ${_epp:.0f}")
if _gap_pct >= 0:
    print(f"  Current price:   ${CURRENT_PRICE:.0f}  \u2192  +{_gap_pct:.0f}% above EPP  \u2713  price embeds premium over pure pessimism")
else:
    print(f"  Current price:   ${CURRENT_PRICE:.0f}  \u2192  {_gap_pct:.0f}% BELOW EPP  \u2190 trading in distressed / structural-break zone")
if _bvf >= 0:
    print(f"  BEAR scenario (${_bear_p:.0f}):   BEAR is +{_bvf:.0f}% above EPP  \u2713  bear case is cyclical, not structural")
else:
    print(f"  BEAR scenario (${_bear_p:.0f}):   BEAR is {_bvf:.0f}% BELOW EPP  \u2190 bear case implies permanent impairment")
print(f"  \u26a0  post-10:1 split (Jul 2024); trough & struct_delta adjusted")
print(f"  \u2192 Same pessimism \u2260 same price: FCF locked in, inflation ratcheted every nominal anchor.")
if _sdelta < 0:
    print(f"    Structural damage since {_yr}: equal pessimism = lower price than CPI-adj {_yr} trough.")
elif _sdelta > 0:
    print(f"    Structural gains since {_yr}: equal pessimism = higher price than CPI-adj {_yr} trough.")

print(f"\n  WHAT THE GAP MEANS")
print("  " + "─" * (W-2))
if mkt_composite:
    gap = proxy_composite - mkt_composite
    print(f"""  Proxy signals score {proxy_composite:.2f}.  Market prices in {mkt_composite:.2f}.
  Gap = {gap:+.2f} — this is NOT the market ignoring the data.
  It is the market's SKEPTICISM DISCOUNT on four things proxies can't measure:

    1. Flow-through risk: CapEx going to AVGO vs NVIDIA / in-house silicon
    2. Execution risk:    $100B AI target is aspiration, not contract
    3. Multiple risk:     XBULL EPS ($27) at decelerating growth → 33x, not 40x
    4. Cycle risk:        AI CapEx can reverse fast if ROI disappoints

  To justify proxy composite ({proxy_composite:.2f}) vs market ({mkt_composite:.2f}):
  you need a NON-CONSENSUS view that proxies translate to AVGO revenue
  with higher certainty than the market assumes. Examples:
    • Supply chain checks confirming AVGO ASIC wafer starts (not just TSMC HPC aggregate)
    • VMware renewal cohort data (not yet public)
    • Confirmation of 6th ASIC customer (each = +$15-20B SAM)

  Without that edge, the stock is FAIRLY PRICED for the data available.
  The proxy signals are already IN the consensus and IN the multiple.""")
print()
print("═" * W)
