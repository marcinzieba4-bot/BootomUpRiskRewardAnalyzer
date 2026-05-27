"""
MARSH & MCLENNAN COMPANIES, INC. (MRSH) — Bottom-Up Risk/Reward Signal Model
==============================================================================
Ticker changed from MMC → MRSH on January 14, 2026 (company rebranded to "Marsh")
Part 1: Framework & Methodology
Part 2: Analyst Commentary & Investment Thesis
Part 3: Numbers & Signal Output
"""

# ── PART 1: FRAMEWORK ────────────────────────────────────────────────────────

FRAMEWORK = """
SIGNAL FRAMEWORK — METHOD B + SCA ENGINE
─────────────────────────────────────────
EPP  = EPS_TROUGH × EPP_MIN_PE          (structural floor; adjusted EPS basis)
Ratio B = (Price − EPP) / (price_b − Price)

MRSH EPS convention: Adjusted EPS (non-GAAP). Excludes amortisation of
acquired intangibles, restructuring costs, and other non-recurring items.
Management's primary earnings metric; used in compensation and guidance.

SIGNAL THRESHOLDS
  Ratio B < 0.75   →  ◉ BUY
  0.75 – 1.10      →  ◎ ACCUMULATE
  1.10 – 1.75      →  ◐ WATCHLIST
  1.75 – 2.50      →  ▷ HOLD/TRIM
  > 2.50           →  ✕ AVOID

EPP_MIN_PE = 18×  rationale:
  Marsh McLennan is an insurance broker and professional services firm — it
  has NO underwriting risk (pure fee/commission model; insurers bear the risk,
  not Marsh). This capital-light model with $4B+ annual FCF deserves a premium
  floor multiple. During the COVID crash (2020), MRSH/MMC never traded below
  ~18× adj EPS. 18× × $7.00 conservative trough = $126 EPP. Comparable
  insurance brokers (Aon, Gallagher) floor at similar multiples.
"""

# ── PART 2: ANALYST COMMENTARY ───────────────────────────────────────────────

