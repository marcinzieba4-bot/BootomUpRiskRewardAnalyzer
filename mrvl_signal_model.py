"""
Marvell Technology (NASDAQ: MRVL) — BottomUp Risk/Reward Signal Model

SIGNAL:  ✕ AVOID
RATIO B: N/A (Method B at 35× FY2028E = $190.40 — BELOW current price $196)
DATE:    2026-05-25
"""

import math

# ── Identifiers ────────────────────────────────────────────────────────────────
TICKER   = "MRVL"
COMPANY  = "Marvell Technology, Inc."
SECTOR   = "Semiconductors · AI Custom Silicon (ASIC) · Optical Interconnect · Data Center"

# ── Price ──────────────────────────────────────────────────────────────────────
CURRENT_PRICE  = 196.00   # MRVL — fetched from Investing.com, 2026-05-25 (day range $192-$198)
PRICE_52W_LOW  = 58.61    # 52-week low (2025 trough; chip cycle + AI narrative washout)
PRICE_52W_HIGH = 198.40   # 52-week high — ALL-TIME HIGH (May 24, 2026 — YESTERDAY)
SHARES_M       = 867.0    # million diluted shares (approx, post stock compensation)

# ── Fiscal Year Note ──────────────────────────────────────────────────────────
# Marvell's fiscal year ends late January / early February.
#   FY2024 ended ~Feb 3, 2024  |  FY2025 ended ~Feb 1, 2025
#   FY2026 ended ~Feb 1, 2026  |  FY2027 ends ~Jan 31, 2027 (current)
# All EPS = non-GAAP diluted (standard analyst metric; GAAP is deeply negative due to
# stock-based comp + intangible amortisation from Cavium/Inphi acquisitions).

# ── EPS (non-GAAP, normalized) ────────────────────────────────────────────────
EPS_FY2024   = 1.51    # FY2024 — chip downcycle trough (annual; Q4 FY2024 single-Q = $0.46)
EPS_Q1FY2025 = 0.24    # Q1 FY2025 — single-quarter trough (annualised = $0.96)
EPS_FY2025   = 1.57    # FY2025 — H1 weak ($0.24+$0.30), H2 AI recovery ($0.43+$0.60 est)
EPS_FY2026   = 2.84    # FY2026 — COMPLETED; strong AI-driven growth (+81% YoY vs FY2025)
EPS_TROUGH   = 1.51    # FY2024 annual trough — worst full-year adj EPS in recent history
EPS_NOW      = 2.84    # FY2026 (most recently completed year, Jan 2026)
EPP_MIN_PE   = 25      # AI custom silicon floor: market won't let it trade below 25× even at trough
EPP          = EPS_TROUGH * EPP_MIN_PE   # $1.51 × 25 = $37.75

# ── Method B ──────────────────────────────────────────────────────────────────
# FY2028E consensus non-GAAP EPS = $5.44 (9 analysts; management guide "well over $5")
# Exit P/E = 35× for AI custom silicon company with hyperscaler moat (fair, not bull)
# price_b = $5.44 × 35 = $190.40 → BELOW current price $196.00
# Even at 40× exit: price_b = $217.60; ratio_b = (196-37.75)/(217.60-196) = 7.33× → AVOID
# Signal: N/A (Method B breached) → ✕ AVOID
CONS_EPS_2YR  = 5.44    # FY2028E consensus non-GAAP (matches mgmt "well over $5" guide)
CONS_EXIT_PE  = 35      # AI custom silicon fair value multiple (not growth premium; base case)

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

# ── Scenario prices ──────────────────────────────────────────────────────────
# BEAR: AI capex cycle reverses; hyperscaler insourcing accelerates; EPS resets to ~$1
#       1.00 × 30× = $30 (still premium multiple given franchise)
# BASE: FY2028E $5.44 × 35× = $190 (fair value, ALREADY BELOW current price)
# BULL: FY2028E $5.44 × 50× + 3rd hyperscaler win: $272
# XBULL: MRVL becomes dominant AI silicon platform; FY2029E ~$8 × 50× = $400
PRICE_BEAR  = 30
PRICE_BASE  = 190
PRICE_BULL  = 272
PRICE_XBULL = 400

