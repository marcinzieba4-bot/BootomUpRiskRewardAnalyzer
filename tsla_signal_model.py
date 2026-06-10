"""
TSLA  ·  Tesla, Inc.  ·  NASDAQ: TSLA
Bottom-up signal model  ·  EV / Energy Storage (Megapack) / FSD-Robotaxi (Cybercab) / Optimus Humanoid Robot
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "TSLA"
COMPANY       = "Tesla, Inc."
SECTOR        = "EV / Autonomy (FSD/Robotaxi/Cybercab) / Energy Storage (Megapack) / Optimus Humanoid Robot · NASDAQ: TSLA"
CURRENT_PRICE = 345.00     # USD; as of 2026-06-10
VOL_52W_LOW   = 215.50     # 2025 EV demand-slowdown / brand-controversy trough
VOL_52W_HIGH  = 488.00     # late-2025 robotaxi/Optimus optionality re-rating peak
SHARES_OUT_M  = 3_220.0    # millions
ANNUAL_DIV    = 0.0        # $/share; Tesla pays no dividend, reinvests in growth/capex

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Automotive (ex-credits)",        72.0, 58.0,  85.0, "Model 3/Y core volume under pressure from BYD/Chinese EV competition + aging lineup; refreshed Model Y + lower-cost model are swing factors"),
    ("Regulatory credits",              2.0,  0.5,   3.0, "Federal/state EV credit revenue shrinking as policy support rolls back and peers need fewer credits"),
    ("Energy generation & storage (Megapack/Powerwall)", 18.0, 13.0,  28.0, "Megapack backlog remains the most credible near-term growth + margin engine; grid-storage demand from AI data centers"),
    ("Services & other",                10.5,  9.0,  13.0, "Supercharging network (incl. NACS licensing to other OEMs), used cars, parts/service - steady growth"),
    ("FSD/Robotaxi (Cybercab) revenue", 1.5,  0.3,  12.0, "Early-stage robotaxi fleet revenue (Austin/other metros) + FSD subscription/licensing - the core optionality bet"),
    ("Optimus (humanoid robot)",        0.2,  0.0,   4.0, "Pre-commercial; bear case = effectively zero revenue, bull case = early external/internal deployment revenue"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.180   # blended gross margin FY2026E (~18%; auto margins compressed by price cuts/competition)
GROSS_MARGIN_BULL = 0.260   # BULL: Megapack + FSD/robotaxi software-like margins lift blend materially
OPEX_FIXED_B      = 9.5     # R&D + SG&A ($B); includes AI/robotics/Optimus development spend
TAX_RATE          = 0.150   # effective rate; favorable jurisdictional mix + credits

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 1.85        # FY2026E adj EPS (consensus ~$1.70-$2.00 non-GAAP; core auto + energy only)
PE_PESSIMISTIC = 35.0        # trough P/E: even in a "no autonomy option value" world, market still pays growth-stock
                              # multiple for Megapack energy-storage growth + brand; historical EV-only trough ~30-40x
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # ~$65

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 1.10, 35,   39, "Auto margins keep compressing under BYD/Chinese EV price war; regulatory credits vanish; robotaxi/Cybercab program stalls on regulatory/safety setbacks; Optimus remains a science project; Megapack growth slows as competition (LFP from China) intensifies; EPS $1.10 → 35× (auto-only multiple) = $39"),
    "BASE":  ( 2.20, 55,  121, "Core auto stabilizes at lower volumes/margins; Megapack continues strong double-digit growth and becomes a real profit contributor; FSD/robotaxi expands city-by-city but remains revenue-immaterial through FY2027; Optimus stays pre-revenue; EPS $2.20 → 55× = $121"),
    "BULL":  ( 4.00, 90,  360, "Robotaxi (Cybercab) scales to multiple metros with meaningful fleet revenue; FSD take-rate and licensing to other OEMs accelerates; Megapack becomes a $10B+ profit business; Optimus begins limited commercial deployment; EPS $4.00 → 90× = $360"),
    "XBULL": ( 7.50, 110, 825, "Robotaxi network becomes a national-scale, high-margin software business re-rating Tesla as an AI/robotics platform; Optimus achieves meaningful external sales/licensing; Megapack + FSD licensing combine into a software-like earnings stream; EPS $7.50 → 110× = $825"),
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
        "name":       "Core auto delivery growth YoY",
        "weight":     0.20,
        "thresholds": ("<-10%", "≥-3%", "≥+5%", "≥+15%"),
        "now":        "-5%",
        "score":      2,
        "comment":    "Global deliveries roughly flat-to-down as BYD/Chinese EV makers and legacy OEM EVs gain share; refreshed Model Y stabilizing but lineup aging",
    },
    {
        "name":       "Automotive gross margin (ex-credits)",
        "weight":     0.15,
        "thresholds": ("<14%",  "≥16%", "≥20%", "≥24%"),
        "now":        "~16%",
        "score":      2,
        "comment":    "Price cuts and incentives to defend volume continue to pressure auto margins; cost-downs (4680 cells, casting) provide partial offset",
    },
    {
        "name":       "Energy storage (Megapack) deployment growth YoY",
        "weight":     0.20,
        "thresholds": ("<20%",  "≥35%", "≥55%", "≥80%"),
        "now":        "~50%",
        "score":      3,
        "comment":    "Megapack deployments (GWh) growing rapidly off Lathrop/Shanghai megafactory ramp; AI data-center grid-storage demand is a strong structural tailwind",
    },
    {
        "name":       "FSD/Robotaxi (Cybercab) deployment progress",
        "weight":     0.25,
        "thresholds": ("paused/regulatory setback", "single-city pilot", "multi-city expansion", "multi-state/licensing deals"),
        "now":        "single-city pilot (Austin + early expansion)",
        "score":      2,
        "comment":    "Robotaxi service live in Austin with safety driver/limited ODD; expansion to additional metros announced but unsupervised scale remains unproven",
    },
    {
        "name":       "Optimus (humanoid robot) commercialization progress",
        "weight":     0.10,
        "thresholds": ("delayed/internal-only", "internal pilot lines", "limited external sales", "scaled production + external orders"),
        "now":        "internal pilot lines",
        "score":      2,
        "comment":    "Optimus units deployed on internal Tesla factory lines for limited tasks; external commercial sales/production timeline remains aspirational",
    },
    {
        "name":       "Brand/demand health & key-man (Musk) governance risk",
        "weight":     0.10,
        "thresholds": ("severe brand damage/demand drop", "ongoing controversy/soft demand", "stabilizing", "improving/strong"),
        "now":        "ongoing controversy/soft demand",
        "score":      2,
        "comment":    "Musk's political activities and public controversies continue to weigh on brand perception in key markets (Europe especially); demand recovery uneven",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("-", "Core auto business under structural margin/share pressure from BYD and Chinese EV makers globally", -0.6, 0.20),
    ("+", "Megapack energy storage is a real, fast-growing, improving-margin business with AI-datacenter demand tailwind", +0.5, 0.20),
    ("-", "Extreme valuation embeds enormous option value for FSD/robotaxi/Optimus that may not materialize on any near-term timeline", -0.8, 0.25),
    ("-", "Musk key-man risk + political/brand controversy create demand and governance overhangs not present in typical auto names", -0.4, 0.15),
    ("+", "Vertical integration (batteries, software, manufacturing, charging network/NACS) provides durable structural advantages vs legacy OEMs", +0.3, 0.10),
    ("+", "Optionality is real, not fictional — Tesla has the most advanced real-world FSD fleet data and a working robotaxi pilot, unlike most peers", +0.3, 0.10),
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
CONS_EPS_2YR  = 2.50    # FY2028E conservative: Megapack growth + modest auto margin recovery, robotaxi still immaterial
CONS_PE_2YR   = 50      # de-rates modestly from current implied multiple as "story stock" premium normalizes somewhat
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  EV / Energy Storage / FSD-Robotaxi / Optimus")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<40}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<40}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<40}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
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
shares_b     = shares * 0.99   # minimal buyback; Tesla doesn't aggressively repurchase
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.92   # mix shift away from higher-margin energy/services
bear_oi      = bear_gp - OPEX_FIXED_B * 1.05           # R&D/Optimus spend sticky even as revenue shrinks
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ~${EPS_FY2026E:.2f}  ✓ roughly in line)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 90× = ~${bull_eps_imp*90:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.92:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 35× trough P/E (auto-only growth-stock floor) = ~${bear_eps_imp*35:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev      = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_megapack = 1.0 * 0.30 * (1 - TAX_RATE) / shares   # Megapack - higher margin than auto
eps_per_1B_fsd      = 1.0 * 0.70 * (1 - TAX_RATE) / shares   # FSD/robotaxi - software-like margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Megapack/energy storage revenue:   +${eps_per_1B_megapack:.3f}/EPS  = +${eps_per_1B_megapack*55:.1f}/share at 55× P/E")
print(f"  Every $1B FSD/robotaxi revenue (software-like): +${eps_per_1B_fsd:.3f}/EPS  = +${eps_per_1B_fsd*55:.1f}/share at 55× P/E")
print(f"  1pp auto gross margin change:                ±${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = ±${curr_total*0.01*(1-TAX_RATE)/shares*55:.1f}/share at 55× P/E")
print(f"  Auto delivery growth ±5pp on ~$72B base:      ±${curr_total*0.05*GROSS_MARGIN_CURR*(1-TAX_RATE)/shares:.3f}/EPS")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Core Auto / Megapack / FSD-Robotaxi / Optimus / Brand-Governance framework)")
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
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Core auto delivery growth",      "-5%",    "<-10%",  "−5pp",   "BYD/Chinese EV makers + legacy OEMs accelerate global share gains"),
    ("Auto gross margin",              "~16%",   "<14%",   "−2pp",   "Sustained price war forces deeper incentives across all regions"),
    ("Megapack deployment growth",     "+50%",   "<20%",   "−30pp",  "Battery cell supply constraints or Chinese LFP competitors undercut pricing"),
    ("FSD/Robotaxi progress",          "single-city", "paused/setback", "regression", "Safety incident triggers regulatory shutdown of robotaxi pilot"),
    ("Optimus progress",               "internal pilot", "delayed/internal-only", "no progress", "Humanoid robotics program slips years behind roadmap"),
    ("Brand/demand & governance",      "soft demand", "severe brand damage", "further decline", "Musk controversy escalates; boycotts spread to more core markets"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Chinese EV competitors (BYD and others) accelerate global share gains, forcing")
print(f"  another round of price cuts that compress auto gross margin below 14%. Simultaneously, a")
print(f"  safety incident or regulatory action pauses the robotaxi pilot, Optimus slips further behind")
print(f"  its roadmap, and Megapack growth decelerates sharply as Chinese LFP storage competitors")
print(f"  undercut on price. The market re-prices TSLA as 'just an automaker' at a 35× trough multiple")
print(f"  on ~$1.10 EPS = ${bear_price}.")
print(f"  Note: ${bear_price} would represent the loss of essentially ALL embedded option value for")
print(f"  FSD/robotaxi/Optimus — a >85% drawdown from current levels. Recovery would require a credible")
print(f"  reset of the autonomy/robotics narrative, which could take years.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:       ${EPS_FY2026E:.2f}  (consensus ~$1.70-$2.00 non-GAAP; core auto + energy only)")
print(f"  Pessimistic P/E at trough:        {PE_PESSIMISTIC:.0f}×  (auto-only growth-stock floor; assumes ZERO value for FSD/robotaxi/Optimus optionality)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  A +{epp_gap_pct:.0f}% premium to EPP means the market is pricing in an enormous amount of")
print(f"  optionality value for FSD/robotaxi (Cybercab) and Optimus that is NOT reflected in current")
print(f"  earnings power AT ALL. At ${CURRENT_PRICE:.2f} on FY2026E EPS ${EPS_FY2026E:.2f}, the implied P/E is")
print(f"  ~{CURRENT_PRICE/EPS_FY2026E:.0f}×. This is less a 'valuation' in the traditional sense and more a market-wide")
print(f"  bet on whether autonomous driving + humanoid robotics become trillion-dollar businesses with")
print(f"  Tesla as the leader. The core auto + energy business alone does not support the current price.")
print(f"  EPP path: even at FY2028E EPS ~$2.50 × {PE_PESSIMISTIC:.0f}× = ${2.50*PE_PESSIMISTIC:.0f} floor — still far below current price.")
print(f"  At 55× BASE-case P/E: ${EPS_FY2026E:.2f} × 55 = ${EPS_FY2026E*55:.0f}  — also well below current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: Megapack growth + modest auto margin stabilization; FSD/robotaxi still immaterial to earnings)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (Megapack scaling, auto margins stabilize modestly, robotaxi/Optimus still pre-material)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (modest de-rate from current ~{CURRENT_PRICE/EPS_FY2026E:.0f}× as 'story premium' normalizes somewhat)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (no dividend; reinvests in growth/capex)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: TSLA trades at ~{CURRENT_PRICE/EPS_FY2026E:.0f}× FY2026E EPS ${EPS_FY2026E:.2f} — a multiple that")
print(f"  cannot be justified by the core auto + energy storage business alone, no matter how well it")
print(f"  executes. The entire bull case for owning TSLA at this price rests on FSD/robotaxi (Cybercab)")
print(f"  and Optimus becoming real, large, high-margin businesses within a multi-year window. Megapack")
print(f"  is a genuinely strong, improving business, but it alone cannot support the current multiple.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2026E - 1)*100:.0f}% EPS growth by FY2028E vs FY2026E — only plausible if robotaxi/FSD")
print(f"  begins contributing materially to earnings, i.e. closer to the BULL scenario than BASE.")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.55
beta        = 2.30
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      $0.00/share  (no dividend; all FCF reinvested in capex/R&D/buybacks)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (extremely high; among the most volatile mega-caps)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (very high; amplifies both macro moves and Musk-headline-driven swings)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe but has happened before in TSLA's history — 2022 saw a >70% drawdown)")
print(f"  52W range itself spans a >2x ratio — TSLA routinely moves 50%+ in either direction within a year.")
print(f"  → Robotaxi (Cybercab) safety record / regulatory approval pace is THE KEY binary catalyst.")
print(f"  → Optimus production ramp + any external sales announcement is a KEY incremental bull catalyst.")
print(f"  → China EV competition (BYD pricing/share) is THE KEY structural bear risk for core auto.")
print(f"  → AVOID above $400  |  WATCHLIST $300–375  |  ACCUMULATE $230–270  |  BUY below $180–210")

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
print(f"  {'ABOVE' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'BELOW'} the model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing")
print(f"  ~{MARKET_COMPOSITE:.2f}/4.0 while the model scores fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0.")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: the market is pricing in a level of confidence in the FSD/robotaxi/Optimus")
print(f"  optionality bet that is well ahead of where the bottom-up signals (still mostly single-city")
print(f"  pilots and internal-only deployments) currently support. This is a binary, story-driven name")
print(f"  where the risk/reward (Ratio B {ratio_b_str}) is dominated by the BEAR/XBULL tails rather")
print(f"  than a typical BASE-case-anchored distribution.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Robotaxi (Cybercab) expansion — new metro launches, removal of safety driver, regulatory approvals")
print(f"  (2) China EV competition — BYD/Chinese OEM global share gains and their impact on Tesla auto margins")
print(f"  (3) Megapack/energy storage growth — GWh deployed, gross margin trajectory, AI-datacenter demand")
print(f"  (4) Optimus production ramp — unit volumes, internal deployment scope, any external sales/orders")
print(f"  (5) FSD take-rate & licensing — software attach rate, any third-party OEM licensing deals")
print(f"  (6) Musk/governance/brand — political controversy trajectory and impact on demand in key markets (Europe)")
print(f"  AVOID above $400  |  WATCHLIST $300–375  |  ACCUMULATE $230–270  |  BUY below $180–210")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}")
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
