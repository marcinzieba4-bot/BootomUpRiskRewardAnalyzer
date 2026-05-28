"""
Dino Polska S.A. (WSE: DNP)
Polish Grocery Retail · Standalone Discount Format · Founder-Led · PLN
Bottom-Up Risk/Reward Signal Model
"""

import math

# ── DINO POLSKA STORE ECONOMICS CALCULATOR ─────────────────────────────────────
STORES_OPEN         = 2750    # stores open at period end (trailing 12m)
NEW_STORES_YR       = 360     # net new stores in trailing 12 months
REV_PER_STORE_M_PLN = 10.2    # avg revenue per store (M PLN/yr)  — ~10M is ~400m² store
EBIT_MARGIN         = 0.054   # group EBIT margin (~5.4%)
NET_INTEREST_B_PLN  = 0.13    # net interest expense (B PLN)
TAX_RATE            = 0.19    # Polish CIT 19%
SHARES_M            = 98.5    # shares outstanding (millions; minimal dilution — founder 52%)

LFL_GROWTH_PCT      = 7.0     # like-for-like revenue growth YoY (%)
WHITESPACE_PCT      = 60.0    # % addressable small municipalities not yet entered by Dino
COMP_NEW_STORES_YR  = 220     # Biedronka/Aldi net new stores overlapping Dino catchments

# Derived P&L
total_rev_b     = STORES_OPEN * REV_PER_STORE_M_PLN / 1000         # ~28.1B PLN
ebit_b          = total_rev_b * EBIT_MARGIN                         # ~1.52B PLN
ebt_b           = ebit_b - NET_INTEREST_B_PLN                       # ~1.39B PLN
net_income_b    = ebt_b * (1 - TAX_RATE)                           # ~1.12B PLN
eps_pln         = net_income_b * 1000 / SHARES_M                    # ~11.4 PLN
rev_growth_pct  = (NEW_STORES_YR / (STORES_OPEN - NEW_STORES_YR) * 100
                   + LFL_GROWTH_PCT * (STORES_OPEN - NEW_STORES_YR / 2) / STORES_OPEN)

# Note: all prices in PLN (Polish Zloty). EUR/PLN ≈ 4.25; USD/PLN ≈ 3.90 (May 2026)
print("=" * 72)
print("DINO POLSKA S.A. — STORE ECONOMICS CALCULATOR (PLN)")
print("=" * 72)
print(f"  Stores open (period end)     : {STORES_OPEN:,}")
print(f"  Net new stores (trailing 12m): {NEW_STORES_YR}  ({NEW_STORES_YR/(STORES_OPEN-NEW_STORES_YR)*100:.1f}% store count growth)")
print(f"  Revenue per store            : PLN {REV_PER_STORE_M_PLN:.1f}M/yr")
print(f"  Total group revenue          : PLN {total_rev_b:.2f}B  ({LFL_GROWTH_PCT:.0f}% LFL growth on existing stores)")
print(f"  EBIT ({EBIT_MARGIN*100:.1f}% margin)            : PLN {ebit_b:.3f}B")
print(f"  Net interest expense         : PLN {NET_INTEREST_B_PLN:.2f}B  (owned-store capex debt)")
print(f"  EBT                          : PLN {ebt_b:.3f}B")
print(f"  Net income ({TAX_RATE*100:.0f}% CIT)         : PLN {net_income_b:.3f}B")
print(f"  EPS                          : PLN {eps_pln:.2f}  ({SHARES_M}M shares)")
print()
print(f"  Store economics:")
print(f"    Breakeven payback (owned):  ~{int(REV_PER_STORE_M_PLN * EBIT_MARGIN * 1 / 0.018 * 1):.0f} yrs at {EBIT_MARGIN*100:.1f}% margin, PLN 1.8M capex/store")
print(f"    Geographic whitespace       : {WHITESPACE_PCT:.0f}% addressable municipalities not yet entered")
print(f"    Competitive overlap stores  : {COMP_NEW_STORES_YR} Biedronka/Aldi openings in Dino catchments/yr")
print()

