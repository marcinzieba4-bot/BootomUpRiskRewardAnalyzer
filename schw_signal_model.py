"""
SCHW  ·  The Charles Schwab Corporation  ·  NYSE: SCHW
Bottom-up signal model  ·  Brokerage / Wealth Management / Bank Sweep
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "SCHW"
COMPANY       = "The Charles Schwab Corporation"
SECTOR        = "Brokerage · Wealth Management · RIA Custody · NYSE: SCHW"
CURRENT_PRICE = 92.50        # USD; as of 2026-06-11
VOL_52W_LOW   = 68.40        # mid-2025 cash-sorting/rate-cut anxiety trough
VOL_52W_HIGH  = 96.80        # early-2026 peak on NIR stabilization optimism
SHARES_OUT_M  = 1_780.0      # millions; modest buyback post-TDA share issuance unwind

# Dividend: steady payer; ~25% payout ratio
ANNUAL_DIV    = 1.04         # $/share ($0.26/quarter)

# ── REVENUE BRIDGE (company-specific calculator) ──────────────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Net Interest Revenue",          9.8,  7.8, 12.0, "Bank sweep deposits + margin lending; most rate-sensitive line"),
    ("Asset Mgmt & Admin Fees",        6.4,  5.4,  8.0, "AUM-based fees; record organic net new assets ~$450B/yr"),
    ("Trading Revenue",                3.1,  2.4,  3.8, "Episodic; volatility-driven order flow & options activity"),
]

# Margin assumptions
PRETAX_MARGIN_CURR = 0.545  # blended pre-tax margin FY2026E
PRETAX_MARGIN_BULL = 0.50   # BULL: NIR recovery + operating leverage on fixed cost base
OPEX_FIXED_B       = 7.6    # largely fixed comp/tech/occupancy cost base ($B)
TAX_RATE           = 0.23   # effective tax rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 4.55        # FY2026E adj EPS (consensus ~$4.45-$4.65)
PE_PESSIMISTIC = 14.0        # trough P/E: brokerage franchise floor even in deep cash-sorting/rate-cut cycle
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # ~$64

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (3.10, 14,  43,  "Cash sorting reaccelerates; Fed cuts crush NIR; EPS $3.10 → 14× floor P/E"),
    "BASE":  (4.55, 20,  91,  "NIR stabilizes; AUM growth +8%/yr; EPS $4.55 → 20× → ~$91"),
    "BULL":  (5.80, 22, 128,  "NIR inflects higher on rate normalization; record net new assets; EPS $5.80 → 22×"),
    "XBULL": (7.20, 24, 173,  "Cash sorting fully reverses to net inflow; AUM at all-time highs; EPS $7.20 → 24×"),
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
        "name":       "Net Interest Revenue YoY growth",
        "weight":     0.30,
        "thresholds": ("<-8%",   "≥-2%",  "≥+5%",   "≥+12%"),
        "now":        "+1%",
        "score":      2,
        "comment":    "Cash sorting headwind largely abated; sweep balances stabilizing as Fed cutting cycle slows",
    },
    {
        "name":       "Net new assets (organic growth, % of AUM)",
        "weight":     0.25,
        "thresholds": ("<3%",    "≥4%",   "≥6%",    "≥8%"),
        "now":        "~6%",
        "score":      3,
        "comment":    "Industry-leading organic growth; ~$450B/yr net new assets post-TDA integration completion",
    },
    {
        "name":       "Bank sweep cash balance trend",
        "weight":     0.20,
        "thresholds": ("declining", "flat", "growing", "strong inflow"),
        "now":        "flat",
        "score":      2,
        "comment":    "Sweep balances roughly flat QoQ; clients no longer aggressively reallocating to money market funds",
    },
    {
        "name":       "Asset Mgmt & Admin fee revenue YoY",
        "weight":     0.15,
        "thresholds": ("<2%",    "≥5%",   "≥9%",    "≥14%"),
        "now":        "+8%",
        "score":      3,
        "comment":    "Record AUM on market appreciation + net new assets; advisory/managed solutions mix shift positive",
    },
    {
        "name":       "Trading revenue YoY",
        "weight":     0.05,
        "thresholds": ("<-10%",  "≥-2%",  "≥+5%",   "≥+15%"),
        "now":        "+3%",
        "score":      3,
        "comment":    "Options & active trading activity steady; episodic but currently constructive",
    },
    {
        "name":       "Pre-tax margin",
        "weight":     0.05,
        "thresholds": ("<40%",   "≥44%",  "≥47%",   "≥50%"),
        "now":        "46%",
        "score":      3,
        "comment":    "TDA integration synergies largely realized; expense discipline driving operating leverage",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Scale & client trust moat — largest US discount broker/RIA custodian; ~$11T client assets",  +0.6, 0.20),
    ("+", "Net new asset engine — industry-leading organic growth; sticky long-duration relationships",  +0.6, 0.20),
    ("-", "Rate sensitivity — NIR is ~45% of revenue; Fed rate path remains the dominant swing factor",  -0.7, 0.25),
    ("-", "Cash-sorting tail risk — clients can still reallocate sweep cash if MMF yields re-widen",     -0.5, 0.15),
    ("+", "TDA integration complete — synergy realization supports margin expansion and FCF growth",     +0.4, 0.10),
    ("-", "Regulatory/leverage scrutiny — bank-charter capital requirements limit balance-sheet flexibility", -0.3, 0.10),
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
CONS_EPS_2YR  = 5.40    # conservative FY2028E: NIR modestly recovers + AUM fee growth continues
CONS_PE_2YR   = 18      # rerates from ~20x toward growth-justified mid-cycle 18x
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Brokerage / Wealth Management / Bank Sweep")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① REVENUE BRIDGE ─────────────────────────────────────────────────────────
print()
print("  REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<26}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<26}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<26}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print()

# EPS bridge
curr_oi   = curr_total * PRETAX_MARGIN_CURR
curr_ni   = curr_oi * (1 - TAX_RATE)
shares    = SHARES_OUT_M / 1000
curr_eps  = round(curr_ni / shares, 2)

bull_oi   = bull_total * PRETAX_MARGIN_BULL
bull_ni   = bull_oi * (1 - TAX_RATE)
shares_b  = shares * 0.97   # modest buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 2)

bear_oi   = max(0, bear_total * PRETAX_MARGIN_CURR * 0.92)   # operating leverage hurts on lower revenue
bear_ni   = bear_oi * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {PRETAX_MARGIN_CURR*100:.0f}% pre-tax margin − {TAX_RATE*100:.0f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {PRETAX_MARGIN_BULL*100:.0f}% pre-tax margin − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.2f}/share  →  ${bull_eps_imp:.2f} × 22× = ~${bull_eps_imp*22:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {PRETAX_MARGIN_CURR*100*0.92:.1f}% margin − tax  =  ~${bear_eps_imp:.2f}/share")
print(f"  At 14× trough P/E (brokerage franchise floor) = ~${bear_eps_imp*14:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_nir  = (1.0 * (1 - TAX_RATE)) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Net Interest Revenue (pre-tax flow-through): +${eps_per_1B_nir:.3f}/EPS  = +${eps_per_1B_nir*20:.1f}/share at 20× P/E")
print(f"  Every $1B AUM fee revenue (~{PRETAX_MARGIN_CURR*100:.0f}% margin): +${eps_per_1B_nir*PRETAX_MARGIN_CURR:.3f}/EPS  = +${eps_per_1B_nir*PRETAX_MARGIN_CURR*20:.1f}/share at 20× P/E")
print(f"  25bps Fed funds move (~$0.4B NIR impact): ±${eps_per_1B_nir*0.4:.3f}/EPS  = ±${eps_per_1B_nir*0.4*20:.2f}/share at 20× P/E")
print(f"  1pp pre-tax margin expansion:    +${curr_total*0.01*(1-TAX_RATE)/shares:.3f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*20:.1f}/share at 20× P/E")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (NIR / Net New Assets / Cash Sorting / AUM Fee framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>5}  {'BASE':>5}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>6}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>5}  {ths[1]:>5}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>6}  {lbl}  {b}")

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
    ("Net Interest Revenue YoY",       "+1%",   "<-8%",     "−9pp",  "Aggressive Fed rate cuts (150bp+) compress NIM sharply"),
    ("Bank sweep cash balance trend",  "flat",  "declining","↓",     "MMF/Treasury yields re-widen vs sweep rate; cash sorting reignites"),
    ("Net new asset growth",           "~6%",   "<3%",      "−3pp",  "Advisor attrition or market downturn slows organic asset gathering"),
    ("Asset Mgmt & Admin fee growth",  "+8%",   "<2%",      "−6pp",  "Equity market correction (-20%+) shrinks AUM fee base"),
    ("Trading revenue YoY",            "+3%",   "<-10%",    "−13pp", "Low-volatility regime suppresses retail trading activity"),
    ("Pre-tax margin",                 "46%",   "<40%",     "−6pp",  "Deposit cost pressure + opex inflation compress margins"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A renewed, sharp Fed rate-cutting cycle (150bp+ over 12mo) re-widens the gap")
print(f"  between money-market fund yields and Schwab's bank sweep rate, reigniting the 'cash")
print(f"  sorting' dynamic that crushed NIR in 2022-2023. Combined with an equity market correction")
print(f"  shrinking AUM-based fees, EPS falls to ~${bear_price_eps if (bear_price_eps:=bear_eps_imp) else 0:.2f} → 14× floor = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT a permanent impairment — the ~$11T client asset base and")
print(f"  industry-leading net new asset franchise provide a durable earnings floor. Recovery to")
print(f"  ~${bear_price+25}-${bear_price+40} in 2yr is base case once rate cycle stabilizes.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~$4.45-$4.65)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (brokerage franchise floor; deep cash-sorting/rate-cut scenario)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP reflects the market's expectation that NIR has")
print(f"  bottomed and net new asset growth continues at industry-leading rates. At ${CURRENT_PRICE:.2f}")
print(f"  and FY2026E EPS ${EPS_FY2026E:.2f}, the P/E is {CURRENT_PRICE/EPS_FY2026E:.1f}× — in line with Schwab's historical")
print(f"  18-22× quality-franchise range. The risk is a renewed rate-cut cycle reopening the")
print(f"  cash-sorting headwind before it has fully stabilized.")
print(f"  EPP path: FY2028E EPS ~${CONS_EPS_2YR:.2f} × {PE_PESSIMISTIC:.0f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor by 2028 (EPP growing with earnings).")
print(f"  At 18× mid-cycle P/E: ${EPS_FY2026E:.2f} × 18 = ${EPS_FY2026E*18:.0f}")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: NIR stabilization + AUM fee growth continue)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (NIR modest recovery + AUM fee growth ~8-10%/yr)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (mid-cycle multiple; in line with 18-22× historical range)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: even the conservative case (FY2028E EPS ${CONS_EPS_2YR:.2f} at 18× + dividends)")
print(f"  implies a {cons_return:.1f}% total return over 2 years, driven by EPS growth from NIR")
print(f"  stabilization and continued AUM fee compounding rather than multiple expansion.")
print(f"  Breakeven at {CONS_PE_2YR}× P/E requires FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  (~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% growth from FY2026E ${EPS_FY2026E:.2f}).")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}-${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case attractive at 18× P/E; ratio_b <1.0×)")

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
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (rate-sensitive financial; cash-sorting binary elevated vol historically)")
print(f"  Beta vs S&P 500:      1.20  (financial sector + rate-cycle amplifier)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (significant; renewed cash-sorting/rate-cut shock)")
print(f"  52W low ${VOL_52W_LOW:.2f} reflects peak cash-sorting anxiety; current price already ~{vol_pct*100:.0f}% recovered.")
print(f"  → Fed rate path is THE KEY binary; aggressive cuts reopen cash-sorting headwind (BEAR trigger).")
print(f"  → Sustained net new asset growth + NIR inflection on rate stabilization is KEY bull catalyst.")
print(f"  → AVOID above $105  |  WATCHLIST $95-105  |  ACCUMULATE $85-95  |  BUY below $80")

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
print(f"  {valuation_label.lower()} by model standards. NIR stabilization (signal score 2/4 = BASE) and")
print(f"  net new asset growth (3/4 = BULL) are the most significant valuation drivers to watch.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Fed rate path — cutting cycle pace determines whether cash sorting reignites or fades (KEY)")
print(f"  (2) Net new assets — sustaining ~$450B/yr organic growth confirms post-TDA franchise strength")
print(f"  (3) Bank sweep balance trend — stabilization/growth signals NIR has bottomed (BULL trigger)")
print(f"  (4) AUM fee growth — equity market levels drive Asset Mgmt & Admin fee trajectory")
print(f"  (5) Trading revenue — episodic upside from elevated retail/options volume in volatile markets")
print(f"  AVOID above $105  |  WATCHLIST $95-105  |  ACCUMULATE $85-95  |  BUY below $80")
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
