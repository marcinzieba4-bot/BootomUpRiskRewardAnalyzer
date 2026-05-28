"""
Dino Polska S.A. (WSE: DNP)
Polish Grocery Retail · Standalone Discount Format · Founder-Led
Bottom-Up Risk/Reward Signal Model  |  All prices in PLN
"""

import math

# ─────────────────────────────────────────────────────────────────────────────
# DINO POLSKA STORE ECONOMICS CALCULATOR
# ─────────────────────────────────────────────────────────────────────────────
STORES            = 2750     # stores open at period-end
NEW_STORES_TTM    = 360      # net new stores trailing 12 months
REV_PER_STORE_M   = 10.2     # avg revenue per store (PLN million / year)
EBIT_MARGIN       = 0.054    # 5.4% EBIT margin
NET_INTEREST_B    = 0.13     # net interest expense (PLN billion) — owned-store debt
TAX_RATE          = 0.19     # Polish CIT 19%
SHARES_M          = 985.0    # shares outstanding (millions; 10:1 split Jul 2025; float ~48%)

LFL_PCT           = 7.0      # like-for-like revenue growth YoY (%)
WHITESPACE_PCT    = 60.0     # % addressable small municipalities not yet entered
COMP_OPENINGS     = 220      # Biedronka/Aldi net new stores in Dino catchment areas / yr

# ── Derived P&L ──────────────────────────────────────────────────────────────
rev_b    = STORES * REV_PER_STORE_M / 1000          # total revenue (PLN B)
ebit_b   = rev_b  * EBIT_MARGIN
ebt_b    = ebit_b - NET_INTEREST_B
ni_b     = ebt_b  * (1 - TAX_RATE)
eps      = ni_b   * 1000 / SHARES_M                 # PLN per share

print("=" * 72)
print("DINO POLSKA S.A.  —  STORE ECONOMICS CALCULATOR  (PLN)")
print("=" * 72)
print(f"  Stores (period-end)      : {STORES:,}")
print(f"  Net new stores (TTM)     : +{NEW_STORES_TTM}  ({NEW_STORES_TTM/(STORES-NEW_STORES_TTM)*100:.1f}% store CAGR)")
print(f"  Revenue / store          : PLN {REV_PER_STORE_M:.1f}M")
print(f"  Group revenue            : PLN {rev_b:.2f}B  (LFL {LFL_PCT:.0f}% on existing base)")
print(f"  EBIT ({EBIT_MARGIN*100:.1f}% margin)        : PLN {ebit_b:.3f}B")
print(f"  Net interest expense     : PLN {NET_INTEREST_B:.2f}B")
print(f"  EBT                      : PLN {ebt_b:.3f}B")
print(f"  Net income (CIT {TAX_RATE*100:.0f}%)   : PLN {ni_b:.3f}B")
print(f"  EPS                      : PLN {eps:.2f}  ({SHARES_M}M shares)")
print()
print(f"  Geographic whitespace    : {WHITESPACE_PCT:.0f}%  addressable municipalities not yet entered")
print(f"  Competitor openings      : {COMP_OPENINGS}  Biedronka/Aldi in Dino zones / yr")
print()

# ─────────────────────────────────────────────────────────────────────────────
# SIGNAL PARAMETERS
# ─────────────────────────────────────────────────────────────────────────────
CURRENT_PRICE = 32.0    # PLN, WSE: DNP  ~May 2026 post 10:1 split Jul 2025  (EUR/PLN ≈ 4.25)

EPP_EPS    = round(eps, 1)   # PLN 1.1
EPP_MIN_PE = 12               # trough P/E — grocery chain at distressed earnings, not zero
EPP        = EPP_EPS * EPP_MIN_PE
epp_gap    = (CURRENT_PRICE - EPP) / EPP * 100

