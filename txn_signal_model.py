"""
TXN  ·  Texas Instruments Incorporated  ·  NASDAQ: TXN
Bottom-up signal model  ·  Analog & Embedded Semiconductors / Industrial / Auto / AI Data Center
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "TXN"
COMPANY       = "Texas Instruments Incorporated"
SECTOR        = "Analog & Embedded Semiconductors · Industrial · Automotive · AI Data Center · NASDAQ: TXN"
CURRENT_PRICE = 308.65      # USD; as of 2026-06-10; +58% YTD on AI/data-center re-rating
VOL_52W_LOW   = 165.00
VOL_52W_HIGH  = 320.00
SHARES_OUT_M  = 905.0       # millions

# Dividend: long-running growth streak
ANNUAL_DIV    = 5.68        # $/share annualized

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Analog — Power Management",   8.20, 6.50, 10.50, "Industrial/auto recovery + data center power; largest segment"),
    ("Analog — Signal Chain",       6.40, 5.00,  8.20, "Industrial sensing/connectivity; data center AI signal chain growth"),
    ("Embedded Processing",         2.80, 2.20,  3.60, "MCUs/processors; auto + industrial cycle; share-loss risk vs ARM"),
    ("Other (DLP, calculators)",    0.85, 0.70,  1.00, "Legacy DLP/education products; stable, low-growth cash generator"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.585   # blended gross margin FY2026E (~58.5%; depressed vs historical 65%+ on capex depreciation)
GROSS_MARGIN_BULL = 0.640   # BULL: 300mm Sherman ramp drives utilization-led margin expansion
OPEX_FIXED_B      = 4.10    # R&D + SG&A ($B); roughly fixed cost base
TAX_RATE          = 0.135   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 7.70        # FY2026E adj EPS (BASE case estimate)
PE_PESSIMISTIC = 22.0        # trough P/E: cyclical analog floor multiple at depressed-trough EPS
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $169

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 5.50, 22,  121, "Analog cycle double-dips; China competition erodes pricing; EPS $5.50 → 22× floor P/E"),
    "BASE":  ( 7.70, 28,  216, "Industrial/auto recovery continues at moderate pace; EPS $7.70 → 28×"),
    "BULL":  ( 9.50, 33,  314, "Data center AI revenue scales further; 300mm utilization lifts margins; EPS $9.50 → 33×"),
    "XBULL": (12.00, 38,  456, "Full capex-cycle payoff; analog supercycle + AI data center dominance; EPS $12.00 → 38×"),
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
        "name":       "Analog/Embedded revenue cycle recovery (industrial + auto)",
        "weight":     0.25,
        "thresholds": ("<0%",    "≥5%",   "≥12%",   "≥20%"),
        "now":        "+8%",
        "score":      2,
        "comment":    "Industrial and automotive revenue growing off the cycle trough; not yet at full BULL recovery pace",
    },
    {
        "name":       "Data center / AI revenue growth YoY",
        "weight":     0.25,
        "thresholds": ("<20%",   "≥40%",  "≥70%",   "≥100%"),
        "now":        "+90%",
        "score":      3,
        "comment":    "Q1 2026 data center/AI revenue +90% YoY; strong but off a small base; key driver of re-rating",
    },
    {
        "name":       "Gross margin recovery (300mm Sherman SM1 utilization)",
        "weight":     0.20,
        "thresholds": ("<55%",   "≥58%",  "≥61%",   "≥64%"),
        "now":        "58.5%",
        "score":      2,
        "comment":    "Margins still depressed by depreciation from 300mm capacity build; utilization ramp gradual",
    },
    {
        "name":       "Free cash flow inflection (capex decline)",
        "weight":     0.15,
        "thresholds": ("<5%",    "≥8%",   "≥14%",   "≥20%"),
        "now":        "~10%",
        "score":      2,
        "comment":    "Capex cycle ~83% complete; FCF margin improving but not yet at full inflection",
    },
    {
        "name":       "Industrial end-market inventory destocking completion",
        "weight":     0.10,
        "thresholds": ("Ongoing","Mostly done","Complete","Restocking"),
        "now":        "Mostly done",
        "score":      2,
        "comment":    "Channel inventory normalized in most industrial sub-segments; some pockets remain elevated",
    },
    {
        "name":       "China/auto competitive pricing pressure (domestic suppliers)",
        "weight":     0.05,
        "thresholds": (">-10%",  "≥-5%",  "≥0%",    "≥+3%"),
        "now":        "-6%",
        "score":      1,
        "comment":    "Domestic Chinese analog suppliers (e.g. SG Micro, Will Semi) gaining share with aggressive pricing",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Highest-quality analog franchise — scale, 300mm cost advantage, broadest catalog",     +0.7, 0.25),
    ("+", "Data center/AI halo — +90% YoY growth provides genuine new growth vector",              +0.5, 0.15),
    ("-", "Valuation already at ~40x FY2026E trough EPS — prices in 2028-2030 capex payoff",       -0.8, 0.25),
    ("-", "Avg analyst target ~$284 sits BELOW current price $308.65 — re-rating ahead of fundamentals", -0.7, 0.20),
    ("-", "China domestic analog competition — structural share/pricing erosion in industrial/auto", -0.4, 0.10),
    ("+", "Capital return — high dividend, long growth streak, capex cycle 83% done supports FCF", +0.3, 0.05),
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
CONS_EPS_2YR  = 8.60    # conservative FY2028E EPS: gradual cycle recovery + margin improvement
CONS_PE_2YR   = 24      # rerating from ~40x toward growth-justified 24x as cycle normalizes
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Analog/Embedded Semis / Industrial / Auto / AI Data Center")
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
shares_b  = shares * 0.97   # modest buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.95   # margin compression in downturn
bear_oi   = bear_gp - OPEX_FIXED_B * 0.97           # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (BASE estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 33× = ~${bull_eps_imp*33:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.95:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 22× trough P/E (cyclical analog floor) = ~${bear_eps_imp*22:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev   = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_dc    = 1.0 * 0.55 * (1 - TAX_RATE) / shares   # data center segment-level incremental margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Data Center/AI revenue:  +${eps_per_1B_dc:.3f}/EPS  = +${eps_per_1B_dc*28:.1f}/share at 28× P/E")
print(f"  Every $1B Analog/Embedded revenue:  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*28:.1f}/share at 28× P/E")
print(f"  1pp GM expansion (300mm utilization): +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*28:.1f}/share at 28× P/E")
print(f"  1% buyback (~9M shares):              +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Analog cycle / Data center AI / Margin recovery / FCF framework)")
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
    ("Analog/Embedded cycle recovery YoY",  "+8%",   "<0%",   "−8pp",   "Industrial + auto orders roll over; recovery stalls/double-dips"),
    ("Data center/AI revenue growth YoY",   "+90%",  "<20%",  "−70pp",  "Hyperscaler capex pause; AI data center revenue growth decelerates sharply"),
    ("Gross margin",                        "58.5%", "<55%",  "−3.5pp", "300mm Sherman SM1 ramp lags guidance; utilization stays depressed"),
    ("FCF margin / capex decline",          "~10%",  "<5%",   "−5pp",   "Capex cycle extends beyond 83% complete; FCF inflection delayed"),
    ("China/auto competitive pricing",      "-6%",   "<-10%", "−4pp",   "Chinese domestic analog suppliers erode industrial/auto pricing further"),
    ("Inventory destocking",                "Mostly done", "Ongoing", "reversal", "New channel inventory build-up reignites destocking cycle"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the analog/embedded cycle recovery (industrial + auto) stalls or double-dips")
print(f"  just as Sherman SM1 300mm capacity continues ramping, leaving margins depressed under")
print(f"  higher fixed depreciation. Simultaneously, data center/AI revenue growth decelerates")
print(f"  sharply from +90% YoY toward the 20% range, removing the primary re-rating narrative.")
print(f"  Chinese domestic analog suppliers (SG Micro, Will Semi, etc.) continue taking share in")
print(f"  industrial and automotive, pressuring pricing. EPS falls to ~$5.50 → 22× floor = ${bear_price}.")
print(f"  Note: ${bear_price} is not a permanent impairment — TXN's scale, 300mm cost advantage,")
print(f"  and broad catalog provide a durable earnings floor through any one cyclical downturn.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (BASE case; depressed-trough EPS)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (cyclical analog floor multiple)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP means the market is pricing a multi-year recovery story")
print(f"  ABOVE the trough-floor multiple. At ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f}, the")
print(f"  P/E is ~40× on a depressed-trough EPS base. The bull case is that the 2028-2030 capex")
print(f"  payoff (300mm cost advantage, AI data center scale) justifies this multiple TODAY.")
print(f"  The bear case is that the AI/data-center halo has pulled forward years of re-rating")
print(f"  before the fundamental recovery (margin expansion, FCF inflection) has materialized.")
print(f"  Avg analyst target ~$284 sits BELOW the current price ${CURRENT_PRICE:.2f} — a notable signal")
print(f"  that sell-side fundamentals have not caught up to the recent +58% YTD re-rating.")
print(f"  At 28× mid-cycle P/E: ${EPS_FY2026E:.2f} × 28 = ${EPS_FY2026E*28:.0f}  — below current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: gradual cycle recovery + partial multiple normalization)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (gradual industrial/auto recovery + margin gains from 300mm ramp)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (rerates from ~40× toward growth-justified 24×; still above historical norm)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE PROBLEM: even the conservative case requires P/E compression from ~40× toward {CONS_PE_2YR}×.")
print(f"  That multiple contraction offsets EPS growth from the cycle recovery — a negative total return")
print(f"  unless the recovery + AI data center growth substantially exceeds the conservative path.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~${((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — possible at BULL, not BASE.")
print(f"  Breakeven at 30× P/E (no multiple compression): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 30:.2f}")
print(f"  ADD trigger: $200–220 pullback (cycle recovery intact, multiple resets toward 28×)")
print(f"  BUY below: $155 (back near EPP floor; ratio_b <0.75×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.30
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock up 58% YTD on AI/data-center re-rating; 52W high near current price")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (cyclical semis; analog historically lower-beta but capex cycle elevates risk)")
print(f"  Beta vs S&P 500:      1.10  (cyclical semiconductor exposure)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown")
print(f"  52W low ${VOL_52W_LOW:.2f} reflects pre-AI-re-rating valuation; current price near 52W high.")
print(f"  → AI/data-center revenue trajectory is THE KEY swing factor for sustaining the multiple.")
print(f"  → 300mm Sherman SM1 utilization ramp and resulting gross margin trajectory is KEY bull catalyst.")
print(f"  → AVOID at current price  |  WATCHLIST $260–290  |  ACCUMULATE $200–220  |  BUY below $155")

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
print(f"  In plain terms: TXN is up 58% YTD on the AI/data-center halo, trading at ~40× FY2026E")
print(f"  trough EPS — a multiple that already prices in the 2028-2030 capex-payoff recovery.")
print(f"  Avg analyst target (~$284) sits BELOW current price, suggesting the re-rating narrative")
print(f"  may be running ahead of the fundamental cycle recovery.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Quarterly data center/AI revenue updates — sustaining +90% YoY growth is the re-rating linchpin")
print(f"  (2) Analog/embedded cycle recovery — industrial order trends, book-to-bill ratio")
print(f"  (3) Gross margin trajectory as Sherman SM1 (300mm) ramps utilization toward target")
print(f"  (4) FCF inflection as capex declines (cycle ~83% done) — confirms capital return acceleration")
print(f"  (5) China auto/industrial competitive dynamics — domestic analog suppliers' share/pricing impact")
print(f"  AVOID at ${CURRENT_PRICE:.2f}  |  WATCHLIST $260–290  |  ACCUMULATE $200–220  |  BUY below $155")
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
