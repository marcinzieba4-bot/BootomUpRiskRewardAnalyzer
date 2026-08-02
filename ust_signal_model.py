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
    "20Y": 5.10,
    "30Y": 5.28,
}

# ── DURATION & CONVEXITY (approximate modified duration) ──────────────────────
DURATIONS  = {"2Y": 1.90, "5Y": 4.50, "10Y": 8.50, "20Y": 13.50, "30Y": 18.00}
CONVEXITY  = {"2Y": 0.05, "5Y": 0.25, "10Y": 0.85, "20Y": 2.20,  "30Y": 4.50}

# ── ROLL YIELD (annualized, per tenor) ────────────────────────────────────────
# Roll yield = Duration × (current yield − interpolated 1yr-shorter yield)
# Interpolated: 1Y≈4.00%, 4Y≈4.40%, 9Y≈4.68%, 19Y≈5.05%, 29Y≈5.25%
ROLL_YIELDS = {
    "2Y":  round(1.90 * (4.29 - 4.00) / 100, 4),
    "5Y":  round(4.50 * (4.46 - 4.40) / 100, 4),
    "10Y": round(8.50 * (4.74 - 4.68) / 100, 4),
    "20Y": round(13.5 * (5.10 - 5.05) / 100, 4),
    "30Y": round(18.0 * (5.28 - 5.25) / 100, 4),
}

# ── SCENARIO YIELD SHIFTS (1-year horizon) ────────────────────────────────────
# BEAR  = +150bps (higher-for-longer; supply shock; inflation resurgence)
# BASE  = flat    (rates on hold; term premium stable)
# BULL  = -100bps (growth slowdown; demand inflows; Fed pivots)
# XBULL = -200bps (recession; flight-to-quality; emergency Fed cuts)
DELTA_YIELD = {"BEAR": +0.0150, "BASE": 0.0, "BULL": -0.0100, "XBULL": -0.0200}

# ── SCENARIO TOTAL RETURNS ────────────────────────────────────────────────────
def _total_return(tenor, scenario):
    y   = YIELDS[tenor] / 100
    r   = ROLL_YIELDS[tenor]
    dur = DURATIONS[tenor]
    cvx = CONVEXITY[tenor]
    dy  = DELTA_YIELD[scenario]
    pc  = -dur * dy
    ca  = 0.5 * cvx * dy ** 2
    return round((y + r + pc + ca) * 100, 2)

SCENARIO_RETURNS = {}
for t in ("2Y", "5Y", "10Y", "20Y", "30Y"):
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

TENOR_RATIO_B = {t: _ratio_b(t) for t in ("2Y", "5Y", "10Y", "20Y", "30Y")}
TENOR_SIGNALS = {t: _bond_signal(TENOR_RATIO_B[t]) for t in TENOR_RATIO_B}

# ── BENCHMARK: 10Y ────────────────────────────────────────────────────────────
ratio_b_10y    = TENOR_RATIO_B["10Y"]
signal_short   = TENOR_SIGNALS["10Y"][0]
signal_full    = TENOR_SIGNALS["10Y"][1]
ratio_b_str    = f"{ratio_b_10y:.3f}x"

# ── STEEPENER ANALYSIS ────────────────────────────────────────────────────────
# Steepener = long the long tenor, short the short tenor (duration-neutral or partly hedged)
# Capital efficiency: steepener doesn't require full capital at the long end.
# Only the net duration exposure demands margin; surplus capital sits at front-end (MM/2Y).
# Roll-down yield on steepener = roll_yield(long) − roll_yield(short)
# Capital cushion = assume 70% allocated at long end, 30% free to earn MM (≈4.10% money-mkt)

MONEY_MKT_RATE = 4.10   # current SOFR/money-market proxy

STEEPENERS = {
    "2/5":  {"short": "2Y", "long": "5Y"},
    "2/10": {"short": "2Y", "long": "10Y"},
    "2/20": {"short": "2Y", "long": "20Y"},
    "2/30": {"short": "2Y", "long": "30Y"},
}

