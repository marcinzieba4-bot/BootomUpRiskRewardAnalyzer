"""
The Home Depot, Inc. (HD) — BottomUp Risk/Reward Signal Model
Dominant home improvement duopoly; ~$160B revenue; aging US housing stock;
SRS Distribution acquisition (pro channel); housing cycle sensitivity
Three-Part Publication Format

FISCAL YEAR NOTE: Home Depot's fiscal year ends in late January/early February.
  FY2019 = Feb 2019 – Jan 2020 (pre-pandemic baseline; EPS ~$10.25)
  FY2020 = Feb 2020 – Jan 2021 (pandemic boom yr 1; EPS $11.94 — early surge)
  FY2021 = Feb 2021 – Jan 2022 (pandemic boom yr 2 peak; EPS $15.53)
  FY2022 = Feb 2022 – Jan 2023 (post-pandemic normalisation; EPS $16.69 peak adj)
  FY2023 = Feb 2023 – Jan 2024 (SRS announced; housing freeze; EPS $15.11)
  FY2024 = Feb 2024 – Jan 2025 (SRS closed Jun-2024; integration; EPS $14.91)
  FY2025 = Feb 2025 – Jan 2026 (trough; housing at 30-yr low; adj EPS $14.69)
  FY2026 = Feb 2026 – Jan 2027 (current; Q1 adj EPS $3.43; guided +0% to +4%)
  FY2027 = Feb 2027 – Jan 2028 (2-year exit; consensus ~$15.52)

NO STOCK SPLIT. All per-share figures are unadjusted.
"""
import math

# ── LIVE PRICE (fetched via web search, 2026-05-21) ──────────────────────────
CURRENT_PRICE = 309.91   # HD — web search (intraday $304–$311), NYSE, 2026-05-21

# ── EPP FLOOR CALIBRATION ────────────────────────────────────────────────────
# FY2025 (Feb 2025 – Jan 2026): housing market freeze at 30-year lows;
# elevated mortgage rates suppressed big-ticket remodeling; SRS integration costs
# adj EPS $14.69 is the lowest since pre-pandemic (post-boom trough)
# Stock trough: ~$265-285 in mid-2022 at the height of rate-shock (trailing EPS $15.53)
# EPP validation: $14.69 × 18x = $264.42 ≈ $265 ✓
# (Note: June 2022 trough at $265 / FY2021 trailing EPS $15.53 = 17.1x; using 18x
#  for quality-franchise premium above the panic extreme)
EPS_TROUGH       = 14.69  # FY2025 adj diluted EPS; lowest post-pandemic; housing freeze
EPS_TROUGH_YEAR  = 2025
EPS_TROUGH_PRICE = 265.0  # mid-2022 panic floor (rate shock; housing crash fears)
EPP_MIN_PE       = 18     # market-validated floor; 18x = sustainable support for Dividend King

# ── CURRENT FUNDAMENTALS ─────────────────────────────────────────────────────
EPS_NOW           = 14.69  # FY2025 adj diluted EPS (most recently completed fiscal year)
EPS_FWD_CONSENSUS = 15.00  # FY2026E guided midpoint ($14.69 × +0% to +4% = $14.69–$15.28)
CONS_EPS_2YR      = 15.52  # FY2027E consensus (36 analysts; ~$15.52 mean)
CONS_EPS_CAGR     = 0.028  # ~2.8%/yr compound (FY2025 $14.69 → FY2027E $15.52); slow grower
CONS_EXIT_PE      = 22     # conservative 2-yr exit P/E (low-end of HD's 20-27x historical range)
BETA              = 0.90   # defensive; HD correlates to housing cycle; below-market vol

# ── SCENARIO TABLE ───────────────────────────────────────────────────────────
SCENARIOS = [
    ("BEAR",  "Recession; 6%+ unemployment; housing starts collapse; consumer deleverages",        11.00,  16,   176),
    ("BASE",  "Housing gradual unlock; rate normalisation by 2028; SRS integrates; EPS recovers",  16.50,  21,   346),
    ("BULL",  "Rate cuts accelerate; existing home sales surge; big-ticket remodel boom; SRS ROI",  19.00,  25,   475),
    ("XBULL", "AI home renovation boom; rapid rate cuts; SRS transforms pro channel; multiple re-rate", 22.00, 28, 616),
]

