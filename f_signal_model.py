"""
F  ·  Ford Motor Company  ·  NYSE: F
Bottom-up signal model  ·  Auto Manufacturing · ICE Cash Cow + Ford Pro + EV Transition
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "F"
COMPANY       = "Ford Motor Company"
SECTOR        = "Auto Manufacturing · ICE + Ford Pro + EV Transition · NYSE: F"
CURRENT_PRICE = 11.00      # USD; as of 2026-06-11
VOL_52W_LOW   = 9.00
VOL_52W_HIGH  = 14.00
SHARES_OUT_M  = 4000.0     # millions

# Dividend
ANNUAL_DIV    = 0.60       # $/share (regular $0.15/qtr; supplemental dividends possible on top)

# ── FORD PRO / ICE PROFITABILITY vs EV LOSSES ANALYSIS (company-specific) ─────
FORD_PRO_OP_MARGIN = 0.12   # Ford Pro (commercial/fleet) segment operating margin
EV_LOSS_PER_UNIT_B = 2.5    # annual EV segment (Model e) operating loss ($B), narrowing
BUYBACK_PCT        = 0.00   # minimal buyback; capital returned mainly via dividend
TAX_RATE           = 0.21

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 1.20    # FY2026E adj EPS
PE_TROUGH = 5       # min P/E at crisis trough (cyclical auto, 2008/2020 lows)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $6

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (0.70, 6,    4, "Recession hits truck/SUV demand + price wars; EV losses widen further; EPS $0.70 -> 6x distress P/E"),
    "BASE":  (1.20, 9,   11, "Ford Pro fleet demand stays solid; ICE trucks/SUVs remain profitable; EV losses narrow gradually; EPS $1.20 -> 9x P/E"),
    "BULL":  (1.60, 11,  18, "Ford Pro margins expand further; EV segment losses narrow faster than expected; EPS $1.60 -> 11x P/E"),
    "XBULL": (2.00, 13,  26, "EV segment reaches breakeven; Ford Pro becomes a recognized high-margin compounder; market re-rates Ford; EPS $2.00 -> 13x peak P/E"),
}

# ── SOFTMAX ───────────────────────────────────────────────────────────────────
CENTERS = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
T = 0.60

def softmax_probs(c):
    raw = {s: math.exp(-abs(c - CENTERS[s]) / T) for s in CENTERS}
    tot = sum(raw.values())
    return {s: raw[s] / tot for s in raw}

def expected_value(c):
    p = softmax_probs(c)
    return sum(p[s] * SCENARIOS[s][2] for s in SCENARIOS)

def back_solve_market_composite(price, tol=0.001):
    target = price * (1.15 ** 2)
    lo, hi = 1.0, 4.0
    for _ in range(80):
        m = (lo + hi) / 2
        if expected_value(m) < target:
            lo = m
        else:
            hi = m
    return round((lo + hi) / 2, 2)

# ── 6 PROXY SIGNALS ───────────────────────────────────────────────────────────
SIGNALS = [
    {
        "name":       "North America ICE (truck/SUV) operating margin",
        "weight":     0.25,
        "thresholds": ("<4%",   "≥6%",   "≥8%",   "≥10%"),
        "now":        "~7%",
        "score":      2,
        "comment":    "~7%; F-Series remains highly profitable but pricing/incentive pressure caps margin expansion",
    },
    {
        "name":       "Ford Pro (commercial/fleet) revenue growth",
        "weight":     0.20,
        "thresholds": ("<0%",   "≥5%",   "≥8%",   "≥12%"),
        "now":        "~9%",
        "score":      3,
        "comment":    "~9%; software/services attach (paid subscriptions) drives high-margin recurring revenue",
    },
    {
        "name":       "EV segment (Model e) operating loss ($B/yr, narrowing)",
        "weight":     0.15,
        "thresholds": (">$5B",  "≥$3B",  "≥$2B",  "≥$1B"),
        "now":        "~$2.5B",
        "score":      2,
        "comment":    "~$2.5B annual loss; capacity right-sizing and battery cost cuts narrowing the drag gradually",
    },
    {
        "name":       "Free cash flow ($B/yr)",
        "weight":     0.15,
        "thresholds": ("<$2B",  "≥$4B",  "≥$6B",  "≥$8B"),
        "now":        "~$5B",
        "score":      2,
        "comment":    "~$5B; supports the dividend with room for occasional supplemental payouts",
    },
    {
        "name":       "Dividend payout ratio",
        "weight":     0.10,
        "thresholds": (">80%",  "≤70%",  "≤60%",  "≤50%"),
        "now":        "~55%",
        "score":      3,
        "comment":    "~55%; well-covered base dividend (~5.5% yield) with supplemental dividend optionality",
    },
    {
        "name":       "Quality / warranty cost trend",
        "weight":     0.15,
        "thresholds": ("worsening", "flat",  "improving", "strongly improving"),
        "now":        "improving",
        "score":      3,
        "comment":    "improving; warranty costs declining YoY as quality initiatives reduce recall frequency",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Ford Pro is a high-margin, recurring-revenue commercial/fleet franchise that is underappreciated by the market", +0.5, 0.20),
    ("+", "Well-covered ~5.5% dividend yield with supplemental dividend optionality provides a return floor",                +0.3, 0.20),
    ("+", "Improving quality/warranty cost trend reduces a multi-year drag on margins",                                       +0.2, 0.15),
    ("-", "EV segment (Model e) losses remain a multi-billion-dollar annual drag with uncertain breakeven timing",            -0.5, 0.25),
    ("-", "Highly cyclical ICE truck/SUV demand and UAW labor cost structure leave thin margins exposed to a downturn",       -0.4, 0.20),
]
SCA = sum(score * weight for _, _, score, weight in SCA_FACTORS)
ADJ_COMPOSITE = round(PROXY_COMPOSITE + SCA, 3)

MARKET_COMPOSITE = back_solve_market_composite(CURRENT_PRICE)
ADJ_GAP = round(ADJ_COMPOSITE - MARKET_COMPOSITE, 2)

if ADJ_GAP > 0.20:
    valuation_label = "UNDERVALUED"
elif ADJ_GAP > -0.20:
    valuation_label = "FAIRLY VALUED"
else:
    valuation_label = "MODESTLY OVERVALUED"

# ── RATIO B ───────────────────────────────────────────────────────────────────
bear_price   = SCENARIOS["BEAR"][2]
bull_price   = SCENARIOS["BULL"][2]
downside_pct = (CURRENT_PRICE - bear_price) / CURRENT_PRICE
upside_pct   = (bull_price - CURRENT_PRICE) / CURRENT_PRICE
ratio_b      = round(downside_pct / upside_pct, 2)

if ratio_b < 0.75:
    signal_short, signal_full = "BUY",       "◉ BUY"
elif ratio_b < 1.10:
    signal_short, signal_full = "ACCUMULATE","◎ ACCUMULATE"
elif ratio_b < 1.75:
    signal_short, signal_full = "WATCHLIST", "◐ WATCHLIST"
else:
    signal_short, signal_full = "AVOID",     "✕ AVOID"

# ── CONSERVATIVE GROWTH (2-yr) ────────────────────────────────────────────────
CONS_EPS_2YR = 1.40    # conservative FY2028E: Ford Pro growth + narrowing EV losses
CONS_PE_2YR  = 8        # floor multiple (slightly above current)
cons_equity  = CONS_EPS_2YR * CONS_PE_2YR
cons_divs    = ANNUAL_DIV * 2
cons_total   = cons_equity + cons_divs
cons_return  = round((cons_total - CURRENT_PRICE) / CURRENT_PRICE * 100, 1)
cons_annual  = round(cons_return / 2, 1)

# ─────────────────────────────────────────────────────────────────────────────
#  OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
W = 72

def hr(): print("  " + "─" * W)
def bar(score):
    return "█" * score + "░" * (4 - score)

print()
print("═" * (W + 4))
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Auto Manufacturing / Ford Pro + EV Transition")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① FORD PRO / EV ANALYSIS ────────────────────────────────────────────────
print()
print("  FORD PRO GROWTH vs EV LOSSES ANALYSIS  (the core F earnings drivers)")
hr()
shares_b = SHARES_OUT_M / 1000
ford_pro_rev_b = 65.0
print(f"  Estimated FY2026E Ford Pro revenue base: ~${ford_pro_rev_b:.0f}B")
print()
print(f"  FORD PRO GROWTH UPSIDE  (incremental EPS from Ford Pro growth at {FORD_PRO_OP_MARGIN*100:.0f}% operating margin):")
print(f"  {'Ford Pro YoY growth':<20}  {'Rev/yr ($B)':>12}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.00, 0.05, 0.09, 0.12]:
    rev_inc = ford_pro_rev_b * g
    inc_eps = rev_inc * FORD_PRO_OP_MARGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% Ford Pro growth         +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
print(f"  EV SEGMENT LOSS  (~${EV_LOSS_PER_UNIT_B:.1f}B/yr drag from Model e; each $1B of loss reduction adds")
print(f"  ~${1.0*(1-TAX_RATE)/shares_b:.2f}/share to EPS as capacity is right-sized and battery costs decline).")
print()
print(f"  BEAR (${bear_price:.2f}) requires: a recession that hits truck/SUV demand and reignites price wars")
print(f"  AND EV losses widen further AND multiple compresses to distress levels — together.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (ICE margin + Ford Pro growth + EV losses + FCF + dividend + quality)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>10}  {'BASE':>7}  {'BULL':>7}  {'XBULL':>14}  {'NOW':>9}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>10}  {ths[1]:>7}  {ths[2]:>7}  {ths[3]:>14}  {s['now']:>9}  {lbl}  {b}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15% hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  ->  Adj composite {ADJ_COMPOSITE:.3f}  ->  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    c = score * weight
    print(f"    {sign}  {desc[:72]:<72}  ({score:+.1f} x {weight*100:.0f}%  =  {c:+.3f})")

# ─── ② BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price:.2f})")
hr()
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>7}  Trigger")
hr()
bear_triggers = [
    ("NA ICE (truck/SUV) operating margin",        "~7%",    "<4%",   "-3pp",   "Recession + price wars compress truck/SUV margins"),
    ("Ford Pro revenue growth",                    "~9%",    "<0%",   "-9pp",   "Fleet customers cut capex amid commercial slowdown"),
    ("EV segment loss ($B/yr)",                    "~$2.5B", ">$5B",  "+$2.5B", "EV demand stalls; capacity underutilization worsens losses"),
    ("Free cash flow ($B/yr)",                     "~$5B",   "<$2B",  "-$3B",   "Working capital drag + lower volumes squeeze cash flow"),
    ("Dividend payout ratio",                      "~55%",   ">80%",  "+25pp",  "Earnings collapse pressures dividend sustainability"),
    ("Quality / warranty cost trend",              "improving", "worsening", "reversal", "New launches bring fresh quality issues and recalls"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A recession hits truck/SUV demand and reignites industry price wars while EV")
print(f"  segment losses widen further on demand softness and capacity underutilization.")
print(f"  EPS falls to ~$0.70; multiple compresses to 6x distress P/E = ${bear_price:.2f}.")

# ─── ③ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS x min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}")
print(f"  Min viable P/E at trough:      {PE_TROUGH}x  (cyclical auto, 2008/2020-era distress multiple)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct>=0 else 'below'} trough floor)")
print()
print(f"  Premium to EPP reflects Ford Pro's recurring-revenue franchise and the well-covered dividend.")
print(f"  Bear ${bear_price:.2f} is below EPP ${EPP:.0f} — would require both EPS collapse AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+0.20:.2f} x {PE_TROUGH}x = ${(EPP_EPS+0.2)*PE_TROUGH:.0f} EPP — narrowing EV losses lift the floor over time.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: Ford Pro growth continues, EV losses narrow gradually)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (Ford Pro growth + narrowing EV losses)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (slightly above current)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f} x 2)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — the dividend yield alone provides a meaningful")
print(f"  floor return, with Ford Pro growth and narrowing EV losses providing modest upside.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.30
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 2),
               round(CURRENT_PRICE * (1 + annual_vol), 2))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (above-market; cyclical auto exposure)")
print(f"  Beta vs S&P 500:      1.35  (above market; cyclical)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.2f}  -  ${sigma_range[1]:.2f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price:.2f} requires:  ~{bear_sigmas:.1f}σ move  (F has fallen ~50%+ from highs in past auto-cycle downturns; tail risk, not base case)")
print(f"  -> Ford Pro growth and EV loss trajectory are the PRIMARY catalysts;")
print(f"     Ford Pro strength + narrowing EV losses = upside; recession + EV losses widen = downside.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — mid range; the high dividend yield cushions downside.")
print(f"  -> BUY $9-$10  |  TRIM $13+  |  AVOID above $15")

# ─── ⑥ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print()
print("  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
hr()
probs_mkt = softmax_probs(MARKET_COMPOSITE)
print(f"  {'Scenario':<10}  {'Price':>6}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>7}  Description")
hr()
for s in ["BEAR","BASE","BULL","XBULL"]:
    pp   = probs_proxy[s] * 100
    pm   = probs_mkt[s]   * 100
    gap  = pp - pm
    pr   = SCENARIOS[s][2]
    desc = SCENARIOS[s][3][:45]
    print(f"  {s:<10}  ${pr:>5.2f}  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): ${ev_adj:.2f}  /  Proxy EV: ${ev_prx:.2f}  /  Market EV: ${ev_mkt:.2f}  /  Current: ${CURRENT_PRICE:.2f}")
hr()
print(f"  Downside  (-> Bear ${bear_price:.2f}):  {downside_pct*100:.1f}%")
print(f"  Upside    (-> Bull ${bull_price:.2f}):   {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b:.2f}x")
print(f"  Signal    :  {signal_full}")
print()
print(f"  Market composite {MARKET_COMPOSITE:.2f} reflects pricing roughly between BASE and BULL")
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees Ford Pro growth tempered by EV losses and cyclicality SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing the Ford Pro story.' if ADJ_GAP>0 else 'model roughly agrees with market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) Ford Pro revenue -> sustained >=9% growth confirms recurring-revenue franchise")
print(f"  (2) EV segment losses -> narrowing toward $1-2B/yr confirms breakeven path")
print(f"  (3) NA ICE margin -> holds >=7% confirms truck/SUV pricing discipline")
print(f"  (4) Quality/warranty trend -> continued improvement lowers cost drag")
print(f"  BUY $9-{round(CURRENT_PRICE*0.95,2):.2f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,2):.2f}  |  TRIM above $13  |  AVOID above $15")
print("═" * (W + 4))
print()

# ── EXPORT ────────────────────────────────────────────────────────────────────
RESULT = {
    "ticker":           TICKER,
    "signal":           signal_full,
    "signal_short":     signal_short,
    "price":            CURRENT_PRICE,
    "epp_gap_pct":      epp_gap_pct,
    "ratio_b":          ratio_b,
    "ratio_b_fmt":      f"{ratio_b:.2f}x",
    "adj_composite":    ADJ_COMPOSITE,
    "market_composite": MARKET_COMPOSITE,
    "adj_gap":          ADJ_GAP,
    "valuation":        valuation_label,
    "cons_return_2yr":  cons_return,
}

if __name__ == "__main__":
    pass
