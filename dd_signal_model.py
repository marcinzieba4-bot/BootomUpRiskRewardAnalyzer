"""
dd_signal_model.py — DuPont de Nemours Inc. (NYSE: DD)
'New DuPont' — Healthcare & Water + Diversified Industrials. Post-Qnity spinoff.
Signal framework: EPP floor + Method B + SCA softmax engine.

⚠ REVERSE SPLIT NOTE: 1-for-3 reverse stock split effective June 24, 2026.
  Pre-split: ~$49.18 / ~409M shares / FY2026E adj EPS ~$2.37
  Post-split: ~$147.54 / ~137M shares / FY2026E adj EPS ~$7.11
  All values in this model are on PRE-SPLIT basis (analysis date 2026-05-28).
"""

import math

# ── LIVE PRICE (fetched before model construction) ──────────────────────────
CURRENT_PRICE = 49.18    # DD — fetched from Yahoo Finance, 2026-05-28 (pre-split basis)
# (~$49.18 close May 26, 2026; 52-wk low $27.15, 52-wk high $52.66)
# ⚠ 1-for-3 REVERSE SPLIT effective June 24, 2026:
#   post-split equivalent price = $147.54; post-split EPS FY2026E = ~$7.11
# Market cap ~$20.1B; shares ~409M (pre-split); P/E ~20.7× FY2026E; yield ~1.6%

TICKER        = "DD"
COMPANY       = "DuPont de Nemours Inc."
SHARES_M      = 409          # million diluted shares (pre-split; ~137M post-June 24, 2026)
DIVIDEND_ANN  = 0.80         # USD/yr pre-split ($0.20/qtr); yield ~1.6% at $49.18
                              # Dividend cut from $1.64 → $0.80 in Nov 2025 alongside Qnity spinoff
                              # New payout ratio target: 35–45% of adj. net income
                              # Post-split equivalent: $2.40/yr on ~137M shares (same economic total)

# ── STRUCTURAL TRANSFORMATION CONTEXT ────────────────────────────────────────
# DuPont has completed a multi-year portfolio reshaping:
#   2019: Spun off Dow (commodity chemicals) and Corteva (agriculture)
#   Nov 2023: Divested Delrin (acetal homopolymer)
#   Aug 2023: Acquired Spectrum Plastics Group (~$1.75B) — medical device components
#   Jul 2024: Acquired Donatelle Plastics — precision medical molding
#   Nov 1, 2025: Spun off Qnity Electronics (NYSE: QNTY) — semiconductor materials,
#                PCB chemicals, advanced films — as independent company;
#                DD shareholders received 1 QNTY share per 2 DD shares held
#   Apr 1, 2026: Divested Aramids business (Kevlar + Nomex) to Arclin for ~$1.8B gross
#                ($1.2B cash + $300M note + $325M equity stake in Arclin)
#   Jun 24, 2026: 1-for-3 reverse stock split (pending)
#
# RESULT: DuPont is now a focused HEALTHCARE, WATER & SPECIALTY MATERIALS company
# Revenue ~$7.2B/yr; no commodity chemicals; no aerospace/defense aramids;
# no semiconductor materials. Two segments:
#   Healthcare & Water Technologies (~47% of revenue; ~30% EBITDA margin)
#   Diversified Industrials (~53% of revenue; ~23% EBITDA margin)

# ── EPS CONVENTION ───────────────────────────────────────────────────────────
# Adjusted EPS (non-GAAP). Excludes: restructuring/integration charges,
# acquisition/divestiture transaction costs, mark-to-market on derivatives,
# discrete tax items, and significant litigation provisions.
# All EPS figures below are PRE-REVERSE-SPLIT basis unless noted.
#
# ⚠ FY2022–FY2024 INCLUDE QNITY ELECTRONICS (now spun off as NYSE: QNTY).
# These years are NOT directly comparable to FY2026+ new DuPont.
# FY2025 is a TRANSITION YEAR (10 months old structure + 2 months new structure).
# FY2026 is the first CLEAN full year of new DuPont.

