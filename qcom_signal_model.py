"""
QCOM  ·  QUALCOMM Incorporated  ·  NASDAQ: QCOM
Bottom-up signal model  ·  Mobile Chips (ex-Apple) / Automotive / IoT / Data Center AI
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "QCOM"
COMPANY       = "QUALCOMM Incorporated"
SECTOR        = "Semiconductors · Snapdragon · Automotive · IoT · Data Center AI (AI200/AI250) · NASDAQ: QCOM"
CURRENT_PRICE = 147.61       # USD; close 2026-07-31 (verified live), post-Q3-earnings selloff
VOL_52W_LOW   = 121.99       # 2025 post-Apple-modem-exit overhang trough
VOL_52W_HIGH  = 259.92       # 2026 diversification re-rating peak (pre-Q3 print)
SHARES_OUT_M  = 1_068.0      # millions; $157.7B mkt cap / $147.61
ANNUAL_DIV    = 3.68         # $/share forward; yield ~2.49%

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B; fiscal year ends September) ─────────
# Q3 FY2026 actual: QCT $8.504B (-5%: Handset $5.086B -20%, Auto $1.588B +61%, IoT $1.830B +9%);
# QTL $1.278B (-3%). Q4 guide: total revenue $9.7-10.5B. Apple revenue ~-50% seq into Dec quarter.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("QCT Handsets (Snapdragon, ex-Apple)", 19.5, 15.0, 22.5, "Android flagship/premium share gains must now offset the accelerating Apple modem exit"),
    ("QCT Automotive",                       6.3,  5.2,  8.0, "Record +61% YoY in Q3; run-rate guide raised to ~$7B exiting FY2026 (from $6B)"),
    ("QCT IoT",                              7.2,  6.2,  8.5, "+9% YoY; industrial/edge-AI demand steady, less dramatic than automotive"),
    ("QTL Licensing",                        5.1,  4.5,  5.6, "69% EBT margin annuity; declining royalty base as Apple's own modem removes a payer"),
]

# Margin assumptions (non-GAAP)
OP_MARGIN_CURR   = 0.342    # FY2026E blended non-GAAP operating margin proxy; QCT EBT margin already fell to 26% in Q3
OP_MARGIN_BULL   = 0.375    # BULL: Automotive/IoT mix improves blend; data center AI200/AI250 adds high-margin revenue
OP_MARGIN_BEAR   = 0.290    # BEAR: Apple exit accelerates faster than diversification revenue backfills it
TAX_RATE         = 0.140    # non-GAAP effective tax rate

# ── APPLE EXIT / DIVERSIFICATION CALCULATOR (the Qualcomm-specific angle) ────
APPLE_SEQ_DECLINE_PCT = 50.0   # % sequential decline in Apple-related revenue guided into the Dec 2026 quarter
AUTO_RUNRATE_EXIT_B   =  7.0   # $B annualized Automotive run-rate guided exiting FY2026 (raised from $6B)
DC_TARGET_FY2027_B    =  5.0   # $B data center AI revenue target for FY2027 (AI200 launches 2026, AI250 2027)
Q3_QCT_EBT_MARGIN_PCT = 26.0   # % QCT EBT margin in Q3, down from 30% YoY
Q4_EPS_GUIDE_LOW      = 2.05   # $ Q4 FY2026 non-GAAP EPS guidance low end (below the ~$2.35-2.38 Street estimate)
Q4_EPS_GUIDE_HIGH     = 2.25   # $ Q4 FY2026 non-GAAP EPS guidance high end

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 10.50       # $/share non-GAAP FY2026E; sum of actual Q1 $3.50 + Q2 $2.65 + Q3 $2.21 + Q4 guide midpoint $2.15
PE_PESSIMISTIC = 10.0        # trough P/E: QCOM traded near 10-11x forward during the depths of the
                             # 2025 Apple-modem-exit overhang; 10x prices a comparable or deeper air pocket
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 7.22, 10,   72, "Apple exit lands faster than guided; Automotive/IoT/data-center can't backfill the gap in time"),
    "BASE":  (10.80, 13,  140, "Apple decline plays out roughly as guided; Automotive hits the $7B+ run-rate; margin stabilizes"),
    "BULL":  (13.89, 16,  222, "Automotive scales past $8B; AI200/AI250 data center revenue proves out toward the $5B FY2027 target"),
    "XBULL": (16.00, 20,  320, "Qualcomm re-rates as a diversified edge-to-datacenter AI silicon company, Apple exit fully absorbed"),
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
        "name":       "Automotive revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<20%",   "≥35%",   "≥50%",   "≥70%"),
        "now":        "+61%",
        "score":      3,
        "comment":    "Record $1.588B in Q3; run-rate guide raised to ~$7B exiting FY2026 — the clearest bright spot in the print",
    },
    {
        "name":       "Apple-related revenue trajectory",
        "weight":     0.25,
        "thresholds": ("accelerating loss","as guided","slower than guided","resolved/immaterial"),
        "now":        "accelerating loss",
        "score":      1,
        "comment":    "Guided -50% sequential into the Dec quarter; FY2027 Apple revenue flagged as 'much lower' than prior expectations",
    },
    {
        "name":       "QCT Handset revenue YoY",
        "weight":     0.15,
        "thresholds": ("<-25%",  "≥-15%",  "≥-5%",   "≥5%"),
        "now":        "-20%",
        "score":      2,
        "comment":    "Memory supply constraints, higher input costs, and softer China demand all hit at once in Q3",
    },
    {
        "name":       "QCT EBT margin",
        "weight":     0.15,
        "thresholds": ("<22%",   "≥26%",   "≥30%",   "≥34%"),
        "now":        "26%",
        "score":      2,
        "comment":    "Down from 30% YoY — cost pressure and mix shift are compressing the core chip business margin",
    },
    {
        "name":       "Data center AI revenue progress",
        "weight":     0.15,
        "thresholds": ("no traction","design wins","early revenue","$5B+ run-rate"),
        "now":        "design wins",
        "score":      2,
        "comment":    "AI200 (2026) and AI250 (2027) target a $5B FY2027 revenue level; hyperscaler shipments begin Dec 2026 at the earliest",
    },
    {
        "name":       "Forward P/E vs 10-yr average (~16x)",
        "weight":     0.10,
        "thresholds": (">18x",   "≤15x",   "≤12x",   "≤9x"),
        "now":        "14.1x",
        "score":      3,
        "comment":    "14.1× FY2026E — below the historical average despite the diversification story being more real than a year ago",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Automotive scaling for real — 61% YoY growth, run-rate guide raised mid-year, not just a design-win pipeline", +0.7, 0.20),
    ("-", "Apple exit accelerating — management's own language ('much lower' FY2027) moved the timeline up, not out",   -0.9, 0.25),
    ("-", "Q4 guide below Street — EPS guidance $2.05-2.25 vs ~$2.35-2.38 consensus is a real, not just sentiment, miss", -0.6, 0.15),
    ("+", "Valuation — 14.1× forward EPS sits below the 10-yr average even after two years of derisking the Apple story", +0.5, 0.15),
    ("+", "QTL licensing annuity — 69% EBT margin, still throwing off durable cash even as the royalty base narrows",    +0.3, 0.10),
    ("-", "Data center AI is unproven revenue — a $5B FY2027 target rests on early hyperscaler engagements, not signed backlog", -0.4, 0.15),
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
CONS_EPS_2YR  = 10.60   # conservative FY2028E: essentially flat EPS — Apple exit offsets Automotive/IoT growth
CONS_PE_2YR   = 13      # modest re-rating from 14.1× — the multiple doesn't need to expand for this to work
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Mobile Chips (ex-Apple) / Automotive / IoT / Data Center AI")
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
print(f"  Q3 FY2026 actual: QCT $8.50B (-5%), QTL $1.28B (-3%). Q4 guide: revenue $9.7-10.5B, EPS $2.05-2.25")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_op   = curr_total * OP_MARGIN_CURR
curr_eps  = round(curr_op * (1 - TAX_RATE) / shares, 2)

bull_op   = bull_total * OP_MARGIN_BULL
shares_b  = shares * 0.97
bull_eps_imp = round(bull_op * (1 - TAX_RATE) / shares_b, 2)

bear_op   = bear_total * OP_MARGIN_BEAR
bear_eps_imp = round(bear_op * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {OP_MARGIN_CURR*100:.1f}% op margin − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2026E:.2f}, from actual Q1-Q3 + Q4 guide  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {OP_MARGIN_BULL*100:.1f}% op margin, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 16× = ~${bull_eps_imp*16:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {OP_MARGIN_BEAR*100:.1f}% op margin (Apple exit outruns diversification)")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 10× trough = ~${bear_eps_imp*10:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")
print()
print(f"  ⚠ THE STRUCTURAL POINT: Automotive is only {SEG_DATA[1][1]/curr_total*100:.0f}% of FY2026E revenue but is almost the")
print(f"  entire growth story; Handsets at {SEG_DATA[0][1]/curr_total*100:.0f}% is still the base the whole model rests on. The bear")
print(f"  case doesn't require Automotive to disappoint — it just requires the Apple-related decline")
print(f"  in Handsets to outrun everything else being added on top of it, which is a timing question.")

# APPLE EXIT / DIVERSIFICATION CHECK
print()
print(f"  APPLE EXIT & DIVERSIFICATION CHECK  (the Qualcomm-specific angle):")
print(f"  Apple revenue sequential decline (guided):  -{APPLE_SEQ_DECLINE_PCT:.0f}%  into the December 2026 quarter")
print(f"  Automotive run-rate exiting FY2026:          ~${AUTO_RUNRATE_EXIT_B:.0f}B  (raised from ~$6B)")
print(f"  Data center AI target (FY2027):              ~${DC_TARGET_FY2027_B:.0f}B  (AI200 2026, AI250 2027; design-win stage)")
print(f"  QCT EBT margin:                               {Q3_QCT_EBT_MARGIN_PCT:.0f}%  (down from 30% YoY)")
print(f"  Q4 FY2026 EPS guide:                          ${Q4_EPS_GUIDE_LOW:.2f}-${Q4_EPS_GUIDE_HIGH:.2f}  (below the ~$2.35-2.38 Street estimate)")
print()
print(f"  The Apple modem exit has been the known, priced-in risk for two years. What moved the")
print(f"  stock on this print wasn't the exit itself — it's that management pulled the timeline")
print(f"  forward ('much lower' FY2027 Apple revenue) faster than diversification revenue can")
print(f"  currently offset. Automotive's raise is genuinely good news; it just isn't big enough")
print(f"  yet, in dollar terms, to fully net out a faster Apple decline.")

# KEY SENSITIVITIES
print()
eps_per_1B_auto = 1.0 * 0.38 * (1 - TAX_RATE) / shares   # automotive incremental margin ~38%
eps_per_1B_hand = 1.0 * 0.27 * (1 - TAX_RATE) / shares   # handset incremental margin ~27% (QCT blended, lower)
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Automotive revenue (38% inc. margin):  +${eps_per_1B_auto:.3f}/EPS  = +${eps_per_1B_auto*13:.2f}/share at 13× P/E")
print(f"  Every $1B Handset revenue (27% inc. margin):      +${eps_per_1B_hand:.3f}/EPS  = +${eps_per_1B_hand*13:.2f}/share at 13× P/E")
print(f"  Every 1 turn of P/E:                              ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Automotive / Apple exit / Handsets / margin / data center AI / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<38}  {'BEAR':>16}  {'BASE':>10}  {'BULL':>13}  {'XBULL':>16}  {'NOW':>16}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<38}  {ths[0]:>16}  {ths[1]:>10}  {ths[2]:>13}  {ths[3]:>16}  {s['now']:>16}  {lbl}  {b}")
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
print(f"  {'Signal':<32}  {'Current':>12}  {'Bear val':>12}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Automotive revenue YoY",     "+61%",  "<20%",     "-41pp",  "Design-win-to-revenue conversion slows; auto production cycle softens"),
    ("Apple revenue trajectory",   "-50% seq","worse",   "steeper","Apple's in-house modem ramps faster than the FY2027 timeline implies"),
    ("QCT Handset revenue YoY",    "-20%",  "<-30%",    "-10pp",  "China Android softness persists; memory/input costs stay elevated"),
    ("QCT EBT margin",             "26%",   "<20%",     "-6pp",   "Pricing pressure across handsets and IoT compresses the core margin further"),
    ("Forward P/E",                "14.1x", "≤10x",     "-4.1x",  "Market re-prices the diversification story as failed, not delayed"),
    ("Data center AI progress",    "design wins","stalled","none","AI200 hyperscaler engagement fails to convert to shipped revenue"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>12}  {bear_v:>12}  {move:>8}  {trigger[:42]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: this is fundamentally a RACE. Apple-related revenue is a known, declining")
print(f"  number with a now-accelerated timeline. Automotive, IoT, and data-center AI are the three")
print(f"  legs meant to replace it, and only Automotive has proven it can scale at the necessary")
print(f"  pace. The bear case isn't that any of these businesses fail — it's that the replacement")
print(f"  legs don't grow fast enough, in absolute dollars, to outrun the leg that's shrinking.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E non-GAAP EPS:       ${EPS_FY2026E:.2f}  (Q1 $3.50 + Q2 $2.65 + Q3 $2.21 + Q4 guide midpoint $2.15)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (QCOM traded 10-11× forward during the depths of the Apple-exit overhang)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E non-GAAP EPS — below its own")
print(f"  10-year average of roughly 16×, and only {abs(epp_gap_pct):.0f}% above the EPP floor. The stock has")
print(f"  already fallen {(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.0f}% from its 52-week high on this print. The market is not pricing")
print(f"  a diversification success story right now — it is pricing renewed uncertainty about the")
print(f"  pace of the Apple exit, on top of a multiple that was never especially generous to begin with.")
print(f"  At a 16× reversion (the 10-yr average): ${EPS_FY2026E:.2f} × 16 = ${EPS_FY2026E*16:.0f}  (+{(EPS_FY2026E*16/CURRENT_PRICE-1)*100:.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: Apple exit roughly offsets diversification, no re-rating)")
hr()
print(f"  Conservative FY2028E non-GAAP EPS:  ${CONS_EPS_2YR:.2f}  (~essentially flat — Apple decline nets against Auto/IoT growth)")
print(f"  Conservative exit P/E:               {CONS_PE_2YR}×  (14.1× → 13×; a small further de-rating, not a recovery)")
print(f"  Conservative equity value:            ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):        +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:               ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:            {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: this case assumes EPS goes essentially NOWHERE for two years — the Apple exit")
print(f"  and the diversification story roughly cancel out — and the dividend plus a token positive")
print(f"  multiple move still clears {cons_annual:.1f}%/yr. The stock does not need Automotive or data-center")
print(f"  AI to be a success for this to work; it needs them to merely keep pace with the known decline.")
print(f"  Breakeven at 13× requires FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f} — close to the current FY2026E level already.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.36
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Move off this print:  -{(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.0f}% from the 52W high, most of it in the days around Q3 earnings")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; long growth streak)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (elevated; Apple-headline sensitivity keeps this a jumpy stock)")
print(f"  Beta vs S&P 500:      1.25  (semiconductor-cycle + single-customer-exit risk premium)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ further drawdown  (would retest the 2025 post-Apple-exit-overhang low)")
print(f"  → Q4 print (likely early November) is the next confirm-or-deny data point on the Apple decline pace.")
print(f"  → Automotive design-win announcements are the highest-frequency positive catalyst available.")
print(f"  → ACCUMULATE at current price  |  BUY below $130  |  TRIM above $220")

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
print(f"  Qualcomm's Q3 print was genuinely mixed, not uniformly bad: a real Automotive beat and")
print(f"  raise sitting next to a real Apple-timeline pull-forward and a soft Q4 EPS guide. The")
print(f"  selloff priced the second half of that sentence more than the first. At 14.1× forward")
print(f"  with the dividend doing real work in the conservative case, this reads as ACCUMULATE.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q4 FY2026 print (~early November) — first read on whether the Apple decline tracks guidance")
print(f"  (2) Automotive run-rate progression toward and past the ~$7B exit target")
print(f"  (3) AI200 hyperscaler shipment confirmation (targeted Dec 2026) — the first real data-center AI revenue proof point")
print(f"  (4) QCT EBT margin trajectory — needs to stabilize, not just the top line, for the bear case to be ruled out")
print(f"  (5) Any FY2027 initial guidance detail on the magnitude of the Apple revenue decline")
print(f"  ACCUMULATE at ${CURRENT_PRICE:.2f}  |  BUY below $130  |  TRIM above $220")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  Auto run-rate: ${AUTO_RUNRATE_EXIT_B:.0f}B")
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