# ── SIGNAL PARAMETERS ─────────────────────────────────────────────────────────
CURRENT_PRICE  = 275.0   # PLN, WSE: DNP ~May 2026

EPP_TODAY_EPS  = round(eps_pln, 1)   # ~11.4 PLN
EPP_MIN_PE     = 12                   # min-viable trough P/E for grocery with positive margins
EPP            = EPP_TODAY_EPS * EPP_MIN_PE
epp_gap_pct    = (CURRENT_PRICE - EPP) / EPP * 100

SCENARIOS = {
    #         EPS(PLN), P/E, price(PLN),  narrative
    "BEAR":  ( 7.0,     12,    84,  "Polish recession + wage cost spiral; Biedronka price war; margins collapse to breakeven"),
    "BASE":  (12.0,     21,   252,  "Steady 13-15% store count growth; LFL 4-6%; margins stable; re-rating to 21x"),
    "BULL":  (15.0,     30,   450,  "Margin recovery + growth acceleration; market re-rates to premium compounder 30x"),
    "XBULL": (20.0,     32,   640,  "Dino captures 25%+ Polish grocery market; dominant position; 32x justified"),
}

# Conservative case
CONS_EPS_CAGR  = 0.12    # 12%/yr EPS growth (moderated from historical 20%+)
CONS_EXIT_PE   = 20.0    # conservative exit multiple (20x — decent quality but not peak)
CONS_DIVIDEND  = 0.0     # no dividend — reinvests all FCF into store openings

# Volatility
VOL_ANNUAL_PCT = 0.30
VOL_BETA       = 0.75
VOL_52W_LOW    = 215.0
VOL_52W_HIGH   = 315.0

# ── HELPER FUNCTIONS ───────────────────────────────────────────────────────────
def softmax_probs(composite: float, T: float = 0.60) -> dict:
    centers = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    raw = {k: math.exp(-((composite - v) ** 2) / (2 * T ** 2)) for k, v in centers.items()}
    total = sum(raw.values())
    return {k: v / total for k, v in raw.items()}

def score_signal(val, base_floor, bull_floor, xbull_floor, higher_is_better=True):
    if higher_is_better:
        if val >= xbull_floor: return 4
        if val >= bull_floor:  return 3
        if val >= base_floor:  return 2
        return 1
    else:
        if val <= xbull_floor: return 4
        if val <= bull_floor:  return 3
        if val <= base_floor:  return 2
        return 1

def market_implied_composite(target_ev: float, tolerance: float = 1.5) -> float:
    for c100 in range(100, 401):
        c = c100 / 100
        probs = softmax_probs(c)
        ev = sum(probs[k] * SCENARIOS[k][2] for k in SCENARIOS)
        if abs(ev - target_ev) < tolerance:
            return c
    return 3.00

# ── SIGNALS ───────────────────────────────────────────────────────────────────
SIGNALS = [
    # (name, unit, bear_val, base_floor, bull_floor, xbull_floor, current_val, higher_is_better, bear_narrative)
    ("Net new store openings — trailing 12m", "#",
     150,  220,  320,  420,
     NEW_STORES_YR, True,
     "Expansion stalls; capex overhang; ROI on new stores deteriorates below hurdle"),

    ("Like-for-like revenue growth — YoY", "%",
     0,    3,    6,   10,
     LFL_GROWTH_PCT, True,
     "LFL goes negative; consumer trading-down; basket shrinks; loyalty breaks"),

    ("EBIT margin — YoY change", "bps",
     -80,  -30,   0,  30,
     -20,  True,
     "Wage spiral (Polish min wage hikes) + energy costs overwhelm pricing; margin collapses"),

    ("Geographic whitespace — % addressable municipalities not entered", "%",
     15,   25,   40,  55,
     WHITESPACE_PCT, True,
     "Market saturated; new store ROI deteriorates; cannibalization accelerates"),

    ("Polish real wage growth — YoY", "%",
     -2,    1,    4,   7,
      6,   True,
     "Real wage contraction; Polish consumer confidence crashes; FMCG volumes fall"),

    ("Competitive response — rival net new stores in Dino catchments / yr", "#",
     400,  300,  200,  100,
     COMP_NEW_STORES_YR, False,
     "Biedronka/Aldi flood Dino's rural territory; price war forces margin sacrifice"),
]

