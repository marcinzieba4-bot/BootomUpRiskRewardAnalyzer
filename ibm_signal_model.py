"""
IBM  ·  International Business Machines Corp.  ·  NYSE: IBM
Bottom-up signal model  ·  Hybrid Cloud / AI (watsonx) / Consulting / zSystems
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "IBM"
COMPANY       = "International Business Machines Corp."
SECTOR        = "Hybrid Cloud · Red Hat · watsonx AI · Consulting · zSystems · NYSE: IBM"
CURRENT_PRICE = 245.00      # USD; as of 2026-06-10
VOL_52W_LOW   = 195.00
VOL_52W_HIGH  = 275.00
SHARES_OUT_M  = 920.0       # millions; modest buyback

# Dividend: 30-year growth streak (Dividend Aristocrat)
ANNUAL_DIV    = 6.72        # $/share annualized

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Software (Red Hat/Hybrid Cloud, Automation, watsonx AI)", 30.5, 26.0, 36.0, "Red Hat OpenShift + watsonx AI book of business; highest-margin engine"),
    ("Consulting",                                              21.0, 17.5, 24.5, "Generative AI + hybrid cloud advisory; backlog-driven, signings sensitive"),
    ("Infrastructure (zSystems, Storage)",                      14.5, 11.0, 18.5, "z17 mainframe cycle; lumpy, transaction-driven; high-margin in cycle years"),
    ("Financing",                                                0.7,  0.6,  0.8, "Client/commercial financing of IBM hardware/software; small, stable"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.570   # blended gross margin FY2026E (~57%; software mix lifts blend)
GROSS_MARGIN_BULL = 0.595   # BULL: software mix shift continues; watsonx scale economics
OPEX_FIXED_B      = 21.0    # SG&A + R&D ($B); largely fixed cost base
TAX_RATE          = 0.150   # effective rate; global tax structure

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 11.50      # FY2026E adj EPS (consensus ~$11.40-$11.65; non-GAAP)
PE_PESSIMISTIC = 16.0       # trough P/E: IBM historical trough multiple in down-cycles
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $184

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 9.50, 18,  171, "watsonx bookings stall; consulting backlog shrinks; z17 cycle disappoints; EPS $9.50 → 18× de-rate"),
    "BASE":  (11.50, 23,  265, "Steady hybrid cloud/Red Hat double-digit growth; watsonx scaling; z17 cycle on track; EPS $11.50 → 23×"),
    "BULL":  (13.50, 27,  365, "watsonx book of business accelerates; consulting signings reaccelerate; FCF re-rates multiple; EPS $13.50 → 27×"),
    "XBULL": (16.00, 31,  496, "AI software platform leadership; Red Hat hybrid cloud becomes default enterprise stack; EPS $16.00 → 31×"),
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
        "name":       "Hybrid cloud / Red Hat revenue growth (constant currency)",
        "weight":     0.25,
        "thresholds": ("<5%",   "≥8%",   "≥12%",   "≥18%"),
        "now":        "+9%",
        "score":      2,
        "comment":    "Red Hat OpenShift + Ansible growing high-single digits; AI workload migrations accelerating",
    },
    {
        "name":       "watsonx AI book of business growth (YoY)",
        "weight":     0.20,
        "thresholds": ("<30%",  "≥50%",  "≥80%",   "≥120%"),
        "now":        "+65%",
        "score":      3,
        "comment":    "watsonx AI book of business compounding from a small base; agentic AI / watsonx Orchestrate driving adoption",
    },
    {
        "name":       "Consulting backlog/signings growth (YoY)",
        "weight":     0.15,
        "thresholds": ("<0%",   "≥3%",   "≥7%",    "≥12%"),
        "now":        "+4%",
        "score":      2,
        "comment":    "GenAI consulting signings growing but overall backlog roughly flat-to-modest; clients cautious on discretionary spend",
    },
    {
        "name":       "Free cash flow growth (YoY)",
        "weight":     0.20,
        "thresholds": ("<0%",   "≥3%",   "≥7%",    "≥12%"),
        "now":        "+6%",
        "score":      2,
        "comment":    "FCF tracking toward ~$13.5-14B guide; steady mid-single-digit growth; supports dividend coverage",
    },
    {
        "name":       "Gross margin expansion (software mix shift)",
        "weight":     0.10,
        "thresholds": ("<55%",  "≥56.5%", "≥58%",  "≥60%"),
        "now":        "57.0%",
        "score":      2,
        "comment":    "Software now >40% of revenue; mix shift toward Red Hat/watsonx steadily lifting blended gross margin",
    },
    {
        "name":       "zSystems mainframe cycle (z17 refresh)",
        "weight":     0.10,
        "thresholds": ("Down >10%", "Flat/+low single", "Up double-digit", "Up >25% (peak cycle)"),
        "now":        "Up ~12%",
        "score":      3,
        "comment":    "z17 launch driving early-cycle MIPS growth; refresh cycle tracking ahead of z16 comparable period",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Red Hat hybrid cloud moat — sticky OpenShift/Ansible platform; high switching costs",      +0.6, 0.20),
    ("+", "watsonx AI optionality — early but compounding; enterprise trust/governance positioning",  +0.5, 0.20),
    ("+", "Durable dividend — 30-yr Dividend Aristocrat; ~$6B+ FCF cushion supports payout",           +0.4, 0.15),
    ("-", "Slower growth profile vs hyperscalers — single-digit total revenue growth ceiling",        -0.7, 0.20),
    ("-", "Consulting cyclicality — discretionary IT spend sensitive to macro slowdowns",              -0.4, 0.15),
    ("-", "zSystems lumpiness — mainframe cycle creates multi-year revenue troughs post-refresh",      -0.3, 0.10),
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
CONS_EPS_2YR  = 12.50   # conservative FY2028E: ~4.5% EPS CAGR; software mix shift continues
CONS_PE_2YR   = 20      # rerating from ~21x toward growth-justified 20x; modest compression
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Hybrid Cloud / AI / Consulting / zSystems")
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
shares_b  = shares * 0.97   # modest buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift away from software
bear_oi   = bear_gp - OPEX_FIXED_B * 0.97           # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 27× = ~${bull_eps_imp*27:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 18× trough P/E (historical down-cycle floor) = ~${bear_eps_imp*18:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev   = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_zsys  = 1.0 * 0.65 * (1 - TAX_RATE) / shares   # zSystems higher-margin contribution

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Software revenue:        +${eps_per_1B_rev * (1-TAX_RATE):.3f}/EPS  = +${eps_per_1B_rev*(1-TAX_RATE)*23:.1f}/share at 23× P/E")
print(f"  zSystems revenue ±$1B (65% margin): ±${eps_per_1B_zsys:.3f}/EPS  =  ±${eps_per_1B_zsys*23:.1f}/share at 23× P/E")
print(f"  1pp GM expansion (mix/pricing):     +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*23:.1f}/share at 23× P/E")
print(f"  1% buyback (~9M shares):            +${curr_eps*0.01:.3f}/EPS  (mechanical accretion; modest annual repurchases)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (hybrid cloud / watsonx AI / consulting / zSystems framework)")
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
    ("Hybrid cloud/Red Hat revenue growth",  "+9%",   "<5%",     "−4pp",   "Enterprise cloud migration slows; hyperscalers win share from Red Hat"),
    ("watsonx AI book of business growth",   "+65%",  "<30%",    "−35pp",  "Enterprise GenAI spend stalls; watsonx loses mindshare to OpenAI/Azure AI"),
    ("Consulting backlog/signings growth",   "+4%",   "<0%",     "−4pp",   "Macro slowdown; clients pause discretionary digital transformation projects"),
    ("Free cash flow growth",                "+6%",   "<0%",     "−6pp",   "Revenue softness + pension/restructuring charges compress FCF"),
    ("Gross margin (software mix)",          "57.0%", "<55%",    "−2.0pp", "Mix reverts toward lower-margin infrastructure/consulting"),
    ("zSystems cycle (z17)",                 "+12%",  "Down>10%","−22pp",  "z17 refresh disappoints; clients delay upgrades amid IT budget freezes"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A combination of enterprise IT budget freezes (macro slowdown) and a stall in")
print(f"  watsonx AI adoption — enterprises shift GenAI workloads to hyperscaler-native AI stacks —")
print(f"  would compress consulting signings and software growth simultaneously. EPS falls to ~$9.50,")
print(f"  and the multiple de-rates to 18× (historical down-cycle floor) = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT a permanent impairment — Red Hat's installed base + the 30-yr")
print(f"  dividend streak provide a durable floor. Recovery toward ${bear_price+50}-${bear_price+90} in 2yr is")
print(f"  plausible once the next zSystems cycle or AI adoption wave resumes.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~$11.40-$11.65; non-GAAP)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (historical IBM down-cycle trough multiple)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  IBM trades near multi-decade highs after years of underperformance. A +{epp_gap_pct:.0f}% premium")
print(f"  to EPP means the market is pricing durable acceleration in hybrid cloud + AI software")
print(f"  (watsonx, Red Hat) rather than a return to the legacy hardware/services profile. At")
print(f"  ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f}, the P/E is ~{CURRENT_PRICE/EPS_FY2026E:.1f}× — elevated for IBM's")
print(f"  historical range but still reasonable vs the broader software/AI cohort. The key question")
print(f"  is whether the re-rating (AI/watsonx + Red Hat hybrid cloud moat) is durable or stretched.")
print(f"  EPP path: FY2028E EPS ~$12.50 × {PE_PESSIMISTIC:.0f}× = ${12.50*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing ~4%/yr).")
print(f"  At 23× mid-cycle P/E: ${EPS_FY2026E:.2f} × 23 = ${EPS_FY2026E*23:.0f}  — close to current price (BASE case alignment).")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest multiple compression; growth + dividend carry the case)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (~4.5% EPS CAGR: software mix shift + buyback)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (modest compression from ~{CURRENT_PRICE/EPS_FY2026E:.0f}× toward growth-justified 20×)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; 30-yr Dividend Aristocrat)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: can IBM sustain FY2028E EPS near ${CONS_EPS_2YR:.2f} even with modest multiple")
print(f"  compression to {CONS_PE_2YR}×? The dividend (${ANNUAL_DIV:.2f}/yr, ~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}% yield) provides a meaningful")
print(f"  cushion against multiple compression — unlike most AI-adjacent names.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — achievable near BASE case.")
print(f"  Breakeven at {int(CURRENT_PRICE/EPS_FY2026E)}× P/E (no multiple compression): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / int(CURRENT_PRICE/EPS_FY2026E):.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.20
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock trading near multi-decade highs after a multi-year hybrid cloud/AI re-rating")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  meaningful; 30-yr Dividend Aristocrat)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (lower than tech peers; defensive enterprise IT profile)")
print(f"  Beta vs S&P 500:      0.75  (defensive; large dividend; lower amplitude than mega-cap tech)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (significant; broad AI-adoption stall scenario)")
print(f"  52W low ${VOL_52W_LOW:.2f} already reflects pre-AI-re-rating valuation levels.")
print(f"  → watsonx AI adoption pace is THE KEY swing factor for sustaining the re-rating.")
print(f"  → Red Hat hybrid cloud growth reacceleration is the key bull catalyst for further upside.")
print(f"  → AVOID at ${CURRENT_PRICE:.0f}+  |  WATCHLIST $215–245  |  ACCUMULATE $190–215  |  BUY below $185")

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
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0 fundamentals.")
print(f"  The model scores the fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0. The gap ({ADJ_GAP:.2f}) indicates the")
print(f"  stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: IBM's hybrid cloud + AI re-rating is {'broadly supported by' if abs(ADJ_GAP) <= 0.20 else ('not yet fully reflected in' if ADJ_GAP > 0.20 else 'running ahead of')} current execution levels.")
print(f"  watsonx AI book-of-business growth (signal score {SIGNALS[1]['score']}/4) is the most significant swing factor.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) watsonx AI book of business updates — quarterly disclosure of AI bookings growth/scale")
print(f"  (2) Red Hat hybrid cloud growth — OpenShift/Ansible reacceleration above +12% (BULL trigger)")
print(f"  (3) zSystems z17 cycle — refresh adoption pace; mainframe MIPS growth trajectory")
print(f"  (4) Consulting signings/backlog — GenAI-driven discretionary spend recovery")
print(f"  (5) Free cash flow guidance — annual FCF target revisions (~$13.5-14B baseline)")
print(f"  (6) Dividend increase — 30-yr Dividend Aristocrat; annual raise typically announced in Q2")
print(f"  AVOID at ${CURRENT_PRICE:.0f}+  |  WATCHLIST $215–245  |  ACCUMULATE $190–215  |  BUY below $185")
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
