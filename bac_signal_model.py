"""
Bank of America Corporation (NYSE: BAC) — BottomUp Risk/Reward Signal Model

SIGNAL:  ▷ HOLD/TRIM
RATIO B: 2.17x  (Method B $4.80 × 14× = $67.20; ratio 33.70/15.50 = 2.17×)
DATE:    2026-05-26

NOTE: EPS figures are GAAP diluted unless noted. BAC's reported EPS is
relatively clean historically — limited adjustments needed. Key one-time
items flagged where material. BAC is the most NII-sensitive major US bank:
$2T+ deposits means every Fed rate cut is a direct P&L headwind of ~$1-1.5B/yr.
The "Buffett exit" (Berkshire sold entire ~1B share stake, 2024-2025) is the
single most important valuation signal for this model.
"""

import math

TICKER  = "BAC"
COMPANY = "Bank of America Corporation"
SECTOR  = "Consumer Banking · Global Markets & Investment Banking · NII Franchise · Wealth Management (MLWM)"

# ── current price (Yahoo Finance, 2026-05-22; May 25 range $51.38-$52.15) ──
CURRENT_PRICE  = 51.70   # BAC — fetched from Yahoo Finance, 2026-05-22
PRICE_52W_LOW  = 42.35   # 52-week low (late 2025 selloff)
PRICE_52W_HIGH = 57.55   # 52-week high
SHARES_M       = 7520.0  # diluted shares (~7.52B); buyback programme ~$4-5B/yr
DIVIDEND_ANN   = 1.12    # $0.28/quarter; yield ~2.2%; raised 2× since 2023

# ── special bank metrics ──────────────────────────────────────────────────
TBV_PER_SHARE  = 28.98   # tangible book value per share (Q1 2026; Mar 2026)
ROTCE          = 16.0    # Q1 2026 annualised; medium-term target 16-18%
CET1_RATIO     = 12.0    # estimated CET1 (Q1 2026; above 10% regulatory minimum)
NII_Q1_2026    = 15.9    # Q1 2026 NII $B (+9% YoY; full-year guidance +6-8%)

# ── EPS history — GAAP diluted ───────────────────────────────────────────
EPS_FY2022 = 3.19   # GAAP; NII expansion beginning; reserve releases helped
EPS_FY2023 = 3.10   # GAAP; NII peaked early then declined; AOCI unrealised losses
                    # hit book value; NII guided down, caused stock to fall to ~$24
EPS_FY2024 = 3.21   # GAAP; +3.6%; NII trough/bottoming; trading and fees offset
EPS_FY2025 = 3.81   # GAAP; +18.7%; NII recovering; trading strong; ROTCE ~14%
EPS_NOW    = 4.00   # FY2026E (post-Q1 beat); Q1 actual $1.11 (+25% YoY; beat $1.01)
                    # NII guidance raised to +6-8% for FY2026; annualised Q1: ~$4.44
                    # Using $4.00 (conservative; seasonal variation; rate cut risk)

# ── EPP — earnings power price (structural floor) ────────────────────────
EPS_TROUGH = 2.00    # severe recession: NII -20% ($63B→$50B), credit costs 2.5×
                     # normal (~$12.5B vs $5B), markets revenue -15%.
                     # Impact: ~-$19B pre-tax = ~-$14B after-tax on ~$34B net income.
                     # Stressed net income ~$17B; ÷ 7.5B shares = ~$2.27 → $2.00 rounded.
                     # Calibration: BAC FY2020 GAAP EPS ~$2.32 (COVID; $11B reserve builds).
                     # $2.00 = slightly more stressed than COVID; appropriate for GFC-style.
EPP_MIN_PE = 9       # Large bank trough P/E with slight quality premium over pure
                     # commoditised lenders. BAC COVID low: $18.10 (Mar 2020) ÷ $2.32
                     # = 7.8× — actual trough was below 9×, so 9× is slightly
                     # conservative (above the historical floor). Modern BAC has better
                     # capital (CET1 ~12% vs 10% in 2019) justifying a modest premium.
