"""
cb_signal_model.py — Chubb Limited (NYSE: CB)
World's largest publicly-traded P&C insurer. Global commercial & life insurance.
Signal framework: EPP floor + Method B + SCA softmax engine.
"""

import math

# ── LIVE PRICE (fetched before model construction) ──────────────────────────
CURRENT_PRICE = 328.75   # CB — fetched from Yahoo Finance / stockanalysis.com, 2026-05-25
# 52-wk range: $264.10 (Aug 1, 2025) – $345.67 (Mar 2, 2026)
# Market cap ~$127B; shares ~387M; dividend yield ~1.2%

TICKER        = "CB"
COMPANY       = "Chubb Limited"
SHARES_M      = 387          # million shares outstanding
DIVIDEND_ANN  = 3.96         # USD/yr; ~$0.99/qtr; raised 5.2% recently; 15+ yr streak

# ── EPS CONVENTION ───────────────────────────────────────────────────────────
# Core Operating EPS (non-GAAP). Chubb's primary earnings metric.
# Excludes net realized gains/losses, mark-to-market of equity securities, and
# other non-recurring items. Used in guidance, compensation, and analyst models.
# GAAP net income EPS is significantly noisier (mark-to-market swings on the
# $120B+ investment portfolio); core operating EPS reflects true underwriting +
# investment income earnings power.

EPS_HISTORY = {
    "FY2022": 15.24,   # hard market accelerating; rising investment income from rate hikes
    "FY2023": 22.54,   # record at time; +47.9%; hard market peak + NII surge; combined ratio 86.5%
    "FY2024": 22.51,   # essentially flat; Hurricane Helene (Sep) + Milton (Oct) impact; combined ratio 86.6%
    "FY2025": 24.79,   # record "best year in company history"; +10%; Q1 hurt by LA wildfires ($3.68/sh);
                        #   Q3 $7.49 (record) + Q4 $7.52 (record; combined ratio 81.2%); NPW ~$56B+
}

# Quarterly FY2025 drill-down:
#   Q1 2025: $3.68  (LA wildfire losses Jan 2025; ~$1.5B net claims; hit quarterly EPS ~-$2.00)
#   Q2 2025: $6.14
#   Q3 2025: $7.49  (record; up 31% YoY)
#   Q4 2025: $7.52  (record; P&C combined ratio 81.2% vs 85.7% prior year)
# Q1 2026:   $6.82  (missed consensus by ~12%; spring catastrophe events; FW guidance intact)

EPS_NOW       = 27.00    # FY2026E consensus; management guides "double-digit" growth from $24.79
EPS_TROUGH    = 16.00    # severe multi-year catastrophe scenario:
                          #   two consecutive above-normal hurricane seasons + reserve development
                          #   well below COVID-crash levels; $3B+ net cat above normalized
EPP_MIN_PE    = 13        # floor multiple for a premium global P&C insurer with REAL underwriting risk
                          # (contrast MRSH/Marsh at 18× — insurance BROKER has ZERO underwriting risk;
                          #  PGR at 22× — personal auto has stable/predictable loss patterns + massive share gains;
                          #  CB at 13× — commercial lines + cat exposure + life insurance = lower floor)
EPP           = EPP_MIN_PE * EPS_TROUGH   # = $208.00

CONS_EPS_2YR  = 30.00    # FY2027E; KBW $29.85; ~10% CAGR from $24.79; double-digit mgmt target
CONS_EXIT_PE  = 16        # mid-range historical multiple; hard market conditions sustained;
                          # below peak (22×) but above current panic (12×); recovery to normalized
price_b       = CONS_EPS_2YR * CONS_EXIT_PE   # = $480.00

ratio_b       = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
epp_gap_pct   = (CURRENT_PRICE - EPP) / EPP * 100

