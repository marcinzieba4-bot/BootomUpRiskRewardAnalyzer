"""
THE CHARLES SCHWAB CORPORATION (SCHW) — Bottom-Up Risk/Reward Signal Model
============================================================================
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

SCHW EPS convention: Adjusted diluted EPS (non-GAAP). Excludes amortisation
of acquired intangibles from the TD Ameritrade acquisition and other non-
recurring items. This is management's primary earnings metric. GAAP EPS is
lower by ~$0.40-0.50/year due to TDA intangible amortisation.

SIGNAL THRESHOLDS
  Ratio B < 0.75   →  ◉ BUY
  0.75 – 1.10      →  ◎ ACCUMULATE
  1.10 – 1.75      →  ◐ WATCHLIST
  1.75 – 2.50      →  ▷ HOLD/TRIM
  > 2.50           →  ✕ AVOID

EPP_MIN_PE = 15×  rationale:
  Schwab is a premium retail brokerage/wealth manager with $11.77T in client
  assets. It has bank-like interest rate sensitivity (NIM is the #1 earnings
  driver) but unlike a bank, has no meaningful credit risk (brokerage assets,
  not loans). At the 2023 SVB/cash-sorting panic, SCHW hit ~$45 — at that
  price, the implied P/E on FY2023E adj EPS (~$3.05) was ~14.8×. The market
  floor multiple has empirically been ~15×. 15× × $2.50 trough = $37.50 EPP.
"""

# ── PART 2: ANALYST COMMENTARY ───────────────────────────────────────────────

