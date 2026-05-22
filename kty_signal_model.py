#!/usr/bin/env python3
"""
kty_signal_model.py  —  Grupa Kęty SA (WSE: KTY / GPW: KTY / KTY.WA)
Bottom-Up Risk/Reward Signal Model
All prices and EPS in PLN (Polish Złoty).
"""

import math, sys, io, contextlib

TICKER        = "KTY"
COMPANY       = "Grupa Kęty SA"
EXCHANGE      = "WSE/GPW (Warsaw Stock Exchange)"
CURRENCY      = "PLN"
FY_END        = "December 31 (calendar year)"
SHARES_M      = 9.84           # million shares (derived: dividend total 482.77M PLN / 49.05 PLN per share)

CURRENT_PRICE = 1155.00        # KTY.WA — ATH 1,179 PLN hit May 6 2026; near-ATH estimate; source: Investing.com / search, 2026-05-22

# ── EPP FLOOR ──────────────────────────────────────────────────────────────
EPS_TROUGH        = 43.7       # FY2020 net profit 430.2M PLN / 9.84M shares; historical EPS floor
EPS_TROUGH_PRICE  = 799.50     # 52-wk recent low (2025 correction); 799.50/56.9 = 14.1x trough PE
EPP_MIN_PE        = 11         # structural floor; conservative vs 14.1x observed trough; recession + BEAR scenario
EPS_FY2025        = 56.9       # FY2025 net profit 560M PLN / 9.84M shares; company forecast; TTM confirmed 57.61 PLN
EPS_NOW           = 64.6       # FY2026E; mgmt guidance 636M PLN / 9.84M shares; Q1 2026 actual 145M PLN (+20% YoY) confirms trajectory
EPP               = round(EPS_NOW * EPP_MIN_PE, 2)   # 710.60 PLN

epp_gap_pct       = round((CURRENT_PRICE - EPP) / EPP * 100, 1)   # +62.5%

# ── METHOD B ───────────────────────────────────────────────────────────────
CONS_EPS_2YR  = 76.0           # FY2028E; FY2026E 64.6 × 1.085^2 ≈ 76; SELT full ramp + organic volume + operating leverage
CONS_EXIT_PE  = 17             # mid-cycle for Polish industrial; KTY historical 10-20x; Trigon bull case 19x; avg analyst ~14x
price_b       = round(CONS_EPS_2YR * CONS_EXIT_PE, 2)   # 1,292 PLN
ratio_b       = round((CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE), 2)   # 3.24x → AVOID

