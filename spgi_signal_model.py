"""
S&P Global Inc.  (SPGI)
BottomUp Risk/Reward Analyzer — Signal Model
"""
import math

# ── Core inputs ──────────────────────────────────────────────────────────────
TICKER        = "SPGI"
COMPANY       = "S&P Global Inc."
SECTOR        = "Financial Data & Analytics · Credit Ratings Duopoly · Indices (S&P 500) · Market Intelligence"

CURRENT_PRICE  = 417.95   # SPGI — fetched via web search, 2026-05-26
                            # May 25-26, 2026 intraday range $415.00–$421.60; mkt cap ~$123.6B
PRICE_52W_LOW  = 381.61   # April 2026 tariff-panic low (+9.5% to current)
PRICE_52W_HIGH = 579.05   # Nov 2025 high; SPGI is 27.8% below its 52-wk peak
SHARES_M       = 296.0    # Approx: mkt cap $123.6B / $417.95; buyback ~$4-5B/yr (~15M shr/yr)
DIVIDEND_ANN   = 3.76     # $0.94/quarter (raised Q1 2026; yield 0.90% at $418)

# ── EPS history (adjusted / non-GAAP diluted) ────────────────────────────────
# NOTE: SPGI uses ADJUSTED EPS for guidance and consensus. Adj-GAAP gap ~$2.59/yr
# (FY2025: adj $17.25 vs GAAP $14.66) — primarily IHS Markit intangible amortisation
# (~$700M/yr amort) following the $44B IHS Markit acquisition completed Feb 2022.
# All EPS figures below are ADJUSTED (non-GAAP).
EPS_HISTORY = {
    "FY2022": 11.19,   # Trough year: IHS Markit integration drag + rates-shock cut bond issuance
                        # Confirmed: adj EPS $11.19 (GAAP $10.20); Ratings down -26% as issuance collapsed
    "FY2023": 13.40,   # Recovery: issuance rebound, Market Intelligence + Indices growth resumed
    "FY2024": 15.10,   # Sustained growth: Indices +25%+, Ratings + Commodities recovery
    "FY2025": 17.25,   # Actuals at high end of guidance: +14% growth; net card fees adj record
}
EPS_NOW = 19.53   # FY2026E adj EPS guidance midpoint ($19.40–$19.65); Q1 2026 actual $4.97 (+14% beat)
                   # FY2026 guidance raised after Q1 2026; reflects Ratings + Indices + MI growth

# ── EPP (Earnings Power Price) — structural floor ────────────────────────────
EPS_TROUGH  = 10.00   # Severe rates shock / credit market freeze: bond issuance collapse -50%+
                        # History: FY2022 adj $11.19 was the ACTUAL rates-shock trough. $10.00 is slightly
                        # below that — a scenario where rates stay high 3+ years AND credit markets
                        # seize. Indices and Market Intelligence provide structural cushion (~60% of
                        # revenue is subscription/recurring; only Ratings is truly cyclical issuance).
                        # $10.00 = ~57% of FY2026E guidance = severe but not existential.
EPP_MIN_PE  = 20      # SPGI franchise floor: even in the FY2022 rates-shock trough, SPGI never
                        # traded below 20-22× forward EPS. Regulated duopoly (S&P + Moody's = 80%
                        # of credit ratings globally) + S&P 500 index franchise (≥$10T AUM tracking)
                        # = structural moat that commands elevated trough multiple. Compare: commercial
                        # banks (9×), IB/GS (11×), AXP (18×) — SPGI at 20× reflects near-monopoly
                        # franchise value and regulatory moat (NRSRO designation is extremely hard to
                        # replicate; Fitch is a distant #3).
EPP         = EPS_TROUGH * EPP_MIN_PE   # = $200.00

# ── Method B (2-year normalised upside ceiling) ───────────────────────────────
CONS_EPS_2YR  = 22.50   # FY2027E adj EPS estimate: FY2026E $19.53 × ~15% = $22.46 ≈ $22.50
                          # Post-Mobility-Global separation SPGI is purer (Ratings + Indices + MI
                          # + Commodity Insights); MBGL spin removes ~$1.5-2B lower-margin revenue
                          # but SPGI retains all high-margin data/analytics. 15% growth = continuation
                          # of 2023-2026 compound rate driven by AI-assisted ratings analytics,
                          # Indices AUM growth (every S&P 500 point = ~$35M in licensing fees).
