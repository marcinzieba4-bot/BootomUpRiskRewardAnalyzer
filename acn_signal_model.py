#!/usr/bin/env python3
"""
acn_signal_model.py  —  Accenture plc (NYSE: ACN)
Bottom-Up Risk/Reward Signal Model
All amounts in USD.  Accenture FY ends August 31.
Non-GAAP EPS = Accenture's "adjusted EPS" (excludes business optimisation charges).
"""

import math, sys, io, contextlib

TICKER        = "ACN"
COMPANY       = "Accenture plc"
EXCHANGE      = "NYSE"
CURRENCY      = "USD"
FY_END        = "August 31 (fiscal year; FY2026 = Sep 2025 – Aug 2026)"
SHARES_M      = 628.0          # million diluted shares (~market cap $111B / $177.52)

CURRENT_PRICE = 177.52         # ACN — fetched from Yahoo Finance / search, 2026-05-21; down ~49% from ATH ~$345

# ── EPP FLOOR ──────────────────────────────────────────────────────────────
EPS_TROUGH        = 7.36       # FY2020 non-GAAP; historically lowest — notably EPS GREW through COVID (defensive model)
EPS_TROUGH_PRICE  = 155.82     # 52-wk recent low (May 2026); 155.82/12.93 = 12.1x trough PE — cheapest in modern history
EPP_MIN_PE        = 16         # structural floor; well below COVID trough PE of ~21x; includes AI disruption risk discount
EPS_NOW           = 13.78      # FY2026E non-GAAP; midpoint of mgmt guidance $13.65-$13.90 (narrowed Q2 FY26); Q1 $3.94 +10%
EPS_FY2025        = 12.93      # FY2025 non-GAAP actual (Aug 2025); +8% from FY2024; FCF $10.9B
EPP               = round(EPS_NOW * EPP_MIN_PE, 2)   # $220.48

epp_gap_pct       = round((CURRENT_PRICE - EPP) / EPP * 100, 1)   # -19.4% — BELOW FLOOR

below_floor       = epp_gap_pct < 0

# ── METHOD B ───────────────────────────────────────────────────────────────
CONS_EPS_2YR  = 16.00          # FY2028E; conservative vs analyst consensus $17.93; ~8% CAGR from FY2025; AI ramp + DOGE headwind fade
EPS_FWD_CONSENSUS = 15.49      # FY2027E analyst consensus; used for PE sensitivity
CONS_EXIT_PE  = 23             # Accenture historical median 24-26x; conservative discount for AI disruption; well below FY2021-22 peak ~30x
price_b       = round(CONS_EPS_2YR * CONS_EXIT_PE, 2)   # $368.00

# When stock < EPP: ratio_b = (price - EPP) / (price_b - price) → negative → BUY
ratio_b       = round((CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE), 2)   # -0.23x

