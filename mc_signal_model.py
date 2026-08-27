#!/usr/bin/env python3
"""
LVMH Signal Model  v1
──────────────────────
LVMH Moët Hennessy Louis Vuitton SE (Euronext Paris: MC)  ·  Luxury Goods Conglomerate
Trough year: 2026 (China/global luxury demand slowdown; Fashion & Leather Goods weakness)

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 467.70   # EUR, Euronext Paris, 2026-08-26
REQUIRED_RETURN  = 0.15
HORIZON_YEARS    = 2

SCENARIOS = {
    "BEAR":  (350,  16,  310, "F&LG organic sales stay negative through 2027; China demand keeps deteriorating"),
    "BASE":  (440,  20,  420, "F&LG stabilizes near flat; Asia growth holds at low-single-digit"),
    "BULL":  (560,  25,  560, "Luxury demand inflects positive; China travel-retail recovery broadens"),
    "XBULL": (680,  29,  700, "Full luxury-cycle recovery + Chinese consumer stimulus + US wealth effect"),
}

# ── SIGNALS ───────────────────────────────────────────────────────────────────
SIGNALS = [
    ("Fashion & Leather Goods organic", "% YoY",
      -15.0,  -5.0,   3.0,  10.0,  -9.0, True,
     "Core division (Louis Vuitton, Dior) organic sales keep declining double-digit"),

    ("Group organic sales growth",     "% YoY",
      -8.0,  -2.0,   4.0,  10.0,  -1.0, True,
     "Group-wide organic growth stays negative through FY2026 and into 2027"),

    ("Asia (ex-Japan) sales growth",   "% YoY",
      -5.0,   2.0,   8.0,  15.0,   4.0, True,
     "China luxury demand slowdown deepens; travel-retail recovery stalls"),

    ("Recurring operating margin",     "%",
      16.0,  20.0,  23.0,  26.0,  20.5, True,
     "Fixed-cost deleverage on falling sales compresses margins further"),

    ("Wines & Spirits organic",        "% YoY",
      -10.0,  -3.0,   3.0,   8.0,  -4.0, True,
     "Cognac destocking in China/US continues; channel inventory stays elevated"),

    ("Watches & Jewelry organic",      "% YoY",
      -5.0,   0.0,   6.0,  12.0,   2.0, True,
     "Tiffany/Bulgari underperform as high-jewelry demand softens with wealth effect"),
]
WEIGHTS = [0.30, 0.20, 0.15, 0.15, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("Irreplaceable brand portfolio (LV, Dior, Tiffany, Moët)",   1.0, 0.30),
    ("China/Asia luxury demand cyclical downturn",               -1.0, 0.30),
    ("Pricing power intact — no discounting despite volume drop", 0.5, 0.15),
    ("Wines & Spirits channel destocking overhang",              -0.4, 0.15),
    ("Diversified across 6 divisions, 75+ maisons",                0.3, 0.10),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
EPP_TODAY_EPS    = 21.86   # TTM EPS, EUR
EPP_MIN_PE       = 16.0    # min viable P/E at panic — luxury brand-moat floor
EPP_HISTORICAL   = 480.0   # historical EPP v1 (approx, pre-downturn)

# ── CONSERVATIVE GROWTH (2-yr, base-minus) ───────────────────────────────────
CONS_SIGNALS = [
    ("Fashion", -6.0, "-6% organic (vs -9%; decline moderates but stays negative)"),
    ("Group",   -2.0, "-2% organic (vs -1%; group stays pressured near-term)"),
    ("Asia",     1.0, "+1% YoY (vs +4%; China recovery stays sluggish)"),
    ("Recurring", 19.0, "19% margin (vs 20.5%; further deleverage on soft sales)"),
    ("Wines",   -6.0, "-6% organic (vs -4%; destocking persists into 2027)"),
    ("Watches",  0.0, "flat YoY (vs +2%; high-jewelry demand stays muted)"),
]
CONS_EPS_CAGR = 0.03     # 3%/yr conservative (vs historical double-digit)
CONS_EXIT_PE  = 19.0     # 19x exit (below historical ~24-26x, reflects derated growth)
CONS_DIVIDEND = 13.00    # approx EUR13/yr cumulative annual dividend

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.28
VOL_BETA       = 1.10
VOL_52W_LOW    = 436.55
VOL_52W_HIGH   = 682.90
VOL_DIVIDEND   = 13.00

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
cons_div_2yr    = CONS_DIVIDEND * (1 + 0.02) + CONS_DIVIDEND * (1 + 0.02) ** 2
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
print(f"  MC  ·  LVMH Moët Hennessy Louis Vuitton SE  ·  €{CURRENT_PRICE:.2f}  ·  Luxury Goods")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

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
print(f"\n  KEY TRIGGER: Fashion & Leather Goods organic sales stay negative for 4+ more")
print(f"  quarters AND China consumer confidence fails to recover → structural (not")
print(f"  cyclical) demand impairment. JOINT event: brand pricing power alone cushions one.")

print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS:          €{EPP_TODAY_EPS:.2f}  (TTM reported, EUR)")
print(f"  Min viable P/E at panic:          {EPP_MIN_PE:.0f}x  [luxury brand-moat floor — irreplaceable maisons, pricing power]")
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
print(f"\n  Even assuming the downturn barely improves (3%/yr EPS growth, 19x exit), the")
print(f"  brand portfolio's pricing power provides a floor most consumer peers lack.")

print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        €{VOL_52W_LOW:.0f}  –  €{VOL_52W_HIGH:.0f}")
if VOL_DIVIDEND > 0:
    print(f"  Annual dividend:      €{VOL_DIVIDEND:.2f}/share  (yield {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized")
print(f"  Beta vs broad market: {VOL_BETA:.2f}")
print(f"  1-sigma range (1yr):  €{vol_low_1yr:.0f}  –  €{vol_high_1yr:.0f}  (€{CURRENT_PRICE:.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  2-sigma range (1yr):  €{CURRENT_PRICE - 2*sigma_1yr:.0f}  –  €{CURRENT_PRICE + 2*sigma_1yr:.0f}")
print(f"  {'─'*60}")
print(f"  Bear €{SCENARIOS['BEAR'][2]} requires:  ~{sigma_needed_bear:.1f}σ price move  {'(unusual — requires fundamental break)' if sigma_needed_bear > 1.5 else '(within normal vol range)'}")
print(f"  Stock is already down ~30% YTD (2026) and trading near 52-week lows —")
print(f"  much of the demand-slowdown bear case may already be reflected in price.")

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