SIGNAL_WEIGHTS = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]

# ── STRUCTURAL COMPOSITE ADJUSTMENT ───────────────────────────────────────────
STRUCTURAL_FACTORS = [
    ("Tomasz Biernacki founder-led; 52% control + consistent capital allocation",  0.6, 0.25),
    ("Owned-store model (not leased) → rent-inflation immune; asset-backed NAV",   0.7, 0.25),
    ("Fresh meat/deli in-store (~30% revenue): hard to replicate moat vs discounters", 0.5, 0.20),
    ("CIT / Polish tax policy uncertainty; estonian model rollout risk",           -0.3, 0.15),
    ("Single-country PLN concentration; FX haircut for EUR/USD investors",        -0.4, 0.15),
]

# ── PART 1 — SIGNAL DASHBOARD ─────────────────────────────────────────────────
print("PART 1 — SIGNAL DASHBOARD")
print("=" * 72)

scores, weighted_scores = [], []
for i, (name, unit, bv, bf, blf, xf, cv, hib, bear_note) in enumerate(SIGNALS):
    sc = score_signal(cv, bf, blf, xf, hib)
    label = {1: "BEAR", 2: "BASE", 3: "BULL", 4: "XBULL"}[sc]
    w = SIGNAL_WEIGHTS[i]
    scores.append(sc)
    weighted_scores.append(sc * w)
    direction = "▲ higher=better" if hib else "▼ lower=better"
    print(f"  [{i+1}] {name}")
    print(f"       Current: {cv:+.0f} {unit}   ({direction})   → {label} ({sc})")
    print(f"       Bear: {bv} | Base≥{bf} | Bull≥{blf} | XBull≥{xf}   weight={w:.0%}")
    print(f"       Bear trigger: {bear_note}")
    print()

proxy_composite = sum(weighted_scores) / sum(SIGNAL_WEIGHTS)
print(f"  Proxy composite (weighted avg): {proxy_composite:.2f}")
print()

# Structural Composite Adjustment
sca = sum(score * weight for _, score, weight in STRUCTURAL_FACTORS)
adj_composite = proxy_composite + sca
print("  Structural Composite Adjustment (SCA):")
for label, score, weight in STRUCTURAL_FACTORS:
    print(f"    {score:+.1f} × {weight:.2f}  {label}")
print(f"  SCA = {sca:+.2f}   Adjusted composite: {adj_composite:.2f}")
print()

# ── PART 2 ANALYST COMMENTARY ─────────────────────────────────────────────────
print()
print("PART 2 ANALYST COMMENTARY")
print("=" * 72)
print()

HURDLE_RATE = 0.15
target_ev   = CURRENT_PRICE * (1 + HURDLE_RATE) ** 2
mic         = market_implied_composite(target_ev)
adj_gap     = adj_composite - mic
verdict     = ("UNDERVALUED" if adj_gap >  0.30
               else "MODESTLY OVERVALUED" if adj_gap < -0.10
               else "FAIRLY VALUED")

probs    = softmax_probs(adj_composite)
ev_model = sum(probs[k] * SCENARIOS[k][2] for k in SCENARIOS)
upside_pct = (ev_model - CURRENT_PRICE) / CURRENT_PRICE * 100

bear_p   = SCENARIOS["BEAR"]

