"""
XTB  ·  XTB S.A.  ·  WSE: XTB
Bottom-up signal model  ·  Retail CFD / Forex Broker / Investment Products
Currency: PLN (Polish złoty) — this model is denominated natively in PLN, not USD
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "XTB"
COMPANY       = "XTB S.A."
SECTOR        = "Retail CFD / Forex Broker · Investment Products · GPW: XTB (PLN)"
CURRENT_PRICE = 129.40      # PLN; all-time high, close 2026-08-03
VOL_52W_LOW   = 61.86       # PLN
VOL_52W_HIGH  = 129.40      # PLN; stock is AT its 52-week/all-time high today
SHARES_OUT_M  = 117.57      # millions
ANNUAL_DIV    = 4.07        # PLN/share; ~60% payout policy

# ── REVENUE BRIDGE (FY2026E, PLN millions) ────────────────────────────────────
# H1 2026 actual: operating revenue +79.7% YoY to 2.09B PLN; net profit +150.5% YoY to 1.03B PLN.
# Q1 2026 was a record quarter; Q2 2026 net profit 492M PLN, -8% QoQ from Q1 but still the
# second-best quarter ever, beating analyst forecasts and pushing the stock to a fresh ATH (+8.6%
# on the print). Active clients hit a record 1.49M (+74.5% YoY, +333K in Q2 alone). Trading volume
# moderated to $343B/month in Q2 (from $444B/month in Q1), but revenue efficiency actually IMPROVED —
# $238 of trading result per $1M traded, up from $216 in Q1. CFDs generate 96% of trading result;
# investment products (ETFs, stocks) drive client acquisition but are a small revenue contributor today.
SEG_DATA = [
    # (segment, curr_rev_M, bear_rev_M, bull_rev_M, description)
    ("CFD trading (spread/commission revenue)", 3300.0, 1440.0, 4320.0, "96% of trading result; directly tracks volatility and trading volume — the core cyclicality driver"),
    ("Investment products & other (ETFs, interest income)", 370.0, 160.0, 480.0, "Smaller today, but the client-stickiness and re-rating story for the long term"),
]

# Net-margin-based bridge (a broker's costs are mostly fixed opex — extreme operating leverage
# in both directions as trading volume rises and falls)
NET_MARGIN_CURR = 0.493   # FY2026E; matches H1 2026's actual 49.3% net margin (1.03B / 2.09B)
NET_MARGIN_BEAR = 0.300   # BEAR: fixed cost base doesn't shrink with revenue; operating leverage inverts hard
NET_MARGIN_BULL = 0.510   # BULL: further operating leverage as revenue scales past the fixed cost base

# ── BOOM-VS-NORMALIZATION CALCULATOR (the XTB-specific angle) ────────────────
H1_2026_NET_PROFIT_B      = 1.03   # PLN billions; H1 2026 actual net profit, +150.5% YoY
H1_2026_NET_PROFIT_GROWTH = 150.5  # % YoY growth, H1 2026 net profit
ACTIVE_CLIENTS_M          = 1.49   # millions; record active clients, +74.5% YoY
Q2_TRADING_VOL_B_USD      = 343    # $B/month; Q2 2026 trading volume (down from $444B/month in Q1)
Q2_REV_PER_1M_TRADED_USD  = 238    # $ trading result per $1M traded, Q2 2026 (up from $216 in Q1 — efficiency improving even as volume cools)
CFD_PCT_OF_TRADING_RESULT = 96     # % of trading result from CFDs specifically
ANALYST_FY27_EPS_CONSENSUS = 10.22 # PLN; analyst consensus EPS for the NEXT full year — already prices in a large reversion from this year's boom
POST_EARNINGS_POP_PCT     = 8.6    # % single-day stock pop on the Q2 2026 beat

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 15.39       # PLN/share FY2026E; bottom-up from H1 actual (1.03B) + a realistic H2 continuation
PE_PESSIMISTIC = 8.0         # trough P/E: a genuine CFD-broker-trough multiple in a low-volatility environment
EPP            = round(PE_PESSIMISTIC * ANALYST_FY27_EPS_CONSENSUS, 0)  # deliberately uses the NORMALIZED FY2027E consensus, not this year's boom EPS

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 4.08,  8,   33, "A genuine low-volatility/crypto-winter reversion hits trading volume and margins simultaneously, echoing prior CFD-broker down-cycles"),
    "BASE":  (15.39,  8,  123, "Roughly today's earnings power persists at a trough-ish multiple — the market gives no credit for the boom continuing"),
    "BULL":  (20.82, 11,  229, "Elevated volatility and client growth continue longer than the analyst consensus reversion assumes"),
    "XBULL": (27.95, 13,  363, "A full repeat of the 2025-2026 boom — crypto mania, high volatility, and client growth all persist without decelerating"),
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
        "name":       "Net profit YoY growth (H1 2026)",
        "weight":     0.20,
        "thresholds": ("<20%",   "≥50%",   "≥100%",  "≥140%"),
        "now":        "+150.5%",
        "score":      4,
        "comment":    "H1 net profit more than doubled YoY to 1.03B PLN — an extraordinary result even by XTB's own volatile history",
    },
    {
        "name":       "Active client growth YoY",
        "weight":     0.15,
        "thresholds": ("<15%",   "≥30%",   "≥50%",   "≥70%"),
        "now":        "+74.5%",
        "score":      4,
        "comment":    "1.49M active clients, a record, growing faster than at any point in the company's history",
    },
    {
        "name":       "Revenue efficiency ($/1M traded)",
        "weight":     0.15,
        "thresholds": ("<180",   "≥200",   "≥220",   "≥240"),
        "now":        "$238",
        "score":      3,
        "comment":    "Up from $216 in Q1 — monetization per unit of trading volume is improving even as raw volume cools",
    },
    {
        "name":       "Trading volume trend (QoQ)",
        "weight":     0.15,
        "thresholds": ("<-30%",  "≥-25%",  "≥-10%",  "≥0%"),
        "now":        "-22.7%",
        "score":      2,
        "comment":    "$343B/month in Q2, down from $444B/month in Q1 — the clearest early signal that the boom is cooling",
    },
    {
        "name":       "ESMA / regulatory risk environment",
        "weight":     0.15,
        "thresholds": ("new restrictions","review pending","stable","favorable"),
        "now":        "stable",
        "score":      3,
        "comment":    "No new EU leverage-restriction proposals currently active, but this is a structural, recurring industry risk",
    },
    {
        "name":       "Forward P/E (on normalized FY2027E)",
        "weight":     0.20,
        "thresholds": (">20x",   "≤16x",   "≤13x",   "≤10x"),
        "now":        "~12.7x",
        "score":      3,
        "comment":    "12.7× on the analyst FY2027E consensus (10.22 PLN) — reasonable, not dirt cheap, on a normalized post-boom earnings basis",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "H1 2026's 150.5% net profit growth and record client base are real, audited results — not guidance or promotion", +0.5, 0.20),
    ("-", "Analyst FY2027E consensus (10.22 PLN) already prices a ~34% reversion from this year's bottom-up run-rate — informed opinion doesn't expect the boom to persist", -0.5, 0.20),
    ("-", "CFD brokerage is a structurally cyclical, volatility-dependent business with a well-documented history of boom-bust earnings at XTB specifically", -0.5, 0.20),
    ("+", "Revenue efficiency ($238/1M traded) improving even as raw volume cools is a genuinely good sign — this isn't purely a volume story", +0.3, 0.15),
    ("+", "~60% dividend payout policy and a real yield provide some downside cushion uncommon among high-beta brokers", +0.3, 0.10),
    ("-", "ESMA leverage restrictions are a recurring, structural regulatory overhang across the entire European CFD industry, not unique to XTB but real", -0.3, 0.15),
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
CONS_EPS_2YR  = 10.22   # PLN; uses the analyst FY2027E consensus directly as the conservative 2yr assumption — no further growth credited
CONS_PE_2YR   = 10      # a modest re-rating from the trough 8x as some of today's franchise gains (client base, brand) prove durable
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
print(f"  {TICKER}  ·  {COMPANY}  ·  {CURRENT_PRICE:.2f} zł  ·  Retail CFD / Forex Broker (all-time high)")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]  (all figures in PLN)")
print("═" * (W + 4))

# ─── ① REVENUE BRIDGE ─────────────────────────────────────────────────────────
print()
print("  REVENUE BRIDGE  (FY2026E, PLN millions  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<50}  {'FY26E (M zł)':>13}  {'Bear (M zł)':>11}  {'Bull (M zł)':>11}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<50}  {curr:>11.0f}  {bear:>9.0f}  {bull:>9.0f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<50}  {curr_total:>11.0f}  {bear_total:>9.0f}  {bull_total:>9.0f}")
print(f"  H1 2026 actual: 2,090M zł revenue (+79.7% YoY), 1,030M zł net profit (+150.5% YoY)")
print()

# EPS bridge (net-margin based)
shares    = SHARES_OUT_M
curr_net  = curr_total * NET_MARGIN_CURR
curr_eps  = round(curr_net / shares, 2)

bull_net  = bull_total * NET_MARGIN_BULL
bull_eps_imp = round(bull_net / shares, 2)

bear_net  = bear_total * NET_MARGIN_BEAR
bear_eps_imp = round(bear_net / shares, 2)

print(f"  FY2026E EPS check:  {curr_total:.0f}M zł rev × {NET_MARGIN_CURR*100:.1f}% net margin")
print(f"  ÷ {shares:.2f}M shares  =  {curr_eps:.2f} zł/share  (model estimate {EPS_FY2026E:.2f} zł  ✓)")
print()
print(f"  BULL EPS check:  {bull_total:.0f}M zł rev × {NET_MARGIN_BULL*100:.1f}% net margin")
print(f"  =  ~{bull_eps_imp:.2f} zł/share  →  × {SCENARIOS['BULL'][1]}× = ~{bull_eps_imp*SCENARIOS['BULL'][1]:.0f} zł  ✓ BULL {SCENARIOS['BULL'][2]} zł")
print()
print(f"  BEAR EPS check:  {bear_total:.0f}M zł rev × {NET_MARGIN_BEAR*100:.1f}% net margin (fixed opex base inverts operating leverage)")
print(f"  =  ~{bear_eps_imp:.2f} zł/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~{bear_eps_imp*SCENARIOS['BEAR'][1]:.0f} zł  ✓ BEAR {SCENARIOS['BEAR'][2]} zł")

# BOOM-VS-NORMALIZATION CHECK
print()
print(f"  BOOM-VS-NORMALIZATION CHECK  (the XTB-specific angle):")
print(f"  H1 2026 net profit:                    {H1_2026_NET_PROFIT_B:.2f}B zł  (+{H1_2026_NET_PROFIT_GROWTH:.1f}% YoY)")
print(f"  Active clients:                         {ACTIVE_CLIENTS_M:.2f}M  (+74.5% YoY, record)")
print(f"  Q2 trading volume:                      ${Q2_TRADING_VOL_B_USD}B/month  (down from $444B/month in Q1)")
print(f"  Q2 revenue per $1M traded:               ${Q2_REV_PER_1M_TRADED_USD}  (up from $216 in Q1 — efficiency improving)")
print(f"  CFD share of trading result:            {CFD_PCT_OF_TRADING_RESULT}%")
print(f"  Analyst FY2027E EPS consensus:           {ANALYST_FY27_EPS_CONSENSUS:.2f} zł  (implies a large reversion from this year's run-rate)")
print(f"  Post-Q2-earnings stock reaction:        +{POST_EARNINGS_POP_PCT:.1f}%  (fresh all-time high)")
print()
print(f"  This is the central tension in owning XTB today: the stock trades at a genuinely modest multiple")
print(f"  of THIS YEAR's earnings power, but that earnings power is the product of an extraordinary volatility")
print(f"  and client-growth environment that both the analyst community and XTB's own trading history suggest")
print(f"  won't simply repeat. The bear case isn't a story problem — it's a base-rate problem for CFD brokers.")

# KEY SENSITIVITIES
print()
eps_per_100M_rev = 100.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every 100M zł revenue (at 49.3% margin):  +{eps_per_100M_rev:.3f} zł/EPS  = +{eps_per_100M_rev*10:.2f} zł/share at 10× P/E")
print(f"  Every 1pp of net margin:                   +{curr_total*0.01/shares:.3f} zł/EPS  = +{curr_total*0.01/shares*10:.2f} zł/share at 10× P/E")
print(f"  Every 1 turn of P/E:                       ±{EPS_FY2026E:.2f} zł/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (net profit growth / clients / efficiency / volume / regulatory / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<38}  {'BEAR':>17}  {'BASE':>15}  {'BULL':>7}  {'XBULL':>9}  {'NOW':>10}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<38}  {ths[0]:>17}  {ths[1]:>15}  {ths[2]:>7}  {ths[3]:>9}  {s['now']:>10}  {lbl}  {b}")
    print(f"    {s['comment']}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from {CURRENT_PRICE} zł + 15%/yr hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:88]:<88}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR {bear_price} zł)")
hr()
print(f"  {'Signal':<32}  {'Current':>14}  {'Bear val':>14}  Trigger")
hr()
bear_triggers = [
    ("Net profit YoY",              "+150.5%",       "<20%",           "A low-vol/crypto-winter reversion hits simultaneously, echoing prior XTB down-cycles"),
    ("Active client growth",        "+74.5%",        "<15%",           "New client acquisition slows sharply as the current promotional/marketing cycle fades"),
    ("Revenue efficiency",          "$238/1M",       "<$180/1M",       "Spread compression from competition or lower realized volatility per trade"),
    ("Trading volume (QoQ)",        "-22.7%",        "<-30%",          "Volume decline accelerates rather than stabilizing, confirming the cyclical peak has passed"),
    ("ESMA/regulatory risk",        "stable",        "new restrictions","A fresh EU leverage-restriction proposal directly compresses CFD revenue per client"),
    ("Forward P/E (normalized)",    "~12.7x",        ">20x",           "Ironically, P/E can rise even as price falls if EPS reverts faster than price does"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>14}  {bear_v:>14}  {trigger[:42]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: XTB's own multi-year history is the bear case's best evidence — this is a company")
print(f"  whose earnings have swung wildly with market volatility before, and the Q2 QoQ volume decline")
print(f"  (-22.7%) is the first concrete data point suggesting the current boom has already peaked, even as")
print(f"  monetization efficiency improvements are (so far) offsetting it at the earnings line.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × NORMALIZED forward EPS)")
hr()
print(f"  Normalized FY2027E EPS estimate:  {ANALYST_FY27_EPS_CONSENSUS:.2f} zł  (analyst consensus — deliberately NOT this year's boom EPS of {EPS_FY2026E:.2f})")
print(f"  Pessimistic P/E at trough:          {PE_PESSIMISTIC:.0f}×  (a genuine CFD-broker-trough multiple)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    {EPP:.0f} zł/share")
print(f"  Current {CURRENT_PRICE:.2f} zł vs EPP {EPP:.0f} zł:  {epp_gap_pct:+.1f}%")
print()
print(f"  This EPP intentionally uses next year's ALREADY-DISCOUNTED consensus EPS, not this year's boom")
print(f"  number — because the whole point of an earnings-power floor is durability, and {EPS_FY2026E:.2f} zł/share is")
print(f"  not a number anyone, including XTB's own covering analysts, expects to repeat automatically.")
print(f"  At a 10× reversion on THIS year's actual EPS (a real premium): {EPS_FY2026E:.2f} × 10 = {EPS_FY2026E*10:.0f} zł  ({(EPS_FY2026E*10/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: uses the analyst FY2027E consensus directly, no further growth credited)")
hr()
print(f"  Conservative FY2028E EPS:  {CONS_EPS_2YR:.2f} zł  (= the FY2027E consensus itself — zero credit for continued growth)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (a modest premium to the 8× trough, crediting some durable franchise value)")
print(f"  Conservative equity value:   {cons_equity:.2f} zł/share")
print(f"  + Cumulative dividends (2yr): +{cons_divs:.2f} zł/share  ({ANNUAL_DIV:.2f} zł/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      {cons_total:.2f} zł  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from {CURRENT_PRICE:.2f} zł)")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: even taking the analyst community's own post-boom normalization at face value and")
print(f"  crediting zero further growth, the conservative case is {'still clearly negative' if cons_return < -10 else 'roughly flat-to-negative' if cons_return < 5 else 'still positive'} — because so much of today's price already")
print(f"  requires either the boom to persist or a durable re-rating that hasn't been earned yet.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.55
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        {VOL_52W_LOW:.2f} – {VOL_52W_HIGH:.2f} zł  (stock at its 52-week/all-time high today)")
print(f"  Annual dividend:      {ANNUAL_DIV:.2f} zł/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; ~60% payout policy)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (very high — a small-cap CFD broker with genuine boom-bust earnings history)")
print(f"  Beta vs WIG20:        1.40  (well above the Warsaw benchmark)")
print(f"  1-sigma range (1yr):  {sigma_range[0]:.0f} – {sigma_range[1]:.0f} zł  ({CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear {bear_price} zł requires:  ~{bear_sigmas:.1f}σ drawdown  (large, but well within XTB's own historical range of moves)")
print(f"  → Q3 2026 print (likely early November) is the next test of whether trading volume stabilizes or keeps declining QoQ.")
print(f"  → Monthly trading-volume disclosures and active-client-growth updates are the leading indicators between prints.")
print(f"  → {signal_short} at {CURRENT_PRICE:.2f} zł  |  Add below 95 zł  |  Trim above 160 zł")

# ─── ⑦ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print()
print("  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
hr()
probs_mkt = softmax_probs(MARKET_COMPOSITE)
print(f"  {'Scenario':<10}  {'Price':>9}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>7}  Description")
hr()
for s in ["BEAR","BASE","BULL","XBULL"]:
    pp  = probs_proxy[s] * 100
    pm  = probs_mkt[s]   * 100
    gap = pp - pm
    pr  = SCENARIOS[s][2]
    desc = SCENARIOS[s][3][:44]
    print(f"  {s:<10}  {pr:>6} zł  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): {ev_adj:.0f} zł  /  Proxy EV: {ev_prx:.0f} zł  /  Market EV: {ev_mkt:.0f} zł  /  Current: {CURRENT_PRICE:.0f} zł")
hr()
print(f"  Downside  (→ Bear {bear_price} zł):  {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull {bull_price} zł):  {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b_str}")
print(f"  Signal    :  {signal_full}")
print()
print(f"  MARKET PRICING: at {CURRENT_PRICE:.2f} zł the market composite is {MARKET_COMPOSITE:.2f}/4.0. The model's")
print(f"  adjusted composite is {ADJ_COMPOSITE:.2f}/4.0, for a gap of {ADJ_GAP:+.2f} — {valuation_label.lower()}.")
print(f"  XTB's H1 2026 results are genuinely extraordinary, and the stock isn't expensive against them —")
print(f"  the real question this signal can't fully resolve is whether 2026 is XTB's new normal or its peak.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q3 2026 print (likely early November) — does trading volume stabilize or keep declining QoQ?")
print(f"  (2) Monthly trading-volume and active-client disclosures — the leading indicators between prints")
print(f"  (3) Any new ESMA or national-regulator leverage-restriction proposals across the EU CFD industry")
print(f"  (4) Investment-products (ETF/stock) platform growth — the longer-term client-stickiness story")
print(f"  (5) Whether analyst FY2027E estimates get revised up or down as more 2026 data lands")
print(f"  {signal_short} at {CURRENT_PRICE:.2f} zł  |  Add below 95 zł  |  Trim above 160 zł")
print(f"  EPP floor: {EPP:.0f} zł  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: {EPS_FY2026E:.2f} zł  |  FY2027E consensus: {ANALYST_FY27_EPS_CONSENSUS:.2f} zł")
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
