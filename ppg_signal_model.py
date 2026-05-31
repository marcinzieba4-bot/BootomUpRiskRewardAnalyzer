"""
PPG  ·  PPG Industries, Inc.  ·  NYSE: PPG
Bottom-up signal model  ·  Paints, Coatings & Specialty Materials
Date: 2026-05-31
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "PPG"
COMPANY       = "PPG Industries, Inc."
SECTOR        = "Paints & Coatings · Performance Coatings · Industrial Coatings · NYSE: PPG"
CURRENT_PRICE = 108.50       # USD; as of 2026-05-31
VOL_52W_LOW   = 86.20        # Oct 2025 trough (tariff fears + China property concerns)
VOL_52W_HIGH  = 131.50       # Jul 2025 high (pre-tariff rally + raw material tailwind)
SHARES_OUT_M  = 232.0        # millions (post-buyback)

# Annual dividend: 54 consecutive annual increases (Dividend Aristocrat since 1970)
ANNUAL_DIV    = 2.68         # $/share FY2026

# ── SEGMENT MARGIN RECOVERY (company-specific calculator constants) ────────────
# Two segments: Performance Coatings (~$9B) and Industrial Coatings (~$7B)
PERF_REVENUE_B   = 9.0       # Performance Coatings revenue ($B): auto refinish, aerospace, arch Americas
PERF_OI_CURRENT  = 0.150     # current adj operating income margin  (15.0%)
PERF_OI_TARGET   = 0.185     # through-cycle target margin          (18.5%)

IND_REVENUE_B    = 7.0       # Industrial Coatings revenue ($B): auto OEM, packaging, specialty
IND_OI_CURRENT   = 0.110     # current adj OI margin                (11.0%)
IND_OI_TARGET    = 0.145     # through-cycle target margin          (14.5%)

TAX_RATE         = 0.23
PE_RECOVERY      = 14        # re-rating multiple at through-cycle margins

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS       = 8.00    # FY2026E adj EPS estimate
PE_TROUGH     = 12      # min viable P/E for diversified coatings at trough (historical floor)
EPP           = round(EPP_EPS * PE_TROUGH, 0)   # $96

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
# (adj_eps, pe_multiple, price, narrative)
SCENARIOS = {
    "BEAR":  (5.50, 10,  55,  "Industrial recession + China collapse; EPS $5.50 → 10× trough P/E"),
    "BASE":  (8.00, 14, 112,  "Modest recovery; Boeing 40/month; EPS $8.00 → 14× mid-cycle P/E"),
    "BULL":  (9.75, 17, 166,  "Full recovery; Boeing 50+/month; China stable; $9.75 → 17× normalised"),
    "XBULL": (11.50,20, 230,  "Cycle peak + China rebound + M&A premium; $11.50 → 20× historical peak"),
}

# ── SOFTMAX PROBABILITY FUNCTION ─────────────────────────────────────────────
# P(s|c) ∝ exp(-|c − center_s| / T);  T = 0.60
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
    target = price * (1.15 ** 2)          # 2-yr 15% hurdle
    lo, hi = 1.0, 4.0
    for _ in range(80):
        m = (lo + hi) / 2
        (lo if expected_value(m) < target else (lo := m) or lo) if False else None
        if expected_value(m) < target:
            lo = m
        else:
            hi = m
    return round((lo + hi) / 2, 2)

# ── 6 PROXY SIGNALS ───────────────────────────────────────────────────────────
# Scores: 1=BEAR  2=BASE  3=BULL  4=XBULL
SIGNALS = [
    {
        "name":       "Industrial Coatings volume — YoY (auto OEM + general industrial)",
        "weight":     0.25,
        "thresholds": ("<−3%",   "≥−1%",  "≥+4%",   "≥+8%"),
        "now":        "+1%",
        "score":      2,
        "comment":    "Auto OEM flat globally; packaging +3%; general industrial recovering from 2025 trough",
    },
    {
        "name":       "Boeing 737 Max monthly deliveries",
        "weight":     0.25,
        "thresholds": ("<25",    "≥32",   "≥38",    "≥55"),
        "now":        "40/mo",
        "score":      3,
        "comment":    "Post-machinist strike recovery; FAA approved 38 rate; tracking toward 42 target",
    },
    {
        "name":       "Raw material cost basket (TiO₂ + resins) — YoY change",
        "weight":     0.20,
        "thresholds": (">+10%",  "≤+3%",  "≤−3%",   "≤−8%"),
        "now":        "−4%",
        "score":      3,
        "comment":    "TiO₂ −5% YoY; petrochemical resins −2%; ~$200M gross margin tailwind",
    },
    {
        "name":       "China coatings volume — architectural + industrial YoY",
        "weight":     0.15,
        "thresholds": ("<−4%",   "≥−2%",  "≥+3%",   "≥+8%"),
        "now":        "−6%",
        "score":      1,
        "comment":    "Residential −8% (structural real estate); industrial offsets partially; ~15% of rev",
    },
    {
        "name":       "Transform 2024+ restructuring — annualised savings ($M)",
        "weight":     0.10,
        "thresholds": ("<$75M",  "≥$125M","≥$160M", "≥$200M"),
        "now":        "$165M",
        "score":      3,
        "comment":    "94% of $175M target delivered; headcount −1,800; plant consolidations complete",
    },
    {
        "name":       "Organic pricing realisation — blended YoY",
        "weight":     0.05,
        "thresholds": ("<−2%",   "≥0%",   "≥+2%",   "≥+4%"),
        "now":        "+0.5%",
        "score":      2,
        "comment":    "Performance +1% offset by Industrial flat; raw tailwind reduces pricing urgency",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Aerospace coatings moat — 7-10yr qualification approval cycles lock revenue; zero substitution",  +0.6, 0.20),
    ("+", "54-yr Dividend Aristocrat — FCF discipline & management quality; 2.5% yield floor signal",        +0.3, 0.15),
    ("-", "China structural headwind — residential real estate structural not cyclical; ~15% of group rev",  -0.5, 0.25),
    ("-", "Boeing production concentration risk — PPG on all Boeing platforms; strike/quality tail risk",    -0.3, 0.20),
    ("+", "M&A optionality — disciplined acquirer (Tikkurila $1.6B, Comex $2.3B); IG balance sheet",        +0.4, 0.20),
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
    valuation_label = "MODESTLY OVERVALUED"

# ── RATIO B (signal determination) ───────────────────────────────────────────
bear_price = SCENARIOS["BEAR"][2]
bull_price = SCENARIOS["BULL"][2]
downside_pct = (CURRENT_PRICE - bear_price) / CURRENT_PRICE
upside_pct   = (bull_price - CURRENT_PRICE) / CURRENT_PRICE
ratio_b      = round(downside_pct / upside_pct, 2)

if ratio_b < 0.75:
    signal_short, signal_full = "BUY",       "◉ BUY"
elif ratio_b < 1.10:
    signal_short, signal_full = "ACCUMULATE","◎ ACCUMULATE"
elif ratio_b < 1.75:
    signal_short, signal_full = "WATCHLIST", "◐ WATCHLIST"
else:
    signal_short, signal_full = "AVOID",     "✕ AVOID"

# ── CONSERVATIVE GROWTH (2-yr) ────────────────────────────────────────────────
CONS_EPS_2YR = 7.50    # conservative FY2028E: modest recovery, China headwind persists
CONS_PE_2YR  = 13      # cautious multiple for slow industrial recovery
cons_equity  = CONS_EPS_2YR * CONS_PE_2YR
cons_divs    = ANNUAL_DIV * 2
cons_total   = cons_equity + cons_divs
cons_return  = round((cons_total - CURRENT_PRICE) / CURRENT_PRICE * 100, 1)
cons_annual  = round(cons_return / 2, 1)

# ─────────────────────────────────────────────────────────────────────────────
#  OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
W = 72

def hr(): print("  " + "─" * W)
def bar(score):
    filled = "█" * score + "░" * (4 - score)
    return filled

print()
print("═" * (W + 4))
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Paints & Coatings / Materials")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT MARGIN RECOVERY BRIDGE ────────────────────────────────────────
print()
print("  SEGMENT MARGIN RECOVERY BRIDGE  (adj OI margin: current → through-cycle target)")
hr()

perf_oi_curr  = PERF_REVENUE_B * PERF_OI_CURRENT * 1000   # $M
perf_oi_tgt   = PERF_REVENUE_B * PERF_OI_TARGET  * 1000
perf_delta    = perf_oi_tgt - perf_oi_curr

ind_oi_curr   = IND_REVENUE_B  * IND_OI_CURRENT  * 1000
ind_oi_tgt    = IND_REVENUE_B  * IND_OI_TARGET   * 1000
ind_delta     = ind_oi_tgt - ind_oi_curr

total_curr    = perf_oi_curr + ind_oi_curr
total_tgt     = perf_oi_tgt  + ind_oi_tgt
total_delta   = total_tgt - total_curr

# EPS uplift from margin recovery
delta_ni      = total_delta * (1 - TAX_RATE)          # $M after tax
delta_eps     = delta_ni / SHARES_OUT_M                # $/share
delta_price   = round(delta_eps * PE_RECOVERY, 1)     # implied stock price uplift

print(f"  {'Segment':<35}  {'Revenue':>8}  {'Curr OI%':>9}  {'Tgt OI%':>9}  {'Δ OI ($M)':>10}")
hr()
print(f"  {'Performance Coatings':<35}  ${PERF_REVENUE_B:.1f}B     {PERF_OI_CURRENT*100:.1f}%       {PERF_OI_TARGET*100:.1f}%       +${perf_delta:.0f}M")
print(f"    Sub-segments: Auto Refinish 25% · Aerospace 12% · Architectural Americas 19%")
print(f"  {'Industrial Coatings':<35}  ${IND_REVENUE_B:.1f}B     {IND_OI_CURRENT*100:.1f}%       {IND_OI_TARGET*100:.1f}%       +${ind_delta:.0f}M")
print(f"    Sub-segments: Auto OEM 20% · Packaging 10% · Specialty Industrial 14%")
hr()
print(f"  {'TOTAL':<35}  $16.0B    {total_curr/16000*100:.1f}%       {total_tgt/16000*100:.1f}%       +${total_delta:.0f}M")
print()
print(f"  Through-cycle margin recovery implies:")
print(f"    Incremental adj OI:  +${total_delta:.0f}M")
print(f"    After-tax uplift:    +${delta_ni:.0f}M  ({TAX_RATE*100:.0f}% tax rate)")
print(f"    EPS uplift:          +${delta_eps:.2f}/share  (÷ {SHARES_OUT_M:.0f}M shares)")
print(f"    At {PE_RECOVERY}× P/E:          +${delta_price:.0f}/share  ← bridge to BULL scenario (${bull_price})")
print()
print(f"  KEY DRIVER: Every 100bp margin improvement across the group = +${16000*0.01*(1-TAX_RATE)/SHARES_OUT_M:.2f}/EPS")
print(f"  = +${16000*0.01*(1-TAX_RATE)/SHARES_OUT_M*PE_RECOVERY:.1f}/share at {PE_RECOVERY}× P/E")
print(f"  Boeing at 50/month (BULL threshold) = ~$400M aerospace rev uplift = ~+$1.30/EPS = +${1.30*PE_RECOVERY:.0f}/share")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>5}  {'BASE':>6}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>6}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>5}  {ths[1]:>6}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>6}  {lbl}  {b}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15% hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.2f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:72]:<72}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.2f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print("  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${:.0f})".format(bear_price))
hr()
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>7}  Trigger")
hr()
bear_triggers = [
    ("Industrial Coatings volume — YoY",                      "+1%",    "<−3%",   "−4pp",   "US/EU mfg recession; auto OEM destocks…"),
    ("Boeing 737 Max monthly deliveries",                      "40/mo",  "<25",    "−15",    "New strike / FAA grounding / quality cr…"),
    ("Raw material costs — TiO₂ + resins basket",             "−4%",    ">+10%",  "+14pp",  "China TiO₂ capacity curtailed; energy s…"),
    ("China coatings volume — arch + industrial",              "−6%",    "<−4%↓", "−2pp",   "Further property market deterioration…"),
    ("Transform 2024+ savings — annualised",                   "$165M",  "<$75M",  "−$90M",  "Programme reversal; new management scra…"),
    ("Organic pricing — blended",                              "+0.5%",  "<−2%",   "−2.5pp", "Volume collapse forces price war; raw …"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Global manufacturing recession (PMI <45 sustained 3+ quarters) collapses")
print(f"  auto OEM volumes (20% of PPG rev) simultaneously with China property worsening. Boeing")
print(f"  faces a new FAA grounding or labour dispute that halts deliveries. Raw material costs")
print(f"  reverse on supply disruption. EPS falls to $5.50; at 10× trough P/E = ${bear_price} (−{downside_pct*100:.0f}%).")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS × min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}")
print(f"  Min viable P/E at trough:      {PE_TROUGH}×  (PPG never traded below 11× at cycle trough)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market +{epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  +{epp_gap_pct:.0f}% premium to EPP → limited downside protection from fundamental floor.")
print(f"  Bear ${bear_price} vs EPP ${EPP:.0f}: stock can fall {((CURRENT_PRICE-bear_price)/CURRENT_PRICE*100):.0f}% before breaching EPP.")
print(f"  EPP rising path: FY2027E EPS ${EPP_EPS+0.75:.2f} × {PE_TROUGH}× = ${(EPP_EPS+0.75)*PE_TROUGH:.0f} EPP by year-end 2027.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: China headwind persists; only partial industrial recovery)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (modest improvement; China still −4%)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (below historical avg of 15-16× for lack of catalysts)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  ({ANNUAL_DIV:.2f} × 2; 54-yr div growth streak assumed)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is SLIGHTLY NEGATIVE — the stock prices in BASE recovery already.")
print(f"  Breakeven requires FY2028E EPS ≥${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f} at {CONS_PE_2YR}× = ~${(CURRENT_PRICE-cons_divs)/CONS_PE_2YR:.1f}/EPS.")
print(f"  Dividend yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}% provides floor income while waiting for cycle turn.")
print(f"  BUY trigger: $86-96 range (EPP zone + 52W low) where 2yr return flips positive.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.28           # 28% realised 2yr volatility
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%  —  54 consecutive annual increases)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (moderate; coatings cycle + FX exposure)")
print(f"  Beta vs S&P 500:      0.85  (below market; chemical cycle, not macro beta)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (within range — last seen Nov 2022 at ${bear_price+5})")
print(f"  → 52W low ${VOL_52W_LOW:.2f} already reflects tariff fears; further drop needs earnings cut.")
print(f"  → Dividend yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}% provides income floor — cut risk low (54 yrs of growth).")
print(f"  → ACCUMULATE range: ${VOL_52W_LOW+2:.0f}–${round(CURRENT_PRICE*1.10,0):.0f}  |  BUY below ${EPP:.0f}  |  TRIM above ${VOL_52W_HIGH:.0f}")

# ─── ⑦ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print()
print("  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
hr()
probs_mkt   = softmax_probs(MARKET_COMPOSITE)
print(f"  {'Scenario':<10}  {'Price':>7}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>7}  Description")
hr()
for s in ["BEAR","BASE","BULL","XBULL"]:
    pp  = probs_proxy[s] * 100
    pm  = probs_mkt[s]   * 100
    gap = pp - pm
    pr  = SCENARIOS[s][2]
    desc = SCENARIOS[s][3][:45]
    print(f"  {s:<10}  ${pr:>6}  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj  = expected_value(ADJ_COMPOSITE)
ev_prx  = expected_value(PROXY_COMPOSITE)
ev_mkt  = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): ${ev_adj:.0f}  /  Proxy EV: ${ev_prx:.0f}  /  Market EV: ${ev_mkt:.0f}  /  Current: ${CURRENT_PRICE:.0f}")
hr()
print(f"  Downside  (→ Bear ${bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull ${bull_price}):    {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b:.2f}x")
print(f"  Signal    :  {signal_full}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) Boeing monthly delivery data → 42/month = BULL threshold for aerospace rev")
print(f"  (2) Q2 2026 industrial volume inflection → China floor or US manufacturing PMI >52")
print(f"  (3) Transform 2024+ full $175M delivery → upgrade to ◎ BUY if + industrial confirms")
print(f"  ACCUMULATE $88–{round(CURRENT_PRICE*1.08,0):.0f}  |  BUY below $96 (EPP zone)  |  AVOID above ${VOL_52W_HIGH:.0f}")
print("═" * (W + 4))
print()

# ── EXPORT (for lambda_function.py import) ────────────────────────────────────
RESULT = {
    "ticker":       TICKER,
    "signal":       signal_full,
    "signal_short": signal_short,
    "price":        CURRENT_PRICE,
    "epp_gap_pct":  epp_gap_pct,
    "ratio_b":      ratio_b,
    "ratio_b_fmt":  f"{ratio_b:.2f}x",
    "adj_composite":ADJ_COMPOSITE,
    "market_composite": MARKET_COMPOSITE,
    "adj_gap":      ADJ_GAP,
    "valuation":    valuation_label,
    "cons_return_2yr": cons_return,
}

if __name__ == "__main__":
    pass
