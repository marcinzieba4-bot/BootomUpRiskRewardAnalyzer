"""
Visa Inc. (NYSE: V) — BottomUp Risk/Reward Signal Model

SIGNAL:  ◐ WATCHLIST
RATIO B: 1.71x  (Method B $14 × 30× = $420; ratio 153.96/90.04 = 1.71×)
DATE:    2026-05-26

NOTE: Visa's fiscal year ends September 30. "FY2026" = Oct 2025 – Sep 2026.
EPS figures are non-GAAP adjusted (Visa's standard reporting; excludes litigation
charges, certain M&A items). GAAP EPS is materially lower in years with large
litigation accruals (FY2023: ~$7.38 GAAP vs ~$8.77 adj; FY2025: ~$9.55 GAAP).
"""

import math

TICKER  = "V"
COMPANY = "Visa Inc."
SECTOR  = "Payment Networks · Digital Commerce Infrastructure · Cross-Border Payments · Agentic Commerce"

# ── current price (Yahoo Finance, 2026-05-22) ────────────────────────────
CURRENT_PRICE  = 329.96   # V — fetched from Yahoo Finance, 2026-05-22
PRICE_52W_LOW  = 293.89   # 2026-04-01 (broader market selloff; was ACCUMULATE entry)
PRICE_52W_HIGH = 375.51   # 2025-06-11
SHARES_M       = 2100.0   # fully diluted (Class A + B + C); aggressive buyback programme
DIVIDEND_ANN   = 2.68     # $0.67/quarter; 17 consecutive years of dividend growth

# ── EPS history — non-GAAP adjusted ─────────────────────────────────────
EPS_FY2022 =  7.50   # adj; GAAP lower due to litigation; post-COVID cross-border recovery
EPS_FY2023 =  8.77   # adj; GAAP $7.38 (large litigation accrual for DOJ/interchange)
EPS_FY2024 =  9.93   # adj; GAAP $8.81; cross-border fully normalised; buybacks kick in
EPS_FY2025 = 10.50   # adj; GAAP $9.55; continued 10-11% growth; tap-to-pay surpassed 80%
EPS_NOW    = 12.00   # FY2026E adj; Q2 FY2026 actual $3.31 (+20% YoY); guidance raised
                     # to "low double-digit to low teens" net revenue; adj EPS "low teens"

# ── EPP — earnings power price (structural floor) ────────────────────────
EPS_TROUGH = 8.00    # severe recession: global payment volume -12%, cross-border -30%
                     # (similar to COVID 2020 cross-border collapse). Revenue -15% from
                     # FY2025E; operating leverage means EPS -20-25% from ~$10.50 base.
                     # Visa's COVID FY2020 adj EPS ~$5.44 (cross-border near-zero briefly);
                     # modern Visa more diversified (Visa Direct, debit, e-commerce).
                     # $8.00 reflects cross-border shock + volume contraction WITHOUT
                     # the complete travel lockdown of 2020 that was a 1-in-50-year event.
EPP_MIN_PE = 22      # Payment network trough P/E. Higher than typical company (~10-12×)
                     # because: (1) asset-light model = essentially no capex/credit risk;
                     # (2) revenue declines reverse faster than earnings (cost base fixed);
                     # (3) network effect means competitive position unchanged in a recession;
                     # (4) Visa NEVER traded below 20× even at COVID trough (May 2020: ~$170
                     # with ~$5.44 stress EPS = 31.2× — market knew the moat was intact).
                     # 22× is conservative vs actual 2020 trough; reflects more pessimism.
EPP = EPS_TROUGH * EPP_MIN_PE   # $176.00

# ── Method B — 2-year normalised upside ceiling ───────────────────────────
CONS_EPS_2YR = 14.00   # FY2027E adj EPS. Analysts project 11-13% growth FY2026→FY2027
                       # (Zacks: +13.2% for FY2027; one source: 18% CAGR through FY2028).
                       # $14.00 = FY2026E $12.00 × 1.167 (+16.7%) — slightly above base
                       # consensus, reflecting accelerating agentic commerce and buyback tailwind.
                       # Visa returned $9.2B to shareholders in Q2 FY2026 alone; float reduction
                       # mechanically boosts EPS 3-4% annually above revenue growth.
