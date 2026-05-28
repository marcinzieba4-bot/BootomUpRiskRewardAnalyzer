"""
DNP Select Income Fund, Inc. (NYSE: DNP)
Closed-End Fund · Utility & Telecom Income · Monthly Distribution · 30% Leverage
Bottom-Up Risk/Reward Signal Model
"""

import math

# ── CEF DISTRIBUTION & NAV CALCULATOR ──────────────────────────────────────────
CURRENT_PRICE       = 11.00   # USD, NYSE: DNP ~May 2026
NAV_PER_SHARE       = 10.55   # estimated current NAV
LEVERAGE_RATIO      = 0.30    # 30% structural leverage
PORTFOLIO_YIELD_PCT = 6.20    # gross portfolio yield %
BORROWING_RATE_PCT  = 5.20    # avg preferred/debt cost %
EXPENSE_RATIO_PCT   = 1.10    # management + admin %
MONTHLY_DIST        = 0.065   # monthly distribution per share ($)
SHARES_OUT_M        = 418     # shares outstanding (millions)

# Derived
equity_ps       = NAV_PER_SHARE * (1 - LEVERAGE_RATIO)          # equity portion per share
portfolio_ps    = NAV_PER_SHARE / (1 - LEVERAGE_RATIO)          # gross portfolio per share
debt_ps         = portfolio_ps - NAV_PER_SHARE                  # debt per share
port_income_ps  = portfolio_ps * PORTFOLIO_YIELD_PCT / 100      # gross income
borrow_cost_ps  = debt_ps      * BORROWING_RATE_PCT  / 100      # interest cost
expense_ps      = NAV_PER_SHARE * EXPENSE_RATIO_PCT  / 100      # expenses
nii_ps          = port_income_ps - borrow_cost_ps - expense_ps  # net investment income
annual_dist_ps  = MONTHLY_DIST * 12                             # annual distribution
coverage_pct    = nii_ps / annual_dist_ps * 100                 # NII coverage ratio
roc_pct         = max(0, 100 - coverage_pct)                    # return-of-capital %
premium_disc    = (CURRENT_PRICE - NAV_PER_SHARE) / NAV_PER_SHARE * 100  # premium/(discount)

print("=" * 72)
print("DNP SELECT INCOME FUND — CEF DISTRIBUTION & NAV CALCULATOR")
print("=" * 72)
print(f"  NAV per share             : ${NAV_PER_SHARE:.2f}")
print(f"  Current price             : ${CURRENT_PRICE:.2f}  ({premium_disc:+.1f}% premium/discount to NAV)")
print(f"  Leverage ratio            : {LEVERAGE_RATIO*100:.0f}%")
print(f"  Gross portfolio per share : ${portfolio_ps:.2f}")
print(f"  Debt per share            : ${debt_ps:.2f}")
print(f"  Gross portfolio income/sh : ${port_income_ps:.3f}  ({PORTFOLIO_YIELD_PCT}% yield on {portfolio_ps:.2f})")
print(f"  Borrowing cost/sh         : ${borrow_cost_ps:.3f}  ({BORROWING_RATE_PCT}% on debt {debt_ps:.2f})")
print(f"  Expenses/sh               : ${expense_ps:.3f}  ({EXPENSE_RATIO_PCT}% on NAV)")
print(f"  Net investment income/sh  : ${nii_ps:.3f}")
print(f"  Annual distribution/sh    : ${annual_dist_ps:.3f}  (${MONTHLY_DIST}/mo × 12)")
print(f"  NII coverage ratio        : {coverage_pct:.1f}%  — ROC component: {roc_pct:.1f}%")
print()

# 100bps rate shock sensitivity
rate_shock_bps   = 100
rate_shock_cost  = debt_ps * (rate_shock_bps / 10000)
print(f"  +100bps rate shock → additional cost/sh: ${rate_shock_cost:.3f}  (NII → ${nii_ps - rate_shock_cost:.3f})")
print(f"  NAV leverage multiplier (bear): {1/(1-LEVERAGE_RATIO):.2f}x  (30% equity loss → ~43% NAV loss)")
print()

# ── SIGNAL PARAMETERS ─────────────────────────────────────────────────────────
EPP_TODAY_EPS  = annual_dist_ps   # treat annual distribution as "earnings" for EPP
EPP_MIN_PE     = 8                # panic yield floor = 12.5% → 1/0.125 = 8x
EPP            = EPP_TODAY_EPS * EPP_MIN_PE
epp_gap_pct    = (CURRENT_PRICE - EPP) / EPP * 100

