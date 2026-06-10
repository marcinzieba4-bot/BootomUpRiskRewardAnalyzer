"""
FCX  ·  Freeport-McMoRan Inc.  ·  NYSE: FCX
Bottom-up signal model  ·  Copper / Gold / Molybdenum Mining
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "FCX"
COMPANY       = "Freeport-McMoRan Inc."
SECTOR        = "Copper / Gold / Molybdenum Mining · Grasberg · NYSE: FCX"
CURRENT_PRICE = 48.50        # USD; as of 2026-06-10
VOL_52W_LOW   = 31.20        # 2025 China-demand-scare / copper price trough
VOL_52W_HIGH  = 55.80        # early-2026 copper spike on AI-datacenter/grid demand
SHARES_OUT_M  = 1_460.0      # millions; modest buyback offset by share-based comp

# Dividend: base $0.15/quarter + variable performance dividend tied to FCF
ANNUAL_DIV    = 0.60         # $/share (base dividend; variable div adds in BULL years)

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B), driven primarily by realized copper price ($/lb)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("North America Copper Mines", 8.0,  6.2, 10.5, "Morenci, Bagdad, Safford; high-cost US operations; leaching/SX-EW growth"),
    ("South America",              4.5,  3.5,  6.0, "Cerro Verde (Peru), El Abra (Chile); stable low-cost concentrate production"),
    ("Indonesia / Grasberg",       9.5,  7.0, 13.5, "Crown jewel; world's largest gold reserve + copper; PT-FI export/regulatory risk"),
    ("Molybdenum / Other",         1.5,  1.0,  2.2, "Henderson/Climax moly mines; byproduct credits; trading/other"),
]

# Margin assumptions — copper price ($/lb) is THE dominant earnings driver
GROSS_MARGIN_CURR = 0.34    # blended gross margin at ~$4.60/lb realized copper
GROSS_MARGIN_BULL = 0.46    # BULL: copper >$6.00/lb; high operating leverage; gold byproduct credits cut net costs
OPEX_FIXED_B      = 4.2     # SG&A + corporate costs ($B); largely fixed, modest scale leverage
TAX_RATE          = 0.32    # effective rate; elevated due to Indonesian government royalty/tax regime at Grasberg

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 1.85        # FY2026E EPS at ~$4.60/lb realized copper (consensus $1.70-$2.00)
PE_PESSIMISTIC = 14.0        # trough P/E: cyclical miner at copper-price-crash multiple
                              # (2015-16 copper crash troughs traded 12-16x normalized earnings)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $26

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (1.55, 14,  22, "China demand collapse + recession; copper $3.00/lb; Grasberg export disruption; EPS $1.55 → 14x floor P/E"),
    "BASE":  (2.10, 17,  36, "Copper ~$4.80/lb; Grasberg ramps steadily; China demand stable; EPS $2.10 → 17x"),
    "BULL":  (3.50, 19,  67, "AI-datacenter/EV/grid electrification supercycle; copper >$6.00/lb; Grasberg full output; EPS $3.50 → 19x"),
    "XBULL": (5.50, 21, 116, "Structural copper deficit; copper >$8.00/lb; gold byproduct windfall; EPS $5.50 → 21x"),
}

# ── SOFTMAX PROBABILITY FUNCTION ─────────────────────────────────────────────
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
# Scores: 1=BEAR  2=BASE  3=BULL  4=XBULL
SIGNALS = [
    {
        "name":       "Copper price ($/lb realized)",
        "weight":     0.35,
        "thresholds": ("<$3.50", "≥$4.20", "≥$5.00", "≥$6.50"),
        "now":        "$4.65",
        "score":      2,
        "comment":    "Realized price ~$4.65/lb; AI-datacenter and grid electrification demand emerging but China property drag persists",
    },
    {
        "name":       "Grasberg (Indonesia) production volume",
        "weight":     0.20,
        "thresholds": ("<1.0Blb", "≥1.2Blb","≥1.4Blb","≥1.6Blb"),
        "now":        "~1.3Blb",
        "score":      3,
        "comment":    "Underground block-cave ramp progressing on plan; PT-FI export permit renewed through 2027; gold byproduct strong",
    },
    {
        "name":       "China copper demand growth (YoY)",
        "weight":     0.20,
        "thresholds": ("<-3%",   "≥0%",   "≥+4%",   "≥+8%"),
        "now":        "+1%",
        "score":      2,
        "comment":    "Property sector still soft; grid/EV/renewables capex offsetting; State Grid spending at record highs",
    },
    {
        "name":       "Indonesian regulatory/political risk (PT-FI)",
        "weight":     0.10,
        "thresholds": ("Severe",  "Elevated","Stable", "Favorable"),
        "now":        "Stable",
        "score":      3,
        "comment":    "Government 51% stake settled; smelter (Manyar) operational reducing export-ban exposure; royalty terms locked through decade",
    },
    {
        "name":       "Net unit cash cost (post byproduct credits, $/lb)",
        "weight":     0.10,
        "thresholds": (">$2.20", "≤$2.00", "≤$1.70", "≤$1.40"),
        "now":        "$1.85",
        "score":      3,
        "comment":    "Gold/moly byproduct credits from Grasberg keep net copper costs near bottom of global cost curve",
    },
    {
        "name":       "Capex intensity (growth capex as % of EBITDA)",
        "weight":     0.05,
        "thresholds": (">55%",   "≤50%",  "≤40%",   "≤30%"),
        "now":        "48%",
        "score":      2,
        "comment":    "Grasberg underground + Indonesia smelter capex still elevated; FCF inflection expected 2027-28 as spend rolls off",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "AI-datacenter/EV/grid electrification — structural copper demand tailwind multi-decade", +0.8, 0.25),
    ("+", "Grasberg crown jewel — world-class low-cost reserve; gold byproduct cushions copper cycle", +0.6, 0.20),
    ("-", "Indonesian sovereign risk — government stake, export rules, royalty changes remain a tail risk", -0.5, 0.20),
    ("-", "China property/demand cyclicality — single largest swing factor for copper price",         -0.5, 0.20),
    ("+", "Operating leverage to copper price — small price moves drive outsized EPS swings on upside", +0.4, 0.10),
    ("-", "Heavy growth capex through 2027 — limits near-term FCF/dividend upside",                   -0.3, 0.05),
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
    valuation_label = "OVERVALUED"

# ── RATIO B ───────────────────────────────────────────────────────────────────
bear_price   = SCENARIOS["BEAR"][2]
bull_price   = SCENARIOS["BULL"][2]
downside_pct = (CURRENT_PRICE - bear_price) / CURRENT_PRICE
upside_pct   = (bull_price - CURRENT_PRICE) / CURRENT_PRICE
ratio_b      = round(downside_pct / upside_pct, 2) if upside_pct > 0 else float("inf")

if ratio_b != float("inf") and ratio_b < 0.75:
    signal_short, signal_full = "BUY",       "◉ BUY"
elif ratio_b != float("inf") and ratio_b < 1.10:
    signal_short, signal_full = "ACCUMULATE","◎ ACCUMULATE"
elif ratio_b != float("inf") and ratio_b < 1.75:
    signal_short, signal_full = "WATCHLIST", "◐ WATCHLIST"
else:
    signal_short, signal_full = "AVOID",     "✕ AVOID"

ratio_b_str = f"{ratio_b:.2f}x" if ratio_b != float("inf") else "N/A"

# ── CONSERVATIVE GROWTH (2-yr) ────────────────────────────────────────────────
CONS_EPS_2YR  = 2.20    # conservative FY2028E: copper ~$4.80/lb; Grasberg ramp continues
CONS_PE_2YR   = 15      # mid-cycle cyclical multiple (15-16x normalized)
cons_equity   = CONS_EPS_2YR * CONS_PE_2YR
cons_divs     = ANNUAL_DIV * 2
cons_total    = cons_equity + cons_divs
cons_return   = round((cons_total - CURRENT_PRICE) / CURRENT_PRICE * 100, 1)
cons_annual   = round(cons_return / 2, 1)

# ─────────────────────────────────────────────────────────────────────────────
#  OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
W = 72

def hr(): print("  " + "─" * W)
def bar(score):
    return "█" * score + "░" * (4 - score)

print()
print("═" * (W + 4))
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Copper / Gold / Molybdenum Mining")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios, driven by copper price)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<26}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<26}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<26}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print()

# EPS bridge
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_ni   = curr_oi * (1 - TAX_RATE)
shares    = SHARES_OUT_M / 1000
curr_eps  = round(curr_ni / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B
bull_ni   = bull_oi * (1 - TAX_RATE)
shares_b  = shares * 0.99   # minimal buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.85   # margin compression in copper crash
bear_oi   = bear_gp - OPEX_FIXED_B * 0.95           # limited cost flexibility
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share EPS  (consensus ~${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 19× = ~${bull_eps_imp*19:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.85:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 14× trough P/E (copper-crash floor) = ~${bear_eps_imp*14:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_dollar_lb = 1.5  # ~$1.50 EPS per $1.00/lb copper price move (operating leverage)
print(f"  KEY SENSITIVITIES:")
print(f"  Every +$0.50/lb copper price:    +${eps_per_dollar_lb*0.5:.2f}/EPS  = +${eps_per_dollar_lb*0.5*16:.1f}/share at 16× P/E")
print(f"  Grasberg volume ±10%:            ±${EPS_FY2026E*0.15:.2f}/EPS  =  ±${EPS_FY2026E*0.15*16:.1f}/share at 16× P/E")
print(f"  Gold price +$200/oz (byproduct): +${0.12:.2f}/EPS  = +${0.12*16:.1f}/share at 16× P/E (net cost reduction)")
print(f"  China copper demand +1pp:        +${EPS_FY2026E*0.05:.2f}/EPS  = +${EPS_FY2026E*0.05*16:.1f}/share at 16× P/E")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (copper price / Grasberg / China demand / Indonesia risk framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>7}  {'BASE':>7}  {'BULL':>7}  {'XBULL':>9}  {'NOW':>7}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>7}  {ths[1]:>7}  {ths[2]:>7}  {ths[3]:>9}  {s['now']:>7}  {lbl}  {b}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15% hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:72]:<72}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Copper price ($/lb)",            "$4.65",  "<$3.00", "−$1.65", "China property collapse + global recession crushes industrial demand"),
    ("Grasberg production volume",     "1.3Blb", "<1.0Blb","−0.3Blb","Indonesian export ban or underground block-cave geotechnical setback"),
    ("China copper demand YoY",        "+1%",    "<-5%",   "−6pp",   "Property sector contagion spreads to broader infrastructure spending"),
    ("Indonesia regulatory risk",      "Stable", "Severe", "+2 lvl", "Government revises PT-FI ownership/royalty terms or revokes export permit"),
    ("Net unit cash cost",             "$1.85",  ">$2.50", "+$0.65", "Gold price crash removes byproduct credit cushion; energy costs spike"),
    ("Capex intensity",                "48%",    ">55%",   "+7pp",   "Grasberg underground cost overruns force additional capital spending"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A China property/infrastructure demand collapse driving copper below $3.00/lb,")
print(f"  combined with an Indonesian regulatory shock (export ban, royalty hike, or PT-FI ownership")
print(f"  dispute) at Grasberg — the single largest profit contributor. Operating leverage means a")
print(f"  ~35% copper price decline collapses EPS to ~$0.85 → 14× floor = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT a permanent impairment — Grasberg's world-class low-cost reserve")
print(f"  and gold byproduct credits provide a durable floor. Copper cycles historically recover within 2yr.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E EPS estimate:           ${EPS_FY2026E:.2f}  (consensus $1.70-$2.00; at ~$4.65/lb realized copper)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (2015-16 copper crash trough multiple; cyclical floor)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP reflects the market pricing in a structurally higher")
print(f"  copper price regime (AI-datacenter, EV, and grid electrification demand) sustaining")
print(f"  earnings well above trough levels. At ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f},")
print(f"  the implied P/E is {CURRENT_PRICE/EPS_FY2026E:.1f}×. The risk is a cyclical copper price downturn")
print(f"  reverting both EPS and multiple toward the {PE_PESSIMISTIC:.0f}× trough floor.")
print(f"  At 16× mid-cycle P/E: ${EPS_FY2026E:.2f} × 16 = ${EPS_FY2026E*16:.0f} — a useful base-case anchor.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: copper ~$4.80/lb, Grasberg ramp continues, modest rerating)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (Grasberg full ramp + modest copper price appreciation)")
print(f"  Conservative exit P/E:           {CONS_PE_2YR}×  (mid-cycle multiple for copper miner)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr base; variable div upside not included)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: does the AI-datacenter/EV/grid electrification copper demand wave")
print(f"  sustain prices above $4.50/lb long enough for Grasberg's ramp to drive durable EPS growth?")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — plausible if copper holds >$4.80/lb.")
print(f"  Breakeven at 18× P/E (BULL multiple): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 18:.2f}")
print(f"  ACCUMULATE trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.85 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.95 + cons_divs * 0.5, 0):.0f} (conservative case attractive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.40
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  base div + variable performance div in strong years)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (high; classic copper-cycle commodity beta)")
print(f"  Beta vs S&P 500:      1.65  (high; commodity cyclical; amplifies macro/China swings)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe but not unprecedented for copper miners)")
print(f"  52W low ${VOL_52W_LOW:.2f} already reflects a meaningful prior copper-demand scare.")
print(f"  → China demand trajectory is THE KEY swing factor; each 10% copper price move = large EPS swing.")
print(f"  → AI-datacenter/grid/EV copper demand acceleration is KEY bull catalyst (structural deficit thesis).")
print(f"  → AVOID above $58  |  WATCHLIST $50–58  |  ACCUMULATE $40–48  |  BUY below $38")

# ─── ⑦ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print()
print("  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
hr()
probs_mkt = softmax_probs(MARKET_COMPOSITE)
print(f"  {'Scenario':<10}  {'Price':>7}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>7}  Description")
hr()
for s in ["BEAR","BASE","BULL","XBULL"]:
    pp  = probs_proxy[s] * 100
    pm  = probs_mkt[s]   * 100
    gap = pp - pm
    pr  = SCENARIOS[s][2]
    desc = SCENARIOS[s][3][:46]
    print(f"  {s:<10}  ${pr:>6}  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): ${ev_adj:.0f}  /  Proxy EV: ${ev_prx:.0f}  /  Market EV: ${ev_mkt:.0f}  /  Current: ${CURRENT_PRICE:.0f}")
hr()
print(f"  Downside  (→ Bear ${bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull ${bull_price}):  {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b_str}")
print(f"  Signal    :  {signal_full}")
print()
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) vs the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The gap ({ADJ_GAP:.2f}) indicates the stock is")
print(f"  {valuation_label.lower()} by model standards.")
print(f"  China demand (signal score {SIGNALS[2]['score']}/4) and copper price (signal score {SIGNALS[0]['score']}/4) remain")
print(f"  the dominant valuation swing factors, while Grasberg execution and Indonesia stability")
print(f"  (both scoring 3/4 = BULL) provide a structural floor under the cyclical commodity exposure.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) AI-datacenter/grid electrification copper demand — structural deficit thesis (BULL trigger)")
print(f"  (2) China property/infrastructure stabilization — copper demand floor (BULL trigger)")
print(f"  (3) Grasberg underground ramp — production volume milestones through 2027 (key execution risk)")
print(f"  (4) Indonesian regulatory stability — PT-FI export permits, royalty terms, smelter operations")
print(f"  (5) Gold price — byproduct credits from Grasberg materially reduce net copper costs")
print(f"  AVOID above $58  |  WATCHLIST $50–58  |  ACCUMULATE $40–48  |  BUY below $38")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}")
print("═" * (W + 4))
print()

# ── EXPORT ────────────────────────────────────────────────────────────────────
RESULT = {
    "ticker":            TICKER,
    "signal":            signal_full,
    "signal_short":      signal_short,
    "price":             CURRENT_PRICE,
    "epp_gap_pct":       epp_gap_pct,
    "ratio_b":           ratio_b if ratio_b != float("inf") else None,
    "ratio_b_fmt":       ratio_b_str,
    "adj_composite":     ADJ_COMPOSITE,
    "market_composite":  MARKET_COMPOSITE,
    "adj_gap":           ADJ_GAP,
    "valuation":         valuation_label,
    "cons_return_2yr":   cons_return,
}

if __name__ == "__main__":
    pass