CONS_EXIT_PE = 30      # Premium payment network historical multiple. Range: 20-40×.
                       # Current FY2026E: 27.5×. Bull case requires modest re-rating to 30×
                       # — justifiable if agentic commerce materialises as a meaningful new
                       # revenue stream and the DOJ lawsuit settles with no structural remedy.
price_b = CONS_EPS_2YR * CONS_EXIT_PE   # $420.00

ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
# = (329.96 - 176.00) / (420.00 - 329.96) = 153.96 / 90.04 = 1.71×
# → ◐ WATCHLIST. Great business at a fair price. The 52-wk low of $293.89
# (April 1, 2026) was the ACCUMULATE entry (ratio_b ~0.93×). That entry has
# partially closed. Current risk/reward: +27% to Method B vs -47% to EPP.

epp_gap_pct = (CURRENT_PRICE - EPP) / EPP * 100
# = (329.96 - 176) / 176 × 100 = 87.5%

# ── price scenarios ───────────────────────────────────────────────────────
PRICE_BEAR  = 176    # = EPP. Severe recession + cross-border collapse. COVID-2020 style
                     # but without government stimulus normalising within 6 months.
                     # $8 × 22× = $176. P/E still elevated vs banks because moat intact.
                     # -47% from current. Visa fell to ~$170 in May 2020 (briefly).
PRICE_BASE  = 385    # Soft landing. FY2027E $14.00 × 27.5× = $385.
                     # Steady 11-13% EPS growth; payment volumes +8-10%; multiple flat.
                     # No structural regulatory remedy; DOJ lawsuit settles behaviourally.
                     # +17% from current. Visa grinds higher via EPS growth + buybacks.
PRICE_BULL  = 420    # = price_b. FY2027E $14.00 × 30×. Multiple re-rates on:
                     # (1) agentic commerce becomes measurable revenue (~$0.5-1B/yr);
                     # (2) DOJ lawsuit dismissed or settled favorably; (3) stablecoin
                     # integration expands Visa's TAM to crypto-native flows.
                     # +27% from current.
PRICE_XBULL = 525    # FY2028E ~$17.50 × 30×. Agentic commerce TAM fully manifests:
                     # every AI agent (shopping, travel, procurement) routes through
                     # Visa Intelligent Commerce; total transaction volume doubles;
                     # cross-border expands with global agentic purchasing.
                     # +59% from current. Requires 2-3 year technology adoption cycle.

# ── SCA (stock-specific composite adjustment) ────────────────────────────
SCA_FACTORS = [
    # (description, score, weight)
    ("Agentic commerce: Trusted Agent Protocol; 16B tokens = every AI agent routed securely; $7B stablecoin annualised; first-mover in AI payment rails", +0.40, 0.25),
    ("Cross-border recovery + travel boom: cross-border ex-intra-EU +11% Q1 FY2026; travel +10%; Visa Direct +23% YoY; e-commerce cross-border +12%", +0.25, 0.20),
    ("Tap-to-pay + cash displacement: >80% face-to-face globally; US 70%; EM cash-to-card conversion adds 1-2% annual volume without needing economic growth", +0.20, 0.15),
    ("DOJ antitrust (debit monopoly): filed Sep 2024; accused Visa of 'monopolizing' debit market; forced routing mandates could trim debit fee income $0.5-1B/yr", -0.35, 0.25),
    ("Stablecoin / CBDC disruption: USDC/USDT on-chain settlement growing; central bank CBDCs in 130+ countries; could bypass card rails for cross-border in 5-10yr", -0.20, 0.15),
]

