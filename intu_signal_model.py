#!/usr/bin/env python3
"""
intu_signal_model.py  —  Intuit Inc. (NASDAQ: INTU)
Bottom-Up Risk/Reward Signal Model
All prices and EPS in USD.
"""

import math, sys, io, contextlib

TICKER        = "INTU"
COMPANY       = "Intuit Inc."
EXCHANGE      = "NASDAQ"
FY_END        = "July 31 (fiscal year; FY2026 ends Jul 31, 2026)"
SHARES_M      = 282.0           # million diluted shares (Q3 FY2026: 283M; buybacks ongoing)

CURRENT_PRICE = 319.94          # INTU — fetched from web search, 2026-05-24
                                 # Day range: $306.51–$321.04; near 52-wk low
                                 # 52-wk high: $813.70 (likely ATH); 52-wk low: $302.36
                                 # Stock -61% from ATH; -20.3% on Q3 FY2026 results (May 20 2026)

# ── EPP FLOOR ──────────────────────────────────────────────────────────────
EPS_TROUGH        = 11.85       # FY2022 non-GAAP; lowest in 4-year window; EPS has NEVER declined
EPS_TROUGH_PRICE  = 302.36      # 52-wk low (May 2026; post-Q3 selloff + workforce cut announcement)
                                 # $302.36 / $23.82 FY2026E = 12.7x — historical valuation floor
EPP_MIN_PE        = 20          # structural floor; below historical 30-50x range; accounts for
                                 # IRS Direct File risk + AI tax disruption; reflects TurboTax near-
                                 # monopoly + QuickBooks 80% SMB share; 20x = "stagnating software" pricing
EPS_FY2025        = 20.10       # FY2025 (ended Jul 31, 2025); non-GAAP diluted EPS; grew ~18-19% YoY
EPS_NOW           = 23.82       # FY2026E raised guidance midpoint ($23.80–$23.85, updated May 20 2026);
                                 # Q3 FY2026 EPS $12.80 (+10%); Q2 $4.15 (+25%); guidance raised 3.2% vs prior
EPP               = round(EPS_NOW * EPP_MIN_PE, 2)    # $476.40

below_floor       = CURRENT_PRICE < EPP               # True — deepest below-EPP in coverage
epp_gap_pct       = round((CURRENT_PRICE - EPP) / EPP * 100, 1)    # -32.9%

# ── METHOD B ───────────────────────────────────────────────────────────────
CONS_EPS_2YR  = 29.00           # FY2028E non-GAAP (FY ends Jul 2028; ~26 months from analysis);
                                 # ~10% CAGR from FY2026E $23.82 — CONSERVATIVE vs historical 18%+;
                                 # accounts for IRS Direct File TAM erosion + QB growth offset by
                                 # Credit Karma monetisation drag; $29 is well below 15% CAGR ($31.50)
CONS_EXIT_PE  = 27              # conservative exit; historical INTU range 30–55x; using 27x to
                                 # persist IRS risk discount; re-rating to 35x+ is BULL upside optionality
price_b       = round(CONS_EPS_2YR * CONS_EXIT_PE, 2)    # $783.00
ratio_b       = round((CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE), 2)   # -0.34x → BUY below floor

# ── SOFTMAX ENGINE ─────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  {"price": 150.0,   "eps": 10.0,  "pe": 15.0,
              "desc": "IRS Direct File kills TurboTax TAM; QB loses to AI startups; EPS collapses to $10"},
    "BASE":  {"price": 783.0,   "eps": 29.0,  "pe": 27.0,
              "desc": "FY2028E $29 × 27x; TurboTax moat holds; QB Enterprise ramp; conservative re-rating"},
    "BULL":  {"price": 1020.0,  "eps": 34.0,  "pe": 30.0,
              "desc": "AI financial platform wins; QB Enterprise scales; TurboTax ARPU lifts; 30x re-rate"},
    "XBULL": {"price": 1400.0,  "eps": 40.0,  "pe": 35.0,
              "desc": "Intuit = global AI financial OS for SMBs; full re-rating to historical premium multiples"},
}

T        = 0.60
CENTRES  = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}

