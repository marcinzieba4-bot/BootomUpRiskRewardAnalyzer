"""
LOW  ·  Lowe's Companies, Inc.  ·  NYSE: LOW
Bottom-up signal model  ·  Home Improvement Retail / Pro Customer / Omnichannel
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "LOW"
COMPANY       = "Lowe's Companies, Inc."
SECTOR        = "Home Improvement Retail · Pro Customer · Omnichannel · NYSE: LOW"
CURRENT_PRICE = 245.00      # USD; as of 2026-06-11
VOL_52W_LOW   = 205.00      # April 2026 housing-slowdown trough
VOL_52W_HIGH  = 290.00      # late 2025 rate-cut rally peak
SHARES_OUT_M  = 545.0       # millions; aggressive buyback (down from ~565M)

# Dividend: long-running Dividend King
ANNUAL_DIV    = 4.80        # $/share FY2026 (quarterly $1.20)

# ── PRO PENETRATION vs DIY HOUSING-CYCLE OFFSET CONSTANTS (company-specific calculator) ─
# Revenue breakdown FY2026E ($B)
TOTAL_REV_B        = 84.0   # total revenue
PRO_REV_B          = 29.0   # Pro customer revenue (~35% of total, growing)
DIY_REV_B          = 55.0   # DIY / consumer revenue
ONLINE_PEN_PCT     = 0.13   # online penetration of total sales

PRO_OP_MARGIN      = 0.15   # Pro segment incremental operating margin (higher ticket, repeat business)
DIY_OP_MARGIN      = 0.115  # DIY segment operating margin
PRO_GROWTH_RATE    = 0.09   # 9% YoY Pro revenue growth (MyLowe's Pro Rewards, Pro loyalty push)
TAX_RATE           = 0.24   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 12.40   # FY2026E adj EPS (consensus $12.10-$12.70)
PE_TROUGH = 13      # min P/E at crisis trough (2008-09 was ~10-12x; brand/scale supports floor)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $161

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 8.50, 14,  119, "Housing market freeze; comps negative for 3+ years; DIY discretionary collapses; EPS $8.50 -> 14x distress P/E"),
    "BASE":  (12.40, 18,  223, "Pro penetration grows steadily; comps flat-to-positive; modest housing recovery; EPS $12.40 -> 18x P/E"),
    "BULL":  (15.50, 20,  310, "Housing turnover recovers (rate cuts); Pro segment >40% of mix; comps +4-6%; EPS $15.50 -> 20x premium P/E"),
    "XBULL": (19.50, 22,  429, "Multi-year housing supercycle; Pro ecosystem (Lowe's One Roof Pro) dominant; EPS $19.50 -> 22x peak P/E"),
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
        "name":       "Comparable sales — YoY growth",
        "weight":     0.25,
        "thresholds": ("<-3%",   "≥0%",   "≥2.5%",  "≥5%"),
        "now":        "+1.1%",
        "score":      2,
        "comment":    "+1.1% YoY; Pro and online offsetting soft DIY big-ticket discretionary",
    },
    {
        "name":       "Pro customer revenue — YoY growth",
        "weight":     0.25,
        "thresholds": ("<2%",    "≥6%",   "≥9%",    "≥14%"),
        "now":        "+9%",
        "score":      3,
        "comment":    "+9% YoY; MyLowe's Pro Rewards + Lowe's One Roof Pro acquisition integration on track",
    },
    {
        "name":       "Online / digital sales penetration",
        "weight":     0.15,
        "thresholds": ("<10%",   "≥12%",  "≥14%",   "≥17%"),
        "now":        "~13%",
        "score":      2,
        "comment":    "~13%; BOPIS and same-day delivery expanding but below HD penetration levels",
    },
    {
        "name":       "Operating margin trend",
        "weight":     0.15,
        "thresholds": ("<11%",   "≥12.5%","≥13.5%", "≥15%"),
        "now":        "~13.0%",
        "score":      2,
        "comment":    "~13.0%; supply chain efficiency gains offset by SG&A deleverage on soft DIY comps",
    },
    {
        "name":       "Housing turnover / existing home sales (annualized, M units)",
        "weight":     0.10,
        "thresholds": ("<3.5M",  "≥4.0M", "≥4.5M",  "≥5.2M"),
        "now":        "~3.9M",
        "score":      1,
        "comment":    "~3.9M; mortgage rates still elevated (~6.3%); housing turnover near multi-decade lows",
    },
    {
        "name":       "Share buyback pace (annual reduction in share count)",
        "weight":     0.10,
        "thresholds": ("<1%",    "≥2%",   "≥3.5%",  "≥5%"),
        "now":        "~3.5%",
        "score":      3,
        "comment":    "~3.5%; consistent ~$4-5B/yr buybacks compounding EPS even with flat earnings",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Pro customer ecosystem moat — Lowe's One Roof Pro (acquired ADG); MyLowe's Pro Rewards loyalty",  +0.6, 0.25),
    ("+", "Capital return discipline — Dividend King (60+ yrs); ~3.5%/yr buyback compounds EPS through cycle", +0.5, 0.20),
    ("+", "Supply chain modernization — bulk distribution centers, cross-dock network lowering cost-to-serve", +0.4, 0.15),
    ("-", "Housing cycle dependency — DIY big-ticket (kitchens, appliances) deferred until rates fall",       -0.6, 0.25),
    ("-", "Competitive intensity — Home Depot's larger Pro/SRS Distribution scale; Amazon/Menards price pressure", -0.4, 0.15),
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
CONS_EPS_2YR = 14.00    # conservative FY2028E: flat comps + buyback compounding
CONS_PE_2YR  = 17       # floor multiple (in line with historical trough-to-mid range)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Home Improvement Retail / Pro / Omnichannel")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRO GROWTH vs HOUSING CYCLE ANALYSIS ─────────────────────────────────
print()
print("  PRO PENETRATION GROWTH vs HOUSING-CYCLE DIY HEADWIND ANALYSIS  (the core LOW tension)")
hr()

print(f"  FY2026E Revenue Mix:")
print(f"  {'Pro customer revenue':<36}  ${PRO_REV_B:>5.1f}B  ({PRO_REV_B/TOTAL_REV_B*100:.0f}% of total; +{PRO_GROWTH_RATE*100:.0f}% YoY; {PRO_OP_MARGIN*100:.1f}% incr. margin)")
print(f"  {'DIY / consumer revenue':<36}  ${DIY_REV_B:>5.1f}B  ({DIY_REV_B/TOTAL_REV_B*100:.0f}%; {DIY_OP_MARGIN*100:.1f}% op margin; housing-sensitive)")
print(f"  {'Online / digital penetration':<36}  {ONLINE_PEN_PCT*100:>5.1f}%  of total sales")
hr()
print(f"  Total FY2026E:                          ${TOTAL_REV_B:>5.1f}B")
print()

shares_b = SHARES_OUT_M / 1000
print(f"  PRO GROWTH UPSIDE  (incremental EPS from Pro revenue growth above/below {PRO_GROWTH_RATE*100:.0f}%):")
print(f"  {'Pro YoY growth':<20}  {'Rev/yr':>10}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.02, 0.05, 0.09, 0.14]:
    rev_inc = PRO_REV_B * g
    inc_eps = rev_inc * PRO_OP_MARGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% Pro growth          +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
diy_y1 = DIY_REV_B * 0.01  # each 1pp DIY comp decline
diy_eps1 = diy_y1 * DIY_OP_MARGIN * (1 - TAX_RATE) / shares_b
print(f"  HOUSING-CYCLE DIY SENSITIVITY  (each -1pp DIY comp = -${diy_eps1:.2f}/EPS/yr):")
print(f"  Current DIY comp ~flat -> -3pp housing freeze = -${diy_eps1*3:.2f}/EPS  -> over 2yr = -${diy_eps1*3*2:.2f}/EPS")
print()
buyback_eps = EPP_EPS * 0.035
print(f"  BUYBACK COMPOUNDING  (~3.5%/yr share count reduction at flat earnings = +${buyback_eps:.2f}/EPS/yr)")
print()
print(f"  BEAR (${bear_price}) requires: housing market freeze AND DIY comps negative for 3+ years AND")
print(f"  Pro growth decelerates to <2% — simultaneously.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (comps + Pro growth + digital + housing turnover + buybacks)")
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
    ("Comparable sales YoY",                    "+1.1%",  "<-3%",  "-4pp",   "Recession + housing freeze; DIY discretionary spend collapses"),
    ("Pro customer revenue YoY",                "+9%",    "<2%",   "-7pp",   "Construction/renovation activity stalls; Pro deferred projects"),
    ("Online penetration",                      "~13%",   "<10%",  "-3pp",   "Digital investment underperforms vs Home Depot/Amazon"),
    ("Operating margin",                        "~13.0%", "<11%",  "-2pp",   "SG&A deleverage on negative comps; promotional pricing pressure"),
    ("Housing turnover (M units)",              "~3.9M",  "<3.5M", "-0.4M",  "Mortgage rates rise further (>7.5%); 'lock-in effect' worsens"),
    ("Buyback pace",                            "~3.5%",  "<1%",   "-2.5pp", "FCF pressured; capital allocation shifts to deleveraging"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A recession combined with persistently elevated mortgage rates (>7.5%) extends")
print(f"  the housing 'lock-in effect' for another multi-year cycle, crushing DIY big-ticket discretionary")
print(f"  spend (kitchens, appliances, flooring) while Pro construction activity also stalls. EPS falls")
print(f"  to ~$8.50; multiple compresses to 14x distress P/E = ${bear_price}.")

# ─── ③ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS x min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}  (consensus $12.10-$12.70)")
print(f"  Min viable P/E at trough:      {PE_TROUGH}x  (2008-09 trough was ~10-12x; brand/scale supports floor)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct>=0 else 'below'} trough floor)")
print()
print(f"  Premium to EPP reflects buyback-driven EPS compounding plus eventual housing-cycle normalization.")
print(f"  Bear ${bear_price} is BELOW EPP ${EPP:.0f} — requires BOTH EPS collapse AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+0.80:.2f} x {PE_TROUGH}x = ${(EPP_EPS+0.8)*PE_TROUGH:.0f} EPP — stock catches up as buybacks compound.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: flat comps, buyback compounding, dividend)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (flat-to-modest comps + ~3.5%/yr buyback compounding)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (in line with historical trough-to-mid range)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f} x 2; Dividend King, 60+ yrs of increases)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — buyback compounding and the dividend provide a")
print(f"  reasonable floor even without a housing-cycle recovery; a rate-cut driven turnover rebound is pure upside.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.24
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%; Dividend King, 60+ consecutive yrs)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (large-cap retail; housing-cycle + rate-sensitivity)")
print(f"  Beta vs S&P 500:      1.05  (near market; less volatile than pure homebuilders)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (2008-09 LOW fell ~50%+ from peak; achievable in a housing freeze)")
print(f"  -> Mortgage rate trajectory is the PRIMARY catalyst; rates <6% = housing turnover recovery upside;")
print(f"     rates >7.5% sustained = -20%+ downside.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — mid-range; not pricing extreme outcomes either way.")
print(f"  -> BUY $205-$235  |  TRIM $290+  |  AVOID above $320")

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
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees Pro growth + buyback compounding, tempered by housing-cycle SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing Pro/buyback trajectory.' if ADJ_GAP>0 else 'model roughly agrees with market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) Comparable sales inflection -> sustained positive comps confirms housing trough")
print(f"  (2) Pro revenue growth -> >=10% confirms One Roof Pro integration delivering share gains")
print(f"  (3) Mortgage rate trajectory -> sustained <6% triggers housing turnover recovery (BULL case)")
print(f"  (4) Buyback pace -> >=4%/yr share reduction confirms continued EPS-compounding tailwind")
print(f"  BUY $205-{round(CURRENT_PRICE*0.95,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $290  |  AVOID above $320")
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