sca_raw = sum(s * w for _, s, w in SCA_FACTORS)   # +0.0625
sca_adj = sca_raw / 2.0                             # +0.031

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
Special context: Visa is the world's largest payment network — a software-
defined global toll road on commerce. Key model adaptations vs a typical
industrial or pharma company:
  • No credit risk: Visa never lends money. Issuing banks bear all default
    risk. Visa simply processes and earns a tiny percentage (~0.1%) of volume.
  • ~50% operating margins: one of the highest in the S&P 500; margins stable
    across economic cycles because cost base is almost entirely fixed (tech).
  • Recession revenue resilience: even in severe downturns, people still spend
    on groceries, utilities, healthcare — all increasingly on card rails.
  • EPP_MIN_PE = 22×: never traded below 20× even at the COVID trough (May 2020
    low ~$170; stress EPS ~$5.44 = 31.2× — market priced in the moat's permanence).

Key metrics (Q2 FY2026, Jan–Mar 2026):
  Payment volume      : ~$4T/quarter  (+8% constant dollar YoY)
  Cross-border vol    : +11% ex-intra-EU  (travel +10%; e-commerce +12%)
  Visa Direct txns    : 3.7B/quarter  (+23% YoY)
  Visa tokens         : 16B           (near-zero fraud; AI agent payments ready)
  Credentials         : 5B+           (globally; tap-to-pay >80% face-to-face)
  Stablecoin run-rate : $7B/yr        (9 blockchains; April 2026)""")

    print(f"""
EPP (Earnings Power Price) — structural floor
  = EPS_TROUGH × EPP_MIN_PE
  Stress EPS ($8.00) × 22× floor. EPS_TROUGH reflects COVID-2020 style shock:
  global payment volume -12%, cross-border -30% (without complete travel lockdown).
  FY2020 adj EPS ~$5.44 was a true once-in-generation event; $8.00 is a more
  realistic modern stress (Visa Direct/debit/e-commerce diversify revenue).
  The 22× floor P/E reflects that Visa's moat — network effects, 300B annual
  transactions, 14,500+ financial institution partnerships — doesn't diminish
  in a recession. Recovery is visible and priced in from day one of the downturn.
  EPP = ${EPP:.2f}.
  Calibration: 52-wk low ${PRICE_52W_LOW:.2f} (Apr 1, 2026) ÷ $8.00 = {PRICE_52W_LOW/EPS_TROUGH:.1f}× stress EPS.
  The correction low was still {PRICE_52W_LOW/EPS_TROUGH:.1f}× stress EPS — confirming $176 EPP is
  a severe catastrophe scenario used to anchor downside, not a realistic near-term risk.

Method B — 2-year normalised upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E adj EPS ~${CONS_EPS_2YR:.2f} ({CONS_EPS_2YR/EPS_NOW*100-100:.0f}% above FY2026E ${EPS_NOW:.2f}; Zacks consensus +13.2%
  for FY2027; above-consensus buyback boost ~3-4% + agentic tailwind) × {CONS_EXIT_PE}×
  exit P/E (current 27.5×; requires modest re-rating to 30× — achievable if DOJ
  resolves favorably and agentic commerce revenue becomes measurable).
  = ${price_b:.2f}.
  Ratio B = (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f}) = ${CURRENT_PRICE-EPP:.2f} / ${price_b-CURRENT_PRICE:.2f} = {ratio_b:.2f}×
  → {signal}. Visa is a world-class compounder at a fair price.
  Method B upside: +{(price_b/CURRENT_PRICE-1)*100:.1f}% to ${price_b:.0f}. Downside to EPP: -{(1-EPP/CURRENT_PRICE)*100:.1f}%.
  Note: The 52-wk low ${PRICE_52W_LOW:.2f} (April 1, 2026) was an ACCUMULATE entry at
  ratio_b ~0.93×. That window has partially closed (+{(CURRENT_PRICE/PRICE_52W_LOW-1)*100:.0f}% in 7 weeks).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

    print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VISA: THE TOLL ROAD ON GLOBAL COMMERCE — AGENTIC COMMERCE IS THE NEXT LANE
===========================================================================

