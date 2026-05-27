"""
Citigroup Inc.  (C)
BottomUp Risk/Reward Analyzer — Signal Model
"""
import math

# ── Core inputs ──────────────────────────────────────────────────────────────
TICKER        = "C"
COMPANY       = "Citigroup Inc."
SECTOR        = "Global Banking · Services (TTS/Securities) · Markets · Wealth · US Consumer Cards"

CURRENT_PRICE  = 126.20   # C — fetched via web search, 2026-05-26
                            # Day range $126.08–$127.42; 52-wk range $73.49–$135.29
                            # Stock +63% in 12 months (52-wk low $73.49 → current)
PRICE_52W_LOW  =  73.49   # April/May 2025 tariff-panic + transformation trough
PRICE_52W_HIGH = 135.29   # Recent 52-wk high; current $126 is 6.7% below peak
SHARES_M       = 1705.6   # Q1 2026 common shares outstanding; was ~1,900M in FY2022 (-10%)
DIVIDEND_ANN   =   2.40   # $0.60/quarter (confirmed May 2026 payment); yield 1.9%

# ── EPS history (GAAP diluted) ────────────────────────────────────────────────
# NOTE: Citigroup's 2022-2025 EPS is SEVERELY depressed by transformation charges:
# Q4 2023: FDIC special assessment ($2.7B) + Argentina exposure + Russia reserves
# FY2024-2025: ongoing restructuring (severance, office closures, consent order remediation)
# FY2026 = first "clean" year post-transformation. EPS step-up is real, not cyclical.
EPS_HISTORY = {
    "FY2022": 7.00,    # Pre-transformation trough; $7.00 GAAP ($7.11 continuing ops);
                        # highest recent year before charges dominated; 1,964M avg diluted shares
    "FY2023": 5.78,    # Q4 2023 charges: FDIC special $2.7B + Argentina + Russia = ~$3/shr drag
    "FY2024": 5.14,    # Continued restructuring; Banamex Mexico sale process; consent order costs
    "FY2025": 4.61,    # Final transformation year; still charging off legacy issues; ROTCE ~7-8%
                        # NOTE: underlying operating earnings were improving; GAAP masked by charges
}
EPS_NOW = 10.50   # FY2026E post-Q1 beat; Q1 2026 actual $3.06 (beat $2.64 consensus by 16%)
                   # First "clean" full year: transformation charges largely eliminated;
                   # Annualised Q1: $12.24; consensus $10.16-10.49 (allows H2 seasonality)

# ── EPP (Earnings Power Price) — structural floor ────────────────────────────
EPS_TROUGH  = 4.00    # Severe recession: provisions spike (Citi's global consumer card book,
                        # ~$200B+ in US cards alone, generates big NCO spikes in recessions);
                        # trading revenues volatile; global macro drag. $4.00 ≈ FY2025 actual
                        # (worst recent year) — recession makes that BAD year look like a template.
                        # Extreme tail: 2008-2009 Citi was insolvent; government bailout required.
                        # This model uses $4.00 as a "bad-but-recoverable" recession scenario,
                        # not an existential crisis. TBV provides a hard floor at ~$99 current.
EPP_MIN_PE  = 9       # Commercial bank trough multiple; same as JPM/BAC/WFC franchise floor.
                        # Citi does NOT get a premium vs peers on trough multiple (unlike AXP/PGR)
                        # because its complexity and historical execution failures mean markets
                        # discount it on trough. 52-wk low $73.49 / FY2026E $10.50 = 7.0× fwd
                        # (extreme trough); 9× is a fair structural floor given franchise value.
EPP         = EPS_TROUGH * EPP_MIN_PE   # = $36.00

# ── Method B (2-year normalised upside ceiling) ───────────────────────────────
CONS_EPS_2YR  = 12.50   # FY2027E adj EPS; consensus implies ~16-20% growth from FY2026E $10.50;
                          # ROTCE trajectory: Q1 2026 13.1% (exceeds 10-11% target); FY2027
                          # company guides 11-13% ROTCE; at 12% ROTCE → ~$12.50 EPS reasonable.
                          # Fraser medium-term target 14-15% ROTCE (2029-2031) could push higher.
