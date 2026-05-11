#!/usr/bin/env python3
"""
ISRG  ·  Intuitive Surgical
BottomUp Risk/Reward Analyzer  —  three-part publication format

Part 1  FRAMEWORK LOGIC     what each concept means (reusable)
Part 2  ISRG CASE           narrative per section, only what matters
Part 3  NUMBERS & SIGNALS   pure data, no prose

Price: $452  (Yahoo Finance, 2026-05-09)
"""
import math

# ══════════════════════════════════════════════════════════════════════════════
# INPUTS
# ══════════════════════════════════════════════════════════════════════════════
TICKER        = "ISRG"
COMPANY       = "Intuitive Surgical"
SECTOR        = "Surgical Robotics · Medical Devices"
DATE          = "2026-05-09"
CURRENT_PRICE = 452.0     # Yahoo Finance / WebSearch 2026-05-09

EPS_TROUGH_YEAR   = 2022
EPS_TROUGH        = 4.96
EPS_NOW           = 8.93
EPS_Q1_2026       = 2.50
EPS_FWD_CONSENSUS = 10.40
EPS_TROUGH_PRICE  = 197.0

EPP_MIN_PE      = 40.0
CONS_EPS_CAGR   = 0.15
CONS_EXIT_PE    = 47.0
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

SCENARIOS = [
    ("BEAR",  "China ban + GLP-1 collapse + hospital freeze",     8.80, 38,  334),
    ("BASE",  "DV5 global rollout; Ion scaling; China contained", 12.30, 52,  640),
    ("BULL",  "Ion mainstream; new indications approved",         14.00, 58,  812),
    ("XBULL", "Surgical AI platform; intl re-acceleration",       16.50, 65, 1073),
]

CROSS_READS = [
    # name, what_it_tells_us, unit, bear_ceil, base_lo, bull_lo, xbull_lo, current, weight
    ("DV5 placements YoY",          "Hospital capex health",           "% YoY",  5,  5, 12, 20,  17, 0.25),
    ("Procedure volume YoY",        "Surgeon adoption & recurring rev", "% YoY",  8,  8, 14, 20,  16, 0.25),
    ("Ion platform procedures YoY", "New market traction",             "% YoY", 25, 25, 55, 90,  39, 0.15),
    ("International revenue YoY",   "Geographic expansion",            "% YoY",  8,  8, 15, 22,  13, 0.15),
    ("Hospital capex YoY",          "Macro / budget environment",      "% YoY",  3,  3,  7, 12,   5, 0.10),
    ("China procedure volume YoY",  "Geopolitical risk barometer",     "% YoY",  0,  0, 10, 20,   8, 0.10),
]

STRUCTURAL_FACTORS = [
    ("Installed base switching cost moat  (9,000+ systems)",     +1.5, 0.25),
    ("No credible full-system competitor (2026)",                +1.0, 0.20),
    ("China revenue concentration  (~10-12% of revenue)",       -1.0, 0.20),
    ("GLP-1 → bariatric procedure volume overhang",             -0.5, 0.15),
    ("DV5 upgrade cycle — hospitals mid-rollout",               +0.8, 0.20),
]

EPS_DECOMP = [
    ("Real procedure volume growth",     0.44,  True),
    ("Operating leverage / margin",      0.26,  True),
    ("Mix shift  (Ion + complex procs)", 0.07,  True),
    ("ASP / consumable price hikes",     0.115, False),
    ("CPI cost pass-through",            0.105, False),
    ("Share count reduction",            0.010, True),
]

