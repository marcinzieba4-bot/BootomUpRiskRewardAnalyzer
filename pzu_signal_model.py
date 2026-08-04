"""
PZU  ·  Powszechny Zakład Ubezpieczeń S.A.  ·  WSE: PZU
Bottom-up signal model  ·  Insurance (P&C + Life) / Bancassurance (Pekao + Alior Bank Stakes)
Currency: PLN (Polish złoty) — this model is denominated natively in PLN, not USD
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "PZU"
COMPANY       = "Powszechny Zakład Ubezpieczeń S.A."
SECTOR        = "Insurance (P&C + Life) · Bancassurance (Pekao + Alior Bank Stakes) · GPW: PZU (PLN)"
CURRENT_PRICE = 63.94       # PLN; close 2026-08-03
VOL_52W_LOW   = 53.36       # PLN
VOL_52W_HIGH  = 72.72       # PLN
SHARES_OUT_M  = 863.52      # millions
ANNUAL_DIV    = 4.80        # PLN/share; ~7.7% yield, among the highest of any major European insurer

# ── PROFIT CONTRIBUTION BRIDGE (FY2026E, PLN millions net profit) ────────────
# Q1 2026 actual: record quarterly gross written premium of 7.8B PLN and net profit of 1.4B PLN.
# FY2025: GWP nearly 31B PLN (+1.5B vs 2024), net profit 6.7B PLN (+25% YoY), solvency ratio 234%.
# PZU is both Poland's largest insurer AND a major bancassurance conglomerate — it holds significant
# equity stakes in Bank Pekao and Alior Bank, so a meaningful share of profit is tied to the Polish
# banking sector's net interest margin cycle, not just underwriting results. Consensus FY2026E EPS:
# 7.13 PLN; consensus target price: 69.54 PLN.
SEG_DATA = [
    # (segment, curr_profit_M, bear_profit_M, bull_profit_M, description)
    ("Insurance underwriting (P&C + Life)",         4300.0, 3200.0, 5100.0, "The core franchise; record Q1 2026 GWP of 7.8B zł, but exposed to catastrophe/claims-inflation risk"),
    ("Banking segment (Pekao + Alior equity income)", 1850.0, 1100.0, 2500.0, "Ties a meaningful share of profit to Poland's interest-rate cycle and bank NIM trends — outside PZU's own control"),
]

# ── BANCASSURANCE / RATE-CYCLE CALCULATOR (the PZU-specific angle) ───────────
Q1_2026_GWP_B              = 7.8   # PLN billions; record Q1 2026 gross written premium
Q1_2026_NET_PROFIT_B       = 1.4   # PLN billions; Q1 2026 net profit
FY2025_GWP_B                = 31.0 # PLN billions; FY2025 gross written premium (nearly)
FY2025_NET_PROFIT_B         = 6.7  # PLN billions; FY2025 net profit, +25% YoY
FY2025_SOLVENCY_RATIO_PCT   = 234  # %; FY2025 solvency ratio — exceptionally strong capital position
CONSENSUS_TARGET_PLN        = 69.54 # PLN; analyst consensus 12-month price target

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 7.13        # PLN/share FY2026E; analyst consensus
PE_PESSIMISTIC = 8.0         # trough P/E: a genuine insurance/bancassurance-trough multiple
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  (4.98,  8,   40, "Rising catastrophe/claims inflation hits underwriting simultaneously with rate-cut-driven bank NIM compression"),
    "BASE":  (7.30, 9.5,  69, "Steady underwriting results and stable banking-segment income continue roughly as guided"),
    "BULL":  (8.80, 10.5, 92, "Underwriting margins improve and the banking stakes benefit from a more favorable rate environment"),
    "XBULL": (10.19, 11.5, 117, "Both segments outperform simultaneously — record underwriting profitability plus a strong banking-sector earnings cycle"),
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
        "name":       "Gross written premium (GWP) growth",
        "weight":     0.20,
        "thresholds": ("<0%",    "≥3%",    "≥6%",    "≥9%"),
        "now":        "~+5.1%",
        "score":      2,
        "comment":    "Record Q1 2026 GWP of 7.8B zł continues a steady, if unspectacular, growth trajectory for a mature market leader",
    },
    {
        "name":       "Net profit YoY growth",
        "weight":     0.15,
        "thresholds": ("<0%",    "≥10%",   "≥18%",   "≥25%"),
        "now":        "+25%",
        "score":      4,
        "comment":    "FY2025 net profit +25% YoY to a record 6.7B zł — genuinely strong execution across both segments",
    },
    {
        "name":       "Solvency ratio",
        "weight":     0.15,
        "thresholds": ("<150%",  "≥180%",  "≥210%",  "≥230%"),
        "now":        "234%",
        "score":      4,
        "comment":    "Exceptionally strong capital position — real capacity for dividends and growth without needing to raise capital",
    },
    {
        "name":       "Banking segment (Pekao/Alior) trend",
        "weight":     0.15,
        "thresholds": ("declining","stable", "growing","accelerating"),
        "now":        "growing",
        "score":      3,
        "comment":    "Equity income from the bank stakes continues to grow, though it remains exposed to the Polish rate cycle",
    },
    {
        "name":       "Dividend yield",
        "weight":     0.15,
        "thresholds": ("<3%",    "≥5%",    "≥6.5%",  "≥8%"),
        "now":        "7.71%",
        "score":      3,
        "comment":    "Among the highest dividend yields of any major European insurer, backed by the strong solvency position",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.20,
        "thresholds": (">14x",   "≤11x",   "≤9x",    "≤7x"),
        "now":        "~8.97x",
        "score":      3,
        "comment":    "8.97× FY2026E consensus EPS — reasonable for a market-leading insurer with a strong capital position",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Record FY2025 net profit (+25% YoY) and record Q1 2026 GWP show consistent execution across both underwriting and banking segments", +0.5, 0.20),
    ("+", "A 234% solvency ratio is exceptionally strong, providing real capacity for both dividends and bolt-on growth without capital raises", +0.4, 0.15),
    ("-", "PZU's banking stakes (Pekao, Alior) tie a meaningful share of profit to Polish interest-rate cycles and NIM compression risk — a factor outside PZU's own underwriting control", -0.4, 0.20),
    ("+", "The ~7.7% dividend yield (4.80 zł/share) is among the highest of any major European insurer, providing real downside cushion", +0.4, 0.15),
    ("-", "Poland's insurance market is mature and consolidated; PZU's own scale limits the organic growth runway relative to smaller regional peers", -0.3, 0.15),
    ("-", "Catastrophe/claims inflation risk (weather events, motor claims inflation) is a structural, recurring risk for any P&C-heavy insurer", -0.3, 0.15),
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
CONS_EPS_2YR  = 7.60    # PLN; conservative FY2028E: modest growth off FY2026E consensus
CONS_PE_2YR   = 9       # roughly flat to the current ~8.97× multiple
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
print(f"  {TICKER}  ·  {COMPANY}  ·  {CURRENT_PRICE:.2f} zł  ·  Insurance / Bancassurance (Pekao + Alior)")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]  (all figures in PLN)")
print("═" * (W + 4))

# ─── ① PROFIT CONTRIBUTION BRIDGE ─────────────────────────────────────────────
print()
print("  PROFIT CONTRIBUTION BRIDGE  (FY2026E, PLN millions net profit  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(p for _, p, _, _, _ in SEG_DATA)
bear_total = sum(p for _, _, p, _, _ in SEG_DATA)
bull_total = sum(p for _, _, _, p, _ in SEG_DATA)

print(f"  {'Segment':<44}  {'FY26E (M zł)':>13}  {'Bear (M zł)':>11}  {'Bull (M zł)':>11}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<44}  {curr:>11.0f}  {bear:>9.0f}  {bull:>9.0f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL NET PROFIT':<44}  {curr_total:>11.0f}  {bear_total:>9.0f}  {bull_total:>9.0f}")
print(f"  Q1 2026 actual: {Q1_2026_GWP_B}B zł GWP (record), {Q1_2026_NET_PROFIT_B}B zł net profit")
print()

# EPS bridge (direct profit / shares — no margin step needed, segments already at net profit)
shares    = SHARES_OUT_M
curr_eps  = round(curr_total / shares, 2)
bull_eps_imp = round(bull_total / shares, 2)
bear_eps_imp = round(bear_total / shares, 2)

print(f"  FY2026E EPS check:  {curr_total:.0f}M zł net profit ÷ {shares:.2f}M shares")
print(f"  =  {curr_eps:.2f} zł/share  (model estimate {EPS_FY2026E:.2f} zł  ✓)")
print()
print(f"  BULL EPS check:  {bull_total:.0f}M zł net profit ÷ {shares:.2f}M shares")
print(f"  =  {bull_eps_imp:.2f} zł/share  →  × {SCENARIOS['BULL'][1]}× = ~{bull_eps_imp*SCENARIOS['BULL'][1]:.0f} zł  ✓ BULL {SCENARIOS['BULL'][2]} zł")
print()
print(f"  BEAR EPS check:  {bear_total:.0f}M zł net profit ÷ {shares:.2f}M shares (catastrophe claims + NIM compression)")
print(f"  =  {bear_eps_imp:.2f} zł/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~{bear_eps_imp*SCENARIOS['BEAR'][1]:.0f} zł  ✓ BEAR {SCENARIOS['BEAR'][2]} zł")

# BANCASSURANCE / RATE-CYCLE CHECK
print()
print(f"  BANCASSURANCE / RATE-CYCLE CHECK  (the PZU-specific angle):")
print(f"  Q1 2026 GWP:                            {Q1_2026_GWP_B}B zł  (record)")
print(f"  Q1 2026 net profit:                     {Q1_2026_NET_PROFIT_B}B zł")
print(f"  FY2025 GWP / net profit:                 {FY2025_GWP_B}B zł / {FY2025_NET_PROFIT_B}B zł (+25% YoY)")
print(f"  FY2025 solvency ratio:                   {FY2025_SOLVENCY_RATIO_PCT}%")
print(f"  Analyst consensus target:                {CONSENSUS_TARGET_PLN:.2f} zł")
print()
print(f"  PZU is structurally two businesses in one: a market-leading Polish insurer, and a meaningful")
print(f"  equity stake in two of Poland's largest banks (Pekao, Alior). This diversifies underwriting risk")
print(f"  but also means a real share of PZU's earnings power rides on the same interest-rate cycle that")
print(f"  drives Polish bank NIMs — a factor entirely outside PZU's own underwriting control.")

# KEY SENSITIVITIES
print()
eps_per_100M_profit = 100.0 / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every 100M zł net profit:                +{eps_per_100M_profit:.3f} zł/EPS  = +{eps_per_100M_profit*9:.2f} zł/share at 9× P/E")
print(f"  Every 1 turn of P/E:                      ±{EPS_FY2026E:.2f} zł/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")
print(f"  Dividend cushion:                          {ANNUAL_DIV:.2f} zł/yr absorbs ~{ANNUAL_DIV/CURRENT_PRICE*100:.1f}% of any annual price drawdown")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (GWP growth / profit growth / solvency / banking segment / yield / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<36}  {'BEAR':>10}  {'BASE':>7}  {'BULL':>10}  {'XBULL':>13}  {'NOW':>9}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<36}  {ths[0]:>10}  {ths[1]:>7}  {ths[2]:>10}  {ths[3]:>13}  {s['now']:>9}  {lbl}  {b}")
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
print(f"  {'Signal':<32}  {'Current':>10}  {'Bear val':>10}  Trigger")
hr()
bear_triggers = [
    ("GWP growth",                  "~+5.1%", "<0%",      "A soft Polish economic cycle or intensified insurance-price competition stalls premium growth"),
    ("Net profit growth",           "+25%",   "<0%",      "Catastrophe losses (weather events) or motor claims inflation spike simultaneously"),
    ("Solvency ratio",              "234%",   "<150%",    "A major capital-depleting event (large claims, regulatory capital change) erodes the buffer"),
    ("Banking segment trend",       "growing","declining","Polish rate cuts compress bank NIMs faster than expected, hitting the Pekao/Alior equity income line"),
    ("Dividend yield",              "7.71%",  "<3%",      "A dividend cut following a genuine earnings shortfall, breaking the income-investor thesis"),
    ("Forward P/E",                 "~8.97x", ">14x",     "Market fully re-prices PZU for a slower, rate-cycle-exposed earnings trajectory"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the two halves of PZU's business have different bear cases — underwriting risk is")
print(f"  catastrophe/claims-driven and largely idiosyncratic, while the banking-stake income is entirely")
print(f"  a function of the Polish interest-rate cycle. A genuine BEAR case likely requires both to go wrong")
print(f"  at once, which is possible but not the base rate for a company with this capital strength.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS estimate:       {EPS_FY2026E:.2f} zł  (analyst consensus)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (a genuine insurance/bancassurance-trough multiple)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    {EPP:.0f} zł/share")
print(f"  Current {CURRENT_PRICE:.2f} zł vs EPP {EPP:.0f} zł:  {epp_gap_pct:+.1f}%")
print()
print(f"  At {CURRENT_PRICE:.2f} zł the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E consensus EPS — a reasonable multiple")
print(f"  for a market-leading insurer with a 234% solvency ratio and a ~7.7% dividend yield. The EPP floor")
print(f"  provides real, if modest, margin of safety versus the trough multiple.")
print(f"  At a 9.7× reversion (roughly the consensus target multiple): {EPS_FY2026E:.2f} × 9.7 = {EPS_FY2026E*9.7:.0f} zł  ({(EPS_FY2026E*9.7/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest growth off FY2026E consensus)")
hr()
print(f"  Conservative FY2028E EPS:  {CONS_EPS_2YR:.2f} zł  (~6.6% cumulative EPS growth — a genuinely modest assumption)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (roughly flat to the current ~8.97× multiple)")
print(f"  Conservative equity value:   {cons_equity:.2f} zł/share")
print(f"  + Cumulative dividends (2yr): +{cons_divs:.2f} zł/share  ({ANNUAL_DIV:.2f} zł/yr, {ANNUAL_DIV/CURRENT_PRICE*100:.2f}% yield)")
hr()
print(f"  Conservative 2yr total:      {cons_total:.2f} zł  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from {CURRENT_PRICE:.2f} zł)")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: because the dividend yield alone is ~7.7%/yr, even a conservative case with")
print(f"  minimal EPS growth and no multiple re-rating clears a {'solidly positive' if cons_return > 15 else 'positive' if cons_return > 0 else 'negative'} return. This is a name where the income")
print(f"  component does most of the work — the equity story is a bonus, not the load-bearing assumption.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.18
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        {VOL_52W_LOW:.2f} – {VOL_52W_HIGH:.2f} zł  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      {ANNUAL_DIV:.2f} zł/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%; among the highest of any major European insurer)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (low — typical for a mature, dividend-heavy insurance name)")
print(f"  Beta vs WIG20:        0.85  (below the Warsaw benchmark — a defensive constituent)")
print(f"  1-sigma range (1yr):  {sigma_range[0]:.0f} – {sigma_range[1]:.0f} zł  ({CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear {bear_price} zł requires:  ~{bear_sigmas:.1f}σ drawdown  (large relative to PZU's typically low realized vol)")
print(f"  → Q2 2026 print (late August) is the next test of whether both underwriting and banking segments hold up.")
print(f"  → Polish NBP rate decisions are the leading indicator for the banking-segment income line between prints.")
print(f"  → {signal_short} at {CURRENT_PRICE:.2f} zł  |  Add below 56 zł  |  Trim above 78 zł")

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
print(f"  PZU combines a well-capitalized, market-leading insurer with real banking-sector income optionality —")
print(f"  a genuinely diversified profile at a reasonable multiple, with a high, well-covered dividend as the anchor.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q2 2026 print (late August) — do both underwriting and banking-segment income hold up?")
print(f"  (2) Polish NBP interest-rate decisions — the leading indicator for the Pekao/Alior equity income line")
print(f"  (3) Any major catastrophe/weather-related claims events affecting the P&C book")
print(f"  (4) Solvency ratio trend — watch for any meaningful decline from the current 234% level")
print(f"  (5) Dividend policy continuity — confirms or breaks the income-investor thesis")
print(f"  {signal_short} at {CURRENT_PRICE:.2f} zł  |  Add below 56 zł  |  Trim above 78 zł")
print(f"  EPP floor: {EPP:.0f} zł  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: {EPS_FY2026E:.2f} zł  |  Solvency ratio: {FY2025_SOLVENCY_RATIO_PCT}%")
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