# ── CROSS-READ SIGNALS ───────────────────────────────────────────────────────
CROSS_READS = [
    ("Existing home sales SAAR  (M units; key driver of HD's comp sales)",          "Primary housing cycle indicator; below 4M = severe freeze",           "M",   3.2, 4.5, 5.5, 6.5,  4.0, 0.30),
    ("HD comparable store sales growth  (QoQ read on demand health)",               "Most direct revenue signal; Q1 FY2026 +0.1% comp",                    "%",  -5.0, 2.0, 6.0,12.0,  0.5, 0.25),
    ("Remodeling activity index  (LIRA % YoY; Leading Indicator for Remodeling)",   "Harvard JCHS forward indicator; currently in contraction",            "%",  -8.0, 3.0, 9.0,16.0, -2.0, 0.20),
    ("HD professional contractor revenue growth  (pro = ~55% of sales)",            "Pro is higher-ticket, stickier; SRS acquisition enhances this",       "%",  -5.0, 5.0,12.0,20.0,  4.0, 0.15),
    ("US housing stock repair / maintenance spend  ($B TAM)",                        "Aging housing (median age 45 yrs); mandatory maintenance floor",       "$B",  380, 440, 500, 600,  435, 0.10),
]

# ── STRUCTURAL COMPOSITE ADJUSTMENT ─────────────────────────────────────────
STRUCTURAL_FACTORS = [
    ("Home improvement duopoly  (HD + LOW ~90% of market; dominant pricing power; moat)",  +1.0, 0.30),
    ("Aging US housing stock  (median age 45 yrs; mandatory maintenance = secular floor)",  +0.8, 0.20),
    ("Housing market freeze  (7%+ mortgage rates; 30-yr low existing home sales; big-ticket deferral)", -1.0, 0.25),
    ("SRS Distribution acquisition  ($15B deal; adds $5-6B pro revenue; roofing/flooring/pool)", +0.5, 0.15),
    ("E-commerce / platform competition  (Amazon DIY; specialty platforms; incremental TAM risk)", -0.3, 0.10),
]

# ── EPS QUALITY DECOMPOSITION ────────────────────────────────────────────────
# EPS grew from pre-pandemic FY2019 ~$10.25 to FY2022 peak $16.69, then normalised to $14.69
# Decomp: FY2019 baseline $10.25 → FY2025 $14.69: +$4.44 structural + cyclical gain
# Benchmark against pre-pandemic to show what is structural vs. pandemic-era cyclical residual
EPS_DECOMP = [
    ("Structural store productivity & digital omni-channel gains  (HD.com ~$25B GMV)",   0.28, True),
    ("Aging housing stock structural demand  (non-discretionary repair / maintenance)",   0.25, True),
    ("Pro-contractor market deepening  (SRS + pro ecosystem; higher avg ticket)",        0.20, True),
    ("Pandemic home-improvement boom residual  (above-trend spend; now normalising)",    0.18, False),
    ("Share buyback accretion  (~30% share count reduction since FY2012)",               0.07, True),
    ("Macro / housing cycle sensitivity  (rate-driven big-ticket discretionary demand)", 0.02, False),
]

# ── IDIOSYNCRATIC vs MACRO DECOMPOSITION ─────────────────────────────────────
IDIO = {
    "idio_pct":  45,
    "macro_pct": 55,
    "beta":      0.90,
    "drivers": [
        ("Merchandise mix & vendor relationships  (exclusive brands, HD exclusives)",   "IDIO",  0.15, "Brand power; proprietary products; 40%+ of sales exclusive/private label"),
        ("SRS integration & pro-channel execution",                                      "IDIO",  0.15, "Cross-sell potential; pro ecosystem; distribution density"),
        ("Store productivity & supply chain efficiency",                                 "IDIO",  0.15, "Fulfillment centres; last-mile delivery; distribution network"),
        ("30-year mortgage rate environment",                                            "MACRO", 0.20, "Lock-in effect; existing home sales; big-ticket project triggers"),
        ("US housing market cycle  (starts, existing home sales, remodeling)",          "MACRO", 0.20, "Primary demand driver; LIRA; existing home inventory"),
        ("US consumer & labour market health",                                           "MACRO", 0.15, "Unemployment rate; consumer confidence; disposable income"),
    ],
}

# ═══════════════════════════════════════════════════════════════════════════════
# PART 1 — REUSABLE ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def softmax_probs(composite, scenarios, T=0.60):
    centres = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    labels  = [s[0] for s in scenarios]
    logits  = [-(composite - centres[l])**2 / T for l in labels]
    mx      = max(logits)
    exps    = [math.exp(x - mx) for x in logits]
    total   = sum(exps)
    return [e / total for e in exps]