Visa is one of the greatest businesses ever built. Consider the core economics:
  • Visa processes ~300 billion transactions per year (900M daily)
  • It charges ~0.1% of the value of every transaction as revenue
  • It has almost no incremental cost for an additional transaction (fixed tech)
  • It takes on zero credit risk (issuing banks lend; Visa just processes)
  • It has built a network connecting 14,500+ financial institutions and 175M+
    merchant locations — a 60-year moat that would cost $50-100B+ to replicate
    and still wouldn't have the trust and acceptance of the Visa brand

The result: ~50% operating margins, EPS growing 10-17%/yr, and a business
model that gets MORE defensible as digital payments displace cash. In 2026,
for the first time in history, more than half of all global consumer payments
are made with card credentials — a secular shift Visa has been riding for decades
and which still has 30-40% of global payments to convert (remaining cash usage).

Q2 FY2026 — STRONGEST REVENUE GROWTH SINCE 2022
================================================
  Revenue (net):    $11.23B  (+17% YoY; strongest since Q3 FY2022)
  Adjusted EPS:     $3.31    (+20% YoY; beat estimate $3.05-3.10 by $0.21-0.26)
  Payment volume:   ~$4T     (+8% constant dollar)
  Cross-border:     +11% ex-intra-EU
  Visa Direct:      3.7B txns (+23% YoY)
  Capital return:   $9.2B    (buybacks + dividends in a single quarter — staggering)

