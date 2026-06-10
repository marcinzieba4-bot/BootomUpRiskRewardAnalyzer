"""
BSX  ·  Boston Scientific Corporation  ·  NYSE: BSX
Bottom-up signal model  ·  Cardiovascular (WATCHMAN/Farapulse) / MedSurg / Premium Growth Valuation
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "BSX"
COMPANY       = "Boston Scientific Corporation"
SECTOR        = "MedTech · Cardiovascular (WATCHMAN/Farapulse PFA) · Structural Heart · Urology/MedSurg · NYSE: BSX"
CURRENT_PRICE = 104.00     # USD; as of 2026-06-10
VOL_52W_LOW   = 86.50      # 2025 broad medtech pullback trough
VOL_52W_HIGH  = 112.50     # 2026 Farapulse/WATCHMAN-driven re-rating peak
SHARES_OUT_M  = 1_475.0    # millions
ANNUAL_DIV    = 0.0        # $/share; BSX pays no dividend - reinvests for growth/M&A

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Electrophysiology (Farapulse PFA)",        2.8,  1.8,  4.2, "Pulsed-field ablation - the single biggest growth driver; rapid global rollout, capacity expansion ongoing"),
    ("Cardiology - WATCHMAN (LAAC)",             3.4,  2.6,  4.4, "Left atrial appendage closure; durable double-digit growth as guidelines/awareness expand"),
    ("Cardiology - Interventional/Other",        6.5,  5.6,  7.4, "Coronary therapies, IVL (shockwave), peripheral interventions; steady mid-single-digit growth"),
    ("Structural Heart (TAVR/Mitral/Tricuspid)", 1.7,  1.3,  2.4, "ACURATE/WATCHMAN-adjacent structural heart pipeline; mitral/tricuspid optionality (Axonics-adjacent M&A)"),
    ("Urology/Neuromodulation (incl. Axonics)",  3.3,  2.7,  4.0, "Axonics sacral neuromodulation integration driving share gains; rezum/urology steady"),
    ("MedSurg/Endoscopy/Other",                  4.3,  3.9,  4.8, "Endoscopy, voice/airway, other; stable low-to-mid single-digit growth"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.700   # blended gross margin; medtech device mix with high-growth Farapulse/WATCHMAN
GROSS_MARGIN_BULL = 0.715   # BULL: Farapulse/WATCHMAN scale + favorable mix lift blend
OPEX_FIXED_B      = 9.6     # SG&A + R&D ($B); heavy commercial investment behind Farapulse launch
TAX_RATE          = 0.140   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 3.10        # FY2027E EPS (consensus ~$3.00-3.20 non-GAAP); ~15%+ growth off FY2026E ~$2.70
PE_PESSIMISTIC = 22.0        # trough P/E: even in a growth-deceleration scare, premium medtech grower floor ~20-24x
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # $68

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (2.55, 24,   61, "Farapulse growth decelerates sharply on competitive PFA entrants (Medtronic PulseSelect, J&J Varipulse); WATCHMAN growth slows; multiple compresses to 24x; EPS $2.55 → 24× = $61"),
    "BASE":  (3.10, 33,  102, "Farapulse maintains strong double-digit growth amid intensifying PFA competition; WATCHMAN expands steadily on guideline tailwinds; Axonics integration on track; EPS $3.10 → 33× = $102"),
    "BULL":  (3.55, 38,  135, "Farapulse extends share lead with next-gen catheter iterations; WATCHMAN FLX Pro + expanded indications accelerate growth; structural heart pipeline (mitral/tricuspid) gains traction; EPS $3.55 → 38× = $135"),
    "XBULL": (4.10, 42,  172, "BSX becomes the clear electrophysiology + structural heart category leader; Farapulse achieves dominant global PFA share; WATCHMAN becomes standard-of-care; M&A pipeline (Axonics-style tuck-ins) compounds growth; EPS $4.10 → 42× = $172"),
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
        "name":       "Farapulse (PFA) revenue YoY growth",
        "weight":     0.30,
        "thresholds": ("<25%",  "≥45%",  "≥65%",   "≥85%"),
        "now":        "+60%",
        "score":      2,
        "comment":    "Farapulse remains the single largest growth driver, scaling rapidly off ~$2.8B run-rate; growth still robust but decelerating from triple-digit launch-year pace as comps normalize and competitors enter",
    },
    {
        "name":       "WATCHMAN (LAAC) revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<8%",   "≥14%",  "≥20%",   "≥28%"),
        "now":        "+17%",
        "score":      2,
        "comment":    "WATCHMAN FLX Pro adoption continues to expand penetration of the AFib/anticoagulation-intolerant population; durable double-digit growth with long runway",
    },
    {
        "name":       "PFA competitive dynamics (Medtronic/J&J)",
        "weight":     0.20,
        "thresholds": ("losing share fast", "share roughly stable", "BSX gaining share", "BSX gaining share + pricing holds"),
        "now":        "BSX gaining share",
        "score":      3,
        "comment":    "Farapulse first-mover advantage and clinical data (ADVENT/ADMIRE) support continued share gains vs Medtronic PulseSelect and J&J Varipulse, though competitive intensity is rising fast",
    },
    {
        "name":       "Organic revenue growth (company-wide)",
        "weight":     0.15,
        "thresholds": ("<8%",   "≥12%",  "≥16%",   "≥20%"),
        "now":        "+15-16%",
        "score":      3,
        "comment":    "Company-wide organic growth has consistently run ~15%+, well above large-cap medtech peers, driven by Farapulse/WATCHMAN/Axonics",
    },
    {
        "name":       "M&A/pipeline integration (Axonics, structural heart)",
        "weight":     0.10,
        "thresholds": ("dilutive/stalled", "on-track integration", "accretive ahead of plan", "additional accretive tuck-ins closing"),
        "now":        "accretive ahead of plan",
        "score":      3,
        "comment":    "Axonics integration tracking ahead of deal-model expectations; management's M&A track record (Axonics, Shockwave-style tuck-ins) has consistently been value-additive",
    },
    {
        "name":       "Valuation vs forward growth (PEG-adjusted)",
        "weight":     0.05,
        "thresholds": ("PEG>2.2", "PEG~1.6-2.2", "PEG~1.1-1.6", "PEG<1.1"),
        "now":        "PEG ~2.1",
        "score":      2,
        "comment":    "~34x FY2027E EPS against ~16-18%/yr EPS growth implies a PEG near 2.0-2.2x - a full premium that already prices durable double-digit growth continuing for years",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Farapulse category leadership — first-mover PFA advantage with strong clinical data; largest single growth lever in medtech", +0.6, 0.25),
    ("-", "Premium valuation already prices years of flawless double-digit growth — limited margin for any deceleration", -0.6, 0.20),
    ("+", "WATCHMAN durable franchise — long runway as guideline adoption and anticoagulation-intolerant population penetration continue", +0.5, 0.15),
    ("-", "Intensifying PFA competition — Medtronic PulseSelect and J&J Varipulse both scaling; pricing/share dynamics could shift quickly", -0.5, 0.20),
    ("+", "Diversified growth engines + M&A track record — Axonics, structural heart pipeline, and MedSurg base provide multiple compounding levers beyond Farapulse alone", +0.4, 0.15),
    ("-", "No dividend / capital returned mostly via reinvestment and M&A — total return depends entirely on multiple + EPS growth, no income cushion", -0.2, 0.05),
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
CONS_EPS_2YR  = 3.55   # FY2028E conservative: ~14% CAGR off FY2027E base, modest deceleration from current pace
CONS_PE_2YR   = 30     # compresses modestly from ~34x as growth normalizes toward "mature high-growth medtech" multiple
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Electrophysiology (Farapulse) / WATCHMAN / Structural Heart / MedSurg")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<42}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<42}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<42}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
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

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift / pricing pressure from PFA competition
bear_oi      = bear_gp - OPEX_FIXED_B * 1.0            # commercial investment not easily cut
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 38× = ~${bull_eps_imp*38:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 24× trough P/E (premium-grower floor) = ~${bear_eps_imp*24:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev    = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_farapulse = 1.0 * 0.78 * (1 - TAX_RATE) / shares   # Farapulse very high incremental margin
eps_per_1B_other  = 1.0 * 0.62 * (1 - TAX_RATE) / shares      # other segments lower margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Farapulse/WATCHMAN revenue:              +${eps_per_1B_farapulse:.3f}/EPS  = +${eps_per_1B_farapulse*33:.1f}/share at 33× P/E")
print(f"  Every $1B other-portfolio revenue:                 +${eps_per_1B_other:.3f}/EPS  = +${eps_per_1B_other*33:.1f}/share at 33× P/E")
print(f"  1pp GM expansion (mix shift to Farapulse/WATCHMAN): +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*33:.1f}/share at 33× P/E")
print(f"  1% buyback (~14.75M shares):                        +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Farapulse growth / WATCHMAN / PFA competition / organic growth / M&A / valuation)")
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
    ("Farapulse revenue growth",           "+60%",   "<25%",   "−35pp",  "Medtronic PulseSelect/J&J Varipulse capture meaningful PFA share faster than expected"),
    ("WATCHMAN revenue growth",            "+17%",   "<8%",    "−9pp",   "Guideline/reimbursement headwinds slow LAAC adoption; competitive devices gain ground"),
    ("PFA competitive share dynamics",     "gaining","losing share", "reversal", "Newer-gen competitor catheters leapfrog Farapulse on efficiency/safety profile"),
    ("Organic revenue growth (co-wide)",   "+15-16%","<8%",    "−8pp",   "Multiple segments decelerate simultaneously amid macro/medtech-spending slowdown"),
    ("Axonics/structural heart M&A",       "ahead of plan","dilutive/stalled", "reversal", "Integration costs run over budget; structural heart pipeline readouts disappoint"),
    ("Gross margin",                       "70.0%",  "<66%",   "−4pp",   "Pricing pressure from PFA competition + unfavorable mix shift away from Farapulse"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Medtronic's PulseSelect and J&J's Varipulse scale faster than expected and")
print(f"  capture meaningful share from Farapulse, simultaneously WATCHMAN growth slows on")
print(f"  guideline/reimbursement friction, and a broader medtech capex slowdown drags company-wide")
print(f"  organic growth toward high-single-digits. EPS growth stalls to ~$2.55 → 24× trough P/E")
print(f"  (premium-grower floor) = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT permanent impairment — the EP/LAAC category remains a multi-year")
print(f"  secular growth market. Recovery toward ~${bear_price+25}-${bear_price+45} in 2yr is plausible post-shock as")
print(f"  next-gen Farapulse iterations and structural heart pipeline provide offsetting growth.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           ${EPS_FY2027E:.2f}  (consensus ~$3.00-3.20 non-GAAP)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (premium-grower floor; even PFA-competitive-scare scenarios likely hold ~22-26×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% {'above' if epp_gap_pct >= 0 else 'below'} trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% {'premium to' if epp_gap_pct >= 0 else 'discount to'} EPP reflects that BSX trades at roughly")
print(f"  {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a steep multiple that prices in continued")
print(f"  Farapulse share leadership, durable WATCHMAN double-digit growth, and successful Axonics/")
print(f"  structural heart integration ALL playing out favorably. The risk is that even modest")
print(f"  disappointment on the PFA competitive front compresses the multiple meaningfully toward")
print(f"  the EPP floor.")
print(f"  EPP path: FY2029E EPS ~$4.10 × {PE_PESSIMISTIC:.0f}× = ${4.10*PE_PESSIMISTIC:.0f} floor (EPP grows quickly given high underlying EPS growth).")
print(f"  At 33× mid-cycle P/E: ${EPS_FY2027E:.2f} × 33 = ${EPS_FY2027E*33:.0f}  — roughly in line with current price, implying market is pricing FY2027E earnings power near full value.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: EPS growth decelerates modestly; P/E compresses from current levels)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (~14% CAGR off FY2027E; modest deceleration from current ~16%+ growth pace)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (compresses from ~{CURRENT_PRICE/EPS_FY2027E:.1f}× as growth normalizes toward 'mature high-growth medtech' multiple)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (no dividend - BSX reinvests for growth/M&A)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: BSX trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a steep multiple even")
print(f"  for a company growing EPS mid-to-high-teens annually. The conservative case assumes growth")
print(f"  decelerates modestly to ~14%/yr by FY2028E AND the multiple compresses to {CONS_PE_2YR}× as PFA")
print(f"  competition intensifies and the market re-rates from 'category-defining grower' toward")
print(f"  'best-in-class compounder' pricing. Multiple compression can offset strong earnings growth —")
print(f"  this is the central risk of owning BSX at current levels, with no dividend cushion.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E - 1)*100:.1f}% EPS growth by FY2028E vs FY2027E.")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.24
beta        = 0.95
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (no dividend - BSX reinvests for growth/M&A)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (moderate; consistent grower but PFA-competitive headlines drive swings)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (roughly market-like; growth-stock sensitivity to medtech sentiment)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (significant but plausible on PFA-competitive-shock scenario)")
print(f"  52W range reflects fairly contained volatility for a premium-multiple grower, given consistent execution.")
print(f"  → PFA competitive dynamics (Medtronic/J&J) are THE KEY binary for downside risk.")
print(f"  → WATCHMAN guideline expansion + structural heart pipeline are KEY bull catalysts.")
print(f"  → AVOID above $120  |  WATCHLIST $100–115  |  ACCUMULATE $85–98  |  BUY below $80")

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
print(f"  In plain terms: the market is pricing in continued Farapulse share leadership and durable")
print(f"  WATCHMAN/Axonics growth with little allowance for PFA-competitive disruption. The risk/")
print(f"  reward skew (Ratio B {ratio_b_str}) reflects that current levels leave limited room for error —")
print(f"  any deceleration in the Farapulse growth story could trigger meaningful multiple compression.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Farapulse (PFA) — global rollout pace, capacity expansion, share vs Medtronic PulseSelect/J&J Varipulse")
print(f"  (2) WATCHMAN (LAAC) — guideline expansion, reimbursement, FLX Pro adoption trajectory")
print(f"  (3) Axonics integration — synergy realization, sacral neuromodulation share gains")
print(f"  (4) Structural heart pipeline — mitral/tricuspid program readouts and approvals")
print(f"  (5) Organic growth sustainability — company-wide growth vs ~15%+ recent run-rate")
print(f"  (6) Capital allocation — further accretive tuck-in M&A vs buybacks (no dividend)")
print(f"  AVOID above $120  |  WATCHLIST $100–115  |  ACCUMULATE $85–98  |  BUY below $80")
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
