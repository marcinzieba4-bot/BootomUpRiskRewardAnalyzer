#!/usr/bin/env python3
"""
DOW Signal Model  v1
─────────────────────
Dow Inc. (NYSE: DOW) · Commodity Chemicals · Basic Resources
Polyethylene (P&SP) · Polyurethanes & Isocyanates (II&I) · Silicones/Coatings (PM&C)
Dividend cut 50% July 2025. Transform to Outperform: $2B+ EBITDA uplift target.
Path2Zero (Fort Saskatchewan): net-zero ethylene cracker; Phase 1 end-2029E.

Format: EBITDA recovery path → signal dashboard → bear anatomy →
        EPP (EV-based) → conservative growth → volatility → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 34.52
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

SCENARIOS = {
    # (placeholder_eps, placeholder_pe, price, narrative)
    "BEAR":  (0.00, 0,  15, "PE spike fades; China glut resumes; 2nd dividend cut; $2.5B EBITDA"),
    "BASE":  (0.60, 0,  38, "Q2 inflection holds; EBITDA $4.5B mid-cycle; Transform on-track"),
    "BULL":  (2.50, 0,  55, "Transform $2B delivered; EBITDA $5.3B; Path2Zero confidence"),
    "XBULL": (5.00, 0,  85, "Full Transform + Path2Zero; EBITDA $6.5B+; commodity upcycle"),
}

# ── EBITDA RECOVERY VALUE PATH  (EV/EBITDA framework; DOW-specific) ───────────
SHARES_OUT_M      = 718.0    # shares outstanding (millions)
NET_DEBT_B        = 13.1     # net debt ($B; Q1 2026)
EV_EBITDA_MULT    = 8.0      # historical reference multiple for commodity chemicals

EBITDA_STAGES = [
    ("Trough (FY2025 actual)",       3.3,  7.0, "No recovery; maintained trough"),
    ("Conservative recovery (2yr)",  4.0,  8.0, "Transform $700M; no Path2Zero uplift"),
    ("Consensus mid-cycle",          4.5,  8.0, "Transform broadly on track; mid-cycle"),
    ("Full Transform target",        5.3,  8.5, "$3.3B baseline + $2B Transform delivered"),
    ("Path2Zero + Transform (long)", 6.3,  9.0, "All programs; Path2Zero Phase 1 operational"),
    ("Q2 2026 run-rate (annualized)", 8.0,  9.0, "Middle East supply shock sustained full-year"),
]

def ebitda_to_equity(ebitda_b, multiple, debt_b=NET_DEBT_B):
    ev_b     = ebitda_b * multiple
    equity_b = ev_b - debt_b
    per_shr  = equity_b * 1000 / SHARES_OUT_M if equity_b > 0 else 0
    return ev_b, equity_b, per_shr

# ── SIGNALS ───────────────────────────────────────────────────────────────────
# Key context: Q1 2026 operating EPS -$0.14 (beat -$0.39 est); Q2 EBITDA guided $2B
# (vs Q1's $873M); PE price increases $0.50/lb cumulative Apr-May 2026; dividend $1.40/yr
SIGNALS = [
    ("NA ethane vs naphtha cracker advantage", "$/MT",
       200,  400,  800, 1200, 1200, True,
     "ME disruption ends; naphtha normalises; NA cost advantage collapses to ~$400"),

    ("Global PE demand growth — YoY", "% YoY",
       -3,    0,    3,    5,   -1, True,
     "China glut + global construction/auto weakness; PE volumes continue declining"),

    ("Transform to Outperform — annualized savings", "$M/yr",
       300,  500, 1000, 1500,  772, True,
     "Program execution fails; one-time costs not recovering into permanent savings"),

    ("Net debt / mid-cycle EBITDA leverage", "x",
       5.0,  4.5,  3.0,  2.0,  2.9, False,
     "Leverage stays above 4× mid-cycle; refinancing risk at 2029 maturity wall"),

    ("ME supply disruption — % global ethylene at risk", "%",
       1.0,  2.0,  5.0, 10.0, 12.0, True,
     "Middle East conflict resolves; supply returns; integrated margins normalize"),

    ("China new PE capacity additions", "MT/yr",
       5.0,  4.0,  2.0,  1.0,  4.0, False,
     "China PE capacity surge accelerates; global price ceiling depressed further"),
]
WEIGHTS = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]

STRUCTURAL_FACTORS = [
    ("NA ethane feedstock moat — structural $600-1200/MT advantage vs naphtha crackers", +0.6, 0.25),
    ("Path2Zero optionality — $1B EBITDA / net-zero PE from 2030; green premium",        +0.5, 0.20),
    ("Balance sheet constraint — $13B net debt + $1B/yr dividend cash drain",            -0.8, 0.25),
    ("Dividend at risk — already cut 50%; FCF negative FY2025; coverage very thin",      -0.5, 0.15),
    ("China structural overcapacity — persistent PE price ceiling; no near-term fix",    -0.4, 0.15),
]

# ── EPP (EV/EBITDA based — earnings negative at trough) ──────────────────────
EPP_EBITDA_B   = 3.3     # trough EBITDA ($B; FY2025 actual)
EPP_EV_MULT    = 7.0     # min viable EV/EBITDA for commodity chemicals at distress
EPP_NOTE       = "(equity floor at trough EBITDA $3.3B × 7× EV/EBITDA less $13.1B net debt)"

epp_ev_b       = EPP_EBITDA_B * EPP_EV_MULT
epp_equity_b   = epp_ev_b - NET_DEBT_B
EPP_FLOOR      = epp_equity_b * 1000 / SHARES_OUT_M   # $/share

# ── CONSERVATIVE GROWTH (2-yr, EBITDA-based) ─────────────────────────────────
CONS_EBITDA_B   = 4.0    # $B — Transform delivers $700M only; no Path2Zero uplift
CONS_EV_MULT    = 8.0    # conservative exit EV/EBITDA
CONS_DEBT_2YR_B = 12.5   # net debt in 2yr ($B; modest paydown from FCF recovery)
CONS_DIVIDEND   = 1.40   # $1.40/yr (maintained at current post-cut rate; not further cut)

cons_ev_b       = CONS_EBITDA_B * CONS_EV_MULT
cons_equity_b   = cons_ev_b - CONS_DEBT_2YR_B
cons_price_2yr  = cons_equity_b * 1000 / SHARES_OUT_M
cons_div_2yr    = CONS_DIVIDEND * 2
cons_total_val  = cons_price_2yr + cons_div_2yr
cons_total_ret  = (cons_total_val - CURRENT_PRICE) / CURRENT_PRICE * 100
cons_annual_ret = cons_total_ret / 2

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.40    # high vol; 52W range $20–$43 (+109% low-to-high swing)
VOL_BETA       = 0.60    # below market; chemical cycle trades vs own supply/demand
VOL_52W_LOW    = 20.40   # 52W low at dividend cut (Jul 2025)
VOL_52W_HIGH   = 42.74   # 52W high
VOL_DIVIDEND   = 1.40    # $1.40/yr (post-cut; was $2.80)

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

def market_implied_composite(target_ev, tolerance=2.0):
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

epp_gap_pct     = (CURRENT_PRICE - EPP_FLOOR) / EPP_FLOOR * 100
bear_vs_epp_pct = (SCENARIOS["BEAR"][2]  - EPP_FLOOR) / EPP_FLOOR * 100

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
print(f"  DOW  ·  Dow Inc.  ·  ${CURRENT_PRICE:.2f}  ·  Commodity Chemicals / Basic Resources")
print(f"  Signal: {signal}   Ratio B: {rb_fmt}   Adj gap: {adj_gap:+.2f}  [{_verdict}]")
print("═" * W)

# EBITDA recovery value path (DOW-specific: earnings are negative at trough)
print(f"\n  EBITDA RECOVERY VALUE PATH  (EV/EBITDA framework; EPS negative at trough)")
print("  " + "─" * (W - 2))
print(f"  {'Scenario':<34}  {'EBITDA':>7}  {'EV/E':>5}  {'EV ($B)':>8}  {'Equity/shr':>12}  Note")
for stage_name, ebitda_b, mult, note in EBITDA_STAGES:
    ev_b, eq_b, per_shr = ebitda_to_equity(ebitda_b, mult)
    flag = " ◄ CURRENT" if abs(per_shr - CURRENT_PRICE) < 5 else ""
    print(f"  {stage_name:<34}  ${ebitda_b:.1f}B  {mult:.0f}×  ${ev_b:.0f}B  "
          f"  ${per_shr:>6.0f}/shr{flag}  {note[:26]}")
print(f"\n  Net debt: ${NET_DEBT_B:.1f}B  ·  Shares: {SHARES_OUT_M:.0f}M  ·  Reference mult: {EV_EBITDA_MULT:.0f}× EV/EBITDA")
print(f"  Current ${CURRENT_PRICE:.2f} implies ~${CURRENT_PRICE + NET_DEBT_B*1000/SHARES_OUT_M:.0f}/shr EV "
      f"= ~${CURRENT_PRICE*SHARES_OUT_M/1000 + NET_DEBT_B:.0f}B total EV "
      f"= {(CURRENT_PRICE*SHARES_OUT_M/1000 + NET_DEBT_B)/4.5:.1f}× mid-cycle EBITDA ($4.5B)")

# ① SIGNAL DASHBOARD
print(f"\n  ① SIGNAL DASHBOARD  (EPS negative at trough; model uses EBITDA/cycle framework)")
print(f"  {'Signal':<40}  {'BEAR':>7}  {'BASE≥':>7}  {'BULL≥':>7}  {'XBULL≥':>7}  {'NOW':>7}  Score")
print("  " + "─" * (W - 2))
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    bv_s  = f"{bv:+.0f}"  if hib else f">{bv:.0f}"
    bf_s  = f"{bf:.0f}"
    blf_s = f"{blf:.0f}"
    xf_s  = f"{xf:.0f}"
    cv_s  = f"{cv:+.0f}"
    bar   = "█" * s + "░" * (4 - s)
    print(f"  {name:<40}  {bv_s:>7}  {bf_s:>7}  {blf_s:>7}  {xf_s:>7}  {cv_s:>7}  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:    {proxy_composite:.2f} / 4.00")
if mkt_composite:
    print(f"  Market composite:   {mkt_composite:.2f} / 4.00  "
          f"(back-solved from ${CURRENT_PRICE:.2f} + {REQUIRED_RETURN*100:.0f}% hurdle)")
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
    cv_s   = f"{cv:+.0f}"
    bv_s   = f"{bv:+.0f}" if hib else f">{bv:.0f}"
    move_s = f"{bv-cv:+.0f}" if hib else f"{cv-bv:+.0f}↑"
    trigger = narr[:36] if len(narr) <= 36 else narr[:33] + "…"
    print(f"  {name:<40}  {cv_s:>8}  {bv_s:>8}  {move_s:>8}  {trigger}")

print(f"\n  Bear probability (proxy model):  {proxy_probs['BEAR']*100:.1f}%")
print(f"\n  KEY TRIGGER: Middle East peace deal → naphtha normalises → NA ethane advantage")
print(f"  collapses from $1,200/MT to $400/MT. Simultaneously, China PE capacity floods")
print(f"  global markets (+5MT/yr new supply). EBITDA drops back to $2.5B. Transform")
print(f"  saves miss targets. Q2 $2B EBITDA guide proves a one-quarter spike.")
print(f"  Dividend is cut a second time. Stock re-tests 52-week low ($20.40) and below.")

# ③ EPP (EV/EBITDA based)
print(f"\n  ③ EPP  (EV/EBITDA based — EPS negative; floor = trough asset/earnings value)")
print("  " + "─" * (W - 2))
print(f"  Trough EBITDA (FY2025 actual):    ${EPP_EBITDA_B:.1f}B")
print(f"  Min viable EV/EBITDA at distress:  {EPP_EV_MULT:.0f}×")
print(f"  Trough EV:                         ${epp_ev_b:.1f}B")
print(f"  Less: net debt ${NET_DEBT_B:.1f}B  →  trough equity ${epp_equity_b:.1f}B")
print(f"  {'─'*60}")
print(f"  EPP floor {EPP_NOTE}:")
print(f"    = ${EPP_FLOOR:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP_FLOOR:.0f}:   {epp_gap_pct:+.0f}%  "
      f"({'← market pricing ABOVE trough; recovery already embedded' if epp_gap_pct > 50 else '← near floor'})")
print(f"  Bear ${SCENARIOS['BEAR'][2]} vs EPP ${EPP_FLOOR:.0f}:    {bear_vs_epp_pct:+.0f}%  "
      f"{'← BEAR ≈ EPP; floor is thin' if abs(bear_vs_epp_pct) < 20 else '← BEAR requires further impairment below trough equity'}")
print(f"\n  The {epp_gap_pct:+.0f}% premium to trough EPP means the market has already priced in")
print(f"  ~${CURRENT_PRICE - EPP_FLOOR:.0f}/share of recovery value above the floor. Full mid-cycle")
print(f"  ($4.5B EBITDA × 8x) implies ${ebitda_to_equity(4.5, 8.0)[2]:.0f}/share — within 8% of current price.")

# ④ CONSERVATIVE GROWTH (EBITDA-based)
print(f"\n  ④ CONSERVATIVE GROWTH  (2-yr; Transform delivers $700M only; Path2Zero delayed)")
print("  " + "─" * (W - 2))
print(f"  Conservative 2yr EBITDA:   ${CONS_EBITDA_B:.1f}B  (Transform $700M vs $2B target; no Path2Zero)")
print(f"  Exit EV/EBITDA:             {CONS_EV_MULT:.0f}×  (conservative; below historical average)")
print(f"  Implied EV:                ${cons_ev_b:.0f}B")
print(f"  Less: net debt in 2yr ($B): ${CONS_DEBT_2YR_B:.1f}B  (modest deleveraging from FCF recovery)")
print(f"  Implied equity value:       ${cons_equity_b:.1f}B  =  ${cons_price_2yr:.0f}/share")
print(f"  + Cumulative dividends:    +${cons_div_2yr:.2f}/share  (2yr × $1.40; assuming no 2nd cut)")
print(f"  {'─'*60}")
print(f"  Conservative 2yr total:     ${cons_total_val:.0f}  "
      f"({'▲' if cons_total_val > CURRENT_PRICE else '▼'}{abs(cons_total_val - CURRENT_PRICE):.0f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:  {cons_total_ret:+.1f}% over 2yr  =  {cons_annual_ret:+.1f}%/yr")
print(f"\n  Key: current price of ${CURRENT_PRICE:.2f} ALREADY prices in recovery above trough.")
print(f"  Conservative case (${cons_price_2yr:.0f}/shr eq + ${cons_div_2yr:.2f} div) = NEGATIVE return.")
print(f"  Breakeven requires EBITDA recovery to ≥$4.5B. Bull case needs ≥$5B.")
print(f"  Only the BULL scenario (Transform full delivery) justifies ${CURRENT_PRICE:.2f}+.")

# ⑤ VOLATILITY
print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W - 2))
pct_range = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW) * 100
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  "
      f"(stock at {pct_range:.0f}th pct; 52W low = dividend cut date Jul 2025)")
print(f"  Annual dividend:      ${VOL_DIVIDEND:.2f}/share  "
      f"(yield {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%  —  cut 50% from $2.80; paid since 1912)")
print(f"  Realized vol (2yr):   {VOL_ANNUAL_PCT*100:.0f}%  (high; 52W range spans +{(VOL_52W_HIGH-VOL_52W_LOW)/VOL_52W_LOW*100:.0f}% low-to-high)")
print(f"  Beta vs S&P 500:      {VOL_BETA:.2f}  (below market; trades on chemical cycle, not macro beta)")
print(f"  1-sigma range (1yr):  ${vol_low_1yr:.0f}  –  ${vol_high_1yr:.0f}  "
      f"(${CURRENT_PRICE:.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  {'─'*60}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} requires:  ~{sigma_needed_bear:.1f}σ move  "
      f"({'within range — stock already did it (52W low $20.40)' if sigma_needed_bear < 1.6 else 'unusual'})")
print(f"  → Dividend yield {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}% provides income while waiting for cycle turn.")
print(f"  → Dividend at risk ($0.35/qtr); confirm FCF positive before sizing a full position.")
print(f"  → ACCUMULATE range: ${CURRENT_PRICE:.0f}–$32  |  BUY below $28  |  Size small until Q2 data confirms")

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
print(f"  Upside    (→ Bull ${bull_p}):    {up*100:.1f}%")
print(f"  Ratio B   :  {rb_fmt}")
print(f"  Signal    :  {signal}")
print()
print("═" * W)
print(f"  Key catalysts: Q2 2026 EBITDA ($2B guided vs Q1's $873M) — the decisive test.")
print(f"  If Q2 delivers, upgrade to ◉ BUY. If Q2 misses, re-evaluate at $26–28.")
print(f"  ACCUMULATE $30–35  |  BUY below $28  |  Avoid sizing large before Q2 prints.")
print("═" * W)
