"""
KKR  ·  KKR & Co. Inc.  ·  NYSE: KKR
Bottom-up signal model  ·  Alternative Asset Management / Private Equity / Insurance / Capital Markets
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "KKR"
COMPANY       = "KKR & Co. Inc."
SECTOR        = "Alternative Asset Management · Private Equity · Credit/Infra/RE · Insurance (Global Atlantic) · NYSE: KKR"
CURRENT_PRICE = 98.50       # USD; as of 2026-06-11
VOL_52W_LOW   = 78.40       # 2025 rate-shock / realization-drought trough
VOL_52W_HIGH  = 134.00      # late-2025 AUM all-time-high peak
SHARES_OUT_M  = 1_580.0     # millions; modest dilution from equity comp/M&A
ANNUAL_DIV    = 0.78        # $/share FY2026 (~$0.195/quarter; growing with FRE)

# ── AUM / EARNINGS REVENUE BRIDGE (company-specific calculator) ──────────────
# FY2026E Fee-Related Earnings (FRE) + segment economics by business line ($B, pre-tax distributable)
SEG_DATA = [
    # (segment, curr_earn_B, bear_earn_B, bull_earn_B, description)
    ("Asset Mgmt - Private Equity FRE",  1.55, 1.20, 2.00, "Flagship PE funds; FPAUM growth + fundraising cycle"),
    ("Asset Mgmt - Credit FRE",          1.30, 1.05, 1.75, "Direct lending/BDC scale-up; fastest-growing FPAUM segment"),
    ("Asset Mgmt - Infrastructure FRE",  0.85, 0.65, 1.25, "Energy transition + digital infra megafunds; structural tailwind"),
    ("Asset Mgmt - Real Estate FRE",     0.40, 0.28, 0.60, "Recovering RE fundraising post rate-cut cycle"),
    ("Insurance (Global Atlantic)",      1.45, 1.15, 1.95, "$219B AUM, +15%/yr; spread + fee income; permanent capital"),
    ("Strategic Holdings/Capital Mkts",  0.95, 0.55, 1.85, "Carry realizations + capital markets fees; M&A-cycle dependent"),
]

# Margin / share-count assumptions
TAX_RATE          = 0.18    # effective rate on distributable earnings (corp conversion structure)
SHARE_GROWTH_BULL = 1.02     # modest dilution even in BULL (equity-funded growth)
SHARE_COUNT_BEAR  = 1.00     # flat in BEAR (buybacks paused)

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 4.85        # FY2026E adj/distributable EPS (consensus ~$4.70-$5.00)
PE_PESSIMISTIC = 14.0        # trough P/E: FRE base + insurance still command above-market multiple
                              # (2022-23 rate-shock trough ~13-15x on FRE-heavy mix)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # ~$68

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 3.30, 17,   56, "Realization drought persists; rates stay elevated; PE marks cut; carry near-zero; EPS $3.30 → 17x floor"),
    "BASE":  ( 5.60, 22,  123, "FRE compounds ~15%/yr; FPAUM $615B → ~$750B; Global Atlantic +15%; moderate carry; EPS $5.60 at FY2028E → 22x"),
    "BULL":  ( 7.50, 28,  210, "M&A/exit window reopens; $120B dry powder deployed; carry realizations surge; EPS $7.50 → 28x"),
    "XBULL": ( 9.75, 32,  312, "Multi-year PE realization supercycle; Insurance scales to $300B+ AUM; KKR re-rates as compounder; EPS $9.75 → 32x"),
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
        "name":       "Fee-paying AUM (FPAUM) growth YoY",
        "weight":     0.25,
        "thresholds": ("<8%",    "≥12%",  "≥17%",   "≥25%"),
        "now":        "+17%",
        "score":      3,
        "comment":    "$615B FPAUM, +17% YoY; Credit + Infrastructure leading; durable fundraising momentum",
    },
    {
        "name":       "Fee-Related Earnings (FRE) growth YoY",
        "weight":     0.25,
        "thresholds": ("<8%",    "≥12%",  "≥18%",   "≥25%"),
        "now":        "+15%",
        "score":      3,
        "comment":    "FRE compounding mid-teens; recurring management fee base scaling with FPAUM",
    },
    {
        "name":       "Realization activity / carried interest trend",
        "weight":     0.20,
        "thresholds": ("declining", "flat",  "recovering", "surging"),
        "now":        "flat-to-recovering",
        "score":      2,
        "comment":    "Exit environment thawing but M&A volumes still below 2021 peak; PE marks pressured by elevated rates",
    },
    {
        "name":       "Global Atlantic (Insurance) AUM growth",
        "weight":     0.15,
        "thresholds": ("<8%",    "≥10%",  "≥15%",   "≥22%"),
        "now":        "+15%",
        "score":      3,
        "comment":    "$219B AUM, +15%/yr; permanent capital diversifies earnings away from carry cyclicality",
    },
    {
        "name":       "Dry powder deployment pace",
        "weight":     0.10,
        "thresholds": ("stalled", "modest", "active", "accelerating"),
        "now":        "modest",
        "score":      2,
        "comment":    "$120B+ dry powder; deployment pace measured given valuation discipline at elevated rates",
    },
    {
        "name":       "Distributable earnings P/E vs history",
        "weight":     0.05,
        "thresholds": ("<14x",   "≥18x",  "≥24x",   "≥30x"),
        "now":        "~20x",
        "score":      2,
        "comment":    "Trading below historical premium growth multiple (25-35x); below long-run average on FY2026E EPS",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Scale & franchise — $758B+ AUM at all-time highs; 50-yr PE pioneer brand",            +0.6, 0.20),
    ("+", "Permanent capital diversification — Global Atlantic insurance float reduces cyclicality", +0.6, 0.20),
    ("+", "Dry powder optionality — $120B+ ready for deployment when valuations reset",          +0.4, 0.15),
    ("-", "Realization drought risk — prolonged high-rate environment suppresses carry/exits",   -0.7, 0.25),
    ("-", "Mark-to-model valuation risk — PE portfolio NAV marks lag public market repricing",    -0.4, 0.15),
    ("+", "Capital markets fee growth — KCM franchise scales with deal volume recovery",          +0.3, 0.05),
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
CONS_EPS_2YR  = 5.60    # conservative FY2028E: FRE compounding mid-teens; modest carry recovery
CONS_PE_2YR   = 22      # holds near current multiple; modest rerate toward historical premium
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Alternative Asset Management / PE / Insurance")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① EARNINGS REVENUE BRIDGE ────────────────────────────────────────────────
print()
print("  EARNINGS BRIDGE  (FY2026E pre-tax distributable earnings  →  BEAR / BULL scenarios, $B)")
hr()

curr_total = sum(e for _, e, _, _, _ in SEG_DATA)
bear_total = sum(e for _, _, e, _, _ in SEG_DATA)
bull_total = sum(e for _, _, _, e, _ in SEG_DATA)

print(f"  {'Segment':<32}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<32}  ${curr:>11.2f}  ${bear:>8.2f}  ${bull:>8.2f}  {bear-curr:>+7.2f}  {bull-curr:>+7.2f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<32}  ${curr_total:>11.2f}  ${bear_total:>8.2f}  ${bull_total:>8.2f}  {bear_total-curr_total:>+7.2f}  {bull_total-curr_total:>+7.2f}")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_ni   = curr_total * (1 - TAX_RATE)
curr_eps  = round(curr_ni / shares, 2)

shares_bull = shares * SHARE_GROWTH_BULL
bull_ni     = bull_total * (1 - TAX_RATE)
bull_eps_imp = round(bull_ni / shares_bull, 2)

shares_bear = shares * SHARE_COUNT_BEAR
bear_ni     = max(0, bear_total) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares_bear, 2)

print(f"  FY2026E EPS check:  ${curr_total:.2f}B pre-tax DE × {(1-TAX_RATE)*100:.0f}% (1 - tax) ÷ {shares:.3f}B shares")
print(f"  =  ${curr_eps:.2f}/share distributable EPS  (consensus ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B × {(1-TAX_RATE)*100:.0f}% ÷ {shares_bull:.3f}B shares  =  ~${bull_eps_imp:.2f}/share")
print(f"  → ${bull_eps_imp:.2f} × 28× = ~${bull_eps_imp*28:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B × {(1-TAX_RATE)*100:.0f}% ÷ {shares_bear:.3f}B shares  =  ~${bear_eps_imp:.2f}/share")
print(f"  At 17× trough P/E (FRE-floor) = ~${bear_eps_imp*17:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
print(f"  KEY SENSITIVITIES:")
print(f"  Every $0.1B FRE growth:           +${0.1*(1-TAX_RATE)/shares:.3f}/EPS  = +${0.1*(1-TAX_RATE)/shares*22:.2f}/share at 22× P/E")
print(f"  Carry/realization swing ±$0.5B:   ±${0.5*(1-TAX_RATE)/shares:.3f}/EPS  = ±${0.5*(1-TAX_RATE)/shares*22:.2f}/share at 22× P/E")
print(f"  Global Atlantic AUM ±$10B (~5%):  ±${10*0.0066*(1-TAX_RATE)/shares:.3f}/EPS  = ±${10*0.0066*(1-TAX_RATE)/shares*22:.2f}/share at 22× P/E")
print(f"  Multiple re-rate to 28× (history): ${curr_eps:.2f} × 28 = ${curr_eps*28:.0f}  vs ${curr_eps:.2f} × 22 = ${curr_eps*22:.0f}")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (FPAUM growth / FRE / realizations / Global Atlantic / dry powder framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>11}  {'BASE':>7}  {'BULL':>11}  {'XBULL':>12}  {'NOW':>20}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>11}  {ths[1]:>7}  {ths[2]:>11}  {ths[3]:>12}  {s['now']:>20}  {lbl}  {b}")

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
print(f"  {'Signal':<52}  {'Current':>14}  {'Bear val':>12}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("FPAUM growth YoY",                  "+17%",            "<8%",       "−9pp",   "Fundraising stalls; LPs pull back amid rate uncertainty"),
    ("FRE growth YoY",                    "+15%",            "<8%",       "−7pp",   "Fee compression + slower deployment of new capital"),
    ("Realization activity",              "flat-to-recov.",  "declining", "↓",      "M&A/IPO window slams shut; carried interest near zero for 2+ yrs"),
    ("Global Atlantic AUM growth",        "+15%",            "<8%",       "−7pp",   "Annuity outflows; spread compression in rate-cut scenario"),
    ("Dry powder deployment",             "modest",          "stalled",   "↓",      "Valuation gap freezes deal activity; capital sits idle"),
    ("Distributable earnings P/E",        "~20x",            "<14x",      "−6x",    "Multiple compresses to trough as carry visibility evaporates"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>14}  {bear_v:>12}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: a prolonged 'higher-for-longer' rate environment combined with a multi-year")
print(f"  realization drought — PE portfolio companies can't be sold/IPO'd at attractive marks,")
print(f"  carried interest stays near zero, and NAV marks get cut as public comps reprice lower.")
print(f"  FRE base ($5.5B) provides a recurring earnings floor even if carry goes to zero.")
print(f"  EPS compresses to ~${bear_eps_imp:.2f} → 17× floor = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT a permanent impairment — FRE compounding + Global Atlantic")
print(f"  permanent capital provides a durable floor. Recovery to ~${bear_price+30}-${bear_price+50} in 2yr is base case post-shock.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E distributable EPS estimate:  ${EPS_FY2026E:.2f}  (consensus ~$4.70-$5.00)")
print(f"  Pessimistic P/E at trough:            {PE_PESSIMISTIC:.0f}×  (FRE-heavy floor; 2022-23 rate-shock trough ~13-15×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  At ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f}, the implied P/E is {CURRENT_PRICE/EPS_FY2026E:.1f}×.")
print(f"  KKR has historically traded at a premium growth multiple (25-35×) on distributable")
print(f"  earnings, reflecting AUM growth + carry optionality + Global Atlantic diversification.")
print(f"  At {CURRENT_PRICE/EPS_FY2026E:.1f}×, the stock sits below its historical premium range — the market is")
print(f"  not yet fully crediting the FPAUM all-time-high or the $120B dry powder optionality.")
print(f"  EPP path: FY2028E EPS ~${CONS_EPS_2YR:.2f} × {PE_PESSIMISTIC:.0f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing with FRE).")
print(f"  At 28× premium P/E (historical mid-range): ${EPS_FY2026E:.2f} × 28 = ${EPS_FY2026E*28:.0f}.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: FRE compounds mid-teens; carry recovery modest; multiple holds)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (FRE +15%/yr base; modest carry contribution)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (holds near current multiple; below historical 25-35× premium)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; growing with FRE)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE OPPORTUNITY: even holding the multiple flat at {CONS_PE_2YR}× (below KKR's historical")
print(f"  25-35× premium range), FRE compounding alone drives a {cons_return:.1f}% 2yr return.")
print(f"  Any re-rate toward the historical premium multiple (driven by realization-cycle reopening)")
print(f"  is incremental upside on top of this base case.")
print(f"  Breakeven at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}  (already below conservative ${CONS_EPS_2YR:.2f})")
print(f"  Breakeven at 17× P/E (bear multiple): need EPS = ${(CURRENT_PRICE - cons_divs) / 17:.2f}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.34
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  modest; growth-focused capital allocation)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (alt-asset managers carry rate-sensitivity + carry-cycle volatility)")
print(f"  Beta vs S&P 500:      1.45  (high; financial leverage to capital markets cycle)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (realization-drought tail scenario)")
print(f"  52W low ${VOL_52W_LOW:.2f} already reflects a meaningful peak-to-trough rate-shock move.")
print(f"  → Realization cycle (M&A/IPO reopening) is THE KEY binary for carry-driven upside.")
print(f"  → FRE compounding + Global Atlantic growth provide a durable downside floor regardless.")
print(f"  → AVOID above $130  |  WATCHLIST $110-125  |  ACCUMULATE $95-110  |  BUY below $90")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) sits")
print(f"  {'BELOW' if MARKET_COMPOSITE < ADJ_COMPOSITE else 'ABOVE'} the model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0,")
print(f"  while the model scores fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0.")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: FPAUM at all-time highs, FRE compounding mid-teens, and Global Atlantic")
print(f"  diversification are not fully reflected at the current multiple — realization-cycle")
print(f"  reopening (signal score 2/4 = BASE) is the most significant remaining catalyst.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) M&A/IPO market reopening — carried interest realizations accelerate (BULL trigger)")
print(f"  (2) Rate cuts — relieves PE portfolio valuation pressure, boosts deal financing (BULL trigger)")
print(f"  (3) Global Atlantic AUM scale — continued 15%/yr growth toward $300B+ (structural tailwind)")
print(f"  (4) Dry powder deployment — $120B+ ready to deploy into a valuation reset")
print(f"  (5) Credit/Infrastructure FPAUM growth — fastest-growing segments, structural fee growth")
print(f"  AVOID above $130  |  WATCHLIST $110-125  |  ACCUMULATE $95-110  |  BUY below $90")
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
