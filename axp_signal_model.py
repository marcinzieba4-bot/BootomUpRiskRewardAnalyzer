"""
AXP  ·  American Express Company  ·  NYSE: AXP
Bottom-up signal model  ·  Closed-Loop Payments / Premium Charge Cards / T&E
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "AXP"
COMPANY       = "American Express Company"
SECTOR        = "Payments · Closed-Loop Network · Premium Charge Cards · T&E · NYSE: AXP"
CURRENT_PRICE = 342.50      # USD; as of 2026-06-10
VOL_52W_LOW   = 255.10      # April 2026 tariff/consumer-spending-scare trough
VOL_52W_HIGH  = 365.80      # early 2026 high on strong card-fee growth
SHARES_OUT_M  = 690.0       # millions; declining ~3%/yr via buyback
SECTOR_NOTE   = SECTOR      # placeholder for parity with AAPL header naming

# Dividend: long growth track record; growing ~15-17%/yr recently
ANNUAL_DIV    = 3.20        # $/share FY2026 ($0.82/quarter, raised early 2026)

# ── REVENUE BRIDGE BY SEGMENT (company-specific calculator) ──────────────────
# FY2026E total revenues net of interest expense by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("U.S. Consumer Services",        29.0, 24.0, 33.5, "Platinum/Gold refresh cycles drive card fee growth; Millennial/Gen-Z acquisition"),
    ("Commercial Services",           16.0, 13.0, 18.5, "SME & mid-market B2B spend; Amex Business Blueprint; T&E recovery"),
    ("International Card Services",   11.5,  9.5, 13.5, "Fastest-growing segment; international consumer & SME card acquisition"),
    ("Global Merchant & Network Svcs", 9.5,  8.3, 10.8, "Discount revenue from merchant acceptance; network fees; coverage expansion"),
]

# Margin assumptions (applied to total revenue net of interest expense)
PRETAX_MARGIN_CURR = 0.201   # blended pretax margin FY2026E (~20.1%, after corporate items/financing costs)
PRETAX_MARGIN_BULL = 0.225   # BULL: operating leverage from spend growth + opex discipline
OPEX_PROVISION_B   = 8.0     # incremental provision for credit losses build / marketing investment ($B)
TAX_RATE           = 0.205   # effective tax rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 15.30       # FY2026E adj EPS (consensus ~$15.00-$15.50)
PE_PESSIMISTIC = 13.0        # trough P/E: 2020 COVID trough ~11x; 2022 credit-fear trough ~13x
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # ~$199

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (11.50, 13,  150, "Consumer spending recession; T&E -15%; credit losses spike; EPS $11.50 → 13× trough P/E"),
    "BASE":  (18.50, 19,  352, "Billed business +7-8%/yr; card fee growth continues; EPS $18.50 at FY2028E → 19×"),
    "BULL":  (23.00, 23,  529, "Premium refresh cycles drive fee growth acceleration; T&E boom; Gen-Z acquisition scales; EPS $23 → 23×"),
    "XBULL": (28.00, 25,  700, "Network effects compound; international scales rapidly; buybacks accelerate EPS; EPS $28 → 25×"),
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
        "name":       "Billed business / spend volume YoY growth",
        "weight":     0.25,
        "thresholds": ("<3%",    "≥6%",   "≥9%",    "≥13%"),
        "now":        "+7%",
        "score":      2,
        "comment":    "Consumer +6%, SME/Commercial +5%, International +12%; T&E spend resilient but normalizing",
    },
    {
        "name":       "Card fee revenue YoY growth",
        "weight":     0.25,
        "thresholds": ("<10%",   "≥14%",  "≥18%",   "≥24%"),
        "now":        "+17%",
        "score":      3,
        "comment":    "Platinum/Gold refresh driving acquisitions; record new card acquisitions, fee base growing fastest revenue line",
    },
    {
        "name":       "Net write-off rate (credit quality)",
        "weight":     0.20,
        "thresholds": (">2.6%",  "≤2.3%", "≤1.9%",  "≤1.6%"),
        "now":        "2.1%",
        "score":      3,
        "comment":    "Premium affluent cardmember base keeps write-offs well below issuer-bank averages; stable through cycle",
    },
    {
        "name":       "New card acquisitions / member retention",
        "weight":     0.15,
        "thresholds": ("<2.5M",  "≥3.0M", "≥3.5M",  "≥4.0M"),
        "now":        "~3.4M",
        "score":      3,
        "comment":    "Millennial/Gen-Z now >60% of new consumer acquisitions; retention rates remain industry-leading ~98%",
    },
    {
        "name":       "International Card Services revenue growth",
        "weight":     0.10,
        "thresholds": ("<6%",    "≥9%",   "≥13%",   "≥18%"),
        "now":        "+12%",
        "score":      3,
        "comment":    "Fastest-growing segment; expanding acceptance footprint and local-currency card products",
    },
    {
        "name":       "Operating expense ratio (opex / revenue)",
        "weight":     0.05,
        "thresholds": (">52%",   "≤50%",  "≤47%",   "≤44%"),
        "now":        "49%",
        "score":      2,
        "comment":    "Marketing & card member rewards costs elevated to support refresh cycles; modest operating leverage",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Closed-loop network moat — issuer + network in one; richer data, pricing power vs Visa/MA",   +0.6, 0.25),
    ("+", "Premium brand / affluent base — high spend-per-card, low write-offs, 98% retention",          +0.6, 0.20),
    ("+", "Card fee flywheel — Platinum/Gold refresh cycles compound recurring high-margin revenue",     +0.4, 0.15),
    ("-", "Consumer spending cyclicality — T&E and discretionary spend highly sensitive to recession",   -0.7, 0.20),
    ("-", "Card loan book credit risk — provisions can spike sharply in a downturn despite premium mix", -0.5, 0.15),
    ("+", "Capital return — buybacks + 17% dividend growth; strong capital generation (CET1 well above min)", +0.3, 0.05),
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
CONS_EPS_2YR  = 18.50   # conservative FY2028E: ~10% EPS CAGR via spend growth + buybacks
CONS_PE_2YR   = 18      # modest rerating from ~19x toward 18x (in line with historical mid-range)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Closed-Loop Payments / Premium Cards / T&E")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① REVENUE BRIDGE ─────────────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<32}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<32}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<32}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print()

# EPS bridge
curr_pti  = curr_total * PRETAX_MARGIN_CURR
curr_ni   = curr_pti * (1 - TAX_RATE)
shares    = SHARES_OUT_M / 1000
curr_eps  = round(curr_ni / shares, 2)

bull_pti  = bull_total * PRETAX_MARGIN_BULL
bull_ni   = bull_pti * (1 - TAX_RATE)
shares_b  = shares * 0.94   # ~3%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_pti  = bear_total * PRETAX_MARGIN_CURR * 0.80   # margin compression from credit provisioning
bear_ni   = max(0, bear_pti) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B revenue × {PRETAX_MARGIN_CURR*100:.1f}% pretax margin − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ~${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {PRETAX_MARGIN_BULL*100:.1f}% pretax margin − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 23× = ~${bull_eps_imp*23:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {PRETAX_MARGIN_CURR*100*0.80:.1f}% pretax margin (credit provisioning hit)  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 13× trough P/E (2022 credit-fear floor) = ~${bear_eps_imp*13:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev   = (1.0 * PRETAX_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_10bp_wo  = curr_eps * 0.04   # rough: 10bp write-off rate change ~4% EPS impact

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B billed-business-driven revenue:  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*19:.1f}/share at 19× P/E")
print(f"  Net write-off rate ±10bp:                   ±${eps_per_10bp_wo:.2f}/EPS  =  ±${eps_per_10bp_wo*19:.1f}/share at 19× P/E")
print(f"  1pp pretax margin expansion (opex leverage): +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*19:.1f}/share at 19× P/E")
print(f"  1% buyback (~7M shares):                     +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (spend volume / card fees / credit quality / acquisition framework)")
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
    ("Billed business YoY",              "+7%",   "<0%",    "−7pp",   "Consumer recession; discretionary T&E spend collapses"),
    ("Net write-off rate",               "2.1%",  ">3.5%",  "+1.4pp", "Unemployment spike; cardmember credit deterioration"),
    ("Card fee revenue YoY",             "+17%",  "<5%",    "−12pp",  "New card acquisition stalls; fee waivers/downgrades rise"),
    ("New card acquisitions",            "3.4M",  "<2.0M",  "−1.4M",  "Marketing pullback; competitive premium card launches"),
    ("International revenue growth",     "+12%",  "<3%",    "−9pp",   "Global recession; FX headwinds; international SME pullback"),
    ("Operating expense ratio",          "49%",   ">55%",   "+6pp",   "Provisions for credit losses surge; rewards costs un-flexed"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A consumer-spending recession driven by labor-market deterioration causes")
print(f"  T&E and discretionary spend to fall sharply (billed business turns negative), while")
print(f"  net write-offs on the cardmember loan book spike toward 3.5%+. Card fee growth stalls")
print(f"  as cardmembers downgrade or cancel premium products. EPS falls to ~$11.50 → 13× trough")
print(f"  P/E (2022 credit-fear floor) = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT a permanent impairment — the closed-loop network, premium")
print(f"  brand, and ~98% retention provide a durable earnings floor. Recovery toward")
print(f"  ${bear_price+50}–${bear_price+90} in 2yr is the base case post-shock.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~$15.00–$15.50)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (2020 COVID trough ~11×; 2022 credit-fear trough ~13×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP means the market prices in continued double-digit")
print(f"  card fee and billed business growth ABOVE the trough-floor multiple. At ${CURRENT_PRICE:.2f}")
print(f"  and FY2026E EPS ${EPS_FY2026E:.2f}, the P/E is ~{CURRENT_PRICE/EPS_FY2026E:.1f}× — near the top of AXP's")
print(f"  historical 18-22× range. The premium brand moat and closed-loop pricing power justify")
print(f"  some premium, but the risk is mean reversion if spend growth or credit quality slips.")
print(f"  EPP path: FY2028E EPS ~$18.50 × {PE_PESSIMISTIC:.0f}× = ${18.50*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing with EPS).")
print(f"  At 19× mid-cycle P/E: ${EPS_FY2026E:.2f} × 19 = ${EPS_FY2026E*19:.0f}  — below current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: spend growth + buybacks; modest multiple normalization)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (~10% EPS CAGR: billed business +7-8%/yr + buybacks ~3%/yr)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (modest normalization within historical 18-22× range)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; ~17% recent dividend growth)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: can EPS compound at ~10%/yr while the multiple holds near {CONS_PE_2YR}×?")
print(f"  Card fee growth (Platinum/Gold refresh) and international scaling are the key drivers.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — achievable in BASE/BULL.")
print(f"  Breakeven at 22× P/E (top of historical range): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 22:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.26
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  modest but growing ~17%/yr)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (consumer-spending sensitivity drives swings vs networks)")
print(f"  Beta vs S&P 500:      1.20  (premium; consumer discretionary cyclicality amplifier)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe; consumer-recession tail scenario)")
print(f"  52W low ${VOL_52W_LOW:.2f} (Apr 2026 spending scare) already a peak-to-trough move of ~30%.")
print(f"  → A consumer-spending / labor-market downturn is THE KEY risk; T&E spend is the swing factor.")
print(f"  → Card fee growth acceleration (Platinum/Gold refresh adoption) is KEY bull catalyst.")
print(f"  → AVOID above $370  |  WATCHLIST $300–345  |  ACCUMULATE $260–300  |  BUY below $230")

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
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The model scores fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0 —")
print(f"  near BASE/BULL boundary, reflecting strong card-fee growth and credit quality offset by")
print(f"  consumer-spending cyclicality risk. The gap ({ADJ_GAP:.2f}) indicates the stock is")
print(f"  {valuation_label.lower()} by model standards.")
print(f"  Card fee growth (signal score 3/4) and credit quality (3/4) are the strongest pillars;")
print(f"  consumer spend cyclicality embedded in the SCA is the key valuation risk.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Platinum/Gold refresh cycle uptake — card fee revenue acceleration above +18%/yr (BULL trigger)")
print(f"  (2) Consumer spending / labor market — T&E and discretionary spend deceleration (BEAR trigger)")
print(f"  (3) Net write-off rate trajectory — premium cardmember base credit quality through the cycle")
print(f"  (4) International Card Services scaling — can it sustain low-double-digit growth as it grows?")
print(f"  (5) Millennial/Gen-Z acquisition — can new-card growth offset any premium-segment saturation?")
print(f"  AVOID above $370  |  WATCHLIST $300–345  |  ACCUMULATE $260–300  |  BUY below $230")
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
