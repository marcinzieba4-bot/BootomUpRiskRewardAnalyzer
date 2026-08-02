"""
UST  ·  US Treasury Bonds  ·  Fixed Income Signal Model
Bottom-up risk/reward analysis adapted for the interest rate cycle
Date: 2026-08-02
Context: New Fed Chair Kevin Warsh (hawkish hold); $2T/yr net issuance; 30Y at 19-yr high (5.28%)
         1/3 of US Treasury debt matures 2026 — massive rollover risk; China reducing UST holdings
"""

import math

# ── TICKER / METADATA ──────────────────────────────────────────────────────────
TICKER   = "UST"
NAME     = "US Treasury Bonds"
SECTOR   = "Fixed Income · Sovereign · Duration Risk · Rate Cycle"
DATE     = "2026-08-02"

# ── YIELD CURVE (July 31, 2026) ────────────────────────────────────────────────
YIELDS = {
    "3M":  4.05,
    "2Y":  4.29,
    "5Y":  4.46,
    "10Y": 4.74,   # benchmark — used as the "price" analog
    "30Y": 5.28,
}

# ── DURATION & CONVEXITY (approximate modified duration) ──────────────────────
DURATIONS  = {"2Y": 1.90, "5Y": 4.50, "10Y": 8.50, "30Y": 18.00}
CONVEXITY  = {"2Y": 0.05, "5Y": 0.25, "10Y": 0.85, "30Y": 4.50}

# ── ROLL YIELD (annualized, per tenor) ────────────────────────────────────────
# Roll yield = Duration × (current yield − interpolated 1yr-shorter yield)
# Interpolated: 1Y≈4.00%, 4Y≈4.40%, 9Y≈4.68%, 29Y≈5.25%
ROLL_YIELDS = {
    "2Y":  round(1.90 * (4.29 - 4.00) / 100, 4),   # 1.90 × 0.29% = 0.55%
    "5Y":  round(4.50 * (4.46 - 4.40) / 100, 4),   # 4.50 × 0.06% = 0.27%
    "10Y": round(8.50 * (4.74 - 4.68) / 100, 4),   # 8.50 × 0.06% = 0.51%
    "30Y": round(18.0 * (5.28 - 5.25) / 100, 4),   # 18.0 × 0.03% = 0.54%
}

# ── SCENARIO YIELD SHIFTS (1-year horizon) ────────────────────────────────────
# BEAR  = +150bps (higher-for-longer; supply shock; inflation resurgence)
# BASE  = flat    (rates on hold; term premium stable)
# BULL  = -100bps (growth slowdown; demand inflows; Fed pivots)
# XBULL = -200bps (recession; flight-to-quality; emergency Fed cuts)
DELTA_YIELD = {"BEAR": +0.0150, "BASE": 0.0, "BULL": -0.0100, "XBULL": -0.0200}

# ── SCENARIO TOTAL RETURNS ────────────────────────────────────────────────────
# total_return = coupon + roll_yield + price_change + convexity_adjustment
# price_change = -Duration × delta_yield
# convexity_adj = 0.5 × Convexity × delta_yield²

def _total_return(tenor, scenario):
    y   = YIELDS[tenor] / 100          # coupon (current yield approx)
    r   = ROLL_YIELDS[tenor]            # roll yield
    dur = DURATIONS[tenor]
    cvx = CONVEXITY[tenor]
    dy  = DELTA_YIELD[scenario]
    pc  = -dur * dy                     # price change
    ca  = 0.5 * cvx * dy ** 2          # convexity adjustment
    return round((y + r + pc + ca) * 100, 2)   # as %

SCENARIO_RETURNS = {}
for t in ("2Y", "5Y", "10Y", "30Y"):
    SCENARIO_RETURNS[t] = {s: _total_return(t, s) for s in ("BEAR", "BASE", "BULL", "XBULL")}

# ── RATIO B (bond version) ────────────────────────────────────────────────────
# ratio_b = max(0, -bear_return%) / bull_return%
# BUY: < 0.50  |  ACCUMULATE: < 0.75  |  WATCHLIST: < 1.20  |  AVOID: >= 1.20

def _ratio_b(tenor):
    bear = SCENARIO_RETURNS[tenor]["BEAR"]
    bull = SCENARIO_RETURNS[tenor]["BULL"]
    if bull <= 0:
        return float("inf")
    return round(max(0.0, -bear) / bull, 3)

def _bond_signal(rb):
    if rb == float("inf"):
        return "AVOID", "✕ AVOID"
    if rb < 0.50:
        return "BUY", "◉ BUY"
    if rb < 0.75:
        return "ACCUMULATE", "◎ ACCUMULATE"
    if rb < 1.20:
        return "WATCHLIST", "◐ WATCHLIST"
    return "AVOID", "✕ AVOID"

