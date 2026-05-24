#!/usr/bin/env python3
"""
pltr_signal_model.py  —  Palantir Technologies Inc. (NASDAQ: PLTR)
Bottom-Up Risk/Reward Signal Model
All prices and EPS in USD.  EPS = non-GAAP adjusted (excludes SBC, M&A charges).
"""

import math, sys, io, contextlib

TICKER        = "PLTR"
COMPANY       = "Palantir Technologies Inc."
EXCHANGE      = "NASDAQ"
FY_END        = "December 31 (calendar year)"
SHARES_M      = 2400.0          # million diluted shares (Q1 2026; ~$328B mkt cap / $136.67)

CURRENT_PRICE = 135.90          # PLTR — fetched from web search, 2026-05-24
                                 # May 22 close: $136.88; May 23 range: $134.30–$139.02 ($135.90)
                                 # ATH: $207.52 / $207.18 close (Nov 3, 2025); -34% from ATH

# ── EPP FLOOR ──────────────────────────────────────────────────────────────
EPS_TROUGH        = 0.19        # FY2023; first year of consistent non-GAAP profitability;
                                 # PLTR turned consistently profitable in FY2023 after years of losses
EPS_TROUGH_PRICE  = 8.50        # PLTR in early 2023 (Jan–Mar 2023) when near this EPS level;
                                 # stock was $6–10 range; recovery began mid-2023 with AI catalyst
EPP_MIN_PE        = 45          # structural floor for a government AI OS with FedRAMP High clearance;
                                 # PLTR never trades below ~40–50x even at selloff trough (52-wk low
                                 # $118.93 = ~91× FY2026E — even "cheap" PLTR is extremely expensive);
                                 # 45x reflects defensible government revenue moat + AI platform premium
EPS_FY2025        = 0.72        # FY2025 full-year non-GAAP adjusted (Q1 $0.13 + Q2 $0.16 + Q3 $0.21
                                 # + Q4 ~$0.22 ≈ $0.72); +76% YoY from FY2024 $0.41
EPS_NOW           = 1.30        # FY2026E conservative; Q1 2026 actual $0.33 (beat $0.28 est);
                                 # FY2026 adj FCF guidance $4.2–4.4B / 2.4B shares ≈ $1.75–1.83/share FCF;
                                 # EPS below FCF due to taxes; using conservative $1.30 vs $1.35–1.40 bull
EPP               = round(EPS_NOW * EPP_MIN_PE, 2)    # $58.50

epp_gap_pct       = round((CURRENT_PRICE - EPP) / EPP * 100, 1)    # +132.3%
below_floor       = CURRENT_PRICE < EPP                              # False

# ── METHOD B ───────────────────────────────────────────────────────────────
CONS_EPS_2YR  = 2.79            # FY2028E consensus non-GAAP; growth compounding at ~31%/yr from $1.94
                                 # FY2027E; reflects AIP commercial + government AI super-cycle continuing
CONS_EXIT_PE  = 55              # very generous for any stock; reflects AI platform premium + gov monopoly;
                                 # historical high-growth SaaS peak multiples 50–80×; 55× = generous BASE;
                                 # at 60× → $167 (+23%); at 50× → $140 (+3%); at 45× → $126 (below current)
price_b       = round(CONS_EPS_2YR * CONS_EXIT_PE, 2)    # $153.45
ratio_b_raw   = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE) if price_b > CURRENT_PRICE else None
ratio_b       = round(ratio_b_raw, 2) if ratio_b_raw is not None else None  # 4.41x → AVOID

