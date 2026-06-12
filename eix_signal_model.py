"""
EIX  ·  Edison International  ·  NYSE: EIX
Bottom-up signal model  ·  Regulated Electric Utility (SCE) · Southern California Wildfire Mitigation · AI/Data-Center & EV Load Growth
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "EIX"
COMPANY       = "Edison International"
SECTOR        = "Regulated Electric Utility (SCE) · Southern California · NYSE: EIX"
CURRENT_PRICE = 58.00     # USD; as of 2026-06-11
VOL_52W_LOW   = 46.00
VOL_52W_HIGH  = 64.00
SHARES_OUT_M  = 400.0      # millions

# Dividend
ANNUAL_DIV    = 3.06       # $/share; ~5.3% yield, modest growth amid wildfire-litigation overhang

# ── RATE BASE / LOAD GROWTH ANALYSIS (company-specific) ───────────────────────
RATE_BASE_GROWTH   = 0.09    # ~9%/yr regulated rate base growth (grid resilience + wildfire mitigation capex)
DATA_CENTER_GROWTH = 0.05    # ~5% incremental load growth from LA basin data-center / EV adoption pipeline
INCREMENTAL_MARGIN = 0.40    # incremental operating margin on new rate base / load growth
TAX_RATE           = 0.21

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 3.50    # FY2026E adj EPS
PE_TROUGH = 12      # min P/E at crisis trough (wildfire-liability distress multiple)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $42

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (3.00, 11,   33,  "A new major SoCal wildfire event reopens liability fears and triggers fresh equity issuance; EPS $3.00 -> 11x distress P/E"),
    "BASE":  (3.50, 17,   60, "Regulated rate base +9%/yr on wildfire mitigation/undergrounding capex; LA basin data-center/EV load growth continues; EPS $3.50 -> 17x P/E"),
    "BULL":  (4.00, 20,   80, "Undergrounding program de-risks the wildfire profile ahead of plan; LA basin data-center/EV load growth accelerates; EPS $4.00 -> 20x premium P/E"),
    "XBULL": (4.50, 23,   104, "Wildfire risk re-rating completes and a multi-year LA basin data-center buildout drives sustained above-plan rate base growth; EPS $4.50 -> 23x peak P/E"),
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
        "name":       "Wildfire mitigation / undergrounding progress (SCE service territory)",
        "weight":     0.25,
        "thresholds": ("<200mi/yr", "≥300mi/yr", "≥400mi/yr", "≥600mi/yr"),
        "now":        "~400mi/yr",
        "score":      3,
        "comment":    "~400 miles/yr of undergrounding across high-fire-risk areas; on pace with the multi-year wildfire mitigation plan",
    },
    {
        "name":       "LA basin data-center / EV load growth",
        "weight":     0.20,
        "thresholds": ("<1%",   "≥2%",   "≥5%",   "≥8%"),
        "now":        "~5%",
        "score":      3,
        "comment":    "~5%; growing data-center interconnection requests and EV adoption across the Los Angeles basin",
    },
    {
        "name":       "Adjusted EPS growth rate",
        "weight":     0.15,
        "thresholds": ("<4%",   "≥6%",   "≥8%",   "≥10%"),
        "now":        "~8%",
        "score":      3,
        "comment":    "~8%; tracking within management's 7-9% long-term EPS growth guidance range, driven by elevated rate base growth",
    },
    {
        "name":       "Regulatory cost recovery / wildfire fund & securitization",
        "weight":     0.15,
        "thresholds": ("Underfunded", "Adequate", "Strong", "Fully de-risked"),
        "now":        "Adequate",
        "score":      2,
        "comment":    "CA wildfire fund and securitization mechanisms provide a meaningful liability backstop, though the 2025 Eaton fire keeps the issue live",
    },
    {
        "name":       "Balance sheet / equity issuance trajectory",
        "weight":     0.10,
        "thresholds": ("Heavy dilution", "Elevated", "Moderating", "Self-funding"),
        "now":        "Elevated",
        "score":      2,
        "comment":    "Equity issuance to fund wildfire mitigation capex and potential liability exposure remains elevated",
    },
    {
        "name":       "Dividend growth rate",
        "weight":     0.15,
        "thresholds": ("Cut risk", "Frozen", "Modest growth", "Meaningful growth"),
        "now":        "Modest growth",
        "score":      2,
        "comment":    "~1-3%/yr growth maintained even amid the wildfire-litigation overhang, supported by the ~5.3% yield",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "SCE serves the Los Angeles basin, one of the largest data-center and EV-adoption markets in the country", +0.4, 0.20),
    ("+", "CA wildfire fund and cost-recovery securitization materially reduce tail liability risk versus the pre-2019 era", +0.4, 0.20),
    ("+", "Elevated grid-resilience and undergrounding capex drives above-average regulated rate base growth",         +0.3, 0.15),
    ("-", "Wildfire ignition / litigation tail risk (including the 2025 Eaton fire) remains the single largest overhang on the equity", -0.5, 0.25),
    ("-", "Ongoing equity issuance to fund the wildfire mitigation program and potential liability exposure continues to dilute per-share growth", -0.3, 0.20),
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
CONS_EPS_2YR = 4.10    # conservative FY2028E: rate base growth + LA basin data-center/EV load growth continue
CONS_PE_2YR  = 16       # floor multiple (slightly below current)
cons_equity  = CONS_EPS_2YR * CONS_PE_2YR
cons_divs    = ANNUAL_DIV * 2 * 1.02   # approximate dividend growth across the 2yr window
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Regulated Southern California Electric Utility")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① RATE BASE / LOAD GROWTH ANALYSIS ──────────────────────────────────────
print()
print("  RATE BASE + DATA-CENTER LOAD GROWTH ANALYSIS  (the core EIX earnings drivers)")
hr()
shares_b = SHARES_OUT_M / 1000
total_revenue_b = 17.0
print(f"  Estimated FY2026E revenue base: ~${total_revenue_b:.1f}B")
print()
print(f"  GROWTH UPSIDE  (incremental EPS from rate base + load growth at {INCREMENTAL_MARGIN*100:.0f}% incremental margin):")
print(f"  {'Combined growth rate':<20}  {'Rev/yr ($B)':>12}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.00, 0.05, 0.09, 0.13]:
    rev_inc = total_revenue_b * g
    inc_eps = rev_inc * INCREMENTAL_MARGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% combined growth        +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
print(f"  LA BASIN DATA-CENTER / EV LOAD GROWTH  (~{DATA_CENTER_GROWTH*100:.0f}% incremental load growth from announced")
print(f"  Los Angeles basin data-center pipeline and EV adoption; converts directly into rate base additions).")
print()
print(f"  BEAR (${bear_price}) requires: a new major SoCal wildfire event reopens liability fears")
print(f"  AND forces fresh equity issuance, compressing the multiple — together.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (undergrounding + LA basin load growth + EPS growth + cost recovery + balance sheet + dividend)")
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
    ("Wildfire mitigation / undergrounding pace",  "~400mi/yr","<200mi/yr","-200mi","Permitting delays or cost overruns slow the undergrounding program"),
    ("LA basin data-center / EV load growth",      "~5%",    "<1%",   "-4pp",   "Hyperscaler/EV pipeline slows on grid-interconnection constraints"),
    ("Adjusted EPS growth",                        "~8%",    "<4%",   "-4pp",   "Equity issuance and financing costs offset rate base growth"),
    ("Wildfire fund / cost recovery adequacy",     "Adequate","Underfunded","-","A new major wildfire event overwhelms the wildfire fund"),
    ("Balance sheet / equity issuance",            "Elevated","Heavy dilution","-","A new liability event forces a large fresh equity raise"),
    ("Dividend growth",                            "Modest growth","Frozen","-","Liability pressure freezes dividend growth"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A new major Southern California wildfire event linked to SCE equipment reopens liability")
print(f"  fears, overwhelms the wildfire fund, and forces a large fresh equity raise that dilutes per-share earnings.")
print(f"  EPS falls to ~$3.00; multiple compresses to 11x distress P/E = ${bear_price}.")

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
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+0.30:.2f} x {PE_TROUGH}x = ${(EPP_EPS+0.3)*PE_TROUGH:.0f} EPP — rate base growth compounds the floor higher.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: rate base growth moderate, LA basin data-center/EV load growth continues)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (rate base growth + LA basin data-center/EV load growth)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (slightly below current)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (~2%/yr dividend growth)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — the ~5.3% dividend yield plus elevated")
print(f"  rate base growth and the LA basin data-center/EV load pipeline support total returns even in a soft macro.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.24
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; wildfire-liability headline risk drives outsized swings)")
print(f"  Beta vs S&P 500:      0.90  (above average for a regulated utility, reflecting liability tail risk)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (EIX fell ~35% on Eaton fire wildfire-liability headlines in early 2025; tail risk, not base case)")
print(f"  -> Wildfire mitigation progress and LA basin data-center/EV load growth are the PRIMARY catalysts;")
print(f"     de-risked wildfire profile + accelerating load growth = upside; new wildfire event = downside.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — mid range; reflects ongoing wildfire-risk sentiment volatility.")
print(f"  -> BUY $44-$48  |  TRIM $62+  |  AVOID above $68")

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
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees wildfire de-risking + LA basin load growth, tempered by liability/dilution SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing the wildfire de-risking + LA basin load growth story.' if ADJ_GAP>0 else 'model roughly agrees with market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) Wildfire mitigation -> undergrounding program stays on/ahead of pace")
print(f"  (2) LA basin data-center/EV load growth -> announced pipeline converts to in-service load")
print(f"  (3) Cost recovery -> wildfire fund and securitization mechanisms remain adequate")
print(f"  (4) Balance sheet -> equity issuance moderates, supporting continued dividend growth")
print(f"  BUY $44-{round(CURRENT_PRICE*0.90,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $62  |  AVOID above $68")
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
