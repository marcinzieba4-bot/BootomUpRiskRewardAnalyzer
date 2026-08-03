"""
PANW  ·  Palo Alto Networks, Inc.  ·  NASDAQ: PANW
Bottom-up signal model  ·  Cybersecurity Platform / NGS / Cortex AI-SOC / CyberArk Identity
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "PANW"
COMPANY       = "Palo Alto Networks, Inc."
SECTOR        = "Cybersecurity Platform · Network Security · Cloud Security · AI-SOC · Identity (CyberArk) · NASDAQ: PANW"
CURRENT_PRICE = 331.83       # USD; close 2026-07-31 (verified live)
VOL_52W_LOW   = 139.57       # 2025 trough
VOL_52W_HIGH  = 368.80       # 2026 platformization/CyberArk-deal re-rating peak
SHARES_OUT_M  = 815.0        # millions; $270.4B mkt cap / $331.83
ANNUAL_DIV    = 0.0          # $/share — no dividend; all capital to M&A, buyback, and platform R&D

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B; fiscal year ends July 31) ───────────
# Q3 FY2026 actual: revenue $3.0B (+31% YoY, incl. $388M from CyberArk+Chronosphere = organic ~+14%)
# FY2026 guide: revenue $11.415-11.425B (+24%), NGS ARR $8.90-8.95B (+59-60%, CyberArk-inflated), RPO ~$21B (+32-33%)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Network Security (FW/SASE)",         4.60, 4.00, 5.30, "Mature core, steady renewal base; the segment least exposed to platformization upside or AI risk"),
    ("Cloud Security (Prisma Cloud)",      2.20, 1.90, 2.70, "Cloud-native security growth; competes with CNAPP specialists and hyperscaler-native tools"),
    ("Security Operations (Cortex/XSIAM)", 1.90, 1.60, 2.60, "The AI-SOC bet; XSIAM is management's proof point that AI displaces, not just assists, the SOC"),
    ("Identity Security (CyberArk) + Other", 2.72, 2.30, 3.60, "Newly consolidated; integration execution and cross-sell into the base are unproven at this scale"),
]

# Margin assumptions (non-GAAP; PANW's non-GAAP EPS also nets in interest income, modeled as a blended pre-tax margin)
OP_MARGIN_CURR   = 0.322    # FY2026E blended non-GAAP pre-tax margin proxy (op margin guide 28.9-29.2% + net interest income)
OP_MARGIN_BULL   = 0.380    # BULL: platformization drives real operating leverage as CyberArk integration completes
OP_MARGIN_BEAR   = 0.267    # BEAR: integration costs and discounting to defend renewals compress the blend
TAX_RATE         = 0.160    # non-GAAP effective tax rate

# ── PLATFORMIZATION / M&A CALCULATOR (the PANW-specific angle) ───────────────
PLATFORM_CUSTOMERS       = 2280   # organizations consolidating multiple PANW products, +110 net new in Q3
PLATFORM_TARGET_FY2030   = 4000   # management's stated platformization target
PLATFORM_NRR_PCT         = 120    # % net retention rate among platformized customers
CYBERARK_Q3_CONTRIB_M    = 388    # $M CyberArk + Chronosphere contribution to Q3 revenue
GAAP_Q3_NET_LOSS_M       = 177    # $M GAAP net loss in Q3 (vs GAAP net income $262M a year ago)
GAAP_Q3_SBC_M            = 517    # $M share-based compensation in Q3
GAAP_Q3_ACQ_COSTS_M      = 198    # $M acquisition-related costs in Q3
NEXT_REPORT_DATE         = "2026-08-17"  # Q4/FY2026 results — about two weeks after this refresh

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 3.78         # $/share non-GAAP FY2026E; company guidance $3.77-$3.79
PE_PESSIMISTIC = 40.0         # trough P/E: even PANW's worst multiple compressions in recent years
                              # have stopped in the high-30s/low-40s on non-GAAP EPS; this is not a value stock
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 2.70, 40,  108, "Platformization stalls; CyberArk integration costs bite margin; NGS ARR growth normalizes hard"),
    "BASE":  ( 5.20, 70,  364, "NGS ARR keeps compounding as CyberArk integrates cleanly; multiple compresses only modestly"),
    "BULL":  ( 5.79, 78,  452, "Platformization scales past 3,000 customers; Cortex XSIAM becomes the enterprise AI-SOC standard"),
    "XBULL": ( 7.20, 88,  634, "PANW re-rates as the AI-native security platform of record; identity + SecOps + network fully cross-sell"),
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
        "name":       "Total revenue YoY growth (reported)",
        "weight":     0.15,
        "thresholds": ("<15%",   "≥20%",   "≥27%",   "≥35%"),
        "now":        "+31%",
        "score":      3,
        "comment":    "Q3 $3.0B (+31%), but $388M (~13pp) came from CyberArk/Chronosphere — headline growth is M&A-flattered",
    },
    {
        "name":       "Organic revenue growth (ex-M&A)",
        "weight":     0.20,
        "thresholds": ("<8%",    "≥12%",   "≥16%",   "≥20%"),
        "now":        "~14%",
        "score":      2,
        "comment":    "Backing out the $388M acquired contribution implies core-business growth in the mid-teens — solid, not spectacular",
    },
    {
        "name":       "NGS ARR growth (reported)",
        "weight":     0.15,
        "thresholds": ("<30%",   "≥40%",   "≥55%",   "≥70%"),
        "now":        "+59-60%",
        "score":      3,
        "comment":    "Guided $8.90-8.95B; again substantially inflated by consolidating CyberArk's existing ARR base, not pure new bookings",
    },
    {
        "name":       "Platformization momentum",
        "weight":     0.20,
        "thresholds": ("<50/qtr","≥80/qtr","≥110/qtr","≥150/qtr"),
        "now":        "110/qtr",
        "score":      3,
        "comment":    "2,280 platformized customers, 120% NRR, single-digit churn — the best evidence the strategy is working, not just a slogan",
    },
    {
        "name":       "GAAP profitability (post-M&A)",
        "weight":     0.15,
        "thresholds": ("deep loss","narrow loss","breakeven","GAAP profitable"),
        "now":        "narrow loss",
        "score":      2,
        "comment":    "Q3 GAAP net loss $177M on $517M SBC + $198M acquisition costs; non-GAAP EPS still grew — a real but bounded distortion",
    },
    {
        "name":       "Forward P/E (non-GAAP)",
        "weight":     0.15,
        "thresholds": (">100x",  "≤85x",   "≤70x",   "≤55x"),
        "now":        "87.8x",
        "score":      1,
        "comment":    "87.8× FY2026E non-GAAP EPS — one of the richest multiples in large-cap software, leaving very little room for error",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Platformization is real and measurable — 2,280 customers, 120% NRR, single-digit churn, not a narrative", +0.7, 0.20),
    ("-", "Valuation — 87.8× forward non-GAAP EPS prices flawless multi-year execution across three integrations at once", -1.0, 0.25),
    ("-", "M&A-flattered growth — organic revenue growth (~14%) is roughly half the ~31% headline; the gap is a real quality discount", -0.6, 0.20),
    ("+", "Cortex XSIAM traction — the clearest evidence yet that PANW can sell AI-native security, not just legacy platform bundling", +0.5, 0.15),
    ("-", "Integration risk — CyberArk and Chronosphere both landed within the same fiscal year; execution risk is stacked, not staggered", -0.5, 0.15),
    ("+", "No debt overhang from a cash-funded core business — the GAAP loss is an accounting artifact of the deals, not a cash problem", +0.3, 0.05),
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
CONS_EPS_2YR  = 4.90    # conservative FY2028E: ~13.9% EPS CAGR — well below the BASE/BULL cases
CONS_PE_2YR   = 55      # multiple compresses hard from 87.8× toward a still-generous large-cap-software level
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Cybersecurity Platform / AI-SOC / Identity")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))
print(f"  ⚠ Q4/FY2026 results due {NEXT_REPORT_DATE} — about two weeks after this refresh. Figures below")
print(f"  use Q3 FY2026 actuals and the company's raised full-year guidance.")

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
    print(f"  {seg:<38}  ${curr:>11.2f}  ${bear:>8.2f}  ${bull:>8.2f}  {bear-curr:>+7.2f}  {bull-curr:>+7.2f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<38}  ${curr_total:>11.2f}  ${bear_total:>8.2f}  ${bull_total:>8.2f}  {bear_total-curr_total:>+7.2f}  {bull_total-curr_total:>+7.2f}")
print(f"  FY2026 guidance: revenue $11.415-11.425B (+24%), non-GAAP EPS $3.77-$3.79, NGS ARR $8.90-8.95B")
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

print(f"  FY2026E EPS check:  ${curr_total:.2f}B rev × {OP_MARGIN_CURR*100:.1f}% pre-tax margin proxy − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (company guidance ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B rev × {OP_MARGIN_BULL*100:.1f}% margin, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 78× = ~${bull_eps_imp*78:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B rev × {OP_MARGIN_BEAR*100:.1f}% margin (integration costs, renewal discounting)")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 40× trough = ~${bear_eps_imp*40:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")
print()
print(f"  ⚠ NOTE: even the BEAR trough multiple (40×) is richer than the CURRENT multiple most")
print(f"  software names in this coverage trade at. PANW does not have a cheap floor — the entire")
print(f"  risk/reward here is about whether a persistently expensive multiple holds, compresses")
print(f"  modestly, or compresses a lot. There is no scenario in this model where it goes to a")
print(f"  conventional value multiple; the platform economics don't support that kind of re-rating.")

# PLATFORMIZATION / M&A CHECK
print()
print(f"  PLATFORMIZATION & M&A CHECK  (the PANW-specific angle):")
print(f"  Platformized customers:        {PLATFORM_CUSTOMERS:,}  (+110 net new in Q3; target {PLATFORM_TARGET_FY2030:,} by FY2030)")
print(f"  Net retention (platform cust.): {PLATFORM_NRR_PCT}%  with single-digit churn")
print(f"  CyberArk + Chronosphere Q3 contribution: ${CYBERARK_Q3_CONTRIB_M}M  (~13pp of the 31% reported growth)")
print(f"  Q3 GAAP net loss:               (${GAAP_Q3_NET_LOSS_M}M)  — driven by ${GAAP_Q3_SBC_M}M SBC + ${GAAP_Q3_ACQ_COSTS_M}M acquisition costs")
print()
print(f"  Two things are true at once, and the model tries to hold both. Platformization is the")
print(f"  best-evidenced strategy in the cybersecurity sector right now — 120% net retention among")
print(f"  platform customers is a genuinely strong number. But roughly 13 points of the quarter's")
print(f"  31% headline growth came from acquired revenue, not organic execution, and the GAAP loss")
print(f"  — while mostly non-cash — shows the real cost of running three integrations at once.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * OP_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_marg = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 32.2% margin proxy):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*70:.2f}/share at 70× P/E")
print(f"  Every 1pp of margin:                        +${eps_per_1pp_marg:.3f}/EPS  = +${eps_per_1pp_marg*70:.2f}/share at 70× P/E")
print(f"  Every 1 turn of P/E:                        ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")
print(f"  ↑ at 87.8× forward, the multiple dwarfs everything else in this table")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (reported vs organic growth / NGS ARR / platformization / GAAP profit / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<40}  {'BEAR':>10}  {'BASE':>9}  {'BULL':>10}  {'XBULL':>10}  {'NOW':>12}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<40}  {ths[0]:>10}  {ths[1]:>9}  {ths[2]:>10}  {ths[3]:>10}  {s['now']:>12}  {lbl}  {b}")
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
print(f"  {'Signal':<34}  {'Current':>10}  {'Bear val':>10}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Organic revenue growth",      "~14%",   "<8%",     "-6pp",   "Core network/cloud security decelerates as the market matures"),
    ("Platformization momentum",    "110/qtr","<50/qtr", "-60/qtr","Customers resist further consolidation after the CyberArk price tag"),
    ("NGS ARR growth (reported)",   "+59-60%","<30%",    "-30pp",  "Acquired ARR anniversaries and organic bookings don't backfill the comp"),
    ("GAAP profitability",          "narrow loss","widens","worse","Integration costs run longer or deeper than guided"),
    ("Forward P/E",                 "87.8x",  "≤55x",    "-33x",   "Market re-prices platformization risk as software multiples broadly compress"),
    ("Cortex XSIAM traction",       "scaling","stalls",  "reverse","AI-SOC bookings plateau; legacy SIEM vendors or hyperscalers win the category"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<34}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:42]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: at 87.8× forward earnings, PANW doesn't need anything to go WRONG for the")
print(f"  stock to underperform — it only needs growth to merely NORMALIZE from an M&A-inflated")
print(f"  pace to a purely organic one, while the market simultaneously decides that multiple no")
print(f"  longer deserves the platformization premium. Both of those are plausible without either")
print(f"  qualifying as a company-specific disaster, which is what makes the valuation risk here")
print(f"  structurally different from a name with a cheap floor to catch it.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E non-GAAP EPS (company guide):  ${EPS_FY2026E:.2f}  ($3.77-$3.79)")
print(f"  Pessimistic P/E at trough:               {PE_PESSIMISTIC:.0f}×  (PANW has rarely compressed below the high-30s/low-40s on non-GAAP EPS)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP is the widest gap in the software coverage. The EPP floor")
print(f"  itself, at 40× non-GAAP earnings, is not a distress multiple by any normal standard — it")
print(f"  is simply PANW's own historical floor. That tells you the whole story: there is no cheap")
print(f"  scenario for this stock short of a genuine platform-thesis failure. You are either paying")
print(f"  up for quality and execution, or you are waiting for a re-rating that may not come.")
print(f"  At a 60× reversion (still a rich multiple by any peer comparison): ${EPS_FY2026E:.2f} × 60 = ${EPS_FY2026E*60:.0f}")
print(f"  ({(EPS_FY2026E*60/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: growth normalizes toward organic pace, real multiple compression)")
hr()
print(f"  Conservative FY2028E non-GAAP EPS:  ${CONS_EPS_2YR:.2f}  (~13.9% EPS CAGR — close to the current organic growth rate)")
print(f"  Conservative exit P/E:               {CONS_PE_2YR}×  (87.8× → 55×; a real de-rating, still rich by absolute standards)")
print(f"  Conservative equity value:            ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):        +${cons_divs:.2f}/share  (no dividend)")
hr()
print(f"  Conservative 2yr total:               ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:            {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: even holding EPS growth near today's healthy organic pace, a multiple")
print(f"  de-rating from 87.8× to a still-generous 55× produces a {'negative' if cons_return < 0 else 'modest positive'} conservative return.")
print(f"  This is the clearest signal the model has on PANW: you are not being paid a margin of")
print(f"  safety for the valuation risk. The bull case is genuinely available — platformization is")
print(f"  real — but the conservative case is a warning, not a floor.")
print(f"  Breakeven at 55× requires FY2028E EPS ≥ ${CURRENT_PRICE / CONS_PE_2YR:.2f} — above this conservative estimate.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.38
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Move off the low:     +{(CURRENT_PRICE/VOL_52W_LOW-1)*100:.0f}%  in the past year — the platformization/M&A re-rating in one number")
print(f"  Annual dividend:      none — all capital to M&A, buyback, and platform R&D")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (high-multiple software beta; earnings-day gaps of ±10% are routine)")
print(f"  Beta vs S&P 500:      1.25  (elevated for a security name; now carries M&A-integration risk premium)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe, but this stock has already moved similarly in the other direction)")
print(f"  → {NEXT_REPORT_DATE} print: watch organic growth disclosure and GAAP-loss trajectory, not just the ARR headline.")
print(f"  → Platformized-customer count is the single best quarterly proof point for the bull case.")
print(f"  → AVOID at current price  |  WATCHLIST $230–270  |  ACCUMULATE $190–220  |  BUY below $180")

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
print(f"  PANW is executing a genuinely ambitious platform strategy, and the platformization")
print(f"  metrics back that up. But roughly 13 points of headline growth is acquired, not organic,")
print(f"  and the multiple leaves no room for the market to notice that gap. AVOID reflects a real")
print(f"  company at a price the model can't underwrite without more evidence of organic acceleration —")
print(f"  ratio B ({ratio_b_str}) says the downside case outweighs the upside case by a wide margin from here.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) {NEXT_REPORT_DATE} Q4/FY2026 results — organic growth disclosure is the single most important number")
print(f"  (2) Platformized-customer count trajectory toward the FY2030 target of {PLATFORM_TARGET_FY2030:,}")
print(f"  (3) GAAP profitability path — does the loss narrow as integration costs roll off, or persist?")
print(f"  (4) Cortex XSIAM booking metrics — the company's specific evidence for the AI-SOC thesis")
print(f"  (5) Any further M&A — another large deal before CyberArk fully integrates would raise execution risk further")
print(f"  AVOID at ${CURRENT_PRICE:.2f}  |  WATCHLIST $230–270  |  ACCUMULATE $190–220  |  BUY below $180")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  Platform customers: {PLATFORM_CUSTOMERS:,}")
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
