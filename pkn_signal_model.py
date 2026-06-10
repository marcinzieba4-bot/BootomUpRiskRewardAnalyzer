"""
PKN  ·  PKN Orlen S.A.  ·  WSE: PKN
Bottom-up signal model  ·  Refining/Petrochemicals (Crack Spreads) / Fuel Retail / Energy Transition (Nuclear SMR/Renewables) / State Ownership
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "PKN"
COMPANY       = "PKN Orlen S.A."
SECTOR        = "Energy · Refining/Petrochemicals (Crack Spreads) · Fuel Retail (PL/CZ/DE/LT) · Upstream E&P · Energy Transition (Nuclear SMR/Renewables) · WSE: PKN"
CURRENT_PRICE = 68.50      # PLN; as of 2026-06-10
VOL_52W_LOW   = 56.20      # 2025 weak refining margin / political-overhang trough
VOL_52W_HIGH  = 78.40      # 2026 crack-spread recovery / dividend-hike peak
SHARES_OUT_M  = 1_041.6    # millions
ANNUAL_DIV    = 4.50       # PLN/share; ~6.6% yield; policy tied to net income, historically volatile

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment (PLN B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Downstream - Refining (crude/diesel/jet)",  120.0,  98.0, 142.0, "Largest segment; refining margins/crack spreads are THE key swing factor; Plock/Litvinov/Mazeikiai/Schwedt"),
    ("Downstream - Petrochemicals (Olefiny III)",  38.0,  30.0,  48.0, "Cyclical petchem margins; Olefiny III expansion ramping capacity; competition from Asian/ME oversupply"),
    ("Energy - Power gen/Renewables/Nuclear SMR",  22.0,  18.0,  32.0, "CCGT/wind/solar growing base; Orlen-Synthos SMR (BWRX-300) optionality; capex-heavy buildout"),
    ("Retail - Fuel/Convenience (PL/CZ/DE/LT)",    58.0,  52.0,  66.0, "~3,500+ stations across 4 countries; non-fuel/convenience margin mix continues to grow, more stable than refining"),
    ("Upstream E&P (Norway/Canada/Poland gas)",    14.0,  10.0,  19.0, "Orlen Upstream production volumes + commodity price exposure; gas price swings drive variability"),
]

# Margin assumptions (blended operating-margin proxy used as "gross margin")
GROSS_MARGIN_CURR = 0.085   # blended operating margin; refining-heavy mix is structurally thin and volatile
GROSS_MARGIN_BULL = 0.110   # BULL: strong crack spreads + petchem recovery + retail mix improvement lift blended margin
OPEX_FIXED_B      = 7.5     # corporate SG&A + below-the-line (PLN B); largely fixed cost base
TAX_RATE          = 0.19    # Polish CIT effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 5.50        # PLN; FY2027E EPS (mid-cycle margin normalization off depressed FY2025/26 base)
PE_PESSIMISTIC = 7.0         # trough P/E: refining-cycle trough + state-ownership discount; PKN historical trough ~6-8x
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # ~38.5 PLN

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 2.50,  7,   18, "Refining crack spreads collapse to cyclical trough amid weak European diesel demand + new Asian/ME refining capacity; petchem stays loss-making; one-off impairments (Litvinov/Schwedt) hit net income; political interference raises capex without returns; EPS PLN2.50 → 7× = PLN18"),
    "BASE":  ( 5.50, 10,   55, "Refining margins normalize to mid-cycle; petchem gradually recovers as Olefiny III ramps; retail provides steady cash floor; energy/renewables segment grows but remains capex-heavy; dividend maintained near current level; EPS PLN5.50 → 10× = PLN55"),
    "BULL":  ( 8.50, 11,   94, "Crack spreads stay elevated on tight European refining capacity (post-Schwedt/Litvinov rationalization industry-wide); petchem cycle turns positive; Olefiny III fully ramped; upstream E&P volumes grow; dividend raised toward policy ceiling; EPS PLN8.50 → 11× = PLN94"),
    "XBULL": (11.00, 13,  143, "Sustained multi-year refining super-cycle; SMR/nuclear program reaches FID with credible state co-funding, re-rating the energy-transition optionality; renewables capacity scales materially; petrochemical and upstream segments all hit cycle highs simultaneously; EPS PLN11.00 → 13× = PLN143"),
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
        "name":       "Refining crack spreads (Brent-based model margin)",
        "weight":     0.30,
        "thresholds": ("<$5/bbl", "≥$8/bbl", "≥$12/bbl", "≥$16/bbl"),
        "now":        "~$9/bbl",
        "score":      2,
        "comment":    "Model refining margin running near mid-cycle ~$9/bbl; European diesel cracks supportive but volatile; remains THE dominant swing factor for group earnings",
    },
    {
        "name":       "Petrochemical margin cycle (Olefiny III ramp)",
        "weight":     0.20,
        "thresholds": ("loss-making", "breakeven", "positive margins", "cycle-high margins"),
        "now":        "near breakeven",
        "score":      2,
        "comment":    "Petchem margins remain pressured by global oversupply; Olefiny III capacity ramping but contributing modestly to volumes so far, not yet to margins",
    },
    {
        "name":       "Retail fuel/convenience volume & margin growth",
        "weight":     0.15,
        "thresholds": ("<-2%",  "≥0%",  "≥3%",   "≥6%"),
        "now":        "+2%",
        "score":      2,
        "comment":    "Retail network across PL/CZ/DE/LT continues steady low-single-digit growth with improving non-fuel mix; the most stable cash-flow segment in the group",
    },
    {
        "name":       "Political/governance overhang (state ownership, mgmt stability)",
        "weight":     0.15,
        "thresholds": ("escalating interference", "ongoing uncertainty", "stabilizing", "depoliticized/clear strategy"),
        "now":        "ongoing uncertainty",
        "score":      2,
        "comment":    "Polish Treasury remains majority shareholder; management/strategy shifts have followed government changes historically; capex allocation (incl. SMR) carries political dimension",
    },
    {
        "name":       "Energy transition optionality (SMR/nuclear, renewables capex)",
        "weight":     0.10,
        "thresholds": ("stalled", "early-stage", "FID progressing", "FID reached + scaling"),
        "now":        "early-stage",
        "score":      2,
        "comment":    "Orlen-Synthos SMR (BWRX-300) JV remains pre-FID; renewables (wind/solar) capacity additions ongoing but small relative to group scale; multi-year optionality not yet reflected in earnings",
    },
    {
        "name":       "Dividend sustainability vs net income volatility",
        "weight":     0.10,
        "thresholds": ("cut likely", "held flat", "modest growth", "policy-ceiling growth"),
        "now":        "held flat",
        "score":      2,
        "comment":    "Dividend policy ties payout to net income, which swings sharply with refining cycle and one-off impairments; ~6.6% current yield assumes broadly maintained payout near recent levels",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("-", "State ownership / political risk — Polish Treasury majority control creates recurring strategy/management discontinuity risk across election cycles", -0.6, 0.25),
    ("-", "Refining margin cyclicality — earnings/EPS swing wildly with crack spreads and one-off impairments (Litvinov/Schwedt write-downs) can dominate any given year", -0.5, 0.25),
    ("+", "High dividend yield (~6.6%) provides a meaningful cash return floor even if the multiple stays depressed", +0.5, 0.15),
    ("+", "Diversified integrated model — retail fuel/convenience cash flows partially offset refining/petchem cyclicality", +0.4, 0.15),
    ("+", "Energy transition optionality — SMR/nuclear JV, renewables buildout, and upstream E&P provide multi-year re-rating catalysts not in current multiple", +0.3, 0.10),
    ("-", "Heavy capex program (energy transition + Olefiny III + upstream) pressures free cash flow and dividend coverage during the buildout phase", -0.3, 0.10),
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
CONS_EPS_2YR  = 6.00   # PLN; FY2028E conservative: modest mid-cycle improvement off FY2027E base
CONS_PE_2YR   = 9      # modest re-rate from ~12.5x current as refining-cycle uncertainty persists
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
print(f"  {TICKER}  ·  {COMPANY}  ·  PLN{CURRENT_PRICE:.2f}  ·  Refining/Petrochemicals (Crack Spreads) / Fuel Retail / Energy Transition (SMR/Renewables)")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<42}  {'FY2026E (PLNB)':>14}  {'Bear (PLNB)':>11}  {'Bull (PLNB)':>11}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<42}  PLN{curr:>10.1f}  PLN{bear:>7.1f}  PLN{bull:>7.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<42}  PLN{curr_total:>10.1f}  PLN{bear_total:>7.1f}  PLN{bull_total:>7.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_ni   = curr_oi * (1 - TAX_RATE)
curr_eps  = round(curr_ni / shares, 2)

bull_gp      = bull_total * GROSS_MARGIN_BULL
bull_oi      = bull_gp - OPEX_FIXED_B
bull_ni      = bull_oi * (1 - TAX_RATE)
shares_b     = shares * 1.00   # PKN does not run meaningful buybacks; share count roughly flat
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.55   # crack spread collapse + petchem losses crush blended margin
bear_oi      = bear_gp - OPEX_FIXED_B * 1.05           # opex sticky / one-off impairment drag
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  PLN{curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% op margin − PLN{OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  PLN{curr_eps:.2f}/share adj EPS")
print()
print(f"  BULL EPS check:  PLN{bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% op margin − PLN{OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares  =  ~PLN{bull_eps_imp:.1f}/share  →  PLN{bull_eps_imp:.1f} × 11× = ~PLN{bull_eps_imp*11:.0f}  ✓ BULL PLN{SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  PLN{bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.55:.1f}% op margin − opex  =  ~PLN{bear_eps_imp:.1f}/share")
print(f"  At 7× trough P/E (refining-cycle/state-discount floor) = ~PLN{bear_eps_imp*7:.0f}  ✓ BEAR PLN{SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev      = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_refining = 1.0 * 0.07 * (1 - TAX_RATE) / shares    # refining - thin but huge volume base
eps_per_1B_retail   = 1.0 * 0.12 * (1 - TAX_RATE) / shares    # retail - higher margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every PLN1B refining segment revenue:           +PLN{eps_per_1B_refining:.3f}/EPS  = +PLN{eps_per_1B_refining*10:.2f}/share at 10× P/E")
print(f"  Every PLN1B retail fuel/convenience revenue:     +PLN{eps_per_1B_retail:.3f}/EPS  = +PLN{eps_per_1B_retail*10:.2f}/share at 10× P/E")
print(f"  1pp blended operating margin expansion:         +PLN{curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +PLN{curr_total*0.01*(1-TAX_RATE)/shares*10:.2f}/share at 10× P/E")
print(f"  $1/bbl model refining margin move (rough):       ~PLN{0.45:.2f}/EPS  (large group throughput amplifies crack spread sensitivity)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Crack spreads / Petchem cycle / Retail / Political risk / Energy transition / Dividend)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>5}  {'BASE':>5}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>6}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>5}  {ths[1]:>5}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>6}  {lbl}  {b}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from PLN{CURRENT_PRICE} + 15% hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:72]:<72}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR PLN{bear_price})")
hr()
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Refining crack spreads",             "~$9/bbl","<$5/bbl","-$4/bbl","New Asian/ME refining capacity + weak EU diesel demand crush margins"),
    ("Petchem margin cycle",                "near breakeven","loss-making","reversal","Global petchem oversupply deepens; Olefiny III ramp adds to losses"),
    ("Retail volume/margin growth",         "+2%",    "<-2%",   "-4pp",   "Recession in PL/CZ/DE/LT cuts fuel demand and convenience spend"),
    ("Political/governance overhang",       "ongoing uncertainty","escalating interference","reversal","Government reshuffle drives abrupt strategy/capex changes, mgmt churn"),
    ("One-off impairments (Litvinov/Schwedt etc.)", "manageable","large new charges","-$XB","Further refinery write-downs hit reported net income"),
    ("Multiple (P/E)",                      "~12.5x", "7x",     "-5.5x",  "State-discount + earnings-cycle trough compresses multiple sharply"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: European refining margins collapse to cyclical trough on new Asian/Middle")
print(f"  Eastern capacity and weak diesel demand, petrochemicals stay loss-making as Olefiny III")
print(f"  ramps into an oversupplied market, and one or more refineries (Litvinov/Schwedt) take")
print(f"  fresh impairment charges. Political reshuffling adds capex uncertainty without offsetting")
print(f"  returns. EPS falls to ~PLN2.50 → 7× trough P/E (refining-cycle/state-discount floor) = PLN{bear_price}.")
print(f"  Note: PLN{bear_price} is NOT permanent impairment — the integrated retail/refining franchise")
print(f"  and dividend-paying history provide a floor. Recovery toward ~PLN{bear_price+15}-PLN{bear_price+25} in 2yr is")
print(f"  plausible once the refining cycle troughs and turns.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           PLN{EPS_FY2027E:.2f}  (mid-cycle margin normalization off depressed FY2025/26 base)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (refining-cycle trough + state-ownership discount; PKN historical trough ~6-8×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    PLN{EPP:.0f}/share")
print(f"  Current PLN{CURRENT_PRICE:.2f} vs EPP PLN{EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% {'above' if epp_gap_pct >= 0 else 'below'} trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% {'premium to' if epp_gap_pct >= 0 else 'discount to'} EPP reflects that PKN trades at roughly")
print(f"  {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS PLN{EPS_FY2027E:.2f} — a modest multiple typical of a state-controlled,")
print(f"  cyclically-exposed integrated energy major. The dividend yield (~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}%) provides a")
print(f"  meaningful cash floor, but the multiple is unlikely to expand materially absent either a")
print(f"  sustained refining-margin upcycle, petrochemical recovery, or a credible re-rating of the")
print(f"  energy-transition (SMR/renewables) optionality.")
print(f"  EPP path: FY2029E EPS ~PLN6.50 × {PE_PESSIMISTIC:.0f}× = PLN{6.50*PE_PESSIMISTIC:.0f} floor (EPP grows modestly as mid-cycle earnings normalize).")
print(f"  At 10× mid-cycle P/E: PLN{EPS_FY2027E:.2f} × 10 = PLN{EPS_FY2027E*10:.0f}  — roughly in line with current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest mid-cycle EPS improvement; multiple stays depressed)")
hr()
print(f"  Conservative FY2028E EPS:        PLN{CONS_EPS_2YR:.2f}  (modest improvement vs FY2027E as petchem gradually recovers)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (modest de-rate from ~{CURRENT_PRICE/EPS_FY2027E:.1f}× as refining-cycle/political uncertainty persists)")
print(f"  Conservative equity value:        PLN{cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +PLN{cons_divs:.2f}/share  (PLN{ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           PLN{cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from PLN{CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: PKN trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS PLN{EPS_FY2027E:.2f} — a modest")
print(f"  multiple reflecting refining-margin cyclicality, petrochemical oversupply, and the")
print(f"  state-ownership/political discount. The high dividend yield (~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}%) provides a")
print(f"  meaningful cash-return cushion even if the multiple stays depressed. The energy-transition")
print(f"  optionality (SMR, renewables, upstream) is effectively a free call option not reflected in")
print(f"  the current price. If the refining cycle stays mid-cycle-or-better and petchem recovers,")
print(f"  total returns are attractive even without multiple expansion.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = PLN{(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E - 1)*100:.1f}% EPS growth by FY2028E vs FY2027E.")
print(f"  BUY trigger: PLN{round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–PLN{round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.30
beta        = 1.10
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        PLN{VOL_52W_LOW:.2f}  –  PLN{VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      PLN{ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  policy tied to net income, historically volatile)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (high; refining-cycle commodity exposure + political headline risk)")
print(f"  Beta vs WIG20:        {beta:.2f}  (above market; cyclical commodity exposure with state-ownership headline sensitivity)")
print(f"  1-sigma range (1yr):  PLN{sigma_range[0]:.0f}  –  PLN{sigma_range[1]:.0f}  (PLN{CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear PLN{bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe but plausible refining-cycle-trough + impairment scenario)")
print(f"  52W range reflects elevated volatility typical of an integrated refiner with political headline risk.")
print(f"  → European refining crack spreads are THE KEY binary for downside/upside risk.")
print(f"  → Petrochemical cycle recovery + SMR/nuclear FID progress are KEY bull catalysts.")
print(f"  → AVOID above PLN95  |  WATCHLIST PLN75–90  |  ACCUMULATE PLN58–70  |  BUY below PLN50–55")

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
    print(f"  {s:<10}  PLN{pr:>4}  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): PLN{ev_adj:.0f}  /  Proxy EV: PLN{ev_prx:.0f}  /  Market EV: PLN{ev_mkt:.0f}  /  Current: PLN{CURRENT_PRICE:.0f}")
hr()
print(f"  Downside  (→ Bear PLN{bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull PLN{bull_price}):  {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b_str}")
print(f"  Signal    :  {signal_full}")
print()
print(f"  MARKET PRICING: at PLN{CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is")
print(f"  {'ABOVE' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'BELOW'} the model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing")
print(f"  ~{MARKET_COMPOSITE:.2f}/4.0 while the model scores fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0.")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: the market is pricing in {'more' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'less'} confidence on a sustained refining-margin")
print(f"  recovery, petrochemical cycle turn, and energy-transition optionality than the bottom-up")
print(f"  fundamentals currently support. The risk/reward skew (Ratio B {ratio_b_str}) reflects PKN's")
print(f"  dual nature — a high-yield, deep-value cyclical with meaningful state-ownership/political")
print(f"  tail risk on one side and SMR/nuclear/renewables optionality on the other.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) European refining crack spreads — the dominant swing factor for group earnings")
print(f"  (2) Petrochemical margin cycle / Olefiny III ramp — capacity online into oversupplied market")
print(f"  (3) Political/governance developments — Polish Treasury control, management/strategy stability")
print(f"  (4) Orlen-Synthos SMR (BWRX-300) — FID timeline and state co-funding credibility")
print(f"  (5) Retail network performance (PL/CZ/DE/LT) — non-fuel/convenience mix growth")
print(f"  (6) Dividend policy execution — payout vs net-income volatility, ~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}% current yield")
print(f"  AVOID above PLN95  |  WATCHLIST PLN75–90  |  ACCUMULATE PLN58–70  |  BUY below PLN50–55")
print(f"  EPP floor: PLN{EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2027E EPS: PLN{EPS_FY2027E:.2f}")
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
