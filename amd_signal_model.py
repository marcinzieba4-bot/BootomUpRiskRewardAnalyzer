#!/usr/bin/env python3
"""
amd_signal_model.py  —  Advanced Micro Devices, Inc. (NASDAQ: AMD)
Bottom-Up Risk/Reward Signal Model
All prices and EPS in USD.
"""

import math, sys, io, contextlib

TICKER        = "AMD"
COMPANY       = "Advanced Micro Devices, Inc."
EXCHANGE      = "NASDAQ"
FY_END        = "December 31 (calendar year)"
SHARES_M      = 1651.0          # million diluted shares (Q1 2026 10-Q; ~1,651M)

CURRENT_PRICE = 467.51          # AMD — fetched from web search (gurufocus / search), 2026-05-24
                                 # Close May 22: $462.98; intraday ATH May 22: $481.41; May 24: $467.51

# ── EPP FLOOR ──────────────────────────────────────────────────────────────
EPS_TROUGH        = 2.65        # FY2023; PC/gaming + embedded downturn; lowest post-2020 non-GAAP EPS
EPS_TROUGH_PRICE  = 107.67      # 52-wk low (May 2025 correction); 107.67/4.50 FY2025E ≈ 23.9x fwd P/E
EPP_MIN_PE        = 25          # structural floor; AMD never historically cheap; 25x reflects AI
                                 # chip company with structural data center / EPYC moat, not legacy PC
EPS_FY2025        = 4.17        # FY2025 full-year non-GAAP record; announced Feb 3 2026 ($6.8B net income)
EPS_NOW           = 6.50        # FY2026E conservative; Q1 2026 actual $1.37 (+28% YoY); consensus $7.41;
                                 # using lower estimate as H2 ramp uncertain; 1.37+1.55+1.75+1.83 ≈ $6.50
EPP               = round(EPS_NOW * EPP_MIN_PE, 2)    # $162.50

epp_gap_pct       = round((CURRENT_PRICE - EPP) / EPP * 100, 1)    # +187.7%

# ── METHOD B ───────────────────────────────────────────────────────────────
CONS_EPS_2YR  = 14.00           # FY2028E conservative; analyst consensus mean $17.91 (range $13.15–$23.84);
                                 # using $14 = below bear-case consensus to reflect execution/competition risk
CONS_EXIT_PE  = 40              # AI chip leader exit multiple; generous vs NVDA ~30x but reflects growth
                                 # premium; AMD trades at 72x FY2026E today — 40x in 2 yrs = meaningful compression
price_b       = round(CONS_EPS_2YR * CONS_EXIT_PE, 2)    # $560.00
ratio_b       = round((CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE), 2)   # 3.30x → AVOID

