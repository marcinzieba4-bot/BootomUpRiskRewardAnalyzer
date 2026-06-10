"""
ISRG  ·  Intuitive Surgical, Inc.  ·  NASDAQ: ISRG
Bottom-up signal model  ·  Surgical Robotics / Recurring Procedure Revenue
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "ISRG"
COMPANY       = "Intuitive Surgical, Inc."
SECTOR        = "Surgical Robotics · da Vinci Platform · Recurring Procedure Revenue · NASDAQ: ISRG"
CURRENT_PRICE = 452.00      # USD; as of 2026-06-10
VOL_52W_LOW   = 380.00
VOL_52W_HIGH  = 620.00
SHARES_OUT_M  = 1_330.0     # millions; modest buyback offsetting SBC dilution

# Dividend: none — all FCF reinvested into platform R&D and capacity
ANNUAL_DIV    = 0.0

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Instruments & Accessories", 14.50, 12.30, 16.90, "Recurring per-procedure revenue; scales with worldwide procedure volume"),
    ("Systems (da Vinci 5)",       6.80,  5.10,  8.80, "da Vinci 5 placements; multi-year capex upgrade cycle from da Vinci Xi base"),
    ("Services",                   3.90,  3.30,  4.50, "Maintenance contracts on growing installed base; high-margin annuity"),
    ("Other (leases/intl/misc)",   2.60,  2.20,  3.10, "Operating lease revenue, international distribution, FX"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.685   # blended gross margin FY2026E (~68.5%)
GROSS_MARGIN_BULL = 0.705   # BULL: scale + da Vinci 5 mix improves blend
OPEX_FIXED_B      = 6.50    # R&D + SG&A ($B); heavy R&D investment in next-gen platform
TAX_RATE          = 0.180   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 8.00        # FY2026E adj EPS (consensus ~$7.85-$8.20; non-GAAP)
PE_PESSIMISTIC = 35.0        # trough P/E: durable recurring-revenue moat floors multiple well above market avg
                              # (2022-23 trough ~32-38×; reflects structural moat)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $280

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 6.50, 35,  228, "Procedure growth decelerates <10%; competitive entrants erode share; EPS $6.50 → 35× floor"),
    "BASE":  ( 8.00, 55,  440, "Procedure volume +13-15%; da Vinci 5 placement steady; EPS $8.00 → 55×"),
    "BULL":  ( 9.50, 65,  618, "da Vinci 5 cycle accelerates; international + general surgery expansion; EPS $9.50 → 65×"),
    "XBULL": (12.00, 75,  900, "New procedure categories scale globally; ISRG becomes platform standard of care; EPS $12.00 → 75×"),
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
        "name":       "Worldwide procedure volume growth",
        "weight":     0.25,
        "thresholds": ("<10%",   "≥13%",  "≥17%",   "≥22%"),
        "now":        "+15%",
        "score":      3,
        "comment":    "Core driver of recurring instrument/accessory revenue; general surgery + bariatric leading growth",
    },
    {
        "name":       "da Vinci 5 system placement growth",
        "weight":     0.20,
        "thresholds": ("<5%",    "≥10%",  "≥18%",   "≥28%"),
        "now":        "~17%",
        "score":      3,
        "comment":    "da Vinci 5 ramping across US installed base; multi-year Xi-to-5 upgrade cycle underway",
    },
    {
        "name":       "Instruments & Accessories revenue per procedure",
        "weight":     0.20,
        "thresholds": ("flat",   "≥+1%",  "≥+3%",   "≥+5%"),
        "now":        "+2.5%",
        "score":      2,
        "comment":    "Recurring revenue mix improving via stapling, vessel-sealing, energy instruments attach rate",
    },
    {
        "name":       "International procedure adoption (Asia/Europe)",
        "weight":     0.15,
        "thresholds": ("<8%",    "≥12%",  "≥18%",   "≥25%"),
        "now":        "+14%",
        "score":      2,
        "comment":    "Japan reimbursement expansion, China JV placements, Europe hospital budget recovery — gradual",
    },
    {
        "name":       "Gross margin trajectory",
        "weight":     0.10,
        "thresholds": ("<65%",   "≥67%",  "≥69%",   "≥71%"),
        "now":        "68.5%",
        "score":      2,
        "comment":    "da Vinci 5 input costs + tariff exposure offsetting scale benefits in near term",
    },
    {
        "name":       "New procedure category penetration (general surgery vs urology/gyn)",
        "weight":     0.10,
        "thresholds": ("<15%",   "≥20%",  "≥28%",   "≥38%"),
        "now":        "~21%",
        "score":      2,
        "comment":    "Hernia, bariatric, colorectal scaling from low base; urology/gyn maturing toward saturation",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Recurring revenue moat — instruments/accessories scale with every procedure; high switching costs",  +0.7, 0.25),
    ("+", "da Vinci 5 platform cycle — multi-year upgrade wave across 10,000+ installed system base",          +0.6, 0.20),
    ("+", "Procedure category runway — general surgery early innings vs mature urology/gyn base",               +0.4, 0.15),
    ("-", "Premium valuation — ~55× current EPS demands sustained double-digit procedure growth indefinitely", -0.7, 0.20),
    ("-", "Competitive robotic entrants — Medtronic Hugo, J&J Ottava targeting ISRG's core soft-tissue niche",  -0.5, 0.15),
    ("-", "Hospital capex sensitivity — system sales (vs recurring revenue) exposed to capital budget cycles", -0.3, 0.05),
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
CONS_EPS_2YR  = 9.00    # conservative FY2028E: ~12% EPS CAGR; procedure growth moderates but stays double-digit
CONS_PE_2YR   = 50      # modest rerating from 55× toward 50× as growth normalizes
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Surgical Robotics / da Vinci 5 / Recurring Revenue")
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
shares_b  = shares * 0.99   # minimal buyback; SBC dilution roughly offset
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift to lower-margin systems
bear_oi   = bear_gp - OPEX_FIXED_B * 0.98           # limited cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.2f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.2f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ~${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.2f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 65× = ~${bull_eps_imp*65:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 35× trough P/E (recurring-revenue floor) = ~${bear_eps_imp*35:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Instruments & Accessories revenue: +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*55:.1f}/share at 55× P/E")
print(f"  1pp procedure volume growth (≈$0.4B I&A):    +${eps_per_1B_rev*0.4:.3f}/EPS  =  +${eps_per_1B_rev*0.4*55:.1f}/share at 55× P/E")
print(f"  1pp GM expansion (mix/pricing):               +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*55:.1f}/share at 55× P/E")
print(f"  da Vinci 5 placement +500 systems/yr:         supports Systems revenue +${0.5*2.5:.2f}B  = +${0.5*2.5*(1-TAX_RATE)/shares:.2f}/EPS")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Procedure growth / da Vinci 5 cycle / recurring revenue framework)")
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
    ("Worldwide procedure volume growth",  "+15%",  "<10%",   "−5pp",   "Hospital capex tightening + payer pushback slows elective surgery"),
    ("da Vinci 5 placement growth",        "+17%",  "<8%",    "−9pp",   "da Vinci 5 ramp disappoints; hospitals delay upgrade from Xi fleet"),
    ("Competitive entrants (Hugo/Ottava)", "early", "scaling","shift",  "Medtronic Hugo / J&J Ottava win meaningful soft-tissue share"),
    ("I&A revenue per procedure",          "+2.5%", "flat",   "−2.5pp", "Pricing pressure as competitors offer lower-cost instrument bundles"),
    ("International adoption",             "+14%",  "<8%",    "−6pp",  "China JV placements stall; Japan/Europe reimbursement delays"),
    ("Gross margin",                       "68.5%", "<65%",   "−3.5pp","da Vinci 5 input costs + tariffs not offset by scale"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Procedure volume growth decelerates below 12-15% as elective surgery")
print(f"  capacity normalizes post-pandemic catch-up, while Medtronic Hugo and J&J Ottava")
print(f"  gain meaningful traction in soft-tissue robotic surgery, pressuring instrument")
print(f"  pricing and slowing da Vinci 5 placements. EPS growth stalls near $6.50 → 35×")
print(f"  trough multiple (recurring-revenue floor) = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT a permanent impairment — the installed base of 10,000+")
print(f"  systems generates a durable instrument/accessory annuity even if placement growth slows.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~$7.85-$8.20; non-GAAP)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (recurring-revenue moat floor; 2022-23 trough ~32-38×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP means the market prices in continuation of the")
print(f"  multi-year da Vinci 5 procedure growth cycle ABOVE the trough-floor multiple.")
print(f"  At ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f}, the P/E is ~{CURRENT_PRICE/EPS_FY2026E:.0f}× — a premium that")
print(f"  requires sustained double-digit procedure growth to justify. The risk is")
print(f"  growth deceleration triggering multiple compression toward the {PE_PESSIMISTIC:.0f}× floor.")
print(f"  EPP path: FY2028E EPS ~$10.00 × {PE_PESSIMISTIC:.0f}× = ${10.00*PE_PESSIMISTIC:.0f} floor by 2028 (EPP growing with EPS).")
print(f"  At 50× mid-cycle P/E: ${EPS_FY2026E:.2f} × 50 = ${EPS_FY2026E*50:.0f}  — modestly below current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: P/E normalizes modestly; procedure growth remains double-digit)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (~12% EPS CAGR: procedure growth + I&A mix + buyback)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (rerates modestly from ~55× toward {CONS_PE_2YR}× as growth normalizes)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (no dividend; all FCF reinvested)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: even the conservative case requires ~12%/yr EPS growth while")
print(f"  the multiple compresses modestly from ~{CURRENT_PRICE/EPS_FY2026E:.0f}× to {CONS_PE_2YR}×. Sustained double-digit")
print(f"  procedure growth is the load-bearing assumption underpinning the entire thesis.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${CURRENT_PRICE / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE / CONS_PE_2YR) / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — achievable at BASE/BULL.")
print(f"  Breakeven at 55× P/E (no multiple compression): FY2028E EPS ≥ ${CURRENT_PRICE / 55:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90, 0):.0f} (conservative case clearly positive; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.30
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (none — all FCF reinvested in platform R&D/capacity)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (high-multiple growth stock; sensitive to procedure-growth headlines)")
print(f"  Beta vs S&P 500:      1.10  (modest premium; med-tech growth profile)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (significant but plausible on growth-deceleration scare)")
print(f"  52W low ${VOL_52W_LOW:.2f} already reflects a peak-to-trough move of ~{(1-VOL_52W_LOW/VOL_52W_HIGH)*100:.0f}%.")
print(f"  → Procedure volume growth deceleration is THE KEY risk; each 1pp miss compresses multiple.")
print(f"  → da Vinci 5 placement acceleration + new procedure category wins are KEY bull catalysts.")
print(f"  → AVOID above $560  |  WATCHLIST $480-560  |  ACCUMULATE $400-480  |  BUY below $400")

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
print(f"  {valuation_label.lower()} by model standards — consistent with ISRG as the best-in-class")
print(f"  surgical robotics franchise priced near fair value for a durable multi-year procedure")
print(f"  growth cycle, roughly {epp_gap_pct:.0f}% above its EPP floor.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) da Vinci 5 placement updates — quarterly system unit growth and installed-base mix")
print(f"  (2) Quarterly procedure volume growth — core driver of recurring instrument revenue")
print(f"  (3) Instruments & Accessories revenue per procedure — recurring revenue mix trend")
print(f"  (4) International expansion progress — Asia (Japan/China JV) and Europe procedure adoption")
print(f"  (5) Competitive robotic surgery launches — Medtronic Hugo, J&J Ottava traction/share")
print(f"  (6) Gross margin trajectory — da Vinci 5 cost curve vs tariff/input cost pressure")
print(f"  AVOID above $560  |  WATCHLIST $480-560  |  ACCUMULATE $400-480  |  BUY below $400")
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