CONS_EXIT_PE  = 14        # Post-transformation re-rating: at sustained 12%+ ROTCE, Citi deserves
                          # to trade closer to BAC (14×) and WFC (13×) than its current 12×.
                          # 14× still discounts Citi vs JPM (14-15×) for remaining complexity/risk.
                          # Bull case: if 14-15% ROTCE materialises, 15-16× multiple possible.
price_b = CONS_EPS_2YR * CONS_EXIT_PE   # = $175.00

# ── Primary signal: Ratio B ───────────────────────────────────────────────────
ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
# = (126.20 - 36.00) / (175.00 - 126.20) = 90.20 / 48.80 = 1.848×
# Signal: ▷ HOLD/TRIM (1.75–2.50×) — stock has already re-rated +63% from lows

# ── Softmax composite engine ──────────────────────────────────────────────────
T = 0.60
SCENARIOS = {
    "BEAR":  {"price":  36.00, "label": "BEAR"},   # EPP floor; severe recession; NCOs spike
    "BASE":  {"price": 143.00, "label": "BASE"},   # FY2026E $10.50 × 13.6× = $143; analyst PT
    "BULL":  {"price": 175.00, "label": "BULL"},   # Method B; FY2027E $12.50 × 14×
    "XBULL": {"price": 225.00, "label": "XBULL"},  # 14-15% ROTCE; TBV $115 × 2.0× = $230
}

SIGNAL_CENTRES = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}

def softmax_weights(composite):
    logits = {s: -(composite - c)**2 / T for s, c in SIGNAL_CENTRES.items()}
    max_l  = max(logits.values())
    raw    = {s: math.exp(v - max_l) for s, v in logits.items()}
    total  = sum(raw.values())
    return {s: v / total for s, v in raw.items()}

def expected_price(composite):
    w = softmax_weights(composite)
    return sum(w[s] * SCENARIOS[s]["price"] for s in SCENARIOS)

def infer_composite(target_price, lo=1.0, hi=4.0, iterations=60):
    for _ in range(iterations):
        mid = (lo + hi) / 2
        if expected_price(mid) < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

market_composite = infer_composite(CURRENT_PRICE)