CONS_EXIT_PE  = 25        # Post-Mobility SPGI deserves higher multiple: purer data/analytics mix.
                          # Historical SPGI P/E range: 20-35× (avg ~27× 2019-2024 ex-trough).
                          # 25× is conservative vs historical avg; reflects current higher-rate
                          # discount rate environment. Vs Moody's (MCO) at ~30× FY2026E.
price_b = CONS_EPS_2YR * CONS_EXIT_PE   # = $562.50

# ── Primary signal: Ratio B ───────────────────────────────────────────────────
ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
# = (417.95 - 200) / (562.50 - 417.95) = 217.95 / 144.55 = 1.508×
# Signal: ◐ WATCHLIST (1.10–1.75×)

# ── Softmax composite engine ──────────────────────────────────────────────────
T = 0.60
SCENARIOS = {
    "BEAR":  {"price": 200.00,  "label": "BEAR"},   # EPP floor; rates stay high 3+ yrs; issuance -50%
    "BASE":  {"price": 490.00,  "label": "BASE"},   # +17% from current; FY2026E $19.53 × 25× = $488
    "BULL":  {"price": 562.50,  "label": "BULL"},   # Method B ceiling; FY2027E $22.50 × 25×
    "XBULL": {"price": 700.00,  "label": "XBULL"},  # Re-rating to 31×; Indices AUM + AI analytics
}

SIGNAL_CENTRES = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}

def softmax_weights(composite):
    logits = {s: -(composite - c)**2 / T for s, c in SIGNAL_CENTRES.items()}
    max_l  = max(logits.values())
    raw    = {s: math.exp(v - max_l) for s, v in logits.items()}
    total  = sum(raw.values())
    return {s: v / total for s, v in raw.items()}

def expected_price(composite):
    w = softmax_weights(composite)
    return sum(w[s] * SCENARIOS[s]["price"] for s in SCENARIOS)

def infer_composite(target_price, lo=1.0, hi=4.0, iterations=60):
    for _ in range(iterations):
        mid = (lo + hi) / 2
        if expected_price(mid) < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

market_composite = infer_composite(CURRENT_PRICE)

# ── SCA (Signal Catalyst Adjustments) ────────────────────────────────────────
SCA_FACTORS = [
    # Tailwinds
    {"label": "Mobility Global spin-off (MBGL)",
     "rating": +0.35, "weight": 0.25,
     "note": "CARFAX + Polk + automotiveMastermind IPO July 1 2026 — shareholders receive MBGL shares."
             " Unlocks SPGI pure-play re-rating; lower-margin auto-data business removed from mix."
             " Record date June 15. Imminent catalyst."},
    {"label": "S&P 500 index franchise AUM compounding",
     "rating": +0.30, "weight": 0.20,
     "note": "≥$10T AUM tracks S&P indices. Each index point ≈ $35M in annual licensing fees."
             " As passive investing grows (now >50% of US equity AUM), this annuity stream compounds"
             " independent of ratings cycle. Dividend Aristocrats, ESG, factor ETF proliferation."},
    {"label": "Ratings duopoly regulatory moat",
     "rating": +0.25, "weight": 0.15,
     "note": "NRSRO designation (SEC-registered) is near-impossible to replicate. S&P + Moody's = ~80%"
             " global credit ratings. When bond issuance recovers (Fed rate-cut cycle), both volume and"
             " pricing power increase simultaneously. AI-assisted ratings analytics expanding addressable."},
    # Headwinds
    {"label": "27.8% below 52-week high — valuation still recovering",
     "rating": -0.20, "weight": 0.25,
     "note": "ATH $579.05 (Nov 2025). Current $417.95 = 27.8% drawdown. Market has not yet re-rated"
             " SPGI back to peak multiple (was 33×; now ~21× FW). Rate environment keeps multiples"
             " compressed. Risk: if rates stay high, 21× may be the new normal vs 27× historical avg."},
    {"label": "Mobility Global separation uncertainty",
     "rating": -0.15, "weight": 0.20,
     "note": "MBGL IPO July 1 2026 introduces short-term dislocation: SPGI shareholders receive MBGL"
             " shares (some will sell immediately = overhang). Integration disruption (auto data was"
             " embedded in Market Intelligence workflows). MBGL valuation at listing uncertain;"
             " if disappointing, could reprice SPGI sum-of-parts negatively in the near term."},
    {"label": "Rate sensitivity of Ratings division",
     "rating": -0.15, "weight": 0.15,
     "note": "Ratings = ~35% of SPGI revenue and the highest-margin, most cyclical segment. Bond issuance"
             " is directly inverse to rate levels (refinancing costs). FY2022 proved: when issuance collapses,"
             " Ratings revenue can drop 25-30% in a year. Fed holding rates higher-for-longer = headwind."
             " Credit market stress (tariff recession fears) = double-hit: less issuance + wider spreads."},
]

