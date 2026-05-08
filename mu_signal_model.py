#!/usr/bin/env python3
"""
MU Signal Model  v2
───────────────────
Micron Technology Inc. (NASDAQ: MU)  ·  Semiconductors

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 730.0     # USD (NASDAQ: MU, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  (-5.0,    8,   250,  "DRAM crash; HBM ramp miss; Samsung floods market; FCF negative"),
    "BASE":  (42.0,   15,   630,  "HBM scaling; DRAM mid-cycle; EPS $40-45"),
    "BULL":  (58.0,   18,  1044,  "HBM dominant; DRAM tight; AI allocation sold out; EPS $55+"),
    "XBULL": (80.0,   20,  1600,  "Memory super-cycle; HBM pricing power; AI compute unabated"),
}

# ── HBM ECONOMICS CALCULATOR (MU-specific structural feature) ─────────────────
AI_GPU_SHIPMENTS_M     = 8.5    # B200/B300 ramp + MI350; strong 2026 datacenter build
HBM_GB_PER_GPU         = 144    # B200=192GB dominant; blended higher than 2025
HBM_ASP_PER_GB         = 25.0   # firmed up; allocated supply; MU guided $24-26
MU_HBM_SHARE           = 0.28   # gaining share vs SK Hynix ~48%, Samsung ~24%
HBM_GROSS_MARGIN       = 0.58   # scale benefits; well above DDR5
DDR5_ASP_PER_GB        = 7.0    # firmed post-trough; mid-cycle recovery
DDR5_GROSS_MARGIN      = 0.42   # mid-cycle
MU_DILUTED_SHARES_B    = 1.11   # diluted shares

def hbm_economics():
    total_hbm_gb_m        = AI_GPU_SHIPMENTS_M * HBM_GB_PER_GPU
    total_hbm_market_b    = total_hbm_gb_m * HBM_ASP_PER_GB / 1000
    mu_hbm_rev_b          = total_hbm_market_b * MU_HBM_SHARE
    mu_hbm_gp_b           = mu_hbm_rev_b * HBM_GROSS_MARGIN
    equiv_ddr5_rev_b      = total_hbm_gb_m * MU_HBM_SHARE * DDR5_ASP_PER_GB / 1000
    equiv_ddr5_gp_b       = equiv_ddr5_rev_b * DDR5_GROSS_MARGIN
    asp_premium_x         = HBM_ASP_PER_GB / DDR5_ASP_PER_GB
    rev_premium_b         = mu_hbm_rev_b - equiv_ddr5_rev_b
    gp_premium_b          = mu_hbm_gp_b  - equiv_ddr5_gp_b
    gp_premium_per_share  = gp_premium_b  / MU_DILUTED_SHARES_B
    mu_guided_hbm_rev_b   = 8.0    # MU FY2026E HBM revenue guidance
    mu_total_dram_rev_b   = 28.0   # MU DRAM segment FY2026E (recovery + HBM mix)
    hbm_mix_pct           = mu_guided_hbm_rev_b / mu_total_dram_rev_b * 100
    future_ai_gpu_m       = AI_GPU_SHIPMENTS_M * 1.35
    future_hbm_gb_gpu     = 150
    future_mu_share       = 0.28
    future_mu_hbm_rev_b   = future_ai_gpu_m * future_hbm_gb_gpu * HBM_ASP_PER_GB * future_mu_share / 1000
    future_mu_hbm_gp_b    = future_mu_hbm_rev_b * HBM_GROSS_MARGIN
    return (total_hbm_market_b, mu_hbm_rev_b, mu_hbm_gp_b,
            equiv_ddr5_rev_b, asp_premium_x, rev_premium_b, gp_premium_b,
            gp_premium_per_share, hbm_mix_pct,
            future_mu_hbm_rev_b, future_mu_hbm_gp_b)

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────────
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("HBM revenue mix — % of DRAM revenue",    "%",
      5.0,  12, 18, 32,   38.0, True,
     "HBM ramp miss; GPU demand fails to materialize"),

    ("DRAM contract ASP — QoQ change",        "% QoQ",
    -12.0,   0,  8, 18,  +18.0, True,
     "Samsung capacity surge; DDR5 contract prices collapse"),

    ("Hyperscaler AI CapEx — YoY growth",     "% YoY",
      0.0,  10, 25, 40,  +55.0, True,
     "AI capex pause; hyperscalers pull back spending"),

    ("MU gross margin — guidance",            "%",
     15.0,  28, 35, 45,  +48.0, True,
     "Inventory glut; underutilisation charges hit GM"),

    ("NAND contract ASP — QoQ change",        "% QoQ",
    -15.0,   0,  8, 18,  +14.0, True,
     "YMTC/NAND oversupply; Chinese dumping"),

    ("CXMT commodity DRAM share — %",         "%",
     30.0,  15,  8,  3,    8.0, False,
     "CXMT qualifies DDR5; commodity ASP ceiling set"),
]
WEIGHTS = [0.25, 0.25, 0.15, 0.15, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("Global DRAM oligopoly (3 players); disciplined capex",      1.2, 0.25),
    ("HBM bandwidth monopoly: TSV stacking moat, 18-30mo qual",  1.0, 0.25),
    ("Extreme cyclicality: EPS $42→-$5→$42 possible in 24 months", -1.2, 0.25),
    ("CXMT commoditising DDR4/NAND; long-run ASP ceiling risk",  -0.5, 0.15),
    ("$45B+ capex cycle 2023-2026; balance sheet in downturn",   -0.3, 0.10),
]

# ── UPDATED EPP ─────────────────────────────────────────────────────────────
EPP_TODAY_EPS      = 42.0   # FY2026E non-GAAP EPS (HBM + DRAM recovery in full swing)
EPP_MIN_PE         = 8.0    # min viable P/E at panic (memory trough multiple; unchanged)
EPP_HISTORICAL     = 57.0   # historical EPP v1 (2022 floor formula)
EPP_REGIME_NOTE    = "(memory panic P/E = 8x; HBM moat does NOT prevent multiple collapse in downcycle)"

# ── CONSERVATIVE GROWTH (2-yr, base-minus assumptions) ───────────────────────
CONS_SIGNALS = [
    ("HBM revenue mix",    30.0,  "30% (vs 38%; AI capex normalises to 2025 pace)"),
    ("DRAM contract",       5.0,  "+5% QoQ (vs +18%; cycle peaks; pricing cools)"),
    ("Hyperscaler AI",     25.0,  "+25%/yr (vs +55%; capex growth decelerates)"),
    ("MU gross margin",    42.0,  "42% (vs 48%; HBM mix growth slows)"),
    ("NAND contract",       3.0,  "+3% QoQ (vs +14%; modest NAND drift)"),
    ("CXMT commodity",     11.0,  "11% (vs 8%; modest CXMT creep into DDR5)"),
]
CONS_EPS_CAGR    = 0.05    # 5%/yr (peak-cycle EPS; normalisation incoming)
CONS_EXIT_PE     = 12.0    # 12x (mid-cycle de-rate; market prices next downcycle)
CONS_DIVIDEND    = 0.0     # no meaningful dividend

# ── VOLATILITY ───────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT   = 0.55    # very high vol; cyclical semiconductor
VOL_BETA         = 1.80    # high beta
VOL_52W_LOW      = 350.0   # approx (dipped on DRAM oversupply fears mid-2025)
VOL_52W_HIGH     = 790.0   # approx (recent AI-driven high)
VOL_DIVIDEND     = 0.0

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

def market_implied_composite(target_ev, tolerance=8.0):
    for c in [x / 100 for x in range(100, 401)]:
        if abs(expected_price(softmax_probs(c)) - target_ev) < tolerance:
            return round(c, 2), softmax_probs(c)
    return None, None

# ── COMPUTE ───────────────────────────────────────────────────────────────────
W = 72

scored = [
    (name, unit, bv, bf, blf, xf, cv, hib, narr,
     score_signal(cv, bf, blf, xf, hib), w)
    for (name, unit, bv, bf, blf, xf, cv, hib, narr), w
    in zip(SIGNALS, WEIGHTS)
]
proxy_composite  = sum(s * w for *_, s, w in scored)
bear_composite   = sum(score_signal(bv, bf, blf, xf, hib) * w
                       for (_, __, bv, bf, blf, xf, ___, hib, ____), w
                       in zip(SIGNALS, WEIGHTS))
sca              = sum(s * w for _, s, w in STRUCTURAL_FACTORS)
adj_composite    = proxy_composite + sca
proxy_probs      = softmax_probs(proxy_composite)
bear_probs       = softmax_probs(bear_composite)
proxy_ev         = expected_price(proxy_probs)
bear_ev          = expected_price(bear_probs)

market_target_ev = CURRENT_PRICE * ((1 + REQUIRED_RETURN) ** HORIZON_YEARS)
mkt_composite, mkt_probs = market_implied_composite(market_target_ev)
mkt_ev = expected_price(mkt_probs) if mkt_probs else market_target_ev

# Updated EPP
epp_updated     = EPP_TODAY_EPS * EPP_MIN_PE
epp_gap_pct     = (CURRENT_PRICE - epp_updated) / epp_updated * 100
bear_vs_epp_pct = (SCENARIOS["BEAR"][2] - epp_updated) / epp_updated * 100

# Conservative growth
cons_eps_2yr    = EPP_TODAY_EPS * ((1 + CONS_EPS_CAGR) ** 2)
cons_price_2yr  = cons_eps_2yr * CONS_EXIT_PE
cons_div_2yr    = 0.0   # no dividend
cons_total_ret  = (cons_price_2yr - CURRENT_PRICE + cons_div_2yr) / CURRENT_PRICE * 100
cons_annual_ret = cons_total_ret / 2

# Volatility
sigma_1yr         = CURRENT_PRICE * VOL_ANNUAL_PCT
vol_low_1yr       = CURRENT_PRICE - sigma_1yr
vol_high_1yr      = CURRENT_PRICE + sigma_1yr
sigma_needed_bear = (CURRENT_PRICE - SCENARIOS["BEAR"][2]) / sigma_1yr

if mkt_composite:
    adj_gap = adj_composite - mkt_composite
    if   adj_gap >  0.50: _verdict = "UNDERVALUED"
    elif adj_gap >  0.20: _verdict = "MODESTLY UNDERVALUED"
    elif adj_gap > -0.20: _verdict = "FAIRLY VALUED"
    elif adj_gap > -0.50: _verdict = "MODESTLY OVERVALUED"
    else:                 _verdict = "OVERVALUED"

(total_hbm_mkt_b, mu_hbm_rev_b, mu_hbm_gp_b,
 equiv_ddr5_rev_b, asp_premium_x, rev_prem_b, gp_prem_b,
 gp_prem_per_share, hbm_mix_pct,
 fut_mu_hbm_rev_b, fut_mu_hbm_gp_b) = hbm_economics()

# ── OUTPUT ────────────────────────────────────────────────────────────────────
print()
print("═" * W)
print(f"  MU  ·  Micron Technology  ·  ${CURRENT_PRICE:.2f}  ·  Semiconductors")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

# HBM economics
print(f"\n  HBM ECONOMICS  (the AI memory revenue engine)")
print("  " + "─" * (W-2))
print(f"  AI GPU shipments (calendar 2026E):      {AI_GPU_SHIPMENTS_M:.1f}M units")
print(f"  HBM content per GPU (blended B200/H200): {HBM_GB_PER_GPU}GB  "
      f"(B200=192GB dominant; H100=80GB phasing out)")
print(f"  HBM3E ASP:                              ${HBM_ASP_PER_GB:.0f}/GB  "
      f"(vs DDR5 ${DDR5_ASP_PER_GB:.0f}/GB = {asp_premium_x:.1f}x premium)")
print(f"  Industry HBM market (AI GPU only):      ${total_hbm_mkt_b:.1f}B")
print(f"  MU HBM market share:                    {MU_HBM_SHARE*100:.0f}%  "
      f"(SK Hynix ~48%, Samsung ~24%, Micron ~28%)")
print(f"  ─────────────────────────────────────────────────────")
print(f"  MU HBM revenue (calendar 2026E):        ${mu_hbm_rev_b:.1f}B")
print(f"  MU HBM gross profit:                    ${mu_hbm_gp_b:.1f}B  ({HBM_GROSS_MARGIN*100:.0f}% GM)")
print(f"  Equiv. DDR5 revenue (same volume):      ${equiv_ddr5_rev_b:.1f}B  (commodity baseline)")
print(f"  Revenue premium from HBM vs DDR5:       +${rev_prem_b:.1f}B / yr")
print(f"  GP premium from HBM vs DDR5:            +${gp_prem_b:.1f}B / yr  "
      f"→  +${gp_prem_per_share:.1f}/share  ← locked-in by qualification")
print(f"  HBM as % of MU DRAM revenue:            {hbm_mix_pct:.0f}%  (proxy signal calibration)")
print(f"\n  2027E forward (B300 ramp + MU share stable at 28%):")
print(f"  MU HBM revenue:                         ${fut_mu_hbm_rev_b:.1f}B")
print(f"  MU HBM gross profit:                    ${fut_mu_hbm_gp_b:.1f}B")
print(f"  → HBM drives $35-40+ EPS at current pricing; DRAM/NAND is incremental.")

# ── ① SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print(f"\n  ① SIGNAL DASHBOARD")
print(f"  {'Signal':<30}  {'BEAR':>7}  {'BASE≥':>7}  {'BULL≥':>7}  {'XBULL≥':>7}  {'NOW':>7}  Score")
print("  " + "─" * (W-2))
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u = unit.split()[0] if unit else ""
    bv_s  = f"{bv:+.0f}{u}"  if hib else f">{bv:.1f}{u}"
    bf_s  = f"{bf:.0f}{u}"
    blf_s = f"{blf:.0f}{u}"
    xf_s  = f"{xf:.0f}{u}"
    cv_s  = f"{cv:+.0f}{u}"
    bar   = "█" * s + "░" * (4 - s)
    print(f"  {name:<30}  {bv_s:>7}  {bf_s:>7}  {blf_s:>7}  {xf_s:>7}  {cv_s:>7}  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:    {proxy_composite:.2f} / 4.00")
if mkt_composite:
    print(f"  Market composite:   {mkt_composite:.2f} / 4.00  "
          f"(back-solved from ${CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% hurdle)")
    print(f"  SCA adjustment:    {sca:+.2f}  →  Adj composite {adj_composite:.2f}  "
          f"→  Gap {adj_gap:+.2f}  [{_verdict}]")

print(f"\n  Structural factors:")
for desc, score, wt in STRUCTURAL_FACTORS:
    arrow = "  +" if score > 0 else "  -"
    print(f"  {arrow}  {desc}  ({score:+.1f} × {wt*100:.0f}%  =  {score*wt:+.2f})")

# ── ② BEAR CASE ANATOMY ──────────────────────────────────────────────────────
print(f"\n  ② BEAR CASE ANATOMY  (what variables need to do for BEAR to materialise)")
print("  " + "─" * (W-2))
print(f"  {'Signal':<30}  {'Current':>8}  {'Bear val':>8}  Move    Trigger")
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u      = unit.split()[0] if unit else ""
    cv_s   = f"{cv:+.0f}{u}"
    bv_s   = f"{bv:+.0f}{u}"
    move   = bv - cv
    move_s = f"{move:+.0f}{u}"
    trigger = narr[:38] if len(narr) <= 38 else narr[:35] + "…"
    print(f"  {name:<30}  {cv_s:>8}  {bv_s:>8}  {move_s:>6}  {trigger}")

bear_model_price = expected_price(bear_probs)
print(f"\n  Bear composite:  {bear_composite:.2f}  →  Bear scenario price: "
      f"~${bear_model_price:.0f}  (model)  /  ${SCENARIOS['BEAR'][2]} (defined)")
print(f"  Bear probability (proxy model):  {proxy_probs['BEAR']*100:.1f}%")
print(f"\n  KEY TRIGGER: Samsung capacity surge ($20B+ DRAM capex) + AI capex deceleration <20% simultaneously.")
print(f"  MU's HBM qualification does NOT prevent ASP collapse if SK Hynix/Samsung flood commodity DRAM.")
print(f"  FCF goes deeply negative ($3-5B cash burn/yr) — the '$42 EPS floor' disappears fast.")

# ── ③ UPDATED EPP ────────────────────────────────────────────────────────────
print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS:          ${EPP_TODAY_EPS:.2f}  (FY2026E non-GAAP)")
print(f"  Min viable P/E at panic:          {EPP_MIN_PE:.0f}x  {EPP_REGIME_NOTE}")
print(f"  {'─'*60}")
print(f"  UPDATED EPP:                     ${epp_updated:.0f}/share")
print(f"  Historical EPP (v1, floor adj):  ${EPP_HISTORICAL:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.0f} vs Updated EPP ${epp_updated:.0f}:  {epp_gap_pct:+.0f}%  {'✓ cushion' if epp_gap_pct >= 0 else '← in distressed zone'}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} vs Updated EPP ${epp_updated:.0f}:  {bear_vs_epp_pct:+.0f}%  {'← BEAR requires earnings impairment' if bear_vs_epp_pct < 0 else '✓ bear is cyclical'}")

# ── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print(f"\n  ④ CONSERVATIVE GROWTH  (2-yr, signals at BASE lower bound — no tailwinds)")
print("  " + "─" * (W-2))
print(f"  {'Signal':<30}  {'Conservative':>14}  vs Current  Rationale")
for sname, sval, srat in CONS_SIGNALS:
    cur = next(cv for name, _, __, ___, ____, _____, cv, ______, _______ in SIGNALS
               if name.lower().startswith(sname.split()[0].lower()))
    diff = sval - cur
    diff_s = f"{diff:+.0f}"
    print(f"  {sname:<30}  {sval:>14.1f}  {diff_s:>9}   {srat[:30]}")

print(f"\n  Conservative 2yr EPS:   ${EPP_TODAY_EPS:.2f} × "
      f"(1+{CONS_EPS_CAGR*100:.0f}%)² = ${cons_eps_2yr:.2f}")
print(f"  At {CONS_EXIT_PE:.0f}x P/E (no multiple expansion):  ${cons_price_2yr:.0f}/share")
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:    ${cons_price_2yr:.0f}  "
      f"({'▲' if cons_price_2yr > CURRENT_PRICE else '▼'}{abs(cons_price_2yr - CURRENT_PRICE):.0f} "
      f"from ${CURRENT_PRICE:.0f})")
print(f"  Conservative total return: {cons_total_ret:+.0f}% over 2yr  "
      f"= {cons_annual_ret:+.0f}%/yr  (incl. dividend)")
print(f"\n  ⚠  AT PEAK CYCLE: conservative 2yr = negative total return. Market prices in continued perfection.")
print(f"  MU at $730 is a BULL/XBULL conviction bet — conservative case implies -20%+ from current.")

# ── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        ${VOL_52W_LOW:.0f}  –  ${VOL_52W_HIGH:.0f}")
if VOL_DIVIDEND > 0:
    print(f"  Annual dividend:      ${VOL_DIVIDEND:.2f}/share  "
          f"(yield {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%)")
else:
    print(f"  Dividend:             None")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized")
print(f"  Beta vs S&P 500:      {VOL_BETA:.2f}")
print(f"  1-sigma range (1yr):  ${vol_low_1yr:.0f}  –  ${vol_high_1yr:.0f}  "
      f"(${CURRENT_PRICE:.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  2-sigma range (1yr):  ${CURRENT_PRICE - 2*sigma_1yr:.0f}  –  "
      f"${CURRENT_PRICE + 2*sigma_1yr:.0f}")
print(f"  {'─'*60}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} requires:  "
      f"~{sigma_needed_bear:.1f}σ price move  "
      f"{'(unusual — requires fundamental break)' if sigma_needed_bear > 1.5 else '(within normal range)'}")
print(f"  At 55% vol: bear ${SCENARIOS['BEAR'][2]} requires only ~{sigma_needed_bear:.1f}σ — easily reached in a normal correction.")
print(f"  No dividend buffer — total return is entirely price-dependent. Size accordingly.")

# ── ⑥ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print(f"\n  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
print("  " + "─" * (W-2))
print(f"  {'Scenario':<8}  {'Price':>6}  {'Proxy%':>7}  {'Market%':>8}  "
      f"{'Gap':>6}  Description")
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    eps, mult, price, narr = SCENARIOS[k]
    pp  = proxy_probs[k]
    mp  = mkt_probs[k] if mkt_probs else 0
    gap_pp = pp - mp
    print(f"  {k:<8}  ${price:>5}  {pp*100:>6.1f}%  {mp*100:>7.1f}%  "
          f"{gap_pp*100:>+6.1f}pp  {narr}")

print(f"\n  Proxy EV (2yr): ${proxy_ev:.0f}  /  Market EV: ${mkt_ev:.0f}  /  Current: ${CURRENT_PRICE:.0f}")
print(f"  Conservative EV (2yr, ④): ${cons_price_2yr:.0f} + ${cons_div_2yr:.2f} divs = "
      f"${cons_price_2yr + cons_div_2yr:.0f} total value")

print()
print("═" * W)