# ── SOFTMAX ENGINE ─────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  {"price": 130.0,  "eps": 10.0,  "pe": 13.0,
              "desc": "AI permanently displaces IT consulting; DOGE cuts permanent; headcount-model collapses"},
    "BASE":  {"price": 368.0,  "eps": 16.0,  "pe": 23.0,
              "desc": "FY2028E consensus recovery; AI consulting ramps; DOGE fades; 23x mid-cycle re-rate"},
    "BULL":  {"price": 494.0,  "eps": 19.0,  "pe": 26.0,
              "desc": "ACN = dominant AI transformation partner; $15B+ AI bookings/yr; 26x quality premium"},
    "XBULL": {"price": 690.0,  "eps": 23.0,  "pe": 30.0,
              "desc": "Agentic AI orchestration at enterprise scale; peak cycle; 30x re-rate to pre-AI-fear levels"},
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
    {"name": "Agentic AI consulting ramp (structural demand creation)",
     "rating": +1.1, "weight": 0.25,
     "desc": ("AI does not replace Accenture — it creates a $10B+ annual market for AI "
              "integration consulting. FY2025 AI bookings $5.9B (nearly double FY2024). "
              "Q1 FY26 AI bookings $2.2B alone (+100% YoY). Cumulative AI bookings $11.5B "
              "through Q2 FY26. Every Fortune 500 company needs ACN to implement agents.")},
    {"name": "Record bookings momentum and pipeline build",
     "rating": +1.0, "weight": 0.20,
     "desc": ("Q2 FY26 total bookings $22.1B (record); 41 clients with >$100M bookings (record). "
              "Bookings-to-revenue lag 6-12 months → revenue acceleration in H2 FY2026 "
              "and FY2027. Consulting +7%, managed services +10% YoY. Q3 FY2026 revenue "
              "guidance raised to $18.35B-$19.0B.")},
    {"name": "FCF machine + capital allocation ($10.9B FY2025 FCF)",
     "rating": +0.7, "weight": 0.20,
     "desc": ("FY2025 FCF $10.9B = 9.8% FCF yield at $177.52 price (628M shares × $177.52 = $111B "
              "market cap). $5B M&A deployment planned FY2026 (3 acquisitions closed Q2 FY26). "
              "Dividend + buyback discipline; net cash balance sheet; no credit risk. "
              "FCF yield creates natural floor in BEAR scenario.")},
    {"name": "DOGE federal spending cuts (1-1.5% revenue headwind)",
     "rating": -0.9, "weight": 0.20,
     "desc": ("US federal government is ~8% of ACN revenue (~$5.5B). DOGE review targeting "
              "$20B collective cuts across top 10 consulting firms. ACN guiding 1-1.5% FY2026 "
              "revenue drag. Risk: cuts extend into FY2027; new agency priorities post-2026 "
              "unknown. Not existential, but multi-year overhang until political clarity.")},
    {"name": "AI labor displacement narrative (structural multiple compression)",
     "rating": -0.6, "weight": 0.15,
     "desc": ("Market pricing that LLMs replace the junior consulting workforce (analysis, "
              "documentation, code review). Real risk: engagement economics change as fewer "
              "analysts needed per project. Partially offset by higher AI tool licensing "
              "revenue per engagement, but narrative weighs on multiple re-rating timeline.")},
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

    sig = ratio_b_signal(ratio_b)

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
                     1.75–2.5 HOLD | >2.5 AVOID

  Company  : {COMPANY}
  Exchange : {EXCHANGE}
  Sector   : IT Consulting & Services · Digital Transformation · Agentic AI
  FY end   : {FY_END}
  EPS basis: Non-GAAP ("adjusted EPS" per Accenture terminology)
  Price    : ${CURRENT_PRICE:.2f}  [2026-05-21]
  52-week  : ${EPS_TROUGH_PRICE:.2f} low – $321.77 high  (ATH ~$345 early 2025; −49% from ATH)
