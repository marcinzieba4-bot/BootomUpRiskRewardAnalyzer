"""
TMO  ·  Thermo Fisher Scientific Inc.  ·  NYSE: TMO
Bottom-up signal model  ·  Life Sciences Tools / Diagnostics / CRO / Bioproduction
Date: 2026-08-04
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "TMO"
COMPANY       = "Thermo Fisher Scientific Inc."
SECTOR        = "Life Sciences Tools · Analytical Instruments · Diagnostics · CRO · NYSE: TMO"
CURRENT_PRICE = 574.03      # USD; close 2026-08-03
VOL_52W_LOW   = 435.27      # USD
VOL_52W_HIGH  = 643.99      # USD
SHARES_OUT_M  = 369.8       # millions
ANNUAL_DIV    = 1.88        # $/share annualized

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# Q2 2026 actual (reported Jul 23, 2026): revenue $11.99B (+10% YoY); adj EPS $6.03 (+13% YoY);
# beat, guidance raised. FY2026 revenue guidance raised to $47.4-48.1B (6-8% reported growth,
# organic ~4%, up from prior 3-4% guide); FY2026 adj EPS guide raised to $24.93-25.33.
# China returned to low-single-digit growth (stabilizing, not yet a rebound); the NIH-exposed
# academic/government segment is also back to low-single-digit growth. Tariffs/reshoring remain
# an ongoing headwind cited by pharma/biotech customers but did not derail the guidance raise —
# strength this quarter was broad-based across all segments and geographies.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Life Sciences Solutions",         8.6,  7.5, 10.2, "Bioproduction (mRNA/gene therapy/biologics); biotech funding swing factor"),
    ("Analytical Instruments",          8.0,  6.7,  9.4, "Recovering from multi-year destocking; China capex now stabilizing, not yet rebounding"),
    ("Specialty Diagnostics",           5.7,  5.2,  6.4, "Stable, recurring; transplant/clinical diagnostics steady growth"),
    ("Laboratory Products & Biopharma Services", 25.45, 22.6, 29.0, "PPD CRO bookings; pharma services; largest segment by revenue"),
]

# Net-margin-based bridge
NET_MARGIN_CURR = 0.1946   # FY2026E; reconciles to raised guidance midpoint
NET_MARGIN_BEAR = 0.1761   # BEAR: policy headwinds re-intensify, margin compresses
NET_MARGIN_BULL = 0.2051   # BULL: bioproduction/CRO mix shift + operating leverage expand margin

# ── POLICY HEADWIND TRACKER (the TMO-specific angle) ──────────────────────────
Q2_2026_REVENUE_GROWTH_PCT = 10.0   # % YoY, Q2 2026 reported revenue growth
Q2_2026_ADJ_EPS_GROWTH_PCT = 13.0   # % YoY, Q2 2026 adjusted EPS growth
Q2_2026_ADJ_EPS            = 6.03   # $ adjusted EPS, Q2 2026 (beat)
CHINA_GROWTH_STATUS        = "low-single-digit (stabilizing)"
NIH_ACADEMIC_GROWTH_STATUS = "low-single-digit (stabilizing)"
STOCK_MOVE_FROM_JUNE_LOW_PCT = round((CURRENT_PRICE - 448.28) / 448.28 * 100, 1)  # recovery since last refresh

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 25.13       # FY2026E adj EPS (raised guidance $24.93-25.33; midpoint)
PE_PESSIMISTIC = 17.0        # pessimistic P/E: below the current ~22.8x multiple, a normalized/conservative multiple
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (20.00, 20,  400, "NIH/tariff/China headwinds re-intensify beyond the levels just guided through; EPS $20 → 20× multiple"),
    "BASE":  (25.13, 22.84, 574, "FY2026 guidance executed at the raised midpoint; China/NIH stabilization holds but doesn't yet accelerate"),
    "BULL":  (30.50, 24,  732, "Bioproduction reaccelerates, China/NIH turn from stabilizing to growing, CRO bookings recover; EPS $30.50 → 24×"),
    "XBULL": (34.00, 27,  918, "Full policy-headwind resolution + bioproduction supercycle; EPS $34 → 27× re-rating"),
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
        "name":       "Bioproduction revenue growth (mRNA/gene therapy/biologics)",
        "weight":     0.25,
        "thresholds": ("<5%",    "≥8%",   "≥13%",   "≥18%"),
        "now":        "+11%",
        "score":      3,
        "comment":    "Biotech manufacturing demand continuing to recover; broad-based strength this quarter",
    },
    {
        "name":       "Laboratory Products & Biopharma Services / CRO (PPD) revenue growth",
        "weight":     0.20,
        "thresholds": ("<0%",    "≥2%",   "≥6%",    "≥10%"),
        "now":        "+8%",
        "score":      3,
        "comment":    "PPD bookings improving alongside the broader Q2 beat; pharma services growth firmer than prior quarter",
    },
    {
        "name":       "Analytical Instruments segment recovery",
        "weight":     0.15,
        "thresholds": ("<-5%",   "≥0%",   "≥5%",    "≥10%"),
        "now":        "+4%",
        "score":      2,
        "comment":    "Destocking cycle largely behind; China capex stabilizing but not yet a clear reacceleration",
    },
    {
        "name":       "NIH/academic-government funding policy trajectory",
        "weight":     0.20,
        "thresholds": ("Worsening", "Stable",  "Improving", "Reversed"),
        "now":        "Improving",
        "score":      3,
        "comment":    "Academic/government end-market back to low-single-digit growth — an actual improvement, not just stabilization",
    },
    {
        "name":       "China market recovery",
        "weight":     0.10,
        "thresholds": ("<-10%",  "≥-5%",  "≥0%",    "≥+8%"),
        "now":        "+2%",
        "score":      3,
        "comment":    "China has turned positive (low-single-digit growth) after multiple quarters of decline",
    },
    {
        "name":       "FY2026 EPS guidance execution ($24.93-25.33, raised)",
        "weight":     0.10,
        "thresholds": ("<$23.50", "≥$24.64", "≥$25.50", "≥$27.00"),
        "now":        "$25.13 (midpoint)",
        "score":      2,
        "comment":    "Guidance raised for a second consecutive quarter on the back of a broad-based beat",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Dominant 'picks-and-shovels' franchise — #1 in lab tools, instruments, CRO, bioproduction", +0.7, 0.25),
    ("+", "Two consecutive guidance raises with broad-based, all-segment/all-geography strength",        +0.6, 0.20),
    ("-", "NIH/China stabilization is recent (one quarter) — not yet proven durable across a full cycle", -0.4, 0.20),
    ("-", "Tariff/reshoring costs remain a live, unresolved headwind even as other pressures ease",       -0.3, 0.15),
    ("-", "Stock has already re-rated ~28% off its June trough — much of the good news looks priced in", -0.5, 0.15),
    ("+", "Long-running dividend growth streak; durable FCF generation supports capital return",          +0.3, 0.05),
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
CONS_EPS_2YR  = 29.50   # conservative FY2028E: ~8%/yr off raised FY2026 guidance
CONS_PE_2YR   = 20      # modest compression from current ~22.8× as the re-rating cools
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Life Sciences Tools / Diagnostics / CRO / Bioproduction")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<26}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<26}  ${curr:>11.2f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<26}  ${curr_total:>11.2f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  Q2 2026 actual: revenue +{Q2_2026_REVENUE_GROWTH_PCT:.0f}% YoY, adj EPS ${Q2_2026_ADJ_EPS:.2f} (+{Q2_2026_ADJ_EPS_GROWTH_PCT:.0f}% YoY, beat)")
print()

# EPS bridge (net-margin based)
shares    = SHARES_OUT_M / 1000
curr_net  = curr_total * NET_MARGIN_CURR
curr_eps  = round(curr_net / shares, 2)

bull_net     = bull_total * NET_MARGIN_BULL
bull_eps_imp = round(bull_net / shares, 2)

bear_net     = bear_total * NET_MARGIN_BEAR
bear_eps_imp = round(bear_net / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.2f}B rev × {NET_MARGIN_CURR*100:.2f}% net margin")
print(f"  ÷ {shares:.4f}B shares  =  ${curr_eps:.2f}/share adj EPS  (guidance ${EPS_FY2026E:.2f} midpoint  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {NET_MARGIN_BULL*100:.2f}% net margin")
print(f"  ÷ {shares:.4f}B shares  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {NET_MARGIN_BEAR*100:.2f}% net margin (policy headwinds re-intensify)")
print(f"  ÷ {shares:.4f}B shares  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# POLICY HEADWIND TRACKER
print()
print(f"  POLICY HEADWIND TRACKER  (the TMO-specific angle):")
print(f"  Q2 2026 revenue growth:                     +{Q2_2026_REVENUE_GROWTH_PCT:.0f}% YoY")
print(f"  Q2 2026 adjusted EPS:                        ${Q2_2026_ADJ_EPS:.2f}  (+{Q2_2026_ADJ_EPS_GROWTH_PCT:.0f}% YoY, beat)")
print(f"  China growth status:                         {CHINA_GROWTH_STATUS}")
print(f"  NIH/academic-government growth status:       {NIH_ACADEMIC_GROWTH_STATUS}")
print(f"  Stock move since last refresh (Jun 10):       +{STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}%")
print()
print(f"  The two biggest overhangs from the last refresh — NIH funding cuts and China weakness — have both")
print(f"  turned from 'deteriorating' to 'stabilizing/improving' in a single quarter. That's genuinely good news,")
print(f"  but the stock has already re-rated ~28% to reflect it, which is the central tension in this name now:")
print(f"  the recovery is real but young, and a lot of it is already in the price.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = 1.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at {NET_MARGIN_CURR*100:.1f}% margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*22.84:.1f}/share at 22.8× P/E")
print(f"  1pp net margin expansion (mix/scale):        +${curr_total*0.01/shares:.3f}/EPS  = +${curr_total*0.01/shares*22.84:.1f}/share at 22.8× P/E")
print(f"  Every 1 turn of P/E:                          ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (bioproduction / CRO / instruments / NIH-China policy framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>9}  {'BASE':>7}  {'BULL':>9}  {'XBULL':>8}  {'NOW':>16}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>9}  {ths[1]:>7}  {ths[2]:>9}  {ths[3]:>8}  {s['now']:>16}  {lbl}  {b}")
    print(f"    {s['comment']}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15% hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:72]:<72}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<52}  {'Current':>16}  {'Bear val':>9}  Trigger")
hr()
bear_triggers = [
    ("Bioproduction revenue growth",   "+11%",   "<5%",    "Biotech funding tightens again; mRNA/gene therapy demand decelerates"),
    ("NIH/academic-government growth", "Improving", "Worsening", "Federal budget pressure resumes, reversing this quarter's stabilization"),
    ("China market revenue YoY",       "+2%",    "<-10%",  "China stimulus fails to sustain, capex freeze resumes"),
    ("Analytical Instruments growth",  "+4%",    "<-5%",   "Destocking resumes as end-market demand softens again"),
    ("Lab Products & Biopharma Svcs growth", "+8%", "<0%",  "PPD/CRO bookings stall as pharma R&D spending contracts"),
    ("FY2026 EPS guidance",            "$25.13", "<$23.50","Guidance cut mid-year as headwinds re-intensify beyond guided levels"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>16}  {bear_v:>9}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the one-quarter stabilization in NIH/academic funding and China demand proves")
print(f"  temporary rather than durable, and tariff costs escalate further — reversing the very trends")
print(f"  that drove the stock's ~28% re-rating off its June trough. The bear case here isn't about")
print(f"  new problems; it's about the recent good news not holding.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (raised guidance midpoint)")
print(f"  Pessimistic P/E:                {PE_PESSIMISTIC:.0f}×  (below the current ~22.8× multiple; a normalized, non-trough multiple)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f}, TMO trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS — near the middle of its 5-year")
print(f"  range again after the post-correction re-rating. The +{epp_gap_pct:.0f}% premium to EPP reflects a stock")
print(f"  pricing durable stabilization in China and NIH funding, not just a one-quarter data point.")
print(f"  EPP path: FY2028E EPS ~${CONS_EPS_2YR:.2f} × {PE_PESSIMISTIC:.0f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor (EPP growing with EPS).")
print(f"  At 24× mid-cycle P/E (durable recovery confirmed): ${EPS_FY2026E:.2f} × 24 = ${EPS_FY2026E*24:.0f}  — {(EPS_FY2026E*24/CURRENT_PRICE-1)*100:+.0f}% above current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: stabilization holds, multiple cools modestly)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (~8%/yr off raised FY2026 guidance)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (modest compression from current ~22.8×)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: the conservative case is muted, not because the business is weak, but because")
print(f"  the stock has already captured much of the recovery story in a single quarter's re-rating.")
print(f"  Breakeven at {CONS_PE_2YR}× P/E (no further multiple change): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  ACCUMULATE trigger: below $460  (ratio_b improves meaningfully on any re-test of the June trough)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.20
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock is up {STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}% since the last refresh (Jun 10) on two straight guidance raises")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (moderating as the policy-driven drawdown fades)")
print(f"  Beta vs S&P 500:      1.00  (life-sciences infrastructure; policy/macro sensitivity has eased but not vanished)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (a re-test of the June trough on renewed policy deterioration)")
print(f"  → China and NIH funding trend durability over the next 1-2 quarters is THE KEY swing factor.")
print(f"  → Bioproduction reacceleration + CRO bookings momentum are the KEY bull catalysts.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $460  |  Trim above $650")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is {'BELOW' if MARKET_COMPOSITE < ADJ_COMPOSITE else 'ABOVE'} the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The gap ({ADJ_GAP:+.2f}) indicates the stock is {valuation_label.lower()}")
print(f"  by model standards. TMO remains the dominant 'picks-and-shovels' franchise for global life sciences,")
print(f"  and the NIH/China stabilization this quarter is genuine — but a lot of that improvement is now priced in.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Durability of the China and NIH/academic funding stabilization over the next 1-2 quarters")
print(f"  (2) Bioproduction (mRNA/gene therapy) revenue growth trajectory")
print(f"  (3) Tariff/reshoring cost trends — whether they escalate or get mitigated")
print(f"  (4) Quarterly EPS guidance tracking vs the raised $24.93-25.33 range")
print(f"  (5) CRO/PPD bookings momentum — Laboratory Products & Biopharma Services segment growth")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $460  |  Trim above $650")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}")
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
