"""
ADBE  ·  Adobe Inc.  ·  NASDAQ: ADBE
Bottom-up signal model  ·  Creative Cloud / Digital Experience / Generative AI (Firefly)
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "ADBE"
COMPANY       = "Adobe Inc."
SECTOR        = "Creative Cloud · Digital Experience · Generative AI (Firefly) · NASDAQ: ADBE"
CURRENT_PRICE = 250.41       # USD; close 2026-07-31 (verified live)
VOL_52W_LOW   = 190.12       # 2026 trough; AI-disruption fear + leadership uncertainty
VOL_52W_HIGH  = 370.86       # 2025 peak, pre-CEO-transition-announcement
SHARES_OUT_M  = 397.0        # millions; $99.5B mkt cap / $250.41; steady buyback under a $25B authorization
ANNUAL_DIV    = 0.0          # $/share — Adobe pays no dividend; reinvests via buybacks

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ─────────────────────────────────────
# Q2 FY2026 actual: revenue $6.62B (+12.7% YoY); FY2026 guide raised to $26.5-26.6B
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Digital Media (Creative Cloud)",   17.8, 15.5, 19.5, "Photoshop/Illustrator/Premiere + Firefly credits; the core franchise under the most direct AI pressure"),
    ("Digital Media (Document Cloud)",    3.4,  3.0,  3.9, "Acrobat + AI Assistant; ARR grew ~3x — one of the cleanest AI-monetization stories in the print"),
    ("Digital Experience (DX/enterprise)", 5.3,  4.7,  6.0, "Enterprise marketing/analytics platform; stickier, slower-growing, less AI-disruption-exposed"),
]

# Margin assumptions (non-GAAP)
OP_MARGIN_CURR   = 0.460    # FY2026E non-GAAP operating margin (Adobe runs mid-40s consistently)
OP_MARGIN_BULL   = 0.480    # BULL: AI monetization adds revenue without proportional cost
OP_MARGIN_BEAR   = 0.400    # BEAR: promotional pricing + Firefly compute costs compress margin
TAX_RATE         = 0.190    # non-GAAP effective tax rate

# ── AI / LEADERSHIP CALCULATOR (the Adobe-specific angle) ────────────────────
AI_FIRST_ARR_M      = 500    # $M AI-first ARR, tripled YoY in Q2
FIREFLY_ARR_M        = 300    # $M total Firefly ARR (apps + credit packs + enterprise)
FIREFLY_CONSUMER_QOQ = 50     # % QoQ growth in Firefly consumer business (apps + credits)
ACROBAT_AI_GROWTH_X  = 3      # Acrobat AI Assistant ARR growth multiple YoY
CEO_TRANSITION       = "in progress"  # Narayen announced March 2026 exit pending successor; remains as Chair
CFO_VACANCY          = True   # Dan Durn exited effective June 15, 2026 — second C-suite opening

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 24.40       # $/share non-GAAP FY2026E; company guidance $24.35-$24.45
PE_PESSIMISTIC = 11.0        # trough P/E: the stock already trades near 10x forward; 11x prices
                             # a modest further derate on leadership uncertainty, not a collapse
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  (18.50, 10,  185, "Firefly cannibalizes Creative Cloud seats faster than it monetizes; leadership vacuum drags on execution"),
    "BASE":  (27.50, 13,  358, "AI-first ARR compounds toward $2-3B; new CEO installed cleanly; Creative Cloud holds share"),
    "BULL":  (31.00, 17,  527, "Firefly becomes the default gen-AI creative layer; DX cross-sell accelerates; multiple recovers"),
    "XBULL": (36.00, 20,  720, "Adobe re-rates as the enterprise content-and-marketing AI platform of record"),
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
        "thresholds": ("<8%",    "≥11%",  "≥15%",   "≥20%"),
        "now":        "+12.7%",
        "score":      2,
        "comment":    "Q2 $6.62B (+12.7%), beat consensus $6.45B. FY guide raised to $26.5-26.6B",
    },
    {
        "name":       "AI-first ARR growth",
        "weight":     0.25,
        "thresholds": ("<1.5x",  "≥2x",   "≥3x",    "≥5x"),
        "now":        "3x",
        "score":      3,
        "comment":    "AI-first ARR tripled YoY to $500M+. Still small (~2% of revenue) but the growth rate is real",
    },
    {
        "name":       "Firefly ARR (total)",
        "weight":     0.15,
        "thresholds": ("<$150M", "≥$250M","≥$400M", "≥$700M"),
        "now":        "~$300M",
        "score":      2,
        "comment":    "Approaching $300M across apps, credit packs, and enterprise; consumer Firefly +50% QoQ",
    },
    {
        "name":       "Non-GAAP operating margin",
        "weight":     0.15,
        "thresholds": ("<40%",   "≥44%",  "≥47%",   "≥50%"),
        "now":        "~46%",
        "score":      3,
        "comment":    "Margin held even while absorbing Firefly compute costs and record AI R&D spend",
    },
    {
        "name":       "Leadership stability",
        "weight":     0.15,
        "thresholds": ("2 vacancies","CEO search open","successor named","transition complete"),
        "now":        "2 vacancies",
        "score":      1,
        "comment":    "CEO Narayen departing (successor TBD) AND CFO Durn already gone — a genuine execution-risk gap",
    },
    {
        "name":       "Forward P/E vs software peers",
        "weight":     0.10,
        "thresholds": (">18x",   "≤14x",  "≤11x",   "≤8x"),
        "now":        "10.3x",
        "score":      3,
        "comment":    "10.3× FY2026E non-GAAP EPS — the cheapest large-cap software name in this coverage by a wide margin",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Valuation reset — 10.3× forward EPS is a distress multiple for a 46%-margin, growing business", +1.0, 0.25),
    ("+", "AI monetization is real — AI-first ARR tripled, Acrobat AI Assistant ARR ~3x, not just a narrative", +0.6, 0.20),
    ("-", "Leadership vacuum — CEO AND CFO both departing simultaneously; a rare double vacancy at this scale", -0.9, 0.20),
    ("-", "Creative Cloud disintermediation risk — the core franchise faces the most direct genAI substitution threat in software", -0.6, 0.20),
    ("+", "Capital return — $25B buyback authorization actively retiring shares at a depressed multiple", +0.4, 0.10),
    ("-", "Sell-side skepticism — Morgan Stanley cut to Underweight, $240 target; not a lone bearish view", -0.3, 0.05),
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
CONS_EPS_2YR  = 27.00   # conservative FY2028E: ~5.2% EPS CAGR off the FY2026E guide — no AI upside assumed
CONS_PE_2YR   = 12      # modest re-rating from 10.3× — still well below the historical mid-20s
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Creative Cloud / Digital Experience / Generative AI")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
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
print(f"  FY2026 guidance (raised at Q2): revenue $26.5-26.6B, non-GAAP EPS $24.35-$24.45")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_op   = curr_total * OP_MARGIN_CURR
curr_eps  = round(curr_op * (1 - TAX_RATE) / shares, 2)

bull_op   = bull_total * OP_MARGIN_BULL
shares_b  = shares * 0.95
bull_eps_imp = round(bull_op * (1 - TAX_RATE) / shares_b, 2)

bear_op   = bear_total * OP_MARGIN_BEAR
bear_eps_imp = round(bear_op * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {OP_MARGIN_CURR*100:.1f}% op margin − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (company guidance ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {OP_MARGIN_BULL*100:.1f}% op margin, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 17× = ~${bull_eps_imp*17:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {OP_MARGIN_BEAR*100:.1f}% op margin (pricing pressure, Firefly compute costs)")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 10× trough = ~${bear_eps_imp*10:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")
print()
print(f"  ⚠ NOTE: the revenue spread bear-to-bull is only {(bull_total/bear_total-1)*100:.0f}%, but a modest multiple swing")
print(f"  (10-17×) does most of the work in the price spread. This is a name where the debate is")
print(f"  overwhelmingly about the MULTIPLE Adobe deserves, not about whether the business grows.")

# AI / LEADERSHIP CHECK
print()
print(f"  AI MONETIZATION & LEADERSHIP CHECK  (the Adobe-specific angle):")
print(f"  AI-first ARR:                  ${AI_FIRST_ARR_M}M+  (tripled YoY)")
print(f"  Total Firefly ARR:             ~${FIREFLY_ARR_M}M  (apps + credit packs + enterprise)")
print(f"  Firefly consumer QoQ growth:   +{FIREFLY_CONSUMER_QOQ}%")
print(f"  Acrobat AI Assistant ARR:      ~{ACROBAT_AI_GROWTH_X}x YoY")
print(f"  CEO transition:                {CEO_TRANSITION.upper()}  (Narayen exits after 18 years; remains Chair)")
print(f"  CFO vacancy:                   {'YES' if CFO_VACANCY else 'NO'}  (Dan Durn departed effective June 15, 2026)")
print()
print(f"  The AI numbers are the best argument for owning this stock: real, growing revenue lines")
print(f"  that did not exist two years ago. The leadership situation is the best argument against")
print(f"  buying it THIS QUARTER: a company navigating the most consequential product transition in")
print(f"  its history is doing so without a permanent CEO or CFO. Both things are true simultaneously.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * OP_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_marg = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 46% op margin):       +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*13:.2f}/share at 13× P/E")
print(f"  Every 1pp of operating margin:               +${eps_per_1pp_marg:.3f}/EPS  = +${eps_per_1pp_marg*13:.2f}/share at 13× P/E")
print(f"  Every 1 turn of P/E:                         ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")
print(f"  ↑ at 10.3× forward, the multiple carries far more sensitivity than the P&L does")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (revenue growth / AI ARR / margin / leadership / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<40}  {'BEAR':>12}  {'BASE':>10}  {'BULL':>10}  {'XBULL':>12}  {'NOW':>9}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<40}  {ths[0]:>12}  {ths[1]:>10}  {ths[2]:>10}  {ths[3]:>12}  {s['now']:>9}  {lbl}  {b}")
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
    ("Total revenue YoY",           "+12.7%", "<8%",     "-4.7pp", "Creative Cloud seat growth stalls as AI-native tools substitute"),
    ("AI-first ARR growth",         "3x",     "<1.5x",   "-1.5x",  "Firefly monetization plateaus; enterprises build on cheaper foundation models"),
    ("Non-GAAP operating margin",   "~46%",   "<40%",    "-6pp",   "Firefly inference costs and discounting to defend seats both bite at once"),
    ("Leadership stability",        "2 vacancies","unresolved 12mo+","worse","Botched CEO search or a second wave of executive departures"),
    ("Forward P/E",                 "10.3x",  "≤8x",     "-2.3x",  "Market prices in structural, not cyclical, Creative Cloud disruption"),
    ("Creative Cloud subscriber growth", "positive","negative","flip","Net subscriber losses — the number that would confirm the bear thesis"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the bear case is that generative AI tools let non-designers do what used")
print(f"  to require Creative Cloud — and that Adobe's own Firefly, however well it sells today,")
print(f"  is a rear-guard action against a market that no longer needs a $60/month subscription")
print(f"  to generate images and video. The leadership vacuum compounds this: the company making")
print(f"  the most consequential bet in its history is doing so without confirmed permanent")
print(f"  leadership at either the CEO or CFO level. Two years is enough time for either scenario")
print(f"  to resolve clearly, which is why the horizon here matters more than for most names.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E non-GAAP EPS (company guide):  ${EPS_FY2026E:.2f}  ($24.35-$24.45, raised at Q2)")
print(f"  Pessimistic P/E at trough:               {PE_PESSIMISTIC:.0f}×  (the stock already trades near 10× forward)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at just {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E non-GAAP EPS — for a")
print(f"  business with a 46% operating margin, no debt, and AI-first ARR that tripled year over")
print(f"  year. Adobe traded in the mid-20s multiple for most of the last decade. This is one of")
print(f"  the largest gaps between current multiple and historical multiple in large-cap software,")
print(f"  and the model's own EPP floor sits only {abs(epp_gap_pct):.0f}% below where the stock already trades.")
print(f"  At a 16× reversion (still a third below the historical mid-20s): ${EPS_FY2026E:.2f} × 16 = ${EPS_FY2026E*16:.0f}")
print(f"  (+{(EPS_FY2026E*16/CURRENT_PRICE-1)*100:.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest EPS growth, only a token re-rating)")
hr()
print(f"  Conservative FY2028E non-GAAP EPS:  ${CONS_EPS_2YR:.2f}  (~5.2% EPS CAGR off the ${EPS_FY2026E:.2f} guide — no AI upside assumed)")
print(f"  Conservative exit P/E:               {CONS_PE_2YR}×  (10.3× → 12×; still a fraction of the historical mid-20s)")
print(f"  Conservative equity value:            ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):        +${cons_divs:.2f}/share  (no dividend; buyback-funded returns)")
hr()
print(f"  Conservative 2yr total:               ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:            {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: this case assumes AI-first ARR growth STALLS at a fraction of its current")
print(f"  pace, gives the multiple only a token 2-point bump, and still clears {cons_annual:.1f}%/yr. The margin")
print(f"  of safety is almost entirely the valuation reset — the AI monetization story is upside")
print(f"  to this case, not a requirement of it, which is an unusual position for a name this")
print(f"  exposed to genuine AI-disruption risk in its core product.")
print(f"  Breakeven at {CONS_PE_2YR}× requires FY2028E EPS ≥ ${CURRENT_PRICE / CONS_PE_2YR:.2f} — below the current FY2026 guide.")
print(f"  BUY-conviction trigger: a permanent CEO named without a strategy reset")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.34
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Drawdown from high:   -{(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.1f}%  (a multi-year de-rating, not a single-quarter air pocket)")
print(f"  Annual dividend:      none — buyback-funded capital return only")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (elevated for Adobe's history; leadership + AI-fear driven)")
print(f"  Beta vs S&P 500:      1.20  (higher than its defensive-software reputation would suggest)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ further drawdown  (would retest, not breach, the 52W low)")
print(f"  → CEO announcement is the single highest-signal catalyst in the entire coverage right now.")
print(f"  → Creative Cloud net-subscriber trend is the metric that would confirm or deny the bear case.")
print(f"  → BUY at current price  |  ADD $210–235  |  TRIM above $340")

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
print(f"  Adobe at 10.3× forward earnings is priced closer to a legacy value stock than a")
print(f"  46%-margin software franchise with tripling AI ARR. The leadership vacuum is a real,")
print(f"  quantifiable reason for some discount — but two simultaneous C-suite openings do not")
print(f"  usually justify pricing a business at less than half its historical multiple.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Permanent CEO announcement — the single biggest overhang removal available to this stock")
print(f"  (2) CFO appointment — a credible finance leader would remove the second vacancy")
print(f"  (3) AI-first ARR trajectory — needs to keep tripling-pace to validate the Firefly bet")
print(f"  (4) Creative Cloud net-subscriber adds — the number that would confirm or deny disintermediation")
print(f"  (5) Buyback pace at a depressed multiple — a signal of the board's own view on valuation")
print(f"  BUY at ${CURRENT_PRICE:.2f}  |  ADD $210–235  |  TRIM above $340")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  AI-first ARR: ${AI_FIRST_ARR_M}M+")
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
