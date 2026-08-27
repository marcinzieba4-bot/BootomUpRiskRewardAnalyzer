#!/usr/bin/env python3
"""
ENR Signal Model  v1
──────────────────────
Siemens Energy AG (XETR: ENR)  ·  Grid Technologies, Gas Services & Wind
Trough year: 2023 (Gamesa quality crisis, state guarantee)

New format: segment bridge → signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 152.37   # EUR, Xetra, 2026-08-26
REQUIRED_RETURN  = 0.15
HORIZON_YEARS    = 2

SCENARIOS = {
    "BEAR": (1.2, 18, 85, "Gamesa quality relapse; grid orders normalize; margin guidance missed"),
    "BASE": (3.0, 18, 150, "Grid supercycle executes; wind stays breakeven-plus; margins at guided high end"),
    "BULL": (4.2, 18, 200, "Grid + gas + Middle East compound; Gamesa turns solidly profitable"),
    "XBULL": (5.5, 18, 250, "Full electrification supercycle; ENR re-rates as the grid pure-play"),
}

# ── SEGMENT REVENUE BRIDGE (FY2026E revenue, EUR bn) ────────────────────────────────
SEGMENTS = [
    ("Grid Technologies", "The crown jewel — transformers/switchgear with record multi-year backlog", 15.5, 14.0, 17.0),
    ("Gas Services", "Turbines + service annuity; data-center gas demand is a new leg", 12.0, 11.5, 12.8),
    ("Siemens Gamesa (Wind)", "First positive quarter in 15; offshore delays and cash burn remain", 10.5, 9.5, 11.5),
    ("Transformation of Industry", "Electrolyzers/industrial decarb — option value", 4.5, 4.2, 5.0),
]

# ── SIGNALS ───────────────────────────────────────────────────────────────────
SIGNALS = [
    ("Order backlog momentum", "/4",
      1.0, 2.0, 3.0, 4.0, 4.0, True,
     "Grid equipment orders normalize as capacity catches up"),

    ("Revenue growth", "% YoY",
      3.0, 8.0, 12.0, 16.0, 13.0, True,
     "Backlog conversion slows on project delays"),

    ("Margin trajectory", "/4",
      1.0, 2.0, 3.0, 4.0, 3.0, True,
     "Guidance high-end abandoned on cost overruns"),

    ("Wind (Gamesa) turnaround", "/4",
      1.0, 2.0, 3.0, 4.0, 2.0, True,
     "Quality issues resurface; offshore losses return"),

    ("Middle East / US grid demand", "/4",
      1.0, 2.0, 3.0, 4.0, 4.0, True,
     "Mega-project pipeline pauses"),

    ("Free cash flow conversion", "/4",
      1.0, 2.0, 3.0, 4.0, 2.0, True,
     "Gamesa cash burn offsets grid cash generation"),

]
WEIGHTS = [0.20, 0.15, 0.20, 0.15, 0.15, 0.15]

STRUCTURAL_FACTORS = [
    ("Grid-equipment scarcity — multi-year sold-out supercycle", 1.0, 0.3),
    ("Wind execution risk — Gamesa's quality history", -0.7, 0.25),
    ("+80% off 52-week low; high multiple on recovering earnings", -0.6, 0.2),
    ("Analyst momentum (avg target ~EUR197, Buy consensus)", 0.3, 0.1),
    ("Structural electrification demand across all segments", 0.5, 0.15),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
EPP_TODAY_EPS    = 3.0   # FY2026E approx, EUR
EPP_MIN_PE       = 18.0    # grid-franchise floor — scarcity value of transformer/switchgear capacity

# ── CONSERVATIVE GROWTH (2-yr, base-minus) ───────────────────────────────────
# (signal_index, conservative_value, rationale)
CONS_SIGNALS = [
    (0, 3.0, "Score 3/4 (vs 4; orders normalize)"),
    (1, 9.0, "+9% revenue (vs +13%)"),
    (2, 2.0, "Score 2/4 (vs 3; margin mid-range)"),
    (3, 2.0, "Score 2/4 (flat; wind fragile)"),
    (4, 3.0, "Score 3/4 (vs 4; pipeline slows)"),
    (5, 2.0, "Score 2/4 (flat; cash still tight)"),
]
CONS_EPS_CAGR = 0.15
CONS_EXIT_PE  = 30.0
CONS_DIVIDEND = 0.0

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.42
VOL_BETA       = 1.35
VOL_52W_LOW    = 83.32
VOL_52W_HIGH   = 191.66
VOL_DIVIDEND   = 0.0

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
CUR = "€"

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

market_target_ev = CURRENT_PRICE * ((1 + REQUIRED_RETURN) ** HORIZON_YEARS)
mkt_composite, mkt_probs = market_implied_composite(market_target_ev)
mkt_ev = expected_price(mkt_probs)

epp_updated     = EPP_TODAY_EPS * EPP_MIN_PE
epp_gap_pct     = (CURRENT_PRICE - epp_updated) / epp_updated * 100
bear_vs_epp_pct = (SCENARIOS["BEAR"][2] - epp_updated) / epp_updated * 100

cons_eps_2yr    = EPP_TODAY_EPS * ((1 + CONS_EPS_CAGR) ** 2)
cons_price_2yr  = cons_eps_2yr * CONS_EXIT_PE
cons_div_2yr    = CONS_DIVIDEND * 2.06
cons_total_ret  = (cons_price_2yr - CURRENT_PRICE + cons_div_2yr) / CURRENT_PRICE * 100
cons_annual_ret = cons_total_ret / 2

sigma_1yr         = CURRENT_PRICE * VOL_ANNUAL_PCT
sigma_needed_bear = (CURRENT_PRICE - SCENARIOS["BEAR"][2]) / sigma_1yr

adj_gap = adj_composite - mkt_composite
if   adj_gap >  0.50: _verdict = "UNDERVALUED"
elif adj_gap >  0.20: _verdict = "MODESTLY UNDERVALUED"
elif adj_gap > -0.20: _verdict = "FAIRLY VALUED"
elif adj_gap > -0.50: _verdict = "MODESTLY OVERVALUED"
else:                 _verdict = "OVERVALUED"

# ── OUTPUT ────────────────────────────────────────────────────────────────────
print()
print("═" * W)
print(f"  ENR  ·  Siemens Energy AG  ·  {CUR}{CURRENT_PRICE:,.2f}  ·  Grid Technologies, Gas Services & Wind")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

print(f"\n  SEGMENT REVENUE BRIDGE  (FY2026E revenue, EUR bn  →  BEAR / BULL scenarios)")
print("  " + "─" * (W-2))
print(f"  {'Segment':<24}  {'FY2026E':>10}  {'Bear':>8}  {'Bull':>8}    Δ Bear    Δ Bull")
print("  " + "─" * (W-2))
tot_now = tot_bear = tot_bull = 0.0
for seg_name, seg_desc, s_now, s_bear, s_bull in SEGMENTS:
    tot_now += s_now; tot_bear += s_bear; tot_bull += s_bull
    print(f"  {seg_name:<24}  {CUR}{s_now:>8.1f}  {CUR}{s_bear:>6.1f}  {CUR}{s_bull:>6.1f}    "
          f"{s_bear-s_now:>+6.1f}    {s_bull-s_now:>+6.1f}")
    print(f"    {seg_desc}")
print("  " + "─" * (W-2))
print(f"  {'TOTAL':<24}  {CUR}{tot_now:>8.1f}  {CUR}{tot_bear:>6.1f}  {CUR}{tot_bull:>6.1f}    "
      f"{tot_bear-tot_now:>+6.1f}    {tot_bull-tot_now:>+6.1f}")
print(f"  Q3 FY2026 (Aug 5): profit before special items tripled; expects HIGH END of FY margin guidance")

print(f"\n  ① SIGNAL DASHBOARD")
print(f"  {'Signal':<32}  {'BEAR':>7}  {'BASE≥':>7}  {'BULL≥':>7}  {'XBULL≥':>7}  {'NOW':>8}  Score")
print("  " + "─" * (W-2))
for name_, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u = unit.split()[0] if unit else ""
    bv_s  = f"{bv:+.1f}{u}" if hib else f">{bv:.1f}{u}"
    bar   = "█" * s + "░" * (4 - s)
    print(f"  {name_:<32}  {bv_s:>7}  {f'{bf:.1f}{u}':>7}  {f'{blf:.1f}{u}':>7}  {f'{xf:.1f}{u}':>7}  {f'{cv:+.1f}{u}':>8}  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:    {proxy_composite:.2f} / 4.00")
print(f"  Market composite:   {mkt_composite:.2f} / 4.00  (back-solved from {CUR}{CURRENT_PRICE:,.0f} + {REQUIRED_RETURN*100:.0f}% hurdle)")
print(f"  SCA adjustment:    {sca:+.2f}  →  Adj composite {adj_composite:.2f}  →  Gap {adj_gap:+.2f}  [{_verdict}]")

print(f"\n  Structural factors:")
for desc, score, wt in STRUCTURAL_FACTORS:
    arrow = "  +" if score > 0 else "  -"
    print(f"  {arrow}  {desc}  ({score:+.1f} × {wt*100:.0f}%  =  {score*wt:+.2f})")

print(f"\n  ② BEAR CASE ANATOMY  (what variables need to do for BEAR to materialise)")
print("  " + "─" * (W-2))
print(f"  {'Signal':<32}  {'Current':>8}  {'Bear val':>8}  Move    Trigger")
for name_, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u = unit.split()[0] if unit else ""
    trigger = narr[:40] if len(narr) <= 40 else narr[:37] + "…"
    print(f"  {name_:<32}  {f'{cv:+.1f}{u}':>8}  {f'{bv:+.1f}{u}':>8}  {f'{bv-cv:+.1f}{u}':>6}  {trigger}")

print(f"\n  Bear composite:  {bear_composite:.2f}  →  Bear scenario price: ~{CUR}{expected_price(bear_probs):,.0f}  (model)  /  {CUR}{SCENARIOS['BEAR'][2]:,} (defined)")
print(f"  Bear probability (proxy model):  {proxy_probs['BEAR']*100:.1f}%")
print("""
  KEY TRIGGER: a Gamesa quality relapse (its recurring failure mode) landing
  WHILE grid-order momentum normalizes — the loss-maker reasserting itself just
  as the crown jewel decelerates. JOINT event: today's backlog cushions timing.""")

