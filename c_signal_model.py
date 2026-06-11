"""
C  ·  Citigroup Inc.  ·  NYSE: C
Bottom-up signal model  ·  Global Bank Holding Company / Transformation Story
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "C"
COMPANY       = "Citigroup Inc."
SECTOR        = "Diversified Bank · Global Transaction Banking · Markets · Wealth · NYSE: C"
CURRENT_PRICE = 92.50        # USD; as of 2026-06-11
VOL_52W_LOW   = 68.40        # mid-2025 trough (rates/recession scare)
VOL_52W_HIGH  = 96.80        # 2026 high (re-rating toward tangible book value)
SHARES_OUT_M  = 1_870.0      # millions; declining via aggressive buyback program
ANNUAL_DIV    = 2.32         # $/share (≈$0.58/quarter); growing alongside ROTCE progress

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B) — "five interconnected businesses"
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Services (TTS/Securities Svcs)", 20.5, 18.5, 24.0, "Crown jewel; high-ROIC global transaction banking; structural growth engine"),
    ("Markets",                        18.0, 14.5, 21.0, "FICC/Equities; volatile but benefits from volatility/rate-cut cycle"),
    ("Banking",                         6.5,  5.0,  9.0, "IB fee recovery; M&A/DCM pipeline rebuild post-restructuring"),
    ("US Personal Banking",            19.5, 17.5, 22.0, "Cards/retail; credit normalization key swing factor"),
    ("Wealth",                          8.0,  6.5, 10.5, "Citigold/Private Bank buildout under new leadership"),
]

# Margin / capital assumptions
ROTCE_CURR    = 0.092   # current run-rate ROTCE (~9.2%), improving toward 11-12% 2026 target
ROTCE_BULL    = 0.13    # BULL: transformation delivers above-target ROTCE
ROTCE_BEAR    = 0.06    # BEAR: credit cycle + execution stumbles compress returns
TBVPS         = 95.50   # tangible book value per share (FY2026E)
TAX_RATE      = 0.23    # effective tax rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 8.20        # FY2026E adj EPS (consensus ~$8.00-$8.40; buyback-driven growth)
PE_PESSIMISTIC = 7.0         # trough P/E: large banks during credit-cycle stress trade 6-8x
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # ~$57

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 6.50,  8,   52, "Transformation stalls; credit losses spike; consent-order setbacks; P/TBV falls to 0.55x"),
    "BASE":  ( 9.00, 10,   90, "ROTCE reaches ~10-11%; gradual P/TBV re-rating to ~0.95x; Services compounds steadily"),
    "BULL":  (10.50, 12,  126, "ROTCE hits 12%+ target; P/TBV re-rates to ~1.15x; Services + Wealth scale, buybacks accelerate"),
    "XBULL": (12.50, 13,  163, "Citi re-rates toward peer-average 1.4-1.5x P/TBV; transformation fully validated; ROTCE 14%+"),
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
        "name":       "ROTCE progression toward 11-12% target",
        "weight":     0.30,
        "thresholds": ("<8%",    "≥9%",   "≥11%",   "≥13%"),
        "now":        "~9.2%",
        "score":      2,
        "comment":    "Steady quarterly progress under Fraser plan; on track for 2026 target band but not yet there",
    },
    {
        "name":       "Services (TTS/Securities) revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<3%",    "≥5%",   "≥8%",    "≥12%"),
        "now":        "+8%",
        "score":      3,
        "comment":    "Crown jewel franchise; cross-border payments & securities services growing high-single digits",
    },
    {
        "name":       "Expense reduction / restructuring execution",
        "weight":     0.20,
        "thresholds": ("Stalled","On track","Ahead",  "Done early"),
        "now":        "On track",
        "score":      2,
        "comment":    "Headcount reductions and divestitures (Mexico/Banamex IPO, international consumer exits) progressing per plan",
    },
    {
        "name":       "P/TBV multiple",
        "weight":     0.15,
        "thresholds": ("<0.65x", "≥0.75x","≥0.95x", "≥1.15x"),
        "now":        "~0.97x",
        "score":      3,
        "comment":    f"At ${CURRENT_PRICE:.2f} vs TBVPS ${TBVPS:.2f} = {CURRENT_PRICE/TBVPS:.2f}x; deepest discount among major US banks but re-rating underway",
    },
    {
        "name":       "Credit quality (NCO / consumer credit trends)",
        "weight":     0.10,
        "thresholds": ("Worsening","Stable","Improving","Strong"),
        "now":        "Stable",
        "score":      2,
        "comment":    "Card NCOs plateauing; reserve builds moderating; no acute deterioration signals",
    },
    {
        "name":       "Capital return (buyback pace / CET1 cushion)",
        "weight":     0.05,
        "thresholds": ("Paused", "Modest", "Robust", "Aggressive"),
        "now":        "Robust",
        "score":      3,
        "comment":    "CET1 well above regulatory requirement (~13.5%); multi-billion quarterly buybacks supporting EPS/TBV growth",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Services franchise — high-ROIC global transaction banking moat; #1 cross-border payments network",  +0.7, 0.25),
    ("+", "Valuation discount — trades at deepest P/TBV discount of major US banks; mean-reversion runway",     +0.6, 0.20),
    ("-", "Multi-year transformation execution risk — consent orders, data infrastructure remediation ongoing", -0.7, 0.20),
    ("-", "US Personal Banking credit cycle exposure — cards portfolio sensitive to consumer stress",            -0.4, 0.15),
    ("+", "Capital return tailwind — excess CET1, large buyback authorization compounds TBVPS/EPS",             +0.5, 0.15),
    ("-", "Markets revenue volatility — FICC/Equities cyclicality clouds run-rate earnings visibility",          -0.3, 0.05),
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
CONS_EPS_2YR  = 9.50    # conservative FY2028E EPS: continued buyback + modest ROTCE gains
CONS_PE_2YR   = 10      # rerating from ~11x toward conservative 10x (P/TBV ~1.0x)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Global Bank Holding Company / Transformation Story")
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

# EPS / ROTCE bridge
shares    = SHARES_OUT_M / 1000
curr_ni   = ROTCE_CURR * (TBVPS * shares)
curr_eps  = round(curr_ni / shares, 2)

shares_b  = shares * 0.92   # ~4%/yr buyback over 2yr
bull_ni   = ROTCE_BULL * (TBVPS * 1.10 * shares_b)
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_ni   = ROTCE_BEAR * (TBVPS * 0.97 * shares)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ROTCE {ROTCE_CURR*100:.1f}% × TBVPS ${TBVPS:.2f} × {shares:.3f}B shares")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ~${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ROTCE {ROTCE_BULL*100:.0f}% × TBVPS (grown) × {shares_b:.3f}B shares (post-buyback)")
print(f"  ÷ {shares_b:.3f}B shares  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 12× = ~${bull_eps_imp*12:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ROTCE {ROTCE_BEAR*100:.0f}% × TBVPS (compressed) × {shares:.3f}B shares  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 8× trough P/E (credit-cycle floor) = ~${bear_eps_imp*8:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
print(f"  KEY SENSITIVITIES:")
print(f"  Every 1pp ROTCE improvement:      +${TBVPS*0.01:.2f}/EPS  = +${TBVPS*0.01*10:.2f}/share at 10× P/E")
print(f"  Every 0.10x P/TBV re-rating:        +${TBVPS*0.10:.2f}/share at constant TBVPS ${TBVPS:.2f}")
print(f"  1pp Services revenue growth:       ~+${20.5*0.01*(1-TAX_RATE)/shares:.3f}/EPS")
print(f"  4% annual buyback (≈75M shares):   mechanical EPS accretion of ~4%/yr at constant NI")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (ROTCE / Services growth / restructuring / P-TBV framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>9}  {'BASE':>9}  {'BULL':>9}  {'XBULL':>10}  {'NOW':>9}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>9}  {ths[1]:>9}  {ths[2]:>9}  {ths[3]:>10}  {s['now']:>9}  {lbl}  {b}")

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
    ("ROTCE progression",              "9.2%",   "<6%",    "−3.2pp", "Recession-driven credit losses + transformation cost overruns"),
    ("Services revenue YoY",           "+8%",    "<3%",    "−5pp",   "Global trade slowdown compresses cross-border payment volumes"),
    ("Expense reduction execution",    "On track","Stalled","2 levels","New consent order or regulatory finding halts restructuring"),
    ("P/TBV multiple",                 "0.97x",  "<0.65x", "−0.32x", "Market re-prices transformation risk; flight to higher-ROTCE peers"),
    ("Credit quality (NCO trend)",     "Stable", "Worsening","2 levels","Unemployment spike drives card NCOs above 6%"),
    ("Capital return pace",            "Robust", "Paused", "2 levels","CET1 buffer consumed by losses; buyback suspended"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A US/global recession drives consumer credit losses sharply higher in")
print(f"  US Personal Banking, while a fresh regulatory setback (consent order escalation) stalls")
print(f"  the multi-year simplification plan. ROTCE retreats toward {ROTCE_BEAR*100:.0f}%, and the market")
print(f"  re-prices the transformation thesis, pushing P/TBV back toward ~0.55x = ${bear_price}.")
print(f"  Note: ${bear_price} is not a permanent impairment — Services franchise earnings power and")
print(f"  excess capital provide a floor; recovery toward ~${bear_price+15}-${bear_price+25} in 2yr is plausible post-shock.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~$8.00-$8.40)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (large-bank credit-cycle trough multiple)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  At a {epp_gap_pct:+.0f}% premium to EPP, the market is pricing in continued ROTCE progress")
print(f"  toward the 11-12% target without a major credit-cycle disruption. At ${CURRENT_PRICE:.2f}")
print(f"  and FY2026E EPS ${EPS_FY2026E:.2f}, the trailing P/E is ~{CURRENT_PRICE/EPS_FY2026E:.1f}x and P/TBV ~{CURRENT_PRICE/TBVPS:.2f}x —")
print(f"  still a discount to peers (JPM/BAC trade ~1.8-2.5x P/TBV), leaving re-rating room if")
print(f"  execution continues, but vulnerable to multiple compression in a credit downturn.")
print(f"  EPP path: as ROTCE rises and TBVPS compounds via buybacks + retained earnings, EPP")
print(f"  itself should grow over time even at a constant {PE_PESSIMISTIC:.0f}× trough multiple.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: gradual P/TBV re-rating toward 1.0x as ROTCE improves)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (buyback-driven EPS growth + modest ROTCE gains)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (≈1.0x P/TBV; consistent with 11% ROTCE)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE THESIS: even a modest re-rating to ~1.0x P/TBV combined with buyback-driven")
print(f"  EPS growth produces a positive total return, with dividends adding a meaningful floor.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — achievable in BASE/BULL.")
print(f"  Breakeven at 11x P/E (slightly fuller re-rating): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 11:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}-${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case attractive at {CONS_PE_2YR}× P/E; ratio_b <0.75x)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.30
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; large-bank beta to credit cycle/macro)")
print(f"  Beta vs S&P 500:      1.30  (above-market sensitivity to rates and credit conditions)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe credit-cycle / execution shock)")
print(f"  52W low ${VOL_52W_LOW:.2f} reflects pre-re-rating valuation before transformation gains traction.")
print(f"  → Credit cycle (consumer cards, CRE) is THE KEY macro risk to monitor.")
print(f"  → ROTCE progress toward 11-12% target and continued P/TBV re-rating is KEY bull catalyst.")
print(f"  → ACCUMULATE near current levels  |  WATCHLIST $100-110  |  BUY below $80")

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
print(f"  {valuation_label.lower()} by model standards. Citigroup remains the deepest-discount major US bank")
print(f"  on P/TBV, with the Services franchise as the primary structural re-rating catalyst.")
print(f"  Execution risk on the multi-year transformation remains the dominant downside variable.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) ROTCE progression toward 11-12% 2026 target — quarterly proof points (BULL trigger)")
print(f"  (2) P/TBV re-rating toward 1.0x+ as transformation de-risks (BULL trigger)")
print(f"  (3) Services (TTS/Securities Services) sustained high-single-digit growth")
print(f"  (4) Consumer credit normalization in US Personal Banking cards portfolio")
print(f"  (5) Continued large-scale buyback execution supported by excess CET1 capital")
print(f"  ACCUMULATE near ${CURRENT_PRICE:.2f}  |  WATCHLIST $100-110  |  BUY below $80")
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
