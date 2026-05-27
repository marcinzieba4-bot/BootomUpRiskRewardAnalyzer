"""
pypl_signal_model.py — PayPal Holdings, Inc. (NASDAQ: PYPL)
Digital payments network: PayPal branded checkout, Venmo P2P, Braintree PSP, BNPL, Fastlane.
Signal framework: EPP floor + Method B + SCA softmax engine.
"""

import math

# ── LIVE PRICE (fetched before model construction) ──────────────────────────
CURRENT_PRICE = 44.16    # PYPL — fetched from Yahoo Finance / stockanalysis.com, 2026-05-27
# 52-wk range: $38.46 (Apr 2026 lows) – $79.50 (summer 2025 high)
# Market cap ~$38.9B; shares ~881M; P/E 8.3× GAAP; FCF yield ~13%+

TICKER        = "PYPL"
COMPANY       = "PayPal Holdings, Inc."
SHARES_M      = 881          # million shares; declining ~7-8%/yr via aggressive buybacks
DIVIDEND_ANN  = 0.56         # USD/yr; $0.14/qtr; recently initiated (Q1 2026); new capital return policy

# ── EPS CONVENTION ───────────────────────────────────────────────────────────
# Non-GAAP Adjusted EPS — PayPal's primary metric. Excludes stock-based compensation,
# restructuring charges, intangible amortisation. Under CEO Chriss (Sept 2023), PayPal
# changed non-GAAP definition to include some restructuring charges — making FY2024
# the reported trough year. FY2025 returned to cleaner run-rate. GAAP EPS is close to
# non-GAAP in FY2025 (SBC relatively small vs. earnings base after years of buybacks).
# CAUTION: Q1 2026 GAAP EPS fell -6% while non-GAAP +1% — impairments re-emerging.

EPS_HISTORY = {
    "FY2022": 4.13,   # growth decelerating; eBay Marketplaces wind-down; rising rates
    "FY2023": 4.95,   # +20% approx; buybacks accelerating; CEO Schulman final year
    "FY2024": 4.03,   # CEO Chriss transition; 9% workforce cut; restructuring in non-GAAP;
                       #   transitional trough; take-rate compression accelerating
    "FY2025": 5.46,   # buyback-driven recovery; ~78M shares retired in LTM;
                       #   float income tailwind (higher rates on $25B+ customer balances);
                       #   Venmo +14% TPV; BNPL +34%; Q4 adj FCF $2.3B/quarter
}

# Q1 2026: non-GAAP EPS $1.34 (+1% YoY); GAAP EPS fell -6%; revenue $8.35B (+7%); TPV $463.96B (+11%)
# FY2026 guidance: non-GAAP EPS "slightly negative to slightly positive" vs FY2025
# Transaction margin dollars: "roughly flat or slightly down" — core margin under pressure
# Venmo TPV +14% YoY (6th consecutive double-digit quarter); Pay with Venmo +23%; BNPL +34%

EPS_NOW       = 5.42     # FY2026E analyst consensus (range $5.11–$6.13)
EPS_TROUGH    = 3.50     # severe scenario: accelerated branded-checkout erosion;
                          #   take-rate compression beyond guidance; FCF declines to ~$3B;
                          #   shares still ~800M from continued buybacks at lower price
EPP_MIN_PE    = 10        # fintech under competitive pressure; real FCF ($5B+) + Venmo
                          #   network (90M users) + Braintree enterprise contracts floor the stock;
                          #   same as FISV restructuring (10×) but FISV has contracted B2B
                          #   revenue; PYPL checkout more exposed to consumer behaviour
EPP           = EPP_MIN_PE * EPS_TROUGH   # = $35.00

CONS_EPS_2YR  = 5.92     # FY2027E analyst consensus (range $5.16–$6.78)
CONS_EXIT_PE  = 14        # cautious; stagnating fintech with buyback-driven EPS;
                          # below historical 20×+ but reflects lack of organic growth momentum;
                          # if Venmo/Fastlane inflects, higher multiple possible
price_b       = CONS_EPS_2YR * CONS_EXIT_PE   # = $82.88

ratio_b       = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
epp_gap_pct   = (CURRENT_PRICE - EPP) / EPP * 100

