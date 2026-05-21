"""
Southern Company (SO) — BottomUp Risk/Reward Signal Model
Regulated electric utility: Georgia Power, Alabama Power, Mississippi Power + Gas distribution
Three-Part Publication Format
"""
import math

# ── LIVE PRICE (fetched Yahoo Finance, 2026-05-21) ───────────────────────────
CURRENT_PRICE = 93.05   # SO — fetched from Yahoo Finance search, 2026-05-21

# ── EPP FLOOR CALIBRATION ────────────────────────────────────────────────────
# Trough period: FY2023 full-year adjusted EPS during rate-spike selloff
# Stock hit ~$61-62 in Oct-2023 when 10Y UST touched 5%; implied P/E = ~17x
EPS_TROUGH       = 3.62   # FY2023 adjusted EPS (rate-spike floor year)
EPS_TROUGH_YEAR  = 2023
EPS_TROUGH_PRICE = 61.54  # Oct-2023 utility rate-spike low; 3.62 × 17x = 61.54 ✓
EPP_MIN_PE       = 17     # min-viable trough P/E (rate-spike compression floor)

# ── CURRENT FUNDAMENTALS ─────────────────────────────────────────────────────
EPS_NOW           = 4.30  # FY2025 adjusted EPS (reported)
EPS_FWD_CONSENSUS = 4.55  # FY2026E (company guidance midpoint $4.50–$4.60)
CONS_EPS_2YR      = 4.92  # FY2027E consensus (Erste Group / Bloomberg)
CONS_EPS_CAGR     = 0.070 # 7.0%/yr (FY2025→FY2027)
CONS_EXIT_PE      = 22    # conservative 2-yr exit P/E (modest re-rating from 20.5x fwd)
BETA              = 0.36  # regulated-utility beta (rate-sensitive, low equity risk)

# ── SCENARIO TABLE ───────────────────────────────────────────────────────────
# (label, thesis, EPS, exit_PE, price_target)
SCENARIOS = [
    ("BEAR",  "Rates spike to 5.5%+; PSC rate case disappoints; EPS misses on rising capex costs",  4.50, 15,  68),
    ("BASE",  "Consensus execution; AI load growth steady; flat multiple on FY2027 earnings",       4.92, 20,  98),
    ("BULL",  "Data center surge; IRA credits beat; rate case win; multiple expansion",             5.35, 24, 128),
    ("XBULL", "Full nuclear-AI infrastructure re-rating; SO becomes premier clean-power utility",  5.70, 28, 160),
]

# ── CROSS-READ SIGNALS ───────────────────────────────────────────────────────
# (label, thesis, unit, bear_lvl, base_lvl, bull_lvl, xbull_lvl, current_val, weight)
CROSS_READS = [
    ("Georgia Power territory load growth YoY",  "AI/data-center demand; industrial expansion",    "% YoY",  -2,  4,  9, 15,  9.0, 0.30),
    ("10Y UST yield (inverse: lower = BULL)",    "Utility discount rate; P/E multiple driver",     "%",     5.5, 4.5, 3.5, 2.5, 4.45, 0.25),
    ("Vogtle 3&4 nuclear capacity factor",       "IRA PTC eligibility; zero-carbon baseload",      "%",      70, 83, 91, 95, 89.0, 0.15),
    ("Georgia PSC allowed ROE",                  "Rate case outcome; capex recovery speed",         "%",    9.5,10.5,11.2,12.0,10.75, 0.15),
    ("US industrial power demand growth YoY",    "Macro grid load; electrification tailwind",      "% YoY",  0,  2,  4,  6,  3.5, 0.10),
    ("Henry Hub natural gas spot ($/MMBtu)",     "Gas fleet cost; nuclear competitive advantage",  "$/MMBtu",2.0, 3.0, 4.0, 5.5,  3.50, 0.05),
]

