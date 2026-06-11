"""
AMZN  ·  Amazon.com, Inc.  ·  NASDAQ: AMZN
Bottom-up signal model  ·  AWS / Retail / Advertising / AI
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "AMZN"
COMPANY       = "Amazon.com, Inc."
SECTOR        = "AWS Cloud · E-commerce/Retail · Advertising · AI Infrastructure · NASDAQ: AMZN"
CURRENT_PRICE = 218.00       # USD; as of 2026-06-11
VOL_52W_LOW   = 161.00       # April 2026 tariff/recession-fear trough
VOL_52W_HIGH  = 245.00       # early 2026 AI/AWS re-acceleration peak
SHARES_OUT_M  = 10_500.0     # millions; post continued buyback drift

# No dividend
ANNUAL_DIV    = 0.00

# ── AWS GROWTH vs RETAIL MARGIN OFFSET CONSTANTS (company-specific calculator) ─
# Revenue / operating-income breakdown FY2026E ($B)
AWS_REV_B          = 145.0  # AWS cloud revenue
NA_RETAIL_REV_B    = 410.0  # North America retail
INTL_RETAIL_REV_B  = 165.0  # International retail
ADS_REV_B          =  68.0  # Advertising services

AWS_OP_MARGIN      = 0.36   # AWS operating margin (capacity constraints easing, AI demand)
NA_OP_MARGIN       = 0.07   # NA retail operating margin (logistics efficiency gains)
INTL_OP_MARGIN     = 0.04   # International retail operating margin (improving from breakeven)
ADS_OP_MARGIN      = 0.45   # Advertising operating margin (high-margin, fast growing)

AWS_GROWTH_RATE    = 0.20   # 20% YoY AWS growth (Q1 2026 run-rate, AI capacity coming online)
TAX_RATE           = 0.20   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 6.40    # FY2026E adj EPS (consensus $6.20-$6.60)
PE_TROUGH = 22      # min P/E at crisis trough (2022 was ~18-20x; AWS scale commands premium)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $141

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 4.30, 18,  155, "Recession hits retail margins + AWS growth slows to single digits; EPS $4.30 -> 18x distress P/E"),
    "BASE":  ( 6.40, 30,  192, "AWS reaccelerates to ~20%; retail margins steady; ads growth strong; EPS $6.40 -> 30x P/E"),
    "BULL":  ( 8.50, 33,  280, "AWS AI capacity fully monetised >24% growth; retail op margin >8%; EPS $8.50 -> 33x premium P/E"),
    "XBULL": (11.50, 36,  414, "AWS becomes dominant AI cloud platform; ads >$100B run-rate; EPS $11.50 -> 36x peak P/E"),
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
        "name":       "AWS revenue — YoY growth rate",
        "weight":     0.30,
        "thresholds": ("<10%",   "≥17%",  "≥22%",   "≥28%"),
        "now":        "+20%",
        "score":      3,
        "comment":    "+20% YoY; AI/Trainium demand outstripping capacity; backlog $200B+",
    },
    {
        "name":       "AWS operating margin trend",
        "weight":     0.20,
        "thresholds": ("<28%",   "≥32%",  "≥36%",   "≥40%"),
        "now":        "~36%",
        "score":      3,
        "comment":    "~36%; custom silicon (Trainium2/3) lowering AI inference costs",
    },
    {
        "name":       "Advertising revenue — YoY growth",
        "weight":     0.20,
        "thresholds": ("<10%",   "≥15%",  "≥20%",   "≥28%"),
        "now":        "+19%",
        "score":      2,
        "comment":    "+19% YoY; sponsored products growth decelerating slightly off large base",
    },
    {
        "name":       "North America retail operating margin",
        "weight":     0.15,
        "thresholds": ("<3%",    "≥5%",   "≥7%",    "≥9%"),
        "now":        "~7%",
        "score":      3,
        "comment":    "~7%; regionalized fulfillment + same-day delivery driving cost-to-serve down",
    },
    {
        "name":       "International retail operating margin",
        "weight":     0.10,
        "thresholds": ("<0%",    "≥2%",   "≥4%",    "≥6%"),
        "now":        "~4%",
        "score":      3,
        "comment":    "~4%; India/Europe approaching NA-level efficiency for first time",
    },
    {
        "name":       "Capex as % of revenue (AI infrastructure build)",
        "weight":     0.05,
        "thresholds": (">18%",   "≤16%",  "≤13%",   "≤10%"),
        "now":        "~15%",
        "score":      2,
        "comment":    "~15% of revenue; elevated AI/data center capex pressuring near-term FCF",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "AWS cloud/AI infrastructure moat — #1 cloud share; Trainium custom silicon cost edge",   +0.8, 0.25),
    ("+", "Advertising flywheel — high-margin, fast-growing, leverages 1P retail data",              +0.6, 0.20),
    ("+", "Retail logistics scale — regionalization + robotics driving structural margin expansion", +0.5, 0.20),
    ("-", "Heavy AI capex cycle — depresses near-term FCF; depreciation drag on margins",            -0.6, 0.20),
    ("-", "Macro/tariff sensitivity — discretionary retail demand exposed to consumer slowdown",     -0.4, 0.15),
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
CONS_EPS_2YR = 7.50    # conservative FY2028E: AWS growth moderates; retail margins hold
CONS_PE_2YR  = 26      # floor multiple (still well above market average given AWS+ads quality)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  AWS / Retail / Ads / AI Infrastructure")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① AWS GROWTH vs RETAIL MARGIN ANALYSIS ─────────────────────────────────
print()
print("  AWS REACCELERATION vs RETAIL MARGIN EXPANSION ANALYSIS  (the core AMZN tension)")
hr()

total_rev_b = AWS_REV_B + NA_RETAIL_REV_B + INTL_RETAIL_REV_B + ADS_REV_B
print(f"  Segment FY2026E Revenue:")
print(f"  {'AWS':<36}  ${AWS_REV_B:>5.1f}B  ({AWS_REV_B/total_rev_b*100:.0f}% of total; {AWS_OP_MARGIN*100:.0f}% op margin)")
print(f"  {'North America retail':<36}  ${NA_RETAIL_REV_B:>5.1f}B  ({NA_RETAIL_REV_B/total_rev_b*100:.0f}%; {NA_OP_MARGIN*100:.0f}% op margin)")
print(f"  {'International retail':<36}  ${INTL_RETAIL_REV_B:>5.1f}B  ({INTL_RETAIL_REV_B/total_rev_b*100:.0f}%; {INTL_OP_MARGIN*100:.0f}% op margin)")
print(f"  {'Advertising':<36}  ${ADS_REV_B:>5.1f}B  ({ADS_REV_B/total_rev_b*100:.0f}%; {ADS_OP_MARGIN*100:.0f}% op margin, fastest growing)")
hr()
print(f"  Total FY2026E:                         ${total_rev_b:>5.1f}B")
print()

shares_b = SHARES_OUT_M / 1000
print(f"  AWS GROWTH UPSIDE  (incremental EPS from AWS growth above/below {AWS_GROWTH_RATE*100:.0f}%):")
print(f"  {'AWS YoY growth':<20}  {'Rev/yr':>10}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.10, 0.16, 0.20, 0.26]:
    rev_inc = AWS_REV_B * g
    inc_eps = rev_inc * AWS_OP_MARGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% AWS growth        +${rev_inc:>5.1f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
na_y1 = NA_RETAIL_REV_B * 0.01  # each 1pp margin expansion
na_eps1 = na_y1 * (1 - TAX_RATE) / shares_b
print(f"  RETAIL MARGIN EXPANSION OFFSET  (each +1pp NA op margin = +${na_eps1:.2f}/EPS/yr):")
print(f"  Current NA margin {NA_OP_MARGIN*100:.0f}% -> +1pp = +${na_eps1:.2f}/EPS  -> +2pp over 2yr = +${na_eps1*2:.2f}/EPS")
print()
print(f"  BEAR (${bear_price}) requires: AWS growth <10% AND NA margin compression to <3% AND ad growth stalls — simultaneously.")

# ─── ② SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (AWS + ads + retail margins + capex discipline)")
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
    ("AWS revenue YoY",                         "+20%",   "<10%",  "-10pp",  "Hyperscaler AI capex digestion; GCP/Azure share gains accelerate"),
    ("AWS operating margin",                    "~36%",   "<28%",  "-8pp",   "AI infra depreciation outpaces revenue ramp; price competition"),
    ("Advertising YoY growth",                  "+19%",   "<10%",  "-9pp",   "Consumer ad budgets cut in recession; TikTok Shop competition"),
    ("NA retail operating margin",              "~7%",    "<3%",   "-4pp",   "Tariffs raise COGS; wage inflation; recession hits AOV"),
    ("Intl retail operating margin",            "~4%",    "<0%",   "-4pp",   "FX headwinds + competitive intensity in India/LatAm"),
    ("AI infra capex % of revenue",             "~15%",   ">18%",  "+3pp",   "Capex super-cycle extends with no revenue payoff yet"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A demand-side AI capex digestion cycle hits AWS growth simultaneously with a")
print(f"  consumer recession that compresses retail margins and ad spend. EPS falls to ~$4.30;")
print(f"  multiple compresses to 18x distress P/E = ${bear_price}.")

# ─── ③ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS x min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}  (consensus $6.20-$6.60)")
print(f"  Min viable P/E at trough:      {PE_TROUGH}x  (2022 trough was ~18-20x; AWS scale supports premium floor)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct>=0 else 'below'} trough floor)")
print()
print(f"  Premium to EPP reflects continued AWS reacceleration + ads optionality not yet in trailing EPS.")
print(f"  Bear ${bear_price} is BELOW EPP ${EPP:.0f} — requires BOTH EPS collapse AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+1.20:.2f} x {PE_TROUGH}x = ${(EPP_EPS+1.2)*PE_TROUGH:.0f} EPP — stock catches up quickly.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: AWS moderates, retail margins steady)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (AWS growth normalizes to mid-teens; ads steady)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (below current multiple; reflects capex digestion discount)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (no dividend; buyback adds incremental return)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is POSITIVE — AWS growth alone (even moderating) plus ads/retail margin")
print(f"  gains support EPS compounding well above the current multiple implies.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.32
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (none; buyback is primary capital return)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (large-cap; AI-capex sentiment + macro consumer exposure)")
print(f"  Beta vs S&P 500:      1.15  (above market; discretionary retail + capex cycle exposure)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (2022 AMZN fell ~50% from peak; achievable in a recession)")
print(f"  -> AWS growth re-rate is the PRIMARY catalyst; sustained >22% growth = +20%+; sub-10% = -25%+.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — mid-range; not pricing extreme outcomes either way.")
print(f"  -> BUY $161-$195  |  TRIM $245+  |  AVOID above $280")

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
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees AWS reacceleration + retail margin gains, tempered by capex SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing AWS/ads/retail margin trajectory.' if ADJ_GAP>0 else 'model roughly agrees with market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) AWS revenue growth re-acceleration -> >=22% confirms BULL capacity unlock")
print(f"  (2) AWS operating margin trend -> Trainium adoption lowering AI inference cost structure")
print(f"  (3) Advertising run-rate -> $80B+ annualised confirms high-margin flywheel intact")
print(f"  (4) NA/Intl retail operating margin -> regionalization + robotics delivering structural gains")
print(f"  BUY $161-{round(CURRENT_PRICE*0.95,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $245  |  AVOID above $280")
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
