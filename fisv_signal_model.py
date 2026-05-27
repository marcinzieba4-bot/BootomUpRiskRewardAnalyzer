"""
FISERV INC. (FISV) — Bottom-Up Risk/Reward Signal Model
=========================================================
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

FISV EPS convention: Adjusted EPS (non-GAAP). Excludes amortisation of
acquired intangibles (large due to First Data / Clover acquisitions), M&A
transaction costs, and restructuring charges. Adjusted EPS is the metric
used by management, analysts, and in guidance. GAAP EPS is much lower.

SIGNAL THRESHOLDS
  Ratio B < 0.75   →  ◉ BUY
  0.75 – 1.10      →  ◎ ACCUMULATE
  1.10 – 1.75      →  ◐ WATCHLIST
  1.75 – 2.50      →  ▷ HOLD/TRIM
  > 2.50           →  ✕ AVOID

EPP_MIN_PE = 10×  rationale:
  Fiserv operates financial plumbing for ~2,500 US banks/credit unions (10-15+
  year contracts) + Clover merchant platform. Core Financial Solutions revenue
  is highly recurring and would survive even a severe downturn. However, the
  company is in active restructuring with new CFO (Paul Todd, Oct 2025) and
  co-presidents (Dec 2025). Argentina exposure creates real tail risk. 10×
  reflects a meaningful discount to stable fintech (15-18×); above commercial
  banks (9×) given the recurring technology contract base. At trough adj EPS
  $4.50 (Argentina permanent + merchant collapse scenario): floor = $45.
"""

# ── PART 2: ANALYST COMMENTARY ───────────────────────────────────────────────