# ── SOFTMAX ENGINE ─────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  {"price": 400.0,  "eps": 40.0,  "pe": 10.0,
              "desc": "EU recession + CBAM fails + construction freeze; EPS near FY2020 trough"},
    "BASE":  {"price": 1292.0, "eps": 76.0,  "pe": 17.0,
              "desc": "Consensus FY2028E 76 PLN × 17x; SELT ramps; CBAM modest tailwind; mid-cycle re-rate"},
    "BULL":  {"price": 1672.0, "eps": 88.0,  "pe": 19.0,
              "desc": "CBAM accelerates EU aluminium re-shoring; SELT synergies exceed plan; 19x quality re-rate"},
    "XBULL": {"price": 2310.0, "eps": 105.0, "pe": 22.0,
              "desc": "EU industrial consolidation + peak margin expansion + dividend premium re-rating; 22x"},
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
    {"name": "CBAM tailwind (EU carbon border tax on imported aluminium)",
     "rating": +1.0, "weight": 0.25,
     "desc": ("CBAM entered full enforcement Jan 2026, levying embedded-carbon cost on aluminium "
              "imported from Turkey, China, Russia. KTY uses ~60% renewable energy — structural "
              "cost advantage vs non-EU smelters. EU aluminium profiles market share should migrate "
              "toward domestic processors through 2026-2028.")},
    {"name": "SELT acquisition synergies (sun protection systems)",
     "rating": +0.9, "weight": 0.20,
     "desc": ("SELT acquired 2024; manufactures pergolas, blinds, awnings. Q2 2025 revenue "
              "contribution 105M PLN; Aluminium Systems Segment +30% YoY, 23% EBITDA margin. "
              "Internal profile consumption rising from 2,000 to 6,000 t/yr — a 3× throughput "
              "multiplier for Extruded Products over 2025-2026.")},
    {"name": "Dividend discipline and management forecast reliability",
     "rating": +0.6, "weight": 0.20,
     "desc": ("Management publishes detailed annual forecasts. 2026 guidance: 636M PLN net profit, "
              "1,112M PLN EBITDA, 5,889M PLN revenue. 85% payout policy. FY2025 dividend 49.05 "
              "PLN/share (4.25% yield at 1,155 PLN). Q1 2026 actual 145M PLN beat guidance 132M "
              "by 10% — track record of conservative, deliverable targets.")},
    {"name": "EU construction cycle weakness",
     "rating": -0.7, "weight": 0.20,
     "desc": ("Sun protection (SELT) and facade systems (Aluprof) depend on new construction and "
              "renovation. EU construction in multi-year downturn: German permits -10% YoY; Polish "
              "residential slowing as mortgage rates remain elevated. Renovation capex deferral "
              "compresses SELT demand ramp and risks Aluminium Systems growth assumptions.")},
    {"name": "PLN/EUR currency translation risk",
     "rating": -0.4, "weight": 0.15,
     "desc": ("KTY reports in PLN; significant revenues are EUR-denominated (Western European "
              "exports). A 5% PLN appreciation vs EUR reduces EBITDA by ~3%. Polish NBP rate "
              "differential and political risk create FX volatility. Management uses rolling "
              "hedges but 18-24 month EUR export exposure remains structurally unhedged.")},
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
  Currency : ALL PRICES AND EPS IN {CURRENCY} (Polish Złoty)
  Sector   : Aluminium Processing · Building Systems · Flexible Packaging
  FY end   : {FY_END}
  Shares   : ~{SHARES_M:.2f}M outstanding
  Price    : PLN {CURRENT_PRICE:,.2f}  [2026-05-22]
  52-week  : PLN 799.50 low – PLN 1,179.00 high  (ATH hit May 6 2026; near ATH)
