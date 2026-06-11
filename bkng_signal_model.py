"""
BKNG  ·  Booking Holdings Inc.  ·  NASDAQ: BKNG
Bottom-up signal model  ·  Online Travel Agency / Booking.com / Priceline / Agoda / AI
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "BKNG"
COMPANY       = "Booking Holdings Inc."
SECTOR        = "Online Travel Agency · Booking.com / Priceline / Agoda / KAYAK · AI Travel Assistant · NASDAQ: BKNG"
CURRENT_PRICE = 5050.00      # USD; as of 2026-06-11
VOL_52W_LOW   = 3850.00      # April 2026 tariff/travel-demand-fear trough
VOL_52W_HIGH  = 5650.00      # early 2026 record bookings peak
SHARES_OUT_M  = 33.5         # millions; aggressive buyback (down from ~37M)

# Dividend: initiated 2024
ANNUAL_DIV    = 35.40        # $/share FY2026 (quarterly $8.85)

# ── ROOM-NIGHT GROWTH vs ALTERNATIVE ACCOMMODATION MIX (company-specific calculator) ─
# Gross bookings / revenue breakdown FY2026E ($B)
GROSS_BOOKINGS_B   = 175.0   # total gross travel bookings
TAKE_RATE          = 0.135   # revenue / gross bookings
MERCHANT_MIX_PCT   = 0.62    # % of bookings on merchant model (higher take, more working capital)
ALT_ACCOM_PCT      = 0.34    # % of room-nights from alternative accommodations (vacation rentals)
AI_AGENT_REV_B     = 1.2     # AI travel-assistant attributable incremental bookings revenue ($B/yr)

CORE_OP_MARGIN     = 0.39    # consolidated operating margin
ROOM_NIGHT_GROWTH  = 0.07    # 7% YoY room-night growth (Q1 2026 run-rate)
TAX_RATE           = 0.19    # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 235.00  # FY2026E adj EPS (consensus $228-$245)
PE_TROUGH = 16      # min P/E at crisis trough (2020 COVID lows ~14-16x on normalized EPS)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $3760

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (155.00, 17,  2635, "Travel recession; room-nights flat/negative; merchant mix margin compression; EPS $155 -> 17x distress P/E"),
    "BASE":  (235.00, 24,  5640, "Room-nights +6-8%; AI agent bookings scale; take rate stable; EPS $235 -> 24x P/E"),
    "BULL":  (300.00, 27,  8100, "AI travel agent drives incremental bookings share gains; alt-accom mix expands margin; EPS $300 -> 27x premium P/E"),
    "XBULL": (390.00, 30, 11700, "Booking.com becomes dominant AI-native travel platform; international penetration deepens; EPS $390 -> 30x peak P/E"),
}

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

# ── 6 PROXY SIGNALS ───────────────────────────────────────────────────────────
SIGNALS = [
    {
        "name":       "Room-nights booked — YoY growth",
        "weight":     0.25,
        "thresholds": ("<2%",    "≥5%",   "≥9%",    "≥14%"),
        "now":        "+7%",
        "score":      2,
        "comment":    "+7% YoY; international (esp. Asia-Pacific) outpacing US/Europe maturity",
    },
    {
        "name":       "Gross bookings — YoY growth (constant currency)",
        "weight":     0.20,
        "thresholds": ("<3%",    "≥6%",   "≥10%",   "≥15%"),
        "now":        "+9%",
        "score":      3,
        "comment":    "+9% YoY; ADR resilience plus room-night growth; merchant mix shift adds rev/booking",
    },
    {
        "name":       "AI travel-assistant adoption — attributable bookings ($B/yr)",
        "weight":     0.15,
        "thresholds": ("<$0.3B", "≥$0.8B","≥$1.5B", "≥$3B"),
        "now":        "~$1.2B",
        "score":      2,
        "comment":    "~$1.2B; Booking.com 'AI Trip Planner' + Priceline 'Penny' driving incremental conversion",
    },
    {
        "name":       "Alternative accommodation room-night mix",
        "weight":     0.15,
        "thresholds": ("<25%",   "≥30%",  "≥35%",   "≥42%"),
        "now":        "~34%",
        "score":      3,
        "comment":    "~34%; vacation rental supply growth continues to outpace traditional hotel mix",
    },
    {
        "name":       "Operating margin trend",
        "weight":     0.15,
        "thresholds": ("<33%",   "≥36%",  "≥39%",   "≥42%"),
        "now":        "~39%",
        "score":      3,
        "comment":    "~39%; marketing efficiency (direct traffic mix) and AI customer-service cost reduction",
    },
    {
        "name":       "Connected Trip / cross-sell attach rate (flights+cars+experiences)",
        "weight":     0.10,
        "thresholds": ("<8%",    "≥12%",  "≥18%",   "≥25%"),
        "now":        "~14%",
        "score":      2,
        "comment":    "~14%; flights/experiences attach growing but still small vs accommodation core",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Global OTA scale moat — #1 in Europe/APAC; 30M+ listings; brand portfolio (Booking/Priceline/Agoda/KAYAK)", +0.7, 0.25),
    ("+", "Capital-light, high-FCF model — ~33.5M shares (aggressive buyback), $35/yr dividend",                       +0.6, 0.20),
    ("+", "AI agent integration — early but credible distribution advantage vs Google/OpenAI travel disintermediation", +0.4, 0.20),
    ("-", "Disintermediation risk — AI search/agents (ChatGPT, Gemini) could route bookings direct to suppliers",      -0.6, 0.20),
    ("-", "Macro travel sensitivity — discretionary spend highly cyclical; Europe/Asia FX exposure",                   -0.4, 0.15),
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

# ── CONSERVATIVE GROWTH (2-yr) ────────────────────────────────────────────────
CONS_EPS_2YR = 270.00   # conservative FY2028E: room-night growth moderates to mid-single digits
CONS_PE_2YR  = 22       # floor multiple (below current; reflects AI-disintermediation discount)
cons_equity  = CONS_EPS_2YR * CONS_PE_2YR
cons_divs    = ANNUAL_DIV * 2
cons_total   = cons_equity + cons_divs
cons_return  = round((cons_total - CURRENT_PRICE) / CURRENT_PRICE * 100, 1)
cons_annual  = round(cons_return / 2, 1)

# ─────────────────────────────────────────────────────────────────────────────
#  OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
W = 72

def hr(): print("  " + "─" * W)
def bar(score):
    return "█" * score + "░" * (4 - score)

print()
print("═" * (W + 4))
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Online Travel Agency / AI Travel Assistant")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① ROOM-NIGHT GROWTH vs AI DISINTERMEDIATION ANALYSIS ────────────────────
print()
print("  ROOM-NIGHT GROWTH vs AI DISINTERMEDIATION ANALYSIS  (the core BKNG tension)")
hr()

print(f"  FY2026E Operating Metrics:")
print(f"  {'Gross travel bookings':<36}  ${GROSS_BOOKINGS_B:>5.1f}B  (+{ROOM_NIGHT_GROWTH*100:.0f}% room-nights YoY)")
print(f"  {'Take rate (revenue/bookings)':<36}  {TAKE_RATE*100:>5.1f}%  (merchant mix {MERCHANT_MIX_PCT*100:.0f}%)")
print(f"  {'Alt. accommodation room-night mix':<36}  {ALT_ACCOM_PCT*100:>5.1f}%  (vacation rentals; structurally growing)")
print(f"  {'Operating margin':<36}  {CORE_OP_MARGIN*100:>5.1f}%  (marketing efficiency + AI cost reduction)")
print(f"  {'AI agent attributable revenue':<36}  ${AI_AGENT_REV_B:>5.1f}B/yr  (Trip Planner / Penny early monetisation)")
hr()
revenue_b = GROSS_BOOKINGS_B * TAKE_RATE
print(f"  Implied FY2026E revenue:                ${revenue_b:>5.1f}B")
print()

shares_b = SHARES_OUT_M / 1000
print(f"  ROOM-NIGHT GROWTH UPSIDE  (incremental EPS from room-night growth above/below {ROOM_NIGHT_GROWTH*100:.0f}%):")
print(f"  {'Room-night YoY growth':<24}  {'Rev/yr':>10}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.02, 0.05, 0.07, 0.12]:
    rev_inc = revenue_b * g
    inc_eps = rev_inc * CORE_OP_MARGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% room-night growth     +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
print(f"  AI DISINTERMEDIATION RISK  (each 5% of bookings re-routed away from BKNG by AI agents):")
disint_loss = revenue_b * 0.05 * CORE_OP_MARGIN * (1 - TAX_RATE) / shares_b
print(f"  5% booking diversion -> -${revenue_b*0.05:.2f}B revenue -> -${disint_loss:.2f}/EPS/yr -> -${disint_loss*2:.2f}/EPS over 2yr")
print()
print(f"  BEAR (${bear_price}) requires: travel recession AND AI agents materially divert bookings AND")
print(f"  merchant-mix margin compression — simultaneously.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (room-nights + AI adoption + alt-accom mix + margins)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>6}  {'BASE':>5}  {'BULL':>6}  {'XBULL':>8}  {'NOW':>7}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>6}  {ths[1]:>5}  {ths[2]:>6}  {ths[3]:>8}  {s['now']:>7}  {lbl}  {b}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15% hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  ->  Adj composite {ADJ_COMPOSITE:.3f}  ->  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    c = score * weight
    print(f"    {sign}  {desc[:72]:<72}  ({score:+.1f} x {weight*100:.0f}%  =  {c:+.3f})")

# ─── ② BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>7}  Trigger")
hr()
bear_triggers = [
    ("Room-nights booked YoY",                  "+7%",    "<2%",   "-5pp",   "Global travel recession; consumer pulls back discretionary trips"),
    ("Gross bookings YoY",                      "+9%",    "<3%",   "-6pp",   "ADR declines as supply outpaces demand; FX headwinds"),
    ("AI agent attributable revenue",           "~$1.2B", "<$0.3B","-$0.9B", "OpenAI/Google AI agents book directly with suppliers, bypass OTA"),
    ("Alt. accommodation mix",                  "~34%",   "<25%",  "-9pp",   "Regulatory crackdown on short-term rentals (EU/US cities)"),
    ("Operating margin",                        "~39%",   "<33%",  "-6pp",   "Marketing cost inflation as AI search referral traffic declines"),
    ("Connected Trip attach rate",              "~14%",   "<8%",   "-6pp",   "Cross-sell stalls; flights/experiences underperform"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: AI travel agents (ChatGPT, Gemini, Perplexity) reach a tipping point where")
print(f"  consumers book directly with hotels/airlines via AI assistants, bypassing OTAs entirely,")
print(f"  while a simultaneous travel recession compresses ADRs. EPS falls to ~$155;")
print(f"  multiple compresses to 17x distress P/E = ${bear_price}.")

# ─── ③ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS x min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}  (consensus $228-$245)")
print(f"  Min viable P/E at trough:      {PE_TROUGH}x  (2020 COVID lows ~14-16x on normalized EPS)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct>=0 else 'below'} trough floor)")
print()
print(f"  Premium to EPP reflects continued buyback-driven EPS compounding (share count down ~10% over 2yr).")
print(f"  Bear ${bear_price} is BELOW EPP ${EPP:.0f} — requires BOTH EPS collapse AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+25:.2f} x {PE_TROUGH}x = ${(EPP_EPS+25)*PE_TROUGH:.0f} EPP — stock catches up quickly.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: room-night growth moderates, buybacks continue)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (mid-single-digit room-night growth + buyback compounding)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (below current multiple; AI-disintermediation discount)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f} x 2)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'NEGATIVE'} — buyback-driven EPS compounding plus dividend")
print(f"  provides a margin of safety even if the multiple compresses from current levels.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.27
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%; initiated 2024; buyback primary return)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (large-cap; travel-cycle + AI-disintermediation sentiment)")
print(f"  Beta vs S&P 500:      1.10  (slightly above market; discretionary travel exposure)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (2020 BKNG fell ~50% from peak; achievable in a travel recession)")
print(f"  -> AI travel-agent integration is the PRIMARY catalyst; successful Connected Trip AI = +15-20%; disintermediation = -25%+.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — mid-to-upper range; some good news already priced in.")
print(f"  -> BUY $3850-$4400  |  TRIM $5650+  |  AVOID above $6200")

# ─── ⑥ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print()
print("  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
hr()
probs_mkt = softmax_probs(MARKET_COMPOSITE)
print(f"  {'Scenario':<10}  {'Price':>6}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>7}  Description")
hr()
for s in ["BEAR","BASE","BULL","XBULL"]:
    pp   = probs_proxy[s] * 100
    pm   = probs_mkt[s]   * 100
    gap  = pp - pm
    pr   = SCENARIOS[s][2]
    desc = SCENARIOS[s][3][:45]
    print(f"  {s:<10}  ${pr:>5}  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): ${ev_adj:.0f}  /  Proxy EV: ${ev_prx:.0f}  /  Market EV: ${ev_mkt:.0f}  /  Current: ${CURRENT_PRICE:.0f}")
hr()
print(f"  Downside  (-> Bear ${bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (-> Bull ${bull_price}):   {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b:.2f}x")
print(f"  Signal    :  {signal_full}")
print()
print(f"  Market composite {MARKET_COMPOSITE:.2f} reflects pricing roughly between BASE and BULL")
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees room-night growth + alt-accom mix gains, tempered by AI-disintermediation SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing room-night/buyback trajectory.' if ADJ_GAP>0 else 'model roughly agrees with market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) Room-night growth re-acceleration -> >=9% confirms BULL international expansion")
print(f"  (2) AI travel-assistant attach -> Connected Trip AI revenue >$2B confirms distribution moat intact")
print(f"  (3) Alternative accommodation mix -> >38% confirms vacation-rental supply growth structural")
print(f"  (4) Buyback pace -> share count <32M confirms continued EPS-compounding tailwind")
print(f"  BUY $3850-{round(CURRENT_PRICE*0.95,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $5650  |  AVOID above $6200")
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