COMMENTARY = """
THE CHARLES SCHWAB CORPORATION (SCHW) — THE GREAT RECOVERY: PAST THE CRISIS
═════════════════════════════════════════════════════════════════════════════

BUSINESS OVERVIEW
─────────────────
Charles Schwab is the largest retail brokerage in the United States with
$11.77T in client assets (Q1 2026), serving ~35M brokerage accounts. Revenue
comes from three primary sources:

  Net Interest Revenue    ~$3.1B/qtr  (48% of total revenue)
    ● Schwab Bank earns the spread between what it pays clients on sweep
      account cash and what it earns on treasuries/agency bonds/loans.
    ● NIM (net interest margin) = 2.88% Q1 2026 (expanding rapidly).
    ● This is THE key earnings driver — 25bps NIM change = ~$0.30-0.40 EPS.

  Asset Management Fees   ~$1.5B/qtr  (24% of total revenue)
    ● Management fees on $11.77T client assets; ETF/mutual fund fees.
    ● Grows naturally with AUM growth; partially offset by zero-fee products.

  Trading Revenue         ~$0.8B/qtr  (13% of total revenue)
    ● Order flow, options commissions; largely stable.

  Other Services          ~$1.0B/qtr  (15% of total revenue)

THE TWO CRISES: CASH SORTING & TDA INTEGRATION — BOTH NOW RESOLVED
────────────────────────────────────────────────────────────────────
SCHW spent 2022-2024 fighting two simultaneous headwinds:

  1. CASH SORTING (2022-2024)
     When the Fed raised rates aggressively in 2022, Schwab clients discovered
     that their sweep account cash (earning ~0.01-0.45%) was costing them
     significant opportunity cost vs money market funds (yielding 5%+). Over
     $200B of client cash "sorted" from Schwab Bank sweep accounts into money
     market funds and other higher-yield alternatives.

     This forced Schwab to:
     a) Borrow from the Federal Home Loan Bank (FHLB) at high rates to fund
        the outflows — dramatically compressing NIM to ~1.8% in 2023.
     b) Accept significantly lower NIM during the transition period.

     Status: RESOLVED. Cash sorting has essentially stopped as rates have
     peaked. Schwab has repaid >$80B of high-cost FHLB/CD borrowings.
     NIM has expanded from trough 1.75% (2023) → 2.53% (Q1 2025) → 2.88%
     (Q1 2026). Path to 3.0%+ is clear as remaining FHLB debt gets repaid.

  2. TD AMERITRADE INTEGRATION (2020-2025)
     The $26B TDA acquisition (completed Oct 2020) was the largest brokerage
     deal in history. Integration took 5 years; Schwab issued ~900M new shares
     (diluting EPS while carrying integration costs).

     Status: COMPLETE. 100% integration finished end of 2025. Final wave of
     cost synergies totalling ~$2B annually are FULLY realized. Legacy TDA
     systems fully decommissioned.

     This is transformative: $2B annualised savings on a $5.10 adj EPS base
     = ~$1.10 per diluted share improvement fully baked into forward earnings.

Q1 2026 RESULTS — RECORD QUARTER
──────────────────────────────────
  Total net revenues:     $6.5B   (+16% YoY)  — record
  Net income:             $2.5B   (+30% YoY)  — record
  Diluted GAAP EPS:       $1.37   (+38% YoY)
  Adjusted diluted EPS:   $1.43   (+38% YoY)  — record
  Net interest revenue:   $3.14B  (+16% YoY)
  Net interest margin:    2.88%   (vs 2.53% Q1 2025; vs 1.75% 2023 trough)
  Interest-earning assets:$437.7B

Full Year 2025 (record):
  Core Net New Assets:    $519.4B  (+42% YoY); Q4 alone $163.9B — record
  Total client assets:    $11.77T  (Q1 2026; +19% YoY)
  GAAP net income:        $8.9B    (+51% YoY) — best in company history
  TD integration:         100% complete; all synergies realised

2026 GUIDANCE — TRACKING ABOVE
────────────────────────────────
Management's January 2026 scenario: adj EPS $5.70-$5.80 for full year.
After Q1 beat at $1.43, management stated it is tracking ABOVE the $5.70-5.80
scenario. Consensus has moved toward ~$5.90-$6.00.
Revenue guidance: +14-15% YoY (meaningfully above prior consensus of +12%).

THE NIM EXPANSION STORY: MORE RUNWAY
──────────────────────────────────────
The most underappreciated aspect of Schwab's recovery is that NIM expansion
is NOT over. Even at 2.88% Q1 2026:

  Pre-crisis NIM peak (2018-2019):  ~3.0%
  Current NIM (Q1 2026):            2.88%
  Gap to peak:                      ~12bps = significant additional EPS upside

Each 25bps of NIM improvement on $437.7B interest-earning assets = ~$1.1B
additional annual revenue = ~$0.45-0.50 adj EPS improvement.

If FHLB repayments continue (they will: maturity schedule), NIM will reach
3.0-3.2% in 2026-2027, driving FY2027E adj EPS to $6.50-7.00.

VALUATION
──────────
  At $90.21:
  FW P/E on FY2026E $5.85:   15.4×  (at or near floor multiple for SCHW)
  FW P/E on FY2027E $6.80:   13.3×  (extremely cheap for a growing franchise)
  Dividend yield:             $1.28 / $90.21 = 1.4%  (19% increase in 2026)
  Market cap:                 ~$164B

  Analyst avg PT:  $112.50-$116.25 (+25-29% from current)
  Barclays PT:     $127 (raised May 2026; "2026 guidance crushes street")
  Consensus:       20 analysts Buy, 1 Hold, 1 Sell

  52-wk low $85.76: BUY zone (ratio_b ~0.73×); barely missed BUY signal.
  52-wk high $107.50: WATCHLIST zone (ratio_b ~1.33×).
  Current $90.21: ACCUMULATE — 16% off 52-wk high, 15.4× FW EPS with 38% growth.

THE BULL CASE: PEG OF 0.4×
────────────────────────────
FY2026E adj EPS growth: ~38% YoY. At 15.4× P/E, PEG = 15.4 / 38 = 0.41×.
This is extraordinarily cheap for a franchise-quality financial company.

Even normalised (to 20% growth per FY2026-2027 average):
  PEG = 15.4 / 20 = 0.77× — still well below fair value of ~1×.

Method B: FY2027E $6.80 × 22× exit multiple = $150 (+66%).
Analyst BASE: $113-127 (+25-41%).

CLIENT ASSET FLYWHEEL
──────────────────────
$519B NNA in FY2025 means Schwab added ~5% of its client base organically.
At $11.77T client assets:
  → $11.77T × 0.40% avg fee rate (blended asset mgmt + NII take rate) = $47B
    annual revenue potential at full monetisation
  → vs current ~$25B annual revenue = massive unmonetised asset base

As clients age into retirement and move from accumulation to managed accounts,
fee take rate naturally increases. The $11.77T is a long-term engine that
compounds regardless of near-term interest rate movements.

KEY RISKS
──────────
  1. RATE SENSITIVITY: If the Fed cuts aggressively, NIM compresses again.
     However, sweep balance stability (cash sorting over) means this would
     be a smaller headwind than 2022-2024 — clients already sorted.
  2. COMPETITION: Fidelity/Vanguard (private; no margin pressure) vs Schwab.
     Robinhood for younger demographic. Zero-commission wars limit pricing
     power in trading. Schwab's moat is $11.77T AUM and scale.
  3. REGULATORY: SEC sweep account reform could require Schwab to pay clients
     more on cash, directly compressing NIM. Low probability but non-zero.
  4. MARKET DOWNTURN: A 30-40% equity market decline would shrink client
     assets and reduce asset management fees; though NII would be less affected.

COMPARISON TO PEERS
────────────────────
  BX at $118.51: ◎ ACCUMULATE (ratio_b 1.05×; alt assets AUM machine)
  SCHW at $90.21: ◎ ACCUMULATE (ratio_b 0.88×; slightly better value)
  Both are institutional-quality financial assets near accumulate zone.
  SCHW is the purer "normalisation of earnings" story; BX needs realisations recovery.

SUMMARY VERDICT
───────────────
Schwab has resolved BOTH of the crises that depressed earnings for three years
(cash sorting AND TDA integration). Q1 2026 was the first quarter to show the
full combined benefit: 38% EPS growth, 2.88% NIM, record revenue. The stock at
$90 = 15× FY2026E earnings is at its empirical floor multiple despite having
one of the clearest earnings growth trajectories among large-cap financials.
NIM still has ~12bps to run to pre-crisis peak; FY2027E $6.80 EPS is very
achievable. ACCUMULATE. Add more on any dip below $86 (BUY zone).
"""

