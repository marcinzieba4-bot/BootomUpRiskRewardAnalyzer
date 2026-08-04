"""
KTY  ·  Grupa Kęty S.A.  ·  WSE: KTY
Bottom-up signal model  ·  Aluminium Extrusion / Architectural Systems / Raw-Material Cost Pass-Through
Currency: PLN (Polish złoty) — this model is denominated natively in PLN, not USD
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "KTY"
COMPANY       = "Grupa Kęty S.A."
SECTOR        = "Aluminium Extrusion · Architectural Systems · GPW: KTY (PLN)"
CURRENT_PRICE = 1_277.0     # PLN; close 2026-08-04, near the 52-week high
VOL_52W_LOW   = 855.0       # PLN
VOL_52W_HIGH  = 1_362.0     # PLN
SHARES_OUT_M  = 9.86        # millions
ANNUAL_DIV    = 50.0        # PLN/share; a reliable, well-established dividend payer (~3.9% yield)

# ── REVENUE BRIDGE (FY2026E, PLN millions) ────────────────────────────────────
# Q2 2026 actual: net profit 241M zł, operating profit 318M zł (+35% YoY, 19.2% op margin), EBITDA
# margin 23.0% (up from 20.5% a year ago), revenue +15% YoY on higher volumes in Extruded Products and
# Architectural Systems PLUS price increases passing through dramatic raw-material cost inflation —
# aluminum prices +40% YoY in PLN terms, billet premiums +120%, polymer granulate +66%. H1 2026: sales
# 3,028M zł (51% of the full-year target), EBITDA 636M zł (57% of target), net profit 386M zł (61% of
# target) — pacing ahead of a straight-line annualization, a genuinely strong first half.
SEG_DATA = [
    # (segment, curr_rev_M, bear_rev_M, bull_rev_M, description)
    ("Extruded Products",      3_200.0, 2_600.0, 3_700.0, "The core volume/pricing engine; successfully passing through extreme aluminum and billet cost inflation"),
    ("Architectural Systems",  2_737.0, 2_200.0, 3_300.0, "Higher-margin systems business; growing faster than Extruded Products on volume and mix"),
]

# Net-margin-based bridge (industrials: revenue minus opex/D&A/tax collapses to net margin)
NET_MARGIN_CURR = 0.1066  # FY2026E; reconciles to management's own implied full-year net profit target
NET_MARGIN_BEAR = 0.0797  # BEAR: raw-material cost inflation (aluminum +40%, billet +120%) outpaces price pass-through
NET_MARGIN_BULL = 0.1442  # BULL: pricing power holds and volume growth adds genuine operating leverage on top

# ── RAW-MATERIAL COST PASS-THROUGH CALCULATOR (the Kęty-specific angle) ──────
Q2_2026_NET_PROFIT_M       = 241   # PLN millions; Q2 2026 net profit
Q2_2026_OP_MARGIN_PCT      = 19.2  # %; Q2 2026 operating margin, +35% YoY operating profit growth
Q2_2026_EBITDA_MARGIN_PCT  = 23.0  # %; Q2 2026 EBITDA margin, up from 20.5% a year ago
ALUMINUM_PRICE_YOY_PCT     = 40    # % YoY increase in aluminum prices (PLN terms)
BILLET_PREMIUM_YOY_PCT     = 120   # % YoY increase in billet premiums
POLYMER_GRANULATE_YOY_PCT  = 66    # % YoY increase in polymer granulate prices
H1_PCT_OF_FY_SALES_TARGET  = 51    # % of full-year sales target achieved in H1 2026
H1_PCT_OF_FY_PROFIT_TARGET = 61    # % of full-year net profit target achieved in H1 2026

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 64.2        # PLN/share FY2026E; derived from management's own implied full-year profit target
PE_PESSIMISTIC = 14.0        # trough P/E: a genuine industrials-trough multiple
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  (38.79, 14,   543, "Raw-material cost inflation (aluminum, billet, polymer) finally outpaces price pass-through, compressing margins hard"),
    "BASE":  (67.16, 19.9, 1_337, "Volume growth and successful cost pass-through continue roughly as guided through the rest of FY2026"),
    "BULL":  (102.36, 17.5, 1_791, "Pricing power holds even as raw-material costs stay elevated, and volume growth adds genuine operating leverage"),
    "XBULL": (130.40, 19,  2_478, "Margins keep expanding as demonstrated in H1, while volume growth accelerates further across both segments"),
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
        "name":       "Revenue YoY growth",
        "weight":     0.15,
        "thresholds": ("<5%",    "≥9%",    "≥13%",   "≥17%"),
        "now":        "+15%",
        "score":      3,
        "comment":    "Genuine volume growth in both segments, on top of price increases reflecting real cost inflation",
    },
    {
        "name":       "Operating margin trend",
        "weight":     0.20,
        "thresholds": ("<12%",   "≥15%",   "≥17%",   "≥19%"),
        "now":        "19.2%",
        "score":      4,
        "comment":    "Operating profit +35% YoY DESPITE aluminum +40% and billet premiums +120% — genuinely impressive cost pass-through execution",
    },
    {
        "name":       "EBITDA margin trend",
        "weight":     0.15,
        "thresholds": ("<17%",   "≥19%",   "≥21%",   "≥23%"),
        "now":        "23.0%",
        "score":      4,
        "comment":    "Up from 20.5% a year ago — margin expansion, not just absolute cost pass-through",
    },
    {
        "name":       "H1 pacing vs full-year profit target",
        "weight":     0.20,
        "thresholds": ("<40%",   "≥45%",   "≥50%",   "≥55%"),
        "now":        "61%",
        "score":      4,
        "comment":    "H1 already delivered 61% of the full-year net profit target — running well ahead of straight-line pacing",
    },
    {
        "name":       "Raw-material cost inflation severity",
        "weight":     0.15,
        "thresholds": ("extreme, unmanaged","severe but passed through","moderate","benign"),
        "now":        "severe but passed through",
        "score":      3,
        "comment":    "Aluminum +40%, billet +120%, polymer +66% — a genuinely severe cost shock that's being successfully managed, not a mild headwind",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.15,
        "thresholds": (">26x",   "≤22x",   "≤19x",   "≤16x"),
        "now":        "~19.9x",
        "score":      3,
        "comment":    "19.9× FY2026E EPS — a reasonable multiple given the demonstrated margin resilience, near the 52-week high",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Successfully passing through aluminum +40%/billet +120% cost inflation while EXPANDING margins is genuinely rare execution, not luck", +0.5, 0.20),
    ("-", "That same severity of raw-material inflation means any pricing missteps or a sudden further spike could reverse the margin gains quickly", -0.4, 0.20),
    ("+", "H1 2026 pacing at 61% of the full-year profit target suggests real upside to guidance if the trend simply continues, not even accelerates", +0.4, 0.15),
    ("-", "The stock is already trading near its 52-week high, leaving less margin for error if the cost-inflation story turns", -0.3, 0.15),
    ("+", "Architectural Systems' higher margin and faster growth than Extruded Products is a favorable, durable mix shift", +0.3, 0.15),
    ("-", "Grupa Kęty is meaningfully exposed to European construction/industrial demand cycles, which remain a genuine macro swing factor", -0.3, 0.15),
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
CONS_EPS_2YR  = 72.0    # PLN; conservative FY2028E: modest growth off FY2026E
CONS_PE_2YR   = 18      # a modest de-rating from ~19.9×
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
print(f"  {TICKER}  ·  {COMPANY}  ·  {CURRENT_PRICE:,.0f} zł  ·  Extruded Products / Architectural Systems")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]  (all figures in PLN)")
print("═" * (W + 4))

# ─── ① REVENUE BRIDGE ─────────────────────────────────────────────────────────
print()
print("  REVENUE BRIDGE  (FY2026E, PLN millions  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(p for _, p, _, _, _ in SEG_DATA)
bear_total = sum(p for _, _, p, _, _ in SEG_DATA)
bull_total = sum(p for _, _, _, p, _ in SEG_DATA)

print(f"  {'Segment':<32}  {'FY26E (M zł)':>13}  {'Bear (M zł)':>11}  {'Bull (M zł)':>11}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<32}  {curr:>11,.0f}  {bear:>9,.0f}  {bull:>9,.0f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL REVENUE':<32}  {curr_total:>11,.0f}  {bear_total:>9,.0f}  {bull_total:>9,.0f}")
print(f"  Q2 2026 actual: {Q2_2026_NET_PROFIT_M}M zł net profit; H1 2026: 386M zł (61% of FY target)")
print()

# EPS bridge (net-margin based)
shares    = SHARES_OUT_M
curr_net  = curr_total * NET_MARGIN_CURR
curr_eps  = round(curr_net / shares, 2)

bull_net  = bull_total * NET_MARGIN_BULL
bull_eps_imp = round(bull_net / shares, 2)

bear_net  = bear_total * NET_MARGIN_BEAR
bear_eps_imp = round(bear_net / shares, 2)

print(f"  FY2026E EPS check:  {curr_total:,.0f}M zł rev × {NET_MARGIN_CURR*100:.2f}% net margin")
print(f"  ÷ {shares:.2f}M shares  =  {curr_eps:.2f} zł/share  (model estimate {EPS_FY2026E:.2f} zł  ✓)")
print()
print(f"  BULL EPS check:  {bull_total:,.0f}M zł rev × {NET_MARGIN_BULL*100:.2f}% net margin")
print(f"  =  {bull_eps_imp:.2f} zł/share  →  × {SCENARIOS['BULL'][1]}× = ~{bull_eps_imp*SCENARIOS['BULL'][1]:.0f} zł  ✓ BULL {SCENARIOS['BULL'][2]:,.0f} zł")
print()
print(f"  BEAR EPS check:  {bear_total:,.0f}M zł rev × {NET_MARGIN_BEAR*100:.2f}% net margin (cost inflation outpaces pass-through)")
print(f"  =  {bear_eps_imp:.2f} zł/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~{bear_eps_imp*SCENARIOS['BEAR'][1]:.0f} zł  ✓ BEAR {SCENARIOS['BEAR'][2]:,.0f} zł")

# RAW-MATERIAL COST PASS-THROUGH CHECK
print()
print(f"  RAW-MATERIAL COST PASS-THROUGH CHECK  (the Kęty-specific angle):")
print(f"  Q2 2026 net profit / op margin / EBITDA margin:  {Q2_2026_NET_PROFIT_M}M zł / {Q2_2026_OP_MARGIN_PCT:.1f}% / {Q2_2026_EBITDA_MARGIN_PCT:.1f}%")
print(f"  Aluminum price inflation (YoY, PLN):               +{ALUMINUM_PRICE_YOY_PCT}%")
print(f"  Billet premium inflation (YoY):                    +{BILLET_PREMIUM_YOY_PCT}%")
print(f"  Polymer granulate inflation (YoY):                 +{POLYMER_GRANULATE_YOY_PCT}%")
print(f"  H1 2026 pacing vs FY targets (sales / profit):     {H1_PCT_OF_FY_SALES_TARGET}% / {H1_PCT_OF_FY_PROFIT_TARGET}%")
print()
print(f"  This is the standout data point: raw-material costs rose by extraordinary amounts (aluminum +40%,")
print(f"  billet premiums +120%) and Grupa Kęty's operating margin EXPANDED anyway, to 19.2% from a lower")
print(f"  base a year ago. That's genuine pricing power and operational discipline, not just a commodity")
print(f"  pass-through — and it's the single best argument for the bull case in this entire batch.")

# KEY SENSITIVITIES
print()
eps_per_100M_profit = 100.0 / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every 100M zł net profit:                +{eps_per_100M_profit:.2f} zł/EPS  = +{eps_per_100M_profit*20:.2f} zł/share at 20× P/E")
print(f"  Every 1 turn of P/E:                      ±{EPS_FY2026E:.2f} zł/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")
print(f"  Dividend cushion:                          {ANNUAL_DIV:.0f} zł/yr absorbs ~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}% of any annual price drawdown")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (revenue / op margin / EBITDA margin / H1 pacing / cost severity / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<38}  {'BEAR':>21}  {'BASE':>26}  {'BULL':>9}  {'XBULL':>8}  {'NOW':>26}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<38}  {ths[0]:>21}  {ths[1]:>26}  {ths[2]:>9}  {ths[3]:>8}  {s['now']:>26}  {lbl}  {b}")
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
print(f"  {'Signal':<32}  {'Current':>10}  {'Bear val':>10}  Trigger")
hr()
bear_triggers = [
    ("Revenue growth",              "+15%",   "<5%",     "European construction/industrial demand softens meaningfully, hitting volumes directly"),
    ("Operating margin",            "19.2%",  "<12%",    "A further raw-material cost spike finally outpaces the company's pricing power"),
    ("EBITDA margin",               "23.0%",  "<17%",    "Cost pass-through breaks down across both segments simultaneously"),
    ("H1 pacing vs FY target",      "61%",    "<40%",    "H2 disappoints sharply relative to the strong H1, a genuine reversal of trend"),
    ("Cost inflation severity",     "passed through","unmanaged","Aluminum/billet costs spike further and faster than the company can reprice contracts"),
    ("Forward P/E",                 "~19.9x", ">26x",    "Market fully re-prices Kęty for a slower, margin-compressed trajectory"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the bear case requires Kęty's demonstrated pricing power to fail — a real risk given")
print(f"  how extreme the current cost inflation already is (billet premiums +120%), but one the company has")
print(f"  so far navigated successfully enough to expand, not compress, margins.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS estimate:       {EPS_FY2026E:.2f} zł  (derived from management's own implied full-year profit target)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (a genuine industrials-trough multiple)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    {EPP:,.0f} zł/share")
print(f"  Current {CURRENT_PRICE:,.0f} zł vs EPP {EPP:,.0f} zł:  {epp_gap_pct:+.1f}%")
print()
print(f"  At {CURRENT_PRICE:,.0f} zł the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS, near its 52-week high after a genuinely")
print(f"  strong H1. The EPP floor provides real margin of safety versus a scenario where the current cost")
print(f"  pass-through success reverses.")
print(f"  At a 16× reversion (a modest premium to trough): {EPS_FY2026E:.2f} × 16 = {EPS_FY2026E*16:.0f} zł  ({(EPS_FY2026E*16/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest growth off FY2026E)")
hr()
print(f"  Conservative FY2028E EPS:  {CONS_EPS_2YR:.2f} zł  (~12% cumulative EPS growth — below the current strong-H1 trajectory)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~19.9× → 18×; a modest de-rating)")
print(f"  Conservative equity value:   {cons_equity:,.0f} zł/share")
print(f"  + Cumulative dividends (2yr): +{cons_divs:.0f} zł/share  ({ANNUAL_DIV:.0f} zł/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      {cons_total:,.0f} zł  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):,.0f} from {CURRENT_PRICE:,.0f} zł)")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: even a conservative case with modest growth and a modest de-rating still comes out")
print(f"  {'positive' if cons_return > 0 else 'negative'}, aided by a reliable ~3.9% dividend yield — a reasonable, if not spectacular, margin of safety")
print(f"  for a stock sitting near its 52-week high.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.24
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        {VOL_52W_LOW:,.0f} – {VOL_52W_HIGH:,.0f} zł  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      {ANNUAL_DIV:.0f} zł/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; a reliable, well-established payer)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (moderate — typical for a mid-cap industrials compounder)")
print(f"  Beta vs WIG20:        0.90  (slightly below the Warsaw benchmark)")
print(f"  1-sigma range (1yr):  {sigma_range[0]:,.0f} – {sigma_range[1]:,.0f} zł  ({CURRENT_PRICE:,.0f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear {bear_price:,.0f} zł requires:  ~{bear_sigmas:.1f}σ drawdown  (large, consistent with a genuine cost-pass-through-failure scenario)")
print(f"  → Q3 2026 print (likely November) is the next test of whether H2 pacing holds up against the strong H1.")
print(f"  → Aluminum/billet spot prices and Kęty's own pricing announcements are the leading indicators between prints.")
print(f"  → {signal_short} at {CURRENT_PRICE:,.0f} zł  |  Add below 1,050 zł  |  Trim above 1,550 zł")

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
    print(f"  {s:<10}  {pr:>7,.0f} zł  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

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
print(f"  Grupa Kęty just demonstrated genuinely impressive pricing power against an extreme raw-material")
print(f"  cost shock — the question for the next two years is whether that discipline holds if costs spike further.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q3 2026 print (likely November) — does H2 pacing hold up against the strong 61%-of-target H1?")
print(f"  (2) Aluminum, billet premium, and polymer granulate spot prices — the leading cost-inflation indicators")
print(f"  (3) Any signs of margin compression as the company continues repricing contracts")
print(f"  (4) European construction/industrial demand data — the macro backdrop for both segments")
print(f"  (5) Dividend policy continuity — confirms the reliable payer thesis")
print(f"  {signal_short} at {CURRENT_PRICE:,.0f} zł  |  Add below 1,050 zł  |  Trim above 1,550 zł")
print(f"  EPP floor: {EPP:,.0f} zł  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: {EPS_FY2026E:.2f} zł  |  H1 pacing vs FY profit target: {H1_PCT_OF_FY_PROFIT_TARGET}%")
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
