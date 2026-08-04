"""
ALE  ·  Allegro.eu S.A.  ·  WSE: ALE
Bottom-up signal model  ·  E-commerce Marketplace / Allegro Pay Fintech / International Expansion (Mall Group)
Currency: PLN (Polish złoty) — this model is denominated natively in PLN, not USD
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "ALE"
COMPANY       = "Allegro.eu S.A."
SECTOR        = "E-commerce Marketplace · Allegro Pay Fintech · International (Mall Group) · GPW: ALE (PLN)"
CURRENT_PRICE = 45.09       # PLN; close 2026-08-03, near the 52-week high
VOL_52W_LOW   = 25.53       # PLN
VOL_52W_HIGH  = 45.94       # PLN
SHARES_OUT_M  = 978.84      # millions
ANNUAL_DIV    = 0.0         # PLN/share; no dividend — cash reinvested in international expansion and Allegro Pay

# ── REVENUE BRIDGE (FY2026E, PLN billions) ────────────────────────────────────
# H1 2026 actual: Group GMV +14%, revenue +16%, adjusted EBITDA +17% YoY — all running AHEAD of full-year
# guidance (10-12% GMV, 12-15% revenue, 9-13% EBITDA growth). Q2 2026: consolidated GMV +14.4%, with
# Poland +12% and International +82.4% (Mall Group: Czech Republic, Slovakia, Hungary, Romania). Allegro
# Pay originated 3.4B PLN in loans in the quarter (+27.1% YoY), now financing 15.5% of GMV — a genuine
# fintech monetization lever. Forward P/E ~20.3x on a consensus-implied ~2.22 PLN FY2026E EPS.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Poland Marketplace",                    20.4, 19.0, 23.0, "The core profit engine; +12% GMV growth, but facing real price competition from Temu/Shein/AliExpress"),
    ("International (Mall Group: CZ/SK/HU/RO)", 3.6,  3.0,  5.2, "Smaller but accelerating fast — +82.4% GMV growth YoY, the clearest evidence the cross-border thesis is working"),
]

# Net-margin-based bridge (marketplace economics: take-rate revenue with a largely fixed logistics/tech opex base)
NET_MARGIN_CURR = 0.0905  # FY2026E; reconciles to the ~2.22 PLN consensus EPS
NET_MARGIN_BEAR = 0.0600  # BEAR: intensified low-cost-platform price competition compresses take rate and margin
NET_MARGIN_BULL = 0.1050  # BULL: Allegro Pay fintech monetization and International scale both lift the blended margin

# ── COMPETITIVE / FINTECH CALCULATOR (the Allegro-specific angle) ────────────
ALLEGRO_PAY_LOANS_Q_B       = 3.4   # PLN billions; Allegro Pay loans originated in the quarter, +27.1% YoY
ALLEGRO_PAY_GMV_PENETRATION = 15.5  # % of GMV financed via Allegro Pay
INTERNATIONAL_GMV_GROWTH    = 82.4  # % YoY, International (Mall Group) GMV growth
POLAND_GMV_GROWTH           = 12.0  # % YoY, Poland Marketplace GMV growth
H1_METRICS_VS_GUIDE         = "ahead on GMV, revenue, and EBITDA"  # H1 2026 running ahead of full-year guidance on all three headline metrics
LOW_COST_COMPETITORS        = "Temu, Shein, AliExpress"  # the structural competitive threat to Poland marketplace take rates

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 2.22        # PLN/share FY2026E; consensus-implied from the ~20.3x forward P/E
PE_PESSIMISTIC = 14.0        # trough P/E: a genuine e-commerce-marketplace-trough multiple under intensified competition
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  (1.35, 15,  20, "Temu/Shein-driven price competition intensifies further, compressing Poland take rates faster than International can offset"),
    "BASE":  (2.31, 20,  46, "GMV and revenue growth moderate toward the guided range as the H1 beat normalizes"),
    "BULL":  (3.03, 22,  67, "International expansion continues compounding at a high rate while Allegro Pay penetration keeps climbing"),
    "XBULL": (3.82, 24,  92, "International becomes a genuine second growth engine alongside Poland, with Allegro Pay reaching fintech-scale profitability"),
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
        "name":       "Group GMV YoY growth",
        "weight":     0.20,
        "thresholds": ("<5%",    "≥8%",    "≥12%",   "≥16%"),
        "now":        "+14.4%",
        "score":      3,
        "comment":    "Running ahead of the 10-12% full-year guidance range in both Q2 and H1",
    },
    {
        "name":       "International GMV growth",
        "weight":     0.15,
        "thresholds": ("<20%",   "≥40%",   "≥60%",   "≥80%"),
        "now":        "+82.4%",
        "score":      4,
        "comment":    "The clearest, fastest-growing evidence the Mall Group cross-border expansion is working",
    },
    {
        "name":       "Total revenue YoY growth",
        "weight":     0.15,
        "thresholds": ("<8%",    "≥10%",   "≥13%",   "≥16%"),
        "now":        "+16%",
        "score":      4,
        "comment":    "H1 revenue growth at the very top of, and ahead of, the 12-15% full-year guidance range",
    },
    {
        "name":       "Allegro Pay GMV penetration",
        "weight":     0.15,
        "thresholds": ("<8%",    "≥10%",   "≥13%",   "≥16%"),
        "now":        "15.5%",
        "score":      3,
        "comment":    "Loan originations +27.1% YoY — a genuine, scaling fintech monetization lever most marketplace peers lack",
    },
    {
        "name":       "Poland Marketplace GMV growth",
        "weight":     0.15,
        "thresholds": ("<5%",    "≥8%",    "≥11%",   "≥14%"),
        "now":        "+12%",
        "score":      3,
        "comment":    "Healthy growth in the core, profit-generating market despite real low-cost-platform competition",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.20,
        "thresholds": (">28x",   "≤24x",   "≤21x",   "≤17x"),
        "now":        "~20.3x",
        "score":      3,
        "comment":    "20.3× FY2026E EPS — a reasonable, not cheap, multiple for a marketplace beating its own growth guidance",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "International (Mall Group) growing 82.4% YoY is genuine, accelerating evidence the cross-border expansion thesis is working, not just a promise", +0.5, 0.20),
    ("-", "Temu, Shein, and AliExpress represent a real, well-funded competitive threat to Allegro's core Polish marketplace take rates", -0.5, 0.20),
    ("+", "Allegro Pay financing 15.5% of GMV with loan originations +27.1% YoY is a genuine fintech monetization lever most marketplace peers lack", +0.4, 0.15),
    ("+", "H1 2026 results running ahead of full-year guidance on GMV, revenue, AND EBITDA simultaneously is a real, quantified beat-and-raise signal", +0.4, 0.15),
    ("-", "At ~20.3x forward earnings, the stock already prices in continued strong execution across both Poland and International", -0.4, 0.15),
    ("-", "Poland's marketplace, while still the profit engine, faces genuine low-cost-platform price competition that could compress take rates over time", -0.3, 0.15),
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
CONS_EPS_2YR  = 2.60    # PLN; conservative FY2028E: modest growth off FY2026E, no re-acceleration credited
CONS_PE_2YR   = 18      # a modest de-rating from ~20.3× as growth normalizes toward guidance
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
print(f"  {TICKER}  ·  {COMPANY}  ·  {CURRENT_PRICE:.2f} zł  ·  Marketplace / Allegro Pay / International")
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
    print(f"  {seg:<44}  {curr:>11.1f}  {bear:>9.1f}  {bull:>9.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<44}  {curr_total:>11.1f}  {bear_total:>9.1f}  {bull_total:>9.1f}")
print(f"  H1 2026 actual: GMV +14%, revenue +16%, adj. EBITDA +17% YoY — all ahead of FY guidance")
print()

# EPS bridge (net-margin based)
shares    = SHARES_OUT_M / 1000
curr_net  = curr_total * NET_MARGIN_CURR
curr_eps  = round(curr_net / shares, 2)

bull_net  = bull_total * NET_MARGIN_BULL
bull_eps_imp = round(bull_net / shares, 2)

bear_net  = bear_total * NET_MARGIN_BEAR
bear_eps_imp = round(bear_net / shares, 2)

print(f"  FY2026E EPS check:  {curr_total:.1f}B zł rev × {NET_MARGIN_CURR*100:.2f}% net margin")
print(f"  ÷ {shares:.4f}B shares  =  {curr_eps:.2f} zł/share  (model estimate {EPS_FY2026E:.2f} zł  ✓)")
print()
print(f"  BULL EPS check:  {bull_total:.1f}B zł rev × {NET_MARGIN_BULL*100:.2f}% net margin")
print(f"  =  ~{bull_eps_imp:.2f} zł/share  →  × {SCENARIOS['BULL'][1]}× = ~{bull_eps_imp*SCENARIOS['BULL'][1]:.0f} zł  ✓ BULL {SCENARIOS['BULL'][2]} zł")
print()
print(f"  BEAR EPS check:  {bear_total:.1f}B zł rev × {NET_MARGIN_BEAR*100:.2f}% net margin (intensified price competition)")
print(f"  =  ~{bear_eps_imp:.2f} zł/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~{bear_eps_imp*SCENARIOS['BEAR'][1]:.0f} zł  ✓ BEAR {SCENARIOS['BEAR'][2]} zł")

# COMPETITIVE / FINTECH CHECK
print()
print(f"  COMPETITIVE / FINTECH CHECK  (the Allegro-specific angle):")
print(f"  Allegro Pay loans originated (qtr):    {ALLEGRO_PAY_LOANS_Q_B:.1f}B zł  (+27.1% YoY)")
print(f"  Allegro Pay GMV penetration:            {ALLEGRO_PAY_GMV_PENETRATION:.1f}%")
print(f"  International GMV growth:               +{INTERNATIONAL_GMV_GROWTH:.1f}% YoY")
print(f"  Poland GMV growth:                       +{POLAND_GMV_GROWTH:.1f}% YoY")
print(f"  H1 2026 vs full-year guidance:           {H1_METRICS_VS_GUIDE}")
print(f"  Structural competitive threat:           {LOW_COST_COMPETITORS}")
print()
print(f"  Allegro's bull case rests on two genuinely separate engines — a still-growing, still-profitable")
print(f"  Polish core, and an accelerating International segment now growing faster than the core ever did.")
print(f"  The bear case is equally real: {LOW_COST_COMPETITORS} have already reshaped price expectations across")
print(f"  European e-commerce, and Allegro's take-rate economics are not immune to that pressure long-term.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = 1.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every 1B zł revenue (at 9.05% margin):  +{eps_per_1B_rev:.4f} zł/EPS  = +{eps_per_1B_rev*20:.2f} zł/share at 20× P/E")
print(f"  Every 1pp of net margin:                 +{curr_total*0.01/shares:.4f} zł/EPS  = +{curr_total*0.01/shares*20:.2f} zł/share at 20× P/E")
print(f"  Every 1 turn of P/E:                     ±{EPS_FY2026E:.2f} zł/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (GMV growth / International / revenue / Allegro Pay / Poland / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<32}  {'BEAR':>7}  {'BASE':>7}  {'BULL':>7}  {'XBULL':>7}  {'NOW':>9}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<32}  {ths[0]:>7}  {ths[1]:>7}  {ths[2]:>7}  {ths[3]:>7}  {s['now']:>9}  {lbl}  {b}")
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
    ("Group GMV growth",            "+14.4%",  "<5%",     "Temu/Shein price war intensifies, pulling volume and take rate down simultaneously"),
    ("International GMV growth",    "+82.4%",  "<20%",    "Mall Group integration stalls or local competition in CZ/SK/HU/RO intensifies"),
    ("Total revenue growth",        "+16%",    "<8%",     "Take-rate compression outpaces GMV growth as pricing pressure bites"),
    ("Allegro Pay penetration",     "15.5%",   "<8%",     "Credit losses or regulatory tightening curtail fintech lending growth"),
    ("Poland GMV growth",           "+12%",    "<5%",     "The core market's growth genuinely stalls under sustained low-cost-platform pressure"),
    ("Forward P/E",                 "~20.3x",  ">28x",    "Market fully re-prices Allegro for a slower, margin-compressed growth trajectory"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the bear case isn't about Allegro's execution — H1 2026 beat its own guidance on every")
print(f"  headline metric — it's about whether Chinese low-cost platforms structurally compress European")
print(f"  marketplace take rates over the next two years regardless of how well Allegro itself executes.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS estimate:       {EPS_FY2026E:.2f} zł  (consensus-implied from the ~20.3x forward P/E)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (a genuine e-commerce-marketplace-trough multiple)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    {EPP:.0f} zł/share")
print(f"  Current {CURRENT_PRICE:.2f} zł vs EPP {EPP:.0f} zł:  {epp_gap_pct:+.1f}%")
print()
print(f"  At {CURRENT_PRICE:.2f} zł the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS, near its 52-week high, after")
print(f"  beating its own full-year guidance across GMV, revenue, and EBITDA in H1. The EPP floor reflects a")
print(f"  genuine competitive-pressure scenario, not a hypothetical one, given Temu/Shein's real market presence.")
print(f"  At a 18× reversion (a modest de-rating): {EPS_FY2026E:.2f} × 18 = {EPS_FY2026E*18:.0f} zł  ({(EPS_FY2026E*18/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest growth off FY2026E, no re-acceleration credited)")
hr()
print(f"  Conservative FY2028E EPS:  {CONS_EPS_2YR:.2f} zł  (~17% cumulative EPS growth — below the current beat-and-raise trajectory)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~20.3× → 18×; a modest de-rating)")
print(f"  Conservative equity value:   {cons_equity:.2f} zł/share")
print(f"  + Cumulative dividends (2yr): +{cons_divs:.2f} zł/share  (no dividend — cash reinvested in growth)")
hr()
print(f"  Conservative 2yr total:      {cons_total:.2f} zł  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from {CURRENT_PRICE:.2f} zł)")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: even a conservative case with meaningfully slower growth than H1 2026 demonstrated")
print(f"  still comes out {'positive' if cons_return > 0 else 'negative'}, because the starting multiple isn't extreme. The real risk is not a growth")
print(f"  slowdown per se, but a structural take-rate compression that this conservative case doesn't fully capture.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.33
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        {VOL_52W_LOW:.2f} – {VOL_52W_HIGH:.2f} zł  (stock at {vol_pct*100:.0f}th pct of 52W range, near the high)")
print(f"  Annual dividend:      0.00 zł/share  (no dividend; cash reinvested in International/Allegro Pay)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (moderate-high, typical for a growth-stage e-commerce platform)")
print(f"  Beta vs WIG20:        1.20  (above the Warsaw benchmark)")
print(f"  1-sigma range (1yr):  {sigma_range[0]:.0f} – {sigma_range[1]:.0f} zł  ({CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear {bear_price} zł requires:  ~{bear_sigmas:.1f}σ drawdown  (large, consistent with a genuine competitive-pressure scenario)")
print(f"  → Q3 2026 print (mid-November) is the next test of whether the H1 beat-and-raise trajectory continues.")
print(f"  → International GMV growth and Allegro Pay penetration trends are the leading indicators between prints.")
print(f"  → {signal_short} at {CURRENT_PRICE:.2f} zł  |  Add below 33 zł  |  Trim above 55 zł")

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
print(f"  Allegro is executing well above its own guidance across every headline metric — the open question")
print(f"  is how durable Polish marketplace economics are against a well-funded, structurally low-cost")
print(f"  competitive set that isn't going away.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q3 2026 print (mid-November) — does the beat-and-raise trajectory across GMV/revenue/EBITDA continue?")
print(f"  (2) International (Mall Group) GMV growth trend — the primary re-rating catalyst if it holds near +80%")
print(f"  (3) Allegro Pay loan originations and GMV penetration — the fintech monetization lever to watch")
print(f"  (4) Any pricing/promotional response to Temu/Shein/AliExpress competitive pressure in Poland")
print(f"  (5) Full-year guidance revisions — will management raise the 10-12%/12-15%/9-13% ranges given the H1 beat?")
print(f"  {signal_short} at {CURRENT_PRICE:.2f} zł  |  Add below 33 zł  |  Trim above 55 zł")
print(f"  EPP floor: {EPP:.0f} zł  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: {EPS_FY2026E:.2f} zł  |  Allegro Pay penetration: {ALLEGRO_PAY_GMV_PENETRATION:.1f}%")
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