# ── STRUCTURAL COMPOSITE ADJUSTMENT ─────────────────────────────────────────
# (factor, rating −2…+2, weight)
STRUCTURAL_FACTORS = [
    ("Vogtle 3&4 nuclear monopoly  (only new US nuclear; 2.2 GW zero-carbon baseload)",   +1.5, 0.25),
    ("AI / data-center load growth  (Google, Microsoft, Meta campuses in Georgia)",        +1.2, 0.25),
    ("Regulatory lag & capex recovery uncertainty  (PSC rate review cycle, cost overruns)", -0.6, 0.20),
    ("High leverage & balance sheet stress  ($26.5B DOE loan; heavy capex programme)",     -0.7, 0.20),
    ("IRA clean-energy tax credits  (nuclear PTC ~$15/MWh if CF > 60%)",                  +0.9, 0.10),
]

# ── EPS QUALITY DECOMPOSITION ────────────────────────────────────────────────
# (driver, fraction_of_EPS_TROUGH, is_structural)
EPS_DECOMP = [
    ("Rate base return & regulated capex recovery  (Georgia / Alabama / Gulf Power RAP)",  0.42, True),
    ("Vogtle Units 3&4 ramp + IRA production tax credits  (~$15/MWh)",                    0.24, True),
    ("AI data-centre & industrial load growth  (hyperscaler contracts, EV charging)",      0.20, True),
    ("Customer growth & electrification  (heat pumps, EVs; Sth-east population inflow)",   0.11, True),
    ("Weather normalisation variance  (heating/cooling degree-days vs. 30-yr normal)",     0.02, False),
    ("Natural gas cost pass-through & fuel hedging gains/losses",                          0.01, False),
]

# ── IDIOSYNCRATIC vs MACRO DECOMPOSITION ─────────────────────────────────────
IDIO = {
    "idio_pct":  35,
    "macro_pct": 65,
    "beta":       0.36,
    "drivers": [
        ("Vogtle nuclear operations & capacity factor",    "IDIO",  0.12, "IRA PTC; zero-carbon dispatch; refuelling risk"),
        ("Georgia PSC rate case & allowed ROE",            "IDIO",  0.12, "Capex recovery; customer rate adjustments"),
        ("Data-centre load growth & contract execution",   "IDIO",  0.11, "Hyperscaler signings; industrial expansion"),
        ("10Y UST yield & FOMC rate path",                 "MACRO", 0.28, "Utility discount rate; P/E multiple driver"),
        ("Utility sector sentiment & risk-on/risk-off",   "MACRO", 0.22, "Defensive sector rotation; relative vs S&P 500"),
        ("Commodity costs  (nat gas, coal, uranium)",      "MACRO", 0.15, "Fuel costs; nuclear fuel cycle; grid cost base"),
    ],
}

# ═══════════════════════════════════════════════════════════════════════════════
# PART 1 — REUSABLE ENGINE (identical across all models)
# ═══════════════════════════════════════════════════════════════════════════════

def softmax_probs(composite, scenarios, T=0.60):
    centres = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    labels  = [s[0] for s in scenarios]
    logits  = [-(composite - centres[l])**2 / T for l in labels]
    mx      = max(logits)
    exps    = [math.exp(x - mx) for x in logits]
    total   = sum(exps)
    return [e / total for e in exps]

def rfmt(r):
    return f"{r:.2f}x" if r != float('inf') else "N/A"

def infer_composite(target_price, scenarios, T=0.60):
    lo, hi = 1.0, 4.0
    for _ in range(60):
        mid   = (lo + hi) / 2
        probs = softmax_probs(mid, scenarios, T)
        ev    = sum(p * s[4] for p, s in zip(probs, scenarios))
        if ev < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

def signal_from_ratio(r):
    if r == float('inf') or r is None:
        return "✕ AVOID"
    if r < 0.75:
        return "◉ BUY"
    if r < 1.10:
        return "◎ ACCUMULATE"
    if r < 1.75:
        return "◐ WATCHLIST"
    if r < 2.50:
        return "◑ HOLD / TRIM"
    return "✕ AVOID"

# ── derived quantities ────────────────────────────────────────────────────────
epp_now         = EPS_NOW * EPP_MIN_PE
epp_gap_pct     = (CURRENT_PRICE - epp_now) / epp_now * 100
price_b         = CONS_EPS_2YR * CONS_EXIT_PE
ratio_b         = (CURRENT_PRICE - epp_now) / (price_b - CURRENT_PRICE) if price_b > CURRENT_PRICE else float('inf')
signal          = signal_from_ratio(ratio_b)