# ── SOFTMAX ENGINE ─────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  {"price": 80.0,   "eps":  4.0,  "pe": 20.0,
              "desc": "AI data center bubble; AMD loses GPU market to NVDA + ASICs; EPYC stalls; EPS ≈ FY2024"},
    "BASE":  {"price": 560.0,  "eps": 14.0,  "pe": 40.0,
              "desc": "Conservative FY2028E $14 × 40x; data center +25% CAGR; AMD 15-20% GPU share"},
    "BULL":  {"price": 860.0,  "eps": 21.5,  "pe": 40.0,
              "desc": "MI400/500 ramp; EPYC 30%+ server share; data center $30B+; near-consensus FY2028E"},
    "XBULL": {"price": 1400.0, "eps": 28.0,  "pe": 50.0,
              "desc": "AMD captures 25%+ AI GPU share; ROCm ecosystem matures; FY2028E top-of-range EPS"},
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
    {"name": "Data Center AI GPU acceleration (MI300X → MI400 ramp)",
     "rating": +1.0, "weight": 0.25,
     "desc": ("AMD MI300X shipped $5B+ in 2025; MI300X is the primary alternative to NVIDIA H100/H200 "
              "for AI inference and training. Q1 2026 Data Center revenue $5.8B (+57% YoY). MI400 "
              "sampling in 2026 with enhanced inference bandwidth. Microsoft, Meta, Oracle and others "
              "now dual-sourcing to reduce NVIDIA dependency — structural AMD share capture in progress.")},
    {"name": "EPYC server CPU market share (taking Intel Data Center share)",
     "rating": +0.8, "weight": 0.15,
     "desc": ("EPYC Genoa/Turin holds ~30% server CPU market share (vs single digits in 2020). Intel "
              "Xeon struggling with Sapphire Rapids yield issues and delayed Granite Rapids. AMD's "
              "chiplet architecture (3D V-Cache) provides performance-per-watt advantage. Each 1% "
              "server market share gain ≈ $300-400M incremental annual revenue at high margins.")},
    {"name": "NVIDIA CUDA software ecosystem moat (existential competitive risk)",
     "rating": -1.0, "weight": 0.30,
     "desc": ("NVIDIA CUDA has 10+ years of developer lock-in across every major AI framework "
              "(PyTorch, TensorFlow, JAX). AMD ROCm is functional but trails in library completeness, "
              "developer tooling, and enterprise support. The majority of AI training workloads remain "
              "on NVIDIA hardware by developer preference. AMD must overcome ecosystem moat to grow "
              "beyond price-sensitive inference and dual-sourcing use cases — a multi-year challenge.")},
    {"name": "Custom ASIC competition from hyperscalers (Google TPU, Meta MTIA, AWS Trainium)",
     "rating": -0.7, "weight": 0.15,
     "desc": ("Google TPU v5, Meta MTIA v2, Amazon Trainium 2, and Microsoft Maia are all ramping at "
              "scale. Hyperscalers are increasingly running their own AI workloads on custom silicon, "
              "reducing the addressable market for both AMD and NVIDIA. Custom ASICs optimised for "
              "specific model architectures (Transformer inference) will erode AMD's addressable TAM "
              "in inference — AMD's fastest-growing GPU use case.")},
    {"name": "Gaming and Embedded structural headwinds",
     "rating": -0.4, "weight": 0.15,
     "desc": ("Gaming revenue Q1 2026: $0.2B (-59% YoY). Semi-custom (Sony/Microsoft console SoCs) "
              "in end-of-cycle decline. Radeon dGPU under pressure from NVIDIA RTX 50-series. Embedded "
              "recovered +28% Q1 2026 from inventory trough but remains well below 2022 peak ($1.3B/qtr). "
              "These segments were 30% of revenue in 2021; now <10%, but their decline concentrates "
              "execution risk in data center — where NVIDIA competition is most intense.")},
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

    mktcap_b = CURRENT_PRICE * SHARES_M / 1000   # $B

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
  Sector   : Semiconductors · AI GPU · Data Center · PC/Client CPU
  FY end   : {FY_END}
  EPS basis: Non-GAAP (excludes stock-based comp, acquisition amortisation)
  Shares   : ~{SHARES_M:.0f}M diluted
  Price    : ${CURRENT_PRICE:.2f}  [2026-05-24]
  52-week  : ${EPS_TROUGH_PRICE:.2f} low – $481.41 high  (ATH $481.41 intraday May 22 2026)
