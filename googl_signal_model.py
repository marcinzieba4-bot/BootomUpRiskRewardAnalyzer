"""
GOOGL  ·  Alphabet Inc.  ·  NASDAQ: GOOGL
Bottom-up signal model  ·  Google Search / YouTube / Google Cloud / AI
Date: 2026-05-31
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "GOOGL"
COMPANY       = "Alphabet Inc."
SECTOR        = "Google Search · YouTube · Google Cloud · AI Infrastructure · NASDAQ: GOOGL"
CURRENT_PRICE = 172.00       # USD; as of 2026-05-31
VOL_52W_LOW   = 148.20       # April 2026 tariff/AI-competition trough
VOL_52W_HIGH  = 212.40       # December 2025 AI rally peak
SHARES_OUT_M  = 12_080.0     # millions; includes A+B+C classes; post-buyback

# Dividend: initiated Q1 2024 at $0.20/quarter
ANNUAL_DIV    = 0.80         # $/share FY2026

# ── SEARCH DISRUPTION vs CLOUD OFFSET CONSTANTS (company-specific calculator) ─
# Revenue breakdown FY2026E ($B)
SEARCH_REV_B      = 195.0   # Google Search & other (incl. AI Overviews ads)
YOUTUBE_REV_B     =  38.0   # YouTube Ads
NETWORK_REV_B     =  31.0   # Google Network (AdSense, AdMob; structural decline)
SUBSCRIPTIONS_B   =  39.0   # Google One, Workspace, Pixel/Nest devices
CLOUD_REV_B       =  52.0   # Google Cloud (GCP + Workspace Enterprise)
OTHER_BETS_LOSS_B =   1.5   # Other Bets net operating loss ($B/yr); Waymo pre-scale

SEARCH_OP_MARGIN  = 0.42    # Search operating margin (powerful network leverage)
CLOUD_OP_MARGIN   = 0.32    # Cloud margin (up from 28% as scale improves)
CLOUD_GROWTH_RATE = 0.28    # 28% YoY Google Cloud growth (Q1 2026 run-rate)
TAX_RATE          = 0.18    # effective rate (R&D credits, offshore, GILTI)

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 10.50   # FY2026E adj EPS (consensus $10.20–$10.80)
PE_TROUGH = 14      # min P/E at crisis trough (2022 was ~14–15×; search moat prevents <12×)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $147

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 6.00, 13,   80, "DOJ structural remedy + AI query loss −25%; EPS $6 → 13× distress P/E"),
    "BASE":  (10.50, 19,  200, "Search holds; Cloud $85B; AI Overviews monetising; EPS $10.50 → 19× P/E"),
    "BULL":  (15.00, 21,  315, "Gemini AI monetisation inflects; Cloud #2 share; $15 EPS → 21× premium P/E"),
    "XBULL": (20.00, 26,  520, "Waymo + AI agents + full AI platform; $20 EPS → 26× peak P/E"),
}

# ── SOFTMAX ───────────────────────────────────────────────────────────────────
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
SIGNALS = [
    {
        "name":       "Google Search revenue — YoY growth (AI Overviews era)",
        "weight":     0.25,
        "thresholds": ("<2%",    "≥6%",   "≥11%",   "≥16%"),
        "now":        "+9%",
        "score":      2,
        "comment":    "+9% YoY; AI Overviews boosting session depth; monetization ratio improving to ~0.90×",
    },
    {
        "name":       "Google Cloud revenue — YoY growth rate",
        "weight":     0.25,
        "thresholds": ("<10%",   "≥20%",  "≥28%",   "≥38%"),
        "now":        "+29%",
        "score":      3,
        "comment":    "+29% YoY; AI workloads driving GCP demand; Vertex AI + Gemini API adoption surging",
    },
    {
        "name":       "AI Overviews monetisation — revenue/query vs standard search",
        "weight":     0.20,
        "thresholds": ("<0.6×",  "≥0.8×", "≥1.05×", "≥1.3×"),
        "now":        "~0.90×",
        "score":      2,
        "comment":    "~0.90× parity; improving from 0.75× launch; AI ad slots rolling out in US/EU",
    },
    {
        "name":       "DOJ antitrust remedy severity (1=structural, 4=dismissed)",
        "weight":     0.15,
        "thresholds": ("struct.", "behav.", "consent","dismissed"),
        "now":        "behav.",
        "score":      2,
        "comment":    "Aug 2024 ruling; remedy phase ongoing; behavioral (no Chrome/Android divestiture)",
    },
    {
        "name":       "YouTube + Shorts ad revenue — YoY growth",
        "weight":     0.10,
        "thresholds": ("<5%",    "≥8%",   "≥15%",   "≥22%"),
        "now":        "+16%",
        "score":      3,
        "comment":    "+16% YoY; Shorts monetisation inflecting; connected TV gaining CTV ad budgets",
    },
    {
        "name":       "Gemini API + AI product revenue — annualised ($B/yr)",
        "weight":     0.05,
        "thresholds": ("<$2B",   "≥$4B",  "≥$8B",   "≥$15B"),
        "now":        "~$5B",
        "score":      2,
        "comment":    "~$5B; Workspace AI Premium, Gemini API, NotebookLM Enterprise; growing rapidly",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Search network moat — unmatched query understanding; 90% global share; advertiser lock-in",      +0.9, 0.25),
    ("+", "Google Cloud AI advantage — TPU v5/6; Vertex AI; Gemini natively embedded; #3 → #2 trajectory",  +0.6, 0.20),
    ("-", "DOJ search monopoly remedy — behavioral restrictions likely; Chrome/Android structural risk",     -0.7, 0.20),
    ("-", "AI search disruption — OpenAI/Perplexity eroding AI-native query share; ChatGPT GPT-4o search",  -0.5, 0.20),
    ("+", "Capital efficiency — $30B+ net cash; $70B buyback auth; FCF ~$80B/yr; no dividend pressure",    +0.5, 0.10),
    ("-", "Other Bets drag — Waymo pre-commercial; $1.5B/yr loss; capital allocation uncertainty",          -0.3, 0.05),
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
CONS_EPS_2YR = 11.00    # conservative FY2028E: modest search growth; DOJ remedies biting
CONS_PE_2YR  = 16       # floor multiple (search monopoly still commands quality premium)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Google Search / Cloud / AI / Technology")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEARCH DISRUPTION vs CLOUD OFFSET ANALYSIS ────────────────────────────
print()
print("  SEARCH DISRUPTION vs GOOGLE CLOUD OFFSET ANALYSIS  (the core GOOGL tension)")
hr()

total_rev_b = SEARCH_REV_B + YOUTUBE_REV_B + NETWORK_REV_B + SUBSCRIPTIONS_B + CLOUD_REV_B
print(f"  Google Services FY2026E Revenue:")
print(f"  {'Search & other (AI Overviews era)':<36}  ${SEARCH_REV_B:>5.1f}B  ({SEARCH_REV_B/total_rev_b*100:.0f}% of total; {SEARCH_OP_MARGIN*100:.0f}% op margin)")
print(f"  {'YouTube Ads':<36}  ${YOUTUBE_REV_B:>5.1f}B  ({YOUTUBE_REV_B/total_rev_b*100:.0f}%; Shorts monetisation ramping)")
print(f"  {'Google Network (AdSense/AdMob)':<36}  ${NETWORK_REV_B:>5.1f}B  ({NETWORK_REV_B/total_rev_b*100:.0f}%; structural TPP migration; declining)")
print(f"  {'Subscriptions + Devices':<36}  ${SUBSCRIPTIONS_B:>5.1f}B  ({SUBSCRIPTIONS_B/total_rev_b*100:.0f}%; Google One, Workspace, Pixel)")
print(f"  {'Google Cloud (GCP + Workspace Ent.)':<36}  ${CLOUD_REV_B:>5.1f}B  ({CLOUD_REV_B/total_rev_b*100:.0f}%; {CLOUD_GROWTH_RATE*100:.0f}% YoY; {CLOUD_OP_MARGIN*100:.0f}% margin)")
hr()
print(f"  Total FY2026E:                         ${total_rev_b:>5.1f}B")
print()

print(f"  SEARCH DISRUPTION SCENARIOS  (AI competitors capture X% of Google query volume):")
print(f"  {'AI query capture':<20}  {'Rev loss/yr':>12}  {'EPS drag/yr':>12}  {'2yr EPS drag':>13}")
hr()
shares_b = SHARES_OUT_M / 1000
for loss_pct in [0.05, 0.10, 0.15, 0.25]:
    rev_loss  = SEARCH_REV_B * loss_pct
    inc_loss  = rev_loss * SEARCH_OP_MARGIN * (1 - TAX_RATE)
    eps_yr    = inc_loss / shares_b
    eps_2yr   = eps_yr * 2
    print(f"  {loss_pct*100:.0f}% of queries        -${rev_loss:>5.1f}B/yr    -${eps_yr:.2f}/EPS/yr    -{eps_2yr:.2f}/EPS over 2yr")

print()
cloud_y1  = CLOUD_REV_B * CLOUD_GROWTH_RATE
cloud_y2  = CLOUD_REV_B * (1 + CLOUD_GROWTH_RATE) * CLOUD_GROWTH_RATE
cloud_eps1 = cloud_y1 * CLOUD_OP_MARGIN * (1 - TAX_RATE) / shares_b
cloud_eps2 = cloud_y2 * CLOUD_OP_MARGIN * (1 - TAX_RATE) / shares_b
cloud_2yr  = cloud_eps1 + cloud_eps2

print(f"  GOOGLE CLOUD GROWTH OFFSET  ({CLOUD_GROWTH_RATE*100:.0f}% CAGR; incremental EPS vs Cloud staying flat):")
print(f"  Year 1: ${CLOUD_REV_B:.0f}B × {CLOUD_GROWTH_RATE*100:.0f}% = +${cloud_y1:.1f}B rev  →  +${cloud_eps1:.2f}/EPS  (incremental income at {CLOUD_OP_MARGIN*100:.0f}% margin)")
print(f"  Year 2: ${CLOUD_REV_B*(1+CLOUD_GROWTH_RATE):.0f}B × {CLOUD_GROWTH_RATE*100:.0f}% = +${cloud_y2:.1f}B rev  →  +${cloud_eps2:.2f}/EPS  (compounding scale)")
print(f"  Total 2yr Cloud growth offset:  +${cloud_2yr:.2f}/EPS")
print()

# breakeven search loss that cloud offsets
break_pct = cloud_2yr / (SEARCH_REV_B * SEARCH_OP_MARGIN * (1-TAX_RATE) / shares_b * 2)
net_10pct = -(SEARCH_REV_B * 0.10 * SEARCH_OP_MARGIN * (1-TAX_RATE) / shares_b * 2) + cloud_2yr
print(f"  NET AT 10% SEARCH LOSS:  −${SEARCH_REV_B*0.10*SEARCH_OP_MARGIN*(1-TAX_RATE)/shares_b*2:.2f} drag  +  ${cloud_2yr:.2f} cloud offset  =  {net_10pct:+.2f}/EPS over 2yr")
print(f"  → Cloud growth at {CLOUD_GROWTH_RATE*100:.0f}% CAGR fully offsets ≤{break_pct*100:.0f}% search query loss; at 10% the net drag is only −${abs(net_10pct):.2f}/EPS.")
print(f"  BEAR ($80) requires: 25%+ search loss AND DOJ structural divestiture AND cloud slowdown — simultaneously.")

# ─── ② SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (search durability + cloud + AI monetisation + regulatory)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>6}  {'BASE':>5}  {'BULL':>6}  {'XBULL':>8}  {'NOW':>7}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>6}  {ths[1]:>5}  {ths[2]:>6}  {ths[3]:>8}  {s['now']:>7}  {lbl}  {b}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15% hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    c = score * weight
    print(f"    {sign}  {desc[:72]:<72}  ({score:+.1f} × {weight*100:.0f}%  =  {c:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>7}  Trigger")
hr()
bear_triggers = [
    ("Google Search revenue YoY",                        "+9%",    "<2%",    "−7pp",   "AI answer engines take 25% of queries; CPM col…"),
    ("Google Cloud growth YoY",                          "+29%",   "<10%",   "−19pp",  "Microsoft Azure AI wins enterprise replatforming…"),
    ("AI Overviews monetisation ratio",                  "~0.90×", "<0.6×",  "−0.3×",  "EU bans AI ads in search; click rates collapse…"),
    ("DOJ antitrust remedy",                             "behav.", "struct.","divestit","Judge orders Chrome + Android divestiture; app…"),
    ("YouTube + Shorts YoY growth",                      "+16%",   "<5%",    "−11pp",  "TikTok un-banned; Shorts demonetized by adverti…"),
    ("Gemini API revenue ($B/yr)",                       "~$5B",   "<$2B",   "−$3B",   "OpenAI GPT-5 dominates API market; Llama eats e…"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: DOJ Judge rules structural remedy — Google must divest Chrome and default")
print(f"  search agreements. Simultaneously AI answers (GPT-4o, Perplexity) capture 25%+ of queries.")
print(f"  Google loses advertiser CPM floor; EPS collapses to ~$6; at 13× distress P/E = ${bear_price}.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS × min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}  (consensus $10.20–$10.80)")
print(f"  Min viable P/E at trough:      {PE_TROUGH}×  (2022 trough was ~14–15×; search moat prevents <12×)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  +{epp_gap_pct:.0f}% premium to EPP is MODEST vs peers — reflects genuine AI disruption discount.")
print(f"  Bear ${bear_price} is BELOW EPP ${EPP:.0f} — requires BOTH EPS collapse AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+1.50:.2f} × {PE_TROUGH}× = ${(EPP_EPS+1.5)*PE_TROUGH:.0f} EPP — stock catches up quickly.")
print(f"  FCF-based EPP: $80B FCF ÷ 12.08B shares = $6.62 FCF/shr × 18× = ${6.62*18:.0f} (confirms trough floor)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: DOJ headwind + modest AI Overviews drag)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (modest growth; DOJ consent decree limits data use)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (below hist. avg of 20-22×; regulatory discount)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f} × 2; buyback also adds)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative 2yr is MARGINALLY POSITIVE — the stock is cheap on near-term earnings.")
print(f"  Even with DOJ consent decree and AI search headwinds, EPS growth continues (cloud + YouTube).")
print(f"  Buyback yield ~3.5%/yr ($6B+/qtr) provides additional return not captured above.")
print(f"  BUY threshold confirmed: even conservative case produces positive 2yr total return.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.30
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%  —  initiated 2024; buyback primary return)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (moderate; large-cap; regulatory binary + AI sentiment)")
print(f"  Beta vs S&P 500:      1.05  (near market; diversified revenue; less ad-cycle exposure than META)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (2022 GOOGL fell ~{(212.40-VOL_52W_LOW)/212.40*100:.0f}% from peak; achievable)")
print(f"  → DOJ ruling is the PRIMARY binary; favorable ruling = +15-20%; structural breakup = −30%+.")
print(f"  → At {vol_pct*100:.0f}th pct of 52W range — trading near the tariff trough; not priced for blue sky.")
print(f"  → BUY $148–$172  |  TRIM $260+  |  AVOID above ${VOL_52W_HIGH:.0f}")

# ─── ⑦ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print()
print("  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
hr()
probs_mkt = softmax_probs(MARKET_COMPOSITE)
print(f"  {'Scenario':<10}  {'Price':>6}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>7}  Description")
hr()
for s in ["BEAR","BASE","BULL","XBULL"]:
    pp   = probs_proxy[s] * 100
    pm   = probs_mkt[s]   * 100
    gap  = pp - pm
    pr   = SCENARIOS[s][2]
    desc = SCENARIOS[s][3][:45]
    print(f"  {s:<10}  ${pr:>5}  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

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
print(f"  Market composite {MARKET_COMPOSITE:.2f} = pricing between BEAR and BASE → AI disruption fear")
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees Cloud BULL + YouTube BULL partially offset by SCA")
print(f"  GAP +{ADJ_GAP:.2f}: model says market is under-pricing Cloud growth relative to search risk.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) DOJ remedy ruling — behavioral vs structural (binary; Q3 2026 timeline)")
print(f"  (2) AI Overviews monetisation ratio → ≥1.05× = BULL; confirms AI enhances, not disrupts, revenue")
print(f"  (3) Google Cloud exit rate: Q2 2026 annualised → ≥$58B = on track for $85B+ by 2027")
print(f"  (4) Gemini 2.5 enterprise adoption: Workspace AI Premium subs × $30/user/mo = inflection signal")
print(f"  BUY $148–{round(CURRENT_PRICE,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.12,0):.0f}  |  TRIM above $260  |  AVOID above $300")
print("═" * (W + 4))
print()

# ── EXPORT ────────────────────────────────────────────────────────────────────
RESULT = {
    "ticker":           TICKER,
    "signal":           signal_full,
    "signal_short":     signal_short,
    "price":            CURRENT_PRICE,
    "epp_gap_pct":      epp_gap_pct,
    "ratio_b":          ratio_b,
    "ratio_b_fmt":      f"{ratio_b:.2f}x",
    "adj_composite":    ADJ_COMPOSITE,
    "market_composite": MARKET_COMPOSITE,
    "adj_gap":          ADJ_GAP,
    "valuation":        valuation_label,
    "cons_return_2yr":  cons_return,
}

if __name__ == "__main__":
    pass
