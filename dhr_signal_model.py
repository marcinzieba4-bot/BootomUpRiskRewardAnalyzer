"""
DHR  ·  Danaher Corporation  ·  NYSE: DHR
Bottom-up signal model  ·  Life Sciences / Bioprocessing (Cytiva/Pall) / Diagnostics / DBS
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "DHR"
COMPANY       = "Danaher Corporation"
SECTOR        = "Life Sciences Tools · Bioprocessing (Cytiva/Pall) · Diagnostics · DBS · NYSE: DHR"
CURRENT_PRICE = 197.50      # USD; close 2026-08-03, +1.29%, largely recovered from the post-earnings selloff
VOL_52W_LOW   = 160.93      # 2025/26 trough
VOL_52W_HIGH  = 242.80      # 2026 pre-earnings peak
SHARES_OUT_M  = 700.0       # millions; ~$138.2B mkt cap / $197.50
ANNUAL_DIV    = 1.16        # $/share; modest but steady grower

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ──────────────────────────────────────
# Q2 2026 actual: revenue $6.3B (+5.5% YoY), adj EPS $1.94 (+8%, beat $1.83 est by 6%). Biotechnology
# segment (Cytiva/Pall) revenue $1.92B (+4.0%: +2.5% core, +1.5% FX), adj operating margin 41.0% flat.
# ~$100M of bioprocessing revenue shifted into 2027 on customer production-schedule timing, even as
# underlying order trends stayed healthy (mid-teens order growth in both consumables and equipment).
# FY2026 core revenue growth guide: 3-4%. FY2026 adj EPS guidance raised to $8.45-$8.60. Shares fell
# ~15% premarket on the bioprocessing-timing news but have since fully recovered.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Bioprocessing (Biotechnology: Cytiva/Pall)", 7.90, 6.50,  9.50, "The margin-rich growth engine; ~$100M shifted to 2027 on customer timing, not lost demand — orders stayed mid-teens"),
    ("Life Sciences & Diagnostics (incl. Masimo)", 17.40, 15.50, 19.50, "The steadier, larger base; Masimo integration adds diagnostics scale"),
]

# Operating-margin assumptions (blended across segments + corporate overhead)
OP_MARGIN_CURR = 0.291   # FY2026E; reconciles to the $8.45-$8.60 adj EPS guide midpoint
OP_MARGIN_BEAR = 0.240   # BEAR: a renewed bioprocessing destocking cycle hits the highest-margin segment hardest
OP_MARGIN_BULL = 0.320   # BULL: the delayed $100M+ shipments land, bioprocessing supercycle reaccelerates, scale efficiencies compound
TAX_RATE       = 0.190   # effective tax rate

# ── BIOPROCESSING TIMING CALCULATOR (the Danaher-specific angle) ─────────────
BIOPROCESSING_SHIFT_TO_2027_M = 100   # $M; bioprocessing revenue shifted from 2026 into 2027 on customer production timing
BIOTECH_SEG_REV_Q2_B          = 1.92  # $B; Q2 2026 Biotechnology (Cytiva/Pall) segment revenue
BIOTECH_SEG_OP_MARGIN_PCT     = 41.0  # % Q2 2026 Biotechnology segment adjusted operating margin (flat YoY)
BIOTECH_ORDER_GROWTH          = "mid-teens"  # consumables and equipment order growth, Q2 2026
PREMARKET_DROP_PCT            = 14.87 # % premarket decline on the Q2 print before the stock recovered

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 8.53        # $/share FY2026E adj; guide midpoint ($8.45-$8.60)
PE_PESSIMISTIC = 17.0        # trough P/E: matches Danaher's own multi-cycle life-sciences-tools trough average
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 6.11, 17,  104, "A renewed bioprocessing destocking cycle hits, echoing 2022-2024; the shifted $100M proves to be the start of a trend"),
    "BASE":  ( 9.12, 22,  201, "Core growth holds near the 3-4% guide; the shifted bioprocessing revenue lands in 2027 roughly as described"),
    "BULL":  (10.96, 24,  263, "Bioprocessing reaccelerates as the delayed shipments land and underlying mid-teens order growth converts to revenue"),
    "XBULL": (13.26, 25,  332, "A genuine multi-year bioprocessing supercycle resumes; Masimo integration and DBS operating leverage compound further"),
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
        "weight":     0.20,
        "thresholds": ("<2%",    "≥4%",    "≥6%",    "≥8%"),
        "now":        "+5.5%",
        "score":      3,
        "comment":    "Q2 beat on both revenue and EPS despite the bioprocessing-timing headline",
    },
    {
        "name":       "Bioprocessing order growth",
        "weight":     0.20,
        "thresholds": ("<0%",    "≥5%",    "≥10%",   "≥15%"),
        "now":        "mid-teens",
        "score":      4,
        "comment":    "Underlying consumables and equipment orders grew mid-teens — the demand signal is stronger than the revenue-timing headline suggests",
    },
    {
        "name":       "Biotechnology segment operating margin",
        "weight":     0.15,
        "thresholds": ("<35%",   "≥38%",   "≥40%",   "≥43%"),
        "now":        "41.0%",
        "score":      3,
        "comment":    "Held flat YoY at an industry-leading level even through the revenue-timing disruption",
    },
    {
        "name":       "Adj EPS beat magnitude",
        "weight":     0.15,
        "thresholds": ("miss",   "in-line", "beat",  "large beat"),
        "now":        "+6.0% beat",
        "score":      3,
        "comment":    "$1.94 vs $1.83 est — a real beat, not just a rounding beat, alongside raised full-year EPS guidance",
    },
    {
        "name":       "FY2026 guidance direction",
        "weight":     0.15,
        "thresholds": ("cut",    "trimmed", "held",   "raised"),
        "now":        "raised",
        "score":      4,
        "comment":    "FY2026 adj EPS guidance raised to $8.45-$8.60 even while flagging the bioprocessing timing shift",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.15,
        "thresholds": (">28x",   "≤23x",   "≤19x",   "≤15x"),
        "now":        "~23.2x",
        "score":      2,
        "comment":    "23.2× FY2026E adj EPS — a fair, not cheap, multiple for a name that just spooked the market on timing, not demand",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "The ~$100M bioprocessing shift is a timing issue (customer production schedules), not a demand issue — orders grew mid-teens", +0.6, 0.25),
    ("-", "Danaher has genuine memory-of-2022-2024 risk here — the market's -15% reaction shows investors are primed to assume the worst on bioprocessing headlines", -0.4, 0.20),
    ("+", "Raising full-year EPS guidance in the same release as the timing disruption is a real signal of underlying confidence", +0.4, 0.15),
    ("+", "DBS (Danaher Business System) has a multi-decade track record of compounding operating margin through cycles", +0.3, 0.15),
    ("-", "At 23.2× forward earnings the stock isn't statistically cheap even after the round-trip back to pre-earnings levels", -0.3, 0.15),
    ("-", "Masimo integration and life-sciences funding (NIH, biotech capex) headwinds remain live, sector-wide risks", -0.3, 0.10),
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
CONS_EPS_2YR  = 9.60    # conservative FY2028E: modest growth off FY2026E guide midpoint
CONS_PE_2YR   = 20      # a modest de-rating from ~23.2×
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Bioprocessing / Diagnostics / DBS")
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
print(f"  Q2 2026 actual: $6.3B (+5.5% YoY). Biotechnology (Cytiva/Pall) $1.92B (+4.0%), op margin 41.0% flat")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_oi   = curr_total * OP_MARGIN_CURR
curr_eps  = round(curr_oi * (1 - TAX_RATE) / shares, 2)

shares_b  = shares * 0.98
bull_oi   = bull_total * OP_MARGIN_BULL
bull_eps_imp = round(bull_oi * (1 - TAX_RATE) / shares_b, 2)

bear_oi   = bear_total * OP_MARGIN_BEAR
bear_eps_imp = round(max(0, bear_oi) * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.2f}B rev × {OP_MARGIN_CURR*100:.1f}% op margin")
print(f"  − {TAX_RATE*100:.1f}% tax  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B rev × {OP_MARGIN_BULL*100:.1f}% op margin, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B rev × {OP_MARGIN_BEAR*100:.1f}% op margin (destocking hits the margin-rich segment)")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# BIOPROCESSING TIMING CHECK
print()
print(f"  BIOPROCESSING TIMING CHECK  (the Danaher-specific angle):")
print(f"  Revenue shifted from 2026 into 2027:   ${BIOPROCESSING_SHIFT_TO_2027_M}M  (customer production-schedule timing, not lost orders)")
print(f"  Biotechnology segment revenue (Q2):     ${BIOTECH_SEG_REV_Q2_B}B  (+4.0% YoY)")
print(f"  Biotechnology segment op margin (Q2):    {BIOTECH_SEG_OP_MARGIN_PCT}%  (flat YoY, industry-leading)")
print(f"  Underlying order growth:                {BIOTECH_ORDER_GROWTH}  (consumables and equipment)")
print(f"  Premarket drop on the print:            -{PREMARKET_DROP_PCT:.2f}%  (since fully recovered)")
print()
print(f"  The market's reaction echoes the 2022-2024 bioprocessing destocking cycle almost reflexively — a")
print(f"  single quarter's $100M timing shift triggered a 15% premarket drop before the stock round-tripped")
print(f"  back within two weeks. The underlying order data (mid-teens growth) is the more reliable signal than")
print(f"  the headline revenue miss, and management raised full-year EPS guidance in the same release.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * OP_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_opm = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 29.1% op margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*23:.2f}/share at 23× P/E")
print(f"  Every 1pp of operating margin:            +${eps_per_1pp_opm:.3f}/EPS  = +${eps_per_1pp_opm*23:.2f}/share at 23× P/E")
print(f"  Every 1 turn of P/E:                      ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (revenue growth / bioprocessing orders / segment margin / EPS beat / guidance / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<40}  {'BEAR':>7}  {'BASE':>7}  {'BULL':>7}  {'XBULL':>10}  {'NOW':>12}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<40}  {ths[0]:>7}  {ths[1]:>7}  {ths[2]:>7}  {ths[3]:>10}  {s['now']:>12}  {lbl}  {b}")
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
    ("Total revenue YoY",           "+5.5%",  "<2%",     "-3.5pp+","A renewed bioprocessing destocking cycle takes hold, echoing 2022-2024"),
    ("Bioprocessing order growth",  "mid-teens","<0%",   "reversal","The order strength proves to be a lagging indicator that also rolls over"),
    ("Biotech segment op margin",   "41.0%",  "<35%",    "-6pp+",  "Underutilization in the highest-margin segment as volumes disappoint"),
    ("Adj EPS beat magnitude",      "+6% beat","miss",   "reversal","A beat-and-raise streak breaks; guidance proves too optimistic"),
    ("FY2026 guidance direction",   "raised", "cut",     "reversal","Management is forced to formally cut guidance at a future quarter"),
    ("Forward P/E",                 "~23.2x", ">28x",    "re-rate","Ironically, P/E can rise even as price falls if EPS disappoints more than price does"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Danaher investors have real, scar-tissue memory of the multi-year 2022-2024 bioprocessing")
print(f"  destocking cycle, which is exactly why a single quarter's $100M timing shift triggered a 15% drop.")
print(f"  The bear case requires that reflexive fear to be right this time — that order strength doesn't")
print(f"  convert to revenue — rather than the more likely reading that this is genuine timing noise.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS estimate:       ${EPS_FY2026E:.2f}  (guide midpoint, $8.45-$8.60)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (Danaher's own multi-cycle life-sciences-tools trough average)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS — a fair, not distressed, multiple")
print(f"  for a name that just had a scare and recovered. The EPP floor provides real, if not enormous, margin")
print(f"  of safety versus the historical trough multiple.")
print(f"  At a 20× reversion (a modest premium to trough): ${EPS_FY2026E:.2f} × 20 = ${EPS_FY2026E*20:.0f}  ({(EPS_FY2026E*20/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest growth off FY2026E guide midpoint)")
hr()
print(f"  Conservative FY2028E EPS:  ${CONS_EPS_2YR:.2f}  (~12.5% cumulative EPS growth — below the historical DBS-driven trajectory)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~23.2× → 20×; a modest de-rating)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: a conservative case with modest growth and a modest de-rating comes out roughly")
print(f"  {'flat' if abs(cons_return) < 3 else 'positive' if cons_return > 0 else 'negative'} — this isn't a name with a wide margin of safety at the current, already-recovered price. The case for")
print(f"  owning it here rests on the bioprocessing order data converting to revenue roughly as guided, not on")
print(f"  a statistically cheap starting multiple.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.30
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Recent moves:          -14.87% premarket on the print, since fully recovered to +1.29% today")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; modest but steady)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (moderate-high, reflecting the bioprocessing-headline sensitivity)")
print(f"  Beta vs S&P 500:      1.05  (roughly market)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (large, consistent with a genuine renewed destocking cycle)")
print(f"  → Q3 2026 print (mid-October) is the next test of whether the shifted bioprocessing revenue lands as described.")
print(f"  → Bioprocessing order trends and any further shipment-timing commentary are the leading indicators.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $175  |  Trim above $230")

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
print(f"  Danaher beat on revenue and EPS and raised full-year guidance, yet the market's reflexive fear of a")
print(f"  repeat bioprocessing destocking cycle drove a sharp initial drop before a full round-trip recovery.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q3 2026 print (mid-October) — does the shifted $100M bioprocessing revenue land as described?")
print(f"  (2) Bioprocessing order trends — the leading indicator that has stayed mid-teens through the timing noise")
print(f"  (3) Masimo integration progress and diagnostics segment performance")
print(f"  (4) Life-sciences funding environment (NIH, biotech capex) — sector-wide, not Danaher-specific")
print(f"  (5) Any further evidence on whether this is timing noise or the start of a renewed destocking cycle")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $175  |  Trim above $230")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  Bioprocessing shift: ${BIOPROCESSING_SHIFT_TO_2027_M}M to 2027")
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
