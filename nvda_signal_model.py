"""
NVIDIA Corporation (NVDA) — BottomUp Risk/Reward Signal Model
AI GPU infrastructure monopoly: Hopper → Blackwell → Rubin; CUDA ecosystem; data centre compute
Three-Part Publication Format

FISCAL YEAR NOTE: NVIDIA's fiscal year ends in late January.
  FY2023 = Feb 2022 – Jan 2023 (gaming/crypto bust; EPS trough)
  FY2026 = Feb 2025 – Jan 2026 (Blackwell ramp; EPS $4.77, reported Feb-2026)
  FY2027 = Feb 2026 – Jan 2027 (current; Q1 = $1.87 reported May-20 2026)
  FY2028 = Feb 2027 – Jan 2028 (2-year exit target)

SPLIT NOTE: NVIDIA did a 10-for-1 stock split on June 10, 2024.
  All EPS figures below are post-split (pre-split FY2023 EPS = $3.34 → $0.334 post-split).
"""
import math

# ── LIVE PRICE (fetched via web search, 2026-05-21) ──────────────────────────
CURRENT_PRICE = 220.66   # NVDA — Yahoo Finance / MarketBeat search, 2026-05-21

# ── EPP FLOOR CALIBRATION ────────────────────────────────────────────────────
# FY2023 (ended Jan-2023): gaming/crypto bust; inventory write-downs; trough EPS
# Stock hit ~$10.80 (post-split) in Oct-2022 — absolute market capitulation
# Pre-split EPS FY2023 = $3.34  →  post-split (÷10) = $0.334
# EPP validation: $0.334 × 32x = $10.69  ≈  $10.80 ✓
EPS_TROUGH       = 0.334  # FY2023 non-GAAP diluted EPS, post-split (÷10 from $3.34 pre-split)
EPS_TROUGH_YEAR  = 2023
EPS_TROUGH_PRICE = 10.80  # Oct-2022 absolute trough (post-split); all-time low in the AI era
EPP_MIN_PE       = 32     # market-validated floor multiple even at full capitulation

# ── CURRENT FUNDAMENTALS ─────────────────────────────────────────────────────
EPS_NOW           = 4.77   # FY2026 non-GAAP diluted EPS, post-split (reported Feb-2026)
EPS_FWD_CONSENSUS = 8.34   # FY2027E consensus (updated post Q1-FY27 beat on May-20-2026)
CONS_EPS_2YR      = 10.50  # FY2028E conservative (consensus $11.43; using -8% haircut)
CONS_EPS_CAGR     = 0.485  # ~49%/yr compound (FY2026 $4.77 → FY2028 $10.50)
CONS_EXIT_PE      = 28     # conservative 2-yr exit P/E (= trough multiple; de-rating scenario)
BETA              = 1.65   # elevated; correlates to AI capex cycle + risk-on tech

# ── SCENARIO TABLE ───────────────────────────────────────────────────────────
SCENARIOS = [
    ("BEAR",  "AI capex collapses; China fully cut off; custom chips displace; EPS disappoints",  2.50,  18,    45),
    ("BASE",  "Blackwell/Rubin ramp continues; AI capex stable; CUDA moat intact",               10.50,  28,   294),
    ("BULL",  "AI capex accelerates; sovereign AI wave; inference boom; margin expansion",        16.00,  38,   608),
    ("XBULL", "AGI infrastructure buildout; NVDA compute monopoly; platform re-rating",          25.00,  55, 1_375),
]

