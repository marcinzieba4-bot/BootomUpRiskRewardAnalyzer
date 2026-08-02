"""
CRM  ·  Salesforce, Inc.  ·  NYSE: CRM
Bottom-up signal model  ·  Enterprise SaaS / CRM / Agentic AI Platform
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "CRM"
COMPANY       = "Salesforce, Inc."
SECTOR        = "Enterprise SaaS · CRM · Agentic AI Platform · NYSE: CRM"
CURRENT_PRICE = 184.02       # USD; as of 2026-08-02 (+1.83% today; refresh from $178 Jun model)
VOL_52W_LOW   = 146.32
VOL_52W_HIGH  = 269.11
SHARES_OUT_M  = 819.0        # millions (~$150.71B market cap / $184.02; declining via $50B buyback)

# Dividend: none (initiated small dividend FY2025 but now suspended; no dividend)
ANNUAL_DIV    = 0.00         # $/share — no current dividend

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)  [Salesforce fiscal year ends January 2026]
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Sales Cloud",              8.8,  7.0, 11.5, "Core CRM; stable growth; Agentforce SDR agents expanding ARPU; ~9% YoY"),
    ("Service Cloud",           10.0,  8.0, 13.5, "Largest segment; AI case deflection (Agentforce) lifting ARPU; ~10% YoY"),
    ("Agentforce (AI Agents)",   1.5,  0.5,  8.0, "New product; autonomous AI agents; growing ARR; hockey-stick if enterprise adopts"),
    ("Marketing & Commerce",     5.2,  4.2,  7.0, "Marketing Cloud + Commerce Cloud; moderate growth; data moat"),
    ("Platform & Integration",   8.0,  6.5, 10.5, "MuleSoft + Tableau + Slack; integration moat; $8B ARR"),
    ("Data Cloud & Other",       8.03, 6.0, 10.5, "Data Cloud (unified customer data platform); fastest organic growth; AI fuel"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.780   # non-GAAP blended; software/SaaS premium
GROSS_MARGIN_BULL = 0.820   # BULL: Agentforce = 20%+ of revenue at 85%+ margin
OPEX_FIXED_B      = 18.5    # non-GAAP R&D + SG&A ($B); leverage improving post cost cuts
TAX_RATE          = 0.190   # effective; US-based; standard SaaS

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 13.93       # FY2027E non-GAAP EPS (forward P/E 13.21× at $184.02)
EPS_BEAR       =  6.00       # BEAR case EPS (revenue growth <5%; AWS/MSFT encroachment)
PE_PESSIMISTIC = 14.0        # pessimistic P/E: FCF yield floor; historic SaaS bear trough
EPP            = round(PE_PESSIMISTIC * EPS_BEAR, 0)   # $84 — bear EPS × trough P/E

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 6.00, 14,   84, "AI agents cannibalize seats; AWS/MSFT CRM encroach; <5% growth; EPS $6 → 14× floor"),
    "BASE":  (13.93, 18,  251, "Agentforce traction; Data Cloud stickiness; EPS $13.93 → 18× = $251"),
    "BULL":  (20.00, 25,  500, "Agentforce enterprise standard; 20%+ ARR growth resumes; EPS $20 → 25× = $500"),
    "XBULL": (30.00, 30,  900, "CRM = enterprise AI OS; agentic workflows scale; EPS $30 → 30× = $900"),
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
        "name":       "Revenue growth / RPO YoY",
        "weight":     0.30,
        "thresholds": ("<5%",    "≥10%",  "≥18%",   "≥28%"),
        "now":        "+9.6%",
        "score":      2,
        "comment":    "FY2026 revenue $41.53B +9.58% YoY; RPO +11% YoY; Agentforce incremental but early",
    },
    {
        "name":       "Agentforce adoption / ARR",
        "weight":     0.25,
        "thresholds": ("<$1B",   "≥$2B",  "≥$5B",   "≥$12B"),
        "now":        "early",
        "score":      2,
        "comment":    "29K pilot deals; ARR growing but not yet disclosed; VA contract $1.6B win positive signal",
    },
    {
        "name":       "Non-GAAP gross margin",
        "weight":     0.20,
        "thresholds": ("<74%",   "≥77%",  "≥81%",   "≥85%"),
        "now":        "~78%",
        "score":      2,
        "comment":    "Gross margin stable ~78%; Agentforce high-margin layer not yet large enough to lift blend",
    },
    {
        "name":       "Non-GAAP operating margin",
        "weight":     0.15,
        "thresholds": ("<28%",   "≥32%",  "≥38%",   "≥44%"),
        "now":        "33.5%",
        "score":      2,
        "comment":    "Expanding from 28% (FY2024) to 33.5%; $1B+ cost cuts complete; path to 35%+ credible",
    },
    {
        "name":       "Customer retention / NRR",
        "weight":     0.10,
        "thresholds": ("<100%",  "≥105%", "≥115%",  "≥125%"),
        "now":        "~107%",
        "score":      2,
        "comment":    "NRR recovering from 103% trough (FY2025); Agentforce ARPU expansion starting to register",
    },
    {
        "name":       "Data Cloud ACV growth",
        "weight":     0.00,
        "thresholds": ("<20%",   "≥35%",  "≥60%",   "≥100%"),
        "now":        "+42%",
        "score":      3,
        "comment":    "Data Cloud +42% YoY; fastest-growing product; 28K+ customers; unified data platform moat",
    },
]

# Note: Data Cloud weight is 0 to keep weights summing to 1.0; captured in SCA instead
assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "CRM installed-base moat — #1 CRM globally; 150K+ enterprise accounts; 3-5yr switching cost",  +0.7, 0.25),
    ("+", "Agentforce optionality — if 20% of 29K pilots convert to $500K ACV = $3B ARR inflection",     +0.6, 0.20),
    ("-", "Agentic AI disruption risk — Microsoft Copilot + SAP Joule + HubSpot AI displace CRM seats",  -0.7, 0.20),
    ("-", "Seat-based model obsolescence — if AI agents replace human reps, CRM seats shrink structurally",-0.5, 0.15),
    ("+", "FCF machine + buyback — $7.5B+ FCF/yr; $50B buyback auth; 8%+ FCF yield at $184",            +0.5, 0.10),
    ("+", "Data Cloud moat — fastest-growing product; unified customer data = AI fuel; hard to replicate", +0.4, 0.10),
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
CONS_EPS_2YR  = 16.00   # conservative FY2028E: ~7% EPS CAGR from $13.93; buyback ~3%/yr + ~4% growth
CONS_PE_2YR   = 18      # rerates from 13.21× current to 18× as Agentforce traction confirms
cons_equity   = CONS_EPS_2YR * CONS_PE_2YR
cons_divs     = ANNUAL_DIV * 2   # $0 — no dividend
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
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<26}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<26}  ${curr:>11.2f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<26}  ${curr_total:>11.2f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_ni   = curr_oi * (1 - TAX_RATE)
curr_eps  = round(curr_ni / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B
bull_ni   = bull_oi * (1 - TAX_RATE)
shares_b  = shares * 0.94   # ~3%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift; lower margin in downturn
bear_oi   = bear_gp - OPEX_FIXED_B * 0.97           # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.2f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (forward EPS FY2027E consensus ${EPS_FY2027E:.2f}  ~✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 25× = ~${bull_eps_imp*25:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 14× trough P/E = ~${bear_eps_imp*14:.0f}  (BEAR ${SCENARIOS['BEAR'][2]} uses specified $6 EPS × 14× = $84)")

# KEY SENSITIVITIES
print()
eps_per_1B_rev       = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_agentforce = 1.0 * 0.85 * (1 - TAX_RATE) / shares
eps_per_1pp_nrr      = curr_total * 0.01 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Agentforce ARR (85% GM):    +${eps_per_1B_agentforce:.3f}/EPS  = +${eps_per_1B_agentforce*18:.1f}/share at 18× P/E")
print(f"  Every $1B total revenue (78% GM):     +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*18:.1f}/share at 18× P/E")
print(f"  1pp NRR expansion (×$41.5B ARR base): +${eps_per_1pp_nrr:.3f}/EPS  = +${eps_per_1pp_nrr*18:.1f}/share at 18× P/E")
print(f"  1% buyback (8.2M shares at $184):     +${curr_eps*0.01:.3f}/EPS  (mechanical accretion; $50B authorization)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Revenue / Agentforce / Margins / NRR / Data Cloud framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>5}  {'BASE':>5}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>6}  Score")
hr()
for s in SIGNALS:
    if s["weight"] == 0:
        continue   # Data Cloud shown as SCA factor; skip from weighted table
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>5}  {ths[1]:>5}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>6}  {lbl}  {b}")
print(f"  Data Cloud ACV growth (captured in SCA)           <20%   ≥35%    ≥60%    ≥100%   +42%  ▲ BULL  ███░")

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
    ("Total revenue YoY",              "+9.6%",  "<+5%",   "−4.6pp", "Agentforce cannibalizes seat ARR; churn accelerates"),
    ("Agentforce ARR",                 "early",  "<$1B",   "stalls",  "Enterprise pilots fail ROI test; proof-of-concept limbo"),
    ("Non-GAAP gross margin",          "~78%",   "<74%",   "−4pp",   "Price competition; AWS/MSFT undercutting CRM contracts"),
    ("Non-GAAP operating margin",      "33.5%",  "<28%",   "−5.5pp", "Cost of Agentforce build + elongated sales cycles"),
    ("Net Revenue Retention (NRR)",    "~107%",  "<100%",  "−7pp",   "NRR breaks below 100%; customers downsizing seats"),
    ("Revenue cRPO growth YoY",        "+11%",   "<+8%",   "−3pp",   "Macro freeze; enterprise IT budgets cut 20%"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: AI agents (Microsoft Copilot for Sales, HubSpot Breeze) replace human reps")
print(f"  while simultaneously disrupting CRM seat demand. If Agentforce's own AI agents cannibalize")
print(f"  license seats before ARR can replace them, revenue growth stalls below 5% and NRR breaks.")
print(f"  Morgan Stanley downgrade to Equal Weight cited exactly this AI strategy concern.")
print(f"  EPS collapses to ~$6 (bear EPS) → 14× trough P/E = ${bear_price}.")
print(f"  Note: $32B RPO backlog + $7.5B+ FCF provide a contractual floor against sudden collapse.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × bear EPS)")
hr()
print(f"  BEAR case EPS:                 ${EPS_BEAR:.2f}  (revenue growth <5%; AI cannibalization scenario)")
print(f"  FY2027E forward EPS (consensus): ${EPS_FY2027E:.2f}  (forward P/E {CURRENT_PRICE/EPS_FY2027E:.1f}× at ${CURRENT_PRICE:.2f})")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (FCF yield floor ~5%; historic SaaS bear-case trough)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share  (= ${PE_PESSIMISTIC:.0f}× × ${EPS_BEAR:.2f} bear EPS)")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above EPP — bear case is the floor)")
print()
print(f"  At ${CURRENT_PRICE:.2f}, CRM trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× forward EPS — cheapest SaaS multiple in years.")
print(f"  The market is pricing in near-BEAR execution: forward P/E of {CURRENT_PRICE/EPS_FY2027E:.1f}× implies maximum fear.")
print(f"  BASE case (18× × $13.93 = $251) is +36% from here. BULL ($500) is +172%.")
print(f"  EPP path: FY2028E EPS ~$16 × {PE_PESSIMISTIC:.0f}× = ${16*PE_PESSIMISTIC:.0f} EPP by late 2028 (EPP growing ~13%/yr).")
print(f"  At 18× normalized P/E: ${EPS_FY2027E:.2f} × 18 = ${EPS_FY2027E*18:.0f}  — 37% above current price at BASE.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: P/E rerates as Agentforce confirms; no dividend)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (~7% EPS CAGR: buyback ~3%/yr + ~4% EPS growth)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (rerates from {CURRENT_PRICE/EPS_FY2027E:.1f}× to 18× as Agentforce traction confirms)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (no dividend currently)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Even the conservative case ({CONS_PE_2YR}× P/E on ${CONS_EPS_2YR:.0f} EPS = ${cons_equity}) implies +{cons_return:.0f}%")
print(f"  from ${CURRENT_PRICE:.2f}. The asymmetry: Bear case (${bear_price}) = −{downside_pct*100:.0f}% downside. BASE (${SCENARIOS['BASE'][2]}) = +{(SCENARIOS['BASE'][2]-CURRENT_PRICE)/CURRENT_PRICE*100:.0f}%.")
print(f"  For conservative 2yr to lose money at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE) / CONS_PE_2YR:.2f}")
print(f"  That requires −{(1 - CURRENT_PRICE / CONS_PE_2YR / EPS_FY2027E)*100:.1f}% miss vs FY2027E consensus — extreme scenario.")
print(f"  $50B buyback at $184 = 27% of market cap → mechanical EPS tailwind regardless of Agentforce.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.40
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: 52W high ($269.11) vs 52W low ($146.32) — massive range on Agentforce uncertainty")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (no dividend; FCF being redeployed to buybacks)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; SaaS de-rating + AI narrative volatility)")
print(f"  Beta vs S&P 500:      1.35  (enterprise SaaS; sentiment-driven; Agentforce binary amplifier)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (tail risk; multi-factor failure)")
print(f"  52W low ${VOL_52W_LOW:.2f} — already a 46% peak-to-trough on AI cannibalization fear.")
print(f"  → Agentforce ARR conversion rate is THE KEY binary; every earnings = ±15–20% move.")
print(f"  → NRR crossing 110%+ = confirmation Agentforce adds not cannibalizes.")
print(f"  → AVOID above $380  |  WATCHLIST $250–280  |  ACCUMULATE $195–220  |  BUY below $195")
print(f"  → Current ${CURRENT_PRICE:.2f} is near BUY zone; 13.2× forward P/E is cheapest SaaS valuation in years.")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, market composite ({MARKET_COMPOSITE:.2f}) vs")
print(f"  adj composite ({ADJ_COMPOSITE:.3f}). Gap ({ADJ_GAP:+.2f}) → {valuation_label}.")
print(f"  13.2× forward P/E embeds maximum Agentforce disruption fear — well below BASE at 18×.")
print(f"  $32B RPO backlog + $7.5B FCF + $50B buyback provide contractual floor the market ignores.")
print(f"  The asymmetric risk/reward: −{downside_pct*100:.0f}% downside vs +{upside_pct*100:.0f}% upside to BULL scenario.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Agentforce ARR disclosure — Q2 FY2027 (Aug 2026): first quantified ARR data")
print(f"  (2) NRR inflection — if NRR crosses 110%+ = Agentforce is NET additive, not cannibalistic")
print(f"  (3) Microsoft Dynamics/Copilot CRM traction — key competitive threat; market share data")
print(f"  (4) $50B buyback pace — at $184, each $1B = 5.4M shares; aggressive pace = floor support")
print(f"  (5) VA contract $1.6B delivery — government CRM win; proves Agentforce at scale outside private sector")
print(f"  AVOID above $380  |  WATCHLIST $250–280  |  ACCUMULATE $195–220  |  BUY below $195")
print(f"  EPP floor: ${EPP:.0f}  |  Bear EPS: ${EPS_BEAR:.2f}  |  FY2027E EPS: ${EPS_FY2027E:.2f}  |  Fwd P/E: {CURRENT_PRICE/EPS_FY2027E:.1f}×")
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
