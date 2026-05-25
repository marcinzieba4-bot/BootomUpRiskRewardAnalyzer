"""
PKN Orlen (WSE: PKN) — BottomUp Risk/Reward Signal Model
NOTE: PLN-denominated stock (Polish Złoty) on Warsaw Stock Exchange (GPW/WSE).
      All prices and EPS figures in PLN.

SIGNAL:  ✕ AVOID
RATIO B: ~290× (Method B price barely above current — effectively N/A)
DATE:    2026-05-25
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER        = "PKN"
COMPANY       = "Orlen S.A."
SECTOR        = "Integrated Energy · Oil Refining · Upstream Gas · Petrochemicals · Power"
CURRENCY      = "PLN"  # Polish Złoty — Warsaw Stock Exchange (GPW/WSE)

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE = 144.50   # PKN.WA — fetched from Yahoo Finance / Investing.com, 2026-05-25
PRICE_52W_LOW  = 69.20   # 52-week low (June/July 2025 trough)
PRICE_52W_HIGH = 146.98  # 52-week high / ALL-TIME HIGH (May 12, 2026 — 2 weeks ago)
SHARES_M      = 1162.4   # million shares outstanding (post-merger combined group)

# ── EPS (adjusted/normalized, non-GAAP) ───────────────────────────────────────
# NOTE: GAAP EPS is unreliable due to massive merger-related write-downs.
#   FY2025 GAAP net profit: PLN 2.65B (distorted by PLN ~16B impairments from
#   Lotos/PGNiG/Energa acquisition accounting) → GAAP EPS ~PLN 2.28
#   FY2025 ADJUSTED net income: PLN 11.1B → adj EPS PLN 9.57 (key metric)
#   FY2025 EBITDA LIFO: PLN 41.5B (industry standard for refining/energy)
#   Analyst consensus uses adjusted EPS consistently; models use adj below.
EPS_TROUGH    = 9.57     # FY2025 adj — lowest adj EPS in modern Orlen Group history
EPS_FY2024    = 1.27     # FY2024 adj — distorted year; GAAP ~PLN 1.26 ≈ adj; merger chaos
EPS_NOW       = 12.50    # FY2026E adj estimate (improving upstream + merger synergies)
EPP_MIN_PE    = 6        # Trough P/E for integrated energy company (CEE context)
EPP           = EPS_TROUGH * EPP_MIN_PE   # 9.57 × 6 = PLN 57.42

# ── Method B ──────────────────────────────────────────────────────────────────
# Analyst consensus FY2027E adj EPS = PLN 14.48 (source: Investing.com consensus, May 2026)
# Exit P/E = 10× (generous upper end for integrated energy; CEE energy typically 6-10×)
# At 10×, price_b = PLN 144.80 — barely above current price → ratio_b ~290×
# At  9×, price_b = PLN 130.32 — BELOW current price → N/A → AVOID
# Either way: stock is AT or ABOVE its 2-year base case fair value target.
CONS_EPS_2YR  = 14.48    # FY2027E adj consensus (Investing.com, 9 analysts)
CONS_EXIT_PE  = 10       # Upper-end energy sector fair value multiple (optimistic)

# ── Computed signals ──────────────────────────────────────────────────────────
price_b = CONS_EPS_2YR * CONS_EXIT_PE           # PLN 144.80

if price_b <= CURRENT_PRICE:
    ratio_b    = None
    ratio_b_fmt = "N/A"
    signal_primary = "✕ AVOID"
else:
    ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
    if   ratio_b < 0:       signal_primary = "◉ BUY"
    elif ratio_b < 0.75:    signal_primary = "◉ BUY"
    elif ratio_b < 1.1:     signal_primary = "◎ ACCUMULATE"
    elif ratio_b < 1.75:    signal_primary = "◐ WATCHLIST"
    elif ratio_b < 2.5:     signal_primary = "▷ HOLD/TRIM"
    else:                   signal_primary = "✕ AVOID"
    ratio_b_fmt = f"{ratio_b:.2f}x"

epp_gap_pct   = (CURRENT_PRICE - EPP) / EPP * 100

# ── Scenario prices ──────────────────────────────────────────────────────────
# BEAR: Oil price -40% cycle; EBITDA LIFO -50%; trough adj EPS ~PLN 5; 6× → PLN 30
# BASE: FY2027E adj EPS PLN 14.48 at 10× fair = PLN 145 (essentially current price)
# BULL: FY2028E adj EPS PLN 17 × 11× = PLN 187 (+29%)
# XBULL: Full cycle peak PLN 22 × 12× = PLN 264 (+83%) — requires $100/bbl oil + upstream scale
PRICE_BEAR  = 30
PRICE_BASE  = 145
PRICE_BULL  = 187
PRICE_XBULL = 264

# ── SCA (Stock-Composite Adjustment) ─────────────────────────────────────────
# Six cross-read factors: rate each -1 to +1, apply weight, sum, divide by 2.0
SCA_FACTORS = [
    # (score, weight, label)
    (+0.60, 0.20, "Upstream gas/oil production growth (YoY)"),        # IDIO +
    (-0.70, 0.25, "Government regulatory risk / fuel price caps"),     # IDIO -
    (+0.50, 0.15, "Dividend sustainability (PLN 8/shr; 5.5% yield)"),  # IDIO +
    (-0.50, 0.25, "Oil/gas macro: crude ~$70-75/bbl, declining"),      # MACRO -
    (+0.30, 0.10, "Polish economy: GDP +3%, EU funds inflow"),         # MACRO +
    (-0.30, 0.05, "Capex burden PLN 36B/yr; FCF limited"),             # IDIO -
]
sca_raw = sum(s * w for s, w, _ in SCA_FACTORS)   # –0.088
sca_adj = sca_raw / 2.0                            # –0.044

# ── Composite inference (softmax engine) ──────────────────────────────────────
CENTRES   = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
T         = 0.60

def _logit(c, x): return -((x - c) ** 2) / T
def softmax_weights(composite):
    raw = {k: math.exp(_logit(v, composite)) for k, v in CENTRES.items()}
    tot = sum(raw.values())
    return {k: v / tot for k, v in raw.items()}

def expected_price(composite):
    w = softmax_weights(composite)
    prices = {"BEAR": PRICE_BEAR, "BASE": PRICE_BASE,
              "BULL": PRICE_BULL, "XBULL": PRICE_XBULL}
    return sum(w[k] * prices[k] for k in prices)

def infer_composite(target_price, lo=1.0, hi=4.0, iters=60):
    for _ in range(iters):
        mid = (lo + hi) / 2
        if expected_price(mid) < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

market_composite  = infer_composite(CURRENT_PRICE)
adj_composite     = market_composite + sca_adj

def composite_label(c):
    if   c < 1.625: return "BEAR"
    elif c < 2.375: return "BASE"
    elif c < 3.25:  return "BULL"
    else:           return "XBULL"

market_label = composite_label(market_composite)
adj_label    = composite_label(adj_composite)

# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 72)
print(f"  {TICKER}  —  {COMPANY}")
print(f"  {SECTOR}")
print(f"  NOTE: PLN-denominated (Warsaw Stock Exchange, GPW/WSE)")
print("=" * 72)

print("""
PART 1 — FRAMEWORK OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This model uses a three-input bottoms-up risk/reward framework:

  EPP (Earnings Power Price) — structural floor
    = EPS_TROUGH × EPP_MIN_PE
    Anchors to the worst foreseeable normal-cycle EPS; migrates up as EPS grows.
    For energy companies, trough P/E = 6-7× (commodity cycle trough multiple).

  Method B — 2-year normalized upside ceiling
    = CONS_EPS_2YR × CONS_EXIT_PE
    Analysts' 2-year forward EPS × sector fair-value exit multiple.

  Ratio B (PRIMARY signal) — where current price sits in the range [EPP → B]
    = (CURRENT_PRICE − EPP) / (price_b − CURRENT_PRICE)
    < 0.75  : BUY
    0.75–1.1 : ACCUMULATE
    1.1–1.75 : WATCHLIST
    1.75–2.5 : HOLD/TRIM
    > 2.5   : AVOID
    N/A (price_b ≤ CURRENT_PRICE): stock AT or ABOVE 2-year upside ceiling → AVOID

