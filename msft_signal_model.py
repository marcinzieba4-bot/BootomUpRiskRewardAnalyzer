#!/usr/bin/env python3
"""
Microsoft Signal Model
────────────────────────
Same framework applied to Microsoft Corporation (NASDAQ: MSFT).

Key structural difference from the other companies in this framework:
  AI thesis is already IN the reported numbers — unlike ORCL ($553B RPO
  contracted but unconverted) or SAP (Joule unmonetised), MSFT's Copilot
  revenue is live, growing, and visible in Azure + M365 segments.
  Yet market composite is still well below proxy composite — why?

  The discount is entirely about EPS FLOW-THROUGH:
  Azure AI revenue grows 35%+, but compute cost runs ahead of revenue.
  Copilot is priced at $30/user but costs more to serve at current scale.
  Microsoft is in a deliberate 'invest now, harvest 2026-2028' posture.
  The market is pricing a growth stock that must PROVE margin expansion.

The interesting comparison to ORCL: proxy scores are nearly identical (~3.45),
but MSFT's gap is smaller (+1.26 vs +2.16) because MSFT's AI is REAL REVENUE
now — it's not concentrated in one unverified customer's backlog.

Run: python msft_signal_model.py
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 415.0     # USD (NASDAQ: MSFT, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

# Scenario 2-year price targets (non-GAAP EPS × exit P/E multiple)
# FY2025E non-GAAP EPS: ~$13.50; FY2028E range: $13 (bear) to $28 (xbull)
# Multiple range: 22-35x — MSFT rarely trades below 22x given recurring rev mix
# XBULL multiple limited to 35x: at $28 EPS and decelerating growth, 40x unwarranted
SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  (13.0,   22,   286,  "Azure slows <10%; Copilot stalls; AI margin drag"),
    "BASE":  (18.0,   27,   486,  "Azure 20-25%; Copilot 50M seats; margins recover"),
    "BULL":  (23.0,   32,   736,  "Azure 30%+; Copilot 100M+ seats; GitHub mainstream"),
    "XBULL": (28.0,   35,   980,  "Azure #2→#1; Copilot standard; AGI adjacency re-rates"),
}

# ── COPILOT MONETIZATION CALCULATOR (MSFT-specific structural feature) ───
# Microsoft 365 commercial has ~400M licensed seats globally.
# Copilot for M365 is an add-on at $30/user/month ($360/yr).
# Each percentage point of seat attach = large incremental high-margin ARR.
# This is the most important through-the-cycle earnings driver to track.

M365_COMMERCIAL_SEATS_M  = 400     # million licensed M365 commercial seats
COPILOT_PAID_SEATS_M     =  30     # M365 Copilot paid seats (million, est. Q1 FY2026)
COPILOT_MONTHLY_USD      =  30     # per user per month
GITHUB_COPILOT_SUBS_M    =   1.8   # GitHub Copilot paid subscribers (million)
GITHUB_COPILOT_ARPU_MO   =  19     # avg GitHub Copilot ARPU ($/month)

def copilot_economics():
    current_attach_pct = COPILOT_PAID_SEATS_M / M365_COMMERCIAL_SEATS_M * 100
    current_arpu_yr    = COPILOT_MONTHLY_USD * 12
    current_arr        = COPILOT_PAID_SEATS_M * 1e6 * current_arpu_yr / 1e9  # $B
    rev_per_pct_attach = M365_COMMERCIAL_SEATS_M * 1e6 * current_arpu_yr / 100 / 1e9  # $B per pp
    # Scenarios
    bull_arr   = 100e6 * current_arpu_yr / 1e9   # 100M seats
    xbull_arr  = 200e6 * current_arpu_yr / 1e9   # 200M seats (50% of base)
    github_arr = GITHUB_COPILOT_SUBS_M * 1e6 * GITHUB_COPILOT_ARPU_MO * 12 / 1e9
    return current_attach_pct, current_arr, rev_per_pct_attach, bull_arr, xbull_arr, github_arr

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
# Chosen to cover: cloud infrastructure demand (Azure), AI seat adoption,
# CapEx environment (MSFT itself invests $50B+/yr), enterprise hiring health
# (LinkedIn), developer AI adoption (GitHub), and enterprise software TAM.
#
# (name, value, unit, base_floor, bull_floor, xbull_floor, higher_is_better,
#  what_it_drives_for_MSFT)
SIGNALS = [
    # Azure / Cloud revenue YoY: +35% in Q3 FY2026.
    # MSFT reports Azure growth each quarter (% YoY, constant currency).
    # Azure is 43% of MSFT revenue and growing. AI services contribution:
    # ~13pp of the 35% growth rate is directly attributable to AI services.
    # This is MSFT's own data but is the single most important signal.
    ("Azure cloud revenue — YoY",        35.0, "% YoY",   15,  25,  35, True,
     "intelligent cloud segment (~43% of revenue); AI services = 13pp of growth"),

    # M365 Copilot paid seats: 30M.
    # Commercial add-on at $30/user/month. Converts the installed M365 base
    # into an AI monetization vehicle. 30M seats = 7.5% of the 400M addressable.
    # Threshold at 30M = XBULL marks the 'crossing the chasm' moment.
    ("M365 Copilot paid seats",          30.0, "M seats",  5,  15,  30, True,
     "direct incremental ARR on top of M365 base; $1.44B per % point of attach"),

    # Hyperscaler CapEx YoY: +77%.
    # Microsoft is BOTH a hyperscaler (investing $50B+/yr in Azure infra)
    # AND a beneficiary of other hyperscaler spend (Azure AI services).
    # High CapEx = industry demand is real and committed.
    ("Hyperscaler CapEx YoY",            77.0, "% YoY",   10,  30,  60, True,
     "validates AI demand; MSFT invests $50B+/yr; co-hyperscalers = Azure workloads"),

    # LinkedIn revenue YoY: +8%.
    # Reflects enterprise hiring health and B2B ad spend. LinkedIn Premium
    # and Talent Solutions are discretionary enterprise spend — a macro canary.
    # Slowed from 10-12% due to hiring freeze cycle but positive and recovering.
    ("LinkedIn revenue — YoY",            8.0, "% YoY",    5,  12,  20, True,
     "enterprise hiring health + B2B ad market; LinkedIn = 7% of MSFT revenue"),

    # GitHub Copilot paid subscribers: 1.8M.
    # Developer-facing AI adoption is the most durable signal — developers choose
    # tools on merit. 1.8M paid at $19/month = ~$410M ARR and growing 80%+ YoY.
    # Leads enterprise Copilot adoption by 6-12 months (developers → IT buyers).
    ("GitHub Copilot paid subscribers",   1.8, "M subs",   0.5,  1,   2, True,
     "developer AI adoption → leads enterprise M365 Copilot decisions by 6-12M"),

    # Enterprise software spend YoY: +14.7% (Gartner, 2026).
    # Measures total enterprise software TAM growth — MSFT captures largest share.
    # Strong enterprise software spend = pricing power on M365 + Azure renewals.
    ("Enterprise software spend YoY",    14.7, "% YoY",    5,  10,  15, True,
     "M365 + Azure renewal pricing power; TAM expansion for cloud and AI services"),
]
WEIGHTS = [0.25, 0.20, 0.15, 0.15, 0.15, 0.10]

STRUCTURAL_FACTORS = [
    ("Azure enterprise incumbent switching cost",     1.5, 0.30),
    ("OpenAI co-opetition / dependency risk",        -0.5, 0.20),
    ("$65B CapEx cycle commitment risk",             -0.5, 0.20),
    ("Copilot adoption ceiling uncertainty",         -0.5, 0.15),
    ("Regulatory / antitrust pressure",              -0.3, 0.15),
]


FLOOR_DATA = {
    "trough_2022":        213.0,
    "cum_fcf_per_share":  29.5,
    "debt_delta":         3.0,   # +ve = debt grew (floor lower); -ve = balance sheet improved
    "reflation":           0.17,   # cumul. US CPI Jan 2022 - May 2026
}

def worst_case_floor():
    t, refl = FLOOR_DATA["trough_2022"], FLOOR_DATA["reflation"]
    fcf, ddt = FLOOR_DATA["cum_fcf_per_share"], FLOOR_DATA["debt_delta"]
    ref_adj = t * (1 + refl)
    floor   = ref_adj + fcf - ddt
    bear_p  = SCENARIOS["BEAR"][2]
    gap_pct = (floor - CURRENT_PRICE) / CURRENT_PRICE * 100
    bvf_pct = (bear_p - floor) / floor * 100
    return ref_adj, floor, gap_pct, bear_p, bvf_pct

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

attach_pct, curr_arr, rev_per_pp, bull_arr, xbull_arr, github_arr = copilot_economics()

print()
print("═" * W)
print("  MSFT SIGNAL MODEL  —  proxy vs. market-implied probability")
print("═" * W)

# Copilot monetization
print(f"\n  COPILOT MONETIZATION CALCULATOR  (the $30/seat revenue engine)")
print("  " + "─" * (W-2))
print(f"  M365 commercial seat base:          {M365_COMMERCIAL_SEATS_M:>4}M seats  (addressable)")
print(f"  Copilot for M365 paid seats:        {COPILOT_PAID_SEATS_M:>4}M seats  ({attach_pct:.1f}% attach rate)")
print(f"  Annual price per seat:              ${COPILOT_MONTHLY_USD*12:>3}/yr  (${COPILOT_MONTHLY_USD}/mo)")
print(f"  Current Copilot ARR:                ${curr_arr:.1f}B / yr")
print(f"  Incremental ARR per 1pp attach:     ${rev_per_pp:.2f}B / pp  ← the compounding lever")
print(f"  ─────────────────────────────────────────────────────")
print(f"  BASE scenario (50M seats, 12.5%):   ${50e6*COPILOT_MONTHLY_USD*12/1e9:.1f}B ARR")
print(f"  BULL scenario (100M seats, 25%):    ${bull_arr:.0f}B ARR")
print(f"  XBULL scenario (200M seats, 50%):   ${xbull_arr:.0f}B ARR  ← adds another Azure")
print(f"\n  GitHub Copilot:  {GITHUB_COPILOT_SUBS_M:.1f}M paid subs × ${GITHUB_COPILOT_ARPU_MO}/mo  =  ${github_arr:.2f}B ARR")
print(f"  → At 80%+ YoY growth, GitHub Copilot crosses $1B ARR within 12 months.")
print(f"  → This precedent (developer adoption) leads enterprise M365 adoption by 6-12M.")

# Signal scorecard
print(f"\n  PROXY SIGNAL SCORECARD")
print(f"  {'Signal':<38}{'Value':>9}  Wt   Score")
print("  " + "─" * (W-2))
for name, val, unit, s, w, rt in scored:
    bar = "█" * s + "░" * (4 - s)
    if unit == "M seats":
        fmt = f"{val:>+7.1f}"
    elif unit == "M subs":
        fmt = f"{val:>+7.1f}"
    else:
        fmt = f"{val:>+7.1f}"
    print(f"  {name:<38}{fmt}{unit[0]}  {w*100:.0f}%  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:   {proxy_composite:.2f} / 4.00")
if mkt_composite:
    print(f"  Market composite:  {mkt_composite:.2f} / 4.00  "
          f"(back-solved from ${CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% reqd return)")
    gap = proxy_composite - mkt_composite
    print(f"  Gap (proxy − mkt): {gap:+.2f}  ← 'show me EPS flow-through' discount")

# Valuation context
print(f"\n  VALUATION CONTEXT")
print("  " + "─" * (W-2))
fy25_eps = 13.5
print(f"  FY2025E non-GAAP EPS:        ~${fy25_eps:.2f}")
print(f"  Current forward P/E:          {CURRENT_PRICE/fy25_eps:.1f}x  (historical range: 22-40x)")
print(f"  FY2026E CapEx:               ~$65B  (Azure + AI infra build-out)")
print(f"  Azure AI services revenue:   ~$13B annualised (13pp of 35% growth)")
print(f"  OpenAI relationship:          $13B invested; Azure = primary OpenAI API cloud")
print(f"  Free cash flow margin:        ~35%  (highest of any $400B+ revenue company)")
print(f"  → Premium multiple justified by recurring revenue mix (~85% of total revenue)")

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

# Downside floor
_ref_adj, _floor, _gap_pct, _bear_p, _bvf = worst_case_floor()
_t   = FLOOR_DATA["trough_2022"]
_fcf = FLOOR_DATA["cum_fcf_per_share"]
_ddt = FLOOR_DATA["debt_delta"]
print(f"\n  DOWNSIDE FLOOR  (why the 2022 low cannot recur at same nominal price)")
print("  " + "─" * (W-2))
print(f"  2022 reference trough:                  ${_t:.0f}")
print(f"    + Reflation (+17% cumul. CPI since 2022):  +${_t*0.17:.0f}  \u2192  ${_t*1.17:.0f}")
print(f"    + Cumul. FCF earned FY2023-2025:           +${_fcf:.0f}  \u2192  ${_t*1.17+_fcf:.0f}")
if _ddt > 0:
    print(f"    - Net debt increase since 2022 / share:    -${_ddt:.0f}  \u2192  ${_floor:.0f}  (leverage drag)")
else:
    print(f"    + Balance sheet improvement / share:       +${-_ddt:.0f}  \u2192  ${_floor:.0f}")
print(f"  {chr(32)*4}{chr(45)*62}")
print(f"  ANALYTICAL FLOOR (2026 equiv.):         ${_floor:.0f}")
print(f"  Current price:                          ${CURRENT_PRICE:.0f}   downside to floor: {_gap_pct:+.0f}%")
if _bvf >= 0:
    print(f"  BEAR scenario (${_bear_p:.0f}):   BEAR is +{_bvf:.0f}% above floor  \u2713  adequate cushion")
else:
    print(f"  BEAR scenario (${_bear_p:.0f}):   BEAR is {_bvf:.0f}% BELOW floor  \u2190 structural break scenario")
print(f"  \u2192 The 2022 low (${_t:.0f}) cannot recur: ${_fcf:.0f}/share FCF already locked in,")
print(f"    17% inflation raised every nominal anchor. Floor ratchets up each year.")

# Verdict
print(f"\n  WHAT THE GAP MEANS")
print("  " + "─" * (W-2))
gap = (proxy_composite - mkt_composite) if mkt_composite else 0
print(f"""  Proxy composite {proxy_composite:.2f}  vs  market-implied {mkt_composite:.2f}.
  Gap = {gap:+.2f}

  Cross-stock gap comparison (full framework):
    ORCL gap = +2.16  (proxies XBULL; market prices OpenAI concentration risk)
    AVGO gap = +1.41  (proxies bullish; market prices AI flow-through risk)
    MSFT gap = {gap:+.2f}  ← EPS margin expansion discount
    SAP  gap = +0.91  (proxies constructive; Joule unmonetised)
    XTB  gap = +0.46  (justified volatility discount on cyclical revenue)
    COIN gap = +0.29  (approximately fairly priced; thesis is BTC price)
    CAT  gap = -0.24  (market already priced ahead of proxy confirmation)

  WHY MSFT'S GAP IS SMALLER THAN ORCL DESPITE SIMILAR PROXY SCORES:

    ORCL proxy: ~3.90   MSFT proxy: {proxy_composite:.2f}   (similar signal strength)
    ORCL gap:  +2.16   MSFT gap:  {gap:+.2f}   (MSFT gets credit for delivery)

    The difference is EXECUTION CERTAINTY:
    • ORCL's $553B RPO is contracted-but-not-yet-recognised. 54% is one
      customer. Zero of it is in reported EPS yet.
    • MSFT's 30M Copilot seats generate $10.8B ARR that IS in the numbers.
      Azure AI services (13pp of growth) IS flowing through to revenue.
    The market discounts ORCL heavily for concentration + delivery risk.
    MSFT gets partial credit because the AI thesis is already confirmed.

  THE THREE REASONS THE GAP STILL EXISTS:

    1. Margin compression at peak investment: MSFT is in the 'invest now,
       harvest later' phase. FY2026 CapEx ~$65B absorbs FCF and compresses
       near-term EPS. Market prices normalised-margin EPS, not peak-invest EPS.
       Azure AI gross margin is ~60% (vs 72% for non-AI Azure) — mix drag.

    2. Copilot attach rate ceiling uncertainty: At 7.5% attach (30M / 400M),
       the product works. The open question is whether 25-50% attach is
       achievable or whether most users find Copilot optional, not essential.
       Enterprise software AI features have historically seen <20% adoption.

    3. OpenAI relationship concentration: MSFT's $13B OpenAI investment and
       Azure's role as primary OpenAI inference cloud creates the same single-
       customer concentration risk as ORCL, but on the COST side (OpenAI
       consumes massive Azure capacity). If OpenAI's model quality advantage
       erodes (open-source models catch up), MSFT loses both revenue and a
       key product differentiator simultaneously.

  THE BULL CASE MATH — WHY $736 IS ACHIEVABLE WITHOUT HEROICS:

    Azure at 25% CAGR to FY2028 → ~$145B cloud revenue.
    M365 Copilot at 50M seats → $18B incremental ARR.
    Margin recovery as CapEx cycle peaks in FY2027 → EPS $23.
    Re-rating from 27x to 32x as investors price confirmed compounding.
    → $23 × 32x = $736  (+77% from $415, 2yr)

    Each 10M additional Copilot seats beyond 50M = +$3.6B ARR.
    At 30% incremental margin → $1.1B additional profit → ~$0.37 EPS.
    The BULL case requires only what LinkedIn and GitHub Copilot adoption
    data already confirm is technically feasible.

  THE NON-CONSENSUS CATALYST (what sell-side doesn't yet model fully):
    MSFT has 400M M365 commercial seats AND 1.5B Windows devices.
    Copilot+ PCs (neural-processing-unit hardware) create a HARDWARE
    attach path: MSFT earns on AI compute at the edge, not just cloud.
    Each 100M Copilot+ PCs at $3/device/month AI services = $3.6B ARR.
    Windows AI-native services is zero in every analyst model today.""")
print()
print("═" * W)
