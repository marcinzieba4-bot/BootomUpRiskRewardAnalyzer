"""
CDR  ·  CD Projekt S.A.  ·  GPW (Warsaw Stock Exchange): CDR
Bottom-up signal model  ·  Video Game Publishing / Cyberpunk & Witcher Catalog / Witcher 4 & Cyberpunk 2 Optionality
Currency: PLN (Polish złoty) — this model is denominated natively in PLN, not USD
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "CDR"
COMPANY       = "CD Projekt S.A."
SECTOR        = "Video Game Publishing · Cyberpunk & Witcher Catalog · GPW: CDR (PLN)"
CURRENT_PRICE = 249.90      # PLN; close 2026-08-02 on the Warsaw Stock Exchange
VOL_52W_LOW   = 211.30      # PLN, 2025/26 trough
VOL_52W_HIGH  = 297.00      # PLN, 2026 peak
SHARES_OUT_M  = 99.8        # millions; ~24.95B PLN mkt cap / 249.90 PLN
ANNUAL_DIV    = 0.0         # PLN/share; 2025 net profit retained in full for Witcher 4/Cyberpunk 2 development (no 2026 dividend)

# ── REVENUE BRIDGE (FY2026E, PLN millions) ────────────────────────────────────
# Q1 2026 actual (ex-GOG, divested in 2025): revenue 191M PLN (+6% YoY), net profit 106M PLN (56% net
# margin). Cyberpunk franchise (2077 + Phantom Liberty) generated 140.1M PLN (-4% YoY) — still the
# largest single contributor five years post-launch, on 35M+ base units and 10M+ Phantom Liberty units
# (45M combined). The Witcher franchise generated 44.7M PLN (+36% YoY), reaccelerating on The Witcher 3
# crossing 65M lifetime copies (+5M in the past year) and a newly announced "Songs of the Past"
# expansion for a decade-old game. FY2025: revenue 867M PLN (+9%), net profit 595M PLN (2nd-best year
# ever, boosted by a one-off GOG divestment gain). Cash/deposits/bonds: >1.4B PLN at end of Q1 2026.
SEG_DATA = [
    # (segment, curr_rev_M, bear_rev_M, bull_rev_M, description)
    ("Cyberpunk franchise (2077 + Phantom Liberty)", 550.0, 400.0, 620.0, "45M lifetime units; -4% YoY in Q1 — a remarkably mild decay five years post-launch, but no new content catalyst until Cyberpunk 2 (Orion)"),
    ("Witcher franchise + catalog/other (Gwent, licensing)", 309.0, 230.0, 420.0, "Witcher 3 at 65M+ lifetime units, +36% YoY on the new 'Songs of the Past' expansion — genuine reacceleration in a decade-old game"),
]

# Net-margin-based bridge (game publishers run high, opex-driven margins — most costs are
# capitalized/amortized development spend rather than a classic COGS/opex split)
NET_MARGIN_CURR = 0.529   # FY2026E; matches Q1 2026's 56% margin, moderated for the full year
NET_MARGIN_BEAR = 0.420   # BEAR: fixed Witcher 4/Cyberpunk 2 development spend keeps running while catalog revenue shrinks
NET_MARGIN_BULL = 0.580   # BULL: operating leverage improves as the "Songs of the Past" DLC and steady catalog sales scale

# ── WITCHER 4 / CYBERPUNK 2 OPTIONALITY CALCULATOR (the CDR-specific angle) ──
CYBERPUNK_LIFETIME_UNITS_M   = 45.0   # million units; Cyberpunk 2077 + Phantom Liberty combined lifetime sales
WITCHER3_LIFETIME_UNITS_M    = 65.0   # million units; The Witcher 3 lifetime sales (+5M in the past year alone)
NET_CASH_PLN_B               = 1.4    # PLN billions; cash + bank deposits + bonds at end of Q1 2026
NET_CASH_PCT_OF_MKTCAP       = 5.6    # % of ~25B PLN market cap held in net cash
WITCHER4_DEV_STAGE           = "full-scale production"  # per management commentary, 250+ developers assigned
WITCHER4_EARLIEST_WINDOW     = "2027"  # earliest plausible release window; not before end of 2026 per management
CYBERPUNK2_STUDIO            = "Boston (CDPR)"  # development studio for Cyberpunk 2 / Project Orion; no date given
CYBERPUNK_2020_LAUNCH_DRAWDOWN_PCT = 67  # % peak-to-trough stock drawdown after the disastrous Dec-2020 Cyberpunk 2077 launch — the precedent this bear case echoes

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 4.55        # PLN/share FY2026E; current analyst consensus
PE_PESSIMISTIC = 20.0        # trough P/E: close to where CDR traded after the 2020 Cyberpunk launch crisis
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E; Witcher 4/Cyberpunk 2 not expected to have shipped yet) ─
SCENARIOS = {
    "BEAR":  (2.65, 28,  74,  "Anticipation cools on delays or scope-risk headlines, echoing the 2020 Cyberpunk launch trauma; catalog decays faster than guided"),
    "BASE":  (4.55, 55, 250,  "Catalog revenue holds roughly flat; Witcher 4/Cyberpunk 2 development proceeds without major news either way"),
    "BULL":  (6.04, 48, 290,  "Catalog outperforms on continued Witcher 3 DLC success and resilient Cyberpunk sales; Witcher 4 marketing momentum builds"),
    "XBULL": (6.98, 52, 363,  "A confirmed Witcher 4 release window with strong early reception buzz, plus a breakout 'Songs of the Past' performance, re-rates the stock on pure anticipation"),
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
        "weight":     0.15,
        "thresholds": ("<0%",    "≥3%",    "≥8%",    "≥15%"),
        "now":        "+6%",
        "score":      2,
        "comment":    "Modest catalog growth — solid for a publisher with no new release this year, but not evidence of anything beyond steady-state",
    },
    {
        "name":       "Witcher franchise reacceleration",
        "weight":     0.15,
        "thresholds": ("<0%",    "≥15%",   "≥25%",   "≥35%"),
        "now":        "+36%",
        "score":      4,
        "comment":    "The Witcher 3, over a decade old, just crossed 65M lifetime units and grew 36% YoY on the new 'Songs of the Past' expansion — genuinely unusual durability",
    },
    {
        "name":       "Cyberpunk franchise decay rate",
        "weight":     0.15,
        "thresholds": ("<-20%",  "≥-15%",  "≥-8%",   "≥0%"),
        "now":        "-4%",
        "score":      3,
        "comment":    "A -4% YoY decline five years post-launch is remarkably mild for a single-player game with no major new DLC this year",
    },
    {
        "name":       "Witcher 4 (Polaris) development stage",
        "weight":     0.20,
        "thresholds": ("delayed/paused","pre-production","full-scale production","window confirmed"),
        "now":        "full-scale production",
        "score":      3,
        "comment":    "250+ developers assigned and past pre-production, but no confirmed release window — the earliest plausible date is 2027",
    },
    {
        "name":       "Net cash position (% of mkt cap)",
        "weight":     0.10,
        "thresholds": ("<2%",    "≥4%",    "≥6%",    "≥9%"),
        "now":        "~5.6%",
        "score":      2,
        "comment":    "1.4B+ PLN in cash/deposits/bonds funds development without dilution risk — a real, if modest, cushion",
    },
    {
        "name":       "Forward P/E",
        "weight":     0.25,
        "thresholds": (">50x",   "≤50x",   "≤35x",   "≤20x"),
        "now":        "~54.9x",
        "score":      1,
        "comment":    "54.9× FY2026E EPS — a rich multiple for a company with no major release inside the next 12+ months; this is the central valuation question",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Witcher 3's reacceleration to +36% YoY with 65M+ lifetime units and a new expansion is genuine, quantified evidence the catalog has unusual staying power", +0.5, 0.20),
    ("-", "Witcher 4 (Polaris) and Cyberpunk 2 (Orion) — the two catalysts the current multiple really prices — are both 1.5-3+ years away, with real execution risk given the 2020 Cyberpunk launch precedent", -0.6, 0.25),
    ("-", "At ~55x forward earnings, the stock already prices in substantial optionality value for games that haven't shipped a single review yet", -0.5, 0.20),
    ("+", "1.4B+ PLN net cash (>5.6% of market cap) funds development without dilution risk and provides a real, if modest, downside cushion", +0.3, 0.15),
    ("+", "Cyberpunk 2077's -4% YoY decline is remarkably mild five years post-launch — evidence of unusually durable single-player catalog economics", +0.3, 0.10),
    ("-", "Analyst consensus is genuinely split (5 buy / 6 sell / 5 hold) with an average target below the current price — informed opinion has no strong conviction either way", -0.2, 0.10),
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
CONS_EPS_2YR  = 3.80    # PLN; conservative FY2028E — catalog decay outpaces DLC-driven growth without a shipped Witcher 4/Cyberpunk 2
CONS_PE_2YR   = 40      # a real de-rating from ~54.9× as anticipation fatigue sets in absent a confirmed release window
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
print(f"  {TICKER}  ·  {COMPANY}  ·  {CURRENT_PRICE:.2f} zł  ·  Cyberpunk & Witcher Catalog / Witcher 4 Optionality")
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
print(f"  Q1 2026 actual: 191M zł (+6% YoY). Cyberpunk 140.1M zł (-4%), Witcher 44.7M zł (+36%)")
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
print(f"  ÷ {shares:.1f}M shares  =  {curr_eps:.2f} zł/share  (model estimate {EPS_FY2026E:.2f} zł  ✓)")
print()
print(f"  BULL EPS check:  {bull_total:.0f}M zł rev × {NET_MARGIN_BULL*100:.1f}% net margin")
print(f"  =  ~{bull_eps_imp:.2f} zł/share  →  × {SCENARIOS['BULL'][1]}× = ~{bull_eps_imp*SCENARIOS['BULL'][1]:.0f} zł  ✓ BULL {SCENARIOS['BULL'][2]} zł")
print()
print(f"  BEAR EPS check:  {bear_total:.0f}M zł rev × {NET_MARGIN_BEAR*100:.1f}% net margin (fixed Witcher 4/Cyberpunk 2 dev spend keeps running)")
print(f"  =  ~{bear_eps_imp:.2f} zł/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~{bear_eps_imp*SCENARIOS['BEAR'][1]:.0f} zł  ✓ BEAR {SCENARIOS['BEAR'][2]} zł")

# WITCHER 4 / CYBERPUNK 2 OPTIONALITY CHECK
print()
print(f"  WITCHER 4 / CYBERPUNK 2 OPTIONALITY CHECK  (the CDR-specific angle):")
print(f"  Cyberpunk lifetime units:              {CYBERPUNK_LIFETIME_UNITS_M:.0f}M  (2077 base + Phantom Liberty combined)")
print(f"  Witcher 3 lifetime units:               {WITCHER3_LIFETIME_UNITS_M:.0f}M  (+5M in the past year alone)")
print(f"  Net cash position:                      {NET_CASH_PLN_B:.1f}B zł  (~{NET_CASH_PCT_OF_MKTCAP:.1f}% of market cap)")
print(f"  Witcher 4 (Polaris) dev stage:           {WITCHER4_DEV_STAGE}  (earliest plausible window: {WITCHER4_EARLIEST_WINDOW}+)")
print(f"  Cyberpunk 2 (Orion) dev studio:          {CYBERPUNK2_STUDIO}  (no date given; follows Witcher 4)")
print(f"  2020 Cyberpunk launch drawdown (precedent): -{CYBERPUNK_2020_LAUNCH_DRAWDOWN_PCT}%  peak-to-trough")
print()
print(f"  This is fundamentally a 'waiting' story: the current ~55x multiple is not being paid for today's")
print(f"  catalog earnings power, it's being paid for optionality on two games that are both years from")
print(f"  release. The single most important historical data point is the 2020 Cyberpunk 2077 launch itself —")
print(f"  a technically troubled release erased two-thirds of the stock's value almost overnight. Anyone")
print(f"  buying CDR today is underwriting both the wait AND the execution risk when Witcher 4 finally ships.")

# KEY SENSITIVITIES
print()
eps_per_100M_rev = 100.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every 100M zł revenue (at 52.9% margin):  +{eps_per_100M_rev:.3f} zł/EPS  = +{eps_per_100M_rev*55:.2f} zł/share at 55× P/E")
print(f"  Every 1pp of net margin:                   +{curr_total*0.01/shares:.3f} zł/EPS  = +{curr_total*0.01/shares*55:.2f} zł/share at 55× P/E")
print(f"  Every 1 turn of P/E:                       ±{EPS_FY2026E:.2f} zł/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (revenue / Witcher reaccel / Cyberpunk decay / Witcher 4 stage / cash / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<36}  {'BEAR':>15}  {'BASE':>14}  {'BULL':>21}  {'XBULL':>17}  {'NOW':>22}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<36}  {ths[0]:>15}  {ths[1]:>14}  {ths[2]:>21}  {ths[3]:>17}  {s['now']:>22}  {lbl}  {b}")
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
print(f"  {'Signal':<32}  {'Current':>18}  {'Bear val':>18}  Trigger")
hr()
bear_triggers = [
    ("Total revenue YoY",           "+6%",             "<0%",              "The catalog rolls over without any new content to offset natural decay"),
    ("Witcher reacceleration",      "+36%",            "<0%",              "'Songs of the Past' underperforms and Witcher 3 sales normalize back to a typical decade-old-game decay curve"),
    ("Cyberpunk decay rate",        "-4%",             "<-20%",            "Catalog interest fades faster as attention shifts entirely to anticipation for Cyberpunk 2"),
    ("Witcher 4 dev stage",         "full production",  "delayed/paused",  "A public delay announcement, echoing the pattern of past CDPR development timelines slipping"),
    ("Net cash position",           "~5.6% of mktcap",  "<2%",              "Development costs for two simultaneous AAA titles burn through the cash cushion faster than expected"),
    ("Forward P/E",                 "~54.9x",          ">70x or re-rated down","Either euphoria peaks right before a disappointment, or sentiment craters on bad news"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>18}  {bear_v:>18}  {trigger[:40]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: CDR's own history is the bear case's strongest evidence — the December 2020 Cyberpunk")
print(f"  2077 launch, following years of hype and a rich pre-launch multiple, wiped out two-thirds of the")
print(f"  stock's value in weeks. Nothing about Witcher 4's current 'full-scale production' status rules out")
print(f"  a repeat; the market is pricing meaningfully less caution today than the company's own precedent warrants.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E EPS estimate:       {EPS_FY2026E:.2f} zł  (current analyst consensus)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (close to where CDR traded after the 2020 Cyberpunk launch crisis)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    {EPP:.0f} zł/share")
print(f"  Current {CURRENT_PRICE:.2f} zł vs EPP {EPP:.0f} zł:  {epp_gap_pct:+.1f}%")
print()
print(f"  At {CURRENT_PRICE:.2f} zł the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS — almost entirely an optionality")
print(f"  premium on games that haven't shipped. The EPP floor reflects what the stock has actually traded at")
print(f"  during a real crisis of confidence in CDPR's execution — not a hypothetical distress scenario.")
print(f"  At a 35× reversion (a 'no major catalyst yet' steady-state multiple): {EPS_FY2026E:.2f} × 35 = {EPS_FY2026E*35:.0f} zł  ({(EPS_FY2026E*35/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: catalog decay outpaces DLC growth, no shipped Witcher 4/Cyberpunk 2)")
hr()
print(f"  Conservative FY2028E EPS:  {CONS_EPS_2YR:.2f} zł  (below FY2026E — catalog decay assumed to outpace the 'Songs of the Past' boost)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~54.9× → 40×; a real de-rating as anticipation fatigue sets in)")
print(f"  Conservative equity value:   {cons_equity:.2f} zł/share")
print(f"  + Cumulative dividends (2yr): +{cons_divs:.2f} zł/share  (no dividend — 2025 profit retained for Witcher 4/Cyberpunk 2 development)")
hr()
print(f"  Conservative 2yr total:      {cons_total:.2f} zł  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from {CURRENT_PRICE:.2f} zł)")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: this is deliberately the scenario where the market gives ZERO credit to the")
print(f"  Witcher 4/Cyberpunk 2 pipeline reaching FY2028E without having shipped either game — and it's")
print(f"  clearly {'negative' if cons_return < -10 else 'flat-to-negative' if cons_return < 5 else 'positive'}. That's the core tension in owning CDR: you are paying up front for optionality that,")
print(f"  by design, has not yet been proven out, on a stock with a well-documented history of disappointing")
print(f"  investors at exactly the moment that optionality was supposed to convert.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.45
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        {VOL_52W_LOW:.2f} – {VOL_52W_HIGH:.2f} zł  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      0.00 zł/share  (2025 profit retained; policy targets 25%+ payout resuming within 5 years or buybacks)")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (high — gaming stocks with binary release catalysts trade with elevated, event-driven volatility)")
print(f"  Beta vs WIG20:        1.35  (well above the Warsaw benchmark; CDR is a large, high-beta constituent)")
print(f"  1-sigma range (1yr):  {sigma_range[0]:.0f} – {sigma_range[1]:.0f} zł  ({CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear {bear_price} zł requires:  ~{bear_sigmas:.1f}σ drawdown  (large, but smaller than the 2020 post-launch crash itself)")
print(f"  → No near-term print moves the thesis much — the real catalyst is a Witcher 4 release-window confirmation, likely 2027+.")
print(f"  → Quarterly catalog revenue trends (Cyberpunk decay rate, Witcher DLC uptake) are the leading indicators between now and then.")
print(f"  → {signal_short} at {CURRENT_PRICE:.2f} zł  |  Add below 180 zł  |  Trim above 280 zł")

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
print(f"  CD Projekt's catalog (Cyberpunk + Witcher) is genuinely durable, and the balance sheet is strong —")
print(f"  but the stock's ~55x multiple is a bet on two unreleased games clearing a bar the company has")
print(f"  missed once before, at real cost, within recent memory.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Any Witcher 4 (Polaris) release-window confirmation — the single biggest re-rating catalyst either way")
print(f"  (2) 'Songs of the Past' Witcher 3 expansion reception and sales — the nearest-term data point")
print(f"  (3) Cyberpunk 2077/Phantom Liberty quarterly decay rate — watch for any acceleration beyond -4% YoY")
print(f"  (4) Cyberpunk 2 (Orion) development updates from the Boston studio")
print(f"  (5) Cash burn rate as two AAA titles are developed simultaneously — the balance-sheet cushion isn't unlimited")
print(f"  {signal_short} at {CURRENT_PRICE:.2f} zł  |  Add below 180 zł  |  Trim above 280 zł")
print(f"  EPP floor: {EPP:.0f} zł  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: {EPS_FY2026E:.2f} zł  |  Net cash: {NET_CASH_PLN_B:.1f}B zł")
print("═" * (W + 4))
print()

# ── EXPORT ────────────────────────────────────────────────────────────────────
RESULT = {
    "ticker":            TICKER,
    "signal":            signal_full,
    "signal_short":      signal_short,
    "price":             CURRENT_PRICE,
    "currency":          "PLN",
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
