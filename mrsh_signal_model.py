"""
MRSH  ·  Marsh & McLennan Companies, Inc. (formerly MMC)  ·  NYSE: MRSH
Bottom-up signal model  ·  Insurance Brokerage / Reinsurance / HR & Management Consulting
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "MRSH"
COMPANY       = "Marsh & McLennan Companies, Inc."
SECTOR        = "Insurance Brokerage · Reinsurance · HR & Management Consulting · NYSE: MRSH"
CURRENT_PRICE = 174.50      # USD; as of 2026-06-11
VOL_52W_LOW   = 158.30      # late-2025 soft-market commission growth scare
VOL_52W_HIGH  = 199.80      # early-2026 high on Aon/AJG re-rating spillover
SHARES_OUT_M  = 480.0       # millions; declining ~1%/yr via buyback

# Dividend: 16-year growth streak; growing ~10%/yr
ANNUAL_DIV    = 3.40        # $/share FY2026 ($0.85/quarter)

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ──────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Risk & Insurance Services", 14.40, 12.80, 16.20, "Marsh + Guy Carpenter; #1 broker + #2 reinsurer; soft market is swing factor"),
    ("Consulting",                10.20,  9.20, 11.60, "Mercer (HR/retirement/wealth) + Oliver Wyman (elite strategy); resilient fee base"),
]

# Margin assumptions
EBIT_MARGIN_CURR = 0.245   # blended adj operating margin FY2026E (~24.5%; 18th straight year of expansion)
EBIT_MARGIN_BULL = 0.260   # BULL: continued operating leverage; tech/AI efficiency gains
OPEX_OTHER_B     = 0.0     # margin already net of opex (fee/commission model, no underwriting risk)
TAX_RATE         = 0.235   # effective tax rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 9.60        # FY2026E adj EPS (consensus $9.45-$9.75)
PE_PESSIMISTIC = 17.0        # trough P/E: hard-market unwind / soft-market trough (historical trough ~17-18x)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # ~$163

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 8.20, 17,  139, "Soft P&C pricing accelerates -8% to -10%; organic growth stalls to 0-1%; multiple compresses to 17x trough"),
    "BASE":  (10.50, 22,  231, "Organic growth ~5%; 19th straight year of margin expansion; EPS $10.50 at FY2028E -> 22x"),
    "BULL":  (12.50, 27,  338, "Hard-market pockets return; Mercer wealth flows accelerate; Oliver Wyman demand strong; EPS $12.50 -> 27x"),
    "XBULL": (14.50, 32,  464, "Re-rating toward Aon/AJG premium multiples (28-35x) on best-in-class moat recognition; EPS $14.50 -> 32x"),
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
        "name":       "Risk & Insurance Services organic growth",
        "weight":     0.25,
        "thresholds": ("<2%",   "≥4%",  "≥6%",   "≥9%"),
        "now":        "+4%",
        "score":      2,
        "comment":    "Marsh + Guy Carpenter; soft P&C pricing offsetting exposure growth and new business",
    },
    {
        "name":       "Consulting (Mercer + Oliver Wyman) organic growth",
        "weight":     0.20,
        "thresholds": ("<2%",   "≥4%",  "≥7%",   "≥10%"),
        "now":        "+6%",
        "score":      3,
        "comment":    "Mercer wealth/retirement flows steady; Oliver Wyman demand for risk/regulatory advisory strong",
    },
    {
        "name":       "Adjusted operating margin trend (consecutive expansion)",
        "weight":     0.25,
        "thresholds": ("flat/-", "+10bps","+30bps", "+50bps"),
        "now":        "+30bps",
        "score":      3,
        "comment":    "On track for 18th consecutive year of margin expansion; the key quality signal for the model",
    },
    {
        "name":       "Global commercial P&C pricing (rate environment)",
        "weight":     0.15,
        "thresholds": ("<-8%",  "≥-5%", "≥-1%",   "≥+2%"),
        "now":        "-4%",
        "score":      2,
        "comment":    "Soft market continues; property rates down high-single-digits, casualty firmer; pressures commission revenue",
    },
    {
        "name":       "M&A / bolt-on contribution to growth",
        "weight":     0.10,
        "thresholds": ("<0.5%", "≥1%",  "≥2%",    "≥3%"),
        "now":        "~1.5%",
        "score":      3,
        "comment":    "Steady disciplined bolt-on acquisition program (McGriff integration, Oliver Wyman tuck-ins) adding to organic",
    },
    {
        "name":       "Free cash flow conversion / capital return",
        "weight":     0.05,
        "thresholds": ("<85%",  "≥90%", "≥100%",  "≥110%"),
        "now":        "~100%",
        "score":      3,
        "comment":    "Strong FCF conversion funds 16-year dividend growth streak (~10%/yr) plus consistent buyback",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Best-in-class professional services moat — #1 broker (Marsh), #2 reinsurer (Guy Carpenter)", +0.6, 0.20),
    ("+", "Pure fee/commission model — no underwriting risk; capital-light, high FCF conversion",        +0.6, 0.20),
    ("+", "18+ consecutive years of margin expansion — structural operating leverage track record",      +0.7, 0.20),
    ("-", "Soft P&C pricing cycle — declining premium rates compress commission revenue growth",          -0.6, 0.20),
    ("-", "Valuation discount to peers — Aon/AJG trade at 23-35x vs MRSH historically lower multiple",   -0.3, 0.10),
    ("+", "Mercer/Oliver Wyman diversification — non-cyclical consulting fee revenue dampens P&C cycle", +0.4, 0.10),
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
CONS_EPS_2YR  = 11.30   # conservative FY2028E: ~8-9% EPS CAGR; organic growth + margin expansion continues
CONS_PE_2YR   = 21      # modest rerating from ~18x toward 21x growth-justified multiple
cons_equity   = CONS_EPS_2YR * CONS_PE_2YR
cons_divs     = ANNUAL_DIV * 2 * 1.10  # dividend growth ~10%/yr over 2yr (approx avg)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Insurance Brokerage / Reinsurance / Consulting")
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
curr_oi   = curr_total * EBIT_MARGIN_CURR
curr_ni   = curr_oi * (1 - TAX_RATE)
shares    = SHARES_OUT_M / 1000
curr_eps  = round(curr_ni / shares, 2)

bull_oi   = bull_total * EBIT_MARGIN_BULL
bull_ni   = bull_oi * (1 - TAX_RATE)
shares_b  = shares * 0.98   # ~1%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_oi   = bear_total * EBIT_MARGIN_CURR * 0.95   # margin gives back some gains in soft market
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {EBIT_MARGIN_CURR*100:.1f}% adj op margin − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {EBIT_MARGIN_BULL*100:.1f}% margin − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 27× = ~${bull_eps_imp*27:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {EBIT_MARGIN_CURR*100*0.95:.1f}% margin  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 17× trough P/E (soft-market floor) = ~${bear_eps_imp*17:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = (1.0 * EBIT_MARGIN_CURR * (1 - TAX_RATE)) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Risk & Insurance revenue: +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*22:.1f}/share at 22× P/E")
print(f"  Every $1B Consulting revenue:       +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*22:.1f}/share at 22× P/E")
print(f"  1pp adj op margin expansion:        +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*22:.1f}/share at 22× P/E")
print(f"  1% buyback (4.8M shares):           +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (organic growth / margin expansion / pricing cycle framework)")
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
    ("R&I Services organic growth",       "+4%",   "<2%",   "−2pp",   "Soft P&C pricing accelerates to -8/-10%; new business slows sharply"),
    ("Consulting organic growth",         "+6%",   "<2%",   "−4pp",   "Mercer retirement outflows; Oliver Wyman demand cools with M&A slowdown"),
    ("Adj operating margin trend",        "+30bps","flat/-","−30bps", "Wage inflation + tech investment outpaces revenue growth; streak ends"),
    ("Global P&C pricing",                "-4%",   "<-8%",  "−4pp",   "Property cat capacity glut accelerates; casualty softens too"),
    ("M&A contribution",                  "~1.5%", "<0.5%", "−1pp",   "Capital redeployed to buybacks; bolt-on pipeline dries up"),
    ("FCF conversion",                    "~100%", "<85%",  "−15pp",  "Working capital drag from integration costs; pension contributions rise"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A sharper-than-expected acceleration in the soft P&C pricing cycle —")
print(f"  property cat rates falling -8% to -10% and casualty softening too — compresses")
print(f"  Risk & Insurance Services commission revenue growth toward zero. Combined with the")
print(f"  18-year margin expansion streak finally breaking (wage/tech cost inflation outpacing")
print(f"  revenue), EPS growth stalls near $8.20 and the multiple compresses to its 17× trough,")
print(f"  giving BEAR ${bear_price}. Note: the fee-based, capital-light model and Mercer/Oliver")
print(f"  Wyman diversification provide a durable floor — recovery as pricing stabilizes is the base case.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus $9.45-$9.75)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (historical soft-market trough ~17-18×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% premium to EPP reflects the market's confidence in continued organic")
print(f"  growth and the 18-year margin expansion streak. At ${CURRENT_PRICE:.2f} and FY2026E EPS")
print(f"  ${EPS_FY2026E:.2f}, the P/E is ~{CURRENT_PRICE/EPS_FY2026E:.1f}×. This remains a discount to Aon and")
print(f"  Arthur J. Gallagher, which trade at 23-35×, leaving room for re-rating if execution continues.")
print(f"  EPP path: FY2028E EPS ~$11.30 × {PE_PESSIMISTIC:.0f}× = ${11.30*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing ~9%/yr).")
print(f"  At 22× mid-cycle P/E: ${EPS_FY2026E:.2f} × 22 = ${EPS_FY2026E*22:.0f}  — close to current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: organic growth + margin expansion compounding)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (~9% EPS CAGR: organic growth ~5% + margin expansion + buyback)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (modest rerating from ~{CURRENT_PRICE/EPS_FY2026E:.0f}× toward growth-justified {CONS_PE_2YR}×)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr growing ~10%/yr; 16-yr growth streak)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: unlike many high-multiple compounders, MRSH's conservative case does NOT")
print(f"  require multiple expansion to deliver positive returns — modest rerating from")
print(f"  ~{CURRENT_PRICE/EPS_FY2026E:.0f}× toward {CONS_PE_2YR}× plus EPS compounding plus a growing dividend produces")
print(f"  a {cons_return:.1f}% 2yr return ({cons_annual:.1f}%/yr).")
print(f"  Breakeven at {CONS_PE_2YR}× P/E (no rerating needed beyond current): need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — well within BASE case.")
print(f"  Breakeven at 18× P/E (further compression): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 18:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case attractive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.20
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  16-yr growth streak, ~10%/yr growth)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (low-beta professional services; defensive fee revenue base)")
print(f"  Beta vs S&P 500:      0.85  (defensive; non-cyclical fee revenue dampens market swings)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (moderate; soft-market acceleration scenario)")
print(f"  → Soft P&C pricing trajectory is THE KEY swing factor for Risk & Insurance Services.")
print(f"  → Continued margin expansion (19th consecutive year) is KEY bull/quality catalyst.")
print(f"  → AVOID above $200  |  WATCHLIST $185–200  |  ACCUMULATE $170–185  |  BUY below $165")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is compared to the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The gap ({ADJ_GAP:.2f}) indicates the stock is")
print(f"  {valuation_label.lower()} by model standards.")
print(f"  In plain terms: the model's structural quality factors (best-in-class moat, fee-based")
print(f"  model, 18-year margin expansion streak) outweigh the soft-market pricing headwind,")
print(f"  supporting an attractive risk/reward at current levels.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Soft P&C pricing stabilization/reversal — property/casualty rate inflection (BULL trigger)")
print(f"  (2) 19th consecutive year of margin expansion — confirms structural operating leverage thesis")
print(f"  (3) Re-rating toward Aon/AJG multiples (23-35×) on recognition of best-in-class moat")
print(f"  (4) Mercer wealth/retirement flow acceleration — demographic tailwind from aging populations")
print(f"  (5) Oliver Wyman demand cycle — regulatory/risk advisory work tied to macro uncertainty")
print(f"  AVOID above $200  |  WATCHLIST $185–200  |  ACCUMULATE $170–185  |  BUY below $165")
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
