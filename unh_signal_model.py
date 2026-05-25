"""
UnitedHealth Group Incorporated (NYSE: UNH) — BottomUp Risk/Reward Signal Model

SIGNAL:  ▷ HOLD/TRIM
RATIO B: 2.25x  (Method B at 20× FY2027E $24 = $480; ratio 208/93 = 2.25×)
DATE:    2026-05-25
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER  = "UNH"
COMPANY = "UnitedHealth Group Incorporated"
SECTOR  = "Managed Care · Medicare Advantage · Optum Health & Rx · Health Insurance"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  = 387.30   # UNH — fetched from Yahoo Finance, 2026-05-25
PRICE_52W_LOW  = 234.60   # 52-week low: 2025 crash (CEO exit + MA crisis + DOJ probe)
PRICE_52W_HIGH = 404.15   # 52-week high: recent recovery; stock down ~25% from 2024 peak ~$520
SHARES_M       = 910.0    # million diluted shares outstanding

# ── EPS (adjusted / non-GAAP — UNH's own metric) ──────────────────────────────
# UNH fiscal year = calendar year (Jan–Dec).
EPS_FY2022 = 22.19    # Record year; Optum momentum strong; Medicare Advantage expanding
EPS_FY2023 = 25.12    # Another record; MA membership + Optum health services scaling
EPS_FY2024 = 27.66    # Peak pre-crisis; Change Healthcare cyberattack impacted H1 2024
EPS_FY2025 = 14.91    # CRISIS YEAR: MA medical cost explosion, CEO Witty resignation (May 2025),
                       # guidance suspended, DOJ investigation confirmed; massive claims surge
EPS_NOW    = 20.00    # FY2026E adj (company guided >$18.25; Q1 2026 adj EPS $7.23 — Q1 strong;
                       # H2 expected weaker due to MA seasonality + legal reserves)
                       # Q1 2026: Revenue $111.7B (+2% YoY); adj EPS $7.23

# ── EPP Floor ─────────────────────────────────────────────────────────────────
# Trough EPS = FY2025 ($14.91): the actual crisis floor when MA losses peaked,
# guidance was pulled, and DOJ investigation became public. This is the verified
# earnings trough, not an estimate.
# Min-viable P/E = 12×: managed care companies trough at 10-14×; UNH as the
# largest (#1 US insurer by revenue) commands a small premium at its worst.
EPS_TROUGH = 14.91    # FY2025 non-GAAP — actual crisis-year trough
EPP_MIN_PE = 12       # Managed care trough floor; UNH quality premium vs generic insurer
EPP        = EPS_TROUGH * EPP_MIN_PE   # $14.91 × 12 = $178.92

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2027E adj EPS: ~$24 consensus (recovery trajectory; DOJ discount applied;
# MA restructuring + Optum growth; CMS 2027 flat rate headwind partially absorbed)
# Exit P/E: 20× — below pre-crisis 22-25× norm, reflecting DOJ overhang, MA
# structural uncertainty, and political/regulatory risk on drug pricing.
#   At 20×: $480  (+24% from $387)
#   At 23×: $552  (+43%)
#   At 25×: $600  (+55%)
CONS_EPS_2YR = 24.00
CONS_EXIT_PE = 20

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
# BEAR:  DOJ criminal prosecution + civil settlement depletes capital; MA continues
#        to bleed; EPS reset to ~$8-10; 10× trough multiple = ~$90
# BASE:  DOJ civil settlement (no criminal prosecution); MA margins partially
#        recover; FY2027E $24 × 18× = $432 — close to current analyst consensus PT
# BULL:  Hemsley operational turnaround succeeds; DOJ settled favorably (civil only);
#        MA trend reverses; Optum Health becomes true care delivery platform; $26 × 23×
# XBULL: Full crisis resolved; UNH returns to compounding machine; FY2029E ~$35 × 25×
PRICE_BEAR  =   90
PRICE_BASE  =  432
PRICE_BULL  =  598
PRICE_XBULL =  875

# ── SCA (Stock-Composite Adjustment) ──────────────────────────────────────────
SCA_FACTORS = [
    (+0.50, 0.25, "Optum Health/Rx vertically integrated platform (growing double-digit)"),
    (+0.40, 0.15, "Hemsley return as CEO — built UNH from 2006-2017; credibility + discipline"),
    (-0.80, 0.25, "DOJ criminal + civil probe: MA billing fraud, False Claims Act — existential"),
    (-0.50, 0.20, "Medicare Advantage structural: flat 2027 CMS rate + chronic cost inflation"),
    (+0.30, 0.10, "Scale moat: 50M+ members, $440B+ revenue, #1 US managed care globally"),
    (-0.20, 0.05, "Political/regulatory risk: drug pricing, DOGE healthcare scrutiny, MA reform"),
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

# ══════════════════════════════════════════════════════════════════════════════
print("=" * 72)
print(f"  {TICKER}  —  {COMPANY}")
print(f"  {SECTOR}")
print("=" * 72)

print("""
PART 1 — FRAMEWORK OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EPP (Earnings Power Price) — structural floor
  = EPS_TROUGH × EPP_MIN_PE
  FY2025 adj EPS ($14.91) × 12× managed-care trough floor. FY2025 was the
  actual verified crisis — MA medical costs exploded, CEO resigned, guidance
  was pulled, and the DOJ investigation went public. $14.91 is the real
  floor, not an estimate. EPP = $178.92. The 52-week low ($234.60) held 57%
  above EPP, reflecting market confidence in Optum + franchise survival.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E consensus adj EPS $24 × 20× exit P/E (DOJ-discounted from historical
  22-25×) = $480. At 20×: +24% from current $387.
  Ratio B = ($387.30 − $178.92) / ($480 − $387.30) = $208 / $93 = 2.25×
  → ▷ HOLD/TRIM. Upside exists but is constrained relative to the EPP gap.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