# ── IDIOSYNCRATIC ASSESSMENT ──────────────────────────────────────────────────
IDIO = {
    "idio_pct": 62,   # % of return driver that is company/sector-specific
    "macro_pct": 38,  # % driven by macro sentiment / rates / risk appetite
    "beta": 1.05,
    "drivers": [
        # (factor, idio_or_macro, weight, description)
        ("DV5 upgrade cycle execution",         "IDIO",  0.22, "Hospital-by-hospital adoption; no macro linkage"),
        ("Ion platform reimbursement & growth", "IDIO",  0.18, "FDA/CMS decisions; lung cancer screening TAM"),
        ("China revenue  (ban vs. growth)",     "IDIO",  0.15, "Geopolitical; specific to US medtech in China"),
        ("GLP-1 procedure volume impact",       "IDIO",  0.07, "Sector-specific; bariatric / hernia volumes"),
        ("P/E multiple  (rate sensitivity)",    "MACRO", 0.18, "At 51x, 100bp rate move ≈ 5-8pt P/E compression"),
        ("Hospital capex budget cycle",         "MACRO", 0.10, "Correlated with GDP / CFO confidence surveys"),
        ("Broad market beta  (1.05x)",          "MACRO", 0.10, "Moves with S&P; amplified in risk-off episodes"),
    ],
    "note": (
        "ISRG is a moderately idiosyncratic bet.  The EPP floor and recurring "
        "revenue base (~70% instruments/accessories) are company-specific — they "
        "do not disappear in a recession.  However ~38% of the return profile is "
        "macro-sensitive: the P/E at 51x is rate-elastic, and broad risk-off "
        "episodes pull the stock down regardless of fundamentals (as seen in 2022 "
        "and YTD 2026).  The single largest idiosyncratic risk is China — a binary "
        "event (ban vs. no ban) that has no macro substitute."
    ),
}

# ══════════════════════════════════════════════════════════════════════════════
# ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def score_cr(val, base_lo, bull_lo, xbull_lo):
    if val >= xbull_lo: return 4
    if val >= bull_lo:  return 3
    if val >= base_lo:  return 2
    return 1

SLABEL = {4: "XBULL ★★", 3: "BULL  ▲ ", 2: "BASE  ◦ ", 1: "BEAR  ⚠ "}
SBAR   = {4: "████", 3: "███░", 2: "██░░", 1: "█░░░"}

scored = [(name, desc, unit, bc, blo, bulo, xlo, cur, w, score_cr(cur, blo, bulo, xlo))
          for (name, desc, unit, bc, blo, bulo, xlo, cur, w) in CROSS_READS]

proxy_composite = sum(sc * w for *_, sc, w in scored)
bear_composite  = sum(score_cr(bc, blo, bulo, xlo) * w
                      for (_, __, ___, bc, blo, bulo, xlo, cur, w) in CROSS_READS)
sca             = sum(s * w for _, s, w in STRUCTURAL_FACTORS)
adj_composite   = proxy_composite + sca

sc_map = {lbl: (narr, eps, pe, price) for lbl, narr, eps, pe, price in SCENARIOS}

def softmax(c, T=0.60):
    centres = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    raw = {k: math.exp(-abs(c - v) / T) for k, v in centres.items()}
    tot = sum(raw.values())
    return {k: v / tot for k, v in raw.items()}

def ev(probs): return sum(probs[k] * sc_map[k][3] for k in probs)

proxy_probs = softmax(proxy_composite)
mkt_target  = CURRENT_PRICE * (1 + REQUIRED_RETURN) ** HORIZON_YEARS

def solve_market(target, tol=5.0):
    for c in [x/100 for x in range(100, 401)]:
        if abs(ev(softmax(c)) - target) < tol:
            return round(c, 2), softmax(c)
    return None, {}

mkt_comp, mkt_probs = solve_market(mkt_target)
mkt_ev = ev(mkt_probs) if mkt_probs else mkt_target
proxy_ev = ev(proxy_probs)

epp_now         = EPS_NOW * EPP_MIN_PE
epp_trough_val  = EPS_TROUGH * EPP_MIN_PE
epp_gap_pct     = (CURRENT_PRICE - epp_now) / epp_now * 100
bear_vs_epp     = (sc_map["BEAR"][3] - epp_now) / epp_now * 100

trailing_pe = CURRENT_PRICE / EPS_NOW
forward_pe  = CURRENT_PRICE / EPS_FWD_CONSENSUS

cons_eps_2yr   = EPS_NOW * (1 + CONS_EPS_CAGR) ** 2
cons_price_2yr = cons_eps_2yr * CONS_EXIT_PE
cons_ret_ann   = (cons_price_2yr - CURRENT_PRICE) / CURRENT_PRICE / 2 * 100

dist_epp = CURRENT_PRICE - epp_now
price_A  = CURRENT_PRICE * (1 + (cons_eps_2yr / EPS_NOW - 1))
price_B  = cons_eps_2yr * CONS_EXIT_PE
price_C  = sc_map["BASE"][3]

ratio_A = dist_epp / (price_A - CURRENT_PRICE)
ratio_B = dist_epp / (price_B - CURRENT_PRICE)
ratio_C = dist_epp / (price_C - CURRENT_PRICE)