# Scenario prices
scenarios = {
    "BEAR":  35,     # EPP; franchise erosion; FCF declines to ~$3B; 10× trough floor
    "BASE":  58,     # FY2026E $5.42 × 10.7×; analyst consensus zone ($55–58); minimal re-rating
    "BULL":  83,     # Method B; FY2027E $5.92 × 14×; buyback flywheel + Venmo monetisation
    "XBULL": 120,    # $5.92 × 20×; Fastlane breakthrough + Venmo full monetisation + re-rate
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
    ("FCF ~$5-6B/yr on $39B market cap = 13-15% FCF yield; $1.5B/quarter buybacks "
     "retire 7-8% of shares/yr at 8× EPS — compounding even with zero revenue growth",
     +0.35, 0.25),
    ("Venmo 90M+ US users: TPV +14% 6th consecutive double-digit quarter; "
     "Pay with Venmo +23%; take rate 0.9% vs 2.2% branded = $4.3B annual monetisation gap",
     +0.25, 0.20),
    ("Fastlane guest checkout + BNPL +34%: nascent growth options with 430M active "
     "account base; Fastlane expanding internationally; conversion uplift data emerging",
     +0.15, 0.15),
    ("Branded checkout structural erosion: Apple Pay/Google Pay/Stripe/Shopify taking "
     "share; transaction margin dollars flat per FY2026 guide; take-rate declining annually",
     -0.35, 0.30),
    ("EPS 'growth' entirely from buybacks since FY2022: $4.13→$5.46 = share-count "
     "reduction, not operating leverage; CEO Chriss restructuring yet to show margin gains",
     -0.30, 0.20),
    ("Near 52-wk low; 86% below $309 ATH (July 2021); persistent multi-year downtrend; "
     "GAAP EPS fell -6% Q1 2026 vs non-GAAP +1% — impairments/charges re-emerging",
     -0.10, 0.10),
]

sca_raw = sum(score * weight for _, score, weight in sca_items)
sca_adj = sca_raw / 2.0
adj_composite = market_composite + sca_adj

adj_weights    = softmax_weights(adj_composite)
expected_px    = expected_price(adj_composite)

# ── SIGNAL ───────────────────────────────────────────────────────────────────
if   ratio_b < 0.75:  signal = "◉ BUY"
elif ratio_b < 1.10:  signal = "◎ ACCUMULATE"
elif ratio_b < 1.75:  signal = "◐ WATCHLIST"
elif ratio_b < 2.50:  signal = "▷ HOLD/TRIM"
else:                  signal = "✕ AVOID"

