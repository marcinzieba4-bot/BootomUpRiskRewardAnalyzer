"""
AZO  ·  AutoZone, Inc.  ·  NYSE: AZO
Bottom-up signal model  ·  Auto Parts Retail · DIY + Commercial (DIFM) · Buyback Compounder
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "AZO"
COMPANY       = "AutoZone, Inc."
SECTOR        = "Auto Parts Retail · DIY / Commercial (DIFM) · NYSE: AZO"
CURRENT_PRICE = 3500.00    # USD; as of 2026-06-11
VOL_52W_LOW   = 3000.00
VOL_52W_HIGH  = 4050.00
SHARES_OUT_M  = 16.5       # millions; one of the most aggressive buybacks in the market

# Dividend
ANNUAL_DIV    = 0.00       # no dividend; 100% of FCF to buybacks

# ── COMP SALES / DIFM MIX ANALYSIS (company-specific) ─────────────────────────
COMP_GROWTH_RATE = 0.03    # ~3% YoY comparable store sales growth (DIY+DIFM blend)
DIFM_MIX         = 0.45    # Commercial (DIFM) share of revenue, growing
OP_MARGIN        = 0.204   # operating margin (best-in-class for the category)
TAX_RATE         = 0.24
BUYBACK_PCT      = 0.06    # ~6%/yr share count reduction (very aggressive, debt-funded)

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 165.00  # FY2026E adj EPS
PE_TROUGH = 15      # min P/E at crisis trough (2008/2020 lows on normalized EPS)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $2475

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (140.00, 18,  2520, "Recession hits DIY discretionary spend + commercial volumes soften; EPS $140 -> 18x distress P/E"),
    "BASE":  (165.00, 21,  3465, "Comps +2-4%; DIFM share gains continue; aggressive buyback compounds EPS; EPS $165 -> 21x P/E"),
    "BULL":  (185.00, 24,  4440, "Commercial hub buildout accelerates DIFM penetration; international (Mexico/Brazil) scales faster; EPS $185 -> 24x premium P/E"),
    "XBULL": (210.00, 27,  5670, "Aging vehicle fleet extends multi-year aftermarket demand tailwind; buyback-driven EPS compounding accelerates; EPS $210 -> 27x peak P/E"),
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
        "name":       "Comparable store sales — YoY growth",
        "weight":     0.25,
        "thresholds": ("<0%",   "≥2%",   "≥3%",   "≥5%"),
        "now":        "~3%",
        "score":      3,
        "comment":    "~3%; aging vehicle fleet (avg ~12.6yrs) sustains DIY+DIFM demand through the cycle",
    },
    {
        "name":       "Commercial (DIFM) revenue mix",
        "weight":     0.15,
        "thresholds": ("<40%",  "≥43%",  "≥46%",  "≥50%"),
        "now":        "~45%",
        "score":      3,
        "comment":    "~45%; hub/mega-hub distribution buildout continues to take professional-installer share",
    },
    {
        "name":       "Operating margin",
        "weight":     0.15,
        "thresholds": ("<17%",  "≥18.5%", "≥20%", "≥21.5%"),
        "now":        "~20.4%",
        "score":      3,
        "comment":    "~20.4%; best-in-class retail margin from scale, private-label mix, and supply-chain efficiency",
    },
    {
        "name":       "New store / distribution growth",
        "weight":     0.10,
        "thresholds": ("<2%",   "≥3%",   "≥4%",   "≥5%"),
        "now":        "~4%",
        "score":      3,
        "comment":    "~4%; steady domestic unit growth plus accelerating Mexico/Brazil store openings",
    },
    {
        "name":       "Buyback pace (% of shares retired/yr)",
        "weight":     0.20,
        "thresholds": ("<3%",   "≥5%",   "≥6%",   "≥8%"),
        "now":        "~6%",
        "score":      3,
        "comment":    "~6%/yr; debt-funded, near-continuous repurchases have shrunk the float for two decades",
    },
    {
        "name":       "International (Mexico/Brazil) expansion",
        "weight":     0.15,
        "thresholds": ("<5%",   "≥8%",   "≥10%",  "≥13%"),
        "now":        "~9%",
        "score":      3,
        "comment":    "~9% unit growth; long runway for store-count expansion outside the US",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Multi-decade aggressive buyback (~6%/yr) is one of the most powerful per-share compounding engines in the market", +0.5, 0.25),
    ("+", "Dual DIY/DIFM model and aging vehicle fleet provide demand resilience across the economic cycle",                  +0.4, 0.20),
    ("+", "Commercial hub network and international expansion (Mexico/Brazil) extend the unit-growth runway",                +0.3, 0.15),
    ("-", "Negative tangible book value / high leverage from debt-funded buybacks raises balance-sheet risk in a downturn",   -0.4, 0.20),
    ("-", "Premium per-share price and valuation leave limited margin of safety if comps decelerate",                          -0.3, 0.20),
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
CONS_EPS_2YR = 195.00  # conservative FY2028E: comps + buyback compounding continues
CONS_PE_2YR  = 19       # floor multiple (slightly below current)
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Auto Parts Retail / Buyback Compounder")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① COMP SALES / BUYBACK ANALYSIS ─────────────────────────────────────────
print()
print("  COMP SALES + BUYBACK ANALYSIS  (the core AZO earnings drivers)")
hr()
shares_b = SHARES_OUT_M / 1000
total_revenue_b = 19.0
print(f"  Estimated FY2026E revenue base: ~${total_revenue_b:.1f}B")
print()
print(f"  COMP SALES UPSIDE  (incremental EPS from comps at {OP_MARGIN*100:.1f}% operating margin):")
print(f"  {'Comp sales YoY growth':<20}  {'Rev/yr ($B)':>12}  {'EPS/yr':>10}  {'2yr EPS':>10}")
hr()
for g in [0.00, 0.02, 0.03, 0.05]:
    rev_inc = total_revenue_b * g
    inc_eps = rev_inc * OP_MARGIN * (1 - TAX_RATE) / shares_b
    eps_2yr = inc_eps * 2
    print(f"  {g*100:.0f}% comp sales growth      +${rev_inc:>5.2f}B    +${inc_eps:.2f}     +${eps_2yr:.2f}")

print()
print(f"  BUYBACK COMPOUNDING  (~{BUYBACK_PCT*100:.0f}%/yr share count reduction directly boosts EPS")
print(f"  regardless of revenue growth; debt-funded but supported by stable, recession-resilient cash flow).")
print()
print(f"  BEAR (${bear_price:.0f}) requires: a recession that hits both DIY discretionary spend AND")
print(f"  commercial (DIFM) volumes, while the multiple compresses to distress levels — together.")

# ─── ① SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (comp sales + DIFM mix + margin + new stores + buybacks + intl expansion)")
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
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price:.0f})")
hr()
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>7}  Trigger")
hr()
bear_triggers = [
    ("Comparable store sales YoY",                 "~3%",    "<0%",   "-3pp",   "Recession curtails DIY discretionary repair spend"),
    ("Commercial (DIFM) revenue mix",              "~45%",   "<40%",  "-5pp",   "Fleet/commercial customers cut maintenance budgets"),
    ("Operating margin",                           "~20.4%", "<17%",  "-3.4pp", "Wage/freight cost inflation outpaces pricing"),
    ("New store / distribution growth",            "~4%",    "<2%",   "-2pp",   "Capex pulled back amid tighter credit conditions"),
    ("Buyback pace (%/yr)",                        "~6%",    "<3%",   "-3pp",   "Higher rates raise cost of debt-funded buybacks"),
    ("International (Mexico/Brazil) expansion",    "~9%",    "<5%",   "-4pp",   "FX headwinds and slower regional consumer spend"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A recession curtails both DIY discretionary repair spend and commercial")
print(f"  fleet maintenance budgets while higher rates raise the cost of debt-funded buybacks.")
print(f"  EPS falls to ~$140; multiple compresses to 18x distress P/E = ${bear_price:.0f}.")

# ─── ③ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS x min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}")
print(f"  Min viable P/E at trough:      {PE_TROUGH}x  (2008/2020-era distress multiple)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct>=0 else 'below'} trough floor)")
print()
print(f"  Premium to EPP reflects the durable buyback-compounding moat and recession-resilient demand.")
print(f"  Bear ${bear_price:.0f} is above EPP ${EPP:.0f} — reflects the floor's resilience even in a downturn.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+15:.2f} x {PE_TROUGH}x = ${(EPP_EPS+15)*PE_TROUGH:.0f} EPP — buybacks compound the floor higher every year.")

# ─── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: comps moderate, buyback compounding continues)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (low-single-digit comps + ~6%/yr buybacks)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}x  (slightly below current)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (no dividend)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is {'POSITIVE' if cons_return > 0 else 'roughly NEUTRAL'} — buyback-driven share count reduction plus")
print(f"  steady comp sales growth support EPS compounding even in a soft macro.")

# ─── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.18
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  -  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (no dividend; capital returned via buybacks)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (below-market; defensive auto-aftermarket demand)")
print(f"  Beta vs S&P 500:      0.55  (below market; defensive)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  -  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price:.0f} requires:  ~{bear_sigmas:.1f}σ move  (AZO has historically been resilient even in recessions; tail risk, not base case)")
print(f"  -> Comp sales trajectory and buyback pace are the PRIMARY catalysts;")
print(f"     steady comps + buybacks = upside; recession + leverage stress = downside.")
print(f"  -> At {vol_pct*100:.0f}th pct of 52W range — mid range; not stretched relative to compounding profile.")
print(f"  -> BUY $3000-$3200  |  TRIM $4000+  |  AVOID above $4400")

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
    print(f"  {s:<10}  ${pr:>5.0f}  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): ${ev_adj:.0f}  /  Proxy EV: ${ev_prx:.0f}  /  Market EV: ${ev_mkt:.0f}  /  Current: ${CURRENT_PRICE:.0f}")
hr()
print(f"  Downside  (-> Bear ${bear_price:.0f}):  {downside_pct*100:.1f}%")
print(f"  Upside    (-> Bull ${bull_price:.0f}):   {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b:.2f}x")
print(f"  Signal    :  {signal_full}")
print()
print(f"  Market composite {MARKET_COMPOSITE:.2f} reflects pricing roughly between BASE and BULL")
print(f"  Adj composite {ADJ_COMPOSITE:.2f} = model sees comps + buyback compounding, tempered by leverage/valuation SCA")
print(f"  GAP {ADJ_GAP:+.2f}: {'model says market is under-pricing the buyback compounding story.' if ADJ_GAP>0 else 'model roughly agrees with market pricing.'}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) Comp sales -> sustained >=3% confirms aftermarket demand resilience")
print(f"  (2) Commercial (DIFM) mix -> continued share gains via hub network")
print(f"  (3) Buyback pace -> sustained >=6%/yr drives per-share EPS compounding")
print(f"  (4) International expansion -> Mexico/Brazil unit growth stays >=9%/yr")
print(f"  BUY $3000-{round(CURRENT_PRICE*0.90,0):.0f}  |  ACCUMULATE to ${round(CURRENT_PRICE*1.05,0):.0f}  |  TRIM above $4000  |  AVOID above $4400")
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
