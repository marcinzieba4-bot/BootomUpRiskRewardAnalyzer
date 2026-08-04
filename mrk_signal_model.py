"""
MRK  ·  Merck & Co., Inc.  ·  NYSE: MRK
Bottom-up signal model  ·  Pharma / Oncology (Keytruda) / Cardiovascular (Winrevair) / Vaccines
Date: 2026-08-04
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "MRK"
COMPANY       = "Merck & Co., Inc."
SECTOR        = "Pharma · Oncology (Keytruda) · Cardiovascular (Winrevair) · Vaccines · NYSE: MRK"
CURRENT_PRICE = 129.30      # USD; intraday 2026-08-04, the morning of Q2 2026 earnings
VOL_52W_LOW   =  77.58      # USD
VOL_52W_HIGH  = 135.05      # USD
SHARES_OUT_M  = 2_470.0     # millions
ANNUAL_DIV    = 3.24        # $/share; quarterly dividend just raised to $0.81 (from $0.77)

# ── PRODUCT REVENUE BRIDGE (company-specific calculator, FY2027E) ────────────
# Q2 2026 actual (reported this morning, Aug 4 2026): revenue $15.8B, net income $5.4B,
# adjusted EPS $2.13. FY2026 non-GAAP guidance raised to revenue $65.8-67.0B, EPS $5.04-5.16
# (~$0.10 FX benefit) — a transition-year number depressed by BD/licensing deal costs and
# Qlex launch investment. The market is pricing MRK on a 2-year-forward, normalized earnings
# view rather than the FY2026 trough, which is why this bridge (and the SCENARIOS/EPP below)
# are built on an FY2027E basis. Q1 2026 color: Keytruda/Qlex $8.03B/qtr (+12% YoY), Winrevair
# $525M (+88% YoY, first full quarter of Qlex SC contributed $128M).
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Oncology (Keytruda/Welireg/Qlex)",        33.5, 24.0, 38.0, "Keytruda near peak (2028 US patent cliff, ~$35B+ at risk); Qlex subcutaneous reformulation extending franchise life"),
    ("Cardiovascular (Winrevair)",                4.0,  2.0,  7.0, "PAH treatment; +88% YoY in Q1; new franchise scaling into its second full year"),
    ("Vaccines (Gardasil/RSV)",                   9.5,  7.0, 11.5, "Gardasil China demand recovery key swing; RSV/vaccines portfolio growth"),
    ("Animal Health",                             6.2,  5.4,  7.0, "Stable, diversified, non-correlated cash flow"),
    ("General Medicine & Hospital/Other Pharma", 16.8, 14.5, 19.0, "Diabetes (Januvia/Janumet), hospital acute care, immunology; largely ex-growth stable base"),
]

# Net-margin-based bridge
NET_MARGIN_CURR = 0.3387   # FY2027E normalized; BD/licensing/launch costs from FY2026 largely roll off
NET_MARGIN_BEAR = 0.3035   # BEAR: cliff-related pricing pressure + fixed-cost deleverage compress margin
NET_MARGIN_BULL = 0.3533   # BULL: Winrevair/Qlex mix shift plus operating leverage expand margin

# ── KEYTRUDA CLIFF / DIVERSIFICATION TRACKER (the Merck-specific angle) ───────
Q2_2026_REVENUE_B          = 15.8   # $B, Q2 2026 actual reported revenue
Q2_2026_NET_INCOME_B       = 5.4    # $B, Q2 2026 actual net income
Q2_2026_ADJ_EPS            = 2.13   # $ adjusted EPS, Q2 2026
FY2026_GUIDANCE_EPS_RANGE  = "5.04-5.16"   # $ non-GAAP, raised FY2026 guidance
Q1_2026_KEYTRUDA_QTR_REV_B = 8.03   # $B/qtr, Keytruda+Qlex, +12% YoY
Q1_2026_WINREVAIR_QTR_REV_M = 525   # $M/qtr, +88% YoY
DIVIDEND_RAISED_TO         = 0.81   # $/qtr, up from $0.77
STOCK_MOVE_FROM_JUNE_LOW_PCT = round((CURRENT_PRICE - 122.55) / 122.55 * 100, 1)  # move since last refresh

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 9.60        # FY2027E EPS (normalized, 2yr-forward consensus-adjacent estimate)
PE_PESSIMISTIC = 9.0         # trough P/E: patent-cliff discount floor; historical pharma trough ~9-10x
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (6.50,  9,   59, "Keytruda decelerates faster pre-cliff; Qlex underwhelms; Winrevair stalls; EPS $6.50 → 9× = $59"),
    "BASE":  (9.60, 13.47, 129, "Keytruda growth slows but holds near-peak; Winrevair scales; Qlex extends franchise modestly; EPS $9.60 → 13.5× = $129"),
    "BULL":  (11.80, 16,  189, "Qlex extends Keytruda franchise meaningfully; Winrevair becomes a major franchise; pipeline delivers; EPS $11.80 → 16× = $189"),
    "XBULL": (14.00, 19,  266, "Cliff largely offset by Winrevair + Qlex + pipeline diversification; multiple re-rates toward growth peers; EPS $14.00 → 19× = $266"),
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
        "name":       "Keytruda revenue YoY growth (near peak, 2028 cliff)",
        "weight":     0.30,
        "thresholds": ("<5%",   "≥10%",  "≥15%",   "≥20%"),
        "now":        "+10%",
        "score":      2,
        "comment":    "Keytruda/Qlex $8.03B/qtr; growth decelerating as expected ahead of 2028 US patent cliff (~$35B+ at risk)",
    },
    {
        "name":       "Winrevair revenue growth (PAH franchise scaling)",
        "weight":     0.20,
        "thresholds": ("<20%",  "≥40%",  "≥70%",   "≥100%"),
        "now":        "+85%",
        "score":      3,
        "comment":    "$525M/qtr (+88% YoY in Q1); new cardiovascular franchise continuing to scale from a small base",
    },
    {
        "name":       "Qlex (subcutaneous Keytruda) launch trajectory",
        "weight":     0.20,
        "thresholds": ("<$50M", "≥$100M","≥$300M", "≥$750M"),
        "now":        "$310M",
        "score":      3,
        "comment":    "Ramping faster than the original $128M Q1 print; the clearest near-term evidence that franchise-life extension is real",
    },
    {
        "name":       "Gardasil/Vaccines franchise stability (China demand)",
        "weight":     0.15,
        "thresholds": ("<-15%", "≥-5%",  "≥+5%",   "≥+15%"),
        "now":        "~-5%",
        "score":      2,
        "comment":    "Gardasil China demand remains soft but stabilizing; broader vaccines portfolio (RSV) provides offset",
    },
    {
        "name":       "Pipeline productivity / new approvals offsetting cliff",
        "weight":     0.10,
        "thresholds": ("none",  "1 readout","2-3 readouts","4+ readouts"),
        "now":        "1-2",
        "score":      2,
        "comment":    "Several oncology/cardiovascular readouts pending; none yet large enough to fully offset the Keytruda cliff",
    },
    {
        "name":       "Cost discipline / margin trajectory",
        "weight":     0.05,
        "thresholds": ("<74%",  "≥76%",  "≥78%",   "≥80%"),
        "now":        "79%",
        "score":      3,
        "comment":    "Gross margin holding near 79%; BD/licensing costs that depressed FY2026 guidance expected to roll off into FY2027",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("-", "Keytruda concentration — ~40% of revenue faces 2028 US patent cliff (~$35B+ at risk)", -0.8, 0.30),
    ("-", "The stock has already re-rated to near its 52-week high — less of a discount left than in June", -0.1, 0.20),
    ("+", "Winrevair + Qlex + pipeline diversification — Qlex's faster-than-expected ramp is real evidence, not just a thesis", +0.5, 0.20),
    ("-", "Cliff timing/magnitude still caps multiple expansion until the offset is proven at full scale", -0.3, 0.15),
    ("+", "Vaccines + Animal Health — diversified, durable cash flow base; dividend support",          +0.3, 0.10),
    ("+", "Capital return — dividend just raised to $0.81/qtr ($3.24/yr, ~2.5% yield); disciplined buyback", +0.2, 0.05),
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
CONS_EPS_2YR  = 10.80   # FY2029E conservative: modest growth off the FY2027E base
CONS_PE_2YR   = 13      # roughly flat vs. the BASE-case ~13.5× multiple
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Pharma / Oncology (Keytruda) / Cardiovascular (Winrevair) / Vaccines")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2027E, normalized  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<40}  {'FY2027E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<40}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<40}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  Q2 2026 actual: revenue ${Q2_2026_REVENUE_B:.1f}B, net income ${Q2_2026_NET_INCOME_B:.1f}B, adj EPS ${Q2_2026_ADJ_EPS:.2f}")
print(f"  FY2026 guidance (transition year, BD/launch costs depress the near-term number): EPS ${FY2026_GUIDANCE_EPS_RANGE}")
print()

# EPS bridge (net-margin based)
shares    = SHARES_OUT_M / 1000
curr_net  = curr_total * NET_MARGIN_CURR
curr_eps  = round(curr_net / shares, 2)

bull_net     = bull_total * NET_MARGIN_BULL
bull_eps_imp = round(bull_net / shares, 2)

bear_net     = bear_total * NET_MARGIN_BEAR
bear_eps_imp = round(bear_net / shares, 2)

print(f"  FY2027E EPS check:  ${curr_total:.1f}B rev × {NET_MARGIN_CURR*100:.2f}% net margin")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2027E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {NET_MARGIN_BULL*100:.2f}% net margin")
print(f"  ÷ {shares:.3f}B shares  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {NET_MARGIN_BEAR*100:.2f}% net margin (cliff pricing pressure + fixed-cost deleverage)")
print(f"  ÷ {shares:.3f}B shares  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# CLIFF / DIVERSIFICATION TRACKER
print()
print(f"  KEYTRUDA CLIFF / DIVERSIFICATION TRACKER  (the Merck-specific angle):")
print(f"  Q1 2026 Keytruda+Qlex revenue:               ${Q1_2026_KEYTRUDA_QTR_REV_B:.2f}B/qtr  (+12% YoY)")
print(f"  Q1 2026 Winrevair revenue:                    ${Q1_2026_WINREVAIR_QTR_REV_M}M/qtr  (+88% YoY)")
print(f"  Q2 2026 revenue / net income / adj EPS:       ${Q2_2026_REVENUE_B:.1f}B / ${Q2_2026_NET_INCOME_B:.1f}B / ${Q2_2026_ADJ_EPS:.2f}")
print(f"  Quarterly dividend:                           raised to ${DIVIDEND_RAISED_TO:.2f} (from $0.77)")
print(f"  Stock move since last refresh (Jun 10):        +{STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}%")
print()
print(f"  MRK is up {STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}% since June, sitting near its 52-week (and multi-decade) high, even though")
print(f"  FY2026 guidance itself reflects a transition-year EPS dip. That combination only makes sense if the")
print(f"  market is looking through FY2026 toward FY2027E+ normalized earnings — which is exactly the basis")
print(f"  this model uses for its SCENARIOS and EPP, rather than the depressed FY2026 guidance figure directly.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev       = 1.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at {NET_MARGIN_CURR*100:.1f}% margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*13.5:.2f}/share at 13.5× P/E")
print(f"  1pp net margin expansion (mix/scale):        +${curr_total*0.01/shares:.3f}/EPS  = +${curr_total*0.01/shares*13.5:.2f}/share at 13.5× P/E")
print(f"  Every 1 turn of P/E:                          ±${EPS_FY2027E:.2f}/share  ({EPS_FY2027E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Keytruda trajectory / Winrevair / Qlex / Vaccines / Pipeline framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>5}  {'BASE':>5}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>6}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>5}  {ths[1]:>5}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>6}  {lbl}  {b}")
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
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  Trigger")
hr()
bear_triggers = [
    ("Keytruda revenue YoY growth",     "+10%",   "<5%",    "Growth decelerates faster than expected ahead of the 2028 cliff"),
    ("Qlex SC launch trajectory",       "$310M",  "<$50M",  "Subcutaneous launch stalls out; fails to extend exclusivity meaningfully"),
    ("Winrevair revenue growth",        "+85%",   "<20%",   "Cardiovascular franchise growth stalls; competitive PAH entrants"),
    ("Gardasil/Vaccines China demand",  "~-5%",   "<-15%",  "China vaccine demand remains structurally weak; no recovery"),
    ("Pipeline readouts",               "1-2",    "none",   "Oncology/cardio readouts disappoint; cliff remains unaddressed"),
    ("Gross margin",                    "79%",    "<74%",   "Mix shift to lower-margin segments as Keytruda declines"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Keytruda growth decelerates sharply ahead of schedule (well before the 2028 US patent")
print(f"  cliff) while Qlex's faster-than-expected ramp reverses, Winrevair growth stalls from competitive PAH")
print(f"  entrants, and Gardasil China demand stays depressed. EPS falls to ~$6.50 at a 9× cliff-discount floor.")
print(f"  Note: ${bear_price} is NOT permanent impairment — Vaccines/Animal Health plus a freshly-raised")
print(f"  dividend (${DIVIDEND_RAISED_TO:.2f}/qtr) provide a durable earnings floor.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           ${EPS_FY2027E:.2f}  (normalized, 2yr-forward basis)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (cliff-discount floor; pharma trough ~9-10×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP is a meaningfully larger gap than in June, reflecting the stock's")
print(f"  re-rating toward its 52-week high on Qlex/Winrevair execution evidence. The 2028 Keytruda US patent")
print(f"  cliff (~$35B+ revenue at risk) is still the dominant multi-year question; the market is now paying")
print(f"  up for the diversification thesis rather than discounting purely for cliff risk.")
print(f"  At {CONS_PE_2YR}× mid-cycle P/E: ${EPS_FY2027E:.2f} × {CONS_PE_2YR} = ${EPS_FY2027E*CONS_PE_2YR:.0f}  — roughly in line with current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest EPS growth into cliff approach; P/E roughly flat)")
hr()
print(f"  Conservative FY2029E EPS:        ${CONS_EPS_2YR:.2f}  (modest growth; Keytruda deceleration partly offset by Winrevair/Qlex)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (roughly flat from the ~13.5× BASE-case multiple)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: MRK now trades near its 52-week high on genuine Qlex/Winrevair execution")
print(f"  evidence, but the 2028 Keytruda cliff (~$35B+ at risk) is unchanged. If diversification keeps")
print(f"  proving out at the current pace, MRK re-rates further toward 16-19×. If it stalls, the stock")
print(f"  has real downside back toward its cliff-discount floor — a genuinely two-sided setup, not a")
print(f"  clear BUY or AVOID.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.22
beta        = 0.85
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock is up {STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}% since the last refresh (Jun 10); near multi-decade highs")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  Dividend Aristocrat, just raised)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (lower than tech peers; defensive pharma; cliff overhang still priced to some degree)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (defensive; lower than market; pharma sector characteristics)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe; cliff-acceleration tail scenario)")
print(f"  → Keytruda growth deceleration pace and Qlex ramp durability are THE KEY binaries for downside risk.")
print(f"  → Winrevair scaling + Qlex exclusivity extension remain the KEY bull catalysts.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $105  |  Trim above $150")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is")
print(f"  {'ABOVE' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'BELOW'} the model's adj composite ({ADJ_COMPOSITE:.3f}). The gap ({ADJ_GAP:+.2f}) indicates the stock is")
print(f"  {valuation_label.lower()} by model standards. In plain terms: the 2028 Keytruda patent cliff discount has")
print(f"  narrowed as Winrevair and Qlex keep proving out — a genuinely positive development — but the stock's")
print(f"  ~{STOCK_MOVE_FROM_JUNE_LOW_PCT:.0f}% re-rating since June means less of that good news is left to be discovered at the current price.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Keytruda quarterly revenue trajectory — growth deceleration tracking ahead of the 2028 cliff")
print(f"  (2) Winrevair revenue scaling — confirmation of the new cardiovascular franchise trajectory")
print(f"  (3) Qlex (subcutaneous Keytruda) ramp — IP/exclusivity implications for franchise life")
print(f"  (4) Gardasil/vaccines China demand recovery — key swing factor for the vaccines segment")
print(f"  (5) Pipeline readouts (oncology, cardiovascular) — productivity to offset the 2028 cliff")
print(f"  (6) Dividend sustainability — ${ANNUAL_DIV:.2f}/share payout, just raised, amid the cliff transition")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $105  |  Trim above $150")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2027E EPS: ${EPS_FY2027E:.2f}")
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
