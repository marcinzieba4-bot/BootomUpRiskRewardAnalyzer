"""
PKO  ·  Powszechna Kasa Oszczędności Bank Polski S.A.  ·  WSE: PKO
Bottom-up signal model  ·  Universal Banking / Net Interest Margin Cycle / Fee Income Diversification
Currency: PLN (Polish złoty) — this model is denominated natively in PLN, not USD
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "PKO"
COMPANY       = "Powszechna Kasa Oszczędności Bank Polski S.A."
SECTOR        = "Universal Banking · Net Interest Margin Cycle · Fee Income · GPW: PKO (PLN)"
CURRENT_PRICE = 105.68      # PLN; close 2026-08-03, near the 52-week high
VOL_52W_LOW   = 67.78       # PLN
VOL_52W_HIGH  = 108.08      # PLN
SHARES_OUT_M  = 1_250.0     # millions
ANNUAL_DIV    = 6.20        # PLN/share; ~5.9% yield

# ── REVENUE BRIDGE (FY2026E, PLN billions) ────────────────────────────────────
# Q1 2026 actual: EPS 2.02 zł (beat 1.95 est), net profit up ~12% YoY to 2.5B zł, revenue 7.78B zł,
# ROE 17.3%, gross income +17% YoY to 4B zł, net fee & commission income +10.1% YoY, total assets
# +12% YoY to 594B zł. Management guided stable net interest income and mid-high single-digit fee
# growth for FY2026, but flagged margin pressure from rate cuts and higher costs in H2 — and targets
# ROE above 18% by 2027 (assuming a 26% CIT rate). The stock is up ~37% over the past year.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Net Interest Income",                24.5, 20.5, 28.5, "The core rate-cycle-sensitive revenue line; management has explicitly flagged H2 margin pressure from rate cuts"),
    ("Fee & Commission Income + Other",      8.2,  7.0, 10.5, "+10.1% YoY in Q1 — the diversification away from pure NII/rate-cycle dependence"),
]

# Net-margin-based bridge (bank economics: revenue minus provisions/opex/tax collapses to net margin)
NET_MARGIN_CURR = 0.321   # FY2026E; matches Q1 2026's actual net margin (2.5B / 7.78B)
NET_MARGIN_BEAR = 0.240   # BEAR: rate-cut-driven NIM compression plus rising provisions/costs
NET_MARGIN_BULL = 0.350   # BULL: NIM holds up better than guided while fee income keeps growing — real progress toward the >18% ROE target

# ── RATE-CYCLE / ROE-TRAJECTORY CALCULATOR (the PKO-specific angle) ──────────
Q1_2026_NET_PROFIT_B      = 2.5    # PLN billions; Q1 2026 net profit, ~+12% YoY
Q1_2026_ROE_PCT           = 17.3   # %; Q1 2026 return on equity
FEE_INCOME_GROWTH_PCT     = 10.1   # % YoY, Q1 2026 net fee & commission income growth
GROSS_INCOME_GROWTH_PCT   = 17.0   # % YoY, Q1 2026 gross income growth
TOTAL_ASSETS_GROWTH_PCT   = 12.0   # % YoY, Q1 2026 total assets growth
ROE_2027_TARGET_PCT       = 18.0   # %; management's FY2027 ROE target (assuming a 26% CIT rate)
STOCK_1YR_GAIN_PCT        = 37.3   # %; trailing 1-year stock price gain

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 8.40        # PLN/share FY2026E; forward-P/E-implied from consensus
PE_PESSIMISTIC = 9.0         # trough P/E: a genuine Polish-banking-sector-trough multiple
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 5.28,  9,   48, "Rate cuts compress NIM faster than guided while provisions and CHF-mortgage-litigation costs rise simultaneously"),
    "BASE":  ( 8.76, 12.6, 110, "NII holds roughly flat as guided while fee income continues its mid-high single-digit growth"),
    "BULL":  (10.92, 14,  153, "NIM proves more resilient than management's own cautious guidance, and the ROE trajectory toward 18%+ continues"),
    "XBULL": (13.43, 16,  215, "PKO decisively hits and exceeds the 18%+ ROE target ahead of the 2027 schedule, re-rating the stock toward regional bank premiums"),
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
        "name":       "Net profit YoY growth",
        "weight":     0.15,
        "thresholds": ("<0%",    "≥5%",    "≥10%",   "≥15%"),
        "now":        "+12%",
        "score":      3,
        "comment":    "Q1 2026 net profit ~+12% YoY to 2.5B zł, beating the EPS estimate",
    },
    {
        "name":       "Return on equity (ROE)",
        "weight":     0.15,
        "thresholds": ("<10%",   "≥13%",   "≥16%",   "≥19%"),
        "now":        "17.3%",
        "score":      3,
        "comment":    "Tracking toward management's own >18% FY2027 target — a guided, not speculative, trajectory",
    },
    {
        "name":       "Fee & commission income growth",
        "weight":     0.15,
        "thresholds": ("<3%",    "≥6%",    "≥9%",    "≥12%"),
        "now":        "+10.1%",
        "score":      3,
        "comment":    "Real diversification away from pure net-interest-income/rate-cycle dependence",
    },
    {
        "name":       "Net interest margin (NIM) trend",
        "weight":     0.20,
        "thresholds": ("compressing sharply","pressure emerging","stable","expanding"),
        "now":        "pressure emerging",
        "score":      2,
        "comment":    "Management itself flagged margin pressure from rate cuts and higher costs in H2 2026 — a real, guided near-term headwind",
    },
    {
        "name":       "Gross income growth",
        "weight":     0.15,
        "thresholds": ("<5%",    "≥10%",   "≥15%",   "≥20%"),
        "now":        "+17%",
        "score":      3,
        "comment":    "A strong headline growth number despite the margin-pressure guidance for later in the year",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.20,
        "thresholds": (">18x",   "≤15x",   "≤13x",   "≤10x"),
        "now":        "~12.6x",
        "score":      3,
        "comment":    "12.6× forward earnings — reasonable for Poland's largest bank with a mid-teens ROE, but not statistically cheap near the 52-week high",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "ROE of 17.3% trending toward management's own >18% FY2027 target reflects genuine, guided operating improvement, not just a rate-cycle tailwind", +0.4, 0.20),
    ("-", "Management explicitly flagged margin pressure from rate cuts and higher costs in H2 2026 — a real, guided near-term headwind, not a hypothetical one", -0.4, 0.20),
    ("+", "Fee and commission income growth (+10.1%) diversifies revenue away from pure NII/rate-cycle dependence", +0.3, 0.15),
    ("-", "The stock is already up ~37% over the past year and trading near its 52-week high — much of the good news may already be priced in", -0.4, 0.15),
    ("-", "Poland's banking sector carries recurring CHF-mortgage-litigation and regulatory windfall-tax risk that periodically resurfaces industry-wide", -0.3, 0.15),
    ("+", "As Poland's largest bank, PKO benefits from scale and systemic importance that smaller regional peers lack", +0.3, 0.15),
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
CONS_EPS_2YR  = 9.00    # PLN; conservative FY2028E: modest growth off FY2026E, the guided H2 margin pressure partly bites
CONS_PE_2YR   = 12      # roughly flat to the current ~12.6× multiple
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
print(f"  {TICKER}  ·  {COMPANY}  ·  {CURRENT_PRICE:.2f} zł  ·  Universal Banking (near 52-week high)")
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
print(f"  Q1 2026 actual: 7.78B zł revenue, {Q1_2026_NET_PROFIT_B}B zł net profit (~+12% YoY), ROE {Q1_2026_ROE_PCT}%")
print()

# EPS bridge (net-margin based)
shares    = SHARES_OUT_M / 1000
curr_net  = curr_total * NET_MARGIN_CURR
curr_eps  = round(curr_net / shares, 2)

bull_net  = bull_total * NET_MARGIN_BULL
bull_eps_imp = round(bull_net / shares, 2)

bear_net  = bear_total * NET_MARGIN_BEAR
bear_eps_imp = round(bear_net / shares, 2)

print(f"  FY2026E EPS check:  {curr_total:.1f}B zł rev × {NET_MARGIN_CURR*100:.1f}% net margin")
print(f"  ÷ {shares:.3f}B shares  =  {curr_eps:.2f} zł/share  (model estimate {EPS_FY2026E:.2f} zł  ✓)")
print()
print(f"  BULL EPS check:  {bull_total:.1f}B zł rev × {NET_MARGIN_BULL*100:.1f}% net margin")
print(f"  =  ~{bull_eps_imp:.2f} zł/share  →  × {SCENARIOS['BULL'][1]}× = ~{bull_eps_imp*SCENARIOS['BULL'][1]:.0f} zł  ✓ BULL {SCENARIOS['BULL'][2]} zł")
print()
print(f"  BEAR EPS check:  {bear_total:.1f}B zł rev × {NET_MARGIN_BEAR*100:.1f}% net margin (NIM compression + rising provisions)")
print(f"  =  ~{bear_eps_imp:.2f} zł/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~{bear_eps_imp*SCENARIOS['BEAR'][1]:.0f} zł  ✓ BEAR {SCENARIOS['BEAR'][2]} zł")

# RATE-CYCLE / ROE-TRAJECTORY CHECK
print()
print(f"  RATE-CYCLE / ROE-TRAJECTORY CHECK  (the PKO-specific angle):")
print(f"  Q1 2026 net profit / ROE:               {Q1_2026_NET_PROFIT_B}B zł / {Q1_2026_ROE_PCT}%")
print(f"  Fee & commission income growth:          +{FEE_INCOME_GROWTH_PCT:.1f}% YoY")
print(f"  Gross income growth:                     +{GROSS_INCOME_GROWTH_PCT:.1f}% YoY")
print(f"  Total assets growth:                     +{TOTAL_ASSETS_GROWTH_PCT:.1f}% YoY")
print(f"  Management's FY2027 ROE target:          >{ROE_2027_TARGET_PCT:.0f}%  (at a 26% CIT rate)")
print(f"  Trailing 1-year stock gain:              +{STOCK_1YR_GAIN_PCT:.1f}%")
print()
print(f"  PKO's own management has done something relatively unusual — explicitly guiding to H2 margin")
print(f"  pressure from rate cuts even while the stock sits near its 52-week high. That's either admirable")
print(f"  candor the market hasn't fully priced, or confirmation that the easy gains from this rate cycle")
print(f"  are behind it. The ROE trajectory toward 18%+ is the more durable, multi-year offsetting story.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = 1.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every 1B zł revenue (at 32.1% margin):  +{eps_per_1B_rev:.3f} zł/EPS  = +{eps_per_1B_rev*12.6:.2f} zł/share at 12.6× P/E")
print(f"  Every 1pp of net margin:                 +{curr_total*0.01/shares:.3f} zł/EPS  = +{curr_total*0.01/shares*12.6:.2f} zł/share at 12.6× P/E")
print(f"  Every 1 turn of P/E:                     ±{EPS_FY2026E:.2f} zł/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (profit growth / ROE / fee income / NIM trend / gross income / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<34}  {'BEAR':>19}  {'BASE':>17}  {'BULL':>7}  {'XBULL':>9}  {'NOW':>17}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<34}  {ths[0]:>19}  {ths[1]:>17}  {ths[2]:>7}  {ths[3]:>9}  {s['now']:>17}  {lbl}  {b}")
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
    ("Net profit growth",           "+12%",   "<0%",      "NIM compression from rate cuts outpaces fee income growth faster than guided"),
    ("ROE",                         "17.3%",  "<10%",     "The path toward the 18%+ 2027 target reverses rather than continues"),
    ("Fee income growth",           "+10.1%", "<3%",      "Fee diversification stalls, leaving the bank fully exposed to the NII/rate cycle again"),
    ("NIM trend",                   "pressure emerging","compressing sharply","Further, deeper-than-guided NBP rate cuts hit net interest income hard"),
    ("Gross income growth",         "+17%",   "<5%",      "The strong Q1 print proves to be a high-water mark rather than a trend"),
    ("Forward P/E",                 "~12.6x", ">18x",     "Market fully re-prices PKO for a slower, margin-pressured earnings trajectory"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: management's own H2 margin-pressure guidance is the single most important near-term")
print(f"  data point — it's a rare case of a bank pre-announcing its own headwind rather than being surprised")
print(f"  by it. The bear case requires that guided pressure to be worse than flagged, not merely present.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS estimate:       {EPS_FY2026E:.2f} zł  (forward-P/E-implied from consensus)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (a genuine Polish-banking-sector-trough multiple)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    {EPP:.0f} zł/share")
print(f"  Current {CURRENT_PRICE:.2f} zł vs EPP {EPP:.0f} zł:  {epp_gap_pct:+.1f}%")
print()
print(f"  At {CURRENT_PRICE:.2f} zł the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS, near its 52-week high after a")
print(f"  ~37% trailing 1-year gain. The EPP floor provides real margin of safety versus a genuine sector-trough")
print(f"  multiple, but the stock is clearly no longer statistically cheap the way it may have been a year ago.")
print(f"  At a 11× reversion (a modest premium to trough): {EPS_FY2026E:.2f} × 11 = {EPS_FY2026E*11:.0f} zł  ({(EPS_FY2026E*11/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest growth off FY2026E, guided H2 margin pressure partly bites)")
hr()
print(f"  Conservative FY2028E EPS:  {CONS_EPS_2YR:.2f} zł  (~7% cumulative EPS growth — below the current trajectory)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (roughly flat to the current ~12.6× multiple)")
print(f"  Conservative equity value:   {cons_equity:.2f} zł/share")
print(f"  + Cumulative dividends (2yr): +{cons_divs:.2f} zł/share  ({ANNUAL_DIV:.2f} zł/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      {cons_total:.2f} zł  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from {CURRENT_PRICE:.2f} zł)")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: a conservative case that takes management's own margin-pressure guidance at face")
print(f"  value and assumes no multiple re-rating still comes out {'positive' if cons_return > 0 else 'negative'}, largely on the back of the ~5.9% dividend")
print(f"  yield — but it's a modest, not compelling, margin of safety after the stock's run over the past year.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.26
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        {VOL_52W_LOW:.2f} – {VOL_52W_HIGH:.2f} zł  (stock at {vol_pct*100:.0f}th pct of 52W range, near the high)")
print(f"  Annual dividend:      {ANNUAL_DIV:.2f} zł/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (moderate, typical for a large, systemically important bank)")
print(f"  Beta vs WIG20:        1.10  (roughly in line with the Warsaw benchmark)")
print(f"  1-sigma range (1yr):  {sigma_range[0]:.0f} – {sigma_range[1]:.0f} zł  ({CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear {bear_price} zł requires:  ~{bear_sigmas:.1f}σ drawdown  (large, consistent with a genuine rate-cycle/provisioning shock)")
print(f"  → Q2 2026 print (mid-August) is the next test of whether the guided H2 margin pressure is showing up yet.")
print(f"  → NBP interest-rate decisions are the single leading indicator to watch between prints.")
print(f"  → {signal_short} at {CURRENT_PRICE:.2f} zł  |  Add below 88 zł  |  Trim above 130 zł")

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
print(f"  PKO is executing well on its ROE trajectory and fee-income diversification, but the stock has")
print(f"  already re-rated meaningfully, and management's own margin-pressure guidance argues for some")
print(f"  near-term caution even as the multi-year story remains intact.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q2 2026 print (mid-August) — is the guided H2 margin pressure starting to show up?")
print(f"  (2) NBP (Polish central bank) interest-rate decisions — the single leading indicator for NII")
print(f"  (3) ROE trajectory toward the >18% FY2027 target — the durable, multi-year offsetting story")
print(f"  (4) Fee & commission income growth sustainability at the +10%+ pace")
print(f"  (5) Any CHF-mortgage-litigation or windfall-tax developments affecting the Polish banking sector broadly")
print(f"  {signal_short} at {CURRENT_PRICE:.2f} zł  |  Add below 88 zł  |  Trim above 130 zł")
print(f"  EPP floor: {EPP:.0f} zł  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: {EPS_FY2026E:.2f} zł  |  ROE: {Q1_2026_ROE_PCT}% (target >{ROE_2027_TARGET_PCT:.0f}% by FY2027)")
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
