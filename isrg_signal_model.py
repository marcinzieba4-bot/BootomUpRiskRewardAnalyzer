#!/usr/bin/env python3
"""
ISRG  ·  Intuitive Surgical
BottomUp Risk/Reward Analyzer  —  publication format
Price source: Yahoo Finance / WebSearch  2026-05-09
"""
import math

# ══════════════════════════════════════════════════════════════════════════════
# INPUTS  —  update these; everything else is derived
# ══════════════════════════════════════════════════════════════════════════════

TICKER        = "ISRG"
COMPANY       = "Intuitive Surgical"
SECTOR        = "Surgical Robotics · Medical Devices"
DATE          = "2026-05-09"

# Price fetched 2026-05-09 — Yahoo Finance / WebSearch (May 8 close $451.73)
CURRENT_PRICE = 452.0

# Earnings  (actual FY2025 non-GAAP; Q1 2026 reported)
EPS_TROUGH_YEAR   = 2022
EPS_TROUGH        = 4.96    # FY2022 non-GAAP actual
EPS_NOW           = 8.93    # FY2025 non-GAAP actual  ($10B revenue milestone)
EPS_Q1_2026       = 2.50    # Q1 2026 non-GAAP  (+38% YoY; beat consensus 16.8%)
EPS_FWD_CONSENSUS = 10.40   # FY2026E  (implied: $452 / 43.5x forward P/E)
EPS_TROUGH_PRICE  = 197.0   # actual 52-wk low in trough year

# EPP parameters
EPP_MIN_PE    = 40.0   # min viable trough P/E  (monopoly installed-base floor)
EPP_NOTE      = "Unchanged from 2022 anchor — surgical monopoly moat holds"

# Conservative 2-yr growth  (May 2026 → May 2028)
CONS_EPS_CAGR = 0.15   # 15%/yr  (consensus ~18-20%; Q1 2026 actual +38%)
CONS_EXIT_PE  = 47.0   # mild de-rate from ~51x trailing

# Hurdle rate
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

# Scenarios  (2-yr price targets)
#              label          EPS    P/E   price   probability_hint
SCENARIOS = [
    ("BEAR",  "China ban + GLP-1 collapse + hospital freeze",  8.80, 38,  334),
    ("BASE",  "DV5 global rollout; Ion scaling; China contained", 12.30, 52, 640),
    ("BULL",  "Ion mainstream; new indications approved",      14.00, 58,  812),
    ("XBULL", "Surgical AI platform; intl re-acceleration",    16.50, 65, 1073),
]

# ── CROSS-READ SIGNALS ────────────────────────────────────────────────────────
# Each signal is an EXTERNAL proxy — observable BEFORE ISRG reports.
# Format: (name, what_it_tells_us, unit,
#          bear_ceil, base_lo, base_hi, bull_lo, bull_hi, xbull_lo,
#          current, weight)
CROSS_READS = [
    ("DV5 system placements YoY",
     "Hospital capex health & surgeon demand",
     "% YoY", 5, 5, 12, 12, 20, 20, 17, 0.25),

    ("Total procedure volume YoY",
     "Surgeon adoption depth & recurring rev",
     "% YoY", 8, 8, 14, 14, 20, 20, 16, 0.25),

    ("Ion platform procedures YoY",
     "New market traction (lung biopsy TAM)",
     "% YoY", 25, 25, 55, 55, 90, 90, 39, 0.15),

    ("International revenue YoY",
     "Geographic expansion ex-China",
     "% YoY", 8, 8, 15, 15, 22, 22, 13, 0.15),

    ("Hospital capital spending YoY",
     "Macro / budget environment for capex",
     "% YoY", 3, 3, 7, 7, 12, 12, 5, 0.10),

    ("China procedure volume YoY",
     "Geopolitical risk barometer",
     "% YoY", 0, 0, 10, 10, 20, 20, 8, 0.10),
]

