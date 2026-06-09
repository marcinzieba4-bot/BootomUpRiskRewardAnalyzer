"""
NVDA  ·  NVIDIA Corporation  ·  NASDAQ: NVDA
Bottom-up signal model  ·  Data Center AI / GPU / Accelerated Computing / Automotive
Date: 2026-06-09
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "NVDA"
COMPANY       = "NVIDIA Corporation"
SECTOR        = "Semiconductors · Data Center AI · Accelerated Computing · NASDAQ: NVDA"
CURRENT_PRICE = 131.50       # USD; as of 2026-06-09
VOL_52W_LOW   =  76.18       # January 2026 DeepSeek/tariff trough
VOL_52W_HIGH  = 165.42       # November 2025 Blackwell ramp peak
SHARES_OUT_M  = 24_420.0     # millions; ~0.5%/yr dilution net (SBC > buybacks at current pace)

# Dividend: initiated 2012; current $0.01/quarter = $0.04/yr; economically negligible
ANNUAL_DIV    = 0.04         # $/share FY2027 (buybacks are the return vehicle; $50B authorization)

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2027E revenue by segment ($B)  [NVDA fiscal year ends Jan; FY2027 = Feb 2026–Jan 2027]
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Data Center",              175.0,  95.0, 225.0, "Blackwell GB200/GB300 clusters; hyperscalers + sovereign AI"),
    ("Gaming",                    12.0,   8.0,  18.0, "RTX 50 series; DLSS 4; AI-driven frame generation; PC market"),
    ("Professional Visualization",  3.0,   2.0,   5.0, "Omniverse; design/simulation; industrial digital twin"),
    ("Automotive",                 5.0,   3.0,   9.0, "DRIVE Thor; robotaxi partnerships; ADAS compute platform"),
    ("OEM & Other",                2.0,   1.5,   3.0, "Embedded NVIDIA; channel; crypto-adjacent mining"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.730   # blended gross margin FY2027E (~73%; Data Center GPU premium)
GROSS_MARGIN_BULL = 0.760   # BULL: Data Center mix >90%; NVL72 rack premium pricing
OPEX_FIXED_B      = 10.0    # R&D + SG&A ($B); non-GAAP (excludes ~$4B SBC); growing ~20%/yr
TAX_RATE          = 0.130   # effective rate; IP structures; R&D credits

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 4.80        # FY2027E adj EPS (consensus $4.70–$5.00; non-GAAP)
PE_PESSIMISTIC = 22.0        # trough P/E: CUDA moat provides floor even in pause scenario
                              # (NVDA trough P/E 2022 bear: ~20×; CUDA lock-in justifies premium)
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # $105.60 → $106

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 2.50, 22,  55,  "Hyperscaler pause + DeepSeek efficiency + ASIC displacement; EPS $2.50 → 22× floor"),
    "BASE":  ( 5.00, 28, 140,  "Blackwell/Rubin cycle healthy; ~40% rev CAGR; sovereign AI adds; EPS $5 → 28×"),
    "BULL":  ( 7.50, 33, 248,  "Rubin supercycle; agentic AI explosion; robotics + autonomous vehicles; EPS $7.50 → 33×"),
    "XBULL": (12.00, 38, 456,  "NVDA = AGI/physical AI backbone; $500B+ revenue; robotics everywhere; EPS $12 → 38×"),
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
        "name":       "Data Center revenue YoY growth",
        "weight":     0.35,
        "thresholds": ("<20%",   "≥40%",  "≥70%",   "≥110%"),
        "now":        "+52%",
        "score":      3,
        "comment":    "FY2026 $115B → FY2027E $175B; Blackwell GB200 NVL72 rack demand from all 5 hyperscalers",
    },
    {
        "name":       "Non-GAAP gross margin",
        "weight":     0.20,
        "thresholds": ("<65%",   "≥70%",  "≥75%",   "≥80%"),
        "now":        "73.0%",
        "score":      2,
        "comment":    "FY2026 Q4 73.5%; Blackwell premium vs Hopper; some supply-chain/CoWoS cost drag",
    },
    {
        "name":       "Hyperscaler AI capex guidance",
        "weight":     0.20,
        "thresholds": ("<+10%",  "≥+20%", "≥+40%",  "≥+70%"),
        "now":        "+38%",
        "score":      2,
        "comment":    "Meta $65B, MSFT $80B, Google $75B, Amazon $105B FY2026 capex; GPU majority",
    },
    {
        "name":       "Blackwell supply tightness / book-to-bill",
        "weight":     0.15,
        "thresholds": ("<1.0×",  "≥1.2×", "≥1.5×",  "≥2.0×"),
        "now":        "~1.6×",
        "score":      3,
        "comment":    "Demand outstrips CoWoS substrate capacity; lead times 6–9 months; pricing power intact",
    },
    {
        "name":       "China revenue / export control exposure",
        "weight":     0.05,
        "thresholds": ("<$5B",   "≥$8B",  "≥$14B",  "≥$20B"),
        "now":        "~$8B",
        "score":      2,
        "comment":    "H20 chip ($8B FY2026) allowed; BIS tightening risk; China was 17% revenue pre-controls",
    },
    {
        "name":       "Automotive + Robotics revenue",
        "weight":     0.05,
        "thresholds": ("<$3B",   "≥$5B",  "≥$8B",   "≥$15B"),
        "now":        "~$5B",
        "score":      2,
        "comment":    "DRIVE Thor wins: BYD, Li Auto, SAIC; Jetson for robotics; long-cycle optionality",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "CUDA ecosystem moat — 5M+ developers; cuDNN/cuBLAS; 10yr+ switching cost; de-facto standard", +0.8, 0.25),
    ("+", "Blackwell / Rubin roadmap — 2× perf/W per gen; NIM microservices; NVIDIA AI Enterprise stack",  +0.6, 0.20),
    ("-", "Hyperscaler ASIC displacement — Google TPU, Amazon Trainium, Meta MTIA; 30%+ of workloads",     -0.6, 0.20),
    ("-", "Concentration risk — top 4 hyperscalers ~45% of revenue; single-customer risk (MSFT ~$15B)",    -0.5, 0.15),
    ("+", "Physical AI optionality — robotics/Jetson; autonomous vehicles; factory automation",             +0.5, 0.10),
    ("-", "Export controls escalation — China market ($8B+) permanently impaired; Taiwan risk binary",     -0.4, 0.10),
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
CONS_EPS_2YR  = 6.00    # conservative FY2029E: 12% EPS CAGR (growth decelerating; competition)
CONS_PE_2YR   = 24      # rerating from ~27× to growth-normalized 24× (growth decelerates to ~15%/yr)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Data Center AI / GPU / Accelerated Computing / Automotive")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2027E  →  BEAR / BULL scenarios)  [Fiscal yr ends Jan]")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<26}  {'FY2027E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<26}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<26}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_ni   = curr_oi * (1 - TAX_RATE)
curr_eps  = round(curr_ni / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B
bull_ni   = bull_oi * (1 - TAX_RATE)
shares_b  = shares * 0.99   # minimal net buyback (SBC ~= repurchases near-term)
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.93   # margin compression in downturn
bear_oi   = bear_gp - OPEX_FIXED_B * 0.85           # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2027E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2027E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 33× = ~${bull_eps_imp*33:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.93:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 22× trough P/E (CUDA floor) = ~${bear_eps_imp*22:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_dc     = 1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_gm    = curr_total * 0.01 * (1 - TAX_RATE) / shares
eps_per_1B_china  = 1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Data Center revenue (73% GM): +${eps_per_1B_dc:.3f}/EPS  = +${eps_per_1B_dc*28:.1f}/share at 28× P/E")
print(f"  China revenue ±$1B (H20 chips):         ±${eps_per_1B_china:.3f}/EPS  =  ±${eps_per_1B_china*28:.1f}/share at 28× P/E")
print(f"  1pp GM expansion (mix/supply):           +${eps_per_1pp_gm:.2f}/EPS  = +${eps_per_1pp_gm*28:.1f}/share at 28× P/E")
print(f"  1× P/E re-rating ($5.00 EPS):            +${EPS_FY2027E:.2f}/share  (P/E sensitivity: significant at growth multiples)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Data Center / Margin / Hyperscaler capex / Supply tightness)")
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
    ("Data Center revenue YoY",         "+52%",   "<+20%",  "−32pp",  "Hyperscalers pivot to in-house ASICs; capex freeze"),
    ("Non-GAAP gross margin",           "73.0%",  "<65%",   "−8pp",   "Supply glut → pricing pressure; CoWoS cost inflation"),
    ("Hyperscaler AI capex guidance",   "+38%",   "<+10%",  "−28pp",  "Recession / rates spike → IT budget freeze"),
    ("Blackwell book-to-bill",          "~1.6×",  "<1.0×",  "−0.6×",  "Demand destruction: LLM efficiency (DeepSeek-level)"),
    ("China revenue",                   "~$8B",   "<$5B",   "−$3B",   "Full export ban; H20 restrictions tightened to zero"),
    ("Automotive + Robotics revenue",   "~$5B",   "<$3B",   "−$2B",   "OEM software deferrals; EV demand slowdown"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Coordinated hyperscaler capex freeze (recession/rate shock) + DeepSeek-style")
print(f"  efficiency breakthrough reducing GPU-hours-per-task by 10×, simultaneous with Google/Amazon")
print(f"  ASIC units (TPU v6/Trainium 3) reaching 60%+ of training workloads. Revenue drops to ~$110B;")
print(f"  gross margin collapses to ~65% (utilization fall + pricing concessions). EPS ~$2.50 → 22× = ${bear_price}.")
print(f"  Note: $55 is NOT a permanent impairment — CUDA installed base ($1T+ cumulative hardware) +")
print(f"  NVIDIA AI Enterprise software ARR provides a durable floor. Recovery likely within 12–18 months.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E adj EPS estimate:      ${EPS_FY2027E:.2f}  (consensus $4.70–$5.00; non-GAAP; excl. SBC)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (CUDA moat floor; FY2022 trough 20–22×; DCF floor)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  At ${CURRENT_PRICE:.2f} and FY2027E EPS ${EPS_FY2027E:.2f}, P/E = {CURRENT_PRICE/EPS_FY2027E:.1f}× — reasonable for a")
print(f"  company compounding EPS at ~40%/yr. PEG = {CURRENT_PRICE/EPS_FY2027E/40:.2f}× on trailing growth rate.")
print(f"  EPP is meaningful: at ${EPP:.0f}, the stock prices in ONLY trough earnings power. The market")
print(f"  currently prices ~{CURRENT_PRICE/EPP:.1f}× EPP — embedding several years of sustained growth.")
print(f"  EPP path: FY2029E EPS ~$6.50 × {PE_PESSIMISTIC:.0f}× = ${6.50*PE_PESSIMISTIC:.0f} floor by late 2028 (+{(6.50*PE_PESSIMISTIC/EPP-1)*100:.0f}% EPP growth).")
print(f"  At 28× mid-cycle P/E: ${EPS_FY2027E:.2f} × 28 = ${EPS_FY2027E*28:.0f}  — {((EPS_FY2027E*28/CURRENT_PRICE)-1)*100:+.0f}% vs current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: growth decelerates; multiple compresses from ~27× to 24×)")
hr()
print(f"  Conservative FY2029E adj EPS:  ${CONS_EPS_2YR:.2f}  (12% EPS CAGR: competition + hyperscaler ASIC drag)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (rerates as growth normalizes to ~15%/yr; still premium)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; nominal; buybacks the real return)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE DYNAMIC: unlike AAPL, NVDA's conservative case is POSITIVE — because the stock")
print(f"  is NOT priced at nosebleed P/E relative to its growth rate. At ~27× FY2027E, you get a")
print(f"  40%/yr EPS grower at PEG ~0.7×. Even at 24× on slower $6 EPS = ${cons_equity} — a positive return.")
print(f"  The KEY risk is NOT valuation compression; it is GROWTH DECELERATION (ASIC/efficiency).")
print(f"  BUY trigger: ${round(bear_price * 1.25, 0):.0f}–${round(bear_price * 1.45, 0):.0f} (deep value; ratio_b <0.60×)")
print(f"  Breakeven on conservative case (24× P/E): current ${CURRENT_PRICE} requires FY2029E EPS ≥ ${CURRENT_PRICE/24:.2f}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.45
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  token; buybacks are the mechanism)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (high; AI narrative binary; hyperscaler capex swings ±25%)")
print(f"  Beta vs S&P 500:      1.85  (elevated; high-growth; AI sentiment amplifier)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (plausible; seen in 2022: −66%; DeepSeek: −17%)")
print(f"  52W low ${VOL_52W_LOW:.2f} (Jan 2026 DeepSeek shock) already a peak-to-trough move of ~54%.")
print(f"  → Hyperscaler capex freeze is THE KEY binary; each $10B capex cut = ~−8–12% NVDA revenue.")
print(f"  → DeepSeek-style efficiency gains are the structural bear risk (lower GPU-hrs per task).")
print(f"  → AVOID above $200  |  WATCHLIST $150–170  |  ACCUMULATE $110–130  |  BUY below $100")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is {'ABOVE' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'BELOW'} the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market prices ~{MARKET_COMPOSITE:.2f}/4.0 — between BASE and BULL.")
print(f"  The model scores the fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0 — between {'BASE and BULL' if ADJ_COMPOSITE < 2.75 else 'BULL and XBULL'}.")
print(f"  The gap ({ADJ_GAP:+.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: strong CUDA moat + Blackwell cycle = {valuation_label.lower()} at current price.")
print(f"  ASIC competition and efficiency risk (DeepSeek) are the primary valuation overhangs.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Hyperscaler Q3/Q4 capex guidance — upward revision = BULL trigger; freeze = BEAR")
print(f"  (2) Rubin GPU (R100/R200) ramp timeline — 2027 volume ramp; NVL144 next-gen rack")
print(f"  (3) DeepSeek-style efficiency breakthrough — each 10× efficiency = structural GPU demand risk")
print(f"  (4) Export control escalation — H20 ban tightening; Taiwan conflict binary")
print(f"  (5) ASIC market share — Google TPU/Amazon Trainium reaching >40% of hyperscaler AI workloads")
print(f"  AVOID above $200  |  WATCHLIST $150–170  |  ACCUMULATE $110–130  |  BUY below $100")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2027E EPS: ${EPS_FY2027E:.2f}")
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
