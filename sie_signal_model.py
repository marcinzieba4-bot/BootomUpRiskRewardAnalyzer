#!/usr/bin/env python3
"""
Siemens Signal Model  v1
──────────────────────
Siemens AG (Xetra/Frankfurt: SIE)  ·  Industrial Automation, Digitalization, Infrastructure
Trough year: 2023 (post-COVID industrial destocking)

New format: signal dashboard → bear anatomy → updated EPP →
            conservative growth → volatility context → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 289.68   # EUR, Xetra, 2026-08-26
REQUIRED_RETURN  = 0.15
HORIZON_YEARS    = 2

SCENARIOS = {
    "BEAR":  (195,  15,  180, "Industrial capex freeze; order backlog burns down; margin compression"),
    "BASE":  (270,  20,  310, "Backlog converts on schedule; DI/SI margins hold at guided ranges"),
    "BULL":  (330,  24,  400, "Data-center/semiconductor capex supercycle sustains order momentum"),
    "XBULL": (400,  28,  480, "Automation re-shoring wave + AI infrastructure buildout accelerates"),
}

# ── SIGNALS ───────────────────────────────────────────────────────────────────
SIGNALS = [
    ("Group orders growth YoY",        "% YoY",
      -10.0,   0.0,  10.0,  20.0,  14.0, True,
     "Industrial customers pause capex; short-cycle automation orders roll over"),

    ("Book-to-bill ratio",             "x",
      0.80,  0.95,  1.10,  1.30,   1.34, True,
     "Backlog burns down faster than bookings replace it; book-to-bill falls below 1"),

    ("Digital Industries margin",      "%",
      12.0,  17.0,  19.0,  21.0,   17.3, True,
     "Software mix shifts to lower-margin automation hardware; price competition intensifies"),

    ("Smart Infrastructure rev growth","% YoY",
      2.0,   8.0,  11.0,  14.0,   10.5, True,
     "Data-center and grid-infrastructure demand cools after multi-year investment cycle"),

    ("FY2026 EPS pre-PPA guidance",    "EUR",
      8.50, 10.00, 11.35, 12.50,  11.35, True,
     "Guidance cut mid-year as backlog conversion disappoints"),

    ("Order backlog",                  "EUR bn",
      95.0, 115.0, 132.0, 150.0,  132.0, True,
     "Large orders cancelled or deferred; backlog erodes from record levels"),
]
WEIGHTS = [0.20, 0.20, 0.20, 0.15, 0.15, 0.10]

STRUCTURAL_FACTORS = [
    ("Record €132bn backlog gives 12-18mo revenue visibility",  1.0, 0.30),
    ("Data-center/semiconductor automation secular tailwind",   0.6, 0.20),
    ("Siemens Healthineers + Energy stake volatility overlay", -0.3, 0.15),
    ("European industrial cycle sensitivity",                  -0.4, 0.20),
    ("Diversified conglomerate — no single customer >5% rev",   0.4, 0.15),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
EPP_TODAY_EPS    = 10.14   # trailing reported EPS, EUR
EPP_MIN_PE       = 15.0    # min viable P/E at panic — diversified industrial floor
EPP_HISTORICAL   = 160.0   # historical EPP v1 (approx)

# ── CONSERVATIVE GROWTH (2-yr, base-minus) ───────────────────────────────────
CONS_SIGNALS = [
    ("Group orders growth",     4.0, "+4% YoY (vs +14%; short-cycle demand normalizes)"),
    ("Book-to-bill ratio",      1.02, "1.02x (vs 1.34; backlog growth slows sharply)"),
    ("Digital Industries",     17.5, "17.5% margin (vs 17.3%; roughly stable, low end of guide)"),
    ("Smart Infrastructure",    8.0, "+8% YoY (vs +10.5%; data-center capex normalizes)"),
    ("FY2026 EPS",              10.50, "EUR10.50 (vs 11.35; low end of guided range)"),
    ("Order backlog",         120.0, "EUR120bn (vs 132bn; modest drawdown as orders normalize)"),
]
CONS_EPS_CAGR = 0.08     # 8%/yr conservative (vs recent double-digit growth)
CONS_EXIT_PE  = 20.0     # 20x exit (de-rate from current ~26x on EPS pre-PPA)
CONS_DIVIDEND = 5.60     # approx EUR5.60/yr annual dividend (current run-rate)

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.24
VOL_BETA       = 1.05
VOL_52W_LOW    = 198.00
VOL_52W_HIGH   = 291.50
VOL_DIVIDEND   = 5.60

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
cons_div_2yr    = CONS_DIVIDEND * (1 + 0.04) + CONS_DIVIDEND * (1 + 0.04) ** 2
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
print(f"  SIE  ·  Siemens AG  ·  €{CURRENT_PRICE:.2f}  ·  Industrial Automation & Infrastructure")
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
print(f"\n  KEY TRIGGER: European industrial recession + data-center capex pause simultaneously")
print(f"  → order intake falls below 1.0x book-to-bill for 2+ quarters, backlog erodes,")
print(f"  and margin mix shifts unfavorably. JOINT event: backlog alone cushions one shock.")

print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS:          €{EPP_TODAY_EPS:.2f}  (trailing reported, EUR)")
print(f"  Min viable P/E at panic:          {EPP_MIN_PE:.0f}x  [diversified industrial floor — automation + healthcare + energy mix]")
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
print(f"\n  Even at conservative 8% EPS growth and a de-rated 20x exit, the €132bn order")
print(f"  backlog gives multi-year revenue visibility few industrial peers can match.")

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
print(f"  Stock trades near its 52-week high after a record Q3 FY2026 order/guidance beat —")
print(f"  most of the near-term good news may already be priced in.")

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