""")

    print("=" * 72)
    print(f"  PART 2 — ANALYST COMMENTARY  |  {TICKER}")
    print("=" * 72)
    print(f"""
  A. INVESTMENT THESIS
  ----------------------------------------------------------------------

  Grupa Kęty SA is Poland's dominant vertically-integrated aluminium
  processor — operating across three segments: Extruded Products
  (aluminium profiles for construction, automotive, HVAC), Aluminium
  Systems (facade systems, sun protection via the SELT and Aluprof
  brands), and Flexible Packaging (aluminium foil and laminate for food).

  The company has delivered stable, growing earnings for 15+ years, with
  a rigorous 85% payout policy and precise management guidance that has
  been met or exceeded consistently.  Q1 2026 net profit of 145M PLN beat
  the 132M PLN guidance by +10% (+20% YoY).  FY2026 management guidance:
  636M PLN net profit, 1,112M PLN EBITDA, 5,889M PLN revenue.

  Two structural catalysts distinguish 2026:
  — CBAM (EU Carbon Border Adjustment Mechanism): Full enforcement began
    Jan 2026, levying embedded-carbon costs on imported aluminium.  KTY
    uses ~60% renewable energy.  Non-EU smelters (Turkey, China) now bear
    a carbon surcharge, narrowing the price gap and restoring EU market
    share to domestic processors.
  — SELT acquisition: Acquired 2024; adds sun protection systems to the
    Aluminium Systems portfolio.  Q2 2025 contribution 105M PLN; segment
    +30% revenue at 23% EBITDA margin.  Internal profile throughput rises
    from 2,000 to 6,000 t/yr — a 3× multiplier for Extruded Products.

  Yet at PLN {CURRENT_PRICE:,.0f} — essentially AT the all-time high (1,179 PLN
  on May 6, 2026) — the market has already priced these catalysts.  The
  forward P/E stands at {CURRENT_PRICE/EPS_NOW:.1f}x FY2026E ({CURRENT_PRICE/CONS_EPS_2YR:.1f}x FY2028E), the
  UPPER end of KTY's historical 10–20x range.

  The average analyst 12-month price target is ~950 PLN — 18% BELOW the
  current price.  Only Trigon DM (raised to Buy, target 1,325 PLN in
  April 2026) sees further near-term upside.  Method B 2-year target of
  PLN {price_b:,.0f} implies only +{(price_b/CURRENT_PRICE-1)*100:.0f}% upside vs -65% BEAR downside.

  Signal: {sig}  |  Ratio B: {ratio_b:.2f}x  |  EPP gap: +{epp_gap_pct:.1f}%


  B. EARNINGS POWER PRICE (EPP) — STRUCTURAL FLOOR
  ----------------------------------------------------------------------

  EPS anchor   : PLN {EPS_TROUGH:.1f}  (FY2020; net profit 430.2M PLN / {SHARES_M}M shares;
                  historical EPS floor — paradoxically COVID year was strong)
  Bear trough  : PLN {EPS_TROUGH_PRICE:.2f}  (52-wk recent low; 2025 correction;
                  799.50 / 56.9 FY2025 EPS = 14.1x observed trough P/E)
  EPP min PE   : {EPP_MIN_PE}x  (structural floor; below 14.1x observed trough; recession/
                  BEAR scenario; appropriate for cyclical industrial)

  EPS now      : PLN {EPS_NOW:.1f}  (FY2026E; management guidance 636M PLN / {SHARES_M}M shares;
                  Q1 2026 actual 145M PLN = 14.7 PLN/sh on track for ~65 PLN FY)
  EPP floor    : PLN {EPS_NOW:.1f} × {EPP_MIN_PE}x = PLN {EPP:,.2f}
  Current vs EPP: PLN {CURRENT_PRICE:,.2f} vs PLN {EPP:,.2f}  (+{epp_gap_pct:.1f}% above floor)

  Note: EPP floor PLN {EPP:,.0f} is ~11% BELOW the 52-week low of PLN 799.50.
  The stock would need to fall -38% from current price before reaching EPP.


  C. METHOD B — 2-YEAR EARNINGS POWER TARGET
  ----------------------------------------------------------------------

  CONS_EPS_2YR : PLN {CONS_EPS_2YR:.1f}  (FY2028E; FY2026E {EPS_NOW:.1f} × 1.085² = 76;
                  SELT volume ramp + organic growth + operating leverage;
                  Q1 2026 beat trajectory supports ~8-9% CAGR through FY2028)
  CONS_EXIT_PE : {CONS_EXIT_PE}x  (mid-cycle; KTY historical range 10-20x; Trigon bull
                  case uses 19x; avg analyst target implies ~14x; 17x = conservative
                  but achievable at quality Polish industrial with CBAM moat)
  Method B     : PLN {CONS_EPS_2YR:.1f} × {CONS_EXIT_PE}x = PLN {price_b:,.2f}

  Ratio B = (PLN {CURRENT_PRICE:,.2f} − PLN {EPP:,.2f}) / (PLN {price_b:,.2f} − PLN {CURRENT_PRICE:,.2f})
           = PLN {CURRENT_PRICE-EPP:,.2f} / PLN {price_b-CURRENT_PRICE:,.2f}
           = {ratio_b:.2f}x  →  {sig}

  Sensitivity to exit PE (at CONS_EPS_2YR PLN {CONS_EPS_2YR:.1f}):
    CONS_EXIT_PE = 14x → Price_B PLN 1,064 → BELOW current price → N/A (AVOID)
    CONS_EXIT_PE = 15x → Price_B PLN 1,140 → Ratio B {(CURRENT_PRICE-EPP)/(1140-CURRENT_PRICE):.2f}x  (AVOID)
    CONS_EXIT_PE = 17x → Price_B PLN 1,292 → Ratio B {ratio_b:.2f}x  (AVOID)  ← base case
    CONS_EXIT_PE = 18x → Price_B PLN 1,368 → Ratio B {(CURRENT_PRICE-EPP)/(1368-CURRENT_PRICE):.2f}x  (HOLD/TRIM)
    CONS_EXIT_PE = 19x → Price_B PLN 1,444 → Ratio B {(CURRENT_PRICE-EPP)/(1444-CURRENT_PRICE):.2f}x  (WATCHLIST)
  Signal is robustly AVOID/HOLD at all plausible conservative exit multiples.
  Only at 19x+ (Trigon DM bull case) does the signal improve to WATCHLIST.


  D. SCENARIO ANALYSIS
  ----------------------------------------------------------------------
  Scenario     EPS      P/E    Price (PLN)  vs Now  Description
  ----------------------------------------------------------------------""")

    for k, s in SCENARIOS.items():
        vs = (s["price"] / CURRENT_PRICE - 1) * 100
        sign = "+" if vs >= 0 else ""
        print(f"  {k:<8}  PLN {s['eps']:5.1f}  {s['pe']:4.1f}x  PLN {s['price']:7,.0f}  {sign}{vs:5.1f}%  {s['desc']}")

    print(f"""
  BASE scenario PLN {price_b:,.0f} = Method B target (by construction).
  BEAR at PLN 400 requires EPS to fall below FY2020 actual (43.7 PLN) AND
  multiple compression to 10x — a genuine recession + CBAM failure scenario.
  BEAR probability is non-trivial for a cyclical industrial at ATH prices.


  E. SOFTMAX MARKET COMPOSITE
  ----------------------------------------------------------------------