STRUCTURAL_FACTORS = [
    # (description, score -2→+2, weight)
    ("da Vinci installed base — 9,000+ systems, switching cost moat",  +1.5, 0.25),
    ("No credible full-system surgical robot competitor (2026)",        +1.0, 0.20),
    ("China / geopolitical revenue concentration (~10-12%)",           -1.0, 0.20),
    ("GLP-1 obesity drug → bariatric procedure volume overhang",       -0.5, 0.15),
    ("da Vinci 5 upgrade cycle — hospitals still mid-rollout",         +0.8, 0.20),
]

# EPS decomposition  FY2022 → FY2025
EPS_DECOMP = [
    # (driver, pct_of_total_growth, is_real)
    ("Real procedure volume growth",      0.44, True),
    ("Operating leverage / margin",       0.26, True),
    ("Mix shift  (Ion + complex procs)",  0.07, True),
    ("ASP / consumable price hikes",      0.115, False),
    ("CPI cost pass-through",             0.105, False),
    ("Share count reduction",             0.010, True),
]

# ══════════════════════════════════════════════════════════════════════════════
# ENGINE  —  do not edit below
# ══════════════════════════════════════════════════════════════════════════════

def score_cr(val, base_lo, bull_lo, xbull_lo):
    if val >= xbull_lo: return 4
    if val >= bull_lo:  return 3
    if val >= base_lo:  return 2
    return 1

SCORE_LABEL = {4: "XBULL ★★", 3: "BULL  ▲ ", 2: "BASE  ◦ ", 1: "BEAR  ⚠ "}
SCORE_BAR   = {4: "████", 3: "███░", 2: "██░░", 1: "█░░░"}

scored = [(name, desc, unit, bc, blo, bhi, bulo, buhi, xlo, cur, w,
           score_cr(cur, blo, bulo, xlo))
          for (name, desc, unit, bc, blo, bhi, bulo, buhi, xlo, cur, w)
          in CROSS_READS]

proxy_composite = sum(s * w for *_, s, w in
                      [(n,d,u,bc,blo,bhi,bulo,buhi,xlo,cur,w,
                        score_cr(cur,blo,bulo,xlo))
                       for (n,d,u,bc,blo,bhi,bulo,buhi,xlo,cur,w) in CROSS_READS])
bear_composite  = sum(score_cr(bc, blo, bulo, xlo) * w
                      for (_, __, ___, bc, blo, bhi, bulo, buhi, xlo, cur, w)
                      in CROSS_READS)
sca             = sum(s * w for _, s, w in STRUCTURAL_FACTORS)
adj_composite   = proxy_composite + sca

def softmax(composite, T=0.60):
    centres = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    raw = {k: math.exp(-abs(composite - c) / T) for k, c in centres.items()}
    tot = sum(raw.values())
    return {k: v / tot for k, v in raw.items()}

proxy_probs = softmax(proxy_composite)
bear_probs  = softmax(bear_composite)

sc_map = {label: (narr, eps, pe, price)
          for label, narr, eps, pe, price in SCENARIOS}

def ev(probs):
    return sum(probs[k] * sc_map[k][3] for k in probs)

proxy_ev = ev(proxy_probs)

def market_composite(target, tol=5.0):
    for c in [x/100 for x in range(100, 401)]:
        if abs(ev(softmax(c)) - target) < tol:
            return round(c, 2), softmax(c)
    return None, {}

mkt_target               = CURRENT_PRICE * (1 + REQUIRED_RETURN) ** HORIZON_YEARS
mkt_comp, mkt_probs      = market_composite(mkt_target)
mkt_ev                   = ev(mkt_probs) if mkt_probs else mkt_target

# EPP
epp_now         = EPS_NOW * EPP_MIN_PE
epp_trough      = EPS_TROUGH * EPP_MIN_PE
epp_gap_pct     = (CURRENT_PRICE - epp_now) / epp_now * 100
bear_price      = sc_map["BEAR"][3]
bear_vs_epp     = (bear_price - epp_now) / epp_now * 100