Note on PKN Orlen EPS:
  GAAP EPS is unreliable due to PLN 30-40B cumulative write-downs from the
  Lotos (2022), PGNiG (2022), and Energa (2020) mergers. All EPS figures
  below are ADJUSTED (normalized), which is the standard analyst metric.
  Key indicator: EBITDA LIFO (inventory-adjusted EBITDA, sector standard).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PKN ORLEN: POLAND'S ENERGY TITAN — BUT PRICED FOR IT
======================================================

PKN Orlen is Poland's largest company and Central Europe's dominant integrated
energy group, formed through the government-orchestrated acquisitions of Lotos
(oil refining, 2022), PGNiG (natural gas upstream/distribution, 2022), and
Energa (electricity, 2020). The combined group is a true national energy
champion: ~PLN 270B in annual revenues, 5,400 petrol stations, upstream gas
production (primarily Norwegian shelf via PGNiG Norway), 10 refineries, and
power generation assets. The Polish government (through PFR and State Treasury)
controls ~49% of the float.

THE RALLY: +110% FROM 52-WEEK LOW IN 12 MONTHS
═══════════════════════════════════════════════
PKN bottomed at PLN 69.20 in mid-2025 during a period of:
  • Declining crude oil prices (-14% in 2025)
  • Uncertainty over Polish government fuel price caps
  • Market digesting the PLN 16B+ of cumulative acquisition write-downs
  • Concerns about the PLN 36B/year capex programme overstretching FCF

