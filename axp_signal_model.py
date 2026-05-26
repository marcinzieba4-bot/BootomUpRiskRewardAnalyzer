"""
American Express Company  (AXP)
BottomUp Risk/Reward Analyzer — Signal Model
"""
import math

# ── Core inputs ──────────────────────────────────────────────────────────────
TICKER        = "AXP"
COMPANY       = "American Express Company"
SECTOR        = "Closed-Loop Payment Network · Premium Card Issuing · Travel & Lifestyle Services"

CURRENT_PRICE = 311.01    # AXP — fetched Yahoo Finance / web search, 2026-05-26
                            # May 25 range $310.50–$314.43; market cap $212.78B
PRICE_52W_LOW  = 281.47   # April 2026 tariff-panic low (+10.5% to current)
PRICE_52W_HIGH = 387.49   # 52-wk high (AXP at $311 is 19.7% below peak)
SHARES_M       = 683.0    # Derived: Berkshire 151.61M shares ÷ 22.22% stake = 682.3M
DIVIDEND_ANN   = 3.80     # $0.95/quarter (raised +16% for 2026; confirmed: BRK receives $576M/yr
                            # = 151.61M × $3.80; yield 1.22% at $311)

# ── EPS history (GAAP diluted) ────────────────────────────────────────────────
EPS_HISTORY = {
    "FY2022": 9.85,    # Post-COVID recovery; travel & entertainment rebounding; billed business +25%
    "FY2023": 11.21,   # +13.8%; record card fees + spend growth; card member acquisition record
    "FY2024": 14.01,   # +25.0%; record year; premium card expansion; Millennials/Gen-Z inflection
    "FY2025": 15.38,   # +9.8%; record revenue $72B (+10%); net card fees $10B (+18%); FY2025 actual
}
EPS_NOW = 17.60   # FY2026E guidance midpoint ($17.30–$17.90); Q1 2026 actual $4.28 (+18% YoY)

# ── EPP (Earnings Power Price) — structural floor ────────────────────────────
EPS_TROUGH  = 7.00    # Severe recession: billed business -35%, loan provisions 2×, travel/ENT
                       # spend collapses. AXP FY2020 GAAP EPS: $3.77 (COVID destroyed travel spend
                       # + $5.7B in reserve builds). A "normal" recession (not pandemic-level
                       # travel shutdown): billed business -25% → revenue -20% → EPS ~$7.
                       # $7 = midpoint between COVID black swan ($3.77) and current normalized level.
                       # Calibration: 52-wk low $281.47 ÷ $7.00 = 40.2× stress EPS — market
                       # consistently assigns 30-40× stress EPS even at trough, reflecting
                       # confidence in franchise recovery. (AXP March 2020 panic low was ~$67.)
EPP_MIN_PE  = 18      # AXP franchise floor: even at COVID trough ($3.77 EPS), GS/peers priced
                       # AXP at 17-22× as recovery was assumed swift. Premium closed-loop network
                       # with recurring card fee revenue (no credit risk) supports elevated floor.
                       # 18× > commercial bank floor (9×) reflects network + recurring revenue quality.
EPP         = EPS_TROUGH * EPP_MIN_PE   # = $126.00

# ── Method B (2-year normalised upside ceiling) ───────────────────────────────
CONS_EPS_2YR  = 20.30   # FY2027E analyst consensus (range $19.08–$21.70; mid $20.31);
                          # = FY2026E $17.60 × ~15% growth (card fee expansion + spending + buybacks)
CONS_EXIT_PE  = 21       # Slight re-rating from current 17.7× FW; AXP historically 18-25× in
                          # strong growth phases; 21× vs V 27.5× / MA 25.6× = still discounted for
                          # credit risk; justified as credit quality proves resilient in premium segment
price_b = CONS_EPS_2YR * CONS_EXIT_PE   # = $426.30

# ── Primary signal ────────────────────────────────────────────────────────────
ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
# = (311.01 − 126.00) / (426.30 − 311.01) = 185.01 / 115.29 = 1.60×  → ◐ WATCHLIST