# ── SCA (Stock-Composite Adjustment) ─────────────────────────────────────────
SCA_FACTORS = [
    # (score, weight, label)
    (+0.80, 0.30, "Amazon Trainium momentum + custom silicon pipeline (2-3 hyperscalers)"),  # IDIO +
    (-0.60, 0.25, "Hyperscaler insourcing risk (customers building own chips)"),              # IDIO -
    (+0.50, 0.15, "Optical interconnect (800G/1.6T): CPO, electro-optic modules"),           # IDIO +
    (+0.30, 0.15, "AI capex cycle continuation (hyperscaler CapEx still $700B+ in 2026)"),   # MACRO +
    (-0.10, 0.10, "China export restrictions (limited MRVL China data center exposure)"),    # MACRO -
    (-0.40, 0.05, "Broadcom competition in custom silicon (alternative hyperscaler vendor)"), # IDIO -
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
  Marvell's FY2024 trough non-GAAP EPS ($1.51) × 25× floor multiple.
  AI custom silicon franchise commands a higher trough P/E than commodity
  semiconductors; even at cycle trough, the market will not let a dominant
  hyperscaler ASIC partner derate below 25×.

Method B — 2-year normalized upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2028E analyst consensus $5.44 × 35× exit = $190.40.
  At $196 current price, MRVL has ALREADY EXCEEDED its 2-year base case
  fair value ceiling. Method B → N/A → ✕ AVOID.

Fiscal Year: Marvell year ends late January. FY2026 = ended ~Feb 1, 2026.
All EPS = non-GAAP diluted (GAAP is negative due to SBC + amortisation).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MARVELL: AI CUSTOM SILICON POWERHOUSE — BUT PRICED BEYOND ITS 2-YEAR TARGET
=============================================================================

Marvell has undergone one of the most dramatic business transformations in
semiconductor history. Once known primarily for broadband/storage controllers
and networking chips, the company is now the leading independent designer of
custom AI silicon (ASICs) for hyperscale data centres. The pivots that made
this possible: the $6B Cavium acquisition (2018, data centre networking) and
the $10B Inphi acquisition (2021, optical interconnect, electro-optic ICs).

CUSTOM SILICON: THE THESIS
══════════════════════════
Amazon AWS (Trainium 2, Trainium 3) is Marvell's anchor AI customer. Trainium
chips — designed with Marvell's ASIC services — power AWS's own AI training
infrastructure, reducing dependence on NVIDIA H100/H200 and enabling
Amazon-specific architecture optimisation. This is Marvell's 'ratable revenue'
story: multi-year silicon development deals with guaranteed production volumes.

Optical interconnect (Inphi legacy): 800G and 1.6T electro-optic modules are
essential for AI cluster fabric bandwidth. Marvell holds a leading position in
co-packaged optics (CPO) — the next-generation architecture for data centre
interconnects. This segment is under-appreciated by most sell-side analysts.

THE NUMBERS: A GENUINE ACCELERATION STORY
══════════════════════════════════════════
  FY2024 (trough):  $1.51 non-GAAP EPS  (chip downcycle; consumer/carrier weak)
  FY2025:           $1.57 non-GAAP EPS  (H1 weak at $0.24/Q; H2 recovery begins)
  FY2026 (done):    $2.84 non-GAAP EPS  (+81% YoY; AI ramp overwhelming other weakness)
  FY2027E (curr):   $3.82 non-GAAP EPS  (consensus; mgmt guide: approaching $11B revenue)
  FY2028E:          $5.44 non-GAAP EPS  (consensus; mgmt: "well over $5")
  FY2027 revenue:   approaching $11B    (+30%+ YoY; management raised Feb 2026)

The growth trajectory is real and rare. At $11B revenue with 50%+ gross
margins, Marvell's EBITDA profile approaches $5-5.5B — a genuine cash machine.

THE PROBLEM: +235% IN 12 MONTHS, AT ATH WITH EARNINGS IN 2 DAYS
════════════════════════════════════════════════════════════════
MRVL closed at $196 on May 24, 2026 — its ALL-TIME HIGH (52-wk high $198.40).
The stock has rallied +235% from its 52-week low of $58.61.

  FY2028E $5.44 × 35× (base AI semi exit) = $190.40 → BELOW current price.
  FY2028E $5.44 × 40× (premium exit)       = $217.60 → ratio_b = 7.33× → AVOID.
  FY2028E $5.44 × 50× (bull multiple)      = $272.00 → ratio_b = 3.50× → still AVOID.

The only scenario that supports the current price is:
  a) EPS significantly above consensus ($6.50+ by FY2028), or
  b) Multiple expansion well above 40× (growth re-rating), or
  c) Winning a 3rd or 4th hyperscaler ASIC deal (Google TPU, Meta, Microsoft)

