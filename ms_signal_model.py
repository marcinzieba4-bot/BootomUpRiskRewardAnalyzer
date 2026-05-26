"""
Morgan Stanley  (MS)
BottomUp Risk/Reward Analyzer — Signal Model
"""
import math

# ── Core inputs ──────────────────────────────────────────────────────────────
TICKER        = "MS"
COMPANY       = "Morgan Stanley"
SECTOR        = "Investment Banking · Global Markets (Trading) · Wealth Management (~$7T AUM) · Investment Management"

CURRENT_PRICE  = 200.92   # MS — fetched via web search, 2026-05-26
                            # Intraday range $200.63–$203.09; all-time high $201.03 (May 22, 2026)
                            # Market cap $317.11B; P/E 18.21× (trailing)
PRICE_52W_LOW  = 123.88   # April 2025 tariff-panic low (+62.2% to current ATH)
PRICE_52W_HIGH = 203.09   # Today's intraday high = all-time high territory
SHARES_M       = 1578.0   # Derived: mkt cap $317.11B / $200.92; buyback $1.75B Q1 2026 (~8.7M shr)
DIVIDEND_ANN   = 4.00     # $1.00/quarter (raised to $1.00 for Q1 2026; 13 consecutive annual increases)
                            # Yield: 1.99% at $200.92

# ── EPS history (GAAP diluted) ────────────────────────────────────────────────
EPS_HISTORY = {
    "FY2022": 6.15,    # IB slowdown began H2 2022; market drawdown compressed AUM fees; deal backlog forming
    "FY2023": 5.18,    # TROUGH: IB fee freeze (IPO winter); AUM compressed; WM revenue pressure;
                        # NOT a recession — this was a non-recessionary trough. -15.8% from FY2022.
    "FY2024": 8.05,    # +55.4% recovery: IB fee rebound, markets recovery, WM AUM inflows resumed
    "FY2025": 10.21,   # +26.8% record; Q4 2025: EPS $2.22; ROTCE ~19.5% FY average; record WM
}
EPS_NOW = 11.50   # FY2026E post-Q1 beat: Q1 actual $3.43 (vs $3.02 consensus, +13.6% beat)
                   # Q2–Q4 assumed to normalize toward FY2025 quarterly average (~$2.60/qtr)
                   # → FY2026E: $3.43 + 3 × $2.69 = ~$11.50; market pricing ~$11 (18.2× implied FW P/E)

# ── EPP (Earnings Power Price) — structural floor ────────────────────────────
EPS_TROUGH  = 5.50    # Mild-to-moderate recession: IB fees collapse, AUM falls ~25%, WM fee income
                        # drops proportionally. FY2023 non-recession trough was $5.18 — a real recession
                        # would likely be slightly worse ($4-6 range). $5.50 is 7% above FY2023 trough,
                        # reflecting WM's structural growth (client assets ~$7T vs ~$4T in 2023) partially
                        # offsetting IB cyclicality. 2008 crisis: MS posted EPS ~($3) — but the firm is
                        # now fundamentally different (WM is ~40% of revenue vs ~15% in 2008).
EPP_MIN_PE  = 12      # MS trough multiple: higher than pure IB (GS 11×) because Wealth Management
                        # provides recurring AUM fee income even in downturns. During FY2023 trough,
                        # MS traded at roughly 12–16× forward — even in an IB winter, WM anchor
                        # prevents the multiple from collapsing to bank-level lows (9×).
                        # 12× = minimum franchise value floor for the WM+IB combination.
EPP         = EPS_TROUGH * EPP_MIN_PE   # = $66.00

# ── Method B (2-year normalised upside ceiling) ───────────────────────────────
CONS_EPS_2YR  = 14.00   # FY2027E adj EPS estimate: pre-Q1 consensus $12.42 revised upward post-beat;
                          # $14.00 assumes Q1 2026 momentum partially sustained, WM AUM compounding,
                          # IB fee cycle continues. Represents ~22% growth from FY2026E $11.50.