SCENARIOS = {
    # key: (EPS PLN, P/E, price PLN, narrative)  — post 10:1 split Jul 2025
    "BEAR":  (0.70, 12,   8.4, "Polish recession + wage spiral; Biedronka price war; EBIT margin halved"),
    "BASE":  (1.20, 21,  25.2, "Steady 13–15% store CAGR; LFL 4–6%; margins stable; 21× re-rate"),
    "BULL":  (1.50, 30,  45.0, "Margin recovery + growth acceleration; premium compounder re-rate 30×"),
    "XBULL": (2.00, 32,  64.0, "25%+ Polish grocery market share; dominant moat; 32× justified"),
}

CONS_EPS_CAGR = 0.12    # conservative 12%/yr EPS growth (half the historical rate)
CONS_EXIT_PE  = 20.0    # conservative exit multiple
CONS_DIV      = 0.0     # no dividend — full FCF reinvested in store rollout

VOL_ANNUAL    = 0.30
VOL_BETA      = 0.75
VOL_52W_LOW   = 28.24   # post-split 52W low (Jul 2025–May 2026)
VOL_52W_HIGH  = 55.80   # post-split 52W high

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def softmax_probs(composite, T=0.60):
    centers = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    raw   = {k: math.exp(-((composite - v)**2) / (2*T**2)) for k, v in centers.items()}
    total = sum(raw.values())
    return {k: v/total for k, v in raw.items()}

def score(val, base_floor, bull_floor, xbull_floor, hib=True):
    if hib:
        if val >= xbull_floor: return 4
        if val >= bull_floor:  return 3
        if val >= base_floor:  return 2
        return 1
    else:
        if val <= xbull_floor: return 4
        if val <= bull_floor:  return 3
        if val <= base_floor:  return 2
        return 1

def market_implied_composite(target, tol=1.5):
    for c100 in range(100, 401):
        c = c100 / 100
        ev = sum(softmax_probs(c)[k] * SCENARIOS[k][2] for k in SCENARIOS)
        if abs(ev - target) < tol:
            return c
    return 3.00

# ─────────────────────────────────────────────────────────────────────────────
# SIGNALS
# ─────────────────────────────────────────────────────────────────────────────
SIGNALS = [
    # (name, unit, bear_val, base_floor, bull_floor, xbull_floor, current, hib, bear_trigger)
    ("Net new store openings — trailing 12m", "#",
      150, 220, 320, 420, NEW_STORES_TTM, True,
      "Expansion stalls; capex overhang; new-store ROI below hurdle rate"),

    ("Like-for-like revenue growth — YoY", "%",
       0,   3,   6,  10, LFL_PCT, True,
      "LFL turns negative; consumer trading-down; basket shrinks; loyalty breaks"),

    ("EBIT margin — YoY change", "bps",
     -80, -30,   0,  30, -20, True,
      "Wage spiral (Polish min-wage hikes) + energy overwhelms pricing; margin collapses"),

    ("Geographic whitespace — % municipalities not yet entered", "%",
      15,  25,  40,  55, WHITESPACE_PCT, True,
      "Market saturated; new-store ROI deteriorates; cannibalization accelerates"),

    ("Polish real wage growth — YoY", "%",
      -2,   1,   4,   7,  6, True,
      "Real wage contraction; Polish consumer confidence crashes; FMCG volumes fall"),

    ("Competitive response — rival new stores in Dino catchments / yr", "#",
     400, 300, 200, 100, COMP_OPENINGS, False,
      "Biedronka/Aldi flood Dino's rural territory; price war forces margin sacrifice"),
]

WEIGHTS = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]

SCA_FACTORS = [
    ("Tomasz Biernacki founder-led; 52% control; reinvests at 20%+ ROIC",           +0.6, 0.25),
    ("Owned-store model (not leased): rent-inflation immune; asset-backed NAV",      +0.7, 0.25),
    ("Fresh meat/deli in-store (~30% of revenue): hard to replicate moat",           +0.5, 0.20),
    ("CIT / Polish tax policy uncertainty; Estonian model rollout risk",             -0.3, 0.15),
    ("Single-country PLN concentration; FX haircut for EUR/USD investors",           -0.4, 0.15),
]

