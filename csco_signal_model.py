"""
CSCO  ·  Cisco Systems, Inc.  ·  NASDAQ: CSCO
Bottom-up signal model  ·  Enterprise Networking / AI Ethernet Fabric / Cybersecurity
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "CSCO"
COMPANY       = "Cisco Systems, Inc."
SECTOR        = "Enterprise Networking · AI Ethernet Fabric · Cybersecurity · NASDAQ: CSCO"
CURRENT_PRICE = 115.99       # USD; close 2026-07-31 (verified live)
VOL_52W_LOW   =  65.75       # 2025 trough; pre-AI-networking re-rating
VOL_52W_HIGH  = 130.37       # 2026 AI-fabric momentum peak
SHARES_OUT_M  = 3_941.0      # millions; $457.2B mkt cap / $115.99; ~2%/yr buyback
ANNUAL_DIV    = 1.68         # $0.42/quarter; 14-year dividend growth streak; yield ~1.45%

# ── SEGMENT REVENUE BRIDGE (FY2026E; fiscal year ends late July) ─────────────
# FY2026 guidance: revenue $62.8–63.0B, non-GAAP EPS $4.27–4.29
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Networking (switch/route/optics)", 30.5, 26.0, 36.0, "Silicon One + optics into AI clusters; Catalyst enterprise refresh; the swing factor"),
    ("Security (incl. Splunk)",          12.5, 11.0, 15.5, "Hypershield, XDR, identity; +22% YoY; fastest-growing and highest-multiple segment"),
    ("Services (support/maintenance)",   13.1, 12.6, 14.0, "Attached annuity on the installed base; the reason the bear case has a floor"),
    ("Observability (Splunk platform)",   2.9,  2.6,  3.6, "Splunk core; cross-sell into security is the $28B acquisition thesis"),
    ("Collaboration (Webex)",             3.9,  3.4,  4.5, "Structural share loss to Teams/Zoom; managed for cash, not growth"),
]

# Margin assumptions (non-GAAP)
GROSS_MARGIN_CURR = 0.680   # FY2026E non-GAAP gross margin
GROSS_MARGIN_BULL = 0.695   # BULL: security/software mix lifts blend
OPEX_FIXED_B      = 22.2    # R&D + SG&A ($B); back-solved to FY2026 guided EPS
TAX_RATE          = 0.190   # non-GAAP effective rate

# ── AI ORDER BOOK (the Cisco-specific calculator) ────────────────────────────
AI_ORDERS_FY2026_B = 9.0    # $B FY2026 AI infrastructure orders (raised from $5.3B YTD at Q3)
AI_REVENUE_FY26_B  = 4.0    # $B FY2026 AI revenue guidance
AI_ORDERS_FY2025_B = 2.0    # $B prior year — the inflection that drove the re-rating
RESTRUCTURING_B    = 1.0    # $B charges through FY2027 (~$450M in Q4 FY2026)

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 4.28        # FY2026 company guidance midpoint, non-GAAP ($4.27–$4.29)
PE_PESSIMISTIC = 16.0        # trough P/E: Cisco's 10-yr average is ~15×; 16× credits the
                             # improved security/software mix but assumes the AI premium unwinds
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 3.10, 16,   51, "AI order digestion; hyperscalers move to Broadcom/white-box; refresh cycle ends"),
    "BASE":  ( 5.20, 20,  104, "FY2026 guide met; ~10% EPS CAGR; AI revenue $6–7B; multiple normalises 27× → 20×"),
    "BULL":  ( 5.90, 28,  165, "Silicon One takes durable AI-ethernet share; $18–20B AI orders; Splunk cross-sell lands"),
    "XBULL": ( 7.00, 32,  224, "Cisco = default AI networking standard; sovereign AI buildouts; 20%+ EPS CAGR"),
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
        "name":       "AI infrastructure orders (FY, $B)",
        "weight":     0.25,
        "thresholds": ("<$3B",   "≥$6B",   "≥$12B",  "≥$20B"),
        "now":        "$9B",
        "score":      2,
        "comment":    "FY2026 raised to $9B from ~$2B in FY2025. Real inflection — but the guide is now the hurdle",
    },
    {
        "name":       "Total revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<0%",    "≥4%",    "≥9%",    "≥15%"),
        "now":        "+12%",
        "score":      3,
        "comment":    "Q3 FY2026 revenue $15.8B (+12%); best growth in a decade. Splunk anniversaried, so this is organic",
    },
    {
        "name":       "Security revenue YoY growth",
        "weight":     0.15,
        "thresholds": ("<5%",    "≥12%",   "≥20%",   "≥30%"),
        "now":        "+22%",
        "score":      3,
        "comment":    "Hypershield + XDR + Splunk; the segment that justifies a software multiple rather than a hardware one",
    },
    {
        "name":       "Non-GAAP operating margin",
        "weight":     0.15,
        "thresholds": ("<28%",   "≥31%",   "≥34%",   "≥37%"),
        "now":        "~32.8%",
        "score":      2,
        "comment":    "Holding up, but AI/hyperscaler revenue carries lower margin than enterprise. Mix dilutes as AI scales",
    },
    {
        "name":       "Forward P/E vs 10-yr average (~15×)",
        "weight":     0.15,
        "thresholds": (">30x",   "≤24x",   "≤18x",   "≤14x"),
        "now":        "27.1x",
        "score":      1,
        "comment":    "THE PROBLEM. 27.1× FY2026E EPS for a ~10% EPS grower = PEG 2.7×. The re-rating already happened",
    },
    {
        "name":       "Product orders ex-AI (enterprise refresh)",
        "weight":     0.10,
        "thresholds": ("<0%",    "≥5%",    "≥10%",   "≥18%"),
        "now":        "+6%",
        "score":      2,
        "comment":    "Campus/branch refresh is mid-cycle, not early. Wi-Fi 7 + Catalyst upgrade wave is 2–3 yrs in",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Installed-base annuity — $13.1B services/support; multi-year contracts; the bear-case floor", +0.6, 0.20),
    ("+", "Silicon One + optics — genuine merchant AI-fabric position; $9B orders from ~$2B a year ago",  +0.8, 0.20),
    ("-", "Multiple risk — 27.1× forward vs ~15× 10-yr average; the AI re-rating is already in the price", -1.0, 0.25),
    ("-", "Hyperscaler in-sourcing — Broadcom Tomahawk + white-box erode the merchant ethernet TAM",      -0.7, 0.15),
    ("+", "Capital return — $1.68 dividend (14-yr growth streak) + steady buyback; a real yield floor",   +0.4, 0.10),
    ("-", "Splunk digestion — $28B deal still diluting margin; up to $1B restructuring through FY2027",   -0.5, 0.10),
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
CONS_EPS_2YR  = 5.10    # conservative FY2028E: ~9% EPS CAGR off the $4.28 guide
CONS_PE_2YR   = 20      # multiple reverts partway from 27× toward the ~15× 10-yr average
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Networking / AI Ethernet Fabric / Security")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

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
print(f"  Company FY2026 guidance: $62.8–63.0B revenue, non-GAAP EPS $4.27–$4.29")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_eps  = round(curr_oi * (1 - TAX_RATE) / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B * 1.08
shares_b  = shares * 0.96          # ~2%/yr buyback over 2yr
bull_eps_imp = round(bull_oi * (1 - TAX_RATE) / shares_b, 2)

bear_gp   = bear_total * 0.655     # AI/hyperscaler mix + price competition compress GM
bear_oi   = bear_gp - OPEX_FIXED_B * 0.97
bear_eps_imp = round(max(0, bear_oi) * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex")
print(f"  − {TAX_RATE*100:.1f}% tax  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share")
print(f"  (company guidance ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − opex, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 28× = ~${bull_eps_imp*28:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × 65.5% GM − opex")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 16× (≈ the 10-yr avg multiple) = ~${bear_eps_imp*16:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")
print()
print(f"  ⚠ THE STRUCTURAL POINT: only {(bull_total-bear_total)/curr_total*100:.0f}% separates the bear and bull REVENUE cases")
print(f"  (${bear_total:.1f}B vs ${bull_total:.1f}B). But the bear/bull PRICE spread is ${bear_price}–${bull_price}, a {bull_price/bear_price:.1f}× range.")
print(f"  Almost all of that spread is the MULTIPLE (15× vs 28×), not the earnings. You are")
print(f"  underwriting a re-rating call, not an execution call.")

# KEY SENSITIVITIES
print()
eps_per_1B_net  = 1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1B_sec  = 1.0 * 0.78 * (1 - TAX_RATE) / shares      # security carries ~78% GM
eps_per_1x_pe   = EPS_FY2026E                                # 1 turn of multiple

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B networking revenue (68% GM):    +${eps_per_1B_net:.3f}/EPS  = +${eps_per_1B_net*20:.2f}/share at 20× P/E")
print(f"  Every $1B security revenue (78% GM):      +${eps_per_1B_sec:.3f}/EPS  = +${eps_per_1B_sec*20:.2f}/share at 20× P/E")
print(f"  Every 1 turn of P/E:                      ±${eps_per_1x_pe:.2f}/share  ({eps_per_1x_pe/CURRENT_PRICE*100:.1f}% of the stock)")
print(f"  ↑ this is why the multiple, not the P&L, is the whole argument at ${CURRENT_PRICE:.2f}")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (AI orders / growth / security mix / valuation discipline)")
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
    ("AI infrastructure orders",   "$9B",     "<$3B",    "−$6B",   "Hyperscalers standardise on Broadcom/white-box"),
    ("Total revenue YoY",          "+12%",    "<0%",     "−12pp",  "AI digestion + enterprise refresh cycle completes"),
    ("Security revenue YoY",       "+22%",    "<5%",     "−17pp",  "Palo Alto/CrowdStrike win the platform consolidation"),
    ("Non-GAAP operating margin",  "~32.8%",  "<28%",    "−5pp",   "Hyperscaler pricing + Splunk dilution + restructuring"),
    ("Forward P/E",                "27.1x",   "≤15x",    "−12x",   "AI premium fully unwinds to the 10-yr average"),
    ("Product orders ex-AI",       "+6%",     "<0%",     "−6pp",   "Enterprise IT budgets redirected to AI capex"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<34}  {curr:>9}  {bear_v:>9}  {move:>8}  {trigger[:46]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Cisco's AI revenue is merchant silicon and optics sold to a handful of")
print(f"  hyperscalers who are all actively building alternatives. Broadcom's Tomahawk line and")
print(f"  white-box designs address the same racks. Cisco does not need to lose the business —")
print(f"  it only needs to stop GAINING share for the ${AI_ORDERS_FY2026_B:.0f}B order line to flatten, and")
print(f"  the entire 27× multiple is underwritten by that line continuing to compound.")
print(f"  Note: BEAR ${bear_price} is a multiple story, not a solvency story. ${SEG_DATA[2][1]:.1f}B of sticky services")
print(f"  revenue and a 14-yr dividend growth streak mean the floor is a valuation floor.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E non-GAAP EPS (company guide):  ${EPS_FY2026E:.2f}  ($4.27–$4.29)")
print(f"  Pessimistic P/E at trough:              {PE_PESSIMISTIC:.0f}×  (10-yr average ~15×; 16× credits the security mix)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to the EPP floor is the widest gap in the large-cap networking")
print(f"  space. At ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f}, the P/E is {CURRENT_PRICE/EPS_FY2026E:.1f}× — versus a 10-year")
print(f"  average near 15×. Cisco has spent two decades as a 13–17× stock; it is being paid")
print(f"  a cloud multiple for the first time since 2000. That can persist — the AI order book")
print(f"  is genuinely different — but it is an assumption, not a margin of safety.")
print(f"  EPP path: FY2028E EPS ~$5.10 × {PE_PESSIMISTIC:.0f}× = ${5.10*PE_PESSIMISTIC:.0f} floor by FY2028 (EPP growing ~9%/yr).")
print(f"  At the 15× 10-yr average: ${EPS_FY2026E:.2f} × 15 = ${EPS_FY2026E*15:.0f}  — {(1-EPS_FY2026E*15/CURRENT_PRICE)*100:.0f}% below spot.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: guide met, multiple reverts partway toward the average)")
hr()
print(f"  Conservative FY2028E non-GAAP EPS:  ${CONS_EPS_2YR:.2f}  (~9% EPS CAGR off the ${EPS_FY2026E:.2f} guide)")
print(f"  Conservative exit P/E:               {CONS_PE_2YR}×  (27× → 20×; still a 33% premium to the 10-yr average)")
print(f"  Conservative equity value:            ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):        +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:               ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:            {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE PROBLEM: the BASE scenario (${SCENARIOS['BASE'][2]}) sits BELOW the current price of ${CURRENT_PRICE:.2f}.")
print(f"  In the single most likely outcome, you lose money. Cisco has to deliver something")
print(f"  closer to BULL just for you to break even — and BULL requires the 28× multiple to")
print(f"  survive two more years, which has not happened in this stock since the dot-com era.")
print(f"  Breakeven at 20× P/E requires FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f} (+{((CURRENT_PRICE - cons_divs)/CONS_PE_2YR/EPS_FY2026E-1)*100:.0f}% from FY2026E).")
print(f"  ACCUMULATE trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.80 + cons_divs, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs, 0):.0f} (where the conservative case turns positive)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.30
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Move off the low:     +{(CURRENT_PRICE/VOL_52W_LOW-1)*100:.0f}%  in 12 months — the AI-networking re-rating in one number")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  14-yr growth streak)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated vs Cisco's historical ~22%; now an AI-beta name)")
print(f"  Beta vs S&P 500:      1.05  (has risen with the AI attachment; used to be a defensive 0.85)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (multiple mean-reversion, not a business collapse)")
print(f"  → The stock sits {(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.0f}% below its 52W high and {(CURRENT_PRICE/VOL_52W_LOW-1)*100:.0f}% above its 52W low.")
print(f"  → Quarterly AI order disclosure is the only number that matters for the multiple.")
print(f"  → WATCHLIST at current price  |  ACCUMULATE $88–98  |  BUY below $80")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f} the market composite is {MARKET_COMPOSITE:.2f}/4.0 — the market is")
print(f"  pricing execution between BASE and BULL. The model's adjusted composite is {ADJ_COMPOSITE:.2f}/4.0.")
print(f"  The gap ({ADJ_GAP:+.2f}) says the stock is {valuation_label.lower()}.")
print(f"  Cisco is doing well. That is not in dispute — revenue +12%, security +22%, AI orders")
print(f"  4.5× year-over-year. The question is what you PAY for it, and at {CURRENT_PRICE/EPS_FY2026E:.1f}× forward the")
print(f"  answer is: nearly everything good that can happen. Good company, demanding price.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) FY2027 AI order guidance — the $9B FY2026 number is now the comparison base")
print(f"  (2) Hyperscaler design wins — any public loss to Broadcom/white-box de-rates the stock")
print(f"  (3) Security ARR trajectory — the segment that would justify a durable 25×+ multiple")
print(f"  (4) Splunk cross-sell metrics — proof the $28B was strategic and not defensive")
print(f"  (5) Enterprise refresh durability — Wi-Fi 7 / Catalyst cycle is mid-innings, not early")
print(f"  WATCHLIST at ${CURRENT_PRICE:.2f}  |  ACCUMULATE $88–98  |  BUY below $80  |  TRIM above $130")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  AI orders: ${AI_ORDERS_FY2026_B:.0f}B")
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