print(f"""DINO POLSKA S.A. — ANALYST COMMENTARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Note: all prices in PLN (Polish Zloty). EUR/PLN ≈ 4.25; USD/PLN ≈ 3.90.
Current price PLN {CURRENT_PRICE:.0f} ≈ EUR {CURRENT_PRICE/4.25:.0f} / USD {CURRENT_PRICE/3.90:.0f}.

① SIGNAL DASHBOARD SUMMARY
────────────────────────────
Proxy composite : {proxy_composite:.2f}  →  SCA {sca:+.2f}  →  Adjusted: {adj_composite:.2f}
Market-implied  : {mic:.2f}  (15% hurdle target = PLN {target_ev:.0f})
Signal gap      : {adj_gap:+.2f}  →  {verdict}

Scenario probabilities (adj. composite {adj_composite:.2f}):
  BEAR  {probs['BEAR']*100:5.1f}%  →  PLN {SCENARIOS['BEAR'][2]}
  BASE  {probs['BASE']*100:5.1f}%  →  PLN {SCENARIOS['BASE'][2]}
  BULL  {probs['BULL']*100:5.1f}%  →  PLN {SCENARIOS['BULL'][2]}
  XBULL {probs['XBULL']*100:5.1f}% →  PLN {SCENARIOS['XBULL'][2]}
  Expected value : PLN {ev_model:.0f}  ({upside_pct:+.1f}% vs PLN {CURRENT_PRICE:.0f})

VERDICT: ACCUMULATE — adjusted composite {adj_composite:.2f} exceeds market-implied {mic:.2f}
({adj_gap:+.2f} gap). The market prices Dino as a maturing retailer; our signals
show an active growth compounder — {NEW_STORES_YR} net new stores/yr ({NEW_STORES_YR/(STORES_OPEN-NEW_STORES_YR)*100:.1f}% store CAGR),
{LFL_GROWTH_PCT:.0f}% LFL, and {WHITESPACE_PCT:.0f}% untapped geographic whitespace. Owned-store
model and fresh meat differentiation are structural moats that discount
retailers (Biedronka) struggle to replicate. Accumulate on weakness.

② BEAR CASE ANATOMY
─────────────────────
Trigger: Polish macro shock — GDP contraction + real wage reversal, coinciding
with Biedronka (Jeronimo Martins) aggressive price-war in rural Poland. Dino's
5.4% EBIT margin has limited buffer; a -200bps compression to 3.4% margin on
PLN {total_rev_b:.1f}B revenue halves net income to ~PLN {total_rev_b*0.034*(1-TAX_RATE):.2f}B, EPS ~{total_rev_b*0.034*(1-TAX_RATE)*1000/SHARES_M:.1f} PLN.

Owned-store leverage cuts both ways in bear case:
  High capex commitments (~PLN 1.8M/store) → free cashflow dries up
  Debt service on store portfolio increases refinancing pressure
  P/E de-rating from 21x to 12x (distressed grocery multiple) → PLN {bear_p[2]}
  Founder sells nothing → stock illiquid on way down (52% locked up)

③ UPDATED EPP (EARNINGS POWER PRICE)
──────────────────────────────────────
  Current trailing EPS  : PLN {EPP_TODAY_EPS:.1f}  (store calculator: PLN {eps_pln:.2f})
  Min-viable trough P/E : {EPP_MIN_PE}×  (grocery chain at breakeven — not zero)
  EPP floor             : PLN {EPP:.0f}
  Current vs EPP        : {epp_gap_pct:+.1f}%  (comfortable but not spectacular for a growth stock)

The EPP floor at PLN {EPP:.0f} implies a scenario where earnings collapse to current
levels and the market prices them at distressed-grocery multiples. The +{epp_gap_pct:.0f}%
cushion to EPP reflects Dino's growth premium — a "normal" grocery stock
trades at 12-15× earnings, but Dino's growth justifies the premium as long
as the store-rollout thesis is intact.

④ CONSERVATIVE GROWTH CASE
───────────────────────────
Assumptions: EPS grows at {CONS_EPS_CAGR*100:.0f}%/yr (vs historical 20%+); exit {CONS_EXIT_PE:.0f}×; no dividend
""")