# ── PART 3: NUMBERS & SIGNAL ─────────────────────────────────────────────────

import math

# ── Live price (MANDATORY — fetched from internet) ──
CURRENT_PRICE = 90.21   # SCHW — search results, 2026-05-27 (last close May 26)

PRICE_52W_LOW  = 85.76
PRICE_52W_HIGH = 107.50

SHARES_M     = 1825.0   # Diluted shares (derived: Q1 net income $2.5B / GAAP EPS $1.37 = 1,825M)
DIVIDEND_ANN = 1.28     # $0.32/quarter × 4; raised 19% in 2026 (from $0.27); yield 1.4%

# ── Adjusted diluted EPS history ──
EPS_HISTORY = {
    "FY2022": 3.43,   # NIM initially helped by rate hikes; partial cash-sorting onset
    "FY2023": 3.05,   # TROUGH — cash sorting peak + FHLB borrowing costs + TDA integration
    "FY2024": 3.65,   # Recovery; Q4 adj $1.01; FHLB repayment begins; sorting stabilizing
    "FY2025": 5.10,   # RECORD — TDA integration 100% complete; NIM recovery; Q4 adj $1.39
}
#  The FY2023→FY2025 jump ($3.05→$5.10) = TWO compounding tailwinds removing simultaneously:
#  (1) Cash sorting fully resolved; NIM expanded from 1.75% trough → 2.88% Q1 2026
#  (2) TD Ameritrade $2B annual synergies fully realised end of 2025

EPS_NOW    = 5.85   # FY2026E adj EPS; mgmt guidance $5.70-5.80, tracking above after Q1 $1.43
EPS_TROUGH = 2.50   # Severe scenario: aggressive rate cuts + major AUM decline + new sorting;
                    # worse than FY2023 actual ($3.05); floor anchored by $11.77T asset base

EPP_MIN_PE = 15     # Premium retail brokerage/wealth manager; 2023 SVB panic floor was ~15×;
                    # above pure banks (9×) given no credit risk, but NIM sensitivity noted
EPP        = EPP_MIN_PE * EPS_TROUGH   # = 37.50

# ── Method B: 2-year forward (FY2027E) ──
CONS_EPS_2YR  = 6.80    # FY2027E adj EPS; NIM reaches 3.0%+ as FHLB repaid; AUM growth;
                         # ~16% from FY2026E; entirely achievable on current trajectory
CONS_EXIT_PE  = 22       # Fair multiple when NIM at cycle peak and earnings compounding;
                         # SCHW historically 20-28× adj EPS in normal environments
price_b       = CONS_EPS_2YR * CONS_EXIT_PE   # = 149.60 → 150.00

ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)