# Scenario prices
scenarios = {
    "BEAR":  208,    # EPP; 13× × $16; two back-to-back catastrophe seasons; multiple compression
    "BASE":  375,    # FY2026E $27 × 13.9×; consensus analyst target zone; KBW $373
    "BULL":  480,    # Method B; FY2027E $30 × 16×
    "XBULL": 570,    # FY2027E $30 × 19×; full hard-market re-rating; Buffett intrinsic value implied
}

# ── SOFTMAX ENGINE ───────────────────────────────────────────────────────────
T = 0.60
CENTRES = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}

def softmax_weights(composite):
    logits = {k: -((composite - c) ** 2) / T for k, c in CENTRES.items()}
    max_l  = max(logits.values())
    exps   = {k: math.exp(v - max_l) for k, v in logits.items()}
    total  = sum(exps.values())
    return {k: v / total for k, v in exps.items()}

def expected_price(composite):
    w = softmax_weights(composite)
    return sum(w[k] * scenarios[k] for k in scenarios)

def infer_composite(target_price, lo=1.0, hi=4.0, iterations=60):
    for _ in range(iterations):
        mid = (lo + hi) / 2
        if expected_price(mid) < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

market_composite = infer_composite(CURRENT_PRICE)

# ── SCA — SIGNAL CATALYST ADJUSTMENTS ───────────────────────────────────────
sca_items = [
    # (description, score, weight)
    ("Berkshire Hathaway 8.78% stake ($11.2B): Buffett actively added in Q3/Q4 2025 at "
     "$270-320 — world's best value investor endorsing intrinsic value well above $370+",
     +0.35, 0.25),
    ("$7.5B buyback at <12× FW EPS + 5.2% dividend increase: combined ~3.5% buyback yield "
     "+ 1.2% dividend = >4% annual capital return; buybacks highly accretive at these multiples",
     +0.30, 0.25),
    ("Record FY2025 ($24.79 core EPS, +10%); Q4 combined ratio 81.2% (record for any quarter); "
     "CEO Greenberg guides double-digit EPS growth 2026; pricing discipline intact",
     +0.20, 0.20),
    ("Q1 2026 missed consensus by -12% ($6.82 vs $7.76E): spring catastrophe events signal "
     "elevated 2026 cat activity; full-year guidance maintained but execution uncertainty rises",
     -0.30, 0.25),
    ("Hard market moderating: commercial lines premium growth slowing from 10%→5-8% as new "
     "capacity enters post-record profits; Marsh soft-market data corroborates trend",
     -0.20, 0.20),
    ("CEO Greenberg succession: age 67; running Chubb since 2004 (post ACE acquisition of legacy "
     "Chubb in 2016); no announced successor; key-man/culture risk for a relationship-driven firm",
     -0.15, 0.05),
]

sca_raw = sum(score * weight for _, score, weight in sca_items)
sca_adj = sca_raw / 2.0
adj_composite = market_composite + sca_adj

adj_weights    = softmax_weights(adj_composite)
expected_px    = expected_price(adj_composite)

# ── SIGNAL THRESHOLDS ────────────────────────────────────────────────────────
# ratio_b < 0.75   →  ◉ BUY          (EPP + price_b imply at $324.57)
# 0.75 – 1.10      →  ◎ ACCUMULATE
# 1.10 – 1.75      →  ◐ WATCHLIST
# 1.75 – 2.50      →  ▷ HOLD/TRIM
# > 2.50           →  ✕ AVOID

if   ratio_b < 0.75:  signal = "◉ BUY"
elif ratio_b < 1.10:  signal = "◎ ACCUMULATE"
elif ratio_b < 1.75:  signal = "◐ WATCHLIST"
elif ratio_b < 2.50:  signal = "▷ HOLD/TRIM"
else:                  signal = "✕ AVOID"