# ── SCA (Signal Catalyst Adjustments) ────────────────────────────────────────
SCA_FACTORS = [
    # Tailwinds
    {"label": "Massive buyback programme ($20B; $6.3B in Q1 alone)",
     "rating": +0.35, "weight": 0.20,
     "note": "Citigroup is close to completing a $20 billion share buyback plan. In Q1 2026 alone,"
             " it repurchased $6.3B = ~50M shares = 3% of float in ONE QUARTER. Annualised 12%."
             " At $73-126 purchase prices, these buybacks retire shares at deep discounts to TBV"
             " ($99.01). TBV per share is GROWING rapidly as cheap shares are retired. By end 2026,"
             " ~$15-20 per share of TBV accretion from buybacks is plausible."},
    {"label": "Q1 2026 ROTCE 13.1% — already exceeds 10-11% target",
     "rating": +0.30, "weight": 0.15,
     "note": "Citigroup's own 2026 guidance was 10-11% ROTCE. Q1 2026 delivered 13.1% — already"
             " at the FY2027 guidance range (11-13%). Four of five businesses grew double-digits."
             " Services (+17%), Markets (+19%), Banking (+15%), Wealth (+11%) all strong."
             " Fraser stated 14-15% ROTCE medium-term (2029-2031) — Q1 suggests the trajectory"
             " is faster than guided."},
    {"label": "P/TBV 1.27× — steepest discount to peers in US large-cap banking",
     "rating": +0.25, "weight": 0.15,
     "note": "At 1.27× TBV, Citi is the cheapest major US bank by book value:  JPM 2.83×, GS 2.94×,"
             " MS 3.89×, BAC 1.77×, WFC 1.77×. Gordon Growth at Q1 ROTCE 13.1% → warranted"
             " 1.82× TBV = $180. Even at the company's conservative 10.5% 2026 target →"
             " warranted 1.30× TBV = $128.71 ≈ current. Once Citi proves 12%+ sustained ROTCE,"
             " P/TBV should converge toward BAC/WFC range (1.7-1.8×) = $168-178."},
    # Headwinds
    {"label": "Near 52-wk high after +63% rally — easy money made",
     "rating": -0.35, "weight": 0.25,
     "note": "The stock rallied from $73.49 (BUY at ratio_b 0.37×) to $126.20 (+63% in 12 months)."
             " At the 52-wk low, Citi was trading at 7× forward earnings — the entry was obvious."
             " Now at $126 (12× forward), the stock is at HOLD/TRIM. Near 52-wk high $135.29."
             " The re-rating from 'deeply beaten-down SIFI' to 'recovering franchise' is largely"
             " complete. The next leg requires ROTCE proof, not just transformation announcement."},
    {"label": "Execution risk / regulatory complexity remains",
     "rating": -0.30, "weight": 0.25,
     "note": "OCC 2020 consent order (data architecture, risk management) remains a constraint."
             " Citi has the most complex global structure of any US bank: 100+ countries, 200+"
             " legal entities, interbank exposures. Fraser's transformation is real but Citi has"
             " disappointed investors on execution for 15+ years. Two declined EPS years (2024, 2025)"
             " remind the market that Citi's stated targets have historically been missed or delayed."
             " Cost savings targets ($2.5B by 2026) need to materialise alongside revenue growth."},
    {"label": "Global macro / tariff exposure (EM + trade finance)",
     "rating": -0.15, "weight": 0.20,
     "note": "Citi's Services (TTS/Securities Services) is the world's largest transaction bank:"
             " $1T+ daily flows in 100+ currencies. This is GREAT in a globalised world but a"
             " headwind in a tariff/deglobalisation scenario. Trade finance volumes correlate with"
             " global trade — tariffs reduce trade → reduce TTS revenue. FY2026 guidance assumed"
             " benign global trade; escalating tariff war is downside risk."},
]

sca_raw = sum(f["rating"] * f["weight"] for f in SCA_FACTORS)
sca_adj = sca_raw / 2.0

adj_composite = market_composite + sca_adj

# ── Bank-specific metrics ─────────────────────────────────────────────────────
TBV_PER_SHARE  = 99.01    # Q1 2026 tangible book value per common share (confirmed)
CET1_RATIO     = 12.7     # Q1 2026 CET1 Standardized; 110bps above regulatory requirement incl. buffer
ROTCE_Q1_2026  = 13.1     # Q1 2026 ROTCE (exceeds 10-11% FY2026 guidance target)
ROTCE_TARGET_26 = 10.5    # Midpoint of FY2026 company guidance (10-11% ROTCE)
ROTCE_TARGET_MT = 14.5    # Medium-term ROTCE target 2029-2031 (midpoint of 14-15% range)
BUYBACK_Q1_B   = 6.3      # Q1 2026 share repurchases ($B; part of $20B programme)

# ── Output ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    w = softmax_weights(adj_composite)
    exp_p = expected_price(adj_composite)

    # Gordon Growth model
    Ke, g = 9.0, 4.0
    warranted_q1      = (ROTCE_Q1_2026   - g) / (Ke - g)
    warranted_tgt26   = (ROTCE_TARGET_26 - g) / (Ke - g)
    warranted_tgtmt   = (ROTCE_TARGET_MT - g) / (Ke - g)
    wpx_q1    = warranted_q1    * TBV_PER_SHARE
    wpx_tgt26 = warranted_tgt26 * TBV_PER_SHARE
    wpx_tgtmt = warranted_tgtmt * TBV_PER_SHARE
    current_ptbv = CURRENT_PRICE / TBV_PER_SHARE

    # ── PART 1: Framework ─────────────────────────────────────────────────────
    part1 = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  BottomUp Risk/Reward Analyzer — Analytical Framework                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
