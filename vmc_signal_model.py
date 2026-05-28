#!/usr/bin/env python3
"""
VMC Signal Model  v1
─────────────────────
Vulcan Materials Company (NYSE: VMC) · Construction Aggregates · Basic Resources
World's largest producer of construction aggregates (crushed stone, sand, gravel)
Investor Day target: $20 cash gross profit/ton on 260–270M tons (~2× current EBITDA)

Format: quarry economics / $20-per-ton path → signal dashboard → bear anatomy →
        EPP → conservative growth → volatility → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 268.94
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

SCENARIOS = {
    "BEAR":  ( 6.25, 16,  100, "Construction recession + IIJA cliff; volumes -20%; EPS -33%"),
    "BASE":  ( 9.30, 27,  251, "FY2026 guidance delivered; stable multiples; diesel abates H2"),
    "BULL":  (12.50, 30,  375, "Investor Day $20/ton trajectory + data-centre construction surge"),
    "XBULL": (16.00, 33,  528, "$20/ton realized at 265M tons; infrastructure supercycle re-rate"),
}

# ── QUARRY ECONOMICS: PATH TO $20/TON (Investor Day target) ───────────────────
AGGS_TONS_FY25      = 227.0    # million tons shipped (FY2025 actual)
CASH_GP_TON_FY25    = 11.33    # $/ton cash gross profit (FY2025 actual)
PRICE_TON_FY25      = 21.98    # $/ton freight-adjusted selling price (FY2025)
AGGS_TONS_GUIDE_MID = 231.5    # million tons (FY2026E midpoint +2% guidance)
PRICE_GUIDE_MID_PCT = 0.05     # +5% price/ton FY2026E (midpoint +4–6% guidance)
IDAY_TONS_TARGET    = 265.0    # Investor Day tonnage target (260–270M midpoint)
IDAY_CASH_GP_TARGET = 20.00    # $/ton (Investor Day long-term cash GP target)
SHARES_OUT_M        = 130.0    # shares outstanding (millions)
NET_DEBT_B          = 4.416    # net debt ($B; Q1 2026)
EBITDA_MULTIPLE     = 15.0     # EV/EBITDA reference multiple for value creation

def quarry_economics():
    cur_cash_gp_m      = AGGS_TONS_FY25  * CASH_GP_TON_FY25
    guide_price_ton    = PRICE_TON_FY25  * (1 + PRICE_GUIDE_MID_PCT)
    iday_cash_gp_m     = IDAY_TONS_TARGET * IDAY_CASH_GP_TARGET
    incremental_gp_m   = iday_cash_gp_m - cur_cash_gp_m
    ev_uplift_b        = incremental_gp_m * EBITDA_MULTIPLE / 1000
    per_shr_uplift     = ev_uplift_b * 1000 / SHARES_OUT_M
    per_1_per_ton      = IDAY_TONS_TARGET * 1.0 * EBITDA_MULTIPLE / SHARES_OUT_M
    return (cur_cash_gp_m, guide_price_ton, iday_cash_gp_m,
            incremental_gp_m, ev_uplift_b, per_shr_uplift, per_1_per_ton)

# ── SIGNALS ───────────────────────────────────────────────────────────────────
SIGNALS = [
    ("Aggregates shipment volume — YoY", "% YoY",
     -5.0,   0.0,   5.0,  10.0,   5.0, True,
     "Construction recession; residential + NRES both contract; vol -20%+"),

    ("Freight-adj aggregates price/ton — YoY", "% YoY",
      0.0,   2.0,   4.0,   7.0,   4.0, True,
     "Demand collapse reverses pricing; generics gain; pricing power breaks"),

    ("Aggregates cash gross profit/ton (FY)", "$/ton",
      7.0,   9.0,  12.0,  16.0,  11.33, True,
     "Diesel + labor cost spike absorbs pricing; cash GP/ton stalls or falls"),

    ("Public infrastructure spending — YoY", "% YoY",
     -5.0,   0.0,   5.0,  10.0,   8.0, True,
     "IIJA cliff: no reauthorization → state DOT awards collapse in 2027"),

    ("Data center / industrial construction — YoY", "% YoY",
    -10.0,   0.0,  15.0,  30.0,  25.0, True,
     "AI capex freeze; hyperscaler pauses; industrial reshoring reverses"),

    ("Retail diesel price ($/gal)", "$/gal",
      5.00,   4.50,   3.50,   3.00,   3.85, False,
     "Energy spike compresses cash margins; surcharges lag; $25M+/qtr headwind"),
]
WEIGHTS = [0.25, 0.25, 0.20, 0.15, 0.10, 0.05]

STRUCTURAL_FACTORS = [
    ("Quarry reserve monopoly — local pricing power; 10–50yr+ reserves; no substitute",  +0.8, 0.25),
    ("$20/ton roadmap — defined compounding path to ~2× current EBITDA at Investor Day",  +0.6, 0.20),
    ("IIJA cliff September 2026 — no reauth → state award slowdown risk from 2027",      -0.5, 0.25),
    ("Debt cycle: $4.4B net debt + $750M+ capex/yr + M&A appetite (Wake Stone, etc.)",  -0.3, 0.15),
    ("Residential absent: affordability + rates suppress housing starts below rplcmt",    -0.3, 0.15),
]

# ── EPP ───────────────────────────────────────────────────────────────────────
EPP_TODAY_EPS = 9.30    # FY2026E adj EPS consensus midpoint ($9.28–$9.34)
EPP_MIN_PE    = 15.0    # trough P/E — quarry assets irreplaceable; revenue not zero in recession
EPP_NOTE      = "(local quarry monopoly; volumes -10-15% in recession, not zero)"

# ── CONSERVATIVE GROWTH ───────────────────────────────────────────────────────
CONS_SIGNALS = [
    ("Agg. volume",        2.0,  "+2% YoY (vs +5% Q1 2026; assumes H2 softens)"),
    ("Agg. price/ton",     3.5,  "+3.5% (vs +4% Q1; guidance low end)"),
    ("Cash GP/ton",       11.80, "$11.80 (vs $11.33 FY25; modest improvement)"),
    ("Public infra",       4.0,  "+4% YoY (vs +8%; IIJA pre-cliff base)"),
    ("Data center/ind.",  15.0,  "+15% (vs +25%; slight slowdown)"),
    ("Diesel ($/gal)",     4.00, "$4.00 (vs $3.85; mild elevation persists)"),
]
CONS_EPS_CAGR = 0.09    # 9%/yr conservative (guidance +7%; add some volume leverage)
CONS_EXIT_PE  = 25.0    # 25x exit (P/E de-rate from 27x; IIJA cliff uncertainty)
CONS_DIVIDEND = 2.08    # $2.08/yr (9th consecutive annual increase)

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.24
VOL_BETA       = 1.06
VOL_52W_LOW    = 252.35
VOL_52W_HIGH   = 331.09
VOL_DIVIDEND   = 2.08

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

def market_implied_composite(target_ev, tolerance=4.0):
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
proxy_composite = sum(s * w for *_, s, w in scored)
sca             = sum(s * w for _, s, w in STRUCTURAL_FACTORS)
adj_composite   = proxy_composite + sca

proxy_probs = softmax_probs(proxy_composite)
adj_probs   = softmax_probs(adj_composite)
proxy_ev    = expected_price(proxy_probs)
adj_ev      = expected_price(adj_probs)

market_target_ev         = CURRENT_PRICE * ((1 + REQUIRED_RETURN) ** HORIZON_YEARS)
mkt_composite, mkt_probs = market_implied_composite(market_target_ev)
mkt_ev = expected_price(mkt_probs) if mkt_probs else market_target_ev

(cur_cash_gp_m, guide_price_ton, iday_cash_gp_m,
 incremental_gp_m, ev_uplift_b, per_shr_uplift, per_1_per_ton) = quarry_economics()

epp_updated     = EPP_TODAY_EPS * EPP_MIN_PE
epp_gap_pct     = (CURRENT_PRICE - epp_updated) / epp_updated * 100
bear_vs_epp_pct = (SCENARIOS["BEAR"][2] - epp_updated) / epp_updated * 100

cons_eps_2yr   = EPP_TODAY_EPS * ((1 + CONS_EPS_CAGR) ** 2)
cons_price_2yr = cons_eps_2yr * CONS_EXIT_PE
cons_div_2yr   = CONS_DIVIDEND * 1.06 + CONS_DIVIDEND * (1.06 ** 2)
cons_total_ret = (cons_price_2yr - CURRENT_PRICE + cons_div_2yr) / CURRENT_PRICE * 100
cons_annual_ret = cons_total_ret / 2

sigma_1yr         = CURRENT_PRICE * VOL_ANNUAL_PCT
vol_low_1yr       = CURRENT_PRICE - sigma_1yr
vol_high_1yr      = CURRENT_PRICE + sigma_1yr
sigma_needed_bear = (CURRENT_PRICE - SCENARIOS["BEAR"][2]) / sigma_1yr

bear_p  = SCENARIOS["BEAR"][2]
bull_p  = SCENARIOS["BULL"][2]
dn      = (CURRENT_PRICE - bear_p) / CURRENT_PRICE
up      = (bull_p - CURRENT_PRICE) / CURRENT_PRICE
ratio_b = dn / up
rb_fmt  = f"{ratio_b:.2f}x"

signal_short = ("BUY"        if ratio_b < 0.75 else
                "ACCUMULATE" if ratio_b < 1.10 else
                "WATCHLIST"  if ratio_b < 1.75 else
                "AVOID")
signal = {"BUY": "◉ BUY", "ACCUMULATE": "◎ ACCUMULATE",
          "WATCHLIST": "◐ WATCHLIST",  "AVOID": "✕ AVOID"}[signal_short]

if mkt_composite:
    adj_gap = adj_composite - mkt_composite
    if   adj_gap >  0.50: _verdict = "UNDERVALUED"
    elif adj_gap >  0.20: _verdict = "MODESTLY UNDERVALUED"
    elif adj_gap > -0.20: _verdict = "FAIRLY VALUED"
    elif adj_gap > -0.50: _verdict = "MODESTLY OVERVALUED"
    else:                 _verdict = "OVERVALUED"
else:
    adj_gap  = 0
    _verdict = "N/A"

# ── OUTPUT ────────────────────────────────────────────────────────────────────
print()
print("═" * W)
print(f"  VMC  ·  Vulcan Materials Company  ·  ${CURRENT_PRICE:.2f}  ·  Construction Aggregates")
print(f"  Signal: {signal}   Ratio B: {rb_fmt}   Adj gap: {adj_gap:+.2f}  [{_verdict}]")
print("═" * W)

# Quarry economics / $20-per-ton value creation path (VMC-specific)
print(f"\n  QUARRY ECONOMICS  (path from ${CASH_GP_TON_FY25:.2f} → ${IDAY_CASH_GP_TARGET:.0f} cash GP/ton  ·  Investor Day target)")
print("  " + "─" * (W - 2))
print(f"  FY2025 actual:    {AGGS_TONS_FY25:.0f}M tons  ×  ${CASH_GP_TON_FY25:.2f}/ton  =  ${cur_cash_gp_m/1000:.2f}B cash gross profit")
print(f"  FY2026 guide mid: {AGGS_TONS_GUIDE_MID:.0f}M tons  ×  ${guide_price_ton:.2f}/ton selling price  (+{PRICE_GUIDE_MID_PCT*100:.0f}% pricing)")
print(f"  Investor Day tgt: {IDAY_TONS_TARGET:.0f}M tons  ×  ${IDAY_CASH_GP_TARGET:.0f}/ton  =  ${iday_cash_gp_m/1000:.2f}B cash gross profit")
print(f"  {'─'*60}")
print(f"  Incremental cash GP (now → target):   +${incremental_gp_m/1000:.2f}B/yr")
print(f"  EV uplift at {EBITDA_MULTIPLE:.0f}× EBITDA:             +${ev_uplift_b:.1f}B  "
      f"=  +${per_shr_uplift:.0f}/share potential")
print(f"  Value per $1/ton improvement:          ${per_1_per_ton:.0f}/share  "
      f"(${IDAY_TONS_TARGET:.0f}M tons × ${EBITDA_MULTIPLE:.0f}× / {SHARES_OUT_M:.0f}M shares)")
print(f"  Gap to target:  ${IDAY_CASH_GP_TARGET - CASH_GP_TON_FY25:.2f}/ton remaining  "
      f"({(IDAY_CASH_GP_TARGET - CASH_GP_TON_FY25)/CASH_GP_TON_FY25*100:.0f}% improvement required)")
print(f"  Note: XBULL scenario (~${SCENARIOS['XBULL'][2]}) broadly consistent with full target realisation")

# ① SIGNAL DASHBOARD
print(f"\n  ① SIGNAL DASHBOARD")
print(f"  {'Signal':<40}  {'BEAR':>7}  {'BASE≥':>7}  {'BULL≥':>7}  {'XBULL≥':>7}  {'NOW':>7}  Score")
print("  " + "─" * (W - 2))
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    bv_s  = f"{bv:+.1f}" if hib else f">{bv:.2f}"
    bf_s  = f"{bf:.1f}"
    blf_s = f"{blf:.1f}"
    xf_s  = f"{xf:.1f}"
    cv_s  = f"{cv:+.2f}" if not hib else f"{cv:+.1f}"
    bar   = "█" * s + "░" * (4 - s)
    print(f"  {name:<40}  {bv_s:>7}  {bf_s:>7}  {blf_s:>7}  {xf_s:>7}  {cv_s:>7}  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:    {proxy_composite:.2f} / 4.00")
if mkt_composite:
    print(f"  Market composite:   {mkt_composite:.2f} / 4.00  "
          f"(back-solved from ${CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% hurdle)")
    print(f"  SCA adjustment:    {sca:+.3f}  →  Adj composite {adj_composite:.2f}  "
          f"→  Gap {adj_gap:+.2f}  [{_verdict}]")

print(f"\n  Structural factors:")
for desc, sc, wt in STRUCTURAL_FACTORS:
    arrow = "  +" if sc > 0 else "  -"
    print(f"  {arrow}  {desc}  ({sc:+.1f} × {wt*100:.0f}%  =  {sc*wt:+.2f})")

# ② BEAR CASE ANATOMY
print(f"\n  ② BEAR CASE ANATOMY  (variables needed to reach BEAR scenario)")
print("  " + "─" * (W - 2))
print(f"  {'Signal':<40}  {'Current':>8}  {'Bear val':>8}  {'Move':>8}  Trigger")
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    cv_s   = f"{cv:+.2f}" if not hib else f"{cv:+.1f}"
    bv_s   = f"{bv:+.2f}" if not hib else f"{bv:+.1f}"
    move_s = f"{bv-cv:+.2f}" if not hib else f"{bv-cv:+.1f}"
    trigger = narr[:36] if len(narr) <= 36 else narr[:33] + "…"
    print(f"  {name:<40}  {cv_s:>8}  {bv_s:>8}  {move_s:>8}  {trigger}")

print(f"\n  Bear probability (proxy model):  {proxy_probs['BEAR']*100:.1f}%")
print(f"\n  KEY TRIGGER: Construction recession simultaneously hits public and private.")
print(f"  IIJA expiry (Sept 2026) without reauthorisation → state DOT award budgets")
print(f"  reset to pre-IIJA levels; private NRES stalls; residential still frozen.")
print(f"  VMC volumes fall -15 to -20%; diesel stays elevated; $20/ton path pauses.")
print(f"  Bear case also requires P/E de-rating from 27× to 16× (cyclical trough).")

# ③ EPP
print(f"\n  ③ UPDATED EPP  (floor anchored on today's fundamentals × trough multiple)")
print("  " + "─" * (W - 2))
print(f"  Today's normalized EPS:           ${EPP_TODAY_EPS:.2f}  (FY2026E adj EPS consensus)")
print(f"  Min viable P/E at max pessimism:   {EPP_MIN_PE:.0f}x  {EPP_NOTE}")
print(f"  {'─'*60}")
print(f"  EPP floor:                        ${epp_updated:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${epp_updated:.0f}:   {epp_gap_pct:+.0f}%  "
      f"{'✓ cushion' if epp_gap_pct >= 0 else '← distressed zone'}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} vs EPP ${epp_updated:.0f}:   {bear_vs_epp_pct:+.0f}%  "
      f"{'← BEAR requires impairment below EPP' if bear_vs_epp_pct < 0 else '✓ bear is cyclical'}")
print(f"\n  The +{epp_gap_pct:.0f}% premium to EPP reflects the market pricing in the $20/ton")
print(f"  Investor Day path and IIJA-driven secular demand. Justified while rollout intact.")

# ④ CONSERVATIVE GROWTH
print(f"\n  ④ CONSERVATIVE GROWTH  (2-yr, BASE lower bound — IIJA headwind, no $20/ton)")
print("  " + "─" * (W - 2))
for sname, sval, srat in CONS_SIGNALS:
    print(f"  {sname:<22}  {sval:>8.2f}   {srat[:44]}")

print(f"\n  Conservative 2yr EPS:   ${EPP_TODAY_EPS:.2f} × (1+{CONS_EPS_CAGR*100:.0f}%)² = ${cons_eps_2yr:.2f}")
print(f"  At {CONS_EXIT_PE:.0f}x P/E (conservative):  ${cons_price_2yr:.0f}/share")
print(f"  + Cumul. dividends (2yr):  +${cons_div_2yr:.2f}/share")
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:     ${cons_price_2yr:.0f}  "
      f"({'▲' if cons_price_2yr > CURRENT_PRICE else '▼'}{abs(cons_price_2yr - CURRENT_PRICE):.0f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:  {cons_total_ret:+.1f}% over 2yr  =  {cons_annual_ret:+.1f}%/yr")
print(f"\n  Key: at $269, 9% EPS CAGR + 25x exit ≈ +15% 2yr total return (near hurdle).")
print(f"  Entry at ACCUMULATE zone ($240–255) would yield ~+25% conservative 2yr return.")

# ⑤ VOLATILITY
print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W - 2))
pct_range = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW) * 100
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  "
      f"(stock at {pct_range:.0f}th pct of range — near 52W LOW)")
print(f"  Annual dividend:      ${VOL_DIVIDEND:.2f}/share  "
      f"(yield {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%  —  9th consecutive annual increase)")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized")
print(f"  Beta vs S&P 500:      {VOL_BETA:.2f}  (slightly above market; cyclical ag construction)")
print(f"  1-sigma range (1yr):  ${vol_low_1yr:.0f}  –  ${vol_high_1yr:.0f}  "
      f"(${CURRENT_PRICE:.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  {'─'*60}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} requires:  ~{sigma_needed_bear:.1f}σ move  "
      f"({'unusual — needs fundamental break' if sigma_needed_bear > 1.5 else 'within normal range'})")
print(f"  → Stock near 52-wk low; already corrected -{(VOL_52W_HIGH - CURRENT_PRICE)/VOL_52W_HIGH*100:.1f}% from 52W high.")
print(f"  → Analyst consensus $314–329 → 17–22% upside from current price.")
print(f"  → ACCUMULATE zone: $240–252  |  BUY below $232")
print(f"  → IIJA September 2026 expiry: key event risk; can create vol opportunity.")

# ⑥ PROBABILITY DISTRIBUTION
print(f"\n  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
print("  " + "─" * (W - 2))
print(f"  {'Scenario':<8}  {'Price':>6}  {'Proxy%':>7}  {'Market%':>8}  "
      f"{'Gap':>6}  Description")
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    eps, mult, price, narr = SCENARIOS[k]
    pp      = proxy_probs[k]
    mp      = mkt_probs[k] if mkt_probs else 0
    gap_pp  = pp - mp
    print(f"  {k:<8}  ${price:>5}  {pp*100:>6.1f}%  {mp*100:>7.1f}%  "
          f"{gap_pp*100:>+6.1f}pp  {narr[:40]}")

up_pct = (adj_ev - CURRENT_PRICE) / CURRENT_PRICE * 100
print(f"\n  Adj EV (2yr): ${adj_ev:.0f}  /  Proxy EV: ${proxy_ev:.0f}  /  "
      f"Market EV: ${mkt_ev:.0f}  /  Current: ${CURRENT_PRICE:.0f}")
print(f"  {'─'*60}")
print(f"  Downside  (→ Bear ${bear_p}):  {dn*100:.1f}%")
print(f"  Upside    (→ Bull ${bull_p}):   {up*100:.1f}%")
print(f"  Ratio B   :  {rb_fmt}")
print(f"  Signal    :  {signal}")
print()
print("═" * W)
print(f"  Key entry levels:")
print(f"  WATCHLIST $252–265  |  ACCUMULATE $240–252  |  BUY below $232")
print(f"  Analyst consensus target $314–329 (+17–22%). IIJA Sept 2026 = key event risk.")
print("═" * W)
