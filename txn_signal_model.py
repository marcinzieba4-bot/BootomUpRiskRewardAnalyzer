"""
TXN  ·  Texas Instruments Incorporated  ·  NASDAQ: TXN
Bottom-up signal model  ·  Analog & Embedded Semiconductors / Industrial / Auto / AI Data Center
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "TXN"
COMPANY       = "Texas Instruments Incorporated"
SECTOR        = "Analog & Embedded Semiconductors · Industrial · Automotive · AI Data Center · NASDAQ: TXN"
CURRENT_PRICE = 275.74       # USD; close 2026-07-31 (verified live)
VOL_52W_LOW   = 152.73       # 2025 industrial-cycle trough
VOL_52W_HIGH  = 334.03       # 2026 post-Q1 AI/data-center re-rating peak (one-day +18% on the print)
SHARES_OUT_M  = 905.0        # millions; $251.8B mkt cap / $275.74
ANNUAL_DIV    = 5.68         # $/share forward; yield ~2.06%; long-running growth streak

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ──────────────────────────────────────
# Q1 actual $4.83B (+19%), Q2 actual $5.46B (+23%); Q3 guide $5.65-6.15B.
# Analog/Embedded mix from Q2: Analog $4.37B (80%), Embedded $788M (14%), Other $310M (6%)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Analog (Power + High-Volume)", 17.6, 14.0, 20.5, "Industrial +30% YoY, auto mid-teens, data-center power roughly doubled YoY in Q2"),
    ("Embedded Processing (MCU)",     3.1,  2.5,  3.8, "Industrial/auto microcontrollers; smaller segment, steadier growth than Analog"),
    ("Other (DLP/custom, royalties)", 1.3,  1.1,  1.5, "Legacy licensing + custom ASIC; low-growth, high-margin tail"),
]

# Margin assumptions (non-GAAP-equivalent; TI reports GAAP with minimal adjustment items)
GROSS_MARGIN_CURR = 0.610   # FY2026E blended gross margin; Q2 GM 61%, +340bp sequentially on utilization
GROSS_MARGIN_BULL = 0.630   # BULL: fab utilization climbs further on data-center/AI demand
OPEX_FIXED_B      = 4.20    # R&D + SG&A ($B)
TAX_RATE          = 0.140   # effective tax rate

# ── DATA CENTER / CAPACITY CALCULATOR (the TI-specific angle) ────────────────
DC_REVENUE_2025_B     = 1.5   # $B AI/data-center-linked revenue in 2025 (~9% of total sales)
DC_GROWTH_Q2_YOY      = "roughly doubled"  # qualitative: Q2 2026 data-center revenue YoY growth
CAPEX_GUIDE_LOW_B     = 2.0   # $B FY2026 capex guidance low end
CAPEX_GUIDE_HIGH_B    = 3.0   # $B FY2026 capex guidance high end (down from prior years' $4-5B pace)
TTM_FCF_B             = 6.5   # $B trailing-twelve-month free cash flow
Q3_GUIDE_REV_LOW_B    = 5.65  # $B Q3 2026 revenue guidance low end
Q3_GUIDE_REV_HIGH_B   = 6.15  # $B Q3 2026 revenue guidance high end

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 8.75         # $/share; Q1 $1.68 + Q2 $2.14 + Q3E ~$2.40 (guide midpoint) + Q4E ~$2.55
PE_PESSIMISTIC = 20.0         # trough P/E: TI traded 20-24x forward during the 2023-24 industrial
                              # down-cycle; 20x prices a comparable inventory-correction repeat
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 5.58, 20,  112, "Industrial/auto inventory correction repeats; data-center demand doesn't scale fast enough to offset"),
    "BASE":  (10.20, 30,  306, "Industrial/auto cycle stays healthy; data-center revenue keeps compounding off a small base"),
    "BULL":  (11.28, 34,  383, "Fab utilization climbs further; data-center becomes a structural double-digit % of revenue"),
    "XBULL": (13.50, 38,  513, "TI re-rates as the analog supplier of record for AI-infrastructure power delivery"),
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
        "thresholds": ("<8%",    "≥14%",   "≥20%",   "≥28%"),
        "now":        "+23%",
        "score":      3,
        "comment":    "Q2 $5.46B (+23%, +13% sequential), above the high end of guidance for a second straight quarter",
    },
    {
        "name":       "Industrial revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<10%",   "≥18%",   "≥26%",   "≥35%"),
        "now":        "+30%",
        "score":      3,
        "comment":    "The segment that led the 2023-24 down-cycle is now leading the recovery — broad-based, not just AI-linked",
    },
    {
        "name":       "Data-center revenue trajectory",
        "weight":     0.20,
        "thresholds": ("flat",   "+30-60%","+60-100%","doubling+"),
        "now":        "~doubled YoY",
        "score":      4,
        "comment":    "~9% of 2025 revenue and roughly doubled YoY in Q2 — small base, but the fastest-growing piece of the mix",
    },
    {
        "name":       "Gross margin trend",
        "weight":     0.15,
        "thresholds": ("<52%",   "≥56%",   "≥60%",   "≥64%"),
        "now":        "61%",
        "score":      3,
        "comment":    "+340bp sequentially in Q2 on utilization — the clearest read on where the cycle sits",
    },
    {
        "name":       "Capex discipline",
        "weight":     0.10,
        "thresholds": (">$5B",   "≤$4B",   "≤$3B",   "≤$2B"),
        "now":        "$2-3B",
        "score":      3,
        "comment":    "Guided down from the $4-5B/yr pace of the prior capacity build-out — funding growth from a smaller check now",
    },
    {
        "name":       "Forward P/E vs 10-yr average (~24x)",
        "weight":     0.15,
        "thresholds": (">34x",   "≤28x",   "≤22x",   "≤17x"),
        "now":        "31.5x",
        "score":      1,
        "comment":    "31.5× FY2026E — a meaningful premium to TI's own history, priced for the AI/data-center growth continuing uninterrupted",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Cycle inflection is real — industrial +30%, two straight above-guidance quarters, GM expanding fast", +0.8, 0.20),
    ("+", "Data-center optionality — ~9% of revenue and doubling YoY, funded by disciplined $2-3B capex, not a re-lever", +0.5, 0.15),
    ("-", "Valuation — 31.5× forward vs a ~24× 10-yr average; the recovery is already substantially priced in",   -0.9, 0.25),
    ("-", "Cyclicality — analog/industrial is the textbook boom-bust semiconductor category; nothing here repeals that", -0.5, 0.15),
    ("+", "Capital return — 2.06% yield, long dividend growth streak, funded by $6.5B TTM FCF",                    +0.4, 0.15),
    ("-", "One-day +18% move on the Q1 print — a stock that reprices this hard on a single quarter has limited room for a miss", -0.4, 0.10),
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
CONS_EPS_2YR  = 10.00   # conservative FY2028E: ~6.9% EPS CAGR — well below the current growth pace
CONS_PE_2YR   = 25      # multiple compresses from 31.5× toward a level closer to the historical average
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Analog / Embedded / Industrial / AI Data Center")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<32}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<32}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<32}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  Q1 actual $4.83B (+19%), Q2 actual $5.46B (+23%). Q3 guide: ${Q3_GUIDE_REV_LOW_B:.2f}-{Q3_GUIDE_REV_HIGH_B:.2f}B")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_eps  = round(curr_oi * (1 - TAX_RATE) / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B * 1.10
shares_b  = shares * 0.98
bull_eps_imp = round(bull_oi * (1 - TAX_RATE) / shares_b, 2)

bear_gp   = bear_total * 0.560     # utilization drops hard in an inventory-correction scenario
bear_oi   = bear_gp - OPEX_FIXED_B * 0.95
bear_eps_imp = round(max(0, bear_oi) * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex")
print(f"  − {TAX_RATE*100:.1f}% tax  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − opex, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 34× = ~${bull_eps_imp*34:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × 56.0% GM (utilization drops in an inventory correction) − opex")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 20× trough = ~${bear_eps_imp*20:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")
print()
print(f"  ⚠ NOTE: analog semiconductor economics are almost entirely about FAB UTILIZATION. A")
print(f"  {(1-bear_total/curr_total)*100:.0f}% revenue decline in the bear case produces a {(1-bear_eps_imp/curr_eps)*100:.0f}% EPS decline, because TI's")
print(f"  largely fixed manufacturing cost base means gross margin swings 5+ points with volume.")
print(f"  This is the same mechanism that made 2023-24 painful and made the current recovery so sharp.")

# DATA CENTER / CAPACITY CHECK
print()
print(f"  DATA CENTER & CAPACITY CHECK  (the TI-specific angle):")
print(f"  2025 AI/data-center revenue:     ~${DC_REVENUE_2025_B:.1f}B  (~9% of total sales)")
print(f"  Q2 2026 data-center YoY growth:  {DC_GROWTH_Q2_YOY}")
print(f"  FY2026 capex guidance:            ${CAPEX_GUIDE_LOW_B:.0f}-${CAPEX_GUIDE_HIGH_B:.0f}B  (down from the $4-5B/yr prior build-out pace)")
print(f"  TTM free cash flow:               ${TTM_FCF_B:.1f}B")
print()
print(f"  The capex discipline matters as much as the growth number. TI spent through 2022-2024")
print(f"  building capacity ahead of demand, which crushed free cash flow and the stock through")
print(f"  the down-cycle. Growing into that capacity now — rather than building more of it — is")
print(f"  why FCF has recovered to ${TTM_FCF_B:.1f}B even as revenue accelerates. This cycle is being funded")
print(f"  differently than the last one.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_gm  = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 61% GM):        +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*28:.2f}/share at 28× P/E")
print(f"  Every 1pp of gross margin:            +${eps_per_1pp_gm:.3f}/EPS  = +${eps_per_1pp_gm*28:.2f}/share at 28× P/E")
print(f"  Every 1 turn of P/E:                  ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (revenue growth / industrial / data-center / margin / capex / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<38}  {'BEAR':>7}  {'BASE':>9}  {'BULL':>10}  {'XBULL':>10}  {'NOW':>13}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<38}  {ths[0]:>7}  {ths[1]:>9}  {ths[2]:>10}  {ths[3]:>10}  {s['now']:>13}  {lbl}  {b}")
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
print(f"  {'Signal':<30}  {'Current':>10}  {'Bear val':>10}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Total revenue YoY",          "+23%",    "<8%",     "-15pp",  "Industrial/auto customers over-ordered into the recovery, then correct again"),
    ("Industrial revenue YoY",     "+30%",    "<10%",    "-20pp",  "Global manufacturing PMI rolls over; the 2023-24 inventory cycle repeats"),
    ("Data-center revenue growth", "~2x YoY", "flat",    "stalls", "Hyperscaler capex pauses; analog power content per rack doesn't scale as modeled"),
    ("Gross margin",               "61%",     "<52%",    "-9pp",   "Utilization collapses as revenue reverses; largely fixed cost base bites hard"),
    ("Capex discipline",           "$2-3B",   ">$5B",    "+$2-3B", "A renewed capacity build-out ahead of demand repeats the 2022-24 FCF squeeze"),
    ("Forward P/E",                "31.5x",   "≤20x",    "-11.5x", "Multiple resets to the historical average as growth decelerates"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<30}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: TI just delivered a rare cyclical-and-secular combination — a genuine")
print(f"  industrial recovery from a real trough, arriving at the same time as a nascent AI/")
print(f"  data-center revenue stream. The market has rewarded that combination with a one-day")
print(f"  +18% move and a multiple well above TI's own history. The bear case doesn't require")
print(f"  either story to be false — it only requires the market's TIMING assumption (uninterrupted")
print(f"  acceleration from here) to be wrong, which analog's own cyclical history says happens regularly.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS estimate:       ${EPS_FY2026E:.2f}  (Q1 $1.68 + Q2 $2.14 + Q3E ~$2.40 + Q4E ~$2.55)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (TI traded 20-24× forward through the 2023-24 industrial down-cycle)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS, against a 10-year average")
print(f"  closer to 24×. A +{epp_gap_pct:.0f}% premium to the EPP floor is a wide gap for a cyclical name —")
print(f"  it says the market is not just pricing today's recovery, but extrapolating its pace")
print(f"  forward for several years. That extrapolation has been wrong before in this stock.")
print(f"  At a 26× reversion (still above the 10-yr average): ${EPS_FY2026E:.2f} × 26 = ${EPS_FY2026E*26:.0f}  ({(EPS_FY2026E*26/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: growth decelerates toward trend, multiple compresses)")
hr()
print(f"  Conservative FY2028E EPS:  ${CONS_EPS_2YR:.2f}  (~6.9% EPS CAGR — well below the current cyclical growth rate)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (31.5× → 25×; still above the 10-yr average, not a full de-rate)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: a growth deceleration toward trend, paired with only a modest multiple")
print(f"  compression (31.5× → 25×, still above TI's own 10-yr average), produces a SLIGHTLY")
print(f"  NEGATIVE conservative return. That is the model's clearest signal on this name — you are")
print(f"  paying a price today that requires the current growth pace, not merely a good business,")
print(f"  to continue. This is a WATCHLIST, not an AVOID, because the bear case isn't catastrophic")
print(f"  and the dividend is real — but it is a TIMING call, not a valuation gift.")
print(f"  Breakeven at 25× requires FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f} — above this conservative estimate.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.34
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Q1 print reaction:     +18% in one session — the largest one-day move since 2000")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; long growth streak)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (elevated for TI's history; cycle-inflection repricing)")
print(f"  Beta vs S&P 500:      1.10  (analog semis carry real cyclicality even with the dividend anchor)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (a real move, but well within analog's historical range)")
print(f"  → Q3 print is the next test of whether above-guidance beats continue or the pace normalizes.")
print(f"  → Watch industrial PMI data and hyperscaler capex commentary as leading indicators between prints.")
print(f"  → WATCHLIST at current price  |  ACCUMULATE $220–250  |  BUY below $195")

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
print(f"  TI's operating momentum is genuinely strong across every signal the model tracks. The")
print(f"  valuation signal is the one exception, and it carries real weight: 31.5× forward is not")
print(f"  a multiple TI has historically sustained through a full cycle. WATCHLIST reflects a")
print(f"  good business at a price with limited room for anything less than continued acceleration.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q3 2026 print — a third straight above-guidance beat would justify more of the premium")
print(f"  (2) Industrial PMI / global manufacturing data — the leading indicator for the core cyclical business")
print(f"  (3) Data-center revenue disclosure — needs to keep scaling in dollar terms, not just percentage terms")
print(f"  (4) Gross margin trajectory — the cleanest read on capacity utilization and the cycle's maturity")
print(f"  (5) Any capex guidance change — a return to $4-5B/yr would signal management sees more room to run")
print(f"  WATCHLIST at ${CURRENT_PRICE:.2f}  |  ACCUMULATE $220–250  |  BUY below $195")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  Data-center: ~{DC_REVENUE_2025_B:.0f}%+ of rev, growing")
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
