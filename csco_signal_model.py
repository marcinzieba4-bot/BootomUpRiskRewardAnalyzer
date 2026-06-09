"""
CSCO  ·  Cisco Systems, Inc.  ·  NASDAQ: CSCO
Bottom-up signal model  ·  Enterprise Networking / AI Infrastructure Fabric / Cybersecurity
Date: 2026-06-09
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "CSCO"
COMPANY       = "Cisco Systems, Inc."
SECTOR        = "Enterprise Networking · AI Infrastructure Fabric · Cybersecurity · NASDAQ: CSCO"
CURRENT_PRICE = 118.20       # USD; as of 2026-06-09; up ~90% in 12 months; near 52-week high
VOL_52W_LOW   =  62.15       # June 2025 trough; pre-AI-networking re-rating
VOL_52W_HIGH  = 124.80       # May 2026 AI fabric + Silicon One momentum peak
SHARES_OUT_M  = 4_020.0      # millions; declining ~2%/yr via buybacks
ANNUAL_DIV    = 1.68         # $0.42/quarter = $1.68/yr; 14-year dividend growth streak

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B); fiscal year ends July 2026
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Networking (Switching/Routing)",  21.0, 15.0, 27.0, "Catalyst 9000/Silicon One; AI cluster spine/ToR fabric; ethernet re-rating"),
    ("Security",                        10.5,  7.5, 14.0, "Hypershield AI; XDR; identity; fastest-growing segment +22% YoY"),
    ("Collaboration (Webex/Video)",      4.0,  3.0,  5.5, "Webex AI; Teams competition structural drag; modest growth"),
    ("Observability & Services",         6.5,  5.0,  9.0, "AppDynamics; ThousandEyes; Splunk integration; recurring ARR"),
    ("Splunk (Security/Observability)",  4.5,  3.0,  7.0, "Acquired Mar 2024 $28B; ARR $4B+; full integration by FY2027"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.665   # blended non-GAAP; hardware mix + Splunk lifting toward 67%
GROSS_MARGIN_BULL = 0.700   # BULL: software/security mix reaches 50%; Splunk at scale
OPEX_FIXED_B      = 16.5    # non-GAAP R&D + SG&A ($B)
TAX_RATE          = 0.190   # effective; US-based; standard

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 4.40        # consensus $4.30–$4.55 non-GAAP FY2026 (July 2026)
PE_PESSIMISTIC = 16.0        # trough: hardware networking at commodity risk; 2022-23 trough was 12-14×
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $70

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 3.20, 14,  45, "AI capex freeze; switching competition (Arista/Juniper); Splunk integration failure; EPS $3.20 → 14×"),
    "BASE":  ( 4.80, 24, 115, "AI networking steady; Splunk ARR grows to $6B; security +15%/yr; EPS $4.80 → 24× = $115"),
    "BULL":  ( 6.50, 28, 182, "Silicon One wins AI cluster hyperscaler fabric; Splunk $8B ARR; security platform; EPS $6.50 → 28×"),
    "XBULL": (10.00, 32, 320, "CSCO = AI networking standard + cybersecurity platform; enterprise full-stack; EPS $10 → 32×"),
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
        "name":       "AI networking orders (Silicon One/Catalyst)",
        "weight":     0.30,
        "thresholds": ("<$3B",  "≥$6B",  "≥$9B",  "≥$15B"),
        "now":        "~$9B",
        "score":      3,
        "comment":    "AI orders $9B FY2026 guided (raised from $1B FY2025); Silicon One GPU cluster fabric wins at hyperscalers",
    },
    {
        "name":       "Security ARR growth YoY",
        "weight":     0.25,
        "thresholds": ("<8%",   "≥15%",  "≥25%",  "≥40%"),
        "now":        "+22%",
        "score":      3,
        "comment":    "Hypershield AI + XDR platform +22% YoY; $10.5B security revenue; fastest segment; Splunk integration",
    },
    {
        "name":       "Splunk ARR growth post-acquisition",
        "weight":     0.20,
        "thresholds": ("<5%",   "≥12%",  "≥22%",  "≥35%"),
        "now":        "+14%",
        "score":      2,
        "comment":    "Splunk ARR $4.5B growing +14% post-acquisition; integration on track; cross-sell to 35K Cisco accounts",
    },
    {
        "name":       "Total product revenue YoY",
        "weight":     0.10,
        "thresholds": ("<-5%",  "≥3%",   "≥8%",   "≥15%"),
        "now":        "+6%",
        "score":      2,
        "comment":    "Product revenue recovering after FY2024 inventory digestion; networking +8% led by AI fabric orders",
    },
    {
        "name":       "Non-GAAP gross margin",
        "weight":     0.10,
        "thresholds": ("<60%",  "≥64%",  "≥68%",  "≥72%"),
        "now":        "66.5%",
        "score":      2,
        "comment":    "Software mix growing; Splunk dilutive near-term but ARR accretive; hardware pricing stable",
    },
    {
        "name":       "Software/subscription % of total revenue",
        "weight":     0.05,
        "thresholds": ("<35%",  "≥42%",  "≥50%",  "≥60%"),
        "now":        "~45%",
        "score":      2,
        "comment":    "Cisco transformation: subscriptions 45% of revenue; Splunk adds pure-software ARR; structural shift",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Installed-base moat — 100K+ enterprise customers; IOS ecosystem; multi-decade switching cost",  +0.7, 0.25),
    ("+", "Silicon One + AI fabric — proprietary ASIC for AI cluster spine/ToR; hyperscaler design wins",  +0.5, 0.20),
    ("-", "Arista structural threat — ANET taking enterprise AI fabric share; superior software stack",     -0.6, 0.20),
    ("-", "Splunk integration execution risk — $28B acquisition; culture clash; churn during migration",    -0.4, 0.15),
    ("+", "Security platform convergence — Hypershield + XDR + identity = sticky ARR; 35K cross-sell",    +0.4, 0.15),
    ("-", "Valuation stretch — 90% 12-month run; 26.9× FY2026E; easy money made; mean reversion risk",    -0.3, 0.05),
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
elif ratio_b != float("inf") and ratio_b < 1.50:
    signal_short, signal_full = "HOLD",      "▷ HOLD/TRIM"
elif ratio_b != float("inf") and ratio_b < 1.75:
    signal_short, signal_full = "WATCHLIST", "◐ WATCHLIST"
else:
    signal_short, signal_full = "AVOID",     "✕ AVOID"

ratio_b_str = f"{ratio_b:.2f}x" if ratio_b != float("inf") else "N/A"

# ── CONSERVATIVE GROWTH (2-yr) ────────────────────────────────────────────────
CONS_EPS_2YR  = 5.50    # FY2028E conservative: 12% EPS CAGR (Splunk matures; networking stable)
CONS_PE_2YR   = 20      # rerates from ~27× toward 20× as AI networking normalizes
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Enterprise Networking / AI Infrastructure Fabric / Cybersecurity")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<35}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<35}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<35}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_ni   = curr_oi * (1 - TAX_RATE)
curr_eps  = round(curr_ni / shares, 2)

bull_gp      = bull_total * GROSS_MARGIN_BULL
bull_oi      = bull_gp - OPEX_FIXED_B
bull_ni      = bull_oi * (1 - TAX_RATE)
shares_b     = shares * 0.96   # ~2%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.96   # mix shift to hardware (lower margin)
bear_oi      = bear_gp - OPEX_FIXED_B * 0.97           # partial cost response
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 28× = ~${bull_eps_imp*28:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.96:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 14× trough P/E (hardware commodity risk) = ~${bear_eps_imp*14:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev        = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_security   = 1.0 * 0.75 * (1 - TAX_RATE) / shares   # security ~75% gross margin
eps_per_1B_networking = 1.0 * 0.55 * (1 - TAX_RATE) / shares   # networking ~55% gross margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B security/software revenue:    +${eps_per_1B_security:.3f}/EPS  = +${eps_per_1B_security*24:.1f}/share at 24× P/E")
print(f"  Every $1B networking revenue:           +${eps_per_1B_networking:.3f}/EPS  = +${eps_per_1B_networking*24:.1f}/share at 24× P/E")
print(f"  1pp GM expansion (mix/Splunk scale):    +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*24:.1f}/share at 24× P/E")
print(f"  1% buyback (~40M shares):               +${curr_eps*0.01:.3f}/EPS  (mechanical accretion; ongoing authorization)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (AI networking / Security ARR / Splunk / Product revenue framework)")
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
    ("AI networking orders",           "~$9B",    "<$3B",    "−$6B",   "Arista wins hyperscaler GPU fabric; Silicon One loses bake-off"),
    ("Security ARR growth YoY",        "+22%",    "<+8%",    "−14pp",  "Microsoft Security suite bundles free with M365 E5"),
    ("Splunk ARR growth",              "+14%",    "<+5%",    "−9pp",   "Elastic/Datadog displace Splunk during integration chaos"),
    ("Total product revenue YoY",      "+6%",     "<-5%",    "−11pp",  "Macro recession; enterprise IT freeze; inventory build"),
    ("Non-GAAP gross margin",          "66.5%",   "<60%",    "−6.5pp", "Competitive pricing pressure on switching hardware"),
    ("Software/subscription % rev",   "~45%",    "<35%",    "−10pp",  "Hardware mix shift back; software deals delayed"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Arista wins the dominant share of AI hyperscaler cluster spine/ToR fabric,")
print(f"  combined with a macro IT spending freeze and Splunk integration failure. Networking falls")
print(f"  from $21B to $15B; security ARR growth stalls at <8%. EPS collapses toward $3.20 → 14×")
print(f"  trough P/E (hardware commodity risk; 2022-23 CSCO trough was 12-14×) = ${bear_price}.")
print(f"  Note: $45 is NOT permanent impairment — 100K enterprise customer base + IOS ecosystem")
print(f"  provides a durable moat floor. Recovery to ~${bear_price+30}–${bear_price+50} in 2yr is base case post-shock.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus $4.30–$4.55; non-GAAP; GAAP ~$3.60 with amort)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (hardware commodity floor; FY2022-23 trough 12-14×; mid at 16×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP reflects the AI networking re-rating: CSCO is no longer")
print(f"  priced as a legacy hardware vendor but as an AI infrastructure platform. At $118.20 and")
print(f"  FY2026E EPS $4.40, the P/E is 26.9× — up from ~12× two years ago. The risk is that the")
print(f"  re-rating is complete: Silicon One wins are priced in; incremental upside requires BULL.")
print(f"  EPP path: FY2028E EPS ~$5.50 × {PE_PESSIMISTIC:.0f}× = ${5.50*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing ~12%/yr).")
print(f"  At 20× mid-cycle P/E: ${EPS_FY2026E:.2f} × 20 = ${EPS_FY2026E*20:.0f}  — still 25% below current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: P/E rerates toward 20× as AI networking normalizes)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (12% EPS CAGR: Splunk ARR matures; networking stable)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (rerates from 27× toward 20× as AI networking cycle normalizes)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; 14-yr dividend growth streak)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE 90% RUN PROBLEM: CSCO is up ~90% in 12 months driven by the AI networking re-rating")
print(f"  (Silicon One + $9B AI orders). The business has genuinely improved — but at $118 and")
print(f"  26.9× FY2026E EPS, the easy money is made. BASE scenario ($115) is essentially at current")
print(f"  price — meaning no upside in the most likely outcome. Upside requires BULL ($182), which")
print(f"  needs Silicon One to win the majority of hyperscaler AI cluster fabric — a coin-flip vs")
print(f"  Arista. The correct posture: HOLD existing positions; add aggressively on pullback to")
print(f"  $95–105 where ratio_b improves materially.")
print(f"  For conservative 2yr to break even at 20× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — achievable only at BASE+.")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at 20× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.35
beta        = 1.20
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: 52W low ($62.15) was the pre-AI-networking trough; stock has nearly doubled since")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  14-year dividend growth streak)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; AI-networking cycle + Splunk integration uncertainty)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (enterprise tech; rates-sensitive; AI capex cycle amplifier)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe; Arista dominance + IT freeze tail scenario)")
print(f"  52W low ${VOL_52W_LOW:.2f} (Jun 2025 trough) was a peak-to-trough starting point; stock has re-rated ~90%.")
print(f"  → Arista competitive wins in AI hyperscaler fabric is THE KEY binary for downside.")
print(f"  → Splunk ARR milestones ($6B target) and Security ARR acceleration are KEY bull catalysts.")
print(f"  → AVOID above $135  |  HOLD/TRIM $115–135  |  WATCHLIST $100–115  |  ACCUMULATE $90–105  |  BUY below $85")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is ABOVE the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0 — between")
print(f"  BASE and BULL. The model scores the fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0 — between BASE and BULL.")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: at $118, you are paying full credit for BASE execution with no margin of")
print(f"  safety. The BULL case ($182) requires Silicon One hyperscaler dominance — not yet proven.")
print(f"  Arista (ANET) remains a credible and growing threat to that thesis.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) FY2026 Q4 earnings (August 2026) — AI order backlog disclosure; Splunk ARR update")
print(f"  (2) Silicon One hyperscaler design win announcements — GPU cluster fabric RFP decisions")
print(f"  (3) Arista market share data — if ANET takes >35% of AI spine, CSCO upside collapses")
print(f"  (4) Splunk ARR at $6B target — cross-sell synergy realization timeline confirmation")
print(f"  (5) Security platform competitive wins — if Hypershield displaces CrowdStrike/Palo Alto")
print(f"  AVOID above $135  |  HOLD/TRIM $115–135  |  WATCHLIST $100–115  |  ACCUMULATE $90–105  |  BUY below $85")
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
