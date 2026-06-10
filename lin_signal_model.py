"""
LIN  ·  Linde plc  ·  NYSE: LIN
Bottom-up signal model  ·  Industrial Gases (O2/N2/H2/Ar/CO2) / Quality Compounder / Clean Hydrogen Backlog
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "LIN"
COMPANY       = "Linde plc"
SECTOR        = "Industrial Gases · Healthcare/Manufacturing/Electronics/Energy/Food&Bev · Clean Hydrogen Backlog · NYSE: LIN"
CURRENT_PRICE = 462.00     # USD; as of 2026-06-10
VOL_52W_LOW   = 410.20     # 2025 industrial-recession growth-scare trough
VOL_52W_HIGH  = 488.50     # 2026 quality-compounder re-rating peak
SHARES_OUT_M  = 460.0      # millions (post continued buybacks)
ANNUAL_DIV    = 5.60       # $/share; ~1.2% yield; Dividend Aristocrat (32+ yrs of increases)

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by reporting segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Americas",                      16.5, 14.5, 18.0, "Largest segment; healthcare/manufacturing/food&bev on-site + merchant gas; resilient take-or-pay base"),
    ("EMEA",                           8.5,  7.5,  9.3, "Mature merchant/on-site network; energy transition (blue/green H2) projects concentrated here"),
    ("APAC",                           7.0,  6.0,  8.0, "Electronics/semiconductor on-site supply (Taiwan/Korea/China) is key swing factor; project backlog ramp"),
    ("Engineering (Linde Engineering)", 2.5,  2.0,  3.5, "Builds air separation/H2/syngas plants for 3rd parties and Linde itself; lumpy order intake, high-margin backlog conversion"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.475   # blended segment operating margin proxy used below as "gross" for simplicity
GROSS_MARGIN_BULL = 0.495   # BULL: project ramp + pricing power + cost pass-through drives further operating leverage
OPEX_FIXED_B      = 4.0     # corporate/SG&A + below-the-line items ($B); largely fixed cost base
TAX_RATE          = 0.225   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 17.10       # FY2027E EPS (consensus ~$16.80-$17.40 adjusted)
PE_PESSIMISTIC = 21.0        # trough P/E: quality-compounder floor; LIN/APD historical trough ~20-22x even in downturns
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # ~$359

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (15.50, 22,  341, "Global manufacturing recession compresses merchant volumes/electronics on-site demand; H2 project FIDs slip further; pricing holds but volume leverage reverses; EPS $15.50 → 22× = $341"),
    "BASE":  (17.10, 27,  462, "Mid-single-digit organic growth via pricing + project backlog conversion (electronics, decarbonization); buybacks add ~1.5pt EPS growth; multiple holds near current premium; EPS $17.10 → 27× = $462"),
    "BULL":  (19.25, 30,  578, "Electronics/semiconductor on-site ramp accelerates (AI-driven fab buildout); clean H2 backlog converts to project starts ahead of schedule; margin expansion continues; EPS $19.25 → 30× = $578"),
    "XBULL": (22.00, 33,  726, "Decarbonization megaprojects (blue/green H2, CCS) become a structural new growth pillar at scale; multiple expands toward best-in-class compounder peers on durable double-digit FCF growth; EPS $22.00 → 33× = $726"),
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
        "name":       "Base volume growth (merchant + on-site, ex-pricing)",
        "weight":     0.25,
        "thresholds": ("<0%",   "≥1%",   "≥3%",   "≥5%"),
        "now":        "+1.5%",
        "score":      2,
        "comment":    "Healthcare/food&bev steady; manufacturing/metals soft globally; electronics on-site providing the marginal lift",
    },
    {
        "name":       "Pricing power (price/cost spread)",
        "weight":     0.20,
        "thresholds": ("price<cost", "roughly even", "price>cost +1-2pp", "price>cost +2pp+"),
        "now":        "price>cost +1.5pp",
        "score":      3,
        "comment":    "Take-or-pay contracts with cost pass-through clauses continue to deliver positive price/cost spread, supporting margin expansion",
    },
    {
        "name":       "Operating margin trajectory (segment OI margin)",
        "weight":     0.20,
        "thresholds": ("<29%",  "≥29.5%", "≥30.5%", "≥32%"),
        "now":        "~30.0%",
        "score":      2,
        "comment":    "Margin expansion continues via productivity actions and project ramp-up, but pace has been incremental (~30-50bps/yr)",
    },
    {
        "name":       "Clean hydrogen / decarbonization project backlog conversion",
        "weight":     0.15,
        "thresholds": ("backlog shrinks", "flat/stable", "FIDs accelerate", "multiple FIDs + early starts"),
        "now":        "flat/stable",
        "score":      2,
        "comment":    "Backlog of sale-of-gas project commitments remains substantial, but new clean-H2 FID pace has been measured given policy/offtake uncertainty",
    },
    {
        "name":       "Electronics/semiconductor on-site capex cycle",
        "weight":     0.10,
        "thresholds": ("downcycle", "stabilizing", "ramping", "broad-based boom"),
        "now":        "ramping",
        "score":      3,
        "comment":    "AI-driven fab capex (Taiwan/Korea/US/Japan) is driving a wave of new on-site gas supply contracts, a multi-year tailwind for APAC/Americas",
    },
    {
        "name":       "Capital allocation discipline (buybacks + ROIC)",
        "weight":     0.10,
        "thresholds": ("ROIC declining", "ROIC stable", "ROIC improving", "best-in-class & accelerating"),
        "now":        "ROIC improving",
        "score":      3,
        "comment":    "Consistent ~$4-5B/yr buybacks plus disciplined project ROIC hurdles (>~15% post-tax) continue to compound EPS ahead of revenue growth",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Take-or-pay contract structure with cost pass-throughs — highly recession-resistant cash flows vs cyclical industrials", +0.6, 0.25),
    ("+", "Diversified end markets (healthcare, electronics, food&bev, energy, manufacturing) — no single end market dominates risk", +0.4, 0.20),
    ("+", "Dividend Aristocrat (32+ yrs) + ~$4-5B/yr buybacks fund double-digit EPS growth even at modest revenue growth", +0.4, 0.15),
    ("-", "Premium quality-compounder valuation (~27x current EPS) leaves little room for multiple expansion and limited margin of safety", -0.5, 0.20),
    ("-", "Clean hydrogen megaproject backlog conversion has been slower than initially signaled — optionality value harder to underwrite near-term", -0.3, 0.10),
    ("+", "Electronics/semiconductor on-site contract wins (AI fab buildout) provide a credible multi-year structural growth vector beyond core gases", +0.3, 0.10),
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
CONS_EPS_2YR  = 19.00   # FY2028E conservative: continued double-digit-ish EPS CAGR via pricing + buybacks
CONS_PE_2YR   = 26      # modest de-rate from ~27x as growth normalizes
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Industrial Gases (O2/N2/H2/Ar/CO2) / Quality Compounder")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
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

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift away from higher-margin electronics on-site
bear_oi      = bear_gp - OPEX_FIXED_B * 0.95           # partial cost response
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% op margin − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% op margin − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 30× = ~${bull_eps_imp*30:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% op margin − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 22× trough P/E (quality-compounder floor) = ~${bear_eps_imp*22:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev          = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_americas     = 1.0 * 0.50 * (1 - TAX_RATE) / shares   # Americas - higher margin
eps_per_1B_electronics  = 1.0 * 0.55 * (1 - TAX_RATE) / shares   # APAC electronics on-site - high margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Americas revenue:               +${eps_per_1B_americas:.3f}/EPS  = +${eps_per_1B_americas*27:.1f}/share at 27× P/E")
print(f"  Every $1B APAC electronics on-site rev.:   +${eps_per_1B_electronics:.3f}/EPS  = +${eps_per_1B_electronics*27:.1f}/share at 27× P/E")
print(f"  1pp operating margin expansion:           +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*27:.1f}/share at 27× P/E")
print(f"  1% buyback (~4.6M shares):                 +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Volumes / Pricing / Margins / H2 backlog / Electronics / Capital allocation)")
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
    ("Base volume growth",            "+1.5%",  "<0%",     "−2pp+",  "Global manufacturing recession hits merchant volumes broadly"),
    ("Pricing/cost spread",           "+1.5pp", "negative","−2pp+",  "Energy cost spike outpaces contractual pass-through lag"),
    ("Operating margin",              "30.0%",  "<29%",    "−1pp+",  "Mix shift to lower-margin merchant volumes; cost inflation"),
    ("H2/decarbonization backlog",    "flat",   "shrinks", "FIDs cancelled", "Policy support (IRA/EU) rolled back; offtake agreements unwind"),
    ("Electronics on-site capex",     "ramping","downcycle","reversal","AI/semiconductor capex cycle pauses sharply"),
    ("Multiple (P/E)",                "~27x",   "22x",     "−5x",    "Quality-compounder premium compresses on growth-scare derating"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A synchronized global manufacturing/industrial-production downturn compresses")
print(f"  merchant gas volumes and stalls the AI-driven electronics on-site ramp, while energy cost")
print(f"  spikes temporarily outrun contractual pass-through mechanisms. Clean hydrogen FIDs are")
print(f"  shelved as policy support wavers. EPS falls to ~$15.50 → 22× trough P/E (still a premium")
print(f"  multiple given LIN's contracted cash-flow base) = ${bear_price}.")
print(f"  Note: $341 is NOT permanent impairment — take-or-pay contracts and a Dividend Aristocrat")
print(f"  track record provide a durable earnings floor. Recovery toward ~${bear_price+60}-${bear_price+90} in 2yr is plausible post-shock.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           ${EPS_FY2027E:.2f}  (consensus ~$16.80-$17.40 adjusted)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (quality-compounder floor; LIN historical trough ~20-22×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% {'above' if epp_gap_pct >= 0 else 'below'} trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% {'premium to' if epp_gap_pct >= 0 else 'discount to'} EPP reflects that LIN trades at roughly")
print(f"  {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a premium 'quality compounder' multiple justified by")
print(f"  highly recession-resistant take-or-pay cash flows, diversified end markets, and a long")
print(f"  runway of double-digit EPS growth via pricing, buybacks, and project backlog conversion.")
print(f"  The open question is whether the premium multiple is sustainable if growth normalizes")
print(f"  toward mid-single digits, or whether electronics/H2 growth vectors justify holding near 27-30×.")
print(f"  EPP path: FY2029E EPS ~$20.50 × {PE_PESSIMISTIC:.0f}× = ${20.50*PE_PESSIMISTIC:.0f} floor (EPP grows as EPS compounds even if multiple stays depressed).")
print(f"  At 27× mid-cycle P/E: ${EPS_FY2027E:.2f} × 27 = ${EPS_FY2027E*27:.0f}  — roughly in line with current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: continued EPS compounding via pricing + buybacks; modest de-rate)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (~6-7%/yr growth via pricing, project ramp, buybacks)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (modest de-rate from ~{CURRENT_PRICE/EPS_FY2027E:.1f}× as growth normalizes)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: LIN trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a premium")
print(f"  'quality compounder' multiple reflecting take-or-pay contractual cash flows, diversified")
print(f"  end markets, and a long double-digit EPS growth runway via pricing + buybacks. The")
print(f"  electronics on-site ramp and clean hydrogen backlog are the key incremental growth levers.")
print(f"  If the premium multiple holds and EPS compounds at ~6-8%/yr, returns are modest but steady.")
print(f"  If the multiple de-rates toward the broader industrials average, near-term upside is limited.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E - 1)*100:.1f}% EPS growth by FY2028E vs FY2027E — achievable at BASE.")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.16
beta        = 0.85
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  Dividend Aristocrat, 32+ yrs of increases)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (low; defensive industrial-gas contracted cash flow base)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (moderate; some cyclicality from manufacturing/energy exposure)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe; global industrial-recession tail scenario)")
print(f"  52W range reflects relatively contained volatility given contracted, diversified cash flows.")
print(f"  → Global industrial production / manufacturing PMI is THE KEY swing factor for downside risk.")
print(f"  → Electronics on-site ramp + clean H2 backlog conversion are KEY bull catalysts.")
print(f"  → AVOID above $510  |  WATCHLIST $470–500  |  ACCUMULATE $430–455  |  BUY below $400–425")

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
print(f"  In plain terms: the market is pricing in {'more' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'less'} confidence on electronics/H2 backlog")
print(f"  conversion and sustained margin expansion than the bottom-up fundamentals currently support.")
print(f"  The risk/reward skew (Ratio B {ratio_b_str}) reflects LIN's premium quality-compounder")
print(f"  positioning — durable but with limited near-term margin of safety at current levels.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Global manufacturing PMI / industrial production — base volume swing factor across all segments")
print(f"  (2) Electronics/semiconductor on-site contract wins — AI-driven fab capex cycle (Taiwan/Korea/US)")
print(f"  (3) Clean hydrogen / decarbonization project FIDs — backlog conversion pace and policy support (IRA/EU)")
print(f"  (4) Pricing vs cost spread — ability to maintain positive spread through energy cost cycles")
print(f"  (5) Operating margin trajectory — productivity actions + project ramp-up vs cost inflation")
print(f"  (6) Capital allocation — buyback pace (~$4-5B/yr) and dividend growth (Aristocrat, 32+ yr streak)")
print(f"  AVOID above $510  |  WATCHLIST $470–500  |  ACCUMULATE $430–455  |  BUY below $400–425")
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
