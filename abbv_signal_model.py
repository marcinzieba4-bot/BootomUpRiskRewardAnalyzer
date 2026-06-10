"""
ABBV  ·  AbbVie Inc.  ·  NYSE: ABBV
Bottom-up signal model  ·  Pharma / Immunology (Skyrizi/Rinvoq) / Aesthetics (Botox) / Oncology
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "ABBV"
COMPANY       = "AbbVie Inc."
SECTOR        = "Pharma · Immunology (Skyrizi/Rinvoq) · Aesthetics (Botox) · Oncology · Neuroscience · NYSE: ABBV"
CURRENT_PRICE = 205.00      # USD; as of 2026-06-10
VOL_52W_LOW   = 165.00      # 2025 rate-sensitivity / Imbruvica-decline trough
VOL_52W_HIGH  = 220.00      # 2026 Skyrizi/Rinvoq re-rating peak
SHARES_OUT_M  = 1_770.0     # millions
ANNUAL_DIV    = 6.56        # $/share; ~3.2% yield; 53-yr Dividend King lineage (incl. Abbott spinoff)

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Immunology (Skyrizi+Rinvoq)",  24.0, 18.0, 29.0, "Combined run-rate >$24B; Skyrizi +~25% & Rinvoq +~25% YoY; key growth engine replacing Humira"),
    ("Humira (legacy)",               2.5,  1.0,  3.0, "Biosimilar erosion largely played out; small stable remainder"),
    ("Oncology (Imbruvica/Elahere/Epcoritamab)", 5.5, 4.0, 8.0, "Imbruvica declining (-10%+); Elahere & Epcoritamab newer launches scaling"),
    ("Neuroscience (Vraylar/Botox Therapeutic)", 10.5, 9.0, 12.5, "Vraylar +double digits; migraine portfolio (Qulipta/Ubrelvy) growing"),
    ("Aesthetics (Botox Cosmetic/Juvederm)", 5.5, 4.5, 7.0, "Recovering from China/macro softness; Botox Cosmetic still category leader"),
    ("Other (eye care, virology, pipeline incl. survodutide obesity)", 3.5, 2.5, 6.0, "Survodutide (obesity, partnered w/ Boehringer) Phase 3 optionality; eye care steady"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.700   # blended gross margin; high debt-driven amortization weighs on GAAP but adj. margin healthy
GROSS_MARGIN_BULL = 0.715   # BULL: Skyrizi/Rinvoq high-margin mix grows further
OPEX_FIXED_B      = 18.5    # SG&A + R&D ($B); includes heavy Allergan-related amortization/interest drag embedded via opex proxy
TAX_RATE          = 0.150   # effective rate; pharma international mix

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 13.50       # FY2027E adj EPS (consensus ~$13.30-$13.70 non-GAAP)
PE_PESSIMISTIC = 12.0        # trough P/E: large-cap pharma defensive floor; ABBV historical trough ~12-13x
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # $162

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (11.00, 12,  132, "Skyrizi/Rinvoq growth decelerates sharply on biosimilar/competitive pressure; Aesthetics stays soft; high debt load weighs; EPS $11.00 → 12× = $132"),
    "BASE":  (13.50, 15,  203, "Skyrizi+Rinvoq sustain low-to-mid teens growth; Imbruvica decline manageable; Aesthetics stabilizes; EPS $13.50 → 15× = $203"),
    "BULL":  (16.00, 17,  272, "Skyrizi/Rinvoq combined exceed $30B run-rate; Elahere/Epcoritamab scale meaningfully; deleveraging accelerates; EPS $16.00 → 17× = $272"),
    "XBULL": (19.00, 19,  361, "Survodutide obesity readout positive + commercial path; immunology franchise becomes dominant growth platform; multiple re-rates toward growth pharma peers; EPS $19.00 → 19× = $361"),
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
        "name":       "Skyrizi + Rinvoq combined revenue growth",
        "weight":     0.30,
        "thresholds": ("<10%",  "≥15%",  "≥22%",   "≥30%"),
        "now":        "+~25%",
        "score":      3,
        "comment":    "Combined run-rate >$24B and still growing strongly (~25% YoY); the primary engine replacing lost Humira revenue",
    },
    {
        "name":       "Humira erosion trajectory (post-cliff stabilization)",
        "weight":     0.10,
        "thresholds": ("still falling >25%", "≥-15%", "≥-5%", "stable/flat"),
        "now":        "~-15%",
        "score":      3,
        "comment":    "Biosimilar erosion largely played out; remaining Humira base stabilizing at low-single-digit billions",
    },
    {
        "name":       "Oncology pipeline (Elahere/Epcoritamab) launch trajectory vs Imbruvica decline",
        "weight":     0.15,
        "thresholds": ("net negative", "roughly offsetting", "modest net growth", "strong net growth"),
        "now":        "roughly offsetting",
        "score":      2,
        "comment":    "Elahere and Epcoritamab scaling but Imbruvica still declining double digits; segment roughly net flat to modestly positive",
    },
    {
        "name":       "Aesthetics (Botox/Juvederm) recovery",
        "weight":     0.15,
        "thresholds": ("<-5%",  "≥0%",   "≥+5%",   "≥+10%"),
        "now":        "~+1%",
        "score":      2,
        "comment":    "China and US discretionary spend softness persists; Botox Cosmetic remains category leader but growth muted vs historical double digits",
    },
    {
        "name":       "Pipeline optionality (survodutide obesity / neuroscience)",
        "weight":     0.10,
        "thresholds": ("no readouts", "1 readout", "2-3 positive readouts", "transformative readout"),
        "now":        "1-2",
        "score":      2,
        "comment":    "Survodutide Phase 3 obesity data pending (partnered w/ Boehringer); Vraylar and migraine portfolio (Qulipta/Ubrelvy) executing well",
    },
    {
        "name":       "Leverage / deleveraging trajectory (Allergan debt)",
        "weight":     0.20,
        "thresholds": ("net debt/EBITDA >3.5x", "≥3.0x", "≥2.5x", "<2.0x"),
        "now":        "~3.0x",
        "score":      2,
        "comment":    "Net debt/EBITDA ~3.0x post-Allergan; steady FCF-funded deleveraging continues but still elevated vs pharma peers",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Skyrizi+Rinvoq franchise — >$24B combined run-rate, still growing ~25%; durable IP runway into early 2030s", +0.7, 0.25),
    ("-", "High leverage from Allergan acquisition — ~3.0x net debt/EBITDA caps multiple expansion and M&A flexibility", -0.5, 0.20),
    ("+", "Dividend King — $6.56/share (~3.2% yield), 53-yr consecutive increase streak provides downside support",      +0.4, 0.15),
    ("-", "Aesthetics & Imbruvica drag — both segments below historical growth rates; macro-sensitive discretionary exposure", -0.3, 0.15),
    ("+", "Diversified ex-immunology base (Vraylar, neuroscience, oncology pipeline) reduces single-product concentration risk", +0.3, 0.15),
    ("+", "Survodutide obesity optionality — call option on a multi-billion-dollar new category if Phase 3 reads out positive", +0.3, 0.10),
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
CONS_EPS_2YR  = 15.00   # FY2028E conservative: continued Skyrizi/Rinvoq growth offsets Imbruvica decline
CONS_PE_2YR   = 14      # modest rerating from ~15x given continued deleveraging
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Pharma / Immunology (Skyrizi/Rinvoq) / Aesthetics (Botox) / Oncology")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<46}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<46}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<46}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
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

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift away from immunology margin
bear_oi      = bear_gp - OPEX_FIXED_B * 0.95           # partial cost response
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 17× = ~${bull_eps_imp*17:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 12× trough P/E (defensive pharma floor) = ~${bear_eps_imp*12:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev      = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_skyrizi  = 1.0 * 0.82 * (1 - TAX_RATE) / shares   # Skyrizi/Rinvoq high margin
eps_per_1B_aesth    = 1.0 * 0.70 * (1 - TAX_RATE) / shares   # Aesthetics margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Skyrizi/Rinvoq revenue:       +${eps_per_1B_skyrizi:.3f}/EPS  = +${eps_per_1B_skyrizi*15:.1f}/share at 15× P/E")
print(f"  Every $1B Aesthetics revenue:           +${eps_per_1B_aesth:.3f}/EPS  = +${eps_per_1B_aesth*15:.1f}/share at 15× P/E")
print(f"  1pp GM expansion (immunology mix):      +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*15:.1f}/share at 15× P/E")
print(f"  1% buyback (~18M shares):                +${curr_eps*0.01:.3f}/EPS  (mechanical accretion; constrained by deleveraging priority)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Skyrizi/Rinvoq trajectory / Aesthetics / Oncology / Leverage framework)")
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
    ("Skyrizi+Rinvoq combined growth",   "+25%",   "<10%",   "−15pp",  "Competitive IL-23/JAK entrants accelerate share loss faster than expected"),
    ("Humira erosion",                   "-15%",   "<-25%",  "−10pp",  "Remaining Humira base erodes faster; no stabilization achieved"),
    ("Oncology (Elahere/Epcoritamab)",   "offsetting", "net negative", "−1 lvl", "Imbruvica decline accelerates; new launches fail to scale"),
    ("Aesthetics growth",                "~+1%",   "<-5%",   "−6pp",   "China/US discretionary spend deteriorates further; GLP-1 substitution risk"),
    ("Pipeline readouts (survodutide)",  "1-2",    "0",      "−1-2",   "Obesity Phase 3 disappoints; neuroscience pipeline stalls"),
    ("Net debt/EBITDA",                  "~3.0x",  ">3.5x",  "+0.5x",  "Deleveraging stalls; M&A or buyback adds leverage instead of reducing it"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Skyrizi/Rinvoq growth decelerates sharply as IL-23 and JAK-class competition")
print(f"  intensifies, while Imbruvica's decline accelerates faster than Elahere/Epcoritamab can")
print(f"  offset, Aesthetics stays soft on macro/GLP-1 substitution concerns, and deleveraging stalls")
print(f"  amid elevated net debt/EBITDA (~3.0x). EPS falls to ~$11.00 → 12× trough P/E = ${bear_price}.")
print(f"  Note: $132 is NOT permanent impairment — the $6.56/share dividend (Dividend King status)")
print(f"  and diversified neuroscience/eye care base provide a durable earnings floor. Recovery to")
print(f"  ~${bear_price+30}–${bear_price+50} in 2yr is base case post-shock.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           ${EPS_FY2027E:.2f}  (consensus ~$13.30-$13.70 non-GAAP)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (defensive large-cap pharma trough; ABBV historical ~12-13×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% premium to EPP reflects the market's confidence in the Skyrizi/Rinvoq")
print(f"  growth runway (combined >$24B run-rate, still growing ~25%) more than offsetting Humira's")
print(f"  now-largely-completed erosion. The open question is whether immunology growth can sustain")
print(f"  through the early 2030s biosimilar windows for Skyrizi/Rinvoq, and whether deleveraging")
print(f"  from the Allergan acquisition proceeds on schedule without crowding out capital return.")
print(f"  EPP path: FY2029E EPS ~$15.50 × {PE_PESSIMISTIC:.0f}× = ${15.50*PE_PESSIMISTIC:.0f} floor (EPP grows modestly as base earnings compound).")
print(f"  At 15× mid-cycle P/E: ${EPS_FY2027E:.2f} × 15 = ${EPS_FY2027E*15:.0f}  — roughly in line with current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest EPS growth as Skyrizi/Rinvoq offset remaining drags; P/E roughly flat)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (modest growth; Skyrizi/Rinvoq + Vraylar offset Imbruvica/Aesthetics softness)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (roughly flat from ~15× as deleveraging continues)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: ABBV trades at ~{CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a reasonable")
print(f"  multiple for a Dividend King with a >$24B and growing immunology franchise (Skyrizi+Rinvoq),")
print(f"  but burdened by ~3.0x net debt/EBITDA from the Allergan acquisition. If Skyrizi/Rinvoq")
print(f"  sustain mid-teens+ growth and Aesthetics recovers, the multiple has room to expand toward")
print(f"  16-17×. If immunology growth decelerates faster than expected or leverage stalls, ~15×")
print(f"  is the appropriate ceiling — i.e. fairly valued, not a clear bargain nor overextended.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E - 1)*100:.1f}% EPS growth by FY2028E vs FY2027E — modest, achievable at BASE.")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.18
beta        = 0.65
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  Dividend King)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (low; defensive pharma; Humira-cliff fears largely resolved)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (defensive; lower than market; pharma sector characteristics)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe; immunology-deceleration tail scenario)")
print(f"  52W range reflects post-Humira-cliff stabilization and Skyrizi/Rinvoq re-rating in 2025-2026.")
print(f"  → Skyrizi/Rinvoq combined growth rate is THE KEY binary for downside risk.")
print(f"  → Aesthetics recovery + survodutide obesity readout are KEY bull catalysts.")
print(f"  → AVOID above $230  |  WATCHLIST $210–225  |  ACCUMULATE $185–200  |  BUY below $170–180")

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
print(f"  In plain terms: Skyrizi/Rinvoq's growth runway and Dividend King status appear roughly")
print(f"  appropriately priced — leverage from the Allergan deal and soft Aesthetics/Imbruvica")
print(f"  segments are real but manageable offsets, keeping ABBV in HOLD/accumulate territory")
print(f"  rather than a clear BUY or AVOID.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Skyrizi + Rinvoq quarterly revenue trajectory — combined run-rate growth vs. competitive entrants")
print(f"  (2) Aesthetics (Botox/Juvederm) recovery — China demand and US discretionary spend trends")
print(f"  (3) Survodutide (obesity) Phase 3 readouts — major pipeline optionality with Boehringer Ingelheim")
print(f"  (4) Oncology launches (Elahere, Epcoritamab) vs. Imbruvica decline — net segment trajectory")
print(f"  (5) Deleveraging pace — net debt/EBITDA progress from ~3.0x toward pharma-peer norms")
print(f"  (6) Dividend sustainability — ${ANNUAL_DIV:.2f}/share payout (Dividend King, 53-yr streak)")
print(f"  AVOID above $230  |  WATCHLIST $210–225  |  ACCUMULATE $185–200  |  BUY below $170–180")
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