""")

    print("=" * 72)
    print(f"  PART 2 — ANALYST COMMENTARY  |  {TICKER}")
    print("=" * 72)
    print(f"""
  A. INVESTMENT THESIS
  ----------------------------------------------------------------------

  AMD has executed one of the most remarkable product turnarounds in
  semiconductor history.  Under Lisa Su (CEO since 2014), AMD rebuilt its
  CPU architecture (Zen), won the console SoC cycle (PlayStation/Xbox),
  took server CPU market share from Intel (EPYC now ~30% of server units),
  and entered the AI accelerator market just as demand exploded.

  Three growth engines defined FY2025 and early FY2026:

  1. DATA CENTER AI GPUs (+57% Q1 2026 YoY → $5.8B quarterly):
     AMD MI300X is the only credible large-scale alternative to NVIDIA's
     H100/H200.  Microsoft, Meta, Oracle, and others are dual-sourcing to
     reduce NVIDIA concentration risk.  MI400 (next-gen inference chip) is
     sampling in 2026.  Data Center is now ~56% of AMD revenue and growing.

  2. EPYC SERVER CPUs (structural Intel displacement):
     EPYC Genoa/Turin holds ~30% server CPU market share.  Intel's Xeon
     roadmap delays continue to gift AMD enterprise design wins.  Each
     new hyperscaler rack design is a 3-5 year revenue lock-in.

  3. EMBEDDED RECOVERY (+28% Q1 2026 after inventory trough):
     Automotive, industrial, and communications embedded returned to
     growth after a brutal FY2023-FY2024 inventory correction.

  The problem: the market has fully priced all three engines — and then
  some.  AMD has surged +317% over 12 months (52-week: ${EPS_TROUGH_PRICE:.2f}–$481.41),
  hitting an ATH intraday on May 22, 2026.  At ${CURRENT_PRICE:.2f}, AMD trades at
  {CURRENT_PRICE/EPS_NOW:.1f}x FY2026E non-GAAP EPS — a price that embeds extraordinary
  execution with no margin for error or competitive setback.

  The central risk is NVIDIA's CUDA ecosystem moat.  AMD ROCm is
  functional but lacks the developer ecosystem depth that CUDA has built
  over 15+ years.  AMD's GPU wins are primarily in price-sensitive
  inference (where cost-per-token matters) and dual-sourcing mandates,
  not in open-competition training workloads where NVIDIA dominates.

  Method B (FY2028E $14.00 × 40x = $560) implies only +{(price_b/CURRENT_PRICE-1)*100:.0f}% upside
  on conservative assumptions vs a BEAR scenario of -83%.  After the
  317% 12-month run, the risk/reward is structurally unfavourable.

  Signal: {sig}  |  Ratio B: {ratio_b:.2f}x  |  EPP gap: +{epp_gap_pct:.1f}%


  B. EARNINGS POWER PRICE (EPP) — STRUCTURAL FLOOR
  ----------------------------------------------------------------------

  EPS anchor   : ${EPS_TROUGH:.2f}  (FY2023; PC/gaming cycle downturn + embedded
                  inventory glut; lowest non-GAAP EPS post-2020; trough in cycle)
  Bear trough  : ${EPS_TROUGH_PRICE:.2f}  (52-wk low; ~May 2025 correction;
                  $107.67 / ~$4.50 FY2025E at that time ≈ 23.9x forward P/E)
  EPP min PE   : {EPP_MIN_PE}x  (structural floor; AMD never historically cheap;
                  25x reflects AI chip company with data center moat; below the
                  23.9x observed trough P/E at the 52-wk low)

  EPS now      : ${EPS_NOW:.2f}  (FY2026E conservative; Q1 2026 actual $1.37 (+28%
                  YoY); Q2 2026 guided revenue $11.2B +9% seq, 56% GM; consensus
                  mean $7.41 but using lower estimate for execution/competition risk)
  EPP floor    : ${EPS_NOW:.2f} × {EPP_MIN_PE}x = ${EPP:.2f}
  Current vs EPP: ${CURRENT_PRICE:.2f} vs ${EPP:.2f}  (+{epp_gap_pct:.1f}% above floor)

  The EPP floor of ${EPP:.2f} is -65% from the current price.  AMD would
  need to fall to FY2023 EPS levels AND trade at 25x — i.e., a genuine
  AI bubble burst combined with AMD losing GPU market share.  The floor
  is real but distant; the gap (+{epp_gap_pct:.1f}%) is the widest in coverage
  alongside TSLA (893%).


  C. METHOD B — 2-YEAR EARNINGS POWER TARGET
  ----------------------------------------------------------------------

  CONS_EPS_2YR : ${CONS_EPS_2YR:.2f}  (FY2028E conservative; analyst consensus mean
                  $17.91, range $13.15–$23.84; using $14.00 = near bear-case of
                  consensus to account for: NVIDIA moat risk, custom ASIC growth,
                  and gaming/embedded structural declines; if AMD achieves $18+
                  EPS the signal would improve significantly)
  CONS_EXIT_PE : {CONS_EXIT_PE}x  (generous for an AI chip co; AMD at 72x FY2026E today;
                  40x in 2 yrs = meaningful multiple compression; NVDA trades ~30x
                  now; AMD at maturity with $14+ EPS likely 30-40x)
  Method B     : ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x = ${price_b:.2f}

  Ratio B = (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})
           = ${CURRENT_PRICE-EPP:.2f} / ${price_b-CURRENT_PRICE:.2f}
           = {ratio_b:.2f}x  →  {sig}

  Sensitivity to exit PE (at CONS_EPS_2YR ${CONS_EPS_2YR:.2f}):
    CONS_EXIT_PE = 30x → Price_B $420 → BELOW current price → N/A (AVOID)
    CONS_EXIT_PE = 35x → Price_B $490 → Ratio B {(CURRENT_PRICE-EPP)/(490-CURRENT_PRICE):.1f}x  (AVOID)
    CONS_EXIT_PE = 40x → Price_B $560 → Ratio B {ratio_b:.2f}x  (AVOID)  ← base case
    CONS_EXIT_PE = 45x → Price_B $630 → Ratio B {(CURRENT_PRICE-EPP)/(630-CURRENT_PRICE):.2f}x  (HOLD/TRIM)
    CONS_EXIT_PE = 50x → Price_B $700 → Ratio B {(CURRENT_PRICE-EPP)/(700-CURRENT_PRICE):.2f}x  (WATCHLIST)
  Even at 50x exit P/E (full bull premium), AMD is only WATCHLIST.
  Signal only reaches ACCUMULATE if EPS achieves $17+ AND exits at 45x+.


  D. SCENARIO ANALYSIS
  ----------------------------------------------------------------------
  Scenario     EPS      P/E    Price ($)    vs Now  Description
  ----------------------------------------------------------------------""")

    for k, s in SCENARIOS.items():
        vs = (s["price"] / CURRENT_PRICE - 1) * 100
        sign = "+" if vs >= 0 else ""
        print(f"  {k:<8}  ${s['eps']:5.1f}  {s['pe']:4.1f}x  ${s['price']:8,.0f}  {sign}{vs:5.1f}%  {s['desc']}")

    bear_p = SCENARIOS["BEAR"]["price"]
    bull_p = SCENARIOS["BULL"]["price"]
    base_p = SCENARIOS["BASE"]["price"]
    xbull_p = SCENARIOS["XBULL"]["price"]

    print(f"""
  BASE scenario ${base_p:,.0f} = Method B target (by construction).
  BEAR at ${bear_p:,.0f} = AI bubble burst: AMD GPU market collapses, EPYC stalls,
  EPS resets to ~FY2024 levels ($4) and market assigns 20x on a commodity
  chip company narrative. -83% from current.
  BULL/XBULL require AMD to achieve consensus or above-consensus EPS AND
  maintain 40-50x exit multiples — plausible if AI boom continues.


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
    sign = "+" if ev_chg >= 0 else ""
    print(f"""
  Model EV (proxy) : ${model_ev:,.0f}  ({sign}{ev_chg:.1f}% vs current ${CURRENT_PRICE:.2f})

  Interpretation: Market composite {mkt_composite:.2f} is between BASE (2.00) and BULL
  (2.75), confirming that the market is pricing AMD well into the BULL
  scenario. SCA of {sca_adj:+.3f} (slightly negative) pulls the model composite
  toward BASE, reflecting NVIDIA's ecosystem moat and custom ASIC headwinds.
  The model EV is {sign}{ev_chg:.0f}% — BUT this is entirely driven by the BULL and
  XBULL tails. For investors today: BASE (+{(base_p/CURRENT_PRICE-1)*100:.0f}%) vs BEAR (-{(1-bear_p/CURRENT_PRICE)*100:.0f}%)
  is a deeply asymmetric risk/reward — the market is pricing a lot right.


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
  Data Center AI GPU ramp (MI300X volume × ASP uplift;           60%    Structural
    Q1 2026 Data Center +57% YoY; $5.8B/qtr; MI400 sampling;
    inference market growing faster than training; multiple OEM wins)
  EPYC server CPU volume + mix shift (units + ASP uplift vs       20%    Structural
    Intel Xeon; EPYC now ~30% server market; Turin wins extending;
    each hyperscaler design win = 3-5yr revenue annuity at 50%+ GM)
  Embedded segment recovery (inventory correction over;           15%    Structural
    +28% Q1 2026 YoY from trough; automotive/industrial restocking;
    Xilinx FPGA portfolio adds software-defined radio + automotive)
  Gaming decline partial offset (console SoC end-of-cycle;       -10%   Temporal
    Radeon dGPU weak vs NVIDIA RTX 50; semi-custom royalties fading;
    structural drag until next console cycle mid-2026+)
  Non-GAAP gross margin expansion (+170bps Q1 2026 to 55%;        15%    Structural
    data center mix-up lifts blended margin; chiplet architecture
    reduces wafer cost per compute unit vs monolithic designs)

  Structural :  110%
  Temporal   :  -10%  (gaming)
  Net         :  +{(EPS_NOW/EPS_FY2025-1)*100:.1f}%
""")

    print("=" * 72)
    print(f"  PART 3 — NUMBERS & SIGNALS   |  {TICKER}")
    print("=" * 72)
    print(f"""
  H. RISK / RETURN SUMMARY
  ----------------------------------------------------------------------

  Current price       : ${CURRENT_PRICE:.2f}  (ATH ${481.41:.2f} intraday May 22 2026; +317% 12-month)
  EPP floor           : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above floor; {EPP_MIN_PE}x × ${EPS_NOW:.2f} FY2026E)
  Method B target     : ${price_b:.2f}  (upside: +{(price_b/CURRENT_PRICE-1)*100:.0f}%; conservative)
  BEAR scenario       : ${bear_p:.0f}  (downside: -{(1-bear_p/CURRENT_PRICE)*100:.0f}%; AI bubble burst)
  Ratio B             : {ratio_b:.2f}x  -> {sig}
  Forward P/E         : {CURRENT_PRICE/EPS_NOW:.1f}x  (FY2026E ${EPS_NOW:.2f}; consensus mean implies {CURRENT_PRICE/7.41:.1f}x)
  FY2028E P/E         : {CURRENT_PRICE/CONS_EPS_2YR:.1f}x  (conservative ${CONS_EPS_2YR:.2f}) / {CURRENT_PRICE/17.91:.1f}x (consensus $17.91)
  Historical PE range : 20–70x  (decline era 20-30x; AI era 40-80x; current {CURRENT_PRICE/EPS_NOW:.0f}x = rich)
  Market cap          : ~${mktcap_b:.0f}B  ({SHARES_M:.0f}M shares × ${CURRENT_PRICE:.2f})
  FCF (Q1 2026)       : $2.6B  (record; tripled YoY; annual run rate ~$10B+; FCF yield ~1.3%)
  Q1 2026 results     : Revenue $10.3B (+38% YoY); non-GAAP EPS $1.37 (beat est $1.27); DC +57%
  Q2 2026 guidance    : Revenue ~$11.2B ±$300M (+46% YoY, +9% seq); non-GAAP GM 56%
  FY2025 annual       : Revenue $34.6B; non-GAAP EPS $4.17 (record); non-GAAP GM 52%
  Data Center Q1 2026 : $5.8B (+57% YoY); beating $5.56B consensus; now 56% of total revenue
  EPYC CPU            : ~30% server CPU market share (vs ~5% in 2020); Turin (Zen 5) shipping
  MI300X AI GPU       : Primary NVDA H100/H200 alternative; $5B+ shipped FY2025; MI400 sampling
  Gaming Q1 2026      : $0.2B (-59% YoY); console end-of-cycle; Radeon dGPU under NVIDIA pressure
  52-week range       : $107.67 – $481.41  (currently {CURRENT_PRICE/481.41*100:.0f}% of 52-week high)
  EPS growth path     : FY2023 $2.65 → FY2025 $4.17 (+57%) → FY2026E $6.50 (+56%) → FY2028E $14.00?
  AVOID thesis breaks if: FY2028E EPS achieves $17-18+ AND exit P/E holds 40-45x → BUY <$280 (ratio_b ~0.75x)
  RE-EVALUATE trigger : Pullback to $250-300 (EPP +54-85%; ratio_b 0.6-1.0x = BUY/ACCUMULATE zone)


  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: 1.55x  |  Idiosyncratic: 70%  |  Macro: 30%

  Driver                                                 Type    Wt  Note
  ────────────────────────────────────────────────────────────────────────────────────────────
  Data Center AI GPU quarterly revenue (MI300X/MI400 units)  IDIO  30%  Primary signal; any miss vs +40% YoY = instant de-rating at 70x P/E
  NVIDIA competitive dynamics (H200/B200/R100 vs MI300X)    IDIO  25%  Market share data; HPC procurement announcements; HGX attach rate
  EPYC server CPU design win cadence                         IDIO  15%  Quarterly PC/server ASP + unit data; any Intel recovery = headwind
  Hyperscaler AI capex cycle (AWS, Azure, GCP, Meta capex)   MACRO 20%  $300B+ annual combined AI capex is AMD's SAM; any cut = -40% AMD
  Semiconductor cycle + export controls (China AI chip ban)  MACRO 10%  BIS entity list expansion could remove China DC revenue (~5-7% AMD)
""")

    print("=" * 72)
    print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-24")
    print("=" * 72)


if __name__ == "__main__":
    run_report()
