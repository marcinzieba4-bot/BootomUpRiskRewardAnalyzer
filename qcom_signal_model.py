#!/usr/bin/env python3
"""
qcom_signal_model.py  —  QUALCOMM Incorporated (NASDAQ: QCOM)
Bottom-Up Risk/Reward Signal Model
All prices and EPS in USD.
"""

import math, sys, io, contextlib

TICKER        = "QCOM"
COMPANY       = "QUALCOMM Incorporated"
EXCHANGE      = "NASDAQ"
FY_END        = "Late September (fiscal year; FY2026 ends ~Sep 27, 2026)"
SHARES_M      = 1059.0          # million shares (Q2 FY2026 10-Q; buybacks reducing count ~2%/yr)

CURRENT_PRICE = 238.16          # QCOM — fetched from web search, 2026-05-22/23
                                 # +11.6% surge May 22 on Q2 FY2026 beat; pre-Q2 was ~$214
                                 # 52-wk high: $247.90; 52-wk low: $121.99 (peak Apple modem fear)

# ── EPP FLOOR ──────────────────────────────────────────────────────────────
EPS_TROUGH        = 8.43        # FY2023 non-GAAP; smartphone inventory crash (-33% from FY2022)
                                 # worst post-2020 cycle; Apple still a customer at that point
EPS_TROUGH_PRICE  = 121.99      # 52-wk low (~late 2025 / early 2026); peak Apple modem loss fears;
                                 # $121.99 / $12.03 FY2025 EPS = 10.1x — absolute panic pricing
EPP_MIN_PE        = 14          # structural floor; below 2023 downturn observed ~12-15x range;
                                 # reflects: #1 non-Apple smartphone modem, automotive ADAS moat,
                                 # QTL royalty stream (royalties from every Android phone sold);
                                 # 14x = "deep semiconductor downturn" pricing, not "business ends"
EPS_FY2025        = 12.03       # FY2025 (ended Sep 28, 2025); non-GAAP EPS; near FY2022 $12.53 peak
EPS_NOW           = 9.40        # FY2026E; transition year; Apple modem ramp-down accelerates;
                                 # Q1 FY2026 ~$2.40E; Q2 actual $2.65; Q3 guided $2.10-$2.30;
                                 # Q4 ~$2.15E; total ~$9.40; aligns with analyst consensus ~$9.39
EPP               = round(EPS_NOW * EPP_MIN_PE, 2)    # $131.60

epp_gap_pct       = round((CURRENT_PRICE - EPP) / EPP * 100, 1)    # +80.9%

# ── METHOD B ───────────────────────────────────────────────────────────────
CONS_EPS_2YR  = 13.00           # FY2028E non-GAAP (~Sep 2028; ~28 months from analysis);
                                 # automotive ~$8B run rate + IoT/PC growth + ex-Apple handset stable;
                                 # above FY2022 peak $12.53; requires automotive CAGR ~25-30% FY2027-28
CONS_EXIT_PE  = 22              # mid-cycle semiconductor with diversification premium; below peak
                                 # QCOM multiples of 25-30x; above trough 12-14x; 22x reflects
                                 # automotive/IoT transition story without full BULL re-rating
price_b       = round(CONS_EPS_2YR * CONS_EXIT_PE, 2)    # $286.00
ratio_b       = round((CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE), 2)   # 2.23x → HOLD/TRIM

