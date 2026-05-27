"""
shw_signal_model.py — The Sherwin-Williams Company (NYSE: SHW)
World's largest paint company. Professional contractor monopoly. 47-yr dividend king.
Signal framework: EPP floor + Method B + SCA softmax engine.
"""

import math

# ── LIVE PRICE (fetched before model construction) ──────────────────────────
CURRENT_PRICE = 316.00    # SHW — fetched from Yahoo Finance / CNBC, 2026-05-27
# ($315.56 as of May 27, 2026; 52-wk low $294.32, 52-wk high $379.65)
# Market cap ~$77.8B; shares ~247M; P/E ~30×; dividend yield ~1.0%

TICKER        = "SHW"
COMPANY       = "The Sherwin-Williams Company"
SHARES_M      = 247          # million diluted shares (~246.64M as of Q1 2026)
DIVIDEND_ANN  = 3.20         # USD/yr; $0.80/quarter; 47th consecutive annual increase
                              # "Dividend King" (50+ years = only 65 US companies qualify)

# ── EPS CONVENTION ───────────────────────────────────────────────────────────
# Adjusted diluted net income per share (non-GAAP). Excludes:
#   - Acquisition-related amortisation (Valspar acquisition, 2017 — largest in industry)
#   - Restructuring and integration charges
#   - Certain pension settlement costs
# GAAP EPS is meaningfully lower (~80% of adjusted) due to ongoing Valspar intangible
# amortisation. Adjusted EPS is the standard metric across the coatings industry.

EPS_HISTORY = {
    "FY2022": 8.73,    # -16% from FY2021; raw material cost spike (TiO2, resins, solvents);
                        # post-COVID supply chain disruption at peak; gross margin compressed
    "FY2023": 10.35,   # +18.6% YoY; raw material normalisation; volume recovery; margin expansion
    "FY2024": 11.33,   # +9.5% YoY; continued margin expansion; pricing actions holding
    "FY2025": 11.43,   # +0.9% YoY; housing market softness; high rates suppressing turnover;
                        #   Q4 2025 adj EPS $2.23 (+6.7%); FY sales $23.57B (+2.1%)
}

# Q1 2026 (Apr 28, 2026): Adj EPS $2.35 (+4.4% YoY); revenue $5.67B (+6.8%); record Q1 EBITDA
# Paint Stores Group +3.7% (same-store +2.4%); Consumer Brands +19.2%; Perf Coatings +6.5%
# Net debt / adj EBITDA: 2.5× (comfortable; consistent with leverage target)
# FY2026 guidance reaffirmed: adj diluted EPS $11.50–$11.90; net sales low to mid-single-digit %

EPS_NOW       = 11.70    # NTM; midpoint of FY2026 adj EPS guidance $11.50–$11.90
                          # Q1 2026 annualised: $2.35 × 4 = $9.40 (Q1 is seasonally weakest);
                          # H2 (peak paint season) substantially stronger than H1
EPS_TROUGH    = 8.00     # deep recession scenario: housing down 20-30%, volumes fall;
                          # raw material cost spike (TiO2 +30%, resin shortage); FX headwinds
                          # Context: FY2020 (COVID) adj EPS was $7.36; FY2022 raw mat crisis = $8.73
                          # $8.00 = realistic floor for a severe combined demand+cost shock
EPP_MIN_PE    = 22        # premium branded consumer/industrial — see rationale below
EPP           = EPP_MIN_PE * EPS_TROUGH   # = $176.00

CONS_EPS_2YR  = 12.75    # FY2027E analyst consensus (~9%/yr growth from FY2026 base;
                          # housing market normalisation + repaint cycle = growth re-acceleration)
CONS_EXIT_PE  = 32        # SHW historically 28–35× forward; 32× = premium maintained for
                          # Dividend King quality + professional contractor lock-in + pricing power
price_b       = CONS_EPS_2YR * CONS_EXIT_PE   # = $408.00

ratio_b       = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
epp_gap_pct   = (CURRENT_PRICE - EPP) / EPP * 100

