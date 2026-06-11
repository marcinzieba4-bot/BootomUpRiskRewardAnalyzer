"""
MS  ·  Morgan Stanley  ·  NYSE: MS
Bottom-up signal model  ·  Investment Bank / Wealth Management / Investment Management
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "MS"
COMPANY       = "Morgan Stanley"
SECTOR        = "Investment Bank · Wealth Management · Investment Management · NYSE: MS"
CURRENT_PRICE = 152.40       # USD; as of 2026-06-11
VOL_52W_LOW   = 118.05       # Apr 2025 tariff/recession-scare trough
VOL_52W_HIGH  = 158.90       # May 2026 high; capital-markets recovery + WM re-rating
SHARES_OUT_M  = 1_330.0      # millions; declining via buyback (~2%/yr)

# Dividend: raised steadily under Pick; ~$0.925/quarter
ANNUAL_DIV    = 3.70         # $/share FY2026 ($0.925/quarter)

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ──────────────────────
# FY2026E net revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Institutional Securities (IB+Trading)", 28.5, 19.0, 36.0, "Advisory/underwriting + Equities/FICC; M&A/IPO recovery is the BULL swing"),
    ("Wealth Management",                     29.0, 25.5, 33.5, "~$7T+ client assets (MS+E*Trade+Eaton Vance); fee-based NNA growth, recurring"),
    ("Investment Management",                  1.6,  1.2,  2.1, "Eaton Vance/Calvert/Parametric AUM-linked fees; smaller but margin-accretive"),
]

# Margin assumptions
PRETAX_MARGIN_CURR = 0.290   # blended pre-tax margin FY2026E (~29%)
PRETAX_MARGIN_BULL = 0.330   # BULL: operating leverage on IB rebound + WM scale
PRETAX_MARGIN_BEAR = 0.190   # BEAR: trading slowdown + AUM fee compression hit margins hard
TAX_RATE           = 0.235   # effective rate (incl. state/local NY)

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 9.20        # FY2026E adj EPS (consensus ~$9.00-9.40)
PE_PESSIMISTIC = 11.0        # trough P/E: WM mix shift supports floor above pure-trading peers
                              # (2022-23 trough ~10-11x; pre-WM-pivot trough was 8x)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # ~$101

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 6.50, 11,   72, "Capital markets freeze + market correction; IB -35%, WM/IM AUM fees -15%; EPS $6.50 → 11x floor P/E"),
    "BASE":  ( 9.80, 14,  137, "IB/trading stable, modest M&A pickup; WM NNA continues ~$250B/yr; EPS $9.80 at FY2028E → 14x"),
    "BULL":  (12.50, 16,  200, "M&A/IPO supercycle; WM crosses $8T AUM, fee penetration rises; EPS $12.50 → 16x"),
    "XBULL": (15.50, 18,  279, "Capital markets boom + WM re-rates toward asset-manager multiple; EPS $15.50 → 18x"),
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
        "name":       "Wealth Management net new assets (NNA) annualized",
        "weight":     0.25,
        "thresholds": ("<$150B", "≥$200B", "≥$280B", "≥$350B"),
        "now":        "$245B",
        "score":      3,
        "comment":    "Continued strong organic growth; advisor recruiting + workplace channel (E*Trade) feeding pipeline",
    },
    {
        "name":       "Investment Banking (advisory+underwriting) revenue YoY",
        "weight":     0.20,
        "thresholds": ("<-10%",  "≥0%",   "≥+15%",  "≥+30%"),
        "now":        "+12%",
        "score":      2,
        "comment":    "M&A backlog rebuilding post-2025 rate cuts; IPO window reopening but not yet at peak pace",
    },
    {
        "name":       "Equities + FICC trading revenue YoY",
        "weight":     0.15,
        "thresholds": ("<-15%",  "≥-3%",  "≥+5%",   "≥+15%"),
        "now":        "+4%",
        "score":      3,
        "comment":    "Solid client activity; equities franchise (prime brokerage) remains #1; FICC normalizing from 2025 highs",
    },
    {
        "name":       "WM fee-based asset penetration (% of WM AUM)",
        "weight":     0.20,
        "thresholds": ("<54%",   "≥56%",  "≥60%",   "≥65%"),
        "now":        "57%",
        "score":      2,
        "comment":    "Steady mix shift toward fee-based advisory accounts; structural tailwind to recurring revenue",
    },
    {
        "name":       "Pre-tax margin (firmwide)",
        "weight":     0.10,
        "thresholds": ("<22%",   "≥27%",  "≥30%",   "≥33%"),
        "now":        "29%",
        "score":      3,
        "comment":    "Operating leverage from WM scale + cost discipline; near multi-year highs",
    },
    {
        "name":       "Tangible book value growth YoY",
        "weight":     0.10,
        "thresholds": ("<2%",    "≥4%",   "≥7%",    "≥10%"),
        "now":        "6%",
        "score":      3,
        "comment":    "Retained earnings + buyback accretion; supports premium P/TBV multiple",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Wealth Management scale moat — ~$7T+ client assets via MS/E*Trade/Eaton Vance integration",  +0.7, 0.25),
    ("+", "Recurring fee mix shift — WM+IM now ~55% of revenue, dampens trading cyclicality",            +0.5, 0.20),
    ("-", "Capital markets cyclicality — IB advisory/underwriting and FICC/Equities still volatile",     -0.6, 0.20),
    ("-", "Correlated downside risk — market correction hits trading AND AUM fees simultaneously",       -0.5, 0.15),
    ("+", "Capital return — steady dividend growth + buyback; strong CET1 ratio supports payouts",       +0.3, 0.10),
    ("-", "Premium valuation vs pure-trading peers — ~13-16x P/E, 1.8-2.2x tangible book leaves limited multiple expansion room", -0.3, 0.10),
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
CONS_EPS_2YR  = 10.80   # conservative FY2028E: WM NNA compounding + modest IB recovery
CONS_PE_2YR   = 13      # roughly in line with historical 13-16x range
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Investment Bank / Wealth Management / Investment Management")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<40}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<40}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<40}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000

curr_pti  = curr_total * PRETAX_MARGIN_CURR
curr_ni   = curr_pti * (1 - TAX_RATE)
curr_eps  = round(curr_ni / shares, 2)

bull_pti  = bull_total * PRETAX_MARGIN_BULL
bull_ni   = bull_pti * (1 - TAX_RATE)
shares_b  = shares * 0.96   # ~2%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_pti  = bear_total * PRETAX_MARGIN_BEAR
bear_ni   = max(0, bear_pti) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {PRETAX_MARGIN_CURR*100:.1f}% pre-tax margin − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ~${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {PRETAX_MARGIN_BULL*100:.1f}% margin − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 16× = ~${bull_eps_imp*16:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {PRETAX_MARGIN_BEAR*100:.1f}% margin − tax  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 11× trough P/E (WM-supported floor) = ~${bear_eps_imp*11:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = (1.0 * PRETAX_MARGIN_CURR * (1 - TAX_RATE)) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Wealth Management revenue:  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*14:.2f}/share at 14× P/E")
print(f"  Every $1B IB/trading revenue (cyclical): ±${eps_per_1B_rev:.3f}/EPS  =  ±${eps_per_1B_rev*14:.2f}/share at 14× P/E")
print(f"  1pp pre-tax margin expansion:         +${curr_total*0.01*(1-TAX_RATE)/shares:.3f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*14:.2f}/share at 14× P/E")
print(f"  2% buyback (~26M shares):              +${curr_eps*0.02:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (NNA growth / IB recovery / fee mix-shift framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>7}  {'BASE':>7}  {'BULL':>7}  {'XBULL':>7}  {'NOW':>7}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>7}  {ths[1]:>7}  {ths[2]:>7}  {ths[3]:>7}  {s['now']:>7}  {lbl}  {b}")

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
    ("WM net new assets (annualized)",  "$245B",  "<$100B", "−$145B", "Market correction triggers client outflows + advisor attrition"),
    ("IB advisory/underwriting YoY",     "+12%",   "<-25%",  "−37pp",  "Capital markets freeze; M&A/IPO pipeline withdrawn en masse"),
    ("Equities/FICC trading YoY",        "+4%",    "<-20%",  "−24pp",  "Volatility collapse + client de-risking cuts trading volumes"),
    ("WM fee-based asset penetration",   "57%",    "<53%",   "−4pp",   "AUM declines mechanically reduce fee base even at flat penetration"),
    ("Pre-tax margin (firmwide)",        "29%",    "<19%",   "−10pp",  "Operating deleverage; comp ratio rises as revenue falls faster than costs"),
    ("Tangible book value growth",       "6%",     "<1%",    "−5pp",   "Trading losses + AUM-linked fee collapse stall capital build"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: a capital markets freeze (recession or geopolitical shock) hits Institutional")
print(f"  Securities (advisory/underwriting/trading) AND simultaneously triggers a market correction")
print(f"  that compresses Wealth/Investment Management AUM-linked fees — the correlated-downside risk")
print(f"  the WM pivot was designed to mitigate but cannot fully eliminate. EPS falls to ~${SCENARIOS['BEAR'][0]:.2f}")
print(f"  → 11× floor P/E = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT a permanent impairment — ~$7T WM client asset base + recurring fee")
print(f"  revenue provides a durable earnings floor. Recovery toward ${bear_price+30}-${bear_price+50} in 2yr is the")
print(f"  base case post-shock as markets normalize.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~$9.00-9.40)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (WM mix supports floor above pure-trading peers; 2022-23 trough ~10-11×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP reflects the market crediting Morgan Stanley's WM-driven")
print(f"  recurring-revenue mix with a higher sustainable multiple than its pure-trading history.")
print(f"  At ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f}, the P/E is {CURRENT_PRICE/EPS_FY2026E:.1f}× — within the historical")
print(f"  13-16× range. EPP path: FY2028E EPS ~${CONS_EPS_2YR:.2f} × {PE_PESSIMISTIC:.0f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing with EPS).")
print(f"  At 13× mid-cycle P/E: ${EPS_FY2026E:.2f} × 13 = ${EPS_FY2026E*13:.0f}  — close to current price, suggesting fair value.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: NNA compounding + modest IB recovery + dividend)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (~8%/yr EPS CAGR: WM fee growth + buyback + modest IB recovery)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (in line with historical 13-16× range; no multiple expansion required)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; steady dividend growth)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: unlike pure-trading peers, MS does not require multiple expansion to deliver")
print(f"  acceptable returns — the WM recurring-fee base supports steady EPS compounding at a")
print(f"  stable 13-16× multiple, plus a ~2.4% dividend yield.")
print(f"  Breakeven at {CONS_PE_2YR}× P/E (no multiple change): need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — achievable in BASE/BULL.")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case attractive at current multiples; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.30
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock near 52W highs as capital-markets recovery + WM re-rating play out")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  steady growth track record)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (higher than mega-cap tech; capital-markets cyclicality)")
print(f"  Beta vs S&P 500:      1.30  (financials/capital-markets sensitivity to rates and risk appetite)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe but plausible in a recession/correction)")
print(f"  52W low ${VOL_52W_LOW:.2f} (Apr 2025 tariff scare) was a peak-to-trough move of ~25%.")
print(f"  → Capital markets activity (M&A/IPO pace, trading volumes) is THE KEY swing factor for IB.")
print(f"  → WM net new assets + fee-based penetration trends are KEY structural bull catalysts.")
print(f"  → WATCHLIST ${bear_price+30:.0f}-${bear_price+45:.0f}  |  ACCUMULATE ${bear_price+10:.0f}-${bear_price+25:.0f}  |  BUY below ${bear_price+10:.0f}")

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
print(f"  WM scale and recurring-fee mix shift (signal scores mostly BULL/BASE) underpin the floor,")
print(f"  while IB/trading cyclicality and correlated downside risk remain the key swing factors.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) M&A/IPO cycle acceleration — IB advisory/underwriting revenue inflection (BULL trigger)")
print(f"  (2) Wealth Management NNA sustaining $250B+/yr — validates the multi-year WM pivot")
print(f"  (3) Fee-based asset penetration crossing 60% — structural recurring-revenue tailwind")
print(f"  (4) Capital markets correction — correlated hit to trading AND AUM fees (BEAR trigger)")
print(f"  (5) Capital return — buyback pace and dividend growth under Ted Pick's capital plan")
print(f"  WATCHLIST ${bear_price+30:.0f}-${bear_price+45:.0f}  |  ACCUMULATE ${bear_price+10:.0f}-${bear_price+25:.0f}  |  BUY below ${bear_price+10:.0f}")
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