This tool applies a structured bottom-up framework to estimate the risk/reward
profile of individual equities over a 2-year investment horizon.  It is NOT a
trading signal or a price prediction — it is a disciplined lens for sizing
positions relative to the gap between structural downside (EPP) and consensus
upside (Method B).

KEY METRICS DEFINED
  EPP  (Earnings Power Price)   = EPS_trough × min-viable trough P/E
       The structural floor: the price the market should not sustainably
       breach even in a severe downturn, because earnings power remains.

  Method B price                = Consensus 2-yr EPS × exit P/E assumption
       The ceiling under the base/bull scenario — what the stock is worth
       if consensus plays out and the market re-rates to a reasonable multiple.

  Ratio B (PRIMARY SIGNAL)      = (Current − EPP) / (Method B − Current)
       How much downside risk are you taking per unit of upside potential?
       < 0.75 = BUY · 0.75–1.10 = ACCUMULATE · 1.10–1.75 = WATCHLIST
       1.75–2.50 = HOLD/TRIM · > 2.50 = AVOID

  Composite score               = market-implied scenario blend (1.0–4.0 scale)
       Inferred by back-solving the softmax price engine against today's price.
       1.0 = deep BEAR | 2.0 = BASE | 3.0 = BULL | 4.0 = XBULL
       SCA adjustments shift the composite to reflect non-price catalysts.

SIGNAL TABLE
  ◉ BUY        Ratio B < 0.75   — asymmetric upside; margin of safety present
  ◎ ACCUMULATE Ratio B 0.75–1.10 — favourable risk/reward; build position
  ◐ WATCHLIST  Ratio B 1.10–1.75 — balanced; monitor for entry improvement
  ▷ HOLD/TRIM  Ratio B 1.75–2.50 — upside limited vs downside; reduce on strength
  ✕ AVOID      Ratio B > 2.50   — risk/reward deeply unfavourable at current price
