"""
Lam Research Corporation (LRCX) — BottomUp Risk/Reward Signal Model
WFE near-monopoly: ~50% global etch share; DRAM/HBM intensity cycle; CSPD service revenue
Three-Part Publication Format

FISCAL YEAR NOTE: Lam Research's fiscal year ends in late June.
  FY2023 = July 2022 – June 2023 (revenue peak $17.4B; EPS near-peak)
  FY2024 = July 2023 – June 2024 (trough year; revenue $14.9B, WFE down-cycle; EPS trough)
  FY2025 = July 2024 – June 2025 (recovery; EPS $4.14)
  FY2026 = July 2025 – June 2026 (current; Q1-Q3 reported; Q4 guided $1.65)
  FY2027 = July 2026 – June 2027 (2-year forward; consensus ~$6.90)
  FY2028 = July 2027 – June 2028 (Method B exit target)

SPLIT NOTE: Lam Research completed a 10-for-1 stock split effective October 2, 2024.
  All EPS and price figures below are post-split (historical pre-Oct-2024 EPS ÷ 10).
  Example: FY2024 Q1 EPS was $6.85 pre-split = $0.685 post-split.
"""
import math

# ── LIVE PRICE (fetched via web search, 2026-05-21) ──────────────────────────
CURRENT_PRICE = 298.46   # LRCX — web search (intraday range $289–$300), 2026-05-21

# ── EPP FLOOR CALIBRATION ────────────────────────────────────────────────────
# FY2024 (July 2023 – June 2024): WFE down-cycle; memory capex collapse; export controls
# Revenue dropped 14.5% ($17.4B → $14.9B); EPS the worst in the AI era
# Quarterly EPS (post-split): Q1(Sep-23)$0.685 + Q2(Dec-23)$0.752 + Q3(Mar-24)$0.779 + Q4(Jun-24)$0.814
# Stock hit ~$52 post-split in Oct–Nov 2023 (export control escalation + broad market low)
# EPP validation: $3.03 × 17x = $51.5  ≈  $52 ✓
EPS_TROUGH       = 3.03   # FY2024 non-GAAP diluted EPS, post-split (sum of 4 quarters)
EPS_TROUGH_YEAR  = 2024
EPS_TROUGH_PRICE = 52.0   # Oct–Nov 2023 post-split equivalent; export-control capitulation floor
EPP_MIN_PE       = 17     # market-validated floor multiple for a WFE near-monopoly at maximum uncertainty

# ── CURRENT FUNDAMENTALS ─────────────────────────────────────────────────────
EPS_NOW           = 5.55   # FY2026E non-GAAP; Q1$1.26+Q2$1.26+Q3$1.47+Q4guide$1.65 (midpoint)
EPS_FWD_CONSENSUS = 6.90   # FY2027E consensus (post Q3-FY2026 beat; fiscal year ending Jun-2027)
CONS_EPS_2YR      = 8.00   # FY2028E conservative (extrapolation of ~16% growth from FY2027E $6.90)
CONS_EPS_CAGR     = 0.200  # ~20%/yr compound (FY2026E $5.55 → FY2028E $8.00)
CONS_EXIT_PE      = 20     # conservative 2-yr exit P/E (= historical WFE trough multiple; cycle-peak haircut)
BETA              = 1.45   # elevated; semiconductor equipment correlates to WFE capex cycle + risk-on tech

# ── SCENARIO TABLE ───────────────────────────────────────────────────────────
SCENARIOS = [
    ("BEAR",  "WFE -30%; memory oversupply + AI capex pause; China fully banned; cycle collapses",   3.50,  16,   56),
    ("BASE",  "WFE stabilises $130-135B; HBM/logic steady; LRCX etch share intact; CSPD grows",     8.00,  20,  160),
    ("BULL",  "WFE $175B+; HBM4+ etch intensity surge; logic 2nm pull-in; margin expansion",        11.50,  25,  288),
    ("XBULL", "WFE $240B+; AGI/quantum silicon buildout; LRCX atomic-layer monopoly extends",       18.00,  30,  540),
]