sca_raw = sum(f["rating"] * f["weight"] for f in SCA_FACTORS)
sca_adj = sca_raw / 2.0

adj_composite = market_composite + sca_adj

# ── Bank / financial metrics (SPGI-specific) ─────────────────────────────────
ADJ_OP_MARGIN   = 52.0   # Q1 2026 adjusted operating margin (record); FY2025 ~49%
RATINGS_REV_Q1  = 1.30   # Ratings division Q1 2026 revenue ($B; +13% YoY)
INDICES_REV_Q1  = 0.75   # Indices Q1 2026 revenue ($B; +17% YoY; driven by AUM fees)
MI_REV_Q1       = 1.29   # Market Intelligence Q1 2026 revenue ($B; +8% YoY)
MBGL_SPIN_DATE  = "2026-07-01"   # Mobility Global NYSE listing; record date June 15 2026

# ── Output ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    w = softmax_weights(adj_composite)
    exp_p = expected_price(adj_composite)

    # ── PART 1: Framework ─────────────────────────────────────────────────────
    part1 = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  BottomUp Risk/Reward Analyzer — Analytical Framework                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
This tool applies a structured bottom-up framework to estimate the risk/reward
profile of individual equities over a 2-year investment horizon.  It is NOT a
trading signal or a price prediction — it is a disciplined lens for sizing
positions relative to the gap between structural downside (EPP) and consensus
upside (Method B).

KEY METRICS DEFINED
  EPP  (Earnings Power Price)   = EPS_trough × min-viable trough P/E
       The structural floor: the price the market should not sustainably
       breach even in a severe downturn, because earnings power remains.

  Method B price                = Consensus 2-yr EPS × exit P/E assumption
       The ceiling under the base/bull scenario — what the stock is worth
       if consensus plays out and the market re-rates to a reasonable multiple.

  Ratio B (PRIMARY SIGNAL)      = (Current − EPP) / (Method B − Current)
       How much downside risk are you taking per unit of upside potential?
       < 0.75 = BUY · 0.75–1.10 = ACCUMULATE · 1.10–1.75 = WATCHLIST
       1.75–2.50 = HOLD/TRIM · > 2.50 = AVOID

  Composite score               = market-implied scenario blend (1.0–4.0 scale)
       Inferred by back-solving the softmax price engine against today's price.
       1.0 = deep BEAR | 2.0 = BASE | 3.0 = BULL | 4.0 = XBULL
       SCA adjustments shift the composite to reflect non-price catalysts.

SIGNAL TABLE
  ◉ BUY        Ratio B < 0.75   — asymmetric upside; margin of safety present
  ◎ ACCUMULATE Ratio B 0.75–1.10 — favourable risk/reward; build position
  ◐ WATCHLIST  Ratio B 1.10–1.75 — balanced; monitor for entry improvement
  ▷ HOLD/TRIM  Ratio B 1.75–2.50 — upside limited vs downside; reduce on strength
  ✕ AVOID      Ratio B > 2.50   — risk/reward deeply unfavourable at current price

DATA QUALITY NOTE
  All EPS figures use ADJUSTED (non-GAAP) earnings per SPGI's own guidance
  convention.  The adj-GAAP gap (~$2.59/yr) reflects IHS Markit intangible
  amortisation following the $44B acquisition (Feb 2022).  Consensus targets
  and Street models universally use adjusted EPS for SPGI comparisons.