def _steepener_stats(short, long):
    roll_net    = round((ROLL_YIELDS[long] - ROLL_YIELDS[short]) * 100, 3)   # bps roll advantage
    carry_pick  = round(YIELDS[long] - YIELDS[short], 2)                      # yield pickup (bps× / pct)
    # Capital efficiency cushion: 30% of notional freed, earning money-mkt
    capital_cushion = round(0.30 * MONEY_MKT_RATE, 3)                         # ~1.23% on full notional
    # Duration exposure = long_dur − short_dur (for a duration-neutral steepener, notional-weighted)
    dur_exposure = round(DURATIONS[long] - DURATIONS[short], 2)
    # Bear-case loss on steepener if curve flattens -50bps (long rates fall 50bps, short flat)
    # Price gain on long leg = +Dur_long × 0.50%; loss on short leg (short position) = 0 (short flat)
    # Actually for a STEEPENER: you profit if long-end rates RISE (steepen). Bear for steepener = flattening.
    # Flattening scenario: long yields -50bps vs short flat → steepener loses: Dur_long × 0.50%
    flatten_loss = round(DURATIONS[long] * 0.005 * 100, 2)   # 50bps flattening, % loss on long leg
    # Steepening scenario (base/bull): long yields +50bps vs short flat → gain: Dur_long × 0.50%
    steepen_gain = flatten_loss   # symmetric at 50bps
    return {
        "roll_net_pct":    roll_net,
        "carry_pickup_pct": carry_pick,
        "capital_cushion_pct": capital_cushion,
        "dur_exposure":    dur_exposure,
        "flatten_50bp_loss": flatten_loss,
        "steepen_50bp_gain": steepen_gain,
        "total_income":    round(carry_pick + capital_cushion, 2),
    }

STEEPENER_STATS = {
    k: _steepener_stats(v["short"], v["long"])
    for k, v in STEEPENERS.items()
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
        "comment":    "Warsh: hawkish hold; higher-for-longer bias; no pivot signal",
    },
    {
        "name":       "Inflation trajectory / breakevens",
        "weight":     0.25,
        "thresholds": (">4%", "2–3.5%", "~2%", "<1.5%"),
        "now":        "~2.8%",
        "comment":    "CPI moderating but services sticky; breakevens anchored ~2.4%",
        "score":      2.0,
    },
    {
        "name":       "US fiscal deficit / supply pressure",
        "weight":     0.20,
        "thresholds": (">$2T", "$1–2T", "<$1T", "Surplus"),
        "now":        "~$1.9T",
        "comment":    "$1.9T FY2026 deficit; $2T gross issuance; net supply overwhelming",
        "score":      1.5,
    },
    {
        "name":       "Growth outlook / recession probability",
        "weight":     0.15,
        "thresholds": ("Boom", "Steady", "Slowing", "Recession"),
        "now":        "Slowing",
        "comment":    "Growth decelerating; consumer softening; labor market cooling",
        "score":      2.0,
    },
    {
        "name":       "Foreign demand / USD reserve status",
        "weight":     0.10,
        "thresholds": ("Selling", "Flat", "Buying", "Strong inflows"),
        "now":        "Selling",
        "comment":    "China reducing UST; reserve diversification into gold/EM",
        "score":      1.5,
    },
    {
        "name":       "Term premium vs historical norm",
        "weight":     0.05,
        "thresholds": ("Rising fast", "Elevated", "Normal", "Compressed"),
        "now":        "Elevated",
        "comment":    "ACM model term premium ~1.2%; 30Y at 19yr high; above neutral",
        "score":      2.0,
    },
]