COMMENTARY = """
MARSH & MCLENNAN (MRSH) — THE UNDERVALUED COMPOUNDER: 19 YEARS OF MARGIN GROWTH
══════════════════════════════════════════════════════════════════════════════════

BUSINESS OVERVIEW
─────────────────
Marsh & McLennan (rebranded from MMC to "Marsh" in Jan 2026) is the world's
leading professional services firm for risk, strategy, and people. Revenue of
$27B (FY2025) across four iconic businesses in 130+ countries:

  RISK & INSURANCE SERVICES   ~$18B revenue  (~67% of total)
  ─────────────────────────
  Marsh             World's #1 insurance broker. Advises and places
                    commercial insurance for corporations, governments, and
                    individuals. Revenue = brokerage commissions (~1-2% of
                    premiums placed). Does NOT underwrite risk.
                    Q1 2026 underlying revenue: +4%

  Guy Carpenter     World's #2 reinsurance broker. Helps insurance companies
                    transfer their own risk to the global reinsurance market.
                    Deep relationships with every major reinsurer globally.
                    Q1 2026: +2% underlying

  CONSULTING                  ~$9B revenue   (~33% of total)
  ─────────────────────────
  Mercer            World's #1 HR and workforce consulting firm. Benefits
                    design, investment consulting for pensions, workforce
                    strategy, pay benchmarking. $16T+ in assets advised.
                    Q1 2026 underlying: +5%

  Oliver Wyman      Elite global management consulting (ranked with McKinsey/
                    BCG for financial services, retail, transport, health).
                    Known for rigor and senior-level access.
                    Q1 2026: +6%

THE DEFINING FRANCHISE CHARACTERISTIC: 18 CONSECUTIVE YEARS OF MARGIN EXPANSION
──────────────────────────────────────────────────────────────────────────────────
Since 2007, Marsh McLennan has expanded its adjusted operating margin EVERY
SINGLE YEAR. This is not an accident — it reflects:

  1. PRICING POWER: Insurance brokers earn % of premium. As global commercial
     insurance premiums rise (hard market, catastrophe losses, inflation), so
     do Marsh's revenues without corresponding cost increases.

  2. SCALE ADVANTAGE: $27B revenue platform means incremental revenue falls
     through at very high margins; fixed cost base is largely covered.

  3. ACQUISITION INTEGRATION: Each acquisition (JLT in 2019, smaller bolt-ons)
     gets integrated into the Marsh platform at higher margins. Synergies are
     structural, not one-time.

  4. TECHNOLOGY ENABLEMENT: Digital platforms reduce labour intensity of
     placement/broking. Oliver Wyman + Mercer use proprietary data/analytics
     that competitors cannot easily replicate.

2026 is expected to be the 19th consecutive year of reported margin expansion
per management guidance.

Q1 2026 RESULTS
────────────────
  Total revenue:         $7.6B  (+8% total; +4% underlying)
  Adjusted EPS:          $3.29  (+8% YoY)
  Risk & Insurance:      $5.1B  (+6% total; +3% underlying; adj margin 38.3%)
  Consulting:            $2.6B  (+11% total; +5% underlying; adj margin 21.6%)

  Company expects full-year 2026 underlying revenue growth "similar to last
  year" (FY2025 was ~4%), and continued margin expansion (the 19th year).

FY2025 FULL YEAR RESULTS
─────────────────────────
  Revenue:              $27.0B  (+10% total; +4% underlying)
  Adj operating income: $7.3B   (+11% YoY)
  Adj EPS:              $9.75   (+9% YoY; 18th consecutive margin expansion)
  Free cash flow:       ~$4.5B+ (~17% FCF margin; capital-light)
  Dividend:             $3.48/yr ($0.87/quarter; raised annually for 15+ years)

THE VALUATION DISLOCATION: 30% BELOW ATH AT 15.5× FW EPS
────────────────────────────────────────────────────────────
At $164.11:
  FW P/E on FY2026E $10.60:   15.5×  (vs historical avg 22-28×; near COVID low)
  FW P/E on FY2027E $11.60:   14.1×  (extremely cheap on 2-year view)
  Dividend yield:              2.1%   ($3.48 / $164.11)
  FCF yield:                  ~2.7%  ($4.5B / $79B market cap)
  52-wk high:                 $235.78 (stock -31% from high)

For context, MRSH's typical valuation range:
  2019-2021 bull run:     25-30× adj EPS
  Post-COVID normalise:   22-26× adj EPS
  Current (May 2026):     15.5× adj EPS = near COVID-crash floor

Why the re-rating?
  1. Insurance market cycle concern: "hard market" (rising commercial premiums
     of 2020-2023) may be softening; Marsh revenue % tied to premium levels.
  2. Higher discount rates reducing P/E multiples broadly across growth stocks.
  3. Oliver Wyman slowing: consulting demand tied to corporate confidence, which
     is softer in 2026 tariff/uncertainty environment.
  4. M&A market slowdown: Marsh earns fees on transaction insurance; deal
     volumes have been slower.

WHY THE RE-RATING IS EXCESSIVE
────────────────────────────────
Even in a "soft" insurance market:
  ✓ Renewal commissions on existing policies continue regardless of premium
    direction (contracts multi-year; switch costs very high)
  ✓ Insurance penetration is still GROWING globally (EM expansion, cyber risk,
    climate risk, supply chain risk — all new premium categories Marsh benefits from)
  ✓ Mercer and Oliver Wyman are benefiting from AI transformation consulting —
    the same uncertainty driving corporate caution INCREASES demand for strategy
    consulting and workforce redesign help
  ✓ EPS growth 8-9% YoY persisting despite headwinds (Q1 2026: +8%)

CAPITAL ALLOCATION: DIVIDEND + BUYBACKS
─────────────────────────────────────────
  Annual dividend:    $3.48/yr  (+annual increases for 15+ years; ~7% growth)
  FCF (~$4.5B):       Funds ~$1.7B dividends + ~$2B+ buybacks + M&A bolt-ons
  Shares outstanding: ~483M → declining at ~1-2%/year via buybacks

  At $164, Marsh is repurchasing stock at the lowest multiple in 15 years —
  the buyback is enormously value-accretive.

PEER COMPARISON
────────────────
  Aon (AON):          ~23-24× FW adj EPS — the primary insurance broker peer
  Gallagher (AJG):    ~30-35× FW adj EPS — premium for organic growth focus
  MRSH at 15.5×:      ~30% discount to Aon; ~50% discount to Gallagher
                       despite comparable or superior business quality metrics

KEY RISKS
──────────
  1. INSURANCE MARKET CYCLE: Softer commercial market → lower premiums →
     lower brokerage commissions. Some exposure, but mitigated by volume growth.
  2. CONSULTING SLOWDOWN: Corporate capex caution slows Oliver Wyman/Mercer.
     Most visible risk given macro uncertainty.
  3. CATASTROPHE YEAR: Major catastrophe year (hurricanes, earthquakes) reduces
     reinsurance capacity, compresses Guy Carpenter margins temporarily.
  4. COMPETITION: Aon and Gallagher competing for talent and acquisitions;
     PE-backed brokers competing for mid-market clients.
  5. INTEREST RATE: Lower fiduciary interest income as rates decline (mitigated
     by volume growth in assets under advisory at Mercer).

SUMMARY VERDICT
───────────────
Marsh McLennan has delivered 18 consecutive years of margin expansion,
maintains a capital-light model with no underwriting risk, generates $4.5B
free cash flow annually, and is compounding EPS at 8-10% with high consistency.
At 15.5× FY2026E earnings — near COVID-crash multiples — the market is pricing
this premium compounder as if its franchise has been impaired. It has not.
The insurance broking moat is structural; the consulting businesses are growing.
At $164, firmly in BUY territory. Target: $200-267 over 2 years.
"""

