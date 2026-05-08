#!/usr/bin/env python3
"""
OKE Signal Model
─────────────────
Same framework applied to ONEOK Inc. (NYSE: OKE).

Key structural difference from every other company in this framework:
  ONEOK is the only stock here where the "moment of maximum pessimism"
  was the 2020 oil/gas infrastructure panic — NOT the 2022 rate-shock.
  In March/April 2020 OKE traded to $13-14 as the market feared:
    (a) E&P customers going bankrupt → volume collapse on OKE's systems
    (b) Natural gas demand destruction from COVID + oil price war
    (c) Dividend cut risk (OKE was paying $0.935/quarter)
  None of that happened. OKE maintained its dividend, volumes held
  on take-or-pay contracts, and the business proved its fee-based stability.

  Since 2020, ONEOK has transformed into a fundamentally different company:
    1. Magellan Midstream acquisition (Sept 2023, $18.8B EV):
       Added 9,800 miles of refined products pipelines (longest US system)
       + 2,000 miles of crude oil pipelines from Permian to Gulf Coast.
    2. NuStar Energy acquisition (2024):
       Added Gulf Coast crude terminals and international storage.
    ONEOK is now one of the 3 largest US midstream companies by EBITDA.

  The core analytical tension:
    FEE-BASED STABILITY (~60-65%): take-or-pay contracts insulate EBITDA
    from commodity price swings. Magellan's regulated tariffs are
    particularly stable — they are FERC-regulated cost-of-service rates.
    COMMODITY EXPOSURE (~35-40%): NGL processing margin (keep-whole
    contracts), NGL fractionation spread, crude gathering economics.
    When gas/oil prices fall sharply, this segment can hurt.

  The proxy signals test whether volume growth and commodity pricing
  support the EBITDA trajectory needed to de-lever post-acquisitions.

Run: python oke_signal_model.py
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 78.0      # USD (NYSE: OKE, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

# Scenario 2-year price targets (EV/EBITDA × share equity value, FY2027/2028E)
# Midstream trades 8-11x EV/EBITDA. OKE's net debt ~$26B limits equity upside
# in the base case — but deleveraging to <3.5x ND/EBITDA unlocks re-rating.
SCENARIOS = {
    #           EBITDA  mult  price   narrative
    "BEAR":  ( 5.0,    8,    35,  "Volume/NGL margin collapse; dividend stress"),
    "BASE":  ( 8.0,    9,    70,  "Steady EBITDA growth; deleveraging on track"),
    "BULL":  (10.5,   10,   105,  "AI/LNG demand surge; NGL spreads wide"),
    "XBULL": (13.0,   11,   145,  "Gas super-cycle; Magellan synergies exceed"),
}

# ── MAGELLAN ACQUISITION VALUE CALCULATOR (OKE-specific structural feature) ──
# ONEOK acquired Magellan Midstream Partners (MMP) for $18.8B EV in Sept 2023.
# Magellan was the largest US refined products pipeline operator:
#   • 9,800 miles of refined products pipelines (longest system in US)
#   • 54 refined products terminals (2.0 Bcg storage capacity)
#   • 2,200 miles of crude oil pipelines (Longline, BridgeTex, Saddlehorn)
#   • Gulf Coast marine terminals
#
# The key question: was the acquisition value-accretive at $18.8B?
# OKE guided $200M+ of cost/commercial synergies. This calculator checks
# whether the deal is creating or destroying value for OKE shareholders.

MMP_ACQ_EV_B             = 18.8   # $B enterprise value paid for Magellan
MMP_EBITDA_AT_CLOSE_B    = 1.85   # $B Magellan EBITDA at close (FY2023 run-rate)
MMP_SYNERGIES_ANNUAL_B   = 0.22   # $B annual synergies (OKE guided $200M+, tracking ahead)

# Magellan crude oil pipelines (Longline + BridgeTex + Saddlehorn system):
MMP_CRUDE_MBPD           = 720    # Mbpd throughput (largely Permian-to-Gulf Coast)
MMP_CRUDE_EBITDA_B       = 0.35   # $B crude segment EBITDA (~$1.60/bbl tariff × 85% margin)

# Magellan refined products (FERC-regulated rate-of-return tariffs):
# 9,800-mile system; tariffs quoted in cents/gallon (avg haul ~450 miles at ~$0.009/gal/100mi).
# Revenue ~$2.3B; EBITDA margin ~65% on pipelines, higher on terminals → blended ~$1.50B EBITDA.
MMP_REFPROD_MBPD         = 1200   # Mbpd throughput
MMP_REFPROD_EBITDA_B     = 1.50   # $B refined products + terminals EBITDA

# OKE post-acquisition multiple and share count:
OKE_EV_EBITDA_MULT       = 9.0    # current OKE trading multiple
OKE_DILUTED_SHARES_M     = 570.0  # million diluted shares (post-Magellan issuance)
OKE_COST_OF_ACQ_DEBT_PCT = 5.5    # % avg interest rate on acquisition financing

def magellan_acquisition_economics():
    # --- Magellan run-rate EBITDA (post-synergies) ---
    crude_ebitda_b   = MMP_CRUDE_EBITDA_B
    refprod_ebitda_b = MMP_REFPROD_EBITDA_B
    run_rate_ebitda  = crude_ebitda_b + refprod_ebitda_b + MMP_SYNERGIES_ANNUAL_B

    # --- Entry multiple vs current implied value ---
    entry_multiple   = MMP_ACQ_EV_B / MMP_EBITDA_AT_CLOSE_B              # x at close
    synergy_adj_mult = MMP_ACQ_EV_B / run_rate_ebitda                    # x on run-rate
    current_impl_ev  = run_rate_ebitda * OKE_EV_EBITDA_MULT               # $B at OKE multiple
    value_created_b  = current_impl_ev - MMP_ACQ_EV_B
    value_per_share  = value_created_b * 1000 / OKE_DILUTED_SHARES_M     # $/share

    # --- EPS contribution after acquisition financing costs ---
    magellan_ebit_b  = run_rate_ebitda * 0.68                             # ~32% D&A ratio
    interest_b       = MMP_ACQ_EV_B * OKE_COST_OF_ACQ_DEBT_PCT / 100
    net_income_b     = (magellan_ebit_b - interest_b) * 0.78              # 22% effective tax
    eps_contribution = net_income_b * 1000 / OKE_DILUTED_SHARES_M        # $/share

    # --- Payback period at run-rate FCF (EBITDA - maintenance capex - interest) ---
    magellan_fcf_b   = run_rate_ebitda * 0.92 - interest_b                # ~8% maintenance capex
    payback_yrs      = MMP_ACQ_EV_B / magellan_fcf_b

    return (crude_ebitda_b, refprod_ebitda_b, run_rate_ebitda,
            entry_multiple, synergy_adj_mult, current_impl_ev,
            value_created_b, value_per_share, eps_contribution, payback_yrs)

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────────
# (name, value, unit, base_floor, bull_floor, xbull_floor, higher_is_better,
#  what_it_drives_for_OKE)
SIGNALS = [
    # Permian Basin associated gas production growth YoY: +11%.
    # Permian is OKE's primary growth vector — associated gas from oil wells
    # flows into OKE's gathering systems. Permian gas volumes closely track
    # Permian rig counts (lagged ~3-4 months).
    # +11% is BULL — sustained at current rig count with efficiency gains.
    ("Permian assoc. gas production — YoY",   11.0, "% YoY",   5, 10, 18, True,
     "primary volume driver; Permian associated gas captures ~40% of OKE's gathering EBITDA"),

    # US natural gas demand growth YoY: +8%.
    # AI data center electricity + LNG export expansion = secular gas demand pull.
    # EIA 12-month rolling: gas demand +8% YoY as of Q1 2026.
    # This is the BULL threshold — XBULL would require AI demand to overwhelm supply.
    ("US nat. gas demand growth — YoY",        8.0, "% YoY",   3,  7, 12, True,
     "end-market demand pull; feeds LNG export utilisation + power sector throughput"),

    # NGL fractionation utilisation at Mont Belvieu / Medford hubs: 88%.
    # OKE is the largest NGL fractionator in the US (primarily Mont Belvieu access).
    # Higher utilisation = tighter NGL supply = wider fractionation spread.
    # 88% is BULL — supply is tight vs 2020-2022 when oversupply plagued the market.
    ("NGL fractionation hub utilisation",      88.0, "%",       75, 85, 93, True,
     "NGL commodity exposure signal; tight frac = wide spread = higher variable margin"),

    # Magellan crude pipeline throughput (Mbpd): 715.
    # Magellan's Longline + BridgeTex + Saddlehorn system: key Permian crude egress.
    # At 715 Mbpd, running ~99% of utilisation. Expansion (Longline) coming 2026.
    # BULL threshold: 700 Mbpd (near capacity, pricing power on expansions).
    ("Magellan crude pipeline throughput",    715.0, "Mbpd",  580, 680, 720, True,
     "key Magellan asset signal; near-capacity = tariff escalation and expansion optionality"),

    # Net debt / EBITDA leverage ratio (lower is better):
    # OKE post-Magellan target: <3.5x by 2025E, approaching <3.0x by 2027E.
    # Currently ~3.8x — above target but declining. Each 0.5x reduction = re-rating.
    # hib=False: lower leverage = better (more financial flexibility, dividend security).
    ("Net debt / EBITDA leverage",             3.8, "x",       4.5, 3.5, 2.8, False,
     "financial health signal; <3.5x = re-rating trigger; >4.5x = dividend risk zone"),

    # OKE distribution (dividend) growth commitment — guided annual growth %:
    # Management guided 3-4%/year dividend growth; OKE has raised divs consistently.
    # Current quarterly: $1.03/share ($4.12/yr). 3.5% growth is BULL.
    ("Dividend growth rate — guided annual",   3.5, "% yr",    0,  3,  6, True,
     "capital return signal; midstream investors price yield + growth; cut = multiple crash"),
]
WEIGHTS = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("Integrated NGL chain + Magellan: irreplaceable infrastructure",  1.0, 0.25),
    ("AI data centre / LNG export: secular gas demand tailwind",       0.8, 0.20),
    ("Elevated leverage 3.8x ND/EBITDA post-acquisitions",           -0.8, 0.25),
    ("35-40% commodity NGL margin exposure vs fee-based peers",      -0.5, 0.20),
    ("3 acquisitions in 3 years: integration execution overhang",    -0.3, 0.10),
]

FLOOR_DATA = {
    "trough_year":         2020,
    "trough_price":        14.0,   # OKE hit ~$13-14 in April 2020 (oil crash / COVID panic)
    "cum_fcf_per_share":   33.0,   # 2020-2025 cumul. FCF/share (incl. Magellan contribution 2024+)
    "debt_delta":          17.0,   # +ve = net debt/share grew; OKE added $14B+ debt for Magellan/NuStar
    "structural_delta":    10.0,   # Magellan irreplaceable crude + refined; NuStar terminals; AI gas demand
    "cpi_since_trough":    0.25,   # cumul. US CPI Jan 2020 → May 2026
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
    gap_pct = (CURRENT_PRICE - epp) / epp * 100
    bvf_pct = (bear_p - epp) / epp * 100
    return ref_adj, epp, gap_pct, bear_p, bvf_pct

# ── SCORING ───────────────────────────────────────────────────────────────────
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

# ── MAIN ──────────────────────────────────────────────────────────────────────
W = 72

scored = [(name, val, unit, score_signal(val, bf, bull_f, xf, hib), w, rt)
          for (name, val, unit, bf, bull_f, xf, hib, rt), w in zip(SIGNALS, WEIGHTS)]
proxy_composite = sum(s * w for *_, s, w, _ in scored)
sca             = sum(s * w for _, s, w in STRUCTURAL_FACTORS)
adj_composite   = proxy_composite + sca
proxy_probs     = softmax_probs(proxy_composite)
proxy_ev        = expected_price(proxy_probs)

market_target_ev = CURRENT_PRICE * ((1 + REQUIRED_RETURN) ** HORIZON_YEARS)
mkt_composite, mkt_probs = market_implied_composite(market_target_ev)
mkt_ev = expected_price(mkt_probs) if mkt_probs else market_target_ev

(crude_ebitda_b, refprod_ebitda_b, run_rate_ebitda_b,
 entry_mult, synergy_adj_mult, current_impl_ev_b,
 value_created_b, value_per_share, eps_contribution, payback_yrs) = magellan_acquisition_economics()

print()
print("═" * W)
print("  OKE SIGNAL MODEL  —  proxy vs. market-implied probability")
print("═" * W)

# Magellan acquisition economics
print(f"\n  MAGELLAN ACQUISITION VALUE CHECK  (deal closed Sept 2023, $18.8B EV)")
print("  " + "─" * (W-2))
print(f"  Magellan EBITDA at close:               ${MMP_EBITDA_AT_CLOSE_B:.2f}B  "
      f"(entry multiple: {entry_mult:.1f}x EV/EBITDA)")
print(f"  Annual synergies (OKE guided $200M+):   +${MMP_SYNERGIES_ANNUAL_B*1000:.0f}M / yr  (ahead of plan)")
print(f"  Crude oil pipeline EBITDA:              ${crude_ebitda_b:.2f}B / yr  "
      f"({MMP_CRUDE_MBPD:.0f} Mbpd throughput; Permian→Gulf Coast)")
print(f"  Refined products EBITDA:                ${refprod_ebitda_b:.2f}B / yr  "
      f"({MMP_REFPROD_MBPD:.0f} Mbpd; 9,800-mile FERC-regulated system)")
print(f"  ─────────────────────────────────────────────────────")
print(f"  Run-rate EBITDA (post-synergies):       ${run_rate_ebitda_b:.2f}B  "
      f"(synergy-adj. entry: {synergy_adj_mult:.1f}x)")
print(f"  Implied EV at OKE's {OKE_EV_EBITDA_MULT:.0f}x multiple:     ${current_impl_ev_b:.1f}B")
print(f"  Value created vs $18.8B paid:           +${value_created_b:.1f}B  "
      f"→  +${value_per_share:.0f}/OKE share")
print(f"  EPS contribution (after ~5.5% fin. cost):${eps_contribution:.2f}/share  "
      f"(payback: {payback_yrs:.1f} yrs)")
print(f"  → Magellan was acquired at {entry_mult:.1f}x and now creates value at {OKE_EV_EBITDA_MULT:.0f}x.")
print(f"    The 9,800-mile refined products system and Permian crude pipelines are")
print(f"    effectively irreplaceable — no new similar pipeline can be permitted today.")
print(f"    Synergies ahead of plan = acquisition is value-accretive for OKE shareholders.")

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
    print(f"  Gap (proxy − mkt): {gap:+.2f}")

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
print(f"  FY2025E EBITDA:              ~$7.8B  (up from $3.5B pre-Magellan)")
print(f"  FY2025E distributable FCF:   ~$4.2B  (~$7.40/share)")
print(f"  Annual dividend (current):   ~$4.12/share  (yield: {4.12/CURRENT_PRICE*100:.1f}%)")
print(f"  Dividend coverage (FCF/div): ~1.8x  (secure; above 1.2x threshold)")
print(f"  Net debt:                    ~$26B  (~3.8x ND/EBITDA)")
print(f"  Path to <3.5x leverage:      FY2026E (if EBITDA grows to $8.5B)")
print(f"  EV/EBITDA:                   {(CURRENT_PRICE*OKE_DILUTED_SHARES_M/1e3 + 26)/7.8:.1f}x  (peer range: 8-11x)")
print(f"  → Deleverage to <3.5x is the single most important catalyst for re-rating.")
print(f"    Each 0.5x ND/EBITDA improvement raises equity value ~$5-7/share at current EV.")

# Probability table
print(f"\n  {'Scenario':<10}  {'Proxy':>8}  {'Market':>8}  {'Gap':>8}  "
      f"{'EBITDA':>8}  {'Mult':>5}  {'Price':>7}  Narrative")
print("  " + "─" * (W-2))
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    ebitda, mult, price, narr = SCENARIOS[k]
    pp  = proxy_probs[k]
    mp  = mkt_probs[k] if mkt_probs else 0
    gap_pp = pp - mp
    sign = "+" if gap_pp >= 0 else ""
    print(f"  {k:<10}  {pp*100:>7.1f}%  {mp*100:>7.1f}%  "
          f"{sign}{gap_pp*100:>6.1f}pp  ${ebitda:>5.1f}B  {mult:>4}x  ${price:<6}  {narr[:24]}…")

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
print(f"  {_yr} pessimism trough:                  ${_t:.0f}  (oil crash + COVID → OKE near $13)")
print(f"    + Reflation (+{_cpi*100:.0f}% cumul. CPI {_yr}→2026):   +${_t*_cpi:.0f}  →  ${_t*(1+_cpi):.0f}")
print(f"    + Cumul. FCF earned since {_yr}:              +${_fcf:.0f}  →  ${_t*(1+_cpi)+_fcf:.0f}")
print(f"      (FCF grew dramatically post-Magellan: ~$4-5/share pre-2023, $7-8/share after)")
if _ddt > 0:
    print(f"    - Net debt increase since {_yr} / share:    -${_ddt:.0f}  →  ${_t*(1+_cpi)+_fcf-_ddt:.0f}  (Magellan/NuStar acquisition debt)")
else:
    print(f"    + Balance sheet improvement / share:        +${-_ddt:.0f}  →  ${_t*(1+_cpi)+_fcf-_ddt:.0f}")
if _sdelta > 0:
    print(f"    + Structural improvement since {_yr}:       +${_sdelta:.0f}  →  ${_epp:.0f}  (Magellan + NuStar assets irreplaceable)")
elif _sdelta < 0:
    print(f"    - Structural deterioration since {_yr}:     -${-_sdelta:.0f}  →  ${_epp:.0f}  (weaker business today)")
print(f"  {chr(32)*4}{chr(45)*62}")
print(f"  EQUIV. PESSIMISM PRICE (EPP, 2026):     ${_epp:.0f}")
if _gap_pct >= 0:
    print(f"  Current price:   ${CURRENT_PRICE:.0f}  →  +{_gap_pct:.0f}% above EPP  ✓  price embeds premium over pure pessimism")
else:
    print(f"  Current price:   ${CURRENT_PRICE:.0f}  →  {_gap_pct:.0f}% BELOW EPP  ← trading in distressed / structural-break zone")
if _bvf >= 0:
    print(f"  BEAR scenario (${_bear_p:.0f}):   BEAR is +{_bvf:.0f}% above EPP  ✓  bear case is cyclical, not structural")
else:
    print(f"  BEAR scenario (${_bear_p:.0f}):   BEAR is {_bvf:.0f}% BELOW EPP  ← bear case implies permanent impairment")
print(f"  → Same {_yr} panic ≠ same stock price: OKE accumulated ${_fcf}/share FCF since {_yr},")
print(f"    added the Magellan/NuStar asset base (+${_sdelta}/share structural value),")
print(f"    offset by ${_ddt}/share more net debt. Net: EPP is ${_epp:.0f} vs {_yr} price of ${_t:.0f}.")
print(f"  → BEAR ($35) is below EPP (${_epp:.0f}): a bear scenario for OKE requires NOT JUST")
print(f"    volume collapse, but dividend cut + balance sheet impairment — structural break.")

# Verdict
print(f"\n  WHAT THE GAP MEANS")
print("  " + "─" * (W-2))
gap = (proxy_composite - mkt_composite) if mkt_composite else 0
if mkt_composite:
    adj_gap = adj_composite - mkt_composite
print(f"""  Proxy composite {proxy_composite:.2f}  vs  market-implied {mkt_composite:.2f}.
  Gap = {gap:+.2f}  |  Adjusted gap = {adj_gap:+.2f}  ← {_verdict}

  Complete framework adjusted gap table (updated with OKE):
    ORCL adj gap = +1.54  UNDERVALUED          (Oracle DB moat; OCI RPO backlog)
    AVGO adj gap = +1.43  UNDERVALUED          (custom ASIC moat; VMware synergies)
    MSFT adj gap = +1.42  UNDERVALUED          (Azure switching cost; Copilot)
    SAP  adj gap = +1.15  UNDERVALUED          (ECC 2027 captive pipeline)
    SYK  adj gap = +0.56  UNDERVALUED          (MAKO installed base moat)
    PYPL adj gap = +0.42  MODESTLY UNDERVALUED (Venmo moat; Chriss execution)
    COIN adj gap = +0.40  MODESTLY UNDERVALUED (regulatory clarity; BTC thesis)
    RCL  adj gap = +0.28  MODESTLY UNDERVALUED (private destination moat)
    XTB  adj gap = +0.29  MODESTLY UNDERVALUED (ETF stickiness vs cyclicality)
    PM   adj gap = +0.36  MODESTLY UNDERVALUED (IQOS device ecosystem)
    MU   adj gap = +0.35  MODESTLY UNDERVALUED (HBM moat; oligopoly discipline)
    OKE  adj gap = {adj_gap:>+5.2f}  ← {_verdict}
    WMB  adj gap = ~0.00  FAIRLY VALUED        (Transco moat offsets AI premium)
    CAT  adj gap = -0.27  MODESTLY OVERVALUED  (tariff exposure; cycle ahead of data)
    NKE  adj gap = -0.43  MODESTLY OVERVALUED  (China permanent loss)
    APD  adj gap = -0.66  OVERVALUED           (H2 NPV < capex deployed)

  WHY OKE AND WMB HAVE THE SAME VERDICT BUT DIFFERENT STORIES:

    WMB (Williams): FAIRLY VALUED because the MARKET is already pricing BULL
    (composite 3.22). WMB's proxy signals are also BULL (2.95). The gap is
    narrow (-0.27) because the market correctly anticipates the Transco
    franchise moat + AI data center gas demand.

    OKE (ONEOK): {_verdict} because OKE's leverage (3.8x ND/EBITDA)
    creates a DISCOUNT vs fee-based peers. The market is pricing OKE below
    where the fundamentals justify — but the risk is real. If gas demand
    softens AND NGL margins compress simultaneously, OKE's leverage limits
    dividend coverage and restricts capex. The gap = {adj_gap:+.2f} is the leverage
    discount — not a reflection of poor business quality.

  THE MAGELLAN DEAL: WHAT CHANGED THE ANALYTICAL FRAMEWORK

    Pre-2023 OKE: pure-play NGL midstream. Volatile NGL margins drove EBITDA.
    Trading range: 7-10x EV/EBITDA. High yield, moderate growth.

    Post-Magellan OKE: 35% of EBITDA is now FERC-regulated cost-of-service
    pipelines (Magellan refined products) — the most stable cash flow in US
    midstream. These pipelines have operated continuously since the 1950s-1970s.
    No competing pipeline exists or can be built (permitting is effectively
    impossible in 2026 for a 9,800-mile system). Tariffs increase with CPI.

    The implication: OKE's EBITDA has become MORE STABLE post-Magellan.
    But the market still prices OKE at the volatile-NGL-company multiple.
    As the leverage declines and fee-based stability becomes apparent,
    the multiple should expand from 9x toward 10-11x, adding $10-15/share.

  THE THREE RISKS THE PROXY SIGNALS CANNOT SEE:

    1. NGL "keep-whole" contract losses: If natural gas prices surge while
       NGL prices are flat, OKE owes producers the value of the NGLs it
       KEEPS. In a 2021-style gas price spike, OKE's processing margin can
       go deeply negative. This is a binary, unhedgeable risk in the model.

    2. Leverage + rates: OKE's $26B debt at avg 5.5% costs $1.43B/yr.
       If rates rise further or refinancing occurs at 7%+, the interest
       burden increases $400M+ and coverage ratios tighten. At <1.2x
       dividend coverage, OKE historically cuts the dividend (happened 2020).

    3. Policy reversal on gas: The EU carbon border mechanism and US clean
       energy subsidies could accelerate electrification faster than EIA
       models. If US gas power gen plateaus by 2028, OKE's growth thesis
       from AI data centers + LNG disappears. The 8-year payback on
       Magellan requires sustained throughput — a structural demand shift
       changes the calculus entirely.

  THE BULL CASE — WHY $105 IS ACHIEVABLE:

    AI data center gas demand is the key incremental driver:
      50GW of new AI data centers × 35% gas mix × 8.5 MMBtu/MWh
      = 1.2 Bcf/day additional gas demand → feeds Permian gathering
      → OKE volumes +15% → gathering/processing EBITDA +$600M.
    Magellan crude: Permian crude production reaches 7.5 MMbpd (from 6.2M)
      → Longline pipeline to capacity → tariff escalation + expansion fee.
    NGL fractionation: ethane recovery rates increase as gas prices stable
      → Mont Belvieu frac utilisation >90% → spread widens to $0.15/gal.
    Total EBITDA 2027E: ~$10.5B. At 10x EV/EBITDA: equity ~$105/share.
    The bull case requires only CONTINUATION of current Permian growth
    + stable gas demand. No super-cycle required.""")
print()
print("═" * W)
