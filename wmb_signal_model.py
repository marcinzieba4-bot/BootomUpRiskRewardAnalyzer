#!/usr/bin/env python3
"""
WMB Signal Model
──────────────────
Same framework applied to The Williams Companies, Inc. (NYSE: WMB).

Key structural difference from the other companies in this framework:
  WMB is an INFRASTRUCTURE TOLL ROAD, not a technology or consumer stock.
  ~95% of revenue is fee-based; Williams does not take commodity price risk.
  The core asset is Transco: the largest interstate natural gas pipeline in
  the US, carrying ~10% of all US natural gas demand daily.

  The market has bid WMB up sharply on TWO structural narratives:
  1. AI DATA CENTER ELECTRICITY DEMAND: data centers require 24/7 reliable
     power; gas is the baseload of last resort; Transco runs through the
     Mid-Atlantic and Southeast — exactly where hyperscalers are building.
  2. LNG EXPORT EXPANSION: US LNG exports are growing 20%+ annually as
     Europe and Asia diversify away from Russian gas. WMB's Gulf Coast
     exposure captures growing export volumes.

  The risk: the market may be pricing these tailwinds too optimistically.
  At $60, WMB trades at a premium to its fee-based cash flow warranted only
  if the AI demand and LNG expansion materialise fully.

Run: python wmb_signal_model.py
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 60.0      # USD (NYSE: WMB, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

# Scenario 2-year price targets (EPS × exit P/E, FY2027/FY2028E)
# WMB's fee-based revenue gives more EPS stability than commodity-exposed midstream.
# FY2025E EPS: ~$2.10. FY2027E range: $1.80 (bear, rate review headwinds)
# to $3.40 (xbull, AI + LNG demand supercycle).
# Multiples: 15-28x; infrastructure stocks deserve premium if earnings visibility high.
SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  ( 1.8,   15,    27,  "Gas demand plateau; FERC rate review; vol flat"),
    "BASE":  ( 2.3,   22,    51,  "Transco steady; LNG expansion; data center gas ramp"),
    "BULL":  ( 2.9,   25,    73,  "AI/LNG supercycle; Transco expansions approved"),
    "XBULL": ( 3.5,   28,    98,  "Gas as grid backbone; Transco utilisation record"),
}

# ── AI DATA CENTER GAS DEMAND CALCULATOR (WMB-specific structural feature) ─
# AI data centers require 24/7 firm electricity. Renewables can't provide firm
# power at scale; natural gas (combined-cycle) is the dispatchable backstop.
# Transco's service territory (Mid-Atlantic / Southeast) is the primary US
# data center build corridor (Virginia, Georgia, Texas).
#
# This calculator estimates the incremental natural gas throughput demand
# from announced AI data center buildouts, and the revenue uplift to WMB.

AI_DC_PLANNED_GW         = 50.0    # GW new AI data center capacity, US (2025-2027)
AI_DC_CAPACITY_FACTOR    = 0.65    # average utilisation (data centers run near-full)
GAS_POWER_SHARE          = 0.30    # share of incremental power demand met by gas
HEAT_RATE_MMBTU_PER_MWH  = 7.0     # combined-cycle heat rate (MMBtu/MWh)
TRANSCO_CAPACITY_BCFD    = 10.4    # Transco design capacity (Bcf/day)
TRANSCO_TARIFF_PER_DTHM  = 0.50    # average transport tariff ($/Dth, simplified)

def ai_gas_demand():
    effective_gw      = AI_DC_PLANNED_GW * AI_DC_CAPACITY_FACTOR           # GW effective
    annual_twh        = effective_gw * 8_760 / 1_000                       # TWh/yr
    gas_twh           = annual_twh * GAS_POWER_SHARE                       # gas-fired TWh
    gas_mmbtu_yr      = gas_twh * 1e6 * HEAT_RATE_MMBTU_PER_MWH           # MMBtu/yr
    gas_bcf_yr        = gas_mmbtu_yr / 1e6                                 # Bcf/yr (1 Bcf = 1e6 MMBtu)
    gas_bcfd          = gas_bcf_yr / 365                                   # Bcf/day
    pct_transco       = gas_bcfd / TRANSCO_CAPACITY_BCFD * 100
    # Revenue: 1 Bcf/d × 365 days × 1e6 MMBtu/Bcf × $0.50/Dth / 1e6 = Bcf/d × 182.5 $M/yr
    tariff_uplift_m   = gas_bcfd * 182.5                                   # $M/yr
    return effective_gw, gas_bcfd, pct_transco, tariff_uplift_m

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
# (name, value, unit, base_floor, bull_floor, xbull_floor, higher_is_better,
#  what_it_drives_for_WMB)
SIGNALS = [
    # US natural gas production YoY: +4%.
    # More production = more gas to move through Transco and gathering systems.
    # WMB's gathering & processing volumes track production in Haynesville, DJ Basin.
    # +4% is BASE — steady but not explosive shale growth.
    ("US natural gas production — YoY",      4.0, "% YoY",   2,  5,  8, True,
     "throughput driver: more production = more volumes on Transco and G&P systems"),

    # US LNG export facility utilisation: 92%.
    # Williams has significant exposure to LNG feed gas (Gulf South, Haynesville).
    # High utilisation = full offtake demand on gas pipeline corridors to Gulf Coast.
    # 92% utilisation is BULL — US LNG facilities running near capacity.
    ("LNG export facility utilisation",      92.0, "%",       80, 88, 95, True,
     "Gulf Coast feed-gas demand: LNG near-capacity = full contractual throughput"),

    # Natural gas power generation YoY: +9%.
    # Data centers + grid reliability requirements are driving gas power gen higher.
    # This is the STRUCTURAL demand driver that distinguishes 2025-2027 from prior cycles.
    # Tracked via EIA Electric Power Monthly; +9% is a BULL reading.
    ("Nat gas power generation — YoY",       9.0, "% YoY",   3,  8, 14, True,
     "power sector pull-through: gas power gen growth = Transco Mid-Atlantic volumes"),

    # AI data center power demand YoY: +55%.
    # Hyperscaler CapEx disclosures and data center construction starts.
    # The single most differentiated demand signal vs prior WMB investment theses.
    # +55% YoY confirms the buildout is real and accelerating.
    ("AI data center power demand — YoY",   55.0, "% YoY",  10, 30, 50, True,
     "structural demand driver: data centers need firm 24/7 gas-backed power"),

    # WMB Transco expansion project backlog: $5.5B.
    # Williams discloses its contracted expansion project backlog on earnings calls.
    # Each approved expansion project is a fixed-fee contract before it's built.
    # $5.5B backlog signals multi-year earnings visibility.
    ("Transco expansion backlog",            5.5, "$B",       2,  4,  6, True,
     "earnings visibility: contracted backlog = confirmed revenue 2-4 years forward"),

    # EIA 2-year US gas demand outlook: +7%.
    # EIA publishes Annual Energy Outlook and Short-Term Energy Outlook monthly.
    # Forward gas demand growth directly forecasts WMB's medium-term volume trajectory.
    # +7% is BULL — significantly above population/industrial growth.
    ("EIA 2yr US gas demand outlook",        7.0, "% YoY",   2,  5,  9, True,
     "medium-term volume forecast; EIA outlook leads WMB volume growth by 18-24M"),
]
WEIGHTS = [0.20, 0.20, 0.20, 0.15, 0.15, 0.10]

STRUCTURAL_FACTORS = [
    ("Transco interstate pipeline franchise moat",    1.5, 0.30),
    ("Gas-to-clean energy policy transition risk",   -0.8, 0.25),
    ("AI data center electricity demand tailwind",    1.0, 0.20),
    ("FERC regulatory rate review risk",             -0.5, 0.15),
    ("Balance sheet leverage (~$22B gross debt)",    -0.3, 0.10),
]

# ── SCORING ───────────────────────────────────────────────────────────────
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

# ── MAIN ──────────────────────────────────────────────────────────────────
W = 72

scored = [(name, val, unit, score_signal(val, bf, bull_f, xf, hib), w, rt)
          for (name, val, unit, bf, bull_f, xf, hib, rt), w in zip(SIGNALS, WEIGHTS)]
proxy_composite = sum(s * w for *_, s, w, _ in scored)
sca             = sum(s * w for _, s, w in STRUCTURAL_FACTORS)
adj_composite   = proxy_composite + sca
proxy_probs     = softmax_probs(proxy_composite)
proxy_ev        = expected_price(proxy_probs)

market_target_ev  = CURRENT_PRICE * ((1 + REQUIRED_RETURN) ** HORIZON_YEARS)
mkt_composite, mkt_probs = market_implied_composite(market_target_ev)
mkt_ev = expected_price(mkt_probs) if mkt_probs else market_target_ev

eff_gw, gas_bcfd, pct_transco, tariff_uplift = ai_gas_demand()

print()
print("═" * W)
print("  WMB SIGNAL MODEL  —  proxy vs. market-implied probability")
print("═" * W)

# AI gas demand calculator
print(f"\n  AI DATA CENTER GAS DEMAND CALCULATOR  (the structural demand driver)")
print("  " + "─" * (W-2))
print(f"  Planned US AI data center capacity (2025-2027):  {AI_DC_PLANNED_GW:.0f} GW")
print(f"  Effective demand (@ {AI_DC_CAPACITY_FACTOR*100:.0f}% utilisation):       {eff_gw:.1f} GW")
print(f"  Annual power generation required:                {eff_gw * 8760 / 1000:.0f} TWh/yr")
print(f"  Gas-fired share ({GAS_POWER_SHARE*100:.0f}% of incremental):          {eff_gw*8760/1000*GAS_POWER_SHARE:.0f} TWh/yr")
print(f"  ─────────────────────────────────────────────────────")
print(f"  Incremental gas demand:                          {gas_bcfd:.2f} Bcf/day")
print(f"  As % of Transco capacity ({TRANSCO_CAPACITY_BCFD:.1f} Bcf/d):          {pct_transco:.0f}%")
print(f"  Estimated Transco tariff uplift:                ~${tariff_uplift:.0f}M/yr")
print(f"  → Even at 50% realisation, ~${tariff_uplift*0.5:.0f}M/yr incremental revenue.")
print(f"    This is NOT in consensus models — data center proximity = captive throughput.")

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
    direction = "market priced AHEAD of proxies" if gap < 0 else "proxies ahead of market"
    print(f"  Gap (proxy − mkt): {gap:+.2f}  ← {direction}")

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

# Valuation context
print(f"\n  VALUATION CONTEXT")
print("  " + "─" * (W-2))
fy25_eps = 2.10
print(f"  FY2025E EPS:                ~${fy25_eps:.2f}")
print(f"  Current forward P/E:         {CURRENT_PRICE/fy25_eps:.0f}x  (infrastructure range: 18-28x)")
print(f"  Adjusted EBITDA (FY2025E):  ~$7.0B  (fee-based; high visibility)")
print(f"  EV / EBITDA:                ~12x   (premium to midstream peers at 9-10x)")
print(f"  Dividend yield:              ~3.5%  (8% growth streak since 2022)")
print(f"  Gross debt:                 ~$22B  (~3x EBITDA; investment-grade BBB)")
print(f"  → Premium valuation requires AI/LNG demand thesis to materialise fully.")

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
    print(f"  {k:<10}  {pp*100:>7.1f}%  {mp*100:>7.1f}%  "
          f"{sign}{gap_pp*100:>6.1f}pp  ${eps:>4.1f}  {mult:>4}x  ${price:<6}  {narr[:28]}…")

print(f"\n  Prob-weighted 2yr:  proxy ${proxy_ev:.0f}  /  market ${mkt_ev:.0f}")
print(f"  Current price: ${CURRENT_PRICE:.0f}")

# Verdict
print(f"\n  WHAT THE GAP MEANS")
print("  " + "─" * (W-2))
gap = (proxy_composite - mkt_composite) if mkt_composite else 0
print(f"""  Proxy composite {proxy_composite:.2f}  vs  market-implied {mkt_composite:.2f}.
  Gap = {gap:+.2f}

  WHY WMB HAS THE LARGEST NEGATIVE RAW GAP IN THIS FRAMEWORK:

    The market composite of {mkt_composite:.2f} means the market is pricing WMB
    as if BULL-to-XBULL conditions are the base case. That requires:
    • Transco expansion approvals coming through without FERC delay
    • AI data center gas demand materialising on Transco's corridors
    • LNG exports at near-capacity utilisation through FY2027
    • No gas-to-clean-energy policy shock

    The proxy signals are genuinely BULL (composite {proxy_composite:.2f}), but the
    market has taken them even further. This is the AI premium:
    investors are paying for the gas-as-AI-infrastructure narrative
    before it shows up in reported throughput volumes.

  WHY THE STRUCTURAL OVERLAY REVERSES THE VERDICT TO FAIRLY VALUED:

    The Transco franchise is REAL and DURABLE. It is the single most
    important piece of gas infrastructure on the East Coast. No new
    interstate pipeline has been permitted in this corridor since 2020.
    The barrier to entry is essentially infinite — it cannot be replicated.

    This moat is NOT captured in the proxy signals, which measure market
    demand conditions. The structural overlay adds +1.5 × 30% = +0.45
    to reflect the regulatory franchise value, which partially offsets
    the market premium (raw gap {gap:+.2f} → adjusted gap ~0.00).

  THE THREE STRUCTURAL RISKS:

    1. FERC rate review: Transco's tariffs were set in a 2019 settlement.
       A new rate case (overdue) could reduce tariffs by 10-20%, hitting
       $700M-$1.4B of annual revenue. Most underwrite Transco at current
       tariffs — a downward reset would be a negative surprise.

    2. Gas transition risk (10-year horizon): The energy transition creates
       a TIMING problem. Data center demand is real for 2025-2030. But
       by 2035-2040, if renewable + battery penetration reaches 60-70%,
       baseload gas demand plateaus. WMB's Transco assets have 30-40 year
       useful lives — the terminal value depends on long-run gas demand.

    3. Regulatory approval risk: Every Transco expansion requires FERC,
       state, and environmental approvals. Virginia and Maryland have
       become more hostile to new pipeline permitting. The $5.5B backlog
       is contracted but not yet in the ground — delays compress returns.

  THE BULL CASE (FAIRLY VALUED → MODESTLY UNDERVALUED):

    If hyperscalers formally contract for firm gas capacity adjacent to
    data centers (like Virginia data center corridor), WMB gets:
    • Long-term (20yr) fee-based contracts at premium tariffs
    • Zero volume risk (data centers = 24/7 flat demand profile)
    • Multiple expansion to 26-28x on infrastructure-quality earnings
    Data center load contracts would make WMB look more like a utility
    than a midstream company — warranting a lower discount rate.""")
print()
print("═" * W)