EPS_HISTORY = {
    "FY2022": 3.41,    # OLD DuPont (includes Qnity Electronics); copper wire, PCB materials,
                        # semiconductor materials all included; strong demand recovery
    "FY2023": 3.48,    # OLD DuPont; +0.2% despite -7% organic sales; Electronics down -11%;
                        # buybacks aided EPS; Healthcare & Water resilient; cost discipline
    "FY2024": 4.07,    # OLD DuPont; +17% EPS growth; Electronics recovery; Water & Healthcare both
                        # accelerating; last full year before Qnity spinoff; Spectrum/Donatelle integrating
    "FY2025": 1.68,    # TRANSITION YEAR — NOT COMPARABLE; mixed 10-month legacy + 2-month new structure;
                        # post-Qnity spinoff (Nov 1, 2025) dramatically changed revenue/profit base;
                        # ~$6.8B revenue (new DuPont annualised ~$6.8-7.0B)
}

# Q1 2026 (May 5, 2026): First CLEAN quarter of new DuPont — strong beat
# Adj EPS $0.55 (vs. $0.48E; +15% beat); Revenue $1.68B (+4% YoY, organic +2%)
# Operating EBITDA $414M (+15%); EBITDA margin 24.6% (+230bps YoY) — record
# Healthcare & Water: revenue $806M (+3% organic); EBITDA margin 30.3%
# Diversified Industrials: revenue $875M (flat organic); EBITDA margin 22.9%
# Aramids divestiture: completed April 1, 2026; $1.2B cash received; ASR initiated
# FY2026 guidance RAISED: adj EPS $2.35–$2.40 (from $2.25–$2.30; +$0.10 midpoint)
# Reverse split announced: 1-for-3 effective June 24, 2026

EPS_NOW       = 2.37     # FY2026E midpoint of raised guidance $2.35–$2.40 (pre-split basis)
                          # Q1 $0.55 × 4 = $2.20 annualised; H2 seasonally stronger;
                          # Aramids interest income + lower tax rate support H2 uplift
EPS_TROUGH    = 1.60     # mild recession scenario: construction down 20-25% (Tyvek wrap,
                          # Styrofoam, Corian); Healthcare/Water provides floor (non-discretionary);
                          # Context: COVID FY2020 (old DuPont) trough adj EPS ~$2.01 on ~2× revenue
                          # $1.60 = ~-33% from FY2026E run-rate; reflects blended defensiveness
EPP_MIN_PE    = 14        # specialty materials + healthcare/water blend — see rationale below
EPP           = EPP_MIN_PE * EPS_TROUGH   # = $22.40

CONS_EPS_2YR  = 2.51     # FY2027E consensus; +6% from FY2026E midpoint;
                          # Healthcare/Water growing 5%/yr; Industrials flat-to-modest recovery;
                          # Aramids divestiture EPS neutral (proceeds redeployed into buybacks)
CONS_EXIT_PE  = 24        # DuPont post-transformation: higher healthcare % deserves premium vs
                          # old DuPont's 19-20×; water treatment secular growth; Spectrum/Donatelle
                          # integration value; 24× = mid-range for specialty healthcare materials
price_b       = CONS_EPS_2YR * CONS_EXIT_PE   # = $60.24

ratio_b       = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
epp_gap_pct   = (CURRENT_PRICE - EPP) / EPP * 100

