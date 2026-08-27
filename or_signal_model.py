#!/usr/bin/env python3
"""
L'Oréal Signal Model  v1
──────────────────────
L'Oréal S.A. (Euronext Paris: OR)  ·  Beauty & Cosmetics
Trough year: 2025 (beauty-market growth deceleration, travel-retail China weakness)

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 387.20   # EUR, Euronext Paris, 2026-08-26
REQUIRED_RETURN  = 0.15
HORIZON_YEARS    = 2

SCENARIOS = {
    "BEAR":  (330,  20,  260, "Beauty market growth stalls; L'Oréal loses share to niche/indie brands"),
    "BASE":  (400,  25,  360, "L'Oréal keeps outpacing the beauty market; margins hold near record"),
    "BULL":  (470,  29,  460, "Travel-retail China fully recovers; dermatological beauty accelerates further"),
    "XBULL": (540,  33,  560, "Beauty super-cycle + North Asia travel-retail rebound + margin expansion"),
}

# ── SEGMENT REVENUE BRIDGE (FY2026E, EUR bn) ────────────────────────────────
SEG_CONS_NOW,  SEG_CONS_BEAR,  SEG_CONS_BULL  = 17.5, 16.5, 18.5
SEG_LUXE_NOW,  SEG_LUXE_BEAR,  SEG_LUXE_BULL  = 14.0, 13.0, 15.5
SEG_PROF_NOW,  SEG_PROF_BEAR,  SEG_PROF_BULL  =  5.5,  5.0,  6.0
SEG_DERMA_NOW, SEG_DERMA_BEAR, SEG_DERMA_BULL =  6.3,  5.8,  7.0

# ── SIGNALS ───────────────────────────────────────────────────────────────────
SIGNALS = [
    ("Like-for-like sales growth",     "% YoY",
      1.0,   4.0,   7.0,  10.0,   6.5, True,
     "Beauty market growth decelerates sharply; L'Oréal growth converges to market rate"),

    ("Outperformance vs beauty market","pp",
      -1.0,   0.5,   1.5,   3.0,   1.4, True,
     "L'Oréal loses share to independent/niche beauty brands and private label"),

    ("Operating margin",               "%",
      17.0,  19.5,  21.0,  22.5,  21.3, True,
     "Input-cost inflation and marketing spend compress margin from record H1 level"),

    ("China (travel retail) growth",   "% YoY",
      -8.0,   0.0,   6.0,  12.0,   4.0, True,
     "Chinese travel-retail channel stays depressed; duty-free demand doesn't recover"),

    ("Dermatological Beauty growth",   "% YoY",
      3.0,   7.0,  11.0,  16.0,  10.6, True,
     "Skincare/derma category growth normalizes off an unusually strong base"),

    ("Professional Products growth",   "% YoY",
      2.0,   6.0,  10.0,  14.0,  11.6, True,
     "Salon channel softens as consumer discretionary spend tightens"),
]
WEIGHTS = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("Consistent multi-decade market-share gainer vs beauty category", 0.8, 0.25),
    ("Record H1 2026 operating margin (21.3%) — execution strength",    0.6, 0.20),
    ("China travel-retail structural overhang (duty-free demand)",     -0.5, 0.20),
    ("Diversified across mass/luxury/derma/professional divisions",     0.4, 0.20),
    ("Premium valuation vs staples peers limits re-rating upside",     -0.3, 0.15),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
EPP_TODAY_EPS    = 11.78   # TTM EPS, EUR
EPP_MIN_PE       = 24.0    # min viable P/E at panic — quality-compounder floor
EPP_HISTORICAL   = 320.0   # historical EPP v1 (approx)

# ── CONSERVATIVE GROWTH (2-yr, base-minus) ───────────────────────────────────
CONS_SIGNALS = [
    ("Like-for-like",   4.0, "+4% YoY (vs +6.5%; market growth decelerates)"),
    ("Outperformance",  0.5, "+0.5pp (vs +1.4pp; share gains narrow)"),
    ("Operating",      20.0, "20% margin (vs 21.3%; modest deleverage on cost inflation)"),
    ("China",           0.0, "flat YoY (vs +4%; travel-retail stays soft)"),
    ("Dermatological",  7.0, "+7% YoY (vs +10.6%; normalizes off strong base)"),
    ("Professional",    6.0, "+6% YoY (vs +11.6%; salon channel softens)"),
]
CONS_EPS_CAGR = 0.06     # 6%/yr conservative (vs recent double-digit)
CONS_EXIT_PE  = 28.0     # 28x exit (below current ~33x, still premium for quality)
CONS_DIVIDEND = 7.20     # approx EUR7.20/yr cumulative annual dividend

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.19
VOL_BETA       = 0.80
VOL_52W_LOW    = 338.85
VOL_52W_HIGH   = 408.35
VOL_DIVIDEND   = 7.20

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

def market_implied_composite(target_ev):
    best_c, best_probs, best_diff = None, None, None
    for c in [x / 100 for x in range(100, 401)]:
        probs = softmax_probs(c)
        diff = abs(expected_price(probs) - target_ev)
        if best_diff is None or diff < best_diff:
            best_c, best_probs, best_diff = c, probs, diff
    return best_c, best_probs

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

epp_updated     = EPP_TODAY_EPS * EPP_MIN_PE
epp_gap_pct     = (CURRENT_PRICE - epp_updated) / epp_updated * 100
bear_vs_epp_pct = (SCENARIOS["BEAR"][2] - epp_updated) / epp_updated * 100

cons_eps_2yr    = EPP_TODAY_EPS * ((1 + CONS_EPS_CAGR) ** 2)
cons_price_2yr  = cons_eps_2yr * CONS_EXIT_PE
cons_div_2yr    = CONS_DIVIDEND * (1 + 0.05) + CONS_DIVIDEND * (1 + 0.05) ** 2
cons_total_ret  = (cons_price_2yr - CURRENT_PRICE + cons_div_2yr) / CURRENT_PRICE * 100
cons_annual_ret = cons_total_ret / 2

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

# ── OUTPUT ────────────────────────────────────────────────────────────────────
print()
print("═" * W)
print(f"  OR  ·  L'Oréal S.A.  ·  €{CURRENT_PRICE:.2f}  ·  Beauty & Cosmetics")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

print(f"\n  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
print("  " + "─" * (W-2))
print(f"  {'Segment':<24}  {'FY2026E (€B)':>13}  {'Bear (€B)':>10}  {'Bull (€B)':>10}    Δ Bear    Δ Bull")
print("  " + "─" * (W-2))
seg_total_now  = SEG_CONS_NOW + SEG_LUXE_NOW + SEG_PROF_NOW + SEG_DERMA_NOW
seg_total_bear = SEG_CONS_BEAR + SEG_LUXE_BEAR + SEG_PROF_BEAR + SEG_DERMA_BEAR
seg_total_bull = SEG_CONS_BULL + SEG_LUXE_BULL + SEG_PROF_BULL + SEG_DERMA_BULL
print(f"  Consumer Products        € {SEG_CONS_NOW:>9.1f}  €  {SEG_CONS_BEAR:>7.1f}  €  {SEG_CONS_BULL:>7.1f}    "
      f"{SEG_CONS_BEAR-SEG_CONS_NOW:>+6.1f}    {SEG_CONS_BULL-SEG_CONS_NOW:>+6.1f}")
print(f"    Mass-market brands (L'Oréal Paris, Garnier, Maybelline) — largest, most economically sensitive")
print(f"  L'Oréal Luxe             € {SEG_LUXE_NOW:>9.1f}  €  {SEG_LUXE_BEAR:>7.1f}  €  {SEG_LUXE_BULL:>7.1f}    "
      f"{SEG_LUXE_BEAR-SEG_LUXE_NOW:>+6.1f}    {SEG_LUXE_BULL-SEG_LUXE_NOW:>+6.1f}")
print(f"    Prestige brands (YSL, Lancôme, Armani) — most exposed to China travel-retail weakness")
print(f"  Professional Products    € {SEG_PROF_NOW:>9.1f}  €  {SEG_PROF_BEAR:>7.1f}  €  {SEG_PROF_BULL:>7.1f}    "
      f"{SEG_PROF_BEAR-SEG_PROF_NOW:>+6.1f}    {SEG_PROF_BULL-SEG_PROF_NOW:>+6.1f}")
print(f"    Salon channel — grew +11.6% last quarter, fastest-growing division")
print(f"  Dermatological Beauty    € {SEG_DERMA_NOW:>9.1f}  €  {SEG_DERMA_BEAR:>7.1f}  €  {SEG_DERMA_BULL:>7.1f}    "
      f"{SEG_DERMA_BEAR-SEG_DERMA_NOW:>+6.1f}    {SEG_DERMA_BULL-SEG_DERMA_NOW:>+6.1f}")
print(f"    La Roche-Posay/CeraVe — grew +10.6% last quarter, strongest structural growth driver")
print("  " + "─" * (W-2))
print(f"  TOTAL                    € {seg_total_now:>9.1f}  €  {seg_total_bear:>7.1f}  €  {seg_total_bull:>7.1f}    "
      f"{seg_total_bear-seg_total_now:>+6.1f}    {seg_total_bull-seg_total_now:>+6.1f}")
print(f"  H1 2026 actual: €23.77bn sales, +6.8% LFL, record 21.3% operating margin")

print(f"\n  ① SIGNAL DASHBOARD")
print(f"  {'Signal':<32}  {'BEAR':>7}  {'BASE≥':>7}  {'BULL≥':>7}  {'XBULL≥':>7}  {'NOW':>8}  Score")
print("  " + "─" * (W-2))
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u = unit.split()[0] if unit else ""
    bv_s  = f"{bv:+.1f}{u}" if hib else f">{bv:.1f}{u}"
    bf_s  = f"{bf:.1f}{u}"
    blf_s = f"{blf:.1f}{u}"
    xf_s  = f"{xf:.1f}{u}"
    cv_s  = f"{cv:+.1f}{u}"
    bar   = "█" * s + "░" * (4 - s)
    print(f"  {name:<32}  {bv_s:>7}  {bf_s:>7}  {blf_s:>7}  {xf_s:>7}  {cv_s:>8}  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:    {proxy_composite:.2f} / 4.00")
if mkt_composite:
    print(f"  Market composite:   {mkt_composite:.2f} / 4.00  (back-solved from €{CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% hurdle)")
    print(f"  SCA adjustment:    {sca:+.2f}  →  Adj composite {adj_composite:.2f}  →  Gap {adj_gap:+.2f}  [{_verdict}]")

print(f"\n  Structural factors:")
for desc, score, wt in STRUCTURAL_FACTORS:
    arrow = "  +" if score > 0 else "  -"
    print(f"  {arrow}  {desc}  ({score:+.1f} × {wt*100:.0f}%  =  {score*wt:+.2f})")

print(f"\n  ② BEAR CASE ANATOMY  (what variables need to do for BEAR to materialise)")
print("  " + "─" * (W-2))
print(f"  {'Signal':<32}  {'Current':>8}  {'Bear val':>8}  Move    Trigger")
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u      = unit.split()[0] if unit else ""
    cv_s   = f"{cv:+.1f}{u}"
    bv_s   = f"{bv:+.1f}{u}"
    move   = bv - cv
    move_s = f"{move:+.1f}{u}"
    trigger = narr[:40] if len(narr) <= 40 else narr[:37] + "…"
    print(f"  {name:<32}  {cv_s:>8}  {bv_s:>8}  {move_s:>6}  {trigger}")

print(f"\n  Bear composite:  {bear_composite:.2f}  →  Bear scenario price: ~€{expected_price(bear_probs):.0f}  (model)  /  €{SCENARIOS['BEAR'][2]} (defined)")
print(f"  Bear probability (proxy model):  {proxy_probs['BEAR']*100:.1f}%")
print(f"\n  KEY TRIGGER: Beauty market growth decelerates below 3% globally AND L'Oréal's")
print(f"  multi-decade outperformance streak breaks → market re-rates it as a staples")
print(f"  compounder, not a growth compounder. JOINT event: derma strength cushions one.")

print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS:          €{EPP_TODAY_EPS:.2f}  (TTM reported, EUR)")
print(f"  Min viable P/E at panic:          {EPP_MIN_PE:.0f}x  [quality-compounder floor — 30+yr track record of share gains]")
print(f"  {'─'*60}")
print(f"  UPDATED EPP:                     €{epp_updated:.0f}/share")
print(f"  Historical EPP (v1, floor adj):  €{EPP_HISTORICAL:.0f}/share")
print(f"  Current €{CURRENT_PRICE:.0f} vs Updated EPP €{epp_updated:.0f}:  {epp_gap_pct:+.0f}%  {'✓ cushion' if epp_gap_pct >= 0 else '← in distressed zone'}")
print(f"  Bear €{SCENARIOS['BEAR'][2]} vs Updated EPP €{epp_updated:.0f}:  {bear_vs_epp_pct:+.0f}%  {'← BEAR requires earnings impairment' if bear_vs_epp_pct < 0 else '✓ bear is cyclical repricing'}")

print(f"\n  ④ CONSERVATIVE GROWTH  (2-yr, signals at BASE lower bound — no tailwinds)")
print("  " + "─" * (W-2))
print(f"  {'Signal':<32}  {'Conservative':>14}  vs Current  Rationale")
for sname, sval, srat in CONS_SIGNALS:
    cur = next(cv for name, _, __, ___, ____, _____, cv, ______, _______ in SIGNALS
               if name.lower().startswith(sname.split()[0].lower()))
    diff = sval - cur
    print(f"  {sname:<32}  {sval:>14.1f}  {diff:>+9.1f}   {srat[:30]}")

print(f"\n  Conservative 2yr EPS:   €{EPP_TODAY_EPS:.2f} × (1+{CONS_EPS_CAGR*100:.0f}%)² = €{cons_eps_2yr:.2f}")
print(f"  At {CONS_EXIT_PE:.0f}x P/E (conservative):  €{cons_price_2yr:.0f}/share")
if CONS_DIVIDEND > 0:
    print(f"  + Cumul. dividends (2yr):  +€{cons_div_2yr:.2f}/share")
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:     €{cons_price_2yr:.0f}  ({'▲' if cons_price_2yr > CURRENT_PRICE else '▼'}{abs(cons_price_2yr - CURRENT_PRICE):.0f} from €{CURRENT_PRICE:.0f})")
print(f"  Conservative total return:  {cons_total_ret:+.0f}% over 2yr  = {cons_annual_ret:+.0f}%/yr")
print(f"\n  Even at conservative 6% EPS growth and a de-rated 28x exit, L'Oréal's record")
print(f"  H1 2026 margins and consistent share gains provide unusual downside protection.")

print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        €{VOL_52W_LOW:.0f}  –  €{VOL_52W_HIGH:.0f}")
if VOL_DIVIDEND > 0:
    print(f"  Annual dividend:      €{VOL_DIVIDEND:.2f}/share  (yield {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized  (low — defensive quality compounder)")
print(f"  Beta vs broad market: {VOL_BETA:.2f}")
print(f"  1-sigma range (1yr):  €{vol_low_1yr:.0f}  –  €{vol_high_1yr:.0f}  (€{CURRENT_PRICE:.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  2-sigma range (1yr):  €{CURRENT_PRICE - 2*sigma_1yr:.0f}  –  €{CURRENT_PRICE + 2*sigma_1yr:.0f}")
print(f"  {'─'*60}")
print(f"  Bear €{SCENARIOS['BEAR'][2]} requires:  ~{sigma_needed_bear:.1f}σ price move  {'(unusual — requires fundamental break)' if sigma_needed_bear > 1.5 else '(within normal vol range)'}")
print(f"  L'Oréal's tight 52-week range (€339–€408, ~20% spread) reflects its defensive,")
print(f"  low-beta profile relative to more cyclical luxury peers like LVMH.")

print(f"\n  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
print("  " + "─" * (W-2))
print(f"  {'Scenario':<8}  {'Price':>6}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>6}  Description")
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    sc = SCENARIOS[k]
    price = sc[2]
    narr  = sc[3] if len(sc) > 3 else ""
    pp  = proxy_probs[k]
    mp  = mkt_probs[k] if mkt_probs else 0
    gap_pp = pp - mp
    print(f"  {k:<8}  €{price:>5}  {pp*100:>6.1f}%  {mp*100:>7.1f}%  {gap_pp*100:>+6.1f}pp  {narr}")

print(f"\n  Proxy EV (2yr): €{proxy_ev:.0f}  /  Market EV: €{mkt_ev:.0f}  /  Current: €{CURRENT_PRICE:.0f}")
print(f"  Conservative EV (2yr, ④): €{cons_price_2yr:.0f} + €{cons_div_2yr:.2f} divs = €{cons_price_2yr + cons_div_2yr:.0f} total value")

print()
print("═" * W)