# ─────────────────────────────────────────────────────────────────────────────
# PART 1 — SIGNAL DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
print("PART 1 — SIGNAL DASHBOARD")
print("=" * 72)
print()

ws = []
for i, (name, unit, bv, bf, blf, xf, cv, hib, bear_note) in enumerate(SIGNALS):
    sc = score(cv, bf, blf, xf, hib)
    label = {1:"BEAR", 2:"BASE", 3:"BULL", 4:"XBULL"}[sc]
    w  = WEIGHTS[i]
    ws.append(sc * w)
    direction = "▲ higher=better" if hib else "▼ lower=better"
    print(f"  [{i+1}] {name}")
    print(f"       Current: {cv:+.0f} {unit}   ({direction})   → {label} ({sc})   weight={w:.0%}")
    print(f"       Bear:{bv}  Base≥{bf}  Bull≥{blf}  XBull≥{xf}")
    print(f"       Bear trigger: {bear_note}")
    print()

proxy = sum(ws) / sum(WEIGHTS)
sca   = sum(sc * w for _, sc, w in SCA_FACTORS)
adj   = proxy + sca

print(f"  Proxy composite : {proxy:.2f}")
print()
print("  Structural Composite Adjustment:")
for label, sc, w in SCA_FACTORS:
    print(f"    {sc:+.1f} × {w:.2f}  {label}")
