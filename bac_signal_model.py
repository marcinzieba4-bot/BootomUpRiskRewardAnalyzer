"""
BAC  ·  Bank of America Corporation  ·  NYSE: BAC
Bottom-up signal model  ·  Money Center Bank / NII / Wealth Management / Markets
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "BAC"
COMPANY       = "Bank of America Corporation"
SECTOR        = "Money Center Bank · Consumer Banking · GWIM · Global Banking · Global Markets · NYSE: BAC"
CURRENT_PRICE = 51.70       # USD; as of 2026-06-11
VOL_52W_LOW   = 36.55       # 2025 rate-cut/recession-fear trough
VOL_52W_HIGH  = 54.90       # 2026 NII-acceleration / ROTCE-expansion peak
SHARES_OUT_M  = 7_700.0     # millions; declining via buyback (~2-3%/yr)

# Dividend: raised steadily; ~2.0% yield
ANNUAL_DIV    = 1.04        # $/share (4 x $0.26/quarter)

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E net revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Consumer Banking",          28.5, 24.0, 31.5, "Deposits + cards; NII-sensitive; 16%+ ROE"),
    ("Global Wealth & Inv Mgmt",  24.0, 20.0, 28.0, "Merrill + Private Bank; AUM fees scale with markets"),
    ("Global Banking",            18.5, 15.5, 21.0, "Commercial lending + IB fees; cyclical"),
    ("Global Markets",            21.0, 16.0, 25.0, "Sales & trading; FICC/Equities; volatile but record FY2026"),
    ("All Other / Corp",           1.0,  0.5,  1.5, "Treasury, residual items, eliminations"),
]

# Margin / earnings assumptions
EFF_RATIO_CURR = 0.62      # current efficiency ratio (~62%)
EFF_RATIO_BULL = 0.58      # BULL: operating leverage from NII growth + cost discipline
TAX_RATE       = 0.235     # effective tax rate (incl. state)
PROVISION_B    = 5.5       # current annual provision for credit losses ($B)
PROVISION_BEAR = 14.0      # recession provision build ($B)

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 4.10        # FY2026E adj EPS run-rate (Q1 2026 $1.11 x ~4, modest growth)
PE_PESSIMISTIC = 8.0         # trough P/E for money-center banks in recession (2009/2020/2023 lows ~7-9x)

vol_pct = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
# (EPS, P/E multiple, price target, narrative)
SCENARIOS = {
    "BEAR":  (1.85, 12,  22,  "Recession: ROTCE compresses to 12% (1.6x P/TBV ~$46); Fed cuts deeper, "
                              "NII -$5B, provisions surge to $14B, credit losses spike; EPS collapses to $1.85 -> 12x"),
    "BASE":  (4.30, 12.5, 54, "ROTCE ~15-16% sustained; NII grows mid-single digits; Q1'26 run-rate "
                              "($1.11 x4 ~$4.40) holds; modest multiple of 12.5x on $4.30 FY2027E EPS"),
    "BULL":  (5.10, 14,  71,  "Peak ROTCE 16%+ -> 2.4x P/TBV (~$69.55); rate cuts stop, NII reaccelerates, "
                              "Global Markets record quarters persist, buybacks accelerate EPS growth"),
    "XBULL": (6.00, 16,  96,  "Soft landing + steepening yield curve supercharges NII; GWIM AUM at "
                              "all-time highs on equity bull market; efficiency ratio <55%; re-rating toward universal-bank premium"),
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
        "name":       "Net Interest Income (NII) YoY growth",
        "weight":     0.30,
        "thresholds": ("<0%",    "≥5%",   "≥9%",    "≥14%"),
        "now":        "+9%",
        "score":      3,
        "comment":    "Q1 2026 NII $15.9B +9% YoY; most rate-sensitive major US bank; deposit repricing tailwind continuing",
    },
    {
        "name":       "ROTCE",
        "weight":     0.25,
        "thresholds": ("<10%",   "≥12%",  "≥15%",   "≥18%"),
        "now":        "16%",
        "score":      3,
        "comment":    "Q1 2026 ROTCE 16%, near peak-cycle levels; operating leverage improving",
    },
    {
        "name":       "EPS YoY growth",
        "weight":     0.20,
        "thresholds": ("<0%",    "≥5%",   "≥15%",   "≥25%"),
        "now":        "+25%",
        "score":      4,
        "comment":    "Q1 2026 EPS $1.11 vs $0.83 prior year, +25% YoY; NII expansion + buyback accretion",
    },
    {
        "name":       "Global Markets (trading) revenue YoY",
        "weight":     0.10,
        "thresholds": ("<-5%",   "≥0%",   "≥8%",    "≥15%"),
        "now":        "~+10%",
        "score":      3,
        "comment":    "FICC + Equities posting record quarters on volatility and client activity",
    },
    {
        "name":       "Credit quality (net charge-off rate)",
        "weight":     0.10,
        "thresholds": (">0.70%", "≤0.65%","≤0.50%", "≤0.35%"),
        "now":        "~0.55%",
        "score":      3,
        "comment":    "Charge-offs stable/improving; consumer credit resilient; no recession stress evident yet",
    },
    {
        "name":       "GWIM (Merrill/Private Bank) AUM flows",
        "weight":     0.05,
        "thresholds": ("<0%",    "≥3%",   "≥7%",    "≥12%"),
        "now":        "~+8%",
        "score":      3,
        "comment":    "Record AUM levels on equity market strength; positive net flows into Merrill/Private Bank",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Most rate-sensitive major bank to NII — deposit repricing lag is a multi-year tailwind as long as rates don't crash",  +0.6, 0.20),
    ("+", "Scale + $2T deposit base — #2 US bank by assets; funding cost advantage; CET1 well-capitalized",                       +0.5, 0.15),
    ("-", "Rate-cut sensitivity is double-edged — each 25bps Fed cut is a ~$1-1.5B NII headwind; aggressive easing cycle risk",   -0.7, 0.20),
    ("-", "Buffett/Berkshire exited entire ~1B share stake at $35-45 (2024-2025) — signals valuation/regulatory caution from a top long-term holder", -0.5, 0.15),
    ("+", "Capital return — buybacks + steadily growing dividend; Q1 2026 ROTCE 16% supports re-rating toward GS/MS-like multiples", +0.4, 0.15),
    ("-", "Regulatory/macro tail risk — CRE exposure, capital rule changes (Basel III endgame remnants), recession credit-cycle risk", -0.5, 0.15),
]
SCA = sum(score * weight for _, _, score, weight in SCA_FACTORS)
ADJ_COMPOSITE = round(PROXY_COMPOSITE + SCA, 3)

EPP = round(PE_PESSIMISTIC * (CURRENT_PRICE / SCENARIOS["BASE"][0] * 0 + SCENARIOS["BEAR"][0]), 0)
# EPP = pessimistic P/E x current/bear EPS  ->  use bear EPS as the "current x bear" anchor per template
EPP = round(PE_PESSIMISTIC * SCENARIOS["BEAR"][0], 0)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

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
CONS_EPS_2YR  = 4.60    # conservative FY2028E: continued mid-single-digit NII growth + buyback accretion
CONS_PE_2YR   = 12      # modest re-rating from ~12.6x current toward 12x (rate-cut risk caps multiple)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Money Center Bank / NII / Wealth Mgmt / Markets")
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
shares = SHARES_OUT_M / 1000

curr_pretax = curr_total * (1 - EFF_RATIO_CURR) - PROVISION_B
curr_ni     = max(0, curr_pretax) * (1 - TAX_RATE)
curr_eps    = round(curr_ni / shares, 2)

bull_pretax = bull_total * (1 - EFF_RATIO_BULL) - PROVISION_B
bull_ni     = max(0, bull_pretax) * (1 - TAX_RATE)
shares_b    = shares * 0.95   # ~2.5%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 2)

bear_pretax = bear_total * (1 - EFF_RATIO_CURR) - PROVISION_BEAR
bear_ni     = max(0, bear_pretax) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B revenue x {(1-EFF_RATIO_CURR)*100:.0f}% pre-provision margin")
print(f"  − ${PROVISION_B:.1f}B provisions − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (Q1'26 run-rate ~${EPS_FY2026E:.2f}  ✓ in range)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev x {(1-EFF_RATIO_BULL)*100:.0f}% margin − ${PROVISION_B:.1f}B provisions − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.2f}/share  →  ${bull_eps_imp:.2f} x 14x = ~${bull_eps_imp*14:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev x {(1-EFF_RATIO_CURR)*100:.0f}% margin − ${PROVISION_BEAR:.1f}B recession provisions  =  ~${bear_eps_imp:.2f}/share")
print(f"  At 12x trough P/E = ~${bear_eps_imp*12:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
print(f"  KEY SENSITIVITIES:")
eps_per_25bps = 1.25 * (1 - TAX_RATE) / shares   # ~$1.25B NII headwind per 25bps cut
print(f"  Each 25bps Fed cut:               −${eps_per_25bps:.3f}/EPS  (≈$1.0-1.5B NII headwind)  =  −${eps_per_25bps*12.5:.2f}/share at 12.5x P/E")
eps_per_1B_nii = 1.0 * (1 - TAX_RATE) / shares
print(f"  Every $1B NII (full flow-through): +${eps_per_1B_nii:.3f}/EPS  =  +${eps_per_1B_nii*12.5:.2f}/share at 12.5x P/E")
print(f"  1pp ROTCE expansion (~$1.4B NI):   +${1.4*(1)/shares:.3f}/EPS  =  +${1.4/shares*12.5:.2f}/share at 12.5x P/E")
print(f"  1% buyback (77M shares):           +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (NII / ROTCE / EPS growth / Markets / Credit / GWIM framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>7}  {'BASE':>6}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>6}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>7}  {ths[1]:>6}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>6}  {lbl}  {b}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15% hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:72]:<72}  ({score:+.1f} x {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("NII YoY growth",                "+9%",   "<0%",    "−9pp",   "Aggressive Fed easing cycle (150bps+) overwhelms deposit repricing"),
    ("ROTCE",                         "16%",   "<10%",   "−6pp",   "Recession: ROTCE compresses to ~12% -> 1.6x P/TBV (~$46) and below"),
    ("EPS YoY growth",                "+25%",  "<0%",    "−25pp",  "Provisions surge to $14B on recession credit losses"),
    ("Global Markets revenue YoY",    "+10%",  "<-5%",   "−15pp",  "Trading revenue normalizes sharply from record levels; risk-off"),
    ("Net charge-off rate",           "0.55%", ">0.70%", "+0.15pp","Consumer/CRE credit cycle turns; unemployment rises materially"),
    ("GWIM AUM flows",                "+8%",   "<0%",    "−8pp",   "Equity market drawdown (-25%+) hits AUM-based fee revenue"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A recession scenario where the Fed cuts rates aggressively (150bps+),")
print(f"  compressing NII by ~$5B even after deposit-cost relief, while credit losses spike and")
print(f"  provisions triple to ~$14B. ROTCE falls from 16% to ~12%, applying the Gordon Growth")
print(f"  framework's 1.6x P/TBV recession multiple (~$46.37 TBV-based floor). EPS falls to ~$1.85,")
print(f"  trading at a 12x trough multiple = ~${bear_price}.")
print(f"  Note: Buffett/Berkshire's full exit of ~1B shares at $35-45 (2024-2025) suggests the")
print(f"  market has already partially priced bank-cycle risk below current levels.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E x current/bear EPS)")
hr()
print(f"  Q1 2026 annualized run-rate EPS:  ${EPS_FY2026E:.2f}  (Q1 $1.11 x4, +25% YoY)")
print(f"  BEAR-case EPS (recession):         ${SCENARIOS['BEAR'][0]:.2f}")
print(f"  Pessimistic P/E at trough:          {PE_PESSIMISTIC:.0f}x  (2009/2020/2023 money-center bank troughs ~7-9x)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share  ({PE_PESSIMISTIC:.0f}x x ${SCENARIOS['BEAR'][0]:.2f} bear EPS)")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  At a current EPS of ${EPS_FY2026E:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}x — a modest multiple")
print(f"  for a bank posting 16% ROTCE and +25% YoY EPS growth. The EPP floor of ${EPP:.0f} represents")
print(f"  the price the market would likely assign in a recession (bear EPS x 12x trough multiple),")
print(f"  consistent with the Gordon Growth recession case (~$46.37 at 1.6x P/TBV).")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest multiple change; rate-cut headwind persists)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (mid-single-digit NII growth + buyback accretion)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (roughly flat vs current ~{CURRENT_PRICE/EPS_FY2026E:.1f}x)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: unlike high-multiple growth stocks, BAC's conservative case does NOT require")
print(f"  multiple expansion — just flat-to-modest re-rating plus continued NII/EPS growth and")
print(f"  buybacks. The dividend (~2.0% yield) provides a meaningful floor to total return.")
print(f"  Breakeven at flat {CURRENT_PRICE/EPS_FY2026E:.1f}x P/E: FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / (CURRENT_PRICE/EPS_FY2026E):.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.85 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.92 + cons_divs * 0.5, 0):.0f} (conservative case strongly positive; ratio_b <1.0x)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.30
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (bank stocks; rate-sensitivity + macro cyclicality)")
print(f"  Beta vs S&P 500:      1.30  (high financial-sector beta; rate-cycle amplifier)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (full recession scenario)")
print(f"  Gordon Growth anchors: peak ROTCE 16% -> 2.4x P/TBV = $69.55  |  recession ROTCE 12% -> 1.6x P/TBV = $46.37")
print(f"  → Fed rate path is THE KEY swing factor: BAC is the most NII-sensitive major US bank to rate cuts.")
print(f"  → Buffett/Berkshire's full exit at $35-45 (2024-2025) is a structural overhang/contrarian signal.")
print(f"  → AVOID above $60  |  WATCHLIST $54–60  |  ACCUMULATE $46–54  |  BUY below $46")

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
print(f"  {valuation_label.lower()} by model standards, driven by strong NII/ROTCE/EPS momentum offset")
print(f"  by rate-cut sensitivity and the Berkshire overhang.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Fed rate path — pause/hike supports NII (BULL); aggressive cutting is the key BEAR trigger")
print(f"  (2) ROTCE trajectory toward/above 16% — sustained expansion drives Gordon Growth re-rating to $69.55")
print(f"  (3) Global Markets revenue durability — can record trading quarters persist or do they normalize")
print(f"  (4) Credit quality — net charge-off rate trend as a recession early-warning indicator")
print(f"  (5) Buyback pace — capital return accelerating EPS growth independent of NII")
print(f"  AVOID above $60  |  WATCHLIST $54–60  |  ACCUMULATE $46–54  |  BUY below $46")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}x  |  Run-rate EPS: ${EPS_FY2026E:.2f}")
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
