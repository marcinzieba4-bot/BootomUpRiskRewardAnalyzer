#!/usr/bin/env python3
"""
AVGO Signal Model — compact edition
────────────────────────────────────
Core question: do proxy signals suggest EPS will beat or miss
what the current stock price already prices in?

At $417 the market isn't ignoring TSMC / hyperscaler CapEx data —
it's already embedding those signals. The edge is only in the GAP
between (a) what proxies imply for future EPS and (b) what $417
requires for a fair return.

Run: python avgo_signal_model.py
"""

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 417.0
EXIT_MULTIPLES  = [25, 30, 35, 40]     # range of reasonable 2-yr exit P/Es
CONSENSUS_EPS   = {"FY2026": 9.39, "FY2027": 12.72, "FY2028": 17.55}

# ── PROXY SIGNALS (latest available: Q1 FY2026 window, Mar 2026) ──────────
#
#  Each signal:  (name, value, unit, bear_floor, base_floor, bull_floor, xbull_floor,
#                 higher_is_better, what_it_implies_for_avgo_eps)
#
SIGNALS = [
    # name                              val    unit         bear  base  bull  xbull  hib
    ("Hyperscaler CapEx YoY",           77.0,  "% YoY",      0,   10,   30,   60,   True,
     "upstream AI ASIC order flow; leads AVGO AI rev by 1-2Q"),
    ("TSMC HPC % of revenue",           61.0,  "% of rev",  40,   50,   57,   62,   True,
     "actual fab utilisation of N3/N5 — AVGO ASIC slots filling"),
    ("Arista Networks rev YoY",         35.1,  "% YoY",      0,   15,   25,   35,   True,
     "AI cluster Ethernet build-out; AVGO Jericho/Tomahawk volume"),
    ("Nutanix ARR YoY (inverse)",       18.0,  "% YoY",     30,   30,   20,   10,   False,
     "VMware churn proxy — lower NTNX growth = VMware stickier"),
    ("Super Micro rev YoY",            123.0,  "% YoY",      0,   20,   60,  100,   True,
     "GPU rack deployments — AI capex flowing into compute density"),
    ("CDW commercial YoY",              9.6,   "% YoY",     -5,    0,    5,   10,   True,
     "enterprise IT budget health — VMware channel + non-AI semi"),
]
WEIGHTS = [0.30, 0.20, 0.15, 0.15, 0.10, 0.10]   # must sum to 1.0

# ── SCENARIO EPS BANDS ────────────────────────────────────────────────────
#  FY2028 non-GAAP EPS implied by each scenario (2-yr horizon)
SCENARIO_EPS = {"BEAR": 8.50, "BASE": 17.55, "BULL": 22.0, "XBULL": 27.0}

# ─────────────────────────────────────────────────────────────────────────
import math

def score(val, bear, base, bull, xbull, hib):
    if hib:
        if val >= xbull: return 4, "XBULL"
        if val >= bull:  return 3, "BULL"
        if val >= base:  return 2, "BASE"
        return 1, "BEAR"
    else:   # inverse: lower is better; xbull is the tightest ceiling
        if val <= xbull: return 4, "XBULL"
        if val <= bull:  return 3, "BULL"
        if val <= base:  return 2, "BASE"
        return 1, "BEAR"

def softmax_probs(composite):
    """Map composite score (1-4) to scenario probabilities."""
    centres = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    T = 0.60
    raw = {k: math.exp(-abs(composite - c) / T) for k, c in centres.items()}
    tot = sum(raw.values())
    return {k: v / tot for k, v in raw.items()}

def implied_breakeven_eps(price, multiples):
    """EPS the stock needs in 2 years to break even at each exit multiple."""
    return {m: round(price / m, 2) for m in multiples}

def ev(probs):
    return sum(probs[k] * SCENARIO_EPS[k] for k in probs)

# ── SCORE ALL SIGNALS ─────────────────────────────────────────────────────
results = []
for (name, val, unit, bear, base, bull, xbull, hib, note), w in zip(SIGNALS, WEIGHTS):
    s, label = score(val, bear, base, bull, xbull, hib)
    results.append((name, val, unit, s, label, w, note))

composite  = sum(r[3] * r[5] for r in results)
probs      = softmax_probs(composite)
top        = max(probs, key=probs.get)
ev_eps     = ev(probs)
breakevens = implied_breakeven_eps(CURRENT_PRICE, EXIT_MULTIPLES)

# ── OUTPUT ────────────────────────────────────────────────────────────────
W = 70
print()
print("═" * W)
print("  AVGO SIGNAL MODEL  (proxy signals vs. what $417 prices in)")
print("═" * W)