"""

    # ── PART 2: Analyst commentary ────────────────────────────────────────────
    part2 = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  C  |  Citigroup Inc.  |  ▷ HOLD/TRIM                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

SNAPSHOT  (as of 2026-05-26)
  Price         ${CURRENT_PRICE:.2f}   52-wk range  ${PRICE_52W_LOW:.2f} – ${PRICE_52W_HIGH:.2f}
  Shares        {SHARES_M:.1f}M       Mkt cap      ~$215.2B
  Dividend      ${DIVIDEND_ANN:.2f}/yr       Yield        ~{DIVIDEND_ANN/CURRENT_PRICE*100:.2f}%
  FY2026E EPS   ${EPS_NOW:.2f}          FW P/E       {CURRENT_PRICE/EPS_NOW:.1f}×
  TBV/share     ${TBV_PER_SHARE:.2f}         P/TBV        {current_ptbv:.3f}×
  CET1          {CET1_RATIO:.1f}%           ROTCE Q1     {ROTCE_Q1_2026:.1f}%  (target: {ROTCE_TARGET_26:.1f}%)
  EPP floor     ${EPP:.2f}         Ratio B      {ratio_b:.3f}×  →  ▷ HOLD/TRIM

THE TRANSFORMATION STORY: THREE YEARS OF PAIN, NOW PROVING OUT
From 2022 to 2025, Citigroup's reported EPS DECLINED every year:
  FY2022: $7.00  →  FY2023: $5.78  →  FY2024: $5.14  →  FY2025: $4.61

This made no sense for a bank with $24.6B quarterly revenue and a transforming
franchise — until you understand the charges:
  • Q4 2023: FDIC special assessment ($2.7B) + Argentina ($880M) + Russia reserves
  • FY2024: ~$2.5B restructuring (severance, office closures, ~20,000 jobs cut)
  • FY2025: Legal settlements, consent order remediation, portfolio sales at losses

FY2026 is the FIRST clean year.  Q1 2026 delivered the proof:
  Revenue: $24.6B (+14% YoY) — best quarter in a decade
  Net income: $5.8B (+42%)
  EPS: $3.06 (beat $2.64 consensus by 16%)
  ROTCE: 13.1% — already ABOVE the full-year 10-11% guidance

Jane Fraser's transformation is working.  The question is: has the stock already priced it in?

THE GORDAN GROWTH INFLECTION — AND WHY IT MATTERS
  Warranted P/TBV = (ROTCE − g) / (Ke − g)   [Ke={Ke:.0f}%, g={g:.0f}%]

  At Q1 2026 ROTCE {ROTCE_Q1_2026:.1f}%        → warranted {warranted_q1:.2f}× TBV = ${wpx_q1:.2f}
  At FY2026 target {ROTCE_TARGET_26:.1f}%   → warranted {warranted_tgt26:.2f}× TBV = ${wpx_tgt26:.2f}  ← roughly current price
  At medium-term {ROTCE_TARGET_MT:.1f}% target → warranted {warranted_tgtmt:.2f}× TBV = ${wpx_tgtmt:.2f}  (+{(wpx_tgtmt/CURRENT_PRICE-1)*100:.0f}% upside)

  Current P/TBV = {current_ptbv:.3f}×

  KEY INSIGHT: At Citi's OWN conservative 2026 ROTCE target (10.5%), Gordon Growth
  implies fair value ~$128 ≈ CURRENT PRICE.  The stock is fairly valued at the stated target.
  To generate meaningful upside, Citi needs to EXCEED 10-11% ROTCE — which Q1 2026 (13.1%)
  suggests is already happening.  Medium-term target 14.5% ROTCE implies $215 = +70% upside.

  Unlike GS ($1,000 at P/TBV above warranted) or MS ($201 above warranted), Citi is still
  BELOW Gordon Growth fair value at Q1 ROTCE (1.27× vs warranted 1.82×).  This is the
  structural undervaluation: the market doesn't believe Q1 ROTCE is sustainable.

THE VALUATION PARADOX: CHEAPEST MAJOR US BANK, FOR GOOD REASON
  P/TBV comparison  (all using current prices):
    JPM:  2.83×  ·  GS: 2.94×  ·  MS: 3.89×
    BAC:  1.77×  ·  WFC: 1.77×
    CITI: 1.27×   ← by far the cheapest

  Citi's discount to peers reflects 15 years of underdelivering on return targets.
  The market applies a "show me" premium — it will not re-rate Citi to BAC/WFC P/TBV
  levels until ROTCE improvement is demonstrated over multiple quarters, not just one.

  The BULL CASE: if ROTCE converges toward BAC/WFC at 14-16% by 2028-2029, and TBV
  grows from $99 to $115 via retained earnings + buybacks, P/TBV would converge
  toward 1.8-2.0× = $207-230.  That's the XBULL scenario.

  The BEAR CASE: execution stumbles again; ROTCE stays at 10-11%; P/TBV stays at
  1.3×; stock returns to mid-$90s.

WHY HOLD/TRIM, NOT BUY
The entry was at $73-90 a year ago (ratio_b 0.37-0.65×, a clear BUY).  The stock is up
63% since then.  At $126:
  1. Still cheap vs peers, but fairly valued at own target ROTCE
  2. Near 52-wk high ($126 vs $135 peak); only 6.7% below high
  3. Analyst consensus "Buy" but PT only $146-147 (+16% from here)
  4. Method B $175 (+38.7%) exists but requires ROTCE > 12% sustained + multiple expansion
  5. Execution risk remains real: OCC consent order, global complexity, cost targets

Best re-entry: ACCUMULATE $100-115 (if macro scare / de-risking creates another dip).
WATCHLIST near $115-125.  Reduce on any push toward $135-145 (approaching AVOID territory).

BUYBACK ENGINE (key differentiated positive)
$20B share repurchase programme, close to completion.  Q1 2026: $6.3B = ~50M shares retired.
From ~1,900M shares in 2022 to 1,706M today = ~200M shares retired at ~$65-100 avg.
At $99 TBV, buying back at $126 is DILUTIVE to TBV per share — this is the one concern.
But relative to peers who barely buy back (JPM paused, WFC modest), Citi's aggression
signals CEO confidence that the stock remains undervalued.
"""

    # ── PART 3: Numbers & signals ─────────────────────────────────────────────
    part3 = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  C — Numbers & Signals                                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