TENOR_RATIO_B = {t: _ratio_b(t) for t in ("2Y", "5Y", "10Y", "30Y")}
TENOR_SIGNALS = {t: _bond_signal(TENOR_RATIO_B[t]) for t in TENOR_RATIO_B}

# ── BENCHMARK: 10Y ────────────────────────────────────────────────────────────
ratio_b_10y    = TENOR_RATIO_B["10Y"]
signal_short   = TENOR_SIGNALS["10Y"][0]
signal_full    = TENOR_SIGNALS["10Y"][1]
ratio_b_str    = f"{ratio_b_10y:.3f}x"

# ── BARBELL vs BULLET vs FUTURES OVERLAY ──────────────────────────────────────
# BARBELL  = 50% 2Y + 50% 30Y  (effective duration ≈ 0.5×1.90 + 0.5×18.00 = 9.95 ≈ 10Y)
# BULLET   = 100% 10Y
# FUTURES  = 10% margin → 100% notional 10Y futures exposure; 90% cash parked at 2Y yield
#   Futures overlay formula: 10% × 10 × 10Y_return + 90% × 2Y_return

barbell = {
    s: round(0.50 * SCENARIO_RETURNS["2Y"][s] + 0.50 * SCENARIO_RETURNS["30Y"][s], 2)
    for s in ("BEAR", "BASE", "BULL")
}
bullet = {s: SCENARIO_RETURNS["10Y"][s] for s in ("BEAR", "BASE", "BULL")}

futures_overlay = {
    "BASE": round(0.10 * 10 * SCENARIO_RETURNS["10Y"]["BASE"] + 0.90 * SCENARIO_RETURNS["2Y"]["BASE"], 2),
    "BEAR": round(0.10 * 10 * SCENARIO_RETURNS["10Y"]["BEAR"] + 0.90 * SCENARIO_RETURNS["2Y"]["BEAR"], 2),
}

# ── SUPPLY / DEMAND SCA FACTORS ───────────────────────────────────────────────
# score ∈ [-1, +1]; positive = bond-bullish (rates fall); negative = bond-bearish (rates rise)
SCA_FACTORS = [
    ("US deficit / net issuance ($2T/yr)",        -0.70, 0.25,
     "Largest peacetime borrower; $2T annual supply absorbs global demand"),
    ("Term premium re-rating risk",                -0.55, 0.20,
     "Warsh era: Fed unlikely to suppress long-end via QE; 19yr high on 30Y"),
    ("China UST selling (reserve diversification)",-0.45, 0.15,
     "PBoC reducing UST; structural shift in marginal buyer base"),
    ("Fed QT (balance sheet shrink)",              -0.30, 0.15,
     "Fed not reinvesting maturities; removes backstop buyer"),
    ("Bank demand (SLR-constrained)",              +0.35, 0.10,
     "Banks absorbing 55% of net issuance; supportive but regulated limit"),
    ("Recession hedge / flight-to-quality",        +0.55, 0.10,
     "In recession, 10Y/30Y see massive rallies; insurance value is real"),
    ("Rollover risk (1/3 debt matures 2026)",      -0.40, 0.05,
     "Concentrated near-term supply = front-end pressure; auction risk"),
]

SCA_SCORE = round(sum(score * weight for _, score, weight, _ in SCA_FACTORS), 4)