COMMENTARY = """
FISERV INC. (FISV) — THE FALLEN FINTECH: ARGENTINA CRISIS MEETS CHEAP MULTIPLE
═════════════════════════════════════════════════════════════════════════════════

BUSINESS OVERVIEW
─────────────────
Fiserv is a $21B-revenue financial technology company split into two segments:

  Financial Solutions   ~$10.5B revenue;  ~40%+ adj margin
    ● Core account processing for ~2,500 US banks & credit unions
    ● Digital banking (online/mobile), fraud/risk, card issuing
    ● Very high retention (switching cost = multi-year migration projects)
    ● Organic growth: +2-3% annually; predictable and recurring

  Merchant Solutions    ~$10.5B revenue;  ~26-34% adj margin (compressed)
    ● Clover® POS/payments platform: ~50M small-business merchants globally
    ● Payment acceptance (acquiring), e-commerce, LatAm operations
    ● Argentina operations (significant): acquiring + FX float income
    ● Growth engine — but also the source of the 2025 crisis

WHAT HAPPENED: THE OCTOBER 2025 CATASTROPHE
─────────────────────────────────────────────
On October 29, 2025, Fiserv cut FY2025 guidance from $10.15-$10.30 adj EPS
→ $8.50-$8.60. The stock fell 44% in a single session — its worst day ever.
Total decline from ATH: 75% ($237.79 → $52 low).

Two compounding triggers:

  1. ARGENTINA FX DEVALUATION (April 14, 2025)
     Argentina's government removed currency controls, causing an immediate
     ~25% peso devaluation. Fiserv recognised a large one-time FX loss on
     the remeasurement of Argentina's monetary assets. But the more damaging
     effect was structural: Fiserv had been earning significant float/interest
     income on Argentine peso balances in a high-inflation environment. When
     inflation + interest rates collapsed post-liberalisation, that income
     stream evaporated almost overnight.

  2. MERCHANT SOLUTIONS MARGIN COMPRESSION
     Adj operating margin in Merchant Solutions fell from ~34% (2023) →
     ~26% (2025-2026). Causes: Argentina income loss, competitive pressure on
     Clover pricing, and increased technology investment. This compressed
     consolidated adj margins meaningfully — hence the EPS reset.

LEADERSHIP REBUILDING: NEW TEAM IN PLACE
──────────────────────────────────────────
The old guard has been replaced:
  CFO       Paul Todd (joined Oct 31, 2025) — ex-CFO of Global Payments and
            TSYS; deeply experienced in merchant payments specifically
  Co-Pres.  Takis Georgakopoulos — Merchant Solutions + Technology (Dec 2025)
  Co-Pres.  Dhivya Suryadevara — Financial Solutions + Sales + Operations (Dec 2025)
  Board     Shaken up simultaneously (audit committee chair replaced Jan 2026)

"One Fiserv" action plan (5 pillars):
  1. Client-first mindset
  2. Build preeminent small-business platform via Clover
  3. Create differentiated platforms in finance + commerce
  4. Deliver operational excellence enabled by AI
  5. Disciplined capital allocation long-term

This is not a company in disarray — it's a company that recognised the
problem, replaced leadership swiftly, and has a concrete restructuring plan.
The CFO change in particular is a strong signal: Paul Todd ran merchant
payments at Global Payments and knows exactly how to fix this.

Q1 2026 RESULTS — STABILISATION SIGNAL
────────────────────────────────────────
Reported May 5, 2026:
  Adj EPS:             $1.79  (beat consensus $1.58 by +13.3%)
  Revenue:             $5.03B  (beat $4.74B estimate by +6.1%)
  Adj operating margin: 29.7%
  FY2026 guidance:      Reaffirmed $8.00–$8.30 adj EPS
  Organic revenue:      -3.6% YoY (lapping Argentina comparison period)

The Q1 beat and guidance reaffirmation is the KEY signal. The market was
pricing in another guidance cut. Instead, FISV delivered a 13% beat and
held guidance. The "anniversary" of the Argentina crisis is Q2 2026, after
which organic growth comps should normalise.

THE VALUATION PARADOX: 7× FORWARD EARNINGS
────────────────────────────────────────────
At $57.13:
  FW P/E on FY2026E $8.15:   7.0×  (vs historical 25-40×; vs S&P 500 ~22×)
  P/S ratio:                  ~1.4×  (vs 5-10× historical premium fintech)
  Market cap:                 $29.95B  (vs $21B revenue = barely 1.4× sales)

For context — FISV's own P/E history:
  2019-2021:  25-35× adj EPS  (post First Data acquisition premium)
  2022-2024:  20-28× adj EPS  (normalisation; still premium)
  Current:     7.0× adj EPS   (crisis-level; priced like a bank, not a fintech)

At 7× earnings, the market is pricing in:
  a) The Argentina situation is PERMANENT (it's not — economies normalise)
  b) Merchant margins NEVER recover from 26% (unlikely; management committed)
  c) "One Fiserv" restructuring FAILS (possible but not base case with new team)

THE CORE BULL CASE
───────────────────
Financial Solutions (~50% of revenue) is:
  ✓ Completely untouched by Argentina
  ✓ Growing organically 2-3% with very high margins
  ✓ 2,500 US bank/CU contracts; multi-year switching friction
  ✓ This segment alone justifies large portion of current market cap

Clover platform:
  ✓ ~50M merchant devices globally; fastest-growing SMB payments platform
  ✓ Net payment volume through Clover growing 15-20% annually
  ✓ The platform has enormous long-term value even at temporarily compressed margins

Argentina:
  ✓ The devaluation was a ONE-TIME event (peso reset)
  ✓ As Argentina's economy stabilises (Milei reform trajectory), underlying
    payment volumes will resume growth; FX income will normalise at new levels
  ✓ The float income that was LOST is unlikely to return, but this is now
    priced into the guidance reset; no more negative surprise from this

Multiple recovery:
  ✓ Even recovering to 15-16× adj EPS on $9.00 FY2027E = $135-144/share
  ✓ Analyst avg PT $70.15 (range $40-115) represents deeply cautious consensus
  ✓ Any positive guidance revision drives massive stock upside from 7× base

PEER COMPARISON
────────────────
  FIS (Fidelity National): Similar restructuring (WorldPay debacle); similar
    deep value at lows; now recovering. FISV on the same path.
  Jack Henry (JKHY): ~31× FY2027E EPS — the premium for "no drama" core
    banking. FISV has the same Financial Solutions business at 7×.
  PayPal (PYPL): ~15× FW EPS. FISV's merchant platform (Clover) is arguably
    better positioned for SMBs than PayPal at a fraction of the multiple.

RISKS
──────
  1. ANOTHER GUIDANCE CUT: Q1 was $1.79, full year $8.00-8.30 → implies avg
     Q2-Q4 of ~$2.07/quarter. This seems achievable but Q2 2026 will be the
     first "clean" Argentina comparison quarter — watch carefully.
  2. MERCHANT MARGINS: If Merchant margins stay at 26% (vs 34% target),
     long-term EPS power is structurally lower than pre-crisis.
  3. COMPETITIVE PRESSURE: Toast, Square/Block, and Stripe are all competing
     for the SMB market. Clover is losing some deals at the high end.
  4. CAPITAL ALLOCATION: With buybacks now less likely (focus on balance sheet),
     EPS growth from share count reduction is slower.
  5. TRUST DEFICIT: Took from $237 ATH to $57 in 8 months. Institutional
     investors need multiple quarters of execution before returning.

SIGNAL COMPARISON
──────────────────
  FISV at $57: ◉ BUY — 75% below ATH, 7× FW earnings, EPP floor $55;
               the classic "when the bad news is fully priced in" setup
  V / MA:       AVOID / HOLD — premium payment networks at 30-35× FW EPS

SUMMARY VERDICT
───────────────
FISV is the classic "fallen quality" investment situation. A dominant
financial infrastructure company (stable core banking contracts, Clover
merchant platform) hit by a single exogenous event (Argentina FX) that has
been fully recognised, guided through, and is now lapping. At 7× forward
earnings with new leadership in place, Q1 beat, and guidance reaffirmed,
the risk/reward is highly asymmetric. Even a modest re-rating to 14-15× on
FY2027E recovery earnings yields +130-150% returns. BUY.
"""