# ── PART 3: NUMBERS & SIGNAL ─────────────────────────────────────────────────

import math

# ── Live price (MANDATORY — fetched from internet) ──
CURRENT_PRICE = 164.11   # MRSH — search results, 2026-05-27 (last close May 25)

PRICE_52W_LOW  = 158.16
PRICE_52W_HIGH = 235.78

SHARES_M     = 483.0    # Approx. shares outstanding ($79.28B mktcap / $164.11 = 483M)
DIVIDEND_ANN = 3.48     # $0.87/quarter; 15+ consecutive annual increases; yield 2.1%

# ── Adjusted EPS history ──
EPS_HISTORY = {
    "FY2022": 6.85,   # +11% YoY; hard insurance market accelerating
    "FY2023": 8.00,   # Derived: FY2024 $8.80 was +10% above FY2023
    "FY2024": 8.80,   # +10% YoY; JLT synergies fully realised; 17th margin expansion year
    "FY2025": 9.75,   # +9% YoY; record; $27B revenue; 18th consecutive margin expansion year
}
#  Compound annual growth FY2022-FY2025: ($9.75/$6.85)^(1/3) - 1 = 12.5%/yr
#  Remarkably consistent; no year of EPS decline in the modern era

EPS_NOW    = 10.60   # FY2026E adj EPS consensus (range $9.95-$11.05); Q1A $3.29 (+8%)
EPS_TROUGH = 7.00    # Conservative floor: insurance soft market + consulting recession;
                     # BELOW FY2024 actual ($8.80); unprecedented for this business

EPP_MIN_PE = 18      # Capital-light insurance broker; no underwriting risk; COVID floor ~18×;
                     # premium to banks (9×); reflects structural quality of fee model
EPP        = EPP_MIN_PE * EPS_TROUGH   # = 126.00