SCENARIOS = {
    #         EPS,   P/E,  price,  narrative
    "BEAR":  (0.40,  12,   5,   "Rate spike 6%+; NAV -40% via leverage; distribution cut ~50%"),
    "BASE":  (0.78,  13,  10,   "Rates 4–5% range; utility stable; near-NAV; distribution maintained"),
    "BULL":  (0.78,  18,  14,   "Fed cuts to 3.5%; utility re-rate; distribution secured + growing"),
    "XBULL": (0.85,  19,  16,   "Deep cuts 2.5%; utility supercycle; premium; distribution raised"),
}

# Conservative case
CONS_EPS_CAGR  = 0.03    # distribution grows 3%/yr
CONS_EXIT_PE   = 14.0    # conservative exit multiple (14x ≈ 7.1% yield)
CONS_DIVIDEND  = annual_dist_ps

# Volatility
VOL_ANNUAL_PCT = 0.18
VOL_BETA       = 0.55
VOL_52W_LOW    = 8.90
VOL_52W_HIGH   = 11.65

# ── HELPER FUNCTIONS ───────────────────────────────────────────────────────────
def softmax_probs(composite: float, T: float = 0.60) -> dict:
    centers = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    raw = {k: math.exp(-((composite - v) ** 2) / (2 * T ** 2)) for k, v in centers.items()}
    total = sum(raw.values())
    return {k: v / total for k, v in raw.items()}

def score_signal(val, base_floor, bull_floor, xbull_floor, higher_is_better=True):
    if higher_is_better:
        if val >= xbull_floor: return 4
        if val >= bull_floor:  return 3
        if val >= base_floor:  return 2
        return 1
    else:
        if val <= xbull_floor: return 4
        if val <= bull_floor:  return 3
        if val <= base_floor:  return 2
        return 1

def market_implied_composite(target_ev: float, tolerance: float = 0.08) -> float:
    for c100 in range(100, 401):
        c = c100 / 100
        probs = softmax_probs(c)
        ev = sum(probs[k] * SCENARIOS[k][2] for k in SCENARIOS)
        if abs(ev - target_ev) < tolerance:
            return c
    return 3.00

# ── SIGNALS ───────────────────────────────────────────────────────────────────
SIGNALS = [
    # (name, unit, bear_val, base_floor, bull_floor, xbull_floor, current_val, higher_is_better, bear_narrative)
    ("10yr Treasury yield — YoY change", "bps",
     150,  50,  -25, -100,
     -60, False,
     "Rate spike crushes NAV via leverage; distribution cut forced"),

    ("Utility sector total return — YoY", "%",
     -20,   0,   12,   25,
      18,  True,
     "Utilities sell off hard; rising discount worsens loss vs NAV"),

    ("NAV premium / (discount)", "%",
     -15,  -5,    0,    5,
       4,  True,
     "Panic drives to 15%+ discount; amplifies price loss beyond NAV"),

    ("NII coverage ratio", "%",
      55,  65,   78,   90,
      68,  True,
     "NII collapses below 55%; forced distribution cut; confidence shock"),

    ("Leverage utilisation vs NAV", "%",
      95,  88,   72,   55,
      86, False,
     "Leverage hits covenant limit; forced asset sales at trough"),

    ("IG credit spread OAS — YoY change", "bps",
     150,  50,    0,  -30,
     -15, False,
     "Credit widening pressures portfolio marks; utility refinancing cost rises"),
]

SIGNAL_WEIGHTS = [0.30, 0.20, 0.15, 0.15, 0.10, 0.10]

# ── STRUCTURAL COMPOSITE ADJUSTMENT ───────────────────────────────────────────
STRUCTURAL_FACTORS = [
    ("37-yr monthly distribution track record; Duff & Phelps expertise",     0.7, 0.25),
    ("AI data-centre power demand: structural utility re-rating tailwind",    0.8, 0.25),
    ("30% leverage amplifies NAV both ways; interest coverage rate-sensitive",-0.6, 0.25),
    ("31% ROC component in distributions erodes NAV if sustained long-term", -0.5, 0.15),
    ("Managed distribution policy; can reduce — limits permanent impairment",  0.2, 0.10),
]

# ── PART 1 — SIGNAL DASHBOARD ─────────────────────────────────────────────────
print("PART 1 — SIGNAL DASHBOARD")
print("=" * 72)