# Scenario prices (2-year forward targets)
scenarios = {
    "BEAR":  176,    # EPP; housing recession + raw material spike; $8.00 × 22×
    "BASE":  344,    # FY2027E $12.00 × 28×; slow recovery; rates stay high; limited re-rating
    "BULL":  408,    # Method B; FY2027E $12.75 × 32×; housing normalises; premium maintained
    "XBULL": 480,    # Housing recovery + repaint acceleration; $13.50 × 35×; peak cycle premium
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
    ("Professional contractor monopoly: 4,900+ company-owned US stores; painters "
     "won't switch (color formulas, rep relationships, tinting system lock-in). "
     "Virtually no churn; dominant pricing power with top 10% volume customers.",
     +0.30, 0.25),
    ("Aging US housing stock: avg US home ~42 years old; repainting frequency "
     "accelerates as homes age. ~70% of SHW volumes = repaint (not new construction) "
     "— structurally resilient. Long-term secular tailwind regardless of rate cycle.",
     +0.25, 0.20),
    ("47 consecutive annual dividend increases (Dividend King); 14.6% FCF margin "
     "(FY2025 $3.45B operating cash on $23.57B revenue); conservative leverage 2.5× "
     "net debt/EBITDA; best-in-class coatings operator by every margin metric.",
     +0.20, 0.10),
    ("Housing market headwinds: mortgage rates elevated; existing home sales subdued "
     "(SHW's biggest demand trigger is home transactions → repaint); new residential "
     "construction still muted. FY2026 guidance only +2.4% adj EPS — deceleration.",
     -0.35, 0.25),
    ("Current WATCHLIST zone ($316): stock down 16.8% from $379.65 ATH but not yet "
     "at ACCUMULATE. Fair entry was the April 2026 tariff-panic low of $294 (ACCUM). "
     "Raw material cost pressure from tariffs on TiO2 and resins adds near-term risk.",
     -0.25, 0.15),
    ("Consumer Brands Group restructuring: SHW is reshaping the DIY/big-box channel "
     "(Lowe's, Home Depot), including exiting some lower-margin SKUs. Transition year "
     "creates near-term noise but long-term margin improvement.",
     -0.10, 0.05),
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
    print("THE SHERWIN-WILLIAMS COMPANY (SHW) — SIGNAL MODEL")
    print("World's largest paint company. Contractor monopoly. 47-yr dividend king.")
    print(SEP)

    print("""
SIGNAL FRAMEWORK — METHOD B + SCA ENGINE
─────────────────────────────────────────
EPP  = EPS_TROUGH × EPP_MIN_PE          (structural floor; adjusted EPS basis)
Ratio B = (Price − EPP) / (price_b − Price)

SHW EPS convention: Adjusted diluted EPS. Excludes amortisation of Valspar
acquisition intangibles (2017; ~$11B deal — the largest in US paint history),
restructuring charges, and pension items. GAAP EPS runs ~$7.50–$8.50 vs
adjusted $11+ because Valspar amortisation ($0.70–$0.80/share/yr) still flows
through. Adjusted EPS is the industry-standard metric (PPG, RPM, Axalta all
use equivalent non-GAAP measures) and reflects true earning power.

SIGNAL THRESHOLDS
  Ratio B < 0.75   →  ◉ BUY
  0.75 – 1.10      →  ◎ ACCUMULATE
  1.10 – 1.75      →  ◐ WATCHLIST
  1.75 – 2.50      →  ▷ HOLD/TRIM
  > 2.50           →  ✕ AVOID

EPP_MIN_PE = 22×  rationale:
  Sherwin-Williams is a quasi-monopoly in professional architectural coatings:
  (1) STORE NETWORK MOAT: 4,900+ company-owned stores in the Americas create
      distribution density impossible for any competitor to replicate. A professional
      painter needs to pick up paint several times per day — they choose the nearest
      store with the deepest product knowledge. Competitors (PPG, RPM, Benjamin Moore)
      cannot match this density without decades of capital investment.
  (2) CONTRACTOR LOCK-IN: SHW's professional customers have invested years in
      learning its colour formulas, tinting systems, and rep relationships. A contractor
      who switches to PPG must re-calibrate all custom colours, retrain staff, and lose
      access to SHW's Chip service, Pro-App, and credit accounts. Switching costs are
      significant — churn from professional segments is near zero.
  (3) PRICING POWER: Because professionals depend on SHW for speed (nearest store)
      and trust (color consistency), SHW consistently takes 3–5% price increases even
      in soft years. Competitors struggle to match because pros pay for reliability,
      not commodity price.
  (4) RECESSION RESILIENCE: Repaint (70% of volumes) is non-discretionary in
      the long run — painted surfaces need repainting every 5–7 years regardless.
      Even in 2020 (COVID), SHW adj EPS fell only to $7.36 (-14% YoY) before
      recovering sharply. Not a cyclical commodity company.
  22× = same as LIN (oligopoly infrastructure). Different from commodity industrials
  but similar quality tier. In COVID (2020), SHW hit ~18× trough; 22× = appropriate
  severe-stress multiple for a brand/franchise business of this quality.
""")

    print("THE SHERWIN-WILLIAMS COMPANY (SHW) — THE INVISIBLE INFRASTRUCTURE OF EVERY PAINTED SURFACE")
    print("=" * 70)

    print("""
BUSINESS OVERVIEW
─────────────────
The Sherwin-Williams Company was founded in 1866 in Cleveland, Ohio. It is the
world's largest paint and coatings company by revenue (~$23.6B/yr) and market cap
(~$78B). The company manufactures, sells, and distributes paints, coatings, and
related products through three segments. Headquarters: Cleveland, Ohio.
CEO: Heidi Petz (President & CEO since January 2024; formerly President of The
Americas Group — deep operational expertise). 47 consecutive years of dividend
increases; 2024 dividend $3.20/share.

SHW operates as a vertically integrated paint company: it manufactures AND retails
paint through its own store network — a structure no major US competitor can match
(PPG sells through third parties; Benjamin Moore through independent dealers).

THREE SEGMENTS: THE EARNINGS ENGINE
──────────────────────────────────────
  PAINT STORES GROUP (THE AMERICAS GROUP)  ~60% of sales; HIGHEST MARGIN
  ──────────────────────────────────────────────────────────────────────
  4,900+ company-owned stores in the United States, Canada, and Latin America.
  Serves professional painters (residential repaint, commercial, new construction),
  property managers, and industrial contractors. This is the crown jewel.

  ARCHITECTURE:
    Residential repaint:     ~35% of PSG  (homeowners hiring pros to repaint)
    Commercial:              ~25% of PSG  (office buildings, retail, hospitality)
    New residential:         ~15% of PSG  (new home construction — most cyclical)
    Protective & marine:     ~15% of PSG  (industrial coatings, bridges, oil/gas)
    Property maintenance:    ~10% of PSG  (apartments, hotels — recurring)

  KEY INSIGHT: ~70% of Paint Stores Group is REPAINT, not new construction.
  Repaint is demand that MUST happen eventually — a home painted in 2018 must
  be repainted in 2023–2025. High rates slow the trigger (home sale = repaint)
  but don't eliminate it. The demand is DEFERRED, not destroyed.

  Q1 2026: PSG net sales +3.7%; same-store +2.4%; margin expanding.
  Record Q1 EBITDA $998.2M (+8.8% YoY). Protective & marine, residential repaint,
  and commercial led growth; new residential offset headwind.

  CONSUMER BRANDS GROUP           ~20% of sales; MID MARGIN
  ──────────────────────────────────────────────────────────────────────
  Products sold under Sherwin-Williams, HGTV Home, Dutch Boy, Minwax, Cabot,
  and other brands through retail channels (Lowe's, Home Depot, Amazon).
  Also includes the Valspar brand.
  IN TRANSITION: SHW is reshaping this segment — exiting low-margin SKUs,
  rationalising SKU count, and focusing on premium DIY products. Q1 2026 +19.2%
  (partly from retailer restocking + prior-year comparison lapping).

  PERFORMANCE COATINGS GROUP      ~20% of sales; MID-HIGH MARGIN
  ──────────────────────────────────────────────────────────────────────
  Industrial/commercial coatings globally: aerospace (Skydrol), automotive
  refinish, coil coatings (metal appliances/construction), general industrial
  coatings, powder coatings (furniture, appliances), protective marine.
  Serves global manufacturers, MRO, and OEM customers. Geographic: US, Europe, APAC.
  Q1 2026: +6.5% — industrial production broadly resilient.

THE PROFESSIONAL CONTRACTOR RELATIONSHIP: THE REAL MOAT
─────────────────────────────────────────────────────────
The magic of SHW is not the paint formula — it's the relationship system:

  STORE PROXIMITY: A professional painter working in a residential neighbourhood
  needs to pick up paint 3–5 times per day as projects evolve (colour changes,
  additional coats, touch-ups). A SHW store every 2–3 miles in suburban America
  means zero time lost. PPG's nearest dealer might be 15 minutes away.

  COLOR SYSTEMS: Over decades, SHW has helped contractors build custom colour
  formulas for their key clients (real estate developers, property managers,
  HOAs). These formulas are stored in SHW's system. Switching suppliers means
  losing those formulas — or paying to re-create them — and risking colour
  inconsistency on repeat jobs.

  CONTRACTOR LOYALTY PROGRAM: SHW's Pro Xtra programme offers tiered discounts
  (up to 40% for high-volume contractors), jobsite delivery, dedicated reps, and
  financing/credit. Volume discounts compound over time — the more you buy, the
  cheaper it gets. A painter who's reached the top tier has NO incentive to switch.

  TINTING EXPERTISE: Store associates are trained paint professionals, not
  retail associates. They understand mix ratios, substrate compatibility, and
  regional climate variations. This expertise creates genuine stickiness.

HOUSING MARKET: THE HEADWIND AND THE DEFERRED DEMAND
──────────────────────────────────────────────────────
The near-term bear case on SHW is simple: mortgage rates at 6.5–7%+ have:
  1. Locked homeowners in place (won't sell because they'd lose 3% mortgage)
  2. Crushed new home construction (affordability crisis)
  3. Reduced home transactions (repaint trigger #1)

This is real and explains FY2025's +0.9% adj EPS growth.

BUT the structural case is equally compelling:
  AGING HOUSING STOCK: The average US home is now ~42 years old (up from ~35 in 2010).
  Older homes repaint MORE frequently (weathering, wear, desire to update aesthetics).
  This is a structural tailwind that compounds regardless of interest rates.

  DEFERRED DEMAND: Every year of low painting activity creates future demand.
  Homes that weren't repainted in 2023–2025 WILL be repainted in 2026–2028.
  The demand doesn't disappear — it accumulates. When rates normalise, the
  repaint cycle accelerates sharply (as it did in 2021–2022 when rates first dropped).

  RATE NORMALISATION: If/when 30-yr mortgage rates fall toward 5.5%, existing home
  sales recover → transaction-driven repaint triggers → Paint Stores Group volume
  inflects. SHW is one of the clearest housing recovery plays in the S&P 500.

FINANCIAL PROFILE: MARGIN MACHINE
───────────────────────────────────
  FY2025 Revenue:          $23.57B   (+2.1% YoY; constrained by housing softness)
  Adj EBIT margin:         ~18–20%   (well above PPG ~15%, RPM ~13%)
  FCF:                     $3.45B    (14.6% FCF/revenue — exceptional for a manufacturer)
  Net debt / adj EBITDA:   2.5×      (within target range; maintains BBB+ credit rating)
  ROIC:                    ~25–30%   (paint stores model = capital-light once stores mature)
  Share count:             ~247M     (modest buyback programme; ~1–2% annual reduction)
  Capex:                   ~$600M    (80–100 new stores/yr + maintenance; ~2.5% of revenue)

KEY OPERATING METRICS: WHY THIS BUSINESS IS EXCEPTIONAL
─────────────────────────────────────────────────────────
  New store openings:      80–100/yr  (each store reaches payback in ~2 years)
  Store-level EBIT margin: ~25–30%   on mature stores (model of capital efficiency)
  Gross profit margin:     ~49–50%   (raw material leverage + pricing power)
  Paint price inflation:   3–5%/yr   (even in weak demand years — brand premium)
  Working capital:         NEGATIVE  (customers pay before SHW pays suppliers)
  Free cash flow:          ~$3.0–3.5B/yr → returned as dividends + buybacks + debt repay

Q1 2026 — RECORD EBITDA IN SEASONALLY WEAKEST QUARTER
─────────────────────────────────────────────────────────
  Adj diluted EPS:    $2.35   (+4.4% YoY; beat consensus)
  Net sales:          $5.67B  (+6.8% YoY)
  EBITDA:             $998.2M (+8.8% YoY; record Q1)
  PSG same-store:     +2.4%   (professional markets leading)
  Consumer Brands:    +19.2%  (restocking + prior-year lapping)
  Perf Coatings:      +6.5%   (industrial resilience)
  Net debt/EBITDA:    2.5×    (stable; well within target)
  Shareholder return: $773M   in Q1 (buybacks + dividends; 1.0% of market cap in one quarter)

FY2026 GUIDANCE REAFFIRMED:
  Adj diluted EPS:  $11.50–$11.90  (+0.6–4.1%; midpoint $11.70 = +2.4%)
  Net sales:        low to mid-single-digit % increase
  Q1 beat vs guidance implies H2 2026 could outperform

FY2025 FULL-YEAR (reported Feb 2026)
─────────────────────────────────────
  Adj EPS:   $11.43  (+0.9% from $11.33; soft but quality business absorbed headwinds)
  Revenue:   $23.57B (+2.1%)
  Q4 2025:   adj EPS $2.23 (+6.7%); sales $5.6B (+5.6%); momentum building into 2026
  Operating cash: $3.45B (14.6% of net sales; converting earnings to cash at premium rate)

LONG-TERM COMPOUNDER THESIS: WHY SHW IS A MULTI-DECADE WINNER
────────────────────────────────────────────────────────────────
Over the 20 years through 2024, Sherwin-Williams has compounded EPS at ~12%/yr
(with interruptions for Valspar integration, raw material cycles, housing cycles).
The structural drivers:
  1. Store network: +80–100 stores/yr × 2yr payback × $1.5M mature store EBIT
  2. Same-store growth: 2–5%/yr via pricing + share gain (professional market)
  3. Margin expansion: gross margin 43% (2015) → 49%+ (2024); still room to grow
  4. Repaint structural tailwind: aging housing stock → more frequent painting
  5. Capital return: $2–3B/yr dividends+buybacks reducing share count

When housing normalises, EPS growth should re-accelerate to 8–12%/yr (from current
~2–4%). The FY2025 and FY2026 slowdown is cyclical, not structural.
""")

    print(DASH)
    print("EPS HISTORY  (Adjusted Diluted EPS, non-GAAP)")
    print(DASH)
    for yr, eps in EPS_HISTORY.items():
        print(f"  {yr}  ${eps:.2f}")
    print(f"  FY2026E ${EPS_NOW:.2f}  (guidance $11.50–$11.90; Q1 $2.35 = +4.4% on track)")
    cagr_3yr = (EPS_HISTORY["FY2025"] / EPS_HISTORY["FY2022"]) ** (1/3) - 1
    print(f"  FY2022–FY2025 CAGR: {cagr_3yr*100:.1f}%/yr  (raw mat recovery + margin expansion)")

    print(f"""
EPP CALCULATION
  EPS_TROUGH × EPP_MIN_PE  =  ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×  =  ${EPP:.2f}
  (Below FY2022 actual $8.73; severe recession + raw material spike + housing collapse)
  Context: FY2020 COVID adj EPS was $7.36; $8.00 = realistic combined-shock trough
  EPP buffer: current ${CURRENT_PRICE:.2f} is +{epp_gap_pct:.1f}% above EPP — comfortable

METHOD B  (2-year forward)
  CONS_EPS_2YR × CONS_EXIT_PE  =  ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×  =  ${price_b:.2f}

RATIO B  (PRIMARY SIGNAL)
  (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})
  = ${CURRENT_PRICE - EPP:.2f} / ${price_b - CURRENT_PRICE:.2f}
  = {ratio_b:.3f}×   →   {signal}
  Fairly priced for the quality; not cheap enough for conviction; housing recovery = re-rate

SCENARIO PRICES
  BEAR     ${scenarios['BEAR']:>7.2f}   EPP; housing recession; raw material spike; $8.00 × 22×
  BASE     ${scenarios['BASE']:>7.2f}   FY2027E $12.00 × 28×; slow housing recovery; no re-rating
  BULL     ${scenarios['BULL']:>7.2f}   Method B; FY2027E $12.75 × 32×; housing normalises; premium
  XBULL    ${scenarios['XBULL']:>7.2f}   Housing recovery + repaint surge; $13.50 × 35×; peak cycle
""")

    print("SOFTMAX COMPOSITE ENGINE")
    print(f"  Market composite (inferred)  =  {market_composite:.3f}")
    print(f"  (Market near BASE — pricing in housing softness; minimal upside priced in)")

    print(f"""
SCA — SIGNAL CATALYST ADJUSTMENTS""")
    for desc, score, wt in sca_items:
        sign = "+" if score >= 0 else ""
        print(f"  {desc[:55]:<55}  {sign}{score:.2f} × {wt:.2f}  =  {score*wt:+.4f}")

    print(f"""
  sca_raw     =  {sca_raw:.4f}
  sca_adj     =  {sca_adj:.4f}  (= sca_raw / 2.0)
  adj_composite  =  {market_composite:.3f}  +  {sca_adj:.4f}  =  {adj_composite:.3f}
  (Near-neutral SCA: long-term quality + structural tailwinds offset housing headwinds)
""")

    print("SOFTMAX SCENARIO WEIGHTS  (at adj_composite = {:.3f})".format(adj_composite))
    for k, w in adj_weights.items():
        print(f"  {k:<10} {w*100:>5.1f}%   ${scenarios[k]:.2f}")

    ep_price = sum(adj_weights[k] * scenarios[k] for k in scenarios)
    print(f"\n  Expected price (probability-weighted)  =  ${ep_price:.2f}")

    print(f"""
BUSINESS METRICS
  FY2025 revenue                  = $23.57B  (+2.1% YoY; housing softness headwind)
  Q1 2026 revenue                 = $5.67B   (+6.8% YoY; beat estimates)
  Q1 2026 EBITDA                  = $998.2M  (+8.8% YoY; record Q1)
  Adj operating margin            = ~18–20%  (best-in-class vs PPG ~15%, RPM ~13%)
  Free cash flow (FY2025)         = $3.45B   (14.6% FCF margin — exceptional)
  Paint Stores Group stores       = 4,900+   (US-dominant; 80–100 new/yr)
  Net debt / adj EBITDA           = 2.5×     (within target; BBB+ credit)
  Dividend growth streak          = 47 consecutive annual increases
  Shareholder return Q1 2026      = $773M    (dividends + buybacks)
  FY2026 adj EPS guidance         = $11.50–$11.90 (+2.4% midpoint)
  Analyst consensus               = Buy; avg PT $380–$385 (+20–22%)
  52-wk low $294.32 (Apr 2026)    = ACCUMULATE at ratio_b 1.04×
  52-wk high $379.65              = AVOID at ratio_b 7.18×

SIGNAL ENTRY GUIDE""")

    thresholds = {}
    for label, rb in [("AVOID", 2.50), ("HOLD", 1.75), ("WATCH", 1.10), ("ACCUM", 0.75)]:
        thresholds[label] = (rb * price_b + EPP) / (1 + rb)

    print(f"  ✕ AVOID      above  ${thresholds['AVOID']:>3.0f}  (ratio_b > 2.50×)")
    print(f"  ▷ HOLD/TRIM  ${thresholds['HOLD']:>3.0f} – ${thresholds['AVOID']:>3.0f}  (ratio_b 1.75–2.50×)")
    print(f"  ◐ WATCHLIST  ${thresholds['WATCH']:>3.0f} – ${thresholds['HOLD']:>3.0f}  (ratio_b 1.10–1.75×)  ← current ${CURRENT_PRICE:.0f}  {signal}")
    print(f"  ◎ ACCUMULATE ${thresholds['ACCUM']:>3.0f} – ${thresholds['WATCH']:>3.0f}  (ratio_b 0.75–1.10×)")
    print(f"  ◉ BUY        below  ${thresholds['ACCUM']:>3.0f}  (ratio_b < 0.75×)")

    lo52 = 294.32
    rb52lo = (lo52 - EPP) / (price_b - lo52)
    hi52 = 379.65
    rb52hi = (hi52 - EPP) / (price_b - hi52)
    print(f"""
  52-wk low $294.32 (Apr 2026 tariff panic) = ACCUMULATE at ratio_b {rb52lo:.2f}×.
  52-wk high $379.65 = AVOID at ratio_b {rb52hi:.2f}×; well above current fair value zone.
  Analyst avg PT $380–$385 = in our AVOID zone — analysts are bullish but we need housing
  recovery to justify that price; $380 at 30× implies FY2027E EPS of $12.67+ already priced.
  KEY WATCH: US housing market data (existing home sales, starts); 30-yr mortgage rate.
  HOUSING RECOVERY THESIS: Rates → 5.5% = existing sales +20% → repaint trigger surge.
  ACCUMULATE on weakness ($279–$298): patience rewarded when rates normalise.""")
