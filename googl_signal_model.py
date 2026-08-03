"""
GOOGL  ·  Alphabet Inc.  ·  NASDAQ: GOOGL
Bottom-up signal model  ·  Google Search / YouTube / Google Cloud / AI
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "GOOGL"
COMPANY       = "Alphabet Inc."
SECTOR        = "Google Search · YouTube · Google Cloud · AI Infrastructure · NASDAQ: GOOGL"
CURRENT_PRICE = 356.13       # USD; close 2026-07-31 (verified live)
VOL_52W_LOW   = 187.82       # 2026 trough
VOL_52W_HIGH  = 408.61       # 2026 AI/Cloud re-rating peak
SHARES_OUT_M  = 12_240.0     # millions; $4.36T mkt cap / $356.13; includes A+B+C classes
ANNUAL_DIV    = 0.84         # $/share forward; yield ~0.24%

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ──────────────────────────────────────
# Q2 2026 actual: revenue $119.8B (+24% YoY); Search $63.3B (+17%), YouTube $11.1B (+13%),
# Cloud $24.8B (+82%!, op income $8.8B vs $2.8B YoY), Cloud backlog $514B. Capex raised to $195-205B.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Search & Other",                250.0, 220.0, 285.0, "+17% YoY; AI Overviews monetizing so far without cannibalizing the core ad engine"),
    ("YouTube Ads",                    44.0,  38.0,  53.0, "+13% YoY; Shorts + connected-TV share gains continue"),
    ("Google Cloud",                  100.0,  75.0, 150.0, "+82% YoY; op income swung from $2.8B to $8.8B YoY; $514B backlog is 5x+ annual revenue"),
    ("Subscriptions/Devices + Other Bets", 66.0,  56.0,  82.0, "YouTube Premium/Music, Pixel/hardware, Waymo — steady, non-core"),
]

# Margin assumptions (GAAP operating margin proxy; EXCLUDES the Q2 $98.0B one-time
# unrealized equity-securities gain that inflated reported net income to $112.1B / EPS $9.11)
OP_MARGIN_CURR   = 0.340    # FY2026E blended operating margin; Q2 actual operating margin was 34%
OP_MARGIN_BULL   = 0.390    # BULL: Cloud margin keeps expanding (already 35.5% in Q2, from near-breakeven a year ago)
OP_MARGIN_BEAR   = 0.290    # BEAR: capex depreciation and AI-Overviews monetization risk both compress margin
TAX_RATE         = 0.160    # effective tax rate

# ── CLOUD INFLECTION / ONE-TIME GAIN CALCULATOR (the Alphabet-specific angle) ──
CLOUD_BACKLOG_B        = 514.0  # $B Cloud backlog, Q2 2026 — over 5x annualized Cloud revenue
CLOUD_OP_INCOME_Q2_B   =   8.8  # $B Cloud operating income, Q2 2026 (vs $2.8B a year ago)
CAPEX_GUIDE_LOW_B      = 195.0  # $B FY2026 capex guidance, low end (raised from $180B)
CAPEX_GUIDE_HIGH_B     = 205.0  # $B FY2026 capex guidance, high end (raised from $190B)
ONE_TIME_EQUITY_GAIN_B =  98.0  # $B net unrealized gain on equity securities, Q2 2026 — NOT operating earnings
EU_ANTITRUST_FINE_B    =   4.1  # € (~$B) fine upheld by the EU Court of Justice over Android
US_ANTITRUST_OUTCOME   = "no breakup; data-sharing + no-exclusivity remedies; both sides appealing"

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 10.75       # $/share; CLEAN operating-basis FY2026E estimate — excludes the Q2 one-time equity gain
PE_PESSIMISTIC = 18.0        # trough P/E: roughly Alphabet's own multi-year average forward multiple pre-AI-rerating;
                              # 18x prices a return to being valued as "just" a very profitable ad/cloud business
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 7.74, 22,  170, "AI Overviews cannibalizes ad monetization faster than it adds; heavy capex depreciation compresses margin"),
    "BASE":  (11.80, 30,  354, "Cloud keeps compounding at a moderating pace; Search holds share through the AI transition"),
    "BULL":  (15.60, 32,  499, "Cloud growth sustains near 60%+ for another year; AI Overviews prove additive, not cannibalistic"),
    "XBULL": (18.50, 34,  629, "Google Cloud becomes a clear #2/#3 hyperscaler at massive scale; antitrust overhang fully resolved"),
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
        "name":       "Google Cloud revenue YoY growth",
        "weight":     0.25,
        "thresholds": ("<30%",   "≥50%",   "≥65%",   "≥80%"),
        "now":        "+82%",
        "score":      4,
        "comment":    "Cloud is now unambiguously the growth story; op income swung from $2.8B to $8.8B YoY on the same quarter",
    },
    {
        "name":       "Search & Other revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<5%",    "≥10%",   "≥15%",   "≥20%"),
        "now":        "+17%",
        "score":      3,
        "comment":    "The single most important disproof point against the 'AI kills search' bear thesis, quarter after quarter",
    },
    {
        "name":       "Cloud backlog coverage",
        "weight":     0.15,
        "thresholds": ("<2x",    "≥3x",    "≥4x",    "≥5x"),
        "now":        "~5.2x",
        "score":      4,
        "comment":    "$514B backlog vs ~$100B annualized Cloud revenue — exceptional forward visibility for the growth segment",
    },
    {
        "name":       "Consolidated operating margin",
        "weight":     0.15,
        "thresholds": ("<28%",   "≥31%",   "≥34%",   "≥37%"),
        "now":        "34%",
        "score":      3,
        "comment":    "Holding up even as capex and depreciation ramp — Cloud's margin inflection is doing real work here",
    },
    {
        "name":       "Capex growth vs revenue growth",
        "weight":     0.10,
        "thresholds": (">2.5x rev","≤2.0x",  "≤1.5x",  "≤1.0x"),
        "now":        "~1.7x",
        "score":      2,
        "comment":    "$195-205B capex guide vs 24% revenue growth — spending is outpacing revenue growth, the crux of the AI-capex debate",
    },
    {
        "name":       "Forward P/E (clean, ex-one-time gains)",
        "weight":     0.15,
        "thresholds": (">40x",   "≤33x",   "≤26x",   "≤20x"),
        "now":        "~33.1x",
        "score":      2,
        "comment":    "The headline 17.9x trailing P/E is misleading — it's deflated by a $98B one-time equity gain; the clean multiple is much richer",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Cloud inflection is real and large — $514B backlog, margin swinging from breakeven to 35%+ in a year", +0.8, 0.20),
    ("+", "Search resilience — +17% YoY growth is the clearest evidence yet that AI Overviews aren't cannibalizing the core business", +0.6, 0.20),
    ("-", "Capex is outrunning revenue growth — $195-205B guide against 24% revenue growth is the same debate weighing on every hyperscaler", -0.6, 0.20),
    ("+", "Antitrust overhang resolved favorably — no breakup, Chrome and Android retained; remaining remedies are manageable", +0.5, 0.15),
    ("-", "Reported earnings quality — the headline EPS beat is largely a $98B non-operating equity gain, not core earnings power", -0.4, 0.15),
    ("+", "Balance sheet + diversification — Search, Cloud, YouTube, and a stake in the AV/robotics optionality (Waymo) all compounding at once", +0.3, 0.10),
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
CONS_EPS_2YR  = 12.60   # conservative FY2028E: ~8.3% EPS CAGR off the clean $10.75 base
CONS_PE_2YR   = 26      # modest de-rating from ~33x — still a real premium multiple
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Search / YouTube / Cloud / AI Infrastructure")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<38}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<38}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<38}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  Q2 2026 actual: $119.8B (+24% YoY). Capex guidance raised to ${CAPEX_GUIDE_LOW_B:.0f}-{CAPEX_GUIDE_HIGH_B:.0f}B for FY2026")
print()

# EPS bridge (clean, operating basis)
shares    = SHARES_OUT_M / 1000
curr_op   = curr_total * OP_MARGIN_CURR
curr_eps  = round(curr_op * (1 - TAX_RATE) / shares, 2)

bull_op   = bull_total * OP_MARGIN_BULL
shares_b  = shares * 0.98
bull_eps_imp = round(bull_op * (1 - TAX_RATE) / shares_b, 2)

bear_op   = bear_total * OP_MARGIN_BEAR
bear_eps_imp = round(bear_op * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check (CLEAN, ex-one-time gains):  ${curr_total:.1f}B rev × {OP_MARGIN_CURR*100:.1f}% op margin")
print(f"  − {TAX_RATE*100:.1f}% tax  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2026E:.2f}  ✓)")
print(f"  Reported Q2 EPS was $9.11, boosted by a ${ONE_TIME_EQUITY_GAIN_B:.0f}B one-time unrealized equity gain — not repeatable.")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {OP_MARGIN_BULL*100:.1f}% op margin, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 32× = ~${bull_eps_imp*32:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {OP_MARGIN_BEAR*100:.1f}% op margin (AI-Overviews risk + capex depreciation)")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 22× trough = ~${bear_eps_imp*22:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# CLOUD INFLECTION / ONE-TIME GAIN CHECK
print()
print(f"  CLOUD INFLECTION & EARNINGS-QUALITY CHECK  (the Alphabet-specific angle):")
print(f"  Cloud backlog:                  ${CLOUD_BACKLOG_B:.0f}B  (~5.2x annualized Cloud revenue)")
print(f"  Cloud operating income (Q2):    ${CLOUD_OP_INCOME_Q2_B:.1f}B  (vs $2.8B a year ago — a real margin inflection, not just scale)")
print(f"  One-time equity gain (Q2):      ${ONE_TIME_EQUITY_GAIN_B:.0f}B  (inflated reported EPS to $9.11; excluded from this model's EPS)")
print(f"  EU antitrust fine (Android):    €{EU_ANTITRUST_FINE_B:.1f}B upheld — a real but bounded cost")
print(f"  US antitrust outcome:           {US_ANTITRUST_OUTCOME}")
print()
print(f"  Two things to separate clearly: Cloud's margin inflection is a genuine operating")
print(f"  achievement — going from near-breakeven to 35%+ margin at this scale in a year is rare.")
print(f"  The $98B equity gain is not that; it is a mark-to-market accounting entry on a")
print(f"  strategic investment, and treating it as recurring earnings power would badly overstate")
print(f"  the multiple the stock actually trades at.")

# KEY SENSITIVITIES
print()
eps_per_1B_cloud = 1.0 * 0.35 * (1 - TAX_RATE) / shares   # Cloud incremental margin ~35%, matching Q2
eps_per_1B_search = 1.0 * 0.45 * (1 - TAX_RATE) / shares  # Search incremental margin ~45%
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Cloud revenue (35% inc. margin):   +${eps_per_1B_cloud:.3f}/EPS  = +${eps_per_1B_cloud*30:.2f}/share at 30× P/E")
print(f"  Every $1B Search revenue (45% inc. margin):  +${eps_per_1B_search:.3f}/EPS  = +${eps_per_1B_search*30:.2f}/share at 30× P/E")
print(f"  Every 1 turn of P/E:                         ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock, clean-EPS basis)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Cloud growth / Search resilience / backlog / margin / capex / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<42}  {'BEAR':>10}  {'BASE':>8}  {'BULL':>8}  {'XBULL':>8}  {'NOW':>9}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<42}  {ths[0]:>10}  {ths[1]:>8}  {ths[2]:>8}  {ths[3]:>8}  {s['now']:>9}  {lbl}  {b}")
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
    ("Google Cloud revenue YoY",   "+82%",   "<30%",    "-52pp",  "Hyperscaler capacity glut or a demand pause after the current buildout wave"),
    ("Search & Other revenue YoY", "+17%",   "<5%",     "-12pp",  "AI Overviews genuinely cannibalize click-through and ad monetization"),
    ("Cloud backlog coverage",     "~5.2x",  "<2x",     "-3.2x",  "Large committed contracts get renegotiated or delayed en masse"),
    ("Consolidated op margin",     "34%",    "<28%",    "-6pp",   "Capex depreciation lands faster than revenue from the assets it funded"),
    ("Capex vs revenue growth",    "~1.7x",  ">2.5x",   "+0.8x",  "Spending keeps accelerating even as growth decelerates — the AI-capex bear case"),
    ("Forward P/E (clean)",        "~33.1x", "≤22x",    "-11x",   "Market fully re-prices AI-infrastructure optimism across the hyperscaler cohort"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>9}  {bear_v:>9}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: this is the same AI-capex debate weighing on every hyperscaler right now —")
print(f"  is $195-205B of annual capex building durable competitive advantage (Cloud backlog,")
print(f"  AI-native Search products) or overbuilding capacity ahead of demand? Alphabet's evidence")
print(f"  is better than most: Cloud backlog of 5.2x revenue and Search growth that has NOT")
print(f"  decelerated through the AI Overviews rollout. The bear case requires both of those")
print(f"  proof points to reverse, not just capex to keep rising.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E clean EPS:          ${EPS_FY2026E:.2f}  (operating-basis; excludes the Q2 one-time equity gain)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (roughly Alphabet's own multi-year pre-AI-rerating average)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× clean FY2026E EPS — a real premium to Alphabet's")
print(f"  historical multiple, reflecting the market's conviction that Cloud plus AI Search is a")
print(f"  structurally better business than the ad-only franchise of five years ago. The headline")
print(f"  17.9× trailing P/E you'll see quoted elsewhere is an artifact of the one-time equity")
print(f"  gain, not a genuine value signal — ignore it.")
print(f"  At a 25× reversion (still above the historical average): ${EPS_FY2026E:.2f} × 25 = ${EPS_FY2026E*25:.0f}  ({(EPS_FY2026E*25/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: growth moderates, multiple compresses toward a still-rich level)")
hr()
print(f"  Conservative FY2028E EPS:  ${CONS_EPS_2YR:.2f}  (~8.3% EPS CAGR off the clean ${EPS_FY2026E:.2f} base)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~33× → 26×; a real de-rating, still a premium multiple)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: a real multiple compression — from a rich 33× to a still-generous 26× —")
print(f"  paired with EPS growth well below the current pace produces a slightly NEGATIVE conservative")
print(f"  return ({cons_annual:+.1f}%/yr). That is not a red flag on the business; it reflects that a")
print(f"  $4.36T company simply cannot offer the kind of margin of safety a smaller, more-discounted")
print(f"  name can. The bull case here is genuinely available — it just isn't the conservative case.")
print(f"  Breakeven at 26× requires FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f} — above this conservative estimate.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.30
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Move off the low:      +{(CURRENT_PRICE/VOL_52W_LOW-1)*100:.0f}%  over the past year — the Cloud/AI re-rating in one number")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; small but growing)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (moderate for a $4T+ company; still elevated by AI-capex-narrative sensitivity)")
print(f"  Beta vs S&P 500:      1.05  (near-market beta despite the size and growth profile)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (a real move, in line with the AI-capex-sector correction risk)")
print(f"  → Q3 print is the next test of Search resilience and Cloud backlog conversion.")
print(f"  → Antitrust appeal timeline is a slow-moving but real background risk through 2026-27.")
print(f"  → WATCHLIST at current price  |  ACCUMULATE $260–290  |  BUY below $220")

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
print(f"  Alphabet's fundamentals are genuinely excellent across nearly every signal this model")
print(f"  tracks — Cloud, Search, backlog, and even the antitrust overhang have all resolved")
print(f"  better than feared. WATCHLIST reflects that the stock has already re-rated substantially")
print(f"  to reflect that improvement; the price is fair for the business, not a bargain for it.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q3 2026 results — Search growth durability through continued AI Overviews rollout")
print(f"  (2) Cloud backlog-to-revenue conversion pace — the $514B backlog needs to keep showing up in revenue")
print(f"  (3) Capex guidance revision — any further raise intensifies the AI-capex debate")
print(f"  (4) Antitrust appeal developments — both Google's and DOJ's appeals are multi-year overhangs")
print(f"  (5) Gemini/AI product monetization — direct evidence AI is additive, not just defensive, to the ad business")
print(f"  WATCHLIST at ${CURRENT_PRICE:.2f}  |  ACCUMULATE $260–290  |  BUY below $220")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E clean EPS: ${EPS_FY2026E:.2f}  |  Cloud backlog: ${CLOUD_BACKLOG_B:.0f}B")
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