EPP = EPS_TROUGH * EPP_MIN_PE   # $18.00

# ── Method B — 2-year normalised upside ceiling ───────────────────────────
CONS_EPS_2YR = 4.80   # FY2027E: FY2026E $4.00 + 20% growth via: NII +6-8%/yr
                      # (~$2-2.5B), IB fee upcycle (~$1B), buybacks ~3-4% share
                      # reduction, operating leverage. Assumes no major credit cycle.
                      # Conservative vs analyst estimates of ~$4.97 for FY2027E.
CONS_EXIT_PE = 14     # BAC historical P/E range: 9-16×. Current 12.9×.
                      # 14× requires ROTCE sustaining above 16% (medium-term target
                      # 16-18%); achievable if NII recovery continues and deregulation
                      # tailwinds materialise. Not aggressive — BAC has touched 14-15×
                      # during NII upcycles (2021-2022). Below JPM's current 13.7×,
                      # appropriately reflecting lower ROTCE (16% vs JPM 23%).
price_b = CONS_EPS_2YR * CONS_EXIT_PE   # $67.20

ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
# = (51.70 − 18.00) / (67.20 − 51.70) = 33.70 / 15.50 = 2.17×
# → ▷ HOLD/TRIM. BAC is running a much better bank than 3 years ago, but
# the stock has already re-rated substantially (+22% from 52-wk low) and
# Buffett's exit signals the easy money has been made. Method B only +30%
# from current. Hold existing positions; await a pullback to $42-46 to ACCUMULATE.

epp_gap_pct = (CURRENT_PRICE - EPP) / EPP * 100
# = (51.70 − 18.00) / 18.00 × 100 = 187.2%

# P/TBV analysis (Gordon Growth model)
ptbv_current  = CURRENT_PRICE / TBV_PER_SHARE          # 1.78× (below warranted)
ptbv_warranted = (ROTCE/100 - 0.04) / (0.09 - 0.04)    # 2.4× (ROTCE 16%, g=4%, Ke=9%)
ptbv_implied   = ptbv_warranted * TBV_PER_SHARE         # $69.55 (warranted price)
ptbv_stress    = (0.12 - 0.04) / (0.09 - 0.04)         # 1.6× (ROTCE 12% recession)
price_ptbv_stress = ptbv_stress * TBV_PER_SHARE         # $46.37

# ── price scenarios ───────────────────────────────────────────────────────
PRICE_BEAR  = 18     # = EPP. GFC-style recession: NII -20%, credit costs 2.5×,
                     # ROTCE collapses to 5-6%. BAC March 2020 low was ~$18.10.
                     # CET1 12% means BAC SURVIVES but EPS craters to ~$2.
                     # -65% from current. BAC hit $5-6 in 2009 (GFC);
                     # $18 is the modern-era stress floor given better capital.
PRICE_BASE  = 58     # FY2027E $4.80 × 12.1× = $58. Multiple flat; no re-rating.
                     # NII grows 6-8%; credit benign; buybacks add ~3% EPS boost.
                     # Near prior ATH $57.55; represents recovery to prior peak.
                     # +12% from current.
PRICE_BULL  = 67     # = price_b. FY2027E $4.80 × 14×. ROTCE hits 17-18%;
                     # deregulation reduces compliance costs; NII beats as loans grow;
                     # IB fees sustain $3B+ quarterly run-rate. Multiple re-rates.
                     # +30% from current.
PRICE_XBULL = 90     # FY2028E ~$6.00 × 15×. Full NII recovery; ROTCE expansion
                     # to 18-20% (closing the gap with JPM); buybacks at $6B+/yr;
                     # deregulation unlocks capital deployment; market share gains
                     # in wealth management and IB. +74% from current.

