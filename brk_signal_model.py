"""
Berkshire Hathaway Inc. Class B (NYSE: BRK.B) — BottomUp Risk/Reward Signal Model

SIGNAL:  ◎ ACCUMULATE
RATIO B: 1.09x  (Method B at 26× FY2027E $24.00/B = $624.00; ratio 149.95/138.05 = 1.09×)
DATE:    2026-05-26

NOTE: All per-share figures are per BRK.B share. BRK.B = 1/1,500th of BRK.A
economically. "EPS" = operating earnings per B-equivalent share (the metric
Buffett and Abel use; excludes unrealized investment gains/losses which are
non-operational). Book value per B = $337.15 (Q1 2026 end; 1/1500 of BRK.A
book $505,723). Cash per B = ~$184 ($397B total / ~2,157M B-equivalent shares).
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "BRK"
COMPANY = "Berkshire Hathaway Inc. (BRK.B — Class B)"
SECTOR  = "Diversified Conglomerate · Insurance (GEICO/BH Re) · Railroad (BNSF) · Utilities (BHE) · Equity Portfolio"

# ── Price (BRK.B) ──────────────────────────────────────────────────────────────
CURRENT_PRICE  = 485.95   # BRK.B — Yahoo Finance, 2026-05-26; 1/1500 of BRK.A; $1.05T market cap
PRICE_52W_LOW  = 455.19   # 52-week low (early 2026; transition anxiety post-Buffett retirement)
PRICE_52W_HIGH = 516.85   # 52-week high (late 2025; record operating earnings + cash accumulation)
SHARES_M       = 2157.0   # ~2,157M B-equivalent shares (~1.438M A equiv × 1,500 per A)
DIVIDEND_ANN   =   0.00   # BRK pays no dividend; Buffett's 60-year policy; Abel continuation expected

# ── Operating EPS per BRK.B (non-GAAP; excl. unrealized investment gains/losses) ─
# Berkshire's board and management define success by OPERATING earnings growth,
# NOT net income (which swings wildly with unrealized equity gains/losses on
# the $318B stock portfolio). Operating earnings = insurance underwriting +
# investment income + railroad + utilities + other businesses.
# Per-B calculation: operating earnings / (equiv A shares × 1,500)
# FY2026 Q1 operating earnings $11.35B / 1.438M A equiv / 1,500 = $5.26/B × 4 = ~$21.05/B ann.
EPS_FY2022 = 13.20    # ~$28.7B operating / 1.450M A equiv / 1500; insurance + BNSF strong
EPS_FY2023 = 17.25    # ~$37.4B operating / 1.445M A equiv / 1500; GEICO turnaround gains momentum
EPS_FY2024 = 21.73    # ~$47.4B operating / 1.450M A equiv / 1500; record year; GEICO fully fixed
EPS_FY2025 = 18.61    # ~$40.2B operating / 1.444M A equiv / 1500; "lower than 2024" (per annual report)
                       # Note: FY2025 net income much higher due to unrealized equity portfolio gains
                       # Insurance combined ratio 87.1% (excellent); BNSF $4.4B div to BRK
EPS_NOW    = 21.05    # FY2026E ($11.35B Q1 × 4 = $45.4B ann. / 1.438M / 1500; +18% vs Q1 2025)
                       # Q1 2026: Greg Abel's first quarter; operating earnings +18% YoY; missed $11.56B est
                       # Cash/T-bills: $397B (record); up from $373B at year-end 2025

# ── EPP Floor ─────────────────────────────────────────────────────────────────
# EPS_TROUGH = simultaneous mega-catastrophe losses (insurance) + BNSF freight
# recession (rail volumes -15%+) + BHE utility write-downs (stranded asset risk
# from energy transition lawsuits) + equity portfolio impaired in crash.
# From FY2026E $21.05: ~-43% haircut to $12.00/B.
# CRITICAL DISTINCTION from typical pharma/tech EPP: Berkshire's $397B cash
# position and $176B insurance float provide an extraordinary balance sheet
# floor. Even in a catastrophic year, BRK carries more liquid assets (~$573B
# combined cash + float) than almost any entity on earth. This justifies a
# HIGHER EPP_MIN_PE than typical companies in distress.
# EPP_MIN_PE = 28: even at trough earnings, Berkshire's fortress balance sheet
# ($397B cash = $184/B; book value $337/B) means the market never lets it
# trade at deep value distressed multiples. Buffett demonstrated this — he
# would begin buybacks below 1.2× book (~$404/B at current book) as a floor.
# EPP = $336.00.
# Calibration: 52-wk low $455.19 ÷ $12.00 = 37.9× stress EPS — the market
# has NEVER approached EPP for BRK. The 52-wk low ($455) was already +35%
# above EPP ($336). This is consistent with Berkshire's historical minimum
# of ~1.1-1.2× book value in any significant drawdown.
# Cash floor context: $397B cash / 2,157M B equiv = $184/B in cash alone.
# Ex-cash EPP = $336 - $184 = $152 on $12 trough = 12.7× — reasonable for
# the underlying operating businesses without the cash treasure chest.
EPS_TROUGH = 12.00    # Mega-CAT losses + BNSF recession + BHE write-downs; still floored by cash
EPP_MIN_PE = 28       # Cash fortress + float + diversification; Buffett buyback floor ~1.2× book
EPP        = EPS_TROUGH * EPP_MIN_PE   # $12.00 × 28 = $336.00

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E ~$24.00/B ($52B operating earnings / 1.44M A / 1500):
# Abel's agenda for 2026-2027 operating earnings improvement:
#   • GEICO: turnaround largely complete by FY2024 (combined ratio <90%). In
#     2025-2026, GEICO grows market share again with improved pricing discipline.
#     GEICO is now competitive vs Progressive/State Farm after the 2021-2023
#     loss-ratio crisis. Expected contribution: $4-5B/yr by 2027.
#   • BNSF: rail volumes stabilising as US industrial production normalises;
#     coal replacement with intermodal/bulk. BNSF pricing power (oligopoly with
#     UP) maintains 60%+ operating ratio discipline. $4-5B/yr dividend to BRK.
#   • BHE (Berkshire Hathaway Energy): regulated utilities in Iowa, Nevada,
#     California, UK, etc. Stable returns but BHE faces wildfire liability
#     litigation in CA/NV (inherited from PacifiCorp). This is a known risk but
#     manageable (similar to PG&E's 2018-2019 scenario; BHE has $10B+ net worth).
#     Annual contribution: $3-4B/yr to BRK.
#   • Cash deployment ($397B): Abel's most important decision. At T-bill rates
#     (~4-5%), $397B generates ~$16-20B in annual interest income. If deployed
#     into acquisitions or equity investments, this converts to operating
#     income — potentially adding $2-5B/yr in operating earnings depending
#     on the target quality and price paid. Every $100B deployed at 10% ROIC
#     adds ~$1.5B/yr to operating earnings (after tax, after cost of cash).
#   • Equity portfolio income: dividends from Apple, BAC, Coca-Cola, AXP etc.
#     ~$6-8B/yr in dividend income included in investment income.
#   • FY2027E: $52B operating earnings / 1.44M / 1500 = $24.07/B ≈ $24.00.
# Exit P/E: 26× — Berkshire historically trades at 1.3-1.5× book value.
# Book value in 2027 projected at ~$380/B (assuming ~12% growth from current
# $337). At 26× operating EPS of $24 = $624 ≈ 1.64× $380 book — slightly
# above historical premium, justified if Abel demonstrates capital deployment
# capability. Conservative if Abel finds a transformative acquisition.
#   At 26×: $624.00  (+28% from $485.95) — conservative; ratio_b = 1.09×
#   At 30×: $720.00  (+48%) — "elephant" acquisition catalyst
#   At 32×: $768.00  (+58%) — dividend initiation + multiple re-rate
CONS_EPS_2YR = 24.00
CONS_EXIT_PE = 26

# ── Computed signals ──────────────────────────────────────────────────────────
price_b = CONS_EPS_2YR * CONS_EXIT_PE

if price_b <= CURRENT_PRICE:
    ratio_b     = None
    ratio_b_fmt = "N/A"
    signal_primary = "✕ AVOID"
else:
    ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
    if   ratio_b < 0:    signal_primary = "◉ BUY"
    elif ratio_b < 0.75: signal_primary = "◉ BUY"
    elif ratio_b < 1.1:  signal_primary = "◎ ACCUMULATE"
    elif ratio_b < 1.75: signal_primary = "◐ WATCHLIST"
    elif ratio_b < 2.5:  signal_primary = "▷ HOLD/TRIM"
    else:                signal_primary = "✕ AVOID"
    ratio_b_fmt = f"{ratio_b:.2f}x"

epp_gap_pct = (CURRENT_PRICE - EPP) / EPP * 100

# ── Scenario prices ───────────────────────────────────────────────────────────
# BEAR:  BHE wildfire litigation results in $20-30B settlement (like PG&E);
#        BNSF suffers freight recession (-15% volume) as US manufacturing
#        contracts; insurance mega-catastrophe losses >$20B in a single year
#        (Pacific earthquake or multi-hurricane season); equity portfolio falls
#        30%+ (GAAP loss massive; operating earnings hit via lower div income).
#        Abel makes a large acquisition at poor terms (overpays for a $100B+
#        company). Operating EPS trough ~$12; 28× EPP = $336. -31%.
# BASE:  Abel continues current playbook — modest acquisitions ($10-30B range);
#        GEICO continues market share gains; BNSF stable; BHE wildfire settled
#        for <$10B (manageable); interest income from $397B cash contributes.
#        Operating EPS grows to $24 by 2027; multiple stays at 24×. $576. +19%.
# BULL:  Abel announces first dividend ($3-5/B share = ~$6.5-10B/yr) — this
#        alone triggers a major multiple expansion as income investors re-rate.
#        OR: "elephant" acquisition ($100-200B deal) at attractive terms creates
#        $3-5B in incremental annual operating earnings. Multiple to 28×.
#        $24 × 28× = $672. +38%.
# XBULL: Abel deploys $200B+ in 2026-2027 into a transformative deal (financial
#        services, infrastructure, or energy) AND initiates dividend; BRK re-rates
#        to 30-32× on "the next chapter" narrative; book value compounds at
#        15%/yr through Abel's capital allocation. FY2028-29E ~$30/B × 28× =
#        $840. +73%.
PRICE_BEAR  = 336
PRICE_BASE  = 576
PRICE_BULL  = 672
PRICE_XBULL = 840

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.40, 0.25, "$397B cash: record dry powder for 'elephant hunt'; T-bill income $16-20B/yr"),
    (+0.35, 0.20, "Insurance float $176B at 87.1% combined ratio; GEICO fully turned around"),
    (+0.25, 0.15, "Operating diversification: BNSF + BHE + 50+ subsidiaries; recession-resilient"),
    (-0.20, 0.25, "Greg Abel transition: first year; deployment track record unproven at Buffett scale"),
    (-0.15, 0.15, "No dividend + slow buybacks: $397B cash earning T-bill rates, not compounding at 15%"),
]
sca_raw = sum(s * w for s, w, _ in SCA_FACTORS)
sca_adj = sca_raw / 2.0

# ── Composite inference ───────────────────────────────────────────────────────
CENTRES = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
T       = 0.60

def _logit(c, x): return -((x - c) ** 2) / T
def softmax_weights(composite):
    raw = {k: math.exp(_logit(v, composite)) for k, v in CENTRES.items()}
    tot = sum(raw.values())
    return {k: v / tot for k, v in raw.items()}

def expected_price(composite):
    w = softmax_weights(composite)
    prices = {"BEAR": PRICE_BEAR, "BASE": PRICE_BASE,
              "BULL": PRICE_BULL, "XBULL": PRICE_XBULL}
    return sum(w[k] * prices[k] for k in prices)

def infer_composite(target_price, lo=1.0, hi=4.0, iters=60):
    for _ in range(iters):
        mid = (lo + hi) / 2
        if expected_price(mid) < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

market_composite = infer_composite(CURRENT_PRICE)
adj_composite    = market_composite + sca_adj

def composite_label(c):
    if   c < 1.625: return "BEAR"
    elif c < 2.375: return "BASE"
    elif c < 3.25:  return "BULL"
    else:           return "XBULL"

market_label = composite_label(market_composite)
adj_label    = composite_label(adj_composite)

# ── Derived metrics ───────────────────────────────────────────────────────────
BOOK_PER_B   = 337.15   # Q1 2026 end; $505,723 per A / 1500
CASH_PER_B   = 184.05   # $397B / 2,157M B-equiv shares
FLOAT_TOTAL  = 176.0    # $176B insurance float (year-end 2025)
PRICE_TO_BOOK = CURRENT_PRICE / BOOK_PER_B

# ══════════════════════════════════════════════════════════════════════════════
print("=" * 72)
print(f"  {TICKER}  —  {COMPANY}")
print(f"  {SECTOR}")
print("=" * 72)

print(f"""
PART 1 — FRAMEWORK OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Special context: All per-share figures are per BRK.B. BRK.B is 1/1,500th
of BRK.A economically. "EPS" = OPERATING earnings per B-equivalent share
(Berkshire's preferred metric; excludes unrealized portfolio gains/losses).
  Book value per B  : ${BOOK_PER_B:.2f}  (Q1 2026; BRK.A $505,723 / 1,500)
  Cash per B        : ${CASH_PER_B:.2f}  ($397B cash + T-bills / ~2,157M B-equiv)
  Float (insurance) : ${FLOAT_TOTAL:.0f}B  (at 87.1% combined ratio; effectively free money)
  Price-to-book     : {PRICE_TO_BOOK:.2f}×  (current; Buffett buyback floor ~1.2× book ≈ $404/B)

EPP (Earnings Power Price) — structural floor
  = EPS_TROUGH × EPP_MIN_PE
  Stress EPS ($12.00/B) × 28× floor. EPS_TROUGH represents mega-CAT losses
  + BNSF freight recession + BHE wildfire settlements — a ~-43% operating
  EPS cut. The 28× floor P/E is HIGHER than typical companies because:
  (1) $397B cash = $184/B in liquid assets that anchor intrinsic value;
  (2) $176B insurance float = essentially free leverage; (3) book value
  per B ($337) provides a hard floor (Buffett/Abel would buy stock below
  1.2× book ≈ $404); (4) 50+ businesses across uncorrelated industries.
  EPP = $336.00.
  Calibration: 52-wk low $455.19 ÷ $12.00 = 37.9× stress EPS — BRK.B
  has NEVER traded near its EPP floor. Even the "low" was 37.9× stress
  EPS and 1.35× book, confirming the cash fortress sets a structural floor
  well above the theoretical EPP level.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E ~$24.00/B (~$52B operating earnings; +15% from FY2026E) × 26×
  exit P/E (in-line with Berkshire's historical 1.3-1.5× book multiple
  at 2027 projected book of ~$380/B: 26 × $24 ≈ $624 = 1.64× $380 book —
  a modest premium justified if Abel demonstrates deployment capability)
  = $624.00.
  Ratio B = ($485.95 − $336.00) / ($624.00 − $485.95) = $149.95 / $138.05 = 1.09×
  → ◎ ACCUMULATE. BRK.B is a rare quality compounder at an attractive entry
  — not quite the screaming buy that Berkshire represents below $404/B
  (1.2× book), but comfortably in the ACCUMULATE zone. The $397B cash
  ($184/B) represents enormous optionality that the operating EPS metric
  alone does not capture. If Abel deploys that cash at 10-12% ROIC in the
  next 24 months, price_b could be $700-800.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BERKSHIRE HATHAWAY: THE $397B QUESTION — WHAT WILL GREG ABEL DO?
=================================================================

Berkshire Hathaway is the world's largest diversified conglomerate by market
capitalisation (~$1.05T) and arguably the most resilient enterprise structure
ever built. At its core: a property & casualty insurance empire (GEICO,
BH Reinsurance, General Re, BHRG) that generates $176B in float — the
largest pool of essentially cost-free capital in private sector history —
which is then invested by the best capital allocator of the 20th century,
Warren Buffett, now succeeded by Greg Abel.

The defining fact of Berkshire in May 2026: $397 BILLION in cash and
T-bills — a number so large it is difficult to comprehend. This represents:
  • ~38% of Berkshire's $1.05T market cap is held in cash
  • ~$184 per BRK.B share in liquid assets
  • ~$278,000 per BRK.A share equivalent
  • The world's largest corporate cash position by a factor of 2-3×

This cash pile is the defining investment question for the next 5 years.
Buffett accumulated it because he found nothing worth buying at his required
returns. Greg Abel, who took over as CEO on January 1, 2026, now must
decide: deploy it at scale, initiate a dividend, or continue accumulating
until the right opportunity arrives.

Q1 2026 — ABEL'S FIRST QUARTER; OPERATING EARNINGS +18%
=========================================================
  Operating earnings:     $11.35B  (+18% YoY from $9.64B Q1 2025; MISSED $11.56B est)
  Net income:             ~$10.1B  (2× prior year; unrealized equity portfolio gains)
  Book value per A share: $505,723  (+11.1% YoY; per B = $337.15)
  Cash + T-bills:         $397B  (record; up from $373B at year-end 2025)
  Insurance float:        ~$176B  (generating ~$8-9B/yr in investment income alone)
  Combined ratio (FY2025): 87.1%  (exceptional; 12.9 pts of underwriting profit)

The Q1 miss vs. expectations was modest ($11.35B vs $11.56B) and reflects
BNSF freight volume weakness and some insurance seasonality. The +18% YoY
growth confirms the underlying business momentum from GEICO's turnaround.

THE FOUR PILLARS OF BERKSHIRE'S VALUE
=======================================

1. INSURANCE — THE COMPOUNDING ENGINE
   Berkshire's insurance operations are the core of its unique structure.
   The "float" concept is Buffett's genius: policyholders pay premiums
   upfront; Berkshire invests those funds until claims are paid. If insurance
   is written at an underwriting profit (combined ratio <100%), the float
   is essentially free leverage on Berkshire's investment portfolio.

   GEICO (15th largest auto insurer in the US):
     2021-2023: severe losses (combined ratio >110%; inflation hit auto claims
     faster than GEICO could raise rates; market share lost to Progressive).
     2024-2025: turnaround complete. GEICO's combined ratio dropped below 90%
     as rate increases caught up with claims inflation. GEICO is now growing
     market share again. Under Todd Combs (GEICO CEO), underwriting discipline
     has been restored.

   Berkshire Hathaway Reinsurance Group / General Re:
     The reinsurance operations are the most sophisticated in the world.
     BH Re and Gen Re write global property & casualty, life, and specialty
     reinsurance. The 2025 combined ratio of 87.1% across all BRK insurance
     reflects exceptional underwriting across a hard pricing cycle (post-
     COVID-19 liability + inflation + CAT losses forcing industry-wide rate
     increases). BRK is taking LESS business when it finds rates inadequate
     ("expects to write less P&C business for a period of time").

   Float ($176B at 87.1% combined ratio):
     Investment income on float: ~$8-9B/yr at 5% T-bill rates.
     This income alone = ~$5.26/B per year — funding ~25% of operating EPS
     from "free" money. This is the moat that no competitor can replicate.

2. BNSF RAILWAY — THE FREIGHT BACKBONE
   BNSF is one of two Class I railroads serving the western US (with UP).
   Together, they constitute a duopoly with extraordinary pricing power.
     Revenue:  ~$23-24B/yr; operating ratio: ~62-63% (industry-leading)
     Cash flow: $8.1B operating cash flow in 2025; $4.4B dividend to BRK
     Volumes: coal replacement with intermodal + agriculture + bulk
     Moat: 32,500 miles of track; physical infrastructure impossible to replicate
     Risk: freight recession; coal volume secular decline; autonomous trucking
     (very long-term); regulatory pricing constraints

3. BERKSHIRE HATHAWAY ENERGY (BHE)
   BHE is a diversified energy infrastructure company: regulated utilities in
   Iowa (MidAmerican), Nevada (NV Energy), Pacific Northwest (PacifiCorp),
   and Western/Central US; UK and Australian assets; pipeline interests.

   Risk: PacifiCorp wildfire litigation in California/Oregon. Pacific Gas
   and Electric (PG&E) declared bankruptcy in 2019 after ~$30B in wildfire
   liability. PacifiCorp faces similar but smaller-scale liability from Oregon
   and California wildfires (2020-2022). BHE has set reserves but ultimate
   exposure is uncertain. This is the PRIMARY downside risk at BHE and the
   reason BRK stopped distributing BHE dividends to shareholders while
   litigation is resolved.

4. EQUITY PORTFOLIO ($318B) + SUBSIDIARY PORTFOLIO
   Berkshire's public equity holdings (~$318B) are concentrated:
     Apple:        ~45% of portfolio (~$142B); dividend: ~$1B/yr
     American Express: ~15% (~$47B); 21% of AXP common shares
     Bank of America: ~11% (~$35B); 12% of BAC common shares
     Coca-Cola:    ~7% (~$22B); 9.3% of KO; $0.84/share/yr dividend
     Chevron:      ~5% (~$16B)
     Others:       ~17%

   Dividend income from equity portfolio: ~$6-8B/yr.
   IMPORTANT: Buffett/Abel sell equities when they find better opportunities
   or need to raise cash. The portfolio is a dynamic allocation, not fixed.

THE GREG ABEL TRANSITION — WHAT CHANGES AND WHAT DOESN'T
=========================================================
  What CHANGES:
    • Abel makes all capital allocation decisions (acquisitions, investments)
    • Abel communicates differently from Buffett (more formal; less folksy)
    • Abel broke Buffett's 21-month streak of not buying back BRK stock in
      March 2026 — bought $1.3B+ in buybacks in Q1. Signals Abel is more
      willing to use the buyback tool when the stock trades below fair value.
    • Abel may be more inclined to initiate a dividend eventually (BRK at
      $1T market cap struggles to deploy $40-50B/yr in dividends meaningfully)

  What DOESN'T CHANGE:
    • The Berkshire collection of businesses (GEICO, BNSF, BHE, etc.)
    • The insurance-float-as-leverage model
    • The decentralised management philosophy
    • The "don't sell good businesses" principle
    • The long-term owner orientation

  Abel's key test: the "elephant" acquisition. Berkshire needs a $100-200B
  deal to move the needle on operating earnings given its $1T+ size. Abel
  has signalled willingness to act but has NOT rushed. The patient approach
  is right — deploying $397B at poor returns would destroy more value than
  sitting in T-bills at 4-5%.

VALUATION FRAMEWORK — THREE LENSES
=====================================
  1. Price-to-Book:     ${CURRENT_PRICE:.2f} / ${BOOK_PER_B:.2f} = {PRICE_TO_BOOK:.2f}×  (Buffett buy floor: 1.2× = ~$404/B; fair: 1.4-1.5×)
  2. Operating P/E:     ${CURRENT_PRICE:.2f} / ${EPS_NOW:.2f} = {CURRENT_PRICE/EPS_NOW:.1f}×   (appears expensive; adjusting for $184/B cash...)
  3. Ex-cash P/E:      ${CURRENT_PRICE - CASH_PER_B:.2f} / ${EPS_NOW:.2f} = {(CURRENT_PRICE - CASH_PER_B)/EPS_NOW:.1f}×  (the "real" earnings multiple on operating businesses)

  The ex-cash P/E of {(CURRENT_PRICE-CASH_PER_B)/EPS_NOW:.1f}× is the most useful metric for comparing BRK.B
  to peers. At {(CURRENT_PRICE-CASH_PER_B)/EPS_NOW:.1f}× ex-cash operating earnings, Berkshire is priced at a
  moderate premium to its quality — justified by the optionality embedded
  in the $397B cash ("what will Abel buy?") and the insurance float moat.

WHERE RISK/REWARD IS ATTRACTIVE
=================================
  STRONG BUY            : ≤$404   (1.2× book; Buffett's stated buyback floor; ratio_b ~0.5×)
  BUY                   : $404-440 (1.2-1.3× book; ratio_b ~0.6-0.85×)
  ACCUMULATE (current)  : $440-510 (1.3-1.5× book; ratio_b ~0.85-1.3×; fair value zone)
  WATCHLIST             : $510-560 (1.5-1.7× book; above historical average; ratio_b ~1.3-1.75×)
  TRIM above             : $560-624 (approaching Method B; book premium excessive without deal)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("PART 3 — NUMBERS & SIGNALS")
print("=" * 72)
print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │  SIGNAL:  {signal_primary:<12}  │  RATIO B: {ratio_b_fmt:<10}               │
  │  TICKER:  BRK.B         │  SECTOR:  Diversified Conglomerate    │
  └──────────────────────────────────────────────────────────────────┘

  ----------------------------------------------------------------------
""")

print(f"  Current price (BRK.B) : ${CURRENT_PRICE:.2f}  (52-wk: ${PRICE_52W_LOW}-${PRICE_52W_HIGH}; BRK.A equiv ~${CURRENT_PRICE*1500:,.0f})")
print(f"  Book value per B      : ${BOOK_PER_B:.2f}  (Q1 2026; P/B = {PRICE_TO_BOOK:.2f}×; Buffett floor 1.2× = ~$404)")
print(f"  Cash per B            : ${CASH_PER_B:.2f}  ($397B total; ex-cash price ${CURRENT_PRICE-CASH_PER_B:.2f}; ex-cash P/E {(CURRENT_PRICE-CASH_PER_B)/EPS_NOW:.1f}×)")
print(f"  EPP floor             : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above; 28× × ${EPS_TROUGH} stress EPS; 52-wk low = 37.9× stress EPS)")
print(f"  Method B (26× exit)   : ${price_b:.2f}  (+{(price_b/CURRENT_PRICE-1)*100:.1f}%; ratio_b = {ratio_b:.2f}× → ACCUMULATE)")
print(f"  At 30× exit           : ${CONS_EPS_2YR*30:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*30-CURRENT_PRICE):.2f}× → ACCUMULATE (elephant deal catalyst)")
print(f"  At 32× exit           : ${CONS_EPS_2YR*32:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*32-CURRENT_PRICE):.2f}× → BUY (dividend + deal re-rate)")
print(f"  BEAR scenario         : ${PRICE_BEAR}   (-31%; BHE wildfire + BNSF recession + mega-CAT; at EPP = 28× $12 trough)")
print(f"  BASE scenario         : ${PRICE_BASE}   (+19%; Abel deploys modestly; GEICO grows; BNSF stable; $24 × 24×)")
print(f"  BULL scenario         : ${PRICE_BULL}   (+38%; 'elephant' acquisition OR dividend initiation; $24 × 28×)")
print(f"  XBULL scenario        : ${PRICE_XBULL}   (+73%; transformative deal + dividend; FY2028-29E ~$30/B × 28×)")
print(f"  Operating P/E (FY2026E): {CURRENT_PRICE/EPS_NOW:.1f}×  (${CURRENT_PRICE} / ${EPS_NOW}; incl. cash; ex-cash {(CURRENT_PRICE-CASH_PER_B)/EPS_NOW:.1f}×)")
print(f"  Operating P/E (FY2027E): {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (${CURRENT_PRICE} / ${CONS_EPS_2YR}; 26× exit; ex-cash {(CURRENT_PRICE-CASH_PER_B)/CONS_EPS_2YR:.1f}×)")
print(f"  Operating EPS/B history: FY22 ${EPS_FY2022} → FY23 ${EPS_FY2023} → FY24 ${EPS_FY2024} → FY25 ${EPS_FY2025} → FY26E ${EPS_NOW}")
print(f"  Q1 2026               : Operating earnings $11.35B (+18%); cash $397B (record); Abel's 1st quarter")
print(f"  Insurance float       : ${FLOAT_TOTAL:.0f}B (year-end 2025); 87.1% combined ratio; ~$8-9B/yr investment income")
print(f"  GEICO                 : turnaround complete (combined ratio <90%); regaining market share 2025-2026")
print(f"  BNSF                  : $8.1B operating cash flow FY2025; $4.4B dividend to BRK; western US duopoly")
print(f"  BHE                   : regulated utilities; PacifiCorp wildfire litigation is PRIMARY downside risk")
print(f"  Equity portfolio      : ~$318B (Apple 45%; AXP 15%; BAC 11%; KO 7%); $6-8B/yr dividend income")
print(f"  Greg Abel             : CEO since Jan 1, 2026; first buybacks in 21 months (Mar 2026, $1.3B+)")
print(f"  No dividend           : 60-year policy continues; Abel may reconsider if cash exceeds $500B")
print(f"  Market cap            : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}T  (~{SHARES_M:.0f}M B-equiv shares × ${CURRENT_PRICE})")
print(f"  STRONG BUY            : ≤$404  (1.2× book; Buffett buyback floor; ratio_b ~0.5×)")
print(f"  ACCUMULATE (current)  : $440-510  (1.3-1.5× book; fair value zone; ratio_b ~0.85-1.3×)")
print(f"  WATCHLIST / TRIM      : $510-560  (above historical average; reduce without deal catalyst)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.55×  |  Idiosyncratic: 65%  |  Macro: 35%

  Driver                                                      Type    Wt  Note
  ─────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  $397B cash deployment: Abel's 'elephant hunt' timing       IDIO  25%  PRIMARY OPTIONALITY: deal or dividend?
  Insurance float $176B: 87.1% combined ratio; GEICO back    IDIO  20%  CORE MOAT: 60yr compounding engine
  BHE wildfire litigation: PacifiCorp CAT exposure           IDIO  15%  PRIMARY RISK: PG&E scenario possible
  BNSF freight cycle: US industrial production + coal shift  MACRO 20%  CYCLICAL: rail recession = -$1-2B/yr
  Macro/rates: T-bill income on $397B; equity portfolio      MACRO 20%  MATERIAL: 4-5% on $397B = $16-20B/yr""")

print(f"""
  II. SIGNAL FACTORS (SCA Cross-Reads)
  ----------------------------------------------------------------------
  Factor                                              Score   Weight  Contrib
  ─────────────────────────────────────────────────  ──────  ──────  ───────""")
for score, weight, label in SCA_FACTORS:
    contrib = score * weight
    print(f"  {label[:50]:<50}  {score:+.1f}    {weight:.2f}    {contrib:+.3f}")
print(f"  {'':─<50}  {'':─<6}  {'':─<6}  {'':─<7}")
print(f"  {'SCA raw':50}                  {sca_raw:+.3f}")
print(f"  {'SCA adj (÷2.0)':50}                  {sca_adj:+.3f}")

print(f"""
  III. COMPOSITE INFERENCE
  ----------------------------------------------------------------------
  Market composite  : {market_composite:.3f}  ({market_label})
  Adj composite     : {adj_composite:.3f}  ({adj_label})
  Softmax weights at adj composite ({adj_composite:.3f}):""")
for k, w in softmax_weights(adj_composite).items():
    prices = {"BEAR": PRICE_BEAR, "BASE": PRICE_BASE,
              "BULL": PRICE_BULL, "XBULL": PRICE_XBULL}
    print(f"    {k:<6}: {w:.1%}  (${prices[k]})")
ep = expected_price(adj_composite)
print(f"  Expected price (adj): ${ep:.1f}  vs current ${CURRENT_PRICE}  (Δ {(ep-CURRENT_PRICE)/CURRENT_PRICE*100:+.1f}%)")

print(f"""
  IV. SCENARIOS SUMMARY
  ----------------------------------------------------------------------
  BEAR  (${PRICE_BEAR}) : PacifiCorp wildfire litigation results in $20-30B settlement
               (similar to PG&E 2019 bankruptcy; BHE balance sheet stressed).
               BNSF freight volumes fall 15%+ as US manufacturing contracts.
               Insurance: mega-catastrophe year (Pacific earthquake OR
               unprecedented multi-hurricane season >$20B industry loss);
               GEICO reverts to combined ratio above 100%. Equity portfolio
               falls 30% (GAAP hit; but operating earnings floored by T-bill
               income). Abel makes a large acquisition at poor terms (overpays).
               Operating EPS trough ~$12; 28× EPP floor = $336. -31%.

  BASE  (${PRICE_BASE}) : Abel continues patient capital deployment — two to three
               bolt-on acquisitions ($10-30B range each) in 2026-2027; GEICO
               continues gaining market share at sub-90% combined ratio;
               BNSF stable with modest volume growth; BHE wildfire settled
               for <$10B total (manageable within BHE's balance sheet);
               interest income on $397B cash ($16-20B/yr) cushions earnings.
               Operating EPS grows to $24/B by 2027; modest multiple.
               $24 × 24× = $576. +19% from current.

  BULL  (${PRICE_BULL}) : Abel announces first dividend ($3-5/B = $6.5-10B/yr) AND/OR
               announces a transformative acquisition ($100-200B deal in
               financial services, infrastructure, or energy) that creates
               $3-5B/yr in incremental operating earnings. Market re-rates
               BRK from "Buffett's legacy" to "Abel's Berkshire 2.0."
               Multiple expands to 28×. $24 × 28× = $672. +38%.

  XBULL (${PRICE_XBULL}) : Abel deploys $200B+ across 2026-2028 into multiple transformative
               deals (infrastructure + energy + financial services platform);
               initiates $5-8/B annual dividend; GEICO becomes #1 US auto
               insurer; BNSF benefits from re-shoring manufacturing wave;
               BHE wildfire settled and BHE IPO'd at a premium multiple;
               book value compounds 15%/yr. FY2028-29E ~$30/B × 28× = $840.
               +73%. Requires sustained world-class capital allocation at scale.
""")

print("=" * 72)
print(f"  END OF REPORT -- BRK.B  |  Generated 2026-05-26")
print("=" * 72)
