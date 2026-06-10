"""
AMD  ·  Advanced Micro Devices, Inc.  ·  NASDAQ: AMD
Bottom-up signal model  ·  AI Accelerators / Data Center / Client / Gaming
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "AMD"
COMPANY       = "Advanced Micro Devices, Inc."
SECTOR        = "AI Accelerators · Data Center GPU/CPU · Client · Gaming · NASDAQ: AMD"
CURRENT_PRICE = 175.00      # USD; as of 2026-06-10
VOL_52W_LOW   = 110.00      # 2025 AI-capex-scare trough
VOL_52W_HIGH  = 240.00      # MI400/Helios hyperscaler-deal euphoria peak
SHARES_OUT_M  = 1_615.0     # millions; modest dilution from equity comp, offset by buybacks

# Dividend: none — all FCF reinvested in AI roadmap / buybacks
ANNUAL_DIV    = 0.0         # $/share

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Data Center (MI300/MI350 AI + EPYC)", 24.0, 14.0, 38.0, "AI accelerator ramp + EPYC server CPU share gains; swing factor"),
    ("Client (Ryzen)",                       9.5,  7.0, 12.5, "Ryzen AI PC refresh cycle; share gains vs Intel in notebooks"),
    ("Gaming",                               5.5,  3.5,  7.0, "Console SoC cyclicality + Radeon discrete GPU softness"),
    ("Embedded",                             3.5,  2.5,  4.5, "Xilinx-derived FPGA/adaptive SoC; industrial/aero/defense recovery"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.540   # blended gross margin FY2026E (~54%; AI mix lifting blend)
GROSS_MARGIN_BULL = 0.580   # BULL: Data Center AI mix dominates; margin expands further
OPEX_FIXED_B      = 8.0     # R&D + SG&A ($B); heavy AI silicon R&D investment
TAX_RATE          = 0.13    # effective rate; R&D credits, foreign mix

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 5.50        # FY2026E adj EPS (consensus ~$5.30–$5.70; non-GAAP)
PE_PESSIMISTIC = 22.0        # trough P/E: AI-capex-scare floor multiple (2025 trough ~22-24×)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $121

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 2.80, 22,   62, "MI300/MI350 ramp stalls; hyperscalers favor in-house silicon; EPS $2.80 → 22× floor P/E"),
    "BASE":  ( 5.50, 28,  154, "MI350/MI400 ramp on track; steady DC GPU share gains vs Nvidia; EPYC share continues; EPS $5.50 → 28×"),
    "BULL":  ( 8.50, 32,  272, "MI400/Helios rack-scale wins major hyperscaler commitments; DC GPU share >15%; EPS $8.50 → 32×"),
    "XBULL": (13.00, 36,  468, "AMD becomes credible #2 AI silicon platform at scale; multi-vendor diversification favors AMD; EPS $13.00 → 36×"),
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
        "name":       "MI300/MI350/MI400 AI accelerator revenue ramp & guidance",
        "weight":     0.30,
        "thresholds": ("<$5B",   "≥$8B",  "≥$13B",  "≥$20B"),
        "now":        "~$8B",
        "score":      2,
        "comment":    "MI350 ramping through 2026; MI400/Helios rack-scale slated for 2027; guidance reaffirmed but unproven at scale",
    },
    {
        "name":       "Data Center GPU market share gains vs Nvidia",
        "weight":     0.20,
        "thresholds": ("<3%",    "≥5%",   "≥10%",   "≥15%"),
        "now":        "~6%",
        "score":      2,
        "comment":    "AMD remains a distant #2; CUDA software moat keeps Nvidia >85% share; AMD gaining selectively in inference workloads",
    },
    {
        "name":       "EPYC server CPU share gains vs Intel",
        "weight":     0.15,
        "thresholds": ("<28%",   "≥32%",  "≥38%",   "≥45%"),
        "now":        "~36%",
        "score":      3,
        "comment":    "EPYC continues steady cloud/enterprise share gains; Turin ramp strong; Intel struggling to respond competitively",
    },
    {
        "name":       "Gross margin trajectory (mix shift to AI accelerators)",
        "weight":     0.15,
        "thresholds": ("<50%",   "≥52%",  "≥56%",   "≥60%"),
        "now":        "~54%",
        "score":      2,
        "comment":    "Blended GM improving as Data Center AI mix grows; still below Nvidia-level margins given competitive pricing on MI-series",
    },
    {
        "name":       "Client / Gaming segment health",
        "weight":     0.10,
        "thresholds": ("<-5%",   "≥0%",   "≥8%",    "≥15%"),
        "now":        "+4%",
        "score":      2,
        "comment":    "Ryzen AI PC refresh modestly positive; Gaming console cycle late-stage and soft; discrete GPU share stable but small",
    },
    {
        "name":       "Hyperscaler customer diversification (multi-vendor AI silicon strategy)",
        "weight":     0.10,
        "thresholds": ("Low",    "Moderate","High",  "Structural"),
        "now":        "Moderate",
        "score":      3,
        "comment":    "OpenAI, Microsoft, Oracle, Meta all signaling multi-vendor AI compute strategies; AMD positioned as credible alternative to Nvidia",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Credible #2 AI accelerator vendor — MI300/MI350/MI400 roadmap gaining real customer traction",  +0.6, 0.20),
    ("+", "EPYC structural share gains — multi-year cloud/enterprise CPU share momentum vs Intel",          +0.5, 0.15),
    ("-", "Nvidia CUDA software moat — switching costs entrench Nvidia's >85% AI training/inference share", -0.7, 0.20),
    ("-", "Custom silicon competition — Google TPU, AWS Trainium, Microsoft Maia erode merchant-silicon TAM",-0.5, 0.15),
    ("-", "High stock volatility / multiple sensitivity to AI capex narrative — sentiment-driven swings",   -0.5, 0.15),
    ("+", "Multi-vendor diversification tailwind — hyperscalers actively want a non-Nvidia alternative",     +0.4, 0.15),
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
CONS_EPS_2YR  = 7.00    # conservative FY2028E: ramp continues but below BULL pace
CONS_PE_2YR   = 24      # rerating from elevated AI-narrative multiple toward growth-justified 24×
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  AI Accelerators / Data Center / Client / Gaming")
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
shares_b  = shares * 0.97   # modest net buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.94   # mix shift away from AI accel; pricing pressure
bear_oi   = bear_gp - OPEX_FIXED_B * 0.97           # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 32× = ~${bull_eps_imp*32:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.94:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 22× trough P/E (AI-capex-scare floor) = ~${bear_eps_imp*22:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev   = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_dc    = 1.0 * 0.60 * (1 - TAX_RATE) / shares   # Data Center AI accel-level incremental margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Data Center AI revenue:  +${eps_per_1B_dc:.3f}/EPS  = +${eps_per_1B_dc*28:.1f}/share at 28× P/E")
print(f"  1pp Data Center GPU share gain (vs Nvidia, ~$3B TAM/pt): +${eps_per_1B_dc*3:.2f}/EPS  =  +${eps_per_1B_dc*3*28:.1f}/share at 28× P/E")
print(f"  1pp GM expansion (mix shift to AI accelerators):  +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*28:.1f}/share at 28× P/E")
print(f"  EPYC 1pp server CPU share gain (~$1.5B TAM/pt):   +${eps_per_1B_dc*1.5:.2f}/EPS  =  +${eps_per_1B_dc*1.5*28:.1f}/share at 28× P/E")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (AI accelerator ramp / DC share / EPYC / margin / client / diversification)")
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
    ("MI300/MI350/MI400 AI accel revenue",  "~$8B",   "<$5B",   "−$3B",   "Major hyperscaler cancels/delays MI400 orders; Helios slips to 2028"),
    ("Data Center GPU share vs Nvidia",     "~6%",    "<3%",    "−3pp",   "CUDA lock-in deepens; AMD ROCm software stack fails to gain developer traction"),
    ("EPYC server CPU share vs Intel",      "~36%",   "<28%",   "−8pp",   "Intel Clearwater Forest competitive resurgence; cloud price wars"),
    ("Gross margin",                        "~54%",   "<50%",   "−4pp",   "Aggressive AI accelerator pricing to win share erodes blended margin"),
    ("Client/Gaming segment growth",        "+4%",    "<-5%",   "−9pp",   "PC market downturn + console cycle trough simultaneously"),
    ("Hyperscaler diversification",         "Moderate","Low",   "−1 lvl", "Hyperscalers consolidate back to Nvidia + fully in-house custom silicon"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A major hyperscaler (Microsoft, Meta, Oracle, or OpenAI/Stargate-affiliated)")
print(f"  publicly pulls back from MI300/MI350/MI400 commitments, citing CUDA/software ecosystem")
print(f"  gaps or in-house silicon (TPU/Trainium/Maia) prioritization. Combined with an AI-capex")
print(f"  digestion cycle, Data Center revenue growth stalls, GM compresses on pricing pressure,")
print(f"  EPS falls to ~$2.80 → 22× floor = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT a permanent impairment — EPYC server share gains and the")
print(f"  Embedded/Client base provide an earnings floor independent of the AI accelerator narrative.")
print(f"  Recovery to ~${bear_price+50}–${bear_price+80} in 2yr is plausible if MI400/Helios re-engages design wins.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus $5.30–$5.70; non-GAAP)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (AI-capex-scare floor; 2025 trough ~22-24×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP means the market is pricing in multiple years of")
print(f"  successful MI300/MI350/MI400 ramp execution ABOVE the trough-floor multiple. At")
print(f"  ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f}, the implied P/E is {CURRENT_PRICE/EPS_FY2026E:.1f}×.")
print(f"  This is the 'AI narrative premium': investors are paying for proof of a Data Center")
print(f"  GPU revenue run-rate that has not yet fully materialized. The risk is narrative reversion")
print(f"  if hyperscaler AI capex growth decelerates or MI400 design wins disappoint.")
print(f"  EPP path: FY2028E EPS ~$8.00 × {PE_PESSIMISTIC:.0f}× = ${8.00*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing with ramp).")
print(f"  At 28× mid-cycle P/E: ${EPS_FY2026E:.2f} × 28 = ${EPS_FY2026E*28:.0f}  — close to current price, i.e. roughly BASE-priced.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: ramp continues at moderate pace; multiple normalizes)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (MI350/MI400 ramp continues; EPYC share gains persist)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (rerates from {CURRENT_PRICE/EPS_FY2026E:.0f}× toward growth-justified {CONS_PE_2YR}×)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (no dividend; 100% reinvested in AI roadmap/buybacks)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE PROBLEM: even the conservative case requires the AI accelerator ramp to keep")
print(f"  delivering ~27%/yr EPS growth while the multiple normalizes from {CURRENT_PRICE/EPS_FY2026E:.0f}× toward {CONS_PE_2YR}×.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — possible at BASE/BULL, not BEAR.")
print(f"  Breakeven at 28× P/E (no multiple compression): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 28:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.45
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: 52W range reflects extreme sensitivity to AI capex narrative shifts and hyperscaler")
print(f"  capex-guidance commentary throughout 2025-2026")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (none — all FCF reinvested in AI roadmap/buybacks)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (high-beta AI capex proxy; among most volatile mega-caps)")
print(f"  Beta vs S&P 500:      1.85  (high-beta AI capex cycle proxy; amplifies both AI optimism and capex-digestion fears)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe but within range seen during 2025 AI-capex scares)")
print(f"  52W low ${VOL_52W_LOW:.2f} (AI-capex-scare trough) was already a peak-to-trough move of >50%.")
print(f"  → Hyperscaler AI capex guidance (Microsoft, Meta, Amazon, Google, OpenAI/Stargate) is THE KEY binary.")
print(f"  → MI400/Helios design-win announcements and Data Center revenue beats are KEY bull catalysts.")
print(f"  → AVOID at current price  |  WATCHLIST $145–165  |  ACCUMULATE $120–140  |  BUY below $115")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) compares to the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0 fundamentals.")
print(f"  The model scores the fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0.")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: the gap between bullish AI narrative and proven Data Center GPU revenue")
print(f"  run-rate is the central risk/reward question for AMD at this price.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) MI400/MI450 (Helios rack-scale) launch and hyperscaler adoption — BULL trigger")
print(f"  (2) Data Center segment revenue/guidance updates — proof of AI accelerator run-rate")
print(f"  (3) EPYC share gains in cloud/enterprise — structural CPU tailwind vs Intel")
print(f"  (4) Gross margin trajectory — mix shift to AI accelerators vs competitive pricing pressure")
print(f"  (5) OpenAI/Microsoft/Oracle compute deals — multi-vendor AI silicon diversification evidence")
print(f"  (6) Q2/Q3 2026 earnings — Data Center segment beat/miss vs guidance")
print(f"  AVOID at ${CURRENT_PRICE:.2f}  |  WATCHLIST $145–165  |  ACCUMULATE $120–140  |  BUY below $115")
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
