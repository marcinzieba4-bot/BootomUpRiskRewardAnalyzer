"""
META  ·  Meta Platforms, Inc.  ·  NASDAQ: META
Bottom-up signal model  ·  Social Media / Digital Advertising / AI Infrastructure
Date: 2026-05-31
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "META"
COMPANY       = "Meta Platforms, Inc."
SECTOR        = "Social Media · Digital Advertising · AI Infrastructure · Reality Labs · NASDAQ: META"
CURRENT_PRICE = 590.00       # USD; as of 2026-05-31
VOL_52W_LOW   = 432.80       # April 2026 tariff/tech selloff trough
VOL_52W_HIGH  = 741.50       # December 2025 AI rally peak
SHARES_OUT_M  = 2530.0       # millions; post-aggressive buyback program

# Dividend: initiated Q1 2024 at $0.50/quarter
ANNUAL_DIV    = 2.00         # $/share FY2026

# ── ARPU BRIDGE CONSTANTS (company-specific calculator) ──────────────────────
# (region, DAU_M, arpu_current_$/yr, arpu_bull_$/yr, description)
GEO_DATA = [
    ("North America",  265.0,  265.0,  305.0, "Advantage+ ROI gains; Reels shopping; AI creative tools"),
    ("Europe",         360.0,   95.0,  118.0, "DMA headwinds partially offset; Reels growth; Advantage+ rising"),
    ("Asia-Pacific", 1_310.0,   34.0,   48.0, "India WhatsApp Business; SE Asia e-commerce; AI ad tools"),
    ("Rest of World",1_415.0,   18.0,   25.0, "LatAm WhatsApp dominant; Africa mobile-first; click-to-message"),
]

WHATSAPP_BUSI_CURR_B  =  8.0   # WhatsApp Business + Click-to-Message ads ($B/yr)
THREADS_ADS_CURR_B    =  1.5   # Threads advertising ($B/yr; just ramping)
WHATSAPP_BUSI_BULL_B  = 15.0   # BULL scenario WhatsApp Business
THREADS_ADS_BULL_B    =  4.5   # BULL scenario Threads

FAMILY_OP_MARGIN_CURR = 0.505  # Family of Apps adj operating margin (FY2026E)
FAMILY_OP_MARGIN_BULL = 0.530  # scale + AI efficiency at BULL revenue
REALITY_LABS_CURR_B   = 20.0   # annual Reality Labs operating loss ($B)
REALITY_LABS_BULL_B   = 16.0   # BULL: Quest scale + cost efficiency
TAX_RATE_EFF          = 0.17   # effective rate (offshore structures, R&D credits)

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 28.00   # FY2026E adj EPS (consensus ~$27.50–$28.50)
PE_TROUGH = 15      # min viable P/E at crisis (2022 trough ~10×; floor here 15× for stable network)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $420

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
# (adj_eps, pe_multiple, price, narrative)
SCENARIOS = {
    "BEAR":  (14.00, 14,  200, "FTC breakup + ad recession + AI capex write-off; EPS $14 → 14× distress P/E"),
    "BASE":  (28.00, 22,  620, "AI ads delivering; DAP +6%; EPS $28 → 22× mid-cycle P/E; FY2026E consensus"),
    "BULL":  (38.00, 26,  990, "AI monetisation inflects; int'l ARPU +40%; $38 EPS → 26× premium P/E"),
    "XBULL": (50.00, 30, 1500, "Reality Labs + AI platform + WhatsApp global; $50 EPS → 30× peak P/E"),
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
        "name":       "Family Daily Active People (DAP) — YoY growth",
        "weight":     0.25,
        "thresholds": ("<3%",   "≥5%",   "≥8%",    "≥12%"),
        "now":        "+6.5%",
        "score":      2,
        "comment":    "3.35B DAP Q1 2026; WhatsApp inflecting in South Asia; Facebook stable in West",
    },
    {
        "name":       "North America ARPU — YoY growth",
        "weight":     0.25,
        "thresholds": ("<3%",   "≥5%",   "≥12%",   "≥20%"),
        "now":        "+14%",
        "score":      3,
        "comment":    "Advantage+ driving +14% YoY; AI ad tools improving advertiser ROAS measurably",
    },
    {
        "name":       "Advantage+ AI campaigns — share of Family of Apps ad revenue",
        "weight":     0.20,
        "thresholds": ("<20%",  "≥35%",  "≥55%",   "≥72%"),
        "now":        "~50%",
        "score":      2,
        "comment":    "~50% adoption; strong but just below BULL threshold; conversion uplift 20-30% vs manual",
    },
    {
        "name":       "Reality Labs quarterly loss — annualised run-rate ($B/yr)",
        "weight":     0.15,
        "thresholds": (">$25B", "≤$22B", "≤$16B",  "≤$8B"),
        "now":        "~$20B",
        "score":      2,
        "comment":    "-$5.0B/qtr → -$20B/yr; within FY2026 guidance; Quest 3 steady, not mass-market",
    },
    {
        "name":       "Global digital advertising market growth — YoY",
        "weight":     0.10,
        "thresholds": ("<3%",   "≥5%",   "≥10%",   "≥15%"),
        "now":        "+8%",
        "score":      2,
        "comment":    "+8% YoY; tariff uncertainty capped from +11% trajectory; social/video gaining share",
    },
    {
        "name":       "WhatsApp Business + Click-to-Message ad revenue ($B/yr)",
        "weight":     0.05,
        "thresholds": ("<$4B",  "≥$6B",  "≥$12B",  "≥$20B"),
        "now":        "~$8B",
        "score":      2,
        "comment":    "$8B annualised; India + LatAm driving growth; deepening commerce integration",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Network effects moat — 3.35B daily users; default social/messaging globally; 10+ yr rebuild",   +0.8, 0.25),
    ("+", "AI monetisation compound — Advantage+ 20-30% ROAS uplift; advertiser wallet share rising",       +0.6, 0.20),
    ("-", "Reality Labs structural drain — $20B/yr losses; Quest <5% TAM; payoff horizon undefined",        -0.7, 0.20),
    ("-", "FTC/regulatory breakup risk — Instagram+WhatsApp divestiture trial; EU DMA fines; GDPR",         -0.5, 0.20),
    ("+", "AI capex infrastructure moat — $65B data centers; custom MTIA silicon; inference scale lead",    +0.4, 0.10),
    ("-", "AI capex ROI uncertainty — FY2026 capex $65-70B; Llama revenue model unclear; equity risk",      -0.3, 0.05),
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
    valuation_label = "MODESTLY OVERVALUED"

# ── RATIO B ───────────────────────────────────────────────────────────────────
bear_price   = SCENARIOS["BEAR"][2]
bull_price   = SCENARIOS["BULL"][2]
downside_pct = (CURRENT_PRICE - bear_price) / CURRENT_PRICE
upside_pct   = (bull_price - CURRENT_PRICE) / CURRENT_PRICE
ratio_b      = round(downside_pct / upside_pct, 2)

if ratio_b < 0.75:
    signal_short, signal_full = "BUY",       "◉ BUY"
elif ratio_b < 1.10:
    signal_short, signal_full = "ACCUMULATE","◎ ACCUMULATE"
elif ratio_b < 1.75:
    signal_short, signal_full = "WATCHLIST", "◐ WATCHLIST"
else:
    signal_short, signal_full = "AVOID",     "✕ AVOID"

# ── CONSERVATIVE GROWTH (2-yr) ────────────────────────────────────────────────
CONS_EPS_2YR = 25.00   # conservative FY2028E: AI capex compresses margins; RL still -$22B
CONS_PE_2YR  = 21      # floor multiple (META network moat commands premium; even bears pay 20×)
cons_equity  = CONS_EPS_2YR * CONS_PE_2YR
cons_divs    = ANNUAL_DIV * 2
cons_total   = cons_equity + cons_divs
cons_return  = round((cons_total - CURRENT_PRICE) / CURRENT_PRICE * 100, 1)
cons_annual  = round(cons_return / 2, 1)

# ─────────────────────────────────────────────────────────────────────────────
#  OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
W = 72

def hr(): print("  " + "─" * W)
def bar(score):
    return "█" * score + "░" * (4 - score)

print()
print("═" * (W + 4))
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Social Media / Digital Advertising / Technology")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① AI MONETISATION & ARPU CONVERGENCE BRIDGE ──────────────────────────
print()
print("  AI MONETISATION & ARPU CONVERGENCE BRIDGE  (current → BULL $990 scenario)")
hr()

curr_geo_rev = sum(dau * arpu for _, dau, arpu, _, _ in GEO_DATA) / 1000   # $B
bull_geo_rev = sum(dau * arpu_b for _, dau, _, arpu_b, _ in GEO_DATA) / 1000
curr_total   = curr_geo_rev + WHATSAPP_BUSI_CURR_B + THREADS_ADS_CURR_B
bull_total   = bull_geo_rev + WHATSAPP_BUSI_BULL_B + THREADS_ADS_BULL_B

print(f"  {'Region':<16}  {'DAU (M)':>8}  {'Curr $/u/yr':>12}  {'Bull $/u/yr':>12}  {'Δ Revenue':>10}")
hr()
for region, dau, arpu, arpu_b, desc in GEO_DATA:
    delta_b = (dau * (arpu_b - arpu)) / 1000
    print(f"  {region:<16}  {dau:>7.0f}M   ${arpu:>8.0f}        ${arpu_b:>6.0f}       +${delta_b:>4.1f}B")
    print(f"    {desc}")

wapp_delta   = WHATSAPP_BUSI_BULL_B - WHATSAPP_BUSI_CURR_B
thread_delta = THREADS_ADS_BULL_B   - THREADS_ADS_CURR_B
print(f"  {'WhatsApp Business':<16}  {'—':>8}   ${WHATSAPP_BUSI_CURR_B:.1f}B                ${WHATSAPP_BUSI_BULL_B:.1f}B      +${wapp_delta:.1f}B")
print(f"  {'Threads Ads':<16}  {'—':>8}   ${THREADS_ADS_CURR_B:.1f}B                 ${THREADS_ADS_BULL_B:.1f}B      +${thread_delta:.1f}B")
hr()
rev_delta = bull_total - curr_total
print(f"  TOTAL           3,350M avg                ${curr_total:.1f}B         ${bull_total:.1f}B    +${rev_delta:.1f}B")
print()

# BULL EPS bridge
bull_oi      = bull_total * FAMILY_OP_MARGIN_BULL - REALITY_LABS_BULL_B
bull_ni      = bull_oi * (1 - TAX_RATE_EFF)
shares_bull  = SHARES_OUT_M / 1000 * 0.97   # ~3% net buyback over 2yr
bull_eps_imp = round(bull_ni / shares_bull, 1)

print(f"  BULL revenue ${bull_total:.1f}B × {FAMILY_OP_MARGIN_BULL*100:.1f}% FoA margin = ${bull_total*FAMILY_OP_MARGIN_BULL:.1f}B adj OI")
print(f"  Less: Reality Labs ${REALITY_LABS_BULL_B:.0f}B loss  →  pre-tax income ${bull_oi:.1f}B")
print(f"  After {TAX_RATE_EFF*100:.0f}% eff. tax:  ${bull_ni:.1f}B net income  ÷  {shares_bull:.2f}B shares (post-buyback)")
print(f"  Implied BULL EPS: ~${bull_eps_imp:.1f}/share  →  at 26× = ~${bull_eps_imp*26:.0f}  ✓ (vs BULL scenario $990)")
print()

# Sensitivity table
na_dau  = GEO_DATA[0][1]   # 265M
rev_per_10_na_arpu = na_dau * 10 / 1000   # $B
eps_per_10_na      = rev_per_10_na_arpu * (1 - TAX_RATE_EFF) / (SHARES_OUT_M / 1000)
adv_plus_5pp_rev   = curr_total * 0.02   # ~2% incremental revenue per 5pp adoption
eps_per_adv_plus   = adv_plus_5pp_rev * (1 - TAX_RATE_EFF) / (SHARES_OUT_M / 1000)
eps_per_rl_1b      = 1.0 * (1 - TAX_RATE_EFF) / (SHARES_OUT_M / 1000)
pe_base            = SCENARIOS["BASE"][1]

print(f"  KEY SENSITIVITIES:")
print(f"  Every $10 increase in NA ARPU (${GEO_DATA[0][2]:.0f} → ${GEO_DATA[0][2]+10:.0f}):  +${rev_per_10_na_arpu:.2f}B rev  =  +${eps_per_10_na:.2f}/EPS  =  +${eps_per_10_na*pe_base:.0f}/share at {pe_base}×")
print(f"  Every 5pp Advantage+ gain (50%→55%):  ~+${adv_plus_5pp_rev:.1f}B rev  =  +${eps_per_adv_plus:.2f}/EPS  =  +${eps_per_adv_plus*pe_base:.0f}/share at {pe_base}×")
print(f"  Reality Labs $1B annual loss reduction:  +${eps_per_rl_1b:.2f}/EPS  =  +${eps_per_rl_1b*pe_base:.1f}/share at {pe_base}×")
print(f"  At BULL: $241B rev × 53% margin − $16B RL − tax → ~$38/EPS × 26× = ~$990 BULL")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (AI advertising + engagement + regulatory drag framework)")
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
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>7}  Trigger")
hr()
bear_triggers = [
    ("Family DAP YoY growth",                                "+6.5%",  "<3%",    "−3.5pp", "Global user stagnation; TikTok gains in US/EU…"),
    ("North America ARPU YoY",                               "+14%",   "<3%",    "−11pp",  "Ad market recession; CPM crash 25%; boycott…"),
    ("Advantage+ AI campaign share",                         "~50%",   "<20%",   "−30pp",  "EU DMA bans cross-app targeting; US privacy law…"),
    ("Reality Labs loss (annualised)",                       "~$20B",  ">$25B",  "+$5B",   "Spending acceleration; no Q headset traction…"),
    ("Global digital ad market growth",                      "+8%",    "<3%",    "−5pp",   "US/EU recession; brands cut digital; tariffs…"),
    ("WhatsApp Business revenue ($B/yr)",                    "~$8B",   "<$4B",   "−$4B",   "Regulatory shutdown; DMA blocks C2M ads in EU…"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: FTC wins Instagram + WhatsApp divestiture case (expected ruling Q4 2026).")
print(f"  Simultaneously, US enters recession — ad CPMs collapse 25%; FY2026 EPS cut to ~$14.")
print(f"  At 14× distress P/E (2022 analogue ~10×; floor higher here due to WhatsApp cash flow) = ${bear_price}.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS × min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPP_EPS:.2f}  (consensus $27.50–$28.50)")
print(f"  Min viable P/E at trough:       {PE_TROUGH}×  (2022 actual was ~10× — exceptional; floor here 15×)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  +{epp_gap_pct:.0f}% premium to EPP means the stock prices in significant growth.")
print(f"  Bear ${bear_price} is BELOW EPP ${EPP:.0f} — the bear scenario implies distress pricing below trough asset value.")
print(f"  EPP path up: FY2027E EPS ~${EPP_EPS+3:.0f} × {PE_TROUGH}× = ${(EPP_EPS+3)*PE_TROUGH:.0f} EPP by late 2027.")
print(f"  EPP at 18× (mid-cycle floor): ${EPP_EPS:.0f} × 18 = ${EPP_EPS*18:.0f} → real asset floor much higher than $420.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: AI capex headwind persists; Reality Labs -$22B/yr)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (capex D&A drag; RL losses sustained; slower growth)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (META commands premium even in conservative — network floor)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f} × 2; buyback-adjusted)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is NEGATIVE — AI capex ($65-70B/yr) delays EPS compounding.")
print(f"  Breakeven requires FY2028E EPS ≥${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.1f} at {CONS_PE_2YR}× P/E.")
print(f"  Dividend yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}% is token — this is a growth story, not income.")
print(f"  BUY trigger: $450–490 zone where conservative 2yr flips positive at 21× P/E.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.35
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%  —  symbolic; initiated 2024)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (high; regulatory binary + AI capex sentiment swings)")
print(f"  Beta vs S&P 500:      1.20  (above market; regulatory binary events; AI capex narrative)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (well within historical range)")
print(f"  52W low ${VOL_52W_LOW:.2f} already a −{(VOL_52W_HIGH-VOL_52W_LOW)*0.5/CURRENT_PRICE*100:.0f}% peak-to-trough — META can move violently.")
print(f"  → Regulatory overhang (FTC ruling) is the KEY binary: win = stable, lose = −30% or more.")
print(f"  → Reality Labs path-to-breakeven is the KEY re-rating catalyst for BULL scenario.")
print(f"  → ACCUMULATE ${VOL_52W_LOW+20:.0f}–${round(CURRENT_PRICE*1.05,0):.0f}  |  BUY below $490  |  TRIM above ${VOL_52W_HIGH:.0f}")

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
    desc = SCENARIOS[s][3][:45]
    print(f"  {s:<10}  ${pr:>6}  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): ${ev_adj:.0f}  /  Proxy EV: ${ev_prx:.0f}  /  Market EV: ${ev_mkt:.0f}  /  Current: ${CURRENT_PRICE:.0f}")
hr()
print(f"  Downside  (→ Bear ${bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull ${bull_price}):   {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b:.2f}x")
print(f"  Signal    :  {signal_full}")
print()
print(f"  NOTE: Proxy/Adj composite (2.35) ≈ Market composite ({MARKET_COMPOSITE:.2f}) → model says META is FAIRLY VALUED.")
print(f"  ACCUMULATE signal driven by Ratio B asymmetry: upside {upside_pct*100:.1f}% > downside {downside_pct*100:.1f}%.")
print(f"  The BULL/XBULL scenarios are more monetarily powerful (+$400–910/share) vs BEAR (−$390).")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) FTC ruling on Instagram+WhatsApp divestiture (binary; watch Q3/Q4 2026)")
print(f"  (2) Reality Labs quarterly loss trajectory → <$4B/qtr = BULL threshold for re-rating")
print(f"  (3) Advantage+ share >55% of ad revenue = BULL upgrade; watch Q2 2026 earnings (Jul)")
print(f"  (4) International ARPU exit rate: Asia-Pacific $34→$40+/yr = +$8B incremental revenue")
print(f"  ACCUMULATE $453–{round(CURRENT_PRICE*1.05,0):.0f}  |  BUY below $490 (conservative case positive)  |  AVOID above ${VOL_52W_HIGH:.0f}")
print("═" * (W + 4))
print()

# ── EXPORT ────────────────────────────────────────────────────────────────────
RESULT = {
    "ticker":            TICKER,
    "signal":            signal_full,
    "signal_short":      signal_short,
    "price":             CURRENT_PRICE,
    "epp_gap_pct":       epp_gap_pct,
    "ratio_b":           ratio_b,
    "ratio_b_fmt":       f"{ratio_b:.2f}x",
    "adj_composite":     ADJ_COMPOSITE,
    "market_composite":  MARKET_COMPOSITE,
    "adj_gap":           ADJ_GAP,
    "valuation":         valuation_label,
    "cons_return_2yr":   cons_return,
}

if __name__ == "__main__":
    pass
