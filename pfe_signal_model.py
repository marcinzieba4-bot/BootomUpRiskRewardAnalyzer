"""
PFE  ·  Pfizer Inc.  ·  NYSE: PFE
Bottom-up signal model  ·  Pharmaceuticals / Oncology (Seagen ADCs) / LOE Cliff / Obesity Pipeline
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "PFE"
COMPANY       = "Pfizer Inc."
SECTOR        = "Pharmaceuticals · Oncology (Seagen ADCs) · Vaccines · Obesity Pipeline · NYSE: PFE"
CURRENT_PRICE = 25.03       # USD; close 2026-08-03. NOTE: Q2 2026 earnings report is due AFTER this close,
                             # on 2026-08-04 — this model is built on the last confirmed data (Q1 actual + FY guide)
VOL_52W_LOW   = 23.40       # 2025/26 trough
VOL_52W_HIGH  = 28.75       # 2026 peak
SHARES_OUT_M  = 5_726.0     # millions; ~$143.3B mkt cap / $25.03
ANNUAL_DIV    = 1.71        # $/share; ~6.8% yield, among the highest in large-cap pharma

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ──────────────────────────────────────
# Q1 2026 actual: adj EPS $0.75 (beat $0.72 est), revenue $14.5B (beat $13.84B est); reported GAAP
# diluted EPS $0.47 (-10% YoY). Eliquis $2.17B (+13% YoY, beat $1.96B est), Ibrance $1.0B (-1%, beat
# $944M est), Vyndaqel family $1.6B (+4%, slight miss vs $1.66B est), Padcev $591M (+39%, beat $542M
# est). FY2026 guidance reaffirmed: revenue $59.5-62.5B, adj EPS $2.80-$3.00. COVID franchise
# (Comirnaty+Paxlovid) guided to just $5B, down from $6.5B — a deliberate de-risking. Q2 2026 consensus
# (not yet reported as of this model): EPS $0.68, revenue ~$14.4B, expected -1.7% YoY on a tough comp.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Non-COVID growth portfolio (Eliquis/Vyndaqel/Padcev/Oncology/Vaccines)", 56.0, 48.0, 63.0, "The core franchise; Eliquis and Ibrance both face LOE (loss of exclusivity) risk over the model horizon"),
    ("COVID franchise (Comirnaty + Paxlovid)",                                  5.0,  2.5,  6.5, "Deliberately de-risked to $5B for FY2026 (from $6.5B) — management is guiding conservatively, not optimistically"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.700   # FY2026E blended gross margin
GROSS_MARGIN_BEAR = 0.660   # BEAR: LOE-driven mix deterioration plus continued COVID franchise erosion
GROSS_MARGIN_BULL = 0.715   # BULL: oncology/specialty mix improves as Seagen ADCs and newer launches scale
OPEX_FIXED_B      = 23.17   # R&D + SG&A + net interest ($B) — includes Seagen-acquisition-related debt service, largely sticky
TAX_RATE          = 0.150   # effective tax rate

# ── LOE PATENT CLIFF CALCULATOR (the Pfizer-specific angle) ──────────────────
ELIQUIS_Q1_REV_B       = 2.17   # $B; Eliquis Q1 2026 revenue, +13% YoY
IBRANCE_Q1_REV_B       = 1.00   # $B; Ibrance Q1 2026 revenue, -1% YoY (already past peak)
VYNDAQEL_Q1_REV_B      = 1.60   # $B; Vyndaqel family Q1 2026 revenue, +4% YoY
PADCEV_Q1_REV_B        = 0.591  # $B; Padcev (Seagen ADC) Q1 2026 revenue, +39% YoY — the fastest grower of the group
COVID_GUIDE_FY26_B     = 5.0    # $B; FY2026 COVID franchise guide (down from $6.5B — a deliberate de-risking)
Q2_CONSENSUS_EPS       = 0.68   # $/share; Street consensus for the Q2 2026 print (not yet reported)
Q2_CONSENSUS_REV_B     = 14.4   # $B; Street consensus revenue for Q2 2026

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 2.90        # $/share FY2026E adj; guide midpoint ($2.80-$3.00)
PE_PESSIMISTIC = 8.0         # trough P/E: matches the stock's own current depressed multiple — already near a distress level
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  (1.44, 8,  11.5, "Eliquis/Ibrance LOE erosion accelerates faster than guided and the COVID franchise keeps shrinking toward zero"),
    "BASE":  (2.96, 10, 30,   "Revenue holds roughly flat as LOE erosion is offset by oncology (Padcev) and vaccine growth, per the reaffirmed guide"),
    "BULL":  (3.92, 10, 39,   "Oncology (Seagen ADC) growth and cost discipline outrun the LOE cliff; obesity pipeline delivers a positive Phase III readout"),
    "XBULL": (4.95, 12, 59,   "The obesity franchise becomes a genuine blockbuster and the multiple re-rates back toward historical large-pharma norms"),
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
        "name":       "Padcev (Seagen ADC) growth",
        "weight":     0.20,
        "thresholds": ("<10%",   "≥20%",   "≥30%",   "≥40%"),
        "now":        "+39%",
        "score":      3,
        "comment":    "The clearest evidence the Seagen acquisition is working — oncology ADCs are genuinely offsetting cliff risk",
    },
    {
        "name":       "Eliquis growth",
        "weight":     0.15,
        "thresholds": ("<0%",    "≥5%",    "≥10%",   "≥15%"),
        "now":        "+13%",
        "score":      3,
        "comment":    "Still growing double-digits even as LOE risk looms — the cliff hasn't hit the P&L yet",
    },
    {
        "name":       "Ibrance growth",
        "weight":     0.10,
        "thresholds": ("<-10%",  "≥-3%",   "≥0%",    "≥5%"),
        "now":        "-1%",
        "score":      2,
        "comment":    "Roughly flat but past its growth peak — the first LOE-adjacent product showing real deceleration",
    },
    {
        "name":       "COVID franchise guidance stance",
        "weight":     0.15,
        "thresholds": ("raised", "held",   "de-risked","conservative"),
        "now":        "de-risked",
        "score":      3,
        "comment":    "Guided down to $5B from $6.5B — management pre-emptively lowering the bar rather than getting surprised later",
    },
    {
        "name":       "Q1 2026 beat magnitude",
        "weight":     0.20,
        "thresholds": ("miss",   "in-line", "beat",  "large beat"),
        "now":        "large beat",
        "score":      4,
        "comment":    "Adj EPS $0.75 vs $0.72 est, revenue $14.5B vs $13.84B est — a genuine, broad-based beat",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.20,
        "thresholds": (">14x",   "≤11x",   "≤9x",    "≤7x"),
        "now":        "~8.6x",
        "score":      3,
        "comment":    "8.6× FY2026E adj EPS — cheapest among large-cap pharma, reflecting real but arguably overdone LOE-cliff fear",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "The ~6.8% dividend yield is among the highest in large-cap pharma and provides real downside cushion while the LOE story plays out", +0.5, 0.20),
    ("-", "Eliquis (2026) and Ibrance (2027) LOE risk together represents $17-18B+ of revenue at risk — a real, quantified structural headwind", -0.6, 0.25),
    ("+", "Padcev's +39% growth and the broader Seagen ADC platform are genuine, quantified evidence the oncology pivot is working, not just a promise", +0.5, 0.20),
    ("-", "Post-COVID normalization means the earnings base itself is smaller and more exposed to any single franchise's underperformance", -0.3, 0.15),
    ("+", "$4B+ in committed cost cuts by 2027 gives management a real, controllable lever independent of pipeline outcomes", +0.4, 0.10),
    ("-", "Obesity pipeline (PF'3944 and successors) remains Phase II/III — genuine optionality, but not yet proven or de-risked", -0.3, 0.10),
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
CONS_EPS_2YR  = 3.00    # conservative FY2028E: modest growth off FY2026E guide midpoint
CONS_PE_2YR   = 9       # a modest re-rating from ~8.6× as LOE fear proves partly overdone
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Oncology ADCs / LOE Cliff / Obesity Pipeline")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))
print(f"  NOTE: Q2 2026 earnings report on 2026-08-04 (after this model's price date). Built on the last")
print(f"  confirmed data — Q1 2026 actuals + reaffirmed FY2026 guidance. Street Q2 consensus: EPS ${Q2_CONSENSUS_EPS:.2f}, revenue ${Q2_CONSENSUS_REV_B:.1f}B.")

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<52}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<52}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<52}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}")
print(f"  FY2026 guide: revenue $59.5-62.5B (midpoint ${curr_total:.1f}B), adj EPS $2.80-$3.00")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_eps  = round(curr_oi * (1 - TAX_RATE) / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B * 1.05
shares_b  = shares * 0.96
bull_eps_imp = round(bull_oi * (1 - TAX_RATE) / shares_b, 2)

bear_gp   = bear_total * GROSS_MARGIN_BEAR
bear_oi   = bear_gp - OPEX_FIXED_B * 1.02
bear_eps_imp = round(max(0, bear_oi) * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.2f}B opex")
print(f"  − {TAX_RATE*100:.1f}% tax  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − opex, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_BEAR*100:.1f}% GM (accelerated LOE erosion + COVID falloff) − opex")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.1f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# LOE PATENT CLIFF CHECK
print()
print(f"  LOE PATENT CLIFF CHECK  (the Pfizer-specific angle):")
print(f"  Eliquis (Q1 2026):     ${ELIQUIS_Q1_REV_B}B  (+13% YoY) — LOE risk begins 2026")
print(f"  Ibrance (Q1 2026):     ${IBRANCE_Q1_REV_B:.2f}B  (-1% YoY) — LOE risk begins 2027")
print(f"  Vyndaqel (Q1 2026):    ${VYNDAQEL_Q1_REV_B}B  (+4% YoY)")
print(f"  Padcev (Q1 2026):      ${PADCEV_Q1_REV_B:.3f}B  (+39% YoY) — the fastest grower, offsetting cliff risk")
print(f"  COVID FY2026 guide:    ${COVID_GUIDE_FY26_B}B  (de-risked down from $6.5B)")
print()
print(f"  The LOE cliff (Eliquis 2026, Ibrance 2027) puts an estimated $17-18B of revenue at risk by 2028 —")
print(f"  a real, quantified structural headwind. The counter-evidence is equally real: Padcev's +39% growth")
print(f"  shows the Seagen ADC platform is a genuine offset, not just a hoped-for one, and management is")
print(f"  de-risking COVID guidance proactively rather than getting caught by a surprise miss.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_gm  = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 70.0% GM):      +${eps_per_1B_rev:.4f}/EPS  = +${eps_per_1B_rev*10:.2f}/share at 10× P/E")
print(f"  Every 1pp of gross margin:            +${eps_per_1pp_gm:.4f}/EPS  = +${eps_per_1pp_gm*10:.2f}/share at 10× P/E")
print(f"  Every 1 turn of P/E:                  ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Padcev growth / Eliquis / Ibrance / COVID guide / Q1 beat / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<34}  {'BEAR':>9}  {'BASE':>7}  {'BULL':>9}  {'XBULL':>13}  {'NOW':>13}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<34}  {ths[0]:>9}  {ths[1]:>7}  {ths[2]:>9}  {ths[3]:>13}  {s['now']:>13}  {lbl}  {b}")
    print(f"    {s['comment']}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15%/yr hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:88]:<88}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<32}  {'Current':>10}  {'Bear val':>10}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Padcev growth",               "+39%",   "<10%",    "-29pp+", "Competitive ADC entrants or safety signals slow the fastest-growing offset to the LOE cliff"),
    ("Eliquis growth",               "+13%",   "<0%",    "reversal","Generic/biosimilar-equivalent competition hits earlier or harder than the 2026 LOE timeline suggests"),
    ("Ibrance growth",               "-1%",    "<-10%",  "-9pp+",  "CDK4/6 inhibitor competition accelerates the decline beyond the already-negative trend"),
    ("COVID franchise guidance",     "de-risked","cut further","worse","Even the $5B de-risked guide proves too optimistic as COVID relevance keeps fading"),
    ("Q1 2026 beat magnitude",       "large beat","miss",  "reversal","A beat-and-raise-adjacent quarter gives way to a genuine guidance miss"),
    ("Forward P/E",                  "~8.6x",  ">14x",    "re-rate","Ironically, P/E can rise even as price falls if EPS collapses faster than price does"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the bear case requires the LOE cliff to hit faster than the Seagen ADC platform and")
print(f"  cost cuts can offset it — plausible, but not yet supported by the data. Q2 earnings (reported the")
print(f"  day after this model's price date) are the immediate next test of whether Q1's broad-based beat")
print(f"  was a trend or a single good quarter.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS estimate:       ${EPS_FY2026E:.2f}  (guide midpoint, $2.80-$3.00)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (matches the stock's own current multiple — already near a distress level)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.1f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.1f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS — near its own trough multiple already,")
print(f"  meaning the EPP floor and the current price sit close together. This is a name priced for the LOE")
print(f"  cliff fear to be roughly correct, not for it to be overdone.")
print(f"  At a 10× reversion (still a below-average pharma multiple): ${EPS_FY2026E:.2f} × 10 = ${EPS_FY2026E*10:.0f}  ({(EPS_FY2026E*10/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest growth off FY2026E guide midpoint)")
hr()
print(f"  Conservative FY2028E EPS:  ${CONS_EPS_2YR:.2f}  (~3.4% cumulative EPS growth — a genuinely conservative assumption)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~8.6× → 9×; a modest re-rating, not a re-rating to a growth multiple)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: the ~6.8% dividend yield alone does most of the work in a conservative scenario —")
print(f"  even flat-to-modest EPS growth and only a small multiple re-rating produces a {'solidly positive' if cons_return > 15 else 'positive' if cons_return > 0 else 'negative'} total return.")
print(f"  This is a name where the dividend is the margin of safety, not the earnings growth story.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.22
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 1),
               round(CURRENT_PRICE * (1 + annual_vol), 1))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Next catalyst:         Q2 2026 earnings, reported 2026-08-04 (the day after this model's price date)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; among the highest in large-cap pharma)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (low-moderate — a mature, dividend-heavy large pharma name)")
print(f"  Beta vs S&P 500:      0.55  (defensive, well below market)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.1f}  –  ${sigma_range[1]:.1f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (large relative to Pfizer's typically low realized vol)")
print(f"  → Q2 2026 print (Aug 4, the day after this price date) is the immediate next catalyst.")
print(f"  → Eliquis/Ibrance prescription-trend data and obesity-pipeline readouts are the leading indicators.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add on weakness $22-24  |  Trim above $29")

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
print(f"  Adj EV (2yr): ${ev_adj:.1f}  /  Proxy EV: ${ev_prx:.1f}  /  Market EV: ${ev_mkt:.1f}  /  Current: ${CURRENT_PRICE:.1f}")
hr()
print(f"  Downside  (→ Bear ${bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull ${bull_price}):  {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b_str}")
print(f"  Signal    :  {signal_full}")
print()
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f} the market composite is {MARKET_COMPOSITE:.2f}/4.0. The model's")
print(f"  adjusted composite is {ADJ_COMPOSITE:.2f}/4.0, for a gap of {ADJ_GAP:+.2f} — {valuation_label.lower()}.")
print(f"  Pfizer is genuinely cheap by conventional metrics, and Padcev's growth is real evidence the Seagen")
print(f"  pivot is working — but this remains a name where the LOE cliff risk is large enough that Q2 earnings")
print(f"  (reported the day after this model's price date) matter more than usual for confirming the thesis.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q2 2026 earnings (Aug 4, the day after this model's price date) — confirm Q1's broad-based beat was a trend")
print(f"  (2) Eliquis/Ibrance prescription-trend data — the leading indicator for how fast the LOE cliff actually bites")
print(f"  (3) Obesity pipeline (PF'3944 and successors) — Phase III readouts through 2026")
print(f"  (4) Progress on the $4B+ cost-cutting program toward its 2027 target")
print(f"  (5) COVID franchise trends versus the de-risked $5B guide — upside surprise potential if it holds up")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add on weakness $22-24  |  Trim above $29")
print(f"  EPP floor: ${EPP:.1f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  Dividend yield: {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%")
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