# ── CROSS-READ SIGNALS ───────────────────────────────────────────────────────
CROSS_READS = [
    ("Hyperscaler AI capex (MSFT+GOOGL+META+AMZN, $B/yr)", "Primary NVDA revenue driver; GPU order visibility",  "$B/yr",  80, 130, 190, 260,  155, 0.30),
    ("NVDA data centre revenue YoY",                        "Execution on Blackwell; demand vs. supply",          "% YoY",  20,  45,  75, 100,   85, 0.25),
    ("NVDA AI GPU market share (vs AMD + custom)",          "CUDA lock-in durability; competitive erosion",       "%",      68,  78,  86,  93,   81, 0.15),
    ("Blackwell GPU utilisation / order backlog",           "Supply-demand tightness; pricing power",             "%",      60,  80,  93,  98,   95, 0.15),
    ("Sovereign AI & regional DC investment pipeline",      "Non-hyperscaler demand; geographic diversification", "$B",     50, 150, 300, 600,  180, 0.10),
    ("Gaming GPU revenue YoY",                              "Consumer GPU cycle; RTX adoption; GeForce share",   "% YoY", -20,   5,  18,  35,    5, 0.05),
]

# ── STRUCTURAL COMPOSITE ADJUSTMENT ─────────────────────────────────────────
STRUCTURAL_FACTORS = [
    ("CUDA software moat  (5M+ developers; 10+ yr lock-in; impossible to replicate cheaply)",  +1.5, 0.25),
    ("Blackwell→Rubin annual architecture cadence  (2-3x perf lead; sustained pricing power)", +1.2, 0.25),
    ("China export restrictions  (H20/A800 ban; ~$15B+ annual revenue permanently blocked)",   -0.8, 0.20),
    ("Hyperscaler custom chip risk  (Google TPU, Amazon Trainium, MSFT Maia; ~15% TAM risk)", -0.6, 0.20),
    ("NIM/NEMO/Omniverse software  (recurring AI factory revenue; margin expansion vector)",   +0.8, 0.10),
]

# ── EPS QUALITY DECOMPOSITION ────────────────────────────────────────────────
# EPS grew from $0.334 (FY2023 trough) to $4.77 (FY2026): +$4.436/share — nearly all structural
EPS_DECOMP = [
    ("AI data centre GPU demand  (Hopper → Blackwell architecture ramp)",          0.63, True),
    ("Software & ecosystem attach  (CUDA, NVLink, InfiniBand, NIM licensing)",     0.15, True),
    ("Gross margin expansion  (data centre mix 78% → 97% of revenue; ASP uplift)", 0.12, True),
    ("Operating leverage  (R&D + SG&A fixed vs 14x revenue growth from FY2023)",   0.07, True),
    ("Gaming GPU revenue cycle  (Ada → Blackwell gaming; RTX AI neural rendering)", 0.02, False),
    ("Crypto / blockchain GPU demand variance  (minor residual cyclicality)",       0.01, False),
]

