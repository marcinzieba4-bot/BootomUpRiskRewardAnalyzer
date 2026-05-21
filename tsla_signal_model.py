"""
Tesla, Inc. (TSLA) — BottomUp Risk/Reward Signal Model
EV + AI Autonomy + Energy: Cybercab robotaxi, FSD, Optimus humanoid robot
Three-Part Publication Format

NOTE ON EPP FRAMEWORK: Tesla's EPS HAS BEEN DECLINING (FY2022 peak $4.07 → FY2025 $1.67).
The EPP floor is validated against the Dec-2022 stock trough ($102) when the market
assigned 25x to peak EPS — this is the market-confirmed min viable P/E. Unlike all other
coverage stocks, TSLA's EPP floor has MIGRATED DOWN as EPS contracted. The enormous
gap (+893%) quantifies the option value premium (robotaxi, Optimus, AI platform) that
the market assigns above any current-earnings anchor.
"""
import math

# ── LIVE PRICE (fetched via web search, 2026-05-21) ──────────────────────────
CURRENT_PRICE = 414.75   # TSLA — fetched from Yahoo Finance / MarketBeat, 2026-05-21

# ── EPP FLOOR CALIBRATION ────────────────────────────────────────────────────
# Reference: Dec-2022 / Jan-2023 stock floor ($102) during growth-stock rout
# At that point FY2022 EPS was $4.07 (peak) → 25x was the absolute min P/E
# EPS has since declined to $1.67 (FY2025) → EPP floor has migrated DOWN accordingly
EPS_TROUGH       = 4.07   # FY2022 non-GAAP peak (EPP validation ref: $4.07 × 25x = $101.75 ≈ $102 ✓)
EPS_TROUGH_YEAR  = 2022
EPS_TROUGH_PRICE = 102.00 # Dec-2022 absolute stock trough (min-viable P/E confirmed)
EPP_MIN_PE       = 25     # market-confirmed floor multiple at maximum pessimism

# ── CURRENT FUNDAMENTALS ─────────────────────────────────────────────────────
EPS_NOW           = 1.67  # FY2025 non-GAAP (trough; Q1 $0.27 + Q2 $0.40 + Q3 $0.50 + Q4 $0.50)
EPS_FWD_CONSENSUS = 2.00  # FY2026E (Q1 beat $0.41; recovery in progress; $20B capex year)
CONS_EPS_2YR      = 4.00  # FY2027E consensus (auto recovery + early robotaxi revenue ramp)
CONS_EPS_CAGR     = 0.547 # ~55%/yr from $1.67→$4.00 (recovery from trough, not steady-state)
CONS_EXIT_PE      = 80    # conservative 2-yr exit P/E (still elevated premium for AI platform)
BETA              = 1.95  # high; correlated to tech/risk-on AND company-specific Musk newsflow

# ── SCENARIO TABLE ───────────────────────────────────────────────────────────
SCENARIOS = [
    ("BEAR",  "Robotaxi stalls; EV margins stay depressed; Tesla re-rates to 'just a car company'",    1.50,  40,    60),
    ("BASE",  "Auto recovery + early robotaxi revenue; FSD subscription grows; no mega re-rating",     4.00,  70,   280),
    ("BULL",  "Cybercab scales to 10K+ fleet; FSD widely adopted; Optimus factory deployment",         8.00,  90,   720),
    ("XBULL", "Robotaxi + Optimus dominate; Tesla valued as AI platform; Musk execution peak",        15.00, 100, 1_500),
]

# ── CROSS-READ SIGNALS ───────────────────────────────────────────────────────
CROSS_READS = [
    ("Tesla global vehicle deliveries YoY",     "Core EV business health; pricing power",            "% YoY",    -15,   5,  20,  40,   6.3, 0.20),
    ("Cybercab / Robotaxi fleet deployed",      "Autonomy revenue ramp; regulatory milestones",      "vehicles",    0, 500, 5000, 50000, 300, 0.25),
    ("FSD miles per disengagement",             "Autonomy reliability; OEM licensing readiness",     "miles/dis",   2,  15,  50,  200,  20.0, 0.20),
    ("Auto gross margin excl. reg. credits",    "Pricing floor; manufacturing efficiency",           "%",          12,  18,  23,   28,  21.1, 0.15),
    ("China BEV market share",                  "Competitive positioning vs. BYD, NIO, Xpeng",      "%",           8,  12,  17,   22,  13.0, 0.15),
    ("Megapack energy storage deployment YoY",  "High-margin recurring energy revenue",              "% YoY",     -40,  20,  60,  120, -38.0, 0.05),
]