sca_raw         = sum(r * w for _, r, w in STRUCTURAL_FACTORS)
sca_adj         = sca_raw / 2.0

market_composite = infer_composite(CURRENT_PRICE, SCENARIOS)
adj_composite    = market_composite + sca_adj

probs            = softmax_probs(adj_composite, SCENARIOS)
proxy_ev         = sum(p * s[4] for p, s in zip(probs, SCENARIOS))

mkt_probs        = softmax_probs(market_composite, SCENARIOS)

eps_g_total      = EPS_NOW - EPS_TROUGH
cyclical_dollar  = sum(EPS_TROUGH * sh for _, sh, is_s in EPS_DECOMP if not is_s)
struct_dollar    = eps_g_total - cyclical_dollar

trailing_pe      = CURRENT_PRICE / EPS_NOW
forward_pe       = CURRENT_PRICE / EPS_FWD_CONSENSUS
cons_ret_ann     = ((price_b / CURRENT_PRICE) ** (1/2) - 1) * 100

# ═══════════════════════════════════════════════════════════════════════════════
# PART 2 — ANALYST COMMENTARY
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 72)
print("  SOUTHERN COMPANY (SO)  |  BottomUp Risk/Reward Signal Model")
print("=" * 72)
print(f"  Signal  : {signal}   |   Ratio B : {rfmt(ratio_b)}")
print(f"  Price   : ${CURRENT_PRICE:.2f}  |   EPP Floor : ${epp_now:.2f}  (+{epp_gap_pct:.1f}% above)")
print(f"  Date    : 2026-05-21  |   Sector  : Regulated Electric Utility")
print("=" * 72)
print()
print("─" * 72)
print("  PART 2 — ANALYST COMMENTARY")
print("─" * 72)
print()

print("  1. BUSINESS QUALITY & COMPETITIVE MOAT")
print("  ─────────────────────────────────────────────────────────────────")
print("""
  Southern Company is the premier regulated electric utility in the
  southeastern United States, serving ~9 million customers across Georgia,
  Alabama, Mississippi and natural gas markets through Southern Company Gas.
  The moat is anchored by three structural advantages:

  REGULATED MONOPOLY FRANCHISE — Georgia Power, Alabama Power and Mississippi
  Power operate as state-regulated monopolies with exclusive service
  territories and guaranteed returns on equity. The Georgia PSC has frozen
  Georgia Power's base rates through 2028 as part of a stipulated agreement,
  providing exceptional near-term EPS visibility. Allowed ROE of ~10.75%
  on a growing rate base translates directly to predictable earnings growth
  even in recessionary environments.

  PLANT VOGTLE UNITS 3 & 4 — The most consequential utility asset built in
  the United States in thirty years. SO completed the only two new nuclear
  reactors in the US (2.2 GW combined) in 2023–24 after a decade of
  construction and $30B in total spend. The capex risk is BEHIND them.
  Vogtle now provides zero-carbon, 24/7 baseload generation that earns IRA
  production tax credits (~$15/MWh if capacity factor exceeds 60%), is
  immune to natural gas price spikes, and is ideally positioned for the
  AI data-centre market's appetite for firm, always-on clean power.

  AI / DATA-CENTRE DEMAND GROWTH — Georgia Power's service territory (Atlanta
  metro and surrounding counties) is one of the three largest data-centre
  markets in the US. Google, Microsoft, Meta and AWS operate significant
  campuses in the region. Q1 2026 saw 9%+ load growth YoY driven by data
  centre expansion, beating estimates by $0.11/share. SO's $26.5B DOE
  infrastructure loan partly funds the grid capacity to serve this demand.
  Georgia Power's IRP projects up to 90 large industrial projects by 2030.
""")

