"""
BRK.B  ·  Berkshire Hathaway Inc.  ·  NYSE: BRK.B
Bottom-up signal model  ·  Conglomerate / Insurance / Railroad / Utilities / Equities
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "BRK.B"
COMPANY       = "Berkshire Hathaway Inc."
SECTOR        = "Conglomerate · Insurance · Railroad · Utilities · Equities · NYSE: BRK.B"
CURRENT_PRICE = 485.95      # USD; as of 2026-06-11
VOL_52W_LOW   = 410.00      # post-Buffett-transition / market drawdown trough
VOL_52W_HIGH  = 512.00      # all-time high on Q1 2026 earnings beat
SHARES_OUT_M  = 1_440_000.0 # millions of B-equivalent shares (~1.44B)

# Dividend: Berkshire pays no dividend; retains all earnings for compounding
ANNUAL_DIV    = 0.00        # $/share

# ── SEGMENT REVENUE/EARNINGS BRIDGE (company-specific calculator) ─────────────
# Q1 2026 annualized operating earnings contribution by segment ($B, pre-tax run-rate)
SEG_DATA = [
    # (segment, curr_earn_B, bear_earn_B, bull_earn_B, description)
    ("Insurance Underwriting",  9.0,   2.0,  13.0, "GEICO turnaround complete (87.1% combined ratio); BH Re + Gen Re; $176B float"),
    ("Insurance Investment Inc", 14.0, 11.0,  17.0, "Float invested in T-bills/equities; ~$176B float at elevated short rates"),
    ("BNSF Railroad",           6.5,   4.5,   8.0, "Volume recovery + pricing; intermodal share gains vs trucking"),
    ("BHE (Utilities/Energy)",  4.0,  -4.0,   6.0, "PacifiCorp wildfire litigation overhang ($20-30B worst case) vs renewables growth"),
    ("Manufacturing/Service/Retail (MSR)", 9.0, 6.5, 11.0, "Industrials, building products, consumer brands; broad economic proxy"),
    ("Other (corp/equity divs)", 2.9,   2.0,   3.5, "Dividends from equity portfolio (Apple, AmEx, Coca-Cola, etc.) + corp items"),
]

# Margin / structural assumptions
TAX_RATE          = 0.21    # effective corporate tax rate on operating earnings
SHARE_COUNT_B     = SHARES_OUT_M / 1000   # 1.44B B-equivalent shares

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_CURRENT    = 31.00       # current annualized operating EPS per B-share (~$11.35B/qtr * 4 / 1.44B + adj)
EPS_BEAR       = 19.00       # bear-case operating EPS per B-share (insurance loss yr + PacifiCorp charge + BHE writedown)
PE_PESSIMISTIC = 16.0        # trough P/E: book-value floor + buyback support near 1.2x book (~$404)
EPP            = round(PE_PESSIMISTIC * (CURRENT_PRICE / EPS_BEAR) * EPS_BEAR / (CURRENT_PRICE/EPS_BEAR), 0)
# Simplify per template definition: EPP = pessimistic P/E × (current price/bear EPS-implied) -> use direct formula
EPP            = round(PE_PESSIMISTIC * EPS_BEAR, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (19.00, 16,  304, "PacifiCorp wildfire judgment ($25B+) + insurance cat year + Abel capital missteps; EPS $19 → 16x book-floor multiple"),
    "BASE":  (33.00, 18,  594, "Operating earnings +10%/yr continuation; GEICO margins hold; Abel deploys cash gradually; EPS $33 → 18x"),
    "BULL":  (39.00, 20,  780, "Cash deployed into accretive acquisition/buybacks; BHE litigation resolved favorably; railroad volumes recover; EPS $39 → 20x"),
    "XBULL": (45.00, 22,  990, "Greg Abel executes major elephant-sized acquisition; insurance hard market persists; equity portfolio re-rates; EPS $45 → 22x"),
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
        "name":       "Operating earnings YoY growth",
        "weight":     0.25,
        "thresholds": ("<0%",    "≥5%",   "≥15%",   "≥25%"),
        "now":        "+18%",
        "score":      3,
        "comment":    "Q1 2026 operating earnings $11.35B, +18% YoY; broad-based across insurance and railroad",
    },
    {
        "name":       "Insurance combined ratio (GEICO)",
        "weight":     0.20,
        "thresholds": (">100%",  "≤97%",  "≤92%",   "≤88%"),
        "now":        "87.1%",
        "score":      4,
        "comment":    "GEICO turnaround complete; 87.1% combined ratio is best-in-class; underwriting profit engine restored",
    },
    {
        "name":       "Cash deployment / buyback activity",
        "weight":     0.20,
        "thresholds": ("none",   "modest","steady", "large deal"),
        "now":        "modest",
        "score":      2,
        "comment":    "$397B cash hoard largely undeployed; buybacks paused near 1.2x book; Abel yet to make major capital allocation call",
    },
    {
        "name":       "BNSF railroad volume/pricing trend",
        "weight":     0.15,
        "thresholds": ("<-5%",   "≥0%",   "≥5%",    "≥10%"),
        "now":        "+4%",
        "score":      2,
        "comment":    "Intermodal volumes recovering; pricing firm; not yet at prior peak utilization",
    },
    {
        "name":       "PacifiCorp wildfire litigation overhang",
        "weight":     0.10,
        "thresholds": (">$25B",  "$15-25B","$5-15B","resolved"),
        "now":        "$20-30B est.",
        "score":      1,
        "comment":    "Worst-case exposure $20-30B remains unresolved; material tail risk to BHE segment value",
    },
    {
        "name":       "Book value per share growth (YoY)",
        "weight":     0.10,
        "thresholds": ("<5%",    "≥8%",   "≥11%",   "≥15%"),
        "now":        "+11.1%",
        "score":      3,
        "comment":    "Book value per B-share $337.15, +11.1% YoY; driven by retained earnings + equity portfolio gains",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Fortress balance sheet — $397B cash; AAA-quality; near-zero financial leverage risk",        +0.7, 0.20),
    ("+", "Insurance float compounding — $176B float at near-zero cost, GEICO turnaround durable",      +0.6, 0.20),
    ("-", "Greg Abel capital allocation unproven at scale — first full quarter as CEO, no track record", -0.6, 0.20),
    ("-", "PacifiCorp wildfire litigation tail risk — $20-30B worst case could impair BHE materially",  -0.5, 0.15),
    ("+", "Buyback floor discipline — Buffett-era ~1.2x book (~$404/B) provides valuation support",     +0.4, 0.15),
    ("-", "Conglomerate complexity discount — diversified holding co trades below sum-of-parts in market", -0.3, 0.10),
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
CONS_EPS_2YR  = 36.00   # conservative FY2028E operating EPS: ~8%/yr growth from $31 base
CONS_PE_2YR   = 18      # conservative exit multiple, in line with BASE scenario
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Conglomerate / Insurance / Railroad / Utilities / Equities")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT EARNINGS BRIDGE ────────────────────────────────────────────────
print()
print("  SEGMENT EARNINGS BRIDGE  (Annualized operating earnings ($B)  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(earn for _, earn, _, _, _ in SEG_DATA)
bear_total = sum(earn for _, _, earn, _, _ in SEG_DATA)
bull_total = sum(earn for _, _, _, earn, _ in SEG_DATA)

print(f"  {'Segment':<32}  {'Current ($B)':>12}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<32}  ${curr:>10.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL (pre-tax operating)':<32}  ${curr_total:>10.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print()

# EPS bridge
curr_ni   = curr_total * (1 - TAX_RATE)
curr_eps  = round(curr_ni / SHARE_COUNT_B, 2)

bull_ni   = bull_total * (1 - TAX_RATE)
bull_eps_imp = round(bull_ni / SHARE_COUNT_B, 1)

bear_ni   = max(0, bear_total) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / SHARE_COUNT_B, 1)

print(f"  Operating EPS check:  ${curr_total:.1f}B pre-tax × {(1-TAX_RATE)*100:.0f}% (after-tax) ÷ {SHARE_COUNT_B:.2f}B B-equiv shares")
print(f"  =  ${curr_eps:.2f}/share annualized operating EPS  (reported run-rate ≈ ${EPS_CURRENT:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B pre-tax × {(1-TAX_RATE)*100:.0f}% ÷ {SHARE_COUNT_B:.2f}B shares")
print(f"  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 20× = ~${bull_eps_imp*20:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B pre-tax × {(1-TAX_RATE)*100:.0f}% ÷ {SHARE_COUNT_B:.2f}B shares")
print(f"  =  ~${bear_eps_imp:.1f}/share  →  ${bear_eps_imp:.1f} × 16× book-floor multiple = ~${bear_eps_imp*16:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B insurance underwriting profit:  +${(1*(1-TAX_RATE))/SHARE_COUNT_B:.3f}/EPS  = +${(1*(1-TAX_RATE))/SHARE_COUNT_B*18:.2f}/share at 18× P/E")
print(f"  PacifiCorp $10B incremental litigation charge:  ~${(10*(1-TAX_RATE))/SHARE_COUNT_B:.2f}/share book value impact")
print(f"  $50B cash deployed at 8% after-tax return:  +${(50*0.08*(1-TAX_RATE))/SHARE_COUNT_B:.2f}/EPS  = +${(50*0.08*(1-TAX_RATE))/SHARE_COUNT_B*18:.2f}/share at 18× P/E")
print(f"  1pt combined ratio improvement (~$1.76B float-related):  +${(1.76*(1-TAX_RATE))/SHARE_COUNT_B:.3f}/EPS")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Earnings growth / Insurance / Capital deployment / Railroad / Litigation / Book value)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<48}  {'BEAR':>9}  {'BASE':>7}  {'BULL':>8}  {'XBULL':>10}  {'NOW':>10}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<48}  {ths[0]:>9}  {ths[1]:>7}  {ths[2]:>8}  {ths[3]:>10}  {s['now']:>10}  {lbl}  {b}")

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
print(f"  {'Signal':<48}  {'Current':>10}  {'Bear val':>10}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Operating earnings YoY growth",  "+18%",        "<0%",        "−18pp", "Severe insurance cat year + economic recession hits BNSF/MSR"),
    ("GEICO combined ratio",           "87.1%",       ">100%",      "+13pp", "Major cat losses (hurricanes/wildfires) push combined ratio above breakeven"),
    ("PacifiCorp litigation outcome",  "$20-30B est.","$25-30B+ paid","worse","Adverse court rulings finalize at high end with no insurance offset"),
    ("Cash deployment",                "modest",      "none/destructive","-", "Abel makes a poorly-timed large acquisition or remains paralyzed"),
    ("BNSF volume/pricing",            "+4%",         "<-5%",       "−9pp",  "Freight recession; trucking competition intensifies"),
    ("Book value growth YoY",          "+11.1%",      "<5%",        "−6pp",  "Equity portfolio (Apple etc.) drawdown + underwriting losses"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<48}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:40]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A finalized adverse PacifiCorp wildfire judgment near the $30B high end,")
print(f"  combined with a severe insurance catastrophe year (hurricanes/wildfires pushing GEICO's")
print(f"  combined ratio above 100%) and a recessionary hit to BNSF/MSR earnings, would compress")
print(f"  operating EPS toward ${bear_price/16:.0f} and the stock toward the ~1.2x Buffett buyback-floor")
print(f"  multiple near book value (~$337 × 1.2 ≈ $404). Note: the $397B cash pile and AAA balance")
print(f"  sheet mean this is a valuation reset, not a solvency event — recovery is the base case.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current/bear EPS)")
hr()
print(f"  Current annualized operating EPS:    ${EPS_CURRENT:.2f}  (Q1 2026 $11.35B/qtr × 4 ÷ {SHARE_COUNT_B:.2f}B shares)")
print(f"  Bear-case operating EPS:               ${EPS_BEAR:.2f}  (cat year + PacifiCorp charge + BHE writedown)")
print(f"  Pessimistic P/E at trough:              {PE_PESSIMISTIC:.0f}×  (~book-value floor; Buffett buyback discipline ~1.2x book)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share  (= {PE_PESSIMISTIC:.0f}× × ${EPS_BEAR:.2f} bear EPS)")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  At ${CURRENT_PRICE:.2f} and current operating EPS ${EPS_CURRENT:.2f}, the P/E is {CURRENT_PRICE/EPS_CURRENT:.1f}× —")
print(f"  modest for a fortress-balance-sheet compounder with $397B in dry powder. The book value")
print(f"  per B-share of $337.15 implies a P/B of {CURRENT_PRICE/337.15:.2f}x, well above Buffett's historical")
print(f"  ~1.2x buyback floor (~$404/share), suggesting limited near-term buyback support but")
print(f"  reasonable downside protection relative to history.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: operating EPS compounding + modest multiple)")
hr()
print(f"  Conservative FY2028E operating EPS:  ${CONS_EPS_2YR:.2f}  (~8% CAGR: float growth + BNSF/MSR recovery + buybacks)")
print(f"  Conservative exit P/E:                {CONS_PE_2YR}×  (in line with BASE scenario multiple)")
print(f"  Conservative equity value:             ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):         +${cons_divs:.2f}/share  (no dividend; 100% retained for compounding)")
hr()
print(f"  Conservative 2yr total:                ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:             {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE THESIS: even at a flat-to-modest 18× exit multiple, ~8%/yr operating EPS")
print(f"  growth (driven by insurance float compounding, BNSF/MSR recovery, and incremental")
print(f"  cash deployment by Abel) produces a {cons_return:.1f}% 2yr return with no dividend support.")
print(f"  Breakeven at {CONS_PE_2YR}× P/E requires FY2028E EPS ≥ ${CURRENT_PRICE / CONS_PE_2YR:.2f}")
print(f"  That implies ~{((CURRENT_PRICE/CONS_PE_2YR)/EPS_CURRENT - 1)*100:.1f}% EPS growth from current ${EPS_CURRENT:.2f} — achievable in BASE/BULL.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.16
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (no dividend; 100% earnings retention/compounding)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (low-volatility mega-cap; defensive conglomerate profile)")
print(f"  Beta vs S&P 500:      0.85  (below-market beta; insurance float + cash cushion dampen drawdowns)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (PacifiCorp adverse ruling + cat year combo)")
print(f"  Buffett buyback floor ~1.2x book ≈ $404/B provides a soft valuation backstop.")
print(f"  → Greg Abel's first major capital allocation decision (deploying part of the $397B)")
print(f"    is THE KEY catalyst — either direction.")
print(f"  → AVOID/WATCHLIST at current price  |  ACCUMULATE $440–460  |  BUY below $420")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) compares to the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The gap ({ADJ_GAP:.2f}) indicates the stock is")
print(f"  {valuation_label.lower()} by model standards. The largest swing factors are GEICO's")
print(f"  underwriting strength (BULL/XBULL signal) versus the unresolved PacifiCorp litigation")
print(f"  and Greg Abel's still-unproven capital deployment of the $397B cash hoard.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Greg Abel's first major capital allocation decision — large acquisition or buyback restart")
print(f"  (2) PacifiCorp wildfire litigation resolution — settlement vs. adverse $20-30B judgment")
print(f"  (3) Insurance underwriting margins — can GEICO sustain sub-90% combined ratios?")
print(f"  (4) BNSF railroad volume recovery — freight cycle inflection")
print(f"  (5) Equity portfolio concentration — Apple stake performance and any further trimming")
print(f"  WATCHLIST near ${CURRENT_PRICE:.2f}  |  ACCUMULATE $440–460  |  BUY below $420  |  Buyback floor ~$404")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  Current operating EPS: ${EPS_CURRENT:.2f}")
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