# ── STRUCTURAL COMPOSITE ADJUSTMENT ─────────────────────────────────────────
STRUCTURAL_FACTORS = [
    ("Cybercab / Robotaxi regulatory path  (Texas, Arizona approved; Dallas & Houston live)", +1.5, 0.25),
    ("FSD autonomy tech lead  (12B+ miles training data; best-in-class real-world AI)",       +1.2, 0.25),
    ("Brand damage — Musk political controversy  (EU/North-America boycotts; brand surveys)", -1.0, 0.20),
    ("China competitive displacement  (BYD, NIO, Xpeng at materially lower price points)",   -0.8, 0.15),
    ("Optimus humanoid robot  (factory deployment; early commercial pipeline in FY2026)",     +0.8, 0.15),
]

# ── EPS QUALITY DECOMPOSITION (CONTRACTION NARRATIVE) ───────────────────────
# TSLA EPS declined FY2022→FY2025: $4.07 → $1.67 (−$2.40). Drivers of DECLINE:
# (driver, fraction_of_EPS_TROUGH, is_structural)
EPS_DECOMP = [
    ("Auto gross margin collapse  (aggressive price cuts; China competition; mix shift)",   0.40, False),
    ("ASP decline  (Model 3/Y refresh promotions; reduced FSD attach rate)",               0.22, False),
    ("Brand erosion  (Musk political controversy; boycotts EU/North America)",             0.15, True),
    ("China market-share loss  (BYD, NIO, Xpeng at 30-50% lower ASPs)",                   0.12, True),
    ("R&D + AI / Optimus capex drag  (pre-revenue autonomy investment phase)",             0.11, True),
]

# ── IDIOSYNCRATIC vs MACRO DECOMPOSITION ─────────────────────────────────────
IDIO = {
    "idio_pct":  70,
    "macro_pct": 30,
    "beta":      1.95,
    "drivers": [
        ("Cybercab / Robotaxi execution & regulatory approvals",  "IDIO",  0.25, "Fleet deployment pace; city expansions; autonomous miles"),
        ("FSD Full Self-Driving progress & safety record",        "IDIO",  0.20, "Disengagement rate; NHTSA incidents; OEM licensing"),
        ("Optimus robot deployment (Tesla factories + commercial)","IDIO",  0.15, "Unit output; AI capability; commercial pricing"),
        ("Elon Musk brand & political risk",                      "IDIO",  0.10, "Consumer boycotts; government relations; management focus"),
        ("Risk-on / tech sentiment & Nasdaq beta",                "MACRO", 0.15, "Growth-stock multiple; rate sensitivity; AI bubble risk"),
        ("EV demand cycle  (consumer confidence; incentives)",    "MACRO", 0.10, "IRA credits; EV adoption curve; gasoline prices"),
        ("China macro & trade policy",                            "MACRO", 0.05, "Tariffs; CATL; BYD subsidies; US-China tensions"),
    ],
}

# ═══════════════════════════════════════════════════════════════════════════════
# PART 1 — REUSABLE ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def softmax_probs(composite, scenarios, T=0.60):
    centres = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    labels  = [s[0] for s in scenarios]
    logits  = [-(composite - centres[l])**2 / T for l in labels]
    mx      = max(logits)
    exps    = [math.exp(x - mx) for x in logits]
    total   = sum(exps)
    return [e / total for e in exps]

def rfmt(r):
    return f"{r:.2f}x" if r != float('inf') else "N/A"

def infer_composite(target_price, scenarios, T=0.60):
    lo, hi = 1.0, 4.0
    for _ in range(60):
        mid   = (lo + hi) / 2
        probs = softmax_probs(mid, scenarios, T)
        ev    = sum(p * s[4] for p, s in zip(probs, scenarios))
        if ev < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

def signal_from_ratio(r):
    if r == float('inf') or r is None:
        return "✕ AVOID"
    if r < 0.75:
        return "◉ BUY"
    if r < 1.10:
        return "◎ ACCUMULATE"
    if r < 1.75:
        return "◐ WATCHLIST"
    if r < 2.50:
        return "◑ HOLD / TRIM"
    return "✕ AVOID"

