"""
lin_signal_model.py — Linde plc (NASDAQ: LIN)
World's largest industrial gas company. Oligopoly. Take-or-pay contracts. Clean energy.
Signal framework: EPP floor + Method B + SCA softmax engine.
"""

import math

# ── LIVE PRICE (fetched before model construction) ──────────────────────────
CURRENT_PRICE = 516.00    # LIN — fetched from Yahoo Finance / CNBC, 2026-05-27
# ($515.90 as of May 26, 2026; 52-wk ATH $521.28 on May 1, 2026)
# 52-wk range: $387.78 (Apr 2026 tariff-shock low) – $521.28 (ATH May 1, 2026)
# Market cap ~$238.4B; shares ~463M; dividend yield ~1.24%

TICKER        = "LIN"
COMPANY       = "Linde plc"
SHARES_M      = 463          # million diluted shares (462.60M as of Q1 2026)
DIVIDEND_ANN  = 6.40         # USD/yr; $1.60/quarter; ~16th consecutive annual increase
                              # yield = 1.24% at $516; modest but consistent compounder

# ── EPS CONVENTION ───────────────────────────────────────────────────────────
# Adjusted EPS — Linde's non-GAAP metric. Excludes:
#   - Amortisation of acquisition-related intangibles (large after Praxair merger)
#   - Restructuring charges / plant divestitures required post-merger by EU regulators
#   - Pension settlement gains/losses
#   - FX mark-to-market on balance sheet items
# GAAP EPS is materially lower due to ongoing intangible amortisation from the
# 2018 Praxair-Linde merger (still working through the P&L in 2026).
# Adjusted EPS is the correct lens for business earning power.

EPS_HISTORY = {
    "FY2022": 12.29,   # +15% YoY; pricing tailwind as post-COVID industrials recover
    "FY2023": 14.20,   # +16% YoY; pricing + efficiency; merger synergies fully captured
    "FY2024": 15.51,   # +9% YoY; volume softness in Europe/APAC; FX headwind ~2%
    "FY2025": 16.46,   # +6% YoY; actual (reported Feb 5, 2026); FX remained a headwind;
                        #   Q4 2025: $4.20 (+6% YoY); FY sales $35.1B (+6%); margin expansion
}

# Q1 2026: Adj EPS $4.33 (+10% YoY); revenue $8.78B (+8%); beat Zacks consensus $4.27 by 1.41%
# Operating profit $2.63B; operating margin 30.0% (expanding YoY)
# FY2026 guidance: $17.40–$17.90 adj EPS (7–9% growth); Q2 2026 guide: $4.40–$4.50

EPS_NOW       = 17.75    # NTM; midpoint of FY2026 guidance $17.40–$17.90; consensus $17.86
                          # Q1 2026 annualised: $4.33 × 4 = $17.32 (slightly below guidance)
EPS_TROUGH    = 13.00    # severe recession scenario: volume collapse in industrial/construction
                          # + FX headwinds (LIN ~40% non-USD revenue) + capex impairment;
                          # ~FY2022 adj EPS level ($12.29) adjusted up for today's higher
                          # operating base; take-or-pay floors and medical/electronics volumes
                          # prevent genuine earnings collapse below ~$12-13
EPP_MIN_PE    = 22        # industrial gas oligopolist with take-or-pay contracts and
                          # on-site infrastructure — see detailed rationale below
EPP           = EPP_MIN_PE * EPS_TROUGH   # = $286.00

CONS_EPS_2YR  = 19.30    # FY2027E analyst consensus (Erste Group raised to $19.45 post Q1 2026
                          # beat; broader consensus range $18.80–$19.45; I use $19.30 as mid)
CONS_EXIT_PE  = 30        # bull case exit multiple: LIN historically trades 27–34× forward;
                          # 30× = premium maintained for oligopoly + clean energy growth + margin
                          # expansion; slightly below current 34× trailing (de-rating built in)
price_b       = CONS_EPS_2YR * CONS_EXIT_PE   # = $579.00

ratio_b       = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
epp_gap_pct   = (CURRENT_PRICE - EPP) / EPP * 100

