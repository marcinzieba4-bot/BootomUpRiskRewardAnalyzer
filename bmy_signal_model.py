"""
BMY  ·  Bristol Myers Squibb Co.  ·  NYSE: BMY
Bottom-up signal model  ·  Pharma / Patent Cliff (Eliquis/Revlimid) / Cobenfy (KarXT) Launch / Cell Therapy / AZN Merger Speculation
Date: 2026-08-04
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "BMY"
COMPANY       = "Bristol Myers Squibb Co."
SECTOR        = "Pharma · Patent Cliff (Eliquis/Revlimid) · Cobenfy (KarXT) · Cell Therapy (Breyanzi/Abecma) · NYSE: BMY"
CURRENT_PRICE = 65.47       # USD; close 2026-08-03 — near 52-week highs, boosted by unconfirmed M&A speculation
VOL_52W_LOW   = 42.52       # USD
VOL_52W_HIGH  = 68.10       # USD
SHARES_OUT_M  = 2_040.0     # millions
ANNUAL_DIV    = 2.52        # $/share; ~3.8% yield at current price

# ── ⚠ ASTRAZENECA MERGER SPECULATION — READ BEFORE INTERPRETING THIS MODEL ────
# On Aug 2, 2026, FT/Bloomberg/Reuters reported AstraZeneca-BMY merger talks — a potential
# >$400B mega-deal. AZN fell ~7%, BMY jumped ~6% premarket. NEITHER COMPANY HAS CONFIRMED
# THIS. There is no definitive agreement, no deal price, no terms. This model is built
# entirely on BMY's STANDALONE fundamentals — it does NOT price in any takeover premium.
# If the talks don't materialize into a deal, a meaningful part of BMY's recent ~6% gain
# could reverse. Treat the mechanical signal below as a read on the standalone business,
# not a merger-arb call — unlike ZAB's Couche-Tard situation, there is no signed deal here
# to model an arb spread against.
AZN_MERGER_TALKS_REPORTED  = "2026-08-02"
AZN_MERGER_DEAL_VALUE_EST  = ">$400B (unconfirmed, no terms disclosed)"
BMY_PREMARKET_MOVE_ON_NEWS_PCT = 6  # approximate

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# Q2 2026 actual (reported ~Jul 30): revenue $12.97B; adj EPS $2.04 (beat). Growth Portfolio
# (Camzyos, Cobenfy, Breyanzi, Reblozyl, Opdualag, Opdivo Qvantig) +14-15% to $7.6B/qtr, now
# ~59% of total revenue. Eliquis +21% to $4.5B/qtr — STILL GROWING, the patent-cliff has NOT
# yet started biting. Camzyos $416M/qtr (+59% YoY) is a standout. Cobenfy +81% to just
# $63M/qtr — genuinely encouraging growth rate, but a much smaller absolute run-rate than
# earlier blockbuster hopes suggested. FY2026 guidance raised: revenue $49.0-50.0B, non-GAAP
# EPS $6.75-7.00.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Eliquis (anticoagulant)",          17.5, 12.0, 19.0, "Still growing +21% YoY in Q2 — the patent cliff has NOT yet started biting, though US LOE risk remains a multi-year overhang"),
    ("Revlimid (multiple myeloma)",       3.0,  1.2,  3.5, "Generic erosion continuing per the existing settlement schedule; legacy cash-cow declining toward minimal base"),
    ("Growth Portfolio - Cell Therapy (Breyanzi/Abecma)", 3.5, 2.8, 5.5, "Breyanzi label expansions and Abecma CAR-T scaling"),
    ("Growth Portfolio - Camzyos/Reblozyl/Opdualag/Qvantig", 12.0, 9.5, 15.0, "Camzyos $416M/qtr (+59% YoY) is the standout; broader Growth Portfolio now ~59% of total revenue"),
    ("Cobenfy (KarXT - schizophrenia/psychiatric)", 0.3, 0.15, 2.5, "+81% YoY but only $63M/qtr — genuinely fast growth off a smaller-than-hoped base; still the key long-term swing factor"),
    ("Other Legacy/Mature Brands",       13.2, 10.5, 14.0, "Diversified mature brands; gradual decline"),
]

# Net-margin-based bridge
NET_MARGIN_CURR = 0.2833   # FY2026E; reconciles to raised guidance midpoint
NET_MARGIN_BEAR = 0.2539   # BEAR: Eliquis cliff finally hits, Cobenfy stays small
NET_MARGIN_BULL = 0.3086   # BULL: Cobenfy scales, cliff proves manageable, cost cuts land

# ── ELIQUIS CLIFF TIMING / COBENFY RAMP TRACKER (the BMY-specific angle) ──────
Q2_2026_REVENUE_B          = 12.97   # $B, Q2 2026 actual reported revenue
Q2_2026_ADJ_EPS            = 2.04    # $ adjusted EPS, Q2 2026 (beat)
ELIQUIS_Q2_GROWTH_PCT      = 21      # % YoY, Q2 2026 — still growing
GROWTH_PORTFOLIO_PCT_OF_REV = 59     # % of total revenue, Growth Portfolio basket
CAMZYOS_Q2_GROWTH_PCT      = 59      # % YoY, Q2 2026
COBENFY_Q2_REVENUE_M       = 63      # $M, Q2 2026 Cobenfy revenue
COBENFY_Q2_GROWTH_PCT      = 81      # % YoY, Q2 2026
FY2026_GUIDANCE_EPS_RANGE  = "6.75-7.00"  # $ non-GAAP, raised FY2026 guidance
STOCK_MOVE_FROM_JUNE_LOW_PCT = round((CURRENT_PRICE - 52.00) / 52.00 * 100, 1)  # move since last refresh

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 6.875       # FY2026E non-GAAP EPS (raised guidance $6.75-7.00; midpoint)
PE_PESSIMISTIC = 8.0         # pessimistic P/E: below the current ~9.5× multiple; deep cliff-discount floor
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (4.50, 8,   36, "Eliquis cliff finally hits hard (generic entry accelerates); Cobenfy launch stays well below blockbuster scale; restructuring savings don't materialize; EPS $4.50 → 8× = $36"),
    "BASE":  (6.875, 9.52, 65, "Eliquis continues growing near-term before the cliff arrives on the known 2026-2028 schedule; Cobenfy keeps growing fast off a small base; Growth Portfolio offsets Revlimid erosion; EPS $6.875 → 9.5× = $65"),
    "BULL":  (9.00, 12,  108, "Eliquis cliff proves more gradual than feared; Cobenfy accelerates toward $500M+ run-rate; Camzyos and cell therapy keep compounding; cost cuts drive margin expansion; EPS $9.00 → 12× = $108"),
    "XBULL": (11.00, 15, 165, "Cobenfy becomes a top-tier psychiatric pipeline platform across multiple indications, fully offsetting the Eliquis/Revlimid cliff; multiple re-rates toward growth-pharma peers; EPS $11.00 → 15× = $165"),
}

# ── SOFTMAX PROBABILITY FUNCTION ─────────────────────────────────────────────
CENTERS = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
T = 0.60

def softmax_probs(c):
    raw = {s: math.exp(-abs(c - CENTERS[s]) / T) for s in CENTERS}
    tot = sum(raw.values())
    return {s: raw[s] / tot for s in raw}

def expected_value(c):
    p = softmax_probs(c)
    return sum(p[s] * SCENARIOS[s][2] for s in SCENARIOS)

def back_solve_market_composite(price, tol=0.001):
    target = price * (1.15 ** 2)
    lo, hi = 1.0, 4.0
    for _ in range(80):
        m = (lo + hi) / 2
        if expected_value(m) < target:
            lo = m
        else:
            hi = m
    return round((lo + hi) / 2, 2)

# ── 6 PROXY SIGNALS ───────────────────────────────────────────────────────────
# Scores: 1=BEAR  2=BASE  3=BULL  4=XBULL
SIGNALS = [
    {
        "name":       "Eliquis/Revlimid patent-cliff erosion pace",
        "weight":     0.25,
        "thresholds": ("erosion>plan", "in line with plan", "erosion slower than plan", "minimal erosion to date"),
        "now":        "Eliquis +21% YoY, still growing",
        "score":      3,
        "comment":    "Eliquis is STILL GROWING (+21% YoY in Q2) — the cliff has genuinely not started biting yet, better than the market's cliff-fear framing implies",
    },
    {
        "name":       "Cobenfy (KarXT) launch trajectory - schizophrenia",
        "weight":     0.25,
        "thresholds": ("<$200M run-rate", "≥$500M", "≥$1B", "≥$2B"),
        "now":        "~$250M run-rate",
        "score":      1,
        "comment":    "$63M/qtr (+81% YoY) annualizes to roughly $250M — genuinely fast growth, but a materially smaller base than the $500-700M run-rate earlier hoped for",
    },
    {
        "name":       "Cobenfy pipeline expansion (Alzheimer's psychosis/bipolar/MDD)",
        "weight":     0.15,
        "thresholds": ("no readouts", "1 positive readout", "2 positive readouts", "3+ positive readouts/filings"),
        "now":        "1 readout pending",
        "score":      2,
        "comment":    "Phase 3 readouts in Alzheimer's-related psychosis and adjunctive MDD still pending; the broader psychiatric platform thesis remains unproven at scale",
    },
    {
        "name":       "Growth Portfolio (Camzyos/Breyanzi/Reblozyl/Opdualag/Qvantig)",
        "weight":     0.15,
        "thresholds": ("<8%", "≥12%", "≥18%", "≥25%"),
        "now":        "+14-15%, now 59% of revenue",
        "score":      3,
        "comment":    "Camzyos alone +59% YoY; the Growth Portfolio basket collectively is now the majority of BMY's revenue — real, quantified diversification progress",
    },
    {
        "name":       "Cost-cutting/restructuring program execution",
        "weight":     0.10,
        "thresholds": ("behind plan", "on track", "ahead of plan", "exceeding + further cuts announced"),
        "now":        "on track",
        "score":      2,
        "comment":    "Multi-billion dollar cost-reduction program tracking on schedule; helps cushion EPS during the cliff transition",
    },
    {
        "name":       "Balance sheet deleveraging (post Karuna/RayzeBio/Mirati M&A)",
        "weight":     0.10,
        "thresholds": ("leverage rising", "stable, elevated (~3x+)", "deleveraging toward ~2.5x", "back below ~2x"),
        "now":        "stable, elevated (~3x)",
        "score":      2,
        "comment":    "Net debt remains elevated following Karuna/RayzeBio/Mirati acquisitions; the dividend raise (to $2.52) is a modest positive capital-return signal regardless",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("-", "Eliquis/Revlimid patent cliff — still a real, multi-year overhang through 2028, even though Q2 shows no erosion yet", -0.5, 0.25),
    ("+", "Cobenfy optionality — the broader psychiatric pipeline thesis is real, though the Q2 print was smaller than earlier hoped", +0.3, 0.20),
    ("-", "High leverage from M&A (Karuna/RayzeBio/Mirati) — constrains capital flexibility during the cliff transition", -0.3, 0.15),
    ("+", "High dividend yield (~3.8% at current price) — provides a meaningful total-return floor", +0.4, 0.15),
    ("+", "Growth Portfolio now the majority of revenue (59%) — real, quantified diversification away from single-product concentration", +0.5, 0.10),
    ("+", "Cost-restructuring program on track — targeted savings provide EPS cushion independent of revenue trajectory", +0.3, 0.10),
]
SCA = sum(score * weight for _, _, score, weight in SCA_FACTORS)
ADJ_COMPOSITE = round(PROXY_COMPOSITE + SCA, 3)

MARKET_COMPOSITE = back_solve_market_composite(CURRENT_PRICE)
ADJ_GAP = round(ADJ_COMPOSITE - MARKET_COMPOSITE, 2)

if ADJ_GAP > 0.20:
    valuation_label = "UNDERVALUED"
elif ADJ_GAP > -0.20:
    valuation_label = "FAIRLY VALUED"
else:
    valuation_label = "OVERVALUED"

# ── RATIO B ───────────────────────────────────────────────────────────────────
bear_price   = SCENARIOS["BEAR"][2]
bull_price   = SCENARIOS["BULL"][2]
downside_pct = (CURRENT_PRICE - bear_price) / CURRENT_PRICE
upside_pct   = (bull_price - CURRENT_PRICE) / CURRENT_PRICE
ratio_b      = round(downside_pct / upside_pct, 2) if upside_pct > 0 else float("inf")

if ratio_b != float("inf") and ratio_b < 0.75:
    signal_short, signal_full = "BUY",       "◉ BUY"
elif ratio_b != float("inf") and ratio_b < 1.10:
    signal_short, signal_full = "ACCUMULATE","◎ ACCUMULATE"
elif ratio_b != float("inf") and ratio_b < 1.75:
    signal_short, signal_full = "WATCHLIST", "◐ WATCHLIST"
else:
    signal_short, signal_full = "AVOID",     "✕ AVOID"

ratio_b_str = f"{ratio_b:.2f}x" if ratio_b != float("inf") else "N/A"

# ── CONSERVATIVE GROWTH (2-yr) ────────────────────────────────────────────────
CONS_EPS_2YR  = 6.20    # FY2028E conservative: a genuine cliff-driven dip below FY2026E as Eliquis LOE progresses
CONS_PE_2YR   = 9       # roughly flat from the current ~9.5×
cons_equity   = CONS_EPS_2YR * CONS_PE_2YR
cons_divs     = ANNUAL_DIV * 2
cons_total    = cons_equity + cons_divs
cons_return   = round((cons_total - CURRENT_PRICE) / CURRENT_PRICE * 100, 1)
cons_annual   = round(cons_return / 2, 1)

# ─────────────────────────────────────────────────────────────────────────────
#  OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
W = 72

def hr(): print("  " + "─" * W)
def bar(score):
    return "█" * score + "░" * (4 - score)

print()
print("═" * (W + 4))
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Patent Cliff (Eliquis/Revlimid) / Cobenfy Launch / Cell Therapy")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

print()
print("  ⚠ ASTRAZENECA MERGER SPECULATION — read before interpreting this model")
hr()
print(f"  Talks reported:        {AZN_MERGER_TALKS_REPORTED}  ({AZN_MERGER_DEAL_VALUE_EST})")
print(f"  BMY premarket move:    +{BMY_PREMARKET_MOVE_ON_NEWS_PCT}% on the news (approx.)")
print(f"  This model is built ENTIRELY on BMY's standalone fundamentals — it does NOT price in")
print(f"  any takeover premium. Neither company has confirmed a deal; there are no terms, no price.")
print(f"  If talks don't materialize, part of the recent gain could reverse. Unlike a signed deal")
print(f"  (e.g. ZAB/Couche-Tard), there is no arb spread to model here — just headline risk both ways.")

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<48}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<48}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<48}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  Q2 2026 actual: revenue ${Q2_2026_REVENUE_B:.2f}B, adj EPS ${Q2_2026_ADJ_EPS:.2f} (beat)")
print()

# EPS bridge (net-margin based)
shares    = SHARES_OUT_M / 1000
curr_net  = curr_total * NET_MARGIN_CURR
curr_eps  = round(curr_net / shares, 2)

bull_net     = bull_total * NET_MARGIN_BULL
bull_eps_imp = round(bull_net / shares, 2)

bear_net     = bear_total * NET_MARGIN_BEAR
bear_eps_imp = round(bear_net / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {NET_MARGIN_CURR*100:.2f}% net margin")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.3f}/share  (guidance ${EPS_FY2026E:.3f} midpoint  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {NET_MARGIN_BULL*100:.2f}% net margin")
print(f"  ÷ {shares:.3f}B shares  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {NET_MARGIN_BEAR*100:.2f}% net margin (cliff finally hits + Cobenfy stays small)")
print(f"  ÷ {shares:.3f}B shares  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# ELIQUIS/COBENFY TRACKER
print()
print(f"  ELIQUIS CLIFF TIMING / COBENFY RAMP TRACKER  (the BMY-specific angle):")
print(f"  Q2 2026 revenue / adj EPS:                   ${Q2_2026_REVENUE_B:.2f}B / ${Q2_2026_ADJ_EPS:.2f}")
print(f"  Eliquis Q2 growth:                             +{ELIQUIS_Q2_GROWTH_PCT}% YoY  (still growing, not yet in cliff decline)")
print(f"  Growth Portfolio % of revenue:                  {GROWTH_PORTFOLIO_PCT_OF_REV}%")
print(f"  Camzyos Q2 growth:                              +{CAMZYOS_Q2_GROWTH_PCT}% YoY")
print(f"  Cobenfy Q2 revenue / growth:                    ${COBENFY_Q2_REVENUE_M}M  (+{COBENFY_Q2_GROWTH_PCT}% YoY)")
print(f"  Stock move since last refresh (Jun 10):        +{STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}%")
print()
print(f"  The honest read: Eliquis hasn't started declining yet (+21% YoY), which is better than the")
print(f"  market's cliff-fear framing often implies. But Cobenfy — the stock's primary long-term offset")
print(f"  thesis — is growing fast off a genuinely small base ($63M/qtr), well below earlier blockbuster")
print(f"  hopes. The Growth Portfolio overall (59% of revenue) is the real diversification story right now.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = 1.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at {NET_MARGIN_CURR*100:.1f}% margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*9.52:.2f}/share at 9.5× P/E")
print(f"  1pp net margin expansion (mix/scale):        +${curr_total*0.01/shares:.3f}/EPS  = +${curr_total*0.01/shares*9.52:.2f}/share at 9.5× P/E")
print(f"  Every 1 turn of P/E:                          ±${EPS_FY2026E:.3f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Patent cliff erosion / Cobenfy launch & pipeline / Growth portfolio / Restructuring)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>5}  {'BASE':>5}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>6}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>5}  {ths[1]:>5}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>6}  {lbl}  {b}")
    print(f"    {s['comment']}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15% hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:72]:<72}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<52}  {'Current':>16}  {'Bear val':>9}  Trigger")
hr()
bear_triggers = [
    ("Eliquis revenue trajectory",         "+21% YoY", "double-digit decline", "US generic entry arrives earlier/faster than expected, cratering Eliquis"),
    ("Cobenfy launch run-rate",            "~$250M",   "<$200M",  "Schizophrenia uptake stalls on access/formulary hurdles or tolerability concerns"),
    ("Cobenfy pipeline readouts",          "1 pending","0 positive", "Alzheimer's psychosis / bipolar / MDD trials fail or show weak efficacy"),
    ("Growth portfolio growth",            "+14-15%",  "<8%",     "Cell therapy competitive pressure intensifies; Camzyos uptake slows"),
    ("Restructuring savings realization",  "on track", "behind plan", "Cost-cutting program slips, EPS cushion fails to materialize"),
    ("Net margin",                         "28.3%",    "<24%",    "Free cash flow diverted, leverage rises further, margin compresses"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>16}  {bear_v:>9}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Eliquis's growth reverses sharply as generic entry finally arrives, while")
print(f"  Cobenfy's launch stalls even further below blockbuster expectations and the Alzheimer's-")
print(f"  psychosis/bipolar/MDD pipeline reads out negatively. EPS falls to ~$4.50 at an 8× trough P/E.")
print(f"  Note: ${bear_price} is NOT permanent impairment — the ~3.8% dividend yield and Growth Portfolio")
print(f"  cash flows (Camzyos/Breyanzi/Reblozyl) provide a floor.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E EPS estimate:           ${EPS_FY2026E:.3f}  (raised guidance midpoint)")
print(f"  Pessimistic P/E:                 {PE_PESSIMISTIC:.0f}×  (below the current ~9.5× multiple; deep cliff-discount floor)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  BMY trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS ${EPS_FY2026E:.3f} — still a deep discount versus pharma")
print(f"  peers despite the recent rally, reflecting the Eliquis/Revlimid cliff overhang even though Q2")
print(f"  showed no erosion yet. Some of the current price reflects unconfirmed AZN merger speculation")
print(f"  rather than pure fundamentals — a real caveat on how much to lean on the current multiple.")
print(f"  At 10× mid-cycle P/E: ${EPS_FY2026E:.3f} × 10 = ${EPS_FY2026E*10:.0f}  — {(EPS_FY2026E*10/CURRENT_PRICE-1)*100:+.0f}% vs current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: a genuine cliff-driven EPS dip as Eliquis LOE progresses)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (BELOW FY2026E — Eliquis LOE genuinely bites by then, even in a non-bear case)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (roughly flat from the current ~9.5×)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST NUANCE: unlike most tickers in this batch, BMY's conservative FY2028E case is")
print(f"  BELOW its FY2026E base — because the Eliquis cliff is a known, dated event that even a")
print(f"  non-bear scenario should expect to actually arrive by then. The mechanical BEAR/BULL 2yr")
print(f"  window looks attractively priced mainly because the cliff hasn't started yet.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.26
beta        = 0.65
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock is up {STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}% since the last refresh (Jun 10); part of the recent move is unconfirmed AZN merger speculation")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; cliff/Cobenfy/M&A-headline-driven swings)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (moderately defensive; below-market beta but idiosyncratic risk elevated by merger headlines)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe; cliff-acceleration + Cobenfy-underwhelm + merger-talk-reversal scenario)")
print(f"  → AZN merger talk developments (confirm/deny/walk away) are THE KEY near-term headline risk in either direction.")
print(f"  → Eliquis quarterly growth trend and Cobenfy's run-rate are the KEY fundamental signals.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $58  |  Trim above $68")

# ─── ⑦ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print()
print("  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
hr()
probs_mkt = softmax_probs(MARKET_COMPOSITE)
print(f"  {'Scenario':<10}  {'Price':>7}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>7}  Description")
hr()
for s in ["BEAR","BASE","BULL","XBULL"]:
    pp  = probs_proxy[s] * 100
    pm  = probs_mkt[s]   * 100
    gap = pp - pm
    pr  = SCENARIOS[s][2]
    desc = SCENARIOS[s][3][:46]
    print(f"  {s:<10}  ${pr:>6}  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): ${ev_adj:.0f}  /  Proxy EV: ${ev_prx:.0f}  /  Market EV: ${ev_mkt:.0f}  /  Current: ${CURRENT_PRICE:.0f}")
hr()
print(f"  Downside  (→ Bear ${bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull ${bull_price}):  {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b_str}")
print(f"  Signal    :  {signal_full}")
print()
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is")
print(f"  {'ABOVE' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'BELOW'} the model's adj composite ({ADJ_COMPOSITE:.3f}). The gap ({ADJ_GAP:+.2f}) indicates the stock is")
print(f"  {valuation_label.lower()} by model standards. In plain terms: the mechanical ratio_b reads BUY because")
print(f"  Eliquis hasn't started declining and the price still embeds a deep cliff discount — but the")
print(f"  proxy fundamentals composite is more muted ({PROXY_COMPOSITE:.1f}/4.0) because Cobenfy's actual Q2 scale")
print(f"  fell short of earlier hopes, and part of the current price is unconfirmed merger speculation.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) AstraZeneca merger talks — confirmation, denial, or walk-away (reported {AZN_MERGER_TALKS_REPORTED})")
print(f"  (2) Eliquis US loss-of-exclusivity timing/pace — generic entry trajectory through 2026-2028")
print(f"  (3) Cobenfy schizophrenia quarterly run-rate — trajectory toward/away from blockbuster status")
print(f"  (4) Cobenfy pipeline readouts — Alzheimer's-related psychosis, bipolar mania, adjunctive MDD")
print(f"  (5) Camzyos (HCM) and Breyanzi/Abecma cell therapy growth — non-Cobenfy growth portfolio scaling")
print(f"  (6) Net leverage trajectory — deleveraging pace post Karuna/RayzeBio/Mirati M&A")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $58  |  Trim above $68")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.3f}")
print("═" * (W + 4))
print()

# ── EXPORT ────────────────────────────────────────────────────────────────────
RESULT = {
    "ticker":            TICKER,
    "signal":            signal_full,
    "signal_short":      signal_short,
    "price":             CURRENT_PRICE,
    "epp_gap_pct":       epp_gap_pct,
    "ratio_b":           ratio_b if ratio_b != float("inf") else None,
    "ratio_b_fmt":       ratio_b_str,
    "adj_composite":     ADJ_COMPOSITE,
    "market_composite":  MARKET_COMPOSITE,
    "adj_gap":           ADJ_GAP,
    "valuation":         valuation_label,
    "cons_return_2yr":   cons_return,
}

if __name__ == "__main__":
    pass
