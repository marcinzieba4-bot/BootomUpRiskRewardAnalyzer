#!/usr/bin/env python3
"""
txn_signal_model.py  —  Texas Instruments Incorporated (NASDAQ: TXN)
Bottom-Up Risk/Reward Signal Model
All prices and EPS in USD.
"""

import math, sys, io, contextlib

TICKER        = "TXN"
COMPANY       = "Texas Instruments Incorporated"
EXCHANGE      = "NASDAQ"
FY_END        = "December 31 (calendar year)"
SHARES_M      = 912.0           # million diluted shares (~$281B mkt cap / $308.65)

CURRENT_PRICE = 308.65          # TXN — fetched from web search, 2026-05-24
                                 # May 22: $312.21; May 23 range: $300.64–$315.57; ATH: $315.57
                                 # Stock up ~58% YTD driven by AI/data center analog re-rating

# ── EPP FLOOR ──────────────────────────────────────────────────────────────
EPS_TROUGH        = 5.20        # FY2024; cycle trough (inventory destocking + peak capex D&A)
                                 # TI GAAP diluted EPS; FY2022 $9.41 → FY2023 $7.07 → FY2024 $5.20
EPS_TROUGH_PRICE  = 152.73      # 52-wk low (2025); trough reflects peak capex concern + cycle fear
EPP_MIN_PE        = 18          # structural floor for a franchise analog semi with 300mm moat;
                                 # TI historical trough P/E ~18-20x; 18x reflects capex headwind discount
EPS_FY2025        = 5.50        # FY2025 full-year GAAP diluted (Q1 $1.28 + Q2 $1.41 + Q3 $1.48 + Q4 $1.27)
EPS_NOW           = 7.75        # FY2026E conservative; Q1 actual $1.68 (+31% YoY, beat $1.37 est);
                                 # Q2 guided $1.77–$2.05 (midpoint $1.91); H2 recovery = ~$7.50–8.00;
                                 # using conservative $7.75 vs sell-side $8.00+ consensus
EPP               = round(EPS_NOW * EPP_MIN_PE, 2)    # $139.50

epp_gap_pct       = round((CURRENT_PRICE - EPP) / EPP * 100, 1)    # +121.3%
below_floor       = CURRENT_PRICE < EPP                              # False

# ── METHOD B ───────────────────────────────────────────────────────────────
CONS_EPS_2YR  = 13.00           # FY2028E; 2-yr horizon from May 2026; capex normalization inflection;
                                 # FY2026 capex guided $2–5B (vs $5B FY2025); SM1 Sherman began Dec 2025;
                                 # capex cycle ~83% complete → D&A starts rolling off → EPS/FCF ramp
                                 # consensus FY2027E ~$9.00, FY2028E ~$11–13; using $13 = bull-leaning base
CONS_EXIT_PE  = 24              # mid-cycle for high-quality analog franchise with 300mm cost moat;
                                 # historical TI mid-cycle 20–28x; 24x = generous but below current 40x fwd
price_b       = round(CONS_EPS_2YR * CONS_EXIT_PE, 2)    # $312.00
ratio_b_raw   = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE) if price_b > CURRENT_PRICE else None
ratio_b       = round(ratio_b_raw, 2) if ratio_b_raw is not None else None  # 50.49x → AVOID

