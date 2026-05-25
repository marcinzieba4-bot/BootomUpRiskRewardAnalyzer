#!/usr/bin/env python3
"""
intc_signal_model.py  —  Intel Corporation (NASDAQ: INTC)
Bottom-Up Risk/Reward Signal Model
All prices and EPS in USD.  EPS = non-GAAP adjusted (excludes SBC, amortisation,
  restructuring charges, acquisition-related items).
Fiscal year ends December 31.
"""

import math, sys, io, contextlib

TICKER        = "INTC"
COMPANY       = "Intel Corporation"
EXCHANGE      = "NASDAQ"
FY_END        = "December 31 (calendar year)"
SHARES_M      = 4200.0          # million diluted shares (approximate; Intel ~4.2B)

CURRENT_PRICE = 119.00          # INTC — fetched from web search, 2026-05-24
                                 # May 22 close: $119.84; May 24 range: $118.09–$122.78
                                 # ATH (recent): $129.44 on May 11, 2026; -8.1% from ATH
                                 # 52-week LOW: $18.97  →  stock up +527% from the bottom

# ── EPP FLOOR ──────────────────────────────────────────────────────────────
EPS_TROUGH        = -0.13       # FY2024; non-GAAP LOSS — first in Intel's modern history;
                                 # foundry losses + PC/server market share collapse + massive
                                 # restructuring charges dragged even non-GAAP into the red
EPS_TROUGH_PRICE  = 18.97       # 52-week low; Intel in FY2024-early-FY2025 with negative EPS;
                                 # stock priced as if Intel might structurally never recover
EPP_MIN_PE        = 20          # franchise floor for Intel; even in distress, x86 monopoly
                                 # (750M+ PCs, 70%+ data centre CPUs), CHIPS Act $19B in
                                 # grants+loans, and $100B+ in fab assets set a structural
                                 # floor; 20× applied to EPS_NOW gives $24 — consistent with
                                 # the actual 52-week low of $18.97 (market's implicit floor)
EPS_FY2025        = 0.65        # FY2025 estimated; Q3 2025 actual $0.23; annual recovery as
                                 # 18A ramped and restructuring savings flowed through
EPS_NOW           = 1.20        # FY2026E conservative; Q1 2026 actual $0.29 (beat guide);
                                 # Q2 2026 guided $0.20; company implied $1.30–1.60 full year;
                                 # analyst consensus $1.09; using $1.20 = midpoint conservative
EPP               = round(EPS_NOW * EPP_MIN_PE, 2)    # $24.00

epp_gap_pct       = round((CURRENT_PRICE - EPP) / EPP * 100, 1)    # +395.8%
below_floor       = CURRENT_PRICE < EPP                              # False

# ── METHOD B ───────────────────────────────────────────────────────────────
CONS_EPS_2YR  = 3.00            # FY2028E (2-yr horizon from May 2026); BULL-LEANING estimate;
                                 # FY2027E analyst consensus $1.56; FY2028E requires 18A to
                                 # win foundry customers + Panther Lake/Nova Lake CPU ramp;
                                 # $3.00 assumes ~$75–80B revenue × 16% non-GAAP net margin
                                 # / 4.2B shares — achievable only in the bull execution case
CONS_EXIT_PE  = 35              # recovery premium for a successful IDM turnaround; 35× is
                                 # generous vs Intel's historical 12–18× mid-cycle; reflects
                                 # optionality from foundry, AI PC, and national security moat
price_b       = round(CONS_EPS_2YR * CONS_EXIT_PE, 2)    # $105.00
# NOTE: price_b $105 < CURRENT_PRICE $119 → Method B BELOW current → N/A → AVOID
ratio_b_raw   = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE) if price_b > CURRENT_PRICE else None
ratio_b       = round(ratio_b_raw, 2) if ratio_b_raw is not None else None  # N/A → AVOID

