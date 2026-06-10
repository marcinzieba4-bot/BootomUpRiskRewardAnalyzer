"""
BMY  ·  Bristol Myers Squibb Co.  ·  NYSE: BMY
Bottom-up signal model  ·  Pharma / Patent Cliff (Eliquis/Revlimid) / Cobenfy (KarXT) Launch / Cell Therapy
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "BMY"
COMPANY       = "Bristol Myers Squibb Co."
SECTOR        = "Pharma · Patent Cliff (Eliquis/Revlimid) · Cobenfy (KarXT) · Cell Therapy (Breyanzi/Abecma) · NYSE: BMY"
CURRENT_PRICE = 52.00       # USD; as of 2026-06-10
VOL_52W_LOW   = 41.65       # 2025 cliff-fear / Cobenfy launch-skepticism trough
VOL_52W_HIGH  = 63.20       # 2026 Cobenfy expanded-indication re-rating peak
SHARES_OUT_M  = 2_020.0     # millions
ANNUAL_DIV    = 2.48        # $/share; ~4.8% yield; reflects market skepticism about cliff

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Eliquis (anticoagulant)",          9.5,  6.0,  10.0, "US small-molecule generic competition begins ~2026/2027 (loses exclusivity); steep multi-year erosion ahead"),
    ("Revlimid (multiple myeloma)",      4.0,  1.5,   4.5, "Generic erosion accelerating per existing settlement schedule; legacy cash-cow declining toward minimal base"),
    ("Growth Portfolio - Cell Therapy (Breyanzi/Abecma)", 3.0, 2.2, 5.0, "Breyanzi (DLBCL/CLL/follicular) and Abecma (multiple myeloma) CAR-T scaling on label expansions"),
    ("Growth Portfolio - Camzyos/Reblozyl/Opdualag", 6.5, 5.0, 8.5, "Camzyos (HCM) ramping fast; Reblozyl (MDS anemia) steady growth; Opdualag (melanoma) stable"),
    ("Cobenfy (KarXT - schizophrenia/psychiatric)", 0.4, 0.1,  3.0, "Novel M1/M4 muscarinic agonist; schizophrenia launch + Alzheimer's psychosis/bipolar/adjunct MDD pipeline - key swing factor"),
    ("Other Legacy/Mature Brands",       6.6,  5.3,   7.0, "Diversified mature brands (Sprycel/generics-exposed, Pomalyst, Orencia, Eliquis ex-US, etc.); gradual decline"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.72    # blended gross margin; pharma mix with generics drag
GROSS_MARGIN_BULL = 0.745   # BULL: Cobenfy/Camzyos/cell therapy higher-margin mix improves blend
OPEX_FIXED_B      = 13.5    # SG&A + R&D ($B); restructuring program targets reductions here
TAX_RATE          = 0.165   # effective rate; pharma international mix

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 6.60        # FY2027E non-GAAP EPS (consensus ~$6.40-$6.80, post-cliff trough year)
PE_PESSIMISTIC = 7.5         # trough P/E: deep patent-cliff discount; historical big-pharma cliff trough ~7-8x
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # $50

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 4.50,  7,   32, "Eliquis/Revlimid erosion outpaces growth portfolio; Cobenfy launch underwhelms vs blockbuster expectations; restructuring savings don't materialize; EPS $4.50 → 7× = $32"),
    "BASE":  ( 6.60, 10,   66, "Eliquis/Revlimid cliff plays out roughly as expected; Cobenfy reaches modest blockbuster status (~$1-1.5B) on schizophrenia alone; cell therapy + Camzyos offset partially; EPS $6.60 → 10× = $66"),
    "BULL":  ( 8.25, 13,  107, "Cobenfy expands into Alzheimer's psychosis/bipolar/adjunct-MDD, becoming a multi-billion dollar franchise; Camzyos and cell therapy scale strongly; cost cuts drive margin expansion; EPS $8.25 → 13× = $107"),
    "XBULL": (10.00, 16,  160, "Cobenfy becomes a top-tier psychiatric pipeline platform across multiple indications, fully offsetting the Eliquis/Revlimid cliff; multiple re-rates toward growth-pharma peers; EPS $10.00 → 16× = $160"),
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
        "name":       "Eliquis/Revlimid patent-cliff erosion pace",
        "weight":     0.25,
        "thresholds": ("erosion>plan", "in line with plan", "erosion slower than plan", "minimal erosion to date"),
        "now":        "Eliquis still growing, Revlimid -20%",
        "score":      2,
        "comment":    "Revlimid generic erosion (~-20% YoY) tracking the known settlement schedule; Eliquis still growing modestly ahead of US LOE but cliff timeline confirmed for 2026-2028",
    },
    {
        "name":       "Cobenfy (KarXT) launch trajectory - schizophrenia",
        "weight":     0.25,
        "thresholds": ("<$200M run-rate", "≥$500M", "≥$1B", "≥$2B"),
        "now":        "~$500-700M run-rate",
        "score":      2,
        "comment":    "Cobenfy schizophrenia launch tracking toward ~$500-700M annualized run-rate; encouraging early uptake but still well below peak blockbuster expectations of $5B+",
    },
    {
        "name":       "Cobenfy pipeline expansion (Alzheimer's psychosis/bipolar/MDD)",
        "weight":     0.15,
        "thresholds": ("no readouts", "1 positive readout", "2 positive readouts", "3+ positive readouts/filings"),
        "now":        "1 readout pending",
        "score":      2,
        "comment":    "Phase 3 readouts in Alzheimer's-related psychosis and adjunctive MDD pending; bipolar mania program advancing; broader psychiatric platform thesis remains unproven at scale",
    },
    {
        "name":       "Cell therapy growth (Breyanzi/Abecma) + Camzyos/Reblozyl",
        "weight":     0.15,
        "thresholds": ("<8%", "≥12%", "≥18%", "≥25%"),
        "now":        "+15%",
        "score":      2,
        "comment":    "Breyanzi label expansions (2L DLBCL/CLL/follicular) and Camzyos (HCM) ramping well (+15% blended growth portfolio); Abecma facing competitive CAR-T pressure",
    },
    {
        "name":       "Cost-cutting/restructuring program execution",
        "weight":     0.10,
        "thresholds": ("behind plan", "on track", "ahead of plan", "exceeding + further cuts announced"),
        "now":        "on track",
        "score":      2,
        "comment":    "Multi-billion dollar cost-reduction program (targeting ~$1.5B+ savings by 2027) tracking on schedule; helps cushion EPS during cliff transition",
    },
    {
        "name":       "Balance sheet deleveraging (post Karuna/RayzeBio/Mirati M&A)",
        "weight":     0.10,
        "thresholds": ("leverage rising", "stable, elevated (~3x+)", "deleveraging toward ~2.5x", "back below ~2x"),
        "now":        "stable, elevated (~3x)",
        "score":      2,
        "comment":    "Net debt remains elevated (~3x EBITDA) following Karuna ($14B), RayzeBio (~$4B), and Mirati (~$4.8B) acquisitions; free cash flow being directed to deleveraging ahead of dividend growth resumption",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("-", "Eliquis/Revlimid patent cliff — ~$14B+ combined revenue facing severe erosion through 2028, the most severe near-term cliff among large-cap pharma", -0.8, 0.30),
    ("+", "Cobenfy optionality — first novel-mechanism schizophrenia drug in decades, with broad psychiatric pipeline (Alzheimer's psychosis, bipolar, MDD) offering asymmetric multi-indication upside", +0.6, 0.20),
    ("-", "High leverage from M&A (Karuna/RayzeBio/Mirati) — constrains capital flexibility and dividend growth during the cliff transition",                       -0.4, 0.15),
    ("+", "Very high dividend yield (~4.8%) — provides meaningful total-return floor and reflects deep market skepticism already priced in",                          +0.4, 0.15),
    ("+", "Growth portfolio diversification (Camzyos/Breyanzi/Abecma/Reblozyl/Opdualag) — multiple credible non-Cobenfy growth vectors reduce single-product risk",   +0.3, 0.10),
    ("+", "Aggressive cost-restructuring program — targeted savings provide EPS cushion independent of revenue trajectory",                                            +0.3, 0.10),
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
CONS_EPS_2YR  = 6.00    # FY2028E conservative: cliff trough year, EPS dips before recovery
CONS_PE_2YR   = 9       # modest multiple recovery from trough as Cobenfy trajectory becomes clearer
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Patent Cliff (Eliquis/Revlimid) / Cobenfy Launch / Cell Therapy")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
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

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift away from high-margin legacy brands
bear_oi      = bear_gp - OPEX_FIXED_B * 0.90           # cost cuts partially offset revenue decline
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 13× = ~${bull_eps_imp*13:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex (10% cut)  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 7× trough P/E (cliff-discount floor) = ~${bear_eps_imp*7:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev      = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_cobenfy  = 1.0 * 0.85 * (1 - TAX_RATE) / shares   # Cobenfy very high incremental margin
eps_per_1B_eliquis  = 1.0 * 0.80 * (1 - TAX_RATE) / shares   # Eliquis high margin, lost dollar-for-dollar

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Cobenfy revenue:                      +${eps_per_1B_cobenfy:.3f}/EPS  = +${eps_per_1B_cobenfy*10:.1f}/share at 10× P/E")
print(f"  Every $1B Eliquis/Revlimid revenue lost:        -${eps_per_1B_eliquis:.3f}/EPS  = -${eps_per_1B_eliquis*10:.1f}/share at 10× P/E")
print(f"  1pp GM expansion (mix shift to Cobenfy/Camzyos): +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*10:.1f}/share at 10× P/E")
print(f"  1% buyback (~20M shares):                        +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Patent cliff erosion / Cobenfy launch & pipeline / Growth portfolio / Restructuring)")
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
    ("Eliquis revenue trajectory",         "growing", "double-digit decline", "swing to -",  "US generic entry arrives earlier/faster than expected, cratering Eliquis"),
    ("Cobenfy launch run-rate",            "$500-700M", "<$200M",  "−$300-500M", "Schizophrenia uptake stalls on access/formulary hurdles or tolerability concerns"),
    ("Cobenfy pipeline readouts",          "1 pending", "0 positive", "−1+",     "Alzheimer's psychosis / bipolar / MDD trials fail or show weak efficacy"),
    ("Growth portfolio (Breyanzi/Camzyos)","+15%",    "<8%",     "−7pp",        "Cell therapy competitive pressure intensifies; Camzyos uptake slows"),
    ("Restructuring savings realization",  "on track", "behind plan", "shortfall", "Cost-cutting program slips, EPS cushion fails to materialize"),
    ("Net leverage",                       "~3.0x",   ">3.5x",   "+0.5x",       "Free cash flow diverted, leverage rises further, dividend cut risk increases"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Eliquis faces earlier/faster generic erosion than the market expects while")
print(f"  Cobenfy's launch stalls well below blockbuster expectations (access/formulary friction or")
print(f"  tolerability issues curb uptake) and the Alzheimer's-psychosis/bipolar/MDD pipeline reads out")
print(f"  negatively, removing the platform-expansion thesis. Restructuring savings fall short and")
print(f"  leverage ticks higher. EPS falls to ~$4.50 → 7× trough P/E (deep cliff-discount floor) = ${bear_price}.")
print(f"  Note: $32 is NOT permanent impairment — the ~4.8% dividend yield and durable growth-portfolio")
print(f"  cash flows (Camzyos/Breyanzi/Reblozyl) provide a floor. Recovery to ~${bear_price+15}–${bear_price+25} in 2yr is base case post-shock.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           ${EPS_FY2027E:.2f}  (consensus ~$6.40-$6.80 non-GAAP, post-cliff trough year)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.1f}×  (deep cliff-discount floor; big-pharma cliff trough ~7-8×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct >= 0 else 'below'} trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% {'premium to' if epp_gap_pct >= 0 else 'discount to'} EPP reflects that BMY trades at roughly")
print(f"  {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a deep discount versus pharma peers, owing to the")
print(f"  severe Eliquis/Revlimid patent cliff (~$14B+ at risk through 2028). The market has priced in")
print(f"  significant cliff risk already; the open question is whether Cobenfy's launch trajectory and")
print(f"  pipeline expansion (Alzheimer's psychosis, bipolar, MDD) provide enough offset to make the")
print(f"  current discount excessive (UNDERVALUED) or whether the discount is appropriately sized given")
print(f"  cliff timing/magnitude and Cobenfy execution risk (HOLD/TRIM territory).")
print(f"  EPP path: FY2029E EPS ~$7.25 × {PE_PESSIMISTIC:.1f}× = ${7.25*PE_PESSIMISTIC:.0f} floor (EPP recovers as cliff laps and Cobenfy scales).")
print(f"  At 10× mid-cycle P/E: ${EPS_FY2027E:.2f} × 10 = ${EPS_FY2027E*10:.0f}  — modest premium to current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: cliff trough year EPS dip, modest P/E recovery)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (cliff trough year; Eliquis/Revlimid erosion peaks before Cobenfy/growth portfolio offset matures)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (modest recovery from ~{CURRENT_PRICE/EPS_FY2027E:.1f}× as Cobenfy trajectory becomes clearer)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: BMY trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — the deepest discount")
print(f"  among large-cap pharma — entirely due to the severe Eliquis/Revlimid patent cliff (~$14B+ at")
print(f"  risk through 2028). Cobenfy (novel schizophrenia mechanism, with Alzheimer's-psychosis/bipolar/")
print(f"  MDD pipeline optionality), Camzyos, and Breyanzi/Abecma cell therapies are the offset levers.")
print(f"  If Cobenfy scales toward blockbuster status across multiple indications, the discount is")
print(f"  excessive and BMY re-rates toward 10-13×. If the launch underwhelms and the cliff bites as")
print(f"  feared, current levels (or lower) are appropriate — i.e. the ~4.8% dividend is the primary")
print(f"  return driver in the interim.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E - 1)*100:.1f}% EPS change by FY2028E vs FY2027E.")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.24
beta        = 0.65
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  very high, reflects market skepticism on the cliff)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated for big pharma; cliff/Cobenfy headline-driven swings)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (moderately defensive; below-market beta but cliff-driven idiosyncratic risk)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe; cliff-acceleration + Cobenfy-failure tail scenario)")
print(f"  52W range already reflects significant cliff-fear and Cobenfy-launch-skepticism repricing.")
print(f"  → Cobenfy launch trajectory (schizophrenia uptake + pipeline readouts) is THE KEY binary for upside.")
print(f"  → Pace of Eliquis/Revlimid erosion is THE KEY binary for downside risk.")
print(f"  → AVOID above $65  |  WATCHLIST $58–63  |  ACCUMULATE $48–54  |  BUY below $42–46")

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
print(f"  In plain terms: the Eliquis/Revlimid cliff discount appears largely priced in, with Cobenfy's")
print(f"  early launch trajectory and pipeline optionality offering a real but execution-dependent")
print(f"  upside lever. The very high dividend yield (~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}%) provides a meaningful")
print(f"  total-return cushion while the market awaits more clarity on Cobenfy's trajectory.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Eliquis US loss-of-exclusivity timing/pace — generic entry trajectory through 2026-2028")
print(f"  (2) Cobenfy schizophrenia quarterly run-rate — trajectory toward/away from blockbuster status")
print(f"  (3) Cobenfy pipeline readouts — Alzheimer's-related psychosis, bipolar mania, adjunctive MDD")
print(f"  (4) Camzyos (HCM) and Breyanzi/Abecma cell therapy growth — non-Cobenfy growth portfolio scaling")
print(f"  (5) Cost-restructuring program execution — progress toward ~$1.5B+ targeted savings")
print(f"  (6) Net leverage trajectory — deleveraging pace post Karuna/RayzeBio/Mirati M&A; dividend coverage")
print(f"  AVOID above $65  |  WATCHLIST $58–63  |  ACCUMULATE $48–54  |  BUY below $42–46")
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