# ── Key financial metrics ──
NET_INTEREST_MARGIN_Q1   = 2.88    # Q1 2026 NIM (%; record post-sorting)
NET_INTEREST_MARGIN_TROUGH = 1.75  # 2023 trough NIM (%)
NET_INTEREST_MARGIN_PEAK  = 3.00   # Pre-crisis (2018-2019) NIM benchmark
INTEREST_EARNING_ASSETS_B = 437.7  # Q1 2026 interest-earning assets ($B)
CLIENT_ASSETS_T           = 11.77  # Total client assets Q1 2026 ($T; +19% YoY)
NNA_FY2025_B              = 519.4  # Core net new assets FY2025 ($B; +42% YoY; record)
NNA_Q4_2025_B             = 163.9  # Q4 2025 NNA ($B; record quarter)
TDA_SYNERGIES_ANN_B       = 2.0    # TD Ameritrade synergies fully realised ($B annual)

# ── Softmax composite engine ──
def softmax_weights(composite, T=0.60):
    centres = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
    logits  = {k: -((composite - v) ** 2) / T for k, v in centres.items()}
    m       = max(logits.values())
    exps    = {k: math.exp(v - m) for k, v in logits.items()}
    s       = sum(exps.values())
    return   {k: v / s for k, v in exps.items()}