# ── Method B: 2-year forward (FY2027E) ──
CONS_EPS_2YR  = 11.60   # FY2027E adj EPS; ~9% growth from FY2026E; 19th margin expansion yr
CONS_EXIT_PE  = 23      # Premium professional services/broker; below ATH peak (28×) but above
                         # current floor (15×); reflects confidence in growth restoration
price_b       = CONS_EPS_2YR * CONS_EXIT_PE   # = 266.80

ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)

# ── Segment metrics ──
REV_FY2025_B           = 27.0    # FY2025 total revenue ($B; +10% YoY)
ADJ_OP_INC_FY2025_B    = 7.3     # FY2025 adj operating income ($B; +11% YoY)
FCF_FY2024_B           = 4.0     # FY2024 free cash flow ($B; 16% of revenue)
MARGIN_EXPANSION_YEARS = 18      # Consecutive years of reported margin expansion (thru FY2025)
RIS_MARGIN_Q1          = 38.3    # Risk & Insurance Services adj op margin Q1 2026 (%)
CONSULTING_MARGIN_Q1   = 21.6    # Consulting adj op margin Q1 2026 (%)

# ── Softmax composite engine ──
def softmax_weights(composite, T=0.60):
    centres = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
    logits  = {k: -((composite - v) ** 2) / T for k, v in centres.items()}
    m       = max(logits.values())
    exps    = {k: math.exp(v - m) for k, v in logits.items()}
    s       = sum(exps.values())
    return   {k: v / s for k, v in exps.items()}

scenarios = {
    "BEAR":  126.00,   # EPP floor; severe insurance soft market + consulting recession
    "BASE":  200.00,   # Analyst zone; FY2026E $10.60 × ~19×; soft market, margins hold
    "BULL":  267.00,   # Method B; FY2027E $11.60 × 23×; full re-rating resumes
    "XBULL": 340.00,   # Peak cycle; FY2028E $13.00 × 26×; hard market returns + margin acc
}

def infer_composite(price, lo=1.0, hi=4.0, iters=60):
    for _ in range(iters):
        mid     = (lo + hi) / 2
        weights = softmax_weights(mid)
        ep      = sum(weights[k] * scenarios[k] for k in scenarios)
        if ep < price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

market_composite = infer_composite(CURRENT_PRICE)

# ── SCA: Signal Catalyst Adjustments ──
sca_factors_clean = [
    # (description,                                                    raw,   weight)
    ("18 consecutive years margin expansion; structural quality unmatched",  +0.35, 0.25),
    ("Capital-light; no underwriting risk; $4.5B FCF; buying back at 15×",  +0.25, 0.20),
    ("30% below ATH at 15.5× FW EPS — COVID-level multiple on non-COVID biz",+0.30, 0.20),
    ("Insurance soft market cycle risk: premiums softening → lower commis",  -0.25, 0.25),
    ("Oliver Wyman/Mercer consulting: corporate caution slows demand",        -0.15, 0.20),
    ("Near 52-wk low; limited near-term downside catalyst to drive shares",  -0.10, 0.10),
]

sca_raw = sum(r * w for _, r, w in sca_factors_clean)
sca_adj = sca_raw / 2.0
adj_composite = market_composite + sca_adj

weights      = softmax_weights(adj_composite)
exp_price    = sum(weights[k] * scenarios[k] for k in scenarios)
epp_gap_pct  = (CURRENT_PRICE - EPP) / EPP * 100

