"""
Wells Fargo & Company  (WFC)
BottomUp Risk/Reward Analyzer — Signal Model
"""
import math

# ── Core inputs ──────────────────────────────────────────────────────────────
TICKER        = "WFC"
COMPANY       = "Wells Fargo & Company"
SECTOR        = "Consumer Banking · Commercial Banking · Corporate & Investment Banking · Wealth Management"

CURRENT_PRICE = 76.33    # WFC — fetched from Yahoo Finance / web search, 2026-05-26; range $76.12–$76.85
PRICE_52W_LOW  = 71.93
PRICE_52W_HIGH = 97.76
SHARES_M       = 3060.0   # ~$233.58B market cap ÷ $76.33; post-buyback (Q1: 46.3M shares repurchased)
DIVIDEND_ANN   = 1.80     # $0.45/quarter declared Q1 2026

# ── EPS history (GAAP diluted — WFC doesn't report formal adjusted EPS) ──────
# FY2022 reduced by ~$3.7B regulatory/litigation charges; FY2023 by $1.9B FDIC assessment
EPS_HISTORY = {
    "FY2022": 3.01,
    "FY2023": 4.83,
    "FY2024": 5.37,
    "FY2025": 6.26,
}
EPS_NOW = 6.60   # FY2026E; Q1 2026 actual $1.60 × 4 = $6.40 annualised; $6.60 reflects modest H2 growth

# ── EPP (Earnings Power Price) — structural floor ────────────────────────────
EPS_TROUGH  = 3.50    # Severe recession (not COVID black swan): NII -15%, provision 2×, markets -20%.
                       # Calibration: FY2020 GAAP EPS $0.41 (COVID + $13B reserve build — extreme outlier).
                       # A "normal bad" recession (GFC-style without Wachovia-merger legacy losses): ~$3.50.
                       # 52-wk low $71.93 ÷ $3.50 = 20.6× stress EPS — reasonable for a top-4 US bank.
EPP_MIN_PE  = 9       # Major US bank trough; CET1 10.3% (above 8.5% regulatory min) + diversified revenues
                       # provide quality premium vs pure-regional floor of 7-8×.
EPP         = EPS_TROUGH * EPP_MIN_PE   # = $31.50

# ── Method B (2-year normalised upside ceiling) ───────────────────────────────
CONS_EPS_2YR  = 7.80   # FY2027E consensus (Truist $7.80; broad Street ~$7.50-8.00);
                         # = FY2026E $6.85 × ~14% growth; asset cap freed, balance sheet expanding.
CONS_EXIT_PE  = 13     # Modest re-rating from current 11.6× (FY2026E $6.85);
                         # 13× achievable if ROTCE reaches 15%+ (management target) and
                         # compares favourably vs WFC's own history; below JPM current 13.7× is appropriate
                         # given ROTCE gap (WFC 14.5% vs JPM 23%).
price_b = CONS_EPS_2YR * CONS_EXIT_PE   # = $101.40

# ── Primary signal ────────────────────────────────────────────────────────────
ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
# = (76.33 − 31.50) / (101.40 − 76.33) = 44.83 / 25.07 = 1.79×  → ▷ HOLD/TRIM

# ── Bank-specific metrics (Q1 2026) ──────────────────────────────────────────
TBV_PER_SHARE  = 43.03   # Tangible book value per share, Q1 2026 (Wells Fargo supplement)
BOOK_PER_SHARE = 51.20   # Estimated book value per share Q1 2026 (TBV + ~$8.17 goodwill/intangibles/share)
ROTCE          = 14.5    # Q1 2026 annualised; from 13.6% a year ago; management target 15%+
CET1_RATIO     = 10.3    # Q1 2026; within WFC target range 10%–10.5%; above 8.5% regulatory minimum
NII_Q1_2026    = 12.1    # Net interest income Q1 2026 ($B); +5% YoY; guided to grow FY2026

