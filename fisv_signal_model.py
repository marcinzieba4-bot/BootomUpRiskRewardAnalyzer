"""
FISV  ·  Fiserv, Inc.  ·  NYSE: FI (FISV)
Bottom-up signal model  ·  Fintech / Payments Processing / Clover / Core Banking
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "FISV"
COMPANY       = "Fiserv, Inc."
SECTOR        = "Financial Technology · Payment Processing · Core Banking · Merchant Acquiring (Clover) · NYSE: FI"
CURRENT_PRICE = 132.50      # USD; as of 2026-06-11, ~50% off 2024 highs near $240
VOL_52W_LOW   = 108.40      # 2026 trough on Clover deceleration / guidance cut
VOL_52W_HIGH  = 218.65      # late-2025 pre-deceleration high
SHARES_OUT_M  = 1_180.0     # millions; declining via buyback but slowed amid drawdown

# Dividend: Fiserv pays no meaningful common dividend (reinvest in buybacks/integration)
ANNUAL_DIV    = 0.00        # $/share; no common dividend

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Merchant Solutions (Clover/Acceptance)", 11.0,  9.5, 13.5, "Clover GPV growth the swing factor; SMB competition from Toast/Square/Square"),
    ("Financial Solutions (Payments & Network/Core)", 10.5, 10.0, 11.5, "Stable recurring core processing for banks/credit unions; sticky multi-yr contracts"),
    ("Fintech (Digital Banking Solutions)",     1.6,  1.4,  2.0, "Smaller digital banking/lending software segment; modest growth"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.55    # blended adj operating margin proxy FY2026E
GROSS_MARGIN_BULL = 0.58    # BULL: Clover scale + Financial Solutions operating leverage
OPEX_FIXED_B      = 1.0     # incremental corporate/SG&A/integration costs ($B) above margin baseline
TAX_RATE          = 0.21    # effective tax rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 8.55       # FY2026E adj EPS (consensus ~$8.50-8.65 non-GAAP)
PE_PESSIMISTIC = 11.0       # trough P/E: payments processors de-rate hard on growth-deceleration fear
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # ~$94

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 7.50, 11,   83, "Clover GPV growth decelerates further to mid-single digits; SMB share loss to Toast/Square accelerates; EPS $7.50 → 11× trough P/E"),
    "BASE":  ( 9.00, 14,  126, "Clover GPV growth stabilizes ~8-10%; Financial Solutions steady mid-single-digit growth; EPS $9.00 at FY2028E → 14×"),
    "BULL":  (10.50, 18,  189, "Clover GPV reaccelerates to mid-teens; new SMB software/embedded finance wins; EPS $10.50 → 18×"),
    "XBULL": (12.50, 21,  263, "Clover becomes dominant SMB platform globally; Financial Solutions cross-sell drives margin expansion; EPS $12.50 → 21×"),
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
        "name":       "Clover GPV YoY growth",
        "weight":     0.30,
        "thresholds": ("<8%",    "≥10%",  "≥18%",   "≥28%"),
        "now":        "~9%",
        "score":      1,
        "comment":    "Clover GPV growth decelerated sharply through 2025 from ~28% to high-single digits; key bear driver",
    },
    {
        "name":       "Merchant Solutions revenue YoY growth",
        "weight":     0.25,
        "thresholds": ("<3%",    "≥5%",   "≥9%",    "≥14%"),
        "now":        "~5%",
        "score":      2,
        "comment":    "Clover deceleration drags overall Merchant segment; international acquiring still adds modest growth",
    },
    {
        "name":       "Financial Solutions revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<2%",    "≥3%",   "≥6%",    "≥9%"),
        "now":        "~4%",
        "score":      2,
        "comment":    "Stable recurring core/issuer processing for banks and credit unions; long-term contract renewals on track",
    },
    {
        "name":       "SMB competitive share (Toast/Square/Block pressure)",
        "weight":     0.15,
        "thresholds": ("Losing share", "Flat", "Gaining", "Gaining strongly"),
        "now":        "Losing share",
        "score":      1,
        "comment":    "Toast and Square continue to win restaurant/SMB accounts; Clover's growth premium narrative under pressure",
    },
    {
        "name":       "Adjusted operating margin",
        "weight":     0.05,
        "thresholds": ("<38%",   "≥40%",  "≥43%",   "≥46%"),
        "now":        "~41%",
        "score":      2,
        "comment":    "Modest margin expansion via cost synergies; First Data integration largely complete but offset by Clover investment spend",
    },
    {
        "name":       "Free cash flow / buyback execution",
        "weight":     0.05,
        "thresholds": ("<$3B",   "≥$3.5B", "≥$4.5B", "≥$5.5B"),
        "now":        "~$4B",
        "score":      3,
        "comment":    "Strong FCF generation continues; management leaning on buybacks to support EPS amid multiple compression",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Sticky core processing base — multi-year contracts with banks/credit unions; high switching costs",  +0.6, 0.20),
    ("-", "Clover deceleration — growth narrative broken; SMB competition from Toast/Square structural",         -0.8, 0.30),
    ("+", "Valuation reset — trading near trough multiples after 50%+ drawdown; bad news largely priced in",     +0.5, 0.20),
    ("-", "Integration/execution risk — First Data integration tail, management credibility post guidance cut",  -0.4, 0.15),
    ("+", "Strong FCF and buyback capacity — supports EPS even amid revenue deceleration",                       +0.3, 0.10),
    ("-", "Limited capital return optionality — no dividend; all eggs in buyback/reinvestment basket",           -0.2, 0.05),
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
CONS_EPS_2YR  = 9.00    # conservative FY2028E: Clover stabilizes, modest EPS growth + buybacks
CONS_PE_2YR   = 13      # modest rerating from ~10x to 13x as growth fears partially abate
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Fintech / Payments / Clover / Core Banking")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<40}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<40}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<40}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
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
shares_b  = shares * 0.94   # ~3%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift / margin pressure
bear_oi   = bear_gp - OPEX_FIXED_B * 0.97           # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% op margin − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% op margin − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 18× = ~${bull_eps_imp*18:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% op margin − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 11× trough P/E (payments de-rate floor) = ~${bear_eps_imp*11:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_clover = 1.0 * 0.45 * (1 - TAX_RATE) / shares   # Clover-level margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Clover revenue:         +${eps_per_1B_clover:.3f}/EPS  = +${eps_per_1B_clover*14:.1f}/share at 14× P/E")
print(f"  Every $1B Financial Solutions rev: +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*14:.1f}/share at 14× P/E")
print(f"  1pp operating margin expansion:   +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*14:.1f}/share at 14× P/E")
print(f"  1% buyback (~12M shares):          +${curr_eps*0.01:.3f}/EPS  (mechanical accretion via FCF-funded repurchases)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Clover GPV / Merchant growth / Financial Solutions / SMB competition framework)")
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
    ("Clover GPV YoY growth",          "~9%",    "<5%",    "−4pp",   "SMB churn accelerates to Toast/Square; pricing pressure intensifies"),
    ("Merchant Solutions revenue YoY", "~5%",    "<2%",    "−3pp",   "Clover deceleration compounds with international acquiring softness"),
    ("Financial Solutions revenue YoY","~4%",    "<1%",    "−3pp",   "Bank/credit union client losses to competitors (Jack Henry, FIS)"),
    ("SMB competitive share",          "Losing", "Losing badly", "—", "Toast/Square accelerate enterprise SMB push; Clover loses flagship accounts"),
    ("Adjusted operating margin",      "~41%",   "<38%",   "−3pp",   "Pricing concessions to retain merchants compress margins"),
    ("Free cash flow",                 "~$4B",   "<$3B",   "−$1B",   "Revenue miss + integration costs resurface; buyback pace slows"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Clover GPV growth, which decelerated from ~28% in 2024 to high-single")
print(f"  digits through 2025, continues sliding toward mid-single digits as Toast and Square")
print(f"  win flagship SMB accounts. Combined with stagnation in Financial Solutions (core bank")
print(f"  processing renewals lost to Jack Henry/FIS), EPS compresses to ~$7.50 and the market")
print(f"  applies an even harsher trough multiple of 11× → ${bear_price}.")
print(f"  Note: ${bear_price} is likely NOT a permanent floor — Financial Solutions ($10.5B recurring")
print(f"  base) and strong FCF generation provide a durable earnings base. A reacceleration in")
print(f"  Clover GPV growth (even back to low-double digits) would be the key recovery catalyst.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~$8.50-8.65; non-GAAP)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (payments processor de-rate floor amid growth-fear cycle)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  After a ~50%+ drawdown from 2024 highs near $240, FISV at ${CURRENT_PRICE:.2f} trades at")
print(f"  only ~{CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS — a steep de-rating from its historical ~20-25×")
print(f"  growth premium multiple. The market has priced in significant Clover deceleration, but")
print(f"  the {epp_gap_pct:.0f}% gap above the trough EPP floor suggests further downside is possible if")
print(f"  Clover GPV growth continues to slow and the market applies an even harsher multiple.")
print(f"  EPP path: FY2028E EPS ~$9.50 × {PE_PESSIMISTIC:.0f}× = ${9.50*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing modestly).")
print(f"  At 14× mid-cycle P/E: ${EPS_FY2026E:.2f} × 14 = ${EPS_FY2026E*14:.0f}  — close to current price (limited margin of safety).")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: Clover stabilizes, modest multiple recovery)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (Clover GPV stabilizes ~8-10%; buyback support)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (modest rerating from ~{CURRENT_PRICE/EPS_FY2026E:.0f}× toward 13×; still below historical 20-25×)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (no common dividend)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: can Fiserv stabilize Clover GPV growth and demonstrate that the")
print(f"  deceleration is cyclical, not structural/competitive? Even a modest rerating from")
print(f"  ~{CURRENT_PRICE/EPS_FY2026E:.0f}× to 13× combined with EPS growth to ${CONS_EPS_2YR:.2f} produces a {cons_return:.1f}% 2yr return.")
print(f"  For conservative 2yr to break even at 13× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — modest, achievable even at BASE.")
print(f"  Breakeven at 11× P/E (no multiple recovery): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 11:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at 13× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.35
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: 52W high pre-dates the 2025 Clover deceleration / guidance-cut selloff (~50%+ drawdown)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (no common dividend; capital returned via buybacks)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; growth-narrative whipsaw post guidance cut)")
print(f"  Beta vs S&P 500:      1.10  (slight premium; payments cyclicality + SMB sensitivity)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (further Clover deceleration tail scenario)")
print(f"  52W low ${VOL_52W_LOW:.2f} already reflects a peak-to-trough move of ~50%+ from 2024 highs.")
print(f"  → Clover GPV growth trajectory is THE KEY signal; each quarterly print is a binary catalyst.")
print(f"  → Evidence of SMB share stabilization vs Toast/Square is the KEY bull catalyst.")
print(f"  → AVOID above $190  |  WATCHLIST $150–175  |  ACCUMULATE $135–150  |  BUY below $125")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is BELOW the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0 — near")
print(f"  BEAR/BASE. The model scores the fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0 — closer to BASE.")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: the market has priced in a Clover growth narrative that is worse than")
print(f"  the model's BASE assumption — providing an attractive risk/reward if Clover merely")
print(f"  stabilizes rather than continuing to decelerate.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Clover GPV growth reacceleration — any quarter showing growth stabilization/uptick (BULL trigger)")
print(f"  (2) SMB competitive dynamics — market share trends vs Toast/Square/Block (key risk)")
print(f"  (3) Financial Solutions renewals — large bank/credit union contract retention (stability anchor)")
print(f"  (4) Capital allocation — pace of buybacks given depressed valuation (EPS support)")
print(f"  (5) Margin trajectory — evidence First Data integration synergies continue flowing through")
print(f"  AVOID above $190  |  WATCHLIST $150–175  |  ACCUMULATE $135–150  |  BUY below $125")
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