The subsequent +110% rally to PLN 146.98 ATH (May 12, 2026) was driven by:
  • Upstream outperformance: Q1 2026 net profit +54% YoY; EBITDA LIFO jump
  • PGNiG synergies materialising: gas upstream diversification proving valuable
  • Dividend raised to PLN 8/share (record high; PLN 9.3B total payout)
  • European energy security re-rating: investors pay premium for reliable supply
  • Macro: PLN strengthening, Polish GDP +3%, EU structural funds inflow
  • Short squeeze dynamics as bear case (fuel price cap risk) failed to materialise

BUSINESS QUALITY: GENUINE MOAT, GENUINE COMPLEXITY
═══════════════════════════════════════════════════
Strengths:
  • 5,400 petrol stations = dominant retail fuel network in CEE (moat)
  • PGNiG Norway: significant upstream gas production on Norwegian continental shelf
  • Long-term LNG contracts + Baltic Pipe = strategic gas import diversification
  • Petrochemicals (Orlen Południe, Anwil) = essential input for Polish agriculture
  • National strategic importance = implicit government support / no bankruptcy risk
  • EBITDA LIFO FY2025: PLN 41.5B — massive cash generation

Structural risks:
  • Oil price dependency: ~40% of adj EBITDA tied to refining margins/crude prices
  • Government interference: Polish government has historically imposed price caps,
    dividend extraction, and strategic directives inconsistent with shareholder value
  • Capital allocation: PLN 36B/yr capex (FY2026 plan) = free cash flow barely covers
    dividends + capex; net debt rising
  • Management risk: post-merger integration complexity still unresolved
  • Energy transition: long-term structural headwind for refining/fossil fuel assets
  • Political sensitivity: election cycles in Poland directly affect Orlen policy

THE VALUATION PROBLEM: STOCK PRICED AT 2-YEAR FAIR VALUE TODAY
═══════════════════════════════════════════════════════════════
FY2027E adj EPS consensus: PLN 14.48 (Investing.com, 9 analysts)
A fair-value multiple for an integrated energy company in CEE is 9-10× (not
lower, not higher — 6× is trough, 12× is peak-cycle premium).

At 10× FY2027E: price_b = PLN 144.80 ≈ CURRENT PRICE PLN 144.50.

This is the most direct AVOID signal in the framework: the stock has ALREADY
rallied to meet its 2-year base-case fair value target. Every additional gain
from here requires either:
  a) Higher-than-consensus EPS (oil price re-acceleration to $90+/bbl), or
  b) Multiple expansion above 10× (unusual for CEE energy)

