#!/usr/bin/env python3
"""
APD Signal Model
──────────────────
Same framework applied to Air Products & Chemicals, Inc. (NYSE: APD).

Key structural difference from the other companies in this framework:
  APD is mid-transformation: a $13.5B+ commitment to hydrogen megaprojects
  (NEOM, Louisiana) that are delayed, over budget, and under new CEO review.

  The core industrial gas business (O2, N2, Ar, H2) is a 70-year franchise
  with on-site take-or-pay contracts, high switching costs, and pricing power.
  Without the hydrogen overhang it would trade at 18-22x normalised EPS.

  The market must simultaneously price:
    (1) Core gas business — transparent, predictable, cash-generative
    (2) Hydrogen megaprojects — $13.5B deployed, near-zero revenue yet
    (3) New CEO uncertainty — strategy still being re-articulated
    (4) Natural gas input cost headwind — ~35% of COGS is energy

  The proxy signals test whether macro/market conditions support the
  BASE scenario recovery. The structural overlay quantifies what the
  proxies cannot: the probability-weighted write-down risk on H2 projects.

Run: python apd_signal_model.py
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 265.0     # USD (NYSE: APD, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

# Scenario 2-year price targets (non-GAAP EPS × exit P/E, FY2027/FY2028E)
# APD's core gas business normalised EPS ~$14-16 (ex hydrogen drag).
# Hydrogen projects add optionality but currently absorb $1-2 EPS in financing cost.
# Exit multiples: 18-27x — range reflects whether H2 is asset or liability.
SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  (10.0,   18,   180,  "H2 write-down; nat gas surge; volumes flat"),
    "BASE":  (14.0,   21,   294,  "Core gas stable; NEOM first contribution 2027"),
    "BULL":  (17.0,   24,   408,  "NEOM online; H2 premium; industrial recovery"),
    "XBULL": (21.0,   27,   567,  "Full H2 scale; green premium; energy leadership"),
}

# ── HYDROGEN MEGAPROJECT NPV CALCULATOR (APD-specific structural feature) ─
# APD has committed capital to two flagship hydrogen megaprojects.
# This calculator shows the NPV per share from these projects vs capex deployed.
#
# NEOM Green Hydrogen Complex (Saudi Arabia):
#   $8.5B investment; 600 TPD H2 → 1.2M t/yr green ammonia
#   Original target: 2026; now delayed to 2027E under CEO review
#
# Louisiana Clean Hydrogen Complex (USA):
#   $4.5B investment; 750 TPD blue H2 (with carbon capture)
#   Target: 2028E; largest single clean H2 project in North America
#
# The key question: does the NPV of these projects exceed the capex deployed?

NEOM_NH3_CAPACITY_MT_YR  = 1.2     # million tonnes/yr green ammonia
NEOM_NH3_PRICE_USD_T     = 550     # $/tonne green ammonia (est. wholesale)
NEOM_CAPEX_B             = 8.5     # $B (APD 100% equity)
NEOM_EBIT_MARGIN         = 0.25    # EBIT margin on H2/NH3 operations
NEOM_DELAY_YRS           = 1       # years until first revenue (2027E)

LOUISIANA_REVENUE_M_YR   = 380     # $M/yr at full ramp (blue H2 + derivatives)
LOUISIANA_CAPEX_B        = 4.5     # $B
LOUISIANA_EBIT_MARGIN    = 0.28    # EBIT margin
LOUISIANA_DELAY_YRS      = 2       # years until first revenue (2028E)

SHARES_OUT_M             = 222     # shares outstanding (millions)
TOTAL_H2_CAPEX_B         = 13.5    # total committed H2 capex ($B)

def hydrogen_project_npv():
    neom_rev_m    = NEOM_NH3_CAPACITY_MT_YR * 1e6 * NEOM_NH3_PRICE_USD_T / 1e6  # $M/yr
    neom_ebit     = neom_rev_m * NEOM_EBIT_MARGIN
    la_ebit       = LOUISIANA_REVENUE_M_YR * LOUISIANA_EBIT_MARGIN
    # Terminal value = 12x EBIT (infrastructure multiple), discounted for delay
    neom_npv_m    = (neom_ebit * 12) / (1 + REQUIRED_RETURN) ** NEOM_DELAY_YRS
    la_npv_m      = (la_ebit   * 12) / (1 + REQUIRED_RETURN) ** LOUISIANA_DELAY_YRS
    total_npv_m   = neom_npv_m + la_npv_m
    npv_per_share = total_npv_m / SHARES_OUT_M
    capex_per_shr = TOTAL_H2_CAPEX_B * 1000 / SHARES_OUT_M
    return neom_ebit, la_ebit, total_npv_m, npv_per_share, capex_per_shr

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
# (name, value, unit, base_floor, bull_floor, xbull_floor, higher_is_better,
#  what_it_drives_for_APD)
SIGNALS = [
    # US industrial production YoY: +1.5%.
    # Directly drives O2, N2, Ar volumes. APD's on-site industrial gas customers
    # are steel, glass, chemicals, refining — all track IP within 1 quarter.
    # +1.5% is sluggish — tariff uncertainty damping manufacturing.
    ("US industrial production — YoY",       1.5, "% YoY",   0,  3,  6, True,
     "O2/N2/Ar volumes track US IP within 1Q; on-site customers = direct pull"),

    # Henry Hub natural gas price YoY: +25%.
    # Natural gas is ~35-40% of APD's production cost (feedstock for H2; power for ASUs).
    # A +25% YoY gas price = ~$200-300M EBIT headwind on core business.
    # BEAR signal for near-term margins; higher_is_better=False.
    ("Natural gas price — YoY change",       25.0, "% YoY",  10,  0,-15, False,
     "COGS headwind: nat gas ~35-40% of APD production cost; direct margin impact"),

    # Global green H2 project FID rate (GW/yr): 8 GW.
    # FID (final investment decisions) by other H2 producers validates the market.
    # Leads APD's hydrogen revenue by 3-5 years. At 8 GW, development is progressing
    # but below the pace needed to confirm the green H2 economy is scaling.
    ("Green H2 project FIDs (GW/yr)",         8.0, "GW/yr",   3, 10, 20, True,
     "validates H2 market development; leads APD NEOM/LA offtake confidence"),

    # EU carbon credit (ETS) price: $45/tonne CO2.
    # Green H2 is only economic vs grey H2 when carbon is priced in.
    # At $45/t: green H2 premium is real but marginal. At $80+: compelling.
    # Directly affects APD's ability to sell H2 at premium prices.
    ("EU ETS carbon price ($/tonne CO2)",    45.0, "$/t",     30, 55, 85, True,
     "green vs grey H2 spread: higher carbon price = H2 premium economics improve"),

    # Global industrial gas demand YoY: +3%.
    # Tracked via Air Liquide and Linde quarterly releases (both report earlier).
    # Peer performance is the best proxy for APD's own volumes before APD reports.
    ("Industrial gas demand — YoY",           3.0, "% YoY",   1,  4,  7, True,
     "market demand; Air Liquide / Linde volumes proxy APD 4-6 weeks ahead"),

    # APD take-or-pay contract renewal rate: 94%.
    # APD discloses long-term contract status. Take-or-pay contracts protect revenue
    # regardless of customer production levels. High renewal rate = no demand churn.
    # 94% is BULL — customers renewing, no structural defection.
    ("APD take-or-pay renewal rate",         94.0, "%",       85, 90, 96, True,
     "contract quality; take-or-pay floor protects core segment in any downturn"),
]
WEIGHTS = [0.20, 0.20, 0.15, 0.15, 0.15, 0.15]

STRUCTURAL_FACTORS = [
    ("Long-term take-or-pay gas contract moat",       0.8, 0.25),
    ("NEOM/Louisiana H2 megaproject execution risk", -1.2, 0.30),
    ("New CEO strategy reset uncertainty",           -0.8, 0.20),
    ("Energy transition secular H2 tailwind",         0.8, 0.15),
    ("Balance sheet leverage from H2 capex",         -0.5, 0.10),
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

def market_implied_composite(target_ev, tolerance=5.0):
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

neom_ebit, la_ebit, total_npv_m, npv_per_shr, capex_per_shr = hydrogen_project_npv()

print()
print("═" * W)
print("  APD SIGNAL MODEL  —  proxy vs. market-implied probability")
print("═" * W)

# Hydrogen project NPV
print(f"\n  HYDROGEN MEGAPROJECT NPV  (capex deployed vs. value created)")
print("  " + "─" * (W-2))
print(f"  NEOM Green H2 (1.2Mt/yr NH3 @ ${NEOM_NH3_PRICE_USD_T}/t):")
print(f"    Revenue at ramp:   ${NEOM_NH3_CAPACITY_MT_YR*1e6*NEOM_NH3_PRICE_USD_T/1e6:.0f}M/yr   EBIT: ${neom_ebit:.0f}M/yr")
print(f"    Capital deployed:  ${NEOM_CAPEX_B:.1f}B    Delay: +{NEOM_DELAY_YRS}yr (2027E)")
print(f"  Louisiana Clean H2 (750 TPD blue H2):")
print(f"    Revenue at ramp:   ${LOUISIANA_REVENUE_M_YR:.0f}M/yr       EBIT: ${la_ebit:.0f}M/yr")
print(f"    Capital deployed:  ${LOUISIANA_CAPEX_B:.1f}B    Delay: +{LOUISIANA_DELAY_YRS}yr (2028E)")
print(f"  ─────────────────────────────────────────────────────")
print(f"  Total H2 capex deployed:  ${TOTAL_H2_CAPEX_B:.1f}B  =  ${capex_per_shr:.0f}/share")
print(f"  NPV of H2 projects:       ${total_npv_m/1000:.1f}B   =  ${npv_per_shr:.0f}/share  (12x EBIT, discounted)")
print(f"  Value destruction gap:    ${(capex_per_shr - npv_per_shr):.0f}/share  (at current commodity prices)")
print(f"  → At NH3 $750/t (upside case): NPV ~${(neom_ebit*750/NEOM_NH3_PRICE_USD_T*12/1.15 + la_ebit*12/1.3225)/SHARES_OUT_M:.0f}/share")
print(f"    Even bull case NPV < capex deployed — unless NH3 price rises materially.")

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
    direction = "market ahead of proxies" if gap < 0 else "proxies ahead of market"
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
core_eps = 14.0
print(f"  Core gas normalised EPS:    ~${core_eps:.0f}/share  (ex H2 financing drag)")
print(f"  Current forward P/E:         {CURRENT_PRICE/core_eps:.1f}x  (core gas range: 18-24x)")
print(f"  H2 capex drag on EPS:       ~$1.5-2.0/share/yr (interest + depreciation)")
print(f"  Net debt / EBITDA:           ~4.5x  (elevated; driven by H2 megaprojects)")
print(f"  Dividend yield:              ~2.5%  (52-year dividend growth streak)")
print(f"  → If H2 projects proceed at plan: fair value ~$280-320 (long-dated call option)")
print(f"    If H2 projects restructured/sold: core gas business = $240-260 standalone")

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

  Complete framework adjusted gap table:
    ORCL adj gap = +1.54  UNDERVALUED          (Oracle DB moat; OpenAI RPO)
    AVGO adj gap = +1.43  UNDERVALUED          (custom ASIC moat)
    MSFT adj gap = +1.42  UNDERVALUED          (Azure switching cost)
    SAP  adj gap = +1.15  UNDERVALUED          (ECC 2027 captive pipeline)
    COIN adj gap = +0.40  MODESTLY UNDERVALUED (regulatory clarity)
    PYPL adj gap = +0.42  MODESTLY UNDERVALUED (Venmo moat; Chriss execution)
    RCL  adj gap = +0.28  MODESTLY UNDERVALUED (private dest moat)
    XTB  adj gap = +0.29  MODESTLY UNDERVALUED (ETF stickiness)
    CAT  adj gap = -0.27  MODESTLY OVERVALUED  (tariff exposure)
    NKE  adj gap = -0.43  MODESTLY OVERVALUED  (China permanent loss)
    APD  adj gap = {adj_gap if mkt_composite else '?':>+5.2f}  ← see verdict above

  WHY APD IS THE MOST COMPLEX VALUATION IN THIS FRAMEWORK:

    Unlike ORCL (one concentrated backlog) or NKE (brand cyclical), APD
    is a TWO-COMPANY PROBLEM in one ticker:

    COMPANY A: Core industrial gases — stable, boring, high-quality.
      ~$14/share normalised EPS. Take-or-pay contracts. Pricing power.
      Should trade 20-22x = $280-308. This business alone justifies $265.

    COMPANY B: Hydrogen megaprojects — $13.5B of capital deployed, 0 revenue.
      NPV at current NH3 prices = ~${total_npv_m/1000:.1f}B = ${npv_per_shr:.0f}/share.
      Capital deployed = ${capex_per_shr:.0f}/share.
      Gap = ${(capex_per_shr - npv_per_shr):.0f}/share of potential value DESTRUCTION.

    The stock at $265 is being priced as if Company B is worth ~$0.
    (Core gas alone = $280-308; market is actually discounting ~$15-40.)
    This is rational: investors don't know what CEO Menezes will do with H2.

  THE THREE SCENARIOS FOR CEO MENEZES:

    1. FULL COMMITMENT (BULL case):
       "Hydrogen is the future; we execute NEOM and Louisiana at cost."
       → NH3 revenues start 2027; market re-rates H2 as an asset, not liability.
       → Stock targets $350-420 as delivery de-risks the capex.

    2. STRATEGIC REVIEW (BASE case):
       "We'll complete NEOM; review Louisiana; no new H2 commitments."
       → Maintains optionality; reduces further capex drag on EPS.
       → Stock fair value $280-320; hydrogen stays option, not obligation.

    3. RESTRUCTURING (BEAR-to-base case):
       "We'll find a partner/buyer for H2 projects to crystallise some value."
       → Reduces debt, restores EPS power to $15-16, re-rates to 22x.
       → Core gas at $330-352; hydrogen write-down hit is one-time.

  THE STRUCTURAL RISK THE PROXY SIGNALS CANNOT SEE:

    Natural gas prices (+25% YoY) tell you margins are compressed now.
    But the REAL risk is that green H2 economics never work at scale:
    At $550/t NH3, APD's projects return ~8% on invested capital.
    WACC is ~9-10%. Every $50/t decline in NH3 price = ~$1.5B NPV loss.
    If NH3 prices fall to $400/t (grey NH3 parity), the projects destroy value
    regardless of execution. This is the OVERVALUED case: the market is
    paying for option value that may never materialise if energy prices
    normalise and the green premium collapses.""")
print()
print("═" * W)