# Scenario prices (2-year forward targets)
scenarios = {
    "BEAR":  22,    # near EPP; construction recession + PFAS escalation + Healthcare decel
    "BASE":  46,    # FY2026E $2.37 × 19.5×; flattish construction; Healthcare 4-5%/yr growth
    "BULL":  60,    # Method B; FY2027E $2.51 × 24×; Healthcare/Water premium; synergies
    "XBULL": 75,    # DuPont achieves full healthcare specialty re-rate; $3.00 × 25×
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
    ("Healthcare & Water Technologies — defensive growth engine: Tyvek "
     "medical packaging (sterile barrier for medical devices; Tyvek = FDA-mandated "
     "standard for 90%+ of medical device packaging), FILMTEC reverse osmosis membranes "
     "(world leader in desalination), Spectrum/Donatelle medical device components. "
     "~47% of revenue at ~30% EBITDA margin. Non-discretionary demand; growing 5%/yr.",
     +0.25, 0.25),
    ("Reverse split + buyback signaling capital discipline: 1-for-3 split June 24, "
     "2026 expands institutional eligibility; $275M accelerated share repurchase "
     "from Aramids cash reduces shares by ~$275M/~$49 = ~5.6M shares; management "
     "returned to growth M&A + buyback + dividend payout ratio discipline.",
     +0.15, 0.15),
    ("PFAS liability substantially quantified: $1.185B public water system settlement "
     "(payments through 2026 claims deadline June 30); $875M NJ NRD settlement "
     "(25-year payments); $27M Hoosick Falls; known structured obligations, not "
     "open-ended. While tail risk remains, the major exposures are ring-fenced.",
     +0.15, 0.10),
    ("Near 52-wk high after near-doubling from $27 post-spinoff panic low. "
     "Stock has recovered most of the Qnity spinoff dislocation. Method B ($60.24) "
     "is only +22% above current. Analyst avg PT $55-56 is BELOW price_b. "
     "Limited near-term re-rating catalyst; market has largely priced the transition.",
     -0.25, 0.25),
    ("Diversified Industrials (~53% of revenue; ~23% EBITDA margin) faces "
     "construction headwinds: Tyvek house wrap + Styrofoam insulation + Corian "
     "surfaces all tied to new residential construction which remains depressed by "
     "high mortgage rates. FY2026E organic growth only +2-4%; recovery catalyst unclear.",
     -0.25, 0.15),
    ("EPS growth trajectory modest: FY2026E $2.37 → FY2027E $2.51 = +6%/yr. "
     "M&A integration costs (Spectrum $1.75B + Donatelle) creating near-term dilution. "
     "Qnity spinoff removed the highest-growth Electronics segment. New DuPont must "
     "prove Healthcare/Water can sustain the organic growth narrative.",
     -0.20, 0.10),
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
    print("DUPONT DE NEMOURS INC. (DD) — SIGNAL MODEL")
    print("'New DuPont': Healthcare & Water + Diversified Industrials.")
    print("⚠ 1-for-3 REVERSE SPLIT effective June 24, 2026 (all values pre-split basis)")
    print(SEP)

    print("""
SIGNAL FRAMEWORK — METHOD B + SCA ENGINE
─────────────────────────────────────────
EPP  = EPS_TROUGH × EPP_MIN_PE          (structural floor; adjusted EPS basis)
Ratio B = (Price − EPP) / (price_b − Price)

DD EPS convention: Adjusted EPS (non-GAAP). Excludes restructuring charges,
acquisition/divestiture transaction costs, discrete tax items, mark-to-market
on commodity derivatives, and material litigation provisions. GAAP EPS is
substantially lower due to ongoing restructuring charges from the portfolio
transformation and Qnity spinoff-related costs.

⚠ PRE-SPLIT vs POST-SPLIT:
  1-for-3 reverse split effective June 24, 2026.
  All prices/EPS in this model are PRE-SPLIT ($49.18, $2.37 FY2026E, etc.)
  Post-split equivalents: price ~$147.54; FY2026E EPS ~$7.11 (×3 every metric)
  P/E ratio is unchanged by the split; framework conclusions are unchanged.

SIGNAL THRESHOLDS
  Ratio B < 0.75   →  ◉ BUY
  0.75 – 1.10      →  ◎ ACCUMULATE
  1.10 – 1.75      →  ◐ WATCHLIST
  1.75 – 2.50      →  ▷ HOLD/TRIM
  > 2.50           →  ✕ AVOID

EPP_MIN_PE = 14×  rationale:
  The new DuPont is a blended portfolio — partly defensive (Healthcare/Water)
  and partly cyclical (construction in Diversified Industrials). 14× reflects:
  (1) HEALTHCARE FLOOR: Tyvek medical packaging is the sterile barrier of
      choice for ~90% of medical device packaging globally. FDA Class II/III
      device manufacturers cannot simply switch barrier materials — validation
      is multi-year and the regulatory risk of switching is prohibitive. This
      portion of the business (Healthcare & Water ~47% of revenue) acts like
      a pharmaceutical ingredient supplier — highly recurring, non-discretionary.
      The FILMTEC RO membrane business provides similar water-infrastructure stickiness.
  (2) CONSTRUCTION CYCLICALITY: Tyvek wrap, Styrofoam insulation, and Corian
      surfaces are tied to new residential and commercial construction — genuinely
      cyclical. In a recession with -20-25% construction volumes, this segment
      would see meaningful margin compression.
  (3) PFAS TAIL: While substantially ring-fenced via settlement, PFAS creates
      an ongoing litigation overhead that prevents the premium of a pure healthcare
      company (which might warrant 20-22× at trough).
  (4) TRANSITION DISCOUNT: DuPont is still proving the post-Qnity narrative.
      FY2026 is the first clean year; integration of Spectrum/Donatelle is
      ongoing. Until the growth algorithm is demonstrated over 2-3 years,
      a 14× trough multiple is appropriate (peer Ashland Global ~12×; Avery
      Dennison ~14× at trough; Sealed Air ~12-15× trough).
  14× = appropriate for a specialty materials company with defensive/cyclical mix
  and a known-but-quantified litigation overhang.
""")

    print("DUPONT DE NEMOURS INC. (DD) — THE SPECIALTY MATERIALS COMPANY AFTER THE GREAT RESTRUCTURING")
    print("=" * 70)

    print("""
BUSINESS OVERVIEW
─────────────────
DuPont de Nemours was founded in 1802 as a gunpowder mill and is one of the
oldest industrial companies in America. The current "new DuPont" is the product
of a decade of portfolio transformation: spinning off Dow (2019), Corteva (2019),
Qnity Electronics (2025), and divesting Kevlar/Nomex Aramids (2026). What remains
is a ~$7.2B revenue specialty materials and services company with two segments.

Headquarters: Wilmington, Delaware. CEO: Lori Koch (CFO 2020–2024; elevated to
President & CEO 2024; deep DuPont lifer with intimate knowledge of each spinoff
decision). Market cap: ~$20.1B at $49.18.

The investment thesis: DuPont has systematically removed commodity exposure
(Dow), agricultural cyclicality (Corteva), semiconductor materials (Qnity), and
defense-adjacent aramids (Kevlar/Nomex) — leaving a more predictable, regulated,
and margins-expanding portfolio. The question is whether the Healthcare & Water
growth engine can sustain ~5%/yr organic growth to justify a premium multiple.

TWO SEGMENTS: THE NEW EARNINGS ENGINE
──────────────────────────────────────────────────────────────────────

  HEALTHCARE & WATER TECHNOLOGIES  (~47% of revenue; ~30% EBITDA margin)
  ──────────────────────────────────────────────────────────────────────
  The highest-quality, most defensive segment. Four sub-businesses:

  TYVEK MEDICAL (Sterile Barrier Packaging) — Crown Jewel
  DuPont's Tyvek spunbonded polyolefin is the industry-standard material for
  sterile medical device packaging. FDA requires sterile barrier validation under
  ISO 11607; once a device manufacturer validates packaging to Tyvek specifications,
  re-validation to a competitor's material costs $500K–$2M and 12–24 months.
  This creates switching costs comparable to pharmaceutical APIs.
  Markets: syringes, surgical kits, IV bags, implant packaging, ETO sterilisation
  pouches. DuPont operates dedicated Tyvek capacity expansions (Luxembourg
  ~$400M facility completed early 2026). No meaningful global substitute.

  SPECTRUM PLASTICS GROUP + DONATELLE PLASTICS (Medical Device Components)
  Acquired Aug 2023 ($1.75B) + Jul 2024; now the #2 diversified medical device
  components platform (behind Integer Holdings):
    Spectrum: structural heart, electrophysiology catheters, surgical robotics,
              fluid management, minimally invasive surgery components
    Donatelle: precision injection molding, liquid silicone rubber (LSR) components
  These businesses provide long-term supply agreements with device OEMs (Medtronic,
  Abbott, Stryker, BD) — recurring revenue with 5–10 year supply contracts.

  FILMTEC (Reverse Osmosis / Nanofiltration Membranes) — Water Winner
  World's leading RO membrane for industrial and municipal water treatment:
  desalination (MENA, Asia), wastewater reuse (semiconductor fabs, power plants,
  food/beverage), municipal drinking water. Water scarcity secular tailwind.
  Q1 2026: water muted by Middle East logistics disruption (MENA project delays);
  recovery expected H2 2026 as project deliveries normalise.

  AMBERLITE + INGE + LIVEO (Ion Exchange, Ultrafiltration, Liquid Silicone)
  Specialty water treatment resins and modules; healthcare silicone applications.

  DIVERSIFIED INDUSTRIALS  (~53% of revenue; ~23% EBITDA margin)
  ──────────────────────────────────────────────────────────────────────
  More cyclical end-markets; construction is the primary sensitivity:

  TYVEK HOUSE WRAP + STYROFOAM + CORIAN (Building/Construction)
  - Tyvek wrap: weatherisation barrier for ~30% of new US residential construction
  - Styrofoam: rigid thermal insulation for walls/roofs (brand name; DuPont owns it)
  - Corian: solid surface countertops (commercial + residential)
  These are NEW CONSTRUCTION driven — sensitive to mortgage rates and housing starts.
  Current headwind: high rates depressing new residential; commercial mixed.

  VESPEL + MOLYKOTE + BETAFORCE/BETASEAL (High-Performance Industrials)
  - Vespel: high-temperature/pressure polymer shapes for aerospace, semiconductor fabs
  - Molykote: specialty lubricants and greases for automotive/industrial MRO
  - Betaforce/Betaseal: structural adhesives for automotive and aerospace bonding
  These serve aerospace + auto — relatively resilient; modest growth.

  PRINTING / PACKAGING SPECIALTY MATERIALS
  Specialty resins, laminates, and release films for flexible packaging and
  commercial printing. Q1 2026: weak (printing volumes declining; packaging mixed).

THE PFAS OVERHANG — KNOWN AND MOSTLY QUANTIFIED
──────────────────────────────────────────────────
DuPont faces legacy PFAS (per- and polyfluoroalkyl substances) liabilities from
its historical Teflon and other fluoropolymer manufacturing:

  MAJOR SETTLEMENTS:
  $1.185B — Public Water Systems: settlement for water utilities with PFAS
             contamination; claims deadline June 30, 2026; structured payments.
  $875M    — New Jersey NRD: natural resource damages settlement; paid over 25 years.
  $27M     — Hoosick Falls (NY): community contamination; finalised April 2026.

  The 2025 3M settlement (separate company) set a market precedent for PFAS
  liability quantification. DuPont's obligations are structured and scheduled —
  no longer open-ended surprise risk. The PFAS overhang is PRICED IN to the
  current multiple discount vs. pure healthcare peers.

  REMAINING RISK: Individual lawsuits (personal injury) continue; the "claims
  deadline" structure should limit future exposure but this tail cannot be fully
  eliminated. Manageable, not existential, at current settlement rates.

THE REVERSE SPLIT — WHAT IT MEANS (AND WHAT IT DOESN'T)
──────────────────────────────────────────────────────────
June 24, 2026: Every 3 DD shares → 1 DD share.
  Pre-split price ~$49 → Post-split price ~$147
  Pre-split EPS $2.37 → Post-split EPS $7.11
  Pre-split shares ~409M → Post-split shares ~137M
  P/E ratio: UNCHANGED (same underlying economics)

Why DuPont is doing it:
  "We are executing this reverse stock split to enhance our appeal to a
  broader investor base." — DuPont May 2026 press release
  Many institutional mandates have minimum price thresholds (~$100/share).
  At ~$49/share, DuPont is excluded from some index fund reconstitution criteria.
  The reverse split is NOT a sign of business distress — DuPont's per-share
  price is low because it has distributed two companies (Dow, Corteva) and spun
  off Qnity, each time distributing value to shareholders as separate securities.

FINANCIAL PROFILE: MARGIN EXPANSION STORY
──────────────────────────────────────────
  FY2026E Revenue:         ~$7.2B    (raised guidance $7.155–$7.215B)
  EBITDA margin:           ~24-25%  (Q1 2026: record 24.6%; expanding)
  Operating CF:            ~$1.5B   (after capex and working capital)
  Net debt:                ~$2.4B   ($3.1B debt − $0.71B cash; post-Aramids improvement)
  Post-Aramids improvement: +$1.2B cash in + $275M ASR buyback out
  Target: 35-45% payout ratio; ~$1B+ annual free cash flow
  Capex:                   ~$0.7B   (Luxembourg Tyvek + Spectrum integration)
  ROIC:                    ~12-14%  (improving as M&A synergies materialise)

Q1 2026 — FIRST CLEAN NEW DUPONT QUARTER
──────────────────────────────────────────
  Adj EPS (pre-split): $0.55   (+15% beat vs. $0.48E)
  Revenue:             $1.68B  (+4% YoY; organic +2%; currency +2%)
  EBITDA:              $414M   (+15% YoY; RECORD Q1 EBITDA margin 24.6%)
  Healthcare & Water:  $806M   (+3% organic; 30.3% EBITDA margin — expanding)
  Diversified Indust:  $875M   (flat organic; 22.9% EBITDA margin)
  Aramids closed Apr 1; $275M ASR initiated with cash proceeds
  FY2026 guidance RAISED to $2.35–$2.40 (from $2.25–$2.30)

FY2026 GUIDANCE (RAISED, POST-Q1):
  Net Sales:   $7.155–$7.215B  (~4% organic growth; ~1% pricing)
  EBITDA:      $1.725–$1.755B
  Adj EPS:     $2.35–$2.40 (pre-split; $7.05–$7.20 post-split equivalent)
  Q2 2026E:    adj EPS ~$0.59 implied (post-split: ~$1.75)
""")

    print(DASH)
    print("EPS HISTORY  (Adjusted Diluted EPS, non-GAAP, PRE-SPLIT basis)")
    print("NOTE: FY2022–FY2024 include Qnity Electronics (now NYSE: QNTY) — NOT COMPARABLE")
    print(DASH)
    for yr, eps in EPS_HISTORY.items():
        note = "  ← OLD DuPont (includes Qnity)" if yr in ("FY2022","FY2023","FY2024") else "  ← TRANSITION YEAR (10-month legacy + 2-month new structure)"
        print(f"  {yr}  ${eps:.2f}{note}")
    print(f"  FY2026E ${EPS_NOW:.2f}  (new DuPont guidance $2.35–$2.40; Q1 $0.55 = +15% beat; first clean year)")
    print(f"  FY2027E $2.51  (consensus; +6% YoY; Healthcare/Water growth + Industrials normalisation)")
    print(f"  POST-SPLIT FY2026E: ~$7.11/sh (×3 for 1-for-3 split; same economic value)")

    print(f"""
EPP CALCULATION
  EPS_TROUGH × EPP_MIN_PE  =  ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×  =  ${EPP:.2f}
  (Mild recession: construction -20-25%, Healthcare/Water resilient at ~$3.5B revenue;
   blended EBITDA falls to ~$1.1-1.2B; ~$650M net income / 409M shares = ~$1.59/sh)
  Context: COVID FY2020 old DuPont (2× size) trough adj EPS was ~$2.01; Healthcare
  floor is genuine; $1.60 is a real but not catastrophic recession scenario
  EPP buffer: current ${CURRENT_PRICE:.2f} is +{epp_gap_pct:.1f}% above EPP

METHOD B  (2-year forward)
  CONS_EPS_2YR × CONS_EXIT_PE  =  ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×  =  ${price_b:.2f}
  (FY2027E $2.51 at 24× = premium vs old DuPont's historical 19-20× forward P/E,
   justified by higher Healthcare/Water mix and water scarcity secular tailwind)

RATIO B  (PRIMARY SIGNAL)
  (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})
  = ${CURRENT_PRICE - EPP:.2f} / ${price_b - CURRENT_PRICE:.2f}
  = {ratio_b:.3f}×   →   {signal}
  Close to AVOID threshold; recovery from $27 post-spinoff low largely complete

NOTE: ratio_b is {ratio_b:.3f}× vs. AVOID threshold 2.50× — stock is in HOLD/TRIM
territory but only 8 cents per share below the AVOID threshold. Treat as borderline.

SCENARIO PRICES
  BEAR     ${scenarios['BEAR']:>7.2f}   near EPP; recession + construction collapse + PFAS escalation
  BASE     ${scenarios['BASE']:>7.2f}   FY2026E $2.37 × 19.5×; flattish construction; Healthcare +4-5%
  BULL     ${scenarios['BULL']:>7.2f}   Method B; FY2027E $2.51 × 24×; Healthcare premium re-rate
  XBULL    ${scenarios['XBULL']:>7.2f}   DuPont 3.0 re-rate; $3.00 × 25×; full specialty healthcare premium
""")

    print("SOFTMAX COMPOSITE ENGINE")
    print(f"  Market composite (inferred)  =  {market_composite:.3f}")
    print(f"  (Market between BASE-BULL — pricing in Healthcare/Water quality at ~21× FY2026E)")

    print(f"""
SCA — SIGNAL CATALYST ADJUSTMENTS""")
    for desc, score, wt in sca_items:
        sign = "+" if score >= 0 else ""
        print(f"  {desc[:55]:<55}  {sign}{score:.2f} × {wt:.2f}  =  {score*wt:+.4f}")

    print(f"""
  sca_raw     =  {sca_raw:.4f}
  sca_adj     =  {sca_adj:.4f}  (= sca_raw / 2.0)
  adj_composite  =  {market_composite:.3f}  +  {sca_adj:.4f}  =  {adj_composite:.3f}
  (Slightly negative SCA: construction headwinds + limited EPS growth offset
   Healthcare/Water quality + PFAS ring-fencing; near-neutral overall)
""")

    print("SOFTMAX SCENARIO WEIGHTS  (at adj_composite = {:.3f})".format(adj_composite))
    for k, w in adj_weights.items():
        print(f"  {k:<10} {w*100:>5.1f}%   ${scenarios[k]:.2f}")

    ep_price = sum(adj_weights[k] * scenarios[k] for k in scenarios)
    print(f"\n  Expected price (probability-weighted)  =  ${ep_price:.2f}")

    print(f"""
BUSINESS METRICS
  FY2026E revenue (raised)        = $7.155–$7.215B (~4% organic)
  Q1 2026 revenue                 = $1.68B  (+4% YoY; organic +2%)
  Q1 2026 EBITDA margin           = 24.6%   (record; +230bps YoY)
  Healthcare & Water margin       = 30.3%   (expanding; Q1 2026)
  Diversified Industrials margin  = 22.9%   (stable; construction offset by auto/aero)
  Net debt (Q1 2026)              = ~$2.4B  (post-Aramids: improving)
  Aramids proceeds                = $1.2B cash + $300M note + $325M equity (Apr 2026)
  Active buyback: $275M ASR       (from Aramids proceeds; underway)
  Annual dividend                 = $0.80/sh pre-split ($2.40 post-split)
  Diluted shares                  = ~409M pre-split (~137M post-June 24)
  Reverse split effective         = June 24, 2026 (1-for-3)
  Post-split FY2026E adj EPS      = $7.02–$7.16 (company stated)
  PFAS settlements                = $1.185B public water + $875M NJ NRD + others
  Analyst consensus               = Strong Buy (15B/2H/0S); avg PT $55–56 (+12-14%)
  52-wk low $27.15 (Nov 2025)     = ◉ BUY at ratio_b 0.21× (post-Qnity dislocation)
  52-wk high $52.66 (Feb 2026)    = ✕ AVOID at ratio_b 3.99×

SIGNAL ENTRY GUIDE""")

    thresholds = {}
    for label, rb in [("AVOID", 2.50), ("HOLD", 1.75), ("WATCH", 1.10), ("ACCUM", 0.75)]:
        thresholds[label] = (rb * price_b + EPP) / (1 + rb)

    print(f"  ✕ AVOID      above  ${thresholds['AVOID']:>5.2f}  (ratio_b > 2.50×)")
    print(f"  ▷ HOLD/TRIM  ${thresholds['HOLD']:>5.2f} – ${thresholds['AVOID']:>5.2f}  (ratio_b 1.75–2.50×)  ← current ${CURRENT_PRICE:.2f}  {signal}")
    print(f"  ◐ WATCHLIST  ${thresholds['WATCH']:>5.2f} – ${thresholds['HOLD']:>5.2f}  (ratio_b 1.10–1.75×)")
    print(f"  ◎ ACCUMULATE ${thresholds['ACCUM']:>5.2f} – ${thresholds['WATCH']:>5.2f}  (ratio_b 0.75–1.10×)")
    print(f"  ◉ BUY        below  ${thresholds['ACCUM']:>5.2f}  (ratio_b < 0.75×)")

    lo52 = 27.15
    rb52lo = (lo52 - EPP) / (price_b - lo52)
    hi52 = 52.66
    rb52hi = (hi52 - EPP) / (price_b - hi52)
    print(f"""
  52-wk low $27.15 (Nov 2025 post-Qnity spinoff panic) = ◉ BUY at ratio_b {rb52lo:.2f}×.
  52-wk high $52.66 (Feb 12, 2026) = ✕ AVOID at ratio_b {rb52hi:.2f}×.
  ⚠ Current $49.18 ratio_b {ratio_b:.2f}× — BORDERLINE (AVOID threshold = ${thresholds['AVOID']:.2f}).
  Analyst avg PT $55–56 is BELOW our price_b ($60.24) — consensus targets are not bullish enough
  to close the gap to Method B; requires Healthcare/Water organic growth proof in H2 2026.
  KEY WATCH: Healthcare & Water organic growth execution (target 5%/yr); Q2 2026 is first
  quarter including full Aramids divestiture economics; Middle East water project normalisation.
  PFAS claims deadline June 30, 2026 — important structural milestone (ring-fencing liability).
  REVERSE SPLIT June 24 — mechanical event only; thesis unchanged; new $147 post-split price.
  BEST ENTRY: Next construction downturn or PFAS headline panic → WATCHLIST $43-47;
  ACCUMULATE $39-43; BUY below $39 (post-split equivalent: ACCUM ~$117-129; BUY <$117).""")
