#!/usr/bin/env python3
"""
ibm_signal_model.py  —  International Business Machines Corp (NYSE: IBM)
Bottom-Up Risk/Reward Signal Model
All amounts in USD.  IBM FY = calendar year (Jan–Dec).
Non-GAAP EPS = IBM "operating (non-GAAP) EPS" (excludes acquisition-related charges,
pension costs, and other items).
Note: Kyndryl infrastructure-services spinoff completed Nov 2021; all EPS figures
are post-spinoff "continuing operations" basis.
"""

import math, sys, io, contextlib

TICKER        = "IBM"
COMPANY       = "International Business Machines Corporation"
EXCHANGE      = "NYSE"
CURRENCY      = "USD"
FY_END        = "December 31 (calendar year)"
SHARES_M      = 935.0          # million diluted shares (~market cap $237.8B / $253.84)

CURRENT_PRICE = 253.84         # IBM — fetched from Yahoo Finance / search, 2026-05-22
                               # Note: includes +17.2% surge on $1B quantum computing govt investment

# ── EPP FLOOR ──────────────────────────────────────────────────────────────
EPS_TROUGH        = 9.12       # FY2022 non-GAAP; first full post-Kyndryl year; lowest in post-spinoff era
EPS_TROUGH_PRICE  = 212.34     # 52-wk recent low (2026 correction); 212.34/11.59 = 18.3x trough PE
EPP_MIN_PE        = 15         # structural floor; below 18.3x recent trough; above 2022-era 13x; accounts
                               # for IBM's ongoing software-mix shift (higher quality = higher floor)
EPS_FY2025        = 11.59      # FY2025 non-GAAP actual; +12.2% from FY2024 $10.33; Q4 $4.52 beat
EPS_NOW           = 12.75      # FY2026E; no explicit EPS guidance; derived from >5% CC rev + FCF +$1B;
                               # Q1 2026 $1.91 (+19% YoY) pace supports $12.50-$13.00 range; midpoint used
EPP               = round(EPS_NOW * EPP_MIN_PE, 2)   # $191.25

epp_gap_pct       = round((CURRENT_PRICE - EPP) / EPP * 100, 1)   # +32.7%

# ── METHOD B ───────────────────────────────────────────────────────────────
CONS_EPS_2YR  = 15.00          # FY2028E; ~8.5% CAGR from FY2026E; Software +10%+ carries; operating leverage
EPS_FWD       = 13.80          # FY2027E (consensus proxy; ~8% growth from FY2026E $12.75)
CONS_EXIT_PE  = 21             # IBM re-rating from "declining IBM" 10-15x → "hybrid-cloud AI IBM" 20-25x;
                               # 21x = conservative mid-cycle; below ATH implied PE ~28x (Nov 2025 $324.90)
price_b       = round(CONS_EPS_2YR * CONS_EXIT_PE, 2)   # $315.00
ratio_b       = round((CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE), 2)   # 1.02x