CONS_EXIT_PE  = 17        # MS has historically traded 13–18× EPS in normal bull markets.
                          # 17× reflects WM premium vs pure IB (GS at 18× given pure IB optionality
                          # premium). MS at 17× = 1× turn premium over GS for recurring WM income.
                          # Conservative vs the 19-20× peak in 2021; appropriate for sustained
                          # normalised earnings power scenario.
price_b = CONS_EPS_2YR * CONS_EXIT_PE   # = $238.00

# ── Primary signal: Ratio B ───────────────────────────────────────────────────
ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
# = (200.92 - 66.00) / (238.00 - 200.92) = 134.92 / 37.08 = 3.638×
# Signal: ✕ AVOID (> 2.50×)

# ── Softmax composite engine ──────────────────────────────────────────────────
T = 0.60
SCENARIOS = {
    "BEAR":  {"price":  66.00,  "label": "BEAR"},   # EPP floor; severe recession / credit crisis
    "BASE":  {"price": 187.00,  "label": "BASE"},   # FY2026E $11.0 × 17× = $187; normalized year
    "BULL":  {"price": 238.00,  "label": "BULL"},   # Method B; FY2027E $14 × 17×
    "XBULL": {"price": 300.00,  "label": "XBULL"},  # Premium WM re-rating; $14 × 21.4×
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
    {"label": "Wealth Management secular compounding",
     "rating": +0.30, "weight": 0.20,
     "note": "MS manages ~$7T in client assets. Net New Assets $118B in Q1 2026 alone;"
             " fee-based asset flows $54B. As the largest US wealth manager, AUM grows"
             " through client recruitment (4,000+ FAs added via E*TRADE), market appreciation,"
             " and generational wealth transfer. WM fees are ~40% of revenue and highly recurring."},
    {"label": "E*TRADE + digital WM platform compounding",
     "rating": +0.25, "weight": 0.15,
     "note": "E*TRADE (acquired 2020 for $13B) has been integrated into MS's WM ecosystem."
             " Workplace channel (equity compensation, 401k) + self-directed retail growing."
             " NNA from workplace $54B Q1 2026. Digital-first WM acquisition is a multi-decade"
             " compounding asset that didn't exist in prior IB cycle."},
    {"label": "Integrated WM+IB model = full client lifecycle",
     "rating": +0.20, "weight": 0.15,
     "note": "CEO Ted Pick's strategy: WM provides recurring income to smooth IB cyclicality."
             " When founders exit (IPO/M&A), MS captures the wealth management mandate."
             " When WM clients need credit/derivatives, IB provides it. The cross-sell loop"
             " is a structural competitive advantage vs standalone IB (GS, Lazard)."},
    # Headwinds
    {"label": "ATH valuation / analyst PTs below current price",
     "rating": -0.40, "weight": 0.25,
     "note": "MS at ALL-TIME HIGH ($201.03 May 22; today $200.92). Analyst consensus PT:"
             " $176–190 — BELOW current price. 21 analysts average $190; 12-analyst Buy"
             " consensus averages $176. Stock has run BEYOND analyst fair value. Gordon Growth"
             " at FY2025 normalized ROTCE 20% → warranted P/TBV 3.20× = $165 vs current 3.89×."
             " Same pattern as GS: market pricing unsustainable Q1 ROTCEs as permanent."},
    {"label": "Q1 2026 exceptional / IB + trading cyclicality",
     "rating": -0.35, "weight": 0.25,
     "note": "Q1 2026 was exceptional: ROTCE 27.1% (above 20% target), equities $5.1B+ (record),"
             " driven by tariff-driven volatility. IB cyclicality is extreme: FY2023 EPS $5.18"
             " (-16% from $6.15) without a recession. Q1 2026 record trading is unlikely to be"
             " sustained — Goldman Sachs and Morgan Stanley both benefited from abnormal Q1"
             " volatility. Normalizing Q2-Q4 back to FY2025 rates implies FW EPS ~$11.50,"
             " not the $13.72 implied by annualizing Q1."},
    {"label": "AUM multiple compression / rate environment",
     "rating": -0.20, "weight": 0.20,
     "note": "WM revenue is AUM-based. Higher rates hurt two ways: (1) equity market multiple"
             " compression reduces AUM base; (2) clients rotate from equities to cash/bonds."
             " MS earns ~50bps on $7T AUM → each 10% AUM decline = ~$350M revenue headwind."
             " Rising rates also increase interest expense on MS's $1T+ balance sheet."},
]

