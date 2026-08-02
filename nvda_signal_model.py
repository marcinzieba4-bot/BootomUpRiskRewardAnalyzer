"""
NVDA  ·  NVIDIA Corporation  ·  NASDAQ: NVDA
Bottom-up signal model  ·  AI Accelerators / Data Center / Gaming / Robotics
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "NVDA"
COMPANY       = "NVIDIA Corporation"
SECTOR        = "AI Accelerators · Data Center · Gaming · Robotics · NASDAQ: NVDA"
CURRENT_PRICE = 200.75       # USD; as of 2026-08-02
VOL_52W_LOW   = 164.07       # 52-week trough
VOL_52W_HIGH  = 236.54       # 52-week peak
SHARES_OUT_M  = 24_400.0     # millions; ~$4.94T market cap / ~$200

# Dividend: token; quarterly $0.01/share ($0.04/yr)
ANNUAL_DIV    = 0.04         # $/share

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2027E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Data Center",              350.0, 200.0, 440.0, "Blackwell/Rubin; hyperscaler + sovereign AI; +92% YoY Q1 FY2027"),
    ("Gaming",                    18.0,  12.0,  25.0, "RTX 50 series; DLSS 4; PC gaming refresh cycle"),
    ("Professional Visualization", 5.0,   3.0,   8.0, "Omniverse; digital twin; enterprise 3D; NIM microservices"),
    ("Automotive",                 8.0,   5.0,  14.0, "DRIVE Thor; robotaxi; ADAS; Waymo/BYD partnerships"),
    ("OEM & Other",                3.0,   2.0,   5.0, "Edge AI; embedded; partner OEM platforms"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.730   # blended non-GAAP gross margin FY2027E (~73%; Blackwell ASP lift)
GROSS_MARGIN_BULL = 0.760   # BULL: Rubin NVLink premium; software/NIM attach rate rises
OPEX_FIXED_B      = 14.0    # R&D + SG&A ($B); investing heavily in Rubin/next-gen; growing ~20%/yr
TAX_RATE          = 0.130   # effective rate; US R&D credits; Singapore/Ireland structures

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 9.34        # FY2027E adj non-GAAP EPS (consensus; beat Q1 $1.87 vs $1.77 est)
PE_PESSIMISTIC = 22.0        # trough P/E: CUDA moat floor; FY2022 trough was 20-22×; CUDA lock-in
                              # supports higher floor than commodity semis
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # ~$205

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 4.50, 22,   99, "Hyperscaler capex freeze + DeepSeek 10x efficiency + ASIC >50% displacement; Rev ~$222B"),
    "BASE":  ( 9.34, 25,  234, "Blackwell/Rubin steady ramp; DC growth normalizes ~40%; Rev ~$391B; EPS $9.34 at 25x"),
    "BULL":  (12.50, 30,  375, "Rubin supercycle + agentic AI + robotics/physical AI explosion; Rev ~$500B; EPS $12.50 at 30x"),
    "XBULL": (18.00, 35,  630, "NVDA = AGI/physical AI backbone; Rev $700B+; EPS $18 at 35x"),
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
        "name":       "Data Center revenue YoY growth",
        "weight":     0.30,
        "thresholds": ("<30%",   ">=60%",  ">=100%",  ">=150%"),
        "now":        "+92%",
        "score":      3,
        "comment":    "Q1 FY2027 Data Center $75.2B +92% YoY; Blackwell ramping; Rubin sampling H2 2026; hyperscaler demand insatiable",
    },
    {
        "name":       "Non-GAAP gross margin",
        "weight":     0.20,
        "thresholds": ("<65%",   ">=70%",  ">=76%",   ">=82%"),
        "now":        "~73%",
        "score":      2,
        "comment":    "Blackwell transition costs pressuring near-term margins; guide to 71.5-73% as yields normalize; software attach TBD",
    },
    {
        "name":       "Hyperscaler AI capex guidance",
        "weight":     0.20,
        "thresholds": ("<+10%",  ">=+30%", ">=+60%",  ">=+100%"),
        "now":        "~+50%",
        "score":      3,
        "comment":    "MSFT $80B, Google $75B, AWS $105B, Meta $65B capex -- all raised FY2026; sovereign AI additive; ~$325B combined",
    },
    {
        "name":       "Blackwell supply tightness / book-to-bill",
        "weight":     0.15,
        "thresholds": ("<1.0x",  ">=1.2x", ">=1.5x",  ">=2.0x"),
        "now":        "~1.6x",
        "score":      3,
        "comment":    "Orders exceed supply; lead times 6-9 months; CoWoS-L packaging at TSMC constrained; NVLink switch backlog",
    },
    {
        "name":       "China/export control exposure",
        "weight":     0.10,
        "thresholds": ("<$5B",   ">=$8B",  ">=$15B",  ">=$25B"),
        "now":        "~$10B",
        "score":      3,
        "comment":    "H20 partially restricted; ~$10B annual China revenue path via non-restricted SKUs; recovery via non-China sovereign AI",
    },
    {
        "name":       "Automotive + Robotics revenue run-rate",
        "weight":     0.05,
        "thresholds": ("<$3B",   ">=$5B",  ">=$10B",  ">=$20B"),
        "now":        "~$8B",
        "score":      2,
        "comment":    "Automotive $8B FY2027E; Jetson Orin/Thor; Isaac robotics; Waymo/BYD/Li Auto design wins; long ramp ahead",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "CUDA ecosystem moat -- 5M+ devs; cuDNN; cuBLAS; 10yr switching cost; NCCL",        +0.8, 0.25),
    ("+", "Blackwell/Rubin roadmap -- 2x+ perf/W per gen; NIM; NVLink; GB200 NVL72",           +0.7, 0.20),
    ("-", "Hyperscaler ASIC displacement -- TPU v6/Trainium 3 scaling; NVDA still dominant",   -0.5, 0.20),
    ("-", "Concentration risk -- top 4 hyperscalers ~45% revenue; capex cycle binary risk",    -0.4, 0.15),
    ("+", "Physical AI / robotics optionality -- Jetson; DRIVE Thor; factory AI; Isaac Sim",   +0.6, 0.10),
    ("-", "Export controls escalation -- H20 restrictions; partial recovery non-China mkts",   -0.3, 0.10),
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
CONS_EPS_2YR  = 14.00   # conservative FY2029E: ~22% CAGR as growth decelerates 85%->20%
CONS_PE_2YR   = 22      # conservative exit P/E: multiple compression as growth normalizes; CUDA floor
cons_equity   = CONS_EPS_2YR * CONS_PE_2YR
cons_divs     = ANNUAL_DIV * 2
cons_total    = cons_equity + cons_divs
cons_return   = round((cons_total - CURRENT_PRICE) / CURRENT_PRICE * 100, 1)
cons_annual   = round(cons_return / 2, 1)

# ─────────────────────────────────────────────────────────────────────────────
#  OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
W = 72

def hr(): print("  " + "-" * W)
def bar(score):
    return "X" * score + "." * (4 - score)

print()
print("=" * (W + 4))
print(f"  {TICKER}  .  {COMPANY}  .  ${CURRENT_PRICE:.2f}  .  AI Accelerators / Data Center / Gaming / Robotics")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("=" * (W + 4))

# --- (1) PRODUCT REVENUE BRIDGE -----------------------------------------------
print()
print("  PRODUCT REVENUE BRIDGE  (FY2027E  ->  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<26}  {'FY2027E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'D Bear':>8}  {'D Bull':>8}")
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
shares_b  = shares * 1.00   # minimal buyback; NVDA issues options; roughly flat share count
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.94   # utilization/ASP pressure
bear_oi   = bear_gp - OPEX_FIXED_B * 0.90           # partial opex flex
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2027E EPS check:  ${curr_total:.1f}B rev x {GROSS_MARGIN_CURR*100:.1f}% GM - ${OPEX_FIXED_B:.1f}B opex - {TAX_RATE*100:.1f}% tax")
print(f"  / {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2027E:.2f}  ok)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev x {GROSS_MARGIN_BULL*100:.1f}% GM - ${OPEX_FIXED_B:.1f}B opex - tax")
print(f"  / {shares_b:.3f}B shares  =  ~${bull_eps_imp:.1f}/share  ->  ${bull_eps_imp:.1f} x 30x = ~${bull_eps_imp*30:.0f}  BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev x {GROSS_MARGIN_CURR*100*0.94:.1f}% GM - opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 22x trough P/E (CUDA moat floor) = ~${bear_eps_imp*22:.0f}  BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev   = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_dc    = 1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Data Center revenue:   +${eps_per_1B_dc:.3f}/EPS  = +${eps_per_1B_dc*25:.1f}/share at 25x P/E")
print(f"  Every 1pp gross margin:          +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*25:.1f}/share at 25x P/E")
print(f"  China export control +$5B rev:   +${5.0*GROSS_MARGIN_CURR*(1-TAX_RATE)/shares:.2f}/EPS  = +${5.0*GROSS_MARGIN_CURR*(1-TAX_RATE)/shares*25:.1f}/share at 25x P/E")
print(f"  Hyperscaler capex -20% (yoy):    ~-$40B Data Center rev  =  ~-${40*eps_per_1B_dc:.1f}/EPS  =  -${40*eps_per_1B_dc*25:.0f}/share")

# --- (2) SIGNAL DASHBOARD -----------------------------------------------------
print()
print("  (1) SIGNAL DASHBOARD  (AI capex cycle / CUDA moat / supply/demand / export controls)")
hr()
score_labels = {1: "BEAR", 2: "BASE", 3: "BULL", 4: "XBULL"}
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
print(f"  SCA adjustment:    {SCA:+.3f}  ->  Adj composite {ADJ_COMPOSITE:.3f}  ->  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:72]:<72}  ({score:+.1f} x {weight*100:.0f}%  =  {contribution:+.3f})")

# --- (3) BEAR CASE ANATOMY ----------------------------------------------------
print()
print(f"  (2) BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Data Center revenue YoY",        "+92%",  "<30%",   "-62pp",  "Hyperscaler capex freeze; DeepSeek-style efficiency 10x"),
    ("Non-GAAP gross margin",          "~73%",  "<65%",   "-8pp",   "ASIC displacement >50%; ASP collapse; utilization drop"),
    ("Hyperscaler AI capex guidance",  "~+50%", "<+10%",  "-40pp",  "CIO survey: ROI unclear; model efficiency renders CapEx excess"),
    ("Blackwell book-to-bill",         "~1.6x", "<1.0x",  "-0.6x",  "Order cancellations; hyperscaler ASIC ramp replaces Blackwell"),
    ("China/export control exposure",  "~$10B", "<$5B",   "-$5B",   "Full H20 ban + secondary sanctions on non-China re-export"),
    ("Automotive+Robotics run-rate",   "~$8B",  "<$3B",   "-$5B",   "DRIVE Thor delays; ADAS customers choose Mobileye/Qualcomm"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Hyperscaler CEOs collectively signal AI infrastructure ROI has plateaued;")
print(f"  combined with DeepSeek-architecture successors achieving 10x inference efficiency gain,")
print(f"  ASIC alternatives (Google TPU v6, AWS Trainium 3) capturing >50% new AI workloads.")
print(f"  Revenue collapses from ~$391B to ~$222B. EPS ~$4.50 x 22x CUDA floor P/E = ~${bear_price}.")
print(f"  Note: ${bear_price} is NOT permanent impairment -- CUDA ecosystem (5M+ devs) + inference growth")
print(f"  provides durable floor. Recovery path to ~${bear_price+80}--${bear_price+130} within 2-3yr post-trough.")

# --- (4) EPP ------------------------------------------------------------------
print()
print("  (3) EPP  (Earnings Power Price: pessimistic P/E x current EPS)")
hr()
print(f"  FY2027E adj non-GAAP EPS:      ${EPS_FY2027E:.2f}  (consensus; Q1 beat $1.87 vs $1.77 est)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}x  (CUDA moat floor; FY2022 trough 20-22x; software defensibility)")
print(f"  -----------------------------------------------------------------------")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (stock is NEAR/BELOW EPP floor -- VERY BULLISH)")
print()
print(f"  CRITICAL INSIGHT: EPP ~${EPP:.0f} is ABOVE current price of ${CURRENT_PRICE:.2f}.")
print(f"  This means the market is pricing NVDA below its pessimistic earnings power floor.")
print(f"  At ${CURRENT_PRICE:.2f} and FY2027E EPS ${EPS_FY2027E:.2f}, the forward P/E is ~{CURRENT_PRICE/EPS_FY2027E:.1f}x -- extraordinarily")
print(f"  cheap for a company growing revenue +85% YoY. The PEG ratio is ~0.25x on near-term growth.")
print(f"  EPP path: FY2029E EPS ~$14 x {PE_PESSIMISTIC:.0f}x = ${14*PE_PESSIMISTIC:.0f} EPP floor by 2029 (EPP growing ~22%/yr).")
print(f"  At 25x mid-cycle P/E: ${EPS_FY2027E:.2f} x 25 = ${EPS_FY2027E*25:.0f}  -- {((EPS_FY2027E*25/CURRENT_PRICE)-1)*100:.0f}% ABOVE current price.")

# --- (5) CONSERVATIVE GROWTH --------------------------------------------------
print()
print("  (4) CONSERVATIVE GROWTH  (2-yr to FY2029E: growth decelerates 85% -> ~20%; multiple compresses)")
hr()
print(f"  Conservative FY2029E adj EPS:  ${CONS_EPS_2YR:.2f}  (~22% EPS CAGR from FY2027E; growth deceleration)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (multiple compression as growth normalizes; CUDA floor)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; token yield)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'v' if cons_total < CURRENT_PRICE else '^'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE OPPORTUNITY: even the CONSERVATIVE case with maximum multiple compression")
print(f"  (85% -> 22% growth, 21.5x -> 22x P/E trough) delivers +{cons_return:.0f}% in 2 years.")
print(f"  This is because the earnings growth (+50% cumulative) overwhelms any P/E compression.")
print(f"  For conservative 2yr to LOSE money: need EPS < ${CURRENT_PRICE / CONS_PE_2YR:.2f} by FY2029E")
print(f"  That requires EPS to DECLINE {((1 - CURRENT_PRICE/CONS_PE_2YR/EPS_FY2027E)*100):.1f}% from today -- only if BEAR scenario hits.")
print(f"  Breakeven at 22x trough P/E: FY2029E EPS >= ${CURRENT_PRICE / CONS_PE_2YR:.2f}  (vs ${CONS_EPS_2YR:.2f} conservative est)")
print(f"  ACCUMULATE trigger: current price IS the entry -- stock at/below EPP floor of ${EPP:.0f}")

# --- (6) VOLATILITY CONTEXT ---------------------------------------------------
print()
print("  (5) VOLATILITY CONTEXT")
hr()
annual_vol  = 0.45
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  --  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  --  token; growth stock)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (high; AI capex cycle binary; export control headlines)")
print(f"  Beta vs S&P 500:      1.85  (high; AI infrastructure proxy; sentiment-driven amplification)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  --  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} +/- {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}sigma drawdown  (tail scenario; capex freeze + ASIC displacement)")
print(f"  52W low ${VOL_52W_LOW:.2f} already tested; Apr-Jun 2026 export control/macro fear drove -18% move.")
print(f"  -> Hyperscaler capex guidance is THE KEY binary; each $10B capex raise = +5-8% NVDA move.")
print(f"  -> DeepSeek-style efficiency gains are THE KEY bear catalyst; watch inference-to-training ratio.")
print(f"  -> BUY/ACCUMULATE at current price  |  ADD on dips to $165-180  |  TRIM above $320-350")

# --- (7) SCENARIO PROBABILITIES -----------------------------------------------
print()
print("  (6) SCENARIO PROBABILITIES  (proxy model vs market-implied)")
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
print(f"  Downside  (-> Bear ${bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (-> Bull ${bull_price}):  {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b_str}")
print(f"  Signal    :  {signal_full}")
print()
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is BELOW the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0 -- between")
print(f"  BASE and BULL. The model scores the fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0 -- solidly BULL.")
print(f"  The gap ({ADJ_GAP:+.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: you are paying BASE-to-BULL prices for what is executing at BULL pace.")
print(f"  Stock at/below EPP floor (${EPP:.0f}) is the most bullish structural signal in the model.")

# --- FOOTER -------------------------------------------------------------------
print()
print("=" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Hyperscaler capex raise cycle -- each quarterly raise is a positive re-rating event")
print(f"  (2) Rubin GPU availability -- sampling H2 2026; volume 2027; 2x perf/W over Blackwell")
print(f"  (3) NIM/software attach rate -- CUDA moat monetized as software; margin expansion catalyst")
print(f"  (4) DRIVE Thor revenue ramp -- $8B->$14B Automotive is underappreciated optionality")
print(f"  (5) DeepSeek/ASIC displacement -- watch inference efficiency gains vs training demand growth")
print(f"  ACCUMULATE at ${CURRENT_PRICE:.2f}  |  ADD on dips $165-180  |  STRONG BUY below $160")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}x  |  FY2027E EPS: ${EPS_FY2027E:.2f}")
print("=" * (W + 4))
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