Neither is the base case. Analyst consensus average target: PLN ~120-127 —
12-17% BELOW the current price. The market has gotten ahead of the analysts.

DIVIDEND YIELD TRAP WARNING
════════════════════════════
PLN 8/share dividend at PLN 144.50 = 5.5% yield. This is attractive in
absolute terms. However:
  • Total payout PLN 9.3B vs FY2025 GAAP net profit PLN 2.65B = paying 3.5×
    earnings (funded from adj operating cash flow, not GAAP profit)
  • If adj EPS declines to PLN 10-11 (oil price down 20%), the PLN 8 dividend
    becomes unsustainable (80% payout on adj earnings)
  • 5.5% yield does NOT compensate for -15% to -20% price risk if oil corrects

WHERE THE RISK/REWARD IMPROVES
════════════════════════════════
  WATCHLIST   : PLN 105–115 (ratio_b ~1.5×; FY2027E at 7.5-8×; yield ~7%)
  ACCUMULATE  :  PLN 90–100 (ratio_b ~0.75×; trough P/E zone; aligned with
                             analyst consensus avg target range)
  BUY         :  PLN 65–75  (ratio_b <0.5×; below EPP; maximum fear zone;
                             52-wk low was PLN 69.20 — proved to be a BUY)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("PART 3 — NUMBERS & SIGNALS")
print("=" * 72)
print(f"""
  ┌─────────────────────────────────────────────────────────────┐
  │  SIGNAL:  {signal_primary:<12}  │  RATIO B: {ratio_b_fmt:<10}          │
  │  TICKER:  {TICKER:<10}    │  CURRENCY: PLN (Warsaw/GPW)    │
  └─────────────────────────────────────────────────────────────┘

  ----------------------------------------------------------------------
""")