# ── SOFTMAX ENGINE ─────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  {"price": 25.0,   "eps":  0.50, "pe": 50.0,
              "desc": "18A yields stall; AMD/ARM take CPU share; foundry never breaks even"},
    "BASE":  {"price": 90.0,   "eps":  2.60, "pe": 34.6,
              "desc": "FY2028E $2.60 × 35×; moderate 18A success; foundry breakeven delayed to FY2029"},
    "BULL":  {"price": 160.0,  "eps":  4.00, "pe": 40.0,
              "desc": "18A wins hyperscaler foundry customer; Panther Lake gains PC share; margins recover"},
    "XBULL": {"price": 300.0,  "eps":  6.50, "pe": 46.0,
              "desc": "Intel Foundry = US answer to TSMC; AI PC monopoly; FY2030 IDM renaissance"},
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
    {"name": "Intel 18A: yields +7%/month; HVM Oct 2025; customers arriving",
     "rating": +0.9, "weight": 0.25,
     "desc": ("Intel 18A entered high-volume manufacturing in October 2025 with yields "
              "improving approximately 7% per month — a milestone that most analysts thought "
              "was years away.  Intel CEO Lip-Bu Tan stated that foundry customers are 'knocking "
              "on the door' following 18A yield improvements.  Microsoft has already signed as "
              "an 18A external foundry customer.  Panther Lake (Intel's first 18A laptop CPU) "
              "is on track for H2 2026 consumer shipments.  If 18A achieves competitive parity "
              "with TSMC N2, Intel's foundry narrative changes from 'catch-up story' to 'viable "
              "TSMC alternative' — a trillion-dollar total addressable market.  This is the "
              "single most important data point in the Intel bull case and it is tracking well.")},
    {"name": "CHIPS Act national security backstop ($7.86B grants + $11B loans)",
     "rating": +0.7, "weight": 0.15,
     "desc": ("The US CHIPS and Science Act allocated Intel $7.86 billion in direct grants "
              "and up to $11 billion in loans — the largest single-company allocation in the "
              "Act.  This creates an asymmetric backstop: the US government has decided that "
              "Intel's manufacturing success is a national security imperative.  The funding "
              "de-risks the capex programme significantly.  No other company in semiconductor "
              "history has had this level of government financial backing.  The geopolitical "
              "dimension (China-Taiwan tensions, TSMC concentration risk) ensures that US "
              "policymakers cannot afford to let Intel's foundry programme fail — creating an "
              "implicit government put option on the stock below ~$40.")},
    {"name": "x86 installed base + Panther Lake AI PC catalyst (H2 2026)",
     "rating": +0.5, "weight": 0.10,
     "desc": ("Intel still holds 70%+ of data centre x86 CPU sockets (Xeon) and ~80% of "
              "PC CPUs.  While AMD has gained share, Intel's installed base is enormous — "
              "corporate refresh cycles benefit Intel when Panther Lake ships.  Panther Lake "
              "on 18A is Intel's first AI PC chip with NPU inference capabilities designed "
              "for on-device Copilot / local LLM.  If 18A performs as advertised, Panther "
              "Lake will be the most competitive Intel laptop chip since 2020.  A PC refresh "
              "cycle driven by Windows AI requirements (Copilot+PC specs require dedicated NPU) "
              "could drive a significant TAM uplift in H2 2026 and FY2027.")},
    {"name": "Stock up 527% from 52-wk low — priced for flawless execution",
     "rating": -0.9, "weight": 0.25,
     "desc": ("Intel's 52-week low was $18.97 (FY2024 EPS = -$0.13).  At $119, the stock "
              "has rallied +527% in approximately one year — one of the largest recoveries "
              "ever seen in a mega-cap semiconductor company.  This rally has pulled forward "
              "ALL of the 18A success, foundry breakeven, CPU recovery, and AI PC catalysts "
              "simultaneously.  The market is now pricing a near-perfect execution scenario. "
              "Even in our bullish FY2028E ($3.00 EPS × 35× = $105), the Method B target is "
              "BELOW the current price.  At $119, investors are paying for FY2028 results that "
              "may not materialise until FY2029-2030.  Any single execution miss — 18A yield "
              "delay, Panther Lake driver issue, foundry customer cancellation — could send "
              "the stock back to $50-70 within weeks.")},
    {"name": "TSMC execution gap — Intel 18A vs TSMC N2/A16; AMD server share loss",
     "rating": -0.6, "weight": 0.15,
     "desc": ("TSMC is not standing still.  TSMC N2 (2nm) is already in volume production "
              "for Apple; A16 (next-gen backside power delivery) ships in 2026.  Intel 18A, "
              "while impressive, is entering a market where TSMC has 30+ years of pure-play "
              "foundry customer relationships, proven defect density records, and packaging "
              "leadership.  Intel has ONE external foundry customer confirmed (Microsoft). "
              "The revenue to break even on Intel Foundry requires $15-20B in external revenue "
              "— a number that requires winning NVIDIA, Apple, Qualcomm, or AMD as customers. "
              "None of these have been announced.  Meanwhile, AMD EPYC (Turin) continued to "
              "take data centre CPU socket share from Intel Xeon in FY2025 — the most profitable "
              "segment of Intel's product business.")},
    {"name": "Foundry losses — breakeven not until FY2028; $18B capex in FY2026",
     "rating": -0.5, "weight": 0.10,
     "desc": ("Intel Foundry (IFS) lost money in every single quarter of FY2024 and FY2025. "
              "Management targets foundry breakeven by late FY2027 or early FY2028 — a 2-3 "
              "year timeline with no guarantee.  In FY2026, Intel plans $18B in capital "
              "expenditure — among the highest in corporate history.  This massive cash burn "
              "constrains Intel's ability to return capital or invest in other priorities. "
              "Even at $13.6B Q1 2026 revenue (+7% YoY), free cash flow remains negative. "
              "FCF breakeven is not expected until FY2027 at the earliest.  The foundry "
              "business is essentially a multi-year call option that requires perfect execution "
              "AND customer wins AND process leadership AND market timing to pay off.")},
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

    ratio_b_fmt = "N/A"   # Method B below current price

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        W    = 72
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
        print(f"  Sector   : Semiconductor IDM · x86 CPU · Intel Foundry (IFS) · AI PC")
        print(f"  FY end   : {FY_END}")
        print(f"  EPS basis: Non-GAAP adjusted (excludes SBC, restructuring, amortisation)")
        print(f"  Shares   : ~{SHARES_M:.0f}M diluted (approximate; large restructuring in progress)")
        print(f"  Price    : ${CURRENT_PRICE:.2f}  [2026-05-24; -8.1% from recent ATH $129.44 (May 11)]")
        print(f"  52-week  : $18.97 low – $129.44 high  (+527% from 52-wk low — one of the")
        print(f"             largest mega-cap semiconductor recoveries in market history)")

        print()
        print(sep)
        print(f"  PART 2 — ANALYST COMMENTARY  |  {TICKER}")
        print(sep)

        # ── A. INVESTMENT THESIS ─────────────────────────────────────────────
        print()
        print("  A. INVESTMENT THESIS")
        print(f"  {dash}")
        print()
        print("  Intel's story is simple to describe and brutally difficult to execute:")
        print("  the world's most important semiconductor company nearly died, and now it")
        print("  is trying to be reborn.  The question is not whether Intel can recover")
        print("  — it is whether the stock at $119 already prices in that recovery.")
        print()
        print("  THE COLLAPSE (FY2020–FY2024):")
        print()
        print("  Intel was the most dominant technology company of the 1990s and 2000s.")
        print("  Then it fell behind on manufacturing.  TSMC mastered the art of process")
        print("  node shrinks while Intel stumbled on 10nm, then again on 7nm.  AMD, using")
        print("  TSMC's nodes, launched Ryzen (2017) and EPYC (2017-2023) — attacking")
        print("  Intel in both PC and data centre.  By FY2024:")
        print()
        print("    · Non-GAAP EPS: -$0.13 (first non-GAAP loss in Intel's modern history)")
        print("    · Stock: $18.97 at the 52-week low — a 30-year price low")
        print("    · Foundry: Losing money every quarter with no clear breakeven path")
        print("    · CEO: Pat Gelsinger fired; Lip-Bu Tan (ex-Cadence CEO) appointed Mar 2024")
        print()
        print("  THE TURNAROUND THESIS (FY2025–FY2028):")
        print()
        print("  1. 18A PROCESS NODE — THE MAKE-OR-BREAK CATALYST:")
        print("     Intel 18A entered high-volume manufacturing in October 2025 with yields")
        print("     improving ~7% monthly.  This is Intel's first competitive process node")
        print("     in nearly a decade.  18A uses RibbonFET (Intel's version of Gate-All-")
        print("     Around transistors) and PowerVia (backside power delivery) — the same")
        print("     technologies TSMC is deploying in its N2P and A16 nodes.  If Intel's")
        print("     18A delivers on density and performance-per-watt, it is TSMC-competitive.")
        print("     CEO Lip-Bu Tan says foundry customers are 'knocking on the door.'")
        print("     Microsoft is confirmed as an external 18A customer.")
        print()
        print("  2. PANTHER LAKE — FIRST 18A CONSUMER PRODUCT (H2 2026):")
        print("     Panther Lake is Intel's next-gen laptop CPU on 18A, shipping H2 2026.")
        print("     If 18A performs, Panther Lake will be the most competitive Intel laptop")
        print("     chip since Core i7-6700HQ.  Windows AI PCs (Copilot+PC) require on-device")
        print("     NPU inference — Panther Lake's integrated NPU is designed for this market.")
        print("     A successful Panther Lake launch validates 18A and accelerates the")
        print("     external foundry customer acquisition story.")
        print()
        print("  3. CHIPS ACT — THE GOVERNMENT PUT:")
        print("     $7.86B in direct grants + $11B in government loans = $18.86B in US")
        print("     government financial backing.  The geopolitical rationale is clear:")
        print("     Taiwan concentration risk makes domestic US semiconductor manufacturing")
        print("     a national security imperative.  Intel cannot fail — the US government")
        print("     will not allow it.  This creates an implicit floor in the stock.")
        print()
        print("  WHY AVOID AT $119:")
        print()
        print("  The bull case is real.  18A tracking well, CHIPS Act backstop, 18-month")
        print("  CEO honeymoon delivering results.  But the stock has already rallied +527%.")
        print("  The market has now priced ALL of this in simultaneously:")
        print()
        print("  Method B (FY2028E $3.00 × 35× = $105) is BELOW the current price of $119.")
        print("  Even in a bullish 2-year scenario, the math does not support buying here.")
        print("  The margin of safety has been completely eliminated by the 6× rally.")
        print()
        print("  At $119 / $1.20 FY2026E EPS = 99.2× forward P/E.  Intel is now trading")
        print("  at nearly 100× the earnings of a company that lost money 12 months ago.")
        print("  This is speculation on the turnaround, not investment in the turnaround.")
        print()
        print(f"  Signal: {signal_str}  |  Ratio B: {ratio_b_fmt}  |  EPP gap: +{epp_gap_pct:.1f}%")
        print(f"  Method B $105 (FY2028E $3.00 × 35×) is BELOW current price → N/A")
        print(f"  WATCHLIST entry: ~$70–80 (FY2027E $1.56 × 45–50×; ratio_b ~1.5×)")
        print(f"  BUY entry: ~$40–50 (ratio_b ~0.75×; buying the optionality at fair value)")

        # ── B. EPP FLOOR ─────────────────────────────────────────────────────
        print()
        print("  B. EARNINGS POWER PRICE (EPP) — STRUCTURAL FLOOR")
        print(f"  {dash}")
        print()
        print(f"  EPS anchor   : ${EPS_TROUGH:.2f}  (FY2024; non-GAAP LOSS — first in modern Intel")
        print(f"                  history; foundry losses + market share erosion + restructuring)")
        print(f"  Trough price : ${EPS_TROUGH_PRICE:.2f}  (52-week low; market pricing existential risk")
        print(f"                  for Intel; stock priced as if TSMC had already won)")
        print(f"  EPP min P/E  : {EPP_MIN_PE}×  (franchise floor; fab assets, x86 monopoly, CHIPS Act")
        print(f"                  backstop prevent a full wipeout; 20× × $1.20 = $24 ≈ trough)")
        print(f"  EPS now      : ${EPS_NOW:.2f}  (FY2026E; Q1 $0.29 actual; Q2 $0.20 guided; H2 ramp)")
        print(f"  EPP          : ${EPP:.2f}  ({EPP_MIN_PE}× × ${EPS_NOW:.2f})")
        print()
        print(f"  Current price ${CURRENT_PRICE:.2f} is +{epp_gap_pct:.1f}% ABOVE EPP floor ${EPP:.2f}")
        print()
        print(f"  NOTE: EPP $24 aligns almost exactly with the actual 52-week low of $18.97.")
        print("  This validates the framework: at the worst moment (FY2024, -$0.13 EPS),")
        print("  the market set the structural floor at ~$19-24, consistent with 20× applied")
        print(f"  to the recovering EPS power.  A return to EPP from $119 = -{(CURRENT_PRICE-EPP)/CURRENT_PRICE*100:.1f}% drawdown.")
        print("  This is the bear case scenario: if 18A stalls, the floor is ~$25-30.")

        # ── C. METHOD B ──────────────────────────────────────────────────────
        print()
        print("  C. METHOD B — 2-YEAR EARNINGS POWER TARGET")
        print(f"  {dash}")
        print()
        print(f"  Consensus EPS (FY2028E) : ${CONS_EPS_2YR:.2f}  (BULLISH estimate; requires 18A ramp +")
        print(f"                             foundry contribution + CPU market stabilisation)")
        print(f"  Exit P/E                : {CONS_EXIT_PE}×  (generous recovery premium for successful IDM)")
        print(f"  Method B target         : ${price_b:.2f}  ({CONS_EXIT_PE}× × ${CONS_EPS_2YR:.2f})")
        print(f"  Current price           : ${CURRENT_PRICE:.2f}")
        print()
        print(f"  ┌─────────────────────────────────────────────────────────────────┐")
        print(f"  │  ✕  Method B ${price_b:.2f} is BELOW current price ${CURRENT_PRICE:.2f}          │")
        print(f"  │     Even in a bullish FY2028 scenario, 2-year upside = NEGATIVE  │")
        print(f"  │     Ratio B = N/A  →  Signal: {signal_str:<37} │")
        print(f"  └─────────────────────────────────────────────────────────────────┘")
        print()
        print("  SENSITIVITY — what FY2028E EPS × P/E is needed to justify $119:")
        print()
        print(f"  {'FY28E EPS':>10}  {'Exit P/E':>8}  {'Method B':>10}  {'vs Current':>10}  {'Signal'}")
        print(f"  {'-'*10}  {'-'*8}  {'-'*10}  {'-'*10}  {'-'*18}")
        cases = [
            (2.50, 35), (2.50, 45), (3.00, 35), (3.00, 40), (3.00, 45),
            (3.50, 35), (3.50, 40), (4.00, 35), (4.00, 40), (5.00, 30),
        ]
        for eps_t, pe_t in cases:
            pb_t = eps_t * pe_t
            if pb_t <= CURRENT_PRICE:
                sig_t   = "✕ AVOID (below)"
                gap_str = f"${CURRENT_PRICE - pb_t:.1f} below"
            else:
                rb_t  = (CURRENT_PRICE - EPP) / (pb_t - CURRENT_PRICE)
                sig_t = ratio_b_signal(rb_t)
                gap_str = f"+{(pb_t-CURRENT_PRICE)/CURRENT_PRICE*100:.1f}%"
            print(f"  ${eps_t:>9.2f}  {pe_t:>8}×  ${pb_t:>9.2f}  {gap_str:>10}  {sig_t}")
        print()
        print("  KEY INSIGHT: To get to WATCHLIST, you need FY2028E EPS of $4.00 at 40×")
        print("  ($160 target = +34% upside → ratio_b ~1.5×). That requires Intel to:")
        print("    · Win 3-5 major external foundry customers beyond Microsoft")
        print("    · Recover 3-5 pts of server CPU market share from AMD")
        print("    · Achieve 18% non-GAAP net margin (vs current <5%)")
        print("  All simultaneously.  At $50–70, you get this optionality at fair value.")

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
        mc_desc = ("market pricing between BASE and BULL — fully priced for moderate turnaround success"
                   if market_composite < 2.5 else
                   "market pricing BULL scenario — significant execution optionality priced in")
        print(f"  → {adj_composite:.2f} = {mc_desc}")

        # ── E. EARNINGS TRAJECTORY ───────────────────────────────────────────
        print()
        print("  E. EARNINGS TRAJECTORY (non-GAAP adjusted EPS; calendar year)")
        print(f"  {dash}")
        print()
        print("  FY2019   ~$4.87  (peak era; dominant Intel; 10nm struggles beginning)")
        print("  FY2020   ~$5.30  (COVID PC boom; but manufacturing gap widening)")
        print("  FY2021   ~$5.47  ◀ PEAK EPS  (last hurrah; AMD still <20% server share)")
        print("  FY2022   ~$1.84  (PC crash + AMD EPYC Genoa launching; 10nm ramp issues)")
        print("  FY2023   ~$1.05  (continued share loss; foundry losses begin; x86 flat)")
        print("  FY2024   -$0.13  ◀ TROUGH EPS  (non-GAAP LOSS; first in modern history)")
        print("  FY2025   ~$0.65  (early recovery; 18A HVM Oct 2025; restructuring savings)")
        print("  FY2026E   $1.20  (Q1 $0.29 actual; guided $1.09–1.60; using $1.20 cons.)")
        print("  FY2027E  ~$1.56  (analyst consensus; 18A/Panther Lake ramp contributing)")
        print("  FY2028E  ~$3.00  (BULL scenario; foundry at breakeven; margin recovery)")
        print()
        print("  Q1 2026 DETAIL:")
        print(f"  {'Metric':<40}  {'Q1 2026':>12}  {'YoY':>8}")
        print(f"  {'-'*40}  {'-'*12}  {'-'*8}")
        q1_data = [
            ("Revenue",                          "$13.6B",      "+7%"),
            ("Non-GAAP EPS",                     "$0.29",       "N/M (vs -$0.13 FY24)"),
            ("Non-GAAP gross margin",             "41%",         "+650bps vs guide"),
            ("DCAI (Data Centre + AI) revenue",  "$4.1B",       "+22%"),
            ("Client (PC) revenue",               "$7.2B",       "+4%"),
            ("Intel Foundry revenue (external)",  "nascent",     "Microsoft 18A signed"),
            ("Q2 2026 revenue guidance",          "$13.8–14.8B", "+2–8% YoY"),
            ("Q2 2026 non-GAAP EPS guidance",     "$0.20",       "sequential dip (mix)"),
            ("FY2026 implied revenue range",      "$58–62B",     "+7–14% YoY"),
            ("FY2026 capex",                      "~$18B",       "peak capex year"),
        ]
        for m, v, yoy in q1_data:
            print(f"  {m:<40}  {v:>12}  {yoy:>8}")

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
            print(f"  [{'+' if f['rating'] > 0 else '-'}] {f['name']}")
            for l in lines:
                print(f"      {l}")
            print()

        # ── G. CATALYSTS & RISKS ─────────────────────────────────────────────
        print()
        print("  G. CATALYSTS & RISKS")
        print(f"  {dash}")
        print()
        print("  NEAR-TERM CATALYSTS (6–12 months):")
        print("    · Panther Lake consumer laptop launch (H2 2026) — 18A first mass-market test")
        print("    · 2nd major external foundry customer announcement (beyond Microsoft)")
        print("    · Nova Lake (next desktop/workstation CPU on Intel 18A) tape-in confirmation")
        print("    · Q2 2026 results (July 2026) — revenue and margin versus guidance")
        print("    · CHIPS Act funding disbursement milestones (tied to employment/production)")
        print()
        print("  MEDIUM-TERM CATALYSTS (1–3 years):")
        print("    · Intel Foundry breakeven (management targets late FY2027/early FY2028)")
        print("    · 14A process node tape-out (Intel's next-gen after 18A; ~2027)")
        print("    · Intel IPF (Intel Foundry) potential IPO or spin-off (discussed)")
        print("    · Gaudi AI accelerator winning hyperscaler AI training orders")
        print("    · FCF turning positive (not until FY2027 at earliest)")
        print()
        print("  KEY RISKS:")
        print("    · 18A yield issues — any deceleration from 7%/month improvement = stock -30%")
        print("    · External foundry customers not materialising beyond Microsoft")
        print("    · AMD Turin/Venice + ARM data centre CPUs further eroding Xeon share")
        print("    · $18B capex + foundry losses creating FCF pressure for 2+ more years")
        print("    · Multiple compression: 100× → 35× on FY2026E EPS = -65% at current earnings")
        print("    · Panther Lake execution risk — first 18A consumer product; any defect = headline")
        print("    · Geopolitical risk: China revenue ~25% of INTC; BIS/export controls exposure")

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
        print(f"  Current price       : ${CURRENT_PRICE:.2f}  (+527% from 52-wk low $18.97; -8% from ATH $129.44)")
        print(f"  EPP floor           : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above; {EPP_MIN_PE}× × ${EPS_NOW:.2f}; aligns with actual trough)")
        print(f"  Method B target     : ${price_b:.2f}  (FY2028E ${CONS_EPS_2YR:.0f} × {CONS_EXIT_PE}× = BELOW CURRENT → N/A)")
        print(f"  BEAR scenario       : $25  (-79%; 18A stalls; foundry losses deepen; de-rating)")
        print(f"  Ratio B             : N/A  (Method B below current) → {signal_str}")
        print(f"  Forward P/E (FY26E) : {CURRENT_PRICE/EPS_NOW:.1f}×  ($119 / $1.20; pricing 2028-era earnings today)")
        print(f"  FY2027E P/E         : {CURRENT_PRICE/1.56:.1f}×  (FY2027E $1.56 analyst consensus; still extreme)")
        print(f"  FY2028E P/E (bull)  : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (FY2028E ${CONS_EPS_2YR:.2f} bull scenario; approaching rational)")
        print(f"  Market cap          : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M shares × ${CURRENT_PRICE:.2f})")
        print(f"  Q1 2026 revenue     : $13.6B (+7% YoY); DCAI $4.1B (+22%); GM 41% (+650bps vs guide)")
        print(f"  18A status          : HVM Oct 2025; yields +7%/month; Panther Lake H2 2026")
        print(f"  External foundry    : Microsoft confirmed; 'customers knocking' per CEO Lip-Bu Tan")
        print(f"  CHIPS Act           : $7.86B direct grants + $11B loans = $18.86B government backing")
        print(f"  FY2026 capex        : ~$18B (peak year; FCF still negative; CHIPS Act funding offsets)")
        print(f"  Foundry breakeven   : Management targets late FY2027/early FY2028")
        print(f"  Dividend            : $0.05/quarter reinstated ($0.20/yr; 0.17% yield — token)")
        print(f"  Analyst consensus   : $87.86 average PT (48 analysts; 26% BELOW current price)")
        print(f"  AVOID thesis breaks : 18A fails completely; stocks returns to $25-40 (EPP zone)")
        print(f"  WATCHLIST entry     : ~$70–80 (FY2027E $1.56 × 45-50×; ratio_b ~1.5×)")
        print(f"  ACCUMULATE entry    : ~$50 (ratio_b ~0.75×; 42× FY2026E; fair turnaround option)")
        print(f"  BUY entry           : ~$35–40 (ratio_b ~0.75× on EPS_NOW; optionality cheap)")

        # ── I. IDIOSYNCRATIC vs MACRO ────────────────────────────────────────
        print()
        print("  I. IDIOSYNCRATIC vs MACRO DRIVERS")
        print(f"  {dash}")
        print(f"  Beta: 1.05×  |  Idiosyncratic: 75%  |  Macro: 25%")
        print()
        drivers = [
            ("Intel 18A yield trajectory (monthly progress reports)",    "IDIO", "35%", "PRIMARY: 7%/month must sustain; any decel = -30% stock"),
            ("External foundry customer announcements",                   "IDIO", "25%", "Next customer beyond MSFT = massive catalyst; still 0 others"),
            ("Panther Lake launch quality (H2 2026 reviews/benchmarks)",  "IDIO", "15%", "First 18A product in consumer hands; defect = catastrophe"),
            ("PC/server macro cycle (AI PC demand, enterprise refresh)",  "MACRO","15%", "AI PC Copilot+ tailwind real but Intel CPU share uncertain"),
            ("China trade restrictions / export controls on chips",       "MACRO","10%", "~25% of INTC revenue from China; BIS escalation = material"),
        ]
        print(f"  {'Driver':<56}  {'Type':>5}  {'Wt':>4}  {'Note'}")
        print(f"  {'─'*56}  {'─'*5}  {'─'*4}  {'─'*38}")
        for d, t, w, n in drivers:
            print(f"  {d:<56}  {t:>5}  {w:>4}  {n}")

        print()
        print(sep)
        print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-24")
        print(sep)

    return out.getvalue()


if __name__ == "__main__":
    print(run_report())