print(f"  SCA = {sca:+.2f}   →   Adjusted composite: {adj:.2f}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# PART 2 ANALYST COMMENTARY
# ─────────────────────────────────────────────────────────────────────────────
print()
print("PART 2 ANALYST COMMENTARY")
print("=" * 72)
print()

target_ev  = CURRENT_PRICE * (1.15)**2
mic        = market_implied_composite(target_ev)
gap        = adj - mic
verdict    = ("UNDERVALUED"         if gap >  0.30 else
              "MODESTLY OVERVALUED" if gap < -0.10 else
              "FAIRLY VALUED")

probs  = softmax_probs(adj)
ev     = sum(probs[k] * SCENARIOS[k][2] for k in SCENARIOS)
up_pct = (ev - CURRENT_PRICE) / CURRENT_PRICE * 100

cons_eps_2yr  = EPP_EPS * (1 + CONS_EPS_CAGR)**2
cons_price    = cons_eps_2yr * CONS_EXIT_PE
cons_ret_pct  = (cons_price - CURRENT_PRICE) / CURRENT_PRICE * 100

bear_p_pre  = SCENARIOS["BEAR"][2]
bull_p_pre  = SCENARIOS["BULL"][2]
dn_pre      = (CURRENT_PRICE - bear_p_pre) / CURRENT_PRICE
up_pre      = (bull_p_pre - CURRENT_PRICE) / CURRENT_PRICE
ratio_b_pre = dn_pre / up_pre
signal_short_pre = ("BUY"        if ratio_b_pre < 0.75 else
                    "ACCUMULATE" if ratio_b_pre < 1.10 else
                    "WATCHLIST"  if ratio_b_pre < 1.75 else
                    "AVOID")

print(f"""DINO POLSKA S.A.  —  ANALYST COMMENTARY
Note: all prices in PLN.  EUR/PLN ≈ 4.25  |  PLN {CURRENT_PRICE:.0f} ≈ EUR {CURRENT_PRICE/4.25:.0f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

① SIGNAL DASHBOARD SUMMARY
Proxy: {proxy:.2f}  SCA: {sca:+.2f}  →  Adjusted: {adj:.2f}
Market-implied: {mic:.2f}  (15% hurdle = PLN {target_ev:.0f})
Gap: {gap:+.2f}  →  {verdict}

Probabilities:
  BEAR   {probs['BEAR']*100:5.1f}%  →  PLN {SCENARIOS['BEAR'][2]}
  BASE   {probs['BASE']*100:5.1f}%  →  PLN {SCENARIOS['BASE'][2]}
  BULL   {probs['BULL']*100:5.1f}%  →  PLN {SCENARIOS['BULL'][2]}
  XBULL  {probs['XBULL']*100:5.1f}%  →  PLN {SCENARIOS['XBULL'][2]}
  EV = PLN {ev:.0f}  ({up_pct:+.1f}% vs PLN {CURRENT_PRICE:.0f})

Verdict: {signal_short_pre} — adjusted composite {adj:.2f} vs market-implied {mic:.2f} ({gap:+.2f}).
The market prices Dino as a maturing retailer; signals show an active growth
compounder: {NEW_STORES_TTM} net new stores/yr ({NEW_STORES_TTM/(STORES-NEW_STORES_TTM)*100:.1f}% store CAGR), {LFL_PCT:.0f}% LFL, {WHITESPACE_PCT:.0f}% geographic whitespace.
Owned-store model and fresh meat differentiation are structural moats
Biedronka cannot replicate.

② BEAR CASE ANATOMY
Polish macro shock: GDP contraction + real wage reversal + Biedronka price
war in rural Poland. Dino's 5.4% EBIT margin has limited buffer; a -200bps
compression on PLN {rev_b:.1f}B revenue halves net income. P/E de-rates 21× → 12×.
  Bear EPS: ~PLN {SCENARIOS['BEAR'][0]:.1f}  ×  {SCENARIOS['BEAR'][1]}× P/E  =  PLN {SCENARIOS['BEAR'][2]}
  Owned-store capex commitments (~PLN 1.8M/store) dry up FCF in downturn.
  Founder 52% locked up → stock illiquid on the way down.

③ EPP (EARNINGS POWER PRICE)
  Calculator EPS  : PLN {eps:.2f}
  Min-viable P/E  : {EPP_MIN_PE}×  (distressed grocery, not zero)
  EPP floor       : PLN {EPP:.0f}
  Current vs EPP  : {epp_gap:+.1f}%  (growth premium priced in; justified while rollout intact)

④ CONSERVATIVE GROWTH CASE
  EPS CAGR {CONS_EPS_CAGR*100:.0f}%/yr (half historical rate); exit {CONS_EXIT_PE:.0f}×; no dividend
  FY+2 EPS : PLN {cons_eps_2yr:.2f}
  Exit price: PLN {cons_price:.0f}  ({CONS_EXIT_PE:.0f}× × {cons_eps_2yr:.2f})
  2yr return: {cons_ret_pct:+.1f}%  (no dividend; full FCF reinvested)
  At 18% CAGR / 26× exit: 2yr return ≈ {(EPP_EPS*(1.18)**2*26-CURRENT_PRICE)/CURRENT_PRICE*100:.0f}%

⑤ VOLATILITY CONTEXT
  52-week range : PLN {VOL_52W_LOW:.0f} – {VOL_52W_HIGH:.0f}
  Current       : PLN {CURRENT_PRICE:.0f}  ({(CURRENT_PRICE-VOL_52W_LOW)/(VOL_52W_HIGH-VOL_52W_LOW)*100:.0f}th pct of range)
  Annual vol    : {VOL_ANNUAL*100:.0f}%   Beta: {VOL_BETA:.2f}×
  1σ range (1yr): PLN {CURRENT_PRICE*(1-VOL_ANNUAL):.0f} – PLN {CURRENT_PRICE*(1+VOL_ANNUAL):.0f}
  Float ~48%; thin liquidity amplifies both drawdowns and squeeze rallies.

⑥ SCENARIO PROBABILITIES  (composite {adj:.2f})""")

for k in ["BEAR","BASE","BULL","XBULL"]:
    e, pe, p, narr = SCENARIOS[k]
    print(f"  {k:<6} {probs[k]*100:5.1f}%  PLN {e:.1f} EPS × {pe}P/E = PLN {p}   {narr}")

print()

# ─────────────────────────────────────────────────────────────────────────────
# PART 3 NUMBERS & SIGNALS
# ─────────────────────────────────────────────────────────────────────────────
print()
print("PART 3 NUMBERS & SIGNALS")
print("=" * 72)

bear_p   = SCENARIOS["BEAR"][2]
bull_p   = SCENARIOS["BULL"][2]
dn       = (CURRENT_PRICE - bear_p) / CURRENT_PRICE
up       = (bull_p - CURRENT_PRICE) / CURRENT_PRICE
ratio_b  = dn / up
rb_fmt   = f"{ratio_b:.2f}x"

signal_short = ("BUY"        if ratio_b < 0.75 else
                "ACCUMULATE" if ratio_b < 1.10 else
                "WATCHLIST"  if ratio_b < 1.75 else
                "AVOID")
signal = {"BUY":"◉ BUY","ACCUMULATE":"◎ ACCUMULATE","WATCHLIST":"◐ WATCHLIST","AVOID":"✕ AVOID"}[signal_short]

print(f"""
  Ticker          : DNP  (Warsaw Stock Exchange / GPW)
  Company         : Dino Polska S.A.
  Sector          : Polish Grocery Retail · Standalone Discount Format
  Currency        : PLN  (EUR/PLN ≈ 4.25)
  Price           : PLN {CURRENT_PRICE:.0f}  (≈ EUR {CURRENT_PRICE/4.25:.0f})
  Stores          : {STORES:,}  (+{NEW_STORES_TTM} net new TTM)
  EPS (calc)      : PLN {eps:.2f}
  EPP floor       : PLN {EPP:.0f}  ({EPP_EPS:.1f} × {EPP_MIN_PE}×)
  EPP gap         : {epp_gap:+.1f}%
  Downside (Bear) : {dn*100:.1f}%  →  PLN {bear_p}
  Upside (Bull)   : {up*100:.1f}%  →  PLN {bull_p}
  Ratio B         : {rb_fmt}
  Expected value  : PLN {ev:.0f}  ({up_pct:+.1f}%)
  Conservative 2yr: {cons_ret_pct:+.1f}%  (PLN {cons_price:.0f}; no dividend)
  Signal          : {signal}
  Proxy composite : {proxy:.2f}
  Adj. composite  : {adj:.2f}  (SCA {sca:+.2f})
  Market-implied  : {mic:.2f}  →  {verdict}
""")
print("━" * 72)
print(f"  SIGNAL: {signal}   Ratio B: {rb_fmt}")
print(f"  Adj. composite {adj:.2f} vs market-implied {mic:.2f} (gap {gap:+.2f})")
print("━" * 72)
print()
print("  KEY MOATS:")
print(f"  • {STORES:,} owned stores: asset base immune to rent inflation; resale backstop")
print(f"  • Fresh meat/deli in-store: ~30% revenue; Biedronka cannot replicate at scale")
print(f"  • {WHITESPACE_PCT:.0f}% geographic whitespace: multi-year organic growth runway, no M&A needed")
print(f"  • Biernacki (52%): aligned owner-operator; no dividends; reinvests at 20%+ ROIC")
print()
print("  KEY RISKS:")
print(f"  • Polish min-wage hikes outpace pricing → margin erosion")
print(f"  • Biedronka rural push → LFL deceleration + store density headwinds")
print(f"  • Thin float (~48%): illiquid in stress; bid-ask widens on drawdowns")
print(f"  • CIT/tax policy uncertainty (Polish government)")
print()
print("  Not financial advice. Prices in PLN. EPP = EPS × min-viable trough P/E.")