# Scenario prices (2-year forward targets)
scenarios = {
    "BEAR":  286,    # EPP; recession + FX; EPS compresses to $13; multiple 22×; trough of troughs
    "BASE":  480,    # FY2027E $18.50 × 26×; consensus earnings; slight multiple de-rate from 29× fwd;
                     # NB: BASE at $480 < current $516 — market is pricing above the consensus base case
    "BULL":  579,    # Method B; FY2027E $19.30 × 30×; premium maintained; clean energy ramp
    "XBULL": 700,    # H2 economy inflection + AI semiconductor gas boom; ~$21.9 × 32×; full re-rate
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
    ("Oligopoly moat: Linde + Air Products + Air Liquide = ~75% global market. "
     "Once an ASU is built on-site (cost $50M–$500M), customers cannot switch — "
     "dismantling and rebuilding is economically impossible. Zero customer churn.",
     +0.35, 0.25),
    ("Clean energy backlog $10B total ($2.5–3B starting revenue 2026): hydrogen "
     "production (green + blue), carbon capture, clean fuel processing. Secular "
     "10-20yr tailwind from global decarbonisation mandates.",
     +0.30, 0.20),
    ("AI semiconductor specialty gas demand: chip fabs require ultra-high-purity "
     "N2, O2, Ar, specialty dopants — all LIN's products. Every new AI fab = "
     "10+ year LIN gas supply contract. TSMC, Samsung, Intel expansions.",
     +0.20, 0.15),
    ("Trading near ATH ($516 vs $521.28 ATH May 2026); 34× trailing EPS; 29× "
     "FY2026E; analyst avg PT $541–553 = only 5–7% upside. Priced for "
     "perfection — no margin of safety at current levels.",
     -0.40, 0.30),
    ("BASE scenario ($480) is BELOW the current stock price ($516): market has "
     "already priced above the consensus 2-yr base case. Any disappointment "
     "in clean energy ramp or macro softness = meaningful downside.",
     -0.30, 0.20),
    ("Multiple compression risk: 29× forward earnings yields only 3.4% vs "
     "4.5–5% risk-free rate. Long-duration premium valuation is most vulnerable "
     "to rates staying elevated longer than market expects.",
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
    print("LINDE PLC (LIN) — SIGNAL MODEL")
    print("World's largest industrial gas company. Oligopoly. Take-or-pay. Clean energy.")
    print(SEP)

    print("""
SIGNAL FRAMEWORK — METHOD B + SCA ENGINE
─────────────────────────────────────────
EPP  = EPS_TROUGH × EPP_MIN_PE          (structural floor; adjusted EPS basis)
Ratio B = (Price − EPP) / (price_b − Price)

LIN EPS convention: Adjusted EPS. Excludes amortisation of acquisition-related
intangibles from the 2018 Praxair-Linde AG merger (the largest-ever chemicals
merger; ~$90B combined entity). GAAP EPS is significantly lower due to ongoing
intangible amortisation working through the P&L. Adjusted EPS is the accepted
standard across the industrial gas sector and used by all three major peers
(LIN, APD, Air Liquide) for comparability.

SIGNAL THRESHOLDS
  Ratio B < 0.75   →  ◉ BUY
  0.75 – 1.10      →  ◎ ACCUMULATE
  1.10 – 1.75      →  ◐ WATCHLIST
  1.75 – 2.50      →  ▷ HOLD/TRIM
  > 2.50           →  ✕ AVOID

EPP_MIN_PE = 22×  rationale:
  Linde operates the world's most defensible industrial infrastructure:
  (1) ON-SITE PLANTS: Linde builds air separation units (ASUs) directly at
      customer facilities (steel mills, chip fabs, hospitals). Once installed,
      the customer CANNOT switch suppliers — dismantling and rebuilding costs
      $50M–$500M and takes 2–4 years. Customer churn is essentially zero.
  (2) TAKE-OR-PAY CONTRACTS: 10–20 year contracts require customers to pay
      for minimum volumes regardless of actual usage. Even in a recession,
      Linde's revenue floor is contractually guaranteed.
  (3) CRITICAL INPUTS: Medical oxygen (hospitals cannot run without it),
      semiconductor fabrication gases (cannot make chips without N2/Ar), and
      steel production (oxygen injection) = demand never goes to zero.
  (4) OLIGOPOLY: Three companies (LIN/APD/Air Liquide) control ~75% of the
      global market. No new entrant has successfully challenged this structure
      in 40+ years. Scale and safety certification barriers are prohibitive.
  22× = premium over peers without take-or-pay (vs PYPL at 10×, MRSH at 18×)
  reflecting the uniquely durable earnings floor. In the 2009 GFC, Air Products
  and Praxair (LIN's predecessor) never fell below 16–18× forward earnings.
  22× = appropriate severe-stress multiple for an oligopoly infrastructure business.
""")

    print("LINDE PLC (LIN) — AN OUTSTANDING BUSINESS AT AN OUTSTANDING PRICE")
    print("=" * 70)

    print("""
BUSINESS OVERVIEW
─────────────────
Linde plc was formed in 2018 through the merger of Linde AG (German; founded 1879)
and Praxair (US; ~$35B market cap pre-merger). The combined entity is the world's
largest industrial gas company by revenue (~$35B/yr) and market cap (~$238B).
Headquarters: Dublin, Ireland (legal domicile). Operations: 100+ countries.
CEO: Sanjiv Lamba (since 2022, previously COO). Trades on NASDAQ (LIN) and
Frankfurt Stock Exchange (LIN.DE). Dividend: $1.60/quarter (+16th consecutive
annual increase). FY2025 adj EPS $16.46; FY2026 guidance $17.40–$17.90 (+7–9%).

INDUSTRIAL GASES: THE INVISIBLE INFRASTRUCTURE
───────────────────────────────────────────────
Linde produces and distributes atmospheric gases (oxygen, nitrogen, argon) and
process gases (hydrogen, helium, carbon dioxide, specialty electronic gases). These
are the hidden inputs without which modern industrial civilisation cannot function:

  OXYGEN (O2)
  ─────────────────────────────────────────────
  Medical: Hospitals depend on a continuous oxygen supply — literally life-critical.
  Steel: Oxygen injection (BOF) is how steel is made; no oxygen = no steel.
  Chemicals: Oxidation reactions in petrochemical production.
  Demand driver: population growth, aging demographics (medical), electrification
  (steel for EV and grid infrastructure).

  NITROGEN (N2)
  ─────────────────────────────────────────────
  Semiconductor fabrication: N2 is the blanket gas in fabs — used to purge
  oxygen from equipment and prevent oxidation. A single leading-edge fab uses
  1,000+ tons/day. Every new AI data centre fab = 10+ year LIN supply contract.
  Food preservation: Modified atmosphere packaging (MAP); cold chain logistics.
  Chemical processing: Inert blanketing to prevent explosions.

  HYDROGEN (H2)
  ─────────────────────────────────────────────
  Today: Refineries use hydrogen for hydrotreating/desulfurisation of fuels.
  Tomorrow: Clean energy carrier. Linde is the world's #1 hydrogen producer
  (both grey and green/blue). The $10B clean energy backlog is overwhelmingly H2.
  Green H2 projects require Linde's electrolysis technology and distribution.
  Blue H2: natural gas reforming + carbon capture — already in Linde's backlog.

  SPECIALTY / ELECTRONIC GASES
  ─────────────────────────────────────────────
  Ultra-high-purity gases for semiconductor manufacturing: silane (SiH4),
  germane, tungsten hexafluoride, specialty dopants. Niche but HIGH MARGIN.
  AI chip demand surge (TSMC N3/N2 nodes, Intel 18A, Samsung GAA) = structural
  demand acceleration for Linde's highest-margin gas category.
  Also: medical specialty gases (anaesthetics), calibration gas standards.

THREE DELIVERY MODELS — THE MOAT ARCHITECTURE
───────────────────────────────────────────────
  ON-SITE (largest; highest margin; zero churn):
    Linde builds and OWNS the gas production plant on the customer's premises.
    Customer signs 15–20 year take-or-pay contract with minimum volume guarantees.
    At contract end, customer almost always renews (cost of switching = rebuild).
    ~60% of Linde's revenue. THE STRUCTURAL MOAT.

  MERCHANT (cylinders/dewars/bulk tanker delivery):
    Gases produced at Linde's own plants, liquefied, and delivered to customers
    too small for on-site plants (hospitals, labs, small manufacturers).
    More competitive than on-site but local distribution networks provide moat.
    ~25% of revenue. Durable, recurring, logistics-intensive.

  PACKAGED GAS (specialty cylinders):
    High-pressure cylinders of specialty/rare gases. Highest margin/unit.
    Medical gas, laboratory standards, electronics. ~15% of revenue.
    Less volume-sensitive; primarily priced on purity and certification.

FINANCIAL PROFILE: MARGIN MACHINE
───────────────────────────────────
Linde is one of the highest-quality industrials in the world on margin metrics:

  FY2025 Revenue:           ~$35.1B  (+6% YoY; organic growth 3–4% + FX ~2%)
  Operating margin:          ~30%    (30.0% in Q1 2026; best-in-class industrials)
  EBITDA margin:             ~35%+   (the gas business is inherently capital-efficient
                                      once plants are installed; D&A is large but plants
                                      run for 30+ years with minimal incremental capex)
  FCF conversion:            ~80%+ of net income; LIN generates $6–7B FCF/yr
  Capital return programme:  $3–4B/yr buybacks + $3B/yr dividends = 25–30% of market cap
                              returned per 5 years at current prices
  Net debt / EBITDA:         ~1.2×   (conservative leverage; AA– / A1 credit rated)

THE CLEAN ENERGY TRANSITION: THE LONG-TERM CATALYST
──────────────────────────────────────────────────────
Linde is uniquely positioned across every decarbonisation pathway:

  HYDROGEN ECONOMY
  Linde is the world's #1 merchant hydrogen producer and the leading pure-play
  on the hydrogen energy transition. Current backlog:
    Total project backlog:     ~€4.5B  (as of Q1 2026)
    Sale-of-Gas backlog:       $7.1B   (long-term SOG projects locked in)
    Total clean energy backlog: $10B   (H2 + clean fuels + CO2 capture)
    Starting revenue 2026:     $2.5–3B  of backlog projects entering ramp phase

  CARBON CAPTURE (CCS)
  Blue hydrogen projects pair H2 production with carbon capture, allowing
  "clean" H2 from natural gas with <5% net CO2 emissions. EU taxonomy aligned.
  Linde has multiple blue H2 projects under construction in the US (IRA incentives).

  AI SEMICONDUCTOR DEMAND ACCELERATION
  Every new AI GPU fab requires massive N2 volumes. TSMC's Arizona fabs, Intel's
  Ohio fab, Samsung's Texas expansion = Linde supply contracts for 15–20 years.
  Each leading-edge fab consumes 1,000–2,000 tons/day of nitrogen — revenue of
  ~$50–100M/yr per fab for Linde. A structural growth layer ON TOP of clean energy.

Q1 2026 — ANOTHER BEAT AND RAISE QUARTER
──────────────────────────────────────────
  Adj EPS:       $4.33  (+10% YoY; beat consensus $4.27 by 1.41%)
  Revenue:       $8.78B (+8% YoY; beat consensus $8.51B by 3.17%)
  Op margin:     30.0%  (expanding YoY; pricing + efficiency)
  Net income:    $1,857M (+11% YoY)
  Diluted EPS:   $3.98  (+13% YoY; helped by buybacks reducing share count)

  FY2026 guidance raised/narrowed: $17.40–$17.90 adj EPS (7–9% growth)
  Q2 2026 guidance: $4.40–$4.50 adj EPS (8–10% growth)
  Erste Group raised FY2026E to $17.90 and FY2027E to $19.45 post-Q1 beat.

FY2025 FULL-YEAR RECAP (reported Feb 5, 2026)
──────────────────────────────────────────────
  Adj EPS:       $16.46  (+6% YoY; Q4 $4.20 = +6% YoY)
  Full-year sales: $35.1B (+6% YoY)
  Q4 results beat guidance of $4.10–$4.20 (came in at top end)
  16th consecutive year of dividend increase
  Shareholder returns: ~$6–7B (buybacks + dividends) in FY2025

THE VALUATION PROBLEM: PRICED FOR PERFECTION
──────────────────────────────────────────────
Linde is one of the best businesses in the industrial sector. The challenge is:

At $516:
  Trailing P/E (FY2025 $16.46):    31.4×   (premium to market; justified?)
  Forward P/E (FY2026E $17.75):    29.1×   (historically 27–34× for LIN)
  Forward P/E (FY2027E $19.30):    26.7×   (reasonable-looking but BULL scenario)
  Dividend yield:                    1.24%  ($6.40 / $516; low yield for an "industrial")
  Earnings yield:                    3.4%   (vs. 4.5–5% risk-free rate → negative carry)
  Analyst avg PT:                  $541–553 (+5–7% upside — barely covers one year of inflation)

The market is pricing in the BULL case:
  METHOD B upside:  $579 = just +12% from $516 — barely worth 2 years of capital at risk
  BASE upside:      $480 = -7% from $516 — the BASE case is a LOSS from current price!
  52-wk low:        $387.78 (April 2026 tariff panic) was a GENUINE BUY at ratio_b 0.53×

This is the textbook definition of a great company that is not a great investment at
the current price. Warren Buffett famously said: "A great company at a fair price is
better than a fair company at a great price." But even a great company bought at an
unfair price will underperform. At $516 = 29× forward earnings, LIN already reflects:
  — Full clean energy ramp over 2–3 years
  — Continued 8–10%/yr EPS growth through FY2027E
  — Multiple premium maintained above historical average
If ANY of these assumptions disappoint (ramp delays, FX headwinds, macro softness,
rates stay high), the stock re-rates DOWN toward BASE ($480) or worse.
""")

    print(DASH)
    print("EPS HISTORY  (Adjusted EPS, non-GAAP)")
    print(DASH)
    for yr, eps in EPS_HISTORY.items():
        print(f"  {yr}  ${eps:.2f}")
    print(f"  FY2026E ${EPS_NOW:.2f}  (mgmt guide $17.40–$17.90; Q1 2026 = $4.33 × 4 = $17.32)")
    cagr = (EPS_HISTORY["FY2025"] / EPS_HISTORY["FY2022"]) ** (1/3) - 1
    print(f"  FY2022–FY2025 CAGR: {cagr*100:.1f}%/yr  (pricing + efficiency + modest volume growth)")

    print(f"""
EPP CALCULATION
  EPS_TROUGH × EPP_MIN_PE  =  ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×  =  ${EPP:.2f}
  (Take-or-pay floors protect even in severe recession; medical/semiconductor demand stays)
  AMPLE BUFFER: current ${CURRENT_PRICE:.2f} is +{epp_gap_pct:.1f}% above EPP
  (But that buffer is entirely consumed by the valuation premium — not a margin of safety)

METHOD B  (2-year forward)
  CONS_EPS_2YR × CONS_EXIT_PE  =  ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×  =  ${price_b:.2f}

RATIO B  (PRIMARY SIGNAL)
  (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})
  = ${CURRENT_PRICE - EPP:.2f} / ${price_b - CURRENT_PRICE:.2f}
  = {ratio_b:.3f}×   →   {signal}
  EPP gap: +{epp_gap_pct:.1f}% above structural floor  (ample gap, but no upside to price_b)

SCENARIO PRICES
  BEAR     ${scenarios['BEAR']:>7.2f}   EPP; recession + FX collapse; EPS to $13; multiple 22×
  BASE     ${scenarios['BASE']:>7.2f}   FY2027E $18.50 × 26×; consensus earnings; slight de-rating
  BULL     ${scenarios['BULL']:>7.2f}   Method B; FY2027E $19.30 × 30×; clean energy ramp + premium
  XBULL    ${scenarios['XBULL']:>7.2f}   H2 economy + AI fab boom; ~$21.9 × 32×; full secular re-rate
""")

    print("SOFTMAX COMPOSITE ENGINE")
    print(f"  Market composite (inferred)  =  {market_composite:.3f}")
    print(f"  (Market pricing between BASE and BULL — already baking in clean energy + AI tailwinds)")

    print(f"""
SCA — SIGNAL CATALYST ADJUSTMENTS""")
    for desc, score, wt in sca_items:
        sign = "+" if score >= 0 else ""
        print(f"  {desc[:55]:<55}  {sign}{score:.2f} × {wt:.2f}  =  {score*wt:+.4f}")

    print(f"""
  sca_raw     =  {sca_raw:.4f}
  sca_adj     =  {sca_adj:.4f}  (= sca_raw / 2.0)
  adj_composite  =  {market_composite:.3f}  +  {sca_adj:.4f}  =  {adj_composite:.3f}
  (Net negative SCA: price already reflects all near-term positives; multiple compression risk)
""")

    print("SOFTMAX SCENARIO WEIGHTS  (at adj_composite = {:.3f})".format(adj_composite))
    for k, w in adj_weights.items():
        print(f"  {k:<10} {w*100:>5.1f}%   ${scenarios[k]:.2f}")

    ep_price = sum(adj_weights[k] * scenarios[k] for k in scenarios)
    print(f"\n  Expected price (probability-weighted)  =  ${ep_price:.2f}")

    print(f"""
BUSINESS METRICS
  FY2025 revenue                  = ~$35.1B  (+6% YoY)
  Q1 2026 revenue                 = $8.78B  (+8% YoY; beat by 3%)
  Operating margin Q1 2026        = 30.0%  (best-in-class industrials; expanding)
  Clean energy project backlog    = $10B total  ($2.5–3B starting revenue 2026)
  Sale-of-Gas (SOG) backlog       = $7.1B  (long-term locked-in projects)
  Linde Engineering backlog       = €4.5B  (as of Q1 2026; raised post-Q1)
  Dividend growth streak          = 16 consecutive annual increases
  Share buyback pace              = ~$3–4B/yr (reducing share count ~2%/yr)
  Net debt / EBITDA               = ~1.2×  (AA–/A1 rated; conservative leverage)
  Peer P/E comparison             = APD ~24–26×; Air Liquide ~26–28×; LIN 34× trailing
  All-time high                   = $521.28  (May 1, 2026; current $516 = near ATH)
  52-wk low                       = $387.78  (April 2026 tariff panic = BUY at 0.53×)

SIGNAL ENTRY GUIDE""")

    # Calculate threshold prices
    thresholds = {}
    for label, rb in [("AVOID", 2.50), ("HOLD", 1.75), ("WATCH", 1.10), ("ACCUM", 0.75)]:
        thresholds[label] = (rb * price_b + EPP) / (1 + rb)

    print(f"  ✕ AVOID      above  ${thresholds['AVOID']:>3.0f}  (ratio_b > 2.50×)  ← current ${CURRENT_PRICE:.2f}  {signal}")
    print(f"  ▷ HOLD/TRIM  ${thresholds['HOLD']:>3.0f} – ${thresholds['AVOID']:>3.0f}  (ratio_b 1.75–2.50×)")
    print(f"  ◐ WATCHLIST  ${thresholds['WATCH']:>3.0f} – ${thresholds['HOLD']:>3.0f}  (ratio_b 1.10–1.75×)")
    print(f"  ◎ ACCUMULATE ${thresholds['ACCUM']:>3.0f} – ${thresholds['WATCH']:>3.0f}  (ratio_b 0.75–1.10×)")
    print(f"  ◉ BUY        below  ${thresholds['ACCUM']:>3.0f}  (ratio_b < 0.75×)")

    lo52 = 387.78
    rb52lo = (lo52 - EPP) / (price_b - lo52)
    hi52 = 521.28
    rb52hi = (hi52 - EPP) / (price_b - hi52)
    print(f"""
  52-wk low $387.78 (Apr 2026 tariff panic) = BUY at ratio_b {rb52lo:.2f}×; pulled far below ACCUM.
  52-wk high $521.28 = extreme AVOID at ratio_b {rb52hi:.2f}×; current $516 ≈ that zone.
  Analyst avg PT $541–553: implies only +5–7% return from current — barely above inflation.
  BASE scenario ${scenarios['BASE']} BELOW current ${CURRENT_PRICE:.0f}: market already priced above consensus.
  The great entry points: below $412 (BUY), or $412–440 (ACCUM) on recession/macro scare.
  LINDE IS A GREAT BUSINESS. AT $516, IT IS NOT A GREAT INVESTMENT.
  The 52-wk low ($387.78) was the right time to act — similar opportunities will recur.""")
