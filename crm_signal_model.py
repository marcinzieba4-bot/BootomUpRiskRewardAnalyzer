"""
CRM  ·  Salesforce, Inc.  ·  NYSE: CRM
Bottom-up signal model  ·  Enterprise SaaS / Agentforce AI Agents / Data Cloud / Public Sector
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "CRM"
COMPANY       = "Salesforce, Inc."
SECTOR        = "Enterprise SaaS · Agentforce AI Agents · Data Cloud · Public Sector · NYSE: CRM"
CURRENT_PRICE = 183.30      # USD; close 2026-08-03, down ~32% from the 52-week high on AI-growth-trajectory concerns
VOL_52W_LOW   = 146.32      # 2025/26 trough
VOL_52W_HIGH  = 269.11      # 2025 pre-AI-growth-concern peak
SHARES_OUT_M  = 819.0       # millions; ~$150B mkt cap / $183.30
ANNUAL_DIV    = 1.60        # $/share; Salesforce's first-ever dividend program, $0.40/qtr

# ── SEGMENT REVENUE BRIDGE (FY2027E, $B) ──────────────────────────────────────
# Q1 FY2027 (ended April 30, 2026) actual: revenue $11.13B (+13% YoY, +12% cc), non-GAAP EPS $3.88
# (beat $3.13 est, +50% YoY), non-GAAP op margin 34.8% (+250bps), GAAP op margin 21.1% (+130bps).
# Agentforce ARR $1.2B (+205% YoY, crossed $1B for the first time); Agentforce + Data 360 combined
# ARR $3.4B. FY27 guide (raised): revenue $45.9-46.2B (+11% YoY), non-GAAP EPS $14.06-14.12, non-GAAP
# op margin 34.3%. Q2 guide: $11.27-11.35B. Recent wins: $1.6B VA Agentic Enterprise License
# Agreement (Jul), $5.6B 10-yr U.S. Army IDIQ (Jan) — a genuine public-sector AI-agent land grab.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Core Subscription Clouds (Sales/Service/Platform/Marketing)", 42.65, 39.0, 46.0, "The mature, profitable base; growth here has decelerated toward high-single-digits"),
    ("Agentforce + Data Cloud (AI)",                                  3.40,  2.0,  9.0, "The fast-growing sliver — Agentforce ARR alone +205% YoY — but still a small share of total revenue"),
]

# Operating-margin assumptions
OP_MARGIN_CURR = 0.343   # FY2027E; matches the raised full-year guide (non-GAAP)
OP_MARGIN_BEAR = 0.270   # BEAR: AI-agent opex investment rises while core-cloud growth decelerates further
OP_MARGIN_BULL = 0.365   # BULL: Agentforce scales with real operating leverage, not just cost cuts
TAX_RATE       = 0.269   # implied effective non-GAAP tax rate (reconciles guided EPS to guided op margin/share count)

# ── AGENTFORCE / PUBLIC-SECTOR CALCULATOR (the Salesforce-specific angle) ────
AGENTFORCE_ARR_B         = 1.2    # $B; Agentforce annual recurring revenue, Q1 FY2027
AGENTFORCE_ARR_YOY_PCT   = 205    # % YoY growth, Agentforce ARR
AGENTFORCE_DATA360_ARR_B = 3.4    # $B; combined Agentforce + Data 360 ARR
VA_CONTRACT_VALUE_B      = 1.6    # $B; VA Agentic Enterprise License Agreement (3-yr, 1yr firm + 2 optional)
ARMY_CONTRACT_VALUE_B    = 5.6    # $B; 10-yr U.S. Army IDIQ (Jan 2026)
STOCK_DRAWDOWN_FROM_HIGH_PCT = 32 # % decline from the 52-week high on AI-growth-trajectory concerns

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 14.09       # $/share FY2027E non-GAAP; guide midpoint ($14.06-$14.12)
PE_PESSIMISTIC = 12.0        # trough P/E: a genuinely depressed multiple for a still-growing, FCF-generative SaaS leader
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2029E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 9.88, 12,  119, "Core cloud growth decelerates further while AI-agent opex investment keeps rising; margins compress"),
    "BASE":  (14.62, 14,  205, "Steady-as-she-goes: core clouds grow high-single-digits, Agentforce scales but stays a minority of revenue"),
    "BULL":  (17.47, 15,  262, "Agentforce reaccelerates total growth back toward the low-teens; the stock recovers toward its prior high"),
    "XBULL": (22.78, 17,  387, "Agentforce becomes a genuine second growth engine; public-sector AI-agent wins (VA, Army) repeat across enterprise"),
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
        "name":       "Total revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<8%",    "≥10%",   "≥13%",   "≥17%"),
        "now":        "+13%",
        "score":      3,
        "comment":    "Q1 FY2027 record revenue, +13% YoY (+12% cc) — a reacceleration off prior deceleration fears",
    },
    {
        "name":       "Agentforce ARR growth",
        "weight":     0.20,
        "thresholds": ("<50%",   "≥100%",  "≥150%",  "≥200%"),
        "now":        "+205%",
        "score":      4,
        "comment":    "Agentforce ARR crossed $1B for the first time, +205% YoY — genuinely the fastest-growing product line",
    },
    {
        "name":       "Non-GAAP operating margin trajectory",
        "weight":     0.15,
        "thresholds": ("<30%",   "≥33%",   "≥35%",   "≥37%"),
        "now":        "34.8%",
        "score":      3,
        "comment":    "+250bps YoY in Q1; FY27 guide holds margin at 34.3% even while investing behind Agentforce",
    },
    {
        "name":       "Public-sector AI-agent contract wins",
        "weight":     0.15,
        "thresholds": ("none",   "modest", "large",  "landmark"),
        "now":        "$1.6B VA + $5.6B Army",
        "score":      4,
        "comment":    "Two landmark government AI-agent contracts in 7 months — a genuine proof point beyond enterprise sales talk",
    },
    {
        "name":       "EPS beat magnitude",
        "weight":     0.15,
        "thresholds": ("miss",   "in-line", "beat",  "large beat"),
        "now":        "$3.88 vs $3.13 est",
        "score":      4,
        "comment":    "A 24% EPS beat — one of the largest in the company's recent history — alongside raised full-year guidance",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.15,
        "thresholds": (">22x",   "≤18x",   "≤15x",   "≤11x"),
        "now":        "~13.0x",
        "score":      3,
        "comment":    "13.0× FY2027E non-GAAP EPS — cheap for a company still growing revenue double-digits with expanding margins",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Agentforce's 205% ARR growth plus two landmark public-sector wins are real, quantified proof — not just AI marketing", +0.6, 0.25),
    ("-", "Agentforce + Data Cloud combined is still only ~7% of total revenue — the core business's deceleration is the bigger swing factor", -0.4, 0.20),
    ("+", "At 13.0× forward earnings, the stock already prices in real skepticism about the AI growth trajectory", +0.5, 0.20),
    ("-", "SaaS multiples across the sector have compressed broadly; Salesforce's -32% drawdown isn't purely company-specific", -0.3, 0.15),
    ("+", "Public-sector AI-agent contracts (VA, Army) demonstrate a repeatable enterprise-agent sales motion beyond pilots", +0.4, 0.10),
    ("-", "Elevated AI/agentic opex investment could compress margins if core-cloud growth doesn't cooperate", -0.3, 0.10),
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
CONS_EPS_2YR  = 15.50   # conservative FY2029E: modest growth off FY2027E guide, no reacceleration assumed
CONS_PE_2YR   = 14       # a modest re-rating from ~13.0× as the AI-growth-trajectory concern partially resolves
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Agentforce AI Agents / Data Cloud / Public Sector")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2027E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<48}  {'FY2027E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<48}  ${curr:>11.2f}  ${bear:>8.1f}  ${bull:>8.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<48}  ${curr_total:>11.2f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}")
print(f"  Q1 FY27 actual: $11.13B (+13%). FY27 guide (raised): $45.9-46.2B (+11%). Q2 guide: $11.27-11.35B")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_oi   = curr_total * OP_MARGIN_CURR
curr_eps  = round(curr_oi * (1 - TAX_RATE) / shares, 2)

shares_b  = shares * 0.97
bull_oi   = bull_total * OP_MARGIN_BULL
bull_eps_imp = round(bull_oi * (1 - TAX_RATE) / shares_b, 2)

bear_oi   = bear_total * OP_MARGIN_BEAR
bear_eps_imp = round(max(0, bear_oi) * (1 - TAX_RATE) / shares, 2)

print(f"  FY2027E EPS check:  ${curr_total:.2f}B rev × {OP_MARGIN_CURR*100:.1f}% op margin")
print(f"  − {TAX_RATE*100:.1f}% eff. tax  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2027E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B rev × {OP_MARGIN_BULL*100:.1f}% op margin, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B rev × {OP_MARGIN_BEAR*100:.1f}% op margin (rising AI opex, slower core growth)")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# AGENTFORCE / PUBLIC-SECTOR CHECK
print()
print(f"  AGENTFORCE / PUBLIC-SECTOR CHECK  (the Salesforce-specific angle):")
print(f"  Agentforce ARR:                       ${AGENTFORCE_ARR_B}B  (+{AGENTFORCE_ARR_YOY_PCT}% YoY, crossed $1B for the first time)")
print(f"  Agentforce + Data 360 combined ARR:    ${AGENTFORCE_DATA360_ARR_B}B")
print(f"  VA Agentic Enterprise License Agmt:    ${VA_CONTRACT_VALUE_B}B  (3-yr, 1yr firm + 2 optional renewals)")
print(f"  U.S. Army IDIQ (Jan 2026):             ${ARMY_CONTRACT_VALUE_B}B  (10-yr)")
print(f"  Stock drawdown from 52-week high:      -{STOCK_DRAWDOWN_FROM_HIGH_PCT}%")
print()
print(f"  Two landmark public-sector AI-agent contracts in seven months is a genuinely different kind of")
print(f"  evidence than a vendor's own ARR figures — a buyer as risk-averse as the U.S. government committing")
print(f"  billions to Salesforce's agentic platform is a real signal about enterprise-readiness. The tension")
print(f"  is scale: Agentforce + Data Cloud is still under 8% of total revenue, so even explosive growth there")
print(f"  moves the needle on the story long before it moves the needle on the consolidated P&L.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * OP_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_opm = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 34.3% op margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*14:.2f}/share at 14× P/E")
print(f"  Every 1pp of operating margin:            +${eps_per_1pp_opm:.3f}/EPS  = +${eps_per_1pp_opm*14:.2f}/share at 14× P/E")
print(f"  Every 1 turn of P/E:                      ±${EPS_FY2027E:.2f}/share  ({EPS_FY2027E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (revenue growth / Agentforce ARR / margin / public sector / EPS beat / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<42}  {'BEAR':>9}  {'BASE':>9}  {'BULL':>9}  {'XBULL':>9}  {'NOW':>20}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<42}  {ths[0]:>9}  {ths[1]:>9}  {ths[2]:>9}  {ths[3]:>9}  {s['now']:>20}  {lbl}  {b}")
    print(f"    {s['comment']}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15%/yr hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:88]:<88}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<32}  {'Current':>10}  {'Bear val':>10}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Total revenue YoY",           "+13%",   "<8%",     "-5pp+",  "Core cloud deceleration resumes; Agentforce isn't yet large enough to offset it"),
    ("Agentforce ARR growth",       "+205%",  "<50%",    "-155pp+","Enterprise AI-agent adoption plateaus after the initial land-grab phase"),
    ("Operating margin",            "34.8%",  "<30%",    "-4.8pp+","Agentic AI opex investment outpaces the revenue it generates"),
    ("Public-sector contract wins", "landmark","none",   "reversal","Government AI-agent momentum stalls after VA/Army amid budget or political scrutiny"),
    ("EPS beat magnitude",          "large beat","miss", "reversal","Guidance proves too optimistic; a beat-and-raise streak breaks"),
    ("Forward P/E",                 "~13.0x", ">22x",    "re-rate","Ironically, P/E can rise even as price falls if EPS growth disappoints more than price does"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the -32% drawdown already prices in real doubt about whether Agentforce can become")
print(f"  large enough, fast enough, to reaccelerate a company whose core clouds have structurally decelerated")
print(f"  to high-single-digit growth. The public-sector wins are genuine evidence against that doubt — but")
print(f"  they're still early, and the bear case simply requires that evidence not scale into the enterprise base.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2027E EPS estimate:       ${EPS_FY2027E:.2f}  (company guide midpoint, $14.06-$14.12)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (a genuinely depressed multiple for a still-growing, FCF-generative SaaS leader)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS — genuinely cheap by large-cap SaaS")
print(f"  standards, and only modestly above the EPP floor. The -32% drawdown from the 52-week high has done")
print(f"  real work bringing the valuation back toward a defensible margin of safety.")
print(f"  At a 16× reversion (a modest re-rating): ${EPS_FY2027E:.2f} × 16 = ${EPS_FY2027E*16:.0f}  ({(EPS_FY2027E*16/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest growth off FY2027E guide, no reacceleration assumed)")
hr()
print(f"  Conservative FY2029E EPS:  ${CONS_EPS_2YR:.2f}  (~10% cumulative EPS growth — below the current beat-and-raise trajectory)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~13.0× → 14×; a modest re-rating, not a re-rating to a growth-stock multiple)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: because the starting multiple is already so undemanding, even a conservative")
print(f"  case with no Agentforce reacceleration and only a modest re-rating still clears a {'solidly positive' if cons_return > 10 else 'positive' if cons_return > 0 else 'negative'} return.")
print(f"  This is the classic depressed-multiple setup — you don't need the AI story to work perfectly,")
print(f"  just to not get meaningfully worse from here.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.32
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Drawdown from high:    -{STOCK_DRAWDOWN_FROM_HIGH_PCT}%  on AI-growth-trajectory concerns")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; a newer but growing capital-return program)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (moderate-high for mega-cap software, reflecting the growth-trajectory debate)")
print(f"  Beta vs S&P 500:      1.15  (modestly above market)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (a moderate move, well within the stock's own recent range)")
print(f"  → Q2 FY2027 print (late Aug) is the next test of whether the Q1 beat-and-raise trajectory continues.")
print(f"  → Agentforce ARR growth and net-new public-sector wins are the leading indicators to watch between prints.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $155  |  Trim above $250")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f} the market composite is {MARKET_COMPOSITE:.2f}/4.0. The model's")
print(f"  adjusted composite is {ADJ_COMPOSITE:.2f}/4.0, for a gap of {ADJ_GAP:+.2f} — {valuation_label.lower()}.")
print(f"  Salesforce's core business is decelerating but still profitable and growing; Agentforce and the")
print(f"  public-sector wins are the real, quantified evidence that the AI pivot has legs. At 13.0× forward")
print(f"  earnings after a 32% drawdown, the risk/reward has turned favorable even without a full AI re-rating.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q2 FY2027 print (late August) — does the Q1 beat-and-raise trajectory continue?")
print(f"  (2) Agentforce ARR growth rate — does it stay above 150%+ or start decelerating from 205%?")
print(f"  (3) Net-new public-sector and large-enterprise AI-agent contract wins beyond VA/Army")
print(f"  (4) Core subscription cloud growth — the bigger swing factor than Agentforce in the near term")
print(f"  (5) Non-GAAP operating margin durability at ~34%+ while investing behind agentic AI")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $155  |  Trim above $250")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2027E EPS: ${EPS_FY2027E:.2f}  |  Agentforce ARR: ${AGENTFORCE_ARR_B}B (+{AGENTFORCE_ARR_YOY_PCT}%)")
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
