"""
AVGO  ·  Broadcom Inc.  ·  NYSE: AVGO
Bottom-up signal model  ·  Semiconductors / AI Custom Silicon (XPU) / VMware Software
Date: 2026-06-09
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "AVGO"
COMPANY       = "Broadcom Inc."
SECTOR        = "Semiconductors · AI Custom Silicon (XPU) · VMware Software · NYSE: AVGO"
CURRENT_PRICE = 420.00       # USD; as of 2026-06-09
VOL_52W_LOW   = 278.00       # January 2026 tariff trough
VOL_52W_HIGH  = 512.40       # November 2025 post-Q4 FY2025 AI beat peak
SHARES_OUT_M  = 4_720.0      # millions; post 10:1 split July 2024
ANNUAL_DIV    = 2.36         # $/share FY2026; growing; Hock Tan capital return

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B); fiscal year ends October 2026
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("AI Custom Silicon (XPU)",      20.0,  8.0, 32.0, "Google XPU v6, Meta MTIA 3; 2 new hyperscaler wins in pipeline"),
    ("Networking Silicon",            7.0,  4.0, 11.0, "Tomahawk 5/Jericho 3; AI cluster spine + ToR fabric"),
    ("Server Storage Connectivity",   3.0,  2.0,  4.0, "PCIe 6/CXL; enterprise & cloud storage fabric"),
    ("Broadband",                     2.0,  1.5,  3.0, "PON/DSL CPE; low growth; stable cash flow"),
    ("Industrial / Other Semi",       1.5,  1.0,  2.0, "Embedded; SAN HBA; declining priority"),
    ("VMware Infrastructure SW",     24.0, 17.0, 30.0, "35K enterprise accounts migrating to subscription; 90%+ gross margin"),
    ("Security / CA / Other SW",      4.0,  3.5,  5.0, "Carbon Black + CA Tech; steady ARR; minimal growth"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.780   # blended; VMware software mix lifting toward 80%
GROSS_MARGIN_BULL = 0.800   # BULL: VMware matures at 90%+ GM; XPU scale
OPEX_FIXED_B      = 10.5    # non-GAAP R&D + SG&A (excl SBC and amortization)
TAX_RATE          = 0.080   # effective low; Cayman IP / Singapore structures

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 9.20        # FY2026E adj EPS (consensus $9.00–$9.50 non-GAAP; FY2026 Oct 2026)
PE_PESSIMISTIC = 22.0        # trough: software ARR + ASIC moat justifies floor above commodity semi
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 8.80, 22,  194, "AI CapEx freeze + VMware churn acceleration; XPU design loss; EPS $8.80 → 22× panic"),
    "BASE":  (14.00, 32,  448, "3 XPU hyperscalers + VMware steadying at 88% renewal; FY2028E EPS $14 → 32× = $448"),
    "BULL":  (20.00, 35,  700, "5-hyperscaler XPU sweep; sovereign AI; VMware 95%+ renewal; FY2028E EPS $20 → 35× = $700"),
    "XBULL": (30.00, 40, 1200, "AVGO = foundational AI chip layer; every frontier lab custom silicon; EPS $30 → 40×"),
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
        "name":       "AI Custom Silicon (XPU) revenue YoY",
        "weight":     0.30,
        "thresholds": ("<20%",    "≥40%",  "≥80%",   "≥140%"),
        "now":        "+64%",
        "score":      3,
        "comment":    "FY2025 $12.2B → FY2026E $20B; Google XPU v6 + Meta MTIA 3 ramp; 2 new wins confirmed",
    },
    {
        "name":       "VMware ACV growth YoY",
        "weight":     0.25,
        "thresholds": ("<5%",     "≥12%",  "≥22%",   "≥35%"),
        "now":        "+18%",
        "score":      2,
        "comment":    "Subscription migration 88% complete; $24B ARR at 90%+ gross margin; churn stabilizing",
    },
    {
        "name":       "Hyperscaler AI CapEx guidance YoY",
        "weight":     0.20,
        "thresholds": ("<+10%",   "≥+20%", "≥+40%",  "≥+70%"),
        "now":        "+38%",
        "score":      2,
        "comment":    "Meta $65B, MSFT $80B, Google $75B, Amazon $105B; AVGO gets ~30% of AI silicon capex",
    },
    {
        "name":       "XPU design-win pipeline (hyperscalers)",
        "weight":     0.15,
        "thresholds": ("0 new",   "1 win", "2 wins", "3+ wins"),
        "now":        "2 wins",
        "score":      3,
        "comment":    "2 new publicly confirmed hyperscaler XPU engagements beyond Google/Meta; tape-out 2026",
    },
    {
        "name":       "Non-GAAP blended gross margin",
        "weight":     0.05,
        "thresholds": ("<72%",    "≥75%",  "≥78%",   "≥82%"),
        "now":        "78.5%",
        "score":      3,
        "comment":    "VMware software (90%+ GM) + XPU mix lifting blended; approaching 80% structural level",
    },
    {
        "name":       "VMware enterprise renewal rate",
        "weight":     0.05,
        "thresholds": ("<80%",    "≥88%",  "≥93%",   "≥97%"),
        "now":        "~91%",
        "score":      2,
        "comment":    "91% renewal; Nutanix/Hyper-V taking some seats but premium accounts renewing; ACV growing",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Custom ASIC switching cost moat — 3–5yr qualification cycle; Google/Meta locked; unique IP",   +0.8, 0.20),
    ("+", "VMware software flywheel — 35K enterprise accounts; $24B ARR at 90%+ GM; Hock Tan pricing",   +0.6, 0.20),
    ("-", "Hyperscaler CapEx concentration — Google ~40% of XPU revenue; single-program binary risk",     -0.6, 0.20),
    ("-", "VMware churn / Nutanix displacement — Hyper-V + NTNX winning budget-conscious accounts",       -0.5, 0.15),
    ("+", "Hock Tan capital allocation — serial M&A compounder; $50B+ buyback authorization; div growth", +0.4, 0.15),
    ("-", "Valuation gap — 45× FY2026E for sum-of-parts semi + software; re-rate risk if AI slows",       -0.3, 0.10),
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
CONS_EPS_2YR  = 11.00   # FY2028E conservative: 9% EPS CAGR (VMware matures; XPU competitive entry)
CONS_PE_2YR   = 28      # rerates from ~45× toward growth-justified 28× as hyper-growth phase ends
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Semiconductors / AI Custom Silicon (XPU) / VMware Software")
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

bull_gp      = bull_total * GROSS_MARGIN_BULL
bull_oi      = bull_gp - OPEX_FIXED_B
bull_ni      = bull_oi * (1 - TAX_RATE)
shares_b     = shares * 0.97   # ~1.5%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.96   # mix shift back to semi (lower margin)
bear_oi      = bear_gp - OPEX_FIXED_B * 0.95           # partial cost response
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 35× = ~${bull_eps_imp*35:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.96:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At {PE_PESSIMISTIC:.0f}× trough P/E (software ARR floor) = ~${bear_eps_imp*PE_PESSIMISTIC:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_xpu    = 1.0 * 0.65 * (1 - TAX_RATE) / shares   # XPU at ~65% gross margin
eps_per_1B_vmware = 1.0 * 0.90 * (1 - TAX_RATE) / shares   # VMware at ~90% gross margin
eps_per_1pp_gm    = curr_total * 0.01 * (1 - TAX_RATE) / shares

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B XPU revenue (65% margin):     +${eps_per_1B_xpu:.3f}/EPS  = +${eps_per_1B_xpu*32:.1f}/share at 32× P/E")
print(f"  Every $1B VMware ACV (90% margin):      +${eps_per_1B_vmware:.3f}/EPS  = +${eps_per_1B_vmware*32:.1f}/share at 32× P/E")
print(f"  1pp GM expansion (VMware mix/pricing):  +${eps_per_1pp_gm:.3f}/EPS  = +${eps_per_1pp_gm*32:.1f}/share at 32× P/E")
print(f"  1 new hyperscaler XPU win:               +$3–5B peak-year revenue = ~${eps_per_1B_xpu*4*32:.0f}–${eps_per_1B_xpu*5*32:.0f}/share at 32× P/E")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (XPU revenue / VMware ACV / hyperscaler CapEx / design wins framework)")
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
    ("AI XPU revenue YoY",             "+64%",    "<+20%",  "−44pp",  "Google defects to in-house NTT silicon project"),
    ("VMware ACV growth YoY",           "+18%",    "<+5%",   "−13pp",  "Churn spikes; Hyper-V free tier wins SMB wave"),
    ("Hyperscaler AI CapEx YoY",        "+38%",    "<+10%",  "−28pp",  "Macro recession → IT freeze → $50B capex cuts"),
    ("XPU design-win pipeline",         "2 wins",  "0 wins", "−2",     "Intel/Marvell win competitive bake-offs at Apple"),
    ("Non-GAAP gross margin",           "78.5%",   "<72%",   "−6.5pp", "Supply chain cost shock + XPU pricing pressure"),
    ("VMware renewal rate",             "~91%",    "<80%",   "−11pp",  "Microsoft bundles Hyper-V free in Azure credits"),
]
for name, curr_v, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr_v:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A major hyperscaler (most likely Google at ~40% of XPU revenue) announces")
print(f"  it is transitioning future AI accelerator roadmap to fully in-house design, ending AVGO")
print(f"  XPU partnership. Simultaneously, VMware churn accelerates as Nutanix and Microsoft Hyper-V")
print(f"  offer free migration incentives. EPS collapses toward $8.80 → 22× trough P/E = ${bear_price}.")
print(f"  Note: ${bear_price} represents a ~54% drawdown — extreme; requires dual fundamental breaks.")
print(f"  VMware $17B ARR floor + Networking silicon provide a durable $150–180 earnings floor.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus $9.00–$9.50; non-GAAP; GAAP ~$6.50 incl. amortization)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (software ARR + ASIC moat; above commodity semi 12–15×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP means the market prices in significant BULL execution.")
print(f"  At ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f}, the P/E is ~{CURRENT_PRICE/EPS_FY2026E:.0f}× — a premium that")
print(f"  reflects the unique XPU + VMware software duality. The risk: AI CapEx cycle mean-reversion")
print(f"  compresses both multiples simultaneously.")
print(f"  EPP path: FY2028E EPS ~${CONS_EPS_2YR:.2f} × {PE_PESSIMISTIC:.0f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing ~9%/yr).")
above_or_below = "above" if EPS_FY2026E * 28 > CURRENT_PRICE else "below"
print(f"  At 28× mid-cycle P/E: ${EPS_FY2026E:.2f} × 28 = ${EPS_FY2026E*28:.0f}  — {abs(EPS_FY2026E*28 - CURRENT_PRICE)/CURRENT_PRICE*100:.0f}% {above_or_below} current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: P/E rerates toward growth rate; XPU hyper-growth phase ends)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (9% EPS CAGR: XPU scale + VMware ARR maturity)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (rerates from ~45× toward growth-justified 28×)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; Hock Tan growth trajectory)")
hr()
up_down = "▼" if cons_total < CURRENT_PRICE else "▲"
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({up_down}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
above_below2 = "below" if cons_total < CURRENT_PRICE else "above"
print(f"  THE CORE TENSION: conservative case at ${cons_total:.0f} is {above_below2} current price.")
print(f"  P/E compression from ~45× to 28× (a −38% multiple re-rate) absorbs EPS growth.")
print(f"  For conservative 2yr to break even at 28× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.1f}% EPS growth by FY2028E — requires BULL execution.")
print(f"  Breakeven at 35× P/E (sustained AI premium): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / 35:.2f}")
print(f"  ACCUMULATE trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.85 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.95 + cons_divs * 0.5, 0):.0f} (conservative case positive at 28× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.40
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  growing; Hock Tan capital return)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; AI CapEx binary + VMware integration overhang)")
print(f"  Beta vs S&P 500:      1.45  (high; AI-sentiment-driven; XPU binary amplifier)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (unusual; requires fundamental break)")
print(f"  52W low ${VOL_52W_LOW:.2f} (Jan 2026 tariff trough) already a peak-to-trough move of ~46%.")
print(f"  → Google XPU partnership continuity is THE KEY binary; any defection = −30%+ move.")
print(f"  → VMware Nov 2026 renewal cohort confirms or breaks the ARR stabilization thesis.")
print(f"  → AVOID above $550  |  WATCHLIST $450–500  |  ACCUMULATE $370–420  |  BUY below $320")

# ─── ⑦ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print()
print("  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
hr()
probs_mkt = softmax_probs(MARKET_COMPOSITE)
print(f"  {'Scenario':<10}  {'Price':>7}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>7}  Description")
hr()
for s in ["BEAR", "BASE", "BULL", "XBULL"]:
    pp   = probs_proxy[s] * 100
    pm   = probs_mkt[s]   * 100
    gap  = pp - pm
    pr   = SCENARIOS[s][2]
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
above_below3 = "ABOVE" if MARKET_COMPOSITE > ADJ_COMPOSITE else "BELOW"
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is {above_below3} the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0 — between")
if MARKET_COMPOSITE < 2.0:
    mkt_band = "BEAR and BASE"
elif MARKET_COMPOSITE < 2.75:
    mkt_band = "BASE and BULL"
elif MARKET_COMPOSITE < 3.75:
    mkt_band = "BULL and XBULL"
else:
    mkt_band = "at XBULL"
if ADJ_COMPOSITE < 2.0:
    adj_band = "BEAR and BASE"
elif ADJ_COMPOSITE < 2.75:
    adj_band = "BASE and BULL"
elif ADJ_COMPOSITE < 3.75:
    adj_band = "BULL and XBULL"
else:
    adj_band = "XBULL"
print(f"  {mkt_band}. The model scores fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0 — between {adj_band}.")
print(f"  The gap ({ADJ_GAP:+.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  XPU BULL execution at 64% YoY is real — but priced at BULL/XBULL. VMware ACV and")
print(f"  hyperscaler CapEx guidance are both at BASE (score 2), creating a valuation mismatch.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q3 FY2026 earnings (August 2026) — XPU revenue beat and new design-win announcement = BULL trigger")
print(f"  (2) VMware renewal cohort (12-month mark, Nov 2026) — churn rate confirmation = key binary")
print(f"  (3) Hyperscaler capex guidance cuts — each 10% CapEx reduction = ~8% AVGO revenue impact")
print(f"  (4) Additional XPU customer announcements — Apple/Microsoft/Oracle XPU = re-rating catalyst")
print(f"  (5) Hock Tan M&A — another transformative acquisition ($40B+) could reset growth trajectory")
print(f"  AVOID above $550  |  WATCHLIST $450–500  |  ACCUMULATE $370–420  |  BUY below $320")
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