print(f"  Current price       : PLN {CURRENT_PRICE:.2f}  (+110% from 52-wk low PLN {PRICE_52W_LOW}; -2% from ATH PLN {PRICE_52W_HIGH})")
print(f"  EPP floor           : PLN {EPP:.2f}  (+{epp_gap_pct:.1f}% above; {EPP_MIN_PE}× × PLN {EPS_TROUGH}; aligns with pre-rally zone)")
print(f"  Method B target     : PLN {price_b:.2f}  (FY2027E PLN {CONS_EPS_2YR} × {CONS_EXIT_PE}× = AT current price → ratio_b {ratio_b_fmt})")
print(f"  BEAR scenario       : PLN {PRICE_BEAR}  (-79%; oil -40% cycle; trough EBITDA; adj EPS ~PLN 5; 6×)")
print(f"  BASE scenario       : PLN {PRICE_BASE}  (~flat; FY2027E PLN {CONS_EPS_2YR} × {CONS_EXIT_PE}× = already priced)")
print(f"  BULL scenario       : PLN {PRICE_BULL}  (+29%; FY2028E PLN 17 × 11×; upstream scale + oil recovery)")
print(f"  XBULL scenario      : PLN {PRICE_XBULL}  (+83%; PLN 22 adj EPS × 12×; $100/bbl oil + full merger synergies)")
print(f"  Forward P/E (FY26E) : {CURRENT_PRICE/EPS_NOW:.1f}×  (PLN {CURRENT_PRICE} / PLN {EPS_NOW}; at upper end of energy range)")
print(f"  Forward P/E (FY27E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (FY2027E PLN {CONS_EPS_2YR}; = 10× = fair value multiple)")
print(f"  FY2025 EBITDA LIFO  : PLN 41.5B  (sector standard metric; +16% YoY; strong cash machine)")
print(f"  FY2025 adj EPS      : PLN {EPS_TROUGH}  (adj net income PLN 11.1B; GAAP was PLN 2.28 — distorted)")
print(f"  Dividend            : PLN 8.00/share (5.5% yield; proposed FY2025; record high; PLN 9.3B total)")
print(f"  Market cap          : ~PLN 167.9B  ({SHARES_M:.0f}M shares × PLN {CURRENT_PRICE}; ~$42B USD)")
print(f"  Analyst avg target  : PLN ~120-127  (9 analysts; 12-17% BELOW current; 'Neutral' consensus)")
print(f"  WATCHLIST entry     : PLN 105-115  (ratio_b ~1.5×; FY2027E at 7.5-8×)")
print(f"  ACCUMULATE entry    : PLN 90-100   (ratio_b ~0.75×; at analyst consensus zone)")
print(f"  BUY entry           : PLN 65-75    (below EPP; 52-wk low PLN 69.20 proved entry quality)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.85×  |  Idiosyncratic: 55%  |  Macro: 45%

  Driver                                                     Type    Wt  Note
  ────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  Oil/gas price & refining margin cycle                      MACRO   25%  PRIMARY: $10/bbl crude = ~PLN 1.5 adj EPS impact
  Polish government regulatory risk (fuel price caps)        IDIO    25%  HIGHEST risk: election year 2027; caps = –PLN 3-5B EBITDA
  Upstream production ramp (PGNiG Norway + domestic)        IDIO    20%  Growing volume + gas price recovery = key bull driver
  Dividend sustainability at PLN 8+/share                    IDIO    15%  80% adj payout ratio; vulnerable to oil price decline
  PLN/EUR/USD exchange rate                                  MACRO   10%  ~60% costs in PLN, crude in USD; PLN strength = margin
  Capex execution / net debt trajectory                      IDIO     5%  PLN 36B/yr capex; net debt rising; FCF ≈ zero""")

print(f"""
  II. SIGNAL FACTORS (SCA Cross-Reads)
  ----------------------------------------------------------------------
  Factor                                              Score   Weight  Contrib
  ─────────────────────────────────────────────────  ──────  ──────  ───────""")
for score, weight, label in SCA_FACTORS:
    contrib = score * weight
    print(f"  {label:<50}  {score:+.1f}    {weight:.2f}    {contrib:+.3f}")
print(f"  {'':─<50}  {'':─<6}  {'':─<6}  {'':─<7}")
print(f"  {'SCA raw':50}                  {sca_raw:+.3f}")
print(f"  {'SCA adj (÷2.0)':50}                  {sca_adj:+.3f}")

print(f"""
  III. COMPOSITE INFERENCE
  ----------------------------------------------------------------------
  Market composite  : {market_composite:.3f}  ({market_label})
  Adj composite     : {adj_composite:.3f}  ({adj_label})
  Softmax weights at adj composite ({adj_composite:.3f}):""")
for k, w in softmax_weights(adj_composite).items():
    prices = {"BEAR": PRICE_BEAR, "BASE": PRICE_BASE,
              "BULL": PRICE_BULL, "XBULL": PRICE_XBULL}
    print(f"    {k:<6}: {w:.1%}  (PLN {prices[k]})")
ep = expected_price(adj_composite)
print(f"  Expected price (adj): PLN {ep:.1f}  vs current PLN {CURRENT_PRICE}  (Δ {(ep - CURRENT_PRICE)/CURRENT_PRICE*100:+.1f}%)")

print(f"""
  IV. SCENARIOS SUMMARY
  ----------------------------------------------------------------------
  BEAR  (PLN {PRICE_BEAR})   : Oil crash (-40%); gov imposes fuel caps; adj EPS ~PLN 5; refineries
               mothballed; dividend cut; de-rating to 6×. –79% downside.

  BASE  (PLN {PRICE_BASE})  : FY2027E adj EPS PLN 14.48 × 10× = PLN 144.8. STOCK ALREADY THERE.
               Flat return over 2 years with dividend support (+5.5%/yr).
               Net 2-year return: ~+11% (dividends only). Not compelling.

  BULL  (PLN {PRICE_BULL})  : FY2028E adj EPS PLN 17 (oil $85/bbl, upstream +30%); 11× → PLN 187.
               +29% price + ~11% dividends over 2 years = ~+40% total. Better,
               but requires oil tailwind not in consensus.

  XBULL (PLN {PRICE_XBULL}) : Oil back to $100/bbl; upstream production doubled; merger synergies
               fully realised; adj EPS PLN 22 × 12× = PLN 264. +83% price gain.
               Probability: ~10%. Only captures the extreme bull.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-25")
print("=" * 72)