scores, weighted_scores = [], []
for i, (name, unit, bv, bf, blf, xf, cv, hib, bear_note) in enumerate(SIGNALS):
    sc = score_signal(cv, bf, blf, xf, hib)
    label = {1: "BEAR", 2: "BASE", 3: "BULL", 4: "XBULL"}[sc]
    w = SIGNAL_WEIGHTS[i]
    scores.append(sc)
    weighted_scores.append(sc * w)
    direction = "▲ higher=better" if hib else "▼ lower=better"
    print(f"  [{i+1}] {name}")
    print(f"       Current: {cv:+.0f} {unit}   ({direction})   → {label} ({sc})")
    print(f"       Bear: {bv} | Base≥{bf} | Bull≥{blf} | XBull≥{xf}   weight={w:.0%}")
    print(f"       Bear trigger: {bear_note}")
    print()

proxy_composite = sum(weighted_scores) / sum(SIGNAL_WEIGHTS)
print(f"  Proxy composite (weighted avg): {proxy_composite:.2f}")
print()

# Structural Composite Adjustment
sca = sum(score * weight for _, score, weight in STRUCTURAL_FACTORS)
adj_composite = proxy_composite + sca
print("  Structural Composite Adjustment (SCA):")
for label, score, weight in STRUCTURAL_FACTORS:
    print(f"    {score:+.1f} × {weight:.2f}  {label}")
print(f"  SCA = {sca:+.2f}   Adjusted composite: {adj_composite:.2f}")
print()

# ── PART 2 ANALYST COMMENTARY ─────────────────────────────────────────────────
print()
print("PART 2 ANALYST COMMENTARY")
print("=" * 72)
print()

HURDLE_RATE     = 0.15
target_ev       = CURRENT_PRICE * (1 + HURDLE_RATE) ** 2
mic             = market_implied_composite(target_ev)
adj_gap         = adj_composite - mic
verdict         = ("UNDERVALUED" if adj_gap >  0.30
                   else "MODESTLY OVERVALUED" if adj_gap < -0.10
                   else "FAIRLY VALUED")

probs           = softmax_probs(adj_composite)
ev_model        = sum(probs[k] * SCENARIOS[k][2] for k in SCENARIOS)
upside_pct      = (ev_model - CURRENT_PRICE) / CURRENT_PRICE * 100

bear_p = SCENARIOS["BEAR"]
epp_gap = (CURRENT_PRICE - EPP) / EPP * 100

print(f"""DNP SELECT INCOME FUND — ANALYST COMMENTARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

① SIGNAL DASHBOARD SUMMARY
────────────────────────────
Proxy composite : {proxy_composite:.2f}  →  SCA {sca:+.2f}  →  Adjusted: {adj_composite:.2f}
Market-implied  : {mic:.2f}  (15% hurdle target = ${target_ev:.2f})
Signal gap      : {adj_gap:+.2f}  →  {verdict}

Scenario probabilities (adj. composite {adj_composite:.2f}):
  BEAR  {probs['BEAR']*100:5.1f}%  →  ${SCENARIOS['BEAR'][2]}
  BASE  {probs['BASE']*100:5.1f}%  →  ${SCENARIOS['BASE'][2]}
  BULL  {probs['BULL']*100:5.1f}%  →  ${SCENARIOS['BULL'][2]}
  XBULL {probs['XBULL']*100:5.1f}% →  ${SCENARIOS['XBULL'][2]}
  Expected value : ${ev_model:.2f}  ({upside_pct:+.1f}% vs ${CURRENT_PRICE:.2f})

VERDICT: WATCHLIST — market pricing near-correctly for a rate-sensitive
income vehicle. Adjusted composite {adj_composite:.2f} vs market-implied {mic:.2f};
gap ({adj_gap:+.2f}) is marginally positive but insufficient to justify
aggressive accumulation at the current ${CURRENT_PRICE:.2f} / +{premium_disc:.1f}% NAV premium.

② BEAR CASE ANATOMY
─────────────────────
Trigger: 10yr Treasury re-tests 6%+ (term premium normalisation, fiscal
concerns, or inflation re-acceleration). At 6% 10yr, utility equities
reprice for a 7–8% yield, NAV falls ~35–40% via 30% leverage amplification.
A forced distribution cut (~50%) follows as NII coverage collapses.

CEF leverage mechanics:
  30% leverage on ${NAV_PER_SHARE:.2f} NAV → gross portfolio ${portfolio_ps:.2f}/share
  A 25% portfolio mark-down → NAV: ${NAV_PER_SHARE:.2f} × (1 - 0.25/{1-LEVERAGE_RATIO:.2f}) = ${NAV_PER_SHARE*(1-0.25/(1-LEVERAGE_RATIO)):.2f}
  Price likely follows to ${bear_p[2]}–${bear_p[2]+1} (deep discount to distressed NAV)
  Distribution cut to ~${bear_p[0]:.2f}/yr (50% cut) reduces income appeal
  Leverage ratio forced higher → potential covenant breach → forced asset sales

③ UPDATED EPP (EARNINGS POWER PRICE — CEF ADAPTATION)
──────────────────────────────────────────────────────
EPP framework adapted: "EPS" = annual distribution = ${EPP_TODAY_EPS:.2f}
Panic floor multiple = 8× (implied yield 12.5% — historical CEF distress)

  EPP = ${EPP_TODAY_EPS:.2f} × {EPP_MIN_PE}× = ${EPP:.2f}
  Current price ${CURRENT_PRICE:.2f} is {epp_gap:.1f}% above EPP floor

Interpretation: the EPP floor ($6.24) represents a genuine panic scenario
(2008/2020 style) where DNP would trade at a 40%+ discount to NAV. This
is a "not-zero" floor. The +{epp_gap:.1f}% premium to EPP is comfortable for
an income-oriented instrument but does NOT imply safety at current rates.

NII floor stress test:
  At 6% borrowing cost: NII ≈ ${nii_ps - rate_shock_cost:.3f}/sh  (coverage {(nii_ps - rate_shock_cost)/annual_dist_ps*100:.0f}%)
  Distribution sustainability is the primary risk, not corporate default.

④ CONSERVATIVE GROWTH CASE
───────────────────────────
Assumptions: distribution flat for 2 years then +{CONS_EPS_CAGR*100:.0f}%/yr; exit at {CONS_EXIT_PE:.0f}× ({1/CONS_EXIT_PE*100:.1f}% yield)
""")