# ── PART 3: NUMBERS & SIGNAL ─────────────────────────────────────────────────

import math

# ── Live price (MANDATORY — fetched from internet) ──
CURRENT_PRICE = 57.13   # FISV — Google Finance / search results, 2026-05-27 (last close May 22)

PRICE_52W_LOW  = 52.17
PRICE_52W_HIGH = 177.36
ATH_PRICE      = 237.79   # March 3, 2025 — all-time high (before Argentina crisis)

SHARES_M    = 535.0    # Diluted shares outstanding (Q1 2026: 535.4M; basic Feb 2026: 534M)
DIVIDEND_ANN = 0.0     # No dividend; Fiserv returns capital via share buybacks

# ── Adjusted EPS history (non-GAAP; management's preferred metric) ──
EPS_HISTORY = {
    "FY2022": 6.50,   # On-target delivery (guidance: $6.40–$6.55)
    "FY2023": 7.50,   # Strong execution (derived from FY2024 growth rates)
    "FY2024": 8.82,   # Record (derived: FY2025 $8.64 was -2% from FY2024)
    "FY2025": 8.64,   # Massive guidance cut in Oct 2025 (from $10.15E → $8.50-8.60 actual)
}
#  FY2022–FY2024: CAGR ~16%/yr — premium fintech compounder
#  FY2025: EPS reset due to (a) Argentina peso devaluation April 2025 + float income loss;
#          (b) Merchant Solutions adj margin compression 34% → ~26%

EPS_NOW    = 8.15   # FY2026E consensus (mid of company guidance $8.00–$8.30)
EPS_TROUGH = 4.50   # Floor scenario: Argentina permanent impairment + merchant margins → 20%;
                    # Financial Solutions alone (~$3.50 EPS) anchors the absolute floor

EPP_MIN_PE = 10     # Fintech in active restructuring; above banks (9×) but below stable
                    # fintech (15-18×); 10× reflects trust deficit + execution uncertainty
EPP        = EPP_MIN_PE * EPS_TROUGH   # = 45.00

# ── Method B: 2-year forward (FY2027E) ──
CONS_EPS_2YR  = 9.00    # FY2027E (Argentina lap complete; "One Fiserv" early wins;
                         # merchant margins recovering toward 30%; ~10% growth from FY2026E)
CONS_EXIT_PE  = 14       # Significant discount to history (25-35×); trust must be rebuilt
                         # over multiple quarters; below-peer-average reflecting execution risk
