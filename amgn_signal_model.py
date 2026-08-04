"""
AMGN  ·  Amgen Inc.  ·  NASDAQ: AMGN
Bottom-up signal model  ·  Inflammation/Oncology / Rare Disease (Horizon) / Bone (Repatha/Prolia/Evenity) / MariTide (Obesity)
Date: 2026-08-04
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "AMGN"
COMPANY       = "Amgen Inc."
SECTOR        = "Biotechnology · Inflammation/Oncology · Rare Disease (Horizon/UPLIZNA) · Cardiometabolic (Repatha/Prolia/Evenity) · Obesity Pipeline (MariTide) · NASDAQ: AMGN"
CURRENT_PRICE = 378.87      # USD; close 2026-08-03
VOL_52W_LOW   = 269.77      # USD
VOL_52W_HIGH  = 398.00      # USD
SHARES_OUT_M  = 539.7       # millions
ANNUAL_DIV    = 10.08       # $/share; raised; 14+ yrs of dividend increases

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# ⚠ Q2 2026 earnings report TONIGHT (Aug 4, after close, 4:30pm ET call) — not yet public.
# This model is built on Q1 2026 actuals (EPS $5.15, beat consensus $4.77) and FY2026
# guidance raised with Q1: revenue $37.1-38.5B, non-GAAP EPS $21.70-23.10. UPLIZNA +188%
# YoY is a standout; Repatha hit a new sales run-rate; legacy Enbrel/Otezla continue
# declining. MariTide's Phase 3 MARITIME-SWITCH study was expanded with encouraging
# tolerability data (lower nausea/vomiting vs earlier readouts) — a genuine positive update.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Repatha/Prolia/Evenity (bone+CV)",   15.0, 12.0, 16.5, "Repatha (PCSK9) hit a new sales run-rate; Prolia facing early biosimilar entrants partly offset by Evenity momentum"),
    ("Tezspire (severe asthma)",            3.2,  2.4,  4.8, "Best-in-class severe asthma biologic; rapid share gains, strong double-digit growth runway"),
    ("UPLIZNA/Tepezza/Horizon rare disease", 3.8,  3.0,  4.8, "UPLIZNA +188% YoY is the standout; Tepezza growth moderating post-launch surge"),
    ("Biosimilars portfolio",               4.3,  3.5,  5.3, "AMJEVITA/Wezlana/etc. — growing contributor as portfolio scales across multiple molecules"),
    ("Otezla/Enbrel (legacy, eroding)",     6.2,  4.3,  6.8, "Otezla generic erosion (LOE Feb 2028, early authorized generics already pressuring); Enbrel biosimilar-driven decline"),
    ("Oncology (BLINCYTO/LUMAKRAS/other)",  5.3,  4.6,  6.2, "BLINCYTO/Imdelltra/LUMAKRAS steady growth; KRAS franchise still scaling"),
    ("MariTide (obesity/GLP-1, Phase 3)",   0.0,  0.0,  2.5, "MARITIME-SWITCH study expanded with improved tolerability data — a genuine de-risking signal; still zero current revenue"),
]

# Net-margin-based bridge
NET_MARGIN_CURR = 0.3198   # FY2026E; reconciles to raised guidance midpoint
NET_MARGIN_BEAR = 0.2988   # BEAR: MariTide disappoints, erosion accelerates, debt drag persists
NET_MARGIN_BULL = 0.3323   # BULL: growth franchise mix shift + MariTide optionality expand margin

# ── MARITIDE / DEBT DELEVERAGING TRACKER (the Amgen-specific angle) ───────────
Q1_2026_EPS                 = 5.15   # $ non-GAAP EPS, Q1 2026 actual (beat consensus $4.77)
UPLIZNA_GROWTH_PCT          = 188    # % YoY growth, Q1 2026
FY2026_GUIDANCE_EPS_RANGE   = "21.70-23.10"  # $ non-GAAP, raised FY2026 guidance
NET_DEBT_TO_EBITDA          = "~3.1x"  # modest improvement from the post-Horizon-acquisition peak
Q2_EARNINGS_DATE            = "2026-08-04 (TONIGHT, after close)"
STOCK_MOVE_FROM_JUNE_LOW_PCT = round((CURRENT_PRICE - 312.00) / 312.00 * 100, 1)  # move since last refresh

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 22.40       # FY2026E non-GAAP EPS (raised guidance $21.70-23.10; midpoint)
PE_PESSIMISTIC = 13.0        # pessimistic P/E: below the current ~16.9× multiple; debt-discount floor
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (16.50, 13,  215, "MariTide Phase 3 disappoints despite the improved tolerability signal; Otezla/Enbrel erosion accelerates; debt load caps multiple; EPS $16.50 → 13× = $215"),
    "BASE":  (22.40, 16.92, 379, "Repatha/Tezspire/UPLIZNA growth roughly offsets Otezla/Enbrel erosion; MariTide Phase 3 continues de-risking but launch still years out; EPS $22.40 → 16.9× = $379"),
    "BULL":  (29.00, 19,  551, "MariTide Phase 3 confirms the improved tolerability profile with strong efficacy, de-risking a multi-billion dollar obesity franchise; Tezspire/UPLIZNA continue strong growth; EPS $29.00 → 19× = $551"),
    "XBULL": (34.00, 22,  748, "MariTide becomes a genuine top-tier obesity franchise with differentiated monthly dosing; full pipeline re-accelerates; balance sheet de-levered; EPS $34.00 → 22× = $748"),
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
        "name":       "Repatha/Tezspire/UPLIZNA growth franchise YoY",
        "weight":     0.25,
        "thresholds": ("<8%",  "≥15%", "≥22%", "≥30%"),
        "now":        "+22%",
        "score":      3,
        "comment":    "UPLIZNA +188% YoY is the standout; Repatha at a new run-rate, Tezspire scaling fast — the core organic growth engine offsetting legacy erosion",
    },
    {
        "name":       "MariTide Phase 3 (MARITIME) readout/de-risking",
        "weight":     0.25,
        "thresholds": ("fails/shelved", "delayed/mixed", "positive, on-track", "best-in-class data"),
        "now":        "positive, on-track",
        "score":      3,
        "comment":    "MARITIME-SWITCH study expanded with lower nausea/vomiting vs earlier data — genuine tolerability de-risking, though full Phase 3 readout is still pending",
    },
    {
        "name":       "Otezla/Enbrel legacy erosion vs new-product offset",
        "weight":     0.20,
        "thresholds": ("erosion>offset", "roughly even", "offset", "net legacy growth"),
        "now":        "roughly even",
        "score":      2,
        "comment":    "Enbrel biosimilar-driven decline and early Otezla generic erosion ahead of Feb 2028 LOE are being roughly offset by the growth franchise",
    },
    {
        "name":       "Biosimilars portfolio scaling",
        "weight":     0.10,
        "thresholds": ("<5%", "≥10%",  "≥18%", "≥25%"),
        "now":        "+15%",
        "score":      2,
        "comment":    "AMJEVITA, Wezlana and other biosimilars growing at a healthy double-digit clip",
    },
    {
        "name":       "Horizon debt deleveraging (net debt/EBITDA)",
        "weight":     0.10,
        "thresholds": (">3.5x", "~3.0-3.5x", "~2.5-3.0x", "<2.5x"),
        "now":        "~3.1x",
        "score":      2,
        "comment":    "Modest improvement from the post-Horizon-acquisition peak (~3.7x); still a meaningful multiple constraint",
    },
    {
        "name":       "Pipeline productivity beyond MariTide (oncology/inflammation)",
        "weight":     0.10,
        "thresholds": ("none",  "1 readout", "2-3 readouts", "4+ readouts"),
        "now":        "2-3, UPLIZNA proof point",
        "score":      3,
        "comment":    "UPLIZNA's outsized growth is real evidence of pipeline productivity beyond the headline MariTide story",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Diversified growth franchise — Repatha/Tezspire/UPLIZNA/biosimilars provide multiple offsets to legacy erosion", +0.5, 0.20),
    ("-", "Horizon debt overhang — still caps multiple expansion even as deleveraging progresses modestly",                -0.4, 0.20),
    ("+", "MariTide optionality — the tolerability improvement is a real, positive update to the >$100B obesity TAM option", +0.6, 0.20),
    ("-", "Otezla/Enbrel cliff — Enbrel biosimilar erosion is structural; Otezla LOE (Feb 2028) is a known, dated headwind", -0.4, 0.20),
    ("+", "Defensive cash flow + dividend — recently raised to $10.08/share, ~2.7% yield with a 14+ yr increase streak",     +0.3, 0.10),
    ("-", "MariTide binary risk — the full Phase 3 readout is still pending; a late disappointment remains possible",       -0.3, 0.10),
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
CONS_EPS_2YR  = 27.00   # FY2028E conservative: ~9.7% CAGR off FY2026E base
CONS_PE_2YR   = 15      # modest compression from ~16.9× given persistent debt-load and binary MariTide overhang
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Inflammation/Oncology / Rare Disease / Cardiometabolic / MariTide")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<38}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<38}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<38}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print(f"  Q1 2026 actual: non-GAAP EPS ${Q1_2026_EPS:.2f} (beat); UPLIZNA +{UPLIZNA_GROWTH_PCT}% YoY")
print(f"  ⚠ Q2 2026 earnings report {Q2_EARNINGS_DATE} — the next confirmation point for this model")
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
print(f"  ÷ {shares:.4f}B shares  =  ${curr_eps:.2f}/share  (guidance ${EPS_FY2026E:.2f} midpoint  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {NET_MARGIN_BULL*100:.2f}% net margin")
print(f"  ÷ {shares:.4f}B shares  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {NET_MARGIN_BEAR*100:.2f}% net margin (MariTide disappoints + erosion accelerates)")
print(f"  ÷ {shares:.4f}B shares  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# MARITIDE / DEBT TRACKER
print()
print(f"  MARITIDE / DEBT DELEVERAGING TRACKER  (the Amgen-specific angle):")
print(f"  Q1 2026 non-GAAP EPS:                        ${Q1_2026_EPS:.2f}  (beat consensus $4.77)")
print(f"  UPLIZNA growth:                                +{UPLIZNA_GROWTH_PCT}% YoY")
print(f"  FY2026 guidance:                                non-GAAP EPS ${FY2026_GUIDANCE_EPS_RANGE}")
print(f"  Net debt/EBITDA:                                {NET_DEBT_TO_EBITDA}")
print(f"  Stock move since last refresh (Jun 10):        +{STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}%")
print()
print(f"  ⚠ This model is built on Q1 2026 data and FY2026 guidance — Q2 2026 results report")
print(f"  {Q2_EARNINGS_DATE}. The MARITIME-SWITCH tolerability improvement is a genuine positive")
print(f"  update, but the full Phase 3 efficacy readout remains the key pending catalyst.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = 1.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at {NET_MARGIN_CURR*100:.1f}% margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*16.92:.2f}/share at 16.9× P/E")
print(f"  1pp net margin expansion (mix/scale):        +${curr_total*0.01/shares:.3f}/EPS  = +${curr_total*0.01/shares*16.92:.2f}/share at 16.9× P/E")
print(f"  Every 1 turn of P/E:                          ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Growth franchise / MariTide / legacy erosion / biosimilars / debt / pipeline)")
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
    ("Repatha/Tezspire/UPLIZNA growth",    "+22%",   "<8%",    "Competitive PCSK9/biologic entrants pressure pricing/share"),
    ("MariTide Phase 3 readout",           "positive, on-track","fails/shelved", "Efficacy data disappoints despite the tolerability improvement"),
    ("Otezla/Enbrel erosion vs offset",    "roughly even", "erosion>>offset", "Generic Otezla launches early/aggressively; Enbrel decline accelerates"),
    ("Biosimilars growth",                 "+15%",   "<5%",    "Pricing competition intensifies across the biosimilar portfolio"),
    ("Net debt/EBITDA",                    "~3.1x",  ">3.7x",  "Free cash flow diverted to MariTide Phase 3 spend instead of deleveraging"),
    ("Net margin",                         "32.0%",  "<28%",   "Mix shift toward lower-margin legacy/biosimilar revenue"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>16}  {bear_v:>9}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: MariTide's full Phase 3 (MARITIME) efficacy data disappoints despite the")
print(f"  encouraging tolerability signal, removing the primary re-rating catalyst, while Enbrel")
print(f"  biosimilar erosion accelerates and Otezla generic competition arrives ahead of the Feb")
print(f"  2028 LOE. EPS falls to ~$16.50 → 13× trough P/E (debt-discount floor) = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT permanent impairment — the growth franchise and dividend provide a floor.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E non-GAAP EPS estimate:  ${EPS_FY2026E:.2f}  (raised guidance midpoint)")
print(f"  Pessimistic P/E:                 {PE_PESSIMISTIC:.1f}×  (below the current ~16.9× multiple; debt-discount floor)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  AMGN trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS ${EPS_FY2026E:.2f} — a middling multiple for a diversified")
print(f"  large-cap biotech with a real, improving obesity option in MariTide. The Horizon debt load")
print(f"  and Otezla/Enbrel erosion remain known and largely priced in.")
print(f"  At 19× mid-cycle P/E (MariTide de-risks further): ${EPS_FY2026E:.2f} × 19 = ${EPS_FY2026E*19:.0f}  — {(EPS_FY2026E*19/CURRENT_PRICE-1)*100:+.0f}% vs current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest EPS growth as legacy erosion laps; P/E compresses modestly)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (~9.7% CAGR; Otezla/Enbrel erosion largely lapped)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (modest compression from ~{CURRENT_PRICE/EPS_FY2026E:.1f}× as debt overhang caps re-rating)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: AMGN's growth franchise (Repatha/Tezspire/UPLIZNA) and biosimilars are")
print(f"  visibly offsetting legacy erosion; MariTide is the free option, now with an improved")
print(f"  tolerability signal. If the full Phase 3 readout confirms, the stock can re-rate toward 19×+.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.22
beta        = 0.80
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock is up {STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}% since the last refresh (Jun 10) on Repatha/UPLIZNA strength + MariTide tolerability data")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  14+ yrs of dividend increases)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (moderate; large-cap biotech with binary MariTide catalyst risk)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (moderate; defensive cash flows offset by pipeline-event volatility)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (significant but plausible on MariTide-failure + erosion shock)")
print(f"  → Tonight's Q2 print, and the full MariTide Phase 3 readout, are THE KEY near-term catalysts.")
print(f"  → Repatha/Tezspire/UPLIZNA growth + debt paydown pace are the KEY ongoing drivers.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $330  |  Trim above $400")

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
print(f"  {valuation_label.lower()} by model standards. In plain terms: the growth franchise (Repatha/Tezspire/UPLIZNA)")
print(f"  is genuinely offsetting legacy erosion, and MariTide's tolerability update is real progress —")
print(f"  tonight's print and the full Phase 3 readout are the next confirmation points.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Q2 2026 earnings — {Q2_EARNINGS_DATE}")
print(f"  (2) MariTide Phase 3 (MARITIME) full efficacy readout — the primary re-rating catalyst")
print(f"  (3) Repatha/Tezspire/UPLIZNA growth trajectory — pace of offset vs Otezla/Enbrel erosion")
print(f"  (4) Otezla generic competition — timing/severity of erosion ahead of Feb 2028 LOE")
print(f"  (5) Net debt/EBITDA deleveraging — pace of Horizon-debt paydown and multiple impact")
print(f"  (6) Dividend sustainability — ${ANNUAL_DIV:.2f}/share payout; 14+ yr increase streak")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $330  |  Trim above $400")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.1f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}")
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