# ── CROSS-READ SIGNALS ───────────────────────────────────────────────────────
CROSS_READS = [
    ("WFE industry spend  (total addressable; LRCX etch+clean+deposition = ~16%)", "Primary cycle driver; industry forecasts raised Q3-2026 to $140B",        "$B",   95, 135, 175, 250, 140, 0.35),
    ("DRAM / HBM etch equipment spend  (HBM layer count drives etch intensity)",   "AI memory; each HBM gen = +20-30% etch steps per wafer",                 "$B",   30,  55,  78, 115,  62, 0.25),
    ("NAND capex utilisation / capacity ramp",                                     "NAND still below peak; GenAI edge inference demand = recovery catalyst",  "%",   40,  70,  85,  95,  60, 0.15),
    ("LRCX China revenue  (H20-equivalent; domestic SMIC/CXMT)",                  "Permanently restricted; ~$3B structural hole; workaround limited",         "$B",  0.5, 2.5,  4.0,  6.0,  2.0, 0.15),
    ("Advanced logic WFE  (TSMC 2nm / N2; Intel 18A; Samsung SF2)",               "Logic etch intensity highest at 2nm-class; LRCX gate-all-around tools",   "$B",   8,  18,  30,  50,  19, 0.10),
]

# ── STRUCTURAL COMPOSITE ADJUSTMENT ─────────────────────────────────────────
STRUCTURAL_FACTORS = [
    ("Etch market near-monopoly  (~50% global share; no credible displacer in <5 yr)",              +1.2, 0.30),
    ("HBM structural tailwind  (each HBM gen = more etch steps; AI = permanent demand uplift)",     +0.8, 0.20),
    ("Memory cyclicality  (~60% revenue from DRAM+NAND capex; historically -30% WFE cycles)",      -1.2, 0.25),
    ("China export restrictions  (historically ~31% revenue; now structurally $2B; future risk)",   -1.0, 0.15),
    ("CSPD recurring revenue  (~20% of revenue; installed-base-driven; cycle-resistant buffer)",    +0.4, 0.10),
]

# ── EPS QUALITY DECOMPOSITION ────────────────────────────────────────────────
# EPS grew from $3.03 (FY2024 trough) to $5.55 (FY2026E): +$2.52/share
# Structural drivers dominate but cyclical WFE recovery is a meaningful component
EPS_DECOMP = [
    ("AI-driven HBM / DRAM advanced etch demand  (layer count multiplier per chip)",   0.42, True),
    ("WFE industry cycle recovery from 2024 trough  ($14.9B → $23B+ LRCX revenue)",   0.27, False),
    ("Advanced logic node ramp  (TSMC 2nm, Intel 18A; etch-intensive gate-all-around)", 0.13, True),
    ("Gross margin expansion + operating leverage  (etch/CSPD mix; scale efficiency)",  0.10, True),
    ("CSPD service revenue growth  (installed base; sticky; multi-year contracts)",     0.05, True),
    ("China export restriction drag  (structural revenue loss; negative offset)",       0.03, False),
]

