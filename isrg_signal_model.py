"""
ISRG  ·  Intuitive Surgical, Inc.  ·  NASDAQ: ISRG
Bottom-up signal model  ·  Surgical Robotics / da Vinci & Ion Platforms / Recurring Instruments
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "ISRG"
COMPANY       = "Intuitive Surgical, Inc."
SECTOR        = "Surgical Robotics · da Vinci & Ion Platforms · Recurring Instruments · NASDAQ: ISRG"
CURRENT_PRICE = 375.41      # USD; close 2026-08-03, +6.25% on the day, still down ~38% from the 52-week high
VOL_52W_LOW   = 328.57      # post-earnings-correction trough
VOL_52W_HIGH  = 603.88      # 2026 pre-correction peak
SHARES_OUT_M  = 354.2       # millions
ANNUAL_DIV    = 0.0         # no dividend; ISRG reinvests entirely in growth/R&D

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ──────────────────────────────────────
# Q2 2026 actual: revenue $2.89B (+19% YoY), non-GAAP EPS $2.80 (beat $2.51 est), non-GAAP gross
# margin 70.0%. 468 da Vinci + 55 Ion systems placed; installed base 11,710 da Vinci (+12%) and
# 1,096 Ion (+21%). Recurring revenue (instruments/accessories/service) $2.47B (+19%), 85% of total.
# FY2026 da Vinci procedure growth guide held at 13.5-15.5%, expected near midpoint — but Q2 procedure
# growth slowed to 12% (from 14% in Q1) on ACA subsidy changes, deferred procedures, and bariatric
# pressure; China remains challenged. The stock fell ~12% on the print and is down ~38% from its high.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Recurring (Instruments/Accessories/Service)", 9.86, 8.60, 11.80, "85% of revenue and growing with the procedure base — the resilient core of the model"),
    ("Systems (da Vinci/Ion capital placements)",    1.74, 1.30,  2.30, "The volatile, capital-cycle-sensitive 15% — first to slow when hospital capex tightens"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.700   # FY2026E; matches Q2 non-GAAP gross margin exactly
GROSS_MARGIN_BEAR = 0.660   # BEAR: pricing/mix pressure as procedure growth decelerates further and China worsens
GROSS_MARGIN_BULL = 0.715   # BULL: recurring-revenue mix shift and scale efficiencies lift the blend
OPEX_FIXED_B      = 3.45    # R&D + SG&A ($B); ISRG invests heavily and doesn't cut opex countercyclically
TAX_RATE          = 0.210   # effective tax rate

# ── PROCEDURE GROWTH DECELERATION CALCULATOR (the ISRG-specific angle) ───────
Q1_2026_PROCEDURE_GROWTH_PCT = 14.0   # % YoY, Q1 2026 da Vinci procedure growth
Q2_2026_PROCEDURE_GROWTH_PCT = 12.0   # % YoY, Q2 2026 da Vinci procedure growth — the deceleration that triggered the selloff
FY26_GUIDE_LOW_PCT           = 13.5   # % FY2026 procedure growth guide, low end (held unchanged)
FY26_GUIDE_HIGH_PCT          = 15.5   # % FY2026 procedure growth guide, high end (held unchanged)
INSTALLED_BASE_DAVINCI       = 11_710 # da Vinci systems installed, +12% YoY
INSTALLED_BASE_ION           = 1_096  # Ion systems installed, +21% YoY
POST_EARNINGS_DROP_PCT       = 11.6   # % single-day drop after the Q2 print (after-hours)

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 10.41       # $/share FY2026E non-GAAP; current analyst consensus
PE_PESSIMISTIC = 25.0        # trough P/E: even in downturns, ISRG's monopoly-like franchise rarely trades cheap
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 6.73, 27,  182, "Procedure growth decelerates further toward high-single-digits; China stays weak; multiple compresses hard"),
    "BASE":  (11.47, 34,  390, "Procedure growth settles near the low end of guidance; steady installed-base compounding continues"),
    "BULL":  (14.32, 32,  458, "Procedure growth reaccelerates back toward the guide midpoint as ACA/bariatric headwinds prove transitory"),
    "XBULL": (18.81, 36,  677, "The da Vinci 5 platform and Ion drive a renewed multi-year procedure and systems upgrade cycle"),
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
        "name":       "da Vinci procedure growth (YoY)",
        "weight":     0.25,
        "thresholds": ("<8%",    "≥11%",   "≥14%",   "≥17%"),
        "now":        "12%",
        "score":      2,
        "comment":    "Decelerated from 14% in Q1 to 12% in Q2 — the specific data point that triggered the selloff",
    },
    {
        "name":       "Revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<10%",   "≥14%",   "≥18%",   "≥22%"),
        "now":        "+19%",
        "score":      3,
        "comment":    "Still a strong beat-and-grow quarter even as the procedure-growth narrative dominated the reaction",
    },
    {
        "name":       "Installed base growth (da Vinci)",
        "weight":     0.15,
        "thresholds": ("<6%",    "≥9%",    "≥12%",   "≥15%"),
        "now":        "+12%",
        "score":      3,
        "comment":    "11,710 da Vinci systems installed, +12% YoY — the annuity-like base keeps compounding regardless of quarterly procedure noise",
    },
    {
        "name":       "Recurring revenue mix",
        "weight":     0.15,
        "thresholds": ("<75%",   "≥80%",   "≥83%",   "≥86%"),
        "now":        "85%",
        "score":      3,
        "comment":    "85% recurring revenue — instruments/accessories/service scale with the growing procedure base, not new system sales",
    },
    {
        "name":       "FY2026 guidance stance",
        "weight":     0.15,
        "thresholds": ("cut",    "trimmed", "held",   "raised"),
        "now":        "held",
        "score":      3,
        "comment":    "Management held the 13.5-15.5% full-year procedure growth guide unchanged despite the Q2 deceleration",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.10,
        "thresholds": (">55x",   "≤45x",   "≤38x",   "≤30x"),
        "now":        "~36.1x",
        "score":      3,
        "comment":    "36.1× FY2026E EPS — still a premium, but meaningfully de-rated from the ~58× multiple at the 52-week high",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Near-monopoly market position in surgical robotics with a genuine installed-base moat — switching costs are real and high", +0.6, 0.20),
    ("-", "ACA subsidy changes, deferred procedures, and bariatric pressure are real, not manufactured — the deceleration is a genuine data point", -0.5, 0.20),
    ("-", "China remains structurally challenged (tender delays, local competition) with no clear near-term resolution", -0.3, 0.15),
    ("+", "85% recurring revenue means even a systems-placement slowdown doesn't collapse the P&L the way it would for a pure capital-equipment name", +0.5, 0.20),
    ("-", "At 36.1× forward earnings even after a 38% correction, the stock still isn't statistically cheap by any conventional measure", -0.4, 0.15),
    ("+", "Management held full-year guidance unchanged rather than trimming it — a real signal of confidence, not just optics", +0.3, 0.10),
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
CONS_EPS_2YR  = 12.20   # conservative FY2028E: modest growth off FY2026E, procedure growth stays near the low end of guidance
CONS_PE_2YR   = 28      # a real de-rating from ~36.1× as the growth-rate debate persists
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  da Vinci / Ion / Recurring Instruments")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<44}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<44}  ${curr:>11.2f}  ${bear:>8.2f}  ${bull:>8.2f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<44}  ${curr_total:>11.2f}  ${bear_total:>8.2f}  ${bull_total:>8.2f}")
print(f"  Q2 2026 actual: $2.89B (+19% YoY). Recurring $2.47B (85% of total, +19%). Systems: 468 da Vinci + 55 Ion placed")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_eps  = round(curr_oi * (1 - TAX_RATE) / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B * 1.08
shares_b  = shares * 0.99
bull_eps_imp = round(bull_oi * (1 - TAX_RATE) / shares_b, 2)

bear_gp   = bear_total * GROSS_MARGIN_BEAR
bear_oi   = bear_gp - OPEX_FIXED_B * 1.02
bear_eps_imp = round(max(0, bear_oi) * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.2f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.2f}B opex")
print(f"  − {TAX_RATE*100:.1f}% tax  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − opex")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B rev × {GROSS_MARGIN_BEAR*100:.1f}% GM (deceleration + China + mix pressure) − opex")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# PROCEDURE GROWTH DECELERATION CHECK
print()
print(f"  PROCEDURE GROWTH DECELERATION CHECK  (the ISRG-specific angle):")
print(f"  Q1 2026 procedure growth:              +{Q1_2026_PROCEDURE_GROWTH_PCT:.1f}% YoY")
print(f"  Q2 2026 procedure growth:               +{Q2_2026_PROCEDURE_GROWTH_PCT:.1f}% YoY  (the deceleration)")
print(f"  FY2026 guide (held unchanged):           {FY26_GUIDE_LOW_PCT:.1f}%-{FY26_GUIDE_HIGH_PCT:.1f}%, expected near midpoint")
print(f"  Installed base: {INSTALLED_BASE_DAVINCI:,} da Vinci (+12%)  ·  {INSTALLED_BASE_ION:,} Ion (+21%)")
print(f"  Post-earnings after-hours drop:          -{POST_EARNINGS_DROP_PCT:.1f}%")
print()
print(f"  A 2-point deceleration (14% → 12%) is a real, quantified signal, but it's also within the range")
print(f"  management explicitly guided to — the market's reaction (a double-digit single-day drop, ~38% off")
print(f"  the high) reflects how little margin for disappointment was priced into a 55x+ multiple at the peak,")
print(f"  not a fundamental break in the franchise. The named culprits (ACA subsidies, bariatric pressure,")
print(f"  deferred procedures) are plausibly transitory rather than structural.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_gm  = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 70.0% GM):      +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*34:.2f}/share at 34× P/E")
print(f"  Every 1pp of gross margin:            +${eps_per_1pp_gm:.3f}/EPS  = +${eps_per_1pp_gm*34:.2f}/share at 34× P/E")
print(f"  Every 1 turn of P/E:                  ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (procedure growth / revenue / installed base / recurring mix / guidance / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<38}  {'BEAR':>7}  {'BASE':>7}  {'BULL':>7}  {'XBULL':>7}  {'NOW':>10}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<38}  {ths[0]:>7}  {ths[1]:>7}  {ths[2]:>7}  {ths[3]:>7}  {s['now']:>10}  {lbl}  {b}")
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
    ("Procedure growth",            "+12%",   "<8%",     "-4pp+",  "ACA/bariatric pressure proves structural rather than transitory; deceleration continues into 2027"),
    ("Revenue YoY",                 "+19%",   "<10%",    "-9pp+",  "Systems placements slow sharply as hospital capex tightens alongside decelerating procedures"),
    ("Installed base growth",       "+12%",   "<6%",     "-6pp+",  "Competitive pressure (Medtronic Hugo, others) starts winning meaningful share"),
    ("Recurring revenue mix",       "85%",    "<75%",    "-10pp+", "Instrument pricing pressure or procedure-mix shift toward lower-intensity cases"),
    ("FY2026 guidance stance",      "held",   "cut",     "reversal","Management is forced to formally cut the growth guide at a future quarter"),
    ("Forward P/E",                 "~36.1x", ">55x",    "re-rate","Ironically, P/E can rise even as price falls if EPS growth disappoints more than price does"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the entire bear case hinges on whether the Q2 deceleration (14%→12%) is the start of a")
print(f"  trend or a single-quarter wobble within a guide range management explicitly held. ISRG's installed-base")
print(f"  moat and 85% recurring revenue mean the P&L doesn't break even if growth merely slows — the real risk")
print(f"  is a multi-year growth-rate reset that keeps the multiple compressed even as absolute dollars keep growing.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS estimate:       ${EPS_FY2026E:.2f}  (current analyst consensus)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (even in downturns, ISRG's franchise rarely trades at a true distress multiple)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS, down from ~58× at the 52-week high.")
print(f"  The correction has done real work, but the EPP floor still sits meaningfully below spot — this is a")
print(f"  name where 'cheap' means 'less expensive than a bubble,' not 'statistically inexpensive.'")
print(f"  At a 30× reversion (a more typical premium-medtech multiple): ${EPS_FY2026E:.2f} × 30 = ${EPS_FY2026E*30:.0f}  ({(EPS_FY2026E*30/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest growth off FY2026E, growth-rate debate persists)")
hr()
print(f"  Conservative FY2028E EPS:  ${CONS_EPS_2YR:.2f}  (~17% cumulative EPS growth — below the historical trajectory)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~36.1× → 28×; a real de-rating)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (ISRG pays no dividend)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: even after a 38% correction, a conservative case with continued (if unspectacular)")
print(f"  earnings growth and only a modest further de-rating comes out {'roughly flat-to-negative' if cons_return < 5 else 'positive'}. The franchise quality is")
print(f"  not in question — the valuation still requires the growth-deceleration scare to prove temporary.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.38
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Recent moves:          -11.6% after-hours on the Q2 print; +6.25% today as the stock stabilizes")
print(f"  Annual dividend:      $0.00/share  (no dividend; full reinvestment in growth)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (elevated — a growth-medtech name now trading on a live growth-rate debate)")
print(f"  Beta vs S&P 500:      1.20  (above market)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (large, but the stock has already moved ~1.5σ this year)")
print(f"  → Q3 2026 print (mid-October) is the next test of whether procedure growth stabilizes near guidance.")
print(f"  → Monthly/quarterly procedure-volume commentary and China tender activity are the leading indicators.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $310  |  Trim above $480")

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
print(f"  ISRG remains the best-in-class franchise in surgical robotics, and the correction has repriced real")
print(f"  risk that didn't exist at the 52-week high — but the bear/bull spread is asymmetric because the")
print(f"  downside from further deceleration is larger than the upside from a guidance-midpoint outcome already priced in.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q3 2026 print (mid-October) — does procedure growth stabilize near the 13.5-15.5% guide?")
print(f"  (2) ACA subsidy and bariatric-procedure trends — the specific named culprits behind the Q2 slowdown")
print(f"  (3) China tender activity and any signs of stabilization in that geography")
print(f"  (4) da Vinci 5 and Ion systems placement trends — the leading indicator for future recurring revenue")
print(f"  (5) Competitive dynamics (Medtronic Hugo and others) — any real share-loss evidence, not just launches")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $310  |  Trim above $480")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  Q2 procedure growth: +{Q2_2026_PROCEDURE_GROWTH_PCT:.0f}%")
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
