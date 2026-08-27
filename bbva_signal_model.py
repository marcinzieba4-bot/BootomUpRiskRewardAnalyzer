#!/usr/bin/env python3
"""
BBVA Signal Model  v1
──────────────────────
Banco Bilbao Vizcaya Argentaria, S.A. (BME: BBVA)  ·  Retail & Commercial Banking (Spain, Mexico)
Trough year: 2020 (COVID provisions + peso shock)

New format: segment bridge → signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 24.8   # EUR, BME Madrid, 2026-08-13
REQUIRED_RETURN  = 0.15
HORIZON_YEARS    = 2

SCENARIOS = {
    "BEAR": (1.2, 13, 16, "Peso devaluation + Mexican credit cycle turn; Spain NII compresses on cuts"),
    "BASE": (1.95, 12, 24, "Mexico compounds, Spain resilient; ~19% ROTE sustained"),
    "BULL": (2.3, 13, 30, "EM re-rating + capital returns accelerate post-Sabadell walk-away"),
    "XBULL": (2.7, 13, 36, "Mexico supercycle + European bank re-rating toward book value premium"),
}

# ── SEGMENT REVENUE BRIDGE (FY2026E attributable profit, EUR bn) ────────────────────────────────
SEGMENTS = [
    ("Mexico", "~half of group profit — the engine and the concentration risk in one", 5.4, 4.6, 5.8),
    ("Spain", "NII-driven domestic franchise; resilient through the rate cycle", 3.6, 3.3, 3.8),
    ("South America", "Colombia/Peru/Argentina — high growth, high volatility", 1.1, 0.9, 1.4),
    ("Turkey (Garanti)", "Structurally profitable but lira-translation hostage", 0.9, 0.6, 1.2),
]

# ── SIGNALS ───────────────────────────────────────────────────────────────────
SIGNALS = [
    ("EPS growth trend", "% YoY",
      -5.0, 5.0, 12.0, 20.0, 15.0, True,
     "Peso shock + provisions reverse the EPS trajectory"),

    ("Mexico profit momentum", "/4",
      1.0, 2.0, 3.0, 4.0, 3.0, True,
     "Mexican credit cycle turns; loan growth stalls"),

    ("Spain NII resilience", "/4",
      1.0, 2.0, 3.0, 4.0, 3.0, True,
     "ECB cuts compress NII faster than volume offsets"),

    ("CET1 ratio", "%",
      11.5, 12.2, 12.8, 13.4, 13.0, True,
     "Capital erodes on FX translation + growth RWAs"),

    ("Cost/income ratio", "%",
      45.0, 42.0, 39.0, 36.0, 38.5, False,
     "Inflation outpaces revenue; efficiency reverses"),

    ("Post-Sabadell strategic clarity", "/4",
      1.0, 2.0, 3.0, 4.0, 3.0, True,
     "Failed bid pushes management toward riskier M&A"),

]
WEIGHTS = [0.20, 0.20, 0.15, 0.15, 0.15, 0.15]

STRUCTURAL_FACTORS = [
    ("Best-in-class ~19-20% ROTE among European banks", 0.8, 0.25),
    ("Mexico concentration — peso/credit-cycle single-factor risk", -0.5, 0.2),
    ("Stock at 52-week high after a +60% run from the low", -0.6, 0.25),
    ("Sabadell walk-away removes dilution overhang, frees buybacks", 0.3, 0.15),
    ("EM funding and translation volatility", -0.2, 0.15),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
EPP_TODAY_EPS    = 1.89   # TTM reported, EUR
EPP_MIN_PE       = 6.0    # EM-bank trough floor — franchise survives peso cycles

# ── CONSERVATIVE GROWTH (2-yr, base-minus) ───────────────────────────────────
# (signal_index, conservative_value, rationale)
CONS_SIGNALS = [
    (0, 6.0, "+6% EPS (vs +15%; normalization)"),
    (1, 2.0, "Score 2/4 (vs 3; Mexico cools)"),
    (2, 2.0, "Score 2/4 (vs 3; NII pressure)"),
    (3, 12.5, "12.5% CET1 (vs 13.0)"),
    (4, 40.0, "40% C/I (vs 38.5; cost creep)"),
    (5, 2.0, "Score 2/4 (vs 3)"),
]
CONS_EPS_CAGR = 0.04
CONS_EXIT_PE  = 8.0
CONS_DIVIDEND = 1.08

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.28
VOL_BETA       = 1.15
VOL_52W_LOW    = 15.28
VOL_52W_HIGH   = 25.04
VOL_DIVIDEND   = 1.08

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
print(f"  BBVA  ·  Banco Bilbao Vizcaya Argentaria, S.A.  ·  {CUR}{CURRENT_PRICE:,.2f}  ·  Retail & Commercial Banking (Spain, Mexico)")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

print(f"\n  SEGMENT REVENUE BRIDGE  (FY2026E attributable profit, EUR bn  →  BEAR / BULL scenarios)")
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
print(f"  Q2 2026: EPS beat ($0.61 vs $0.59 cons); Sabadell takeover effectively failed (~1-3% acceptance)")

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
  KEY TRIGGER: a Mexican credit-cycle turn (rising NPLs) arriving WITH a peso
  devaluation — earnings hit and translation hit compounding. JOINT event:
  Spain's rate-cycle resilience cushions a single-region shock, not both.""")

print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS:          {CUR}{EPP_TODAY_EPS:.2f}  (TTM reported, EUR)")
print(f"  Min viable P/E at panic:          {EPP_MIN_PE:.0f}x  [EM-bank trough floor — franchise survives peso cycles]")
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
  At 4% EPS CAGR and an 8x exit, the 2-yr return is meaningfully negative from
  a 52-week high — the franchise is excellent; the entry price is the problem.""")

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
print("""  Up ~60% from the 52-week low (EUR15.28) to essentially the high (EUR25.04);
  EM-bank rallies of this magnitude historically give back a third or more.""")

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
