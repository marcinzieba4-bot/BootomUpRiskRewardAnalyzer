"""
PLTR  ·  Palantir Technologies Inc.  ·  NASDAQ: PLTR
Bottom-up signal model  ·  Government AI OS / Commercial AIP / Big Data Analytics
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "PLTR"
COMPANY       = "Palantir Technologies Inc."
SECTOR        = "Government AI OS · Commercial AIP · Big Data Analytics · NASDAQ: PLTR"
CURRENT_PRICE = 123.06       # USD; close 2026-07-31 (verified live), day before Q2 print
VOL_52W_LOW   = 106.37       # 2026 trough — already a ~91x forward-EPS floor
VOL_52W_HIGH  = 207.52       # 2026 AI-mania peak
SHARES_OUT_M  = 2_400.0      # millions; $295.0B mkt cap / $123.06
ANNUAL_DIV    = 0.0          # $/share; no dividend

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ──────────────────────────────────────
# Q1 2026 actual: revenue $1.633B (+85% YoY); US commercial $595M (+133%), US
# gov $687M (+84%), international $351M. FY2026 guide: $7.65-7.662B (+71% YoY)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("US Commercial (AIP)",           2.90, 2.30,  5.50, "+133% YoY in Q1; the swing factor — AIP bootcamp-to-contract conversion pace"),
    ("US Government",                 3.00, 2.60,  4.20, "+84% YoY; Maven, defense, and intelligence-community expansion; steadier than commercial"),
    ("International (Comm. + Gov.)",  1.75, 1.40,  3.00, "NATO/allied government expansion + international commercial; the smallest, most optional piece"),
]

# Margin assumptions (adjusted, per Palantir's own disclosure convention)
OP_MARGIN_CURR   = 0.377    # FY2026E blended adjusted operating margin proxy; Q1 adj op margin was 60%, seasonally strong
OP_MARGIN_BULL   = 0.604    # BULL: margin holds near Q1's 60% as commercial scales with operating leverage
OP_MARGIN_BEAR   = 0.300    # BEAR: heavy S&M/R&D spend persists while growth decelerates, compressing the margin
TAX_RATE         = 0.210    # effective tax rate now that Palantir is consistently GAAP-profitable

# ── RULE OF 40 / GROWTH QUALITY CALCULATOR (the Palantir-specific angle) ─────
RULE_OF_40_SCORE     = 145   # revenue growth % + margin %, Q1 2026 — matched only by NVDA/MU/SK hynix per mgmt
US_COMMERCIAL_GROWTH = 133   # % YoY, Q1 2026
US_GOV_GROWTH        =  84   # % YoY, Q1 2026
US_TOTAL_GROWTH      = 104   # % YoY, Q1 2026
Q2_REPORT_DATE        = "2026-08-03"  # reports AFTER THE CLOSE on the same day as this refresh
Q2_CONSENSUS_REV_B    = 1.812  # $B consensus Q2 2026 revenue
Q2_CONSENSUS_EPS      = 0.34   # $ consensus Q2 2026 non-GAAP EPS

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 0.95        # $/share GAAP-basis FY2026E estimate, built bottom-up off the raised revenue guide
PE_PESSIMISTIC = 45.0        # trough P/E: even PLTR's 52-week low implies ~90x+ forward earnings; 45x
                              # prices a genuine multiple reset, not a return to a "normal" software multiple
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 0.62, 45,   28, "Commercial AIP growth decelerates sharply; government budget scrutiny bites; multiple resets hard"),
    "BASE":  ( 1.35, 70,   95, "Growth normalizes toward a still-strong 25-35%/yr; multiple compresses from today's extreme level"),
    "BULL":  ( 2.55, 75,  191, "Rule-of-40 economics persist near 100+; commercial AIP conversion keeps compounding at scale"),
    "XBULL": ( 3.30, 95,  314, "Palantir becomes the default enterprise/government AI operating system; growth AND multiple both hold"),
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
        "name":       "US Commercial revenue YoY growth",
        "weight":     0.25,
        "thresholds": ("<40%",   "≥70%",   "≥100%",  "≥130%"),
        "now":        "+133%",
        "score":      4,
        "comment":    "The single best growth number in large-cap software right now; the entire bull case rests on this holding",
    },
    {
        "name":       "US Government revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<10%",   "≥30%",   "≥55%",   "≥80%"),
        "now":        "+84%",
        "score":      4,
        "comment":    "Government isn't the laggard here either — Maven and intel-community expansion are both scaling fast",
    },
    {
        "name":       "Total revenue YoY growth",
        "weight":     0.15,
        "thresholds": ("<30%",   "≥50%",   "≥65%",   "≥80%"),
        "now":        "+85%",
        "score":      4,
        "comment":    "$1.633B in Q1, well above the pace implied by even the raised FY2026 guide of $7.65-7.662B (+71%)",
    },
    {
        "name":       "Rule of 40 score",
        "weight":     0.15,
        "thresholds": ("<40",    "≥70",    "≥100",   "≥130"),
        "now":        "145",
        "score":      4,
        "comment":    "Growth + margin = 145. Management notes this is matched only by NVIDIA, Micron, and SK hynix — extremely rare company",
    },
    {
        "name":       "Adjusted operating margin",
        "weight":     0.10,
        "thresholds": ("<35%",   "≥45%",   "≥55%",   "≥62%"),
        "now":        "60%",
        "score":      4,
        "comment":    "Q1 adj operating margin 60% on 85% revenue growth — genuine operating leverage, not just top-line hype",
    },
    {
        "name":       "Forward P/E (GAAP-basis)",
        "weight":     0.15,
        "thresholds": (">180x",  "≤130x",  "≤90x",   "≤60x"),
        "now":        "~130x",
        "score":      1,
        "comment":    "Even after a 40% drawdown from the 52-week high, the stock trades at a multiple few businesses can grow into fast enough",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Growth quality — Rule of 40 = 145; this is not growth bought with margin, both are exceptional simultaneously", +0.9, 0.20),
    ("+", "Government moat — FedRAMP High, classified workloads, and defense AI integration are extremely hard to replicate", +0.5, 0.15),
    ("-", "Valuation — ~130x forward GAAP earnings prices near-flawless execution for years, with no margin for a slowdown", -1.1, 0.30),
    ("+", "Commercial AIP proof point — 133% US commercial growth is now multiple quarters old, not a single-quarter spike",  +0.6, 0.15),
    ("-", "Concentration + comp difficulty — US government and a handful of large commercial logos still drive an outsized share", -0.4, 0.10),
    ("-", "Multiple has already round-tripped once — the 40% drawdown from the 52-week high shows how fast sentiment can reverse here", -0.5, 0.10),
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
CONS_EPS_2YR  = 1.55    # conservative FY2028E: ~27.7% EPS CAGR — a sharp deceleration from current pace, still very good
CONS_PE_2YR   = 65      # multiple compresses meaningfully from ~130× today, still a rich growth-stock multiple
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Government AI OS / Commercial AIP")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))
print(f"  ⚠ Q2 2026 results due {Q2_REPORT_DATE} AFTER THE CLOSE — the same day as this refresh.")
print(f"  Consensus: revenue ${Q2_CONSENSUS_REV_B:.3f}B, non-GAAP EPS ${Q2_CONSENSUS_EPS:.2f}. Figures below use Q1 actuals + guidance.")

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<32}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<32}  ${curr:>11.2f}  ${bear:>8.2f}  ${bull:>8.2f}  {bear-curr:>+7.2f}  {bull-curr:>+7.2f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<32}  ${curr_total:>11.2f}  ${bear_total:>8.2f}  ${bull_total:>8.2f}  {bear_total-curr_total:>+7.2f}  {bull_total-curr_total:>+7.2f}")
print(f"  FY2026 guidance (raised at Q1): revenue $7.65-7.662B (+71% YoY)")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_op   = curr_total * OP_MARGIN_CURR
curr_eps  = round(curr_op * (1 - TAX_RATE) / shares, 2)

bull_op   = bull_total * OP_MARGIN_BULL
shares_b  = shares * 0.99
bull_eps_imp = round(bull_op * (1 - TAX_RATE) / shares_b, 2)

bear_op   = bear_total * OP_MARGIN_BEAR
bear_eps_imp = round(max(0, bear_op) * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.2f}B rev × {OP_MARGIN_CURR*100:.1f}% margin proxy − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B rev × {OP_MARGIN_BULL*100:.1f}% margin, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 75× = ~${bull_eps_imp*75:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B rev × {OP_MARGIN_BEAR*100:.1f}% margin (heavy spend persists, growth decelerates)")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 45× trough = ~${bear_eps_imp*45:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")
print()
print(f"  ⚠ NOTE THE ASYMMETRY: even the BEAR trough multiple (45×) would be considered rich for")
print(f"  almost any other company in this coverage. There is no scenario here where PLTR becomes")
print(f"  a conventionally cheap stock — the question is only how much growth premium survives.")

# RULE OF 40 CHECK
print()
print(f"  RULE OF 40 CHECK  (the Palantir-specific angle):")
print(f"  Rule of 40 score (Q1 2026):     {RULE_OF_40_SCORE}  (revenue growth % + adj operating margin %)")
print(f"  US Commercial growth:            +{US_COMMERCIAL_GROWTH}% YoY")
print(f"  US Government growth:            +{US_GOV_GROWTH}% YoY")
print(f"  Total US growth:                 +{US_TOTAL_GROWTH}% YoY")
print()
print(f"  A score of 145 puts Palantir in a group management describes as matched only by Nvidia,")
print(f"  Micron, and SK hynix — companies riding the physical AI buildout. Palantir is the only")
print(f"  one of that group selling SOFTWARE, not silicon or memory, which is either the best")
print(f"  argument for a durable premium multiple or the best argument that this growth rate")
print(f"  cannot possibly be extrapolated in a straight line — the model can't fully resolve which.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * OP_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_marg = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 37.7% margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*65:.2f}/share at 65× P/E")
print(f"  Every 1pp of operating margin:        +${eps_per_1pp_marg:.3f}/EPS  = +${eps_per_1pp_marg*65:.2f}/share at 65× P/E")
print(f"  Every 1 turn of P/E:                  ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")
print(f"  ↑ at ~130× forward, the multiple is overwhelmingly the whole story here")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (commercial / government / total growth / Rule of 40 / margin / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<38}  {'BEAR':>7}  {'BASE':>7}  {'BULL':>7}  {'XBULL':>7}  {'NOW':>7}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<38}  {ths[0]:>7}  {ths[1]:>7}  {ths[2]:>7}  {ths[3]:>7}  {s['now']:>7}  {lbl}  {b}")
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
    ("US Commercial growth",       "+133%",  "<40%",    "-93pp",  "AIP bootcamp conversion rate drops; enterprise pilots don't scale to contracts"),
    ("US Government growth",       "+84%",   "<10%",    "-74pp",  "Defense/intel budget scrutiny or a contract-review cycle stalls renewals"),
    ("Total revenue growth",       "+85%",   "<30%",    "-55pp",  "Both commercial and government legs decelerate at once"),
    ("Rule of 40 score",           "145",    "<40",     "-105",   "Margin compression AND growth deceleration hit simultaneously"),
    ("Adjusted operating margin",  "60%",    "<35%",    "-25pp",  "S&M/R&D spend doesn't scale down even as growth slows"),
    ("Forward P/E",                "~130x",  "≤45x",    "-85x",   "Sentiment fully reverses; market reprices PLTR as a normal enterprise software name"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: this is a bear case about the MULTIPLE far more than the business. Every")
print(f"  operating signal in this dashboard scores BULL or XBULL — the growth, the margin, the")
print(f"  Rule of 40 score are all exceptional and multi-quarter, not a single lucky print. The")
print(f"  bear case requires the market to decide 130x forward earnings was never sustainable,")
print(f"  independent of whether the underlying execution keeps delivering. That has already")
print(f"  happened once this year — the 40% drawdown from the 52-week high — and could happen again.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS estimate:       ${EPS_FY2026E:.2f}  (bottom-up off the raised $7.65-7.662B revenue guide)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (even the 52-week low implies ~90x+ forward — this is not a value stock)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP is enormous by this coverage's standards — but note what the")
print(f"  EPP floor itself assumes: a 45× multiple, which most large-cap software names would")
print(f"  consider generous, not distressed. There is no version of this model where PLTR becomes")
print(f"  cheap in an absolute sense. The entire investment case is a bet on GROWTH DURATION, not")
print(f"  on a margin of safety in the conventional value-investing sense.")
print(f"  At a 55× reversion (still well above a normal software multiple): ${EPS_FY2026E:.2f} × 55 = ${EPS_FY2026E*55:.0f}")
print(f"  ({(EPS_FY2026E*55/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: growth decelerates sharply, multiple compresses hard)")
hr()
print(f"  Conservative FY2028E EPS:  ${CONS_EPS_2YR:.2f}  (~27.7% EPS CAGR — a sharp deceleration, still a very good growth rate)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~130× → 65×; a real de-rating, still a rich growth multiple)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (no dividend)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: this case assumes growth decelerates from 85%+ to under 30%/yr AND the")
print(f"  multiple is cut in half — and even with EPS still compounding at a rate most companies")
print(f"  would envy, the total return comes out {cons_annual:+.1f}%/yr. That is the model's clearest signal")
print(f"  on PLTR: you are not being paid a margin of safety for the valuation risk. A genuinely")
print(f"  strong growth outcome, paired with only a HALVING (not a collapse) of the multiple, still")
print(f"  loses money from here. The bull case is real, but the conservative case is a warning.")
print(f"  Breakeven at 65× requires FY2028E EPS ≥ ${CURRENT_PRICE / CONS_PE_2YR:.2f} — above this conservative estimate.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.60
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Drawdown from high:   -{(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.1f}%  (a real correction, on a stock still growing 85%+ YoY)")
print(f"  Annual dividend:      none")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (one of the highest-beta large-caps in the market)")
print(f"  Beta vs S&P 500:      2.00+  (moves as a high-multiple AI-sentiment proxy, not a typical software stock)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe, but this stock has already moved similarly before)")
print(f"  → Q2 print TODAY after close is the immediate catalyst — options market pricing a ~12% swing.")
print(f"  → US Commercial growth rate is the single number that matters most for the multiple.")
print(f"  → WATCHLIST at current price  |  ACCUMULATE $85–100  |  BUY below $65")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f} the market composite is {MARKET_COMPOSITE:.2f}/4.0. The model's")
print(f"  adjusted composite is {ADJ_COMPOSITE:.2f}/4.0, for a gap of {ADJ_GAP:+.2f} — {valuation_label.lower()}.")
print(f"  Every operating signal here is exceptional. The reason this isn't a clean BUY is that the")
print(f"  price already reflects almost all of that excellence — WATCHLIST is the model's way of")
print(f"  saying 'great business, and the valuation risk is real enough that today's price is not")
print(f"  obviously the right entry point,' which is a genuinely different statement from 'avoid.'")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q2 2026 results TODAY after close — US Commercial growth rate is the number that matters most")
print(f"  (2) FY2026/FY2027 guidance revision — another raise would validate the durability of the growth rate")
print(f"  (3) Large new government contract wins/losses — concentration cuts both ways here")
print(f"  (4) Any signs of AIP bootcamp-to-contract conversion slowing — the leading indicator for commercial deceleration")
print(f"  (5) Broader AI-sentiment/multiple-compression risk across the sector, independent of PLTR's own execution")
print(f"  WATCHLIST at ${CURRENT_PRICE:.2f}  |  ACCUMULATE $85–100  |  BUY below $65")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  Rule of 40: {RULE_OF_40_SCORE}")
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