""")
    print(f"  Market composite  (inferred from PLN {CURRENT_PRICE:,.2f}): {mkt_composite:.3f}")
    print(f"  SCA adjustment                                  : {sca_adj:+.3f}")
    print(f"  Model composite                                 : {model_composite:.3f}")
    print()
    print(f"  Scenario probabilities (model):")
    for k, p in model_probs.items():
        bar = "█" * int(p * 40)
        print(f"    {k:<8}  {p*100:5.1f}%  {bar}")

    ev_chg = (model_ev / CURRENT_PRICE - 1) * 100
    sign = "+" if ev_chg >= 0 else ""
    print(f"""
  Model EV (proxy) : PLN {model_ev:,.0f}  ({sign}{ev_chg:.1f}% vs current PLN {CURRENT_PRICE:,.2f})

  Interpretation: Market composite {mkt_composite:.2f} ≈ BASE centre (2.0) — market is
  pricing the BASE scenario as most likely. Despite positive model EV
  (+{ev_chg:.0f}%), the BEAR scenario (-65%) is ~{model_probs['BEAR']*100:.0f}% probable with only +{(SCENARIOS['BASE']['price']/CURRENT_PRICE-1)*100:.0f}% BASE
  upside. Risk/reward is deeply asymmetric: +{(SCENARIOS['BASE']['price']/CURRENT_PRICE-1)*100:.0f}% vs -65% for the two
  highest-probability outcomes. The positive EV is driven by the tail
  BULL and XBULL, not a favourable near-term entry point.


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


  G. EPS QUALITY DECOMP  (FY2025 PLN {EPS_FY2025:.1f} → FY2026E PLN {EPS_NOW:.1f} = +PLN {EPS_NOW - EPS_FY2025:.1f} = +{(EPS_NOW/EPS_FY2025-1)*100:.1f}%)
  ----------------------------------------------------------------------
  Component                                                      Share          Type
  ---------------------------------------------------------------------------------
  Organic volume growth — Extruded Products (higher throughput   32%    Structural
    from SELT pull-through; EU CBAM shifts demand to KTY profiles)
  SELT full-year ramp (2025 = partial year; FY2026 first full    32%    Structural
    year; Aluminium Systems targeting 105M PLN/quarter run-rate)
  Operating leverage (EBITDA margin 18.5% → 19%+; revenue       20%    Structural
    growing faster than fixed cost base; guidance 1,112M EBITDA)
  Flexible Packaging growth (food aluminium foil; stable         13%    Structural
    volumes + modest pricing; defensive cash generator)
  Net finance cost headwind (SELT acquisition debt financing;    -4%    Temporal
    net debt/EBITDA 1.3x; manageable but partial earnings drag)

  Structural :  97%
  Temporal   :   3%