UNITEDHEALTH: THE WORLD'S LARGEST HEALTH INSURER — POST-CRISIS RECOVERY
=========================================================================

UnitedHealth Group is the most complex and vertically integrated health
enterprise on the planet — simultaneously running the largest US health
insurer (UnitedHealthcare, ~50M members) and one of the largest healthcare
services businesses (Optum Health, Optum Rx, Optum Insight). At over $440B
in annual revenue it is larger than many nation-states' healthcare budgets.
The 2025 crisis was severe but did not destroy the franchise. The debate
today: how much of the recovery is priced in, and what is the DOJ discount?

THE 2025 CRISIS — WHAT HAPPENED
═════════════════════════════════
1. MEDICARE ADVANTAGE COST EXPLOSION
   Medicare Advantage members — especially those new to UnitedHealthcare
   in 2025 — consumed vastly more healthcare than priced into premiums.
   The "medical loss ratio" (MLR) blew out. UNH had been flagging MA cost
   pressure; in Q1 2025 it became a miss (first in over a decade), and by
   May 2025 management pulled guidance entirely. FY2025 EPS came in at
   $14.91 vs prior guidance of $29.50-$30.00 — a ~50% shortfall.

2. CEO ANDREW WITTY RESIGNATION (MAY 13, 2025)
   Witty stepped down citing personal reasons. Stephen Hemsley — who built
   UNH into a mega-cap from 2006-2017 — returned as CEO immediately. Market
   read Witty's exit as forced by crisis management failure. Stock fell ~18%
   on the announcement alone; down ~25% year-to-date at that point.

3. DOJ CRIMINAL + CIVIL INVESTIGATION (CONFIRMED JULY 2025)
   UNH confirmed active DOJ investigations into Medicare Advantage billing:
   • Criminal probe: whether the company manipulated patient diagnoses
     (via in-home nurse assessments) to inflate risk scores and extract
     higher CMS reimbursements. Criminal means potential prosecution.
   • Civil probe: False Claims Act violations from a 2011 whistleblower
     case, alleging improper risk adjustment submissions.
   The combination of criminal + civil with a 2011 origination (14-year
   history) suggests deep, systematic issues — not isolated events.
   Status as of May 2026: ongoing, no resolution announced.

4. CHANGE HEALTHCARE CYBERATTACK (FEBRUARY 2024 — TAIL INTO 2025)
   The $22B Optum-owned Change Healthcare unit was hit by the largest
   healthcare data breach in US history. Disrupted claims processing
   for ~70% of US hospitals for months. Costs exceeded $3B; class action
   lawsuits ongoing; regulatory scrutiny elevated.

