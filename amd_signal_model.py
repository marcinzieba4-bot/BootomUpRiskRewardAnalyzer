"""
AMD  ·  Advanced Micro Devices, Inc.  ·  NASDAQ: AMD
Bottom-up signal model  ·  AI Accelerators (MI400/Helios) / Data Center / Client / Gaming
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "AMD"
COMPANY       = "Advanced Micro Devices, Inc."
SECTOR        = "AI Accelerators · Data Center GPU/CPU · Client · Gaming · NASDAQ: AMD"
CURRENT_PRICE = 476.15       # USD; close 2026-07-31 (verified live)
VOL_52W_LOW   = 149.22       # 2025 AI-capex-scare trough
VOL_52W_HIGH  = 584.73       # 2026 MI400/Helios hyperscaler-deal euphoria peak
SHARES_OUT_M  = 1_630.0      # millions; $776.4B mkt cap / $476.15; modest dilution from equity comp
ANNUAL_DIV    = 0.0          # $/share — all FCF reinvested in the AI roadmap / buybacks

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ─────────────────────────────────────
# Q1 2026 actual: total revenue $10.3B (+38% YoY); Data Center $5.8B (+57%)
# Q2 2026 guide (reports Aug 4, 2026 — after this refresh): ~$11.2B (+46% YoY)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Data Center (EPYC + Instinct GPU)", 27.5, 18.0, 46.0, "MI400/Helios ramp is the entire thesis; OpenAI + Meta each committed up to 6GW"),
    ("Client (Ryzen)",                    11.0,  8.5, 14.5, "PC refresh cycle + AI-PC mix shift; share gains against Intel continue"),
    ("Gaming (Radeon + semi-custom)",      6.5,  5.0,  8.0, "Console semi-custom cyclical; discrete GPU a smaller, steadier piece"),
    ("Embedded (Xilinx)",                  3.5,  3.0,  4.5, "Industrial/aerospace/comms; still working through post-acquisition digestion"),
]

# Margin assumptions (non-GAAP)
GROSS_MARGIN_CURR = 0.478   # FY2026E blended non-GAAP gross margin; Data Center GPU mix still dilutive early in the ramp
GROSS_MARGIN_BULL = 0.560   # BULL: MI400/Helios reach scale, software stack (ROCm) improves attach economics
OPEX_FIXED_B      = 9.5     # R&D + SG&A ($B); heavy AI roadmap investment
TAX_RATE          = 0.140   # non-GAAP effective tax rate

# ── HYPERSCALER COMMITMENT CALCULATOR (the AMD-specific angle) ───────────────
OPENAI_COMMIT_GW   = 6.0    # GW committed by OpenAI, multi-year Helios deployment
META_COMMIT_GW     = 6.0    # GW committed by Meta, multi-year deployment (~$60B combined value cited)
COMBINED_VALUE_B   = 60.0   # $B approximate combined multi-year value of the two anchor deals
Q1_DC_REV_B        =  5.8   # $B Q1 2026 Data Center revenue (+57% YoY)
Q2_GUIDE_B         = 11.2   # $B total revenue guide for Q2 2026 (+46% YoY) — reports Aug 4, after this refresh
HELIOS_SHIP_QTR    = "Q3 2026"  # first Helios rack shipments

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 7.20        # $/share non-GAAP FY2026E; Q1 actual $1.37 (+43%), full-year ramping on Data Center
PE_PESSIMISTIC = 22.0        # trough P/E: AMD traded in the low-20s forward during the 2025 AI-capex
                             # scare; 22x prices a real air pocket without assuming the AI story is dead
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 3.61, 18,   65, "Data Center growth stalls (not collapses); mix and opex compress margin; multiple resets"),
    "BASE":  ( 9.35, 28,  262, "Helios ramps on schedule; Data Center compounds ~35%/yr; margin expands to ~50%"),
    "BULL":  (15.95, 34,  543, "OpenAI/Meta commitments convert on schedule; AMD takes durable #2 AI-accelerator share"),
    "XBULL": (21.50, 38,  817, "MI500 (2027) extends the roadmap lead; AMD becomes co-equal with Nvidia in merchant AI silicon"),
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
        "name":       "Data Center revenue YoY growth",
        "weight":     0.30,
        "thresholds": ("<25%",   "≥40%",   "≥60%",   "≥85%"),
        "now":        "+57%",
        "score":      3,
        "comment":    "Q1 2026 $5.8B (+57%); Q2 guide $11.2B total implies continued sequential acceleration",
    },
    {
        "name":       "Hyperscaler multi-year commitments",
        "weight":     0.20,
        "thresholds": ("<2GW",   "≥4GW",  "≥8GW",   "≥15GW"),
        "now":        "~12GW",
        "score":      3,
        "comment":    "OpenAI 6GW + Meta up to 6GW, ~$60B combined value — genuinely large, but unproven at scale",
    },
    {
        "name":       "Total revenue YoY growth",
        "weight":     0.15,
        "thresholds": ("<15%",   "≥25%",   "≥38%",   "≥55%"),
        "now":        "+38%",
        "score":      3,
        "comment":    "Q1 $10.3B (+38%); Q2 guide $11.2B (+46% YoY) — accelerating, not just holding",
    },
    {
        "name":       "Non-GAAP gross margin",
        "weight":     0.15,
        "thresholds": ("<44%",   "≥48%",   "≥52%",   "≥56%"),
        "now":        "~48%",
        "score":      2,
        "comment":    "Data Center GPU mix is margin-dilutive early in the ramp; needs to expand as Helios scales",
    },
    {
        "name":       "Forward P/E vs the AI-hardware cohort",
        "weight":     0.10,
        "thresholds": (">60x",   "≤45x",  "≤32x",   "≤24x"),
        "now":        "66.1x",
        "score":      1,
        "comment":    "66.1× FY2026E — the richest multiple in this batch by a wide margin; priced for flawless execution",
    },
    {
        "name":       "Helios ramp execution (qualitative)",
        "weight":     0.10,
        "thresholds": ("delayed","on-track","ahead",  "sold-out"),
        "now":        "on-track",
        "score":      2,
        "comment":    "First racks shipping Q3 2026 as announced; no disclosed slippage yet, but nothing has shipped at scale either",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Anchor hyperscaler commitments — OpenAI + Meta, ~12GW combined, ~$60B value; not a hope, a signed book", +0.8, 0.20),
    ("+", "Data Center inflection — +57% YoY and accelerating into a Q2 guide well above the Street setup",         +0.7, 0.20),
    ("-", "Valuation — 66.1× forward EPS leaves almost no room for a ramp delay or a hyperscaler capex pause",      -1.0, 0.25),
    ("-", "Execution risk — MI400/Helios is unproven at the scale the commitments imply; software (ROCm) still trails CUDA", -0.6, 0.15),
    ("-", "Single-supplier concentration risk — two customers anchor most of the incremental Data Center growth",   -0.4, 0.10),
    ("+", "Client + Gaming diversification — a profitable, cash-generative base that doesn't need the AI story to work", +0.3, 0.10),
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
CONS_EPS_2YR  = 9.60    # conservative FY2028E: ~15.5% EPS CAGR — well below what BASE/BULL imply
CONS_PE_2YR   = 26      # multiple compresses hard from 66.1× toward a normal-growth-stock range
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  AI Accelerators / Data Center / Client / Gaming")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))
print(f"  ⚠ Q2 2026 earnings report Aug 4, 2026 — two days after this refresh. Figures below use")
print(f"  Q1 2026 actuals and the company's Q2 guide; treat Q2 guide as guidance, not a confirmed print.")

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<36}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<36}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<36}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  Q1 2026 actual: $10.3B total (+38%), Data Center $5.8B (+57%). Q2 guide: ~$11.2B (+46%)")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_eps  = round(curr_oi * (1 - TAX_RATE) / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B * 1.15
shares_b  = shares * 0.99
bull_eps_imp = round(bull_oi * (1 - TAX_RATE) / shares_b, 2)

bear_gp   = bear_total * 0.460     # margin compresses as Data Center mix shrinks back toward Client
bear_oi   = bear_gp - OPEX_FIXED_B * 0.95    # management trims opex growth in a real downturn
bear_eps_imp = round(max(0, bear_oi) * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex")
print(f"  − {TAX_RATE*100:.1f}% tax  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − opex, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 34× = ~${bull_eps_imp*34:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × 46.0% GM (Data Center mix shrinks back toward Client) − opex")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 18× trough = ~${bear_eps_imp*18:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")
print()
print(f"  ⚠ THE LEVERAGE POINT: Data Center is {SEG_DATA[0][1]/curr_total*100:.0f}% of FY2026E revenue but essentially")
print(f"  100% of the bear-to-bull swing. Client and Gaming are relatively stable, profitable")
print(f"  businesses on their own — the entire multiple is a bet on one segment's trajectory.")

# HYPERSCALER COMMITMENT CHECK
print()
print(f"  HYPERSCALER COMMITMENT CHECK  (the AMD-specific angle):")
print(f"  OpenAI commitment:             {OPENAI_COMMIT_GW:.0f}GW multi-year Helios deployment")
print(f"  Meta commitment:               up to {META_COMMIT_GW:.0f}GW multi-year deployment")
print(f"  Combined approximate value:    ~${COMBINED_VALUE_B:.0f}B across both deals")
print(f"  First Helios rack shipments:   {HELIOS_SHIP_QTR}")
print()
print(f"  These are the two commitments underwriting the entire BULL/XBULL case. Neither has yet")
print(f"  converted into a full quarter of shipped, recognized Data Center revenue at the scale")
print(f"  implied by ~12GW of capacity. The gap between 'signed multi-year framework agreement'")
print(f"  and 'quarterly revenue run-rate' is exactly where AI-hardware theses have broken before —")
print(f"  it is the thing to track, not the headline GW number itself.")

# KEY SENSITIVITIES
print()
eps_per_1B_dc   = 1.0 * 0.58 * (1 - TAX_RATE) / shares    # Data Center incremental margin ~58%
eps_per_1pp_gm  = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Data Center revenue (58% inc. margin):  +${eps_per_1B_dc:.3f}/EPS  = +${eps_per_1B_dc*30:.2f}/share at 30× P/E")
print(f"  Every 1pp of blended gross margin:                +${eps_per_1pp_gm:.3f}/EPS  = +${eps_per_1pp_gm*30:.2f}/share at 30× P/E")
print(f"  Every 1 turn of P/E:                              ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")
print(f"  ↑ at 66.1× forward, small misses on either revenue or margin move the stock a lot")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Data Center growth / hyperscaler commitments / margin / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<42}  {'BEAR':>8}  {'BASE':>8}  {'BULL':>7}  {'XBULL':>8}  {'NOW':>8}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<42}  {ths[0]:>8}  {ths[1]:>8}  {ths[2]:>7}  {ths[3]:>8}  {s['now']:>8}  {lbl}  {b}")
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
print(f"  {'Signal':<32}  {'Current':>9}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Data Center revenue YoY",    "+57%",   "<25%",    "-32pp",  "OpenAI/Meta phase deployments slower than committed"),
    ("Hyperscaler commitments",    "~12GW",  "<4GW",    "-8GW",   "A committed deal is renegotiated or scaled back publicly"),
    ("Total revenue YoY",          "+38%",   "<15%",    "-23pp",  "Data Center deceleration drags the whole company down with it"),
    ("Non-GAAP gross margin",      "~56%",   "<50%",    "-6pp",   "GPU mix reverts to Client-heavy; pricing pressure from Nvidia"),
    ("Forward P/E",                "66.1x",  "≤20x",    "-54x",   "Multiple resets to a normal semiconductor-cycle range"),
    ("Helios ramp",                "on-track","delayed", "slip",  "Manufacturing, HBM supply, or software-stack delays push shipments out"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>9}  {bear_v:>9}  {move:>8}  {trigger[:46]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: AMD's bear case is not demand disappearing — it's demand arriving on a")
print(f"  slower schedule than a 66.1× multiple can tolerate. Two customers anchor most of the")
print(f"  incremental growth story; if either phases their Helios deployment over 4 years instead")
print(f"  of 2, the revenue is still coming but the stock re-rates hard in the meantime. This is a")
print(f"  timing risk wearing a demand-risk costume, and the multiple treats it as if it can't happen.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E non-GAAP EPS:       ${EPS_FY2026E:.2f}  (Q1 actual $1.37, +43% YoY; full-year ramping)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (AMD traded low-20s forward during the 2025 AI-capex scare)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP is the widest gap in this batch by a large margin. At")
print(f"  ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E non-GAAP EPS — a multiple that assigns")
print(f"  almost no probability to the ramp disappointing. The EPP floor itself (22× trough) is not")
print(f"  a distress multiple; it is roughly where AMD traded twelve months ago on a fraction of")
print(f"  today's Data Center revenue. The floor is real, but it is a long way down from here.")
print(f"  At a 40× 'still-growth-priced' multiple: ${EPS_FY2026E:.2f} × 40 = ${EPS_FY2026E*40:.0f}  ({(EPS_FY2026E*40/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: strong execution, but the multiple compresses hard)")
hr()
print(f"  Conservative FY2028E non-GAAP EPS:  ${CONS_EPS_2YR:.2f}  (~15.5% EPS CAGR — a fraction of the BULL case)")
print(f"  Conservative exit P/E:               {CONS_PE_2YR}×  (66.1× → 26×; a normal-growth-stock multiple)")
print(f"  Conservative equity value:            ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):        +${cons_divs:.2f}/share  (no dividend)")
hr()
print(f"  Conservative 2yr total:               ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:            {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE PROBLEM THIS MODEL FLAGS: even 15.5%/yr EPS growth — a very good outcome for almost")
print(f"  any company — produces a NEGATIVE conservative return here, because the multiple has to")
print(f"  come down from 66.1× to a still-generous 26×. AMD needs the BULL case, not just good")
print(f"  execution, to justify today's price. That is the definition of priced for perfection.")
print(f"  Breakeven at 26× requires FY2028E EPS ≥ ${CURRENT_PRICE / CONS_PE_2YR:.2f} — well above even the BASE-case path.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.55
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Round trip:            low $149 → high $585 → current ${CURRENT_PRICE:.2f}, a 3.9× peak-to-trough range in one year")
print(f"  Annual dividend:      none — all cash reinvested in the AI roadmap / buybacks")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (among the highest in large-cap tech; earnings-day moves of ±15% are routine)")
print(f"  Beta vs S&P 500:      1.85  (high-beta AI-capex proxy, more volatile than Nvidia on the same news)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (well within a single year's realized range for this stock)")
print(f"  → Q2 earnings (Aug 4, 2026) is the immediate catalyst — Data Center revenue vs the $11.2B guide.")
print(f"  → Any hyperscaler commentary on Helios deployment PACE (not just the GW headline) will move the stock.")
print(f"  → AVOID at current price  |  WATCHLIST $350–420  |  ACCUMULATE $260–310  |  BUY below $220")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f} the market composite is {MARKET_COMPOSITE:.2f}/4.0 — between BULL and")
print(f"  XBULL. The model's adjusted composite is {ADJ_COMPOSITE:.2f}/4.0, for a gap of {ADJ_GAP:+.2f} — {valuation_label.lower()}.")
print(f"  AMD's fundamentals are genuinely strong: +57% Data Center growth, ~12GW of anchor")
print(f"  commitments, and a real roadmap lead over the last AI-capex-scare cycle. None of that is")
print(f"  in dispute. What the model disputes is whether 66.1× forward earnings leaves room for")
print(f"  ANY of it to arrive slower than scheduled — and multi-year hyperscaler buildouts almost")
print(f"  always do. This is AVOID on price, not on the business: the ratio B math says the market")
print(f"  is already paying for a scenario better than this model's own BULL case delivers.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q2 2026 earnings (Aug 4) — Data Center revenue vs the $11.2B total-revenue guide")
print(f"  (2) Helios rack shipment cadence starting Q3 2026 — proof the timeline is real, not aspirational")
print(f"  (3) Gross margin trajectory — must expand as GPU mix scales, or the EPS bridge breaks")
print(f"  (4) Any hyperscaler commentary narrowing or reaffirming OpenAI/Meta deployment pace")
print(f"  (5) Nvidia competitive response — pricing or roadmap moves that pressure AMD's share gains")
print(f"  AVOID at ${CURRENT_PRICE:.2f}  |  WATCHLIST $350–420  |  ACCUMULATE $260–310  |  BUY below $220")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  Commitments: ~{OPENAI_COMMIT_GW+META_COMMIT_GW:.0f}GW")
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
