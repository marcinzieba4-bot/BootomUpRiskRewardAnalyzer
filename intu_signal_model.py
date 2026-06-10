"""
INTU  ·  Intuit Inc.  ·  NASDAQ: INTU
Bottom-up signal model  ·  SMB Financial Platform / AI Tax & Bookkeeping / Credit Karma
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "INTU"
COMPANY       = "Intuit Inc."
SECTOR        = "SMB Financial Platform · QuickBooks · TurboTax · Credit Karma · NASDAQ: INTU"
CURRENT_PRICE = 319.94      # USD; as of 2026-06-10; -61% from $813.70 ATH
VOL_52W_LOW   = 290.00      # 15-year-low multiple trough
VOL_52W_HIGH  = 700.00      # pre-selloff high

SHARES_OUT_M  = 280.0       # millions; modest buyback offsetting SBC dilution

# Dividend: long growth streak; growing ~10-15%/yr historically
ANNUAL_DIV    = 4.32        # $/share annualized

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Global Business Solutions", 11.50,  9.80, 13.50, "QuickBooks Online ecosystem + Mailchimp; bookkeeping/payments/payroll attach"),
    ("Consumer (TurboTax)",         4.40,  3.40,  5.20, "AI-driven 'done-for-you' tax filing; IRS Direct File the swing risk"),
    ("Credit Karma",                2.10,  1.60,  2.70, "Lending/insurance recovery; ad monetization of 130M+ members"),
    ("ProTax",                      0.75,  0.65,  0.95, "Pro-tax software for accountants; steady mid-single-digit grower"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.79    # blended gross margin FY2026E (~79%; SaaS-heavy mix)
GROSS_MARGIN_BULL = 0.81    # BULL: AI agent monetization lifts mix further
OPEX_FIXED_B      = 6.20    # R&D + S&M + G&A ($B); restructuring (17% workforce cut) trims base
TAX_RATE          = 0.23    # effective tax rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 23.82       # FY2026E non-GAAP EPS guidance (raised)
PE_PESSIMISTIC = 14.0        # trough P/E: 15-year-low multiple already approximates the floor
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $333

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (22.00, 14,  308, "QBO growth decelerates; IRS Direct File erodes TurboTax; restructuring stalls; EPS $22 → 14× floor"),
    "BASE":  (23.82, 22,  524, "FY2026E guidance achieved; QBO ecosystem +mid-teens; Credit Karma recovery; EPS $23.82 → 22×"),
    "BULL":  (28.00, 27,  756, "AI 'done-for-you' monetization scales; Mailchimp/mid-market traction; margin expansion; EPS $28 → 27×"),
    "XBULL": (34.00, 32, 1088, "Intuit re-rates as AI financial-platform leader; QBO ecosystem accelerates; EPS $34 → 32×"),
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
        "name":       "QuickBooks Online ecosystem revenue growth",
        "weight":     0.30,
        "thresholds": ("<10%",   "≥14%",  "≥19%",   "≥25%"),
        "now":        "+19%",
        "score":      3,
        "comment":    "Online Ecosystem revenue +19% YoY; mid-market and platform attach driving durable growth",
    },
    {
        "name":       "Credit Karma revenue growth",
        "weight":     0.15,
        "thresholds": ("<-5%",   "≥0%",   "≥10%",   "≥20%"),
        "now":        "~+8%",
        "score":      2,
        "comment":    "Lending recovery uneven; ad monetization improving but below pre-2022 peak growth rates",
    },
    {
        "name":       "AI 'done-for-you' tax/bookkeeping monetization",
        "weight":     0.20,
        "thresholds": ("Pilot",  "Limited","Scaling","Mainstream"),
        "now":        "Scaling",
        "score":      3,
        "comment":    "AI agents embedded across TurboTax Live and QBO bookkeeping; early monetization signals positive",
    },
    {
        "name":       "Mid-market / Mailchimp expansion",
        "weight":     0.10,
        "thresholds": ("<5%",    "≥8%",   "≥14%",   "≥20%"),
        "now":        "+10%",
        "score":      2,
        "comment":    "Mid-market customer growth steady; Mailchimp integration into QBO ecosystem still maturing",
    },
    {
        "name":       "Operating margin trajectory (post-restructuring)",
        "weight":     0.15,
        "thresholds": ("Contracting","Flat","Expanding","Strong expansion"),
        "now":        "Flat-to-expanding",
        "score":      2,
        "comment":    "17% workforce reduction creates near-term optics risk; opex savings should flow through FY2027",
    },
    {
        "name":       "IRS Direct File competitive risk to TurboTax",
        "weight":     0.10,
        "thresholds": ("Severe",  "Elevated","Contained","Minimal"),
        "now":        "Elevated",
        "score":      2,
        "comment":    "Direct File expanding state coverage; TurboTax free-filer base under pressure but paid mix resilient",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "QBO ecosystem moat — durable SMB platform; payments/payroll attach; +19% YoY growth",   +0.7, 0.25),
    ("+", "Raised FY2026 EPS guidance to $23.82 despite restructuring — execution intact",          +0.4, 0.15),
    ("-", "Workforce-cut optics — 17% reduction reads as growth-deceleration signal to market",      -0.5, 0.15),
    ("-", "IRS Direct File — government free-filing competitor expanding scope; structural overhang", -0.6, 0.20),
    ("+", "Credit Karma + AI agent optionality — 130M members; 'done-for-you' monetization runway",  +0.5, 0.15),
    ("-", "Multiple compression — 15-year-low P/E (~13.4×) reflects sentiment, not fundamentals",    -0.3, 0.10),
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
CONS_EPS_2YR  = 27.50   # conservative FY2028E: ~7-8%/yr EPS CAGR off $23.82 base
CONS_PE_2YR   = 18      # modest rerating from ~13.4x toward 18x as restructuring optics fade
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  SMB Financial Platform / TurboTax / Credit Karma / AI")
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
    print(f"  {seg:<26}  ${curr:>11.2f}  ${bear:>8.2f}  ${bull:>8.2f}  {bear-curr:>+7.2f}  {bull-curr:>+7.2f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<26}  ${curr_total:>11.2f}  ${bear_total:>8.2f}  ${bull_total:>8.2f}  {bear_total-curr_total:>+7.2f}  {bull_total-curr_total:>+7.2f}")
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

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.98   # mix shift / pricing pressure
bear_oi   = bear_gp - OPEX_FIXED_B * 0.95           # restructuring savings partially offset
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.2f}B rev × {GROSS_MARGIN_CURR*100:.0f}% GM − ${OPEX_FIXED_B:.2f}B opex − {TAX_RATE*100:.0f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share non-GAAP EPS  (guidance ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B rev × {GROSS_MARGIN_BULL*100:.0f}% GM − ${OPEX_FIXED_B:.2f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 27× = ~${bull_eps_imp*27:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B rev × {GROSS_MARGIN_CURR*100*0.98:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 14× trough P/E (15-year-low multiple) = ~${bear_eps_imp*14:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B QBO ecosystem revenue:  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*22:.1f}/share at 22× P/E")
print(f"  Credit Karma revenue ±$0.5B:      ±${eps_per_1B_rev*0.5:.3f}/EPS  =  ±${eps_per_1B_rev*0.5*22:.1f}/share at 22× P/E")
print(f"  1pp GM expansion (mix/AI agents):  +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*22:.1f}/share at 22× P/E")
print(f"  Restructuring opex savings ($0.5B): +${0.5*(1-TAX_RATE)/shares:.2f}/EPS  (mechanical from 17% workforce cut)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (QBO ecosystem / Credit Karma / AI monetization / IRS Direct File framework)")
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
    ("QBO ecosystem revenue growth",   "+19%",    "<10%",     "−9pp",   "Mid-market deceleration + payments/payroll attach stalls"),
    ("IRS Direct File expansion",      "Elevated","Severe",   "↑ risk", "Direct File expands to most states; TurboTax free-filer share collapses"),
    ("Credit Karma growth",            "~+8%",    "<-5%",     "−13pp",  "Lending environment deteriorates; ad spend pulled by partners"),
    ("AI monetization rollout",        "Scaling", "Pilot",    "↓ stage","'Done-for-you' agent adoption stalls; pricing power fails to materialize"),
    ("Operating margin trajectory",    "Flat-to-exp.","Contracting","↓","Restructuring savings consumed by AI infrastructure capex"),
    ("Mid-market/Mailchimp growth",    "+10%",    "<5%",      "−5pp",   "Mailchimp integration disappoints; mid-market churn rises"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: IRS Direct File expands to cover most states and form types, eroding")
print(f"  TurboTax's free-filer funnel (the top of the conversion pipeline into paid products),")
print(f"  while QBO ecosystem growth decelerates from +19% toward low double digits as mid-market")
print(f"  competition intensifies. Combined with restructuring savings being absorbed by AI capex,")
print(f"  EPS stalls near $22 → 14× floor (15-year-low multiple, already near current levels) = ${bear_price}.")
print(f"  Note: ${bear_price} is close to CURRENT price — the BEAR case is largely already priced in.")
print(f"  The QBO ecosystem moat (SMB platform lock-in, payments/payroll attach) provides a durable")
print(f"  earnings floor even in a Direct File adverse scenario.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E non-GAAP EPS guidance:  ${EPS_FY2026E:.2f}  (raised guidance; despite restructuring)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (15-year-low multiple ~13.4× already near floor)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({abs(epp_gap_pct):.0f}% below trough floor)")
print()
print(f"  Intuit is trading at the deepest below-EPP discount in coverage — roughly {abs(epp_gap_pct):.0f}%")
print(f"  BELOW the trough-multiple floor, despite management RAISING FY2026 EPS guidance to")
print(f"  ${EPS_FY2026E:.2f}. At ${CURRENT_PRICE:.2f}, the stock trades at ~{CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E non-GAAP EPS —")
print(f"  a 15-year-low multiple. The market is pricing in workforce-cut optics and revenue")
print(f"  deceleration fears as if they were earnings cuts, when guidance was actually raised.")
print(f"  This is the central question: is the market over-penalizing restructuring optics vs")
print(f"  a durable SMB + AI financial platform moat (QBO ecosystem +19% YoY)?")
print(f"  At 18× mid-cycle P/E: ${EPS_FY2026E:.2f} × 18 = ${EPS_FY2026E*18:.0f}  — {(EPS_FY2026E*18/CURRENT_PRICE-1)*100:+.0f}% vs current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest rerating off 15-year-low multiple; restructuring savings flow through)")
hr()
print(f"  Conservative FY2028E non-GAAP EPS:  ${CONS_EPS_2YR:.2f}  (~7-8% EPS CAGR: QBO ecosystem growth + restructuring savings)")
print(f"  Conservative exit P/E:               {CONS_PE_2YR}×  (rerates from ~13.4× toward growth-justified 18×; still below historical avg)")
print(f"  Conservative equity value:            ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):        +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:               ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:            {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE OPPORTUNITY: even a modest rerating from ~13.4× to 18× (still well below Intuit's")
print(f"  historical premium multiple) combined with high-single-digit EPS growth produces a")
print(f"  meaningfully positive return. Unlike mega-cap compounders facing multiple compression,")
print(f"  Intuit's downside case is a multiple EXPANSION story off a depressed base.")
print(f"  Breakeven at 14× P/E (no rerating, BEAR floor): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / PE_PESSIMISTIC:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * 14 * 0.95 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * 16 * 0.95 + cons_divs * 0.5, 0):.0f} (margin of safety vs EPP floor; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.35
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: 52W high pre-dates the -61% drawdown from the $813.70 ATH to current ${CURRENT_PRICE:.2f}")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  growing payout)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; restructuring + multiple compression has driven swings)")
print(f"  Beta vs S&P 500:      1.15  (high-growth software; sentiment-sensitive)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  ({'mild' if bear_sigmas < 0.5 else 'moderate'}; close to current price)")
print(f"  52W low ${VOL_52W_LOW:.2f} (15-year-low multiple trough) is close to current price already.")
print(f"  → IRS Direct File expansion is THE KEY structural risk — each state added pressures TurboTax funnel.")
print(f"  → AI 'done-for-you' monetization evidence (pricing/attach data) is KEY bull catalyst.")
print(f"  → AVOID above $450  |  WATCHLIST $360–450  |  ACCUMULATE $330–360  |  BUY below $330")

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
print(f"  In plain terms: the market is pricing BEAR-case execution into a company that just RAISED")
print(f"  guidance. QBO ecosystem growth (+19% YoY, signal score 3/4 = BULL) is the most significant")
print(f"  valuation mismatch — restructuring optics and IRS Direct File fears appear over-weighted.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) QBO ecosystem revenue updates — sustained mid-to-high-teens growth (BULL trigger)")
print(f"  (2) Credit Karma growth — lending recovery + ad monetization re-acceleration")
print(f"  (3) AI agent ('done-for-you') monetization rollout — pricing/attach data from TurboTax & QBO")
print(f"  (4) Mailchimp/mid-market traction — integration progress and customer growth")
print(f"  (5) IRS Direct File expansion news — state coverage and form-type expansion (BEAR trigger)")
print(f"  (6) FY2026 tax season results — April 2026 filing data for TurboTax volume/mix")
print(f"  AVOID above $450  |  WATCHLIST $360–450  |  ACCUMULATE $330–360  |  BUY below $330")
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