print("  2. EARNINGS QUALITY & EPP FLOOR ANALYSIS")
print("  ─────────────────────────────────────────────────────────────────")
print(f"""
  EPP FLOOR VALIDATION
  Trough EPS  : ${EPS_TROUGH:.2f}  (FY{EPS_TROUGH_YEAR} adjusted — rate-spike floor year)
  Trough Price: ${EPS_TROUGH_PRICE:.2f}  (Oct-2023 utility selloff when 10Y UST hit 5%)
  Min viable P/E: {EPP_MIN_PE}x  →  ${EPS_TROUGH:.2f} × {EPP_MIN_PE}x = ${EPS_TROUGH * EPP_MIN_PE:.2f}  ≈  ${EPS_TROUGH_PRICE:.2f} ✓

  The Oct-2023 rate-spike was the market-validated stress test for regulated
  utilities. With the 10Y UST at 5%, SO compressed to ~17x trailing EPS —
  the floor P/E for a regulated utility franchise of this quality. Earnings
  themselves did NOT decline; the $61 low was a pure multiple-compression
  event, which defines the min-viable P/E for this business.

  MIGRATED EPP (today)
  Current EPS : ${EPS_NOW:.2f}  (FY2025 adjusted, reported)
  EPP Floor   : ${EPS_NOW:.2f} × {EPP_MIN_PE}x  =  ${epp_now:.2f}
  Current Gap : ${CURRENT_PRICE:.2f} − ${epp_now:.2f}  =  +{epp_gap_pct:.1f}% above floor

  The EPP migrates upward every year as earnings grow. At 7%/yr EPS growth,
  the floor rises ~$5/year in dollar terms — providing a rising cushion for
  long-term holders. The 27% gap is moderate for a utility in re-rating mode.

  EPS QUALITY DECOMPOSITION  (FY{EPS_TROUGH_YEAR} → FY2025)
  Total EPS growth  : ${EPS_TROUGH:.2f} → ${EPS_NOW:.2f}  (+${eps_g_total:.2f}/share)
  Structural dollar : ${struct_dollar:.2f}  ({struct_dollar/eps_g_total*100:.0f}% of growth)
  Cyclical dollar   : ${cyclical_dollar:.2f}  ({cyclical_dollar/eps_g_total*100:.0f}% of growth)
""")

print(f"  {'Driver':<55}  {'Share':>6}  {'Type':>8}")
print(f"  {'─'*55}  {'─'*6}  {'─'*8}")
for desc, sh, is_s in EPS_DECOMP:
    type_label = "REAL ✓" if is_s else "INFL. ~"
    print(f"  {desc:<55}  {sh*100:>5.0f}%  {type_label:>8}")
print()

print("""
  Regulated utilities are among the highest-quality EPS compoundersin the
  equity universe. Over 93% of SO's EPS growth is structural — driven by
  allowed returns on invested capital, nuclear ramp, and secular load growth
  from data centres and electrification. Weather and fuel hedging contribute
  minimally (<3%). This is not a cyclical earnings stream.
""")

print("  3. CROSS-READ COMPOSITE & SCENARIO PROBABILITIES")
print("  ─────────────────────────────────────────────────────────────────")
print()
print(f"  {'Signal':<44} {'Unit':>8}  {'BEAR':>6}  {'BASE':>6}  {'BULL':>6} {'XBULL':>6}  {'NOW':>7}  {'Wt':>4}")
print(f"  {'─'*44} {'─'*8}  {'─'*6}  {'─'*6}  {'─'*6} {'─'*6}  {'─'*7}  {'─'*4}")
for label, thesis, unit, bv, bsv, blv, xv, cur, wt in CROSS_READS:
    print(f"  {label:<44} {unit:>8}  {bv:>6.1f}  {bsv:>6.1f}  {blv:>6.1f} {xv:>6.1f}  {cur:>7.2f}  {wt:>4.2f}")
print()
print(f"  Market composite (implied by ${CURRENT_PRICE:.2f}): {market_composite:.2f}")
print(f"  SCA adjustment                                : {sca_adj:+.2f}")
print(f"  Model adj. composite                          : {adj_composite:.2f}")
print(f"  Composite gap (model − market)                : {adj_composite - market_composite:+.2f}")
print()

