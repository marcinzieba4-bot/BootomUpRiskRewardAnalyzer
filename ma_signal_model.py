"""
Mastercard Incorporated (NYSE: MA) — BottomUp Risk/Reward Signal Model

SIGNAL:  ◐ WATCHLIST
RATIO B: 1.17x  (Method B $22.65 × 30× = $680; ratio 212.54/181.46 = 1.17×)
DATE:    2026-05-26

NOTE: EPS figures are non-GAAP adjusted (Mastercard's standard reporting;
excludes litigation charges, foreign currency remeasurement, certain M&A items).
Mastercard's fiscal year is the calendar year (ends Dec 31).
For direct comparison: MA forward P/E 25.6× vs V 27.5× (MA cheaper on P/E
despite similar/faster growth — see commentary for context).
"""

import math

TICKER  = "MA"
COMPANY = "Mastercard Incorporated"
SECTOR  = "Payment Networks · Value-Added Services (Cyber/Analytics/Data) · Cross-Border Payments · Open Banking"

# ── current price (Yahoo Finance, 2026-05-22; May 25 range $497.32-$504.08) ──
CURRENT_PRICE  = 498.54   # MA — fetched from Yahoo Finance, 2026-05-22
PRICE_52W_LOW  = 480.50   # recent low during April 2026 market selloff
PRICE_52W_HIGH = 601.77   # 52-week high
SHARES_M       = 884.0    # diluted shares (883.6M); aggressive buyback programme
DIVIDEND_ANN   = 3.48     # $0.87/quarter; 13 consecutive years of dividend growth

# ── EPS history — non-GAAP adjusted ─────────────────────────────────────
EPS_FY2022 = 10.05   # adj; post-COVID cross-border recovery; Russia exit ~$200M charge
EPS_FY2023 = 12.03   # adj; +19.7% growth; cross-border fully normalised; VAS scaling
EPS_FY2024 = 14.40   # adj; +19.7% growth; consistent compounding; buybacks +3-4%/yr
EPS_FY2025 = 17.00   # adj; ~+18.1%; Q3 FY2025 single-quarter $4.38; full-year derived
                     # (implied by FY2026E $19.58 ÷ 1.151 = $17.01; Q1 FY2025 = $3.74)
EPS_NOW    = 19.50   # FY2026E adj consensus ~$19.58; Q1 FY2026 actual $4.60 (+23% YoY)
                     # Q2-Q4 projected $4.83-$5.15/quarter avg; full year ~$19.50-19.60

# ── EPP — earnings power price (structural floor) ────────────────────────
EPS_TROUGH = 13.00   # severe recession: GDV -12%, cross-border -30% (similar to
                     # COVID 2020). Revenue -15%; operating leverage → EPS -24%.
                     # From FY2025 base ~$17.00: stress = $17.00 × 0.76 = $12.92.
                     # Round to $13.00. MA COVID FY2020 adj EPS ~$6.37 (complete
                     # cross-border lockdown); modern MA more diversified (VAS now
                     # ~36% of net revenue; less cross-border dependent than 2020).
                     # $13.00 reflects GFC-severity WITHOUT complete travel shutdown.
EPP_MIN_PE = 22      # Same rationale as Visa (see v_signal_model.py). Payment
                     # network trough P/E: never below 20× in history because
                     # moat permanence is visible and repriced in immediately.
                     # MA COVID trough ~$218 / $6.37 adj = 34.2× — even the 2020
                     # crisis trough was 34× because recovery was expected within 12m.
                     # 22× is conservative; structural floor anchoring, not a
                     # near-term trading target.
EPP = EPS_TROUGH * EPP_MIN_PE   # $286.00

# ── Method B — 2-year normalised upside ceiling ───────────────────────────
CONS_EPS_2YR = 22.65   # FY2027E adj consensus (Zacks: +15.7% from FY2026E $19.58).
                       # MA EPS growth has been 18-20%/yr for 3 consecutive years.
                       # FY2027E $22.65 = FY2026E $19.58 × 1.157 — conservative vs
                       # historic run-rate; appropriate given macro uncertainty.
                       # Buyback tailwind (~4-5% annual float reduction) mechanical
                       # EPS boost embedded in the consensus.
CONS_EXIT_PE = 30      # Premium payment network historical multiple. MA has traded
                       # 25-45× historically; current 25.6× is at the LOWER bound.
                       # 30× requires no re-rating relative to recent history (MA
                       # was at 30× for much of 2023-2024). Modest from current 25.6×.