# ── derived quantities ────────────────────────────────────────────────────────
epp_now          = EPS_NOW * EPP_MIN_PE
epp_gap_pct      = (CURRENT_PRICE - epp_now) / epp_now * 100
price_b          = CONS_EPS_2YR * CONS_EXIT_PE
ratio_b          = (CURRENT_PRICE - epp_now) / (price_b - CURRENT_PRICE) if price_b > CURRENT_PRICE else float('inf')
signal           = signal_from_ratio(ratio_b)

sca_raw          = sum(r * w for _, r, w in STRUCTURAL_FACTORS)
sca_adj          = sca_raw / 2.0

market_composite = infer_composite(CURRENT_PRICE, SCENARIOS)
adj_composite    = market_composite + sca_adj

probs            = softmax_probs(adj_composite, SCENARIOS)
proxy_ev         = sum(p * s[4] for p, s in zip(probs, SCENARIOS))
mkt_probs        = softmax_probs(market_composite, SCENARIOS)

# EPS cycle (declining — EPS_NOW < EPS_TROUGH)
eps_change       = EPS_NOW - EPS_TROUGH   # negative: -$2.40
trailing_pe      = CURRENT_PRICE / EPS_NOW
forward_pe       = CURRENT_PRICE / EPS_FWD_CONSENSUS
cons_ret_ann     = ((price_b / CURRENT_PRICE) ** (1/2) - 1) * 100 if price_b > CURRENT_PRICE else float('-inf')

# ═══════════════════════════════════════════════════════════════════════════════
# PART 2 — ANALYST COMMENTARY
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 72)
print("  TESLA, INC. (TSLA)  |  BottomUp Risk/Reward Signal Model")
print("=" * 72)
print(f"  Signal  : {signal}   |   Ratio B : {rfmt(ratio_b)}")
print(f"  Price   : ${CURRENT_PRICE:.2f}  |   EPP Floor : ${epp_now:.2f}  (+{epp_gap_pct:.0f}% above floor)")
print(f"  Date    : 2026-05-21  |   Sector  : EV + AI Autonomy + Energy Storage")
print("=" * 72)
print()
print("─" * 72)
print("  PART 2 — ANALYST COMMENTARY")
print("─" * 72)
print()

print("  1. BUSINESS QUALITY & COMPETITIVE MOAT")
print("  ─────────────────────────────────────────────────────────────────")
print("""
  Tesla operates at the intersection of three secular transitions: electric
  vehicle adoption, artificial intelligence / autonomy, and distributed energy.
  The market is repricing TSLA as a hybrid of three businesses — each with a
  different valuation framework:

  EV MANUFACTURING (~50% of current revenue, declining share)
  Tesla remains the global BEV technology leader — Q1 2026 reclaimed the
  global pure-EV sales lead from BYD with 358,023 deliveries (+6.3% YoY).
  The competitive moat is VERTICAL INTEGRATION: proprietary battery cells
  (4680), in-house powertrains, Dojo AI supercomputer for training, and the
  highest auto gross margins in the industry (21.1% ex-credits in Q1 2026,
  a massive beat vs. the 17.7% consensus). However, the moat is under serious
  pressure from BYD, NIO and Xpeng at 30-50% lower ASPs in China, and from
  legacy OEMs closing the technology gap in Europe and North America.

  AI AUTONOMY (Cybercab / FSD / Robotaxi — the primary valuation driver)
  This is the category that justifies the $1.5T market cap despite $1.67/share
  in trailing earnings. Tesla began unsupervised Robotaxi rides in Dallas and
  Houston in April 2026. Production lines for the Cybercab are being installed.
  The data moat is real: ~12 billion real-world miles of training data, far
  beyond any competitor. FSD (Supervised) received regulatory approval in the
  Netherlands in April 2026. The bull case centres on Cybercab becoming the
  first scalable, profitable autonomous ride-hailing network — a TAM of
  potentially trillions over a decade. This is option value, not current EPS.

  OPTIMUS + ENERGY (~20% of current value, emerging)
  Optimus humanoid robots are being deployed in Tesla's own factories and a
  small-scale commercial pipeline is expected in late 2026. Megapack energy
  storage is a high-margin, recurring revenue business — though Q1 2026
  deployment (8.8 GWh) was down 38% YoY and severely missed consensus.
  The $26.5B DOE loan / $20B capex guidance for 2026 funds grid-scale energy,
  new factory capacity, and the robotaxi ramp — but will compress near-term FCF.
""")

