"""
apd_signal_model.py — Air Products and Chemicals, Inc. (NYSE: APD)
Industrial gas oligopolist. Hydrogen economy leader. NEOM + Louisiana mega-projects.
Signal framework: EPP floor + Method B + SCA softmax engine.
"""

import math

# ── LIVE PRICE (fetched before model construction) ──────────────────────────
CURRENT_PRICE = 290.00    # APD — fetched from Yahoo Finance / CNBC, 2026-05-27
# ($289.60 as of May 26, 2026; 52-wk low $229.11, 52-wk high $307.96)
# Market cap ~$64.6B; shares ~223M; dividend yield ~2.5%

TICKER        = "APD"
COMPANY       = "Air Products and Chemicals, Inc."
SHARES_M      = 223          # million diluted shares (~222.7M as of Q2 FY2026)
DIVIDEND_ANN  = 7.24         # USD/yr; $1.81/quarter (raised Q4 FY2025)
                              # 44th consecutive annual dividend increase — Dividend King

# ── EPS CONVENTION / FISCAL YEAR NOTE ────────────────────────────────────────
# Adjusted (non-GAAP) EPS. Excludes: business exit / impairment charges (massive in FY2025:
# ~$3.7B pre-tax / $13.68/share GAAP hit from exiting US projects), restructuring costs,
# certain equity affiliate income adjustments, and tax-related items.
# IMPORTANT: APD's fiscal year ends September 30 (not December 31 like most peers).
#   FY2025 = Oct 2024 – Sep 2025; FY2026 = Oct 2025 – Sep 2026 (currently in Q3 FY2026)
# GAAP FY2025 showed a loss (-$1.74/sh) due to $3.7B in strategic charges — use adj EPS only.

EPS_HISTORY = {
    "FY2022": 10.32,   # (approx; guidance $10.20–$10.40); recovering post-COVID volumes
    "FY2023": 11.42,   # (approx; guidance $11.20–$11.50); +10% YoY; pricing + efficiency
    "FY2024": 12.43,   # actual; +9% YoY; Ghasemi era final full year
    "FY2025": 12.03,   # actual (Nov 6, 2025); -3% YoY; STRATEGIC RESET YEAR —
                        #   new CEO Menezes (Feb 2025) exited 3 US H2 projects;
                        #   $3.7B GAAP charges; core business resilient
}

# Q1 FY2026 (Jan 30, 2026): Adj EPS $3.16 (+10% YoY, beat $3.04); revenue $3.1B (+1%)
# Q2 FY2026 (Apr 30, 2026): Adj EPS $3.20 (+19% YoY); revenue $3.17B (beat +3.3%)
# Guidance raised to $13.00–$13.25 adj EPS for FY2026 (7–9% growth from $12.03)

EPS_NOW       = 13.13    # NTM; midpoint of raised FY2026 guidance $13.00–$13.25
                          # H1 FY2026 ($3.16+$3.20=$6.36) on track; H2 seasonally stronger
EPS_TROUGH    = 10.50    # severe scenario: core industrial gas recession + H2 projects disappoint;
                          # below FY2022 actual ($10.32); reflects volume declines + FX + no NEOM
                          # APD's core gas business never collapses: take-or-pay contracts floor
EPP_MIN_PE    = 20        # industrial gas oligopolist (same structural moat as LIN: take-or-pay,
                          # on-site ASUs, zero churn, oligopoly pricing) — see rationale below.
                          # Slightly below LIN (22×) due to higher execution risk from mega-projects
EPP           = EPP_MIN_PE * EPS_TROUGH   # = $210.00

# NOTE: Horizon is FY2027 (Oct 2026–Sep 2027) — NEOM inflection year. Technically ~16 months
# from analysis date but chosen deliberately: NEOM starts commercial production in 2027, which
# is the first earnings step-up from the decade-long H2 investment cycle.
CONS_EPS_2YR  = 14.80    # FY2027E analyst consensus; NEOM contributing ~$0.50–$1.50/share;
                          # core gas growing 5–7%/yr; Louisiana still under construction
