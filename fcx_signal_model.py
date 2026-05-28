"""
fcx_signal_model.py — Freeport-McMoRan Inc. (NYSE: FCX)
World's largest publicly traded copper company. Grasberg + Americas. AI copper thesis.
Signal framework: EPP floor + Method B + SCA softmax engine.
"""

import math

# ── LIVE PRICE (fetched before model construction) ──────────────────────────
CURRENT_PRICE = 63.63    # FCX — fetched from Yahoo Finance, 2026-05-28
# (~$63.63 close May 27, 2026; 52-wk low $35.15, 52-wk high $70.97)
# Market cap ~$91.4B; shares ~1,437M; P/E ~27× FY2026E; dividend ~$0.60/yr run-rate
# Copper at ~$5.79/lb COMEX avg Q1 2026 (all-time highs); COMEX 28% premium to LME

TICKER        = "FCX"
COMPANY       = "Freeport-McMoRan Inc."
SHARES_M      = 1437         # million diluted shares (~1,437M as of Q1 2026)
DIVIDEND_ANN  = 0.60         # USD/yr run-rate: $0.30 base + ~$0.30 variable (performance-based)
                              # Variable dividend = 50/50 policy; scales with FCF / copper price

# ── EPS CONVENTION ───────────────────────────────────────────────────────────
# Adjusted Net Income Attributable to Common Stock Per Share (FCX non-GAAP).
# Excludes: mark-to-market adjustments (copper/gold collars), restructuring,
# unusual tax items, and acquisition/divestiture charges.
# EPS is HIGHLY sensitive to copper price: every $0.10/lb copper swing = ~$100-140M/yr net income.
# Grasberg production profile creates additional EPS volatility (gold byproduct credit).

EPS_HISTORY = {
    "FY2022": 2.43,    # Strongest year in decade; copper $4.20/lb avg; Grasberg producing normally;
                        # H1 (copper spike $4.90/lb): Q1 $1.07 + Q2 $0.58; H2 correction: Q3 $0.26 + Q4 $0.52
    "FY2023": 1.53,    # -37% YoY; copper $3.80/lb avg; Grasberg underground ramp challenges;
                        # leaching technology program initiated (~200M lbs incremental target)
    "FY2024": 1.48,    # Roughly flat; copper $4.15/lb avg; Americas strong; Grasberg block cave ramping;
                        # leaching technology adding ~250-300M lbs/yr; unit cash costs $1.65/lb
    "FY2025": 1.52,    # +2.7% YoY; copper $4.20/lb avg; September 2025 mudflow/mud rush at
                        # Grasberg Block Cave = major underground incident; PTFI production cut ~40%;
                        # Americas compensated; full year unit costs $1.65/lb within guidance
}

# Q1 2026 (Apr 23, 2026): Adj EPS $0.57 (+21% beat vs $0.47E); revenue $6.23B (+9.3% beat)
# Adj EBITDA $2.47B (+24% beat); copper realization $5.78/lb (COMEX all-time high)
# Consolidated copper sold 657M lbs; gold sold 121K oz; moly 24M lbs
# Indonesia/Grasberg: only 82M lbs Cu sold (vs 290M lbs Q1 2025) — mine still recovering
# Americas compensated: Americas operating income was 2.5× higher YoY
# Idle facility / mine restoration costs: $406M in Q1 (excluded from unit cash costs)

# FY2026 guidance (as of Q1 earnings, Apr 23, 2026):
#   Copper sales: ~3.1B lbs (cut from prior 3.4B guide; Grasberg GBC bottleneck delays)
#   Gold sales: ~650K oz
#   Operating CF (at ~$6/lb Cu): ~$8.7B
#   Capex: ~$4.3B (Grasberg recovery + leaching/Americas expansion)
#   H2 2026: ~30% more copper, ~50% more gold than H1 (Grasberg ramp recovering)
#   Grasberg target: 65% of nameplate in H2 2026; full capacity end-2027 (FCX) / early 2028 (PTFI)
#   US tariff COMEX premium benefit: ~$1.6B/yr incremental at current 28% premium