# ── Signal classification ──
if   ratio_b < 0.75:  signal = "◉ BUY"
elif ratio_b < 1.10:  signal = "◎ ACCUMULATE"
elif ratio_b < 1.75:  signal = "◐ WATCHLIST"
elif ratio_b < 2.50:  signal = "▷ HOLD/TRIM"
else:                 signal = "✕ AVOID"

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 70)
    print("MARSH & MCLENNAN COMPANIES, INC. (MRSH) — SIGNAL MODEL")
    print("(ticker changed from MMC → MRSH on January 14, 2026)")
    print("=" * 70)

    print(FRAMEWORK)
    print(COMMENTARY)

    print("KEY METRICS")
    print(f"  Current price (fetched)      = ${CURRENT_PRICE:>8.2f}")
    print(f"  52-week range                = ${PRICE_52W_LOW:.2f} – ${PRICE_52W_HIGH:.2f}")
    print(f"  Market cap                   = ${CURRENT_PRICE * SHARES_M / 1000:.1f}B")
    print(f"  FW P/E on FY2026E $10.60     = {CURRENT_PRICE/EPS_NOW:.1f}×  (vs historical 22-28×)")
    print(f"  FW P/E on FY2027E $11.60     = {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (very cheap 2-yr view)")
    print(f"  Dividend (annual)            = ${DIVIDEND_ANN:.2f}  (yield {DIVIDEND_ANN/CURRENT_PRICE*100:.1f}%;  15+ yr growth streak)")
    print(f"  Revenue FY2025               = ${REV_FY2025_B:.0f}B  (+10% YoY; 130+ countries)")
    print(f"  Adj op income FY2025         = ${ADJ_OP_INC_FY2025_B:.1f}B  (+11% YoY)")
    print(f"  FCF FY2024                   = ${FCF_FY2024_B:.0f}B  (~16% FCF margin; capital-light)")
    print(f"  Consecutive margin expansion = {MARGIN_EXPANSION_YEARS} years  (targeting 19th in 2026)")

    print("\nADJUSTED EPS HISTORY")
    for yr, eps in EPS_HISTORY.items():
        yoy = ""
        if yr == "FY2025": yoy = "  ← 18th consecutive margin expansion; $27B revenue record"
        print(f"  {yr}  ${eps:>5.2f}{yoy}")
    print(f"  FY2026E ${EPS_NOW:.2f}  (consensus $9.95–$11.05; Q1A $3.29 +8% YoY)")
    print(f"  FY2022–FY2025 CAGR: {((EPS_HISTORY['FY2025']/EPS_HISTORY['FY2022'])**(1/3)-1)*100:.1f}%/yr  (highly consistent compounding)")

    print(f"\nEPP CALCULATION")
    print(f"  EPS_TROUGH × EPP_MIN_PE  =  ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×  =  ${EPP:.2f}")
    print(f"  (COVID crash low ~18× adj EPS; no underwriting risk = premium floor)")

    print(f"\nMETHOD B  (2-year forward)")
    print(f"  CONS_EPS_2YR × CONS_EXIT_PE  =  ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×  =  ${price_b:.2f}")

    print(f"\nRATIO B  (PRIMARY SIGNAL)")
    print(f"  (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})")
    print(f"  = ${CURRENT_PRICE - EPP:.2f} / ${price_b - CURRENT_PRICE:.2f}")
    print(f"  = {ratio_b:.3f}×   →   {signal}")
    print(f"  EPP gap: +{epp_gap_pct:.1f}% above structural floor")

    print(f"\nSCENARIO PRICES")
    for k, v in scenarios.items():
        print(f"  {k:<7}  $ {v:>7.2f}   ", end="")
        if k == "BEAR":  print("EPP floor; severe soft market + consulting recession + multiple compression")
        if k == "BASE":  print("Analyst zone; FY2026E $10.60 × ~19×; growth continues at current rate")
        if k == "BULL":  print("Method B; FY2027E $11.60 × 23×; multiple re-rating toward historical norm")
        if k == "XBULL": print("Peak cycle; $13 × 26×; hard market returns; AI consulting boom; full re-rate")

    print(f"\nSOFTMAX COMPOSITE ENGINE")
    print(f"  Market composite (inferred)  =  {market_composite:.3f}")
    print(f"  (Market pricing near BEAR-BASE mix — pricing cycle risk, ignoring franchise quality)")

    print(f"\nSCA — SIGNAL CATALYST ADJUSTMENTS")
    for desc, raw, w in sca_factors_clean:
        contrib = raw * w
        sign = "+" if contrib >= 0 else ""
        print(f"  {desc[:52]:<52}  {sign}{raw:.2f} × {w:.2f}  =  {sign}{contrib:.4f}")
    print(f"\n  sca_raw     =  {sca_raw:+.4f}")
    print(f"  sca_adj     =  {sca_adj:+.4f}  (= sca_raw / 2.0)")
    print(f"  adj_composite  =  {market_composite:.3f}  +  {sca_adj:.4f}  =  {adj_composite:.3f}")

    print(f"\nSOFTMAX SCENARIO WEIGHTS  (at adj_composite = {adj_composite:.3f})")
    for k, w in weights.items():
        print(f"  {k:<8} {w*100:>5.1f}%   ${scenarios[k]:.2f}")
    print(f"\n  Expected price (probability-weighted)  =  ${exp_price:.2f}")

    print(f"\nBUSINESS METRICS")
    print(f"  FY2025 revenue               = ${REV_FY2025_B:.0f}B  (+10%; 130+ countries)")
    print(f"  Risk & Insurance Svcs margin = {RIS_MARGIN_Q1:.1f}%  (Q1 2026; world's #1 insurance broker)")
    print(f"  Consulting margin            = {CONSULTING_MARGIN_Q1:.1f}%  (Q1 2026; Mercer + Oliver Wyman)")
    print(f"  FCF margin                   = ~16-17%  ($4.5B+ annual FCF; capital-light model)")
    print(f"  Margin expansion streak      = {MARGIN_EXPANSION_YEARS} consecutive years  (targeting year {MARGIN_EXPANSION_YEARS+1})")
    print(f"  FY2025 underlying rev growth = 4%  (soft market headwinds; structural 5-7% trend)")
    print(f"  Analyst avg PT               = $202.62  (range $179–$236; +23% from current)")
    print(f"  Analyst consensus            = 9 Buy / 1 Sell  (unusually strong conviction)")

    print(f"\nSIGNAL ENTRY GUIDE")
    # Thresholds: solve (p - EPP) / (price_b - p) = ratio_threshold  (EPP=126, price_b=266.80)
    # BUY:        p = (126 + 0.75×266.80) / 1.75 = (126 + 200.1) / 1.75 = $186.34 ≈ $186
    # ACCUMULATE: p = (126 + 1.10×266.80) / 2.10 = (126 + 293.48) / 2.10 = $199.75 ≈ $200
    # WATCHLIST:  p = (126 + 1.75×266.80) / 2.75 = (126 + 466.9) / 2.75 = $215.60 ≈ $216
    # HOLD/TRIM:  p = (126 + 2.50×266.80) / 3.50 = (126 + 667) / 3.50 = $226.57 ≈ $227
    print(f"  ✕ AVOID      above  $227  (ratio_b > 2.50×; 52-wk high $236 was deep AVOID at 3.54×)")
    print(f"  ▷ HOLD/TRIM  $216 – $227  (ratio_b 1.75–2.50×)")
    print(f"  ◐ WATCHLIST  $200 – $216  (ratio_b 1.10–1.75×; analyst avg PT $203 = low-WATCHLIST)")
    print(f"  ◎ ACCUMULATE $186 – $200  (ratio_b 0.75–1.10×)")
    print(f"  ◉ BUY        below  $186  (ratio_b < 0.75×)  ← current ${CURRENT_PRICE:.2f}  BUY")
    print()
    print(f"  52-wk low $158.16 = deep BUY (ratio_b 0.23×); near-term support at $158.")
    print(f"  52-wk high $235.78 = deep AVOID (ratio_b 3.54×) — appropriate at 22× FW EPS.")
    print(f"  Analyst avg PT $202.62 = bottom of WATCHLIST zone (not reflecting BUY signal).")
    print(f"  Key thesis: multiple normalisation from 15.5× → 22-23× = +$60-80 price gain,")
    print(f"  BEFORE accounting for EPS growth of 9-10%/yr. Double compounder at current price.")
    print(f"  Watch: Q2 2026 underlying revenue growth rate; Marsh segment premium data.")
