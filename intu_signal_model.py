"""
INTU  ·  Intuit Inc.  ·  NASDAQ: INTU
Bottom-up signal model  ·  SMB Financial Platform / AI Tax & Bookkeeping / Credit Karma
Date: 2026-08-02
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "INTU"
COMPANY       = "Intuit Inc."
SECTOR        = "SMB Financial Platform · QuickBooks · TurboTax · Credit Karma · NASDAQ: INTU"
CURRENT_PRICE = 316.07       # USD; close 2026-07-31 (verified live)
VOL_52W_LOW   = 252.84       # June 22, 2026 trough; post-layoff/lawsuit overhang
VOL_52W_HIGH  = 807.15       # 2025 pre-selloff ATH
SHARES_OUT_M  = 274.0        # millions; $86.5B mkt cap / $316.07; modest buyback vs SBC dilution
ANNUAL_DIV    = 4.80         # $/share forward; yield ~1.52%

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B; fiscal year ends July 31) ───────────
# Q3 FY2026 actual: revenue $8.56B (+10.4% YoY); FY2026 guide raised to $21.34-21.37B (+13-14%)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Global Business Solutions (QBO)", 9.6,  8.3, 11.0, "QBO Accounting +22%; core SMB platform; the segment absorbing the AI-agent bet"),
    ("Consumer (TurboTax)",             4.6,  4.0,  5.2, "Assisted tax momentum was the guide-raise driver; also the segment named in the securities suit"),
    ("Credit Karma",                    2.5,  2.1,  2.9, "+15% YoY; monetizing the Mint/CK data asset via lending & insurance referrals"),
    ("ProTax + Other",                  4.7,  4.2,  5.1, "Professional tax software + Mailchimp (being pulled back) + small residual segments"),
]

# Margin assumptions (non-GAAP)
OP_MARGIN_CURR   = 0.372    # FY2026E non-GAAP operating margin; restructuring charges are a headwind this year
OP_MARGIN_BULL   = 0.430    # BULL: AI-agent products (Intuit Assist) drive opex leverage post-restructuring
OP_MARGIN_BEAR   = 0.310    # BEAR: pricing/legal overhang forces discounting; restructuring savings don't materialize
TAX_RATE         = 0.180    # non-GAAP effective tax rate

# ── RESTRUCTURING / LEGAL CALCULATOR (the Intuit-specific angle) ─────────────
WORKFORCE_CUT_PCT   = 17.0   # % of full-time workforce cut, announced with Q3 (~3,000+ people)
LAWSUIT_CLASS_START = "2025-08-22"  # securities class action alleges misleading TurboTax growth claims
LAWSUIT_CLASS_END   = "2026-05-20"
QBO_GROWTH_PCT      = 22.0   # % YoY QuickBooks Online Accounting revenue growth, Q3
CK_GROWTH_PCT       = 15.0   # % YoY Credit Karma revenue growth, Q3
NEXT_REPORT_DATE    = "2026-08-25"  # Q4 + full-year FY2026 results — three weeks after this refresh

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 23.82       # $/share non-GAAP FY2026E; company guidance $23.80-$23.85 (+18%)
PE_PESSIMISTIC = 12.0        # trough P/E: the stock already trades near 13x forward; 12x prices
                             # a further legal/competitive overhang without assuming the franchise breaks
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  (17.25, 11,  190, "Securities litigation drags on; AI-agent tools cannibalize DIY TurboTax pricing power"),
    "BASE":  (28.50, 16,  456, "Restructuring savings land; QBO/Credit Karma keep compounding at a mid-teens blended rate"),
    "BULL":  (32.10, 21,  674, "Intuit Assist becomes the default SMB financial agent; assisted-tax mix keeps shifting up"),
    "XBULL": (39.00, 24,  936, "Intuit re-rates as the AI-native operating system for SMB finance; multi-year multiple recovery"),
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
        "name":       "Total revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<6%",    "≥9%",   "≥13%",   "≥18%"),
        "now":        "+10.4%",
        "score":      2,
        "comment":    "Q3 $8.56B (+10.4%), beat consensus. FY2026 guide raised to $21.34-21.37B (+13-14%)",
    },
    {
        "name":       "QuickBooks Online Accounting growth",
        "weight":     0.20,
        "thresholds": ("<10%",   "≥15%",  "≥20%",   "≥28%"),
        "now":        "+22%",
        "score":      3,
        "comment":    "Pricing + customer growth + mix shift all contributing — the core platform is not slowing down",
    },
    {
        "name":       "Credit Karma revenue growth",
        "weight":     0.10,
        "thresholds": ("<5%",    "≥10%",  "≥16%",   "≥24%"),
        "now":        "+15%",
        "score":      2,
        "comment":    "Steady monetization of the data asset via lending/insurance referrals; not the swing factor here",
    },
    {
        "name":       "Non-GAAP operating margin (restructuring year)",
        "weight":     0.20,
        "thresholds": ("<34%",   "≥37%",  "≥40%",   "≥43%"),
        "now":        "~37%",
        "score":      2,
        "comment":    "17% workforce cut and Mailchimp pullback are real near-term costs before any savings show up",
    },
    {
        "name":       "Legal/regulatory overhang",
        "weight":     0.15,
        "thresholds": ("active suit + downgrades","suit pending","narrowing","resolved/dismissed"),
        "now":        "active suit + downgrades",
        "score":      1,
        "comment":    "Securities class action over TurboTax growth claims (Aug 2025-May 2026 purchase window) plus analyst downgrades",
    },
    {
        "name":       "Forward P/E vs 10-yr average (~35x)",
        "weight":     0.15,
        "thresholds": (">24x",   "≤18x",  "≤14x",   "≤10x"),
        "now":        "13.3x",
        "score":      3,
        "comment":    "13.3× FY2026E — a 15-year-low multiple for a company still guiding to 18% EPS growth",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Valuation reset — 13.3× forward EPS is a 15-year low for a business still growing revenue 13-14%", +0.9, 0.20),
    ("+", "QBO platform moat — 22% growth, pricing power intact, the SMB financial system-of-record position", +0.6, 0.20),
    ("-", "Securities litigation — an active class action naming executives is a genuine, not theoretical, overhang", -0.6, 0.20),
    ("-", "Restructuring execution risk — 17% workforce cut plus Mailchimp pullback must convert to real savings", -0.5, 0.15),
    ("+", "Credit Karma + assisted tax — two segments proving Intuit can monetize AI-era products, not just defend share", +0.4, 0.15),
    ("-", "AI-disintermediation risk — DIY tax/bookkeeping is exactly the workflow generalist AI agents target first", -0.5, 0.10),
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
CONS_EPS_2YR  = 29.50   # conservative FY2028E: ~11.3% EPS CAGR off the FY2026E guide — well below BASE
CONS_PE_2YR   = 15      # modest re-rating from 13.3× — still far below the historical ~35× average
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  SMB Financial Platform / AI Tax & Bookkeeping")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))
print(f"  ⚠ Q4/FY2026 results due {NEXT_REPORT_DATE} — three weeks after this refresh. Figures below use")
print(f"  Q3 FY2026 actuals and the company's raised full-year guidance.")

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<34}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<34}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<34}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  FY2026 guidance (raised at Q3): revenue $21.34-21.37B (+13-14%), non-GAAP EPS $23.80-$23.85 (+18%)")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_op   = curr_total * OP_MARGIN_CURR
curr_eps  = round(curr_op * (1 - TAX_RATE) / shares, 2)

bull_op   = bull_total * OP_MARGIN_BULL
shares_b  = shares * 0.97
bull_eps_imp = round(bull_op * (1 - TAX_RATE) / shares_b, 2)

bear_op   = bear_total * OP_MARGIN_BEAR
bear_eps_imp = round(bear_op * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {OP_MARGIN_CURR*100:.1f}% op margin − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (company guidance ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {OP_MARGIN_BULL*100:.1f}% op margin, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 21× = ~${bull_eps_imp*21:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {OP_MARGIN_BEAR*100:.1f}% op margin (legal/pricing overhang, no restructuring payoff)")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 11× trough = ~${bear_eps_imp*11:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")
print()
print(f"  ⚠ NOTE: the revenue spread bear-to-bull is only {(bull_total/bear_total-1)*100:.0f}%, but the EPS spread is")
print(f"  {(bull_eps_imp/bear_eps_imp-1)*100:.0f}%. Restructuring makes this a margin-swing story in the near term —")
print(f"  the 17% workforce cut either converts into real opex leverage or it becomes a")
print(f"  distraction layered on top of an already-active securities lawsuit.")

# RESTRUCTURING / LEGAL CHECK
print()
print(f"  RESTRUCTURING & LEGAL CHECK  (the Intuit-specific angle):")
print(f"  Workforce reduction:          {WORKFORCE_CUT_PCT:.0f}% of FTEs (~3,000+ people), announced with Q3")
print(f"  QBO Accounting growth:        +{QBO_GROWTH_PCT:.0f}% YoY  (the segment funding the AI-agent bet)")
print(f"  Credit Karma growth:          +{CK_GROWTH_PCT:.0f}% YoY")
print(f"  Securities class action:      alleges misleading TurboTax growth/competitive claims,")
print(f"                                covering purchases {LAWSUIT_CLASS_START} to {LAWSUIT_CLASS_END}")
print()
print(f"  Two distinct narratives are running simultaneously. Operationally: QBO and Credit Karma")
print(f"  are compounding fine, and management just raised guidance. Structurally: a 17% workforce")
print(f"  cut and an active securities suit are the kind of events that take multiple quarters to")
print(f"  fully resolve, and the market is pricing the uncertainty more than the current numbers.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * OP_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_marg = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 40% op margin):       +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*16:.2f}/share at 16× P/E")
print(f"  Every 1pp of operating margin:               +${eps_per_1pp_marg:.3f}/EPS  = +${eps_per_1pp_marg*16:.2f}/share at 16× P/E")
print(f"  Every 1 turn of P/E:                         ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (revenue growth / QBO / Credit Karma / margin / legal overhang / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<44}  {'BEAR':>13}  {'BASE':>9}  {'BULL':>9}  {'XBULL':>10}  {'NOW':>9}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<44}  {ths[0]:>13}  {ths[1]:>9}  {ths[2]:>9}  {ths[3]:>10}  {s['now']:>9}  {lbl}  {b}")
    print(f"    {s['comment']}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15%/yr hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:88]:<88}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<32}  {'Current':>10}  {'Bear val':>10}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Total revenue YoY",           "+10.4%", "<6%",     "-4.4pp", "QBO price increases stop converting; SMB macro softens"),
    ("QBO Accounting growth",       "+22%",   "<10%",    "-12pp",  "AI-native bookkeeping tools win net-new SMB share"),
    ("Non-GAAP operating margin",   "~40%",   "<36%",    "-4pp",   "Restructuring costs land without the promised savings"),
    ("Legal/regulatory overhang",   "active", "worse",   "escalate","Class certified, or a second suit/regulatory probe opens"),
    ("Forward P/E",                 "13.3x",  "≤10x",    "-3.3x",  "Multiple resets further on sustained AI-disintermediation fear"),
    ("Credit Karma growth",         "+15%",   "<5%",     "-10pp",  "Lending/insurance referral demand softens with consumer credit cycle"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the bear case braids together two separate risks that the market is")
print(f"  currently pricing as one. The AI-disintermediation risk (generalist agents doing DIY")
print(f"  tax/bookkeeping) is a real multi-year structural question. The securities litigation is")
print(f"  a discrete legal process with its own timeline, largely unrelated to whether QBO keeps")
print(f"  growing 22%. If the market is conflating 'the stock fell on a lawsuit' with 'the AI")
print(f"  thesis is broken,' that gap is exactly where the mispricing this model flags would sit.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E non-GAAP EPS (company guide):  ${EPS_FY2026E:.2f}  ($23.80-$23.85, +18% YoY)")
print(f"  Pessimistic P/E at trough:               {PE_PESSIMISTIC:.0f}×  (stock already trades near 13× forward)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E non-GAAP EPS — down from a")
print(f"  10-year average closer to 35×. A 61% drawdown from the ${VOL_52W_HIGH:.2f} ATH has taken Intuit")
print(f"  from a premium SaaS multiple to a value-stock multiple while the company still guides")
print(f"  to 18% EPS growth. The EPP floor sits only {abs(epp_gap_pct):.0f}% below spot — a narrow gap for")
print(f"  a name this far off its highs, which is itself informative about how much bad news is priced in.")
print(f"  At an 18× reversion (about half the historical average): ${EPS_FY2026E:.2f} × 18 = ${EPS_FY2026E*18:.0f}  (+{(EPS_FY2026E*18/CURRENT_PRICE-1)*100:.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: legal overhang persists, only a modest re-rating)")
hr()
print(f"  Conservative FY2028E non-GAAP EPS:  ${CONS_EPS_2YR:.2f}  (~11.3% EPS CAGR — below the FY2026 guided pace)")
print(f"  Conservative exit P/E:               {CONS_PE_2YR}×  (13.3× → 15×; still a fraction of the historical ~35×)")
print(f"  Conservative equity value:            ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):        +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:               ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:            {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: even assuming EPS growth decelerates from the guided 18% to ~11%/yr and the")
print(f"  multiple only partially recovers, the conservative case clears {cons_annual:.1f}%/yr. The margin of")
print(f"  safety here is almost entirely the valuation reset — the litigation resolving favorably")
print(f"  and the AI-agent products landing are both upside to this case, not requirements of it.")
print(f"  Breakeven at 15× requires FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f} — below the FY2026 guide already.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.40
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Drawdown from high:   -{(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.1f}%  (multi-year de-rating: lawsuit + layoffs + AI-fear compounding)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; long growth streak)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (elevated for Intuit's history; legal + restructuring headline risk)")
print(f"  Beta vs S&P 500:      1.15  (higher than its historically defensive SaaS profile)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (would retest, not breach, the June 2026 low)")
print(f"  → {NEXT_REPORT_DATE} full-year print is the near-term catalyst — restructuring savings vs cost, guidance for FY2027.")
print(f"  → Any lawsuit development (dismissal motion, class certification ruling) will move the stock independent of fundamentals.")
print(f"  → BUY at current price  |  ADD $260–290  |  TRIM above $520")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f} the market composite is {MARKET_COMPOSITE:.2f}/4.0. The model's")
print(f"  adjusted composite is {ADJ_COMPOSITE:.2f}/4.0, for a gap of {ADJ_GAP:+.2f} — {valuation_label.lower()}.")
print(f"  Intuit at 13.3× forward earnings, growing revenue 13-14% and EPS 18%, is priced closer")
print(f"  to a legacy value stock than a platform business with pricing power and two proven")
print(f"  AI-era monetization engines (QBO, Credit Karma). The legal overhang justifies SOME")
print(f"  discount; the model's read is that the market has applied more than that.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) {NEXT_REPORT_DATE} Q4/FY2026 results — restructuring-savings evidence and FY2027 initial guidance")
print(f"  (2) Securities litigation timeline — a dismissal motion ruling is the next concrete milestone")
print(f"  (3) QBO Accounting growth durability — needs to hold near +20% to validate the platform-moat thesis")
print(f"  (4) Intuit Assist (AI agent) adoption metrics — the company's own answer to the disintermediation fear")
print(f"  (5) Workforce reduction completion — confirmation the 17% cut converts to durable opex leverage")
print(f"  BUY at ${CURRENT_PRICE:.2f}  |  ADD $260–290  |  TRIM above $520")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  QBO growth: +{QBO_GROWTH_PCT:.0f}%")
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