EPS_NOW       = 2.32     # FY2026E analyst consensus; Q1 $0.57 on-track;
                          # copper at $6/lb offsets Grasberg volume shortfall;
                          # H2 2026 volume ramp should support this; conservative for $6/lb copper
EPS_TROUGH    = 0.75     # severe copper downturn scenario: copper falls to ~$3.50/lb
                          # (vs current $6/lb; a -42% correction to near 2016 bear market levels)
                          # At $3.50/lb with $1.65/lb cash costs: margins severely compressed;
                          # Context: FY2023 = $1.53 at $3.80/lb copper; $0.75 at $3.50/lb is realistic
                          # Note: at $3.00/lb (extreme), EPS approaches zero — EPP floor holds asset value
EPP_MIN_PE    = 20        # world-class strategic asset; clean balance sheet — see rationale below
EPP           = EPP_MIN_PE * EPS_TROUGH   # = $15.00

CONS_EPS_2YR  = 3.86     # FY2027E consensus; assumes partial Grasberg recovery toward full capacity;
                          # copper at ~$5.50-6.00/lb structural support; leaching adds ~300M lbs
CONS_EXIT_PE  = 22        # copper miners at recovery: 18-22× as structural demand premium justified
                          # AI data center + EV + grid electrification = demand compounding above cycle
price_b       = CONS_EPS_2YR * CONS_EXIT_PE   # = $84.92 → $85.00
price_b       = 85.00

ratio_b       = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
epp_gap_pct   = (CURRENT_PRICE - EPP) / EPP * 100

# Scenario prices (2-year forward targets)
scenarios = {
    "BEAR":   15,    # EPP; copper $3.50/lb + Grasberg delays + recession; $0.75 × 20×
    "BASE":   50,    # copper at $5.00/lb; partial Grasberg ramp; ~$2.50/sh × 20×
    "BULL":   85,    # Method B; FY2027E $3.86 × 22×; full Grasberg + copper $5.50-6/lb
    "XBULL": 120,    # structural deficit: full Grasberg + copper $6.50-7/lb; $5.50/sh × 22×
}

# ── SOFTMAX ENGINE ───────────────────────────────────────────────────────────
T = 0.60
CENTRES = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}

def softmax_weights(composite):
    logits = {k: -((composite - c) ** 2) / T for k, c in CENTRES.items()}
    max_l  = max(logits.values())
    exps   = {k: math.exp(v - max_l) for k, v in logits.items()}
    total  = sum(exps.values())
    return {k: v / total for k, v in exps.items()}

def expected_price(composite):
    w = softmax_weights(composite)
    return sum(w[k] * scenarios[k] for k in scenarios)

def infer_composite(target_price, lo=1.0, hi=4.0, iterations=60):
    for _ in range(iterations):
        mid = (lo + hi) / 2
        if expected_price(mid) < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

market_composite = infer_composite(CURRENT_PRICE)

# ── SCA — SIGNAL CATALYST ADJUSTMENTS ───────────────────────────────────────
sca_items = [
    # (description, score, weight)
    ("AI/electrification structural copper demand: each AI data centre requires "
     "30,000-50,000 tonnes copper; global hyperscale buildout 2026-2030 is unprecedented. "
     "EVs need 6× more copper than ICE vehicles; grid electrification, offshore wind, "
     "heat pumps all accelerating. Copper supply response is constrained: 10-15yr mine "
     "development timeline + declining ore grades = structural deficit.",
     +0.35, 0.25),
    ("US copper tariff windfall: COMEX-LME premium ~28% due to 50% US import tariffs. "
     "FCX produces ~70% of US refined copper and ~1.4B lbs/yr at COMEX prices. "
     "Each $0.10/lb COMEX premium = ~$70M incremental annual profit. "
     "At current premium: ~$1.6B/yr incremental vs pre-tariff. Uniquely domestic.",
     +0.30, 0.20),
    ("Grasberg recovery catalyst: full production end-2027 (FCX target) = step-change "
     "from 1.0B lbs/yr to 1.6B lbs Cu + 1.3M oz Au/yr — EPS potentially $5-7+. "
     "Life-of-resource MOU with Indonesia removes long-tail political risk. "
     "H2 2026 30% more copper than H1 = recovery momentum building.",
     +0.25, 0.15),
    ("Copper at $6/lb is near all-time highs; mean reversion risk is material. "
     "China slowdown, trade war de-escalation (collapsing COMEX premium), or global "
     "recession could bring copper to $4/lb → FCX EPS ~$1.00-1.25/sh. Stock near "
     "52-wk high; only 10% from $70.97 ATH; Morgan Stanley downgraded April 2026.",
     -0.35, 0.25),
    ("Grasberg operational uncertainty: PTFI (Indonesian JV partner) says early 2028; "
     "FCX says end-2027 — a 6-month disparity. Q1 2026 Indonesia copper only 82M lbs "
     "vs 290M lbs a year prior. Any further underground incidents (wet ore management, "
     "infrastructure) would push the catalyst further right and erode confidence.",
     -0.25, 0.15),
]

