"""
LRCX  ·  Lam Research Corporation  ·  NASDAQ: LRCX
Bottom-up signal model  ·  Semiconductor Capital Equipment / Etch & Deposition / AI Fab Buildout
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "LRCX"
COMPANY       = "Lam Research Corporation"
SECTOR        = "Semiconductor Capital Equipment · Etch & Deposition · WFE · NASDAQ: LRCX"
CURRENT_PRICE = 298.06      # USD; up +1.56% intraday 2026-08-03, still digesting the +18% post-Q4-earnings pop
VOL_52W_LOW   = 90.94       # 2025/26 trough
VOL_52W_HIGH  = 438.50      # 2026 AI-fab-buildout peak
SHARES_OUT_M  = 1_254.0     # millions; $373.72B mkt cap / $298.06
ANNUAL_DIV    = 2.40        # $/share FY2027E; steadily growing capital-return program

# ── SEGMENT REVENUE BRIDGE (FY2027E, $B) ──────────────────────────────────────
# FY2026 (ended June) actual: revenue $23.23B (+26% YoY), GM 50.6%, diluted EPS $5.82 (+41% YoY).
# Q4 FY2026 (June qtr) actual: revenue $6.72B (record, +15% seq/+30% YoY), GM 52% (20-yr high),
# op margin 38.4% (record), EPS $1.82 (beat $1.68 est). Q1 FY2027 (Sept qtr) guide: revenue
# $8.1B±$400M (+20%+ seq), GM 52%±1pp, op margin 39.5%±1pp, EPS $2.15±$0.15. CY2026 WFE outlook
# raised to the low-$150B range (from $140B); 2027 setup described by management as "extraordinary."
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Systems  (deposition/etch)", 21.82, 11.5, 28.0, "The AI-fab capex engine; most exposed to a WFE cyclical downturn in the bear case"),
    ("CSBG  (support/spares/service)", 11.75, 6.5, 14.0, "Recurring, installed-base-driven revenue; falls less than Systems in a downturn but still cyclical"),
]

# Operating-margin assumptions (semicap opex scales with the cycle far less than revenue does)
OP_MARGIN_CURR = 0.395   # FY2027E; matches the Q1 FY2027 guide (39.5% ±1pp) and Q4 FY2026 record trajectory
OP_MARGIN_BEAR = 0.200   # BEAR: WFE downturn — utilization drops, R&D/SG&A don't cut proportionally, echoing Lam's 2023 trough
OP_MARGIN_BULL = 0.430   # BULL: further operating leverage as the AI-fab buildout extends into FY2028
TAX_RATE       = 0.130   # effective tax rate

# ── WFE CYCLE CALCULATOR (the Lam-specific angle) ─────────────────────────────
WFE_2026_OUTLOOK_LOW_B  = 150   # $B; CY2026 WFE spending outlook, raised from $140B
WFE_2026_OUTLOOK_PRIOR_B= 140   # $B; prior CY2026 WFE outlook before the raise
Q1_FY27_GUIDE_REV_B     = 8.1   # $B; September-quarter revenue guide
Q1_FY27_GUIDE_SEQ_GROWTH_PCT = 20.5  # % sequential growth implied by the Q1 FY2027 guide
POST_EARNINGS_POP_PCT   = 18    # % single-day stock pop on the Q4 FY2026 print

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 9.20        # $/share FY2027E; derived from the revenue bridge below off the "extraordinary" 2027 WFE setup
PE_PESSIMISTIC = 16.0        # trough P/E: Lam's own multi-cycle semicap-trough average (WFE stocks re-rate hard at cycle peaks)
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2029E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 2.50, 18,   45,  "WFE spending rolls over into a classic cyclical downturn; utilization and op margin collapse"),
    "BASE":  (10.77, 30,  323,  "WFE holds near the raised $150B+ range; steady share gains in etch/deposition continue"),
    "BULL":  (12.92, 29,  375,  "The AI-fab buildout extends WFE growth into FY2028; operating leverage keeps compounding"),
    "XBULL": (17.94, 31,  556,  "WFE breaks decisively above $175B+ on a multi-year AI/leading-edge capacity supercycle"),
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
        "thresholds": ("<0%",    "≥15%",   "≥25%",   "≥35%"),
        "now":        "+30%",
        "score":      3,
        "comment":    "Q4 FY2026 +30% YoY, fourth straight record quarter — broad-based AI-fab capex strength",
    },
    {
        "name":       "Gross margin trajectory",
        "weight":     0.20,
        "thresholds": ("<44%",   "≥48%",   "≥51%",   "≥54%"),
        "now":        "52%",
        "score":      3,
        "comment":    "20-year high gross margin in Q4 FY2026, guided to hold at 52% in Q1 FY2027",
    },
    {
        "name":       "WFE spending outlook",
        "weight":     0.20,
        "thresholds": ("cuts",   "flat",   "raised",  "sharply raised"),
        "now":        "raised to low-$150Bs",
        "score":      3,
        "comment":    "CY2026 WFE outlook raised from $140B to the low-$150B range; 2027 called 'extraordinary' by management",
    },
    {
        "name":       "Q1 FY2027 guide vs prior run-rate",
        "weight":     0.15,
        "thresholds": ("<0%",    "≥10%",   "≥18%",   "≥25%"),
        "now":        "+20.5%",
        "score":      3,
        "comment":    "$8.1B guide implies >20% sequential growth off an already-record June quarter",
    },
    {
        "name":       "Operating margin trajectory",
        "weight":     0.15,
        "thresholds": ("<30%",   "≥35%",   "≥38%",   "≥42%"),
        "now":        "39.5%",
        "score":      3,
        "comment":    "Record 38.4% in Q4 FY2026, guided to 39.5% in Q1 FY2027 — genuine operating leverage, not just cyclical revenue",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.10,
        "thresholds": (">40x",   "≤32x",   "≤26x",   "≤20x"),
        "now":        "~32.4x",
        "score":      2,
        "comment":    "32.4× FY2027E EPS after an 18% post-earnings pop — a real premium for a highly cyclical equipment name",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "The AI-fab capex buildout has genuine multi-year visibility — management's 'extraordinary' 2027 language is unusually direct", +0.5, 0.20),
    ("-", "WFE is one of the most cyclical end-markets in tech; every prior upcycle has ended in a sharp correction", -0.6, 0.25),
    ("-", "Valuation already reflects an 18% post-earnings pop — the easy re-rating has likely happened", -0.4, 0.15),
    ("+", "Record gross and operating margins reflect real share gains in etch/deposition, not just cyclical volume", +0.4, 0.15),
    ("+", "CSBG's recurring, installed-base revenue cushions the downside versus a pure-Systems equipment peer", +0.3, 0.15),
    ("-", "Customer concentration (a handful of leading-edge fabs) means any single customer's capex pause hits hard", -0.3, 0.10),
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
CONS_EPS_2YR  = 9.80    # conservative FY2029E: modest growth off FY2027E, assumes some cyclical moderation
CONS_PE_2YR   = 22      # a real de-rating from ~32.4× as cycle-peak skepticism sets in
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Etch / Deposition / AI Fab Buildout")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2027E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<32}  {'FY2027E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<32}  ${curr:>11.2f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<32}  ${curr_total:>11.2f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  FY2026 actual: $23.23B (+26%). Q1 FY2027 guide: ${Q1_FY27_GUIDE_REV_B}B±$0.4B (+{Q1_FY27_GUIDE_SEQ_GROWTH_PCT:.1f}% seq)")
print()

# EPS bridge (operating-margin based — semicap opex is sticky, doesn't scale down 1:1 with revenue)
shares    = SHARES_OUT_M / 1000
curr_oi   = curr_total * OP_MARGIN_CURR
curr_eps  = round(curr_oi * (1 - TAX_RATE) / shares, 2)

shares_b  = shares * 0.97
bull_oi   = bull_total * OP_MARGIN_BULL
bull_eps_imp = round(bull_oi * (1 - TAX_RATE) / shares_b, 2)

bear_oi   = bear_total * OP_MARGIN_BEAR
bear_eps_imp = round(max(0, bear_oi) * (1 - TAX_RATE) / shares, 2)

print(f"  FY2027E EPS check:  ${curr_total:.2f}B rev × {OP_MARGIN_CURR*100:.1f}% op margin")
print(f"  − {TAX_RATE*100:.1f}% tax  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2027E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B rev × {OP_MARGIN_BULL*100:.1f}% op margin, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B rev × {OP_MARGIN_BEAR*100:.1f}% op margin (WFE downturn, sticky opex) ")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# WFE CYCLE CHECK
print()
print(f"  WFE CYCLE CHECK  (the Lam-specific angle):")
print(f"  CY2026 WFE outlook:                   ${WFE_2026_OUTLOOK_LOW_B}B+  (raised from ${WFE_2026_OUTLOOK_PRIOR_B}B)")
print(f"  Q1 FY2027 guide vs Q4 FY2026 actual:   +{Q1_FY27_GUIDE_SEQ_GROWTH_PCT:.1f}% sequential — an unusually strong step-up")
print(f"  Post-earnings stock reaction:           +{POST_EARNINGS_POP_PCT}%  (the market has already re-rated the stock once)")
print()
print(f"  Lam sits downstream of the same AI infrastructure buildout that is inflating Micron's DRAM/HBM")
print(f"  pricing power and squeezing Apple's iPhone margins — three different points on the same AI capex")
print(f"  supply chain. The risk is the one that has ended every prior WFE upcycle: customers eventually")
print(f"  digest capacity, utilization falls, and Systems revenue (the high-beta segment) drops hard while")
print(f"  CSBG's recurring base cushions but does not offset the decline.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * OP_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_opm = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 39.5% op margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*30:.2f}/share at 30× P/E")
print(f"  Every 1pp of operating margin:            +${eps_per_1pp_opm:.3f}/EPS  = +${eps_per_1pp_opm*30:.2f}/share at 30× P/E")
print(f"  Every 1 turn of P/E:                      ±${EPS_FY2027E:.2f}/share  ({EPS_FY2027E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (revenue growth / margin / WFE outlook / guide / op leverage / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<38}  {'BEAR':>11}  {'BASE':>7}  {'BULL':>10}  {'XBULL':>14}  {'NOW':>13}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<38}  {ths[0]:>11}  {ths[1]:>7}  {ths[2]:>10}  {ths[3]:>14}  {s['now']:>13}  {lbl}  {b}")
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
    ("Revenue YoY",                 "+30%",   "<0%",     "collapse","Leading-edge customers pause or digest capacity after two years of record capex"),
    ("Gross margin",                "52%",    "<44%",    "-8pp+",  "Utilization drops sharply; fixed manufacturing costs are spread over far less volume"),
    ("WFE spending outlook",        "raised", "cuts",    "reversal","CY2027/28 WFE guidance gets cut as AI-fab capex digestion sets in industry-wide"),
    ("Q-over-Q growth",             "+20.5%", "<0%",     "reversal","Sequential growth reverses as the current order backlog gets worked through"),
    ("Operating margin",            "39.5%",  "<30%",    "-9.5pp+","Sticky R&D/SG&A don't scale down with revenue, compressing margins in the downturn"),
    ("Forward P/E",                 "~32.4x", ">40x",    "re-rate","P/E can rise even as price falls if EPS collapses faster, echoing prior WFE downcycles"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: WFE is a boom-bust category almost by definition — every AI/leading-edge capex cycle")
print(f"  in Lam's history has eventually been followed by a digestion phase. The current cycle's supporting")
print(f"  evidence (raised WFE guidance, 'extraordinary' 2027 commentary, record margins) is genuinely strong,")
print(f"  but none of it repeals the cyclicality — it only pushes the eventual digestion phase further out.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2027E EPS estimate:       ${EPS_FY2027E:.2f}  (off the Q1 FY2027 guide of $2.15±$0.15 and the raised WFE outlook)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (Lam's own multi-cycle semicap-trough average)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS, a real premium after the post-earnings pop.")
print(f"  The EPP floor assumes a full reversion to Lam's historical trough multiple on cycle-peak earnings —")
print(f"  a conservative floor that has historically been tested in every prior WFE downcycle.")
print(f"  At a 24× reversion (a normalized cyclical multiple): ${EPS_FY2027E:.2f} × 24 = ${EPS_FY2027E*24:.0f}  ({(EPS_FY2027E*24/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest growth off FY2027E, some cyclical moderation assumed)")
hr()
print(f"  Conservative FY2029E EPS:  ${CONS_EPS_2YR:.2f}  (roughly flat to FY2027E — assumes the cycle has partly rolled over)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~32.4× → 22×; a real de-rating)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: even a conservative case — flat EPS off the FY2027E base — still comes out")
print(f"  {'positive' if cons_return > 0 else 'negative'} once the multiple de-rates from ~32.4× to a more normal 22×, because that de-rating alone erases")
print(f"  most of the cushion a merely-flat EPS outcome would otherwise provide. This is the honest reason")
print(f"  the signal is {signal_short}, not a higher rating: the stock needs sustained growth, not just stability, to work from here.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.45
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Recent move:           +{POST_EARNINGS_POP_PCT}% on the Q4 FY2026 print/Q1 FY2027 guide")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; growing alongside record profitability)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (high — typical for cyclical semicap equipment names)")
print(f"  Beta vs S&P 500:      1.55  (well above market; a high-beta AI-capex-cycle proxy)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (large but within the range of prior WFE-downcycle drawdowns)")
print(f"  → Q1 FY2027 print (late Oct) is the next test of whether the guide's growth rate is sustained.")
print(f"  → CY2027 WFE spending revisions are the leading indicator to watch between prints.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $230  |  Trim above $420")

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
print(f"  Lam is executing about as well as a semicap company can — record margins, raised WFE guidance,")
print(f"  and genuine operating leverage — but the market has already awarded much of that credit via the")
print(f"  post-earnings pop, and WFE's cyclicality means the multiple carries real downside if the cycle turns.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q1 FY2027 print (late October) — does the +20.5% sequential growth guide hold?")
print(f"  (2) CY2027 WFE spending revisions across the industry — the leading cyclical indicator")
print(f"  (3) Leading-edge customer capex commentary (TSMC, Samsung, Intel, Micron) at their own earnings")
print(f"  (4) Gross/operating margin durability at the 52%/39.5% levels through further volume growth")
print(f"  (5) Any signs of order push-outs or capacity digestion — the first tell of a cycle turn")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $230  |  Trim above $420")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2027E EPS: ${EPS_FY2027E:.2f}  |  CY2026 WFE outlook: ${WFE_2026_OUTLOOK_LOW_B}B+")
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
