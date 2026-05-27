"""
BLACKSTONE INC. (BX) — Bottom-Up Risk/Reward Signal Model
==========================================================
Part 1: Framework & Methodology
Part 2: Analyst Commentary & Investment Thesis
Part 3: Numbers & Signal Output
"""

# ── PART 1: FRAMEWORK ────────────────────────────────────────────────────────

FRAMEWORK = """
SIGNAL FRAMEWORK — METHOD B + SCA ENGINE
─────────────────────────────────────────
EPP  = EPS_TROUGH × EPP_MIN_PE          (structural floor; DE-based, not GAAP)
Ratio B = (Price − EPP) / (price_b − Price)

BX-specific EPS convention: Distributable Earnings (DE) per participating common
share. NOT GAAP EPS. GAAP includes unrealised mark-to-market gains/losses on
investments, which is very noisy and not relevant for valuation. DE = FRE + net
realisations (actual carried interest received + investment income paid out).
This is what actually gets paid to shareholders as dividends.

SIGNAL THRESHOLDS
  Ratio B < 0.75   →  ◉ BUY
  0.75 – 1.10      →  ◎ ACCUMULATE
  1.10 – 1.75      →  ◐ WATCHLIST
  1.75 – 2.50      →  ▷ HOLD/TRIM
  > 2.50           →  ✕ AVOID

EPP_MIN_PE = 18×  rationale:
  Blackstone manages 10-year locked-up capital funds (PE, RE, Credit, Infra).
  Management fees on $937B fee-earning AUM are contractually locked; they cannot
  "redeem" the way mutual fund investors can. Even in a severe recession, FRE
  would decline only modestly (AUM drawdowns are marked down, but fees accrue on
  committed capital during investment periods). Floor multiple of 18× is premium
  to BLK (17×) and commercial banks (9×) but appropriate for locked-up capital
  moat. 18× × $3.50 trough DE = $63 EPP.
"""

# ── PART 2: ANALYST COMMENTARY ───────────────────────────────────────────────

