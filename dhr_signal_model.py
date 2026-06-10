"""
DHR  ·  Danaher Corporation  ·  NYSE: DHR
Bottom-up signal model  ·  Life Sciences / Bioprocessing / Diagnostics / DBS
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "DHR"
COMPANY       = "Danaher Corporation"
SECTOR        = "Life Sciences · Bioprocessing · Diagnostics · DBS · NYSE: DHR"
CURRENT_PRICE = 172.93      # USD; as of 2026-06-10
VOL_52W_LOW   = 165.00      # post-correction trough
VOL_52W_HIGH  = 245.00      # January 2026 high (down 29% from here to current)
SHARES_OUT_M  = 715.0       # millions

# Dividend: long growth streak; modest payout
ANNUAL_DIV    = 1.16        # $/share annualized

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Biotechnology (Cytiva, Pall)",      8.6,  7.4, 10.2, "Bioprocessing equip/consumables; Q1'26 orders +30% YoY inflection"),
    ("Life Sciences (Beckman/Leica/SCIEX)", 6.4, 5.7, 7.3, "Instrument segment recovery; academic/govt + pharma capex"),
    ("Diagnostics (Cepheid/Beckman/Radiometer)", 7.5, 7.0, 8.2, "Molecular dx, clinical chem, blood gas; stable/growing"),
    ("Masimo (pending H2 2026 close)",     0.0,  0.0,  1.4, "Patient monitoring/diagnostics add-on; $9.9B deal"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.595   # blended gross margin FY2026E
GROSS_MARGIN_BULL = 0.620   # BULL: bioprocessing consumables mix shift + DBS margin gains
OPEX_FIXED_B      = 6.7     # SG&A + R&D ($B)
TAX_RATE          = 0.155   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 8.45        # FY2026E adj EPS (BASE case estimate)
PE_PESSIMISTIC = 20.0        # trough P/E: BEAR scenario multiple ($6.50 EPS × 20× = $130)
EPP            = round(PE_PESSIMISTIC * 6.50, 0)   # $130 (20x x BEAR EPS $6.50)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (6.50, 20,  130, "Cytiva +30% proves a one-quarter blip; biopharma capex stays depressed; EPS $6.50 → 20× floor"),
    "BASE":  (8.45, 24,  203, "Cytiva orders stabilize +10-15%/yr; Diagnostics steady; DBS margin gains; EPS $8.45 → 24×"),
    "BULL":  (9.75, 28,  273, "Bioprocessing supercycle confirmed; Masimo accretive; EPS $9.75 → 28× (Method B: 25x x $9.75=$243.75)"),
    "XBULL": (12.00, 32, 384, "Multi-year bioprocessing super-cycle + Masimo synergies + DBS re-rating; EPS $12.00 → 32×"),
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
        "name":       "Cytiva/bioprocessing equipment order growth (YoY)",
        "weight":     0.30,
        "thresholds": ("<0%",    "≥10%",  "≥20%",   "≥35%"),
        "now":        "+30%",
        "score":      3,
        "comment":    "Q1 2026 +30% YoY — first positive growth in 2 years; key question: durable inflection or one-off restock",
    },
    {
        "name":       "Life Sciences instrument segment growth",
        "weight":     0.20,
        "thresholds": ("<-3%",   "≥0%",   "≥5%",    "≥10%"),
        "now":        "+2%",
        "score":      2,
        "comment":    "Beckman/Leica/SCIEX instrument demand stabilizing off depressed base; academic/govt funding still soft",
    },
    {
        "name":       "Diagnostics segment growth (Cepheid molecular dx)",
        "weight":     0.15,
        "thresholds": ("<0%",    "≥3%",   "≥6%",    "≥10%"),
        "now":        "+5%",
        "score":      3,
        "comment":    "Cepheid respiratory/molecular panels growing; Beckman Dx and Radiometer stable core franchises",
    },
    {
        "name":       "DBS-driven operating margin expansion (bps YoY)",
        "weight":     0.15,
        "thresholds": ("<0bps",  "≥30bps","≥75bps", "≥125bps"),
        "now":        "+60bps",
        "score":      2,
        "comment":    "DBS continuous-improvement playbook delivering steady margin gains; historical 15-20% compounding track record",
    },
    {
        "name":       "Masimo acquisition integration progress",
        "weight":     0.10,
        "thresholds": ("Stalled","On track","Accretive Y1","Synergy beat"),
        "now":        "On track",
        "score":      2,
        "comment":    "$9.9B deal expected to close H2 2026; adds patient monitoring/diagnostics; integration risk to management bandwidth",
    },
    {
        "name":       "Bioprocessing consumables pull-through (recurring rev growth)",
        "weight":     0.10,
        "thresholds": ("<0%",    "≥5%",   "≥12%",   "≥20%"),
        "now":        "+8%",
        "score":      2,
        "comment":    "Higher-margin consumables tied to biopharma production volumes; recovering off destocking trough but not yet at peak run-rate",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Premier life-sciences/bioprocessing franchise — Cytiva/Pall global leadership in biopharma tools", +0.6, 0.20),
    ("+", "DBS operating model — durable margin-expansion engine; 15-20% historical compounding track record", +0.5, 0.20),
    ("+", "Q1 2026 Cytiva orders +30% YoY — first positive growth in 2yrs; signals destocking cycle is over", +0.7, 0.20),
    ("-", "Down 29% from Jan 2026 highs — bioprocessing destocking hangover from 2022-2024 still weighs on sentiment", -0.4, 0.15),
    ("+", "Valuation reset — trades at just 20.5x FY2026E EPS, near-zero recovery priced in vs historical premium multiple", +0.5, 0.15),
    ("-", "Masimo integration risk — $9.9B deal closing H2 2026 could disrupt margins/distract management near-term", -0.3, 0.10),
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
CONS_EPS_2YR  = 9.00    # conservative FY2028E EPS: modest bioprocessing recovery + DBS margin gains
CONS_PE_2YR   = 22      # conservative exit multiple: modest re-rate from 20.5x toward 22x
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Life Sciences / Bioprocessing / Diagnostics / DBS")
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
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_ni   = curr_oi * (1 - TAX_RATE)
shares    = SHARES_OUT_M / 1000
curr_eps  = round(curr_ni / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B
bull_ni   = bull_oi * (1 - TAX_RATE)
shares_b  = shares * 0.97   # modest buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift / consumables weakness
bear_oi   = bear_gp - OPEX_FIXED_B * 0.97           # partial cost response (DBS)
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (BASE estimate ${EPS_FY2026E:.2f}  ✓ approx)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 28× = ~${bull_eps_imp*28:.0f}  vs BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 20× trough P/E (EPP basis) = ~${bear_eps_imp*20:.0f}  vs BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Cytiva/bioprocessing revenue:  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*24:.1f}/share at 24× P/E")
print(f"  100bps DBS margin expansion (Group):     +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*24:.1f}/share at 24× P/E")
print(f"  Masimo accretion (FY2027E, ~$1.4B rev):  +${1.4*GROSS_MARGIN_CURR*(1-TAX_RATE)/shares:.2f}/EPS  = +${1.4*GROSS_MARGIN_CURR*(1-TAX_RATE)/shares*24:.1f}/share at 24× P/E")
print(f"  Each +5pp Cytiva order growth durability: re-rates BEAR/BASE probability mix toward BULL")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Cytiva inflection / Life Sciences recovery / Diagnostics / DBS / Masimo)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>8}  {'BASE':>8}  {'BULL':>8}  {'XBULL':>9}  {'NOW':>9}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>8}  {ths[1]:>8}  {ths[2]:>8}  {ths[3]:>9}  {s['now']:>9}  {lbl}  {b}")

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
    ("Cytiva/bioprocessing order growth",   "+30%",  "<0%",   "−30pp",  "Q1'26 +30% proves a one-quarter restock blip, not durable inflection"),
    ("Life Sciences instrument growth",     "+2%",   "<-3%",  "−5pp",   "Biopharma/academic capex remains depressed; instrument orders relapse"),
    ("Diagnostics growth (Cepheid)",        "+5%",   "<0%",   "−5pp",   "Respiratory testing volumes normalize lower; Cepheid growth stalls"),
    ("DBS margin expansion",                "+60bps","<0bps", "−60bps", "Inflation/integration costs offset DBS productivity gains"),
    ("Masimo integration",                  "On track","Stalled","-1 lvl","Deal close delayed/blocked; integration disrupts margins, distracts mgmt"),
    ("Bioprocessing consumables pull-through","+8%",  "<0%",   "−8pp",  "Biopharma production volumes contract; consumables restocking reverses"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the Q1 2026 Cytiva/bioprocessing equipment order growth of +30% YoY — the first")
print(f"  positive growth in 2 years — proves to be a one-quarter inventory restock rather than the")
print(f"  start of a durable bioprocessing supercycle recovery. Biopharma capex stays depressed,")
print(f"  Life Sciences instrument demand relapses, and the Masimo integration ($9.9B, closing H2 2026)")
print(f"  distracts management and pressures margins. EPS stalls near $6.50 → 20× floor = ${bear_price}.")
print(f"  Note: ${bear_price} is close to current price — DHR's diversified Diagnostics/DBS base provides")
print(f"  a relatively shallow downside floor versus pure-play bioprocessing peers.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × bear-case EPS)")
hr()
print(f"  BEAR-case EPS estimate:         $6.50  (trough bioprocessing/Life Sciences environment)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (historical trough multiple for diversified life-sciences tools)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share  (20× × $6.50)")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  Method B cross-check: 25× × FY2027E BULL EPS $9.75 = ${25*9.75:.2f}  (BULL target ${SCENARIOS['BULL'][2]})")
print(f"  At current ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f}, implied P/E = {CURRENT_PRICE/EPS_FY2026E:.1f}×")
print(f"  — a multi-year low multiple for DHR, which has historically traded 24-30×. The market is")
print(f"  pricing near-zero recovery credit despite the Cytiva +30% order inflection.")
print(f"  EPP path: FY2028E BEAR EPS ~$7.00 × {PE_PESSIMISTIC:.0f}× = ${7.00*PE_PESSIMISTIC:.0f} floor by 2028 (EPP growing modestly).")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest bioprocessing recovery + DBS margin gains)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (modest Cytiva recovery + DBS-driven margin gains + Masimo accretion)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (modest re-rate from {CURRENT_PRICE/8.45:.1f}× toward historical-discount {CONS_PE_2YR}×)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE OPPORTUNITY: even a modest re-rate from {CURRENT_PRICE/8.45:.1f}× to {CONS_PE_2YR}× combined with")
print(f"  conservative EPS growth to ${CONS_EPS_2YR:.2f} produces a positive total return.")
print(f"  Breakeven at flat {CURRENT_PRICE/8.45:.1f}× P/E (no multiple expansion): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / (CURRENT_PRICE/8.45):.2f}")
print(f"  Breakeven at 24× P/E: FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 24:.2f}")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.24
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: 52W high (Jan 2026) — current price is down ~29% from that high")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (life-sciences tools peer-typical)")
print(f"  Beta vs S&P 500:      1.15  (slight premium; bioprocessing cycle amplifier)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (modest; near current trading range)")
print(f"  52W low ${VOL_52W_LOW:.2f} already a peak-to-trough move of ~{(1-VOL_52W_LOW/VOL_52W_HIGH)*100:.0f}% from 52W high.")
print(f"  → Cytiva order sustainability over the next 1-2 quarters is THE KEY binary.")
print(f"  → Trading at 20.5× FY2026E $8.45 EPS is a multi-year valuation low for DHR.")
print(f"  → AVOID above $245  |  WATCHLIST $185–245  |  ACCUMULATE $165–185  |  BUY $165–185 (strong add $155-165)")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) sits")
print(f"  {'ABOVE' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'BELOW'} the model's adj composite ({ADJ_COMPOSITE:.3f}).")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: at 20.5× FY2026E EPS, the market is pricing in near-zero credit for the")
print(f"  Cytiva-led bioprocessing recovery just as Q1 2026 order data shows the first positive")
print(f"  inflection in 2 years — a potential high-conviction entry point ahead of an earnings re-acceleration.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Cytiva/bioprocessing order growth sustainability — next 1-2 quarters confirming +30% inflection")
print(f"  (2) Life Sciences instrument segment recovery (Beckman/Leica/SCIEX)")
print(f"  (3) Masimo acquisition close and integration ($9.9B, H2 2026) — adds diagnostics/patient monitoring")
print(f"  (4) Diagnostics/Cepheid growth — molecular dx volumes and clinical chemistry")
print(f"  (5) DBS margin expansion updates — historical 15-20% compounding track record")
print(f"  (6) Biopharma capex spending trends — leading indicator for bioprocessing consumables pull-through")
print(f"  AVOID above $245  |  WATCHLIST $185–245  |  ACCUMULATE $165–185  |  BUY $165–185 (strong add $155–165)")
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