price_b = CONS_EPS_2YR * CONS_EXIT_PE   # $679.50 ≈ $680

ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
# = (498.54 − 286.00) / (679.50 − 498.54) = 212.54 / 180.96 = 1.17×
# → ◐ WATCHLIST (just above the 1.10 ACCUMULATE boundary).
# Compare: Visa (V) ratio_b 1.71× — MA is materially better risk/reward
# at current prices despite being near highs. Reason: MA corrected -17%
# from $601 to ~$499; lower forward P/E (25.6× vs Visa 27.5×); faster EPS
# growth (Q1 adj EPS +23% vs Visa +20%).

epp_gap_pct = (CURRENT_PRICE - EPP) / EPP * 100
# = (498.54 - 286) / 286 × 100 = 74.3%

# ── price scenarios ───────────────────────────────────────────────────────
PRICE_BEAR  = 286    # = EPP. Severe recession + COVID-style cross-border shock.
                     # GDV -12%, cross-border -30%. EPS $13 × 22×.
                     # -43% from current. MA COVID low ~$218 was at 34× $6.37 adj EPS.
                     # $286 is a far more conservative bear (only 22× on $13 stress).
PRICE_BASE  = 600    # FY2027E $22.65 × 26.5× = $600. Multiple flat (no re-rating).
                     # Represents recovery to just below the 52-wk high of $601.77
                     # via fundamental EPS growth + buybacks. +20% from current.
PRICE_BULL  = 680    # = price_b. FY2027E $22.65 × 30×. Multiple returns to recent
                     # average (MA traded 28-32× for much of 2023-24). VAS segment
                     # re-rated as faster-growing. No major regulatory shock. +36%.
PRICE_XBULL = 850    # FY2028E ~$26 × 33×. Agentic commerce + VAS become measurable
                     # new revenue streams; MA accelerates open banking monetisation
                     # (Aiia, Finicity); stablecoin/crypto settlement on MA rails;
                     # buybacks at $5B+/yr drive EPS well above consensus. +70%.

# ── SCA (stock-specific composite adjustment) ────────────────────────────
SCA_FACTORS = [
    # (description, score, weight)
    ("Value-Added Services: +18% currency-neutral Q1 FY2026; cybersecurity (NuData, Ethoca), analytics (Brighterion), open banking (Aiia, Finicity) now ~36% of net revenue; higher-margin, stickier than pure network fees", +0.35, 0.25),
    ("Cross-border premium: MA more cross-border-weighted than Visa; cross-border vol +13% Q1; travel boom ongoing; earns ~3× the fee rate on cross-border vs domestic; higher upside in global travel recovery", +0.30, 0.20),
    ("Buyback compounding: $4B Q1 + $1.7B Apr 2026 = $5.7B in 4 months; ~6-7% annual float reduction at this pace; mechanical EPS boost significantly above revenue growth", +0.20, 0.15),
    ("Regulatory / legal overhang: UK interchange class action (~£14B claim pending); EU payment regulation tightening; US Congress interchange fee bills; debit routing rules risk (even without DOJ suit)", -0.30, 0.25),
    ("Stablecoin / CBDC disruption: cross-border is MA's highest-margin revenue; on-chain B2B settlement growing; Circle/USDC and CBDCs most threaten MA's premium cross-border fees in 5-10yr", -0.20, 0.15),
]

sca_raw = sum(s * w for _, s, w in SCA_FACTORS)   # +0.0725
sca_adj = sca_raw / 2.0                             # +0.036

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

signal = classify(ratio_b)   # ◐ WATCHLIST

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
Special context: Mastercard is the natural twin of Visa (V) — same asset-light
payment network model, same ~50% operating margins, same zero credit-risk
structure. Both are covered in this framework. Key MA vs V differences:

  MA forward P/E (FY2026E): 25.6×  vs  Visa 27.5×  ← MA cheaper despite same moat
  MA adj EPS growth (Q1):   +23%   vs  Visa +20%   ← MA growing marginally faster
  MA ratio_b (this model):   1.17×  vs  Visa 1.71×  ← MA better risk/reward
  MA VAS revenue share:      ~36%   vs  Visa ~50%+ (VAS broader at MA)
  MA DOJ lawsuit:            None   vs  Visa debit monopoly suit (filed Sep 2024)
  MA 52-wk drawdown:        -17%   vs  Visa -12%   ← MA corrected more from peak

Both are WATCHLIST, but MA offers marginally better risk/reward at current prices.
The 52-wk low of $480.50 (April 2026) was the ACCUMULATE entry (ratio_b ~0.99×).

