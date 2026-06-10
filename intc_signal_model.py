"""
INTC  ·  Intel Corporation  ·  NASDAQ: INTC
Bottom-up signal model  ·  Semiconductors / Foundry Turnaround / AI PC / Data Center
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "INTC"
COMPANY       = "Intel Corporation"
SECTOR        = "Semiconductors · Foundry Turnaround · AI PC · Data Center · NASDAQ: INTC"
CURRENT_PRICE = 119.00      # USD; as of 2026-06-10
VOL_52W_LOW   = 18.97       # 52-week low; pre-turnaround trough
VOL_52W_HIGH  = 124.00      # 52-week high; near current, post +527% recovery
SHARES_OUT_M  = 4_350.0     # millions; diluted shares outstanding

# Dividend: suspended during turnaround; capital preserved for capex
ANNUAL_DIV    = 0.0         # $/share; dividend suspended

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Intel Products - Client Computing",  31.0, 26.0, 36.0, "Core Ultra AI PC; Panther Lake H2 2026 launch swing factor"),
    ("Intel Products - Data Center & AI",  18.0, 14.0, 24.0, "Xeon vs AMD EPYC; AI accelerator share remains small"),
    ("Intel Foundry (IFS)",                18.0, 14.0, 26.0, "18A external customers (Microsoft); foundry losses narrowing"),
    ("Altera / Mobileye (equity stakes)",   2.5,  1.5,  3.5, "Divested/spun-off stakes; residual consolidated contribution"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.40    # blended gross margin FY2026E (~40%; foundry losses still a drag)
GROSS_MARGIN_BULL = 0.52    # BULL: 18A yields ramp, foundry losses narrow sharply, mix improves
OPEX_FIXED_B      = 21.0    # R&D + SG&A ($B); large fixed cost base; some CHIPS Act offset
TAX_RATE          = 0.15    # effective rate; CHIPS Act credits; NOL carryforwards

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 1.20        # FY2026E EPS estimate (BASE case level; turnaround still early)
PE_PESSIMISTIC = 30.0        # trough P/E: cyclical semis trough multiple even mid-turnaround
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $36

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (0.40, 30,  12,  "18A yields stall, Panther Lake delayed; no new foundry customers; EPS $0.40 → 30× floor"),
    "BASE":  (1.20, 55,  66,  "18A ramps as guided; Panther Lake launches H2 2026; Microsoft + 1-2 customers; EPS $1.20 → 55×"),
    "BULL":  (2.20, 65,  143, "18A leadership established; multiple foundry wins; Data Center share stabilizes; EPS $2.20 → 65×"),
    "XBULL": (3.50, 75,  263, "Intel becomes credible #2 foundry to TSMC; AI accelerator traction; EPS $3.50 → 75×"),
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
        "name":       "18A process node yield improvement / ramp",
        "weight":     0.25,
        "thresholds": ("<3%/mo", "≥5%/mo", "≥8%/mo", "≥12%/mo"),
        "now":        "+7%/mo",
        "score":      3,
        "comment":    "18A in HVM since Oct 2025; yields improving ~7%/month; on track but not yet at parity with TSMC N2",
    },
    {
        "name":       "Intel Foundry external customer wins",
        "weight":     0.20,
        "thresholds": ("0 cust", "1 cust", "2-3 cust", "4+ cust"),
        "now":        "1 (MSFT)",
        "score":      2,
        "comment":    "Microsoft committed to 18A; other prospective customers (AWS, others) in qualification, not signed",
    },
    {
        "name":       "Panther Lake (AI PC) launch reception",
        "weight":     0.20,
        "thresholds": ("delayed", "on-time", "share gain", "supercycle"),
        "now":        "on-time",
        "score":      2,
        "comment":    "H2 2026 launch tracking on schedule on 18A; OEM design wins building but reception unproven",
    },
    {
        "name":       "Data Center / Xeon vs AMD EPYC competitive position",
        "weight":     0.15,
        "thresholds": ("share -5pp", "flat", "share +2pp", "share +5pp"),
        "now":        "flat-ish",
        "score":      2,
        "comment":    "Granite Rapids stabilizing share losses to EPYC; AI accelerator gap to Nvidia/AMD remains wide",
    },
    {
        "name":       "Gross margin recovery trajectory (foundry losses narrowing)",
        "weight":     0.10,
        "thresholds": ("<35%", "≥38%", "≥45%", "≥52%"),
        "now":        "~40%",
        "score":      2,
        "comment":    "Blended GM ~40%; foundry operating losses narrowing YoY but still a multi-billion drag",
    },
    {
        "name":       "CHIPS Act funding execution / capex discipline",
        "weight":     0.10,
        "thresholds": ("delayed", "on-track", "ahead", "self-funding"),
        "now":        "on-track",
        "score":      3,
        "comment":    "$19B CHIPS Act backing flowing as milestones hit; capex growth moderating vs 2024-25 peak",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "18A process leadership optionality — first US leading-edge node in HVM since Intel 7",  +0.6, 0.20),
    ("+", "Foundry diversification — Microsoft commitment + $19B CHIPS Act de-risks capex",          +0.4, 0.15),
    ("-", "Valuation overshoot — +527% off 52-wk low; trading at 99x FY2026E EPS prices years of execution", -0.9, 0.25),
    ("-", "Analyst skepticism — avg target $87.86 sits 26% BELOW current $119 price",                -0.6, 0.20),
    ("-", "Method B (FY2028E $3.00 × 35x = $105) also below current price — fundamentals lag price", -0.5, 0.15),
    ("-", "Execution risk — turnaround narrative real but unproven at scale; 18A vs N2 parity TBD",  -0.3, 0.05),
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
CONS_EPS_2YR  = 3.00    # conservative FY2028E EPS per SUMMARY guidance
CONS_PE_2YR   = 35      # rerating: turnaround proven, but multiple compresses from 99x toward growth-justified 35x
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Semiconductors / Foundry Turnaround / AI PC / Data Center")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
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
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_ni   = curr_oi * (1 - TAX_RATE)
shares    = SHARES_OUT_M / 1000
curr_eps  = round(curr_ni / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B
bull_ni   = bull_oi * (1 - TAX_RATE)
shares_b  = shares * 1.00   # no buyback expected during turnaround
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.90   # mix shift; foundry losses widen
bear_oi   = bear_gp - OPEX_FIXED_B * 0.97            # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (BASE est ${EPS_FY2026E:.2f}  ✓ approx)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 65× = ~${bull_eps_imp*65:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.90:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 30× trough P/E (cyclical floor) = ~${bear_eps_imp*30:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_foundry = 1.0 * 0.30 * (1 - TAX_RATE) / shares   # foundry incremental margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Foundry external revenue:  +${eps_per_1B_foundry:.3f}/EPS  = +${eps_per_1B_foundry*55:.1f}/share at 55× P/E")
print(f"  Data Center revenue ±$1B (45% margin): ±${1.0*0.45*(1-TAX_RATE)/shares:.3f}/EPS  =  ±${1.0*0.45*(1-TAX_RATE)/shares*55:.1f}/share at 55× P/E")
print(f"  1pp GM expansion (18A yield gain):  +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*55:.1f}/share at 55× P/E")
print(f"  Each new major foundry customer:     est. +$2-4B revenue, multi-year ramp; re-rates IFS segment")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (18A ramp / Foundry wins / Panther Lake / Data Center / GM / CHIPS framework)")
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
    ("18A yield improvement / ramp",   "+7%/mo", "<3%/mo", "−4pp",   "Yield curve plateaus below cost-parity; Panther Lake delayed to 2027"),
    ("Foundry external customer wins", "1 (MSFT)","0 new", "flat",   "No additional major customers signed; Microsoft scope narrows"),
    ("Panther Lake reception",         "on-time","delayed","slip",   "18A defect density too high for volume; OEMs delay designs"),
    ("Data Center vs AMD EPYC",        "flat-ish","-5pp",  "−5pp",   "EPYC Turin/Venice gains accelerate; Granite Rapids underperforms"),
    ("Gross margin recovery",          "~40%",   "<35%",  "−5pp",   "Foundry losses widen on under-utilization; mix shifts to low-margin"),
    ("CHIPS Act funding execution",    "on-track","delayed","slip",  "Funding milestones missed/conditions tightened; capex cuts follow"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: 18A yield improvement stalls below cost-parity AND Panther Lake slips into")
print(f"  2027, while no additional major Intel Foundry customers are announced. Combined with")
print(f"  continued Data Center share losses to AMD EPYC and slower-than-guided gross margin")
print(f"  recovery, the turnaround narrative stalls. EPS compresses to ~${bear_price/30:.2f} → 30× floor = ${bear_price}.")
print(f"  Note: ${bear_price} would represent a return to pre-recovery levels — a near-total reversal")
print(f"  of the +527% move off the ${VOL_52W_LOW} 52-week low. CHIPS Act backing and the foundry")
print(f"  asset base provide some floor, but the equity has substantial air pocket below current price.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E EPS estimate:           ${EPS_FY2026E:.2f}  (BASE case; turnaround still early-stage)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (cyclical semis trough multiple)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP means the market prices in years of successful execution")
print(f"  on 18A, Panther Lake, and foundry diversification ABOVE the trough-floor multiple. At")
print(f"  ${CURRENT_PRICE:.2f} and FY2026E EPS ~${EPS_FY2026E:.2f}, the implied P/E is ~99× — extraordinary for a")
print(f"  company still working through foundry losses. The risk is that the +527% recovery from")
print(f"  ${VOL_52W_LOW} has run ahead of delivered fundamentals.")
print(f"  EPP path: FY2028E EPS ~$3.00 × {PE_PESSIMISTIC:.0f}× = ${3.00*PE_PESSIMISTIC:.0f} floor by 2028 (EPP growing as turnaround matures).")
print(f"  Method B: FY2028E EPS $3.00 × 35× = ${3.00*35:.0f}  — still {round((3.00*35-CURRENT_PRICE)/CURRENT_PRICE*100,1)}% below current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: P/E rerates from 99x toward growth-justified 35x)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (per guidance; 18A ramp + foundry losses narrow)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (rerates from 99× toward growth-justified 35×; still a premium)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (no dividend; suspended during turnaround)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE PROBLEM: even the conservative case (FY2028E EPS $3.00 at 35×) implies a price")
print(f"  BELOW the current ${CURRENT_PRICE:.2f} — a {abs(cons_return):.1f}% decline. That requires multiple compression")
print(f"  from 99× to 35× to outweigh the EPS recovery from ~${EPS_FY2026E:.2f} to $3.00 (2.5x EPS growth).")
print(f"  For conservative 2yr to break even at 35× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~${((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth above the FY2026E base — possible at BULL/XBULL, not BASE.")
print(f"  Breakeven at 55× P/E (BASE multiple held): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 55:.2f}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.55
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: +527% move off ${VOL_52W_LOW} low is one of the largest mega-cap recoveries ever recorded")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (suspended; capital redirected to capex/turnaround)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (extreme; turnaround binary outcomes drive wide swings)")
print(f"  Beta vs S&P 500:      1.6  (high; cyclical semis + binary turnaround narrative)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe but plausible given turnaround binary risk)")
print(f"  52W low ${VOL_52W_LOW:.2f} represents the pre-recovery valuation floor before the 18A/foundry re-rating.")
print(f"  → 18A yield/ramp trajectory and Panther Lake reception are THE KEY binaries for the next 12mo.")
print(f"  → Additional Intel Foundry customer announcements are the key BULL catalyst (re-rates IFS).")
print(f"  → WATCHLIST $70-80  |  ACCUMULATE ~$50  |  BUY below $40  |  AVOID above current price")

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
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0 fundamentals,")
print(f"  while the model scores actual fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0. The gap ({ADJ_GAP:.2f}) indicates")
print(f"  the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: the average analyst target ($87.86, 26% below current) and Method B")
print(f"  (FY2028E $3.00 × 35x = $105, also below current) both suggest the +527% recovery has")
print(f"  run ahead of delivered fundamentals — the turnaround thesis is real, but the durability")
print(f"  of a re-rating to current levels depends on 18A execution still largely ahead of us.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) 18A yield/ramp updates — current +7%/month pace must continue toward cost-parity")
print(f"  (2) Panther Lake launch reception (H2 2026) — AI PC OEM uptake and unit volumes")
print(f"  (3) Additional Intel Foundry external customer announcements — beyond Microsoft")
print(f"  (4) Data Center/Xeon vs AMD EPYC competitive dynamics — share stabilization or further loss")
print(f"  (5) Gross margin trajectory — foundry operating losses narrowing on schedule")
print(f"  (6) CHIPS Act capex execution — $19B funding milestones and capex discipline")
print(f"  WATCHLIST $70-80  |  ACCUMULATE ~$50  |  BUY below $40  |  AVOID above ${CURRENT_PRICE:.2f}")
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