COMMENTARY = """
BLACKSTONE INC. (BX) — THE WORLD'S LARGEST ALTERNATIVE ASSET MANAGER
═══════════════════════════════════════════════════════════════════════

BUSINESS OVERVIEW
─────────────────
Blackstone ($1.30T AUM as of Q1 2026) is the dominant global alternative asset
manager across four platforms:

  Real Estate       ~$340B AUM — largest private RE investor globally; BREIT
                    (non-traded REIT) + opportunistic funds; logistics, data
                    centres, rentals, hospitality
  Private Equity    ~$340B AUM — flagship corporate PE; BAAM (hedge fund
                    solutions); life sciences; Asia
  Credit & Insurance ~$430B AUM — BXC direct lending, CLOs, BXCI insurance
                    platform (AIG, Allstate partnerships); fastest-growing unit
  Multi-Asset/Infra ~$190B AUM — infrastructure, secondaries, GP solutions

Fee-Earning AUM: $937.6B (72% of total; only fee-earning AUM generates management
fees; the balance is in investment/commitment period where fees commence later).

WHY BX IS DIFFERENT FROM A TRADITIONAL ASSET MANAGER
──────────────────────────────────────────────────────
1. LOCKED CAPITAL: PE/RE/Infra funds have 10-year lock-up periods. Unlike mutual
   funds, investors CANNOT redeem even in a crisis. Management fees are contractual
   and protected from market volatility.

2. PERFORMANCE FEE (CARRY) STRUCTURE: BX earns 20% carried interest on gains above
   8% hurdle rate. This creates enormous upside in bull market years (FY2022 $8.14
   DE/sh = record carry) but near-zero realisations when exit markets freeze (FY2023
   $3.95 trough). The KEY insight: Fee-Related Earnings (FRE) is the stable,
   recurring base (~$4.90 LTM); realisations layer on top.

3. AI INFRASTRUCTURE MEGA-CYCLE: BX is the single largest beneficiary of the AI
   capex boom among financial companies. Its data centre portfolio (hyperscale
   facilities, power infrastructure) is being valued at multiples of acquisition
   cost. AI-driven demand is creating $200B+ of new fund deployment opportunities.
   Q1 2026 data centre FRE contribution growing >40% YoY.

4. FRE DOMINANCE GROWING: FRE LTM Q1 2026 = $4.90/sh (+11% YoY), representing
   ~72% of total DE. As AUM grows (target $2T+ by 2030), FRE becomes increasingly
   dominant, reducing volatility and warranting higher multiples.

Q1 2026 RESULTS — RECORD AUM, STRONG GROWTH
─────────────────────────────────────────────
  Total AUM             $1.30T    +12% YoY; all-time record
  Fee-Earning AUM       $937.6B   +9% YoY
  Distributable Earnings $1.36/sh  +25% YoY
  Fee-Related Earnings   $1.26/sh  +22% YoY
  Inflows               $69B      (vs $72B Q4 2025)
  FRE Margin            (record; >100bps expansion FY2025)
  Dividend declared     $1.16/sh  (ex-div May 4, 2026)

FY2025 was "the best results in our 40-year history" (Schwarzman):
  Full year DE: $5.57/sh (+20% YoY from $4.64 in FY2024)
  Full year FRE: $4.40/sh LTM (structural; rate-independent)
  AUM: $1.27T (year-end); inflows $240B for full year

EARNINGS QUALITY: FRE vs DE
─────────────────────────────
  FRE per share (LTM Q1 2026): $4.90  (recurring; grows with AUM)
  DE per share (FY2025):       $5.57  (FRE + actual realisations)
  DE per share (FY2026E):      $6.58  (consensus; implies realisations recovery)

  The FY2023 trough ($3.95 DE) was almost entirely a REALISATIONS problem, not
  an FRE problem. FRE in FY2023 was ~$3.30-3.50/sh. The core business never
  stopped growing — markets just froze PE/RE exits. As rates normalise and
  M&A/IPO markets reopen, realisations recover and DE follows.

VALUATION SNAPSHOT
───────────────────
  At $118.51:
  FW P/E on FY2026E DE $6.58:  18.0×  (historically cheap; 5-yr avg 27-30×)
  FW P/E on FRE LTM $4.90:     24.2×  (fair for FRE alone; BLK trades 27× FRE)
  P/FRE premium to BLK:        DISCOUNT (BX at 24×, BLK at 27× FRE = BX cheaper)

  Analyst avg PT: $156–157 (+33% from current)
  Analyst consensus: "Buy" (17/26 analysts)

  At 52-wk high $190: was trading at 34× FY2025E DE = AVOID (overpriced)
  At 52-wk low $101.73: was trading at 15.5× FY2026E = BUY (deep value)

THE VALUATION PARADOX: AUM AT RECORD, STOCK AT -38% FROM ATH
──────────────────────────────────────────────────────────────
The disconnect: AUM hit $1.30T record (up 12% YoY) while the stock sits 38%
below the $190 ATH. Why?

  1. Higher-for-longer rates: PE/RE exits still below FY2021-22 levels; DE
     recovery below expectations (FY2026E $6.58 vs $8.14 FY2022 peak).
  2. BREIT overhang: BX's $70B non-traded REIT hit redemption gates in
     2022-2023 (retail investors sought liquidity). Recovery progressing but
     institutional confidence rebuilding.
  3. Multiple compression: from 30-35× DE at ATH to 18× today. Classic
     "growing business, compressing multiple" scenario.

THE BULL CASE: AUM $2T BY 2029 + RATE CUT TAILWIND
─────────────────────────────────────────────────────
BX's own target: $2T AUM by end of decade. At 18% FRE margins on $2T:
  $2T × 0.90% mgmt fee × 18% margin = ~$3.24B FRE annually at maturity
  Plus normalised carry at ~50% of FRE = total DE ~$11-12B
  At 1.27B participating shares: $9.50-10.00 DE/sh × 25× = $238-250/sh

That's the XBULL scenario. More near-term:
  FY2027E DE $7.80 × 22× = $172 (+45% from $118.51)
  Analyst consensus: $157 (+33%)

KEY RISKS
──────────
  1. Rates: if rates stay elevated, PE/RE exit values remain depressed;
     realisations stay low; DE falls short of $6.58E
  2. Commercial RE headwinds: office vacancy + rate-driven cap rate expansion
     could mark down RE funds; performance fees delayed
  3. BREIT / retail investor confidence: another redemption wave would cap
     retail AUM growth; BX retail strategy is a key growth pillar
  4. Regulatory: SEC scrutiny of private markets fee transparency; potential
     limits on retail access to alts (ERISA/40 Act changes)
  5. Concentration: 20% of fee-earning AUM in real estate in a CRE downturn

SIGNAL COMPARISON TO PEERS
────────────────────────────
  BLK at $1,073: ▷ HOLD/TRIM (ratio_b 2.05×) — fairly valued at BASE
  BX at $118.51: ◎ ACCUMULATE (ratio_b 1.04×) — 38% drawdown = entry zone
  BX is the better risk/reward in the asset manager space right now.

SUMMARY VERDICT
───────────────
BX is the world's dominant alt asset manager with $1.3T locked-up capital
generating contractual management fees — the AUM machine keeps running
regardless of market volatility. At 38% below ATH while AUM is at a record,
the market is pricing in a prolonged PE/RE exit freeze that appears excessive
given normalising rate expectations. FRE alone ($4.90 LTM) justifies current
price. Any realisations recovery drives significant upside. ACCUMULATE.
"""

