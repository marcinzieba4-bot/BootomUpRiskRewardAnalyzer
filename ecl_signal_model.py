"""
ecl_signal_model.py — Ecolab Inc. (NYSE: ECL)
World leader in water, hygiene, and infection prevention. Service + chemistry model.
Signal framework: EPP floor + Method B + SCA softmax engine.
"""

import math

# ── LIVE PRICE (fetched before model construction) ──────────────────────────
CURRENT_PRICE = 254.00    # ECL — fetched from Yahoo Finance, 2026-05-27
# (~$254.23 as of May 27, 2026; 52-wk low $243.15, 52-wk high $309.27)
# Market cap ~$71.3B; shares ~281M; P/E ~30×; dividend yield ~1.0%

TICKER        = "ECL"
COMPANY       = "Ecolab Inc."
SHARES_M      = 281          # million diluted shares (~281M as of Q1 2026)
DIVIDEND_ANN  = 2.60         # USD/yr; ~34 consecutive annual increases; +12% most recent hike
                              # Consistent dividend grower (not yet at 25yr King threshold)

# ── EPS CONVENTION ───────────────────────────────────────────────────────────
# Adjusted diluted EPS (non-GAAP). Excludes:
#   - Special charges / restructuring (discrete cost actions)
#   - Discrete tax items
#   - Acquisition and divestiture-related charges
# GAAP EPS is meaningfully lower due to amortisation of acquisition intangibles
# (Nalco 2011, Champion 2013, and ongoing bolt-ons). Adjusted EPS is the standard
# metric used by sell-side and management guidance for ECL.

EPS_HISTORY = {
    "FY2022": 4.69,    # recovery year post-COVID + supply chain costs;
                        # inflation headwinds compressing margins; below pre-COVID trajectory
    "FY2023": 5.21,    # +11.1% YoY; pricing actions + volume recovery; margin expansion begins
    "FY2024": 6.65,    # +27.6% YoY; exceptional operating leverage; strongest growth in decade
    "FY2025": 7.53,    # +13.2% YoY; continued pricing + volume; record Q4; full-year beat
}

# Q1 2026 (Apr 29, 2026): Adj EPS $1.70 (+13% YoY); revenue $4.07B (+10%); record EBITDA Q1
# Global Water +11%, Institutional & Specialty +9%, Pest Elimination +8%, Life Sciences +7%
# CoolIT acquisition $4.75B announced March 2026 (AI data center liquid cooling); closing Q3 2026
# FY2026 guidance: adj EPS $8.43-$8.63 (+13%); EXCLUDES CoolIT (closes Q3; EPS dilutive yr1)

EPS_NOW       = 8.53     # NTM; midpoint of FY2026 adj EPS guidance $8.43–$8.63
                          # Q1 2026 +13% on track; guidance does NOT include CoolIT
EPS_TROUGH    = 5.00     # severe recession scenario: institutional/hospitality down 20-30%;
                          # industrial production falls; water compliance budgets delayed;
                          # Context: FY2022 was $4.69 (elevated supply chain + inflation shock);
                          # $5.00 = realistic floor for a severe combined demand+cost shock
EPP_MIN_PE    = 22        # service + chemistry model with non-discretionary compliance demand
EPP           = EPP_MIN_PE * EPS_TROUGH   # = $110.00

CONS_EPS_2YR  = 9.70     # FY2027E analyst consensus (Erste Group, post-CoolIT integration;
                          # ~14%/yr growth trajectory; CoolIT adds scale but year-2 accretive)
CONS_EXIT_PE  = 38        # ECL historically 32-45× forward; 38× = premium maintained for
                          # water scarcity secular tailwind + service model + pricing power
price_b       = CONS_EPS_2YR * CONS_EXIT_PE   # = $368.60 → rounded to $370.00
price_b       = 370.00

ratio_b       = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
epp_gap_pct   = (CURRENT_PRICE - EPP) / EPP * 100