print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS:          {CUR}{EPP_TODAY_EPS:.2f}  (FY2026E approx, EUR)")
print(f"  Min viable P/E at panic:          {EPP_MIN_PE:.0f}x  [grid-franchise floor — scarcity value of transformer/switchgear capacity]")
print(f"  {'─'*60}")
print(f"  UPDATED EPP:                     {CUR}{epp_updated:,.0f}/share")
print(f"  Current {CUR}{CURRENT_PRICE:,.0f} vs Updated EPP {CUR}{epp_updated:,.0f}:  {epp_gap_pct:+.0f}%  {'✓ cushion' if epp_gap_pct >= 0 else '← in distressed zone'}")
print(f"  Bear {CUR}{SCENARIOS['BEAR'][2]:,} vs Updated EPP {CUR}{epp_updated:,.0f}:  {bear_vs_epp_pct:+.0f}%  {'← BEAR requires earnings impairment' if bear_vs_epp_pct < 0 else '✓ bear is cyclical repricing'}")

print(f"\n  ④ CONSERVATIVE GROWTH  (2-yr, signals at BASE lower bound — no tailwinds)")
print("  " + "─" * (W-2))
print(f"  {'Signal':<32}  {'Conservative':>14}  vs Current  Rationale")
for idx, sval, srat in CONS_SIGNALS:
    sig = SIGNALS[idx]
    print(f"  {sig[0]:<32}  {sval:>14.1f}  {sval-sig[6]:>+9.1f}   {srat[:34]}")