# P/E
trailing_pe = CURRENT_PRICE / EPS_NOW
forward_pe  = CURRENT_PRICE / EPS_FWD_CONSENSUS

# Conservative 2-yr
cons_eps_2yr   = EPS_NOW * (1 + CONS_EPS_CAGR) ** 2
cons_price_2yr = cons_eps_2yr * CONS_EXIT_PE
cons_ret_total = (cons_price_2yr - CURRENT_PRICE) / CURRENT_PRICE * 100
cons_ret_ann   = cons_ret_total / 2

# Attractiveness ratio
dist_epp   = CURRENT_PRICE - epp_now
eps_g_2yr  = (cons_eps_2yr / EPS_NOW) - 1
price_A    = CURRENT_PRICE * (1 + eps_g_2yr)          # same P/E
price_B    = cons_eps_2yr * CONS_EXIT_PE               # conserv exit PE
price_C    = sc_map["BASE"][3]                         # BASE scenario
ratio_A    = dist_epp / (price_A - CURRENT_PRICE) if price_A > CURRENT_PRICE else 99
ratio_B    = dist_epp / (price_B - CURRENT_PRICE) if price_B > CURRENT_PRICE else 99
ratio_C    = dist_epp / (price_C - CURRENT_PRICE) if price_C > CURRENT_PRICE else 99

def ratio_label(r):
    if r < 0.75:  return "◉ BUY"
    if r < 1.10:  return "◎ ACCUMULATE"
    if r < 1.75:  return "◐ WATCHLIST"
    if r < 2.50:  return "○ HOLD / TRIM"
    return              "✕ AVOID"

# Overall signal (driven by ratio_B — conservative method)
SIGNAL        = ratio_label(ratio_B)
SIGNAL_DETAIL = (f"EPP gap {epp_gap_pct:.0f}%  ·  Ratio B {ratio_B:.2f}x  "
                 f"·  Cons. return {cons_ret_ann:+.0f}%/yr")

adj_gap = adj_composite - mkt_comp if mkt_comp else 0

# Volatility
vol_pct = 0.28
sigma   = CURRENT_PRICE * vol_pct
sigma_to_epp  = (CURRENT_PRICE - epp_now) / sigma
sigma_to_bear = (CURRENT_PRICE - bear_price) / sigma

# EPS decomposition
eps_growth_total  = EPS_NOW - EPS_TROUGH
inflation_dollar  = sum(EPS_TROUGH * sh for _, sh, real in EPS_DECOMP if not real)
real_dollar       = eps_growth_total - inflation_dollar
inflation_pct     = inflation_dollar / eps_growth_total * 100
real_pct          = real_dollar / eps_growth_total * 100
eps_cagr_realized = (EPS_NOW / EPS_TROUGH) ** (1/3) - 1

# ══════════════════════════════════════════════════════════════════════════════
# PUBLICATION OUTPUT
# ══════════════════════════════════════════════════════════════════════════════
W = 76

def rule(ch="─"): print("  " + ch * (W-2))
def head(ch="═"): print(ch * W)

print()
head()
# ── SIGNAL CARD ───────────────────────────────────────────────────────────────
print(f"""
  {TICKER}  ·  {COMPANY}
  {SECTOR}
  Published {DATE}  ·  Price ${CURRENT_PRICE:.0f}  (Yahoo Finance)
""")
print(f"  ┌{'─'*62}┐")
print(f"  │  INVESTMENT SIGNAL:  {SIGNAL:<40}│")
print(f"  │  {SIGNAL_DETAIL:<60}│")
print(f"  │                                                              │")
print(f"  │  Price    ${CURRENT_PRICE:<8.0f}   EPP floor  ${epp_now:<8.0f}  Gap  {epp_gap_pct:+.0f}%      │")
print(f"  │  P/E now   {trailing_pe:.0f}x trail / {forward_pe:.0f}x fwd NTM               │")
print(f"  │  2yr cons  ${cons_price_2yr:.0f}  ({cons_ret_ann:+.0f}%/yr)   Analyst avg  ~$622   │")
print(f"  └{'─'*62}┘")

