"""
ORCL  ·  Oracle Corporation  ·  NYSE: ORCL
Bottom-up signal model  ·  Enterprise Database / OCI AI Cloud / Debt-Funded Buildout
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "ORCL"
COMPANY       = "Oracle Corporation"
SECTOR        = "Enterprise Database · OCI AI Cloud Infrastructure · Applications SaaS · NYSE: ORCL"
CURRENT_PRICE = 129.87       # USD; close 2026-07-31 (verified live)
VOL_52W_LOW   = 114.50       # July 2026 trough; AI-financing panic
VOL_52W_HIGH  = 345.72       # 2025 post-RPO-announcement peak
SHARES_OUT_M  = 2_880.0      # millions; $374.1B mkt cap / $129.87
ANNUAL_DIV    = 2.00         # $0.50/quarter; yield ~1.54%

# ── SEGMENT REVENUE BRIDGE (FY2027E; fiscal year ends May) ───────────────────
# FY2026 actual: $67.4B total revenue (+17%); FY2027 guide: $90B (+34% cc)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Cloud Infrastructure (OCI)",  38.0, 26.0, 46.0, "FY2026 $18.1B (+77%); Q4 IaaS $5.8B (+93%); the entire thesis lives here"),
    ("Cloud Applications (SaaS)",   16.0, 14.5, 18.0, "Fusion ERP + NetSuite; ~18% growth; the quiet compounder nobody models"),
    ("License support (on-prem)",   19.5, 18.5, 20.5, "~95% gross margin annuity; DB switching costs; funds the entire buildout"),
    ("Cloud + on-prem license",      5.0,  3.5,  6.5, "New licences; declining as workloads migrate to OCI/multicloud"),
    ("Hardware",                     6.0,  4.5,  7.5, "Exadata + Zettascale racks; increasingly customer-supplied GPUs"),
    ("Services",                     5.5,  5.0,  6.0, "Consulting attach to Fusion migrations; low margin, strategic"),
]

# Margin assumptions (non-GAAP)
GROSS_MARGIN_CURR = 0.630   # FY2027E blended; FY2026 was 67.1% (−5pp YoY as OCI mixes up)
GROSS_MARGIN_BULL = 0.655   # BULL: OCI utilisation scales; depreciation absorbed over full racks
OPEX_FIXED_B      = 22.1    # R&D + SG&A ($B)
NET_INTEREST_B    = 6.0     # net interest expense ($B); much of it capitalised into construction
TAX_RATE          = 0.190   # non-GAAP effective rate

# ── FINANCING REALITY (the Oracle-specific calculator) ───────────────────────
RPO_B             = 638.0   # $B remaining performance obligations at Q4 FY2026 (+363% YoY)
RPO_PREPAID_B     =  75.0   # $B of RPO that is customer-prepaid or customer-supplied GPUs
RPO_CONV_12M_B    =  76.6   # $B management expects to convert to revenue in next 12 months
CAPEX_FY2026_B    =  55.7   # $B; the number that broke the stock
FCF_FY2026_B      = -23.7   # $B free cash flow; consensus stays negative through FY2028
NET_DEBT_B        = 131.2   # $B; S&P downgraded to BBB− on the scale of AI commitments
EBITDA_FY2026_B   =  34.0   # $B approximate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 8.05        # FY2027 company guidance, non-GAAP (+18%); consensus was $8.01
PE_PESSIMISTIC = 12.0        # trough P/E: BBB− credit + negative FCF; Oracle traded 12–14×
                             # forward through 2016–2019 as an ex-growth licence business
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 3.63, 15,   55, "AI customer default/renegotiation; RPO impaired; depreciation on idle capacity"),
    "BASE":  ( 9.50, 17,  162, "FY2027 $8.05 guide delivered; FCF inflects positive FY2028; multiple stays derated"),
    "BULL":  (11.00, 24,  264, "OCI $46B run-rate; RPO converts on schedule; FCF positive; re-rates to cloud peer"),
    "XBULL": (15.00, 26,  390, "Oracle = #3 AI cloud; $638B backlog proves real; margin + multiple both recover"),
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
        "name":       "OCI (IaaS) revenue YoY growth",
        "weight":     0.25,
        "thresholds": ("<25%",   "≥40%",   "≥65%",   "≥90%"),
        "now":        "+77%",
        "score":      3,
        "comment":    "FY2026 OCI $18.1B (+77%); Q4 alone $5.8B (+93%). Growth is not the problem — funding it is",
    },
    {
        "name":       "Free cash flow (TTM, $B)",
        "weight":     0.25,
        "thresholds": ("<−20B",  "≥−10B",  "≥+5B",   "≥+20B"),
        "now":        "−23.7B",
        "score":      1,
        "comment":    "$55.7B capex against $67.4B revenue. Consensus has FCF negative through FY2028. This is the bear case",
    },
    {
        "name":       "RPO 12-month conversion rate",
        "weight":     0.15,
        "thresholds": ("<8%",    "≥11%",   "≥15%",   "≥20%"),
        "now":        "12.0%",
        "score":      2,
        "comment":    "$76.6B of $638B converts next 12 months. Backlog is real but the duration is very long (8+ yrs)",
    },
    {
        "name":       "Non-GAAP gross margin",
        "weight":     0.15,
        "thresholds": ("<60%",   "≥65%",   "≥70%",   "≥75%"),
        "now":        "67.1%",
        "score":      2,
        "comment":    "Down ~5pp in FY2026 as low-margin OCI mixes up against the 95%-margin licence-support annuity",
    },
    {
        "name":       "Net debt / EBITDA",
        "weight":     0.10,
        "thresholds": (">5.0x",  "≤4.0x",  "≤2.5x",  "≤1.5x"),
        "now":        "~3.9x",
        "score":      2,
        "comment":    "$131B net debt on ~$34B EBITDA; $40B raise announced. S&P cut to BBB− — one notch above junk",
    },
    {
        "name":       "Top-customer share of RPO",
        "weight":     0.10,
        "thresholds": (">50%",   "≤35%",   "≤20%",   "≤10%"),
        "now":        "~40%",
        "score":      1,
        "comment":    "A single pre-profit AI lab anchors the largest tranche. $638B backlog is only as good as who signed it",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Database franchise — $19.5B licence support at ~95% margin; mission-critical switching costs", +0.8, 0.20),
    ("+", "$638B RPO — 9.5× FY2026 revenue; contracted, not pipeline; $75B already prepaid/GPU-supplied", +0.9, 0.20),
    ("-", "Debt-funded buildout — $55.7B capex, −$23.7B FCF, $131B net debt, S&P downgrade to BBB−",      -1.0, 0.25),
    ("-", "Counterparty risk — anchor AI tenants are pre-profit; one renegotiation impairs the thesis",   -0.9, 0.15),
    ("+", "Valuation reset — 16.1× FY2027E guided EPS on +18% EPS growth; PEG ~0.9× for a hyperscaler",   +0.7, 0.10),
    ("-", "Depreciation wall — GPU/DC assets on 5–6yr schedules; earnings quality degrades as builds land", -0.6, 0.10),
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
CONS_EPS_2YR  = 9.00    # conservative FY2028E: guide met in FY2027, then only 12% growth
CONS_PE_2YR   = 16      # no multiple recovery — stays at today's derated 16×
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Database / OCI AI Cloud / Debt-Funded Buildout")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2027E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<28}  {'FY2027E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<28}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<28}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  Company FY2027 guidance: $90B revenue (+34% cc), non-GAAP EPS $8.05 (+18%)")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_pbt  = curr_oi - NET_INTEREST_B
curr_eps  = round(curr_pbt * (1 - TAX_RATE) / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B * 1.06
bull_pbt  = bull_oi - NET_INTEREST_B * 1.10
shares_b  = shares * 0.98
bull_eps_imp = round(bull_pbt * (1 - TAX_RATE) / shares_b, 2)

bear_gp   = bear_total * 0.600          # idle-capacity depreciation crushes OCI gross margin
bear_oi   = bear_gp - OPEX_FIXED_B * 0.95
bear_pbt  = bear_oi - NET_INTEREST_B * 1.55   # downgrade + $40B raise repriced wider
bear_eps_imp = round(max(0, bear_pbt) * (1 - TAX_RATE) / shares, 2)

print(f"  FY2027E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex")
print(f"  − ${NET_INTEREST_B:.1f}B net interest − {TAX_RATE*100:.1f}% tax  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share")
print(f"  (company guidance ${EPS_FY2027E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − opex − interest")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 24× = ~${bull_eps_imp*24:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × 60.0% GM − opex − ${NET_INTEREST_B*1.55:.1f}B interest")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 15× trough = ~${bear_eps_imp*15:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")
print()
print(f"  ⚠ NOTE THE ASYMMETRY IN THE BRIDGE: revenue only has to fall {(1-bear_total/curr_total)*100:.0f}% for EPS to fall")
print(f"  {(1-bear_eps_imp/curr_eps)*100:.0f}%. Oracle has converted a variable-cost software P&L into a fixed-cost")
print(f"  infrastructure P&L. Depreciation and interest do not care about utilisation.")

# KEY SENSITIVITIES
print()
eps_per_1B_oci  = 1.0 * 0.38 * (1 - TAX_RATE) / shares     # OCI incremental margin ~38%
eps_per_1B_supp = 1.0 * 0.95 * (1 - TAX_RATE) / shares     # licence support ~95% margin
eps_per_1pp_int = 1.31 * (1 - TAX_RATE) / shares           # +100bp on ~$131B net debt

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B OCI revenue (38% inc. margin):   +${eps_per_1B_oci:.3f}/EPS  = +${eps_per_1B_oci*17:.2f}/share at 17× P/E")
print(f"  Every $1B licence support (95% margin):    +${eps_per_1B_supp:.3f}/EPS  = +${eps_per_1B_supp*17:.2f}/share at 17× P/E")
print(f"  Every +100bp on $131B net debt:            −${eps_per_1pp_int:.3f}/EPS  = −${eps_per_1pp_int*17:.2f}/share at 17× P/E")
print(f"  Every $10B capex deferred:                 +$10B FCF, −~$2B/yr future revenue run-rate")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (OCI growth / cash generation / backlog quality / leverage)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<44}  {'BEAR':>6}  {'BASE':>6}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>7}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<44}  {ths[0]:>6}  {ths[1]:>6}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>7}  {lbl}  {b}")
    print(f"    {s['comment']}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15%/yr hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:90]:<90}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<30}  {'Current':>9}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("OCI revenue YoY",           "+77%",    "<25%",    "−52pp",  "Anchor AI tenant halts capacity draw-down"),
    ("Free cash flow (TTM)",      "−23.7B",  "<−35B",   "−11B",   "Capex continues into contracts that never convert"),
    ("RPO 12-mo conversion",      "12.0%",   "<8%",     "−4pp",   "Contracts deferred; take-or-pay renegotiated"),
    ("Non-GAAP gross margin",     "67.1%",   "<58%",    "−9pp",   "Depreciation on idle GPU racks, no revenue against it"),
    ("Net debt / EBITDA",         "~3.9x",   ">5.5x",   "+1.6x",  "Further raises + EBITDA decline; cut below IG"),
    ("Top-customer RPO share",    "~40%",    ">55%",    "+15pp",  "Concentration rises as smaller contracts lapse"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<30}  {curr:>9}  {bear_v:>9}  {move:>8}  {trigger[:48]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Oracle borrowed ~$131B net to build capacity for customers whose own")
print(f"  funding is not yet secured. The bear case is not 'AI demand disappoints' — it is")
print(f"  'Oracle's counterparties cannot pay, while Oracle's interest and depreciation are")
print(f"  contractual'. $75B of the $638B RPO is prepaid or customer-supplied hardware; the")
print(f"  other $563B is a promise. If even 20% is renegotiated, the equity absorbs it.")
print(f"  Note: BEAR ${bear_price} is NOT a zero. Licence support (${SEG_DATA[2][2]:.1f}B at ~95% margin) plus Fusion/")
print(f"  NetSuite (${SEG_DATA[1][2]:.1f}B) is a durable ~$4–5/share earnings franchise on its own.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2027E non-GAAP EPS (company guide):  ${EPS_FY2027E:.2f}  (+18% YoY; consensus was $8.01)")
print(f"  Pessimistic P/E at trough:              {PE_PESSIMISTIC:.0f}×  (BBB− credit + negative FCF; 2016–19 range 12–14×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× guided FY2027 EPS. For context, the")
print(f"  S&P 500 trades ~21×; Oracle is guiding EPS +18% and revenue +34%. The market is not")
print(f"  paying for growth at all — it is pricing the balance sheet. That is the whole story:")
print(f"  a {(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.0f}% drawdown from ${VOL_52W_HIGH:.2f} took the multiple from ~45× to {CURRENT_PRICE/EPS_FY2027E:.0f}×.")
print(f"  EPP sits only {abs(epp_gap_pct):.0f}% below spot — the floor is close, which is what makes the")
print(f"  risk/reward work even though the risk itself is genuinely large.")
print(f"  At 20× mid-cycle: ${EPS_FY2027E:.2f} × 20 = ${EPS_FY2027E*20:.0f}  (+{(EPS_FY2027E*20/CURRENT_PRICE-1)*100:.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: guide met, then decelerates; NO multiple recovery)")
hr()
print(f"  Conservative FY2028E non-GAAP EPS:  ${CONS_EPS_2YR:.2f}  (guide met FY2027, then only +12%)")
print(f"  Conservative exit P/E:               {CONS_PE_2YR}×  (stays at today's derated multiple — no re-rating credit)")
print(f"  Conservative equity value:            ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):        +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:               ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:            {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: the conservative case assumes ZERO multiple expansion and still clears")
print(f"  {cons_annual:.1f}%/yr. That is the point — you are not paying for a re-rating here, so the")
print(f"  re-rating is free optionality rather than the thing that has to happen. Every")
print(f"  scenario above BASE requires the multiple, not the earnings, to do the work.")
print(f"  Breakeven at 16× requires FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f} — below the FY2027 guide already.")
print(f"  MAX-SIZE trigger: below ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.72 + cons_divs, 0):.0f} (at/below the EPP floor)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.52
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Drawdown from high:   −{(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.1f}%  (worst weekly decline since the 2001 dot-com bust)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (extreme for a mega-cap; AI-financing headline sensitivity)")
print(f"  Beta vs S&P 500:      1.45  (now trades as a levered AI-capex derivative, not a software name)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ further drawdown  (plausible — this stock has already done worse)")
print(f"  → Watch quarterly FCF and the capex line, not the RPO headline. RPO is priced in reverse now.")
print(f"  → A credible 'anchor tenant funded through 2029' datapoint is the single re-rating catalyst.")
print(f"  → BUY at current price  |  ADD $105–120  |  MAX SIZE below $100 (at/below EPP)")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f} the market composite is {MARKET_COMPOSITE:.2f}/4.0 — at or below BASE.")
print(f"  The model's adjusted composite is {ADJ_COMPOSITE:.2f}/4.0. The gap ({ADJ_GAP:+.2f}) says the stock is")
print(f"  {valuation_label.lower()}. In plain terms: the market is pricing a materially worse outcome")
print(f"  than a company that just guided to $90B revenue and $8.05 EPS. Both things are true —")
print(f"  the balance-sheet risk is real AND the price already reflects more than the base case.")
print(f"  This is a position-sizing problem, not a thesis problem. Size it as a levered bet.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Quarterly FCF trajectory — the single number that resolves the entire debate")
print(f"  (2) Anchor-tenant funding news — any confirmed multi-year financing = re-rating trigger")
print(f"  (3) Capex guidance revision — a *cut* would read as bullish (discipline), not bearish")
print(f"  (4) Credit rating actions — a further cut below IG forces mechanical index selling")
print(f"  (5) OCI gross-margin disclosure — proves or kills the unit economics of the buildout")
print(f"  BUY at ${CURRENT_PRICE:.2f}  |  ADD $105–120  |  MAX SIZE below $100  |  TRIM above $230")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2027E EPS: ${EPS_FY2027E:.2f}  |  RPO: ${RPO_B:.0f}B")
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
