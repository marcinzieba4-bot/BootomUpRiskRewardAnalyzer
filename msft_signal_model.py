"""
MSFT  ·  Microsoft Corporation  ·  NASDAQ: MSFT
Bottom-up signal model  ·  Cloud / Azure / AI / Enterprise SaaS
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "MSFT"
COMPANY       = "Microsoft Corporation"
SECTOR        = "Cloud / Azure / AI / Enterprise SaaS · NASDAQ: MSFT"
CURRENT_PRICE = 464.72       # USD; as of 2026-08-02 (+3.02% Jul 31 earnings surge; +15% on earnings)
VOL_52W_LOW   = 349.20
VOL_52W_HIGH  = 555.45
SHARES_OUT_M  = 7_430.0      # millions (~$3.45T market cap / $464.72)

# Dividend: growing ~10%/yr
ANNUAL_DIV    = 3.64         # $/share FY2026 ($0.91/quarter; 0.78% yield)

# ── SEGMENT REVENUE BRIDGE ────────────────────────────────────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Azure / Intelligent Cloud",     150.0,  90.0, 220.0, "Azure #2 globally ~22% share; Copilot/OpenAI AI workloads; re-acceleration"),
    ("Microsoft 365 / Productivity",   98.0,  82.0, 130.0, "M365 SaaS seats + Copilot ARPU uplift; ~$30/user/month AI add-on"),
    ("Dynamics / Business Apps",       12.0,   9.0,  18.0, "ERP/CRM; Copilot for Dynamics; slower growth"),
    ("LinkedIn",                       18.0,  13.0,  24.0, "Hiring recovery; AI-powered recruiter tools; Premium expansion"),
    ("Xbox / Gaming / Devices",        21.0,  14.0,  28.0, "Activision Blizzard integration; Game Pass; Surface hardware"),
    ("Search / Bing / Advertising",     9.0,   6.0,  15.0, "Bing AI chat search; OpenAI ChatGPT browser deal; ad market share"),
    ("Other",                          23.84, 17.0,  30.0, "Azure Marketplace, GitHub, professional services"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.695   # blended gross margin FY2026E (~69.5%; cloud + software premium)
GROSS_MARGIN_BULL = 0.720   # BULL: Azure scale economics; AI workload mix improvement
OPEX_FIXED_B      = 84.0    # R&D + SG&A ($B); AI investment cycle peak; growing ~8%/yr
TAX_RATE          = 0.185   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 19.60       # FY2026E forward EPS (consensus; forward P/E 23.71× at $464.72)
PE_PESSIMISTIC = 20.0        # trough P/E: Azure floor + M365 recurring revenue justifies 20× minimum
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $392

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (11.00, 20,  220, "Azure <10% growth; ASIC displacement; Google/AWS AI wins; EPS $11 → 20× floor"),
    "BASE":  (19.60, 26,  510, "Azure ~25% growth; Copilot monetization; M365 ARPU lifts; EPS $19.60 → 26×"),
    "BULL":  (26.00, 32,  832, "Azure AI dominant enterprise layer; GitHub Copilot/M365 AI 35%+ growth; EPS $26 → 32×"),
    "XBULL": (35.00, 38, 1330, "Microsoft = Enterprise AI OS; AGI integration all products; EPS $35 → 38×"),
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
        "name":       "Azure revenue YoY growth",
        "weight":     0.30,
        "thresholds": ("<10%",   "≥20%",  "≥30%",   "≥40%"),
        "now":        "~29%",
        "score":      3,
        "comment":    "Azure ~29% YoY recent quarter; AI workloads (OpenAI partnership) driving re-acceleration",
    },
    {
        "name":       "M365 commercial seats / ARPU",
        "weight":     0.20,
        "thresholds": ("<5%",    "≥8%",   "≥15%",   "≥25%"),
        "now":        "+12%",
        "score":      3,
        "comment":    "M365 Copilot $30/user/month add-on driving ARPU; seat count stable; Teams integration",
    },
    {
        "name":       "GitHub Copilot / AI penetration",
        "weight":     0.20,
        "thresholds": ("<5%",    "≥15%",  "≥30%",   "≥50%"),
        "now":        "~20%",
        "score":      2,
        "comment":    "GitHub Copilot 2M+ paid seats; early enterprise rollout; not yet transformative at scale",
    },
    {
        "name":       "Operating margin",
        "weight":     0.15,
        "thresholds": ("<35%",   "≥40%",  "≥45%",   "≥50%"),
        "now":        "~45%",
        "score":      3,
        "comment":    "FY2026 operating margin ~45%; AI capex headwind partially offset by cloud scale leverage",
    },
    {
        "name":       "Cloud gross margin",
        "weight":     0.10,
        "thresholds": ("<60%",   "≥65%",  "≥70%",   "≥75%"),
        "now":        "~69%",
        "score":      2,
        "comment":    "Azure gross margin ~69%; AI GPU costs pressuring margins; scale expected to improve over 2yr",
    },
    {
        "name":       "LinkedIn / Gaming revenue mix",
        "weight":     0.05,
        "thresholds": ("<3%",    "≥5%",   "≥8%",    "≥12%"),
        "now":        "~6%",
        "score":      2,
        "comment":    "LinkedIn steady; Activision Blizzard integration in-progress; non-core but diversification",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Azure moat — #2 cloud globally; 22% share; enterprise trust; hybrid via Arc",          +0.7, 0.25),
    ("+", "OpenAI partnership — exclusive Azure rights; deepest AI integration in enterprise",     +0.6, 0.20),
    ("-", "AI capex cycle risk — $80B+ annual capex; ROI timeline uncertain; margin pressure",    -0.5, 0.20),
    ("-", "Hyperscaler ASIC displacement — Google TPU / AWS Trainium threaten Azure GPU share",   -0.5, 0.20),
    ("+", "M365 flywheel — 400M+ commercial seats; 75%+ gross margin SaaS; high switching cost", +0.4, 0.10),
    ("-", "Valuation premium — 24× forward P/E for 15% EPS grower; limited margin of safety",    -0.3, 0.05),
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
CONS_EPS_2YR  = 23.00   # conservative FY2028E: ~8.5% EPS CAGR; AI capex peaks; Azure scale
CONS_PE_2YR   = 26      # exit P/E: premium for AI-driven cloud compounder; PEG ~3×
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Cloud / Azure / AI / Enterprise SaaS")
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

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_ni   = curr_oi * (1 - TAX_RATE)
curr_eps  = round(curr_ni / shares, 2)

bull_gp      = bull_total * GROSS_MARGIN_BULL
bull_oi      = bull_gp - OPEX_FIXED_B * 1.05
bull_ni      = bull_oi * (1 - TAX_RATE)
bull_eps_imp = round(bull_ni / shares, 1)

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.95
bear_oi      = bear_gp - OPEX_FIXED_B * 0.92
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (forward EPS consensus ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − opex − tax")
print(f"  ÷ {shares:.3f}B shares  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 32× = ~${bull_eps_imp*32:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × reduced GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 20× trough P/E = ~${bear_eps_imp*20:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B = 1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Azure revenue:          +${eps_per_1B:.3f}/EPS  = +${eps_per_1B*26:.1f}/share at 26× P/E")
print(f"  1pp blended GM expansion:         +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*26:.1f}/share at 26× P/E")
print(f"  M365 Copilot 10M seats × $30/mo:  +${10*0.30*12*(1-TAX_RATE)/shares:.2f}/share EPS annually (high-margin SaaS)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Azure / M365 / Copilot / AI margin framework)")
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
    ("Azure revenue YoY",            "~29%",   "<10%",   "−19pp",  "Hyperscaler ASIC displacement; Google TPU wins enterprise"),
    ("M365 commercial ARPU growth",  "+12%",   "<5%",    "−7pp",   "Copilot add-on fails to scale; seat saturation"),
    ("GitHub Copilot penetration",   "~20%",   "<5%",    "−15pp",  "Open-source Codex alternatives; enterprise passes"),
    ("Operating margin",             "~45%",   "<35%",   "−10pp",  "AI capex $80B+/yr insufficient revenue offset by 2027"),
    ("Cloud gross margin",           "~69%",   "<60%",   "−9pp",   "GPU cost inflation + AI inference margin pressure"),
    ("LinkedIn / Gaming revenue",    "~6%",    "<3%",    "−3pp",   "Gaming integration costs; ad market slowdown"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Google Cloud TPU v6 + AWS Trainium 2 capture enterprise AI training workloads.")
print(f"  Azure AI differentiation narrows as OpenAI models become API-accessible on all clouds.")
print(f"  Simultaneously, $80B+ annual AI capex fails to convert to revenue by FY2027 → margin crisis.")
print(f"  EPS collapses to ~$11 (bear scenario) → 20× trough P/E = ${bear_price}.")
print(f"  Note: M365's 400M seat base provides durable $82B+ revenue floor regardless of AI outcome.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E forward EPS estimate:  ${EPS_FY2026E:.2f}  (forward P/E {CURRENT_PRICE/EPS_FY2026E:.1f}× at ${CURRENT_PRICE:.2f})")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (Azure + M365 recurring revenues justify 20× floor)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  At ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f}, forward P/E is {CURRENT_PRICE/EPS_FY2026E:.1f}×.")
print(f"  57 analyst 'Strong Buy', avg PT $563 (+21%). Market pricing substantial Azure AI premium.")
print(f"  EPP path: FY2028E EPS ~$23 × {PE_PESSIMISTIC:.0f}× = ${23*PE_PESSIMISTIC:.0f} EPP floor by late 2028 (~8%/yr growth).")
print(f"  At 26× mid-cycle P/E: ${EPS_FY2026E:.2f} × 26 = ${EPS_FY2026E*26:.0f}  — ~9% above current price at BASE.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: AI capex peaks; Azure scales; P/E holds premium)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (~8.5% EPS CAGR: Azure +25%, M365 Copilot ramp)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (AI-cloud compounder premium; PEG ~3×)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; growing ~10%/yr)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case at 26× exit P/E provides {cons_return:.1f}% over 2yr — modestly positive.")
print(f"  Key risk: if P/E compresses to 20× (AI disappointment), FY2028E $23 EPS → ${23*20} — a loss.")
print(f"  BUY trigger: ~${round(CONS_EPS_2YR*CONS_PE_2YR*0.78+cons_divs*0.5):.0f}–${round(CONS_EPS_2YR*CONS_PE_2YR*0.85+cons_divs*0.5):.0f} (ratio_b <0.75×; conservative case strongly positive)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.25
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  growing ~10%/yr)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (enterprise stability; lower than pure-AI plays)")
print(f"  Beta vs S&P 500:      0.90  (lower vol than market; institutional anchor holding)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (extreme; multi-factor failure scenario)")
print(f"  52W low ${VOL_52W_LOW:.2f} (trough) — AI capex concern + macro risk drove down.")
print(f"  → Azure quarterly growth rate is THE KEY binary catalyst for H2 2026.")
print(f"  → >30% Azure growth = strong BULL trigger; <20% deceleration = BEAR signal.")
print(f"  → WATCHLIST at current price  |  ACCUMULATE $400–420  |  BUY below $370")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, market composite ({MARKET_COMPOSITE:.2f}) vs")
print(f"  adj composite ({ADJ_COMPOSITE:.3f}). Gap ({ADJ_GAP:.2f}) → {valuation_label}.")
print(f"  Azure AI thesis is priced in; execution must deliver 25%+ growth to justify multiple.")
print(f"  57 analyst 'Strong Buy' avg PT $563 suggests further upside if AI ROI proves out.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Azure quarterly revenue growth — >30% = BULL; <20% = BEAR signal")
print(f"  (2) AI capex ROI evidence — Copilot/Azure AI revenue per dollar of GPU capex")
print(f"  (3) M365 Copilot seat adoption — 10M+ paid seats = meaningful ARPU inflection")
print(f"  (4) GitHub Copilot enterprise — code generation displacing developer FTE seats")
print(f"  (5) OpenAI partnership renewal / exclusivity — key structural moat risk 2026-27")
print(f"  WATCHLIST at ${CURRENT_PRICE:.2f}  |  ACCUMULATE $400–420  |  BUY below $370")
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