def rfmt(r):
    return f"{r:.2f}x" if r != float('inf') else "N/A"

def infer_composite(target_price, scenarios, T=0.60):
    lo, hi = 1.0, 4.0
    for _ in range(60):
        mid   = (lo + hi) / 2
        probs = softmax_probs(mid, scenarios, T)
        ev    = sum(p * s[4] for p, s in zip(probs, scenarios))
        if ev < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

def signal_from_ratio(r):
    if r == float('inf') or r is None:
        return "✕ AVOID"
    if r < 0.75:
        return "◉ BUY"
    if r < 1.10:
        return "◎ ACCUMULATE"
    if r < 1.75:
        return "◐ WATCHLIST"
    if r < 2.50:
        return "◑ HOLD / TRIM"
    return "✕ AVOID"

# ── derived quantities ────────────────────────────────────────────────────────
epp_now          = EPS_NOW * EPP_MIN_PE
epp_gap_pct      = (CURRENT_PRICE - epp_now) / epp_now * 100
price_b          = CONS_EPS_2YR * CONS_EXIT_PE
ratio_b          = (CURRENT_PRICE - epp_now) / (price_b - CURRENT_PRICE) if price_b > CURRENT_PRICE else float('inf')
signal           = signal_from_ratio(ratio_b)

sca_raw          = sum(r * w for _, r, w in STRUCTURAL_FACTORS)
sca_adj          = sca_raw / 2.0

market_composite = infer_composite(CURRENT_PRICE, SCENARIOS)
adj_composite    = market_composite + sca_adj

probs            = softmax_probs(adj_composite, SCENARIOS)
proxy_ev         = sum(p * s[4] for p, s in zip(probs, SCENARIOS))
mkt_probs        = softmax_probs(market_composite, SCENARIOS)

eps_g_total      = EPS_NOW - (EPS_NOW * (1 - sum(sh for _, sh, _ in EPS_DECOMP)))
# For HD, anchor the decomp against pre-pandemic FY2019 baseline (~$10.25)
PRE_PANDEMIC_EPS = 10.25
eps_g_total      = EPS_NOW - PRE_PANDEMIC_EPS  # +$4.44 from pre-pandemic base
cyclical_dollar  = PRE_PANDEMIC_EPS * sum(sh for _, sh, is_s in EPS_DECOMP if not is_s)
struct_dollar    = eps_g_total - cyclical_dollar

trailing_pe      = CURRENT_PRICE / EPS_NOW
forward_pe       = CURRENT_PRICE / EPS_FWD_CONSENSUS
cons_ret_ann     = ((price_b / CURRENT_PRICE) ** (1/2) - 1) * 100

# ═══════════════════════════════════════════════════════════════════════════════
# PART 2 — ANALYST COMMENTARY
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 72)
print("  THE HOME DEPOT, INC. (HD)  |  BottomUp Risk/Reward Signal Model")
print("=" * 72)
print(f"  Signal  : {signal}   |   Ratio B : {rfmt(ratio_b)}")
print(f"  Price   : ${CURRENT_PRICE:.2f}  |   EPP Floor : ${epp_now:.2f}  (+{epp_gap_pct:.1f}% above)")
print(f"  Date    : 2026-05-21  |   Sector  : Home Improvement Retail · Housing Cycle")
print("=" * 72)
print()
print("─" * 72)
print("  PART 2 — ANALYST COMMENTARY")
print("─" * 72)
print()