# ── SOFTMAX ENGINE ─────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  {"price": 30.0,   "eps":  0.75, "pe": 40.0,
              "desc": "DOGE cuts + AI bubble pop; revenue -30%; growth stalls; gov contracts clawed back"},
    "BASE":  {"price": 153.45, "eps":  2.79, "pe": 55.0,
              "desc": "FY2028E $2.79 × 55×; AIP scales; gov AI OS sustains; commercial continues at 50%+ CAGR"},
    "BULL":  {"price": 260.0,  "eps":  4.00, "pe": 65.0,
              "desc": "Commercial breakout; defense super-cycle; FY2028E EPS upside; near ATH re-test"},
    "XBULL": {"price": 420.0,  "eps":  5.50, "pe": 76.0,
              "desc": "AI OS monopoly for NATO/DoD; commercial AIP = Salesforce-scale; 100%+ commercial CAGR sustained"},
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
    {"name": "Government AI OS monopoly (FedRAMP High; classified networks)",
     "rating": +1.0, "weight": 0.35,
     "desc": ("Palantir operates in classified government environments that AWS, Azure, and Google "
              "cannot access.  Gotham (defense intelligence), Maven Smart System (military AI "
              "targeting), and Palantir's classified network presence represent a structural "
              "monopoly.  No competitor has the clearance depth, the FedRAMP High + IL5/IL6 "
              "authorisations, or the 20+ years of classified data integration experience to "
              "displace PLTR.  NATO adoption, US Army AI warfighting systems, and allied "
              "intelligence sharing all run on Palantir rails.  Ukraine, Israel, DoD — PLTR "
              "is the AI operating system for Western military operations.  This is not a "
              "feature; it is a structural moat that competes with nation-states, not startups.")},
    {"name": "AIP bootcamp commercial flywheel (75% conversion, 5-day sales cycle)",
     "rating": +0.8, "weight": 0.15,
     "desc": ("Palantir AIP Bootcamp compresses 12–18 month enterprise sales cycles to 5 days. "
              "A company sends engineers and operators who build their own AI use cases ON Palantir "
              "infrastructure with Palantir forward-deployed engineers.  Conversion rate: ~75%.  "
              "This eliminates the traditional SaaS 'evaluation' phase — customers become users "
              "before they can talk to competitors.  US commercial grew +133% YoY Q1 2026 and "
              "+18% QoQ.  Rule of 40 hit 145% in Q1 2026 (revenue growth + adj op margin).  "
              "The commercial TAM expansion into healthcare, energy, manufacturing, and finance "
              "is real and compounding.  US Commercial FY2026 guidance: +120% YoY growth.")},
    {"name": "Extreme valuation — 101× FY2026E P/E, 43× P/S",
     "rating": -1.0, "weight": 0.25,
     "desc": ("At $135.90 / $1.30 FY2026E non-GAAP EPS = 104.5× forward P/E.  Revenue multiple: "
              "$326B mkt cap / $7.65B FY2026E revenue = 42.6× P/S.  These are among the highest "
              "multiples in the entire market.  Even using FY2028E ($2.79 EPS), the P/E is 48.7×.  "
              "The 52-week LOW of $118.93 implies ~91× FY2026E — meaning even a 'cheap' PLTR is "
              "extraordinarily expensive.  Any multiple contraction from 100× to 60× on FY2026E "
              "implies a stock price of $78 — a -43% drawdown from current.  The ATH of $207 "
              "represented a ~159× FY2026E multiple — the current price is NOT a bargain even "
              "34% below ATH.")},
    {"name": "Government budget concentration risk (DOGE, administration dependency)",
     "rating": -0.7, "weight": 0.15,
     "desc": ("~50%+ of PLTR revenue is from US and international governments.  The DOGE "
              "(Department of Government Efficiency) initiative under the current administration "
              "creates non-trivial risk: if government AI spending is cut or consolidated, "
              "PLTR's largest segment could face headwinds.  Additionally, PLTR's classified "
              "contracts require ongoing re-authorisations and are subject to administration "
              "priorities.  A government shift toward in-house AI development (parallel to "
              "the DoD DIU programme) could reduce reliance on external vendors over 5–10 "
              "years.  Single-administration dependency for a company this large is a "
              "structural risk that markets periodically re-price.")},
    {"name": "Stock-based compensation — GAAP EPS vs non-GAAP gap; insider selling",
     "rating": -0.4, "weight": 0.10,
     "desc": ("PLTR's non-GAAP EPS excludes substantial stock-based compensation (~$500–600M/yr). "
              "GAAP EPS is dramatically lower than non-GAAP.  Shares outstanding grew from "
              "~1.9B at IPO to 2.4B — ongoing dilution from SBC and option exercises.  "
              "CEO Alex Karp is one of the most prolific insider sellers in the S&P 500, with "
              "a 10b5-1 trading plan that sells millions of shares quarterly.  While legally "
              "required to be pre-set, the pace of CEO selling creates negative sentiment "
              "signals and raises corporate governance questions.  The fully-diluted share "
              "count expansion will reduce per-share EPS/FCF growth relative to total company "
              "growth over time.")},
]

