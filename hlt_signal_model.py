"""
HLT  ·  Hilton Worldwide Holdings Inc.  ·  NYSE: HLT
Bottom-up signal model  ·  Lodging · Asset-Light Franchise/Management Model · Global Travel Demand
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "HLT"
COMPANY       = "Hilton Worldwide Holdings Inc."
SECTOR        = "Lodging · Asset-Light Franchise/Management · NYSE: HLT"
CURRENT_PRICE = 260.00      # USD; as of 2026-06-11
VOL_52W_LOW   = 195.00
VOL_52W_HIGH  = 275.00
SHARES_OUT_M  = 245.0       # millions; ongoing buyback

# Dividend
ANNUAL_DIV    = 1.00        # $/share

# ── RevPAR / UNIT GROWTH ANALYSIS (company-specific) ──────────────────────────
GLOBAL_REVPAR_GROWTH = 0.03  # 3% YoY global RevPAR growth
NET_UNIT_GROWTH      = 0.05  # ~5% net rooms growth (largely fee-based, capital-light)
FEE_HLTGIN           = 0.60  # incremental margin on fee revenue is very high
TAX_RATE             = 0.24

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 7.80    # FY2026E adj EPS
PE_TROUGH = 16      # min P/E at crisis trough (2020 lows on normalized EPS)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $143

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 6.20, 20,  124, "Global travel demand shock (recession/geopolitical); RevPAR negative; EPS $6.20 -> 20x distress P/E"),
    "BASE":  ( 7.80, 33,  257, "RevPAR +2-4%; net rooms growth ~5% drives high-margin fee growth; EPS $9.50 -> 30x P/E"),
    "BULL":  ( 9.00, 36,  324, "Travel demand re-accelerates; loyalty program (Hilton Honors) drives direct-booking mix higher; EPS $9.00 -> 36x premium P/E"),
    "XBULL": (10.50, 40,  420, "Multi-year global travel supercycle; unit growth accelerates in Asia/Middle East; EPS $10.50 -> 40x peak P/E"),
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
        "name":       "Global RevPAR — YoY growth",
        "weight":     0.25,
        "thresholds": ("<0%",    "≥2%",   "≥4%",    "≥6%"),
        "now":        "+3%",
        "score":      2,
        "comment":    "+3% YoY; international travel demand offsetting softer US group/business travel",
    },
    {
        "name":       "Net rooms (unit) growth",
        "weight":     0.20,
        "thresholds": ("<3%",    "≥4%",   "≥5%",    "≥6.5%"),
        "now":        "~5%",
        "score":      3,
        "comment":    "~5%; record development pipeline (>0.5M rooms), capital-light franchise model",
    },
    {
        "name":       "Fee revenue mix / margin trend",
        "weight":     0.20,
        "thresholds": ("<55%",   "≥58%",  "≥61%",   "≥65%"),
        "now":        "~61%",
        "score":      3,
        "comment":    "~61% high-margin fee revenue; incremental fee dollars drop through at ~60%+ margin",
    },
    {
        "name":       "Loyalty program engagement (Hilton Honors direct-booking mix)",
        "weight":     0.15,
        "thresholds": ("<55%",   "≥60%",  "≥65%",   "≥70%"),
        "now":        "~64%",
        "score":      3,
        "comment":    "~64%; ~210M Hilton Honors members lower distribution costs and improve owner economics",
    },
    {
        "name":       "Buyback pace (% of shares retired/yr)",
        "weight":     0.10,
        "thresholds": ("<2%",    "≥3%",   "≥4%",    "≥5%"),
        "now":        "~3%",
        "score":      2,
        "comment":    "~3%/yr; consistent capital return funded by asset-light free cash flow",
    },
    {
        "name":       "Group/business travel recovery (vs 2019 baseline)",
        "weight":     0.10,
        "thresholds": ("<90%",   "≥95%",  "≥100%",  "≥105%"),
        "now":        "~98%",
        "score":      2,
        "comment":    "~98% of 2019 levels; corporate travel budgets remain a swing factor for US RevPAR",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Asset-light franchise/management moat — minimal capex, high-margin recurring fee streams scale with global travel growth", +0.6, 0.25),
    ("+", "Largest global hotel footprint + Hilton Honors loyalty network — distribution and brand scale advantages compound over time",      +0.5, 0.20),
    ("+", "Record development pipeline — ~5% net unit growth largely locked in for several years regardless of near-term RevPAR",      +0.4, 0.20),
    ("-", "Cyclicality to global travel demand — RevPAR highly sensitive to recession/geopolitical shocks",                            -0.4, 0.20),
    ("-", "Premium valuation — trades at a premium multiple reflecting asset-light quality, limited margin of safety",                 -0.3, 0.15),
]
SCA = sum(score * weight for _, _, score, weight in SCA_FACTORS)
ADJ_COMPOSITE = round(PROXY_COMPOSITE + SCA, 3)

HLTKET_COMPOSITE = back_solve_market_composite(CURRENT_PRICE)
ADJ_GAP = round(ADJ_COMPOSITE - HLTKET_COMPOSITE, 2)

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
CONS_EPS_2YR = 9.00    # conservative FY2028E: unit growth + buyback compounding continues
CONS_PE_2YR  = 30       # floor multiple (slightly below current)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Lodging / Asset-Light Franchise Model")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① REVPAR / UNIT GROWTH ANALYSIS ─────────────────────────────────────────
print()
print("  REVPAR GROWTH vs UNIT GROWTH ANALYSIS  (the core HLT earnings drivers)")
hr()
shares_b = SHARES_OUT_M / 1000
total_fee_rev_b = 6.0
print(f"  Estimated FY2026E fee revenue base: ~${total_fee_rev_b:.1f}B")
print()
print(f"  REVPAR GROWTH UPSIDE  (incremental EPS from RevPAR growth at {FEE_HLTGIN*100:.0f}% incremental margin):")
print(f"  {'RevPAR YoY growth':<20}  {'Rev/yr ($B)':>12}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.00, 0.02, 0.03, 0.05]:
    rev_inc = total_fee_rev_b * g
    inc_eps = rev_inc * FEE_HLTGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% RevPAR growth         +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
print(f"  NET UNIT GROWTH  (~{NET_UNIT_GROWTH*100:.0f}%/yr rooms growth adds directly to fee base regardless of RevPAR;")
print(f"  capital-light franchise model means most of this drops to free cash flow).")
print()
print(f"  BEAR (${bear_price}) requires: a global travel demand shock (recession/geopolitical) drives RevPAR")
print(f"  negative AND multiple compresses to distress levels — together.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (RevPAR + unit growth + fee mix + loyalty + buybacks + group travel)")
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
print(f"  Market composite:   {HLTKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15% hurdle)")
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
    ("Global RevPAR YoY",                         "+3%",    "<0%",   "-3pp",   "Global recession or geopolitical shock craters travel demand"),
    ("Net rooms growth",                          "~5%",    "<3%",   "-2pp",   "Development financing tightens; owner pipeline slows"),
    ("Fee revenue mix",                           "~61%",   "<55%",  "-6pp",   "Owned/leased segment grows faster than franchise mix"),
    ("Hilton Honors direct-booking mix",                 "~64%",   "<55%",  "-9pp",   "OTA share regains ground, raising distribution costs"),
    ("Buyback pace (%/yr)",                       "~3%",    "<2%",   "-1pp",   "Free cash flow pressured, capital return slows"),
    ("Group/business travel (vs 2019)",           "~98%",   "<90%",  "-8pp",   "Corporate travel budgets cut sharply in a downturn"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A global recession or geopolitical shock sharply curtails business and leisure")
print(f"  travel, turning RevPAR negative across regions while development financing tightens.")
print(f"  EPS falls to ~$7.50; multiple compresses to 18x distress P/E = ${bear_price}.")

# ─── ③ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS x min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}")
print(f"  Min viable P/E at trough:      {PE_TROUGH}x  (2020 lows on normalized EPS)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct>=0 else 'below'} trough floor)")
print()
print(f"  Premium to EPP reflects asset-light moat, scale advantages, and locked-in unit growth pipeline.")
print(f"  Bear ${bear_price} is below EPP ${EPP:.0f} — would require both EPS collapse AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+0.80:.2f} x {PE_TROUGH}x = ${(EPP_EPS+0.8)*PE_TROUGH:.0f} EPP — unit growth compounds the floor higher.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: RevPAR moderate, unit growth + buyback compounding continue)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (low-single-digit RevPAR + ~5% unit growth + buybacks)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (slightly below current)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f} x 2)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — locked-in unit growth pipeline plus")
print(f"  fee-revenue operating leverage and buybacks support steady EPS compounding even in a soft macro.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.22
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (above-market; cyclical travel exposure)")
print(f"  Beta vs S&P 500:      1.20  (above market; cyclical)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (2020 HLT fell ~70% from peak intra-COVID; tail risk, not base case)")
print(f"  -> Global travel demand trajectory is the PRIHLTY catalyst; resilient travel = upside;")
print(f"     recession/shock = -30%+ downside.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — upper-mid range; not stretched relative to growth profile.")
print(f"  -> BUY $200-$220  |  TRIM $280+  |  AVOID above $305")

# ─── ⑥ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print()
print("  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
hr()
probs_mkt = softmax_probs(HLTKET_COMPOSITE)
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
ev_mkt = expected_value(HLTKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): ${ev_adj:.0f}  /  Proxy EV: ${ev_prx:.0f}  /  Market EV: ${ev_mkt:.0f}  /  Current: ${CURRENT_PRICE:.0f}")
hr()
print(f"  Downside  (-> Bear ${bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (-> Bull ${bull_price}):   {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b:.2f}x")
print(f"  Signal    :  {signal_full}")
print()
print(f"  Market composite {HLTKET_COMPOSITE:.2f} reflects pricing roughly between BASE and BULL")
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees fee growth + unit growth pipeline, tempered by cyclicality/valuation SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing the asset-light compounding story.' if ADJ_GAP>0 else 'model roughly agrees with market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) Global RevPAR -> sustained >=4% confirms travel demand resilience")
print(f"  (2) Net unit growth -> pipeline conversion stays >=5%/yr")
print(f"  (3) Hilton Honors direct-booking mix -> continued gains lower distribution costs")
print(f"  (4) Group/business travel recovery -> approach/exceed 2019 levels confirms BULL case")
print(f"  BUY $200-{round(CURRENT_PRICE*0.90,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $280  |  AVOID above $305")
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
    "market_composite": HLTKET_COMPOSITE,
    "adj_gap":          ADJ_GAP,
    "valuation":        valuation_label,
    "cons_return_2yr":  cons_return,
}

if __name__ == "__main__":
    pass