def softmax_ev(composite):
    logits = {k: -(composite - CENTRES[k])**2 / T for k in SCENARIOS}
    max_l  = max(logits.values())
    exps   = {k: math.exp(logits[k] - max_l) for k in SCENARIOS}
    total  = sum(exps.values())
    probs  = {k: exps[k] / total for k in SCENARIOS}
    ev     = sum(probs[k] * SCENARIOS[k]["price"] for k in SCENARIOS)
    return ev, probs

def infer_composite(target_price):
    lo, hi = 1.0, 4.0
    for _ in range(60):
        mid = (lo + hi) / 2
        ev, _ = softmax_ev(mid)
        if ev < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────
STRUCTURAL_FACTORS = [
    {"name": "QuickBooks SMB monopoly + Intuit Enterprise Suite expansion",
     "rating": +0.9, "weight": 0.25,
     "desc": ("QuickBooks holds ~80% of the US SMB accounting market; 10M+ subscribers growing at "
              "19% online ecosystem revenue YoY (Q3 FY2026). The Intuit Enterprise Suite — targeting "
              "businesses with $100M+ revenue — opens an entirely new TAM at 3-5× the ARPU of "
              "standard QB. Partnered with Anthropic (Claude) to build AI agents for mid-market "
              "businesses starting spring 2026. International expansion (UK, Canada, Australia) adds "
              "durable multi-year growth. QuickBooks is NOT threatened by IRS Direct File; this "
              "segment is the clearest structural growth engine in the Intuit portfolio.")},
    {"name": "AI data moat + OpenAI/Anthropic partnerships ($100M OpenAI deal)",
     "rating": +0.7, "weight": 0.15,
     "desc": ("Intuit holds 730M+ consumer financial data points — the largest proprietary financial "
              "dataset in the world. Intuit Assist is embedded across TurboTax, QB, Credit Karma and "
              "Mailchimp. In 2025, Intuit signed a $100M partnership with OpenAI integrating Intuit's "
              "products into ChatGPT — one of the largest enterprise AI adoptions ever. A multi-year "
              "Anthropic deal (Claude agents for mid-market businesses) followed in early 2026. The "
              "data moat means any AI assistant querying financial data must either partner with "
              "Intuit or build from scratch — Intuit is becoming the AI financial data layer.")},
    {"name": "IRS Direct File expansion (25 states; structural TurboTax TAM risk)",
     "rating": -0.8, "weight": 0.30,
     "desc": ("After Intuit successfully lobbied to wind down Direct File in 2024, the IRS pivoted "
              "and expanded Direct File to 25 states — the central structural risk to TurboTax. "
              "Simple return filers (W-2 only, standard deduction) are the primary target. Intuit "
              "is responding with assisted TurboTax services, deeper Credit Karma integration, and "
              "higher-value expert offerings. However, if Direct File expands to 35+ states and "
              "covers itemisers, TurboTax revenue growth could decelerate from 7-8% to 0-3%. "
              "This risk is REAL — hence the stock trading at 13x forward earnings.")},
    {"name": "Credit Karma monetisation drag (macro-sensitive ad/fintech model)",
     "rating": -0.4, "weight": 0.15,
     "desc": ("Credit Karma (acquired $7.1B in 2020) generates revenue from credit card sign-ups, "
              "loans, and insurance leads — highly sensitive to credit tightness and fintech ad "
              "spending. Q3 FY2026 Credit Karma revenue was $631M (+15% YoY) — recovering but "
              "well below the original acquisition thesis. Credit Karma has never contributed the "
              "$1.5B+ annual revenue justified by the acquisition price. In a credit tightening "
              "cycle, Credit Karma revenue can fall 20-30% quickly. It remains the weakest link "
              "in the Intuit portfolio relative to the purchase price paid.")},
    {"name": "17% workforce cut execution risk (3,000 jobs; $300-340M charges Q4 FY2026)",
     "rating": -0.3, "weight": 0.15,
     "desc": ("Intuit announced in May 2026 that it is cutting ~3,000 employees (17% of workforce), "
              "citing excessive organisational layers slowing agility. Restructuring charges of "
              "$300-340M hit Q4 FY2026. The cuts are AI-driven — replacing manual roles with "
              "Intuit Assist automation. Positives: annual cost savings ~$400-500M ($0.90-1.15 EPS "
              "accretion once annualised) + leaner structure. Risks: talent flight, product "
              "development disruption, and employee morale during tax season ramp. Execution on "
              "this scale of restructuring has historically increased near-term uncertainty.")},
]