Q1 2026 — RECOVERY IN PROGRESS
════════════════════════════════
  Revenue:              $111.7B (+2% YoY — growth constrained by MA exit/restructuring)
  Adjusted EPS:         $7.23   (strong Q1; H2 expected to moderate on MA seasonality)
  FY2026 guidance:      >$18.25 adj EPS (conservative given DOJ legal reserve uncertainty)
  Note: Q1 EPS of $7.23 implies full-year well above $18.25 if H2 holds
        — management likely holding back given DOJ proceedings

OPTUM — THE REAL ASSET
══════════════════════
Optum is what makes UNH structurally different from a pure insurer:
  • Optum Health: ~90,000 physicians employed or affiliated; care delivery
    at scale; drives medical cost savings through integrated management
  • Optum Rx: one of the largest pharmacy benefit managers (PBM) in the US;
    $120B+ annual prescription revenue
  • Optum Insight: healthcare data/analytics/technology
Optum collectively generates ~50-55% of UNH's operating earnings and is
the primary re-rating lever if the DOJ crisis is resolved favourably.

MEDICARE ADVANTAGE — THE STRUCTURAL PROBLEM
════════════════════════════════════════════
MA is the fastest-growing segment of US healthcare (~60% of Medicare now in
MA plans). The structural challenge:
  • CMS (Centers for Medicare & Medicaid Services) sets the premium rates.
    For 2027, CMS proposed a nearly FLAT 0.09% rate increase.
  • Medical costs continue to inflate 5-8%/yr.
  • Insurers who priced aggressively in 2022-2023 (when rates were generous)
    are now underwater on those cohorts.
  • UNH was the most aggressive at MA membership growth and is paying the
    highest price. The structural mismatch likely persists into 2027.

ANALYST CONSENSUS
══════════════════
  Consensus price target:   $391.79  (28 analysts) — effectively AT current price $387
  Buy/Hold/Sell:            22 Buy | 5 Hold | 1 Sell → 78% bullish
  UBS target raised to $460 (Buy)
  Implication: even bullish consensus barely sees upside from here. This is a
  HOLD at current price by definition of the analyst community's own targets.

DOJ RISK QUANTIFICATION
═════════════════════════
The DOJ investigation is the single largest risk. Potential outcomes:
  • Best case (civil only): $2-5B settlement, paid over 2-3 years, no
    admission of wrongdoing. Manageable. EPS diluted ~$2-3 over settlement years.
  • Base case (civil + deferred prosecution): $8-15B settlement, monitoring,
    restrictions on certain MA billing practices. Significant but survivable.
  • Worst case (criminal prosecution): Potential exclusion from Medicare /
    Medicaid programs. This is existential — UNH cannot survive as a managed
    care company without CMS contracts. Probability low but non-zero.
  Market currently prices the "base case" scenario with some worst-case tail.

WHERE THE RISK/REWARD IMPROVES
════════════════════════════════
  WATCHLIST  : $310-330  (FY2027E ~13-14×; ratio_b ~1.5×; post-settlement clarity)
  ACCUMULATE : $260-280  (FY2027E ~11-12×; ratio_b ~0.8×; near 52-wk low zone)
  BUY        : $180-210  (approaching EPP + worst-case DOJ scenario priced)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("PART 3 — NUMBERS & SIGNALS")
print("=" * 72)
print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │  SIGNAL:  {signal_primary:<12}  │  RATIO B: {ratio_b_fmt:<10}               │
  │  TICKER:  {TICKER:<10}    │  SECTOR:  Healthcare / Managed Care    │
  └──────────────────────────────────────────────────────────────────┘

  ----------------------------------------------------------------------
