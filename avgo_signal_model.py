"""
AVGO  ·  Broadcom Inc.  ·  NASDAQ: AVGO
Bottom-up signal model  ·  AI Semiconductors / Custom XPU / Networking / VMware Infrastructure Software
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "AVGO"
COMPANY       = "Broadcom Inc."
SECTOR        = "AI Semiconductors · Custom XPU · Networking · VMware Infrastructure Software · NASDAQ: AVGO"
CURRENT_PRICE = 390.74      # USD; close 2026-08-03
VOL_52W_LOW   = 281.61      # 2025/26 trough
VOL_52W_HIGH  = 495.00      # 2026 AI-semiconductor-cycle peak
SHARES_OUT_M  = 4_900.0     # millions diluted (non-GAAP); ~4.76B basic shares outstanding
ANNUAL_DIV    = 2.36        # $/share; quarterly ~$0.59, growing alongside AI semi profitability

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ──────────────────────────────────────
# Q1 actual: rev $19.31B (+29% YoY), non-GAAP EPS $2.05. Q2 actual: rev $22.19B (+48% YoY), non-GAAP
# EPS $2.44, GAAP EPS $1.91; AI semiconductor revenue $10.8B (+143% YoY); AI semi bookings >$30B vs
# $10.8B shipped. Q3 guide: rev $29.4B (+84% YoY), AI semi ~$16.0B (+200%+), infra software ~$8.9B
# (+31%). FY2026 full-year AI semi guide $56B (+180% YoY); FY2027 AI semi guidance reiterated $100B+.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Semiconductor Solutions (AI/XPU + networking)", 68.0, 40.0, 95.0, "AI semi bookings ($30B+) already outrun shipments ($10.8B) by 3x — the backlog is the bull case's foundation"),
    ("Infrastructure Software (VMware)",               35.0, 30.0, 42.0, "Recurring, high-margin, sticky post-migration revenue; the floor under the bear case"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.711   # FY2026E blended (semis ~65-70%, VMware software ~90%+)
GROSS_MARGIN_BEAR = 0.550   # BEAR: an AI-capex pause hits semi pricing/mix hard even as software holds up
GROSS_MARGIN_BULL = 0.740   # BULL: AI semi scale + rising software mix lift the blend further
OPEX_FIXED_B      = 14.0    # R&D + SG&A ($B, non-GAAP)
TAX_RATE          = 0.140   # effective tax rate

# ── CUSTOM XPU / HYPERSCALER CALCULATOR (the Broadcom-specific angle) ────────
AI_SEMI_Q2_ACTUAL_B      = 10.8   # $B; Q2 FY2026 AI semiconductor revenue
AI_SEMI_Q2_YOY_PCT       = 143    # % YoY growth, Q2 AI semiconductor revenue
AI_SEMI_Q3_GUIDE_B       = 16.0   # $B; Q3 FY2026 AI semiconductor revenue guide
AI_SEMI_FY26_GUIDE_B     = 56     # $B; full-year FY2026 AI semiconductor revenue guide (+180% YoY)
AI_SEMI_FY27_GUIDE_B     = 100    # $B; FY2027 AI semiconductor revenue guide (reiterated, "in excess of")
AI_BOOKINGS_Q2_B         = 30     # $B; Q2 AI semiconductor bookings (vs $10.8B shipped — ~3x book-to-bill)
HYPERSCALE_XPU_CUSTOMERS = 6      # confirmed/rumored hyperscale custom XPU customers (Google, Meta, Anthropic, OpenAI + 2 unnamed)
XPU_JV_VALUE_B           = 35     # $B; Apollo/Blackstone-backed AI XPU platform partnership

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 10.40       # $/share FY2026E non-GAAP; Q1 $2.05 + Q2 $2.44 + Q3E ~$2.85 + Q4E ~$3.05
PE_PESSIMISTIC = 16.0        # trough P/E: a genuine semis-cycle-trough multiple, not a distressed one
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 4.25, 16,   68,  "Hyperscaler AI capex pauses; custom XPU orders slow sharply even as VMware software holds up"),
    "BASE":  (12.84, 33,  424,  "AI semi growth moderates toward the $56B FY2026 guide but doesn't reaccelerate much beyond it"),
    "BULL":  (15.61, 32,  500,  "The $100B+ FY2027 AI semi guide is hit on schedule; the $30B bookings backlog converts to shipments"),
    "XBULL": (19.12, 34,  650,  "Custom XPU expands well beyond the current 6 hyperscale customers; AI semi revenue keeps compounding into FY2028"),
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
        "name":       "AI semiconductor revenue YoY growth",
        "weight":     0.25,
        "thresholds": ("<30%",   "≥80%",   "≥130%",  "≥180%"),
        "now":        "+143%",
        "score":      3,
        "comment":    "Q2 AI semi revenue +143% YoY; Q3 guided to accelerate further to +200%+",
    },
    {
        "name":       "AI semi bookings vs shipments (book-to-bill)",
        "weight":     0.20,
        "thresholds": ("<1.0x",  "≥1.5x",  "≥2.5x",  "≥3.5x"),
        "now":        "~2.8x",
        "score":      3,
        "comment":    "$30B booked vs $10.8B shipped in Q2 — a large, real backlog cushion for the growth guide",
    },
    {
        "name":       "Total revenue YoY growth",
        "weight":     0.15,
        "thresholds": ("<20%",   "≥35%",   "≥50%",   "≥70%"),
        "now":        "+48%",
        "score":      3,
        "comment":    "Q2 +48% YoY; Q3 guided to accelerate to +84% YoY on the AI semi ramp",
    },
    {
        "name":       "VMware/infra software growth",
        "weight":     0.15,
        "thresholds": ("<10%",   "≥20%",   "≥28%",   "≥35%"),
        "now":        "+31%",
        "score":      3,
        "comment":    "Post-acquisition VMware integration is delivering real, sticky, high-margin growth — not just cost cuts",
    },
    {
        "name":       "Custom XPU customer base",
        "weight":     0.15,
        "thresholds": ("1-2",    "3-4",    "5-6",    "7+"),
        "now":        "6 (4 named + 2 unnamed)",
        "score":      3,
        "comment":    "Google, Meta, Anthropic, OpenAI plus two unnamed hyperscale customers — a genuinely diversified custom-silicon base",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.10,
        "thresholds": (">45x",   "≤37x",   "≤30x",   "≤24x"),
        "now":        "~37.6x",
        "score":      2,
        "comment":    "37.6× FY2026E non-GAAP EPS — a rich multiple even against this growth rate",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "The $30B AI semi bookings vs $10.8B shipped is a real, quantified backlog — not a promotional growth claim", +0.6, 0.20),
    ("-", "Custom XPU demand still concentrates in a handful of hyperscale customers; any single pause hits hard", -0.5, 0.20),
    ("-", "Valuation (37.6× forward) already prices in most of the FY2027 $100B+ AI semi guide being hit on schedule", -0.6, 0.20),
    ("+", "VMware gives Broadcom a large, recurring, non-cyclical software base most AI-semi peers lack entirely", +0.5, 0.20),
    ("+", "Reiterated (not raised, but also not walked back) FY2027 guidance signals management confidence in the backlog", +0.3, 0.10),
    ("-", "AI capex is ultimately hyperscaler-discretionary spend; a broader AI-infrastructure digestion cycle would hit all of it at once", -0.4, 0.10),
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
CONS_EPS_2YR  = 13.50   # conservative FY2028E: modest growth off FY2026E, AI semi growth decelerates but doesn't reverse
CONS_PE_2YR   = 28      # a real de-rating from ~37.6× as growth-rate skepticism increases
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  AI Semiconductors / Custom XPU / VMware")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<48}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<48}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<48}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}")
print(f"  Q1 $19.31B → Q2 $22.19B (+48%) → Q3 $29.4B guide (+84%). AI semi: Q2 $10.8B → Q3 $16.0B guide → FY26 $56B guide")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_eps  = round(curr_oi * (1 - TAX_RATE) / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B * 1.08
shares_b  = shares * 0.97
bull_eps_imp = round(bull_oi * (1 - TAX_RATE) / shares_b, 2)

bear_gp   = bear_total * GROSS_MARGIN_BEAR
bear_oi   = bear_gp - OPEX_FIXED_B * 1.02
bear_eps_imp = round(max(0, bear_oi) * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex")
print(f"  − {TAX_RATE*100:.1f}% tax  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − opex, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_BEAR*100:.1f}% GM (AI capex pause hits semi mix) − opex")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# CUSTOM XPU / HYPERSCALER CHECK
print()
print(f"  CUSTOM XPU / HYPERSCALER CHECK  (the Broadcom-specific angle):")
print(f"  AI semi bookings vs shipped (Q2):     ${AI_BOOKINGS_Q2_B}B booked vs ${AI_SEMI_Q2_ACTUAL_B}B shipped  (~{AI_BOOKINGS_Q2_B/AI_SEMI_Q2_ACTUAL_B:.1f}x book-to-bill)")
print(f"  AI semi revenue trajectory:            Q2 ${AI_SEMI_Q2_ACTUAL_B}B (+{AI_SEMI_Q2_YOY_PCT}%) → Q3 ${AI_SEMI_Q3_GUIDE_B}B guide → FY26 ${AI_SEMI_FY26_GUIDE_B}B guide → FY27 ${AI_SEMI_FY27_GUIDE_B}B+ guide")
print(f"  Hyperscale custom XPU customers:       {HYPERSCALE_XPU_CUSTOMERS}  (Google, Meta, Anthropic, OpenAI + 2 unnamed)")
print(f"  Apollo/Blackstone AI XPU platform JV:  ${XPU_JV_VALUE_B}B")
print()
print(f"  This sits at the far downstream end of the same AI infrastructure buildout lifting Lam Research's")
print(f"  equipment orders and Micron's HBM pricing — Broadcom's custom XPUs are what hyperscalers actually")
print(f"  deploy the fabbed, packaged memory-attached silicon into. The backlog (bookings 3x shipments) is a")
print(f"  genuine, quantified signal that this isn't purely sentiment-driven — but it also means the market")
print(f"  has a lot of very specific, checkable numbers to hold Broadcom accountable to each quarter.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_gm  = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 71.1% GM):      +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*33:.2f}/share at 33× P/E")
print(f"  Every 1pp of gross margin:            +${eps_per_1pp_gm:.3f}/EPS  = +${eps_per_1pp_gm*33:.2f}/share at 33× P/E")
print(f"  Every 1 turn of P/E:                  ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (AI semi growth / bookings / total growth / VMware / XPU base / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<44}  {'BEAR':>7}  {'BASE':>7}  {'BULL':>7}  {'XBULL':>7}  {'NOW':>24}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<44}  {ths[0]:>7}  {ths[1]:>7}  {ths[2]:>7}  {ths[3]:>7}  {s['now']:>24}  {lbl}  {b}")
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
    ("AI semi revenue YoY",         "+143%",  "<30%",    "-113pp", "Hyperscalers pause custom XPU orders after over-provisioning capacity in 2025-26"),
    ("Book-to-bill",                "~2.8x",  "<1.0x",   "reversal","The $30B backlog gets cancelled or pushed out rather than converting to shipments"),
    ("Total revenue YoY",           "+48%",   "<20%",    "-28pp+", "AI semi deceleration drags down the consolidated growth rate"),
    ("VMware growth",               "+31%",   "<10%",    "-21pp+", "Post-migration software growth normalizes faster than expected"),
    ("Custom XPU customer base",    "6",      "1-2",     "-4/5",   "Concentration risk materializes — one or two customers dominate and then pull back"),
    ("Forward P/E",                 "~37.6x", ">45x",    "re-rate","Market fully re-prices AI semis for a slower, more cyclical growth trajectory"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Broadcom's bear case isn't really about VMware (sticky, recurring, already de-risked) —")
print(f"  it's entirely about whether the AI semiconductor bookings backlog converts to shipments on schedule.")
print(f"  A 3x book-to-bill ratio is reassuring, but bookings are cancellable in a way shipped, recognized")
print(f"  revenue is not. The single biggest swing factor is hyperscaler capex discipline, not Broadcom execution.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS estimate:       ${EPS_FY2026E:.2f}  (Q1 $2.05 + Q2 $2.44 + Q3E ~$2.85 + Q4E ~$3.05 non-GAAP)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (a genuine semis-cycle-trough multiple, not distressed)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS — a steep premium that prices in most")
print(f"  of the FY2027 $100B+ AI semi guide being hit essentially on schedule. The EPP floor assumes a full")
print(f"  reversion to a normalized semis multiple on THIS YEAR'S earnings — a real, not hypothetical, risk")
print(f"  if AI semi growth merely decelerates rather than reverses.")
print(f"  At a 26× reversion (still a growth premium): ${EPS_FY2026E:.2f} × 26 = ${EPS_FY2026E*26:.0f}  ({(EPS_FY2026E*26/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest growth off FY2026E, AI semi growth decelerates)")
hr()
print(f"  Conservative FY2028E EPS:  ${CONS_EPS_2YR:.2f}  (~14% total EPS growth over 2yr — well below the current trajectory)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~37.6× → 28×; a real de-rating)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: even assuming the AI semi bookings backlog converts to shipments roughly as guided,")
print(f"  a meaningful multiple de-rating from today's 37.6× is enough to produce a {'positive' if cons_return > 0 else 'roughly flat-to-negative'} conservative return.")
print(f"  This is not a name offering a wide margin of safety — you are paying up front for the $100B+ FY2027")
print(f"  AI semi guide to be hit close to on schedule, not for it to already be de-risked.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.40
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; growing alongside AI semi profitability)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (elevated — a high-growth AI semi name with real cyclical exposure)")
print(f"  Beta vs S&P 500:      1.40  (above market; a levered play on AI infrastructure capex)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (large, consistent with a full AI-capex-cycle reversal)")
print(f"  → Q3 FY2026 print (early Sept) is the next test of whether the $16B AI semi guide is hit or exceeded.")
print(f"  → Hyperscaler capex commentary (Google, Meta, Microsoft, Amazon) is the leading indicator between prints.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $310  |  Trim above $470")

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
print(f"  Broadcom's AI semiconductor backlog is real and quantified, and VMware provides a genuine software")
print(f"  floor most AI-semi peers lack — but at 37.6× forward earnings, the stock needs the $100B+ FY2027")
print(f"  guide to land close to on schedule, and the risk/reward skews toward downside if it merely decelerates.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q3 FY2026 print (early September) — does the $16B AI semi guide get hit or exceeded?")
print(f"  (2) Hyperscaler capex guidance at Google, Meta, Microsoft, Amazon earnings — the leading indicator")
print(f"  (3) AI semi book-to-bill trend — does the ~2.8x ratio hold, expand, or start converting down to 1x?")
print(f"  (4) Custom XPU customer count — any expansion beyond the current 6 hyperscale names")
print(f"  (5) VMware growth durability at the ~31% rate as the post-acquisition base normalizes")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $310  |  Trim above $470")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  AI semi FY27 guide: ${AI_SEMI_FY27_GUIDE_B}B+")
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