# ── PART 3: NUMBERS & SIGNAL ─────────────────────────────────────────────────

import math

# ── Live price (MANDATORY — fetched from internet) ──
CURRENT_PRICE = 118.51   # BX — Google Finance / search results, 2026-05-27 (last close May 22)

PRICE_52W_LOW  = 101.73
PRICE_52W_HIGH = 190.08

SHARES_M    = 1188.0   # Class A common shares (millions)
DIVIDEND_ANN = 4.64    # Trailing 4-quarter variable dividend est.; Q1 2026 declared $1.16/sh

# ── Distributable Earnings per participating share (NOT GAAP) ──
EPS_HISTORY = {
    "FY2022": 8.14,   # Record — peak PE/RE/structured credit realisations boom
    "FY2023": 3.95,   # TROUGH — rate shock froze exit markets; FRE was ~$3.40
    "FY2024": 4.64,   # Recovery start (FY2025 $5.57 was +20% from this)
    "FY2025": 5.57,   # Record FRE + partial realisations recovery; "best 40-yr history"
}

EPS_NOW    = 6.58   # FY2026E consensus DE per participating share (range: $5.82–$7.13)
EPS_TROUGH = 3.50   # Conservative floor; below FY2023 actual $3.95

EPP_MIN_PE = 18     # Alternative asset manager; locked-capital moat; contractual fee stream
EPP        = EPP_MIN_PE * EPS_TROUGH   # = 63.00

# ── Method B: 2-year forward (FY2027E) ──
CONS_EPS_2YR  = 7.80    # FY2027E DE est. (FY2026E $6.58 × ~18% AUM growth + realisations)
CONS_EXIT_PE  = 22      # Normalised multiple; BX has historically traded 20-30× DE
price_b       = CONS_EPS_2YR * CONS_EXIT_PE   # = 171.60

ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)

# ── AUM & Operating Metrics ──
AUM_TOTAL_T          = 1.30    # Total AUM ($T, Q1 2026)
FEE_EARNING_AUM_B    = 937.6   # Fee-earning AUM ($B)
FRE_PER_SHARE_LTM    = 4.90    # FRE LTM through Q1 2026 (+11% YoY)
FRE_PER_SHARE_Q1     = 1.26    # Q1 2026 FRE per participating share (+22% YoY)
DE_PER_SHARE_Q1      = 1.36    # Q1 2026 DE (+25% YoY)
INFLOWS_Q1_B         = 69.0    # Q1 2026 inflows ($B)
INFLOWS_FY2025_B     = 240.0   # FY2025 full-year inflows ($B)

# ── Softmax composite engine ──
def softmax_weights(composite, T=0.60):
    centres = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
    logits  = {k: -((composite - v) ** 2) / T for k, v in centres.items()}
    m       = max(logits.values())
    exps    = {k: math.exp(v - m) for k, v in logits.items()}
    s       = sum(exps.values())
    return   {k: v / s for k, v in exps.items()}

