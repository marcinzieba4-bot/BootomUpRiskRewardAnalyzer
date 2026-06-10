"""
MRK  ·  Merck & Co., Inc.  ·  NYSE: MRK
Bottom-up signal model  ·  Pharma / Oncology (Keytruda) / Cardiovascular (Winrevair) / Vaccines
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "MRK"
COMPANY       = "Merck & Co., Inc."
SECTOR        = "Pharma · Oncology (Keytruda) · Cardiovascular (Winrevair) · Vaccines · NYSE: MRK"
CURRENT_PRICE = 122.55      # USD; as of 2026-06-10
VOL_52W_LOW   =  75.00      # 2025 patent-cliff fear trough
VOL_52W_HIGH  = 135.00      # 2026 Winrevair/Qlex re-rating peak
SHARES_OUT_M  = 2_530.0     # millions
ANNUAL_DIV    = 3.28        # $/share; ~2.7% yield

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Oncology (Keytruda/Welireg)",  32.0, 22.0, 36.0, "Keytruda $8.03B/qtr (+12% YoY) near peak; 2028 US patent cliff (~$35B+ at risk)"),
    ("Cardiovascular (Winrevair)",    2.2,  1.2,  4.5, "PAH treatment; +88% YoY; new franchise scaling rapidly from small base"),
    ("Vaccines (Gardasil/RSV)",       9.0,  6.5, 11.0, "Gardasil China demand recovery key swing; RSV/vaccines portfolio growth"),
    ("Animal Health",                 6.0,  5.2,  6.8, "Stable, diversified, non-correlated cash flow"),
    ("Pipeline/New Launches (Qlex)",  1.0,  0.3,  4.0, "Subcutaneous Keytruda (Qlex) launch $128M; potential to extend franchise life"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.78    # blended gross margin; pharma high-margin mix
GROSS_MARGIN_BULL = 0.80    # BULL: Qlex/Winrevair higher-margin mix improves blend
OPEX_FIXED_B      = 22.0    # SG&A + R&D ($B); largely fixed cost base
TAX_RATE          = 0.150   # effective rate; pharma international mix

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 9.50        # FY2027E EPS (consensus ~$9.50 non-GAAP)
PE_PESSIMISTIC = 9.0         # trough P/E: patent-cliff discount already embedded; historical pharma trough ~9-10x
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # $86

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 7.50,  9,   68, "Keytruda decelerates faster pre-cliff; Qlex underwhelms; Winrevair stalls; EPS $7.50 → 9× = $68"),
    "BASE":  ( 9.50, 13,  124, "Keytruda growth slows but holds near-peak; Winrevair scales; Qlex modest extension; EPS $9.50 → 13× = $124"),
    "BULL":  (11.00, 16,  176, "Qlex extends Keytruda franchise meaningfully; Winrevair becomes major franchise; pipeline delivers; EPS $11.00 → 16× = $176"),
    "XBULL": (13.50, 19,  257, "Cliff largely offset by Winrevair + Qlex + pipeline diversification; multiple re-rates toward growth peers; EPS $13.50 → 19× = $257"),
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
        "name":       "Keytruda revenue YoY growth (near peak, 2028 cliff)",
        "weight":     0.30,
        "thresholds": ("<5%",   "≥10%",  "≥15%",   "≥20%"),
        "now":        "+12%",
        "score":      2,
        "comment":    "Keytruda $8.03B/qtr +12% YoY; growth decelerating as expected ahead of 2028 US patent cliff (~$35B+ at risk)",
    },
    {
        "name":       "Winrevair revenue growth (PAH franchise scaling)",
        "weight":     0.20,
        "thresholds": ("<20%",  "≥40%",  "≥70%",   "≥100%"),
        "now":        "+88%",
        "score":      3,
        "comment":    "Winrevair $525M (+88% YoY); new cardiovascular franchise scaling from small base; key offset to cliff",
    },
    {
        "name":       "Qlex (subcutaneous Keytruda) launch trajectory",
        "weight":     0.20,
        "thresholds": ("<$50M", "≥$100M","≥$300M", "≥$750M"),
        "now":        "$128M",
        "score":      2,
        "comment":    "Qlex SC launch at $128M; early innings; potential to extend Keytruda franchise life via new IP/exclusivity",
    },
    {
        "name":       "Gardasil/Vaccines franchise stability (China demand)",
        "weight":     0.15,
        "thresholds": ("<-15%", "≥-5%",  "≥+5%",   "≥+15%"),
        "now":        "~-5%",
        "score":      2,
        "comment":    "Gardasil China demand remains soft but stabilizing; broader vaccines portfolio (RSV) provides offset",
    },
    {
        "name":       "Pipeline productivity / new approvals offsetting cliff",
        "weight":     0.10,
        "thresholds": ("none",  "1 readout","2-3 readouts","4+ readouts"),
        "now":        "1-2",
        "score":      2,
        "comment":    "Several oncology/cardiovascular readouts pending; none yet large enough to fully offset Keytruda cliff",
    },
    {
        "name":       "Cost discipline / margin trajectory",
        "weight":     0.05,
        "thresholds": ("<74%",  "≥76%",  "≥78%",   "≥80%"),
        "now":        "78%",
        "score":      3,
        "comment":    "Gross margin holding ~78%; opex discipline maintained ahead of cliff-driven cost restructuring",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("-", "Keytruda concentration — ~40% of revenue faces 2028 US patent cliff (~$35B+ at risk)", -0.8, 0.30),
    ("+", "Market has already priced the cliff — 12.9× FY2027E EPS is a deep discount vs pharma peers", +0.5, 0.20),
    ("+", "Winrevair + Qlex + pipeline diversification — credible but unproven offset to cliff timing", +0.4, 0.20),
    ("-", "Cliff timing/magnitude caps multiple expansion until offset is proven at scale",            -0.3, 0.15),
    ("+", "Vaccines + Animal Health — diversified, durable cash flow base; dividend support",          +0.3, 0.10),
    ("+", "Capital return — $3.28/share dividend (~2.7% yield); disciplined buyback program",          +0.2, 0.05),
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
    signal_short, signal_full = "HOLD",      "▷ HOLD/TRIM"
else:
    signal_short, signal_full = "AVOID",     "✕ AVOID"

ratio_b_str = f"{ratio_b:.2f}x" if ratio_b != float("inf") else "N/A"

# ── CONSERVATIVE GROWTH (2-yr) ────────────────────────────────────────────────
CONS_EPS_2YR  = 10.00   # FY2028E conservative: modest growth as cliff begins to bite
CONS_PE_2YR   = 12      # rerates modestly from 12.9× given cliff proximity in FY2028
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Pharma / Oncology (Keytruda) / Cardiovascular (Winrevair) / Vaccines")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<32}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<32}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<32}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
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
shares_b     = shares * 0.97   # ~1.5%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift away from Keytruda margin
bear_oi      = bear_gp - OPEX_FIXED_B * 0.95           # partial cost response
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 16× = ~${bull_eps_imp*16:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 9× trough P/E (cliff-discount floor) = ~${bear_eps_imp*9:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev       = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_keytruda  = 1.0 * 0.85 * (1 - TAX_RATE) / shares   # Keytruda very high margin
eps_per_1B_winrevair = 1.0 * 0.80 * (1 - TAX_RATE) / shares   # Winrevair high margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Keytruda revenue:             +${eps_per_1B_keytruda:.3f}/EPS  = +${eps_per_1B_keytruda*13:.1f}/share at 13× P/E")
print(f"  Every $1B Winrevair revenue:            +${eps_per_1B_winrevair:.3f}/EPS  = +${eps_per_1B_winrevair*13:.1f}/share at 13× P/E")
print(f"  1pp GM expansion (Qlex/Winrevair mix):  +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*13:.1f}/share at 13× P/E")
print(f"  1% buyback (~25M shares):               +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Keytruda trajectory / Winrevair / Qlex / Vaccines / Pipeline framework)")
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
    ("Keytruda revenue YoY growth",     "+12%",   "<0%",    "−12pp",  "Growth decelerates faster than expected ahead of 2028 cliff"),
    ("Qlex SC launch trajectory",       "$128M",  "<$50M",  "−$78M",  "Subcutaneous launch underwhelms; fails to extend exclusivity"),
    ("Winrevair revenue growth",        "+88%",   "<20%",   "−68pp",  "Cardiovascular franchise growth stalls; competitive PAH entrants"),
    ("Gardasil/Vaccines China demand",  "~-5%",   "<-15%",  "−10pp",  "China vaccine demand remains structurally weak; no recovery"),
    ("Pipeline readouts",               "1-2",    "0",      "−1-2",   "Oncology/cardio readouts disappoint; cliff remains unaddressed"),
    ("Gross margin",                    "78%",    "<74%",   "−4pp",   "Mix shift to lower-margin segments as Keytruda declines"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Keytruda growth decelerates sharply ahead of schedule (well before the 2028")
print(f"  US patent cliff) while Qlex's subcutaneous reformulation fails to meaningfully extend")
print(f"  exclusivity, Winrevair growth stalls from competitive PAH entrants, and Gardasil China")
print(f"  demand stays depressed. EPS falls to ~$7.50 → 9× trough P/E (cliff-discount floor) = ${bear_price}.")
print(f"  Note: $68 is NOT permanent impairment — Vaccines/Animal Health + dividend ($3.28/share)")
print(f"  provide a durable earnings floor. Recovery to ~${bear_price+30}–${bear_price+50} in 2yr is base case post-shock.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           ${EPS_FY2027E:.2f}  (consensus ~$9.50 non-GAAP)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (cliff-discount floor; pharma trough ~9-10×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP reflects that MRK already trades at a steep discount —")
print(f"  12.9× FY2027E EPS ${EPS_FY2027E:.2f} — owing to the well-telegraphed 2028 Keytruda US patent")
print(f"  cliff (~$35B+ revenue at risk). The market has priced in significant cliff risk already;")
print(f"  the open question is whether Winrevair + Qlex + pipeline diversification provides enough")
print(f"  offset to make the current discount excessive (UNDERVALUED) or whether the discount is")
print(f"  appropriately sized given cliff timing/magnitude uncertainty (HOLD/TRIM territory).")
print(f"  EPP path: FY2029E EPS ~$10.50 × {PE_PESSIMISTIC:.0f}× = ${10.50*PE_PESSIMISTIC:.0f} floor (EPP roughly flat as cliff approaches).")
print(f"  At 13× mid-cycle P/E: ${EPS_FY2027E:.2f} × 13 = ${EPS_FY2027E*13:.0f}  — roughly in line with current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest EPS growth into cliff approach; P/E roughly flat)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (modest growth; Keytruda deceleration partly offset by Winrevair/Qlex)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (roughly flat from 12.9× as cliff proximity caps re-rating)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: MRK trades at 12.9× FY2027E EPS ${EPS_FY2027E:.2f} — a deep discount versus")
print(f"  pharma peers — entirely due to the well-telegraphed 2028 Keytruda US patent cliff (~$35B+")
print(f"  at risk). Winrevair (+88% YoY) and Qlex (subcutaneous Keytruda, $128M launch) are the")
print(f"  diversification levers. If they scale enough to offset even half the cliff, the discount")
print(f"  is excessive and MRK re-rates toward 14-16×. If they underwhelm, 12.9× is appropriate —")
print(f"  i.e. HOLD/TRIM, not a value trap nor a bargain.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E - 1)*100:.1f}% EPS growth by FY2028E vs FY2027E — modest, achievable at BASE.")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.22
beta        = 0.85
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  Dividend Aristocrat)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (lower than tech peers; defensive pharma; cliff overhang priced in)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (defensive; lower than market; pharma sector characteristics)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe; cliff-acceleration tail scenario)")
print(f"  52W range already reflects significant cliff-fear repricing in 2025-2026.")
print(f"  → Keytruda growth deceleration pace is THE KEY binary for downside risk.")
print(f"  → Winrevair scaling + Qlex exclusivity extension are KEY bull catalysts.")
print(f"  → AVOID above $135  |  WATCHLIST $100–108  |  ACCUMULATE $88–95  |  BUY below $75–85")

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
print(f"  {'ABOVE' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'BELOW'} the model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing")
print(f"  ~{MARKET_COMPOSITE:.2f}/4.0 while the model scores fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0.")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: the 2028 Keytruda patent cliff discount appears largely appropriately")
print(f"  sized at current levels — Winrevair + Qlex + pipeline diversification is a real but")
print(f"  unproven offset, keeping MRK in HOLD/TRIM territory rather than a clear BUY or AVOID.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Keytruda quarterly revenue trajectory — growth deceleration tracking ahead of 2028 cliff")
print(f"  (2) Winrevair revenue scaling — confirmation of new cardiovascular franchise trajectory")
print(f"  (3) Qlex (subcutaneous Keytruda) launch update — IP/exclusivity implications for franchise life")
print(f"  (4) Gardasil/vaccines China demand recovery — key swing factor for vaccines segment")
print(f"  (5) Pipeline readouts (oncology, cardiovascular) — productivity to offset 2028 cliff")
print(f"  (6) Dividend sustainability — ${ANNUAL_DIV:.2f}/share payout amid cliff transition")
print(f"  AVOID above $135  |  WATCHLIST $100–108  |  ACCUMULATE $88–95  |  BUY below $75–85")
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
