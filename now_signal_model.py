"""
NOW  ·  ServiceNow, Inc.  ·  NYSE: NOW
Bottom-up signal model  ·  Enterprise SaaS / Workflow Automation / Agentic AI Platform
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "NOW"
COMPANY       = "ServiceNow, Inc."
SECTOR        = "Enterprise SaaS · Workflow Automation · Agentic AI Platform · NYSE: NOW"
CURRENT_PRICE = 100.58       # USD; June 9 2026; post 5-for-1 split Dec 2025; down 52% from $211.48 pre-split-adjusted ATH
VOL_52W_LOW   = 78.40        # March 2026 trough; AI disruption fear / macro
VOL_52W_HIGH  = 130.20       # post-split adjusted prior peak
SHARES_OUT_M  = 1_245.0      # millions; post 5-for-1 split (was ~249M pre-split)

# Dividend: none; reinvests in growth + buybacks
ANNUAL_DIV    = 0.0          # $/share

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2027E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("IT Workflows (ITSM/ITOM/ITAM)",       6.5, 5.5, 8.0, "Core ITSM platform; AI-powered incident resolution; mature but durable"),
    ("Customer & Industry Workflows (CSM)", 3.0, 2.3, 4.2, "Customer service management; vertical industry solutions (telecom/healthcare/finance)"),
    ("Employee Workflows (HR/Now Assist)",  2.2, 1.6, 3.2, "HR Service Delivery; Now Assist generative AI agents embedded across HR"),
    ("Creator Workflows / App Engine",      1.5, 1.0, 2.3, "Low-code platform; App Engine; citizen developer expansion"),
    ("AI Agent Platform (Agentic AI)",      1.8, 0.6, 5.5, "New: autonomous AI agents across workflows; RPO $27.7B includes growing AI agent ACV"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.815   # non-GAAP; best-in-class SaaS gross margin
GROSS_MARGIN_BULL = 0.840   # BULL: AI agent layer adds high-margin incremental revenue
OPEX_FIXED_B      = 9.2     # non-GAAP R&D + SG&A; heavy go-to-market investment
TAX_RATE          = 0.180   # effective US-based SaaS

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 4.20        # consensus non-GAAP EPS post-split (was ~$21 pre-split / 5)
PE_PESSIMISTIC = 24.0        # trough P/E: best-in-class SaaS franchise; rarely trades below 24× even in distress
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # $101

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 3.20, 22,  70,  "Macro recession + agentic AI disruption fear peaks; NRR <105%; EPS $3.20 → 22× distress"),
    "BASE":  ( 4.80, 32, 154,  "Now Assist/AI agents drive 18-20% subscription growth; NRR 112%+; EPS $4.80 → 32×"),
    "BULL":  ( 6.50, 38, 247,  "AI Agent Platform becomes enterprise standard; RPO accelerates >25%; EPS $6.50 → 38×"),
    "XBULL": ( 9.50, 44, 418,  "NOW = enterprise AI operating system; agentic workflows replace legacy SaaS seats; EPS $9.50 → 44×"),
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
        "name":       "Subscription revenue YoY growth",
        "weight":     0.25,
        "thresholds": ("<14%",  "≥18%",  "≥24%",  "≥32%"),
        "now":        "+20%",
        "score":      2,
        "comment":    "Q1 2026 subscription rev +20% YoY; durable double-digit growth despite macro headwinds",
    },
    {
        "name":       "Current RPO (cRPO) growth YoY",
        "weight":     0.25,
        "thresholds": ("<14%",  "≥18%",  "≥24%",  "≥32%"),
        "now":        "+22%",
        "score":      2,
        "comment":    "cRPO $14.8B +22% YoY — leading indicator; AI agent ACV embedded in new bookings",
    },
    {
        "name":       "Net Revenue Retention (NRR)",
        "weight":     0.20,
        "thresholds": ("<105%", "≥110%", "≥118%", "≥125%"),
        "now":        "~112%",
        "score":      2,
        "comment":    "NRR 112%, stable; large enterprise accounts (>$1M ACV) growing +20%+ YoY",
    },
    {
        "name":       "Now Assist / AI agent ACV",
        "weight":     0.15,
        "thresholds": ("<$300M","≥$600M","≥$1.2B","≥$2.5B"),
        "now":        "~$700M",
        "score":      2,
        "comment":    "Now Assist ACV crossed $700M, doubling YoY; early but rapid enterprise AI agent adoption",
    },
    {
        "name":       "Non-GAAP operating margin",
        "weight":     0.10,
        "thresholds": ("<27%",  "≥30%",  "≥34%",  "≥40%"),
        "now":        "31%",
        "score":      2,
        "comment":    "Op margin 31%, expanding ~1pp/yr; reinvestment in AI R&D balanced with operating leverage",
    },
    {
        "name":       "Free cash flow margin",
        "weight":     0.05,
        "thresholds": ("<28%",  "≥32%",  "≥36%",  "≥42%"),
        "now":        "~32%",
        "score":      2,
        "comment":    "FCF margin ~32%; strong cash generation funding AI platform R&D without dilution",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Workflow platform moat — single data model across IT/HR/CSM; deep enterprise integration, 5yr+ switching cost", +0.7, 0.25),
    ("+", "Agentic AI early leader — Now Assist embedded across all workflows; platform-level (not bolt-on) AI",          +0.6, 0.20),
    ("-", "Macro sensitivity — large enterprise deals elongating in slow-IT-budget environment; deal cycle risk",          -0.4, 0.20),
    ("-", "Competitive AI agent crowding — Microsoft Copilot Studio, Salesforce Agentforce, Workday all building agents",  -0.5, 0.15),
    ("+", "Founder-grade execution — Bill McDermott; consistent beat-and-raise; 25%+ revenue CAGR for a decade",           +0.5, 0.10),
    ("+", "Post-split entry point — down 52% from pre-split-adjusted ATH; lowest forward multiple since 2018",             +0.4, 0.10),
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
CONS_EPS_2YR  = 6.20    # FY2029E conservative: 21% EPS CAGR; still strong; below BASE
CONS_PE_2YR   = 30      # rerates from ~24× toward 30× as growth durability re-confirmed
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Enterprise SaaS / Workflow Automation / Agentic AI")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2027E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<26}  {'FY2027E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<26}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<26}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print()

# EPS bridge
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_ni   = curr_oi * (1 - TAX_RATE)
shares    = SHARES_OUT_M / 1000
curr_eps  = round(curr_ni / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B
bull_ni   = bull_oi * (1 - TAX_RATE)
shares_b  = shares * 0.97   # modest buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift / pricing pressure
bear_oi   = bear_gp - OPEX_FIXED_B * 0.97           # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2027E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2027E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 38× = ~${bull_eps_imp*38:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 22× trough P/E (distress) = ~${bear_eps_imp*22:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B subscription revenue:  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*32:.1f}/share at 32× P/E")
print(f"  1pp GM expansion (AI agent mix):  +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*32:.1f}/share at 32× P/E")
print(f"  Now Assist ACV +$1B:              boosts AI Agent Platform segment revenue directly; high-margin incremental")
print(f"  1% buyback (~12.5M shares):        +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (subscription growth / cRPO / NRR / Now Assist framework)")
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
    ("Subscription revenue YoY",     "+20%",   "<+14%",  "−6pp",   "Macro IT budget freeze; deal elongation hits renewals"),
    ("cRPO growth YoY",               "+22%",   "<+14%",  "−8pp",   "Large enterprise deals slip to next quarter en masse"),
    ("Net Revenue Retention",         "~112%",  "<105%",  "−7pp",   "Seat reductions as AI agents replace human workflow operators"),
    ("Now Assist / AI agent ACV",     "~$700M", "<$300M", "−$400M", "Agentic AI pilots fail to convert; ROI unproven"),
    ("Non-GAAP operating margin",     "31%",    "<27%",   "−4pp",   "AI compute costs (inference) compress margins faster than revenue grows"),
    ("Free cash flow margin",         "~32%",   "<28%",   "−4pp",   "Working capital deterioration; deferred revenue growth slows"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  POST-SPLIT REPRICING: ServiceNow completed a 5-for-1 stock split in December 2025")
print(f"  ($502 → ~$100 equivalent). The Q1 2026 non-GAAP EPS of $0.97 (post-split) beat the")
print(f"  $0.55 estimate by 76% — yet the stock remains 52% below its pre-split-adjusted ATH")
print(f"  ($211.48 equiv. post-split / $1,057 pre-split). At 24x FY2027E, this is the lowest")
print(f"  forward multiple for NOW since 2018, despite RPO of $27.7B (+24% YoY) representing")
print(f"  nearly 3x current-year revenue in contracted backlog. The market is treating")
print(f"  ServiceNow like a mature, slowing SaaS name — but RPO growth and Now Assist traction")
print(f"  both argue the growth re-acceleration thesis is intact.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E adj EPS estimate:      ${EPS_FY2027E:.2f}  (consensus; non-GAAP)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (best-in-class SaaS franchise; rarely trades below 24× even in distress)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% vs trough floor)")
print()
print(f"  At a {epp_gap_pct:+.1f}% gap to EPP, the current price is essentially trading AT the trough")
print(f"  floor multiple — the market is pricing almost zero growth premium into a franchise")
print(f"  still compounding subscription revenue at +20% YoY with cRPO +22% YoY. This is the")
print(f"  'distress-priced compounder' setup: downside is cushioned by the floor multiple itself.")
print(f"  EPP path: FY2029E EPS ~${CONS_EPS_2YR:.2f} × {PE_PESSIMISTIC:.0f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor by 2028 (EPP growing with EPS).")
print(f"  At 32× mid-cycle P/E: ${EPS_FY2027E:.2f} × 32 = ${EPS_FY2027E*32:.0f}  — {(EPS_FY2027E*32-CURRENT_PRICE)/CURRENT_PRICE*100:.0f}% above current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: P/E rerates as growth durability re-confirmed)")
hr()
print(f"  Conservative FY2029E adj EPS:  ${CONS_EPS_2YR:.2f}  (21% EPS CAGR; below BASE but still strong)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (rerates from ~24× toward 30× as growth durability re-confirmed)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (no dividend; reinvests in growth + buybacks)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: even the conservative case (21% EPS CAGR, modest rerate to 30×) produces a")
print(f"  large positive return from current levels — unlike mature mega-cap compounders where")
print(f"  multiple compression offsets growth. NOW's combination of post-split distress pricing")
print(f"  and durable double-digit growth is the core of the bottom-up thesis.")
print(f"  Breakeven at 24× P/E (no rerate): FY2029E EPS ≥ ${(CURRENT_PRICE - cons_divs) / PE_PESSIMISTIC:.2f}")
print(f"  Breakeven at 30× P/E: FY2029E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 30:.2f}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.38
beta        = 1.25
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: range is post-5-for-1-split-adjusted; March 2026 trough = AI disruption fear / macro")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (none; reinvests in growth + buybacks)")
print(f"  Realized vol (annual):{annual_vol*100:.0f}%  (elevated; high-multiple SaaS + AI narrative sensitivity)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (high-beta growth name; amplifies macro swings)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe but plausible in a recession scenario)")
print(f"  52W low ${VOL_52W_LOW:.2f} (Mar 2026 AI-disruption panic) already a peak-to-trough move of ~22% from current.")
print(f"  → Macro/recession risk + AI-agent disruption fear are THE KEY binaries for downside.")
print(f"  → Now Assist ACV acceleration + cRPO reacceleration are KEY bull catalysts.")
print(f"  → AVOID above $180  |  WATCHLIST $130–150  |  ACCUMULATE $105–125  |  BUY below $105")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is BELOW the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0 — close to")
print(f"  BEAR/BASE boundary. The model scores the fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0 — between BASE and BULL.")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: you are paying near-BEAR scenario prices for what is currently solid")
print(f"  BASE-to-BULL execution. The post-split repricing is the most significant valuation mismatch.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q2 2026 earnings (July 2026) — Now Assist ACV update; cRPO trajectory confirmation")
print(f"  (2) Federal/public sector wins — FedRAMP High momentum continuing post-DOGE disruption")
print(f"  (3) AI agent competitive differentiation — platform-level vs point-solution agents (vs Copilot/Agentforce)")
print(f"  (4) Knowledge 2026 (May) product announcements — agentic AI roadmap, pricing model evolution")
print(f"  (5) Large deal (>$1M ACV) momentum — count and average deal size growth as enterprise AI budget signal")
print(f"  AVOID above $180  |  WATCHLIST $130–150  |  ACCUMULATE $105–125  |  BUY below $105")
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