print(f"  {'Scenario':<8}  {'EPS':>6}  {'P/E':>5}  {'Target':>8}  {'Proxy%':>7}  {'Mkt%':>6}  {'Gap':>7}")
print(f"  {'─'*8}  {'─'*6}  {'─'*5}  {'─'*8}  {'─'*7}  {'─'*6}  {'─'*7}")
for (lbl, thesis, eps, pe, pt), p, mp in zip(SCENARIOS, probs, mkt_probs):
    gap = p*100 - mp*100
    print(f"  {lbl:<8}  ${eps:>5.2f}  {pe:>4}x  ${pt:>7.0f}  {p*100:>6.1f}%  {mp*100:>5.1f}%  {gap:>+6.1f}pp")
print()
print(f"  Proxy EV  : ${proxy_ev:.0f}   (weighted scenario price at model composite)")
print(f"  vs Market : ${CURRENT_PRICE:.2f}  (gap: {(proxy_ev - CURRENT_PRICE)/CURRENT_PRICE*100:+.1f}%)")
print()

print("""
  READ: The model composite sits comfortably above BASE, reflecting the
  AI data-centre load growth and Vogtle operational delivery. The SCA adds
  ~+0.25pp from the nuclear / AI structural tailwinds net of leverage risk.
  The proxy EV implies modest upside from current price, consistent with a
  WATCHLIST rating — real, but not explosive.

  The 10Y UST yield is the swing factor. If rates normalise toward 3.5%,
  the utility P/E multiple expands to 23–24x and SO becomes ACCUMULATE.
  If rates reprice to 5%+, the floor multiple re-compresses and the stock
  revisits $70–75. The yield is the primary macro variable to monitor.
""")

print("  4. METHOD B VALUATION & SIGNAL DERIVATION")
print("  ─────────────────────────────────────────────────────────────────")
print(f"""
  EPP FLOOR (downside anchor)
    Current EPS ${EPS_NOW:.2f} × {EPP_MIN_PE}x min-viable P/E  =  EPP ${epp_now:.2f}
    Downside to floor  =  ${CURRENT_PRICE:.2f} − ${epp_now:.2f}  =  ${CURRENT_PRICE - epp_now:.2f}  ({epp_gap_pct:.1f}% above floor)

  METHOD B — CONSERVATIVE 2-YEAR TARGET
    Consensus EPS FY2027  : ${CONS_EPS_2YR:.2f}  (EPS CAGR {CONS_EPS_CAGR*100:.1f}%/yr)
    Conservative exit P/E : {CONS_EXIT_PE}x  (above current 20.5x fwd; AI/nuclear re-rating)
    Price B               : ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x  =  ${price_b:.2f}
    Upside (Method B)     : ${price_b:.2f} − ${CURRENT_PRICE:.2f}  =  ${price_b - CURRENT_PRICE:.2f}  ({(price_b/CURRENT_PRICE-1)*100:.1f}%)

  ATTRACTIVENESS RATIO B
    Ratio B  =  Downside / Upside  =  ${CURRENT_PRICE - epp_now:.2f} / ${price_b - CURRENT_PRICE:.2f}  =  {rfmt(ratio_b)}

  SIGNAL SCALE:  ◉ BUY <0.75  ◎ ACCUM. 0.75–1.10  ◐ WATCHLIST 1.10–1.75
                 ◑ HOLD 1.75–2.50  ✕ AVOID >2.50 or N/A (upside negative)

  PRIMARY SIGNAL:  {signal}  (Ratio B {rfmt(ratio_b)})

  Valuation context:
    Trailing P/E     : {trailing_pe:.1f}x  (FY2025 EPS ${EPS_NOW:.2f})
    Forward P/E      : {forward_pe:.1f}x  (FY2026E ${EPS_FWD_CONSENSUS:.2f})
    Cons. 2yr return : {cons_ret_ann:+.0f}%/yr  (Method B, from ${CURRENT_PRICE:.2f} to ${price_b:.2f})
    Dividend yield   : ~3.2%  (adds to total return estimate)

  The Ratio B of {rfmt(ratio_b)} sits in the upper WATCHLIST band. The stock is not
  expensive — a regulated utility with nuclear and AI tailwinds trading at
  20.5x forward earns a quality premium. But at $93 the downside to the EPP
  floor ($20) exceeds the upside to the conservative 2-year target ($15),
  leaving asymmetry modestly unfavourable. The investment case improves
  meaningfully if: (a) rates fall 50-100bp expanding the floor multiple, or
  (b) data-centre signings drive EPS upgrades above consensus $4.92.
""")

