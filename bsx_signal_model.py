"""
BSX  ·  Boston Scientific Corporation  ·  NYSE: BSX
Bottom-up signal model  ·  Cardiovascular (WATCHMAN/Farapulse) / MedSurg / Post-Crash Reset
Date: 2026-08-04
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "BSX"
COMPANY       = "Boston Scientific Corporation"
SECTOR        = "MedTech · Cardiovascular (WATCHMAN/Farapulse PFA) · Structural Heart · Urology/MedSurg · NYSE: BSX"
CURRENT_PRICE = 48.43       # USD; close 2026-08-03 — down ~53% from Sep 2025 peak
VOL_52W_LOW   = 42.20       # USD
VOL_52W_HIGH  = 109.50      # USD
SHARES_OUT_M  = 1_450.0     # millions
ANNUAL_DIV    = 0.0         # $/share; BSX pays no dividend — reinvests for growth/M&A

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# THE HEADLINE EVENT: BSX has cut FY2026 guidance repeatedly through the year, driven by a
# sharp, unexpected slowdown in WATCHMAN (LAAC) procedure growth tied to compounding
# clinical-evidence concerns affecting physician referrals — management now assumes the
# weakness persists into 2027. Q2 2026 (reported Jul 29): revenue $5.442B (+7.5% YoY, beat);
# adj EPS $0.86 (beat the high end of guide, aided by favorable tax); GAAP EPS $0.61 — but
# FY2026 guidance was slashed to reported sales growth ~5.5-6.5% (from an earlier 10-11%) and
# adj EPS $3.28-3.32 (below consensus $3.36). Two Class II recalls hit in June 2026 (Orca
# air/water/suction valves, ~9,750 units; Coyote PTA balloon catheter), and a $500M
# restructuring was announced to protect margins. Despite the crash, 27 of 31 analysts still
# rate BSX Buy-equivalent, with a consensus target (~$78) implying substantial recovery.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Electrophysiology (Farapulse PFA)",        3.2,  2.4,  4.5, "Still the healthiest growth driver — no negative news this refresh; pulsed-field ablation rollout continues"),
    ("Cardiology - WATCHMAN (LAAC)",             3.0,  2.0,  3.8, "THE crisis driver: procedure growth has slowed sharply on compounding clinical-evidence concerns affecting referrals"),
    ("Cardiology - Interventional/Other",        6.0,  5.3,  6.8, "Coronary therapies, IVL (shockwave), peripheral interventions; steady mid-single-digit growth continuing"),
    ("Structural Heart (TAVR/Mitral/Tricuspid)", 1.6,  1.2,  2.2, "ACURATE/WATCHMAN-adjacent structural heart pipeline; mitral/tricuspid optionality"),
    ("Urology/Neuromodulation (incl. Axonics)",  3.2,  2.7,  3.8, "Axonics sacral neuromodulation integration continuing to drive share gains"),
    ("MedSurg/Endoscopy/Other",                  4.37, 3.9,  4.9, "Includes the segments affected by the June 2026 Orca/Coyote Class II recalls"),
]

# Net-margin-based bridge
NET_MARGIN_CURR = 0.2239   # FY2026E; reconciles to cut guidance midpoint
NET_MARGIN_BEAR = 0.1906   # BEAR: WATCHMAN weakness persists into 2027 as management now assumes, plus recall/restructuring costs linger
NET_MARGIN_BULL = 0.2510   # BULL: WATCHMAN concerns resolve, Farapulse continues, restructuring delivers margin benefit

# ── WATCHMAN CRISIS / RECALL TRACKER (the BSX-specific angle) ─────────────────
Q2_2026_REVENUE_B          = 5.442   # $B, Q2 2026 actual reported revenue
Q2_2026_ADJ_EPS            = 0.86    # $ adjusted EPS, Q2 2026 (beat, aided by favorable tax)
Q2_2026_GAAP_EPS           = 0.61    # $ GAAP EPS, Q2 2026
FY2026_ORIGINAL_GROWTH_GUIDE_PCT = "10-11"   # % reported sales growth, original guidance
FY2026_CUT_GROWTH_GUIDE_PCT      = "5.5-6.5" # % reported sales growth, current guidance after cuts
RESTRUCTURING_ANNOUNCED_B  = 0.5     # $B, restructuring program announced to protect margins
RECALLED_UNITS_ORCA        = 9_750   # units, Orca air/water/suction valve Class II recall
ANALYST_BUY_RATIO          = "27 of 31"  # analysts still rating BSX Buy-equivalent despite the crash
CONSENSUS_TARGET_PRICE     = 78.0    # $, analyst consensus price target
STOCK_MOVE_FROM_JUNE_LOW_PCT = round((CURRENT_PRICE - 104.00) / 104.00 * 100, 1)  # move since last refresh

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 3.30        # FY2026E adj EPS (cut guidance $3.28-3.32; midpoint)
PE_PESSIMISTIC = 12.0        # pessimistic P/E: a genuine fresh trough, below the current ~14.7× multiple, reflecting the WATCHMAN/recall overhang
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (2.30, 12,   28, "WATCHMAN weakness persists into 2027 as management now assumes; recall/restructuring costs linger; EPS $2.30 → 12× = $28"),
    "BASE":  (3.30, 14.68, 48, "FY2026 guidance holds at the cut level; WATCHMAN stabilizes but doesn't recover; Farapulse and other segments offset partially; EPS $3.30 → 14.7× = $48"),
    "BULL":  (4.50, 18,   81, "WATCHMAN referral concerns resolve faster than guided; restructuring delivers real margin benefit; Farapulse continues strong; EPS $4.50 → 18× = $81"),
    "XBULL": (5.20, 21,  109, "Full recovery toward pre-crisis growth trajectory; WATCHMAN concerns fully resolved; multiple re-rates back toward its prior premium; EPS $5.20 → 21× = $109"),
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
        "name":       "Farapulse (PFA) revenue YoY growth",
        "weight":     0.25,
        "thresholds": ("<25%",  "≥45%",  "≥65%",   "≥85%"),
        "now":        "+55%",
        "score":      2,
        "comment":    "Still the healthiest part of the story — no negative Farapulse-specific news this refresh, decelerating from launch-year highs as expected",
    },
    {
        "name":       "WATCHMAN (LAAC) revenue growth",
        "weight":     0.25,
        "thresholds": ("<8%",   "≥14%",  "≥20%",   "≥28%"),
        "now":        "~-2%",
        "score":      1,
        "comment":    "THE crisis driver — procedure growth has gone negative on compounding clinical-evidence concerns affecting physician referrals",
    },
    {
        "name":       "PFA competitive dynamics (Medtronic/J&J)",
        "weight":     0.15,
        "thresholds": ("losing share fast", "share roughly stable", "BSX gaining share", "BSX gaining share + pricing holds"),
        "now":        "BSX gaining share",
        "score":      3,
        "comment":    "Farapulse first-mover advantage remains intact even as WATCHMAN struggles — this is a WATCHMAN-specific problem, not a company-wide one",
    },
    {
        "name":       "Organic revenue growth (company-wide)",
        "weight":     0.15,
        "thresholds": ("<8%",   "≥12%",  "≥16%",   "≥20%"),
        "now":        "~6%",
        "score":      1,
        "comment":    "Guidance cut sharply from 10-11% to 5.5-6.5% — the WATCHMAN slowdown is now dragging on company-wide growth",
    },
    {
        "name":       "Recall/restructuring execution",
        "weight":     0.10,
        "thresholds": ("escalating/cost overrun", "contained but costly", "resolved, modest cost", "resolved ahead of plan"),
        "now":        "contained but costly",
        "score":      2,
        "comment":    "$500M restructuring announced to protect margins; Orca/Coyote Class II recalls are real but not existential",
    },
    {
        "name":       "Valuation vs forward growth (PEG-adjusted)",
        "weight":     0.10,
        "thresholds": ("PEG>2.2", "PEG~1.6-2.2", "PEG~1.1-1.6", "PEG<1.1"),
        "now":        "PEG ~0.8",
        "score":      4,
        "comment":    "~14.7× FY2026E EPS against ~18%/yr forward growth (FY2027E consensus $3.90) is now a genuinely cheap PEG — the crash re-priced the multiple faster than the fundamentals actually deteriorated",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Farapulse category leadership remains intact — the crisis is specific to WATCHMAN, not company-wide", +0.6, 0.25),
    ("-", "WATCHMAN clinical-evidence concerns — real, quantified, and management itself assumes persistence into 2027", -0.8, 0.25),
    ("+", "Diversified portfolio (Farapulse, Interventional, Urology/Axonics) provides real offset outside WATCHMAN",     +0.5, 0.15),
    ("-", "Guidance cut from 10-11% to 5.5-6.5% signals the slowdown reached beyond WATCHMAN alone",                       -0.4, 0.15),
    ("+", "Valuation reset — the ~53% price decline is a larger move than the ~19% guidance-EPS cut, a real margin of safety", +0.5, 0.10),
    ("-", "No dividend / two Class II recalls add reputational and execution risk on top of the WATCHMAN issue",           -0.3, 0.10),
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
CONS_EPS_2YR  = 4.20   # FY2028E conservative: ~13%/yr off FY2026E, below the street's implied pace
CONS_PE_2YR   = 16     # a modest re-rate from the current depressed ~14.7× as risks partially resolve
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Cardiovascular (WATCHMAN/Farapulse) / MedSurg — Post-Crash Reset")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<42}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<42}  ${curr:>11.2f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<42}  ${curr_total:>11.2f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  Q2 2026 actual: revenue ${Q2_2026_REVENUE_B:.3f}B (+7.5% YoY, beat), adj EPS ${Q2_2026_ADJ_EPS:.2f} (beat), GAAP EPS ${Q2_2026_GAAP_EPS:.2f}")
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
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {NET_MARGIN_BEAR*100:.2f}% net margin (WATCHMAN weakness persists + recall/restructuring drag)")
print(f"  ÷ {shares:.3f}B shares  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# WATCHMAN CRISIS / RECALL TRACKER
print()
print(f"  WATCHMAN CRISIS / RECALL TRACKER  (the BSX-specific angle):")
print(f"  Q2 2026 revenue / adj EPS / GAAP EPS:        ${Q2_2026_REVENUE_B:.3f}B / ${Q2_2026_ADJ_EPS:.2f} / ${Q2_2026_GAAP_EPS:.2f}")
print(f"  FY2026 growth guide, original → cut:          {FY2026_ORIGINAL_GROWTH_GUIDE_PCT}%  →  {FY2026_CUT_GROWTH_GUIDE_PCT}%")
print(f"  Restructuring announced:                       ${RESTRUCTURING_ANNOUNCED_B:.1f}B  (to protect margins)")
print(f"  Orca valve recall (Class II, Jun 2026):         {RECALLED_UNITS_ORCA:,} units")
print(f"  Analyst sentiment despite the crash:            {ANALYST_BUY_RATIO} rate Buy-equivalent, consensus target ${CONSENSUS_TARGET_PRICE:.0f}")
print(f"  Stock move since last refresh (Jun 10):        {STOCK_MOVE_FROM_JUNE_LOW_PCT:+.1f}%")
print()
print(f"  This is a real, quantified crisis, not a sentiment-only selloff: WATCHMAN procedure growth")
print(f"  has gone negative on clinical-evidence concerns affecting referrals, and management itself")
print(f"  now assumes the weakness persists into 2027 — that's a genuinely bearish admission. But the")
print(f"  {abs(STOCK_MOVE_FROM_JUNE_LOW_PCT):.0f}% price decline is considerably larger than the ~19% cut to guided EPS, and the rest of the")
print(f"  portfolio (Farapulse, Interventional, Urology) shows no comparable deterioration.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = 1.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at {NET_MARGIN_CURR*100:.1f}% margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*14.68:.2f}/share at 14.7× P/E")
print(f"  1pp net margin expansion (mix/restructuring):+${curr_total*0.01/shares:.3f}/EPS  = +${curr_total*0.01/shares*14.68:.2f}/share at 14.7× P/E")
print(f"  Every 1 turn of P/E:                          ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Farapulse growth / WATCHMAN crisis / PFA competition / organic growth / recall / valuation)")
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
    ("Farapulse revenue growth",           "+55%",   "<25%",   "Medtronic PulseSelect/J&J Varipulse capture share faster than expected"),
    ("WATCHMAN revenue growth",            "~-2%",   "<-10%",  "Clinical-evidence concerns deepen further, referral slowdown accelerates"),
    ("PFA competitive share dynamics",     "gaining","losing share", "Newer-gen competitor catheters leapfrog Farapulse"),
    ("Organic revenue growth (co-wide)",   "~6%",    "<3%",    "WATCHMAN drag spreads to other segments; broader medtech slowdown"),
    ("Recall/restructuring execution",     "contained","escalating", "Additional recalls surface; restructuring costs exceed the $500M budget"),
    ("Net margin",                         "22.4%",  "<19%",   "Sustained WATCHMAN + recall drag compresses margins further"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>16}  {bear_v:>9}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the WATCHMAN clinical-evidence concerns deepen rather than stabilize, referral")
print(f"  volumes keep declining through 2027 as management now assumes, and the recall/restructuring")
print(f"  costs run over the $500M budget. EPS falls to ~$2.30 at a 12× fresh-trough multiple.")
print(f"  Note: ${bear_price} would represent a level BELOW the current 52-week low (${VOL_52W_LOW:.2f}) —")
print(f"  a genuinely severe outcome, not the base case even in this bear scenario.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (cut guidance midpoint)")
print(f"  Pessimistic P/E:                {PE_PESSIMISTIC:.0f}×  (below the current ~14.7× multiple; a fresh trough reflecting the WATCHMAN/recall overhang)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f}, BSX trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS — a dramatic de-rating from the")
print(f"  ~30× multiples it commanded through 2025 as a premium medtech grower. The EPP floor still")
print(f"  provides real margin of safety even after accounting for the genuine WATCHMAN deterioration.")
print(f"  At 18× mid-cycle P/E (WATCHMAN concerns resolve): ${EPS_FY2026E:.2f} × 18 = ${EPS_FY2026E*18:.0f}  — {(EPS_FY2026E*18/CURRENT_PRICE-1)*100:+.0f}% above current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest EPS growth, partial multiple recovery)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (~13%/yr off FY2026E, below the street's implied pace)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (a modest re-rate from the current depressed ~14.7×)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (no dividend — BSX reinvests for growth/M&A)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: even a conservative case — modest EPS growth, only a partial multiple")
print(f"  recovery, and no credit for WATCHMAN fully resolving — delivers a substantial positive")
print(f"  return, because the ~53% price decline has already priced in more damage than the")
print(f"  guidance cuts (~19% EPS reduction) actually reflect.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.42
beta        = 0.95
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock is down {abs(STOCK_MOVE_FROM_JUNE_LOW_PCT):.1f}% since the last refresh (Jun 10) and ~57-60% from its Sep 2025 peak")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (no dividend — BSX reinvests for growth/M&A)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; repeated guidance cuts drove large single-day moves through 2026)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (roughly market-like; now compounded by idiosyncratic WATCHMAN risk)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (a genuinely severe outcome below the current 52-week low)")
print(f"  → WATCHMAN referral-volume trend over the next 1-2 quarters is THE KEY signal to watch.")
print(f"  → Farapulse growth durability and restructuring execution are the KEY offsetting factors.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $45  |  Trim above $75")

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
print(f"  {valuation_label.lower()} by model standards. In plain terms: the WATCHMAN crisis is real and the proxy")
print(f"  fundamentals score genuinely weak (~{PROXY_COMPOSITE:.1f}/4.0) — but the price decline has been so severe that")
print(f"  the resulting valuation reset (ratio_b {ratio_b_str}) more than compensates, consistent with the")
print(f"  {ANALYST_BUY_RATIO} analysts still rating the stock Buy-equivalent.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) WATCHMAN referral-volume trend — the next 1-2 quarterly prints are the key test")
print(f"  (2) Farapulse (PFA) growth durability — confirming the rest of the portfolio stays healthy")
print(f"  (3) $500M restructuring execution — margin benefit realization vs cost overrun risk")
print(f"  (4) Any further Class II/III recalls — quality-system scrutiny following Orca/Coyote")
print(f"  (5) Organic revenue growth stabilization — confirming 5.5-6.5% guidance holds, doesn't get cut again")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $45  |  Trim above $75")
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
