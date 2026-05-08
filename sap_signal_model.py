#!/usr/bin/env python3
"""
SAP Signal Model
──────────────────
Same framework applied to SAP SE (NYSE: SAP).

Key structural difference from AVGO and COIN:
  86% of revenue is predictable (cloud + maintenance contracts)
  Built-in demand catalyst: ECC maintenance ends 2027 → 21,000 customers
  must migrate to S/4HANA — structural demand pipe regardless of macro
  Stock trades 23% BELOW its 10-year median P/E despite solid fundamentals

The interesting question: why is the market pricing SAP below median
when proxy signals are constructive? The gap explains the thesis.

Run: python sap_signal_model.py
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 173.0     # USD (NYSE ADR, each = 1 ordinary share)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2
EUR_USD         = 1.12      # approximate; drives reported vs CC gap

# Scenario 2-year price targets (non-IFRS EPS in USD × exit multiple)
# SAP 10-yr median P/E: 30.65x — currently at 23.6x (23% discount)
# Exit multiples below median justified only if growth slows materially
SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  ( 6.0,   18,   108,  "Cloud decelerates to 10%; Joule fails; migration stalls"),
    "BASE":  ( 9.0,   25,   225,  "Cloud 23-25%; ECC wave executes; Joule 10%+ adoption"),
    "BULL":  (12.0,   30,   360,  "Cloud 30%+; Joule monetisation begins; buyback accretive"),
    "XBULL": (15.0,   35,   525,  "ECC surge + Joule premium pricing + EUR/USD tailwind"),
}

# ── STRUCTURAL DEMAND CALCULATOR (SAP-specific, like COIN's floor) ────────
ECC_TOTAL_CUSTOMERS     = 35_000
ECC_MIGRATED_PCT        = 0.39        # 39% migrated by end of 2024
ECC_ACTIVE_PROJECTS_PCT = 0.25        # ~25% of remaining have active projects
AVG_MIGRATION_ACV_EUR_M = 0.8         # avg annual cloud contract per migration ($M)
ECC_MAINSTREAM_END      = 2027        # ECC mainstream support ends

def migration_pipeline():
    remaining     = ECC_TOTAL_CUSTOMERS * (1 - ECC_MIGRATED_PCT)
    active        = remaining * ECC_ACTIVE_PROJECTS_PCT
    uncommitted   = remaining * (1 - ECC_ACTIVE_PROJECTS_PCT)
    active_acv    = active * AVG_MIGRATION_ACV_EUR_M / 1000      # €B / yr
    potential_acv = uncommitted * AVG_MIGRATION_ACV_EUR_M / 1000  # €B / yr (not yet committed)
    return remaining, active, uncommitted, active_acv, potential_acv

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
# Chosen to cover: enterprise budget health, structural migration demand,
# FX (key reported-vs-CC wedge), AI adoption pace, and leading backlog.
#
# (name, value, unit, base_floor, bull_floor, xbull_floor, higher_is_better,
#  what_it_drives_for_SAP)
SIGNALS = [
    # ServiceNow Q1 2026: +22% YoY revenue. Best enterprise IT budget proxy.
    # SAP and ServiceNow co-exist in every large enterprise; their budgets move together.
    ("ServiceNow rev growth YoY",      22.0, "% YoY",    10,  15,  25, True,
     "enterprise IT budget health; co-purchased in same enterprise accounts"),

    # SAP current cloud backlog (CC growth): +25% Q1 2026.
    # Contracted-not-yet-recognised revenue. Converts to revenue in 4-18 months.
    # This is SAP's own data but genuinely leads reported revenue by 2-3Q.
    ("SAP cloud backlog growth CC",    25.0, "% CC",     10,  20,  30, True,
     "contracted future cloud revenue; 2-3Q lead on reported cloud growth"),

    # ECC migration urgency (scored 1-4 ordinal):
    # 1=no urgency, 2=moderate, 3=deadline pressure building, 4=crisis migration
    # Current: 21,000 customers unmirgated, 18 months to ECC mainstream end → 3
    ("ECC migration urgency",           3.0, "/4 scale",  1,   2,   4, True,
     "structural demand: 21K ECC customers face 2027 deadline — captive pipeline"),

    # Gartner enterprise software spend YoY: +14.7% in 2026.
    # Measures TAM expansion pace — directly expands SAP's addressable market.
    ("Enterprise software spend YoY",  14.7, "% YoY",     5,  10,  15, True,
     "ERP/cloud market expansion; portion flows directly to SAP migrations"),

    # EUR/USD rate (INVERSE for SAP): SAP earns and reports in EUR.
    # NYSE ADR investors care about USD EPS. Strong EUR = headwind on USD reporting.
    # Q1 2026 had +12% CC growth but only +6% reported — 6pp FX drag.
    # Current EUR/USD ~1.12 → moderate headwind (BASE signal).
    ("EUR/USD rate (inverse)",          1.12, "EUR/USD",1.05, 1.10, 1.20, False,
     "FX translation: strong EUR compresses USD EPS and reported revenue growth"),

    # Joule AI production adoption: currently 3% of SAP customers in production.
    # Grew 9x in 2025. Still early — market waiting for monetisation proof.
    # Bull/XBULL requires >10% adoption where premium pricing kicks in.
    ("Joule AI production adoption",    3.0, "%",          1,   5,  15, True,
     "AI monetisation optionality; premium ACV uplift when adoption >10%"),
]
WEIGHTS = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]

# ── STRUCTURAL RISK OVERLAY ──────────────────────────────────────────────
STRUCTURAL_FACTORS = [
    ("ECC 2027 deadline — captive 21K pipeline",      1.5, 0.30),
    ("EUR/USD structural reporting headwind",         -0.5, 0.20),
    ("Joule monetisation timeline uncertainty",       -0.8, 0.20),
    ("S/4HANA migration complexity discount",         -0.5, 0.15),
    ("86% ARR-quality revenue base resilience",        0.8, 0.15),
]


FLOOR_DATA = {
    "trough_year":        2022,
    "trough_price":       75.0,
    "cum_fcf_per_share":  13.2,
    "debt_delta":         -3.6,     # +ve = debt grew (EPP lower); -ve = improved
    "structural_delta":   8.0,  # +ve = fundamentals improved; -ve = weaker today
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
proxy_composite = sum(s * w for *_, s, w, _ in scored)
sca           = sum(s * w for _, s, w in STRUCTURAL_FACTORS)
adj_composite = proxy_composite + sca
proxy_probs     = softmax_probs(proxy_composite)
proxy_ev        = expected_price(proxy_probs)

market_target_ev  = CURRENT_PRICE * ((1 + REQUIRED_RETURN) ** HORIZON_YEARS)
mkt_composite, mkt_probs = market_implied_composite(market_target_ev)
mkt_ev = expected_price(mkt_probs) if mkt_probs else market_target_ev

remaining, active, uncommitted, active_acv, potential_acv = migration_pipeline()

print()
print("═" * W)
print("  SAP SIGNAL MODEL  —  proxy vs. market-implied probability")
print("═" * W)

# Structural demand math
print(f"\n  ECC MIGRATION PIPELINE  (structural demand regardless of macro)")
print("  " + "─" * (W-2))
print(f"  Total ECC customers                              {ECC_TOTAL_CUSTOMERS:>7,}")
print(f"  Migrated to S/4HANA by end-2024 (~39%)          {int(ECC_TOTAL_CUSTOMERS*ECC_MIGRATED_PCT):>7,}")
print(f"  Still on ECC — must migrate by 2027             {int(remaining):>7,}")
print(f"    → active migration projects (~25%)            {int(active):>7,}   ~€{active_acv:.1f}B ACV in-flight")
print(f"    → not yet committed (~75%)                    {int(uncommitted):>7,}   ~€{potential_acv:.1f}B ACV pipeline")
print(f"  ECC mainstream support ends:                     {'2027':>7}")
print(f"  → This pipeline is CAPTIVE. Customers can delay but not avoid.")

# Signal scorecard
print(f"\n  PROXY SIGNAL SCORECARD")
print(f"  {'Signal':<38}{'Value':>9}  Wt   Score")
print("  " + "─" * (W-2))
for name, val, unit, s, w, rt in scored:
    bar = "█" * s + "░" * (4 - s)
    fmt = f"{val:>+7.2f}" if unit not in ("/4 scale",) else f"{val:>+7.1f}"
    print(f"  {name:<38}{fmt}{unit[0]}  {w*100:.0f}%  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:   {proxy_composite:.2f} / 4.00")
if mkt_composite:
    print(f"  Market composite:  {mkt_composite:.2f} / 4.00  "
          f"(back-solved from ${CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% reqd return)")
    gap = proxy_composite - mkt_composite
    print(f"  Gap (proxy − mkt): {gap:+.2f}  ← the trade")

# Multiple context
print(f"\n  VALUATION CONTEXT")
print("  " + "─" * (W-2))
fwd_eps_usd = 6.84 * EUR_USD
print(f"  SAP 10-yr median P/E:   30.6x")
print(f"  Current trailing P/E:   24.3x  (23% BELOW median)")
print(f"  Current forward P/E:    20.2x  (on ~€6.84 / ${fwd_eps_usd:.2f} 2026E EPS)")
print(f"  Analyst avg target:     $288-306  (+{(295/CURRENT_PRICE-1)*100:.0f}% vs current)")
print(f"  → Market is in 'show me' mode on Joule monetisation")

# Probability table
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
print(f"  \u2192 Same pessimism \u2260 same price: FCF locked in, inflation ratcheted every nominal anchor.")
if _sdelta < 0:
    print(f"    Structural damage since {_yr}: equal pessimism = lower price than CPI-adj {_yr} trough.")
elif _sdelta > 0:
    print(f"    Structural gains since {_yr}: equal pessimism = higher price than CPI-adj {_yr} trough.")

# Verdict
print(f"\n  WHAT THE GAP MEANS")
print("  " + "─" * (W-2))
gap = (proxy_composite - mkt_composite) if mkt_composite else 0
print(f"""  Proxy composite {proxy_composite:.2f}  vs  market-implied {mkt_composite:.2f}.
  Gap = {gap:+.2f}

  AVGO gap was +1.41 (proxies far ahead — priced for perfection).
  COIN gap was +0.29 (proxies confirm price — BTC is just the thesis).
  SAP gap is  {gap:+.2f} (proxies constructive, market discounting — why?)

  FOUR REASONS THE MARKET IS BELOW PROXIES:

    1. FX illusion: cloud backlog grows 25% CC but only 19% reported.
       US investors see reported USD numbers first. EUR strength at 1.12
       creates a 6pp wedge that flatters CC metrics vs actual USD delivery.

    2. Joule is unmonetised: only 3% of customers in production. Market
       assigns near-zero value to AI premium pricing until adoption
       crosses ~10-15%. The 9x growth in 2025 is notable but from tiny base.

    3. Migration complexity discount: The Register survey (Feb 2026) found
       most SAP ECC migrations bust budgets and deadlines. Market applies
       execution risk discount to the 21,000-customer pipeline.

    4. ECC 'imminent deadline' fatigue: This deadline has been extended
       before (2025 → 2027 → extended maintenance to 2030). Market may
       be sceptical that urgency translates to acceleration.

  THE BULL CASE REQUIRES ONLY BASE ASSUMPTIONS:
    Cloud backlog converting normally → €26B cloud in 2026 (on track).
    Multiple returning to 10-yr median (30x) on €9 USD EPS → $270.
    That is a +56% return from $173 on no heroic assumptions.

  THE NON-CONSENSUS CATALYST (not yet priced):
    Joule crossing 10%+ production adoption with measurable ACV uplift.
    Each 10pp increase in adoption at €500/user/yr premium =
    ~€500M additional annual revenue at SAP's installed base scale.""")
print()
print("═" * W)
