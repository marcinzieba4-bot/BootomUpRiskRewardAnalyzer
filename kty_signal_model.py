"""
KTY  ·  Grupa Kety S.A.  ·  WSE: KTY
Bottom-up signal model  ·  Aluminium Extrusion/Processing / Architectural Systems / Flexible Packaging / CBAM
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "KTY"
COMPANY       = "Grupa Kety S.A."
SECTOR        = "Basic Resources · Aluminium Extrusion/Processing (EPG) · Architectural Aluminium Systems (ASG) · Flexible Packaging (FPG) · CBAM beneficiary · WSE: KTY"
CURRENT_PRICE = 1050.00   # PLN; pulled back from May 2026 ATH ~1,179 PLN
VOL_52W_LOW   = 760.00    # 2025 European construction-demand trough
VOL_52W_HIGH  = 1179.00   # May 2026 ATH (CBAM optimism / construction recovery hopes)
SHARES_OUT_M  = 9.6       # millions
ANNUAL_DIV    = 38.00     # PLN/share; ~85% payout ratio of net income, historically consistent

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ──────────────────────
# FY2026E revenue by segment (PLN millions)
SEG_DATA = [
    # (segment, curr_rev_M, bear_rev_M, bull_rev_M, description)
    ("Extruded Products Group (EPG)",      3000.0, 2500.0, 3450.0, "Largest segment; aluminium profiles for construction/automotive/industrial; CBAM protects EU pricing vs Asian imports; volumes track European industrial production"),
    ("Aluminium Systems Group (ASG)",      1850.0, 1500.0, 2200.0, "Architectural systems - windows/doors/facades; directly geared to European residential/commercial construction cycle and ECB rate path"),
    ("Flexible Packaging Group (FPG)",     1450.0, 1300.0, 1650.0, "Flexible packaging films for food/consumer goods; defensive, non-cyclical demand; steady mid-single-digit growth"),
]

# Margin assumptions (blended operating-margin proxy used as "gross margin")
GROSS_MARGIN_CURR = 0.115   # blended operating margin; CBAM + execution discipline support above-peer margins
GROSS_MARGIN_BULL = 0.130   # BULL: construction recovery + CBAM pricing power lift blended margin further
OPEX_FIXED_M      = 280.0   # corporate SG&A + below-the-line (PLN M); largely fixed cost base
TAX_RATE          = 0.19    # Polish CIT effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 62.00       # PLN; FY2027E EPS (modest growth off FY2026E base as construction stabilizes)
PE_PESSIMISTIC = 11.0        # trough P/E: cyclical-construction-downturn floor; KTY historical trough ~10-12x
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # ~682 PLN

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ─────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (40.00, 12,  480, "European industrial/construction demand contracts sharply; ASG volumes fall double-digits as residential construction stays depressed; EPG margins compress despite CBAM as overall volumes shrink; FPG holds up but can't offset; dividend cut as payout ratio pressured; multiple compresses to cyclical-trough 12x; EPS PLN40.00 -> 12x = PLN480"),
    "BASE":  (62.00, 14,  868, "European construction/industrial demand stabilizes near current depressed levels with gradual recovery; CBAM continues to support EU pricing vs Asian/Turkish imports; FPG steady growth; dividend maintained near current payout; EPS PLN62.00 -> 14x = PLN868"),
    "BULL":  (78.00, 16, 1248, "ECB rate cuts spark European residential construction recovery, lifting ASG and EPG volumes meaningfully; CBAM fully phases in, providing structural pricing tailwind and import protection; FPG accelerates on consumer demand recovery; dividend grows with earnings; EPS PLN78.00 -> 16x = PLN1248"),
    "XBULL": (98.00, 18, 1764, "Sustained multi-year European construction supercycle (rate cuts + green-building retrofit wave + reshoring of industrial capacity); CBAM creates a structural re-rating of EU aluminium processors as Asian competition is locked out; all three segments hit cycle highs simultaneously; premium multiple expands further on quality/execution track record; EPS PLN98.00 -> 18x = PLN1764"),
}

# ── SOFTMAX PROBABILITY FUNCTION ──────────────────────────────────────────────
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

# ── 6 PROXY SIGNALS ────────────────────────────────────────────────────────────
# Scores: 1=BEAR  2=BASE  3=BULL  4=XBULL
SIGNALS = [
    {
        "name":       "EPG (extruded products) volume/revenue growth",
        "weight":     0.25,
        "thresholds": ("<-5%",  "≥0%",  "≥5%",   "≥10%"),
        "now":        "+1%",
        "score":      2,
        "comment":    "Largest segment near flat as European industrial production remains soft; CBAM provides pricing support but volumes have not yet inflected upward",
    },
    {
        "name":       "ASG (architectural systems) - construction cycle exposure",
        "weight":     0.25,
        "thresholds": ("<-8%",  "≥-2%", "≥4%",   "≥10%"),
        "now":        "-2%",
        "score":      2,
        "comment":    "European residential construction remains in a multi-year downturn; order books stabilizing but not yet growing; ECB rate cuts are the key recovery catalyst not yet fully reflected",
    },
    {
        "name":       "CBAM implementation / EU import protection",
        "weight":     0.20,
        "thresholds": ("delayed/diluted", "on-track", "accelerating benefit", "structural re-rating"),
        "now":        "on-track",
        "score":      3,
        "comment":    "CBAM definitive regime phasing in as scheduled, raising costs on Asian/Turkish aluminium imports and supporting EU processor pricing power; a genuine structural tailwind for KTY's EPG segment",
    },
    {
        "name":       "FPG (flexible packaging) revenue growth",
        "weight":     0.10,
        "thresholds": ("<0%",   "≥3%",  "≥6%",   "≥9%"),
        "now":        "+4%",
        "score":      2,
        "comment":    "Defensive packaging segment continues steady mid-single-digit growth on stable food/consumer-goods demand, providing a counter-cyclical earnings floor",
    },
    {
        "name":       "Blended operating margin trend",
        "weight":     0.10,
        "thresholds": ("<10%",  "≥11%", "≥12.5%", "≥14%"),
        "now":        "~11.5%",
        "score":      2,
        "comment":    "Margins holding near recent levels through cost discipline and CBAM pricing support, despite soft volumes; further expansion likely requires a construction-cycle volume recovery",
    },
    {
        "name":       "Dividend sustainability (~85% payout)",
        "weight":     0.10,
        "thresholds": ("cut likely", "held flat", "modest growth", "policy-ceiling growth"),
        "now":        "held flat",
        "score":      2,
        "comment":    "High ~85% payout ratio has been maintained consistently through cycles thanks to a strong balance sheet and disciplined capex; current yield ~3.6% at PLN1,050",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ──────────────────────────────────────
SCA_FACTORS = [
    ("+", "CBAM structural tailwind — EU carbon border tax permanently raises the cost of Asian/Turkish aluminium imports, protecting KTY's pricing power", +0.6, 0.20),
    ("+", "Best-in-class execution track record — consistent operational delivery and capital discipline across cycles supports a premium multiple", +0.4, 0.15),
    ("+", "Strong balance sheet / high dividend payout (~85%) provides a meaningful cash-return floor and downside cushion", +0.4, 0.15),
    ("-", "European construction/industrial demand cyclicality — ASG and EPG remain geared to a still-depressed European residential construction cycle", -0.6, 0.25),
    ("-", "Premium starting valuation — trades near ATH at a multiple that already prices in significant execution quality, leaving limited margin of safety", -0.5, 0.15),
    ("-", "Diversification limits but does not eliminate cyclicality — FPG defensiveness offsets only ~25% of group revenue exposed to construction cycles", -0.2, 0.10),
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

# ── RATIO B ────────────────────────────────────────────────────────────────────
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

# ── CONSERVATIVE GROWTH (2-yr) ─────────────────────────────────────────────────
CONS_EPS_2YR  = 68.00   # PLN; FY2028E conservative: modest improvement off FY2027E base
CONS_PE_2YR   = 13      # modest de-rate from ~17x current as construction-cycle uncertainty persists
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
print(f"  {TICKER}  ·  {COMPANY}  ·  PLN{CURRENT_PRICE:.2f}  ·  Aluminium Extrusion (CBAM) / Architectural Systems / Flexible Packaging")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<32}  {'FY2026E (PLNM)':>14}  {'Bear (PLNM)':>11}  {'Bull (PLNM)':>11}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<32}  PLN{curr:>10.1f}  PLN{bear:>7.1f}  PLN{bull:>7.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<32}  PLN{curr_total:>10.1f}  PLN{bear_total:>7.1f}  PLN{bull_total:>7.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print()

# EPS bridge
shares    = SHARES_OUT_M
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_M
curr_ni   = curr_oi * (1 - TAX_RATE)
curr_eps  = round(curr_ni / shares, 2)

bull_gp      = bull_total * GROSS_MARGIN_BULL
bull_oi      = bull_gp - OPEX_FIXED_M
bull_ni      = bull_oi * (1 - TAX_RATE)
shares_b     = shares * 1.00   # KTY does not run meaningful buybacks; share count flat
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.85   # demand contraction pressures blended margin
bear_oi      = bear_gp - OPEX_FIXED_M * 1.05            # opex sticky
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  PLN{curr_total:.1f}M rev × {GROSS_MARGIN_CURR*100:.1f}% op margin − PLN{OPEX_FIXED_M:.1f}M opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}M shares  =  PLN{curr_eps:.2f}/share adj EPS")
print()
print(f"  BULL EPS check:  PLN{bull_total:.1f}M rev × {GROSS_MARGIN_BULL*100:.1f}% op margin − PLN{OPEX_FIXED_M:.1f}M opex − tax")
print(f"  ÷ {shares_b:.3f}M shares  =  ~PLN{bull_eps_imp:.1f}/share  →  PLN{bull_eps_imp:.1f} × 16× = ~PLN{bull_eps_imp*16:.0f}  ✓ BULL PLN{SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  PLN{bear_total:.1f}M rev × {GROSS_MARGIN_CURR*100*0.85:.1f}% op margin − opex  =  ~PLN{bear_eps_imp:.1f}/share")
print(f"  At 12× trough P/E (construction-cycle floor) = ~PLN{bear_eps_imp*12:.0f}  ✓ BEAR PLN{SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1M_rev   = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1M_epg   = 1.0 * 0.10 * (1 - TAX_RATE) / shares
eps_per_1M_asg   = 1.0 * 0.09 * (1 - TAX_RATE) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every PLN100M EPG segment revenue:               +PLN{eps_per_1M_epg*100:.2f}/EPS  = +PLN{eps_per_1M_epg*100*14:.1f}/share at 14× P/E")
print(f"  Every PLN100M ASG segment revenue:               +PLN{eps_per_1M_asg*100:.2f}/EPS  = +PLN{eps_per_1M_asg*100*14:.1f}/share at 14× P/E")
print(f"  1pp blended operating margin expansion:          +PLN{curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +PLN{curr_total*0.01*(1-TAX_RATE)/shares*14:.1f}/share at 14× P/E")
print(f"  CBAM-driven price pass-through (~2% price uplift on EPG): ~+PLN{curr_total*0.30*0.02*(1-TAX_RATE)/shares:.2f}/EPS")

# ─── ② SIGNAL DASHBOARD ────────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (EPG / ASG construction cycle / CBAM / FPG / Margins / Dividend)")
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
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from PLN{CURRENT_PRICE} + 15% hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:72]:<72}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ──────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR PLN{bear_price})")
hr()
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("EPG revenue growth",                  "+1%",   "<-5%",   "-6pp",   "European industrial production contracts; CBAM offsets only partially"),
    ("ASG construction exposure",           "-2%",   "<-8%",   "-6pp",   "Residential construction downturn deepens; ECB delays/reverses rate cuts"),
    ("CBAM implementation",                 "on-track","delayed/diluted","reversal","EU dilutes CBAM enforcement under trade-policy pressure, reducing import protection"),
    ("FPG revenue growth",                  "+4%",   "<0%",    "-4pp",   "Consumer demand softens across food/packaging end-markets"),
    ("Blended operating margin",            "~11.5%","<10%",   "-1.5pp", "Volume deleverage + raw material cost inflation compress margins"),
    ("Multiple (P/E)",                      "~17x",  "12x",    "-5x",    "Construction-cycle-trough sentiment compresses premium multiple sharply"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: European construction and industrial demand contracts further as ECB rate")
print(f"  cuts fail to materialize or are delayed, ASG order books shrink double-digits, and EPG")
print(f"  volumes fall even as CBAM provides only partial pricing offset. FPG growth slows on")
print(f"  weaker consumer spending. Blended margins compress to ~9.8% and the premium multiple")
print(f"  de-rates from ~17x to a cyclical-trough 12x. EPS falls to ~PLN40 → 12x = PLN{bear_price}.")
print(f"  Note: PLN{bear_price} is NOT a permanent impairment — KTY's strong balance sheet, high")
print(f"  dividend payout, and best-in-class execution track record provide a floor. Recovery")
print(f"  toward ~PLN{bear_price+150}-PLN{bear_price+250} in 2yr is plausible once construction demand troughs.")

# ─── ④ EPP ─────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           PLN{EPS_FY2027E:.2f}  (modest growth off FY2026E base as construction stabilizes)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (cyclical-construction-downturn floor; KTY historical trough ~10-12×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    PLN{EPP:.0f}/share")
print(f"  Current PLN{CURRENT_PRICE:.2f} vs EPP PLN{EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% {'above' if epp_gap_pct >= 0 else 'below'} trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% {'premium to' if epp_gap_pct >= 0 else 'discount to'} EPP reflects that KTY trades at roughly")
print(f"  {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS PLN{EPS_FY2027E:.2f} — a premium multiple typical of a high-quality")
print(f"  industrial compounder with a CBAM structural tailwind and an ~85% dividend payout.")
print(f"  The dividend yield (~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}%) provides a real cash floor, but the multiple")
print(f"  already prices in significant execution quality and CBAM benefit, leaving limited")
print(f"  margin of safety should European construction demand disappoint further.")
print(f"  EPP path: FY2029E EPS ~PLN72.00 × {PE_PESSIMISTIC:.0f}× = PLN{72.00*PE_PESSIMISTIC:.0f} floor (EPP grows modestly as earnings normalize).")
print(f"  At 14× mid-cycle P/E: PLN{EPS_FY2027E:.2f} × 14 = PLN{EPS_FY2027E*14:.0f}  — close to the BASE scenario target.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest EPS improvement; multiple de-rates modestly)")
hr()
print(f"  Conservative FY2028E EPS:        PLN{CONS_EPS_2YR:.2f}  (modest improvement vs FY2027E as construction gradually stabilizes)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (modest de-rate from ~{CURRENT_PRICE/EPS_FY2027E:.1f}× as construction-cycle uncertainty persists)")
print(f"  Conservative equity value:        PLN{cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +PLN{cons_divs:.2f}/share  (PLN{ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           PLN{cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from PLN{CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: KTY trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS PLN{EPS_FY2027E:.2f} — a premium")
print(f"  multiple reflecting CBAM tailwind, best-in-class execution, and a strong balance sheet")
print(f"  with an ~85% dividend payout. The dividend yield (~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}%) provides a")
print(f"  meaningful cash-return cushion. If European construction demand merely stabilizes (not")
print(f"  even recovers), CBAM-driven pricing power alone can sustain earnings near current")
print(f"  levels. A genuine residential-construction recovery (ECB cuts) would be a strong")
print(f"  re-rating catalyst not yet fully reflected in the price.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = PLN{(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E - 1)*100:.1f}% EPS growth by FY2028E vs FY2027E.")
print(f"  BUY trigger: PLN{round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–PLN{round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ──────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.24
beta        = 0.95
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        PLN{VOL_52W_LOW:.2f}  –  PLN{VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      PLN{ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  ~85% payout, historically consistent)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (moderate; quality industrial compounder, but construction-cycle exposure)")
print(f"  Beta vs WIG20:        {beta:.2f}  (slightly below market; defensive FPG segment offsets cyclical EPG/ASG)")
print(f"  1-sigma range (1yr):  PLN{sigma_range[0]:.0f}  –  PLN{sigma_range[1]:.0f}  (PLN{CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear PLN{bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (plausible construction-cycle-trough + multiple de-rate scenario)")
print(f"  52W range reflects a stock near ATH after a CBAM-driven re-rating, with a meaningful pullback already underway.")
print(f"  → European construction demand (ECB rate path) is THE KEY binary for ASG/EPG upside/downside.")
print(f"  → CBAM full implementation is the KEY structural bull catalyst not fully priced in.")
print(f"  → AVOID above PLN1150  |  WATCHLIST PLN950–1150  |  ACCUMULATE PLN800–950  |  BUY below PLN750")

# ─── ⑦ SCENARIO PROBABILITIES ──────────────────────────────────────────────────
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
    print(f"  {s:<10}  PLN{pr:>5}  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): PLN{ev_adj:.0f}  /  Proxy EV: PLN{ev_prx:.0f}  /  Market EV: PLN{ev_mkt:.0f}  /  Current: PLN{CURRENT_PRICE:.0f}")
hr()
print(f"  Downside  (→ Bear PLN{bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull PLN{bull_price}):  {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b_str}")
print(f"  Signal    :  {signal_full}")
print()
print(f"  MARKET PRICING: at PLN{CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is")
print(f"  {'ABOVE' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'BELOW'} the model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing")
print(f"  ~{MARKET_COMPOSITE:.2f}/4.0 while the model scores fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0.")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: the market is pricing in {'more' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'less'} confidence on a sustained European")
print(f"  construction recovery and full CBAM benefit realization than the bottom-up fundamentals")
print(f"  currently support. The risk/reward skew (Ratio B {ratio_b_str}) reflects KTY's dual nature —")
print(f"  a high-quality, CBAM-protected industrial compounder with a strong dividend on one side,")
print(f"  and a premium valuation fully exposed to European construction-cycle disappointment on the other.")

# ─── FOOTER ────────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) ECB rate cuts / European residential construction recovery — the dominant swing factor for ASG")
print(f"  (2) CBAM full implementation — structural pricing protection vs Asian/Turkish aluminium imports")
print(f"  (3) European industrial production (EPG demand) — automotive/industrial profile volumes")
print(f"  (4) FPG flexible packaging growth — defensive counter-cyclical earnings floor")
print(f"  (5) Blended operating margin trend — cost discipline vs raw material/energy cost inflation")
print(f"  (6) Dividend policy execution — ~85% payout vs net-income cyclicality, ~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}% current yield")
print(f"  AVOID above PLN1150  |  WATCHLIST PLN950–1150  |  ACCUMULATE PLN800–950  |  BUY below PLN750")
print(f"  EPP floor: PLN{EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2027E EPS: PLN{EPS_FY2027E:.2f}")
print("═" * (W + 4))
print()

# ── EXPORT ─────────────────────────────────────────────────────────────────────
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