EARNINGS IN 2 DAYS (MAY 27, 2026) — ASYMMETRIC RISK AT ATH
═══════════════════════════════════════════════════════════
Q1 FY2027 results due after market close May 27, 2026. Consensus:
  Revenue: $2.4B (±5%) | EPS: $0.75–$0.79

A beat is EXPECTED given the 24-hour pre-earnings analyst upgrade frenzy:
  Citi: PT raised $118 → $215  |  Melius: $140 → $220
  BofA: $125 → $200            |  TD Cowen: $90 → $180

When every analyst raises the day before earnings, the bar is implicitly higher
than the formal consensus number. Any miss — or guidance that doesn't raise
FY2027 meaningfully — could trigger a -15-20% reversal from ATH.

This is the identical setup to PANW ($260, Q3 earnings June 2) and TSLA: the
market prices the bull scenario as the floor, then the stock dips when 'merely
good' results arrive. The risk/reward at ATH the day before earnings is
structurally unfavourable.

WHERE THE RISK/REWARD IMPROVES
════════════════════════════════
  WATCHLIST  : $140–155  (ratio_b ~1.3-1.5×; 27-28× FY2028E; post-earnings reset)
  ACCUMULATE : $120–135  (ratio_b ~0.8-1.0×; ~23-25× FY2028E; approaching EPP zone)
  BUY        :  $80–100  (ratio_b ~0.5-0.65×; trough P/E scenario; panic washout)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("PART 3 — NUMBERS & SIGNALS")
print("=" * 72)
print(f"""
  ┌────────────────────────────────────────────────────────────────┐
  │  SIGNAL:  {signal_primary:<12}  │  RATIO B: {ratio_b_fmt:<10}             │
  │  TICKER:  {TICKER:<10}    │  NEXT EVENT: Earnings May 27       │
  └────────────────────────────────────────────────────────────────┘

  ----------------------------------------------------------------------
""")

print(f"  Current price       : ${CURRENT_PRICE:.2f}  (+235% from 52-wk low ${PRICE_52W_LOW}; at ATH ${PRICE_52W_HIGH})")
print(f"  EPP floor           : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above; 25× × ${EPS_TROUGH} trough EPS FY2024)")
print(f"  Method B target     : ${price_b:.2f}  (FY2028E ${CONS_EPS_2YR} × {CONS_EXIT_PE}× = BELOW current → N/A → AVOID)")
print(f"  At 40× exit         : ${CONS_EPS_2YR * 40:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*40-CURRENT_PRICE):.2f}× → still AVOID")
print(f"  At 50× exit         : ${CONS_EPS_2YR * 50:.2f}  ratio_b = {(CURRENT_PRICE-EPP)/(CONS_EPS_2YR*50-CURRENT_PRICE):.2f}× → still AVOID")
print(f"  BEAR scenario       : ${PRICE_BEAR}  (-85%; AI capex cycle reversal; EPS resets to ~$1; 30×)")
print(f"  BASE scenario       : ${PRICE_BASE}  (-3%; FY2028E ${CONS_EPS_2YR} × 35× = already BELOW current)")
print(f"  BULL scenario       : ${PRICE_BULL}  (+39%; FY2028E ${CONS_EPS_2YR} × 50× + 3rd hyperscaler win)")
print(f"  XBULL scenario      : ${PRICE_XBULL}  (+104%; FY2029E ~$8 × 50×; dominant AI silicon platform)")
print(f"  Forward P/E (FY27E) : {CURRENT_PRICE/3.82:.1f}×  (${CURRENT_PRICE} / $3.82 FY2027E; pricey but growth warranted)")
print(f"  Forward P/E (FY28E) : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (${CURRENT_PRICE} / ${CONS_EPS_2YR} FY2028E; already at fair-value exit)")
print(f"  FY2027 rev guidance : approaching $11B (+30%+ YoY; management raised Feb 2026)")
print(f"  Q1 FY2027 consensus : Revenue $2.4B ±5% | EPS $0.75-0.79 (results May 27)")
print(f"  Market cap          : ~${CURRENT_PRICE * SHARES_M / 1000:.1f}B  ({SHARES_M:.0f}M diluted shares × ${CURRENT_PRICE})")
print(f"  Analyst targets     : Citi $215 | Melius $220 | BofA $200 | TD Cowen $180")
print(f"  WATCHLIST entry     : $140-155  (27-28× FY2028E; ratio_b ~1.3-1.5×)")
print(f"  ACCUMULATE entry    : $120-135  (~23-25× FY2028E; ratio_b ~0.8-1.0×)")
print(f"  BUY entry           : $80-100   (trough zone; ratio_b ~0.5-0.65×)")