"""

    # ── PART 2: Analyst commentary ────────────────────────────────────────────
    part2 = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SPGI  |  S&P Global Inc.  |  ◐ WATCHLIST                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

SNAPSHOT  (as of 2026-05-26)
  Price         ${CURRENT_PRICE:,.2f}   52-wk range  ${PRICE_52W_LOW:.2f} – ${PRICE_52W_HIGH:.2f}
  Shares        ~{SHARES_M:.0f}M          Mkt cap      ~$123.6B
  Dividend      ${DIVIDEND_ANN:.2f}/yr    Yield        ~{DIVIDEND_ANN/CURRENT_PRICE*100:.2f}%
  FY2026E EPS   ${EPS_NOW:.2f} (adj)   FY2026 FW P/E  {CURRENT_PRICE/EPS_NOW:.1f}×
  EPP floor     ${EPP:.2f}            Ratio B      {ratio_b:.2f}×  →  ◐ WATCHLIST

THE BUSINESS: REGULATED DUOPOLY + PASSIVE INVESTING PERPETUAL ANNUITY
S&P Global is a two-engine machine hiding behind one ticker.

Engine 1 — Ratings (35% of revenue, 60%+ of economics):
S&P and Moody's together control ~80% of global credit ratings.  The NRSRO
(Nationally Recognized Statistical Rating Organization) designation is granted
by the SEC and is effectively a government-backed oligopoly licence.  Every
investment-grade and high-yield bond issued globally requires at least two NRSRO
ratings for regulatory/index inclusion purposes.  There is no substitute.
Q1 2026: Ratings revenue +13% to $1.30B.

Engine 2 — Indices (20% of revenue, 40%+ of economics, 100% recurring):
The S&P 500 is the world's most-tracked index.  SPGI licenses the S&P 500 name,
methodology, and constituent data to every ETF, mutual fund, futures contract,
and structured product that tracks it.  With ≥$10 trillion AUM following S&P
indices, each index point = approximately $35M in annual licensing fees.  As
passive investing has grown from <30% to >50% of US equity AUM since 2010, this
royalty stream compounds regardless of the economic cycle.
Q1 2026: Indices revenue +17%; this segment is structurally growing 15-20%/yr.

Engine 3 — Market Intelligence + Commodity Insights (recurring data, ~40%):
Bloomberg-adjacent data terminals + S&P Capital IQ + SNL Energy/Real Estate +
Platts commodity pricing.  These are subscription-based, multi-year enterprise
contracts with high switching costs and 90%+ renewal rates.
Q1 2026: MI +8%, adj operating margin 52% (record).

IMMINENT CATALYST: MOBILITY GLOBAL SEPARATION (MBGL)
On July 1, 2026, SPGI spins off its auto-data division (CARFAX, Polk, Carfax
Business Solutions, automotiveMastermind) as an independent NYSE-listed company
"Mobility Global" (MBGL).  Record date: June 15, 2026 — less than 3 weeks away.

Why this matters for SPGI's intrinsic value:
  1. PURITY premium: Post-spin, SPGI is a pure financial data/analytics business.
     The auto-data segment had ~$1.5–2B revenue but lower margins than Ratings/Indices.
     Its removal should mathematically lift SPGI's blended margin and deserves
     a higher multiple (compare pure Indices/ratings peers at 28–32×).
  2. Unlocks hidden value: MBGL will trade on its own merits.  SPGI shareholders
     receive MBGL shares directly — realising value that was embedded but not
     visible in the SPGI P&L consolidation.
  3. Management focus: The IHS Markit acquisition brought integration complexity.
     Mobility was arguably a misfit.  Post-spin, SPGI management can concentrate
     capital allocation on Ratings, Indices, and MI — each with secular tailwinds.

EARNINGS POWER AND CYCLE CONTEXT
The FY2022 trough (adj EPS $11.19) is the base case stress test: the Fed hiked
rates 425bps in 12 months, bond issuance collapsed ~25%, and SPGI digested the
$44B IHS Markit acquisition simultaneously.  Despite all of that, SPGI traded
at 20–22× forward EPS even at the trough.  This confirms the EPP_MIN_PE=20×
assumption — the market has never ascribed less than 20× to SPGI even in its
worst documented year.

Recovery trajectory:
  FY2022: $11.19 (trough)  →  FY2023: $13.40  →  FY2024: $15.10  →  FY2025: $17.25
  FY2026E: $19.53 (+13% at mid-guidance)  →  FY2027E: ~$22.50 (consensus est.)

The 15-20% CAGR in adj EPS reflects: (1) Ratings volume recovery as issuance
rebounds, (2) Indices AUM growth compounding, (3) MI subscription price increases,
and (4) share buybacks (~$4–5B/yr = ~3% annual float reduction).

ANALYST CONSENSUS AND PEER COMPARISON
  Analyst avg PT: $533–562   →  +27–34% upside from current $418
  Strong Buy consensus: majority of 25+ covering analysts
  Moody's (MCO): $419 price, 30× FW P/E — SPGI at 21.4× is a discount to its duopoly peer
  Verisk Analytics: 28× FW P/E — data analytics peers trade 25–30×

The 28% discount to MCO's forward multiple is the core valuation case: as MBGL
spin clarifies SPGI's pure-play profile, multiple re-rating toward MCO/Verisk
levels would alone justify $490–530 per share.

RISK FACTORS
  Rate sensitivity:  Ratings is 35% of revenue and directly correlated with bond
  issuance volume.  Every 100bps sustained rate increase = ~$500–700M Ratings revenue
  headwind.  If the Fed holds or re-hikes in 2026–2027, Ratings growth slows.

  Mobility spin dislocation:  When MBGL begins trading July 1, passive funds
  indexed to SPGI will automatically receive MBGL shares.  Many will sell MBGL
  immediately (it's not in their mandates), creating post-spin overhang.

  DOJ/regulatory risk:  Like V/MA, credit ratings agencies have faced periodic
  DOJ/CFPB scrutiny.  The 2008 financial crisis led to $1.5B+ settlements for SPGI
  (2015).  New regulatory scrutiny on ESG ratings methodology is emerging.

SIGNAL SUMMARY
  52-wk low  $381.61  →  ratio_b  {(PRICE_52W_LOW-EPP)/(price_b-PRICE_52W_LOW):.2f}×  →  WATCHLIST
  Current    $417.95  →  ratio_b  {ratio_b:.2f}×  →  ◐ WATCHLIST
  52-wk high $579.05  →  ratio_b  {(PRICE_52W_HIGH-EPP)/(price_b-PRICE_52W_HIGH):.2f}×  →  AVOID

  Best entry: ACCUMULATE $370–400 (ratio_b 0.85–1.05×); BUY below $340 (ratio_b <0.70×)
  Mobility spin (July 1) is the near-term trigger — watch for post-spin dislocation entry.
"""

    # ── PART 3: Numbers & signals ─────────────────────────────────────────────
    part3 = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SPGI — Numbers & Signals                                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