print(f"\n  Conservative 2yr EPS:   {CUR}{EPP_TODAY_EPS:.2f} × (1+{CONS_EPS_CAGR*100:.0f}%)² = {CUR}{cons_eps_2yr:.2f}")
print(f"  At {CONS_EXIT_PE:.0f}x P/E (conservative):  {CUR}{cons_price_2yr:,.0f}/share")
print(f"  + Cumul. dividends (2yr):  +{CUR}{cons_div_2yr:.2f}/share")
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:     {CUR}{cons_price_2yr:,.0f}  ({'▲' if cons_price_2yr > CURRENT_PRICE else '▼'}{abs(cons_price_2yr - CURRENT_PRICE):,.0f} from {CUR}{CURRENT_PRICE:,.0f})")
print(f"  Conservative total return:  {cons_total_ret:+.0f}% over 2yr  = {cons_annual_ret:+.0f}%/yr")
print("""
  Even at 15% EPS CAGR (a recovery-phase rate) and 30x, the 2-yr return is
  negative from here — the supercycle is real, and heavily pre-paid at EUR152.""")

print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        {CUR}{VOL_52W_LOW:,.2f}  –  {CUR}{VOL_52W_HIGH:,.2f}")
print(f"  Annual dividend:      {CUR}{VOL_DIVIDEND:.2f}/share  (yield {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized")
print(f"  Beta vs broad market: {VOL_BETA:.2f}")
print(f"  1-sigma range (1yr):  {CUR}{CURRENT_PRICE - sigma_1yr:,.0f}  –  {CUR}{CURRENT_PRICE + sigma_1yr:,.0f}  ({CUR}{CURRENT_PRICE:,.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  2-sigma range (1yr):  {CUR}{CURRENT_PRICE - 2*sigma_1yr:,.0f}  –  {CUR}{CURRENT_PRICE + 2*sigma_1yr:,.0f}")
print(f"  {'─'*60}")
print(f"  Bear {CUR}{SCENARIOS['BEAR'][2]:,} requires:  ~{sigma_needed_bear:.1f}σ price move  {'(unusual — requires fundamental break)' if sigma_needed_bear > 1.5 else '(within normal vol range)'}")
print("""  Highest-volatility addition (42% realized, beta 1.35): a 52-week range of
  EUR83-192 on a still-recovering earnings base. Position size accordingly. No dividend.""")

print(f"\n  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
print("  " + "─" * (W-2))
print(f"  {'Scenario':<8}  {'Price':>8}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>6}  Description")
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    sc = SCENARIOS[k]
    pp, mp = proxy_probs[k], mkt_probs[k]
    print(f"  {k:<8}  {CUR}{sc[2]:>7,}  {pp*100:>6.1f}%  {mp*100:>7.1f}%  {(pp-mp)*100:>+6.1f}pp  {sc[3]}")

print(f"\n  Proxy EV (2yr): {CUR}{proxy_ev:,.0f}  /  Market EV: {CUR}{mkt_ev:,.0f}  /  Current: {CUR}{CURRENT_PRICE:,.0f}")
print(f"  Conservative EV (2yr, ④): {CUR}{cons_price_2yr:,.0f} + {CUR}{cons_div_2yr:.2f} divs = {CUR}{cons_price_2yr + cons_div_2yr:,.0f} total value")

print()
print("═" * W)