Key metrics (Q1 2026, Jan–Mar 2026):
  Gross Dollar Volume     : +7% local currency
  Cross-border volume     : +13%  (MA's premium revenue driver)
  Value-Added Services    : +18% currency-neutral  (cybersecurity, analytics, open banking)
  Adj diluted EPS         : $4.60 (+23% YoY from $3.73)
  Share repurchases       : $4.0B in Q1; $1.7B additional through Apr 27, 2026""")

    print(f"""
EPP (Earnings Power Price) — structural floor
  = EPS_TROUGH × EPP_MIN_PE
  Stress EPS ($13.00) × 22× floor.
  $13.00 reflects GFC-severity recession: GDV -12%, cross-border -30%, VAS
  growth slows. From FY2025 $17.00 base: $17.00 × 0.76 = $12.92 ≈ $13.00.
  Note: MA COVID FY2020 adj EPS was only ~$6.37 due to complete cross-border
  lockdown (international travel near-zero); modern MA VAS segment provides
  ~36% of revenue that is far less cyclical, making $13 a more realistic floor
  for the current business mix vs 2020. The 22× floor P/E reflects moat
  permanence — MA COVID low ~$218 was 34× the trough adj EPS.
  EPP = ${EPP:.2f}.
  Calibration: 52-wk low ${PRICE_52W_LOW:.2f} ÷ $13.00 = {PRICE_52W_LOW/EPS_TROUGH:.1f}× stress EPS — confirming
  the April 2026 low was still {PRICE_52W_LOW/EPS_TROUGH:.1f}× above the catastrophe floor.

Method B — 2-year normalised upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E adj EPS ~${CONS_EPS_2YR:.2f} (Zacks consensus: +15.7% from FY2026E ${EPS_NOW:.2f};
  conservative vs MA's 18-20%/yr historical run-rate) × {CONS_EXIT_PE}× exit P/E
  (current 25.6×; 30× is MA's recent average — not aggressive).
  = ${price_b:.2f}.
  Ratio B = (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f}) = ${CURRENT_PRICE-EPP:.2f} / ${price_b-CURRENT_PRICE:.2f} = {ratio_b:.2f}×
  → {signal}. MA is at the attractive end of WATCHLIST — near ACCUMULATE.
  Method B upside: +{(price_b/CURRENT_PRICE-1)*100:.1f}% to ${price_b:.0f}. Downside to EPP: -{(1-EPP/CURRENT_PRICE)*100:.1f}%.
  Note: 52-wk low ${PRICE_52W_LOW:.2f} was ACCUMULATE entry (ratio_b ~0.99×).
  The entry was only 7 weeks ago; +{(CURRENT_PRICE/PRICE_52W_LOW-1)*100:.1f}% since then. Still near the boundary.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

    print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MASTERCARD: THE OTHER VISA — BUT CHEAPER, FASTER-GROWING, AND DOJ-FREE
========================================================================

Mastercard and Visa are the Coke and Pepsi of global payments — two dominant
duopolists sharing ~80% of the world's card payment volume. Mastercard holds
approximately 26-28% of global card spend volume; Visa ~52%. Both have
essentially identical business models: pure payment infrastructure companies
that earn a small percentage of every transaction processed on their network,
with zero credit risk, ~50% operating margins, and decades-long network-effect
moats.

In May 2026, there is one important relative positioning insight:
  MA is cheaper than V on a forward P/E basis (25.6× vs 27.5×) despite:
    (a) growing EPS slightly faster (Q1: +23% vs Visa +20%)
    (b) having no active DOJ antitrust lawsuit
    (c) having a growing Value-Added Services segment (~36% net revenue)
    (d) slightly more attractive ratio_b (1.17× vs Visa 1.71×)

The discount likely reflects: (1) MA's $601.77 ATH vs current $499 = a more
painful recent drawdown; (2) MA's UK class action litigation uncertainty;
(3) institutional preference for Visa's larger network scale. This valuation
gap appears unjustified to us — if anything, MA's VAS diversification makes
it MORE defensible against payment disruption risk.

Q1 2026 — ACCELERATING GROWTH; STRONGEST VAS QUARTER IN YEARS
==============================================================
  Revenue (net):          $8.4B   (+16% reported; +12% currency-neutral)
  Adjusted diluted EPS:   $4.60   (+23% YoY; beat $4.41 est by $0.19)
  GAAP diluted EPS:       $4.35
  GDV:                    +7% local currency
  Cross-border volume:    +13%    (MA's highest-margin revenue driver)
  Value-Added Services:   +18% currency-neutral  (record growth; ~36% of net rev)
  Share buybacks:         $4.0B in Q1; $1.7B additional through Apr 27 = $5.7B in 4M

Full-year 2026 guidance confirmed: revenue ~$36.9B; Q2-Q4 EPS trajectory
of $4.83-5.15/quarter, implying full-year FY2026E adj EPS of ~$19.50-19.60.
16 analysts revised estimates higher post-Q1. Consensus analyst PT: $648.54
(+30% from current). MA has 26 analysts covering with "Strong Buy" consensus.

THE VALUE-ADDED SERVICES EDGE
==============================
This is where MA differentiates most meaningfully from Visa. MA's VAS segment
includes a growing portfolio of software and data businesses:

  Cybersecurity services:
    • NuData: behavioural biometrics (detects bot vs. human in real time)
    • Ethoca: chargeback prevention and dispute resolution
    • Ekata: identity verification (acquired 2021; $850M)
    • RiskRecon: third-party cyber risk intelligence

  Analytics & AI:
    • Brighterion: real-time AI for fraud detection (1.8B models deployed)
    • Test & Learn: merchant analytics platform

  Open banking:
    • Aiia (Denmark): European open banking connectivity
    • Finicity (US): credit decisioning and financial data aggregation

  Loyalty & marketing:
    • Dynamic Yield: personalisation platform (acquired from McDonald's 2022; $300M)
    • Priceless Cities/consumer offers network

Combined, VAS grew +18% in Q1 FY2026 (currency-neutral) and now represents
~36% of Mastercard's net revenue, up from ~30% in 2020. Critically, VAS
revenue is:
  (a) subscription/software-based — not purely volume-linked
  (b) higher margin than core network fees
  (c) sticky — hard to switch once embedded in bank/merchant systems
  (d) cross-selling platform — each VAS customer is more likely to route
      more transaction volume on MA's core network

This VAS business is a meaningful moat extension that Visa has been slower to
build. If VAS becomes 50%+ of MA's revenue by 2028, Mastercard's valuation
deserves a premium to Visa, not a discount.

THE CROSS-BORDER PREMIUM — MA'S BIGGEST LEVER
=============================================
Cross-border transactions (international travel, online shopping across borders,
B2B international payments) carry approximately 3× the fee rate of domestic
transactions for both MA and Visa. This premium exists because:
  (1) FX conversion fees: MA earns a spread on currency conversion
  (2) Absence of domestic interchange cap: no regulatory cap on cross-border fees
  (3) Higher authorisation complexity: more fraud risk = more MA value-add

MA has historically been slightly more cross-border-weighted than Visa, meaning
cross-border recovery is a larger tailwind relative to its network size:
  Q1 FY2026: cross-border +13% (vs Visa's +11% ex-intra-EU)
  Travel spending: +12% YoY — post-COVID travel boom still running
  Cross-border e-commerce: +12% — not just travel; online global retail

If cross-border sustains +10-13% growth through FY2027, this single line item
could add $2-3B in incremental revenue vs trough levels. At 50% margins,
that's $1-1.5B in incremental operating income = ~$1.20-$1.80/share EPS boost.

THE REGULATORY PICTURE — LESS ACUTE THAN VISA BUT NOT ZERO RISK
================================================================
Unlike Visa, MA does not currently face a US DOJ antitrust lawsuit (as of
May 2026). However, MA faces several regulatory headwinds:

UK Interchange Class Action (~£14B potential):
  The UK class action (Walter Merricks vs Mastercard; filed 2007; UK Supreme
  Court ruled in 2020 it could proceed) is now in active litigation. The claim
  covers ~$46M UK consumers overcharged on interchange fees 1992-2008.
  Settlement probability: high; quantum uncertain. Best case: £1-3B (manageable).
  Worst case: £8-14B (significant but survivable with MA's balance sheet).
  Status: trial expected 2026-2027. This is the largest single legal risk for MA.

EU Payments Regulation:
  EU is actively developing stricter interchange fee rules and open banking
  mandates. PSD3 (Payment Services Directive 3) being finalised — could
  incrementally reduce interchange revenues from EU issuers.

US Congress Interchange Bills:
  Credit Card Competition Act (resurfaced 2025-2026): proposed forced routing
  for credit cards (similar to Durbin Amendment for debit). If passed, would
  reduce MA/Visa network fees by 15-25% on US credit. Probability: LOW (banking
  industry opposition is fierce), but the legislative tail risk exists.

THE BUYBACK COMPOUNDING MACHINE
================================
Mastercard's capital return programme is extraordinary:
  Q1 2026: $4.0B buybacks in a single quarter
  Apr 1-27 2026: additional $1.7B
  Total 4M: $5.7B — annualised pace ~$17-18B/yr

Against a market cap of ~$440B, this represents ~4% of the market cap being
retired annually. With $884M diluted shares outstanding:
  $17B buybacks ÷ ~$499 avg price ≈ 34M shares/yr retired
  34M / 884M = 3.8% annual share count reduction
  Effect: even with 0% EPS growth, buybacks alone create 3.8% EPS growth
  Combined with 12-15% revenue growth + operating leverage: 18-22% EPS growth

This compounding engine has driven EPS from $8.40 (FY2021) to $19.50E (FY2026)
= +132% in 5 years = ~18.3% CAGR — almost entirely via genuine business growth
and buybacks, not financial engineering.

AGENTIC COMMERCE — SAME OPPORTUNITY AS VISA
============================================
Like Visa, MA is positioning itself as infrastructure for AI agent transactions:
  • Token Hub: MA's equivalent of Visa Tokens — 30B+ network tokens globally
  • Agent Pay: announced 2026; MA infrastructure for AI agent-initiated payments
  • Click to Pay: global guest checkout standardisation (W3C standard)
  • MA's cybersecurity VAS (NuData, Ethoca) = ideal fraud layer for AI agents

Both MA and V will benefit from agentic commerce. MA's cybersecurity
and fraud detection VAS tools may give it a slight edge in risk management
for AI agent transactions, where establishing identity/trust is critical.

ENTRY/EXIT FRAMEWORK
====================
  ◉ BUY        : $345-375  (1.2-1.3× EPP of $286)
  ◎ ACCUMULATE : $420-480  (ratio_b ~0.6-1.0×; 52-wk low territory)
  ◐ WATCHLIST  : $480-540  (current; fair-to-attractive for quality compounder)
  ▷ HOLD/TRIM  : $540-590  (approaching Method B; near ATH territory)
  ✕ TRIM HARD  : >$590     (above Method B; near ATH $601.77)

The 52-wk low of $480.50 (April 2026) was a strong ACCUMULATE entry
(ratio_b ~0.99×, just below the 1.10 ACCUMULATE boundary). Current $499
is WATCHLIST. Still very near the ACCUMULATE threshold — not a chasing
trade, but a quality business you can continue to own confidently.

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
  Market cap      : ~${mktcap_b:.0f}B   |   Shares (diluted): ~{SHARES_M/1000:.3f}B
  Dividend (ann)  : ${DIVIDEND_ANN:.2f}   |   Yield: {DIVIDEND_ANN/CURRENT_PRICE*100:.2f}%
  Forward P/E     : {CURRENT_PRICE/EPS_NOW:.1f}×  (on FY2026E adj ${EPS_NOW:.2f})
  FY2027E P/E     : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (on FY2027E adj ${CONS_EPS_2YR:.2f})
  PEG ratio       : {(CURRENT_PRICE/EPS_NOW)/16:.2f}×  (P/E {CURRENT_PRICE/EPS_NOW:.1f}× ÷ 16% EPS growth rate)
  vs Visa (V)     : MA P/E {CURRENT_PRICE/EPS_NOW:.1f}× vs V P/E 27.5× — MA cheaper despite similar growth""")

    print(f"""
  II. EPS HISTORY (non-GAAP adjusted; calendar fiscal year Dec 31)
  ----------------------------------------------------------------------
  FY2022  : ${EPS_FY2022:.2f}  (post-COVID cross-border recovery; Russia exit ~$200M charge)
  FY2023  : ${EPS_FY2023:.2f}  (+19.7%; cross-border fully normalised; VAS growing ~30% of rev)
  FY2024  : ${EPS_FY2024:.2f}  (+19.7%; consistent; buybacks driving ~4% mechanical EPS boost)
  FY2025  : ${EPS_FY2025:.2f}  (~+18.1%; Q3 FY2025 single-quarter $4.38; implied from FY2026E)
  FY2026E : ${EPS_NOW:.2f}  (Q1 actual $4.60 +23% YoY; full year guided ~$19.50-19.60)
  FY2027E : ${CONS_EPS_2YR:.2f}  (consensus +15.7% from FY2026E; used for Method B)
  Q1 2026 : $4.60 adj  (beat $4.41; +23% YoY; GDV +7%; cross-border +13%; VAS +18%)

  III. EPP & METHOD B
  ----------------------------------------------------------------------
  EPS_TROUGH  : ${EPS_TROUGH:.2f}/share  (GDV -12%, cross-border -30%; COVID-level ex travel lockdown)
  EPP_MIN_PE  : {EPP_MIN_PE}×          (network moat; never traded <20× historically)
  EPP (floor) : ${EPP:.2f}       (= ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×)
  EPP gap     : +{epp_gap_pct:.1f}%     (current price is {epp_gap_pct/100:.1f}× above EPP floor)

  CONS_EPS_2YR: ${CONS_EPS_2YR:.2f}/share  (FY2027E adj; +{CONS_EPS_2YR/EPS_NOW*100-100:.0f}% above FY2026E; conservative vs history)
  CONS_EXIT_PE: {CONS_EXIT_PE}×          (return to recent 2023-24 average multiple; not aggressive)
  Method B    : ${price_b:.2f}       (= ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×; ≈ analyst avg PT $648)
  Upside to B : +{(price_b/CURRENT_PRICE-1)*100:.1f}%
  Downside EPP: -{(1-EPP/CURRENT_PRICE)*100:.1f}%

  ┌─────────────────────────────────────────────────────────────────────┐
  │  RATIO B = ({CURRENT_PRICE:.2f} − {EPP:.2f}) / ({price_b:.2f} − {CURRENT_PRICE:.2f})             │
  │           = {CURRENT_PRICE-EPP:.2f} / {price_b-CURRENT_PRICE:.2f} = {ratio_b:.2f}×                              │
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
  Market composite  : {market_composite:.3f}  (BASE, leaning toward BEAR)
  Adj composite     : {adj_composite:.3f}  (BASE)
  Softmax weights at adj composite ({adj_composite:.3f}):
    BEAR  : {W['BEAR']*100:.1f}%  (${PRICE_BEAR})
    BASE  : {W['BASE']*100:.1f}%  (${PRICE_BASE})
    BULL  : {W['BULL']*100:.1f}%  (${PRICE_BULL})
    XBULL : {W['XBULL']*100:.1f}%  (${PRICE_XBULL})
  Expected price (adj): ${exp_p:.1f}  vs current ${CURRENT_PRICE:.2f}  (Δ {(exp_p/CURRENT_PRICE-1)*100:+.1f}%)

  VI. SCENARIOS SUMMARY
  ----------------------------------------------------------------------
  BEAR  (${PRICE_BEAR}) : Severe recession + COVID-style cross-border collapse.
               GDV -12%, cross-border -30%, VAS growth stalls. EPS $13 × 22×.
               UK class action settles at £10B+; absorbs significant cash.
               Stablecoin/CBDC disintermediates cross-border premium fees.
               -{(1-PRICE_BEAR/CURRENT_PRICE)*100:.0f}% from current. MA COVID low (Mar 2020): ~$218 at 34× trough.

  BASE  (${PRICE_BASE}) : Steady compounding. GDV +7-8%/yr; cross-border +10-12%;
               VAS +15-18%; buybacks continue at ~$5-6B/yr. Multiple flat.
               UK litigation settles for £2-4B (manageable). FY2027E $22.65 ×
               26.5× = $600 — recovering to 52-wk high via EPS growth.
               +{(PRICE_BASE/CURRENT_PRICE-1)*100:.0f}% from current.

  BULL  (${PRICE_BULL}) : Multiple re-rates + agentic commerce. FY2027E $22.65 × 30×.
               VAS reaches 40%+ of revenue; re-rated as a software/data
               company partially. No DOJ lawsuit; UK settles £1-2B. Agentic
               commerce Agent Pay generates first measurable revenue.
               +{(PRICE_BULL/CURRENT_PRICE-1)*100:.0f}% from current.

  XBULL (${PRICE_XBULL}) : Structural acceleration. FY2028E ~$26 × 33×. VAS becomes
               50%+ of revenue; MA re-rated at 32-35× (software premium).
               Buybacks reach $6B+/yr. Stablecoin on-chain settlement runs
               on MA rails. Cross-border sustains +15%/yr. Open banking
               (Finicity/Aiia) becomes major credit decisioning revenue.
               +{(PRICE_XBULL/CURRENT_PRICE-1)*100:.0f}% from current.
""")

    print("=" * 72)
    print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-26")
    print("=" * 72)
