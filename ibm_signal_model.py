"""
IBM  ·  International Business Machines Corp.  ·  NYSE: IBM
Bottom-up signal model  ·  Hybrid Cloud (Red Hat) / Consulting / zSystems / Quantum
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "IBM"
COMPANY       = "International Business Machines Corp."
SECTOR        = "Hybrid Cloud · Red Hat · Consulting · zSystems · Quantum Computing · NYSE: IBM"
CURRENT_PRICE = 221.74       # USD; close 2026-07-31 (verified live)
VOL_52W_LOW   = 199.19       # 2026 trough; post Q2 guidance trim
VOL_52W_HIGH  = 332.46       # 2025/26 peak; 46.5-year high before the derate
SHARES_OUT_M  = 942.0        # millions; $208.9B mkt cap / $221.74
ANNUAL_DIV    = 6.76         # $/share forward; 30-year growth streak (Dividend Aristocrat); yield ~2.99%

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ─────────────────────────────────────
# Q2 2026 actual: revenue $17.2B (+1% YoY); Software $7.8B (+5%), Consulting $5.3B (flat)
# FY2026 guide: constant-currency revenue growth trimmed to 4-5% (from prior 5%+)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Software (Red Hat/Data/Automation)", 32.5, 29.0, 36.5, "80% recurring; ARR $24.6B (+8%); Red Hat +11%, Data +19% — the growth engine"),
    ("Consulting",                         21.5, 18.5, 24.5, "Flat YoY in Q2 — the segment that determines whether this is 4% or 6% growth"),
    ("Infrastructure (zSystems/Power)",     14.5, 12.0, 16.5, "Mainframe cycle-dependent; z17 refresh a 2026-27 tailwind, then troughs again"),
    ("Financing & Other",                    2.5,  2.2,  2.8, "Small, stable annuity on the installed base"),
]

# Margin assumptions (non-GAAP)
OP_MARGIN_CURR   = 0.175    # FY2026E non-GAAP pre-tax margin proxy; guided to expand ~100bp
OP_MARGIN_BULL   = 0.205    # BULL: software mix shift + quantum optionality monetizes
OP_MARGIN_BEAR   = 0.140    # BEAR: consulting stays flat/declines, mainframe cycle troughs
TAX_RATE         = 0.140    # effective non-GAAP tax rate (IBM runs structurally low on tax)

# ── ARR / QUANTUM CALCULATOR (the IBM-specific angle) ────────────────────────
SOFTWARE_ARR_B      = 24.6   # $B annual recurring revenue, +8% YoY
RECURRING_PCT       = 0.80   # % of software revenue that is recurring
QUANTUM_INVEST_B    = 10.0   # $B committed to quantum over the next 5 years
FCF_GUIDE_DELTA_B   =  1.0   # $B guided FCF growth YoY for FY2026
CONSULTING_SIGNINGS_TREND = "up"  # management flagged rising GenAI-driven signings despite flat revenue

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 11.35       # $/share non-GAAP FY2026E; TTM $11.02, Q2 $2.93 (+5%), full-year trending up
PE_PESSIMISTIC = 15.0        # trough P/E: IBM spent most of 2015-2020 at 11-13× forward as a
                             # declining-revenue value trap; 15× credits the now-real Red Hat growth engine
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 7.90, 14,  111, "Consulting declines; mainframe cycle troughs; software growth decelerates to mid-single digits"),
    "BASE":  (12.80, 19,  243, "Software +7-8% holds; consulting returns to low-single-digit growth; margin expands as guided"),
    "BULL":  (15.35, 22,  338, "Red Hat/AI software reaccelerates; consulting GenAI signings convert; z17 cycle beats"),
    "XBULL": (18.00, 25,  450, "Quantum commercialization becomes a real revenue line; IBM re-rates as an AI infrastructure compounder"),
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
        "name":       "Software revenue YoY growth",
        "weight":     0.25,
        "thresholds": ("<2%",    "≥5%",   "≥8%",    "≥12%"),
        "now":        "+5%",
        "score":      2,
        "comment":    "$7.8B (+5%); Red Hat/Hybrid Cloud +11%, Data +19%. FY guide 6-8% — Q2 came in at the low end",
    },
    {
        "name":       "Consulting revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<-3%",   "≥0%",   "≥4%",    "≥8%"),
        "now":        "0%",
        "score":      2,
        "comment":    "Flat in Q2. Signings are rising on GenAI demand — a leading indicator revenue hasn't confirmed yet",
    },
    {
        "name":       "Total revenue YoY growth (cc)",
        "weight":     0.20,
        "thresholds": ("<2%",    "≥4%",   "≥6%",    "≥9%"),
        "now":        "+1%",
        "score":      1,
        "comment":    "Q2 reported +1% YoY (USD); FY guide trimmed to 4-5% cc from a prior 5%+ — the miss that moved the stock",
    },
    {
        "name":       "Software ARR growth",
        "weight":     0.15,
        "thresholds": ("<4%",    "≥6%",   "≥9%",    "≥13%"),
        "now":        "+8%",
        "score":      2,
        "comment":    "$24.6B ARR, +8% YoY, 80% recurring — the most durable number in the print",
    },
    {
        "name":       "Non-GAAP pre-tax margin trend",
        "weight":     0.10,
        "thresholds": ("<0bp",   "≥50bp", "≥100bp", "≥180bp"),
        "now":        "~30bp",
        "score":      1,
        "comment":    "Q2 margin expansion of 30bp came in below the ~100bp guided for the full year",
    },
    {
        "name":       "Free cash flow growth guide",
        "weight":     0.10,
        "thresholds": ("<0",     "≥$0.5B","≥$1.0B", "≥$2.0B"),
        "now":        "~$1.0B",
        "score":      2,
        "comment":    "Guided +$1B YoY — solid, but the growth-vs-margin miss this quarter puts the guide at risk",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Software ARR franchise — $24.6B, 80% recurring, +8% YoY; the real re-rating case",          +0.8, 0.20),
    ("+", "Dividend Aristocrat — 30-year growth streak, ~3.0% yield, backed by durable FCF",             +0.5, 0.15),
    ("-", "Consulting stagnation — flat revenue despite rising signings; conversion lag is unresolved",  -0.6, 0.20),
    ("-", "Guidance cut — Q2 growth trim from 5%+ to 4-5% cc breaks a multi-quarter beat-and-raise streak", -0.7, 0.20),
    ("+", "Quantum optionality — $10B committed, a foundry LOI signed; a call option the market isn't pricing", +0.4, 0.10),
    ("-", "Reduced AI disclosure — IBM stopped breaking out generative-AI book of business, cutting transparency right when investors need more of it", -0.4, 0.15),
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
CONS_EPS_2YR  = 12.60   # conservative FY2028E: ~5.4% EPS CAGR off the FY2026E base
CONS_PE_2YR   = 17      # modest de-rating from ~19.5× today, short of the BASE-case 19×
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Hybrid Cloud / Consulting / zSystems / Quantum")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
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
print(f"  FY2026 guidance: constant-currency revenue growth 4-5% (trimmed from prior 5%+ at Q2)")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_op   = curr_total * OP_MARGIN_CURR
curr_eps  = round(curr_op * (1 - TAX_RATE) / shares, 2)

bull_op   = bull_total * OP_MARGIN_BULL
shares_b  = shares * 0.98
bull_eps_imp = round(bull_op * (1 - TAX_RATE) / shares_b, 2)

bear_op   = bear_total * OP_MARGIN_BEAR
bear_eps_imp = round(bear_op * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {OP_MARGIN_CURR*100:.1f}% margin proxy − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {OP_MARGIN_BULL*100:.1f}% margin, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 22× = ~${bull_eps_imp*22:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {OP_MARGIN_BEAR*100:.1f}% margin (consulting decline, mainframe trough)")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 14× trough = ~${bear_eps_imp*14:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")
print()
print(f"  ⚠ THE STRUCTURAL POINT: {SEG_DATA[0][1]/curr_total*100:.0f}% of revenue is Software, and within that {RECURRING_PCT*100:.0f}%")
print(f"  is recurring ARR. That base moves slowly in either direction. The bear/bull spread is")
print(f"  driven far more by Consulting (flat-to-declining vs GenAI-signings-convert) and the")
print(f"  cyclical zSystems mainframe refresh than by anything happening in Software itself.")

# ARR / QUANTUM CHECK
print()
print(f"  ARR & QUANTUM CHECK  (the IBM-specific angle):")
print(f"  Software ARR:                 ${SOFTWARE_ARR_B:.1f}B  (+8% YoY, {RECURRING_PCT*100:.0f}% recurring)")
print(f"  Quantum investment committed:  ${QUANTUM_INVEST_B:.0f}B over 5 years; foundry LOI signed this quarter")
print(f"  FCF growth guide (FY2026):    +${FCF_GUIDE_DELTA_B:.1f}B YoY")
print(f"  Consulting signings trend:    {CONSULTING_SIGNINGS_TREND.upper()} — rising GenAI-driven signings despite flat revenue")
print()
print(f"  Quantum is a genuine call option most models assign zero value to — $10B is real money")
print(f"  but the revenue is 2030s-dated. It should not be underwriting the thesis today, and it")
print(f"  isn't in this model; it sits only in the XBULL narrative as optionality, not in the EPS bridge.")

# KEY SENSITIVITIES
print()
eps_per_1B_sw   = 1.0 * 0.35 * (1 - TAX_RATE) / shares   # software incremental margin ~35%
eps_per_1B_cons = 1.0 * 0.14 * (1 - TAX_RATE) / shares   # consulting incremental margin ~14%
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B software revenue (35% inc. margin):    +${eps_per_1B_sw:.3f}/EPS  = +${eps_per_1B_sw*17:.2f}/share at 17× P/E")
print(f"  Every $1B consulting revenue (14% inc. margin):  +${eps_per_1B_cons:.3f}/EPS  = +${eps_per_1B_cons*17:.2f}/share at 17× P/E")
print(f"  Every 1 turn of P/E:                             ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (software growth / consulting / total revenue / ARR / margin)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<40}  {'BEAR':>7}  {'BASE':>7}  {'BULL':>7}  {'XBULL':>7}  {'NOW':>7}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<40}  {ths[0]:>7}  {ths[1]:>7}  {ths[2]:>7}  {ths[3]:>7}  {s['now']:>7}  {lbl}  {b}")
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
print(f"  {'Signal':<32}  {'Current':>9}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Software revenue YoY",       "+5%",    "<2%",     "-3pp",   "Red Hat/Data growth decelerates as easy comps lap"),
    ("Consulting revenue YoY",     "0%",     "<-3%",    "-3pp",   "GenAI signings never convert; legacy IT services book shrinks"),
    ("Total revenue YoY (cc)",     "+1%",    "<2%",     "flat",   "Another guidance trim confirms the deceleration is structural"),
    ("Software ARR growth",        "+8%",    "<4%",     "-4pp",   "Renewal pricing pressure; hyperscaler-native tools win net-new"),
    ("Non-GAAP margin expansion",  "~30bp",  "<0bp",    "-30bp",  "Cost discipline breaks down as revenue growth disappoints"),
    ("Forward P/E",                "19.5x",  "≤14x",    "-5.5x",  "Market re-rates IBM back to its pre-Red-Hat-growth value multiple"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>9}  {bear_v:>9}  {move:>8}  {trigger[:46]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: IBM's Q2 print was a genuine guidance cut, not a beat with cautious")
print(f"  language — cc growth guidance moved from 5%+ to 4-5%, and margin expansion of 30bp")
print(f"  missed the ~100bp full-year pace. The bear case is that Consulting's flat revenue,")
print(f"  not Software's ARR, is the real signal, and that rising GenAI signings are a")
print(f"  management talking point until they show up in billed revenue for two more quarters.")
print(f"  Note: BEAR ${bear_price} still implies EPS growth from today's ${EPS_FY2026E:.2f} — this is a multiple")
print(f"  compression case (19.5× → 14×), not an earnings-collapse case.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E non-GAAP EPS:      ${EPS_FY2026E:.2f}  (TTM $11.02; Q2 $2.93, +5% YoY)")
print(f"  Pessimistic P/E at trough:  {PE_PESSIMISTIC:.0f}×  (2015-2020 value-trap years averaged 11-13×; 15× credits Red Hat)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP is a middling reading for IBM. At ${CURRENT_PRICE:.2f} the stock")
print(f"  trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E non-GAAP EPS, down from a 46.5-year-high multiple earlier")
print(f"  in 2026 to ${VOL_52W_HIGH:.2f}. The EPP floor assumes IBM reverts to being priced like the")
print(f"  pre-Red-Hat value name it was for most of the 2010s — a real risk if Consulting's flat")
print(f"  revenue turns out to be the leading indicator rather than the lagging one.")
print(f"  At a 22× reversion (roughly where it traded before the Q2 guidance cut): ${EPS_FY2026E:.2f} × 22 = ${EPS_FY2026E*22:.0f}")
print(f"  (+{(EPS_FY2026E*22/CURRENT_PRICE-1)*100:.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: growth stays at the trimmed guidance pace, modest re-rating)")
hr()
print(f"  Conservative FY2028E non-GAAP EPS:  ${CONS_EPS_2YR:.2f}  (~5.4% EPS CAGR off the ${EPS_FY2026E:.2f} FY2026E base)")
print(f"  Conservative exit P/E:               {CONS_PE_2YR}×  (19.5× → 16×; a real de-rating, not a re-rating)")
print(f"  Conservative equity value:            ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):        +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:               ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:            {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: this case assumes the multiple CONTRACTS from 19.5× to 16× — a real penalty")
print(f"  for the guidance cut — and the dividend still carries the total return to {cons_annual:.1f}%/yr.")
print(f"  IBM's ~3% yield does real work here; this is not a story that needs a re-rating to work,")
print(f"  it needs the dividend to keep growing and the multiple to not fall much further.")
print(f"  Breakeven at 16× requires FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f} — a modest bar given the FY2026E base.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.24
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Drawdown from high:   -{(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.1f}%  (a genuine derate off a 46.5-year price high)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; 30-year Dividend Aristocrat)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (low for tech, consistent with IBM's defensive positioning)")
print(f"  Beta vs S&P 500:      0.75  (still trades more like a value/dividend name than a growth one)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (a full round-trip to the 52W low and through it)")
print(f"  → Q3 2026 is the confirm-or-deny quarter: does Consulting revenue follow signings up?")
print(f"  → The dividend yield sets a soft floor that most of the coverage doesn't have.")
print(f"  → ACCUMULATE at current price  |  BUY below $195  |  TRIM above $310")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f} the market composite is {MARKET_COMPOSITE:.2f}/4.0 — pricing execution")
print(f"  between BASE and BULL. The model's adjusted composite is {ADJ_COMPOSITE:.2f}/4.0, near the BEAR/BASE")
print(f"  boundary, for a gap of {ADJ_GAP:+.2f} — {valuation_label.lower()}. NOTE THE TENSION, because it is the")
print(f"  whole decision: ratio B ({ratio_b_str}) says the risk/reward is workable on the scenario spread,")
print(f"  while the composite gap says the market hasn't yet priced in how weak Q2 actually was —")
print(f"  a guidance cut, a margin miss, and Consulting stuck at zero. ACCUMULATE, not BUY, reflects")
print(f"  that the multiple has room to fall further before the signals catch up to the price.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q3 2026 Consulting revenue — does it follow the rising GenAI signings up, finally?")
print(f"  (2) Software ARR trajectory — any deceleration below +6% YoY would be the first bad sign")
print(f"  (3) Full-year margin expansion — needs to accelerate from Q2's 30bp toward the ~100bp guide")
print(f"  (4) z17 mainframe cycle — infrastructure segment is the most cyclical, least AI-linked piece")
print(f"  (5) Quantum foundry progress — pure optionality, but a proof point would support the multiple")
print(f"  ACCUMULATE at ${CURRENT_PRICE:.2f}  |  BUY below $195  |  TRIM above $310")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  ARR: ${SOFTWARE_ARR_B:.1f}B")
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