# ── SOFTMAX ENGINE ─────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  {"price":  80.0,  "eps":  5.0, "pe": 16.0,
              "desc": "Smartphone super-cycle collapses; auto delayed; QTL challenged; EPS falls to $5"},
    "BASE":  {"price": 286.0,  "eps": 13.0, "pe": 22.0,
              "desc": "FY2028E $13 × 22x; auto ramp delivers; ex-Apple modem stable; IoT grows 10%+"},
    "BULL":  {"price": 360.0,  "eps": 18.0, "pe": 20.0,
              "desc": "Automotive $9B+ + Snapdragon X PC wins + data center; EPS recovers to $18"},
    "XBULL": {"price": 460.0,  "eps": 23.0, "pe": 20.0,
              "desc": "QCOM = AI edge chip leader (phone + car + PC + IoT); $23+ EPS at 20x"},
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
    {"name": "Automotive ADAS dominance (>$5B annualised; +38-50% YoY trajectory)",
     "rating": +1.0, "weight": 0.30,
     "desc": ("Qualcomm's Snapdragon Ride platform has 80%+ share of ADAS and digital cockpit SoCs. "
              "Q2 FY2026 auto revenue reached a record $1.33B (+38% YoY), with annualised run rate "
              "exceeding $5B for the first time. Q3 FY2026 automotive guided to grow ~50% YoY. "
              "By FY2026 year-end, Qualcomm expects >$6B annualised rate. The design win pipeline "
              "covers 2026-2030 model years at BMW, Stellantis, GM, Renault-Nissan, Mercedes. "
              "Automotive is now 13% of QCT revenue and growing — the clearest structural "
              "growth engine replacing Apple modem revenue dollar-for-dollar by FY2028.")},
    {"name": "Snapdragon X / Windows-on-ARM PC + data center custom chips (emerging)",
     "rating": +0.7, "weight": 0.10,
     "desc": ("Snapdragon X Elite (4nm, ARM-native) launched in 2024-2025 Windows PCs from Dell, "
              "HP, Lenovo, Microsoft Surface. Performance benchmarks exceed Intel Core Ultra on "
              "multi-threaded and AI workloads. Q2 FY2026 earnings call confirmed a hyperscaler "
              "custom chip programme for data center inference, targeting December 2026 tape-out. "
              "If successful, this is a new TAM worth $2-5B revenue by FY2028. Early innings but "
              "the pipeline exists — a second diversification leg beyond automotive.")},
    {"name": "Apple modem structural headwind (iPhone modem exit FY2025-FY2027)",
     "rating": -0.8, "weight": 0.30,
     "desc": ("Apple began shipping its in-house C1 modem with iPhone 17 (Sep 2025). Qualcomm "
              "retains some Apple modem business in FY2026 (higher-end models/regions) but is on "
              "a structured exit path. The full Apple modem loss is ~$6-8B annual QCT revenue at "
              "~50% gross margins = ~$3-4B gross profit headwind = ~$2.50-3.00 EPS drag vs FY2025. "
              "This headwind is fully embedded in FY2026E $9.40 EPS vs FY2025 $12.03 ($2.63 decline). "
              "The KEY question: does automotive + IoT + PC/data center fill the Apple revenue gap "
              "by FY2028? The math works but execution risk is real.")},
    {"name": "QTL licensing royalty risk (ARM/RISC-V custom silicon challenges royalty model)",
     "rating": -0.4, "weight": 0.15,
     "desc": ("Qualcomm Technology Licensing (QTL) earns royalties on every smartphone sold globally "
              "(typically 3.25% of wholesale selling price). Q2 FY2026 QTL revenue was $1.4B with "
              "72% EBT margin — it's QCOM's highest-margin segment. The risk: as phones move to "
              "custom SoCs (Apple's own design, Chinese OEM chips), QTL royalty per phone may "
              "face pressure. Also, RISC-V threatens to displace ARM in IoT/embedded — reducing "
              "QCOM licensing leverage over time. QTL is currently stable but structurally at risk "
              "from the 10-year trend toward IP independence in China and in custom silicon.")},
    {"name": "Non-Apple handset growth + IoT AI (Samsung, Xiaomi AI phones; IoT +9% Q2)",
     "rating": +0.5, "weight": 0.15,
     "desc": ("Ex-Apple QCT revenues grew 18% in FY2025. Android flagship phones (Samsung Galaxy "
              "S26, Xiaomi 15, Oppo Find X) all use Snapdragon 8 Elite. AI-enhanced camera, voice, "
              "and on-device LLM inference (Llama on Snapdragon) creates ASP uplift of 15-20% vs "
              "prior generation. IoT segment grew 9% in Q2 FY2026 — industrial IoT, smart home, "
              "and mixed reality (Meta Quest 4 uses Snapdragon XR2+). The non-Apple handset "
              "franchise is solid; it's ~60% of QCT revenue and growing modestly with AI uplift.")},
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
    div_yield = 3.40 / CURRENT_PRICE * 100   # $3.40/share annual dividend
    fcf_est  = 10.0   # annual FCF estimate $B (~$9.40 EPS × 1.06B shares ≈ $9.96B NI)
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
                     1.75–2.5 HOLD | >2.5 AVOID

  Company  : {COMPANY}
  Exchange : {EXCHANGE}
  Sector   : Semiconductors · Smartphone Modems · Automotive ADAS · AI Edge
  FY end   : {FY_END}
  EPS basis: Non-GAAP (excludes SBC, amortisation, acquisition charges)
  Shares   : ~{SHARES_M:.0f}M (Q2 FY2026 10-Q; buybacks ~2%/yr reducing count)
  Price    : ${CURRENT_PRICE:.2f}  [2026-05-22/23; post-Q2 FY2026 +11.6% surge]
  52-week  : ${EPS_TROUGH_PRICE:.2f} low – $247.90 high  (52-wk low = peak Apple modem fears)
