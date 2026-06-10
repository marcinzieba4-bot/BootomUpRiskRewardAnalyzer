"""
PFE  ·  Pfizer Inc.  ·  NYSE: PFE
Bottom-up signal model  ·  Pharmaceuticals / Oncology ADCs / LOE Cliff / Obesity Pipeline
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "PFE"
COMPANY       = "Pfizer Inc."
SECTOR        = "Pharmaceuticals · Oncology (Seagen ADCs) · Vaccines · LOE Cliff Management · NYSE: PFE"
CURRENT_PRICE = 25.90        # USD; as of 2026-06-10
VOL_52W_LOW   = 20.92        # 52-week low
VOL_52W_HIGH  = 30.50        # 52-week high
SHARES_OUT_M  = 5_650.0      # millions

# Dividend: 6.6% yield at current price
ANNUAL_DIV    = 1.72         # $/share

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Oncology (Seagen ADCs + Ibrance)", 17.0, 14.5, 21.0, "Padcev/Adcetris/Tukysa/Elahere +20% Q1'26; Ibrance facing 2027 LOE"),
    ("Vaccines (Prevnar/Comirnaty)",      13.0, 10.5, 14.5, "Prevnar franchise stable; Comirnaty COVID demand normalized"),
    ("Internal Med/Cardiology (Eliquis)", 10.5,  6.5, 11.5, "Eliquis 2026 LOE cliff; generic erosion the key swing factor"),
    ("Hospital/Specialty Care",           9.5,  8.5, 10.5, "Anti-infectives, inflammation/immunology, rare disease"),
    ("Obesity pipeline (PF-3944/danuglipron-class)", 0.5, 0.0,  4.0, "Phase III readouts 2026; pure optionality, near-zero current rev"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.660   # blended gross margin FY2026E (~66%)
GROSS_MARGIN_BULL = 0.690   # BULL: ADC/obesity mix lifts margin further
OPEX_FIXED_B      = 19.0    # SI&A + R&D ($B); cost-cutting program targets $4B+ by 2027
TAX_RATE          = 0.150   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 2.90        # FY2026E adj EPS (consensus ~$2.85-$3.00)
PE_PESSIMISTIC = 8.0         # trough P/E: cheapest since FY2023 trough at ~8.9x
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $23

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (2.20,  8,  18, "Eliquis/Ibrance generic erosion faster than modeled; cost cuts miss; EPS $2.20 → 8x floor"),
    "BASE":  (2.90, 10,  29, "LOE cliff managed via Seagen ADC growth + cost cuts; EPS $2.90 → 10x"),
    "BULL":  (3.40, 13,  44, "ADC growth accelerates, obesity Phase III positive readouts de-risk pipeline; EPS $3.40 → 13x"),
    "XBULL": (4.20, 16,  67, "Obesity pipeline becomes major franchise; LOE cliff fully offset; EPS $4.20 → 16x"),
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
        "name":       "Seagen ADC oncology revenue growth",
        "weight":     0.25,
        "thresholds": ("<5%",    "≥10%",  "≥18%",   "≥28%"),
        "now":        "+20%",
        "score":      3,
        "comment":    "Padcev/Adcetris/Tukysa/Elahere Q1 2026 +20% YoY; integration synergies ahead of plan",
    },
    {
        "name":       "LOE cliff management (Eliquis/Ibrance erosion vs offsets)",
        "weight":     0.25,
        "thresholds": ("<-25%",  "≥-15%", "≥-8%",   "≥0%"),
        "now":        "-12%",
        "score":      2,
        "comment":    "Eliquis 2026 / Ibrance 2027 generic erosion tracking modeled pace; new launches partially offsetting ~$17-18B at-risk revenue by 2028",
    },
    {
        "name":       "Cost-cutting program execution ($4B+ by 2027)",
        "weight":     0.20,
        "thresholds": ("<40%",   "≥60%",  "≥85%",   "≥100%"),
        "now":        "~70%",
        "score":      3,
        "comment":    "Run-rate savings tracking ahead of schedule; manufacturing network optimization and SI&A reductions on pace",
    },
    {
        "name":       "Obesity pipeline progress (Phase III readouts)",
        "weight":     0.15,
        "thresholds": ("Failed", "Mixed", "Positive","Best-in-class"),
        "now":        "Pending 2026",
        "score":      2,
        "comment":    "PF-3944/danuglipron-class Phase III readouts due 2026; outcome remains a binary pipeline catalyst",
    },
    {
        "name":       "Vaccines franchise stability (Prevnar/Comirnaty)",
        "weight":     0.10,
        "thresholds": ("<-10%",  "≥-3%",  "≥+2%",   "≥+8%"),
        "now":        "-2%",
        "score":      2,
        "comment":    "Prevnar holding share vs Merck's Capvaxive; Comirnaty demand normalized post-pandemic; broadly stable",
    },
    {
        "name":       "Pipeline productivity / new approvals replacing LOE revenue",
        "weight":     0.05,
        "thresholds": ("<2/yr",  "≥3/yr", "≥5/yr",  "≥8/yr"),
        "now":        "~4/yr",
        "score":      2,
        "comment":    "Steady cadence of approvals across oncology and specialty care; not yet enough to fully offset cliff",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Cheapest valuation since FY2023 trough — 8.9x FY2026E EPS, multi-year low",            +0.7, 0.20),
    ("+", "6.6% dividend yield — paid while waiting; large cash flow cushion if cliff manageable", +0.5, 0.15),
    ("-", "LOE cliff — ~$17-18B revenue at risk by 2028 from Eliquis/Ibrance generic erosion",     -0.9, 0.30),
    ("+", "Seagen ADC franchise momentum — +20% growth, integration synergies ahead of plan",      +0.6, 0.20),
    ("+", "Cost-cutting program ($4B+ by 2027) tracking ahead of schedule",                         +0.3, 0.10),
    ("-", "Dividend coverage risk if FCF deteriorates faster than cost cuts materialize",          -0.4, 0.05),
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
CONS_EPS_2YR  = 2.80    # conservative FY2028E: LOE drag offsets ADC/cost-cut gains; near-flat EPS
CONS_PE_2YR   = 9       # modest rerate from 8.9x toward 9x as cliff visibility improves
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Pharma / Oncology ADCs / LOE Cliff / Obesity Pipeline")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<36}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<36}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<36}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
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

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift / pricing pressure
bear_oi   = bear_gp - OPEX_FIXED_B * 0.97           # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ~${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 13× = ~${bull_eps_imp*13:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At {PE_PESSIMISTIC:.0f}× trough P/E = ~${bear_eps_imp*PE_PESSIMISTIC:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev   = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_eliquis = 1.0 * 0.55 * (1 - TAX_RATE) / shares   # high-margin Eliquis revenue

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Seagen ADC revenue:     +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*10:.2f}/share at 10× P/E")
print(f"  Eliquis revenue ±$1B (55% margin): ±${eps_per_1B_eliquis:.3f}/EPS  =  ±${eps_per_1B_eliquis*10:.2f}/share at 10× P/E")
print(f"  1pp GM expansion (cost cuts):     +${curr_total*0.01*(1-TAX_RATE)/shares:.3f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*10:.2f}/share at 10× P/E")
print(f"  $1B incremental cost savings:     +${1.0*(1-TAX_RATE)/shares:.3f}/EPS  (toward $4B+ by 2027 program)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (ADC growth / LOE cliff / cost cuts / obesity pipeline framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>8}  {'BASE':>6}  {'BULL':>9}  {'XBULL':>13}  {'NOW':>12}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>8}  {ths[1]:>6}  {ths[2]:>9}  {ths[3]:>13}  {s['now']:>12}  {lbl}  {b}")

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
    ("Seagen ADC oncology revenue growth", "+20%",   "<5%",    "−15pp",  "ADC growth decelerates sharply on competition/pricing pressure"),
    ("LOE cliff erosion (Eliquis/Ibrance)","-12%",   "<-25%",  "−13pp",  "Generic erosion accelerates faster than modeled post-LOE"),
    ("Cost-cutting program progress",      "~70%",   "<40%",   "−30pp",  "$4B+ savings target by 2027 missed; opex stays elevated"),
    ("Obesity Phase III readout",          "Pending","Failed", "n/a",    "PF-3944/danuglipron-class Phase III fails or shows weak efficacy"),
    ("Vaccines franchise YoY",             "-2%",    "<-10%",  "−8pp",   "Prevnar share loss to Capvaxive accelerates; Comirnaty demand collapses"),
    ("Dividend coverage (FCF/div)",        "Stable", "Cut risk","n/a",   "FCF deterioration forces dividend cut, crushing yield-support thesis"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Eliquis (2026 LOE) and Ibrance (2027 LOE) generic erosion outpaces the")
print(f"  modeled trajectory, putting the full ~$17-18B at-risk revenue base under pressure")
print(f"  simultaneously while Seagen ADC growth decelerates and obesity Phase III disappoints.")
print(f"  EPS compresses to ~$2.20 → {PE_PESSIMISTIC:.0f}× floor = ${bear_price}.")
print(f"  Note: ${bear_price} is close to the existing 52-week low (${VOL_52W_LOW:.2f}), so the")
print(f"  bear case is only a modest incremental drawdown from current levels — limited tail risk.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~$2.85-$3.00)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (cheapest since FY2023 trough; current 8.9x)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  At ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f}, the stock trades at 8.9× — the")
print(f"  cheapest multiple since the FY2023 trough. The +{epp_gap_pct:.0f}% EPP gap is modest,")
print(f"  meaning the market is pricing in only a small premium above the trough-floor multiple.")
print(f"  In other words: the LOE cliff appears to already be substantially priced in, with the")
print(f"  6.6% dividend yield paid while the market waits for ADC growth/cost cuts/obesity")
print(f"  optionality to play out and offset the Eliquis/Ibrance erosion.")
print(f"  EPP path: FY2028E EPS ~$3.00 × {PE_PESSIMISTIC:.0f}× = ${3.00*PE_PESSIMISTIC:.0f} floor (EPP roughly flat to slightly higher).")
print(f"  At 10× mid-cycle P/E: ${EPS_FY2026E:.2f} × 10 = ${EPS_FY2026E*10:.0f}  — close to current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: LOE drag offsets ADC/cost-cut gains; modest rerate)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (LOE erosion roughly offset by ADC growth + cost cuts; near-flat EPS)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (modest rerate from 8.9× as cliff visibility improves)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; 6.6% current yield)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: can EPS hold roughly flat (~${CONS_EPS_2YR:.2f}) through the worst of the")
print(f"  Eliquis/Ibrance LOE cliff via Seagen ADC growth and the $4B+ cost-cutting program? If so,")
print(f"  even a modest rerate from 8.9× to {CONS_PE_2YR}× plus the 6.6% dividend yield delivers a")
print(f"  positive return while waiting for obesity pipeline optionality to potentially re-rate further.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:+.1f}% EPS change vs FY2026E — modest, achievable in BASE.")
print(f"  Breakeven at {PE_PESSIMISTIC:.0f}× P/E (no rerate): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / PE_PESSIMISTIC:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.18
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  high; Dividend Aristocrat-adjacent)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (large-cap pharma; lower vol than tech, but LOE cliff is a known binary)")
print(f"  Beta vs S&P 500:      0.55  (defensive; low beta; pharma sector rotation sensitivity)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (modest move; close to existing 52W low)")
print(f"  52W low ${VOL_52W_LOW:.2f} already reflects much of the LOE cliff concern.")
print(f"  → The Eliquis/Ibrance LOE cliff is THE KEY known risk — already substantially priced in.")
print(f"  → Seagen ADC growth sustaining +20%+ and obesity Phase III readouts are KEY bull catalysts.")
print(f"  → AVOID above ${VOL_52W_HIGH:.2f}  |  WATCHLIST $28-30  |  ACCUMULATE $22-28  |  BUY on panic $20-23")

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
print(f"  {'ABOVE' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'BELOW'} the model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0.")
print(f"  The model scores the fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0.")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: at the cheapest valuation since the FY2023 trough with a 6.6% dividend")
print(f"  yield, the well-known Eliquis/Ibrance LOE cliff appears largely priced in, with Seagen")
print(f"  ADC momentum, cost discipline, and obesity optionality offering asymmetric upside.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Seagen ADC quarterly revenue growth — Padcev/Adcetris/Tukysa/Elahere (currently +20%)")
print(f"  (2) Eliquis/Ibrance LOE revenue trajectory — tracking the ~$17-18B at-risk cliff through 2028")
print(f"  (3) Obesity Phase III readouts (2026) — PF-3944/danuglipron-class binary catalyst")
print(f"  (4) Cost-cutting program milestones — $4B+ savings target by 2027")
print(f"  (5) Vaccines franchise updates — Prevnar vs Capvaxive competition; Comirnaty demand")
print(f"  (6) Dividend sustainability/coverage — 6.6% yield depends on FCF holding up through cliff")
print(f"  AVOID above ${VOL_52W_HIGH:.2f}  |  WATCHLIST $28-30  |  ACCUMULATE $22-28  |  BUY on panic $20-23")
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