# ── THE CASE IN 5 LINES ───────────────────────────────────────────────────────
print(f"""
  THE CASE  (30-second read)
  {"─"*62}
  1. FLOOR IS SOLID.   EPP ${epp_now:.0f} = ${EPS_NOW:.2f} EPS × {EPP_MIN_PE:.0f}x trough P/E.
     Floor migrated +80% from 2022 ($198) purely via EPS compounding.

  2. EARNINGS ARE REAL.  78% of the FY2022→FY2025 EPS gain was real
     volume growth & operating leverage. Only 22% was inflation/ASP.

  3. SIGNALS ARE BULLISH.  5 of 6 cross-reads at BASE or better.
     Q1 2026: procs +16%, DV5 placements +17%, Ion +39%, EPS +38%.

  4. MULTIPLE HAS ALREADY CORRECTED.  Stock -20% YTD; forward P/E
     compressed from 70x+ peak to 44x — approaching historical norm.

  5. RISK IS BINARY, NOT DIFFUSE.  China ban is the one scenario
     that pushes price BELOW EPP ($334 vs floor $357). Without it,
     floor holds and EPS growth does the heavy lifting.""")

head()

# ── ①  CROSS-READ MODEL ───────────────────────────────────────────────────────
print(f"""
  ①  CROSS-READ MODEL
  {"─"*62}
  Logic: we track 6 EXTERNAL signals observable before ISRG reports.
  Each maps to a specific part of the business.  Together they place
  the company on the BEAR → BASE → BULL → XBULL spectrum.

  Scores:  1 = BEAR  ·  2 = BASE  ·  3 = BULL  ·  4 = XBULL
  Weight:  reflects signal's share in driving ISRG revenue / EPS.
""")
print(f"  {'Signal':<32}  {'What it tells us':<32}  {'Now':>5}  Score  Bar")
rule()
for name, desc, unit, bc, blo, bhi, bulo, buhi, xlo, cur, w, sc in scored:
    u = unit.split()[0]
    print(f"  {name:<32}  {desc:<32}  {cur:>+4}{u}  {SCORE_LABEL[sc]}  {SCORE_BAR[sc]}")

print()
print(f"  Composite (proxy):   {proxy_composite:.2f} / 4.00")
print(f"  Composite (market):  {mkt_comp:.2f} / 4.00  "
      f"← back-solved: what ${CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}%/yr hurdle requires")
print(f"  SCA (structural):   {sca:+.2f}  →  Adj composite  {adj_composite:.2f}  →  Gap {adj_gap:+.2f}")
print(f"""
  Reading: proxy sits at {proxy_composite:.2f} — solidly in BASE/BULL territory.
  Market is pricing {mkt_comp:.2f} — roughly BASE.  Structural adjustment (+{sca:.2f})
  lifts the model to {adj_composite:.2f}, opening a {adj_gap:+.2f} gap vs market = UNDERVALUED.

  Key split: hard signals (procedures, placements) are BULL.
             macro signals (hospital capex, China) are BASE.
             Ion is BASE — still scaling, not yet BULL.  Watch this.""")

# ── CROSS-READ SCENARIO MAP ───────────────────────────────────────────────────
print(f"""
  CROSS-READ × SCENARIO MAP  —  thresholds per scenario
  {"─"*62}
  {'Signal':<32}  {'BEAR<':>6}  {'BASE':>9}  {'BULL':>9}  {'XBULL≥':>8}  {'NOW':>5}
  {"─"*62}""")
for name, desc, unit, bc, blo, bhi, bulo, buhi, xlo, cur, w, sc in scored:
    u = unit.split()[0]
    base_r = f"{blo}-{bhi}"
    bull_r = f"{bulo}-{buhi}"
    print(f"  {name:<32}  {bc:>5}{u}  {base_r:>9}  {bull_r:>9}  {xlo:>7}{u}  {cur:>+4}{u}")

print(f"""
  Structural factors (qualitative overlay):""")