CONS_EXIT_PE  = 25        # bull case: H2 optionality + NEOM de-risked drives multiple expansion
                          # from current 22× FW → 25×; still below LIN's 29×; reflects execution risk
price_b       = CONS_EPS_2YR * CONS_EXIT_PE   # = $370.00

ratio_b       = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
epp_gap_pct   = (CURRENT_PRICE - EPP) / EPP * 100

# Scenario prices
scenarios = {
    "BEAR":  210,    # EPP; core gas recession; H2 projects delayed/cancelled; $10.50 × 20×
    "BASE":  305,    # FY2027E $13.80 × 22×; core growth only; NEOM modest; no re-rating
    "BULL":  370,    # Method B; FY2027E $14.80 × 25×; NEOM on-time; distribution deal signed
    "XBULL": 480,    # Louisiana online early + NEOM at full rate; H2 economy materialises; $16 × 30×
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
    ("Core industrial gas oligopoly: same LIN-class moat (on-site ASUs; take-or-pay; "
     "zero churn; Linde/APD/Air Liquide = ~75% global market). 44yr div increases.",
     +0.30, 0.25),
    ("NEOM Green H2: 90% complete; 2.2GW electrolysis; commercial production 2027; "
     "world's largest green ammonia project. Yara distribution deal 'anticipated' H1 2026.",
     +0.30, 0.20),
    ("New CEO Eduardo Menezes (ex-Linde EVP EMEA): disciplined reset — exited 3 risky "
     "US projects; raised guidance twice; FY2026 on track. Right operator for right-sizing.",
     +0.20, 0.10),
    ("Significant valuation discount to LIN: APD at 22× FY2026E vs LIN at 29×. "
     "Same core moat, lower multiple → option value on H2 is essentially free.",
     +0.20, 0.10),
    ("NEOM demand risk: no final distribution agreement signed; green ammonia market "
     "nascent; green H2 uneconomic without subsidies at scale. 'Demand risk is real' "
     "(Energy Connects, May 2025). Project economics only proven at commercial startup.",
     -0.40, 0.25),
    ("Louisiana Blue H2: cost ballooned $4.5B → $8–9B; FID expected mid-2026 (not yet "
     "committed); online 2030. Yara partnership for ammonia offtake in advanced talks. "
     "High execution risk; significant capital still required.",
     -0.25, 0.20),
    ("Heavy capex ~$4B/yr constraining FCF; net debt elevated during construction phase. "
     "Interest burden grows before NEOM/Louisiana earnings arrive.",
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
    print("AIR PRODUCTS AND CHEMICALS, INC. (APD) — SIGNAL MODEL")
    print("Industrial gas oligopolist. 44yr dividend king. NEOM + Louisiana H2.")
    print(SEP)

    print("""
SIGNAL FRAMEWORK — METHOD B + SCA ENGINE
─────────────────────────────────────────
EPP  = EPS_TROUGH × EPP_MIN_PE          (structural floor; adjusted EPS basis)
Ratio B = (Price − EPP) / (price_b − Price)

APD EPS convention: Adjusted (non-GAAP) EPS. Excludes restructuring charges,
business exit impairments (FY2025 included ~$3.7B pre-tax / $13.68/share from
strategic project exits), and certain non-recurring items. GAAP FY2025 was a
loss per share of -$1.74 due to strategic charges — adjusted EPS ($12.03) is
the correct economic earnings lens.

FISCAL YEAR NOTE: APD's fiscal year ends September 30. Current quarter is Q3
FY2026 (April–June 2026). FY2026 ends September 30, 2026.

SIGNAL THRESHOLDS
  Ratio B < 0.75   →  ◉ BUY
  0.75 – 1.10      →  ◎ ACCUMULATE
  1.10 – 1.75      →  ◐ WATCHLIST
  1.75 – 2.50      →  ▷ HOLD/TRIM
  > 2.50           →  ✕ AVOID

EPP_MIN_PE = 20×  rationale:
  Air Products operates the same core industrial gas infrastructure as Linde:
  (1) ON-SITE ASUs: Air separation units built at customer facilities (steel mills,
      chip fabs, chemical plants, hospitals). Once installed, the customer physically
      CANNOT switch — dismantling costs $50M–$500M and takes years. Zero churn.
  (2) TAKE-OR-PAY CONTRACTS: 10–20 year contracts guarantee minimum revenue.
      Customers must pay even if they use zero volume. True floor on earnings.
  (3) OLIGOPOLY: Linde + Air Products + Air Liquide = ~75% global market. Pricing
      power maintained across cycles. No new entrant in 40+ years.
  20× (vs LIN 22×): 2-turn discount reflects higher execution risk from mega-projects
  (NEOM, Louisiana). Core gas business warrants ≥20× (same as LIN analysis basis)
  but the H2 bet creates more earnings volatility scenarios below EPP than LIN.
  During the 2009 GFC, Air Products (standalone pre-merger) traded no lower than
  16–18× forward. 20× = appropriate severe-stress floor for this business quality.
""")

    print("AIR PRODUCTS (APD) — THE H2 OPTION ON AN INDUSTRIAL GAS OLIGOPOLY")
    print("=" * 70)

    print("""
BUSINESS OVERVIEW
─────────────────
Air Products and Chemicals was founded in 1940 in Emmaus, Pennsylvania. It is
the world's #2 industrial gas company by revenue (~$12B/yr; behind Linde ~$35B
and roughly equal to Air Liquide). Headquarters: Allentown, Pennsylvania.
CEO: Eduardo F. Menezes (appointed February 7, 2025; former Linde EVP EMEA,
overseeing €8B+ operations across 40+ countries). Predecessor: Seifi Ghasemi,
who ran the company 2014–2025 and pivoted APD aggressively toward clean H2.
44 consecutive years of dividend increases — a Dividend King (Champion tier).
Dividend: $1.81/quarter = $7.24/yr; 2.5% yield at $290.

THE CORE BUSINESS: THREE GAS SEGMENTS
───────────────────────────────────────
  AMERICAS GAS        ~45% of segment operating profit
  ─────────────────────────────────────────────────────
  On-site industrial gas supply (ASUs, H2 generators) at customer sites across
  North and South America. Long-term take-or-pay contracts. Customers include
  steel producers, refineries, chemical plants, food processors, semiconductors.
  The structural backbone of APD — predictable, high-margin, recurring.

  EUROPE GAS          ~30% of segment operating profit
  ─────────────────────────────────────────────────────
  Same model across Europe. Key markets: Germany, Belgium, UK, Netherlands.
  Hydrogen supply to refineries (hydrotreating). Specialty gases for electronics.
  FX headwind as EUR/USD fluctuates (APD ~40% ex-USD revenue).

  ASIA GAS            ~25% of segment operating profit
  ─────────────────────────────────────────────────────
  China, India, South Korea. On-site supply to steel (China), semiconductor fabs
  (South Korea/Taiwan), chemical plants. Semiconductor-related specialty gases
  are the highest-growth, highest-margin sub-segment. TSMC/Samsung-adjacent.

THE STRATEGIC PIVOT: FROM GHASEMI TO MENEZES
─────────────────────────────────────────────
Under Seifi Ghasemi (2014–2025), APD pursued the world's most aggressive clean
hydrogen strategy. Key bets committed:

  NEOM Green Hydrogen (Saudi Arabia):    $8.5B  (world's largest green H2 project)
  Louisiana Blue Hydrogen (US):          $4.5B → $8–9B  (cost inflation)
  Alberta Oil Sands H2 (Canada):        ~$1.5B  (EXITED Feb 2025 under Menezes)
  Several US H2 projects:               ~$1.5B  (ALL EXITED Feb 2025 under Menezes)

Total committed H2 capex at peak: ~$15–20B — extraordinary for a ~$60B market
cap company. Market worried about execution risk, cost overruns, demand uncertainty.

Menezes's reset (Feb 2025 onwards):
  ✓ Exited 3 US-based projects (Feb 2025) — reduced risk, improved capital discipline
  ✓ FY2026 guidance raised twice (initial $12.85–$13.15 → current $13.00–$13.25)
  ✓ Pursuing Yara partnership for NEOM ammonia distribution (H1 2026 target)
  ✓ Louisiana FID expected mid-2026 (pending Yara offtake deal)
  ✓ Core margins expanding: Q1 FY2026 +140bps; Q2 FY2026 adj EPS +19% YoY

THE MEGA-PROJECTS: THE OPTION VALUE
─────────────────────────────────────
  NEOM GREEN HYDROGEN COMPLEX (Saudi Arabia)
  ──────────────────────────────────────────
  Structure: JV — ACWA Power (26.3%), NEOM Company (26.3%), Air Products (47.4%)
  Scale: 2.2GW electrolysis; 1.2 million metric tonnes/yr green ammonia
  Status: >90% complete; commercial production targeted 2027
  Cost: ~$8.5B total project cost (APD share ~$4B)
  APD's thesis: offtake the green ammonia; sell globally as clean fuel alternative
  Challenge: No final distribution agreement yet. APD + Yara "anticipating" deal.
             Green ammonia demand is nascent — market must be built.
  If successful: $0.50–$1.50 adj EPS annually when at full rate; option on H2 economy
  Risk: Green H2 is currently uneconomic without policy support. If green ammonia
        prices don't develop or demand stalls, economics are poor.

  LOUISIANA BLUE HYDROGEN CLEAN ENERGY COMPLEX
  ─────────────────────────────────────────────
  Location: Darrow, Louisiana
  Scale: >750M scf/day blue H2; ~95% CO2 capture; ammonia production
  Cost: $4.5B (announced 2021) → now $8–9B (inflation + scope; Yara to take ~25%)
  Status: FID expected mid-2026 (pending Yara deal); startup targeted 2030
  US IRA: $3/kg clean hydrogen production tax credit — critical economic enabler
  If successful: ~$1.50–$2.50 adj EPS at full rate (2030+)
  Risk: Yara deal not yet final; 2030 startup; IRA policy uncertainty; cost may grow

  COMBINED H2 OPTION VALUE (if both execute):
  NEOM (full rate 2028+):      +$1.00–$1.50 EPS
  Louisiana (full rate 2030+): +$1.50–$2.50 EPS
  Core FY2027 baseline:        ~$14.00 EPS
  Total by 2030:               $16.50–$18.00 EPS → at 25–28× = $410–$504 stock

FY2026 RESULTS SO FAR (two quarters)
──────────────────────────────────────
  Q1 FY2026 (Jan 30, 2026):
    Adj EPS:    $3.16  (+10% YoY; beat consensus $3.04 by 4%)
    Revenue:    $3.10B (+1% YoY); Op margin 24.4% (+140 bps)
    Key driver: Non-helium pricing actions + business mix improvement

  Q2 FY2026 (Apr 30, 2026):
    Adj EPS:    $3.20  (+19% YoY; exceeded top-end of guidance)
    Revenue:    $3.17B (+3.3% beat estimate)
    Key driver: Strong onsite volumes + productivity + favourable currency
    Guidance raised: FY2026 adj EPS to $13.00–$13.25 (was $12.85–$13.15)

FY2025 FULL-YEAR (reported Nov 6, 2025)
──────────────────────────────────────
  Adj EPS:      $12.03  (-3% from $12.43 in FY2024; strategic reset year)
  Q4 adj EPS:   $3.39   (modest beat; stock surged ~10% on strategic clarity)
  Revenue:      $12.0B  (-1% YoY)
  FY2026 initial guidance: $12.85–$13.15 (+7–9%)

THE DISCOUNT TO LIN: THE OPPORTUNITY FRAMING
──────────────────────────────────────────────
  Metric              APD ($290)        LIN ($516)
  ────────────────────────────────────────────────
  FW P/E (FY2026E)    22.1×             29.1×         APD 7-turn discount
  Div yield           2.5%              1.2%           APD pays you more to wait
  EPP buffer          +38%              +80%           LIN has more margin of safety
  Method B upside     +27.6%            +12.2%         APD 2× more upside to BULL
  H2 option value     LARGE (free)      smaller        APD has the bigger H2 bet

The 7-turn PE discount to LIN is entirely explained by NEOM/Louisiana uncertainty.
Same core industrial gas moat. At $290, you're paying roughly core-only value for
APD's industrial gas franchise — NEOM and Louisiana are FREE CALL OPTIONS.
""")

    print(DASH)
    print("EPS HISTORY  (Adjusted EPS, non-GAAP; fiscal year ends Sep 30)")
    print(DASH)
    for yr, eps in EPS_HISTORY.items():
        print(f"  {yr}  ${eps:.2f}")
    print(f"  FY2026E ${EPS_NOW:.2f}  (raised guidance $13.00–$13.25; H1 FY2026 = $6.36 on track)")
    cagr = (EPS_HISTORY["FY2024"] / EPS_HISTORY["FY2022"]) ** (1/2) - 1
    print(f"  FY2022–FY2024 CAGR: {cagr*100:.1f}%/yr  (FY2025 reset year excluded from trend)")

    print(f"""
EPP CALCULATION
  EPS_TROUGH × EPP_MIN_PE  =  ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×  =  ${EPP:.2f}
  (Core gas take-or-pay floor; below FY2022 actual $10.32; H2 projects = $0)
  EPP buffer: current ${CURRENT_PRICE:.2f} is +{epp_gap_pct:.1f}% above EPP — adequate margin of safety

METHOD B  (FY2027E horizon — NEOM inflection year)
  CONS_EPS_2YR × CONS_EXIT_PE  =  ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×  =  ${price_b:.2f}

RATIO B  (PRIMARY SIGNAL)
  (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})
  = ${CURRENT_PRICE - EPP:.2f} / ${price_b - CURRENT_PRICE:.2f}
  = {ratio_b:.3f}×   →   {signal}
  H2 option approximately FREE at current price: core gas alone ≈ $290 at 22× FY2027 EPS

SCENARIO PRICES
  BEAR     ${scenarios['BEAR']:>7.2f}   EPP; H2 projects fail; core recession; $10.50 × 20×
  BASE     ${scenarios['BASE']:>7.2f}   Core-only growth; NEOM modest start; $13.80 × 22×; no re-rate
  BULL     ${scenarios['BULL']:>7.2f}   Method B; FY2027E $14.80 × 25×; NEOM on-time + distribution
  XBULL    ${scenarios['XBULL']:>7.2f}   Louisiana + NEOM at full rate; H2 economy; $16 × 30×
""")

    print("SOFTMAX COMPOSITE ENGINE")
    print(f"  Market composite (inferred)  =  {market_composite:.3f}")
    print(f"  (Market pricing core recovery only — minimal H2 option value priced in)")

    print(f"""
SCA — SIGNAL CATALYST ADJUSTMENTS""")
    for desc, score, wt in sca_items:
        sign = "+" if score >= 0 else ""
        print(f"  {desc[:55]:<55}  {sign}{score:.2f} × {wt:.2f}  =  {score*wt:+.4f}")

    print(f"""
  sca_raw     =  {sca_raw:.4f}
  sca_adj     =  {sca_adj:.4f}  (= sca_raw / 2.0)
  adj_composite  =  {market_composite:.3f}  +  {sca_adj:.4f}  =  {adj_composite:.3f}
  (Near-neutral SCA: core quality + free H2 option vs. execution risk balance out)
""")

    print("SOFTMAX SCENARIO WEIGHTS  (at adj_composite = {:.3f})".format(adj_composite))
    for k, w in adj_weights.items():
        print(f"  {k:<10} {w*100:>5.1f}%   ${scenarios[k]:.2f}")

    ep_price = sum(adj_weights[k] * scenarios[k] for k in scenarios)
    print(f"\n  Expected price (probability-weighted)  =  ${ep_price:.2f}")

    print(f"""
BUSINESS METRICS
  FY2025 revenue                  = $12.0B  (-1% YoY; strategic reset year)
  Q2 FY2026 revenue               = $3.17B  (+3% YoY; beat estimates)
  Operating margin Q1 FY2026      = 24.4%  (+140 bps; expanding under Menezes)
  NEOM completion                 = >90%  (commercial production target 2027)
  Louisiana FID                   = expected mid-2026 (pending Yara deal)
  Capex FY2026 guidance           = ~$4.0B  (heavy construction spend)
  Dividend growth streak          = 44 consecutive annual increases (Dividend King)
  Dividend yield at $290          = 2.5%  (highest of industrial gas majors)
  Shares outstanding              = ~223M  (stable; minimal buybacks)
  Analyst consensus               = Moderate Buy; avg PT $301–$328 (+4–13%)
  52-wk low $229.11 (Apr 2026)    = deep BUY at ratio_b 0.14×
  52-wk high $307.96              = WATCHLIST at ratio_b 1.58×

SIGNAL ENTRY GUIDE""")

    thresholds = {}
    for label, rb in [("AVOID", 2.50), ("HOLD", 1.75), ("WATCH", 1.10), ("ACCUM", 0.75)]:
        thresholds[label] = (rb * price_b + EPP) / (1 + rb)

    print(f"  ✕ AVOID      above  ${thresholds['AVOID']:>3.0f}  (ratio_b > 2.50×)")
    print(f"  ▷ HOLD/TRIM  ${thresholds['HOLD']:>3.0f} – ${thresholds['AVOID']:>3.0f}  (ratio_b 1.75–2.50×)")
    print(f"  ◐ WATCHLIST  ${thresholds['WATCH']:>3.0f} – ${thresholds['HOLD']:>3.0f}  (ratio_b 1.10–1.75×)")
    print(f"  ◎ ACCUMULATE ${thresholds['ACCUM']:>3.0f} – ${thresholds['WATCH']:>3.0f}  (ratio_b 0.75–1.10×)  ← current ${CURRENT_PRICE:.0f}  {signal}")
    print(f"  ◉ BUY        below  ${thresholds['ACCUM']:>3.0f}  (ratio_b < 0.75×)")

    lo52 = 229.11
    rb52lo = (lo52 - EPP) / (price_b - lo52)
    hi52 = 307.96
    rb52hi = (hi52 - EPP) / (price_b - hi52)
    print(f"""
  52-wk low $229.11 (Apr 2026 tariff panic) = deep BUY at ratio_b {rb52lo:.2f}×.
  52-wk high $307.96 = WATCHLIST at ratio_b {rb52hi:.2f}×.
  Analyst avg PT $301–$328: within WATCHLIST/HOLD zone — analysts see limited upside.
  NEOM + Louisiana = FREE option at $290 (core gas alone ≈ $286–$295 at 22× core EPS).
  KEY CATALYSTS: NEOM Yara distribution deal (H1 2026); Louisiana FID (mid-2026).
  If both catalysts confirm → upgrade to BULL scenario; ACCUMULATE adds sharply.
  If NEOM demand disappoints → stock drifts toward BASE ($305); hold core position.""")
