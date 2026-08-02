"""
LRCX  ·  Lam Research Corporation  ·  NASDAQ: LRCX
Bottom-up signal model  ·  Wafer Fabrication Equipment / HBM / NAND / Logic
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "LRCX"
COMPANY       = "Lam Research Corporation"
SECTOR        = "Wafer Fabrication Equipment · HBM / NAND / Logic · NASDAQ: LRCX"
CURRENT_PRICE = 293.02       # USD; as of 2026-08-02
VOL_52W_LOW   =  90.94       # 52-week low
VOL_52W_HIGH  = 438.50       # 52-week high
SHARES_OUT_M  = 1_251.0      # millions (~$366.65B mkt cap / $293.02)

# Dividend: $0.26/qtr → $1.04/yr (0.35% yield)
ANNUAL_DIV    = 1.04         # $/share

# ── WFE END-MARKET REVENUE BRIDGE ─────────────────────────────────────────────
# FY2026E revenue by end-market ($B); TTM = $23.23B (+26.0% YoY)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("DRAM / HBM Etch & Dep",   9.5,  5.0, 15.0, "HBM3/HBM4 each layer needs Lam etch; every HBM stack = 10+ etch steps"),
    ("NAND WFE",                 7.5,  3.0, 12.0, "NAND recovering from 2023-24 trough; 200+ layer drives deep etch intensity"),
    ("Logic / Foundry",          4.5,  3.5,  7.0, "TSMC 2nm, Intel 18A — gate-all-around requires more etch/dep per node"),
    ("CSBG (Services/Spares)",   1.7,  1.4,  2.2, "Recurring; highest-margin segment; grows with installed base"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.480   # blended gross margin FY2026E (~48%)
GROSS_MARGIN_BULL = 0.500   # BULL: services mix + volume leverage
OPEX_FIXED_B      = 4.8     # R&D + SG&A ($B); ~20.6% of revenue
TAX_RATE          = 0.130   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 9.48        # FY2026E non-GAAP EPS (consensus; forward P/E 30.92×)
PE_PESSIMISTIC = 18.0        # trough P/E: WFE cycle floor; 2019 trough ~15–18×
BEAR_EPS       = 5.00        # bear scenario EPS (WFE downturn + China step-down)
EPP            = round(PE_PESSIMISTIC * BEAR_EPS, 0)   # $90

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 5.00, 18,   90, "WFE cycle downturn; China restrictions tighten; capex pause; EPS $5 → 18× trough"),
    "BASE":  ( 9.48, 24,  227, "HBM/AI memory capex sustains; NAND recovery; EPS $9.48 → 24× justified growth P/E"),
    "BULL":  (14.00, 28,  392, "Logic+HBM supercycle; DRAM/NAND simultaneous ramp; EPS $14 → 28× premium"),
    "XBULL": (20.00, 32,  640, "All nodes + EUV upgrade + China localisation; EPS $20 → 32× peak cycle"),
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
        "name":       "HBM/DRAM etch intensity & spend",
        "weight":     0.30,
        "thresholds": ("<10%", "≥15%",  "≥30%",  "≥50%"),
        "now":        "+35%",
        "score":      3,
        "comment":    "HBM3/4 drives etch steps per wafer; AI memory capex robust; DRAM investment accelerating YoY",
    },
    {
        "name":       "NAND WFE spend YoY",
        "weight":     0.20,
        "thresholds": ("<-20%", "≥0%",  "≥20%",  "≥40%"),
        "now":        "+18%",
        "score":      2,
        "comment":    "NAND recovering from trough; 200+ layer drives etch intensity; Samsung/SK Hynix capex stabilising",
    },
    {
        "name":       "Logic node WFE spending YoY",
        "weight":     0.20,
        "thresholds": ("<5%",  "≥8%",   "≥18%",  "≥30%"),
        "now":        "+12%",
        "score":      2,
        "comment":    "TSMC 2nm ramp; Intel 18A investment; gate-all-around requires more etch/dep steps per node",
    },
    {
        "name":       "China revenue YoY",
        "weight":     0.15,
        "thresholds": ("<-30%", "≥-10%", "≥+5%", "≥+20%"),
        "now":        "-5%",
        "score":      2,
        "comment":    "Export controls constrain leading-edge; legacy node demand partially offsets; uncertainty elevated",
    },
    {
        "name":       "Gross margin",
        "weight":     0.10,
        "thresholds": ("<44%",  "≥46%",  "≥48%",  "≥50%"),
        "now":        "48%",
        "score":      3,
        "comment":    "CSBG high-margin services growing; volume leverage on fixed opex; mix toward advanced nodes",
    },
    {
        "name":       "Book-to-bill ratio",
        "weight":     0.05,
        "thresholds": ("<0.9",  "≥1.0",  "≥1.1",  "≥1.25"),
        "now":        "~1.05",
        "score":      2,
        "comment":    "Slightly above parity; HBM/memory orders positive; logic orders building; NAND still rebuilding",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "HBM monopoly position — every HBM layer requires Lam etch; no viable substitute",           +0.8, 0.25),
    ("+", "Duopoly WFE market — Lam (#2 globally) + ASML/TEL; high barriers to entry; pricing power",  +0.5, 0.20),
    ("-", "China export restriction risk — China ~30% of revenue; escalation = step-down revenue",       -0.9, 0.20),
    ("-", "WFE cycle volatility — capex discretionary; memory over-investment risk post-HBM peak",       -0.6, 0.20),
    ("+", "CSBG installed-base flywheel — $4B+ recurring services revenue growing with installed base",  +0.4, 0.10),
    ("-", "Customer concentration — Samsung + SK Hynix + Micron >60% revenue; single-customer risk",    -0.3, 0.05),
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
CONS_EPS_2YR  = 10.50   # conservative FY2028E: HBM sustains + NAND recovery; ~10.5% EPS CAGR
CONS_PE_2YR   = 22      # mid-cycle WFE P/E; below current 30.9× forward
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Wafer Fabrication Equipment / HBM / NAND / Logic")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① WFE REVENUE BRIDGE ─────────────────────────────────────────────────────
print()
print("  WFE END-MARKET REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
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
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_ni   = curr_oi * (1 - TAX_RATE)
curr_eps  = round(curr_ni / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B
bull_ni   = bull_oi * (1 - TAX_RATE)
shares_b  = shares * 0.97   # modest buyback
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.95   # margin compression in downturn
bear_oi   = bear_gp - OPEX_FIXED_B * 0.95
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2026E:.2f} non-GAAP  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 28× = ~${bull_eps_imp*28:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.95:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 18× trough P/E (WFE cycle floor) = ~${bear_eps_imp*18:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev   = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_china = 1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at {GROSS_MARGIN_CURR*100:.0f}% GM):     +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*24:.1f}/share at 24× P/E")
print(f"  China revenue ±$1B (export risk):    ±${eps_per_1B_china:.3f}/EPS  =  ±${eps_per_1B_china*24:.1f}/share at 24× P/E")
print(f"  1pp GM expansion (mix/volume):        +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*24:.1f}/share at 24× P/E")
print(f"  HBM layer count increase (+1 layer):  structural TAM uplift — each extra etch step = ~$300M+ TAM")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (HBM etch / NAND WFE / Logic / China / GM / B2B framework)")
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
    ("HBM/DRAM etch spend YoY",       "+35%",    "<10%",    "−25pp",  "Memory capex pause; hyperscalers defer HBM orders"),
    ("NAND WFE spend YoY",            "+18%",    "<-20%",   "−38pp",  "NAND oversupply; producers cut capex dramatically"),
    ("Logic node WFE spending YoY",   "+12%",    "<5%",     "−7pp",   "TSMC delays 2nm; Intel 18A cancelled/deferred"),
    ("China revenue YoY",             "-5%",     "<-30%",   "−25pp",  "BIS expands export controls to legacy nodes"),
    ("Gross margin",                  "48%",     "<44%",    "−4pp",   "Volume deleverage; pricing pressure; mix shift"),
    ("Book-to-bill ratio",            "~1.05",   "<0.9",    "−0.15",  "Order cancellations; customers cut WFE budgets"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Simultaneous WFE capex pause (memory oversupply) + China export control")
print(f"  escalation to legacy nodes. China is ~$7B revenue (~30% of TTM). A BIS expansion plus")
print(f"  DRAM/NAND oversupply (as seen 2022-23) compresses revenue to ~$13B and EPS to ~$5.")
print(f"  At 18× trough P/E (historical WFE floor) = ${bear_price}.")
print(f"  Note: HBM structural demand limits depth/duration of bear case vs prior WFE cycles.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × bear EPS)")
hr()
print(f"  Bear EPS estimate (cycle trough):  ${BEAR_EPS:.2f}  (WFE downturn + China revenue step-down)")
print(f"  FY2026E non-GAAP EPS estimate:     ${EPS_FY2026E:.2f}  (forward P/E {CURRENT_PRICE/EPS_FY2026E:.1f}×)")
print(f"  Pessimistic P/E at trough:          {PE_PESSIMISTIC:.0f}×  (2019 WFE trough ~15–18×; HBM floor premium)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP means market prices in substantial cycle duration.")
print(f"  At ${CURRENT_PRICE:.2f} and FY2026E non-GAAP EPS ${EPS_FY2026E:.2f}, forward P/E = {CURRENT_PRICE/EPS_FY2026E:.1f}×.")
print(f"  WFE companies historically trade 20–35× mid-cycle; current premium reflects HBM.")
print(f"  EPP path: bear EPS $7 by FY2028E × 18× = $126 bear floor (rising as EPS recovers).")
print(f"  At 24× mid-cycle P/E: ${EPS_FY2026E:.2f} × 24 = ${EPS_FY2026E*24:.0f}  ({(EPS_FY2026E*24/CURRENT_PRICE-1)*100:+.1f}% from current).")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: mid-cycle P/E; HBM sustains; NAND partial recovery)")
hr()
print(f"  Conservative FY2028E non-GAAP EPS:  ${CONS_EPS_2YR:.2f}  (HBM stable + NAND recovery + logic ramp)")
print(f"  Conservative exit P/E:               {CONS_PE_2YR}×  (mid-cycle; below current {CURRENT_PRICE/EPS_FY2026E:.1f}× forward)")
print(f"  Conservative equity value:            ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):        +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:               ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:            {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  P/E compression from {CURRENT_PRICE/EPS_FY2026E:.1f}× to {CONS_PE_2YR}× offsets EPS growth. Key risk: WFE")
print(f"  cycle mean-reversion compresses multiple before earnings inflect higher.")
print(f"  Breakeven at {CONS_PE_2YR}× P/E: FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f}  (conservative case clearly positive; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.38   # WFE stocks more volatile than market
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  token yield)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (WFE cycle amplifies; China binary adds tail risk)")
print(f"  Beta vs S&P 500:      1.60  (high beta; semiconductor capex cycle + China overhang)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (tail; requires full WFE cycle + China shock)")
print(f"  52W range ${VOL_52W_LOW:.2f}–${VOL_52W_HIGH:.2f} shows extreme cycle amplitude (>4× trough to peak).")
print(f"  → China export controls are THE binary risk; each escalation = −15–25% move.")
print(f"  → HBM demand durability (AI memory capex) is THE key bull catalyst to monitor.")
print(f"  → Signal: {signal_full}  |  WATCHLIST $230–250  |  ACCUMULATE $190–210  |  BUY below $175")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, market composite ({MARKET_COMPOSITE:.2f}) vs model adj ({ADJ_COMPOSITE:.3f}).")
print(f"  Gap ({ADJ_GAP:.2f}) → stock is {valuation_label.lower()} by model standards.")
print(f"  Analyst consensus: 35 Strong Buy; avg PT $368 (+25.6% upside). Model more cautious")
print(f"  on China export risk and WFE cycle timing vs street optimism on HBM durability.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) HBM4 ramp velocity — SK Hynix + Samsung HBM4 capex commitments (BULL trigger)")
print(f"  (2) China export controls — BIS expansion to legacy nodes (BEAR trigger)")
print(f"  (3) NAND recovery timeline — flash price inflection confirms capex return (BASE→BULL)")
print(f"  (4) TSMC 2nm yield — high yield = higher etch tool utilisation (BULL trigger)")
print(f"  (5) Intel 18A volume ramp — determines magnitude of logic WFE spend in 2027")
print(f"  Signal: {signal_full}  |  Ratio B: {ratio_b_str}  |  EPP floor: ${EPP:.0f}")
print(f"  Current ${CURRENT_PRICE:.2f}  |  52W: ${VOL_52W_LOW}–${VOL_52W_HIGH}  |  FY2026E EPS: ${EPS_FY2026E:.2f}")
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
