"""
UBER  ·  Uber Technologies, Inc.  ·  NYSE: UBER
Bottom-up signal model  ·  Mobility / Delivery / Freight / Autonomous Vehicle Platform
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "UBER"
COMPANY       = "Uber Technologies, Inc."
SECTOR        = "Ridesharing · Food Delivery · Freight · Autonomous Vehicle Platform · NYSE: UBER"
CURRENT_PRICE = 70.36        # USD; close 2026-07-31 (verified live)
VOL_52W_LOW   = 65.41        # 2026 trough — the stock is near this level right now
VOL_52W_HIGH  = 101.99       # 2025/26 peak
SHARES_OUT_M  = 2_035.0      # millions; $143.2B mkt cap / $70.36
ANNUAL_DIV    = 0.0          # $/share; no dividend, capital returned via buyback ($7B authorization)

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ──────────────────────────────────────
# Q1 2026 actual: gross bookings $53.7B (+25%, above guide), adj EBITDA $2.5B (+33%, margin
# 4.6% of bookings), non-GAAP EPS $0.72 (+44%), revenue $13.2B (+14.5%, hit by a $1B UK tax
# accounting headwind). Q2 guide/consensus: bookings $56.25-57.75B, EPS $0.83 consensus.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Mobility (rides)",     31.0, 27.0, 36.0, "Core rideshare; steady take-rate expansion; the segment most exposed to AV disruption long-term"),
    ("Delivery (Eats)",      15.5, 13.5, 18.0, "Uber One membership (50M+) driving frequency and retention; advertising is a growing high-margin kicker"),
    ("Freight",               1.4,  1.1,  1.8, "Small, cyclical, non-core; a minor drag/contributor either way"),
]

# Margin assumptions (adjusted EBITDA as % of revenue, translated to a net-income-equivalent proxy)
OP_MARGIN_CURR   = 0.180    # FY2026E blended adj EBITDA margin on revenue (~4.6% of GROSS BOOKINGS translates to a higher % of net revenue)
OP_MARGIN_BULL   = 0.215    # BULL: take-rate expansion + advertising + AV-platform fees all lift the margin
OP_MARGIN_BEAR   = 0.135    # BEAR: AV disruption forces pricing concessions to retain drivers/riders during the transition
TAX_RATE         = 0.220    # effective tax rate

# ── AUTONOMOUS VEHICLE PLATFORM CALCULATOR (the Uber-specific angle) ─────────
AV_TRIP_GROWTH_YOY_X  = 10   # AV trips on the Uber platform grew this many times YoY, Q1 2026
AV_PARTNERS           = 30   # number of autonomous vehicle partners across mobility and delivery
AV_CITIES_TARGET_2026 = 15   # cities targeted for AV operation by end of 2026
WAYMO_WEEKLY_RIDES_K  = 250  # thousand paid Waymo rides per week via the Uber partnership
Q1_BOOKINGS_GROWTH_PCT = 25  # % YoY gross bookings growth, Q1 2026
UK_TAX_HEADWIND_B      = 1.0 # $B one-time revenue accounting headwind from UK tax law changes, Q1 2026

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 3.30         # $/share non-GAAP FY2026E; Q1 $0.72 (+44%) annualizing with continued growth
PE_PESSIMISTIC = 14.0         # trough P/E: a reasonable floor for a company now solidly GAAP-and-non-GAAP
                               # profitable with double-digit bookings growth; not a distressed-multiple business anymore
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 2.15, 13,   28, "AV platforms (Waymo, Tesla) disintermediate Uber's demand-aggregation role faster than expected"),
    "BASE":  ( 3.70, 18,   67, "Gross bookings keep compounding at a mid-teens-to-20% pace; AV remains a platform partner, not a threat"),
    "BULL":  ( 4.74, 21,  100, "Uber becomes the default distribution layer for AV fleets across multiple operators; margin expands further"),
    "XBULL": ( 6.00, 24,  144, "Uber = the operating system for autonomous urban mobility globally, capturing fees across every AV operator's fleet"),
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
        "name":       "Gross bookings YoY growth",
        "weight":     0.20,
        "thresholds": ("<12%",   "≥18%",   "≥24%",   "≥30%"),
        "now":        "+25%",
        "score":      3,
        "comment":    "$53.7B in Q1, above the guided range — the core marketplace is not slowing down",
    },
    {
        "name":       "Adjusted EBITDA growth",
        "weight":     0.20,
        "thresholds": ("<15%",   "≥25%",   "≥33%",   "≥42%"),
        "now":        "+33%",
        "score":      3,
        "comment":    "$2.5B, margin 4.6% of bookings and rising — profitability is scaling faster than revenue",
    },
    {
        "name":       "AV trip growth on the platform",
        "weight":     0.20,
        "thresholds": ("<2x",    "≥4x",    "≥7x",    "≥10x"),
        "now":        "10x+",
        "score":      4,
        "comment":    "AV trips grew more than 10x YoY — the clearest evidence yet that Uber is capturing AV demand, not losing it",
    },
    {
        "name":       "AV partner breadth",
        "weight":     0.15,
        "thresholds": ("<10",    "≥15",    "≥25",    "≥35"),
        "now":        "30+",
        "score":      3,
        "comment":    "30+ AV partners across mobility and delivery — Uber is positioning as the aggregator across operators, not betting on one",
    },
    {
        "name":       "Non-GAAP EPS growth",
        "weight":     0.15,
        "thresholds": ("<15%",   "≥25%",   "≥35%",   "≥45%"),
        "now":        "+44%",
        "score":      3,
        "comment":    "$0.72 in Q1, +44% YoY — profitability growth is outpacing revenue growth, a sign of genuine operating leverage",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.10,
        "thresholds": (">24x",   "≤19x",   "≤15x",   "≤11x"),
        "now":        "~21.3x",
        "score":      2,
        "comment":    "21.3× FY2026E non-GAAP EPS — reasonable, not cheap, for a company growing bookings 25% and EPS 44%",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "AV trips growing 10x+ YoY on the platform — the single best disproof of the 'AVs kill Uber' thesis available", +0.9, 0.25),
    ("+", "Genuine operating leverage — EPS growth (+44%) outpacing bookings growth (+25%) for multiple quarters running", +0.6, 0.20),
    ("-", "Valuation near the 52-week low despite the strong operating momentum — the market isn't yet crediting the AV pivot", -0.3, 0.10),
    ("+", "30+ AV partnerships is a platform strategy, not a single-bet — Uber wins whichever AV operator scales fastest", +0.5, 0.20),
    ("-", "AV economics long-term are genuinely uncertain — today's take-rate model may not survive a fully autonomous fleet mix", -0.5, 0.15),
    ("+", "Uber One membership (50M+) and advertising are two underappreciated, high-margin growth engines beyond core rides/delivery", +0.4, 0.10),
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
CONS_EPS_2YR  = 4.30    # conservative FY2028E: ~14.2% EPS CAGR — a real deceleration from the current 44% pace
CONS_PE_2YR   = 17      # modest re-rating from ~21.3x — reflects continued AV-thesis uncertainty
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Mobility / Delivery / Freight / Autonomous Vehicle Platform")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))
print(f"  ⚠ Q2 2026 results due 2026-08-05 — two days after this refresh. Street consensus: EPS $0.83,")
print(f"  revenue $14.27B, gross bookings ~$57.2B (+18-22% cc). Figures below use Q1 actuals + guidance.")

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<28}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<28}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<28}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  Q1 2026 actual: gross bookings $53.7B (+25%), revenue $13.2B (+14.5%, incl. ${UK_TAX_HEADWIND_B:.0f}B UK tax headwind)")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_op   = curr_total * OP_MARGIN_CURR
curr_eps  = round(curr_op * (1 - TAX_RATE) / shares, 2)

bull_op   = bull_total * OP_MARGIN_BULL
shares_b  = shares * 0.97
bull_eps_imp = round(bull_op * (1 - TAX_RATE) / shares_b, 2)

bear_op   = bear_total * OP_MARGIN_BEAR
bear_eps_imp = round(bear_op * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {OP_MARGIN_CURR*100:.1f}% margin proxy − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {OP_MARGIN_BULL*100:.1f}% margin, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 21× = ~${bull_eps_imp*21:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {OP_MARGIN_BEAR*100:.1f}% margin (AV transition pricing pressure)")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 13× trough = ~${bear_eps_imp*13:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# AV PLATFORM CHECK
print()
print(f"  AUTONOMOUS VEHICLE PLATFORM CHECK  (the Uber-specific angle):")
print(f"  AV trip growth (Q1 2026):       {AV_TRIP_GROWTH_YOY_X}x+  YoY")
print(f"  AV partners:                    {AV_PARTNERS}+  across mobility and delivery")
print(f"  Cities targeted for AV (2026):  up to {AV_CITIES_TARGET_2026}")
print(f"  Waymo weekly paid rides:        {WAYMO_WEEKLY_RIDES_K}K  (via the Uber partnership; Waymo is Alphabet-owned)")
print()
print(f"  This is the single most important data set in the Uber thesis right now. The bear case")
print(f"  for Uber has always been 'once AVs work, riders go direct to the AV operator and Uber's")
print(f"  demand-aggregation layer becomes worthless.' The Q1 data says the opposite is happening")
print(f"  so far: AV trips on Uber's platform grew 10x+ YoY, and Uber has partnered with 30+ AV")
print(f"  operators rather than betting on a single winner. Uber is positioning itself as the")
print(f"  distribution layer FOR autonomous vehicles, not the business autonomous vehicles replace.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * OP_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_marg = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 14.5% margin proxy):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*18:.2f}/share at 18× P/E")
print(f"  Every 1pp of margin:                        +${eps_per_1pp_marg:.3f}/EPS  = +${eps_per_1pp_marg*18:.2f}/share at 18× P/E")
print(f"  Every 1 turn of P/E:                        ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (bookings / EBITDA / AV trips / AV partners / EPS growth / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<34}  {'BEAR':>6}  {'BASE':>7}  {'BULL':>7}  {'XBULL':>7}  {'NOW':>8}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<34}  {ths[0]:>6}  {ths[1]:>7}  {ths[2]:>7}  {ths[3]:>7}  {s['now']:>8}  {lbl}  {b}")
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
print(f"  {'Signal':<30}  {'Current':>9}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Gross bookings YoY",         "+25%",   "<12%",    "-13pp",  "Consumer spending softens; AV-operator direct apps start winning share"),
    ("Adjusted EBITDA growth",     "+33%",   "<15%",    "-18pp",  "Pricing concessions to retain drivers/riders during an AV transition compress margin"),
    ("AV trip growth",             "10x+",   "<2x",     "flat",   "AV operators bypass Uber's platform in favor of proprietary apps"),
    ("AV partner breadth",         "30+",    "<10",     "-20",    "Consolidation among AV operators reduces the number of platform partners"),
    ("Non-GAAP EPS growth",        "+44%",   "<15%",    "-29pp",  "Growth deceleration across bookings and margin both hit the P&L at once"),
    ("Forward P/E",                "~21.3x", "≤13x",    "-8.3x",  "Market re-prices Uber as an AV-disruption casualty rather than an AV-platform winner"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<30}  {curr:>9}  {bear_v:>9}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the entire multi-year debate on Uber comes down to whether autonomous")
print(f"  vehicles need a demand-aggregation layer or can go direct to consumers. Every AV")
print(f"  operator building its own app (as Waymo and Tesla both have, to varying degrees) is a")
print(f"  bear signal; every AV operator choosing to distribute through Uber (as Waymo is ALSO")
print(f"  doing, at 250K paid rides/week) is a bull signal. Right now both are happening")
print(f"  simultaneously, which is exactly why this remains a genuine, unresolved question.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E non-GAAP EPS:       ${EPS_FY2026E:.2f}  (Q1 $0.72, +44% YoY, annualizing with continued growth)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (a reasonable floor for a profitable, double-digit-growth marketplace business)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} — near the stock's own 52-week low — the market is pricing real AV-")
print(f"  disruption anxiety despite Uber's own data showing AV trips on its platform growing 10x+.")
print(f"  The EPP floor sits only {abs(epp_gap_pct):.0f}% below spot, a narrow gap that says the stock is")
print(f"  already discounting a meaningful amount of that anxiety.")
print(f"  At a 19× reversion (a modest re-rating credit for the AV-platform evidence): ${EPS_FY2026E:.2f} × 19 = ${EPS_FY2026E*19:.0f}")
print(f"  ({(EPS_FY2026E*19/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: growth decelerates well below the current pace, modest re-rating)")
hr()
print(f"  Conservative FY2028E EPS:  ${CONS_EPS_2YR:.2f}  (~14.2% EPS CAGR — a real deceleration from the current 44% pace)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~21.3× → 17×; reflects continued AV-thesis uncertainty, not resolution)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (no dividend)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: this case assumes EPS growth decelerates sharply (44% → ~14%/yr) and the")
print(f"  multiple gets essentially no re-rating credit for the AV-platform evidence, and it still")
print(f"  clears {cons_annual:.1f}%/yr. Trading near its 52-week low with genuinely strong operating momentum")
print(f"  is an unusual combination — the market's AV anxiety is doing more work in the price than")
print(f"  the current data supports.")
print(f"  Breakeven at 17× requires FY2028E EPS ≥ ${CURRENT_PRICE / CONS_PE_2YR:.2f} — below this conservative estimate already.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.36
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range — near the low)")
print(f"  Drawdown from high:    -{(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.1f}%  (AV-disruption anxiety, despite bookings/EBITDA both accelerating)")
print(f"  Annual dividend:      none — capital returned via a $7B buyback authorization")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (elevated; AV-headline sensitivity keeps this a jumpy stock)")
print(f"  Beta vs S&P 500:      1.35  (consumer-discretionary-adjacent plus AV-narrative sensitivity)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (would meaningfully breach the current 52W low)")
print(f"  → Q2 print (Aug 5) is the immediate catalyst — watch AV trip growth disclosure specifically, not just bookings.")
print(f"  → Any AV operator publicly moving to a direct-to-consumer app would be the clearest bear signal available.")
print(f"  → WATCHLIST at current price  |  ACCUMULATE $60–66  |  BUY below $56  |  TRIM above $100")

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
print(f"  Uber is trading near its 52-week low while bookings grow 25%, EBITDA grows 33%, EPS")
print(f"  grows 44%, and AV trips on its own platform grow 10x. That combination — accelerating")
print(f"  operating momentum at a price reflecting the opposite. Ratio B (1.43x) keeps this at")
print(f"  WATCHLIST rather than BUY only because the AV-disruption downside case, while less likely")
print(f"  than the data currently suggests, would still be severe if it materialized.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q2 2026 results (Aug 5) — AV trip growth disclosure and gross bookings vs the ~$57.2B consensus")
print(f"  (2) Any AV operator (Waymo, Tesla, others) moving toward or away from Uber platform distribution")
print(f"  (3) Adjusted EBITDA margin trajectory — confirmation that operating leverage keeps compounding")
print(f"  (4) Uber One membership growth and advertising revenue — the underappreciated margin engines")
print(f"  (5) Regulatory developments around AV deployment in target cities")
print(f"  WATCHLIST at ${CURRENT_PRICE:.2f}  |  ACCUMULATE $60–66  |  BUY below $56  |  TRIM above $100")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  AV trip growth: {AV_TRIP_GROWTH_YOY_X}x+")
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