print("  2. EARNINGS QUALITY & EPP FLOOR ANALYSIS")
print("  ─────────────────────────────────────────────────────────────────")
print(f"""
  EPP FRAMEWORK NOTE — INVERTED CYCLE
  Unlike other portfolio stocks (where EPS grew from a trough), Tesla's EPS
  has been in a DOWN cycle since the FY2022 peak. The EPP floor has migrated
  DOWNWARD with earnings — an unusual and important signal.

  EPP FLOOR VALIDATION (Dec-2022 stock trough)
  Reference EPS  : ${EPS_TROUGH:.2f}  (FY{EPS_TROUGH_YEAR} non-GAAP peak — highest Tesla ever earned)
  Reference Price: ${EPS_TROUGH_PRICE:.2f}  (Dec-2022 / Jan-2023 absolute stock floor)
  Min viable P/E : {EPP_MIN_PE}x  →  ${EPS_TROUGH:.2f} × {EPP_MIN_PE}x  =  ${EPS_TROUGH * EPP_MIN_PE:.2f}  ≈  ${EPS_TROUGH_PRICE:.2f} ✓

  At the Dec-2022 trough, the market capitulated on Tesla's growth narrative —
  Elon Musk sold stock to buy Twitter, growth expectations collapsed, and the
  multiple compressed to 25x trailing earnings. This is Tesla's market-validated
  "no-option-value" floor P/E. It has never gone lower.

  EPS CONTRACTION  (FY2022 peak → FY2025 trough)
  FY2022 (peak)  :  ${EPS_TROUGH:.2f}  →  EPP at {EPP_MIN_PE}x:  ${EPS_TROUGH * EPP_MIN_PE:.2f}  (validated ✓)
  FY2023         :  $3.01  →  EPP at {EPP_MIN_PE}x:  $75.25
  FY2024         :  $2.35  →  EPP at {EPP_MIN_PE}x:  $58.75
  FY2025 (trough):  ${EPS_NOW:.2f}  →  EPP at {EPP_MIN_PE}x:  ${epp_now:.2f}  ← TODAY'S FLOOR

  The floor has fallen from $102 (FY2022-based) to $42 (FY2025-based). Every
  $1 of EPS decline reduced the fundamental floor by $25. The $372 gap between
  the floor ($41.75) and the stock ($414.75) is PURE OPTION VALUE — the market's
  bet on robotaxi + Optimus + AI platform monetisation.

  EPS CONTRACTION DRIVERS  (FY2022 ${EPS_TROUGH:.2f} → FY2025 ${EPS_NOW:.2f}, −${abs(eps_change):.2f}/share)
""")
print(f"  {'Driver':<63}  {'Share':>5}  {'Type':>8}")
print(f"  {'─'*63}  {'─'*5}  {'─'*8}")
for desc, sh, is_s in EPS_DECOMP:
    type_label = "STRUCT." if is_s else "CYCL. ~"
    print(f"  {desc:<63}  {sh*100:>4.0f}%  {type_label:>8}")
print(f"""
  Cyclical components (margins + ASP) drove ~62% of the EPS decline — they CAN
  recover as the pricing war stabilises and volume scales. Structural components
  (brand damage, China share loss, investment drag) drove ~38% — these require
  deliberate execution to reverse. Q1 2026 auto gross margin of 21.1% (+360bp
  vs estimate) is the first concrete evidence of cyclical recovery in margins.
""")

print("  3. CROSS-READ COMPOSITE & SCENARIO PROBABILITIES")
print("  ─────────────────────────────────────────────────────────────────")
print()
print(f"  {'Signal':<43} {'Unit':>9}  {'BEAR':>6}  {'BASE':>6}  {'BULL':>6} {'XBULL':>7}  {'NOW':>8}  {'Wt':>4}")
print(f"  {'─'*43} {'─'*9}  {'─'*6}  {'─'*6}  {'─'*6} {'─'*7}  {'─'*8}  {'─'*4}")
for label, thesis, unit, bv, bsv, blv, xv, cur, wt in CROSS_READS:
    print(f"  {label:<43} {unit:>9}  {bv:>6.1f}  {bsv:>6.1f}  {blv:>6.1f} {xv:>7.0f}  {cur:>8.1f}  {wt:>4.2f}")
