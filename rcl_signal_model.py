#!/usr/bin/env python3
"""
Royal Caribbean Signal Model
──────────────────────────────
Same framework applied to Royal Caribbean Group (NYSE: RCL).

Key structural difference from the other companies in this framework:
  RCL is a CAPITAL-INTENSIVE RECOVERY story — not tech growth, not a
  turnaround (like NKE), but a maturing post-COVID upcycle with one
  structural innovation the market systematically under-models:
  PRIVATE DESTINATION ECONOMICS.

  The standard cruise analyst model treats all sea days equally.
  It does not. A day at Perfect Day at CocoCay (RCL-owned private island)
  generates ~$175 MORE net yield per passenger than a regular port call —
  purely from onshore spend that flows entirely to RCL with no port fees.
  As private destination capacity grows (Royal Beach Club Nassau opened 2025),
  net yield per APCD rises structurally even if pricing power is zero.

  Bear risk is simpler: $20B+ gross debt × consumer spending recession
  = cash flow squeeze at exactly the wrong moment for debt servicing.
  The bull case needs BOTH demand staying elevated AND debt declining.

Run: python rcl_signal_model.py
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 235.0     # USD (NYSE: RCL, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

# Scenario 2-year price targets (non-GAAP EPS × exit P/E multiple)
# RCL's own "Trifecta+" plan targeted $18+ EPS by FY2025.
# FY2025E non-GAAP EPS: ~$14-15 (strong but below original target due to
# capacity additions diluting per-share economics during ramp).
# FY2028 scenarios: lower multiples reflect capital-intensity + debt.
# Cruise stocks rarely trade above 15-18x given cyclicality.
SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  (12.0,   12,   144,  "Recession; consumer pullback; debt servicing squeeze"),
    "BASE":  (20.0,   14,   280,  "Steady demand; private dest ramp; debt falls to $15B"),
    "BULL":  (25.0,   17,   425,  "Yield growth 7%+; private dest at scale; China opens"),
    "XBULL": (30.0,   20,   600,  "Supercycle: pricing power + private dest + China boom"),
}

# ── PRIVATE DESTINATION ECONOMICS CALCULATOR (RCL-specific) ──────────────
# RCL owns/operates private resort destinations exclusively for its guests.
# Onshore spend at private destinations (food, excursions, beach clubs)
# flows 100% to RCL with no port authority fees or revenue sharing.
# Net yield premium over a standard Caribbean port call:
#
# Regular Caribbean port call NPCCD contribution: ~$120-140
# Perfect Day at CocoCay NPCCD contribution:       ~$290-310
# Delta (private vs standard):                      ~$160-175 / passenger day

COCCOCAY_ANNUAL_VISITORS     = 4_200_000   # annual visitor throughput (pax)
RBC_NASSAU_ANNUAL_VISITORS   = 2_400_000   # Royal Beach Club Nassau (pax, 2026E)
PRIVATE_DEST_YIELD_PREMIUM   =       170   # USD per passenger vs standard port
STANDARD_PORT_NPCCD          =       130   # USD net yield per passenger / standard port
FLEET_CAPACITY_APCD_M        =        95   # ~95M available passenger cruise days / yr

def private_dest_economics():
    total_private_pax  = COCCOCAY_ANNUAL_VISITORS + RBC_NASSAU_ANNUAL_VISITORS
    annual_premium_rev = total_private_pax * PRIVATE_DEST_YIELD_PREMIUM / 1e9  # $B
    pct_of_capacity    = total_private_pax / (FLEET_CAPACITY_APCD_M * 1e6) * 100
    npccd_lift         = (total_private_pax * PRIVATE_DEST_YIELD_PREMIUM) / (FLEET_CAPACITY_APCD_M * 1e6)
    # If RCL adds 2 more private destinations at similar scale:
    future_premium     = annual_premium_rev * 2.5
    return total_private_pax, annual_premium_rev, pct_of_capacity, npccd_lift, future_premium

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
# Consumer-facing and cruise-specific signals. Unlike tech models, there is
# no analogue of "RPO" or "backlog" — the leading signals are consumer
# sentiment, competitive pricing, and real-time booking data.
#
# (name, value, unit, base_floor, bull_floor, xbull_floor, higher_is_better,
#  what_it_drives_for_RCL)
SIGNALS = [
    # US consumer confidence index: 93.
    # Cruise vacations are high-ticket discretionary purchases ($3,000-8,000/trip).
    # Consumer confidence is the primary macro gating factor — when it drops
    # below 85-90, discretionary travel is among the first cuts.
    # Currently moderate: tariff uncertainty → below trend but not recessionary.
    ("US consumer confidence index",     93.0, "pts",      90, 100, 115, True,
     "discretionary spend gating: confidence <85 = booking cancellations accelerate"),

    # Cruise net yield per APCD YoY: +7.5%.
    # RCL publishes net yield growth quarterly. It is the single best
    # measure of pricing power + mix (private dest weighting).
    # At +7.5%, demand is running ahead of capacity addition — a BULL signal.
    # Private destination expansion is the structural driver above the trend.
    ("Cruise net yield per APCD YoY",    7.5, "% YoY",     3,   6,  10, True,
     "primary revenue driver; private dest premium lifts this structurally above inflation"),

    # Forward 12-month booking price premium YoY: +8%.
    # RCL reports booking trends on earnings calls. Premium pricing in the
    # forward book means demand is absorbing new capacity at higher prices —
    # the key bull signal for the next 2-4 quarters of reported revenue.
    ("Fwd 12M booking price premium",    8.0, "% YoY",     3,   7,  12, True,
     "2-4Q lead on revenue; elevated forward pricing = current demand exceeds supply"),

    # Caribbean resort ADR (Average Daily Rate) YoY: +5%.
    # Land-based Caribbean resort pricing is RCL's key competitive alternative.
    # When hotels are expensive, cruises look relatively cheap (value proposition).
    # STR / Smith Travel Research data, monthly.
    ("Caribbean resort ADR YoY",         5.0, "% YoY",     2,   6,  10, True,
     "land-based competition: higher hotel rates → cruise perceived value improves"),

    # US leisure travel spend YoY: +4%.
    # BEA / TSA travel data. Broad leisure travel spend includes air, hotel, cruise.
    # At +4%, the market is growing but not booming — consistent with BASE conditions.
    ("US leisure travel spend YoY",      4.0, "% YoY",     2,   5,   9, True,
     "total addressable leisure spend; RCL captures ~5-6% of US leisure travel market"),

    # Fleet load factor: 108%.
    # RCL consistently sells above double occupancy (100%). At 108%, cabins
    # are selling additional berths (bunk beds, pullman beds) — demonstrating
    # that demand exceeds base capacity. Load factor below 104% = weak demand.
    ("Fleet load factor",               108.0, "%",        100, 106, 110, True,
     "demand vs. supply: >106% means all berths sold + extras; drives onboard revenue"),
]
WEIGHTS = [0.20, 0.20, 0.15, 0.15, 0.15, 0.15]

STRUCTURAL_FACTORS = [
    ("Private destination captive revenue moat",      1.0, 0.25),
    ("Industry overcapacity (8-10 new ships 25-27)", -0.8, 0.25),
    ("$20B gross debt financial constraint",         -0.8, 0.20),
    ("Royal Caribbean / Celebrity brand premium",     0.5, 0.15),
    ("Fuel / LNG transition capital cost",           -0.3, 0.15),
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

def market_implied_composite(target_ev, tolerance=2.0):
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

total_pax, premium_rev, pct_cap, npccd_lift, future_premium = private_dest_economics()

print()
print("═" * W)
print("  RCL SIGNAL MODEL  —  proxy vs. market-implied probability")
print("═" * W)

# Private destination economics
print(f"\n  PRIVATE DESTINATION ECONOMICS  (the structural yield driver)")
print("  " + "─" * (W-2))
print(f"  Perfect Day at CocoCay (visitors/yr):  {COCCOCAY_ANNUAL_VISITORS/1e6:.1f}M")
print(f"  Royal Beach Club Nassau (visitors/yr): {RBC_NASSAU_ANNUAL_VISITORS/1e6:.1f}M  (opened 2025)")
print(f"  Total private destination traffic:     {total_pax/1e6:.1f}M pax/yr  "
      f"({pct_cap:.0f}% of fleet APCD)")
print(f"  Net yield premium vs regular port:     ${PRIVATE_DEST_YIELD_PREMIUM}/passenger")
print(f"  ─────────────────────────────────────────────────────")
print(f"  Annual revenue premium over std ports: ${premium_rev:.2f}B / yr")
print(f"  Fleet-wide NPCCD structural lift:      +${npccd_lift:.1f} / APCD  ← invisible in yield YoY comps")
print(f"  If 2 additional private dests added:   ~${future_premium:.1f}B / yr premium (2028E)")
print(f"\n  STANDARD ANALYST ERROR: models showing '7.5% net yield growth' as")
print(f"  'demand/pricing' miss ~${npccd_lift:.0f} of that being structural private-dest mix shift.")
print(f"  The true underlying pricing growth is ~${npccd_lift:.0f} lower than headline shows.")
print(f"  This ALSO means yield can sustain above inflation even in a weak demand env.")

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
    print(f"  Gap (proxy − mkt): {gap:+.2f}  ← debt discount + capacity absorption risk")

# Valuation context
print(f"\n  VALUATION CONTEXT")
print("  " + "─" * (W-2))
fy25_eps = 14.5
print(f"  FY2025E non-GAAP EPS:       ~${fy25_eps:.2f}")
print(f"  Forward P/E:                 {CURRENT_PRICE/fy25_eps:.1f}x  (cruise sector range: 10-18x)")
print(f"  Gross debt:                  ~$20B  (down from $22B peak; ~2x EV/EBITDA of debt)")
print(f"  FCF yield:                   ~6-7%  ($3.5-4B FCF / $30B market cap)")
print(f"  'Trifecta+' EPS target:      $18+  (original FY2025 target; now a FY2026 target)")
print(f"  Net debt / EBITDA:           ~3.5x  (target: 2.5x by FY2027)")
print(f"  → At $235, market prices solid execution but not full debt re-rating.")
print(f"    When net debt/EBITDA crosses 2.5x, multiple should expand to 16-18x.")

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
    print(f"  {k:<10}  {pp*100:>7.1f}%  {mp*100:>7.1f}%  "
          f"{sign}{gap_pp*100:>6.1f}pp  ${eps:>5}  {mult:>4}x  ${price:<6}  {narr[:28]}…")

print(f"\n  Prob-weighted 2yr:  proxy ${proxy_ev:.0f}  /  market ${mkt_ev:.0f}")
print(f"  Current price: ${CURRENT_PRICE:.0f}")

# Verdict
print(f"\n  WHAT THE GAP MEANS")
print("  " + "─" * (W-2))
gap = (proxy_composite - mkt_composite) if mkt_composite else 0
print(f"""  Proxy composite {proxy_composite:.2f}  vs  market-implied {mkt_composite:.2f}.
  Gap = {gap:+.2f}

  Complete framework gap table:
    ORCL gap = +2.16  (proxies XBULL; market prices execution/concentration risk)
    AVGO gap = +1.41  (proxies bullish; AI flow-through uncertainty)
    MSFT gap = +1.29  (proxies bullish; Copilot margin expansion uncertainty)
    SAP  gap = +0.91  (proxies constructive; Joule unmonetised)
    XTB  gap = +0.46  (justified volatility discount on cyclical revenue)
    RCL  gap = {gap:+.2f}  ← debt multiple compression + capacity risk discount
    COIN gap = +0.29  (approximately fairly priced; thesis is BTC price)
    CAT  gap = -0.24  (market ahead of confirmed cycle recovery)
    NKE  gap = -0.12  (market pricing unconfirmed turnaround hope)

  WHY RCL'S GAP IS SMALL BUT POSITIVE:

    Unlike ORCL/AVGO/MSFT, RCL's execution is ALREADY CONFIRMED:
    Icon of the Seas sailing full. Utopia of the Seas delivering XBULL yields.
    CocoCay printing money. Forward books at records. The market has credited
    this execution — hence RCL trades at 16x forward vs 10x in 2022.

    The residual +{gap:.2f} gap reflects two legitimate market concerns:
    1. DEBT: $20B gross debt requires ~$1.5B/yr interest. A 200bp rate
       spike or a 2-quarter demand softening converts the bull case to
       a balance sheet stress scenario. The market is right to discount.
    2. CAPACITY: RCL, Carnival, and Norwegian are all adding ships
       simultaneously. ~8-10 new ships across the industry in 2025-2027.
       If demand grows 4% and supply grows 6%, pricing power evaporates.

  THE PRIVATE DESTINATION THESIS — WHY ANALYSTS ARE WRONG:

    Most models attribute ALL net yield growth to pricing power or demand.
    At 6.5M private destination visitors × $170 premium = $1.1B in revenue
    that has NOTHING to do with consumer confidence or macro.
    It flows from: (1) more ships routed through CocoCay/RBC Nassau,
    (2) onshore spend once guests are there (captive audience).

    This means:
      • Even in a moderate recession, yield doesn't fall as far as models predict
        because private dest revenue is sticky (guests already onboard, no alternative)
      • Each new private destination adds a structural $300-500M of incremental
        high-margin revenue that isn't visible in booking or yield trend data

    The correct way to model RCL: split yield into (a) market-driven pricing
    and (b) private destination structural mix shift. Most sell-side does not.

  THE DEBT RE-RATING CATALYST (not yet in multiple):
    Net debt / EBITDA: ~3.5x today → target 2.5x in FY2027.
    At 2.5x, investment-grade credit ratings normalise → interest cost falls
    ~$300-400M/yr → ~$0.70-0.90 EPS tailwind with zero revenue growth.
    Credit upgrade also triggers multiple expansion from 14x to 16-17x.
    Combined: EPS lift + multiple expansion = 25-35% re-rating at the
    debt crossover point. This is a date-specific, predictable catalyst.

  WHAT WOULD BREAK THE THESIS:
    1. US recession: consumer confidence below 80 → forward bookings cancel
       at scale. NCL Chapter 11 risk (2020 replay) if demand falls 25%+.
    2. Fuel price spike: RCL hedges ~60% but an unhedged spike at $100+ oil
       costs ~$500M EBIT → ~$1.00 EPS headwind per $20/bbl move.
    3. Industry overcapacity: if all three major lines execute their orderbooks,
       Caribbean supply grows 6-8%/yr 2025-2027. At 4% demand growth,
       pricing power disappears and yield growth turns negative.""")
print()
print("═" * W)
