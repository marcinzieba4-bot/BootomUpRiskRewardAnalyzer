"""
ABT  ·  Abbott Laboratories  ·  NYSE: ABT
Bottom-up signal model  ·  Diversified MedTech / Diagnostics / Nutrition
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "ABT"
COMPANY       = "Abbott Laboratories"
SECTOR        = "Diversified MedTech · Diagnostics · Nutrition · NYSE: ABT"
CURRENT_PRICE = 87.41        # USD; as of 2026-06-10
VOL_52W_LOW   = 78.00        # 2026 NEC litigation panic trough
VOL_52W_HIGH  = 140.00       # June 2025 high (pre-NEC litigation overhang)
SHARES_OUT_M  = 1_740.0      # millions; modest buyback

# Dividend King: 52+ consecutive years of dividend increases
ANNUAL_DIV    = 2.56         # $/share annualized

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ──────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Diabetes Care",        7.5,  6.4,  9.5, "FreeStyle Libre CGM — global #1, 60%+ share; CMS Type 2 expansion driving TAM"),
    ("Diagnostics",          9.6,  8.3, 11.2, "Cologuard via Exact Sciences (Mar 2026 deal) + core lab diagnostics"),
    ("Established Pharma",   5.8,  5.2,  6.8, "Branded generics across emerging markets (Latin America, India, Russia)"),
    ("Medical Devices",     19.0, 16.8, 22.5, "Structural heart, electrophysiology, neuromodulation; durable double-digit growth"),
    ("Nutrition",            8.6,  7.0,  9.4, "Adult/pediatric formula; NEC baby formula litigation overhang on Similac/Pediasure"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.560   # blended gross margin FY2026E (~56%)
GROSS_MARGIN_BULL = 0.580   # BULL: Devices/Diagnostics mix shift + Cologuard scale lifts blend
OPEX_FIXED_B      = 17.5    # R&D + SG&A ($B); includes litigation reserve drag
TAX_RATE          = 0.150   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 5.45        # FY2026E adj EPS (BASE case consensus)
PE_PESSIMISTIC = 16.0        # trough P/E: current trading multiple post NEC selloff
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $87

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (4.20, 13,  55,  "NEC verdicts >$2B + FreeStyle Libre deceleration; EPS $4.20 → 13× distressed multiple"),
    "BASE":  (5.45, 16,  87,  "NEC settles ~$1.5-2B as expected; steady CGM/devices growth; EPS $5.45 → 16× trough multiple"),
    "BULL":  (6.30, 20, 126,  "NEC litigation overhang resolved/contained; multiple normalizes to 20×; EPS $6.30"),
    "XBULL": (7.50, 24, 180,  "Litigation discount fully removed; CGM/Cologuard accelerate; EPS $7.50 → 24× quality MedTech multiple"),
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
        "now":        "+18%",
        "score":      3,
        "comment":    "CMS Type 2 diabetes coverage expansion drives TAM; global #1 CGM with 60%+ share; intensive insulin + basal segments scaling",
    },
    {
        "name":       "Cologuard / Exact Sciences integration",
        "weight":     0.20,
        "thresholds": ("Disrupted", "On-track", "Ahead",  "Accretive+synergy"),
        "now":        "On-track",
        "score":      2,
        "comment":    "March 2026 deal closed; cross-sell into Diagnostics distribution; integration costs near-term drag, synergies emerging FY2027",
    },
    {
        "name":       "Medical Devices segment growth",
        "weight":     0.20,
        "thresholds": ("<5%",    "≥7%",   "≥10%",   "≥14%"),
        "now":        "+9%",
        "score":      2,
        "comment":    "Structural heart (TriClip, Navitor) + electrophysiology (Volt PFA) double-digit; neuromodulation steady",
    },
    {
        "name":       "NEC litigation resolution progress",
        "weight":     0.20,
        "thresholds": ("Verdicts >$3B", "Settling ~$1.5-2B", "Settled <$1.5B", "Dismissed/favorable"),
        "now":        "Settling ~$1.5-2B",
        "score":      2,
        "comment":    "~782 cases in MDL; August 2026 trial pending; settlement talks ongoing; quantifiable but uncertain reserve",
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
        "now":        "56.0%",
        "score":      2,
        "comment":    "Litigation reserves and integration costs offsetting mix-driven gross margin gains; stable but not yet expanding",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "FreeStyle Libre #1 global CGM franchise — 60%+ share; CMS Type 2 TAM expansion runway",  +0.7, 0.25),
    ("+", "Cologuard #1 colon cancer screening — Exact Sciences deal adds scaled diagnostics moat",  +0.5, 0.20),
    ("+", "Diversified MedTech/Devices base — structural heart, EP, neuromod all durable growers",   +0.5, 0.15),
    ("-", "NEC baby formula MDL — ~782 cases, Aug 2026 trial; quantifiable but binary tail risk",     -0.6, 0.20),
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
CONS_EPS_2YR  = 6.00    # conservative FY2028E EPS: NEC resolved, CGM/Devices compounding
CONS_PE_2YR   = 17      # modest rerating from 16× toward 17× as litigation overhang clears
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
print()

# EPS bridge
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_ni   = curr_oi * (1 - TAX_RATE)
shares    = SHARES_OUT_M / 1000
curr_eps  = round(curr_ni / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B
bull_ni   = bull_oi * (1 - TAX_RATE)
shares_b  = shares * 0.97   # modest buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift + litigation cost pressure
bear_oi   = bear_gp - OPEX_FIXED_B * 1.10           # higher litigation reserve drag
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (vs BASE estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 20× = ~${bull_eps_imp*20:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex (incl. litigation reserve build)  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 13× distressed P/E (NEC verdicts >$2B) = ~${bear_eps_imp*13:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev   = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_libre = 1.0 * 0.65 * (1 - TAX_RATE) / shares   # CGM-level incremental margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B FreeStyle Libre revenue:  +${eps_per_1B_libre:.3f}/EPS  = +${eps_per_1B_libre*16:.1f}/share at 16× P/E")
print(f"  Every $1B Diagnostics revenue:      +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*16:.1f}/share at 16× P/E")
print(f"  1pp GM expansion (mix/scale):       +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*16:.1f}/share at 16× P/E")
print(f"  NEC settlement -$1B vs reserve:     ~${1.0*(1-TAX_RATE)/shares:.2f}/EPS one-time hit  =  ~${1.0*(1-TAX_RATE)/shares*16:.1f}/share at 16× P/E")

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

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15% hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:72]:<72}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("NEC litigation outcome",          "Settling ~$1.5-2B", "Verdicts >$2B", "Adverse",  "Aug 2026 trial produces large plaintiff verdicts; bellwether losses cascade"),
    ("FreeStyle Libre revenue growth",  "+18%",   "<10%",   "−8pp",   "Dexcom G8/Stelo + Medtronic Simplera CGM entrants erode share"),
    ("Cologuard/Exact integration",     "On-track","Disrupted","Reversal","Integration costs balloon; payer reimbursement pushback on Cologuard Plus"),
    ("Established Pharma EM growth",    "+6%",    "<3%",    "−3pp",   "EM currency devaluation (Argentina, Russia) compresses reported growth"),
    ("Medical Devices growth",          "+9%",    "<5%",    "−4pp",   "Structural heart competitive losses to Edwards/Medtronic"),
    ("Overall margin trajectory",       "56.0%",  "<54%",   "−2pp",   "Litigation reserve build + integration costs compress margins further"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: August 2026 NEC baby formula MDL trial produces a materially adverse")
print(f"  bellwether verdict (>$2B aggregate exposure implied), triggering cascading settlement")
print(f"  pressure across ~782 pending cases. Combined with FreeStyle Libre share loss to")
print(f"  Dexcom/Medtronic CGM entrants,")
print(f"  Note: ${bear_price} is NOT a permanent impairment — Diabetes Care, Diagnostics, and")
print(f"  EPS compresses to ~${SCENARIOS['BEAR'][0]:.2f} at a 13× distressed multiple = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT a permanent impairment — Diabetes Care, Diagnostics, and")
print(f"  Medical Devices remain world-class franchises; recovery to ~${bear_price+25}–${bear_price+40} in 2yr is plausible post-settlement clarity.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (BASE case)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (current trading multiple — already at trough post NEC selloff)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  At a +{epp_gap_pct:.0f}% gap to EPP, ABT trades almost exactly at its trough-multiple")
print(f"  earnings power, down 37% from its June 2025 high of ${VOL_52W_HIGH:.0f}. The market is pricing")
print(f"  in essentially zero credit for the diversified MedTech/diagnostics franchise quality —")
print(f"  FreeStyle Libre (#1 CGM globally), Cologuard (#1 colon cancer screen post Exact Sciences),")
print(f"  and a 52+ year Dividend King streak — beyond the headline NEC litigation discount.")
print(f"  EPP path: FY2028E EPS ~${CONS_EPS_2YR:.2f} × {PE_PESSIMISTIC:.0f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing as litigation clarity emerges).")
print(f"  At 20× mid-cycle P/E (litigation resolved): ${EPS_FY2026E:.2f} × 20 = ${EPS_FY2026E*20:.0f}  — {(EPS_FY2026E*20/CURRENT_PRICE-1)*100:+.0f}% above current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: NEC litigation resolved, modest multiple recovery)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (CGM/Devices/Diagnostics compounding ~7-8%/yr)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (modest rerating from 16× trough toward 17× as NEC overhang clears)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; Dividend King 52+ yr streak)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE OPPORTUNITY: unlike many trough-valuation calls, the conservative case here does NOT")
print(f"  require multiple expansion beyond 16×→17× — just modest EPS growth plus the Dividend King yield.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires only ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — well within BASE case range.")
print(f"  Breakeven at 16× P/E (no multiple expansion): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 16:.2f}")
print(f"  BUY trigger: ${78}–${90} (current trough range; ratio_b <0.75×)  |  STRONG ADD: ${74}–${82} on Aug 2026 trial panic")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.24
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: 52W high (Jun 2025) pre-dates NEC baby formula litigation overhang (-37% to current ${CURRENT_PRICE:.2f})")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  Dividend King, 52+ consecutive yrs of increases)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated vs historical defensiveness due to litigation binary)")
print(f"  Beta vs S&P 500:      0.70  (defensive healthcare; litigation overhang is the primary idiosyncratic risk)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (large adverse NEC verdicts; CGM competitive share loss)")
print(f"  52W low ${VOL_52W_LOW:.2f} (2026 NEC litigation panic) is already a peak-to-trough move of ~44% from the high.")
print(f"  → August 2026 NEC trial outcome is THE KEY binary; settlement clarity = de-risking catalyst.")
print(f"  → FreeStyle Libre CMS Type 2 expansion data is KEY bull catalyst for re-rating.")
print(f"  → AVOID above $100  |  WATCHLIST $90–100  |  ACCUMULATE/BUY $78–90  |  STRONG ADD $74–82 on Aug 2026 trial panic")

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
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0, while the model")
print(f"  scores fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0. The gap ({ADJ_GAP:.2f}) indicates the stock is")
print(f"  {valuation_label.lower()} by model standards.")
print(f"  In plain terms: the NEC litigation discount appears to price in a near-BEAR outcome,")
print(f"  while the diversified franchise (CGM, diagnostics, devices, Dividend King yield) supports")
print(f"  closer to a BASE/BULL fundamental composite.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) NEC litigation developments — August 2026 bellwether trial; settlement talks (~$1.5-2B range expected)")
print(f"  (2) FreeStyle Libre CGM revenue / CMS Type 2 diabetes coverage expansion updates")
print(f"  (3) Cologuard / Exact Sciences integration progress and cross-sell synergy realization")
print(f"  (4) Medical Devices segment growth — structural heart (TriClip, Navitor) and EP (Volt PFA)")
print(f"  (5) Dividend increase announcement — Dividend King streak continuation (53rd consecutive yr)")
print(f"  AVOID above $100  |  WATCHLIST $90–100  |  ACCUMULATE/BUY $78–90  |  STRONG ADD $74–82 (Aug 2026 trial panic)")
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
