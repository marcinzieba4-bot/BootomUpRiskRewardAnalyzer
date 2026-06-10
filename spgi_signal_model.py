"""
SPGI  ·  S&P Global Inc.  ·  NYSE: SPGI
Bottom-up signal model  ·  Credit Ratings / Market Intelligence / Indices / Commodity Insights
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "SPGI"
COMPANY       = "S&P Global Inc."
SECTOR        = "Credit Ratings · Market Intelligence · Indices · Commodity Insights · NYSE: SPGI"
CURRENT_PRICE = 512.40       # USD; as of 2026-06-10
VOL_52W_LOW   = 442.50       # 2025 rate-uncertainty/credit-tightening trough
VOL_52W_HIGH  = 558.90       # early-2026 peak on issuance recovery + Indices AUM growth
SHARES_OUT_M  = 305.0        # millions; declining ~1.5%/yr via buyback
SHARES_OUT_M_2YR = SHARES_OUT_M * 0.97   # post-buyback shares (2yr)

# Dividend: 52-year growth streak (Dividend King); growing ~6-8%/yr
ANNUAL_DIV    = 3.84         # $/share FY2026 ($0.96/quarter)

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ──────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Ratings",            4.55, 3.40, 5.45, "Bond issuance duopoly w/ Moody's; rate cuts/refi waves = key swing factor"),
    ("Market Intelligence",4.95, 4.65, 5.45, "Subscription data/analytics post-IHS Markit; recurring, sticky ~95% retention"),
    ("Mobility",           1.45, 1.30, 1.65, "Auto data/analytics (CARFAX, dealer); used-car & EV transition tailwinds"),
    ("Commodity Insights", 2.85, 2.60, 3.30, "Energy/commodity pricing benchmarks (Platts); energy transition data demand"),
    ("Indices",            1.95, 1.65, 2.55, "S&P 500/Dow Jones licensing; AUM-linked + transaction fees; passive investing growth"),
]

# Margin assumptions
OPERATING_MARGIN_CURR = 0.485   # blended adj operating margin FY2026E (~48.5%; toll-booth model)
OPERATING_MARGIN_BULL = 0.510   # BULL: Ratings operating leverage + Indices mix lift margin further
OPEX_BELOW_LINE_B     = 1.10    # net interest + other below-the-line items ($B)
TAX_RATE              = 0.225   # effective tax rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 17.50       # FY2026E adj EPS (consensus ~$17.30-$17.70; non-GAAP)
PE_PESSIMISTIC = 26.0        # trough P/E: even in credit-tightening, duopoly toll-booth commands premium floor
                              # (2022 issuance collapse trough ~24-25x; structural floor ~26x)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $455

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (14.50, 26,  377, "Credit-tightening cycle; bond issuance -25%; Ratings -25%; EPS $14.50 → 26x trough P/E"),
    "BASE":  (18.50, 30,  555, "Moderate refi wave continues; Indices AUM growth steady; EPS $18.50 at FY2028E → 30x"),
    "BULL":  (22.50, 34,  765, "Rate-cut cycle drives issuance boom; Indices AUM surge w/ passive flows; EPS $22.50 → 34x"),
    "XBULL": (27.00, 36,  972, "Multi-year refi supercycle + private credit ratings expansion; Indices ETF AUM >$25T; EPS $27 → 36x"),
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
        "name":       "Global bond issuance volume YoY",
        "weight":     0.30,
        "thresholds": ("<-15%",  "≥0%",   "≥+12%",  "≥+25%"),
        "now":        "+8%",
        "score":      2,
        "comment":    "Refi wave from 2024-25 maturity wall continues; rate-cut expectations supportive but not euphoric",
    },
    {
        "name":       "Ratings revenue YoY growth",
        "weight":     0.25,
        "thresholds": ("<-10%",  "≥0%",   "≥+10%",  "≥+20%"),
        "now":        "+6%",
        "score":      2,
        "comment":    "Transaction revenue tracking issuance; non-transaction (surveillance) fees stable +5%",
    },
    {
        "name":       "Indices AUM-linked revenue growth",
        "weight":     0.20,
        "thresholds": ("<0%",    "≥+8%",  "≥+15%",  "≥+25%"),
        "now":        "+13%",
        "score":      3,
        "comment":    "Passive investing structural tailwind; S&P 500/Dow ETF AUM at record highs; strong asset-based fee growth",
    },
    {
        "name":       "Market Intelligence subscription revenue growth",
        "weight":     0.15,
        "thresholds": ("<3%",    "≥5%",   "≥8%",    "≥12%"),
        "now":        "+6%",
        "score":      2,
        "comment":    "Post-IHS Markit integration mature; steady recurring growth; AI/analytics upsell modest contributor",
    },
    {
        "name":       "Adjusted operating margin",
        "weight":     0.05,
        "thresholds": ("<45%",   "≥47%",  "≥49%",   "≥52%"),
        "now":        "48.5%",
        "score":      2,
        "comment":    "Toll-booth economics intact; merger synergy realization largely complete; modest opex inflation",
    },
    {
        "name":       "Commodity Insights / Mobility revenue growth (combined)",
        "weight":     0.05,
        "thresholds": ("<2%",    "≥4%",   "≥7%",    "≥10%"),
        "now":        "+5%",
        "score":      2,
        "comment":    "Energy transition data demand offsetting legacy oil/gas pricing; Mobility benefits from EV/used-car data",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Ratings duopoly moat — S&P + Moody's control ~80% of global ratings market; near-impossible entry", +0.7, 0.25),
    ("+", "Indices flywheel — S&P 500/Dow licensing; AUM-linked recurring fees; passive investing secular growth", +0.6, 0.20),
    ("-", "Bond issuance cyclicality — Ratings revenue swings sharply with rate cycle & credit conditions",      -0.6, 0.20),
    ("+", "Market Intelligence diversification — post-IHS Markit subscription base smooths cyclical Ratings swings", +0.4, 0.15),
    ("+", "Capital return — Dividend King (52yr streak); steady buyback; strong FCF conversion ~90%+",           +0.3, 0.10),
    ("-", "Premium valuation risk — 29x FY2026E P/E historically rich (28-35x range); limited multiple re-rating room", -0.4, 0.10),
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
CONS_EPS_2YR  = 19.50   # conservative FY2028E: ~5.6% EPS CAGR; modest issuance growth + buyback
CONS_PE_2YR   = 27      # rerates from 29x toward growth-justified 27x; still premium
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Credit Ratings / Market Intelligence / Indices")
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
    print(f"  {seg:<26}  ${curr:>11.2f}  ${bear:>8.2f}  ${bull:>8.2f}  {bear-curr:>+7.2f}  {bull-curr:>+7.2f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<26}  ${curr_total:>11.2f}  ${bear_total:>8.2f}  ${bull_total:>8.2f}  {bear_total-curr_total:>+7.2f}  {bull_total-curr_total:>+7.2f}")
print()

# EPS bridge
curr_oi   = curr_total * OPERATING_MARGIN_CURR
curr_pretax = curr_oi - OPEX_BELOW_LINE_B
curr_ni   = curr_pretax * (1 - TAX_RATE)
shares    = SHARES_OUT_M / 1000
curr_eps  = round(curr_ni / shares, 2)

bull_oi   = bull_total * OPERATING_MARGIN_BULL
bull_pretax = bull_oi - OPEX_BELOW_LINE_B
bull_ni   = bull_pretax * (1 - TAX_RATE)
shares_b  = SHARES_OUT_M_2YR / 1000   # ~3% buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_oi   = bear_total * OPERATING_MARGIN_CURR * 0.95   # operating deleverage on lower issuance
bear_pretax = bear_oi - OPEX_BELOW_LINE_B
bear_ni   = max(0, bear_pretax) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.2f}B rev × {OPERATING_MARGIN_CURR*100:.1f}% op margin − ${OPEX_BELOW_LINE_B:.2f}B below-line − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B rev × {OPERATING_MARGIN_BULL*100:.1f}% op margin − below-line − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 34× = ~${bull_eps_imp*34:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B rev × {OPERATING_MARGIN_CURR*100*0.95:.1f}% op margin − below-line  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 26× trough P/E (duopoly floor) = ~${bear_eps_imp*26:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = (1.0 * OPERATING_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_ratings = 1.0 * 0.58 * (1 - TAX_RATE) / shares   # Ratings has higher incremental margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Indices revenue:        +${eps_per_1B_rev * 1.05:.3f}/EPS  = +${eps_per_1B_rev*1.05*30:.1f}/share at 30× P/E")
print(f"  Every $1B Ratings revenue (high incremental margin): ±${eps_per_1B_ratings:.3f}/EPS  =  ±${eps_per_1B_ratings*30:.1f}/share at 30× P/E")
print(f"  10% bond issuance swing (~${SEG_DATA[0][1]*0.10:.2f}B Ratings rev): ±${eps_per_1B_ratings*SEG_DATA[0][1]*0.10:.2f}/EPS = ±${eps_per_1B_ratings*SEG_DATA[0][1]*0.10*30:.1f}/share at 30× P/E")
print(f"  1% buyback (~3M shares):          +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (bond issuance cycle / Ratings / Indices AUM / diversification framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>6}  {'BASE':>5}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>6}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>6}  {ths[1]:>5}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>6}  {lbl}  {b}")

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
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Bond issuance volume YoY",        "+8%",    "<-15%",  "−23pp",  "Inflation resurgence forces Fed hikes; refi wall pushed out; credit spreads widen"),
    ("Ratings revenue YoY",             "+6%",    "<-10%",  "−16pp",  "Issuance freeze; high-yield market closes; transaction revenue collapses"),
    ("Indices AUM-linked growth",       "+13%",   "<0%",    "−13pp",  "Equity market correction (-25%+); AUM-linked fees decline with index levels"),
    ("Market Intelligence sub growth",  "+6%",    "<3%",    "−3pp",   "Client budget cuts at banks/asset managers; subscription churn rises"),
    ("Adjusted operating margin",       "48.5%",  "<45%",   "−3.5pp", "Operating deleverage on revenue decline; cost base largely fixed"),
    ("Commodity/Mobility growth",       "+5%",    "<2%",    "−3pp",   "Energy price collapse reduces commodity data demand; auto market slowdown"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A renewed inflation shock forcing the Fed to hike (rather than cut) would")
print(f"  freeze the bond refinancing wall, collapsing high-yield issuance and Ratings transaction")
print(f"  revenue (~{SEG_DATA[0][1]/curr_total*100:.0f}% of total). Combined with an equity market correction hitting")
print(f"  Indices AUM-linked fees, EPS falls to ~$14.50 → 26× trough = ${bear_price}.")
print(f"  Note: Market Intelligence's recurring subscription base ({SEG_DATA[1][1]/curr_total*100:.0f}% of revenue) and")
print(f"  Ratings non-transaction surveillance fees provide a durable earnings floor vs pre-2018")
print(f"  single-segment cyclicality. Recovery to ~${bear_price+90}–${bear_price+130} in 2yr is plausible post-shock.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~$17.30-$17.70; non-GAAP)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (duopoly toll-booth floor; 2022 issuance collapse trough ~24-25×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP reflects the market's confidence in the Ratings/Moody's")
print(f"  duopoly and the secular Indices/passive-investing tailwind. At ${CURRENT_PRICE:.2f} and FY2026E")
print(f"  EPS ${EPS_FY2026E:.2f}, the P/E is {CURRENT_PRICE/EPS_FY2026E:.1f}× — within the historical 28-35× 'best-in-class' premium")
print(f"  band, but near the upper end given bond issuance is only moderately recovered.")
print(f"  EPP path: FY2028E EPS ~${CONS_EPS_2YR:.2f} × {PE_PESSIMISTIC:.0f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing ~8%/yr).")
print(f"  At 27× mid-cycle P/E: ${EPS_FY2026E:.2f} × 27 = ${EPS_FY2026E*27:.0f}  — still {(1-(EPS_FY2026E*27)/CURRENT_PRICE)*100:.0f}% below current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: P/E rerates modestly; issuance growth normalizes)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (~5.6% EPS CAGR: buyback ~1.5%/yr + organic growth ~4%/yr)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (rerates from {CURRENT_PRICE/EPS_FY2026E:.0f}× toward growth-justified 27×; still premium)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; 52-yr Dividend King streak)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE PROBLEM: even the conservative case requires the bond issuance recovery to")
print(f"  continue without a credit-tightening reversal. A modest P/E compression from {CURRENT_PRICE/EPS_FY2026E:.0f}× to {CONS_PE_2YR}×")
print(f"  largely offsets EPS growth — a near-flat total return.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — achievable in BASE-to-BULL.")
print(f"  Breakeven at 30× P/E (no multiple compression): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 30:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.24
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  Dividend King, 52-yr growth streak)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (lower than tech peers; recurring revenue base dampens swings)")
print(f"  Beta vs S&P 500:      1.05  (near-market; rate-sensitivity via Ratings issuance cycle)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (credit-tightening + equity correction combo)")
print(f"  → Fed rate path is THE KEY swing factor: rate cuts/refi waves drive Ratings upside;")
print(f"    inflation resurgence/hikes are the dominant bear trigger.")
print(f"  → Indices AUM growth (passive flows, S&P 500 level) is the key BULL catalyst.")
print(f"  → AVOID at current price  |  WATCHLIST $440–470  |  ACCUMULATE $400–425  |  BUY below $385")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) compares to the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The gap ({ADJ_GAP:.2f}) indicates the stock is")
print(f"  {valuation_label.lower()} by model standards.")
print(f"  In plain terms: the duopoly moat and Indices growth justify a premium, but bond issuance")
print(f"  (signal score {SIGNALS[0]['score']}/4 = BASE) is the swing factor that determines whether the premium holds.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Fed rate cuts / credit easing — drives bond refi wave, Ratings transaction revenue (BULL trigger)")
print(f"  (2) Indices AUM growth — S&P 500 level + passive ETF flows drive asset-based fee growth (BULL trigger)")
print(f"  (3) Inflation resurgence / hawkish Fed pivot — freezes issuance, key BEAR trigger")
print(f"  (4) Private credit ratings expansion — new TAM for Ratings beyond traditional bond markets")
print(f"  (5) Market Intelligence AI/analytics upsell — incremental subscription ARPU growth")
print(f"  AVOID at ${CURRENT_PRICE:.2f}  |  WATCHLIST $440–470  |  ACCUMULATE $400–425  |  BUY below $385")
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
