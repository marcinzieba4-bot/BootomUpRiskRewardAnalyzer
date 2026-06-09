"""
AAPL  ·  Apple Inc.  ·  NASDAQ: AAPL
Bottom-up signal model  ·  Consumer Technology / iPhone / Services / AI
Date: 2026-05-21
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "AAPL"
COMPANY       = "Apple Inc."
SECTOR        = "Consumer Technology · iPhone · Services · Apple Intelligence · NASDAQ: AAPL"
CURRENT_PRICE = 302.25       # USD; as of 2026-05-21
VOL_52W_LOW   = 169.21       # April 2026 tariff/China-war trough
VOL_52W_HIGH  = 259.81       # December 2025 pre-tariff peak (pre-AI-re-rating)
SHARES_OUT_M  = 15_050.0     # millions; declining ~3%/yr via buyback ($95B+ authorization)

# Dividend: 47-year growth streak; growing ~4%/yr
ANNUAL_DIV    = 1.04         # $/share FY2026 ($0.26/quarter)

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("iPhone",             215.0, 152.0, 255.0, "AI iPhone 17 cycle; China headwinds the swing factor"),
    ("Services",           107.0,  86.0, 135.0, "App Store + subs + ads; 75%+ gross margin; 13%+ CAGR"),
    ("Mac",                 42.0,  36.0,  52.0, "M4 Ultra refresh; Apple Intelligence boosts switchers"),
    ("iPad",                 9.5,   7.5,  12.0, "AI-enabled; declining priority but stable"),
    ("Wearables/Home/Acc",  42.0,  28.0,  55.0, "AirPods AI; Apple Watch Ultra; Vision Pro ramp optionality"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.468   # blended gross margin FY2026E (~46.8%; Services lifts blend)
GROSS_MARGIN_BULL = 0.490   # BULL: Services reaches 30% of revenue; blend lifts further
OPEX_FIXED_B      = 57.0    # R&D + SG&A ($B); grows ~5%/yr; largely fixed cost base
TAX_RATE          = 0.163   # effective rate; R&D credits; offshore (Ireland/Netherlands)

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 7.50        # FY2026E adj EPS (consensus $7.40–$7.65; non-GAAP)
PE_PESSIMISTIC = 20.0        # trough P/E: Services mix commands premium even at crisis
                              # (FY2022-23 trough ~22×; incl. China-ban scenario: 20×)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $150

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 5.00, 20,  100, "China hardware ban + tariffs; iPhone −30%; EPS $5 → 20× floor P/E"),
    "BASE":  ( 8.50, 26,  221, "AI features modest; China stable/flat; Services+13%; EPS $8.50 at FY2028E → 26×"),
    "BULL":  (11.50, 34,  391, "AI iPhone supercycle 2027; India scales; Services $135B; EPS $11.50 → 34×"),
    "XBULL": (16.00, 36,  576, "AAPL becomes AI platform; Vision Pro mainstream; Services $180B; EPS $16 → 36×"),
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
        "name":       "iPhone revenue YoY growth",
        "weight":     0.30,
        "thresholds": ("<0%",    "≥3%",   "≥8%",    "≥15%"),
        "now":        "+3%",
        "score":      2,
        "comment":    "AI iPhone 17 mild cycle; China -11% drags blended; India emerging (+18%) offsets partially",
    },
    {
        "name":       "Services revenue YoY growth",
        "weight":     0.25,
        "thresholds": ("<8%",    "≥10%",  "≥16%",   "≥22%"),
        "now":        "+13%",
        "score":      3,
        "comment":    "App Store +12%; Advertising +25%; Apple One/iCloud subs steady; 75%+ gross margin; $107B ARR",
    },
    {
        "name":       "China revenue YoY",
        "weight":     0.20,
        "thresholds": ("<-15%",  "≥-5%",  "≥+3%",   "≥+10%"),
        "now":        "-11%",
        "score":      1,
        "comment":    "Huawei Mate recovery (-6pp share); US tariffs raising iPhone price in China; Q1 FY2026 -11% YoY",
    },
    {
        "name":       "Apple Intelligence daily active user penetration",
        "weight":     0.15,
        "thresholds": ("<10%",   "≥20%",  "≥45%",   "≥65%"),
        "now":        "~22%",
        "score":      2,
        "comment":    "Feature set expanding (Writing Tools, Image Playground, Siri+); strong iOS 18.4 uptake; not yet transformative",
    },
    {
        "name":       "Blended gross margin",
        "weight":     0.05,
        "thresholds": ("<44%",   "≥45%",  "≥47%",   "≥49%"),
        "now":        "46.8%",
        "score":      3,
        "comment":    "Services (75%+ margin) lifting blended rate; structural improvement; Q2 FY2026 record 46.9%",
    },
    {
        "name":       "Active installed base (devices)",
        "weight":     0.05,
        "thresholds": ("<2.0B",  "≥2.1B", "≥2.3B",  "≥2.6B"),
        "now":        "2.2B",
        "score":      3,
        "comment":    "Record 2.2B active devices; iOS 18 penetration >80%; ecosystem lock-in structural moat",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Installed-base moat — 2.2B active devices; 89% iOS retention rate; ecosystem lock-in",       +0.7, 0.25),
    ("+", "Services flywheel — $107B ARR at 75%+ margin; App Store monopoly; payments; advertising",    +0.6, 0.20),
    ("-", "China structural drag — 17% of revenue; Huawei comeback; tariff/ban escalation risk",         -0.8, 0.20),
    ("-", "AI commoditization — Apple Intelligence = Google Gemini API; no proprietary frontier model",  -0.6, 0.20),
    ("+", "Capital return machine — $95B+ buyback; 47-yr dividend growth; $60B+ annual FCF",            +0.3, 0.10),
    ("-", "Valuation compression risk — 40× FY2026E P/E for 7%/yr EPS compounder; PEG ~5.7×",          -0.4, 0.05),
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
CONS_EPS_2YR  = 8.50    # conservative FY2028E: 7% EPS CAGR; China headwind; Services continues
CONS_PE_2YR   = 25      # rerating from 40× to growth-justified 25× (in line with PEG ~3.5×)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Consumer Technology / iPhone / Services / AI")
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
    print(f"  {seg:<26}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<26}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
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
shares_b  = shares * 0.94   # ~3%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift to iPhone (lower margin)
bear_oi   = bear_gp - OPEX_FIXED_B * 0.97           # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 34× = ~${bull_eps_imp*34:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 20× trough P/E (Services floor) = ~${bear_eps_imp*20:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
china_delta_1pp = sum(r for _, r, _, _, _ in SEG_DATA if "iPhone" in _) * 0.17 / 100 / 100  # 1pp china share = 1pp of iPhone China
# Simpler: $1B China revenue = ~$0.045 EPS
eps_per_1B_china = 1.0 * 0.38 * (1 - TAX_RATE) / shares   # iPhone-level margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Services revenue:      +${eps_per_1B_rev * 0.75 * (1-TAX_RATE):.3f}/EPS  = +${eps_per_1B_rev*0.75*(1-TAX_RATE)*26:.1f}/share at 26× P/E")
print(f"  China revenue ±$1B (38% margin): ±${eps_per_1B_china:.3f}/EPS  =  ±${eps_per_1B_china*26:.1f}/share at 26× P/E")
print(f"  1pp GM expansion (mix/pricing):  +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*26:.1f}/share at 26× P/E")
print(f"  1% buyback (150M shares):        +${curr_eps*0.01:.3f}/EPS  (mechanical accretion; ~${95:.0f}B authorization)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (iPhone cycle / Services / China / AI penetration framework)")
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
    ("iPhone revenue YoY",            "+3%",    "<0%",    "−3pp",   "Executive Order banning US components in Huawei + tariff 125%"),
    ("China revenue YoY",             "-11%",   "<-30%",  "−19pp",  "Full hardware ban + WeChat/iCloud removal from Chinese stores"),
    ("Services revenue YoY",          "+13%",   "<8%",    "−5pp",   "DOJ App Store structural remedy; 30% commission reduced to 12%"),
    ("Apple Intelligence DAU %",      "~22%",   "<10%",   "−12pp",  "Gemini API reliability issues; feature set fails vs Android"),
    ("Blended gross margin",          "46.8%",  "<44%",   "−2.8pp", "iPhone mix + tariff cost absorption; no Services offset"),
    ("Active installed base",         "2.2B",   "<2.0B",  "−0.2B",  "China ban forces 250M device ecosystem exit"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Executive Order banning sale of US-designed chips/components to Chinese")
print(f"  manufacturers, combined with Chinese government retaliation removing Apple from app")
print(f"  stores. China is $65–70B iPhone revenue (~30% of iPhone; 17% of total). Simultaneous")
print(f"  DOJ App Store remedy cuts commission rate. EPS collapses to ~$5 → 20× floor = ${bear_price}.")
print(f"  Note: $100 is NOT a permanent impairment — Services ($86B floor) + 2.0B device base")
print(f"  provides a durable earnings floor. Recovery to ~${bear_price+50}–${bear_price+80} in 2yr is base case post-shock.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus $7.40–$7.65; non-GAAP; GAAP ~$6.85)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (Services mix floor; FY2022-23 trough 22×; China-ban ~20×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP means the market prices in 5–6 years of uninterrupted")
print(f"  earnings growth ABOVE the trough-floor multiple. At $302.25 and FY2026E EPS $7.50,")
print(f"  the P/E is 40× — a PEG of ~5.7× on 7%/yr EPS growth. This is the 'premium brand tax':")
print(f"  investors pay for certainty of future cash flows. The risk is mean reversion.")
print(f"  EPP path: FY2028E EPS ~$8.75 × {PE_PESSIMISTIC:.0f}× = ${8.75*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing ~8%/yr).")
print(f"  At 25× mid-cycle P/E: ${EPS_FY2026E:.2f} × 25 = ${EPS_FY2026E*25:.0f}  — still 41% below current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: P/E rerates toward growth rate; China headwind persists)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (7% EPS CAGR: buyback ~3%/yr + EPS growth ~4%/yr)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (rerates from 40× toward growth-justified 25×; still premium)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; 47-yr growth streak)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE PROBLEM: even the conservative case requires P/E compression from 40× to 25×.")
print(f"  That 38% multiple contraction offsets 7% annual EPS growth — a negative total return.")
print(f"  For conservative 2yr to break even at 25× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~${((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — possible at BULL, not BASE.")
print(f"  Breakeven at 30× P/E (no multiple compression): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 30:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at 25× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.28
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: 52W high pre-dates AI-re-rating surge in Jan–May 2026 (+$42 to current $302.25)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  token; Dividend Aristocrat)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (lower than peers; brand stability; but China binary elevated)")
print(f"  Beta vs S&P 500:      1.15  (slight premium; mega-cap; China trade war amplifier)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (extreme; China-ban tail scenario)")
print(f"  52W low ${VOL_52W_LOW:.2f} (Apr 2026 tariff panic) already a peak-to-trough move of ~35%.")
print(f"  → China trade war escalation is THE KEY binary; each tariff escalation = −10–15% move.")
print(f"  → Apple Intelligence monetisation evidence (Services ARPU acceleration) is KEY bull catalyst.")
print(f"  → AVOID at current price  |  WATCHLIST $235–255  |  ACCUMULATE $195–215  |  BUY below $185")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is ABOVE the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0 — between")
print(f"  BULL and XBULL. The model scores the fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0 — between BASE and BULL.")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: you are paying BULL scenario prices for what is currently BASE execution.")
print(f"  China headwinds (signal score 1/4 = BEAR) are the most significant valuation mismatch.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) China trade war de-escalation — tariff deal restoring iPhone competitiveness (BULL trigger)")
print(f"  (2) Apple Intelligence monetisation — Services ARPU acceleration above +16%/yr (BULL trigger)")
print(f"  (3) DOJ App Store remedy — structural commission cut risks ~$8–12B annual Services revenue")
print(f"  (4) India ramp — 1.4B population, growing middle class; can India replace China by 2030?")
print(f"  (5) Vision Pro mainstream — current niche ($3,499); any sub-$1,500 mass-market version?")
print(f"  AVOID at ${CURRENT_PRICE:.2f}  |  WATCHLIST $235–255  |  ACCUMULATE $195–215  |  BUY below $185")
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