cons_eps_yr2 = EPP_TODAY_EPS * (1 + CONS_EPS_CAGR) ** 2
cons_price_2yr = cons_eps_yr2 * CONS_EXIT_PE
cons_total = cons_price_2yr  # no dividends
cons_ret_pct = (cons_total - CURRENT_PRICE) / CURRENT_PRICE * 100

print(f"""  EPS year 2 (FY+2, {CONS_EPS_CAGR*100:.0f}%/yr CAGR): PLN {cons_eps_yr2:.2f}
  Exit price (2yr)             : PLN {cons_price_2yr:.0f}  ({CONS_EXIT_PE:.0f}× × {cons_eps_yr2:.2f})
  Dividend income (2yr)        : PLN 0  (full reinvestment model; no payout)
  Conservative total return    : {cons_ret_pct:+.1f}%  over 2 years  (~{cons_ret_pct/2:.1f}%/yr)

Conservative case delivers {cons_ret_pct:.1f}% over 2 years even at half the historical
growth rate and a compressed 20× exit multiple — decent for a zero-dividend
compounder. Upside leverage to higher growth rates is significant: at 18%
EPS CAGR and 26× exit, 2yr return = {(EPP_TODAY_EPS*(1.18)**2*26-CURRENT_PRICE)/CURRENT_PRICE*100:.0f}%.

⑤ VOLATILITY CONTEXT
──────────────────────
  52-week range   : PLN {VOL_52W_LOW:.0f} – {VOL_52W_HIGH:.0f}
  Current         : PLN {CURRENT_PRICE:.0f}   ({(CURRENT_PRICE-VOL_52W_LOW)/(VOL_52W_HIGH-VOL_52W_LOW)*100:.0f}th percentile of range)
  Annual vol      : {VOL_ANNUAL_PCT*100:.0f}%   Beta: {VOL_BETA:.2f}x  (lower than broad WIG20 due to domestic-demand nature)
  1σ range (1yr)  : PLN {CURRENT_PRICE*(1-VOL_ANNUAL_PCT):.0f} – PLN {CURRENT_PRICE*(1+VOL_ANNUAL_PCT):.0f}

Note: Dino's float is thin (~48% free float; Biernacki owns ~52%). This creates
both a liquidity discount and a squeeze premium in bull runs. The stock
often trades at wider bid-ask spreads vs Polish blue chips.

⑥ SCENARIO PROBABILITIES
──────────────────────────
Softmax distribution centred on adj. composite {adj_composite:.2f}:
""")

print(f"  BEAR   {probs['BEAR']*100:5.1f}%  EPS PLN {SCENARIOS['BEAR'][0]:.1f}  ×{SCENARIOS['BEAR'][1]}P/E  =  PLN {SCENARIOS['BEAR'][2]}")
print(f"         {SCENARIOS['BEAR'][3]}")
print(f"  BASE   {probs['BASE']*100:5.1f}%  EPS PLN {SCENARIOS['BASE'][0]:.1f}  ×{SCENARIOS['BASE'][1]}P/E  =  PLN {SCENARIOS['BASE'][2]}")
print(f"         {SCENARIOS['BASE'][3]}")
print(f"  BULL   {probs['BULL']*100:5.1f}%  EPS PLN {SCENARIOS['BULL'][0]:.1f}  ×{SCENARIOS['BULL'][1]}P/E  =  PLN {SCENARIOS['BULL'][2]}")
print(f"         {SCENARIOS['BULL'][3]}")
print(f"  XBULL  {probs['XBULL']*100:5.1f}%  EPS PLN {SCENARIOS['XBULL'][0]:.1f}  ×{SCENARIOS['XBULL'][1]}P/E  =  PLN {SCENARIOS['XBULL'][2]}")
print(f"         {SCENARIOS['XBULL'][3]}")
print()
print(f"  Expected value : PLN {ev_model:.0f}  ({upside_pct:+.1f}% upside from PLN {CURRENT_PRICE:.0f})")
print()