def rlabel(r):
    if r < 0.75:  return "◉ BUY"
    if r < 1.10:  return "◎ ACCUMULATE"
    if r < 1.75:  return "◐ WATCHLIST"
    if r < 2.50:  return "○ HOLD / TRIM"
    return              "✕ AVOID"

SIGNAL = rlabel(ratio_B)
adj_gap = adj_composite - mkt_comp if mkt_comp else 0

vol_pct = 0.28
sigma   = CURRENT_PRICE * vol_pct
eps_g_total = EPS_NOW - EPS_TROUGH
infl_dollar = sum(EPS_TROUGH * sh for _, sh, real in EPS_DECOMP if not real)
real_dollar = eps_g_total - infl_dollar

# ══════════════════════════════════════════════════════════════════════════════
# ── PART 1  FRAMEWORK LOGIC ───────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
W   = 74
HR  = "─" * 62
HR2 = "─" * (W-2)
HR3 = "─" * 60
HR4 = "─" * 38
HR5 = "─" * 48

def rule(): print("  " + HR)
def head():
    print()
    print("█" * W)

head()
print(f"""
  PART 1  ·  FRAMEWORK LOGIC
  What each concept means  —  applies to any stock in this system
  {HR2}

  EPP  —  Earnings Power Price
  ────────────────────────────
  The lowest price rational capital will accept for a business, given
  what it earns today.  Calculated as:

      EPP  =  current normalized EPS  ×  min-viable trough P/E

  The trough P/E is the floor multiple the market has historically
  assigned this business at maximum fear — a function of franchise
  quality, switching costs, and revenue predictability.  It does NOT
  change with sentiment.  Only EPS changes it.  When price = EPP you
  are buying at the floor.  When price > EPP you are paying a premium
  over the floor — that premium must be earned back by EPS growth.

  ATTRACTIVENESS RATIO
  ────────────────────
  Answers the single most important question in value investing:
  is the upside worth the floor risk?

      Ratio  =  (current price − EPP)  /  (2yr reflated price − current)
             =  downside to floor  /  upside from EPS compounding

  Below 0.75   ◉  BUY          EPS growth dominates the floor gap
  0.75 – 1.1   ◎  ACCUMULATE   Balanced; slight edge to upside
  1.1  – 1.75  ◐  WATCHLIST    Floor gap exceeds EPS upside; wait
  Above 1.75   ✕  AVOID        Growth priced in; asymmetric downside

  Three methods (A/B/C) test the ratio under different multiple assumptions.
  Method B (conservative exit P/E) is the primary signal — it stress-tests
  the upside by assuming a modest de-rate alongside conservative EPS growth.

  CROSS-READ MODEL
  ────────────────
  Instead of trusting management guidance, we track 5-6 EXTERNAL signals
  that are observable before the company reports.  Each signal maps to a
  specific revenue or cost driver.  When multiple signals align, conviction
  is high.  When they diverge, uncertainty is high.

  Each signal is scored 1-4 (BEAR / BASE / BULL / XBULL) against
  pre-defined thresholds.  The weighted composite places the company on
  the scenario spectrum.  That composite is then compared to the market
  composite — back-solved from: what score does the current price require
  to deliver the hurdle rate?  The gap between the two is the edge.

  STRUCTURAL FACTORS  (SCA — Structural Composite Adjustment)
  ─────────────────────────────────────────────────────────────
  Qualitative overlay on top of the quantitative signal composite.
  Moats, competitive dynamics, and risks that do not show up in the
  proxy signals but affect the long-run floor and ceiling.  Scored
  −2 to +2, weighted, added to the proxy composite.

  EPS QUALITY CHECK
  ─────────────────
  Not all EPS growth is equal.  We decompose EPS growth into:
    Real:       procedure / unit volume, operating leverage, mix shift
    Inflation:  ASP price hikes, CPI pass-through
  A business growing EPS 80% where 78% is real and only 22% is price
  is structurally compounding.  One where the inverse is true is not.

  SCENARIO MAP
  ────────────
  Four named outcomes (BEAR / BASE / BULL / XBULL) each with an EPS
  assumption, exit multiple, and 2-year price target.  The model assigns
  probabilities via a softmax function centered on the proxy composite.
  The market's implied probabilities are back-solved from the current price.
  The gap between model and market probabilities is where conviction lives.

  IDIOSYNCRATIC SCORE
  ───────────────────
  Estimates what fraction of the investment outcome is driven by
  company/sector-specific factors (idiosyncratic) versus macro sentiment,
  rate cycles, and broad market moves.  High idiosyncratic → thesis is
  right or wrong on its own merits.  High macro → you also need to be
  right on the environment.  The EPP floor is always more idiosyncratic
  than the premium above it.""")