""")

    print("=" * 72)
    print(f"  PART 2 — ANALYST COMMENTARY  |  {TICKER}")
    print("=" * 72)
    print(f"""
  A. INVESTMENT THESIS
  ----------------------------------------------------------------------

  Accenture is the world's largest IT consulting and professional services
  firm — 750,000 employees, $69.7B FY2025 revenue, operating across every
  major industry and geography.  The model is simple: clients pay Accenture
  to implement technology transformations they cannot execute internally.
  ACN has compounded non-GAAP EPS at 10%+ annually for 15+ years, growing
  earnings THROUGH every recession including COVID (FY2020 EPS +5% YoY).

  Yet at ${CURRENT_PRICE:.2f} — down ~49% from the early-2025 ATH of ~$345 — the
  stock trades at {CURRENT_PRICE/EPS_NOW:.1f}x FY2026E adjusted EPS.  That is the lowest
  forward P/E in Accenture's modern history.  The COVID trough PE in March
  2020 was ~21x; today's trailing trough PE (52-wk low $155.82 / FY2025
  EPS $12.93) was 12.1x — 40% cheaper than the pandemic panic bottom.

  Two fears are driving the dislocation:
  1. DOGE: US federal government (~8% of ACN revenue) is cutting consulting
     contracts.  Management guides 1-1.5% FY2026 revenue headwind — real,
     but not existential for a $70B global business.
  2. AI disruption: The market fears LLMs replace junior consultants and
     collapse the business model.

  Both fears invert on examination:
  — Every company NEEDS Accenture to implement AI.  FY2025 AI bookings
    $5.9B (doubled YoY).  Q1 FY26 AI bookings $2.2B alone (+100% YoY).
    Cumulative AI bookings $11.5B through Q2 FY26.  Record Q2 FY26 total
    bookings $22.1B (41 clients booked >$100M — also a record).
  — AI tools deployed BY consultants (not against them) expand margins and
    reduce time-per-engagement, allowing ACN to take more clients per head.

  The market is pricing maximum BEAR fear for a company generating $10.9B
  in annual FCF — a 9.8% FCF yield at current price.

  Signal: {sig}  |  Ratio B: {ratio_b:.2f}x  |  EPP gap: {epp_gap_pct:.1f}%


  B. EARNINGS POWER PRICE (EPP) — STRUCTURAL FLOOR
  ----------------------------------------------------------------------

  EPS anchor   : ${EPS_TROUGH:.2f}  (FY2020 non-GAAP; lowest EPS in recent history;
                  note: grew 5% YoY THROUGH COVID — defensive consulting model)
  Bear trough  : ${EPS_TROUGH_PRICE:.2f}  (52-wk recent low, May 2026; 12.1x FY2025 EPS;
                  lowest observed P/E in Accenture's modern history — below COVID!)
  EPP min PE   : {EPP_MIN_PE}x  (structural floor; conservative discount for AI disruption
                  and DOGE risk; COVID panic trough was 21x — this is 24% lower)

  EPS now      : ${EPS_NOW:.2f}  (FY2026E non-GAAP; midpoint $13.65-$13.90 guidance;
                  narrowed and raised Q2 FY26; Q1 FY26 actual ${3.94:.2f} (+10% YoY))
  EPP floor    : ${EPS_NOW:.2f} × {EPP_MIN_PE}x = ${EPP:.2f}
  Current vs EPP: ${CURRENT_PRICE:.2f} vs ${EPP:.2f}  ({epp_gap_pct:.1f}% — BELOW EPP FLOOR)

  The stock is trading {abs(epp_gap_pct):.1f}% BELOW the structural earnings power floor.
  This is the second stock in coverage universe to breach EPP (after CRM).
  Even using a deeply conservative 16x floor (40% below COVID panic trough
  PE), the stock is structurally undervalued at current prices.


  C. METHOD B — 2-YEAR EARNINGS POWER TARGET
  ----------------------------------------------------------------------

  CONS_EPS_2YR : ${CONS_EPS_2YR:.2f}  (FY2028E; conservative vs analyst consensus $17.93;
                  ~8% CAGR from FY2025 $12.93; assumes DOGE fades by FY2027, AI
                  consulting ramps; FY2027 analyst consensus $15.49 supports trajectory)
  CONS_EXIT_PE : {CONS_EXIT_PE}x  (Accenture historical median 24-26x; discounted for
                  structural AI risk; below FY2021-22 peak ~30x; conservative base case)
  Method B     : ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x = ${price_b:.2f}

  Ratio B = (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})
           = (${CURRENT_PRICE - EPP:.2f}) / ${price_b - CURRENT_PRICE:.2f}
           = {ratio_b:.2f}x  →  {sig}

  Negative ratio_b: stock is below EPP floor → strongest BUY signal in the framework.

  Sensitivity to exit PE (at CONS_EPS_2YR ${CONS_EPS_2YR:.2f}):
    CONS_EXIT_PE = 20x → Price_B $320.00 → Ratio B {(CURRENT_PRICE-EPP)/(320-CURRENT_PRICE):.2f}x  (BUY, below floor)
    CONS_EXIT_PE = 23x → Price_B $368.00 → Ratio B {ratio_b:.2f}x  (BUY, below floor)  ← base case
    CONS_EXIT_PE = 26x → Price_B $416.00 → Ratio B {(CURRENT_PRICE-EPP)/(416-CURRENT_PRICE):.2f}x  (BUY, below floor)
    CONS_EXIT_PE = 28x → Price_B $448.00 → Ratio B {(CURRENT_PRICE-EPP)/(448-CURRENT_PRICE):.2f}x  (BUY, below floor)
  BUY signal is robust across ALL exit multiples (stock below EPP at any PE).


  D. SCENARIO ANALYSIS
  ----------------------------------------------------------------------
  Scenario     EPS     P/E    Price    vs Now  Description
  ----------------------------------------------------------------------""")

    for k, s in SCENARIOS.items():
        vs = (s["price"] / CURRENT_PRICE - 1) * 100
        sign = "+" if vs >= 0 else ""
        print(f"  {k:<8}  ${s['eps']:5.2f}  {s['pe']:4.1f}x  ${s['price']:6,.0f}   {sign}{vs:5.1f}%  {s['desc']}")

    bear_p = SCENARIOS["BEAR"]["price"]
    base_p = SCENARIOS["BASE"]["price"]
    print(f"""
  BASE scenario ${base_p:,.0f} = Method B target (by construction).
  BEAR at ${bear_p:.0f} requires AI to permanently destroy consulting economics AND DOGE
  to permanently cut federal IT budgets — a simultaneous double-structural-break.
  Even in BEAR, FCF yield at ${bear_p:.0f} would be ~{10.9/(SHARES_M*bear_p/1000)*100:.0f}% (FCF $10.9B / market cap
  ${SHARES_M*bear_p/1000:.0f}B) — an automatic floor for buybacks and institutional value buying.


  E. SOFTMAX MARKET COMPOSITE
  ----------------------------------------------------------------------
