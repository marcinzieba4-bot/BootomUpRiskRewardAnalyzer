"""
CMG  ·  Chipotle Mexican Grill, Inc.  ·  NYSE: CMG
Bottom-up signal model  ·  Fast-Casual Restaurant / Throughput & Unit Growth / Automation (Autocado)
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "CMG"
COMPANY       = "Chipotle Mexican Grill, Inc."
SECTOR        = "Fast-Casual Restaurant · Throughput & Unit Growth · Kitchen Automation · NYSE: CMG"
CURRENT_PRICE = 48.00       # USD; as of 2026-06-11 (post 50-for-1 split adjusted basis)
VOL_52W_LOW   = 38.00       # April 2026 comp-slowdown trough
VOL_52W_HIGH  = 62.00       # late 2025 throughput-acceleration peak
SHARES_OUT_M  = 3550.0      # millions; aggressive buyback continues

# No dividend — reinvests in unit growth
ANNUAL_DIV    = 0.00

# ── UNIT GROWTH vs COMP DECELERATION ANALYSIS (company-specific calculator) ─
# Revenue / unit economics breakdown FY2026E
TOTAL_REV_B        = 13.2   # total revenue
RESTAURANT_COUNT   = 3950   # total restaurants (incl. ~80 international/licensed)
NEW_UNIT_TARGET    = 330    # net new restaurant openings/yr target
AVG_UNIT_VOLUME_M  = 3.2    # average unit volume ($M/restaurant/yr)
DIGITAL_MIX_PCT    = 0.36   # % of sales through digital channels (app/web/Chipotlanes)

RESTAURANT_OP_MARGIN = 0.275 # restaurant-level operating margin
COMP_GROWTH_RATE    = 0.015  # 1.5% YoY comp sales growth (Q1 2026 run-rate; decelerating from historical 5-7%)
AUTOCADO_LABOR_SAVE_PCT = 0.005  # ~50bps labor cost savings from kitchen automation rollout
TAX_RATE            = 0.25   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 1.18    # FY2026E adj EPS (consensus $1.12-$1.25, post-split basis)
PE_TROUGH = 28      # min P/E at crisis trough (premium growth name; 2015-16 food-safety crisis ~25-30x)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $33

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 0.85, 26,   22, "Comps turn negative; unit growth slows amid saturation fears; margin compression; EPS $0.85 -> 26x distress P/E"),
    "BASE":  ( 1.18, 38,   45, "Comps +1-3%; unit growth ~330/yr continues; Autocado labor savings offset wage inflation; EPS $1.18 -> 38x P/E"),
    "BULL":  ( 1.55, 42,   65, "Comps reaccelerate to 4-6% on menu innovation (new proteins); international expansion (Chipotle Europe) scales; EPS $1.55 -> 42x premium P/E"),
    "XBULL": ( 2.05, 45,   92, "Throughput/automation step-change drives sustained 6%+ comps + 400+ unit/yr growth; EPS $2.05 -> 45x peak P/E"),
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
        "name":       "Comparable restaurant sales — YoY growth",
        "weight":     0.25,
        "thresholds": ("<-1%",   "≥1%",   "≥3%",    "≥5%"),
        "now":        "+1.5%",
        "score":      2,
        "comment":    "+1.5% YoY; transaction growth positive but decelerating from historical 5-7% pace",
    },
    {
        "name":       "Net new restaurant openings (annual pace)",
        "weight":     0.20,
        "thresholds": ("<200",   "≥280",  "≥330",   "≥400"),
        "now":        "~330",
        "score":      3,
        "comment":    "~330 net new units/yr; long-term target of 7000+ in NA; international (Europe) accelerating",
    },
    {
        "name":       "Digital sales mix (app/web/Chipotlanes)",
        "weight":     0.15,
        "thresholds": ("<30%",   "≥34%",  "≥38%",   "≥43%"),
        "now":        "~36%",
        "score":      2,
        "comment":    "~36%; Chipotlane-equipped units continue outperforming on throughput and digital attach",
    },
    {
        "name":       "Restaurant-level operating margin trend",
        "weight":     0.15,
        "thresholds": ("<25%",   "≥26.5%","≥28%",   "≥30%"),
        "now":        "~27.5%",
        "score":      2,
        "comment":    "~27.5%; near record highs; food cost inflation (avocado, beef) offsetting some throughput gains",
    },
    {
        "name":       "Kitchen automation (Autocado/Augmented Throughput) rollout progress",
        "weight":     0.15,
        "thresholds": ("pilot",  "expanding","majority","full rollout"),
        "now":        "expanding",
        "score":      2,
        "comment":    "Autocado (avocado prep) + digital makeline expanding beyond pilot to several hundred restaurants",
    },
    {
        "name":       "Menu innovation pipeline (new protein/LTO contribution to traffic)",
        "weight":     0.10,
        "thresholds": ("none",   "tested", "launched","scaling"),
        "now":        "launched",
        "score":      2,
        "comment":    "New protein LTOs (e.g., Adobo Ranch chicken) launched; early traffic lift modest but positive",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Best-in-class unit economics — ~$3.2M AUV, ~27.5% restaurant margins, fully company-owned (no franchise drag)", +0.7, 0.25),
    ("+", "Long runway for unit growth — target 7000+ NA units (vs ~3950 today) plus nascent international (Europe)",     +0.6, 0.20),
    ("+", "Automation/throughput investment — Autocado + digital makelines structurally lower labor cost per transaction", +0.4, 0.15),
    ("-", "Comp deceleration risk — slowing from historical 5-7% to ~1-3% raises questions about saturation/fatigue",      -0.5, 0.25),
    ("-", "Premium valuation — trades at growth-stock multiple with limited margin of safety if comps stay low",           -0.4, 0.15),
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
CONS_EPS_2YR = 1.35    # conservative FY2028E: comps stay ~1-2%, unit growth continues, modest margin gains
CONS_PE_2YR  = 33      # floor multiple (below current; reflects comp-deceleration discount)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Fast-Casual Restaurant / Unit Growth / Automation")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① UNIT GROWTH vs COMP DECELERATION ANALYSIS ────────────────────────────
print()
print("  UNIT GROWTH RUNWAY vs COMP DECELERATION / AUTOMATION OFFSET ANALYSIS  (the core CMG tension)")
hr()

print(f"  FY2026E Operating Metrics:")
print(f"  {'Total revenue':<36}  ${TOTAL_REV_B:>5.1f}B")
print(f"  {'Restaurant count':<36}  {RESTAURANT_COUNT:>6,}  (+{NEW_UNIT_TARGET} net new/yr target)")
print(f"  {'Average unit volume (AUV)':<36}  ${AVG_UNIT_VOLUME_M:>5.1f}M/restaurant/yr")
print(f"  {'Digital sales mix':<36}  {DIGITAL_MIX_PCT*100:>5.1f}%  of total sales")
print(f"  {'Restaurant-level operating margin':<36}  {RESTAURANT_OP_MARGIN*100:>5.1f}%")
hr()
print()

shares_b = SHARES_OUT_M / 1000
print(f"  COMP GROWTH UPSIDE  (incremental EPS from comp growth above/below {COMP_GROWTH_RATE*100:.1f}%):")
print(f"  {'Comp YoY growth':<20}  {'Rev/yr':>10}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.00, 0.02, 0.04, 0.06]:
    rev_inc = TOTAL_REV_B * g
    inc_eps = rev_inc * RESTAURANT_OP_MARGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% comp growth          +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
new_unit_rev_b = NEW_UNIT_TARGET * AVG_UNIT_VOLUME_M / 1000
new_unit_eps   = new_unit_rev_b * RESTAURANT_OP_MARGIN * (1 - TAX_RATE) / shares_b
print(f"  UNIT GROWTH CONTRIBUTION  ({NEW_UNIT_TARGET} net new units/yr at ${AVG_UNIT_VOLUME_M:.1f}M AUV):")
print(f"  +${new_unit_rev_b:.2f}B incremental revenue/yr -> +${new_unit_eps:.2f}/EPS/yr -> over 2yr (compounding) = +${new_unit_eps*2.1:.2f}/EPS")
print()
autocado_save = TOTAL_REV_B * AUTOCADO_LABOR_SAVE_PCT * (1 - TAX_RATE) / shares_b
print(f"  AUTOCADO LABOR SAVINGS  (each 50bps of labor cost reduction = +${autocado_save:.2f}/EPS/yr):")
print(f"  Current rollout pace ~50bps/yr = +${autocado_save:.2f}/EPS  -> over 2yr (full rollout) = +${autocado_save*2:.2f}/EPS")
print()
print(f"  BEAR (${bear_price}) requires: comps turn negative AND unit growth slows on saturation fears AND")
print(f"  food-cost inflation outpaces automation savings — simultaneously.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (comps + unit growth + digital mix + margins + automation + menu innovation)")
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
    ("Comparable restaurant sales YoY",          "+1.5%",  "<-1%",  "-2.5pp", "Consumer pulls back on discretionary dining; value perception erodes"),
    ("Net new unit openings/yr",                 "~330",   "<200",  "-130",   "Real estate cost inflation + saturation concerns slow expansion pace"),
    ("Digital sales mix",                        "~36%",   "<30%",  "-6pp",   "App engagement declines; loyalty promotions lose effectiveness"),
    ("Restaurant-level operating margin",        "~27.5%", "<25%",  "-2.5pp", "Avocado/beef cost spikes outpace menu pricing and automation savings"),
    ("Autocado/automation rollout",              "expanding","pilot","reversal","Technology issues stall rollout beyond initial pilot restaurants"),
    ("Menu innovation traffic lift",             "launched","none", "reversal","New protein LTOs fail to drive incremental visits; menu fatigue"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A consumer pullback turns comps negative just as avocado/beef cost inflation")
print(f"  outpaces automation-driven labor savings, while saturation concerns force management to slow")
print(f"  the unit growth pace below 200/yr. EPS falls to ~$0.85; multiple compresses to 26x distress")
print(f"  P/E = ${bear_price}.")

# ─── ③ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS x min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}  (consensus $1.12-$1.25, post-split basis)")
print(f"  Min viable P/E at trough:      {PE_TROUGH}x  (premium growth name; 2015-16 food-safety crisis ~25-30x)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct>=0 else 'below'} trough floor)")
print()
print(f"  Premium to EPP reflects market pricing in continued unit growth + automation margin tailwinds.")
print(f"  Bear ${bear_price} is BELOW EPP ${EPP:.0f} — requires BOTH EPS collapse AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+0.18:.2f} x {PE_TROUGH}x = ${(EPP_EPS+0.18)*PE_TROUGH:.0f} EPP — unit growth alone compounds EPP higher.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: comps stay low-single-digit, unit growth + automation continue)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (comps ~1-2% + ~330 units/yr + Autocado margin gains)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (below current; comp-deceleration discount)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (no dividend; reinvests in unit growth + buybacks)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — unit growth alone (even with muted comps) drives")
print(f"  EPS compounding; menu innovation/automation provide additional optionality not in the conservative case.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.30
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (none; reinvests in unit growth + buybacks)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (premium growth name; comp-print sensitivity drives large moves)")
print(f"  Beta vs S&P 500:      1.10  (above market; discretionary dining + growth-multiple sensitivity)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (CMG fell ~50% in 2024-25 comp-deceleration scare — comparable magnitude possible)")
print(f"  -> Comp sales trajectory is the PRIMARY catalyst; reacceleration to >=4% = BULL re-rate;")
print(f"     sustained negative comps = -25%+ downside.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — mid-range; comp-deceleration concerns partially priced in.")
print(f"  -> BUY $38-$44  |  TRIM $62+  |  AVOID above $70")

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
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees unit-growth + automation tailwinds, tempered by comp-deceleration SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing unit-growth/automation trajectory.' if ADJ_GAP>0 else 'model is more cautious than market on comp-deceleration risk.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) Comp sales trajectory -> reacceleration to >=4% confirms menu innovation working")
print(f"  (2) Unit growth pace -> sustained >=330/yr confirms long-term 7000+ NA target on track")
print(f"  (3) Autocado/automation rollout -> expansion beyond pilot confirms structural margin tailwind")
print(f"  (4) International (Europe) expansion -> accelerating unit growth confirms new growth vector")
print(f"  BUY $38-{round(CURRENT_PRICE*0.95,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $62  |  AVOID above $70")
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
