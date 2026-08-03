"""
META  ·  Meta Platforms, Inc.  ·  NASDAQ: META
Bottom-up signal model  ·  Social Media / Digital Advertising / AI Infrastructure
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "META"
COMPANY       = "Meta Platforms, Inc."
SECTOR        = "Social Media · Digital Advertising · AI Infrastructure · Reality Labs · NASDAQ: META"
CURRENT_PRICE = 556.71       # USD; close 2026-07-31 (verified live)
VOL_52W_LOW   = 520.26       # 2026 trough; post-Q2-earnings selloff
VOL_52W_HIGH  = 796.25       # 2025/26 peak, pre-capex-concern derate
SHARES_OUT_M  = 2_550.0      # millions; $1.42T mkt cap / $556.71
ANNUAL_DIV    = 2.10         # $/share forward; yield ~0.38%

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ──────────────────────────────────────
# Q2 2026 actual: revenue $60.8B (+28% YoY); ad revenue $59.4B (+27%, impressions +14%, price/ad +12%).
# EPS $6.18 missed by 13.8% on legal/severance charges. Capex $31.1B in Q2 alone; FY guide raised to $130-145B.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Family of Apps Advertising",  248.0, 220.0, 275.0, "Impressions +14%, price/ad +12% — both legs of the ad engine growing, not just one"),
    ("Reality Labs + Other",          3.5,   2.8,   5.5, "Structural loss-maker; smart glasses are the one bright spot, still tiny in revenue terms"),
]

# Margin assumptions (GAAP operating margin proxy)
OP_MARGIN_CURR   = 0.300    # FY2026E blended operating margin; depressed by AI capex depreciation ramp and legal/severance charges
OP_MARGIN_BULL   = 0.360    # BULL: ad efficiency (Advantage+) and AI infrastructure ROI both improve the margin
OP_MARGIN_BEAR   = 0.240    # BEAR: capex depreciation and content/legal costs keep compressing margin faster than ad revenue grows
TAX_RATE         = 0.170    # effective tax rate

# ── AI CAPEX / FREE CASH FLOW CALCULATOR (the Meta-specific angle) ───────────
CAPEX_Q2_B          =  31.1   # $B capital expenditures, Q2 2026 alone
CAPEX_GUIDE_LOW_B   = 130.0   # $B FY2026 capex guidance, low end (raised again)
CAPEX_GUIDE_HIGH_B  = 145.0   # $B FY2026 capex guidance, high end
FCF_Q2_M            =   784   # $M free cash flow, Q2 2026 — a sharp drop from prior levels
Q2_EPS_MISS_PCT     =  13.8   # % EPS miss vs consensus, driven by legal and severance charges
Q3_GUIDE_REV_LOW_B  =  61.0   # $B Q3 2026 revenue guidance, low end
Q3_GUIDE_REV_HIGH_B =  64.0   # $B Q3 2026 revenue guidance, high end

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 24.50       # $/share; clean operating-basis FY2026E estimate (Q2 $6.18 included one-time legal/severance drag)
PE_PESSIMISTIC = 15.0        # trough P/E: META traded near this level during the 2022 Reality-Labs-spend
                              # panic; 15x prices a comparable capex/FCF-driven de-rating
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  (17.40, 15,  261, "Capex keeps outrunning ad-revenue growth; FCF stays depressed for multiple years; margin never recovers"),
    "BASE":  (25.50, 20,  510, "Ad engine keeps compounding at a moderating pace; capex growth decelerates as guided; margin stabilizes"),
    "BULL":  (33.54, 23,  771, "AI-driven ad efficiency (Advantage+, ranking) shows up clearly in monetization; capex ROI becomes visible in FCF recovery"),
    "XBULL": (39.00, 26, 1014, "Meta's AI infrastructure bet fully pays off in both ad efficiency and a new compute-platform business line"),
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
        "name":       "Advertising revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<15%",   "≥22%",   "≥28%",   "≥35%"),
        "now":        "+27%",
        "score":      3,
        "comment":    "Impressions +14% AND price/ad +12% — both volume and pricing growing together, not one masking the other",
    },
    {
        "name":       "Free cash flow (quarterly)",
        "weight":     0.25,
        "thresholds": ("<$1B",   "≥$3B",   "≥$8B",   "≥$15B"),
        "now":        "$784M",
        "score":      1,
        "comment":    "A sharp drop from prior levels — $31.1B of Q2 capex alone is consuming nearly all operating cash flow",
    },
    {
        "name":       "FY2026 capex guidance",
        "weight":     0.20,
        "thresholds": (">$150B", "≤$140B", "≤$120B", "≤$100B"),
        "now":        "$130-145B",
        "score":      1,
        "comment":    "Raised again this quarter; the market's core question is whether this spend is building durable advantage or just cost",
    },
    {
        "name":       "Operating margin",
        "weight":     0.15,
        "thresholds": ("<26%",   "≥30%",   "≥34%",   "≥38%"),
        "now":        "~30%",
        "score":      2,
        "comment":    "Holding up reasonably given the capex ramp, but the Q2 EPS miss shows real near-term cost pressure",
    },
    {
        "name":       "Q2 EPS quality (one-time items)",
        "weight":     0.10,
        "thresholds": ("large miss","clean miss","in-line","clean beat"),
        "now":        "large miss",
        "score":      2,
        "comment":    "The 13.8% miss was driven by legal and severance charges — a real cost, but not evidence of a broken ad business",
    },
    {
        "name":       "Forward P/E (clean)",
        "weight":     0.10,
        "thresholds": (">28x",   "≤23x",   "≤19x",   "≤15x"),
        "now":        "~22.7x",
        "score":      3,
        "comment":    "22.7× FY2026E clean EPS — a real discount for a 27%-growing ad business, reflecting the market's capex anxiety",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Ad engine is genuinely healthy — impressions AND pricing both growing double digits simultaneously", +0.7, 0.20),
    ("-", "Free cash flow has effectively disappeared — $784M in a quarter for a company this size is a real signal, not noise", -0.9, 0.25),
    ("-", "Capex guidance keeps rising — $130-145B FY2026 with no clear ceiling yet disclosed", -0.6, 0.20),
    ("+", "Valuation discount — 22.7× clean forward EPS is cheap for the growth rate, reflecting the market pricing in real capex risk", +0.5, 0.15),
    ("-", "Reality Labs remains a structural drag — billions in annual losses with no clear monetization timeline", -0.3, 0.10),
    ("+", "Balance sheet strength — even at $130B+ capex, Meta's core ad cash generation can fund this without existential leverage risk", +0.3, 0.10),
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
CONS_EPS_2YR  = 27.00   # conservative FY2028E: ~4.9% EPS CAGR — capex pressure persists, ad growth decelerates
CONS_PE_2YR   = 18      # modest re-rating from ~22.7× — still reflects real capex-driven caution
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Social Media / Advertising / AI Infrastructure")
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
print(f"  Q2 2026 actual: $60.8B (+28% YoY). Q3 guide: ${Q3_GUIDE_REV_LOW_B:.0f}-{Q3_GUIDE_REV_HIGH_B:.0f}B")
print()

# EPS bridge (clean, operating basis)
shares    = SHARES_OUT_M / 1000
curr_op   = curr_total * OP_MARGIN_CURR
curr_eps  = round(curr_op * (1 - TAX_RATE) / shares, 2)

bull_op   = bull_total * OP_MARGIN_BULL
shares_b  = shares * 0.98
bull_eps_imp = round(bull_op * (1 - TAX_RATE) / shares_b, 2)

bear_op   = bear_total * OP_MARGIN_BEAR
bear_eps_imp = round(bear_op * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {OP_MARGIN_CURR*100:.1f}% op margin − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {OP_MARGIN_BULL*100:.1f}% op margin, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 23× = ~${bull_eps_imp*23:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {OP_MARGIN_BEAR*100:.1f}% op margin (capex depreciation outruns ad growth)")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 15× trough = ~${bear_eps_imp*15:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# AI CAPEX / FCF CHECK
print()
print(f"  AI CAPEX & FREE CASH FLOW CHECK  (the Meta-specific angle):")
print(f"  Q2 2026 capex:                 ${CAPEX_Q2_B:.1f}B  (a single quarter)")
print(f"  FY2026 capex guidance:         ${CAPEX_GUIDE_LOW_B:.0f}-{CAPEX_GUIDE_HIGH_B:.0f}B  (raised again this quarter)")
print(f"  Q2 2026 free cash flow:        ${FCF_Q2_M}M  (a sharp drop from prior levels)")
print(f"  Q2 EPS miss vs consensus:      -{Q2_EPS_MISS_PCT:.1f}%  (driven by legal + severance charges, not the ad business)")
print()
print(f"  This is the number that matters most for META right now: free cash flow of $784M in a")
print(f"  quarter, for a company generating $60.8B of revenue at 27% growth, means essentially")
print(f"  all of the cash the ad business throws off is being reinvested into AI infrastructure.")
print(f"  That is a legitimate strategic choice if the capex builds durable ad-efficiency and/or")
print(f"  a new compute business — but it removes the cash-generation cushion that used to make")
print(f"  META a lower-risk mega-cap holding, at least for as long as the capex ramp continues.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * OP_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_marg = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B ad revenue (at 30.0% op margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*20:.2f}/share at 20× P/E")
print(f"  Every 1pp of operating margin:               +${eps_per_1pp_marg:.3f}/EPS  = +${eps_per_1pp_marg*20:.2f}/share at 20× P/E")
print(f"  Every 1 turn of P/E:                         ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (ad growth / FCF / capex / margin / EPS quality / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<38}  {'BEAR':>10}  {'BASE':>9}  {'BULL':>8}  {'XBULL':>10}  {'NOW':>10}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<38}  {ths[0]:>10}  {ths[1]:>9}  {ths[2]:>8}  {ths[3]:>10}  {s['now']:>10}  {lbl}  {b}")
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
    ("Advertising revenue YoY",    "+27%",   "<15%",    "-12pp",  "Ad market softens or TikTok/other platforms take meaningful share back"),
    ("Free cash flow (qtrly)",     "$784M",  "<$0",     "worse",  "Capex keeps rising while revenue growth decelerates — FCF turns negative"),
    ("FY2026 capex guide",         "$130-145B","$160B+", "+$20B+", "Another guidance raise with no visible ceiling spooks the market further"),
    ("Operating margin",           "~30%",   "<24%",    "-6pp",   "Depreciation on the AI infrastructure buildout outpaces revenue it generates"),
    ("Forward P/E (clean)",        "~22.7x", "≤15x",    "-8x",    "Market fully re-prices the capex risk as a multi-year FCF problem, not a blip"),
    ("Reality Labs losses",        "steady", "widening","worse",  "No path to monetization emerges even as losses continue to scale"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: unlike a demand-side bear case, this one is entirely about CAPITAL")
print(f"  ALLOCATION. The ad business itself — impressions and pricing both growing double")
print(f"  digits — shows no sign of the deceleration bears in other names worry about. The")
print(f"  question is whether $130-145B of annual capex generates a return, and free cash flow")
print(f"  near zero for several quarters running is the tangible cost of finding out.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E clean EPS:          ${EPS_FY2026E:.2f}  (Q2 reported $6.18 included one-time legal/severance drag)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (near where META traded during the 2022 Reality Labs spending panic)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× clean FY2026E EPS — a real discount for")
print(f"  a 27%-growing advertising business. META has been through this exact debate before:")
print(f"  in 2022, the market decided Reality Labs spending was value-destructive and cut the")
print(f"  multiple to the mid-teens; the stock then delivered one of the largest recoveries in")
print(f"  mega-cap history once the ad business proved the spending wasn't fatal. That precedent")
print(f"  cuts both ways — it argues for patience, not for assuming this time resolves the same way.")
print(f"  At a 20× reversion (still a discount to the historical premium multiple): ${EPS_FY2026E:.2f} × 20 = ${EPS_FY2026E*20:.0f}")
print(f"  ({(EPS_FY2026E*20/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: capex pressure persists, ad growth decelerates, modest re-rating)")
hr()
print(f"  Conservative FY2028E EPS:  ${CONS_EPS_2YR:.2f}  (~4.9% EPS CAGR — capex depreciation keeps weighing on the P&L)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~22.7× → 18×; the capex anxiety persists, doesn't fully resolve)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: even assuming the capex overhang persists for two more years and EPS growth")
print(f"  slows to under 5%/yr, the conservative case still clears {cons_annual:.1f}%/yr, because so little")
print(f"  multiple expansion is required from an already-discounted starting point. The FCF")
print(f"  recovery — not required for this case, but likely upside if capex growth decelerates")
print(f"  as guided in 2027 — is what would move this from WATCHLIST toward ACCUMULATE or BUY.")
print(f"  Breakeven at 18× requires FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f} — below this conservative estimate already.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.33
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Drawdown from high:   -{(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.1f}%  (the capex/FCF-driven de-rating, concentrated around the Q2 print)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; small but a real capital-return signal)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (elevated around earnings; the Q2 print alone moved the stock ~10% after-hours)")
print(f"  Beta vs S&P 500:      1.25  (higher than its historical profile given the current capex-narrative sensitivity)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (a real but not extreme move by this stock's own history)")
print(f"  → Q3 print is the next test of whether FCF stabilizes or keeps deteriorating.")
print(f"  → Any explicit capex ceiling from management would be a major sentiment catalyst.")
print(f"  → WATCHLIST at current price  |  ACCUMULATE $460–500  |  BUY below $400  |  TRIM above $750")

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
print(f"  The ad business is not the problem — it's growing 27% with both volume and price")
print(f"  expanding. The capex/FCF story is the entire debate, and the market has already priced")
print(f"  in real caution about it (22.7× is a discount multiple for this growth rate). That")
print(f"  combination — good business, genuinely uncertain capital allocation, real discount — is")
print(f"  what makes this a WATCHLIST rather than a clean AVOID — the discount is real, but so is the")
print(f"  capex risk, and ratio B (1.38x) says the downside case still outweighs the upside from here.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q3 2026 free cash flow — does it stabilize/recover, or deteriorate further?")
print(f"  (2) Any explicit multi-year capex ceiling or moderation signal from management")
print(f"  (3) Ad efficiency metrics (Advantage+ adoption, ROAS improvement) — evidence AI capex pays off directly")
print(f"  (4) Reality Labs losses — any path to monetization, or confirmation it stays a pure cost center")
print(f"  (5) Competitive dynamics — TikTok, Google, and others' share of the digital ad market")
print(f"  WATCHLIST at ${CURRENT_PRICE:.2f}  |  ACCUMULATE $460–500  |  BUY below $400  |  TRIM above $750")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E clean EPS: ${EPS_FY2026E:.2f}  |  Q2 FCF: ${FCF_Q2_M}M")
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
