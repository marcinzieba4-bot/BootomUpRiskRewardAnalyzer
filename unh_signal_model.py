"""
UNH  ·  UnitedHealth Group Inc.  ·  NYSE: UNH
Bottom-up signal model  ·  UnitedHealthcare (Insurance) / Optum Health / Optum Rx / Optum Insight
Date: 2026-08-04
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "UNH"
COMPANY       = "UnitedHealth Group Inc."
SECTOR        = "Managed Care · UnitedHealthcare Insurance · Optum Health/Rx/Insight · Medicare Advantage Reset · NYSE: UNH"
CURRENT_PRICE = 415.36      # USD; close 2026-08-03
VOL_52W_LOW   = 236.95      # USD
VOL_52W_HIGH  = 461.62      # USD
SHARES_OUT_M  = 908.0       # millions; buybacks still paused during the reset
ANNUAL_DIV    = 9.28        # $/share; maintained through the crisis (~2.2% yield)

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# Q2 2026 actual (reported ~Jul 16): revenue $112.03B (beat), adj EPS $6.38 — a huge beat
# vs. ~$4.90-4.91 consensus (+30%); Medical Care Ratio improved sharply to 86.7% from 89.4%
# YoY. FY2026 guidance raised: adj EPS $19.50-20.00 (from $18.25+), revenue >$439B (consensus
# ~$446.5B). Hemsley's "operational reset" continues: M&A/buybacks still paused, exiting
# unprofitable MA markets — management expects to shed 3M+ members in 2026 (first revenue
# decline in a decade), but margins are recovering faster than expected. The DOJ criminal
# probe into Medicare Advantage risk-adjustment billing remains open and now extends to
# Optum Rx physician compensation — no resolution disclosed.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("UnitedHealthcare (Medicare Adv./Comm./Medicaid)", 290.0, 270.0, 310.0, "MA repricing driving MCR improvement even as membership shrinks by design"),
    ("Optum Health (value-based care/clinics)",           60.0,  54.0,  68.0, "Value-based care margins recovering post-reset; physician group consolidation continues"),
    ("Optum Rx (PBM)",                                     75.0,  70.0,  82.0, "PBM steady growth; DOJ probe now extends here too, plus reform/transparency pressure"),
    ("Optum Insight (data/tech/services)",                 21.5,  19.0,  24.0, "Smaller, stable analytics/tech segment; modest growth"),
]

# Net-margin-based bridge
NET_MARGIN_CURR = 0.0402   # FY2026E; reconciles to raised guidance midpoint
NET_MARGIN_BEAR = 0.0330   # BEAR: MCR relapses, DOJ escalates, repricing gains reverse
NET_MARGIN_BULL = 0.0516   # BULL: MCR normalizes further, repricing cycle fully validated

# ── MCR / DOJ RESET TRACKER (the UNH-specific angle) ──────────────────────────
Q2_2026_REVENUE_B          = 112.03   # $B, Q2 2026 actual reported revenue
Q2_2026_ADJ_EPS            = 6.38     # $ adjusted EPS, Q2 2026 (huge beat, +30% vs consensus)
Q2_2026_MCR_PCT            = 86.7     # % Medical Care Ratio, Q2 2026 (down from 89.4% YoY)
MEMBERS_EXPECTED_TO_SHED_M = 3.0      # million, 2026 MA membership reduction (deliberate)
DOJ_PROBE_SCOPE            = "MA risk-adjustment coding + Optum Rx physician comp"
STOCK_MOVE_FROM_JUNE_LOW_PCT = round((CURRENT_PRICE - 285.00) / 285.00 * 100, 1)  # move since last refresh

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 19.75       # FY2026E EPS (raised guidance $19.50-20.00; midpoint)
PE_PESSIMISTIC = 13.0        # pessimistic P/E: below the current ~21× multiple; DOJ tail risk still live despite the operational beat
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (15.00, 16,  240, "DOJ investigation escalates (charges or major penalty, now covering Optum Rx too); MCR relapses above 90%; EPS $15.00 → 16× = $240"),
    "BASE":  (19.75, 21.03, 415, "2026 MA repricing continues restoring margins; DOJ investigation drags on but no crippling penalty; Optum Rx/Insight provide steady ballast; EPS $19.75 → 21× = $415"),
    "BULL":  (27.50, 19,  523, "MCR normalizes further toward mid-80s; DOJ matter resolved with a manageable settlement; Hemsley-led reset fully validated; EPS $27.50 → 19× = $523"),
    "XBULL": (31.00, 22,  682, "Full earnings power restoration; DOJ overhang fully lifted; multiple re-rates back toward UNH's historical premium as the largest US insurer regains its growth narrative; EPS $31.00 → 22× = $682"),
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
        "name":       "Medical Care Ratio (MCR) trend",
        "weight":     0.30,
        "thresholds": (">90%",  "≥88%",  "≥86%",   "≤84%"),
        "now":        "86.7%",
        "score":      3,
        "comment":    "MCR improved sharply to 86.7% from 89.4% YoY — the 2026 repricing cycle is working faster than expected",
    },
    {
        "name":       "DOJ Medicare Advantage risk-adjustment investigation",
        "weight":     0.20,
        "thresholds": ("criminal charges/major penalty", "ongoing/uncertain", "narrowing/civil settlement", "closed, no material findings"),
        "now":        "ongoing/uncertain, scope widening",
        "score":      1,
        "comment":    "Probe now extends to Optum Rx physician compensation on top of the original MA coding investigation; no resolution disclosed",
    },
    {
        "name":       "2026 MA bid repricing / membership stability",
        "weight":     0.20,
        "thresholds": ("attrition>repricing gain", "roughly even", "repricing offsets attrition", "net margin expansion"),
        "now":        "repricing driving net margin gains",
        "score":      3,
        "comment":    "Management is deliberately shedding 3M+ members from unprofitable plans while MCR improves — repricing is clearly working at the margin level",
    },
    {
        "name":       "Optum Rx / Optum Insight stability",
        "weight":     0.15,
        "thresholds": ("declining", "flat", "mid-single-digit growth", "high-single-digit+ growth"),
        "now":        "+5-6%",
        "score":      3,
        "comment":    "PBM and analytics segments continue growing steadily, providing earnings ballast during the reset",
    },
    {
        "name":       "Leadership/cost discipline (Hemsley return)",
        "weight":     0.10,
        "thresholds": ("no clear plan", "plan announced, unproven", "early execution wins", "clear turnaround traction"),
        "now":        "early execution wins",
        "score":      3,
        "comment":    "The Q2 beat and MCR improvement are the first hard evidence the Hemsley cost-discipline plan is actually working",
    },
    {
        "name":       "Balance sheet / capital return capacity",
        "weight":     0.05,
        "thresholds": ("<A-",  "A to A+",  "AA-",   "AA"),
        "now":        "A+",
        "score":      3,
        "comment":    "Still investment-grade with strong free cash flow generation; dividend maintained through the crisis",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("-", "DOJ criminal investigation tail risk — unresolved, now covering both MA coding and Optum Rx; binary downside", -0.7, 0.25),
    ("+", "Scale moat — largest US health insurer; diversified across UnitedHealthcare/Optum Health/Rx/Insight", +0.5, 0.20),
    ("+", "MCR improved sharply (89.4%→86.7%) faster than the market expected — real, quantified evidence the reset is working", +0.5, 0.20),
    ("+", "Optum Rx/Insight diversification — non-insurance segments provide earnings stability during the UnitedHealthcare reset", +0.4, 0.15),
    ("+", "Leadership credibility — the Q2 beat is the first hard proof point for Hemsley's turnaround plan", +0.4, 0.10),
    ("-", "Trust/regulatory overhang — reputational damage and heightened political/regulatory scrutiny of MA broadly persist",  -0.3, 0.10),
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
CONS_EPS_2YR  = 23.50   # FY2028E conservative: gradual MCR normalization, modest membership stabilization
CONS_PE_2YR   = 17      # a modest compression from the current ~21× as DOJ uncertainty persists
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  UnitedHealthcare Insurance / Optum Health/Rx/Insight / MA Reset")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
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
print(f"  Q2 2026 actual: revenue ${Q2_2026_REVENUE_B:.2f}B, adj EPS ${Q2_2026_ADJ_EPS:.2f} (+30% vs consensus), MCR {Q2_2026_MCR_PCT:.1f}% (down from 89.4% YoY)")
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
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (guidance ${EPS_FY2026E:.2f} midpoint  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {NET_MARGIN_BULL*100:.2f}% net margin")
print(f"  ÷ {shares:.3f}B shares  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {NET_MARGIN_BEAR*100:.2f}% net margin (DOJ escalation + MCR relapse)")
print(f"  ÷ {shares:.3f}B shares  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# MCR / DOJ RESET TRACKER
print()
print(f"  MCR / DOJ RESET TRACKER  (the UNH-specific angle):")
print(f"  Q2 2026 revenue / adj EPS:                   ${Q2_2026_REVENUE_B:.2f}B / ${Q2_2026_ADJ_EPS:.2f}  (adj EPS +30% vs consensus)")
print(f"  Medical Care Ratio (MCR):                     {Q2_2026_MCR_PCT:.1f}%  (down from 89.4% a year ago)")
print(f"  2026 membership reduction (deliberate):        {MEMBERS_EXPECTED_TO_SHED_M:.0f}M+ members")
print(f"  DOJ probe scope:                               {DOJ_PROBE_SCOPE}")
print(f"  Stock move since last refresh (Jun 10):        +{STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}%")
print()
print(f"  The Q2 print is the first hard evidence that Hemsley's operational reset is working: MCR")
print(f"  improved by 2.7pp YoY, well ahead of expectations, even as the company deliberately sheds")
print(f"  unprofitable membership. That's a real, quantified turnaround signal — but the DOJ investigation")
print(f"  is unresolved and has actually widened in scope, which is why this model stays cautious")
print(f"  despite the stock's {STOCK_MOVE_FROM_JUNE_LOW_PCT:.0f}% rally since June.")

# KEY SENSITIVITIES
print()
eps_per_1pp_mcr = curr_total * 0.01 / shares
eps_per_1B_rev  = 1.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every 1pp MCR change (medical cost ratio):    ∓${eps_per_1pp_mcr:.2f}/EPS  = ∓${eps_per_1pp_mcr*21:.1f}/share at 21× P/E")
print(f"  Every $1B revenue (at {NET_MARGIN_CURR*100:.1f}% margin):        +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*21:.2f}/share at 21× P/E")
print(f"  Every 1 turn of P/E:                           ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (MCR trend / DOJ investigation / MA repricing / Optum diversification framework)")
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
    ("Medical Care Ratio (MCR)",         "86.7%",  ">90%",   "Utilization trend reaccelerates faster than repricing can offset"),
    ("DOJ investigation outcome",        "ongoing, widening", "criminal charges/major fine", "DOJ brings charges or imposes a multi-billion-dollar penalty"),
    ("MA membership/repricing",          "net margin gains", "attrition>repricing", "Members flee faster than premium/mix gains offset"),
    ("Optum Rx/Insight growth",          "+5-6%",  "<2%",    "PBM reform/transparency rules compress spread economics"),
    ("Leadership turnaround traction",   "early wins", "stalled", "Hemsley cost-cutting plan stalls; guidance cut again"),
    ("Net margin",                       "4.0%",   "<3%",    "Sustained margin pressure reverses the Q2 improvement"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>16}  {bear_v:>9}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the DOJ investigation — now covering both MA risk-adjustment coding and Optum Rx")
print(f"  physician compensation — results in formal charges or a major penalty, while the MCR relapses")
print(f"  above 90% as the Q2 improvement proves temporary rather than structural.")
print(f"  Note: ${bear_price} is NOT necessarily permanent impairment — UNH remains the largest US health")
print(f"  insurer with Optum Rx/Insight ballast and a maintained dividend (${ANNUAL_DIV:.2f}/share).")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E EPS estimate:           ${EPS_FY2026E:.2f}  (raised guidance midpoint)")
print(f"  Pessimistic P/E:                 {PE_PESSIMISTIC:.0f}×  (below the current ~21× multiple; DOJ tail risk still live)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  UNH trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS ${EPS_FY2026E:.2f} — a genuine re-rating from its crisis-era")
print(f"  low-teens multiple, reflecting the Q2 beat and MCR improvement. The +{epp_gap_pct:.0f}% premium to EPP")
print(f"  captures both real operational progress and an unresolved DOJ overhang the market may be")
print(f"  underweighting after such a strong quarter.")
print(f"  At 19× mid-cycle P/E (DOJ resolved, MCR holds): ${EPS_FY2026E:.2f} × 19 = ${EPS_FY2026E*19:.0f}  — {(EPS_FY2026E*19/CURRENT_PRICE-1)*100:+.0f}% vs current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: gradual MCR normalization continues, multiple compresses modestly)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (modest growth as MCR normalization continues)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (a modest compression from the current ~21× as DOJ uncertainty persists)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: the conservative case is nearly flat, not because the operational turnaround")
print(f"  isn't real — it clearly is — but because the stock's {STOCK_MOVE_FROM_JUNE_LOW_PCT:.0f}% rally since June has already")
print(f"  captured most of that improvement, while the DOJ investigation remains a genuine, unresolved,")
print(f"  and recently-widened tail risk.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.35
beta        = 0.75
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock is up {STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}% since the last refresh (Jun 10) on the Q2 beat; still well below the ~$600 2024 peak")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  maintained through the crisis)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (still elevated; DOJ/MCR binary catalysts drive large single-day moves)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (historically defensive, now elevated idiosyncratic risk dominates)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (a DOJ-shock + MCR-relapse tail scenario)")
print(f"  → DOJ investigation outcome/timeline is THE KEY binary for both downside and upside.")
print(f"  → MCR trajectory in coming quarterly prints is the KEY operational signal to watch.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $340  |  Trim above $470")

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
print(f"  {valuation_label.lower()} by model standards. In plain terms: the Q2 operational beat is real and the MCR")
print(f"  improvement is genuine progress, but the DOJ investigation remains unresolved and has actually")
print(f"  widened in scope — a real reason for caution even after such a strong quarter.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) DOJ Medicare Advantage risk-adjustment / Optum Rx investigation — charges, settlement, or resolution timeline")
print(f"  (2) Medical Care Ratio (MCR) quarterly trend — confirming the Q2 improvement is structural, not one-off")
print(f"  (3) 2026/2027 MA bid cycle outcomes — membership retention vs margin restoration tradeoff")
print(f"  (4) Hemsley-led cost discipline — SG&A leverage and capital allocation signals (buyback resumption)")
print(f"  (5) Optum Rx PBM reform — transparency/spread-pricing legislation impact on segment economics")
print(f"  (6) Dividend sustainability — ${ANNUAL_DIV:.2f}/share maintained through the crisis as a confidence signal")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $340  |  Trim above $470")
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
