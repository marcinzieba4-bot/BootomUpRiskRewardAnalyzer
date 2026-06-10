"""
SO  ·  Southern Company  ·  NYSE: SO
Bottom-up signal model  ·  Regulated Electric Utility (Georgia Power/Alabama Power/Mississippi Power) / Vogtle Nuclear / AI Data-Center Load Growth
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "SO"
COMPANY       = "Southern Company"
SECTOR        = "Regulated Electric Utility · Nuclear (Vogtle 3&4) · AI/Data-Center Load Growth (Georgia) · NYSE: SO"
CURRENT_PRICE = 92.00      # USD; as of 2026-06-10
VOL_52W_LOW   = 81.40      # 2025 rate-sensitivity/bond-proxy selloff trough
VOL_52W_HIGH  = 96.80      # 2026 data-center load-growth re-rating peak
SHARES_OUT_M  = 1_100.0    # millions
ANNUAL_DIV    = 2.92       # $/share; ~3.2% yield; 24+ consecutive years of increases

# ── SUBSIDIARY REVENUE BRIDGE (company-specific calculator) ──────────────────
# FY2026E revenue by subsidiary ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Georgia Power",                14.5, 13.0, 17.0, "Largest subsidiary; Vogtle 3&4 fully in rate base; data-center/AI load growth (Atlanta corridor) is THE key swing factor for rate base growth"),
    ("Alabama Power",                 7.6,  7.0,  8.3, "Stable industrial/residential base; modest economic-development-driven load growth, less data-center exposure than Georgia"),
    ("Mississippi Power",             1.4,  1.3,  1.6, "Smallest utility subsidiary; steady regulated returns post Kemper resolution"),
    ("Southern Power / Other (incl. SCS)", 2.5,  2.1,  3.2, "Wholesale/contracted generation (renewables PPAs) + parent/financing segment; growing via renewable additions"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.39    # blended regulated operating margin proxy
GROSS_MARGIN_BULL = 0.41    # BULL: operating leverage on incremental data-center load (low marginal cost on existing rate base)
OPEX_FIXED_B      = 4.3     # corporate SG&A + interest expense allocation ($B); largely fixed cost base
TAX_RATE          = 0.21    # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 4.55       # FY2027E EPS (consensus ~$4.45-$4.65; ~6% growth off FY2026E ~$4.30)
PE_PESSIMISTIC = 16.0       # trough P/E: regulated-utility floor in a higher-rate environment; SO historical trough ~15-17x
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # $73

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (4.30, 16,  69,  "Long-term rates stay elevated/rise further, compressing utility multiples; Georgia PSC rate case outcome disappoints; data-center load growth fails to materialize at scale; EPS $4.30 → 16× = $69"),
    "BASE":  (4.55, 19,  86,  "Steady ~5-6% regulated EPS growth continues; Georgia data-center load growth supports incremental rate base capex without major rate shock; multiple holds near current ~19-20x; EPS $4.55 → 19× = $86"),
    "BULL":  (4.85, 21,  102, "Georgia Power data-center demand (AI/hyperscale) drives accelerated rate base growth (IRP capacity additions); constructive rate case outcomes; EPS growth accelerates toward 7%+; EPS $4.85 → 21× = $102"),
    "XBULL": (5.45, 25,  136, "Southeast becomes the primary US AI/data-center buildout corridor; Georgia Power load forecasts repeatedly revised up; multiple re-rates toward growth-utility premium (Nextera-like) on durable double-digit rate base growth; EPS $5.45 → 25× = $136"),
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
        "name":       "Georgia Power data-center/AI load growth pipeline",
        "weight":     0.25,
        "thresholds": ("flat/declining", "≥1-2% load growth", "≥3-5% w/ IRP capacity adds", "≥6%+ structural step-change"),
        "now":        "+3-4% (large-load queue)",
        "score":      3,
        "comment":    "Georgia Power's large-load (data center) interconnection queue has grown sharply; latest IRP filings reflect multi-GW of new capacity additions tied to hyperscale demand",
    },
    {
        "name":       "Vogtle 3&4 operations / capex cycle status",
        "weight":     0.15,
        "thresholds": ("major capex overrun ongoing", "completed but cost recovery contested", "fully in rate base, performing", "performing + enables further nuclear expansion"),
        "now":        "fully in rate base, performing",
        "score":      3,
        "comment":    "Both Vogtle units operating at/near capacity factor targets; major capex cycle complete and largely de-risked, removing the primary historical overhang",
    },
    {
        "name":       "Regulated EPS growth rate (consensus)",
        "weight":     0.20,
        "thresholds": ("<4%",  "5-6%",  "6-7%",  ">7%"),
        "now":        "~6%",
        "score":      2,
        "comment":    "Management reaffirms 5-7% long-term EPS growth guidance off a higher post-Vogtle base; FY2026E-FY2027E tracking near the midpoint",
    },
    {
        "name":       "Interest rate environment / bond-proxy multiple sensitivity",
        "weight":     0.15,
        "thresholds": ("rates rising sharply", "rates elevated/stable", "rates easing modestly", "rates falling meaningfully"),
        "now":        "elevated/stable (10yr ~4.3-4.5%)",
        "score":      2,
        "comment":    "10-year Treasury yields remain elevated relative to the pre-2022 era, capping utility multiple expansion; any easing cycle would be a tailwind",
    },
    {
        "name":       "Georgia PSC / Alabama regulatory outcomes (rate cases, fuel cost recovery)",
        "weight":     0.15,
        "thresholds": ("adverse rulings", "neutral/as-expected", "constructive", "highly constructive + accelerated cost recovery"),
        "now":        "constructive",
        "score":      3,
        "comment":    "Recent Georgia rate case settlements and fuel cost recovery mechanisms have been constructive, supporting predictable ROE realization",
    },
    {
        "name":       "Balance sheet / credit profile",
        "weight":     0.10,
        "thresholds": ("sub-investment-grade risk", "BBB/Baa2 stable", "BBB+/Baa1 stable", "A-/A3 or better"),
        "now":        "BBB+/Baa2 stable, improving",
        "score":      3,
        "comment":    "Post-Vogtle deleveraging is underway; credit metrics improving as major capex cycle winds down, supporting continued dividend growth",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Georgia data-center/AI load growth — multi-GW interconnection queue provides multi-year rate base growth visibility unmatched by most regulated peers", +0.6, 0.25),
    ("+", "Vogtle de-risked — major nuclear capex cycle complete, both units operating; removes the dominant historical overhang and execution risk", +0.5, 0.15),
    ("-", "Bond-proxy interest-rate sensitivity — utility multiples remain capped while long rates stay elevated; SO carries above-average leverage from Vogtle financing", -0.4, 0.20),
    ("+", "24+ year dividend growth streak + investment-grade balance sheet improving — durable income floor with deleveraging tailwind", +0.4, 0.15),
    ("-", "Premium valuation already reflects growth optionality — SO trades at a premium to utility peers (~19-20x vs ~16-17x sector average), limiting further re-rating room absent upside surprises", -0.4, 0.15),
    ("-", "Regulatory/rate-case risk — large incremental capex for new generation/transmission to serve data-center load must clear PSC review; politically sensitive given residential bill impacts", -0.3, 0.10),
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
    signal_short, signal_full = "HOLD",      "▷ HOLD/TRIM"
else:
    signal_short, signal_full = "AVOID",     "✕ AVOID"

ratio_b_str = f"{ratio_b:.2f}x" if ratio_b != float("inf") else "N/A"

# ── CONSERVATIVE GROWTH (2-yr) ────────────────────────────────────────────────
CONS_EPS_2YR  = 4.85    # FY2028E conservative: ~6%/yr regulated EPS growth continues
CONS_PE_2YR   = 18      # modest de-rate from ~19-20x as growth optionality gets partially priced in
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Regulated Electric Utility (GA Power/AL Power/MS Power) / Vogtle Nuclear / AI Load Growth")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SUBSIDIARY REVENUE BRIDGE ──────────────────────────────────────────────
print()
print("  SUBSIDIARY REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
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
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_ni   = curr_oi * (1 - TAX_RATE)
curr_eps  = round(curr_ni / shares, 2)

bull_gp      = bull_total * GROSS_MARGIN_BULL
bull_oi      = bull_gp - OPEX_FIXED_B
bull_ni      = bull_oi * (1 - TAX_RATE)
shares_b     = shares * 1.01   # modest equity issuance to fund data-center-driven capex
bull_eps_imp = round(bull_ni / shares_b, 2)

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift / cost pressure
bear_oi      = bear_gp - OPEX_FIXED_B * 1.02           # higher interest expense
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% op margin − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% op margin − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (modest equity issuance)  =  ~${bull_eps_imp:.2f}/share  →  ${bull_eps_imp:.2f} × 21× = ~${bull_eps_imp*21:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% op margin − higher opex  =  ~${bear_eps_imp:.2f}/share")
print(f"  At 16× trough P/E (rate-sensitivity floor) = ~${bear_eps_imp*16:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev    = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_gapower = 1.0 * 0.42 * (1 - TAX_RATE) / shares   # Georgia Power - slightly higher margin
eps_per_100bps_rate = 0.18  # approx EPS sensitivity to 100bps move in cost of long-term debt over time

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Georgia Power revenue (data-center driven): +${eps_per_1B_gapower:.3f}/EPS  = +${eps_per_1B_gapower*19:.1f}/share at 19× P/E")
print(f"  Every $1B total revenue (blended):                     +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*19:.1f}/share at 19× P/E")
print(f"  1pp operating margin expansion:                        +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*19:.1f}/share at 19× P/E")
print(f"  100bps move in long-term rates (multiple impact):      ~∓1-2× P/E  = ~∓${CURRENT_PRICE*0.06:.0f}-${CURRENT_PRICE*0.10:.0f}/share")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Data-center load growth / Vogtle / EPS growth / Rates / Regulatory / Balance sheet)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>16}  {'BASE':>16}  {'BULL':>20}  {'XBULL':>22}  {'NOW':>22}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>16}  {ths[1]:>16}  {ths[2]:>20}  {ths[3]:>22}  {s['now']:>22}  {lbl}  {b}")

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
print(f"  {'Signal':<52}  {'Current':>14}  {'Bear val':>14}  {'Move':>10}  Trigger")
hr()
bear_triggers = [
    ("Georgia Power data-center load growth",  "+3-4%",   "flat/declining",  "−3-4pp",  "Hyperscale projects delayed/cancelled; AI capex cycle slows materially"),
    ("Long-term interest rates",               "~4.3-4.5%", "rise to 5%+",   "+50-75bp", "Persistent inflation forces Fed to hold/hike, compressing utility multiples"),
    ("Georgia PSC rate case outcomes",         "constructive", "adverse/delayed", "ROE cut", "Political pressure on residential bills leads to disallowed cost recovery"),
    ("Regulated EPS growth",                   "~6%",     "<4%",     "−2pp",   "Capex execution slips; financing costs rise faster than rate base growth"),
    ("Multiple (P/E)",                         "~19-20x", "16x",     "−3-4x",  "Bond-proxy de-rating as utility sector underperforms in rising-rate regime"),
    ("Credit profile",                         "BBB+/Baa2 improving", "downgrade risk", "outlook negative", "New data-center capex requires incremental debt faster than deleveraging"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>14}  {bear_v:>14}  {move:>10}  {trigger[:40]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Long-term interest rates rise further (10yr toward 5%+) compressing utility")
print(f"  multiples sector-wide, while Georgia's data-center/AI load growth pipeline disappoints as")
print(f"  hyperscale projects slip, and Georgia PSC rate case outcomes turn less constructive amid")
print(f"  political pressure on residential bills. EPS growth slows to ~$4.30 → 16× trough P/E = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT permanent impairment — regulated cash flows and a 24+ year dividend")
print(f"  growth streak (${ANNUAL_DIV:.2f}/share) provide a durable earnings floor. Recovery toward ~${bear_price+10}-${bear_price+17} in 2yr is plausible as rates normalize.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           ${EPS_FY2027E:.2f}  (consensus ~$4.45-$4.65)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (regulated-utility floor in elevated-rate regime; SO historical trough ~15-17×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% {'above' if epp_gap_pct >= 0 else 'below'} trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% {'premium to' if epp_gap_pct >= 0 else 'discount to'} EPP reflects that SO trades at roughly")
print(f"  {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a premium to the ~16-17× regulated-utility")
print(f"  sector average, justified by Vogtle de-risking and the Georgia data-center load-growth")
print(f"  pipeline that few regulated peers can match. The open question is whether that growth")
print(f"  visibility is durable enough to sustain a premium multiple if long-term rates stay elevated,")
print(f"  or whether SO converges back toward sector-average multiples over time.")
print(f"  EPP path: FY2029E EPS ~$5.05 × {PE_PESSIMISTIC:.0f}× = ${5.05*PE_PESSIMISTIC:.0f} floor (EPP grows as regulated EPS compounds even if multiple stays depressed).")
print(f"  At 19× mid-cycle P/E: ${EPS_FY2027E:.2f} × 19 = ${EPS_FY2027E*19:.0f}  — roughly in line with current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: continued ~6% regulated EPS growth; modest de-rate)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (~6%/yr growth via rate base growth, data-center load additions)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (modest de-rate from ~{CURRENT_PRICE/EPS_FY2027E:.1f}× as data-center optionality partially priced in)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: SO trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a premium")
print(f"  to the regulated-utility sector average, reflecting Vogtle de-risking and the Georgia")
print(f"  data-center/AI load-growth pipeline. The core debate is whether that load growth converts")
print(f"  into durable rate-base growth (supporting 6-7%+ EPS growth and the premium multiple) or")
print(f"  whether elevated rates and rate-case friction cap returns to dividend yield plus modest")
print(f"  EPS growth. For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E - 1)*100:.1f}% EPS growth by FY2028E vs FY2027E — modest, in line with guidance.")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.13
beta        = 0.45
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  24+ consecutive years of dividend increases)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (low; defensive regulated-utility bond-proxy profile)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (low-beta defensive utility)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (moderate; rate-shock/de-rating scenario, not a fundamental collapse)")
print(f"  52W range reflects relatively contained volatility typical of a regulated utility.")
print(f"  → Long-term interest rates (10yr Treasury) are THE KEY swing factor for the multiple.")
print(f"  → Georgia Power data-center/AI load growth pipeline conversion is the KEY bull catalyst.")
print(f"  → AVOID above $102  |  WATCHLIST $94–101  |  ACCUMULATE $84–93  |  BUY below $78–83")

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
print(f"  In plain terms: the market is pricing in {'more' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'less'} confidence on Georgia data-center load")
print(f"  growth conversion and rate-environment stability than the bottom-up fundamentals currently support.")
print(f"  The risk/reward skew (Ratio B {ratio_b_str}) reflects SO's position as a premium, de-risked")
print(f"  regulated utility with a credible structural growth driver, balanced against bond-proxy")
print(f"  rate sensitivity and an already-elevated relative multiple.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Georgia Power large-load (data center) interconnection queue — conversion to firm contracts and IRP capacity additions")
print(f"  (2) Long-term interest rates (10yr Treasury) — primary driver of utility sector multiple")
print(f"  (3) Georgia PSC / Alabama PSC rate case outcomes — ROE levels and cost recovery mechanisms")
print(f"  (4) Vogtle 3&4 operating performance — capacity factors and ongoing cost recovery true-ups")
print(f"  (5) Regulated EPS growth trajectory vs 5-7% long-term guidance")
print(f"  (6) Credit metrics / deleveraging progress — FFO/debt trends post-Vogtle capex cycle")
print(f"  AVOID above $102  |  WATCHLIST $94–101  |  ACCUMULATE $84–93  |  BUY below $78–83")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2027E EPS: ${EPS_FY2027E:.2f}")
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