""")
    mkt_composite = infer_composite(CURRENT_PRICE)
    sca_raw, sca_adj = sca_composite()
    model_composite = mkt_composite + sca_adj
    model_ev, model_probs = softmax_ev(model_composite)

    print(f"  Market composite  (inferred from ${CURRENT_PRICE:.2f}): {mkt_composite:.3f}")
    print(f"  SCA adjustment                               : {sca_adj:+.3f}")
    print(f"  Model composite                              : {model_composite:.3f}")
    print()
    print(f"  Scenario probabilities (model):")
    for k, p in model_probs.items():
        bar = "█" * int(p * 40)
        print(f"    {k:<8}  {p*100:5.1f}%  {bar}")

    ev_chg = (model_ev / CURRENT_PRICE - 1) * 100
    sign = "+" if ev_chg >= 0 else ""
    bear_prob = model_probs["BEAR"]
    base_prob = model_probs["BASE"]
    bull_prob = model_probs["BULL"]
    xbull_prob = model_probs["XBULL"]
    print(f"""
  Model EV (proxy) : ${model_ev:,.0f}  ({sign}{ev_chg:.1f}% vs current ${CURRENT_PRICE:.2f})

  Interpretation: Market composite {mkt_composite:.2f} is deep in the BEAR zone (BEAR centre =
  1.25) — the market is pricing maximum pessimism on AI disruption + DOGE.
  Model composite {model_composite:.2f} (SCA adds AI booking tailwind) shifts probability
  toward BASE/BULL. Model EV of ${model_ev:,.0f} implies {sign}{ev_chg:.0f}% upside.
  Critical insight: BEAR at ${bear_p:.0f} = only -{(1-bear_p/CURRENT_PRICE)*100:.0f}% downside. BASE at ${base_p:,.0f}
  = +{(base_p/CURRENT_PRICE-1)*100:.0f}% upside. The risk/reward is deeply asymmetric to the UPSIDE —
  rare for a name with this quality track record at this FCF yield.


  F. STRUCTURAL COMPOSITE ADJUSTMENT (SCA)
  ----------------------------------------------------------------------
  Factor                                                        Rating    Wt
  --------------------------------------------------------------------------""")
    for f in STRUCTURAL_FACTORS:
        name_trunc = f["name"][:55]
        desc_trunc = f["desc"][:60]
        print(f"  {name_trunc:<55}  {f['rating']:+.1f}  {f['weight']:.0%}")
        print(f"    {desc_trunc}")

    print(f"""
  SCA raw = {sca_raw:.3f}   SCA adj (div 2) = {sca_adj:.3f}
  Market composite {mkt_composite:.2f}  +  SCA {sca_adj:.3f}  =  Model composite {model_composite:.3f}


  G. EPS QUALITY DECOMP  (FY2025 ${EPS_FY2025:.2f} → FY2026E ${EPS_NOW:.2f} = +${EPS_NOW - EPS_FY2025:.2f} = +{(EPS_NOW/EPS_FY2025-1)*100:.1f}%)
  ----------------------------------------------------------------------
  Component                                                      Share          Type
  ---------------------------------------------------------------------------------
  AI consulting bookings ramp (FY2025 AI bookings $5.9B;         45%    Structural
    Q1 FY26 alone $2.2B; AI implementation engagements are
    higher-margin, longer-duration than traditional IT projects)
  Managed services growth (+10% YoY Q2 FY26; recurring model;   25%    Structural
    annuity-like revenue base supporting EPS floor stability)
  Operating margin expansion (FY2026 guidance: +10-30 bps;       15%    Structural
    AI tools boosting consultant productivity per engagement)
  DOGE / US federal revenue headwind offsetting growth            -10%   Temporal
    (1-1.5% FY2026 revenue drag; ~$1-1.5B revenue impact;
    management expects partial recovery FY2027 as cuts stabilise)
  FX translation (USD strength vs EUR/GBP/JPY; ~60% of ACN       -5%    Temporal
    revenue is non-USD; FX-neutral growth higher than USD growth;
    local currency guidance 3-5% vs reported 8% Q2 divergence shows)
  M&A integration contribution (3 acquisitions closed Q2 FY26;   30%    Structural
    $1.6B deployed; $5B planned FY2026; bolt-on capabilities)

  Structural :  115%  (partially offsets temporal headwinds)
  Temporal   :  -15%  (DOGE + FX)
  Net         :  +{(EPS_NOW/EPS_FY2025-1)*100:.1f}%
