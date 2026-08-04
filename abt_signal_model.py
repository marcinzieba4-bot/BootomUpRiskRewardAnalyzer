"""
ABT  ·  Abbott Laboratories  ·  NYSE: ABT
Bottom-up signal model  ·  Diversified MedTech / Diagnostics / Nutrition
Date: 2026-08-04
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "ABT"
COMPANY       = "Abbott Laboratories"
SECTOR        = "Diversified MedTech · Diagnostics · Nutrition · NYSE: ABT"
CURRENT_PRICE = 107.12       # USD; close 2026-08-03
VOL_52W_LOW   = 81.97        # USD
VOL_52W_HIGH  = 137.49       # USD
SHARES_OUT_M  = 1_730.0      # millions
ANNUAL_DIV    = 2.52         # $/share annualized; Dividend King, 52+ consecutive yrs of increases

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ──────────────────────
# Q2 2026 actual (reported Jul 16, 2026): reported sales +13.0% YoY (Exact Sciences boost),
# comparable sales +4.8%; adjusted diluted EPS $1.31 (beat), GAAP EPS $0.53. Full-year adjusted
# EPS guidance raised to $5.45-$5.60 (from $5.38-$5.58); comparable sales growth guided 6.5-7.5%.
# NEC baby-formula litigation remains unresolved: Missouri appeals court upheld a $495M verdict
# (May 2026, $95M compensatory / $400M punitive); a Chicago jury returned a $70M verdict (Apr 2026).
# New bellwether trials are scheduled for Aug 2026, Nov 2026, and Feb 2027.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Diabetes Care",        8.1,  6.9,  9.5, "FreeStyle Libre CGM — global #1, 60%+ share; CMS Type 2 coverage expansion driving TAM"),
    ("Diagnostics",         11.6,  9.9, 13.6, "Cologuard via Exact Sciences (deal closed Mar 2026), now fully ramped; the biggest driver of Q2's +13% reported sales growth"),
    ("Established Pharma",   6.1,  5.4,  6.7, "Branded generics across emerging markets (Latin America, India, Russia)"),
    ("Medical Devices",     20.5, 17.6, 21.7, "Structural heart, electrophysiology, neuromodulation; durable double-digit growth continuing"),
    ("Nutrition",            8.2,  7.2,  8.5, "Adult/pediatric formula; NEC baby formula litigation overhang persists on Similac/Pediasure despite Q2 strength elsewhere"),
]

# Net-margin-based bridge
NET_MARGIN_CURR = 0.1752   # FY2026E; reconciles to raised guidance midpoint
NET_MARGIN_BEAR = 0.1693   # BEAR: litigation reserve build + competitive pressure compress margin
NET_MARGIN_BULL = 0.1831   # BULL: Diagnostics/Devices mix shift expands margin

# ── NEC LITIGATION TRACKER (the Abbott-specific angle) ────────────────────────
Q2_2026_REPORTED_SALES_GROWTH_PCT   = 13.0   # % YoY, Q2 2026 reported sales growth
Q2_2026_COMPARABLE_SALES_GROWTH_PCT = 4.8    # % YoY, Q2 2026 comparable sales growth
Q2_2026_ADJ_EPS                     = 1.31   # $ adjusted diluted EPS, Q2 2026 (beat)
MISSOURI_VERDICT_UPHELD_M           = 495    # $M, appeals court upheld May 2026 ($95M comp + $400M punitive)
CHICAGO_VERDICT_M                   = 70     # $M, Apr 2026 jury verdict
UPCOMING_BELLWETHER_TRIALS          = "Aug 2026, Nov 2026, Feb 2027"
STOCK_MOVE_FROM_JUNE_LOW_PCT        = round((CURRENT_PRICE - 87.41) / 87.41 * 100, 1)  # recovery since last refresh

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 5.52        # FY2026E adj EPS (raised-guidance midpoint)
PE_PESSIMISTIC = 15.0        # pessimistic P/E: below the current ~19.4x multiple, litigation tail still live
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (4.60, 14,  64,  "NEC bellwether trials produce further large adverse verdicts + Libre competitive share loss; EPS $4.60 → 14× distressed multiple"),
    "BASE":  (5.52, 19.4, 107, "FY2026 guidance holds near the raised midpoint; litigation remains a live but contained tail risk"),
    "BULL":  (6.35, 21, 133,  "Diagnostics/Devices margin mix shift continues; litigation stays contained to verdicts already seen; EPS $6.35"),
    "XBULL": (7.10, 24, 170,  "NEC litigation overhang substantially resolved; CGM/Cologuard growth accelerates; EPS $7.10 → 24× quality MedTech multiple"),
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
        "name":       "FreeStyle Libre (CGM) revenue growth",
        "weight":     0.25,
        "thresholds": ("<10%",   "≥14%",  "≥20%",   "≥28%"),
        "now":        "+16%",
        "score":      3,
        "comment":    "CMS Type 2 diabetes coverage expansion drives TAM; global #1 CGM with 60%+ share",
    },
    {
        "name":       "Cologuard / Exact Sciences integration",
        "weight":     0.20,
        "thresholds": ("Disrupted", "On-track", "Ahead",  "Accretive+synergy"),
        "now":        "Ahead",
        "score":      3,
        "comment":    "Fully ramped post-March 2026 close; the largest single driver behind Q2's +13% reported sales growth",
    },
    {
        "name":       "Medical Devices segment growth",
        "weight":     0.20,
        "thresholds": ("<5%",    "≥7%",   "≥10%",   "≥14%"),
        "now":        "+10%",
        "score":      3,
        "comment":    "Structural heart (TriClip, Navitor) + electrophysiology (Volt PFA) double-digit; neuromodulation steady",
    },
    {
        "name":       "NEC litigation resolution progress",
        "weight":     0.20,
        "thresholds": ("Verdicts >$3B", "Settling ~$1.5-2B", "Settled <$1.5B", "Dismissed/favorable"),
        "now":        "Verdicts accumulating, no global deal",
        "score":      2,
        "comment":    "Missouri ($495M, upheld on appeal) and Chicago ($70M) verdicts total ~$565M so far; new bellwether trials Aug/Nov 2026, Feb 2027",
    },
    {
        "name":       "Established Pharma emerging markets growth",
        "weight":     0.10,
        "thresholds": ("<3%",    "≥5%",   "≥8%",    "≥12%"),
        "now":        "+6%",
        "score":      2,
        "comment":    "Branded generics steady in Latin America/India; FX headwinds partially offset by volume growth",
    },
    {
        "name":       "Overall margin trajectory",
        "weight":     0.05,
        "thresholds": ("<54%",   "≥55.5%", "≥57%",  "≥58.5%"),
        "now":        "56.5%",
        "score":      2,
        "comment":    "Mix-driven gains from Diagnostics/Devices offsetting litigation reserve and integration costs",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "FreeStyle Libre #1 global CGM franchise — 60%+ share; CMS Type 2 TAM expansion runway",  +0.7, 0.25),
    ("+", "Cologuard #1 colon cancer screening — Exact Sciences deal adds scaled diagnostics moat, now ahead of integration plan", +0.5, 0.20),
    ("+", "Diversified MedTech/Devices base — structural heart, EP, neuromod all durable growers",   +0.5, 0.15),
    ("-", "NEC baby formula MDL — verdicts accumulating (~$565M so far, one upheld on appeal); binary tail risk remains live through Feb 2027", -0.6, 0.20),
    ("+", "Dividend King — 52+ years of increases; durable FCF; capital return discipline",          +0.4, 0.10),
    ("-", "Established Pharma EM exposure — FX volatility, slower structural growth segment",        -0.3, 0.10),
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
CONS_EPS_2YR  = 6.60    # conservative FY2028E EPS: litigation contained, CGM/Devices/Diagnostics compounding
CONS_PE_2YR   = 19      # roughly flat multiple vs. current ~19.4x
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Diversified MedTech / Diagnostics / Nutrition")
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
print(f"  Q2 2026 actual: reported sales +{Q2_2026_REPORTED_SALES_GROWTH_PCT:.1f}% YoY, comparable sales +{Q2_2026_COMPARABLE_SALES_GROWTH_PCT:.1f}% YoY, adj EPS ${Q2_2026_ADJ_EPS:.2f} (beat)")
print()

# EPS bridge (net-margin based)
shares    = SHARES_OUT_M / 1000
curr_net  = curr_total * NET_MARGIN_CURR
curr_eps  = round(curr_net / shares, 2)

bull_net     = bull_total * NET_MARGIN_BULL
bull_eps_imp = round(bull_net / shares, 2)

bear_net     = bear_total * NET_MARGIN_BEAR
bear_eps_imp = round(bear_net / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {NET_MARGIN_CURR*100:.2f}% net margin")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (vs BASE estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {NET_MARGIN_BULL*100:.2f}% net margin")
print(f"  ÷ {shares:.3f}B shares  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {NET_MARGIN_BEAR*100:.2f}% net margin (litigation reserve build + competitive pressure)")
print(f"  ÷ {shares:.3f}B shares  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× distressed = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# NEC LITIGATION TRACKER
print()
print(f"  NEC LITIGATION TRACKER  (the Abbott-specific angle):")
print(f"  Q2 2026 reported sales growth:            +{Q2_2026_REPORTED_SALES_GROWTH_PCT:.1f}% YoY  (comparable +{Q2_2026_COMPARABLE_SALES_GROWTH_PCT:.1f}%)")
print(f"  Q2 2026 adjusted diluted EPS:               ${Q2_2026_ADJ_EPS:.2f}  (beat)")
print(f"  Missouri verdict (upheld on appeal, May):   ${MISSOURI_VERDICT_UPHELD_M}M  ($95M compensatory / $400M punitive)")
print(f"  Chicago verdict (Apr 2026):                 ${CHICAGO_VERDICT_M}M")
print(f"  Upcoming bellwether trials:                 {UPCOMING_BELLWETHER_TRIALS}")
print(f"  Stock move since last refresh (Jun 10):     +{STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}%")
print()
print(f"  The market has re-rated ABT sharply higher on Q2 strength and raised guidance even as the NEC")
print(f"  litigation itself has NOT been resolved — verdicts are still accumulating case by case, with the")
print(f"  next real test being the August 2026 bellwether trial. The stock is pricing improving fundamentals")
print(f"  faster than it's pricing litigation clarity, which is the central tension in this name right now.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = 1.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at {NET_MARGIN_CURR*100:.1f}% margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*19.4:.2f}/share at 19.4× P/E")
print(f"  1pp net margin expansion (mix/scale):        +${curr_total*0.01/shares:.3f}/EPS  = +${curr_total*0.01/shares*19.4:.2f}/share at 19.4× P/E")
print(f"  Every 1 turn of P/E:                          ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (CGM growth / Diagnostics integration / Devices / NEC litigation framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>5}  {'BASE':>5}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>6}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>5}  {ths[1]:>5}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>6}  {lbl}  {b}")
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
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  Trigger")
hr()
bear_triggers = [
    ("NEC litigation outcome",          "Accumulating, no deal", "Verdicts >$3B", "Aug/Nov 2026 + Feb 2027 bellwether trials produce large plaintiff verdicts"),
    ("FreeStyle Libre revenue growth",  "+16%",   "<10%",   "Dexcom G8/Stelo + Medtronic Simplera CGM entrants erode share"),
    ("Cologuard/Exact integration",     "Ahead",  "Disrupted","Payer reimbursement pushback or integration cost overruns reverse the ramp"),
    ("Established Pharma EM growth",    "+6%",    "<3%",    "EM currency devaluation (Argentina, Russia) compresses reported growth"),
    ("Medical Devices growth",          "+10%",   "<5%",    "Structural heart competitive losses to Edwards/Medtronic"),
    ("Overall margin trajectory",       "56.5%",  "<54%",   "Litigation reserve build + integration costs compress margins further"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the August 2026 NEC bellwether trial (plus Nov 2026 and Feb 2027) produces a materially")
print(f"  adverse verdict that reprices aggregate exposure well above the ~$565M seen so far, triggering a")
print(f"  re-rating of the litigation discount even as the underlying CGM/Diagnostics/Devices franchises keep growing.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (raised-guidance midpoint)")
print(f"  Pessimistic P/E:                {PE_PESSIMISTIC:.0f}×  (below the current ~19.4× multiple; litigation tail still live)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f}, ABT trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS — a meaningful recovery from the")
print(f"  post-NEC-selloff trough multiple, but still short of a fully de-risked ~24× quality-MedTech multiple.")
print(f"  EPP path: FY2028E EPS ~${CONS_EPS_2YR:.2f} × {PE_PESSIMISTIC:.0f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor (EPP growing as litigation clarity emerges).")
print(f"  At 24× mid-cycle P/E (litigation resolved): ${EPS_FY2026E:.2f} × 24 = ${EPS_FY2026E*24:.0f}  — {(EPS_FY2026E*24/CURRENT_PRICE-1)*100:+.0f}% above current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: litigation stays contained, modest multiple holds)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (CGM/Devices/Diagnostics compounding ~9%/yr)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (roughly flat vs. current ~19.4×)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; Dividend King 52+ yr streak)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: after the post-Q2 rally, the conservative case still works but with less margin of")
print(f"  safety than in June — it now leans more on EPS growth actually materializing than on multiple re-rating.")
print(f"  Breakeven at {CONS_PE_2YR}× P/E (no multiple change): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  BUY trigger: below $85  (ratio_b <0.75×)  |  STRONG ADD: $75–$85 on a bad bellwether-trial verdict")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.22
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock is up {STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}% since the last refresh (Jun 10) on the Q2 beat + raised guidance")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  Dividend King, 52+ consecutive yrs of increases)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (still elevated vs historical defensiveness due to litigation binary)")
print(f"  Beta vs S&P 500:      0.72  (defensive healthcare; litigation overhang is the primary idiosyncratic risk)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (large adverse NEC verdicts; CGM competitive share loss)")
print(f"  → August 2026 NEC bellwether trial outcome is THE KEY near-term binary.")
print(f"  → FreeStyle Libre CMS Type 2 expansion data is the key bull catalyst for further re-rating.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $90  |  Trim above $135")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is {'BELOW' if MARKET_COMPOSITE < ADJ_COMPOSITE else 'ABOVE'} the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The gap ({ADJ_GAP:+.2f}) indicates the stock is {valuation_label.lower()}")
print(f"  by model standards. In plain terms: the Q2 beat and raised guidance have re-rated the stock a long")
print(f"  way back toward fair value, but real, unresolved litigation tail risk still argues for some caution.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) NEC litigation developments — August 2026 bellwether trial; further verdicts or settlement talks")
print(f"  (2) FreeStyle Libre CGM revenue / CMS Type 2 diabetes coverage expansion updates")
print(f"  (3) Cologuard / Exact Sciences integration progress and cross-sell synergy realization")
print(f"  (4) Medical Devices segment growth — structural heart (TriClip, Navitor) and EP (Volt PFA)")
print(f"  (5) Dividend increase announcement — Dividend King streak continuation (53rd consecutive yr)")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $90  |  Trim above $135")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}")
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