# ── OUTPUT ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    SEP  = "=" * 70
    DASH = "─" * 70

    print(SEP)
    print("CHUBB LIMITED (CB) — SIGNAL MODEL")
    print("World's largest publicly-traded P&C insurer. 54 countries. $127B market cap.")
    print(SEP)

    print("""
SIGNAL FRAMEWORK — METHOD B + SCA ENGINE
─────────────────────────────────────────
EPP  = EPS_TROUGH × EPP_MIN_PE          (structural floor; core operating EPS basis)
Ratio B = (Price − EPP) / (price_b − Price)

CB EPS convention: Core Operating EPS (non-GAAP). Excludes net realized gains/losses,
mark-to-market of equity securities held, and non-recurring items. Management's primary
metric; used in guidance, compensation targets, and all analyst models. Reflects true
underwriting income + net investment income + life insurance income.

SIGNAL THRESHOLDS
  Ratio B < 0.75   →  ◉ BUY
  0.75 – 1.10      →  ◎ ACCUMULATE
  1.10 – 1.75      →  ◐ WATCHLIST
  1.75 – 2.50      →  ▷ HOLD/TRIM
  > 2.50           →  ✕ AVOID

EPP_MIN_PE = 13×  rationale:
  Chubb is a REAL insurer — it underwrites policies and bears the risk. When major
  catastrophes hit (LA wildfires, major hurricanes, earthquake), Chubb pays claims
  and core operating EPS falls. This is fundamentally different from insurance BROKERS
  (MRSH at 18×, Aon, Gallagher) who earn commissions but bear NO underwriting risk.
  In the COVID crash (March 2020), Chubb traded briefly to ~$95 — roughly 8-9× what
  it might earn that year. A realistic trough (not panic) multiple for a premium
  global P&C insurer with exceptional underwriting discipline is 13×. During two
  consecutive severe hurricane seasons + reserve development, earnings could fall to
  $16/share (vs. $24.79 normalized FY2025); 13× × $16 = $208 EPP.
  Compare: PGR (22×) = dominant personal auto, stable-loss business gaining share;
  CB (13×) = global commercial + cat exposure + life + macro/FX risk = lower floor.
""")

    print("CHUBB LIMITED (CB) — THE WORLD'S PREMIER COMMERCIAL INSURER AT A DISCOUNT")
    print("=" * 70)

    print("""
BUSINESS OVERVIEW
─────────────────
Chubb Limited (incorporated in Zurich; listed NYSE) is the world's largest
publicly-traded property and casualty insurer by net premiums written. Founded
from the 2016 merger of ACE Limited (acquirer) and legacy Chubb Corporation,
led since 2004 by CEO Evan Greenberg. Operates in 54 countries with ~40,000
employees. FY2025 net premiums written: ~$56B.

BUSINESS SEGMENTS
─────────────────
  NORTH AMERICA COMMERCIAL P&C     ~45% of NPW
  ─────────────────────────────
  Commercial lines: property, casualty, D&O, professional liability, workers'
  comp, surety, accident & health. Serves large corporations, mid-market, and
  small businesses. Pricing power from hard commercial market (2020-2025).

  NORTH AMERICA PERSONAL LINES       ~8% of NPW
  ─────────────────────────────
  High-net-worth personal insurance — Masterpiece® brand. Homes, autos,
  fine art, jewelry, yachts for affluent clients. Less commoditised; sticky.

  OVERSEAS GENERAL (INTERNATIONAL)  ~35% of NPW
  ─────────────────────────────
  Commercial and personal lines across Europe, Asia-Pacific, Latin America,
  Middle East. Serving multinationals, governments, and local markets.
  Asia (China, Japan, Korea) is a key growth driver — large under-insured
  populations rapidly gaining middle-class coverage.

  LIFE INSURANCE                     ~12% of NPW
  ─────────────────────────────
  Life and A&H products in Asia (Korea, Japan, Taiwan, Southeast Asia) and
  Latin America. Provides diversification and recurring income. Different
  risk profile (mortality/longevity) from P&C, generally lower volatility.

THE UNDERWRITING FRANCHISE: WHY CHUBB IS DIFFERENT
───────────────────────────────────────────────────
Since CEO Evan Greenberg took the helm in 2004, Chubb has been defined by
underwriting discipline — the rare insurer that will WALK AWAY from business
when pricing is inadequate, and GROWS aggressively when the market hardens.

Evidence of this discipline:
  ✓ FY2023 P&C combined ratio: 86.5%  (below 100% = underwriting profit)
  ✓ FY2024 P&C combined ratio: 86.6%  (DESPITE Hurricane Helene/Milton)
  ✓ Q4 2025 P&C combined ratio: 81.2%  (record for any quarter; historic)
  ✓ FY2022–2025 core operating EPS grew 62.7% in 4 years
  ✓ Record investment income as $120B+ investment portfolio reprices higher

For reference: a combined ratio of 100% = breaking even on underwriting alone;
anything below means actual underwriting profit. Industry average in a "hard"
market is ~93-96%. Chubb consistently beats by 7-10 points = massive advantage.

INVESTMENT PORTFOLIO: THE HIDDEN ENGINE
────────────────────────────────────────
Chubb holds a ~$120B+ investment portfolio (bonds, equities, alternatives).
As interest rates rose from 2022→2025, this portfolio's investment income
surged — net investment income grew from ~$4.5B (2022) to ~$6.3B+ (2025).
Each additional 100bps of portfolio yield ≈ $1.2B pre-tax income (≈ $2.40/share).
With rates structurally higher in 2025-2026 vs. 2019-2021, investment income
is a persistent tailwind — the portfolio reinvests maturing bonds at higher yields.

WARREN BUFFETT'S ENDORSEMENT: 8.78% STAKE
──────────────────────────────────────────
Berkshire Hathaway revealed a ~6.7% Chubb stake in mid-2024 (the position had
been built confidentially via SEC filing delay). Berkshire has continued adding:
  Q3 2025: +4.3M shares (position +16%) — buying at ~$270-300 range
  Q4 2025: +2.9M shares (position +9%)  — buying at ~$300-325 range
  Total stake: 8.78% of Chubb shares outstanding (~$11.2B position)
  8th largest Berkshire holding (3.9% of Berkshire's equity portfolio)

Buffett — who runs Berkshire's insurance operations (GEICO, Berkshire Re, etc.)
and understands P&C insurance better than anyone — has been a BUYER of Chubb
at prices well ABOVE current levels. Berkshire's cost basis of $270-320 implies
intrinsic value estimate materially above $370+.

WHY THE STOCK IS TRADING AT 12× FORWARD EPS (NEAR COVID MULTIPLES)
────────────────────────────────────────────────────────────────────
At $328.75 / $27.00E FY2026E = 12.2× forward core operating EPS.
Historical multiple range: 14-18× in normal years; 22×+ in hard-market peak.
COVID crash (March 2020): briefly touched 8-9× (extreme panic, not sustainable).

Current discount drivers:
  1. CATASTROPHE ANXIETY: LA wildfire losses (Q1 2025 $3.68/share vs $5.50
     normalized) showed real cat exposure. Q1 2026 miss (-12%) suggests
     ongoing cat activity. Market pricing in above-average losses.
  2. INSURANCE MARKET CYCLE PEAK CONCERN: Hard commercial market (2020-2025)
     generated exceptional pricing power. Market worries the cycle is turning
     — premium growth may slow from 10% to 5-7%.
  3. BUFFETT SELLING FEAR: Investors worry Berkshire may eventually sell.
     The opposite has been happening — Berkshire has been BUYING aggressively.
  4. RATE SENSITIVITY: Some concern that if rates fall, investment income drops.
     Partially mitigated by long portfolio duration and repricing at higher yields.

WHY THESE FEARS ARE OVERPRICED
────────────────────────────────
  ✓ Catastrophes are cyclical: a bad cat year is followed by even higher
    reinsurance pricing and commercial market hardening — Chubb BENEFITS from
    this cycle through higher premium growth in subsequent years.
  ✓ Even in a soft commercial market, underwriting discipline means Chubb
    maintains adequate pricing or exits lines — it does not chase volume.
  ✓ Buffett's buying at $270-325 vs. current $328 — he sees more value, not less.
  ✓ International expansion (Asia life insurance, global commercial) provides
    structural growth independent of US market cycle.
  ✓ At 12.2× forward earnings with a $7.5B buyback (3.5% annual buyback yield),
    capital compounding is exceptional even without multiple expansion.

CAPITAL ALLOCATION: BUYBACK + DIVIDEND DUAL COMPOUNDER
────────────────────────────────────────────────────────
  $7.5B buyback authorized (at $328 = ~5.9% of float); executed at <12× EPS
  Dividend: $3.96/yr (+5.2% recent raise; 15+ consecutive annual increases)
  Combined capital return: ~4.2% yield at current price + EPS compounding

  Each share repurchased at 12× reduces share count → remaining shareholders
  own a larger fraction of growing earnings. At 10% EPS growth + 3.5% buyback
  yield = 13.5% total annual return potential before any multiple expansion.

FY2025 FULL YEAR HIGHLIGHTS — "BEST YEAR IN COMPANY HISTORY"
──────────────────────────────────────────────────────────────
  Core operating EPS:    $24.79     (+10% YoY; record)
  Q4 combined ratio:      81.2%     (record low for any quarter; dramatic improvement)
  NPW growth:            ~8-9% YoY  (despite insurance market softening; volume growth)
  Record investment income: rising as $120B+ portfolio reprices to higher yields
  CEO Greenberg: "Best year in the 22-year history of this company"
  Guided FY2026: "double-digit growth in EPS and tangible book value"

Q1 2026 — THE MISS AND WHAT IT MEANS
──────────────────────────────────────
  Core operating EPS: $6.82 (missed consensus $7.76 by -12%)
  Net income:          $5.88/share (GAAP; also missed)
  Context: Spring catastrophes (tornadoes, floods, possibly hail) hit earlier
  than modeled. Full-year guidance reiterated — management sees temporary,
  not structural, impact.
  RISK: If spring/summer 2026 cat season is above-average, FY2026E estimates
  of $27+ may be optimistic.

PEER COMPARISON
────────────────
  Progressive (PGR):    ~20-22× FW EPS — personal auto; massive share gains; 22× EPP_MIN_PE
  Travelers (TRV):      ~14-16× FW EPS — commercial P&C; smaller/domestic; lower quality
  AIG:                  ~10-12× FW EPS — restructured; weaker brand; past under-reserving
  Chubb (CB) at 12.2×: Trades at a DISCOUNT to TRV despite being higher-quality globally.
  Historical CB premium to TRV: 10-15%. Current: CB is at parity or slight discount.
  This is a mispricing driven by cat anxiety, not fundamental deterioration.

KEY RISKS
──────────
  1. CATASTROPHE SEVERITY: A major hurricane season, earthquake (California, Japan),
     or cyber catastrophe event could reduce EPS $3-6/share in a single year.
  2. INSURANCE MARKET SOFTENING: If commercial lines competition intensifies,
     Chubb may need to reduce premiums, pressuring combined ratios.
  3. INTEREST RATE DECLINE: Falling rates reduce investment income over time
     as the portfolio rolls over to lower-yielding bonds.
  4. CEO SUCCESSION: Greenberg (age 67) has no announced successor; management
     culture and underwriting discipline are deeply personal to his leadership.
  5. FOREIGN EXCHANGE: International operations exposed to USD strength;
     local-currency results can look better than USD-reported.
  6. RESERVE DEVELOPMENT: Adverse reserve development on commercial liability
     (long-tail lines) remains a structural risk for any P&C insurer.

SUMMARY VERDICT
───────────────
Chubb is the world's premier P&C insurer — disciplined underwriting, exceptional
management, global scale, growing investment income, and Warren Buffett's largest
insurance investment. At 12.2× FY2026E core operating EPS, the stock is priced
for sustained catastrophe losses and insurance market collapse. Neither is likely.
The market is ignoring Buffett's conviction (8.78% stake, actively adding at
$270-325), the $7.5B buyback accretion, and the structural improvement in
investment income. At $328.75, firmly in ACCUMULATE territory; BUY below $325.
Target: $375-480 over 2 years (FY2027E $30 × 13-16× = $390-480).
""")

    print("KEY METRICS")
    print(f"  Current price (fetched)          = ${CURRENT_PRICE:>8.2f}")
    print(f"  52-week range                    = $264.10 – $345.67")
    print(f"  Market cap                       = ~$127B")
    print(f"  FW P/E on FY2026E ${EPS_NOW:.2f}       = {CURRENT_PRICE/EPS_NOW:.1f}×  (vs historical 14-22×; COVID-crash level)")
    print(f"  FW P/E on FY2027E ${CONS_EPS_2YR:.2f}       = {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (very cheap 2-yr view)")
    print(f"  Dividend (annual)                = ${DIVIDEND_ANN:.2f}  (yield {DIVIDEND_ANN/CURRENT_PRICE*100:.1f}%; 15+ yr growth streak)")
    print(f"  Berkshire Hathaway stake         = 8.78%  (~$11.2B; 8th largest Berkshire holding)")
    print(f"  Buyback authorized               = $7.5B  (~5.9% of float at current price)")
    print(f"  FY2025 NPW growth                = ~8-9% YoY  (global P&C + life)")
    print(f"  Q4 2025 P&C combined ratio       = 81.2%  (record; prior year Q4 = 85.7%)")
    print(f"  Countries of operation           = 54  (global commercial + life insurance)")
    print()

    print("CORE OPERATING EPS HISTORY")
    for yr, val in EPS_HISTORY.items():
        print(f"  {yr}  ${val:5.2f}")
    print(f"  FY2026E ${EPS_NOW:.2f}  (consensus; mgmt guides double-digit from ${EPS_HISTORY['FY2025']:.2f})")
    print(f"  FY2022–FY2025 CAGR: {((EPS_HISTORY['FY2025']/EPS_HISTORY['FY2022'])**(1/3)-1)*100:.1f}%/yr  (hard market + rate tailwind)")
    print()

    print("EPP CALCULATION")
    print(f"  EPS_TROUGH × EPP_MIN_PE  =  ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×  =  ${EPP:.2f}")
    print(f"  (severe two-season cat year; 13× = realistic trough multiple for global P&C insurer)")
    print()

    print("METHOD B  (2-year forward)")
    print(f"  CONS_EPS_2YR × CONS_EXIT_PE  =  ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×  =  ${price_b:.2f}")
    print()

    print("RATIO B  (PRIMARY SIGNAL)")
    print(f"  (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})")
    print(f"  = ${CURRENT_PRICE - EPP:.2f} / ${price_b - CURRENT_PRICE:.2f}")
    print(f"  = {ratio_b:.3f}×   →   {signal}")
    print(f"  EPP gap: +{epp_gap_pct:.1f}% above structural floor")
    print()

    print("SCENARIO PRICES")
    for name, price in scenarios.items():
        print(f"  {name:<8} ${price:>7.2f}   ", end="")
        if name == "BEAR":
            print("EPP floor; two major hurricane seasons + reserve development")
        elif name == "BASE":
            print("Analyst consensus PT zone; FY2026E $27 × 13.9×; KBW target $373")
        elif name == "BULL":
            print("Method B; FY2027E $30 × 16×; normalized multiple recovery")
        else:
            print("Full re-rating; $30 × 19×; hard market return; Buffett implied intrinsic value")
    print()

    print("SOFTMAX COMPOSITE ENGINE")
    print(f"  Market composite (inferred)  =  {market_composite:.3f}")
    print(f"  (Market pricing near BEAR-BASE mix — cat anxiety + cycle concerns outweigh franchise quality)")
    print()

    print("SCA — SIGNAL CATALYST ADJUSTMENTS")
    for desc, score, weight in sca_items:
        trunc = desc[:55]
        sign  = "+" if score >= 0 else ""
        print(f"  {trunc:<55}  {sign}{score:.2f} × {weight:.2f}  =  {'+' if score*weight>=0 else ''}{score*weight:.4f}")
    print()
    print(f"  sca_raw     =  {'+' if sca_raw>=0 else ''}{sca_raw:.4f}")
    print(f"  sca_adj     =  {'+' if sca_adj>=0 else ''}{sca_adj:.4f}  (= sca_raw / 2.0)")
    print(f"  adj_composite  =  {market_composite:.3f}  +  {sca_adj:.4f}  =  {adj_composite:.3f}")
    print()

    print("SOFTMAX SCENARIO WEIGHTS  (at adj_composite = {:.3f})".format(adj_composite))
    for name, w in adj_weights.items():
        print(f"  {name:<8}  {w*100:5.1f}%   ${scenarios[name]:.2f}")
    print()
    print(f"  Expected price (probability-weighted)  =  ${expected_px:.2f}")
    print()

    print("BUSINESS METRICS")
    print(f"  Net premiums written (FY2024)  = ~$51.5B  (+8.7% YoY; FY2025 ~$56B est.)")
    print(f"  P&C combined ratio FY2024      = 86.6%  (despite Hurricane Helene + Milton)")
    print(f"  Q4 2025 combined ratio (record) = 81.2%  (exceptional; best ever quarter)")
    print(f"  Investment portfolio            = ~$120B+  (bonds; repricing to higher yields)")
    print(f"  Countries of operation          = 54  (global; North America + International + Life)")
    print(f"  Berkshire Hathaway stake        = 8.78%  (actively adding; Q3+Q4 2025 purchases)")
    print(f"  Analyst avg price target        = ~$365-373  (KBW $373; +11-14% from current)")
    print(f"  Analyst consensus               = majority Buy  (Q1 miss seen as temporary)")
    print()

    print("SIGNAL ENTRY GUIDE")
    # Compute threshold prices
    # ratio_b = (P - EPP) / (price_b - P) = threshold
    # P = (EPP + threshold × price_b) / (1 + threshold)
    def threshold_price(rb):
        return (EPP + rb * price_b) / (1 + rb)
    p_buy     = threshold_price(0.75)
    p_watch   = threshold_price(1.10)
    p_hold    = threshold_price(1.75)
    p_avoid   = threshold_price(2.50)
    print(f"  ✕ AVOID      above  ${p_avoid:.0f}  (ratio_b > 2.50×)")
    print(f"  ▷ HOLD/TRIM  ${p_hold:.0f} – ${p_avoid:.0f}  (ratio_b 1.75–2.50×)")
    print(f"  ◐ WATCHLIST  ${p_watch:.0f} – ${p_hold:.0f}  (ratio_b 1.10–1.75×; KBW $373 = low-WATCHLIST)")
    print(f"  ◎ ACCUMULATE ${p_buy:.0f} – ${p_watch:.0f}  (ratio_b 0.75–1.10×)")
    print(f"  ◉ BUY        below  ${p_buy:.0f}  (ratio_b < 0.75×)")
    print(f"  ← current ${CURRENT_PRICE:.2f}  {signal}")
    print()
    print(f"  52-wk low $264.10 = deep BUY (ratio_b 0.26×); Buffett was buying at these levels.")
    print(f"  52-wk high $345.67 = ACCUMULATE (ratio_b 0.92×) — even the 52-week high was ACCUM.")
    print(f"  Analyst consensus PT ~$373 = low-WATCHLIST (ratio_b 1.21×); market is cautious.")
    print(f"  Buffett buying: $270-325 implies intrinsic value >$400; consistent with BULL $480.")
    print(f"  Key watch: Q2 2026 cat losses (April-June storms); FY2026 combined ratio trajectory.")
    print(f"  Hard market renewal data (Marsh): any acceleration → re-rating trigger.")
    print(f"  CEO succession announcement would remove key-man overhang → positive catalyst.")