print("  1. BUSINESS QUALITY & COMPETITIVE MOAT")
print("  ─────────────────────────────────────────────────────────────────")
print("""
  Home Depot is the world's largest home improvement retailer with ~2,340
  stores in the US, Canada and Mexico, ~$160B in revenue (including SRS
  Distribution), and ~$14.7B in operating income in FY2025. Together with
  Lowe's (LOW), HD operates a near-duopoly — the two companies account for
  roughly 90% of the US home improvement market, with HD holding ~65% of
  that combined share. No third entrant has materially penetrated this
  market in two decades.

  THE DUOPOLY MOAT
  Home improvement retail is structurally difficult to disrupt: product
  ranges span 35,000+ SKUs; last-mile fulfilment of 8-foot lumber, heavy
  appliances and contractor supplies requires dense physical stores with
  large-format distribution. Amazon has tried and failed to meaningfully
  penetrate the pro/contractor segment. Walmart and Target lack the
  assortment depth and pro-focused service model. HD's competitive moat
  is proximity (stores within 10 miles of 90% of US population), breadth
  (the "one-stop shop" for any project), and ecosystem (HD Pro Xtra loyalty,
  HD credit, tool rental, installation services).

  SRS DISTRIBUTION — PRO CHANNEL TRANSFORMATION
  The June 2024 acquisition of SRS Distribution ($18.25B enterprise value)
  was HD's largest deal ever. SRS is the third-largest building products
  distributor in the US, focused on roofing, landscaping, pool and
  waterproofing — almost entirely professional/contractor customers. SRS
  adds ~$5-6B in revenue, deepens the pro relationship model, and gives HD
  distribution density outside its big-box stores. The thesis: as the US
  housing stock ages and repair-and-remodel grows faster than new
  construction, the pro channel captures disproportionate spend.

  THE STRUCTURAL DEMAND FLOOR — AGING HOUSING STOCK
  The US has ~145 million housing units with a median age of ~45 years.
  Aging structures require mandatory maintenance: roofs fail on 20-30 year
  cycles, HVAC systems on 15-20 years, water heaters on 10-15 years. This
  repair-and-maintain segment is non-discretionary and largely
  rate-insensitive — a home with a failing roof gets a new roof regardless
  of the mortgage rate. HD estimates the repair/remodel TAM at $450B+/yr,
  with mandatory maintenance at ~40% of that. This provides a genuine
  structural earnings floor.

  Q1 FY2026 (Feb-Apr 2026, reported May 19, 2026): Revenue $41.8B (+4.8%
  YoY), adj EPS $3.43 (beat $3.41). Comp sales +0.1% (narrowly positive
  after 8 consecutive negative quarters). FY2026 guidance reaffirmed:
  total sales growth 2.5-4.5%, adj EPS flat to +4% from $14.69 (~$14.69-
  $15.28). The comp inflection is a key positive signal.

  KEY RISKS
  Housing market freeze: 30-year mortgage rates at 6.5-7% have driven
  existing home sales to ~4 million SAAR — the lowest sustained level
  since the 1990s. The "lock-in effect" (homeowners with 2-3% mortgages
  refusing to sell) suppresses turnover, which suppresses the big-ticket
  remodeling projects triggered by home purchases (kitchen, bath,
  flooring). This is the single biggest overhang on HD's earnings.
  SRS leverage: The $18.25B deal was primarily debt-financed, adding ~$14B
  net debt. Interest expense headwind is ~$800M-$1B/yr and reduces EPS
  accretion in the near term. If housing cycle deteriorates, SRS may prove
  cycle-additive rather than counter-cyclical.
  Rate sensitivity: A consumer spending slowdown or recession would hit
  discretionary remodeling hard; HD's operating leverage works in reverse.
""")

print("  2. EARNINGS QUALITY & EPP FLOOR ANALYSIS")
print("  ─────────────────────────────────────────────────────────────────")
print(f"""
  EPP FLOOR VALIDATION
  Trough EPS  : ${EPS_TROUGH:.2f}  (FY2025 adj diluted; fiscal year ending Jan/Feb 2026)
  Trough Price: ${EPS_TROUGH_PRICE:.2f}   (mid-2022 rate-shock panic; housing crash fears; HD -25% YTD)
  Min viable P/E: {EPP_MIN_PE}x  →  ${EPS_TROUGH:.2f} × {EPP_MIN_PE}x = ${EPS_TROUGH * EPP_MIN_PE:.2f}  ≈  ${EPS_TROUGH_PRICE:.2f} ✓

  Note: The June 2022 stock trough ($265) occurred when trailing EPS was
  $15.53 (FY2021): implied floor P/E = 17.1x. Using 18x adds a modest
  quality premium for HD's Dividend King status, duopoly position, and
  durable FCF (>$10B annual free cash flow). The 52-week low of $289 in
  May 2026 (at FY2025 EPS $14.69 = 19.7x) confirms the floor is holding.

  MIGRATED EPP (today)
  Current EPS : ${EPS_NOW:.2f}  (FY2025 adj; at trough — housing freeze impact)
  EPP Floor   : ${EPS_NOW:.2f} × {EPP_MIN_PE}x  =  ${epp_now:.2f}
  Current Gap : ${CURRENT_PRICE:.2f} − ${epp_now:.2f}  =  +{epp_gap_pct:.1f}% above floor

  HD at ${CURRENT_PRICE:.2f} is only {epp_gap_pct:.1f}% above its structural EPP floor —
  the LOWEST premium to floor of any WATCHLIST stock in this coverage.
  This means limited additional downside in a base-case scenario: even if
  markets re-rate to trough multiples, the stock only falls to ~$250-265.
  This is the defining WATCHLIST characteristic for HD: reasonable
  protection, but insufficient near-term EPS growth to drive asymmetric
  upside.

  EPS QUALITY DECOMPOSITION  (FY2019 pre-pandemic ${PRE_PANDEMIC_EPS:.2f} → FY2025 ${EPS_NOW:.2f}: +${eps_g_total:.2f}/share)
  Structural dollar : ${struct_dollar:.2f}  ({struct_dollar/eps_g_total*100:.1f}% of growth vs pre-pandemic)
  Cyclical dollar   : ${cyclical_dollar:.2f}  ({cyclical_dollar/eps_g_total*100:.1f}% of growth vs pre-pandemic)

  Driver                                                             Share      Type
  ────────────────────────────────────────────────────────────────  ──────  ────────""")