scenarios = {
    "BEAR":  63.00,    # EPP floor; severe recession; realisations → $0; FRE haircut
    "BASE":  145.00,   # FY2026E $6.58 × 22×; normalised rate environment
    "BULL":  172.00,   # Method B; FY2027E $7.80 × 22×; realisations recovering
    "XBULL": 215.00,   # Full cycle; $8.60 × 25×; AUM $1.7T, rate cuts, AI mega-exits
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
sca_factors = [
    # (description,                                                    raw,   weight)
    ("AI infrastructure mega-cycle — BX largest alt RE investor;     ", +0.40, 0.25),
    (" data centres + power infra portfolio growing >40% YoY in FRE  ", +0.00, 0.00),
    ("FRE growing 22% YoY Q1 2026; now 74% of DE (stable, recurring)", +0.25, 0.20),
    ("38% below 52-wk high $190 while AUM at record $1.30T — mis-    ", +0.30, 0.20),
    (" match between operating performance and stock price            ", +0.00, 0.00),
    ("Rates higher-for-longer: PE/RE exit market below 2021-22 pace; ", -0.25, 0.25),
    (" realisations + carry income soft                               ", +0.00, 0.00),
    ("BREIT overhang: office/CRE marks + prior gate-triggers weigh   ", -0.20, 0.20),
    ("Macro/geopolitical: M&A + IPO market dependent on stability;   ", -0.15, 0.15),
    (" tariff uncertainty dampens exit valuations                     ", +0.00, 0.00),
]

# Cleaner SCA factors (non-zero entries only):
sca_factors_clean = [
    ("AI infrastructure mega-cycle; data centres + power infra portfolio growing >40% YoY", +0.40, 0.25),
    ("FRE growing 22% YoY Q1 2026; now ~74% of DE (stable, rate-independent base)",         +0.25, 0.20),
    ("38% below 52-wk high $190 while AUM is at record $1.30T — operational/price mismatch",+0.30, 0.20),
    ("Higher-for-longer rates: PE/RE exit market below 2021-22 pace; realisations soft",     -0.25, 0.25),
    ("BREIT overhang: CRE marks + past redemption gate triggers weigh on retail confidence", -0.20, 0.20),
    ("Macro/geopolitical: M&A + IPO markets depend on stability; tariffs dampen exits",      -0.15, 0.15),
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
    print("BLACKSTONE INC. (BX) — SIGNAL MODEL")
    print("=" * 70)

    print(FRAMEWORK)
    print(COMMENTARY)

    print("KEY METRICS")
    print(f"  Current price (fetched)      = ${CURRENT_PRICE:>8.2f}")
    print(f"  52-week range                = ${PRICE_52W_LOW:.2f} – ${PRICE_52W_HIGH:.2f}")
    print(f"  Market cap                   = ${CURRENT_PRICE * SHARES_M / 1000:.1f}B")
    print(f"  FW P/E on FY2026E DE $6.58   = {CURRENT_PRICE/EPS_NOW:.1f}× (vs 5-yr avg 27-30×)")
    print(f"  FW P/FRE on LTM $4.90        = {CURRENT_PRICE/FRE_PER_SHARE_LTM:.1f}×")
    print(f"  Dividend (trailing est.)     = ${DIVIDEND_ANN:.2f}  (yield {DIVIDEND_ANN/CURRENT_PRICE*100:.1f}%)")
    print(f"  Total AUM                    = ${AUM_TOTAL_T:.2f}T  (record Q1 2026)")
    print(f"  Fee-Earning AUM              = ${FEE_EARNING_AUM_B:.0f}B")
    print(f"  FRE per share LTM            = ${FRE_PER_SHARE_LTM:.2f}  (+11% YoY)")
    print(f"  DE per share Q1 2026         = ${DE_PER_SHARE_Q1:.2f}  (+25% YoY)")

    print("\nDE PER PARTICIPATING SHARE HISTORY  (NOT GAAP)")
    for yr, eps in EPS_HISTORY.items():
        note = ""
        if yr == "FY2022": note = "  ← record (peak carry)"
        if yr == "FY2023": note = "  ← TROUGH (exit market freeze)"
        if yr == "FY2025": note = "  ← record FRE-driven"
        print(f"  {yr}  ${eps:>5.2f}{note}")
    print(f"  FY2026E ${EPS_NOW:.2f}   (consensus; range $5.82–$7.13)")

    print(f"\nEPP CALCULATION")
    print(f"  EPS_TROUGH × EPP_MIN_PE  =  ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×  =  ${EPP:.2f}")

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
        if k == "BEAR":  print("EPP floor; severe recession; carry → $0; FRE -20%")
        if k == "BASE":  print("FY2026E $6.58 × 22×; normalised exit market")
        if k == "BULL":  print("Method B; FY2027E $7.80 × 22×; realisations recovering")
        if k == "XBULL": print("Full cycle; $8.60 × 25×; AUM $1.7T, AI mega-exits")

    print(f"\nSOFTMAX COMPOSITE ENGINE")
    print(f"  Market composite (inferred)  =  {market_composite:.3f}")
    print(f"  (Market pricing BX in lower-BASE zone — reflecting realisations headwinds)")

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

    print(f"\nALT ASSET MANAGER METRICS")
    print(f"  Total AUM (Q1 2026)          = ${AUM_TOTAL_T:.2f}T  (record; +12% YoY)")
    print(f"  Fee-Earning AUM              = ${FEE_EARNING_AUM_B:.1f}B  (72% of total)")
    print(f"  Q1 2026 inflows              = ${INFLOWS_Q1_B:.0f}B  (FY2025: $240B)")
    print(f"  FRE per share LTM            = ${FRE_PER_SHARE_LTM:.2f}  (+11% YoY)")
    print(f"  FRE per share Q1 2026        = ${FRE_PER_SHARE_Q1:.2f}  (+22% YoY)")
    print(f"  DE per share Q1 2026         = ${DE_PER_SHARE_Q1:.2f}  (+25% YoY)")
    print(f"  FY2026E DE consensus         = ${EPS_NOW:.2f}  (range $5.82–$7.13)")
    print(f"  Analyst avg PT               = $156–157  (+33% from current); 'Buy' consensus")
    print(f"  Dividend (Q1 2026 declared)  = $1.16/sh  (variable; yield ~{1.16*4/CURRENT_PRICE*100:.1f}% ann.)")

    print(f"\nSIGNAL ENTRY GUIDE")
    # BUY:        ratio_b = 0.75  → (p-63)/(172-p) = 0.75 → p = (63 + 0.75×172)/1.75 = 110.0
    # ACCUMULATE: ratio_b = 1.10  → p = (63 + 1.10×172)/2.10 = 120.1
    # WATCHLIST:  ratio_b = 1.75  → p = (63 + 1.75×172)/2.75 = 132.4
    # HOLD/TRIM:  ratio_b = 2.50  → p = (63 + 2.50×172)/3.50 = 140.9
    print(f"  ✕ AVOID      above  $141  (ratio_b > 2.50×; 52-wk high $190 was deep AVOID at 34×)")
    print(f"  ▷ HOLD/TRIM  $132 – $141  (ratio_b 1.75–2.50×)")
    print(f"  ◐ WATCHLIST  $120 – $132  (ratio_b 1.10–1.75×)")
    print(f"  ◎ ACCUMULATE $110 – $120  (current ${CURRENT_PRICE:.2f}; ratio_b 0.75–1.10×)  ← HERE")
    print(f"  ◉ BUY        below  $110  (ratio_b < 0.75×; near 52-wk low $101.73)")
    print()
    print(f"  52-wk low $101.73 = deep BUY (ratio_b 0.73×); 52-wk high $190 = AVOID (ratio_b 3.53×).")
    print(f"  38% drawdown from ATH while AUM at record = classic accumulation zone.")
    print(f"  Optimal add: $110–118 range; scale in to BUY threshold $110 on rate-driven pullbacks.")
    print(f"  Watch: Q2 2026 realisations; Fed rate path; BREIT flows; AI data centre pipeline.")