""")

    print("=" * 72)
    print(f"  PART 3 — NUMBERS & SIGNALS   |  {TICKER}")
    print("=" * 72)
    fcf_yield = 10.9 / (SHARES_M * CURRENT_PRICE / 1000) * 100
    mktcap = SHARES_M * CURRENT_PRICE / 1000
    print(f"""
  H. RISK / RETURN SUMMARY
  ----------------------------------------------------------------------

  Current price       : ${CURRENT_PRICE:.2f}  (down ~49% from ATH ~$345; 52-wk low ${EPS_TROUGH_PRICE:.2f})
  EPP floor           : ${EPP:.2f}  (stock is {abs(epp_gap_pct):.1f}% BELOW floor; {EPP_MIN_PE}x × ${EPS_NOW:.2f} FY2026E)
  Method B target     : ${price_b:.2f}  (upside: +{(price_b/CURRENT_PRICE-1)*100:.0f}%)
  BEAR scenario       : ${bear_p:.0f}  (downside: -{(1-bear_p/CURRENT_PRICE)*100:.0f}%; AI displacement + DOGE permanent)
  Ratio B             : {ratio_b:.2f}x  -> {sig}
  Forward P/E         : {CURRENT_PRICE/EPS_NOW:.1f}x  (FY2026E non-GAAP ${EPS_NOW:.2f}; lowest in modern ACN history)
  COVID trough P/E    : ~21x  (March 2020; today's 52-wk trough was 12.1x — 40% cheaper)
  FY2028E P/E         : {CURRENT_PRICE/CONS_EPS_2YR:.1f}x  (conservative consensus ${CONS_EPS_2YR:.2f}; analyst ${17.93:.2f})
  Historical P/E range: 20–30x  (current {CURRENT_PRICE/EPS_NOW:.1f}x is BELOW historical FLOOR)
  Market cap          : ~${mktcap:.1f}B  ({SHARES_M:.0f}M shares × ${CURRENT_PRICE:.2f})
  FCF yield           : {fcf_yield:.1f}%  (FY2025 FCF $10.9B / market cap ${mktcap:.1f}B; extraordinary)
  FY2025 revenue      : $69.7B  (+7% YoY; FY2026E guidance +3-5% LC / +8% USD)
  Q2 FY26 bookings    : $22.1B  (record); 41 clients >$100M (record)
  AI bookings cumul.  : $11.5B  (through Q2 FY26; FY2025 alone $5.9B; doubling each year)
  Q1 FY26 AI bookings : $2.2B  (+100% YoY — doubling annually)
  Q3 FY26 catalyst    : June 18 2026  (Q3 FY26 results; Q3 revenue guided $18.35-$19.0B)
  DOGE headwind       : ~1-1.5% FY2026 revenue drag (~$1B); US federal ~8% of revenue
  Analyst consensus   : 39 Buy / 12 Hold / 1 Sell; avg price target ~$257 (vs $178 current)
  52-week range       : ${EPS_TROUGH_PRICE:.2f} – $321.77  (currently {CURRENT_PRICE/321.77*100:.0f}% of 52-week high)
  BUY thesis breaks if: AI bookings DECELERATE (below $1.5B/quarter); DOGE cuts extend to
                        commercial agencies; operating margin compresses below 14.5% (FY2026E 15%+)
  ADD trigger         : Current price IS the trigger — stock below EPP floor at $177.52


  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: 1.15x  |  Idiosyncratic: 60%  |  Macro: 40%

  Driver                                                 Type    Wt  Note
  ────────────────────────────────────────────────────────────────────────────────────────────
  Quarterly AI bookings growth rate                      IDIO   25%  $2.2B in Q1 FY26 (+100%). Must sustain $2B+ per quarter; any
  Consulting vs managed services revenue mix shift       IDIO   20%  Managed services (+10%) more recurring than consulting (+7%)
  DOGE resolution / US federal contract reinstatement    IDIO   15%  Policy risk; non-renewal of specific agency contracts is tracked
  Global IT spending cycle (Fortune 500 budgets)        MACRO   20%  CFO willingness to approve transformation projects is macro-linked
  USD strength (FX translation headwind)                MACRO   10%  60%+ revenue non-USD; reported EPS sensitive to DXY; local currency
  Interest rate environment (M&A cost of capital)       MACRO   10%  $5B/yr M&A program at risk if rates remain elevated; acquisition
""")

    print("=" * 72)
    print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-22")
    print("=" * 72)


if __name__ == "__main__":
    run_report()
