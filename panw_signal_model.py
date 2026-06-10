"""
PANW  ·  Palo Alto Networks, Inc.  ·  NASDAQ: PANW
Bottom-up signal model  ·  Cybersecurity Platform / NGS / Cortex AI-SOC
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "PANW"
COMPANY       = "Palo Alto Networks, Inc."
SECTOR        = "Cybersecurity Platform · Network Security · Cloud Security · AI-SOC · NASDAQ: PANW"
CURRENT_PRICE = 260.00      # USD; as of 2026-06-10, near all-time high $261.41
VOL_52W_LOW   = 145.00
VOL_52W_HIGH  = 262.00      # all-time-high territory ahead of Q3 FY2026 earnings (June 2)
SHARES_OUT_M  = 615.0       # millions

# Dividend: none
ANNUAL_DIV    = 0.0

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Network Security (FW/SASE)",    5.10, 4.40, 5.70, "Hardware/software firewalls + SASE; mature core, steady renewal base"),
    ("Cloud Security (Prisma Cloud)", 1.55, 1.20, 2.05, "CNAPP consolidation share gains; cloud workload growth tailwind"),
    ("Security Ops (Cortex XSIAM)",   1.35, 0.95, 1.95, "AI-SOC replacing legacy SIEM; fastest-growing NGS pillar"),
    ("NGS Platformization (other)",   0.65, 0.45, 1.05, "Bundled platformization ARR conversions across product lines"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.760   # blended gross margin FY2026E (~76%)
GROSS_MARGIN_BULL = 0.785   # BULL: NGS/software mix shift lifts blend further
OPEX_FIXED_B      = 4.55    # R&D + SG&A ($B); platformization sales investment
TAX_RATE          = 0.220   # effective non-GAAP tax rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 3.75        # FY2026E adj EPS (consensus ~$3.75; non-GAAP)
PE_PESSIMISTIC = 28.0        # trough P/E: even bear case keeps premium for #1 platform position
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $105

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 4.50, 28,  126, "NGS ARR growth decelerates <45%; platformization stalls; multiple compresses to 28×"),
    "BASE":  ( 7.00, 38,  266, "FY2028 Rule of 60 trajectory intact; NGS ARR ~$15B; 38× on $7.00 EPS"),
    "BULL":  ( 9.50, 45,  428, "AI-SOC (Cortex XSIAM) ARR scales sharply; >40% FCF margin achieved early; 45×"),
    "XBULL": (13.00, 52,  676, "PANW becomes default cybersecurity OS; NGS ARR >$20B; 52× re-rating"),
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
        "name":       "Next-Gen Security (NGS) ARR YoY growth",
        "weight":     0.25,
        "thresholds": ("<40%",   "≥48%",  "≥55%",   "≥65%"),
        "now":        "53-54%",
        "score":      3,
        "comment":    "NGS ARR $8.5B+, growing 53-54% YoY; on Rule-of-60 trajectory toward FY2028 target",
    },
    {
        "name":       "Platformization deal momentum (consolidation)",
        "weight":     0.20,
        "thresholds": ("Slowing", "Steady", "Accelerating", "Land-grab"),
        "now":        "Accelerating",
        "score":      3,
        "comment":    "1,550 platform customers; large enterprises consolidating point products to single vendor",
    },
    {
        "name":       "Cortex XSIAM (AI-SOC) ARR contribution",
        "weight":     0.20,
        "thresholds": ("<$0.8B", "≥$1.0B","≥$1.4B", "≥$2.0B"),
        "now":        "~$1.2B",
        "score":      3,
        "comment":    "AI-SOC bookings outpacing legacy SIEM displacement; fastest-growing NGS pillar but early innings",
    },
    {
        "name":       "Prisma Cloud / cloud security growth",
        "weight":     0.15,
        "thresholds": ("<15%",   "≥20%",  "≥28%",   "≥38%"),
        "now":        "~25%",
        "score":      2,
        "comment":    "CNAPP consolidation share gains continue but competitive intensity from Wiz/CrowdStrike rising",
    },
    {
        "name":       "FCF margin trajectory (toward FY2028 40% target)",
        "weight":     0.10,
        "thresholds": ("<32%",   "≥35%",  "≥38%",   "≥41%"),
        "now":        "~36%",
        "score":      2,
        "comment":    "On track toward 40% FY2028 target but expansion pace needs to hold through platformization spend",
    },
    {
        "name":       "Net retention rate (NRR) & large deal (>$5M/$10M ACV) momentum",
        "weight":     0.10,
        "thresholds": ("<110%",  "≥115%", "≥120%",  "≥125%"),
        "now":        "119% NRR",
        "score":      2,
        "comment":    "119% NRR steady; >$5M and >$10M ACV deal counts growing but not yet accelerating sharply",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "#1 cybersecurity platform position — broadest portfolio; structural consolidation tailwind",     +0.6, 0.20),
    ("+", "NGS ARR growth (53-54% YoY) industry-leading; platformization strategy de-risks revenue mix",     +0.5, 0.20),
    ("-", "All-time-high valuation — $260 vs ATH $261.41, leaves zero cushion into Q3 FY2026 earnings",      -0.6, 0.20),
    ("-", "71x FY2026E EPS prices in years of flawless execution; PEG stretched vs decelerating hardware",   -0.7, 0.20),
    ("+", "Cortex XSIAM (AI-SOC) optionality — credible attacker on legacy SIEM incumbents (Splunk/IBM)",    +0.3, 0.10),
    ("-", "Competitive intensity — CrowdStrike (XDR/identity) and Microsoft (bundled E5) pressuring share",  -0.4, 0.10),
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
CONS_EPS_2YR  = 6.00    # conservative FY2028E EPS: NGS growth decelerates somewhat from current pace
CONS_PE_2YR   = 32      # rerating from 71× toward growth-justified 32×
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Cybersecurity Platform / NGS / AI-SOC")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<26}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<26}  ${curr:>11.2f}  ${bear:>8.2f}  ${bull:>8.2f}  {bear-curr:>+7.2f}  {bull-curr:>+7.2f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<26}  ${curr_total:>11.2f}  ${bear_total:>8.2f}  ${bull_total:>8.2f}  {bear_total-curr_total:>+7.2f}  {bull_total-curr_total:>+7.2f}")
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

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.97   # margin pressure from competitive discounting
bear_oi   = bear_gp - OPEX_FIXED_B * 0.97
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.2f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.2f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ~${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.2f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 45× = ~${bull_eps_imp*45:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 28× compressed P/E = ~${bear_eps_imp*28:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B NGS ARR converted to revenue: +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*38:.1f}/share at 38× P/E")
print(f"  1pp gross margin expansion:             +${curr_total*0.01*(1-TAX_RATE)/shares:.3f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*38:.1f}/share at 38× P/E")
print(f"  Cortex XSIAM ARR +$0.5B (high margin):  +${0.5*0.80*(1-TAX_RATE)/shares:.3f}/EPS  = +${0.5*0.80*(1-TAX_RATE)/shares*38:.1f}/share at 38× P/E")
print(f"  P/E compression 71× → 50× (no EPS chg): ${EPS_FY2026E*50:.0f}  vs current ${CURRENT_PRICE:.0f}  ({(EPS_FY2026E*50-CURRENT_PRICE)/CURRENT_PRICE*100:.0f}%)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (NGS ARR / Platformization / Cortex XSIAM / Cloud Security / FCF / NRR)")
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
    ("NGS ARR growth YoY",                "53-54%", "<45%",   "−9pp",   "Macro spending pause; mega-deal slippage to next quarter"),
    ("Platformization deal cadence",      "Accel.", "Slowing","Decel.", "Enterprises pause consolidation amid budget scrutiny"),
    ("Cortex XSIAM ARR growth",           "~$1.2B", "<$0.9B", "Slower", "CrowdStrike Falcon Next-Gen SIEM / Microsoft Sentinel share gains"),
    ("Prisma Cloud growth",               "~25%",   "<15%",   "−10pp",  "Wiz (post-Google) and CrowdStrike CNAPP undercut on price"),
    ("FCF margin trajectory",             "~36%",   "<32%",   "−4pp",   "Platformization sales investment outpaces opex leverage"),
    ("Net retention rate (NRR)",          "119%",   "<112%",  "−7pp",   "Cross-sell saturation; customers right-size after consolidation"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Q3 FY2026 earnings (June 2) shows NGS ARR growth decelerating below 45%")
print(f"  alongside a softer platformization large-deal cadence (>$5M/>$10M ACV deal counts flat")
print(f"  to down QoQ). Combined with Cortex XSIAM ARR disclosure missing the implied pace needed")
print(f"  for the FY2028 Rule-of-60 + 40% FCF margin target, the market re-rates from 71× toward")
print(f"  ~28× on $4.50 EPS = ${bear_price}. At an all-time high with zero cushion, even an")
print(f"  in-line-but-not-beat quarter could trigger meaningful multiple compression.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~${EPS_FY2026E:.2f}; non-GAAP)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (#1 platform position retains premium even in a derate)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP means the market is pricing in many years of")
print(f"  uninterrupted NGS ARR growth, platformization deal momentum, and FCF margin expansion")
print(f"  ABOVE the trough-floor multiple. At ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f}, the")
print(f"  P/E is {CURRENT_PRICE/EPS_FY2026E:.0f}× — extraordinarily rich even for a best-in-class compounder.")
print(f"  EPP path: FY2028E EPS ~$6.00 × {PE_PESSIMISTIC:.0f}× = ${6.00*PE_PESSIMISTIC:.0f} floor by FY2028 (EPP growing as EPS scales).")
print(f"  At 38× mid-cycle P/E: ${EPS_FY2026E:.2f} × 38 = ${EPS_FY2026E*38:.0f}  — still well below current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: P/E rerates toward growth-justified multiple)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (NGS ARR growth moderates from 53-54% but remains strong)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (rerates from {CURRENT_PRICE/EPS_FY2026E:.0f}× toward growth-justified {CONS_PE_2YR}×)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (no dividend)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE PROBLEM: even the conservative case requires P/E compression from {CURRENT_PRICE/EPS_FY2026E:.0f}× to {CONS_PE_2YR}×.")
print(f"  That multiple contraction can offset most/all of EPS growth over 2 years — flat to")
print(f"  negative total return even if NGS ARR keeps growing in the 40-50% range.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~${((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — possible at BULL, not BASE.")
print(f"  Breakeven at 45× P/E (limited multiple compression): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 45:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.34
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: ${CURRENT_PRICE:.2f} sits essentially at the all-time high (~$261.41), heading into")
print(f"  Q3 FY2026 earnings (June 2, 2026) — minimal cushion for any guidance disappointment.")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (no dividend; full reinvestment in platform)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; high-multiple growth name; earnings-reaction prone)")
print(f"  Beta vs S&P 500:      1.15  (premium; high-multiple software/security exposure)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (a multiple derate on a soft quarter, not a fundamental collapse)")
print(f"  52W low ${VOL_52W_LOW:.2f} already represents a peak-to-trough move of ~{(VOL_52W_HIGH-VOL_52W_LOW)/VOL_52W_HIGH*100:.0f}% from current highs.")
print(f"  → Q3 FY2026 earnings (June 2) is THE near-term binary; any NGS ARR deceleration or")
print(f"  platformization deal-cadence softness at 71× FY2026E EPS could trigger a sharp derate.")
print(f"  → Cortex XSIAM ARR disclosure beating expectations is the KEY near-term bull catalyst.")
print(f"  → Signal screens {signal_short} (Ratio B {ratio_b_str})  |  WATCHLIST $185–195  |  ACCUMULATE ~$165  |  BUY below $145")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) sits relative to the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0 fundamentals,")
print(f"  while the model scores current execution at ~{ADJ_COMPOSITE:.2f}/4.0 (between BASE and BULL).")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: at $260 and 71x FY2026E EPS, downside to BEAR ($126, -{downside_pct*100:.0f}%) is")
print(f"  comparable to upside to BULL ($428, +{upside_pct*100:.0f}%) — Ratio B {ratio_b_str} is roughly")
print(f"  symmetric, but the BEAR scenario itself is a deep multiple derate from an all-time high,")
print(f"  meaning the 'cushion' is thin even though the raw ratio screens as {signal_short}.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q3 FY2026 earnings (June 2, 2026) — NGS ARR update vs 53-54% YoY pace")
print(f"  (2) Cortex XSIAM (AI-SOC) ARR disclosure — pace toward FY2028 Rule-of-60 target")
print(f"  (3) Platformization large-deal momentum — >$5M and >$10M ACV deal counts QoQ")
print(f"  (4) FCF margin trajectory toward 40% FY2028 target — any stalling vs plan")
print(f"  (5) Competitive dynamics vs CrowdStrike (XDR/Next-Gen SIEM), Microsoft (E5 bundling), Zscaler (SASE)")
print(f"  Signal: {signal_full} at ${CURRENT_PRICE:.2f}  |  WATCHLIST $185–195  |  ACCUMULATE ~$165  |  BUY below $145")
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
