"""
GM  ·  General Motors Company  ·  NYSE: GM
Bottom-up signal model  ·  Auto Manufacturing · ICE Cash Cow + EV Transition · Capital Returns
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "GM"
COMPANY       = "General Motors Company"
SECTOR        = "Auto Manufacturing · ICE Cash Cow + EV Transition · NYSE: GM"
CURRENT_PRICE = 55.00       # USD; as of 2026-06-11
VOL_52W_LOW   = 40.00
VOL_52W_HIGH  = 62.00
SHARES_OUT_M  = 1100.0      # millions; aggressive ongoing buyback (down from ~1400M)

# Dividend
ANNUAL_DIV    = 0.50        # $/share

# ── ICE PROFITABILITY vs EV LOSSES ANALYSIS (company-specific) ────────────────
ICE_NA_OP_MARGIN   = 0.10   # North America ICE (trucks/SUVs) operating margin
EV_LOSS_PER_UNIT_B = 2.0    # annual EV segment operating loss ($B), narrowing
BUYBACK_PCT        = 0.08   # ~8%/yr share count reduction (very aggressive)
TAX_RATE           = 0.21

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 9.50    # FY2026E adj EPS
PE_TROUGH = 4       # min P/E at crisis trough (cyclical auto, 2008/2020 lows)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $38

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 6.00, 5,    30, "Recession hits truck/SUV demand + price wars; EV losses widen; EPS $6.00 -> 5x distress P/E"),
    "BASE":  ( 9.50, 5.8,  55, "ICE trucks/SUVs remain highly profitable; EV losses narrow; aggressive buyback; EPS $9.50 -> 5.8x P/E"),
    "BULL":  (11.50, 7,    80, "EV segment reaches breakeven; pricing discipline holds; multiple re-rates toward peers; EPS $11.50 -> 7x P/E"),
    "XBULL": (13.50, 8,   108, "EV profitability inflection plus continued buyback compounds EPS; market re-rates GM as a tech-adjacent compounder; EPS $13.50 -> 8x peak P/E"),
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
        "name":       "North America ICE (trucks/SUVs) operating margin",
        "weight":     0.25,
        "thresholds": ("<7%",    "≥9%",   "≥10%",   "≥12%"),
        "now":        "~10%",
        "score":      3,
        "comment":    "~10%; full-size trucks/SUVs (Silverado, Tahoe, Suburban) remain the profit engine",
    },
    {
        "name":       "EV segment loss trajectory (YoY narrowing)",
        "weight":     0.20,
        "thresholds": ("widening","flat",  "narrowing","near breakeven"),
        "now":        "narrowing",
        "score":      3,
        "comment":    "EV losses narrowing as battery cell costs fall (Ultium) and volumes scale",
    },
    {
        "name":       "Buyback pace (% of shares retired/yr)",
        "weight":     0.20,
        "thresholds": ("<3%",    "≥5%",   "≥7%",    "≥9%"),
        "now":        "~8%",
        "score":      4,
        "comment":    "~8%/yr — among the most aggressive buyback programs in the S&P 500",
    },
    {
        "name":       "Pricing discipline / incentive levels (vs industry)",
        "weight":     0.15,
        "thresholds": ("rising fast","rising","stable", "falling"),
        "now":        "stable",
        "score":      3,
        "comment":    "Incentives stable vs prior year; production discipline avoiding oversupply",
    },
    {
        "name":       "China JV / international results",
        "weight":     0.10,
        "thresholds": ("large losses","losses","breakeven","profitable"),
        "now":        "losses",
        "score":      2,
        "comment":    "China JV remains a drag; restructuring underway but not yet a tailwind",
    },
    {
        "name":       "Cruise/AV (autonomous) optionality progress",
        "weight":     0.10,
        "thresholds": ("wound down","paused","scaling", "commercial"),
        "now":        "paused",
        "score":      2,
        "comment":    "Cruise robotaxi ambitions scaled back; optionality value is now minimal near-term",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Best-in-class capital returns — ~8%/yr buyback is a structural EPS tailwind regardless of cycle",            +0.6, 0.30),
    ("+", "Full-size truck/SUV franchise — durable, high-margin profit pool that funds the EV transition",              +0.5, 0.20),
    ("-", "Deep cyclicality — auto demand and pricing highly sensitive to rates/recession; thin GAAP margins",          -0.5, 0.25),
    ("-", "EV transition execution risk — losses could widen again if demand slows or competition intensifies",         -0.4, 0.15),
    ("-", "China JV drag — ongoing losses with uncertain restructuring timeline",                                        -0.2, 0.10),
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
CONS_EPS_2YR = 11.00    # conservative FY2028E: ICE margins hold, buyback compounding continues
CONS_PE_2YR  = 6.0      # floor multiple (modest re-rate)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Auto Manufacturing / ICE Cash Cow + EV Transition")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① ICE PROFITABILITY vs EV LOSSES ANALYSIS ──────────────────────────────
print()
print("  ICE TRUCK/SUV PROFITS vs EV LOSSES vs BUYBACK ANALYSIS  (the core GM tension)")
hr()
shares_b = SHARES_OUT_M / 1000
total_na_rev_b = 110.0
print(f"  Estimated NA ICE revenue base: ~${total_na_rev_b:.0f}B  (trucks/SUVs at ~{ICE_NA_OP_MARGIN*100:.0f}% op margin)")
print(f"  Estimated annual EV segment operating loss: ~${EV_LOSS_PER_UNIT_B:.1f}B  (narrowing YoY)")
print()
print(f"  BUYBACK COMPOUNDING  (~{BUYBACK_PCT*100:.0f}%/yr share count reduction adds directly to EPS growth")
print(f"  independent of operating results — GM's primary value-creation lever in this scenario set).")
print()
print(f"  NA OP MARGIN SENSITIVITY  (incremental EPS from ICE margin changes):")
print(f"  {'NA op margin':<20}  {'Op income chg ($B)':>18}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for m in [0.07, 0.085, 0.10, 0.12]:
    op_chg = total_na_rev_b * (m - ICE_NA_OP_MARGIN)
    inc_eps = op_chg * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {m*100:.1f}% margin            {op_chg:>+15.1f}B    {inc_eps:>+.2f}     {eps_2yr:>+.2f}")

print()
print(f"  BEAR (${bear_price}) requires: a recession cuts truck/SUV demand and forces price wars (NA margin")
print(f"  compresses toward ~7%), EV losses widen again, AND the multiple compresses to a 5x distress level.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (NA ICE margin + EV losses + buybacks + pricing + China JV + AV optionality)")
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
    ("NA ICE operating margin",                   "~10%",   "<7%",   "-3pp",   "Recession-driven price wars erode truck/SUV pricing power"),
    ("EV segment loss trajectory",                "narrowing","widening","reverse","Demand softens / competition intensifies, EV losses re-widen"),
    ("Buyback pace (%/yr)",                       "~8%",    "<3%",   "-5pp",   "Free cash flow pressured in a downturn, capital return slows sharply"),
    ("Pricing/incentive levels",                  "stable", "rising fast","worse","Industry-wide oversupply forces heavy incentives"),
    ("China JV results",                          "losses", "large losses","worse","Restructuring stalls, JV losses deepen further"),
    ("AV/Cruise optionality",                     "paused", "wound down","worse", "Remaining AV investment fully written off"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A recession cuts North American truck/SUV demand sharply, forcing price wars that")
print(f"  compress NA margins toward 7%, while EV losses widen again on softer EV demand. EPS falls to")
print(f"  ~$6.00; the multiple compresses to a 5x distress P/E = ${bear_price}.")

# ─── ③ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS x min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}")
print(f"  Min viable P/E at trough:      {PE_TROUGH}x  (cyclical auto, 2008/2020-style trough multiple)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct>=0 else 'below'} trough floor)")
print()
print(f"  Premium to EPP reflects the market pricing in some credit for the buyback program and ICE cash flows.")
print(f"  Bear ${bear_price} is BELOW EPP ${EPP:.0f} — the model's bear case is more severe than even a trough-multiple floor,")
print(f"  reflecting how punishing a simultaneous demand/EV-loss/multiple shock would be.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+1.00:.2f} x {PE_TROUGH}x = ${(EPP_EPS+1.0)*PE_TROUGH:.0f} EPP — buyback-driven EPS growth lifts the floor.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: ICE margins hold, buyback compounding continues)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (ICE margins hold + ~8%/yr buyback compounding)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (modest re-rate from current ~5.8x)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f} x 2)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — the buyback alone provides a")
print(f"  meaningful EPS tailwind even if the ICE/EV mix doesn't materially improve.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.35
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (high; classic deep-cyclical auto profile)")
print(f"  Beta vs S&P 500:      1.40  (well above market; deep cyclical)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (2008/2020-style demand collapse; tail risk, not base case)")
print(f"  -> Auto cycle / interest rates are the PRIMARY catalyst; rate cuts + stable demand = upside;")
print(f"     recession = -45%+ downside.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — mid-range; not stretched given the low absolute multiple.")
print(f"  -> BUY $42-$48  |  TRIM $62+  |  AVOID above $70")

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
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees buyback compounding + ICE cash flows, tempered by deep cyclicality SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing the buyback compounding story.' if ADJ_GAP>0 else 'model roughly agrees with market pricing on a deeply cyclical, low-multiple business.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) NA ICE margin -> hold >=10% confirms truck/SUV franchise durability")
print(f"  (2) EV segment losses -> continued narrowing toward breakeven")
print(f"  (3) Buyback pace -> sustained ~8%/yr share count reduction compounds EPS")
print(f"  (4) China JV -> stabilization or restructuring resolution removes a drag")
print(f"  BUY $42-{round(CURRENT_PRICE*0.90,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $62  |  AVOID above $70")
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
