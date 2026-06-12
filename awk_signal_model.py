"""
AWK  ·  American Water Works Company, Inc.  ·  NYSE: AWK
Bottom-up signal model  ·  Regulated Water & Wastewater Utility · M&A Tuck-Ins + Infrastructure Replacement Capex
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "AWK"
COMPANY       = "American Water Works Company, Inc."
SECTOR        = "Regulated Water & Wastewater Utility · Multi-State · NYSE: AWK"
CURRENT_PRICE = 145.00     # USD; as of 2026-06-11
VOL_52W_LOW   = 125.00
VOL_52W_HIGH  = 150.00
SHARES_OUT_M  = 195.0      # millions

# Dividend
ANNUAL_DIV    = 3.10       # $/share; ~2.1% yield, ~7-9%/yr dividend growth

# ── RATE BASE / GROWTH ANALYSIS (company-specific) ────────────────────────────
RATE_BASE_GROWTH   = 0.080   # ~8.0%/yr regulated rate base growth (infrastructure replacement capex plan)
DATA_CENTER_GROWTH = 0.02    # ~2% incremental contribution from M&A tuck-in acquisitions
INCREMENTAL_MARGIN = 0.40    # incremental operating margin on new rate base / acquired utilities
TAX_RATE           = 0.21

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 5.50    # FY2026E adj EPS
PE_TROUGH = 22      # min P/E at crisis trough (bond-proxy distress multiple)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $121

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (5.00, 18,   90,  "Rate case outcomes disappoint and rising rates compress bond-proxy multiples; M&A pipeline stalls; EPS $5.00 -> 18x distress P/E"),
    "BASE":  (5.50, 26,   143, "Regulated rate base +8%/yr on lead service line and main replacement capex; steady tuck-in M&A pace continues; EPS $5.50 -> 26x P/E"),
    "BULL":  (6.10, 30,   183,  "Tuck-in acquisition pace accelerates and infrastructure replacement programs expand; rate relief constructive; EPS $6.10 -> 30x premium P/E"),
    "XBULL": (6.75, 33,   223,  "Multi-year wave of municipal system acquisitions plus accelerated PFAS/lead-line replacement capex drives sustained above-plan rate base growth; EPS $6.75 -> 33x peak P/E"),
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
        "name":       "M&A tuck-in acquisition growth (regulated systems)",
        "weight":     0.25,
        "thresholds": ("<2 deals", "≥4 deals", "≥6 deals", "≥10 deals"),
        "now":        "~6 deals",
        "score":      3,
        "comment":    "~6 municipal/private water system acquisitions per year, in line with management's targeted pace across a highly fragmented industry",
    },
    {
        "name":       "Infrastructure replacement capex (lead/main replacement)",
        "weight":     0.25,
        "thresholds": ("Behind plan", "On track", "Ahead of plan", "Accelerated"),
        "now":        "On track",
        "score":      3,
        "comment":    "Multi-year lead service line and main replacement program tracking on schedule, underpinning a decade-plus rate base growth runway",
    },
    {
        "name":       "Adjusted EPS growth rate",
        "weight":     0.15,
        "thresholds": ("<6%",   "≥7%",   "≥8%",   "≥10%"),
        "now":        "~8%",
        "score":      3,
        "comment":    "~8%; tracking within management's 7-9% long-term EPS growth guidance range",
    },
    {
        "name":       "Regulatory ROE / multi-state rate case outcomes",
        "weight":     0.15,
        "thresholds": ("<9.0%", "≥9.5%", "≥9.8%", "≥10.2%"),
        "now":        "~9.7%",
        "score":      2,
        "comment":    "~9.7% blended allowed ROE; multi-state rate case outcomes have been mixed-to-constructive on infrastructure capex recovery",
    },
    {
        "name":       "Military Services Group (MSG) contract growth",
        "weight":     0.10,
        "thresholds": ("Flat",  "+1 base", "+2 bases", "+3 bases"),
        "now":        "+1 base",
        "score":      2,
        "comment":    "Steady, low-risk contract renewals and one incremental military base privatization win added to the portfolio",
    },
    {
        "name":       "Dividend growth rate",
        "weight":     0.10,
        "thresholds": ("<5%",   "≥6%",   "≥8%",   "≥10%"),
        "now":        "~8%",
        "score":      3,
        "comment":    "~8%/yr; consistent with management's targeted 7-9% long-term dividend growth",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Largest investor-owned water utility; highly fragmented industry gives a long M&A tuck-in runway",                                  +0.4, 0.25),
    ("+", "Aging infrastructure replacement need provides decade-plus visible capex/rate base growth",                                         +0.4, 0.25),
    ("+", "Essential-service demand inelasticity creates defensive, highly predictable earnings",                                               +0.2, 0.15),
    ("-", "Premium bond-proxy valuation is sensitive to interest-rate moves",                                                                   -0.4, 0.20),
    ("-", "PFAS remediation costs and emerging-contaminant regulatory risk create capex/cost uncertainty",                                      -0.3, 0.15),
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
CONS_EPS_2YR = 6.40    # conservative FY2028E: rate base growth + tuck-in M&A continue
CONS_PE_2YR  = 25       # floor multiple (slightly below current)
cons_equity  = CONS_EPS_2YR * CONS_PE_2YR
cons_divs    = ANNUAL_DIV * 2 * 1.08   # approximate dividend growth across the 2yr window
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Regulated Multi-State Water & Wastewater Utility")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① RATE BASE / GROWTH ANALYSIS ───────────────────────────────────────────
print()
print("  RATE BASE GROWTH + M&A TUCK-IN ANALYSIS  (the core AWK earnings drivers)")
hr()
shares_b = SHARES_OUT_M / 1000
total_revenue_b = 4.7
print(f"  Estimated FY2026E revenue base: ~${total_revenue_b:.1f}B")
print()
print(f"  GROWTH UPSIDE  (incremental EPS from rate base + acquired-system growth at {INCREMENTAL_MARGIN*100:.0f}% incremental margin):")
print(f"  {'Combined growth rate':<20}  {'Rev/yr ($B)':>12}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.00, 0.05, 0.080, 0.10]:
    rev_inc = total_revenue_b * g
    inc_eps = rev_inc * INCREMENTAL_MARGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.1f}% combined growth        +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
print(f"  M&A TUCK-IN ACQUISITION GROWTH  (~{DATA_CENTER_GROWTH*100:.0f}% incremental contribution from regulated")
print(f"  municipal/private water system acquisitions; converts directly into rate base additions under existing regulatory frameworks).")
print()
print(f"  BEAR (${bear_price}) requires: rate case outcomes disappoint")
print(f"  AND the M&A pipeline stalls amid rising rates, compressing the multiple — together.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (M&A tuck-in growth + infrastructure capex + EPS growth + ROE + MSG contracts + dividend)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>6}  {'BASE':>5}  {'BULL':>6}  {'XBULL':>8}  {'NOW':>7}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>6}  {ths[1]:>5}  {ths[2]:>6}  {ths[3]:>8}  {s['now']:>7}  {lbl}  {b}")

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
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>7}  Trigger")
hr()
bear_triggers = [
    ("M&A tuck-in acquisition growth",             "~6 deals","<2 deals","-4 deals","Pipeline stalls as rising rates raise financing costs for deals"),
    ("Infrastructure replacement capex execution", "On track","Behind plan","-","Cost overruns or supply-chain delays slow the replacement program"),
    ("Adjusted EPS growth",                        "~8%",    "<6%",   "-2pp",   "Financing costs and dilution offset rate base growth"),
    ("Regulatory ROE / rate case outcomes",        "~9.7%",  "<9.0%", "-0.7pp", "Multiple state commissions deliver disappointing rate case outcomes"),
    ("MSG contract growth",                        "+1 base","Flat",  "-1 base","No new military base privatization wins; contract attrition"),
    ("Dividend growth rate",                       "~8%",    "<5%",   "-3pp",   "Capital allocation shifts toward elevated capex/M&A funding"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A sustained rise in interest rates compresses AWK's bond-proxy multiple just as the")
print(f"  M&A pipeline stalls and rate case outcomes disappoint across multiple states.")
print(f"  EPS falls to ~$5.00; multiple compresses to 18x distress P/E = ${bear_price}.")

# ─── ③ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS x min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}")
print(f"  Min viable P/E at trough:      {PE_TROUGH}x  (bond-proxy rate-shock distress multiple)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct>=0 else 'below'} trough floor)")
print()
print(f"  Premium to EPP reflects the long M&A tuck-in runway and visible infrastructure-replacement-driven rate base growth.")
print(f"  Bear ${bear_price} is below EPP ${EPP:.0f} — would require both EPS pressure AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+0.45:.2f} x {PE_TROUGH}x = ${(EPP_EPS+0.45)*PE_TROUGH:.0f} EPP — rate base growth compounds the floor higher.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: rate base growth moderate, M&A tuck-in pace continues)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (rate base growth + M&A tuck-in contribution)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (slightly below current)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (~8%/yr dividend growth)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — the ~2.1% dividend yield plus steady")
print(f"  rate base growth and the M&A tuck-in pipeline support total returns even in a soft macro.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.13
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (typical for a bond-proxy regulated water utility)")
print(f"  Beta vs S&P 500:      0.40  (below market; defensive but rate-sensitive)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (AWK fell ~13% during prior rate-shock episodes; tail risk, not base case)")
print(f"  -> M&A tuck-in pace and multi-state rate case outcomes are the PRIMARY catalysts;")
print(f"     accelerating acquisitions + constructive rate cases = upside; stalled deals + rate setbacks + rising rates = downside.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — upper-middle of range; reflects bond-proxy sensitivity to rate expectations.")
print(f"  -> BUY $125-$131  |  TRIM $152+  |  AVOID above $164")

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
    print(f"  {s:<10}  ${pr:>5}  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): ${ev_adj:.0f}  /  Proxy EV: ${ev_prx:.0f}  /  Market EV: ${ev_mkt:.0f}  /  Current: ${CURRENT_PRICE:.0f}")
hr()
print(f"  Downside  (-> Bear ${bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (-> Bull ${bull_price}):   {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b:.2f}x")
print(f"  Signal    :  {signal_full}")
print()
print(f"  Market composite {MARKET_COMPOSITE:.2f} reflects pricing roughly between BASE and BULL")
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees the M&A tuck-in growth runway + infrastructure capex plan, tempered by rate-sensitivity/PFAS SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing the M&A tuck-in growth story.' if ADJ_GAP>0 else 'model roughly agrees with market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) M&A tuck-in growth -> regulated system acquisitions continue at pace")
print(f"  (2) Regulatory ROE -> constructive multi-state rate case outcomes")
print(f"  (3) Infrastructure replacement capex -> lead service line and main replacement program stays on/ahead of pace")
print(f"  (4) MSG contracts -> military base privatization contracts renew and expand")
print(f"  BUY $125-{round(CURRENT_PRICE*0.90,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $152  |  AVOID above $164")
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
