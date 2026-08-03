"""
MRVL  ·  Marvell Technology, Inc.  ·  NASDAQ: MRVL
Bottom-up signal model  ·  AI Custom Silicon (ASIC) / Optical Interconnect / Data Center
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "MRVL"
COMPANY       = "Marvell Technology, Inc."
SECTOR        = "AI Custom Silicon (ASIC) · Optical Interconnect · Data Center · NASDAQ: MRVL"
CURRENT_PRICE = 187.56       # USD; close 2026-07-31 (verified live)
VOL_52W_LOW   =  61.44       # 2025 trough
VOL_52W_HIGH  = 329.88       # 2026 cycle high — the stock has already round-tripped hugely within this range
SHARES_OUT_M  = 876.0        # millions; $164.3B mkt cap / $187.56
ANNUAL_DIV    = 0.24         # $/share ($0.06/quarter); token payout, capital skews to buybacks/R&D

# ── SEGMENT REVENUE BRIDGE (FY2027E, $B; fiscal year ends ~Jan 2027) ─────────
# Q1 FY2027 actual: revenue $2.418B (above guide midpoint), non-GAAP EPS $0.80.
# Q2 FY2027 guide: $2.700B ±5%, EPS $0.93 ±$0.05 (~35% YoY). Data center ~75% of revenue.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Data Center (AI custom silicon/ASIC/optical)", 8.55, 6.00, 11.50, "50+ custom AI design wins; custom chip business targeted at $10B+ by FY2029"),
    ("Enterprise Networking + Carrier Infrastructure", 2.20, 1.80,  2.70, "Cyclical, steadier than data center; recovering off a soft prior cycle"),
    ("Consumer + Automotive/Industrial",               0.65, 0.50,  0.90, "Small, non-strategic tail; not a growth driver either direction"),
]

# Margin assumptions (non-GAAP)
GROSS_MARGIN_CURR = 0.620   # FY2027E blended non-GAAP gross margin
GROSS_MARGIN_BULL = 0.650   # BULL: custom silicon mix keeps improving margin as programs scale
OPEX_FIXED_B      = 3.60    # R&D + SG&A ($B)
TAX_RATE          = 0.050   # low effective non-GAAP tax rate (international mix)

# ── HYPERSCALER CONCENTRATION CALCULATOR (the Marvell-specific angle) ────────
DC_PCT_OF_REVENUE     = 75    # % of total revenue from Data Center, Q1 FY2027
CUSTOM_DESIGN_WINS    = 50    # named custom AI silicon design wins (cumulative)
CUSTOM_TARGET_FY2029_B = 10   # $B custom-chip business target by FY2029
Q2_GUIDE_YOY_PCT      = 35    # % YoY growth implied by the Q2 FY2027 revenue guide

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 3.75         # $/share non-GAAP FY2027E; Q1 $0.80 + Q2 guide $0.93 + Q3E ~$1.00 + Q4E ~$1.02
PE_PESSIMISTIC = 20.0         # trough P/E: MRVL traded near this level at the 2025 hyperscaler-concentration
                              # scare low; 20x prices a comparable renewed customer-concentration episode
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2029E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 1.24, 20,   25, "A key hyperscaler customer in-sources or dual-sources away; custom-silicon concentration risk materializes"),
    "BASE":  ( 4.60, 42,  193, "Data center AI custom silicon keeps compounding at a more moderate pace; design-win pipeline converts as guided"),
    "BULL":  ( 6.28, 45,  283, "Custom chip business scales toward the $10B+ FY2029 target ahead of schedule; multiple re-expands toward prior highs"),
    "XBULL": ( 7.50, 50,  375, "Marvell becomes the clear #2 merchant AI-silicon platform behind Broadcom; a new all-time high"),
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
        "thresholds": ("<15%",   "≥25%",   "≥35%",   "≥50%"),
        "now":        "~35%",
        "score":      3,
        "comment":    "Q2 FY2027 guide implies +35% YoY; management is 'significantly raising' both FY2027 and FY2028 outlooks",
    },
    {
        "name":       "Data Center revenue mix",
        "weight":     0.20,
        "thresholds": ("<50%",   "≥60%",   "≥70%",   "≥80%"),
        "now":        "~75%",
        "score":      3,
        "comment":    "Three-quarters of revenue now rides on AI infrastructure demand — the growth engine, and the concentration risk",
    },
    {
        "name":       "Custom AI silicon design wins",
        "weight":     0.15,
        "thresholds": ("<20",    "≥35",    "≥50",    "≥70"),
        "now":        "50+",
        "score":      3,
        "comment":    "50+ named design wins is real breadth, not a one- or two-customer story, though revenue is still concentrated",
    },
    {
        "name":       "Non-GAAP gross margin",
        "weight":     0.15,
        "thresholds": ("<55%",   "≥60%",   "≥64%",   "≥68%"),
        "now":        "~62%",
        "score":      2,
        "comment":    "Solid and stable; custom-silicon mix should lift this further as programs scale, but hasn't dramatically yet",
    },
    {
        "name":       "Forward P/E vs history",
        "weight":     0.15,
        "thresholds": (">65x",   "≤50x",   "≤35x",   "≤25x"),
        "now":        "~50x",
        "score":      2,
        "comment":    "~50× FY2027E — down sharply from the cycle-high multiple at the 52-week high, but still a real growth premium",
    },
    {
        "name":       "Price stability (realized volatility)",
        "weight":     0.15,
        "thresholds": ("extreme","high",   "moderate","low"),
        "now":        "extreme",
        "score":      1,
        "comment":    "A 52-week range of $61-$330 is a 5.4x peak-to-trough swing — this is a fundamentally high-beta stock, priced or not",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Design-win breadth — 50+ named custom AI silicon programs; not a single-customer story on paper", +0.6, 0.20),
    ("-", "Revenue concentration — ~75% of revenue is Data Center, and within that a handful of hyperscalers dominate", -0.7, 0.20),
    ("+", "Valuation reset — ~50× forward vs a much richer multiple at the 52-week high; real de-risking already happened", +0.5, 0.15),
    ("-", "Extreme historical volatility — a 5.4x 52-week range means the market has already proven it will reprice this stock violently", -0.6, 0.20),
    ("+", "Guidance raised, not cut — management explicitly raising both FY2027 and FY2028 outlooks on 'exceptional AI bookings'", +0.5, 0.15),
    ("-", "Custom silicon margins still developing — gross margin hasn't yet shown the step-change scale should eventually deliver", -0.3, 0.10),
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
CONS_EPS_2YR  = 5.00    # conservative FY2029E: ~15.5% EPS CAGR — a sharp deceleration from the current ~35% pace
CONS_PE_2YR   = 30      # multiple compresses from ~50× today toward a still-generous growth-semiconductor level
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  AI Custom Silicon / Optical Interconnect / Data Center")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))
print(f"  ⚠ Q2 FY2027 results due 2026-08-20 — the quarter is already guided; figures below use Q1")
print(f"  FY2027 actuals and the company's Q2 guide.")

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2027E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<44}  {'FY2027E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<44}  ${curr:>11.2f}  ${bear:>8.2f}  ${bull:>8.2f}  {bear-curr:>+7.2f}  {bull-curr:>+7.2f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<44}  ${curr_total:>11.2f}  ${bear_total:>8.2f}  ${bull_total:>8.2f}  {bear_total-curr_total:>+7.2f}  {bull_total-curr_total:>+7.2f}")
print(f"  Q1 FY2027 actual: $2.418B (above guide midpoint). Q2 guide: $2.700B ±5% (+{Q2_GUIDE_YOY_PCT}% YoY)")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_eps  = round(curr_oi * (1 - TAX_RATE) / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B * 1.15
shares_b  = shares * 0.98
bull_eps_imp = round(bull_oi * (1 - TAX_RATE) / shares_b, 2)

bear_gp   = bear_total * 0.550     # margin compresses if the mix shifts away from custom silicon
bear_oi   = bear_gp - OPEX_FIXED_B * 0.95
bear_eps_imp = round(max(0, bear_oi) * (1 - TAX_RATE) / shares, 2)

print(f"  FY2027E EPS check:  ${curr_total:.2f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex")
print(f"  − {TAX_RATE*100:.1f}% tax  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2027E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − opex, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 45× = ~${bull_eps_imp*45:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B rev × 55.0% GM (mix shifts away from custom silicon) − opex")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 20× trough = ~${bear_eps_imp*20:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")
print()
print(f"  ⚠ THE STRUCTURAL POINT: Data Center is {SEG_DATA[0][1]/curr_total*100:.0f}% of revenue, and within that a handful of")
print(f"  hyperscaler programs dominate. The bear/bull revenue spread ({(bull_total/bear_total-1)*100:.0f}%) is almost entirely")
print(f"  a function of whether 2-3 large custom-silicon programs scale as designed or get renegotiated.")

# HYPERSCALER CONCENTRATION CHECK
print()
print(f"  HYPERSCALER CONCENTRATION CHECK  (the Marvell-specific angle):")
print(f"  Data Center % of revenue:       {DC_PCT_OF_REVENUE}%  (Q1 FY2027)")
print(f"  Custom AI silicon design wins:  {CUSTOM_DESIGN_WINS}+  (cumulative, named programs)")
print(f"  Custom chip revenue target:     ~${CUSTOM_TARGET_FY2029_B}B  by FY2029")
print(f"  Q2 FY2027 guide implies:        +{Q2_GUIDE_YOY_PCT}% YoY growth")
print()
print(f"  50+ design wins is genuine breadth — this is not literally a one-customer story. But")
print(f"  revenue recognition on custom silicon programs is lumpy and concentrated in whichever")
print(f"  handful of programs have reached volume production. The stock's own 52-week history —")
print(f"  a 5.4x round trip — is direct evidence of how violently the market reprices this name")
print(f"  when a single hyperscaler relationship comes into question.")

# KEY SENSITIVITIES
print()
eps_per_1B_dc   = 1.0 * 0.68 * (1 - TAX_RATE) / shares   # data center incremental margin ~68%
eps_per_1pp_gm  = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Data Center revenue (68% inc. margin):  +${eps_per_1B_dc:.3f}/EPS  = +${eps_per_1B_dc*35:.2f}/share at 35× P/E")
print(f"  Every 1pp of blended gross margin:                +${eps_per_1pp_gm:.3f}/EPS  = +${eps_per_1pp_gm*35:.2f}/share at 35× P/E")
print(f"  Every 1 turn of P/E:                              ±${EPS_FY2027E:.2f}/share  ({EPS_FY2027E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (revenue growth / DC mix / design wins / margin / valuation / volatility)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<38}  {'BEAR':>7}  {'BASE':>7}  {'BULL':>7}  {'XBULL':>7}  {'NOW':>8}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<38}  {ths[0]:>7}  {ths[1]:>7}  {ths[2]:>7}  {ths[3]:>7}  {s['now']:>8}  {lbl}  {b}")
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
    ("Total revenue YoY",           "~35%",   "<15%",    "-20pp",  "A top hyperscaler customer pauses or renegotiates a custom-silicon program"),
    ("Data Center revenue mix",     "~75%",   "<50%",    "-25pp",  "Concentration itself becomes the catalyst as one program's decline dominates"),
    ("Custom design win conversion","50+",    "stalls",  "flat",   "Design wins don't convert to volume production on the modeled timeline"),
    ("Non-GAAP gross margin",       "~62%",   "<55%",    "-7pp",   "Mix shifts back toward lower-margin networking/carrier as data center slows"),
    ("Forward P/E",                 "~50x",   "≤20x",    "-30x",   "Market fully re-prices custom-silicon concentration risk, as it has before"),
    ("Realized volatility",         "extreme","extreme", "same",   "This stock's beta doesn't change — the direction of the next big move does"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: this is a concentration story wearing a diversification narrative. 50+")
print(f"  design wins sounds diversified; the REVENUE is still concentrated in whichever 2-3")
print(f"  programs have reached scale. The 52-week round trip from $61 to $330 and back to $188")
print(f"  is not a fluke — it is what happens to this stock every time the market updates its")
print(f"  view on a single major customer relationship. That pattern should be the base-rate")
print(f"  expectation for volatility here, not a tail-risk footnote.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2027E non-GAAP EPS:       ${EPS_FY2027E:.2f}  (Q1 $0.80 + Q2 guide $0.93 + Q3E ~$1.00 + Q4E ~$1.02)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (near where MRVL traded at the 2025 concentration-scare low)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E non-GAAP EPS — well down from the")
print(f"  multiple implied at the 52-week high of ${VOL_52W_HIGH:.2f}. Real de-risking has already happened")
print(f"  in the price. The question the EPP gap can't answer is whether the NEXT concentration")
print(f"  scare — and this stock's history says there will be one — takes the multiple back toward")
print(f"  the {PE_PESSIMISTIC:.0f}× trough or stops well short of it.")
print(f"  At a 30× reversion (a real but partial re-rating): ${EPS_FY2027E:.2f} × 30 = ${EPS_FY2027E*30:.0f}  ({(EPS_FY2027E*30/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: growth decelerates sharply, multiple compresses)")
hr()
print(f"  Conservative FY2029E EPS:  ${CONS_EPS_2YR:.2f}  (~15.5% EPS CAGR — a sharp deceleration from the current ~35% pace)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~50× → 30×; still a real growth-semiconductor premium)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, token yield)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: a sharp growth deceleration (still ~15.5%/yr EPS growth — not a collapse)")
print(f"  paired with a real multiple compression to a still-generous 30× produces a NEGATIVE")
print(f"  conservative return of {cons_annual:.1f}%/yr. That is a genuine signal: at ${CURRENT_PRICE:.2f}, you need the")
print(f"  growth story to keep compounding near its current pace, not merely decelerate gracefully,")
print(f"  for this to work. Combined with a 5.4x 52-week trading range, the PATH to any 2-year")
print(f"  outcome here is likely to be extremely volatile even when the destination is reasonable.")
print(f"  Breakeven at 30× requires FY2029E EPS ≥ ${CURRENT_PRICE / CONS_PE_2YR:.2f} — above this conservative estimate.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.65
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (a 5.4x peak-to-trough range — extreme even for AI semis)")
print(f"  Position in range:     {vol_pct*100:.0f}th percentile")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (token yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; not an income holding)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (among the highest of any large-cap semiconductor name)")
print(f"  Beta vs S&P 500:      2.10  (extreme sensitivity to both AI-capex sentiment and single-customer news)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (well within this stock's demonstrated one-year range)")
print(f"  → Q2 FY2027 results (Aug 20) are the next major catalyst — watch Data Center revenue vs the guide.")
print(f"  → Any hyperscaler commentary on custom-silicon program pace moves this stock more than almost any peer.")
print(f"  → WATCHLIST at current price  |  ACCUMULATE $130–155  |  BUY below $100")

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
print(f"  Marvell's design-win breadth and raised guidance are genuinely encouraging. But this")
print(f"  stock has already demonstrated — twice within one 52-week window — that sentiment on")
print(f"  hyperscaler concentration can swing violently in either direction. WATCHLIST reflects a")
print(f"  reasonable price for a business whose PATH to any outcome is unusually uncertain.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q2 FY2027 results (Aug 20, 2026) — Data Center revenue and any updated custom-silicon commentary")
print(f"  (2) Any single hyperscaler customer news — this is the highest-beta catalyst category for this stock")
print(f"  (3) Gross margin trajectory — the clearest read on whether custom silicon mix is truly accretive yet")
print(f"  (4) Progress toward the $10B+ FY2029 custom-chip revenue target")
print(f"  (5) Broader AI-capex sentiment — MRVL trades as a high-beta proxy for the sector, not just its own numbers")
print(f"  WATCHLIST at ${CURRENT_PRICE:.2f}  |  ACCUMULATE $130–155  |  BUY below $100")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2027E EPS: ${EPS_FY2027E:.2f}  |  Design wins: {CUSTOM_DESIGN_WINS}+")
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