cons_dist_yr1 = CONS_DIVIDEND
cons_dist_yr2 = CONS_DIVIDEND * (1 + CONS_EPS_CAGR)
cons_dist_2yr = cons_dist_yr1 + cons_dist_yr2
cons_price_2yr = CONS_DIVIDEND * (1 + CONS_EPS_CAGR) ** 2 * CONS_EXIT_PE
cons_total     = cons_dist_2yr + cons_price_2yr
cons_ret_pct   = (cons_total - CURRENT_PRICE) / CURRENT_PRICE * 100

print(f"""  Year 1 distribution : ${cons_dist_yr1:.2f}
  Year 2 distribution : ${cons_dist_yr2:.3f}
  Total distributions : ${cons_dist_2yr:.3f}
  Exit price (2yr)    : ${cons_price_2yr:.2f}   ({CONS_EXIT_PE:.0f}× × ${CONS_DIVIDEND*(1+CONS_EPS_CAGR)**2:.3f})
  Conservative total  : ${cons_total:.2f}   ({cons_ret_pct:+.1f}% over 2 yr)

Conservative case delivers only {cons_ret_pct:.1f}% over 2 years at current price —
equivalent to ~{cons_ret_pct/2:.1f}%/yr total return. Income investors could match
this in short-duration IG bonds with zero NAV risk. The risk/reward tilts
to WATCHLIST unless rates fall meaningfully.

⑤ VOLATILITY CONTEXT
──────────────────────
  52-week range : ${VOL_52W_LOW:.2f} – ${VOL_52W_HIGH:.2f}
  Current       : ${CURRENT_PRICE:.2f}   ({(CURRENT_PRICE-VOL_52W_LOW)/(VOL_52W_HIGH-VOL_52W_LOW)*100:.0f}th percentile of range)
  Annual vol    : {VOL_ANNUAL_PCT*100:.0f}%   Beta: {VOL_BETA:.2f}x (low equity beta; high rate-duration beta)
  1σ range (1yr): ${CURRENT_PRICE*(1-VOL_ANNUAL_PCT):.2f} – ${CURRENT_PRICE*(1+VOL_ANNUAL_PCT):.2f}

CEF-specific volatility note: DNP's equity beta (~0.55) understates true
interest-rate duration risk. A +100bps parallel shift in rates can produce
a 10–15% price decline — far larger than the equity beta implies. The key
risk variable is the 10yr Treasury yield, not the S&P 500.

⑥ SCENARIO PROBABILITIES
──────────────────────────
Softmax distribution centred on adj. composite {adj_composite:.2f}:
""")

