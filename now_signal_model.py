"""
NOW  ·  ServiceNow, Inc.  ·  NYSE: NOW
Bottom-up signal model  ·  Enterprise SaaS / Workflow Automation / Agentic AI Platform
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "NOW"
COMPANY       = "ServiceNow, Inc."
SECTOR        = "Enterprise SaaS · Workflow Automation · Agentic AI Platform · NYSE: NOW"
CURRENT_PRICE = 111.23       # USD; close 2026-07-31 (verified live); post 5-for-1 split
VOL_52W_LOW   =  81.24       # 2026 trough; agentic-AI disruption fear
VOL_52W_HIGH  = 196.40       # 2025 peak (split-adjusted)
SHARES_OUT_M  = 1_030.0      # millions; post 5-for-1 split; $115.0B mkt cap / $111.23
ANNUAL_DIV    = 0.0          # no dividend; cash goes to R&D and buyback

# ── SEGMENT REVENUE BRIDGE ($B) ──────────────────────────────────────────────
# Current column = FY2026E. Bear/Bull columns = the FY2028E revenue level on each path.
# FY2026 guidance: subscription revenue $15.77B (+21% YoY)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("IT Workflows (ITSM/ITOM/SecOps)",  6.6,  8.0,  9.8, "The core franchise; system of record for enterprise IT; ~98% renewal rate"),
    ("Customer & Industry Workflows",    3.5,  4.3,  5.6, "CSM + telco/banking/public-sector verticals; the fastest-growing land motion"),
    ("Creator / Platform / AI",          3.3,  4.2,  5.4, "App Engine, Now Assist, AI Control Tower — where the $1B+ AI ACV is booked"),
    ("Employee Workflows (HR)",          2.4,  2.9,  3.7, "HRSD + Workplace; steady 20% grower; expands seat count per logo"),
    ("Professional services & other",    0.6,  0.7,  0.8, "Deliberately kept small and partner-led; a margin choice, not a business"),
]

# Margin assumptions (non-GAAP)
OP_MARGIN_CURR   = 0.305    # FY2026E: Q2 29.5% actual, Q3 guided 31%
OP_MARGIN_BULL   = 0.360    # BULL: platform leverage exceeds AI inference cost
OP_MARGIN_BEAR   = 0.270    # BEAR: pricing pressure + inference COGS compress the model
INTEREST_INC_B   = 0.4      # $B net interest income on the cash pile
TAX_RATE         = 0.230    # non-GAAP effective rate

# ── AI TRACTION (the ServiceNow-specific calculator) ─────────────────────────
AI_ACV_B            = 1.0    # $B AI annual contract value — crossed $1B in Q2 2026
SUB_REV_Q2_M        = 3877   # $M Q2 2026 subscription revenue (+24.5% YoY, +23% cc)
SUB_REV_FY26_GUIDE  = 15.77  # $B FY2026 subscription revenue guidance (+21%)
OP_MARGIN_Q2        = 0.295  # Q2 2026 non-GAAP operating margin — 3pp above guidance
CONTROL_TOWER_LOGOS = 500    # AI Control Tower customers in the first six months
AGENTIC_GROWTH_X    = 9      # agentic AI deployments up 9× in nine months

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 4.00        # FY2026E non-GAAP EPS, post-split consensus (2025 actual $3.51)
PE_PESSIMISTIC = 24.0        # trough P/E: NOW has never traded below ~35× forward; 24× prices
                             # the agentic-AI disruption fear as if it were already happening
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 4.20, 18,   76, "Agentic AI compresses seat pricing; NRR below 110%; federal reverses; SaaS de-rating completes"),
    "BASE":  ( 6.30, 28,  176, "20% subscription CAGR holds; AI ACV $2.5B+; op margin 33%; multiple stabilises at 28×"),
    "BULL":  ( 7.25, 38,  276, "AI Control Tower becomes the enterprise agent-orchestration standard; ACV $5B; margin 36%"),
    "XBULL": ( 8.80, 46,  405, "ServiceNow = the enterprise AI operating system; consumption pricing opens a second S-curve"),
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
        "name":       "Subscription revenue YoY growth (cc)",
        "weight":     0.25,
        "thresholds": ("<14%",   "≥18%",   "≥23%",   "≥28%"),
        "now":        "+23%",
        "score":      3,
        "comment":    "Q2 subscription revenue $3,877M (+24.5% reported, +23% cc) — 1.5pp above guidance. FY raised to $15.77B",
    },
    {
        "name":       "AI (Now Assist) annual contract value",
        "weight":     0.20,
        "thresholds": ("<$0.4B", "≥$0.8B", "≥$2.0B", "≥$4.0B"),
        "now":        "$1.0B",
        "score":      2,
        "comment":    "Crossed $1B in Q2. Real money, but ~6% of subscription revenue — not yet the growth engine the bulls need",
    },
    {
        "name":       "Non-GAAP operating margin",
        "weight":     0.20,
        "thresholds": ("<26%",   "≥29%",   "≥33%",   "≥37%"),
        "now":        "29.5%",
        "score":      2,
        "comment":    "Q2 29.5% — 3pp ABOVE guidance; Q3 guided to 31%. Beating on margin while investing heavily in AI",
    },
    {
        "name":       "cRPO growth (cc)",
        "weight":     0.15,
        "thresholds": ("<14%",   "≥18%",   "≥22%",   "≥27%"),
        "now":        "+19%",
        "score":      2,
        "comment":    "The soft line in an otherwise clean print. A $35M FX headwind and Q2 federal pull-forward both hit Q3 cRPO",
    },
    {
        "name":       "EV/NTM revenue vs 5-yr avg (~14×)",
        "weight":     0.10,
        "thresholds": (">16x",   "≤11x",   "≤8x",    "≤6x"),
        "now":        "7.1x",
        "score":      3,
        "comment":    "$115B EV on ~$16.3B revenue. Half the multiple NOW carried for five years, on faster AI-era growth",
    },
    {
        "name":       "Customers with >$5M ACV",
        "weight":     0.10,
        "thresholds": ("<80",    "≥110",   "≥150",   "≥200"),
        "now":        "~130",
        "score":      2,
        "comment":    "Large-deal motion intact; US federal a standout. Expansion within logos still outruns new-logo adds",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Platform lock-in — one data model across IT/HR/CS; ~98% renewal rate; 15-yr customer lives", +0.8, 0.20),
    ("+", "Valuation reset — 7.1× EV/NTM revenue vs a ~14× 5-yr average; 43% below the split-adj high",  +0.8, 0.20),
    ("-", "Agentic-AI seat risk — the market's core fear: AI agents replace the licensed seats NOW sells", -0.9, 0.20),
    ("+", "AI is landing, not theoretical — $1B ACV, agentic deploys 9× in 9 months, 500 Control Tower logos", +0.7, 0.15),
    ("-", "US federal concentration — a genuine driver, but Q2 pulled on-prem revenue forward from Q3",  -0.5, 0.15),
    ("-", "AI inference COGS — a structural drag on the 30%+ operating margin as usage scales",          -0.4, 0.10),
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
CONS_EPS_2YR  = 5.90    # conservative FY2028E: ~21% EPS CAGR (below the revenue growth rate)
CONS_PE_2YR   = 26      # multiple stays near today's 27.8× — no re-rating credit at all
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Enterprise SaaS / Workflow / Agentic AI")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  FY2028E under BEAR / BULL paths)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<34}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<34}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<34}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  FY2026 guidance: subscription revenue ${SUB_REV_FY26_GUIDE:.2f}B (+21% YoY), raised at Q2")
print(f"  Implied 2-yr revenue CAGR:   BEAR {((bear_total/curr_total)**0.5-1)*100:>4.1f}%   BULL {((bull_total/curr_total)**0.5-1)*100:>4.1f}%")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_op   = curr_total * OP_MARGIN_CURR
curr_eps  = round((curr_op + INTEREST_INC_B) * (1 - TAX_RATE) / shares, 2)

bull_op   = bull_total * OP_MARGIN_BULL
shares_b  = shares * 0.99
bull_eps_imp = round((bull_op + INTEREST_INC_B * 1.3) * (1 - TAX_RATE) / shares_b, 2)

bear_op   = bear_total * OP_MARGIN_BEAR
bear_eps_imp = round((bear_op + INTEREST_INC_B * 0.8) * (1 - TAX_RATE) / (shares * 1.02), 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {OP_MARGIN_CURR*100:.1f}% op margin + ${INTEREST_INC_B:.1f}B interest income")
print(f"  − {TAX_RATE*100:.1f}% tax  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (consensus ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B FY2028E rev × {OP_MARGIN_BULL*100:.1f}% op margin")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 38× = ~${bull_eps_imp*38:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B FY2028E rev × {OP_MARGIN_BEAR*100:.1f}% op margin (pricing + inference COGS)")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 18× = ~${bear_eps_imp*18:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")
print()
print(f"  ⚠ READ THE BEAR COLUMN CAREFULLY: even in the BEAR case ServiceNow still GROWS")
print(f"  revenue from ${curr_total:.1f}B to ${bear_total:.1f}B ({((bear_total/curr_total)**0.5-1)*100:.0f}%/yr) and earns ${bear_eps_imp:.2f}/share. The bear case")
print(f"  is not a shrinking company — it is a company that keeps compounding while the")
print(f"  market pays 18× instead of 28× for it. That is what a ${bear_price} print requires.")

# ─── AI TRACTION CHECK ───────────────────────────────────────────────────────
print()
print(f"  AI TRACTION CHECK  (the axis the whole valuation now turns on):")
print(f"  AI annual contract value:        ${AI_ACV_B:.1f}B  (crossed $1B in Q2 2026)")
print(f"  ...as % of subscription revenue:  {AI_ACV_B/SUB_REV_FY26_GUIDE*100:.1f}%  — meaningful, not yet dominant")
print(f"  Agentic AI deployments:          {AGENTIC_GROWTH_X}× growth in nine months")
print(f"  AI Control Tower customers:      {CONTROL_TOWER_LOGOS}+ in the first six months")
print(f"  Q2 operating margin:             {OP_MARGIN_Q2*100:.1f}%  ({(OP_MARGIN_Q2-0.265)*100:.0f}pp above guidance) — AI investment is not")
print(f"                                   breaking the margin structure, which was the fear")
print()
print(f"  THE CENTRAL IRONY: the market de-rated ServiceNow from ~14× to {7.1:.1f}× revenue on the")
print(f"  thesis that agentic AI destroys per-seat SaaS. ServiceNow then booked ${AI_ACV_B:.1f}B of ACV")
print(f"  SELLING agentic AI. If AI is an existential threat to this business, the company's")
print(f"  own AI revenue line is a strange place for it to be showing up.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * 0.80 * (1 - TAX_RATE) / shares   # ~80% incremental margin on subscription
eps_per_1pp_mar = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B subscription revenue (80% inc.):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*28:.2f}/share at 28× P/E")
print(f"  Every 1pp of operating margin:              +${eps_per_1pp_mar:.3f}/EPS  = +${eps_per_1pp_mar*28:.2f}/share at 28× P/E")
print(f"  Every 1 turn of P/E:                        ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")
print(f"  Every 1pp of NRR (net revenue retention):   ~+${SUB_REV_FY26_GUIDE*0.01*0.8*(1-TAX_RATE)/shares:.3f}/EPS compounding — the highest-leverage metric NOW has")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (subscription growth / AI ACV / margin / backlog / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<44}  {'BEAR':>7}  {'BASE':>7}  {'BULL':>7}  {'XBULL':>7}  {'NOW':>7}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<44}  {ths[0]:>7}  {ths[1]:>7}  {ths[2]:>7}  {ths[3]:>7}  {s['now']:>7}  {lbl}  {b}")
    print(f"    {s['comment']}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15%/yr hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:92]:<92}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<34}  {'Current':>9}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Subscription revenue YoY (cc)", "+23%",   "<14%",    "−9pp",   "Agentic AI compresses seats faster than ACV grows"),
    ("AI ACV",                        "$1.0B",  "<$0.4B",  "−$0.6B", "Now Assist upsell stalls; customers build on OpenAI"),
    ("Non-GAAP operating margin",     "29.5%",  "<26%",    "−3.5pp", "Inference COGS + discounting to defend renewals"),
    ("cRPO growth (cc)",              "+19%",   "<14%",    "−5pp",   "Federal reverses; pull-forward unwinds; FX persists"),
    ("EV/NTM revenue",                "7.1x",   "≤4x",     "−3x",    "SaaS repriced permanently as a low-growth utility"),
    ("Customers >$5M ACV",            "~130",   "<80",     "−50",    "Large logos consolidate onto a competing AI platform"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<34}  {curr:>9}  {bear_v:>9}  {move:>8}  {trigger[:46]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the bear case is a single thesis — that agentic AI collapses the")
print(f"  per-seat licensing model ServiceNow sells. If AI agents do the work instead of")
print(f"  licensed humans, seat counts fall even as the work grows, and NRR breaks below 110%.")
print(f"  This is a genuine structural risk and it deserves the weight the model gives it.")
print(f"  What the model disputes is the TIMING: NOW's own AI ACV crossed ${AI_ACV_B:.1f}B this quarter")
print(f"  while subscription revenue grew +23% cc. The disruption is not visible in the")
print(f"  numbers yet, and the price already reflects several years of it.")
print(f"  Note: BEAR ${bear_price} is {(1-bear_price/VOL_52W_LOW)*100:.0f}% below the 52W low of ${VOL_52W_LOW:.2f} — a real path, not a floor.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E non-GAAP EPS:       ${EPS_FY2026E:.2f}  (post-split; 2025 actual $3.51; 2027E ~$5.00)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (NOW has never traded below ~35× forward in its public life)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP is remarkable for a business compounding subscription")
print(f"  revenue at 23% with a 30% operating margin. At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}×")
print(f"  FY2026E and {CURRENT_PRICE/5.00:.1f}× FY2027E non-GAAP EPS — multiples ServiceNow last saw when it")
print(f"  was a fraction of its current size. And note what the EPP floor is built on: a 24×")
print(f"  pessimistic multiple that is itself far below anything this stock has ever traded at.")
print(f"  The floor assumption is doing conservative work, not flattering work.")
print(f"  EPP path: FY2028E EPS ~$5.90 × {PE_PESSIMISTIC:.0f}× = ${5.90*PE_PESSIMISTIC:.0f} floor by 2028 (EPP compounding ~21%/yr).")
print(f"  At a 35× 'never-below' multiple: ${EPS_FY2026E:.2f} × 35 = ${EPS_FY2026E*35:.0f}  (+{(EPS_FY2026E*35/CURRENT_PRICE-1)*100:.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: growth decelerates, multiple gets NO re-rating credit)")
hr()
print(f"  Conservative FY2028E non-GAAP EPS:  ${CONS_EPS_2YR:.2f}  (~21% EPS CAGR — below the current revenue growth rate)")
print(f"  Conservative exit P/E:               {CONS_PE_2YR}×  (below today's {CURRENT_PRICE/EPS_FY2026E:.1f}× — the multiple contracts further)")
print(f"  Conservative equity value:            ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):        +${cons_divs:.2f}/share  (no dividend; all cash reinvested + buyback)")
hr()
print(f"  Conservative 2yr total:               ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:            {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: this case assumes growth SLOWS and the multiple CONTRACTS from {CURRENT_PRICE/EPS_FY2026E:.1f}× to {CONS_PE_2YR}×,")
print(f"  and still returns {cons_annual:.1f}%/yr. That is what happens when a 20%+ compounder is")
print(f"  repriced to 28× forward earnings: the growth alone carries the return, and you")
print(f"  need no help at all from sentiment.")
print(f"  Breakeven at {CONS_PE_2YR}× requires FY2028E EPS ≥ ${CURRENT_PRICE / CONS_PE_2YR:.2f} — barely above the FY2027E consensus.")
print(f"  MAX-SIZE trigger: below ${EPP:.0f} (the EPP floor), where you are paid to take the AI-disruption risk")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.42
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Drawdown from high:   −{(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.1f}%  (split-adjusted; a multiple event, not an earnings event)")
print(f"  Annual dividend:      none  —  cash funds R&D and buyback")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (high-multiple SaaS beta; earnings gaps of ±10% are routine)")
print(f"  Beta vs S&P 500:      1.30  (long-duration cash flows; rate- and AI-narrative sensitive)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (well within one year's normal range — do not dismiss it)")
print(f"  → The stock fell 6.5% on a Q2 print that beat on every line except cRPO. Sentiment,")
print(f"    not fundamentals, is setting the price — which cuts both ways.")
print(f"  → NRR and seat-count disclosure are the metrics that resolve the agentic-AI debate.")
print(f"  → BUY at current price  |  MAX SIZE below ${EPP:.0f}  |  TRIM above $250")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f} the market composite is {MARKET_COMPOSITE:.2f}/4.0 — the market is")
print(f"  pricing execution BELOW the BASE case. The model's adjusted composite is {ADJ_COMPOSITE:.2f}/4.0,")
print(f"  for a gap of {ADJ_GAP:+.2f} — the stock is {valuation_label.lower()}.")
print(f"  In plain terms: ServiceNow raised full-year guidance, beat on subscription revenue,")
print(f"  beat on margin by 3pp, and crossed $1B in AI ACV — and the market is paying for a")
print(f"  company doing worse than its base case. The asymmetry ({ratio_b_str}) is the widest in the")
print(f"  software coverage. The risk is real and named; the price for taking it is generous.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Net revenue retention — the single number that settles the agentic-AI seat debate")
print(f"  (2) cRPO growth in Q3 — the pull-forward washes out; a clean +20% cc restores the story")
print(f"  (3) AI ACV trajectory — $1B → $2B is the proof point the BULL case is built on")
print(f"  (4) US federal renewal cycle — the biggest single driver, and the biggest single risk")
print(f"  (5) Operating margin vs inference COGS — can 33%+ survive scaled AI usage?")
print(f"  BUY at ${CURRENT_PRICE:.2f}  |  MAX SIZE below ${EPP:.0f}  |  TRIM above $250")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  AI ACV: ${AI_ACV_B:.1f}B")
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
