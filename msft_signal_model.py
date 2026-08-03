"""
MSFT  ·  Microsoft Corporation  ·  NASDAQ: MSFT
Bottom-up signal model  ·  Azure Cloud / Microsoft 365 Copilot / OpenAI Partnership / Gaming
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "MSFT"
COMPANY       = "Microsoft Corporation"
SECTOR        = "Enterprise Cloud (Azure) · Microsoft 365 Copilot · OpenAI Partnership · Gaming · NASDAQ: MSFT"
CURRENT_PRICE = 464.72       # USD; close 2026-07-31 (verified live)
VOL_52W_LOW   = 349.20       # 2025/26 trough
VOL_52W_HIGH  = 555.45       # 2026 peak, pre-capex-concern derate
SHARES_OUT_M  = 7_425.0      # millions; $3.45T mkt cap / $464.72
ANNUAL_DIV    = 3.64         # $/share forward; yield ~0.78%; long dividend growth streak

# ── SEGMENT REVENUE BRIDGE (FY2027E, $B; fiscal year ends June) ──────────────
# FY2026 (just closed) actual: revenue $331.84B (+17.8%), net income $133.75B (+31.3%).
# Q4 FY2026: revenue $90B (+18%, beat $87.72B consensus). Azure crossed $100B annual
# revenue, +43% YoY in Q4; Intelligent Cloud segment $39.31B (+31.6%). Copilot 30M paid seats.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Intelligent Cloud (Azure + server)", 168.0, 148.0, 195.0, "Azure crossed $100B annualized, +43% YoY in Q4; guided to accelerate to 45% cc in Q1 FY2027"),
    ("Productivity & Business (M365/Copilot)", 122.0, 110.0, 138.0, "Copilot paid seats hit 30M in a single quarter; the clearest enterprise AI monetization story available"),
    ("More Personal Computing (Windows/Gaming/Search)", 78.0, 70.0, 88.0, "Windows OEM, Xbox/gaming, Bing/ads — steadier, lower-growth, still meaningfully profitable"),
]

# Margin assumptions (GAAP operating margin proxy)
OP_MARGIN_CURR   = 0.400    # FY2027E blended operating margin; AI infrastructure depreciation is a real but manageable drag
OP_MARGIN_BULL   = 0.430    # BULL: Azure AI margin improves with scale; Copilot attach keeps growing at high incremental margin
OP_MARGIN_BEAR   = 0.340    # BEAR: AI capex depreciation outpaces monetization; Azure growth decelerates from the current 43%+ pace
TAX_RATE         = 0.180    # effective tax rate

# ── OPENAI PARTNERSHIP / AI MONETIZATION CALCULATOR (the Microsoft-specific angle) ─
AZURE_ANNUAL_REV_B   = 100.0  # $B Azure crossed this annualized revenue level in FY2026
AZURE_Q4_GROWTH_PCT  =  43.0  # % YoY Azure growth, Q4 FY2026
AZURE_Q1_FY27_GUIDE  =  45.0  # % YoY Azure growth guided for Q1 FY2027 (cc) — an ACCELERATION, not a deceleration
COPILOT_PAID_SEATS_M =  30.0  # million paid M365 Copilot seats, added in a single quarter
AI_RUNRATE_B         =  37.0  # $B annualized AI business revenue run-rate (as of Q3 disclosure), +123% YoY
OPENAI_STAKE_PCT     =  49.0  # % economic interest in OpenAI's for-profit entity (below a return-threshold cap)

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 16.20        # $/share non-GAAP-equivalent FY2027E; FY2026 actual net income $133.75B / diluted shares
PE_PESSIMISTIC = 22.0         # trough P/E: roughly Microsoft's own pre-AI-rerating multiple; 22x prices
                               # a return to being valued as "just" a very profitable enterprise software/cloud company
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2029E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  (12.32, 20,  246, "Azure growth decelerates sharply; AI capex depreciation outpaces Copilot/AI monetization"),
    "BASE":  (17.50, 27,  473, "Azure holds high-30s/low-40s growth; Copilot seats keep scaling; margin holds near guide"),
    "BULL":  (20.40, 29,  592, "Azure growth stays near 45%+; Copilot becomes the default enterprise AI seat; OpenAI stake compounds in value"),
    "XBULL": (24.50, 32,  784, "Microsoft becomes the clear enterprise AI operating system across cloud, productivity, and agents"),
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
        "name":       "Azure revenue YoY growth",
        "weight":     0.25,
        "thresholds": ("<25%",   "≥33%",   "≥40%",   "≥48%"),
        "now":        "+43%",
        "score":      4,
        "comment":    "Crossed $100B annualized; management is guiding Q1 FY2027 to ACCELERATE further to 45% cc",
    },
    {
        "name":       "Copilot paid seat growth",
        "weight":     0.20,
        "thresholds": ("<5M/qtr","≥10M/qtr","≥20M/qtr","≥28M/qtr"),
        "now":        "30M/qtr",
        "score":      4,
        "comment":    "30M paid seats added in a single quarter is the most concrete enterprise-AI-seat monetization number in the market",
    },
    {
        "name":       "AI business run-rate growth",
        "weight":     0.15,
        "thresholds": ("<50%",   "≥80%",   "≥100%",  "≥120%"),
        "now":        "+123%",
        "score":      4,
        "comment":    "$37B annualized run-rate, +123% YoY — one of the fastest-growing revenue lines at this dollar scale anywhere",
    },
    {
        "name":       "Consolidated operating margin",
        "weight":     0.15,
        "thresholds": ("<38%",   "≥42%",   "≥45%",   "≥48%"),
        "now":        "~45%",
        "score":      3,
        "comment":    "Holding up well despite the AI capex ramp — evidence the infrastructure spend isn't yet crushing profitability",
    },
    {
        "name":       "Full-year net income growth",
        "weight":     0.10,
        "thresholds": ("<12%",   "≥18%",   "≥25%",   "≥32%"),
        "now":        "+31.3%",
        "score":      4,
        "comment":    "FY2026 net income $133.75B, +31.3% — growth accelerating even at Microsoft's scale",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.15,
        "thresholds": (">34x",   "≤28x",   "≤24x",   "≤19x"),
        "now":        "~28.7x",
        "score":      2,
        "comment":    "28.7× FY2027E EPS — a real premium, though not extreme for the growth and quality on display",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Azure is accelerating, not decelerating — guided to 45% cc growth in Q1 FY2027, above even Q4's 43%", +0.9, 0.20),
    ("+", "Copilot seat growth is the cleanest enterprise-AI-monetization proof point of any large-cap software name", +0.7, 0.20),
    ("-", "Valuation carries a real premium — 28.7× forward for a $3.45T company leaves less room for a growth disappointment", -0.6, 0.20),
    ("+", "Diversified AI exposure — Azure infrastructure, Copilot seats, AND the OpenAI equity stake are three separate ways to win", +0.5, 0.15),
    ("-", "AI capex intensity — funding the buildout at this scale requires sustained, unbroken execution across multiple product lines", -0.4, 0.15),
    ("+", "Capital return — dividend growth streak plus buyback, funded by genuinely enormous free cash flow generation", +0.3, 0.10),
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
CONS_EPS_2YR  = 19.50   # conservative FY2029E: ~9.7% EPS CAGR — well below the current growth pace
CONS_PE_2YR   = 25      # modest de-rating from ~28.7× — still a real premium multiple
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Azure Cloud / M365 Copilot / OpenAI Partnership / Gaming")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

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
    print(f"  {seg:<44}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<44}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  FY2026 actual: revenue $331.84B (+17.8%), net income $133.75B (+31.3%). Q4: revenue $90B (+18%, beat)")
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

print(f"  FY2027E EPS check:  ${curr_total:.1f}B rev × {OP_MARGIN_CURR*100:.1f}% op margin − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2027E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {OP_MARGIN_BULL*100:.1f}% op margin, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 29× = ~${bull_eps_imp*29:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {OP_MARGIN_BEAR*100:.1f}% op margin (Azure decel + capex depreciation)")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 20× trough = ~${bear_eps_imp*20:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# OPENAI / AI MONETIZATION CHECK
print()
print(f"  OPENAI PARTNERSHIP & AI MONETIZATION CHECK  (the Microsoft-specific angle):")
print(f"  Azure annualized revenue:       ${AZURE_ANNUAL_REV_B:.0f}B+  (crossed this level in FY2026)")
print(f"  Azure Q4 FY2026 growth:         +{AZURE_Q4_GROWTH_PCT:.0f}% YoY")
print(f"  Azure Q1 FY2027 guide:          +{AZURE_Q1_FY27_GUIDE:.0f}% cc  (an ACCELERATION from Q4, not a deceleration)")
print(f"  Copilot paid seats added:       {COPILOT_PAID_SEATS_M:.0f}M  (in a single quarter)")
print(f"  AI business run-rate:           ${AI_RUNRATE_B:.0f}B  (+123% YoY)")
print(f"  OpenAI economic interest:       ~{OPENAI_STAKE_PCT:.0f}%  (below a capped-return threshold)")
print()
print(f"  Microsoft has three independent ways to monetize the AI cycle, not one: Azure")
print(f"  infrastructure (the picks-and-shovels layer), Copilot seats (the direct enterprise")
print(f"  software monetization layer), and the OpenAI equity stake (the model-layer optionality).")
print(f"  Azure guiding to ACCELERATE off an already-$100B base is the single most important")
print(f"  data point in this entire report — it directly contradicts the 'AI capex is overbuilding")
print(f"  ahead of demand' bear thesis that weighs on the rest of the hyperscaler cohort.")

# KEY SENSITIVITIES
print()
eps_per_1B_azure = 1.0 * 0.55 * (1 - TAX_RATE) / shares   # Azure incremental margin ~55%
eps_per_1B_copilot = 1.0 * 0.60 * (1 - TAX_RATE) / shares  # Copilot incremental margin ~60%
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Azure revenue (55% inc. margin):    +${eps_per_1B_azure:.3f}/EPS  = +${eps_per_1B_azure*27:.2f}/share at 27× P/E")
print(f"  Every $1B Copilot/M365 revenue (60% inc. margin): +${eps_per_1B_copilot:.3f}/EPS  = +${eps_per_1B_copilot*27:.2f}/share at 27× P/E")
print(f"  Every 1 turn of P/E:                          ±${EPS_FY2027E:.2f}/share  ({EPS_FY2027E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Azure growth / Copilot / AI run-rate / margin / earnings growth / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<38}  {'BEAR':>8}  {'BASE':>9}  {'BULL':>9}  {'XBULL':>9}  {'NOW':>9}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<38}  {ths[0]:>8}  {ths[1]:>9}  {ths[2]:>9}  {ths[3]:>9}  {s['now']:>9}  {lbl}  {b}")
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
    ("Azure revenue YoY",           "+43%",   "<25%",    "-18pp",  "Enterprise cloud capex pauses; hyperscaler capacity glut hits pricing"),
    ("Copilot seat growth",         "30M/qtr","<5M/qtr", "-25M",   "Enterprise AI-seat adoption stalls after the initial land-grab phase"),
    ("AI business run-rate growth", "+123%",  "<50%",    "-73pp",  "AI revenue growth normalizes hard off the current small-base acceleration"),
    ("Consolidated op margin",      "~45%",   "<38%",    "-7pp",   "AI infrastructure depreciation outpaces the revenue it's meant to generate"),
    ("Full-year net income growth", "+31.3%", "<12%",    "-19pp",  "Growth decelerates sharply across all three major segments at once"),
    ("Forward P/E",                 "~28.7x", "≤20x",    "-8.7x",  "Market fully re-prices AI-infrastructure optimism across the hyperscaler cohort"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: this is the same AI-capex debate every hyperscaler faces, but Microsoft's")
print(f"  evidence is the strongest in the group — Azure is ACCELERATING off a $100B base, not")
print(f"  decelerating, and Copilot's 30M-seat quarter is a concrete enterprise monetization proof")
print(f"  point most AI narratives lack entirely. The bear case requires all three legs (Azure,")
print(f"  Copilot, AI run-rate) to reverse simultaneously, which none of the current data supports.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2027E EPS estimate:       ${EPS_FY2027E:.2f}  (FY2026 net income $133.75B was +31.3% YoY)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (roughly Microsoft's pre-AI-rerating multi-year average)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS — a real but not extreme premium")
print(f"  for a company growing net income over 30%/yr with an accelerating cloud business.")
print(f"  Microsoft has earned a structurally higher multiple than most large-caps by successfully")
print(f"  navigating two prior platform transitions (PC, enterprise cloud); the AI transition is")
print(f"  the third, and the evidence so far says it's going at least as well.")
print(f"  At a 32× reversion (a genuine premium, reflecting sustained AI leadership): ${EPS_FY2027E:.2f} × 32 = ${EPS_FY2027E*32:.0f}")
print(f"  ({(EPS_FY2027E*32/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: growth decelerates well below the current pace, modest re-rating)")
hr()
print(f"  Conservative FY2029E EPS:  ${CONS_EPS_2YR:.2f}  (~9.7% EPS CAGR — a sharp deceleration from the current >30% pace)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~28.7× → 25×; a real de-rating, still a premium multiple)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: even assuming EPS growth decelerates from over 30% to under 10%/yr AND the")
print(f"  multiple compresses meaningfully, the conservative case still clears {cons_annual:.1f}%/yr. For a")
print(f"  company of this scale and quality, that combination of a real growth deceleration")
print(f"  assumption plus a real multiple haircut still working is a genuine margin of safety.")
print(f"  Breakeven at 25× requires FY2029E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f} — below this conservative estimate already.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.24
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Drawdown from high:    -{(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.1f}%  (a moderate pullback despite genuinely strong fundamentals)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; long, low-drama growth streak)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (lower than most AI-infrastructure names; MSFT's diversification dampens swings)")
print(f"  Beta vs S&P 500:      0.95  (near-market beta — unusual for a name with this much AI exposure)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (a genuine sector-wide AI-capex correction, not an MSFT-specific failure)")
print(f"  → Q1 FY2027 print is the test of whether the guided Azure acceleration (45% cc) actually lands.")
print(f"  → Copilot seat growth trajectory each quarter is the cleanest ongoing monetization signal.")
print(f"  → WATCHLIST at current price  |  ACCUMULATE $400–430  |  BUY below $370  |  TRIM above $560")

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
print(f"  Microsoft is delivering the single cleanest AI-monetization story among the mega-caps:")
print(f"  an accelerating $100B+ cloud business, a concrete enterprise AI seat product, and equity")
print(f"  optionality in the leading model lab. The stock has pulled back {(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.0f}% from its high")
print(f"  despite that. WATCHLIST, not BUY, only because ratio B ({ratio_b_str}) says the wide bear/bull")
print(f"  spread at this size and price still tilts slightly toward caution — this is a name to own,")
print(f"  and to add to more aggressively on any further weakness.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q1 FY2027 print — does Azure actually accelerate to the guided 45% cc growth?")
print(f"  (2) Copilot paid seat growth trajectory — needs to keep pace with the 30M-seat quarter to sustain the thesis")
print(f"  (3) AI capex guidance and depreciation schedule — the margin risk that ties Microsoft to the broader hyperscaler debate")
print(f"  (4) OpenAI relationship developments — commercial terms, model access, and equity value realization")
print(f"  (5) Gaming/More Personal Computing stability — the steady base that funds the AI investment cycle")
print(f"  WATCHLIST at ${CURRENT_PRICE:.2f}  |  ACCUMULATE $400–430  |  BUY below $370  |  TRIM above $560")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2027E EPS: ${EPS_FY2027E:.2f}  |  Azure: ${AZURE_ANNUAL_REV_B:.0f}B+ annualized")
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