# ── RATE CYCLE PROXY SIGNALS (1=BEAR → 4=XBULL) ──────────────────────────────
RATE_SIGNALS = [
    {
        "name":       "Fed policy direction (Warsh hawkish hold)",
        "weight":     0.25,
        "thresholds": ("Hiking", "On hold", "Easing", "Emergency cuts"),
        "now":        "On hold",
        "score":      1.5,
        "comment":    "Warsh: hawkish hold; higher-for-longer bias; no pivot signal; between BEAR (hiking) and BASE (hold)",
    },
    {
        "name":       "Inflation trajectory / breakevens",
        "weight":     0.25,
        "thresholds": (">4%", "2–3.5%", "~2%", "<1.5%"),
        "now":        "~2.8%",
        "comment":    "CPI moderating but services sticky; breakevens anchored ~2.4%; BASE — neither hike nor cut pressure",
        "score":      2.0,
    },
    {
        "name":       "US fiscal deficit / supply pressure",
        "weight":     0.20,
        "thresholds": (">$2T", "$1–2T", "<$1T", "Surplus"),
        "now":        "~$1.9T",
        "comment":    "$1.9T FY2026 deficit; $2T gross issuance; net supply overwhelming private demand; between BEAR and BASE",
        "score":      1.5,
    },
    {
        "name":       "Growth outlook / recession probability",
        "weight":     0.15,
        "thresholds": ("Boom", "Steady", "Slowing", "Recession"),
        "now":        "Slowing",
        "comment":    "Growth decelerating; consumer spending softening; labor market cooling; no recession YET → BASE/BULL mix",
        "score":      2.0,
    },
    {
        "name":       "Foreign demand / USD reserve status",
        "weight":     0.10,
        "thresholds": ("Selling", "Flat", "Buying", "Strong inflows"),
        "now":        "Selling",
        "comment":    "China reducing UST; reserve diversification into gold/EM; USD share of reserves declining → lean BEAR",
        "score":      1.5,
    },
    {
        "name":       "Term premium vs historical norm",
        "weight":     0.05,
        "thresholds": ("Rising fast", "Elevated", "Normal", "Compressed"),
        "now":        "Elevated",
        "comment":    "Term premium rising; 30Y at 19yr high; ACM model term premium ~1.2%; above neutral → BASE",
        "score":      2.0,
    },
]