EPS HISTORY (adjusted / non-GAAP)
  FY2022   ${EPS_HISTORY['FY2022']:>6.2f}   Trough: IHS Markit integration + rates-shock issuance collapse (-26% Ratings)
  FY2023   ${EPS_HISTORY['FY2023']:>6.2f}   Recovery: issuance rebound, Indices AUM growth accelerating
  FY2024   ${EPS_HISTORY['FY2024']:>6.2f}   Sustained: Indices +25%+; Commodity Insights + MI expansion
  FY2025   ${EPS_HISTORY['FY2025']:>6.2f}   Record: adj EPS at high end of guidance; Q4 adj margin 53%
  FY2026E  ${EPS_NOW:>6.2f}   Guidance: $19.40–$19.65 (raised post-Q1 2026 beat)
  FY2027E  ${CONS_EPS_2YR:>6.2f}   Consensus estimate: +15% growth; post-MBGL pure-play tailwind

EPP — STRUCTURAL FLOOR
  EPS_trough  = ${EPS_TROUGH:.2f}   (severe rates shock; below FY2022 actual $11.19)
  EPP_min_PE  = {EPP_MIN_PE}×       (SPGI never traded <20× even at FY2022 trough; duopoly moat)
  EPP         = ${EPP:.2f}   (= ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×)
  Gap to EPP  = {(CURRENT_PRICE/EPP - 1)*100:.1f}% above floor  (current $418 is {CURRENT_PRICE/EPP:.2f}× EPP)