# ── AXP-specific metrics ─────────────────────────────────────────────────────
ROE             = 35.0    # Q1 2026 annualised ROE — extraordinary for a business with credit risk
EQUITY_PER_SHR  = 50.50  # Implied: FY2026E EPS $17.60 ÷ ROE 34-35% ≈ $50-51; far below $311 price
                           # AXP P/B ~6.2× — franchise value dominates book value
BILLED_BUS_Q1   = 428.0  # Billed business Q1 2026 ($B); +10% YoY; highest quarterly growth in 3yrs
NET_CARD_FEES   = 10.0    # FY2025 net card fees ($B; +18%; growing fast; ZERO credit risk on fees)
BERKSHIRE_STAKE = 22.22   # Berkshire Hathaway ownership %; 151.61M shares; Buffett's 2nd-largest holding

# ── Scenario anchors ─────────────────────────────────────────────────────────
scenarios = {
    "BEAR":  126.0,    # EPP floor: $7 × 18× = $126. Severe recession + travel collapse.
    "BASE":  375.0,    # FY2027E $20.30 × ~18.5× = $375; ≈ analyst avg PT ($362-375).
    "BULL":  426.3,    # = price_b. Re-rating to 21× as ROE 35% + card fee compounding evident.
    "XBULL": 550.0,    # FY2028E ~$25 × 22× = $550; multiple converges with V/MA as credit quality
                        # proven through cycle; net card fees → 30% of revenue.
}

# ── SCA (Stock-specific Composite Adjustment) ─────────────────────────────────
sca_factors = [
    # (description,                                                       score,  weight)
    ("Buffett conviction hold: BRK owns 22.22% for 35 years; sold ENTIRE "
     "V and MA positions Q1 2026 but HELD AXP — strongest quality signal",  +0.40,  0.25),
    ("Net card fees compounding: $10B FY2025 (+18%); $0.95/qtr dividend "
     "(+16%); fee revenue has zero credit risk; growing >EPS growth",       +0.30,  0.20),
    ("Closed-loop data moat: AXP owns network + issuer; full card member "
     "data enables superior marketing, risk management, cross-sell",         +0.25,  0.15),
    ("Credit risk vs V/MA: AXP carries loan losses (~$1.5B/qtr provision); "
     "recession = provisions double; 35% P/E discount to V/MA reflects this", -0.30,  0.25),
    ("19.7% below 52-wk high: recoverable but not 'on sale' — April "
     "$281 was the entry; current $311 has partially recovered",              -0.15,  0.20),
    ("Premium spend concentration: travel/ENT/dining = large billed share; "
     "recession cuts these categories first (COVID FY2020 EPS: $3.77)",       -0.20,  0.15),
]

sca_raw = sum(score * weight for _, score, weight in sca_factors)
sca_adj = sca_raw / 2.0

# ── Softmax composite engine ─────────────────────────────────────────────────
def infer_composite(current_price: float, scens: dict[str, float],
                    lo: float = 1.0, hi: float = 4.0, iters: int = 60) -> float:
    centres = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
    T = 0.60
    for _ in range(iters):
        mid = (lo + hi) / 2
        logits  = {k: -(mid - centres[k])**2 / T for k in centres}
        max_l   = max(logits.values())
        exp_l   = {k: math.exp(logits[k] - max_l) for k in logits}
        denom   = sum(exp_l.values())
        weights = {k: exp_l[k] / denom for k in exp_l}
        ev = sum(weights[k] * scens[k] for k in weights)
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
pb_current   = CURRENT_PRICE / EQUITY_PER_SHR
mkt_cap_b    = CURRENT_PRICE * SHARES_M / 1000
ratio_b_52wk_low = (PRICE_52W_LOW - EPP) / (price_b - PRICE_52W_LOW)
ratio_b_52wk_hi  = (PRICE_52W_HIGH - EPP) / (price_b - PRICE_52W_HIGH)

