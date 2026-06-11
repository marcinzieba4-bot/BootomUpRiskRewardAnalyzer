"""
ABNB  ·  Airbnb, Inc.  ·  NASDAQ: ABNB
Bottom-up signal model  ·  Travel · Asset-Light Marketplace · Alternative Accommodations
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "ABNB"
COMPANY       = "Airbnb, Inc."
SECTOR        = "Travel · Asset-Light Marketplace · NASDAQ: ABNB"
CURRENT_PRICE = 130.00     # USD; as of 2026-06-11
VOL_52W_LOW   = 95.00
VOL_52W_HIGH  = 170.00
SHARES_OUT_M  = 410.0      # millions; ongoing buyback

# Dividend
ANNUAL_DIV    = 0.00       # $/share; no dividend, all capital returned via buybacks

# ── GBV / NIGHTS GROWTH ANALYSIS (company-specific) ───────────────────────────
GBV_GROWTH       = 0.11    # ~11% YoY Gross Booking Value growth
TAKE_RATE        = 0.183   # revenue / GBV
INCREMENTAL_MGIN = 0.55    # incremental operating margin on revenue growth (asset-light)
TAX_RATE         = 0.21

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 4.20    # FY2026E adj EPS
PE_TROUGH = 15      # min P/E at crisis trough (post-IPO/COVID-era distress multiple)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $63

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (3.00, 15,  45,  "Global travel slump + regulatory crackdowns on short-term rentals; EPS $3.00 -> 15x distress P/E"),
    "BASE":  (4.50, 30,  135, "GBV +9-11%; take rate stable; buybacks compound EPS; EPS $4.50 -> 30x P/E"),
    "BULL":  (5.50, 35,  193, "Experiences/new-category expansion accelerates growth; take rate expands; EPS $5.50 -> 35x premium P/E"),
    "XBULL": (7.00, 40,  280, "Multi-year alternative-accommodation share gains globally; EPS $7.00 -> 40x peak P/E"),
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
        "name":       "Gross Booking Value — YoY growth",
        "weight":     0.25,
        "thresholds": ("<5%",   "≥8%",   "≥10%",  "≥13%"),
        "now":        "~11%",
        "score":      3,
        "comment":    "~11% YoY; resilient demand for alternative accommodations across core markets",
    },
    {
        "name":       "Nights & Experiences booked — YoY growth",
        "weight":     0.15,
        "thresholds": ("<5%",   "≥7%",   "≥9%",   "≥12%"),
        "now":        "~9%",
        "score":      3,
        "comment":    "~9%; cross-border travel and emerging-market expansion drive unit growth",
    },
    {
        "name":       "Take rate (revenue / GBV)",
        "weight":     0.15,
        "thresholds": ("<17%",  "≥18%",  "≥18.5%", "≥19.5%"),
        "now":        "~18.3%",
        "score":      2,
        "comment":    "~18.3%; modest mix-driven uplift from host fee adjustments and ad/services attach",
    },
    {
        "name":       "Free cash flow margin",
        "weight":     0.20,
        "thresholds": ("<25%",  "≥30%",  "≥35%",   "≥40%"),
        "now":        "~35%",
        "score":      3,
        "comment":    "~35%; capital-light marketplace model converts revenue growth into cash at high rates",
    },
    {
        "name":       "Non-core/international market mix",
        "weight":     0.10,
        "thresholds": ("<40%",  "≥43%",  "≥46%",   "≥50%"),
        "now":        "~45%",
        "score":      3,
        "comment":    "~45%; geographic diversification reduces reliance on any single regulatory regime",
    },
    {
        "name":       "Buyback pace (% of shares retired/yr)",
        "weight":     0.15,
        "thresholds": ("<2%",   "≥3%",   "≥4%",    "≥6%"),
        "now":        "~4%",
        "score":      3,
        "comment":    "~4%/yr; large net cash position funds aggressive, ongoing share repurchases",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Asset-light two-sided marketplace with strong network effects — supply (listings) and demand reinforce each other globally", +0.5, 0.25),
    ("+", "Net-cash balance sheet with no debt funds large, ongoing buybacks that compound per-share value",                            +0.4, 0.20),
    ("+", "Expansion into experiences/services adds optionality for future GBV and take-rate growth",                                  +0.3, 0.15),
    ("-", "Regulatory risk — short-term rental restrictions in major cities (NYC, Barcelona, etc.) cap supply growth in key markets",   -0.5, 0.20),
    ("-", "Competitive pressure from Booking.com/Vrbo and hotel chains expanding into alternative accommodations",                       -0.3, 0.20),
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
CONS_EPS_2YR = 5.50    # conservative FY2028E: GBV growth + buyback compounding continues
CONS_PE_2YR  = 28       # floor multiple (slightly below current)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Travel / Asset-Light Marketplace")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① GBV / NIGHTS GROWTH ANALYSIS ──────────────────────────────────────────
print()
print("  GBV GROWTH ANALYSIS  (the core ABNB earnings driver)")
hr()
shares_b = SHARES_OUT_M / 1000
total_revenue_b = 12.0
print(f"  Estimated FY2026E revenue base: ~${total_revenue_b:.1f}B")
print()
print(f"  GBV GROWTH UPSIDE  (incremental EPS from GBV growth at {INCREMENTAL_MGIN*100:.0f}% incremental margin):")
print(f"  {'GBV YoY growth':<20}  {'Rev/yr ($B)':>12}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.00, 0.08, 0.11, 0.15]:
    rev_inc = total_revenue_b * g
    inc_eps = rev_inc * INCREMENTAL_MGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% GBV growth            +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
print(f"  TAKE RATE  (~{TAKE_RATE*100:.1f}% of GBV; modest mix-driven expansion adds directly to revenue")
print(f"  with no incremental supply cost — capital-light marketplace model maximizes drop-through).")
print()
print(f"  BEAR (${bear_price}) requires: a global travel slump combined with regulatory crackdowns on")
print(f"  short-term rentals in major markets AND multiple compresses to distress levels — together.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (GBV growth + nights + take rate + FCF margin + intl mix + buybacks)")
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
    ("Gross Booking Value YoY",                    "~11%",   "<5%",   "-6pp",   "Global recession curtails discretionary travel spend"),
    ("Nights & Experiences growth",                "~9%",    "<5%",   "-4pp",   "Booking volume growth stalls as travel demand softens"),
    ("Take rate",                                  "~18.3%", "<17%",  "-1.3pp", "Competitive pricing pressure forces fee reductions"),
    ("Free cash flow margin",                      "~35%",   "<25%",  "-10pp",  "Marketing spend rises sharply to defend market share"),
    ("Non-core/international mix",                 "~45%",   "<40%",  "-5pp",   "Regulatory bans force exit from key international markets"),
    ("Buyback pace (%/yr)",                        "~4%",    "<2%",   "-2pp",   "Cash deployed defensively; capital return slows"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A global recession sharply curtails discretionary travel spend while regulatory")
print(f"  crackdowns on short-term rentals in major cities cap supply growth in key markets.")
print(f"  EPS falls to ~$3.00; multiple compresses to 15x distress P/E = ${bear_price}.")

# ─── ③ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS x min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}")
print(f"  Min viable P/E at trough:      {PE_TROUGH}x  (post-COVID-era distress multiple)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct>=0 else 'below'} trough floor)")
print()
print(f"  Premium to EPP reflects asset-light marketplace moat, net-cash balance sheet, and ongoing buybacks.")
print(f"  Bear ${bear_price} is below EPP ${EPP:.0f} — would require both EPS collapse AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+0.50:.2f} x {PE_TROUGH}x = ${(EPP_EPS+0.5)*PE_TROUGH:.0f} EPP — buybacks compound the floor higher.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: GBV growth moderate, buyback compounding continues)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (mid-single-digit GBV growth + ~4%/yr buybacks)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (slightly below current)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (no dividend)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — buyback-driven share count reduction plus")
print(f"  steady GBV growth and high FCF conversion support EPS compounding even in a soft macro.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.32
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (no dividend; capital returned via buybacks)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (above-market; growth/travel-cyclical exposure)")
print(f"  Beta vs S&P 500:      1.30  (above market; growth/cyclical)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (post-IPO ABNB has fallen ~50%+ from highs in past drawdowns; tail risk, not base case)")
print(f"  -> Global travel demand trajectory and regulatory environment are the PRIMARY catalysts;")
print(f"     resilient travel = upside; recession/regulatory shock = -50%+ downside.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — mid range; not stretched relative to growth profile.")
print(f"  -> BUY $100-$110  |  TRIM $160+  |  AVOID above $180")

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
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees GBV growth + buyback compounding, tempered by regulatory/competitive SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing the asset-light marketplace compounding story.' if ADJ_GAP>0 else 'model roughly agrees with market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) GBV growth -> sustained >=10% confirms travel demand resilience")
print(f"  (2) Nights & Experiences growth -> booking volume growth stays >=9%/yr")
print(f"  (3) Take rate -> mix-driven expansion confirms monetization upside")
print(f"  (4) Free cash flow margin -> sustained >=35% funds aggressive buybacks")
print(f"  BUY $100-{round(CURRENT_PRICE*0.90,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $160  |  AVOID above $180")
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
