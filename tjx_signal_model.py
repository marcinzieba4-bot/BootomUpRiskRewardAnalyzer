"""
TJX  ·  The TJX Companies, Inc.  ·  NYSE: TJX
Bottom-up signal model  ·  Off-Price Retail / TJ Maxx · Marshalls · HomeGoods · Sierra · Winners
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "TJX"
COMPANY       = "The TJX Companies, Inc."
SECTOR        = "Off-Price Retail · TJ Maxx / Marshalls / HomeGoods / Sierra / Winners · NYSE: TJX"
CURRENT_PRICE = 132.00      # USD; as of 2026-06-11
VOL_52W_LOW   = 105.00      # April 2026 tariff-fear trough
VOL_52W_HIGH  = 145.00      # late 2025 trade-down rally peak
SHARES_OUT_M  = 1090.0      # millions; aggressive buyback (down from ~1140M)

# Dividend
ANNUAL_DIV    = 1.70        # $/share FY2026 (quarterly $0.425)

# ── TRADE-DOWN TAILWIND vs TARIFF/SOURCING COST ANALYSIS (company-specific calculator) ─
# Revenue / segment breakdown FY2026E ($B)
MARMAXX_REV_B      = 56.0   # TJ Maxx + Marshalls (US)
HOMEGOODS_REV_B    = 11.5   # HomeGoods + Homesense (US)
TJX_INTL_REV_B     = 18.5   # Europe (TK Maxx) + Australia
TJX_CANADA_REV_B   = 5.5    # Winners, HomeSense, Marshalls Canada

US_OP_MARGIN      = 0.115   # US segments operating margin
INTL_OP_MARGIN    = 0.095   # International segments operating margin
COMP_GROWTH_RATE  = 0.03    # 3% YoY consolidated comp sales growth (Q1 2026 run-rate)
TARIFF_DRAG_PCT   = 0.005   # ~50bps gross margin drag from tariffs on imported sourcing
TAX_RATE          = 0.25    # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 4.55    # FY2026E adj EPS (consensus $4.45-$4.65)
PE_TROUGH = 16      # min P/E at crisis trough (2020 COVID lows ~14-16x on normalized EPS)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $73

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 3.30, 18,   59, "Consumer trade-down reverses on recovery + tariff costs un-passable; comps negative; EPS $3.30 -> 18x distress P/E"),
    "BASE":  ( 4.55, 24,  109, "Comps +2-4%; trade-down tailwind persists; tariff drag managed via buying power; EPS $4.55 -> 24x P/E"),
    "BULL":  ( 5.40, 27,  146, "Recession-driven trade-down accelerates; international (TK Maxx Europe) expansion; EPS $5.40 -> 27x premium P/E"),
    "XBULL": ( 6.50, 29,  189, "Off-price structurally gains permanent share from full-price/department stores; EPS $6.50 -> 29x peak P/E"),
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
        "name":       "Consolidated comparable sales — YoY growth",
        "weight":     0.25,
        "thresholds": ("<0%",    "≥2%",   "≥4%",    "≥6%"),
        "now":        "+3%",
        "score":      2,
        "comment":    "+3% YoY; trade-down from full-price/department stores continues amid macro uncertainty",
    },
    {
        "name":       "Gross margin trend (vs tariff/sourcing cost pressure)",
        "weight":     0.20,
        "thresholds": ("<28%",   "≥29%",  "≥30%",   "≥31.5%"),
        "now":        "~30%",
        "score":      3,
        "comment":    "~30%; buying organization (1000+ buyers, 21000+ vendors) absorbing tariff costs via flexible sourcing",
    },
    {
        "name":       "International segment growth (TK Maxx Europe + Australia)",
        "weight":     0.15,
        "thresholds": ("<2%",    "≥4%",   "≥7%",    "≥10%"),
        "now":        "+6%",
        "score":      3,
        "comment":    "+6%; European off-price penetration still low vs US, long runway for store growth",
    },
    {
        "name":       "Inventory turns / freshness (inventory growth vs sales growth)",
        "weight":     0.15,
        "thresholds": ("inv>sales+5pp","inv≈sales","inv<sales-2pp","inv<sales-5pp"),
        "now":        "inv<sales-2pp",
        "score":      3,
        "comment":    "Inventory growth running below sales growth — disciplined buying, fresh assortments driving traffic",
    },
    {
        "name":       "Operating margin trend",
        "weight":     0.15,
        "thresholds": ("<10%",   "≥11%",  "≥11.7%", "≥12.5%"),
        "now":        "~11.5%",
        "score":      2,
        "comment":    "~11.5%; near record highs; freight/supply-chain efficiency offsetting wage inflation",
    },
    {
        "name":       "New store growth (annual net unit additions)",
        "weight":     0.10,
        "thresholds": ("<60",    "≥80",   "≥100",   "≥130"),
        "now":        "~100",
        "score":      3,
        "comment":    "~100 net new stores/yr; long-term target of 6300+ stores (from ~5000 today)",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Off-price buying moat — flexible, opportunistic sourcing from 21000+ vendors absorbs tariff/oversupply shocks", +0.7, 0.25),
    ("+", "Trade-down demand resilience — counter-cyclical: gains share in both strong and weak consumer environments",     +0.6, 0.20),
    ("+", "International white space — TK Maxx Europe penetration far below US; long runway for unit growth",              +0.5, 0.20),
    ("-", "Tariff/sourcing cost pressure — import-heavy model exposed to trade policy shifts; gross margin at risk",        -0.4, 0.20),
    ("-", "Valuation premium — trades at premium multiple vs historical average; limited margin of safety on multiple",     -0.3, 0.15),
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
CONS_EPS_2YR = 5.10    # conservative FY2028E: comps moderate, buyback compounding continues
CONS_PE_2YR  = 22      # floor multiple (slightly below current; reflects tariff-cost discount)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Off-Price Retail / Trade-Down Beneficiary")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① TRADE-DOWN TAILWIND vs TARIFF COST ANALYSIS ──────────────────────────
print()
print("  TRADE-DOWN TAILWIND vs TARIFF/SOURCING COST ANALYSIS  (the core TJX tension)")
hr()

total_rev_b = MARMAXX_REV_B + HOMEGOODS_REV_B + TJX_INTL_REV_B + TJX_CANADA_REV_B
print(f"  FY2026E Segment Revenue:")
print(f"  {'Marmaxx (TJ Maxx + Marshalls US)':<36}  ${MARMAXX_REV_B:>5.1f}B  ({MARMAXX_REV_B/total_rev_b*100:.0f}% of total; {US_OP_MARGIN*100:.1f}% op margin)")
print(f"  {'HomeGoods + Homesense':<36}  ${HOMEGOODS_REV_B:>5.1f}B  ({HOMEGOODS_REV_B/total_rev_b*100:.0f}%; {US_OP_MARGIN*100:.1f}% op margin)")
print(f"  {'TJX International (TK Maxx Europe/AU)':<36}  ${TJX_INTL_REV_B:>5.1f}B  ({TJX_INTL_REV_B/total_rev_b*100:.0f}%; {INTL_OP_MARGIN*100:.1f}% op margin)")
print(f"  {'TJX Canada (Winners/HomeSense/Marshalls)':<36}  ${TJX_CANADA_REV_B:>5.1f}B  ({TJX_CANADA_REV_B/total_rev_b*100:.0f}%; {INTL_OP_MARGIN*100:.1f}% op margin)")
hr()
print(f"  Total FY2026E:                          ${total_rev_b:>5.1f}B")
print()

shares_b = SHARES_OUT_M / 1000
print(f"  COMP GROWTH UPSIDE  (incremental EPS from comp growth above/below {COMP_GROWTH_RATE*100:.0f}%):")
print(f"  {'Comp YoY growth':<20}  {'Rev/yr':>10}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.00, 0.02, 0.03, 0.05]:
    rev_inc = total_rev_b * g
    inc_eps = rev_inc * US_OP_MARGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% comp growth         +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
tariff_drag = total_rev_b * TARIFF_DRAG_PCT * (1 - TAX_RATE) / shares_b
print(f"  TARIFF DRAG  (each 50bps of gross margin lost to tariffs = -${tariff_drag:.2f}/EPS/yr):")
print(f"  Current ~50bps drag = -${tariff_drag:.2f}/EPS  -> over 2yr = -${tariff_drag*2:.2f}/EPS (if not offset by buying power)")
print()
print(f"  BEAR (${bear_price}) requires: trade-down reverses (consumer recovery shifts spend back to full-price)")
print(f"  AND tariff costs become un-passable AND comps turn negative — simultaneously.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (comps + gross margin + international + inventory + new stores)")
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
    ("Consolidated comp sales YoY",              "+3%",    "<0%",   "-3pp",   "Consumer recovery shifts spend back to full-price/department stores"),
    ("Gross margin",                             "~30%",   "<28%",  "-2pp",   "Tariff escalation outpaces buying-power offsets; markdown pressure"),
    ("International growth",                     "+6%",    "<2%",   "-4pp",   "European consumer slowdown; FX headwinds"),
    ("Inventory vs sales growth",                "inv<sales-2pp", "inv>sales+5pp", "+7pp", "Overbuying leads to markdown-heavy clearance, margin compression"),
    ("Operating margin",                         "~11.5%", "<10%",  "-1.5pp", "Wage inflation + freight costs outpace efficiency gains"),
    ("New store growth (units/yr)",              "~100",   "<60",   "-40",    "Real estate cost inflation slows expansion pace"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A sharp consumer recovery (real wage growth + lower rates) shifts spending back")
print(f"  toward full-price retail and department stores just as tariff costs escalate beyond what")
print(f"  TJX's buying organization can absorb via opportunistic sourcing. EPS falls to ~$3.30;")
print(f"  multiple compresses to 18x distress P/E = ${bear_price}.")

# ─── ③ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS x min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}  (consensus $4.45-$4.65)")
print(f"  Min viable P/E at trough:      {PE_TROUGH}x  (2020 COVID lows ~14-16x on normalized EPS)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct>=0 else 'below'} trough floor)")
print()
print(f"  Premium to EPP reflects defensive, counter-cyclical growth profile and consistent buyback.")
print(f"  Bear ${bear_price} is BELOW EPP ${EPP:.0f} — requires BOTH EPS collapse AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+0.40:.2f} x {PE_TROUGH}x = ${(EPP_EPS+0.4)*PE_TROUGH:.0f} EPP — stock catches up quickly.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: comps moderate, buyback compounding continues)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (low-single-digit comps + new store growth + buybacks)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (slightly below current; tariff-cost discount)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f} x 2)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — counter-cyclical comp growth plus")
print(f"  international unit expansion and buybacks support steady EPS compounding even in a soft macro.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.20
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%; consistent dividend growth)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (low for retail; defensive/counter-cyclical profile)")
print(f"  Beta vs S&P 500:      0.85  (below market; defensive trade-down beneficiary)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (2020 TJX fell ~50% from peak intra-COVID; less likely in normal cycle)")
print(f"  -> Tariff policy trajectory is the PRIMARY catalyst; tariff rollback = margin upside;")
print(f"     escalation = -15%+ downside if un-passable.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — mid-range; defensive profile not stretched.")
print(f"  -> BUY $105-$120  |  TRIM $145+  |  AVOID above $160")

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
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees comp growth + international expansion, tempered by tariff/valuation SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing comp/international trajectory.' if ADJ_GAP>0 else 'model roughly agrees with market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) Comp sales sustainability -> >=4% confirms trade-down tailwind durable")
print(f"  (2) Gross margin trend -> stable >=30% confirms buying power absorbs tariff costs")
print(f"  (3) International unit growth -> TK Maxx Europe expansion accelerates (BULL case)")
print(f"  (4) Inventory discipline -> inventory growth below sales growth confirms fresh assortments")
print(f"  BUY $105-{round(CURRENT_PRICE*0.95,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $145  |  AVOID above $160")
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
