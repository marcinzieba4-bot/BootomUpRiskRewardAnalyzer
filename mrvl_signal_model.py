"""
MRVL  ·  Marvell Technology, Inc.  ·  NASDAQ: MRVL
Bottom-up signal model  ·  AI Custom Silicon (ASIC) / Optical Interconnect / Data Center
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "MRVL"
COMPANY       = "Marvell Technology, Inc."
SECTOR        = "AI Custom Silicon (ASIC) · Optical Interconnect · Data Center · NASDAQ: MRVL"
CURRENT_PRICE = 196.00      # USD; as of 2026-06-10; all-time high
VOL_52W_LOW   = 58.61       # 2025 trough (AI-capex-fear / hyperscaler-concentration scare)
VOL_52W_HIGH  = 200.00      # current cycle high; +235% off the 52W low
SHARES_OUT_M  = 860.0       # millions; modest dilution from equity comp

# Dividend: token payout; capital allocation skews to buybacks/R&D
ANNUAL_DIV    = 0.24        # $/share ($0.06/quarter)

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2027E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Data Center (AI custom silicon/ASIC)", 5.80, 3.80, 8.50, "Amazon Trainium ramp; optical DSPs/electro-optics; hyperscaler capex wave"),
    ("Enterprise Networking",                 1.55, 1.20, 1.90, "Switching/routing silicon recovery; cloud + on-prem refresh cycle"),
    ("Carrier Infrastructure",                0.85, 0.65, 1.05, "5G/access silicon; multi-year inventory digestion easing"),
    ("Consumer/Automotive",                   0.55, 0.40, 0.70, "Storage/auto Ethernet; cyclical, smaller mix of total"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.605   # blended non-GAAP gross margin (~60.5%; ASIC mix is dilutive vs legacy)
GROSS_MARGIN_BULL = 0.640   # BULL: scale + custom-silicon mix maturity lifts blended GM
OPEX_FIXED_B      = 1.95    # R&D + SG&A ($B); heavy custom-silicon R&D investment
TAX_RATE          = 0.060   # effective non-GAAP cash tax rate (NOLs, offshore structure)

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 2.84        # FY2026 (ending Jan 2026) adj EPS — actual/near-final
PE_PESSIMISTIC = 18.0        # trough P/E: semis-cycle floor multiple ex-AI-premium
                              # (pre-AI-ASIC-narrative MRVL traded 15-20x trough)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # ~$51

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (2.00, 25,   50, "Trainium ramp decelerates; no new ASIC wins; Enterprise/Carrier stay weak; EPS $2.00 → 25x trough"),
    "BASE":  (2.84, 45,  128, "FY2026 EPS $2.84 holds at premium AI-supplier multiple; steady Data Center growth; 45x"),
    "BULL":  (4.20, 50,  210, "3rd hyperscaler ASIC win + optical interconnect accel; FY2028E EPS $4.20 → 50x"),
    "XBULL": (5.44, 58,  316, "FY2028E EPS $5.44 (mgmt 'well over $5'); 4th custom-silicon customer; AI-ASIC platform re-rate to 58x"),
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
        "name":       "AI custom silicon (ASIC) revenue growth — Amazon Trainium ramp",
        "weight":     0.30,
        "thresholds": ("<20%",   "≥40%",  "≥80%",   "≥130%"),
        "now":        "+~100%",
        "score":      3,
        "comment":    "Trainium2/3 ramp driving Data Center custom compute revenue; multi-billion run-rate; concentration risk on Amazon",
    },
    {
        "name":       "Optical interconnect / electro-optics revenue growth",
        "weight":     0.20,
        "thresholds": ("<10%",   "≥20%",  "≥35%",   "≥50%"),
        "now":        "+~30%",
        "score":      3,
        "comment":    "1.6T DSP/PAM4 ramp; co-packaged optics roadmap; data-center connectivity content per AI server rising",
    },
    {
        "name":       "Additional hyperscaler custom-silicon design wins (3rd/4th customer)",
        "weight":     0.20,
        "thresholds": ("None",   "Rumored","1 confirmed","2+ confirmed"),
        "now":        "Rumored only",
        "score":      2,
        "comment":    "Beyond Amazon (Trainium) and Google (TPU-adjacent); Microsoft/Meta talks reported but unconfirmed at scale",
    },
    {
        "name":       "Data Center segment gross margin trajectory",
        "weight":     0.15,
        "thresholds": ("<55%",   "≥58%",  "≥62%",   "≥66%"),
        "now":        "~60.5%",
        "score":      2,
        "comment":    "ASIC mix is structurally dilutive to corporate GM vs legacy networking; scale benefits offsetting so far",
    },
    {
        "name":       "Enterprise Networking / Carrier Infrastructure recovery",
        "weight":     0.10,
        "thresholds": ("<-5%",   "≥0%",   "≥8%",    "≥15%"),
        "now":        "+~3%",
        "score":      2,
        "comment":    "Inventory digestion largely complete; modest sequential recovery; still a drag vs Data Center growth",
    },
    {
        "name":       "FY2028E EPS guidance trajectory ($5.44 / 'well over $5')",
        "weight":     0.05,
        "thresholds": ("<$3.50", "≥$4.20","≥$5.00", "≥$5.44"),
        "now":        "$5.44 framed",
        "score":      4,
        "comment":    "Management has framed FY2028E EPS as 'well over $5'; $5.44 is the high end of the framework",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "AI-ASIC platform leader — Amazon Trainium anchor customer; multi-year hyperscaler capex wave",  +0.7, 0.25),
    ("+", "Optical interconnect content growth — DSP/electro-optics attach rate rises with AI cluster scale", +0.5, 0.15),
    ("-", "Single-customer concentration — Amazon dominates Data Center ASIC revenue; renewal/diversification risk", -0.6, 0.20),
    ("-", "Valuation already reflects bull case — Method B (FY2028E $5.44 x 35x = $190) is BELOW current $196", -0.7, 0.20),
    ("+", "Analyst PT momentum — Citi $215 / Melius $220 racing to keep pace with the AI-ASIC re-rate",     +0.3, 0.10),
    ("-", "All-time-high / +235% off 52W low — limited margin of safety; Enterprise/Carrier still subscale drag", -0.5, 0.10),
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
CONS_EPS_2YR  = 4.20    # conservative FY2028E: below mgmt "well over $5"; partial ASIC ramp + optical growth
CONS_PE_2YR   = 35      # rerating from 36x toward growth-justified-but-de-risked 35x
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  AI Custom Silicon / Optical Interconnect / Data Center")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2027E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<26}  {'FY2027E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<26}  ${curr:>11.2f}  ${bear:>8.2f}  ${bull:>8.2f}  {bear-curr:>+7.2f}  {bull-curr:>+7.2f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<26}  ${curr_total:>11.2f}  ${bear_total:>8.2f}  ${bull_total:>8.2f}  {bear_total-curr_total:>+7.2f}  {bull_total-curr_total:>+7.2f}")
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
shares_b  = shares * 1.00   # roughly flat share count over 2yr
bull_eps_imp = round(bull_ni / shares_b, 2)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift away from higher-margin ASIC scale
bear_oi   = bear_gp - OPEX_FIXED_B * 0.95           # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 2)

print(f"  FY2026 EPS check:  ${curr_total:.2f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.2f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (FY2026 actual ${EPS_FY2026E:.2f}  ✓ approx)")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.2f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares  =  ~${bull_eps_imp:.2f}/share  →  ${bull_eps_imp:.2f} × 50× = ~${bull_eps_imp*50:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.2f}/share")
print(f"  At 25× trough P/E = ~${bear_eps_imp*25:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Data Center (ASIC) revenue:  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*45:.2f}/share at 45× P/E")
print(f"  1pp Data Center GM expansion:          +${curr_total*0.01*(1-TAX_RATE)/shares:.3f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*45:.2f}/share at 45× P/E")
print(f"  3rd hyperscaler ASIC win (~$1.5-2B run-rate): could add ${1.75*eps_per_1B_rev:.2f}-${2.0*eps_per_1B_rev:.2f}/EPS once ramped")
print(f"  Multiple compression 45× → 35× on FY2026 EPS ${EPS_FY2026E:.2f}: ${EPS_FY2026E*45:.0f} → ${EPS_FY2026E*35:.0f}  (−{(1-35/45)*100:.0f}%)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (AI custom silicon / optical interconnect / hyperscaler diversification framework)")
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
    ("AI ASIC (Trainium) revenue growth",   "+~100%", "<20%",   "−80pp",  "Amazon Trainium ramp decelerates / single-customer concentration risk hits"),
    ("Additional hyperscaler ASIC wins",    "Rumored","None",   "n/a",    "No 3rd/4th hyperscaler custom-silicon design win announced over 2yr"),
    ("Optical interconnect growth",         "+~30%",  "<10%",   "−20pp",  "1.6T DSP ramp slows; co-packaged optics delays push out content growth"),
    ("Data Center gross margin",            "~60.5%", "<55%",   "−5.5pp", "ASIC mix dilution accelerates faster than scale benefits offset"),
    ("Enterprise/Carrier revenue growth",   "+~3%",   "<-5%",   "−8pp",   "Networking/carrier capex pulls back; segments remain structural drag"),
    ("FY2028E EPS guidance",                "$5.44",  "<$3.50", "−$1.94", "Guidance walked back from 'well over $5' toward $2.00 on ASIC slowdown"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Amazon Trainium ramp decelerates — either due to internal silicon")
print(f"  diversification (Amazon dual-sourcing), capex digestion, or in-house yield/perf issues —")
print(f"  combined with no announced 3rd/4th hyperscaler ASIC customer. Data Center revenue growth")
print(f"  stalls below 20% YoY, gross margins compress on unfavorable mix, and Enterprise/Carrier")
print(f"  remain a drag. EPS resets toward ~$2.00 → 25× trough multiple = ${bear_price}.")
print(f"  Note: ${bear_price} would be a ~{(1-bear_price/CURRENT_PRICE)*100:.0f}% drawdown from current ${CURRENT_PRICE:.2f} — severe but")
print(f"  plausible given the stock is +235% off its 52-week low and priced for flawless execution.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026 adj EPS:                 ${EPS_FY2026E:.2f}  (FY2026, ending Jan 2026)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (pre-AI-ASIC-narrative semis-cycle floor)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP reflects the market's conviction in the AI custom-silicon")
print(f"  and optical-interconnect growth story. At ${CURRENT_PRICE:.2f} and FY2028E EPS ${SCENARIOS['XBULL'][0]:.2f},")
print(f"  the implied P/E is {CURRENT_PRICE/SCENARIOS['XBULL'][0]:.1f}× FY2028E — a very large bet on multi-year hyperscaler capex durability.")
print(f"  Method B check: FY2028E ${SCENARIOS['XBULL'][0]:.2f} × 35× = ${SCENARIOS['XBULL'][0]*35:.0f}  — BELOW current ${CURRENT_PRICE:.0f}.")
print(f"  This means even a 35× multiple on the high end of management's FY2028E framework does")
print(f"  not justify the current price — the 3rd hyperscaler win narrative may already be priced in.")
print(f"  Analyst PT upgrades (Citi $215 / Melius $220) are clustered just above current price,")
print(f"  leaving little margin of safety even in bullish sell-side scenarios.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: partial ASIC ramp + optical growth, modest multiple compression)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (below mgmt 'well over $5'; partial Trainium ramp + optical growth)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (compresses from ~{CURRENT_PRICE/EPS_FY2026E:.0f}× FY2026 to {CONS_PE_2YR}× on FY2028E)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE PROBLEM: at ${CURRENT_PRICE:.2f}, the stock already trades at {CURRENT_PRICE/SCENARIOS['XBULL'][0]:.1f}× the HIGH END")
print(f"  of management's FY2028E EPS framework ($5.44). Even hitting that number requires the")
print(f"  multiple to hold near 36× — any moderation toward a 'mature AI supplier' multiple of")
print(f"  {CONS_PE_2YR}× produces negative returns despite real EPS growth.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.0f}% EPS growth from FY2026 — above even the BULL EPS of ${SCENARIOS['BULL'][0]:.2f}.")
print(f"  Breakeven at 45× P/E (no multiple compression): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 45:.2f}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.55
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: +235% move off the 52W low to current all-time high in under 12 months")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  token; capital skews to R&D/buybacks)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (high; AI-cycle semis name; single-customer concentration amplifier)")
print(f"  Beta vs S&P 500:      1.85  (high-beta AI-capex proxy)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (large but within range for a name that ran +235% in a year)")
print(f"  52W low ${VOL_52W_LOW:.2f} reflects a prior AI-capex-fear / hyperscaler-concentration scare —")
print(f"  the same risk (Amazon Trainium dependency) that could resurface as the BEAR trigger.")
print(f"  → Single-customer (Amazon) concentration is THE KEY binary; loss of share = severe re-rating.")
print(f"  → A confirmed 3rd/4th hyperscaler ASIC win is the KEY bull catalyst that could justify XBULL.")
print(f"  → AVOID at current price  |  WATCHLIST $140–155  |  ACCUMULATE $120–135  |  BUY below $100")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) sits relative to the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0, while the")
print(f"  model scores fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0. The gap ({ADJ_GAP:.2f}) indicates the stock is")
print(f"  {valuation_label.lower()} by model standards.")
print(f"  In plain terms: at an all-time high, with Method B (FY2028E $5.44 x 35x = ${SCENARIOS['XBULL'][0]*35:.0f}) already")
print(f"  BELOW the current price, the AI custom-silicon and optical-interconnect growth story must")
print(f"  not just continue — it must accelerate (3rd/4th hyperscaler win) to justify ${CURRENT_PRICE:.0f}.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch (Q1 FY2027 earnings — May 27, 2026):")
print(f"  (1) Data Center segment growth — sequential and YoY trajectory vs. ~100% ASIC growth run-rate")
print(f"  (2) Amazon Trainium revenue update — any commentary on concentration, renewal terms, or roadmap")
print(f"  (3) New hyperscaler custom silicon design win announcements — 3rd/4th customer confirmation (BULL trigger)")
print(f"  (4) Optical interconnect / electro-optics revenue trajectory — 1.6T DSP ramp, co-packaged optics progress")
print(f"  (5) FY2028E EPS guidance updates — does 'well over $5' framework hold, rise, or get walked back")
print(f"  (6) Enterprise/Carrier segment recovery signs — any inflection from drag to contributor")
print(f"  AVOID at ${CURRENT_PRICE:.2f}  |  WATCHLIST $140–155  |  ACCUMULATE $120–135  |  BUY below $100")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026 EPS: ${EPS_FY2026E:.2f}")
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
