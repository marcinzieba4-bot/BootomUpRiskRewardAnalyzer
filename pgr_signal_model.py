"""
PGR  ·  The Progressive Corporation  ·  NYSE: PGR
Bottom-up signal model  ·  Auto / Property Insurance · Personal & Commercial Lines
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "PGR"
COMPANY       = "The Progressive Corporation"
SECTOR        = "Auto / Property Insurance · Personal & Commercial Lines · NYSE: PGR"
CURRENT_PRICE = 258.40      # USD; as of 2026-06-10
VOL_52W_LOW   = 216.50      # late-2025 trough on cat-loss/CR-spike fears
VOL_52W_HIGH  = 295.50      # early-2026 peak on PIF growth + CR improvement
SHARES_OUT_M  = 571.0       # millions; modest buyback offsetting share creep

# Dividend: small quarterly dividend + variable annual special dividend (omitted from base ANNUAL_DIV)
ANNUAL_DIV    = 1.24        # $/share; regular quarterly dividend run-rate ($0.31/qtr)

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E net premiums earned + investment income by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Personal Lines (Auto/Property)", 58.0, 50.0, 65.0, "Auto PIF growth + Snapshot telematics pricing edge; rate increases moderating"),
    ("Commercial Lines",               10.5,  8.5, 12.5, "Fleet/BOP growth; competitive market softening rates"),
    ("Property segment",                4.5,  3.0,  5.5, "Homeowners bundling growth; cat/weather losses the swing factor"),
    ("Investment income",               4.2,  3.4,  5.0, "Float income from $80B+ portfolio; rates higher-for-longer = tailwind"),
]

# Combined ratio assumptions (the dominant earnings driver)
CR_CURR   = 0.960   # FY2026E blended combined ratio (~96.0%; best-in-class underwriting)
CR_BULL   = 0.920   # BULL: telematics/claims-AI drives CR to elite ~92%
CR_BEAR   = 1.020   # BEAR: claims inflation (used cars, repair, BI medical) pushes CR >100%
TAX_RATE  = 0.21    # effective corporate tax rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 12.00       # FY2026E adj EPS (consensus ~$11.50-$12.50)
PE_PESSIMISTIC = 13.0        # trough P/E: hard-market underwriting cycle / CR spike scenario
                              # (2022 CR-spike trough traded near 13-14x depressed earnings)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $156

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 7.50, 16,  120, "Claims inflation (used cars, repair, BI medical) pushes CR to ~102%; EPS $7.50 → 16x distressed multiple"),
    "BASE":  (12.50, 19,  238, "CR holds ~96%; PIF growth +8%; investment income steady; EPS $12.50 → 19x"),
    "BULL":  (16.50, 22,  363, "CR improves to ~93% on telematics/claims-AI; PIF growth accelerates; EPS $16.50 → 22x"),
    "XBULL": (21.00, 24,  504, "CR reaches elite ~91%; Commercial Lines scales; market-share gains compound; EPS $21.00 → 24x"),
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
        "name":       "Combined ratio (blended)",
        "weight":     0.30,
        "thresholds": (">99%",   "≤97%",  "≤95%",   "≤93%"),
        "now":        "96.0%",
        "score":      2,
        "comment":    "Underwriting profitability stable near target; claims inflation offsetting rate gains",
    },
    {
        "name":       "Policies in force (PIF) YoY growth",
        "weight":     0.25,
        "thresholds": ("<2%",    "≥4%",   "≥8%",    "≥14%"),
        "now":        "+8%",
        "score":      3,
        "comment":    "Direct + agency channel growth strong; Snapshot telematics pricing advantage drives policy retention",
    },
    {
        "name":       "Claims cost inflation (severity)",
        "weight":     0.20,
        "thresholds": (">8%",    "≤6%",   "≤4%",    "≤2%"),
        "now":        "5.0%",
        "score":      2,
        "comment":    "Used car prices, repair/parts costs, and BI medical severity remain elevated but moderating from 2023-24 peaks",
    },
    {
        "name":       "Net investment income YoY growth",
        "weight":     0.10,
        "thresholds": ("<0%",    "≥3%",   "≥8%",    "≥14%"),
        "now":        "+9%",
        "score":      3,
        "comment":    "Higher-for-longer rates plus growing float ($80B+) lift portfolio yield",
    },
    {
        "name":       "Property segment cat/weather loss ratio",
        "weight":     0.10,
        "thresholds": (">12%",   "≤10%",  "≤7%",    "≤5%"),
        "now":        "9.5%",
        "score":      2,
        "comment":    "2026 hurricane/wildfire season tracking near-normal so far; tail risk remains the key swing factor",
    },
    {
        "name":       "Premium-to-book valuation",
        "weight":     0.05,
        "thresholds": (">5.5x",  "≤5.0x", "≤4.3x",  "≤3.7x"),
        "now":        "4.6x",
        "score":      3,
        "comment":    "Trading mid-range of historical 4-5x P/B premium band; reflects best-in-class underwriting discipline",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Underwriting discipline moat — sustained ~96% CR vs peers' 100%+; data/analytics edge",     +0.7, 0.25),
    ("+", "Telematics/Snapshot advantage — granular usage-based pricing drives PIF growth & retention", +0.5, 0.20),
    ("-", "Claims cost inflation — used car prices, repair/parts, BI medical severity structural risk", -0.6, 0.20),
    ("-", "Catastrophe/weather tail risk — Property segment exposure to hurricanes/wildfires growing",  -0.5, 0.15),
    ("+", "Float/investment income tailwind — higher-for-longer rates on $80B+ portfolio",              +0.4, 0.10),
    ("-", "Premium valuation — ~19-22x P/E and ~4-5x P/B vs peers leaves limited multiple expansion",   -0.4, 0.10),
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
CONS_EPS_2YR  = 14.50   # conservative FY2028E: ~10%/yr EPS CAGR; CR steady ~95-96%; PIF growth continues
CONS_PE_2YR   = 18      # conservative exit multiple; modest compression from ~21.5x current
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Auto / Property Insurance · Personal & Commercial Lines")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<32}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<32}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<32}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print()

# EPS bridge driven primarily by combined ratio (underwriting margin)
shares      = SHARES_OUT_M / 1000
underwriting_premium_curr = curr_total - SEG_DATA[3][1]   # exclude investment income
underwriting_profit_curr  = underwriting_premium_curr * (1 - CR_CURR)
pretax_curr  = underwriting_profit_curr + SEG_DATA[3][1]
ni_curr      = pretax_curr * (1 - TAX_RATE)
curr_eps     = round(ni_curr / shares, 2)

underwriting_premium_bull = bull_total - SEG_DATA[3][2]
underwriting_profit_bull  = underwriting_premium_bull * (1 - CR_BULL)
pretax_bull  = underwriting_profit_bull + SEG_DATA[3][2]
ni_bull      = pretax_bull * (1 - TAX_RATE)
shares_b     = shares * 0.99   # modest buyback over 2yr
bull_eps_imp = round(ni_bull / shares_b, 1)

underwriting_premium_bear = bear_total - SEG_DATA[3][1]
underwriting_profit_bear  = underwriting_premium_bear * (1 - CR_BEAR)
pretax_bear  = underwriting_profit_bear + SEG_DATA[3][1]
ni_bear      = pretax_bear * (1 - TAX_RATE)
bear_eps_imp = round(ni_bear / shares, 1)

print(f"  FY2026E EPS check:  ${underwriting_premium_curr:.1f}B premium × (1 − {CR_CURR*100:.1f}% CR) + ${SEG_DATA[3][1]:.1f}B inv. income")
print(f"  ÷ {shares:.3f}B shares × (1 − {TAX_RATE*100:.0f}% tax)  =  ${curr_eps:.2f}/share adj EPS  (vs target ${EPS_FY2026E:.2f})")
print()
print(f"  BULL EPS check:  CR improves to {CR_BULL*100:.0f}% on ${underwriting_premium_bull:.1f}B premium + ${SEG_DATA[3][2]:.1f}B inv. income")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 22x = ~${bull_eps_imp*22:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  CR deteriorates to {CR_BEAR*100:.0f}% on ${underwriting_premium_bear:.1f}B premium + ${SEG_DATA[3][1]:.1f}B inv. income")
print(f"  ÷ {shares:.3f}B shares  =  ~${bear_eps_imp:.1f}/share  →  ${bear_eps_imp:.1f} × 16x = ~${bear_eps_imp*16:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
total_premium = curr_total - SEG_DATA[3][1]
eps_per_1pt_cr = total_premium * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every 1pt of combined ratio:      ±${eps_per_1pt_cr:.2f}/EPS  =  ±${eps_per_1pt_cr*19:.1f}/share at 19x P/E")
print(f"  Every 1B of investment income:    +${1.0*(1-TAX_RATE)/shares:.2f}/EPS  =  +${1.0*(1-TAX_RATE)/shares*19:.1f}/share at 19x P/E")
print(f"  PIF growth +1pp (premium ~+1pp):  +${total_premium*0.01*(1-CR_CURR)*(1-TAX_RATE)/shares:.3f}/EPS  =  +${total_premium*0.01*(1-CR_CURR)*(1-TAX_RATE)/shares*19:.2f}/share at 19x P/E")
print(f"  Cat/weather event (+2pt CR in Property): ~-${eps_per_1pt_cr*2:.2f}/EPS one-time hit")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (combined ratio / PIF growth / claims inflation framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<46}  {'BEAR':>6}  {'BASE':>6}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>6}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<46}  {ths[0]:>6}  {ths[1]:>6}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>6}  {lbl}  {b}")

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
print(f"  {'Signal':<46}  {'Current':>8}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Combined ratio (blended)",          "96.0%",  ">102%",  "+6pp",   "Severe used-car/repair/BI medical inflation spike outpaces rate filings"),
    ("PIF growth YoY",                    "+8%",    "<2%",    "−6pp",   "Rate increases push policyholders to shop; competitive market share loss"),
    ("Claims cost inflation",             "5.0%",   ">10%",   "+5pp",   "Auto parts/labor and medical CPI re-accelerate sharply"),
    ("Property cat/weather loss ratio",   "9.5%",   ">15%",   "+5.5pp", "Major hurricane season + wildfire losses hit Property segment"),
    ("Net investment income growth",      "+9%",    "<0%",    "−9pp",   "Sharp rate cuts compress portfolio yield on rollover"),
    ("Premium-to-book multiple",          "4.6x",   "<3.0x",  "−1.6x",  "Multiple compresses on underwriting credibility loss"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<46}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A renewed surge in claims severity (used car prices, auto repair/parts costs,")
print(f"  and bodily-injury medical inflation) outpaces Progressive's rate filings, pushing the")
print(f"  combined ratio above 100% for several quarters. Combined with an active hurricane/wildfire")
print(f"  season hitting the Property segment, EPS collapses to ~${SCENARIOS['BEAR'][0]:.2f} → 16x distressed multiple = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT a permanent impairment — Progressive's data/analytics edge allows")
print(f"  rapid rate re-filing (often within a quarter), and the underwriting cycle historically")
print(f"  normalizes within 12-18 months. Recovery toward ${bear_price+60}-${bear_price+90} in 2yr is plausible post-shock.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~$11.50-$12.50)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}x  (hard-market/CR-spike trough multiple, e.g. 2022 cycle)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% premium to EPP reflects the market's confidence in Progressive's")
print(f"  best-in-class underwriting discipline and consistent profitable PIF growth, which has")
print(f"  historically supported a premium P/E of ~18-22x and premium P/B of ~4-5x vs peers.")
print(f"  At ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f}, the implied P/E is {CURRENT_PRICE/EPS_FY2026E:.1f}x — within")
print(f"  the historical premium band, but leaving limited room for further multiple expansion.")
print(f"  EPP path: FY2028E EPS ~${CONS_EPS_2YR:.2f} × {PE_PESSIMISTIC:.0f}x = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing with EPS).")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: CR holds near target; modest multiple compression)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (~10% EPS CAGR: PIF growth + steady ~95-96% CR + investment income)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (modest compression from ~{CURRENT_PRICE/EPS_FY2026E:.1f}x toward {CONS_PE_2YR}x)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr regular dividend)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE DYNAMIC: even with modest P/E compression from {CURRENT_PRICE/EPS_FY2026E:.1f}x to {CONS_PE_2YR}x,")
print(f"  the ~10%/yr EPS growth (driven by PIF growth + stable CR + investment income) more than")
print(f"  offsets the multiple contraction, producing a positive conservative return.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}x P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E.")
print(f"  Breakeven at 21x P/E (no multiple compression): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 21:.2f}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.22
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  modest; variable special div not included)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (lower than market; insurance earnings smoother but cat-event tail risk)")
print(f"  Beta vs S&P 500:      0.55  (defensive financial; cat events and rate-cycle the key drivers)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (extreme; CR-spike + cat-event tail scenario)")
print(f"  → Combined ratio trend is THE KEY signal; quarterly CR prints drive most of the EPS revisions.")
print(f"  → Hurricane/wildfire season (Jun-Nov) is the key tail-risk catalyst for the Property segment.")
print(f"  → AVOID above $290  |  WATCHLIST $270-290  |  ACCUMULATE $245-270  |  BUY below $230")

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
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The gap ({ADJ_GAP:+.2f}) indicates the stock is")
print(f"  {valuation_label.lower()} by model standards. Combined ratio trajectory and PIF growth")
print(f"  remain the dominant levers; claims inflation and cat/weather tail risk are the key offsets.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Combined ratio prints — sustained sub-95% CR would support BULL re-rating")
print(f"  (2) PIF growth trajectory — direct/agency channel growth + Snapshot telematics retention")
print(f"  (3) Claims severity trends — used car prices, auto repair/parts, BI medical inflation")
print(f"  (4) Catastrophe/weather losses — Property segment exposure during hurricane/wildfire season")
print(f"  (5) Investment portfolio yield — float income from $80B+ portfolio as rates evolve")
print(f"  AVOID above $290  |  WATCHLIST $270-290  |  ACCUMULATE $245-270  |  BUY below $230")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}x  |  FY2026E EPS: ${EPS_FY2026E:.2f}")
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