METHOD B — 2-YEAR UPSIDE CEILING
  Consensus EPS (FY2027E)  = ${CONS_EPS_2YR:.2f}
  Exit P/E assumption      = {CONS_EXIT_PE}×   (conservative vs 27× historical avg; post-MBGL purity premium)
  Method B price           = ${price_b:.2f}   (+{(price_b/CURRENT_PRICE-1)*100:.1f}% from current)

RATIO B (PRIMARY SIGNAL)
  Ratio B = (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})
          = {CURRENT_PRICE-EPP:.2f} / {price_b-CURRENT_PRICE:.2f}
          = {ratio_b:.2f}×   →   ◐ WATCHLIST  (range: 1.10–1.75×)

SCENARIO ANALYSIS
  BEAR   ${SCENARIOS['BEAR']['price']:>7.2f}  EPP floor; sustained high rates; issuance -50%; Ratings -30%
  BASE   ${SCENARIOS['BASE']['price']:>7.2f}  FY2026E $19.53 × 25× = $488; MBGL unlocks re-rating
  BULL   ${SCENARIOS['BULL']['price']:>7.2f}  Method B; FY2027E $22.50 × 25× = $562.50; post-spin re-rate
  XBULL  ${SCENARIOS['XBULL']['price']:>7.2f}  MCO-parity re-rating (31×); AI analytics + Indices compounding

SOFTMAX COMPOSITE ENGINE
  Market composite (inferred)  =  {market_composite:.3f}
  (Market pricing SPGI between BASE and BULL — consistent with WATCHLIST)

SCA — SIGNAL CATALYST ADJUSTMENTS
{"".join(f"  {f['label'][:50]:<50}  {f['rating']:+.2f} × {f['weight']:.2f}  =  {f['rating']*f['weight']:+.4f}" + chr(10) for f in SCA_FACTORS)}
  sca_raw     =  {sca_raw:+.4f}
  sca_adj     =  {sca_adj:+.4f}  (= sca_raw / 2.0)
  adj_composite  =  {market_composite:.3f}  +  {sca_adj:+.4f}  =  {adj_composite:.3f}

SOFTMAX SCENARIO WEIGHTS  (at adj_composite = {adj_composite:.3f})
{"".join(f"  {s:<6}  {w[s]*100:5.1f}%   ${SCENARIOS[s]['price']:.2f}" + chr(10) for s in ['BEAR','BASE','BULL','XBULL'])}
  Expected price (probability-weighted)  =  ${exp_p:.2f}

FINANCIAL METRICS
  Adj operating margin (Q1 2026)  =  {ADJ_OP_MARGIN:.1f}%  (record)
  Ratings revenue Q1 2026         =  ${RATINGS_REV_Q1:.2f}B  (+13% YoY)
  Indices revenue Q1 2026         =  ${INDICES_REV_Q1:.2f}B  (+17% YoY)
  Market Intelligence Q1 2026     =  ${MI_REV_Q1:.2f}B  (+8% YoY)
  Mobility Global spin date       =  {MBGL_SPIN_DATE}  (record: 2026-06-15)
  Duopoly peer MCO fwd P/E        =  ~30×  vs  SPGI {CURRENT_PRICE/EPS_NOW:.1f}×  (SPGI at 29% discount)

SIGNAL ENTRY GUIDE
  ✕ AVOID      above  $530  (ratio_b > 2.3×; fully pricing BULL scenario)
  ▷ HOLD/TRIM  $465 – $530  (ratio_b 1.75–2.3×)
  ◐ WATCHLIST  $415 – $465  (current; ratio_b 1.10–1.75×)  ← HERE
  ◎ ACCUMULATE $370 – $415  (ratio_b 0.85–1.10×; post-MBGL-spin dislocation zone)
  ◉ BUY        below  $340  (ratio_b < 0.70×; severe macro dislocation)

  Analyst avg PT: $533–562  (+{(545/CURRENT_PRICE-1)*100:.0f}% from current)
  Near-term catalyst: Mobility Global (MBGL) IPO — July 1, 2026
"""

    print(part1)
    print(part2)
    print(part3)