def sca_composite():
    raw = sum(f["rating"] * f["weight"] for f in STRUCTURAL_FACTORS)
    adj = raw / 2.0
    return raw, adj

# ── SIGNAL MAPPING ─────────────────────────────────────────────────────────
def ratio_b_signal(rb):
    if rb < 0:       return "◉ BUY (below EPP floor)"
    elif rb < 0.75:  return "◉ BUY"
    elif rb < 1.10:  return "◎ ACCUMULATE"
    elif rb < 1.75:  return "◐ WATCHLIST"
    elif rb < 2.50:  return "▷ HOLD/TRIM"
    else:            return "✕ AVOID"

# ──────────────────────────────────────────────────────────────────────────
def run_report():
    mkt_composite = infer_composite(CURRENT_PRICE)
    sca_raw, sca_adj = sca_composite()
    model_composite = mkt_composite + sca_adj
    model_ev, model_probs = softmax_ev(model_composite)
    mkt_ev,   mkt_probs  = softmax_ev(mkt_composite)

    sig = ratio_b_signal(ratio_b)
    mktcap_b = CURRENT_PRICE * SHARES_M / 1000
    fcf_est  = 6.0   # annual FCF estimate $B (~28% of FY2026E $21.4B revenue)
    fcf_yield = fcf_est / mktcap_b * 100

    bear_p  = SCENARIOS["BEAR"]["price"]
    base_p  = SCENARIOS["BASE"]["price"]
    bull_p  = SCENARIOS["BULL"]["price"]
    xbull_p = SCENARIOS["XBULL"]["price"]

    print("=" * 72)
    print(f"  PART 1 — FRAMEWORK OVERVIEW  |  {TICKER}  |  {COMPANY}")
    print("=" * 72)
    print(f"""
  Bottom-Up Risk/Reward (EPP / Ratio-B / Softmax) applied to {COMPANY}.

  Three pillars:
  1. EPP Floor     — structural downside anchor  (EPS × min-viable trough P/E)
  2. Method B      — 2-yr consensus earnings power target (EPS × exit P/E)
  3. Ratio B       — primary signal: (price − EPP) / (Method B − price)
                     <0.75 BUY | 0.75–1.1 ACCUMULATE | 1.1–1.75 WATCHLIST
                     1.75–2.5 HOLD | >2.5 AVOID  |  <0 BUY (BELOW EPP FLOOR)

  Company  : {COMPANY}
  Exchange : {EXCHANGE}
  Sector   : SMB Financial Software · Tax · AI Financial Platform
  FY end   : {FY_END}
  EPS basis: Non-GAAP (excludes SBC, amortisation, restructuring charges)
  Shares   : ~{SHARES_M:.0f}M diluted (buybacks ongoing)
  Price    : ${CURRENT_PRICE:.2f}  [2026-05-24]
  52-week  : ${EPS_TROUGH_PRICE:.2f} low – $813.70 high  (ATH ~$813.70; down 61% from ATH)
""")

    print("=" * 72)
    print(f"  PART 2 — ANALYST COMMENTARY  |  {TICKER}")
    print("=" * 72)
    print(f"""
  A. INVESTMENT THESIS
  ----------------------------------------------------------------------

  Intuit is the financial operating system for American small businesses
  and consumers.  Its three core franchises — TurboTax (40%+ paid
  e-filing market share), QuickBooks (80% SMB accounting market), and
  Credit Karma (130M members) — represent some of the most durable
  competitive moats in enterprise software.

  The stock has been destroyed.  From its ATH of ~$813.70, INTU has
  fallen 61% to ${CURRENT_PRICE:.2f}.  On May 20, 2026, Intuit reported Q3 FY2026
  results that BEAT estimates and RAISED full-year guidance — then fell
  a further 20.3% as two fears collided:

  1. REVENUE DECELERATION: Q3 growth was +10% YoY, vs +17% in Q2.
     Tax season (Q3) drives ~50% of annual revenue; any slowdown is
     magnified.  TurboTax revenue +7% — below expectations but still
     growing, generating $4.4B in a single quarter.

  2. 17% WORKFORCE CUT: Intuit announced 3,000 layoffs (17% of staff),
     citing AI-driven reorganisation.  $300-340M in charges vs ~$400-
     $500M in annualised savings = a net-positive restructuring.

  The bull case is straightforward at this price:

  — TURBOTAX MOAT: IRS Direct File expanded to 25 states but targets
    only simple (W-2) filers.  Complex returns — the profitable
    segment — still require TurboTax or a CPA.  TurboTax launched
    the "Now This Is Taxes" campaign with agentic AI + 13,000 human
    experts to protect the premium tier.

  — QUICKBOOKS IS ACCELERATING: Online Ecosystem +19% YoY (Q3 FY2026).
    The new Intuit Enterprise Suite ($100M+ revenue business tier) is
    a meaningful TAM expansion.  The Anthropic (Claude) partnership
    brings AI agents to mid-market businesses starting spring 2026.

  — AI DATA MOAT: 730M financial data points.  $100M OpenAI partnership.
    Intuit Assist embedded across all four products.  This is NOT a
    company being disrupted by AI — it IS the AI financial platform.

  At ${CURRENT_PRICE:.2f}, Intuit trades at:
  — {CURRENT_PRICE/EPS_NOW:.1f}x FY2026E non-GAAP EPS (${EPS_NOW:.2f} raised guidance midpoint)
  — ~{fcf_yield:.0f}% FCF yield (~${fcf_est:.1f}B annual FCF / ~${mktcap_b:.0f}B market cap)
  — Its cheapest forward P/E in 15+ years

  The EPP structural floor is ${EPP:.2f} (20x × ${EPS_NOW:.2f}).  Intuit is
  trading {abs(epp_gap_pct):.1f}% BELOW this floor — the deepest discount of any
  stock in this coverage universe (ADBE -30.3%, CRM -25.6%, ACN -19.5%).

  Signal: {sig}  |  Ratio B: {ratio_b:.2f}x  |  EPP gap: {epp_gap_pct:.1f}%


  B. EARNINGS POWER PRICE (EPP) — STRUCTURAL FLOOR
  ----------------------------------------------------------------------

  EPS anchor   : ${EPS_TROUGH:.2f}  (FY2022 non-GAAP; lowest in 4-year window;
                  NOTE: Intuit EPS has NEVER declined — $11.85 was a growing year)
  Bear trough  : ${EPS_TROUGH_PRICE:.2f}  (52-wk low; hit post-Q3 FY2026 selloff May 2026;
                  $302.36 / $23.82 FY2026E = 12.7x — historical absolute valuation floor)
  EPP min PE   : {EPP_MIN_PE}x  (structural floor; below historical 30-50x range;
                  accounts for IRS Direct File risk + AI disruption discount; reflects
                  TurboTax near-monopoly + QB 80% market share; 20x = "business stagnates,
                  stops growing" pricing, not "business collapses" pricing)

  EPS now      : ${EPS_NOW:.2f}  (FY2026E raised guidance midpoint; original Q4 FY2025
                  guidance was $23.08; raised post-Q3 to $23.82; Q3 actual $12.80 +10%;
                  Q2 actual $4.15 +25%; consistent 18%+ non-GAAP EPS CAGR for 4+ years)
  EPP floor    : ${EPS_NOW:.2f} × {EPP_MIN_PE}x = ${EPP:.2f}

  ┌──────────────────────────────────────────────────────────────────┐
  │  CURRENT PRICE ${CURRENT_PRICE:.2f} is {abs(epp_gap_pct):.1f}% BELOW EPP FLOOR ${EPP:.2f}      │
  │  → SIGNAL: ◉ BUY (below EPP floor)  — deepest in coverage       │
  └──────────────────────────────────────────────────────────────────┘

  The market is assigning Intuit a permanent multiple of 13.4x — below
  where utilities trade.  This implies the market believes TurboTax and
  QuickBooks will never meaningfully grow earnings again.  The actual
  Q3 FY2026 data showed +10% revenue growth and a RAISED guidance.


  C. METHOD B — 2-YEAR EARNINGS POWER TARGET
  ----------------------------------------------------------------------

  CONS_EPS_2YR : ${CONS_EPS_2YR:.2f}  (FY2028E non-GAAP; FY ends Jul 2028 = ~26 months;
                  ~10% CAGR from $23.82 — CONSERVATIVE vs historical 18% CAGR;
                  deliberately discounts IRS risk eroding TurboTax growth;
                  $29 is ~$2.50 below the 15% CAGR scenario of $31.50)
  CONS_EXIT_PE : {CONS_EXIT_PE}x  (below historical 30-55x range; IRS risk premium
                  persists; 27x = re-rating to "mature software" from current "panic";
                  re-rating to 35x+ is BULL optionality if IRS risk is contained)
  Method B     : ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x = ${price_b:.2f}

  Ratio B = (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})
           = −${abs(CURRENT_PRICE - EPP):.2f} / ${price_b - CURRENT_PRICE:.2f}
           = {ratio_b:.2f}x  →  {sig}

  Sensitivity to exit PE (at CONS_EPS_2YR ${CONS_EPS_2YR:.2f}):
    CONS_EXIT_PE = 20x → Price_B $580 → Ratio B {(CURRENT_PRICE-EPP)/(580-CURRENT_PRICE):.2f}x  (BUY below floor)
    CONS_EXIT_PE = 25x → Price_B $725 → Ratio B {(CURRENT_PRICE-EPP)/(725-CURRENT_PRICE):.2f}x  (BUY below floor)
    CONS_EXIT_PE = 27x → Price_B $783 → Ratio B {ratio_b:.2f}x  (BUY below floor)  ← base
    CONS_EXIT_PE = 35x → Price_B $1015 → Ratio B {(CURRENT_PRICE-EPP)/(1015-CURRENT_PRICE):.2f}x  (BUY below floor)
    CONS_EXIT_PE = 45x → Price_B $1305 → Ratio B {(CURRENT_PRICE-EPP)/(1305-CURRENT_PRICE):.2f}x  (BUY below floor)
  At ANY plausible exit multiple, INTU is a BUY (below EPP floor).
  Signal is robust across the entire range of conservative to historical multiples.


  D. SCENARIO ANALYSIS
  ----------------------------------------------------------------------
  Scenario     EPS      P/E    Price ($)    vs Now  Description
  ----------------------------------------------------------------------""")

    for k, s in SCENARIOS.items():
        vs = (s["price"] / CURRENT_PRICE - 1) * 100
        sign = "+" if vs >= 0 else ""
        print(f"  {k:<8}  ${s['eps']:5.1f}  {s['pe']:4.1f}x  ${s['price']:8,.0f}  {sign}{vs:5.1f}%  {s['desc']}")

    print(f"""
  BASE scenario ${base_p:,.0f} = Method B target (by construction).
  BEAR at ${bear_p:.0f}: IRS Direct File expands to 45+ states covering complex returns,
  TurboTax loses 50%+ of users, QB faces AI-native startup disruption; EPS
  collapses to $10 at 15x = $150.  This requires BOTH the IRS expanding to
  cover all returns AND QuickBooks losing its SMB moat simultaneously.
  Possible, but not base case given QuickBooks +19% online ecosystem growth.
  XBULL ${xbull_p:.0f}: Intuit achieves the "AI financial OS" vision; $100M+ SMB
  segment scales globally; Credit Karma re-rates; full multiple restoration.


  E. SOFTMAX MARKET COMPOSITE
  ----------------------------------------------------------------------
""")
    print(f"  Market composite  (inferred from ${CURRENT_PRICE:.2f}): {mkt_composite:.3f}")
    print(f"  SCA adjustment                              : {sca_adj:+.3f}")
    print(f"  Model composite                             : {model_composite:.3f}")
    print()
    print(f"  Scenario probabilities (model):")
    for k, p in model_probs.items():
        bar = "█" * int(p * 40)
        print(f"    {k:<8}  {p*100:5.1f}%  {bar}")

    ev_chg = (model_ev / CURRENT_PRICE - 1) * 100
    sign_ev = "+" if ev_chg >= 0 else ""
    print(f"""
  Model EV (proxy) : ${model_ev:,.0f}  ({sign_ev}{ev_chg:.1f}% vs current ${CURRENT_PRICE:.2f})

  Interpretation: Market composite {mkt_composite:.2f} reflects extreme BEAR-weighted
  pricing — the market assigns majority probability to the BEAR scenario
  (IRS kills TurboTax + QB disruption). SCA of {sca_adj:+.3f} is near-zero: QB
  moat and AI tailwinds roughly offset IRS and Credit Karma risks. Model
  EV {sign_ev}{ev_chg:.0f}%: the current price embeds too pessimistic a scenario.
  The deepest below-EPP stock in coverage, alongside CRM and ADBE.


  F. STRUCTURAL COMPOSITE ADJUSTMENT (SCA)
  ----------------------------------------------------------------------
  Factor                                                        Rating    Wt
  --------------------------------------------------------------------------""")
    for f in STRUCTURAL_FACTORS:
        name_trunc = f["name"][:55]
        desc_trunc = f["desc"][:60]
        print(f"  {name_trunc:<55}  {f['rating']:+.1f}  {f['weight']:.0%}")
        print(f"    {desc_trunc}")

    sca_r, sca_a = sca_composite()
    print(f"""
  SCA raw = {sca_r:.3f}   SCA adj (div 2) = {sca_a:.3f}
  Market composite {mkt_composite:.2f}  +  SCA {sca_a:.3f}  =  Model composite {model_composite:.3f}


  G. EPS QUALITY DECOMP  (FY2025 ${EPS_FY2025:.2f} → FY2026E ${EPS_NOW:.2f} = +${EPS_NOW - EPS_FY2025:.2f} = +{(EPS_NOW/EPS_FY2025-1)*100:.1f}%)
  ----------------------------------------------------------------------
  Component                                                      Share          Type
  ---------------------------------------------------------------------------------
  QuickBooks Online Ecosystem growth (+19% Q3 FY2026 YoY;        40%    Structural
    GMV-based pricing + seat expansion + Enterprise Suite lift;
    higher ARPU from AI-enhanced bookkeeping; international ramp)
  TurboTax ARPU uplift + Assisted tier growth (human+AI;          25%    Structural
    TurboTax revenue +7% on stable/declining filer volumes means
    meaningful per-user spend increase; assisted/expert tier 2-3x ASP
    vs self-file; Credit Karma cross-sell adds refund advance value)
  Credit Karma partial recovery (+15% Q3; fintech ad market         10%    Structural
    rebounding from FY2024 trough; insurance + credit card leads
    improving as consumer credit stabilises; still below FY2022 peak)
  Share count reduction + buyback programme (~$2B/yr; ~280M        10%    Structural
    shares declining ~1% annually; pure EPS accretion independent
    of operating performance; funded from $6B+ FCF generation)
  Operating leverage on non-GAAP margin expansion (non-GAAP        25%    Structural
    OM expanding 100-150bps YoY; revenue growing faster than opex;
    AI-driven efficiency + 17% workforce cut saves $400-500M/yr)
  Workforce restructuring charges (Q4 FY2026 one-time costs;       -5%   Temporal
    $300-340M charges hit Q4 non-GAAP partially; some costs
    treated below the non-GAAP line but modest near-term drag)
  Mailchimp/SMB marketing headwinds (small business ad budgets;    -5%   Temporal
    Mailchimp growing slowly vs e-mail marketing commoditisation;
    segment drag partly offset by QuickBooks ecosystem bundling)

  Structural :  110%
  Temporal   :  -10%  (restructuring + Mailchimp)
  Net         :  +{(EPS_NOW/EPS_FY2025-1)*100:.1f}%
""")

    print("=" * 72)
    print(f"  PART 3 — NUMBERS & SIGNALS   |  {TICKER}")
    print("=" * 72)
    print(f"""
  H. RISK / RETURN SUMMARY
  ----------------------------------------------------------------------

  Current price       : ${CURRENT_PRICE:.2f}  (down 61% from ATH ~$813.70; -20% on Q3 May 20 2026)
  EPP floor           : ${EPP:.2f}  ({epp_gap_pct:.1f}% GAP — deepest below-EPP in coverage)
  Method B target     : ${price_b:.2f}  (upside: +{(price_b/CURRENT_PRICE-1)*100:.0f}%; conservative FY2028E $29 × 27x)
  BEAR scenario       : ${bear_p:.0f}  (downside: -{(1-bear_p/CURRENT_PRICE)*100:.0f}%; IRS + QB disruption Kodak scenario)
  Ratio B             : {ratio_b:.2f}x  -> {sig}
  Forward P/E         : {CURRENT_PRICE/EPS_NOW:.1f}x  (FY2026E ${EPS_NOW:.2f}; LOWEST in 15+ years for INTU)
  FY2028E P/E         : {CURRENT_PRICE/CONS_EPS_2YR:.1f}x  (conservative ${CONS_EPS_2YR:.2f} FY2028E)
  Historical PE range : 30–55x  (2019-2024 premium SaaS); current {CURRENT_PRICE/EPS_NOW:.1f}x = distressed pricing
  Market cap          : ~${mktcap_b:.0f}B  ({SHARES_M:.0f}M shares × ${CURRENT_PRICE:.2f})
  FCF (FY2026E est)   : ~${fcf_est:.1f}B  (~28% FCF margin on $21.4B revenue guidance)
  FCF yield           : ~{fcf_yield:.0f}%  (${fcf_est:.1f}B / ${mktcap_b:.0f}B) — exceptional for 18% EPS compounder
  Q3 FY2026 results   : Revenue $8.558B (+10%); non-GAAP EPS $12.80 (+10%); guidance RAISED
  Q3 segment breakdown: TurboTax $4.4B (+7%); QB Online Eco $2.5B (+19%); Credit Karma $631M (+15%)
  Q2 FY2026 results   : Revenue $4.65B (+17%); non-GAAP EPS $4.15 (+25%)
  FY2026 guidance     : Revenue $21.34–$21.37B; non-GAAP EPS $23.80–$23.85 (raised May 20 2026)
  FY2025 actual       : Non-GAAP EPS ~$20.10; FY ended Jul 31 2025; ~18-19% YoY growth
  TurboTax            : 40%+ paid e-filing market share; 13,000 human experts + agentic AI
  QuickBooks          : 10M+ subscribers; 80% SMB accounting market; Enterprise Suite launched
  Credit Karma        : 130M members; $631M Q3 revenue (+15% YoY); recovering from ad market trough
  IRS Direct File     : Expanded to 25 states (May 2026); simple returns only; complex = TurboTax
  Workforce cut       : 3,000 employees (~17%); $300-340M charges Q4; ~$400-500M annual savings
  AI partnerships     : $100M OpenAI deal (products in ChatGPT); Anthropic deal (Claude agents, spring 2026)
  Data moat           : 730M consumer financial data points; Intuit Assist embedded in all products
  52-week range       : ${EPS_TROUGH_PRICE:.2f} – $813.70  (currently {CURRENT_PRICE/813.70*100:.0f}% of 52-week high)
  EPS growth path     : FY2022 $11.85 → FY2024 ~$17.00 → FY2025 $20.10 → FY2026E $23.82 → FY2028E $29?
  Restructuring bonus : $400-500M annual cost savings ÷ 282M shares ≈ +$1.00 EPS accretion FY2027+
  BUY thesis breaks if: IRS Direct File expands to complex returns (beyond W-2 simple filers);
                        OR QB Online Ecosystem decelerates below 10% for 2 consecutive quarters;
                        OR FY2026 EPS guidance cut below $23.00 (materialising Credit Karma miss)
  ADD CONTEXT         : At $302-320, INTU is the deepest below-EPP stock in coverage (-33%).
                        The 17% workforce cut saves $1+ EPS/yr. QB+19% is accelerating, not slowing.
                        The Q3 "miss" was deceleration noise in Intuit's most seasonal quarter.


  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: 1.20x  |  Idiosyncratic: 70%  |  Macro: 30%

  Driver                                                 Type    Wt  Note
  ────────────────────────────────────────────────────────────────────────────────────────────
  IRS Direct File expansion scope (state count + filer types) IDIO  30%  PRIMARY risk; quarterly IRS announcements; Intuit lobbying activity
  QuickBooks Online Ecosystem growth rate (quarterly %YoY)  IDIO   25%  Must sustain >15% to confirm SMB moat; Enterprise Suite ramp is key
  TurboTax season revenue + paying filer count               IDIO   15%  Annual Q3 result is the moment of truth; +7% in heavy season = OK
  US consumer credit health (Credit Karma ad market)        MACRO  15%  Credit card sign-up rates + loan approval rates drive CK monetisation
  Small business health (QB seats + GMV)                    MACRO  15%  SMB failure rate + capex sentiment drive QB unit economics
""")

    print("=" * 72)
    print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-24")
    print("=" * 72)


if __name__ == "__main__":
    run_report()