Following Q2, Visa raised its FY2026 guidance:
  Net revenue growth: "low double-digit to low teens" (from "high single digit to
  low double-digit") — upgrade driven by IB volume, cross-border strength, and
  the emerging agentic commerce tailwind
  Adj EPS growth:     "low teens" — approximately 12-14% growth vs FY2025

Sixteen analysts upgraded estimates post-earnings. The consensus reaction was
cautiously bullish — Q2 was undeniably strong, but the stock had already run
+12% from its April 1 low ($293.89) before earnings.

THE AGENTIC COMMERCE OPPORTUNITY: VISA AS AI INFRASTRUCTURE
==========================================================
This is Visa's most important 5-year growth narrative. As AI agents become
the primary way consumers and businesses discover, compare, and purchase goods
and services, the payment infrastructure layer becomes more, not less, important.

Key developments:
  • Trusted Agent Protocol (Oct 2025): open framework enabling secure AI
    agent-driven checkout; Visa + 10+ partners; leverages existing web infra
  • Visa Intelligent Commerce: API platform for AI agents to access Visa payment
    rails with identity verification, fraud detection, and tokenisation built in
  • Visa Ready Programme: 16B Visa tokens = every AI agent can be bound to a
    specific credential, eliminating fraud in autonomous transactions
  • Stablecoin settlement: $7B annualised run-rate across 9 blockchains (Apr 2026)
    — Visa is POSITIONING itself as the settlement layer for crypto-native commerce,
    not fighting it

CEO Ryan McInerney: "We believe we are well positioned to be the infrastructure
provider and key enabler in agentic commerce so that every agent interaction is
trusted and secure."

The commercial implications: if every AI shopping/travel/procurement agent routes
through Visa's infrastructure, and total AI-driven e-commerce reaches $500B-1T by
2028-2030, Visa earns its ~0.1% network fee on a new, incremental volume stream
that doesn't require any additional capex. This is the XBULL scenario.

The bear case on agentic commerce: AI agents could also route around card rails
entirely using bank-to-bank transfers, stablecoins, or proprietary fintech rails.
This is why the DOJ lawsuit is so important — if Visa is forced to open its debit
network to competitors, the regulatory precedent could eventually reach credit too.

THE DOJ LAWSUIT: THE KEY RISK
==============================
In September 2024, the U.S. Department of Justice filed an antitrust lawsuit
accusing Visa of illegally monopolising the debit card market. Key allegations:
  1. Visa charges "above-competitive" fees in debit (debit is ~45% of volume)
  2. Visa uses agreements with banks and tech companies (including Apple, PayPal)
    to suppress competition from rivals like FedNow, Zelle, and debit processors
  3. Visa's anti-steering agreements prevent merchants from routing transactions
    away from Visa's network

The legal timeline and outcomes:
  • Case is proceeding through discovery; trial likely 2026-2027
  • Most likely outcome: behavioural remedies (forced routing rules; reduced
    anti-steering agreements) rather than structural breakup
  • Financial impact of behavioural remedies: $0.5-1.0B in annual debit fee
    income at risk (3-8% of total revenue). Manageable, not existential.
  • The DOJ has NOT accused Visa of credit card monopolisation — credit is
    40-50% of revenue and remains largely untouched by the lawsuit

Visa argued in its Q2 2026 earnings call that "innovation and competition have
never been more robust in payments" — pointing to PayPal, Stripe, Apple Pay,
and ACH/FedNow as evidence of a competitive market. The courts will decide.

COMPETITIVE MOAT: HOW DURABLE IS THE VISA NETWORK?
===================================================
Threats (real but long-duration):
  • Stablecoins: USDC/USDT growing for cross-border B2B; Visa itself processing
    stablecoin settlements = BOTH threat and opportunity; $7B annualised
  • CBDCs: 130+ countries researching; implementation 5-10 years away
  • Pay-by-bank / FedNow: instant bank-to-bank gaining traction for bill pay;
    ~5-10% of debit volume at risk; merchants pay less but banks earn less too
  • Buy Now Pay Later: Klarna, Affirm growing; but these RIDE ON Visa rails
    (BNPL providers fund through bank accounts or debit; still transacts on V)

Why the moat remains:
  • Consumer trust: "Visa" is synonymous with payment acceptance in 200+ countries
  • Fraud protection: 16B tokens + AI fraud detection = unmatched security vs bank rails
  • Rewards ecosystem: airline miles, cashback, hotel points all funded through
    interchange fees and incentivise card usage over alternatives
  • Network effects are self-reinforcing: 175M merchant locations accept Visa;
    consumers carry Visa because it's accepted everywhere; merchants accept it
    because consumers carry it. This circular reinforcement took 60 years to build.

ENTRY/EXIT FRAMEWORK
====================
  ◉ BUY        : $255-275  (EPP floor ×1.45-1.55; COVID-2020 range revisited)
  ◎ ACCUMULATE : $285-315  (52-wk low territory; ratio_b ~0.7-1.1×)
  ◐ WATCHLIST  : $315-345  (current; fair value for quality compounder)
  ▷ HOLD/TRIM  : $345-380  (premium to fair value; near Method B territory)
  ✕ TRIM HARD  : >$380     (above Method B; approaching ATH $375.51)

The April 1, 2026 low of $293.89 was the entry. +12% in 7 weeks has brought
it into WATCHLIST territory. Patient investors should accumulate on pullbacks
to $290-315 range; the thesis is intact but current pricing offers less margin.

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
  Market cap      : ~${mktcap_b:.0f}B   |   Shares (diluted): ~{SHARES_M/1000:.2f}B
  Dividend (ann)  : ${DIVIDEND_ANN:.2f}   |   Yield: {DIVIDEND_ANN/CURRENT_PRICE*100:.2f}%
  Forward P/E     : {CURRENT_PRICE/EPS_NOW:.1f}×  (on FY2026E adj ${EPS_NOW:.2f})
  FY2027E P/E     : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (on FY2027E adj ${CONS_EPS_2YR:.2f})
  PEG ratio       : {(CURRENT_PRICE/EPS_NOW)/13:.2f}×  (P/E {CURRENT_PRICE/EPS_NOW:.1f}× ÷ 13% EPS growth rate)""")

    print(f"""
  II. EPS HISTORY (non-GAAP adjusted; Visa fiscal year ends Sep 30)
  ----------------------------------------------------------------------
  FY2022  : ${EPS_FY2022:.2f}  (GAAP lower; post-COVID cross-border recovery; DOJ accruals)
  FY2023  : ${EPS_FY2023:.2f}  (GAAP ~$7.38; litigation charges; cross-border +15%)
  FY2024  : ${EPS_FY2024:.2f}  (GAAP ~$8.81; normalised cross-border; buybacks accelerate)
  FY2025  : ${EPS_FY2025:.2f}  (GAAP ~$9.55; tap-to-pay >80%; Visa Direct +20%+ YoY)
  FY2026E : ${EPS_NOW:.2f}  (guidance: "low teens" adj EPS growth; Q2 actual $3.31 +20% YoY)
  FY2027E : ${CONS_EPS_2YR:.2f}  (consensus +11-13%; used for Method B)
  Q2 FY26 : $3.31  (record; +20% YoY; revenue $11.23B +17%; strongest since FY2022)

  III. EPP & METHOD B
  ----------------------------------------------------------------------
  EPS_TROUGH  : ${EPS_TROUGH:.2f}/share  (COVID-style: vol -12%, cross-border -30%)
  EPP_MIN_PE  : {EPP_MIN_PE}×          (network moat justifies premium trough P/E; never <20× in history)
  EPP (floor) : ${EPP:.2f}       (= ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×)
  EPP gap     : +{epp_gap_pct:.1f}%     (current price is {epp_gap_pct/100:.1f}× above EPP floor)

  CONS_EPS_2YR: ${CONS_EPS_2YR:.2f}/share  (FY2027E adj; +{CONS_EPS_2YR/EPS_NOW*100-100:.0f}% above FY2026E)
  CONS_EXIT_PE: {CONS_EXIT_PE}×          (modest re-rating from current 27.5×; DOJ resolved; agentic visible)
  Method B    : ${price_b:.2f}       (= ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×)
  Upside to B : +{(price_b/CURRENT_PRICE-1)*100:.1f}%
  Downside EPP: -{(1-EPP/CURRENT_PRICE)*100:.1f}%

  ┌─────────────────────────────────────────────────────────────────────┐
  │  RATIO B = ({CURRENT_PRICE:.2f} − {EPP:.2f}) / ({price_b:.2f} − {CURRENT_PRICE:.2f})             │
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
  BEAR  (${PRICE_BEAR}) : Severe recession + COVID-style cross-border collapse (-30%).
               Global payment volume -12%. Visa Direct + e-commerce partly offset.
               EPS stress $8.00; market prices moat permanence at 22×.
               EPP = $8 × 22× = $176. P/E trough higher than banks because
               recovery is visible and faster. -{(1-PRICE_BEAR/CURRENT_PRICE)*100:.0f}% from current.

  BASE  (${PRICE_BASE}) : Soft landing. Payment volumes +8-10%; cross-border +10-12%.
               FY2027E EPS $14 × 27.5× = $385 (flat multiple; no re-rating).
               DOJ lawsuit: behavioural remedy, ~$0.5B annual debit impact absorbed.
               Agentic commerce: early stage, not yet material to revenue.
               Visa compounds via EPS growth + buybacks. +{(PRICE_BASE/CURRENT_PRICE-1)*100:.0f}% from current.

  BULL  (${PRICE_BULL}) : Agentic commerce + DOJ win. FY2027E $14 × 30×.
               DOJ lawsuit dismissed or settled favourably; anti-steering rules
               unchanged; Visa moat confirmed legally. Agentic commerce generates
               first measurable incremental revenue ($0.5-1B/yr). Stablecoin
               integration on-boarded major banks. Multiple re-rates to 30×.
               +{(PRICE_BULL/CURRENT_PRICE-1)*100:.0f}% from current.

  XBULL (${PRICE_XBULL}) : AI commerce infrastructure wave. FY2028E ~$17.50 × 30×.
               Every major AI agent (Amazon Rufus, OpenAI Operator, Google Gemini
               Shopping) routes through Visa Intelligent Commerce; total AI-
               attributed transaction volume $500B+ by 2028; stablecoin settlement
               runs $50B+/yr on Visa rails; tap-to-pay at 95% globally.
               +{(PRICE_XBULL/CURRENT_PRICE-1)*100:.0f}% from current.
""")

    print("=" * 72)
    print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-26")
    print("=" * 72)
