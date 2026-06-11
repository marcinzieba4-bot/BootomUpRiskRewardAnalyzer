"""
CEG  ·  Constellation Energy Corporation  ·  NASDAQ: CEG
Bottom-up signal model  ·  Largest US Nuclear Fleet · Carbon-Free Baseload · AI/Data-Center Power Demand
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "CEG"
COMPANY       = "Constellation Energy Corporation"
SECTOR        = "Independent Power Producer · Nuclear Fleet · NASDAQ: CEG"
CURRENT_PRICE = 310.00     # USD; as of 2026-06-11
VOL_52W_LOW   = 220.00
VOL_52W_HIGH  = 380.00
SHARES_OUT_M  = 310.0      # millions

# Dividend
ANNUAL_DIV    = 1.00       # $/share; modest yield, capital prioritized toward growth/buybacks

# ── DATA-CENTER PPA / NUCLEAR CAPACITY ANALYSIS (company-specific) ────────────
CONTRACTED_CAPACITY_GROWTH = 0.18   # ~18% YoY growth in long-duration data-center/hyperscaler PPAs
NUCLEAR_CAPACITY_FACTOR    = 0.945  # fleet-wide nuclear capacity factor
INCREMENTAL_MARGIN         = 0.50   # incremental margin on contracted PPA volumes (existing baseload assets)
TAX_RATE                   = 0.21

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 10.50   # FY2026E adj EPS
PE_TROUGH = 18      # min P/E at crisis trough (pre-AI-rerating IPP multiple)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $189

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (8.00,  18,  144, "AI/data-center demand narrative stalls; power prices fall; nuclear PTC policy support weakens; EPS $8.00 -> 18x distress P/E"),
    "BASE":  (10.50, 30,  315, "Long-duration hyperscaler PPAs continue to be signed at premium pricing; nuclear fleet runs at ~94-95% capacity factor; EPS $10.50 -> 30x P/E"),
    "BULL":  (13.00, 34,  442, "Contracted data-center capacity accelerates beyond plan; power price capture rates improve; EPS $13.00 -> 34x premium P/E"),
    "XBULL": (16.00, 38,  608, "Multi-year AI buildout supercycle locks in a large share of the nuclear fleet under premium long-term PPAs; EPS $16.00 -> 38x peak P/E"),
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
        "name":       "Contracted data-center/hyperscaler PPA capacity — YoY growth",
        "weight":     0.25,
        "thresholds": ("<5%",   "≥10%",  "≥15%",  "≥25%"),
        "now":        "~18%",
        "score":      3,
        "comment":    "~18%; long-duration agreements with hyperscalers (incl. restarted Crane Clean Energy Center) lock in premium pricing",
    },
    {
        "name":       "Power price realization (capture rate vs PJM/ERCOT)",
        "weight":     0.15,
        "thresholds": ("<90%",  "≥95%",  "≥100%", "≥105%"),
        "now":        "~98%",
        "score":      2,
        "comment":    "~98%; hedging program smooths near-term realized prices below spot during volatile periods",
    },
    {
        "name":       "Clean energy / nuclear PTC policy support",
        "weight":     0.15,
        "thresholds": ("negative", "neutral", "supportive", "highly supportive"),
        "now":        "supportive",
        "score":      3,
        "comment":    "supportive; existing nuclear PTC framework underpins baseload economics through the decade",
    },
    {
        "name":       "Nuclear fleet capacity factor",
        "weight":     0.15,
        "thresholds": ("<90%",  "≥92%",  "≥94%",  "≥96%"),
        "now":        "~94.5%",
        "score":      3,
        "comment":    "~94.5%; industry-leading uptime across the largest US nuclear fleet",
    },
    {
        "name":       "Adjusted EPS growth rate",
        "weight":     0.15,
        "thresholds": ("<5%",   "≥10%",  "≥15%",  "≥20%"),
        "now":        "~15%",
        "score":      3,
        "comment":    "~15%; PPA repricing and contracted capacity additions drive above-utility-average growth",
    },
    {
        "name":       "Leverage / deleveraging (net debt / EBITDA)",
        "weight":     0.15,
        "thresholds": (">2.5x", "≤2.5x", "≤2.0x", "≤1.5x"),
        "now":        "~2.2x",
        "score":      2,
        "comment":    "~2.2x; balance sheet investment-grade but capex for plant uprates/restarts limits faster deleveraging",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Largest US carbon-free nuclear fleet is uniquely positioned to supply 24/7 baseload power for AI data centers", +0.6, 0.25),
    ("+", "Long-duration hyperscaler PPAs (Microsoft, etc.) lock in premium pricing and de-risk multi-year cash flows",      +0.4, 0.20),
    ("+", "Existing nuclear PTC framework provides a durable policy floor for plant economics",                              +0.2, 0.15),
    ("-", "Regulatory/political risk — changes to nuclear subsidies, PTC framework, or PPA approvals could compress economics", -0.4, 0.20),
    ("-", "Valuation already reflects a significant AI-driven re-rating, leaving limited margin of safety if the narrative stalls", -0.4, 0.20),
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
CONS_EPS_2YR = 13.50   # conservative FY2028E: PPA repricing + contracted capacity additions continue
CONS_PE_2YR  = 27       # floor multiple (slightly below current)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Nuclear Fleet / AI Power Demand")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PPA / NUCLEAR CAPACITY ANALYSIS ───────────────────────────────────────
print()
print("  CONTRACTED PPA + NUCLEAR CAPACITY ANALYSIS  (the core CEG earnings drivers)")
hr()
shares_b = SHARES_OUT_M / 1000
total_revenue_b = 24.0
print(f"  Estimated FY2026E revenue base: ~${total_revenue_b:.1f}B")
print()
print(f"  CONTRACTED PPA UPSIDE  (incremental EPS from PPA capacity growth at {INCREMENTAL_MARGIN*100:.0f}% incremental margin):")
print(f"  {'Contracted capacity growth':<20}  {'Rev/yr ($B)':>12}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.00, 0.10, 0.15, 0.25]:
    rev_inc = total_revenue_b * g
    inc_eps = rev_inc * INCREMENTAL_MARGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% PPA capacity growth     +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
print(f"  NUCLEAR FLEET CAPACITY FACTOR  (~{NUCLEAR_CAPACITY_FACTOR*100:.1f}%; every 1pp of uptime improvement")
print(f"  across the ~32GW fleet adds incremental high-margin generation with no new capex).")
print()
print(f"  BEAR (${bear_price}) requires: the AI/data-center demand narrative stalls, power prices fall,")
print(f"  AND nuclear PTC policy support weakens — together.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (PPA growth + price realization + PTC policy + capacity factor + EPS growth + leverage)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>10}  {'BASE':>8}  {'BULL':>11}  {'XBULL':>18}  {'NOW':>10}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>10}  {ths[1]:>8}  {ths[2]:>11}  {ths[3]:>18}  {s['now']:>10}  {lbl}  {b}")

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
    ("Contracted PPA capacity growth",             "~18%",   "<5%",   "-13pp",  "Hyperscaler capex pullback slows new PPA signings"),
    ("Power price realization",                    "~98%",   "<90%",  "-8pp",   "Sustained low natural gas prices depress wholesale power prices"),
    ("Nuclear PTC policy support",                 "supportive", "negative", "reversal", "Policy shift weakens or repeals nuclear production tax credits"),
    ("Nuclear fleet capacity factor",              "~94.5%", "<90%",  "-4.5pp", "Unplanned outages or extended refueling cycles reduce uptime"),
    ("Adjusted EPS growth",                        "~15%",   "<5%",   "-10pp",  "Lower power prices and slower PPA growth compress earnings growth"),
    ("Leverage (net debt/EBITDA)",                 "~2.2x",  ">2.5x", "+0.3x",  "Capex for plant uprates/restarts outpaces deleveraging"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: The AI/data-center demand narrative stalls and hyperscaler capex pulls back,")
print(f"  while sustained low power prices and weakening nuclear PTC support compress baseload economics.")
print(f"  EPS falls to ~$8.00; multiple compresses to 18x distress P/E = ${bear_price}.")

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
print(f"  Premium to EPP reflects the AI/data-center power demand re-rating of carbon-free nuclear baseload.")
print(f"  Bear ${bear_price} is below EPP ${EPP:.0f} — would require both EPS pressure AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+1.50:.2f} x {PE_TROUGH}x = ${(EPP_EPS+1.5)*PE_TROUGH:.0f} EPP — PPA repricing compounds the floor higher.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: PPA repricing + contracted capacity additions continue)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (PPA repricing + contracted capacity additions)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (slightly below current)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f} x 2)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — long-duration PPA contracts already signed")
print(f"  provide multi-year revenue visibility even if new contracting slows from current pace.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.35
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (well above-market; AI-power-demand sentiment swings)")
print(f"  Beta vs S&P 500:      1.10  (above market for a power producer; AI-narrative sensitive)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (CEG has seen 30%+ drawdowns on AI-capex sentiment shifts; tail risk, not base case)")
print(f"  -> Hyperscaler PPA signings and power price trends are the PRIMARY catalysts;")
print(f"     continued PPA growth = upside; AI capex pullback or PTC policy reversal = downside.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — mid range; reflects volatile AI-power-demand sentiment.")
print(f"  -> BUY $235-$255  |  TRIM $360+  |  AVOID above $400")

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
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees nuclear/AI-power demand growth, tempered by policy/valuation SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing the nuclear AI-power story.' if ADJ_GAP>0 else 'model is cautious relative to market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) Contracted PPA capacity -> sustained >=15% growth confirms hyperscaler demand")
print(f"  (2) Power price realization -> capture rates trend toward 100%+")
print(f"  (3) Nuclear PTC policy -> continued federal support locks in baseload economics")
print(f"  (4) Nuclear fleet capacity factor -> sustained >=94% confirms operational excellence")
print(f"  BUY $235-{round(CURRENT_PRICE*0.90,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $360  |  AVOID above $400")
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