# ── SOFTMAX ENGINE ─────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  {"price": 140.0,  "eps": 10.0,  "pe": 14.0,
              "desc": "Software growth stalls; HashiCorp mis-integration; mainframe cycle disappoints"},
    "BASE":  {"price": 315.0,  "eps": 15.0,  "pe": 21.0,
              "desc": "FY2028E consensus; Software +10%/yr; quantum matures; 21x mid-cycle re-rate"},
    "BULL":  {"price": 450.0,  "eps": 18.0,  "pe": 25.0,
              "desc": "watsonx dominates enterprise AI; quantum commercialises; 25x premium re-rate"},
    "XBULL": {"price": 616.0,  "eps": 22.0,  "pe": 28.0,
              "desc": "Quantum + agentic AI super-cycle; IBM = enterprise AI OS; ATH PE restored"},
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
    {"name": "Software segment acceleration (Red Hat + watsonx + automation)",
     "rating": +1.0, "weight": 0.25,
     "desc": ("Software growing +11% Q1 2026 YoY; ~43% of IBM revenue at 75%+ gross margins. "
              "Red Hat OpenShift = de-facto enterprise hybrid cloud OS. watsonx AI platform "
              "gaining enterprise traction (50,000+ clients at Think 2026). HashiCorp adds "
              "infrastructure-automation ARR. Software mix expansion structurally re-rates IBM.")},
    {"name": "Quantum computing leadership ($1B govt investment)",
     "rating": +0.9, "weight": 0.15,
     "desc": ("IBM leads globally in quantum computing (1,000+ qubit systems; error-correction "
              "milestones in 2025). US government committed $1B for quantum chip foundry — "
              "national-security driven; sticky multi-year revenue. Near-term catalyst that "
              "preceded the May 2026 +17% stock surge. Quantum monetisation 2027-2030 window.")},
    {"name": "FCF quality + 100-year dividend ($6.76/share; 2.66% yield)",
     "rating": +0.6, "weight": 0.20,
     "desc": ("FY2025 FCF $12.7-14.7B (definition-dependent); FY2026E ~$14B. Dividend raised "
              "to $1.69/share quarterly ($6.76 annual; IBM has paid continuously since 1916). "
              "2.66% yield at $253.84 creates institutional floor; dividend covenant disciplines "
              "capital allocation. Buybacks minimal — FCF used for acquisitions + dividends.")},
    {"name": "HashiCorp integration risk ($6.4B acquisition, 2024)",
     "rating": -0.7, "weight": 0.20,
     "desc": ("HashiCorp (Terraform/Vault) acquired 2024 for $6.4B. Integration complexity: "
              "open-source community friction (BSL license change), cloud-native competition. "
              "EPS-dilutive for 2-3 years. IBM must prove Terraform + IBM portfolio synergies "
              "before the market gives credit. Integration failures could impair Software growth.")},
    {"name": "Consulting growth lag and structural headwinds",
     "rating": -0.5, "weight": 0.20,
     "desc": ("IBM Consulting (~30% of revenue) growing low-to-mid single digits vs Software +11%. "
              "Labor-intensive model faces same AI displacement narrative as ACN. Smaller US "
              "federal exposure than ACN but still present (~$1-2B). Mix drag on blended margins "
              "as Consulting grows slower than high-margin Software — margin expansion pace risk.")},
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

    div_yield = 6.76 / CURRENT_PRICE * 100
    mktcap    = SHARES_M * CURRENT_PRICE / 1000

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
  Sector   : Hybrid Cloud · Enterprise AI (watsonx) · Quantum Computing
  FY end   : {FY_END}
  EPS basis: Non-GAAP ("operating EPS"; excludes acquisition charges, pension)
  Post-Kyndryl: Kyndryl infra-services spun off Nov 2021; all EPS post-spinoff
  Price    : ${CURRENT_PRICE:.2f}  [2026-05-22]
  52-week  : ${EPS_TROUGH_PRICE:.2f} low – $324.90 high  (ATH $324.90; −21.9% from ATH)