""")

    print("=" * 72)
    print(f"  PART 2 — ANALYST COMMENTARY  |  {TICKER}")
    print("=" * 72)
    print(f"""
  A. INVESTMENT THESIS
  ----------------------------------------------------------------------

  Qualcomm is undergoing the most consequential diversification in its
  history.  Founded as a semiconductor and licensing company for 3G/4G/5G
  modems, it dominated every smartphone made — until Apple started making
  its own.

  The Apple modem departure is the central bear thesis.  Apple shipped its
  in-house C1 modem with iPhone 17 (September 2025), putting Qualcomm on
  a structured exit path from ~$6-8B of annual QCT modem revenue.  This
  explains why FY2026E EPS is $9.40 — down 21.9% from FY2025's $12.03
  — even as the underlying business is otherwise healthy.

  The bull case is an automotive and edge-AI renaissance:

  1. AUTOMOTIVE (+38% Q2, +50% guided Q3; annualised >$5B rate):
     Qualcomm's Snapdragon Ride platform holds 80%+ of the automotive
     ADAS and digital cockpit SoC market.  BMW, Mercedes, Stellantis,
     GM, Renault-Nissan all have multi-year design wins locked in for
     2026-2030 model year vehicles.  The automotive pipeline is not
     dependent on quarter-to-quarter design wins — it is CONTRACTED.
     Annualised automotive revenue exceeded $5B for the first time in
     Q2 FY2026.  By FY2028, Qualcomm expects $8-10B automotive annually.

  2. AI PHONE UPLIFT (ex-Apple, Snapdragon 8 Elite):
     Samsung Galaxy S26, Xiaomi 15, OPPO, vivo — all use Snapdragon
     8 Elite for on-device AI inference.  Llama models running locally
     on Snapdragon enable AI photography, real-time translation, and
     voice assistance without cloud latency.  ASP uplift of ~15-20%
     vs prior-generation Snapdragon drives EPS even on flat handset units.

  3. PC / DATA CENTER CUSTOM CHIPS (emerging):
     Snapdragon X Elite is gaining traction in Windows AI PCs.
     More importantly, on the Q2 FY2026 call, Qualcomm confirmed a
     custom hyperscaler chip programme with tape-out planned December 2026.
     If successful, this is a 2028-2030 revenue catalyst worth $2-5B.

  The challenge: the +11.6% surge on May 22, 2026 (Q2 beat) pushed QCOM
  from WATCHLIST territory (~$214) into HOLD/TRIM at ${CURRENT_PRICE:.2f}.
  At 25.3x FY2026E EPS ($9.40 — a DECLINING year), the stock is not cheap.
  Method B at ${price_b:.0f} implies only +{(price_b/CURRENT_PRICE-1)*100:.0f}% upside.
  The automotive thesis is real, but the Apple exit math takes 2-3 years
  to fully bridge.  Add on dips; trim into strength.

  Signal: {sig}  |  Ratio B: {ratio_b:.2f}x  |  EPP gap: +{epp_gap_pct:.1f}%
  Prior to Q2 surge (~$214): Ratio B ~{(214-EPP)/(price_b-214):.2f}x → would have been ◐ WATCHLIST


  B. EARNINGS POWER PRICE (EPP) — STRUCTURAL FLOOR
  ----------------------------------------------------------------------

  EPS anchor   : ${EPS_TROUGH:.2f}  (FY2023; smartphone inventory crash; PC/IoT weak;
                  worst post-2020 year; Apple STILL a customer — so not even the
                  Apple-exit floor; represents normal cyclical trough for Qualcomm)
  Bear trough  : ${EPS_TROUGH_PRICE:.2f}  (52-wk low; peak Apple-modem-exit fear;
                  $121.99 / $12.03 FY2025 EPS = 10.1x — extreme panic pricing;
                  doubled since then as automotive ramp proof-points accumulated)
  EPP min PE   : {EPP_MIN_PE}x  (structural floor; below 2023 trough observed 12-15x;
                  reflects #1 non-Apple smartphone modem + QTL royalty stream +
                  80% automotive ADAS market share; 14x = deep downturn pricing)

  EPS now      : ${EPS_NOW:.2f}  (FY2026E; Apple modem transition year;
                  Q1 FY2026 est ~$2.40; Q2 actual $2.65; Q3 guided $2.10-$2.30;
                  Q4 est ~$2.15; analyst consensus ~$9.39; company doesn't provide
                  full-year guidance but quarterly trajectory is well-telegraphed)
  EPP floor    : ${EPS_NOW:.2f} × {EPP_MIN_PE}x = ${EPP:.2f}
  Current vs EPP: ${CURRENT_PRICE:.2f} vs ${EPP:.2f}  (+{epp_gap_pct:.1f}% above floor)

  EPP is rising: FY2028E EPS ~$13 × 14x = $182 floor — rising toward current price.
  This means QCOM's EPP floor is "migrating up" as automotive ramps.
  By FY2028, EPP floor may reach $182-190, reducing the gap to ~25%.


  C. METHOD B — 2-YEAR EARNINGS POWER TARGET
  ----------------------------------------------------------------------

  CONS_EPS_2YR : ${CONS_EPS_2YR:.2f}  (FY2028E; ~28 months from analysis;
                  automotive ~$8B run rate + IoT growth + non-Apple handsets stable;
                  above FY2022 peak $12.53; assumes automotive CAGR ~25% FY2027-28;
                  requires hyperscaler data center chip to be early revenue stage)
  CONS_EXIT_PE : {CONS_EXIT_PE}x  (mid-cycle with diversification premium; below 25-30x
                  QCOM historical peaks; above 12-14x trough; 22x = "recovering growth
                  semiconductor with automotive franchise" not "mature/cyclical chip")
  Method B     : ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x = ${price_b:.2f}

  Ratio B = (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})
           = ${CURRENT_PRICE-EPP:.2f} / ${price_b-CURRENT_PRICE:.2f}
           = {ratio_b:.2f}x  →  {sig}

  Sensitivity to exit PE (at CONS_EPS_2YR ${CONS_EPS_2YR:.2f}):
    CONS_EXIT_PE = 18x → Price_B $234 → BELOW current price → N/A (AVOID)
    CONS_EXIT_PE = 20x → Price_B $260 → Ratio B {(CURRENT_PRICE-EPP)/(260-CURRENT_PRICE):.1f}x  (AVOID)
    CONS_EXIT_PE = 22x → Price_B $286 → Ratio B {ratio_b:.2f}x  (HOLD/TRIM)  ← base case
    CONS_EXIT_PE = 25x → Price_B $325 → Ratio B {(CURRENT_PRICE-EPP)/(325-CURRENT_PRICE):.2f}x  (WATCHLIST)
    CONS_EXIT_PE = 28x → Price_B $364 → Ratio B {(CURRENT_PRICE-EPP)/(364-CURRENT_PRICE):.2f}x  (ACCUMULATE)
  Signal is HIGHLY SENSITIVE to exit multiple — reflecting genuine uncertainty
  whether automotive-driven Qualcomm re-rates to 25x+ or stays at 18-22x.
  PRE-SURGE price (~$214): Ratio B {(214-EPP)/(price_b-214):.2f}x → ◐ WATCHLIST (better risk/reward).


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
  BEAR at ${bear_p:.0f}: smartphone super-downturn (AI hype fades; units down 15%),
  Apple modem exit causes EPS to collapse to ~$5 (below FY2023 trough of $8.43),
  auto delays push delivery to FY2030+; QTL challenged by royalty litigation.
  The BEAR requires simultaneous failure of ALL diversification initiatives.
  XBULL ${xbull_p:.0f}: automotive $9B+, IoT $8B, hyperscaler chip $4B, AI phone
  royalty uplift = $23+ EPS at 20x. Not priced in even today.


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

  Interpretation: Market composite {mkt_composite:.2f} sits between BASE and BEAR,
  consistent with the stock having nearly doubled from $121.99 (panic low)
  but not yet pricing full auto-diversification success. SCA of {sca_adj:+.3f}
  (positive: auto dominance + PC/data center emerging outweigh Apple exit +
  QTL risk) pushes model composite to {model_composite:.2f} — near BASE centre.
  Model EV {sign_ev}{ev_chg:.0f}%: fair value at current levels. HOLD, not chase.


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


  G. EPS QUALITY DECOMP  (FY2025 ${EPS_FY2025:.2f} → FY2026E ${EPS_NOW:.2f} = −${EPS_FY2025 - EPS_NOW:.2f} = {(EPS_NOW/EPS_FY2025-1)*100:.1f}%)
  ----------------------------------------------------------------------
  NOTE: EPS DECLINING FY2025→FY2026 due to Apple modem exit. Components below
  show each contributor to the NET CHANGE (NEGATIVE = drag on EPS this year).
  Component                                                      Share          Type
  ---------------------------------------------------------------------------------
  Apple modem exit revenue loss (~$3-4B gross profit; FY2026    -120%   Temporal
    structural onset; iPhone 17/18 C1 modem replacing Qualcomm;
    $6-8B QCT revenue → 50% GM → $3-4B GP → ~$2.50-3.00 EPS drag
    at full exit; FY2026 is partial year; full hit in FY2027)
  Automotive gross profit contribution (+38% QCT auto YoY;        +55%   Structural
    $1.33B Q2; $5B+ annualised rate; 50%+ margin; replaces portion
    of Apple GP; ~$1.50 EPS contribution growing toward $3.00 by FY2028)
  IoT gross profit growth (+9% YoY; industrial AI, AR/VR, smart   +15%   Structural
    home, industrial edge; $1.7B quarterly = $6.8B annualised; mixed
    margins but growing volume; ~$0.40 EPS contribution this year)
  Non-Apple handset ASP uplift (Snapdragon 8 Elite AI phone        +25%   Structural
    premium; Samsung/Xiaomi/OPPO paying 15-20% more per flagship
    chip; 60% of QCT = largest segment; modest but real; ~$0.70/yr)
  QTL stability (royalties on global Android; $1.4B Q2; 72%        +15%   Structural
    EBT margin; flat YoY as global handset units flat but ASP rises;
    ~$0.40 royalty contribution per quarter; stable annuity stream)
  Operating leverage + share buybacks (QCOM reduces shares ~2%/yr  +10%   Structural
    via buybacks; ~$0.20/yr EPS accretion; plus some R&D leverage
    on auto/IoT platform vs having to build new from scratch)

  Structural :   +120%   (auto + IoT + handset ASP + QTL + buybacks)
  Temporal   :   -220%   (Apple modem exit dominant driver of EPS decline)
  Net         :   {(EPS_NOW/EPS_FY2025-1)*100:.1f}%  (EPS decline is APPLE EXIT, not business deterioration)

  KEY INSIGHT: The EPS DECLINE from $12.03 → $9.40 is 100% explained by the
  Apple modem departure — not by any deterioration in the underlying franchise.
  By FY2028, when automotive reaches $8-10B and the Apple headwind is fully
  absorbed, EPS is expected to EXCEED the FY2022 peak of $12.53.
