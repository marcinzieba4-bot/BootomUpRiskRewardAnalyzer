#!/usr/bin/env python3
"""
XTB Signal Model
──────────────────
Same framework applied to XTB S.A. (WSE: XTB).

⚠  Prices and EPS are in PLN (Polish złoty). XTB trades on the Warsaw
   Stock Exchange; roughly PLN 4.1 = USD 1.0 (May 2026).

Key structural differences from the other companies in this framework:
  Revenue is not driven by products, contracts, or ARR —
  it is driven by: CLIENTS × ACTIVITY × MARKET VOLATILITY
  In record years (2022, 2024): revenue per active client ~PLN 4,200
  In quiet years (2020, 2023): revenue per active client ~PLN 1,500-2,000
  The client BASE grows structurally; revenue per client mean-reverts

  NEW: XTB is transitioning from pure-play CFD broker to investment
  platform (ETF investing, savings deposits, multi-asset). If the
  recurring revenue mix reaches 25-30%, the multiple re-rates from
  ~12x (volatile broker) to ~15-16x (semi-recurring fintech).

The market prices XTB's volatile revenue conservatively. Proxy signals
say conditions are BULL. The gap is real but justified — it is the
structural volatility discount, not a mispricing.

Run: python xtb_signal_model.py
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 58.0      # PLN (WSE: XTB, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

# Scenario 2-year price targets (non-GAAP EPS × exit P/E, all in PLN)
# XTB multiples compressed by revenue volatility and Polish market discount.
# FY2024 actual: EPS ~PLN 6.0 (record year). FY2025E ~PLN 3.0 (normalising).
# FY2027 scenarios assume ~292M shares outstanding.
SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  ( 2.5,    8,    20,  "Low vol; crypto winter; margin pressure; client churn"),
    "BASE":  ( 4.5,   12,    54,  "Moderate activity; steady client growth; ECB rates hold"),
    "BULL":  ( 7.0,   14,    98,  "Elevated vol; crypto active; ETF platform growing fast"),
    "XBULL": (10.0,   16,   160,  "Retail frenzy + crypto cycle + ETF re-rating to fintech"),
}

# ── CLIENT ECONOMICS CALCULATOR (XTB-specific structural feature) ─────────
# Total revenue = Active clients × Revenue per active client
# Active clients is STRUCTURAL (cumulative base → 400K+ new per year)
# Revenue per active client is CYCLICAL (tied to volatility and asset prices)
#
# This decomposition shows: the market should ALWAYS be willing to pay
# for the client base growth, even if revenue per client normalises.

REGISTERED_CLIENTS_M     = 1.54    # total registered (millions, cumulative)
ACTIVE_CLIENTS_K         = 650     # active in last 12 months (thousands)
ACTIVATION_RATE          = ACTIVE_CLIENTS_K / (REGISTERED_CLIENTS_M * 1000)
REVENUE_PER_CLIENT_CURR  = 4_200   # PLN/yr, current (elevated volatility year)
REVENUE_PER_CLIENT_NORM  = 2_200   # PLN/yr, 10-year normalised average
NEW_CLIENTS_PER_YEAR_K   = 420     # organic new registrations/yr (thousands)
ETFINVEST_CLIENTS_K      = 380     # clients using ETF/savings platform (thousands)
ETFINVEST_AVG_AUM_PLN    = 8_500   # PLN avg AUM per ETF investor

def client_economics():
    floor_rev  = (ACTIVE_CLIENTS_K * 1000) * REVENUE_PER_CLIENT_NORM / 1e9  # PLN B
    curr_rev   = (ACTIVE_CLIENTS_K * 1000) * REVENUE_PER_CLIENT_CURR / 1e9
    etf_aum    = ETFINVEST_CLIENTS_K * 1000 * ETFINVEST_AVG_AUM_PLN / 1e9   # PLN B
    # ETF income: XTB earns via spread/management equivalent ~0.5% p.a.
    etf_rev    = etf_aum * 0.005
    # In 2 years at current acquisition pace, active base grows ~30%
    future_k   = ACTIVE_CLIENTS_K + NEW_CLIENTS_PER_YEAR_K * 2 * ACTIVATION_RATE
    future_floor_rev = future_k * 1000 * REVENUE_PER_CLIENT_NORM / 1e9
    return floor_rev, curr_rev, etf_aum, etf_rev, future_k, future_floor_rev

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
# Chosen to cover: market volatility (primary revenue driver), client
# growth (structural base), crypto activity (large revenue segment),
# European trading volumes (regional client base), interest rates
# (deposit income), and peer brokers (direct comparable).
#
# (name, value, unit, base_floor, bull_floor, xbull_floor, higher_is_better,
#  what_it_drives_for_XTB)
SIGNALS = [
    # VIX (CBOE Volatility Index): 22.0.
    # When equity markets are volatile, retail clients trade more CFDs on
    # indices, FX, and commodities. VIX is the single best weekly proxy for
    # XTB's transaction revenue. At VIX 22, conditions are BULL-grade for activity.
    ("VIX — CBOE Volatility Index",      22.0, "pts",      15,  22,  30, True,
     "primary revenue driver: high vol → more CFD trading → higher spread revenue"),

    # XTB active clients YoY: +52%.
    # XTB publishes monthly KPI data including new registrations and active count.
    # Active client growth is the structural driver that survives volatility cycles.
    # +52% YoY is BULL — continues the 40-60% growth streak of 2022-2024.
    ("XTB active clients — YoY growth",  52.0, "% YoY",   20,  40,  65, True,
     "structural revenue growth regardless of vol cycle; client base compounds"),

    # Crypto market cap YoY: -20%.
    # XTB derives significant revenue from crypto CFDs (BTC, ETH, altcoins).
    # BTC at ~$77K vs ~$103K May 2025 = -26% YoY. Crypto market cap similarly.
    # BEAR directionally but clients still trade crypto in declining markets.
    # Threshold relaxed to account for two-way trading (clients go short too).
    ("Crypto market cap — YoY",         -20.0, "% YoY",  -25,   5,  40, True,
     "crypto CFD revenue (~20% of total); both bull and bear markets drive volume"),

    # European equity trading volume YoY: +15%.
    # Tariff uncertainty + ECB policy pivots have driven elevated Euronext volumes.
    # XTB's largest client base is European; EU equity vol leads CFD activity.
    ("European equity trading vol YoY",  15.0, "% YoY",    5,  15,  30, True,
     "CFD demand signal; European clients (DE, ES, PL, UK) are core revenue base"),

    # ECB deposit rate: 2.5%.
    # XTB holds client cash deposits and earns the spread on uninvested balances.
    # Rate hike cycle created a new revenue stream (~€40-60M/yr at current levels).
    # Not yet back to near-zero (structural improvement vs 2020-2021).
    ("ECB deposit rate",                  2.5, "%",        1.0, 2.5, 4.0, True,
     "deposit interest income on EUR client cash; ~15% of revenue at 2.5% ECB rate"),

    # IG Group revenue YoY: +12%.
    # IG Group (LSE: IGG) is the closest comparable retail CFD broker.
    # IG reports quarterly; its revenue YoY is the best short-lead proxy
    # for XTB's revenue before XTB reports. Strong IG → strong XTB.
    ("IG Group revenue — YoY",           12.0, "% YoY",    0,  10,  25, True,
     "peer proxy: IG Group revenue leads XTB by ~4 weeks (IG reports earlier)"),
]
WEIGHTS = [0.25, 0.20, 0.15, 0.15, 0.15, 0.10]

STRUCTURAL_FACTORS = [
    ("ESMA leverage restriction / regulatory risk",  -0.8, 0.30),
    ("ETF / investment platform client stickiness",   0.5, 0.20),
    ("Bank and neobank competitive entry",           -0.3, 0.20),
    ("Net cash + high dividend yield",                0.5, 0.15),
    ("Warsaw listing / emerging-market discount",    -0.3, 0.15),
]

# ── SCORING ───────────────────────────────────────────────────────────────
def score_signal(val, base_f, bull_f, xbull_f, hib):
    if hib:
        if val >= xbull_f: return 4
        if val >= bull_f:  return 3
        if val >= base_f:  return 2
        return 1
    else:
        if val <= xbull_f: return 4
        if val <= bull_f:  return 3
        if val <= base_f:  return 2
        return 1

ICONS = {4: "★ XBULL", 3: "▲ BULL", 2: "◦ BASE", 1: "⚠ BEAR"}

def softmax_probs(composite, T=0.60):
    centres = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    raw = {k: math.exp(-abs(composite - c) / T) for k, c in centres.items()}
    tot = sum(raw.values())
    return {k: v / tot for k, v in raw.items()}

def expected_price(probs):
    return sum(probs[k] * SCENARIOS[k][2] for k in probs)

def market_implied_composite(target_ev, tolerance=0.5):
    for c in [x / 100 for x in range(100, 401)]:
        if abs(expected_price(softmax_probs(c)) - target_ev) < tolerance:
            return round(c, 2), softmax_probs(c)
    return None, None

# ── MAIN ──────────────────────────────────────────────────────────────────
W = 72

scored = [(name, val, unit, score_signal(val, bf, bull_f, xf, hib), w, rt)
          for (name, val, unit, bf, bull_f, xf, hib, rt), w in zip(SIGNALS, WEIGHTS)]
proxy_composite = sum(s * w for *_, s, w, _ in scored)
sca             = sum(s * w for _, s, w in STRUCTURAL_FACTORS)
adj_composite   = proxy_composite + sca
proxy_probs     = softmax_probs(proxy_composite)
proxy_ev        = expected_price(proxy_probs)

market_target_ev  = CURRENT_PRICE * ((1 + REQUIRED_RETURN) ** HORIZON_YEARS)
mkt_composite, mkt_probs = market_implied_composite(market_target_ev)
mkt_ev = expected_price(mkt_probs) if mkt_probs else market_target_ev

floor_rev, curr_rev, etf_aum, etf_rev, future_k, future_floor_rev = client_economics()

print()
print("═" * W)
print("  XTB SIGNAL MODEL  —  proxy vs. market-implied probability  [PLN]")
print("═" * W)
print(f"  ⚠  All prices and EPS in PLN (Polish złoty).  PLN/USD ≈ 0.24")

# Client economics
print(f"\n  CLIENT ECONOMICS  (revenue = clients × activity × volatility)")
print("  " + "─" * (W-2))
print(f"  Total registered clients:                {REGISTERED_CLIENTS_M*1e6:>10,.0f}")
print(f"  Active clients (last 12M):               {ACTIVE_CLIENTS_K*1000:>10,.0f}  ({ACTIVATION_RATE*100:.0f}% activation rate)")
print(f"  New registrations per year (est.):       {NEW_CLIENTS_PER_YEAR_K*1000:>10,.0f}")
print(f"  Revenue/active client — current yr:      PLN {REVENUE_PER_CLIENT_CURR:>6,}  (elevated volatility)")
print(f"  Revenue/active client — 10yr normal:     PLN {REVENUE_PER_CLIENT_NORM:>6,}  (normalised)")
print(f"  ─────────────────────────────────────────────────────")
print(f"  Floor revenue (current base × normal):   PLN {floor_rev:.1f}B / yr")
print(f"  Current run-rate (current × elevated):   PLN {curr_rev:.1f}B / yr")
print(f"  In 2yrs at current acq pace, active:     ~{future_k:>6,.0f}K  (~{future_k/1000:.1f}M clients)")
print(f"  → 2yr floor (growing base × normal):     PLN {future_floor_rev:.1f}B / yr  (structural floor grows)")
print(f"\n  ETF / Investment Platform (re-rating driver):")
print(f"  ETF/savings platform clients:            {ETFINVEST_CLIENTS_K*1000:>10,.0f}")
print(f"  Estimated total AUM:                     PLN {etf_aum:.1f}B")
print(f"  Recurring fee-equivalent (~0.5% AUM):    PLN {etf_rev*1000:.0f}M / yr  (small but compounding)")
print(f"  → At PLN 20B AUM × 0.5% = PLN 100M/yr in recurring rev — the re-rating trigger.")

# Signal scorecard
print(f"\n  PROXY SIGNAL SCORECARD")
print(f"  {'Signal':<38}{'Value':>9}  Wt   Score")
print("  " + "─" * (W-2))
for name, val, unit, s, w, rt in scored:
    bar = "█" * s + "░" * (4 - s)
    fmt = f"{val:>+7.1f}"
    print(f"  {name:<38}{fmt}{unit[0]}  {w*100:.0f}%  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:   {proxy_composite:.2f} / 4.00")
if mkt_composite:
    print(f"  Market composite:  {mkt_composite:.2f} / 4.00  "
          f"(back-solved from PLN {CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% reqd return)")
    gap = proxy_composite - mkt_composite
    print(f"  Gap (proxy − mkt): {gap:+.2f}  ← volatility discount; market sees same proxies")

# Valuation context
print(f"\n  VALUATION CONTEXT  (PLN)")
print("  " + "─" * (W-2))
print(f"  Current price:            PLN {CURRENT_PRICE:.0f}")
print(f"  FY2024 actual EPS:        PLN ~6.0  (record year)")
print(f"  FY2025E EPS (normalised): PLN ~3.0  (-50% from peak)")
print(f"  Current trailing P/E:     ~{CURRENT_PRICE/6.0:.0f}x  (on FY2024 record)")
print(f"  Current forward P/E:      ~{CURRENT_PRICE/3.0:.0f}x  (on FY2025E normalised)")
print(f"  Dividend policy:          60% of net profit → yield ~8-10% at current price")
print(f"  Net cash:                 Strong — no debt, significant cash buffer")
print(f"  → P/E 10-12x on normalised earnings; 14-16x possible if ETF platform re-rates")

# Structural overlay
print(f"\n  STRUCTURAL RISK OVERLAY  (analyst-assessed; beyond proxy signals)")
print("  " + "─" * (W-2))
print(f"  {'Factor':<44}  {'Score':>5}  {'Wt':>3}   {'Adj':>5}")
for desc, score, wt in STRUCTURAL_FACTORS:
    adj_c = score * wt
    arrow = "▲" if score > 0 else "▼"
    print(f"  {desc:<44}  {score:>+5.1f}  {wt*100:>3.0f}%  {adj_c:>+5.2f}  {arrow}")
print(f"  {'─'*68}")
print(f"  Structural adj. (SCA):     {sca:>+6.2f}")
print(f"  Adjusted composite:         {adj_composite:.2f}  "
      f"(proxy {proxy_composite:.2f} {'+' if sca >= 0 else ''}{sca:.2f})")
if mkt_composite:
    adj_gap = adj_composite - mkt_composite
    if   adj_gap >  0.50: _verdict = "UNDERVALUED"
    elif adj_gap >  0.20: _verdict = "MODESTLY UNDERVALUED"
    elif adj_gap > -0.20: _verdict = "FAIRLY VALUED"
    elif adj_gap > -0.50: _verdict = "MODESTLY OVERVALUED"
    else:                 _verdict = "OVERVALUED"
    print(f"  Market composite:          {mkt_composite:.2f}")
    print(f"  ADJUSTED GAP:             {adj_gap:>+6.2f}  ← {_verdict}")

# Probability table
print(f"\n  {'Scenario':<10}  {'Proxy':>8}  {'Market':>8}  {'Gap':>8}  "
      f"{'EPS':>6}  {'Mult':>5}  {'Price':>7}  Narrative")
print("  " + "─" * (W-2))
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    eps, mult, price, narr = SCENARIOS[k]
    pp  = proxy_probs[k]
    mp  = mkt_probs[k] if mkt_probs else 0
    gap_pp = pp - mp
    sign = "+" if gap_pp >= 0 else ""
    print(f"  {k:<10}  {pp*100:>7.1f}%  {mp*100:>7.1f}%  "
          f"{sign}{gap_pp*100:>6.1f}pp  {eps:>5.1f}  {mult:>4}x  {price:<7}  {narr[:28]}…")

print(f"\n  Prob-weighted 2yr:  proxy PLN {proxy_ev:.0f}  /  market PLN {mkt_ev:.0f}")
print(f"  Current price: PLN {CURRENT_PRICE:.0f}")

# Verdict
print(f"\n  WHAT THE GAP MEANS")
print("  " + "─" * (W-2))
gap = (proxy_composite - mkt_composite) if mkt_composite else 0
print(f"""  Proxy composite {proxy_composite:.2f}  vs  market-implied {mkt_composite:.2f}.
  Gap = {gap:+.2f}

  Cross-stock gap comparison (full framework):
    ORCL gap = +2.16  (proxies XBULL; market prices delivery/concentration risk)
    AVGO gap = +1.41  (proxies bullish; market prices flow-through uncertainty)
    SAP  gap = +0.91  (proxies constructive; Joule and FX drag unresolved)
    XTB  gap = {gap:+.2f}  ← volatility discount on cyclical revenue
    COIN gap = +0.29  (approximately fairly priced; thesis is just BTC)
    CAT  gap = -0.24  (market already priced ahead of proxy confirmation)

  WHY THE GAP EXISTS — AND WHY IT'S LARGELY JUSTIFIED:

    The gap for XTB is SMALLER than AVGO/SAP/ORCL not because the
    signals are weaker, but because the market ALREADY KNOWS the
    signals are temporary:

    1. Revenue per client mean-reverts: VIX at 22 drives revenue/client
       to PLN 4,200. When VIX normalises to 15, that falls to PLN 1,800.
       The market applies normalised earnings (PLN 3-4 EPS), not current
       elevated earnings (PLN 5-6 EPS). This is correct and rational.

    2. Crypto signal is structurally mixed: XTB earns whether BTC goes
       up or down — but absolute price level matters for retail engagement.
       At BTC $77K (-26% YoY), retail crypto traders are less active than
       at $103K. The -20% crypto cap score drags composite below pure-BULL.

    3. Dividend policy creates re-investment competition: XTB pays out
       60% of profit as dividends. At PLN 3 normalised EPS and 60% payout,
       yield is ~3.1 PLN / PLN 58 = ~5.3%. Investors compare this to
       Polish government bonds (~5.5%) — limiting re-rating potential.

  THE CASE FOR A HIGHER MULTIPLE OVER 2 YEARS:

    The ETF/investment platform is the re-rating catalyst. Every broker
    that successfully transitions from 100% transaction revenue to 70/30
    transaction/recurring gets a 3-4x multiple expansion:
      eToro: filed for IPO at ~18x earnings on growing recurring base
      Robinhood: re-rated from 8x to 22x when Gold subscriptions became
                 material (recurring $10/month per subscriber)

    XTB's path: PLN 20B ETF AUM is the threshold. At that scale:
      PLN 100M/yr recurring fee-equivalent (vs ~PLN 0M in 2020)
      Demonstrates client stickiness beyond the volatility cycle
      Justifies 14-16x rather than 10-12x on normalised earnings
      At PLN 4.5 EPS × 15x = PLN 67.5 (+16% from current PLN 58)

    That re-rating doesn't require a record volatility year —
    it requires PROOF OF PLATFORM STICKINESS. That's the non-consensus
    catalyst: XTB's ETF clients are revealed to have 2-3x higher LTV
    than pure-CFD clients, changing the multiple conversation.

  WHAT MAKES XTB DIFFERENT FROM THE OTHER FIVE COMPANIES:
    • Only non-subscription / non-contract revenue model in the set
    • Revenue can literally double or halve year-over-year (not SAP ARR)
    • The STRUCTURAL driver (client base growth) is hidden by the
      CYCLICAL driver (revenue per client) in reported EPS
    • Investors who track monthly active client data have a genuine edge:
      the gap between registered (1.54M) and active (650K) represents
      ~890K dormant clients who can be reactivated in high-vol periods —
      each 10% reactivation of dormant clients = +PLN 0.6-1.0B revenue""")
print()
print("═" * W)
