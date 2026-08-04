"""
ABBV  ·  AbbVie Inc.  ·  NYSE: ABBV
Bottom-up signal model  ·  Pharma / Immunology (Skyrizi/Rinvoq) / Humira Cliff / Aesthetics / Oncology
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "ABBV"
COMPANY       = "AbbVie Inc."
SECTOR        = "Pharmaceuticals · Immunology · Oncology · Neuroscience · Aesthetics · NYSE: ABBV"
CURRENT_PRICE = 245.10      # USD; close 2026-08-03, -2.33% on the day
VOL_52W_LOW   = 190.75      # 2025/26 trough
VOL_52W_HIGH  = 267.47      # 2026 peak
SHARES_OUT_M  = 1_826.0     # millions; ~$448.7B mkt cap / $245.71
ANNUAL_DIV    = 6.68        # $/share; Dividend King, ~2.7% yield

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ──────────────────────────────────────
# Q2 2026 actual: revenue $16.99B (+10.2% operational), adj EPS $3.65 (beat $3.61 est, $0.06 above
# guide midpoint). SKYRIZI $5.5B in the quarter (+24% operationally), full-year forecast raised to
# $21.7B; RINVOQ topped $2.5B (+23.7%). HUMIRA fell 36.1% YoY on continued biosimilar erosion. FY2026
# revenue guidance raised by $300M to ~$67.6B, but FY2026 adj EPS guidance was trimmed to $13.87-$14.07
# (from $13.91-$14.11) on ~$0.14 dilution from the pending Apogee Therapeutics acquisition, partly
# offset by $0.10 of operational overperformance.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Skyrizi + Rinvoq (Immunology growth engine)", 31.5, 25.0, 38.0, "Already beat AbbVie's own 2027 combined target; Skyrizi alone guided to $21.7B for FY2026"),
    ("Rest of portfolio (Humira + Oncology/Neuro/Aesthetics)", 36.1, 30.0, 42.0, "Humira continues its biosimilar-driven decline (-36.1% YoY); the rest is a diversification cushion"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.820   # FY2026E blended gross margin
GROSS_MARGIN_BEAR = 0.780   # BEAR: Humira cliff accelerates and mix shifts toward lower-margin products
GROSS_MARGIN_BULL = 0.835   # BULL: Skyrizi/Rinvoq mix shift lifts the blend further
OPEX_FIXED_B      = 25.77   # R&D + SG&A + intangible amortization ($B) — largely sticky given AbbVie's M&A-heavy intangible base
TAX_RATE          = 0.140   # effective tax rate (AbbVie's is structurally low)

# ── SKYRIZI/RINVOQ VS HUMIRA CLIFF CALCULATOR (the AbbVie-specific angle) ────
SKYRIZI_Q2_REV_B          = 5.5   # $B; Skyrizi quarterly revenue, +24% operationally
SKYRIZI_FY26_GUIDE_B      = 21.7  # $B; Skyrizi full-year 2026 revenue guide (raised)
RINVOQ_Q2_REV_B           = 2.5   # $B; Rinvoq quarterly revenue, +23.7% YoY
HUMIRA_YOY_DECLINE_PCT    = 36.1  # % YoY decline, Humira, on continued biosimilar erosion
APOGEE_EPS_DILUTION       = 0.14  # $/share; 2026 EPS dilution from the pending Apogee Therapeutics acquisition
APOGEE_OFFSET_OVERPERFORM = 0.10  # $/share; operational overperformance partly offsetting the Apogee dilution
FY26_REVENUE_GUIDE_RAISE_M = 300  # $M; FY2026 revenue guidance raise (to ~$67.6B)

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 13.97       # $/share FY2026E adj; guide midpoint ($13.87-$14.07)
PE_PESSIMISTIC = 13.0        # trough P/E: a genuine big-pharma-trough multiple
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 7.82, 13,  102, "Humira's decline accelerates further, Skyrizi/Rinvoq growth decelerates, and Apogee dilution compounds with pipeline disappointment"),
    "BASE":  (15.62, 17.5, 273, "Skyrizi/Rinvoq keep compounding roughly as guided while Humira's decline gradually moderates"),
    "BULL":  (19.17, 18,  345, "Skyrizi/Rinvoq growth reaccelerates on new indications; Humira's drag becomes immaterial to the growth algorithm"),
    "XBULL": (23.90, 20,  478, "Immunology franchise becomes AbbVie's dominant growth engine; pipeline (emraclidine, new indications) delivers multiple wins"),
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
        "name":       "Skyrizi + Rinvoq combined growth",
        "weight":     0.25,
        "thresholds": ("<10%",   "≥16%",   "≥20%",   "≥24%"),
        "now":        "+24%/+23.7%",
        "score":      4,
        "comment":    "Both franchises growing near or above +24% operationally — already ahead of AbbVie's own 2027 targets",
    },
    {
        "name":       "Humira decline rate",
        "weight":     0.15,
        "thresholds": (">45%",   "≤40%",   "≤30%",   "≤20%"),
        "now":        "-36.1%",
        "score":      2,
        "comment":    "A steep but expected decline as biosimilar competition matures — the cliff is largely known, not a surprise",
    },
    {
        "name":       "Total revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<5%",    "≥8%",    "≥11%",   "≥14%"),
        "now":        "+10.2%",
        "score":      3,
        "comment":    "Double-digit operational growth even while absorbing the Humira decline — a genuine sign the cliff is being outgrown",
    },
    {
        "name":       "Adj EPS beat magnitude",
        "weight":     0.15,
        "thresholds": ("miss",   "in-line", "beat",  "large beat"),
        "now":        "+1.2% beat",
        "score":      2,
        "comment":    "A modest beat, and full-year EPS guidance was trimmed (not raised) on Apogee dilution — a mixed quarter, not a clean win",
    },
    {
        "name":       "FY2026 revenue guidance direction",
        "weight":     0.15,
        "thresholds": ("cut",    "held",    "raised", "sharply raised"),
        "now":        "raised",
        "score":      3,
        "comment":    "Revenue guidance raised by $300M to ~$67.6B, the second raise this year — the top-line story remains intact",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.10,
        "thresholds": (">22x",   "≤19x",   "≤16x",   "≤13x"),
        "now":        "~17.5x",
        "score":      3,
        "comment":    "17.5× FY2026E adj EPS — a reasonable, not demanding, multiple for a double-digit revenue grower",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Skyrizi and Rinvoq have already exceeded AbbVie's own 2027 combined revenue target a year early — genuine, proven execution", +0.6, 0.25),
    ("-", "Humira's -36.1% decline is a real, ongoing drag that must keep being outgrown, not just absorbed once", -0.3, 0.15),
    ("-", "The EPS guidance trim on Apogee dilution shows M&A can still create near-term earnings friction even amid strong top-line growth", -0.3, 0.15),
    ("+", "Emraclidine (schizophrenia) Phase III readout in 2026 is a real, underappreciated binary catalyst beyond the known immunology story", +0.4, 0.15),
    ("+", "Dividend King status (50+ years of increases) with a ~2.7% yield provides a real floor most growth pharma names lack", +0.3, 0.15),
    ("-", "At 17.5× forward earnings the stock isn't statistically cheap despite the -2.3% daily move; a genuine pipeline disappointment would hurt", -0.3, 0.15),
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
CONS_EPS_2YR  = 15.20   # conservative FY2028E: modest growth off FY2026E guide midpoint
CONS_PE_2YR   = 15      # a modest de-rating from ~17.5×
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Skyrizi/Rinvoq / Humira Cliff / Aesthetics / Oncology")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<46}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<46}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<46}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}")
print(f"  Q2 2026 actual: $16.99B (+10.2% operational). FY2026 guide raised by ${FY26_REVENUE_GUIDE_RAISE_M}M to ~$67.6B")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_eps  = round(curr_oi * (1 - TAX_RATE) / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B * 1.06
shares_b  = shares * 0.97
bull_eps_imp = round(bull_oi * (1 - TAX_RATE) / shares_b, 2)

bear_gp   = bear_total * GROSS_MARGIN_BEAR
bear_oi   = bear_gp - OPEX_FIXED_B * 1.02
bear_eps_imp = round(max(0, bear_oi) * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.2f}B opex")
print(f"  − {TAX_RATE*100:.1f}% tax  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − opex, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_BEAR*100:.1f}% GM (accelerated Humira decline + Apogee drag) − opex")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# SKYRIZI/RINVOQ VS HUMIRA CLIFF CHECK
print()
print(f"  SKYRIZI/RINVOQ VS HUMIRA CLIFF CHECK  (the AbbVie-specific angle):")
print(f"  Skyrizi (Q2 quarterly / FY26 guide):    ${SKYRIZI_Q2_REV_B}B / ${SKYRIZI_FY26_GUIDE_B}B  (guide raised)")
print(f"  Rinvoq (Q2 quarterly):                  ${RINVOQ_Q2_REV_B}B+  (+23.7% YoY)")
print(f"  Humira YoY decline:                     -{HUMIRA_YOY_DECLINE_PCT:.1f}%")
print(f"  Apogee acquisition EPS dilution:         -${APOGEE_EPS_DILUTION:.2f}/share  (offset +${APOGEE_OFFSET_OVERPERFORM:.2f} by overperformance)")
print()
print(f"  This is the clearest 'outgrowing the cliff' story in big pharma: Skyrizi and Rinvoq combined already")
print(f"  exceed AbbVie's own 2027 target a year early, and the company keeps raising revenue guidance even")
print(f"  while absorbing a -36% Humira decline. The EPS guidance trim is real but narrow — a single M&A")
print(f"  dilution item, not a sign the core growth engines are underperforming.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_gm  = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 82.0% GM):      +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*17:.2f}/share at 17× P/E")
print(f"  Every 1pp of gross margin:            +${eps_per_1pp_gm:.3f}/EPS  = +${eps_per_1pp_gm*17:.2f}/share at 17× P/E")
print(f"  Every 1 turn of P/E:                  ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Skyrizi/Rinvoq growth / Humira decline / revenue / EPS beat / guidance / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<40}  {'BEAR':>7}  {'BASE':>7}  {'BULL':>7}  {'XBULL':>9}  {'NOW':>13}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<40}  {ths[0]:>7}  {ths[1]:>7}  {ths[2]:>7}  {ths[3]:>9}  {s['now']:>13}  {lbl}  {b}")
    print(f"    {s['comment']}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15%/yr hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:88]:<88}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<32}  {'Current':>10}  {'Bear val':>10}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Skyrizi+Rinvoq growth",       "+24%",   "<10%",    "-14pp+", "New indication launches disappoint or competitive immunology entrants gain real share"),
    ("Humira decline rate",         "-36.1%", ">45%",    "worse",  "Biosimilar erosion accelerates further, faster than the growth engines can offset"),
    ("Total revenue YoY",           "+10.2%", "<5%",     "-5pp+",  "The Humira drag finally outpaces Skyrizi/Rinvoq growth on a consolidated basis"),
    ("Adj EPS beat magnitude",      "+1.2%",  "miss",    "reversal","A beat-and-raise streak breaks; further M&A dilution compounds without offsetting overperformance"),
    ("FY2026 guidance direction",   "raised", "cut",     "reversal","Management is forced to cut revenue guidance at a future quarter"),
    ("Forward P/E",                 "~17.5x", ">22x",    "re-rate","Market fully re-prices AbbVie for a slower, Humira-cliff-dominated growth trajectory"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the bear case requires Skyrizi/Rinvoq's currently exceptional growth (+24%/+23.7%) to")
print(f"  decelerate sharply at the exact moment Humira's decline is still running at -36% — a genuine")
print(f"  crossover risk, but one the data doesn't yet show any sign of. Emraclidine's 2026 Phase III readout")
print(f"  is the specific binary catalyst that could either reinforce or undercut the bull case independently.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS estimate:       ${EPS_FY2026E:.2f}  (guide midpoint, $13.87-$14.07)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (a genuine big-pharma-trough multiple)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS — a reasonable multiple for a")
print(f"  double-digit revenue grower with a proven, ahead-of-target immunology franchise.")
print(f"  At a 15× reversion (a modest premium to trough): ${EPS_FY2026E:.2f} × 15 = ${EPS_FY2026E*15:.0f}  ({(EPS_FY2026E*15/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest growth off FY2026E guide midpoint)")
hr()
print(f"  Conservative FY2028E EPS:  ${CONS_EPS_2YR:.2f}  (~8.8% cumulative EPS growth — below the current trajectory)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~17.5× → 15×; a modest de-rating)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: a conservative case with muted EPS growth and a modest de-rating comes out roughly")
print(f"  flat, propped up almost entirely by the ~2.7% dividend yield. The case for owning ABBV here rests on")
print(f"  Skyrizi/Rinvoq's growth staying exceptional, not on a statistically cheap starting multiple.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.24
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Recent move:           -2.33% today, digesting the Q2 print's EPS-guidance trim")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; Dividend King, 50+ years of increases)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (moderate — lower than most growth pharma names)")
print(f"  Beta vs S&P 500:      0.75  (defensive, below-market)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (large, consistent with a genuine crossover-risk scenario)")
print(f"  → Q3 2026 print (late October) is the next test of whether Skyrizi/Rinvoq growth holds near +24%.")
print(f"  → Emraclidine's 2026 Phase III schizophrenia readout is the key independent binary catalyst to watch.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $205  |  Trim above $310")

# ─── ⑦ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print()
print("  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
hr()
probs_mkt = softmax_probs(MARKET_COMPOSITE)
print(f"  {'Scenario':<10}  {'Price':>7}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>7}  Description")
hr()
for s in ["BEAR","BASE","BULL","XBULL"]:
    pp  = probs_proxy[s] * 100
    pm  = probs_mkt[s]   * 100
    gap = pp - pm
    pr  = SCENARIOS[s][2]
    desc = SCENARIOS[s][3][:46]
    print(f"  {s:<10}  ${pr:>6}  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): ${ev_adj:.0f}  /  Proxy EV: ${ev_prx:.0f}  /  Market EV: ${ev_mkt:.0f}  /  Current: ${CURRENT_PRICE:.0f}")
hr()
print(f"  Downside  (→ Bear ${bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull ${bull_price}):  {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b_str}")
print(f"  Signal    :  {signal_full}")
print()
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f} the market composite is {MARKET_COMPOSITE:.2f}/4.0. The model's")
print(f"  adjusted composite is {ADJ_COMPOSITE:.2f}/4.0, for a gap of {ADJ_GAP:+.2f} — {valuation_label.lower()}.")
print(f"  AbbVie's immunology franchise is executing at an exceptional level and has already beaten its own")
print(f"  multi-year targets — the stock's modest pullback reflects a narrow M&A-dilution item, not a crack")
print(f"  in the core growth story.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q3 2026 print (late October) — does Skyrizi/Rinvoq combined growth hold near +24%?")
print(f"  (2) Emraclidine (schizophrenia) Phase III readout — the key independent binary catalyst in 2026")
print(f"  (3) Apogee Therapeutics acquisition close and integration — confirm the dilution stays contained")
print(f"  (4) Humira decline rate — watch for any acceleration beyond the current -36% pace")
print(f"  (5) New Rinvoq indications (vitiligo, alopecia areata) ramp toward their ~$2B combined peak-sales target")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $205  |  Trim above $310")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  Skyrizi FY26 guide: ${SKYRIZI_FY26_GUIDE_B}B")
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
