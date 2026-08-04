"""
LLY  ·  Eli Lilly and Company  ·  NYSE: LLY
Bottom-up signal model  ·  GLP-1 (Zepbound/Mounjaro/Foundayo) / Pipeline (Donanemab/Verzenio) / Premium Valuation
Date: 2026-08-04
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "LLY"
COMPANY       = "Eli Lilly and Company"
SECTOR        = "Pharma · GLP-1 (Zepbound/Mounjaro/Foundayo) · Alzheimer's (Kisunla) · Oncology (Verzenio) · NYSE: LLY"
CURRENT_PRICE = 1_121.36    # USD; close 2026-08-03
VOL_52W_LOW   =   623.78    # USD
VOL_52W_HIGH  = 1_249.45    # USD
SHARES_OUT_M  = 892.0       # millions
ANNUAL_DIV    = 6.92        # $/share; small but growing fast off a low payout ratio

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# NOTE: Q2 2026 results have NOT yet been reported as of this refresh — Lilly reports
# tomorrow, Aug 5, 2026. This model is built on Q1 2026 actuals (Mounjaro+Zepbound $12.82B
# combined, ~65% of revenue) and FY2026 guidance: revenue $82.0-85.0B, adj EPS $35.50-37.00
# (consensus ~$34.51, +42% YoY). FY2027 consensus EPS ~$45.14. Foundayo (orforglipron, the
# oral GLP-1 pill) launched April 2026 with an encouraging early ramp — 20,000+ patients
# treated, 80% new-to-class — a real proof point for the category-expansion thesis.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Mounjaro/Zepbound (tirzepatide)",  52.0, 38.0,  64.0, "Combined GLP-1 incretin franchise; Q1 2026 alone was $12.82B, ~65% of revenue"),
    ("Foundayo (orforglipron, oral GLP-1)", 4.0,  1.0,  12.0, "Launched Apr 2026; 20,000+ patients treated, 80% new-to-class — early proof of category expansion"),
    ("Verzenio (oncology, CDK4/6)",       8.5,  7.0,  10.0, "Adjuvant breast cancer label drives steady double-digit growth"),
    ("Donanemab/Kisunla (Alzheimer's)",   2.0,  0.8,   4.5, "Early-stage launch; reimbursement/diagnostic infrastructure the swing factor"),
    ("Trulicity/Jardiance/Established",   9.5,  7.5,  10.5, "Legacy diabetes/CV portfolio; Trulicity cannibalized by tirzepatide but Jardiance steady"),
    ("Other (immunology/rare disease)",   7.5,  6.2,   9.0, "Taltz, Olumiant, smaller franchises; mid-single-digit growth"),
]

# Net-margin-based bridge
NET_MARGIN_CURR = 0.3872   # FY2026E; reconciles to raised guidance midpoint
NET_MARGIN_BEAR = 0.3539   # BEAR: competitive share loss + pricing pressure compress margin
NET_MARGIN_BULL = 0.4217   # BULL: continued GLP-1 scale economies expand margin further

# ── GLP-1 SCALE / ORAL LAUNCH TRACKER (the Lilly-specific angle) ──────────────
Q1_2026_TIRZEPATIDE_REV_B     = 12.82   # $B, Q1 2026 Mounjaro+Zepbound combined
FOUNDAYO_PATIENTS_TREATED     = 20_000  # patients treated since April 2026 launch
FOUNDAYO_NEW_TO_CLASS_PCT     = 80      # % of Foundayo patients new to the GLP-1 class
FY2026_GUIDANCE_EPS_RANGE     = "35.50-37.00"  # $ non-GAAP, FY2026 guidance
Q2_EARNINGS_DATE               = "2026-08-05"  # tomorrow — the next real catalyst
STOCK_MOVE_FROM_JUNE_LOW_PCT  = round((CURRENT_PRICE - 825.00) / 825.00 * 100, 1)  # move since last refresh

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 36.25       # FY2026E EPS (guidance $35.50-37.00; midpoint)
PE_PESSIMISTIC = 24.0        # pessimistic P/E: premium-grower floor; even a GLP-1 competitive scare likely holds ~22-26×
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (24.00, 24,  576, "Novo Nordisk next-gen competition erodes GLP-1 pricing/share; Foundayo uptake stalls; EPS $24 → 24× = $576"),
    "BASE":  (36.25, 30.93, 1121, "Mounjaro/Zepbound continue strong growth as supply constraints ease; Foundayo scales steadily; Verzenio steady; EPS $36.25 → 31× = $1121"),
    "BULL":  (52.00, 28,  1456, "Foundayo becomes a blockbuster oral franchise expanding total GLP-1 TAM; donanemab uptake accelerates; international access expands; EPS $52 → 28× = $1456"),
    "XBULL": (62.00, 32, 1984, "LLY achieves durable GLP-1 category dominance across obesity/diabetes/cardiometabolic with minimal share loss to Novo; pipeline becomes a second growth engine; EPS $62 → 32× = $1984"),
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
        "name":       "Mounjaro/Zepbound combined revenue YoY growth",
        "weight":     0.30,
        "thresholds": ("<25%",  "≥40%",  "≥60%",   "≥80%"),
        "now":        "+45%",
        "score":      2,
        "comment":    "Combined incretin franchise still scaling off a now-massive base; growth naturally decelerating from triple-digit early years",
    },
    {
        "name":       "Foundayo (orforglipron) launch trajectory",
        "weight":     0.20,
        "thresholds": ("delayed/weak", "on-track modest", "strong uptake", "category-expanding blockbuster"),
        "now":        "strong early uptake",
        "score":      3,
        "comment":    "20,000+ patients treated since April launch, 80% new-to-class — real early evidence the oral pill is expanding the category, not just cannibalizing injectables",
    },
    {
        "name":       "GLP-1 manufacturing capacity / supply-demand balance",
        "weight":     0.15,
        "thresholds": ("severe shortage", "constrained", "balanced",  "surplus capacity"),
        "now":        "constrained, improving",
        "score":      2,
        "comment":    "Multi-billion dollar capex expansion (US/Europe sites) easing shortages; still constrained in some dose strengths/markets",
    },
    {
        "name":       "Competitive dynamics vs Novo Nordisk / oral entrants",
        "weight":     0.15,
        "thresholds": ("share loss accelerating", "share roughly stable", "LLY gaining share", "LLY gaining share + price holds"),
        "now":        "LLY gaining share",
        "score":      3,
        "comment":    "Tirzepatide head-to-head data favors LLY vs semaglutide; Novo execution stumbles have allowed LLY to gain incretin share",
    },
    {
        "name":       "Donanemab (Kisunla) Alzheimer's uptake",
        "weight":     0.10,
        "thresholds": ("stalled", "slow ramp", "accelerating", "standard-of-care adoption"),
        "now":        "slow ramp, improving",
        "score":      2,
        "comment":    "Diagnostic infrastructure (amyloid PET/blood biomarkers) and reimbursement still building",
    },
    {
        "name":       "Valuation vs forward growth (PEG-adjusted)",
        "weight":     0.10,
        "thresholds": ("PEG>2.5", "PEG~1.8-2.5", "PEG~1.2-1.8", "PEG<1.2"),
        "now":        "PEG ~1.3",
        "score":      3,
        "comment":    "~31x FY2026E EPS against ~25%/yr forward EPS growth (FY2027E consensus $45.14) implies a PEG near 1.3x — rich but not as stretched as the headline multiple suggests",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "GLP-1 category leadership — tirzepatide best-in-class efficacy data; first-mover advantage now proving out in oral GLP-1 (Foundayo)", +0.7, 0.25),
    ("-", "Premium valuation still prices substantial future success even after the PEG-adjusted read looks more reasonable", -0.5, 0.20),
    ("+", "Manufacturing capex build-out — multi-billion dollar capacity expansion removes supply as a growth constraint over time", +0.5, 0.15),
    ("-", "Competitive/pricing risk — Novo Nordisk next-gen (CagriSema/oral semaglutide) + eventual generic/biosimilar incretin entrants by early 2030s", -0.5, 0.20),
    ("+", "Pipeline optionality — Foundayo's early data is real proof of diversification beyond injectable tirzepatide, plus donanemab/Verzenio", +0.5, 0.10),
    ("-", "Policy/pricing risk — US drug pricing reform (IRA negotiation), international reference pricing pressure on GLP-1 list prices", -0.3, 0.10),
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
CONS_EPS_2YR  = 48.00   # FY2028E conservative: ~15%/yr off FY2026E, below street's ~25%/yr pace
CONS_PE_2YR   = 26      # compresses modestly from ~31× as growth normalizes
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  GLP-1 (Zepbound/Mounjaro/Foundayo) / Donanemab / Verzenio")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<38}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<38}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<38}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  Q1 2026 actual: Mounjaro+Zepbound ${Q1_2026_TIRZEPATIDE_REV_B:.2f}B combined (~65% of revenue)")
print(f"  ⚠ Q2 2026 earnings report tomorrow ({Q2_EARNINGS_DATE}) — the next confirmation point for this model")
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
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (guidance ${EPS_FY2026E:.2f} midpoint  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {NET_MARGIN_BULL*100:.2f}% net margin")
print(f"  ÷ {shares:.3f}B shares  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {NET_MARGIN_BEAR*100:.2f}% net margin (competitive share loss + pricing pressure)")
print(f"  ÷ {shares:.3f}B shares  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# GLP-1 SCALE / ORAL LAUNCH TRACKER
print()
print(f"  GLP-1 SCALE / ORAL LAUNCH TRACKER  (the Lilly-specific angle):")
print(f"  Q1 2026 Mounjaro+Zepbound revenue:            ${Q1_2026_TIRZEPATIDE_REV_B:.2f}B combined")
print(f"  Foundayo patients treated since Apr launch:    {FOUNDAYO_PATIENTS_TREATED:,}+")
print(f"  Foundayo new-to-class patients:                 {FOUNDAYO_NEW_TO_CLASS_PCT}%")
print(f"  FY2026 guidance:                                EPS ${FY2026_GUIDANCE_EPS_RANGE}")
print(f"  Stock move since last refresh (Jun 10):        +{STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}%")
print()
print(f"  ⚠ This model is built entirely on Q1 2026 data and FY2026 guidance — Q2 2026 results report")
print(f"  tomorrow, {Q2_EARNINGS_DATE}. Given the stock is up {STOCK_MOVE_FROM_JUNE_LOW_PCT:.0f}% since June on Foundayo launch enthusiasm,")
print(f"  tomorrow's print (and any commentary on oral GLP-1 uptake specifically) is a real near-term")
print(f"  catalyst that could move this model's inputs meaningfully in either direction.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = 1.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at {NET_MARGIN_CURR*100:.1f}% margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*30.9:.2f}/share at 30.9× P/E")
print(f"  1pp net margin expansion (mix/scale):        +${curr_total*0.01/shares:.3f}/EPS  = +${curr_total*0.01/shares*30.9:.2f}/share at 30.9× P/E")
print(f"  Every 1 turn of P/E:                          ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (GLP-1 growth / oral launch / capacity / competition / pipeline / valuation)")
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
    ("Mounjaro/Zepbound revenue growth",   "+45%",   "<25%",   "Novo Nordisk next-gen (CagriSema) + price wars erode share/pricing"),
    ("Foundayo launch trajectory",         "strong uptake", "delayed/weak", "Efficacy/tolerability data underwhelms vs injectables; slow uptake"),
    ("Manufacturing capacity",             "constrained, improving", "severe shortage", "Capex delays/quality issues at new sites stall supply growth"),
    ("Competitive share vs Novo",          "gaining", "losing share", "Novo oral semaglutide + biosimilar entrants take meaningful share"),
    ("Donanemab uptake",                   "slow ramp", "stalled", "Reimbursement/diagnostic barriers prevent meaningful Alzheimer's revenue"),
    ("Net margin",                         "38.7%",  "<33%",   "Pricing concessions (US IRA negotiation, international reference pricing)"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>16}  {bear_v:>9}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Novo Nordisk's next-generation incretins launch with competitive efficacy and")
print(f"  aggressive pricing, Foundayo's early strong uptake proves unsustainable, and US drug-pricing")
print(f"  reform forces GLP-1 list-price cuts. EPS growth stalls to ~$24 at a 24× premium-grower floor.")
print(f"  Note: ${bear_price} is NOT permanent impairment — GLP-1 remains a multi-decade secular growth")
print(f"  market, and Lilly's pipeline (donanemab, retatrutide) provides offsetting growth vectors.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E EPS estimate:           ${EPS_FY2026E:.2f}  (guidance midpoint)")
print(f"  Pessimistic P/E:                 {PE_PESSIMISTIC:.0f}×  (premium-grower floor; even a GLP-1 competitive scare likely holds ~22-26×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  LLY trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS ${EPS_FY2026E:.2f} — a steep multiple that prices in")
print(f"  continued GLP-1 dominance and a successful Foundayo launch. The early oral-launch data (20,000+")
print(f"  patients, 80% new-to-class) is genuinely supportive, but tomorrow's Q2 print is the next real test.")
print(f"  At 34× mid-cycle P/E (FY2027E consensus $45.14): ${45.14:.2f} × 34 = ${45.14*34:.0f}  — {(45.14*34/CURRENT_PRICE-1)*100:+.0f}% vs current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: EPS growth decelerates; P/E compresses modestly from current levels)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (~15%/yr off FY2026E; below the street's ~25%/yr pace)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (compresses from ~{CURRENT_PRICE/EPS_FY2026E:.1f}× as growth normalizes toward 'mature blockbuster' multiple)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: LLY trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS — steep even for a company growing")
print(f"  EPS 25-45%/yr. The conservative case assumes deceleration to ~15%/yr AND multiple compression")
print(f"  to {CONS_PE_2YR}×. Multiple compression can offset even strong earnings growth — the central risk")
print(f"  of owning LLY at current levels, especially heading into tomorrow's earnings print.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.30
beta        = 0.75
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock is up {STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}% since the last refresh (Jun 10) on Foundayo launch momentum")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  small but growing fast off low payout ratio)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; GLP-1 headline-driven swings on competitive/clinical/earnings news)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (moderate; large-cap pharma but high growth-stock sensitivity)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (significant but plausible on a competitive or earnings shock)")
print(f"  → Tomorrow's Q2 print ({Q2_EARNINGS_DATE}) is the immediate catalyst — watch Foundayo uptake commentary specifically.")
print(f"  → Novo Nordisk competitive dynamics + US drug pricing policy are the KEY medium-term binaries.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $950  |  Trim above $1,250")

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
print(f"  {valuation_label.lower()} by model standards. In plain terms: Foundayo's early launch data is genuinely")
print(f"  encouraging, but the market is pricing in continued flawless execution — and tomorrow's Q2 print")
print(f"  is the next real confirmation point, not yet reflected in this model's fundamentals.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q2 2026 earnings ({Q2_EARNINGS_DATE}, TOMORROW) — Foundayo uptake commentary is the key line item")
print(f"  (2) Novo Nordisk competitive response — CagriSema/oral semaglutide data and pricing actions")
print(f"  (3) GLP-1 manufacturing capacity expansion — pace of supply normalization across dose strengths")
print(f"  (4) Donanemab (Kisunla) Alzheimer's ramp — diagnostic infrastructure and reimbursement progress")
print(f"  (5) US drug pricing policy (IRA negotiation) — GLP-1 list price exposure")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $950  |  Trim above $1,250")
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
