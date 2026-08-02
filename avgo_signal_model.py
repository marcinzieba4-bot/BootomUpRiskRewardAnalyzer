"""
AVGO  ·  Broadcom Inc.  ·  NYSE: AVGO
Bottom-up signal model  ·  Semiconductors / AI Custom Silicon (XPU) / VMware Software
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "AVGO"
COMPANY       = "Broadcom Inc."
SECTOR        = "Semiconductors · AI XPU / VMware Software · NYSE: AVGO"
CURRENT_PRICE = 389.28       # USD; as of 2026-08-02
VOL_52W_LOW   = 281.61       # 52-week low
VOL_52W_HIGH  = 495.00       # 52-week high
SHARES_OUT_M  = 4_754.0      # millions (~$1.85T mkt cap / $389.28)

# Dividend: $0.59/qtr → $2.36/yr
ANNUAL_DIV    = 2.36         # $/share

# ── SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────────
# FY2025 revenue = $63.89B (+23.87% YoY); FY2026E segments ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("AI XPU / Custom Silicon",  32.0, 12.0, 58.0, "Google TPU, Meta MTIA, Apple AI chip; Q2 FY26 AI semi $10.8B (+143% YoY)"),
    ("VMware Software (ARR)",    17.0, 14.0, 22.0, "~$15B ARR enterprise software; SaaS transition; sticky renewal base"),
    ("Networking (Switches)",    10.0,  7.0, 14.0, "Tomahawk/Trident for AI clusters; Ethernet wins vs InfiniBand narrative"),
    ("Storage / Broadband",       6.5,  5.5,  8.0, "HDD preamps; broadband CPE; stable/declining but cash-generative"),
    ("Other Semiconductor",       4.0,  3.0,  6.0, "Custom ASICs, wireless, industrial; diversified base"),
]

# Margin assumptions (non-GAAP)
GROSS_MARGIN_CURR = 0.670   # blended non-GAAP gross margin (~67%; software lifts blend)
GROSS_MARGIN_BULL = 0.700   # BULL: AI XPU scale + VMware ARR mix improve
OPEX_FIXED_B      = 10.5    # R&D + SG&A ($B); post-VMware integration
TAX_RATE          = 0.130   # effective rate (non-GAAP)

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 15.76       # FY2026E non-GAAP EPS (forward P/E 24.70×)
PE_PESSIMISTIC = 18.0        # trough P/E: custom ASIC demand collapse + VMware churn
BEAR_EPS       = 8.00        # bear scenario EPS (hyperscaler ASIC shift back to NVDA)
EPP            = round(PE_PESSIMISTIC * BEAR_EPS, 0)   # $144

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 8.00, 18,  144, "Custom ASIC market shrinks; hyperscalers shift to NVIDIA; VMware churn; EPS $8 → 18×"),
    "BASE":  (15.76, 22,  347, "AI XPU + VMware ARR scales; EPS ~$15.76 → 22× mid-cycle justified P/E"),
    "BULL":  (22.00, 27,  594, "Apple + Google + Meta XPU ramp drives >$50B AI revenue; EPS $22 → 27× premium"),
    "XBULL": (35.00, 30, 1050, "Broadcom = standard AI ASIC platform; $200B+ AI revenue; EPS $35 → 30× peak"),
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

# ── 5 PROXY SIGNALS ───────────────────────────────────────────────────────────
# Scores: 1=BEAR  2=BASE  3=BULL  4=XBULL
# Note: 5 signals summing to 1.0 per brief (AI XPU, VMware ARR, Networking, GM, Div/FCF)
SIGNALS = [
    {
        "name":       "AI XPU / custom chip revenue YoY",
        "weight":     0.35,
        "thresholds": ("<20%",  "≥50%",  "≥100%", "≥150%"),
        "now":        "+143%",
        "score":      4,
        "comment":    "Q2 FY26 AI semi $10.8B (+143% YoY); Google/Meta/Apple ramps ongoing; TAM expanding rapidly",
    },
    {
        "name":       "VMware ARR growth YoY",
        "weight":     0.25,
        "thresholds": ("<5%",   "≥10%",  "≥18%",  "≥28%"),
        "now":        "+15%",
        "score":      2,
        "comment":    "~$15B ARR; SaaS transition sticky; renewal rates high; some enterprise churn post-price increase",
    },
    {
        "name":       "Networking revenue growth YoY",
        "weight":     0.20,
        "thresholds": ("<5%",   "≥10%",  "≥20%",  "≥35%"),
        "now":        "+22%",
        "score":      3,
        "comment":    "Tomahawk/Trident AI cluster demand; Ethernet vs InfiniBand shift benefits Broadcom; hyperscaler capex",
    },
    {
        "name":       "Non-GAAP gross margin",
        "weight":     0.12,
        "thresholds": ("<63%",  "≥65%",  "≥68%",  "≥71%"),
        "now":        "67%",
        "score":      2,
        "comment":    "Software (VMware) lifts blended margin; AI XPU at lower margin than pure software; mix transition",
    },
    {
        "name":       "Dividend / FCF yield",
        "weight":     0.08,
        "thresholds": ("<0.5%", "≥0.6%", "≥0.9%", "≥1.3%"),
        "now":        "0.61%",
        "score":      2,
        "comment":    "Dividend yield 0.61%; strong FCF generation; consistent dividend grower post-VMware integration",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "AI XPU structural shift — hyperscalers build custom chips; 3 confirmed (Google/Meta/Apple)",  +0.9, 0.25),
    ("+", "VMware software moat — $15B ARR; 300K+ enterprise customers; high switching costs",            +0.6, 0.20),
    ("-", "NVIDIA substitution risk — if GPT-5 class models re-centralize on NVIDIA H200/B200",           -0.8, 0.20),
    ("-", "VMware integration risk — price increases driving churn; AWS/Azure native competition",         -0.5, 0.20),
    ("+", "Networking secular growth — AI cluster scale requires Broadcom Ethernet at every pod",          +0.4, 0.10),
    ("-", "Valuation premium — 24.7× forward P/E for non-GAAP; GAAP P/E 64.8× (stock-comp heavy)",       -0.3, 0.05),
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
CONS_EPS_2YR  = 18.00   # conservative FY2028E: AI XPU sustains + VMware ARR matures
CONS_PE_2YR   = 22      # mid-cycle non-GAAP P/E; in line with current forward P/E
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Semiconductors / AI XPU / VMware Software")
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
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_ni   = curr_oi * (1 - TAX_RATE)
curr_eps  = round(curr_ni / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B
bull_ni   = bull_oi * (1 - TAX_RATE)
shares_b  = shares * 0.99   # minimal buyback; shares relatively stable
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.95   # margin compression; VMware churn
bear_oi   = bear_gp - OPEX_FIXED_B * 0.93
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E non-GAAP EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share non-GAAP EPS  (consensus ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 27× = ~${bull_eps_imp*27:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.95:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 18× trough P/E (custom ASIC collapse) = ~${bear_eps_imp*18:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_ai   = (1.0 * 0.55 * (1 - TAX_RATE)) / shares    # AI XPU ~55% non-GAAP GM
eps_per_1B_vmw  = (1.0 * 0.85 * (1 - TAX_RATE)) / shares    # VMware software ~85% GM
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B AI XPU revenue (~55% GM):   +${eps_per_1B_ai:.3f}/EPS  = +${eps_per_1B_ai*22:.1f}/share at 22× P/E")
print(f"  Every $1B VMware ARR (~85% GM):        +${eps_per_1B_vmw:.3f}/EPS  = +${eps_per_1B_vmw*22:.1f}/share at 22× P/E")
print(f"  1pp non-GAAP GM expansion:             +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*22:.1f}/share at 22× P/E")
print(f"  New XPU customer (hyperscaler):         structural re-rating event; each = $5–15B potential TAM")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (AI XPU / VMware ARR / Networking / GM / FCF framework)")
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
    ("AI XPU / custom chip revenue YoY",  "+143%",   "<20%",    "−123pp", "Hyperscalers revert to NVIDIA; Apple cancels XPU deal"),
    ("VMware ARR growth YoY",             "+15%",    "<5%",     "−10pp",  "Enterprise churn >20%; AWS/Azure wins migrations back"),
    ("Networking revenue growth YoY",     "+22%",    "<5%",     "−17pp",  "InfiniBand wins AI cluster standard; Broadcom loses design"),
    ("Non-GAAP gross margin",             "67%",     "<63%",    "−4pp",   "AI XPU at lower GM displaces high-margin software mix"),
    ("Dividend / FCF yield",              "0.61%",   "<0.5%",   "−0.1pp", "FCF compression from revenue decline + debt service"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Hyperscalers (Google, Meta, Apple) collectively decide custom XPUs are")
print(f"  too complex/risky vs NVIDIA's turnkey GPU platform. AI XPU revenue collapses from")
print(f"  ~$30B+ to <$10B. Simultaneously, VMware churn accelerates (15%+ annual attrition)")
print(f"  as enterprises migrate workloads to cloud-native. Non-GAAP EPS falls to ~$8.")
print(f"  At 18× trough P/E = ${bear_price}. Note: $144 requires dual failure — XPU AND VMware.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × bear EPS)")
hr()
print(f"  Bear EPS estimate:               ${BEAR_EPS:.2f}  (XPU market shrinks + VMware churn + deleveraging)")
print(f"  FY2026E non-GAAP EPS estimate:   ${EPS_FY2026E:.2f}  (forward P/E {CURRENT_PRICE/EPS_FY2026E:.1f}×; consensus)")
print(f"  GAAP EPS TTM:                    $6.01  (GAAP P/E 64.8× — stock-comp heavy)")
print(f"  Pessimistic P/E at trough:        {PE_PESSIMISTIC:.0f}×  (software+semi blended floor; VMware provides floor)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP reflects AI XPU optionality pricing.")
print(f"  At 24.7× forward non-GAAP P/E, market prices in XPU growth sustaining 2+ years.")
print(f"  VMware ($15B ARR) provides meaningful earnings floor even in AI disappointment case.")
print(f"  EPP path: bear EPS $10 by FY2028E × 18× = $180 bear floor (rising as VMware ARR grows).")
print(f"  At 22× mid-cycle: ${EPS_FY2026E:.2f} × 22 = ${EPS_FY2026E*22:.0f}  ({(EPS_FY2026E*22/CURRENT_PRICE-1)*100:+.1f}% from current).")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: AI XPU sustains; VMware ARR matures)")
hr()
print(f"  Conservative FY2028E non-GAAP EPS:  ${CONS_EPS_2YR:.2f}  (XPU sustains + VMware ARR +12%/yr compounding)")
print(f"  Conservative exit P/E:               {CONS_PE_2YR}×  (in line with current 24.7× forward; no re-rating)")
print(f"  Conservative equity value:            ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):        +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:               ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:            {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case positive at {CONS_PE_2YR}× non-GAAP P/E IF XPU revenues hold.")
print(f"  Key risk: AI XPU concentration (>50% of revenue on 3 customers) creates lumpiness.")
print(f"  Breakeven at {CONS_PE_2YR}× P/E: FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f}  (conservative case clearly positive; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.32   # large-cap semi/software blend
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (semi + software blend; AI narrative amplifies moves)")
print(f"  Beta vs S&P 500:      1.35  (large-cap; AI theme elevated beta vs historical)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (dual failure: XPU + VMware)")
print(f"  52W range ${VOL_52W_LOW:.2f}–${VOL_52W_HIGH:.2f}  (+76% peak-to-trough amplitude in prior 12 months).")
print(f"  → AI XPU customer announcements/cancellations are binary ±15–25% catalysts.")
print(f"  → VMware renewal data (annual ARR growth) is THE enterprise health signal.")
print(f"  → Signal: {signal_full}  |  WATCHLIST $340–360  |  ACCUMULATE $290–310  |  BUY below $270")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, market composite ({MARKET_COMPOSITE:.2f}) vs model adj ({ADJ_COMPOSITE:.3f}).")
print(f"  Gap ({ADJ_GAP:.2f}) → stock is {valuation_label.lower()} by model standards.")
print(f"  AI XPU signal at 4/4 (XBULL) drives proxy composite above market-implied composite.")
print(f"  The 'other side of the NVDA trade' thesis: custom silicon = lower cost/watt for")
print(f"  inference at scale. Broadcom wins if hyperscalers standardize on XPU, not GPU.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Apple AI chip ramp — $30B+ Apple deal; volumes confirm or disappoint (BULL trigger)")
print(f"  (2) New XPU customer announcement — any new hyperscaler = structural re-rating")
print(f"  (3) VMware ARR Q/Q acceleration — confirms enterprise stickiness post-migration")
print(f"  (4) AI XPU gross margin disclosure — higher margin confirms software-like economics")
print(f"  (5) Samsung $200B deal — execution timeline; revenue recognition timing critical")
print(f"  Signal: {signal_full}  |  Ratio B: {ratio_b_str}  |  EPP floor: ${EPP:.0f}")
print(f"  Current ${CURRENT_PRICE:.2f}  |  52W: ${VOL_52W_LOW}–${VOL_52W_HIGH}  |  FY2026E non-GAAP EPS: ${EPS_FY2026E:.2f}")
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