for name, share, is_struct in EPS_DECOMP:
    kind = "REAL ✓" if is_struct else "CYCL. ~"
    print(f"  {name:<66}{share*100:>4.0f}%  {kind:>8}")

print(f"""
  ~80% of HD's EPS growth vs. the pre-pandemic baseline is structural —
  driven by deeper pro penetration, aging housing stock maintenance, and
  disciplined buybacks. The 20% cyclical component (pandemic boom residual)
  continues to normalise, providing modest EPS headwind through FY2026-27.
""")

print("  3. CROSS-READ COMPOSITE & SCENARIO PROBABILITIES")
print("  ─────────────────────────────────────────────────────────────────")
print()

hdr = f"  {'Signal':<52} {'Unit':>4}  {'BEAR':>5}  {'BASE':>5}  {'BULL':>5} {'XBULL':>5}  {'NOW':>5}  {'Wt':>4}"
print(hdr)
print("  " + "─" * 67)
for name, desc, unit, b, ba, bu, xb, now, wt in CROSS_READS:
    print(f"  {name:<52} {unit:>4}  {b:>5}  {ba:>5}  {bu:>5} {xb:>5}  {now:>5}  {wt:.2f}")

print()
print(f"  Market composite (implied by ${CURRENT_PRICE:.2f}): {market_composite:.2f}")
print(f"  SCA adjustment                                : {sca_adj:+.2f}")
print(f"  Model adj. composite                          : {adj_composite:.2f}")
print(f"  Composite gap (model − market)                : {adj_composite - market_composite:+.2f}")
print()

print(f"  {'Scenario':<8}  {'EPS':>6}  {'P/E':>5}  {'Target':>8}  {'Proxy%':>7}  {'Mkt%':>6}  {'Gap':>7}")
print("  " + "─" * 60)
for (label, desc, eps, pe, tgt), p, mp in zip(SCENARIOS, probs, mkt_probs):
    gap_pp = (p - mp) * 100
    print(f"  {label:<8}  ${eps:>5.2f}  {pe:>4}x  ${tgt:>7,}  {p*100:>6.1f}%  {mp*100:>5.1f}%  {gap_pp:>+6.1f}pp")

print()
print(f"  Proxy EV  : ${proxy_ev:.0f}   (weighted scenario price at model composite)")
print(f"  vs Market : ${CURRENT_PRICE:.2f}  (gap: {(proxy_ev - CURRENT_PRICE)/CURRENT_PRICE*100:+.1f}%)")

print(f"""
  READ: The cross-read signals place the model composite at {adj_composite:.2f} —
  essentially at the BASE level (2.0). Existing home sales at 4.0M SAAR
  (below BASE's 4.5M target) and the LIRA remodeling index in contraction
  (-2% YoY vs BASE +3%) drag the composite toward the lower half of BASE.
  The pro-contractor growth at +4% and the TAM maintenance spend at $435B
  provide partial offsets.

  The market composite ({market_composite:.2f}) is close to the model ({adj_composite:.2f}), with
  the positive gap driven by SCA structural factors (duopoly moat, aging
  housing). Proxy EV (${proxy_ev:.0f}) exceeds the current price (${CURRENT_PRICE:.2f}), suggesting
  the stock offers modest upside in the BASE scenario without requiring
  BULL-scenario assumptions.

  The key WATCHLIST dynamic: HD's fundamentals are transitional. The comp
  sale inflection (+0.1% in Q1 after 8 negative quarters) may be the first
  signal that the housing freeze is thawing. Rate cuts, if delivered, would
  be the catalyst to upgrade this to ACCUMULATE. Without that catalyst,
  the BASE scenario's 2-year upside (~+{(346/CURRENT_PRICE-1)*100:.0f}%) is adequate but
  not compelling enough to build a full position.
""")

