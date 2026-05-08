#!/usr/bin/env python3
"""
PayPal Signal Model
─────────────────────
Same framework applied to PayPal Holdings, Inc. (NASDAQ: PYPL).

Key structural difference from every other company in this framework:
  PYPL is a QUALITY RESET story — not tech growth (MSFT/ORCL), not a
  turnaround (NKE), but a mature payments processor re-rating from
  'high-growth fintech' (60-70x P/E in 2021) to 'utility processor'
  (~17x today) while a new CEO (Alex Chriss, Sep 2023) tries to reverse
  the revenue growth deceleration without compromising buyback-driven EPS.

  The brutal math: stock fell 75% (peak $309 → trough $55) while EPS
  was essentially FLAT ($4.60 FY2021 → $4.65 FY2024). This is 100% a
  multiple compression story, not an earnings story. The bull case is
  multiple re-expansion as branded checkout recovers; the bear case is
  further structural displacement by Apple Pay / AI-native wallets.

  THE TAKE RATE DECOMPOSITION is the analytical key no proxy signals show:
  - Branded PayPal checkout: ~2.3% take rate (high margin)
  - Unbranded Braintree processing: ~0.7% take rate (low margin)
  - Dan Schulman overbuilt Braintree → mix shift → blended take rate fell
  - Alex Chriss: slow Braintree intentionally, rebuild branded share
  - Each 1pp mix shift from Braintree to branded = ~$1B incremental ARR

Run: python pypl_signal_model.py
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 78.0      # USD (NASDAQ: PYPL, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

# Scenario 2-year price targets (non-GAAP EPS × exit P/E multiple)
# FY2025E non-GAAP EPS: ~$4.70 (buybacks + cost cuts, modest revenue growth)
# Multiple range: 13-25x — PayPal is between 'utility processor' (13-15x)
# and 'fintech platform' (22-26x). Re-rating requires revenue re-acceleration.
SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  ( 3.0,   13,    39,  "Apple Pay/AI wallets structurally displace PYPL checkout"),
    "BASE":  ( 6.0,   17,   102,  "Chriss executes; take rate stabilises; Venmo monetises"),
    "BULL":  ( 9.0,   21,   189,  "Branded checkout revival; ads platform grows; Venmo at scale"),
    "XBULL": (12.0,   25,   300,  "PayPal = primary wallet for AI-native commerce; re-rates to fintech"),
}

# ── TAKE RATE DECOMPOSITION (PYPL-specific structural feature) ────────────
# Total revenue = (Branded TPV × branded take rate) + (Unbranded TPV × unbranded take rate)
# The Chriss strategy: shift TPV mix back toward branded.
# Each 1pp shift in branded mix from unbranded to branded = ~$1B incremental ARR.

TOTAL_TPV_T         = 1.65       # total payment volume ($T, FY2025E)
BRANDED_MIX_PCT     = 46         # branded checkout % of TPV
BRANDED_TAKE_RATE   = 2.30       # % take rate on branded checkout TPV
UNBRANDED_TAKE_RATE = 0.72       # % take rate on Braintree/unbranded TPV
PEAK_BRANDED_MIX    = 55         # % branded at peak (FY2019) before DTC push

def take_rate_economics():
    unbranded_mix    = 100 - BRANDED_MIX_PCT
    blended          = (BRANDED_MIX_PCT * BRANDED_TAKE_RATE +
                        unbranded_mix * UNBRANDED_TAKE_RATE) / 100
    current_rev      = TOTAL_TPV_T * 1e12 * blended / 100 / 1e9   # $B
    take_rate_prem   = BRANDED_TAKE_RATE - UNBRANDED_TAKE_RATE      # pp premium
    # Revenue uplift per 1pp shift from unbranded to branded:
    rev_per_pp_shift = TOTAL_TPV_T * 1e12 * (take_rate_prem / 100) * 0.01 / 1e9  # $B per pp shift
    # If Chriss recovers mix to peak (55% branded):
    recovery_blend   = (55 * BRANDED_TAKE_RATE + 45 * UNBRANDED_TAKE_RATE) / 100
    recovery_rev     = TOTAL_TPV_T * 1e12 * recovery_blend / 100 / 1e9
    mix_recovery_upside = recovery_rev - current_rev
    return blended, current_rev, take_rate_prem, rev_per_pp_shift, mix_recovery_upside

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
# PYPL signals must cover: e-commerce TAM health, engagement depth (not breadth),
# competitive ecosystem (Shopify = key partner), take rate trend, cross-border
# (PYPL's highest-take-rate segment), and BNPL (Pay Later segment growth).
#
# (name, value, unit, base_floor, bull_floor, xbull_floor, higher_is_better,
#  what_it_drives_for_PYPL)
SIGNALS = [
    # US e-commerce sales YoY: +7% (Census Bureau, Q1 2026).
    # PayPal's core TAM is US/global e-commerce. At +7%, the market is growing
    # at a healthy pace — not boom conditions but not contracting.
    # PayPal's TPV grows roughly in line with e-commerce (may gain/lose share).
    ("US e-commerce sales YoY",           7.0, "% YoY",    4,   8,  14, True,
     "primary TAM: PayPal processes ~16% of US e-commerce; market growth = floor"),

    # PayPal transactions per active account: 62 TPA.
    # The engagement metric. More transactions per user = deeper wallet integration.
    # Chriss target: 60+ TPA (vs 45 TPA in 2022). At 62, the engagement push is working.
    # This leads revenue by 2-3 quarters — more engaged users = more monetisation.
    ("PayPal transactions / active acct", 62.0, "TPA",     55,  65,  75, True,
     "engagement depth → revenue quality; drives monetisation per user, not account count"),

    # Shopify GMV YoY: +23%.
    # Shopify is PYPL's largest e-commerce platform partner (and partial competitor).
    # Strong Shopify GMV = healthy SMB e-commerce ecosystem where PYPL checkout
    # is offered. Also validates that non-Amazon e-commerce is growing.
    ("Shopify GMV YoY",                  23.0, "% YoY",   10,  20,  30, True,
     "SMB e-commerce ecosystem health; Shopify merchants = large PYPL checkout cohort"),

    # PayPal blended take rate YoY change: -0.03pp.
    # The single most important internal indicator. Under Schulman, take rate fell
    # ~0.15-0.20pp per year. Under Chriss, intentional Braintree slowdown means
    # take rate is near-stabilising (-0.03pp). Not yet positive but improving trend.
    ("PYPL blended take rate change",    -0.03, "pp YoY", -0.15,  0, 0.10, True,
     "mix quality signal: near-zero means Braintree drag is ending; positive = re-rating"),

    # Global cross-border e-commerce growth YoY: +15%.
    # PayPal has a structural advantage in cross-border payments (FX, buyer protection).
    # Cross-border transactions carry a ~2.5% take rate vs ~1.8% domestic.
    # Strong cross-border growth = revenue mix improvement without needing branded recovery.
    ("Global cross-border e-commerce",   15.0, "% YoY",    8,  15,  22, True,
     "premium take-rate segment (~2.5%); PayPal trusted brand advantage in cross-border"),

    # BNPL (Buy Now Pay Later) industry volume YoY: +22%.
    # PayPal Pay Later is a top-3 BNPL provider in the US by volume.
    # Growing BNPL industry validates the product category and drives
    # incremental PayPal transactions from price-sensitive consumers.
    ("BNPL industry volume YoY",         22.0, "% YoY",   10,  20,  35, True,
     "Pay Later segment growth; high-engagement product driving checkout frequency"),
]
WEIGHTS = [0.25, 0.20, 0.15, 0.15, 0.15, 0.10]

# ── STRUCTURAL RISK OVERLAY ──────────────────────────────────────────────
# Author-assessed factors beyond proxy signals. Score: -2 (severe risk) to
# +2 (strong advantage). Weighted sum = structural composite adjustment (SCA).
STRUCTURAL_FACTORS = [
    # (description, score -2..+2, weight)
    ("Apple/Google OS-native checkout displacement", -1.0, 0.40),
    ("Venmo 90M user network effect moat",            0.5, 0.20),
    ("Chriss turnaround execution (18M record)",      0.3, 0.20),
    ("$7B net cash — balance sheet strength",         0.3, 0.10),
    ("US fintech regulatory tailwind",                0.2, 0.10),
]


FLOOR_DATA = {
    "trough_year":        2022,
    "trough_price":       63.0,
    "cum_fcf_per_share":  12.0,
    "debt_delta":         -2.7,     # +ve = debt grew (EPP lower); -ve = improved
    "structural_delta":   -10.0,  # +ve = fundamentals improved; -ve = weaker today
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
sca           = sum(s * w for _, s, w in STRUCTURAL_FACTORS)
adj_composite = proxy_composite + sca
proxy_probs     = softmax_probs(proxy_composite)
proxy_ev        = expected_price(proxy_probs)

market_target_ev  = CURRENT_PRICE * ((1 + REQUIRED_RETURN) ** HORIZON_YEARS)
mkt_composite, mkt_probs = market_implied_composite(market_target_ev)
mkt_ev = expected_price(mkt_probs) if mkt_probs else market_target_ev

blended_tr, curr_rev, tr_prem, rev_per_pp, mix_upside = take_rate_economics()

print()
print("═" * W)
print("  PYPL SIGNAL MODEL  —  proxy vs. market-implied probability")
print("═" * W)

# Take rate decomposition
print(f"\n  TAKE RATE DECOMPOSITION  (the entire Chriss thesis in one table)")
print("  " + "─" * (W-2))
print(f"  Total TPV (FY2025E):                         ${TOTAL_TPV_T:.2f}T")
print(f"  Branded checkout mix:                        {BRANDED_MIX_PCT}%  (take rate {BRANDED_TAKE_RATE:.2f}%)")
print(f"  Unbranded / Braintree mix:                   {100-BRANDED_MIX_PCT}%  (take rate {UNBRANDED_TAKE_RATE:.2f}%)")
print(f"  Blended take rate (current):                 {blended_tr:.3f}%")
print(f"  Transaction revenue (take rate component):   ${curr_rev:.1f}B / yr  (excl. BNPL interest, subs)")
print(f"  Take rate premium branded vs unbranded:      {tr_prem:.2f}pp")
print(f"  ─────────────────────────────────────────────────────")
print(f"  Revenue uplift per 1pp branded mix gain:     ${rev_per_pp:.2f}B / yr  ← the leverage")
print(f"  Peak branded mix was {PEAK_BRANDED_MIX}% (FY2019).")
print(f"  Full recovery to {PEAK_BRANDED_MIX}% branded mix → +${mix_upside:.1f}B annual revenue uplift")
print(f"  → This requires NO macro tailwind. It is 100% an execution decision:  ")
print(f"    stop signing low-margin Braintree deals; re-win SMB checkout share.")

# Signal scorecard
print(f"\n  PROXY SIGNAL SCORECARD")
print(f"  {'Signal':<38}{'Value':>9}  Wt   Score")
print("  " + "─" * (W-2))
for name, val, unit, s, w, rt in scored:
    bar = "█" * s + "░" * (4 - s)
    fmt = f"{val:>+7.2f}" if unit == "pp YoY" else f"{val:>+7.1f}"
    print(f"  {name:<38}{fmt}{unit[0]}  {w*100:.0f}%  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:   {proxy_composite:.2f} / 4.00")
if mkt_composite:
    print(f"  Market composite:  {mkt_composite:.2f} / 4.00  "
          f"(back-solved from ${CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% reqd return)")
    gap = proxy_composite - mkt_composite
    print(f"  Gap (proxy − mkt): {gap:+.2f}  ← structural disruption discount (Apple Pay / AI wallets)")

# Valuation context
print(f"\n  VALUATION CONTEXT")
print("  " + "─" * (W-2))
fy25_eps = 4.70
print(f"  FY2025E non-GAAP EPS:        ~${fy25_eps:.2f}  (buybacks + cost cuts, not revenue growth)")
print(f"  Forward P/E:                  {CURRENT_PRICE/fy25_eps:.1f}x  (sector range: 13-26x)")
print(f"  FY2021 peak price / EPS:      $309 / $4.60  =  67x  (reset to 17x = ~75% de-rating)")
print(f"  Active accounts:              ~432M  (vs 426M FY2021 peak; essentially flat 4 years)")
print(f"  TPV growth FY2025E:           ~+7%  (vs 33% in FY2021)")
print(f"  Share buybacks (FY2024):      ~$5B  (EPS supported; not organic growth)")
print(f"  Net cash:                     ~$7B  (strong balance sheet; enables buyback program)")
print(f"  → At $78, market is pricing PYPL as a mature utility processor, not a fintech platform.")
print(f"    Re-rating to 20-21x requires evidence of organic revenue re-acceleration.")

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
print(f"  \u26a0  EPP < CPI-adj trough: OS-level displacement (Apple Pay/Google Pay) is structural.")
print(f"          Take rate compression is permanent, not cyclical.")
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

  Complete framework gap table:
    ORCL gap = +2.16  (proxies XBULL; market prices delivery/concentration risk)
    AVGO gap = +1.41  (proxies bullish; AI flow-through uncertainty)
    MSFT gap = +1.29  (proxies bullish; Copilot margin expansion uncertainty)
    SAP  gap = +0.91  (proxies constructive; Joule unmonetised)
    XTB  gap = +0.46  (justified volatility discount on cyclical revenue)
    RCL  gap = +0.36  (debt + capacity risk discount)
    COIN gap = +0.29  (approximately fairly priced; thesis is BTC price)
    PYPL gap = {gap:+.2f}  ← structural disruption discount beyond what proxies capture
    CAT  gap = -0.24  (market priced ahead of confirmed recovery)
    NKE  gap = -0.12  (market pricing unconfirmed turnaround hope)

  WHY THE GAP EXISTS — AND WHAT TYPE OF DISCOUNT IT IS:

    Unlike ORCL/AVGO/MSFT (delivery uncertainty on confirmed demand),
    PYPL's market discount is STRUCTURAL — the market prices a risk that
    NONE of the six proxy signals can measure:

    THE APPLE PAY / AI WALLET DISPLACEMENT RISK:
    Apple Pay is accepted at 90%+ of US contactless terminals. Apple
    Intelligence (iOS 18+) allows Siri to complete purchases natively,
    bypassing the PayPal checkout button entirely for Apple device users
    (~57% of US smartphone market). Every iOS update makes the
    PayPal checkout button marginally more optional.

    Google Pay and BNPL integrations (Affirm, Klarna) embedded directly
    in Chrome and Android follow the same logic on Android.

    This displacement risk is:
      • Real but slow (sticky habits, merchant integration costs)
      • Not measurable in any quarterly proxy signal
      • Worth a structural 2-3x multiple discount vs a platform with no
        native OS competitor

  THE CHRISS THESIS — THREE LEGS:

    1. Take rate mix recovery (within Chriss's control):
       Slow Braintree → branded mix recovers from 46% to 50-55%
       Revenue impact: +${rev_per_pp:.2f}B per 1pp mix shift at zero volume growth
       Signal to watch: quarterly blended take rate disclosed on earnings call

    2. Venmo monetisation per user (early stage, high optionality):
       Venmo has 90M+ active users. Revenue per user ~$14/yr.
       If Chriss gets to $25/user: +$1B ARR with no new user acquisition.
       Key products: Pay with Venmo (merchant), Venmo debit card, Teen accounts.
       Signal: Venmo revenue per active account, disclosed quarterly.

    3. PayPal Ads / merchant intelligence (zero in analyst models):
       PYPL sees $1.65T of real purchase data — who bought what, when,
       for how much, across 430M accounts. This is Google/Meta-grade
       purchase intent data. A PayPal advertising platform using this
       data could command CPMs 5-8x higher than general display.
       ~$500M revenue today → $2-3B potential by FY2027 at scale.

  THE BEAR CASE IS NOT PRICED — IT'S ALREADY HAPPENED:
    The 75% decline from $309 to $78 IS the structural discount being
    applied. The market moved first. The question is whether the discount
    is appropriate, excessive, or insufficient given where execution lands.

    If Chriss delivers $6 EPS at 17x → $102 (+31% from $78). That's BASE.
    If Chriss delivers $6 EPS but branded checkout recovery triggers
    multiple re-expansion to 21x → $126 (+62% from $78). That's mid-BULL.
    The bull case doesn't require heroics — just proof that PYPL is NOT
    being structurally displaced, which a few good quarters of take rate
    stabilisation + Venmo revenue acceleration would provide.""")
print()
print("═" * W)