# ── Signal label ──────────────────────────────────────────────────────────────
def signal_label(r: float) -> str:
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
    print(f"""Special context: AXP occupies a unique position in financial services —
it is the only CLOSED-LOOP payment network that also issues its own cards.
Unlike Visa/MA (pure toll roads with zero credit risk), AXP both operates the
network AND lends money, creating a more complex but also more lucrative model.
AXP is valued as a hybrid: P/E vs through-cycle earning power (bank-like)
+ network premium (V/MA-like) + franchise optionality (Buffett-endorsed).

  AXP vs peers (closed-loop vs open-loop payment networks):
  AXP  P/E fwd : {CURRENT_PRICE/EPS_NOW:.1f}×   vs  V: 27.5×  vs  MA: 25.6×  ← AXP CHEAPEST
  AXP  ROE Q1  : {ROE:.1f}%    vs  V: ~50%  vs  MA: ~50%  ← AXP lower (credit risk)
  AXP  ratio_b : {ratio_b:.2f}×   vs  V: 1.71× vs  MA: 1.17× ← AXP WATCHLIST
  Berkshire    : 22.22% stake; sold ENTIRE V + MA Q1 2026; HELD AXP

THE DEFINING SIGNAL: Buffett sold Visa AND Mastercard entirely in Q1 2026
but maintained his FULL 151.61M share position in AXP. This is not passive —
Berkshire actively chose the closed-loop model over the open-loop models at
this valuation. Berkshire now earns $576M/yr in dividends from AXP alone.

AXP is NOT a traditional bank. It is best understood as:
  1. A premium payment NETWORK (owns network rails — like V/MA)
  2. A card ISSUER (lends money — unlike V/MA)
  3. A membership FRANCHISE (annual card fees from Platinum/Gold members)
  4. A DATA MOAT (closed loop = full transaction data; V/MA don't see this)

Key metrics (Q1 2026, Jan–Mar 2026):
  Revenue (net)       : $18.9B  (+11% YoY; beat estimates)
  Net income          : $3.0B   (+15% YoY; vs $2.6B Q1 2025)
  EPS (diluted)       : $4.28   (+18% YoY; guidance reaffirmed at $17.30-$17.90)
  Billed business     : ${BILLED_BUS_Q1:.0f}B    (+10% YoY; highest quarterly growth in 3 years)
  Card member spend   : +10%    (highest quarterly growth since 2022)
  Net card fees       : +16% FX-adj (recurring fee revenue; zero credit risk)
  ROE (annualised)    : {ROE:.1f}%    (extraordinary for any financial institution)
  Capital returned    : $2.3B   ($1.7B buybacks + $0.7B dividends in ONE quarter)
  FY2025 net card fees: ${NET_CARD_FEES:.0f}B    (+18% FY; now a dominant revenue driver)
  BRK dividend income : $576M/yr from AXP (151.61M × $3.80; no other position pays this)

EPP (Earnings Power Price) — structural floor
  = EPS_TROUGH × EPP_MIN_PE
  Stress EPS (${EPS_TROUGH:.2f}) × {EPP_MIN_PE}× floor.
  ${EPS_TROUGH:.2f}: Billed business -35% (recession + travel collapse), provisions ×2,
  marketing cut back, card fee growth stalls. AXP FY2020 actual EPS: $3.77
  (COVID pandemic destroyed travel/restaurant/entertainment spending — AXP's
  core categories — AND required $5.7B+ in loan loss reserves).
  A "normal" recession (no pandemic-level category shutdown): billed -25% →
  revenue -20% → EPS ~$7.00. Floor is well above COVID black swan.
  EPP_MIN_PE {EPP_MIN_PE}× (vs 9× for commercial banks): even at COVID trough,
  AXP priced at 17-22× because: (a) card fees continue regardless of spending,
  (b) premium card member base recovers faster than mass market, and (c) the
  franchise value is permanent. AXP March 2020 low $67 ÷ $3.77 = 17.8× --
  the market assigned 18× even at the pandemic panic bottom.
  EPP = ${EPP:.2f}.
  Calibration: 52-wk low $281.47 ÷ $7 = 40× stress EPS — NOT pricing recession.

Method B — 2-year normalised upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E ${CONS_EPS_2YR:.2f} (analyst consensus range $19.08-$21.70; mid ~$20.31);
  = FY2026E ${EPS_NOW:.2f} × ~15% growth (card fee compounding + spending + buybacks)
  × {CONS_EXIT_PE}× exit P/E (vs current {CURRENT_PRICE/EPS_NOW:.1f}×; slight re-rating as ROE {ROE:.0f}% premium
  gains recognition; discount vs V {CONS_EXIT_PE}× vs 27.5× / MA 25.6× justified for credit risk;
  analyst avg PT $362-375 sits at 18.5× FY2027E — between current and {CONS_EXIT_PE}×)
  = ${price_b:.2f}.
  Ratio B = (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f}) = ${CURRENT_PRICE-EPP:.2f} / ${price_b-CURRENT_PRICE:.2f} = {ratio_b:.2f}×
  → {signal}. Method B upside: +{upside_b_pct:.1f}%. Downside to EPP: {dn_epp_pct:.1f}%.
  52-wk low ${PRICE_52W_LOW:.2f} was ACCUMULATE at ratio_b {ratio_b_52wk_low:.2f}× — that was the entry.
  52-wk high ${PRICE_52W_HIGH:.2f} was AVOID at ratio_b {ratio_b_52wk_hi:.1f}× — that was the exit.
  Current $311 = WATCHLIST. Add on pullback to $270-295 (ACCUMULATE zone).
{thin}
""")

    print()
    print("PART 2 — ANALYST COMMENTARY & CONTEXT")
    print(thin)
    print(f"""
AMERICAN EXPRESS: THE FRANCHISE BUFFETT WOULD NEVER SELL
=========================================================

Warren Buffett first bought American Express in 1963 — during the "Salad Oil
Scandal" when AXP's stock crashed 50% on fraudulent warehouse receipts. Buffett
saw what the market missed: the franchise (the green card, the travelers' cheques,
the trust) was untouched. He made his first fortunes on that investment.

In 2026, Berkshire Hathaway owns 22.22% of American Express — 151.61 million
shares, a position worth ~$47.5 billion, generating $576M in annual dividends.
In Q1 2026, Berkshire SOLD ITS ENTIRE POSITIONS in Visa and Mastercard.
AXP was not touched.

THIS IS THE DEFINING SIGNAL OF THE AXP INVESTMENT THESIS IN 2026.

Buffett chose AXP's closed-loop model over V/MA's open-loop models at current
valuations. AXP trades at 17.7× FY2026E vs Visa 27.5× and Mastercard 25.6×.
Buffett is essentially saying: the credit-risk premium required of AXP (its
lower P/E vs V/MA) is more than compensated by its closed-loop advantages.

THE AXP BUSINESS MODEL — WHY IT'S DIFFERENT FROM BANKS
=======================================================
AXP has three distinct revenue engines:

ENGINE 1: DISCOUNT REVENUE (like Visa/MA toll)
  When a merchant accepts Amex, they pay 2.2-2.5% of the transaction
  (vs 1.5-1.8% for Visa/MC). AXP charges more because Amex card members
  spend more: avg AXP spend ~$26,000/year vs ~$8,000 industry average.
  This is the "Merchant Discount Rate" — AXP's transaction revenue.
  Q1 2026: Billed business $428B × ~2.3% = ~$9.8B in this revenue stream.

ENGINE 2: NET INTEREST INCOME (like a bank)
  AXP lends money via credit card receivables. Card members who carry balances
  pay ~18-22% APR. AXP's loan book (~$80B+) generates $5-6B/yr in net interest.
  RISK: these receivables can go bad in recessions.
  PROTECTION: AXP's premium card members have FAR lower default rates than
  mass-market cards. Write-off rates 40-60% below industry average.

ENGINE 3: NET CARD FEES (the purest, highest-quality revenue)
  Card members pay annual fees:
    Platinum Card: $695/year
    Gold Card: $325/year
    Corporate cards: $250-500/year
  These fees are paid regardless of spending level or credit performance.
  FY2025: $10 billion in card fees (+18%). This is the fastest-growing and
  highest-quality revenue stream — zero credit risk, extremely sticky.
  Membership in Amex is aspirational; churn rates are very low (<5%/yr).

THE CLOSED-LOOP DATA ADVANTAGE
================================
Visa and Mastercard are "blind pipes" — they know money moved from A to B but
cannot see WHAT was purchased, WHERE, by WHOM, or for HOW MUCH at the item level.
AXP sees EVERYTHING because it owns both ends of the transaction:

  → AXP knows: "John Smith, $1,200 household income bracket, spent $450 at
    Michelin-starred restaurants last month, $2,100 at luxury hotels, and
    $300 on business-class flights."

This data moat enables:
  1. Superior credit risk management (predict defaults before they happen)
  2. Targeted marketing (AXP can sell merchant data/advertising to luxury brands)
  3. Premium offers and benefits (Centurion Lounges, hotel upgrades, concierge)
  4. Cross-selling financial products to verified high-income customers

Visa and Mastercard do NOT have this. This is AXP's structural moat vs V/MA.

MILLENNIALS & GEN-Z — THE LONG-TERM GROWTH DRIVER
===================================================
AXP's traditional customer base was Baby Boomers (business travelers, corporate
executives). The transformational insight of CEO Stephen Squeri (since 2018):
Millennials and Gen-Z aspirationally WANT to be Amex card members.

Evidence:
  - 60%+ of new card acquisitions in FY2025: Millennials and Gen-Z
  - Premium card member acquisition record set in FY2024 AND FY2025
  - These customers have 20-30 year spending horizon ahead → lifetime value
    multiple of what a Boomer member creates
  - Amex benefits (Centurion Lounge, dining credits, hotel status) resonate
    strongly with younger premium earners

The generational transition de-risks the "Boomers aging out" concern entirely.

CREDIT QUALITY — THE BEAR CASE ADDRESSED
==========================================
AXP bears argue: "AXP is just a bank with a fancy name. When recession hits,
credit losses will spike and the premium image will shatter."

The data says otherwise:
  Net write-off rate (Q1 2026): ~2.1% of card member loans
  Industry average credit card write-off: ~3.8-4.5%
  AXP write-offs have been consistently 40-60% below industry for a decade.

WHY premium customers default less:
  1. Wealth buffer: most AXP card members have $100K+ household income
     — they can absorb a job loss for 6-12 months
  2. Charge card culture: many AXP products are PAY-IN-FULL (no revolving)
     — this screens for financially disciplined customers
  3. Status loss: losing an Amex card (especially Platinum/Centurion) is
     a status event for premium customers — they pay to avoid that

That said: AXP is NOT immune to recession. FY2020 showed what a real shock
looks like. The $3.77 COVID EPS was driven by:
  (a) Travel/restaurant spending collapse (AXP's biggest categories)
  (b) $5.7B in reserve builds (on top of actual charge-offs)
  COVID was an extreme scenario specific to AXP's spend categories.

A "normal" recession (unemployment +2-3pp): billed business -20-25%,
provisions ×1.5-2×, EPS ≈ $7-9. This is our EPP scenario.

AXP AT $311 — ENTRY/EXIT FRAMEWORK
=====================================
  ◉ BUY        : $180-230  (1.4-1.8× EPP; severe recession; franchise impairment fear)
  ◎ ACCUMULATE : $230-285  (1.8-2.3× EPP; near 52-wk low territory; April 2026 entry)
  ◐ WATCHLIST  : $285-340  (current at $311; above April low; below analyst PTs)
  ▷ HOLD/TRIM  : $340-390  (approaching analyst targets; premium well-recognised)
  ✕ AVOID      : >$390     (near 52-wk high $387; ratio_b >4×; IB + fee cycle priced)

The 52-wk low of $281.47 (April 2026) at ratio_b {ratio_b_52wk_low:.2f}× was the ACCUMULATE entry.
Buying there gave +10.5% gain to current; buying below $270 would have been
even better. At $311, WATCHLIST — strong business, attractive vs peers,
not "on sale" but not expensive. Analyst avg PT $362-375 = +16-20% upside.
Add aggressively on any pullback to $270-295 (ratio_b 1.0-1.1× = ACCUMULATE).
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
  Market cap      : ~${mkt_cap_b:.0f}B   |   Shares: ~{SHARES_M/1000:.3f}B
  Dividend (ann)  : ${DIVIDEND_ANN:.2f}   |   Yield: {DIVIDEND_ANN/CURRENT_PRICE*100:.2f}%
  Equity/share    : ~${EQUITY_PER_SHR:.2f}  |   P/B: {pb_current:.1f}×  (franchise value >> book)
  ROE (Q1 2026)   : {ROE:.1f}%     |   Closed-loop network (owns issuing + network)
  Forward P/E     : {CURRENT_PRICE/EPS_NOW:.1f}×  (on FY2026E ${EPS_NOW:.2f})
  vs Visa         : 27.5×  vs MA: 25.6×  ← AXP cheapest payment network by P/E
  Berkshire stake : {BERKSHIRE_STAKE:.2f}%  (151.61M shares; sold V/MA Q1 2026; HELD AXP)
  BRK dividends   : $576M/yr from AXP  ($3.80 × 151.61M shares — confirmed exact)
  Net card fees   : ${NET_CARD_FEES:.0f}B/yr FY2025  (+18%; zero-credit-risk recurring revenue)
  Billed business : ${BILLED_BUS_Q1:.0f}B Q1 2026  (+10% YoY; highest growth in 3 years)

  II. EPS HISTORY (GAAP diluted)
  {line}
  FY2022  : ${EPS_HISTORY['FY2022']:.2f}   (post-COVID travel rebound; billed business +25% YoY)
  FY2023  : ${EPS_HISTORY['FY2023']:.2f}   (+{(EPS_HISTORY['FY2023']/EPS_HISTORY['FY2022']-1)*100:.1f}%; record card acquisitions; net card fees growing strongly)
  FY2024  : ${EPS_HISTORY['FY2024']:.2f}   (+{(EPS_HISTORY['FY2024']/EPS_HISTORY['FY2023']-1)*100:.1f}%; record year; Millennials/Gen-Z card acquisition inflection)
  FY2025  : ${EPS_HISTORY['FY2025']:.2f}   (+{(EPS_HISTORY['FY2025']/EPS_HISTORY['FY2024']-1)*100:.1f}%; record revenue $72B; net card fees $10B (+18%))
  FY2026E : ${EPS_NOW:.2f}   (+{(EPS_NOW/EPS_HISTORY['FY2025']-1)*100:.1f}%; guidance $17.30-$17.90; Q1 actual $4.28 (+18%))
  FY2027E : ${CONS_EPS_2YR:.2f}   (used for Method B; analyst consensus range $19.08-$21.70)
  Q1 2026 : $4.28   (+18% YoY; ROE 35%; billed $428B +10%; guidance reaffirmed)

  Note: FY2020 EPS was $3.77 (COVID: travel collapse + $5.7B reserve builds).
  This is the most relevant historical stress test — and AXP recovered to
  record EPS within 2 years. Premium franchise resilience confirmed.

  III. EPP & METHOD B
  {line}
  EPS_TROUGH  : ${EPS_TROUGH:.2f}/share  (severe recession; NOT COVID black swan $3.77)
  EPP_MIN_PE  : {EPP_MIN_PE}×           (AXP franchise premium; market assigns 18× even at trough)
  EPP (floor) : ${EPP:.2f}        (= ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×; COVID panic low $67 = 17.8× $3.77 EPS)
  EPP gap     : +{epp_gap_pct:.1f}%    (current is {CURRENT_PRICE/EPP:.1f}× above EPP floor)

  CONS_EPS_2YR: ${CONS_EPS_2YR:.2f}/share  (FY2027E consensus)
  CONS_EXIT_PE: {CONS_EXIT_PE}×           (modest re-rating vs current {CURRENT_PRICE/EPS_NOW:.1f}×; below V/MA multiples)
  Method B    : ${price_b:.2f}       (= ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×; above analyst avg PT $362-375)
  Upside to B : +{upside_b_pct:.1f}%
  Downside EPP: {dn_epp_pct:.1f}%

  ┌─────────────────────────────────────────────────────────────────────┐
  │  RATIO B = ({CURRENT_PRICE:.2f} − {EPP:.2f}) / ({price_b:.2f} − {CURRENT_PRICE:.2f})               │
  │           = {CURRENT_PRICE-EPP:.2f} / {price_b-CURRENT_PRICE:.2f} = {ratio_b:.2f}×                              │
  │  SIGNAL   = {signal}                                       │
  └─────────────────────────────────────────────────────────────────────┘
  52-wk low  ${PRICE_52W_LOW:.2f}: ratio_b {ratio_b_52wk_low:.2f}× = ◎ ACCUMULATE  ← April 2026 entry
  52-wk high ${PRICE_52W_HIGH:.2f}: ratio_b {ratio_b_52wk_hi:.1f}×  = ✕ AVOID       ← peak exit signal

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
  Market composite  : {market_composite:.3f}  ({"BASE" if 1.625<=market_composite<2.375 else "BEAR" if market_composite<1.625 else "BULL" if market_composite < 3.125 else "XBULL"})
  Adj composite     : {adj_composite:.3f}  ({"BASE" if 1.625<=adj_composite<2.375 else "BEAR" if adj_composite<1.625 else "BULL" if adj_composite < 3.125 else "XBULL"})
  Softmax weights at adj composite ({adj_composite:.3f}):""")

    scen_prices = {"BEAR": scenarios["BEAR"], "BASE": scenarios["BASE"],
                   "BULL": scenarios["BULL"], "XBULL": scenarios["XBULL"]}
    for k, w in adj_weights.items():
        print(f"    {k:<6}: {w*100:.1f}%  (${scen_prices[k]:.0f})")

    print(f"""  Expected price (adj): ${adj_ev:.0f}  vs current ${CURRENT_PRICE:.2f}  (Δ {(adj_ev/CURRENT_PRICE-1)*100:+.1f}%)

  VI. SCENARIOS SUMMARY
  {line}
  BEAR  (${scenarios['BEAR']:.0f}) : Severe recession + travel collapse. Billed business -35%;
               provisions ×2 ($3.0B→$6.0B); net card fees stall; marketing cut.
               EPS $7.00 × 18× = $126. COVID showed what real shock looks like ($3.77 EPS;
               stock to $67). This scenario is WORSE than COVID in EPS terms
               (no specific pandemic shutdown, but prolonged spending depression).
               {(scenarios['BEAR']/CURRENT_PRICE-1)*100:.0f}% from current.

  BASE  (${scenarios['BASE']:.0f}) : Soft landing. Billed +7%; net card fees +14%; provisions stable;
               ROTE holds 30%+. FY2027E $20.30 × ~18.5× = $375. Analyst avg PT
               $362-375 is this scenario. Ongoing generational acquisition cycle.
               {(scenarios['BASE']/CURRENT_PRICE-1)*100:+.0f}% from current.

  BULL  (${scenarios['BULL']:.0f}) : = price_b. ROE 35% fully recognised in multiple. Billed +10%;
               net card fees become 30%+ of revenue; P/E re-rates to 21× as
               credit quality through-cycle proves V/MA discount unjustified.
               FY2027E $20.30 × 21×. Buffett's conviction is proven correct.
               {(scenarios['BULL']/CURRENT_PRICE-1)*100:+.0f}% from current.

  XBULL (${scenarios['XBULL']:.0f}) : Full convergence with V/MA multiples. Net card fees exceed
               $15B; AXP's closed-loop data becomes most valuable financial
               dataset globally (AI-powered targeting). FY2028E EPS ~$25 × 22×.
               Buffett exits at ~$600 after tripling again from current levels.
               BRK receives $1B+/yr in dividends on original $1.3B investment.
               {(scenarios['XBULL']/CURRENT_PRICE-1)*100:+.0f}% from current.

{"=" * 72}
  END OF REPORT -- {TICKER}  |  Generated 2026-05-26
{"=" * 72}""")
