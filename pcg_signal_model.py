"""
PCG  ·  PG&E Corporation  ·  NYSE: PCG
Bottom-up signal model  ·  Regulated Electric & Gas Utility · California Wildfire Mitigation/Undergrounding · AI/Data-Center Load Growth
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "PCG"
COMPANY       = "PG&E Corporation"
SECTOR        = "Regulated Electric & Gas Utility · California · NYSE: PCG"
CURRENT_PRICE = 22.00     # USD; as of 2026-06-11
VOL_52W_LOW   = 14.00
VOL_52W_HIGH  = 24.00
SHARES_OUT_M  = 2200.0     # millions

# Dividend
ANNUAL_DIV    = 0.10       # $/share; modest dividend reinstated post-bankruptcy

# ── RATE BASE / LOAD GROWTH ANALYSIS (company-specific) ───────────────────────
RATE_BASE_GROWTH   = 0.10    # ~10%/yr regulated rate base growth (wildfire mitigation + grid capex)
DATA_CENTER_GROWTH = 0.04    # ~4% incremental load growth from CA data-center / EV adoption pipeline
INCREMENTAL_MARGIN = 0.40    # incremental operating margin on new rate base / load growth
TAX_RATE           = 0.21

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 1.50    # FY2026E adj EPS
PE_TROUGH = 12      # min P/E at crisis trough (wildfire-liability distress multiple)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $18

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (1.30, 11,   14,  "New major wildfire event reopens liability fears and triggers fresh equity issuance; EPS $1.30 -> 11x distress P/E"),
    "BASE":  (1.50, 16,   24, "Regulated rate base +10%/yr on wildfire mitigation/undergrounding capex; CA load growth continues; EPS $1.50 -> 16x P/E"),
    "BULL":  (1.80, 19,   34,  "Undergrounding program de-risks the wildfire profile ahead of plan; CA data-center/EV load growth accelerates; EPS $1.80 -> 19x premium P/E"),
    "XBULL": (2.10, 22,   46,  "Wildfire risk re-rating completes, dividend growth resumes, and a multi-year CA data-center buildout drives sustained above-plan rate base growth; EPS $2.10 -> 22x peak P/E"),
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
        "name":       "Wildfire mitigation / undergrounding progress",
        "weight":     0.25,
        "thresholds": ("<300mi/yr", "≥400mi/yr", "≥600mi/yr", "≥800mi/yr"),
        "now":        "~600mi/yr",
        "score":      3,
        "comment":    "~600 miles/yr of undergrounding; on pace with the multi-year plan to materially reduce ignition risk",
    },
    {
        "name":       "California data-center / EV load growth",
        "weight":     0.20,
        "thresholds": ("<1%",   "≥2%",   "≥4%",   "≥6%"),
        "now":        "~4%",
        "score":      3,
        "comment":    "~4%; growing data-center interconnection requests and EV adoption across the Bay Area and Central Valley",
    },
    {
        "name":       "Adjusted EPS growth rate",
        "weight":     0.15,
        "thresholds": ("<5%",   "≥7%",   "≥9%",   "≥12%"),
        "now":        "~9%",
        "score":      3,
        "comment":    "~9%; tracking within management's 9-10% long-term EPS growth guidance range, driven by elevated rate base growth",
    },
    {
        "name":       "Regulatory cost recovery / wildfire fund & securitization",
        "weight":     0.15,
        "thresholds": ("Underfunded", "Adequate", "Strong", "Fully de-risked"),
        "now":        "Adequate",
        "score":      2,
        "comment":    "CA wildfire fund and securitization mechanisms provide a meaningful liability backstop, though not yet fully de-risked",
    },
    {
        "name":       "Balance sheet / equity issuance trajectory",
        "weight":     0.10,
        "thresholds": ("Heavy dilution", "Elevated", "Moderating", "Self-funding"),
        "now":        "Moderating",
        "score":      2,
        "comment":    "Annual equity issuance to fund capex is moderating as securitization proceeds reduce the funding gap",
    },
    {
        "name":       "Dividend reinstatement / growth progress",
        "weight":     0.15,
        "thresholds": ("None", "Token", "Modest growth", "Meaningful growth"),
        "now":        "Token",
        "score":      1,
        "comment":    "Token $0.10/share dividend reinstated post-bankruptcy; meaningful growth not expected for several years",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Largest electric/gas utility in California with a regulated monopoly footprint and elevated allowed rate base growth", +0.4, 0.20),
    ("+", "CA wildfire fund and cost-recovery securitization materially reduce tail liability risk versus the pre-bankruptcy era", +0.4, 0.20),
    ("+", "California data-center and EV adoption pipeline provides a multi-year load-growth tailwind on top of the capex plan",   +0.3, 0.15),
    ("-", "Wildfire ignition / litigation tail risk remains the single largest overhang on the equity",                            -0.5, 0.25),
    ("-", "Heavy ongoing equity issuance to fund the undergrounding program continues to dilute per-share growth",                 -0.3, 0.20),
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
CONS_EPS_2YR = 1.80    # conservative FY2028E: rate base growth + CA data-center/EV load growth continue
CONS_PE_2YR  = 17       # floor multiple (slightly below current)
cons_equity  = CONS_EPS_2YR * CONS_PE_2YR
cons_divs    = ANNUAL_DIV * 2 * 1.05   # approximate dividend growth across the 2yr window
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Regulated California Electric & Gas Utility")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① RATE BASE / LOAD GROWTH ANALYSIS ──────────────────────────────────────
print()
print("  RATE BASE + DATA-CENTER LOAD GROWTH ANALYSIS  (the core PCG earnings drivers)")
hr()
shares_b = SHARES_OUT_M / 1000
total_revenue_b = 24.0
print(f"  Estimated FY2026E revenue base: ~${total_revenue_b:.1f}B")
print()
print(f"  GROWTH UPSIDE  (incremental EPS from rate base + load growth at {INCREMENTAL_MARGIN*100:.0f}% incremental margin):")
print(f"  {'Combined growth rate':<20}  {'Rev/yr ($B)':>12}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.00, 0.06, 0.10, 0.14]:
    rev_inc = total_revenue_b * g
    inc_eps = rev_inc * INCREMENTAL_MARGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% combined growth        +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
print(f"  CALIFORNIA DATA-CENTER / EV LOAD GROWTH  (~{DATA_CENTER_GROWTH*100:.0f}% incremental load growth from announced")
print(f"  Bay Area/Central Valley data-center pipeline and EV adoption; converts directly into rate base additions).")
print()
print(f"  BEAR (${bear_price}) requires: a new major wildfire event reopens liability fears")
print(f"  AND forces fresh equity issuance, compressing the multiple — together.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (undergrounding + CA load growth + EPS growth + cost recovery + balance sheet + dividend)")
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
    ("Wildfire mitigation / undergrounding pace",  "~600mi/yr","<300mi/yr","-300mi","Permitting delays or cost overruns slow the undergrounding program"),
    ("CA data-center / EV load growth",            "~4%",    "<1%",   "-3pp",   "Hyperscaler/EV pipeline slows on grid-interconnection constraints"),
    ("Adjusted EPS growth",                        "~9%",    "<5%",   "-4pp",   "Equity issuance and financing costs offset rate base growth"),
    ("Wildfire fund / cost recovery adequacy",     "Adequate","Underfunded","-","A new major wildfire event overwhelms the wildfire fund"),
    ("Balance sheet / equity issuance",            "Moderating","Heavy dilution","-","Liability event forces a large fresh equity raise"),
    ("Dividend reinstatement progress",            "Token",  "None",  "-",      "Capital allocation shifts entirely to liability funding"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A new major California wildfire event linked to PG&E equipment reopens liability fears,")
print(f"  overwhelms the wildfire fund, and forces a large fresh equity raise that dilutes per-share earnings.")
print(f"  EPS falls to ~$1.30; multiple compresses to 11x distress P/E = ${bear_price}.")

# ─── ③ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS x min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}")
print(f"  Min viable P/E at trough:      {PE_TROUGH}x  (wildfire-liability distress multiple)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct>=0 else 'below'} trough floor)")
print()
print(f"  Premium to EPP reflects the elevated regulated rate base growth and improving wildfire-liability backstop.")
print(f"  Bear ${bear_price} is below EPP ${EPP:.0f} — would require both EPS pressure AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+0.20:.2f} x {PE_TROUGH}x = ${(EPP_EPS+0.2)*PE_TROUGH:.0f} EPP — rate base growth compounds the floor higher.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: rate base growth moderate, CA data-center/EV load growth continues)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (rate base growth + CA data-center/EV load growth)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (slightly below current)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (~5% dividend growth)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — elevated rate base growth and a")
print(f"  growing California data-center/EV load pipeline support total returns even if the dividend stays minimal.")

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
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; wildfire-liability headline risk drives outsized swings)")
print(f"  Beta vs S&P 500:      0.85  (above average for a regulated utility, reflecting liability tail risk)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (PCG fell ~30% on wildfire-liability headlines historically; tail risk, not base case)")
print(f"  -> Wildfire mitigation progress and CA data-center/EV load growth are the PRIMARY catalysts;")
print(f"     de-risked wildfire profile + accelerating load growth = upside; new wildfire event = downside.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — upper-middle of range; reflects improving wildfire-risk sentiment.")
print(f"  -> BUY $16-$18  |  TRIM $24+  |  AVOID above $28")

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
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees wildfire de-risking + CA load growth, tempered by liability/dilution SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing the wildfire de-risking + CA load growth story.' if ADJ_GAP>0 else 'model roughly agrees with market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) Wildfire mitigation -> undergrounding program stays on/ahead of pace")
print(f"  (2) California data-center/EV load growth -> announced pipeline converts to in-service load")
print(f"  (3) Cost recovery -> wildfire fund and securitization mechanisms remain adequate")
print(f"  (4) Balance sheet -> equity issuance continues to moderate, opening the door to dividend growth")
print(f"  BUY $16-{round(CURRENT_PRICE*0.90,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $24  |  AVOID above $28")
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