price_b       = CONS_EPS_2YR * CONS_EXIT_PE   # = 126.00

ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)

# ── Segment metrics ──
REV_FY2025_B         = 21.19   # GAAP revenue FY2025 ($B); +4% YoY
MERCHANT_MARGIN_HIST = 34.0    # Merchant Solutions adj op margin pre-crisis (%)
MERCHANT_MARGIN_NOW  = 26.0    # Merchant Solutions adj op margin Q1 2026 (%)
FIN_SOL_MARGIN       = 40.0    # Financial Solutions adj op margin (~stable)
ORGANIC_GROWTH_FY25  = 4.0     # Full year 2025 organic revenue growth (%)
ORGANIC_GROWTH_Q1    = -3.6    # Q1 2026 organic (Argentina comp headwind; one-time)

# ── Softmax composite engine ──
def softmax_weights(composite, T=0.60):
    centres = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
    logits  = {k: -((composite - v) ** 2) / T for k, v in centres.items()}
    m       = max(logits.values())
    exps    = {k: math.exp(v - m) for k, v in logits.items()}
    s       = sum(exps.values())
    return   {k: v / s for k, v in exps.items()}

scenarios = {
    "BEAR":  45.00,    # EPP floor; restructuring failure + Argentina permanent impairment
    "BASE":  82.00,    # Analyst zone; stabilised earnings at 10× FY2026E $8.15
    "BULL":  126.00,   # Method B; FY2027E $9.00 × 14×; One Fiserv delivering
    "XBULL": 175.00,   # Full recovery; $9.50 × 18-19×; trust fully rebuilt; ATH path
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
    ("Q1 2026: adj EPS $1.79 beat $1.58 (+13%); guidance reaffirmed  ",  +0.30, 0.20),
    ("Financial Solutions fully intact; 2,500 bank contracts; 2-3% grow",  +0.25, 0.20),
    ("7× FW P/E — all-time cheapest multiple; Clover 50M SMBs = asset ",  +0.35, 0.25),
    ("Argentina lapping: Q2 2026 comps normalise; one-time FX behind us",  +0.20, 0.15),
    ("Execution risk: 'One Fiserv' unproven; 4-quarter trust rebuild req",  -0.35, 0.25),
    ("Merchant margins still declining; 26% vs 34% target; no floor yet",  -0.20, 0.20),
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
    print("FISERV INC. (FISV) — SIGNAL MODEL")
    print("=" * 70)

    print(FRAMEWORK)
    print(COMMENTARY)

    print("KEY METRICS")
    print(f"  Current price (fetched)      = ${CURRENT_PRICE:>8.2f}")
    print(f"  52-week range                = ${PRICE_52W_LOW:.2f} – ${PRICE_52W_HIGH:.2f}")
    print(f"  All-time high (March 2025)   = ${ATH_PRICE:.2f}  (stock -76% from ATH)")
    print(f"  Market cap                   = ${CURRENT_PRICE * SHARES_M / 1000:.1f}B")
    print(f"  FW P/E on FY2026E $8.15      = {CURRENT_PRICE/EPS_NOW:.1f}×  (vs historical 25-35×)")
    print(f"  Dividend                     = None  (capital return via buybacks)")
    print(f"  Revenue FY2025               = ${REV_FY2025_B:.2f}B  (+4% GAAP YoY)")
    print(f"  Merchant Solutions margin    = {MERCHANT_MARGIN_NOW:.0f}%  (was {MERCHANT_MARGIN_HIST:.0f}% pre-crisis)")
    print(f"  Financial Solutions margin   = {FIN_SOL_MARGIN:.0f}%  (stable; untouched)")

    print("\nADJUSTED EPS HISTORY  (non-GAAP; guidance-based estimates for FY2022–FY2023)")
    for yr, eps in EPS_HISTORY.items():
        note = ""
        if yr == "FY2024": note = "  ← peak"
        if yr == "FY2025": note = "  ← CRISIS YEAR (guidance cut Oct 2025: $10.15E → $8.64A)"
        print(f"  {yr}  ${eps:>5.2f}{note}")
    print(f"  FY2026E ${EPS_NOW:.2f}  (company guidance $8.00–$8.30; Q1A $1.79 = beat +13%)")

    print(f"\nEPP CALCULATION")
    print(f"  EPS_TROUGH × EPP_MIN_PE  =  ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×  =  ${EPP:.2f}")
    print(f"  Note: current ${CURRENT_PRICE:.2f} is +{epp_gap_pct:.1f}% above EPP floor — stock deeply discounted")

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
        if k == "BEAR":  print("EPP floor; restructuring failure + Argentina total write-off")
        if k == "BASE":  print("Analyst zone; FY2026E $8.15 × 10×; stabilised but cheap")
        if k == "BULL":  print("Method B; FY2027E $9.00 × 14×; One Fiserv delivering")
        if k == "XBULL": print("Full recovery; $9.50 × 18-19×; trust fully rebuilt; ATH path")

    print(f"\nSOFTMAX COMPOSITE ENGINE")
    print(f"  Market composite (inferred)  =  {market_composite:.3f}")
    print(f"  (Market pricing deep BEAR — priced for restructuring failure / Argentina permanent)")

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

    print(f"\nSEGMENT METRICS")
    print(f"  Revenue FY2025               = ${REV_FY2025_B:.2f}B  (+4% GAAP YoY)")
    print(f"  Merchant Solutions margin    = {MERCHANT_MARGIN_NOW:.0f}%  (was {MERCHANT_MARGIN_HIST:.0f}% pre-Argentina crisis)")
    print(f"  Financial Solutions margin   = {FIN_SOL_MARGIN:.0f}%  (stable; multi-year contracts)")
    print(f"  Organic revenue growth FY25  = +{ORGANIC_GROWTH_FY25:.1f}%  (pre-crisis trajectory)")
    print(f"  Organic revenue Q1 2026      = {ORGANIC_GROWTH_Q1:.1f}%  (Argentina anniversary headwind)")
    print(f"  Clover merchant devices      = ~50M SMB merchants globally")
    print(f"  Bank/CU contracts            = ~2,500  US financial institutions")
    print(f"  CFO (new)                    = Paul Todd  (ex-Global Payments, TSYS; joined Oct 2025)")
    print(f"  Analyst avg PT               = $70.15  (range $40–$115); deeply cautious post-crisis")

    print(f"\nSIGNAL ENTRY GUIDE")
    # Thresholds: solve (p - EPP) / (price_b - p) = ratio_threshold  (EPP=45, price_b=126)
    # BUY:        p = (45 + 0.75×126) / 1.75 = (45 + 94.5) / 1.75 = $79.71 ≈ $80
    # ACCUMULATE: p = (45 + 1.10×126) / 2.10 = (45 + 138.6) / 2.10 = $87.43 ≈ $87
    # WATCHLIST:  p = (45 + 1.75×126) / 2.75 = (45 + 220.5) / 2.75 = $96.55 ≈ $97
    # HOLD/TRIM:  p = (45 + 2.50×126) / 3.50 = (45 + 315) / 3.50 = $102.86 ≈ $103
    print(f"  ✕ AVOID      above  $103  (ratio_b > 2.50×; 52-wk high $177 was AVOID territory)")
    print(f"  ▷ HOLD/TRIM   $97 – $103  (ratio_b 1.75–2.50×)")
    print(f"  ◐ WATCHLIST   $87 –  $97  (ratio_b 1.10–1.75×)")
    print(f"  ◎ ACCUMULATE  $80 –  $87  (ratio_b 0.75–1.10×)")
    print(f"  ◉ BUY         below  $80  (ratio_b < 0.75×)  ← current ${CURRENT_PRICE:.2f}  DEEP BUY")
    print()
    print(f"  52-wk low $52.17 = extreme distress (below EPP floor; ratio_b negative).")
    print(f"  52-wk high $177 = AVOID had appeared on any rational valuation basis.")
    print(f"  Key watch: Q2 2026 organic growth (first clean Argentina comp).")
    print(f"  Key watch: Merchant Solutions adj margin — must stabilise ≥ 28% to validate thesis.")
    print(f"  Key trigger: Any positive guidance revision drives massive multiple re-rating.")