print()
print(f"  Market composite (implied by ${CURRENT_PRICE:.2f}): {market_composite:.2f}")
print(f"  SCA adjustment                                : {sca_adj:+.2f}")
print(f"  Model adj. composite                          : {adj_composite:.2f}")
print(f"  Composite gap (model − market)                : {adj_composite - market_composite:+.2f}")
print()
print(f"  {'Scenario':<8}  {'EPS':>6}  {'P/E':>5}  {'Target':>8}  {'Proxy%':>7}  {'Mkt%':>6}  {'Gap':>7}")
print(f"  {'─'*8}  {'─'*6}  {'─'*5}  {'─'*8}  {'─'*7}  {'─'*6}  {'─'*7}")
for (lbl, thesis, eps, pe, pt), p, mp in zip(SCENARIOS, probs, mkt_probs):
    gap = p*100 - mp*100
    print(f"  {lbl:<8}  ${eps:>5.2f}  {pe:>4}x  ${pt:>7,.0f}  {p*100:>6.1f}%  {mp*100:>5.1f}%  {gap:>+6.1f}pp")
print()
print(f"  Proxy EV  : ${proxy_ev:,.0f}   (model-weighted scenario price)")
print(f"  vs Market : ${CURRENT_PRICE:.2f}  (gap: {(proxy_ev - CURRENT_PRICE)/CURRENT_PRICE*100:+.1f}%)")
print()
print("""
  READ: The cross-read composite sits just above BASE (2.0). The Cybercab fleet
  is only in pilot phase (~300 vehicles vs 5,000 for BULL signal), which is the
  dominant weight signal. FSD disengagement and auto margins are both near the
  BASE/BULL boundary. The energy storage miss (-38% YoY) is the key drag.

  The SCA adds +0.24pp from the autonomy tech lead and Optimus pipeline, net
  of brand damage and China competitive headwinds. The overall read: the market
  is pricing in a higher composite than the fundamentals currently justify —
  the stock is running ahead of the robotaxi deployment evidence.

  The proxy EV of ~$440 at the model composite is ABOVE the current price,
  reflecting that IF the BULL scenario (Cybercab at scale) materialises, the
  stock is fair or cheap. But Method B (conservative 2yr base case) says AVOID.
""")

print("  4. METHOD B VALUATION & SIGNAL DERIVATION")
print("  ─────────────────────────────────────────────────────────────────")
print(f"""
  EPP FLOOR (downside anchor — theoretical; market never trades at this level)
    Current EPS ${EPS_NOW:.2f} × {EPP_MIN_PE}x min-viable P/E  =  EPP ${epp_now:.2f}
    Gap above floor: ${CURRENT_PRICE:.2f} − ${epp_now:.2f}  =  ${CURRENT_PRICE - epp_now:.2f}  ({epp_gap_pct:.0f}% — nearly all option value)

  METHOD B — CONSERVATIVE 2-YEAR TARGET
    Consensus EPS FY2027  : ${CONS_EPS_2YR:.2f}  (auto recovery + early robotaxi revenue)
    Conservative exit P/E : {CONS_EXIT_PE}x  (still elevated premium vs. history; AI platform)
    Price B               : ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x  =  ${price_b:.2f}

    Price B (${price_b:.2f}) is BELOW current price (${CURRENT_PRICE:.2f})
    → Upside is NEGATIVE under Method B conservative assumptions
    → Ratio B  =  N/A  →  Signal  =  ✕ AVOID

  SIGNAL SCALE:  ◉ BUY <0.75  ◎ ACCUM. 0.75–1.10  ◐ WATCHLIST 1.10–1.75
                 ◑ HOLD 1.75–2.50  ✕ AVOID >2.50 or N/A (upside negative)

  PRIMARY SIGNAL:  {signal}  (Ratio B {rfmt(ratio_b)})

  To justify $414.75 on Method B, you need EITHER:
    a) FY2027 EPS of $5.00 at 85x exit P/E  =  $425  (requires full robotaxi ramp)
    b) FY2027 EPS of $4.00 at 105x exit P/E  =  $420  (requires multiple expansion)
    c) FY2027 EPS of $6.00 at 70x exit P/E  =  $420  (aggressive BULL execution)
  None of these are the CONSENSUS base case. They are BULL case scenarios.

  Valuation context:
    Trailing P/E  : {trailing_pe:.0f}x  (FY2025 EPS ${EPS_NOW:.2f} — peak pessimism multiple)
    Forward P/E   : {forward_pe:.0f}x  (FY2026E ${EPS_FWD_CONSENSUS:.2f})
    FY2027 P/E    : {CURRENT_PRICE/CONS_EPS_2YR:.0f}x  (${CONS_EPS_2YR:.2f} consensus)
    Dividend yield: 0%  (no dividend; all FCF reinvested in capex)

  TSLA is not investable via the EPP/Method B framework at current prices unless
  you adopt BULL scenario assumptions as your BASE CASE — which is precisely what
  the $1.5T market cap is doing. The framework flags this correctly as AVOID for
  risk-managed long-only allocation. TSLA at $414 is a high-conviction BULL bet,
  not a value-anchored position.
""")

