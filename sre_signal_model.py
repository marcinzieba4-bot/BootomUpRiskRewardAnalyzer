"""
SRE  ·  Sempra  ·  NYSE: SRE
Bottom-up signal model  ·  Regulated Utility (SDG&E/SoCalGas/Oncor) + LNG Export Growth Platform (Sempra Infrastructure)
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "SRE"
COMPANY       = "Sempra"
SECTOR        = "Regulated Utility (CA/TX) + LNG Export Growth Platform · NYSE: SRE"
CURRENT_PRICE = 78.00      # USD; as of 2026-06-11
VOL_52W_LOW   = 65.00
VOL_52W_HIGH  = 95.00
SHARES_OUT_M  = 660.0      # millions

# Dividend
ANNUAL_DIV    = 2.52       # $/share; ~7%/yr dividend growth

# ── LNG / RATE BASE GROWTH ANALYSIS (company-specific) ────────────────────────
LNG_PROJECT_GROWTH   = 0.10   # ~10%/yr growth in Sempra Infrastructure (LNG export) project pipeline/FIDs
SDGE_RATE_BASE_GROWTH = 0.07   # ~7%/yr SDG&E/SoCalGas regulated rate base growth
ONCOR_RATE_BASE_GROWTH = 0.09  # ~9%/yr Oncor (Texas) rate base growth
INCREMENTAL_MARGIN   = 0.42    # incremental margin on rate base / contracted LNG volumes
TAX_RATE             = 0.21

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 4.60    # FY2026E adj EPS
PE_TROUGH = 14      # min P/E at crisis trough (rate-shock/utility distress multiple)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $64

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (4.00, 14,   56, "Long-term rates rise further, compressing utility multiples; LNG project FIDs delayed; California wildfire liability concerns resurface; EPS $4.00 -> 14x distress P/E"),
    "BASE":  (4.60, 17,   78, "SDG&E/SoCalGas + Oncor rate base growth ~7-9%/yr; Sempra Infrastructure LNG projects (Port Arthur, ECA) progress on schedule; EPS $4.60 -> 17x P/E"),
    "BULL":  (5.20, 19,   99, "Additional LNG trains reach FID; long-term contract coverage expands; Oncor Texas data-center load growth accelerates; EPS $5.20 -> 19x premium P/E"),
    "XBULL": (6.00, 21,  126, "Multi-train LNG export buildout plus Oncor/Texas growth re-rate Sempra as a structural growth utility; EPS $6.00 -> 21x peak P/E"),
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
        "name":       "Sempra Infrastructure (LNG export) project pipeline growth",
        "weight":     0.25,
        "thresholds": ("<0%",   "≥5%",   "≥10%",  "≥15%"),
        "now":        "~10%",
        "score":      3,
        "comment":    "~10%; Port Arthur LNG and ECA projects progressing toward in-service, with additional trains under development",
    },
    {
        "name":       "SDG&E / SoCalGas regulated rate base growth",
        "weight":     0.20,
        "thresholds": ("<4%",   "≥5%",   "≥7%",   "≥9%"),
        "now":        "~7%",
        "score":      3,
        "comment":    "~7%/yr; California regulatory framework supports grid hardening and wildfire mitigation capex",
    },
    {
        "name":       "Oncor (Texas) rate base growth",
        "weight":     0.15,
        "thresholds": ("<5%",   "≥7%",   "≥9%",   "≥12%"),
        "now":        "~9%",
        "score":      3,
        "comment":    "~9%; Texas data-center and population growth drive one of the fastest-growing transmission rate bases in the US",
    },
    {
        "name":       "Adjusted EPS growth rate",
        "weight":     0.15,
        "thresholds": ("<5%",   "≥7%",   "≥8%",   "≥10%"),
        "now":        "~8%",
        "score":      3,
        "comment":    "~8%; tracking within management's long-term EPS growth guidance range",
    },
    {
        "name":       "LNG long-term contract coverage",
        "weight":     0.15,
        "thresholds": ("<60%",  "≥70%",  "≥80%",  "≥90%"),
        "now":        "~85%",
        "score":      3,
        "comment":    "~85% of planned LNG capacity covered by long-term offtake agreements with creditworthy counterparties",
    },
    {
        "name":       "Dividend growth rate",
        "weight":     0.10,
        "thresholds": ("<3%",   "≥5%",   "≥7%",   "≥9%"),
        "now":        "~7%",
        "score":      3,
        "comment":    "~7%/yr; consistent dividend growth supported by diversified regulated and contracted cash flows",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Sempra Infrastructure LNG export platform (Port Arthur, ECA) provides a structural growth runway beyond regulated rate base", +0.5, 0.25),
    ("+", "Oncor (Texas) is one of the fastest-growing transmission utilities in the US, benefiting from data-center and population growth", +0.4, 0.20),
    ("+", "Long-term LNG offtake contracts with creditworthy counterparties de-risk the growth platform's cash flows",                       +0.3, 0.15),
    ("-", "California wildfire liability and regulatory risk at SDG&E/SoCalGas remain a tail risk despite mitigation efforts",               -0.4, 0.20),
    ("-", "LNG project execution/financing risk and commodity price exposure could delay FIDs or compress economics",                        -0.4, 0.20),
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
CONS_EPS_2YR = 5.30    # conservative FY2028E: rate base growth + LNG project ramp continue
CONS_PE_2YR  = 16       # floor multiple (slightly below current)
cons_equity  = CONS_EPS_2YR * CONS_PE_2YR
cons_divs    = ANNUAL_DIV * 2 * 1.07   # approximate dividend growth across the 2yr window
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Regulated Utility (CA/TX) + LNG Export Growth Platform")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① LNG / RATE BASE GROWTH ANALYSIS ───────────────────────────────────────
print()
print("  LNG EXPORT + RATE BASE GROWTH ANALYSIS  (the core SRE earnings drivers)")
hr()
shares_b = SHARES_OUT_M / 1000
total_revenue_b = 17.0
print(f"  Estimated FY2026E revenue base: ~${total_revenue_b:.1f}B")
print()
print(f"  GROWTH UPSIDE  (incremental EPS from rate base + LNG project growth at {INCREMENTAL_MARGIN*100:.0f}% incremental margin):")
print(f"  {'Combined growth rate':<20}  {'Rev/yr ($B)':>12}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.00, 0.06, 0.08, 0.11]:
    rev_inc = total_revenue_b * g
    inc_eps = rev_inc * INCREMENTAL_MARGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% combined growth        +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
print(f"  SEGMENT GROWTH RATES:  SDG&E/SoCalGas ~{SDGE_RATE_BASE_GROWTH*100:.0f}%/yr  ·  Oncor (TX) ~{ONCOR_RATE_BASE_GROWTH*100:.0f}%/yr  ·")
print(f"  Sempra Infrastructure (LNG) project pipeline ~{LNG_PROJECT_GROWTH*100:.0f}%/yr — three distinct growth engines")
print(f"  diversify SRE's earnings base across regulated and contracted cash flows.")
print()
print(f"  BEAR (${bear_price}) requires: long-term rates rise further, compressing utility multiples,")
print(f"  AND LNG project FIDs are delayed AND California wildfire liability concerns resurface — together.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (LNG pipeline + SDG&E/SoCalGas + Oncor + EPS growth + LNG contracts + dividend)")
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
    ("Sempra Infrastructure (LNG) pipeline growth",  "~10%",   "<0%",   "-10pp",  "LNG project FIDs delayed amid financing or permitting setbacks"),
    ("SDG&E/SoCalGas rate base growth",              "~7%",    "<4%",   "-3pp",   "California regulatory disallowances or wildfire-related cost pressure"),
    ("Oncor (Texas) rate base growth",               "~9%",    "<5%",   "-4pp",   "Texas data-center buildout slows; transmission capex plan trimmed"),
    ("Adjusted EPS growth",                          "~8%",    "<5%",   "-3pp",   "Higher financing costs and dilution offset rate base/LNG growth"),
    ("LNG long-term contract coverage",              "~85%",   "<60%",  "-25pp",  "Counterparty defaults or contract renegotiations reduce coverage"),
    ("Dividend growth rate",                         "~7%",    "<3%",   "-4pp",   "Balance sheet pressure from LNG capex slows dividend growth"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Long-term rates rise further, compressing utility multiples, while LNG project")
print(f"  FIDs are delayed and California wildfire liability concerns resurface at SDG&E/SoCalGas.")
print(f"  EPS falls to ~$4.00; multiple compresses to 14x distress P/E = ${bear_price}.")

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
print(f"  Premium to EPP reflects the diversified regulated base plus the LNG export growth optionality.")
print(f"  Bear ${bear_price} is below EPP ${EPP:.0f} — would require both EPS pressure AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+0.40:.2f} x {PE_TROUGH}x = ${(EPP_EPS+0.4)*PE_TROUGH:.0f} EPP — rate base + LNG ramp compounds the floor higher.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: rate base growth continues, LNG projects ramp toward in-service)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (SDG&E/Oncor rate base growth + early LNG ramp)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (slightly below current)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (~7%/yr dividend growth)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — the ~3.2% dividend yield plus steady")
print(f"  regulated rate base growth across three jurisdictions support total returns even in a soft macro.")

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
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (above-average for a utility; LNG project/commodity sensitivity)")
print(f"  Beta vs S&P 500:      0.60  (below market but more volatile than pure-play regulated utilities)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (SRE fell ~25% during the 2023 rate-shock and CA wildfire-fear selloffs; tail risk, not base case)")
print(f"  -> LNG project FID/financing progress and CA wildfire policy are the PRIMARY catalysts;")
print(f"     LNG progress + stable CA regulation = upside; LNG delays or wildfire liability shock = downside.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — mid range; not stretched relative to growth profile.")
print(f"  -> BUY $68-$72  |  TRIM $90+  |  AVOID above $98")

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
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees LNG export + multi-jurisdiction rate base growth, tempered by CA/LNG-execution SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing the LNG export growth story.' if ADJ_GAP>0 else 'model roughly agrees with market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) Sempra Infrastructure LNG pipeline -> additional FIDs confirm export growth platform")
print(f"  (2) Oncor (Texas) rate base -> sustained >=9%/yr growth on data-center demand")
print(f"  (3) SDG&E/SoCalGas -> constructive rate case outcomes with no major wildfire liability shocks")
print(f"  (4) LNG contract coverage -> sustained >=85% confirms cash flow visibility")
print(f"  BUY $68-{round(CURRENT_PRICE*0.90,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $90  |  AVOID above $98")
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
