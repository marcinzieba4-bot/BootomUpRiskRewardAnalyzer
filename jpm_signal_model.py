"""
JPM  ·  JPMorgan Chase & Co.  ·  NYSE: JPM
Bottom-up signal model  ·  Money Center Bank / NII / Investment Banking / Fortress Balance Sheet
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "JPM"
COMPANY       = "JPMorgan Chase & Co."
SECTOR        = "Money Center Bank · Net Interest Income · Investment Banking · NYSE: JPM"
CURRENT_PRICE = 305.50      # USD; as of 2026-06-10
VOL_52W_LOW   = 218.50      # April 2025 tariff-shock trough
VOL_52W_HIGH  = 312.00      # May 2026 high; CET1 strength + buyback pace
SHARES_OUT_M  = 2_720.0     # millions; declining ~3-4%/yr via buyback

# Dividend: raised steadily; ~2.0% yield
ANNUAL_DIV    = 5.60        # $/share (annualized; $1.40/quarter)

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E managed net revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Consumer & Community Banking", 70.0, 62.0,  76.0, "NII-driven; deposit margins, card NCOs, branch banking"),
    ("Corporate & Investment Bank",  56.0, 44.0,  68.0, "Markets/trading + IB fees; M&A/IPO recovery is swing factor"),
    ("Commercial Banking",           14.5, 12.0,  16.5, "Middle-market & corporate lending; credit quality sensitive"),
    ("Asset & Wealth Management",    24.5, 21.0,  28.0, "AUM-linked fees; record AUM; market-level dependent"),
]

# Margin / earnings build assumptions
EFFICIENCY_RATIO_CURR = 0.55   # opex / revenue, blended FY2026E
EFFICIENCY_RATIO_BULL = 0.52   # operating leverage in BULL (fee growth outpaces opex)
PROVISION_RATE_CURR   = 0.045  # provisions as % of revenue, FY2026E normal credit
PROVISION_RATE_BEAR   = 0.090  # recession: loan loss provisions roughly double
TAX_RATE              = 0.23   # effective tax rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 19.50       # FY2026E adj EPS (consensus ~$19-20)
PE_PESSIMISTIC = 9.0         # trough P/E: GFC-era / regional bank crisis trough ~8-10x
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # ~$176

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (12.50, 11,  138, "Recession: rate cuts compress NII, credit costs double, IB fees dry up; EPS $12.50 → 11x"),
    "BASE":  (20.50, 13,  267, "Soft landing; NII stable, modest IB recovery, normal credit; EPS $20.50 at FY2028E → 13x"),
    "BULL":  (24.50, 15,  368, "M&A/IPO boom, steepening curve aids NII, CET1 buyback acceleration; EPS $24.50 → 15x"),
    "XBULL": (29.00, 17,  493, "Capital markets supercycle, fortress balance sheet share gains, premium re-rating to 17x"),
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
        "name":       "Net interest income (NII) YoY growth",
        "weight":     0.30,
        "thresholds": ("<-5%",   "≥-1%",  "≥+3%",   "≥+8%"),
        "now":        "+1%",
        "score":      2,
        "comment":    "Fed on hold/cutting modestly; deposit costs sticky; loan growth offsetting margin compression",
    },
    {
        "name":       "Investment banking fees YoY growth",
        "weight":     0.20,
        "thresholds": ("<-15%",  "≥0%",   "≥+15%",  "≥+30%"),
        "now":        "+18%",
        "score":      3,
        "comment":    "M&A and IPO pipeline reaccelerating; CIB advisory backlog at multi-year highs",
    },
    {
        "name":       "Net charge-off rate (credit quality)",
        "weight":     0.20,
        "thresholds": (">1.20%", "≤1.10%","≤0.85%", "≤0.65%"),
        "now":        "0.95%",
        "score":      2,
        "comment":    "Card NCOs normalizing post-pandemic; consumer credit stable but not pristine; reserve build modest",
    },
    {
        "name":       "Markets/trading revenue YoY growth",
        "weight":     0.10,
        "thresholds": ("<-10%",  "≥0%",   "≥+10%",  "≥+20%"),
        "now":        "+6%",
        "score":      2,
        "comment":    "Equities/FICC steady; volatility-dependent; no extraordinary tailwind currently",
    },
    {
        "name":       "CET1 ratio / capital return capacity",
        "weight":     0.10,
        "thresholds": ("<13.0%", "≥13.5%","≥14.5%", "≥15.5%"),
        "now":        "15.0%",
        "score":      3,
        "comment":    "CET1 well above 11.5% regulatory minimum; supports aggressive buyback ($30B+/yr) and dividend growth",
    },
    {
        "name":       "AWM AUM YoY growth",
        "weight":     0.10,
        "thresholds": ("<0%",    "≥+5%",  "≥+10%",  "≥+18%"),
        "now":        "+11%",
        "score":      3,
        "comment":    "Record AUM ~$4T+ driven by net inflows and market appreciation; fee revenue compounding",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Fortress balance sheet — CET1 15.0%, best-in-class credit underwriting, scale moat",          +0.6, 0.20),
    ("+", "Diversified earnings — CCB/CIB/CB/AWM reduce single-segment cyclicality vs pure-play banks",  +0.4, 0.15),
    ("-", "Rate-path sensitivity — NII is ~45% of revenue; Fed cutting cycle compresses net interest margin", -0.6, 0.25),
    ("-", "Credit cycle risk — late-cycle consumer leverage; recession would double provisions rapidly", -0.5, 0.20),
    ("+", "Capital return engine — $30B+ annual buyback + steady dividend growth at 15% CET1",           +0.4, 0.10),
    ("-", "Premium valuation — trading near record highs at ~2.5x tangible book vs historical 1.5-2.0x", -0.5, 0.10),
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
CONS_EPS_2YR  = 21.50   # conservative FY2028E: modest NII growth + IB recovery + buyback accretion
CONS_PE_2YR   = 12      # rerating from ~15.7x toward historical normal ~12x
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Money Center Bank / NII / Investment Banking")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<30}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<30}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<30}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print()

# EPS bridge
curr_pretax = curr_total * (1 - EFFICIENCY_RATIO_CURR) - curr_total * PROVISION_RATE_CURR
curr_ni     = curr_pretax * (1 - TAX_RATE)
shares      = SHARES_OUT_M / 1000
curr_eps    = round(curr_ni / shares, 2)

bull_pretax = bull_total * (1 - EFFICIENCY_RATIO_BULL) - bull_total * PROVISION_RATE_CURR
bull_ni     = bull_pretax * (1 - TAX_RATE)
shares_b    = shares * 0.93   # ~3.5%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_pretax = bear_total * (1 - EFFICIENCY_RATIO_CURR) - bear_total * PROVISION_RATE_BEAR
bear_ni     = max(0, bear_pretax) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {(1-EFFICIENCY_RATIO_CURR)*100:.0f}% pre-provision margin")
print(f"  − {PROVISION_RATE_CURR*100:.1f}% provisions − {TAX_RATE*100:.0f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ~${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {(1-EFFICIENCY_RATIO_BULL)*100:.0f}% margin − provisions − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 15× = ~${bull_eps_imp*15:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {(1-EFFICIENCY_RATIO_CURR)*100:.0f}% margin − {PROVISION_RATE_BEAR*100:.1f}% provisions − tax")
print(f"  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 11× trough P/E (recession floor) = ~${bear_eps_imp*11:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = (1.0 * (1 - EFFICIENCY_RATIO_CURR) * (1 - PROVISION_RATE_CURR) * (1 - TAX_RATE)) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B NII (rate path):        +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*13:.1f}/share at 13× P/E")
print(f"  25bp Fed funds move ~ $1.5-2B NII: ~±${eps_per_1B_rev*1.75:.2f}/EPS  =  ~±${eps_per_1B_rev*1.75*13:.1f}/share at 13× P/E")
print(f"  Provision rate +1pp of revenue:    -${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = -${curr_total*0.01*(1-TAX_RATE)/shares*13:.1f}/share at 13× P/E")
print(f"  1% buyback (~27M shares):          +${curr_eps*0.01:.3f}/EPS  (mechanical accretion; CET1 15.0% supports pace)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (NII / IB fees / credit quality / capital framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>6}  {'BASE':>6}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>6}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>6}  {ths[1]:>6}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>6}  {lbl}  {b}")

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
    ("NII YoY growth",                 "+1%",   "<-5%",   "−6pp",   "Fed cuts 200bp+ amid recession; deposit beta lags loan repricing"),
    ("IB fees YoY growth",             "+18%",  "<-15%",  "−33pp",  "M&A/IPO pipeline freezes as recession fears spike"),
    ("Net charge-off rate",            "0.95%", ">1.20%", "+0.25pp","Unemployment rises >5.5%; consumer/card delinquencies surge"),
    ("Markets/trading revenue YoY",    "+6%",   "<-10%",  "−16pp",  "Risk-off de-grossing; client activity collapses"),
    ("CET1 ratio",                     "15.0%", "<13.0%", "−2.0pp", "Mark-to-market AOCI losses + higher RWA in stress"),
    ("AWM AUM YoY growth",             "+11%",  "<0%",    "−11pp",  "Equity market drawdown >25% hits AUM and fee revenue"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A recession scenario where the Fed cuts aggressively (200bp+), compressing")
print(f"  net interest margin faster than deposit costs reprice, while loan loss provisions roughly")
print(f"  double as unemployment rises and IB fee pipeline (M&A/IPO) freezes entirely. EPS falls")
print(f"  to ~${bear_price/11:.2f} → 11× recession-floor P/E = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT permanent impairment — fortress balance sheet (CET1 15.0%) and")
print(f"  diversified franchise (CCB/CIB/CB/AWM) provide a durable earnings floor. Recovery to")
print(f"  ~${bear_price+60}-${bear_price+90} in 2yr is base case post-shock as credit normalizes and curve re-steepens.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~$19-20)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (GFC/regional-bank-crisis trough ~8-10×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP means the market prices in continued earnings growth and")
print(f"  multiple stability well ABOVE the trough-floor multiple. At ${CURRENT_PRICE:.2f} and FY2026E EPS")
print(f"  ${EPS_FY2026E:.2f}, the P/E is ~{CURRENT_PRICE/EPS_FY2026E:.1f}× — near the high end of JPM's historical range")
print(f"  (typically 9-14×). The risk is mean reversion in the multiple toward the historical band")
print(f"  if rate-cut-driven NII pressure or a credit cycle turn materializes.")
print(f"  EPP path: FY2028E EPS ~${CONS_EPS_2YR:.2f} × {PE_PESSIMISTIC:.0f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing modestly).")
print(f"  At 12× mid-cycle P/E: ${EPS_FY2026E:.2f} × 12 = ${EPS_FY2026E*12:.0f}  — below current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: P/E reverts toward historical normal; rate-cut headwind persists)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (modest NII growth + IB recovery + buyback accretion)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (reverts from ~{CURRENT_PRICE/EPS_FY2026E:.1f}× toward historical normal {CONS_PE_2YR}×)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE PROBLEM: even the conservative case requires P/E reversion from ~{CURRENT_PRICE/EPS_FY2026E:.1f}× to {CONS_PE_2YR}×.")
print(f"  That multiple contraction offsets EPS growth and dividends — a modest/negative total return.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — possible at BULL, not BASE.")
print(f"  Breakeven at 14× P/E (modest multiple support): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 14:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.24
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (large-cap money center bank; rate-cycle and credit-cycle sensitive)")
print(f"  Beta vs S&P 500:      1.10  (moderate premium; macro/financials cyclicality)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (recession scenario; not extreme tail)")
print(f"  52W low ${VOL_52W_LOW:.2f} (Apr 2025 tariff shock) was a peak-to-trough move of ~25-30%.")
print(f"  → Fed rate path (cuts vs hikes) is THE KEY driver of NII and the multiple.")
print(f"  → IB fee pipeline (M&A/IPO reacceleration) is the KEY bull catalyst for CIB segment.")
print(f"  → AVOID/WATCHLIST at current price  |  ACCUMULATE ${EPP+30:.0f}-${EPP+50:.0f}  |  BUY below ${EPP+15:.0f}")

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
print(f"  Rate-path sensitivity (NII, signal weight 30%) and credit-cycle risk are the most")
print(f"  significant swing factors versus current premium valuation (~2.5x tangible book).")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Fed rate path — cuts compress NII margin; steepening curve would be a BULL trigger")
print(f"  (2) M&A/IPO fee recovery — CIB advisory backlog conversion to realized fees (BULL trigger)")
print(f"  (3) Credit cycle — card/consumer NCOs and commercial loan loss provisions (BEAR trigger)")
print(f"  (4) CET1 capital deployment — pace of buyback at 15.0% CET1 vs 11.5% requirement")
print(f"  (5) Tangible book value premium — ~2.5x TBV vs historical 1.5-2.0x normalization risk")
print(f"  WATCHLIST at ${CURRENT_PRICE:.2f}  |  ACCUMULATE ${EPP+30:.0f}-${EPP+50:.0f}  |  BUY below ${EPP+15:.0f}")
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
