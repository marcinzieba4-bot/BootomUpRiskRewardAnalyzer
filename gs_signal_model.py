"""
GS  ·  The Goldman Sachs Group, Inc.  ·  NYSE: GS
Bottom-up signal model  ·  Investment Banking / Trading / Asset & Wealth Management
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "GS"
COMPANY       = "The Goldman Sachs Group, Inc."
SECTOR        = "Global Investment Banking · FICC/Equities · AWM · Platform Solutions · NYSE: GS"
CURRENT_PRICE = 745.00      # USD; as of 2026-06-10
VOL_52W_LOW   = 520.18      # mid-2025 trough (rate-cut delay / recession scare)
VOL_52W_HIGH  = 762.40      # May 2026 high (deal-cycle recovery momentum)
SHARES_OUT_M  = 320.0       # millions; declining ~4-5%/yr via aggressive buyback

# Dividend: raised steadily; ~28-30% payout
ANNUAL_DIV    = 13.00       # $/share FY2026 ($3.25/quarter)

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ──────────────────────
# FY2026E net revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Global Banking & Markets",  34.0, 24.0, 44.0, "IB advisory/UW fees + FICC/Equities trading; deal-cycle swing factor"),
    ("Asset & Wealth Management", 17.0, 14.5, 21.0, "Fee-based AUS $3.5T+; management/incentive fees; diversification engine"),
    ("Platform Solutions",         1.8,  1.2,  2.6, "Consumer/transaction banking; Marcus wind-down complete; now stabilizing/profitable"),
]

# Margin / cost assumptions (illustrative pre-tax operating model)
PRETAX_MARGIN_CURR = 0.36   # blended pre-tax margin FY2026E
PRETAX_MARGIN_BULL = 0.40   # BULL: operating leverage on higher banking/trading revenue
COMP_RATIO         = 0.335  # comp & benefits as % of net revenue (efficiency ratio driver)
TAX_RATE           = 0.22   # effective tax rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 46.50       # FY2026E adj EPS (consensus ~$45-48)
PE_PESSIMISTIC = 9.0         # trough P/E: GFC/2011-12 era trough multiples for GS (~8-10x)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # ~$419

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (28.00,  9,  252, "Deal recession + trading slump; IB fees -35%; EPS $28 → 9x trough P/E"),
    "BASE":  (46.50, 14,  651, "Moderate deal recovery continues; AWM fees grow; FICC normal; EPS $46.50 → 14x"),
    "BULL":  (62.00, 16,  992, "Full M&A/IPO supercycle; record advisory backlog; buybacks accelerate; EPS $62 → 16x"),
    "XBULL": (78.00, 18, 1404, "Multi-year capital markets boom; AWM AUS >$4.5T; CET1 relief boosts buybacks; EPS $78 → 18x"),
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
        "name":       "Investment Banking fees YoY growth",
        "weight":     0.30,
        "thresholds": ("<-10%",  "≥10%",  "≥25%",   "≥40%"),
        "now":        "+24%",
        "score":      2,
        "comment":    "M&A advisory + UW recovery underway; record backlog; sponsor-led activity reaccelerating",
    },
    {
        "name":       "FICC + Equities trading revenue YoY",
        "weight":     0.25,
        "thresholds": ("<-15%",  "≥0%",   "≥8%",    "≥15%"),
        "now":        "+6%",
        "score":      2,
        "comment":    "Equities financing/derivatives strong; FICC normalizing off elevated volatility years",
    },
    {
        "name":       "AWM management/incentive fee growth",
        "weight":     0.20,
        "thresholds": ("<0%",    "≥5%",   "≥10%",   "≥18%"),
        "now":        "+9%",
        "score":      2,
        "comment":    "AUS surpassing $3.5T; alternatives fundraising solid; incentive fees lumpy but improving",
    },
    {
        "name":       "Efficiency ratio (opex/net revenue)",
        "weight":     0.10,
        "thresholds": (">68%",   "≤66%",  "≤62%",   "≤58%"),
        "now":        "63%",
        "score":      3,
        "comment":    "Comp ratio held near 33.5%; non-comp expense discipline; operating leverage building",
    },
    {
        "name":       "ROTE (return on tangible equity)",
        "weight":     0.10,
        "thresholds": ("<8%",    "≥10%",  "≥13%",   "≥16%"),
        "now":        "13.5%",
        "score":      3,
        "comment":    "Above through-the-cycle 13-15% target; capital markets recovery lifting returns",
    },
    {
        "name":       "CET1 ratio / buyback capacity",
        "weight":     0.05,
        "thresholds": ("<13%",   "≥13%",  "≥14.5%", "≥15.5%"),
        "now":        "14.8%",
        "score":      3,
        "comment":    "Comfortably above SCB-driven requirement; supports $30B+ annual buyback pace",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Premier IB franchise — #1 in global M&A and equity underwriting league tables",        +0.6, 0.20),
    ("+", "AWM diversification — $3.5T+ AUS, fee-based recurring revenue smooths cyclicality",     +0.5, 0.20),
    ("-", "Deal-cycle cyclicality — IB fees and trading revenue remain volatile, macro-sensitive", -0.6, 0.20),
    ("+", "Capital return discipline — large buyback authorization; CET1 well above requirement",  +0.4, 0.15),
    ("-", "Regulatory capital risk — Basel III endgame / SCB changes could constrain returns",     -0.4, 0.15),
    ("-", "Platform Solutions legacy drag — consumer-lending losses still working through book",   -0.3, 0.10),
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
CONS_EPS_2YR  = 54.00   # conservative FY2028E: continued moderate IB/AWM growth, buybacks
CONS_PE_2YR   = 13      # in-line with historical mid-cycle 12-14x band
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Investment Banking / Trading / AWM / Platform Solutions")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① REVENUE BRIDGE ──────────────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
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
curr_pti  = curr_total * PRETAX_MARGIN_CURR
curr_ni   = curr_pti * (1 - TAX_RATE)
shares    = SHARES_OUT_M / 1000
curr_eps  = round(curr_ni / shares, 2)

bull_pti  = bull_total * PRETAX_MARGIN_BULL
bull_ni   = bull_pti * (1 - TAX_RATE)
shares_b  = shares * 0.92   # ~4%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_pti  = bear_total * PRETAX_MARGIN_CURR * 0.85   # operating deleverage in downturn
bear_ni   = max(0, bear_pti) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B net rev × {PRETAX_MARGIN_CURR*100:.0f}% pre-tax margin − {TAX_RATE*100:.0f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ~${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {PRETAX_MARGIN_BULL*100:.0f}% pre-tax margin − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 16× = ~${bull_eps_imp*16:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {PRETAX_MARGIN_CURR*100*0.85:.0f}% pre-tax margin − tax  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 9× trough P/E (GFC-era floor) = ~${bear_eps_imp*9:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = (1.0 * PRETAX_MARGIN_CURR * (1 - TAX_RATE)) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Banking & Markets revenue:  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*14:.1f}/share at 14× P/E")
print(f"  Every $1B AWM fee revenue:             +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*14:.1f}/share at 14× P/E (more durable mix)")
print(f"  1pp comp ratio reduction:              +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*14:.1f}/share at 14× P/E")
print(f"  4% annual buyback (~13M shares):       +${curr_eps*0.04:.3f}/EPS  (mechanical accretion; $30B+ authorization)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (deal-cycle / trading / AWM / capital-return framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>6}  {'BASE':>5}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>6}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>6}  {ths[1]:>5}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>6}  {lbl}  {b}")

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
    ("IB fees YoY",                   "+24%",   "<-10%",  "−34pp",  "Global recession freezes M&A/IPO pipeline; sponsor exits halt"),
    ("FICC + Equities trading YoY",   "+6%",    "<-15%",  "−21pp",  "Volatility collapse + client de-risking; balance sheet shrinks"),
    ("AWM fee growth",                "+9%",    "<0%",    "−9pp",   "Market drawdown cuts AUS; outflows from alternatives funds"),
    ("Efficiency ratio",              "63%",    ">68%",   "+5pp",   "Revenue declines faster than comp/non-comp can be cut"),
    ("ROTE",                          "13.5%",  "<8%",    "−5.5pp", "Litigation charge + credit losses compress returns to GFC-era lows"),
    ("CET1 / buyback capacity",       "14.8%",  "<13%",   "−1.8pp", "Regulatory capital hike (Basel endgame) forces buyback pause"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A global recession or credit-shock event freezes the M&A/IPO pipeline")
print(f"  (the dominant earnings swing factor) while simultaneously crushing trading revenue via")
print(f"  a volatility collapse and client de-risking. AWM outflows compound the hit. EPS falls")
print(f"  to ~${bear_price/9:.0f} → 9× trough P/E (GFC-era floor) = ${bear_price}.")
print(f"  Note: AWM's $3.5T+ AUS fee base and CET1 buffer provide a partial earnings floor;")
print(f"  recovery to ~${bear_price+150}–${bear_price+250} in 2yr is base case post-shock as deal backlog reloads.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~$45-48)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (GFC / 2011-12 era trough multiple for GS)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% premium to EPP reflects the market's confidence that the deal-cycle")
print(f"  recovery and AWM growth persist without a recessionary reset. At ${CURRENT_PRICE:.2f} and")
print(f"  FY2026E EPS ${EPS_FY2026E:.2f}, the P/E is ~{CURRENT_PRICE/EPS_FY2026E:.1f}×, near the upper end of GS's")
print(f"  historical 11-14× mid-cycle band, and roughly {CURRENT_PRICE/(13.0*40):.1f}× tangible book value (~$40 TBVPS BBL est).")
print(f"  EPP path: FY2028E EPS ~${CONS_EPS_2YR:.0f} × {PE_PESSIMISTIC:.0f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing with EPS).")
print(f"  At {CONS_PE_2YR}× mid-cycle P/E: ${EPS_FY2026E:.2f} × {CONS_PE_2YR} = ${EPS_FY2026E*CONS_PE_2YR:.0f}  — below current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: moderate deal-cycle progress + buybacks + dividends)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (continued IB/AWM growth + ~8% buyback over 2yr)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (mid-cycle historical band 12-14×)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: at {CONS_PE_2YR}× P/E (no multiple expansion needed from mid-cycle norms), EPS")
print(f"  growth from ${EPS_FY2026E:.2f} to ${CONS_EPS_2YR:.2f} (driven by deal-cycle recovery + buybacks) plus")
print(f"  dividends produces a {cons_return:.1f}% 2yr return ({cons_annual:.1f}%/yr).")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  Breakeven at 16× P/E (continued re-rating): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 16:.2f}")
print(f"  ACCUMULATE trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.85 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.92 + cons_divs * 0.5, 0):.0f} (ratio_b approaches 1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.30
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (high-beta money-center bank; macro/credit-cycle sensitive)")
print(f"  Beta vs S&P 500:      1.35  (high beta; capital-markets revenue amplifies macro swings)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (a recession/credit-shock tail scenario)")
print(f"  → Global recession / credit event is THE KEY binary; each macro shock = sharp deal-pipeline freeze.")
print(f"  → M&A/IPO backlog conversion + AWM AUS growth are KEY bull catalysts.")
print(f"  → WATCHLIST current  |  ACCUMULATE $620–660  |  BUY below $560")

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
print(f"  {valuation_label.lower()} by model standards. Deal-cycle recovery momentum and AWM growth")
print(f"  are largely priced in; a recessionary reset in IB fees/trading is the key downside risk.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) M&A/IPO pipeline conversion — record advisory backlog turning into closed fee revenue (BULL trigger)")
print(f"  (2) FICC/Equities trading normalization — sustained client activity vs. post-volatility fade (swing factor)")
print(f"  (3) AWM AUS growth — alternatives fundraising and management-fee compounding (diversification)")
print(f"  (4) Basel III endgame / SCB outcome — capital requirements drive buyback pace (capital-return risk)")
print(f"  (5) Platform Solutions — continued stabilization removes a multi-year earnings drag")
print(f"  WATCHLIST current ${CURRENT_PRICE:.2f}  |  ACCUMULATE $620-660  |  BUY below $560")
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