sca_raw = sum(f["rating"] * f["weight"] for f in SCA_FACTORS)
sca_adj = sca_raw / 2.0

adj_composite = market_composite + sca_adj

# ── Bank / financial metrics (MS-specific) ───────────────────────────────────
TBV_PER_SHARE  = 51.58    # Q1 2026 tangible book value per common share (up from $50.00 prior)
BOOK_PER_SHARE = 66.18    # Q1 2026 book value per common share
ROTCE_Q1_2026  = 27.1     # Q1 2026 ROTCE (record; 20% target exceeded; tariff-driven trading spike)
ROTCE_FY2025   = 19.5     # FY2025 ROTCE estimate based on $10.21 EPS / ~$52.4 avg TBV
CET1_RATIO     = 15.1     # Q1 2026 CET1 (Standardized); regulatory minimum 11.8% → +330bps buffer
AUM_WEALTH_T   = 7.0      # Wealth Management client assets ~$7 trillion
NNA_Q1_2026    = 118.0    # Net New Assets Q1 2026 ($B)

# ── Output ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    w = softmax_weights(adj_composite)
    exp_p = expected_price(adj_composite)

    # Gordon Growth model
    Ke, g = 9.0, 4.0
    warranted_tbv_q1    = (ROTCE_Q1_2026 - g) / (Ke - g)
    warranted_tbv_fy25  = (ROTCE_FY2025  - g) / (Ke - g)
    warranted_tbv_recess = (12.0          - g) / (Ke - g)
    warranted_px_q1     = warranted_tbv_q1    * TBV_PER_SHARE
    warranted_px_fy25   = warranted_tbv_fy25  * TBV_PER_SHARE
    warranted_px_recess = warranted_tbv_recess * TBV_PER_SHARE
    current_ptbv        = CURRENT_PRICE / TBV_PER_SHARE

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
║  MS  |  Morgan Stanley  |  ✕ AVOID                                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

SNAPSHOT  (as of 2026-05-26)
  Price         ${CURRENT_PRICE:,.2f}   52-wk range  ${PRICE_52W_LOW:.2f} – ${PRICE_52W_HIGH:.2f}
  Shares        ~{SHARES_M:.0f}M       Mkt cap      ~$317.1B
  Dividend      ${DIVIDEND_ANN:.2f}/yr      Yield        ~{DIVIDEND_ANN/CURRENT_PRICE*100:.2f}%
  FY2026E EPS   ${EPS_NOW:.2f}          FW P/E       {CURRENT_PRICE/EPS_NOW:.1f}×
  TBV/share     ${TBV_PER_SHARE:.2f}        P/TBV        {current_ptbv:.2f}×
  EPP floor     ${EPP:.2f}          Ratio B      {ratio_b:.2f}×  →  ✕ AVOID

THE BUSINESS: IB + WEALTH MANAGEMENT HYBRID
Morgan Stanley is a $317B financial conglomerate that operates across three
complementary segments, each with different cyclicality and multiple characteristics:

Institutional Securities (~35% of revenue, highest margin, most cyclical):
  Investment Banking (M&A advisory, equity/debt underwriting), Equities sales &
  trading, Fixed Income sales & trading.  Q1 2026: record $10.7B Institutional
  Securities revenue; Equities surpassed $5.1B for the first time.  Driven by
  tariff-related client activity and market volatility — a structurally exceptional
  quarter.  IB cycle is extreme: FY2023 EPS $5.18 (-16% YoY) without a recession.

Wealth Management (~40% of revenue, highly recurring):
  ~$7 trillion in client assets.  Revenue is primarily fee-based (% of AUM) plus
  net interest income on client cash balances.  E*TRADE acquisition (2020, $13B)
  added self-directed and workplace equity compensation channels.  NNA $118B Q1 2026;
  fee-based flows $54B.  This is the business that distinguishes MS from Goldman Sachs:
  GS has abandoned Consumer/Marcus; MS's WM is the world's largest retail brokerage.