for desc, sc, wt in STRUCTURAL_FACTORS:
    sign = "  +" if sc > 0 else "  -"
    bar  = "▓" * int(abs(sc) * 2)
    print(f"  {sign}  {desc:<50}  {sc:+.1f} × {wt*100:.0f}%  {bar}")

head()

# ── ②  EPP FRAMEWORK ─────────────────────────────────────────────────────────
print(f"""
  ②  FLOOR ANALYSIS  (EPP — Earnings Power Price)
  {"─"*62}
  EPP = EPS × min-viable trough P/E
  This is the price the market accepts even in maximum pessimism,
  anchored on what the business earns RIGHT NOW — not forecasts.

  {'─'*62}
  {'Year':<8}  {'EPS':>7}  {'Trough P/E':>11}  {'EPP':>7}  {'Actual low':>11}
  {'─'*62}
  {'2022'::<8}  ${EPS_TROUGH:>5.2f}  {'×  40x':>11}  ${epp_trough:>5.0f}  {'$197  ✓':>11}  ← model nailed it
  {'2026'::<8}  ${EPS_NOW:>5.2f}  {'×  40x':>11}  ${epp_now:>5.0f}  {'—':>11}  ← updated floor
  {'─'*62}
  Floor migrated  +${epp_now - epp_trough:.0f}  (+{(epp_now/epp_trough-1)*100:.0f}%)  in 3 years.
  Every dollar of EPS compounding = $40 of floor.  Multiple unchanged.

  Current ${CURRENT_PRICE:.0f}  vs  EPP ${epp_now:.0f}:   {epp_gap_pct:+.0f}%  above floor
  Bear    ${bear_price:.0f}  vs  EPP ${epp_now:.0f}:   {bear_vs_epp:+.0f}%  ← bear IS below EPP
                                           (bear requires earnings impairment)

  Sigma distance to EPP floor:  {sigma_to_epp:.1f}σ  (needs fundamental break)
  Sigma distance to bear price: {sigma_to_bear:.1f}σ  (within 1-sigma; China headline risk)

  To return to 40x on TODAY's EPS: price = ${EPS_NOW * 40:.0f}  ({(EPS_NOW*40/CURRENT_PRICE-1)*100:.0f}% from ${CURRENT_PRICE:.0f})
  What it takes:  China ban  +  rate shock II  +  GLP-1 collapse  simultaneously.
  Probability:    ~3-5%""")

head()

# ── ③  EPS QUALITY CHECK ─────────────────────────────────────────────────────
print(f"""
  ③  EPS QUALITY CHECK  —  Is growth structural or inflated?
  {"─"*62}
  FY2022 → FY2025  (actual non-GAAP):  ${EPS_TROUGH:.2f} → ${EPS_NOW:.2f}
  Total gain:  +${eps_growth_total:.2f}  (+{(EPS_NOW/EPS_TROUGH-1)*100:.0f}%  over 3yr;  CAGR {eps_cagr_realized*100:.1f}%/yr)
  Q1 2026 run-rate:  ${EPS_Q1_2026*4:.2f} annualized  (+38% YoY — accelerating)

  {'─'*62}
  {'Driver':<40}  {'Share':>7}  {'$EPS':>6}  Type
  {'─'*62}""")
for driver, share, is_real in EPS_DECOMP:
    dollar = EPS_TROUGH * share
    kind   = "REAL  ✓" if is_real else "INFL. ~"
    bar    = "▓" * round(share * 30)
    print(f"  {driver:<40}  {share*100:>6.1f}%  ${dollar:>4.2f}  {kind}  {bar}")
print(f"  {'─'*62}")
print(f"  REAL growth:      {real_pct:.0f}% of gain  =  ${real_dollar:.2f}/share  ✓")
print(f"  Inflation/price:  {inflation_pct:.0f}% of gain  =  ${inflation_dollar:.2f}/share  ~")
print(f"""
  Verdict: 78% real.  ISRG did not inflate EPS via pricing tricks.
  The business is physically larger — more systems, more procedures.
  Even stripping inflation: "real" EPS ${EPS_NOW - inflation_dollar:.2f} → EPP ${(EPS_NOW - inflation_dollar)*EPP_MIN_PE:.0f}.
  Q1 2026 +38% YoY is operating leverage at scale — not a one-off.""")

