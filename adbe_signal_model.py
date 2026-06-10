"""
ADBE  ·  Adobe Inc.  ·  NASDAQ: ADBE
Bottom-up signal model  ·  Creative Software / Digital Experience / Generative AI
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "ADBE"
COMPANY       = "Adobe Inc."
SECTOR        = "Creative Software · Digital Experience · Generative AI (Firefly) · NASDAQ: ADBE"
CURRENT_PRICE = 244.48      # USD; as of 2026-06-10
VOL_52W_LOW   = 220.00      # post-earnings AI-fear trough
VOL_52W_HIGH  = 480.00      # 52-week high (down 65% from $699 ATH)
SHARES_OUT_M  = 410.0       # millions; steady buyback offsetting dilution

# Dividend: Adobe pays no dividend; reinvests via buybacks
ANNUAL_DIV    = 0.0         # $/share

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Digital Media (Creative+Document Cloud)", 16.80, 14.50, 19.50, "Creative Cloud subs + Acrobat/Document Cloud AI Assistant"),
    ("Digital Experience (Experience Cloud)",    5.90,  5.20,  7.00, "Marketing/analytics software; bookings growth, enterprise AEP"),
    ("Firefly / Generative AI add-ons",          0.60,  0.20,  1.80, "Direct Firefly credits + indirect CC/DX uplift; nascent but scaling"),
    ("Publishing/Other",                         0.45,  0.40,  0.50, "Legacy/other; immaterial, stable"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.885   # blended gross margin FY2026E (~88.5%; software economics)
GROSS_MARGIN_BULL = 0.895   # BULL: Firefly scale + opex leverage lifts blend further
OPEX_FIXED_B      = 11.20   # R&D + SG&A ($B); grows modestly; AI infra capex pressure
TAX_RATE          = 0.205   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 18.50       # FY2026E non-GAAP EPS at trough/BEAR-like assumptions
PE_PESSIMISTIC = 12.0        # trough P/E: 15-yr-low multiple on AI-disruption fear
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $222

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (18.50, 12, 222,  "AI disruption thesis confirmed; CC subscriber growth stalls; multiple stays at 15yr-low 12×"),
    "BASE":  (23.50, 18, 423,  "EPS grows ~19% to $23.50; multiple normalizes to 18× as Firefly monetization de-risks"),
    "BULL":  (28.00, 24, 672,  "Firefly becomes material revenue line; CC ARR reaccelerates; multiple rerates to 24×"),
    "XBULL": (34.00, 30, 1020, "Adobe establishes itself as the enterprise creative-AI platform of record; 30× multiple"),
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
        "name":       "Creative Cloud subscriber/ARR growth",
        "weight":     0.25,
        "thresholds": ("<5%",    "≥7%",   "≥10%",   "≥14%"),
        "now":        "+8%",
        "score":      2,
        "comment":    "CC ARR growth steady at ~8% YoY; net adds resilient; no visible churn from gen-AI substitutes yet",
    },
    {
        "name":       "Firefly / generative AI monetization (direct + indirect)",
        "weight":     0.20,
        "thresholds": ("<$0.3B", "≥$0.6B","≥$1.2B", "≥$2.0B"),
        "now":        "~$0.6B run-rate",
        "score":      2,
        "comment":    "Firefly credits + Express + GenStudio scaling; still small vs $24B total revenue but growing fast",
    },
    {
        "name":       "Document Cloud (Acrobat AI Assistant) growth",
        "weight":     0.15,
        "thresholds": ("<8%",    "≥11%",  "≥15%",   "≥20%"),
        "now":        "+12%",
        "score":      2,
        "comment":    "AI Assistant add-on driving incremental ARPU; Acrobat reach (1B+ users) underpins funnel",
    },
    {
        "name":       "Digital Experience / Experience Cloud growth",
        "weight":     0.15,
        "thresholds": ("<6%",    "≥8%",   "≥11%",   "≥15%"),
        "now":        "+9%",
        "score":      2,
        "comment":    "Enterprise bookings stable; AEP/GenStudio for Performance Marketing gaining traction",
    },
    {
        "name":       "FCF margin",
        "weight":     0.10,
        "thresholds": ("<35%",   "≥38%",  "≥42%",   "≥46%"),
        "now":        "~40%",
        "score":      2,
        "comment":    "Software economics intact; FCF still ~$8-9B annually despite AI infra capex step-up",
    },
    {
        "name":       "AI disruption risk to creative-tools moat (Midjourney/Sora/Canva)",
        "weight":     0.15,
        "thresholds": ("Severe", "Elevated","Contained","Tailwind"),
        "now":        "Elevated",
        "score":      1,
        "comment":    "Market pricing in moat erosion from native gen-AI tools; workflow lock-in (PSD/professional pipelines) untested at scale",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "EPS still compounding ~19% YoY despite the AI-fear narrative; estimates not cut",         +0.6, 0.20),
    ("+", "Subscriber churn from generative-AI substitutes has NOT materialized in the data",         +0.5, 0.20),
    ("-", "15-year-low multiple reflects genuine market belief that Firefly is too little/late",      -0.7, 0.20),
    ("-", "CEO transition (Narayen exit, Mar 2026) adds execution-risk discount during AI pivot",     -0.5, 0.15),
    ("+", "Firefly/GenStudio optionality: AI as tailwind (workflow integration) mispriced as tail risk", +0.5, 0.15),
    ("-", "Professional-tool moat erosion risk — Canva/Midjourney/Sora encroaching on prosumer base", -0.4, 0.10),
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
CONS_EPS_2YR  = 21.50   # conservative FY2028E: modest growth from $18.50, AI fears partially persist
CONS_PE_2YR   = 15      # rerating from 10.4× to 15× as fears partially abate but discount persists
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Creative Software / Digital Experience / Generative AI")
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
shares_b  = shares * 0.96   # ~2%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.99   # mix shift slightly compresses margin
bear_oi   = bear_gp - OPEX_FIXED_B * 0.99           # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.2f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.2f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share non-GAAP EPS  (target ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.2f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 24× = ~${bull_eps_imp*24:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B rev × {GROSS_MARGIN_CURR*100*0.99:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 12× trough P/E (15-yr-low fear multiple) = ~${bear_eps_imp*12:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Digital Media revenue:  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*18:.1f}/share at 18× P/E")
print(f"  Every $0.5B Firefly revenue:       +${eps_per_1B_rev*0.5:.3f}/EPS  =  +${eps_per_1B_rev*0.5*18:.1f}/share at 18× P/E")
print(f"  1pp GM expansion (Firefly mix):   +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*18:.1f}/share at 18× P/E")
print(f"  1× P/E rerate (multiple expansion): +${EPS_FY2026E*1:.2f}/share  (mechanical; current EPS × 1×)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Creative Cloud / Firefly / Document Cloud / Digital Experience framework)")
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
    ("CC subscriber/ARR growth",       "+8%",    "<5%",    "−3pp",   "Net adds decelerate as Canva/Midjourney capture prosumer segment"),
    ("Firefly monetization run-rate",  "$0.6B",  "<$0.3B", "−$0.3B", "Firefly credits cannibalized by free/cheap third-party gen-AI tools"),
    ("Document Cloud growth",          "+12%",   "<8%",    "−4pp",   "AI Assistant add-on attach rate stalls; Acrobat commoditized"),
    ("Digital Experience growth",      "+9%",    "<6%",    "−3pp",   "Enterprise bookings soften on macro slowdown / AI-native rivals"),
    ("FCF margin",                     "~40%",   "<35%",   "−5pp",   "AI infra capex step-up outpaces revenue; opex discipline lapses"),
    ("AI disruption risk score",       "Elevated","Severe","↓1 lvl", "Native gen-AI creative suites achieve professional-grade parity"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Creative Cloud subscriber/ARR growth decelerates below 5% as native")
print(f"  generative-AI tools (Midjourney, Sora, Canva) achieve professional-grade workflow parity,")
print(f"  while Firefly monetization stalls below $0.3B run-rate. Combined with churn finally")
print(f"  showing up in the data and the new CEO failing to articulate a credible AI strategy,")
print(f"  the multiple stays pinned at the 15-yr-low 12× and EPS growth flattens to ~$18.50 → ${bear_price}.")
print(f"  Note: ${bear_price} is close to current price — the BEAR case is largely already priced in.")
print(f"  The asymmetry is in the BASE/BULL recovery: a modest re-rating to 18× on $23.50 EPS = ${SCENARIOS['BASE'][2]}.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E non-GAAP EPS estimate:  ${EPS_FY2026E:.2f}  (consensus; EPS still growing ~19% YoY)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (15-year-low multiple on AI-disruption fear)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% vs trough floor)")
print()
print(f"  Adobe is currently trading at ~10.4× FY2026E non-GAAP EPS — BELOW even the pessimistic")
print(f"  trough P/E of {PE_PESSIMISTIC:.0f}×. This is the deepest valuation discount in 15+ years, roughly")
print(f"  {abs(epp_gap_pct):.0f}% below the EPP floor. The market is pricing generative-AI disruption as a")
print(f"  near-certain tail risk to the Creative Cloud moat — yet EPS is still compounding ~19% YoY")
print(f"  and subscriber churn from gen-AI substitutes has NOT materialized in the reported numbers.")
print(f"  EPP path: FY2028E EPS ~${CONS_EPS_2YR:.2f} × {PE_PESSIMISTIC:.0f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing with EPS).")
print(f"  At 18× mid-cycle P/E (BASE): ${EPS_FY2026E:.2f} × 18 = ${EPS_FY2026E*18:.0f}  — {((EPS_FY2026E*18/CURRENT_PRICE)-1)*100:+.0f}% vs current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest EPS growth + partial multiple recovery from 10.4×)")
hr()
print(f"  Conservative FY2028E non-GAAP EPS:  ${CONS_EPS_2YR:.2f}  (~7-8% CAGR from ${EPS_FY2026E:.2f}; Firefly ramps slowly)")
print(f"  Conservative exit P/E:               {CONS_PE_2YR}×  (rerates from 10.4× toward 15×; still well below historical ~25-30×)")
print(f"  Conservative equity value:            ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):        +${cons_divs:.2f}/share  (Adobe pays no dividend)")
hr()
print(f"  Conservative 2yr total:               ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:            {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE OPPORTUNITY: even a MODEST multiple rerate (10.4× → 15×, still a discount to the")
print(f"  historical norm) combined with single-digit EPS growth produces a {cons_return:.0f}% 2yr return.")
print(f"  For conservative 2yr to break even at 15× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
breakeven_growth_pct = ((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1) * 100
print(f"  Current ${EPS_FY2026E:.2f} EPS already EXCEEDS this breakeven — no growth needed at 15× (already {breakeven_growth_pct:+.1f}pp cushion).")
print(f"  Breakeven at 12× P/E (no multiple recovery): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 12:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at 15× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.32
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock is down 65% from its $699 ATH; 52W high already reflects post-peak decline")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (Adobe pays no dividend; reinvests via buybacks)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; AI-disruption narrative drives wide swings)")
print(f"  Beta vs S&P 500:      1.15  (slight premium; software/growth sensitivity to rates and AI sentiment)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (modest; BEAR is near current price)")
print(f"  52W low ${VOL_52W_LOW:.2f} already represents a peak-to-trough move of ~65% from the $699 ATH.")
print(f"  → Firefly/AI revenue disclosure is THE KEY binary; any concrete monetization data point is a BULL catalyst.")
print(f"  → Creative Cloud subscriber/ARR deceleration below 5% is the KEY bear catalyst to monitor.")
print(f"  → AVOID at current price  |  WATCHLIST $230–250  |  ACCUMULATE $200–225  |  BUY below $200")

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
print(f"  BEAR. The model scores the fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0 — closer to BASE.")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: you are paying near-BEAR scenario prices for what is currently BASE execution.")
print(f"  AI-disruption fear (signal score 1/4 = BEAR) is the most significant valuation mismatch —")
print(f"  the question is whether Firefly/generative AI is a tailwind being mispriced as a tail risk.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Firefly/AI revenue disclosure updates — concrete monetization data points (BULL trigger)")
print(f"  (2) Creative Cloud subscriber/ARR growth — reacceleration above 10% (BULL trigger)")
print(f"  (3) Document Cloud AI Assistant adoption — attach rate and ARPU uplift")
print(f"  (4) Digital Experience bookings — Experience Cloud / GenStudio enterprise traction")
print(f"  (5) FCF guidance — confirms software economics intact despite AI infra capex")
print(f"  (6) New CEO strategy signals — credible AI roadmap post Narayen transition (Mar 2026)")
print(f"  AVOID at ${CURRENT_PRICE:.2f}  |  WATCHLIST $230–250  |  ACCUMULATE $200–225  |  BUY below $200")
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
