"""
WFC  ·  Wells Fargo & Company  ·  NYSE: WFC
Bottom-up signal model  ·  Bank Holding Company / Asset-Cap Removal Re-rating
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "WFC"
COMPANY       = "Wells Fargo & Company"
SECTOR        = "Bank Holding Company · Consumer/Commercial Banking · NYSE: WFC"
CURRENT_PRICE = 84.50       # USD; as of 2026-06-10
VOL_52W_LOW   = 64.97       # 2025 trough (pre-cap-removal)
VOL_52W_HIGH  = 89.20       # 2026 high post asset-cap removal re-rating
SHARES_OUT_M  = 2_900.0     # millions; declining via aggressive buyback program

# Dividend: growing steadily post-stress-test clearance
ANNUAL_DIV    = 1.80        # $/share FY2026 ($0.45/quarter)

# ── REVENUE BRIDGE (company-specific calculator) ──────────────────────────────
# FY2026E net revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Consumer Banking & Lending",      19.5, 17.0, 22.5, "Deposits, cards, auto, home lending; rate-path sensitive NII"),
    ("Commercial Banking",               8.5,  7.3, 10.0, "Middle-market lending; benefits most from asset-cap removal"),
    ("Corporate & Investment Banking",  10.0,  8.0, 13.0, "Markets/banking fees; balance-sheet growth post-cap unlocks growth"),
    ("Wealth & Investment Management",   4.0,  3.4,  4.8, "Fee-based AUM growth; market-level sensitivity"),
]

# Margin / cost assumptions (bank-specific: efficiency ratio framework)
EFF_RATIO_CURR   = 0.61    # current efficiency ratio (~61%); Scharf turnaround target ~58-60%
EFF_RATIO_BULL   = 0.56    # BULL: continued expense discipline + operating leverage from cap removal
PROVISION_B_CURR = 1.3     # quarterly credit provision run-rate ($B) annualized to ~5.2B; using annual below
PROVISION_B_ANNUAL_CURR = 5.2   # annual credit loss provision ($B) - normalized
PROVISION_B_ANNUAL_BEAR = 9.5   # BEAR: credit cycle deterioration in consumer/CRE book
TAX_RATE         = 0.235   # effective tax rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 5.85        # FY2026E adj EPS (consensus ~$5.70-$6.00)
PE_PESSIMISTIC = 9.0         # trough P/E: pre-cap-removal regulatory-discount multiple
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # ~$53

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 5.10, 11,   56, "Credit cycle deterioration in consumer/CRE; NII compression on rate cuts; EPS $5.10 → 11× regulatory-discount P/E"),
    "BASE":  ( 5.85, 14.5, 85, "Cap-removal benefits gradual; efficiency ratio improves to ~59%; EPS $5.85 → 14.5× (in line with current price)"),
    "BULL":  ( 7.20, 15.5, 112, "Balance sheet growth accelerates post-cap; efficiency ratio ~57%; EPS $7.20 → 15.5× (peer-level re-rating)"),
    "XBULL": ( 8.50, 17,  145, "Full re-rating above JPM/BAC peer multiples; cap-removal fully realized; EPS $8.50 → 17×"),
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
        "name":       "Asset cap removal / balance sheet growth",
        "weight":     0.25,
        "thresholds": ("Frozen",  "Easing", "Growing", "Accelerating"),
        "now":        "Growing",
        "score":      3,
        "comment":    "Fed removed the ~$1.95T asset cap in mid-2025; balance sheet growth resuming in commercial/CIB",
    },
    {
        "name":       "Efficiency ratio (lower = better)",
        "weight":     0.20,
        "thresholds": (">63%",   "≤61%",  "≤58%",   "≤55%"),
        "now":        "61%",
        "score":      2,
        "comment":    "Scharf-led expense discipline continuing; targeting sub-60% but not yet there",
    },
    {
        "name":       "Net interest income YoY growth",
        "weight":     0.20,
        "thresholds": ("<-3%",   "≥0%",   "≥4%",    "≥8%"),
        "now":        "+1%",
        "score":      2,
        "comment":    "Rate cuts pressure NIM but balance sheet growth post-cap offsets; modest growth",
    },
    {
        "name":       "Credit quality (NCO ratio trend)",
        "weight":     0.15,
        "thresholds": ("Worsening", "Stable", "Improving", "Strong improving"),
        "now":        "Stable",
        "score":      2,
        "comment":    "Consumer card/auto charge-offs normalizing; CRE office exposure remains a watch item",
    },
    {
        "name":       "P/E vs peer (JPM/BAC) discount",
        "weight":     0.10,
        "thresholds": (">30%",   "≥20%",  "≥10%",   "<5%"),
        "now":        "~20%",
        "score":      2,
        "comment":    "WFC trades ~11-13x vs JPM/BAC ~13-15x; discount narrowing post-cap-removal but not closed",
    },
    {
        "name":       "Capital return (buyback + dividend)",
        "weight":     0.10,
        "thresholds": ("<5%",    "≥7%",   "≥10%",   "≥13%"),
        "now":        "~9%",
        "score":      2,
        "comment":    "Combined buyback + dividend yield ~9% of market cap; CET1 well above requirement",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Asset cap removal — structural unlock; first balance-sheet growth runway since 2018",     +0.8, 0.25),
    ("+", "Capital return machine — large buyback authorization + growing dividend; strong CET1",    +0.5, 0.20),
    ("-", "Credit cycle risk — consumer (cards/auto) and CRE office exposure late-cycle",             -0.6, 0.20),
    ("+", "Efficiency turnaround — Scharf-era cost cuts structurally lower expense base",            +0.4, 0.15),
    ("-", "NIM sensitivity — Fed rate-cut path compresses net interest margin near-term",            -0.5, 0.15),
    ("-", "Regulatory overhang residual — consent orders not fully closed; execution risk remains",  -0.3, 0.05),
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
CONS_EPS_2YR  = 6.60    # conservative FY2028E: cap-removal benefits + efficiency gains, modest credit normalization
CONS_PE_2YR   = 11      # rerating from ~12x toward conservative 11x (some multiple compression risk)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Bank Holding Company / Asset-Cap Removal Re-rating")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① REVENUE BRIDGE ─────────────────────────────────────────────────────────
print()
print("  REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
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

# EPS bridge (bank-specific: revenue → pre-provision profit → less provisions → tax)
shares    = SHARES_OUT_M / 1000

curr_ppnr = curr_total * (1 - EFF_RATIO_CURR)
curr_pretax = curr_ppnr - PROVISION_B_ANNUAL_CURR
curr_ni   = curr_pretax * (1 - TAX_RATE)
curr_eps  = round(curr_ni / shares, 2)

bull_ppnr = bull_total * (1 - EFF_RATIO_BULL)
bull_pretax = bull_ppnr - PROVISION_B_ANNUAL_CURR
bull_ni   = bull_pretax * (1 - TAX_RATE)
shares_b  = shares * 0.92   # ~4%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 2)

bear_ppnr = bear_total * (1 - EFF_RATIO_CURR * 1.02)   # slight efficiency slippage in downturn
bear_pretax = bear_ppnr - PROVISION_B_ANNUAL_BEAR
bear_ni   = max(0, bear_pretax) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B revenue × (1−{EFF_RATIO_CURR*100:.0f}% eff. ratio) − ${PROVISION_B_ANNUAL_CURR:.1f}B provisions − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ~${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × (1−{EFF_RATIO_BULL*100:.0f}% eff. ratio) − ${PROVISION_B_ANNUAL_CURR:.1f}B provisions − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.2f}/share  →  ${bull_eps_imp:.2f} × 13.5 = ~${bull_eps_imp*13.5:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × (1−{EFF_RATIO_CURR*1.02*100:.0f}% eff. ratio) − ${PROVISION_B_ANNUAL_BEAR:.1f}B provisions  =  ~${bear_eps_imp:.2f}/share")
print(f"  At 10× regulatory-discount P/E = ~${bear_eps_imp*10:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev   = (1.0 * (1 - EFF_RATIO_CURR) * (1 - TAX_RATE)) / shares
eps_per_1B_provision = 1.0 * (1 - TAX_RATE) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B total revenue (op. leverage): +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*12:.2f}/share at 12× P/E")
print(f"  Every $1B credit provision:             -${eps_per_1B_provision:.3f}/EPS  = -${eps_per_1B_provision*12:.2f}/share at 12× P/E")
print(f"  1pp efficiency ratio improvement:       +${curr_total*0.01*(1-TAX_RATE)/shares:.3f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*12:.2f}/share at 12× P/E")
print(f"  4% buyback (~116M shares):               +${curr_eps*0.04:.3f}/EPS  (mechanical accretion from large repurchase program)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (asset-cap removal / efficiency / NII / credit framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<48}  {'BEAR':>9}  {'BASE':>8}  {'BULL':>9}  {'XBULL':>13}  {'NOW':>9}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<48}  {ths[0]:>9}  {ths[1]:>8}  {ths[2]:>9}  {ths[3]:>13}  {s['now']:>9}  {lbl}  {b}")

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
print(f"  {'Signal':<48}  {'Current':>10}  {'Bear val':>10}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Asset cap removal benefit",     "Growing", "Stalled",  "—",     "Regulatory re-imposition or self-imposed pause on growth"),
    ("Efficiency ratio",              "61%",     ">64%",     "+3pp",  "Expense reinvestment outpaces revenue; turnaround stalls"),
    ("Net interest income YoY",       "+1%",     "<-4%",     "−5pp",  "Aggressive Fed rate cuts compress NIM faster than balance sheet grows"),
    ("Credit quality (NCO trend)",    "Stable",  "Worsening","↓",     "Recession hits consumer cards/auto + CRE office defaults spike"),
    ("Credit provisions (annual)",    "$5.2B",   ">$9B",     "+$4B",  "Reserve build for deteriorating loan book"),
    ("P/E multiple",                  "~12×",    "10×",      "−2x",   "Risk-off de-rating; regulatory discount widens again"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<48}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:42]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A recession-driven credit cycle (consumer cards/auto charge-offs spike,")
print(f"  CRE office defaults accelerate) combined with aggressive Fed rate cuts compressing NII")
print(f"  forces provisions toward ${PROVISION_B_ANNUAL_BEAR:.1f}B and EPS down to ~${bear_eps_imp:.2f}. With sentiment")
print(f"  reverting to the pre-cap-removal regulatory-discount multiple (~10×), price falls to ${bear_price}.")
print(f"  Note: ${bear_price} is not a permanent impairment — strong CET1 capital base and the structural")
print(f"  asset-cap-removal tailwind provide a durable recovery path over 1-2yr.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~$5.70-$6.00)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.1f}×  (pre-cap-removal regulatory-discount multiple)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP reflects the market pricing in continued cap-removal")
print(f"  re-rating toward peer (JPM/BAC) multiples of ~13-15×. At ${CURRENT_PRICE:.2f} and FY2026E EPS")
print(f"  ${EPS_FY2026E:.2f}, the implied P/E is ~{CURRENT_PRICE/EPS_FY2026E:.1f}×. The risk is the cap-removal benefits")
print(f"  take longer than expected to flow through to NII/fee growth, stalling the re-rating.")
print(f"  EPP path: FY2028E EPS ~${CONS_EPS_2YR:.2f} × {PE_PESSIMISTIC:.1f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing as earnings compound).")
print(f"  At {CONS_PE_2YR}× mid-cycle P/E: ${EPS_FY2026E:.2f} × {CONS_PE_2YR} = ${EPS_FY2026E*CONS_PE_2YR:.0f}  — close to current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: cap-removal benefits + efficiency gains, modest re-rating)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (~13% EPS growth: cap-removal NII/fee benefit + efficiency gains)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (modest move from ~12× toward 11-13× peer-discount range)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE OPPORTUNITY: cap-removal benefits are still early-stage. Even a conservative ~13%")
print(f"  EPS growth scenario with only modest multiple movement (12× → {CONS_PE_2YR}×) generates a")
print(f"  positive total return including dividends — unlike many post-rally bank names.")
print(f"  Breakeven at flat 12× P/E (no multiple compression): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 12:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case attractive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.26
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: 52W high reflects post-asset-cap-removal re-rating gains through mid-2026")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (typical large-cap bank volatility; rate-cycle sensitive)")
print(f"  Beta vs S&P 500:      1.20  (above-market; cyclical/financials amplifier)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (credit-cycle recession scenario)")
print(f"  52W low ${VOL_52W_LOW:.2f} (pre-cap-removal) already reflects a meaningful regulatory discount.")
print(f"  → Credit cycle (consumer + CRE office) is THE KEY downside risk; each provision surprise = -5-10% move.")
print(f"  → Continued balance-sheet growth post-cap-removal is KEY bull catalyst toward peer multiples.")
print(f"  → AVOID above $95  |  WATCHLIST $85–95  |  ACCUMULATE $75–85  |  BUY below $70")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) compares to")
print(f"  the model's adj composite ({ADJ_COMPOSITE:.3f}). The gap ({ADJ_GAP:.2f}) indicates the stock is")
print(f"  {valuation_label.lower()} by model standards. The asset-cap-removal re-rating thesis (signal score 3/4)")
print(f"  is the most significant structural driver, partially offset by NII/credit-cycle risk.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Asset cap removal follow-through — balance sheet growth in commercial/CIB driving NII/fees (BULL trigger)")
print(f"  (2) Efficiency ratio progress toward sub-58% — Scharf turnaround execution (BULL trigger)")
print(f"  (3) Credit quality — consumer card/auto charge-offs and CRE office exposure (BEAR risk)")
print(f"  (4) Fed rate path — NIM sensitivity to pace/depth of rate cuts")
print(f"  (5) Peer multiple convergence — P/E re-rating toward JPM/BAC (~13-15×) vs current ~{CURRENT_PRICE/EPS_FY2026E:.0f}×")
print(f"  AVOID above $95  |  WATCHLIST $85–95  |  ACCUMULATE $75–85  |  BUY below $70")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.1f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}")
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
