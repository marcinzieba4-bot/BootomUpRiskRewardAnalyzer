"""
PEG  ·  Public Service Enterprise Group Incorporated  ·  NYSE: PEG
Bottom-up signal model  ·  Regulated Electric & Gas Utility · NJ Transmission + Nuclear Fleet · PJM Data-Center Load Growth
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "PEG"
COMPANY       = "Public Service Enterprise Group Incorporated"
SECTOR        = "Regulated Electric & Gas Utility · NJ Transmission + Nuclear Fleet · NYSE: PEG"
CURRENT_PRICE = 95.00     # USD; as of 2026-06-11
VOL_52W_LOW   = 78.00
VOL_52W_HIGH  = 102.00
SHARES_OUT_M  = 500.0      # millions

# Dividend
ANNUAL_DIV    = 2.60       # $/share; ~2.7% yield, ~6%/yr dividend growth

# ── RATE BASE / LOAD GROWTH ANALYSIS (company-specific) ───────────────────────
RATE_BASE_GROWTH   = 0.075   # ~7.5%/yr regulated transmission/distribution rate base growth
DATA_CENTER_GROWTH = 0.06    # ~6% incremental load growth from NJ/PJM data-center pipeline
INCREMENTAL_MARGIN = 0.40    # incremental operating margin on new rate base / load growth
TAX_RATE           = 0.21

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 3.85    # FY2026E adj EPS
PE_TROUGH = 16      # min P/E at crisis trough (rate-shock/utility distress multiple)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $62

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (3.50, 15,   53,  "PJM capacity prices roll over and a nuclear unit faces an unplanned outage; multiples compress; EPS $3.50 -> 15x distress P/E"),
    "BASE":  (4.20, 23,   97, "Regulated T&D rate base +7.5%/yr; PJM data-center load growth lifts nuclear fleet capacity factors and prices; EPS $4.20 -> 23x P/E"),
    "BULL":  (4.60, 26,   120, "PJM capacity auction prices stay elevated on data-center demand; nuclear fleet runs near-100% capacity factor; EPS $4.60 -> 26x premium P/E"),
    "XBULL": (5.10, 29,   148, "Multi-year PJM data-center buildout supercycle drives sustained elevated capacity prices and accelerated rate base growth; EPS $5.10 -> 29x peak P/E"),
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
        "name":       "NJ/PJM data-center load growth",
        "weight":     0.30,
        "thresholds": ("<2%",   "≥4%",   "≥6%",   "≥9%"),
        "now":        "~6%",
        "score":      3,
        "comment":    "~6%; rapidly growing PJM data-center interconnection queue across central/northern New Jersey",
    },
    {
        "name":       "Nuclear fleet (Salem/Hope Creek) capacity factor & ZEC support",
        "weight":     0.15,
        "thresholds": ("<88%",  "≥92%",  "≥95%",  "≥97%"),
        "now":        "~95%",
        "score":      3,
        "comment":    "~95% capacity factor; NJ zero-emission credit program continues to support nuclear economics",
    },
    {
        "name":       "Adjusted EPS growth rate",
        "weight":     0.15,
        "thresholds": ("<5%",   "≥6%",   "≥8%",   "≥10%"),
        "now":        "~8%",
        "score":      3,
        "comment":    "~8%; tracking within management's 6-8% long-term EPS growth guidance range",
    },
    {
        "name":       "Regulatory ROE / NJ BPU rate case outcomes",
        "weight":     0.20,
        "thresholds": ("<9.0%", "≥9.5%", "≥9.8%", "≥10.2%"),
        "now":        "~9.6%",
        "score":      2,
        "comment":    "~9.6% blended allowed ROE; NJ BPU rate case outcomes have been mixed-to-constructive on T&D capex recovery",
    },
    {
        "name":       "Energy transition / non-core divestiture progress",
        "weight":     0.10,
        "thresholds": ("Reversed", "Stalled", "On track", "Complete"),
        "now":        "On track",
        "score":      3,
        "comment":    "Offshore wind exit and non-core fossil divestitures complete, leaving a simplified regulated T&D + nuclear platform",
    },
    {
        "name":       "Dividend growth rate",
        "weight":     0.10,
        "thresholds": ("<2%",   "≥4%",   "≥6%",   "≥8%"),
        "now":        "~6%",
        "score":      3,
        "comment":    "~6%/yr; consistent with management's targeted 5-7% long-term dividend growth",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Elevated PJM capacity auction prices driven by data-center demand directly benefit the nuclear fleet's economics", +0.5, 0.25),
    ("+", "Central/northern New Jersey data-center pipeline provides a multi-year T&D rate base growth tailwind",             +0.4, 0.20),
    ("+", "Simplified pure-play regulated T&D + nuclear platform post non-core divestitures improves earnings predictability", +0.3, 0.15),
    ("-", "PJM capacity market price volatility and potential regulatory price caps create earnings uncertainty",              -0.4, 0.20),
    ("-", "Nuclear relicensing timelines and ZEC policy renewal risk remain multi-year overhangs",                             -0.3, 0.20),
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
CONS_EPS_2YR = 4.55    # conservative FY2028E: rate base growth + PJM data-center-driven nuclear economics continue
CONS_PE_2YR  = 22       # floor multiple (slightly below current)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Regulated NJ Transmission + Nuclear Utility")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① RATE BASE / LOAD GROWTH ANALYSIS ──────────────────────────────────────
print()
print("  RATE BASE + DATA-CENTER LOAD GROWTH ANALYSIS  (the core PEG earnings drivers)")
hr()
shares_b = SHARES_OUT_M / 1000
total_revenue_b = 11.5
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
print(f"  PJM DATA-CENTER LOAD GROWTH  (~{DATA_CENTER_GROWTH*100:.0f}% incremental load growth from announced central/")
print(f"  northern New Jersey data-center pipeline; lifts both T&D rate base and nuclear fleet capacity-price realization).")
print()
print(f"  BEAR (${bear_price}) requires: PJM capacity prices roll over from data-center-driven highs")
print(f"  AND a nuclear unit suffers an unplanned outage, compressing the multiple — together.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (PJM data-center load + nuclear fleet + EPS growth + ROE + transition + dividend)")
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
    ("NJ/PJM data-center load growth",             "~6%",    "<2%",   "-4pp",   "Announced data-center projects delayed on grid-interconnection constraints"),
    ("Nuclear fleet capacity factor",              "~95%",   "<88%",  "-7pp",   "Unplanned outage at Salem or Hope Creek"),
    ("Adjusted EPS growth",                        "~8%",    "<5%",   "-3pp",   "PJM capacity price rollback offsets rate base growth"),
    ("Regulatory ROE / NJ BPU rate cases",         "~9.6%",  "<9.0%", "-0.6pp", "NJ BPU delivers disappointing rate case outcomes"),
    ("Energy transition / divestiture progress",   "On track","Stalled","-",    "Remaining non-core asset sales stall"),
    ("Dividend growth rate",                       "~6%",    "<2%",   "-4pp",   "Capital allocation shifts toward balance sheet repair"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: PJM capacity auction prices roll over from data-center-driven highs just as a nuclear unit")
print(f"  suffers an unplanned outage, compressing both the earnings base and the multiple.")
print(f"  EPS falls to ~$3.50; multiple compresses to 15x distress P/E = ${bear_price}.")

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
print(f"  Premium to EPP reflects the PJM data-center-driven nuclear capacity-price tailwind and visible T&D rate base growth.")
print(f"  Bear ${bear_price} is below EPP ${EPP:.0f} — would require both EPS pressure AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+0.35:.2f} x {PE_TROUGH}x = ${(EPP_EPS+0.35)*PE_TROUGH:.0f} EPP — rate base growth compounds the floor higher.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: rate base growth moderate, PJM data-center-driven nuclear economics continue)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (rate base growth + PJM data-center load growth)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (slightly below current)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (~6%/yr dividend growth)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — the ~2.7% dividend yield plus steady")
print(f"  rate base growth and the PJM data-center-driven nuclear capacity tailwind support total returns even in a soft macro.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.18
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (typical for a regulated utility with a nuclear fleet)")
print(f"  Beta vs S&P 500:      0.50  (below market; defensive but PJM-capacity-price-sensitive)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (PEG fell ~20% during prior PJM capacity-price downcycles; tail risk, not base case)")
print(f"  -> PJM data-center load growth and nuclear fleet capacity factors are the PRIMARY catalysts;")
print(f"     elevated capacity prices + high capacity factors = upside; price rollback + outages = downside.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — upper-middle of range; reflects strong PJM data-center sentiment.")
print(f"  -> BUY $86-$91  |  TRIM $112+  |  AVOID above $120")

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
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees PJM data-center-driven nuclear tailwind + rate base growth, tempered by capacity-price/policy SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing the PJM data-center-driven nuclear story.' if ADJ_GAP>0 else 'model roughly agrees with market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) PJM data-center load growth -> announced pipeline converts to in-service load")
print(f"  (2) Nuclear fleet -> Salem/Hope Creek capacity factors stay >=95% with continued ZEC support")
print(f"  (3) Regulatory ROE -> constructive NJ BPU rate case outcomes")
print(f"  (4) PJM capacity prices -> data-center-driven demand keeps capacity auction prices elevated")
print(f"  BUY $86-{round(CURRENT_PRICE*0.90,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $112  |  AVOID above $120")
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