""")

    print("=" * 72)
    print(f"  PART 3 — NUMBERS & SIGNALS   |  {TICKER}")
    print("=" * 72)
    print(f"""
  H. RISK / RETURN SUMMARY
  ----------------------------------------------------------------------

  Current price       : ${CURRENT_PRICE:.2f}  (+11.6% surge May 22; pre-Q2 was ~$214 → WATCHLIST)
  EPP floor           : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above floor; {EPP_MIN_PE}x × ${EPS_NOW:.2f} FY2026E)
  Method B target     : ${price_b:.2f}  (upside: +{(price_b/CURRENT_PRICE-1)*100:.0f}%; FY2028E ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x)
  BEAR scenario       : ${bear_p:.0f}  (downside: -{(1-bear_p/CURRENT_PRICE)*100:.0f}%; auto delayed + handset crash)
  Ratio B             : {ratio_b:.2f}x  -> {sig}
  Pre-surge ratio B   : ~{(214-EPP)/(price_b-214):.2f}x at ~$214  (would have been ◐ WATCHLIST)
  Forward P/E         : {CURRENT_PRICE/EPS_NOW:.1f}x  (FY2026E ${EPS_NOW:.2f} — DECLINING EPS year; high for cycle)
  FY2028E P/E         : {CURRENT_PRICE/CONS_EPS_2YR:.1f}x  (FY2028E ${CONS_EPS_2YR:.2f}; fair if auto ramp delivers)
  Historical PE range : 12–28x  (trough 12x; mid-cycle 18-22x; peak 26-28x AI-phone mania)
  Market cap          : ~${mktcap_b:.0f}B  ({SHARES_M:.0f}M shares × ${CURRENT_PRICE:.2f})
  Dividend yield      : {div_yield:.1f}%  ($3.40/share annual; 14 consecutive years of dividend growth)
  FCF (FY2026E est)   : ~${fcf_est:.1f}B  (~$9.96B non-GAAP net income; FCF conversion ~100%)
  FCF yield           : ~{fcf_yield:.1f}%  (${fcf_est:.1f}B / ${mktcap_b:.0f}B)
  Q2 FY2026 results   : Revenue $10.6B; non-GAAP EPS $2.65 (high end of guidance)
  Q2 segment detail   : QCT $9.1B [Handsets $6.0B | IoT $1.7B (+9%) | Auto $1.33B (+38% RECORD)]
  Q3 FY2026 guidance  : Revenue $9.2-10.0B; non-GAAP EPS $2.10-$2.30; Auto guided +~50% YoY
  FY2025 actual       : Non-GAAP EPS $12.03; revenue $44.3B; FY ended Sep 28 2025
  EPS trajectory      : FY2022 $12.53 → FY2023 $8.43 → FY2024 $10.22 → FY2025 $12.03 → FY2026E $9.40
  Apple modem         : iPhone 17/18 uses Apple C1 modem; QCOM exit $6-8B revenue over FY2026-2027
  Automotive          : Snapdragon Ride; 80%+ ADAS market share; annualised >$5B rate Q2 FY2026
  Hyperscaler chip    : Custom data center inference chip confirmed; Dec 2026 tape-out target
  Snapdragon X Elite  : Windows AI PCs (Dell, HP, Lenovo, Surface); competing with Intel Core Ultra
  QTL royalties       : $1.4B quarterly; 72% EBT margin; royalties on every global Android phone
  52-week range       : ${EPS_TROUGH_PRICE:.2f} – $247.90  (currently {CURRENT_PRICE/247.90*100:.0f}% of 52-week high)
  HOLD thesis breaks if: Automotive Q3/Q4 decelerates below +20% YoY (execution risk);
                         OR hyperscaler chip news negative (cancelled or delayed beyond 2027);
                         OR QTL faces new royalty litigation/settlement pressure
  ADD trigger         : Pullback to $185-210 (ratio_b 1.1-1.5x → WATCHLIST/ACCUMULATE zone);
                         at $165 ratio_b ~0.75x → ◉ BUY territory; BE PATIENT after surge


  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: 1.35x  |  Idiosyncratic: 60%  |  Macro: 40%

  Driver                                                 Type    Wt  Note
  ────────────────────────────────────────────────────────────────────────────────────────────
  Automotive design win / revenue delivery (quarterly)      IDIO  30%  PRIMARY signal; sustained +30%+ YoY validates diversification thesis
  Apple modem wind-down pace (quarterly QCT handset rev)    IDIO  20%  Faster exit = worse near-term; any Apple win-back = massive upside
  Hyperscaler custom chip programme progress                IDIO  10%  Dec 2026 tape-out confirmed; any delay = multiple compression
  Global smartphone unit cycle (5G upgrades, AI phones)    MACRO 20%  Flat units = QCOM relies on ASP; down >10% = EPS miss risk
  China tech restrictions / export controls                MACRO 20%  ~65% of QCT revenue is China-region; any BIS action = severe downside
""")

    print("=" * 72)
    print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-24")
    print("=" * 72)


if __name__ == "__main__":
    run_report()