""")

print(f"  Current price         : ${CURRENT_PRICE:.2f}  (+65% from 52-wk low ${PRICE_52W_LOW}; -4% from 52-wk high ${PRICE_52W_HIGH})")
print(f"  EPP floor             : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above; 12× × ${EPS_TROUGH} FY2025 crisis trough)")
print(f"  Method B (20× exit)   : ${price_b:.2f}  (+{(price_b/CURRENT_PRICE-1)*100:.1f}% from current; ratio_b = {ratio_b:.2f}× → HOLD/TRIM)")
print(f"  At 23× exit           : ${CONS_EPS_2YR*23:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*23-CURRENT_PRICE):.2f}× → WATCHLIST")
print(f"  At 25× exit           : ${CONS_EPS_2YR*25:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*25-CURRENT_PRICE):.2f}× → WATCHLIST")
print(f"  BEAR scenario         : ${PRICE_BEAR}    (-77%; criminal DOJ prosecution; MA exclusion risk; EPS ~$8-10)")
print(f"  BASE scenario         : ${PRICE_BASE}   (+12%; FY2027E $24 × 18×; civil settlement + MA recovery)")
print(f"  BULL scenario         : ${PRICE_BULL}   (+54%; FY2027E $26 × 23×; Hemsley turnaround + DOJ resolved)")
print(f"  XBULL scenario        : ${PRICE_XBULL}   (+126%; FY2029E ~$35 × 25×; Optum dominates care delivery)")
print(f"  Forward P/E (FY2026E) : {CURRENT_PRICE/EPS_NOW:.1f}×  (${CURRENT_PRICE} / ${EPS_NOW}; guidance >$18.25; using $20 est)")
print(f"  Forward P/E (FY2027E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (${CURRENT_PRICE} / ${CONS_EPS_2YR}; recovery year; DOJ discounted)")
print(f"  EPS history           : FY22 ${EPS_FY2022} → FY23 ${EPS_FY2023} → FY24 ${EPS_FY2024} → FY25 ${EPS_FY2025} (crisis) → FY26E ~${EPS_NOW}")
print(f"  Q1 2026               : Revenue $111.7B (+2% YoY); adj EPS $7.23 (strong; H2 expected weaker)")
print(f"  DOJ status            : Criminal + civil ongoing (Medicare billing fraud; False Claims Act)")
print(f"  CEO                   : Stephen Hemsley (returned May 2025; was CEO 2006-2017)")
print(f"  Analyst consensus PT  : $391.79 (~AT current price; 22 Buy / 5 Hold / 1 Sell)")
print(f"  Dividend yield        : ~2.3% at current price ($8.80/share annualised)")
print(f"  Market cap            : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  WATCHLIST entry       : $310-330  (FY2027E ~13-14×; ratio_b ~1.5×; DOJ clarity)")
print(f"  ACCUMULATE entry      : $260-280  (near 52-wk low; ~11-12× FY2027E; worst-case priced)")
print(f"  BUY entry             : $180-210  (approaching EPP; catastrophic scenario priced in)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~0.55×  |  Idiosyncratic: 75%  |  Macro: 25%

  Driver                                                     Type    Wt  Note
  ────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  DOJ criminal + civil Medicare fraud investigation          IDIO    25%  KEY BEAR: criminal probe is existential tail risk
  Medicare Advantage cost inflation vs CMS flat rate 2027    IDIO    20%  KEY BEAR: structural margin squeeze; multi-year
  Optum Health/Rx vertically integrated platform growth      IDIO    25%  KEY BULL: ~50% of earnings; growing double-digit
  Hemsley return: operational discipline + cost restructuring IDIO  15%  BULL: credibility + execution track record
  Scale + market position (50M members; #1 US insurer)       IDIO  10%  STRUCTURAL: not easily disrupted; CMS dependency
  Macro: employment, rate sensitivity, regulatory backdrop   MACRO    5%  Low beta vs S&P; primarily idiosyncratic story""")

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
  BEAR  (${PRICE_BEAR}) : DOJ criminal prosecution → UNH excluded from Medicare/Medicaid
               programs. Existential outcome. EPS collapses to $8-10 on rump
               commercial business. 10× trough = ~$90. -77% from current.
               Low probability (~5-8%) but fat tail; market is not pricing this
               at 0%.

  BASE  (${PRICE_BASE}) : DOJ civil settlement ($8-15B over 3 years); criminal deferred
               prosecution agreement; MA margins partially recover 2027+; Optum
               continues double-digit growth. FY2027E $24 × 18× = $432. +12%
               from current. Barely above analyst consensus PT ($391.79).

  BULL  (${PRICE_BULL}) : Civil-only DOJ settlement ($2-5B); MA trend inflects positively
               (Hemsley restructuring works); Optum Health at scale; FY2027E
               $26 × 23× = $598. +54%. Requires DOJ to go civil-only AND MA
               to recover AND Optum to execute. All three simultaneously.

  XBULL (${PRICE_XBULL}) : Full crisis resolution; UNH returns to 25%+ ROE compounder.
               Optum Health dominant care delivery platform; FY2029E adj EPS
               ~$35 × 25× = $875. +126% over 3-4 years. Requires complete
               legal clearance and structural MA margin recovery.
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-25")
print("=" * 72)