# ── IDIOSYNCRATIC vs MACRO DECOMPOSITION ─────────────────────────────────────
IDIO = {
    "idio_pct":  40,
    "macro_pct": 60,
    "beta":      1.45,
    "drivers": [
        ("Etch market share defence & product leadership",          "IDIO",  0.20, "Vantara, Argos, Sense.i platform executions; <5% share to lose"),
        ("CSPD & installed-base monetisation",                      "IDIO",  0.10, "Service revenue ~20% of total; grows every quarter regardless of cycle"),
        ("China revenue workaround strategy",                       "IDIO",  0.10, "SMIC/CXMT alternative channel; export-control navigation"),
        ("WFE industry spending cycle  (memory + logic capex)",     "MACRO", 0.25, "DRAM/NAND customer capex decisions; TSMC/Samsung 2-yr plans"),
        ("Memory oversupply / HBM demand sustainability",           "MACRO", 0.20, "HBM3e→HBM4 ramp; NAND recovery timeline; AI edge inference"),
        ("Semiconductor geopolitics  (Taiwan, export controls)",    "MACRO", 0.15, "TSMC Taiwan supply; US export restrictions escalation risk"),
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

eps_g_total      = EPS_NOW - EPS_TROUGH
cyclical_dollar  = sum(EPS_TROUGH * sh for _, sh, is_s in EPS_DECOMP if not is_s)
struct_dollar    = eps_g_total - cyclical_dollar

trailing_pe      = CURRENT_PRICE / EPS_NOW
forward_pe       = CURRENT_PRICE / EPS_FWD_CONSENSUS
cons_ret_ann     = ((price_b / CURRENT_PRICE) ** (1/2) - 1) * 100

# ═══════════════════════════════════════════════════════════════════════════════
# PART 2 — ANALYST COMMENTARY
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 72)
print("  LAM RESEARCH CORPORATION (LRCX)  |  BottomUp Risk/Reward Signal Model")
print("=" * 72)
print(f"  Signal  : {signal}   |   Ratio B : {rfmt(ratio_b)}")
print(f"  Price   : ${CURRENT_PRICE:.2f}  |   EPP Floor : ${epp_now:.2f}  (+{epp_gap_pct:.1f}% above)")
print(f"  Date    : 2026-05-21  |   Sector  : Semiconductor Equipment · WFE · Etch")
print("=" * 72)
print()
print("─" * 72)
print("  PART 2 — ANALYST COMMENTARY")
print("─" * 72)
print()

print("  1. BUSINESS QUALITY & COMPETITIVE MOAT")
print("  ─────────────────────────────────────────────────────────────────")
print("""
  Lam Research is the dominant global supplier of etch and deposition
  equipment — the critical tools that pattern and deposit thin films on every
  semiconductor chip manufactured. With ~50% share of global etch equipment
  spend and a deep installed base of over 80,000 systems worldwide, LRCX
  occupies a near-monopoly position in its core market with no credible
  near-term displacer.

  ETCH MONOPOLY — THE PHYSICAL BARRIER TO ENTRY
  Etch is arguably the most technically demanding step in semiconductor
  manufacturing: precision at the atomic scale, plasma chemistry that takes
  decades to master, and chamber designs validated through billions of wafer
  starts. Tokyo Electron (TEL) is the only credible alternative at ~35%
  share; all others are niche. LRCX's technical lead — embodied in the
  Vantara etch platform, Sense.i process control, and Argos ALD tools —
  accumulates year over year as the installed base deepens and process
  recipes (developed collaboratively with TSMC, Samsung, SK Hynix) become
  proprietary lock-in. Switching cost for a foundry is not just price; it's
  re-qualification of every process layer — a multi-year, $100M+ exercise.

  HBM STRUCTURAL TAILWIND — AI DIRECTLY GROWS THE ADDRESSABLE MARKET
  High-Bandwidth Memory (HBM) is the enabling technology for AI training at
  scale. Each generation of HBM (HBM3 → HBM3e → HBM4) stacks more DRAM
  dies and increases the via count per die — each of which requires
  additional etch steps. LRCX estimates that HBM manufacturing requires
  approximately 2-3x the etch intensity vs. standard DRAM production. As
  every AI accelerator (NVDA Blackwell, AMD MI300, Google TPUv5) ships with
  HBM, and as HBM capacity doubles YoY, the structural etch TAM is expanding
  independent of the broader WFE cycle. This is a genuine secular growth
  driver embedded within a cyclical business.

  Q3 FY2026 (March 2026, reported Apr 22, 2026): Revenue $5.84B (+23.8% YoY),
  non-GAAP EPS $1.47 (beat consensus $1.36, +8.1%). Record quarter.
  WFE industry forecast raised to ~$140B. Q4 FY2026 guided at $6.60B revenue
  (+/- $400M) and $1.65 EPS (+/- $0.15) — set to be another record quarter.
  Morgan Stanley upgraded to Overweight (price target $331) on May 20, 2026.

  KEY RISKS
  Memory cyclicality: ~60% of LRCX revenue traces to DRAM and NAND capex.
  Memory has historically exhibited 30-40% WFE capex swings peak-to-trough.
  The 2022-2024 down-cycle saw LRCX revenue fall 14.5% in FY2024 — and
  that was a mild cycle vs. prior downturns. A more severe memory correction
  triggered by AI capex normalisation or oversupply in commodity DRAM would
  compress earnings substantially.
  China: historically ~31% of LRCX revenue; export restrictions have
  structurally reduced this to ~$2B/yr (roughly 9-10% of current revenue).
  Further escalation or secondary restrictions on SMIC tools could cut this
  further. The structural hole is permanent and cannot be backfilled.
  Customer concentration: TSMC, Samsung, SK Hynix, and Micron represent
  ~65%+ of revenue; any coordinated capex freeze hits LRCX asymmetrically.
""")

print("  2. EARNINGS QUALITY & EPP FLOOR ANALYSIS")
print("  ─────────────────────────────────────────────────────────────────")
print(f"""
  EPP FLOOR VALIDATION
  [Post-split figures. 10-for-1 split effective October 2, 2024. Pre-split EPS ÷ 10.]
  Trough EPS  : ${EPS_TROUGH:.2f}  (FY2024; Q1$0.685+Q2$0.752+Q3$0.779+Q4$0.814; WFE down-cycle)
  Trough Price: ${EPS_TROUGH_PRICE:.2f}   (Oct-Nov 2023 post-split; export-control + macro capitulation)
  Min viable P/E: {EPP_MIN_PE}x  →  ${EPS_TROUGH:.2f} × {EPP_MIN_PE}x = ${EPS_TROUGH * EPP_MIN_PE:.2f}  ≈  ${EPS_TROUGH_PRICE:.2f} ✓

  Even at the absolute trough — WFE down 14.5%, China restrictions doubling,
  memory customers cutting capex — the market did not let LRCX trade below
  17x trough EPS for long. The etch monopoly (50% market share; decades of
  process recipe lock-in) provides a structural floor to valuation that
  pure-memory or commodity semis do not enjoy.

  MIGRATED EPP (today)
  Current EPS : ${EPS_NOW:.2f}  (FY2026E; Q1-Q3 reported + Q4 guided midpoint; record year)
  EPP Floor   : ${EPS_NOW:.2f} × {EPP_MIN_PE}x  =  ${epp_now:.2f}
  Current Gap : ${CURRENT_PRICE:.2f} − ${epp_now:.2f}  =  +{epp_gap_pct:.1f}% above floor

  A {epp_gap_pct:.0f}% gap above the EPP floor is extreme for a semiconductor equipment
  company — it implies the market is paying 53.8x trailing EPS for a
  business that historically bottomed at 17x. At this gap, the stock has
  no margin of safety: any earnings disappointment, WFE cycle deceleration,
  or multiple compression will drive a significant drawdown.

  IMPORTANT CYCLICAL CAVEAT
  Not all of LRCX's current earnings are structural. ~30% of the EPS
  recovery from the FY2024 trough ($3.03) to FY2026E ($5.55) is attributable
  to WFE industry cycle recovery — i.e., cyclical revenue that was
  temporarily depressed and has now normalised. If WFE spending reverts
  toward prior-cycle averages, the normalised EPS is closer to $4.00-4.50,
  not $5.55. This matters significantly for valuation.

  EPS QUALITY DECOMPOSITION  (FY2024 ${EPS_TROUGH:.2f} → FY2026E ${EPS_NOW:.2f}: +${eps_g_total:.2f}/share)
  Structural dollar : ${struct_dollar:.3f}  ({struct_dollar/eps_g_total*100:.1f}% of growth)
  Cyclical dollar   : ${cyclical_dollar:.3f}  ({cyclical_dollar/eps_g_total*100:.1f}% of growth)

  Driver                                                             Share      Type
  ────────────────────────────────────────────────────────────────  ──────  ────────""")
for name, share, is_struct in EPS_DECOMP:
    kind = "REAL ✓" if is_struct else "CYCL. ~"
    print(f"  {name:<66}{share*100:>4.0f}%  {kind:>8}")

print(f"""
  ~70% of LRCX's EPS recovery from the trough is structural — driven by the
  HBM etch intensity wave and logic node ramp — but a meaningful 30% is the
  WFE cycle normalising from depressed levels. This cyclical component is
  the key earnings risk: if WFE contracts again, it reverses.
""")

print("  3. CROSS-READ COMPOSITE & SCENARIO PROBABILITIES")
print("  ─────────────────────────────────────────────────────────────────")
print()

hdr = f"  {'Signal':<51} {'Unit':>7}  {'BEAR':>6}  {'BASE':>6}  {'BULL':>6} {'XBULL':>6}  {'NOW':>6}  {'Wt':>4}"
print(hdr)
print("  " + "─" * 67)
for name, desc, unit, b, ba, bu, xb, now, wt in CROSS_READS:
    print(f"  {name:<51} {unit:>7}  {b:>6}  {ba:>6}  {bu:>6} {xb:>6}  {now:>6}  {wt:.2f}")

print()
print(f"  Market composite (implied by ${CURRENT_PRICE:.2f}): {market_composite:.2f}")
print(f"  SCA adjustment                                : {sca_adj:+.2f}")
print(f"  Model adj. composite                          : {adj_composite:.2f}")
print(f"  Composite gap (model − market)                : {adj_composite - market_composite:+.2f}")
print()

print(f"  {'Scenario':<8}  {'EPS':>6}  {'P/E':>5}  {'Target':>8}  {'Proxy%':>7}  {'Mkt%':>6}  {'Gap':>7}")
print("  " + "─" * 60)
for (label, desc, eps, pe, tgt), p, mp in zip(SCENARIOS, probs, mkt_probs):
    gap_pp = (p - mp) * 100
    print(f"  {label:<8}  ${eps:>5.2f}  {pe:>4}x  ${tgt:>7,}  {p*100:>6.1f}%  {mp*100:>5.1f}%  {gap_pp:>+6.1f}pp")

print()
print(f"  Proxy EV  : ${proxy_ev:.0f}   (weighted scenario price at model composite)")
print(f"  vs Market : ${CURRENT_PRICE:.2f}  (gap: {(proxy_ev - CURRENT_PRICE)/CURRENT_PRICE*100:+.1f}%)")

print(f"""

  READ: The cross-read signals place the model composite at {adj_composite:.2f} — between
  BASE (2.0) and BULL (2.75). WFE at $140B (between BASE's $135B and BULL's
  $175B), DRAM/HBM etch spend at $62B (above BASE's $55B), and advanced logic
  at $19B (just above BASE's $18B) all support a mild-BULL reading. However,
  NAND utilisation at only 60% (sub-BASE at 70%) and China revenue barely
  above BEAR floor drag the composite back toward BASE.

  CRITICAL INSIGHT: The market at ${CURRENT_PRICE:.2f} implies composite {market_composite:.2f} —
  essentially pricing LRCX at the BULL scenario (2.75). At BULL, the proxy
  EV is ~$288 (the BULL target itself). For the stock to DELIVER that return
  from here, the BULL scenario must not only materialise but become the floor.
  Meanwhile, the BASE scenario ($160) implies a -46% drawdown from today.
  Any mean-reversion of the WFE multiple from 53x to historical norms (20-25x)
  produces catastrophic losses regardless of earnings trajectory.

  The softmax model shows the market assigning ~62% probability to BULL and
  ~15% to XBULL — leaving only ~23% for BASE+BEAR. History says WFE equipment
  companies swing between BASE and BEAR on 3-5 year cycles. The current
  pricing requires that this cycle is structurally different — possible but
  not the base case.
""")

print("  4. METHOD B VALUATION & SIGNAL DERIVATION")
print("  ─────────────────────────────────────────────────────────────────")
print(f"""
  EPP FLOOR (downside anchor)
    Current EPS ${EPS_NOW:.2f} × {EPP_MIN_PE}x min-viable P/E  =  EPP ${epp_now:.2f}
    Downside to floor  =  ${CURRENT_PRICE:.2f} − ${epp_now:.2f}  =  ${CURRENT_PRICE - epp_now:.2f}  ({epp_gap_pct:.1f}% above floor)

  METHOD B — CONSERVATIVE 2-YEAR TARGET (FY2028 exit)
    Consensus FY2028E EPS : ${CONS_EPS_2YR:.2f}  (~16% growth from FY2027E $6.90; moderate extrapolation)
    Conservative exit P/E : {CONS_EXIT_PE}x  (= FY2024 trough multiple area; cycle-peak haircut)
    Price B               : ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x  =  ${price_b:.2f}
    Price B vs Current    : ${price_b:.2f} < ${CURRENT_PRICE:.2f}  →  N/A  (no 2-year upside to target)

  ATTRACTIVENESS RATIO B
    Price B (${price_b:.2f}) is BELOW current price (${CURRENT_PRICE:.2f})
    Method B produces negative upside → Ratio B is N/A → PRIMARY SIGNAL: AVOID

  SIGNAL SCALE:  ◉ BUY <0.75  ◎ ACCUM. 0.75–1.10  ◐ WATCHLIST 1.10–1.75
                 ◑ HOLD 1.75–2.50  ✕ AVOID >2.50 or N/A (upside negative)

  PRIMARY SIGNAL:  ✕ AVOID  (Method B N/A; Price B ${price_b:.2f} < Current ${CURRENT_PRICE:.2f})

  The AVOID signal reflects the core valuation arithmetic:
  — At ${CURRENT_PRICE:.2f}, LRCX trades at {trailing_pe:.1f}x FY2026E EPS (record WFE year)
  — Even at $8.00 FY2028E (20% EPS CAGR) × 20x conservative exit = $160
  — The BULL scenario target ($288) is BELOW the current stock price ($298)
  — The market is pricing somewhere between BULL and XBULL — both tail outcomes
  — EPP floor at ${epp_now:.2f} is {epp_gap_pct:.0f}% below current price — maximum P/E extension

  At what price does LRCX become interesting?
  — WATCHLIST zone: ~$185-210 (Ratio B ~1.1-1.5x; approaching BULL scenario pricing)
  — ACCUMULATE zone: ~$140-165 (Ratio B ~0.75-1.0x; near BASE scenario, large upside to BULL)
  — BUY zone: ~$105-130 (Ratio B <0.75x; EPP floor proximity; margin of safety restored)

  Valuation context:
    Trailing P/E (FY2026E)   : {trailing_pe:.1f}x
    Forward P/E (FY2027E)    : {forward_pe:.1f}x  (${CURRENT_PRICE:.2f} / ${EPS_FWD_CONSENSUS:.2f})
    FY2028 conservative P/E  : {CURRENT_PRICE/CONS_EPS_2YR:.1f}x
    2yr cons. return (B)     : {cons_ret_ann:.1f}%/yr  (${CURRENT_PRICE:.2f} → ${price_b:.2f} = negative)
    Morgan Stanley target    : $331  (vs $160 Method B conservative; implies BULL+ multiple)
""")

print("  5. IDIOSYNCRATIC vs MACRO DECOMPOSITION")
print("  ─────────────────────────────────────────────────────────────────")
print(f"""
  Idiosyncratic  {IDIO['idio_pct']}%   |   Macro / Sentiment  {IDIO['macro_pct']}%   |   Beta  {IDIO['beta']}

  LRCX is fundamentally a macro story with idiosyncratic etch monopoly
  defence. The 60% macro weight reflects the reality that WFE equipment
  demand is almost entirely determined by customer capex decisions — TSMC,
  Samsung, SK Hynix, and Micron collectively set LRCX's revenue trajectory.
  LRCX's only idiosyncratic levers are market share (stable at ~50%) and
  CSPD service revenue (~20% of sales, growing regardless of the cycle).
  Beta 1.45 reflects high correlation to the semiconductor capex cycle and
  risk-on/risk-off tech sentiment.

  Driver                                               Type    Wt  Detail
  ──────────────────────────────────────────────────  ─────  ────  ──────────────────────────""")
for drv, typ, wt, detail in IDIO["drivers"]:
    print(f"  {drv:<50}  {typ:>5}  {wt:.2f}  {detail}")

print()

# ═══════════════════════════════════════════════════════════════════════════════
# PART 3 — NUMBERS & SIGNALS
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("─" * 72)
print("  PART 3 — NUMBERS & SIGNALS")
print("─" * 72)
print()
print("  A. EPP FLOOR TABLE  (all figures post-split; ÷10 from pre-Oct-2024 reports)")
print(f"  {'FY':<8}  {'nGAAP EPS':>10}  {'EPP@17x':>9}  {'Δ EPS':>8}  Note")
print("  " + "─" * 68)

eps_table = [
    ("FY2022", 2.90,  "WFE boom peak — backlog-driven demand; FY2023 set to be higher"),
    ("FY2023", 3.50,  "Revenue peak $17.4B; strong margins; EPS peak before down-cycle"),
    ("FY2024", 3.03,  "← EPP trough; revenue $14.9B (-14.5%); export controls + WFE cut"),
    ("FY2025", 4.14,  "Recovery; Q1$0.86+Q2$0.91+Q3$1.04+Q4$1.33"),
    ("FY2026", EPS_NOW, "← CURRENT; record; Q1-Q3 reported + Q4 guided $1.65"),
]
prev_eps = None
for fy, eps, note in eps_table:
    epp = eps * EPP_MIN_PE
    delta = f"{eps - prev_eps:+.3f}" if prev_eps else "     —"
    marker = "  ← trough ✓" if "trough" in note else ""
    print(f"  {fy:<8}  ${eps:>9.3f}  ${epp:>8.2f}  {delta:>8}  {note}")
    prev_eps = eps

print()
print(f"  FY2027E  ${EPS_FWD_CONSENSUS:>9.2f}  ${EPS_FWD_CONSENSUS * EPP_MIN_PE:>8.2f}            ← consensus (post Q3-FY26 beat)")
print(f"  FY2028E  ${CONS_EPS_2YR:>9.2f}  ${CONS_EPS_2YR * EPP_MIN_PE:>8.2f}            ← Method B exit; EPP floor ${CONS_EPS_2YR * EPP_MIN_PE:.0f} (still well below ${CURRENT_PRICE:.2f})")

print()
print("  B. SCENARIO TABLE (2-year horizon, FY2028 exit)")
print(f"  {'Scenario':<8}  {'Thesis':<66}  {'EPS':>5}  {'P/E':>4}  {'Target':>8}  {'Prob%':>6}")
print("  " + "─" * 100)
for (label, desc, eps, pe, tgt), p in zip(SCENARIOS, probs):
    print(f"  {label:<8}  {desc:<66}  ${eps:>4.2f}  {pe:>3}x  ${tgt:>7,}  {p*100:>5.1f}%")

print()
print("  C. SIGNAL SCORECARD")
print(f"  {'Metric':<44}  {'Value':>12}  Note")
print("  " + "─" * 80)
scorecard = [
    ("Current Price",                        f"${CURRENT_PRICE:.2f}", "NASDAQ:LRCX, 2026-05-21"),
    ("EPP Floor (FY2026E EPS)",              f"${epp_now:.2f}", f"${EPS_NOW:.2f} × {EPP_MIN_PE}x"),
    ("Gap Above EPP",                        f"+{epp_gap_pct:.1f}%",  "extreme; full cycle-peak P/E expansion"),
    ("Method B Target (2yr)",                f"${price_b:.2f}",  f"${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x FY2028E conservative"),
    ("Ratio B (PRIMARY)",                     "N/A",            "Price B < Current → AVOID"),
    ("Trailing P/E (FY2026E)",               f"{trailing_pe:.1f}x",   "record WFE year; unsustainably high"),
    ("Forward P/E (FY2027E)",                f"{forward_pe:.1f}x",   f"${EPS_FWD_CONSENSUS} consensus; still elevated"),
    ("FY2028 conservative P/E",              f"{CURRENT_PRICE/CONS_EPS_2YR:.1f}x",   f"${CONS_EPS_2YR} est.; no margin of safety"),
    ("2yr Cons. Return (B)",                 f"{cons_ret_ann:.1f}%/yr", f"negative; ${CURRENT_PRICE:.2f} → ${price_b:.2f}"),
    ("EPS CAGR (FY2026→FY2028E)",           f"{CONS_EPS_CAGR*100:.0f}%/yr",   "WFE expansion + HBM intensity"),
    ("Beta",                                  f"{BETA}",         "WFE capex cycle + tech beta"),
    ("Model composite",                       f"{adj_composite:.2f}",  "between BASE (2.0) and BULL (2.75)"),
    ("Market composite (implied)",            f"{market_composite:.2f}",  "near BULL (2.75); aggressively priced"),
    ("Proxy EV",                              f"${proxy_ev:.0f}",  f"vs market ${CURRENT_PRICE:.2f} (gap: {(proxy_ev-CURRENT_PRICE)/CURRENT_PRICE*100:+.1f}%)"),
    ("Idio / Macro split",                   f"{IDIO['idio_pct']}% / {IDIO['macro_pct']}%",  "etch share + WFE cycle dominates"),
    ("Market cap",                           "~$373B",           f"{trailing_pe:.0f}x FY2026E — WFE equipment pricing"),
]
for metric, val, note in scorecard:
    print(f"  {metric:<44}  {val:>12}  {note}")

print()
print("  D. STRUCTURAL FACTORS (SCA)")
print(f"  {'Factor':<72}  {'Rating':>7}  {'Wt':>4}")
print("  " + "─" * 88)
for name, rating, wt in STRUCTURAL_FACTORS:
    print(f"  {name:<72}  {rating:>+7.1f}  {wt:.2f}")
print(f"\n  SCA raw: {sca_raw:+.3f}  →  adj (+raw/2): {sca_adj:+.3f}  →  composite bump: {sca_adj:+.3f}pp")

print(f"""
  E. INVESTMENT DECISION SUMMARY

  Signal   :  ✕ AVOID  |  Ratio B N/A  (Price B ${price_b:.0f} < Current ${CURRENT_PRICE:.2f})
  Thesis   :  LRCX's etch monopoly is real — but it's fully priced and then
              some. At 53.8x FY2026E and 43.3x FY2027E, the market is
              pricing the BULL scenario (~$288) as the floor, not the ceiling.
              Even assuming a structurally higher WFE floor ($135B vs $80B
              historical), the math does not support $298. Method B at the
              conservative FY2028E ($8.00 × 20x = $160) is 46% below current
              price. The EPP floor at $94.35 is 216% below. Re-evaluate
              below $165.

  Re-evaluate: Below $165-185  (Ratio B ~0.75-1.0; METHOD B near current price)
               Or: WFE contracts to $95-100B (BEAR confirmed; buy the flush)
               Or: China restrictions reversed (structurally adds $3-4B revenue)
  Avoid until: Trailing P/E falls below 25x, OR EPS grows into the multiple
               via 3+ consecutive quarters of WFE expansion confirmation.

  Key watch: WFE industry guidance (AMAT/KLAC/TEL as checks)
             Memory customer capex (Samsung, SK Hynix, Micron quarterly calls)
             HBM4 ramp timeline — key EPS upside catalyst
             NAND utilisation rate — first mover of WFE cycle reversal
             China policy (SMIC/CXMT workaround volumes)
             Q4 FY2026 guide (Jun 2026) — momentum confirmation or miss

  ────────────────────────────────────────────────────────────────────
  NOT FINANCIAL ADVICE. All prices USD. Analysis date 2026-05-21.
  ────────────────────────────────────────────────────────────────────""")