# Signal scorecard
print(f"\n  {'Signal':<34} {'Value':>9}  {'Wt':>4}  {'Score'}")
print("  " + "─" * (W-2))
icons = {4: "★ XBULL", 3: "▲ BULL", 2: "◦ BASE", 1: "⚠ BEAR"}
for name, val, unit, s, label, w, note in results:
    bar = "█" * s + "░" * (4-s)
    print(f"  {name:<34} {val:>7.1f}{unit[0]:1}  {w*100:.0f}%   {icons[s]}  {bar}")

print(f"\n  Proxy composite : {composite:.2f} / 4.00")
print(f"  Signal says     : {top}  ({probs[top]*100:.0f}% probability)")

# What the price already implies
print(f"\n  WHAT $417 REQUIRES  (break-even EPS in 2 years at exit multiple)")
print("  " + "─" * (W-2))
print(f"  {'Exit multiple':<20} {'Required EPS':>14}  {'vs consensus FY2028 ($17.55)':>28}")
print("  " + "─" * (W-2))
for m, eps in breakevens.items():
    diff   = (eps / CONSENSUS_EPS["FY2028"] - 1) * 100
    sign   = "+" if diff >= 0 else ""
    marker = " ← stock looks CHEAP vs consensus" if eps < CONSENSUS_EPS["FY2028"] else \
             " ← requires ABOVE consensus" if eps > CONSENSUS_EPS["FY2028"] * 1.1 else ""
    print(f"  {m}x exit{'':<13} {eps:>14.2f}  consensus {sign}{diff:.0f}%{marker}")

# Probability-weighted EPS vs. break-evens
print(f"\n  Proxy-implied expected EPS (prob-weighted): ${ev_eps:.2f}")
print(f"  Consensus FY2028E:                          ${CONSENSUS_EPS['FY2028']:.2f}")
gap = (ev_eps / CONSENSUS_EPS["FY2028"] - 1) * 100
print(f"  Proxy vs consensus gap:                    {'+' if gap>=0 else ''}{gap:.0f}%")

# THE KEY QUESTION
print(f"\n  THE KEY QUESTION")
print("  " + "─" * (W-2))
if ev_eps > CONSENSUS_EPS["FY2028"] * 1.10:
    verdict = "PROXIES AHEAD OF CONSENSUS — potential upside if signals are right"
    detail  = (f"  Proxy-implied EPS ${ev_eps:.2f} > consensus ${CONSENSUS_EPS['FY2028']:.2f}.\n"
               f"  If correct, stock is pricing in less than proxies suggest.\n"
               f"  Edge exists — but only if signals haven't fully reached analyst models yet.")
elif ev_eps < CONSENSUS_EPS["FY2028"] * 0.90:
    verdict = "PROXIES BELOW CONSENSUS — proxy signals warn of downside to estimates"
    detail  = (f"  Proxy-implied EPS ${ev_eps:.2f} < consensus ${CONSENSUS_EPS['FY2028']:.2f}.\n"
               f"  Market may be overly optimistic. Watch for estimate cuts.")
else:
    verdict = "PROXIES IN LINE WITH CONSENSUS — stock fairly reflects available data"
    detail  = (f"  Proxy-implied EPS ${ev_eps:.2f} ≈ consensus ${CONSENSUS_EPS['FY2028']:.2f}.\n"
               f"  No informational edge from proxy signals at current price.\n"
               f"  Alpha requires a VIEW on: (1) new ASIC customer timing,\n"
               f"  (2) VMware renewal cohort data not yet public,\n"
               f"  (3) hyperscaler CapEx guidance revisions.")
print(f"  {verdict}")
print()
for line in detail.split("\n"):
    print(f"  {line}")

# Scenario probability table
print(f"\n  SCENARIO DISTRIBUTION  (proxy-only)")
print("  " + "─" * (W-2))
eps_map = {"BEAR": 187, "BASE": 526, "BULL": 770, "XBULL": 1080}
for k, p in probs.items():
    bar = "█" * int(p*20) + "░" * (20-int(p*20))
    print(f"  {k:<8} {p*100:>5.1f}%  {bar}  ${eps_map[k]}")
ev_price = sum(probs[k]*eps_map[k] for k in probs)
print(f"\n  Prob-weighted price target: ${ev_price:.0f}  "
      f"({'+'if ev_price>CURRENT_PRICE else ''}{(ev_price/CURRENT_PRICE-1)*100:.0f}% vs $417)")
print()
print("═" * W)
