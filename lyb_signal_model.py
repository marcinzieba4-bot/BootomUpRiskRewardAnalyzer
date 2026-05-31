"""
LYB  ·  LyondellBasell Industries N.V.  ·  NYSE: LYB
Bottom-up signal model  ·  Polypropylene / Polyethylene / PO / Technology Licensing
Date: 2026-05-31

EPS is severely compressed at trough; model uses EV/EBITDA framework for EPP and scenarios.
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "LYB"
COMPANY       = "LyondellBasell Industries N.V."
SECTOR        = "Commodity Chemicals · Polypropylene · PO/Styrene · Technology Licensing · NYSE: LYB"
CURRENT_PRICE = 72.50        # USD; as of 2026-05-31
VOL_52W_LOW   = 53.80        # Oct 2025 trough (dividend sustainability concerns)
VOL_52W_HIGH  = 97.20        # Jun 2025 high (raw material tailwind + Houston refinery exit)
SHARES_OUT_M  = 310.0        # millions (post-buyback)

ANNUAL_DIV    = 4.52         # $/share — maintained through cycle (management commitment)
TOTAL_DIV_B   = ANNUAL_DIV * SHARES_OUT_M / 1000   # ~$1.40B/yr annual dividend burden

# ── EV/EBITDA FRAMEWORK ───────────────────────────────────────────────────────
# EPS severely compressed at trough; standard P/E EPP inapplicable
NET_DEBT_B       = 8.8       # $B net debt (post-Houston-refinery closure proceeds)
DA_B             = 0.80      # $B D&A (depreciation & amortisation)
INTEREST_B       = 0.45      # $B annual interest expense
CAPEX_MAINT_B    = 0.90      # $B maintenance capex (post-Houston)
TAX_RATE         = 0.23

# Dividend sustainability table constants
EBITDA_STAGES = [
    ("Trough (FY2025 actual)",          2.7,  5.5, "PP spread compression + China glut + European weakness"),
    ("Dividend breakeven (2yr base)",   3.5,  6.0, "VEP savings + Houston exit; FCF just covers dividend"),
    ("Consensus BASE mid-cycle",        4.0,  6.5, "PP/PE spreads normalise; European manufacturing recovers"),
    ("VEP full delivery target",        4.5,  6.5, "$600M VEP target achieved; spread recovery underway"),
    ("BULL — spread + Europe recovery", 5.5,  7.0, "PP/PE spreads to 2019 levels; China capacity additions peak"),
    ("XBULL — near-peak cycle",         7.0,  7.5, "Full cycle recovery; tech licensing re-rating; China stabilises"),
]

vol_pct = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)

# EPP (EV/EBITDA trough equity floor)
TROUGH_EBITDA_B  = 2.7    # FY2025 trough
MIN_EV_EBITDA    = 5.5    # distress multiple for leveraged commodity chem
trough_ev_b      = TROUGH_EBITDA_B * MIN_EV_EBITDA
trough_equity_b  = max(trough_ev_b - NET_DEBT_B, 0.5)   # floor at $0.5B (tech license value)
EPP              = round(trough_equity_b / SHARES_OUT_M * 1000, 1)   # $/share
epp_gap_pct      = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
# EPS/PE placeholders 0 (EV/EBITDA drives prices); prices from EV-equity bridge
SCENARIOS = {
    "BEAR":  (0.00, 0,  25,  "PP/PO collapse + China glut surge; EBITDA $1.5B; dividend cut; distress discount"),
    "BASE":  (0.00, 0,  60,  "EBITDA $4.0B × 6.5× EV → equity $17.5B → $57/shr; some deleveraging"),
    "BULL":  (0.00, 0, 105,  "EBITDA $5.5B × 7.0× EV → equity $30B → $96/shr + liquidity re-rating"),
    "XBULL": (0.00, 0, 155,  "EBITDA $7.0B × 7.5× EV → equity $44B → $142/shr; tech licensing premium"),
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

def back_solve_market_composite(price):
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
SIGNALS = [
    {
        "name":       "PP–propylene integrated spread — global blended ($/MT)",
        "weight":     0.25,
        "thresholds": ("<$120",  "≥$135",  "≥$200",   "≥$300"),
        "now":        "$145",
        "score":      2,
        "comment":    "US PDH at $210/MT offset by Asia <$80/MT; blended ~$145; recovering but below BASE threshold",
    },
    {
        "name":       "China polypropylene net capacity additions (MT/yr)",
        "weight":     0.20,
        "thresholds": (">4MT",   "2–4MT",  "0–2MT",   "<0MT"),
        "now":        "~3MT",
        "score":      2,
        "comment":    "Chinese additions slowing (poor project economics) but still ~3MT/yr net; remains headwind",
    },
    {
        "name":       "European industrial output YoY (Ger + NL + Italy weighted)",
        "weight":     0.20,
        "thresholds": ("<−3%",   "≥0%",    "≥2.5%",   "≥5%"),
        "now":        "+0.5%",
        "score":      2,
        "comment":    "German PMI 48→49; ECB rate cuts transmitting; manufacturing barely positive YoY; fragile",
    },
    {
        "name":       "Propylene Oxide margin over propylene ($/MT) — POSM process",
        "weight":     0.15,
        "thresholds": ("<$180",  "≥$230",  "≥$320",   "≥$420"),
        "now":        "$265",
        "score":      2,
        "comment":    "PO demand steady (polyurethane foam, construction); $265/MT; below BULL threshold at $320",
    },
    {
        "name":       "Value Enhancement Programme + Houston exit — annualised savings ($M)",
        "weight":     0.15,
        "thresholds": ("<$200M", "≥$300M", "≥$450M",  "≥$650M"),
        "now":        "$430M",
        "score":      3,
        "comment":    "Houston refinery closed (saves ~$250M losses/yr); VEP programme $430M of $600M target",
    },
    {
        "name":       "Technology licensing revenue ($M annual — Spherizone, Lupotech)",
        "weight":     0.05,
        "thresholds": ("<$400M", "≥$450M", "≥$550M",  "≥$650M"),
        "now":        "$505M",
        "score":      3,
        "comment":    "$505M licensing rev (+5% YoY); ~50% margin; 200+ plants licensed globally; growing",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Technology licensing moat — Spherizone/Lupotech IP; 200+ global plants; 40yr track record", +0.8, 0.20),
    ("+", "US propane feedstock advantage — PDH plants; cheap US propane vs naphtha crackers in Europe",  +0.5, 0.10),
    ("-", "China structural PP/PE overcapacity — 3-5MT/yr additions; structural 20yr ceiling on spreads", -0.8, 0.25),
    ("-", "Leverage + dividend risk — $8.8B net debt; FCF <$1.4B dividend at trough EBITDA <$3.5B",      -0.6, 0.20),
    ("-", "European deindustrialisation — German auto crisis; structural energy cost disadvantage vs US",  -0.4, 0.15),
    ("+", "Circularity/recycling optionality — MoReTec molecular recycling; EU regulatory tailwind",      +0.3, 0.10),
]
assert abs(sum(w for _, _, _, w in SCA_FACTORS) - 1.0) < 0.001
SCA = sum(score * weight for _, _, score, weight in SCA_FACTORS)

ADJ_COMPOSITE    = round(PROXY_COMPOSITE + SCA, 3)
MARKET_COMPOSITE = back_solve_market_composite(CURRENT_PRICE)
ADJ_GAP          = round(ADJ_COMPOSITE - MARKET_COMPOSITE, 2)

if ADJ_GAP > 0.20:
    valuation_label = "UNDERVALUED"
elif ADJ_GAP > -0.20:
    valuation_label = "FAIRLY VALUED"
elif ADJ_GAP > -0.60:
    valuation_label = "MODESTLY OVERVALUED"
else:
    valuation_label = "OVERVALUED"

# ── RATIO B (signal) ──────────────────────────────────────────────────────────
bear_price   = SCENARIOS["BEAR"][2]
bull_price   = SCENARIOS["BULL"][2]
downside_pct = (CURRENT_PRICE - bear_price) / CURRENT_PRICE
upside_pct   = (bull_price   - CURRENT_PRICE) / CURRENT_PRICE
ratio_b      = round(downside_pct / upside_pct, 2)

if ratio_b < 0.75:    signal_short, signal_full = "BUY",       "◉ BUY"
elif ratio_b < 1.10:  signal_short, signal_full = "ACCUMULATE","◎ ACCUMULATE"
elif ratio_b < 1.75:  signal_short, signal_full = "WATCHLIST", "◐ WATCHLIST"
else:                 signal_short, signal_full = "AVOID",     "✕ AVOID"

# ── CONSERVATIVE GROWTH (2-yr) ────────────────────────────────────────────────
CONS_EBITDA_B    = 3.5    # $B: VEP savings offset by slow spread recovery
CONS_EV_EBITDA   = 6.0    # cautious multiple; below mid-cycle average
CONS_NET_DEBT_2Y = 8.3    # $B: FCF barely covers dividend; minimal deleveraging
cons_ev_b        = CONS_EBITDA_B * CONS_EV_EBITDA
cons_equity_b    = cons_ev_b - CONS_NET_DEBT_2Y
cons_price_eq    = cons_equity_b / SHARES_OUT_M * 1000
cons_divs        = ANNUAL_DIV * 2
cons_total       = cons_price_eq + cons_divs
cons_return      = round((cons_total - CURRENT_PRICE) / CURRENT_PRICE * 100, 1)
cons_annual      = round(cons_return / 2, 1)

# ── FCF bridge helper ─────────────────────────────────────────────────────────
def fcf_at_ebitda(ebitda_b):
    ebit      = ebitda_b - DA_B
    pretax    = ebit - INTEREST_B
    net_inc   = pretax * (1 - TAX_RATE)
    op_cf     = net_inc + DA_B
    fcf       = op_cf - CAPEX_MAINT_B
    return fcf

# ─────────────────────────────────────────────────────────────────────────────
#  OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
W = 72

def hr(): print("  " + "─" * W)

print()
print("═" * (W + 4))
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Commodity Chemicals / Basic Resources")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① DIVIDEND COVERAGE & FCF SUSTAINABILITY ─────────────────────────────────
print()
print("  DIVIDEND COVERAGE & FCF SUSTAINABILITY  (EV/EBITDA framework; adj EPS compressed at trough)")
hr()
print(f"  Annual dividend: ${ANNUAL_DIV:.2f}/share × {SHARES_OUT_M:.0f}M shares = ${TOTAL_DIV_B:.2f}B/yr total dividend burden")
print(f"  FCF = (EBITDA − D&A ${DA_B:.2f}B − interest ${INTEREST_B:.2f}B) × {(1-TAX_RATE)*100:.0f}% + D&A − capex ${CAPEX_MAINT_B:.2f}B")
print()
print(f"  {'Scenario':<38}  {'EBITDA':>7}  {'EV/E':>5}  {'EV ($B)':>8}  {'Eq/shr':>8}  {'FCF($B)':>8}  {'Div cov':>8}")
hr()
for label, ebitda, ev_mult, note in EBITDA_STAGES:
    ev_b     = ebitda * ev_mult
    eq_b     = max(ev_b - NET_DEBT_B, 0.0)
    eq_shr   = eq_b / SHARES_OUT_M * 1000
    fcf      = fcf_at_ebitda(ebitda)
    div_cov  = fcf / TOTAL_DIV_B
    marker   = " ◄ CURRENT" if abs(ebitda - 2.7) < 0.1 else ""
    cov_flag = "⚠ DEFICIT" if div_cov < 1.0 else ("✓ COVERED" if div_cov >= 1.3 else "~ TIGHT")
    print(f"  {label:<38}  ${ebitda:.1f}B  {ev_mult:.1f}×  ${ev_b:.1f}B    ${eq_shr:>5.0f}/shr  ${fcf:.2f}B    {div_cov:.2f}×  {cov_flag}{marker}")
hr()
breakeven_ebitda = 3.5   # EBITDA where FCF = dividend
print(f"  Dividend breakeven EBITDA: ~$3.5B  (FCF = ${TOTAL_DIV_B:.2f}B dividend at ${CAPEX_MAINT_B:.2f}B capex)")
print(f"  Current trough $2.7B → FCF deficit ~${TOTAL_DIV_B - fcf_at_ebitda(2.7):.2f}B/yr → dividend is being PARTIALLY FUNDED BY DEBT")
print(f"  Tech licensing floor: ${505:.0f}M rev × ~50% margin = ~$250M EBITDA contribution (structural; won't go to 0)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (adj EPS negative / near-zero at trough; EBITDA/cycle framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
def bar(s): return "█" * s + "░" * (4 - s)
print(f"  {'Signal':<54}  {'BEAR':>5}  {'BASE':>6}  {'BULL':>7}  {'XBULL':>8}  {'NOW':>6}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<54}  {ths[0]:>5}  {ths[1]:>6}  {ths[2]:>7}  {ths[3]:>8}  {s['now']:>6}  {lbl}  {b}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15% hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.2f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contr = score * weight
    print(f"    {sign}  {desc[:74]:<74}  ({score:+.1f} × {weight*100:.0f}%  =  {contr:+.2f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<54}  {'Current':>7}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("PP–propylene spread ($/MT)",                    "$145",  "<$120",   "−$25",    "Global recession; US tariffs redirect US PP…"),
    ("China PP capacity additions (MT/yr)",           "~3MT",  ">4MT",    "+1MT",    "New Chinese PP complexes commissioned despit…"),
    ("European industrial output YoY",                "+0.5%", "<−3%",    "−3.5pp",  "German auto crisis deepens; France contracts…"),
    ("Propylene Oxide margin ($/MT)",                 "$265",  "<$180",   "−$85",    "PO oversupply; POSM plant economics collapse…"),
    ("VEP + Houston savings ($M annualised)",         "$430M", "<$200M",  "−$230M",  "Programme reversal; VEP targets scrapped; Ho…"),
    ("Technology licensing revenue ($M)",             "$505M", "<$400M",  "−$105M",  "New competing PP technology (INEOS Innovene…"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<54}  {curr:>7}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Global manufacturing recession collapses PP/PE demand simultaneously with")
print(f"  Chinese capacity surge. EBITDA falls to $1.5B; FCF turns sharply negative; dividend cut")
print(f"  announced (50%+ reduction). With $8.8B net debt and negative equity at 5× EV/EBITDA,")
print(f"  market prices distress discount → stock re-tests $25 or below (2009 analogue).")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (EV/EBITDA based — adj EPS compressed at trough; floor = trough asset value)")
hr()
print(f"  Trough EBITDA (FY2025 actual):    ${TROUGH_EBITDA_B:.1f}B")
print(f"  Min viable EV/EBITDA at distress:  {MIN_EV_EBITDA:.1f}×")
print(f"  Trough EV:                         ${trough_ev_b:.2f}B")
print(f"  Less: net debt ${NET_DEBT_B:.1f}B  →  trough equity ${trough_equity_b:.2f}B")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor (trough EBITDA ${TROUGH_EBITDA_B:.1f}B × {MIN_EV_EBITDA:.1f}× EV/EBITDA less ${NET_DEBT_B:.1f}B net debt):")
print(f"    = ${EPP:.1f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.1f}:   +{epp_gap_pct:.0f}%  (← market pricing WELL ABOVE trough; recovery embedded)")
print(f"  Bear ${bear_price} vs EPP ${EPP:.1f}:    +{(bear_price-EPP)/EPP*100:.0f}%  ← BEAR still above EPP (dividend cut prevents distress)")
print()
print(f"  The +{epp_gap_pct:.0f}% premium to trough EPP = ~${(CURRENT_PRICE-EPP):.0f}/share of recovery value.")
print(f"  Full mid-cycle ($4.0B × 6.5×) implies $57/share — BELOW current price of ${CURRENT_PRICE:.2f}.")
print(f"  Only BULL ($5.5B × 7×) and XBULL scenarios justify current price. That is the risk.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: partial VEP delivery; spreads recovering slowly)")
hr()
print(f"  Conservative 2yr EBITDA:   ${CONS_EBITDA_B:.1f}B  (VEP $430M + Houston closure; spread recovery sluggish)")
print(f"  Exit EV/EBITDA:             {CONS_EV_EBITDA:.1f}×  (cautious; below historical avg ~7×)")
print(f"  Implied EV:                ${cons_ev_b:.1f}B")
print(f"  Less: net debt in 2yr (${CONS_NET_DEBT_2Y:.1f}B):  minimal deleveraging (FCF ≈ dividend)")
print(f"  Implied equity value:       ${cons_equity_b:.1f}B  =  ${cons_price_eq:.1f}/share")
print(f"  + Cumulative dividends:    +${cons_divs:.2f}/share  (2yr × ${ANNUAL_DIV:.2f}; assuming no cut)")
hr()
print(f"  Conservative 2yr total:     ${cons_total:.1f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.1f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:  {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is SIGNIFICANTLY NEGATIVE — BASE scenario (${SCENARIOS['BASE'][2]}) is already below")
print(f"  current price. Dividend yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}% is attractive but requires EBITDA >$3.5B to cover.")
print(f"  Breakeven total return: EBITDA ≥$4.0B at {CONS_EV_EBITDA:.1f}× = ${60:.0f}/shr + ${cons_divs:.2f} div = ${60+cons_divs:.2f}; still below ${CURRENT_PRICE:.2f}.")
print(f"  ONLY BULL ($5.5B EBITDA → ${SCENARIOS['BULL'][2]}) generates a positive 2yr total return from current levels.")
print(f"  Better entry: ${VOL_52W_LOW+2:.0f}–65 range where BASE scenario generates +10-25% total return including dividend.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.35
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol)), round(CURRENT_PRICE * (1 + annual_vol)))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct; below 2025 high)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%  —  management committed but FCF-constrained)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (high; commodity cycle + China sensitivity + leverage)")
print(f"  Beta vs S&P 500:      1.05  (above market; high operating + financial leverage)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]}  –  ${sigma_range[1]}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (achievable — 52W low ${VOL_52W_LOW:.2f} was only {(CURRENT_PRICE-VOL_52W_LOW)/(CURRENT_PRICE*annual_vol):.1f}σ)")
print(f"  → Dividend yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}% attractive but NOT safe if EBITDA stays <$3.5B.")
print(f"  → Leverage (net debt/EBITDA {NET_DEBT_B/TROUGH_EBITDA_B:.1f}× at trough) is the key amplifier in downside.")
print(f"  → WATCHLIST range: ${VOL_52W_HIGH-35:.0f}–{VOL_52W_HIGH:.0f}  |  ACCUMULATE $58–67  |  BUY below ${int(EPP*2.8):.0f}  |  AVOID above $85")

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
    desc = SCENARIOS[s][3][:48]
    print(f"  {s:<10}  ${pr:>6}  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): ${ev_adj:.0f}  /  Proxy EV: ${ev_prx:.0f}  /  Market EV: ${ev_mkt:.0f}  /  Current: ${CURRENT_PRICE:.0f}")
hr()
print(f"  Downside  (→ Bear ${bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull ${bull_price}):   {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b:.2f}x")
print(f"  Signal    :  {signal_full}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) PP-propylene spread recovery → $200/MT = BULL threshold for margin re-rating")
print(f"  (2) China capacity slow-down confirmation (new plant cancellations; poor project economics)")
print(f"  (3) Q2/Q3 2026 EBITDA trajectory → $3.5B run-rate = dividend coverage; $4B+ = ACCUMULATE upgrade")
print(f"  (4) VEP $600M full delivery announcement + next cost programme (LYB pattern: always has one)")
print(f"  WATCHLIST ${VOL_52W_HIGH-35:.0f}–85  |  ACCUMULATE $58–67  |  BUY below $55  |  Size small — dividend at risk below $3.5B EBITDA")
print("═" * (W + 4))
print()

RESULT = {
    "ticker":            TICKER,
    "signal":            signal_full,
    "signal_short":      signal_short,
    "price":             CURRENT_PRICE,
    "epp_gap_pct":       epp_gap_pct,
    "ratio_b":           ratio_b,
    "ratio_b_fmt":       f"{ratio_b:.2f}x",
    "adj_composite":     ADJ_COMPOSITE,
    "market_composite":  MARKET_COMPOSITE,
    "adj_gap":           ADJ_GAP,
    "valuation":         valuation_label,
    "cons_return_2yr":   cons_return,
}

if __name__ == "__main__":
    pass