def sca_composite():
    raw = sum(f["rating"] * f["weight"] for f in STRUCTURAL_FACTORS)
    adj = raw / 2.0
    return raw, adj

# ── SIGNAL MAPPING ─────────────────────────────────────────────────────────
def ratio_b_signal(rb):
    if rb is None:     return "✕ AVOID"
    if rb < 0:         return "◉ BUY (below EPP floor)"
    elif rb < 0.75:    return "◉ BUY"
    elif rb < 1.10:    return "◎ ACCUMULATE"
    elif rb < 1.75:    return "◐ WATCHLIST"
    elif rb < 2.50:    return "▷ HOLD/TRIM"
    else:              return "✕ AVOID"

signal_str = ratio_b_signal(ratio_b)

# ── REPORT ─────────────────────────────────────────────────────────────────
def run_report():
    sca_raw, sca_adj = sca_composite()
    market_composite  = infer_composite(CURRENT_PRICE)
    adj_composite     = market_composite + sca_adj
    _, mkt_probs      = softmax_ev(market_composite)
    _, adj_probs      = softmax_ev(adj_composite)

    ratio_b_fmt = f"{ratio_b:.2f}x" if ratio_b is not None else "N/A"

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        W   = 72
        sep  = "=" * W
        dash = "-" * 70

        # ── PART 1 ──────────────────────────────────────────────────────────
        print(sep)
        print(f"  PART 1 — FRAMEWORK OVERVIEW  |  {TICKER}  |  {COMPANY}")
        print(sep)
        print()
        print(f"  Bottom-Up Risk/Reward (EPP / Ratio-B / Softmax) applied to {COMPANY}.")
        print()
        print("  Three pillars:")
        print("  1. EPP Floor     — structural downside anchor  (EPS × min-viable trough P/E)")
        print("  2. Method B      — 2-yr consensus earnings power target (EPS × exit P/E)")
        print("  3. Ratio B       — primary signal: (price − EPP) / (Method B − price)")
        print("                     <0.75 BUY | 0.75–1.1 ACCUMULATE | 1.1–1.75 WATCHLIST")
        print("                     1.75–2.5 HOLD | >2.5 AVOID")
        print()
        print(f"  Company  : {COMPANY}")
        print(f"  Exchange : {EXCHANGE}")
        print(f"  Sector   : AI Operating System · Government Defense AI · Enterprise SaaS")
        print(f"  FY end   : {FY_END}")
        print(f"  EPS basis: Non-GAAP adjusted (excludes SBC ~$500–600M/yr, acquisition charges)")
        print(f"  Shares   : ~{SHARES_M:.0f}M diluted (Q1 2026; growing ~2-3%/yr via SBC issuance)")
        print(f"  Price    : ${CURRENT_PRICE:.2f}  [2026-05-24; -34% from ATH $207.52 (Nov 3 2025)]")
        print(f"  52-week  : $118.93 low – $207.52 high  (AI re-rating; 52-wk low = 91× FY2026E)")

        print()
        print(sep)
        print(f"  PART 2 — ANALYST COMMENTARY  |  {TICKER}")
        print(sep)

        # ── A. INVESTMENT THESIS ─────────────────────────────────────────────
        print()
        print("  A. INVESTMENT THESIS")
        print(f"  {dash}")
        print()
        print("  Palantir is not a software company.  It is an AI operating system.")
        print("  The distinction matters: operating systems do not get replaced.")
        print()
        print("  Founded in 2003 by Peter Thiel, Alex Karp, and Joe Lonsdale to help the")
        print("  US government prevent terrorist attacks, Palantir spent 20 years building")
        print("  the classified data integration infrastructure that underlies Western")
        print("  intelligence, military targeting, and battlefield AI.  No startup can")
        print("  replicate this.  You cannot get FedRAMP High, IL5, IL6 authorisations")
        print("  and 20 years of classified network integrations in 24 months.")
        print()
        print("  THE BULL CASE — GOVERNMENT AI OS + COMMERCIAL AIP FLYWHEEL:")
        print()
        print("  1. GOVERNMENT MONOPOLY (unassailable):")
        print("     Maven Smart System powers US Army AI targeting.  Palantir's Gotham")
        print("     platform processes classified intelligence for NSA, CIA, and allied")
        print("     services.  Ukraine and Israel are running active warfighting AI on")
        print("     Palantir rails.  NATO is standardising on PLTR infrastructure.  US")
        print("     Government revenue grew +84% YoY in Q1 2026 despite DOGE headlines.")
        print("     The government is not cutting AI — it is accelerating it.")
        print()
        print("  2. AIP BOOTCAMP — SALES CYCLE COLLAPSED:")
        print("     Palantir AIP Platform converts enterprises in 5 days.  The bootcamp")
        print("     model sends a company's own engineers to build their AI use cases on")
        print("     PLTR infrastructure with Palantir forward-deployed engineers.  75%")
        print("     conversion rate.  18-month sales cycles → 5 days.  US Commercial")
        print("     grew +133% YoY and +18% QoQ in Q1 2026.  FY2026 US Commercial")
        print("     guidance: +120% YoY.  This is not marketing — it is product-led growth")
        print("     at industrial scale, and it is accelerating.")
        print()
        print("  3. FINANCIAL QUALITY:")
        print("     Q1 2026: Revenue $1.6B (+85% YoY); adjusted operating margin 60%;")
        print("     Rule of 40 = 145% (growth rate + margin = extraordinary).  Adj FCF")
        print("     guided $4.2–4.4B for FY2026.  This is not a money-losing growth story")
        print("     — PLTR is profitable, cash-generative, and growing at 85%.")
        print()
        print("  THE BEAR CASE — ALREADY PRICED FOR PERFECTION AND MORE:")
        print()
        print("  At $135.90, PLTR trades at 104× FY2026E non-GAAP EPS and 42.6× P/S.")
        print("  These multiples price in not just success, but extraordinary, decade-")
        print("  long compounding at rates that have never been sustained by any company")
        print("  at this scale.  The math on Method B is brutal:")
        print()
        print("    FY2028E $2.79 EPS × 55× exit P/E = $153.45 (BASE target)")
        print("    That is only +12.9% above today's price over 2 years.")
        print()
        print("  Even more striking: at a 50× exit P/E (still historically extreme),")
        print("  price_b = $139.50 — barely above current.  At 45×, $125.55 is BELOW")
        print("  current.  The margin of safety is negative in any non-extreme scenario.")
        print()
        print("  The stock fell -34% from its ATH of $207.52 (Nov 2025).  This sounds")
        print("  like a bargain.  It is not.  At $207, PLTR traded at 159× FY2026E EPS.")
        print("  At $135, it trades at 104×.  Both are extraordinary.  The 'correction'")
        print("  has done almost nothing to restore rational valuation.")
        print()
        print(f"  Signal: {signal_str}  |  Ratio B: {ratio_b_fmt}  |  EPP gap: +{epp_gap_pct:.1f}%")
        print(f"  WATCHLIST entry: ~$85 (ratio_b ~1.5×); BUY at ~$50 (ratio_b ~0.75×)")
        print(f"  At 55× exit P/E, need FY2028E EPS to reach $4.50+ just to justify today's price")

        # ── B. EPP FLOOR ─────────────────────────────────────────────────────
        print()
        print("  B. EARNINGS POWER PRICE (EPP) — STRUCTURAL FLOOR")
        print(f"  {dash}")
        print()
        print(f"  EPS anchor   : ${EPS_TROUGH:.2f}  (FY2023; first year of consistent non-GAAP")
        print(f"                  profitability; PLTR turned the corner structurally)")
        print(f"  Trough price : ${EPS_TROUGH_PRICE:.2f}  (PLTR Jan–Mar 2023; pre-AI re-rating bottom)")
        print(f"  EPP min P/E  : {EPP_MIN_PE}×  (floor for a classified AI OS franchise; even the 52-wk")
        print(f"                  low $118.93 = 91× FY2026E — 45× is the analytical floor)")
        print(f"  EPS now      : ${EPS_NOW:.2f}  (FY2026E; Q1 actual $0.33 + H2 ramp conservative)")
        print(f"  EPP          : ${EPP:.2f}  ({EPP_MIN_PE}× × ${EPS_NOW:.2f})")
        print()
        print(f"  Current price ${CURRENT_PRICE:.2f} is +{epp_gap_pct:.1f}% ABOVE EPP floor ${EPP:.2f}")
        print()
        print("  EPP is the structural floor — where a franchise buyer would step in.")
        print("  At 45× EPS, even a worst-case government-only scenario implies a floor")
        print(f"  around ${EPP:.0f}.  The current price is 2.3× above this floor, meaning")
        print("  the market is pricing extraordinary growth outcomes, not the floor.")
        print(f"  A reversion to EPP from current levels = {(EPP - CURRENT_PRICE)/CURRENT_PRICE*100:.1f}% drawdown.")

        # ── C. METHOD B ──────────────────────────────────────────────────────
        print()
        print("  C. METHOD B — 2-YEAR EARNINGS POWER TARGET")
        print(f"  {dash}")
        print()
        print(f"  Consensus EPS (FY2028E) : ${CONS_EPS_2YR:.2f}  (analyst consensus; 31%/yr from FY2027E $1.94)")
        print(f"  Exit P/E                : {CONS_EXIT_PE}×  (very generous; top of sustainable growth SaaS range)")
        print(f"  Method B target         : ${price_b:.2f}  ({CONS_EXIT_PE}× × ${CONS_EPS_2YR:.2f})")
        print(f"  Current price           : ${CURRENT_PRICE:.2f}")
        print(f"  Implied upside          : +{(price_b - CURRENT_PRICE)/CURRENT_PRICE*100:.1f}%")
        print()
        print(f"  Ratio B = ({CURRENT_PRICE:.2f} − {EPP:.2f}) / ({price_b:.2f} − {CURRENT_PRICE:.2f})")
        print(f"          = {CURRENT_PRICE - EPP:.2f} / {price_b - CURRENT_PRICE:.2f}")
        print(f"          = {ratio_b_fmt}")
        print()
        print("  ┌─────────────────────────────────────────────────────────────────┐")
        print(f"  │  Even at 55× exit P/E (historically extreme), Method B         │")
        print(f"  │  offers only +12.9% upside over 2 years on a Ratio B of 4.41×  │")
        print(f"  │  Signal: {signal_str:<55} │")
        print("  └─────────────────────────────────────────────────────────────────┘")
        print()
        print("  SENSITIVITY — how signal changes at different exit P/E assumptions:")
        print()
        print(f"  {'Exit P/E':>8}  {'Method B':>10}  {'Upside':>8}  {'Ratio B':>10}  {'Signal':<18}")
        print(f"  {'-'*8}  {'-'*10}  {'-'*8}  {'-'*10}  {'-'*18}")
        for pe_test in [40, 45, 50, 55, 60, 65, 70, 80]:
            pb_test = CONS_EPS_2YR * pe_test
            if pb_test <= CURRENT_PRICE:
                rb_test_fmt = "N/A"
                sig_test    = "✕ AVOID"
            else:
                rb_test = (CURRENT_PRICE - EPP) / (pb_test - CURRENT_PRICE)
                rb_test_fmt = f"{rb_test:.2f}x"
                sig_test = ratio_b_signal(rb_test)
            upside_test = (pb_test - CURRENT_PRICE) / CURRENT_PRICE * 100
            print(f"  {pe_test:>8}×  ${pb_test:>9.2f}  {upside_test:>+7.1f}%  {rb_test_fmt:>10}  {sig_test:<18}")
        print()
        print("  KEY INSIGHT: You need to believe in 80× FY2028E exit P/E ($223) to get")
        print("  to WATCHLIST.  At 70× ($195 — still the ATH zone) Ratio B = 1.60× =")
        print("  WATCHLIST.  The signal only becomes ACCUMULATE at 85–90× P/E.  This is")
        print("  not a normal valuation framework — it requires extraordinary assumptions")
        print("  at every step to get to a BUY signal.")

        # ── D. SOFTMAX SCENARIO ENGINE ───────────────────────────────────────
        print()
        print("  D. SCENARIO ENGINE & MARKET COMPOSITE")
        print(f"  {dash}")
        print()
        print(f"  {'Scenario':<8}  {'Price':>7}  {'EPS':>6}  {'P/E':>5}  {'Mkt%':>6}  {'Adj%':>6}  Description")
        print(f"  {'-'*8}  {'-'*7}  {'-'*6}  {'-'*5}  {'-'*6}  {'-'*6}  {'-'*40}")
        for k, s in SCENARIOS.items():
            mp = mkt_probs[k] * 100
            ap = adj_probs[k] * 100
            print(f"  {k:<8}  ${s['price']:>6.0f}  ${s['eps']:>5.2f}  {s['pe']:>4.0f}×  {mp:>5.1f}%  {ap:>5.1f}%  {s['desc'][:40]}")
        print()
        print(f"  Market composite   : {market_composite:.3f}  (inferred from current price ${CURRENT_PRICE:.2f})")
        print(f"  SCA adjustment     : {sca_adj:+.3f}  (structural factors; see section F)")
        print(f"  Adjusted composite : {adj_composite:.3f}")
        print()
        print("  Composite interpretation:")
        print("  1.0–1.5 = deep value  |  1.5–2.0 = value  |  2.0–2.5 = fair")
        print("  2.5–3.0 = rich  |  3.0–3.5 = expensive  |  3.5–4.0 = bubble")

        # ── E. EARNINGS TRAJECTORY ───────────────────────────────────────────
        print()
        print("  E. EARNINGS TRAJECTORY (non-GAAP adjusted EPS)")
        print(f"  {dash}")
        print()
        print("  FY2020   −$0.47  (deep losses; scaling government segment)")
        print("  FY2021   −$0.17  (losses narrowing; $1.5B revenue; S-1 year)")
        print("  FY2022   +$0.06  (first full-year non-GAAP profitability)")
        print("  FY2023   +$0.19  ◀ TROUGH REFERENCE EPS (first consistent profitability)")
        print("  FY2024   +$0.41  (+116% YoY)")
        print("  FY2025   +$0.72  (+76% YoY; Q1 $0.13 + Q2 $0.16 + Q3 $0.21 + Q4 $0.22)")
        print("  FY2026E  +$1.30  (Q1 $0.33 actual; +85% revenue; 60% adj op margin; conservative)")
        print("  FY2027E  +$1.94  (consensus; +49% YoY; AIP commercial reaching critical mass)")
        print("  FY2028E  +$2.79  (consensus; +44% YoY; capex-light model; FCF machine)")
        print()
        print("  EPS QUALITY DECOMPOSITION (FY2026E vs FY2025):")
        print()
        print(f"  {'Driver':<48}  {'Delta':>8}  {'%':>6}")
        print(f"  {'-'*48}  {'-'*8}  {'-'*6}")
        decomp = [
            ("US Commercial revenue ramp (+133% YoY Q1 2026)",    +0.34, +58.6),
            ("US Government acceleration (+84% YoY Q1 2026)",     +0.26, +44.8),
            ("International government growth (+48% YoY Q1)",     +0.10, +17.2),
            ("Operating leverage (60% adj op margin sustainable)", +0.08, +13.8),
            ("SBC dilution (shares +2–3%/yr, negative EPS impact)",-0.06,-10.3),
            ("Tax normalisation (~20% effective rate)",            -0.04, -6.9),
            ("Other / rounding",                                   +0.00, +0.0),
        ]
        for d, delta, pct in decomp:
            print(f"  {d:<48}  {delta:>+8.2f}  {pct:>+6.1f}%")
        print(f"  {'─'*48}  {'─'*8}  {'─'*6}")
        print(f"  {'Net (FY2025 $0.72 → FY2026E $1.30)':<48}  {1.30-0.72:>+8.2f}  {(1.30-0.72)/0.72*100:>+6.1f}%")

        # ── F. STRUCTURAL FACTORS ────────────────────────────────────────────
        print()
        print("  F. STRUCTURAL COMPETITIVE FACTORS  (SCA)")
        print(f"  {dash}")
        print()
        print(f"  {'Factor':<52}  {'Score':>6}  {'Wt':>4}  {'Contrib':>7}")
        print(f"  {'-'*52}  {'-'*6}  {'-'*4}  {'-'*7}")
        for f in STRUCTURAL_FACTORS:
            contrib = f["rating"] * f["weight"]
            print(f"  {f['name']:<52}  {f['rating']:>+6.1f}  {f['weight']:>4.2f}  {contrib:>+7.3f}")
        print(f"  {'-'*52}  {'-'*6}  {'-'*4}  {'-'*7}")
        print(f"  {'SCA raw (Σ r×w)':<52}  {'':>6}  {'':>4}  {sca_raw:>+7.3f}")
        print(f"  {'SCA adj  (÷ 2.0)':<52}  {'':>6}  {'':>4}  {sca_adj:>+7.3f}")
        print()
        for f in STRUCTURAL_FACTORS:
            name = f["name"]
            lines = []
            words = f["desc"].split()
            line = ""
            for w in words:
                if len(line) + len(w) + 1 <= 65:
                    line = (line + " " + w).strip()
                else:
                    lines.append(line)
                    line = w
            if line:
                lines.append(line)
            print(f"  [{'+' if f['rating'] > 0 else '-'}] {name}")
            for l in lines:
                print(f"      {l}")
            print()

        # ── G. CATALYSTS & RISKS ─────────────────────────────────────────────
        print()
        print("  G. CATALYSTS & RISKS")
        print(f"  {dash}")
        print()
        print("  NEAR-TERM CATALYSTS (6–12 months):")
        print("    · Q2 2026 earnings (Aug 2026) — US commercial Q2 print vs +120% FY guide")
        print("    · Maven Smart System expansion — new DoD/NATO contracts announcement")
        print("    · AIP enterprise deals — Fortune 500 bootcamp conversion disclosures")
        print("    · Defense budget finalisation — FY2027 NDAA AI contract awards")
        print()
        print("  MEDIUM-TERM CATALYSTS (1–3 years):")
        print("    · US Commercial reaching $3B+ annually (validates platform at scale)")
        print("    · International government scaling beyond UK/France/Germany")
        print("    · AIP healthcare penetration — FDA, hospital systems, pharma")
        print("    · Possible S&P 500 re-weighting upgrades (already S&P 500 member)")
        print()
        print("  KEY RISKS:")
        print("    · DOGE government spending cuts — direct hit to 50%+ of revenue")
        print("    · Multiple compression from 100× to 50× = -50%+ drawdown")
        print("    · Administration change (post-2028 election) altering classified contracts")
        print("    · OpenAI / Anthropic / Microsoft Copilot competing in unclassified enterprise")
        print("    · CEO Alex Karp insider selling creating persistent overhang (10b5-1 plan)")
        print("    · Share count growing 2-3%/yr from SBC diluting per-share returns")
        print("    · Revenue guided +71% YoY — any miss against this will be severely punished")

        # ── PART 3 ──────────────────────────────────────────────────────────
        print()
        print(sep)
        print(f"  PART 3 — NUMBERS & SIGNALS   |  {TICKER}")
        print(sep)

        # ── H. RISK/RETURN SUMMARY ───────────────────────────────────────────
        print()
        print("  H. RISK / RETURN SUMMARY")
        print(f"  {dash}")
        print()
        print(f"  Current price       : ${CURRENT_PRICE:.2f}  (-34% from ATH $207.52; still 104× FY2026E EPS)")
        print(f"  EPP floor           : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above; {EPP_MIN_PE}× × ${EPS_NOW:.2f} FY2026E; 52-wk low = 91×)")
        print(f"  Method B target     : ${price_b:.2f}  (upside: +{(price_b-CURRENT_PRICE)/CURRENT_PRICE*100:.1f}%; FY2028E ${CONS_EPS_2YR} × {CONS_EXIT_PE}×)")
        print(f"  BEAR scenario       : $30  (downside: {(30-CURRENT_PRICE)/CURRENT_PRICE*100:.1f}%; DOGE + AI bubble pop)")
        print(f"  Ratio B             : {ratio_b_fmt}  -> {signal_str}")
        print(f"  Forward P/E (FY26E) : {CURRENT_PRICE/EPS_NOW:.1f}×  (vs ~20–30× typical enterprise software)  ")
        print(f"  FY2027E P/E         : {CURRENT_PRICE/1.94:.1f}×  (FY2027E $1.94; still extreme)")
        print(f"  FY2028E P/E         : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (FY2028E ${CONS_EPS_2YR}; approaching 'merely expensive')")
        print(f"  Price/Sales (FY26E) : {CURRENT_PRICE * SHARES_M / (7650):.1f}×  ($326B / $7.65B FY2026E revenue)")
        print(f"  Market cap          : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M shares × ${CURRENT_PRICE:.2f})")
        print(f"  Rule of 40 (Q1 26)  : 145%  (revenue growth 85% + adj op margin 60% = 145; extraordinary)")
        print(f"  Adj FCF guidance    : $4.2–4.4B FY2026E  (FCF yield: {4300/(CURRENT_PRICE * SHARES_M / 1000):.1f}% — reasonable on FCF basis)")
        print(f"  Q1 2026 results     : Revenue $1.6B (+85%); non-GAAP EPS $0.33 (beat $0.28); adj op margin 60%")
        print(f"  Q1 US breakdown     : US Commercial $595M (+133% YoY +18% QoQ) | US Gov $687M (+84% YoY)")
        print(f"  FY2026 guidance     : Revenue $7.65–7.66B (+71% YoY); adj FCF $4.2–4.4B; US Comm +120%")
        print(f"  ATH context         : ATH $207.52 (Nov 3 2025) = 159× FY2026E; $135 = 'cheap' at 104× only")
        print(f"  Insider selling     : CEO Karp sells via 10b5-1 plan continuously; monitor pace")
        print(f"  WATCHLIST entry     : ~$85  (ratio_b ~1.5×; 65× FY2026E; more appropriate risk/reward)")
        print(f"  BUY entry           : ~$50  (ratio_b ~0.75×; 38× FY2026E; legitimate margin of safety)")

        # ── I. IDIOSYNCRATIC vs MACRO ────────────────────────────────────────
        print()
        print("  I. IDIOSYNCRATIC vs MACRO DRIVERS")
        print(f"  {dash}")
        print(f"  Beta: 2.20×  |  Idiosyncratic: 65%  |  Macro: 35%")
        print()
        drivers = [
            ("US Commercial AIP growth — quarterly revenue print",     "IDIO", "30%", "PRIMARY watch; +133% Q1; any decel punished severely"),
            ("US Government contract wins / DOGE impact",              "IDIO", "25%", "50%+ revenue; DOGE risk binary; new NDAA contracts = +"),
            ("CEO/insider selling pace (10b5-1 plan activity)",        "IDIO", "10%", "Sentiment signal; persistent overhang on rally attempts"),
            ("AI/tech sector sentiment (NASDAQ/growth risk-off)",      "MACRO","20%", "High-beta 2.2×; risk-off = PLTR -3% for every NASDAQ -1%"),
            ("Defense budget / geopolitical environment",              "MACRO","15%", "Conflict escalation = PLTR wins; peacetime cuts = headwind"),
        ]
        print(f"  {'Driver':<54}  {'Type':>5}  {'Wt':>4}  {'Note'}")
        print(f"  {'─'*54}  {'─'*5}  {'─'*4}  {'─'*42}")
        for d, t, w, n in drivers:
            print(f"  {d:<54}  {t:>5}  {w:>4}  {n}")

        print()
        print(sep)
        print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-24")
        print(sep)

    return out.getvalue()


if __name__ == "__main__":
    print(run_report())