# ── Scenario anchors ─────────────────────────────────────────────────────────
scenarios = {
    "BEAR":  31.50,    # EPP floor; GFC-style recession. EPS $3.50 × 9× = $31.50.
    "BASE":  85.00,    # FY2027E $7.50 × 11.3× = $84.75 → $85; soft landing, ROTCE holds 14-15%.
    "BULL":  101.40,   # = price_b. ROTCE 15%+; balance sheet expansion post-cap; 13× exit.
    "XBULL": 135.00,   # FY2028E EPS ~$10 × 13.5×; ROTCE hits 17%+; WFC re-rates toward JPM/BAC multiples.
}

# ── SCA (Stock-specific Composite Adjustment) ─────────────────────────────────
sca_factors = [
    # (description,                                                       score,  weight)
    ("Asset cap removal (June 2025): 7-year restraint lifted; balance "
     "sheet free to grow; mgmt guided phased expansion — 3-5yr catalyst",  +0.35,  0.25),
    ("NII recovery + ROTCE trajectory: Q1 NII $12.1B (+5% YoY); "
     "ROTCE 13.6%→14.5%; management target 15%+",                          +0.30,  0.20),
    ("Expense efficiency: Scharf's op efficiency improving; "
     "efficiency ratio declining; $4B Q1 buybacks (capital return)",        +0.20,  0.15),
    ("ROTCE quality discount: 14.5% vs JPM 23%, BAC 16% — lowest "
     "ROTCE of big-4 US banks; structural quality gap limits re-rating",   -0.30,  0.25),
    ("NIM compression risk: NIM 2.47% (down from 2.60% YoY); "
     "rate-sensitive; each 25bps Fed cut = ~$0.8-1.0B NII headwind",       -0.25,  0.20),
    ("Revenue miss / execution: Q1 2026 revenue $21.45B missed "
     "$21.76B estimate; three analyst PT cuts post-Q1",                    -0.15,  0.15),
]

sca_raw = sum(score * weight for _, score, weight in sca_factors)
sca_adj = sca_raw / 2.0

# ── Softmax composite engine ─────────────────────────────────────────────────
def infer_composite(current_price: float, scens: dict[str, float],
                    lo: float = 1.0, hi: float = 4.0, iters: int = 60) -> float:
    bear, base, bull, xbull = scens["BEAR"], scens["BASE"], scens["BULL"], scens["XBULL"]
    centres = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
    T = 0.60
    prices = {"BEAR": bear, "BASE": base, "BULL": bull, "XBULL": xbull}
    for _ in range(iters):
        mid = (lo + hi) / 2
        logits  = {k: -(mid - centres[k])**2 / T for k in centres}
        max_l   = max(logits.values())
        exp_l   = {k: math.exp(logits[k] - max_l) for k in logits}
        denom   = sum(exp_l.values())
        weights = {k: exp_l[k] / denom for k in exp_l}
        ev = sum(weights[k] * prices[k] for k in weights)
        if ev < current_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

market_composite = infer_composite(CURRENT_PRICE, scenarios)
adj_composite    = market_composite + sca_adj

def softmax_weights(composite: float) -> dict[str, float]:
    centres = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
    T = 0.60
    logits  = {k: -(composite - centres[k])**2 / T for k in centres}
    max_l   = max(logits.values())
    exp_l   = {k: math.exp(logits[k] - max_l) for k in logits}
    denom   = sum(exp_l.values())
    return {k: exp_l[k] / denom for k in exp_l}

adj_weights = softmax_weights(adj_composite)
adj_ev      = sum(adj_weights[k] * scenarios[k] for k in adj_weights)

# ── Derived display values ────────────────────────────────────────────────────
epp_gap_pct  = (CURRENT_PRICE / EPP - 1) * 100
upside_b_pct = (price_b / CURRENT_PRICE - 1) * 100
dn_epp_pct   = (EPP / CURRENT_PRICE - 1) * 100
ptbv_current = CURRENT_PRICE / TBV_PER_SHARE
# Gordon Growth dual check
ke, g = 0.09, 0.04
warranted_ptbv_peak   = (ROTCE/100 - g) / (ke - g)
warranted_price_peak  = warranted_ptbv_peak  * TBV_PER_SHARE
rotce_stress          = 10.0   # recession ROTCE
warranted_ptbv_stress = (rotce_stress/100 - g) / (ke - g)
warranted_price_stress = warranted_ptbv_stress * TBV_PER_SHARE
mkt_cap_b = CURRENT_PRICE * SHARES_M / 1000