print(f"  BEAR   {probs['BEAR']*100:5.1f}%  EPS ${SCENARIOS['BEAR'][0]:.2f}  ×{SCENARIOS['BEAR'][1]}P/E  =  ${SCENARIOS['BEAR'][2]}")
print(f"         {SCENARIOS['BEAR'][3]}")
print(f"  BASE   {probs['BASE']*100:5.1f}%  EPS ${SCENARIOS['BASE'][0]:.2f}  ×{SCENARIOS['BASE'][1]}P/E  =  ${SCENARIOS['BASE'][2]}")
print(f"         {SCENARIOS['BASE'][3]}")
print(f"  BULL   {probs['BULL']*100:5.1f}%  EPS ${SCENARIOS['BULL'][0]:.2f}  ×{SCENARIOS['BULL'][1]}P/E  =  ${SCENARIOS['BULL'][2]}")
print(f"         {SCENARIOS['BULL'][3]}")
print(f"  XBULL  {probs['XBULL']*100:5.1f}%  EPS ${SCENARIOS['XBULL'][0]:.2f}  ×{SCENARIOS['XBULL'][1]}P/E  =  ${SCENARIOS['XBULL'][2]}")
print(f"         {SCENARIOS['XBULL'][3]}")
print()
print(f"  Expected value : ${ev_model:.2f}  ({upside_pct:+.1f}% upside from ${CURRENT_PRICE:.2f})")
print()

# ── PART 3 NUMBERS & SIGNALS ──────────────────────────────────────────────────
print()
print("PART 3 NUMBERS & SIGNALS")
print("=" * 72)

# Ratio B
bear_price  = SCENARIOS["BEAR"][2]
bull_price  = SCENARIOS["BULL"][2]
downside    = (CURRENT_PRICE - bear_price) / CURRENT_PRICE
upside      = (bull_price - CURRENT_PRICE) / CURRENT_PRICE
ratio_b     = downside / upside if upside > 0 else 99
ratio_b_fmt = f"{ratio_b:.2f}x"

if ratio_b < 0.75:
    signal_short = "BUY"
    signal       = "◉ BUY"
elif ratio_b < 1.10:
    signal_short = "ACCUMULATE"
    signal       = "◎ ACCUMULATE"
elif ratio_b < 1.75:
    signal_short = "WATCHLIST"
    signal       = "◐ WATCHLIST"
else:
    signal_short = "AVOID"
    signal       = "✕ AVOID"

print(f"""
  Ticker          : DNP
  Company         : DNP Select Income Fund, Inc.
  Sector          : Closed-End Fund (CEF) · Utility & Telecom Income · Leveraged
  Current price   : ${CURRENT_PRICE:.2f}
  NAV per share   : ${NAV_PER_SHARE:.2f}  (premium: {premium_disc:+.1f}%)
  Annual dist.    : ${annual_dist_ps:.3f}  (${MONTHLY_DIST}/mo × 12)
  NII coverage    : {coverage_pct:.1f}%  (ROC: {roc_pct:.1f}%)
  EPP floor       : ${EPP:.2f}  ({EPP_TODAY_EPS:.2f} × {EPP_MIN_PE}×)
  EPP gap         : {epp_gap:.1f}%  (current vs EPP floor)
  Downside (Bear) : {downside*100:.1f}%  → ${bear_price}
  Upside (Bull)   : {upside*100:.1f}%   → ${bull_price}
  Ratio B         : {ratio_b_fmt}  (downside ÷ upside)
  Expected value  : ${ev_model:.2f}  ({upside_pct:+.1f}%)
  Conservative 2yr: {cons_ret_pct:+.1f}%  (${cons_total:.2f} total)
  Signal          : {signal}
  Proxy composite : {proxy_composite:.2f}
  Adj. composite  : {adj_composite:.2f}  (SCA: {sca:+.2f})
  Market-implied  : {mic:.2f}  → {verdict}
""")

print("━" * 72)
print(f"  SIGNAL: {signal}   Ratio B: {ratio_b_fmt}")
print(f"  Adj. composite {adj_composite:.2f} vs market-implied {mic:.2f} ({adj_gap:+.2f})")
print("━" * 72)
print()
print("  RISK FACTORS:")
print(f"  • Rate sensitivity: +100bps → NII falls ${rate_shock_cost:.3f}/sh; NAV -4–6% direct")
print(f"  • Leverage amplification: 1/{1-LEVERAGE_RATIO:.2f} = {1/(1-LEVERAGE_RATIO):.2f}× NAV multiplier on portfolio moves")
print(f"  • ROC sustainability: {roc_pct:.1f}% of dist. is return-of-capital; long-term NAV erosion risk")
print(f"  • Current {premium_disc:+.1f}% NAV premium offers limited margin of safety vs historical discounts")
print()
print("  Not financial advice. EPP = annual distribution × panic-floor multiple.")
print("  CEF model: 'P/E' = 1/yield floor; leverage mechanics drive scenario pricing.")
