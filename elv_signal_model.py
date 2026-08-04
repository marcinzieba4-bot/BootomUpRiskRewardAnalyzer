"""
ELV  ·  Elevance Health, Inc.  ·  NYSE: ELV
Bottom-up signal model  ·  Anthem/BCBS Commercial & Medicaid / Medicare Advantage / Carelon Health Services & PBM
Date: 2026-08-04
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "ELV"
COMPANY       = "Elevance Health, Inc."
SECTOR        = "Managed Care · Anthem/BCBS Commercial · Medicaid · Medicare Advantage · Carelon (Health Services/PBM) · NYSE: ELV"
CURRENT_PRICE = 382.77      # USD; close 2026-08-03
VOL_52W_LOW   = 273.71      # USD
VOL_52W_HIGH  = 436.24      # USD
SHARES_OUT_M  = 216.9       # millions
ANNUAL_DIV    = 6.88        # $/share; long dividend-growth track record

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# Q2 2026 actual (reported Jul 15): adj EPS $7.45 vs consensus $6.21 — a big beat; revenue
# $49.8B vs $48.63B consensus. FY2026 guidance RAISED to adj EPS "at least $27.00" (from
# $25.50). Sector-wide MA cost pressure confirmed: medical loss ratio hit 93.5%; management
# is guiding to a deliberate "high-teens %" MA membership decline in 2026 as a repricing/exit
# strategy (the same playbook UNH is running), targeting a benefit expense ratio ~90.2%.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Health Benefits - Commercial (Anthem/BCBS)", 62.0, 58.5,  66.0, "Self-funded ASO + fully-insured commercial; stable membership, mid-single-digit premium growth"),
    ("Health Benefits - Medicaid",                  33.0, 29.0,  36.0, "2026-2027 rate re-pricing showing early evidence of working, given the Q2 beat"),
    ("Health Benefits - Medicare (incl. MA)",       30.0, 26.0,  34.0, "Deliberate high-teens% MA membership reduction as a repricing/exit strategy — mirrors the UNH playbook"),
    ("Carelon (Health Services + CarelonRx PBM)",   58.0, 52.0,  66.0, "Fastest-growing segment; CarelonRx PBM scaling + Carelon Health value-based care; high-margin external growth"),
]

# Net-margin-based bridge
NET_MARGIN_CURR = 0.0320   # FY2026E; reconciles to raised guidance floor
NET_MARGIN_BEAR = 0.0275   # BEAR: MLR deteriorates further, repricing lags cost trend
NET_MARGIN_BULL = 0.0365   # BULL: repricing succeeds, Carelon mix shift expands margin

# ── MEDICAID/MA REPRICING TRACKER (the Elevance-specific angle) ───────────────
Q2_2026_REVENUE_B          = 49.8    # $B, Q2 2026 actual reported revenue
Q2_2026_ADJ_EPS            = 7.45    # $ adjusted EPS, Q2 2026 (big beat vs $6.21 consensus)
MLR_PCT                    = 93.5    # % medical loss ratio, confirming sector-wide MA cost pressure
MA_MEMBERSHIP_DECLINE_PCT  = "high-teens"  # % 2026 deliberate MA membership reduction
FY2026_GUIDANCE_EPS_FLOOR  = 27.00    # $, raised FY2026 guidance ("at least")
STOCK_MOVE_FROM_JUNE_LOW_PCT = round((CURRENT_PRICE - 352.00) / 352.00 * 100, 1)  # move since last refresh

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 27.00       # FY2026E adj EPS (raised guidance floor, "at least $27.00")
PE_PESSIMISTIC = 10.0        # pessimistic P/E: below the current ~14.2× multiple; Medicaid/MA-discount floor
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (21.00, 10,  210, "Medicaid rate re-pricing stalls despite the Q2 beat; MA cost trend reaccelerates further; Carelon growth slows; EPS $21.00 → 10× = $210"),
    "BASE":  (27.00, 14.18, 383, "FY2026 raised guidance floor (≥$27.00) holds; Medicaid repricing continues showing progress; deliberate MA membership shedding continues restoring margin; EPS $27.00 → 14.2× = $383"),
    "BULL":  (34.00, 15,  510, "Medicaid 2026-2027 rate cycle fully restores margin to historical range; MA cost trend normalizes; CarelonRx PBM scaling drives margin mix improvement; EPS $34.00 → 15× = $510"),
    "XBULL": (39.00, 17,  663, "Full earnings power restoration; Medicaid/MA margins both above target; Carelon becomes a $70B+ external-revenue platform; multiple re-rates toward historical MCO premium; EPS $39.00 → 17× = $663"),
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
        "name":       "Medicaid medical loss ratio (MLR) trend / rate re-pricing",
        "weight":     0.25,
        "thresholds": ("worsening, rates lag", "stable, rates flat to trend", "rates ahead of trend", "margin restored to target"),
        "now":        "rates ahead of trend",
        "score":      3,
        "comment":    "The Q2 beat (adj EPS $7.45 vs $6.21 consensus) is real evidence the 2026-2027 repricing cycle is landing ahead of expectations",
    },
    {
        "name":       "Medicare Advantage cost trend / deliberate membership shedding",
        "weight":     0.25,
        "thresholds": ("trend reaccelerates, sanctions extend", "trend stable, deliberate shedding", "trend moderating, sanctions narrowing", "trend normalized, sanctions lifted"),
        "now":        "trend stable, deliberate shedding",
        "score":      2,
        "comment":    "MLR at 93.5% confirms sector-wide MA cost pressure; management is deliberately shedding high-teens% of MA membership to restore margin — the same playbook UNH is running",
    },
    {
        "name":       "Carelon (CarelonRx PBM + Health Services) growth",
        "weight":     0.20,
        "thresholds": ("<5%",  "≥8%",  "≥12%",   "≥18%"),
        "now":        "+11%",
        "score":      3,
        "comment":    "Carelon is ELV's Optum analogue — CarelonRx PBM scaling with external clients, Carelon Health value-based care expanding",
    },
    {
        "name":       "Commercial segment stability (Anthem/BCBS ASO/fully-insured)",
        "weight":     0.10,
        "thresholds": ("membership declining", "flat", "low-single-digit growth", "mid-single-digit+ growth"),
        "now":        "low-single-digit growth",
        "score":      2,
        "comment":    "Largest, most stable segment; ASO membership growth offsetting modest fully-insured pressure",
    },
    {
        "name":       "FY2026 guidance credibility / EPS trajectory",
        "weight":     0.10,
        "thresholds": ("guidance cut again", "guidance held flat", "guidance reaffirmed/raised modestly", "guidance raised meaningfully"),
        "now":        "guidance raised meaningfully",
        "score":      4,
        "comment":    "FY2026 guidance raised to ≥$27.00 from $25.50 after a beat-and-raise Q2 — real credibility rebuild after the 2025 reset",
    },
    {
        "name":       "Balance sheet / capital return capacity",
        "weight":     0.10,
        "thresholds": ("<A-",  "A to A+",  "AA-",   "AA"),
        "now":        "A",
        "score":      3,
        "comment":    "Investment-grade with solid free cash flow generation; dividend maintained through the 2025 reset",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("-", "Medicaid repricing execution risk — the Q2 beat is one quarter of evidence, not yet a full-cycle confirmation", -0.4, 0.25),
    ("-", "MA cost-trend overhang — industry-wide MA pressure (MLR 93.5%) requires continued deliberate membership shedding", -0.4, 0.20),
    ("+", "No DOJ criminal overhang — unlike UNH, ELV's regulatory issues are administrative (CMS sanctions/RADV), not a criminal risk-adjustment probe", +0.5, 0.15),
    ("+", "Carelon diversification — fast-growing, high-margin PBM/health-services platform reduces pure managed-care concentration", +0.5, 0.20),
    ("+", "Second-largest BCBS-affiliated commercial franchise — scale moat in core commercial/ASO business provides earnings stability", +0.3, 0.10),
    ("+", "Dividend maintained through the reset — signals management confidence in underlying earnings power", +0.3, 0.10),
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
CONS_EPS_2YR  = 31.00   # FY2028E conservative: ~7%/yr off FY2026E, gradual Medicaid/MA margin recovery
CONS_PE_2YR   = 13      # a modest compression from the current ~14.2×
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Anthem/BCBS Commercial / Medicaid / Medicare Advantage / Carelon")
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
print(f"  Q2 2026 actual: revenue ${Q2_2026_REVENUE_B:.1f}B, adj EPS ${Q2_2026_ADJ_EPS:.2f} (big beat vs $6.21 consensus), MLR {MLR_PCT:.1f}%")
print()

# EPS bridge (net-margin based)
shares    = SHARES_OUT_M / 1000
curr_net  = curr_total * NET_MARGIN_CURR
curr_eps  = round(curr_net / shares, 2)

bull_net     = bull_total * NET_MARGIN_BULL
bull_eps_imp = round(bull_net / shares, 2)

bear_net     = bear_total * NET_MARGIN_BEAR
bear_eps_imp = round(bear_net / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {NET_MARGIN_CURR*100:.2f}% net margin")
print(f"  ÷ {shares:.4f}B shares  =  ${curr_eps:.2f}/share  (guidance ≥${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {NET_MARGIN_BULL*100:.2f}% net margin")
print(f"  ÷ {shares:.4f}B shares  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {NET_MARGIN_BEAR*100:.2f}% net margin (repricing stalls + MA cost trend reaccelerates)")
print(f"  ÷ {shares:.4f}B shares  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# MEDICAID/MA REPRICING TRACKER
print()
print(f"  MEDICAID/MA REPRICING TRACKER  (the Elevance-specific angle):")
print(f"  Q2 2026 revenue / adj EPS:                   ${Q2_2026_REVENUE_B:.1f}B / ${Q2_2026_ADJ_EPS:.2f}  (big beat)")
print(f"  Medical loss ratio (MLR):                     {MLR_PCT:.1f}%")
print(f"  2026 MA membership reduction (deliberate):     {MA_MEMBERSHIP_DECLINE_PCT}%")
print(f"  FY2026 guidance:                                adj EPS ≥${FY2026_GUIDANCE_EPS_FLOOR:.2f}  (raised from $25.50)")
print(f"  Stock move since last refresh (Jun 10):        +{STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}%")
print()
print(f"  ELV is running the same playbook as UNH: deliberately shedding unprofitable MA membership")
print(f"  while repricing Medicaid contracts, and the Q2 beat-and-raise is the first hard evidence it's")
print(f"  working. Unlike UNH, ELV carries no DOJ criminal overhang — its regulatory issues (CMS")
print(f"  sanctions/RADV) are administrative, a meaningfully lower tail risk.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = 1.0 * NET_MARGIN_CURR / shares
eps_per_10bps_margin = curr_total * 0.001 / shares   # 0.1pp of net margin — a more realistic increment for a ~3% margin insurer
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at {NET_MARGIN_CURR*100:.1f}% margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*14.18:.2f}/share at 14.2× P/E")
print(f"  Every 0.1pp net margin change (MLR-equivalent): ∓${eps_per_10bps_margin:.3f}/EPS  = ∓${eps_per_10bps_margin*14.18:.2f}/share at 14.2× P/E")
print(f"  Every 1 turn of P/E:                          ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Medicaid repricing / MA cost trend / Carelon growth / capital strength framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>5}  {'BASE':>5}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>6}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>5}  {ths[1]:>5}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>6}  {lbl}  {b}")
    print(f"    {s['comment']}")

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
print(f"  {'Signal':<52}  {'Current':>16}  {'Bear val':>9}  Trigger")
hr()
bear_triggers = [
    ("Medicaid MLR / rate re-pricing",     "ahead of trend", "rates lag trend", "State contracts re-price slower than acuity-driven cost trend after all"),
    ("MA cost trend",                      "stable, shedding", "reaccelerates", "MA utilization trend reaccelerates faster than deliberate membership shedding can offset"),
    ("Carelon growth",                     "+11%",   "<5%",    "CarelonRx PBM client losses or Carelon Health margin compression"),
    ("Commercial membership",              "low-single-digit growth", "declining", "Employer groups shift to competitors amid premium increases"),
    ("FY2026 guidance",                    "raised (≥$27.00)", "cut again", "Q3/Q4 2026 prints reveal the Q2 beat was a one-off, forcing a reset"),
    ("Net margin",                         "3.2%",   "<2.5%",  "Combined Medicaid/MA cost pressure outpaces repricing across the book"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>16}  {bear_v:>9}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the Q2 beat proves to be a one-off rather than the start of a durable repricing")
print(f"  cycle — Medicaid rates lag acuity-driven cost trend after all, MA cost trend reaccelerates")
print(f"  faster than the deliberate membership shedding can offset, and Carelon growth slows.")
print(f"  Note: ${bear_price} is NOT necessarily permanent impairment — ELV remains the #2 BCBS-affiliated")
print(f"  insurer with a fast-growing Carelon platform and no DOJ-criminal overhang.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:       ${EPS_FY2026E:.2f}  (raised guidance floor)")
print(f"  Pessimistic P/E:                 {PE_PESSIMISTIC:.1f}×  (below the current ~14.2× multiple; Medicaid/MA-discount floor)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  ELV trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS ${EPS_FY2026E:.2f} — a real re-rating from its 2025-reset")
print(f"  trough multiple, driven by the Q2 beat-and-raise. The Medicaid repricing cycle and MA cost")
print(f"  trend are both showing early evidence of working, but one strong quarter isn't a full cycle.")
print(f"  At 15× mid-cycle P/E (repricing fully confirmed): ${EPS_FY2026E:.2f} × 15 = ${EPS_FY2026E*15:.0f}  — {(EPS_FY2026E*15/CURRENT_PRICE-1)*100:+.0f}% vs current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: gradual Medicaid/MA margin normalization continues)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (~7%/yr as Medicaid rate re-pricing lands and MA cost trend stabilizes)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (a modest compression from the current ~14.2×)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: ELV's Q2 beat-and-raise is genuinely encouraging, but the Medicaid/MA")
print(f"  repricing cycle needs several more quarters of confirmation before the multiple can re-rate")
print(f"  meaningfully further. Carelon remains the reliable diversification ballast in the meantime.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.28
beta        = 0.65
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock is up {STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}% since the last refresh (Jun 10) on the Q2 beat-and-raise")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  maintained/growing through the 2025 reset)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; Medicaid/MA cost-trend prints drive large moves)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (historically defensive, now elevated idiosyncratic MCO-sector risk)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (plausible on a Medicaid-repricing-failure + MA-cost-trend-shock scenario)")
print(f"  → Medicaid 2026-2027 rate re-pricing cadence over the next few quarters is THE KEY signal.")
print(f"  → MA cost trend + deliberate membership shedding pace are the KEY ongoing drivers.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $340  |  Trim above $430")

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
print(f"  {'ABOVE' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'BELOW'} the model's adj composite ({ADJ_COMPOSITE:.3f}). The gap ({ADJ_GAP:+.2f}) indicates the stock is")
print(f"  {valuation_label.lower()} by model standards. In plain terms: the Q2 beat-and-raise is genuine progress on")
print(f"  Medicaid repricing, and ELV's lack of a DOJ-style criminal overhang is a real differentiator")
print(f"  vs UNH — but one strong quarter doesn't yet confirm the full multi-year repricing cycle.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Medicaid 2026-2027 rate re-pricing cadence — confirming the Q2 beat wasn't a one-off")
print(f"  (2) Medicare Advantage cost trend trajectory — quarterly MLR prints vs deliberate membership shedding")
print(f"  (3) CMS star-rating/RADV sanction resolution — re-enabling MA new-member enrollment growth")
print(f"  (4) Carelon (CarelonRx PBM + Health Services) growth — external client wins and margin mix shift")
print(f"  (5) FY2026 guidance cadence — credibility rebuild continuing after the 2025 reset")
print(f"  (6) Dividend sustainability — ${ANNUAL_DIV:.2f}/share maintained/growing through the reset")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $340  |  Trim above $430")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.1f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}")
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