assert abs(sum(s["weight"] for s in RATE_SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = round(sum(s["score"] * s["weight"] for s in RATE_SIGNALS), 3)
ADJ_COMPOSITE   = round(PROXY_COMPOSITE + SCA_SCORE, 3)
MARKET_COMPOSITE = 2.10
ADJ_GAP          = round(ADJ_COMPOSITE - MARKET_COMPOSITE, 2)

if ADJ_GAP > 0.20:
    valuation_label = "UNDERVALUED"
elif ADJ_GAP > -0.20:
    valuation_label = "FAIRLY VALUED"
else:
    valuation_label = "OVERVALUED"

cons_return_2yr = round(((1 + SCENARIO_RETURNS["10Y"]["BASE"] / 100) ** 2 - 1) * 100, 1)
epp_gap_pct = round(YIELDS["10Y"] + ROLL_YIELDS["10Y"] * 100, 2)
BEST_TENOR = "5Y"

# ─────────────────────────────────────────────────────────────────────────────
#  OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
W = 76

def hr(): print("  " + "─" * W)
def bar_rate(score):
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
print(f"  Curve fully un-inverted (2s10s +{spread_2s10s:.0f}bps). Steepening driven by long-end supply")
print(f"  pressure, NOT a Fed pivot. 30Y at 5.28% reflects term premium re-rating. 2Y anchored")
print(f"  at 4.29% = market pricing Fed on hold through 2026. 2s30s {spread_2s30s:.0f}bps = bond vigilante premium.")

# ── ② ROLL YIELD SUMMARY ─────────────────────────────────────────────────────
print()
print("  ② ROLL YIELD SUMMARY  (annualized; price gain as bond rolls down the curve)")
hr()
print(f"  {'Tenor':<6}  {'Yield':>8}  {'Roll Yield':>11}  {'Total Carry':>12}  Note")
hr()
for t in ("2Y", "5Y", "10Y", "20Y", "30Y"):
    y = YIELDS[t]; r = ROLL_YIELDS[t]
    flag = "  ← best carry+roll" if t == "5Y" else ""
    print(f"  {t:<6}  {y:>7.2f}%  {r*100:>10.2f}%  {y + r*100:>11.2f}%{flag}")
hr()
print(f"  2Y roll highest (steep short-end); 5Y flat slope = thin roll; 10Y best overall carry.")

# ── ③ SCENARIO TOTAL RETURNS ─────────────────────────────────────────────────
print()
print("  ③ SCENARIO TOTAL RETURNS  (1-year horizon, %)")
print(f"  BEAR=+150bps  |  BASE=flat  |  BULL=−100bps  |  XBULL=−200bps")
hr()
print(f"  {'Tenor':<8}  {'Dur':>5}  {'BEAR':>8}  {'BASE':>8}  {'BULL':>8}  {'XBULL':>8}  {'Ratio B':>9}  Signal")
hr()
for t in ("2Y", "5Y", "10Y", "20Y", "30Y"):
    sr  = SCENARIO_RETURNS[t]
    rb  = TENOR_RATIO_B[t]
    sig = TENOR_SIGNALS[t][1]
    rb_s = f"{rb:.3f}x" if rb != float("inf") else "N/A"
    flag = " ◄" if t == BEST_TENOR else ""
    print(f"  {t:<8}  {DURATIONS[t]:>5.2f}  {sr['BEAR']:>+7.2f}%  {sr['BASE']:>+7.2f}%  {sr['BULL']:>+7.2f}%  {sr['XBULL']:>+7.2f}%  {rb_s:>9}  {sig}{flag}")
hr()

# ── ④ STEEPENER ANALYSIS ─────────────────────────────────────────────────────
print()
print("  ④ STEEPENER ANALYSIS  (long long-tenor / short 2Y; profit if curve steepens further)")
print(f"  Capital efficiency: ~30% freed capital earns money-mkt ({MONEY_MKT_RATE:.2f}%), boosting all-in income.")
hr()
print(f"  {'Trade':<6}  {'Carry pickup':>13}  {'Roll-down adv':>14}  {'MM cushion':>11}  {'All-in income':>14}  {'Dur exposure':>13}  {'Flat -50bp loss':>16}")
hr()
for trade, stats in STEEPENER_STATS.items():
    lt = STEEPENERS[trade]["long"]
    print(
        f"  {trade:<6}  "
        f"{stats['carry_pickup_pct']:>+12.2f}%  "
        f"{stats['roll_net_pct']:>+13.3f}%  "
        f"{stats['capital_cushion_pct']:>+10.3f}%  "
        f"{stats['total_income']:>+13.2f}%  "
        f"{stats['dur_exposure']:>12.2f}yr  "
        f"{stats['flatten_50bp_loss']:>+15.2f}%"
    )
hr()
print()
print(f"  STEEPENER LOGIC:")
print(f"  In the current environment, the curve is steepening via long-end supply pressure, not")
print(f"  a Fed pivot. This means steepeners are valid if you believe: (a) supply stays heavy,")
print(f"  (b) term premium continues re-rating, or (c) a recession eventually triggers a bull")
print(f"  steepener (Fed cuts short-end faster than long-end falls).")
print()
print(f"  2/5  steepener: modest carry pickup ({STEEPENER_STATS['2/5']['carry_pickup_pct']:.2f}%), thin roll advantage. Low duration risk.")
print(f"        Best for: tactical play on near-term Fed hold + mild taper of front-end support.")
print(f"  2/10 steepener: {STEEPENER_STATS['2/10']['carry_pickup_pct']:.2f}% carry pickup; 30% freed capital earns {MONEY_MKT_RATE:.2f}% MM → total ~{STEEPENER_STATS['2/10']['total_income']:.2f}%.")
print(f"        Best for: core steepener trade; conviction on no near-term 10Y rally (no BULL flat).")
print(f"  2/20 steepener: {STEEPENER_STATS['2/20']['carry_pickup_pct']:.2f}% carry; high duration ({STEEPENER_STATS['2/20']['dur_exposure']:.1f}yr). Risk: 50bps flattening = {STEEPENER_STATS['2/20']['flatten_50bp_loss']:.2f}% loss.")
print(f"        Best for: structural supply-pressure thesis; requires high-conviction macro view.")
print(f"  2/30 steepener: highest carry ({STEEPENER_STATS['2/30']['carry_pickup_pct']:.2f}%) but {STEEPENER_STATS['2/30']['dur_exposure']:.1f}yr duration. All-in ~{STEEPENER_STATS['2/30']['total_income']:.2f}%.")
print(f"        Best for: recession hedge overlay — in XBULL the long leg rallies massively.")
print()
print(f"  CAPITAL EFFICIENCY CUSHION:")
print(f"  Unlike outright longs, steepeners free up capital at the short leg (typically margined).")
print(f"  Surplus {MONEY_MKT_RATE:.2f}% money-mkt return adds {0.30*MONEY_MKT_RATE:.2f}% to all-in income — a meaningful buffer")
print(f"  that outright bond positions don't capture. This makes steepeners attractive even when")
print(f"  the pure yield pickup looks modest (e.g. 2/5 at only {STEEPENER_STATS['2/5']['carry_pickup_pct']:.2f}%).")

# ── ⑤ RATE CYCLE COMMENTARY ──────────────────────────────────────────────────
print()
print("  ⑤ RATE CYCLE — CURRENT ENVIRONMENT  (does it make sense to play the cycle?)")
hr()
print()
print(f"  SHORT ANSWER: Yes — but tactically, not directionally. Here's why:")
print()
print(f"  CASE FOR PLAYING THE CYCLE (bull bond trade):")
print(f"  · Growth is visibly slowing; consumer spending and labor market softening")
print(f"  · At 4.74% (10Y), real yield is ~+2.0% above current CPI — historically high; pricing pain")
print(f"  · A recession would trigger emergency rate cuts; 10Y/30Y could rally 100–200bps")
print(f"  · 1/3 of US Treasury debt matures 2026 — if refunding stumbles, Fed forced to pivot")
print()
print(f"  CASE AGAINST (bear bond / avoid duration):")
print(f"  · Kevin Warsh is explicitly hawkish; no pivot signal; market wrongly priced 3 cuts YTD")
print(f"  · $2T/yr supply overwhelms demand; term premium still re-rating higher")
print(f"  · China reducing UST; foreign marginal buyer fading; Eurodollar recycling slowing")
print(f"  · Tariff-driven inflation keeps CPI sticky above 2% — gives Warsh cover to hold")
print()
print(f"  VERDICT: Rate cycle is NOT a clean play — too many cross-currents.")
print(f"  → Prefer CARRY over DURATION: stay 5Y/2Y; earn {YIELDS['5Y']:.2f}%+ with limited bear exposure.")
print(f"  → Use STEEPENERS (2/10, 2/20) rather than outright longs to express a bear-steepen view.")
print(f"  → Only go outright long 10Y/30Y if recession materialises (ISM <47, unemployment +1pp).")

# ── ⑥ SUPPLY / DEMAND SCA ────────────────────────────────────────────────────
print()
print("  ⑥ SUPPLY / DEMAND SCA  (Structural Composite Adjustment)")
print(f"  Score scale: −1.0 = strongly bond-bearish (rates up) → +1.0 = bond-bullish (rates down)")
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
print(f"  IMMUNE SEGMENTS — parts of the curve shielded from supply/demand headwinds:")
print()
print(f"  · 2Y / T-Bills: Nearly immune. Set by Fed funds expectations, not supply/demand.")
print(f"    Even with $2T issuance, short-end stays anchored as long as Fed holds rates.")
print(f"    Banks and MMFs have uncapped appetite for T-bills; auction failure risk = ~0.")
print()
print(f"  · TIPS (5Y/10Y): Inflation-linked; attractive if CPI re-accelerates above 2.8%.")
print(f"    Real yield at ~+2.0% (10Y TIPS ~2.0%) is historically high → floor for real rates.")
print(f"    Supply headwind applies but partially offset by pension/sovereign demand for real assets.")
print()
print(f"  · 5Y nominal: Caught between Fed anchor and long-end supply. Thin roll yield,")
print(f"    but ratio_b {TENOR_RATIO_B['5Y']:.3f}x (BUY). Benefits from: (a) carry above inflation,")
print(f"    (b) low duration risk in bear scenario, (c) rolls down toward 2Y anchor over time.")
print()
print(f"  · 30Y (supply-sensitive): MOST exposed to auction dynamics, China selling, and")
print(f"    term premium re-rating. Only buy 30Y as a recession/deflation hedge, not for carry.")

# ── ⑦ COMPOSITE SCORING ──────────────────────────────────────────────────────
print()
print("  ⑦ COMPOSITE SCORING  (Rate Cycle Proxy: 1=BEAR/rates-rise → 4=XBULL/rates-fall)")
hr()
score_labels = {1: "▼ BEAR", 2: "▷ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'Now':>8}  {'Score':>6}  Bar")
hr()
for s in RATE_SIGNALS:
    sc  = s["score"]
    lbl = score_labels.get(round(sc), f"~{sc:.1f}")
    b   = bar_rate(sc)
    print(f"  {s['name']:<52}  {s['now']:>8}  {sc:>6.1f}  {b}  {lbl}")
    print(f"    → {s['comment'][:75]}")
print()
print(f"  Proxy composite:   {PROXY_COMPOSITE:.3f} / 4.00  (lean BEAR/BASE)")
print(f"  Market composite:  {MARKET_COMPOSITE:.2f} / 4.00  (market pricing roughly BASE — flat rates)")
print(f"  SCA adjustment:   {SCA_SCORE:+.4f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print(f"  Model sees more rate pressure than market prices. But at current YIELD LEVELS")
print(f"  (4.74% 10Y), carry is attractive enough → ACCUMULATE on 10Y, BUY on 5Y/2Y.")

# ── ⑧ ASSESSMENT ─────────────────────────────────────────────────────────────
print()
print("  ⑧ OVERALL ASSESSMENT")
print("═" * (W + 4))
print()
print(f"  BENCHMARK (10Y):  {signal_full}  |  Ratio B: {ratio_b_str}  |  Yield: {YIELDS['10Y']:.2f}%  |  Carry: {epp_gap_pct:.2f}%/yr")
print()
print(f"  TENOR HIERARCHY (best to worst risk/reward):")
print(f"    ① 2Y  ◉ BUY       rb {TENOR_RATIO_B['2Y']:.3f}x — positive return even at +150bps; Fed-anchored")
print(f"    ② 5Y  ◉ BUY       rb {TENOR_RATIO_B['5Y']:.3f}x — {YIELDS['5Y']:.2f}% yield; best risk/reward; bear-resistant")
print(f"    ③ 10Y ◎ ACCUM     rb {TENOR_RATIO_B['10Y']:.3f}x — {YIELDS['10Y']:.2f}% yield; XBULL convexity payoff {SCENARIO_RETURNS['10Y']['XBULL']:.1f}%")
print(f"    ④ 20Y ◐ WATCH     rb {TENOR_RATIO_B['20Y']:.3f}x — supply headwind; steepener leg only")
print(f"    ⑤ 30Y ◐ WATCH     rb {TENOR_RATIO_B['30Y']:.3f}x — recession hedge only; not for carry")
print()
print(f"  PREFERRED EXPRESSION: 2/10 steepener or outright 5Y.")
print(f"  2-year compounded BASE return (10Y): {cons_return_2yr:.1f}%")
print(f"  Floor yield (10Y base carry): {epp_gap_pct:.2f}%/yr")
print()
print("═" * (W + 4))
print()

# ── EXPORT RESULT DICT ────────────────────────────────────────────────────────
RESULT = {
    "ticker":             TICKER,
    "signal":             signal_full,
    "signal_short":       signal_short,
    "price":              YIELDS["10Y"],
    "epp_gap_pct":        epp_gap_pct,
    "ratio_b":            ratio_b_10y,
    "ratio_b_fmt":        ratio_b_str,
    "adj_composite":      ADJ_COMPOSITE,
    "market_composite":   MARKET_COMPOSITE,
    "adj_gap":            ADJ_GAP,
    "valuation":          valuation_label,
    "cons_return_2yr":    cons_return_2yr,
    "tenors": {
        t: {
            "yield":          YIELDS[t],
            "duration":       DURATIONS[t],
            "roll_yield_pct": round(ROLL_YIELDS[t] * 100, 3),
            "bear_1yr":       SCENARIO_RETURNS[t]["BEAR"],
            "base_1yr":       SCENARIO_RETURNS[t]["BASE"],
            "bull_1yr":       SCENARIO_RETURNS[t]["BULL"],
            "xbull_1yr":      SCENARIO_RETURNS[t]["XBULL"],
            "ratio_b":        TENOR_RATIO_B[t],
            "signal":         TENOR_SIGNALS[t][0],
        }
        for t in ("2Y", "5Y", "10Y", "20Y", "30Y")
    },
    "steepeners":         STEEPENER_STATS,
    "supply_demand_score": SCA_SCORE,
    "best_value_tenor":   BEST_TENOR,
}

if __name__ == "__main__":
    pass
