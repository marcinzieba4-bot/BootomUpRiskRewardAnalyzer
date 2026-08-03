"""
AAPL  ·  Apple Inc.  ·  NASDAQ: AAPL
Bottom-up signal model  ·  Consumer Technology / iPhone / Services / Memory Cost Crisis
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "AAPL"
COMPANY       = "Apple Inc."
SECTOR        = "Consumer Technology · iPhone · Services · Apple Intelligence · NASDAQ: AAPL"
CURRENT_PRICE = 308.91       # USD; close 2026-07-31 (verified live), -7.35% on the Q3 print/Q4 guide
VOL_52W_LOW   = 201.68       # 2025/26 trough
VOL_52W_HIGH  = 344.57       # 2026 pre-memory-crisis peak
SHARES_OUT_M  = 14_600.0     # millions; $4.51T mkt cap / $308.91; declining via buyback
ANNUAL_DIV    = 1.08         # $/share FY2026; 47-year growth streak

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ──────────────────────────────────────
# Q3 FY2026 (June qtr) actual: revenue $109.4B (+16%); iPhone $54.3B (+22%), Mac $10.4B
# (+29%), Services $30.7B (record, but missed the $31.22B estimate). Q4 (Sept qtr) guide:
# +9-11% YoY (~$113B, below the $114.9B Street consensus) on memory-cost/supply pressure.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("iPhone",                212.0, 185.0, 260.0, "+22% YoY in Q3; the segment most exposed to the memory-driven BOM cost spike heading into Q4"),
    ("Services",               114.0, 100.0, 150.0, "Record but decelerating — missed the Q3 estimate for the first time in several quarters"),
    ("Mac + iPad",              62.0,  52.0,  76.0, "Mac +29% YoY; both lines now face lengthening delivery delays from memory/component scarcity"),
    ("Wearables/Home/Acc",      36.0,  30.0,  34.0, "Steadier, less exposed to the current supply squeeze than the compute-heavy product lines"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.462   # FY2026E blended gross margin; memory cost inflation is compressing this from the low-47s
GROSS_MARGIN_BULL = 0.490   # BULL: Apple Intelligence supercycle + Services mix shift lift margin even as memory costs partly persist
OPEX_FIXED_B      = 60.0    # R&D + SG&A ($B)
TAX_RATE          = 0.160   # effective tax rate

# ── MEMORY COST CRISIS CALCULATOR (the Apple-specific angle) ─────────────────
IPHONE_BOM_INCREASE_LOW  = 200   # $ estimated additional per-unit production cost from memory inflation, iPhone 18 Pro
IPHONE_BOM_INCREASE_HIGH = 300   # $ high end of the estimated per-unit cost increase
Q4_GUIDE_GROWTH_LOW_PCT  = 9.0   # % YoY revenue growth, Q4 FY2026 guide, low end
Q4_GUIDE_GROWTH_HIGH_PCT = 11.0  # % YoY revenue growth, Q4 FY2026 guide, high end
Q4_STREET_CONSENSUS_B    = 114.9 # $B Street revenue consensus the guide fell short of
FX_HEADWIND_PP           = 2.5   # percentage points of FX headwind cited for the Q4 guide
Q3_TARIFF_REFUND_EPS     = 0.11  # $/share one-time favorable tariff-refund impact included in Q3 EPS

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 7.82        # $/share FY2026E; matches Wedbush's $7.85 and the segment-bridge build below (consensus range $7.28-7.85);
                              # below the ~$8.27-8.29 TTM run-rate — the memory-cost-driven Q4 guide implies full-year deceleration
PE_PESSIMISTIC = 20.0        # trough P/E: Apple's own multi-year pre-AI-rerating average; 20x prices
                              # a genuine margin-compression cycle without assuming the franchise is broken
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 5.66, 20,  113, "Memory cost inflation persists through FY2027; margin compression outlasts the current supply cycle"),
    "BASE":  ( 9.88, 34,  336, "Memory costs normalize through FY2027 as HBM-driven fab capacity catches up; rich multiple persists on franchise quality"),
    "BULL":  (11.38, 32,  364, "Component costs ease faster than guided; Services reaccelerates; AI features drive a real upgrade supercycle"),
    "XBULL": (13.80, 34,  469, "Apple Intelligence becomes a genuine upgrade driver; Services re-accelerates to mid-teens growth; margin fully recovers"),
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
        "name":       "iPhone revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<0%",    "≥10%",   "≥18%",   "≥25%"),
        "now":        "+22%",
        "score":      3,
        "comment":    "Q3's strongest print in years — the demand side is not the current problem, the supply/cost side is",
    },
    {
        "name":       "Services revenue YoY growth",
        "weight":     0.15,
        "thresholds": ("<5%",    "≥8%",   "≥12%",   "≥16%"),
        "now":        "~decel.",
        "score":      2,
        "comment":    "A record quarter that still missed the Street estimate — the first sign of deceleration in a while",
    },
    {
        "name":       "Q4 guidance vs Street consensus",
        "weight":     0.20,
        "thresholds": ("well below","below",  "in-line", "above"),
        "now":        "below",
        "score":      2,
        "comment":    "Guide implies ~$113B vs a $114.9B consensus — a real, not manufactured, guidance miss",
    },
    {
        "name":       "Gross margin trajectory",
        "weight":     0.20,
        "thresholds": ("<43%",   "≥45%",   "≥47%",   "≥49%"),
        "now":        "~46.2%",
        "score":      2,
        "comment":    "Memory cost inflation is the direct, quantified culprit — Cook flagged 'even higher' costs ahead",
    },
    {
        "name":       "Memory cost impact (iPhone 18 Pro BOM)",
        "weight":     0.15,
        "thresholds": (">$400",  "≤$300",  "≤$200",  "≤$100"),
        "now":        "$200-300",
        "score":      2,
        "comment":    "A quantified, real cost headwind tied directly to the AI-driven HBM/DRAM supply crunch hitting the whole industry",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.10,
        "thresholds": (">40x",   "≤34x",   "≤28x",   "≤22x"),
        "now":        "~39.5x",
        "score":      1,
        "comment":    "39.5× FY2026E — a rich multiple, close to the >40x BEAR bucket, for a company guiding below consensus on margin pressure",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Demand is not the problem — iPhone +22%, Mac +29%; this is a supply/cost cycle, not a demand cycle", +0.6, 0.20),
    ("-", "Memory cost inflation is real, quantified, and industry-wide — Apple has limited near-term pricing power to fully pass it through", -0.7, 0.25),
    ("-", "Valuation carries a steep premium (39.5× forward) for a company that just guided below consensus", -0.7, 0.20),
    ("+", "Services deceleration, while real, is from a still-large, still-growing, high-margin recurring base", +0.4, 0.15),
    ("-", "Advanced-node (TSMC) capacity constraints compound the memory problem — this is a multi-input supply squeeze, not one fixable lever", -0.4, 0.10),
    ("+", "Capital return machine — buyback + 47-year dividend growth streak continues regardless of the cyclical cost pressure", +0.3, 0.10),
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
CONS_EPS_2YR  = 9.60    # conservative FY2028E: ~3.6% EPS CAGR — memory cost pressure persists, limited margin recovery
CONS_PE_2YR   = 24      # modest de-rating from ~34.5× — still a real premium multiple
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  iPhone / Services / Memory Cost Crisis")
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
    print(f"  {seg:<26}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<26}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  Q3 FY2026 actual: $109.4B (+16%). Q4 guide: +{Q4_GUIDE_GROWTH_LOW_PCT:.0f}-{Q4_GUIDE_GROWTH_HIGH_PCT:.0f}% YoY (~$113B, below ${Q4_STREET_CONSENSUS_B:.1f}B consensus)")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_eps  = round(curr_oi * (1 - TAX_RATE) / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B * 1.05
shares_b  = shares * 0.97
bull_eps_imp = round(bull_oi * (1 - TAX_RATE) / shares_b, 2)

bear_gp   = bear_total * 0.435     # memory costs persist and deepen without offset
bear_oi   = bear_gp - OPEX_FIXED_B * 1.02
bear_eps_imp = round(max(0, bear_oi) * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex")
print(f"  − {TAX_RATE*100:.1f}% tax  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − opex, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 32× = ~${bull_eps_imp*32:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × 43.5% GM (memory costs persist without offset) − opex")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 20× trough = ~${bear_eps_imp*20:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# MEMORY COST CRISIS CHECK
print()
print(f"  MEMORY COST CRISIS CHECK  (the Apple-specific angle):")
print(f"  iPhone 18 Pro BOM increase (est.):  ${IPHONE_BOM_INCREASE_LOW}-${IPHONE_BOM_INCREASE_HIGH}  per unit")
print(f"  Q4 guide vs Street consensus:        ~${113}B vs ${Q4_STREET_CONSENSUS_B:.1f}B  (a real, quantified miss)")
print(f"  FX headwind cited in the guide:      -{FX_HEADWIND_PP:.1f}pp")
print(f"  Q3 one-time tariff-refund EPS boost:  +${Q3_TARIFF_REFUND_EPS:.2f}/share  (not repeatable)")
print()
print(f"  This is the same memory supercycle driving Micron's earnings to records — DRAM and HBM")
print(f"  capacity is being redirected to AI infrastructure, and consumer electronics makers are")
print(f"  bidding for what's left. Apple is a price-taker on memory the way it has never had to be")
print(f"  on advanced logic (where its TSMC relationship gives it priority access). This is a real,")
print(f"  industry-wide cost shock, not an Apple-specific execution failure — but it still hits the")
print(f"  P&L directly and the market has correctly repriced for it.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_gm  = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 46.2% GM):      +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*26:.2f}/share at 26× P/E")
print(f"  Every 1pp of gross margin:            +${eps_per_1pp_gm:.3f}/EPS  = +${eps_per_1pp_gm*26:.2f}/share at 26× P/E")
print(f"  Every 1 turn of P/E:                  ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (iPhone / Services / guidance / margin / memory cost / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<42}  {'BEAR':>11}  {'BASE':>7}  {'BULL':>8}  {'XBULL':>7}  {'NOW':>9}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<42}  {ths[0]:>11}  {ths[1]:>7}  {ths[2]:>8}  {ths[3]:>7}  {s['now']:>9}  {lbl}  {b}")
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
print(f"  {'Signal':<32}  {'Current':>10}  {'Bear val':>10}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("iPhone revenue YoY",         "+22%",   "<0%",     "-22pp",  "Higher retail prices from BOM inflation finally crack consumer demand"),
    ("Services revenue YoY",       "decel.", "<5%",     "further","AI-native alternatives erode App Store/subscription economics"),
    ("Q4 guide vs consensus",      "below",  "well below","worse","Memory/component costs prove even worse than the current guide assumes"),
    ("Gross margin",               "~46.2%", "<43%",    "-3.2pp", "Memory cost inflation persists through FY2027 without full pass-through"),
    ("Memory BOM impact",          "$200-300","≥$400",  "worse",  "DRAM/HBM scarcity deepens as AI infrastructure demand keeps outrunning supply"),
    ("Forward P/E",                "~39.5x", "≤20x",    "-19.5x", "Market fully re-prices Apple as a lower-growth, margin-challenged hardware name"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: this is a cost-and-supply story, not a demand story — which is actually the")
print(f"  more repairable kind of problem for Apple to have. iPhone grew 22% and Mac grew 29% in")
print(f"  the most recent quarter; the risk is entirely about whether memory/component scarcity")
print(f"  compresses margins for one bad quarter or bleeds into FY2027. The AI-driven memory")
print(f"  supercycle that is hurting Apple's margins is the same one driving record profits at")
print(f"  Micron — it will not resolve on Apple's schedule, only on the industry's.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS estimate:       ${EPS_FY2026E:.2f}  (TTM ~$8.27-8.29 through March 2026; Q4 pressured by memory costs)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (Apple's own multi-year pre-AI-rerating average)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS — a real premium, though the")
print(f"  stock has already fallen {(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.0f}% from its 52-week high on the Q4 guide. The EPP floor")
print(f"  assumes a return to Apple's own historical trough multiple, not a distressed one — the")
print(f"  margin of safety here is thinner than it looks unless the memory cost cycle resolves.")
print(f"  At a 26× reversion (still a real premium): ${EPS_FY2026E:.2f} × 26 = ${EPS_FY2026E*26:.0f}  ({(EPS_FY2026E*26/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: memory cost pressure persists, limited margin recovery)")
hr()
print(f"  Conservative FY2028E EPS:  ${CONS_EPS_2YR:.2f}  (~3.6% EPS CAGR — memory costs stay elevated)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~39.5× → 24×; a real de-rating)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: assuming memory costs stay elevated through FY2027 with only modest")
print(f"  margin recovery, and the multiple de-rates meaningfully from today's premium, the")
print(f"  conservative case is roughly {'clearly negative' if cons_return < -10 else 'flat-to-negative' if cons_return < 5 else 'modestly positive'}. This is not a name offering a wide margin of")
print(f"  safety at the current price — you are paying for the memory cost cycle to resolve")
print(f"  reasonably, not for it to already be resolved.")
print(f"  Breakeven at 24× requires FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f} — {'above' if (CURRENT_PRICE - cons_divs) / CONS_PE_2YR > CONS_EPS_2YR else 'below'} this conservative estimate.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.28
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Single-session move:   -7.35% on the Q3 print/Q4 guide — a large move for Apple specifically")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; 47-year growth streak, low but reliable)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (moderate for mega-cap tech; the memory-cost narrative adds near-term jumpiness)")
print(f"  Beta vs S&P 500:      1.10  (near-market, slightly elevated on the current cost-cycle sensitivity)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (a real move, in line with the current cost-shock magnitude)")
print(f"  → Q4 FY2026 print (late Oct) is the next test of whether the memory cost impact matches or exceeds the guide.")
print(f"  → Memory spot pricing (DRAM/NAND/HBM) is the leading indicator to watch between prints.")
print(f"  → AVOID at current price  |  Reassess ACCUMULATE under $220  |  BUY below $180")

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
print(f"  adjusted composite is {ADJ_COMPOSITE:.2f}/4.0, for a gap of {ADJ_GAP:+.2f} — {valuation_label.lower()}.")
print(f"  Apple's demand engines (iPhone, Mac) are working; its cost structure is under genuine,")
print(f"  industry-wide pressure from the AI memory supercycle. The stock's {(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.0f}% drawdown has")
print(f"  already priced in real caution, but not enough of it — a {(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.0f}% drawdown from the high still leaves")
print(f"  the stock at ~39.5× depressed forward earnings. AVOID reflects that the memory cost")
print(f"  resolution timeline — not Apple's execution — is the swing factor the model can't resolve,")
print(f"  and the market isn't being paid to wait for a favorable answer.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q4 FY2026 print (late October) — does the memory cost impact match, beat, or miss the guide?")
print(f"  (2) DRAM/NAND/HBM spot pricing trends — the leading indicator for Apple's cost trajectory")
print(f"  (3) iPhone 18 Pro retail pricing decisions — how much of the BOM increase gets passed through")
print(f"  (4) Services growth reacceleration — needs to resume double-digit growth to offset hardware margin pressure")
print(f"  (5) TSMC advanced-node capacity allocation — the second supply constraint compounding the memory issue")
print(f"  AVOID at ${CURRENT_PRICE:.2f}  |  Reassess ACCUMULATE under $220  |  BUY below $180")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  Memory BOM hit: ${IPHONE_BOM_INCREASE_LOW}-${IPHONE_BOM_INCREASE_HIGH}/unit")
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
