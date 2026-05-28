#!/usr/bin/env python3
"""
CTVA Signal Model  v1
─────────────────────
Corteva, Inc. (NYSE: CTVA) · Agricultural Sciences
Seeds (Pioneer brand + biotech traits) + Crop Protection
Planned separation into two independent public companies: Q4 2026E

Format: SOTP calculator → signal dashboard → bear anatomy →
        EPP → conservative growth → volatility → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 82.21
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

SCENARIOS = {
    "BEAR":  (2.00, 14,  28, "DOJ loyalty ruling + commodity crash; EPS halved; P/E at distress"),
    "BASE":  (3.58, 22,  79, "FY2026 guidance delivered; stable comps; modest P/E contraction"),
    "BULL":  (4.80, 26, 125, "Brazil trait accel + CP pricing recovery + separation re-rating"),
    "XBULL": (6.00, 30, 180, "Full ag supercycle; pure-play SpinCo/NewCo each re-rated at premium"),
}

# ── SUM OF PARTS CALCULATOR (Seed SpinCo + New Corteva CP · Q4 2026E) ─────────
SEED_REVENUE_B     = 9.90    # FY2025 Seed net sales ($B; Pioneer brand, traits)
SEED_EBITDA_MARGIN = 0.255   # ~25.5% EBITDA margin (seed/biotech premium business)
SEED_MULTIPLE      = 18.0    # EV/EBITDA — pure-play seed IP franchise (bear = 14x, bull = 22x)

CP_REVENUE_B       = 7.50    # FY2025 Crop Protection net sales ($B)
CP_EBITDA_MARGIN   = 0.180   # ~18.0% EBITDA margin (specialty chemical/ag CP profile)
CP_MULTIPLE        = 11.0    # EV/EBITDA — ag CP specialty chem peer (bear = 8x, bull = 14x)

SHARES_OUT_M       = 675.7   # shares outstanding (millions)
NET_DEBT_B         = 3.50    # approximate net debt ($B; post-$1.5B pension contribution)
SEPARATION_COSTS_B = 0.35    # one-time separation costs ($B; mgmt estimate)

def sotp_value():
    seed_ebitda  = SEED_REVENUE_B  * SEED_EBITDA_MARGIN
    cp_ebitda    = CP_REVENUE_B    * CP_EBITDA_MARGIN
    seed_ev      = seed_ebitda     * SEED_MULTIPLE
    cp_ev        = cp_ebitda       * CP_MULTIPLE
    total_ev     = seed_ev + cp_ev
    equity_val_b = total_ev - NET_DEBT_B - SEPARATION_COSTS_B
    per_share    = equity_val_b * 1000 / SHARES_OUT_M
    return seed_ebitda, cp_ebitda, seed_ev, cp_ev, total_ev, equity_val_b, per_share

# ── SIGNALS ───────────────────────────────────────────────────────────────────
SIGNALS = [
    ("US corn planted acreage — YoY", "% YoY",
     -8.0,  -6.0,   0.0,   3.0,  -3.5, True,
     "Prolonged acreage rotation → seed volume shortfall; US Seed EBITDA contracts"),

    ("Corn price — proxy grower economics", "$/bu",
      3.50,   4.00,   5.00,   6.00,  4.20, True,
     "Commodity crash → grower belt-tightening; seed upgrades deferred; CP volumes fall"),

    ("Brazil soy trait penetration", "%",
      5.0,    7.0,   10.0,  20.0,  11.0, True,
     "Trait adoption stalls; royalty runway shrinks; Brazil competitive advantage erodes"),

    ("Crop protection pricing — YoY", "% YoY",
     -8.0,   -4.0,    2.0,   5.0,  -1.0, True,
     "Generic flood (Chinese off-patent APIs); CP margins collapse; volume recovery fails"),

    ("Enlist trait penetration — US soybeans", "%",
     40.0,   50.0,   65.0,  80.0,  65.0, True,
     "Competing trait platforms displace Enlist; royalty stream and pricing power erode"),

    ("Novel product mix — % of CP sales from patented products", "%",
     40.0,   55.0,   70.0,  80.0,  67.0, True,
     "DOJ forces distribution restructure; patent cliff accelerates; generics flood channel"),
]
WEIGHTS = [0.20, 0.20, 0.20, 0.15, 0.15, 0.10]

STRUCTURAL_FACTORS = [
    ("Pioneer germplasm library — 60yr+ IP moat; irreplicable breeding advantage",  +0.8, 0.25),
    ("Brazil trait licensing model — multi-decade royalty expansion runway",          +0.6, 0.20),
    ("DOJ antitrust trial Oct 2026 — loyalty program forced restructuring risk",     -0.8, 0.25),
    ("Separation execution risk — $350M costs + synergy loss + index rebalancing",  -0.4, 0.15),
    ("Corn/soy commodity cycle — single-season earnings concentration",              -0.3, 0.15),
]

# ── EPP ───────────────────────────────────────────────────────────────────────
EPP_TODAY_EPS = 3.58    # FY2026E non-GAAP operating EPS (guidance midpoint $3.45–$3.70)
EPP_MIN_PE    = 14.0    # ag-input trough P/E (Bayer Crop distress / Syngenta buyout ~12–15x)
EPP_NOTE      = "(annual seed demand is non-discretionary; earnings floor above zero)"

# ── CONSERVATIVE GROWTH ───────────────────────────────────────────────────────
CONS_SIGNALS = [
    ("Corn acreage",         -5.0, "-5% YoY (vs -3.5%; acreage pressure persists into 2027)"),
    ("Corn price",            4.00, "$4.00/bu (vs $4.20; commodity remains weak)"),
    ("Brazil penetration",    8.5,  "8.5% (vs 11%; adoption slower than guidance)"),
    ("CP pricing",           -2.5, "-2.5% YoY (vs -1%; pricing recovery slower)"),
    ("Enlist US soy",        62.0, "62% (vs 65%; minimal incremental gains)"),
    ("Novel product mix",    63.0, "63% (vs 67%; a few patents roll off early)"),
]
CONS_EPS_CAGR = 0.07    # 7%/yr conservative (below consensus ~11%; DOJ + separation drag)
CONS_EXIT_PE  = 20.0    # 20x exit (contracts from ~22x; DOJ + separation uncertainty)
CONS_DIVIDEND = 0.72    # $0.72/yr (5th consecutive annual raise; ~6%/yr growth)

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.22
VOL_BETA       = 0.74
VOL_52W_LOW    = 60.54
VOL_52W_HIGH   = 85.63
VOL_DIVIDEND   = 0.72

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

seed_ebitda, cp_ebitda, seed_ev_b, cp_ev_b, total_ev_b, equity_val_b, sotp_per_shr = sotp_value()

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
print(f"  CTVA  ·  Corteva, Inc.  ·  ${CURRENT_PRICE:.2f}  ·  Agricultural Sciences")
print(f"  Signal: {signal}   Ratio B: {rb_fmt}   Adj gap: {adj_gap:+.2f}  [{_verdict}]")
print("═" * W)

# Sum of parts (CTVA-specific: separation into Seed SpinCo + New Corteva CP, Q4 2026E)
print(f"\n  SUM OF PARTS  (separation: Seed SpinCo + New Corteva CP  ·  Q4 2026E target)")
print("  " + "─" * (W - 2))
print(f"  Seed (Pioneer + traits):  ${SEED_REVENUE_B:.2f}B rev × {SEED_EBITDA_MARGIN*100:.1f}% EBITDA "
      f"= ${seed_ebitda:.2f}B EBITDA  ×  {SEED_MULTIPLE:.0f}x EV/EBITDA = ${seed_ev_b:.1f}B EV")
print(f"  Crop Protection:          ${CP_REVENUE_B:.2f}B rev × {CP_EBITDA_MARGIN*100:.1f}% EBITDA "
      f"= ${cp_ebitda:.2f}B EBITDA  ×  {CP_MULTIPLE:.0f}x EV/EBITDA = ${cp_ev_b:.1f}B EV")
print(f"  {'─'*60}")
print(f"  Combined EV:              ${total_ev_b:.1f}B")
print(f"  Less: net debt ${NET_DEBT_B}B + separation costs ${SEPARATION_COSTS_B}B:  "
      f"-${NET_DEBT_B + SEPARATION_COSTS_B:.2f}B")
print(f"  SOTP equity value:        ${equity_val_b:.1f}B  =  ${sotp_per_shr:.0f}/share")
mktcap_b = CURRENT_PRICE * SHARES_OUT_M / 1000
premium  = (CURRENT_PRICE - sotp_per_shr) / sotp_per_shr * 100
print(f"  Current market cap:       ${mktcap_b:.1f}B  (${CURRENT_PRICE:.2f}/share)")
print(f"  Premium / (discount):     {premium:+.1f}%  "
      f"({'← conglomerate premium; split needed to unlock value' if premium < 0 else '← market already prices separation optionality'})")
print(f"  Bull SOTP (Seed 22x / CP 14x): ~${(seed_ebitda*22 + cp_ebitda*14 - NET_DEBT_B - SEPARATION_COSTS_B)*1000/SHARES_OUT_M:.0f}/share")
print(f"  Bear SOTP (Seed 14x / CP  8x): ~${(seed_ebitda*14 + cp_ebitda*8  - NET_DEBT_B - SEPARATION_COSTS_B)*1000/SHARES_OUT_M:.0f}/share")

# ① SIGNAL DASHBOARD
print(f"\n  ① SIGNAL DASHBOARD")
print(f"  {'Signal':<38}  {'BEAR':>7}  {'BASE≥':>7}  {'BULL≥':>7}  {'XBULL≥':>7}  {'NOW':>7}  Score")
print("  " + "─" * (W - 2))
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    bv_s  = f"{bv:+.1f}"
    bf_s  = f"{bf:.1f}"
    blf_s = f"{blf:.1f}"
    xf_s  = f"{xf:.1f}"
    cv_s  = f"{cv:+.1f}"
    bar   = "█" * s + "░" * (4 - s)
    print(f"  {name:<38}  {bv_s:>7}  {bf_s:>7}  {blf_s:>7}  {xf_s:>7}  {cv_s:>7}  {ICONS[s]}  {bar}")

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
print(f"  {'Signal':<38}  {'Current':>8}  {'Bear val':>8}  {'Move':>8}  Trigger")
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    cv_s    = f"{cv:+.1f}"
    bv_s    = f"{bv:+.1f}"
    move_s  = f"{bv-cv:+.1f}"
    trigger = narr[:36] if len(narr) <= 36 else narr[:33] + "…"
    print(f"  {name:<38}  {cv_s:>8}  {bv_s:>8}  {move_s:>8}  {trigger}")

print(f"\n  Bear probability (proxy model):  {proxy_probs['BEAR']*100:.1f}%")
print(f"\n  KEY TRIGGER: DOJ October 2026 trial rules Corteva's crop protection")
print(f"  loyalty/rebate programs anticompetitive → forced restructuring → distributor")
print(f"  shift to generics. Simultaneously, corn price falls below $4.00 → growers")
print(f"  defer seed upgrades, CP purchase volumes decline. Joint probability event.")
print(f"  Separation one-time costs ($350M) + pension ($1.5B) amplify cash drag.")

# ③ EPP
print(f"\n  ③ UPDATED EPP  (floor anchored on today's fundamentals × trough multiple)")
print("  " + "─" * (W - 2))
print(f"  Today's normalized EPS:           ${EPP_TODAY_EPS:.2f}  (FY2026E non-GAAP operating EPS)")
print(f"  Min viable P/E at max pessimism:   {EPP_MIN_PE:.0f}x  {EPP_NOTE}")
print(f"  {'─'*60}")
print(f"  EPP floor:                        ${epp_updated:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${epp_updated:.0f}:   {epp_gap_pct:+.0f}%  "
      f"{'✓ cushion' if epp_gap_pct >= 0 else '← distressed zone'}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} vs EPP ${epp_updated:.0f}:   {bear_vs_epp_pct:+.0f}%  "
      f"{'← BEAR requires earnings impairment below EPP' if bear_vs_epp_pct < 0 else '✓ bear is cyclical'}")
print(f"\n  Note: Pioneer annual seed demand is non-discretionary — farmers must")
print(f"  rebuy every season. Even in recession, seed volumes decline modestly,")
print(f"  not collapse. The 14x floor reflects the combined distress P/E, not zero.")

# ④ CONSERVATIVE GROWTH
print(f"\n  ④ CONSERVATIVE GROWTH  (2-yr, BASE lower bound — no Brazil acceleration)")
print("  " + "─" * (W - 2))
for sname, sval, srat in CONS_SIGNALS:
    print(f"  {sname:<26}  {sval:>8.1f}   {srat[:44]}")

print(f"\n  Conservative 2yr EPS:   ${EPP_TODAY_EPS:.2f} × (1+{CONS_EPS_CAGR*100:.0f}%)² = ${cons_eps_2yr:.2f}")
print(f"  At {CONS_EXIT_PE:.0f}x P/E (conservative):  ${cons_price_2yr:.0f}/share")
print(f"  + Cumul. dividends (2yr):  +${cons_div_2yr:.2f}/share")
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:     ${cons_price_2yr:.0f}  "
      f"({'▲' if cons_price_2yr > CURRENT_PRICE else '▼'}{abs(cons_price_2yr - CURRENT_PRICE):.0f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:  {cons_total_ret:+.1f}% over 2yr  =  {cons_annual_ret:+.1f}%/yr")
print(f"\n  Key: at $82, 7% EPS growth + 20x exit ≈ breakeven. The market has already")
print(f"  priced in much of the EPS recovery from FY2024. Entry price matters — a")
print(f"  $68–72 entry (post-DOJ dip scenario) yields ~+20% 2yr conservative return.")

# ⑤ VOLATILITY
print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W - 2))
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  "
      f"(stock at {(CURRENT_PRICE-VOL_52W_LOW)/(VOL_52W_HIGH-VOL_52W_LOW)*100:.0f}th pct of range — near 52W HIGH)")
print(f"  Annual dividend:      ${VOL_DIVIDEND:.2f}/share  "
      f"(yield {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%  —  5th consecutive annual increase)")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized")
print(f"  Beta vs S&P 500:      {VOL_BETA:.2f}  (below market; seasonal ag input profile)")
print(f"  1-sigma range (1yr):  ${vol_low_1yr:.0f}  –  ${vol_high_1yr:.0f}  "
      f"(${CURRENT_PRICE:.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  {'─'*60}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} requires:  ~{sigma_needed_bear:.1f}σ move  "
      f"({'unusual — needs fundamental break' if sigma_needed_bear > 1.5 else 'within normal range'})")
print(f"  → Stock 4% from 52-week high. Limited margin of safety at current levels.")
print(f"  → DOJ October 2026 trial = event-driven vol opportunity. Buy the dip.")
print(f"  → WATCHLIST range: ${VOL_52W_LOW:.0f}–${(VOL_52W_LOW+VOL_52W_HIGH)/2:.0f};  "
      f"ACCUMULATE below ${(0.4*VOL_52W_LOW + 0.6*VOL_52W_HIGH):.0f}")

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
print(f"  WATCHLIST  ${VOL_52W_LOW:.0f}–{(VOL_52W_LOW+VOL_52W_HIGH)/2:.0f}  "
      f"|  ACCUMULATE ${(0.55*VOL_52W_LOW+0.45*VOL_52W_HIGH):.0f}–{(0.4*VOL_52W_LOW+0.6*VOL_52W_HIGH):.0f}  "
      f"|  BUY below ${0.65*VOL_52W_LOW+0.35*VOL_52W_HIGH:.0f}")
print(f"  DOJ October 2026 trial = key event risk. Accumulate if dip to $68–72 on verdict.")
print("═" * W)