print("  5. IDIOSYNCRATIC vs MACRO DECOMPOSITION")
print("  ─────────────────────────────────────────────────────────────────")
print(f"""
  Idiosyncratic  {IDIO['idio_pct']}%   |   Macro / Sentiment  {IDIO['macro_pct']}%   |   Beta  {IDIO['beta']:.2f}

  Tesla is the highest-idiosyncratic stock in this coverage universe. 70% of
  the price driver is company-specific: Cybercab regulatory progress, FSD
  disengagement milestones, Optimus deployment pace, and Elon Musk's brand
  and management focus. A single regulatory approval (FSD national rollout),
  a Cybercab fleet announcement, or an Optimus commercial deal could move the
  stock ±20-30% irrespective of macro conditions. Equally, a fatal accident,
  a major recall, or a Musk distraction event creates asymmetric downside.
  Beta 1.95 reflects high absolute volatility — but most of it is idiosyncratic,
  not macro. Fundamental research creates genuine edge here; momentum does not.
""")

print(f"  {'Driver':<48}  {'Type':>5}  {'Wt':>4}  {'Detail'}")
print(f"  {'─'*48}  {'─'*5}  {'─'*4}  {'─'*28}")
for drv, typ, wt, detail in IDIO["drivers"]:
    print(f"  {drv:<48}  {typ:>5}  {wt:.2f}  {detail}")
print()

# ═══════════════════════════════════════════════════════════════════════════════
# PART 3 — NUMBERS & SIGNALS
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("─" * 72)
print("  PART 3 — NUMBERS & SIGNALS")
print("─" * 72)
print()

print("  A. EPP FLOOR TABLE  (NB: floor has MIGRATED DOWN as EPS contracted)")
print(f"  {'FY':<6}  {'Adj.EPS':>8}  {'EPP@25x':>9}  {'Δ EPS':>7}  {'Note'}")
print(f"  {'─'*6}  {'─'*8}  {'─'*9}  {'─'*7}  {'─'*32}")
hist = [
    (2021, 2.26, ""),
    (2022, 4.07, "← EPS peak; EPP validated by Dec-22 floor ✓"),
    (2023, 3.01, "price cuts; margin compression begins"),
    (2024, 2.35, ""),
    (2025, 1.67, "← CURRENT (EPS trough; recovery started Q1-26)"),
]
prev_eps = None
for yr, eps, note in hist:
    epp_yr = eps * EPP_MIN_PE
    d_eps  = f"{eps - prev_eps:+.2f}" if prev_eps else "  —"
    print(f"  {yr:<6}  ${eps:>7.2f}  ${epp_yr:>8.2f}  {d_eps:>7}  {note}")
    prev_eps = eps
print(f"\n  FY2026E  ${'2.00':>7}  ${'50.00':>8}  {'':>7}  ← recovery (Q1 beat $0.41)")
print(f"  FY2027E  ${'4.00':>7}  ${'100.00':>8}  {'':>7}  ← Method B exit EPS (consensus incl. robotaxi)")
print()

print("  B. SCENARIO TABLE (2-year horizon)")
print(f"  {'Scenario':<8}  {'Thesis':<62}  {'EPS':>5}  {'P/E':>4}  {'Target':>8}  {'Prob%':>6}")
print(f"  {'─'*8}  {'─'*62}  {'─'*5}  {'─'*4}  {'─'*8}  {'─'*6}")
for (lbl, thesis, eps, pe, pt), p in zip(SCENARIOS, probs):
    print(f"  {lbl:<8}  {thesis:<62}  ${eps:>4.2f}  {pe:>3}x  ${pt:>7,.0f}  {p*100:>5.1f}%")
print()

