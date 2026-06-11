"""
ORLY  ·  O'Reilly Automotive, Inc.  ·  NASDAQ: ORLY
Bottom-up signal model  ·  Auto Parts Retail · DIY + Professional (DIFM) · Dual-Market Resilience
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "ORLY"
COMPANY       = "O'Reilly Automotive, Inc."
SECTOR        = "Auto Parts Retail · DIY / Professional (DIFM) · NASDAQ: ORLY"
CURRENT_PRICE = 95.00       # USD; post 15-for-1 split (June 2025), as of 2026-06-11
VOL_52W_LOW   = 72.00       # post-split early-2026 trough
VOL_52W_HIGH  = 102.00      # late-2025/early-2026 high
SHARES_OUT_M  = 590.0       # millions; aggressive ongoing buyback (down from ~600M)

# Dividend
ANNUAL_DIV    = 0.00        # no dividend; 100% of FCF to buybacks

# ── FLEET-AGE / MILES-DRIVEN TAILWIND ANALYSIS (company-specific calculator) ──
# Comparable store sales build (FY2026E)
COMP_GROWTH_RATE   = 0.03   # 3% YoY comparable store sales growth (DIY+DIFM blend)
DIY_MIX            = 0.55   # DIY share of revenue
DIFM_MIX           = 0.45   # Professional/DIFM share of revenue
OP_MARGIN          = 0.205  # operating margin (best-in-class for the category)
TAX_RATE           = 0.24   # effective rate
NEW_STORE_GROWTH   = 0.04   # ~4% annual square-footage/unit growth

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 2.85    # FY2026E adj EPS (post-split basis; consensus $2.78-$2.92)
PE_TROUGH = 18      # min P/E at crisis trough (2020 lows ~17-19x on normalized EPS)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $51

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 2.50, 20,   50, "Recession hits DIFM volumes; new-car sales recovery shrinks fleet age tailwind; EPS $2.50 -> 20x distress P/E"),
    "BASE":  ( 2.90, 33,   96, "Comps +2-4%; aging vehicle fleet (avg ~12.6yrs) sustains DIY+DIFM demand; EPS $2.90 -> 33x P/E"),
    "BULL":  ( 3.30, 36,  119, "DIFM share gains accelerate via hub/distribution buildout; buyback compounds EPS faster; EPS $3.30 -> 36x premium P/E"),
    "XBULL": ( 3.80, 40,  152, "Macro downturn extends fleet life further, structurally boosting aftermarket demand for years; EPS $3.80 -> 40x peak P/E"),
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
        "name":       "Comparable store sales — YoY growth (DIY + DIFM blend)",
        "weight":     0.25,
        "thresholds": ("<0%",    "≥2%",   "≥4%",    "≥6%"),
        "now":        "+3%",
        "score":      2,
        "comment":    "+3% YoY; aging vehicle fleet (avg age ~12.6yrs, record high) drives steady aftermarket demand",
    },
    {
        "name":       "DIFM (professional) revenue mix growth",
        "weight":     0.20,
        "thresholds": ("<40%",   "≥43%",  "≥46%",   "≥50%"),
        "now":        "~45%",
        "score":      3,
        "comment":    "~45% and rising; hub/super-hub distribution buildout improving same-day fill rates for shops",
    },
    {
        "name":       "Operating margin trend",
        "weight":     0.20,
        "thresholds": ("<18%",   "≥19.5%","≥20.5%", "≥21.5%"),
        "now":        "~20.5%",
        "score":      3,
        "comment":    "~20.5%; best-in-class cost discipline, supply chain leverage offsetting wage inflation",
    },
    {
        "name":       "Share buyback pace (% of shares retired/yr)",
        "weight":     0.15,
        "thresholds": ("<2%",    "≥3%",   "≥4%",    "≥5%"),
        "now":        "~4%",
        "score":      3,
        "comment":    "~4%/yr; consistent aggressive repurchase program compounding EPS regardless of macro",
    },
    {
        "name":       "New store / distribution footprint growth",
        "weight":     0.10,
        "thresholds": ("<2%",    "≥3%",   "≥4%",    "≥5%"),
        "now":        "~4%",
        "score":      3,
        "comment":    "~4%/yr unit growth; long runway in underpenetrated regions (Northeast, Midwest expansion)",
    },
    {
        "name":       "New & used vehicle sales trend (inverse correlation to demand)",
        "weight":     0.10,
        "thresholds": ("strong rebound","modest rebound","flat","declining"),
        "now":        "flat",
        "score":      2,
        "comment":    "New car affordability remains stretched; vehicle replacement cycle elongating, supportive of demand",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Dual-market resilience — DIY (recession-resistant) + DIFM (growth) provide demand stability across cycles",  +0.6, 0.25),
    ("+", "Aging vehicle fleet structural tailwind — record avg fleet age (~12.6yrs) supports multi-year aftermarket demand", +0.5, 0.20),
    ("+", "Best-in-class capital allocation — relentless buyback compounding EPS at ~4%/yr regardless of top-line", +0.5, 0.20),
    ("-", "Premium valuation — trades near peak historical multiple, limited margin of safety on multiple compression", -0.4, 0.20),
    ("-", "New-vehicle sales recovery risk — sustained drop in used-car prices/financing easing could shorten replacement cycles", -0.3, 0.15),
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
CONS_EPS_2YR = 3.30    # conservative FY2028E: comps moderate, buyback compounding continues
CONS_PE_2YR  = 30      # floor multiple (slightly below current; some multiple normalization)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Auto Parts Retail / Aging Fleet Beneficiary")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① FLEET-AGE TAILWIND vs NEW-CAR-RECOVERY RISK ANALYSIS ─────────────────
print()
print("  AGING FLEET TAILWIND vs NEW-VEHICLE-RECOVERY RISK ANALYSIS  (the core ORLY tension)")
hr()

shares_b = SHARES_OUT_M / 1000
print(f"  Revenue mix: DIY {DIY_MIX*100:.0f}% / DIFM (Professional) {DIFM_MIX*100:.0f}%")
print(f"  Operating margin: {OP_MARGIN*100:.1f}%  (best-in-class for auto parts retail)")
print()
print(f"  COMP GROWTH UPSIDE  (incremental EPS from comp growth, illustrative on ~$18B revenue base):")
print(f"  {'Comp YoY growth':<20}  {'Rev/yr ($B)':>12}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
total_rev_b = 18.0
for g in [0.00, 0.02, 0.03, 0.05]:
    rev_inc = total_rev_b * g
    inc_eps = rev_inc * OP_MARGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% comp growth         +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
print(f"  BUYBACK COMPOUNDING  (~{NEW_STORE_GROWTH*100:.0f}% annual share count reduction adds directly to EPS growth")
print(f"  independent of revenue trends — a structural advantage versus most retailers).")
print()
print(f"  BEAR (${bear_price}) requires: new/used vehicle sales rebound sharply (shortening replacement cycle),")
print(f"  DIFM volumes soften with a broader recession, AND multiple compresses to distress levels — together.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (comps + DIFM mix + margin + buybacks + store growth + vehicle sales)")
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
    ("Comparable store sales YoY",                "+3%",    "<0%",   "-3pp",   "New/used vehicle affordability improves; replacement cycle shortens"),
    ("DIFM revenue mix",                          "~45%",   "<40%",  "-5pp",   "Independent shop closures / consolidation reduces DIFM customer base"),
    ("Operating margin",                          "~20.5%", "<18%",  "-2.5pp", "Wage and freight inflation outpace pricing power"),
    ("Buyback pace (%/yr)",                       "~4%",    "<2%",   "-2pp",   "Leverage constraints or capital reallocation slows repurchases"),
    ("New store/footprint growth",                "~4%",    "<2%",   "-2pp",   "Real estate cost inflation slows expansion pace"),
    ("New/used vehicle sales trend",              "flat",   "strong rebound", "n/a", "Falling rates + improved affordability spur a vehicle-buying wave"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A sharp drop in financing rates and used-car prices makes new-vehicle ownership")
print(f"  affordable again, accelerating fleet turnover and shrinking the aging-fleet tailwind just as")
print(f"  a broader slowdown softens DIFM shop volumes. EPS falls to ~$2.50; multiple compresses to")
print(f"  20x distress P/E = ${bear_price}.")

# ─── ③ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS x min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}  (post-split basis; consensus $2.78-$2.92)")
print(f"  Min viable P/E at trough:      {PE_TROUGH}x  (2020 lows ~17-19x on normalized EPS)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct>=0 else 'below'} trough floor)")
print()
print(f"  Premium to EPP reflects dual-market resilience, structural fleet-age tailwind, and consistent buyback.")
print(f"  Bear ${bear_price} is roughly AT EPP ${EPP:.0f} — would require both EPS softness AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+0.30:.2f} x {PE_TROUGH}x = ${(EPP_EPS+0.3)*PE_TROUGH:.0f} EPP — buyback-driven EPS growth lifts the floor.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: comps moderate, buyback compounding continues)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (low-single-digit comps + buyback-driven EPS growth)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (slightly below current; modest multiple normalization)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (no dividend; 100% to buybacks)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — aging fleet demand plus")
print(f"  aggressive buybacks support steady EPS compounding even in a soft macro.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.18
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (no dividend; 100% of FCF to buybacks)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (low for retail; defensive/counter-cyclical profile)")
print(f"  Beta vs S&P 500:      0.75  (below market; defensive auto-aftermarket profile)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (would require a sharp reversal of the fleet-age tailwind)")
print(f"  -> New/used vehicle affordability trend is the PRIMARY catalyst; falling rates = downside risk;")
print(f"     elevated rates/prices = aging-fleet tailwind persists.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — mid-to-upper range; defensive profile not stretched.")
print(f"  -> BUY $75-$85  |  TRIM $105+  |  AVOID above $115")

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
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees aging-fleet demand + buyback compounding, tempered by valuation/recovery-risk SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing the fleet-age/buyback compounding story.' if ADJ_GAP>0 else 'model roughly agrees with market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) Comp sales sustainability -> >=4% confirms aging-fleet tailwind durable")
print(f"  (2) DIFM mix growth -> hub/super-hub buildout continues gaining professional share")
print(f"  (3) Buyback pace -> sustained ~4%/yr share count reduction compounds EPS")
print(f"  (4) New/used vehicle sales -> stay flat-to-declining confirms elongated replacement cycle")
print(f"  BUY $75-{round(CURRENT_PRICE*0.90,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $105  |  AVOID above $115")
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
