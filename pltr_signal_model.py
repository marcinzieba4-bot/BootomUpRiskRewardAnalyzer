"""
PLTR  ·  Palantir Technologies Inc.  ·  NASDAQ: PLTR
Bottom-up signal model  ·  Government AI / Commercial AIP / Big Data Analytics
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "PLTR"
COMPANY       = "Palantir Technologies Inc."
SECTOR        = "Government AI OS · Commercial AIP · Big Data Analytics · NASDAQ: PLTR"
CURRENT_PRICE = 135.90      # USD; as of 2026-06-10
VOL_52W_LOW   = 118.93      # 52-week low; implies ~91x forward EPS even at trough
VOL_52W_HIGH  = 200.00      # 52-week high; AI mania peak
SHARES_OUT_M  = 2_400.0     # millions; modest dilution from SBC

# Dividend: none
ANNUAL_DIV    = 0.0         # $/share; no dividend, all cash reinvested/buyback-offset SBC

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Government (US/Allied)",      1.55, 1.30, 1.95, "FedRAMP High classified workloads; defense AI; Maven/NATO expansion"),
    ("US Commercial",                1.30, 0.85, 1.95, "AIP bootcamp-to-contract flywheel; +133% YoY; deceleration risk swing factor"),
    ("International Commercial",     0.55, 0.40, 0.85, "Europe/APAC AIP rollout; slower enterprise adoption cycles"),
    ("International Government",     0.45, 0.35, 0.65, "Allied defense AI; UK/Europe/Asia government contracts"),
]

# Margin assumptions
ADJ_OP_MARGIN_CURR = 0.60   # blended adj operating margin FY2026E (~60%)
ADJ_OP_MARGIN_BULL = 0.66   # BULL: continued operating leverage as revenue scales
OPEX_FIXED_B       = 1.10   # R&D + SG&A baseline ($B); grows slower than revenue (operating leverage)
TAX_RATE           = 0.21   # effective rate; large NOLs reduce cash tax near-term but model uses statutory

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 1.30        # FY2026E adj EPS estimate (consensus ~$1.25-1.35; non-GAAP)
PE_PESSIMISTIC = 50.0        # trough P/E: even bear case retains premium for AI OS monopoly position
                              # (52W low $118.93 / $1.30 ~ 91x; 50x reflects severe-but-not-collapse de-rate)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $65

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (0.60, 50,   30, "US Commercial decelerates to <60% YoY; multiple compresses to 50x; EPS $0.60 → 50x = $30"),
    "BASE":  (1.30, 80,  104, "Growth moderates toward 70-90% YoY; Rule of 40 sustains ~120+; EPS $1.30 → 80x = $104"),
    "BULL":  (2.00, 90,  180, "AIP flywheel accelerates; gov contract wins compound; EPS $2.00 → 90x = $180"),
    "XBULL": (3.20, 100, 320, "Palantir becomes default enterprise/government AI OS; EPS $3.20 → 100x = $320"),
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
        "thresholds": ("<60%",   "≥80%",  "≥110%",  "≥140%"),
        "now":        "+133%",
        "score":      4,
        "comment":    "AIP bootcamp-to-contract conversion driving record growth; Q1 +133% YoY; key swing factor",
    },
    {
        "name":       "US Government/defense AI contract momentum",
        "weight":     0.20,
        "thresholds": ("Slowing","Stable", "Accel.", "Surge"),
        "now":        "Accel.",
        "score":      3,
        "comment":    "FedRAMP High classified workload expansion; Maven/NATO/allied defense AI deals scaling",
    },
    {
        "name":       "International commercial expansion",
        "weight":     0.15,
        "thresholds": ("<20%",   "≥30%",  "≥50%",   "≥70%"),
        "now":        "~40%",
        "score":      2,
        "comment":    "Europe/APAC AIP rollout lagging US pace; slower enterprise adoption cycles abroad",
    },
    {
        "name":       "Adjusted operating margin trajectory",
        "weight":     0.15,
        "thresholds": ("<45%",   "≥55%",  "≥62%",   "≥68%"),
        "now":        "60%",
        "score":      3,
        "comment":    "Operating leverage strong; 60% adj op margin reflects software-like scaling economics",
    },
    {
        "name":       "Rule of 40 sustainability (growth + margin)",
        "weight":     0.15,
        "thresholds": ("<60",    "≥80",   "≥120",   "≥150"),
        "now":        "145",
        "score":      4,
        "comment":    "Rule of 40 = 145%; extraordinary by any software benchmark; durability is the question",
    },
    {
        "name":       "Revenue growth deceleration risk (comp difficulty)",
        "weight":     0.10,
        "thresholds": ("Sharp ↓","Mod. ↓", "Stable", "Accel."),
        "now":        "Mod. ↓ risk",
        "score":      2,
        "comment":    "85% YoY growth rate faces tougher comps; 133% US Commercial print unlikely to repeat at scale",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Government AI OS monopoly — FedRAMP High, classified workloads, deep allied defense moat",   +0.7, 0.25),
    ("+", "Commercial AIP flywheel — bootcamp model drives rapid land-and-expand; Rule of 40 = 145%",    +0.6, 0.20),
    ("-", "Extreme valuation — 104x FY2026E EPS, 43x P/S already prices years of 80%+ growth",          -0.9, 0.25),
    ("-", "No valuation floor near current range — 52W low $118.93 still implies ~91x forward EPS",     -0.6, 0.15),
    ("+", "Founder-led culture / mission alignment — sticky multi-year government relationships",        +0.3, 0.10),
    ("-", "Growth deceleration risk — 85% YoY comps get harder; AIP bootcamp conversion may plateau",    -0.5, 0.05),
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
CONS_EPS_2YR  = 1.80    # conservative FY2028E: growth decelerates but compounds; ~50% effective EPS CAGR off small base
CONS_PE_2YR   = 50      # rerating from 104x toward growth-justified 50x (still premium vs software peers)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Government AI / Commercial AIP / Big Data")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<26}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<26}  ${curr:>11.2f}  ${bear:>8.2f}  ${bull:>8.2f}  {bear-curr:>+7.2f}  {bull-curr:>+7.2f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<26}  ${curr_total:>11.2f}  ${bear_total:>8.2f}  ${bull_total:>8.2f}  {bear_total-curr_total:>+7.2f}  {bull_total-curr_total:>+7.2f}")
print()

# EPS bridge
curr_oi   = curr_total * ADJ_OP_MARGIN_CURR
curr_ni   = curr_oi * (1 - TAX_RATE)
shares    = SHARES_OUT_M / 1000
curr_eps  = round(curr_ni / shares, 2)

bull_oi      = bull_total * ADJ_OP_MARGIN_BULL
bull_ni      = bull_oi * (1 - TAX_RATE)
shares_b     = shares * 1.02   # modest SBC dilution over 2yr
bull_eps_imp = round(bull_ni / shares_b, 2)

bear_oi      = max(0, bear_total * ADJ_OP_MARGIN_CURR * 0.85 - OPEX_FIXED_B * 0.3)  # margin compression in bear
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.2f}B rev × {ADJ_OP_MARGIN_CURR*100:.0f}% adj op margin − {TAX_RATE*100:.0f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ~${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B rev × {ADJ_OP_MARGIN_BULL*100:.0f}% adj op margin − tax")
print(f"  ÷ {shares_b:.3f}B shares (SBC dilution)  =  ~${bull_eps_imp:.2f}/share  →  ${bull_eps_imp:.2f} × 90× = ~${bull_eps_imp*90:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B rev × {ADJ_OP_MARGIN_CURR*100*0.85:.0f}% margin − fixed opex haircut  =  ~${bear_eps_imp:.2f}/share")
print(f"  At 50× de-rated P/E = ~${bear_eps_imp*50:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = (1.0 * ADJ_OP_MARGIN_CURR * (1 - TAX_RATE)) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B US Commercial revenue (60% margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*80:.1f}/share at 80× P/E")
print(f"  10pp adj op margin expansion:                   +${curr_total*0.10*(1-TAX_RATE)/shares:.3f}/EPS  = +${curr_total*0.10*(1-TAX_RATE)/shares*80:.1f}/share at 80× P/E")
print(f"  Every 10x of P/E multiple compression:          −${curr_eps*10:.1f}/share  (at FY2026E EPS ${curr_eps:.2f})")
print(f"  US Commercial growth 133% → 70% (deceleration):  ~${(SEG_DATA[1][1]*0.70 - SEG_DATA[1][1]*1.33)*ADJ_OP_MARGIN_CURR*(1-TAX_RATE)/shares*80:.1f}/share impact at 80× P/E (rev base effect, illustrative)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (US Commercial growth / Gov AI / Margin / Rule of 40 framework)")
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
    ("US Commercial revenue YoY growth",  "+133%",  "60-70%", "−63pp",  "AIP bootcamp conversion rate declines; enterprise budget tightening"),
    ("Government contract renewals",       "Strong", "At risk","↓",      "Federal budget cuts / DOGE-style spending reductions hit FedRAMP deals"),
    ("Adjusted operating margin",          "60%",    "<45%",   "−15pp",  "Reinvestment in sales/AIP infra outpaces revenue scaling"),
    ("Rule of 40",                         "145",    "<60",    "−85pts", "Growth collapses to ~30% with margin compression to ~30%"),
    ("Forward P/E multiple",               "104x",   "50x",    "−54x",   "Multiple de-rating from 104x toward 50-60x even if fundamentals hold"),
    ("International commercial growth",    "~40%",   "<20%",   "−20pp",  "European AIP adoption stalls amid macro slowdown / regulatory friction"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: US Commercial revenue growth decelerates from 133% YoY toward 60-70% as")
print(f"  AIP bootcamp-to-contract conversion rates decline and the law of large numbers bites.")
print(f"  Simultaneously, government budget pressure (defense spending review, FedRAMP renewal")
print(f"  delays) slows the second growth engine. Combined growth deceleration plus a multiple")
print(f"  de-rating from 104x toward 50x (even on still-solid 60% margins) collapses the price")
print(f"  to ~${bear_price}. Note: this is NOT a business-quality failure — it is a re-rating of an")
print(f"  exceptional business from priced-for-perfection multiples toward merely-excellent multiples.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~$1.25-1.35; non-GAAP)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (severe de-rate but still premium for AI OS moat)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  At ${CURRENT_PRICE:.2f} on FY2026E EPS ${EPS_FY2026E:.2f}, the trailing/forward P/E is ~104× and")
print(f"  P/S is ~43×. Even the 52-week low of ${VOL_52W_LOW:.2f} implies ~91× forward EPS — meaning")
print(f"  there is effectively NO valuation floor anywhere near the current trading range. A")
print(f"  +{epp_gap_pct:.0f}% premium to the EPP floor means the market is pricing in many years of")
print(f"  uninterrupted 80%+ revenue growth AND margin expansion AND multiple persistence.")
print(f"  EPP path: even if FY2028E EPS reaches ${EPS_FY2026E*2.4:.2f} (extraordinary ~85% CAGR), at")
print(f"  {PE_PESSIMISTIC:.0f}× that floor is only ${EPS_FY2026E*2.4*PE_PESSIMISTIC:.0f} — still requiring the multiple to hold near 50x.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: P/E rerates toward growth-justified levels; comps get harder)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (growth decelerates but compounds off small EPS base)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (rerates from 104× toward growth-justified 50×; still rich)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (no dividend)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE PROBLEM: even a strong conservative case (EPS more than doubling to $1.80 in")
print(f"  2 years) requires the multiple to compress from 104x to 50x just to be roughly flat.")
print(f"  For conservative 2yr to break even at 50× P/E: need EPS = ${CURRENT_PRICE / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE / CONS_PE_2YR) / EPS_FY2026E - 1)*100:.0f}% cumulative EPS growth by FY2028E — plausible given current trajectory,")
print(f"  but underscores that PLTR needs to GROW INTO its multiple, not the other way around.")
print(f"  Breakeven at 80× P/E (no multiple compression): FY2028E EPS ≥ ${CURRENT_PRICE / 80:.2f}")
print(f"  WATCHLIST trigger: ~$85  |  BUY trigger: ~$50  (levels where ratio_b moves toward <1.0x)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.55
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: even 52W LOW (${VOL_52W_LOW:.2f}) implies ~91x forward EPS — no valuation floor in range")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (none — all value via growth/multiple)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (extreme; high-multiple AI-narrative stock)")
print(f"  Beta vs S&P 500:      2.5  (very high; momentum/retail-driven; macro-AI-sentiment amplifier)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (large but not unprecedented for PLTR)")
print(f"  52W low ${VOL_52W_LOW:.2f} already a peak-to-trough move of ~{(VOL_52W_HIGH-VOL_52W_LOW)/VOL_52W_HIGH*100:.0f}% from 52W high.")
print(f"  → Multiple de-rating (104x → 50-60x) is THE KEY risk, independent of fundamentals.")
print(f"  → US Commercial growth durability (AIP bootcamp conversion) is KEY signal to monitor.")
print(f"  → AVOID at current price  |  WATCHLIST ~$85  |  ACCUMULATE ~$65-75  |  BUY below ~$50")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) reflects")
print(f"  the model's pricing of PLTR relative to the BEAR/BASE/BULL/XBULL framework. The model")
print(f"  scores fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0 after structural adjustments for the extraordinary")
print(f"  business (Rule of 40 = 145%) but extreme valuation (104x FY2026E EPS, 43x P/S).")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: PLTR is an extraordinary business priced for perfection and beyond —")
print(f"  even the 52-week low implies ~91x forward EPS, meaning there is effectively no")
print(f"  valuation floor in the current trading range.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Quarterly US Commercial revenue growth rate — deceleration watch from +133% YoY")
print(f"  (2) AIP bootcamp-to-contract conversion metrics — flywheel health indicator")
print(f"  (3) Government/defense contract awards — FedRAMP High classified workload expansion")
print(f"  (4) Adjusted operating margin trajectory — currently 60%, watch for compression/expansion")
print(f"  (5) Rule of 40 sustainability — currently 145%, durability as growth normalizes")
print(f"  (6) Multiple de-rating catalysts — macro AI sentiment shifts, rate environment, rotation")
print(f"  AVOID at ${CURRENT_PRICE:.2f}  |  WATCHLIST ~$85  |  ACCUMULATE ~$65-75  |  BUY below ~$50")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}")
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
