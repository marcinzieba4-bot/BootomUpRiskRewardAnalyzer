"""
KNEBV  ·  KONE Corporation  ·  HEL: KNEBV
Bottom-up signal model  ·  Elevators & Escalators / Service / Modernisation
Date: 2026-06-01
NOTE: All prices in EUR (Helsinki Stock Exchange listing)
*** UPDATED: KONE + TK ELEVATOR COMBINATION ANNOUNCED 2026-04-29 ***
*** Largest ever Finnish corporate acquisition — €29.4B TKE deal ***
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "KNEBV"
COMPANY       = "KONE Corporation"
SECTOR        = "Elevators & Escalators · Service & Modernisation · Building Technology · HEL: KNEBV · Prices in EUR"
CURRENT_PRICE = 46.00        # EUR; 2026-06-01 (post-deal-announcement; deal announced 2026-04-29)
VOL_52W_LOW   = 38.20        # January 2026 trough (China property fears)
VOL_52W_HIGH  = 57.40        # July 2025 high (service growth re-rating)
SHARES_OUT_M  = 541.0        # millions standalone pre-close (270M new shares issued at deal close)
ANNUAL_DIV    = 1.78         # €/share FY2026; KONE committed to ~2026 level post-deal completion

# ── TKE DEAL CONSTANTS (announced 2026-04-29) ─────────────────────────────────
TKE_EV_B             = 29.4    # EUR bn total enterprise value for TKE
TKE_CASH_B           = 5.0     # EUR bn cash (Bank of America + BNP Paribas committed)
TKE_SHARES_NEW_M     = 270.0   # New KONE Class B shares → Advent/Cinven (33.8% post-deal, 18.3% votes)
TKE_DEBT_REFI_B      = 9.2     # EUR bn TKE net debt refinanced into new KONE balance sheet
TKE_COMBINED_REV_B   = 20.5    # EUR bn combined annual revenue (illustrative, last FY)
TKE_SERVICE_PCT      = 0.65    # 65% service post-deal (vs ~53% KONE standalone)
TKE_SYNERGIES_B      = 0.70    # EUR bn annual run-rate synergies (Year 3 post-close)
TKE_INTEGRATION_B    = 0.84    # EUR bn one-off integration costs (~1.2× synergies over ~2yr)
TKE_PRO_FORMA_SHARES = SHARES_OUT_M + TKE_SHARES_NEW_M   # 811M total post-close
TKE_CLOSE            = "Q2 2027"       # expected; subject to regulatory approvals
TKE_EGM              = "2026-06-03"    # KONE EGM to approve deal
TKE_NET_DEBT_B       = 12.0    # estimated pro-forma net debt post-close (EUR bn)
TKE_LEVERAGE_X       = 4.0     # ~4× net debt/EBITDA (Otis ~2.5×; Schindler ~0.5×)
KONE_STANDALONE_REV  = 12.0    # KONE FY2026E standalone revenue (EUR bn)
TKE_REV_B            = TKE_COMBINED_REV_B - KONE_STANDALONE_REV  # TKE standalone ~€8.5B

# ── CHINA vs SERVICE CONSTANTS ────────────────────────────────────────────────
MAINTENANCE_REV_B  = 5.0
MAINTENANCE_MARGIN = 0.22
MODERN_REV_B       = 1.4
MODERN_MARGIN      = 0.13
EMEA_NE_REV_B      = 3.8
EMEA_NE_MARGIN     = 0.08
CHINA_NE_REV_B     = 1.8
CHINA_NE_MARGIN    = 0.05
CHINA_NE_PEAK_B    = 4.2
TAX_RATE           = 0.23

# ── EPP (Earnings Power Price) ─────────────────────────────────────────────────
# Pre-close standalone EPP. Post-close combined EPP is lower (~€28-32) due to ~4× leverage
# reducing the minimum viable trough P/E from 20× standalone to ~14-16× for the leveraged entity.
EPP_EPS   = 2.10    # FY2026E standalone adj EPS (€); consensus €2.05–€2.20
PE_TROUGH = 20      # standalone trough P/E (2022-23 actual ~18-20×; service floor)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # €42 (standalone floor, pre-close)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIOS — UPDATED FOR COMBINED KONE+TKE ENTITY ─────────────────────────
# EPS on 811M post-close shares; prices reflect combined entity post-close
# Bear = antitrust block (standalone) OR integration failure (combined)
# Base/Bull/XBull = combined entity with varying synergy outcomes
SCENARIOS = {
    "BEAR":  (1.30, 14,  18, "Antitrust block or integration failure + China collapse; EPS €1.30 → 14× distress"),
    "BASE":  (2.10, 23,  48, "Close Q2 2027; synergies €500M by FY2028; combined EPS €2.10 → 23× mid-cycle"),
    "BULL":  (2.80, 25,  70, "Full €700M synergies; service 65%; >16% EBIT margin; EPS €2.80 → 25× premium"),
    "XBULL": (3.50, 28,  98, "Synergies exceed €900M; global #1 pricing power; Americas inflects; EPS €3.50 → 28×"),
}
# Note: €1.30×14=€18.2≈€18; €2.10×23=€48.3≈€48; €2.80×25=€70; €3.50×28=€98

# ── SOFTMAX ───────────────────────────────────────────────────────────────────
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

# ── 6 PROXY SIGNALS (standalone, pre-close) ───────────────────────────────────
SIGNALS = [
    {
        "name":       "China new equipment order intake — YoY growth",
        "weight":     0.25,
        "thresholds": ("<−20%",  "≥−15%", "≥+5%",  "≥+20%"),
        "now":        "−12%",
        "score":      2,
        "comment":    "−12% YoY; property starts still −20%/yr; floor forming; China exit via TKE deal reduces ongoing exposure",
    },
    {
        "name":       "Service + modernisation revenue — YoY organic growth",
        "weight":     0.25,
        "thresholds": ("<2%",    "≥4%",   "≥6%",   "≥9%"),
        "now":        "+6%",
        "score":      3,
        "comment":    "+6% YoY; 1.4M units under maintenance; modernisation backlog growing; pricing +3%",
    },
    {
        "name":       "Adjusted EBIT margin (reported, trailing 12m)",
        "weight":     0.20,
        "thresholds": ("<10%",   "≥11%",  "≥13%",  "≥15%"),
        "now":        "12.5%",
        "score":      2,
        "comment":    "12.5%; service mix improving; combined target >16% EBIT long-term post-synergies",
    },
    {
        "name":       "EMEA + Americas new equipment orders — YoY growth",
        "weight":     0.15,
        "thresholds": ("<−5%",   "≥+3%",  "≥+8%",  "≥+15%"),
        "now":        "+5%",
        "score":      2,
        "comment":    "+5% YoY; TKE deal adds Americas NE strength — KONE's weakest region historically",
    },
    {
        "name":       "Modernisation order backlog — YoY growth",
        "weight":     0.10,
        "thresholds": ("<0%",    "≥3%",   "≥8%",   "≥14%"),
        "now":        "+7%",
        "score":      2,
        "comment":    "+7% YoY; EU safety directive enforcement 2027; TKE adds modernisation scale",
    },
    {
        "name":       "KONE Connect — connected units in maintenance base (M cumulative)",
        "weight":     0.05,
        "thresholds": ("<0.4M",  "≥0.7M", "≥1.0M", "≥1.8M"),
        "now":        "1.2M",
        "score":      3,
        "comment":    "1.2M units; combined entity will have 2.5M+ connected units — digital moat step-change",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) — UPDATED FOR TKE DEAL ──────────────
# Weights restructured to incorporate deal factors (7 factors; weights sum to 1.00)
SCA_FACTORS = [
    ("+", "Service moat — combined 2.5M+ units post-deal; 90% renewal; pricing power at scale",       +0.8, 0.20),
    ("-", "China structural headwind — NE peak €4.2B → €1.8B; property crisis structural not cyclical",-0.8, 0.20),
    ("+", "TKE combination — global #1 (>Otis); Americas exposure; service 65%; 811M shares post-close",+0.6, 0.20),
    ("-", "Leverage risk — ~4× net debt/EBITDA post-close (Otis 2.5×; Schindler 0.5×); limits flex",  -0.8, 0.15),
    ("+", "Modernisation wave — 50% of 20M global elevators >20yr; EU safety reg; TKE backlog",        +0.6, 0.13),
    ("-", "Integration/regulatory execution risk — antitrust (EU/US); 100K employees; 2yr disruption", -0.4, 0.07),
    ("-", "EUR/HEL listing — lower liquidity vs NYSE; Herlin family control (>50% votes)",              -0.2, 0.05),
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
    valuation_label = "MODESTLY OVERVALUED"

# ── RATIO B ───────────────────────────────────────────────────────────────────
bear_price   = SCENARIOS["BEAR"][2]
bull_price   = SCENARIOS["BULL"][2]
downside_pct = (CURRENT_PRICE - bear_price) / CURRENT_PRICE
upside_pct   = (bull_price - CURRENT_PRICE) / CURRENT_PRICE
ratio_b      = round(downside_pct / upside_pct, 2)

if ratio_b < 0.75:
    signal_short, signal_full = "BUY",       "◉ BUY"
elif ratio_b < 1.10:
    signal_short, signal_full = "ACCUMULATE","◎ ACCUMULATE"
elif ratio_b < 1.75:
    signal_short, signal_full = "WATCHLIST", "◐ WATCHLIST"
else:
    signal_short, signal_full = "AVOID",     "✕ AVOID"

# ── CONSERVATIVE GROWTH (2-yr, post-deal close) ───────────────────────────────
# Deal closes Q2 2027; Year 1 post-close EPS on 811M shares; conservative 18× floor
CONS_EPS_2YR = 2.00    # FY2028E post-deal (partial synergies, 811M shares basis)
CONS_PE_2YR  = 18      # leveraged entity floor multiple (below standalone 20× due to ~4× debt)
cons_equity  = CONS_EPS_2YR * CONS_PE_2YR
cons_divs    = ANNUAL_DIV * 2
cons_total   = cons_equity + cons_divs
cons_return  = round((cons_total - CURRENT_PRICE) / CURRENT_PRICE * 100, 1)
cons_annual  = round(cons_return / 2, 1)

# ── PRO-FORMA EPS BRIDGE (computed, for display) ──────────────────────────────
# Combined EBIT at 13% margin on €20.5B: €2.665B
# Interest on ~€12B net debt at ~4%: ~€480M (declining as leverage falls)
# Net income post-tax = (EBIT - interest) × (1 - TAX_RATE)
# EPS on 811M post-close shares
COMBINED_EBIT_BASE = TKE_COMBINED_REV_B * 0.13   # 13% pre-synergy margin
PF_INTEREST_BASE   = TKE_NET_DEBT_B * 0.04        # ~4% blended rate

def pf_eps(synergies_b, debt_b=TKE_NET_DEBT_B, rate=0.04):
    ebit = COMBINED_EBIT_BASE + synergies_b
    interest = debt_b * rate
    ni = (ebit - interest) * (1 - TAX_RATE)
    return ni / (TKE_PRO_FORMA_SHARES / 1000)

# ─────────────────────────────────────────────────────────────────────────────
#  OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
W = 76

def hr(): print("  " + "─" * W)
def bar(score):
    return "█" * score + "░" * (4 - score)

shares_b      = SHARES_OUT_M / 1000
total_rev_b   = MAINTENANCE_REV_B + MODERN_REV_B + EMEA_NE_REV_B + CHINA_NE_REV_B
service_rev_b = MAINTENANCE_REV_B + MODERN_REV_B
svc_blend_mgn = (MAINTENANCE_REV_B * MAINTENANCE_MARGIN + MODERN_REV_B * MODERN_MARGIN) / service_rev_b

print()
print("═" * (W + 4))
print(f"  {TICKER}  ·  {COMPANY}  ·  €{CURRENT_PRICE:.2f}  ·  Elevators & Escalators / Service  [PRICES IN EUR]")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print(f"  *** KONE + TKE COMBINATION ANNOUNCED 2026-04-29 — scenarios updated for combined entity ***")
print("═" * (W + 4))

# ─── ① TKE DEAL ANALYSIS ──────────────────────────────────────────────────────
print()
print("  KONE + TK ELEVATOR (TKE) COMBINATION  (announced 2026-04-29)")
print("  Largest corporate acquisition in Finnish history  ·  Creates global #1 elevator maker")
hr()

pf_shares_b = TKE_PRO_FORMA_SHARES / 1000
print(f"  DEAL STRUCTURE:")
print(f"    TKE enterprise value              €{TKE_EV_B:.1f}B   (vs KONE standalone market cap ~€{CURRENT_PRICE * shares_b:.0f}B at €{CURRENT_PRICE})")
print(f"    Cash component (KONE pays)        €{TKE_CASH_B:.1f}B   (financed: Bank of America + BNP Paribas)")
print(f"    Share component (new shares)      €15.2B   ({TKE_SHARES_NEW_M:.0f}M new Class B shares → Advent/Cinven: 33.8%)")
print(f"    TKE net debt refinanced           €{TKE_DEBT_REFI_B:.1f}B   (becomes KONE debt; total pro-forma net debt ~€{TKE_NET_DEBT_B:.0f}B)")
hr()
print(f"    Post-deal shares outstanding      {TKE_PRO_FORMA_SHARES:.0f}M   (vs {SHARES_OUT_M:.0f}M standalone: +{(TKE_PRO_FORMA_SHARES/SHARES_OUT_M-1)*100:.0f}% dilution)")
print(f"    Pro-forma leverage                ~{TKE_LEVERAGE_X:.1f}×    net debt/EBITDA  (Otis ~2.5×; Schindler ~0.5×)")
print(f"    Expected close                    {TKE_CLOSE}  (subject to regulatory approvals + EGM {TKE_EGM})")
print()
print(f"  COMBINED ENTITY PROFILE:")
print(f"    Revenue                  €{TKE_COMBINED_REV_B:.1f}B  (KONE €{KONE_STANDALONE_REV:.1f}B + TKE ~€{TKE_REV_B:.1f}B)")
print(f"    Service % of revenue      {TKE_SERVICE_PCT*100:.0f}%   (vs KONE standalone {service_rev_b/total_rev_b*100:.0f}% — structural step-change)")
print(f"    Global position            #1    (surpasses Otis ~$20B revenue; European champion)")
print(f"    Americas (KONE gap)        ✓     (TKE strongest in Americas — KONE's historic weakness)")
print(f"    Synergies (run-rate, Yr3)  €{TKE_SYNERGIES_B:.2f}B  (network density, procurement, platform, SG&A)")
print()

print(f"  PRO-FORMA EPS BRIDGE  (all on {TKE_PRO_FORMA_SHARES:.0f}M post-close shares):")
print(f"  {'Phase':<38}  {'EBIT':>7}  {'Interest':>9}  {'Net inc':>8}  {'EPS':>6}  vs standalone")
hr()
pf_cases = [
    ("Year 1 post-close (0 synergies)",   0.00, 0.480),
    ("+€300M synergies (Year 1 partial)", 0.30, 0.460),
    ("+€500M synergies (Year 2)",         0.50, 0.440),
    ("Full €700M run-rate (Year 3)",      0.70, 0.420),
]
standalone_ni = EPP_EPS * SHARES_OUT_M / 1000  # approx standalone net income
for label, syn_b, int_b in pf_cases:
    ebit  = COMBINED_EBIT_BASE + syn_b
    ni    = (ebit - int_b) * (1 - TAX_RATE)
    eps   = ni / pf_shares_b
    vs_sa = (eps / EPP_EPS - 1) * 100
    marker = "  ← BULL case" if abs(syn_b - TKE_SYNERGIES_B) < 0.01 else ""
    print(f"  {label:<38}  €{ebit:.2f}B  €{int_b:.3f}B    €{ni:.2f}B  €{eps:.2f}  {vs_sa:+.0f}%{marker}")
hr()
int_cost_eps = (TKE_INTEGRATION_B / 2) * (1 - TAX_RATE) / pf_shares_b
yr1_adj_eps  = pf_eps(0.00)
yr1_rep_eps  = yr1_adj_eps - int_cost_eps
print(f"  Integration cost drag: ~€{int_cost_eps:.2f}/EPS per year (2yr) → Year 1 reported ≈ €{yr1_rep_eps:.2f}; adjusted ≈ €{yr1_adj_eps:.2f}")
print(f"  JPMorgan: upgraded to Overweight; PT raised €65→€70 on deal day (endorses BULL scenario ✓)")

print()
print(f"  SYNERGY BRIDGE  (€{TKE_SYNERGIES_B:.2f}B run-rate target; realised by Year 3 post-close):")
synergies = [
    ("Network density (shared service routes)",   0.250, 36),
    ("Procurement savings (scale)",               0.200, 29),
    ("Platform & R&D consolidation",              0.150, 21),
    ("SG&A overlap elimination",                  0.100, 14),
]
for name, val, pct in synergies:
    print(f"    {name:<42}  ~€{val:.3f}B  ({pct}%)")
print(f"    {'Total':<42}   €{TKE_SYNERGIES_B:.2f}B  (100%)  ·  one-off cost ~€{TKE_INTEGRATION_B:.2f}B over ~2yr")
print()
print(f"  ANTITRUST RISK  (creating world's #1 with combined ~25% global market share):")
print(f"  KONE confident in approvals; prepared to offer behavioral/geographic remedies if needed.")
print(f"  Probability: ~70% clean/behavioral close  |  ~20% material remedy (divestitures)  |  ~10% block")
print(f"  BEAR case embeds the block/integration failure scenario; BASE assumes clean/behavioral close.")

# ─── ② CHINA vs SERVICE: THE EARNINGS DRIVER COMPARISON ──────────────────────
print()
print("  STANDALONE THESIS: CHINA vs SERVICE  (still relevant pre-close; drives BEAR anatomy)")
hr()

total_ebit = (MAINTENANCE_REV_B * MAINTENANCE_MARGIN + MODERN_REV_B * MODERN_MARGIN +
              EMEA_NE_REV_B * EMEA_NE_MARGIN + CHINA_NE_REV_B * CHINA_NE_MARGIN)
total_ni   = total_ebit * (1 - TAX_RATE)
total_eps  = total_ni / shares_b

print(f"  KONE Revenue Architecture FY2026E:")
print(f"  {'Segment':<28}  {'Revenue':>8}  {'EBIT%':>7}  {'EBIT (€M)':>10}  of total")
hr()
segs = [
    ("Maintenance contracts", MAINTENANCE_REV_B, MAINTENANCE_MARGIN, "90% renewal; 7yr avg; pricing power"),
    ("Modernisation",         MODERN_REV_B,       MODERN_MARGIN,       "fastest-growing; aging installed base"),
    ("NE — EMEA/Americas",   EMEA_NE_REV_B,      EMEA_NE_MARGIN,      "recovering; infrastructure + resi"),
    ("NE — China",           CHINA_NE_REV_B,     CHINA_NE_MARGIN,     "−57% from €4.2B 2019 peak ◄ THE RISK"),
]
for name, rev, mgn, note in segs:
    ebit_m = rev * mgn * 1000
    print(f"  {name:<28}  €{rev:>5.1f}B    {mgn*100:>5.1f}%    €{ebit_m:>7.0f}M    {rev/total_rev_b*100:.0f}%")
hr()
print(f"  {'TOTAL':<28}  €{total_rev_b:>5.1f}B    {total_ebit/total_rev_b*100:>5.1f}%    €{total_ebit*1000:>7.0f}M    100%")
print(f"  After {TAX_RATE*100:.0f}% tax: €{total_ni:.3f}B net income  ÷  {SHARES_OUT_M:.0f}M shares = €{total_eps:.2f}/EPS (FY2026E)")
print()

china_full_recovery_eps = (CHINA_NE_PEAK_B - CHINA_NE_REV_B) * CHINA_NE_MARGIN * (1 - TAX_RATE) / shares_b
eps_per_1pct_service    = service_rev_b * 0.01 * svc_blend_mgn * (1 - TAX_RATE) / shares_b

print(f"  CHINA NE RECOVERY SENSITIVITY  (vs current depressed €{CHINA_NE_REV_B:.1f}B; 2019 peak €{CHINA_NE_PEAK_B:.1f}B):")
print(f"  {'China NE revenue':<24}  {'vs current':>10}  {'EBIT impact':>12}  {'EPS impact':>11}  Standalone EPS basis")
hr()
for china_rev in [2.5, 3.0, 3.5, CHINA_NE_PEAK_B]:
    delta_rev  = china_rev - CHINA_NE_REV_B
    delta_ebit = delta_rev * CHINA_NE_MARGIN
    delta_eps  = delta_ebit * (1 - TAX_RATE) / shares_b
    pct_pk = china_rev / CHINA_NE_PEAK_B * 100
    label = " ← PEAK" if china_rev == CHINA_NE_PEAK_B else ""
    print(f"  €{china_rev:.1f}B  ({pct_pk:.0f}% of peak)        +€{delta_rev:.1f}B       +€{delta_ebit*1000:.0f}M EBIT     +€{delta_eps:.2f}/EPS{label}")
print()
print(f"  Full China recovery: only +€{china_full_recovery_eps:.2f}/EPS — thin 5% NE margins neutralise the headline fear.")
cum7_5yr = sum(service_rev_b * ((1.07)**y - (1.07)**(y-1)) * svc_blend_mgn * (1-TAX_RATE) / shares_b for y in range(1,6))
print(f"  5yr of 7% service growth: +€{cum7_5yr:.2f}/EPS cumulative — {cum7_5yr/china_full_recovery_eps:.1f}× more valuable than full China recovery.")
print(f"  Note: TKE deal cuts China NE concentration to <9% of combined revenue (vs 15% standalone).")

# ─── ③ SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (pre-close standalone indicators; monitored until deal closes)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>6}  {'BASE':>5}  {'BULL':>5}  {'XBULL':>6}  {'NOW':>6}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>6}  {ths[1]:>5}  {ths[2]:>5}  {ths[3]:>6}  {s['now']:>6}  {lbl}  {b}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from €{CURRENT_PRICE} + 15% hurdle; new scenarios)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors (updated for TKE deal):")
for sign, desc, score, weight in SCA_FACTORS:
    c = score * weight
    print(f"    {sign}  {desc[:72]:<72}  ({score:+.1f} × {weight*100:.0f}%  =  {c:+.3f})")

# ─── ④ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR €{bear_price})")
hr()
print(f"  PRIMARY NEW RISK: ANTITRUST BLOCK or MATERIAL REMEDY")
print(f"  EU/US regulators may require divestiture of overlapping markets (est. ~20% probability).")
print(f"  Full block (~10%): KONE reverts to standalone bear with deal cost overhang.")
print(f"  Material remedy (~20%): reduced synergies, partial divestiture of European NE assets.")
print()
print(f"  SECONDARY TRIGGERS  (fundamental signals — still relevant for standalone health pre-close):")
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>7}")
hr()
bear_triggers = [
    ("China new equipment orders YoY",               "−12%",   "<−20%",  "−8pp"),
    ("Service + modernisation growth YoY",           "+6%",    "<2%",    "−4pp"),
    ("Adjusted EBIT margin",                         "12.5%",  "<10%",   "−2.5pp"),
    ("EMEA + Americas NE orders YoY",                "+5%",    "<−5%",   "−10pp"),
    ("Modernisation backlog growth",                 "+7%",    "<0%",    "−7pp"),
    ("KONE Connect connected units (M)",             "1.2M",   "<0.4M",  "−0.8M"),
]
for name, curr, bear_v, move in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  Bear €{bear_price}: ANTITRUST BLOCK forces standalone bear (China NE collapse + recession)")
print(f"  OR: Deal closes but integration chaos + synergy miss + leverage unsustainable → €{bear_price}.")
print(f"  Requires {downside_pct*100:.0f}% decline from €{CURRENT_PRICE}. Probability ~{probs_proxy['BEAR']*100:.0f}% (proxy) but binary event risk")
print(f"  makes distribution non-normal — antitrust headline can gap stock −15–25% in a session.")

# ─── ⑤ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price)  [EUR — standalone pre-close basis]")
hr()
print(f"  Pre-close standalone EPS:   €{EPP_EPS:.2f}  (FY2026E; consensus €2.05–€2.20)")
print(f"  Standalone trough P/E:       {PE_TROUGH}×  (2022-23 trough ~18-20×; service recurring revenue floor)")
print(f"  ─────────────────────────────────────────────────────────────────────────────────")
print(f"  Standalone EPP floor:    €{EPP:.0f}/share  (+{epp_gap_pct:.1f}% gap to current €{CURRENT_PRICE})")
print()
print(f"  POST-CLOSE EPP NOTE: Combined entity trough P/E ≈ 14-16× (leverage discount vs 20× standalone)")
combined_epp_eps  = pf_eps(0.0)           # Year 1, no synergies
combined_epp_low  = round(combined_epp_eps * 14, 0)
combined_epp_high = round(combined_epp_eps * 16, 0)
print(f"  Combined Year 1 EPS ~€{combined_epp_eps:.2f} × 14-16× → Post-close EPP range ~€{combined_epp_low:.0f}–€{combined_epp_high:.0f}/share")
print(f"  Bear €{bear_price} is BELOW both EPP measures — requires EPS collapse + multiple compression.")
print(f"  Service 65% post-deal provides a stronger recurring revenue floor than standalone.")
print(f"  EPP path: synergies ramp → EPS €2.80 (BULL) → EPP floor rises to €{round(2.80*16,0):.0f}–€{round(2.80*18,0):.0f} by Year 3.")

# ─── ⑥ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: deal closes Q2 2027; no synergy upside; 18× floor)")
hr()
print(f"  Conservative FY2028E EPS:  €{CONS_EPS_2YR:.2f}  (811M shares; Year 1 post-close; no synergies above baseline)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (leveraged entity floor; below standalone 20× due to ~4× debt)")
print(f"  Conservative equity value:  €{cons_equity:.2f}/share")
print(f"  + Cumulative dividends:    +€{cons_divs:.2f}/share  (€{ANNUAL_DIV:.2f} × 2; maintained per KONE commitment)")
hr()
print(f"  Conservative 2yr total:     €{cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from €{CURRENT_PRICE:.2f})")
print(f"  Conservative total return:  {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is NEGATIVE: deal dilution + lower trough P/E outweigh standalone growth.")
print(f"  Dividend (3.9% yield) cushions the decline but does not make conservative case positive.")
print(f"  Year 1 adjusted EPS ≈ €{yr1_adj_eps:.2f} (accretive on adjusted basis per KONE guidance ✓).")
print(f"  BUY trigger: <€{int(cons_total-1):.0f} (conservative 2yr total return >10% including dividend).")

# ─── ⑦ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT  [EUR]")
hr()
annual_vol  = 0.28   # higher post-deal (M&A arb + regulatory binary event adds uncertainty)
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 1),
               round(CURRENT_PRICE * (1 + annual_vol), 1))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        €{VOL_52W_LOW:.2f}  –  €{VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      €{ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%  —  maintained post-deal per company guidance)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated: deal uncertainty + regulatory binary + China)")
print(f"  Beta vs EuroStoxx:    0.85 standalone; ~1.0+ during M&A period (regulatory headline risk)")
print(f"  1-sigma range (1yr):  €{sigma_range[0]:.1f}  –  €{sigma_range[1]:.1f}  (€{CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear €{bear_price} requires:  ~{bear_sigmas:.1f}σ move  (antitrust headline could gap −15-25% in a session)")
print(f"  → Stock fell 3.3% day-1 post-announcement; recovered partially as JPMorgan PT €70 circulated.")
print(f"  → M&A arb premium: deal at ~18.3% vote discount (Herlin controls >50% — EGM approval certain).")
print(f"  → WATCHLIST €38–€50  |  BUY on antitrust clearance below €42  |  TRIM above €70")

# ─── ⑧ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print()
print("  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied; combined entity scenarios)")
hr()
probs_mkt = softmax_probs(MARKET_COMPOSITE)
print(f"  {'Scenario':<10}  {'Price':>6}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>7}  Description")
hr()
for s in ["BEAR","BASE","BULL","XBULL"]:
    pp   = probs_proxy[s] * 100
    pm   = probs_mkt[s]   * 100
    gap  = pp - pm
    pr   = SCENARIOS[s][2]
    desc = SCENARIOS[s][3][:50]
    print(f"  {s:<10}  €{pr:>5}  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): €{ev_adj:.0f}  /  Proxy EV: €{ev_prx:.0f}  /  Market EV: €{ev_mkt:.0f}  /  Current: €{CURRENT_PRICE:.0f}")
hr()
print(f"  Downside  (→ Bear €{bear_price}):   {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull €{bull_price}):    {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b:.2f}x")
print(f"  Signal    :  {signal_full}  (downgraded from ◎ ACCUMULATE — TKE deal adds execution + leverage risk)")
print()
print(f"  Market pricing ~{MARKET_COMPOSITE:.2f} composite — embedding significant BULL/synergy probability.")
print(f"  Model more cautious (gap {ADJ_GAP:+.2f}): leverage risk and integration uncertainty weigh on adj composite.")
print(f"  WATCHLIST does not reflect KONE quality concern — it reflects the binary deal execution event.")
print(f"  Upgrade path: antitrust clearance (regulatory) OR synergy confirmation (operating).")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts:")
print(f"  (1) EGM June 3, 2026 — shareholder vote on deal (Herlin >50% votes; outcome virtually certain)")
print(f"  (2) Regulatory approvals — EU/US antitrust; behavioral remedy = ACCUMULATE trigger;")
print(f"      structural divestiture = reduced synergies; block = revert to standalone bear")
print(f"  (3) Deal close Q2 2027 — first combined quarterly results → synergy run-rate confirmation")
print(f"  (4) Leverage trajectory — each 0.5× EBITDA deleveraging = ~1-2× P/E multiple expansion")
print(f"  (5) Service growth ≥7% pre-close → confirms standalone quality entering the combination")
print(f"  WATCHLIST €38–€50  |  BUY on antitrust clarity below €42  |  TRIM above €70  [ALL IN EUR]")
print("═" * (W + 4))
print()

# ── EXPORT ────────────────────────────────────────────────────────────────────
RESULT = {
    "ticker":           TICKER,
    "signal":           signal_full,
    "signal_short":     signal_short,
    "price":            CURRENT_PRICE,
    "epp_gap_pct":      epp_gap_pct,
    "ratio_b":          ratio_b,
    "ratio_b_fmt":      f"{ratio_b:.2f}x",
    "adj_composite":    ADJ_COMPOSITE,
    "market_composite": MARKET_COMPOSITE,
    "adj_gap":          ADJ_GAP,
    "valuation":        valuation_label,
    "cons_return_2yr":  cons_return,
}

if __name__ == "__main__":
    pass
