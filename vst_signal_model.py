"""
VST  ·  Vistra Corp.  ·  NYSE: VST
Bottom-up signal model  ·  Diversified IPP (Nuclear/Gas/Renewables) + Retail · ERCOT/PJM AI Power Demand
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "VST"
COMPANY       = "Vistra Corp."
SECTOR        = "Independent Power Producer · Nuclear/Gas/Renewables + Retail · NYSE: VST"
CURRENT_PRICE = 190.00     # USD; as of 2026-06-11
VOL_52W_LOW   = 90.00
VOL_52W_HIGH  = 220.00
SHARES_OUT_M  = 340.0      # millions

# Dividend
ANNUAL_DIV    = 0.88       # $/share; modest yield, capital prioritized toward buybacks/growth

# ── CONTRACTED CAPACITY / GENERATION FLEET ANALYSIS (company-specific) ────────
CONTRACTED_CAPACITY_GROWTH = 0.15   # ~15% YoY growth in contracted/hedged data-center-linked capacity
NUCLEAR_CAPACITY_FACTOR    = 0.96   # Comanche Peak nuclear capacity factor
INCREMENTAL_MARGIN         = 0.48   # incremental margin on contracted volumes (existing fleet)
TAX_RATE                   = 0.21
BUYBACK_PCT                = 0.07   # ~7%/yr share count reduction

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 7.50    # FY2026E adj EPS
PE_TROUGH = 10      # min P/E at crisis trough (pre-AI-rerating IPP multiple)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $75

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (5.50, 10,   55,  "AI/data-center demand narrative stalls; ERCOT power prices fall sharply; leverage stress amid a downturn; EPS $5.50 -> 10x distress P/E"),
    "BASE":  (7.50, 25,  188, "Contracted data-center capacity continues to grow; nuclear fleet runs at ~95-96% capacity factor; buybacks compound EPS; EPS $7.50 -> 25x P/E"),
    "BULL":  (10.00, 28, 280, "Contracted capacity for data centers accelerates beyond plan; ERCOT/PJM power price capture improves; EPS $10.00 -> 28x premium P/E"),
    "XBULL": (12.50, 32, 400, "Multi-year AI buildout supercycle locks in a large share of the diversified fleet under premium long-term contracts; EPS $12.50 -> 32x peak P/E"),
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
        "name":       "Contracted/hedged data-center-linked capacity — YoY growth",
        "weight":     0.25,
        "thresholds": ("<5%",   "≥10%",  "≥15%",  "≥25%"),
        "now":        "~15%",
        "score":      3,
        "comment":    "~15%; agreements to supply large load customers (incl. data centers) from existing nuclear/gas fleet are growing",
    },
    {
        "name":       "ERCOT/PJM power price realization (capture rate)",
        "weight":     0.15,
        "thresholds": ("<85%",  "≥90%",  "≥95%",  "≥100%"),
        "now":        "~92%",
        "score":      2,
        "comment":    "~92%; hedging program smooths near-term realized prices below spot during volatile periods",
    },
    {
        "name":       "Nuclear (Comanche Peak) capacity factor",
        "weight":     0.15,
        "thresholds": ("<90%",  "≥92%",  "≥95%",  "≥97%"),
        "now":        "~96%",
        "score":      3,
        "comment":    "~96%; Comanche Peak continues to run at industry-leading uptime, anchoring baseload economics",
    },
    {
        "name":       "Retail electricity segment margin",
        "weight":     0.15,
        "thresholds": ("<5%",   "≥7%",   "≥9%",   "≥12%"),
        "now":        "~8%",
        "score":      2,
        "comment":    "~8%; retail margins remain healthy but competitive intensity in Texas/PJM retail markets caps upside",
    },
    {
        "name":       "Free cash flow / buyback pace (% of shares retired/yr)",
        "weight":     0.15,
        "thresholds": ("<3%",   "≥5%",   "≥7%",   "≥10%"),
        "now":        "~7%",
        "score":      3,
        "comment":    "~7%/yr; strong free cash flow generation funds an aggressive, ongoing buyback program",
    },
    {
        "name":       "Leverage (net debt / EBITDA)",
        "weight":     0.15,
        "thresholds": (">3.5x", "≤3.5x", "≤3.0x", "≤2.5x"),
        "now":        "~3.2x",
        "score":      2,
        "comment":    "~3.2x; balance sheet investment-grade but capex/buybacks limit faster deleveraging",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Diversified generation fleet (nuclear/gas/renewables/storage) across ERCOT and PJM is well-positioned to supply AI/data-center load", +0.5, 0.25),
    ("+", "Aggressive ~7%/yr buyback funded by strong free cash flow compounds per-share value",                                                     +0.4, 0.20),
    ("+", "Vertically integrated retail business provides a natural hedge against wholesale power price swings",                                    +0.2, 0.15),
    ("-", "ERCOT/PJM power price and weather volatility (e.g., extreme winter/summer events) create earnings swings",                               -0.4, 0.20),
    ("-", "Valuation already reflects a significant AI-driven re-rating, leaving limited margin of safety if the narrative stalls",                  -0.4, 0.20),
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
CONS_EPS_2YR = 9.50    # conservative FY2028E: contracted capacity growth + buyback compounding continue
CONS_PE_2YR  = 22       # floor multiple (slightly below current)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Diversified IPP / AI Power Demand")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① CONTRACTED CAPACITY / FLEET ANALYSIS ──────────────────────────────────
print()
print("  CONTRACTED CAPACITY + GENERATION FLEET ANALYSIS  (the core VST earnings drivers)")
hr()
shares_b = SHARES_OUT_M / 1000
total_revenue_b = 18.0
print(f"  Estimated FY2026E revenue base: ~${total_revenue_b:.1f}B")
print()
print(f"  CONTRACTED CAPACITY UPSIDE  (incremental EPS from contracted growth at {INCREMENTAL_MARGIN*100:.0f}% incremental margin):")
print(f"  {'Contracted capacity growth':<20}  {'Rev/yr ($B)':>12}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.00, 0.10, 0.15, 0.25]:
    rev_inc = total_revenue_b * g
    inc_eps = rev_inc * INCREMENTAL_MARGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% capacity growth         +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
print(f"  BUYBACK COMPOUNDING  (~{BUYBACK_PCT*100:.0f}%/yr share count reduction directly boosts EPS,")
print(f"  funded by strong free cash flow from the existing nuclear/gas/renewables fleet).")
print()
print(f"  BEAR (${bear_price}) requires: the AI/data-center demand narrative stalls, ERCOT power prices")
print(f"  fall sharply, AND leverage stress emerges in a downturn — together.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (contracted capacity + price realization + nuclear CF + retail margin + FCF/buyback + leverage)")
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
    ("Contracted data-center-linked capacity growth", "~15%", "<5%",   "-10pp",  "Hyperscaler capex pullback slows new contract signings"),
    ("ERCOT/PJM power price realization",          "~92%",   "<85%",  "-7pp",   "Mild weather and oversupply depress wholesale power prices"),
    ("Nuclear (Comanche Peak) capacity factor",    "~96%",   "<90%",  "-6pp",   "Unplanned outage or extended refueling cycle reduces uptime"),
    ("Retail electricity segment margin",          "~8%",    "<5%",   "-3pp",   "Increased retail competition compresses customer margins"),
    ("Free cash flow / buyback pace",              "~7%",    "<3%",   "-4pp",   "Lower power prices reduce free cash flow available for buybacks"),
    ("Leverage (net debt/EBITDA)",                 "~3.2x",  ">3.5x", "+0.3x",  "Lower EBITDA in a downturn pushes leverage above target range"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: The AI/data-center demand narrative stalls and hyperscaler capex pulls back,")
print(f"  while mild weather and oversupply depress ERCOT/PJM power prices and pressure leverage.")
print(f"  EPS falls to ~$5.50; multiple compresses to 10x distress P/E = ${bear_price}.")

# ─── ③ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS x min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}")
print(f"  Min viable P/E at trough:      {PE_TROUGH}x  (pre-AI-rerating IPP multiple)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct>=0 else 'below'} trough floor)")
print()
print(f"  Premium to EPP reflects the AI/data-center power demand re-rating of the diversified generation fleet.")
print(f"  Bear ${bear_price} is below EPP ${EPP:.0f} — would require both EPS pressure AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+1.00:.2f} x {PE_TROUGH}x = ${(EPP_EPS+1.0)*PE_TROUGH:.0f} EPP — contracted capacity growth and buybacks compound the floor higher.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: contracted capacity growth + buyback compounding continue)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (contracted capacity growth + ~7%/yr buybacks)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (slightly below current)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f} x 2)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — long-duration contracts already signed plus")
print(f"  buyback-driven share count reduction support EPS even if new contracting slows from current pace.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.40
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (well above-market; AI-power-demand sentiment + commodity swings)")
print(f"  Beta vs S&P 500:      1.30  (above market for a power producer; AI-narrative and commodity sensitive)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (VST has seen 50%+ drawdowns on commodity/AI-sentiment shifts; tail risk, not base case)")
print(f"  -> Contracted capacity signings and ERCOT/PJM power price trends are the PRIMARY catalysts;")
print(f"     continued contracting + firm prices = upside; AI capex pullback or commodity glut = downside.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — mid range; reflects volatile AI-power-demand sentiment.")
print(f"  -> BUY $135-$150  |  TRIM $210+  |  AVOID above $235")

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
print(f"  Downside  (-> Bear ${bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (-> Bull ${bull_price}):   {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b:.2f}x")
print(f"  Signal    :  {signal_full}")
print()
print(f"  Market composite {MARKET_COMPOSITE:.2f} reflects pricing roughly between BASE and BULL")
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees diversified-fleet AI power demand growth, tempered by commodity/valuation SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing the diversified-fleet AI power story.' if ADJ_GAP>0 else 'model is cautious relative to market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) Contracted data-center-linked capacity -> sustained >=15% growth confirms hyperscaler demand")
print(f"  (2) ERCOT/PJM power price realization -> capture rates trend toward 95-100%")
print(f"  (3) Nuclear (Comanche Peak) capacity factor -> sustained >=95% confirms operational excellence")
print(f"  (4) Buyback pace -> sustained >=7%/yr drives per-share EPS compounding")
print(f"  BUY $135-{round(CURRENT_PRICE*0.90,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $210  |  AVOID above $235")
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
