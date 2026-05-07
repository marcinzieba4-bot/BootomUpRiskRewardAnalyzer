#!/usr/bin/env python3
"""
CAT Signal Model
──────────────────
Same framework applied to Caterpillar Inc. (NYSE: CAT).

Key structural difference from AVGO, COIN, SAP, and ORCL:
  Pure-play industrial cyclical — revenue driven by construction,
  mining, and oil & gas capex cycles, NOT software contracts or AI hype
  Dealer inventory cycle is the #1 short-term production multiplier:
    2024 saw ~$4B of dealer destocking that crushed revenue despite
    solid end-market demand; normalization creates 2025-2026 tailwind
  NEW secular driver: AI data center construction drives power generation
    demand — backup generators, containerised power, UPS systems

The interesting question: proxy signals confirm a cycle recovery is
BEGINNING, but the market is already priced for it. Unlike ORCL and AVGO
where proxies run far ahead of market pricing, CAT proxies and market
pricing are closely aligned — which is what efficient markets look like
for a well-covered industrial with transparent dealer inventory data.

Run: python cat_signal_model.py
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 305.0     # USD (NYSE: CAT, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

# Scenario 2-year price targets (non-GAAP EPS × exit P/E multiple)
# CAT is a cyclical — multiples compress in downturns, expand in upswings.
# Through-cycle EPS: FY2024 actuals ~$21.90, FY2025 expected ~$17-18
# (tariff headwinds + dealer destocking aftermath), FY2027 base recovery.
# Exit multiples: CAT historically 14-22x depending on cycle position.
SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  (12.0,   14,   168,  "Recession; construction -20%; mining bust; tariff hit"),
    "BASE":  (18.0,   17,   306,  "Moderate recovery; infra steady; mining stable; restock"),
    "BULL":  (23.0,   19,   437,  "Construction upcycle; copper boom; data center wave"),
    "XBULL": (28.0,   21,   588,  "Full supercycle: infra + mining + energy transition + AI"),
}

# ── DEALER INVENTORY CYCLE CALCULATOR (CAT-specific structural feature) ──
# CAT's ~3,800 dealers globally hold finished-machine inventory.
# When dealers DESTOCK (months supply rising), CAT produces LESS than
# end-market demand → revenue headwind.
# When dealers RESTOCK (months supply falling), CAT produces MORE than
# end-market demand → revenue tailwind.
#
# FY2024 destocking was ~$4B revenue headwind (months supply peak ~4.2M).
# Normal range: 2.5–3.5 months. Below 2.5 = potential restock signal.

DEALER_MONTHS_CURRENT   = 2.7      # months of machine supply, est. Q1 2026
DEALER_MONTHS_NORMAL    = 3.0      # steady-state neutral
DEALER_MONTHS_PEAK      = 4.2      # peak destocking (2024)
REVENUE_PER_MONTH_SWING = 1_600    # ~$1.6B revenue impact per 1-month inventory swing ($M)
ANNUAL_RESTOCK_WINDOW   = 2        # years to normalise from low-inventory to restock

def dealer_cycle():
    vs_normal    = DEALER_MONTHS_CURRENT - DEALER_MONTHS_NORMAL      # negative = lean
    restock_need = max(0, DEALER_MONTHS_NORMAL - DEALER_MONTHS_CURRENT)
    tailwind_m   = restock_need * REVENUE_PER_MONTH_SWING             # $M, spread over window
    tailwind_ann = tailwind_m / ANNUAL_RESTOCK_WINDOW                 # $M/yr
    # FY2024 headwind from destocking (peak 4.2 → 2.7 = 1.5 months swing)
    peak_headwind = (DEALER_MONTHS_PEAK - DEALER_MONTHS_CURRENT) * REVENUE_PER_MONTH_SWING
    return vs_normal, restock_need, tailwind_ann, peak_headwind

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
# Chosen to cover all three end-market segments (Construction, Resource,
# Energy & Transportation) plus the unique inventory cycle and new
# data-center secular driver.
#
# (name, value, unit, base_floor, bull_floor, xbull_floor, higher_is_better,
#  what_it_drives_for_CAT)
SIGNALS = [
    # Architecture Billings Index (ABI): 50.8 (May 2026 reading).
    # Published monthly by AIA; readings >50 = expanding billings.
    # Non-residential construction leads CAT Construction Industries revenue
    # by approximately 6-9 months. Includes commercial, industrial, institutional.
    # Highways and infrastructure spending from IIJA supplements ABI.
    ("Architecture Billings Index",      50.8, "ABI",      49,  52,  56, True,
     "non-residential construction pipeline; 6-9M lead on Construction Industries rev"),

    # Copper price YoY: +8%.
    # Two-channel signal: (1) mining companies greenlight new copper mines/expansions
    # when price is elevated → Resource Industries orders. (2) Energy-transition copper
    # demand (EVs, grids) sustains long-cycle mine investment regardless of macro.
    ("Copper price — YoY change",         8.0, "% YoY",    0,  10,  20, True,
     "mining investment decisions; Resource Industries order pipeline 2-4Q lead"),

    # Global mining CapEx YoY: +10%.
    # Direct survey-based measure (CRU Group, Wood Mackenzie) of mining company
    # capex intentions. Leads CAT Resource Industries orders by 1-3 quarters.
    # Copper and lithium drives most of the increase; coal declining.
    ("Global mining CapEx YoY",          10.0, "% YoY",    5,  10,  18, True,
     "Resource Industries demand; each $10B mining CapEx ≈ $0.5-0.8B CAT orders"),

    # Baker Hughes US rig count — YoY change: -3%.
    # CAT sells engines, reciprocating compressors, and turbines to oil & gas.
    # Rig count leads Energy & Transportation orders by 1-2 quarters.
    # Currently mildly negative as energy prices soften; not a collapse.
    ("Baker Hughes US rig count — YoY",  -3.0, "% YoY",   -5,   5,  15, True,
     "Energy & Transportation orders (oil & gas engines, turbines, compressors)"),

    # CAT dealer inventory — months supply (INVERSE signal).
    # Lower inventory = lean dealers = restocking tailwind to production.
    # 2.7 months is below normal (3.0) but above XBULL restock threshold (2.5).
    # After 2024's destocking headwind (~$4B), inventory is now LEAN.
    # Any macro uptick causes immediate dealer restocking = outsized production lift.
    ("CAT dealer inventory (months, inv)",  2.7, "months",3.5, 3.0, 2.5, False,
     "production multiplier: lean inventory → restock surge on demand uptick"),

    # Data center construction spending YoY: +48%.
    # AI buildout is driving massive data center construction — which requires:
    # (1) CAT backup power generators (largest market share globally)
    # (2) Construction equipment on data center sites
    # (3) Containerised power / UPS systems (growing product line)
    # This is a NEW secular tailwind not in analyst consensus models for CAT.
    ("Data center construction YoY",     48.0, "% YoY",   15,  30,  55, True,
     "backup power generators + construction equipment; new secular demand stream"),
]
WEIGHTS = [0.25, 0.20, 0.15, 0.15, 0.15, 0.10]

STRUCTURAL_FACTORS = [
    ("3,800-dealer global distribution moat",         0.8, 0.25),
    ("Steel / component tariff cost exposure",       -0.8, 0.30),
    ("Construction / mining cyclicality risk",       -0.5, 0.25),
    ("Data center power generation new TAM",          0.8, 0.10),
    ("Strong balance sheet net cash",                 0.5, 0.10),
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

vs_normal, restock_need, tailwind_ann, peak_headwind = dealer_cycle()

print()
print("═" * W)
print("  CAT SIGNAL MODEL  —  proxy vs. market-implied probability")
print("═" * W)

# Dealer inventory cycle
print(f"\n  DEALER INVENTORY CYCLE  (CAT's hidden production multiplier)")
print("  " + "─" * (W-2))
print(f"  Current dealer inventory:       {DEALER_MONTHS_CURRENT:.1f} months supply")
print(f"  Normal (neutral) level:         {DEALER_MONTHS_NORMAL:.1f} months")
print(f"  vs normal:                     {vs_normal:+.1f} months  {'(LEAN — restock territory)' if vs_normal < 0 else '(ELEVATED — destocking risk)'}")
print(f"  2024 peak (destocking):         {DEALER_MONTHS_PEAK:.1f} months  (~${peak_headwind/1000:.1f}B cumulative headwind now absorbed)")
print(f"  Potential restock tailwind:    ~${tailwind_ann/1000:.1f}B / yr revenue over next {ANNUAL_RESTOCK_WINDOW} years")
print(f"  → Inventory is below normal. ANY demand uptick triggers immediate")
print(f"    dealer restocking, amplifying production volumes above end-market demand.")

# Signal scorecard
print(f"\n  PROXY SIGNAL SCORECARD")
print(f"  {'Signal':<38}{'Value':>9}  Wt   Score")
print("  " + "─" * (W-2))
for name, val, unit, s, w, rt in scored:
    bar = "█" * s + "░" * (4 - s)
    if unit == "months":
        fmt = f"{val:>+7.1f}"
    elif unit == "ABI":
        fmt = f"{val:>+7.1f}"
    else:
        fmt = f"{val:>+7.1f}"
    print(f"  {name:<38}{fmt}{unit[0]}  {w*100:.0f}%  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:   {proxy_composite:.2f} / 4.00")
if mkt_composite:
    print(f"  Market composite:  {mkt_composite:.2f} / 4.00  "
          f"(back-solved from ${CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% reqd return)")
    gap = proxy_composite - mkt_composite
    direction = "market ahead of proxies" if gap < 0 else "proxies ahead of market"
    print(f"  Gap (proxy − mkt): {gap:+.2f}  ← {direction}")

# Valuation context
print(f"\n  VALUATION CONTEXT")
print("  " + "─" * (W-2))
fwd_eps = 17.5
print(f"  FY2025E non-GAAP EPS:       ~${fwd_eps:.2f}  (tariff headwind + cycle trough)")
print(f"  Current forward P/E:         {CURRENT_PRICE/fwd_eps:.1f}x  (historical range: 14-22x)")
print(f"  FY2024 actual EPS:           $21.90  (record; cycle peak year)")
print(f"  FY2026E CapEx:               ~$3.5B  (maintenance + modest expansion)")
print(f"  Net cash / debt:             Net cash positive (no leverage risk)")
print(f"  Dividend yield:              ~1.8%  (25+ year dividend growth streak)")
print(f"  → Cheap if recovery materialises; fair if tariffs persist and construction stalls")

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

  Cross-stock gap comparison (all models in this framework):
    ORCL gap = +2.16  (proxies near-XBULL; market prices massive delivery risk)
    AVGO gap = +1.41  (proxies bullish; market prices flow-through uncertainty)
    SAP  gap = +0.91  (proxies constructive; market in 'show me' mode on Joule)
    COIN gap = +0.29  (approximately fairly priced; it's just BTC price)
    CAT  gap = {gap:+.2f}  ← market is {'priced AHEAD of proxy confirmation' if gap < 0 else 'approximately aligned with proxies'}

  WHY CAT IS THE MOST EFFICIENTLY PRICED STOCK IN THIS FRAMEWORK:

    CAT has 30+ sell-side analysts, monthly dealer survey data, and
    transparent order backlog disclosures. Every signal in this model
    is in the consensus. The market has already absorbed them.

    Unlike ORCL's $300B OpenAI RPO (hard to value) or SAP's Joule
    (unmonetised AI option), CAT's proxies are straightforward numbers
    that every construction/mining analyst tracks weekly.

  WHAT THE {'NEGATIVE' if gap < 0 else 'SMALL'} GAP ACTUALLY MEANS:
    The market is pricing a cycle recovery that proxy signals {'confirm is beginning' if gap > -0.3 else 'do not yet fully support'}.
    This is NOT a bearish signal — it means:
      (a) If recovery materialises as proxies suggest → stock is fairly valued
      (b) If recovery accelerates beyond proxies → stock is cheap
      (c) If recovery stalls (tariffs, recession) → stock has 30-40% downside

  THE THREE THINGS THAT WOULD MOVE THE NEEDLE:

    1. Dealer restock inflection: When months supply falls below 2.5,
       dealers ORDER aggressively. Each down-0.5-month = ~$800M of
       incremental production revenue. Visible in monthly dealer surveys
       BEFORE it shows up in CAT's quarterly numbers.

    2. Data center power contracts: Each 1GW of new data center capacity
       requires ~$200-400M of backup generator infrastructure. At 50GW
       of AI data center buildout planned in 2025-2027, this is a
       $10-20B incremental TAM that consensus models don't fully price.

    3. Copper mine greenfield approval wave: Copper price >$4.50/lb
       makes previously uneconomic deposits viable. Each major mine
       approval (e.g., Resolution Copper, Oak Flat) = 5-7yr equipment
       supply contract. CAT has 60-70% market share in large mining trucks.

  THE RISK THE MARKET IS CORRECTLY PRICING:

    Tariff exposure: CAT imports ~$3B of steel/components annually.
    At 25% steel tariffs, COGS rises ~$600-750M → ~$3-4 EPS headwind.
    Simultaneously, retaliatory tariffs from China/EU on US manufacturers
    compress export demand (30%+ of revenue is outside North America).
    The bear case is NOT a construction collapse — it is tariffs
    persisting + strong USD compressing international margins.

  THE NON-CONSENSUS CATALYST (not yet in analyst models):
    AI data center power generation is modelled as a Construction
    Industries story (site work). It is actually an Energy &
    Transportation story — backup power, containerised generators,
    and UPS systems. E&T has CAT's highest margins (~20% operating).
    A single 500MW data center campus = $80-120M of CAT power equipment
    at 20% margins vs 13% for an equivalent construction equipment order.
    This margin mix-shift is not yet in sell-side models.""")
print()
print("═" * W)