Investment Management (~25% of revenue):
  Eaton Vance, Parametric, AIP (alternatives).  AUM ~$1.6T; institutional and
  high-net-worth mandates.  Less cyclical than IS; revenue primarily management fees.

THE Q1 2026 EXCEPTIONAL QUARTER — AND WHY IT DOESN'T JUSTIFY THE PRICE
Q1 2026 metrics were extraordinary: ROTCE 27.1% (well above 20% target), EPS $3.43
(+13.6% beat vs $3.02 consensus), revenue $20.6B (+16% YoY, record).

But this was driven by ABNORMAL market conditions:
  1. Tariff shock (April 2025 rebound still in the Q1 base; new tariff announcements
     driving client hedging/repositioning in Q1 2026) → Equities $5.1B+ record volume
  2. Rate volatility → Fixed Income elevated
  3. IB fee cycle at peak (best IB environment since 2021)

ROTCE 27.1% in a single quarter cannot be projected forward.  The firm's own FY2025
full-year ROTCE was ~19.5%.  At FY2025 ROTCE, the Gordon Growth warranted P/TBV is
only {warranted_tbv_fy25:.2f}× → implied price ${warranted_px_fy25:.2f} — BELOW current price.

GORDON GROWTH TRAP (same pattern as GS, JPM, BAC at peak cycle)
  Warranted P/TBV = (ROTCE − g) / (Ke − g)   [Ke=9%, g=4%]

  At Q1 2026 ROTCE {ROTCE_Q1_2026}%   → warranted {warranted_tbv_q1:.2f}× = ${warranted_px_q1:.2f}  (above current — looks cheap)
  At FY2025 ROTCE  {ROTCE_FY2025}%   → warranted {warranted_tbv_fy25:.2f}× = ${warranted_px_fy25:.2f}  (BELOW current — expensive)
  At recession ROTCE 12%  → warranted {warranted_tbv_recess:.2f}× = ${warranted_px_recess:.2f}  (-{(1-warranted_px_recess/CURRENT_PRICE)*100:.0f}% from here)

  Current P/TBV = {current_ptbv:.2f}×.  The stock is priced above FY2025-normalized fair value
  and requires sustained Q1-level ROTCE to justify the current multiple.  As with GS in
  Q1 2026 and BAC/JPM at various cycle peaks, the market is pricing the peak as permanent.

THE DEFINING SIGNAL: ANALYSTS ARE BELOW CURRENT PRICE
Avg analyst 12-month price target: $176–$190 — BELOW the current stock price of ${CURRENT_PRICE:.2f}.
Of 21 analysts, the average PT is $190.33; a subset Buy consensus averages $176.
The stock has RUN PAST analyst fair value.  This is the same pattern as Goldman Sachs
($1,000 with analyst avg PT $901-918) and a classic sign of a stock priced for perfection.

52-WEEK RANGE PERSPECTIVE
  52-wk low   $123.88  (Apr 2025 tariff panic)  →  ratio_b {(PRICE_52W_LOW-EPP)/(price_b-PRICE_52W_LOW):.2f}×  →  ◉ BUY
  Current     $200.92  (near all-time high)      →  ratio_b {ratio_b:.2f}×  →  ✕ AVOID
  52-wk high  $203.09  (today's intraday)        →  ratio_b {(PRICE_52W_HIGH-EPP)/(price_b-PRICE_52W_HIGH):.2f}×  →  ✕ AVOID

MS was a BUY 12 months ago at its 52-wk low ($123.88).  The stock has rallied +62%
to an all-time high.  The risk/reward has rotated from highly favourable to highly
unfavourable in a single year.  The fundamentals are excellent — the price is not.

THE BULL CASE (why the stock might stay elevated)
  1. WM AUM compounding: $7T × 50bps fees = $35B annual revenue run-rate growing
     as AUM grows organically.  The WM multiple is structurally higher than IB.
  2. E*TRADE workplace growth: employer equity compensation plans locked in 5-10yr
     contracts; each IPO/vesting event brings AUM into MS ecosystem.
  3. Ted Pick's unified firm: cross-sell between IS and WM (founder sells company
     via IB → MS manages proceeds via WM) is the most powerful client flywheel in finance.
  4. CET1 15.1% = fortress capital; $1.75B quarterly buybacks will continue.
  5. IB super-cycle: if dealmaking/IPO activity stays elevated through 2027, FY2027E
     $14+ EPS is achievable, and at 17× that's $238.