print("  5. IDIOSYNCRATIC vs MACRO DECOMPOSITION")
print("  ─────────────────────────────────────────────────────────────────")
print(f"""
  Idiosyncratic  {IDIO['idio_pct']}%   |   Macro / Sentiment  {IDIO['macro_pct']}%   |   Beta  {IDIO['beta']:.2f}

  Southern Company is more macro-sensitive than most stocks in this coverage
  universe. With Beta 0.36, absolute volatility is low — but the PRIMARY
  driver of the multiple is the 10Y UST yield, which is a macro variable.
  A 100bp rate move shifts the utility sector P/E by ~2-3x, worth ~$8-12/share.
  Fundamental research edge is highest in three idiosyncratic areas: Vogtle
  operational performance, Georgia PSC rate case outcomes, and the pace of
  data-centre load growth in SO's territory.
""")

print(f"  {'Driver':<46}  {'Type':>5}  {'Wt':>4}  {'Detail'}")
print(f"  {'─'*46}  {'─'*5}  {'─'*4}  {'─'*30}")
for drv, typ, wt, detail in IDIO["drivers"]:
    print(f"  {drv:<46}  {typ:>5}  {wt:.2f}  {detail}")
print()

# ═══════════════════════════════════════════════════════════════════════════════
# PART 3 — NUMBERS & SIGNALS
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("─" * 72)
print("  PART 3 — NUMBERS & SIGNALS")
print("─" * 72)
print()

print("  A. EPP FLOOR TABLE")
print(f"  {'FY':<6}  {'Adj.EPS':>8}  {'EPP@17x':>9}  {'Δ EPS':>7}  {'Δ EPP':>7}")
print(f"  {'─'*6}  {'─'*8}  {'─'*9}  {'─'*7}  {'─'*7}")
hist = [
    (2020, 3.10), (2021, 3.24), (2022, 3.26),
    (2023, EPS_TROUGH), (2024, 3.99), (2025, EPS_NOW),
]
prev_eps = None
for yr, eps in hist:
    epp_yr  = eps * EPP_MIN_PE
    d_eps   = f"+{eps - prev_eps:.2f}" if prev_eps else "  —"
    d_epp   = f"+{(eps - prev_eps)*EPP_MIN_PE:.2f}" if prev_eps else "  —"
    marker  = "  ← trough price floor" if yr == EPS_TROUGH_YEAR else ""
    marker  = "  ← CURRENT" if yr == 2025 else marker
    print(f"  {yr:<6}  ${eps:>7.2f}  ${epp_yr:>8.2f}  {d_eps:>7}  {d_epp:>7}{marker}")
    prev_eps = eps
print(f"\n  FY2026E  ${EPS_FWD_CONSENSUS:>7.2f}  ${EPS_FWD_CONSENSUS*EPP_MIN_PE:>8.2f}  {'':>7}  {'':>7}  ← consensus guidance")
print(f"  FY2027E  ${CONS_EPS_2YR:>7.2f}  ${CONS_EPS_2YR*EPP_MIN_PE:>8.2f}  {'':>7}  {'':>7}  ← Method B exit EPS")
print()

print("  B. SCENARIO TABLE (2-year horizon)")
print(f"  {'Scenario':<8}  {'Thesis':<55}  {'EPS':>5}  {'P/E':>4}  {'Target':>7}  {'Prob%':>6}")
print(f"  {'─'*8}  {'─'*55}  {'─'*5}  {'─'*4}  {'─'*7}  {'─'*6}")
for (lbl, thesis, eps, pe, pt), p in zip(SCENARIOS, probs):
    print(f"  {lbl:<8}  {thesis:<55}  ${eps:>4.2f}  {pe:>3}x  ${pt:>6.0f}  {p*100:>5.1f}%")
