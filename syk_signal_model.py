"""
SYK  ·  Stryker Corporation  ·  NYSE: SYK
Bottom-up signal model  ·  Orthopaedics (Mako Robotics) / MedSurg & Neurotechnology / Spine / Vascular
Date: 2026-08-04
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "SYK"
COMPANY       = "Stryker Corporation"
SECTOR        = "MedTech · Orthopaedics (Mako Robotics) · MedSurg & Neurotechnology · Spine · Vascular · NYSE: SYK"
CURRENT_PRICE = 341.20      # USD; close 2026-08-03
VOL_52W_LOW   = 281.00      # USD
VOL_52W_HIGH  = 396.86      # USD
SHARES_OUT_M  = 384.0       # millions
ANNUAL_DIV    = 3.52        # $/share; ~1.0% yield

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# Q2 2026 actual (reported Jul 30): revenue $6.59B (+9.4% YoY, organic +9.0%, slight beat);
# adj EPS $3.69 (+17.9% YoY, beat by ~5.8%); GAAP EPS $3.30 (+44.1%). The stock DROPPED on
# the print despite the beat: Vascular (-6.7%) was hurt by an operational disruption at an
# Inari Peripheral Vascular plant causing backorders. FY2026 guidance narrowed to organic
# growth 8.3-9.3%, adj EPS $14.95-15.10 (consensus ~$14.99-15.01, revenue ~$27.29B). Offsetting
# the Vascular hit: record Mako robotic installations and a strong capital equipment backlog.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Orthopaedics (Mako Robotics/Hip/Knee)", 11.5, 10.0, 13.0, "Record Mako installations continuing to drive recurring implant/consumable pull-through"),
    ("MedSurg & Neurotechnology",             10.0,  8.8, 11.5, "Broad-based capital equipment strength; strong backlog supports visibility"),
    ("Spine",                                  2.3,  2.0,  2.6, "Steady, unspectacular growth"),
    ("Vascular (Inari Peripheral Vascular)",   3.49,  2.5,  4.2, "Plant operational disruption caused backorders (-6.7% this quarter); the swing factor for this refresh"),
]

# Net-margin-based bridge
NET_MARGIN_CURR = 0.2114   # FY2026E; reconciles to guidance midpoint
NET_MARGIN_BEAR = 0.1978   # BEAR: Vascular disruption persists, elective surgery softens
NET_MARGIN_BULL = 0.2208   # BULL: Vascular resolves, Mako installed base keeps compounding

# ── VASCULAR DISRUPTION / MAKO INSTALLED BASE TRACKER (the SYK-specific angle) ─
Q2_2026_REVENUE_B          = 6.59    # $B, Q2 2026 actual reported revenue
Q2_2026_ADJ_EPS            = 3.69    # $ adjusted EPS, Q2 2026 (+17.9% YoY, beat)
Q2_2026_GAAP_EPS           = 3.30    # $ GAAP EPS, Q2 2026 (+44.1% YoY)
VASCULAR_SEGMENT_GROWTH_PCT = -6.7   # % YoY, Vascular segment (Inari plant disruption)
FY2026_GUIDANCE_EPS_RANGE  = "14.95-15.10"  # $ adjusted, FY2026 guidance
STOCK_MOVE_FROM_JUNE_LOW_PCT = round((CURRENT_PRICE - 380.00) / 380.00 * 100, 1)  # move since last refresh

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 15.025      # FY2026E adj EPS (guidance $14.95-15.10; midpoint)
PE_PESSIMISTIC = 18.0        # pessimistic P/E: below the current ~22.7× multiple; a genuine hospital-capex-freeze trough
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (12.00, 19,  228, "Vascular disruption persists longer than guided; elective surgery volume softens on hospital budget pressure; EPS $12.00 → 19× = $228"),
    "BASE":  (15.025, 22.71, 341, "Vascular backorders clear as guided; Mako/MedSurg momentum continues; Spine steady; EPS $15.03 → 22.7× = $341"),
    "BULL":  (18.00, 25,  450, "Vascular fully recovers and re-accelerates; record Mako installed base keeps compounding recurring revenue; EPS $18.00 → 25× = $450"),
    "XBULL": (21.00, 28,  588, "Mako robotics category leadership widens further; hospital capex supercycle continues; Vascular becomes a genuine growth contributor; EPS $21.00 → 28× = $588"),
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
        "name":       "Organic revenue growth",
        "weight":     0.25,
        "thresholds": ("<5%",   "≥7%",   "≥9%",    "≥12%"),
        "now":        "+9.0%",
        "score":      3,
        "comment":    "Q2 2026 organic growth +9.0%, at the high end of the guided range",
    },
    {
        "name":       "Mako robotics installations",
        "weight":     0.20,
        "thresholds": ("declining", "flat", "growing", "record pace"),
        "now":        "record pace",
        "score":      4,
        "comment":    "Record Mako installations this quarter — the installed-base moat keeps widening",
    },
    {
        "name":       "Vascular (Inari) disruption recovery",
        "weight":     0.20,
        "thresholds": ("worsening", "stabilizing", "resolved", "growth resumed"),
        "now":        "plant disruption, backorders",
        "score":      1,
        "comment":    "The reason the stock dropped despite the beat — a real, quantified operational problem, not yet resolved",
    },
    {
        "name":       "Hospital capital equipment backlog",
        "weight":     0.15,
        "thresholds": ("declining", "flat", "growing", "strong"),
        "now":        "strong backlog",
        "score":      3,
        "comment":    "MedSurg & Neurotechnology capital equipment backlog remains a source of forward visibility",
    },
    {
        "name":       "Adjusted EPS growth",
        "weight":     0.10,
        "thresholds": ("<10%",  "≥14%",  "≥18%",   "≥25%"),
        "now":        "+17.9%",
        "score":      2,
        "comment":    "Just shy of the BULL threshold; a genuine beat but not a blowout",
    },
    {
        "name":       "Post-cyberattack operational normalization",
        "weight":     0.10,
        "thresholds": ("disrupted", "stabilizing", "normalized", "ahead of plan"),
        "now":        "normalized (ex-Vascular)",
        "score":      3,
        "comment":    "The prior cyberattack disruption is largely behind the company; the Vascular issue is a separate, newer problem",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Mako installed base switching-cost moat — record installations widen the recurring-revenue base further", +1.0, 0.25),
    ("-", "Vascular (Inari) plant operational disruption — real, quantified near-term drag (-6.7% segment growth)", -0.6, 0.20),
    ("+", "Aging demographics — structural, multi-decade demand tailwind for orthopaedic/surgical procedure volume",  +0.6, 0.20),
    ("+", "Hospital capital equipment backlog — supports forward revenue visibility across MedSurg & Neurotechnology", +0.4, 0.15),
    ("-", "Valuation remains rich even after the pullback — limited margin of safety for further disappointments",    -0.4, 0.10),
    ("+", "Prior cyberattack disruption largely resolved — operations normalized outside of the separate Vascular issue", +0.3, 0.10),
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
CONS_EPS_2YR  = 17.50   # FY2028E conservative: ~8%/yr off FY2026E, Vascular recovers modestly
CONS_PE_2YR   = 21      # a modest compression from the current ~22.7×
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Orthopaedics (Mako) / MedSurg & Neuro / Spine / Vascular")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<40}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<40}  ${curr:>11.2f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<40}  ${curr_total:>11.2f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  Q2 2026 actual: revenue ${Q2_2026_REVENUE_B:.2f}B (+9.4% YoY), adj EPS ${Q2_2026_ADJ_EPS:.2f} (+17.9% YoY, beat), GAAP EPS ${Q2_2026_GAAP_EPS:.2f}")
print()

# EPS bridge (net-margin based)
shares    = SHARES_OUT_M / 1000
curr_net  = curr_total * NET_MARGIN_CURR
curr_eps  = round(curr_net / shares, 2)

bull_net     = bull_total * NET_MARGIN_BULL
bull_eps_imp = round(bull_net / shares, 2)

bear_net     = bear_total * NET_MARGIN_BEAR
bear_eps_imp = round(bear_net / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.2f}B rev × {NET_MARGIN_CURR*100:.2f}% net margin")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (guidance ${EPS_FY2026E:.2f} midpoint  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {NET_MARGIN_BULL*100:.2f}% net margin")
print(f"  ÷ {shares:.3f}B shares  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {NET_MARGIN_BEAR*100:.2f}% net margin (Vascular disruption + surgery softness)")
print(f"  ÷ {shares:.3f}B shares  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# VASCULAR DISRUPTION / MAKO TRACKER
print()
print(f"  VASCULAR DISRUPTION / MAKO INSTALLED BASE TRACKER  (the SYK-specific angle):")
print(f"  Q2 2026 revenue / adj EPS / GAAP EPS:        ${Q2_2026_REVENUE_B:.2f}B / ${Q2_2026_ADJ_EPS:.2f} / ${Q2_2026_GAAP_EPS:.2f}")
print(f"  Vascular segment growth:                      {VASCULAR_SEGMENT_GROWTH_PCT:+.1f}% YoY  (Inari plant disruption, backorders)")
print(f"  FY2026 guidance:                               adj EPS ${FY2026_GUIDANCE_EPS_RANGE}")
print(f"  Stock move since last refresh (Jun 10):        {STOCK_MOVE_FROM_JUNE_LOW_PCT:+.1f}%")
print()
print(f"  This is a genuine 'good quarter, bad reaction' setup: SYK beat on revenue and adj EPS, but")
print(f"  a plant-level operational disruption at Inari (acquired for Peripheral Vascular) caused")
print(f"  backorders that dragged that one segment -6.7%. Record Mako installations and a strong")
print(f"  MedSurg/Neuro capital backlog were largely overshadowed by that single negative data point.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = 1.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at {NET_MARGIN_CURR*100:.1f}% margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*22.71:.2f}/share at 22.7× P/E")
print(f"  1pp net margin expansion (mix/scale):        +${curr_total*0.01/shares:.3f}/EPS  = +${curr_total*0.01/shares*22.71:.2f}/share at 22.7× P/E")
print(f"  Every 1 turn of P/E:                          ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (organic growth / Mako installs / Vascular recovery / backlog / EPS / operations)")
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
print(f"  {'Signal':<52}  {'Current':>16}  {'Bear val':>9}  Trigger")
hr()
bear_triggers = [
    ("Organic revenue growth",           "+9.0%",  "<5%",    "Elective surgery volume softens on hospital budget pressure"),
    ("Mako robotics installations",      "record pace", "declining", "Competing robots (JNJ Velys, Zimmer ROSA) displace Mako in new evaluations"),
    ("Vascular (Inari) recovery",        "disrupted", "worsening", "Plant issues persist beyond guided timeline, backorders deepen"),
    ("Hospital capital backlog",         "strong", "declining", "CFOs pull back capex amid reimbursement pressure"),
    ("Adjusted EPS growth",              "+17.9%", "<10%",   "Margin pressure from Vascular disruption spreads to other segments"),
    ("Net margin",                       "21.1%",  "<18%",   "Sustained operational disruption compresses margins further"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>16}  {bear_v:>9}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the Inari Vascular plant disruption persists well beyond the guided timeline,")
print(f"  and simultaneously hospital capex tightens (reimbursement pressure, budget cuts) enough to")
print(f"  slow Mako installations and elective surgery volume. EPS falls to ~$12.00 → 19× trough P/E.")
print(f"  Note: ${bear_price} is NOT permanent impairment — the Mako installed base keeps generating")
print(f"  recurring implant/consumable revenue regardless of new system sales.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (guidance midpoint)")
print(f"  Pessimistic P/E:                {PE_PESSIMISTIC:.0f}×  (below the current ~22.7× multiple; a genuine hospital-capex-freeze trough)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f}, SYK trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS — down from the ~30× multiples")
print(f"  seen through mid-2026, largely due to the Vascular-driven pullback despite the underlying")
print(f"  Mako/MedSurg beat. The EPP floor provides real, if not enormous, margin of safety.")
print(f"  At 25× mid-cycle P/E (Vascular resolved): ${EPS_FY2026E:.2f} × 25 = ${EPS_FY2026E*25:.0f}  — {(EPS_FY2026E*25/CURRENT_PRICE-1)*100:+.0f}% above current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: Vascular recovers modestly, multiple compresses slightly)")
hr()
print(f"  Conservative FY2028E EPS:  ${CONS_EPS_2YR:.2f}  (~8%/yr off FY2026E base)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (a modest compression from ~22.7×)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: even a conservative case with modest growth and a modest de-rating still")
print(f"  comes out positive, since the Mako installed base and MedSurg backlog provide real earnings")
print(f"  visibility independent of the Vascular disruption resolving on any particular timeline.")
print(f"  Breakeven at {CONS_PE_2YR}× P/E (no multiple change): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.22
beta        = 0.75
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock is down {abs(STOCK_MOVE_FROM_JUNE_LOW_PCT):.1f}% since the last refresh (Jun 10), dropping on the Vascular miss despite a broader beat")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (low; defensive healthcare compounder)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (low beta; draws flight-to-quality in risk-off environments)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (a genuine multi-quarter Vascular/hospital-capex shock)")
print(f"  → Vascular (Inari) plant disruption resolution timeline is THE KEY near-term signal to watch.")
print(f"  → Mako installation pace and MedSurg backlog conversion are the KEY bull catalysts.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $310  |  Trim above $390")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is")
print(f"  {'ABOVE' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'BELOW'} the model's adj composite ({ADJ_COMPOSITE:.3f}). The gap ({ADJ_GAP:+.2f}) indicates the stock is")
print(f"  {valuation_label.lower()} by model standards. In plain terms: the market appears to be over-weighting")
print(f"  a single, fixable segment disruption relative to the broader Mako/MedSurg strength underneath it.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Vascular (Inari) plant disruption resolution — timeline to clearing backorders")
print(f"  (2) Mako robotics installation pace — confirming the record-quarter trend continues")
print(f"  (3) MedSurg & Neurotechnology capital equipment backlog conversion")
print(f"  (4) Elective surgery volume trends — hospital capacity and budget signals")
print(f"  (5) Q3 2026 print — the next confirmation point for Vascular recovery")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $310  |  Trim above $390")
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
