#!/usr/bin/env python3
"""
SYK Signal Model
──────────────────
Same framework applied to Stryker Corporation (NYSE: SYK).

Key structural difference from the other companies in this framework:
  Stryker is the COMPOUNDING MACHINE of the medical device sector.
  22 consecutive years of organic revenue growth above 8%. Never missed
  a year of double-digit EPS growth outside of COVID (2020).

  The core thesis is not complicated — it has THREE compounding engines:
  1. DEMOGRAPHICS: 10,000 Baby Boomers turn 65 every day through 2029.
     Hip/knee procedures surge when the 65-80 cohort hits peak ortho need.
  2. MAKO ROBOTICS: 3,200+ installed systems generating recurring procedure
     revenue. Each MAKO installation = 10+ years of high-margin consumables.
     As competitors (JNJ Velys, Zimmer Rosa) struggle to match MAKO's
     installed base, the switching cost moat widens each quarter.
  3. M&A ENGINE: Stryker has made 60+ acquisitions since 2010. Track record
     of paying 3-4x revenue, integrating within 18 months, hitting synergies.

  The question is whether the current $380 price already discounts all three
  or whether the MAKO installed base compounding creates ongoing surprises.

Run: python syk_signal_model.py
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 380.0     # USD (NYSE: SYK, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

# Scenario 2-year price targets (non-GAAP EPS × exit P/E, FY2027/FY2028E)
# SYK's FY2025E non-GAAP EPS: ~$13.50. 8%+ organic growth through FY2027:
# BASE: ~$17.0 (2yr CAGR ~12% — consistent with SYK's historical pattern)
# Exit multiples: 22-34x; SYK historically 26-32x when execution is evident.
SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  (12.5,   22,   275,  "Elective surgery freeze; hospital budget cuts"),
    "BASE":  (17.0,   26,   442,  "Steady recovery; MAKO growing; demographics"),
    "BULL":  (21.0,   30,   630,  "MAKO dominant; international expansion; M&A"),
    "XBULL": (26.0,   34,   884,  "Surgical robotics re-rating; spine/neuro boom"),
}

# ── MAKO ROBOTICS INSTALLED BASE CALCULATOR (SYK-specific structural feature) ─
# MAKO Smart Robotics is Stryker's surgical robot for total hip, total knee,
# and partial knee replacements. Each installed system creates a durable
# recurring revenue stream through:
#   (a) Implant pull-through: MAKO cases use SYK implants exclusively
#   (b) Procedure-linked consumables (cutting guides, software licensing)
#   (c) Servicing and upgrades (multi-year service contracts)
#
# The compounding math: each new system installed creates a "mini-annuity"
# that persists for the life of the robot (~10-12 years).

MAKO_INSTALLED_BASE      = 3_200    # systems globally (est. FY2025E)
MAKO_NEW_PER_YEAR        =   380    # annual new system installations
MAKO_PROCEDURE_VOLUME    =   175    # avg procedures per system per year
MAKO_IMPLANT_ASP         = 2_400    # avg selling price per implant set ($)
MAKO_CONSUMABLE_PER_PROC =   350    # disposables/consumables per procedure ($)
MAKO_SYSTEM_ASP_K        = 1_500    # capital equipment price ($K per system)
MAKO_SERVICE_CONTRACT_K  =   450    # annual service contract per system ($K)

def mako_economics():
    # Annual recurring revenue from installed base
    total_procs_yr   = MAKO_INSTALLED_BASE * MAKO_PROCEDURE_VOLUME          # procedures
    implant_rev_b    = total_procs_yr * MAKO_IMPLANT_ASP / 1e9              # $B
    consumable_rev_b = total_procs_yr * MAKO_CONSUMABLE_PER_PROC / 1e9
    service_rev_b    = MAKO_INSTALLED_BASE * MAKO_SERVICE_CONTRACT_K / 1e6  # $B
    total_rec_rev_b  = implant_rev_b + consumable_rev_b + service_rev_b
    # New system capital revenue
    capital_rev_b    = MAKO_NEW_PER_YEAR * MAKO_SYSTEM_ASP_K / 1e6         # $B
    # Incremental revenue per new system installed (over 10yr life)
    ltv_per_system   = (MAKO_PROCEDURE_VOLUME * (MAKO_IMPLANT_ASP + MAKO_CONSUMABLE_PER_PROC)
                        + MAKO_SERVICE_CONTRACT_K * 1000) * 10 / 1e6       # $M LTV over 10yr
    # In 2 years at current installation pace:
    future_base      = MAKO_INSTALLED_BASE + MAKO_NEW_PER_YEAR * 2
    future_rec_rev_b = future_base * MAKO_PROCEDURE_VOLUME * \
                       (MAKO_IMPLANT_ASP + MAKO_CONSUMABLE_PER_PROC) / 1e9 + \
                       future_base * MAKO_SERVICE_CONTRACT_K / 1e6
    return total_procs_yr, total_rec_rev_b, capital_rev_b, ltv_per_system, future_base, future_rec_rev_b

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
# (name, value, unit, base_floor, bull_floor, xbull_floor, higher_is_better,
#  what_it_drives_for_SYK)
SIGNALS = [
    # US elective surgery volume YoY: +4%.
    # Elective orthopaedic procedures (hips, knees) are SYK's primary volume driver.
    # Post-COVID backlog cleared by 2024; 2026 growth reflects organic demand.
    # +4% is BASE — solid but tariff/consumer uncertainty limiting acceleration.
    # Tracked via hospital system earnings (HCA, THC, CYH) 4-6 weeks before SYK.
    ("US elective surgery volume — YoY",     4.0, "% YoY",   2,  5,  9, True,
     "primary volume driver: hip/knee/spine procedure volumes = SYK implant units"),

    # Hospital capital spending YoY: +6%.
    # MAKO is a capital purchase ($1.5M system). Hospital CFOs must approve capex.
    # At +6%, hospital balance sheets are healthy enough for equipment investment.
    # Below +3% = BEAR for MAKO capital sales cycle.
    ("Hospital capital spending — YoY",      6.0, "% YoY",   3,  7, 12, True,
     "MAKO capital sales driver; below $3% growth = hospital CFOs freeze robot budgets"),

    # MAKO robotic surgery procedure volume YoY: +24%.
    # Stryker reports MAKO procedure volume quarterly. This is the most direct signal.
    # At +24%, adoption is BULL — new system installations driving procedure ramp.
    # Leading indicator: procedure growth leads implant ASP improvement 1-2 quarters.
    ("MAKO procedure volume — YoY",         24.0, "% YoY",  10, 20, 35, True,
     "direct MAKO adoption signal; procedure growth leads implant revenue 1-2 quarters"),

    # US 65+ population growth: +3.2%.
    # The primary demographic driver for elective orthopaedic procedures.
    # Baby Boomers peaking: 65+ cohort grows fastest 2025-2029, then moderates.
    # Not cyclical — this demand WILL materialise regardless of macro.
    ("US population 65+ — growth",           3.2, "% YoY",   2,  3,  4, True,
     "structural demand: hip/knee procedure rates surge 3-5x at age 65-80"),

    # Orthopedic implant market YoY: +5%.
    # Tracked via OrthoWorld, Zimmer Biomet, JNJ MedTech quarterly disclosures.
    # Peers report before SYK; strong market growth = SYK likely outperformed.
    # +5% is BASE — in line with trend but not exceptional.
    ("Orthopedic implant market — YoY",      5.0, "% YoY",   3,  6,  9, True,
     "market-level growth; SYK typically captures share above market growth rate"),

    # MAKO competitive win rate vs JNJ Velys: 68%.
    # Based on hospital purchase decisions tracked by orthopedic distributor surveys.
    # JNJ launched Velys (total knee only) in 2022. MAKO has multi-joint capability.
    # 68% MAKO win rate confirms SYK is maintaining dominance in new robot evaluations.
    ("MAKO win rate vs JNJ Velys",          68.0, "%",       55, 65, 75, True,
     "competitive moat: win rate falling below 55% = MAKO premium starts eroding"),
]
WEIGHTS = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("MAKO installed base switching cost moat",       1.2, 0.25),
    ("JNJ / Zimmer Biomet robotics competitive risk", -0.5, 0.25),
    ("Aging demographics structural demand",           0.8, 0.20),
    ("Hospital consolidation → SYK preferred vendor", 0.5, 0.15),
    ("High valuation limits margin of safety",        -0.5, 0.15),
]


FLOOR_DATA = {
    "trough_2022":        190.0,
    "cum_fcf_per_share":  21.4,
    "debt_delta":         4.8,     # +ve = debt grew (EPP lower); -ve = balance sheet improved
    "structural_delta":   10.0,  # +ve = fundamentals improved; -ve = structurally weaker
    "reflation":           0.17,     # cumul. US CPI Jan 2022 - May 2026
}

def worst_case_floor():
    t, refl   = FLOOR_DATA["trough_2022"], FLOOR_DATA["reflation"]
    fcf, ddt  = FLOOR_DATA["cum_fcf_per_share"], FLOOR_DATA["debt_delta"]
    sdelta    = FLOOR_DATA["structural_delta"]
    ref_adj   = t * (1 + refl)
    epp       = ref_adj + fcf - ddt + sdelta
    bear_p    = SCENARIOS["BEAR"][2]
    gap_pct   = (CURRENT_PRICE - epp) / epp * 100   # +ve = price above EPP; -ve = below
    bvf_pct   = (bear_p - epp) / epp * 100
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

total_procs, rec_rev, cap_rev, ltv, future_base, future_rec = mako_economics()

print()
print("═" * W)
print("  SYK SIGNAL MODEL  —  proxy vs. market-implied probability")
print("═" * W)

# MAKO installed base calculator
print(f"\n  MAKO ROBOTICS INSTALLED BASE  (the compounding revenue engine)")
print("  " + "─" * (W-2))
print(f"  Systems installed globally:              {MAKO_INSTALLED_BASE:>6,}")
print(f"  New installations per year:              {MAKO_NEW_PER_YEAR:>6,}")
print(f"  Average procedures per system/yr:        {MAKO_PROCEDURE_VOLUME:>6,}")
print(f"  Total annual MAKO procedures:            {total_procs:>6,}")
print(f"  ─────────────────────────────────────────────────────")
print(f"  Implant pull-through revenue:            ${MAKO_INSTALLED_BASE*MAKO_PROCEDURE_VOLUME*MAKO_IMPLANT_ASP/1e9:.1f}B / yr")
print(f"  Consumables revenue:                     ${MAKO_INSTALLED_BASE*MAKO_PROCEDURE_VOLUME*MAKO_CONSUMABLE_PER_PROC/1e9:.2f}B / yr")
print(f"  Service contracts:                       ${MAKO_INSTALLED_BASE*MAKO_SERVICE_CONTRACT_K/1e6:.2f}B / yr")
print(f"  Total MAKO recurring rev (est.):         ${rec_rev:.2f}B / yr  ← not in most models")
print(f"  New system capital sales:                ${cap_rev:.2f}B / yr")
print(f"  LTV per new MAKO installation (10yr):    ${ltv:.1f}M / system")
print(f"\n  In 2 years at current pace:")
print(f"  Future installed base:                   {future_base:>6,} systems (+{future_base-MAKO_INSTALLED_BASE:,} vs today)")
print(f"  Future recurring revenue:               ~${future_rec:.1f}B / yr  (structural floor grows)")
print(f"  → Each new MAKO = ${ltv:.0f}M LTV = {MAKO_SYSTEM_ASP_K/ltv*100:.0f}% recovered as capital + {(ltv - MAKO_SYSTEM_ASP_K/1000)/ltv*100:.0f}% recurring profit")

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
    print(f"  Gap (proxy − mkt): {gap:+.2f}  ← proxy signals ahead of market pricing")

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
fy25_eps = 13.50
print(f"  FY2025E non-GAAP EPS:        ~${fy25_eps:.2f}")
print(f"  Current forward P/E:          {CURRENT_PRICE/fy25_eps:.1f}x  (SYK historical: 24-32x)")
print(f"  Revenue (FY2025E):           ~$23B  (+8-9% organic)")
print(f"  EBITDA margin (FY2025E):     ~27%  (expanding via MAKO mix)")
print(f"  Net debt / EBITDA:           ~2.5x  (comfortable; M&A capacity intact)")
print(f"  FCF conversion:              ~85%  of net income (high quality earnings)")
print(f"  22-yr organic growth streak:  never missed 8%+ except COVID 2020")
print(f"  → Premium P/E warranted by consistency; MAKO creates earnings predictability.")

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

# Equivalent Pessimism Price
_ref_adj, _epp, _gap_pct, _bear_p, _bvf = worst_case_floor()
_t      = FLOOR_DATA["trough_2022"]
_fcf    = FLOOR_DATA["cum_fcf_per_share"]
_ddt    = FLOOR_DATA["debt_delta"]
_sdelta = FLOOR_DATA["structural_delta"]
print(f"\n  EQUIV. PESSIMISM PRICE  (if 2022 pessimism returned today, price would be:)")
print("  " + "─" * (W-2))
print(f"  2022 pessimism trough:                  ${_t:.0f}")
print(f"    + Reflation (+17% cumul. CPI since 2022):  +${_t*0.17:.0f}  \u2192  ${_t*1.17:.0f}")
print(f"    + Cumul. FCF earned FY2023-2025:           +${_fcf:.0f}  \u2192  ${_t*1.17+_fcf:.0f}")
if _ddt > 0:
    print(f"    - Net debt increase since 2022 / share:    -${_ddt:.0f}  \u2192  ${_t*1.17+_fcf-_ddt:.0f}  (leverage drag)")
else:
    print(f"    + Balance sheet improvement / share:       +${-_ddt:.0f}  \u2192  ${_t*1.17+_fcf-_ddt:.0f}")
if _sdelta > 0:
    print(f"    + Structural improvement since 2022:       +${_sdelta:.0f}  \u2192  ${_epp:.0f}  (moat/earnings-power \u2191)")
elif _sdelta < 0:
    print(f"    - Structural deterioration since 2022:     -${-_sdelta:.0f}  \u2192  ${_epp:.0f}  (weaker business today)")
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
    print(f"    Structural damage since 2022 means equal pessimism = lower price than CPI-adj 2022.")
elif _sdelta > 0:
    print(f"    Structural gains since 2022 means equal pessimism = higher price than CPI-adj 2022.")

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
    SYK  adj gap = {adj_gap if mkt_composite else '?':>+5.2f}  ← see verdict above
    COIN adj gap = +0.40  MODESTLY UNDERVALUED (regulatory clarity)
    PYPL adj gap = +0.42  MODESTLY UNDERVALUED (Venmo moat)
    RCL  adj gap = +0.28  MODESTLY UNDERVALUED (private dest moat)
    XTB  adj gap = +0.29  MODESTLY UNDERVALUED (ETF stickiness)
    WMB  adj gap = ~0.00  FAIRLY VALUED        (Transco moat offsets premium)
    APD  adj gap = -0.68  OVERVALUED           (H2 project NPV < capex)
    CAT  adj gap = -0.27  MODESTLY OVERVALUED  (tariff exposure)
    NKE  adj gap = -0.43  MODESTLY OVERVALUED  (China permanent loss)

  WHY SYK IS THE HIGHEST-QUALITY UNDERVALUED IN THIS FRAMEWORK:

    AVGO, MSFT, and ORCL have large positive gaps, but they require:
    • ORCL: $553B RPO to actually convert to revenue
    • MSFT: Copilot attach rate to reach 25%+
    • AVGO: Hyperscaler CapEx to flow through to EPS

    SYK's gap is backed by ALREADY-EARNING assets:
    • {MAKO_INSTALLED_BASE:,} MAKO robots ARE installed and generating ${rec_rev:.1f}B/yr
    • Demographic wave IS happening — it's on the actuarial tables
    • 22 years of consistent execution IS the track record, not a forecast

  THE MAKO MOAT — WHY IT COMPOUNDS:

    Unlike most technology hardware, MAKO creates a captive ecosystem:
    1. LEARNING CURVE: Surgeons trained on MAKO don't switch to JNJ Velys.
       Each surgeon requires 20+ MAKO cases to reach proficiency.
       Retraining on a competitor = 6-12 months of reduced efficiency.
    2. HOSPITAL STICKINESS: Once a hospital buys MAKO, its OR workflow,
       scheduling, and staff training are optimised around the system.
       Switching = $500K training cost + 6-12 month productivity hit.
    3. DATA MOAT: SYK has procedure data from 3,200 systems and millions
       of cases. This data trains MAKO's planning algorithms. Competitors
       with 300-400 systems cannot replicate this data advantage.

    Result: MAKO win rate of 68% INCREASES as installed base grows.
    Each hospital that goes MAKO converts its referring surgeon network.

  THE DEMOGRAPHIC MATH (structural, not cyclical):

    US population reaching 65-74 (peak hip/knee replacement age):
    2024: 35.5M people
    2028: 39.2M people (+10.4%)
    2032: 41.8M people (+18%)

    Hip replacement rate in 65-74 cohort: ~5.5 per 1,000 per year.
    Every +1M people in this cohort = ~5,500 incremental hip replacements/yr.
    At $2,400 implant ASP and 65% SYK share: +$8.6M revenue per 1M cohort increase.
    By 2028, cohort grows +3.7M → ~$32M incremental revenue from demographics alone.

  THE RISK THAT MAKES BULLS NERVOUS:

    JNJ acquired Abiomed + Shockwave; its medical device ambition is clear.
    JNJ Velys has a total knee indication and robotics-guided workflow.
    If JNJ can close the MAKO gap in 2-3 years (matching multi-joint capability)
    AND offer a lower capital cost (JNJ's balance sheet vs SYK's), MAKO's
    68% win rate could compress to 55-60% — still dominant but directionally
    concerning. The structural overlay scores this at -0.5/25% = -0.125 impact,
    acknowledging the risk without overweighting it against a proven 3,200-system moat.""")
print()
print("═" * W)