""")

    print("=" * 72)
    print(f"  PART 2 — ANALYST COMMENTARY  |  {TICKER}")
    print("=" * 72)
    print(f"""
  A. INVESTMENT THESIS
  ----------------------------------------------------------------------

  IBM has completed one of the most consequential business transformations
  in enterprise technology history.  The "declining IBM" of 2014-2020 —
  characterised by 22 consecutive quarters of revenue decline, over-reliance
  on legacy mainframe services, and financial-engineering EPS — is gone.
  The $34B acquisition of Red Hat (2019) installed hybrid cloud as IBM's
  strategic core.  The Kyndryl spinoff (Nov 2021) shed the low-margin
  managed infrastructure drag.  The result: a focused Hybrid Cloud + AI +
  Quantum business generating $14B+ in annual FCF.

  Three structural growth engines are converging in 2026:

  1. SOFTWARE (+11% Q1 2026 YoY): Red Hat / OpenShift is the de-facto
     enterprise hybrid cloud operating system.  watsonx AI — launched 2023,
     scaled 2024-25 — now serves 50,000+ enterprise clients.  HashiCorp
     (Terraform / Vault) adds infrastructure-automation ARR.  Software is
     ~43% of revenue at 75%+ gross margins — the re-rating engine.

  2. QUANTUM ($1B US government investment): IBM leads globally in
     practical quantum computing.  A $1B government commitment for a quantum
     chip foundry (announced May 2026) catalysed a +17.2% stock surge.
     This is not speculative — IBM has 1,000+ qubit error-corrected systems
     and a monetisation window opening in 2027-2030.

  3. MAINFRAME (z-series AI monetisation): The z16 / z17 mainframe cycle
     embeds on-chip AI accelerators.  Every financial, insurance and
     government IBM mainframe customer is now an AI workload buyer.

  At ${CURRENT_PRICE:.2f}, IBM trades at {CURRENT_PRICE/EPS_NOW:.1f}x FY2026E non-GAAP EPS — a
  meaningful discount to its November 2025 ATH-implied ~28x and well below
  where a 43%-software, AI-native IBM should trade at maturity.

  Pre-surge (stock at ~$216 before the quantum announcement), Ratio B was
  ~0.12x — a strong BUY.  Post-surge Ratio B is {ratio_b:.2f}x: ACCUMULATE.
  Add on weakness; core thesis intact.

  Signal: {sig}  |  Ratio B: {ratio_b:.2f}x  |  EPP gap: +{epp_gap_pct:.1f}%


  B. EARNINGS POWER PRICE (EPP) — STRUCTURAL FLOOR
  ----------------------------------------------------------------------

  EPS anchor   : ${EPS_TROUGH:.2f}  (FY2022; first full post-Kyndryl year; lowest
                  post-spinoff EPS; clean baseline before Red Hat/watsonx ramp)
  Bear trough  : ${EPS_TROUGH_PRICE:.2f}  (52-wk recent low; {EPS_TROUGH_PRICE:.2f}/{EPS_FY2025:.2f} = 18.3x trough PE;
                  stock bottomed during early 2026 macro selloff before quantum news)
  EPP min PE   : {EPP_MIN_PE}x  (structural floor; below 18.3x recent trough; reflects
                  IBM as software-dominant hybrid cloud, not legacy IT services)

  EPS now      : ${EPS_NOW:.2f}  (FY2026E; Q1 2026 $1.91 +19% YoY; >5% CC revenue;
                  Software >10%; FCF +~$1B YoY → $14B+; midpoint full-year estimate)
  EPP floor    : ${EPS_NOW:.2f} × {EPP_MIN_PE}x = ${EPP:.2f}
  Current vs EPP: ${CURRENT_PRICE:.2f} vs ${EPP:.2f}  (+{epp_gap_pct:.1f}% above floor)

  Pre-surge price ~$216 was only ~13% above EPP → very low risk/reward buffer.
  At current ${CURRENT_PRICE:.2f}, EPP gap has expanded to 32.7% — still not stretched
  for a business with this FCF yield and EPS growth trajectory.


  C. METHOD B — 2-YEAR EARNINGS POWER TARGET
  ----------------------------------------------------------------------

  CONS_EPS_2YR : ${CONS_EPS_2YR:.2f}  (FY2028E; ~8.5% CAGR from ${EPS_NOW:.2f};
                  Software +10%+ drags blended IBM growth; HashiCorp accretive by
                  FY2027; quantum begins monetising; FY2027E proxy ~${EPS_FWD:.2f})
  CONS_EXIT_PE : {CONS_EXIT_PE}x  (conservative; IBM historical 10-15x in decline era;
                  20-25x in transformation era; 21x = below ATH implied 28x; accounts
                  for execution risk on HashiCorp + consulting drag)
  Method B     : ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x = ${price_b:.2f}

  Ratio B = (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})
           = ${CURRENT_PRICE - EPP:.2f} / ${price_b - CURRENT_PRICE:.2f}
           = {ratio_b:.2f}x  →  {sig}

  Sensitivity to exit PE (at CONS_EPS_2YR ${CONS_EPS_2YR:.2f}):
    CONS_EXIT_PE = 18x → Price_B $270 → Ratio B {(CURRENT_PRICE-EPP)/(270-CURRENT_PRICE):.2f}x  (HOLD/TRIM)
    CONS_EXIT_PE = 20x → Price_B $300 → Ratio B {(CURRENT_PRICE-EPP)/(300-CURRENT_PRICE):.2f}x  (WATCHLIST)
    CONS_EXIT_PE = 21x → Price_B $315 → Ratio B {ratio_b:.2f}x  (ACCUMULATE)  ← base case
    CONS_EXIT_PE = 23x → Price_B $345 → Ratio B {(CURRENT_PRICE-EPP)/(345-CURRENT_PRICE):.2f}x  (BUY)
    CONS_EXIT_PE = 25x → Price_B $375 → Ratio B {(CURRENT_PRICE-EPP)/(375-CURRENT_PRICE):.2f}x  (BUY)
  Bull case (23-25x, justified if Software mix reaches 50%+) gives BUY.
  Base case (21x) gives ACCUMULATE. Conservative (18x) gives HOLD.


  D. SCENARIO ANALYSIS
  ----------------------------------------------------------------------
  Scenario     EPS     P/E    Price    vs Now  Description
  ----------------------------------------------------------------------""")

    for k, s in SCENARIOS.items():
        vs = (s["price"] / CURRENT_PRICE - 1) * 100
        sign = "+" if vs >= 0 else ""
        print(f"  {k:<8}  ${s['eps']:5.2f}  {s['pe']:4.1f}x  ${s['price']:6,.0f}   {sign}{vs:5.1f}%  {s['desc']}")

    print(f"""
  BASE scenario $315 = Method B target (by construction); close to ATH $324.90.
  BEAR at $140 requires both Software growth stall AND multiple compression to
  14x — a simultaneous Kyndryl-era re-regression; unlikely given Red Hat moat.
  BULL $450 requires watsonx to win meaningful enterprise AI budget share beyond
  current 50,000-client base; achievable but requires 2-3 year ramp.


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

  Interpretation: Market composite {mkt_composite:.2f} sits between BEAR (1.25) and BASE (2.00),
  reflecting lingering scepticism about IBM's transformation pace and the
  sustainability of the quantum catalyst. SCA pushes the model composite to
  {model_composite:.2f} — closer to BASE — on Software momentum and government quantum
  backing. Model EV {sign_ev}{ev_chg:.0f}% implies meaningful upside from current prices,
  consistent with the ACCUMULATE signal.


  F. STRUCTURAL COMPOSITE ADJUSTMENT (SCA)
  ----------------------------------------------------------------------
  Factor                                                        Rating    Wt
  --------------------------------------------------------------------------""")
    for f in STRUCTURAL_FACTORS:
        name_t = f["name"][:55]
        desc_t = f["desc"][:60]
        print(f"  {name_t:<55}  {f['rating']:+.1f}  {f['weight']:.0%}")
        print(f"    {desc_t}")

    print(f"""
  SCA raw = {sca_raw:.3f}   SCA adj (div 2) = {sca_adj:.3f}
  Market composite {mkt_composite:.2f}  +  SCA {sca_adj:.3f}  =  Model composite {model_composite:.3f}


  G. EPS QUALITY DECOMP  (FY2025 ${EPS_FY2025:.2f} → FY2026E ${EPS_NOW:.2f} = +${EPS_NOW - EPS_FY2025:.2f} = +{(EPS_NOW/EPS_FY2025-1)*100:.1f}%)
  ----------------------------------------------------------------------
  Component                                                      Share          Type
  ---------------------------------------------------------------------------------
  Software segment operating leverage (Red Hat / watsonx /       55%    Structural
    automation at 75%+ gross margin; mix shift lifts blended margin
    as Software grows from 43% → 45%+ of total revenue by FY2026)
  HashiCorp first full-year contribution (closed mid-2024;        15%    Structural
    Terraform/Vault ARR added to Software segment; full FY2026 vs
    partial FY2025; infrastructure-automation becomes recurring)
  Consulting stable base + modest AI uplift (IBM Consulting       10%    Structural
    grows low-single-digits; agentic AI projects add higher-value
    engagements; partially offset by slower headcount-model growth)
  Share count stability (minimal buybacks; dividend + M&A         5%    Structural
    consume FCF; ~935M shares; EPS growth is P&L-driven)
  FX translation headwind (IBM ~60% non-USD revenue; USD          -5%    Temporal
    strength in H1 2026 weighs on reported vs CC growth rates)
  Quantum / Infrastructure one-time items (R&D investment         20%    Structural
    in quantum foundation models; mainframe z-series AI silicon
    generates incremental software-attach revenue per box)

  Structural :  105%
  Temporal   :   -5%  (FX)
  Net         :  +{(EPS_NOW/EPS_FY2025-1)*100:.1f}%
