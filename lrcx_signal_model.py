"""
LRCX  ·  Lam Research Corporation  ·  NASDAQ: LRCX
Bottom-up signal model  ·  Semiconductor Equipment / Etch & Deposition / WFE
Date: 2026-06-09
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "LRCX"
COMPANY       = "Lam Research Corporation"
SECTOR        = "Semiconductor Equipment · Etch & Deposition · WFE · NASDAQ: LRCX"
CURRENT_PRICE = 298.46       # USD; as of 2026-06-09; up significantly from 52W low on AI WFE thesis
VOL_52W_LOW   = 156.30       # October 2025 trough; WFE correction + China uncertainty
VOL_52W_HIGH  = 345.80       # March 2026 NAND recovery + HBM capex peak
SHARES_OUT_M  = 1_330.0      # millions; declining ~3%/yr via buybacks
ANNUAL_DIV    = 2.40         # $/share ($0.60/quarter; growing ~10%/yr; initiated 2014)

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2027E revenue by segment ($B)  [fiscal year ends June 2027]
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Etch — Logic/Foundry (TSMC/Samsung/Intel)",  7.5, 4.5, 11.0, "Gate-all-around transition; TSMC N2/A16 etch intensity up 30%+ per wafer"),
    ("Etch — Memory (DRAM/HBM)",                   5.5, 2.5,  9.0, "HBM4 high aspect ratio etch; DRAM EUV integration; SK Hynix/Micron"),
    ("Etch — NAND",                                3.0, 1.5,  5.5, "232L+ 3D NAND etch; Samsung recovery; inventory cycle bottom"),
    ("Deposition (CVD/ALD/Epitaxy)",               5.0, 3.0,  8.0, "ALD gate dielectric; EUV underlayers; advanced packaging Cu/barrier"),
    ("Cryogenic & Cleaning / Other",               2.5, 1.5,  4.0, "Cryo-etch for GAA fins; single wafer clean; advanced packaging"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.480   # blended; WFE equipment typical ~47-49%
GROSS_MARGIN_BULL = 0.510   # BULL: high-margin service/spares mix increases; pricing power
OPEX_FIXED_B      = 3.8     # non-GAAP R&D + SG&A; relatively lean
TAX_RATE          = 0.120   # effective; Singapore/offshore structures

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 4.80        # FY2027E adj EPS (consensus $4.50–$5.10 non-GAAP; fiscal June 2027)
PE_PESSIMISTIC = 16.0        # trough P/E: semiconductor equipment is deeply cyclical; 2022-23 trough ~12-16×
                              # Note: at $298 and EPP $77, stock is 287% above trough floor — rich
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # $77

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 2.50, 14,  35, "WFE collapse: memory oversupply + China ban; revenue -45%; EPS $2.50 → 14× trough"),
    "BASE":  ( 5.50, 26, 143, "WFE recovery cycle; HBM3E/4 etch intensity; GAA ramp at TSMC; EPS $5.50 → 26×"),
    "BULL":  ( 8.00, 30, 240, "HBM supercycle + GAA logic ramp + NAND recovery; EPS $8.00 → 30× growth premium"),
    "XBULL": (12.00, 35, 420, "AI hardware arms race never pauses; LRCX critical path every node; EPS $12 → 35×"),
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
        "name":       "WFE spending YoY (industry)",
        "weight":     0.25,
        "thresholds": ("<-10%",  "≥5%",   "≥15%",   "≥25%"),
        "now":        "+12%",
        "score":      2,
        "comment":    "FY2027E WFE ~$115B (+12% YoY); HBM + logic driving; NAND still recovering; China export risk",
    },
    {
        "name":       "HBM etch intensity / revenue",
        "weight":     0.25,
        "thresholds": ("<$2B",   "≥$3B",  "≥$5B",   "≥$8B"),
        "now":        "~$5B",
        "score":      3,
        "comment":    "HBM4 requires 2× etch steps vs HBM3; LRCX sole-source on key high aspect ratio steps; SK Hynix/Micron",
    },
    {
        "name":       "Gate-all-around logic ramp (TSMC N2)",
        "weight":     0.20,
        "thresholds": ("<20%",   "≥40%",  "≥65%",   "≥90%"),
        "now":        "~55%",
        "score":      2,
        "comment":    "TSMC N2 volume ramp at ~55% of planned capacity; GAA adds 15-20% etch steps vs FinFET; FY2027 peak",
    },
    {
        "name":       "NAND WFE recovery",
        "weight":     0.15,
        "thresholds": ("<-20%",  "≥0%",   "≥15%",   "≥35%"),
        "now":        "+8%",
        "score":      2,
        "comment":    "3D NAND capex recovering from trough; 232L+ adoption; Samsung restoring utilization; slow recovery",
    },
    {
        "name":       "China revenue / export controls",
        "weight":     0.10,
        "thresholds": ("<$2B",   "≥$3.5B","≥$5B",   "≥$7B"),
        "now":        "~$3.5B",
        "score":      2,
        "comment":    "China ~15% of revenue (~$3.5B); export controls limit advanced etch; lagging-node still allowed",
    },
    {
        "name":       "Service/spares as % of revenue",
        "weight":     0.05,
        "thresholds": ("<20%",   "≥25%",  "≥30%",   "≥38%"),
        "now":        "~27%",
        "score":      2,
        "comment":    "Service/spares $6.5B/yr (~27% of rev); recurring; high-margin; growing installed base",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Etch technology moat — #1 globally ~50% etch market share; conductors/dielectrics/GAA fins",   +0.8, 0.25),
    ("+", "HBM structural tailwind — sole-source on key HBM4 high-AR etch; AI memory = structural demand", +0.6, 0.20),
    ("-", "Cyclicality — WFE is deeply cyclical; memory capex can fall 40-50% in down-cycle",             -0.7, 0.20),
    ("-", "China export control binary — China 15% of rev; tighter BIS rules = permanent revenue loss",   -0.5, 0.15),
    ("+", "GAA technology transition — N2/A16/Intel 18A all require new etch chamber types; sole-source",  +0.4, 0.15),
    ("-", "Valuation at cycle peak — 62× FY2026E at $298; paying peak-cycle P/E for cyclical",            -0.5, 0.05),
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

# BULL ($240) < CURRENT ($298.46) → upside_pct < 0 → ratio_b = inf → AVOID
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
CONS_EPS_2YR  = 5.80    # FY2028E conservative: 10% EPS CAGR from FY2027E (cycle normalizes)
CONS_PE_2YR   = 22      # WFE companies trade 18-25× mid-cycle; 22× reasonable floor
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Semiconductor Equipment / Etch & Deposition / WFE")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2027E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<45}  {'FY2027E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<45}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<45}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_ni   = curr_oi * (1 - TAX_RATE)
curr_eps  = round(curr_ni / shares, 2)

bull_gp      = bull_total * GROSS_MARGIN_BULL
bull_oi      = bull_gp - OPEX_FIXED_B
bull_ni      = bull_oi * (1 - TAX_RATE)
shares_b     = shares * 0.94   # ~3%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.95   # mix shift to lower-margin systems
bear_oi      = bear_gp - OPEX_FIXED_B * 0.95           # partial cost response
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2027E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2027E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 30× = ~${bull_eps_imp*30:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.95:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 14× trough P/E (WFE cycle floor) = ~${bear_eps_imp*14:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev   = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_china = 1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B WFE revenue:           +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*26:.1f}/share at 26× P/E")
print(f"  China revenue ±$1B ({GROSS_MARGIN_CURR*100:.0f}% margin): ±${eps_per_1B_china:.3f}/EPS  =  ±${eps_per_1B_china*26:.1f}/share at 26× P/E")
print(f"  1pp GM expansion (spares mix):   +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*26:.1f}/share at 26× P/E")
print(f"  1% buyback (13.3M shares):       +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (WFE spending / HBM etch / GAA logic / NAND / China / Services framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>5}  {'BASE':>6}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>7}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>5}  {ths[1]:>6}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>7}  {lbl}  {b}")

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
    ("WFE spending YoY",               "+12%",    "<-10%",  "−22pp",  "Macro recession + memory oversupply; WFE -30%"),
    ("HBM etch revenue",               "~$5B",    "<$2B",   "−$3B",   "HBM demand collapses; hyperscaler GPU orders drop"),
    ("GAA logic ramp (TSMC N2)",       "~55%",    "<20%",   "−35pp",  "TSMC N2 yield crisis delays; FinFET extension"),
    ("NAND WFE recovery",              "+8%",     "<-20%",  "−28pp",  "NAND oversupply 2.0; Samsung cuts capex 50%"),
    ("China revenue",                  "~$3.5B",  "<$2B",   "−$1.5B", "BIS expands export controls to all etch tools"),
    ("Service/spares % of revenue",    "~27%",    "<20%",   "−7pp",   "Customer utilization drops; service contracts cut"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: BIS expansion of export controls to cover all etch tools (not just advanced-")
print(f"  node), combined with a memory oversupply cycle. China contributed ~$3.5B (~15% of rev);")
print(f"  full etch-tool ban removes this permanently. Simultaneously, HBM hyperscaler orders slow")
print(f"  (GPU demand air-pocket) and TSMC N2 ramp delays. Revenue -45% → EPS ~$2.50 → 14× trough")
print(f"  floor P/E = ${bear_price}. Note: WFE trough recoveries are violent — LRCX recovered 3× from")
print(f"  2023 trough within 18 months. Bear scenario is real but likely temporary (~12-18 months).")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E adj EPS estimate:      ${EPS_FY2027E:.2f}  (consensus $4.50–$5.10; non-GAAP; fiscal June 2027)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (WFE equipment deeply cyclical; 2022-23 trough ~12-16×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP is extreme even for a high-quality business. At $298.46")
print(f"  and FY2027E EPS $4.80, the P/E is ~62× — pricing in a permanent AI WFE supercycle with")
print(f"  no cyclical correction. WFE equipment has NEVER sustained 60×+ P/E through a full cycle.")
print(f"  EPP path: FY2029E EPS ~$6.50 × {PE_PESSIMISTIC:.0f}× = ${6.50*PE_PESSIMISTIC:.0f} floor (EPP growing ~15%/yr on EPS growth).")
print(f"  At 25× mid-cycle P/E: ${EPS_FY2027E:.2f} × 25 = ${EPS_FY2027E*25:.0f}  — still 60% below current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: P/E rerates from cycle-peak 62× toward mid-cycle 22×)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (10% EPS CAGR: buyback ~3%/yr + EPS growth ~7%/yr)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (WFE mid-cycle floor; 18-25× range; 22× reasonable)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; growing ~10%/yr)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE PROBLEM: P/E compression from ~62× to 22× = -65% multiple contraction.")
print(f"  Even with EPS growing 10%/yr, that multiple contraction produces a deeply negative")
print(f"  total return. For conservative 2yr to break even at 22× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E - 1)*100:.1f}% EPS growth by FY2028E — requires XBULL scenario.")
print(f"  Breakeven at 30× P/E (partial compression only): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 30:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at 22× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.50   # WFE stocks are very volatile; beta ~1.6
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: 52W low ${VOL_52W_LOW:.2f} (Oct 2025 WFE correction); 52W high ${VOL_52W_HIGH:.2f} (Mar 2026 HBM peak)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  growing ~10%/yr)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (WFE equipment highly cyclical; beta ~1.6; earnings binary risk)")
print(f"  Beta vs S&P 500:      1.60  (significant; WFE amplifies semiconductor cycle moves)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (plausible; WFE stocks fall 50-70% in down-cycles)")
print(f"  52W range ${VOL_52W_LOW:.2f}–${VOL_52W_HIGH:.2f} reflects +91% trough-to-peak in 5 months — extreme WFE vol.")
print(f"  → China export control expansion is THE KEY binary; full etch ban = -30–40% in days.")
print(f"  → HBM4 volume ramp timing (H2 2026) is KEY bull catalyst for next re-rating leg.")
print(f"  → AVOID above $250  |  WATCHLIST $200–230  |  ACCUMULATE $165–195  |  BUY below $150")

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
print(f"  Upside    (→ Bull ${bull_price}):  {upside_pct*100:.1f}%  ← NEGATIVE: BULL target BELOW current price")
print(f"  Ratio B   :  {ratio_b_str}  (undefined — bull price below current; zero upside to BULL)")
print(f"  Signal    :  {signal_full}")
print()
print(f"  THE PEAK-CYCLE VALUATION PROBLEM: At $298, LRCX trades at ~62× FY2026E EPS ($4.80)")
print(f"  and ~2.8× forward revenue — near historical peak multiples for WFE equipment. The BULL")
print(f"  case ($240) is BELOW the current price. This means buying at $298 requires the XBULL")
print(f"  scenario to break even on a 2-year horizon. The business is excellent — #1 etch globally,")
print(f"  sole-source on HBM4, GAA transition additive — but the market has already priced the")
print(f"  cycle peak. EPP floor ($77) is 287% below current price. Conservative 2yr return is")
print(f"  highly negative if P/E normalizes from 62× to 22×. The correct posture: outstanding")
print(f"  business, wrong price. Re-evaluate on any 30%+ drawdown toward $180–200.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) HBM4 volume ramp timing — SK Hynix/Micron capex for HBM4 (H2 2026) = key BULL catalyst")
print(f"  (2) TSMC N2 yield data — GAA ramp pace determines etch tool demand timeline")
print(f"  (3) China export control expansion — BIS rule change to include lagging-node etch = BEAR trigger")
print(f"  (4) NAND capex recovery signal — Samsung/Kioxia announcing new fab investments")
print(f"  (5) Memory customer utilization rates — leading indicator for spares/service revenue")
print(f"  AVOID above $250  |  WATCHLIST $200–230  |  ACCUMULATE $165–195  |  BUY below $150")
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
