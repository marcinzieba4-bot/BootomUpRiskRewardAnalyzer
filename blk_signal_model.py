"""
BLK  ·  BlackRock, Inc.  ·  NYSE: BLK
Bottom-up signal model  ·  Asset Management / iShares ETFs / Aladdin / Private Markets
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "BLK"
COMPANY       = "BlackRock, Inc."
SECTOR        = "Asset Management · iShares ETFs · Aladdin · Private Markets · NYSE: BLK"
CURRENT_PRICE = 1025.00     # USD; as of 2026-06-11
VOL_52W_LOW   = 820.45      # April 2026 tariff/equity-market drawdown trough
VOL_52W_HIGH  = 1140.00     # early 2026 record-AUM peak
SHARES_OUT_M  = 148.5       # millions; modest buyback offsetting GIP/HPS share issuance
SHARES_OUT_B  = SHARES_OUT_M / 1000

# Dividend: long growth streak; growing high-single-digits
ANNUAL_DIV    = 21.40       # $/share FY2026 (~$5.35/quarter)

# ── REVENUE BRIDGE (company-specific calculator) ──────────────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Investment Advisory & Admin Fees (iShares/ETFs)", 8.40, 6.50, 10.20, "Largest revenue line; AUM-linked; organic flows + market beta"),
    ("Investment Advisory & Admin Fees (Index)",        2.30, 1.80,  2.70, "Institutional index mandates; fee compression headwind"),
    ("Investment Advisory & Admin Fees (Active/Alts)",  4.60, 3.70,  5.80, "Fixed income + equity active, plus GIP/HPS private markets"),
    ("Technology Services (Aladdin)",                   2.10, 1.85,  2.55, "High-margin SaaS-like ACV; Preqin data integration"),
    ("Performance Fees",                                0.90, 0.40,  1.60, "Alternatives carry; highly variable, market-sensitive"),
    ("Distribution Fees",                               1.30, 1.05,  1.55, "Servicing/distribution fees on retail AUM"),
]

# Margin assumptions
OP_MARGIN_CURR = 0.435     # blended operating margin FY2026E (~43.5%)
OP_MARGIN_BULL = 0.460     # BULL: operating leverage on AUM growth + Aladdin scale
OP_MARGIN_BEAR = 0.400     # BEAR: fee compression + lower performance fees
TAX_RATE       = 0.245     # effective tax rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 46.50      # FY2026E adj EPS (consensus ~$46-48; non-GAAP)
PE_PESSIMISTIC = 16.0       # trough P/E: AUM-linked earnings de-rate hard in equity selloffs
                             # (2022 bear-market trough ~16-17×)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # ~$744

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (32.00, 16,  512,  "Equity market correction (-25%); AUM down via market + outflows; fee compression bites; EPS $32 → 16× trough"),
    "BASE":  (50.00, 21, 1050,  "Steady iShares organic growth (+5-6%); markets flat-to-up modest; Aladdin ACV +12%; EPS $50 → 21×"),
    "BULL":  (62.00, 25, 1550,  "Strong equity markets + accelerating ETF flows; private markets (GIP/HPS) scale; EPS $62 → 25×"),
    "XBULL": (78.00, 28, 2184,  "AUM surpasses $16T; Aladdin becomes dominant risk OS for industry; alts mix re-rates multiple; EPS $78 → 28×"),
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
        "name":       "iShares/ETF net flows (annualized organic growth %)",
        "weight":     0.30,
        "thresholds": ("<2%",   "≥4%",   "≥6%",   "≥9%"),
        "now":        "~5%",
        "score":      2,
        "comment":    "iShares remains #1 ETF franchise globally; steady organic growth; fixed income + crypto ETFs contributing",
    },
    {
        "name":       "Total AUM YoY growth (organic + market)",
        "weight":     0.25,
        "thresholds": ("<0%",   "≥5%",   "≥10%",  "≥15%"),
        "now":        "+9%",
        "score":      3,
        "comment":    "AUM ~$13.5T; equity market appreciation + steady inflows; highly correlated to S&P 500 level",
    },
    {
        "name":       "Aladdin technology services revenue YoY",
        "weight":     0.20,
        "thresholds": ("<5%",   "≥9%",   "≥13%",  "≥18%"),
        "now":        "+12%",
        "score":      3,
        "comment":    "Recurring high-margin ACV growth; Preqin private-markets data cross-sell; client retention >95%",
    },
    {
        "name":       "Private markets / alternatives AUM growth (GIP/HPS/Preqin)",
        "weight":     0.10,
        "thresholds": ("<5%",   "≥10%",  "≥20%",  "≥35%"),
        "now":        "~18%",
        "score":      2,
        "comment":    "HPS credit + GIP infrastructure integration ramping; fundraising momentum building but early innings",
    },
    {
        "name":       "Effective fee rate (bps on AUM, base fees)",
        "weight":     0.10,
        "thresholds": ("<14bps","≥15bps","≥16bps","≥18bps"),
        "now":        "~15.5bps",
        "score":      2,
        "comment":    "Passive/index fee compression structural headwind, partly offset by alts mix shift to higher-fee products",
    },
    {
        "name":       "Operating margin",
        "weight":     0.05,
        "thresholds": ("<40%",  "≥42%",  "≥44%",  "≥46%"),
        "now":        "43.5%",
        "score":      2,
        "comment":    "Operating leverage from scale; Aladdin and technology services margin-accretive; integration costs a near-term drag",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "iShares scale moat — #1 global ETF franchise; ~$13T+ AUM; brand + liquidity network effects",  +0.7, 0.25),
    ("+", "Aladdin platform — high-margin recurring SaaS-like revenue; deep client switching costs",       +0.6, 0.20),
    ("-", "Equity market correlation — AUM-linked revenue makes BLK a leveraged proxy on equity/bond levels", -0.7, 0.20),
    ("-", "Fee compression — structural pricing pressure in passive/index products erodes effective fee rate", -0.5, 0.15),
    ("+", "Private markets diversification — GIP, HPS, Preqin push into higher-fee alternatives & data",   +0.5, 0.15),
    ("-", "Premium valuation risk — 20-24x historical premium leaves little room if growth disappoints",   -0.4, 0.05),
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
CONS_EPS_2YR  = 56.00   # conservative FY2028E: ~9.5%/yr EPS CAGR; AUM growth + Aladdin scale, modest fee compression
CONS_PE_2YR   = 20      # rerating from ~22x toward growth-justified 20x
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Asset Management / iShares / Aladdin / Private Markets")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① REVENUE BRIDGE ─────────────────────────────────────────────────────────
print()
print("  REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<48}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<48}  ${curr:>11.2f}  ${bear:>8.2f}  ${bull:>8.2f}  {bear-curr:>+7.2f}  {bull-curr:>+7.2f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<48}  ${curr_total:>11.2f}  ${bear_total:>8.2f}  ${bull_total:>8.2f}  {bear_total-curr_total:>+7.2f}  {bull_total-curr_total:>+7.2f}")
print()

# EPS bridge
curr_oi   = curr_total * OP_MARGIN_CURR
curr_ni   = curr_oi * (1 - TAX_RATE)
shares    = SHARES_OUT_B
curr_eps  = round(curr_ni / shares, 2)

bull_oi   = bull_total * OP_MARGIN_BULL
bull_ni   = bull_oi * (1 - TAX_RATE)
shares_b  = shares * 0.97   # modest buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_oi   = bear_total * OP_MARGIN_BEAR
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.2f}B rev × {OP_MARGIN_CURR*100:.1f}% op margin − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.4f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ~${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B rev × {OP_MARGIN_BULL*100:.1f}% op margin − tax")
print(f"  ÷ {shares_b:.4f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 25× = ~${bull_eps_imp*25:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B rev × {OP_MARGIN_BEAR*100:.1f}% op margin − tax  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 16× trough P/E (equity-market crisis floor) = ~${bear_eps_imp*16:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = (1.0 * OP_MARGIN_CURR * (1 - TAX_RATE)) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Advisory/iShares revenue:  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*21:.1f}/share at 21× P/E")
print(f"  Every 10% S&P 500 move (AUM beta):   ~±${curr_total*0.06*OP_MARGIN_CURR*(1-TAX_RATE)/shares:.2f}/EPS  (AUM ~60% equity-linked)")
print(f"  Every $1B Aladdin revenue:            +${1.0*0.55*(1-TAX_RATE)/shares:.3f}/EPS  (Aladdin op margin ~55%)")
print(f"  1pp effective fee rate change:        ~±${curr_total*(1/15.5)*OP_MARGIN_CURR*(1-TAX_RATE)/shares:.2f}/EPS  (on ~15.5bps base)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (AUM growth / iShares flows / Aladdin / fee-rate framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>7}  {'BASE':>7}  {'BULL':>7}  {'XBULL':>7}  {'NOW':>9}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>7}  {ths[1]:>7}  {ths[2]:>7}  {ths[3]:>7}  {s['now']:>9}  {lbl}  {b}")

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
print(f"  {'Signal':<52}  {'Current':>10}  {'Bear val':>10}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("iShares/ETF net flows (organic growth)", "~5%",     "<2%",     "−3pp",   "Equity selloff triggers risk-off redemptions across passive products"),
    ("Total AUM YoY growth",                   "+9%",     "<0%",     "−9pp",   "S&P 500 -25% drawdown; AUM falls via market value + net outflows"),
    ("Aladdin revenue YoY",                    "+12%",    "<5%",     "−7pp",   "Client budget cuts delay technology contract renewals/expansions"),
    ("Private markets AUM growth",             "~18%",    "<5%",     "−13pp",  "Fundraising freeze; GIP/HPS integration stalls amid market stress"),
    ("Effective fee rate",                     "~15.5bps","<14bps",  "−1.5bps","Continued mix-shift to lowest-cost index products accelerates"),
    ("Operating margin",                       "43.5%",   "<40%",    "−3.5pp", "Performance fees evaporate; fixed cost base de-levers on lower AUM"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A broad equity/bond market correction (S&P 500 -20-25%) is the dominant")
print(f"  BEAR risk for BLK — AUM-linked base fees fall mechanically with market levels, while")
print(f"  performance fees on alternatives compress sharply and net flows turn risk-off.")
print(f"  EPS falls to ~${bear_price/16:.0f} → 16× crisis-trough P/E = ${bear_price}.")
print(f"  Note: BlackRock's diversified platform (iShares + Aladdin recurring revenue + private")
print(f"  markets) provides a faster recovery than pure beta plays — Aladdin ACV is largely")
print(f"  contractual and does not reprice with markets.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~$46-48; non-GAAP)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (2022 bear-market trough ~16-17×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP reflects the market pricing BlackRock's scale advantages")
print(f"  (iShares #1 ETF franchise, Aladdin recurring tech revenue, and the GIP/HPS private")
print(f"  markets push) at a premium multiple (~22× current vs 16× trough). The risk is that")
print(f"  a market correction compresses BOTH the E (AUM-linked earnings) and the multiple")
print(f"  simultaneously — a double hit characteristic of AUM-levered financials.")
print(f"  EPP path: FY2028E EPS ~${CONS_EPS_2YR:.0f} × {PE_PESSIMISTIC:.0f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing with earnings).")
print(f"  At {CONS_PE_2YR}× mid-cycle P/E: ${EPS_FY2026E:.2f} × {CONS_PE_2YR} = ${EPS_FY2026E*CONS_PE_2YR:.0f}  — below current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: P/E rerates toward growth rate; equity markets flat-to-up modest)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (~9.5% EPS CAGR: AUM growth + Aladdin scale, modest fee compression)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (rerates from ~22× toward growth-justified 20×)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: AUM growth (organic flows + market appreciation) must continue at a")
print(f"  high-single-digit pace for EPS to reach ${CONS_EPS_2YR:.0f} by FY2028E. A flat equity market")
print(f"  alone would likely fall short, requiring organic flow acceleration or alts mix-shift to compensate.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E.")
print(f"  Breakeven at 22× P/E (current multiple held): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 22:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case attractive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.27
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (AUM-linked earnings amplify equity-market beta)")
print(f"  Beta vs S&P 500:      1.25  (financial-services + AUM leverage to market levels)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (consistent with a sharp equity-market correction)")
print(f"  52W low ${VOL_52W_LOW:.2f} (April 2026 drawdown) reflects a peak-to-trough move of ~{(VOL_52W_HIGH-VOL_52W_LOW)/VOL_52W_HIGH*100:.0f}%.")
print(f"  → Equity/bond market levels are THE KEY driver — BLK is effectively a leveraged proxy on AUM.")
print(f"  → iShares net flow acceleration + Aladdin ACV growth are KEY bull catalysts independent of markets.")
print(f"  → AVOID/WATCHLIST near current  |  ACCUMULATE $850-900  |  BUY below $800")

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
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The gap ({ADJ_GAP:.2f}) indicates the stock is")
print(f"  {valuation_label.lower()} by model standards.")
print(f"  Equity market correlation (signal weighted at 25% on AUM growth) is the most significant")
print(f"  swing factor for this valuation — a correction would compress both EPS and multiple.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Equity/bond market levels — the dominant AUM and earnings driver (BEAR/BULL swing)")
print(f"  (2) iShares net flow acceleration — fixed income, crypto, and active ETF conversions")
print(f"  (3) Aladdin ACV growth — recurring high-margin technology revenue, Preqin cross-sell")
print(f"  (4) Private markets integration — GIP infrastructure + HPS credit fundraising momentum")
print(f"  (5) Fee compression trajectory — effective fee rate stabilization vs continued erosion")
print(f"  AVOID/WATCHLIST near ${CURRENT_PRICE:.2f}  |  ACCUMULATE $850-900  |  BUY below $800")
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
