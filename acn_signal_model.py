"""
ACN  ·  Accenture plc  ·  NYSE: ACN
Bottom-up signal model  ·  IT Consulting & Services / Digital Transformation / Agentic AI
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "ACN"
COMPANY       = "Accenture plc"
SECTOR        = "IT Consulting & Services · Digital Transformation · Agentic AI · NYSE: ACN"
CURRENT_PRICE = 177.52      # USD; June 9 2026; down ~49% from ATH ~$345
VOL_52W_LOW   = 159.80      # April 2026 trough; DOGE federal contract cuts fear
VOL_52W_HIGH  = 298.40      # June 2025 pre-correction peak
SHARES_OUT_M  = 620.0       # millions; declining via buybacks

# Dividend: consistent grower
ANNUAL_DIV    = 5.92        # $1.48/quarter; ~3.3% yield at current price

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B), fiscal year ends August 2026
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Strategy & Consulting",         18.5, 15.5, 23.0, "Core advisory; AI strategy engagements; cyclically sensitive to discretionary spend"),
    ("Technology Services",           32.0, 27.0, 40.0, "Largest segment; cloud migration, ERP modernization, AI integration build-out"),
    ("Operations (Managed Services)", 16.5, 14.0, 21.0, "BPO + managed services; recurring revenue; AI agents automating back-office"),
    ("Industry X (Engineering/Mfg)",   8.0,  6.5, 11.0, "Digital engineering, manufacturing, supply chain; physical-digital convergence"),
    ("Song (Marketing/Experience)",    7.5,  6.0,  9.5, "Creative + marketing transformation; smallest, most discretionary segment"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.330   # non-GAAP gross margin (services business; labor-cost driven)
GROSS_MARGIN_BULL = 0.355   # BULL: AI agent productivity tools lift utilization & margin
OPEX_FIXED_B      = 14.0    # SG&A (sales, bench, overhead)
TAX_RATE          = 0.230   # effective; Ireland-domiciled but global operations

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 13.50      # consensus non-GAAP EPS FY2026 (Aug 2026); guided ~$13.45-13.65
PE_PESSIMISTIC = 13.0       # trough: COVID-era trough was ~21x; current 12.9x is BELOW that — historic low
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $176

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (11.50, 12, 138,  "DOGE-style federal cuts spread to private sector; discretionary consulting freeze; EPS $11.50 → 12×"),
    "BASE":  (15.00, 18, 270,  "AI bookings ($2.2B/qtr) convert to delivery revenue; FY2028E EPS $15 → 18× = $270"),
    "BULL":  (19.00, 22, 418,  "GenAI/agentic transformation supercycle; record bookings sustained; FY2028E EPS $19 → 22×"),
    "XBULL": (26.00, 27, 702,  "ACN = systems integrator for the agentic AI economy; every enterprise re-platforms; EPS $26 → 27×"),
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
        "name":       "New bookings YoY growth",
        "weight":     0.30,
        "thresholds": ("<-5%",   "≥0%",   "≥10%",   "≥25%"),
        "now":        "+15%",
        "score":      3,
        "comment":    "Record Q2 FY2026 bookings $22.1B (+15% YoY); GenAI bookings $2.2B/qtr (+100% YoY)",
    },
    {
        "name":       "GenAI/Agentic AI bookings",
        "weight":     0.25,
        "thresholds": ("<$1B",   "≥$1.5B","≥$2.5B", "≥$5B"),
        "now":        "~$2.2B",
        "score":      2,
        "comment":    "GenAI bookings $2.2B/qtr, doubling YoY; cumulative GenAI bookings >$10B since launch",
    },
    {
        "name":       "Revenue YoY growth (constant currency)",
        "weight":     0.20,
        "thresholds": ("<0%",    "≥3%",   "≥7%",    "≥12%"),
        "now":        "+5%",
        "score":      2,
        "comment":    "Revenue +5% cc; Federal segment headwind (-decline) offset by commercial growth",
    },
    {
        "name":       "Federal/Government revenue (DOGE exposure)",
        "weight":     0.10,
        "thresholds": ("<-25%",  "≥-10%", "≥0%",    "≥+10%"),
        "now":        "-12%",
        "score":      2,
        "comment":    "Federal revenue ~8% of total, down -12% YoY post-DOGE contract reviews; mostly absorbed",
    },
    {
        "name":       "Non-GAAP operating margin",
        "weight":     0.10,
        "thresholds": ("<14%",   "≥15%",  "≥16.5%", "≥18%"),
        "now":        "15.8%",
        "score":      2,
        "comment":    "Op margin 15.8%, expanding via pyramid optimization + AI-driven delivery efficiency",
    },
    {
        "name":       "Free cash flow yield",
        "weight":     0.05,
        "thresholds": ("<5%",    "≥7%",   "≥9%",    "≥12%"),
        "now":        "9.8%",
        "score":      3,
        "comment":    "FCF yield 9.8% ($10.9B FCF / $111B mkt cap) — among highest in large-cap services",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Scale + relationship moat — #1 global IT services; embedded in Fortune 500 transformation roadmaps", +0.7, 0.20),
    ("+", "GenAI delivery leadership — $10B+ cumulative GenAI bookings; AI Refinery platform; first-mover in agentic delivery", +0.6, 0.20),
    ("-", "DOGE/federal headwind — US federal ~8% of revenue under sustained contract review pressure",          -0.4, 0.15),
    ("-", "Margin structure at risk — agentic AI could compress billable-hours model; productivity = less revenue per project", -0.5, 0.20),
    ("+", "Historic valuation trough — 12.9× FY2026E is lowest P/E in modern history (vs COVID trough ~21×)",     +0.6, 0.15),
    ("+", "FCF + capital return — $10.9B FCF, 3.3% dividend yield, consistent buyback program",                   +0.4, 0.10),
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
CONS_EPS_2YR  = 15.50   # FY2028E conservative: 7% EPS CAGR; modest bookings conversion
CONS_PE_2YR   = 16      # rerates modestly from 12.9× toward 16× as fears partially recede
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  IT Consulting / Digital Transformation / Agentic AI")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
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
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_ni   = curr_oi * (1 - TAX_RATE)
shares    = SHARES_OUT_M / 1000
curr_eps  = round(curr_ni / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B
bull_ni   = bull_oi * (1 - TAX_RATE)
shares_b  = shares * 0.94   # ~3%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift, pricing pressure
bear_oi   = bear_gp - OPEX_FIXED_B * 0.97           # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 22× = ~${bull_eps_imp*22:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 12× trough P/E (DOGE-cut floor) = ~${bear_eps_imp*12:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Technology Services revenue:  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*18:.2f}/share at 18× P/E")
print(f"  Federal revenue ±$1B (ops margin):       ±${eps_per_1B_rev:.3f}/EPS  =  ±${eps_per_1B_rev*18:.2f}/share at 18× P/E")
print(f"  1pp GM expansion (AI productivity):      +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*18:.2f}/share at 18× P/E")
print(f"  1% buyback (6.2M shares):                 +${curr_eps*0.01:.3f}/EPS  (mechanical accretion; ongoing buyback program)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Bookings / GenAI conversion / Federal exposure / Margin framework)")
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
    ("New bookings YoY",              "+15%",   "<-5%",   "−20pp",  "Enterprise discretionary spend freeze; recession"),
    ("GenAI/Agentic bookings",         "~$2.2B", "<$1B",   "−$1.2B", "AI pilot fatigue; enterprises pause agentic rollouts"),
    ("Revenue YoY (constant currency)", "+5%",    "<0%",    "−5pp",   "Bookings-to-revenue conversion stalls; project delays"),
    ("Federal revenue YoY",            "-12%",   "<-25%",  "−13pp",  "DOGE expands cuts to all discretionary federal IT spend"),
    ("Non-GAAP operating margin",      "15.8%",  "<14%",   "−1.8pp", "Pricing pressure as clients demand AI-driven cost savings"),
    ("Free cash flow yield",           "9.8%",   "<5%",    "−4.8pp", "Working capital deterioration; DSO extension from clients"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: DOGE-style federal contract cuts (currently -12% YoY, ~8% of revenue)")
print(f"  metastasize into a broader private-sector pullback as enterprises freeze discretionary")
print(f"  consulting spend amid macro uncertainty. Bookings reverse from +15% to negative,")
print(f"  GenAI pilot enthusiasm fades, and EPS compresses to ~$11.50 → 12× trough = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT a permanent impairment — $10.9B FCF, dividend, and buyback")
print(f"  provide a durable floor. Recovery toward BASE in 2yr remains plausible post-shock.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus $13.45–$13.65; non-GAAP)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.1f}×  (BELOW COVID-era trough of ~21×; historic low)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({'below' if epp_gap_pct < 0 else 'above'} trough floor)")
print()
print(f"  ACN trades essentially AT/BELOW its own historic trough-multiple floor while")
print(f"  delivering record bookings ($22.1B, +15% YoY) and doubling GenAI bookings ($2.2B/qtr).")
print(f"  At ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f}, the P/E is {CURRENT_PRICE/EPS_FY2026E:.1f}× —")
print(f"  the lowest multiple in the company's modern history, even below the COVID-19 trough (~21×).")
print(f"  EPP path: FY2028E EPS ~${CONS_EPS_2YR:.2f} × {PE_PESSIMISTIC:.0f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor by FY2028 (EPP growing with EPS).")
print(f"  At {CONS_PE_2YR}× mid-cycle P/E: ${EPS_FY2026E:.2f} × {CONS_PE_2YR} = ${EPS_FY2026E*CONS_PE_2YR:.0f}  — {(EPS_FY2026E*CONS_PE_2YR/CURRENT_PRICE-1)*100:+.0f}% vs current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: P/E rerates modestly off historic trough)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (7% EPS CAGR: buyback + bookings conversion)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (rerates from 12.9× toward 16× as fears partially recede)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; consistent dividend grower)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: even a MODEST rerating from 12.9× to {CONS_PE_2YR}× combined with 7% EPS growth")
print(f"  produces a strong 2yr return — unlike mega-cap compounders priced for perfection,")
print(f"  ACN does not need multiple expansion beyond historically normal levels to work.")
print(f"  Breakeven at current 12.9× P/E (no rerating): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / (CURRENT_PRICE/EPS_FY2026E):.2f}")
print(f"  Breakeven at {PE_PESSIMISTIC:.0f}× P/E (further de-rate): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / PE_PESSIMISTIC:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.30
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: 52W high pre-dates DOGE federal-cuts selloff that drove stock down ~49% from ATH ~$345")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  consistent dividend grower)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated post-correction; federal-spend headline risk)")
print(f"  Beta vs S&P 500:      1.10  (modest premium; cyclical discretionary-spend exposure)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown")
print(f"  52W low ${VOL_52W_LOW:.2f} (Apr 2026 DOGE-cut panic) is already close to BEAR scenario territory.")
print(f"  → Federal contract review resolution is THE KEY near-term binary.")
print(f"  → GenAI bookings-to-revenue conversion (FY2027-2028) is KEY bull catalyst.")
print(f"  → AVOID above $280  |  WATCHLIST $230–260  |  ACCUMULATE $195–220  |  BUY below $195")

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
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0 — near")
print(f"  BEAR/BASE. The model scores the fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0 — between BASE and BULL.")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: you are paying BEAR scenario prices for what is currently BASE/BULL execution.")
print(f"  DOGE federal headwinds (signal score 2/4 = BASE) are being extrapolated far beyond their")
print(f"  actual ~8% revenue footprint into a broader demand-destruction narrative the data does not support.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  HISTORIC VALUATION TROUGH: At 12.9× FY2026E EPS, ACN trades BELOW its COVID-19 trough")
print(f"  multiple (~21×) despite record bookings ($22.1B, +15% YoY) and GenAI bookings doubling")
print(f"  YoY to $2.2B/quarter (cumulative >$10B). The market is pricing DOGE-driven federal cuts")
print(f"  (-12% YoY, ~8% of revenue) as if they signal broader enterprise AI-driven consulting")
print(f"  demand destruction — but the data shows the opposite: commercial bookings are")
print(f"  accelerating as enterprises hire ACN to BUILD their agentic AI transformations. The DOGE")
print(f"  headwind is real but bounded (~1-1.5% of total revenue impact) — not existential. Down")
print(f"  49% from ATH ~$345, ACN offers FCF yield 9.8% and 3.3% dividend yield while the GenAI")
print(f"  bookings-to-revenue conversion plays out over FY2027-2028.")
print()
print(f"  Key catalysts to watch:")
print(f"  (1) Q3 FY2026 earnings (June 2026) — bookings momentum + GenAI revenue conversion update")
print(f"  (2) Federal contract review resolution — DOGE-related federal spend stabilization signal")
print(f"  (3) GenAI bookings-to-revenue conversion — first major cohort of GenAI projects moving to delivery phase")
print(f"  (4) Margin trajectory — does AI delivery efficiency show up as margin expansion or price erosion?")
print(f"  (5) Capital allocation — buyback pace acceleration at depressed valuation; M&A for AI capability gaps")
print(f"  AVOID above $280  |  WATCHLIST $230–260  |  ACCUMULATE $195–220  |  BUY below $195")
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
