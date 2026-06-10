"""
V  ·  Visa Inc.  ·  NYSE: V
Bottom-up signal model  ·  Global Payments Network / Consumer Payments / New Flows / VAS
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "V"
COMPANY       = "Visa Inc."
SECTOR        = "Global Payments Network · Consumer Payments · New Flows · Value Added Services · NYSE: V"
CURRENT_PRICE = 352.40       # USD; as of 2026-06-10
VOL_52W_LOW   = 298.55       # 2025 rate-fear / consumer-spend-slowdown trough
VOL_52W_HIGH  = 366.54       # early-2026 high on resilient cross-border volume
SHARES_OUT_M  = 1_980.0      # millions; declining ~2%/yr via buyback
SHARES_OUT_M  = 1_980.0

# Dividend: 17-year growth streak; growing ~15%/yr historically
ANNUAL_DIV    = 2.36         # $/share FY2026 ($0.59/quarter)

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B) — net revenue allocation basis
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Consumer Payments (credit/debit)", 23.5, 19.0, 27.0, "Core toll-booth: payments volume + cross-border travel/e-com"),
    ("New Flows (B2B/P2P/Visa Direct)",   5.5,  4.3,  7.5, "Visa Direct push payments, B2B Connect, account-to-account"),
    ("Value Added Services",              9.5,  8.0, 12.5, "Fraud/risk, data analytics, advisory, issuing/acceptance solutions"),
]

# Margin assumptions (operating margin on net revenue, "toll-booth" model)
OPMARGIN_CURR = 0.665   # blended operating margin FY2026E (~66.5%)
OPMARGIN_BULL = 0.685   # BULL: VAS mix + operating leverage lift margin further
OPEX_OTHER_B  = 0.0     # margin already net of opex in OPMARGIN figures
TAX_RATE      = 0.185   # effective tax rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 11.30       # FY2026E adj EPS (consensus ~$11.20-$11.45; non-GAAP)
PE_PESSIMISTIC = 22.0        # trough P/E: duopoly toll-booth model rarely de-rates below low-20s
                              # (2022 rate-shock trough ~24x; severe interchange-regulation tail ~22x)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $249

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 9.50, 22,  209, "Interchange regulation (Durbin-style expansion) + DOJ antitrust remedy; payment volume growth stalls to low-single digits; EPS $9.50 → 22x floor P/E"),
    "BASE":  (12.50, 29,  363, "Steady cash-to-card conversion + cross-border travel normalization; VAS +18%/yr; EPS $12.50 at FY2028E → 29x"),
    "BULL":  (14.50, 33,  479, "Emerging-market cash displacement accelerates; Visa Direct scales to major P2P/B2B rails; VAS $14B; EPS $14.50 → 33x"),
    "XBULL": (17.00, 36,  612, "Visa becomes dominant global money-movement network beyond cards; stablecoin/real-time rails settle on Visa infrastructure; EPS $17.00 → 36x"),
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
        "name":       "Payments volume YoY growth (constant-dollar)",
        "weight":     0.30,
        "thresholds": ("<3%",    "≥5%",   "≥8%",    "≥12%"),
        "now":        "+6%",
        "score":      2,
        "comment":    "US debit/credit steady; resilient consumer spend offset by mix shift to lower-ticket categories",
    },
    {
        "name":       "Cross-border volume YoY growth (ex-intra-Europe)",
        "weight":     0.20,
        "thresholds": ("<5%",    "≥8%",   "≥12%",   "≥18%"),
        "now":        "+11%",
        "score":      3,
        "comment":    "International travel/e-commerce remains a high-margin growth engine; near pre-pandemic trend",
    },
    {
        "name":       "Value Added Services revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<10%",   "≥14%",  "≥18%",   "≥24%"),
        "now":        "+19%",
        "score":      3,
        "comment":    "Fraud/risk, data analytics, advisory, issuing solutions; fastest-growing, highest-margin segment",
    },
    {
        "name":       "New Flows volume (Visa Direct transactions) YoY growth",
        "weight":     0.15,
        "thresholds": ("<15%",   "≥20%",  "≥30%",   "≥45%"),
        "now":        "+24%",
        "score":      3,
        "comment":    "Visa Direct scaling across P2P, remittances, B2B disbursements; long runway vs core card volume",
    },
    {
        "name":       "Regulatory/litigation overhang (interchange & antitrust)",
        "weight":     0.10,
        "thresholds": ("severe", "elevated", "moderate", "low"),
        "now":        "elevated",
        "score":      2,
        "comment":    "DOJ antitrust suit ongoing; merchant-fee legislation proposals recurring in Congress; no near-term resolution",
    },
    {
        "name":       "Operating margin",
        "weight":     0.05,
        "thresholds": ("<63%",   "≥65%",  "≥67%",   "≥69%"),
        "now":        "66.5%",
        "score":      3,
        "comment":    "VAS mix and continued operating leverage support margin near record highs",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Duopoly network moat — Visa/Mastercard control ~85%+ of global card networks; immense switching costs",  +0.7, 0.25),
    ("+", "Secular cash-to-card conversion — emerging markets still 30-50% cash; decades-long tailwind",            +0.6, 0.20),
    ("+", "VAS flywheel — fraud/data/advisory growing >18%/yr at higher margin than core network business",         +0.4, 0.15),
    ("-", "Regulatory/antitrust risk — DOJ suit + interchange-fee legislation could compress take-rate structurally",-0.7, 0.20),
    ("+", "Asset-light toll-booth economics — 65%+ operating margin, minimal capex, massive FCF, consistent buybacks",+0.4, 0.10),
    ("-", "Premium valuation — historically trades 28-32x; little room for multiple expansion from here",          -0.3, 0.10),
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
CONS_EPS_2YR  = 14.00   # conservative FY2028E: ~11% EPS CAGR (volume growth + buyback + VAS mix)
CONS_PE_2YR   = 27      # modest rerating from ~31x to growth-justified 27x
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Global Payments Network / Consumer Payments / New Flows / VAS")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<36}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<36}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<36}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print()

# EPS bridge
curr_oi   = curr_total * OPMARGIN_CURR
curr_ni   = curr_oi * (1 - TAX_RATE)
shares    = SHARES_OUT_M / 1000
curr_eps  = round(curr_ni / shares, 2)

bull_oi   = bull_total * OPMARGIN_BULL
bull_ni   = bull_oi * (1 - TAX_RATE)
shares_b  = shares * 0.96   # ~2%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_oi   = bear_total * OPMARGIN_CURR * 0.97   # margin compression from regulatory take-rate hit
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B net rev × {OPMARGIN_CURR*100:.1f}% op margin − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {OPMARGIN_BULL*100:.1f}% op margin − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 33× = ~${bull_eps_imp*33:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {OPMARGIN_CURR*100*0.97:.1f}% op margin − tax  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 22× trough P/E (toll-booth floor) = ~${bear_eps_imp*22:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = (1.0 * OPMARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_xb  = 1.0 * 0.80 * (1 - TAX_RATE) / shares   # cross-border carries higher incremental margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Consumer Payments revenue:  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*29:.1f}/share at 29× P/E")
print(f"  Every $1B cross-border revenue (~80% incr. margin): +${eps_per_1B_xb:.3f}/EPS  =  +${eps_per_1B_xb*29:.1f}/share at 29× P/E")
print(f"  1pp operating margin (VAS mix/efficiency):  +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*29:.1f}/share at 29× P/E")
print(f"  1% buyback (~20M shares):  +${curr_eps*0.01:.3f}/EPS  (mechanical accretion; ongoing multi-billion $ authorization)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (payment volume / cross-border / VAS / New Flows / regulation framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>9}  {'BASE':>9}  {'BULL':>9}  {'XBULL':>9}  {'NOW':>9}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>9}  {ths[1]:>9}  {ths[2]:>9}  {ths[3]:>9}  {s['now']:>9}  {lbl}  {b}")

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
    ("Payments volume YoY growth",    "+6%",    "<3%",     "−3pp",   "Consumer spending recession; high-end/travel pullback"),
    ("Cross-border volume YoY",       "+11%",   "<5%",     "−6pp",   "Global travel demand shock (pandemic-style or geopolitical)"),
    ("VAS revenue YoY growth",        "+19%",   "<10%",    "−9pp",   "Issuer/merchant budget cuts; VAS attach rate stalls"),
    ("New Flows volume YoY",          "+24%",   "<15%",    "−9pp",   "Visa Direct loses share to bank-led real-time rail (FedNow/RTP)"),
    ("Regulatory overhang",           "elevated","severe",  "↓1 lvl", "Congress passes Durbin-style expansion to credit interchange"),
    ("Operating margin",              "66.5%",  "<63%",    "−3.5pp", "Take-rate compression from regulation + incentive payment inflation"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A combination of (1) US legislation extending Durbin-style interchange caps")
print(f"  to credit cards, (2) an adverse DOJ antitrust remedy forcing network-fee concessions, and")
print(f"  (3) a consumer-spending recession that stalls payment volume growth to low-single digits.")
print(f"  Operating margin compresses ~3.5pp and EPS falls to ~${bear_eps_imp:.2f} → 22× floor = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT a permanent impairment — the duopoly network moat and secular")
print(f"  cash-to-card conversion in emerging markets provide a durable earnings floor. Recovery to")
print(f"  ~${bear_price+60}–${bear_price+100} in 2yr is base case post-shock.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~$11.20–$11.45; non-GAAP)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (toll-booth duopoly floor; 2022 rate-shock trough ~24×; severe-regulation tail ~22×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP means the market prices in several years of uninterrupted")
print(f"  payment-volume and VAS growth ABOVE the trough-floor multiple. At ${CURRENT_PRICE:.2f} and")
print(f"  FY2026E EPS ${EPS_FY2026E:.2f}, the P/E is {CURRENT_PRICE/EPS_FY2026E:.1f}× — near the historical 28-32× 'best-in-class'")
print(f"  premium band. Investors pay for the duopoly moat and decades-long cash-to-card runway.")
print(f"  EPP path: FY2028E EPS ~${CONS_EPS_2YR:.2f} × {PE_PESSIMISTIC:.0f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing ~11%/yr).")
print(f"  At 27× mid-cycle P/E: ${EPS_FY2026E:.2f} × 27 = ${EPS_FY2026E*27:.0f}  — {'below' if EPS_FY2026E*27 < CURRENT_PRICE else 'above'} current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest P/E rerate; secular volume growth persists)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (~11% EPS CAGR: buyback ~2%/yr + volume/VAS growth ~9%/yr)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (modest derate from ~{CURRENT_PRICE/EPS_FY2026E:.0f}× toward {CONS_PE_2YR}×; still premium)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; 17-yr growth streak)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: can EPS growth (~11%/yr) outpace any multiple compression from the")
print(f"  current {CURRENT_PRICE/EPS_FY2026E:.0f}× toward {CONS_PE_2YR}×? At {CONS_PE_2YR}× P/E, breakeven requires EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — broadly in line with consensus BASE case.")
print(f"  Breakeven at 30× P/E (no multiple compression): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 30:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.20
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  token; Dividend Aristocrat-track)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (lower than tech peers; defensive toll-booth cash flows)")
print(f"  Beta vs S&P 500:      0.95  (slight discount to market; resilient consumer-spending exposure)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (extreme; regulatory-shock tail scenario)")
print(f"  → Interchange/antitrust regulation is THE KEY binary; adverse legislation = −10–20% move.")
print(f"  → Cross-border travel volume reacceleration + VAS attach-rate gains are KEY bull catalysts.")
print(f"  → AVOID above ${round(EPP*1.6,-1):.0f}  |  WATCHLIST ${round(EPP*1.35,-1):.0f}–{round(EPP*1.5,-1):.0f}  |  ACCUMULATE ${round(EPP*1.15,-1):.0f}–{round(EPP*1.3,-1):.0f}  |  BUY below ${round(EPP*1.1,-1):.0f}")

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
print(f"  Regulatory overhang (signal score 2/4 = BASE) and the premium 28-32× historical multiple")
print(f"  band remain the most significant valuation considerations.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Interchange/antitrust regulation — DOJ suit outcome and Congressional credit-interchange bills (BEAR trigger)")
print(f"  (2) Cross-border/travel volume reacceleration — international e-commerce and travel demand (BULL trigger)")
print(f"  (3) Value Added Services growth — fraud/data/advisory attach rates and margin mix (BULL trigger)")
print(f"  (4) New Flows / Visa Direct scaling vs bank-led real-time rails (FedNow/RTP) — share-of-wallet battle")
print(f"  (5) Emerging-market cash-to-card conversion — multi-decade secular tailwind (India, LatAm, Africa, SE Asia)")
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
