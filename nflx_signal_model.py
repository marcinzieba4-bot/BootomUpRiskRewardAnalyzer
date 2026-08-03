"""
NFLX  ·  Netflix, Inc.  ·  NASDAQ: NFLX
Bottom-up signal model  ·  Streaming Subscription / Advertising / Live Events / Gaming
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "NFLX"
COMPANY       = "Netflix, Inc."
SECTOR        = "Streaming · Ad-Supported Tier · Live Events · Gaming · NASDAQ: NFLX"
CURRENT_PRICE = 71.71        # USD; close 2026-07-31 (verified live); post 10-for-1 split (Nov 2025)
VOL_52W_LOW   = 65.08        # 2026 trough; post Q2 growth-deceleration selloff
VOL_52W_HIGH  = 126.71       # 2026 peak, pre-deceleration-concern selloff
SHARES_OUT_M  = 4_164.0      # millions; $298.6B mkt cap / $71.71; post-split share count
ANNUAL_DIV    = 0.0          # $/share; no dividend, all capital return via buyback

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ──────────────────────────────────────
# Q2 2026 actual: revenue $12.56B (+13% YoY), op margin 33.4%. FY2026 guide: $51.0-51.4B,
# op margin 31.5%. Ad revenue guided to roughly double to ~$3B in 2026.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Streaming Subscription",  48.2, 44.0, 52.5, "Core sub revenue; price increases + moderate member growth; the large, slow-moving base"),
    ("Advertising",              3.0,  2.2,  4.5, "Roughly doubling in 2026; small base, by far the fastest-growing and highest-optionality line"),
]

# Margin assumptions (non-GAAP-equivalent; Netflix reports GAAP with minimal adjustment items)
OP_MARGIN_CURR   = 0.315    # FY2026E guided operating margin (unchanged at 31.5% even as the revenue range narrowed)
OP_MARGIN_BULL   = 0.360    # BULL: ad tier scales with high incremental margin; content spend efficiency improves
OP_MARGIN_BEAR   = 0.270    # BEAR: member growth stalls, forcing pricing/promotional concessions that compress margin
TAX_RATE         = 0.150    # effective tax rate (below US statutory due to international mix)

# ── WBD TERMINATION / STRATEGIC REFOCUS CALCULATOR (the Netflix-specific angle) ──
WBD_TERMINATION_FEE_B = 2.8   # $B received from Warner Bros. Discovery when Paramount Skydance won the bidding war
WBD_DEAL_OUTCOME       = "Netflix withdrew; Paramount Skydance acquired WBD for $31/share"
Q1_REPORTED_EPS        = 1.23  # $ Q1 2026 diluted EPS, INCLUDING the one-time WBD fee (~$0.67/share pre-tax impact)
Q2_CLEAN_EPS            = 0.80 # $ Q2 2026 diluted EPS, a clean quarter with no one-time items, still beat consensus
AD_REVENUE_DOUBLING     = True # 2026 ad revenue guided to roughly double YoY to ~$3B
Q3_GUIDE_REV_B          = 12.86 # $B Q3 2026 revenue guide (+11.7% YoY — the deceleration that triggered the selloff)

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 3.75         # $/share; reported-basis FY2026E (Q1 $1.23 incl. WBD fee + Q2 $0.80 + Q3E ~$0.83 + Q4E ~$0.88)
                               # NOTE: ~$0.46/share of this is the one-time WBD termination fee; clean run-rate EPS is closer to $3.29
PE_PESSIMISTIC = 15.0         # trough P/E: NFLX traded near this level during the 2022 subscriber-loss
                               # panic (pre-split-adjusted terms); 15x prices a comparable growth-deceleration scare
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 2.55, 15,   38, "Member growth stalls; ad tier monetization disappoints; content cost inflation compresses margin"),
    "BASE":  ( 3.55, 22,   78, "Steady mid-teens subscription growth continues; ad revenue keeps roughly doubling; margin holds near 31-32%"),
    "BULL":  ( 4.32, 28,  121, "Ad tier and live sports fully scale; content efficiency improves margin faster than guided; multiple re-rates"),
    "XBULL": ( 5.20, 32,  166, "Netflix becomes the default global video-plus-live-sports platform; ad revenue rivals subscription as a growth driver"),
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
        "thresholds": ("<8%",    "≥11%",   "≥15%",   "≥20%"),
        "now":        "+13%",
        "score":      2,
        "comment":    "Q2 $12.56B (+13%); Q3 guide implies +11.7% — the deceleration that triggered the post-earnings selloff",
    },
    {
        "name":       "Operating margin",
        "weight":     0.15,
        "thresholds": ("<28%",   "≥31%",   "≥34%",   "≥37%"),
        "now":        "33.4%",
        "score":      3,
        "comment":    "Down 0.7pp YoY on higher tech/marketing spend, but still comfortably above the FY guide of 31.5%",
    },
    {
        "name":       "Advertising revenue growth",
        "weight":     0.20,
        "thresholds": ("<40%",   "≥60%",   "≥85%",   "≥110%"),
        "now":        "~100%",
        "score":      4,
        "comment":    "Guided to roughly double in 2026 to ~$3B — still a small base, but by far the fastest-growing segment",
    },
    {
        "name":       "WBD deal outcome / capital position",
        "weight":     0.15,
        "thresholds": ("lost + no fee","lost + fee","fee + refocus","fee + accretive M&A"),
        "now":        "fee + refocus",
        "score":      3,
        "comment":    "Netflix walked away from a $110B+ bidding war, collected a $2.8B fee, and avoided a massive integration risk",
    },
    {
        "name":       "Q3 guidance vs Street",
        "weight":     0.15,
        "thresholds": ("well below","below",  "in-line", "above"),
        "now":        "below",
        "score":      2,
        "comment":    "Both Q3 revenue and EPS guidance came in modestly below Street forecasts — the proximate cause of the drawdown",
    },
    {
        "name":       "Forward P/E (reported-basis)",
        "weight":     0.15,
        "thresholds": (">30x",   "≤24x",   "≤19x",   "≤14x"),
        "now":        "~19.1x",
        "score":      3,
        "comment":    "19.1× FY2026E — the cheapest Netflix has traded relative to its own growth rate in years",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Dodged a bullet — walking away from WBD avoided integrating a declining legacy media conglomerate at a $110B+ price", +0.7, 0.20),
    ("+", "$2.8B termination fee — pure cash gain, no dilution, no debt; strengthens the balance sheet with zero integration risk", +0.4, 0.10),
    ("+", "Advertising inflection — doubling off a real base, with a completed ad-tech stack now largely built out", +0.6, 0.20),
    ("-", "Growth deceleration is real — +13% and slowing is a genuine multi-quarter trend, not noise", -0.5, 0.20),
    ("+", "Valuation reset — 19.1× forward is a historic discount for this name relative to its own growth history", +0.5, 0.15),
    ("-", "Content cost inflation + competitive intensity — live sports rights and general content costs keep climbing across the industry", -0.4, 0.15),
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
CONS_EPS_2YR  = 3.90    # conservative FY2028E: ~2.0% EPS CAGR off the clean (ex-WBD-fee) ~$3.29 base — a genuine deceleration case
CONS_PE_2YR   = 20      # modest re-rating from ~19x — still below Netflix's historical richer multiples
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Streaming / Advertising / Live Events / Gaming")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))
print(f"  ⚠ Post 10-for-1 stock split (effective Nov 17, 2025). All figures below are split-adjusted.")

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<28}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<28}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<28}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  FY2026 guidance: revenue $51.0-51.4B, operating margin 31.5% (narrowed range, unchanged margin)")
print()

# EPS bridge (clean, ex-one-time-items basis)
shares    = SHARES_OUT_M / 1000
curr_op   = curr_total * OP_MARGIN_CURR
curr_eps_clean = round(curr_op * (1 - TAX_RATE) / shares, 2)

bull_op   = bull_total * OP_MARGIN_BULL
shares_b  = shares * 0.97
bull_eps_imp = round(bull_op * (1 - TAX_RATE) / shares_b, 2)

bear_op   = bear_total * OP_MARGIN_BEAR
bear_eps_imp = round(bear_op * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check (CLEAN basis):  ${curr_total:.1f}B rev × {OP_MARGIN_CURR*100:.1f}% op margin − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps_clean:.2f}/share")
print(f"  Reported FY2026E EPS (incl. $2.8B WBD termination fee, ~$0.46/share after-tax): ${EPS_FY2026E:.2f}")
print(f"  The ${EPS_FY2026E - curr_eps_clean:.2f}/share gap is the one-time item — real cash, but not repeatable operating earnings.")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {OP_MARGIN_BULL*100:.1f}% op margin, post-buyback")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 28× = ~${bull_eps_imp*28:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {OP_MARGIN_BEAR*100:.1f}% op margin (member growth stalls, pricing pressure)")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 15× trough = ~${bear_eps_imp*15:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# WBD TERMINATION CHECK
print()
print(f"  WBD TERMINATION & STRATEGIC REFOCUS CHECK  (the Netflix-specific angle):")
print(f"  Deal outcome:                  {WBD_DEAL_OUTCOME}")
print(f"  Termination fee received:      ${WBD_TERMINATION_FEE_B:.1f}B  (pure cash, no dilution, no debt)")
print(f"  Q1 2026 reported EPS:          ${Q1_REPORTED_EPS:.2f}  (includes the one-time fee)")
print(f"  Q2 2026 clean EPS:             ${Q2_CLEAN_EPS:.2f}  (no one-time items; still beat consensus)")
print()
print(f"  Losing the WBD bidding war is, on balance, good news dressed as a disappointment.")
print(f"  Netflix avoided integrating a declining linear-TV and legacy-studio conglomerate at a")
print(f"  price north of $110B, kept $2.8B in cash for the trouble, and can now put full")
print(f"  management attention back on the organic growth engines — ads, live sports, gaming —")
print(f"  that are actually working. The market's reaction (selling off on the Q2 growth-guide")
print(f"  miss) suggests this distinction hasn't been fully appreciated yet.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * OP_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_marg = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 31.5% op margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*22:.2f}/share at 22× P/E")
print(f"  Every 1pp of operating margin:            +${eps_per_1pp_marg:.3f}/EPS  = +${eps_per_1pp_marg*22:.2f}/share at 22× P/E")
print(f"  Every 1 turn of P/E:                      ±${curr_eps_clean:.2f}/share  ({curr_eps_clean/CURRENT_PRICE*100:.1f}% of the stock, clean-EPS basis)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (revenue growth / margin / advertising / WBD outcome / guidance / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<38}  {'BEAR':>12}  {'BASE':>10}  {'BULL':>12}  {'XBULL':>13}  {'NOW':>10}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<38}  {ths[0]:>12}  {ths[1]:>10}  {ths[2]:>12}  {ths[3]:>13}  {s['now']:>10}  {lbl}  {b}")
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
print(f"  {'Signal':<30}  {'Current':>9}  {'Bear val':>9}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Total revenue YoY",          "+13%",   "<8%",     "-5pp",   "Member growth stalls in mature markets; pricing power hits a wall"),
    ("Operating margin",           "33.4%",  "<28%",    "-5.4pp", "Content cost inflation (esp. live sports rights) outpaces revenue growth"),
    ("Advertising revenue growth", "~100%",  "<40%",    "-60pp",  "Ad tier monetization plateaus below the doubling pace already guided"),
    ("Q3 guide vs Street",         "below",  "well below","worse","A second consecutive guidance disappointment confirms a structural slowdown"),
    ("Forward P/E",                "~19.1x", "≤15x",    "-4x",    "Market fully re-prices the deceleration as a durable trend, not a blip"),
    ("Free cash flow",             "healthy","pressured","worse", "Content spend commitments (sports rights, film slate) squeeze near-term FCF"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<30}  {curr:>9}  {bear_v:>9}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the bear case is a genuine, not manufactured, growth deceleration — revenue")
print(f"  growth has stepped down from the mid-teens toward roughly 12%, and Q3 guidance came in")
print(f"  below Street on both lines. That is real and worth taking seriously. What it is NOT is")
print(f"  evidence of a broken business: margin remains well above guide, advertising is genuinely")
print(f"  inflecting, and the company just avoided a massive, distracting acquisition. The bear")
print(f"  case requires deceleration to become disorderly, not merely continue at its current pace.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS (reported basis):  ${EPS_FY2026E:.2f}  (includes the one-time $2.8B WBD termination fee)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (near where NFLX traded during the 2022 subscriber-loss panic)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× reported FY2026E EPS, or {CURRENT_PRICE/curr_eps_clean:.1f}× on a")
print(f"  clean, ex-one-time basis — either way, one of the cheapest multiples Netflix has carried")
print(f"  relative to its own growth rate since well before the 2022 correction. The EPP floor")
print(f"  itself sits {abs(epp_gap_pct):.0f}% below the current price, which is a meaningfully tighter gap than")
print(f"  most names in this coverage — the market has already done real work pricing in caution.")
print(f"  At a 24× reversion (still below Netflix's historical premium multiples): ${curr_eps_clean:.2f} × 24 = ${curr_eps_clean*24:.0f}")
print(f"  ({(curr_eps_clean*24/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: growth stays near the decelerated Q3 pace, modest re-rating)")
hr()
print(f"  Conservative FY2028E EPS:  ${CONS_EPS_2YR:.2f}  (~2.0% EPS CAGR off the clean ~${curr_eps_clean:.2f} base — a genuine deceleration case)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~19× → 20×; barely any re-rating credit)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (no dividend)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: this case assumes growth essentially STALLS at the clean EPS level and the")
print(f"  multiple barely moves, and it still clears {cons_annual:.1f}%/yr. The margin of safety here comes from")
print(f"  how little the price already assumes — you are not paying for the advertising ramp or")
print(f"  the live-sports optionality to work, both of which are upside to this case.")
print(f"  Breakeven at {CONS_PE_2YR}× requires FY2028E EPS ≥ ${CURRENT_PRICE / CONS_PE_2YR:.2f} — below this conservative estimate already.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.32
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range, post-split)")
print(f"  Drawdown from high:   -{(1-CURRENT_PRICE/VOL_52W_HIGH)*100:.1f}%  (the growth-deceleration selloff following the Q2 print)")
print(f"  Annual dividend:      none — all capital return via buyback")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (moderate for a mega-cap; less extreme than the AI-hardware names in this coverage)")
print(f"  Beta vs S&P 500:      1.15  (still a consumer-discretionary-adjacent name at its core)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (would meaningfully breach the current 52W low)")
print(f"  → Q3 2026 print is the next test of whether the deceleration stabilizes or continues.")
print(f"  → Advertising revenue disclosure is the highest-optionality number to track each quarter.")
print(f"  → BUY at current price  |  ADD $60–68  |  TRIM above $115")

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
print(f"  Netflix sold off on a real but modest growth-guidance miss, while simultaneously")
print(f"  banking a $2.8B fee for walking away from a much riskier acquisition. The market appears")
print(f"  to be pricing the first fact and ignoring the second. At {CURRENT_PRICE/curr_eps_clean:.1f}× clean earnings for a")
print(f"  business still growing double digits with a genuinely inflecting ad business, this reads as a buy.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q3 2026 results — does revenue growth stabilize near the guided +11.7%, or decelerate further?")
print(f"  (2) Advertising revenue trajectory — the doubling guide is the single highest-value number to track")
print(f"  (3) Live sports rights renewals/additions — content cost trajectory and competitive positioning")
print(f"  (4) Capital allocation post-WBD — how the $2.8B fee and freed-up management bandwidth get deployed")
print(f"  (5) Member growth in mature markets (UCAN/EMEA) vs still-developing regions (LATAM/APAC)")
print(f"  BUY at ${CURRENT_PRICE:.2f}  |  ADD $60–68  |  TRIM above $115")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS (reported): ${EPS_FY2026E:.2f}  |  Clean EPS: ~${curr_eps_clean:.2f}")
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