print(f"""
  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: ~1.35×  |  Idiosyncratic: 65%  |  Macro: 35%

  Driver                                                     Type    Wt  Note
  ────────────────────────────────────────────────────────  ─────  ────  ──────────────────────────────────────
  Amazon Trainium momentum + custom silicon pipeline        IDIO    30%  PRIMARY: Trainium 3 tape-out 2026; AWS GPU capex redirected
  Hyperscaler insourcing risk (customers build own chips)   IDIO    25%  KEY BEAR RISK: if AWS/Google decide to design fully in-house
  Optical interconnect (800G/1.6T CPO market position)     IDIO    15%  Under-appreciated: co-packaged optics = $5B+ TAM by FY2028
  AI capex cycle continuation (hyperscaler spend 2026+)    MACRO   15%  $700B+ annual capex; still accelerating; MRVL direct beneficiary
  China export restrictions (limited MRVL China DC expo.)  MACRO   10%  <15% China DC revenue; less exposed than peer semis
  Broadcom competition in custom silicon                    IDIO     5%  AVGO serves Google/Meta; MRVL serves Amazon/others — not overlap""")

print(f"""
  II. SIGNAL FACTORS (SCA Cross-Reads)
  ----------------------------------------------------------------------
  Factor                                              Score   Weight  Contrib
  ─────────────────────────────────────────────────  ──────  ──────  ───────""")
for score, weight, label in SCA_FACTORS:
    contrib = score * weight
    label_short = label[:50]
    print(f"  {label_short:<50}  {score:+.1f}    {weight:.2f}    {contrib:+.3f}")
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
  BEAR  (${PRICE_BEAR}) : AI capex reverses (tariffs, recession, cloud slowdown). Hyperscalers
               cancel/defer Trainium 3. Optical interconnect delays. EPS resets to ~$1.
               Stock derated to 30× trough = $30. –85% from current. Low probability
               but non-trivial given valuation at 36× forward.

  BASE  (${PRICE_BASE}) : FY2028E consensus $5.44 × 35× = $190.40. Modest downside (-3%)
               over 2 years. Marvell executes perfectly but the run-up means
               2-year total return ≈ -3% (no dividend). Capital opportunity cost.

  BULL  (${PRICE_BULL}) : 3rd hyperscaler ASIC win announced (Google TPU or Meta); FY2028E
               EPS revised up to $6.50; market re-rates to 42× = $273. +39% from
               here. Requires catalyst not in current consensus.

  XBULL (${PRICE_XBULL}) : MRVL wins 4 hyperscalers; optical CPO ramp ahead of schedule;
               FY2029E EPS ~$8 × 50× = $400. +104% over 2+ years. Market must
               believe MRVL = standard AI infrastructure (like ARM in mobile).
""")

print("=" * 72)
print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-25")
print("=" * 72)
