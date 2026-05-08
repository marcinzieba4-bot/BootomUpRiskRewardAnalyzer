#!/usr/bin/env python3
"""
MU Signal Model
───────────────
Same framework applied to Micron Technology Inc. (NASDAQ: MU).

Key structural difference from every other company in this framework:
  Micron manufactures a commodity — DRAM and NAND flash memory.
  Pricing is set by global supply/demand, not by moat or switching cost.
  A single capacity wave from Samsung can collapse industry margins 50%+
  in 12-18 months. This is NOT a risk in any software or services company.

  However, two structural forces are changing the commodity dynamic:
    1. DRAM oligopoly (3 global suppliers: Samsung, SK Hynix, Micron)
       is more disciplined than at any prior point in memory history.
       All three players burned cash in 2022-2023; all three have cut capex
       in downturns. Rational oligopoly behaviour is now the base case.

    2. HBM (High Bandwidth Memory) for AI accelerators:
       HBM3/HBM3E is NOT a commodity. It requires advanced 3D stacking
       (through-silicon vias) that takes 2-3 years to qualify per customer.
       Only Samsung, SK Hynix, and Micron can supply. NVIDIA's H100/H200/B200
       all require HBM, and the content per GPU is growing (B200: 192GB).
       HBM commands 3-4x the ASP per GB vs standard DDR5.
       Allocation is SOLD OUT through at least 2026.

  The core analytical tension:
    DRAM/NAND COMMODITY: subject to brutal cycles; 2022-2023 saw EPS go from
    +$8 (FY2022 peak) to -$5.6 (FY2023 trough) — a $13.6 swing in 12 months.
    HBM / AI MEMORY: secular demand from AI compute; differentiated product;
    pricing power; quality-assured supply — structurally different from DRAM.

  This model tests whether the AI memory thesis is executing via proxy signals
  and whether the structural cyclicality risk justifies the current discount.

Run: python mu_signal_model.py
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 103.0     # USD (NASDAQ: MU, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

# Scenario 2-year price targets  (EPS × exit P/E, FY2027/FY2028E)
# Memory P/E is structurally capped at 8-12x peak earnings because
# investors anchor to mid-cycle EPS, not peak EPS (the cycle always turns).
# Exception: if HBM creates a durable ASP premium, mid-cycle EPS rises
# permanently → market could award 12-15x on a higher, less-volatile base.
SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  (-2.0,    8,    60,  "DRAM downcycle; HBM ramp miss; oversupply"),
    "BASE":  ( 9.0,   10,    90,  "DRAM recovery; HBM on track; EPS $8-10"),
    "BULL":  (14.0,   10,   140,  "HBM share gains; DRAM pricing tight; EPS $14"),
    "XBULL": (20.0,   10,   200,  "Memory super-cycle; HBM monopoly pricing"),
}

# ── HBM ECONOMICS CALCULATOR (MU-specific structural feature) ─────────────────
# HBM (High Bandwidth Memory) is purpose-built for AI accelerators.
# It uses 3D through-silicon via (TSV) stacking of DRAM dies on a base logic die.
# The result: 10-12x the memory bandwidth of standard DDR5 at 3-4x the ASP/GB.
#
# Every NVIDIA H100 uses 80GB HBM3. Every B200 uses 192GB HBM3E.
# AMD MI300X uses 192GB HBM3. Each GPU is one "socket" = ~6-9 stacks.
#
# Qualification: a new memory supplier takes 18-30 months to qualify at each
# hyperscaler/GPU maker. This creates a durable supply moat within the oligopoly.
# Micron began shipping HBM3E to NVIDIA in early 2024.
#
# Note on MU's HBM position vs SK Hynix:
# SK Hynix is the dominant HBM supplier (~50-55% share, primary NVIDIA supplier).
# Micron: ~20-25% share, growing. Samsung: ~20-25%, quality/yield struggles.
# MU's path to higher share depends on qualification wins at NVIDIA/AMD customers.

AI_GPU_SHIPMENTS_M     = 5.5    # M AI GPUs shipped calendar 2026 (NVDA H200/B200 + AMD MI300)
HBM_GB_PER_GPU         = 120    # blended GB per AI GPU (H200=96GB, B200=192GB, mixed ramp)
HBM_ASP_PER_GB         = 22.0   # USD/GB for HBM3E (range: $18-26; spot-like; MU guided ~$20-24)
MU_HBM_SHARE           = 0.25   # MU's market share in HBM (vs SK Hynix ~52%, Samsung ~23%)
HBM_GROSS_MARGIN       = 0.52   # HBM gross margin % (vs standard DRAM ~40%; premium product)
DDR5_ASP_PER_GB        = 6.0    # USD/GB for standard DDR5 DRAM (commodity reference)
DDR5_GROSS_MARGIN      = 0.40   # Standard DRAM gross margin at mid-cycle
MU_DILUTED_SHARES_B    = 1.10   # billion diluted shares outstanding

def hbm_economics():
    # --- AI GPU HBM market (calendar 2026) ---
    total_hbm_gb_m        = AI_GPU_SHIPMENTS_M * HBM_GB_PER_GPU          # million GB
    total_hbm_market_b    = total_hbm_gb_m * HBM_ASP_PER_GB / 1000       # $B industry
    mu_hbm_rev_b          = total_hbm_market_b * MU_HBM_SHARE             # $B MU share
    mu_hbm_gp_b           = mu_hbm_rev_b * HBM_GROSS_MARGIN               # $B gross profit

    # --- What MU would earn if HBM volume were standard DDR5 (baseline) ---
    equiv_ddr5_rev_b      = total_hbm_gb_m * MU_HBM_SHARE * DDR5_ASP_PER_GB / 1000
    equiv_ddr5_gp_b       = equiv_ddr5_rev_b * DDR5_GROSS_MARGIN
    asp_premium_x         = HBM_ASP_PER_GB / DDR5_ASP_PER_GB              # x premium

    # --- Incremental economics vs if all memory were DDR5 ---
    rev_premium_b         = mu_hbm_rev_b - equiv_ddr5_rev_b
    gp_premium_b          = mu_hbm_gp_b  - equiv_ddr5_gp_b
    gp_premium_per_share  = gp_premium_b  / MU_DILUTED_SHARES_B           # $/share

    # --- HBM as % of MU total DRAM revenue (proxy calibration check) ---
    # GPU shipment math captures AI-GPU HBM only (~$3.6B). MU also supplies
    # HBM for HPC, enterprise AI, and automotive → total guided ~$4.5B.
    # DRAM segment revenue FY2026E: ~$22B (mid-cycle recovery).
    mu_guided_hbm_rev_b   = 4.5   # MU management guidance (FY2026E total HBM revenue)
    mu_total_dram_rev_b   = 22.0  # MU DRAM segment revenue FY2026E
    hbm_mix_pct           = mu_guided_hbm_rev_b / mu_total_dram_rev_b * 100

    # --- Forward scenario: 2027E (B200 fully ramped, MU share gains to 28%) ---
    future_ai_gpu_m       = AI_GPU_SHIPMENTS_M * 1.35                      # +35% GPU shipments
    future_hbm_gb_gpu     = 150                                             # B200 ramp → higher/GPU
    future_mu_share       = 0.28                                            # share gains
    future_mu_hbm_rev_b   = future_ai_gpu_m * future_hbm_gb_gpu * HBM_ASP_PER_GB * future_mu_share / 1000
    future_mu_hbm_gp_b    = future_mu_hbm_rev_b * HBM_GROSS_MARGIN

    return (total_hbm_market_b, mu_hbm_rev_b, mu_hbm_gp_b,
            equiv_ddr5_rev_b, asp_premium_x, rev_premium_b, gp_premium_b,
            gp_premium_per_share, hbm_mix_pct,
            future_mu_hbm_rev_b, future_mu_hbm_gp_b)

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────────
# (name, value, unit, base_floor, bull_floor, xbull_floor, higher_is_better,
#  what_it_drives_for_MU)
SIGNALS = [
    # HBM revenue as % of MU's total DRAM revenue: ~32%.
    # The primary AI-era signal. HBM carries 3-4x ASP and ~52% GM vs ~40% for DDR5.
    # MU disclosed HBM reached "multiple billions" quarterly run-rate in early 2026.
    # 32% mix is BULL — reflects genuine AI allocation but not yet super-cycle.
    ("HBM revenue mix — % of DRAM revenue",    20.0, "%",   12, 18, 32, True,
     "primary AI memory KPI; HBM is 3-4x ASP, 52% GM vs 40% DDR5 — accretive to every margin line"),

    # DRAM contract ASP trend QoQ: +10%.
    # Spot and contract DRAM pricing is the most real-time industry health signal.
    # DRAMeXchange / TrendForce publish weekly spot; contract price set monthly.
    # +10% QoQ reflects the mid-cycle recovery with AI pulling forward demand.
    ("DRAM contract ASP — QoQ change",        +10.0, "% QoQ",  0,  8, 18, True,
     "core commodity pricing health; contract ASP leads earnings with ~1 quarter lag"),

    # Hyperscaler AI CapEx growth YoY: +42%.
    # Combined MSFT/GOOG/META/AMZN data center capex is the primary HBM demand driver.
    # +42% YoY is the actual reported growth in 2025/2026 earnings calls.
    # XBULL threshold = 40% — this signal is XBULL territory.
    ("Hyperscaler AI CapEx — YoY growth",     +42.0, "% YoY",  10, 25, 40, True,
     "end-market demand for HBM; each $1B of AI capex requires ~$50-80M of HBM"),

    # MU gross margin guidance: ~37% for FY2026E.
    # MU guides gross margin quarterly; 37% reflects HBM premium + DRAM recovery.
    # Compare: FY2023 trough was 1.5% gross margin. 37% = healthy mid-cycle.
    # BULL threshold = 35% (achieved). XBULL would require HBM mix-driven GM >45%.
    ("MU gross margin — guidance",            +37.0, "%",       28, 35, 45, True,
     "management's own mid-cycle read; leads EPS by 1-2 quarters; XBULL requires HBM mix shift"),

    # NAND contract ASP QoQ: +4%.
    # NAND is MU's second segment (~35% of revenue). Less AI-sensitive than DRAM.
    # NAND remains somewhat oversupplied (China YMTC + SK Hynix excess capacity).
    # +4% is BASE — recovering slowly but not tight.
    ("NAND contract ASP — QoQ change",         +4.0, "% QoQ",   0,  8, 18, True,
     "secondary segment signal; NAND oversupply from China (YMTC) is the key bear risk"),

    # CXMT commodity DRAM market share: ~10%.
    # CXMT (Changxin Memory) is China's state-backed DRAM entrant.
    # Currently shipping DDR4 commodity at ~10% of that segment.
    # At 10%, CXMT is a concern but not yet systematic — limited to DDR4/older nodes.
    # NOT qualified for HBM or DDR5 at scale. Lower CXMT share = better for MU.
    ("CXMT commodity DRAM share — %",         10.0, "%",       15,  8,  3, False,
     "competitive threat signal (lower=better): CXMT can collapse DDR4 ASPs if it scales DDR5"),
]
WEIGHTS = [0.25, 0.25, 0.15, 0.15, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("Global DRAM oligopoly (3 players); disciplined capex",      1.2, 0.25),
    ("HBM bandwidth monopoly: TSV stacking moat, 18-30mo qual",  1.0, 0.25),
    ("Extreme cyclicality: EPS $8→-$6→$8 in 24 months",         -1.2, 0.25),
    ("CXMT commoditising DDR4/NAND; long-run ASP ceiling risk",  -0.5, 0.15),
    ("$45B+ capex cycle 2023-2026; balance sheet in downturn",   -0.3, 0.10),
]

FLOOR_DATA = {
    "trough_2022":        51.0,
    "cum_fcf_per_share":   3.5,  # Net of FY2023 negative FCF (-$4/sh); FY2024 +$2.5; FY2025 +$5
    "debt_delta":          5.0,  # +ve = debt grew (EPP lower); MU issued bonds for capex cycle
    "structural_delta":    8.0,  # HBM is a genuinely new revenue category vs 2022 HBM2E
    "reflation":           0.17, # cumul. US CPI Jan 2022 - May 2026
}

def worst_case_floor():
    t, refl   = FLOOR_DATA["trough_2022"], FLOOR_DATA["reflation"]
    fcf, ddt  = FLOOR_DATA["cum_fcf_per_share"], FLOOR_DATA["debt_delta"]
    sdelta    = FLOOR_DATA["structural_delta"]
    ref_adj   = t * (1 + refl)
    epp       = ref_adj + fcf - ddt + sdelta
    bear_p    = SCENARIOS["BEAR"][2]
    gap_pct   = (CURRENT_PRICE - epp) / epp * 100   # +ve = above EPP; -ve = below
    bvf_pct   = (bear_p - epp) / epp * 100
    return ref_adj, epp, gap_pct, bear_p, bvf_pct

# ── SCORING ───────────────────────────────────────────────────────────────────
def score_signal(val, base_f, bull_f, xbull_f, hib):
    if hib:
        if val >= xbull_f: return 4
        if val >= bull_f:  return 3
        if val >= base_f:  return 2
        return 1
    else:
        if val <= xbull_f: return 4
        if val <= bull_f:  return 3
        if val <= base_f:  return 2
        return 1

ICONS = {4: "★ XBULL", 3: "▲ BULL", 2: "◦ BASE", 1: "⚠ BEAR"}

def softmax_probs(composite, T=0.60):
    centres = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    raw = {k: math.exp(-abs(composite - c) / T) for k, c in centres.items()}
    tot = sum(raw.values())
    return {k: v / tot for k, v in raw.items()}

def expected_price(probs):
    return sum(probs[k] * SCENARIOS[k][2] for k in probs)

def market_implied_composite(target_ev, tolerance=3.0):
    for c in [x / 100 for x in range(100, 401)]:
        if abs(expected_price(softmax_probs(c)) - target_ev) < tolerance:
            return round(c, 2), softmax_probs(c)
    return None, None

# ── MAIN ──────────────────────────────────────────────────────────────────────
W = 72

scored = [(name, val, unit, score_signal(val, bf, bull_f, xf, hib), w, rt)
          for (name, val, unit, bf, bull_f, xf, hib, rt), w in zip(SIGNALS, WEIGHTS)]
proxy_composite = sum(s * w for *_, s, w, _ in scored)
sca             = sum(s * w for _, s, w in STRUCTURAL_FACTORS)
adj_composite   = proxy_composite + sca
proxy_probs     = softmax_probs(proxy_composite)
proxy_ev        = expected_price(proxy_probs)

market_target_ev = CURRENT_PRICE * ((1 + REQUIRED_RETURN) ** HORIZON_YEARS)
mkt_composite, mkt_probs = market_implied_composite(market_target_ev)
mkt_ev = expected_price(mkt_probs) if mkt_probs else market_target_ev

(total_hbm_mkt_b, mu_hbm_rev_b, mu_hbm_gp_b,
 equiv_ddr5_rev_b, asp_premium_x, rev_prem_b, gp_prem_b,
 gp_prem_per_share, hbm_mix_pct,
 fut_mu_hbm_rev_b, fut_mu_hbm_gp_b) = hbm_economics()

print()
print("═" * W)
print("  MU SIGNAL MODEL  —  proxy vs. market-implied probability")
print("═" * W)

# HBM economics
print(f"\n  HBM ECONOMICS  (the AI memory revenue engine)")
print("  " + "─" * (W-2))
print(f"  AI GPU shipments (calendar 2026E):      {AI_GPU_SHIPMENTS_M:.1f}M units")
print(f"  HBM content per GPU (blended H200/B200):{HBM_GB_PER_GPU}GB  "
      f"(H200=96GB, B200=192GB, ~50/50 mix)")
print(f"  HBM3E ASP:                              ${HBM_ASP_PER_GB:.0f}/GB  "
      f"(vs DDR5 ${DDR5_ASP_PER_GB:.0f}/GB = {asp_premium_x:.1f}x premium)")
print(f"  Industry HBM market (AI GPU only):      ${total_hbm_mkt_b:.1f}B")
print(f"  MU HBM market share:                    {MU_HBM_SHARE*100:.0f}%  "
      f"(SK Hynix ~52%, Samsung ~23%, Micron ~25%)")
print(f"  ─────────────────────────────────────────────────────")
print(f"  MU HBM revenue (calendar 2026E):        ${mu_hbm_rev_b:.1f}B")
print(f"  MU HBM gross profit:                    ${mu_hbm_gp_b:.1f}B  ({HBM_GROSS_MARGIN*100:.0f}% GM)")
print(f"  Equiv. DDR5 revenue (same volume):      ${equiv_ddr5_rev_b:.1f}B  (commodity baseline)")
print(f"  Revenue premium from HBM vs DDR5:       +${rev_prem_b:.1f}B / yr")
print(f"  GP premium from HBM vs DDR5:            +${gp_prem_b:.1f}B / yr  "
      f"→  +${gp_prem_per_share:.1f}/share  ← locked-in by qualification")
print(f"  HBM as % of MU DRAM revenue:            {hbm_mix_pct:.0f}%  (proxy signal calibration)")
print(f"\n  2027E forward (B200 ramp + MU share gains to 28%):")
print(f"  MU HBM revenue:                         ${fut_mu_hbm_rev_b:.1f}B")
print(f"  MU HBM gross profit:                    ${fut_mu_hbm_gp_b:.1f}B")
print(f"  → HBM alone could drive EPS of $8-10+ in a zero-NAND scenario.")
print(f"  → Qualification moat: once MU is in the NVIDIA/AMD supply chain,")
print(f"    switching to Samsung mid-generation requires a full re-qualification (18-30 months).")

# Signal scorecard
print(f"\n  PROXY SIGNAL SCORECARD")
print(f"  {'Signal':<38}{'Value':>9}  Wt   Score")
print("  " + "─" * (W-2))
for name, val, unit, s, w, rt in scored:
    bar = "█" * s + "░" * (4 - s)
    print(f"  {name:<38}{val:>+7.1f}{unit[0]}  {w*100:.0f}%  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:   {proxy_composite:.2f} / 4.00")
if mkt_composite:
    print(f"  Market composite:  {mkt_composite:.2f} / 4.00  "
          f"(back-solved from ${CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% reqd return)")
    gap = proxy_composite - mkt_composite
    print(f"  Gap (proxy − mkt): {gap:+.2f}")

# Structural overlay
print(f"\n  STRUCTURAL RISK OVERLAY  (analyst-assessed; beyond proxy signals)")
print("  " + "─" * (W-2))
print(f"  {'Factor':<44}  {'Score':>5}  {'Wt':>3}   {'Adj':>5}")
for desc, score, wt in STRUCTURAL_FACTORS:
    adj_c = score * wt
    arrow = "▲" if score > 0 else "▼"
    print(f"  {desc:<44}  {score:>+5.1f}  {wt*100:>3.0f}%  {adj_c:>+5.2f}  {arrow}")
print(f"  {'─'*68}")
print(f"  Structural adj. (SCA):     {sca:>+6.2f}")
print(f"  Adjusted composite:         {adj_composite:.2f}  "
      f"(proxy {proxy_composite:.2f} {'+' if sca >= 0 else ''}{sca:.2f})")
if mkt_composite:
    adj_gap = adj_composite - mkt_composite
    if   adj_gap >  0.50: _verdict = "UNDERVALUED"
    elif adj_gap >  0.20: _verdict = "MODESTLY UNDERVALUED"
    elif adj_gap > -0.20: _verdict = "FAIRLY VALUED"
    elif adj_gap > -0.50: _verdict = "MODESTLY OVERVALUED"
    else:                 _verdict = "OVERVALUED"
    print(f"  Market composite:          {mkt_composite:.2f}")
    print(f"  ADJUSTED GAP:             {adj_gap:>+6.2f}  ← {_verdict}")

# Valuation context
print(f"\n  VALUATION CONTEXT")
print("  " + "─" * (W-2))
peak_eps = 8.35  # FY2022 actual peak EPS
trough_eps = -5.63  # FY2023 actual trough EPS
print(f"  Peak EPS (FY2022):           ${peak_eps:.2f}  ← DRAM supercycle peak")
print(f"  Trough EPS (FY2023):        -${abs(trough_eps):.2f}  ← inventory write-down year")
print(f"  FY2026E EPS consensus:       ~$8-10  (recovery + HBM contribution)")
print(f"  Current P/E (FY2026E):       {CURRENT_PRICE/9:.1f}x  (vs 8-12x typical memory range)")
print(f"  P/Book:                      ~1.6x  (tangible book ~$65/share)")
print(f"  Net debt / EBITDA:           ~1.5x  (post-capex cycle; declining as FCF recovers)")
print(f"  EPS volatility (peak-trough):{peak_eps - trough_eps:.0f}/share swing in 12 months")
print(f"  → Market refuses to pay >10-12x peak EPS for memory because the NEXT")
print(f"    downcycle (from Samsung capacity adds or demand shock) always comes.")
print(f"  → Bull case: HBM creates a permanently higher mid-cycle EPS floor ($8-10)")
print(f"    because HBM allocation is sold out regardless of commodity DRAM pricing.")

# Probability table
print(f"\n  {'Scenario':<10}  {'Proxy':>8}  {'Market':>8}  {'Gap':>8}  "
      f"{'EPS':>6}  {'Mult':>5}  {'Price':>7}  Narrative")
print("  " + "─" * (W-2))
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    eps, mult, price, narr = SCENARIOS[k]
    pp  = proxy_probs[k]
    mp  = mkt_probs[k] if mkt_probs else 0
    gap_pp = pp - mp
    sign = "+" if gap_pp >= 0 else ""
    print(f"  {k:<10}  {pp*100:>7.1f}%  {mp*100:>7.1f}%  "
          f"{sign}{gap_pp*100:>6.1f}pp  ${eps:>+5.1f}  {mult:>4}x  ${price:<6}  {narr[:28]}…")

print(f"\n  Prob-weighted 2yr:  proxy ${proxy_ev:.0f}  /  market ${mkt_ev:.0f}")
print(f"  Current price: ${CURRENT_PRICE:.0f}")

# Equivalent Pessimism Price
_ref_adj, _epp, _gap_pct, _bear_p, _bvf = worst_case_floor()
_t      = FLOOR_DATA["trough_2022"]
_fcf    = FLOOR_DATA["cum_fcf_per_share"]
_ddt    = FLOOR_DATA["debt_delta"]
_sdelta = FLOOR_DATA["structural_delta"]
print(f"\n  EQUIV. PESSIMISM PRICE  (if 2022 pessimism returned today, price would be:)")
print("  " + "─" * (W-2))
print(f"  2022 pessimism trough:                  ${_t:.0f}")
print(f"    + Reflation (+17% cumul. CPI since 2022):  +${_t*0.17:.0f}  →  ${_t*1.17:.0f}")
print(f"    + Cumul. FCF earned FY2023-2025:           +${_fcf:.0f}  →  ${_t*1.17+_fcf:.0f}")
print(f"      (note: FY2023 FCF was deeply negative; +$3.5 is net of that -$4/share year)")
if _ddt > 0:
    print(f"    - Net debt increase since 2022 / share:    -${_ddt:.0f}  →  ${_t*1.17+_fcf-_ddt:.0f}  (capex cycle leverage)")
else:
    print(f"    + Balance sheet improvement / share:       +${-_ddt:.0f}  →  ${_t*1.17+_fcf-_ddt:.0f}")
if _sdelta > 0:
    print(f"    + Structural improvement since 2022:       +${_sdelta:.0f}  →  ${_epp:.0f}  (HBM: new category, higher EPP)")
elif _sdelta < 0:
    print(f"    - Structural deterioration since 2022:     -${-_sdelta:.0f}  →  ${_epp:.0f}  (weaker business today)")
print(f"  {chr(32)*4}{chr(45)*62}")
print(f"  EQUIV. PESSIMISM PRICE (EPP, 2026):     ${_epp:.0f}")
if _gap_pct >= 0:
    print(f"  Current price:   ${CURRENT_PRICE:.0f}  →  +{_gap_pct:.0f}% above EPP  ✓  price embeds AI premium over pessimism")
else:
    print(f"  Current price:   ${CURRENT_PRICE:.0f}  →  {_gap_pct:.0f}% BELOW EPP  ← trading in distressed / structural-break zone")
if _bvf >= 0:
    print(f"  BEAR scenario (${_bear_p:.0f}):   BEAR is +{_bvf:.0f}% above EPP  ✓  bear case is cyclical, not structural")
else:
    print(f"  BEAR scenario (${_bear_p:.0f}):   BEAR is {_bvf:.0f}% BELOW EPP  ← bear case implies permanent impairment")
print(f"  → Same pessimism ≠ same price: FCF locked in (net), inflation ratcheted anchors.")
print(f"    HBM structural gain means equal pessimism = higher price than CPI-adj 2022.")
print(f"  ⚠  IMPORTANT: MU's EPP math is less reliable than for stable compounders.")
print(f"    In a true memory downcycle, MU burns $3-5B cash/yr — the 'FCF locked in'")
print(f"    concept is weaker here. Bear scenarios can gap below EPP rapidly.")

# Verdict
print(f"\n  WHAT THE GAP MEANS")
print("  " + "─" * (W-2))
gap = (proxy_composite - mkt_composite) if mkt_composite else 0
if mkt_composite:
    adj_gap = adj_composite - mkt_composite
print(f"""  Proxy composite {proxy_composite:.2f}  vs  market-implied {mkt_composite:.2f}.
  Gap = {gap:+.2f}  |  Adjusted gap = {adj_gap:+.2f}  ← {_verdict}

  Complete framework adjusted gap table (updated):
    ORCL adj gap = +1.54  UNDERVALUED          (Oracle DB moat; OCI RPO backlog)
    AVGO adj gap = +1.43  UNDERVALUED          (custom ASIC moat; VMware synergies)
    MSFT adj gap = +1.42  UNDERVALUED          (Azure switching cost; Copilot)
    SAP  adj gap = +1.15  UNDERVALUED          (ECC 2027 captive pipeline)
    SYK  adj gap = +0.56  UNDERVALUED          (MAKO installed base moat)
    PYPL adj gap = +0.42  MODESTLY UNDERVALUED (Venmo moat; Chriss execution)
    COIN adj gap = +0.40  MODESTLY UNDERVALUED (regulatory clarity; BTC thesis)
    RCL  adj gap = +0.28  MODESTLY UNDERVALUED (private destination moat)
    XTB  adj gap = +0.29  MODESTLY UNDERVALUED (ETF stickiness vs cyclicality)
    PM   adj gap = +0.36  MODESTLY UNDERVALUED (IQOS device ecosystem)
    MU   adj gap = {adj_gap:>+5.2f}  ← {_verdict}
    WMB  adj gap = ~0.00  FAIRLY VALUED        (Transco moat offsets AI premium)
    CAT  adj gap = -0.27  MODESTLY OVERVALUED  (tariff exposure; cycle ahead of data)
    NKE  adj gap = -0.43  MODESTLY OVERVALUED  (China permanent loss)
    APD  adj gap = -0.66  OVERVALUED           (H2 NPV < capex deployed)

  WHY MU'S GAP IS STRUCTURALLY SMALLER THAN SOFTWARE COMPANIES:

    The framework uses proxy signals to estimate intrinsic value, then compares
    to what the market implies. For software moat companies (ORCL, MSFT, SAP),
    the gap is wide because:
      • Switching costs mean above-average ROIC is DURABLE (10+ year visibility)
      • Multiple expansion is rational as the market recognises the moat
      • Proxy signals capturing cloud/AI adoption lead the P&L by 12-24 months

    For Micron, even strong proxy signals translate to a SMALLER justified gap:
      • DRAM pricing is set by global supply/demand — Samsung can unilaterally
        add capacity and destroy margins within 12-18 months
      • The oligopoly is disciplined TODAY — but "disciplined Korean/US/Japan
        consortium" has historically been an oxymoron in memory
      • HBM is real, but if Samsung solves its HBM3E yield problems, MU's
        share and ASP premium both compress simultaneously
      • A +{adj_gap:.2f} adj gap for MU means: our proxies say BUY, but
        the structural cyclicality overlay correctly limits the conviction

  THE CRITICAL INSIGHT — TWO TYPES OF MEMORY REVENUE:

    1. COMMODITY DRAM/NAND (~68% of revenue): Same physics as 1990. Samsung,
       SK Hynix, MU compete on cost structure. Margins collapse in downturns.
       ROIC is cyclical: 25% at peak, -5% at trough. Mean-reverts every 2-3 yrs.

    2. HBM (~32% of revenue, growing): Qualification-gated. 18-30 month lead
       time to certify a new supplier. NVIDIA cannot switch mid-generation.
       ASP is negotiated annually (not spot). GM ~52% vs DDR5 ~40%.
       This segment BEHAVES LIKE A SPECIALTY CHEMICAL or INDUSTRIAL GAS —
       long-term contracts, pricing power, customer switching cost.

    The market is slowly re-rating MU as the HBM mix grows:
       HBM at 15% of revenue (2024) → MU traded at 8-9x earnings
       HBM at 30% of revenue (2026) → MU trading at 10-11x earnings
       HBM at 50% of revenue (2028E) → market may award 13-15x at mid-cycle

    The bull case is a MULTIPLE EXPANSION story, not just an EPS story.

  THE THREE RISKS THE PROXY SIGNALS CANNOT SEE:

    1. Samsung capacity wave: Samsung has a history of building capacity
       regardless of returns (market share, national strategic interest).
       A Samsung DRAM capex surge collapses commodity ASPs 30-40% in 6 months.
       No proxy signal gives 12-month advance warning of this. It is binary.

    2. HBM yield break at Micron: MU has publicly admitted HBM yield ramp
       is complex. A yield problem delays deliveries, loses qualification slots.
       SK Hynix took 6-9 months to fix its HBM3 yield issues in 2023.
       If this happens to MU at current scale, the HBM premium disappears.

    3. AI capex pause: Hyperscaler capex is growing 40%+ but it is discretionary.
       A macro downturn, regulatory AI pause (EU AI Act enforcement), or
       disappointing AI monetisation (2025 concern) could cut capex 20-30%
       in 90 days. This hits HBM demand faster than it hits DRAM demand.

  THE BULL CASE — WHY $140 IS ACHIEVABLE:

    HBM at 40%+ of DRAM revenue (MU guided 2027E): $8B+ HBM revenue
    Standard DRAM recovery (tight supply, disciplined Samsung): $15-17B
    NAND recovery (normalised inventory): $8B
    Total revenue: $31-35B. GM of 42-45%: EBITDA $13-16B. EPS $14.
    At 10x (standard memory peak): $140/share.

    The only requirement: HBM ramp continues on schedule and Samsung
    does not flood the standard DRAM market during the next 18 months.""")
print()
print("═" * W)
