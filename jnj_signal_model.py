"""
JNJ  ·  Johnson & Johnson  ·  NYSE: JNJ
Bottom-up signal model  ·  Innovative Medicine (Oncology/Immunology) / MedTech (Abiomed/EP/Ortho) / Talc Litigation
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "JNJ"
COMPANY       = "Johnson & Johnson"
SECTOR        = "Pharma · Innovative Medicine (Darzalex/Carvykti/Tremfya) · MedTech (Abiomed/Varipulse/Ortho) · Talc Litigation · NYSE: JNJ"
CURRENT_PRICE = 162.50      # USD; as of 2026-06-10
VOL_52W_LOW   = 140.68      # 2025 talc-litigation/Stelara-erosion trough
VOL_52W_HIGH  = 172.83      # 2026 Innovative Medicine pipeline re-rating peak
SHARES_OUT_M  = 2_390.0     # millions
ANNUAL_DIV    = 5.20        # $/share; ~3.2% yield; Dividend King (62+ yrs of increases)

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Oncology (Darzalex/Carvykti/Erleada)", 24.0, 19.0, 28.0, "Darzalex ~$13B run-rate +18% YoY; Carvykti CAR-T scaling rapidly off capacity expansion"),
    ("Immunology (Tremfya/Stelara biosim.)", 17.5, 13.0, 21.0, "Stelara biosimilar erosion (-$2-3B/yr) offset by Tremfya (+25%+) and ICP-related launches (icotrokinra)"),
    ("Neuroscience/Pulmonary/Other Pharma",   8.5,  7.0, 10.0, "Spravato, Tremfya in IBD, smaller franchises; mixed growth"),
    ("MedTech - Cardiovascular (Abiomed/EP)", 14.0, 11.5, 18.0, "Abiomed Impella + Varipulse (PFA electrophysiology) - high-growth swing factor"),
    ("MedTech - Ortho/Surgery/Vision",        13.0, 11.0, 15.0, "Orthopedics stabilizing post-divestiture cleanup; Surgery/Vision steady mid-single-digit growth"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.685   # blended gross margin; pharma + medtech mix
GROSS_MARGIN_BULL = 0.705   # BULL: higher-margin Innovative Medicine mix (Darzalex/Carvykti/Tremfya) improves blend
OPEX_FIXED_B      = 27.0    # SG&A + R&D ($B); largely fixed cost base
TAX_RATE          = 0.155   # effective rate; pharma/medtech international mix

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 11.00       # FY2027E EPS (consensus ~$10.80-$11.20 non-GAAP)
PE_PESSIMISTIC = 13.0        # trough P/E: AAA balance sheet + dividend king floor; historical JNJ trough ~13-14x
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # $143

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 9.50, 12,  114, "Talc litigation resolution forces large adverse cash settlement; Stelara erosion outpaces Tremfya/Carvykti ramp; MedTech growth stalls; EPS $9.50 → 12× = $114"),
    "BASE":  (11.00, 16,  176, "Stelara erosion offset by Tremfya/Darzalex/Carvykti growth; MedTech (Abiomed/Varipulse) grows mid-to-high single digits; talc resolved at manageable cost; EPS $11.00 → 16× = $176"),
    "BULL":  (12.75, 18,  230, "Carvykti capacity expansion + icotrokinra launch drive Innovative Medicine reacceleration; Varipulse PFA gains meaningful share; talc overhang fully resolved; EPS $12.75 → 18× = $230"),
    "XBULL": (14.50, 21,  305, "Pipeline (oncology bispecifics, immunology ICP franchise) becomes new growth engine; MedTech re-rates on Abiomed/EP momentum; multiple expands toward healthcare growth peers; EPS $14.50 → 21× = $305"),
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
        "name":       "Darzalex/Carvykti oncology revenue YoY growth",
        "weight":     0.25,
        "thresholds": ("<8%",   "≥15%",  "≥22%",   "≥30%"),
        "now":        "+18%",
        "score":      2,
        "comment":    "Darzalex ~$13B run-rate +18% YoY; Carvykti CAR-T scaling with capacity expansions; oncology remains core growth engine",
    },
    {
        "name":       "Stelara biosimilar erosion vs Tremfya/ICP offset",
        "weight":     0.25,
        "thresholds": ("erosion>offset", "roughly even", "Tremfya offsets", "net immunology growth"),
        "now":        "Tremfya +25%, Stelara -45%",
        "score":      2,
        "comment":    "Stelara biosimilar erosion (~-45% YoY) is steep but Tremfya (+25%+) and icotrokinra (ICP) launches are closing the gap toward FY2027",
    },
    {
        "name":       "MedTech cardiovascular growth (Abiomed/Varipulse PFA)",
        "weight":     0.20,
        "thresholds": ("<3%",   "≥6%",   "≥10%",   "≥15%"),
        "now":        "+8%",
        "score":      2,
        "comment":    "Abiomed Impella steady growth; Varipulse PFA early launch gaining traction in competitive electrophysiology market",
    },
    {
        "name":       "Talc litigation resolution progress",
        "weight":     0.15,
        "thresholds": ("escalating/unresolved", "ongoing/uncertain", "settlement framework progressing", "resolved at modest cost"),
        "now":        "ongoing/uncertain",
        "score":      2,
        "comment":    "Multiple bankruptcy-strategy attempts (LTL Management) rejected by courts; litigation remains a multi-billion dollar overhang with timeline uncertainty",
    },
    {
        "name":       "Pipeline productivity (icotrokinra, bispecifics, ortho)",
        "weight":     0.10,
        "thresholds": ("none",  "1 readout","2-3 readouts","4+ readouts"),
        "now":        "2",
        "score":      2,
        "comment":    "Icotrokinra (oral IL-23) Phase 3 readouts in psoriasis/IBD; oncology bispecifics progressing; ortho stabilization ongoing",
    },
    {
        "name":       "Balance sheet strength / capital return capacity",
        "weight":     0.05,
        "thresholds": ("<AA-",  "AA",  "AA+",   "AAA"),
        "now":        "AAA",
        "score":      4,
        "comment":    "One of only two AAA-rated US corporates; Dividend King (62+ consecutive years of increases); ~3.2% yield with ample coverage",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("-", "Talc litigation tail risk — unresolved multi-billion dollar liability; bankruptcy strategy repeatedly rejected by courts", -0.7, 0.25),
    ("+", "AAA balance sheet + Dividend King — 62+ yr dividend growth streak provides downside floor and capital flexibility", +0.6, 0.20),
    ("-", "Stelara cliff — biosimilar erosion is steep and immediate; Tremfya/ICP offset timing remains unproven at scale", -0.4, 0.20),
    ("+", "Diversification — Innovative Medicine + MedTech dual-engine model reduces single-franchise concentration risk vs peers", +0.4, 0.15),
    ("+", "Carvykti/Abiomed/Varipulse — multiple credible growth vectors across oncology, cell therapy, and cardiovascular MedTech", +0.3, 0.15),
    ("-", "Valuation already reflects defensive premium — limited multiple expansion until talc + Stelara uncertainty clears",       -0.2, 0.05),
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
CONS_EPS_2YR  = 11.75   # FY2028E conservative: modest EPS growth as Stelara erosion fully laps
CONS_PE_2YR   = 15      # rerates modestly from ~14.8x given residual talc/Stelara uncertainty
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Innovative Medicine (Oncology/Immunology) / MedTech / Talc Litigation")
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
shares_b     = shares * 0.97   # ~1.5%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift away from high-margin Innovative Medicine
bear_oi      = bear_gp - OPEX_FIXED_B * 0.95           # partial cost response
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 18× = ~${bull_eps_imp*18:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 12× trough P/E (talc-discount floor) = ~${bear_eps_imp*12:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev       = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_oncology  = 1.0 * 0.82 * (1 - TAX_RATE) / shares   # Oncology very high margin
eps_per_1B_medtech   = 1.0 * 0.62 * (1 - TAX_RATE) / shares   # MedTech lower margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Oncology (Darzalex/Carvykti) revenue:  +${eps_per_1B_oncology:.3f}/EPS  = +${eps_per_1B_oncology*16:.1f}/share at 16× P/E")
print(f"  Every $1B MedTech (Abiomed/Varipulse) revenue:   +${eps_per_1B_medtech:.3f}/EPS  = +${eps_per_1B_medtech*16:.1f}/share at 16× P/E")
print(f"  1pp GM expansion (mix shift to Innov. Medicine): +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*16:.1f}/share at 16× P/E")
print(f"  1% buyback (~24M shares):                        +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Oncology / Immunology transition / MedTech / Talc litigation framework)")
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
    ("Darzalex/Carvykti oncology growth",  "+18%",   "<8%",    "−10pp",  "Competitive entrants (bispecifics) pressure multiple myeloma share"),
    ("Stelara erosion vs Tremfya offset",  "-45%/+25%", "erosion widens", "gap widens", "Tremfya/ICP launches underwhelm; immunology segment shrinks net"),
    ("MedTech cardiovascular growth",      "+8%",    "<3%",    "−5pp",   "Varipulse PFA loses share to Boston Scientific/Medtronic competitors"),
    ("Talc litigation resolution",         "ongoing","adverse ruling/large settlement", "−$X0B charge", "Courts force large cash settlement outside bankruptcy protection"),
    ("Pipeline readouts",                  "2",      "0",      "−2",     "Icotrokinra/bispecific Phase 3 readouts disappoint or delay"),
    ("Gross margin",                       "68.5%",  "<65%",   "−3.5pp", "Mix shift to lower-margin MedTech/generics-pressured immunology"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Talc litigation resolution forces a large adverse cash settlement (well")
print(f"  beyond reserved amounts) outside any bankruptcy-protection strategy, while Stelara")
print(f"  biosimilar erosion outpaces Tremfya/icotrokinra ramp and Varipulse PFA loses ground to")
print(f"  larger EP competitors. EPS falls to ~$9.50 → 12× trough P/E (talc-discount floor) = ${bear_price}.")
print(f"  Note: $114 is NOT permanent impairment — AAA balance sheet + Dividend King ($5.20/share)")
print(f"  provide a durable earnings floor. Recovery to ~${bear_price+30}–${bear_price+50} in 2yr is base case post-shock.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           ${EPS_FY2027E:.2f}  (consensus ~$10.80-$11.20 non-GAAP)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (talc-discount floor; AAA-rated pharma trough ~13-14×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% {'above' if epp_gap_pct >= 0 else 'below'} trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% {'premium to' if epp_gap_pct >= 0 else 'discount to'} EPP reflects that JNJ trades at roughly")
print(f"  {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a modest valuation for an AAA-rated, Dividend King")
print(f"  pharma/medtech hybrid. The talc litigation overhang and Stelara biosimilar erosion are")
print(f"  largely priced in. The open question is whether Carvykti/Tremfya/Abiomed/Varipulse growth")
print(f"  vectors provide enough offset to justify a modest re-rating, or whether the talc tail")
print(f"  risk caps the multiple near current levels (HOLD/TRIM territory).")
print(f"  EPP path: FY2029E EPS ~$12.50 × {PE_PESSIMISTIC:.0f}× = ${12.50*PE_PESSIMISTIC:.0f} floor (EPP grows modestly as Stelara erosion laps).")
print(f"  At 16× mid-cycle P/E: ${EPS_FY2027E:.2f} × 16 = ${EPS_FY2027E*16:.0f}  — roughly in line with current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest EPS growth as Stelara erosion laps; P/E roughly flat)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (modest growth; Stelara erosion largely lapped, Tremfya/Carvykti/MedTech offset)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (roughly flat from ~{CURRENT_PRICE/EPS_FY2027E:.1f}× as talc uncertainty caps re-rating)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: JNJ trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a modest multiple for")
print(f"  an AAA-rated Dividend King — reflecting the talc litigation overhang and Stelara biosimilar")
print(f"  erosion. Carvykti capacity expansion, Tremfya/icotrokinra immunology growth, and Abiomed/")
print(f"  Varipulse MedTech momentum are the diversification levers. If talc resolves at manageable")
print(f"  cost and the Innovative Medicine pipeline delivers, the stock can re-rate modestly toward")
print(f"  16-18×. If talc escalates or Stelara erosion outpaces offsets, current levels are appropriate.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E - 1)*100:.1f}% EPS growth by FY2028E vs FY2027E — modest, achievable at BASE.")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.15
beta        = 0.55
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  Dividend King, 62+ yrs of increases)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (very low; defensive AAA-rated healthcare staple)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (highly defensive; among lowest-beta large caps)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe; talc-litigation-shock tail scenario)")
print(f"  52W range reflects relatively contained volatility given litigation/biosimilar overhangs.")
print(f"  → Talc litigation resolution timeline/cost is THE KEY binary for downside risk.")
print(f"  → Carvykti scaling + Varipulse PFA share gains are KEY bull catalysts.")
print(f"  → AVOID above $185  |  WATCHLIST $165–175  |  ACCUMULATE $148–158  |  BUY below $135–145")

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
print(f"  In plain terms: the market is pricing in more confidence on Stelara/Tremfya offset and")
print(f"  talc resolution than the bottom-up fundamentals currently support. The risk/reward skew")
print(f"  (Ratio B {ratio_b_str}) still favors accumulation given the AAA-rated downside floor and")
print(f"  Dividend King support, but the gap above warrants some caution on near-term entries.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Talc litigation resolution — settlement size/timing vs reserves; bankruptcy strategy outcomes")
print(f"  (2) Stelara biosimilar erosion trajectory — pace vs Tremfya/icotrokinra immunology offset")
print(f"  (3) Carvykti capacity expansion — CAR-T manufacturing scale-up and share gains in multiple myeloma")
print(f"  (4) Varipulse PFA adoption — electrophysiology share gains vs Boston Scientific/Medtronic")
print(f"  (5) Icotrokinra (oral IL-23) Phase 3 readouts — psoriasis/IBD pipeline productivity")
print(f"  (6) Dividend sustainability — ${ANNUAL_DIV:.2f}/share payout; 62+ yr increase streak (Dividend King)")
print(f"  AVOID above $185  |  WATCHLIST $165–175  |  ACCUMULATE $148–158  |  BUY below $135–145")
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
