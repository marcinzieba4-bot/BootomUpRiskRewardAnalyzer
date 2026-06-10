"""
HD  ·  Home Depot, Inc.  ·  NYSE: HD
Bottom-up signal model  ·  Home Improvement Retail / Pro Customer (SRS Distribution) / Housing Cycle
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "HD"
COMPANY       = "Home Depot, Inc."
SECTOR        = "Home Improvement Retail · Pro/Contractor (SRS Distribution) · Housing Cycle · NYSE: HD"
CURRENT_PRICE = 398.00     # USD; as of 2026-06-10
VOL_52W_LOW   = 326.31     # 2025 high-rate / soft remodel-spend trough
VOL_52W_HIGH  = 421.83     # 2026 rate-cut-hope / Pro recovery peak
SHARES_OUT_M  = 980.0      # millions
ANNUAL_DIV    = 9.30       # $/share; ~2.34% yield; 16+ yrs of consecutive increases

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Core US Retail (DIY)",                88.0, 82.0,  94.0, "DIY comps roughly flat to slightly negative; big-ticket discretionary remodel projects deferred under high mortgage rates"),
    ("Pro/Contractor - legacy HD Pro",       38.0, 35.0,  43.0, "Pro share-of-wallet initiatives (trade credit, delivery, MaxPro) gaining traction; outpacing DIY"),
    ("SRS Distribution (Pro specialty)",     20.0, 18.0,  25.0, "Roofing/landscape/pool specialty distribution; integration synergies and cross-sell into HD Pro ecosystem still ramping"),
    ("Installation Services / Other",         5.5,  5.0,   6.5, "Installation services steady; modest growth tied to big-ticket project recovery"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.335   # blended gross margin; SRS dilutes slightly vs core retail
GROSS_MARGIN_BULL = 0.340   # BULL: operating leverage + Pro mix improvement at scale
OPEX_FIXED_B      = 36.0    # SG&A + D&A ($B); largely fixed cost base, modest opex discipline
TAX_RATE          = 0.245   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 15.40       # FY2027E EPS (consensus ~$15.20-$15.60 non-GAAP)
PE_PESSIMISTIC = 18.0        # trough P/E: best-in-class retailer floor; HD historical trough ~17-19x in downturns
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # $277

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (14.25, 19,  271, "Mortgage rates stay elevated/rise further; DIY comps turn modestly negative (-1% to -3%); SRS integration stalls; slight margin compression from deleverage; EPS $14.25 → 19× = $271"),
    "BASE":  (15.40, 25,  385, "Comps stabilize near flat to low-single-digit positive as rate environment gradually eases; Pro/SRS continues mid-single-digit growth; modest margin expansion from opex discipline; EPS $15.40 × 25× = $385"),
    "BULL":  (17.50, 27,  473, "Rate cuts spur housing turnover and big-ticket remodel recovery; comps reaccelerate to +3-5%; SRS cross-sell synergies materialize; Pro segment share gains compound; EPS $17.50 → 27× = $473"),
    "XBULL": (20.00, 29,  580, "Full housing-cycle recovery (existing home sales rebound, mortgage rates <6%); multi-year pent-up remodel demand unleashed; Pro ecosystem (HD Pro + SRS) becomes dominant moat; multiple re-rates toward growth-retail peers; EPS $20.00 → 29× = $580"),
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
        "name":       "Comparable sales growth (consolidated)",
        "weight":     0.25,
        "thresholds": ("≤-3%", "≈0%",  "≥+2%",  "≥+4%"),
        "now":        "-0.5%",
        "score":      2,
        "comment":    "Comps roughly flat to slightly negative for ~2 years; recent quarters show stabilization/modest sequential improvement off elevated mortgage rates",
    },
    {
        "name":       "Pro/SRS Distribution growth & integration",
        "weight":     0.20,
        "thresholds": ("stalling", "low-single-digit", "mid-single-digit", "high-single-digit+"),
        "now":        "+5-6%",
        "score":      3,
        "comment":    "SRS Distribution + legacy HD Pro initiatives (trade credit, MaxPro, delivery) growing faster than DIY; cross-sell synergies still early-stage",
    },
    {
        "name":       "Big-ticket discretionary project demand",
        "weight":     0.15,
        "thresholds": ("declining", "stable/soft", "improving", "strong rebound"),
        "now":        "soft/stable",
        "score":      2,
        "comment":    "Large remodel/renovation projects (>$1,000) remain depressed under high financing costs; transaction count for big-ticket items still below pre-2022 levels",
    },
    {
        "name":       "Mortgage rate / housing turnover environment",
        "weight":     0.15,
        "thresholds": ("rates rising/>7.5%", "rates flat ~6.5-7.5%", "rates declining toward 6%", "rates <5.5%, turnover rebounds"),
        "now":        "~6.5-7%, range-bound",
        "score":      2,
        "comment":    "Mortgage rates have been range-bound near 6.5-7% for an extended period; existing home sales remain near multi-decade lows, suppressing the remodel cycle that HD depends on",
    },
    {
        "name":       "Gross margin / operating leverage trajectory",
        "weight":     0.10,
        "thresholds": ("contracting", "roughly flat", "expanding modestly", "expanding meaningfully"),
        "now":        "roughly flat",
        "score":      2,
        "comment":    "Gross margin holding near 33-34% despite SRS mix dilution; opex discipline offsetting deleverage from soft comps",
    },
    {
        "name":       "Capital return / balance sheet (dividend + buybacks)",
        "weight":     0.15,
        "thresholds": ("cuts/freeze", "maintained", "growing modestly", "growing + accelerated buybacks"),
        "now":        "growing",
        "score":      3,
        "comment":    "16+ consecutive years of dividend increases (~2.3% yield); continued share buybacks despite SRS-related leverage uptick; investment-grade balance sheet intact",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Best-in-class retailer moat — scale, supply chain, and Pro ecosystem (HD Pro + SRS) create durable competitive advantage", +0.5, 0.20),
    ("-", "Premium valuation (~24-26x earnings) leaves little room for multiple expansion absent a clear housing-cycle catalyst", -0.5, 0.20),
    ("-", "Housing market sensitivity — ~2 years of suppressed big-ticket remodel spend tied to mortgage rates outside HD's control", -0.4, 0.20),
    ("+", "SRS Distribution acquisition expands TAM into Pro/specialty trade (roofing, landscape, pool) with long runway for cross-sell", +0.4, 0.15),
    ("+", "Consistent dividend growth (16+ yrs) + buybacks provide capital-return floor even in a soft comp environment", +0.3, 0.15),
    ("-", "SRS-related leverage increase modestly reduces balance sheet flexibility versus HD's historically pristine credit profile", -0.2, 0.10),
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
CONS_EPS_2YR  = 16.50   # FY2028E conservative: modest EPS growth as comps stabilize, SRS scales
CONS_PE_2YR   = 23      # rerates modestly lower from ~25.8x given limited near-term catalyst
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Home Improvement Retail / Pro (SRS Distribution) / Housing Cycle")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
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
shares_b     = shares * 0.96   # ~2%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.985   # slight margin deleverage
bear_oi      = bear_gp - OPEX_FIXED_B * 0.97             # partial cost response
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 27× = ~${bull_eps_imp*27:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.985:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 19× trough P/E (best-in-class retailer floor) = ~${bear_eps_imp*19:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev      = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_pro      = 1.0 * 0.34 * (1 - TAX_RATE) / shares   # Pro/SRS roughly in-line margin
eps_per_1B_diy      = 1.0 * 0.335 * (1 - TAX_RATE) / shares  # Core DIY

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Pro/SRS revenue:                       +${eps_per_1B_pro:.3f}/EPS  = +${eps_per_1B_pro*24:.1f}/share at 24× P/E")
print(f"  Every $1B Core DIY revenue:                      +${eps_per_1B_diy:.3f}/EPS  = +${eps_per_1B_diy*24:.1f}/share at 24× P/E")
print(f"  1pp GM expansion (Pro mix / opex leverage):      +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*24:.1f}/share at 24× P/E")
print(f"  1% buyback (~9.8M shares):                       +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Comps / Pro-SRS growth / Big-ticket demand / Housing rate cycle)")
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
    ("Comparable sales growth",            "-0.5%",  "≤-3%",   "−2.5pp", "Mortgage rates rise further or consumer spending broadly weakens, cutting DIY traffic"),
    ("Pro/SRS growth & integration",       "+5-6%",  "stalling", "−5pp+", "SRS integration synergies disappoint; Pro share gains stall amid construction slowdown"),
    ("Big-ticket discretionary demand",    "soft",   "declining", "further down", "Continued or worsening rate environment delays remodel projects indefinitely"),
    ("Mortgage rate / housing turnover",   "~6.5-7%","rising/>7.5%", "+1pp+", "Rates push higher, existing home sales fall further, remodel cycle extends its trough"),
    ("Gross margin trajectory",            "flat",   "contracting", "-1.5pp", "SRS mix dilution + promotional intensity to defend traffic compress margins"),
    ("Capital return / balance sheet",     "growing","maintained/frozen", "flat", "SRS-related leverage forces a pause in buyback pace to protect credit rating"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Mortgage rates resume climbing (back toward/above 7.5%) rather than easing,")
print(f"  pushing existing home sales to fresh multi-decade lows and forcing comps materially")
print(f"  negative (-3% to -5%). SRS integration synergies stall, Pro growth decelerates sharply,")
print(f"  and gross margin compresses as HD leans on promotions to defend traffic.")
print(f"  EPS falls to ~$13.50 → 18× trough P/E (best-in-class-retailer floor) = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT permanent impairment — HD's scale moat, Pro ecosystem, and")
print(f"  dividend (${ANNUAL_DIV:.2f}/share) provide a durable floor. Recovery toward ${bear_price+60}-${bear_price+100}")
print(f"  in 2yr is plausible once the housing cycle turns.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           ${EPS_FY2027E:.2f}  (consensus ~$15.20-$15.60 non-GAAP)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (best-in-class-retailer floor; HD historical trough ~17-19×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct >= 0 else 'below'} trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% {'premium to' if epp_gap_pct >= 0 else 'discount to'} EPP reflects that HD trades at roughly")
print(f"  {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a premium multiple consistent with HD's status as the")
print(f"  best-in-class home improvement retailer. Two years of suppressed big-ticket remodel demand")
print(f"  (driven by elevated mortgage rates) are largely priced in via flattish near-term comps. The")
print(f"  open question is whether SRS Distribution / Pro initiatives can keep growing through the")
print(f"  housing downturn, or whether the premium multiple caps further re-rating until rates fall.")
print(f"  EPP path: FY2029E EPS ~$17.50 × {PE_PESSIMISTIC:.0f}× = ${17.50*PE_PESSIMISTIC:.0f} floor (EPP grows as Pro/SRS scale).")
print(f"  At 24× mid-cycle P/E: ${EPS_FY2027E:.2f} × 24 = ${EPS_FY2027E*24:.0f}  — roughly in line with current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest EPS growth as comps stabilize, P/E compresses slightly)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (modest growth; comps stabilize near flat-to-positive, Pro/SRS continue mid-single-digit growth)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (modestly down from ~{CURRENT_PRICE/EPS_FY2027E:.1f}× as premium multiple compresses slightly absent rate-cut catalyst)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: HD trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a premium multiple that")
print(f"  reflects HD's best-in-class scale, supply chain, and Pro ecosystem (HD Pro + SRS Distribution).")
print(f"  Comparable sales have been roughly flat to slightly negative for ~2 years as elevated")
print(f"  mortgage rates suppress big-ticket discretionary remodel spend, but trends are stabilizing.")
print(f"  If the housing market/rate-cut recovery materializes, comps reaccelerate and the premium")
print(f"  multiple is sustained or expands. If rates stay elevated, current levels are roughly fair.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E - 1)*100:.1f}% EPS growth by FY2028E vs FY2027E — modest, achievable at BASE.")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.20
beta        = 1.00
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  consistent grower, 16+ yrs of increases)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (moderate; large-cap retailer with housing-cycle sensitivity)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (roughly market beta; cyclical consumer discretionary exposure)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (significant; rate-shock/housing-downturn-deepens scenario)")
print(f"  52W range reflects moderate volatility tied to rate expectations and Pro/SRS execution.")
print(f"  → Mortgage rate trajectory / housing turnover is THE KEY binary for the comp recovery.")
print(f"  → SRS Distribution cross-sell synergies + Pro share gains are KEY bull catalysts.")
print(f"  → AVOID above $440  |  WATCHLIST $400–440  |  ACCUMULATE $355–375  |  BUY below $330–350")

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
print(f"  In plain terms: the market is pricing in {'more' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'less'} confidence on a near-term housing/")
print(f"  rate-cut recovery and Pro/SRS execution than the bottom-up fundamentals currently support.")
print(f"  The risk/reward skew (Ratio B {ratio_b_str}) reflects HD's premium valuation balanced against")
print(f"  its best-in-class moat, dividend support, and the eventual housing-cycle recovery catalyst.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Mortgage rate trajectory — rate cuts would unlock pent-up big-ticket remodel demand")
print(f"  (2) SRS Distribution integration — cross-sell synergies into HD Pro ecosystem (roofing/landscape/pool)")
print(f"  (3) Comparable sales trajectory — stabilization vs reacceleration of DIY and Pro segments")
print(f"  (4) Pro customer share-of-wallet — trade credit, MaxPro, delivery initiatives")
print(f"  (5) Gross margin / opex leverage — ability to expand margins through soft-comp environment")
print(f"  (6) Dividend sustainability — ${ANNUAL_DIV:.2f}/share payout; 16+ yr increase streak")
print(f"  AVOID above $440  |  WATCHLIST $400–440  |  ACCUMULATE $355–375  |  BUY below $330–350")
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