# ── Signal label ──────────────────────────────────────────────────────────────
def signal_label(r: float) -> str:
    if r < 0:      return "◉ BUY"
    if r < 0.75:   return "◉ BUY"
    if r < 1.10:   return "◎ ACCUMULATE"
    if r < 1.75:   return "◐ WATCHLIST"
    if r < 2.50:   return "▷ HOLD/TRIM"
    return "✕ AVOID"

signal = signal_label(ratio_b)


# ════════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    sep  = "=" * 72
    line = "─" * 72
    thin = "━" * 72

    print(sep)
    print(f"  {TICKER}  —  {COMPANY}")
    print(f"  {SECTOR}")
    print(sep)

    print()
    print("PART 1 — FRAMEWORK OVERVIEW")
    print(thin)
    print(f"""Special context: WFC is valued using the same dual-lens approach as JPM/BAC
(P/E vs through-cycle earning power + P/TBV vs ROTCE). Key WFC vs peers:

  WFC P/TBV (current)  : {ptbv_current:.2f}×  vs JPM 2.83×  vs BAC 1.78×  ← WFC middle
  WFC ROTCE (Q1 2026)  : {ROTCE:.1f}%  vs JPM 23%    vs BAC 16%  ← WFC lowest of big-4
  WFC ratio_b          : {ratio_b:.2f}×   vs JPM 2.27× vs BAC 2.17× ← similar risk/reward
  WFC CET1 ratio       : {CET1_RATIO:.1f}%  vs JPM 14.3% vs BAC 12%  ← WFC lowest capital
  WFC NIM (Q1 2026)    : 2.47%  (declining; most pressured NIM of big-4)
  DEFINING CATALYST    : Asset cap REMOVED June 2025 — 7-year constraint lifted

Gordon Growth (P/TBV vs ROTCE) dual check:
  Warranted P/TBV = (ROTCE {ROTCE:.1f}% − g {g*100:.0f}%) / (Ke {ke*100:.0f}% − g {g*100:.0f}%) = {warranted_ptbv_peak:.2f}×
  Warranted price = {warranted_ptbv_peak:.2f}× × ${TBV_PER_SHARE:.2f} TBV = ${warranted_price_peak:.2f}
  Current {ptbv_current:.2f}× TBV vs warranted {warranted_ptbv_peak:.2f}× → WFC is THEORETICALLY CHEAP.
  (This distinguishes WFC from BAC and JPM — both of which trade near or above warranted.)
  However: ROTCE {ROTCE:.1f}% is early-recovery, not terminal. If recession hits (ROTCE {rotce_stress:.0f}%):
    Warranted = {warranted_ptbv_stress:.2f}× TBV = ${warranted_price_stress:.2f}  — well below current price.
  This tension (cheap at current ROTCE; risky in recession) explains HOLD/TRIM.

Key metrics (Q1 2026, Jan–Mar 2026):
  Revenue (net)       : $21.45B (+6% YoY; missed estimate $21.76B)
  NII                 : ${NII_Q1_2026:.1f}B   (+5% YoY; beat $11.96B est; NIM 2.47% declining)
  EPS (diluted)       : $1.60   (+15% YoY; beat estimate $1.58)
  Net income          : $5.3B   (+7% YoY)
  Capital return      : $4.0B buybacks + $1.4B dividends = $5.4B total in one quarter
  ROTCE               : {ROTCE:.1f}%    (from 13.6% a year ago; target 15%+)
  TBV per share       : ${TBV_PER_SHARE:.2f}  (P/TBV: {ptbv_current:.2f}×)
  CET1 ratio          : {CET1_RATIO:.1f}%    (within target range 10.0%–10.5%)

EPP (Earnings Power Price) — structural floor
  = EPS_TROUGH × EPP_MIN_PE
  Stress EPS (${EPS_TROUGH:.2f}) × {EPP_MIN_PE}× floor.
  ${EPS_TROUGH:.2f}: NII -15% ($12.1B→$10.3B), credit provisions 2× ($2.4B→$4.8B),
  markets/IB -20%. Pre-tax impact ~-$8B → net income ~$11B → EPS ~$3.60 → $3.50.
  Calibration: WFC FY2020 GAAP EPS $0.41 (COVID + $13B reserve build + Wachovia
  legacy runoff — extreme black swan; not an appropriate recurring floor).
  $3.50 represents a "real" recession (bad credit + NIM compression) without
  the specific one-time legacy write-offs of FY2020. WFC 52-wk low $71.93 ÷
  $3.50 = 20.6× stress EPS — the worst 2025/2026 trading day priced in 20×
  the catastrophe EPS, consistent with market confidence in WFC's survival.
  EPP = ${EPP:.2f}.

Method B — 2-year normalised upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E ~${CONS_EPS_2YR:.2f} (FY2026E $6.85 × ~14% growth; asset cap freed + NII expansion
  + buybacks reducing share count; Truist and Street consensus cluster $7.50-8.00)
  × {CONS_EXIT_PE}× exit P/E (current {CURRENT_PRICE/EPS_NOW:.1f}×; 13× achievable if ROTCE hits 15%+;
  discount to JPM 13.7× appropriate given ROTCE gap; premium to current 11.6×
  justified by ROTCE improvement trajectory).
  = ${price_b:.2f}.
  Ratio B = (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f}) = ${CURRENT_PRICE-EPP:.2f} / ${price_b-CURRENT_PRICE:.2f} = {ratio_b:.2f}×
  → {signal}. Method B upside: +{upside_b_pct:.1f}% to ${price_b:.2f}. Downside to EPP: {dn_epp_pct:.1f}%.
  The 52-wk low ${PRICE_52W_LOW:.2f} was the WATCHLIST/ACCUMULATE entry (ratio_b ~1.37×).
  The easy money is made; now HOLD/TRIM territory.
{thin}
""")

    print()
    print("PART 2 — ANALYST COMMENTARY & CONTEXT")
    print(thin)
    print(f"""
WELLS FARGO: THE REFORM STORY — NOW AN EXECUTION STORY
=======================================================

Wells Fargo is the third-largest US bank by assets (~$1.95T) and the largest
US consumer bank by branch count. Under CEO Charlie Scharf (since Oct 2019),
WFC has been transformed from a compliance disaster into a functioning, well-
governed bank — but the ROTCE gap vs peers (14.5% vs JPM 23%) means the
transformation work is ongoing, not complete.

THE DEFINING CATALYST: ASSET CAP REMOVAL — JUNE 2025
=====================================================
In February 2018, the Federal Reserve imposed a unique punishment: WFC was
barred from growing assets above ~$1.95 trillion — its year-end 2017 level.
This cap, placed in response to the 2016 fake-accounts scandal (~3.5M
unauthorised accounts), constrained WFC's ability to grow loans, deposits,
and capital markets activity for SEVEN YEARS.

The cap was lifted in June 2025 after WFC satisfied all outstanding consent
orders. This was the most significant positive catalyst for WFC in a decade:

  BEFORE cap removal: WFC had to turn away deposits, shrink loan books,
  pass on IB deal flow, exit certain products — costing billions in lost revenue.
  AFTER cap removal: WFC can compete fully with JPM, BAC, and C for the first
  time since 2018. Balance sheet growth, loan expansion, and IB market share
  recovery can all now proceed.

Market reaction: WFC stock surged from ~$55-60 pre-removal anticipation to
a 52-wk high of $97.76 — fully pricing in the narrative within 12 months.
Since the ATH, WFC has pulled back 22% to $76.33, primarily on:
  (1) NIM compression: NIM fell from 2.60% (Q1 2025) to 2.47% (Q1 2026)
  (2) Revenue miss: Q1 2026 revenue $21.45B missed $21.76B estimate
  (3) Three analyst PT cuts post-Q1 2026 results
  (4) General macro/tariff uncertainty

The selloff is an opportunity to re-examine WFC on fundamentals rather than narrative.

ROTCE RECOVERY — THE CENTRAL INVESTMENT THESIS
===============================================
WFC's ROTCE has been recovering since the GFC-era nadirs:
  FY2020: ~5% (COVID provisioning)
  FY2022: ~9.6% (NII expansion beginning; regulatory costs peak)
  FY2023: ~11% (NII peak; then declined; FDIC assessment $1.9B)
  FY2024: ~13% (NII stabilising; efficiency improving)
  FY2025: ~14% (ROTCE acceleration; asset cap removal pending)
  Q1 2026: {ROTCE:.1f}% (management target 15%+)

The trajectory is clearly positive. Management's target of 15%+ is achievable.
But it requires continued NII growth (which NIM compression threatens) AND
loan/fee income growth (which the asset cap removal unlocks).

The KEY TENSION in the WFC thesis:
  Gordon Growth at current ROTCE {ROTCE:.1f}%: warranted P/TBV {warranted_ptbv_peak:.2f}× = ${warranted_price_peak:.2f}
  Current P/TBV {ptbv_current:.2f}× → CHEAP vs warranted at current ROTCE
  BUT: If recession hits and ROTCE reverts to {rotce_stress:.0f}%:
    Warranted P/TBV {warranted_ptbv_stress:.2f}× = ${warranted_price_stress:.2f} — 32% BELOW current price

WFC's ROTCE {ROTCE:.1f}% is LOWER than BAC (16%) and JPM (23%). This means WFC has
MORE UPSIDE if ROTCE continues improving, but MORE DOWNSIDE in a recession.

Q1 2026 — EARNINGS BEAT, REVENUE MISS
=======================================
  Revenue:       $21.45B  (+6% YoY; MISSED estimate $21.76B — driven by NIM compression)
  NII:           ${NII_Q1_2026:.1f}B    (+5% YoY; beat $11.96B; but NIM fell 13bps QoQ to 2.47%)
  Diluted EPS:   $1.60    (+15% YoY; beat estimate $1.58)
  Net income:    $5.3B    (+7%)
  ROTCE:         {ROTCE:.1f}%    (from 13.6% a year ago; target 15%+)
  TBV/share:     ${TBV_PER_SHARE:.2f}
  CET1:          {CET1_RATIO:.1f}%    (within 10.0-10.5% target)
  Buybacks:      $4.0B    (46.3M shares — substantial capital return)

The NIM decline is the most concerning data point. WFC earns a relatively
thin net interest margin (2.47%) vs JPM (~2.80%) because WFC's deposit mix
skews heavily to lower-yielding consumer/small-business accounts. As the Fed
cuts rates, WFC's NIM faces structural headwinds:
  Each 25bps Fed cut → ~$0.8-1.0B annual NII headwind
  Market pricing 2 more cuts in 2026 → potential -$1.6-2.0B NII impact

Counter: Fee income (investment banking, mortgage, wealth management) grows
as rates decline. WFC's IB platform (formerly constrained by asset cap) can
now take market share in deals, advisory, and underwriting.

NIM COMPRESSION — THE KEY BEAR CASE
=====================================
Wells Fargo's NIM peaked at ~2.92% in early 2023 (high-rate environment) and
has been compressing since. At 2.47% in Q1 2026 it is 13bps below Q4 2025 and
45bps below the peak. The rate outlook is the single biggest variable:

  BULL: Fed holds or raises → NIM stabilises → NII accelerates → ROTCE 16%+
  BASE: Fed cuts 2× → NIM compresses to ~2.35% → NII grows slowly → ROTCE 15%
  BEAR: Recession → Fed cuts to 2.5-3% → NIM collapses to ~2.0-2.1% →
        NII -15-20% from peak → ROTCE 10-11% → stock rerate to $46-52

This NIM sensitivity, combined with WFC's below-peer ROTCE starting point,
makes WFC the most "rate-levered" of the big-4 banks.

WFC vs PEERS — THE QUALITY LEAGUE TABLE
=========================================
                WFC         BAC         JPM
  ROTCE         {ROTCE:.1f}%       16%         23%      ← WFC lowest
  P/TBV         {ptbv_current:.2f}×       1.78×       2.83×    ← WFC cheapest
  CET1          {CET1_RATIO:.1f}%        12.0%       14.3%    ← WFC lowest capital
  NIM           2.47%       2.5%+       2.80%    ← WFC most compressed
  Market cap    ~$233B      ~$368B      ~$824B
  P/E fwd       11.6×       12.9×       13.7×    ← WFC cheapest

Gordon Growth at current ROTCE:
  WFC warranted P/TBV: (14.5%-4%)/(9%-4%) = {warranted_ptbv_peak:.2f}× → ${warranted_price_peak:.2f}  ← ABOVE current
  BAC warranted P/TBV: (16%-4%)/(9%-4%) = 2.40× → $69.55
  JPM warranted P/TBV: (23%-4%)/(9%-4%) = 3.80× → $414

WFC is the ONLY one of the three trading below its Gordon Growth warranted price
at current ROTCE. This is genuinely interesting — it suggests the market is either:
  (a) Discounting WFC's current ROTCE as unsustainably high (recession risk), OR
  (b) Applying a "quality discount" for lowest ROTCE + NIM pressure + cap legacy

In a world with no recession and ROTCE improving to 15-16%:
  Warranted at 15% ROTCE: (15%-4%)/(9%-4%) = 2.20× × $43.03 TBV = $94.67
  Warranted at 16% ROTCE: (16%-4%)/(9%-4%) = 2.40× × $43.03 TBV = $103.27

The asymmetry: if ROTCE improves (more likely given asset cap removal + efficiency gains),
WFC at $76 looks genuinely cheap vs warranted $90-103. If recession hits, warranted $46-52.

SCHARF'S TRANSFORMATION — WHAT'S DONE AND WHAT'S NOT
======================================================
Charlie Scharf's five-year transformation of WFC:

DONE:
  ✓ All outstanding consent orders satisfied (asset cap removed June 2025)
  ✓ Risk management overhaul: 3 lines of defence, independent risk function
  ✓ Consumer banking simplification: mortgage, auto, student lending restructured
  ✓ Technology modernisation: $10B+ annual tech spend; core banking migration
  ✓ Expense discipline: efficiency ratio from 78% (2019) toward 63-65% (2026)
  ✓ Capital return: 2025 buybacks $15B+; Q1 2026 alone $4B (annualised $16B+)

IN PROGRESS:
  → Corporate & IB: rebuilding advisory, underwriting, leverage finance capabilities
    constrained by asset cap. Only now (post-cap) can WFC compete for mandates.
  → Wealth management: Merrill Lynch analogue; growing high-net-worth business
  → ROTCE bridge from 14.5% to 15%+ target: requires NII stability + fee growth

NOT YET:
  ✗ ROTCE parity with peers (JPM 23%, BAC 16%) — achievable at 16-18% in 3-5yr
  ✗ Full franchise re-rating (WFC historically traded at P/TBV discount to JPM/BAC)

ENTRY/EXIT FRAMEWORK
====================
  ◉ BUY        : $45-55  (1.4-1.7× EPP; equivalent to GFC-era or COVID-era pricing)
  ◎ ACCUMULATE : $56-68  (1.8-2.2× EPP; below 52-wk low; Buffett-ENTRY territory)
  ◐ WATCHLIST  : $68-76  (approaching HOLD; 52-wk low $71.93 was entry; Gordon Growth cheap)
  ▷ HOLD/TRIM  : $76-88  (current; above 52-wk low but below ATH; HOLD/TRIM)
  ✕ TRIM HARD  : >$88    (approaching price_b; trim hard above $92-95)

The 52-wk low of $71.93 (April 2026 market sell-off) was the WATCHLIST/ACCUMULATE
entry at ratio_b ~1.37×. From there WFC has recovered +6%. Current $76.33 is
still modestly below warranted at current ROTCE ($90.36) — NOT expensive —
but not a screaming buy either. HOLD existing positions; wait for $68-72 to add.
""")
    print(thin)

    print()
    print("PART 3 — NUMBERS & SIGNALS")
    print(thin)

    print(f"""
  I. PRICE & VALUATION SNAPSHOT
  {line}
  Current price   : ${CURRENT_PRICE:.2f}  (52-wk range: ${PRICE_52W_LOW:.2f}–${PRICE_52W_HIGH:.2f})
  vs 52-wk low    : +{(CURRENT_PRICE/PRICE_52W_LOW-1)*100:.1f}%   |   vs 52-wk high: {(CURRENT_PRICE/PRICE_52W_HIGH-1)*100:.1f}%
  Market cap      : ~${mkt_cap_b:.0f}B   |   Shares: ~{SHARES_M/1000:.2f}B
  Dividend (ann)  : ${DIVIDEND_ANN:.2f}   |   Yield: {DIVIDEND_ANN/CURRENT_PRICE*100:.2f}%
  TBV per share   : ${TBV_PER_SHARE:.2f}  |   P/TBV: {ptbv_current:.2f}×
  ROTCE (Q1 2026) : {ROTCE:.1f}%     |   CET1 ratio: {CET1_RATIO:.1f}%
  Forward P/E     : {CURRENT_PRICE/EPS_NOW:.1f}×  (on FY2026E ${EPS_NOW:.2f})
  NIM (Q1 2026)   : 2.47%  (declining; peak 2.92% Q1 2023; key bear case variable)
  Gordon Growth   : warranted P/TBV {warranted_ptbv_peak:.2f}× → ${warranted_price_peak:.2f}  |  stress P/TBV {warranted_ptbv_stress:.2f}× → ${warranted_price_stress:.2f}
  Asset cap       : REMOVED June 2025 — 7-year $1.95T asset ceiling lifted by Fed

  II. EPS HISTORY (GAAP diluted)
  {line}
  FY2022  : $3.01  (included ~$3.7B regulatory/litigation charges; opex peak)
  FY2023  : $4.83  (included $1.9B FDIC special assessment; NII peaked mid-year)
  FY2024  : $5.37  (+11.2%; NII stabilising; expense discipline bearing fruit)
  FY2025  : $6.26  (+16.6%; ROTCE improving; asset cap removal imminent)
  FY2026E : ${EPS_NOW:.2f}  (Q1 actual $1.60 ×4 = $6.40 annualised; $6.60 with H2 growth)
  FY2027E : ${CONS_EPS_2YR:.2f}  (used for Method B; +{(CONS_EPS_2YR/EPS_NOW-1)*100:.0f}% from FY2026E; balance sheet + fee growth)
  Q1 2026 : $1.60  (beat $1.58; +15% YoY; EPS beat despite revenue miss = buyback leverage)

  III. EPP & METHOD B
  {line}
  EPS_TROUGH  : ${EPS_TROUGH:.2f}/share  (severe recession; NII -15% + prov 2× + markets -20%)
  EPP_MIN_PE  : {EPP_MIN_PE}×          (major bank trough; CET1 10.3% provides quality premium)
  EPP (floor) : ${EPP:.2f}       (= ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×; WFC COVID low ~$22 reflects $0.41 EPS black swan)
  EPP gap     : +{epp_gap_pct:.1f}%   (current price is {CURRENT_PRICE/EPP:.1f}× above EPP floor)

  CONS_EPS_2YR: ${CONS_EPS_2YR:.2f}/share  (FY2027E; Truist $7.80; Street ~$7.50-8.00)
  CONS_EXIT_PE: {CONS_EXIT_PE}×          (current {CURRENT_PRICE/EPS_NOW:.1f}×; 13× as ROTCE improves to 15%+)
  Method B    : ${price_b:.2f}       (= ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×; near analyst avg PT $96.32)
  Upside to B : +{upside_b_pct:.1f}%
  Downside EPP: {dn_epp_pct:.1f}%

  ┌─────────────────────────────────────────────────────────────────────┐
  │  RATIO B = ({CURRENT_PRICE:.2f} − {EPP:.2f}) / ({price_b:.2f} − {CURRENT_PRICE:.2f})                │
  │           = {CURRENT_PRICE-EPP:.2f} / {price_b-CURRENT_PRICE:.2f} = {ratio_b:.2f}×                               │
  │  SIGNAL   = {signal}                                      │
  └─────────────────────────────────────────────────────────────────────┘

  IV. STOCK-SPECIFIC COMPOSITE ADJUSTMENT (SCA)
  {line}
  Factor                                                 Score      Wt  Contrib
  ────────────────────────────────────────────────────  ──────  ──────  ───────""")

    for desc, score, wt in sca_factors:
        short = desc[:51].ljust(51)
        print(f"  {short}  {score:+.2f}    {wt:.2f}   {score*wt:+.3f}")

    print(f"""  ────────────────────────────────────────────────────  ──────  ──────  ───────
  SCA raw                                                                {sca_raw:+.3f}
  SCA adj (÷2.0)                                                         {sca_adj:+.3f}

  V. COMPOSITE INFERENCE
  {line}
  Market composite  : {market_composite:.3f}  ({"BASE" if 1.625<=market_composite<2.375 else "BEAR" if market_composite<1.625 else "BULL/XBULL"})
  Adj composite     : {adj_composite:.3f}  ({"BASE" if 1.625<=adj_composite<2.375 else "BEAR" if adj_composite<1.625 else "BULL/XBULL"})
  Softmax weights at adj composite ({adj_composite:.3f}):""")

    scen_prices = {"BEAR": scenarios["BEAR"], "BASE": scenarios["BASE"],
                   "BULL": scenarios["BULL"], "XBULL": scenarios["XBULL"]}
    for k, w in adj_weights.items():
        print(f"    {k:<6}: {w*100:.1f}%  (${scen_prices[k]:.0f})")

    print(f"""  Expected price (adj): ${adj_ev:.1f}  vs current ${CURRENT_PRICE:.2f}  (Δ {(adj_ev/CURRENT_PRICE-1)*100:+.1f}%)

  VI. SCENARIOS SUMMARY
  {line}
  BEAR  (${scenarios['BEAR']:.0f}) : Recession + NIM collapse. NII -15% ($12.1B→$10.3B); provisions 2×
               ($2.4B→$4.8B); markets/IB -20%. ROTCE collapses to 9-10%. EPS $3.50 × 9×.
               CET1 10.3% means WFC SURVIVES without dilution. Calibration: WFC March 2020
               low was $22 (EPS $0.41 black swan); $31.50 represents a less extreme floor.
               {(scenarios['BEAR']/CURRENT_PRICE-1)*100:.0f}% from current.

  BASE  (${scenarios['BASE']:.0f}) : Soft landing. NII $49B+ FY2027 (modest growth despite NIM pressure);
               IB market share recovery post-cap; ROTCE 14.5-15%; buybacks $14-16B/yr.
               FY2027E $7.50 × 11.3× = $84.75 → $85. No multiple re-rating — just EPS.
               {(scenarios['BASE']/CURRENT_PRICE-1)*100:+.0f}% from current.

  BULL  (${scenarios['BULL']:.0f}) : = price_b. ROTCE hits 15%+; asset cap grows loan book; NII holds
               above $50B; multiple re-rates to 13× as ROTCE gap vs BAC/JPM narrows.
               FY2027E ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×. Analyst avg PT $96.32 is between BASE and BULL.
               {(scenarios['BULL']/CURRENT_PRICE-1)*100:+.0f}% from current.

  XBULL (${scenarios['XBULL']:.0f}) : Full ROTCE re-rating to 16-18%. Asset cap removal drives 3-yr balance sheet
               expansion; IB market share from Citi/GS; WFC closes P/TBV gap with JPM.
               FY2028E EPS ~$10 × 13.5× = $135. Scharf's transformation fully vindicated.
               Scharf says 15%+ ROTCE; market re-rates to 15.5× on the path to 17-18%.
               {(scenarios['XBULL']/CURRENT_PRICE-1)*100:+.0f}% from current.

{"=" * 72}
  END OF REPORT -- {TICKER}  |  Generated 2026-05-26
{"=" * 72}""")