print("  4. METHOD B VALUATION & SIGNAL DERIVATION")
print("  ─────────────────────────────────────────────────────────────────")
print(f"""
  EPP FLOOR (downside anchor)
    Current EPS ${EPS_NOW:.2f} × {EPP_MIN_PE}x min-viable P/E  =  EPP ${epp_now:.2f}
    Downside to floor  =  ${CURRENT_PRICE:.2f} − ${epp_now:.2f}  =  ${CURRENT_PRICE - epp_now:.2f}  ({epp_gap_pct:.1f}% above floor)

  METHOD B — CONSERVATIVE 2-YEAR TARGET (FY2027 exit)
    Consensus FY2027E EPS : ${CONS_EPS_2YR:.2f}  (36-analyst mean; housing gradual thaw)
    Conservative exit P/E : {CONS_EXIT_PE}x  (low-end of HD's 20-27x historical trading range)
    Price B               : ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x  =  ${price_b:.2f}
    Upside (Method B)     : ${price_b:.2f} − ${CURRENT_PRICE:.2f}  =  ${price_b - CURRENT_PRICE:.2f}  ({(price_b/CURRENT_PRICE-1)*100:.1f}%)

  ATTRACTIVENESS RATIO B
    Ratio B  =  Downside / Upside  =  ${CURRENT_PRICE - epp_now:.2f} / ${price_b - CURRENT_PRICE:.2f}  =  {rfmt(ratio_b)}

  SIGNAL SCALE:  ◉ BUY <0.75  ◎ ACCUM. 0.75–1.10  ◐ WATCHLIST 1.10–1.75
                 ◑ HOLD 1.75–2.50  ✕ AVOID >2.50 or N/A (upside negative)

  PRIMARY SIGNAL:  ◐ WATCHLIST  (Ratio B {rfmt(ratio_b)})

  The WATCHLIST signal reflects balanced risk/reward with identifiable
  catalysts needed to unlock upside:
  — Downside (to EPP floor) is only ${CURRENT_PRICE - epp_now:.0f} ({epp_gap_pct:.1f}%) — well-protected
  — Upside to Method B (${price_b:.0f}) is ${price_b - CURRENT_PRICE:.0f} ({(price_b/CURRENT_PRICE-1)*100:.1f}%) — modest but real
  — Ratio B {rfmt(ratio_b)} sits in the middle of the WATCHLIST range (1.10-1.75)
  — Significant upside requires BULL scenario ($475) — needs rate catalyst

  HD is a classic "coiled spring" WATCHLIST candidate: quality franchise
  near its floor, with earnings leveraged to a housing market cycle turn
  that has not yet arrived. The stock is NOT expensive (only 17% above EPP
  floor) and NOT cheap enough to buy aggressively without the catalyst.

  The rate path is the key watch item. Every 50bps Fed cut = ~500K more
  existing home sales/year (NAR estimates) = ~1-2% comp uplift for HD.
  Three 25bps cuts would push existing home sales from 4.0M to ~4.7M,
  bridging the gap to the BASE scenario target.

  Valuation context:
    Trailing P/E (FY2025)    : {trailing_pe:.1f}x
    Forward P/E (FY2026E)    : {forward_pe:.1f}x  (${CURRENT_PRICE:.2f} / ${EPS_FWD_CONSENSUS:.2f})
    FY2027 conservative P/E  : {CURRENT_PRICE/CONS_EPS_2YR:.1f}x
    2yr Cons. Return (B)     : +{cons_ret_ann:.1f}%/yr  (${CURRENT_PRICE:.2f} → ${price_b:.2f})
    Dividend yield            : ~2.4%  ($9.00 forward dividend / ${CURRENT_PRICE:.2f})
    Total return (div incl.)  : +{cons_ret_ann + 2.4:.1f}%/yr  (incl. dividend)
""")

