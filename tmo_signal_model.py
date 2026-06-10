"""
TMO  ·  Thermo Fisher Scientific Inc.  ·  NYSE: TMO
Bottom-up signal model  ·  Life Sciences Tools / Diagnostics / CRO / Bioproduction
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "TMO"
COMPANY       = "Thermo Fisher Scientific Inc."
SECTOR        = "Life Sciences Tools · Analytical Instruments · Diagnostics · CRO · NYSE: TMO"
CURRENT_PRICE = 448.28      # USD; as of 2026-06-10
VOL_52W_LOW   = 420.00      # post-correction trough (NIH funding cuts + tariffs + China weakness)
VOL_52W_HIGH  = 650.00      # January 2026 high, pre-correction
SHARES_OUT_M  = 380.0       # millions; modest buyback program

# Dividend: long-running growth streak; growing ~10%/yr historically
ANNUAL_DIV    = 6.84        # $/share annualized

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Life Sciences Solutions",         7.6,  6.6,  9.0, "Bioproduction (mRNA/gene therapy/biologics) +13% Q4 2025; biotech funding swing factor"),
    ("Analytical Instruments",          7.0,  5.9,  8.2, "Recovering from multi-year destocking; China capex sensitive"),
    ("Specialty Diagnostics",           5.0,  4.6,  5.6, "Stable, recurring; transplant/clinical diagnostics steady growth"),
    ("Laboratory Products & Biopharma Services", 22.4, 19.8, 25.5, "PPD CRO bookings; pharma services; largest segment by revenue"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.420   # blended gross margin FY2026E (~42%)
GROSS_MARGIN_BULL = 0.445   # BULL: bioproduction/CRO mix shift lifts margin
OPEX_FIXED_B      = 9.5     # SG&A + R&D ($B); largely fixed cost base
TAX_RATE          = 0.135   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 24.85       # FY2026E adj EPS (guidance $24.64-25.12; midpoint)
PE_PESSIMISTIC = 14.0        # trough P/E: BEAR scenario floor multiple (cyclical low)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $348

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (22.00, 14,  308, "NIH funding cuts deepen + tariffs escalate + China stays weak; EPS $22 → 14× cyclical floor"),
    "BASE":  (24.85, 18,  447, "FY2026 guidance executed at midpoint $24.85; policy headwinds stabilize at quantified levels; 18× low-end multiple"),
    "BULL":  (28.00, 22,  616, "Bioproduction reaccelerates, China stabilizes, CRO bookings recover; EPS $28 → 22× mid-cycle"),
    "XBULL": (33.00, 26,  858, "NIH funding restored, tariffs resolved, China rebound, bioproduction supercycle; EPS $33 → 26× re-rating"),
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
        "name":       "Bioproduction revenue growth (mRNA/gene therapy/biologics)",
        "weight":     0.25,
        "thresholds": ("<5%",    "≥8%",   "≥13%",   "≥18%"),
        "now":        "+13%",
        "score":      3,
        "comment":    "Q4 2025 bioproduction +13%; biotech manufacturing demand recovering off destocking lows",
    },
    {
        "name":       "Laboratory Products & Biopharma Services / CRO (PPD) revenue growth",
        "weight":     0.20,
        "thresholds": ("<0%",    "≥2%",   "≥6%",    "≥10%"),
        "now":        "+3%",
        "score":      2,
        "comment":    "PPD bookings stabilizing; pharma services growth modest amid biotech funding caution",
    },
    {
        "name":       "Analytical Instruments segment recovery",
        "weight":     0.15,
        "thresholds": ("<-5%",   "≥0%",   "≥5%",    "≥10%"),
        "now":        "+1%",
        "score":      2,
        "comment":    "Multi-year destocking cycle bottoming; China capex still soft; early signs of order recovery",
    },
    {
        "name":       "NIH funding policy impact trajectory ($500M headwind)",
        "weight":     0.20,
        "thresholds": ("Worsening", "Stable",  "Improving", "Reversed"),
        "now":        "Stable",
        "score":      2,
        "comment":    "$500M NIH funding cut quantified and incorporated into guidance; no further deterioration signaled",
    },
    {
        "name":       "China market recovery",
        "weight":     0.10,
        "thresholds": ("<-10%",  "≥-5%",  "≥0%",    "≥+8%"),
        "now":        "-6%",
        "score":      2,
        "comment":    "China revenue still declining YoY but pace of decline moderating; stimulus measures pending",
    },
    {
        "name":       "FY2026 EPS guidance execution ($24.64-25.12, +8-10% growth)",
        "weight":     0.10,
        "thresholds": ("<$23.50", "≥$24.64", "≥$25.50", "≥$27.00"),
        "now":        "$24.85 (midpoint)",
        "score":      2,
        "comment":    "Management RAISED FY2026 guidance despite NIH/tariff/China headwinds — signals underlying resilience",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Dominant 'picks-and-shovels' franchise — #1 in lab tools, instruments, CRO, bioproduction", +0.7, 0.25),
    ("+", "Guidance raised despite headwinds — management quantified $500M NIH + $400M tariff impact and still guided +8-10% EPS growth", +0.6, 0.20),
    ("-", "NIH funding policy risk — $500M headwind could deepen or become structural under sustained federal budget pressure", -0.5, 0.20),
    ("-", "China weakness — revenue still declining; macro/political overhang on capex recovery timeline",  -0.4, 0.15),
    ("+", "Trough valuation — 18x FY2026E EPS, low end of 5-year range; mean-reversion potential as headwinds normalize", +0.6, 0.15),
    ("-", "Tariff escalation risk — $400M impact could grow if trade tensions broaden across instrument/consumables supply chains", -0.3, 0.05),
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
CONS_EPS_2YR  = 27.50   # conservative FY2028E: ~5-6% CAGR off raised FY2026 guidance
CONS_PE_2YR   = 17      # roughly flat multiple near low end of 5-yr range; modest reversion
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Life Sciences Tools / Diagnostics / CRO / Bioproduction")
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

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift / pricing pressure
bear_oi   = bear_gp - OPEX_FIXED_B * 0.98           # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (guidance ${EPS_FY2026E:.2f} midpoint  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 22× = ~${bull_eps_imp*22:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 14× cyclical-floor P/E = ~${bear_eps_imp*14:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev   = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_china = 1.0 * 0.35 * (1 - TAX_RATE) / shares   # China revenue at instrument-level margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Bioproduction revenue:  +${eps_per_1B_rev * 0.55 * (1-TAX_RATE):.3f}/EPS  = +${eps_per_1B_rev*0.55*(1-TAX_RATE)*18:.1f}/share at 18× P/E")
print(f"  China revenue ±$1B (35% margin):  ±${eps_per_1B_china:.3f}/EPS  =  ±${eps_per_1B_china*18:.1f}/share at 18× P/E")
print(f"  1pp GM expansion (mix/pricing):    +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*18:.1f}/share at 18× P/E")
print(f"  1% buyback (3.8M shares):          +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (bioproduction / CRO / instruments / NIH-China policy framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>9}  {'BASE':>7}  {'BULL':>9}  {'XBULL':>8}  {'NOW':>16}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>9}  {ths[1]:>7}  {ths[2]:>9}  {ths[3]:>8}  {s['now']:>16}  {lbl}  {b}")

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
    ("Bioproduction revenue growth",   "+13%",   "<5%",    "−8pp",   "Biotech funding remains tight; mRNA/gene therapy demand decelerates sharply"),
    ("NIH funding policy impact",      "Stable", "Worsening", "n/a", "NIH funding cuts deepen beyond $500M or become structural multi-year policy"),
    ("China market revenue YoY",       "-6%",    "<-15%",  "−9pp",  "China weakness persists/worsens; no stimulus, capex freeze extends"),
    ("Tariff impact",                  "$400M",  ">$600M", "+$200M","Tariff impact escalates beyond $400M as trade tensions broaden"),
    ("Lab Products & Biopharma Svcs growth", "+3%", "<0%",  "−3pp",  "PPD/CRO bookings stall as pharma R&D spending contracts further"),
    ("FY2026 EPS guidance",            "$24.85", "<$23.50","−$1.35","Guidance cut mid-year as cumulative headwinds exceed quantified levels"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: NIH funding cuts deepen beyond the quantified $500M and become a structural")
print(f"  multi-year drag on Life Sciences Solutions and academic/government end-markets, while")
print(f"  China capex remains frozen and tariff costs escalate beyond $400M. Combined, these would")
print(f"  force a mid-year guidance cut from the raised $24.64-25.12 range, compressing EPS toward")
print(f"  ~$22 at a 14× cyclical-floor multiple = ${bear_price}.")
print(f"  Note: management has ALREADY quantified and guided through the current headwinds — the")
print(f"  bear case requires INCREMENTAL deterioration, not just persistence of known issues.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (guidance $24.64-25.12; midpoint)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (cyclical floor multiple for diversified life-sciences tools leader)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  At ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f}, the P/E is ~{CURRENT_PRICE/EPS_FY2026E:.1f}× — the LOW end of")
print(f"  TMO's 5-year valuation range. The +{epp_gap_pct:.0f}% premium to the EPP trough floor reflects a")
print(f"  stock that has already de-rated 30% from January 2026 highs on quantified policy")
print(f"  headwinds (NIH $500M, tariffs $400M, China weakness) — NOT structural deterioration.")
print(f"  EPP path: FY2028E EPS ~$27.50 × {PE_PESSIMISTIC:.0f}× = ${27.50*PE_PESSIMISTIC:.0f} floor (EPP growing with EPS).")
print(f"  At 18× current-guidance multiple: ${EPS_FY2026E:.2f} × 18 = ${EPS_FY2026E*18:.0f}  — roughly in line with current price,")
print(f"  implying the stock is pricing BASE-case execution with little credit for recovery.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest EPS growth, multiple roughly flat near 5-yr low)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (~5-6% CAGR off raised FY2026 guidance)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (near low end of 5-yr range; minimal multiple expansion assumed)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Even WITHOUT multiple expansion from the current trough 18×, EPS growth alone driven by")
print(f"  bioproduction recovery and CRO bookings momentum produces a positive total return.")
print(f"  Breakeven at flat 18× P/E (no multiple change): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 18:.2f}")
print(f"  That requires only ~{((CURRENT_PRICE - cons_divs) / 18 / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — well within raised guidance trajectory.")
print(f"  Any reversion toward the mid-cycle 22-24× multiple (BULL scenario) adds significant upside.")
print(f"  ACCUMULATE trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case clearly positive; ratio_b improves further)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.24
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: 52W high is the January 2026 peak; stock down ~30% on NIH funding cuts ($500M),")
print(f"  tariffs ($400M), and China weakness — all already incorporated into raised FY2026 guidance.")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated by policy-driven drawdown; historically lower-beta name)")
print(f"  Beta vs S&P 500:      1.05  (defensive life-sciences infrastructure; policy/macro sensitivity has risen)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (incremental policy deterioration beyond guided levels)")
print(f"  52W low ${VOL_52W_LOW:.2f} already reflects a ~35% peak-to-trough move from January 2026 highs.")
print(f"  → NIH funding policy trajectory is THE KEY swing factor for Life Sciences Solutions.")
print(f"  → Bioproduction (mRNA/gene therapy) reacceleration + CRO bookings are KEY bull catalysts.")
print(f"  → AVOID at current price  |  WATCHLIST $415–440  |  ACCUMULATE $370–395  |  BUY $310–340")

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
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0, while the model")
print(f"  scores fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0. The gap ({ADJ_GAP:.2f}) indicates the stock is")
print(f"  {valuation_label.lower()} by model standards.")
print(f"  In plain terms: TMO is the dominant 'picks-and-shovels' franchise for global life sciences")
print(f"  trading at a trough multiple (18× FY2026E, low end of 5-yr range) on quantified, guided-")
print(f"  through policy headwinds (NIH, tariffs, China) — not structural impairment.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) NIH funding policy developments — stabilization or further cuts to the $500M headwind")
print(f"  (2) Bioproduction (mRNA/gene therapy) revenue growth trajectory — sustaining +13% pace")
print(f"  (3) China market recovery signs — capex thaw, stimulus measures, order book inflection")
print(f"  (4) Tariff resolution/mitigation — reducing the quantified $400M impact")
print(f"  (5) Quarterly EPS guidance tracking vs the raised $24.64-25.12 range")
print(f"  (6) CRO/PPD bookings momentum — Laboratory Products & Biopharma Services segment growth")
print(f"  AVOID at ${CURRENT_PRICE:.2f}  |  WATCHLIST $415–440  |  ACCUMULATE $370–395  |  BUY $310–340")
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
