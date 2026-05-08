#!/usr/bin/env python3
"""
PM Signal Model
──────────────────
Same framework applied to Philip Morris International Inc. (NYSE: PM).

Key structural difference from the other companies in this framework:
  PM is mid-way through the most consequential transformation in consumer
  staples: from a combustible tobacco company to a "smoke-free" company.
  The transformation is not aspirational — it is already in the P&L:
    • IQOS: 40M+ registered users globally; 52%+ of gross profit
    • ZYN: 700M+ tins shipped in FY2024; dominant US oral nicotine

  The core analytical tension:
    COMBUSTIBLES: structurally declining (-4-5%/yr volumes), but generate
    ~50% of gross profit and are the highest-margin cash cow in consumer
    staples. Each pack of cigarettes carries ~65-70% gross margin.
    SMOKE-FREE: volumes and revenue growing 15-20%/yr; higher GM% than cigs;
    device ecosystem creates switching costs; regulatory authorization reduces
    policy risk vs unregulated alternatives.

  The proxy signals test whether the transformation is on track.
  The structural overlay assesses whether regulatory, ESG, and long-run
  category risks justify a discount vs the proxy data suggests.

Run: python pm_signal_model.py
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 175.0     # USD (NYSE: PM, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

# Scenario 2-year price targets (non-GAAP EPS × exit P/E, FY2027/FY2028E)
# PM's FY2025E non-GAAP EPS: ~$7.50. Base growth: 8-12%/yr (smoke-free mix shift).
# Exit multiples: 13-25x; range reflects whether market values PM as
# declining tobacco (-→ 13x) or growing smoke-free platform (→ 22-25x).
SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  ( 7.0,   13,    91,  "Regulatory setback; IQOS stall; ZYN FDA issue"),
    "BASE":  ( 9.0,   18,   162,  "Steady transformation; ZYN 50% share; IQOS 45M"),
    "BULL":  (11.5,   22,   253,  "IQOS 55M users; ZYN US #1; multiple re-rates"),
    "XBULL": (14.0,   25,   350,  "Full transformation; PM = smoke-free standard globally"),
}

# ── IQOS USER ECONOMICS CALCULATOR (PM-specific structural feature) ───────
# IQOS (I Quit Ordinary Smoking) is PM's heated tobacco system.
# Each IQOS device costs ~$80-120 (one-time investment by consumer).
# Heated Tobacco Units (HTUs: HEETS, Terea, Levia) generate recurring revenue.
#
# The transformation economics: switching a cigarette smoker to IQOS
# increases PM's revenue and gross profit per user because:
#   (1) HTU net revenue/stick is higher than cigarette net revenue/stick
#   (2) IQOS device revenue is incremental (combustibles have no device)
#   (3) HTU gross margin > combustible gross margin in most markets
#
# ZYN (Swedish Match): oral nicotine pouches — no tobacco leaf, no smoke.
# Fastest-growing nicotine category in the US; PM acquired Swedish Match in 2022.

IQOS_REGISTERED_USERS_M      = 40.0    # registered IQOS users globally (millions)
HTU_ANNUAL_REV_PER_USER_USD   = 280     # net revenue/yr per IQOS user (HTU consumption)
HTU_GROSS_MARGIN              = 0.70    # gross margin on HTUs
COMBUSTIBLE_REV_PER_USER_USD  = 190     # net revenue/yr per cigarette smoker (PM mkts avg)
COMBUSTIBLE_GROSS_MARGIN      = 0.65    # gross margin on combustibles
IQOS_DEVICE_ASP               = 95      # average device selling price ($)
IQOS_DEVICE_REPLACE_YRS       = 3       # device replacement cycle (years)

ZYN_US_SHIPMENTS_M_TINS       = 700     # tins shipped FY2024 estimate (millions)
ZYN_NET_REV_PER_TIN           = 3.80    # net revenue to PM per tin (after trade margin)
ZYN_GROSS_MARGIN              = 0.60    # gross margin on oral nicotine
ZYN_GROWTH_YOY                = 0.40    # YoY volume growth

def iqos_economics():
    # Annual revenue uplift per converted IQOS user vs cigarette smoker
    rev_uplift_per_user  = HTU_ANNUAL_REV_PER_USER_USD - COMBUSTIBLE_REV_PER_USER_USD
    # Device revenue (annualised over replacement cycle)
    device_rev_annual    = IQOS_DEVICE_ASP / IQOS_DEVICE_REPLACE_YRS
    # Gross profit per user comparison
    iqos_gp_per_user     = HTU_ANNUAL_REV_PER_USER_USD * HTU_GROSS_MARGIN + device_rev_annual
    comb_gp_per_user     = COMBUSTIBLE_REV_PER_USER_USD * COMBUSTIBLE_GROSS_MARGIN
    gp_uplift_per_user   = iqos_gp_per_user - comb_gp_per_user
    # Portfolio-level impact
    total_rev_uplift_b   = IQOS_REGISTERED_USERS_M * rev_uplift_per_user / 1000   # $B
    total_gp_uplift_b    = IQOS_REGISTERED_USERS_M * gp_uplift_per_user  / 1000   # $B
    # ZYN US revenue
    zyn_rev_b            = ZYN_US_SHIPMENTS_M_TINS * ZYN_NET_REV_PER_TIN / 1000  # $B
    zyn_gp_b             = zyn_rev_b * ZYN_GROSS_MARGIN
    # 2-year forward (15% IQOS user growth + 40% ZYN volume growth)
    future_iqos_m        = IQOS_REGISTERED_USERS_M * (1.15 ** 2)
    future_zyn_rev_b     = zyn_rev_b * (1 + ZYN_GROWTH_YOY) ** 2
    return (rev_uplift_per_user, device_rev_annual, gp_uplift_per_user,
            total_rev_uplift_b, total_gp_uplift_b,
            zyn_rev_b, zyn_gp_b, future_iqos_m, future_zyn_rev_b)

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
# (name, value, unit, base_floor, bull_floor, xbull_floor, higher_is_better,
#  what_it_drives_for_PM)
SIGNALS = [
    # IQOS registered user base YoY growth: +15%.
    # PM discloses IQOS user metrics quarterly. This is the primary transformation KPI.
    # User growth leads HTU volume with ~1 quarter lag as new users ramp consumption.
    # +15% is BULL — sustained at scale (40M base). Would need +25% for XBULL.
    ("IQOS registered user growth — YoY",   15.0, "% YoY",   8, 15, 25, True,
     "primary transformation KPI; user growth leads HTU volume 1Q; device ecosystem lock-in"),

    # ZYN US shipment volume YoY: +40%.
    # The fastest-growing nicotine category in the US market.
    # PM reports ZYN volumes quarterly; FDA shipment data provides monthly check.
    # +40% is BULL — sustaining breakneck growth vs 2023 shortages resolved.
    ("ZYN US shipment volume — YoY",        40.0, "% YoY",  15, 35, 55, True,
     "US oral nicotine category leader; highest GM nicotine product in PM portfolio"),

    # Smoke-free gross profit mix: 52%.
    # The most important transformation metric: SF% of total gross profit.
    # Crossing 50% is the inflection point for multiple re-rating.
    # At 52%, PM is now majority smoke-free on gross profit — a structural milestone.
    ("Smoke-free gross profit mix",         52.0, "%",       40, 50, 65, True,
     "transformation milestone: crossing 50% SF gross profit = multiple re-rating trigger"),

    # HTU (Heated Tobacco Unit) volume YoY: +18%.
    # HTU volumes (HEETS, Terea) are PM's own smoke-free consumable.
    # Volume growth validates device adoption → consumable conversion is holding.
    # +18% is BULL — consistent with user base growth.
    ("HTU (heated tobacco unit) vol — YoY", 18.0, "% YoY",   8, 15, 25, True,
     "smoke-free consumable volumes; HTU volume growth directly drives smoke-free revenue"),

    # Combustible cigarette volume decline rate: -4.0% YoY.
    # Slower decline = better (more combustible cash flow to fund transformation).
    # PM's combustibles are concentrated in premium markets (EU, Japan, ASEAN).
    # At -4%: in line with structural decline; not accelerating.
    ("Combustible volume decline",          -4.0, "% YoY",  -6, -3, -1, True,
     "combustible cash flow anchor; slower decline = longer runway for transformation"),

    # IQOS regulatory authorisation depth: 3.2/4.
    # Scored as ordinal: 1=no auth, 2=reduced risk, 3=MRTP (US FDA), 4=full re-rating
    # FDA granted IQOS Modified Risk Tobacco Product (MRTP) authorization in 2024.
    # At 3.2: MRTP granted but not yet in multiple full markets = BULL, not XBULL.
    ("IQOS regulatory authorisation depth",  3.2, "/4",       2,  3,  4, True,
     "de-risking: MRTP authorization validates PM's science claims; leads re-rating"),
]
WEIGHTS = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("IQOS device + ecosystem user switching cost",   1.2, 0.25),
    ("Regulatory re-classification / ban risk",      -0.8, 0.25),
    ("Combustible secular terminal decline risk",    -0.5, 0.20),
    ("HTU pricing premium / excise architecture",     0.8, 0.15),
    ("Swedish Match debt ($16B acquisition)",        -0.3, 0.15),
]


FLOOR_DATA = {
    "trough_year":        2022,
    "trough_price":       82.0,
    "cum_fcf_per_share":  17.6,
    "debt_delta":         9.0,     # +ve = debt grew (EPP lower); -ve = improved
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

def market_implied_composite(target_ev, tolerance=3.0):
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

(rev_uplift, dev_rev_ann, gp_uplift, tot_rev_b, tot_gp_b,
 zyn_rev_b, zyn_gp_b, fut_iqos_m, fut_zyn_rev_b) = iqos_economics()

print()
print("═" * W)
print("  PM SIGNAL MODEL  —  proxy vs. market-implied probability")
print("═" * W)

# IQOS user economics
print(f"\n  IQOS USER ECONOMICS  (the transformation revenue engine)")
print("  " + "─" * (W-2))
print(f"  Registered IQOS users globally:         {IQOS_REGISTERED_USERS_M:.0f}M")
print(f"  HTU net revenue per user per year:       ${HTU_ANNUAL_REV_PER_USER_USD}/yr")
print(f"  Combustible revenue per smoker per yr:   ${COMBUSTIBLE_REV_PER_USER_USD}/yr")
print(f"  Revenue uplift per converted user:       +${rev_uplift}/yr")
print(f"  Device revenue (annualised):             +${dev_rev_ann:.0f}/yr  (${IQOS_DEVICE_ASP} / {IQOS_DEVICE_REPLACE_YRS}-yr cycle)")
print(f"  Gross profit uplift per converted user:  +${gp_uplift:.0f}/yr  "
      f"(HTU {HTU_GROSS_MARGIN*100:.0f}% GM vs cig {COMBUSTIBLE_GROSS_MARGIN*100:.0f}% GM)")
print(f"  ─────────────────────────────────────────────────────")
print(f"  Total portfolio revenue uplift:          +${tot_rev_b:.1f}B / yr")
print(f"  Total gross profit uplift:               +${tot_gp_b:.1f}B / yr  ← incremental vs if all smoked")
print(f"\n  ZYN US Oral Nicotine:")
print(f"  Shipments FY2024:                        {ZYN_US_SHIPMENTS_M_TINS:.0f}M tins")
print(f"  Net revenue to PM:                       ${zyn_rev_b:.2f}B / yr  (@ ${ZYN_NET_REV_PER_TIN}/tin)")
print(f"  Gross profit:                            ${zyn_gp_b:.2f}B / yr  ({ZYN_GROSS_MARGIN*100:.0f}% GM)")
print(f"\n  2-year forward (at current growth rates):")
print(f"  IQOS users (15%/yr):                     {fut_iqos_m:.1f}M")
print(f"  ZYN US revenue (40%/yr):                 ${fut_zyn_rev_b:.2f}B / yr")
print(f"  → Smoke-free GP mix reaches ~60-65%  by FY2027 — full multiple re-rating territory.")

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
    print(f"  Gap (proxy − mkt): {gap:+.2f}  ← transformation executing ahead of market pricing")

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
fy25_eps = 7.50
print(f"  FY2025E non-GAAP EPS:        ~${fy25_eps:.2f}")
print(f"  Current forward P/E:          {CURRENT_PRICE/fy25_eps:.1f}x  (prior peak: 18x; trough: 13x)")
print(f"  Smoke-free GP mix (FY2025E): ~52%  (majority milestone crossed)")
print(f"  Revenue growth (organic):     ~9-10%  (SF volume + combustible pricing)")
print(f"  Net debt / EBITDA:            ~3.2x  (post Swedish Match; declining)")
print(f"  Dividend yield:               ~3.5%  (55+ year dividend growth streak)")
print(f"  FCF conversion:               ~90%+ of net income (tobacco economics)")
print(f"  → At 18-22x, PM re-rates as 'smoke-free growth company' vs 'tobacco value trap'.")

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

  Complete framework adjusted gap table (updated):
    ORCL adj gap = +1.54  UNDERVALUED          (Oracle DB moat; OpenAI RPO)
    AVGO adj gap = +1.43  UNDERVALUED          (custom ASIC moat)
    MSFT adj gap = +1.42  UNDERVALUED          (Azure switching cost)
    SAP  adj gap = +1.15  UNDERVALUED          (ECC 2027 captive pipeline)
    SYK  adj gap = +0.56  UNDERVALUED          (MAKO installed base moat)
    PYPL adj gap = +0.42  MODESTLY UNDERVALUED (Venmo moat; Chriss execution)
    COIN adj gap = +0.40  MODESTLY UNDERVALUED (regulatory clarity)
    PM   adj gap = {adj_gap if mkt_composite else '?':>+5.2f}  ← see verdict above
    RCL  adj gap = +0.28  MODESTLY UNDERVALUED (private dest moat)
    XTB  adj gap = +0.29  MODESTLY UNDERVALUED (ETF stickiness)
    WMB  adj gap = ~0.00  FAIRLY VALUED        (Transco moat offsets AI premium)
    CAT  adj gap = -0.27  MODESTLY OVERVALUED  (tariff exposure)
    NKE  adj gap = -0.43  MODESTLY OVERVALUED  (China permanent loss)
    APD  adj gap = -0.66  OVERVALUED           (H2 NPV < capex deployed)

  WHY PM IS A UNIQUE ANALYTICAL PROBLEM IN THIS FRAMEWORK:

    Every other company in this set is in a growing category.
    PM is the only company TRANSFORMING OUT of a structurally declining one.
    This creates a DUAL VALUATION PROBLEM:
      (a) Core combustibles: mature, declining, but ENORMOUS cash generator
          ~$7.5B gross profit/yr from cigarettes. Never modelled correctly.
      (b) Smoke-free portfolio: growing 15-20%/yr, higher margins, scaling.
          Should be valued as a consumer growth company, not tobacco.
    The market blends these two in the P/E multiple. The transformation
    thesis says: as SF% crosses 60-70%, the blended multiple RE-RATES.

  THE IQOS SWITCHING COST THAT PROXY SIGNALS CAN'T CAPTURE:

    40M consumers have PURCHASED an IQOS device for $80-120.
    Unlike cigarette smokers (no capital investment), IQOS users:
    1. Have a DEVICE they're not willing to abandon
    2. Have LEARNED a consumption behaviour (heat vs combust)
    3. Are registered in PM's CRM — PM can market directly to them
    4. Face REAL SWITCHING COST vs competing heated tobacco (iQOS
       HTUs are not cross-compatible with rivals' devices)

    This is the SYK/MAKO dynamic in nicotine: install the platform,
    lock in the consumable revenue. The structural overlay captures
    this as +1.2 × 25% = +0.30 to the adjusted composite.

  THE THREE RISKS THE PROXY SIGNALS CANNOT SEE:

    1. Regulatory re-classification: FDA's MRTP authorization can be
       withdrawn or conditioned. The EU Tobacco Products Directive is
       under review. A single adverse regulatory ruling in a key market
       (Japan, Germany, Italy) removes 15-25% of IQOS revenue.
       This is NOT in any proxy signal — it's binary.

    2. Terminal combustible value: Even a successful smoke-free transition
       assumes cigarette cash flow funds the transition for 10-15 years.
       If combustible volumes decline FASTER than projected (-8% vs -4%),
       the free cash flow bridge is shorter — PM may need to raise equity
       to fund growth capex. The SCA deducts -0.5 × 20% for this risk.

    3. PM USA re-entry risk: If PM eventually re-enters the US combustible
       market (via merger with Altria), the strategic rationale and capital
       allocation become complex. PM's current premium is partly because
       investors value the simplicity of the international smoke-free story.

  THE BULL CASE — WHY $253 IS ACHIEVABLE:

    IQOS reaching 55M users (from 40M) over 2 years requires +18%/yr.
    Historically PM has grown IQOS users 20-25%/yr at this scale.
    At 55M users × $72.50 GP uplift = additional $1.1B GP vs today.
    ZYN reaching 1,000M tins/yr: ${ZYN_NET_REV_PER_TIN} × 1,000M × {ZYN_GROSS_MARGIN:.0%} GM = ${ZYN_NET_REV_PER_TIN*1000*ZYN_GROSS_MARGIN/1000:.2f}B incremental GP.
    Combined: total GP ~$18B, EPS ~$11+, re-rate to 22x = $242-253.
    The bull case requires only CONTINUATION of current execution rates.""")
print()
print("═" * W)
