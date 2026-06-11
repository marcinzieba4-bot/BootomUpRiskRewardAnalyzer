"""
NEE  ·  NextEra Energy, Inc.  ·  NYSE: NEE
Bottom-up signal model  ·  Regulated Electric Utility (FPL) + Renewables (NextEra Energy Resources) · AI/Data-Center Load Growth
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "NEE"
COMPANY       = "NextEra Energy, Inc."
SECTOR        = "Regulated Electric Utility (FPL) + Renewables (NEER) · NYSE: NEE"
CURRENT_PRICE = 75.00      # USD; as of 2026-06-11
VOL_52W_LOW   = 60.00
VOL_52W_HIGH  = 85.00
SHARES_OUT_M  = 2050.0     # millions

# Dividend
ANNUAL_DIV    = 2.12       # $/share; ~10%/yr dividend growth target

# ── RENEWABLES BACKLOG / RATE BASE GROWTH ANALYSIS (company-specific) ─────────
RENEWABLES_BACKLOG_GROWTH = 0.12   # ~12% YoY growth in NEER renewables/storage backlog
FPL_RATE_BASE_GROWTH      = 0.09   # ~9%/yr regulated rate base growth at FPL
INCREMENTAL_MARGIN        = 0.45   # incremental operating margin on new renewables/rate base additions
TAX_RATE                  = 0.21

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 3.65    # FY2026E adj EPS
PE_TROUGH = 14      # min P/E at crisis trough (rate-shock/utility distress multiple)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $51

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (3.30, 14,   46, "Long-term rates rise further, compressing utility/renewables multiples; renewables backlog growth slows; EPS $3.30 -> 14x distress P/E"),
    "BASE":  (3.65, 21,   77, "FPL rate base +9%/yr; renewables backlog +10-12%; dividend grows ~10%/yr; EPS $3.65 -> 21x P/E"),
    "BULL":  (4.10, 24,   98, "AI/data-center load growth in Florida and contracted renewables accelerates backlog conversion; EPS $4.10 -> 24x premium P/E"),
    "XBULL": (4.70, 27,  127, "Multi-year renewables buildout supercycle plus battery storage scale drive sustained double-digit EPS growth; EPS $4.70 -> 27x peak P/E"),
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
        "name":       "Renewables (NEER) backlog — YoY growth",
        "weight":     0.25,
        "thresholds": ("<5%",   "≥8%",   "≥10%",  "≥14%"),
        "now":        "~12%",
        "score":      3,
        "comment":    "~12%; record backlog of wind/solar/storage projects under contract supports multi-year growth",
    },
    {
        "name":       "FPL regulated rate base growth",
        "weight":     0.20,
        "thresholds": ("<5%",   "≥6%",   "≥8%",   "≥10%"),
        "now":        "~9%",
        "score":      3,
        "comment":    "~9%/yr; constructive Florida regulatory framework supports steady capital deployment",
    },
    {
        "name":       "AI/data-center load growth (Florida + contracted)",
        "weight":     0.15,
        "thresholds": ("<2%",   "≥4%",   "≥6%",   "≥9%"),
        "now":        "~6%",
        "score":      3,
        "comment":    "~6%; Florida population growth plus emerging data-center demand support load growth",
    },
    {
        "name":       "Adjusted EPS growth rate",
        "weight":     0.15,
        "thresholds": ("<4%",   "≥6%",   "≥8%",   "≥10%"),
        "now":        "~8%",
        "score":      3,
        "comment":    "~8%; near top of management's 6-8% long-term EPS growth guidance range",
    },
    {
        "name":       "Dividend growth rate",
        "weight":     0.10,
        "thresholds": ("<6%",   "≥8%",   "≥10%",  "≥12%"),
        "now":        "~10%",
        "score":      3,
        "comment":    "~10%/yr; long-standing track record of double-digit dividend growth",
    },
    {
        "name":       "Battery storage deployment growth",
        "weight":     0.15,
        "thresholds": ("<20%",  "≥30%",  "≥40%",  "≥60%"),
        "now":        "~45%",
        "score":      3,
        "comment":    "~45%; storage attach rate on new renewables projects rising rapidly, adding margin",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Largest regulated utility (FPL) plus largest renewables developer (NEER) in the US — scale and origination moat", +0.5, 0.25),
    ("+", "Constructive Florida regulatory framework provides a stable earnings base to fund renewables growth",              +0.3, 0.20),
    ("+", "AI/data-center demand growth provides incremental upside to both FPL load and contracted renewables backlog",      +0.3, 0.15),
    ("-", "Elevated leverage and ongoing equity issuance needs to fund the growth capex plan dilute per-share growth",         -0.4, 0.20),
    ("-", "Bond-proxy interest-rate sensitivity — sustained higher long-term rates compress the multiple",                     -0.4, 0.20),
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
CONS_EPS_2YR = 4.20    # conservative FY2028E: FPL rate base + renewables backlog conversion continue
CONS_PE_2YR  = 19       # floor multiple (slightly below current)
cons_equity  = CONS_EPS_2YR * CONS_PE_2YR
cons_divs    = ANNUAL_DIV * 2 * 1.10   # approximate dividend growth across the 2yr window
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Regulated Utility (FPL) + Renewables (NEER)")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① RENEWABLES BACKLOG / RATE BASE ANALYSIS ───────────────────────────────
print()
print("  RENEWABLES BACKLOG + RATE BASE GROWTH ANALYSIS  (the core NEE earnings drivers)")
hr()
shares_b = SHARES_OUT_M / 1000
total_revenue_b = 28.0
print(f"  Estimated FY2026E revenue base: ~${total_revenue_b:.1f}B")
print()
print(f"  GROWTH UPSIDE  (incremental EPS from rate base + backlog growth at {INCREMENTAL_MARGIN*100:.0f}% incremental margin):")
print(f"  {'Combined growth rate':<20}  {'Rev/yr ($B)':>12}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.00, 0.06, 0.09, 0.12]:
    rev_inc = total_revenue_b * g
    inc_eps = rev_inc * INCREMENTAL_MARGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% combined growth        +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
print(f"  RENEWABLES BACKLOG  (~{RENEWABLES_BACKLOG_GROWTH*100:.0f}%/yr growth in contracted wind/solar/storage projects;")
print(f"  conversion to in-service assets drives multi-year EPS visibility independent of FPL rate cases).")
print()
print(f"  BEAR (${bear_price}) requires: long-term rates rise further, compressing utility/renewables")
print(f"  multiples AND renewables backlog growth slows materially — together.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (renewables backlog + FPL rate base + AI load + EPS growth + dividend + storage)")
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
    ("Renewables (NEER) backlog growth",           "~12%",   "<5%",   "-7pp",   "Tax credit changes or financing costs slow new project signings"),
    ("FPL regulated rate base growth",             "~9%",    "<5%",   "-4pp",   "Florida PSC rate case outcome disappoints; capex plan trimmed"),
    ("AI/data-center load growth",                 "~6%",    "<2%",   "-4pp",   "Data-center buildout in Florida slows amid macro softness"),
    ("Adjusted EPS growth",                        "~8%",    "<4%",   "-4pp",   "Higher financing costs offset rate base/backlog growth"),
    ("Dividend growth rate",                       "~10%",   "<6%",   "-4pp",   "Management trims dividend growth target to preserve balance sheet"),
    ("Battery storage deployment growth",          "~45%",   "<20%",  "-25pp",  "Supply chain or interconnection delays slow storage attach rate"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Long-term rates rise further, compressing utility/renewables multiples, while")
print(f"  tax-credit changes or financing costs slow new renewables project signings and rate case outcomes disappoint.")
print(f"  EPS falls to ~$3.30; multiple compresses to 14x distress P/E = ${bear_price}.")

# ─── ③ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS x min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}")
print(f"  Min viable P/E at trough:      {PE_TROUGH}x  (rate-shock/utility distress multiple)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct>=0 else 'below'} trough floor)")
print()
print(f"  Premium to EPP reflects the renewables scale moat, regulated FPL base, and double-digit dividend growth.")
print(f"  Bear ${bear_price} is below EPP ${EPP:.0f} — would require both EPS pressure AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+0.30:.2f} x {PE_TROUGH}x = ${(EPP_EPS+0.3)*PE_TROUGH:.0f} EPP — rate base/backlog growth compounds the floor higher.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: rate base + backlog growth moderate, dividend growth continues)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (FPL rate base + renewables backlog conversion continue)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (slightly below current)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (~10%/yr dividend growth)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — regulated FPL earnings plus contracted")
print(f"  renewables backlog conversion and dividend growth support steady total returns even in a soft macro.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.20
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (above-average for a utility; rate-sensitive bond-proxy)")
print(f"  Beta vs S&P 500:      0.45  (below market; defensive but rate-sensitive)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (NEE fell ~30% during the 2023 rate-shock selloff; tail risk, not base case)")
print(f"  -> Long-term rate trajectory and renewables backlog conversion are the PRIMARY catalysts;")
print(f"     falling rates + backlog conversion = upside; sustained higher rates = downside.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — mid range; not stretched relative to growth profile.")
print(f"  -> BUY $62-$68  |  TRIM $82+  |  AVOID above $90")

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
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees rate base + renewables backlog growth, tempered by leverage/rate-sensitivity SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing the renewables compounding story.' if ADJ_GAP>0 else 'model roughly agrees with market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) Renewables backlog -> sustained >=10% growth confirms originate-to-build pipeline")
print(f"  (2) FPL rate base -> capex plan execution stays >=8%/yr")
print(f"  (3) AI/data-center load growth -> Florida demand accelerates beyond population growth")
print(f"  (4) Battery storage attach rate -> continued scale-up adds incremental margin")
print(f"  BUY $62-{round(CURRENT_PRICE*0.90,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $82  |  AVOID above $90")
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
