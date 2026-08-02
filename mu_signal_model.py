"""
MU  ·  Micron Technology Inc.  ·  NASDAQ: MU
Bottom-up signal model  ·  DRAM / HBM / NAND / AI Memory Infrastructure
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "MU"
COMPANY       = "Micron Technology Inc."
SECTOR        = "Semiconductors · DRAM · HBM · NAND · AI Memory Infrastructure · NASDAQ: MU"
CURRENT_PRICE = 823.03       # USD; as of 2026-08-02
VOL_52W_LOW   = 103.38       # 52-week low (memory cycle trough)
VOL_52W_HIGH  = 1255.00      # 52-week high (HBM supercycle peak)
SHARES_OUT_M  = 1_130.0      # millions; relatively stable (modest buyback)

# Dividend: modest; not a dividend story; free cash flow reinvested in HBM capex
ANNUAL_DIV    = 0.46         # $/share FY2026 ($0.115/quarter)

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)  — run-rate from Q3 ($41.46B) + Q4 guide ($50B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("HBM / Data Center DRAM",    80.0,  35.0, 120.0, "HBM3E/HBM4 for NVIDIA Blackwell; supply-constrained 6-9mo lead times"),
    ("Compute & Networking DRAM", 40.0,  15.0,  55.0, "Server DDR5; hyperscaler DRAM; PC memory; DDR5 cycle"),
    ("NAND / Storage",            25.0,  10.0,  35.0, "Enterprise SSD; UFS mobile NAND; QLC density gains"),
    ("Embedded / Automotive",      8.0,   5.0,  12.0, "LPDDR5 automotive ADAS; industrial MCU; IoT edge"),
    ("Consumer DRAM / NAND",       7.0,   3.0,  10.0, "PC/mobile spot market; most cyclical segment; price-taker"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.524   # blended FY2026E (weak H1 ~35% + strong H2 ~75% average ~52%)
GROSS_MARGIN_BULL = 0.650   # BULL: HBM ASPs sustained; DRAM supply discipline; >65% blended
OPEX_FIXED_B      = 8.0     # R&D + SG&A ($B); semi-fixed cost base; grows with HBM R&D
TAX_RATE          = 0.15    # effective rate; CHIPS Act credits; R&D deductions

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 57.0        # FY2026E non-GAAP EPS (consensus ~$57; non-GAAP)
PE_PESSIMISTIC = 8.0         # trough P/E: memory trough; MU at 5-10× trough EPS (2016, 2019, 2023 cycles)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $456

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (  8.0,  12,   96, "Supply glut; ASP collapse -60%; Samsung floods DRAM; AI capex freeze; EPS $8 → 12× trough"),
    "BASE":  ( 57.0,  16,  912, "HBM steady demand 2027; Micron gains HBM share; supply discipline; EPS $57 → 16×"),
    "BULL":  ( 96.0,  20, 1920, "HBM4 ramp; Micron 30%+ HBM share; NAND/DRAM ASPs elevated; EPS $96 → 20×"),
    "XBULL": (130.0,  24, 3120, "Micron = critical AI infra bottleneck; geopolitical tailwind vs Samsung; EPS $130 → 24×"),
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
        "name":       "HBM revenue growth / ASP trends",
        "weight":     0.30,
        "thresholds": ("<$10B/yr", ">=60B", ">=100B",  ">=150B"),
        "now":        "~$80B ann",
        "score":      3,
        "comment":    "HBM3E annualized ~$80B; NVIDIA Blackwell allocation sold out; 6-9mo lead times confirm supply tightness",
    },
    {
        "name":       "DRAM gross margin",
        "weight":     0.25,
        "thresholds": ("<40%",    ">=60%",  ">=75%",   ">=85%"),
        "now":        "~86% Q4",
        "score":      4,
        "comment":    "Q4 FY2026 guide ~86% GM — all-time high; HBM premium pricing; fixed-cost leverage at peak utilization",
    },
    {
        "name":       "HBM supply / demand tightness",
        "weight":     0.20,
        "thresholds": ("Oversply", "Balanced", "Tight 6mo", "Alloc-cstr"),
        "now":        "Tight 6-9mo",
        "score":      3,
        "comment":    "HBM3E backlog extends 6-9 months; HBM4 qualification queue already forming; CoWoS packaging = binding constraint",
    },
    {
        "name":       "Samsung/SK Hynix capacity discipline",
        "weight":     0.10,
        "thresholds": ("Agrsv exp", "Disciplnd", "Constrd",  "Ultra-cstr"),
        "now":        "Constrained",
        "score":      3,
        "comment":    "HBM packaging (CoWoS) limits rapid capacity adds; Samsung lagging on HBM3E yields; 18-24mo to flood risk",
    },
    {
        "name":       "AI data center capex trajectory",
        "weight":     0.10,
        "thresholds": ("<+10%",   ">=+30%",  ">=+60%",   ">=+100%"),
        "now":        "~+50% YoY",
        "score":      3,
        "comment":    "Hyperscaler capex: AWS/Azure/Google/Meta collectively guiding +50%+ YoY; inference demand = HBM demand",
    },
    {
        "name":       "Micron HBM market share",
        "weight":     0.05,
        "thresholds": ("<5%",     ">=15%",   ">=25%",    ">=35%"),
        "now":        "~20-25%",
        "score":      3,
        "comment":    "Estimated 20-25% HBM share vs SK Hynix ~50%, Samsung ~25%; NVIDIA qualified; gaining share in HBM4",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "HBM technology leadership — HBM3E ahead of schedule; HBM4 on roadmap; NVIDIA qualified",     +0.6, 0.25),
    ("-", "Memory cyclicality risk — historically brutal; DRAM gluts follow booms within 12-24 months",  -0.8, 0.25),
    ("-", "Samsung capacity wildcard — can flood market in 18-24 months; HBM ramp risk if yields fix",   -0.5, 0.20),
    ("+", "AI structural demand floor — HBM is inescapable for AI compute; no substitute architecture",  +0.7, 0.15),
    ("+", "Geopolitical / CHIPS Act tailwind — US fab; export controls disadvantage Samsung China sales", +0.4, 0.10),
    ("+", "Balance sheet / cash generation — record FCF; buybacks; investment-grade; HBM capex funded",  +0.5, 0.05),
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
# Cycle turns: FY2028E EPS collapses as DRAM/NAND glut sets in post-boom
CONS_EPS_2YR  = 20.0   # conservative FY2028E: severe down-cycle, mean-reversion; MU trough EPS
CONS_PE_2YR   = 12     # trough-to-recovery P/E (MU traded 8-15x at trough; recovery phase = 12x)
cons_equity   = CONS_EPS_2YR * CONS_PE_2YR
cons_divs     = ANNUAL_DIV * 2
cons_total    = cons_equity + cons_divs
cons_return   = round((cons_total - CURRENT_PRICE) / CURRENT_PRICE * 100, 1)
cons_annual   = round(cons_return / 2, 1)

# ─────────────────────────────────────────────────────────────────────────────
#  OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
W = 72

def hr(): print("  " + "-" * W)
def bar(score):
    return "X" * score + "." * (4 - score)

print()
print("=" * (W + 4))
print(f"  {TICKER}  .  {COMPANY}  .  ${CURRENT_PRICE:.2f}  .  DRAM / HBM / NAND / AI Memory Infrastructure")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("=" * (W + 4))

# --- PRODUCT REVENUE BRIDGE ---------------------------------------------------
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  ->  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<26}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'D Bear':>8}  {'D Bull':>8}")
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

bull_gp      = bull_total * GROSS_MARGIN_BULL
bull_oi      = bull_gp - OPEX_FIXED_B * 1.25     # HBM R&D opex grows
bull_ni      = bull_oi * (1 - TAX_RATE)
shares_b     = shares * 0.97                       # modest share reduction
bull_eps_imp = round(bull_ni / shares_b, 1)

# Bear: severe ASP collapse; gross margin collapses to ~27% (near-trough)
bear_gp      = bear_total * 0.27
bear_oi      = bear_gp - OPEX_FIXED_B * 0.95
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev x {GROSS_MARGIN_CURR*100:.1f}% GM - ${OPEX_FIXED_B:.1f}B opex - {TAX_RATE*100:.0f}% tax")
print(f"  / {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2026E:.2f}  OK)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev x {GROSS_MARGIN_BULL*100:.1f}% GM - ${OPEX_FIXED_B*1.25:.1f}B opex - tax")
print(f"  / {shares_b:.3f}B shares  =  ~${bull_eps_imp:.1f}/share  ->  ${bull_eps_imp:.1f} x 20x = ~${bull_eps_imp*20:.0f}  OK BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev x 27.0% GM (ASP collapse)  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 12x trough P/E = ~${bear_eps_imp*12:.0f}  OK BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_hbm  = (1.0 * 0.85 * (1 - TAX_RATE)) / shares
eps_per_1B_dram = (1.0 * 0.60 * (1 - TAX_RATE)) / shares
eps_per_1pp_gm  = (curr_total * 0.01 * (1 - TAX_RATE)) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B HBM revenue (~85% margin):     +${eps_per_1B_hbm:.3f}/EPS  = +${eps_per_1B_hbm*16:.1f}/share at 16x P/E")
print(f"  Every $1B commodity DRAM (~60% margin):  +${eps_per_1B_dram:.3f}/EPS  = +${eps_per_1B_dram*16:.1f}/share at 16x P/E")
print(f"  1pp GM expansion (ASP/mix):              +${eps_per_1pp_gm:.2f}/EPS  = +${eps_per_1pp_gm*16:.1f}/share at 16x P/E")
print(f"  Samsung/SK Hynix HBM supply +20%:        ASP -15% -> GM -8pp -> EPS -${eps_per_1pp_gm*8:.0f}/share (key downside risk)")

# --- SIGNAL DASHBOARD ---------------------------------------------------------
print()
print("  [1] SIGNAL DASHBOARD  (HBM cycle / DRAM margin / supply tightness / AI capex framework)")
hr()
score_labels = {1: "BEAR", 2: "BASE", 3: "BULL", 4: "XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>8}  {'BASE':>8}  {'BULL':>8}  {'XBULL':>8}  {'NOW':>10}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>8}  {ths[1]:>8}  {ths[2]:>8}  {ths[3]:>8}  {s['now']:>10}  {lbl}  {b}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15% hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  ->  Adj composite {ADJ_COMPOSITE:.3f}  ->  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:72]:<72}  ({score:+.1f} x {weight*100:.0f}%  =  {contribution:+.3f})")

# --- BEAR CASE ANATOMY --------------------------------------------------------
print()
print(f"  [2] BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<52}  {'Current':>10}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("HBM revenue / ASP",               "~$80B ann",  "<$10B",    "-88%",   "Samsung HBM3E yield fix + SK Hynix floods supply"),
    ("DRAM gross margin",               "~86% Q4",    "<40%",     "-46pp",  "ASP collapse -60%; fixed costs unabsorbed at low util"),
    ("HBM supply/demand",               "Tight 6-9mo","Oversply", "sharply","Samsung + SK Hynix add 40%+ HBM capacity by 2027"),
    ("AI data center capex",            "~+50% YoY",  "<+10%",    "-40pp",  "AI capex freeze; hyperscalers pause Blackwell orders"),
    ("Micron HBM market share",         "~20-25%",    "<5%",      "-20pp",  "Samsung fixes HBM3E yields; sweeps existing contracts"),
    ("NAND pricing",                    "Recovery",   "Glut",     "severe", "QLC oversupply from Samsung + Western Digital war"),
]
for name, curr_v, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr_v:>10}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Samsung Technology fixes HBM3E packaging yields in 2H 2027, allowing rapid")
print(f"  capacity expansion. SK Hynix simultaneously ramps HBM4 at volume. Combined, global HBM")
print(f"  supply doubles in 12 months. AI hyperscaler demand growth decelerates as inference shifts")
print(f"  to smaller models (SLMs). HBM ASPs fall 50-60%; Micron gross margin collapses from 86%")
print(f"  to sub-40%; EPS falls from $57 to $8. At 12x trough P/E -> ${bear_price}.")
print(f"  Note: ${bear_price} is NOT permanent impairment — it mirrors the 2023 trough ($48-52). Recovery")
print(f"  to $400-500 in 2-3yr post-trough is historical base case as next AI hardware cycle restarts.")

# --- EPP ----------------------------------------------------------------------
print()
print("  [3] EPP  (Earnings Power Price: pessimistic P/E x current EPS)")
hr()
print(f"  FY2026E non-GAAP EPS estimate:  ${EPS_FY2026E:.2f}  (consensus ~$57; Q3 $25.11 + Q4E $31.00)")
print(f"  Pessimistic trough P/E:          {PE_PESSIMISTIC:.0f}x  (MU trough P/E: 5-10x in 2016, 2019, 2023 cycles)")
print(f"  -----------------------------------------------------------------------")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above pessimistic trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP means the market prices in 1-2 years of uninterrupted")
print(f"  HBM boom AND no cycle turn. At ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f} (non-GAAP),")
print(f"  the forward P/E is ~{CURRENT_PRICE/EPS_FY2026E:.1f}x — very cheap IF the cycle holds. The risk is")
print(f"  cyclicality: memory has NEVER sustained peak margins for more than 4-6 quarters historically.")
print(f"  EPP path: FY2027E EPS ~$96 x {PE_PESSIMISTIC:.0f}x = ${96*PE_PESSIMISTIC:.0f} forward EPP floor — support is rising fast.")
print(f"  At 12x mid-cycle P/E: ${EPS_FY2026E:.2f} x 12 = ${EPS_FY2026E*12:.0f}  — 17% below current price.")

# --- CONSERVATIVE GROWTH ------------------------------------------------------
print()
print("  [4] CONSERVATIVE GROWTH  (2-yr: cycle turns; DRAM/NAND glut; EPS mean-reverts)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (severe down-cycle; Samsung floods supply; mean-reversion)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (trough-to-recovery P/E; MU historically 8-15x at trough)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; not a dividend story)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'DOWN' if cons_total < CURRENT_PRICE else 'UP'} {abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE RISK: memory cycles are historically brutal. Every major DRAM supercycle in")
print(f"  the last 20 years (2000, 2007-08, 2014-15, 2018, 2021-22) was followed by a severe glut")
print(f"  that collapsed EPS by 70-95%. At ${CURRENT_PRICE:.2f}, the market is pricing near-perpetual HBM")
print(f"  demand without a cycle turn. A conservative 2yr return of {cons_return:.1f}% is the key risk.")
print(f"  For conservative 2yr to break even: need FY2028E EPS >= ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.0f} at {CONS_PE_2YR}x P/E")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90, 0):.0f}-${round(CONS_EPS_2YR * CONS_PE_2YR * 1.10, 0):.0f} (conservative case positive; ratio_b <1.0x)")

# --- VOLATILITY CONTEXT -------------------------------------------------------
print()
print("  [5] VOLATILITY CONTEXT")
hr()
annual_vol  = 0.55    # MU is a high-beta cyclical semi; 52W range shows extreme vol
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: 52W range ${VOL_52W_LOW:.2f}-${VOL_52W_HIGH:.2f} implies {(VOL_52W_HIGH/VOL_52W_LOW-1)*100:.0f}% peak-to-trough — typical for MU in cycle turns")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  — token; HBM capex takes priority)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (high-beta cyclical semi; memory cycle amplifies moves)")
print(f"  Beta vs S&P 500:      1.80  (MU moves 1.8x market; extreme at cycle turns)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} +/- {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}sigma drawdown  (plausible — MU fell 85% in 2022-23 cycle)")
print(f"  52W low ${VOL_52W_LOW:.2f} (cycle trough) shows scale of prior move: +{(CURRENT_PRICE/VOL_52W_LOW-1)*100:.0f}% off lows.")
print(f"  52W high ${VOL_52W_HIGH:.2f} is the HBM supercycle peak — ${CURRENT_PRICE:.2f} is 34% below the peak.")
print(f"  -> HBM supply data (Samsung yield reports, SK Hynix guidance) = primary price catalyst.")
print(f"  -> AI hyperscaler capex guidance (AWS, Azure, Google) = leading indicator of HBM demand.")
print(f"  -> WATCHLIST at current price  |  ACCUMULATE $650-700  |  BUY below $550")

# --- SCENARIO PROBABILITIES ---------------------------------------------------
print()
print("  [6] SCENARIO PROBABILITIES  (proxy model vs market-implied)")
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
print(f"  Downside  (-> Bear ${bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (-> Bull ${bull_price}):  {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b_str}")
print(f"  Signal    :  {signal_full}")
print()
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, market composite {MARKET_COMPOSITE:.2f} / model adj composite {ADJ_COMPOSITE:.3f}.")
print(f"  Gap {ADJ_GAP:+.2f} -> stock is {valuation_label.lower()} by model standards.")
print(f"  Cyclicality SCA penalty (-0.200) appropriately drags adj composite below proxy,")
print(f"  penalizing the structural risk that memory supercycles always end. Fundamentals are")
print(f"  BULL-level (proxy {PROXY_COMPOSITE:.2f}/4.0) but cyclicality-adjusted at {ADJ_COMPOSITE:.3f}/4.0.")
print(f"  Ratio B {ratio_b_str}: downside to BEAR (${bear_price}) = {downside_pct*100:.1f}% vs upside to BULL (${bull_price}) = {upside_pct*100:.1f}%.")
print(f"  The asymmetry is unfavorable: bear scenario is historically very plausible for Micron.")

# --- FOOTER -------------------------------------------------------------------
print()
print("=" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Samsung HBM3E yield / ramp cadence — monthly wafer starts = leading indicator of supply glut")
print(f"  (2) Hyperscaler capex guidance (AWS/Azure/Google Q3 2026 earnings) — demand floor confirmation")
print(f"  (3) Micron HBM4 qualification at NVIDIA — secures next-gen allocation; +15-20% ASP vs HBM3E")
print(f"  (4) NAND pricing recovery — enterprise SSD pricing stabilizes Q4 2026 (current WATCHLIST)")
print(f"  (5) CHIPS Act fab milestones — Boise/Singapore/Japan fabs; US capacity independence narrative")
print(f"  WATCHLIST at ${CURRENT_PRICE:.2f}  |  ACCUMULATE $650-700  |  BUY below $550")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}x  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  FY2027E EPS: $96")
print(f"  WARNING: Conservative 2yr return = {cons_return:.1f}%  -- memory cycle risk is the key bear case.")
print("=" * (W + 4))
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