EPS HISTORY (GAAP diluted)
  FY2022   ${EPS_HISTORY['FY2022']:>6.2f}   Pre-transformation; $7.11 continuing + ($0.12) discontinued ops
  FY2023   ${EPS_HISTORY['FY2023']:>6.2f}   Q4 charges: FDIC $2.7B + Argentina $0.9B + Russia; EPS -17%
  FY2024   ${EPS_HISTORY['FY2024']:>6.2f}   Restructuring drag: ~20K jobs cut; divestitures; OCC remediation
  FY2025   ${EPS_HISTORY['FY2025']:>6.2f}   Last transformation year; final cleanup; ROTCE ~7-8% underlying
  FY2026E  ${EPS_NOW:>6.2f}   CLEAN year: Q1 actual $3.06 (+16% beat); post-transformation run-rate
  FY2027E  ${CONS_EPS_2YR:>6.2f}   ROTCE 12-13% path; Services+Markets+Wealth compounding

EPP — STRUCTURAL FLOOR
  EPS_trough  = ${EPS_TROUGH:.2f}   (severe recession: NCOs spike, provisions double; ≈ worst recent trough)
  EPP_min_PE  = {EPP_MIN_PE}×       (SIFI commercial bank floor; complex global structure discounted vs JPM)
  EPP         = ${EPP:.2f}   (= ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×)
  Gap to EPP  = {(CURRENT_PRICE/EPP - 1)*100:.1f}% above floor  (current ${CURRENT_PRICE:.0f} is {CURRENT_PRICE/EPP:.2f}× EPP)

METHOD B — 2-YEAR UPSIDE CEILING
  Consensus EPS (FY2027E)  = ${CONS_EPS_2YR:.2f}   (ROTCE 12-13% path; Fraser +16% growth yr-on-yr)
  Exit P/E assumption      = {CONS_EXIT_PE}×   (re-rate toward BAC/WFC at 14× if sustained 12%+ ROTCE)
  Method B price           = ${price_b:.2f}   (+{(price_b/CURRENT_PRICE-1)*100:.1f}% from current)

RATIO B (PRIMARY SIGNAL)
  Ratio B = (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})
          = {CURRENT_PRICE-EPP:.2f} / {price_b-CURRENT_PRICE:.2f}
          = {ratio_b:.3f}×   →   ▷ HOLD/TRIM  (range: 1.75–2.50×)

  52-wk low  $73.49  →  ratio_b {(PRICE_52W_LOW-EPP)/(price_b-PRICE_52W_LOW):.3f}×  →  ◉ BUY  (was a clear entry a year ago)
  Current    $126.20 →  ratio_b {ratio_b:.3f}×  →  ▷ HOLD/TRIM  (re-rating largely complete)
  52-wk high $135.29 →  ratio_b {(PRICE_52W_HIGH-EPP)/(price_b-PRICE_52W_HIGH):.3f}×  →  ✕ AVOID  (at ATH, AVOID territory)

GORDON GROWTH MODEL  (Warranted P/TBV = (ROTCE − g) / (Ke − g);  Ke={Ke:.0f}%, g={g:.0f}%)
  At Q1 2026 ROTCE  {ROTCE_Q1_2026:.1f}%   → warranted {warranted_q1:.2f}× TBV = ${wpx_q1:.2f}   (above current — cheap!)
  At FY2026 target  {ROTCE_TARGET_26:.1f}%  → warranted {warranted_tgt26:.2f}× TBV = ${wpx_tgt26:.2f}  (≈ current price)
  At medium-term    {ROTCE_TARGET_MT:.1f}%  → warranted {warranted_tgtmt:.2f}× TBV = ${wpx_tgtmt:.2f}  (+{(wpx_tgtmt/CURRENT_PRICE-1)*100:.0f}% upside!)

  Current P/TBV = {current_ptbv:.3f}×.  Still BELOW Gordon Growth warranted at Q1 ROTCE.

