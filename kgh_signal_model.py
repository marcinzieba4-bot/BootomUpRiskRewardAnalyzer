"""
KGH  ·  KGHM Polska Miedź S.A.  ·  WSE: KGH
Bottom-up signal model  ·  Copper & Silver Mining / Commodity Price Cycle
Currency: PLN (Polish złoty) — this model is denominated natively in PLN, not USD
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "KGH"
COMPANY       = "KGHM Polska Miedź S.A."
SECTOR        = "Copper & Silver Mining · Commodity Price Cycle · GPW: KGH (PLN)"
CURRENT_PRICE = 322.70      # PLN; close 2026-08-03
VOL_52W_LOW   = 125.55      # PLN
VOL_52W_HIGH  = 396.40      # PLN
SHARES_OUT_M  = 200.0       # millions
ANNUAL_DIV    = 8.00        # PLN/share; variable, tied to profits given commodity cyclicality

# ── PROFIT CONTRIBUTION BRIDGE (FY2026E, PLN millions net profit) ────────────
# Q1 2026 actual: net profit 3,529M zł — roughly 10.7x higher than Q1 2025 — on EBITDA of 5.46B zł
# (more than double the prior year), driven almost entirely by higher copper and silver prices;
# payable copper production was in line with budget at 176kt, silver production 329t (37koz).
# Q2 2026 results have not yet been reported as of this model's date. KGHM's own 52-week range
# (125.55–396.40 zł, more than a 3x swing) is the clearest evidence of how violently this business
# swings with metal prices — this is a commodity cyclical, not a steady compounder.
SEG_DATA = [
    # (segment, curr_profit_M, bear_profit_M, bull_profit_M, description)
    ("Copper segment profit",                    7500.0, 2500.0, 11000.0, "The core earnings driver; directly tracks LME copper prices and the PLN/USD exchange rate"),
    ("Silver & precious metals byproduct profit", 2794.0, 1000.0,  4500.0, "A high-margin byproduct stream that has become a meaningful profit contributor in its own right"),
]

# ── COMMODITY PRICE CYCLE CALCULATOR (the KGHM-specific angle) ───────────────
Q1_2026_NET_PROFIT_B       = 3.529  # PLN billions; Q1 2026 net profit, ~10.7x YoY
Q1_2026_EBITDA_B           = 5.46   # PLN billions; Q1 2026 EBITDA, more than double YoY
Q1_2026_COPPER_PRODUCTION_KT = 176  # thousand tonnes; payable copper production, in line with budget
Q1_2026_SILVER_PRODUCTION_T  = 329  # tonnes; silver production (~37koz)
FY26_WFE_52W_RANGE_MULTIPLE   = round(VOL_52W_HIGH / VOL_52W_LOW, 1)  # the scale of KGHM's own commodity-cycle swings

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 51.47       # PLN/share FY2026E; forward-P/E-implied from consensus
PE_PESSIMISTIC = 6.0         # trough P/E: a genuine commodity-miner-trough multiple — even in good years KGHM rarely re-rates much higher
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  (17.50, 6,  105, "Copper and silver prices revert sharply toward pre-rally levels as the current commodity cycle turns"),
    "BASE":  (55.00, 6.27, 345, "Metal prices hold roughly near current elevated levels, with production continuing near budget"),
    "BULL":  (77.50, 7,  543, "AI-infrastructure and EV-driven copper demand keeps prices elevated for longer than the market currently expects"),
    "XBULL": (95.00, 7.5, 713, "A genuine multi-year copper supercycle takes hold as global electrification and AI-datacenter power buildout both intensify demand"),
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
        "name":       "Net profit YoY growth",
        "weight":     0.20,
        "thresholds": ("<0%",    "≥50%",   "≥150%",  "≥300%"),
        "now":        "~+970%",
        "score":      4,
        "comment":    "Q1 2026 net profit ~10.7x Q1 2025 — an extraordinary, commodity-price-driven swing",
    },
    {
        "name":       "EBITDA growth YoY",
        "weight":     0.15,
        "thresholds": ("<0%",    "≥30%",   "≥70%",   "≥100%"),
        "now":        "+100%+",
        "score":      4,
        "comment":    "More than doubled YoY in Q1 — the clearest signal of how much operating leverage KGHM has to metal prices",
    },
    {
        "name":       "Copper production vs budget",
        "weight":     0.15,
        "thresholds": ("well below","below",  "on budget","above budget"),
        "now":        "on budget",
        "score":      3,
        "comment":    "176kt in Q1, in line with budget — the operational side is executing cleanly, letting price do the work",
    },
    {
        "name":       "Silver/precious metals contribution",
        "weight":     0.15,
        "thresholds": ("declining","stable", "growing","accelerating"),
        "now":        "growing",
        "score":      3,
        "comment":    "A genuinely meaningful, high-margin byproduct stream that diversifies the pure-copper price exposure somewhat",
    },
    {
        "name":       "Commodity cycle stage (qualitative)",
        "weight":     0.20,
        "thresholds": ("late-cycle peak","mid-cycle","early-cycle","structural supercycle"),
        "now":        "mid-cycle",
        "score":      2,
        "comment":    "Genuinely hard to call — AI/EV demand narratives are real, but so is KGHM's own history of sharp cyclical reversals",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.15,
        "thresholds": (">12x",   "≤9x",    "≤7x",    "≤5x"),
        "now":        "~6.3x",
        "score":      3,
        "comment":    "6.3× forward earnings — deeply cheap in absolute terms, reflecting the market's structural skepticism about earnings durability",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Q1 2026's ~10.7x YoY net profit growth is a real, audited result on production that was in-line with budget — this is a price story, not an execution story", +0.4, 0.20),
    ("-", "KGHM's own 52-week range (a 3.2x high-to-low swing) is the clearest possible evidence that today's exceptional earnings are not a stable new baseline", -0.5, 0.25),
    ("+", "At ~6.3x forward earnings, the market is already pricing deep skepticism about earnings durability — there isn't much froth left to unwind", +0.4, 0.20),
    ("+", "Silver and precious-metals byproduct income provides some genuine diversification away from pure copper-price exposure", +0.2, 0.10),
    ("-", "KGHM carries real, company-specific tail risks beyond commodity prices: Polish extraction tax policy, historically challenged Sierra Gorda/international assets, and labor relations", -0.3, 0.15),
    ("-", "As a partially state-influenced Polish champion, capital allocation and dividend policy can be subject to political as well as commercial considerations", -0.2, 0.10),
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
CONS_EPS_2YR  = 45.00   # PLN; conservative FY2028E: assumes meaningful normalization from today's exceptional metal prices
CONS_PE_2YR   = 6.5     # roughly flat to the current ~6.3× multiple
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
print(f"  {TICKER}  ·  {COMPANY}  ·  {CURRENT_PRICE:.2f} zł  ·  Copper & Silver Mining")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]  (all figures in PLN)")
print("═" * (W + 4))

# ─── ① PROFIT CONTRIBUTION BRIDGE ─────────────────────────────────────────────
print()
print("  PROFIT CONTRIBUTION BRIDGE  (FY2026E, PLN millions net profit  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(p for _, p, _, _, _ in SEG_DATA)
bear_total = sum(p for _, _, p, _, _ in SEG_DATA)
bull_total = sum(p for _, _, _, p, _ in SEG_DATA)

print(f"  {'Segment':<44}  {'FY26E (M zł)':>13}  {'Bear (M zł)':>11}  {'Bull (M zł)':>11}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<44}  {curr:>11.0f}  {bear:>9.0f}  {bull:>9.0f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL NET PROFIT':<44}  {curr_total:>11.0f}  {bear_total:>9.0f}  {bull_total:>9.0f}")
print(f"  Q1 2026 actual: {Q1_2026_NET_PROFIT_B}B zł net profit (~10.7x YoY), {Q1_2026_EBITDA_B}B zł EBITDA (>2x YoY)")
print()

# EPS bridge (direct profit / shares — no margin step needed, segments already at net profit)
shares    = SHARES_OUT_M
curr_eps  = round(curr_total / shares, 2)
bull_eps_imp = round(bull_total / shares, 2)
bear_eps_imp = round(bear_total / shares, 2)

print(f"  FY2026E EPS check:  {curr_total:.0f}M zł net profit ÷ {shares:.2f}M shares")
print(f"  =  {curr_eps:.2f} zł/share  (model estimate {EPS_FY2026E:.2f} zł  ✓)")
print()
print(f"  BULL EPS check:  {bull_total:.0f}M zł net profit ÷ {shares:.2f}M shares")
print(f"  =  {bull_eps_imp:.2f} zł/share  →  × {SCENARIOS['BULL'][1]}× = ~{bull_eps_imp*SCENARIOS['BULL'][1]:.0f} zł  ✓ BULL {SCENARIOS['BULL'][2]} zł")
print()
print(f"  BEAR EPS check:  {bear_total:.0f}M zł net profit ÷ {shares:.2f}M shares (metal prices revert)")
print(f"  =  {bear_eps_imp:.2f} zł/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~{bear_eps_imp*SCENARIOS['BEAR'][1]:.0f} zł  ✓ BEAR {SCENARIOS['BEAR'][2]} zł")

# COMMODITY PRICE CYCLE CHECK
print()
print(f"  COMMODITY PRICE CYCLE CHECK  (the KGHM-specific angle):")
print(f"  Q1 2026 net profit:                     {Q1_2026_NET_PROFIT_B}B zł  (~10.7x YoY)")
print(f"  Q1 2026 EBITDA:                          {Q1_2026_EBITDA_B}B zł  (>2x YoY)")
print(f"  Copper production (Q1):                  {Q1_2026_COPPER_PRODUCTION_KT}kt  (in line with budget)")
print(f"  Silver production (Q1):                  {Q1_2026_SILVER_PRODUCTION_T}t  (~37koz)")
print(f"  52-week high/low ratio:                  {FY26_WFE_52W_RANGE_MULTIPLE:.1f}x  (the scale of KGHM's own commodity-cycle swings)")
print()
print(f"  KGHM's exceptional current profitability is entirely a metals-price story, not an operational one —")
print(f"  production came in exactly on budget. That's both reassuring (the company isn't overextending to")
print(f"  chase prices) and the whole risk (there's no operational lever to pull if copper and silver prices")
print(f"  revert). This is the flip side of the AI/EV-driven demand narrative that's also showing up in this")
print(f"  session's other commodity-adjacent names — the market simply hasn't decided if it's structural or cyclical.")

# KEY SENSITIVITIES
print()
eps_per_100M_profit = 100.0 / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every 100M zł net profit:                +{eps_per_100M_profit:.3f} zł/EPS  = +{eps_per_100M_profit*6.3:.2f} zł/share at 6.3× P/E")
print(f"  Every 1 turn of P/E:                      ±{EPS_FY2026E:.2f} zł/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")
print(f"  Dividend cushion:                          {ANNUAL_DIV:.2f} zł/yr absorbs ~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}% of any annual price drawdown")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (profit growth / EBITDA / production / silver / cycle stage / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<36}  {'BEAR':>16}  {'BASE':>9}  {'BULL':>11}  {'XBULL':>22}  {'NOW':>10}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<36}  {ths[0]:>16}  {ths[1]:>9}  {ths[2]:>11}  {ths[3]:>22}  {s['now']:>10}  {lbl}  {b}")
    print(f"    {s['comment']}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from {CURRENT_PRICE} zł + 15%/yr hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:88]:<88}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR {bear_price} zł)")
hr()
print(f"  {'Signal':<32}  {'Current':>14}  {'Bear val':>14}  Trigger")
hr()
bear_triggers = [
    ("Net profit growth",           "~+970%", "<0%",           "Copper/silver prices revert sharply as the current demand narrative disappoints or supply responds"),
    ("EBITDA growth",               "+100%+", "<0%",           "Margins compress as elevated prices prove temporary while cost inflation persists"),
    ("Copper production",           "on budget","well below",  "Operational disruption (labor, ore grade decline, regulatory) hits production independent of price"),
    ("Silver contribution",         "growing","declining",     "Byproduct grades decline or silver prices revert alongside copper"),
    ("Commodity cycle stage",       "mid-cycle","late-cycle peak","The current rally proves to have been the cyclical top, not a new structural regime"),
    ("Forward P/E",                 "~6.3x",  ">12x",          "Ironically, P/E can rise even as price falls if EPS collapses faster than price does"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>14}  {bear_v:>14}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: KGHM has no operational lever against a metals-price reversal — production is already")
print(f"  running on budget, so the entire bear case is a pure price call, and KGHM's own 3.2x 52-week trading")
print(f"  range is the best evidence that such reversals happen fast and are not merely theoretical for this stock.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS estimate:       {EPS_FY2026E:.2f} zł  (forward-P/E-implied from consensus)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (a genuine commodity-miner-trough multiple)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    {EPP:.0f} zł/share")
print(f"  Current {CURRENT_PRICE:.2f} zł vs EPP {EPP:.0f} zł:  {epp_gap_pct:+.1f}%")
print()
print(f"  At {CURRENT_PRICE:.2f} zł the stock trades at just {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS — the EPP floor and the current")
print(f"  price sit remarkably close together, which is unusual and tells its own story: the market is pricing")
print(f"  KGHM as if today's exceptional earnings power is already close to a trough-multiple valuation, i.e.")
print(f"  giving essentially no credit for the earnings being durable.")
print(f"  At a 9× reversion (a still-modest cyclical multiple): {EPS_FY2026E:.2f} × 9 = {EPS_FY2026E*9:.0f} zł  ({(EPS_FY2026E*9/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: assumes meaningful normalization from today's exceptional prices)")
hr()
print(f"  Conservative FY2028E EPS:  {CONS_EPS_2YR:.2f} zł  (below FY2026E — assumes real, not full, mean reversion)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (roughly flat to the current ~6.3× multiple)")
print(f"  Conservative equity value:   {cons_equity:.2f} zł/share")
print(f"  + Cumulative dividends (2yr): +{cons_divs:.2f} zł/share  ({ANNUAL_DIV:.2f} zł/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      {cons_total:.2f} zł  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from {CURRENT_PRICE:.2f} zł)")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: even assuming real mean-reversion in metal prices (EPS falls from {EPS_FY2026E:.2f} to {CONS_EPS_2YR:.2f}),")
print(f"  the conservative case is roughly {'flat-to-negative' if cons_return < 5 else 'positive'} — because the starting multiple is already so low. The trough")
print(f"  multiple assumption is doing most of the protective work here, not an assumption that prices hold.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.42
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        {VOL_52W_LOW:.2f} – {VOL_52W_HIGH:.2f} zł  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      {ANNUAL_DIV:.2f} zł/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; variable, tied to profits)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (very high — a leveraged play on two volatile commodity prices simultaneously)")
print(f"  Beta vs WIG20:        1.45  (well above the Warsaw benchmark — a high-beta commodity cyclical)")
print(f"  1-sigma range (1yr):  {sigma_range[0]:.0f} – {sigma_range[1]:.0f} zł  ({CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear {bear_price} zł requires:  ~{bear_sigmas:.1f}σ drawdown  (large, but well within KGHM's own historical cycle-swing range)")
print(f"  → Q2 2026 print (expected in the coming weeks) is the next confirmation point for whether the Q1 pace held.")
print(f"  → LME copper and silver spot prices are the single leading indicator to watch between prints.")
print(f"  → {signal_short} at {CURRENT_PRICE:.2f} zł  |  Add below 220 zł  |  Trim above 400 zł")

# ─── ⑦ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print()
print("  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
hr()
probs_mkt = softmax_probs(MARKET_COMPOSITE)
print(f"  {'Scenario':<10}  {'Price':>9}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>7}  Description")
hr()
for s in ["BEAR","BASE","BULL","XBULL"]:
    pp  = probs_proxy[s] * 100
    pm  = probs_mkt[s]   * 100
    gap = pp - pm
    pr  = SCENARIOS[s][2]
    desc = SCENARIOS[s][3][:44]
    print(f"  {s:<10}  {pr:>6} zł  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): {ev_adj:.0f} zł  /  Proxy EV: {ev_prx:.0f} zł  /  Market EV: {ev_mkt:.0f} zł  /  Current: {CURRENT_PRICE:.0f} zł")
hr()
print(f"  Downside  (→ Bear {bear_price} zł):  {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull {bull_price} zł):  {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b_str}")
print(f"  Signal    :  {signal_full}")
print()
print(f"  MARKET PRICING: at {CURRENT_PRICE:.2f} zł the market composite is {MARKET_COMPOSITE:.2f}/4.0. The model's")
print(f"  adjusted composite is {ADJ_COMPOSITE:.2f}/4.0, for a gap of {ADJ_GAP:+.2f} — {valuation_label.lower()}.")
print(f"  KGHM is a genuine commodity cyclical trading at a genuine commodity-cyclical multiple — the")
print(f"  mechanically attractive risk/reward reflects the market's appropriate skepticism, not mispricing.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q2 2026 print (expected in the coming weeks) — does the Q1 profit pace hold?")
print(f"  (2) LME copper and silver spot prices — the single leading indicator for the entire thesis")
print(f"  (3) AI-datacenter and EV-driven copper demand data points — the structural-vs-cyclical debate")
print(f"  (4) Any Polish extraction-tax or regulatory policy changes affecting KGHM specifically")
print(f"  (5) Sierra Gorda and other international asset performance — the diversification-vs-distraction debate")
print(f"  {signal_short} at {CURRENT_PRICE:.2f} zł  |  Add below 220 zł  |  Trim above 400 zł")
print(f"  EPP floor: {EPP:.0f} zł  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: {EPS_FY2026E:.2f} zł  |  Q1 net profit growth: ~+970% YoY")
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
