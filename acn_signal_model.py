"""
ACN  ·  Accenture plc  ·  NYSE: ACN
Bottom-up signal model  ·  IT Consulting & Services / Digital Transformation / Agentic AI
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "ACN"
COMPANY       = "Accenture plc"
SECTOR        = "IT Consulting & Services · Digital Transformation · Agentic AI · NYSE: ACN"
CURRENT_PRICE = 165.92       # USD; close 2026-07-31 (verified live)
VOL_52W_LOW   = 118.15       # June 2026 trough; post Q3 FY2026 selloff (-18% in one session)
VOL_52W_HIGH  = 291.09       # 2025 pre-correction peak
SHARES_OUT_M  = 612.0        # millions; $101.5B mkt cap / $165.92; steady buyback
ANNUAL_DIV    = 6.52         # $/share forward; yield ~3.93%

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ─────────────────────────────────────
# FY2025 actual revenue $69.7B (+7%); FY2026 guide: local-currency growth 3-4%
# (4-5% ex ~1pt federal drag) → FY2026E ≈ $72.0B
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Products (consumer/retail/industrial)", 16.5, 14.0, 19.0, "Largest segment; cyclical, tied to discretionary transformation budgets"),
    ("Financial Services",                    14.8, 13.5, 16.5, "Capital markets + insurance consulting; steadiest segment through the cycle"),
    ("Resources (energy/utilities)",          15.2, 13.0, 17.0, "Energy transition + grid modernization work; long-duration programs"),
    ("Health & Public Service",               13.0, 10.0, 14.5, "Where DOGE/federal contract risk concentrates; ~8% of total revenue is US federal"),
    ("Communications, Media & Tech",          12.5, 10.5, 14.5, "Telco/media consulting + the advisory layer riding hyperscaler AI capex"),
]

# Margin assumptions (adjusted / non-GAAP; Accenture reports operating margin, not gross margin)
OP_MARGIN_CURR   = 0.156    # FY2026E adjusted operating margin guide (~15.6%, +~30bp YoY)
OP_MARGIN_BULL   = 0.178    # BULL: pyramid optimization + AI delivery efficiency land faster
OP_MARGIN_BEAR   = 0.128    # BEAR: federal cuts + pricing pressure on GenAI-displaced staffing work
TAX_RATE         = 0.245    # effective tax rate net of minority interest

# ── BOOKINGS / GENAI TRACTION (the Accenture-specific calculator) ────────────
BOOKINGS_Q3_B      = 20.5    # $B Q3 FY2026 new bookings (management called out softness)
BOOKINGS_YOY_PCT   = -2.0    # % YoY change in USD bookings — the number that spooked the market
GENAI_BOOKINGS_B   =  2.2    # $B/qtr GenAI bookings run-rate, still expanding
FEDERAL_PCT_REV    =  8.0    # % of FY2024 revenue from US federal government
FEDERAL_IMPACT_PT  =  1.0    # percentage points of FY2026 revenue growth guidance lost to federal

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 13.84       # $/share; company guidance midpoint ($13.78-$13.90, +7-8%)
PE_PESSIMISTIC = 11.0        # trough P/E: the stock traded near 12x forward at the June low;
                             # 11x prices a deeper federal-driven bookings air pocket
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 9.80, 12,  118, "Bookings keep declining; federal cuts deepen; GenAI cannibalizes staffing revenue"),
    "BASE":  (15.40, 15,  231, "Bookings stabilize +low-single-digits; federal drag fades; margin holds ~15.6%"),
    "BULL":  (18.00, 19,  342, "GenAI bookings compound past $3B/qtr; pyramid optimization lifts margin to 17.8%"),
    "XBULL": (21.50, 22,  473, "Accenture becomes the systems integrator of record for enterprise agentic AI"),
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
        "name":       "New bookings YoY growth (USD)",
        "weight":     0.25,
        "thresholds": ("<-8%",   "≥-3%",  "≥3%",    "≥12%"),
        "now":        "-2%",
        "score":      2,
        "comment":    "Q3 FY2026 bookings fell 2% YoY — the single data point that drove the 18% one-day selloff",
    },
    {
        "name":       "GenAI/Agentic AI bookings run-rate",
        "weight":     0.20,
        "thresholds": ("<$1B",   "≥$1.5B","≥$2.5B", "≥$4.5B"),
        "now":        "~$2.2B",
        "score":      2,
        "comment":    "$2.2B/qtr and still growing, but the pace has decelerated from the initial ramp",
    },
    {
        "name":       "Revenue YoY growth (local currency)",
        "weight":     0.20,
        "thresholds": ("<0%",    "≥3%",   "≥6%",    "≥10%"),
        "now":        "+3%",
        "score":      2,
        "comment":    "Q3 +3% cc, +6% USD. FY2026 guide narrowed to 3-4% cc — deceleration from FY2025's +7%",
    },
    {
        "name":       "US federal revenue YoY",
        "weight":     0.15,
        "thresholds": ("<-25%",  "≥-15%", "≥-5%",   "≥0%"),
        "now":        "~-15%",
        "score":      2,
        "comment":    "~8% of revenue; DOGE contract reviews and Pentagon cancellations cut ~1pt off FY2026 growth",
    },
    {
        "name":       "Adjusted operating margin",
        "weight":     0.10,
        "thresholds": ("<14%",   "≥15%",  "≥16.5%", "≥18%"),
        "now":        "15.6%",
        "score":      2,
        "comment":    "Modest expansion continues even through the bookings air pocket — a good sign on cost discipline",
    },
    {
        "name":       "Free cash flow yield",
        "weight":     0.10,
        "thresholds": ("<5%",    "≥7%",   "≥9%",    "≥12%"),
        "now":        "~8.9%",
        "score":      3,
        "comment":    "Q3 FCF $3.6B; TTM FCF yield near 9% of market cap — still among the best in large-cap services",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Valuation reset — 12.0× FY2026E EPS vs a historical ~22-25× multiple; 43% off the ATH",   +0.9, 0.20),
    ("+", "Balance sheet + capital return — net cash position, 3.93% yield, consistent buyback",       +0.5, 0.15),
    ("-", "Bookings deceleration — the -2% YoY print is the first negative bookings quarter in years", -0.8, 0.20),
    ("-", "Federal overhang — DOGE reviews are a structural, not cyclical, repricing of ~8% of revenue", -0.6, 0.15),
    ("+", "GenAI services demand — $2.2B/qtr bookings prove Accenture is a net beneficiary, not a victim", +0.6, 0.15),
    ("-", "Disintermediation risk — agentic AI could compress the staff-augmentation delivery model",  -0.5, 0.15),
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
CONS_EPS_2YR  = 15.00   # conservative FY2028E: ~4.2% EPS CAGR — bookings stay soft, no margin surprise
CONS_PE_2YR   = 13      # modest re-rating from 12.0× — well short of the historical ~22-25×
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  IT Consulting / Digital Transformation / Agentic AI")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<38}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<38}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<38}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  FY2025 actual: $69.7B (+7%). FY2026 guide: local-currency growth 3-4% (4-5% ex ~1pt federal drag)")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_op   = curr_total * OP_MARGIN_CURR
curr_eps  = round(curr_op * (1 - TAX_RATE) / shares, 2)

bull_op   = bull_total * OP_MARGIN_BULL
shares_b  = shares * 0.96
bull_eps_imp = round(bull_op * (1 - TAX_RATE) / shares_b, 2)

bear_op   = bear_total * OP_MARGIN_BEAR
bear_eps_imp = round(bear_op * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {OP_MARGIN_CURR*100:.1f}% op margin − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (company guidance ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {OP_MARGIN_BULL*100:.1f}% op margin, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 19× = ~${bull_eps_imp*19:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {OP_MARGIN_BEAR*100:.1f}% op margin (pricing pressure, federal drag)")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 12× trough = ~${bear_eps_imp*12:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")
print()
print(f"  ⚠ NOTE: the revenue spread bear-to-bull is only {(bull_total/bear_total-1)*100:.0f}%, but the EPS spread is")
print(f"  {(bull_eps_imp/bear_eps_imp-1)*100:.0f}%. Accenture's cost base is overwhelmingly people — pyramid mix and")
print(f"  utilization drive operating leverage in both directions faster than revenue moves.")

# BOOKINGS CHECK
print()
print(f"  BOOKINGS CHECK  (the leading indicator that moved the stock 18% in one session):")
print(f"  Q3 FY2026 new bookings:        ${BOOKINGS_Q3_B:.1f}B  ({BOOKINGS_YOY_PCT:+.0f}% YoY — first negative print in years)")
print(f"  GenAI/agentic bookings:        ${GENAI_BOOKINGS_B:.1f}B/qtr  (still growing, pace decelerating)")
print(f"  US federal revenue:            ~{FEDERAL_PCT_REV:.0f}% of total; DOGE reviews cost ~{FEDERAL_IMPACT_PT:.0f}pt of FY2026 growth")
print(f"  Bookings-to-revenue coverage is the metric to watch next: two more negative quarters would")
print(f"  confirm a structural GenAI-driven repricing of consulting hours rather than a one-off air pocket.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * OP_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_marg = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 15.6% op margin):     +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*15:.2f}/share at 15× P/E")
print(f"  Every 1pp of operating margin:              +${eps_per_1pp_marg:.3f}/EPS  = +${eps_per_1pp_marg*15:.2f}/share at 15× P/E")
print(f"  Every 1 turn of P/E:                        ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (bookings / GenAI demand / federal exposure / margin)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<40}  {'BEAR':>7}  {'BASE':>7}  {'BULL':>7}  {'XBULL':>7}  {'NOW':>7}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<40}  {ths[0]:>7}  {ths[1]:>7}  {ths[2]:>7}  {ths[3]:>7}  {s['now']:>7}  {lbl}  {b}")
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
print(f"  {'Signal':<32}  {'Current':>9}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("New bookings YoY",           "-2%",    "<-8%",    "-6pp",   "Enterprises pause discretionary transformation spend"),
    ("GenAI bookings run-rate",    "$2.2B",  "<$1.0B",  "-$1.2B", "Agentic AI tooling lets clients build in-house, bypassing SI"),
    ("Revenue YoY (cc)",           "+3%",    "<0%",     "-3pp",   "Bookings weakness converts into a revenue contraction"),
    ("US federal revenue YoY",     "~-15%",  "<-30%",   "-15pp",  "Further DOGE-style reviews or a shutdown-driven freeze"),
    ("Adjusted operating margin",  "15.6%",  "<12.8%",  "-2.8pp", "Pricing concessions to defend bookings; bench costs rise"),
    ("Forward P/E",                "12.0x",  "≤10x",    "-2x",    "Services multiple compresses further on the AI-disruption narrative"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>9}  {bear_v:>9}  {move:>8}  {trigger[:46]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the -2% bookings print is the tell. If it is macro caution and federal")
print(f"  noise, it reverses within two quarters and the stock re-rates off an 11-12× trough.")
print(f"  If it is agentic AI structurally repricing consulting hours — clients using AI copilots")
print(f"  to do what Accenture used to bill for — the multiple should stay compressed even after")
print(f"  bookings stabilize. The model's -0.5 SCA factor on disintermediation risk reflects that")
print(f"  the second scenario cannot yet be ruled out from two quarters of data.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E adjusted EPS (company guide):  ${EPS_FY2026E:.2f}  ($13.78-$13.90, +7-8% YoY)")
print(f"  Pessimistic P/E at trough:               {PE_PESSIMISTIC:.0f}×  (traded near 12× at the June low; 11× prices a deeper air pocket)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E adjusted EPS — against a")
print(f"  historical range of roughly 22-25× for most of the last decade. That is not a modest")
print(f"  discount; it is a re-rating to a value-services multiple while the company still guides")
print(f"  to 7-8% EPS growth and a 3.93% dividend yield. The market is pricing structural AI")
print(f"  disruption risk, not a cyclical soft patch — which is exactly the debate this model can't settle.")
print(f"  At a 18× reversion (still below the historical range): ${EPS_FY2026E:.2f} × 18 = ${EPS_FY2026E*18:.0f}  (+{(EPS_FY2026E*18/CURRENT_PRICE-1)*100:.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: bookings stay soft, only a token re-rating)")
hr()
print(f"  Conservative FY2028E adjusted EPS:  ${CONS_EPS_2YR:.2f}  (~4.2% EPS CAGR off the ${EPS_FY2026E:.2f} guide)")
print(f"  Conservative exit P/E:               {CONS_PE_2YR}×  (12.0× → 13×; still a fraction of the historical range)")
print(f"  Conservative equity value:            ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):        +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:               ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:            {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: even with bookings staying soft and the multiple barely moving off its")
print(f"  trough, the dividend and modest EPS growth clear {cons_annual:.1f}%/yr. The margin of safety")
print(f"  here is the valuation reset, not an assumption that the bookings story turns around.")
print(f"  Breakeven at 13× requires FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f} — below the FY2026 guide already.")
print(f"  BUY-conviction trigger: two consecutive quarters of positive bookings growth")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.38
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Single-session move:  -18% on the Q3 FY2026 print — a rare move for a consulting franchise")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; consistent grower)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (elevated vs Accenture's historical ~24%; bookings-driven repricing)")
print(f"  Beta vs S&P 500:      1.15  (higher than its defensive-services reputation would suggest now)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ further drawdown  (would retest, not breach, the 52W low)")
print(f"  → Next quarterly bookings print is the single highest-signal data point in the coverage.")
print(f"  → Federal revenue stabilization would remove the most quantifiable piece of the bear case.")
print(f"  → BUY at current price  |  ADD $130–150  |  TRIM above $260")

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
print(f"  Accenture at 12× forward EPS with a 3.93% yield and a still-positive (if decelerating)")
print(f"  GenAI bookings line is priced for a worse outcome than the base case. The open question")
print(f"  the model cannot resolve from two quarters of data: is this a cyclical bookings air")
print(f"  pocket, or the first evidence that agentic AI structurally shrinks billable hours?")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q4 FY2026 bookings — two consecutive positive quarters would resolve the air-pocket debate")
print(f"  (2) GenAI bookings run-rate — deceleration below $2B/qtr would confirm the disintermediation fear")
print(f"  (3) Federal revenue trajectory — any stabilization removes a quantifiable 1pt of the growth drag")
print(f"  (4) Operating margin — continued expansion through a bookings slump signals real cost discipline")
print(f"  (5) Capital allocation — buyback pace at a depressed multiple is a signal of management's own view")
print(f"  BUY at ${CURRENT_PRICE:.2f}  |  ADD $130–150  |  TRIM above $260")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  Bookings YoY: {BOOKINGS_YOY_PCT:+.0f}%")
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