# ── PART 3 NUMBERS & SIGNALS ──────────────────────────────────────────────────
print()
print("PART 3 NUMBERS & SIGNALS")
print("=" * 72)

bear_price  = SCENARIOS["BEAR"][2]
bull_price  = SCENARIOS["BULL"][2]
downside    = (CURRENT_PRICE - bear_price) / CURRENT_PRICE
upside      = (bull_price - CURRENT_PRICE) / CURRENT_PRICE
ratio_b     = downside / upside if upside > 0 else 99
ratio_b_fmt = f"{ratio_b:.2f}x"

if ratio_b < 0.75:
    signal_short = "BUY"
    signal       = "◉ BUY"
elif ratio_b < 1.10:
    signal_short = "ACCUMULATE"
    signal       = "◎ ACCUMULATE"
elif ratio_b < 1.75:
    signal_short = "WATCHLIST"
    signal       = "◐ WATCHLIST"
else:
    signal_short = "AVOID"
    signal       = "✕ AVOID"

print(f"""
  Ticker          : DNP  (Warsaw Stock Exchange / GPW)
  Company         : Dino Polska S.A.
  Sector          : Polish Grocery Retail · Standalone Discount Format
  Currency        : PLN (Polish Zloty)   EUR/PLN ≈ 4.25
  Current price   : PLN {CURRENT_PRICE:.0f}  (≈ EUR {CURRENT_PRICE/4.25:.0f})
  Stores open     : {STORES_OPEN:,}  (+{NEW_STORES_YR} net new trailing 12m)
  EPS (calc)      : PLN {eps_pln:.2f}  →  EPP floor PLN {EPP:.0f}  ({EPP_TODAY_EPS}× {EPP_MIN_PE})
  EPP gap         : {epp_gap_pct:.1f}%  (current vs EPP floor)
  Downside (Bear) : {downside*100:.1f}%  → PLN {bear_price}
  Upside (Bull)   : {upside*100:.1f}%   → PLN {bull_price}
  Ratio B         : {ratio_b_fmt}  (downside ÷ upside)
  Expected value  : PLN {ev_model:.0f}  ({upside_pct:+.1f}%)
  Conservative 2yr: {cons_ret_pct:+.1f}%  (PLN {cons_price_2yr:.0f}; no dividend)
  Signal          : {signal}
  Proxy composite : {proxy_composite:.2f}
  Adj. composite  : {adj_composite:.2f}  (SCA: {sca:+.2f})
  Market-implied  : {mic:.2f}  → {verdict}
""")

print("━" * 72)
print(f"  SIGNAL: {signal}   Ratio B: {ratio_b_fmt}")
print(f"  Adj. composite {adj_composite:.2f} vs market-implied {mic:.2f} ({adj_gap:+.2f})")
print("━" * 72)
print()
print("  KEY MOATS:")
print(f"  • Owned stores ({STORES_OPEN:,}): asset base insulates from rent inflation; resale backstop")
print(f"  • Fresh meat/deli in-store: ~30% revenue; impossible to match in a pure discount format")
print(f"  • {WHITESPACE_PCT:.0f}% geographic whitespace: multi-year organic growth runway without M&A risk")
print(f"  • Founder Biernacki (52%): aligned; zero dividend extractions; reinvests at ~20%+ ROIC")
print()
print("  KEY RISKS:")
print(f"  • Polish minimum wage hikes outpace pricing power → margin erosion")
print(f"  • Biedronka (JMT) aggressive rural expansion → LFL deceleration")
print(f"  • Store cannibalization as density increases in core Central Poland")
print(f"  • CIT/tax policy risk (Poland; estonian model changes possible)")
print(f"  • Thin free float (~48%): illiquid in stress; bid-ask widening amplifies drawdowns")
print()
print("  Not financial advice. All prices in PLN. EPP = calc EPS × min-viable trough P/E.")
print("  Store calculator assumes trailing 12m actuals; LFL and whitespace are estimates.")
