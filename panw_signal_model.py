#!/usr/bin/env python3
"""
panw_signal_model.py  —  Palo Alto Networks, Inc. (NASDAQ: PANW)
Bottom-Up Risk/Reward Signal Model
All prices and EPS in USD.  EPS = non-GAAP adjusted (excludes SBC, amortisation).
Fiscal year ends July 31.  2-for-1 stock split completed December 2024.
All per-share figures are post-split.
"""

import math, sys, io, contextlib

TICKER        = "PANW"
COMPANY       = "Palo Alto Networks, Inc."
EXCHANGE      = "NASDAQ"
FY_END        = "July 31 (FY2026 ends Jul 31, 2026; FY2028 ends Jul 31, 2028)"
SHARES_M      = 818.0           # million diluted (post 2-for-1 split Dec 2024; ~$213B / $260)

CURRENT_PRICE = 260.00          # PANW — fetched from web search, 2026-05-24
                                 # May 22 close: $260.13; ATH intraday May 22: $261.41
                                 # Stock near ATH; +44% recent surge on cyber sector strength
                                 # Q3 FY2026 earnings due June 2, 2026 (9 days away)

# ── EPP FLOOR ──────────────────────────────────────────────────────────────
EPS_TROUGH        = 2.84        # FY2024 (ended Jul 2024); post-split; platformization strategy
                                 # announced Feb 2024 shocked market; billings missed; stock crashed
                                 # to ~$135 (post-split); EPS itself continued growing but growth
                                 # narrative was disrupted → trough multiple applied to trough EPS
EPS_TROUGH_PRICE  = 135.0       # post-split; PANW February 2024 crash low (~$270 pre-split / $135
                                 # post-split); 48× FY2024 EPS = market applying distress multiple
                                 # despite continued earnings growth
EPP_MIN_PE        = 40          # structural floor for the #1 cybersecurity platform; 40× reflects
                                 # "critical infrastructure" premium — enterprise security is non-
                                 # discretionary; even at trough PANW deserves 40× given contracts
EPS_FY2025        = 3.34        # FY2025 (ended Jul 2025); post-split; Q1 $0.78 + Q2 $0.81 +
                                 # Q3 $0.80 + Q4 $0.95 = $3.34; platformization drag on near-term
                                 # billings growth, but margins held steady
EPS_NOW           = 3.67        # FY2026E; company guided $3.65–$3.70 (midpoint); Q1 actual $0.93
                                 # (beat $0.88–0.90 guide); Q2 actual $1.03 (beat $0.94 est); Q3
                                 # guided $0.78–$0.80; Q4 estimated $0.90–0.95; total ≈ $3.67
EPP               = round(EPS_NOW * EPP_MIN_PE, 2)    # $146.80

epp_gap_pct       = round((CURRENT_PRICE - EPP) / EPP * 100, 1)    # +77.1%
below_floor       = CURRENT_PRICE < EPP                              # False

# ── METHOD B ───────────────────────────────────────────────────────────────
CONS_EPS_2YR  = 7.00            # FY2028E (ends Jul 2028; 2-yr horizon from May 2026); company
                                 # targets 40% adj FCF margin by FY2028; at ~$15–16B revenue × 40%
                                 # FCF margin = $6–6.4B FCF / 818M shares = $7.3–7.8 FCF/share;
                                 # using $7.00 non-GAAP EPS = slight discount to FCF (conservative)
CONS_EXIT_PE  = 40              # generous for a mature cybersecurity platform; historical PANW
                                 # mid-cycle 50–80×; 40× in 2028 = maturation discount from 70×
                                 # today; reflects revenue growth decelerating to ~15-18% by FY2028
price_b       = round(CONS_EPS_2YR * CONS_EXIT_PE, 2)    # $280.00
ratio_b_raw   = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE) if price_b > CURRENT_PRICE else None
ratio_b       = round(ratio_b_raw, 2) if ratio_b_raw is not None else None  # 5.66x → AVOID