sca_raw = sum(score * weight for _, score, weight in sca_items)
sca_adj = sca_raw / 2.0
adj_composite = market_composite + sca_adj

adj_weights    = softmax_weights(adj_composite)
expected_px    = expected_price(adj_composite)

# ── SIGNAL ───────────────────────────────────────────────────────────────────
if   ratio_b < 0.75:  signal = "◉ BUY"
elif ratio_b < 1.10:  signal = "◎ ACCUMULATE"
elif ratio_b < 1.75:  signal = "◐ WATCHLIST"
elif ratio_b < 2.50:  signal = "▷ HOLD/TRIM"
else:                  signal = "✕ AVOID"

# ── OUTPUT ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    SEP  = "=" * 70
    DASH = "─" * 70

    print(SEP)
    print("FREEPORT-McMoRan INC. (FCX) — SIGNAL MODEL")
    print("World's largest publicly traded copper company. Grasberg + Americas.")
    print(SEP)

    print("""
SIGNAL FRAMEWORK — METHOD B + SCA ENGINE
─────────────────────────────────────────
EPP  = EPS_TROUGH × EPP_MIN_PE          (structural floor; adjusted EPS basis)
Ratio B = (Price − EPP) / (price_b − Price)

FCX EPS convention: Adjusted Net Income Attributable to Common Stock per Share.
Excludes mark-to-market adjustments on derivatives, restructuring, unusual tax
items, and acquisition-related charges. GAAP EPS can differ meaningfully due to
commodity derivative MTM swings. EPS is HIGHLY sensitive to copper price:
each $0.10/lb copper change = ~$100-140M net income (~$0.07/sh impact).
Gold byproduct credits (from Grasberg) also significantly affect unit cash costs.

SIGNAL THRESHOLDS
  Ratio B < 0.75   →  ◉ BUY
  0.75 – 1.10      →  ◎ ACCUMULATE
  1.10 – 1.75      →  ◐ WATCHLIST
  1.75 – 2.50      →  ▷ HOLD/TRIM
  > 2.50           →  ✕ AVOID

EPP_MIN_PE = 20×  rationale:
  FCX is a commodity company — EPS volatility is extreme (from near-zero at
  $3/lb copper to $5-7/sh at full Grasberg + $6/lb copper). However, the EPP
  floor reflects what the stock trades for even at EPS trough because:
  (1) ASSET VALUE FLOOR: Grasberg is one of the world's largest copper-gold
      deposits. The long-term NPV of future production (decades of reserves)
      provides a valuation floor that is ASSET-BASED, not earnings-based.
      Even at trough earnings, the market prices FCX on mine NAV, not current EPS.
  (2) CLEAN BALANCE SHEET: Net debt $2.3B vs $8.7B operating CF at $6/lb.
      Contrast with 2016 (near-bankruptcy fear with $20B gross debt). The
      current FCX cannot be threatened with bankruptcy even at $3.50/lb copper.
      This eliminates the 2016-style trough discount and supports 20× floor.
  (3) STRUCTURAL COPPER DEMAND: Even bearish analysts don't project copper
      staying at $3.50/lb for more than 1-2 years. AI data centre buildout,
      EV adoption, grid electrification = demand growing 3-5%/yr while mine
      supply response takes 10-15 years. Trough multiples reflect recovery certainty.
  (4) US STRATEGIC ASSET: FCX's Americas operations (Morenci, Cerro Verde,
      Chino + leaching technology) produce ~1.4B lbs/yr of US copper — strategic
      in a world of reshoring and critical mineral supply chain security. This
      introduces a policy/strategic floor premium.
  20× trough = appropriate for a world-class strategic asset with a clean
  balance sheet and a commodity whose structural demand case is unambiguous.
  Note: 2016 trough ($3.52 stock) reflected $20B debt + near-zero EPS. Today's
  $2.3B net debt eliminates that scenario — $15 EPP floor is conservative but real.
""")

    print("FREEPORT-McMoRan INC. (FCX) — THE ESSENTIAL METAL OF THE ELECTRIFICATION ERA")
    print("=" * 70)

    print("""
BUSINESS OVERVIEW
─────────────────
Freeport-McMoRan was incorporated in 1987 and is headquartered in Phoenix, Arizona.
It is the world's largest publicly traded copper producer (~4B+ lbs Cu/yr at
full capacity) and a major gold producer (via Grasberg). CEO: Kathleen Quirk
(since January 2023; CFO for decades; deep operational and capital allocation
expertise). Market cap: ~$91B at $63.63.

FCX is a PURE-PLAY copper company (post-2016 oil/gas divestiture). Its earnings
are the most direct proxy for the copper price of any large-cap in the S&P 500.
The business has two distinct engines that together create the investment thesis:

  (1) AMERICAS: Reliable, large-scale, low-cost US + Peru copper production
  (2) GRASBERG: The world's most valuable single copper-gold mine — currently
      impaired but recovering; full ramp = step-change EPS event

THREE SEGMENTS
──────────────────────────────────────────────────────────────────────

  NORTH AMERICA  (~45% of copper production; MOST RELIABLE)
  ──────────────────────────────────────────────────────────────────────
  Large-scale open-pit and leach copper mines across the US Southwest:
    Morenci (Arizona)    — largest copper mine in North America; ~900M lbs/yr
    Bagdad, Sierrita, Chino, Tyrone, Safford (Arizona/New Mexico) — portfolio
  Target: ~1.4B lbs copper in FY2026; performing at/above plan.

  US operations sell primarily at COMEX prices. With the current 50% US copper
  import tariff, COMEX trades at a ~28% premium to LME → Americas operations
  earn ~$1.6B/yr more than they would at LME prices. FCX is the ONLY major
  domestic US copper producer capable of capturing this full premium at scale.

  LEACHING TECHNOLOGY BREAKTHROUGH (transformational for Americas):
  Traditional copper mines leave significant copper in oxide ore that can't
  be economically extracted by conventional smelting. FCX's proprietary
  leaching technology uses enhanced acid application to recover this copper:
  Target: 300M additional lbs/yr from otherwise-unrecoverable ore
  Economics: VERY low incremental cost ($0.40-0.60/lb vs $1.65/lb average)
  This is effectively adding a new mid-size copper mine without building one.
  Q1 2026: ~78M lbs from leaching technology (annualised ~310M lbs); on track.

  SOUTH AMERICA  (~15% of copper production; CERRO VERDE, PERU)
  ──────────────────────────────────────────────────────────────────────
  Cerro Verde: large open-pit copper mine near Arequipa, Peru
  FCX owns 53.56%; operator; ~700M lbs Cu/yr
  Peru country risk (political strikes, regulatory uncertainty) is manageable
  but occasionally creates noise. Not a primary investment thesis driver.

  INDONESIA / PT FREEPORT INDONESIA (PTFI)  — THE CROWN JEWEL
  ──────────────────────────────────────────────────────────────────────
  Grasberg is the world's premier copper-gold porphyry deposit:
    Location: Remote Papua (formerly Irian Jaya), Indonesia; altitude 4,200m
    Scale: 10-20B lbs copper equivalent reserves; decades of mine life
    FCX's stake: 48.76% of PTFI (post-2018 divestiture to Inalum/Indonesia)
    Operating rights: Recently extended via MOU for LIFE OF RESOURCE
      (FCX retains 48.76% through 2041; transfers 12% at no cost post-2041)

  GRASBERG TRANSITION (from open pit to underground — the defining event):
  The original Grasberg Open Pit (one of the largest open-pit mines on Earth)
  was exhausted ~2019. The mine transitioned to the Grasberg Block Cave (GBC)
  underground system — one of the most ambitious underground mining projects ever:
    Nameplate capacity: ~1.6B lbs Cu/yr + ~1.7M oz Au/yr (at full ramp)
    Underground infrastructure: miles of tunnels, massive drawpoint system
    Production to date: ramping; reached ~1.5B lbs Cu/yr annualised by mid-2025

  SEPTEMBER 2025 — THE MUDFLOW INCIDENT (why FCX earnings fell):
  A catastrophic underground mudflow/mud rush at the GBC caused partial
  collapse of key drawpoints. This immediately cut PTFI production by ~40%.
  Timeline to recovery:
    H2 2026: 65% of nameplate (per FCX latest guidance)
    End-2027: FCX target for full capacity
    Early 2028: PTFI's (more conservative) estimate
  This 6-12 month delay is the primary near-term risk and the reason the stock
  traded from $70+ to a 52-wk low of $35.15 (Oct-Dec 2025 panic).

  Q1 2026 PTFI: only 82M lbs Cu sold (vs. 290M lbs Q1 2025) — the recovery
  is clearly still early stage. But H2 2026 guidance of 30% more copper
  than H1 confirms the recovery trajectory is real.

  WHY GRASBERG MATTERS SO MUCH:
  At FULL capacity, Grasberg contributes:
    ~1.6B lbs Cu × FCX's 48.76% share = ~780M lbs Cu net to FCX
    ~1.3M oz Au × 48.76% = ~630K oz Au net (gold credit vs cash costs)
    At $6/lb Cu + $3,000/oz Au: this segment alone = ~$3-4B EBITDA/yr to FCX
  At CURRENT impaired capacity: contributing ~$500M-1B EBITDA/yr to FCX
  The gap between impaired and full = the recovery upside the market is pricing.

COPPER: THE METAL OF THE ELECTRIFICATION ERA
──────────────────────────────────────────────
Copper is not a commodity like iron ore or coal. It is the irreplaceable
conductive metal of the energy transition and AI infrastructure buildout:

  AI DATA CENTRES:
    A single hyperscale AI data centre requires 30,000-50,000 tonnes of copper
    (wiring, busbars, cooling systems, power distribution). Microsoft, Google,
    Amazon, and Meta are building 100+ data centres each over the next 5 years.
    If 500 major data centres are built 2025-2030, that's 15-25M tonnes of
    copper demand — equal to several years of global production.

  ELECTRIC VEHICLES:
    An EV requires ~83kg copper (vs ~23kg for ICE vehicle); EV charging
    infrastructure requires 10× more copper per station than gasoline pumps.
    Global EV penetration 10% → 50% over 10 years = sustained demand surge.

  GRID ELECTRIFICATION:
    Offshore wind farms, solar installations, transmission line upgrades,
    and substation rebuilds are all copper-intensive. The US alone announced
    $60B+ in grid investment under the Infrastructure Act.

  SUPPLY CONSTRAINT:
    New copper mines take 10-15 years from discovery to production.
    Declining ore grades: average copper ore grade has fallen from 2% in 1990
    to ~0.45% today. Every tonne of copper requires processing 2-4× more rock.
    Permitting delays: new mine approvals take 7-10 years in developed countries.
    Result: structural supply deficit estimated at 4-8M tonnes/yr by 2030.

  FCX'S POSITION: As the world's largest publicly traded producer with
  established operations, FCX cannot be replicated. No new mine can be
  permitted, built, and ramped to Morenci/Grasberg scale in the 2020s.
  FCX benefits directly and immediately from every dollar increase in copper.

US TARIFF WINDFALL — THE 2026 NEAR-TERM CATALYST
──────────────────────────────────────────────────
The 50% US copper import tariff created an unprecedented COMEX-LME spread:
  LME (global): ~$4.50/lb
  COMEX (US): ~$5.79/lb (Q1 2026 avg; ~28% premium)
  FCX's Americas production: ~1.4B lbs/yr sold at COMEX prices
  Incremental benefit vs. LME: ~$1.28/lb × 1.4B lbs = ~$1.79B/yr pretax
  After-tax benefit: ~$1.3-1.5B/yr = ~$0.90-1.05/sh incremental EPS

This tariff benefit is NOT in the FY2023-FY2025 historical earnings.
It is partially in FY2026E ($2.32 consensus). If the tariff persists at
current levels, it alone justifies a significantly higher EPS run-rate.

FINANCIAL PROFILE: FORTRESS BALANCE SHEET
──────────────────────────────────────────
  FY2025 Revenue:          $25.9B    (record; copper + gold volumes)
  Adj EBITDA (FY2025):     ~$9.9B    (record; copper price + Americas strength)
  OCF (FY2026E at $6/lb):  ~$8.7B   (management guidance)
  Capex FY2026:            ~$4.3B    (Grasberg recovery + leaching)
  Free Cash Flow FY2026:   ~$4.4B   ($8.7B - $4.3B)
  Net debt:                ~$2.3B   (vs $20B gross in 2016 crisis — transformed)
  New credit facility:     $3.0B    (revolving; matures 2031; secured May 14, 2026)
  Buyback authorization:   ~$2.9B   remaining (1.7M shares repurchased Q1 at $93M)
  Share count:             ~1,437M  diluted
  Annual dividend:         ~$0.60   ($0.30 base + ~$0.30 variable at current levels)

The 2016-era bankruptcy concerns were driven by ~$20B debt with near-zero copper
prices. Today, FCX has $2.3B net debt and $8.7B operating CF — even at $4/lb
copper ($3.5B operating CF), capex can be easily funded and debt serviced.
This clean balance sheet changes the trough scenario fundamentally.

Q1 2026 — RECORD COPPER PRICES + AMERICAS EXECUTION
─────────────────────────────────────────────────────
  Adj EPS:          $0.57   (+21% beat vs $0.47 estimate)
  Revenue:          $6.23B  (+9.3% beat)
  Adj EBITDA:       $2.47B  (+24% beat)
  Copper realization: $5.78/lb  (COMEX all-time high; Q1 avg)
  Americas copper: Very strong (+2.5× Americas operating income YoY)
  Indonesia copper: 82M lbs sold (vs 290M lbs Q1 2025; recovery in progress)
  Grasberg restoration costs: $406M one-time (excluded from unit costs)
  Unit net cash costs: $1.91/lb (elevated due to low Grasberg volumes)
  Balance sheet: Net debt stable at ~$2.3B; $2.9B buyback remaining

KEY CONTEXT: The Q1 beat was Americas + copper price driven, NOT Grasberg.
When Grasberg recovers (H2 2026 → end-2027), that is INCREMENTAL to this base.
""")

    print(DASH)
    print("EPS HISTORY  (Adjusted Net Income per Diluted Share, non-GAAP)")
    print(DASH)
    for yr, eps in EPS_HISTORY.items():
        print(f"  {yr}  ${eps:.2f}")
    print(f"  FY2026E ${EPS_NOW:.2f}  (consensus; copper $5.5-6/lb; Grasberg recovering; H2 volume ramp)")
    cagr_3yr = (EPS_HISTORY["FY2025"] / EPS_HISTORY["FY2022"]) ** (1/3) - 1
    print(f"  FY2022–FY2025 CAGR: {cagr_3yr*100:.1f}%/yr  (copper price decline from $4.50 → $4.20/lb; Grasberg ramp)")
    print(f"  NOTE: FY2022 = last full-capacity Grasberg year; FY2023-25 = ramp/incident period")

    print(f"""
EPP CALCULATION
  EPS_TROUGH × EPP_MIN_PE  =  ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×  =  ${EPP:.2f}
  (Assumes copper falls to ~$3.50/lb — a -42% drop from current $6/lb;
   FCX's Americas + leaching still generating positive cash; no solvency risk)
  Context: FY2016 near-zero EPS was due to $20B debt (now $2.3B) + $2.10/lb copper
  EPP buffer: current ${CURRENT_PRICE:.2f} is +{epp_gap_pct:.1f}% above EPP
  (HIGH EPP GAP is EXPECTED for cyclical commodity companies at high copper prices)

METHOD B  (2-year forward)
  CONS_EPS_2YR × CONS_EXIT_PE  =  ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×  =  ${price_b:.2f}
  (FY2027E assumes Grasberg recovering toward full capacity + copper $5.5-6/lb;
   22× exit = structural demand premium vs historical copper miner PEs of 15-18×)

RATIO B  (PRIMARY SIGNAL)
  (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})
  = ${CURRENT_PRICE - EPP:.2f} / ${price_b - CURRENT_PRICE:.2f}
  = {ratio_b:.3f}×   →   {signal}
  Near 52-wk high; Method B only 34% above current; Grasberg recovery is priced in

COPPER PRICE SENSITIVITY (approximate; at current volume assumptions)
  Copper $3.50/lb   →  Adj EPS ~$0.75/sh    EPP scenario
  Copper $4.00/lb   →  Adj EPS ~$1.00-1.25/sh
  Copper $5.00/lb   →  Adj EPS ~$1.75-2.00/sh
  Copper $5.79/lb   →  Adj EPS ~$2.32/sh    FY2026E consensus (current spot)
  Copper $6.00/lb + Grasberg recovery  →  Adj EPS ~$3.50-4.00/sh
  Copper $6.00/lb + Grasberg FULL      →  Adj EPS ~$5.00-7.00/sh  XBULL

SCENARIO PRICES
  BEAR     ${scenarios['BEAR']:>7.2f}   EPP; copper $3.50/lb + Grasberg delays + recession
  BASE     ${scenarios['BASE']:>7.2f}   copper $5.00/lb; partial Grasberg; ~$2.50/sh × 20×
  BULL     ${scenarios['BULL']:>7.2f}   Method B; FY2027E $3.86 × 22×; full Grasberg + copper $5.5-6/lb
  XBULL    ${scenarios['XBULL']:>7.2f}   structural deficit; full Grasberg; copper $6.5-7/lb; $5.50/sh × 22×
""")

    print("SOFTMAX COMPOSITE ENGINE")
    print(f"  Market composite (inferred)  =  {market_composite:.3f}")
    print(f"  (Market pricing between BASE-BULL — copper bull + Grasberg recovery anticipated)")

    print(f"""
SCA — SIGNAL CATALYST ADJUSTMENTS""")
    for desc, score, wt in sca_items:
        sign = "+" if score >= 0 else ""
        print(f"  {desc[:55]:<55}  {sign}{score:.2f} × {wt:.2f}  =  {score*wt:+.4f}")

    print(f"""
  sca_raw     =  {sca_raw:.4f}
  sca_adj     =  {sca_adj:.4f}  (= sca_raw / 2.0)
  adj_composite  =  {market_composite:.3f}  +  {sca_adj:.4f}  =  {adj_composite:.3f}
  (Net positive SCA: structural AI/electrification demand + US tariff windfall
   outweigh copper mean-reversion and Grasberg operational risks near-term)
""")

    print("SOFTMAX SCENARIO WEIGHTS  (at adj_composite = {:.3f})".format(adj_composite))
    for k, w in adj_weights.items():
        print(f"  {k:<10} {w*100:>5.1f}%   ${scenarios[k]:.2f}")

    ep_price = sum(adj_weights[k] * scenarios[k] for k in scenarios)
    print(f"\n  Expected price (probability-weighted)  =  ${ep_price:.2f}")

    print(f"""
BUSINESS METRICS
  FY2025 revenue                  = $25.9B   (record; copper + gold volumes)
  FY2025 adj EBITDA               = ~$9.9B   (record)
  FY2026E operating CF (at $6/lb) = ~$8.7B   (management guidance)
  FY2026E capex                   = ~$4.3B   (Grasberg recovery + leaching)
  FY2026E FCF                     = ~$4.4B   (before dividends/buybacks)
  Net debt (Q1 2026)              = ~$2.3B   (vs $20B gross in 2016; transformed)
  Copper production (FY2026E)     = ~3.1B lbs (guidance; vs 4.0-4.5B at full capacity)
  Gold production (FY2026E)       = ~650K oz  (vs 1.3-1.7M oz at full Grasberg)
  US copper market share          = ~70%      (dominant domestic producer)
  US tariff premium benefit       = ~$1.6B/yr (at current 28% COMEX-LME spread)
  Leaching technology             = ~300M lbs/yr incremental target (low-cost addition)
  Buyback authorization remaining = ~$2.9B
  Analyst consensus               = Buy (~80%); avg PT $70-72; high $81, low $39
  52-wk low $35.15 (Oct-Dec 2025) = BUY at ratio_b 0.40× (Grasberg panic)
  52-wk high $70.97               = AVOID at ratio_b 3.99×
  FY2026 guidance cut (Apr 2026)  = 3.1B lbs (from 3.4B; Grasberg GBC bottleneck)
  Morgan Stanley downgraded (Apr 2026) on Grasberg timeline concerns
  Life-of-resource MOU signed (2026): FCX retains 48.76% through 2041 → Indonesia 63% post-2041

SIGNAL ENTRY GUIDE""")

    thresholds = {}
    for label, rb in [("AVOID", 2.50), ("HOLD", 1.75), ("WATCH", 1.10), ("ACCUM", 0.75)]:
        thresholds[label] = (rb * price_b + EPP) / (1 + rb)

    print(f"  ✕ AVOID      above  ${thresholds['AVOID']:>3.0f}  (ratio_b > 2.50×)")
    print(f"  ▷ HOLD/TRIM  ${thresholds['HOLD']:>3.0f} – ${thresholds['AVOID']:>3.0f}  (ratio_b 1.75–2.50×)  ← current ${CURRENT_PRICE:.2f}  {signal}")
    print(f"  ◐ WATCHLIST  ${thresholds['WATCH']:>3.0f} – ${thresholds['HOLD']:>3.0f}  (ratio_b 1.10–1.75×)")
    print(f"  ◎ ACCUMULATE ${thresholds['ACCUM']:>3.0f} – ${thresholds['WATCH']:>3.0f}  (ratio_b 0.75–1.10×)")
    print(f"  ◉ BUY        below  ${thresholds['ACCUM']:>3.0f}  (ratio_b < 0.75×)")

    lo52 = 35.15
    rb52lo = (lo52 - EPP) / (price_b - lo52)
    hi52 = 70.97
    rb52hi = (hi52 - EPP) / (price_b - hi52)
    print(f"""
  52-wk low $35.15 (Oct-Dec 2025 Grasberg panic) = ◉ BUY at ratio_b {rb52lo:.2f}×.
  52-wk high $70.97 = AVOID at ratio_b {rb52hi:.2f}×; above AVOID threshold of $65.
  Analyst avg PT $70-72 = just inside AVOID zone — consensus is already near Method B.
  COPPER CYCLE THESIS: Every previous copper bear (2015-16, 2019-20) has been followed
  by a recovery to new highs. The AI/electrification demand floor is structurally higher
  than any prior cycle. Buy the NEXT copper correction, not the top.
  GRASBERG CATALYST WATCH: Any H2 2026 production update showing >65% nameplate
  capacity = near-term re-rating catalyst. Formal end-2027 recovery confirmation = BULL.
  ACCUMULATE on copper correction ($45-52): best risk/reward when copper pulls to $4.50-5/lb.
  BUY ZONE ($32-45): next full copper bear cycle entry. Patience over impulse.""")