# ── OUTPUT ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    SEP  = "=" * 70

    print(SEP)
    print("PAYPAL HOLDINGS, INC. (PYPL) — SIGNAL MODEL")
    print("Digital payments: PayPal, Venmo, Braintree, BNPL, Fastlane. 430M accounts.")
    print(SEP)

    print("""
SIGNAL FRAMEWORK — METHOD B + SCA ENGINE
─────────────────────────────────────────
EPP  = EPS_TROUGH × EPP_MIN_PE          (structural floor; non-GAAP adj EPS basis)
Ratio B = (Price − EPP) / (price_b − Price)

PYPL EPS convention: Non-GAAP Adjusted EPS. Excludes SBC, restructuring charges,
intangible amortisation. Under CEO Chriss (Sept 2023), PayPal changed non-GAAP
definition to include some restructuring — making FY2024 the reported trough year.
CAUTION: Q1 2026 GAAP EPS fell -6% while non-GAAP +1% — watch GAAP trend closely.

SIGNAL THRESHOLDS
  Ratio B < 0.75   →  ◉ BUY
  0.75 – 1.10      →  ◎ ACCUMULATE
  1.10 – 1.75      →  ◐ WATCHLIST
  1.75 – 2.50      →  ▷ HOLD/TRIM
  > 2.50           →  ✕ AVOID

EPP_MIN_PE = 10×  rationale:
  PayPal is a fintech under real competitive pressure — not a temporary operational
  disruption but structural market-share erosion from Apple Pay, Google Pay, Stripe,
  and Shopify. However, the floor is protected by genuine assets:
  (1) $5-6B annual free cash flow — does NOT disappear even with branded share loss
  (2) Venmo's 90M+ US user network — sticky P2P with growing commerce use
  (3) Braintree enterprise contracts — lower margin but durable volume
  (4) 430M active global accounts — large embedded base with switching costs
  10× of conservative trough EPS ($3.50) = $35 EPP. At $44.16 = only 26% above floor —
  a THIN buffer that accurately reflects the competitive overhang.
  Note: FISV (also 10×) has contracted B2B revenue from banks that cannot easily switch.
  PYPL's consumer checkout is more vulnerable to behaviour change.
""")

    print("PAYPAL HOLDINGS (PYPL) — THE FCF FORTRESS PRICED AT 8× EARNINGS")
    print("=" * 70)

    print("""
BUSINESS OVERVIEW
─────────────────
PayPal Holdings was spun off from eBay in July 2015. It is the world's largest
digital payments network by account base (430M active accounts, $1.9T annual TPV).
Headquarters: San Jose, CA. CEO: Alex Chriss (since September 2023, formerly
President of Intuit Small Business and QuickBooks). PayPal pioneered online payments
(1998) and remains a default brand for digital wallets globally — but faces the most
significant competitive pressure in its history from OS-native wallets.

FOUR REVENUE STREAMS
─────────────────────
  PAYPAL BRANDED CHECKOUT      ~50% of revenue  (HIGH MARGIN; AT RISK)
  ─────────────────────────────────────────────
  The blue PayPal button at checkout. 2.2% take rate. Consumer trust for purchase
  protection, dispute resolution, and fraud protection.
  THE FRANCHISE AT RISK from Apple Pay/Google Pay convenience advantage.
  Q1 2026: branded checkout growing but slower than total TPV (mix dilution).

  BRAINTREE / PSP (Unbranded)  ~30% of revenue  (LOW MARGIN; GROWING)
  ─────────────────────────────────────────────
  Unbranded payment processing for Airbnb, Uber, large merchants, and SMBs.
  Take rate: ~0.4-0.6% — far lower than branded. Growing double-digits but
  diluting overall economics as it grows faster than branded.

  VENMO                        ~10% of revenue  (THE HIDDEN ASSET)
  ─────────────────────────────────────────────
  America's #1 P2P payments app. 90M+ accounts, $330B+ annual TPV.
  Currently undermonetised at 0.9% take rate (vs PayPal 2.2% branded).
  Venmo is accelerating: Pay with Venmo merchant TPV +23% Q1 2026;
  Venmo Debit/Credit Card; BNPL integration. Six consecutive double-digit quarters.
  The take-rate gap (0.9% → 2.2%) on $330B+ TPV = $4.3B annual revenue opportunity.

  OTHER (BNPL, FASTLANE, XOOM) ~10% of revenue  (EMERGING)
  ─────────────────────────────────────────────
  Buy Now Pay Later: TPV +34% Q1 2026 — meaningful volume growth.
  Fastlane: one-click guest checkout — PayPal's answer to Apple Pay convenience.
            Early data shows 40%+ conversion lift vs. traditional guest checkout.
            Expanding internationally as of Q1 2026.
  Xoom: international P2P money transfer.

THE VALUATION CASE: 8× EARNINGS ON $5.7B OF BUYBACKS
─────────────────────────────────────────────────────
At $44.16:
  Non-GAAP P/E on FY2026E $5.42:   8.1×  (vs any fintech peer at 15-25×)
  GAAP P/E:                         8.3×  (GAAP and non-GAAP converged in FY2025)
  FCF yield:                      ~13-15% (free cash flow $5-6B / market cap $39B)
  Buyback yield:                    ~15%  ($6B annualised buybacks on $39B market cap)
  Share count decline:              ~7-8%/yr (881M today from ~1.16B in 2020)

The buyback math is compelling even without any operational improvement:
  FY2027E EPS $5.92 = already priced in at 14× = $83 BULL case
  If EPS stays flat but share count declines 7%/yr, EPS self-compounds to:
    2027: $5.92 → 2028: $6.35 → 2029: $6.80 → at 10× P/E = $68 (just from buybacks)
  This is the FCF/buyback floor that makes PYPL a BUY despite operational uncertainty.

TAKE-RATE COMPRESSION: THE CORE CONCERN
─────────────────────────────────────────
FY2026 guidance: transaction margin dollars "roughly flat or slightly down."
Revenue growing 7% but gross profit NOT growing = TPV mix shifting to unbranded.
  Branded checkout take rate: 2.2%   (declining slowly)
  Braintree/PSP take rate:    0.4-0.6% (growing in volume mix)
  Blended result: each 1pp shift from branded to unbranded = ~$19B in affected revenue
  → ~$30-32M annual gross profit loss per basis point of blended take rate decline.

Apple Pay, Google Pay, Shopify Pay, and Stripe are the primary share-takers.
Apple Pay in particular offers zero-friction biometric authentication — no password,
no redirect. At iPhone's 55%+ US market share, this is a structural competitive moat
that PayPal cannot directly replicate.

CEO ALEX CHRISS: THE TURNAROUND
──────────────────────────────────
Alex Chriss joined from Intuit in September 2023. Key actions under his tenure:
  1. 9% workforce reduction (Jan 2024) + additional restructuring → cost base lower
  2. Focus on "profitable growth" — fewer large-merchant price-competitive Braintree deals
  3. Launched Fastlane (one-click guest checkout) to compete on convenience
  4. Venmo monetisation acceleration: push merchant checkout, debit/credit card use
  5. PayPal Everywhere: 3% cashback card to drive branded checkout habit
  6. Advertising/data platform: PayPal's 430M account purchase data = targeting asset

FY2025 results show cost savings flowing through (EPS $5.46 vs $4.03 in FY2024).
However, Q1 2026 non-GAAP EPS barely grew (+1%) and GAAP fell -6%: no operating
leverage yet. The restructuring has stabilised costs but not reversed take-rate erosion.

Q1 2026 RESULTS — THE TENSION
────────────────────────────────
  Revenue:             $8.35B  (+7% YoY)        ← volumes growing
  TPV:               $463.96B  (+11% YoY)        ← strong
  Non-GAAP EPS:          $1.34  (+1% YoY)        ← barely growing
  GAAP EPS:           fell -6%  YoY              ← warning sign
  Transaction margin:  flat/slightly down         ← core pressure
  Venmo TPV:             +14%                    ← bright spot
  Pay with Venmo:        +23%                    ← bright spot
  BNPL TPV:             +34%                     ← bright spot
  Fastlane:           expanding internationally  ← early stage

The tension: volume metrics are strong (+11% TPV) but economics are stagnant
(transaction margin flat). Revenue grows but profit doesn't follow — classic
symptom of mix shift toward lower-margin processing.

VENMO MONETISATION: THE UPSIDE OPTION
──────────────────────────────────────
Venmo's 90M US accounts are a defensible and undermonetised asset:
  Current Venmo take rate: ~0.9%
  PayPal branded take rate: ~2.2%
  Gap: 1.3pp × Venmo annual TPV est. $330B = $4.3B annual revenue opportunity

  If Venmo take rate reaches 1.5% (still 0.7pp below PayPal branded):
    Additional annual revenue: +0.6pp × $330B = $1.98B → +$1.80 EPS (20% margin)
    At 14× multiple: +$25/share upside from Venmo monetisation alone

  This is optionality that the current 8× multiple prices at ZERO.
  Pay with Venmo +23% Q1 2026 = the monetisation is working — slowly.

FASTLANE: CONVERSION REINVENTION OPTION
─────────────────────────────────────────
Guest checkout is ~50%+ of ecommerce transactions. Apple Pay wins here on
convenience (tap, FaceID, done). Fastlane stores card/shipping for PayPal wallet
users AND guest buyers — auto-fills at any Fastlane-enabled merchant.
  Early data: 40%+ conversion improvement vs. traditional guest checkout
  Expanding to international markets Q1 2026
  Competing with Stripe Link (Stripe's equivalent product)
  Key risk: needs merchant adoption; PayPal's relationship with large merchants

If Fastlane captures meaningful share of guest checkout → revenue without incremental
customer acquisition cost → high incremental margins.

KEY RISKS
──────────
  1. FRANCHISE EROSION: Apple Pay/Google Pay gaining share faster than projected;
     branded checkout revenue line could decline while Braintree grows (net margin loss).
  2. FCF COMPRESSION: Take-rate erosion beyond guidance → FCF declines from $5-6B
     toward $3-4B → buyback capacity shrinks → EPS compounding slows.
  3. GAAP vs NON-GAAP DIVERGENCE: Q1 2026 GAAP fell -6% vs non-GAAP +1%.
     If impairments or asset write-downs persist, true economic earnings may be lower.
  4. VENMO MONETISATION FAILURE: Venmo users resistant to fees; Gen Z may not
     adopt "Pay with Venmo" at merchant checkout if Apple Pay is easier.
  5. CEO EXECUTION: Chriss 2.5 years in without demonstrable margin expansion.
     If FY2026-2027 EPS growth is entirely from buybacks, multiple stays depressed.
  6. VALUE TRAP: A company generating 13% FCF yield but buying back shares of a
     structurally declining franchise is ultimately just liquidating itself — the
     question is HOW SLOWLY the franchise erodes vs. how fast buybacks compound EPS.

SUMMARY VERDICT
───────────────
PayPal at $44.16 is trading at 8.1× non-GAAP EPS and 13-15% FCF yield. Even as a
"value trap" scenario with zero organic growth, the buyback math makes the stock a
BUY: share count shrinking 7-8%/yr compounds EPS to ~$8-9 by 2029 before any
business improvement. The bears are right about branded-checkout erosion; the bulls
are right that Venmo (90M users; 1.3pp take-rate gap) and Fastlane represent growth
options not priced in at 8×. The Q1 2026 GAAP EPS decline is the key watch item.
BUY below $55. Moderate conviction on the FCF/buyback floor; lower conviction on the
operational turnaround. This is NOT a high-quality franchise BUY (like MRSH or SCHW);
it is a deep-value / capital-return BUY with meaningful downside execution risk.
""")

    print("KEY METRICS")
    print(f"  Current price (fetched)          = $  {CURRENT_PRICE:.2f}")
    print(f"  52-week range                    = $38.46 – $79.50")
    print(f"  Market cap                       = ~$38.9B")
    print(f"  Non-GAAP P/E on FY2026E ${EPS_NOW:.2f}  = {CURRENT_PRICE/EPS_NOW:.1f}×  (vs fintech peers 15-25×; near-trough multiple)")
    print(f"  Non-GAAP P/E on FY2027E ${CONS_EPS_2YR:.2f}  = {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (cheap on 2-yr view)")
    print(f"  Dividend (annual)                = ${DIVIDEND_ANN:.2f}  (yield {DIVIDEND_ANN/CURRENT_PRICE*100:.2f}%; recently initiated Q1 2026)")
    print(f"  Buyback pace                     = ~$6B/yr  (15% of market cap; 7-8% share count decline)")
    print(f"  Active accounts                  = 430M+  (global; +0.1% sequential Q3 2025 — stagnant)")
    print(f"  Venmo accounts                   = 90M+  (US P2P; +14% TPV; undermonetised at 0.9% rate)")
    print(f"  Q1 2026 TPV                      = $463.96B  (+11% YoY)")
    print(f"  Q1 2026 revenue                  = $8.35B  (+7% YoY)")
    print(f"  FY2026 transaction margin guide  = flat/slightly down  (core economics under pressure)")
    print(f"  Analyst avg price target         = ~$55-58  (consensus Hold; wide range $32-$105)")
    print()

    print("NON-GAAP ADJUSTED EPS HISTORY")
    for yr, val in EPS_HISTORY.items():
        print(f"  {yr}  ${val:.2f}")
    print(f"  FY2026E ${EPS_NOW:.2f}  (consensus; mgmt guides 'roughly flat'; Q1 2026 = $1.34 × 4 = $5.36)")
    cagr = ((EPS_HISTORY["FY2025"]/EPS_HISTORY["FY2022"])**(1/3)-1)*100
    print(f"  FY2022–FY2025 CAGR: {cagr:.1f}%/yr  (driven primarily by share reduction, not operating leverage)")
    print()

    print("EPP CALCULATION")
    print(f"  EPS_TROUGH × EPP_MIN_PE  =  ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×  =  ${EPP:.2f}")
    print(f"  (FCF floor; accelerated erosion; buybacks slow as FCF declines to ~$3B)")
    print(f"  THIN BUFFER: current ${CURRENT_PRICE:.2f} is only +{epp_gap_pct:.1f}% above EPP — reflects real franchise risk")
    print()

    print("METHOD B  (2-year forward)")
    print(f"  CONS_EPS_2YR × CONS_EXIT_PE  =  ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×  =  ${price_b:.2f}")
    print()

    print("RATIO B  (PRIMARY SIGNAL)")
    print(f"  (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})")
    print(f"  = ${CURRENT_PRICE - EPP:.2f} / ${price_b - CURRENT_PRICE:.2f}")
    print(f"  = {ratio_b:.3f}×   →   {signal}")
    print(f"  EPP gap: +{epp_gap_pct:.1f}% above structural floor  (THIN — reflects competitive overhang)")
    print()

    print("SCENARIO PRICES")
    for name, price in scenarios.items():
        print(f"  {name:<8} ${price:>7.2f}   ", end="")
        if name == "BEAR":
            print("EPP; FCF declines to ~$3B; franchise erosion accelerates beyond guidance")
        elif name == "BASE":
            print("FY2026E $5.42 × 10.7×; analyst consensus zone; minimal re-rating from 8×")
        elif name == "BULL":
            print("Method B; FY2027E $5.92 × 14×; buyback flywheel + Venmo monetisation")
        else:
            print("Fastlane + Venmo breakthrough; $5.92 × 20×; full turnaround re-rate")
    print()

    print("SOFTMAX COMPOSITE ENGINE")
    print(f"  Market composite (inferred)  =  {market_composite:.3f}")
    print(f"  (Market near BEAR zone — pricing structural decline and ignoring FCF/buyback floor)")
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
    print(f"  (Net slightly negative SCA: headwinds outweigh near-term catalysts; cheap but re-rating uncertain)")
    print()

    print("SOFTMAX SCENARIO WEIGHTS  (at adj_composite = {:.3f})".format(adj_composite))
    for name, w in adj_weights.items():
        print(f"  {name:<8}  {w*100:5.1f}%   ${scenarios[name]:.2f}")
    print()
    print(f"  Expected price (probability-weighted)  =  ${expected_px:.2f}")
    print()

    print("BUSINESS METRICS")
    print(f"  Total payment volume Q1 2026    = $463.96B  (+11% YoY; growing strongly)")
    print(f"  Active accounts                 = 430M+  (stagnant +0.1% sequential; a concern)")
    print(f"  Venmo TPV growth Q1 2026        = +14%  (6th consecutive double-digit quarter)")
    print(f"  Pay with Venmo (merchant)       = +23%  (monetisation accelerating)")
    print(f"  BNPL TPV growth Q1 2026         = +34%  (strong growth; crowded market)")
    print(f"  Buyback LTM (through Q3 2025)   = $5.7B  (~78M shares; declining share base)")
    print(f"  Share count decline             = ~7-8%/yr  (881M now; from 1.16B in 2020)")
    print(f"  Venmo take rate                 = ~0.9%  (vs PayPal branded 2.2%; $4.3B gap)")
    print(f"  FY2026 transaction margin guide = roughly flat/slightly down  (core stagnant)")
    print(f"  ATH (July 2021)                 = $309  (current $44 = 86% below ATH)")
    print()

    print("SIGNAL ENTRY GUIDE")
    def threshold_price(rb):
        return (EPP + rb * price_b) / (1 + rb)
    p_buy   = threshold_price(0.75)
    p_watch = threshold_price(1.10)
    p_hold  = threshold_price(1.75)
    p_avoid = threshold_price(2.50)
    print(f"  ✕ AVOID      above  ${p_avoid:.0f}  (ratio_b > 2.50×; 52-wk high $79.50 = extreme AVOID)")
    print(f"  ▷ HOLD/TRIM  ${p_hold:.0f} – ${p_avoid:.0f}  (ratio_b 1.75–2.50×)")
    print(f"  ◐ WATCHLIST  ${p_watch:.0f} – ${p_hold:.0f}  (ratio_b 1.10–1.75×)")
    print(f"  ◎ ACCUMULATE ${p_buy:.0f} – ${p_watch:.0f}  (ratio_b 0.75–1.10×; analyst avg PT $55-58 ≈ zone)")
    print(f"  ◉ BUY        below  ${p_buy:.0f}  (ratio_b < 0.75×)  ← current ${CURRENT_PRICE:.2f}  BUY")
    print()
    print(f"  52-wk low $38.46 = extreme BUY (ratio_b 0.10×); near EPP $35; hard floor.")
    print(f"  52-wk high $79.50 = deep AVOID (ratio_b 7.0×); market over-optimistic at $79.")
    print(f"  Analyst avg PT $55-58 ≈ ACCUMULATE zone: consistent with 8× → 10× modest re-rating.")
    print(f"  EPP gap only +{epp_gap_pct:.1f}%: THINNEST buffer in coverage — genuine franchise risk.")
    print(f"  KEY WATCH: Transaction margin dollar growth/decline Q2 2026 — the defining metric.")
    print(f"  GAAP vs non-GAAP divergence: GAAP fell -6% Q1 2026 — impairments/charges re-emerging.")
    print(f"  Venmo take-rate progress: 0.9%→1.2%+ in next 4 quarters = re-rate trigger.")
    print(f"  CAVEAT: FCF/buyback BUY, not a high-quality franchise BUY. Requires either")
    print(f"  (a) multiple re-rating from 8× or (b) Venmo/Fastlane operating inflection.")