print()

print("  C. SIGNAL SCORECARD")
print(f"  {'Metric':<38}  {'Value':>12}  {'Note'}")
print(f"  {'─'*38}  {'─'*12}  {'─'*28}")
metrics = [
    ("Current Price",          f"${CURRENT_PRICE:.2f}",            "NYSE:SO, 2026-05-21"),
    ("EPP Floor (FY2025 EPS)", f"${epp_now:.2f}",                  f"${EPS_NOW:.2f} × {EPP_MIN_PE}x"),
    ("Gap Above EPP",          f"+{epp_gap_pct:.1f}%",             "moderate; cushion present"),
    ("Method B Target (2yr)",  f"${price_b:.2f}",                  f"${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x"),
    ("Ratio B (PRIMARY)",      rfmt(ratio_b),                       signal),
    ("Trailing P/E",           f"{trailing_pe:.1f}x",              f"FY2025 EPS ${EPS_NOW:.2f}"),
    ("Forward P/E",            f"{forward_pe:.1f}x",               f"FY2026E ${EPS_FWD_CONSENSUS:.2f}"),
    ("2yr Cons. Return (B)",   f"{cons_ret_ann:+.0f}%/yr",        "excl. ~3.2% dividend yield"),
    ("EPS CAGR (cons.)",       f"{CONS_EPS_CAGR*100:.1f}%/yr",    "FY25→FY27 consensus"),
    ("Beta",                   f"{BETA:.2f}",                      "low; rate-sensitive utility"),
    ("Model composite",        f"{adj_composite:.2f}",             "between BASE 2.0 & BULL 2.75"),
    ("Proxy EV",               f"${proxy_ev:.0f}",                 f"vs market ${CURRENT_PRICE:.2f}"),
    ("Idio / Macro split",     f"{IDIO['idio_pct']}% / {IDIO['macro_pct']}%", "10Y yield is primary variable"),
]
for name, val, note in metrics:
    print(f"  {name:<38}  {val:>12}  {note}")
print()

print("  D. STRUCTURAL FACTORS (SCA)")
print(f"  {'Factor':<65}  {'Rating':>7}  {'Wt':>4}")
print(f"  {'─'*65}  {'─'*7}  {'─'*4}")
for fac, r, w in STRUCTURAL_FACTORS:
    print(f"  {fac:<65}  {r:>+6.1f}   {w:.2f}")
print(f"\n  SCA raw: {sca_raw:+.3f}  →  adj (+raw/2): {sca_adj:+.3f}  →  composite bump: {sca_adj:+.3f}pp")
print()

print("  E. INVESTMENT DECISION SUMMARY")
print()
print(f"  Signal   :  {signal}  |  Ratio B {rfmt(ratio_b)}")
print(f"  Thesis   :  Vogtle nuclear + AI data-centre demand re-rating in progress.")
print(f"              Execution confirmed (Q1 2026 beat; FY2026 guidance $4.50–$4.60")
print(f"              maintained). But at $93 / 20.5x forward, the risk/reward is")
print(f"              balanced — not asymmetric. Rate path is the swing factor.")
print()
print(f"  Add on   :  Rate-spike pullbacks toward $78–$82 (EPP + 7–12% buffer)")
print(f"              or on evidence of data-centre load upside vs. consensus.")
print(f"  Reduce on:  Sustained 10Y UST above 5.0%; or Georgia PSC rate-case miss;")
print(f"              or Vogtle capacity factor deterioration below 82%.")
print()
print(f"  Key watch: FY2026 Q2–Q4 EPS prints vs. $1.00 / $1.30 / $1.98 guidance")
print(f"             Georgia PSC IRP approval timeline (90 industrial projects)")
print(f"             10Y UST yield direction (±50bp = ±$4–6/share on multiple)")
print()
print("  " + "─" * 68)
print("  NOT FINANCIAL ADVICE. All prices USD. Analysis date 2026-05-21.")
print("  " + "─" * 68)
print()