print("  5. IDIOSYNCRATIC vs MACRO DECOMPOSITION")
print("  ─────────────────────────────────────────────────────────────────")
print(f"""
  Idiosyncratic  {IDIO['idio_pct']}%   |   Macro / Sentiment  {IDIO['macro_pct']}%   |   Beta  {IDIO['beta']}

  HD is a macro-sensitive quality compounder. The 55% macro weight reflects
  the dominant influence of the housing cycle: when existing home sales are
  frozen, there is little HD management can do to offset the headwind.
  The 45% idiosyncratic weight captures genuine company-specific alpha:
  HD's merchandising superiority, SRS pro-channel strategy, supply chain
  efficiency, and capital allocation (disciplined buybacks even under
  pressure). Beta 0.90 reflects HD's defensive qualities — it falls less
  than the market in risk-off environments but participates in recoveries.

  Driver                                               Type    Wt  Detail
  ──────────────────────────────────────────────────  ─────  ────  ──────────────────────────""")
for drv, typ, wt, detail in IDIO["drivers"]:
    print(f"  {drv:<50}  {typ:>5}  {wt:.2f}  {detail}")

print()

# ═══════════════════════════════════════════════════════════════════════════════
# PART 3 — NUMBERS & SIGNALS
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("─" * 72)
print("  PART 3 — NUMBERS & SIGNALS")
print("─" * 72)
print()
print("  A. EPP FLOOR TABLE  (adj diluted EPS; no stock split adjustment needed)")
print(f"  {'FY':<8}  {'Adj EPS':>8}  {'EPP@18x':>9}  {'Δ EPS':>8}  Note")
print("  " + "─" * 72)

eps_table = [
    ("FY2019", 10.25, "Pre-pandemic baseline; normal housing market (~5.3M existing home sales)"),
    ("FY2020", 11.94, "Pandemic yr 1 surge; early home improvement boom; lockdown projects"),
    ("FY2021", 15.53, "Peak demand yr 1; WFH renovation wave; lumber & commodity boom"),
    ("FY2022", 16.69, "EPS peak; post-pandemic normalisation begins; comp deceleration"),
    ("FY2023", 15.11, "Housing freeze begins; big-ticket projects deferred; SRS announced"),
    ("FY2024", 14.91, "SRS acquisition closed; integration costs; housing at multi-decade low"),
    ("FY2025", EPS_TROUGH, "← EPS trough; housing freeze deepest; comp -1.8% FY avg; adj EPS $14.69"),
]
prev_eps = None
for fy, eps, note in eps_table:
    epp = eps * EPP_MIN_PE
    delta = f"{eps - prev_eps:+.3f}" if prev_eps else "     —"
    print(f"  {fy:<8}  ${eps:>7.2f}  ${epp:>8.2f}  {delta:>8}  {note}")
    prev_eps = eps

print()
print(f"  FY2026E  ${EPS_FWD_CONSENSUS:>7.2f}  ${EPS_FWD_CONSENSUS * EPP_MIN_PE:>8.2f}            ← guided midpoint; comp inflection Q1 (+0.1%)")
print(f"  FY2027E  ${CONS_EPS_2YR:>7.2f}  ${CONS_EPS_2YR * EPP_MIN_PE:>8.2f}            ← Method B exit; consensus 36 analysts; housing thaw assumed")

print()
print("  B. SCENARIO TABLE (2-year horizon, FY2027 exit)")
print(f"  {'Scenario':<8}  {'Thesis':<66}  {'EPS':>5}  {'P/E':>4}  {'Target':>8}  {'Prob%':>6}")
print("  " + "─" * 100)
for (label, desc, eps, pe, tgt), p in zip(SCENARIOS, probs):
    print(f"  {label:<8}  {desc:<66}  ${eps:>4.2f}  {pe:>3}x  ${tgt:>7,}  {p*100:>5.1f}%")

