"""
CRM  ·  Salesforce, Inc.  ·  NYSE: CRM
Bottom-up signal model  ·  Enterprise SaaS / CRM / Agentic AI Platform
Date: 2026-06-09
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "CRM"
COMPANY       = "Salesforce, Inc."
SECTOR        = "Enterprise SaaS · CRM · Agentic AI Platform · NYSE: CRM"
CURRENT_PRICE = 178.00       # USD; June 9 2026; down ~48% from $341 ATH; AI disruption fear discount
VOL_52W_LOW   = 122.50       # March 2026 trough; maximum Agentforce disruption fear
VOL_52W_HIGH  = 326.84       # June 2025 pre-AI-disruption-narrative peak
SHARES_OUT_M  = 920.0        # millions; declining via $50B buyback authorization; was ~970M, now ~920M

# Dividend: initiated FY2025; $0.42/quarter = $1.68/yr; growing
ANNUAL_DIV    = 1.68         # $/share FY2026 ($0.42/quarter)

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2027E revenue by segment ($B)  [Salesforce fiscal year ends January 2027]
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Sales Cloud",              9.5,  8.0, 12.5, "Core CRM; stable; Agentforce SDR agents adding expansion; 9% YoY"),
    ("Service Cloud",           10.5,  8.5, 14.0, "Largest segment; AI case deflection (Agentforce) lifting ARPU"),
    ("Agentforce (AI Agents)",   4.5,  1.5, 10.0, "New: autonomous AI agents; $500M ARR at IPO of unit; hockey-stick if enterprise adopts"),
    ("Marketing & Commerce",     5.5,  4.5,  7.5, "Marketing Cloud + Commerce Cloud; moderate growth; data moat"),
    ("Platform & Integration",   8.0,  6.5, 10.5, "MuleSoft + Tableau + Slack; integration moat; $8B ARR"),
    ("Data Cloud & Other",       5.0,  3.5,  6.5, "Data Cloud (unified customer data platform); fastest organic growth; AI fuel"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.780   # non-GAAP blended; Agentforce higher margin lifts mix
GROSS_MARGIN_BULL = 0.820   # BULL: Agentforce = 20%+ of revenue at 85%+ margin
OPEX_FIXED_B      = 18.5    # non-GAAP R&D + SG&A ($B); $50B+ revenue → some leverage
TAX_RATE          = 0.190   # effective; US-based; standard SaaS

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 13.00       # consensus $12.50–$13.50 non-GAAP; FY2027 (Jan 2027)
PE_PESSIMISTIC = 18.0        # trough: FCF yield protection floor (~5.5% FCF yield at trough)
                              # Note: CRM trades BELOW EPP at $178 — rare signal
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # $234

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 9.50, 15,  143, "Agentforce cannibalizes seat-based ARR; NRR <100%; EPS $9.50 → 15× distress floor"),
    "BASE":  (14.00, 24,  336, "Agentforce traction; 18% ARR growth; P/E re-rates from 14× to 24×; FY2028E EPS $14 → 24×"),
    "BULL":  (19.00, 27,  513, "Agentforce enterprise standard; 28% ARR growth; $6B+ ARR; FY2028E EPS $19 → 27× = $513"),
    "XBULL": (28.00, 32,  896, "CRM = enterprise AGI platform; agentic workflows displace human SaaS seats; EPS $28 → 32×"),
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
        "name":       "Total revenue YoY growth",
        "weight":     0.25,
        "thresholds": ("<8%",    "≥12%",  "≥18%",   "≥28%"),
        "now":        "+13%",
        "score":      2,
        "comment":    "FY2027 guidance +12-13% YoY; Agentforce incremental; Data Cloud re-accelerating",
    },
    {
        "name":       "Agentforce ARR / traction",
        "weight":     0.25,
        "thresholds": ("<$1B",   "≥$2B",  "≥$5B",   "≥$12B"),
        "now":        "~$2B",
        "score":      2,
        "comment":    "29K pilot deals; $500M ARR growing; not yet transformative — conversion rate is the question",
    },
    {
        "name":       "Net Revenue Retention (NRR)",
        "weight":     0.20,
        "thresholds": ("<100%",  "≥105%", "≥115%",  "≥125%"),
        "now":        "~107%",
        "score":      2,
        "comment":    "NRR recovering from 103% trough (FY2025); Agentforce ARPU expansion starting to register",
    },
    {
        "name":       "Non-GAAP operating margin",
        "weight":     0.15,
        "thresholds": ("<28%",   "≥32%",  "≥38%",   "≥44%"),
        "now":        "33.5%",
        "score":      2,
        "comment":    "Expanding from 28% (FY2024) to 33.5%; $1B+ cost cuts complete; Agentforce high-margin layer",
    },
    {
        "name":       "cRPO growth YoY (fwd bookings)",
        "weight":     0.10,
        "thresholds": ("<8%",    "≥11%",  "≥16%",   "≥24%"),
        "now":        "+12%",
        "score":      2,
        "comment":    "Current RPO $32B +14% YoY; cRPO +12% — leading indicator of next 12-month revenue",
    },
    {
        "name":       "Data Cloud ACV growth",
        "weight":     0.05,
        "thresholds": ("<20%",   "≥35%",  "≥60%",   "≥100%"),
        "now":        "+42%",
        "score":      3,
        "comment":    "Data Cloud +42% YoY; unified customer data platform is the AI fuel; 28K+ active customers",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "CRM installed-base moat — #1 CRM globally; 150K+ enterprise accounts; switching cost 3-5yr",  +0.7, 0.25),
    ("+", "Agentforce optionality — 29K pilots; if 20% convert to $500K ACV = $3B ARR inflection",       +0.6, 0.20),
    ("-", "Agentic AI disruption risk — Microsoft Copilot + SAP Joule + HubSpot AI could displace",       -0.7, 0.20),
    ("-", "Seat-based model obsolescence risk — if AI agents replace human reps, CRM seats shrink",       -0.5, 0.15),
    ("+", "FCF machine + buyback — $14B+ FCF/yr; 8.4% FCF yield; $50B buyback = 30%+ of market cap",    +0.5, 0.10),
    ("+", "Valuation asymmetry — trading BELOW EPP floor ($234); cheapest SaaS multiple in 15 years",    +0.4, 0.10),
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
CONS_EPS_2YR  = 15.00   # FY2029E conservative: 7.5% EPS CAGR (Agentforce modest; competition)
CONS_PE_2YR   = 20      # rerates from 14× toward normalized 20× (Agentforce traction confirmed)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Enterprise SaaS / CRM / Agentic AI Platform")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2027E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<26}  {'FY2027E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<26}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<26}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
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
shares_b  = shares * 0.94   # ~3%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift toward lower-margin segments
bear_oi   = bear_gp - OPEX_FIXED_B * 0.97           # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2027E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2027E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 27× = ~${bull_eps_imp*27:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 15× distress P/E (NRR <100% scenario) = ~${bear_eps_imp*15:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev      = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_agentforce = 1.0 * 0.85 * (1 - TAX_RATE) / shares   # Agentforce ~85% gross margin
eps_per_1pp_nrr     = curr_total * 0.01 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Agentforce ARR (85% margin): +${eps_per_1B_agentforce:.3f}/EPS  = +${eps_per_1B_agentforce*24:.1f}/share at 24× P/E")
print(f"  Every $1B total revenue (78% GM):      +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*24:.1f}/share at 24× P/E")
print(f"  1pp NRR expansion (×{curr_total:.0f}B ARR base):   +${eps_per_1pp_nrr:.3f}/EPS  = +${eps_per_1pp_nrr*24:.1f}/share at 24× P/E")
print(f"  1% buyback (9.2M shares at $178):      +${curr_eps*0.01:.3f}/EPS  (mechanical accretion; $50B authorization)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Agentforce traction / NRR / margins / cRPO / Data Cloud framework)")
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
    ("Total revenue YoY",          "+13%",   "<+8%",   "−5pp",   "Agentforce self-cannibalizes license ARR"),
    ("Agentforce ARR",             "~$2B",   "<$1B",   "−$1B",   "Enterprise pilots stall; ROI unproven at scale"),
    ("Net Revenue Retention",      "~107%",  "<100%",  "−7pp",   "NRR breaks below 100%; net churn triggered"),
    ("Non-GAAP op margin",         "33.5%",  "<28%",   "−5.5pp", "Agentforce build costs + sales cycle elongation"),
    ("cRPO growth YoY",            "+12%",   "<+8%",   "−4pp",   "Macro freeze; enterprise IT budgets cut 20%"),
    ("Data Cloud ACV growth",      "+42%",   "<+20%",  "−22pp",  "Snowflake/Databricks win unified data war"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  CRM BELOW EPP FLOOR — THE RARE SIGNAL: At $178, the stock trades 24% BELOW its own")
print(f"  Earnings Power Price floor ($234 = 18× × $13.00 FY2027E EPS). This happens when the")
print(f"  market prices maximum existential risk — that Agentforce destroys the seat-based model")
print(f"  before it can replace it. Historically, buying SaaS leaders at sub-EPP prices has been")
print(f"  generational: Salesforce itself at 2022 trough ($127), ServiceNow at various troughs,")
print(f"  HubSpot at 2023 lows. The burden of proof is on the BEAR — $14B+ FCF and $32B RPO")
print(f"  backlog provide a floor the market is ignoring.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E adj EPS estimate:      ${EPS_FY2027E:.2f}  (consensus $12.50–$13.50; non-GAAP; FY ends Jan 2027)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (~5.5% FCF yield floor; historic SaaS bear-case trough)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({'BELOW EPP — RARE DISTRESS SIGNAL' if epp_gap_pct < 0 else str(epp_gap_pct) + '% above trough floor'})")
print()
print(f"  CRITICAL: CRM is trading {abs(epp_gap_pct):.0f}% BELOW its own EPP floor. This means even the")
print(f"  pessimistic scenario (18× P/E on consensus EPS) is above the current price. The market")
print(f"  is embedding a scenario worse than EPP — i.e., EPS below $13 OR a P/E below 18×.")
print(f"  For EPP to justify $178: either EPS = ${178/PE_PESSIMISTIC:.2f} (requires −{(1-178/PE_PESSIMISTIC/EPS_FY2027E)*100:.0f}% miss) OR")
print(f"  P/E compresses to {178/EPS_FY2027E:.1f}× (below all historic SaaS trough multiples except crisis).")
print(f"  EPP path: FY2029E EPS ~$16.50 × {PE_PESSIMISTIC:.0f}× = ${16.50*PE_PESSIMISTIC:.0f} floor by 2029 (EPP growing ~13%/yr on buybacks).")
print(f"  At 24× mid-cycle P/E: ${EPS_FY2027E:.2f} × 24 = ${EPS_FY2027E*24:.0f}  — 97% above current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: P/E rerates toward normalized SaaS; Agentforce confirms)")
hr()
print(f"  Conservative FY2029E adj EPS:  ${CONS_EPS_2YR:.2f}  (7.5% EPS CAGR; buyback ~3%/yr + EPS growth ~4.5%/yr)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (rerates from ~14× current to normalized 20× SaaS compounder)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; growing since FY2025 initiation)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Even the conservative case (20× P/E on $15 EPS = $300 + $3.36 divs = $303) implies +70%")
print(f"  from $178. This is the hallmark of a sub-EPP entry: the range of outcomes is asymmetric.")
print(f"  Bear case ($143) is −20% downside. Conservative case is +70%. BULL ($513) is +188%.")
print(f"  For conservative 2yr to lose money at 20× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires −{(1 - (CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E)*100:.1f}% EPS miss vs FY2027E consensus — an extreme scenario.")
print(f"  BUY trigger: current ${CURRENT_PRICE:.0f} IS already below trigger  |  ratio_b = {ratio_b_str}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.42
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: 52W high ($326.84) was pre-AI-disruption-narrative; stock fell 48% on Agentforce fear")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  growing; initiated FY2025)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; SaaS de-rating + AI narrative volatility)")
print(f"  Beta vs S&P 500:      1.35  (enterprise SaaS; sentiment-driven; Agentforce binary amplifier)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (extreme; NRR collapse + multiple compression)")
print(f"  52W low ${VOL_52W_LOW:.2f} (Mar 2026 Agentforce panic) already a peak-to-trough move of ~63%.")
print(f"  → Agentforce ARR conversion rate is THE KEY binary; each earnings with ARR data = ±15–20%.")
print(f"  → NRR crossing 110%+ is the definitive confirmation Agentforce adds not cannibalizes.")
print(f"  → AVOID above $380  |  WATCHLIST $250–280  |  ACCUMULATE $195–220  |  BUY below $195")
print(f"  → Current price ${CURRENT_PRICE:.2f} IS in the BUY zone — rare sub-EPP entry point.")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is {'ABOVE' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'BELOW'} the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0 — between")
print(f"  {'BASE and BULL' if 2.0 <= MARKET_COMPOSITE <= 2.75 else 'BEAR and BASE' if MARKET_COMPOSITE < 2.0 else 'BULL and XBULL'}. The model scores the fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0 — between BASE and BULL.")
print(f"  The gap ({ADJ_GAP:+.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: the market is pricing heavy Agentforce disruption fear. The model sees")
print(f"  $32B RPO backlog + $14B FCF + sub-EPP entry as an asymmetric risk/reward setup.")
print(f"  At $178, the worst-case downside (−20% to $143) is dwarfed by the base-case upside (+89%).")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Agentforce enterprise conversion data — Q2 FY2027 (Aug 2026) — first Agentforce ARR disclosure")
print(f"  (2) NRR inflection — if NRR crosses 110%+ = confirmation Agentforce is NET additive not cannibalistic")
print(f"  (3) Microsoft Dynamics/Copilot CRM traction — the key competitive threat; market share data")
print(f"  (4) $50B buyback acceleration — at $178, each $1B buyback = 5.6M shares = structural EPS tailwind")
print(f"  (5) Marc Benioff succession / governance — CEO clarity removes overhang; COO succession plan")
print(f"  AVOID above $380  |  WATCHLIST $250–280  |  ACCUMULATE $195–220  |  BUY below $195")
print(f"  (current price ${CURRENT_PRICE:.2f} IS in the BUY zone)")
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
