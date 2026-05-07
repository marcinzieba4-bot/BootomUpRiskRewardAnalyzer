#!/usr/bin/env python3
"""
Nike Signal Model
──────────────────
Same framework applied to Nike, Inc. (NYSE: NKE).

Key structural difference from every other company in this framework:
  NKE is NOT a growth story — it is a TURNAROUND.
  The analytical question is not "will tailwinds persist?" but
  "will the fix work?"

  Context: CEO John Donahoe stepped down Oct 2024 → Elliott Hill (returning
  Nike veteran) took over. Recovery plan: rebuild wholesale relationships
  damaged by over-indexing on DTC, restore premium brand positioning,
  cut $2B in costs, refocus on sport-performance storytelling.

  The stock fell ~50% from its 2021 peak ($179) to trough (~$70) as:
    1. DTC over-rotation cut retailer relationships → channel conflict
    2. Gross margin declined 2.5pp from peak (heavy discounting)
    3. Greater China revenue stalled (geopolitics + local brands)
    4. Disruptive competitors (On Running, HOKA) took premium running share
    5. Inventory bloat required margin-dilutive clearance (now resolved)

  The gap in this model has a different meaning than ORCL/AVGO/MSFT:
  here, a NEGATIVE gap means the market is PRICING IN HOPE that proxy
  signals haven't yet confirmed. This is a structural feature of turnarounds.

Run: python nke_signal_model.py
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 77.0      # USD (NYSE: NKE, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

# Scenario 2-year price targets (non-GAAP EPS × exit P/E multiple)
# FY2025E non-GAAP EPS: ~$2.70 (trough; heavily discounted year).
# FY2028 scenarios assume recovery path under Elliott Hill.
# Multiple range 20-30x: Nike is premium consumer brand — deserves premium
# vs market only if it re-establishes pricing power and brand heat.
SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  ( 1.5,   20,    30,  "Turnaround fails; China loss permanent; On/HOKA cement share"),
    "BASE":  ( 3.5,   23,    81,  "Partial recovery; GM +150bp; wholesale rebuilt; China stable"),
    "BULL":  ( 5.0,   27,   135,  "Full recovery; GM 47%+; product heat returns; China rebounds"),
    "XBULL": ( 7.0,   30,   210,  "Re-establishment as dominant brand; China boom; AI personalisation"),
}

# ── GROSS MARGIN RECOVERY CALCULATOR (NKE-specific structural feature) ───
# The turnaround thesis is primarily a MARGIN story, not a volume story.
# Nike's gross margin fell from a ~46.6% peak (FY2022) to ~44.0% (FY2024)
# via: (1) heavy promotional discounting to clear inventory,
#      (2) DTC mix headwinds (higher cost to serve vs wholesale),
#      (3) input cost inflation (transport, materials).
# Elliott Hill's key levers: less promo, less outlet, premium positioning.
# Revenue base and share count stable; GM recovery = direct EPS leverage.

REVENUE_BASE_B      = 47.0     # FY2025E revenue ($B)
GM_CURRENT_PCT      = 44.5     # FY2025E gross margin (%)
GM_PEAK_PCT         = 46.6     # FY2022 peak gross margin (%)
GM_TARGET_PCT       = 47.5     # bull case GM target (%)
SHARES_OUT_B        =  1.22    # diluted shares outstanding (billions)
TAX_RATE            =  0.19    # effective tax rate

def gm_recovery():
    gm_gap_to_peak   = GM_PEAK_PCT - GM_CURRENT_PCT   # pp to recover to peak
    gm_gap_to_target = GM_TARGET_PCT - GM_CURRENT_PCT  # pp to bull-case target
    # Each 1pp of GM on $47B revenue = incremental EBIT
    rev_per_pp       = REVENUE_BASE_B * 1e9 * 0.01     # $ per 1pp
    ebit_per_pp      = rev_per_pp / 1e9                 # $B per 1pp
    eps_per_pp       = ebit_per_pp * (1 - TAX_RATE) / SHARES_OUT_B  # $/share per 1pp
    eps_peak_recovery = gm_gap_to_peak * eps_per_pp
    eps_target        = gm_gap_to_target * eps_per_pp
    return gm_gap_to_peak, gm_gap_to_target, eps_per_pp, eps_peak_recovery, eps_target

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
# NKE signals are consumer-demand and brand-health focused — fundamentally
# different from the capex/cloud/backlog signals used in the tech models.
#
# (name, value, unit, base_floor, bull_floor, xbull_floor, higher_is_better,
#  what_it_drives_for_NKE)
SIGNALS = [
    # US consumer discretionary spend YoY: +3.5%.
    # Nike earns ~43% of revenue in North America. Discretionary spend
    # is the primary macro driver of athletic footwear / apparel demand.
    # Tariff headwinds and elevated rates keeping spend below trend.
    ("US consumer discretionary YoY",    3.5, "% YoY",    2,   5,   9, True,
     "North America segment (~43% of rev); consumer willingness to pay $120+ for sneakers"),

    # China sportswear retail sales YoY: +4%.
    # Greater China = ~15% of NKE revenue, but was 22% at peak (2021).
    # Recovery is slow: geopolitics (US-China tension), local brand competition
    # (Anta, Li-Ning), and weakened Chinese consumer confidence post-property crisis.
    ("China sportswear retail YoY",       4.0, "% YoY",    3,   7,  12, True,
     "Greater China segment (~15% of rev); structural recovery or permanent share loss"),

    # Key wholesale partner comps (Foot Locker + Dick's Sporting Goods YoY): +5%.
    # Nike's decision to rebuild wholesale after the DTC over-rotation.
    # FL and DKS comps are the best lead indicator for Nike wholesale order health:
    # strong comps → partners re-order → Nike wholesale revenue recovers.
    ("Wholesale partner comps YoY",       5.0, "% YoY",    0,   5,  10, True,
     "channel rebuild signal: FL/DKS health → Nike wholesale order book re-fill"),

    # Nike gross margin YoY change (pp): +0.3pp.
    # The most critical internal metric. Recovery from 44.5% toward 46-47%
    # is the primary driver of EPS recovery. Currently stabilising —
    # not yet the 1-2pp annual recovery the bull case requires.
    ("Nike gross margin change (pp YoY)", 0.3, "pp YoY", -0.5,   1,   2, True,
     "pricing power proxy; recovering GM = less discounting + premium positioning working"),

    # On Running revenue YoY (INVERSE signal): +28%.
    # On Running (ONON) growing at +28% YoY is the clearest signal of
    # competitive displacement in Nike's highest-margin running category.
    # Higher On growth = more share lost in premium performance running.
    # Each ~$600M of On incremental revenue represents ex-Nike wallet share.
    ("On Running revenue YoY (inverse)",  28.0, "% YoY",  20,  15,  10, False,
     "competitive displacement: On + HOKA taking premium running share from Nike"),

    # Nike DTC digital comparable sales: +6%.
    # Nike.com and SNKRS app comps measure brand heat and premium pricing
    # without channel noise. Recovering DTC comps = consumers still seeking
    # Nike directly at full price (vs. off-price / Foot Locker clearance).
    ("Nike DTC digital comparable sales", 6.0, "% YoY",    0,   5,  12, True,
     "brand heat and full-price demand; recovering DTC = pricing power returning"),
]
WEIGHTS = [0.20, 0.20, 0.15, 0.15, 0.15, 0.15]

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
proxy_probs     = softmax_probs(proxy_composite)
proxy_ev        = expected_price(proxy_probs)

market_target_ev  = CURRENT_PRICE * ((1 + REQUIRED_RETURN) ** HORIZON_YEARS)
mkt_composite, mkt_probs = market_implied_composite(market_target_ev)
mkt_ev = expected_price(mkt_probs) if mkt_probs else market_target_ev

gm_gap_peak, gm_gap_target, eps_per_pp, eps_peak, eps_target = gm_recovery()

print()
print("═" * W)
print("  NKE SIGNAL MODEL  —  proxy vs. market-implied probability")
print("═" * W)
print(f"  ⚠  Turnaround context: Elliott Hill (CEO since Oct 2024) executing reset.")

# Gross margin recovery
print(f"\n  GROSS MARGIN RECOVERY CALCULATOR  (the turnaround in one number)")
print("  " + "─" * (W-2))
print(f"  Current gross margin (FY2025E):      {GM_CURRENT_PCT:.1f}%")
print(f"  Peak gross margin (FY2022):          {GM_PEAK_PCT:.1f}%  (-{gm_gap_peak:.1f}pp from peak)")
print(f"  Bull-case target:                    {GM_TARGET_PCT:.1f}%  (+{gm_gap_target:.1f}pp recovery needed)")
print(f"  Revenue base (FY2025E):              ${REVENUE_BASE_B:.0f}B")
print(f"  ─────────────────────────────────────────────────────")
print(f"  EPS impact per 1pp GM recovery:      ${eps_per_pp:.2f} / share  ← the leverage")
print(f"  Recovery to {GM_PEAK_PCT:.1f}% peak → EPS tailwind:  +${eps_peak:.2f} / share")
print(f"  Recovery to {GM_TARGET_PCT:.1f}% target → EPS uplift: +${eps_target:.2f} / share")
print(f"\n  WHY MARGINS FELL:  inventory discounting (resolved) + DTC promo + FX.")
print(f"  WHY THEY CAN RECOVER:  less promo is a strategic choice, not market-dependent.")
print(f"  → This is largely WITHIN NIKE'S CONTROL. The bull case doesn't require macro.")

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
    print(f"  Gap (proxy − mkt): {gap:+.2f}  ← market pricing TURNAROUND HOPE ahead of data")

# Valuation context
print(f"\n  VALUATION CONTEXT")
print("  " + "─" * (W-2))
fwd_eps = 2.70
print(f"  FY2025E non-GAAP EPS:       ~${fwd_eps:.2f}  (trough year)")
print(f"  FY2026E non-GAAP EPS:       ~$3.20  (partial recovery expected)")
print(f"  Current P/E on FY2025E:      {CURRENT_PRICE/fwd_eps:.0f}x  (distressed-year multiple)")
print(f"  Current P/E on FY2026E:      {CURRENT_PRICE/3.20:.0f}x  (forward recovery multiple)")
print(f"  2021 peak EPS:               ~$3.56  (pre-DTC-over-rotation peak)")
print(f"  2021 peak stock price:       ~$179   (at ~50x peak-year EPS)")
print(f"  Dividend yield:              ~2.3%   (dividend maintained throughout decline)")
print(f"  Net cash:                    ~$10B cash vs ~$9B debt — roughly net flat")
print(f"  → At $77, market is paying 24x FY2026E for a brand that earned $3.56 EPS in FY2021.")
print(f"    The implicit bet: Nike EPS returns to at least $3.50 and the multiple holds.")

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
    COIN gap = +0.29  (approximately fairly priced; thesis is BTC price)
    CAT  gap = -0.24  (market priced ahead of confirmed cycle recovery)
    NKE  gap = {gap:+.2f}  ← market priced ahead of UNCONFIRMED recovery

  WHY NKE'S NEGATIVE GAP IS DIFFERENT FROM CAT'S NEGATIVE GAP:

    CAT (-0.24): Market priced ahead of data because EVERY proxy signal
    confirms a genuine recovery IS happening — dealer inventory lean,
    data center construction strong, mining capex up. The market is just
    one step ahead of lagging monthly surveys. The gap should close.

    NKE ({gap:+.2f}): Market priced ahead of data because investors are
    BETTING on turnaround success BEFORE proxies confirm it. The
    competitor displacement signal (On Running +28%) is actively BEARISH.
    China is only modestly positive. GM recovery is just +0.3pp, not the
    1-2pp the bull case needs. The market is discounting the bad signals
    and buying the hope. This gap may NOT close — it may widen bearishly.

  THE THREE SIGNALS TO WATCH (in order of importance):

    1. Gross margin quarterly progression: The single most important
       data point. If Nike's Q1 FY2026 reports GM +100bp+ YoY, the
       turnaround is working (pricing discipline confirmed). If GM stays
       flat or declines, Elliott Hill's reset is failing. Published 4x/yr.

    2. On Running quarterly revenue growth rate: If On slows to <20% YoY
       (saturation signal), Nike is no longer losing net share in running.
       If On accelerates to 35%+, Nike running is a structural loss.
       Published quarterly via ONON earnings.

    3. China quarterly revenue: Greater China was 22% of NKE revenue in
       FY2021, now ~15%. Even a stabilisation at 15% is fine; a recovery
       to 18-20% is the BULL case; further erosion to 12% is the BEAR.

  THE STRUCTURAL RISK NOT IN THE MODEL — LOCAL BRAND DISRUPTION IN CHINA:
    Anta and Li-Ning are not just cheap alternatives. They have signed
    Chinese Olympic athletes, launched premium performance lines, and
    operate thousands of stores that are culturally resonant in ways that
    a Beaverton, Oregon brand cannot easily replicate. The Chinese consumer
    in 2026 is different from 2019: national brand preference has
    structurally increased. Nike's Chinese market share loss may be
    permanent — not cyclically driven but identity-driven.

  THE NON-CONSENSUS BULL CASE (mostly within Nike's control):
    Gross margin recovery from 44.5% to 47% requires NO volume growth.
    It requires only: stop discounting, reduce SNKRS / Nike.com promo,
    return to wholesale at higher ASP, reduce outlet channel mixing.
    At $47B revenue × 47% GM × tax-effected = ~$5.00 EPS without
    a single additional unit sold. At 27x (below 2019 median of 32x):
    $5 × 27x = $135 (BULL scenario, +75% from current $77).
    This is the asymmetry: the bull case is operational execution,
    not macro recovery. Markets systematically underprice CEO-controlled
    operational levers in favour of macro sensitivity analysis.""")
print()
print("═" * W)
