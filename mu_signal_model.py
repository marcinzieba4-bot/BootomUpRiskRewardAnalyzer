"""
MU  ·  Micron Technology, Inc.  ·  NASDAQ: MU
Bottom-up signal model  ·  Memory Semiconductors / DRAM / NAND / HBM AI Supercycle
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "MU"
COMPANY       = "Micron Technology, Inc."
SECTOR        = "Memory Semiconductors · DRAM · NAND · HBM AI Infrastructure · NASDAQ: MU"
CURRENT_PRICE = 823.03      # USD; close 2026-07-31, -5.9% on the day (-10.6% for the week) on CXMT competitive news
VOL_52W_LOW   = 105.46      # pre-AI-memory-supercycle trough
VOL_52W_HIGH  = 1255.00     # 2026 AI/HBM-supercycle peak
SHARES_OUT_M  = 1_150.0     # millions diluted; per Q4 FY2026 guide basis
ANNUAL_DIV    = 0.46        # $/share; reinstated/small dividend alongside record profitability

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ──────────────────────────────────────
# Q1 actual: rev $13.64B (DRAM $10.8B record +69% YoY, NAND $2.7B record). Q2 actual: rev $23.86B
# (EPS $12.20 non-GAAP, crushed the $8.19 guide). Q3 actual: rev $41.5B (+74% seq/+346% YoY, record),
# GM 84.9%, EPS $25.11. Q4 guide: rev $50.0B±$1.0B (beat $43.45B Street by $6.55B), non-GAAP GM ~86%,
# non-GAAP EPS $31.00±$1.00 on ~1.15B diluted shares.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("DRAM",  99.0, 55.0, 145.0, "Record pricing on AI/HBM demand; CXMT's ramp is the swing factor for the 2-yr bear case"),
    ("NAND",  30.0, 20.0,  42.0, "Smaller, steadier segment; less exposed to the DRAM-specific CXMT competitive threat"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.816   # FY2026E blended (Q1-Q4 weighted; Q3 actual 84.9%, Q4 guide ~86%, lower Q1/Q2 drag the blend down)
GROSS_MARGIN_BEAR  = 0.350  # BEAR: CXMT-driven oversupply + cyclical downturn crushes pricing, echoing prior memory troughs
GROSS_MARGIN_BULL  = 0.860  # BULL: HBM supercycle pricing power persists through FY2028
OPEX_FIXED_B      = 6.5     # R&D + SG&A ($B); ~$1.65B/qtr non-GAAP opex run-rate annualized
TAX_RATE          = 0.150   # effective tax rate

# ── CXMT COMPETITIVE THREAT CALCULATOR (the Micron-specific risk) ────────────
CXMT_WSPM_2026        = 350_000  # wafer starts per month CXMT is on track for by end-2026
MICRON_WSPM_EST       = 375_000  # approx Micron wafer starts per month (CXMT within ~25K of parity)
CXMT_IPO_RAISE_B      = 8.6      # $B raised in CXMT's Shanghai IPO
CXMT_IPO_POP_PCT      = 466      # % first-day pop on CXMT's Shanghai debut
MU_MKT_CAP_LOST_B     = 45.0     # $B of Micron market cap erased on the CXMT-driven selloff
HBM_TAM_2025_B        = 35       # $B; HBM total addressable market, 2025
HBM_TAM_2028_B        = 100      # $B; HBM TAM, 2028E — the structural bull counterweight to the CXMT threat

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 73.00       # $/share FY2026E non-GAAP; Q1 $4.78 + Q2 $12.20 + Q3 $25.11 + Q4E $31.00 (guide midpoint)
PE_PESSIMISTIC = 8.0         # trough P/E: Micron's own multi-cycle memory-trough average (memory stocks re-rate hard at cycle peaks)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 14.36,  8, 115,   "CXMT and Chinese DRAM capacity trigger a classic memory down-cycle; pricing collapses toward variable cost"),
    "BASE":  ( 90.00, 11, 990,   "AI/HBM demand and Chinese competition roughly balance; growth continues but the multiple compresses modestly"),
    "BULL":  (117.15, 13, 1523,  "HBM supercycle outruns CXMT's ramp; pricing power holds through FY2028 (matches the $1,522 average analyst target)"),
    "XBULL": (146.70, 15, 2200,  "HBM TAM hits $100B+ on schedule, Micron holds share, and the AI infrastructure buildout re-rates memory permanently"),
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
        "name":       "Revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<50%",   "≥100%",  "≥200%",  "≥300%"),
        "now":        "+346%",
        "score":      4,
        "comment":    "Q3 FY2026 record — the fastest revenue growth in Micron's history, driven by AI/HBM demand",
    },
    {
        "name":       "Gross margin trajectory",
        "weight":     0.20,
        "thresholds": ("<50%",   "≥65%",   "≥78%",   "≥85%"),
        "now":        "~85-86%",
        "score":      4,
        "comment":    "Q3 actual 84.9%, Q4 guided ~86% — both multi-decade highs for the company",
    },
    {
        "name":       "HBM TAM capture",
        "weight":     0.15,
        "thresholds": ("shrinking","flat",   "growing", "tripling"),
        "now":        "$35B→$100B by 2028",
        "score":      3,
        "comment":    "HBM TAM nearly tripling through 2028; Micron is a top-3 qualified HBM supplier but not the clear share leader",
    },
    {
        "name":       "CXMT / Chinese DRAM competitive threat",
        "weight":     0.20,
        "thresholds": ("share loss now","parity risk","manageable","non-factor"),
        "now":        "parity risk",
        "score":      2,
        "comment":    "CXMT on track for ~350K WSPM by end-2026, within ~25K of Micron; $8.6B Shanghai IPO funds further expansion",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.15,
        "thresholds": (">25x",   "≤18x",   "≤13x",   "≤9x"),
        "now":        "~11.3x",
        "score":      3,
        "comment":    "11.3× FY2026E non-GAAP EPS — cheap for the growth rate, reflecting the market's distrust of cycle-peak memory earnings",
    },
    {
        "name":       "Q4 guidance vs Street consensus",
        "weight":     0.10,
        "thresholds": ("well below","below",  "in-line", "above"),
        "now":        "well above",
        "score":      4,
        "comment":    "Q4 revenue guide beat consensus by $6.55B and EPS guide beat by ~$5.57 at the midpoint",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "HBM demand is structurally durable through the 2028 AI infrastructure buildout, not a one-quarter blip", +0.6, 0.20),
    ("-", "CXMT and Chinese DRAM capacity are the single biggest 2-yr risk — a real, funded, fast-moving competitive threat", -0.6, 0.25),
    ("-", "Memory is a historically brutal boom-bust cycle; today's 85%+ gross margins are almost certainly near a cyclical peak", -0.5, 0.20),
    ("+", "At ~11.3× forward earnings the stock is still priced for skepticism, not for the AI supercycle continuing", +0.4, 0.15),
    ("+", "HBM customer base spans essentially every AI accelerator maker, reducing single-customer concentration risk", +0.3, 0.10),
    ("-", "Capex intensity is rising sharply to chase capacity, which will pressure free cash flow even as earnings peak", -0.3, 0.10),
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
CONS_EPS_2YR  = 85.00   # conservative FY2028E: modest growth off the FY2026E base, memory cycle risk discounted
CONS_PE_2YR   = 10       # a real de-rating from ~11.3× as cycle-peak skepticism persists
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  DRAM / NAND / HBM AI Supercycle")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
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
print(f"  Q1 $13.64B → Q2 $23.86B → Q3 $41.5B (actual) → Q4 $50.0B±$1.0B (guide, beat Street by $6.55B)")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_eps  = round(curr_oi * (1 - TAX_RATE) / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B * 1.10
shares_b  = shares * 0.97
bull_eps_imp = round(bull_oi * (1 - TAX_RATE) / shares_b, 2)

bear_gp   = bear_total * GROSS_MARGIN_BEAR
bear_oi   = bear_gp - OPEX_FIXED_B * 1.05
bear_eps_imp = round(max(0, bear_oi) * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex")
print(f"  − {TAX_RATE*100:.1f}% tax  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − opex, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_BEAR*100:.1f}% GM (CXMT-driven oversupply cycle) − opex")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# CXMT COMPETITIVE THREAT CHECK
print()
print(f"  CXMT COMPETITIVE THREAT CHECK  (the Micron-specific risk):")
print(f"  CXMT wafer starts/month (2026E):     {CXMT_WSPM_2026:,}  vs Micron's ~{MICRON_WSPM_EST:,}  (within ~25K of parity)")
print(f"  CXMT Shanghai IPO:                    ${CXMT_IPO_RAISE_B:.1f}B raised, +{CXMT_IPO_POP_PCT}% first-day pop")
print(f"  Micron market cap erased on the news: ${MU_MKT_CAP_LOST_B:.1f}B  (~$5.20 lost for every $1 CXMT raised)")
print(f"  HBM TAM (the structural counterweight): ${HBM_TAM_2025_B}B (2025) → ${HBM_TAM_2028_B}B (2028E)")
print()
print(f"  This is the flip side of the same AI-driven memory supercycle squeezing Apple's iPhone margins —")
print(f"  DRAM and HBM capacity is being bid away from consumer electronics toward AI infrastructure, and")
print(f"  Micron is the direct beneficiary of the pricing power Apple is complaining about. CXMT is the real")
print(f"  counter-risk: a state-backed, fast-scaling Chinese DRAM maker that could cap the pricing upside")
print(f"  this cycle has delivered, particularly in commodity DRAM rather than leading-edge HBM.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_gm  = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 81.6% GM):      +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*11:.2f}/share at 11× P/E")
print(f"  Every 1pp of gross margin:            +${eps_per_1pp_gm:.3f}/EPS  = +${eps_per_1pp_gm*11:.2f}/share at 11× P/E")
print(f"  Every 1 turn of P/E:                  ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (revenue growth / margin / HBM TAM / CXMT threat / valuation / guidance)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<42}  {'BEAR':>15}  {'BASE':>11}  {'BULL':>10}  {'XBULL':>9}  {'NOW':>13}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<42}  {ths[0]:>15}  {ths[1]:>11}  {ths[2]:>10}  {ths[3]:>9}  {s['now']:>13}  {lbl}  {b}")
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
    ("Revenue YoY",                 "+346%",  "<0%",     "collapse","CXMT floods the commodity DRAM market; pricing reverts toward variable cost"),
    ("Gross margin",                "~85-86%","<40%",    "-45pp+", "Classic memory down-cycle; oversupply crushes pricing across DRAM and NAND alike"),
    ("HBM TAM capture",             "growing","stalls",  "reversal","Alternative memory architectures or a slower AI capex cycle cap HBM's growth"),
    ("CXMT competitive threat",     "parity risk","share loss now","worse","CXMT's second Beijing fab comes online faster than expected, undercutting on price"),
    ("Forward P/E",                 "~11.3x", ">25x",    "re-rate","Ironically, P/E can rise even as the stock falls if EPS collapses faster than price"),
    ("Q4 guide vs consensus",       "well above","well below","reversal","A single quarter's beat proves to be peak-cycle, not a new trajectory"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: memory is the most cyclical major semiconductor category, and Micron's own history")
print(f"  includes multiple 50-80% peak-to-trough drawdowns. CXMT is the specific, funded, fast-moving")
print(f"  catalyst that could turn this AI-driven supercycle into a conventional memory down-cycle faster")
print(f"  than the HBM TAM buildout can offset it. The same memory shortage inflating Apple's iPhone costs")
print(f"  is Micron's tailwind today — but tailwinds in memory have historically reversed hard and fast.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS estimate:       ${EPS_FY2026E:.2f}  (Q1 $4.78 + Q2 $12.20 + Q3 $25.11 + Q4E $31.00 non-GAAP)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (Micron's own multi-cycle memory-trough average)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS — cheap by growth-stock standards, but")
print(f"  the market is pricing meaningful skepticism that ~85% gross margins and record EPS are sustainable.")
print(f"  The EPP floor assumes a full reversion to Micron's historical trough multiple on THIS YEAR'S")
print(f"  cycle-peak earnings — a genuinely conservative floor, not a base case.")
print(f"  At a 15× reversion (a normalized cyclical multiple): ${EPS_FY2026E:.2f} × 15 = ${EPS_FY2026E*15:.0f}  ({(EPS_FY2026E*15/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest growth off the FY2026E base, cycle risk discounted)")
hr()
print(f"  Conservative FY2028E EPS:  ${CONS_EPS_2YR:.2f}  (below FY2026E — assumes the cycle has partially rolled over by then)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~11.3× → 10×; a modest further de-rating)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: even a conservative case that assumes EPS declines modestly off this year's")
print(f"  cycle-peak and the multiple compresses further still clears a {'positive' if cons_return > 0 else 'negative'} return, because the starting")
print(f"  multiple (11.3×) is already so undemanding. The real risk isn't a modest EPS decline — it's the")
print(f"  full-cycle-reversal BEAR case, where CXMT-driven oversupply pushes margins toward the 30s.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.55
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Recent moves:          -5.9% (1-day) / -10.6% (1-week) on the CXMT competitive news")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; a small, recently reinstated payout)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (high — typical for cyclical memory semis, especially at a cycle extreme)")
print(f"  Beta vs S&P 500:      1.75  (well above market; among the most volatile large-cap semis)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (large but well within Micron's own historical cycle-crash range)")
print(f"  → Q4 FY2026 print (late Sept) is the next test of whether pricing power holds through the CXMT headlines.")
print(f"  → CXMT capacity ramp and Chinese DRAM ASPs are the leading indicators to watch between prints.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add aggressively below $650  |  Trim above $1,400")

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
print(f"  Micron is delivering the strongest growth and margin expansion in its history, and the market")
print(f"  is still pricing it at a cyclical discount ({CURRENT_PRICE/EPS_FY2026E:.1f}× forward) rather than a growth-stock multiple.")
print(f"  CXMT is a real, quantified risk to the 2-year horizon, but the HBM TAM buildout is the larger force.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q4 FY2026 print (late September) — does pricing power hold through the CXMT headlines?")
print(f"  (2) CXMT's second Beijing fab progress and Chinese DRAM ASP trends — the leading competitive indicator")
print(f"  (3) HBM4 qualification and share gains at Nvidia/AI accelerator customers")
print(f"  (4) Capex guidance — how aggressively Micron chases capacity vs. protects free cash flow")
print(f"  (5) Any signs of DRAM/NAND spot pricing cracking — the first tell of a cycle turn")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add aggressively below $650  |  Trim above $1,400")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  CXMT WSPM: {CXMT_WSPM_2026:,} vs Micron ~{MICRON_WSPM_EST:,}")
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