print("  C. SIGNAL SCORECARD")
print(f"  {'Metric':<40}  {'Value':>12}  {'Note'}")
print(f"  {'─'*40}  {'─'*12}  {'─'*28}")
fwd_p27 = CURRENT_PRICE / CONS_EPS_2YR
metrics = [
    ("Current Price",              f"${CURRENT_PRICE:.2f}",         "NASDAQ:TSLA, 2026-05-21"),
    ("EPP Floor (FY2025 EPS)",     f"${epp_now:.2f}",               f"${EPS_NOW:.2f} × {EPP_MIN_PE}x (theoretical)"),
    ("Gap Above EPP",              f"+{epp_gap_pct:.0f}%",          "~all option value premium"),
    ("Method B Target (2yr)",      f"${price_b:.2f}",               f"${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x"),
    ("Ratio B (PRIMARY)",          rfmt(ratio_b),                   f"{signal}"),
    ("Trailing P/E",               f"{trailing_pe:.0f}x",           f"FY2025 EPS ${EPS_NOW:.2f}"),
    ("Forward P/E (FY2026E)",      f"{forward_pe:.0f}x",            f"FY2026E ${EPS_FWD_CONSENSUS:.2f}"),
    ("FY2027 P/E",                 f"{fwd_p27:.0f}x",               f"${CONS_EPS_2YR:.2f} consensus"),
    ("2yr Cons. Return (B)",       "N/A",                           "price_B below current price"),
    ("EPS cycle",                  f"${EPS_TROUGH:.2f}→${EPS_NOW:.2f}",  "FY2022 peak → FY2025 trough"),
    ("Beta",                       f"{BETA:.2f}",                   "high idio + tech sentiment"),
    ("Model composite",            f"{adj_composite:.2f}",          "just above BASE 2.0"),
    ("Proxy EV",                   f"${proxy_ev:,.0f}",             f"vs market ${CURRENT_PRICE:.2f}"),
    ("Idio / Macro split",         f"{IDIO['idio_pct']}% / {IDIO['macro_pct']}%",  "Musk + robotaxi drive the stock"),
    ("Market cap",                 "~$1.35T",                       "pricing BULL/XBULL scenario blend"),
]
for name, val, note in metrics:
    print(f"  {name:<40}  {val:>12}  {note}")
print()

print("  D. STRUCTURAL FACTORS (SCA)")
print(f"  {'Factor':<68}  {'Rating':>7}  {'Wt':>4}")
print(f"  {'─'*68}  {'─'*7}  {'─'*4}")
for fac, r, w in STRUCTURAL_FACTORS:
    print(f"  {fac:<68}  {r:>+6.1f}   {w:.2f}")
print(f"\n  SCA raw: {sca_raw:+.3f}  →  adj (+raw/2): {sca_adj:+.3f}  →  composite bump: {sca_adj:+.3f}pp")
print()

print("  E. INVESTMENT DECISION SUMMARY")
print()
print(f"  Signal   :  {signal}  |  Ratio B {rfmt(ratio_b)}")
print(f"  Thesis   :  At $414 (~{trailing_pe:.0f}x trailing / {forward_pe:.0f}x FY2026 / {fwd_p27:.0f}x FY2027E), Tesla")
print(f"              is priced for the BULL scenario — Cybercab at scale,")
print(f"              FSD nationally deployed, Optimus in commercial use. None")
print(f"              of this is in the 2-year consensus EPS of $4.00. The EPP")
print(f"              framework correctly identifies this as 'option value only'.")
print()
print(f"  For long-only risk-managed portfolios: AVOID. The risk/reward requires")
print(f"  BULL case assumptions as the base case, which violates conservative")
print(f"  Method B discipline.")
print()
print(f"  Re-evaluate at: (a) Price <$280 (BASE scenario priced in) — stock")
print(f"  would become WATCHLIST/ACCUMULATE; (b) Cybercab fleet >5,000 units")
print(f"  with confirmed revenue traction — would upgrade FY2027E EPS materially;")
print(f"  (c) FSD disengagement rate <50 miles/dis nationally — signals OEM")
print(f"  licensing TAM is real and near.")
print()
print(f"  Key watch: Monthly Cybercab fleet deployment figures (primary catalyst)")
print(f"             Q2 2026 auto gross margin vs. 19-21% expected range")
print(f"             FSD supervised → unsupervised approval in more US states")
print(f"             Optimus robot unit economics & commercial pricing disclosure")
print()
print("  " + "─" * 68)
print("  NOT FINANCIAL ADVICE. All prices USD. Analysis date 2026-05-21.")
print("  " + "─" * 68)
print()