# ── SCA (stock-specific composite adjustment) ────────────────────────────
SCA_FACTORS = [
    # (description, score, weight)
    ("NII recovery upcycle: $15.9B Q1 +9% YoY; FY2026 guidance raised to +6-8%; loan repricing + deposit cost stabilisation; largest NII franchise in US consumer banking", +0.35, 0.25),
    ("IB & trading renaissance: equities trading best quarter in 15 years (+30% to $2.83B); Q1 total trading $8.5B+; M&A upcycle benefiting Global Markets; BAML IB fees recovering", +0.25, 0.20),
    ("Consumer franchise + digital: 90M+ relationships; #1 in digital banking users; Zelle dominant; Merrill Lynch wealth management $3.5T+ AUM; fee income diversifies NII", +0.15, 0.15),
    ("Buffett exit (-): Berkshire sold entire ~1B share position (2024-2025); Buffett accumulated in 2011 at ~$5-7; his complete exit at $35-45 is strongest possible 'fully valued' signal", -0.40, 0.25),
    ("NII rate sensitivity: most rate-sensitive major US bank; $2T+ deposits; each 25bps Fed cut = ~$1-1.5B annual NII headwind; 2 more 2026 cuts = -$2-3B impact (~$0.30/share)", -0.25, 0.15),
]

sca_raw = sum(s * w for _, s, w in SCA_FACTORS)   # +0.0225
sca_adj = sca_raw / 2.0                             # +0.011

# ── softmax scenario engine ───────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  {"price": PRICE_BEAR,  "centre": 1.25},
    "BASE":  {"price": PRICE_BASE,  "centre": 2.00},
    "BULL":  {"price": PRICE_BULL,  "centre": 2.75},
    "XBULL": {"price": PRICE_XBULL, "centre": 3.75},
}
T = 0.60

def softmax_weights(composite):
    logits = {k: -((composite - v["centre"]) ** 2) / T for k, v in SCENARIOS.items()}
    m = max(logits.values())
    exps = {k: math.exp(v - m) for k, v in logits.items()}
    s = sum(exps.values())
    return {k: exps[k] / s for k in exps}

def expected_price(composite):
    w = softmax_weights(composite)
    return sum(w[k] * SCENARIOS[k]["price"] for k in SCENARIOS)

def infer_composite(target_price, lo=1.0, hi=4.0, iterations=60):
    for _ in range(iterations):
        mid = (lo + hi) / 2
        if expected_price(mid) < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

market_composite = infer_composite(CURRENT_PRICE)
adj_composite    = market_composite + sca_adj

# ── signal classification ─────────────────────────────────────────────────
def classify(rb):
    if   rb < 0.75: return "◉ BUY"
    elif rb < 1.10: return "◎ ACCUMULATE"
    elif rb < 1.75: return "◐ WATCHLIST"
    elif rb < 2.50: return "▷ HOLD/TRIM"
    else:           return "✕ AVOID"

signal = classify(ratio_b)   # ▷ HOLD/TRIM