RISK FACTORS
  IB cyclicality:  FY2023 EPS $5.18 occurred in a non-recessionary environment.
  A real recession would likely produce $3-5 EPS — at 12× that's $36–60, far below
  the current $200.92.

  AUM market risk:  $7T in client assets. A 25% market drawdown = AUM down $1.75T →
  ~$875M annual WM revenue loss (assuming 50bps avg fee).

  Rising rate headwind:  MS borrows at scale; higher rates increase funding costs.
  AUM-based fees also compress if equities re-rate lower due to sustained high rates.
"""

    # ── PART 3: Numbers & signals ─────────────────────────────────────────────
    part3 = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  MS — Numbers & Signals                                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

EPS HISTORY (GAAP diluted)
  FY2022   ${EPS_HISTORY['FY2022']:>6.2f}   IB slowdown begins H2; market compression starts
  FY2023   ${EPS_HISTORY['FY2023']:>6.2f}   TROUGH (non-recession): IB freeze + AUM compression; -15.8% YoY
  FY2024   ${EPS_HISTORY['FY2024']:>6.2f}   Recovery: +55.4% YoY; IB rebound, markets recovery
  FY2025   ${EPS_HISTORY['FY2025']:>6.2f}   Record: +26.8% YoY; ROTCE ~19.5% FY avg; NNA strong
  FY2026E  ${EPS_NOW:>6.2f}   Q1 actual $3.43 (record); Q2–Q4 normalize ~$2.69/qtr
  FY2027E  ${CONS_EPS_2YR:>6.2f}   Consensus post-Q1 revision; +21.7% from FY2026E

EPP — STRUCTURAL FLOOR
  EPS_trough  = ${EPS_TROUGH:.2f}   (FY2023 non-recession trough $5.18; mild recession = $5-6)
  EPP_min_PE  = {EPP_MIN_PE}×       (WM anchor prevents multiple collapse to bank level 9×; FY2023 trough 12-16×)
  EPP         = ${EPP:.2f}   (= ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×)
  Gap to EPP  = {(CURRENT_PRICE/EPP - 1)*100:.1f}% above floor  (current $201 is {CURRENT_PRICE/EPP:.2f}× EPP)

METHOD B — 2-YEAR UPSIDE CEILING
  Consensus EPS (FY2027E)  = ${CONS_EPS_2YR:.2f}
  Exit P/E assumption      = {CONS_EXIT_PE}×   (WM premium: 1× turn above pure IB; 17× vs GS 18×)
  Method B price           = ${price_b:.2f}   (+{(price_b/CURRENT_PRICE-1)*100:.1f}% from current — very limited upside)

RATIO B (PRIMARY SIGNAL)
  Ratio B = (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})
          = {CURRENT_PRICE-EPP:.2f} / {price_b-CURRENT_PRICE:.2f}
          = {ratio_b:.2f}×   →   ✕ AVOID  (threshold: > 2.50×)

  Interpretation: for every $1 of upside to Method B, there is ${ratio_b:.2f} of downside to EPP floor.
  The asymmetry is decisively unfavourable at current price.

SCENARIO ANALYSIS
  BEAR   ${SCENARIOS['BEAR']['price']:>7.2f}  EPP floor; recession; AUM -25%; IB frozen; EPS $5.50 × 12×
  BASE   ${SCENARIOS['BASE']['price']:>7.2f}  FY2026E $11.0 × 17× = $187; normalized IB + WM growth
  BULL   ${SCENARIOS['BULL']['price']:>7.2f}  Method B; FY2027E $14 × 17×; sustained IB + WM compounding
  XBULL  ${SCENARIOS['XBULL']['price']:>7.2f}  WM re-rating 21.4×; $14 EPS; pure WM multiple peers

GORDON GROWTH MODEL  (Warranted P/TBV = (ROTCE − g) / (Ke − g);  Ke={Ke:.0f}%, g={g:.0f}%)
  At Q1 2026 ROTCE {ROTCE_Q1_2026:.1f}%   → warranted {warranted_tbv_q1:.2f}× TBV = ${warranted_px_q1:.2f}  (above current)
  At FY2025 ROTCE  {ROTCE_FY2025:.1f}%   → warranted {warranted_tbv_fy25:.2f}× TBV = ${warranted_px_fy25:.2f}  (BELOW current!)
  At recession ROTCE 12.0%  → warranted {warranted_tbv_recess:.2f}× TBV = ${warranted_px_recess:.2f}

  Current P/TBV = {current_ptbv:.2f}× (above FY2025-normalized fair value of {warranted_tbv_fy25:.2f}×)
  The stock requires sustained ROTCE above {ROTCE_FY2025:.1f}% to justify current valuation.

SOFTMAX COMPOSITE ENGINE
  Market composite (inferred)  =  {market_composite:.3f}
  (Market pricing MS between BASE and BULL — above BASE = price has priced in good news)

SCA — SIGNAL CATALYST ADJUSTMENTS
{"".join(f"  {f['label'][:50]:<50}  {f['rating']:+.2f} × {f['weight']:.2f}  =  {f['rating']*f['weight']:+.4f}" + chr(10) for f in SCA_FACTORS)}
  sca_raw     =  {sca_raw:+.4f}
  sca_adj     =  {sca_adj:+.4f}  (= sca_raw / 2.0)
  adj_composite  =  {market_composite:.3f}  +  {sca_adj:+.4f}  =  {adj_composite:.3f}

SOFTMAX SCENARIO WEIGHTS  (at adj_composite = {adj_composite:.3f})
{"".join(f"  {s:<6}  {w[s]*100:5.1f}%   ${SCENARIOS[s]['price']:.2f}" + chr(10) for s in ['BEAR','BASE','BULL','XBULL'])}
  Expected price (probability-weighted)  =  ${exp_p:.2f}

FINANCIAL METRICS
  TBV per share (Q1 2026)    =  ${TBV_PER_SHARE:.2f}   P/TBV = {current_ptbv:.2f}×
  Book per share (Q1 2026)   =  ${BOOK_PER_SHARE:.2f}   P/Book = {CURRENT_PRICE/BOOK_PER_SHARE:.2f}×
  ROTCE Q1 2026              =  {ROTCE_Q1_2026:.1f}%   (record; above 20% target; exceptional quarter)
  ROTCE FY2025 (est)         =  {ROTCE_FY2025:.1f}%   (normalised full-year; basis for Gordon Growth)
  CET1 ratio (Q1 2026)       =  {CET1_RATIO:.1f}%   (regulatory min 11.8%; +{CET1_RATIO-11.8:.0f}bps buffer)
  WM client assets           =  ~${AUM_WEALTH_T:.1f}T
  Net New Assets Q1 2026     =  ${NNA_Q1_2026:.0f}B
  Analyst avg PT             =  $176–$190  (BELOW current $200.92)
  Shares outstanding         =  ~{SHARES_M:.0f}M   Dividend $4.00/yr ({DIVIDEND_ANN/CURRENT_PRICE*100:.2f}% yield)

SIGNAL ENTRY GUIDE
  ✕ AVOID      above  $190  (current; ratio_b > 2.50×)  ← HERE
  ▷ HOLD/TRIM  $160 – $190  (ratio_b 1.75–2.50×)
  ◐ WATCHLIST  $140 – $160  (ratio_b 1.10–1.75×)
  ◎ ACCUMULATE $120 – $140  (ratio_b 0.75–1.10×; near FY2023 trough level)
  ◉ BUY        below  $105  (ratio_b < 0.75×; severe dislocation)

  Revisit below $155 (WATCHLIST); ACCUMULATE $120–140 (approx 52-wk low zone);
  BUY below $105 if macro deterioration creates re-entry below Gordon Growth floor.
"""

    print(part1)
    print(part2)
    print(part3)