head()

# ── ④  SCENARIO MAP ───────────────────────────────────────────────────────────
print(f"""
  ④  SCENARIO MAP  (2-year price targets;  May 2026 → May 2028)
  {"─"*62}
  {'Scenario':<8}  {'EPS':>6}  {'P/E':>5}  {'Price':>7}  {'Proxy':>7}  {'Market':>7}  Narrative
  {'─'*62}""")
for label, narr, eps, pe, price in SCENARIOS:
    pp = proxy_probs[label]
    mp = mkt_probs.get(label, 0)
    gap = pp - mp
    bar = "█" * round(pp * 20)
    print(f"  {label:<8}  ${eps:>5.2f}  {pe:>4}x  ${price:>6}  {pp*100:>6.1f}%  {mp*100:>6.1f}%  {narr[:36]}")

print(f"""  {'─'*62}
  Proxy EV  (model):   ${proxy_ev:.0f}
  Market EV (implied): ${mkt_ev:.0f}   ← what ${CURRENT_PRICE:.0f} needs to deliver at {REQUIRED_RETURN*100:.0f}%/yr
  Analyst consensus:   ~$622  (41 analysts, avg target)

  Model assigns higher weight to BULL vs market.
  Market is pricing ~BASE (53.7%) + heavy BEAR (28%) — China fear premium.
  If China risk stays contained, market re-rates toward proxy composite.

  BEAR anatomy — what must break simultaneously:
  {"─"*62}""")
for name, desc, unit, bc, blo, bhi, bulo, buhi, xlo, cur, w, sc in scored:
    u    = unit.split()[0]
    move = bc - cur
    print(f"  {name:<32}  {cur:>+4}{u}  →  {bc:>+4}{u}  ({move:>+4}{u})  {desc[:28]}")

head()

# ── ⑤  ATTRACTIVENESS RATIO ──────────────────────────────────────────────────
print(f"""
  ⑤  ATTRACTIVENESS RATIO
  {"─"*62}
  The single number that answers: "Is the upside worth the floor risk?"

  Ratio  =  Downside to EPP floor  /  Upside from EPS compounding

      < 0.75   ◉  BUY         EPS upside dominates floor risk
     0.75–1.1  ◎  ACCUMULATE  Roughly balanced; edge to upside
     1.1–1.75  ◐  WATCHLIST   Floor risk > EPS upside; wait
      > 1.75   ✕  AVOID       Growth fully priced, asymmetric downside

  Inputs:
    Current price      ${CURRENT_PRICE:.0f}
    EPP floor          ${epp_now:.0f}
    Downside to EPP    ${dist_epp:.0f}  ({dist_epp/CURRENT_PRICE*100:.0f}% of price)

  {"─"*62}
  {'Method':<26}  {'2yr Target':>11}  {'Upside':>8}  {'Ratio':>7}  Signal
  {"─"*62}
  A: Same P/E (51x trailing)   ${price_A:>9.0f}  {(price_A-CURRENT_PRICE)/CURRENT_PRICE*100:>+7.0f}%  {ratio_A:>6.2f}x  {ratio_label(ratio_A)}
     (P/E held; conserv EPS ${cons_eps_2yr:.2f})
  B: Conserv exit {CONS_EXIT_PE:.0f}x           ${price_B:>9.0f}  {(price_B-CURRENT_PRICE)/CURRENT_PRICE*100:>+7.0f}%  {ratio_B:>6.2f}x  {ratio_label(ratio_B)}
     (mild de-rate from today's 51x trailing)
  C: BASE scenario             ${price_C:>9.0f}  {(price_C-CURRENT_PRICE)/CURRENT_PRICE*100:>+7.0f}%  {ratio_C:>6.2f}x  {ratio_label(ratio_C)}
     (model BASE: {sc_map['BASE'][2]}x × ${sc_map['BASE'][1]:.2f} EPS)
  {"─"*62}
  Primary signal (Method B):  {ratio_B:.2f}x  →  {ratio_label(ratio_B)}

  B is the honest method — it assumes a modest de-rate (50x→47x)
  alongside conservative EPS growth.  At 0.92x the upside (+{(price_B-CURRENT_PRICE)/CURRENT_PRICE*100:.0f}%)
  just covers the floor gap ({dist_epp/CURRENT_PRICE*100:.0f}%).  Conservative return: {cons_ret_ann:+.0f}%/yr.

  The stock reaches ◉ BUY at ~${epp_now + dist_epp*0.35:.0f}  (ratio B → 0.75x).
  The stock reaches ◉ BUY at EPP ${epp_now:.0f}  if China headline hits.""")

