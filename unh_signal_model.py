"""
UNH  ·  UnitedHealth Group Inc.  ·  NYSE: UNH
Bottom-up signal model  ·  UnitedHealthcare (Insurance) / Optum Health / Optum Rx / Optum Insight
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "UNH"
COMPANY       = "UnitedHealth Group Inc."
SECTOR        = "Managed Care · UnitedHealthcare Insurance · Optum Health/Rx/Insight · Medicare Advantage Reset · NYSE: UNH"
CURRENT_PRICE = 285.00      # USD; as of 2026-06-10, post-2025 collapse from ~$600 highs
VOL_52W_LOW   = 234.60      # 2025-2026 DOJ investigation / guidance-suspension trough
VOL_52W_HIGH  = 401.50      # mid-2025 pre-collapse level (still well off 2024 highs ~$600)
SHARES_OUT_M  = 920.0       # millions; buybacks paused during crisis
ANNUAL_DIV    = 8.40        # $/share; maintained through crisis (~2.95% yield) as capital-return signal

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("UnitedHealthcare (Medicare Adv./Comm./Medicaid)", 305.0, 290.0, 325.0, "MA repricing/membership attrition vs disciplined 2026 bid cycle recovery"),
    ("Optum Health (value-based care/clinics)",          115.0, 105.0, 130.0, "Value-based care margins reset post MCR spike; physician group consolidation continues"),
    ("Optum Rx (PBM)",                                     145.0, 138.0, 158.0, "PBM steady growth; reform/transparency pressure on spread pricing economics"),
    ("Optum Insight (data/tech/services)",                  20.0,  18.0,  23.0, "Smaller, stable analytics/tech segment; modest growth"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.155   # blended margin proxy (post-MCO costs); reflects ~89-90% MCR drag
GROSS_MARGIN_BULL = 0.185   # BULL: MCR normalizes toward ~85% as repricing takes hold
OPEX_FIXED_B      = 38.0    # SG&A ($B); largely fixed cost base, some leverage from scale
TAX_RATE          = 0.235   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 18.50      # FY2027E EPS (recovery year; consensus range wide $16-21 given reset)
PE_PESSIMISTIC = 11.0       # trough P/E: DOJ overhang + MCR uncertainty caps multiple near historic lows
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # ~$204

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (12.00, 10,  120, "DOJ criminal case results in adverse findings/penalties; MCR stays >90% through 2027 as repricing fails to offset utilization; membership attrition accelerates; EPS $12.00 → 10× = $120"),
    "BASE":  (18.50, 13,  241, "MA repricing gradually restores margins (MCR trends to ~87-88%); DOJ investigation drags on but no crippling penalty; Optum Rx/Insight provide steady ballast; EPS $18.50 → 13× = $241"),
    "BULL":  (24.00, 16,  384, "2026-2027 MA bid cycle repricing successful, MCR normalizes to ~85%; DOJ matter resolved with manageable settlement; Hemsley-led cost discipline restores investor confidence; EPS $24.00 → 16× = $384"),
    "XBULL": (29.00, 19,  551, "Full earnings power restoration toward pre-2025 trajectory; MCR <84%; DOJ overhang fully lifted; multiple re-rates back toward historical premium as largest US insurer regains growth narrative; EPS $29.00 → 19× = $551"),
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
        "name":       "Medical Care Ratio (MCR) trend",
        "weight":     0.30,
        "thresholds": (">90%",  "≥88%",  "≥86%",   "≤84%"),
        "now":        "~89.5%",
        "score":      1,
        "comment":    "MCR spiked above 90% in 2025 on Medicare Advantage utilization (outpatient, physician services); 2026 repricing aims to bring this back toward high-80s but not yet proven",
    },
    {
        "name":       "DOJ Medicare Advantage risk-adjustment investigation",
        "weight":     0.20,
        "thresholds": ("criminal charges/major penalty", "ongoing/uncertain", "narrowing/civil settlement", "closed, no material findings"),
        "now":        "ongoing/uncertain",
        "score":      1,
        "comment":    "DOJ criminal investigation into MA risk-adjustment coding practices remains a major unresolved overhang with binary tail risk for fines, exclusion, or executive liability",
    },
    {
        "name":       "2026 MA bid repricing / membership stability",
        "weight":     0.20,
        "thresholds": ("attrition>repricing gain", "roughly even", "repricing offsets attrition", "net margin expansion"),
        "now":        "early signs of repricing benefit, membership flat/slightly down",
        "score":      2,
        "comment":    "Aggressive 2026 MA bids aim to restore margins even at cost of membership; early data shows some plans exiting unprofitable counties, partially offset by premium increases",
    },
    {
        "name":       "Optum Rx / Optum Insight stability",
        "weight":     0.15,
        "thresholds": ("declining", "flat", "mid-single-digit growth", "high-single-digit+ growth"),
        "now":        "+6-7%",
        "score":      3,
        "comment":    "PBM and analytics segments continue to grow steadily, providing earnings ballast while UnitedHealthcare/Optum Health work through the reset",
    },
    {
        "name":       "Leadership/cost discipline (Hemsley return)",
        "weight":     0.10,
        "thresholds": ("no clear plan", "plan announced, unproven", "early execution wins", "clear turnaround traction"),
        "now":        "plan announced, early execution",
        "score":      2,
        "comment":    "Stephen Hemsley's return as CEO brings credibility and renewed cost-discipline focus; 2026 guidance reinstated but conservative; turnaround still in early innings",
    },
    {
        "name":       "Balance sheet / capital return capacity",
        "weight":     0.05,
        "thresholds": ("<A-",  "A to A+",  "AA-",   "AA"),
        "now":        "A+",
        "score":      3,
        "comment":    "Still investment-grade with strong free cash flow generation; dividend maintained (~3% yield) through the crisis as a signal of underlying balance sheet resilience",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("-", "DOJ criminal investigation tail risk — unresolved Medicare Advantage risk-adjustment coding probe with binary downside", -0.7, 0.25),
    ("+", "Scale moat — largest US health insurer (~$400B revenue); diversified across UnitedHealthcare/Optum Health/Rx/Insight", +0.5, 0.20),
    ("-", "MCR uncertainty — medical cost trend (Medicare Advantage utilization) repricing lag is unproven at scale through 2026-2027", -0.5, 0.20),
    ("+", "Optum Rx/Insight diversification — non-insurance segments provide earnings stability during UnitedHealthcare reset", +0.4, 0.15),
    ("+", "Leadership credibility — Hemsley's prior tenure track record provides some confidence in turnaround execution", +0.3, 0.10),
    ("-", "Trust/regulatory overhang — reputational damage and heightened political/regulatory scrutiny of MA program broadly", -0.3, 0.10),
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
CONS_EPS_2YR  = 20.50   # FY2028E conservative: gradual MCR normalization, modest growth
CONS_PE_2YR   = 13      # rerates modestly from current depressed levels as DOJ uncertainty persists
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  UnitedHealthcare Insurance / Optum Health/Rx/Insight / MA Reset")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<48}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<48}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<48}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
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
shares_b     = shares * 0.98   # modest buyback resumption over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.92   # MCR stays elevated, margin compresses further
bear_oi      = bear_gp - OPEX_FIXED_B * 1.02           # limited cost flexibility
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% margin − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% margin − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (modest buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 16× = ~${bull_eps_imp*16:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.92:.1f}% margin − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 10× trough P/E (DOJ-discount floor) = ~${bear_eps_imp*10:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1pp_mcr     = curr_total * 0.01 * (1 - TAX_RATE) / shares   # 1pp MCR change ~ 1pp of revenue as margin
eps_per_1B_optumrx  = 1.0 * 0.04 * (1 - TAX_RATE) / shares          # Optum Rx thin-margin PBM
eps_per_1B_uhc      = 1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every 1pp MCR change (medical cost ratio):       ∓${eps_per_1pp_mcr:.2f}/EPS  = ∓${eps_per_1pp_mcr*13:.1f}/share at 13× P/E")
print(f"  Every $1B Optum Rx (PBM) revenue:                +${eps_per_1B_optumrx:.3f}/EPS  = +${eps_per_1B_optumrx*13:.1f}/share at 13× P/E")
print(f"  Every $1B UnitedHealthcare revenue (at blend):   +${eps_per_1B_uhc:.3f}/EPS  = +${eps_per_1B_uhc*13:.1f}/share at 13× P/E")
print(f"  1% buyback resumption (~9.2M shares):            +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (MCR trend / DOJ investigation / MA repricing / Optum diversification framework)")
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
    ("Medical Care Ratio (MCR)",         "~89.5%", ">92%",   "+2.5pp", "Utilization trend reaccelerates faster than 2026 repricing can offset"),
    ("DOJ investigation outcome",        "ongoing","criminal charges/major fine", "adverse ruling", "DOJ brings criminal charges or imposes multi-billion-dollar penalty/exclusion risk"),
    ("MA membership/repricing",          "flat",   "attrition>repricing", "net negative", "Members flee repriced/exited plans faster than premium gains offset"),
    ("Optum Rx/Insight growth",          "+6-7%",  "<2%",    "−5pp",   "PBM reform/transparency rules compress Optum Rx spread economics"),
    ("Leadership turnaround traction",   "early",  "stalled",  "no progress", "Hemsley cost-cutting plan fails to gain traction; further guidance cuts in 2026/2027"),
    ("Balance sheet/credit rating",      "A+",     "downgrade to A-/BBB", "−2 notches", "Rating agencies downgrade on sustained margin pressure + litigation reserves"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: The DOJ criminal investigation into Medicare Advantage risk-adjustment coding")
print(f"  results in formal charges or a multi-billion-dollar settlement/program exclusion risk, while")
print(f"  the MCR fails to retreat from >90% as 2026 bid repricing proves insufficient against ongoing")
print(f"  utilization trend. EPS falls to ~$12.00 → 10× trough P/E (DOJ-discount floor) = ${bear_price}.")
print(f"  Note: $120 is NOT necessarily permanent impairment — UNH remains the largest US health insurer")
print(f"  with ~$400B revenue and Optum Rx/Insight ballast. Recovery to ~${bear_price+50}–${bear_price+90} in 2yr")
print(f"  is plausible if the DOJ matter resolves short of existential and MCR normalizes by 2028.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           ${EPS_FY2027E:.2f}  (recovery-year consensus; wide range $16-21 given reset)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (DOJ-discount floor; historical UNH trough multiples 11-13×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct >= 0 else 'below'} trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% {'premium to' if epp_gap_pct >= 0 else 'discount to'} EPP reflects that UNH trades at roughly")
print(f"  {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a deeply depressed multiple for the largest US health")
print(f"  insurer, reflecting the combined MCR/DOJ overhang. The open question is whether 2026 MA")
print(f"  bid repricing restores margins toward historical norms (MCR <87%) and whether the DOJ")
print(f"  matter resolves without existential consequences. If both resolve favorably, the current")
print(f"  price embeds significant discount to even a modest recovery scenario.")
print(f"  EPP path: FY2029E EPS ~$22.00 × {PE_PESSIMISTIC:.0f}× = ${22.00*PE_PESSIMISTIC:.0f} floor (EPP grows as MCR normalizes).")
print(f"  At 13× mid-cycle P/E: ${EPS_FY2027E:.2f} × 13 = ${EPS_FY2027E*13:.0f}  — implies meaningful upside from current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: gradual MCR normalization; P/E remains depressed near trough)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (modest growth as MCR drifts from ~89.5% toward ~88%)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (roughly flat from ~{CURRENT_PRICE/EPS_FY2027E:.1f}× as DOJ uncertainty caps re-rating)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: UNH trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a historically depressed")
print(f"  multiple for the largest US health insurer — reflecting the MCR spike above 90% and the")
print(f"  unresolved DOJ Medicare Advantage risk-adjustment investigation. Optum Rx/Insight provide")
print(f"  diversification ballast while UnitedHealthcare/Optum Health work through the 2026 MA bid")
print(f"  repricing cycle under Hemsley's renewed cost discipline. If MCR normalizes toward the mid-80s")
print(f"  and the DOJ matter resolves short of existential, the multiple can re-rate toward 13-16×.")
print(f"  If MCR stays elevated and the DOJ probe escalates, current depressed levels persist or worsen.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E - 1)*100:.1f}% EPS growth by FY2028E vs FY2027E.")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.40
beta        = 0.75
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: 52W high itself is far below the ~$600 2024 peak — entire range is post-collapse")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  maintained through crisis as confidence signal)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; binary DOJ/MCR catalysts drive large single-day moves)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (historically defensive, now elevated idiosyncratic risk dominates)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (plausible; DOJ-shock + MCR-failure tail scenario)")
print(f"  52W range already reflects an extraordinary collapse from ~$600 2024 highs to current levels.")
print(f"  → DOJ investigation outcome/timeline is THE KEY binary for both downside and upside.")
print(f"  → MCR trajectory in 2026 quarterly prints is the KEY operational signal to watch.")
print(f"  → AVOID above $340  |  WATCHLIST $290–340  |  ACCUMULATE $250–290  |  BUY below $250")

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
print(f"  In plain terms: the market is pricing in more confidence in a 2026-2027 MCR normalization")
print(f"  and DOJ resolution than the bottom-up fundamentals currently support — fundamentals (Optum")
print(f"  diversification, scale moat, dividend maintenance, leadership credibility) currently score")
print(f"  closer to BASE/BEAR than the market's implied BULL-leaning ~{MARKET_COMPOSITE:.2f}/4.0. The DOJ binary")
print(f"  remains a genuine tail risk that could invalidate any recovery thesis entirely.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) DOJ Medicare Advantage risk-adjustment investigation — charges, settlement, or resolution timeline")
print(f"  (2) Medical Care Ratio (MCR) quarterly trend — repricing benefit vs utilization trend")
print(f"  (3) 2026/2027 MA bid cycle outcomes — membership retention vs margin restoration tradeoff")
print(f"  (4) Hemsley-led cost discipline — SG&A leverage and capital allocation signals (buyback resumption)")
print(f"  (5) Optum Rx PBM reform — transparency/spread-pricing legislation impact on segment economics")
print(f"  (6) Dividend sustainability — ${ANNUAL_DIV:.2f}/share maintained through crisis as confidence signal")
print(f"  AVOID above $340  |  WATCHLIST $290–340  |  ACCUMULATE $250–290  |  BUY below $250")
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