# ══════════════════════════════════════════════════════════════════════════════
# ── PART 2  ISRG CASE ─────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
head()
print(f"""
  PART 2  ·  ISRG CASE  —  What matters for this specific bet
  {HR2}

  EPP FLOOR
  ─────────
  The 2022 EPP model called $198 — the actual low was $197.  The floor
  has since migrated to $357 (+80%) driven entirely by EPS compounding;
  the trough multiple is unchanged at 40x.  That 40x is the historical
  minimum — the market has never valued ISRG's installed base below this
  even at maximum fear, because ~70% of revenue is instruments and
  accessories locked to existing systems regardless of new sales.

  EPS QUALITY
  ───────────
  The $3.97 EPS gain from FY2022 to FY2025 is 78% real — procedure
  volume growth and operating leverage, not pricing games.  The business
  is physically larger (9,000+ systems vs ~7,500 in 2022) and Q1 2026
  came in at +38% YoY, accelerating.  Stripping inflation entirely,
  the "real EPS" still yields a floor of $314 — well below today's price.

  CROSS-READ MODEL
  ────────────────
  Two signals are running hot (BULL): DV5 placements +17% and procedure
  volume +16% — these are the core recurring-revenue engine and confirm
  the installed base is expanding fast.  Four signals are at BASE: Ion
  (+39%) is still below the BULL threshold (55%) but is the most important
  one to watch — if it crosses, it opens a genuinely new TAM (lung cancer
  screening) that isn't in the current multiple.  China at +8% is the key
  risk signal — any geopolitical escalation flips it to BEAR instantly.

  SCENARIO MAP
  ────────────
  The market is pricing 28% BEAR probability — heavy China fear premium.
  The model assigns 9%.  That 19pp gap is the thesis: China risk is real
  but the market is over-weighting it relative to the underlying momentum.
  BASE ($640) requires nothing extraordinary — just DV5 executing and
  Ion continuing its current trajectory.  BULL requires Ion to reach
  mainstream reimbursement (colorectal / cardiac), which is 2-3yr optionality
  not yet in consensus.

  ATTRACTIVENESS RATIO
  ─────────────────────
  At $452, Method B (conservative 47x exit, 15% EPS CAGR) gives 0.92x —
  meaning the EPS upside (+23%) just covers the floor gap (21%).  This
  is the level where entry begins to make sense: not a screaming buy,
  but the stock has already absorbed the -20% YTD tariff shock and the
  multiple has normalized.  The stock becomes ◉ BUY at ~$390, which
  requires only a China headline or broad market correction.

  IDIOSYNCRATIC SCORE  —  62% idiosyncratic / 38% macro-sentiment
  ──────────────────────────────────────────────────────────────────""")

total_idio  = sum(w for _, t, w, __ in IDIO["drivers"] if t == "IDIO")
total_macro = sum(w for _, t, w, __ in IDIO["drivers"] if t == "MACRO")
for factor, kind, wt, desc in IDIO["drivers"]:
    tag = "IDIO  →" if kind == "IDIO" else "MACRO →"
    bar = "▓" * round(wt * 60)
    print(f"  {tag}  {wt*100:.0f}%  {factor:<38}  {desc[:32]}")

print(f"""
  {IDIO['note']}

  Practical implication:  you can be right on ISRG's fundamentals and
  still lose 15-20% in a rate shock or risk-off episode because the P/E
  at 51x is elastic.  The EPP floor ($357) cushions this — below it,
  macro cannot push price much further without an EPS break.  Above $500,
  macro risk dominates and the bet becomes increasingly sentiment-driven.""")

# ══════════════════════════════════════════════════════════════════════════════
# ── PART 3  NUMBERS & SIGNALS ─────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
head()
print(f"""
  PART 3  ·  NUMBERS & SIGNALS  ·  {TICKER}  ·  ${CURRENT_PRICE:.0f}  ·  {DATE}
  {HR2}""")

