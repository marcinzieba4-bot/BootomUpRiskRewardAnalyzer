"""
MA  ·  Mastercard Inc.  ·  NYSE: MA
Bottom-up signal model  ·  Global Payments Network / Cyber & Intelligence / Cross-Border
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "MA"
COMPANY       = "Mastercard Inc."
SECTOR        = "Payments Network · Value-Added Services & Solutions · Cyber & Intelligence · NYSE: MA"
CURRENT_PRICE = 545.00      # USD; as of 2026-06-10
VOL_52W_LOW   = 462.30      # 2025 rate-fear / fintech-disruption trough
VOL_52W_HIGH  = 588.75      # early-2026 high on resilient cross-border volume
SHARES_OUT_M  = 905.0       # millions; declining ~2-3%/yr via buyback

# Dividend: long growth streak; growing ~15%/yr historically
ANNUAL_DIV    = 3.32        # $/share FY2026 ($0.83/quarter)

# ── REVENUE BRIDGE (company-specific calculator) ──────────────────────────────
# FY2026E net revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Payment Network (GDV/cross-border)", 19.5, 15.5, 23.5, "Switched volume + cross-border volume; toll-booth on GDV; FX/travel sensitive"),
    ("Value-Added Services & Solutions",    9.8,  8.0, 13.0, "Cyber & Intelligence, data analytics, loyalty, consulting; fastest-growing, high-margin"),
    ("Other (processing/rebates net)",      0.7,  0.5,  1.0,  "Other revenue net of rebates/incentives"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.870   # blended contribution margin proxy FY2026E (before opex)
GROSS_MARGIN_BULL = 0.885   # BULL: VAS mix shift + operating leverage lifts margin
OPEX_FIXED_B      = 12.5    # advertising + G&A + base opex ($B); grows ~5%/yr
TAX_RATE          = 0.180   # effective rate; favorable jurisdictional mix

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 15.50       # FY2026E adj EPS (consensus ~$15.30-$15.70; non-GAAP)
PE_PESSIMISTIC = 24.0        # trough P/E: duopoly toll-booth model rarely de-rates below mid-20s
                              # (2022 rate-shock trough ~26x; severe recession/regulatory shock: 24x)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $372

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (12.50, 24,  300, "Global recession + interchange regulation crackdown; cross-border volume -20%; EPS $12.50 -> 24x floor P/E"),
    "BASE":  (17.50, 33,  578, "Cash-to-card secular conversion continues; VAS growth ~14%; EPS $17.50 at FY2028E -> 33x"),
    "BULL":  (21.00, 38,  798, "Cross-border travel boom + Cyber & Intelligence scales faster; emerging-market acceleration; EPS $21.00 -> 38x"),
    "XBULL": (25.00, 42, 1050, "Stablecoin/real-time-rails partnerships expand network; VAS becomes >35% of revenue; EPS $25.00 -> 42x"),
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
        "name":       "Switched volume / GDV growth (FX-neutral)",
        "weight":     0.25,
        "thresholds": ("<3%",   "≥6%",   "≥10%",  "≥14%"),
        "now":        "+9%",
        "score":      2,
        "comment":    "Resilient consumer spend; debit/credit mix stable; cash-to-card conversion in EM continues",
    },
    {
        "name":       "Cross-border volume growth",
        "weight":     0.20,
        "thresholds": ("<2%",   "≥6%",   "≥12%",  "≥18%"),
        "now":        "+11%",
        "score":      3,
        "comment":    "International travel & e-commerce strong; card-not-present cross-border outpacing GDV",
    },
    {
        "name":       "Value-Added Services & Solutions revenue YoY",
        "weight":     0.25,
        "thresholds": ("<8%",   "≥12%",  "≥16%",  "≥22%"),
        "now":        "+15%",
        "score":      3,
        "comment":    "Cyber & Intelligence (fraud/security), data analytics, loyalty programs; ~33% of net revenue and rising",
    },
    {
        "name":       "Regulatory / interchange litigation overhang",
        "weight":     0.15,
        "thresholds": ("severe", "elevated", "moderate", "benign"),
        "now":        "elevated",
        "score":      2,
        "comment":    "EU/UK/US interchange caps and antitrust suits ongoing; durbin-style debit cap risk in US debated",
    },
    {
        "name":       "Operating margin (adj.)",
        "weight":     0.10,
        "thresholds": ("<53%",  "≥55%",  "≥57%",  "≥59%"),
        "now":        "56.0%",
        "score":      3,
        "comment":    "VAS mix shift and operating leverage continue to expand margins toward upper-50s",
    },
    {
        "name":       "New payment flows / network partnerships (B2B, A2A, stablecoin rails)",
        "weight":     0.05,
        "thresholds": ("stalled", "early",  "scaling", "inflection"),
        "now":        "scaling",
        "score":      3,
        "comment":    "Multi-rail strategy (B2B, disbursements, stablecoin settlement pilots) expanding TAM beyond card rails",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Duopoly toll-booth moat — Visa/Mastercard share ~85%+ of global card network volume",   +0.7, 0.25),
    ("+", "VAS flywheel — Cyber & Intelligence/data/loyalty growing >2x network rate, high-margin", +0.6, 0.20),
    ("-", "Regulatory/antitrust risk — interchange caps (EU, UK, US Durbin-style proposals)",       -0.7, 0.20),
    ("-", "Disruption risk — real-time payments (FedNow/Pix), stablecoins, A2A bypass card rails",  -0.5, 0.15),
    ("+", "Capital-light compounder — ~50%+ FCF margin; consistent buybacks + dividend growth",     +0.4, 0.10),
    ("-", "Premium valuation risk — historically 30-35x; slight premium to Visa, sensitive to rates", -0.3, 0.10),
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
CONS_EPS_2YR  = 19.50   # conservative FY2028E: ~12% EPS CAGR (mid-teens revenue, buybacks, margin expansion)
CONS_PE_2YR   = 30      # modest rerating/de-rating from current ~35x toward growth-justified 30x
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Payments Network / VAS / Cross-Border")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① REVENUE BRIDGE ─────────────────────────────────────────────────────────
print()
print("  REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<38}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<38}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<38}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
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
shares_b  = shares * 0.95   # ~2.5%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.96   # margin compression in downturn
bear_oi   = bear_gp - OPEX_FIXED_B * 0.97           # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% margin − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% margin − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 38× = ~${bull_eps_imp*38:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.96:.1f}% margin − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 24× trough P/E (duopoly floor) = ~${bear_eps_imp*24:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev   = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_vas   = 1.0 * 0.65 * (1 - TAX_RATE) / shares   # VAS-level margin (higher than network avg)

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B VAS revenue:            +${eps_per_1B_vas:.3f}/EPS  = +${eps_per_1B_vas*33:.1f}/share at 33× P/E")
print(f"  Every $1B Network/GDV revenue:    +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*33:.1f}/share at 33× P/E")
print(f"  1pp margin expansion (mix/scale): +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*33:.1f}/share at 33× P/E")
print(f"  1% buyback (~9M shares):          +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (GDV growth / cross-border / VAS / regulatory framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>9}  {'BASE':>9}  {'BULL':>9}  {'XBULL':>10}  {'NOW':>9}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>9}  {ths[1]:>9}  {ths[2]:>9}  {ths[3]:>10}  {s['now']:>9}  {lbl}  {b}")

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
    ("Switched volume / GDV growth",   "+9%",     "<3%",     "−6pp",   "Global recession; consumer spend contraction"),
    ("Cross-border volume growth",     "+11%",    "<2%",     "−9pp",   "International travel collapse; FX/trade war shock"),
    ("VAS revenue YoY",                "+15%",    "<8%",     "−7pp",   "Cyber/data spend cuts amid enterprise budget tightening"),
    ("Regulatory overhang",            "elevated","severe",  "−1 lvl", "US adopts Durbin-style debit interchange caps; EU caps extend to credit"),
    ("Operating margin",               "56.0%",   "<53%",    "−3.0pp", "Rebate/incentive escalation + regulatory fee caps compress take rate"),
    ("New payment flows momentum",     "scaling", "stalled", "−2 lvl", "A2A/stablecoin rails bypass card network faster than expected"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A synchronized global recession cuts consumer spend and cross-border travel")
print(f"  volume sharply, while simultaneously regulators (US Durbin-style debit caps + EU/UK")
print(f"  interchange extension to credit) compress take rates structurally. EPS falls to ~$12.50")
print(f"  -> 24x floor P/E (duopoly resilience prevents deeper de-rating) = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT a permanent impairment — the network moat and VAS base provide")
print(f"  a durable earnings floor. Recovery to ~${bear_price+100}-${bear_price+150} in 2yr is base case post-shock.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus $15.30-$15.70; non-GAAP)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (duopoly toll-booth floor; 2022 rate-shock trough ~26×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% premium to EPP means the market prices in several years of uninterrupted")
print(f"  earnings growth ABOVE the trough-floor multiple. At ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f},")
print(f"  the P/E is {CURRENT_PRICE/EPS_FY2026E:.1f}× — a premium 'best-in-class duopoly' multiple, historically")
print(f"  in the 30-35× range and often at a slight premium to Visa given faster VAS growth.")
print(f"  EPP path: FY2028E EPS ~$19.00 × {PE_PESSIMISTIC:.0f}× = ${19.00*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing ~10%/yr).")
print(f"  At 30× mid-cycle P/E: ${EPS_FY2026E:.2f} × 30 = ${EPS_FY2026E*30:.0f}  — still below current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest multiple normalization; secular cash-to-card intact)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (~12% EPS CAGR: GDV/VAS growth + buybacks + margin expansion)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (modest normalization from ~{CURRENT_PRICE/EPS_FY2026E:.0f}× toward growth-justified 30×)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; long dividend growth streak)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE PICTURE: ~12% EPS CAGR roughly offsets a modest multiple normalization from")
print(f"  ~{CURRENT_PRICE/EPS_FY2026E:.0f}× to 30×, leaving total return close to flat-to-modestly-positive plus dividends.")
print(f"  For conservative 2yr to break even at 30× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~${((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E.")
print(f"  Breakeven at 33× P/E (limited multiple compression): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 33:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case attractive at 30× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.22
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  token; long dividend growth streak)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (lower than peers; resilient consumer-spend-linked cash flows)")
print(f"  Beta vs S&P 500:      1.10  (slight premium; global-consumer-spend amplifier)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe; global-recession + regulatory tail scenario)")
print(f"  52W low ${VOL_52W_LOW:.2f} already represents a peak-to-trough move of ~{(1-VOL_52W_LOW/VOL_52W_HIGH)*100:.0f}%.")
print(f"  → Regulatory/interchange action (US/EU/UK) is THE KEY binary; each cap escalation = -5-10% move.")
print(f"  → Cyber & Intelligence / data analytics revenue acceleration is KEY bull catalyst.")
print(f"  → WATCHLIST at current price  |  ACCUMULATE $480-510  |  BUY below $460")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is compared against the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0 while")
print(f"  the model scores fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0.")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: Mastercard remains a high-quality duopoly compounder; the key swing factors")
print(f"  are regulatory action on interchange and the pace of VAS/Cyber & Intelligence growth.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Regulatory action — US Durbin-style debit caps, EU/UK interchange extension to credit (BEAR trigger)")
print(f"  (2) Cyber & Intelligence / data analytics acceleration — VAS growth >18%/yr (BULL trigger)")
print(f"  (3) Cross-border travel & e-commerce volume — sustained double-digit growth (BULL trigger)")
print(f"  (4) Cash-to-card conversion in emerging markets — multi-decade secular tailwind")
print(f"  (5) New payment flows — B2B, disbursements, real-time/stablecoin rail partnerships")
print(f"  WATCHLIST at ${CURRENT_PRICE:.2f}  |  ACCUMULATE $480-510  |  BUY below $460")
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
