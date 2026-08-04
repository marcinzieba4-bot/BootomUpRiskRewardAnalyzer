"""
LPP  ·  LPP S.A.  ·  WSE: LPP
Bottom-up signal model  ·  Apparel Retail / Sinsay Discount Brand / Reserved-Cropp-House-Mohito
Currency: PLN (Polish złoty) — this model is denominated natively in PLN, not USD
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "LPP"
COMPANY       = "LPP S.A."
SECTOR        = "Apparel Retail · Sinsay Discount Brand · Reserved/Cropp/House/Mohito · GPW: LPP (PLN)"
CURRENT_PRICE = 21_780.0    # PLN; close 2026-08-04. Very few shares outstanding (~1.86M), hence the high nominal price
VOL_52W_LOW   = 15_405.0    # PLN
VOL_52W_HIGH  = 24_480.0    # PLN
SHARES_OUT_M  = 1.86        # millions
ANNUAL_DIV    = 220.0       # PLN/share; modest payout, ~1.0% yield — most cash reinvested in Sinsay store growth

# ── REVENUE BRIDGE (FY2026E, PLN billions) ────────────────────────────────────
# Q1 FY2026 (Feb-Apr) actual: revenue 5.5B zł (+10.5% YoY), net profit 475M zł (+42% YoY), EBITDA
# +36% YoY to 1.3B zł, record gross margin of 58.2%. Sinsay — the discount-focused growth brand — is
# targeted for ~750 new stores in FY2026 alone, with an average 17-month payback and 98% of stores
# already EBITDA-positive. The one soft spot: like-for-like (LFL) sales fell 2.8%, which management
# attributed to unseasonably cold spring/summer weather rather than a demand problem.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Sinsay (discount growth brand)",              10.35, 8.0, 13.5, "The primary growth engine — ~750 new stores planned FY2026, 17-month payback, 98% EBITDA-positive"),
    ("Core brands (Reserved/Cropp/House/Mohito)",   12.65, 10.5, 14.0, "The mature base; -2.8% LFL in Q1, attributed to unseasonably cold weather rather than demand weakness"),
]

# Net-margin-based bridge (apparel retail: gross-margin-driven economics with real seasonal swings)
NET_MARGIN_CURR = 0.1097  # FY2026E; reconciles to the forward-P/E-implied EPS
NET_MARGIN_BEAR = 0.0750  # BEAR: LFL weakness persists and promotional activity compresses margin to clear inventory
NET_MARGIN_BULL = 0.1250  # BULL: Sinsay's high-margin scale economics continue compounding as the network expands

# ── SINSAY EXPANSION CALCULATOR (the LPP-specific angle) ─────────────────────
Q1_REVENUE_GROWTH_PCT      = 10.5   # % YoY, Q1 FY2026 revenue growth
Q1_NET_PROFIT_GROWTH_PCT   = 42.0   # % YoY, Q1 FY2026 net profit growth
Q1_EBITDA_GROWTH_PCT       = 36.0   # % YoY, Q1 FY2026 EBITDA growth
RECORD_GROSS_MARGIN_PCT    = 58.2   # % Q1 FY2026 gross margin, a record
SINSAY_NEW_STORES_FY26     = 750    # planned new Sinsay stores for the full FY2026
SINSAY_PAYBACK_MONTHS      = 17     # average payback period for a new Sinsay store
SINSAY_EBITDA_POSITIVE_PCT = 98     # % of Sinsay stores already EBITDA-positive
Q1_LFL_DECLINE_PCT         = -2.8   # % YoY, Q1 FY2026 like-for-like sales (weather-attributed)

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 1_356.0     # PLN/share FY2026E; forward-P/E-implied from consensus
PE_PESSIMISTIC = 12.0        # trough P/E: a genuine apparel-retail-trough multiple
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 746.0, 12,   8_952, "LFL weakness proves structural rather than weather-driven, and heavy promotional activity compresses margin"),
    "BASE":  (1_453.0, 16.06, 23_340, "Sinsay store growth continues roughly as planned while core-brand LFL stabilizes near flat"),
    "BULL":  (1_867.0, 18,  33_606, "The Sinsay expansion thesis fully plays out — margin keeps expanding as the discount format scales further"),
    "XBULL": (2_394.0, 20,  47_880, "Sinsay becomes a genuine European discount-apparel leader, re-rating LPP well above its prior highs"),
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
        "name":       "Total revenue YoY growth",
        "weight":     0.15,
        "thresholds": ("<5%",    "≥8%",    "≥11%",   "≥14%"),
        "now":        "+10.5%",
        "score":      2,
        "comment":    "Solid but not spectacular — the LFL weakness is a real drag on an otherwise strong store-growth story",
    },
    {
        "name":       "Net profit YoY growth",
        "weight":     0.20,
        "thresholds": ("<10%",   "≥20%",   "≥30%",   "≥40%"),
        "now":        "+42%",
        "score":      4,
        "comment":    "A genuinely exceptional profit-growth quarter, well ahead of revenue growth — real margin expansion, not just volume",
    },
    {
        "name":       "Gross margin",
        "weight":     0.15,
        "thresholds": ("<52%",   "≥55%",   "≥57%",   "≥59%"),
        "now":        "58.2%",
        "score":      3,
        "comment":    "A record level — genuine evidence of pricing power and a favorable mix shift toward higher-margin Sinsay",
    },
    {
        "name":       "Sinsay new store economics",
        "weight":     0.20,
        "thresholds": ("unprofitable","≥80% EBITDA+","≥90% EBITDA+","≥97% EBITDA+"),
        "now":        "98% EBITDA+",
        "score":      4,
        "comment":    "98% of Sinsay stores already EBITDA-positive with a 17-month payback — a genuinely proven, scalable store economic model",
    },
    {
        "name":       "Like-for-like (LFL) sales growth",
        "weight":     0.15,
        "thresholds": ("<-6%",   "≥-4%",   "≥-1%",   "≥2%"),
        "now":        "-2.8%",
        "score":      2,
        "comment":    "Management attributes this to unseasonably cold weather — plausible, but not yet proven out by a subsequent quarter",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.15,
        "thresholds": (">22x",   "≤19x",   "≤16x",   "≤13x"),
        "now":        "~16.1x",
        "score":      3,
        "comment":    "16.1× FY2026E EPS — reasonable for a business compounding profit at +42% YoY",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Sinsay's store economics (98% EBITDA-positive, 17-month payback) are proven at scale, not a hopeful projection — 750 more stores planned this year alone", +0.5, 0.25),
    ("-", "The -2.8% LFL decline needs the weather explanation to hold; a second consecutive weak LFL quarter would be a genuine red flag", -0.3, 0.15),
    ("+", "Record 58.2% gross margin and +42% profit growth show real operating leverage, not just top-line expansion", +0.4, 0.15),
    ("-", "European apparel retail is exposed to genuine macro/weather/fashion-cycle risk that no single company fully controls", -0.3, 0.15),
    ("+", "LPP has a long public-market track record of successfully scaling multiple brands (Reserved historically, now Sinsay) through complete store-format cycles", +0.3, 0.15),
    ("-", "At a market cap approaching PLN 40B+, Sinsay's continued expansion needs to keep finding productive new markets/formats, not just Poland/CEE saturation", -0.2, 0.15),
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
CONS_EPS_2YR  = 1_550.0  # PLN; conservative FY2028E: modest growth off FY2026E, LFL stays soft
CONS_PE_2YR   = 15       # a modest de-rating from ~16.1×
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
print(f"  {TICKER}  ·  {COMPANY}  ·  {CURRENT_PRICE:,.0f} zł  ·  Sinsay / Reserved / Cropp / House / Mohito")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]  (all figures in PLN)")
print("═" * (W + 4))

# ─── ① REVENUE BRIDGE ─────────────────────────────────────────────────────────
print()
print("  REVENUE BRIDGE  (FY2026E, PLN billions  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<44}  {'FY26E (B zł)':>13}  {'Bear (B zł)':>11}  {'Bull (B zł)':>11}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<44}  {curr:>11.2f}  {bear:>9.1f}  {bull:>9.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<44}  {curr_total:>11.2f}  {bear_total:>9.1f}  {bull_total:>9.1f}")
print(f"  Q1 FY2026 actual: 5.5B zł revenue (+10.5% YoY), 475M zł net profit (+42% YoY)")
print()

# EPS bridge (net-margin based)
shares    = SHARES_OUT_M / 1000
curr_net  = curr_total * NET_MARGIN_CURR
curr_eps  = round(curr_net / shares, 0)

bull_net  = bull_total * NET_MARGIN_BULL
shares_b  = shares * 0.99
bull_eps_imp = round(bull_net / shares_b, 0)

bear_net  = bear_total * NET_MARGIN_BEAR
bear_eps_imp = round(bear_net / shares, 0)

print(f"  FY2026E EPS check:  {curr_total:.2f}B zł rev × {NET_MARGIN_CURR*100:.2f}% net margin")
print(f"  ÷ {shares:.6f}B shares  =  {curr_eps:,.0f} zł/share  (model estimate {EPS_FY2026E:,.0f} zł  ✓)")
print()
print(f"  BULL EPS check:  {bull_total:.2f}B zł rev × {NET_MARGIN_BULL*100:.2f}% net margin, post-buyback")
print(f"  =  ~{bull_eps_imp:,.0f} zł/share  →  × {SCENARIOS['BULL'][1]}× = ~{bull_eps_imp*SCENARIOS['BULL'][1]:,.0f} zł  ✓ BULL {SCENARIOS['BULL'][2]:,.0f} zł")
print()
print(f"  BEAR EPS check:  {bear_total:.2f}B zł rev × {NET_MARGIN_BEAR*100:.2f}% net margin (LFL weakness + promotional activity)")
print(f"  =  ~{bear_eps_imp:,.0f} zł/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~{bear_eps_imp*SCENARIOS['BEAR'][1]:,.0f} zł  ✓ BEAR {SCENARIOS['BEAR'][2]:,.0f} zł")

# SINSAY EXPANSION CHECK
print()
print(f"  SINSAY EXPANSION CHECK  (the LPP-specific angle):")
print(f"  Q1 revenue / net profit growth:          +{Q1_REVENUE_GROWTH_PCT:.1f}% / +{Q1_NET_PROFIT_GROWTH_PCT:.1f}% YoY")
print(f"  Record gross margin:                      {RECORD_GROSS_MARGIN_PCT:.1f}%")
print(f"  Sinsay new stores planned (FY2026):        {SINSAY_NEW_STORES_FY26}")
print(f"  Sinsay store payback / EBITDA-positive:    {SINSAY_PAYBACK_MONTHS} months  /  {SINSAY_EBITDA_POSITIVE_PCT}%")
print(f"  Q1 LFL sales:                              {Q1_LFL_DECLINE_PCT:.1f}%  (attributed to cold weather)")
print()
print(f"  Sinsay is the clearest, most quantified growth story in this batch — a discount format with proven")
print(f"  98%-EBITDA-positive unit economics and a sub-1.5-year payback, still early enough in its rollout")
print(f"  (750 more stores planned this year alone) to compound for years. The offsetting question is whether")
print(f"  the -2.8% LFL decline is genuinely weather noise or the first sign of demand softness in the core brands.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = 1.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every 1B zł revenue (at 10.97% margin):  +{eps_per_1B_rev:,.0f} zł/EPS  = +{eps_per_1B_rev*16:,.0f} zł/share at 16× P/E")
print(f"  Every 1pp of net margin:                   +{curr_total*0.01/shares:,.0f} zł/EPS  = +{curr_total*0.01/shares*16:,.0f} zł/share at 16× P/E")
print(f"  Every 1 turn of P/E:                       ±{EPS_FY2026E:,.0f} zł/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (revenue / profit growth / gross margin / Sinsay economics / LFL / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<32}  {'BEAR':>15}  {'BASE':>13}  {'BULL':>13}  {'XBULL':>13}  {'NOW':>13}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<32}  {ths[0]:>15}  {ths[1]:>13}  {ths[2]:>13}  {ths[3]:>13}  {s['now']:>13}  {lbl}  {b}")
    print(f"    {s['comment']}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from {CURRENT_PRICE:,.0f} zł + 15%/yr hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:88]:<88}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR {bear_price:,.0f} zł)")
hr()
print(f"  {'Signal':<32}  {'Current':>11}  {'Bear val':>11}  Trigger")
hr()
bear_triggers = [
    ("Revenue growth",              "+10.5%",  "<5%",     "Sinsay store productivity declines as the network matures and saturates key CEE markets"),
    ("Net profit growth",           "+42%",    "<10%",    "Gross margin gains reverse as promotional activity increases to defend market share"),
    ("Gross margin",                "58.2%",   "<52%",    "Input cost inflation or FX headwinds erode the pricing power behind the record margin"),
    ("Sinsay EBITDA-positive rate", "98%",     "<80%",    "New-format store productivity disappoints as expansion moves into less favorable locations"),
    ("LFL sales",                   "-2.8%",   "<-6%",    "The weather explanation proves wrong and demand weakness is confirmed as structural"),
    ("Forward P/E",                 "~16.1x",  ">22x",    "Market fully re-prices LPP for a slower, LFL-challenged growth trajectory"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>11}  {bear_v:>11}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the bear case hinges almost entirely on whether the -2.8% LFL decline was genuinely")
print(f"  weather-driven (as management claims) or the first sign of demand softness — Sinsay's unit economics")
print(f"  are proven enough that the bear case needs the CORE brands to weaken, not just Sinsay to slow down.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS estimate:       {EPS_FY2026E:,.0f} zł  (forward-P/E-implied from consensus)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (a genuine apparel-retail-trough multiple)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    {EPP:,.0f} zł/share")
print(f"  Current {CURRENT_PRICE:,.0f} zł vs EPP {EPP:,.0f} zł:  {epp_gap_pct:+.1f}%")
print()
print(f"  At {CURRENT_PRICE:,.0f} zł the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS — a reasonable, not demanding,")
print(f"  multiple for a business that just grew profit +42% YoY. The EPP floor provides real margin of safety")
print(f"  versus a genuine apparel-retail-downturn scenario.")
print(f"  At a 18× reversion (a modest premium to trough): {EPS_FY2026E:,.0f} × 18 = {EPS_FY2026E*18:,.0f} zł  ({(EPS_FY2026E*18/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest growth off FY2026E, LFL stays soft)")
hr()
print(f"  Conservative FY2028E EPS:  {CONS_EPS_2YR:,.0f} zł  (~14% cumulative EPS growth — below the current +42% trajectory)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~16.1× → 15×; a modest de-rating)")
print(f"  Conservative equity value:   {cons_equity:,.0f} zł/share")
print(f"  + Cumulative dividends (2yr): +{cons_divs:,.0f} zł/share  ({ANNUAL_DIV:.0f} zł/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      {cons_total:,.0f} zł  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):,.0f} from {CURRENT_PRICE:,.0f} zł)")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: even a conservative case with growth well below the current +42% pace and a modest")
print(f"  de-rating still clears a {'positive' if cons_return > 0 else 'negative'} return, because Sinsay's proven unit economics provide a real floor under")
print(f"  the growth story even if the core brands stay soft.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.28
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        {VOL_52W_LOW:,.0f} – {VOL_52W_HIGH:,.0f} zł  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      {ANNUAL_DIV:.0f} zł/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; modest — most cash reinvested in growth)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (moderate — typical for a large-cap apparel retailer with a genuine growth story)")
print(f"  Beta vs WIG20:        1.05  (roughly in line with the Warsaw benchmark)")
print(f"  1-sigma range (1yr):  {sigma_range[0]:,.0f} – {sigma_range[1]:,.0f} zł  ({CURRENT_PRICE:,.0f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear {bear_price:,.0f} zł requires:  ~{bear_sigmas:.1f}σ drawdown  (large, consistent with a genuine LFL-driven downturn scenario)")
print(f"  → Q2 FY2026 print (likely September) is the next test of whether LFL recovers as the weather normalizes.")
print(f"  → Sinsay store-opening pace and monthly LFL trends are the leading indicators between prints.")
print(f"  → {signal_short} at {CURRENT_PRICE:,.0f} zł  |  Add below 17,500 zł  |  Trim above 27,000 zł")

# ─── ⑦ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print()
print("  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
hr()
probs_mkt = softmax_probs(MARKET_COMPOSITE)
print(f"  {'Scenario':<10}  {'Price':>10}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>7}  Description")
hr()
for s in ["BEAR","BASE","BULL","XBULL"]:
    pp  = probs_proxy[s] * 100
    pm  = probs_mkt[s]   * 100
    gap = pp - pm
    pr  = SCENARIOS[s][2]
    desc = SCENARIOS[s][3][:40]
    print(f"  {s:<10}  {pr:>8,.0f} zł  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): {ev_adj:,.0f} zł  /  Proxy EV: {ev_prx:,.0f} zł  /  Market EV: {ev_mkt:,.0f} zł  /  Current: {CURRENT_PRICE:,.0f} zł")
hr()
print(f"  Downside  (→ Bear {bear_price:,.0f} zł):  {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull {bull_price:,.0f} zł):  {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b_str}")
print(f"  Signal    :  {signal_full}")
print()
print(f"  MARKET PRICING: at {CURRENT_PRICE:,.0f} zł the market composite is {MARKET_COMPOSITE:.2f}/4.0. The model's")
print(f"  adjusted composite is {ADJ_COMPOSITE:.2f}/4.0, for a gap of {ADJ_GAP:+.2f} — {valuation_label.lower()}.")
print(f"  LPP's Sinsay-driven profit growth (+42% YoY) is genuinely exceptional, and the stock isn't pricing")
print(f"  in an unreasonable amount of continued success — the LFL softness is the one real crack to watch.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q2 FY2026 print (likely September) — does LFL recover as weather normalizes into summer?")
print(f"  (2) Sinsay store-opening pace toward the 750-store FY2026 target")
print(f"  (3) Gross margin durability at or near the record 58.2% level")
print(f"  (4) Any signs of promotional intensity picking up to defend market share in the core brands")
print(f"  (5) International Sinsay expansion beyond the CEE core market — the next leg of the growth story")
print(f"  {signal_short} at {CURRENT_PRICE:,.0f} zł  |  Add below 17,500 zł  |  Trim above 27,000 zł")
print(f"  EPP floor: {EPP:,.0f} zł  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: {EPS_FY2026E:,.0f} zł  |  Sinsay stores planned: {SINSAY_NEW_STORES_FY26}")
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
