"""
QCOM  ·  QUALCOMM Incorporated  ·  NASDAQ: QCOM
Bottom-up signal model  ·  Mobile Chips / Automotive / IoT / Edge AI / Hyperscaler Silicon
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "QCOM"
COMPANY       = "QUALCOMM Incorporated"
SECTOR        = "Semiconductors · Snapdragon · Automotive · IoT/Edge AI · Hyperscaler Silicon · NASDAQ: QCOM"
CURRENT_PRICE = 238.16      # USD; surged +11.6% on Automotive/Edge AI momentum
VOL_52W_LOW   = 125.00      # post-Apple-modem-exit overhang trough
VOL_52W_HIGH  = 250.00      # recent highs on diversification re-rating
SHARES_OUT_M  = 1_080.0     # millions; steady buyback program

# Dividend: long growth streak; ~1.4% yield at current price
ANNUAL_DIV    = 3.40        # $/share annualized

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("QCT - Handsets (Snapdragon)", 16.5, 13.0, 19.5, "Android flagship/premium share gains; Apple modem now ~0% of mix"),
    ("QCT - Automotive (ADAS/Digital Chassis)", 4.8, 3.5, 7.5, "Snapdragon Digital Chassis design-win pipeline; >$5B annualized run rate"),
    ("QCT - IoT / Edge AI", 6.0, 4.5, 8.5, "On-device AI inference, industrial, XR, PC; edge AI silicon ramp"),
    ("QTL - Licensing", 5.6, 5.0, 6.2, "Stable royalty base; 5G/6G IP portfolio; durable high-margin annuity"),
    ("Hyperscaler Custom AI Silicon", 0.5, 0.0, 3.0, "Custom AI inference chips; Dec 2026 tape-out milestone; pre-revenue optionality"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.560   # blended gross margin FY2026E (~56%; QTL mix supports blend)
GROSS_MARGIN_BULL = 0.585   # BULL: Automotive/Edge AI/QTL mix shift lifts blend further
OPEX_FIXED_B      = 9.0     # R&D + SG&A ($B); elevated R&D for hyperscaler silicon program
TAX_RATE          = 0.135   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 9.40        # FY2026E adj EPS post-Apple-modem-exit step-down (was $12.03)
PE_PESSIMISTIC = 13.0        # trough P/E: reflects Apple-exit overhang skepticism
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $122

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 8.00, 13,  104, "Automotive momentum stalls; Android share loss to MediaTek; hyperscaler program slips; EPS $8.00 → 13×"),
    "BASE":  ( 9.40, 18,  169, "Apple-exit step-down stabilizes; Automotive >$5B run rate sustains; QTL stable; EPS $9.40 → 18×"),
    "BULL":  (12.00, 22,  264, "Automotive +40-50% YoY continues; Edge AI scales; hyperscaler tape-out on track; EPS $12.00 → 22×"),
    "XBULL": (15.50, 26,  403, "Hyperscaler custom AI silicon becomes meaningful revenue line; Automotive >$8B; EPS $15.50 → 26×"),
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
        "name":       "Automotive segment revenue growth (annualized run rate)",
        "weight":     0.25,
        "thresholds": ("<10%",   "≥25%",  "≥38%",   "≥50%"),
        "now":        "+44%",
        "score":      3,
        "comment":    "Snapdragon Digital Chassis design wins ramping; annualized run rate now >$5B; +38-50% YoY",
    },
    {
        "name":       "Non-Apple smartphone (Android) Snapdragon share & ASP growth",
        "weight":     0.20,
        "thresholds": ("<0%",    "≥3%",   "≥7%",    "≥12%"),
        "now":        "+6%",
        "score":      2,
        "comment":    "Premium Android share holding; ASP growth steady; Samsung/Xiaomi flagship wins; MediaTek competitive at mid-tier",
    },
    {
        "name":       "IoT / Edge AI revenue growth",
        "weight":     0.15,
        "thresholds": ("<0%",    "≥5%",   "≥12%",   "≥20%"),
        "now":        "+10%",
        "score":      2,
        "comment":    "On-device AI inference demand building; PC/XR/industrial diversification continuing steadily",
    },
    {
        "name":       "Hyperscaler custom AI inference chip pipeline (Dec 2026 tape-out)",
        "weight":     0.20,
        "thresholds": ("delayed","on-track","sampling","design-win confirmed"),
        "now":        "on-track",
        "score":      2,
        "comment":    "Dec 2026 tape-out milestone tracking on schedule; commercial revenue still pre-launch optionality",
    },
    {
        "name":       "QTL licensing revenue stability",
        "weight":     0.10,
        "thresholds": ("<-5%",   "≥-2%",  "≥0%",    "≥+3%"),
        "now":        "+1%",
        "score":      3,
        "comment":    "Royalty base stable; 5G/6G IP portfolio renewals on track; high-margin annuity intact",
    },
    {
        "name":       "Diversification away from Apple modem revenue",
        "weight":     0.10,
        "thresholds": ("≥15%",   "≥5%",   "≥1%",    "0%"),
        "now":        "0%",
        "score":      4,
        "comment":    "Apple modem revenue now fully transitioned to ~0%; FY2026 EPS step-down is the one-time optical comp reset",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Automotive design-win pipeline — Snapdragon Digital Chassis multi-year backlog; >$5B run rate", +0.7, 0.25),
    ("+", "Edge AI / IoT diversification — on-device inference becoming structural demand driver",          +0.5, 0.20),
    ("+", "Hyperscaler custom silicon optionality — Dec 2026 tape-out; new TAM if commercialized",          +0.5, 0.15),
    ("-", "Apple-exit comp reset — FY2026 EPS $12.03→$9.40 is one-time step-down, but near-term optics weigh on sentiment", -0.4, 0.20),
    ("-", "Android OEM competitive pressure — MediaTek share gains at mid-tier; margin pressure risk",      -0.4, 0.10),
    ("+", "QTL annuity — high-margin licensing base provides earnings floor independent of chip cycles",    +0.3, 0.10),
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
CONS_EPS_2YR  = 11.00   # conservative FY2028E: ~$13 BULL path discounted; Apple-exit comp normalizes
CONS_PE_2YR   = 17      # modest rerating from depressed ~25× FY2026E (on $9.40) toward 17× on normalized EPS
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Mobile Chips / Automotive / IoT / Edge AI / Hyperscaler Silicon")
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
shares_b  = shares * 0.96   # ~2%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift / pricing pressure
bear_oi   = bear_gp - OPEX_FIXED_B * 0.98           # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (target ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 22× = ~${bull_eps_imp*22:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 13× trough P/E (Apple-exit overhang) = ~${bear_eps_imp*13:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Automotive revenue:    +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*18:.2f}/share at 18× P/E")
print(f"  Every $1B IoT/Edge AI revenue:    +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*18:.2f}/share at 18× P/E")
print(f"  1pp GM expansion (mix/pricing):  +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*18:.2f}/share at 18× P/E")
print(f"  1% buyback (~11M shares):         +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Automotive growth / Edge AI / hyperscaler silicon / QTL framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<58}  {'BEAR':>6}  {'BASE':>6}  {'BULL':>6}  {'XBULL':>10}  {'NOW':>9}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<58}  {ths[0]:>6}  {ths[1]:>6}  {ths[2]:>6}  {ths[3]:>10}  {s['now']:>9}  {lbl}  {b}")

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
print(f"  {'Signal':<52}  {'Current':>10}  {'Bear val':>10}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Automotive revenue growth",          "+44%",     "<10%",    "−34pp",  "Design-win momentum stalls; OEM platform delays push out revenue recognition"),
    ("Android Snapdragon share/ASP",       "+6%",      "<0%",     "−6pp",   "MediaTek gains share at premium tier; ASP compression on flagship Android"),
    ("IoT/Edge AI revenue growth",         "+10%",     "<0%",     "−10pp",  "Edge AI demand fails to materialize; PC/XR ramp disappoints"),
    ("Hyperscaler chip pipeline",          "on-track", "delayed", "slip",   "Dec 2026 tape-out delayed or program cancelled by hyperscaler partner"),
    ("QTL licensing revenue",              "+1%",      "<-5%",    "−6pp",   "Major licensee dispute or non-renewal of 5G IP agreement"),
    ("Blended gross margin",               "56.0%",    "<52%",    "−4pp",   "Pricing pressure across QCT segments; mix shift to lower-margin IoT"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Automotive design-win momentum stalling combined with Android OEM share")
print(f"  loss to MediaTek at the mid-tier and a delayed/cancelled hyperscaler custom AI chip")
print(f"  program would remove the three pillars of the post-Apple diversification thesis.")
print(f"  EPS would compress toward ~$8.00 and the multiple would re-derate to a 13× trough,")
print(f"  reflecting renewed concern that QCOM is structurally ex-growth without Apple modem revenue.")
print(f"  Note: QTL licensing ($5.6B annuity) provides a durable earnings floor even in BEAR.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (post-Apple-modem-exit step-down from $12.03)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (Apple-exit overhang skepticism floor)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  At ${CURRENT_PRICE:.2f} on FY2026E EPS of ${EPS_FY2026E:.2f}, QCOM trades at ~{CURRENT_PRICE/EPS_FY2026E:.1f}×.")
print(f"  This multiple looks elevated only because FY2026E EPS is artificially depressed by the")
print(f"  one-time Apple-modem-exit step-down ($12.03 → $9.40) — a 100% Apple-driven optical")
print(f"  decline, NOT a fundamental deterioration of the underlying business.")
print(f"  EPP path: FY2028E EPS ~$13.00 × {PE_PESSIMISTIC:.0f}× = ${13.00*PE_PESSIMISTIC:.0f} floor as the Apple-exit comp normalizes.")
print(f"  At 18× mid-cycle P/E on FY2028E EPS: $13.00 × 18 = ${13.00*18:.0f}  — close to the BASE target.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: Apple-exit comp normalizes; Automotive/Edge AI scale)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (Apple-exit comp base normalizes; Automotive/Edge AI growth)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (modest rerating on normalized, diversified earnings base)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: does Automotive (>$5B run rate, +38-50% YoY) + Edge AI + hyperscaler")
print(f"  custom silicon optionality justify a re-rating from the current ~25× depressed FY2026E")
print(f"  multiple toward a normalized ~17-18× on FY2028E EPS of ~$13?")
print(f"  Breakeven at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~${((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth from FY2026E — plausible by FY2028E as Apple comp normalizes.")
print(f"  Breakeven at 22× P/E (BULL multiple): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 22:.2f}")
print(f"  ADD AGGRESSIVELY on pullback to $185-210; HOLD existing positions near current price.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.34
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock recently surged +11.6% to ${CURRENT_PRICE:.2f} on Automotive/Edge AI momentum")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (semiconductor cycle + diversification narrative volatility)")
print(f"  Beta vs S&P 500:      1.15  (semiconductor mega-cap; AI/Automotive cycle amplifier)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe; multi-pillar thesis failure)")
print(f"  → Hyperscaler custom AI chip Dec 2026 tape-out is THE KEY binary catalyst over next 6 months.")
print(f"  → Automotive quarterly revenue trajectory is the clearest near-term confirmation signal.")
print(f"  → AVOID above $250  |  WATCHLIST $210-238 (HOLD existing)  |  ACCUMULATE/ADD $185-210  |  BUY below $160")

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
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The gap ({ADJ_GAP:.2f}) indicates the stock is")
print(f"  {valuation_label.lower()} by model standards. The post-Apple diversification thesis — Automotive,")
print(f"  Edge AI, and hyperscaler custom silicon — is the primary driver of any re-rating from the")
print(f"  optically depressed FY2026E EPS base.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Hyperscaler custom AI inference chip — Dec 2026 tape-out updates (BULL/XBULL trigger)")
print(f"  (2) Automotive segment quarterly revenue growth — confirm >$5B run rate sustaining +38-50% YoY")
print(f"  (3) Snapdragon flagship Android design wins — Samsung/Xiaomi/OEM premium-tier share")
print(f"  (4) IoT/Edge AI revenue trajectory — on-device inference demand inflection")
print(f"  (5) FY2027/2028 EPS guidance updates as Apple-exit comp normalizes ($9.40 → ~$13)")
print(f"  AVOID above $250  |  WATCHLIST $210-238 (HOLD existing)  |  ACCUMULATE/ADD $185-210  |  BUY below $160")
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