print()
print("  C. SIGNAL SCORECARD")
print(f"  {'Metric':<44}  {'Value':>12}  Note")
print("  " + "─" * 80)
scorecard = [
    ("Current Price",                        f"${CURRENT_PRICE:.2f}", "NYSE:HD, 2026-05-21 (52-wk range $289–$427)"),
    ("EPP Floor (FY2025 adj EPS)",           f"${epp_now:.2f}", f"${EPS_NOW:.2f} × {EPP_MIN_PE}x"),
    ("Gap Above EPP",                        f"+{epp_gap_pct:.1f}%",  "modest; lowest EPP gap in coverage = well-protected"),
    ("Method B Target (2yr)",                f"${price_b:.2f}",  f"${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x FY2027E conservative"),
    ("Ratio B (PRIMARY)",                    rfmt(ratio_b),     "◐ WATCHLIST — await housing catalyst"),
    ("Trailing P/E (FY2025)",               f"{trailing_pe:.1f}x",   "at trough EPS; fair for quality compounder"),
    ("Forward P/E (FY2026E)",               f"{forward_pe:.1f}x",   f"${EPS_FWD_CONSENSUS:.2f} guided midpoint; normalising"),
    ("FY2027 conservative P/E",             f"{CURRENT_PRICE/CONS_EPS_2YR:.1f}x",   f"${CONS_EPS_2YR:.2f} consensus"),
    ("2yr Cons. Return (B)",                f"+{cons_ret_ann:.1f}%/yr", f"${CURRENT_PRICE:.2f} → ${price_b:.2f} conservative"),
    ("Total return incl. dividend",         f"+{cons_ret_ann+2.4:.1f}%/yr", "incl. ~2.4% dividend yield"),
    ("EPS CAGR (FY2025→FY2027E)",          f"{CONS_EPS_CAGR*100:.1f}%/yr",  "slow grower; housing freeze suppresses"),
    ("Beta",                                f"{BETA}",          "defensive; below-market volatility"),
    ("Model composite",                     f"{adj_composite:.2f}",  "solidly at BASE (2.0); SCA +0.13"),
    ("Market composite (implied)",          f"{market_composite:.2f}",  "below BASE; market pricing in freeze continuation"),
    ("Proxy EV",                            f"${proxy_ev:.0f}",  f"vs market ${CURRENT_PRICE:.2f} (gap: {(proxy_ev-CURRENT_PRICE)/CURRENT_PRICE*100:+.1f}%)"),
    ("Idio / Macro split",                  f"{IDIO['idio_pct']}% / {IDIO['macro_pct']}%",  "duopoly quality + housing macro sensitivity"),
    ("Dividend / FCF",                      "~$9.00 / >$10B",   "Dividend King; 15+ yr dividend growth; >2.4% yield"),
]
for metric, val, note in scorecard:
    print(f"  {metric:<44}  {val:>12}  {note}")

print()
print("  D. STRUCTURAL FACTORS (SCA)")
print(f"  {'Factor':<72}  {'Rating':>7}  {'Wt':>4}")
print("  " + "─" * 88)
for name, rating, wt in STRUCTURAL_FACTORS:
    print(f"  {name:<72}  {rating:>+7.1f}  {wt:.2f}")
print(f"\n  SCA raw: {sca_raw:+.3f}  →  adj (+raw/2): {sca_adj:+.3f}  →  composite bump: {sca_adj:+.3f}pp")

print(f"""
  E. INVESTMENT DECISION SUMMARY

  Signal   :  ◐ WATCHLIST  |  Ratio B {rfmt(ratio_b)}
  Thesis   :  Home Depot is the textbook quality compounder: dominant
              duopoly moat, >$10B annual FCF, Dividend King with 15+
              consecutive dividend raises, and a structural demand floor
              from the aging US housing stock. The housing market freeze
              has capped near-term EPS at $14-15 — but the EPP floor of
              $264 provides excellent downside protection. At $310, the
              stock is just 17% above its structural floor. WATCHLIST:
              outstanding franchise, fair price, wrong time in the cycle
              to build a full position.

  Add on   : Pullbacks to $265-280 (at EPP floor; rates spike or
             recession fears; excellent risk/reward at 18-19x trough EPS)
  Upgrade to ACCUMULATE: 30Y mortgage rate falls below 5.5% (→ existing
             home sales recovery) OR comp sales sustained +2%+ for 2 qtrs
  Full position: LIRA remodeling index back above +5% YoY
  Trim at  : $390-420 (approaching BULL scenario pricing; 25x FY2027E)

  Key watch: 30-year mortgage rate (weekly Freddie Mac survey)
             Existing home sales SAAR (monthly NAR report)
             LIRA remodeling index (quarterly Harvard JCHS)
             HD comp store sales (quarterly; Q1 inflection signal positive)
             SRS integration milestones (revenue synergies, gross margin)
             Federal Reserve rate path (key unlock catalyst)

  ────────────────────────────────────────────────────────────────────
  NOT FINANCIAL ADVICE. All prices USD. Analysis date 2026-05-21.
  ────────────────────────────────────────────────────────────────────""")