SCENARIO ANALYSIS
  BEAR   ${SCENARIOS['BEAR']['price']:>7.2f}   EPP floor; severe recession; Citi's global exposure amplifies macro
  BASE   ${SCENARIOS['BASE']['price']:>7.2f}   Analyst PT zone; FY2026E $10.50 × 13.6× = $143; fair value at target
  BULL   ${SCENARIOS['BULL']['price']:>7.2f}   Method B; FY2027E $12.50 × 14×; ROTCE 12-13% sustained
  XBULL  ${SCENARIOS['XBULL']['price']:>7.2f}   Medium-term ROTCE 14-15%; TBV $115 × 2.0× = $230; peer re-rating

SOFTMAX COMPOSITE ENGINE
  Market composite (inferred)  =  {market_composite:.3f}
  (Market pricing C between BASE and BULL — reflecting transformation progress)

SCA — SIGNAL CATALYST ADJUSTMENTS
{"".join(f"  {f['label'][:50]:<50}  {f['rating']:+.2f} × {f['weight']:.2f}  =  {f['rating']*f['weight']:+.4f}" + chr(10) for f in SCA_FACTORS)}
  sca_raw     =  {sca_raw:+.4f}
  sca_adj     =  {sca_adj:+.4f}  (= sca_raw / 2.0)
  adj_composite  =  {market_composite:.3f}  +  {sca_adj:+.4f}  =  {adj_composite:.3f}

SOFTMAX SCENARIO WEIGHTS  (at adj_composite = {adj_composite:.3f})
{"".join(f"  {s:<6}  {w[s]*100:5.1f}%   ${SCENARIOS[s]['price']:.2f}" + chr(10) for s in ['BEAR','BASE','BULL','XBULL'])}
  Expected price (probability-weighted)  =  ${exp_p:.2f}

BANK METRICS
  TBV per share (Q1 2026)    =  ${TBV_PER_SHARE:.2f}   P/TBV = {current_ptbv:.3f}×  (cheapest US SIFI)
  ROTCE Q1 2026              =  {ROTCE_Q1_2026:.1f}%   (beats 10-11% FY2026 target already)
  FY2026 ROTCE target        =  {ROTCE_TARGET_26:.1f}%   (company guidance; interim milestone)
  Medium-term ROTCE target   =  {ROTCE_TARGET_MT:.1f}%   (2029-2031; "not a destination, a waypoint")
  CET1 ratio (Q1 2026)       =  {CET1_RATIO:.1f}%   (110bps above regulatory requirement incl. buffer)
  Q1 2026 revenue            =  $24.6B   (+14% YoY; best quarter in a decade)
  Q1 2026 buybacks           =  ${BUYBACK_Q1_B:.1f}B   (~50M shares; ~3% float in one quarter)
  Analyst avg PT             =  $146–148  (+{(147/CURRENT_PRICE-1)*100:.0f}% from current); "Buy" consensus

SIGNAL ENTRY GUIDE
  ✕ AVOID      above  $142  (ratio_b > 2.50×; at 52-wk high $135 = 2.50×)
  ▷ HOLD/TRIM  $125 – $142  (current; ratio_b 1.75–2.50×)  ← HERE
  ◐ WATCHLIST  $113 – $125  (ratio_b 1.10–1.75×)
  ◎ ACCUMULATE $100 – $113  (ratio_b 0.75–1.10×)
  ◉ BUY        below  $100  (ratio_b < 0.75×; near or below TBV = structural floor)

  52-wk low $73.49 was deep BUY (ratio_b 0.37×); +63% to current HOLD.
  Best re-entry: ACCUMULATE $100-113 on next macro dislocation.
  Watch: Investor Day guidance update; Q2 2026 ROTCE confirmation.
"""

    print(part1)
    print(part2)
    print(part3)
