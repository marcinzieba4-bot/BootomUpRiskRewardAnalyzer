"""
EXC  ·  Exelon Corporation  ·  NASDAQ: EXC
Bottom-up signal model  ·  Regulated Electric & Gas T&D Utility (ComEd/PECO/BGE/Pepco/Delmarva/ACE) · PJM Data-Center Load Growth
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "EXC"
COMPANY       = "Exelon Corporation"
SECTOR        = "Regulated Electric & Gas T&D Utility · Chicago/PA/MD-DC · NASDAQ: EXC"
CURRENT_PRICE = 45.00     # USD; as of 2026-06-11
VOL_52W_LOW   = 38.00
VOL_52W_HIGH  = 48.00
SHARES_OUT_M  = 1000.0     # millions

# Dividend
ANNUAL_DIV    = 1.60       # $/share; ~3.6% yield, ~6%/yr dividend growth

# ── RATE BASE / LOAD GROWTH ANALYSIS (company-specific) ───────────────────────
RATE_BASE_GROWTH   = 0.075   # ~7.5%/yr regulated T&D rate base growth (6-utility capex plan)
DATA_CENTER_GROWTH = 0.06    # ~6% incremental load growth from ComEd/PECO/BGE/Pepco data-center pipeline
INCREMENTAL_MARGIN = 0.40    # incremental operating margin on new rate base / load growth
TAX_RATE           = 0.21

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 2.50    # FY2026E adj EPS
PE_TROUGH = 13      # min P/E at crisis trough (rate-shock/utility distress multiple)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $33

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (2.30, 12,   28,  "Multi-state rate case outcomes disappoint and PJM transmission revenue growth stalls; multiples compress; EPS $2.30 -> 12x distress P/E"),
    "BASE":  (2.50, 18,   45, "Regulated T&D rate base +7.5%/yr across the six-utility platform; ComEd/PECO/BGE data-center load growth continues; EPS $2.50 -> 18x P/E"),
    "BULL":  (2.75, 21,   58,  "PJM data-center load growth accelerates beyond plan across ComEd/PECO/BGE/Pepco territories; EPS $2.75 -> 21x premium P/E"),
    "XBULL": (3.05, 24,   73,  "Multi-year PJM data-center buildout supercycle drives sustained above-plan rate base growth across the six-utility platform; EPS $3.05 -> 24x peak P/E"),
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
        "name":       "PJM data-center load growth (ComEd/PECO/BGE/Pepco/DPL/ACE)",
        "weight":     0.30,
        "thresholds": ("<2%",   "≥4%",   "≥6%",   "≥9%"),
        "now":        "~6%",
        "score":      3,
        "comment":    "~6%; rapidly growing PJM data-center interconnection queues across Chicago, eastern PA, and the Maryland/DC corridor",
    },
    {
        "name":       "Adjusted EPS growth rate",
        "weight":     0.15,
        "thresholds": ("<4%",   "≥5%",   "≥6%",   "≥8%"),
        "now":        "~6%",
        "score":      3,
        "comment":    "~6%; tracking within management's 5-7% long-term EPS growth guidance range",
    },
    {
        "name":       "Regulatory ROE / multi-state rate case outcomes",
        "weight":     0.20,
        "thresholds": ("<8.5%", "≥9.0%", "≥9.4%", "≥9.8%"),
        "now":        "~9.2%",
        "score":      2,
        "comment":    "~9.2% blended allowed ROE; rate cases across IL/PA/MD/DE/NJ/DC have been mixed-to-constructive on grid capex recovery",
    },
    {
        "name":       "Grid modernization / reliability capex execution",
        "weight":     0.15,
        "thresholds": ("Behind plan", "On track", "Ahead of plan", "Accelerated"),
        "now":        "Ahead of plan",
        "score":      3,
        "comment":    "Six-utility grid modernization plan running ahead of plan, supporting the elevated rate base growth trajectory",
    },
    {
        "name":       "PJM capacity price realization (transmission revenue)",
        "weight":     0.10,
        "thresholds": ("Declining", "Flat", "Rising", "Sharply rising"),
        "now":        "Rising",
        "score":      3,
        "comment":    "Elevated PJM capacity auction prices driven by data-center demand support transmission formula-rate revenue growth",
    },
    {
        "name":       "Dividend growth rate",
        "weight":     0.10,
        "thresholds": ("<3%",   "≥4%",   "≥5%",   "≥7%"),
        "now":        "~6%",
        "score":      2,
        "comment":    "~6%/yr; consistent with management's targeted 5-7% long-term dividend growth, slightly below top of range",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Pure-play T&D platform across six utilities (ComEd/PECO/BGE/Pepco/DPL/ACE) sits in major PJM data-center corridors", +0.5, 0.25),
    ("+", "Elevated PJM capacity auction prices driven by data-center demand boost transmission formula-rate revenue growth",   +0.3, 0.20),
    ("+", "Simplified pure-play regulated T&D story post generation spinoff improves earnings predictability",                  +0.3, 0.15),
    ("-", "Multi-state regulatory complexity (6 jurisdictions) creates rate case timing/ROE compression risk",                  -0.4, 0.20),
    ("-", "Elevated grid modernization capex requires ongoing equity issuance, diluting per-share growth",                       -0.3, 0.20),
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
CONS_EPS_2YR = 2.75    # conservative FY2028E: rate base growth + PJM data-center load growth continue
CONS_PE_2YR  = 17       # floor multiple (slightly below current)
cons_equity  = CONS_EPS_2YR * CONS_PE_2YR
cons_divs    = ANNUAL_DIV * 2 * 1.06   # approximate dividend growth across the 2yr window
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Regulated Multi-State T&D Utility")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① RATE BASE / LOAD GROWTH ANALYSIS ──────────────────────────────────────
print()
print("  RATE BASE + DATA-CENTER LOAD GROWTH ANALYSIS  (the core EXC earnings drivers)")
hr()
shares_b = SHARES_OUT_M / 1000
total_revenue_b = 24.0
print(f"  Estimated FY2026E revenue base: ~${total_revenue_b:.1f}B")
print()
print(f"  GROWTH UPSIDE  (incremental EPS from rate base + load growth at {INCREMENTAL_MARGIN*100:.0f}% incremental margin):")
print(f"  {'Combined growth rate':<20}  {'Rev/yr ($B)':>12}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.00, 0.05, 0.08, 0.12]:
    rev_inc = total_revenue_b * g
    inc_eps = rev_inc * INCREMENTAL_MARGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% combined growth        +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
print(f"  PJM DATA-CENTER LOAD GROWTH  (~{DATA_CENTER_GROWTH*100:.0f}% incremental load growth from announced ComEd/PECO/BGE/")
print(f"  Pepco data-center pipeline; converts directly into rate base additions under existing regulatory frameworks).")
print()
print(f"  BEAR (${bear_price}) requires: multi-state rate case outcomes disappoint")
print(f"  AND PJM transmission revenue growth stalls, compressing the multiple — together.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (PJM data-center load + EPS growth + ROE + grid capex + capacity prices + dividend)")
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
    ("PJM data-center load growth",                "~6%",    "<2%",   "-4pp",   "Announced data-center projects delayed on grid-interconnection constraints"),
    ("Adjusted EPS growth",                        "~6%",    "<4%",   "-2pp",   "Higher financing costs and dilution offset rate base growth"),
    ("Regulatory ROE / rate case outcomes",        "~9.2%",  "<8.5%", "-0.7pp", "Multiple jurisdictions deliver disappointing rate case outcomes"),
    ("Grid modernization capex execution",         "Ahead of plan","Behind plan","-","Cost overruns or supply-chain delays slow the capex plan"),
    ("PJM capacity price realization",             "Rising", "Declining","-",  "PJM capacity prices roll over from data-center-driven highs"),
    ("Dividend growth rate",                       "~6%",    "<3%",   "-3pp",   "Capital allocation shifts toward balance sheet repair"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Multi-state rate case outcomes disappoint across the six-utility platform just as PJM")
print(f"  capacity prices roll over from data-center-driven highs, compressing both EPS and the multiple.")
print(f"  EPS falls to ~$2.30; multiple compresses to 12x distress P/E = ${bear_price}.")

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
print(f"  Premium to EPP reflects the unmatched PJM data-center T&D footprint and visible capex-driven rate base growth.")
print(f"  Bear ${bear_price} is below EPP ${EPP:.0f} — would require both EPS pressure AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+0.20:.2f} x {PE_TROUGH}x = ${(EPP_EPS+0.2)*PE_TROUGH:.0f} EPP — rate base growth compounds the floor higher.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: rate base growth moderate, PJM data-center load growth continues)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (rate base growth + PJM data-center load growth)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (slightly below current)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (~6%/yr dividend growth)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — the ~3.6% dividend yield plus steady")
print(f"  rate base growth and the PJM data-center T&D footprint support total returns even in a soft macro.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.15
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (typical for a regulated T&D utility)")
print(f"  Beta vs S&P 500:      0.40  (below market; defensive but PJM-capacity-price-sensitive)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (EXC fell ~15% during prior multi-state rate case disappointments; tail risk, not base case)")
print(f"  -> PJM data-center load growth and multi-state rate case outcomes are the PRIMARY catalysts;")
print(f"     accelerating data-center demand + constructive rate cases = upside; rate case setbacks = downside.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — upper-middle of range; reflects strong PJM data-center sentiment.")
print(f"  -> BUY $40-$43  |  TRIM $52+  |  AVOID above $56")

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
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees PJM data-center T&D tailwind + rate base growth, tempered by multi-state ROE/dilution SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing the PJM data-center T&D story.' if ADJ_GAP>0 else 'model roughly agrees with market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) PJM data-center load growth -> announced ComEd/PECO/BGE/Pepco pipeline converts to in-service load")
print(f"  (2) Regulatory ROE -> constructive multi-state rate case outcomes")
print(f"  (3) Grid modernization capex -> six-utility plan stays on/ahead of pace")
print(f"  (4) PJM capacity prices -> data-center-driven demand keeps transmission revenue growing")
print(f"  BUY $40-{round(CURRENT_PRICE*0.90,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $52  |  AVOID above $56")
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