# ── SOFTMAX ENGINE ─────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  {"price": 85.0,   "eps":  5.0,  "pe": 17.0,
              "desc": "Semiconductor cycle downturn; capex normalisation delayed; AI analog demand fades; EPS reverts to trough"},
    "BASE":  {"price": 312.0,  "eps": 13.0,  "pe": 24.0,
              "desc": "FY2028E $13 × 24x; 300mm cost benefits materialise; industrial + auto recovery; AI analog sustains"},
    "BULL":  {"price": 420.0,  "eps": 16.0,  "pe": 26.0,
              "desc": "Capex fully normalised FY2027; FCF/share $15+; data center analog upside; margin expansion above guidance"},
    "XBULL": {"price": 600.0,  "eps": 20.0,  "pe": 30.0,
              "desc": "TI 300mm advantage drives 60%+ gross margins; $24B revenue × 30% op margin; FCF machine; Buffett-level compounder"},
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
    {"name": "300mm analog fab transition — unique structural cost moat",
     "rating": +0.9, "weight": 0.30,
     "desc": ("Texas Instruments is the ONLY large analog semiconductor company making the "
              "200mm → 300mm wafer transition at scale. 300mm wafers produce 2× the chips of "
              "200mm at ~40% lower cost per die. No analog competitor — not Analog Devices, "
              "not ON Semi, not STMicro — has this structural cost advantage at scale. "
              "SM1 (Sherman, TX) began production December 17, 2025. The capex cycle is ~83% "
              "complete as of late 2025; FY2026 capex guided $2–5B vs $5B in FY2025 — the "
              "normalisation has begun. When fully ramped, TI's gross margins could reach "
              "60%+ (vs ~55% today), creating a cost wall competitors cannot breach.")},
    {"name": "Analog franchise depth (80K+ products, 10-15yr design-in cycles)",
     "rating": +0.7, "weight": 0.20,
     "desc": ("TI has >80,000 analog and embedded products. Once a TI chip is designed into "
              "an industrial robot, automotive ECU, or medical device, it stays for the life "
              "of the platform (10–15 years). This creates an annuity-like revenue stream that "
              "is nearly impossible to displace mid-cycle. With 100,000+ customers and no "
              "single customer >10% of revenue, the franchise is both deep and diversified. "
              "TI's direct sales model (vs distributor-heavy peers) gives pricing power and "
              "customer intimacy that drives sticky design wins.")},
    {"name": "Data center / AI analog uplift (DC revenue +90% YoY Q1 2026)",
     "rating": +0.5, "weight": 0.10,
     "desc": ("AI server racks require massive amounts of analog content — power management ICs, "
              "signal isolation, interface chips, temperature sensors, clock/timing. Every NVIDIA "
              "H100/H200/B200 GPU cluster runs hundreds of TI power and signal chain chips. "
              "Q1 2026 data center revenue grew +90% YoY. While TI doesn't break out exact "
              "percentages, data center is now a material and fast-growing segment. This is "
              "incremental to TI's traditional industrial/automotive base — it adds TAM without "
              "cannibalising existing revenue streams.")},
    {"name": "AI re-rating multiple risk — 40x fwd vs 20–28x historical",
     "rating": -0.8, "weight": 0.20,
     "desc": ("At $308.65 / $7.75 FY2026E EPS = 39.8x forward P/E. TI's historical mid-cycle "
              "P/E is 20–28x. The AI/data center narrative has re-rated TI to a growth multiple "
              "it has never sustained over a full cycle. When/if AI capex spend moderates, or if "
              "data center analog growth decelerates from 90% to 30%, the multiple could compress "
              "back to 22–26x — implying meaningful downside even with EPS recovery. The average "
              "analyst price target is ~$284 — BELOW the current $308 price — consistent with "
              "the view that the stock has overshot consensus fair value.")},
    {"name": "Capex normalisation timing uncertainty (FY2026 guided $2–5B — wide range)",
     "rating": -0.6, "weight": 0.20,
     "desc": ("TI's FY2026 capex guidance is unusually wide: $2–5B. The lower end ($2B) implies "
              "capex has already collapsed, accelerating EPS/FCF recovery. The upper end ($5B) "
              "means another year of suppressed earnings. The timing of the 300mm ramp benefit "
              "showing in margins is unclear — SM1 Sherman production began Dec 2025, but "
              "ramping a fab to full utilisation takes 18–36 months. If the cycle turns down "
              "before full utilisation, TI will have built massive capacity into a trough, "
              "compounding both capex drag and pricing pressure simultaneously.")},
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
    if ratio_b is not None and ratio_b > 10:
        ratio_b_fmt = f"{ratio_b:.1f}x"

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        W = 72
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
        print(f"  Sector   : Analog Semiconductors · Embedded Processors · Industrial / Auto / AI")
        print(f"  FY end   : {FY_END}")
        print(f"  EPS basis: GAAP diluted (TI does not provide formal non-GAAP EPS reconciliation)")
        print(f"  Shares   : ~{SHARES_M:.0f}M (estimated from market cap)")
        print(f"  Price    : ${CURRENT_PRICE:.2f}  [2026-05-24; near ATH $315.57; +58% YTD]")
        print(f"  52-week  : $152.73 low – $315.57 high  (AI/data center re-rating drove 2x from trough)")

        print()
        print(sep)
        print(f"  PART 2 — ANALYST COMMENTARY  |  {TICKER}")
        print(sep)

        # ── A. INVESTMENT THESIS ─────────────────────────────────────────────
        print()
        print("  A. INVESTMENT THESIS")
        print(f"  {dash}")
        print()
        print("  Texas Instruments is the world's pre-eminent analog semiconductor company.")
        print("  It makes the unglamorous but irreplaceable chips that power every industrial")
        print("  machine, every automobile, every data centre rack, and every consumer device")
        print("  on the planet.  Power management ICs, operational amplifiers, data converters,")
        print("  signal isolators, microcontrollers, motor drivers — TI makes all of them,")
        print("  across 80,000+ products, serving 100,000+ customers in 100+ countries.")
        print()
        print("  The core investment debate is NOT about the quality of the franchise.")
        print("  Almost no one disputes that TI is a world-class business.  The debate is")
        print("  entirely about PRICE.")
        print()
        print("  THE BULL CASE — THE 300MM CAPEX PAYOFF:")
        print()
        print("  From 2018 to 2026, TI committed ~$30B of capital to building 300mm wafer")
        print("  fabrication plants — a scale that dwarfs every analog competitor.  300mm")
        print("  wafers produce 2× the chips of legacy 200mm wafers at ~40% lower cost per die.")
        print("  No competitor — not Analog Devices, not ON Semi, not STMicro — can match this.")
        print("  The key fabs:")
        print()
        print("    · LFAB (Lehi, UT) — acquired from Micron 2021; 300mm; ramping")
        print("    · SM1 (Sherman, TX) — greenfield; 300mm; BEGAN PRODUCTION Dec 17, 2025")
        print("    · SM2/SM3/SM4 — planned on same Sherman mega-site (long-term)")
        print()
        print("  The capex cycle is ~83% complete as of late 2025.  FY2026 capex is guided")
        print("  at $2–5B (vs $5B in FY2025).  When capex normalises from ~$5B to ~$2B/yr,")
        print("  free cash flow per share could reach $15–20 — more than 2× EPS, because")
        print("  depreciation/amortisation front-loads the income statement pain.")
        print()
        print("  The ADDITIONAL re-rating driver is AI analog demand:")
        print()
        print("    · Every AI server rack needs hundreds of TI power management, signal chain,")
        print("      and interface chips.  Data centre revenue grew +90% YoY in Q1 2026.")
        print("    · AI phone ASP uplift; industrial automation; automotive ADAS proliferation.")
        print("    · TI's chips are in the BOM of every major AI infrastructure build.")
        print()
        print("  THE BEAR CASE — FULLY PRICED, NO MARGIN OF SAFETY:")
        print()
        print("  At $308.65, TI trades at 39.8x FY2026E GAAP EPS ($7.75).  Historical mid-")
        print("  cycle P/E is 20–28x.  The market is paying a structurally elevated multiple")
        print("  for a recovery story that plays out in FY2028–2030, not today.  In effect,")
        print("  investors are pre-buying the 300mm payoff at full price — with no discount")
        print("  for timing risk, execution risk, or cycle risk.")
        print()
        print("  Method B (our 2-year EPS consensus target): FY2028E $13 × 24x = $312.")
        print("  That is only +$3 above today's price — meaning if you bought at $308.65,")
        print("  your 2-year return in the BASE case is essentially zero.")
        print()
        print("  Even more telling: the average Wall Street price target is ~$284 — BELOW")
        print("  the current price.  The sell-side, which tends to be optimistic, is saying")
        print("  TXN is overvalued here.")
        print()
        print(f"  Signal: {signal_str}  |  Ratio B: {ratio_b_fmt}  |  EPP gap: +{epp_gap_pct:.1f}%")
        print(f"  Method B $312 is only +1.1% above current price — essentially zero upside in BASE case")
        print(f"  Re-evaluate below $210 (ratio_b ~3-5x); BUY territory at ~$155 (ratio_b ~0.75x)")

        # ── B. EPP FLOOR ─────────────────────────────────────────────────────
        print()
        print("  B. EARNINGS POWER PRICE (EPP) — STRUCTURAL FLOOR")
        print(f"  {dash}")
        print()
        print(f"  EPS anchor   : ${EPS_TROUGH:.2f}  (FY2024; cycle trough from inventory destocking")
        print(f"                  + peak capex D&A suppression; TI's worst EPS since pre-2016)")
        print(f"  Trough price : ${EPS_TROUGH_PRICE:.2f}  (52-week low; market pricing maximum capex fear)")
        print(f"  EPP min P/E  : {EPP_MIN_PE}×  (franchise floor; TI rarely trades below 18x even at trough)")
        print(f"  EPS now      : ${EPS_NOW:.2f}  (FY2026E; Q1 actual $1.68 + Q2 guided mid $1.91 + H2)")
        print(f"  EPP          : ${EPP:.2f}  ({EPP_MIN_PE}× × ${EPS_NOW:.2f})")
        print()
        print(f"  Current price ${CURRENT_PRICE:.2f} is +{epp_gap_pct:.1f}% ABOVE EPP floor ${EPP:.2f}")
        print()
        print("  The EPP floor is well below current price — TI is not at risk of trading")
        print("  below structural support.  The issue is the OPPOSITE: the stock is so far")
        print("  above its EPP that there is no downside cushion from here at this price.")
        print("  If the multiple reverts from 40x to 22x on FY2026E EPS, the stock trades")
        print(f"  at ${EPS_NOW * 22:.0f} — a {(EPS_NOW * 22 - CURRENT_PRICE)/CURRENT_PRICE*100:.1f}% drawdown from current levels.")

        # ── C. METHOD B ──────────────────────────────────────────────────────
        print()
        print("  C. METHOD B — 2-YEAR EARNINGS POWER TARGET")
        print(f"  {dash}")
        print()
        print(f"  Consensus EPS (FY2028E) : ${CONS_EPS_2YR:.2f}")
        print(f"  Exit P/E                : {CONS_EXIT_PE}×  (mid-cycle; generous vs 20-28x hist; reflects 300mm moat)")
        print(f"  Method B target         : ${price_b:.2f}  ({CONS_EXIT_PE}× × ${CONS_EPS_2YR:.2f})")
        print(f"  Current price           : ${CURRENT_PRICE:.2f}")
        print(f"  Implied upside          : +{(price_b - CURRENT_PRICE)/CURRENT_PRICE*100:.1f}%")
        print()
        print(f"  Ratio B = ({CURRENT_PRICE:.2f} − {EPP:.2f}) / ({price_b:.2f} − {CURRENT_PRICE:.2f})")
        print(f"          = {CURRENT_PRICE - EPP:.2f} / {price_b - CURRENT_PRICE:.2f}")
        print(f"          = {ratio_b_fmt}")
        print()
        print("  ┌─────────────────────────────────────────────────────────────────┐")
        print(f"  │  METHOD B target ${price_b:.2f} is only +1.1% above current ${CURRENT_PRICE:.2f}   │")
        print(f"  │  Even in the BASE recovery case, TXN offers near-ZERO upside   │")
        print(f"  │  Signal: {signal_str:<55} │")
        print("  └─────────────────────────────────────────────────────────────────┘")
        print()
        print("  SENSITIVITY — how signal changes at different exit P/E assumptions:")
        print()
        print(f"  {'Exit P/E':>8}  {'Method B':>10}  {'Upside':>8}  {'Ratio B':>10}  {'Signal':<18}")
        print(f"  {'-'*8}  {'-'*10}  {'-'*8}  {'-'*10}  {'-'*18}")
        for pe_test in [20, 22, 24, 26, 28, 30, 35]:
            pb_test = CONS_EPS_2YR * pe_test
            if pb_test <= CURRENT_PRICE:
                rb_test_fmt = "N/A"
                sig_test    = "✕ AVOID"
            else:
                rb_test = (CURRENT_PRICE - EPP) / (pb_test - CURRENT_PRICE)
                rb_test_fmt = f"{rb_test:.1f}x"
                sig_test = ratio_b_signal(rb_test)
            upside_test = (pb_test - CURRENT_PRICE) / CURRENT_PRICE * 100
            print(f"  {pe_test:>8}×  ${pb_test:>9.0f}  {upside_test:>+7.1f}%  {rb_test_fmt:>10}  {sig_test:<18}")
        print()
        print("  KEY INSIGHT: You need to believe in 35× exit P/E (above historical range)")
        print(f"  AND $13 FY2028E EPS just to get Ratio B into AVOID territory (3.0x).")
        print(f"  At a fair mid-cycle 22x, the 2-year target is ${CONS_EPS_2YR * 22:.0f} — BELOW current price.")

        # ── D. SOFTMAX SCENARIO ENGINE ───────────────────────────────────────
        print()
        print("  D. SCENARIO ENGINE & MARKET COMPOSITE")
        print(f"  {dash}")
        print()
        print(f"  {'Scenario':<8}  {'Price':>7}  {'EPS':>6}  {'P/E':>5}  {'Mkt%':>6}  {'Adj%':>6}  Description")
        print(f"  {'-'*8}  {'-'*7}  {'-'*6}  {'-'*5}  {'-'*6}  {'-'*6}  {'-'*42}")
        for k, s in SCENARIOS.items():
            mp = mkt_probs[k] * 100
            ap = adj_probs[k] * 100
            print(f"  {k:<8}  ${s['price']:>6.0f}  ${s['eps']:>5.1f}  {s['pe']:>4.0f}×  {mp:>5.1f}%  {ap:>5.1f}%  {s['desc'][:42]}")
        print()
        print(f"  Market composite   : {market_composite:.3f}  (inferred from current price ${CURRENT_PRICE:.2f})")
        print(f"  SCA adjustment     : {sca_adj:+.3f}  (structural factors; see section F)")
        print(f"  Adjusted composite : {adj_composite:.3f}")
        print()
        print("  Composite interpretation:")
        print("  1.0–1.5 = deep value / distress  |  1.5–2.0 = value  |  2.0–2.5 = fair")
        print("  2.5–3.0 = richly valued  |  3.0–3.5 = expensive  |  3.5–4.0 = bubble")
        print(f"  → {adj_composite:.2f} = {'richly valued / expensive; market pricing BASE→BULL transition' if adj_composite < 3.0 else 'expensive; material BULL scenario probability priced in'}")

        # ── E. EARNINGS TRAJECTORY ───────────────────────────────────────────
        print()
        print("  E. EARNINGS TRAJECTORY & RECOVERY ROADMAP")
        print(f"  {dash}")
        print()
        print("  FY2020    $6.43   (pre-cycle; modest analog recovery post-COVID)")
        print("  FY2021    $8.26   (demand surge; semi shortage; pricing power peak)")
        print("  FY2022    $9.41   ◀ PEAK EPS  (inventory build; multi-year cycle top)")
        print("  FY2023    $7.07   (inventory correction begins; industrial/personal elec weak)")
        print("  FY2024    $5.20   ◀ TROUGH EPS  (peak capex D&A + deepest inventory trough)")
        print("  FY2025    $5.50   (early recovery; Q4 $1.27 showed sequential improvement)")
        print("  FY2026E   $7.75   (Q1 $1.68 actual; Q2 $1.77–2.05 guided; H2 ramp)")
        print("  FY2027E   $9.00   (300mm cost curve kicking in; capex normalising)")
        print("  FY2028E  $13.00   (capex fully normalised; 300mm scale producing; FCF explosion)")
        print()
        print("  CAPEX CYCLE STATUS (the key thesis variable):")
        print("  ─────────────────────────────────────────────")
        print("  Total capex commitment (2018–2026E):  ~$30B")
        print("  Cycle completion (late 2025 estimate):  ~83%")
        print("  FY2025 actual capex:  ~$5.0B")
        print("  FY2026 guided capex:  $2.0–5.0B  (WIDE range = key uncertainty)")
        print("  FY2027+ normalised capex estimate:  ~$2B/yr")
        print()
        print("  FABS IN THE 300mm PROGRAMME:")
        print("  · LFAB (Lehi, UT)    — acquired from Micron 2021; 300mm; production ramping")
        print("  · SM1 (Sherman, TX)  — BEGAN PRODUCTION December 17, 2025")
        print("  · SM2/3/4 (Sherman)  — planned; timeline dependent on market demand")
        print()
        print("  When capex drops from $5B to $2B, that frees ~$3B/yr in cash flow.")
        print("  At 912M shares, that's ~$3.29 incremental FCF/share annually.")
        print("  GAAP EPS will lag FCF recovery as D&A is amortised over 20–30 years,")
        print("  but free cash flow is TI's primary shareholder return metric.")

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
        print("    · Q2 2026 earnings (July 2026) — key read on SM1 Sherman ramp cadence")
        print("    · FY2026 capex actualisation — lower end ($2B) vs upper ($5B) is decisive")
        print("    · Industrial order recovery — inventory replenishment cycle confirmation")
        print("    · Data centre revenue sustaining post-Q1 +90% baseline (Q2 print crucial)")
        print()
        print("  MEDIUM-TERM CATALYSTS (1–3 years):")
        print("    · 300mm gross margin expansion — first visible in FY2027 gross margin")
        print("    · FCF per share reaching $12–15 (triggers shareholder return expansion)")
        print("    · SM2 ground-breaking announcement (market demand-gated)")
        print("    · Automotive ADAS proliferation — TI chipset wins in next-gen platforms")
        print()
        print("  KEY RISKS:")
        print("    · Multiple compression from 40x → 22x on EPS recovery = -45% drawdown")
        print("    · Semiconductor cycle downturn before 300mm ramp delivers FCF benefit")
        print("    · AI data centre capex cycle pause — hyperscalers slow orders (key risk 2025–2026)")
        print("    · Industrial softness persistent beyond inventory correction")
        print("    · Competition: ADI + ON Semi accelerating 300mm capacity (later but real)")
        print("    · China market risk: ~20–25% of TI revenue; any BIS restriction = severe")

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
        print(f"  Current price       : ${CURRENT_PRICE:.2f}  (+58% YTD; AI/data center analog re-rating)")
        print(f"  EPP floor           : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above floor; {EPP_MIN_PE}× × ${EPS_NOW:.2f} FY2026E)")
        print(f"  Method B target     : ${price_b:.2f}  (upside: +{(price_b-CURRENT_PRICE)/CURRENT_PRICE*100:.1f}%; FY2028E ${CONS_EPS_2YR:.0f} × {CONS_EXIT_PE}×)")
        print(f"  BEAR scenario       : $85  (downside: {(85-CURRENT_PRICE)/CURRENT_PRICE*100:.1f}%; cycle downturn + capex delay)")
        print(f"  Ratio B             : {ratio_b_fmt}  -> {signal_str}")
        print(f"  Forward P/E (FY26E) : {CURRENT_PRICE/EPS_NOW:.1f}×  (vs 20–28× historical mid-cycle; 2× historical norm)")
        print(f"  FY2027E P/E         : {CURRENT_PRICE/9.0:.1f}×  (FY2027E $9.00; still elevated vs history)")
        print(f"  FY2028E P/E         : {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (FY2028E ${CONS_EPS_2YR:.0f}; approaching historical range)")
        print(f"  Historical PE range : 18–35×  (trough 18×; mid-cycle 22–28×; peak 32–35× AI-hype)")
        print(f"  Market cap          : ~${CURRENT_PRICE * SHARES_M / 1000:.0f}B  ({SHARES_M:.0f}M shares × ${CURRENT_PRICE:.2f})")
        print(f"  Dividend yield      : ~1.8%  ($5.44/share annual; 21+ consecutive years of growth)")
        print(f"  Dividend coverage   : EPS ${EPS_NOW:.2f}E / dividend $5.44 = {EPS_NOW/5.44:.1f}× covered (healthy)")
        print(f"  Q1 2026 results     : Revenue $4.83B (+19% YoY); EPS $1.68 (+31% YoY); beat $1.37 est")
        print(f"  Q1 segment detail   : Analog $3.80B (+22% YoY) | Embedded $0.97B (+10% YoY)")
        print(f"  Q1 channel          : Data centre +90% YoY; industrial recovering; auto steady")
        print(f"  Q2 2026 guidance    : Revenue $5.0–5.4B; EPS $1.77–$2.05 (vs $1.57 est = major beat)")
        print(f"  Capex cycle         : ~83% complete; SM1 Sherman production began Dec 17, 2025")
        print(f"  FY2026 capex guide  : $2–5B  (normalisation has begun; lower end = massive FCF catalyst)")
        print(f"  52-week range       : $152.73 – $315.57  (stock 2× from trough to near ATH)")
        print(f"  Analyst avg target  : ~$284  (BELOW current price; consensus is HOLD/SELL at these levels)")
        print(f"  AVOID thesis breaks : Multiple compression to 22× FY2026E = ${EPS_NOW * 22:.0f} (-{(CURRENT_PRICE - EPS_NOW*22)/CURRENT_PRICE*100:.0f}% drawdown)")
        print(f"  ADD trigger         : Pullback to $200–220 (ratio_b ~3–5×); BUY at ~$155 (ratio_b ~0.75×)")

        # ── I. IDIOSYNCRATIC vs MACRO ────────────────────────────────────────
        print()
        print("  I. IDIOSYNCRATIC vs MACRO DRIVERS")
        print(f"  {dash}")
        print(f"  Beta: 1.10×  |  Idiosyncratic: 55%  |  Macro: 45%")
        print()
        drivers = [
            ("300mm capex normalisation pace (FY2026 capex actual)",         "IDIO", "30%", "PRIMARY signal; $2B vs $5B makes ~$3.3/share FCF diff"),
            ("Industrial end-market recovery (TI's largest segment ~40%)",    "IDIO", "20%", "Inventory cycle confirms; sustained recovery = EPS upside"),
            ("Data centre analog demand sustainability (post-90% YoY Q1)",    "IDIO", "10%", "Bull case requires DC at +40-50%+ going forward, not 90%"),
            ("Semiconductor cycle / broad macro (GDP, manufacturing PMI)",    "MACRO","25%", "Analog has 4–6 wk lead time; PMI <50 = risk to near-term rev"),
            ("China export controls / geopolitical risk",                     "MACRO","15%", "~20–25% TI revenue from China; BIS action = material hit"),
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
