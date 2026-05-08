#!/usr/bin/env python3
"""
OKE Signal Model  v2
─────────────────────
ONEOK Inc. (NYSE: OKE)  ·  Midstream Energy
Trough year: 2020 (oil crash / COVID pipeline panic)

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 78.0
REQUIRED_RETURN  = 0.15
HORIZON_YEARS    = 2

SCENARIOS = {
    "BEAR":  ( 5.0,  8,  35, "NGL crash + leverage stress + div cut"),
    "BASE":  ( 8.0,  9,  70, "Steady EBITDA growth; deleveraging on track"),
    "BULL":  (10.5, 10, 105, "AI/LNG demand surge; NGL spreads wide"),
    "XBULL": (13.0, 11, 145, "Gas super-cycle; Magellan synergies exceed"),
}

# ── SIGNALS ───────────────────────────────────────────────────────────────────
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("Permian assoc. gas — YoY",      "% YoY",
     -3.0,   5.0,  10.0,  18.0,   11.0, True,
     "Oil <$55 → E&P capex cut → Permian rig count drops → assoc. gas falls"),

    ("US nat. gas demand — YoY",      "% YoY",
     -1.0,   3.0,   7.0,  12.0,    8.0, True,
     "Warm winters + AI capex pause; LNG utilisation drops below 85%"),

    ("NGL frac. hub utilisation",     "%",
     68.0,  78.0,  85.0,  93.0,   88.0, True,
     "Gas price spike → ethane rejection → fracs run empty; keep-whole losses"),

    ("Magellan crude throughput",     "Mbpd",
    560.0, 630.0, 680.0, 720.0,  715.0, True,
     "Permian crude oversupply → producers route to rail; Longline underutilised"),

    ("Net debt / EBITDA",             "x ND/EBITDA",
      5.2,   4.5,   3.5,   2.8,    3.8, False,
     "EBITDA falls faster than debt repays; covenant pressure; div cut risk"),

    ("Dividend growth (guided)",      "% yr",
      0.0,   1.0,   3.0,   6.0,    3.5, True,
     "Coverage <1.2x → freeze/cut; destroys midstream equity multiple"),
]
WEIGHTS = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("Integrated NGL chain + Magellan: irreplaceable infrastructure",  1.0, 0.25),
    ("AI data centre / LNG export: secular gas demand tailwind",       0.8, 0.20),
    ("Elevated leverage 3.8x ND/EBITDA post-acquisitions",           -0.8, 0.25),
    ("35-40% commodity NGL margin exposure vs fee-based peers",      -0.5, 0.20),
    ("3 acquisitions in 3 years: integration execution overhang",    -0.3, 0.10),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
# Anchored on TODAY's earnings × trough multiple (not a historical price + adjustments).
# "If maximum pessimism hit the market TODAY, what price would the business justify?"
# For a pipeline: EBITDA × min_viable_EV/EBITDA − net debt.
# New regime note: AI data-center gas demand raises the floor multiple from
# the 2020-era 7.0x to 7.5x — gas pipelines now carry a structural demand premium
# not present in 2020 (when the fear was stranded-asset risk).
EPP_TODAY_EBITDA_B   = 7.8    # FY2025E EBITDA ($B) — today's actual earning power
EPP_MIN_EV_EBITDA    = 7.5    # minimum viable EV/EBITDA at max pessimism (raised from 7x)
EPP_NET_DEBT_B       = 26.0   # current net debt ($B)
EPP_SHARES_M         = 570.0  # diluted shares (M)
EPP_HISTORICAL       = 44.0   # historical EPP (2020 trough + adjustments, from v1)

# ── CONSERVATIVE GROWTH (2-3yr, base-minus assumptions) ───────────────────────
# Each signal held at the LOWER end of BASE — no tailwinds assumed.
# Compute 2yr EBITDA growth conservatively; apply slight re-rating on deleveraging.
CONS_SIGNALS = [
    # (name, conservative_value, rationale)  — name must start with SIGNALS[i] first word
    ("Permian assoc. gas",    5.0,  "+5% YoY (vs current +11%); lower rig count assumed"),
    ("US nat. gas demand",    3.0,  "+3% YoY (vs current +8%); no AI upside assumed"),
    ("NGL frac. hub",        80.0,  "80% (vs current 88%); partial ethane rejection"),
    ("Magellan crude",       650.0, "650 Mbpd (vs current 715); modest Permian slowdown"),
    ("Net debt / EBITDA",     3.7,  "3.7x (vs current 3.8x; deleveraging but slow)"),
    ("Dividend growth",        2.0,  "2%/yr (vs guided 3.5%; conservative re-cut risk)"),
]
CONS_EBITDA_CAGR = 0.05      # 5%/yr conservative EBITDA growth (vs analyst ~9%)
CONS_EV_EBITDA   = 9.0       # multiple held flat (no re-rating assumed)
CONS_DEBT_PAYDOWN_B = 1.0    # $B debt repaid per year (conservative)

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT   = 0.28      # 2yr realized annualized volatility (~28%)
VOL_BETA         = 0.85      # beta vs S&P 500
VOL_52W_LOW      = 58.0      # 52-week low
VOL_52W_HIGH     = 94.0      # 52-week high
VOL_DIVIDEND     = 4.12      # annual dividend ($)

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
epp_updated      = (EPP_TODAY_EBITDA_B * EPP_MIN_EV_EBITDA - EPP_NET_DEBT_B) * 1000 / EPP_SHARES_M
epp_gap_pct      = (CURRENT_PRICE - epp_updated) / epp_updated * 100
bear_vs_epp_pct  = (SCENARIOS["BEAR"][2] - epp_updated) / epp_updated * 100

# Conservative growth
cons_ebitda_2yr  = EPP_TODAY_EBITDA_B * ((1 + CONS_EBITDA_CAGR) ** 2)
cons_debt_2yr    = EPP_NET_DEBT_B - CONS_DEBT_PAYDOWN_B * 2
cons_equity_2yr  = (cons_ebitda_2yr * CONS_EV_EBITDA - cons_debt_2yr) * 1000 / EPP_SHARES_M
cons_div_2yr     = VOL_DIVIDEND * (1 + 0.02) + VOL_DIVIDEND * (1 + 0.02) ** 2   # 2 yrs divs
cons_total_ret   = (cons_equity_2yr - CURRENT_PRICE + cons_div_2yr) / CURRENT_PRICE * 100
cons_annual_ret  = cons_total_ret / 2

# Volatility
sigma_1yr        = CURRENT_PRICE * VOL_ANNUAL_PCT
vol_low_1yr      = CURRENT_PRICE - sigma_1yr
vol_high_1yr     = CURRENT_PRICE + sigma_1yr
sigma_needed_bear= (CURRENT_PRICE - SCENARIOS["BEAR"][2]) / sigma_1yr

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
print(f"  OKE  ·  ONEOK Inc.  ·  ${CURRENT_PRICE:.2f}  ·  Midstream Energy")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

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
    # Truncate narrative to fit
    trigger = narr[:38] if len(narr) <= 38 else narr[:35] + "…"
    print(f"  {name:<30}  {cv_s:>8}  {bv_s:>8}  {move_s:>6}  {trigger}")

print(f"\n  Bear composite:  {bear_composite:.2f}  →  Bear scenario price: "
      f"~${expected_price(bear_probs):.0f}  (model)  /  ${SCENARIOS['BEAR'][2]} (defined)")
print(f"  Bear probability (proxy model):  {proxy_probs['BEAR']*100:.1f}%")
print(f"\n  KEY TRIGGER: NGL keep-whole losses simultaneously with leverage >4.5x")
print(f"  causes dividend coverage to fall below 1.2x → cut → multiple collapse.")
print(f"  This is a JOINT PROBABILITY event — each leg alone doesn't produce bear.")

# ── ③ UPDATED EPP ────────────────────────────────────────────────────────────
print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EBITDA:       ${EPP_TODAY_EBITDA_B:.1f}B  (FY2025E actuals)")
print(f"  Min viable EV/EBITDA at panic:    {EPP_MIN_EV_EBITDA:.1f}x  "
      f"(raised from 7.0x in 2020 → AI/LNG secular demand = new regime)")
print(f"  → Trough EV:                     ${EPP_TODAY_EBITDA_B * EPP_MIN_EV_EBITDA:.1f}B")
print(f"  Less net debt:                  -${EPP_NET_DEBT_B:.0f}B")
print(f"  → Equity value:                  ${EPP_TODAY_EBITDA_B * EPP_MIN_EV_EBITDA - EPP_NET_DEBT_B:.1f}B"
      f"  /  {EPP_SHARES_M:.0f}M shares")
print(f"  {'─'*60}")
print(f"  UPDATED EPP:                     ${epp_updated:.0f}/share")
print(f"  Historical EPP (v1, 2020 adj):   ${EPP_HISTORICAL:.0f}/share  "
      f"(+${epp_updated - EPP_HISTORICAL:.0f} — EBITDA grew $3.5B→$7.8B)")
print(f"  Current ${CURRENT_PRICE:.0f} vs Updated EPP ${epp_updated:.0f}:  "
      f"{'+' if epp_gap_pct>=0 else ''}{epp_gap_pct:.0f}%  "
      f"{'✓ cushion' if epp_gap_pct >= 0 else '← in distressed zone'}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} vs Updated EPP ${epp_updated:.0f}:  "
      f"{bear_vs_epp_pct:+.0f}%  "
      f"{'← BEAR requires EBITDA impairment, not just price drop' if bear_vs_epp_pct < 0 else '✓'}")

# ── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print(f"\n  ④ CONSERVATIVE GROWTH  (2-yr, all signals at BASE lower bound — no tailwinds)")
print("  " + "─" * (W-2))
print(f"  {'Signal':<30}  {'Conservative':>14}  vs Current  Rationale")
for sname, sval, srat in CONS_SIGNALS:
    # find the current value
    cur = next(cv for name, _, __, ___, ____, _____, cv, ______, _______ in SIGNALS
               if name.lower().startswith(sname.split()[0].lower()))
    diff = sval - cur
    diff_s = f"{diff:+.0f}"
    print(f"  {sname:<30}  {sval:>14.1f}  {diff_s:>9}   {srat[:30]}")

print(f"\n  Conservative 2yr EBITDA:   ${EPP_TODAY_EBITDA_B:.1f}B × "
      f"(1+{CONS_EBITDA_CAGR*100:.0f}%)² = ${cons_ebitda_2yr:.2f}B")
print(f"  Net debt (after paydown):  ${cons_debt_2yr:.1f}B  "
      f"(-${CONS_DEBT_PAYDOWN_B:.0f}B/yr free cash repayment)")
print(f"  At {CONS_EV_EBITDA:.0f}x EV/EBITDA (no re-rating):  "
      f"EV ${cons_ebitda_2yr * CONS_EV_EBITDA:.1f}B  →  equity ${cons_equity_2yr:.0f}/share")
print(f"  + Cumul. dividends (2yr):  +${cons_div_2yr:.2f}/share  "
      f"(${VOL_DIVIDEND:.2f} growing 2%/yr)")
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:     ${cons_equity_2yr:.0f}  "
      f"({'▲' if cons_equity_2yr > CURRENT_PRICE else '▼'}{abs(cons_equity_2yr - CURRENT_PRICE):.0f} "
      f"from ${CURRENT_PRICE:.0f})")
print(f"  Conservative total return:  {cons_total_ret:+.0f}% over 2yr  "
      f"= {cons_annual_ret:+.0f}%/yr  (incl. dividend)")
print(f"\n  Key: even conservative growth triggers re-rating as leverage drops <3.5x.")
print(f"  No BULL scenario required. Base-minus is sufficient for double-digit returns.")

# ── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        ${VOL_52W_LOW:.0f}  –  ${VOL_52W_HIGH:.0f}")
print(f"  Annual dividend:      ${VOL_DIVIDEND:.2f}/share  "
      f"(yield {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized")
print(f"  Beta vs S&P 500:      {VOL_BETA:.2f}  (below market; defensive income stock)")
print(f"  1-sigma range (1yr):  ${vol_low_1yr:.0f}  –  ${vol_high_1yr:.0f}  "
      f"(${CURRENT_PRICE:.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  2-sigma range (1yr):  ${CURRENT_PRICE - 2*sigma_1yr:.0f}  –  "
      f"${CURRENT_PRICE + 2*sigma_1yr:.0f}")
print(f"  {'─'*60}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} requires:  "
      f"~{sigma_needed_bear:.1f}σ price move  "
      f"{'(unusual — requires fundamental break)' if sigma_needed_bear > 1.5 else '(within normal range)'}")
print(f"  Dividend buffer:      ${VOL_DIVIDEND:.2f}/yr absorbs ~{VOL_DIVIDEND/CURRENT_PRICE*100:.1f}% "
      f"of annual price drawdown")
print(f"  → Midstream is low-beta income. Buy on dividend yield expansion (>6% = attractive).")
print(f"  → OKE yield today: {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%.  "
      f"Attractive >6% = price <${VOL_DIVIDEND/0.06:.0f}.")

# ── ⑥ PROBABILITY DISTRIBUTION ───────────────────────────────────────────────
print(f"\n  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
print("  " + "─" * (W-2))
print(f"  {'Scenario':<8}  {'Price':>6}  {'Proxy%':>7}  {'Market%':>8}  "
      f"{'Gap':>6}  Description")
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    ebitda, mult, price, narr = SCENARIOS[k]
    pp  = proxy_probs[k]
    mp  = mkt_probs[k] if mkt_probs else 0
    gap_pp = pp - mp
    print(f"  {k:<8}  ${price:>5}  {pp*100:>6.1f}%  {mp*100:>7.1f}%  "
          f"{gap_pp*100:>+6.1f}pp  {narr}")

print(f"\n  Proxy EV (2yr): ${proxy_ev:.0f}  /  Market EV: ${mkt_ev:.0f}  /  "
      f"Current: ${CURRENT_PRICE:.0f}")
print(f"  Conservative EV (2yr, ④): ${cons_equity_2yr:.0f} + ${cons_div_2yr:.2f} divs = "
      f"${cons_equity_2yr + cons_div_2yr:.0f} total value")

print()
print("═" * W)
