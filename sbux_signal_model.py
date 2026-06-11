"""
SBUX  ·  Starbucks Corporation  ·  NASDAQ: SBUX
Bottom-up signal model  ·  Coffeehouse / Global Retail / "Back to Starbucks" Turnaround
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "SBUX"
COMPANY       = "Starbucks Corporation"
SECTOR        = "Coffeehouse / Global Retail · 'Back to Starbucks' Turnaround · NASDAQ: SBUX"
CURRENT_PRICE = 92.00       # USD; as of 2026-06-11
VOL_52W_LOW   = 72.00       # April 2026 turnaround-fear trough
VOL_52W_HIGH  = 105.00      # late 2025 turnaround-hope rally peak
SHARES_OUT_M  = 1145.0      # millions

# Dividend
ANNUAL_DIV    = 2.28        # $/share FY2026 (quarterly $0.57; long dividend growth streak)

# ── US TURNAROUND vs CHINA RECOVERY ANALYSIS (company-specific calculator) ─
# Revenue / segment breakdown FY2026E ($B)
NA_REV_B          = 24.0    # North America company-operated + licensed
INTL_REV_B        = 9.5     # International (incl. China JV consolidation effects)
CHINA_REV_B       = 3.2     # China standalone (subset of International)
CPG_REV_B         = 2.3     # Channel Development / CPG (packaged coffee, ready-to-drink)

NA_OP_MARGIN     = 0.16     # NA operating margin (pressured by "Green Apron" labor investment)
INTL_OP_MARGIN   = 0.13     # International operating margin
US_COMP_GROWTH   = 0.02     # 2% YoY US comp sales growth (turnaround stabilizing, Q1 2026)
CHINA_COMP_GROWTH = -0.02   # -2% YoY China comps (competitive intensity from Luckin/local brands)
TAX_RATE         = 0.23     # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 2.45    # FY2026E adj EPS (consensus $2.30-$2.60; depressed by turnaround investment)
PE_TROUGH = 18      # min P/E at crisis trough (brand value supports floor above typical restaurant troughs)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $44

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 1.60, 22,   35, "US comps stay negative; China JV divestiture proceeds disappoint; 'Back to Starbucks' stalls; EPS $1.60 -> 22x distress P/E"),
    "BASE":  ( 2.45, 30,   74, "US comps +2-3%; China stabilizes; turnaround costs moderate; EPS $2.45 -> 30x P/E"),
    "BULL":  ( 3.60, 33,  119, "US comps +4-6% (Green Apron staffing pays off); China JV partner accelerates store growth; EPS $3.60 -> 33x premium P/E"),
    "XBULL": ( 4.80, 35,  168, "Full turnaround completion; throughput/digital reaccelerate; China re-rates as growth market again; EPS $4.80 -> 35x peak P/E"),
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
        "name":       "US comparable sales — YoY growth",
        "weight":     0.25,
        "thresholds": ("<-1%",   "≥1%",   "≥3%",    "≥5%"),
        "now":        "+2%",
        "score":      2,
        "comment":    "+2% YoY; first positive comp in 6 quarters; Green Apron staffing improving throughput",
    },
    {
        "name":       "China comparable sales — YoY growth",
        "weight":     0.20,
        "thresholds": ("<-6%",   "≥-3%",  "≥0%",    "≥4%"),
        "now":        "-2%",
        "score":      2,
        "comment":    "-2% YoY; improving from -8% trough but still negative vs Luckin/local competition",
    },
    {
        "name":       "Operating margin trend (turnaround cost absorption)",
        "weight":     0.20,
        "thresholds": ("<10%",   "≥12%",  "≥14.5%", "≥17%"),
        "now":        "~13%",
        "score":      2,
        "comment":    "~13%; Green Apron labor investment pressuring margins, expected to inflect FY2027",
    },
    {
        "name":       "Store-level throughput / order accuracy improvement",
        "weight":     0.15,
        "thresholds": ("declining","flat","improving","strong improvement"),
        "now":        "improving",
        "score":      3,
        "comment":    "Equipment investments (Green Apron, cold-brew systems) improving wait times measurably",
    },
    {
        "name":       "China JV / strategic partnership progress",
        "weight":     0.10,
        "thresholds": ("stalled", "announced", "signed",  "executing"),
        "now":        "signed",
        "score":      3,
        "comment":    "Strategic partnership for China retail JV signed; partner brings local capital + distribution",
    },
    {
        "name":       "Loyalty / digital mix (Starbucks Rewards % of US transactions)",
        "weight":     0.10,
        "thresholds": ("<55%",   "≥58%",  "≥62%",   "≥66%"),
        "now":        "~60%",
        "score":      2,
        "comment":    "~60%; loyalty mix steady; mobile order/pay remains a structural advantage vs peers",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Global brand moat — #1 coffeehouse brand; ~40000 stores; loyalty program with 34M+ active US members", +0.7, 0.25),
    ("+", "'Back to Starbucks' turnaround — Niccol-led changes (Green Apron, simplified menu) showing early traction", +0.5, 0.20),
    ("+", "China JV partnership — de-risks China execution, brings local capital for store growth resumption",     +0.4, 0.15),
    ("-", "Margin recovery uncertainty — labor investment costs may persist longer than guided; execution risk",     -0.6, 0.25),
    ("-", "Competitive intensity — Luckin Coffee (China), independent specialty coffee, QSR coffee programs (US)",   -0.4, 0.15),
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
CONS_EPS_2YR = 3.00    # conservative FY2028E: turnaround partially delivers, margins recover modestly
CONS_PE_2YR  = 26      # floor multiple (below current; reflects execution-risk discount)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Coffeehouse / Global Retail / Turnaround")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① US TURNAROUND vs CHINA RECOVERY ANALYSIS ─────────────────────────────
print()
print("  US TURNAROUND MARGIN RECOVERY vs CHINA STABILIZATION ANALYSIS  (the core SBUX tension)")
hr()

total_rev_b = NA_REV_B + INTL_REV_B + CPG_REV_B
print(f"  FY2026E Segment Revenue:")
print(f"  {'North America (company-op + licensed)':<36}  ${NA_REV_B:>5.1f}B  ({NA_REV_B/total_rev_b*100:.0f}% of total; {NA_OP_MARGIN*100:.0f}% op margin)")
print(f"  {'International (incl. China)':<36}  ${INTL_REV_B:>5.1f}B  ({INTL_REV_B/total_rev_b*100:.0f}%; {INTL_OP_MARGIN*100:.0f}% op margin)")
print(f"  {'  of which China':<36}  ${CHINA_REV_B:>5.1f}B  ({CHINA_REV_B/total_rev_b*100:.0f}%; comps {CHINA_COMP_GROWTH*100:+.0f}%)")
print(f"  {'Channel Development / CPG':<36}  ${CPG_REV_B:>5.1f}B  ({CPG_REV_B/total_rev_b*100:.0f}%; high-margin licensing)")
hr()
print(f"  Total FY2026E:                          ${total_rev_b:>5.1f}B")
print()

shares_b = SHARES_OUT_M / 1000
print(f"  US COMP GROWTH UPSIDE  (incremental EPS from US comp growth above/below {US_COMP_GROWTH*100:.0f}%):")
print(f"  {'US comp YoY growth':<22}  {'Rev/yr':>10}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.00, 0.02, 0.04, 0.06]:
    rev_inc = NA_REV_B * g
    inc_eps = rev_inc * NA_OP_MARGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% US comp growth        +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
margin_recovery = NA_REV_B * 0.01 * (1 - TAX_RATE) / shares_b  # each 1pp NA margin recovery
print(f"  MARGIN RECOVERY UPSIDE  (each +1pp NA operating margin = +${margin_recovery:.2f}/EPS/yr):")
print(f"  Current ~{NA_OP_MARGIN*100:.0f}% -> recovery to historical ~18-19% (+5-6pp) = +${margin_recovery*5:.2f} to +${margin_recovery*6:.2f}/EPS/yr")
print(f"  -> over 2yr (phased) = +${margin_recovery*5:.2f} to +${margin_recovery*6*2:.2f}/EPS")
print()
print(f"  BEAR (${bear_price}) requires: US comps stay negative AND China JV partnership disappoints AND")
print(f"  Green Apron labor investment fails to translate into margin recovery — simultaneously.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (US comps + China + margins + throughput + JV + loyalty)")
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
    ("US comparable sales YoY",                  "+2%",    "<-1%",  "-3pp",   "Turnaround stalls; QSR coffee competition (McCafe, Dunkin) intensifies"),
    ("China comparable sales YoY",               "-2%",    "<-6%",  "-4pp",   "Luckin Coffee + local brands accelerate share gains; consumer downtrade"),
    ("Operating margin",                         "~13%",   "<10%",  "-3pp",   "Green Apron labor costs persist without throughput payoff"),
    ("Store throughput improvement",             "improving","declining","reversal", "Equipment rollout fails to reduce wait times; mobile order congestion worsens"),
    ("China JV progress",                        "signed", "stalled","reversal", "Strategic partner negotiations collapse; China store growth frozen"),
    ("Loyalty / digital mix",                    "~60%",   "<55%",  "-5pp",   "App fatigue; promotional intensity erodes loyalty engagement"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: The 'Back to Starbucks' turnaround stalls — Green Apron labor investment raises")
print(f"  costs without driving throughput/comp recovery, while China JV negotiations collapse and")
print(f"  Luckin continues taking share. EPS falls to ~$1.60; multiple compresses to 22x distress P/E")
print(f"  = ${bear_price}.")

# ─── ③ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS x min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}  (consensus $2.30-$2.60; depressed by turnaround investment)")
print(f"  Min viable P/E at trough:      {PE_TROUGH}x  (brand value supports floor above typical restaurant troughs)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct>=0 else 'below'} trough floor)")
print()
print(f"  Large premium to EPP reflects market pricing in turnaround success (margin recovery from depressed base).")
print(f"  Bear ${bear_price} is BELOW EPP ${EPP:.0f} — requires BOTH EPS collapse AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+0.55:.2f} x {PE_TROUGH}x = ${(EPP_EPS+0.55)*PE_TROUGH:.0f} EPP — EPP rises sharply if margin recovery begins.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: partial turnaround delivery, modest margin recovery)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (US comps +2-3% + partial margin recovery to ~15%)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (below current; execution-risk discount)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f} x 2)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — even partial turnaround delivery plus the dividend")
print(f"  provides reasonable return; full margin recovery (BULL/XBULL) is the larger optionality.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.28
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%; long dividend growth streak)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (turnaround-stage volatility; quarterly comp data is the swing factor)")
print(f"  Beta vs S&P 500:      0.95  (near market; consumer discretionary with defensive brand qualities)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (turnaround disappointment scenarios have produced -30%+ moves before)")
print(f"  -> Quarterly US comp trajectory is the PRIMARY catalyst; sustained >=4% = BULL re-rate;")
print(f"     return to negative comps = -25%+ downside.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — mid-range; turnaround-hope partially priced in.")
print(f"  -> BUY $72-$85  |  TRIM $105+  |  AVOID above $120")

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
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees early turnaround traction + China JV optionality, tempered by margin-recovery SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing turnaround trajectory.' if ADJ_GAP>0 else 'model roughly agrees with market pricing on turnaround execution risk.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) US comp sales trajectory -> sustained >=3% confirms 'Back to Starbucks' working")
print(f"  (2) Operating margin inflection -> NA margin recovery toward 16-18% confirms labor investment payoff")
print(f"  (3) China JV execution -> partner-funded store growth resumption signals China stabilization")
print(f"  (4) China comps -> return to positive confirms competitive position vs Luckin stabilizing")
print(f"  BUY $72-{round(CURRENT_PRICE*0.95,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $105  |  AVOID above $120")
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
