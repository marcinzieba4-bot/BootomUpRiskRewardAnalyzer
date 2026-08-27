#!/usr/bin/env python3
"""
ASML Signal Model  v1
──────────────────────
ASML Holding N.V. (AEX/Euronext Amsterdam: ASML)  ·  Semiconductor Lithography Equipment
Trough year: 2026 (China export-control shock; DUV/EUV mix shift)

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 1487.20   # EUR, Euronext Amsterdam, 2026-08-26
REQUIRED_RETURN  = 0.15
HORIZON_YEARS    = 2

SCENARIOS = {
    "BEAR":  ( 620,  25,  700, "MATCH Act passes; China DUV sales collapse further; AI capex pause"),
    "BASE":  ( 900,  32, 1350, "China stabilizes ~20% of sales; EUV/High-NA ramp on schedule"),
    "BULL":  (1500,  40, 1950, "AI-driven leading-edge capex accelerates; High-NA orders surge"),
    "XBULL": (1900,  48, 2450, "Foundry capex supercycle + China restrictions ease + High-NA beats"),
}

# ── SIGNALS ───────────────────────────────────────────────────────────────────
SIGNALS = [
    ("China % of system sales",        "%",
      45.0,  30.0,  20.0,  15.0,  19.0, False,
     "China share re-accelerates as customers stockpile ahead of tighter export rules"),

    ("EUV bookings growth YoY",        "% YoY",
      -20.0,  0.0,  15.0,  30.0,  12.0, True,
     "Leading-edge foundry/logic capex freezes; EUV order intake stalls"),

    ("Gross margin",                   "%",
      48.0,  52.0,  55.0,  58.0,  55.5, True,
     "Mix shifts back to lower-margin DUV; pricing pressure from single large customer"),

    ("2026 revenue guidance (mid)",    "EUR bn",
      36.0,  40.0,  44.0,  48.0,  44.0, True,
     "Guidance cut as China restrictions bite faster than modeled"),

    ("High-NA EUV tool shipments",     "units/yr",
      2.0,   4.0,   8.0,  14.0,   6.0, True,
     "High-NA adoption delayed; customers stay on low-NA for longer than expected"),

    ("US-China export policy risk",    "/4 scale (inv)",
      1.0,   2.0,   3.0,   4.0,   2.5, True,
     "MATCH Act or equivalent legislation tightens DUV/service export rules further"),
]
WEIGHTS = [0.20, 0.25, 0.15, 0.20, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("Monopoly on EUV lithography — no credible competitor",   1.2, 0.30),
    ("China export-control overhang (US/Dutch policy risk)",  -1.0, 0.25),
    ("Record €132bn+ industry-wide capex commitments to 2027", 0.6, 0.20),
    ("High-NA transition execution risk",                     -0.4, 0.15),
    ("EUR-denominated earnings vs USD-reporting AI-capex peers", -0.2, 0.10),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
EPP_TODAY_EPS    = 24.73   # FY2025 reported EPS, EUR
EPP_MIN_PE       = 25.0    # min viable P/E at panic — monopoly moat + structural AI demand floor
EPP_HISTORICAL   = 500.0   # historical EPP v1 (approx, pre-2026 China shock)

# ── CONSERVATIVE GROWTH (2-yr, base-minus) ───────────────────────────────────
CONS_SIGNALS = [
    ("China % of sales",        25.0, "25% (vs 19%; some restocking, still below historical 35-45%)"),
    ("EUV bookings growth",      5.0, "+5% YoY (vs +12%; capex digestion continues)"),
    ("Gross margin",            53.0, "53% (vs 55.5%; mix stays DUV-heavy)"),
    ("2026 revenue guidance",   41.0, "EUR41bn (vs 44bn; low end of guided range)"),
    ("High-NA shipments",        4.0, "4 units/yr (vs 6; adoption slower than plan)"),
    ("US-China export risk",     2.0, "Score 2/4 (vs 2.5; status quo, no new legislation)"),
]
CONS_EPS_CAGR = 0.12     # 12%/yr conservative (vs consensus mid-20s%)
CONS_EXIT_PE  = 32.0     # 32x exit (de-rate from current elevated multiple)
CONS_DIVIDEND = 7.50     # approx EUR7.50 cumulative annual dividend (current ~EUR7.5-8/yr run-rate)

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.38    # elevated 2yr realized vol (China-news-driven whipsaws)
VOL_BETA       = 1.35    # beta vs broad market
VOL_52W_LOW    = 611.80
VOL_52W_HIGH   = 1741.00
VOL_DIVIDEND   = 7.50

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
print(f"  ASML  ·  ASML Holding N.V.  ·  €{CURRENT_PRICE:.2f}  ·  Semiconductor Lithography (EUV monopoly)")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

print(f"\n  ① SIGNAL DASHBOARD")
print(f"  {'Signal':<32}  {'BEAR':>7}  {'BASE≥':>7}  {'BULL≥':>7}  {'XBULL≥':>7}  {'NOW':>8}  Score")
print("  " + "─" * (W-2))
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u = unit.split()[0] if unit else ""
    bv_s  = f"{bv:+.0f}{u}" if hib else f">{bv:.1f}{u}"
    bf_s  = f"{bf:.0f}{u}"
    blf_s = f"{blf:.0f}{u}"
    xf_s  = f"{xf:.0f}{u}"
    cv_s  = f"{cv:+.0f}{u}"
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
    cv_s   = f"{cv:+.0f}{u}"
    bv_s   = f"{bv:+.0f}{u}"
    move   = bv - cv
    move_s = f"{move:+.0f}{u}"
    trigger = narr[:40] if len(narr) <= 40 else narr[:37] + "…"
    print(f"  {name:<32}  {cv_s:>8}  {bv_s:>8}  {move_s:>6}  {trigger}")

print(f"\n  Bear composite:  {bear_composite:.2f}  →  Bear scenario price: ~€{expected_price(bear_probs):.0f}  (model)  /  €{SCENARIOS['BEAR'][2]} (defined)")
print(f"  Bear probability (proxy model):  {proxy_probs['BEAR']*100:.1f}%")
print(f"\n  KEY TRIGGER: MATCH Act (or equivalent) passes, extending export curbs to DUV")
print(f"  service/spares for China → China share falls below 10% and AI-capex customers")
print(f"  pause orders simultaneously. JOINT event: EUV monopoly alone doesn't bear this.")

print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS:          €{EPP_TODAY_EPS:.2f}  (FY2025 reported, EUR)")
print(f"  Min viable P/E at panic:          {EPP_MIN_PE:.0f}x  [EUV monopoly floor; no credible competitor exists]")
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
    print(f"  {sname:<32}  {sval:>14.1f}  {diff:>+9.0f}   {srat[:30]}")

print(f"\n  Conservative 2yr EPS:   €{EPP_TODAY_EPS:.2f} × (1+{CONS_EPS_CAGR*100:.0f}%)² = €{cons_eps_2yr:.2f}")
print(f"  At {CONS_EXIT_PE:.0f}x P/E (conservative):  €{cons_price_2yr:.0f}/share")
if CONS_DIVIDEND > 0:
    print(f"  + Cumul. dividends (2yr):  +€{cons_div_2yr:.2f}/share")
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:     €{cons_price_2yr:.0f}  ({'▲' if cons_price_2yr > CURRENT_PRICE else '▼'}{abs(cons_price_2yr - CURRENT_PRICE):.0f} from €{CURRENT_PRICE:.0f})")
print(f"  Conservative total return:  {cons_total_ret:+.0f}% over 2yr  = {cons_annual_ret:+.0f}%/yr")
print(f"\n  Even at conservative 12% EPS growth and a de-rated 32x exit, ASML's EUV monopoly")
print(f"  and €132bn+ industry backlog visibility provide a floor few peers can match.")

print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        €{VOL_52W_LOW:.0f}  –  €{VOL_52W_HIGH:.0f}")
if VOL_DIVIDEND > 0:
    print(f"  Annual dividend:      €{VOL_DIVIDEND:.2f}/share  (yield {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized  (elevated — China-news whipsaws)")
print(f"  Beta vs broad market: {VOL_BETA:.2f}")
print(f"  1-sigma range (1yr):  €{vol_low_1yr:.0f}  –  €{vol_high_1yr:.0f}  (€{CURRENT_PRICE:.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  2-sigma range (1yr):  €{CURRENT_PRICE - 2*sigma_1yr:.0f}  –  €{CURRENT_PRICE + 2*sigma_1yr:.0f}")
print(f"  {'─'*60}")
print(f"  Bear €{SCENARIOS['BEAR'][2]} requires:  ~{sigma_needed_bear:.1f}σ price move  {'(unusual — requires fundamental break)' if sigma_needed_bear > 1.5 else '(within normal vol range)'}")
print(f"  ASML's 52-week range spans nearly 3x (€612–€1,741) — among the widest of any")
print(f"  mega-cap, reflecting binary sensitivity to US/Dutch export-policy headlines.")

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