""")

    print("=" * 72)
    print(f"  PART 3 — NUMBERS & SIGNALS   |  {TICKER}")
    print("=" * 72)
    print(f"""
  H. RISK / RETURN SUMMARY  (all amounts in PLN)
  ----------------------------------------------------------------------

  Current price       : PLN {CURRENT_PRICE:,.2f}  (ATH PLN 1,179 hit May 6 2026; near ATH)
  EPP floor           : PLN {EPP:,.2f}  (+{epp_gap_pct:.1f}% above floor; {EPP_MIN_PE}x × PLN {EPS_NOW:.1f} FY2026E)
  Method B target     : PLN {price_b:,.2f}  (upside: +{(price_b/CURRENT_PRICE-1)*100:.0f}%)
  BEAR scenario       : PLN 400  (downside: -{(1-400/CURRENT_PRICE)*100:.0f}%; recession + CBAM failure)
  Ratio B             : {ratio_b:.2f}x  -> {sig}
  Forward P/E         : {CURRENT_PRICE/EPS_NOW:.1f}x non-GAAP  (FY2026E PLN {EPS_NOW:.1f})
  FY2028E P/E         : {CURRENT_PRICE/CONS_EPS_2YR:.1f}x  (consensus FY2028E PLN {CONS_EPS_2YR:.1f})
  Historical PE range : 10–20x  (current {CURRENT_PRICE/EPS_NOW:.1f}x is UPPER band)
  Dividend yield      : {49.05/CURRENT_PRICE*100:.2f}%  (FY2025 div PLN 49.05/share; 85% payout policy)
  Market cap          : ~PLN 11.4B  (~{CURRENT_PRICE*SHARES_M/1000:.1f}B PLN at current price)
  Net debt/EBITDA     : 1.3x  (guided FY2026; PLN 1,488M net debt / PLN 1,112M EBITDA)
  FY2026 guidance     : Net profit 636M PLN, EBITDA 1,112M PLN, Revenue 5,889M PLN
  Q1 2026 actual      : Net profit 145M PLN (beat guidance 132M by +10%; +20% YoY)
  SELT contribution   : PLN 105M revenue Q2 2025; Aluminium Systems +30% YoY; 23% margin
  CBAM effective      : Jan 2026 — levies embedded-carbon cost on imported aluminium
  Analyst consensus   : Average target PLN ~950 (-18% vs current); 1 Bull (Trigon 1,325)
  52-week range       : PLN 799.50 – 1,179.00  (recent ATH May 6 2026)
  Q2 2026 catalyst    : ~Aug 2026 (H1 2026 results; CBAM benefit visibility, SELT ramp)
  AVOID thesis breaks if: Method B exit PE sustainably re-rates to 20-22x (CBAM moat
                          premium), OR FY2028E EPS upgrades to 88-90 PLN (BULL scenario).
  ACCUMULATE trigger  : Pullback to PLN 850–950 (EPP +20-35% buffer; ~14x FY2026E = observed trough multiple)


  I. IDIOSYNCRATIC vs MACRO DRIVERS
  ----------------------------------------------------------------------
  Beta: 0.85x  |  Idiosyncratic: 55%  |  Macro: 45%

  Driver                                                 Type    Wt  Note
  ────────────────────────────────────────────────────────────────────────────────────────────
  CBAM enforcement and EU aluminium market share shift   IDIO   25%  Monthly EU import data (volumes from Turkey/China) will show whether
  SELT integration revenue ramp (target 6,000 t/yr)     IDIO   20%  Quarterly Aluminium Systems revenue + EBITDA margin is the key score
  Management guidance delivery (quarterly tracking)     IDIO   10%  KTY has consistently met or beaten published forecasts; any miss
  EU construction cycle — permits + residential starts  MACRO  25%  German, Polish, Czech construction stats are leading indicators for
  Aluminium LME price cycle                             MACRO  10%  KTY is a processor (buys raw Al, sells profiles) — spread matters more
  PLN/EUR exchange rate                                 MACRO  10%  5% PLN appreciation ≈ 3% EBITDA headwind; NBP policy key variable
""")

    print("=" * 72)
    print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-22")
    print("=" * 72)


if __name__ == "__main__":
    run_report()