# Scenario prices (2-year forward targets)
scenarios = {
    "BEAR":  110,    # EPP; deep recession + institutional collapse; $5.00 × 22×
    "BASE":  280,    # FY2027E $9.70 × 28×; modest CoolIT contribution; rate pressure
    "BULL":  370,    # Method B; FY2027E $9.70 × 38×; CoolIT synergies; water scarcity re-rate
    "XBULL": 450,    # AI data centre cooling at scale; water scarcity premium; $11 × 41×
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
    ("Service + chemistry model moat: 45,000+ field reps visit 3M+ customer "
     "locations daily. Nalco One digital water platform integration = years of "
     "re-implementation cost to switch. Non-discretionary compliance (food safety, "
     "sterilisation, water treatment regulations) means ECL's value cannot be cut.",
     +0.35, 0.25),
    ("Water scarcity secular tailwind: global water stress accelerating; industrial "
     "water treatment is mission-critical (cannot run plants without clean water); "
     "expanding regulation (EU Water Framework, EPA PFAS rules) expands TAM; "
     "pricing power = 3-5%/yr without volume growth needed.",
     +0.30, 0.20),
    ("CoolIT acquisition ($4.75B; AI data centre liquid cooling): positions ECL as "
     "THE water and cooling solutions provider for AI data centres — the highest-growth "
     "infrastructure segment. CoolIT $550M revenue growing fast; ECL's existing data "
     "centre water treatment relationships = immediate cross-sell optionality.",
     +0.25, 0.15),
    ("34 consecutive annual dividend increases; strong FCF generation (~$2.5B/yr); "
     "record FY2025 adj EPS $7.53 (+13%); Q1 2026 +13% on track; 21 analyst Buy "
     "consensus; UBS upgraded to Buy May 20, 2026.",
     +0.20, 0.10),
    ("CoolIT execution and leverage risk: $4.75B financed 100% with term loan adds "
     "~3× net debt/EBITDA temporarily; EPS dilutive year 1; integration of a "
     "hardware business (CoolIT) into a service/chemistry model is operationally "
     "complex; data centre cooling is a new vertical for ECL.",
     -0.30, 0.15),
    ("Premium valuation at 30× FY2026E: ECL has rarely been cheap; 52-wk high "
     "$309.27 = AVOID at ratio_b 7.6×; current $254 near 52-wk low $243.15 but "
     "still WATCHLIST, not ACCUMULATE; CoolIT leverage overhang caps re-rating "
     "near-term; macro softness could compress institutional hospitality volumes.",
     -0.20, 0.15),
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
    DASH = "─" * 70

    print(SEP)
    print("ECOLAB INC. (ECL) — SIGNAL MODEL")
    print("World leader in water, hygiene & infection prevention. Service + chemistry.")
    print(SEP)

    print("""
SIGNAL FRAMEWORK — METHOD B + SCA ENGINE
─────────────────────────────────────────
EPP  = EPS_TROUGH × EPP_MIN_PE          (structural floor; adjusted EPS basis)
Ratio B = (Price − EPP) / (price_b − Price)

ECL EPS convention: Adjusted diluted EPS. Excludes special charges, discrete
tax items, and acquisition/divestiture-related charges. GAAP EPS is lower due
to amortisation of Nalco (2011), Champion (2013), and other acquisition
intangibles. Adjusted EPS is the standard metric used by management guidance
and sell-side coverage for ECL.

SIGNAL THRESHOLDS
  Ratio B < 0.75   →  ◉ BUY
  0.75 – 1.10      →  ◎ ACCUMULATE
  1.10 – 1.75      →  ◐ WATCHLIST
  1.75 – 2.50      →  ▷ HOLD/TRIM
  > 2.50           →  ✕ AVOID

EPP_MIN_PE = 22×  rationale:
  Ecolab operates a uniquely resilient service + chemistry model:
  (1) NON-DISCRETIONARY DEMAND: ECL's core services — water treatment for
      industrial facilities, sanitisation for food processing, infection
      prevention for healthcare, and pest elimination — are regulatory
      requirements, not discretionary spend. A food processing plant cannot
      legally operate without water treatment and sanitation compliance.
      A hospital cannot operate without ECL's sterilisation protocols.
      This creates a structural floor that resists deep recessions.
  (2) SERVICE MOAT: 45,000+ field service reps visit 3M+ customer locations
      daily. These reps monitor water chemistry, adjust treatment protocols,
      and provide compliance documentation. Once integrated into a facility's
      operations, switching ECL requires retraining staff, re-validating
      chemistry protocols, and risking regulatory compliance gaps. The
      Nalco One digital platform deepens this lock-in further.
  (3) PRICING POWER: Chemical inputs (caustics, biocides) are a minority of
      ECL's cost; the majority is field service labour. ECL can pass through
      3-5% price increases annually without significant volume loss because
      customers value compliance certainty over cost minimisation.
  (4) RECESSION PERFORMANCE: In COVID-2020, institutional hospitality volumes
      collapsed (hotels shut) but industrial, healthcare, and food segments
      held. ECL's FY2020 adj EPS fell from $5.78 → $3.83 (-34%) — significant
      but recovered fully in FY2021. At 22×, EPP = $110 = FY2020 COVID trough
      implied multiple, reflecting the genuine (not permanent) cyclical risk.
  22× = appropriate minimum for a service-model business with regulatory lock-in.
""")

    print("ECOLAB INC. (ECL) — THE INVISIBLE INFRASTRUCTURE OF CLEAN WATER AND SAFE FOOD")
    print("=" * 70)

    print("""
BUSINESS OVERVIEW
─────────────────
Ecolab was founded in 1923 in St. Paul, Minnesota. It is the world's leading
water, hygiene, and infection prevention company (~$16.2B revenue FY2025).
Headquarters: St. Paul, Minnesota. CEO: Christophe Beck (since 2021; former
CFO/COO — deep operational and financial expertise). Market cap: ~$71B.

The core insight: Ecolab does not sell chemicals. It sells the OUTCOME of
clean water, safe food, and hygienic surfaces — backed by 45,000+ field reps
who monitor, optimise, and guarantee compliance. Competitors who sell commodity
chemicals cannot replicate this service model.

FOUR SEGMENTS: THE EARNINGS ENGINE
──────────────────────────────────────
  GLOBAL WATER  (~40% of sales; HIGHEST MARGIN)
  ──────────────────────────────────────────────────────────────────────
  Industrial water treatment and process efficiency: serves petrochemical,
  oil/gas, mining, food & beverage manufacturing, pulp/paper, and power
  generation facilities globally. The Nalco Water brand (acquired 2011 for
  $8.1B) is the market leader.

  KEY INSIGHT: Industrial facilities cannot operate without water treatment.
  A refinery that runs without corrosion inhibitors destroys its pipes in
  months; a power plant without scale inhibitors loses heat transfer
  efficiency; a food processing plant without biocides fails FDA inspections.
  This makes Global Water uniquely non-discretionary. Q1 2026: +11% YoY.

  Nalco One digital platform: real-time water quality monitoring sensors +
  AI-optimised chemical dosing = fewer chemicals, less water consumption,
  and better compliance documentation. Once deployed, Nalco One creates
  sticky, multi-year service contracts that are self-reinforcing.

  INSTITUTIONAL & SPECIALTY  (~35% of sales; MID-HIGH MARGIN)
  ──────────────────────────────────────────────────────────────────────
  Sanitisation, cleaning, and hygiene programs for foodservice, hospitality,
  laundry, and building care. Serves restaurant chains, hotels, hospitals,
  schools, and food processors globally.

  CRITICAL: In food processing and foodservice, ECL is the service provider
  that stands between the operator and an FDA/USDA food safety violation.
  A restaurant chain with 2,000 locations cannot afford a single outbreak
  traced to a sanitisation failure — ECL's service contract is their
  insurance policy. This creates extremely low churn.

  Q1 2026: +9% YoY — driven by new customer wins in food & beverage and
  ongoing hospitality recovery.

  PEST ELIMINATION  (~15% of sales; RECURRING CONTRACT MODEL)
  ──────────────────────────────────────────────────────────────────────
  Commercial pest control (not consumer). Serves food processing, hospitality,
  healthcare, and retail. Highly recurring (monthly/quarterly service contracts).
  ~$2.4B revenue. ECL is the #2 commercial pest control company globally.

  LIFE SCIENCES  (~10% of sales; HIGHEST GROWTH)
  ──────────────────────────────────────────────────────────────────────
  Specialised cleaning, disinfection, and biosafety solutions for biopharma
  manufacturing, medical devices, and clinical environments. Post-COVID, this
  segment expanded from vaccine/gene therapy manufacturing compliance.
  Fastest-growing segment; margin expansion ongoing. Q1 2026: +7% YoY.

THE SERVICE MODEL: WHY COMPETITORS CANNOT REPLICATE ECL
─────────────────────────────────────────────────────────
A chemical distributor can sell biocides, scale inhibitors, or sanitisers at
lower prices than ECL. But they cannot replicate the service infrastructure:

  FIELD DENSITY: 45,000+ field reps across all major industrial regions visit
  customer locations daily to test water chemistry, adjust treatment programmes,
  and verify compliance. A food plant superintendent does not need cheaper
  chemicals — they need someone who arrives before the FDA inspector and
  ensures the paperwork is perfect.

  DIGITAL PLATFORM: Nalco One IoT sensors continuously monitor water quality
  parameters in real time. The AI system automatically adjusts chemical dosing
  to optimise both efficacy and cost. This data creates a compliance audit trail
  that regulators increasingly require — and that a commodity supplier cannot provide.

  COMPLIANCE EXPERTISE: ECL's specialists understand the regulatory
  requirements across every vertical (FDA food safety, EPA water discharge,
  USDA processing rules, OSHA safety). They function as outsourced compliance
  departments for mid-size facilities that can't afford in-house specialists.

  OUTCOME GUARANTEE: ECL offers performance guarantees — if a facility's
  water treatment fails to meet spec, ECL provides remediation at no charge.
  No commodity chemical supplier can make this guarantee. The guarantee is
  only possible because ECL has 100+ years of application data.

COOLT IT ACQUISITION: AI DATA CENTRES AS THE NEW FRONTIER
──────────────────────────────────────────────────────────
March 2026: Ecolab announced the acquisition of CoolIT Systems for $4.75B cash.
CoolIT is the world's leading provider of liquid cooling systems for AI/HPC
data centres (~$550M revenue; growing double-digits annually).

  THE THESIS: AI data centres require exponentially more cooling per rack
  (from 5-10 kW per rack in 2020 to 100-200 kW per rack in 2026 for GPU
  clusters). Air cooling is approaching its physical limits; direct liquid
  cooling (DLC) — circulating chilled water through server hardware — is
  the only scalable solution.

  ECL'S STRATEGIC LOGIC: Ecolab already manages cooling water systems for
  thousands of data centres (Global Water segment). CoolIT adds the DLC
  hardware layer — meaning ECL can now offer a COMPLETE thermal management
  solution: the water treatment chemicals, the water quality monitoring
  (Nalco One), AND the liquid cooling infrastructure. This is a natural
  extension of ECL's existing data centre water relationships.

  FINANCIAL IMPACT:
    - $4.75B purchase price (100% debt-financed; ~3× incremental leverage)
    - CoolIT contributes ~$550M revenue; growing at double-digit rates
    - EPS dilutive in year 1 (interest expense + integration costs)
    - Management expects accretion by year 2-3 as CoolIT grows into valuation
    - FY2026 guidance EXCLUDES CoolIT (deal closes Q3 2026)

  RISK: Integration of a hardware business into a service/chemistry model
  is operationally complex. CoolIT's margin profile differs from ECL's core.
  This is the primary execution risk and explains the near-term discount.

WATER SCARCITY: THE SECULAR TAILWIND THAT CANNOT BE STOPPED
──────────────────────────────────────────────────────────────
Global water stress is accelerating:
  - 40% of the global population faces water scarcity
  - Industrial water demand growing +2%/yr globally
  - Regulatory pressure increasing: EU Water Framework Directive, US PFAS rules,
    China water treatment mandates for manufacturing — all expand ECL's TAM
  - Water recycling and reclamation at industrial facilities is a primary
    sustainability priority for Fortune 500 companies — ECL is the provider
  - Each year, ECL saves customers ~200B gallons of water through treatment
    efficiency — this metric creates tangible, auditable ESG value

This secular trend means ECL's pricing power is structural, not cyclical.
Water scarcity makes every gallon of industrial water MORE valuable, which
increases the ROI of ECL's treatment programs and justifies premium pricing.

FINANCIAL PROFILE: CONSISTENT COMPOUNDER
──────────────────────────────────────────
  FY2025 Revenue:          ~$16.2B  (+8% YoY; broad-based growth)
  Adj operating margin:    ~17-18%  (best in 5 years; ongoing expansion)
  FCF:                     ~$2.5B   (~15% FCF margin — strong for a service/mfg hybrid)
  Net debt / adj EBITDA:   ~2.0× pre-CoolIT; ~3.0-3.5× post-CoolIT (temporary)
  ROIC:                    ~20-22%  (exceptional; service model = capital-efficient)
  Share count:             ~281M    (modest annual buyback programme ~1-2%)
  Dividend streak:         ~34 consecutive annual increases (+12% most recent)
  EPS CAGR 10yr:           ~10%/yr  (remarkably consistent through cycles)

Q1 2026 RESULTS (April 29, 2026):
  Adj diluted EPS:    $1.70   (+13% YoY; beat consensus)
  Net sales:          $4.07B  (+10% YoY; organic +9%)
  Record Q1 EBITDA    (all four segments growing)
  Global Water:       +11%    (industrial recovery + pricing)
  Institutional:      +9%     (hospitality + food safety demand)
  Pest Elimination:   +8%     (new contracts + geographic expansion)
  Life Sciences:      +7%     (biopharma manufacturing)
  FY2026 guidance:    $8.43–$8.63 adj EPS (maintained; excludes CoolIT)

FY2025 FULL YEAR:
  Adj EPS:   $7.53  (+13.2% from $6.65; strong operating leverage)
  Revenue:   ~$16.2B (+8%)
  Q4 2025:   record adj EPS quarter; momentum building into FY2026
  Operating cash: ~$2.8B (strong cash conversion; supports CoolIT financing)

LONG-TERM THESIS: WHY ECL COMPOUNDS AT 10%/YR FOR DECADES
────────────────────────────────────────────────────────────
Ecolab has compounded adj EPS at ~10%/yr for 20+ years. The structural drivers:
  1. Pricing power: 3-5%/yr into non-discretionary demand (no volume needed)
  2. Volume growth: industrial production + new vertical penetration
  3. CoolIT: AI data centre cooling = new $20B+ TAM at premium margins yr 3+
  4. Water scarcity: every year this worsens = higher value of ECL services
  5. Life Sciences: biopharma compliance demand growing faster than GDP
  6. Capital return: ~$1-2B/yr dividends+buybacks; 34yr dividend growth streak

The premium P/E (30-40× forward) is justified by: low cyclicality, regulatory
lock-in, service model stickiness, pricing power, and multi-decade secular tailwinds.
ECL near the 52-wk low ($243) = rare opportunity to accumulate at a cyclical discount.
""")

    print(DASH)
    print("EPS HISTORY  (Adjusted Diluted EPS, non-GAAP)")
    print(DASH)
    for yr, eps in EPS_HISTORY.items():
        print(f"  {yr}  ${eps:.2f}")
    print(f"  FY2026E ${EPS_NOW:.2f}  (guidance $8.43–$8.63; Q1 $1.70 = +13% on track; excludes CoolIT)")
    cagr_3yr = (EPS_HISTORY["FY2025"] / EPS_HISTORY["FY2022"]) ** (1/3) - 1
    print(f"  FY2022–FY2025 CAGR: {cagr_3yr*100:.1f}%/yr  (pricing + volume + margin expansion)")

    print(f"""
EPP CALCULATION
  EPS_TROUGH × EPP_MIN_PE  =  ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×  =  ${EPP:.2f}
  (Below FY2022 actual $4.69; assumes severe demand collapse + compliance spend freeze)
  Context: FY2020 COVID adj EPS was $3.83; $5.00 = realistic severe combined-shock trough
  EPP buffer: current ${CURRENT_PRICE:.2f} is +{epp_gap_pct:.1f}% above EPP

METHOD B  (2-year forward)
  CONS_EPS_2YR × CONS_EXIT_PE  =  ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×  =  ${price_b:.2f}

RATIO B  (PRIMARY SIGNAL)
  (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})
  = ${CURRENT_PRICE - EPP:.2f} / ${price_b - CURRENT_PRICE:.2f}
  = {ratio_b:.3f}×   →   {signal}
  Near 52-wk low; UBS upgraded to Buy May 20; CoolIT leverage = near-term overhang

SCENARIO PRICES
  BEAR     ${scenarios['BEAR']:>7.2f}   EPP; deep recession + institutional collapse; $5.00 × 22×
  BASE     ${scenarios['BASE']:>7.2f}   FY2027E $9.70 × 28×; modest CoolIT; rate pressure on multiple
  BULL     ${scenarios['BULL']:>7.2f}   Method B; FY2027E $9.70 × 38×; CoolIT synergies; water scarcity premium
  XBULL    ${scenarios['XBULL']:>7.2f}   AI data centre at scale + water scarcity re-rate; $11 × 41×
""")

    print("SOFTMAX COMPOSITE ENGINE")
    print(f"  Market composite (inferred)  =  {market_composite:.3f}")
    print(f"  (Market near BASE/lower — pricing CoolIT leverage discount vs secular quality)")

    print(f"""
SCA — SIGNAL CATALYST ADJUSTMENTS""")
    for desc, score, wt in sca_items:
        sign = "+" if score >= 0 else ""
        print(f"  {desc[:55]:<55}  {sign}{score:.2f} × {wt:.2f}  =  {score*wt:+.4f}")

    print(f"""
  sca_raw     =  {sca_raw:.4f}
  sca_adj     =  {sca_adj:.4f}  (= sca_raw / 2.0)
  adj_composite  =  {market_composite:.3f}  +  {sca_adj:.4f}  =  {adj_composite:.3f}
  (Net positive SCA: service moat + water scarcity + CoolIT AI option outweigh leverage risk)
""")

    print("SOFTMAX SCENARIO WEIGHTS  (at adj_composite = {:.3f})".format(adj_composite))
    for k, w in adj_weights.items():
        print(f"  {k:<10} {w*100:>5.1f}%   ${scenarios[k]:.2f}")

    ep_price = sum(adj_weights[k] * scenarios[k] for k in scenarios)
    print(f"\n  Expected price (probability-weighted)  =  ${ep_price:.2f}")

    print(f"""
BUSINESS METRICS
  FY2025 revenue                  = ~$16.2B  (+8% YoY; broad-based)
  Q1 2026 revenue                 = $4.07B   (+10% YoY; organic +9%)
  Q1 2026 adj EPS                 = $1.70    (+13% YoY; beat consensus)
  Adj operating margin            = ~17-18%  (record; expanding)
  Free cash flow (FY2025)         = ~$2.5B   (~15% FCF margin)
  Field service reps              = 45,000+  (3M+ customer locations daily)
  Dividend growth streak          = ~34 consecutive annual increases
  Net debt / EBITDA pre-CoolIT    = ~2.0×    (post-CoolIT: ~3.0-3.5× temporarily)
  CoolIT acquisition price        = $4.75B   (100% debt; closing Q3 2026)
  CoolIT revenue                  = ~$550M   (growing double-digits)
  FY2026 adj EPS guidance         = $8.43–$8.63 (+13% midpoint; excludes CoolIT)
  Analyst consensus               = Buy; avg PT $320.19 (21 analysts; UBS upgraded May 20)
  52-wk low $243.15 (May 2026)    = ACCUMULATE at ratio_b 1.05×
  52-wk high $309.27              = AVOID at ratio_b 7.63×

SIGNAL ENTRY GUIDE""")

    thresholds = {}
    for label, rb in [("AVOID", 2.50), ("HOLD", 1.75), ("WATCH", 1.10), ("ACCUM", 0.75)]:
        thresholds[label] = (rb * price_b + EPP) / (1 + rb)

    print(f"  ✕ AVOID      above  ${thresholds['AVOID']:>3.0f}  (ratio_b > 2.50×)")
    print(f"  ▷ HOLD/TRIM  ${thresholds['HOLD']:>3.0f} – ${thresholds['AVOID']:>3.0f}  (ratio_b 1.75–2.50×)")
    print(f"  ◐ WATCHLIST  ${thresholds['WATCH']:>3.0f} – ${thresholds['HOLD']:>3.0f}  (ratio_b 1.10–1.75×)  ← current ${CURRENT_PRICE:.0f}  {signal}")
    print(f"  ◎ ACCUMULATE ${thresholds['ACCUM']:>3.0f} – ${thresholds['WATCH']:>3.0f}  (ratio_b 0.75–1.10×)")
    print(f"  ◉ BUY        below  ${thresholds['ACCUM']:>3.0f}  (ratio_b < 0.75×)")

    lo52 = 243.15
    rb52lo = (lo52 - EPP) / (price_b - lo52)
    hi52 = 309.27
    rb52hi = (hi52 - EPP) / (price_b - hi52)
    print(f"""
  52-wk low $243.15 (May 2026 CoolIT leverage concern) = ACCUMULATE at ratio_b {rb52lo:.2f}×.
  52-wk high $309.27 = AVOID at ratio_b {rb52hi:.2f}×; reached before CoolIT announcement discount.
  UBS upgraded to Buy from Neutral on May 20, 2026 (PT $320); analyst avg PT $320.19.
  Analyst avg PT $320 = in our AVOID zone — buy before the crowd or pay up.
  KEY WATCH: CoolIT closing confirmation (Q3 2026); CoolIT integration progress (yr1 EPS drag);
  Water treatment volume in industrial production; FY2026 guidance raise potential.
  CoolIT THESIS: If CoolIT delivers $700M+ revenue by FY2027 (AI data centre demand surge),
  ECL's BULL scenario ($370) opens; if CoolIT integration stumbles, near-term overhang persists.
  ACCUMULATE on weakness ($215–$244): patience rewarded as CoolIT leverage concern clears.""")