# ════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    W = softmax_weights(adj_composite)
    exp_p = expected_price(adj_composite)

    print("=" * 72)
    print(f"  {TICKER}  —  {COMPANY}")
    print(f"  {SECTOR}")
    print("=" * 72)

    print(f"""
PART 1 — FRAMEWORK OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Special context: BAC is valued using the same dual-lens approach as JPM
(P/E vs through-cycle earning power + P/TBV vs ROTCE). Key BAC vs JPM:

  BAC P/TBV (current)  : {ptbv_current:.2f}×  vs JPM 2.83×  ← BAC cheaper on P/TBV
  BAC ROTCE (Q1 2026)  : {ROTCE:.0f}%    vs JPM 23%   ← BAC lower quality ROTCE
  BAC ratio_b          : {ratio_b:.2f}×   vs JPM 2.27× ← similar risk/reward
  BAC CET1 ratio        : {CET1_RATIO:.1f}%  vs JPM 14.3% ← JPM more fortified
  BAC NII sensitivity   : HIGHEST of major US banks ($2T deposits)
  Buffett exit          : Berkshire sold ~1B shares (2024-2025) — definitive signal

Gordon Growth (P/TBV vs ROTCE) dual check:
  Warranted P/TBV = (ROTCE {ROTCE:.0f}% − g 4%) / (Ke 9% − g 4%) = {ptbv_warranted:.1f}×
  Warranted price = {ptbv_warranted:.1f}× × ${TBV_PER_SHARE:.2f} TBV = ${ptbv_implied:.2f}
  Current {ptbv_current:.2f}× TBV vs warranted {ptbv_warranted:.1f}× → BAC is THEORETICALLY cheap.
  However: ROTCE {ROTCE:.0f}% is a CYCLICAL PEAK. If ROTCE reverts to 12% (mild recession):
    Warranted = {ptbv_stress:.1f}× TBV = ${price_ptbv_stress:.2f}  — BELOW current price.
  This tension (cheap at peak ROTCE; fair at trough ROTCE) explains HOLD/TRIM.

Key metrics (Q1 2026, Jan–Mar 2026):
  Revenue (net)       : $30.3B  (+7% YoY; beat $29.92B est)
  NII                 : $15.9B  (+9% YoY; beat $15.67B est; guidance raised +6-8%)
  EPS (diluted)       : $1.11   (+25% YoY; beat $1.01 est; "highest in almost 2 decades")
  Net income          : $8.6B   (+17% YoY)
  Trading revenue     : $8.5B+  (best quarter in 15 years; equities +30%)
  ROTCE               : {ROTCE:.0f}%    (medium-term target 16-18%)
  TBV per share       : ${TBV_PER_SHARE:.2f}  (P/TBV: {ptbv_current:.2f}×)""")

    print(f"""
EPP (Earnings Power Price) — structural floor
  = EPS_TROUGH × EPP_MIN_PE
  Stress EPS (${EPS_TROUGH:.2f}) × {EPP_MIN_PE}× floor.
  ${EPS_TROUGH:.2f}: NII -20% ($63B→$50B), credit provisions 2.5× ($12.5B vs $5B),
  markets -15%. Pre-tax impact ~-$19B → net income ~$17B → EPS ~$2.27 → $2.00.
  Calibration: BAC FY2020 GAAP EPS $2.32 (COVID reserve builds $11B).
  $2.00 represents slightly more stress than COVID — appropriate GFC-style floor.
  The {EPP_MIN_PE}× P/E premium over generic bank trough (8×) reflects BAC's improved
  CET1 ({CET1_RATIO:.1f}% vs ~10% pre-GFC) and diversified revenue base.
  EPP = ${EPP:.2f}. (BAC March 2020 low: ~$18.10 — exactly this EPP level.)
  Calibration: 52-wk low ${PRICE_52W_LOW:.2f} ÷ $2.00 = {PRICE_52W_LOW/EPS_TROUGH:.1f}× stress EPS.
  The worst trading day of 2025-2026 was still {PRICE_52W_LOW/EPS_TROUGH:.1f}× above the catastrophe scenario.

Method B — 2-year normalised upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E ~${CONS_EPS_2YR:.2f} (FY2026E ${EPS_NOW:.2f} × 1.20; NII +6-8% + IB + buybacks)
  × {CONS_EXIT_PE}× exit P/E (current 12.9×; 14× achievable if ROTCE sustains 16-18%
  as per management medium-term guidance; below JPM's current 13.7× multiple,
  appropriately reflecting lower ROTCE 16% vs JPM 23%).
  = ${price_b:.2f}.
  Ratio B = (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f}) = ${CURRENT_PRICE-EPP:.2f} / ${price_b-CURRENT_PRICE:.2f} = {ratio_b:.2f}×
  → {signal}. BAC is running a fundamentally better bank but is not cheap.
  Method B upside: +{(price_b/CURRENT_PRICE-1)*100:.1f}% to ${price_b:.0f}. Downside to EPP: -{(1-EPP/CURRENT_PRICE)*100:.1f}%.
  The 52-wk low ${PRICE_52W_LOW:.2f} was the ACCUMULATE entry (ratio_b ~0.90×).
  Buffett sold at ~$35-45 range — his internal "fair value" was clearly below $50-55.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

    print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BANK OF AMERICA: A BETTER BANK — BUT BUFFETT ALREADY LEFT
==========================================================

Bank of America is the second-largest US bank by assets ($3.3T) and the
largest US consumer bank by deposit market share. Under CEO Brian Moynihan
(since 2010), BAC has been transformed from one of the most troubled large
banks post-GFC into a genuinely well-run financial institution:

  FY2022 → FY2025 EPS CAGR: ~6.1% (NII expansion + credit quality + buybacks)
  ROTCE trajectory: 9% (2020) → 11% (2022) → 14% (2024) → 16% (Q1 2026 ann.)
  NII growth: from $44B trough (2023) → $63B annualised (Q1 2026)
  Consumer digital: #1 in US mobile banking users (58M+ active); Zelle dominant

The fundamental trajectory is clearly positive. Yet one investor's actions
speak louder than any analyst note:

THE BUFFETT EXIT — THE DEFINING SIGNAL FOR BAC IN 2026
=======================================================
Warren Buffett's Berkshire Hathaway sold approximately 1 billion Bank of America
shares between mid-2024 and early 2025, liquidating the entire position that
Buffett had built over 13 years. Key context:

Timeline:
  2011: Buffett invested $5B in BAC preferred shares + warrants at ~$6-7/share
        equivalent during the post-GFC crisis (a textbook contrarian BUY)
  2017: Converted warrants to ~700M common shares
  2024-25: Systematically sold ~1B shares at $35-45 range
  2025: Zero BAC shares remaining in Berkshire portfolio

What this means:
  Buffett's exit at $35-45 is his revealed "fair value" upper bound for BAC.
  He would not sell a position he believed was worth materially more. At $51.70,
  BAC is +15-48% above Buffett's exit price. This is not a bearish call on the
  business — it simply means the easy money is made.

Counter-argument: Berkshire may have sold for capital allocation reasons
  (deploying into BRK buybacks or other positions, given his $397B cash pile),
  not purely because BAC was fully valued. This is a valid point. But Buffett
  does NOT sell franchise-quality businesses just for capital — he sold because
  the price was right.

Our assessment: Buffett's exit is a significant weight in the HOLD/TRIM
conclusion. It is one of the model's largest SCA negative factors (-0.40 × 0.25).

Q1 2026 — RECORD EPS; NII GUIDANCE RAISED
==========================================
  Revenue:       $30.3B   (+7% YoY; beat estimate $29.92B)
  NII:           $15.9B   (+9% YoY; beat $15.67B; annualised $63.6B)
  Adj EPS:       $1.11    (+25% YoY; beat $1.01; highest in "almost two decades")
  Net income:    $8.6B    (+17%)
  Trading:       Best quarter in 15 years
    Equities:    $2.83B   (+30% YoY) — record performance
    FICC:        $5.7B    (+8% YoY)
  ROTCE:         16.0%    (medium-term target 16-18%)
  TBV/share:     $28.98

The quarter was genuinely strong across all segments. Notably, CEO Moynihan
said consumer banking is "healthy" — consumer spending +6% YoY, delinquencies
stable, no signs of consumer credit deterioration. This is important context
given the macro uncertainty Dimon (JPM) highlighted.

NII guidance raised to +6-8% for FY2026 (from prior guidance of +5-7%).
Full year FY2026 NII now expected at ~$61-62B. This is the key positive
lever — NII bottomed in FY2023 at ~$44B and has been in a multi-year recovery.

THE NII FRANCHISE — THE BIGGEST LEVER AND BIGGEST RISK
=======================================================
Bank of America has the most interest-rate-sensitive balance sheet among the
major US banks. With $2T+ in deposits (largely current/savings accounts),
BAC earns meaningfully higher NII when rates are elevated:

  2022-2023: Fed raised rates to 5.25-5.50%; BAC NII benefited enormously
  2024: Fed started cutting; BAC NII began declining (drove stock to $24 lows)
  2025-2026: Rates stabilised; BAC NII recovering; now $63B annualised

Rate sensitivity (estimated):
  Each 25bps Fed rate cut → ~$1.0-1.5B annual NII reduction
  Market pricing 2 more cuts in 2026 → potential -$2-3B NII impact
  FY2027E NII at risk: could compress to $58-60B if full cut cycle resumes

This rate sensitivity is a double-edged sword:
  BULL: If Fed keeps rates higher-for-longer, BAC NII accelerates → EPS beats
  BEAR: If recession drives aggressive cuts (Fed to 2.5-3%), NII falls $10-15B
  → this is THE single biggest variable in the BAC investment thesis

BAC vs JPM — THE QUALITY DISCOUNT
===================================
The natural comparison is JPMorgan (JPM), covered in this framework:

                BAC         JPM
  ROTCE         16%         23%      ← JPM 7pts higher
  P/TBV         1.78×       2.83×    ← BAC much cheaper
  CET1          ~12%        14.3%    ← JPM better capitalised
  NII/Revenue   ~52%        ~51%     ← similar NII dependence
  Market cap    ~$368B      ~$824B
  P/E fwd       12.9×       13.7×    ← BAC slightly cheaper

Gordon Growth at current ROTCE:
  BAC warranted P/TBV: (16%-4%)/(9%-4%) = 2.4× → implied $69.55
  JPM warranted P/TBV: (23%-4%)/(9%-4%) = 3.8× → implied $414

BAC LOOKS cheap vs Gordon Growth warranted price ($69 vs $51.70). BUT:
The market is correctly discounting the risk that BAC's 16% ROTCE is
cyclical peak (achievable only in a benign credit + high-rate environment).
If ROTCE reverts to 12% in a recession, warranted P/TBV = 1.6× = $46.37.

BAC's ROTCE improvement from 9% (2020) to 16% (2026) is real and structural:
  - Technology investment ($3.5B/yr): AI-powered risk management, auto loan
    underwriting, fraud detection driving cost efficiency
  - Expense discipline: efficiency ratio improved from 70%+ to ~65%
  - Revenue diversification: GWM ($3.5T AUM), Global Markets, transaction banking

But part of the ROTCE improvement is cyclical (high-rate NII):
  - At 3% Fed Funds: BAC ROTCE probably 13-14%, not 16%
  - At 5%+ Fed Funds: BAC ROTCE could reach 18% (top of guidance range)

ENTRY/EXIT FRAMEWORK
====================
  ◉ BUY        : $26-32  (1.4-1.7× EPP; post-GFC style entry)
  ◎ ACCUMULATE : $38-47  (2.1-2.6× EPP; 52-wk low territory; Buffett's sale range)
  ◐ WATCHLIST  : $47-51  (approaching post-Buffett-exit fair value)
  ▷ HOLD/TRIM  : $51-58  (current; above Buffett exit price; fair-to-full value)
  ✕ TRIM HARD  : >$58    (above ATH; Method B territory; trim hard)

The 52-wk low of $42.35 was the ACCUMULATE zone (ratio_b ~0.90×). BAC has
recovered +22% from that low. The easy money (below $47-48) is made.
Current $51.70 represents HOLD — a quality bank at a fair price.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

    print("PART 3 — NUMBERS & SIGNALS")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    pct_from_low  = (CURRENT_PRICE - PRICE_52W_LOW)  / PRICE_52W_LOW  * 100
    pct_from_high = (CURRENT_PRICE - PRICE_52W_HIGH) / PRICE_52W_HIGH * 100
    mktcap_b      = CURRENT_PRICE * SHARES_M / 1000

    print(f"""
  I. PRICE & VALUATION SNAPSHOT
  ----------------------------------------------------------------------
  Current price   : ${CURRENT_PRICE:.2f}  (52-wk range: ${PRICE_52W_LOW:.2f}–${PRICE_52W_HIGH:.2f})
  vs 52-wk low    : +{pct_from_low:.1f}%   |   vs 52-wk high: {pct_from_high:.1f}%
  Market cap      : ~${mktcap_b:.0f}B   |   Shares (B-eq): ~{SHARES_M/1000:.2f}B
  Dividend (ann)  : ${DIVIDEND_ANN:.2f}   |   Yield: {DIVIDEND_ANN/CURRENT_PRICE*100:.2f}%
  TBV per share   : ${TBV_PER_SHARE:.2f}  |   P/TBV: {ptbv_current:.2f}×
  ROTCE (Q1 2026) : {ROTCE:.1f}%     |   CET1 ratio: ~{CET1_RATIO:.1f}%
  Forward P/E     : {CURRENT_PRICE/EPS_NOW:.1f}×  (on FY2026E ${EPS_NOW:.2f})
  Gordon Growth   : warranted P/TBV {ptbv_warranted:.1f}× → ${ptbv_implied:.2f}  |  stress P/TBV {ptbv_stress:.1f}× → ${price_ptbv_stress:.2f}
  Buffett exit    : ~$35-45/share (2024-2025); current ${CURRENT_PRICE:.2f} is +{(CURRENT_PRICE/42-1)*100:.0f}% above exit""")

    print(f"""
  II. EPS HISTORY (GAAP diluted)
  ----------------------------------------------------------------------
  FY2022  : ${EPS_FY2022:.2f}  (NII expansion beginning; reserve releases; AOCI issues)
  FY2023  : ${EPS_FY2023:.2f}  (NII peaked mid-year then declined; AOCI $100B+ unrealised loss)
  FY2024  : ${EPS_FY2024:.2f}  (+3.6%; NII trough; trading/fees partially offset)
  FY2025  : ${EPS_FY2025:.2f}  (+18.7%; NII recovery underway; ROTCE ~14%)
  FY2026E : ${EPS_NOW:.2f}  (Q1 actual $1.11 +25% YoY; NII guidance raised +6-8%)
  FY2027E : ${CONS_EPS_2YR:.2f}  (used for Method B; +20% growth; NII + IB + buybacks)
  Q1 2026 : $1.11  (beat $1.01; +25% YoY; "highest EPS in almost two decades")

  III. EPP & METHOD B
  ----------------------------------------------------------------------
  EPS_TROUGH  : ${EPS_TROUGH:.2f}/share  (NII -20%; credit costs 2.5×; GFC-style; ≈ FY2020 $2.32)
  EPP_MIN_PE  : {EPP_MIN_PE}×          (large bank trough; above 8× floor for CET1 quality premium)
  EPP (floor) : ${EPP:.2f}       (= ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×; matches BAC March 2020 low ~$18.10)
  EPP gap     : +{epp_gap_pct:.1f}%   (current price is {epp_gap_pct/100:.1f}× above EPP floor)

  CONS_EPS_2YR: ${CONS_EPS_2YR:.2f}/share  (FY2027E; +{CONS_EPS_2YR/EPS_NOW*100-100:.0f}% from FY2026E; NII + IB + buybacks)
  CONS_EXIT_PE: {CONS_EXIT_PE}×          (current 12.9×; 14× achievable if ROTCE holds 16-18%)
  Method B    : ${price_b:.2f}       (= ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×; ~analyst avg PT $62.98)
  Upside to B : +{(price_b/CURRENT_PRICE-1)*100:.1f}%
  Downside EPP: -{(1-EPP/CURRENT_PRICE)*100:.1f}%

  ┌─────────────────────────────────────────────────────────────────────┐
  │  RATIO B = ({CURRENT_PRICE:.2f} − {EPP:.2f}) / ({price_b:.2f} − {CURRENT_PRICE:.2f})                │
  │           = {CURRENT_PRICE-EPP:.2f} / {price_b-CURRENT_PRICE:.2f} = {ratio_b:.2f}×                               │
  │  SIGNAL   = {signal:<35}              │
  └─────────────────────────────────────────────────────────────────────┘""")

    print(f"""
  IV. STOCK-SPECIFIC COMPOSITE ADJUSTMENT (SCA)
  ----------------------------------------------------------------------
  {'Factor':<52}  {'Score':>6}  {'Wt':>6}  {'Contrib':>7}""")
    print(f"  {'─'*52}  {'──────'}  {'──────'}  {'───────'}")
    for desc, score, weight in SCA_FACTORS:
        contrib = score * weight
        print(f"  {desc[:52]:<52}  {score:>+6.2f}  {weight:>6.2f}  {contrib:>+7.3f}")
    print(f"  {'─'*52}  {'──────'}  {'──────'}  {'───────'}")
    print(f"  {'SCA raw':<52}  {'':>6}  {'':>6}  {sca_raw:>+7.3f}")
    print(f"  {'SCA adj (÷2.0)':<52}  {'':>6}  {'':>6}  {sca_adj:>+7.3f}")

    print(f"""
  V. COMPOSITE INFERENCE
  ----------------------------------------------------------------------
  Market composite  : {market_composite:.3f}  (BASE)
  Adj composite     : {adj_composite:.3f}  (BASE)
  Softmax weights at adj composite ({adj_composite:.3f}):
    BEAR  : {W['BEAR']*100:.1f}%  (${PRICE_BEAR})
    BASE  : {W['BASE']*100:.1f}%  (${PRICE_BASE})
    BULL  : {W['BULL']*100:.1f}%  (${PRICE_BULL})
    XBULL : {W['XBULL']*100:.1f}%  (${PRICE_XBULL})
  Expected price (adj): ${exp_p:.1f}  vs current ${CURRENT_PRICE:.2f}  (Δ {(exp_p/CURRENT_PRICE-1)*100:+.1f}%)

  VI. SCENARIOS SUMMARY
  ----------------------------------------------------------------------
  BEAR  (${PRICE_BEAR}) : GFC-style recession. NII -20% ($63B→$50B); credit provisions
               2.5× ($12.5B); equities/IB revenue -30%. ROTCE collapses to 5-6%.
               EPS $2.00 × 9× = $18. BAC March 2020 low was $18.10 — this is the
               precedent. CET1 {CET1_RATIO:.1f}% means BAC SURVIVES without dilution.
               -{(1-PRICE_BEAR/CURRENT_PRICE)*100:.0f}% from current.

  BASE  (${PRICE_BASE}) : Soft landing. NII grows to ~$65B (FY2027); IB fees $3B+/qtr;
               credit benign; ROTCE 16-17%; buybacks $4-5B/yr.
               FY2027E $4.80 × 12.1× = ${PRICE_BASE:.0f}. No multiple re-rating — just
               EPS compounding. Near prior ATH ${PRICE_52W_HIGH:.2f}.
               +{(PRICE_BASE/CURRENT_PRICE-1)*100:.0f}% from current.

  BULL  (${PRICE_BULL}) : = price_b. ROTCE hits 17-18% (top of guidance); deregulation
               tailwinds (lighter capital rules); NII holds above $65B; multiple
               re-rates to 14× as ROTCE gap vs JPM narrows. FY2027E $4.80 × 14×.
               +{(PRICE_BULL/CURRENT_PRICE-1)*100:.0f}% from current.

  XBULL (${PRICE_XBULL}) : Full franchise re-rating. ROTCE hits 18-20% on AI-driven cost
               efficiency + NII recovery + deregulation. BAC closes the P/TBV
               gap with JPM. FY2028E ~$6 × 15× = $90. Buffett proved wrong for
               selling early. Merrill Lynch wealth management becomes #1 US WM.
               +{(PRICE_XBULL/CURRENT_PRICE-1)*100:.0f}% from current.
""")

    print("=" * 72)
    print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-26")
    print("=" * 72)
