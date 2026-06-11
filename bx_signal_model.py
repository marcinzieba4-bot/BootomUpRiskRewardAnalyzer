"""
BX  ·  Blackstone Inc.  ·  NYSE: BX
Bottom-up signal model  ·  Alternative Asset Management / Real Estate / PE / Credit & Insurance
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "BX"
COMPANY       = "Blackstone Inc."
SECTOR        = "Alternative Asset Management · Real Estate · PE · Credit & Insurance · NYSE: BX"
CURRENT_PRICE = 152.40       # USD; as of 2026-06-11
VOL_52W_LOW   = 118.30       # 2025 rate-fear / commercial real estate trough
VOL_52W_HIGH  = 168.95       # 2026 realization-recovery / private wealth fundraising peak
SHARES_OUT_M  = 1_410.0      # millions; common shares outstanding (incl. partnership units economics)

# Dividend: variable, tied to distributable earnings (DE); ~80% payout
ANNUAL_DIV    = 3.60         # $/share FY2026E (quarterly variable distribution)

# ── SEGMENT REVENUE BRIDGE (FRE + Performance Revenue drivers) ────────────────
# FY2026E Total Segment Revenue by business ($B) — combines management fees (FRE)
# and performance revenues (carry/incentive fees), the cyclical swing factor
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Real Estate",              4.20, 2.90, 5.60, "Largest legacy segment; higher-for-longer rates pressure CRE values & realizations"),
    ("Private Equity",           3.10, 2.10, 4.60, "Corporate PE + tactical opps/secondaries; M&A/IPO recovery drives carry realizations"),
    ("Credit & Insurance",       3.60, 3.00, 4.80, "Fastest-growing FRE base; Corebridge & insurance permanent capital; investment-grade credit"),
    ("Hedge Fund Solutions / MAI",1.30, 1.05, 1.65, "BAAM multi-strategy/multi-manager; steadier fee stream, modest performance fee component"),
]

# FRE / Performance Revenue split assumptions
FRE_MARGIN_CURR   = 0.57   # blended Fee-Related Earnings margin on fee revenue (~57%)
FRE_MARGIN_BULL   = 0.60   # operating leverage as AUM scales (perpetual capital growth)
PERF_REV_SHARE_CURR = 0.22 # performance revenue as % of total segment revenue, current (subdued realizations)
PERF_REV_SHARE_BULL = 0.34 # performance revenue share in BULL (M&A/IPO window reopens; large carry crystallization)
PERF_REV_SHARE_BEAR = 0.10 # performance revenue share in BEAR (realization drought)
PERF_MARGIN        = 0.85  # performance revenue flows through at high margin (comp accrual netted)
OPEX_OTHER_B       = 1.20  # corporate / other unallocated costs ($B)
TAX_RATE           = 0.07  # effective corporate tax rate post-2019 C-corp conversion (low due to FPI/intangibles)

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 4.95        # FY2026E adj/distributable EPS estimate (consensus $4.85-$5.05)
PE_PESSIMISTIC = 16.0        # trough P/E: realization drought + retail redemption stress (2023 trough ~15-17x)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # ~$79

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 3.30, 16,   53, "Realization drought persists; BREIT/BCRED redemptions accelerate; CRE marks fall further; EPS $3.30 → 16× floor"),
    "BASE":  ( 5.60, 26,  146, "FRE compounds at low-teens; performance fees normalize gradually as deal activity recovers; EPS $5.60 at FY2028E → 26×"),
    "BULL":  ( 7.80, 32,  250, "M&A/IPO window reopens; large carry crystallizations across PE & RE; private wealth inflows accelerate; EPS $7.80 → 32×"),
    "XBULL": (10.50, 36,  378, "Multi-year realization super-cycle; insurance/permanent capital AUM doubles; FRE margin expands to 65%+; EPS $10.50 → 36×"),
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
        "name":       "Total AUM growth YoY",
        "weight":     0.20,
        "thresholds": ("<3%",    "≥6%",   "≥10%",   "≥15%"),
        "now":        "+9%",
        "score":      2,
        "comment":    "AUM ~$1.18T; inflows broad-based across credit/insurance & private wealth; approaching BULL threshold",
    },
    {
        "name":       "Fee-Related Earnings (FRE) growth YoY",
        "weight":     0.25,
        "thresholds": ("<5%",    "≥8%",   "≥13%",   "≥18%"),
        "now":        "+12%",
        "score":      2,
        "comment":    "Management fees on perpetual capital compounding steadily; Credit & Insurance the main driver",
    },
    {
        "name":       "Performance revenue / realization activity",
        "weight":     0.25,
        "thresholds": ("<-20%",  "≥0%",   "≥+30%",  "≥+60%"),
        "now":        "+8%",
        "score":      2,
        "comment":    "Realizations recovering off a depressed base but M&A/IPO markets not yet fully open; carry recognition lumpy",
    },
    {
        "name":       "Real Estate dry powder deployment / RE NAV trend",
        "weight":     0.15,
        "thresholds": ("declining", "flat", "rising mod.", "rising strong"),
        "now":        "flat",
        "score":      2,
        "comment":    "CRE values stabilizing but higher-for-longer rates cap appreciation; BREIT redemptions moderating",
    },
    {
        "name":       "Private wealth / perpetual capital fundraising (BREIT/BCRED, etc.)",
        "weight":     0.10,
        "thresholds": ("net outflows", "flat/small inflow", "solid net inflow", "record inflow"),
        "now":        "solid net inflow",
        "score":      3,
        "comment":    "Retail channel inflection positive; BCRED & private wealth credit vehicles gathering net new assets again",
    },
    {
        "name":       "FRE margin",
        "weight":     0.05,
        "thresholds": ("<53%",   "≥55%",  "≥58%",   "≥62%"),
        "now":        "57%",
        "score":      2,
        "comment":    "Operating leverage from scale; margin steady near mid-cycle level, room to expand with AUM growth",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Permanent/perpetual capital base — Credit & Insurance + perpetual RE/credit vehicles de-risk AUM",  +0.6, 0.20),
    ("+", "Private wealth channel structural tailwind — BREIT/BCRED retail distribution scaling globally",     +0.5, 0.20),
    ("-", "Realization drought risk — extended low-exit environment starves performance fee earnings",         -0.7, 0.20),
    ("-", "Commercial real estate overhang — higher-for-longer rates cap RE segment NAV recovery",              -0.5, 0.15),
    ("+", "Premium franchise / scale moat — $1.1T+ AUM, brand, fundraising machine, fee-stream visibility",    +0.4, 0.15),
    ("-", "Valuation premium risk — distributable-earnings P/E near top of historical range; multiple compression risk", -0.3, 0.10),
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
CONS_EPS_2YR  = 5.60    # conservative FY2028E: gradual realization recovery + FRE compounding
CONS_PE_2YR   = 24      # rerating from current ~31× toward growth-justified 24×
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Alternative Asset Management / RE / PE / Credit & Insurance")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios; Total Segment Revenue, $B)")
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

# EPS bridge: split each scenario's revenue into FRE-driven fee revenue + performance revenue
fee_curr   = curr_total * (1 - PERF_REV_SHARE_CURR)
perf_curr  = curr_total * PERF_REV_SHARE_CURR
fre_ni     = fee_curr * FRE_MARGIN_CURR
perf_ni    = perf_curr * PERF_MARGIN
curr_pretax = fre_ni + perf_ni - OPEX_OTHER_B
curr_ni    = curr_pretax * (1 - TAX_RATE)
shares     = SHARES_OUT_M / 1000
curr_eps   = round(curr_ni / shares, 2)

fee_bull   = bull_total * (1 - PERF_REV_SHARE_BULL)
perf_bull  = bull_total * PERF_REV_SHARE_BULL
bull_fre_ni  = fee_bull * FRE_MARGIN_BULL
bull_perf_ni = perf_bull * PERF_MARGIN
bull_pretax  = bull_fre_ni + bull_perf_ni - OPEX_OTHER_B
bull_ni      = bull_pretax * (1 - TAX_RATE)
shares_b     = shares * 0.97   # modest share count reduction over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

fee_bear   = bear_total * (1 - PERF_REV_SHARE_BEAR)
perf_bear  = bear_total * PERF_REV_SHARE_BEAR
bear_fre_ni  = fee_bear * (FRE_MARGIN_CURR * 0.97)
bear_perf_ni = perf_bear * PERF_MARGIN
bear_pretax  = bear_fre_ni + bear_perf_ni - OPEX_OTHER_B * 0.95
bear_ni      = max(0, bear_pretax) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.2f}B total rev  →  fee rev ${fee_curr:.2f}B × {FRE_MARGIN_CURR*100:.0f}% FRE margin")
print(f"  + perf rev ${perf_curr:.2f}B × {PERF_MARGIN*100:.0f}% margin − ${OPEX_OTHER_B:.2f}B opex − {TAX_RATE*100:.0f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  fee rev ${fee_bull:.2f}B × {FRE_MARGIN_BULL*100:.0f}% + perf rev ${perf_bull:.2f}B × {PERF_MARGIN*100:.0f}% − opex − tax")
print(f"  ÷ {shares_b:.3f}B shares  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 32× = ~${bull_eps_imp*32:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  fee rev ${fee_bear:.2f}B (margin {FRE_MARGIN_CURR*0.97*100:.0f}%) + perf rev ${perf_bear:.2f}B (drought) − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 16× trough P/E (FRE floor) = ~${bear_eps_imp*16:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Credit & Insurance fee revenue:  +${1.0*FRE_MARGIN_CURR*(1-TAX_RATE)/shares:.3f}/EPS  = +${1.0*FRE_MARGIN_CURR*(1-TAX_RATE)/shares*26:.1f}/share at 26× P/E")
print(f"  Performance revenue ±$1B (85% margin):     ±${1.0*PERF_MARGIN*(1-TAX_RATE)/shares:.3f}/EPS  =  ±${1.0*PERF_MARGIN*(1-TAX_RATE)/shares*26:.1f}/share at 26× P/E")
print(f"  1pp FRE margin expansion (scale leverage):  +${fee_curr*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${fee_curr*0.01*(1-TAX_RATE)/shares*26:.1f}/share at 26× P/E")
print(f"  10pp shift in performance-revenue share:    ~${curr_total*0.10*(PERF_MARGIN-FRE_MARGIN_CURR)*(1-TAX_RATE)/shares:.2f}/EPS swing  (realization cycle is THE swing factor)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (AUM growth / FRE / realization activity / RE NAV / fundraising / margin)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>14}  {'BASE':>14}  {'BULL':>14}  {'XBULL':>14}  {'NOW':>17}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>14}  {ths[1]:>14}  {ths[2]:>14}  {ths[3]:>14}  {s['now']:>17}  {lbl}  {b}")

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
print(f"  {'Signal':<52}  {'Current':>14}  {'Bear val':>14}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Total AUM growth YoY",                      "+9%",            "<3%",        "−6pp",   "Sustained net outflows from perpetual capital vehicles + asset depreciation"),
    ("Performance revenue / realization act.",    "+8%",            "<-20%",      "−28pp",  "M&A/IPO markets remain shut for 2+ yrs; near-zero carry crystallization"),
    ("Real Estate NAV trend",                      "flat",           "declining",  "↓",      "Renewed cap-rate expansion; CRE values mark down another 10-15%"),
    ("Private wealth fundraising",                 "solid net inflow","net outflows","↓↓",   "BREIT/BCRED redemption requests exceed gates; retail confidence breaks"),
    ("Fee-Related Earnings growth",                "+12%",           "<5%",        "−7pp",   "Fee-rate compression + AUM stagnation across flagship funds"),
    ("FRE margin",                                  "57%",            "<53%",       "−4pp",   "Cost discipline fails to offset revenue stagnation; opex grows faster than fees"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>14}  {bear_v:>14}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A prolonged realization drought — M&A and IPO markets stay closed,")
print(f"  preventing PE and Real Estate exits — combined with continued higher-for-longer")
print(f"  rates keeping CRE values depressed. Performance revenue collapses toward near-zero")
print(f"  while BREIT/BCRED face renewed redemption pressure from retail investors. FRE base")
print(f"  remains the floor (management fees on perpetual capital persist), but EPS falls to")
print(f"  ~${bear_price/PE_PESSIMISTIC:.2f} → 16× floor P/E = ${bear_price}.")
print(f"  Note: the FRE base ({fee_curr:.1f}B fee revenue at {FRE_MARGIN_CURR*100:.0f}% margin) is largely contractual/")
print(f"  recurring — providing a durable earnings floor. Recovery to ~${bear_price+40}-${bear_price+70} in 2yr")
print(f"  is base case once realization activity normalizes.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj/distributable EPS estimate:  ${EPS_FY2026E:.2f}  (consensus $4.85-$5.05)")
print(f"  Pessimistic P/E at trough:                {PE_PESSIMISTIC:.0f}×  (2023 realization-drought trough ~15-17×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP means the market prices in continued AUM growth")
print(f"  and a recovering realization cycle ABOVE the trough-floor multiple. At ${CURRENT_PRICE:.2f}")
print(f"  and FY2026E EPS ${EPS_FY2026E:.2f}, the implied P/E is {CURRENT_PRICE/EPS_FY2026E:.1f}× — Blackstone's premium")
print(f"  'growth-like' multiple reflecting AUM compounding + fee margin expansion + permanent")
print(f"  capital optionality. The risk is a realization drought re-rating the multiple toward")
print(f"  the trough floor.")
print(f"  EPP path: FY2028E EPS ~${EPS_FY2026E*1.10:.2f} × {PE_PESSIMISTIC:.0f}× = ${EPS_FY2026E*1.10*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing ~10%/yr with FRE compounding).")
print(f"  At 24× mid-cycle P/E: ${EPS_FY2026E:.2f} × 24 = ${EPS_FY2026E*24:.0f}  — {'below' if EPS_FY2026E*24 < CURRENT_PRICE else 'above'} current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: P/E rerates toward mid-cycle; gradual realization recovery)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (FRE compounding low-teens + gradual perf-fee recovery)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (rerates from ~{CURRENT_PRICE/EPS_FY2026E:.0f}× toward growth-justified {CONS_PE_2YR}×)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; variable distribution ~80% payout)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: can FRE compounding + a gradual realization recovery offset any")
print(f"  multiple normalization from the current premium valuation?")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E.")
print(f"  Breakeven at 28× P/E (modest multiple compression): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 28:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}-${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.32
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  -  variable, tied to distributable earnings)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (alt-asset managers carry beta to capital markets/realization cycle)")
print(f"  Beta vs S&P 500:      1.45  (high; cyclical performance-fee earnings amplify market swings)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe but plausible in a deep realization drought)")
print(f"  52W low ${VOL_52W_LOW:.2f} reflects rate-fear / CRE-value concerns from 2025.")
print(f"  -> Realization cycle (M&A/IPO activity) is THE KEY swing factor for performance revenue.")
print(f"  -> Private wealth net inflows (BREIT/BCRED) and Credit & Insurance FRE growth are KEY bull catalysts.")
print(f"  -> AVOID at current price  |  WATCHLIST $130-145  |  ACCUMULATE $110-125  |  BUY below $100")

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
print(f"  Downside  (-> Bear ${bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (-> Bull ${bull_price}):  {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b_str}")
print(f"  Signal    :  {signal_full}")
print()
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) compares to the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0.")
print(f"  The model scores the fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0.")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  Realization-cycle recovery (performance revenue signal) is the most significant swing factor.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) M&A/IPO market reopening — drives performance revenue realizations across PE & RE (BULL trigger)")
print(f"  (2) Credit & Insurance growth — Corebridge & insurance permanent capital scaling FRE base")
print(f"  (3) Private wealth fundraising — BREIT/BCRED net flows turning sustainably positive")
print(f"  (4) Real estate NAV stabilization/recovery as rate-cut cycle progresses")
print(f"  (5) Risk: prolonged realization drought + retail redemption pressure on perpetual vehicles")
print(f"  AVOID at ${CURRENT_PRICE:.2f}  |  WATCHLIST $130-145  |  ACCUMULATE $110-125  |  BUY below $100")
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
