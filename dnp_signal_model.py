"""
DNP  ·  Dino Polska S.A.  ·  WSE: DNP
Bottom-up signal model  ·  Grocery Retail / Standalone Discount Format / Founder-Led
Currency: PLN (Polish złoty) — this model is denominated natively in PLN, not USD
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "DNP"
COMPANY       = "Dino Polska S.A."
SECTOR        = "Grocery Retail · Standalone Discount Format · GPW: DNP (PLN)"
CURRENT_PRICE = 32.46       # PLN; close 2026-08-03, down ~36% from the 52-week high
VOL_52W_LOW   = 26.89       # PLN
VOL_52W_HIGH  = 50.68       # PLN
SHARES_OUT_M  = 980.4       # millions
ANNUAL_DIV    = 0.0         # PLN/share; no dividend — cash reinvested in store network expansion

# ── REVENUE BRIDGE (FY2026E, PLN billions) ────────────────────────────────────
# Q1 2026 actual: revenue 8,896M zł (+14.8% YoY), driven by 4.4% like-for-like (LFL) growth plus
# network expansion (62 new stores, 3,094 total, net sales area +13% YoY). Operating profit +1.2%
# to 419.2M zł, net profit +1.6% to 316.3M zł — profit growth lagging revenue growth because
# management is deliberately prioritizing volume over margin (net margin 6.7%, down from 7.2%) amid
# an escalating price war with Jerónimo Martins' Biedronka and Lidl. The stock has fallen sharply
# from its 52-week high on exactly this margin-compression dynamic.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Like-for-like sales (existing stores)", 27.0, 23.0, 31.0, "The core, mature store base; +4.4% LFL growth in Q1 despite intense discounter competition"),
    ("New store network expansion",            9.5,  7.5, 12.0, "62 new stores in Q1 alone; net sales area +13% YoY — the primary growth lever"),
]

# Net-margin-based bridge (grocery retail: thin, competitive margins)
NET_MARGIN_CURR = 0.0473  # FY2026E; reconciles to the forward-P/E-implied EPS
NET_MARGIN_BEAR = 0.0320  # BEAR: the volume-over-margin price war escalates further
NET_MARGIN_BULL = 0.0580  # BULL: competitive intensity eases, allowing some margin recovery

# ── PRICE WAR CALCULATOR (the Dino-specific angle) ────────────────────────────
Q1_2026_LFL_GROWTH_PCT     = 4.4   # % YoY, Q1 2026 like-for-like sales growth
Q1_2026_REVENUE_GROWTH_PCT = 14.8  # % YoY, Q1 2026 total revenue growth
NEW_STORES_Q1              = 62    # new stores opened in Q1 2026
TOTAL_STORES               = 3_094 # total store count after Q1 2026
NET_SALES_AREA_GROWTH_PCT  = 13.0  # % YoY, net sales area growth
NET_MARGIN_CURRENT_PCT     = 6.7   # % current net margin (down from 7.2% a year ago)
STOCK_DRAWDOWN_FROM_HIGH_PCT = 36  # % decline from the 52-week high
KEY_COMPETITORS             = "Biedronka (Jerónimo Martins), Lidl"  # the discounters driving the price war

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 1.76        # PLN/share FY2026E; forward-P/E-implied from consensus
PE_PESSIMISTIC = 14.0        # trough P/E: a genuine grocery-retail-trough multiple under intensified competition
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  (1.00, 14,  14, "The Biedronka/Lidl price war escalates further; the deliberate volume-over-margin strategy keeps compressing profitability"),
    "BASE":  (1.85, 18.4, 34, "LFL growth and new-store expansion continue roughly as guided while margins stay pressured near current levels"),
    "BULL":  (2.57, 20,  51, "Competitive intensity eases and margins begin recovering while store growth continues — a path back toward the 52-week high"),
    "XBULL": (3.32, 22,  73, "A genuine margin recovery combines with accelerating store growth, re-rating the stock well above its prior highs"),
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
        "name":       "Like-for-like (LFL) sales growth",
        "weight":     0.20,
        "thresholds": ("<0%",    "≥2%",    "≥4%",    "≥6%"),
        "now":        "+4.4%",
        "score":      3,
        "comment":    "Genuinely healthy LFL growth despite an escalating discounter price war",
    },
    {
        "name":       "Total revenue YoY growth",
        "weight":     0.15,
        "thresholds": ("<8%",    "≥11%",   "≥14%",   "≥17%"),
        "now":        "+14.8%",
        "score":      3,
        "comment":    "Store network expansion continues compounding revenue growth well above LFL alone",
    },
    {
        "name":       "Net sales area growth",
        "weight":     0.15,
        "thresholds": ("<6%",    "≥9%",    "≥12%",   "≥15%"),
        "now":        "+13.0%",
        "score":      3,
        "comment":    "The store rollout machine hasn't slowed — 62 new stores in a single quarter",
    },
    {
        "name":       "Net margin trend",
        "weight":     0.20,
        "thresholds": ("<4%",    "≥5%",    "≥6.5%",  "≥8%"),
        "now":        "6.7%",
        "score":      2,
        "comment":    "Down from 7.2% a year ago — the direct, quantified cost of the deliberate volume-over-margin strategy",
    },
    {
        "name":       "Profit growth vs revenue growth gap",
        "weight":     0.15,
        "thresholds": (">10pp gap","≥6pp gap","≥3pp gap","≤1pp gap"),
        "now":        "13.2pp gap",
        "score":      1,
        "comment":    "Net profit grew only +1.6% against +14.8% revenue growth — the clearest single number showing the margin story",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.15,
        "thresholds": (">24x",   "≤20x",   "≤17x",   "≤14x"),
        "now":        "~18.4x",
        "score":      2,
        "comment":    "18.4× FY2026E EPS — no longer expensive after the 36% drawdown, but not yet statistically cheap either",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "LFL growth (+4.4%) and store rollout (+13% net sales area) are both genuinely healthy, underlying-demand-driven numbers, not manufactured", +0.4, 0.20),
    ("-", "The Biedronka/Lidl price war is a real, structural, multi-year competitive dynamic, not a one-quarter event — margin recovery isn't guaranteed on any specific timeline", -0.5, 0.25),
    ("+", "Founder-led management has a long, credible track record of prioritizing long-term market share over short-term margin, which has historically paid off for Dino shareholders", +0.4, 0.15),
    ("-", "A 13.2pp gap between revenue growth (+14.8%) and profit growth (+1.6%) is a genuinely large operating-leverage inversion, not a rounding error", -0.4, 0.15),
    ("+", "The stock's 36% drawdown from its high has already priced in real caution about the margin story", +0.3, 0.15),
    ("-", "Polish grocery is a mature, low-margin, intensely competitive category with limited pricing power for any single player", -0.3, 0.10),
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
CONS_EPS_2YR  = 2.00    # PLN; conservative FY2028E: modest growth off FY2026E, margin stays pressured
CONS_PE_2YR   = 17      # a modest de-rating from ~18.4× as the margin story stays unresolved
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
print(f"  {TICKER}  ·  {COMPANY}  ·  {CURRENT_PRICE:.2f} zł  ·  Grocery Retail (down 36% from 52W high)")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]  (all figures in PLN)")
print("═" * (W + 4))

# ─── ① REVENUE BRIDGE ─────────────────────────────────────────────────────────
print()
print("  REVENUE BRIDGE  (FY2026E, PLN billions  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<40}  {'FY26E (B zł)':>13}  {'Bear (B zł)':>11}  {'Bull (B zł)':>11}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<40}  {curr:>11.1f}  {bear:>9.1f}  {bull:>9.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<40}  {curr_total:>11.1f}  {bear_total:>9.1f}  {bull_total:>9.1f}")
print(f"  Q1 2026 actual: 8,896M zł revenue (+14.8% YoY), 316.3M zł net profit (+1.6% YoY)")
print()

# EPS bridge (net-margin based)
shares    = SHARES_OUT_M / 1000
curr_net  = curr_total * NET_MARGIN_CURR
curr_eps  = round(curr_net / shares, 2)

bull_net  = bull_total * NET_MARGIN_BULL
shares_b  = shares * 0.99
bull_eps_imp = round(bull_net / shares_b, 2)

bear_net  = bear_total * NET_MARGIN_BEAR
bear_eps_imp = round(bear_net / shares, 2)

print(f"  FY2026E EPS check:  {curr_total:.1f}B zł rev × {NET_MARGIN_CURR*100:.2f}% net margin")
print(f"  ÷ {shares:.4f}B shares  =  {curr_eps:.2f} zł/share  (model estimate {EPS_FY2026E:.2f} zł  ✓)")
print()
print(f"  BULL EPS check:  {bull_total:.1f}B zł rev × {NET_MARGIN_BULL*100:.2f}% net margin, post-buyback")
print(f"  =  ~{bull_eps_imp:.2f} zł/share  →  × {SCENARIOS['BULL'][1]}× = ~{bull_eps_imp*SCENARIOS['BULL'][1]:.0f} zł  ✓ BULL {SCENARIOS['BULL'][2]} zł")
print()
print(f"  BEAR EPS check:  {bear_total:.1f}B zł rev × {NET_MARGIN_BEAR*100:.2f}% net margin (price war escalates)")
print(f"  =  ~{bear_eps_imp:.2f} zł/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~{bear_eps_imp*SCENARIOS['BEAR'][1]:.0f} zł  ✓ BEAR {SCENARIOS['BEAR'][2]} zł")

# PRICE WAR CHECK
print()
print(f"  PRICE WAR CHECK  (the Dino-specific angle):")
print(f"  Q1 2026 LFL growth:                     +{Q1_2026_LFL_GROWTH_PCT:.1f}% YoY")
print(f"  Q1 2026 total revenue growth:            +{Q1_2026_REVENUE_GROWTH_PCT:.1f}% YoY")
print(f"  New stores (Q1) / total:                 {NEW_STORES_Q1}  /  {TOTAL_STORES:,}")
print(f"  Net sales area growth:                   +{NET_SALES_AREA_GROWTH_PCT:.1f}% YoY")
print(f"  Current net margin (vs 7.2% a year ago):  {NET_MARGIN_CURRENT_PCT:.1f}%")
print(f"  Stock drawdown from 52-week high:        -{STOCK_DRAWDOWN_FROM_HIGH_PCT}%")
print(f"  Key competitors:                         {KEY_COMPETITORS}")
print()
print(f"  Dino's own management has made an explicit strategic choice: hold prices down and prioritize")
print(f"  volume/market-share over near-term margin, even as {KEY_COMPETITORS} escalate their own price")
print(f"  competition. The demand side of that bet is working (LFL +4.4%, revenue +14.8%) — the margin side")
print(f"  is the genuine open question, and the stock's 36% drawdown reflects real doubt about the payoff timeline.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = 1.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every 1B zł revenue (at 4.73% margin):  +{eps_per_1B_rev:.4f} zł/EPS  = +{eps_per_1B_rev*18:.2f} zł/share at 18× P/E")
print(f"  Every 1pp of net margin:                 +{curr_total*0.01/shares:.4f} zł/EPS  = +{curr_total*0.01/shares*18:.2f} zł/share at 18× P/E")
print(f"  Every 1 turn of P/E:                     ±{EPS_FY2026E:.2f} zł/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (LFL growth / revenue / store area / margin / profit gap / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<38}  {'BEAR':>10}  {'BASE':>9}  {'BULL':>9}  {'XBULL':>9}  {'NOW':>11}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<38}  {ths[0]:>10}  {ths[1]:>9}  {ths[2]:>9}  {ths[3]:>9}  {s['now']:>11}  {lbl}  {b}")
    print(f"    {s['comment']}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from {CURRENT_PRICE} zł + 15%/yr hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:88]:<88}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR {bear_price} zł)")
hr()
print(f"  {'Signal':<32}  {'Current':>10}  {'Bear val':>10}  Trigger")
hr()
bear_triggers = [
    ("LFL sales growth",            "+4.4%",  "<0%",     "Discounter price war intensifies enough to actually shrink like-for-like sales"),
    ("Total revenue growth",        "+14.8%", "<8%",     "New-store productivity declines as the network matures and saturates key regions"),
    ("Net sales area growth",       "+13.0%", "<6%",     "Management slows the store rollout pace in response to margin pressure"),
    ("Net margin",                  "6.7%",   "<4%",     "The volume-over-margin strategy fails to stabilize as competitors match every price cut"),
    ("Profit/revenue growth gap",   "13.2pp", ">10pp gap persists","The operating-leverage inversion becomes structural rather than a transitional cost"),
    ("Forward P/E",                 "~18.4x", ">24x",    "Ironically, P/E can rise even as price falls if EPS collapses faster than price does"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the bear case doesn't require Dino to stop growing — it requires the price war with")
print(f"  Biedronka and Lidl to keep widening the gap between revenue growth and profit growth indefinitely,")
print(f"  rather than the current squeeze being a transitional cost of defending market share.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS estimate:       {EPS_FY2026E:.2f} zł  (forward-P/E-implied from consensus)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (a genuine grocery-retail-trough multiple)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    {EPP:.0f} zł/share")
print(f"  Current {CURRENT_PRICE:.2f} zł vs EPP {EPP:.0f} zł:  {epp_gap_pct:+.1f}%")
print()
print(f"  At {CURRENT_PRICE:.2f} zł the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS, down meaningfully from its")
print(f"  pre-drawdown multiple. The EPP floor provides real, if not enormous, margin of safety versus a")
print(f"  genuine competitive-pressure scenario.")
print(f"  At a 17× reversion (a modest premium to trough): {EPS_FY2026E:.2f} × 17 = {EPS_FY2026E*17:.0f} zł  ({(EPS_FY2026E*17/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest growth off FY2026E, margin stays pressured)")
hr()
print(f"  Conservative FY2028E EPS:  {CONS_EPS_2YR:.2f} zł  (~14% cumulative EPS growth — below the historical store-rollout-driven trajectory)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~18.4× → 17×; a modest de-rating)")
print(f"  Conservative equity value:   {cons_equity:.2f} zł/share")
print(f"  + Cumulative dividends (2yr): +{cons_divs:.2f} zł/share  (no dividend — cash reinvested in store growth)")
hr()
print(f"  Conservative 2yr total:      {cons_total:.2f} zł  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from {CURRENT_PRICE:.2f} zł)")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: a conservative case with continued but margin-pressured growth and only a modest")
print(f"  de-rating still comes out {'positive' if cons_return > 0 else 'negative'}, largely because the stock has already re-priced so much of the margin")
print(f"  concern. The real risk isn't a growth slowdown — it's the margin gap never closing.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.35
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        {VOL_52W_LOW:.2f} – {VOL_52W_HIGH:.2f} zł  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Recent moves:          -15% on the March 26 earnings release alone; -36% peak-to-trough YTD")
print(f"  Annual dividend:      0.00 zł/share  (no dividend; cash reinvested in growth)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (elevated — the market is actively re-pricing the margin story quarter to quarter)")
print(f"  Beta vs WIG20:        0.95  (roughly in line with the Warsaw benchmark)")
print(f"  1-sigma range (1yr):  {sigma_range[0]:.0f} – {sigma_range[1]:.0f} zł  ({CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear {bear_price} zł requires:  ~{bear_sigmas:.1f}σ drawdown  (a real move, but the stock has already moved ~1σ this year)")
print(f"  → Q2 2026 print (late August) is the next test of whether the margin gap narrows or keeps widening.")
print(f"  → Weekly/monthly discounter pricing actions (Biedronka, Lidl) are the leading indicators between prints.")
print(f"  → {signal_short} at {CURRENT_PRICE:.2f} zł  |  Add below 26 zł  |  Trim above 42 zł")

# ─── ⑦ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print()
print("  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
hr()
probs_mkt = softmax_probs(MARKET_COMPOSITE)
print(f"  {'Scenario':<10}  {'Price':>9}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>7}  Description")
hr()
for s in ["BEAR","BASE","BULL","XBULL"]:
    pp  = probs_proxy[s] * 100
    pm  = probs_mkt[s]   * 100
    gap = pp - pm
    pr  = SCENARIOS[s][2]
    desc = SCENARIOS[s][3][:44]
    print(f"  {s:<10}  {pr:>6} zł  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): {ev_adj:.0f} zł  /  Proxy EV: {ev_prx:.0f} zł  /  Market EV: {ev_mkt:.0f} zł  /  Current: {CURRENT_PRICE:.0f} zł")
hr()
print(f"  Downside  (→ Bear {bear_price} zł):  {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull {bull_price} zł):  {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b_str}")
print(f"  Signal    :  {signal_full}")
print()
print(f"  MARKET PRICING: at {CURRENT_PRICE:.2f} zł the market composite is {MARKET_COMPOSITE:.2f}/4.0. The model's")
print(f"  adjusted composite is {ADJ_COMPOSITE:.2f}/4.0, for a gap of {ADJ_GAP:+.2f} — {valuation_label.lower()}.")
print(f"  Dino's demand engine (LFL growth, store rollout) is genuinely intact — the entire investment case")
print(f"  now rests on whether the margin gap versus revenue growth closes over the next few quarters.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q2 2026 print (late August) — does the profit/revenue growth gap start narrowing?")
print(f"  (2) Biedronka and Lidl pricing actions — the leading indicator for competitive intensity")
print(f"  (3) Net margin trend — watch specifically for stabilization near or below the current 6.7%")
print(f"  (4) Store rollout pace — any deceleration would signal a strategic response to margin pressure")
print(f"  (5) Management commentary on the pricing policy — any signal of a shift away from volume-first")
print(f"  {signal_short} at {CURRENT_PRICE:.2f} zł  |  Add below 26 zł  |  Trim above 42 zł")
print(f"  EPP floor: {EPP:.0f} zł  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: {EPS_FY2026E:.2f} zł  |  Net margin: {NET_MARGIN_CURRENT_PCT:.1f}%")
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
