"""
SAP  ·  SAP SE (ADR)  ·  NYSE: SAP
Bottom-up signal model  ·  Enterprise ERP Cloud / S/4HANA Migration / Business AI
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "SAP"
COMPANY       = "SAP SE"
SECTOR        = "Enterprise ERP Cloud · S/4HANA Migration · Business AI (Joule) · NYSE: SAP"
CURRENT_PRICE = 183.62       # USD per ADR; close 2026-07-31 (verified live)
VOL_52W_LOW   = 144.97       # 2026 trough
VOL_52W_HIGH  = 299.48       # 2025 peak; pre-derating
SHARES_OUT_M  = 1_140.0      # millions; $209.4B mkt cap / $183.62 (1 ADR = 1 ordinary share)
ANNUAL_DIV    = 2.14         # $/ADR; yield ~1.16%
EUR_USD       = 1.165        # implied from Q1 reporting (€1.72 non-IFRS EPS = $2.01)

# ── SEGMENT REVENUE BRIDGE (FY2026E, € billions) ─────────────────────────────
# Q2 2026: revenue €9.88B (+9%, +11% cc); cloud €6.3B (+24%); backlog €22.9B (+26%)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Cloud (SaaS + BTP)",       25.5, 23.5, 28.0, "€6.3B/qtr growing +24%; €22.9B current cloud backlog (+26%) underwrites it"),
    ("Software support",         10.0,  9.8, 10.3, "On-prem ECC maintenance annuity; converts into cloud as the 2027 deadline bites"),
    ("Services",                  4.0,  3.8,  4.4, "Migration consulting; low margin but the on-ramp for every S/4HANA conversion"),
    ("Software licenses",         1.0,  0.7,  1.3, "Perpetual licences; structurally in run-off by design"),
]

# Margin assumptions (non-IFRS, € basis)
OP_MARGIN_CURR    = 0.296   # FY2026E: €12.0B op profit guidance midpoint on ~€40.5B revenue
OP_MARGIN_BULL    = 0.330   # BULL: 2027 opex grows at 80–90% of revenue growth = operating leverage
OP_MARGIN_BEAR    = 0.270   # BEAR: R&D + AI marketing + M&A dilution outrun revenue
NET_FIN_EXPENSE_B = 0.4     # € net financial expense
TAX_RATE          = 0.310   # non-IFRS effective rate (SBC non-deductibility keeps this high)

# ── BACKLOG / MIGRATION CLOCK (the SAP-specific calculator) ──────────────────
CLOUD_BACKLOG_B     = 22.9   # € current cloud backlog at Q2 2026 (+26% YoY)
CLOUD_REV_Q2_B      =  6.3   # € cloud revenue in Q2 2026 (+24% YoY)
ECC_MIGRATED_PCT    = 0.55   # ~55% of the legacy ECC base has committed to S/4HANA
ECC_DEADLINE_YEAR   = 2027   # mainstream ECC maintenance ends — a contractual forcing function
OP_PROFIT_GUIDE_LO  = 11.8   # € FY2026 non-IFRS operating profit guidance (cc), trimmed
OP_PROFIT_GUIDE_HI  = 12.2

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E_EUR = 7.05       # € non-IFRS FY2026E (H1 actual €3.31: Q1 €1.72 + Q2 €1.59)
EPS_FY2026E     = round(EPS_FY2026E_EUR * EUR_USD, 2)   # USD per ADR
PE_PESSIMISTIC  = 17.0       # trough P/E: SAP's 2022 rate-shock trough was ~16× forward;
                             # 17× credits the far higher recurring-revenue mix today
EPP             = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E; USD per ADR) ───────────────────
SCENARIOS = {
    "BEAR":  ( 6.85, 15,  103, "Cloud decelerates below 15%; 2027 deadline slips; margin expansion never arrives"),
    "BASE":  ( 9.60, 20,  192, "Cloud ~20%; €23B backlog converts; 2027 acceleration delivered; margin to 31%"),
    "BULL":  (10.60, 26,  276, "Cloud reaccelerates; operating leverage lands; multiple recovers toward the 5-yr norm"),
    "XBULL": (12.50, 30,  375, "SAP = system of record for enterprise AI agents; Joule premium pricing; Dremio data layer"),
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
        "name":       "Cloud revenue YoY growth (cc)",
        "weight":     0.25,
        "thresholds": ("<12%",   "≥18%",   "≥25%",   "≥32%"),
        "now":        "+24%",
        "score":      2,
        "comment":    "€6.3B in Q2, +24% — an acceleration from Q1. Just below the BULL threshold, and trending the right way",
    },
    {
        "name":       "Current cloud backlog YoY",
        "weight":     0.25,
        "thresholds": ("<15%",   "≥20%",   "≥25%",   "≥33%"),
        "now":        "+26%",
        "score":      3,
        "comment":    "€22.9B and growing FASTER than cloud revenue — reverses last year's pattern. Best single datapoint in the print",
    },
    {
        "name":       "Non-IFRS operating margin",
        "weight":     0.15,
        "thresholds": ("<26%",   "≥29%",   "≥32%",   "≥35%"),
        "now":        "27.8%",
        "score":      1,
        "comment":    "Down 0.7pp YoY; FY guidance trimmed to €11.8–12.2B on R&D, AI marketing and Dremio/Prior Labs dilution",
    },
    {
        "name":       "Total revenue growth (cc)",
        "weight":     0.15,
        "thresholds": ("<7%",    "≥10%",   "≥14%",   "≥18%"),
        "now":        "+11%",
        "score":      2,
        "comment":    "€9.88B in Q2 (+9% reported, +11% cc). The licence run-off caps headline growth below cloud growth",
    },
    {
        "name":       "Forward P/E vs 5-yr average (~30×)",
        "weight":     0.10,
        "thresholds": (">32x",   "≤26x",   "≤21x",   "≤17x"),
        "now":        "22.4x",
        "score":      2,
        "comment":    "22.4× FY2026E non-IFRS EPS. Cheap against SAP's own history, not yet cheap in absolute terms",
    },
    {
        "name":       "S/4HANA migration conversion",
        "weight":     0.10,
        "thresholds": ("<35%",   "≥50%",   "≥65%",   "≥80%"),
        "now":        "~55%",
        "score":      2,
        "comment":    "~45% of the ECC base is still unconverted with mainstream maintenance ending 2027 — a contractual clock",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "S/4HANA 2027 deadline — ~45% of the ECC base still to move; a contractual forcing function", +0.8, 0.20),
    ("+", "€22.9B cloud backlog (+26%) — contracted and growing faster than revenue; visibility is high", +0.7, 0.20),
    ("-", "Margin trajectory — guidance trimmed; R&D, AI marketing and M&A dilution outrunning revenue",  -0.7, 0.20),
    ("+", "Valuation reset — 22.4× forward vs a ~30× 5-yr average; 39% below the ATH on better backlog",  +0.7, 0.15),
    ("-", "AI disintermediation — agentic AI is a genuine threat to per-seat ERP subscription economics", -0.6, 0.15),
    ("-", "FX translation — a stronger dollar is a persistent reported-revenue headwind for ADR holders", -0.4, 0.10),
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
CONS_EPS_2YR  = 9.40    # conservative FY2028E USD/ADR: ~13% EPS CAGR, no margin surprise
CONS_PE_2YR   = 21      # modest re-rating from 22.4× — well short of the ~30× 5-yr average
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  ERP Cloud / S/4HANA Migration / Business AI")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E, € billions  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<26}  {'FY2026E (€B)':>13}  {'Bear (€B)':>10}  {'Bull (€B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<26}  €{curr:>11.1f}  €{bear:>8.1f}  €{bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<26}  €{curr_total:>11.1f}  €{bear_total:>8.1f}  €{bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  FY2026 guidance: non-IFRS operating profit €{OP_PROFIT_GUIDE_LO:.1f}–{OP_PROFIT_GUIDE_HI:.1f}B at constant currencies")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_op   = curr_total * OP_MARGIN_CURR
curr_eps_eur = round((curr_op - NET_FIN_EXPENSE_B) * (1 - TAX_RATE) / shares, 2)
curr_eps  = round(curr_eps_eur * EUR_USD, 2)

bull_op   = bull_total * OP_MARGIN_BULL
shares_b  = shares * 0.98        # modest buyback
bull_eps_eur = round((bull_op - NET_FIN_EXPENSE_B * 0.75) * (1 - TAX_RATE) / shares_b, 2)
bull_eps_imp = round(bull_eps_eur * EUR_USD, 2)

bear_op   = bear_total * OP_MARGIN_BEAR
bear_eps_eur = round((bear_op - NET_FIN_EXPENSE_B * 1.5) * (1 - TAX_RATE) / shares, 2)
bear_eps_imp = round(bear_eps_eur * EUR_USD, 2)

print(f"  FY2026E EPS check:  €{curr_total:.1f}B rev × {OP_MARGIN_CURR*100:.1f}% op margin = €{curr_op:.1f}B")
print(f"  − €{NET_FIN_EXPENSE_B:.1f}B net financial expense − {TAX_RATE*100:.1f}% tax  ÷ {shares:.3f}B shares")
print(f"  =  €{curr_eps_eur:.2f}  ×  {EUR_USD:.3f} EUR/USD  =  ${curr_eps:.2f}/ADR  (model estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  €{bull_total:.1f}B rev × {OP_MARGIN_BULL*100:.1f}% op margin (operating leverage lands)")
print(f"  =  €{bull_eps_eur:.2f}  =  ${bull_eps_imp:.2f}/ADR  →  × 26× = ~${bull_eps_imp*26:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  €{bear_total:.1f}B rev × {OP_MARGIN_BEAR*100:.1f}% op margin (expansion never arrives)")
print(f"  =  €{bear_eps_eur:.2f}  =  ${bear_eps_imp:.2f}/ADR  →  × 15× trough = ~${bear_eps_imp*15:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")
print()
print(f"  ⚠ THE SAP-SPECIFIC POINT: the revenue range is narrow (€{bear_total:.1f}B–€{bull_total:.1f}B, a {(bull_total/bear_total-1)*100:.0f}% spread)")
print(f"  because {(SEG_DATA[0][1]+SEG_DATA[1][1])/curr_total*100:.0f}% of revenue is cloud subscriptions plus maintenance — contracted, recurring,")
print(f"  and already in the €{CLOUD_BACKLOG_B:.1f}B backlog. SAP's outcome is decided by MARGIN and MULTIPLE,")
print(f"  not by whether the revenue shows up. That is a much narrower thing to underwrite.")

# ─── BACKLOG CLOCK ───────────────────────────────────────────────────────────
print()
print(f"  BACKLOG COVERAGE CHECK:")
print(f"  Current cloud backlog:            €{CLOUD_BACKLOG_B:.1f}B  (contracted, next 12 months)")
print(f"  Annualised cloud revenue run-rate: €{CLOUD_REV_Q2_B*4:.1f}B  (Q2 €{CLOUD_REV_Q2_B:.1f}B × 4)")
print(f"  Coverage ratio:                    {CLOUD_BACKLOG_B/(CLOUD_REV_Q2_B*4)*100:.0f}%  of the forward cloud year already signed")
print(f"  Backlog growth (+26%) > cloud revenue growth (+24%) → the pipeline is REFILLING faster")
print(f"  than it drains. This reversed last year's pattern and is the strongest tell in the print.")
print()
print(f"  MIGRATION CLOCK: ~{(1-ECC_MIGRATED_PCT)*100:.0f}% of the ECC installed base has NOT committed to S/4HANA")
print(f"  with mainstream maintenance ending in {ECC_DEADLINE_YEAR}. Every one of those customers faces a")
print(f"  choice between paying for extended support, migrating to SAP cloud, or replatforming")
print(f"  an ERP — the last of which is a multi-year, career-risking project. This is the most")
print(f"  reliable revenue forcing function in enterprise software.")

# KEY SENSITIVITIES
print()
eps_per_1B_cloud = 1.0 * 0.75 * (1 - TAX_RATE) / shares * EUR_USD   # cloud incremental margin ~75%
eps_per_1pp_marg = curr_total * 0.01 * (1 - TAX_RATE) / shares * EUR_USD
print(f"  KEY SENSITIVITIES:")
print(f"  Every €1B cloud revenue (75% inc. margin):  +${eps_per_1B_cloud:.3f}/ADR EPS  = +${eps_per_1B_cloud*20:.2f}/ADR at 20× P/E")
print(f"  Every 1pp of operating margin:              +${eps_per_1pp_marg:.3f}/ADR EPS  = +${eps_per_1pp_marg*20:.2f}/ADR at 20× P/E")
print(f"  Every 1 turn of P/E:                        ±${EPS_FY2026E:.2f}/ADR  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")
print(f"  Every 5% move in EUR/USD:                   ±${EPS_FY2026E*0.05:.2f}/ADR EPS (pure translation, no economics)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (cloud growth / backlog / margin / migration clock)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<44}  {'BEAR':>6}  {'BASE':>6}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>7}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<44}  {ths[0]:>6}  {ths[1]:>6}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>7}  {lbl}  {b}")
    print(f"    {s['comment']}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15%/yr hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:90]:<90}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<34}  {'Current':>9}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Cloud revenue YoY (cc)",     "+24%",   "<12%",    "−12pp",  "AI-native ERP entrants win net-new workloads"),
    ("Current cloud backlog YoY",  "+26%",   "<15%",    "−11pp",  "Migration decisions deferred past the 2027 deadline"),
    ("Non-IFRS operating margin",  "27.8%",  "<26%",    "−2pp",   "AI compute + R&D + serial M&A dilution compound"),
    ("Total revenue growth (cc)",  "+11%",   "<7%",     "−4pp",   "Licence run-off outpaces cloud adds; European macro"),
    ("Forward P/E",                "22.4x",  "≤15x",    "−7x",    "Software de-rating: SaaS repriced as a utility"),
    ("S/4HANA conversion",         "~55%",   "<40%",    "−15pp",  "Extended-support option chosen en masse over migration"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<34}  {curr:>9}  {bear_v:>9}  {move:>8}  {trigger[:46]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the bear case for SAP is NOT a demand collapse — €{CLOUD_BACKLOG_B:.1f}B of backlog makes")
print(f"  that arithmetically hard over two years. The bear case is that SAP spends the")
print(f"  migration windfall as fast as it earns it: R&D, AI marketing, and a string of")
print(f"  acquisitions (Dremio, Prior Labs) that each dilute margin by ~100bp. Revenue keeps")
print(f"  compounding, operating leverage never appears, and the market stops paying a")
print(f"  software multiple for a 10%-growth, 27%-margin business. That is how you get to 15×.")
print(f"  Note: BEAR ${bear_price} is ~{(1-bear_price/VOL_52W_LOW)*100:.0f}% below the 52W low of ${VOL_52W_LOW:.2f} — a real but severe path.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E non-IFRS EPS:      €{EPS_FY2026E_EUR:.2f}  =  ${EPS_FY2026E:.2f}/ADR  (H1 actual €3.31)")
print(f"  Pessimistic P/E at trough:  {PE_PESSIMISTIC:.0f}×  (2022 rate-shock trough ~16×; 17× credits today's recurring mix)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/ADR")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP is a middling reading — neither the distress signal SAP")
print(f"  offered at its 2026 low nor the 90%+ premiums carried by the AI-infrastructure names.")
print(f"  At ${CURRENT_PRICE:.2f} the ADR trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E non-IFRS EPS against a 5-year")
print(f"  average near 30×, having fallen {(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.0f}% from ${VOL_52W_HIGH:.2f} while the backlog it")
print(f"  is valued on grew 26%. Price down, contracted revenue up — that is the setup.")
print(f"  EPP path: FY2028E EPS ~$9.40 × {PE_PESSIMISTIC:.0f}× = ${9.40*PE_PESSIMISTIC:.0f} floor by 2028 (EPP compounding ~13%/yr).")
print(f"  At the ~30× 5-yr average: ${EPS_FY2026E:.2f} × 30 = ${EPS_FY2026E*30:.0f}  (+{(EPS_FY2026E*30/CURRENT_PRICE-1)*100:.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: no margin surprise, only a partial re-rating)")
hr()
print(f"  Conservative FY2028E EPS:  ${CONS_EPS_2YR:.2f}/ADR  (~13% EPS CAGR; margin holds, no expansion credit)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (22.4× → 21×; still 30% BELOW the 5-yr average)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/ADR")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/ADR  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP — AND THE LIMIT: with no margin-expansion credit and a slightly lower")
print(f"  multiple than today's, SAP returns only {cons_annual:.1f}%/yr. That is positive but it does not")
print(f"  clear a 15% hurdle, and it is the honest reason this is ACCUMULATE and not BUY.")
print(f"  The margin of safety here comes from the contracted backlog, not from the price.")
print(f"  To earn a BUY you need EITHER the 2027 operating leverage management has guided to,")
print(f"  OR a lower entry — roughly ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs, 0):.0f}, where ratio B drops under 0.75×.")
print(f"  Breakeven at 21× requires FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f} (+{((CURRENT_PRICE - cons_divs)/CONS_PE_2YR/EPS_FY2026E-1)*100:.0f}% over 2 years).")
print(f"  BUY trigger: below ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs, 0):.0f} (where ratio B drops under 0.75×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.32
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (ADR at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Drawdown from high:   −{(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.1f}%  (a full software de-rating, not an SAP-specific event)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/ADR  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; German withholding applies)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated for a recurring-revenue business; sector beta)")
print(f"  Beta vs S&P 500:      1.10  (plus a EUR/USD overlay ADR holders cannot hedge away)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (would take the ADR well below its 52W low)")
print(f"  → Q3 margin is the swing print: guidance was trimmed, so the bar is now low.")
print(f"  → Backlog growth is the leading indicator; cloud revenue growth is the lagging one.")
print(f"  → ACCUMULATE at current price  |  BUY below ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs, 0):.0f}  |  TRIM above $290")

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
print(f"  adjusted composite is {ADJ_COMPOSITE:.2f}/4.0, giving a gap of {ADJ_GAP:+.2f} — {valuation_label.lower()}.")
print(f"  NOTE THE TENSION IN THIS MODEL, because it is the whole decision: ratio B ({ratio_b_str})")
print(f"  says the risk/reward is good — the contracted backlog makes the downside genuinely")
print(f"  hard to reach. The composite gap ({ADJ_GAP:+.2f}) says the market is already paying for better")
print(f"  execution than SAP is currently delivering, chiefly on margin. Both readings are")
print(f"  right: the revenue is de-risked and the profitability is not. That combination is")
print(f"  what ACCUMULATE means — own it, keep sizing room, and let the Q3 margin print or a")
print(f"  move toward ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs, 0):.0f} decide whether it becomes a BUY.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q3 2026 operating margin — guidance was trimmed, so the bar is now low")
print(f"  (2) 2027 revenue acceleration — management has explicitly guided to it; hold them to it")
print(f"  (3) Current cloud backlog growth — the leading indicator; must stay above +20%")
print(f"  (4) Joule / Business AI monetisation — the first real pricing datapoint re-rates the stock")
print(f"  (5) S/4HANA conversion rate into the 2027 maintenance deadline")
print(f"  ACCUMULATE at ${CURRENT_PRICE:.2f}  |  BUY below $170  |  MAX SIZE near EPP ${EPP:.0f}  |  TRIM above $290")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  Backlog: €{CLOUD_BACKLOG_B:.1f}B")
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