# Signal card
print(f"""
  ┌{HR3}┐
  │  {SIGNAL:<20}  EPP gap {epp_gap_pct:+.0f}%  ·  Ratio B {ratio_B:.2f}x          │
  │  Cons. return {cons_ret_ann:+.0f}%/yr  ·  EPP ${epp_now:.0f}  ·  Fwd P/E {forward_pe:.0f}x       │
  └{HR3}┘""")

# Cross-read
print(f"""
  CROSS-READ  (proxy {proxy_composite:.2f} / 4.00  ·  market {mkt_comp:.2f}  ·  gap {adj_gap:+.2f})
  {HR}
  {"Signal":<32}  {"What it tracks":<28}  {"Now":>5}  Score""")
rule()
for name, desc, unit, bc, blo, bulo, xlo, cur, w, sc in scored:
    u = unit.split()[0]
    print(f"  {name:<32}  {desc:<28}  {cur:>+4}{u}  {SLABEL[sc]}  {SBAR[sc]}")

print(f"""
  {HR}
  {"Factor":<48}  {"Score":>6}  {"Wt":>5}  {"Adj":>6}""")
for desc, sc, wt in STRUCTURAL_FACTORS:
    print(f"  {desc:<48}  {sc:>+5.1f}  {wt*100:>4.0f}%  {sc*wt:>+5.2f}")
print(f"  {HR}")
print(f"  SCA total {sca:+.2f}  ·  Adj composite {adj_composite:.2f}  ·  Verdict: UNDERVALUED  (gap {adj_gap:+.2f})")

# Scenario × threshold
print(f"""
  SCENARIO THRESHOLDS  (signal must reach → for scenario to hold)
  {HR}
  {"Signal":<32}  {"BEAR<":>6}  {"BASE":>8}  {"BULL":>8}  {"XBULL≥":>7}  {"NOW":>5}""")
rule()
for name, desc, unit, bc, blo, bulo, xlo, cur, w, sc in scored:
    u = unit.split()[0]
    base_r = f"{blo}-{bulo}"
    bull_r = f"{bulo}-{xlo}"
    print(f"  {name:<32}  {bc:>5}{u}  {base_r:>8}  {bull_r:>8}  {xlo:>6}{u}  {cur:>+4}{u}")

# EPS quality
print(f"""
  EPS QUALITY  (FY2022 ${EPS_TROUGH:.2f} → FY2025 ${EPS_NOW:.2f};  CAGR {((EPS_NOW/EPS_TROUGH)**(1/3)-1)*100:.1f}%/yr)
  {HR}
  {"Driver":<38}  {"Share":>7}  {"$EPS":>6}  Type""")
rule()
for driver, share, is_real in EPS_DECOMP:
    dollar = EPS_TROUGH * share
    kind   = "REAL  ✓" if is_real else "INFL. ~"
    print(f"  {driver:<38}  {share*100:>6.1f}%  ${dollar:>4.2f}  {kind}")
print(f"  {HR4}")
print(f"  Real {real_dollar/eps_g_total*100:.0f}%  ${real_dollar:.2f}  ✓    Inflation {infl_dollar/eps_g_total*100:.0f}%  ${infl_dollar:.2f}  ~")

# EPP
print(f"""
  EPP FLOOR
  {HR}
  {"Year":<8}  {"EPS":>6}  {"Trough P/E":>12}  {"EPP":>7}  {"Actual low":>11}
  {HR}
  {"2022":<8}  ${EPS_TROUGH:>5.2f}  {"× 40x":>12}  ${epp_trough_val:>5.0f}  {"$197  ✓":>11}
  {"2026":<8}  ${EPS_NOW:>5.2f}  {"× 40x":>12}  ${epp_now:>5.0f}  {"today":>11}
  {HR}
  Current ${CURRENT_PRICE:.0f}  vs  EPP ${epp_now:.0f}:  {epp_gap_pct:+.0f}%  above floor  ·  {(CURRENT_PRICE-epp_now)/sigma:.1f}σ to EPP
  Bear    ${sc_map['BEAR'][3]:.0f}  vs  EPP ${epp_now:.0f}:  {bear_vs_epp:+.0f}%  ← bear breaks the floor""")

# Scenarios
print(f"""
  SCENARIOS  (2yr targets;  proxy vs market probabilities)
  {HR}
  {"Scenario":<8}  {"EPS":>6}  {"P/E":>5}  {"Price":>7}  {"Proxy%":>8}  {"Mkt%":>7}  {"Gap":>7}""")
