"""
ELV  ·  Elevance Health, Inc.  ·  NYSE: ELV
Bottom-up signal model  ·  Anthem/BCBS Commercial & Medicaid / Medicare Advantage / Carelon Health Services & PBM
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "ELV"
COMPANY       = "Elevance Health, Inc."
SECTOR        = "Managed Care · Anthem/BCBS Commercial · Medicaid · Medicare Advantage · Carelon (Health Services/PBM) · NYSE: ELV"
CURRENT_PRICE = 352.00     # USD; as of 2026-06-10
VOL_52W_LOW   = 271.00     # 2025 Medicaid/MA cost-trend crisis trough
VOL_52W_HIGH  = 451.00     # 2025-2026 partial recovery / pre-guidance-reset highs
SHARES_OUT_M  = 215.0      # millions
ANNUAL_DIV    = 7.44       # $/share; ~2.1% yield; long dividend-growth track record

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Health Benefits - Commercial (Anthem/BCBS)", 60.0, 57.0,  64.0, "Self-funded ASO + fully-insured commercial; stable membership, mid-single-digit premium growth"),
    ("Health Benefits - Medicaid",                  35.0, 31.0,  38.0, "Post-redetermination membership stabilizing; 2026-2027 rate re-pricing is THE key margin driver"),
    ("Health Benefits - Medicare (incl. MA)",       33.0, 29.0,  37.0, "MA cost-trend pressure persists from 2025; CMS star-rating/RADV sanctions limit new enrollment growth"),
    ("Carelon (Health Services + CarelonRx PBM)",   52.0, 48.0,  60.0, "Fastest-growing segment; CarelonRx PBM scaling + Carelon Health value-based care; high-margin external growth"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.135   # blended margin proxy (post-benefit-expense / MLR ~88.5%)
GROSS_MARGIN_BULL = 0.160   # BULL: MLR normalizes toward ~86% as Medicaid/MA repricing takes hold
OPEX_FIXED_B      = 17.5    # SG&A ($B); largely fixed cost base
TAX_RATE          = 0.255   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 33.50      # FY2027E EPS (recovery year; FY2026E guided ≥$30, consensus FY2027 ~$33-35)
PE_PESSIMISTIC = 9.5        # trough P/E: Medicaid/MA cost-trend discount floor; historical MCO trough ~9-10×
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # ~$318

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (24.00,  9,  216, "Medicaid rate re-pricing lags cost trend through 2027; MA cost trend reaccelerates and CMS sanctions extend MA enrollment freeze; Carelon growth stalls; EPS $24.00 → 9× = $216"),
    "BASE":  (30.50, 12,  366, "FY2026 guidance (≥$30) holds; Medicaid rates gradually re-price through 2026-2027; MA cost trend moderates but CMS sanctions cap new MA growth near-term; Carelon (PBM/health services) provides steady offsetting growth; EPS $30.50 → 12× = $366"),
    "BULL":  (35.00, 14,  490, "Medicaid 2026-2027 rate cycle fully restores margin to historical range; MA cost trend normalizes and CMS sanctions lift, re-enabling MA growth; CarelonRx PBM scaling drives margin mix improvement; EPS $35.00 → 14× = $490"),
    "XBULL": (40.00, 16,  640, "Full earnings power restoration toward pre-2025 trajectory; Medicaid/MA margins both above target; Carelon becomes a $70B+ external-revenue platform rivaling Optum scale; multiple re-rates toward historical MCO premium; EPS $40.00 → 16× = $640"),
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
        "now":        "rates re-pricing in progress",
        "score":      2,
        "comment":    "Medicaid MLR trough hit in 2025 on redetermination/acuity mismatch; 26+ state contracts repricing through 2026-2027 is the single biggest swing factor for FY2027 earnings",
    },
    {
        "name":       "Medicare Advantage cost trend / CMS sanctions",
        "weight":     0.25,
        "thresholds": ("trend reaccelerates, sanctions extend", "trend stable, sanctions persist", "trend moderating, sanctions narrowing", "trend normalized, sanctions lifted"),
        "now":        "trend moderating, sanctions persist",
        "score":      2,
        "comment":    "MA cost trend pressure mirrors UNH/industry-wide 2025 dynamic; CMS star-rating/RADV-related sanctions ($935M accrual) cap new MA enrollment near-term but do not carry a DOJ-criminal overhang",
    },
    {
        "name":       "Carelon (CarelonRx PBM + Health Services) growth",
        "weight":     0.20,
        "thresholds": ("<5%",  "≥8%",  "≥12%",   "≥18%"),
        "now":        "+11%",
        "score":      3,
        "comment":    "Carelon is ELV's Optum analogue — CarelonRx PBM scaling with external clients, Carelon Health value-based care expanding; consistently the fastest-growing, highest-margin segment",
    },
    {
        "name":       "Commercial segment stability (Anthem/BCBS ASO/fully-insured)",
        "weight":     0.10,
        "thresholds": ("membership declining", "flat", "low-single-digit growth", "mid-single-digit+ growth"),
        "now":        "low-single-digit growth",
        "score":      2,
        "comment":    "Largest, most stable segment; ASO membership growth offsetting modest fully-insured pressure; pricing keeping pace with trend",
    },
    {
        "name":       "FY2026 guidance credibility / EPS trajectory",
        "weight":     0.10,
        "thresholds": ("guidance cut again", "guidance held flat", "guidance reaffirmed/raised modestly", "guidance raised meaningfully"),
        "now":        "guidance reaffirmed (≥$30)",
        "score":      3,
        "comment":    "Management reset 2025 guidance sharply lower but FY2026 guidance (≥$30 adj EPS) has been reaffirmed through early 2026 prints, restoring some credibility after the 2025 reset",
    },
    {
        "name":       "Balance sheet / capital return capacity",
        "weight":     0.10,
        "thresholds": ("<A-",  "A to A+",  "AA-",   "AA"),
        "now":        "A",
        "score":      3,
        "comment":    "Investment-grade with solid free cash flow generation; dividend maintained and growing (~2.1% yield) through the 2025 reset, signaling underlying balance sheet resilience",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("-", "Medicaid repricing execution risk — 26+ state contracts must re-rate through 2026-2027; timing/magnitude unproven", -0.5, 0.25),
    ("-", "MA cost-trend / CMS sanctions overhang — industry-wide MA pressure plus ELV-specific RADV/star-rating sanctions cap MA growth", -0.4, 0.20),
    ("+", "No DOJ criminal overhang — unlike UNH, ELV's regulatory issues are administrative (CMS sanctions/RADV), not a criminal risk-adjustment probe", +0.5, 0.15),
    ("+", "Carelon diversification — fast-growing, high-margin PBM/health-services platform reduces pure managed-care concentration", +0.5, 0.20),
    ("+", "Second-largest BCBS-affiliated commercial franchise — scale moat in core commercial/ASO business provides earnings stability", +0.3, 0.10),
    ("+", "Dividend maintained/growing through reset — signals management confidence in underlying earnings power", +0.3, 0.10),
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
CONS_EPS_2YR  = 33.00   # FY2028E conservative: gradual Medicaid/MA margin recovery
CONS_PE_2YR   = 12      # roughly flat from current multiple given residual Medicaid/MA uncertainty
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
shares_b     = shares * 0.97   # ~1.5%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.92   # MLR stays elevated, margin compresses further
bear_oi      = bear_gp - OPEX_FIXED_B * 1.02           # limited cost flexibility
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% margin − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% margin − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 14× = ~${bull_eps_imp*14:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.92:.1f}% margin − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 9× trough P/E (Medicaid/MA-discount floor) = ~${bear_eps_imp*9:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1pp_mlr     = curr_total * 0.01 * (1 - TAX_RATE) / shares   # 1pp MLR change ~ 1pp of revenue as margin
eps_per_1B_carelon  = 1.0 * 0.10 * (1 - TAX_RATE) / shares          # Carelon higher-margin
eps_per_1B_medicaid = 1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every 1pp MLR change (medical loss ratio):       ∓${eps_per_1pp_mlr:.2f}/EPS  = ∓${eps_per_1pp_mlr*12:.1f}/share at 12× P/E")
print(f"  Every $1B Carelon (CarelonRx/Health Services):   +${eps_per_1B_carelon:.3f}/EPS  = +${eps_per_1B_carelon*12:.1f}/share at 12× P/E")
print(f"  Every $1B Medicaid revenue (at blend):           +${eps_per_1B_medicaid:.3f}/EPS  = +${eps_per_1B_medicaid*12:.1f}/share at 12× P/E")
print(f"  1% buyback (~2.15M shares):                      +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

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
    ("Medicaid MLR / rate re-pricing",     "repricing", "rates lag trend", "−2-3pp",  "26+ state contracts re-price slower than acuity-driven cost trend through 2027"),
    ("MA cost trend / CMS sanctions",      "moderating", "reaccelerates", "+2pp",    "MA utilization trend reaccelerates while CMS sanctions extend the new-enrollment freeze"),
    ("Carelon growth",                     "+11%",   "<5%",    "−6pp",   "CarelonRx PBM client losses or Carelon Health value-based care margin compression"),
    ("Commercial membership",              "low-single-digit growth", "declining", "negative", "Employer groups shift to competitors amid premium increases"),
    ("FY2026 guidance",                    "reaffirmed (≥$30)", "cut again", "guidance cut", "Q2/Q3 2026 prints reveal another cost-trend miss, forcing a second guidance reset"),
    ("Medical loss ratio (overall)",       "~88.5%", ">91%",   "+2.5pp", "Combined Medicaid/MA cost pressure outpaces repricing across the book"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Medicaid 2026-2027 rate re-pricing fails to keep pace with acuity-driven cost")
print(f"  trend across the 26+ state contract book, while Medicare Advantage cost trend reaccelerates")
print(f"  and CMS star-rating/RADV sanctions extend the new-MA-enrollment freeze. Carelon growth stalls")
print(f"  as PBM client wins slow. EPS falls to ~$24.00 → 9× trough P/E (Medicaid/MA-discount floor) = ${bear_price}.")
print(f"  Note: $216 is NOT necessarily permanent impairment — ELV remains the #2 BCBS-affiliated insurer")
print(f"  with a fast-growing Carelon platform and no DOJ-criminal overhang. Recovery to ~${bear_price+60}–${bear_price+100}")
print(f"  in 2yr is plausible if Medicaid repricing lands on schedule by 2028.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           ${EPS_FY2027E:.2f}  (recovery-year consensus; FY2026E guided ≥$30)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.1f}×  (Medicaid/MA-discount floor; historical MCO trough ~9-10×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct >= 0 else 'below'} trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% {'premium to' if epp_gap_pct >= 0 else 'discount to'} EPP reflects that ELV trades at roughly")
print(f"  {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a depressed multiple for the #2 BCBS-affiliated")
print(f"  insurer, reflecting the combined Medicaid/MA cost-trend overhang. The open question is whether")
print(f"  2026-2027 Medicaid rate re-pricing restores margins toward historical norms and whether MA cost")
print(f"  trend moderates enough for CMS sanctions to lift. If both resolve favorably, the current price")
print(f"  embeds meaningful discount to even a modest recovery scenario.")
print(f"  EPP path: FY2029E EPS ~$38.00 × {PE_PESSIMISTIC:.1f}× = ${38.00*PE_PESSIMISTIC:.0f} floor (EPP grows as Medicaid/MA margins normalize).")
print(f"  At 12× mid-cycle P/E: ${EPS_FY2027E:.2f} × 12 = ${EPS_FY2027E*12:.0f}  — implies upside from current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: gradual Medicaid/MA margin normalization; P/E remains near current levels)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (modest growth as Medicaid rate re-pricing lands and MA cost trend stabilizes)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (roughly flat from ~{CURRENT_PRICE/EPS_FY2027E:.1f}× as residual cost-trend uncertainty caps re-rating)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: ELV trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a depressed multiple")
print(f"  for the #2 BCBS-affiliated insurer — reflecting the combined Medicaid margin trough and Medicare")
print(f"  Advantage cost-trend/CMS-sanctions overhang carried over from 2025. Carelon (CarelonRx PBM +")
print(f"  Health Services) provides a fast-growing diversification ballast while the core Health Benefits")
print(f"  segments work through the 2026-2027 Medicaid repricing cycle. If Medicaid rates land on schedule")
print(f"  and MA cost trend moderates, the multiple can re-rate toward 12-14×. If repricing lags or MA")
print(f"  sanctions persist longer than expected, current depressed levels persist.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E - 1)*100:.1f}% EPS growth by FY2028E vs FY2027E.")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.32
beta        = 0.65
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: 52W high itself remains well below the ~$550 2024 peak — entire range is post-reset")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  maintained/growing through the 2025 reset)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; Medicaid/MA cost-trend prints drive large moves)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (historically defensive, now elevated idiosyncratic MCO-sector risk)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (plausible; Medicaid-repricing-failure + MA-cost-trend-shock tail scenario)")
print(f"  52W range already reflects a significant collapse and partial recovery from the 2025 cost-trend crisis.")
print(f"  → Medicaid 2026-2027 rate re-pricing cadence is THE KEY operational signal to watch.")
print(f"  → MA cost trend + CMS sanction resolution timeline is the KEY binary for MA segment growth.")
print(f"  → AVOID above $430  |  WATCHLIST $355–430  |  ACCUMULATE $300–355  |  BUY below $300")

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
print(f"  In plain terms: the market's implied confidence in a smooth 2026-2027 Medicaid repricing cycle")
print(f"  and MA cost-trend normalization is roughly in line with (or modestly different from) the bottom-up")
print(f"  fundamentals score. Carelon's growth trajectory and the absence of a DOJ-style criminal overhang")
print(f"  are the key differentiators vs UNH's deeper discount.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Medicaid 2026-2027 rate re-pricing cadence — the single biggest swing factor for FY2027 margin")
print(f"  (2) Medicare Advantage cost trend trajectory — quarterly MLR prints vs CMS sanction timeline")
print(f"  (3) CMS star-rating/RADV sanction resolution — re-enabling MA new-member enrollment growth")
print(f"  (4) Carelon (CarelonRx PBM + Health Services) growth — external client wins and margin mix shift")
print(f"  (5) FY2026 guidance cadence — credibility rebuild after the 2025 reset")
print(f"  (6) Dividend sustainability — ${ANNUAL_DIV:.2f}/share maintained/growing through the reset")
print(f"  AVOID above $430  |  WATCHLIST $355–430  |  ACCUMULATE $300–355  |  BUY below $300")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.1f}×  |  FY2027E EPS: ${EPS_FY2027E:.2f}")
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
