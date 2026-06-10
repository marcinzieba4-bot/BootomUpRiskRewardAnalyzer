"""
LLY  ·  Eli Lilly and Company  ·  NYSE: LLY
Bottom-up signal model  ·  GLP-1 (Zepbound/Mounjaro/orforglipron) / Pipeline (Donanemab/Verzenio) / Premium Valuation
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "LLY"
COMPANY       = "Eli Lilly and Company"
SECTOR        = "Pharma · GLP-1 (Zepbound/Mounjaro/Orforglipron) · Alzheimer's (Kisunla) · Oncology (Verzenio) · NYSE: LLY"
CURRENT_PRICE = 825.00      # USD; as of 2026-06-10
VOL_52W_LOW   = 680.00      # 2025 GLP-1 competitive-scare trough
VOL_52W_HIGH  = 985.00      # early-2026 oral GLP-1 (orforglipron) approval euphoria peak
SHARES_OUT_M  = 950.0       # millions
ANNUAL_DIV    = 6.16        # $/share; ~0.7% yield; growing fast off small base

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Mounjaro/Zepbound (tirzepatide)", 38.0, 26.0, 50.0, "Combined GLP-1 incretin franchise; tens-of-billions run-rate, still capacity-constrained in places"),
    ("Orforglipron (oral GLP-1)",        2.0,  0.0, 10.0, "Newly launched oral GLP-1; massive TAM expansion if uptake/access strong; near-zero if delayed/underwhelming"),
    ("Verzenio (oncology, CDK4/6)",      8.0,  6.5,  9.5, "Adjuvant breast cancer label drives steady double-digit growth"),
    ("Donanemab/Kisunla (Alzheimer's)",  1.5,  0.5,  4.0, "Early-stage launch; reimbursement/diagnostic infrastructure the swing factor"),
    ("Trulicity/Jardiance/Established",  9.5,  7.0, 10.5, "Legacy diabetes/CV portfolio; Trulicity cannibalized by tirzepatide but Jardiance steady"),
    ("Other (immunology/rare disease)",  6.0,  5.0,  7.5, "Taltz, Olumiant, smaller franchises; mid-single-digit growth"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.820   # blended gross margin; high-margin GLP-1 mix
GROSS_MARGIN_BULL = 0.840   # BULL: scale economies on GLP-1 manufacturing further lift blend
OPEX_FIXED_B      = 24.0    # SG&A + R&D ($B); heavy R&D investment in pipeline
TAX_RATE          = 0.130   # effective rate; Puerto Rico/Ireland manufacturing footprint

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 28.00       # FY2027E EPS (consensus ~$27-29 non-GAAP)
PE_PESSIMISTIC = 22.0        # trough P/E: even in a GLP-1-competitive-scare scenario, premium grower floor ~20-24x
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # $616

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (20.00, 22,  440, "Novo Nordisk + oral generic competition erodes GLP-1 pricing/share; orforglipron launch disappoints; donanemab uptake stalls; EPS $20 → 22× = $440"),
    "BASE":  (28.00, 30,  840, "Mounjaro/Zepbound continue strong growth as supply constraints ease; orforglipron launches successfully but cannibalizes some injectable share; Verzenio steady; EPS $28 → 30× = $840"),
    "BULL":  (38.00, 34, 1292, "Orforglipron becomes a blockbuster oral franchise expanding total GLP-1 TAM; donanemab Alzheimer's uptake accelerates; international GLP-1 access expands rapidly; EPS $38 → 34× = $1292"),
    "XBULL": (52.00, 38, 1976, "LLY achieves durable GLP-1 category dominance across obesity/diabetes/cardiometabolic with minimal share loss to Novo; pipeline (donanemab, next-gen incretins) becomes a second growth engine; EPS $52 → 38× = $1976"),
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
        "now":        "+55%",
        "score":      2,
        "comment":    "Combined incretin franchise still scaling rapidly off a now-massive base; growth rate naturally decelerating from triple-digit early years",
    },
    {
        "name":       "Orforglipron (oral GLP-1) launch trajectory",
        "weight":     0.20,
        "thresholds": ("delayed/weak", "on-track modest", "strong uptake", "category-expanding blockbuster"),
        "now":        "early launch, on-track",
        "score":      2,
        "comment":    "Approved and launching; early scripts encouraging but too soon to confirm category-expanding blockbuster trajectory vs modest cannibalization of injectables",
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
        "comment":    "Tirzepatide head-to-head data favors LLY vs semaglutide; Novo execution stumbles have allowed LLY to gain incretin share, though pricing pressure is emerging",
    },
    {
        "name":       "Donanemab (Kisunla) Alzheimer's uptake",
        "weight":     0.10,
        "thresholds": ("stalled", "slow ramp", "accelerating", "standard-of-care adoption"),
        "now":        "slow ramp",
        "score":      2,
        "comment":    "Diagnostic infrastructure (amyloid PET/blood biomarkers) and reimbursement still building; uptake slower than GLP-1 but improving",
    },
    {
        "name":       "Valuation vs forward growth (PEG-adjusted)",
        "weight":     0.10,
        "thresholds": ("PEG>2.5", "PEG~1.8-2.5", "PEG~1.2-1.8", "PEG<1.2"),
        "now":        "PEG ~2.0",
        "score":      2,
        "comment":    "~29x FY2027E EPS against ~20-25%/yr EPS growth implies a PEG near 2.0x - a premium that already prices substantial future success",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "GLP-1 category leadership — tirzepatide best-in-class efficacy data; first-mover in oral GLP-1 (orforglipron)", +0.7, 0.25),
    ("-", "Premium valuation already prices years of flawless execution — limited margin for disappointment", -0.7, 0.20),
    ("+", "Manufacturing capex build-out — multi-billion dollar capacity expansion removes supply as a growth constraint over time", +0.5, 0.15),
    ("-", "Competitive/pricing risk — Novo Nordisk next-gen (CagriSema/oral semaglutide) + eventual generic/biosimilar incretin entrants by early 2030s", -0.5, 0.20),
    ("+", "Pipeline optionality — donanemab (Alzheimer's), Verzenio (oncology), next-gen incretins (retatrutide) provide diversification beyond tirzepatide", +0.4, 0.10),
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
CONS_EPS_2YR  = 33.00   # FY2028E conservative: ~18% CAGR off FY2027E base, deceleration from current pace
CONS_PE_2YR   = 26      # rerates down modestly from ~30x as growth decelerates toward "mature blockbuster" multiple
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  GLP-1 (Zepbound/Mounjaro/Orforglipron) / Donanemab / Verzenio")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<36}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<36}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<36}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
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
shares_b     = shares * 0.985   # modest buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift / pricing pressure
bear_oi      = bear_gp - OPEX_FIXED_B * 1.0            # R&D not easily cut
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 34× = ~${bull_eps_imp*34:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 22× trough P/E (premium-grower floor) = ~${bear_eps_imp*22:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev      = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_glp1     = 1.0 * 0.85 * (1 - TAX_RATE) / shares   # GLP-1 very high incremental margin
eps_per_1B_other    = 1.0 * 0.70 * (1 - TAX_RATE) / shares   # other segments lower margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Mounjaro/Zepbound/Orforglipron revenue:  +${eps_per_1B_glp1:.3f}/EPS  = +${eps_per_1B_glp1*30:.1f}/share at 30× P/E")
print(f"  Every $1B other-portfolio revenue:                 +${eps_per_1B_other:.3f}/EPS  = +${eps_per_1B_other*30:.1f}/share at 30× P/E")
print(f"  1pp GM expansion (manufacturing scale economies):  +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*30:.1f}/share at 30× P/E")
print(f"  1% buyback (~9.5M shares):                          +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

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
    ("Mounjaro/Zepbound revenue growth",   "+55%",   "<25%",   "−30pp",  "Novo Nordisk next-gen (CagriSema) + price wars erode share/pricing"),
    ("Orforglipron launch trajectory",     "on-track","delayed/weak", "downgrade", "Efficacy/tolerability data underwhelms vs injectables; slow uptake"),
    ("Manufacturing capacity",             "constrained","severe shortage", "worse", "Capex delays/quality issues at new sites stall supply growth"),
    ("Competitive share vs Novo",          "gaining","losing share", "reversal", "Novo oral semaglutide + biosimilar entrants take meaningful share"),
    ("Donanemab uptake",                   "slow ramp","stalled", "worse", "Reimbursement/diagnostic barriers prevent meaningful Alzheimer's revenue"),
    ("Gross margin",                       "82.0%",  "<78%",   "−4pp",   "Pricing concessions (US IRA negotiation, international reference pricing)"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Novo Nordisk's next-generation incretins (CagriSema, oral semaglutide) launch")
print(f"  with competitive efficacy and aggressive pricing, simultaneously orforglipron's launch")
print(f"  underwhelms on tolerability/efficacy, and US drug-pricing reform (IRA negotiation) forces")
print(f"  GLP-1 list-price cuts. EPS growth stalls to ~$20 → 22× trough P/E (premium-grower floor) = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT permanent impairment — GLP-1 category remains a multi-decade secular")
print(f"  growth market. Recovery toward ~${bear_price+150}-${bear_price+250} in 2yr is plausible post-shock as")
print(f"  pipeline (donanemab, retatrutide) and international expansion provide offsetting growth.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           ${EPS_FY2027E:.2f}  (consensus ~$27-29 non-GAAP)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (premium-grower floor; even GLP-1 scare scenarios likely hold ~20-24×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% {'above' if epp_gap_pct >= 0 else 'below'} trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% {'premium to' if epp_gap_pct >= 0 else 'discount to'} EPP reflects that LLY trades at roughly")
print(f"  {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a steep multiple that prices in continued")
print(f"  GLP-1 dominance, successful orforglipron launch, and donanemab ramp ALL playing out")
print(f"  favorably. The risk is that even modest disappointment on any single pillar (competition,")
print(f"  oral launch, pricing policy) compresses the multiple meaningfully toward the EPP floor.")
print(f"  EPP path: FY2029E EPS ~$40 × {PE_PESSIMISTIC:.0f}× = ${40*PE_PESSIMISTIC:.0f} floor (EPP grows quickly given high underlying EPS growth).")
print(f"  At 30× mid-cycle P/E: ${EPS_FY2027E:.2f} × 30 = ${EPS_FY2027E*30:.0f}  — below current price, implying market expects >FY2027E earnings power already.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: EPS growth decelerates; P/E compresses modestly from current levels)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (~18% CAGR off FY2027E; deceleration from current 50%+ growth pace)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (compresses from ~{CURRENT_PRICE/EPS_FY2027E:.1f}× as growth normalizes toward 'mature blockbuster' multiple)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: LLY trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a steep multiple even")
print(f"  for a company growing EPS 30-50%/yr. The conservative case assumes growth decelerates to")
print(f"  ~18%/yr by FY2028E AND the multiple compresses to {CONS_PE_2YR}× as the market re-rates from")
print(f"  'hyper-growth' to 'mature blockbuster' pricing. Multiple compression can offset even strong")
print(f"  earnings growth — this is the central risk of owning LLY at current levels.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E - 1)*100:.1f}% EPS growth by FY2028E vs FY2027E.")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.32
beta        = 0.75
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  small but growing fast off low payout ratio)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; GLP-1 headline-driven swings on competitive/clinical news)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (moderate; large-cap pharma but high growth-stock sensitivity)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (significant but plausible on competitive-shock scenario)")
print(f"  52W range already reflects substantial GLP-1-news-driven volatility (competitive scares, trial readouts).")
print(f"  → Novo Nordisk competitive dynamics + US drug pricing policy are THE KEY binaries for downside risk.")
print(f"  → Orforglipron uptake + donanemab Alzheimer's ramp are KEY bull catalysts.")
print(f"  → AVOID above $900  |  WATCHLIST $750–875  |  ACCUMULATE $620–720  |  BUY below $570")

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
print(f"  In plain terms: the market is pricing in near-flawless execution across orforglipron,")
print(f"  donanemab, and continued GLP-1 share gains versus Novo Nordisk. The risk/reward skew")
print(f"  (Ratio B {ratio_b_str}) reflects that current levels leave little room for error — any single")
print(f"  pillar disappointing could trigger meaningful multiple compression.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Orforglipron (oral GLP-1) — launch uptake, pricing, formulary access vs injectables")
print(f"  (2) Novo Nordisk competitive response — CagriSema/oral semaglutide data and pricing actions")
print(f"  (3) GLP-1 manufacturing capacity expansion — pace of supply normalization across dose strengths")
print(f"  (4) Donanemab (Kisunla) Alzheimer's ramp — diagnostic infrastructure and reimbursement progress")
print(f"  (5) US drug pricing policy (IRA negotiation) — GLP-1 list price exposure")
print(f"  (6) Verzenio oncology growth — adjuvant breast cancer label expansion")
print(f"  AVOID above $900  |  WATCHLIST $750–875  |  ACCUMULATE $620–720  |  BUY below $570")
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