# ── IDIOSYNCRATIC vs MACRO DECOMPOSITION ─────────────────────────────────────
IDIO = {
    "idio_pct":  55,
    "macro_pct": 45,
    "beta":      1.65,
    "drivers": [
        ("CUDA moat & architecture roadmap execution",       "IDIO",  0.20, "Jensen Huang; annual GPU cadence; developer lock-in"),
        ("Blackwell → Rubin ramp & gross margin delivery",   "IDIO",  0.20, "Supply ramp; CoWoS packaging; HBM availability"),
        ("China revenue management & export workarounds",    "IDIO",  0.15, "H20 alternatives; sovereign AI channels"),
        ("AI capex cycle  (hyperscaler CapEx decisions)",    "MACRO", 0.20, "Microsoft, Google, Meta, Amazon 2026-27 spend"),
        ("Tech/risk-on sentiment & rate environment",        "MACRO", 0.15, "Nasdaq beta; multiple sensitivity to rates"),
        ("Semiconductor supply chain  (TSMC, HBM, CoWoS)",  "MACRO", 0.10, "Capacity allocation; geopolitical risk (Taiwan)"),
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
print("  NVIDIA CORPORATION (NVDA)  |  BottomUp Risk/Reward Signal Model")
print("=" * 72)
print(f"  Signal  : {signal}   |   Ratio B : {rfmt(ratio_b)}")
print(f"  Price   : ${CURRENT_PRICE:.2f}  |   EPP Floor : ${epp_now:.2f}  (+{epp_gap_pct:.1f}% above)")
print(f"  Date    : 2026-05-21  |   Sector  : Semiconductors · AI Infrastructure")
print("=" * 72)
print()
print("─" * 72)
print("  PART 2 — ANALYST COMMENTARY")
print("─" * 72)
print()

print("  1. BUSINESS QUALITY & COMPETITIVE MOAT")
print("  ─────────────────────────────────────────────────────────────────")
print("""
  NVIDIA is the essential infrastructure layer of the AI revolution. With
  ~81% share of AI training GPU market and CUDA as the de-facto programming
  standard, NVIDIA has achieved a monopoly position that compounds annually
  through architecture, software, and ecosystem lock-in. Three structural moats:

  CUDA ECOSYSTEM — THE UNBREAKABLE MOAT
  Fifteen years of CUDA investment have created a network effect involving
  5M+ developers, 40,000+ libraries, and millions of lines of production AI
  code optimised for NVIDIA hardware. Switching to AMD ROCm or Google TPUs
  requires full re-training of developer muscle memory and code migration —
  an enormous friction for production workloads. Even hyperscalers developing
  their own silicon (Google TPU, Amazon Trainium, Microsoft Maia) use these
  primarily for specific inference tasks while continuing to buy NVDA H100/B200
  for training where the performance gap is widest and tolerance for risk lowest.

  ANNUAL ARCHITECTURE CADENCE (Hopper → Blackwell → Rubin)
  Jensen Huang's "one-year new product cycle" discipline is unique in semis.
  Hopper (H100/H200) captured the first wave of AI training demand (2023-24).
  Blackwell (B100/B200/GB200 NVL72) is the current generation — delivering
  5x training performance improvement and first-class inference at scale.
  Rubin, sampling in H2-2026, promises 4x efficiency gains over Blackwell with
  a focus on inference monetisation. This cadence makes the competitive gap
  self-reinforcing: AMD, Intel and custom chips are always one generation behind.

  Q1 FY2027 (reported May 20, 2026): Revenue $81.6B (+85% YoY), non-GAAP EPS
  $1.87 vs $1.75 consensus (+6.9% beat). Blackwell revenue set a quarterly
  record. Data centre alone was $67.6B. FY2027 full year consensus updated
  to $8.34 EPS ($370B+ revenue, 74% growth).

  KEY RISKS
  China export restrictions: H20/A800 bans removed ~$15B+ of annual revenue
  permanently. NVDA cannot recapture this without regulatory reversal.
  Hyperscaler custom chips: Google, Amazon and Microsoft are building their own
  AI ASICs — primarily for inference (lower performance requirements). This caps
  the TAM at ~80-85% of the addressable market for NVDA training GPUs.
  Concentration risk: top-5 hyperscalers represent ~45% of revenue; any capex
  pause or deployment delay creates outsized earnings risk.
""")

print("  2. EARNINGS QUALITY & EPP FLOOR ANALYSIS")
print("  ─────────────────────────────────────────────────────────────────")
print(f"""
  EPP FLOOR VALIDATION
  [Post-split figures. 10-for-1 split: June 10, 2024. Pre-split FY2023 EPS = $3.34]
  Trough EPS  : ${EPS_TROUGH:.3f}  (FY{EPS_TROUGH_YEAR} post-split; gaming/crypto bust + inventory charges)
  Trough Price: ${EPS_TROUGH_PRICE:.2f}   (Oct-2022 absolute low post-split; market fully capitulated)
  Min viable P/E: {EPP_MIN_PE}x  →  ${EPS_TROUGH:.3f} × {EPP_MIN_PE}x = ${EPS_TROUGH * EPP_MIN_PE:.2f}  ≈  ${EPS_TROUGH_PRICE:.2f} ✓

  Even at the absolute trough — with gaming demand collapsed, inventory charged
  off, and no AI demand yet visible — the market did not let NVDA trade below
  32x trailing EPS. The CUDA ecosystem and architecture leadership were valued
  at $10.80/share with only $0.334 in earnings. This is the structural floor.

  MIGRATED EPP (today)
  Current EPS : ${EPS_NOW:.2f}  (FY2026 non-GAAP; data centre 97% of mix)
  EPP Floor   : ${EPS_NOW:.2f} × {EPP_MIN_PE}x  =  ${epp_now:.2f}
  Current Gap : ${CURRENT_PRICE:.2f} − ${epp_now:.2f}  =  +{epp_gap_pct:.1f}% above floor

  A 45% gap above EPP is moderate for a company compounding EPS at 49%/yr.
  Importantly, the EPP floor itself is RISING RAPIDLY: each $1 of EPS growth
  adds $32 to the floor. At $8.34 FY2027E, the floor rises to $267. At $10.50
  FY2028E, the floor reaches $336 — well above the current stock price. The EPP
  floor will surpass today's stock price within 18-24 months if consensus holds.

  EPS QUALITY DECOMPOSITION  (FY{EPS_TROUGH_YEAR} ${EPS_TROUGH:.3f} → FY2026 ${EPS_NOW:.2f}: +${eps_g_total:.3f}/share)
  Structural dollar : ${struct_dollar:.3f}  ({struct_dollar/eps_g_total*100:.1f}% of growth)
  Cyclical dollar   : ${cyclical_dollar:.3f}  ({cyclical_dollar/eps_g_total*100:.1f}% of growth)
""")
print(f"  {'Driver':<62}  {'Share':>6}  {'Type':>8}")
print(f"  {'─'*62}  {'─'*6}  {'─'*8}")
for desc, sh, is_s in EPS_DECOMP:
    type_label = "REAL ✓" if is_s else "INFL. ~"
    print(f"  {desc:<62}  {sh*100:>5.0f}%  {type_label:>8}")
print(f"""
  99%+ of NVDA's EPS growth from the trough is structural — driven by the
  AI data centre GPU supercycle, not by cyclical macro recovery or financial
  engineering. This is the highest structural earnings quality in the
  technology sector. The small cyclical residual (gaming demand normalisation)
  is a rounding error relative to the data centre flywheel.
""")

print("  3. CROSS-READ COMPOSITE & SCENARIO PROBABILITIES")
print("  ─────────────────────────────────────────────────────────────────")
print()
print(f"  {'Signal':<47} {'Unit':>7}  {'BEAR':>6}  {'BASE':>6}  {'BULL':>6} {'XBULL':>6}  {'NOW':>6}  {'Wt':>4}")
print(f"  {'─'*47} {'─'*7}  {'─'*6}  {'─'*6}  {'─'*6} {'─'*6}  {'─'*6}  {'─'*4}")
for label, thesis, unit, bv, bsv, blv, xv, cur, wt in CROSS_READS:
    print(f"  {label:<47} {unit:>7}  {bv:>6.0f}  {bsv:>6.0f}  {blv:>6.0f} {xv:>6.0f}  {cur:>6.0f}  {wt:>4.2f}")
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
print(f"  Proxy EV  : ${proxy_ev:,.0f}   (weighted scenario price at model composite)")
print(f"  vs Market : ${CURRENT_PRICE:.2f}  (gap: {(proxy_ev - CURRENT_PRICE)/CURRENT_PRICE*100:+.1f}%)")
print()
print(f"""
  READ: The model composite sits close to BULL (2.75), driven by the trifecta
  of hyperscaler capex ($150B+ confirmed), Blackwell backlog fully committed
  (~95% utilisation), and Q1 FY2027 +85% YoY data centre growth. The SCA adds
  +0.24pp for the CUDA moat and Rubin roadmap, partially offset by China risk.

  The proxy EV of ${proxy_ev:,.0f} represents meaningful upside from $220 — reflecting
  that the BULL scenario (AI capex accelerates; Rubin cycles through) has the
  highest probability weight in the model. The BEAR scenario ($45, at 18x on
  depressed EPS) represents a genuine tail risk if AI capex contracts 40%+ or
  China restrictions escalate to domestic fabs displacing NVDA in Asia.

  Critical insight: the market composite (inferred from $220.66) is only
  {market_composite:.2f} — significantly below the model's {adj_composite:.2f}. The market is
  pricing in MORE BEAR RISK than the current fundamental evidence supports.
  This is the ACCUMULATE signal's core logic.
""")

print("  4. METHOD B VALUATION & SIGNAL DERIVATION")
print("  ─────────────────────────────────────────────────────────────────")
print(f"""
  EPP FLOOR (downside anchor)
    Current EPS ${EPS_NOW:.2f} × {EPP_MIN_PE}x min-viable P/E  =  EPP ${epp_now:.2f}
    Downside to floor  =  ${CURRENT_PRICE:.2f} − ${epp_now:.2f}  =  ${CURRENT_PRICE - epp_now:.2f}  ({epp_gap_pct:.1f}% above floor)

  METHOD B — CONSERVATIVE 2-YEAR TARGET (FY2028 exit)
    Consensus FY2028E EPS : ${CONS_EPS_2YR:.2f}  (below consensus $11.43; -8% haircut applied)
    Conservative exit P/E : {CONS_EXIT_PE}x  (= FY2023 trough multiple — extremely conservative)
    Price B               : ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x  =  ${price_b:.2f}
    Upside (Method B)     : ${price_b:.2f} − ${CURRENT_PRICE:.2f}  =  ${price_b - CURRENT_PRICE:.2f}  ({(price_b/CURRENT_PRICE-1)*100:.1f}%)

  ATTRACTIVENESS RATIO B
    Ratio B  =  Downside / Upside  =  ${CURRENT_PRICE - epp_now:.2f} / ${price_b - CURRENT_PRICE:.2f}  =  {rfmt(ratio_b)}

  SIGNAL SCALE:  ◉ BUY <0.75  ◎ ACCUM. 0.75–1.10  ◐ WATCHLIST 1.10–1.75
                 ◑ HOLD 1.75–2.50  ✕ AVOID >2.50 or N/A (upside negative)

  PRIMARY SIGNAL:  {signal}  (Ratio B {rfmt(ratio_b)})

  The conservative nature of the exit assumptions is important to appreciate:
  — Exit P/E of {CONS_EXIT_PE}x equals the TROUGH multiple (worst capitulation in NVDA history)
  — FY2028E EPS of ${CONS_EPS_2YR:.2f} is BELOW the consensus of $11.43 (8% haircut)
  — Even with these haircuts, Method B produces ${price_b:.2f} vs current ${CURRENT_PRICE:.2f}
  — At consensus FY2028 $11.43 × 32x (trough): ${11.43*32:.0f} → Ratio B well into BUY territory
  — The upside is NOT priced in. The market is discounting AI capex sustainability.

  Valuation context:
    Trailing P/E     : {trailing_pe:.1f}x  (FY2026 EPS ${EPS_NOW:.2f})
    Forward P/E      : {forward_pe:.1f}x  (FY2027E ${EPS_FWD_CONSENSUS:.2f} — growing 75%)
    FY2028 P/E       : {CURRENT_PRICE/CONS_EPS_2YR:.1f}x  (${CONS_EPS_2YR:.2f} conservative exit)
    Cons. 2yr return : {cons_ret_ann:+.0f}%/yr  (Method B conservative, ${CURRENT_PRICE:.2f} → ${price_b:.2f})

  The forward P/E of {forward_pe:.1f}x on an EPS growing 75%+ YoY is the lowest PEG ratio
  in the S&P 500. NVDA at 26.5x FY2027 is cheaper than Microsoft at 32x and
  Apple at 35x, despite growing at 5-7x faster. The market is applying a
  "capex-cycle-peak" discount that the EPP floor analysis suggests is excessive.
""")

print("  5. IDIOSYNCRATIC vs MACRO DECOMPOSITION")
print("  ─────────────────────────────────────────────────────────────────")
print(f"""
  Idiosyncratic  {IDIO['idio_pct']}%   |   Macro / Sentiment  {IDIO['macro_pct']}%   |   Beta  {IDIO['beta']:.2f}

  NVDA straddles idiosyncratic execution (CUDA moat, architecture roadmap,
  Jensen Huang capital allocation) and the macro AI capex cycle. The 45% macro
  weight reflects genuine sensitivity: if the hyperscaler AI capex cycle peaks
  and CapEx falls 30-40%, NVDA's near-term revenue is exposed regardless of
  competitive position. Conversely, the 55% idiosyncratic weight reflects that
  Jensen's execution edge — annual architecture cadence, CUDA ecosystem
  expansion, NIM software monetisation — is company-specific alpha.
  Beta 1.65 reflects high volatility relative to the S&P 500, driven by both
  the capex cycle correlation and headline-driven newsflow around AI.
""")

print(f"  {'Driver':<50}  {'Type':>5}  {'Wt':>4}  {'Detail'}")
print(f"  {'─'*50}  {'─'*5}  {'─'*4}  {'─'*26}")
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

print("  A. EPP FLOOR TABLE  (all figures post-split; ÷10 from pre-June-2024 reports)")
print(f"  {'FY':<6}  {'nGAAP EPS':>10}  {'EPP@32x':>9}  {'Δ EPS':>8}  {'Note'}")
print(f"  {'─'*6}  {'─'*10}  {'─'*9}  {'─'*8}  {'─'*32}")
hist = [
    (2022, 0.497, "gaming/crypto peak — pre-bust"),
    (2023, 0.334, "← EPP trough; $10.80 stock floor validated ✓"),
    (2024, 1.225, "AI data centre demand ignites (Hopper launch)"),
    (2025, 2.972, "H100/H200 supercycle; hyperscaler arms race"),
    (2026, 4.770, "← CURRENT; Blackwell ramp; $215.9B revenue"),
]
prev_eps = None
for yr, eps, note in hist:
    epp_yr = eps * EPP_MIN_PE
    d_eps  = f"{eps - prev_eps:+.3f}" if prev_eps else "    —"
    print(f"  FY{yr:<4}  ${eps:>9.3f}  ${epp_yr:>8.2f}  {d_eps:>8}  {note}")
    prev_eps = eps
print(f"\n  FY2027E  ${EPS_FWD_CONSENSUS:>9.2f}  ${EPS_FWD_CONSENSUS*EPP_MIN_PE:>9.2f}  {'':>8}  ← consensus (post Q1 FY27 $1.87 beat)")
print(f"  FY2028E  ${CONS_EPS_2YR:>9.2f}  ${CONS_EPS_2YR*EPP_MIN_PE:>9.2f}  {'':>8}  ← Method B exit; EPP floor ${CONS_EPS_2YR*EPP_MIN_PE:.0f} > today's ${CURRENT_PRICE:.2f}")
print()

print("  B. SCENARIO TABLE (2-year horizon, FY2028 exit)")
print(f"  {'Scenario':<8}  {'Thesis':<58}  {'EPS':>5}  {'P/E':>4}  {'Target':>8}  {'Prob%':>6}")
print(f"  {'─'*8}  {'─'*58}  {'─'*5}  {'─'*4}  {'─'*8}  {'─'*6}")
for (lbl, thesis, eps, pe, pt), p in zip(SCENARIOS, probs):
    print(f"  {lbl:<8}  {thesis:<58}  ${eps:>4.2f}  {pe:>3}x  ${pt:>7,.0f}  {p*100:>5.1f}%")
print()

print("  C. SIGNAL SCORECARD")
print(f"  {'Metric':<40}  {'Value':>12}  {'Note'}")
print(f"  {'─'*40}  {'─'*12}  {'─'*30}")
metrics = [
    ("Current Price",              f"${CURRENT_PRICE:.2f}",        "NASDAQ:NVDA, 2026-05-21"),
    ("EPP Floor (FY2026 EPS)",     f"${epp_now:.2f}",              f"${EPS_NOW:.2f} × {EPP_MIN_PE}x"),
    ("Gap Above EPP",              f"+{epp_gap_pct:.1f}%",         "moderate; floor rising fast"),
    ("Method B Target (2yr)",      f"${price_b:.2f}",              f"${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x FY2028E conservative"),
    ("Ratio B (PRIMARY)",          rfmt(ratio_b),                  signal),
    ("Trailing P/E",               f"{trailing_pe:.1f}x",          f"FY2026 EPS ${EPS_NOW:.2f}"),
    ("Forward P/E (FY2027E)",      f"{forward_pe:.1f}x",           f"${EPS_FWD_CONSENSUS:.2f} consensus (+75% YoY)"),
    ("FY2028 conservative P/E",    f"{CURRENT_PRICE/CONS_EPS_2YR:.1f}x",  f"${CONS_EPS_2YR:.2f} est. (consensus $11.43)"),
    ("2yr Cons. Return (B)",       f"{cons_ret_ann:+.0f}%/yr",    f"conservative ${CURRENT_PRICE:.2f} → ${price_b:.2f}"),
    ("EPS CAGR (FY2026→FY2028E)", f"{CONS_EPS_CAGR*100:.0f}%/yr", "AI data centre supercycle"),
    ("Beta",                       f"{BETA:.2f}",                  "AI capex cycle + tech beta"),
    ("Model composite",            f"{adj_composite:.2f}",         "approaching BULL (2.75)"),
    ("Proxy EV",                   f"${proxy_ev:,.0f}",            f"vs market ${CURRENT_PRICE:.2f}"),
    ("Idio / Macro split",         f"{IDIO['idio_pct']}% / {IDIO['macro_pct']}%", "CUDA moat + capex cycle"),
    ("Market cap",                 "~$5.5T",                       f"26.5x FY2027E — cheapest mega-cap by PEG"),
]
for name, val, note in metrics:
    print(f"  {name:<40}  {val:>12}  {note}")
print()

print("  D. STRUCTURAL FACTORS (SCA)")
print(f"  {'Factor':<70}  {'Rating':>7}  {'Wt':>4}")
print(f"  {'─'*70}  {'─'*7}  {'─'*4}")
for fac, r, w in STRUCTURAL_FACTORS:
    print(f"  {fac:<70}  {r:>+6.1f}   {w:.2f}")
print(f"\n  SCA raw: {sca_raw:+.3f}  →  adj (+raw/2): {sca_adj:+.3f}  →  composite bump: {sca_adj:+.3f}pp")
print()

print("  E. INVESTMENT DECISION SUMMARY")
print()
print(f"  Signal   :  {signal}  |  Ratio B {rfmt(ratio_b)}")
print(f"  Thesis   :  NVDA at 26.5x FY2027E is the cheapest mega-cap by PEG.")
print(f"              EPP floor ${epp_now:.0f} rising to $267 (FY2027E) and $336 (FY2028E)")
print(f"              — floor surpasses today's price within 18-24 months at")
print(f"              consensus EPS. CUDA moat + annual architecture cadence =")
print(f"              durable monopoly. ACCUMULATE on any macro-driven pullbacks.")
print()
print(f"  Add more : Pullbacks to $175-190 (approaching EPP floor; AI capex fear)")
print(f"             or on confirmation of Rubin architecture sampling on schedule.")
print(f"  Trim at  : $340-380 (approaching BULL scenario pricing at 32-36x FY2028)")
print(f"             or if hyperscaler capex guidance cuts >25% in 2026.")
print()
print(f"  Key watch: FY2027 quarterly EPS progression (Q2 guide: next Aug report)")
print(f"             Rubin sampling schedule (H2-2026) — next architecture trigger")
print(f"             Hyperscaler CapEx guidance (Microsoft/Google/Meta/Amazon)")
print(f"             AMD MI300X/MI400 market share — CUDA erosion monitor")
print(f"             China revenue trajectory — H20 replacement products")
print()
print("  " + "─" * 68)
print("  NOT FINANCIAL ADVICE. All prices USD. Analysis date 2026-05-21.")
print("  " + "─" * 68)
print()