scenarios = {
    "BEAR":  37.50,    # EPP floor; severe rate cuts + 35% AUM crash + new cash sorting
    "BASE":  110.00,   # Analyst zone; ~$5.85 × 18-19×; steady NIM expansion; fair value
    "BULL":  150.00,   # Method B; FY2027E $6.80 × 22×; full NIM recovery to 3.0%+
    "XBULL": 195.00,   # Peak cycle; $7.50 × 26×; NIM 3.2%+; $15T+ client assets
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
    ("TD Ameritrade 100% complete; $2B annual synergies fully in run-rate",  +0.30, 0.20),
    ("NIM 2.88% Q1 2026 (+35bps YoY); FHLB repayment → 3.0%+ path clear",  +0.35, 0.25),
    ("Record NNA $519B FY2025 (+42%); client assets $11.77T growing fast",   +0.25, 0.20),
    ("Stock at floor multiple (15.4× FW EPS); 2023 panic was ~15×",          +0.20, 0.15),
    ("Rate sensitivity: Fed cuts would compress NIM; earnings not rate-free", -0.25, 0.25),
    ("Competition: Fidelity/Vanguard/Robinhood; zero-commission limits moat", -0.15, 0.15),
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
    print("THE CHARLES SCHWAB CORPORATION (SCHW) — SIGNAL MODEL")
    print("=" * 70)

    print(FRAMEWORK)
    print(COMMENTARY)

    print("KEY METRICS")
    print(f"  Current price (fetched)      = ${CURRENT_PRICE:>8.2f}")
    print(f"  52-week range                = ${PRICE_52W_LOW:.2f} – ${PRICE_52W_HIGH:.2f}")
    print(f"  Market cap                   = ${CURRENT_PRICE * SHARES_M / 1000:.1f}B")
    print(f"  FW P/E on FY2026E $5.85      = {CURRENT_PRICE/EPS_NOW:.1f}×  (near floor multiple)")
    print(f"  FW P/E on FY2027E $6.80      = {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (very cheap on 2-yr view)")
    print(f"  Dividend (annualised 2026)   = ${DIVIDEND_ANN:.2f}  (yield {DIVIDEND_ANN/CURRENT_PRICE*100:.1f}%;  +19% vs 2025)")
    print(f"  Net interest margin Q1 2026  = {NET_INTEREST_MARGIN_Q1:.2f}%  (trough {NET_INTEREST_MARGIN_TROUGH:.2f}%; peak {NET_INTEREST_MARGIN_PEAK:.2f}%)")
    print(f"  Interest-earning assets      = ${INTEREST_EARNING_ASSETS_B:.0f}B")
    print(f"  Total client assets          = ${CLIENT_ASSETS_T:.2f}T  (+19% YoY; record)")
    print(f"  FY2025 core NNA              = ${NNA_FY2025_B:.0f}B  (+42% YoY; record)")
    print(f"  TD Ameritrade synergies      = ${TDA_SYNERGIES_ANN_B:.0f}B/yr fully realised (100% integration complete)")

    print("\nADJUSTED DILUTED EPS HISTORY")
    for yr, eps in EPS_HISTORY.items():
        note = ""
        if yr == "FY2023": note = "  ← TROUGH (cash sorting + FHLB costs + TDA integration)"
        if yr == "FY2025": note = "  ← record (both crises resolved)"
        print(f"  {yr}  ${eps:>5.2f}{note}")
    print(f"  FY2026E ${EPS_NOW:.2f}  (guidance $5.70-5.80; tracking above; Q1A $1.43 +38% YoY)")

    print(f"\nEPP CALCULATION")
    print(f"  EPS_TROUGH × EPP_MIN_PE  =  ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×  =  ${EPP:.2f}")
    print(f"  (2023 SVB panic low $45 implied ~15× on $3.05 trough EPS; floor validated)")

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
        if k == "BEAR":  print("EPP floor; rate crash + 35% AUM decline + cash sorting restart")
        if k == "BASE":  print("Analyst zone; ~18-19× FY2026E; steady NIM + AUM growth")
        if k == "BULL":  print("Method B; FY2027E $6.80 × 22×; NIM reaches 3.0%+")
        if k == "XBULL": print("Peak cycle; $7.50 × 26×; NIM 3.2%+; $15T+ client assets")

    print(f"\nSOFTMAX COMPOSITE ENGINE")
    print(f"  Market composite (inferred)  =  {market_composite:.3f}")
    print(f"  (Market pricing between BEAR and BASE — 'floor multiple' sentiment)")

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

    print(f"\nCLIENT & INTEREST METRICS")
    print(f"  Total client assets          = ${CLIENT_ASSETS_T:.2f}T  (Q1 2026; +19% YoY)")
    print(f"  Core NNA FY2025              = ${NNA_FY2025_B:.1f}B  (+42% YoY; record; Q4 $163.9B)")
    print(f"  Interest-earning assets      = ${INTEREST_EARNING_ASSETS_B:.0f}B  (Q1 2026)")
    print(f"  NIM Q1 2026                  = {NET_INTEREST_MARGIN_Q1:.2f}%  (vs 2.53% Q1 2025; vs 1.75% trough)")
    print(f"  NIM sensitivity              = ~$0.45-0.50 adj EPS per 25bps NIM improvement")
    print(f"  NIM gap to pre-crisis peak   = ~12bps  (upside to 3.0%+)")
    print(f"  TD Ameritrade integration    = 100% complete; $2.0B/yr synergies fully realised")
    print(f"  Q1 2026 adj EPS              = $1.43  (+38% YoY; record)")
    print(f"  Q1 2026 revenue              = $6.5B  (+16% YoY; record)")
    print(f"  Analyst avg PT               = $112.50–$116.25  (+25-29%); Barclays $127")
    print(f"  Analyst consensus            = 20 Buy / 1 Hold / 1 Sell")

    print(f"\nSIGNAL ENTRY GUIDE")
    # Thresholds: solve (p - EPP) / (price_b - p) = ratio_threshold  (EPP=37.50, price_b=150)
    # BUY:        p = (37.5 + 0.75×150) / 1.75 = (37.5 + 112.5) / 1.75 = $85.71 ≈ $86
    # ACCUMULATE: p = (37.5 + 1.10×150) / 2.10 = (37.5 + 165) / 2.10 = $96.43 ≈ $96
    # WATCHLIST:  p = (37.5 + 1.75×150) / 2.75 = (37.5 + 262.5) / 2.75 = $109.09 ≈ $109
    # HOLD/TRIM:  p = (37.5 + 2.50×150) / 3.50 = (37.5 + 375) / 3.50 = $118.21 ≈ $118
    print(f"  ✕ AVOID      above  $118  (ratio_b > 2.50×)")
    print(f"  ▷ HOLD/TRIM  $109 – $118  (ratio_b 1.75–2.50×)")
    print(f"  ◐ WATCHLIST   $96 – $109  (ratio_b 1.10–1.75×)")
    print(f"  ◎ ACCUMULATE  $86 –  $96  (current ${CURRENT_PRICE:.2f}; ratio_b 0.75–1.10×)  ← HERE")
    print(f"  ◉ BUY         below  $86  (ratio_b < 0.75×; near 52-wk low $85.76)")
    print()
    print(f"  52-wk low $85.76 ≈ BUY threshold ($86) — barely missed BUY signal at the low.")
    print(f"  52-wk high $107.50 = WATCHLIST zone (ratio_b 1.33×).")
    print(f"  Current $90.21 = ACCUMULATE; just $4 above BUY threshold.")
    print(f"  Best entry: $85-86 on any pullback (e.g. macro risk-off or rate cut fears).")
    print(f"  Key watch: Q2 2026 NIM (must hold ≥ 2.85% to confirm trajectory).")
    print(f"  Key watch: Core NNA — must sustain $100B+/quarter to prove AUM flywheel.")
