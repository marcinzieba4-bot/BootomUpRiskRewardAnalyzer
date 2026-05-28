#!/usr/bin/env python3
"""
NEM Signal Model  v2
─────────────────────
Newmont Corporation (NYSE: NEM)  ·  Gold Mining / Basic Resources

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 50.0      # USD (NYSE: NEM, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  ( 1.00,    8,   28,  "Gold crash $1,800; AISC inflation; Newcrest write-down"),
    "BASE":  ( 5.00,   11,   55,  "Gold $2,800-3,000 avg; AISC controlled; integration on track"),
    "BULL":  ( 7.00,   13,   91,  "Gold $3,500+; Newcrest synergies; copper credits boost"),
    "XBULL": (11.00,   11,  121,  "Gold supercycle $4,500+; record FCF; reserve expansion"),
}

# ── GOLD MARGIN CALCULATOR (NEM-specific structural feature) ──────────────────
GOLD_SPOT_USD_OZ         = 3300.0    # current spot (May 2026 ATH; ~+38% YoY)
GOLD_SPOT_PREV_YR_OZ     = 2380.0    # ~May 2025 average
NEM_GEO_PROD_MOZ         = 7.0       # M oz GEO (post-Newcrest divestiture programme; 2026E)
NEM_AISC_PER_OZ          = 1500      # all-in sustaining cost (blended group, 2026E)
NEM_COPPER_PROD_KT       = 155       # thousand tonnes copper-equivalent
COPPER_PRICE_USD_T       = 10000     # copper spot $/tonne (electrification demand)
NEM_SILVER_PROD_MOZ      = 18        # million oz silver (Newcrest contribution)
SILVER_PRICE_USD_OZ      = 33        # silver spot
NEM_CORP_OVERHEAD_B      = 7.0       # D&A ~$4B + G&A $0.5B + exploration $0.4B + interest $1.2B + reclamation $0.9B
NEM_TAX_RATE             = 0.28      # effective tax rate (multi-jurisdictional; royalties)
NEM_SHARES_B             = 1.25      # diluted shares outstanding post-Newcrest ($B)

def gold_margin_calculator():
    gold_rev_b      = NEM_GEO_PROD_MOZ * GOLD_SPOT_USD_OZ / 1000
    copper_rev_b    = NEM_COPPER_PROD_KT * COPPER_PRICE_USD_T / 1e6
    silver_rev_b    = NEM_SILVER_PROD_MOZ * SILVER_PRICE_USD_OZ / 1000
    total_rev_b     = gold_rev_b + copper_rev_b + silver_rev_b
    aisc_cost_b     = NEM_GEO_PROD_MOZ * NEM_AISC_PER_OZ / 1000
    gold_margin_oz  = GOLD_SPOT_USD_OZ - NEM_AISC_PER_OZ
    gold_margin_pct = gold_margin_oz / GOLD_SPOT_USD_OZ * 100
    operating_inc_b = total_rev_b - aisc_cost_b - NEM_CORP_OVERHEAD_B
    est_eps         = operating_inc_b * (1 - NEM_TAX_RATE) / NEM_SHARES_B
    # EPS sensitivity per $100 gold move
    eps_per_100     = (NEM_GEO_PROD_MOZ * 100 / 1000) * (1 - NEM_TAX_RATE) / NEM_SHARES_B
    # Scenario EPS bridge
    bear_ebit_b     = (NEM_GEO_PROD_MOZ * 1800 / 1000 + copper_rev_b + silver_rev_b
                       - aisc_cost_b - NEM_CORP_OVERHEAD_B)
    bear_eps        = bear_ebit_b * (1 - NEM_TAX_RATE) / NEM_SHARES_B
    bull_ebit_b     = (NEM_GEO_PROD_MOZ * 3500 / 1000 + copper_rev_b + silver_rev_b
                       - aisc_cost_b - NEM_CORP_OVERHEAD_B)
    bull_eps        = bull_ebit_b * (1 - NEM_TAX_RATE) / NEM_SHARES_B
    xbull_ebit_b    = (NEM_GEO_PROD_MOZ * 4500 / 1000 + copper_rev_b + silver_rev_b
                       - aisc_cost_b - NEM_CORP_OVERHEAD_B)
    xbull_eps       = xbull_ebit_b * (1 - NEM_TAX_RATE) / NEM_SHARES_B
    yoy_gain_oz     = GOLD_SPOT_USD_OZ - GOLD_SPOT_PREV_YR_OZ
    return (gold_rev_b, copper_rev_b, silver_rev_b, total_rev_b, aisc_cost_b,
            gold_margin_oz, gold_margin_pct, operating_inc_b, est_eps,
            eps_per_100, bear_eps, bull_eps, xbull_eps, yoy_gain_oz)

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────────
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("Gold spot price — YoY change",  "% YoY",
     -20.0,   0.0,  15.0,  35.0,  +35.0, True,
     "Gold crashes $1,800 on rate normalization; dollar soars"),

    ("AISC — YoY trend",              "% YoY",
      15.0,   8.0,   3.0,  -2.0,   +7.0, False,
     "AISC inflation >15%; energy/labour cost spiral; mines uneconomic"),

    ("Production volume — YoY",       "% YoY",
      -5.0,  -2.0,   3.0,   8.0,   +1.0, True,
     "Newcrest integration failure; mine suspensions; reserve depletion"),

    ("Net ETF flows (gold, t/mo)",    "t/mo",
     -30.0,   0.0,  20.0,  60.0,  +55.0, True,
     "Gold ETF liquidation; institutional de-risking; crypto substitute"),

    ("Copper price — YoY change",     "% YoY",
     -20.0,   0.0,  15.0,  30.0,  +11.0, True,
     "Copper crash destroys byproduct credit; real revenue declines"),

    ("USD Index — YoY change",        "% YoY",
       8.0,   4.0,   0.0,  -6.0,   -5.0, False,
     "Dollar surge +8%+; gold devalued in USD; demand collapses"),
]
WEIGHTS = [0.35, 0.20, 0.15, 0.10, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("Gold safe-haven / inflation-hedge secular demand",             1.0, 0.25),
    ("Newcrest synergies: $500M/yr target; high-grade copper-gold",  0.6, 0.20),
    ("Geopolitical / de-dollarisation CB gold demand tailwind",      0.8, 0.20),
    ("Reserve replacement risk: NEM depletes 8M oz/yr; cap intensive", -0.8, 0.20),
    ("Max operating leverage: AISC 44% of spot; 1:1 margin gearing", -0.3, 0.15),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
EPP_TODAY_EPS   = 4.50      # FY2026E non-GAAP EPS (~$3,300 spot; consensus lags gold ATH move)
EPP_MIN_PE      = 8.0       # min viable P/E at panic (gold-miner trough multiple)
EPP_HISTORICAL  = 30.0      # historical EPP v1 (2022 rate-shock trough)
EPP_REGIME_NOTE = "(gold miners get 8x trough: no earnings floor — EPS follows gold price)"

# ── CONSERVATIVE GROWTH (2-yr, base-minus assumptions) ────────────────────────
CONS_SIGNALS = [
    ("Gold spot",     5.0,  "+5% YoY (vs +35%; gold normalises post-ATH)"),
    ("AISC",          8.0,  "+8% YoY (vs +7%; labour/energy inflation persists)"),
    ("Production",    0.0,  "+0% YoY (vs +1%; Newcrest ramp slower than guided)"),
    ("Net ETF",      10.0,  "+10 t/mo (vs +55; ETF inflow normalises)"),
    ("Copper",        5.0,  "+5% YoY (vs +11%; copper demand growth cools)"),
    ("USD",           2.0,  "+2% YoY (vs -5%; partial dollar recovery)"),
]
CONS_EPS_CAGR   = 0.04      # 4%/yr (gold sideways; AISC inflates; limited EPS growth)
CONS_EXIT_PE    = 10.0      # 10x (below current ~11x; gold premium removed at flat price)
CONS_DIVIDEND   = 1.00      # $1.00/yr (post-Newcrest cut from $1.60; growing modestly)

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT  = 0.35      # high vol; gold miners ~2x gold bullion vol
VOL_BETA        = 1.20      # vs S&P 500 (correlated to gold, not market cycle)
VOL_52W_LOW     = 32.0      # approx (rate-scare dip; dollar strength episode)
VOL_52W_HIGH    = 58.0      # approx (gold ATH-driven high)
VOL_DIVIDEND    = 1.00

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

(gold_rev_b, copper_rev_b, silver_rev_b, total_rev_b, aisc_cost_b,
 gold_margin_oz, gold_margin_pct, operating_inc_b, est_eps,
 eps_per_100, bear_eps, bull_eps, xbull_eps, yoy_gain_oz) = gold_margin_calculator()

# Updated EPP
epp_updated     = EPP_TODAY_EPS * EPP_MIN_PE
epp_gap_pct     = (CURRENT_PRICE - epp_updated) / epp_updated * 100
bear_vs_epp_pct = (SCENARIOS["BEAR"][2] - epp_updated) / epp_updated * 100

# Conservative growth
cons_eps_2yr    = EPP_TODAY_EPS * ((1 + CONS_EPS_CAGR) ** 2)
cons_price_2yr  = cons_eps_2yr * CONS_EXIT_PE
cons_div_2yr    = CONS_DIVIDEND * (1 + 0.03) + CONS_DIVIDEND * (1 + 0.03) ** 2
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

# ── OUTPUT ────────────────────────────────────────────────────────────────────
print()
print("═" * W)
print(f"  NEM  ·  Newmont Corporation  ·  ${CURRENT_PRICE:.2f}  ·  Gold Mining")
print(f"  Verdict: {_verdict}  ·  Adj gap {adj_gap:+.2f}")
print("═" * W)

# Gold margin calculator
print(f"\n  GOLD MARGIN CALCULATOR  (gold price → margin → EPS bridge)")
print("  " + "─" * (W-2))
yoy_pct = yoy_gain_oz / GOLD_SPOT_PREV_YR_OZ * 100
print(f"  Gold spot (current):             ${GOLD_SPOT_USD_OZ:,.0f}/oz  "
      f"(+${yoy_gain_oz:.0f}/oz YoY, +{yoy_pct:.0f}% from ${GOLD_SPOT_PREV_YR_OZ:.0f})")
print(f"  NEM production (2026E):          {NEM_GEO_PROD_MOZ:.1f}M oz GEO  "
      f"(gold + copper/silver equivalents, post-Newcrest)")
print(f"  AISC (blended group):            ${NEM_AISC_PER_OZ:,}/oz   "
      f"(all-in sustaining cost, incl. Newcrest)")
print(f"  Gold margin:                     ${gold_margin_oz:,}/oz  "
      f"({gold_margin_pct:.0f}% of spot)")
print(f"  ─────────────────────────────────────────────────────")
print(f"  Gold revenue:                    ${gold_rev_b:.1f}B/yr")
print(f"  Copper byproduct ({NEM_COPPER_PROD_KT}kt @ ${COPPER_PRICE_USD_T/1000:.0f}k/t):   "
      f"${copper_rev_b:.1f}B/yr")
print(f"  Silver ({NEM_SILVER_PROD_MOZ}M oz @ ${SILVER_PRICE_USD_OZ}/oz):           "
      f"${silver_rev_b:.1f}B/yr")
print(f"  Total revenue:                   ${total_rev_b:.1f}B/yr")
print(f"  AISC cost ({NEM_GEO_PROD_MOZ:.1f}M oz × ${NEM_AISC_PER_OZ:,}/oz):    "
      f"${aisc_cost_b:.1f}B/yr")
print(f"  Corp overhead / D&A / other:     ${NEM_CORP_OVERHEAD_B:.1f}B/yr")
print(f"  Operating income:                ${operating_inc_b:.1f}B/yr   "
      f"→  Est. EPS: ${est_eps:.2f}  ({NEM_SHARES_B:.2f}B shares, {NEM_TAX_RATE*100:.0f}% tax)")
print(f"\n  EPS sensitivity to gold price moves:")
print(f"    +$100/oz gold  =  +${NEM_GEO_PROD_MOZ*100/1000*(1-NEM_TAX_RATE)/NEM_SHARES_B:.2f}/share/yr  "
      f"(operating leverage = max)")
print(f"    Bear  ($1,800/oz):  EPS ~${bear_eps:.2f}   margin ${1800-NEM_AISC_PER_OZ}/oz  "
      f"(rate shock; EPS goes negative in crash year)")
print(f"    Bull  ($3,500/oz):  EPS ~${bull_eps:.2f}   margin ${3500-NEM_AISC_PER_OZ:,}/oz")
print(f"    XBull ($4,500/oz):  EPS ~${xbull_eps:.2f}   margin ${4500-NEM_AISC_PER_OZ:,}/oz  "
      f"(supercycle; record FCF)")
print(f"  → NEM is a pure gold price bet. AISC is relatively fixed; "
      f"every $100 gold = +${eps_per_100:.2f} EPS.")

# ── ① SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print(f"\n  ① SIGNAL DASHBOARD")
print(f"  {'Signal':<30}  {'BEAR':>7}  {'BASE≥':>7}  {'BULL≥':>7}  {'XBULL≥':>7}  {'NOW':>7}  Score")
print("  " + "─" * (W-2))
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u     = unit.split()[0] if unit else ""
    bv_s  = f"{bv:+.0f}{u}" if hib else f">{bv:.0f}{u}"
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
    u       = unit.split()[0] if unit else ""
    cv_s    = f"{cv:+.0f}{u}"
    bv_s    = f"{bv:+.0f}{u}"
    move    = bv - cv
    move_s  = f"{move:+.0f}{u}"
    trigger = narr[:38] if len(narr) <= 38 else narr[:35] + "…"
    print(f"  {name:<30}  {cv_s:>8}  {bv_s:>8}  {move_s:>6}  {trigger}")

print(f"\n  Bear composite:  {bear_composite:.2f}  →  Bear scenario price: "
      f"~${expected_price(bear_probs):.0f}  (model)  /  ${SCENARIOS['BEAR'][2]} (defined)")
print(f"  Bear probability (proxy model):  {proxy_probs['BEAR']*100:.1f}%")
print(f"\n  KEY TRIGGER: Fed re-acceleration + dollar surge simultaneously drives gold")
print(f"  from $3,300 to $1,800-2,000 range (2022 playbook). At $1,800 gold, NEM's")
print(f"  margin compresses from ${gold_margin_oz:.0f}/oz to ~${1800-NEM_AISC_PER_OZ}/oz — EPS turns negative in crash year.")
print(f"  Newcrest write-down risk amplifies: $8B+ goodwill at risk if gold stays down.")

# ── ③ UPDATED EPP ────────────────────────────────────────────────────────────
print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS:           ${EPP_TODAY_EPS:.2f}  (FY2026E non-GAAP; gold ATH)")
print(f"  Min viable P/E at panic:           {EPP_MIN_PE:.0f}x  {EPP_REGIME_NOTE}")
print(f"  {'─'*60}")
print(f"  UPDATED EPP:                      ${epp_updated:.0f}/share")
print(f"  Historical EPP (v1, 2022 floor):  ${EPP_HISTORICAL:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.0f} vs Updated EPP ${epp_updated:.0f}:  {epp_gap_pct:+.0f}%  "
      f"{'✓ cushion' if epp_gap_pct >= 0 else '← in distressed zone'}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} vs Updated EPP ${epp_updated:.0f}:  {bear_vs_epp_pct:+.0f}%  "
      f"{'← BEAR requires impairment' if bear_vs_epp_pct < 0 else '✓ bear is cyclical'}")
print(f"\n  IMPORTANT: NEM's EPP is NOT robust — it is entirely dependent on gold price.")
print(f"  At $1,800 gold, EPS falls to ~$1.50 → EPP at 8x = $12. The floor follows gold.")

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

print(f"\n  Conservative 2yr EPS:   ${EPP_TODAY_EPS:.2f} × (1+{CONS_EPS_CAGR*100:.0f}%)² = ${cons_eps_2yr:.2f}")
print(f"  At {CONS_EXIT_PE:.0f}x P/E (conservative de-rate):  ${cons_price_2yr:.0f}/share")
print(f"  + Cumul. dividends (2yr):  +${cons_div_2yr:.2f}/share")
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:     ${cons_price_2yr:.0f}  "
      f"({'▲' if cons_price_2yr > CURRENT_PRICE else '▼'}{abs(cons_price_2yr - CURRENT_PRICE):.0f} "
      f"from ${CURRENT_PRICE:.0f})")
print(f"  Conservative total return:  {cons_total_ret:+.0f}% over 2yr  = {cons_annual_ret:+.0f}%/yr")
print(f"\n  Conservative case: gold flat at $3,300 = very modest EPS growth + slight de-rate.")
print(f"  NEM at $50 already prices gold ~sideways. Bull case requires gold continuation.")

# ── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        ${VOL_52W_LOW:.0f}  –  ${VOL_52W_HIGH:.0f}")
print(f"  Annual dividend:      ${VOL_DIVIDEND:.2f}/share  "
      f"(yield {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%; cut from $1.60 post-Newcrest)")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized  (gold miners ≈ 2× bullion vol)")
print(f"  Beta vs S&P 500:      {VOL_BETA:.2f}  (gold correlated, not market-cycle driven)")
print(f"  1-sigma range (1yr):  ${vol_low_1yr:.0f}  –  ${vol_high_1yr:.0f}  "
      f"(${CURRENT_PRICE:.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  2-sigma range (1yr):  ${CURRENT_PRICE - 2*sigma_1yr:.0f}  –  "
      f"${CURRENT_PRICE + 2*sigma_1yr:.0f}")
print(f"  {'─'*60}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} requires:  "
      f"~{sigma_needed_bear:.1f}σ price move  "
      f"{'(unusual — requires fundamental break)' if sigma_needed_bear > 1.5 else '(within normal range)'}")
print(f"  At {VOL_ANNUAL_PCT*100:.0f}% vol: bear ${SCENARIOS['BEAR'][2]} = "
      f"~{sigma_needed_bear:.1f}σ — plausible in a sharp gold reversal.")
print(f"  Dividend ${VOL_DIVIDEND:.2f}/yr = only {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}% buffer — not a yield story.")
print(f"  → NEM is a leveraged gold call option, not a dividend compounder. Size accordingly.")

# ── ⑥ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print(f"\n  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
print("  " + "─" * (W-2))
print(f"  {'Scenario':<8}  {'Price':>6}  {'Proxy%':>7}  {'Market%':>8}  "
      f"{'Gap':>6}  Description")
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    eps, mult, price, narr = SCENARIOS[k]
    pp     = proxy_probs[k]
    mp     = mkt_probs[k] if mkt_probs else 0
    gap_pp = pp - mp
    print(f"  {k:<8}  ${price:>5}  {pp*100:>6.1f}%  {mp*100:>7.1f}%  "
          f"{gap_pp*100:>+6.1f}pp  {narr}")

print(f"\n  Proxy EV (2yr): ${proxy_ev:.0f}  /  Market EV: ${mkt_ev:.0f}  /  "
      f"Current: ${CURRENT_PRICE:.0f}")
print(f"  Conservative EV (2yr, ④): ${cons_price_2yr:.0f} + ${cons_div_2yr:.2f} divs = "
      f"${cons_price_2yr + cons_div_2yr:.0f} total value")

print()
print("═" * W)