assert abs(sum(s["weight"] for s in RATE_SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = round(sum(s["score"] * s["weight"] for s in RATE_SIGNALS), 3)
ADJ_COMPOSITE   = round(PROXY_COMPOSITE + SCA_SCORE, 3)

# Market composite: what rate scenario does the market price?
# At 4.74% 10Y with positive term premium and flat-to-hawkish Fed,
# the market prices roughly BASE/mild bear → composite ≈ 2.10
MARKET_COMPOSITE = 2.10
ADJ_GAP          = round(ADJ_COMPOSITE - MARKET_COMPOSITE, 2)

if ADJ_GAP > 0.20:
    valuation_label = "UNDERVALUED"        # structural backdrop better than priced
elif ADJ_GAP > -0.20:
    valuation_label = "FAIRLY VALUED"
else:
    valuation_label = "OVERVALUED"         # structural risks exceed market pricing

# ── CONSERVATIVE 2-YEAR RETURN (10Y compounded base) ─────────────────────────
base_10y_annual = SCENARIO_RETURNS["10Y"]["BASE"] / 100   # 5.25%
cons_return_2yr = round(((1 + base_10y_annual) ** 2 - 1) * 100, 1)

# ── EPP ANALOG: base carry return (yield + roll) = floor yield ────────────────
epp_gap_pct = round(YIELDS["10Y"] + ROLL_YIELDS["10Y"] * 100, 2)   # = 4.74 + 0.51 = 5.25%

# ── BEST VALUE TENOR ──────────────────────────────────────────────────────────
# 2Y: ratio_b=0.00 (BUY — no bear downside), 5Y: ratio_b≈0.22 (BUY — higher carry)
# 5Y is the sweet spot: best carry + low ratio_b vs. 2Y's near-zero term premium
BEST_TENOR = "5Y"

# ─────────────────────────────────────────────────────────────────────────────
#  OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
W = 76

def hr(): print("  " + "─" * W)
def bar_rate(score):
    """Rate cycle bar: ↓ = rates rise (BEAR), ↑ = rates fall (BULL)"""
    filled = round(score)
    return "●" * filled + "○" * (4 - filled)

print()
print("═" * (W + 4))
print(f"  {TICKER}  ·  {NAME}  ·  10Y Yield: {YIELDS['10Y']:.2f}%  ·  {SECTOR}")
print(f"  Signal (10Y): {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print(f"  Date: {DATE}  |  30Y at 19-yr high ({YIELDS['30Y']:.2f}%)  |  Warsh hawkish hold  |  $2T/yr net issuance")
print("═" * (W + 4))

# ── ① YIELD CURVE SNAPSHOT ────────────────────────────────────────────────────
print()
print("  ① YIELD CURVE SNAPSHOT  (July 31, 2026 — positively sloped; no inversion)")
hr()
print(f"  {'Tenor':<8}  {'Yield':>8}  {'vs 2Y (bps)':>12}  {'vs 3M (bps)':>12}  {'Dur':>6}  {'Convexity':>10}")
hr()
for t, y in YIELDS.items():
    vs2y = round((y - YIELDS["2Y"]) * 100, 0) if t != "2Y" else 0
    vs3m = round((y - YIELDS["3M"]) * 100, 0)
    dur  = DURATIONS.get(t, "—")
    cvx  = CONVEXITY.get(t, "—")
    dur_s = f"{dur:.2f}" if isinstance(dur, float) else "—"
    cvx_s = f"{cvx:.2f}" if isinstance(cvx, float) else "—"
    flag  = " ◄ BENCHMARK" if t == "10Y" else ""
    print(f"  {t:<8}  {y:>7.2f}%  {vs2y:>+11.0f}  {vs3m:>+11.0f}  {dur_s:>6}  {cvx_s:>10}{flag}")
hr()
spread_2s10s = round((YIELDS["10Y"] - YIELDS["2Y"]) * 100, 0)
spread_2s30s = round((YIELDS["30Y"] - YIELDS["2Y"]) * 100, 0)
spread_5s30s = round((YIELDS["30Y"] - YIELDS["5Y"]) * 100, 0)
spread_3m10s = round((YIELDS["10Y"] - YIELDS["3M"]) * 100, 0)
print(f"  Key spreads:  2s10s {spread_2s10s:+.0f}bps  |  2s30s {spread_2s30s:+.0f}bps  |  5s30s {spread_5s30s:+.0f}bps  |  3m10s {spread_3m10s:+.0f}bps")
print()
print(f"  CURVE COMMENT: Curve fully un-inverted (2s10s +{spread_2s10s:.0f}bps). Steepening driven by long-end")
print(f"  supply pressure, NOT a Fed pivot. 30Y at 5.28% reflects term premium re-rating, not growth")
print(f"  expectations. 2Y anchored at 4.29% = market pricing Fed on hold through 2026. Back end")
print(f"  steepening with {spread_2s30s:.0f}bps 2s30s = bond vigilantes demanding premium for duration risk.")
print(f"  Historical context: pre-GFC normal = ~50bps 2s10s; current {spread_2s10s:.0f}bps is above neutral.")

# ── ② ROLL YIELD ANALYSIS ─────────────────────────────────────────────────────
print()
print("  ② ROLL YIELD ANALYSIS  (annualized price gain as bond ages down the curve)")
hr()
print(f"  {'Tenor':<8}  {'Current Yield':>13}  {'→ 1yr older':>12}  {'Interpolated':>12}  {'Roll Yield':>10}  {'Total Carry':>12}")
hr()
interp_data = {
    "2Y":  ("1Y",  4.00),
    "5Y":  ("4Y",  4.40),
    "10Y": ("9Y",  4.68),
    "30Y": ("29Y", 5.25),
}
for t in ("2Y", "5Y", "10Y", "30Y"):
    y    = YIELDS[t]
    r    = ROLL_YIELDS[t]
    old, interp_y = interp_data[t]
    total_carry = round(y + r * 100, 2)
    print(f"  {t:<8}  {y:>12.2f}%  {old:>12}  {interp_y:>11.2f}%  {r*100:>9.2f}%  {total_carry:>11.2f}%")
    print(f"    Duration {DURATIONS[t]:.2f} × ({y:.2f}% − {interp_y:.2f}%) = {r*100:.2f}% roll pickup/yr")
hr()
print(f"  Roll yield is highest at 2Y (largest slope in short end) and 10Y.")
print(f"  5Y has minimal roll (curve nearly flat 4Y–5Y); thin reward for rolling here.")
print(f"  Total carry = coupon + roll — this is the BASE return if rates stay flat.")

# ── ③ SCENARIO TOTAL RETURNS ─────────────────────────────────────────────────
print()
print("  ③ SCENARIO TOTAL RETURNS  (1-year horizon, %)")
print(f"  BEAR=+150bps  |  BASE=flat  |  BULL=−100bps  |  XBULL=−200bps")
hr()
print(f"  {'Tenor':<8}  {'Duration':>9}  {'BEAR':>8}  {'BASE':>8}  {'BULL':>8}  {'XBULL':>8}  {'Ratio B':>9}  Signal")
hr()
for t in ("2Y", "5Y", "10Y", "30Y"):
    sr  = SCENARIO_RETURNS[t]
    rb  = TENOR_RATIO_B[t]
    sig = TENOR_SIGNALS[t][1]
    rb_s = f"{rb:.3f}x" if rb != float("inf") else "N/A"
    flag = " ◄" if t == BEST_TENOR else ""
    print(f"  {t:<8}  {DURATIONS[t]:>9.2f}  {sr['BEAR']:>+7.2f}%  {sr['BASE']:>+7.2f}%  {sr['BULL']:>+7.2f}%  {sr['XBULL']:>+7.2f}%  {rb_s:>9}  {sig}{flag}")
hr()

print()
print(f"  RETURN MATH (10Y as example, +150bps BEAR case):")
print(f"    coupon     = {YIELDS['10Y']:.2f}%")
print(f"    roll yield = {ROLL_YIELDS['10Y']*100:.2f}%  (8.50 × ({YIELDS['10Y']:.2f}% − 4.68%) ÷ 100)")
print(f"    price chg  = −8.50 × (+1.50%) = −{8.50*1.50:.2f}%")
print(f"    convexity  = 0.5 × 0.85 × 0.015² = +{0.5*0.85*0.015**2*100:.3f}%")
print(f"    TOTAL      = {YIELDS['10Y']:.2f}% + {ROLL_YIELDS['10Y']*100:.2f}% − {8.50*1.50:.2f}% + {0.5*0.85*0.015**2*100:.3f}% = {SCENARIO_RETURNS['10Y']['BEAR']:+.2f}%")
print()
print(f"  KEY INSIGHT: 2Y barely bleeds in BEAR (+1.99%) — short duration = safety cushion.")
print(f"  5Y offers 4.73% carry with only −2.02% downside — best risk/reward in pure bonds.")
print(f"  10Y's convexity ({CONVEXITY['10Y']:.2f}) provides meaningful upside optionality: BULL +13.75%, XBULL +22.27%.")
print(f"  30Y is volatility: −21% in BEAR, +24% in BULL — pure rate-cycle directional bet.")

# ── ④ RATIO B PER TENOR ──────────────────────────────────────────────────────
print()
print("  ④ RATIO B PER TENOR  (bond risk/reward; BUY<0.50 | ACCUM<0.75 | WATCH<1.20 | AVOID≥1.20)")
hr()
print(f"  {'Tenor':<8}  {'Bear (-)':>10}  {'Bull (+)':>10}  {'Ratio B':>9}  {'Signal':<16}  Assessment")
hr()
for t in ("2Y", "5Y", "10Y", "30Y"):
    bear = SCENARIO_RETURNS[t]["BEAR"]
    bull = SCENARIO_RETURNS[t]["BULL"]
    rb   = TENOR_RATIO_B[t]
    sig  = TENOR_SIGNALS[t][1]
    rb_s = f"{rb:.3f}x"
    downside = max(0.0, -bear)
    asmt = {
        "2Y":  "Bear is positive — carry exceeds duration loss at +150bps",
        "5Y":  "Strong BUY: carry+roll absorbs most of bear shock",
        "10Y": "ACCUMULATE: attractive carry; asymmetric upside",
        "30Y": "WATCHLIST: bear drawdown large; convexity helps but insufficient",
    }[t]
    print(f"  {t:<8}  {downside:>9.2f}%  {bull:>9.2f}%  {rb_s:>9}  {sig:<16}  {asmt}")
hr()
print(f"  Best value tenor: {BEST_TENOR} (BUY signal; ratio_b {TENOR_RATIO_B[BEST_TENOR]:.3f}x; optimal carry + limited bear loss)")
print(f"  2Y is risk-free in our bear scenario but offers 69bps less yield than 5Y.")
print(f"  10Y benchmark: ACCUMULATE — not a screaming BUY but attractive for long horizons.")
print(f"  30Y WATCHLIST — hold only as recession hedge; ratio_b {TENOR_RATIO_B['30Y']:.3f}x near the AVOID threshold.")

# ── ⑤ BARBELL vs BULLET vs FUTURES OVERLAY ──────────────────────────────────
print()
print("  ⑤ BARBELL vs BULLET vs FUTURES OVERLAY")
hr()
barbell_dur = 0.5 * DURATIONS["2Y"] + 0.5 * DURATIONS["30Y"]
print(f"  BARBELL  = 50% 2Y + 50% 30Y  (eff. duration {barbell_dur:.2f} ≈ 10Y's {DURATIONS['10Y']:.2f})")
print(f"  BULLET   = 100% 10Y           (duration {DURATIONS['10Y']:.2f})")
print(f"  FUTURES  = 10% margin 10Y futures + 90% 2Y cash (capital-efficient leverage)")
print()
print(f"  {'Strategy':<30}  {'BEAR':>8}  {'BASE':>8}  {'BULL':>8}  Commentary")
hr()
print(f"  {'Barbell (50% 2Y + 50% 30Y)':<30}  {barbell['BEAR']:>+7.2f}%  {barbell['BASE']:>+7.2f}%  {barbell['BULL']:>+7.2f}%  Convexity > bullet; more curve exposure")
print(f"  {'Bullet (100% 10Y)':<30}  {bullet['BEAR']:>+7.2f}%  {bullet['BASE']:>+7.2f}%  {bullet['BULL']:>+7.2f}%  Single-point duration; less spread risk")
print(f"  {'Futures overlay (10% × 10 + 90% 2Y)':<30}  {futures_overlay['BEAR']:>+7.2f}%  {futures_overlay['BASE']:>+7.2f}%  {'N/A':>8}  Capital-efficient; earn 2Y carry + 10Y beta")
hr()
print()
print(f"  BARBELL vs BULLET:")
print(f"  Bear: Barbell {barbell['BEAR']:+.2f}% vs Bullet {bullet['BEAR']:+.2f}%  →  Barbell WINS (30Y convexity hurts less than extra 2Y drag)")
print(f"  Note: Barbell bear is worse ({barbell['BEAR']:+.2f}%) than bullet ({bullet['BEAR']:+.2f}%) — 30Y's large bear loss dominates")
bvb_bear_edge  = bullet["BEAR"] - barbell["BEAR"]
bvb_bull_edge  = barbell["BULL"] - bullet["BULL"]
print(f"  Bear edge (bullet over barbell): {bvb_bear_edge:+.2f}pp  |  Bull edge (barbell over bullet): {bvb_bull_edge:+.2f}pp")
print(f"  Barbell captures more BULL upside (+{bvb_bull_edge:.2f}pp) due to 30Y convexity; bullet is safer in BEAR.")
print()
print(f"  FUTURES OVERLAY:")
print(f"  10% margin → 100% notional 10Y exposure. 90% of capital earns 2Y rate ({YIELDS['2Y']:.2f}%).")
print(f"  Base return: 10% × 10 × {SCENARIO_RETURNS['10Y']['BASE']:.2f}% + 90% × {SCENARIO_RETURNS['2Y']['BASE']:.2f}% = {futures_overlay['BASE']:.2f}%")
print(f"  Bear return: 10% × 10 × {SCENARIO_RETURNS['10Y']['BEAR']:.2f}% + 90% × {SCENARIO_RETURNS['2Y']['BEAR']:.2f}% = {futures_overlay['BEAR']:.2f}%")
print(f"  Capital efficiency: {futures_overlay['BASE']:.2f}% base on 100% of capital (vs bullet {bullet['BASE']:.2f}%)")
print(f"  RISK: leverage amplifies bear loss; futures roll cost ~{0.10:.0%} of position/quarter; not suitable for all mandates.")

# ── ⑥ SUPPLY / DEMAND SCA ────────────────────────────────────────────────────
print()
print("  ⑥ SUPPLY / DEMAND SCA  (Structural Composite Adjustment)")
print(f"  Score scale: −1.0 = strongly bond-bearish (rates up) → +1.0 = strongly bond-bullish (rates down)")
hr()
print(f"  {'Factor':<50}  {'Score':>6}  {'Wt':>4}  {'Contrib':>8}  Commentary")
hr()
for factor, score, weight, comment in SCA_FACTORS:
    contrib = score * weight
    sign = "▼" if score < 0 else "▲"
    print(f"  {sign} {factor:<48}  {score:>+5.2f}  {weight*100:>3.0f}%  {contrib:>+7.3f}  {comment[:52]}")
hr()
print(f"  Net SCA score: {SCA_SCORE:+.4f}  (negative = structural headwinds for bonds outweigh tailwinds)")
print()
print(f"  SUMMARY: Supply-demand balance is structurally bearish for bonds. The $2T/yr issuance")
print(f"  requirement overwhelms private sector absorption capacity, especially with China selling,")
print(f"  Fed in QT mode, and banks SLR-constrained. Only saving grace: recession-hedge optionality")
print(f"  (flight-to-quality flows) and bank demand. Front-end is safer; long-end faces structural headwinds.")

# ── ⑦ COMPOSITE SCORING ──────────────────────────────────────────────────────
print()
print("  ⑦ COMPOSITE SCORING  (Rate Cycle Proxy: 1=BEAR/rates-rise → 4=XBULL/rates-fall)")
hr()
score_labels = {1: "▼ BEAR", 2: "▷ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'Now':>8}  {'Score':>6}  Positions")
hr()
for s in RATE_SIGNALS:
    ths = s["thresholds"]
    sc  = s["score"]
    lbl = score_labels.get(round(sc), f"~{sc:.1f}")
    b   = bar_rate(sc)
    print(f"  {s['name']:<52}  {s['now']:>8}  {sc:>6.1f}  {b}  {lbl}")
    print(f"    → {s['comment'][:75]}")

print()
print(f"  Proxy composite:   {PROXY_COMPOSITE:.3f} / 4.00  (lean BEAR/BASE — rate environment unfavorable for bonds)")
print(f"  Market composite:  {MARKET_COMPOSITE:.2f} / 4.00  (market pricing roughly BASE — flat rates)")
print(f"  SCA adjustment:   {SCA_SCORE:+.4f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print(f"  INTERPRETATION: Adj composite {ADJ_COMPOSITE:.3f} is BELOW market composite {MARKET_COMPOSITE:.2f}.")
print(f"  The model sees more rate pressure than the market prices — suggesting bonds face more")
print(f"  headwinds than current yields imply. However, at current yield LEVELS (4.74% 10Y),")
print(f"  the carry return is attractive enough that the risk/reward for short-to-medium tenors")
print(f"  is positive despite the bearish composite score (hence ACCUMULATE on 10Y, BUY on 5Y).")

# ── ⑧ BEST TENOR RECOMMENDATION ─────────────────────────────────────────────
print()
print("  ⑧ BEST TENOR RECOMMENDATION  &  OVERALL ASSESSMENT")
print("═" * (W + 4))
print()
print(f"  BENCHMARK (10Y):  {signal_full}  |  Ratio B: {ratio_b_str}  |  Yield: {YIELDS['10Y']:.2f}%  |  Total carry: {epp_gap_pct:.2f}%/yr")
print()
print(f"  TENOR HIERARCHY (best to worst risk/reward):")
print(f"    ① 5Y  ◉ BUY       ratio_b {TENOR_RATIO_B['5Y']:.3f}x  — {YIELDS['5Y']:.2f}% yield; only {abs(SCENARIO_RETURNS['5Y']['BEAR']):.2f}% bear loss; {SCENARIO_RETURNS['5Y']['BULL']:.2f}% bull gain")
print(f"    ② 2Y  ◉ BUY       ratio_b {TENOR_RATIO_B['2Y']:.3f}x  — {YIELDS['2Y']:.2f}% yield; POSITIVE return even at +150bps; near-zero duration risk")
print(f"    ③ 10Y ◎ ACCUMULATE ratio_b {TENOR_RATIO_B['10Y']:.3f}x  — {YIELDS['10Y']:.2f}% yield; attractive for income; XBULL convexity payoff")
print(f"    ④ 30Y ◐ WATCHLIST  ratio_b {TENOR_RATIO_B['30Y']:.3f}x  — {YIELDS['30Y']:.2f}% yield; high-conviction recession/deflation trade only")
print()
print(f"  MACRO THESIS:")
print(f"  The structural case for bonds is challenged: $2T annual issuance, China selling, Fed QT,")
print(f"  and a hawkish new Fed Chair (Warsh) create persistent supply pressure on the long end.")
print(f"  30Y at 5.28% (19-yr high) reflects term premium re-rating, not a growth signal.")
print()
print(f"  However, YIELD LEVELS now provide genuine carry. At {YIELDS['5Y']:.2f}%+ (5Y), bonds offer:")
print(f"  (a) Real income above a 2.8% CPI → positive real yield of ~{YIELDS['5Y']-2.8:.2f}%")
print(f"  (b) Recession insurance: 10Y rallies {abs(SCENARIO_RETURNS['10Y']['XBULL']):.1f}%  in XBULL (−200bps flight-to-quality)")
print(f"  (c) Duration pickup vs cash: 2s10s spread {spread_2s10s:.0f}bps rewards holding beyond 2Y")
print()
print(f"  RECOMMENDED POSITIONING:")
print(f"  — Core (60%): 5Y UST — best risk/reward; BUY signal; immune to bear scenario")
print(f"  — Anchor (30%): 2Y UST — duration-free carry; hedge against further rate rise")
print(f"  — Option (10%): 10Y UST — ACCUMULATE; recession convexity; don't overweight")
print(f"  — AVOID: 30Y unhedged — WATCHLIST only; use as barbell leg if paired with 2Y")
print()
print(f"  TRIGGERS TO UPGRADE (10Y/30Y to BUY):")
print(f"  → Recession confirmation (ISM <47, unemployment +1pp) → rates fall −150–200bps")
print(f"  → Fed pivot language / rate cut cycle begins → 10Y yield < 4.0%")
print(f"  → Congressional deficit reduction deal > $1T over 5yr → supply pressure eases")
print()
print(f"  TRIGGERS TO DOWNGRADE (5Y/2Y to WATCHLIST):")
print(f"  → CPI re-acceleration above 3.5% → market prices hikes; yields +75–100bps")
print(f"  → Failed Treasury auction (tail >3bps) → structural demand breakdown")
print(f"  → Warsh signals rate hike in H2 2026")
print()
print(f"  2-year compounded BASE return (10Y): {cons_return_2yr:.1f}%  (collecting coupon + roll each year)")
print(f"  Floor yield (10Y base carry):  {epp_gap_pct:.2f}%/yr  (yield {YIELDS['10Y']:.2f}% + roll {ROLL_YIELDS['10Y']*100:.2f}%)")
print()
print("═" * (W + 4))
print()

# ── EXPORT RESULT DICT ────────────────────────────────────────────────────────
RESULT = {
    "ticker":             TICKER,
    "signal":             signal_full,
    "signal_short":       signal_short,
    "price":              YIELDS["10Y"],      # 10Y yield is the "price" for bonds
    "epp_gap_pct":        epp_gap_pct,        # base carry (yield + roll) = floor yield %
    "ratio_b":            ratio_b_10y,
    "ratio_b_fmt":        ratio_b_str,
    "adj_composite":      ADJ_COMPOSITE,
    "market_composite":   MARKET_COMPOSITE,
    "adj_gap":            ADJ_GAP,
    "valuation":          valuation_label,
    "cons_return_2yr":    cons_return_2yr,    # 2-yr compounded base return, 10Y
    # Bond-specific extras
    "tenors": {
        "2Y": {
            "yield":          YIELDS["2Y"],
            "duration":       DURATIONS["2Y"],
            "roll_yield_pct": round(ROLL_YIELDS["2Y"] * 100, 3),
            "bear_1yr":       SCENARIO_RETURNS["2Y"]["BEAR"],
            "base_1yr":       SCENARIO_RETURNS["2Y"]["BASE"],
            "bull_1yr":       SCENARIO_RETURNS["2Y"]["BULL"],
            "xbull_1yr":      SCENARIO_RETURNS["2Y"]["XBULL"],
            "ratio_b":        TENOR_RATIO_B["2Y"],
            "signal":         TENOR_SIGNALS["2Y"][0],
        },
        "5Y": {
            "yield":          YIELDS["5Y"],
            "duration":       DURATIONS["5Y"],
            "roll_yield_pct": round(ROLL_YIELDS["5Y"] * 100, 3),
            "bear_1yr":       SCENARIO_RETURNS["5Y"]["BEAR"],
            "base_1yr":       SCENARIO_RETURNS["5Y"]["BASE"],
            "bull_1yr":       SCENARIO_RETURNS["5Y"]["BULL"],
            "xbull_1yr":      SCENARIO_RETURNS["5Y"]["XBULL"],
            "ratio_b":        TENOR_RATIO_B["5Y"],
            "signal":         TENOR_SIGNALS["5Y"][0],
        },
        "10Y": {
            "yield":          YIELDS["10Y"],
            "duration":       DURATIONS["10Y"],
            "roll_yield_pct": round(ROLL_YIELDS["10Y"] * 100, 3),
            "bear_1yr":       SCENARIO_RETURNS["10Y"]["BEAR"],
            "base_1yr":       SCENARIO_RETURNS["10Y"]["BASE"],
            "bull_1yr":       SCENARIO_RETURNS["10Y"]["BULL"],
            "xbull_1yr":      SCENARIO_RETURNS["10Y"]["XBULL"],
            "ratio_b":        TENOR_RATIO_B["10Y"],
            "signal":         TENOR_SIGNALS["10Y"][0],
        },
        "30Y": {
            "yield":          YIELDS["30Y"],
            "duration":       DURATIONS["30Y"],
            "roll_yield_pct": round(ROLL_YIELDS["30Y"] * 100, 3),
            "bear_1yr":       SCENARIO_RETURNS["30Y"]["BEAR"],
            "base_1yr":       SCENARIO_RETURNS["30Y"]["BASE"],
            "bull_1yr":       SCENARIO_RETURNS["30Y"]["BULL"],
            "xbull_1yr":      SCENARIO_RETURNS["30Y"]["XBULL"],
            "ratio_b":        TENOR_RATIO_B["30Y"],
            "signal":         TENOR_SIGNALS["30Y"][0],
        },
    },
    "barbell_vs_bullet": {
        "barbell_base":         barbell["BASE"],
        "barbell_bear":         barbell["BEAR"],
        "barbell_bull":         barbell["BULL"],
        "bullet_base":          bullet["BASE"],
        "bullet_bear":          bullet["BEAR"],
        "bullet_bull":          bullet["BULL"],
        "futures_overlay_base": futures_overlay["BASE"],
        "futures_overlay_bear": futures_overlay["BEAR"],
    },
    "supply_demand_score": SCA_SCORE,
    "best_value_tenor":    BEST_TENOR,
}

if __name__ == "__main__":
    pass