""")

    print("=" * 72)
    print(f"  PART 3 — NUMBERS & SIGNALS   |  {TICKER}")
    print("=" * 72)
    print(f"""
  H. RISK / RETURN SUMMARY
  ----------------------------------------------------------------------

  Current price       : ${CURRENT_PRICE:.2f}  (post +17.2% quantum surge; 52-wk low ${EPS_TROUGH_PRICE:.2f})
  EPP floor           : ${EPP:.2f}  (+{epp_gap_pct:.1f}% above floor; {EPP_MIN_PE}x × ${EPS_NOW:.2f} FY2026E)
  Method B target     : ${price_b:.2f}  (upside: +{(price_b/CURRENT_PRICE-1)*100:.0f}%; near ATH of $324.90)
  BEAR scenario       : $140  (downside: -{(1-140/CURRENT_PRICE)*100:.0f}%; software stall + 14x compression)
  Ratio B             : {ratio_b:.2f}x  -> {sig}
  Pre-surge ratio B   : ~0.12x at ~$216  (would have been ◉ BUY before quantum news)
  Forward P/E         : {CURRENT_PRICE/EPS_NOW:.1f}x  (FY2026E ${EPS_NOW:.2f}; ATH implied ~28x at $324.90)
  FY2028E P/E         : {CURRENT_PRICE/CONS_EPS_2YR:.1f}x  (FY2028E ${CONS_EPS_2YR:.2f})
  Historical PE range : 10–15x (decline era) → 18–28x (transformation era); current {CURRENT_PRICE/EPS_NOW:.1f}x
  Market cap          : ~${mktcap:.1f}B  ({SHARES_M:.0f}M shares × ${CURRENT_PRICE:.2f})
  Dividend yield      : {div_yield:.2f}%  (${6.76:.2f}/share annual; raised to $1.69/qtr Q1 2026; 100+ yr history)
  FCF (FY2025)        : ~$12.7–14.7B  (definition-dependent); FY2026E ~$14B+ (reaffirmed)
  Q1 2026 results     : Revenue $15.9B (+9% YoY, +6% CC); non-GAAP EPS $1.91 (+19% YoY)
  Software Q1 2026    : +11% YoY; Red Hat / OpenShift + watsonx + HashiCorp all growing
  Quantum catalyst    : $1B US govt quantum chip foundry investment (May 2026); +17.2% stock response
  FY2026 guidance     : >5% CC revenue; Software >10% CC; FCF +~$1B YoY (~$14B+)
  Q2 2026 catalyst    : ~July 2026 (Q2 FY2026 results; watch Software growth rate and FCF)
  52-week range       : ${EPS_TROUGH_PRICE:.2f} – $324.90  (currently {CURRENT_PRICE/324.90*100:.0f}% of 52-week high)
  ACCUMULATE thesis breaks if: Software growth decelerates below 7% (Red Hat/HashiCorp slip);
                        OR FCF disappoints below $13B (acquisition integration drain);
                        OR quantum timeline extends beyond 2030 (no near-term monetisation)
  ADD trigger         : Current price is in range; add more aggressively on pullback to $215–230


  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: 0.85x  |  Idiosyncratic: 65%  |  Macro: 35%

  Driver                                                 Type    Wt  Note
  ────────────────────────────────────────────────────────────────────────────────────────────
  Software segment quarterly growth rate (Red Hat/watsonx)  IDIO  30%  Must sustain >10% CC growth; any decel below 8% = major de-rating
  HashiCorp integration progress (ARR contribution)      IDIO   20%  FY2027 is the proof year; accretion vs dilution confirmed by FCF
  Quantum computing programme milestones                 IDIO   15%  Technical gates (error correction, qubit scale) drive govt contract
  Enterprise IT spending cycle (Fortune 500 capex)      MACRO  20%  Hybrid cloud + AI transformation budgets; CFO caution = booking lag
  USD strength (FX translation; ~60% non-USD revenue)   MACRO  10%  IBM reports CC and USD; local-currency strength of 5-6% vs USD 9%
  Interest rates (M&A cost of capital; pension liability) MACRO   5%  IBM pension fund is large; rate sensitivity meaningful on GAAP P&L
""")

    print("=" * 72)
    print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-22")
    print("=" * 72)


if __name__ == "__main__":
    run_report()