rule()
for lbl, narr, eps, pe, price in SCENARIOS:
    pp = proxy_probs[lbl]
    mp = mkt_probs.get(lbl, 0)
    print(f"  {lbl:<8}  ${eps:>5.2f}  {pe:>4}x  ${price:>6}  {pp*100:>7.1f}%  {mp*100:>6.1f}%  {(pp-mp)*100:>+6.1f}pp")
print(f"  {HR}")
print(f"  Proxy EV ${proxy_ev:.0f}  ·  Market EV ${mkt_ev:.0f}  ·  Consensus ~$622  ·  Bear prob: model {proxy_probs['BEAR']*100:.0f}% vs mkt {mkt_probs.get('BEAR',0)*100:.0f}%")

# Attractiveness ratio
print(f"""
  ATTRACTIVENESS RATIO  (downside to EPP / upside to 2yr target)
  {HR}
  Downside to EPP:  ${dist_epp:.0f}  ({dist_epp/CURRENT_PRICE*100:.0f}% of current price)
  {HR}
  {"Method":<28}  {"2yr target":>11}  {"Upside":>8}  {"Ratio":>7}  Signal
  {HR}
  {"A: Same P/E (51x trailing)":<28}  ${price_A:>9.0f}  {(price_A-CURRENT_PRICE)/CURRENT_PRICE*100:>+7.0f}%  {ratio_A:>6.2f}x  {rlabel(ratio_A)}
  {"B: Conserv exit 47x  ←PRIMARY":<28}  ${price_B:>9.0f}  {(price_B-CURRENT_PRICE)/CURRENT_PRICE*100:>+7.0f}%  {ratio_B:>6.2f}x  {rlabel(ratio_B)}
  {"C: BASE scenario":<28}  ${price_C:>9.0f}  {(price_C-CURRENT_PRICE)/CURRENT_PRICE*100:>+7.0f}%  {ratio_C:>6.2f}x  {rlabel(ratio_C)}""")

# Idiosyncratic
print(f"""
  IDIOSYNCRATIC SCORE
  {HR}
  Idiosyncratic  {IDIO['idio_pct']}%   ██████████████████░░░░░░░░░░░░
  Macro/sentiment {IDIO['macro_pct']}%   ████████████░░░░░░░░░░░░░░░░░░
  Beta  {IDIO['beta']:.2f}
  {HR}
  {"Factor":<38}  {"Type":>6}  {"Wt":>5}""")
rule()
for factor, kind, wt, desc in IDIO["drivers"]:
    print(f"  {factor:<38}  {kind:>6}  {wt*100:>4.0f}%  {desc[:28]}")

# Entry framework
print(f"""
  ENTRY FRAMEWORK
  {HR}
  {"Zone":<16}  {"Price range":>14}  {"Ratio B":>8}  Action
  {HR}
  {"◉ EPP floor":<16}  {"$357 – $397":>14}  {"< 0.50x":>8}  Buy aggressively
  {"◎ High conv.":<16}  {"$397 – $430":>14}  {"0.50–0.75x":>8}  Build position
  {"◎ Today":<16}  {"~$452":>14}  {"0.92x":>8}  Accumulate
  {"◐ Watchlist":<16}  {"$480 – $530":>14}  {"1.1–1.5x":>8}  Hold / no add
  {"✕ Avoid":<16}  {"> $530":>14}  {"> 1.75x":>8}  Trim on strength
  {HR}
  UPGRADE to ◉ BUY if:   Ion crosses 55% growth  OR  China risk removed
  DOWNGRADE to ✕ if:     Procedure vol < 8% for 2 qtrs  OR  DV5 ASP pushback""")

# Summary
print(f"""
  {HR}
  {TICKER}  ·  ${CURRENT_PRICE:.0f}  ·  {DATE}

  {SIGNAL:<20}  Ratio B {ratio_B:.2f}x  ·  EPP ${epp_now:.0f} ({epp_gap_pct:+.0f}%)  ·  Cons. {cons_ret_ann:+.0f}%/yr
  Idiosyncratic {IDIO['idio_pct']}% / Macro {IDIO['macro_pct']}%  ·  #1 risk: China  ·  Best entry: ${epp_now:.0f}–${epp_now+80:.0f}""")
print()
print("█" * W)
print()