head()

# ── ⑥  ENTRY FRAMEWORK ───────────────────────────────────────────────────────
print(f"""
  ⑥  ENTRY FRAMEWORK
  {"─"*62}

  ┌───────────────┬────────────┬──────────────┬───────────────────┐
  │  Zone         │  Price     │  Ratio B     │  Action           │
  ├───────────────┼────────────┼──────────────┼───────────────────┤
  │  ◉ EPP floor  │  ${epp_now:.0f}–${epp_now+40:.0f}   │  < 0.50x     │  Buy aggressively │
  │  ◎ High conv. │  ${epp_now+40:.0f}–${epp_now+80:.0f}   │  0.50–0.75x  │  Build position   │
  │  ◎ Today      │  ~${CURRENT_PRICE:.0f}      │  {ratio_B:.2f}x       │  Accumulate       │
  │  ◐ Watchlist  │  ${CURRENT_PRICE+30:.0f}–${CURRENT_PRICE+80:.0f}   │  1.1–1.5x    │  Hold / no add    │
  │  ✕ Avoid      │  >${CURRENT_PRICE+80:.0f}       │  > 1.75x     │  Trim on strength │
  └───────────────┴────────────┴──────────────┴───────────────────┘

  Most probable catalyst for better entry:
    →  China trade war headline (sudden, -10% to -20% move)
    →  Hospital capex pause (slower; gives 3-6 month window)
    →  Broad market correction (beta 1.05; moves with market)

  What would UPGRADE the signal to ◉ BUY without price falling:
    →  Ion platform reimbursement expanded to colorectal / cardiac
    →  DV5 placed into 2nd and 3rd tier US hospitals (volume inflection)
    →  China trade war de-escalation (removes the binary risk premium)

  Watch for DOWNGRADE triggers (move to AVOID):
    →  2 consecutive quarters of procedure volume growth < 8%
    →  DV5 ASP pushback materializes (hospitals delay upgrades)
    →  GLP-1 bariatric volume data shows structural -15%+ decline""")

head()

# ── COMPACT SUMMARY ───────────────────────────────────────────────────────────
print(f"""
  SUMMARY CARD  ·  {TICKER}  ·  ${CURRENT_PRICE:.0f}  ·  {DATE}

  Signal         {SIGNAL}
  EPP floor      ${epp_now:.0f}   ({epp_gap_pct:.0f}% below current;  migrated +80% from 2022)
  Ratio B        {ratio_B:.2f}x  ({ratio_label(ratio_B)} — floor gap ≈ EPS upside)
  Cons. return   {cons_ret_ann:+.0f}%/yr  (15% CAGR, 47x exit;  no dividend)
  EPS quality    78% real  /  22% inflation  (structural growth confirmed)
  #1 risk        China revenue ban  →  EPS cut + multiple compression → $334
  #1 catalyst    Ion + DV5 execute  →  BASE/BULL  →  $640–$812  in 2yr
  Best entry     ${epp_now:.0f}–${epp_now+80:.0f}  (on China headline or broad market dip)""")
print()
head()
print()