# ── SOFTMAX ENGINE ─────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  {"price": 80.0,   "eps":  2.50, "pe": 32.0,
              "desc": "Cyber spending cuts + M&A integration drag; platformization stalls; 30× EPS"},
    "BASE":  {"price": 280.0,  "eps":  7.00, "pe": 40.0,
              "desc": "FY2028E $7.00 × 40×; Rule of 60 on track; NGS ARR reaches $16B by FY2028"},
    "BULL":  {"price": 380.0,  "eps":  8.50, "pe": 45.0,
              "desc": "Platformization accelerates; Cortex XSIAM wins SOC market; FCF margin >42%"},
    "XBULL": {"price": 550.0,  "eps": 11.00, "pe": 50.0,
              "desc": "PANW becomes the Microsoft of cybersecurity; $20B NGS ARR by FY2030; AI-SOC"},
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
    {"name": "Platformization consolidation moat (1,550+ customers, 119% NRR)",
     "rating": +0.8, "weight": 0.25,
     "desc": ("Palantir's platform customers — those running 3+ PANW modules (Strata, Prisma, "
              "Cortex) — have a net retention rate of 119% and single-digit churn.  Once an "
              "enterprise moves to the full Palo Alto platform, switching costs become extreme "
              ": ripping out firewall, cloud security, AND the SOC simultaneously requires "
              "a complete security re-architecture.  The platformization strategy (offering "
              "free trials and discounts to consolidate) creates a temporary billings headwind "
              "but locks in customers for 10+ years.  1,550 platform customers added 110 net "
              "new in Q2 FY2026 — a quarterly record.  NGS ARR (contracted SaaS/sub revenue) "
              "of $8.52–8.62B guided for FY2026, growing 53–54% YoY including M&A.")},
    {"name": "NGS ARR growth engine ($8.5B + targeting $20B by FY2030)",
     "rating": +0.7, "weight": 0.20,
     "desc": ("PANW's Next-Gen Security ARR is the most important forward-looking metric. "
              "It represents contracted, recurring SaaS/subscription revenue — essentially a "
              "software annuity.  At $8.5B+ for FY2026 growing at 53%, the ARR alone is worth "
              "$170B+ at a 20× ARR multiple.  The $20B NGS ARR target for FY2030 (from current "
              "$8.5B) implies ~24% CAGR — highly visible given platformization conversion rates. "
              "Unlike traditional security vendors, PANW's ARR model creates revenue visibility "
              "3–5 years out.  This is the moat: as ARR compounds, billings volatility matters "
              "less and revenue quality (recurring %) improves.")},
    {"name": "Cortex XSIAM AI-powered SOC — winning against CrowdStrike",
     "rating": +0.6, "weight": 0.10,
     "desc": ("Cortex XSIAM is PANW's AI-native Security Operations Center platform.  It "
              "replaces 15–30 point products with a single AI-driven platform that ingests "
              "all telemetry, triages alerts, and auto-remediates threats.  Win rate against "
              "CrowdStrike Falcon in competitive SOC bids is >60% per management commentary. "
              "The AI angle (AutoML models trained on 1T+ security events) is a genuine moat "
              "— PANW has more threat intelligence than any competitor from its 92K+ customer "
              "base.  XSIAM is also driving the Rule of 60 (revenue growth + FCF margin ≥ 60) "
              "as it carries premium ARR pricing vs point product alternatives.")},
    {"name": "Valuation at ATH — 70× FY2026E, near-term earnings event risk",
     "rating": -0.9, "weight": 0.25,
     "desc": ("At $260 / $3.67 FY2026E non-GAAP EPS = 70.8× forward P/E.  The stock hit an "
              "ATH of $261.41 on May 22, 2026 — just 9 days before Q3 FY2026 earnings on "
              "June 2, 2026.  This creates maximum 'sell the news' risk: if Q3 beats but "
              "raises guidance only modestly, the stock could sell off 15–20%.  The 44% "
              "surge prior to earnings (driven by a competitor's strong results) has pulled "
              "forward future returns.  At 70× FY2026E, PANW is priced for sustained 25%+ "
              "revenue CAGR AND margin expansion — a narrow corridor.  Any Q3 weakness in "
              "new platformization wins or NGS ARR growth decel = significant drawdown.")},
    {"name": "EPS growth decelerating despite 22% revenue growth (M&A dilution)",
     "rating": -0.5, "weight": 0.20,
     "desc": ("FY2025 to FY2026E EPS growth: $3.34 → $3.67 = only +10%.  Revenue growing "
              "22–23% but EPS growing at 10% — massive divergence from operating leverage. "
              "Reasons: (1) IBM QRadar and other M&A adding ~$340M quarterly revenue at "
              "lower-than-average margins; (2) ongoing platformization discounts reducing "
              "near-term billings quality; (3) high SBC (~$800M–1B/yr) diluting per-share "
              "metrics; (4) integration costs for multiple acquisitions.  Investors pricing "
              "in the 2028 Rule of 60 target, but getting there requires flawless execution "
              "across Strata, Prisma, Cortex, and all acquired platforms simultaneously.")},
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
        print(f"  Sector   : Cybersecurity Platform · Zero Trust · AI-Powered SOC · Cloud Security")
        print(f"  FY end   : {FY_END}")
        print(f"  EPS basis: Non-GAAP adjusted (excludes SBC ~$800M–1B/yr, amortisation)")
        print(f"  Shares   : ~{SHARES_M:.0f}M diluted (post 2-for-1 split Dec 2024)")
        print(f"  Price    : ${CURRENT_PRICE:.2f}  [2026-05-24; near ATH $261.41 (May 22 2026)]")
        print(f"  52-week  : ~$160 low – $261.41 high  (recent +44% cyber sector surge to ATH)")
        print(f"  ⚠ Q3 FY2026 earnings due June 2, 2026 — 9 days away; MAXIMUM event risk")

        print()
        print(sep)
        print(f"  PART 2 — ANALYST COMMENTARY  |  {TICKER}")
        print(sep)

        # ── A. INVESTMENT THESIS ─────────────────────────────────────────────
        print()
        print("  A. INVESTMENT THESIS")
        print(f"  {dash}")
        print()
        print("  Palo Alto Networks is the largest pure-play cybersecurity company in the")
        print("  world by revenue, and it is executing a deliberate strategy to become the")
        print("  Microsoft of enterprise security — a platform that replaces 30-40 point")
        print("  products with one integrated, AI-driven security operating system.")
        print()
        print("  PANW operates across three security domains:")
        print("    · Strata   — network security (firewall, SASE, SD-WAN)")
        print("    · Prisma   — cloud security (CNAPP, DSPM, code security)")
        print("    · Cortex   — AI-powered SOC (XSIAM, XDR, XSOAR, XPANSE)")
        print()
        print("  The PLATFORMIZATION strategy (announced February 2024) is the defining")
        print("  thesis.  PANW offers enterprises deep discounts — or even free trials")
        print("  — to consolidate 3+ modules onto the full platform.  Short-term pain")
        print("  (billings volatility, near-term EPS deceleration), long-term gain (119%")
        print("  net retention rate once fully platformised, multi-year lock-in, much")
        print("  higher lifetime customer value).")
        print()
        print("  THE BULL CASE — PLATFORMIZATION PAYOFF + AI-SOC DOMINANCE:")
        print()
        print("  1. NGS ARR COMPOUNDING ($8.5B → $20B by FY2030):")
        print("     Next-Gen Security ARR is the software annuity at the core of the")
        print("     business.  Platform customers have 119% NRR — every year they spend")
        print("     19% more automatically.  The $20B NGS ARR FY2030 target at even 15×")
        print("     ARR = $300B company.  1,550 platform customers (Q2 FY2026), adding")
        print("     110 per quarter.  The funnel is building and converting.")
        print()
        print("  2. CORTEX XSIAM — WINNING THE AI-SOC WAR:")
        print("     The SOC (Security Operations Centre) is the most crowded and highest-")
        print("     value battleground in cybersecurity.  XSIAM replaces SIEM, SOAR, and")
        print("     XDR simultaneously with a single AI platform.  Management claims >60%")
        print("     win rate vs CrowdStrike in competitive SOC replacements.  If XSIAM")
        print("     wins, PANW gets 3-5× more ARPU from that customer vs Strata-only.")
        print()
        print("  3. RULE OF 60 BY FY2028:")
        print("     PANW targets (revenue growth % + adj FCF margin %) ≥ 60 by FY2028.")
        print("     At ~15% revenue growth + 45% FCF margin, this is achievable.  40%")
        print("     adj FCF margin by FY2028 on ~$16B revenue = $6.4B FCF/yr.  At 818M")
        print("     shares = $7.82 FCF/share — a major step change from $3.67 today.")
        print()
        print("  THE BEAR CASE — AT THE ATH, HEADING INTO EARNINGS:")
        print()
        print("  At $260, PANW trades at 70.8× FY2026E non-GAAP EPS.  The stock hit its")
        print("  all-time high of $261.41 on May 22 — just 9 days before Q3 FY2026")
        print("  earnings on June 2, 2026.  The +44% recent surge (driven partly by a")
        print("  competitor's strong earnings) has already priced in the beat.")
        print()
        print("  Method B: FY2028E $7.00 × 40× = $280 — only +7.7% from current.")
        print("  Even with a generous FY2028E estimate and a still-elevated 40× exit")
        print("  P/E, the 2-year BASE case return is barely positive.")
        print()
        print("  EPS growth problem: FY2025 $3.34 → FY2026E $3.67 = only +10%, despite")
        print("  22-23% revenue growth.  M&A integration, SBC, and platformization")
        print("  discounts are consuming the operating leverage that bulls expect.")
        print()
        print(f"  Signal: {signal_str}  |  Ratio B: {ratio_b_fmt}  |  EPP gap: +{epp_gap_pct:.1f}%")
        print(f"  WATCHLIST entry: ~$185–195 (ratio_b ~1.5×); ACCUMULATE: ~$165 (ratio_b ~1.0×)")
        print(f"  ⚠ Earnings risk: Q3 FY2026 June 2 — stock at ATH = asymmetric downside")

        # ── B. EPP FLOOR ─────────────────────────────────────────────────────
        print()
        print("  B. EARNINGS POWER PRICE (EPP) — STRUCTURAL FLOOR")
        print(f"  {dash}")
        print()
        print(f"  EPS anchor   : ${EPS_TROUGH:.2f}  (FY2024 post-split; platformization shock year;")
        print(f"                  EPS continued to grow but market applied trough multiple)")
        print(f"  Trough price : ${EPS_TROUGH_PRICE:.2f}  (post-split; Feb 2024 crash on platformization")
        print(f"                  announcement; 48× $2.84 = market correctly repriced near-term growth)")
        print(f"  EPP min P/E  : {EPP_MIN_PE}×  (franchise floor for #1 cybersecurity platform; security is")
        print(f"                  non-discretionary; 40× reflects critical infrastructure premium)")
        print(f"  EPS now      : ${EPS_NOW:.2f}  (FY2026E; company guided $3.65–$3.70)")
        print(f"  EPP          : ${EPP:.2f}  ({EPP_MIN_PE}× × ${EPS_NOW:.2f})")
        print()
        print(f"  Current price ${CURRENT_PRICE:.2f} is +{epp_gap_pct:.1f}% ABOVE EPP floor ${EPP:.2f}")
        print()
        print("  The EPP floor at $146.80 aligns remarkably well with the Feb 2024")
        print(f"  post-shock low of $135 (40× $3.00 forward EPS at the time).  This")
        print("  validates 40× as the structural floor multiple.  A return to EPP from")
        print(f"  current levels would require a -{(CURRENT_PRICE-EPP)/CURRENT_PRICE*100:.1f}% drawdown — feasible in a")
        print("  prolonged risk-off period or a significant earnings disappointment.")

        # ── C. METHOD B ──────────────────────────────────────────────────────
        print()
        print("  C. METHOD B — 2-YEAR EARNINGS POWER TARGET")
        print(f"  {dash}")
        print()
        print(f"  Consensus EPS (FY2028E) : ${CONS_EPS_2YR:.2f}  (40% adj FCF margin on ~$15B revenue)")
        print(f"  Exit P/E                : {CONS_EXIT_PE}×  (generous; maturation from today's 71× fwd)")
        print(f"  Method B target         : ${price_b:.2f}  ({CONS_EXIT_PE}× × ${CONS_EPS_2YR:.2f})")
        print(f"  Current price           : ${CURRENT_PRICE:.2f}")
        print(f"  Implied upside          : +{(price_b - CURRENT_PRICE)/CURRENT_PRICE*100:.1f}%")
        print()
        print(f"  Ratio B = ({CURRENT_PRICE:.2f} − {EPP:.2f}) / ({price_b:.2f} − {CURRENT_PRICE:.2f})")
        print(f"          = {CURRENT_PRICE - EPP:.2f} / {price_b - CURRENT_PRICE:.2f}")
        print(f"          = {ratio_b_fmt}")
        print()
        print("  ┌─────────────────────────────────────────────────────────────────┐")
        print(f"  │  FY2028E $7.00 × 40× = $280 — only +7.7% upside from $260      │")
        print(f"  │  You need 50× exit P/E ($350) just to get to WATCHLIST          │")
        print(f"  │  Signal: {signal_str:<55} │")
        print("  └─────────────────────────────────────────────────────────────────┘")
        print()
        print("  SENSITIVITY — signal at different exit P/E assumptions (FY2028E $7.00):")
        print()
        print(f"  {'Exit P/E':>8}  {'Method B':>10}  {'Upside':>8}  {'Ratio B':>10}  {'Signal':<18}")
        print(f"  {'-'*8}  {'-'*10}  {'-'*8}  {'-'*10}  {'-'*18}")
        for pe_test in [32, 35, 38, 40, 43, 46, 50, 55, 60]:
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
        print("  KEY INSIGHT: Even 50× FY2028E gives only WATCHLIST (ratio_b 1.73×).")
        print("  ACCUMULATE requires 58-60× exit P/E — above PANW's mid-cycle historical")
        print("  average and implying the stock never de-rates. This is the challenge")
        print("  with buying any company at 70× fwd earnings near an all-time high.")

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
        print("  E. EARNINGS TRAJECTORY (non-GAAP diluted EPS; post 2-for-1 split Dec 2024)")
        print(f"  {dash}")
        print()
        print("  FY2022   ~$1.38  (post-split; growing from early-stage profitability)")
        print("  FY2023   ~$2.22  (post-split; +61% YoY; SASE/CNAPP scaling)")
        print("  FY2024    $2.84  ◀ TROUGH REFERENCE (post-split; platformization shock Feb 2024)")
        print("  FY2025    $3.34  (+18% YoY despite billings headwinds; margins held)")
        print("  FY2026E   $3.67  (company guided $3.65–$3.70; Q1 $0.93 + Q2 $1.03 actuals)")
        print("  FY2027E  ~$5.00  (22% revenue growth + operating leverage; M&A integrated)")
        print("  FY2028E  ~$7.00  (40% FCF margin target; Rule of 60; ~$16B revenue)")
        print()
        print("  NOTE: EPS growth FY2025→FY2026E only +10% despite 22-23% revenue growth.")
        print("  This is the key near-term challenge: margin expansion is being consumed by")
        print("  M&A integration (IBM QRadar +$340M lower-margin revenue in Q3), SBC,")
        print("  and platformization discounts.  The FCF payoff is FY2027-2028, not today.")
        print()
        print("  FY2026 KEY METRICS (full year guidance / actuals):")
        print(f"  {'Metric':<38}  {'Value':>20}  {'YoY':>8}")
        print(f"  {'-'*38}  {'-'*20}  {'-'*8}")
        metrics = [
            ("Revenue (FY2026E)",                  "$11.28–11.31B",    "+22–23%"),
            ("Non-GAAP EPS (FY2026E guided)",       "$3.65–3.70",       "+10%"),
            ("NGS ARR (FY2026E guided)",             "$8.52–8.62B",      "+53–54%"),
            ("Remaining Performance Obligation",     "$20.2–20.3B",      "+28%"),
            ("Adj FCF margin (FY2026 target)",       "~37%",             "stable"),
            ("Q3 FY2026 EPS guidance",               "$0.78–0.80",       "28–29% rev"),
            ("Q3 FY2026 revenue guidance",           "$2.941–2.945B",    "+28–29%"),
            ("Platform customers (Q2 FY2026)",       "~1,550",           "+110 net new"),
            ("Platform customer NRR",                "~119%",            "steady"),
        ]
        for m, v, yoy in metrics:
            print(f"  {m:<38}  {v:>20}  {yoy:>8}")

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
        print("  NEAR-TERM CATALYST / RISK (IMMEDIATE — June 2, 2026):")
        print("    ⚠ Q3 FY2026 earnings in 9 days.  PANW is at ALL-TIME HIGH heading in.")
        print("    · BULL: Q3 beat + raise; NGS ARR accelerates; platformization record wins")
        print("    · BEAR: Revenue or ARR at-or-below high end; stock -15 to -25% correction")
        print("    · ASYMMETRIC: Upside capped (already priced in); downside uncapped on miss")
        print()
        print("  MEDIUM-TERM CATALYSTS (6–18 months):")
        print("    · IBM QRadar integration complete — SIEM displacement accelerates XSIAM")
        print("    · Rule of 60 / 40% FCF margin achievement in FY2027 (ahead of FY2028 target)")
        print("    · NGS ARR exceeding $10B milestone — validates $20B by FY2030 target")
        print("    · Platform customer count reaching 2,000 (from current ~1,550)")
        print()
        print("  MEDIUM-TERM RISKS:")
        print("    · CrowdStrike recovery from Falcon outage driving competitive wins vs PANW")
        print("    · Microsoft Defender for Cloud gaining at Prisma's expense (bundled in E5)")
        print("    · Platformization discounts deeper than expected → ARR quality concern")
        print("    · Government cyber budget cuts (DOGE) hitting ~20% of PANW revenue")
        print("    · Multiple compression: 70× → 45× = -37% on unchanged EPS")

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
        print(f"  Current price       : ${CURRENT_PRICE:.2f}  (ATH $261.41 May 22; Q3 earnings June 2 = event risk)")
        print(f"  EPP floor           : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above; {EPP_MIN_PE}× × ${EPS_NOW:.2f} FY2026E)")
        print(f"  Method B target     : ${price_b:.2f}  (+{(price_b-CURRENT_PRICE)/CURRENT_PRICE*100:.1f}%; FY2028E ${CONS_EPS_2YR:.0f} × {CONS_EXIT_PE}×)")
        print(f"  BEAR scenario       : $80  ({(80-CURRENT_PRICE)/CURRENT_PRICE*100:.1f}%; M&A drag + cyber spend cut + derating)")
        print(f"  Ratio B             : {ratio_b_fmt}  -> {signal_str}")
        print(f"  Forward P/E (FY26E) : {CURRENT_PRICE/EPS_NOW:.1f}×  ({CURRENT_PRICE:.0f} / ${EPS_NOW:.2f}; near-cycle peak multiple)")
        print(f"  FY2027E P/E         : {CURRENT_PRICE/5.00:.1f}×  (FY2027E ~$5.00; still elevated)")
        print(f"  FY2028E P/E         : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (FY2028E ${CONS_EPS_2YR}; approaching rational)")
        print(f"  Market cap          : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M shares × ${CURRENT_PRICE:.2f})")
        print(f"  Revenue FY2026E     : $11.28–11.31B  (+22–23% YoY; incl. M&A)")
        print(f"  NGS ARR FY2026E     : $8.52–8.62B  (+53–54% YoY; PRIMARY metric)")
        print(f"  RPO FY2026E         : $20.2–20.3B  (+28% YoY; 1.8× annual revenue = strong backlog)")
        print(f"  Rule of 40 (Q2 26)  : NGS ARR +33% + adj op margin ~33% ≈ 66% (excellent)")
        print(f"  Platform customers  : ~1,550  (+110 net new Q2; 119% NRR; sticky annuity)")
        print(f"  Adj FCF target FY28 : 40% margin  (~$6.4B FCF at $16B rev = $7.82/share)")
        print(f"  2-for-1 split       : Completed December 2024; share count doubled")
        print(f"  Div / buyback       : No dividend; periodic buybacks (~$1–2B/yr)")
        print(f"  AVOID thesis breaks : Q3 miss June 2 → -20% to $208 (40× FY2026E)")
        print(f"  WATCHLIST entry     : ~$185–195 (ratio_b ~1.3–1.6×; 50–53× FY2026E)")
        print(f"  ACCUMULATE entry    : ~$165 (ratio_b ~1.0×; 45× FY2026E; near-EPP)")

        # ── I. IDIOSYNCRATIC vs MACRO ────────────────────────────────────────
        print()
        print("  I. IDIOSYNCRATIC vs MACRO DRIVERS")
        print(f"  {dash}")
        print(f"  Beta: 1.25×  |  Idiosyncratic: 70%  |  Macro: 30%")
        print()
        drivers = [
            ("NGS ARR growth (quarterly; primary forward indicator)",   "IDIO", "35%", "TARGET: sustain 30%+ even ex-M&A; Q3 June 2 critical"),
            ("Platform customer adds + NRR trajectory",                 "IDIO", "20%", "110/qtr net adds; NRR must stay 115%+; erosion = SELL"),
            ("Cortex XSIAM competitive win rate vs CrowdStrike",        "IDIO", "15%", ">60% win rate claimed; any decel = bull thesis challenged"),
            ("Enterprise IT spend cycle (macro sentiment)",             "MACRO","20%", "Security = non-discretionary but can be deferred; PMI watch"),
            ("Government cyber budget (DOGE / NDAA allocations)",      "MACRO","10%", "~20% revenue; DOGE risk real but AI security expanding"),
        ]
        print(f"  {'Driver':<55}  {'Type':>5}  {'Wt':>4}  {'Note'}")
        print(f"  {'─'*55}  {'─'*5}  {'─'*4}  {'─'*40}")
        for d, t, w, n in drivers:
            print(f"  {d:<55}  {t:>5}  {w:>4}  {n}")

        print()
        print(sep)
        print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-24")
        print(sep)

    return out.getvalue()


if __name__ == "__main__":
    print(run_report())
