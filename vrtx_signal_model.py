"""
VRTX  ·  Vertex Pharmaceuticals Incorporated  ·  NASDAQ: VRTX
Bottom-up signal model  ·  CF Franchise (Trikafta/Kaftrio/Alyftrek) / Journavx (non-opioid pain) / Casgevy / Crinetics M&A / Pipeline
Date: 2026-08-04
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "VRTX"
COMPANY       = "Vertex Pharmaceuticals Incorporated"
SECTOR        = "Biotech · Cystic Fibrosis (Trikafta/Alyftrek) · Non-opioid Pain (Journavx) · Gene Therapy (Casgevy) · NASDAQ: VRTX"
CURRENT_PRICE = 470.72      # USD; close 2026-08-03
VOL_52W_LOW   = 362.50      # USD
VOL_52W_HIGH  = 533.67      # USD
SHARES_OUT_M  = 253.8       # millions
ANNUAL_DIV    = 0.0         # VRTX pays no dividend; reinvests in pipeline/M&A

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# Q2 2026 actual (reported ~Aug 3): revenue $3.33B (+12.4% YoY, beat); adj EPS $4.73
# (narrowly missed $4.75 consensus). Casgevy revenue $76M (+150% YoY, +75% sequential —
# genuine acceleration). Journavx $50M (up from $12M YoY, 45% Rx growth, 260M covered
# lives — real payer-access traction). FY2026 revenue guidance raised to $13.1-13.2B.
# THE HEADLINE EVENT: VRTX signed a definitive agreement to acquire Crinetics
# Pharmaceuticals for $10B (rare endocrine diseases), expected to close Q3 2026 — this will
# consume most of VRTX's ~$11B net cash pile. Also: FDA accepted the BLA for povetacicept
# (IgA nephropathy, PDUFA Nov 30, 2026); VX-407 (ADPKD) Phase 2 enrollment complete.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("CF franchise (Trikafta/Kaftrio/Alyftrek)", 11.5, 10.7, 12.4, "Near-total eligible-patient penetration; Alyftrek switch drives modest pricing/duration upside but limited volume runway"),
    ("Journavx (suzetrigine, non-opioid pain)",   0.5, 0.25,  2.5, "Q2 revenue $50M/qtr, up from $12M YoY; 45% Rx growth, 260M covered lives — real payer-access traction"),
    ("Casgevy (exa-cel, gene therapy SCD/TDT)",    0.3, 0.15,  1.0, "Q2 revenue $76M/qtr, +150% YoY, +75% sequential — genuine acceleration, no longer just a slow ramp"),
    ("Pipeline/royalties (povetacicept, VX-407, Crinetics)", 0.85, 0.5, 1.5, "Povetacicept BLA accepted (PDUFA Nov 2026); VX-407 Phase 2 enrollment complete; Crinetics deal adds rare endocrine pipeline"),
]

# Net-margin-based bridge
NET_MARGIN_CURR = 0.3571   # FY2026E normalized (ex-Crinetics one-time acquisition charges)
NET_MARGIN_BEAR = 0.3282   # BEAR: CF plateau + Journavx/Casgevy underwhelm compress margin
NET_MARGIN_BULL = 0.3647   # BULL: Journavx/Casgevy scale + Crinetics integration proves accretive

# ── JOURNAVX/CASGEVY RAMP / CRINETICS M&A TRACKER (the Vertex-specific angle) ─
Q2_2026_REVENUE_B          = 3.33    # $B, Q2 2026 actual reported revenue
Q2_2026_ADJ_EPS            = 4.73    # $ adjusted EPS, Q2 2026 (narrowly missed $4.75 consensus)
CASGEVY_QOQ_GROWTH_PCT     = 75      # % sequential growth, Q2 2026
JOURNAVX_COVERED_LIVES_M   = 260     # million covered lives, Journavx payer access
CRINETICS_DEAL_VALUE_B     = 10.0    # $B, definitive agreement to acquire Crinetics Pharmaceuticals
CRINETICS_CLOSE_TARGET     = "Q3 2026"
POVETACICEPT_PDUFA         = "2026-11-30"  # IgA nephropathy BLA PDUFA date
STOCK_MOVE_FROM_JUNE_LOW_PCT = round((CURRENT_PRICE - 445.00) / 445.00 * 100, 1)  # move since last refresh

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 18.50       # FY2026E normalized EPS (ex-Crinetics acquisition charges; consensus range is wide due to deal noise)
PE_PESSIMISTIC = 17.0        # pessimistic P/E: below the current ~25.4× multiple; cash-rich profitable biotech floor
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (15.00, 17,  255, "CF franchise growth stalls; Journavx/Casgevy momentum fades; Crinetics integration proves dilutive/costly; EPS $15.00 → 17× = $255"),
    "BASE":  (18.50, 25.44, 471, "CF franchise grows low-single-digits; Journavx and Casgevy continue their current ramp pace; Crinetics closes on schedule; EPS $18.50 → 25.4× = $471"),
    "BULL":  (25.00, 26,  650, "Journavx and Casgevy both sustain their Q2 acceleration into multi-billion-dollar franchises; Crinetics integration proves accretive; pipeline (povetacicept, VX-407) delivers; EPS $25.00 → 26× = $650"),
    "XBULL": (31.00, 29,  899, "Journavx achieves blockbuster status displacing opioids at scale; Casgevy becomes standard-of-care; Crinetics fully integrated as a second growth platform; EPS $31.00 → 29× = $899"),
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
        "name":       "CF franchise revenue YoY growth (Trikafta/Alyftrek)",
        "weight":     0.25,
        "thresholds": ("<2%",   "≥4%",   "≥7%",    "≥10%"),
        "now":        "+4%",
        "score":      2,
        "comment":    "CF franchise approaching saturation; Alyftrek switch provides modest pricing/duration tailwind but volume growth is largely exhausted",
    },
    {
        "name":       "Journavx (suzetrigine) launch trajectory",
        "weight":     0.25,
        "thresholds": ("delayed/weak", "on-track modest", "strong uptake", "category-expanding blockbuster"),
        "now":        "strong uptake",
        "score":      3,
        "comment":    "$50M/qtr, up from $12M YoY; 45% Rx growth and 260M covered lives is real, quantified payer-access traction",
    },
    {
        "name":       "Casgevy (gene therapy) commercial rollout pace",
        "weight":     0.15,
        "thresholds": ("stalled", "slow ramp", "accelerating", "rapid center expansion"),
        "now":        "accelerating",
        "score":      3,
        "comment":    "$76M/qtr, +150% YoY and +75% sequential — genuine acceleration, no longer just a slow center-by-center ramp",
    },
    {
        "name":       "Pipeline readouts + Crinetics M&A",
        "weight":     0.15,
        "thresholds": ("none/negative", "1 mixed readout", "1-2 positive readouts", "multiple positive + filing"),
        "now":        "multiple positive + filing",
        "score":      4,
        "comment":    "Povetacicept BLA accepted (PDUFA Nov 2026), VX-407 Phase 2 enrollment complete, plus the $10B Crinetics acquisition adds a whole new rare-endocrine pipeline",
    },
    {
        "name":       "Operating margin / R&D efficiency",
        "weight":     0.10,
        "thresholds": ("<55%",  "≥58%",  "≥62%",   "≥66%"),
        "now":        "~58%",
        "score":      2,
        "comment":    "High-80s gross margin offset by substantial R&D/launch investment; Crinetics integration will add near-term cost pressure",
    },
    {
        "name":       "Balance sheet / capital allocation flexibility",
        "weight":     0.10,
        "thresholds": ("net debt", "net cash <$5B", "net cash $5-10B", "net cash >$10B"),
        "now":        "~$11B pre-Crinetics, shrinking post-close",
        "score":      3,
        "comment":    "Still debt-free today, but the $10B Crinetics acquisition (closing Q3 2026) will consume most of the cash cushion",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("-", "CF franchise maturation — near-total eligible-patient penetration leaves limited organic volume growth runway", -0.6, 0.25),
    ("+", "Journavx optionality — Q2's real payer-access traction (260M covered lives, 45% Rx growth) is the single biggest re-rating catalyst beyond CF", +0.7, 0.20),
    ("+", "Cash position — still debt-free today, though the Crinetics deal will consume most of the ~$11B cushion post-close", +0.3, 0.15),
    ("+", "Casgevy acceleration — +150% YoY and +75% sequential is genuine evidence the rollout bottleneck is easing", +0.6, 0.15),
    ("-", "Pipeline binary risk — Crinetics integration, povetacicept's PDUFA decision, and VX-407 data are all still pending", -0.4, 0.15),
    ("-", "Premium valuation + a $10B acquisition adds integration risk on top of already-full pipeline optionality pricing", -0.4, 0.10),
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
CONS_EPS_2YR  = 22.00   # FY2028E conservative: ~9%/yr off FY2026E, below the bull case, reflecting Crinetics integration costs
CONS_PE_2YR   = 22      # a modest compression from the current ~25.4×
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  CF Franchise / Journavx / Casgevy / Crinetics M&A / Pipeline")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<48}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<48}  ${curr:>11.2f}  ${bear:>8.2f}  ${bull:>8.2f}  {bear-curr:>+7.2f}  {bull-curr:>+7.2f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<48}  ${curr_total:>11.2f}  ${bear_total:>8.2f}  ${bull_total:>8.2f}  {bear_total-curr_total:>+7.2f}  {bull_total-curr_total:>+7.2f}")
print(f"  Q2 2026 actual: revenue ${Q2_2026_REVENUE_B:.2f}B (+12.4% YoY, beat), adj EPS ${Q2_2026_ADJ_EPS:.2f} (narrow miss)")
print()

# EPS bridge (net-margin based)
shares    = SHARES_OUT_M / 1000
curr_net  = curr_total * NET_MARGIN_CURR
curr_eps  = round(curr_net / shares, 2)

bull_net     = bull_total * NET_MARGIN_BULL
bull_eps_imp = round(bull_net / shares, 2)

bear_net     = bear_total * NET_MARGIN_BEAR
bear_eps_imp = round(bear_net / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.2f}B rev × {NET_MARGIN_CURR*100:.2f}% net margin")
print(f"  ÷ {shares:.4f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B rev × {NET_MARGIN_BULL*100:.2f}% net margin")
print(f"  ÷ {shares:.4f}B shares  =  ~${bull_eps_imp:.2f}/share  →  × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B rev × {NET_MARGIN_BEAR*100:.2f}% net margin (CF plateau + launches underwhelm)")
print(f"  ÷ {shares:.4f}B shares  =  ~${bear_eps_imp:.2f}/share  →  × {SCENARIOS['BEAR'][1]}× trough = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# JOURNAVX/CASGEVY/CRINETICS TRACKER
print()
print(f"  JOURNAVX/CASGEVY RAMP / CRINETICS M&A TRACKER  (the Vertex-specific angle):")
print(f"  Q2 2026 revenue / adj EPS:                   ${Q2_2026_REVENUE_B:.2f}B / ${Q2_2026_ADJ_EPS:.2f}")
print(f"  Casgevy sequential growth:                     +{CASGEVY_QOQ_GROWTH_PCT}% QoQ")
print(f"  Journavx covered lives:                         {JOURNAVX_COVERED_LIVES_M}M")
print(f"  Crinetics acquisition:                          ${CRINETICS_DEAL_VALUE_B:.0f}B, closing {CRINETICS_CLOSE_TARGET}")
print(f"  Povetacicept PDUFA date:                        {POVETACICEPT_PDUFA}")
print(f"  Stock move since last refresh (Jun 10):        +{STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}%")
print()
print(f"  Both post-CF growth pillars showed real acceleration this quarter — Casgevy's +75% sequential")
print(f"  jump and Journavx's 260M covered lives are genuine, quantified evidence the launches are")
print(f"  working, not just early promise. The $10B Crinetics acquisition adds a new growth platform")
print(f"  but will consume most of VRTX's cash cushion and adds real integration risk on top of an")
print(f"  already-full valuation.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev = 1.0 * NET_MARGIN_CURR / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at {NET_MARGIN_CURR*100:.1f}% margin):  +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*25.44:.2f}/share at 25.4× P/E")
print(f"  1pp net margin expansion (mix/scale):        +${curr_total*0.01/shares:.3f}/EPS  = +${curr_total*0.01/shares*25.44:.2f}/share at 25.4× P/E")
print(f"  Every 1 turn of P/E:                          ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (CF maturation / Journavx launch / Casgevy rollout / pipeline+M&A / margins / balance sheet)")
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
    ("CF franchise revenue growth",        "+4%",    "<2%",    "Penetration plateau confirmed; Alyftrek switch yields no net pricing uplift"),
    ("Journavx launch trajectory",         "strong uptake", "delayed/weak", "Payer formulary restrictions tighten despite the current 260M covered-lives access"),
    ("Casgevy rollout pace",               "accelerating", "stalled", "Treatment center activation and manufacturing logistics bottleneck resurfaces"),
    ("Crinetics integration",              "pending close", "dilutive/costly", "Deal closes but integration costs run over budget or synergies disappoint"),
    ("Operating margin",                   "~58%",   "<55%",   "Heavy launch/R&D + Crinetics integration spend pressures margins"),
    ("Net margin",                         "35.7%",  "<30%",   "Mix shift toward lower-margin Casgevy/cell-therapy manufacturing plus deal costs"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>16}  {bear_v:>9}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: CF franchise growth flatlines as eligible-patient penetration plateaus, while")
print(f"  Journavx and Casgevy's current acceleration proves temporary rather than durable, and the")
print(f"  Crinetics integration turns out to be dilutive or costly. EPS falls to ~$15.00 → 17× trough P/E.")
print(f"  Note: ${bear_price} is NOT permanent impairment — VRTX's durable CF cash flows provide a floor.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E normalized EPS estimate: ${EPS_FY2026E:.2f}  (ex-Crinetics acquisition charges)")
print(f"  Pessimistic P/E:                  {PE_PESSIMISTIC:.0f}×  (below the current ~25.4× multiple; cash-rich, debt-free profitable biotech floor)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  VRTX trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E normalized EPS ${EPS_FY2026E:.2f} — a premium multiple for a CF")
print(f"  franchise approaching saturation, justified by real Q2 traction in Journavx and Casgevy plus")
print(f"  the new Crinetics pipeline. Headline consensus EPS is unusually wide (~$15.37-19.16) because")
print(f"  the Crinetics deal will introduce one-time acquisition-charge noise, similar to what GILD is")
print(f"  seeing from its own 2026 M&A spend.")
print(f"  At 26× mid-cycle P/E: ${EPS_FY2026E:.2f} × 26 = ${EPS_FY2026E*26:.0f}  — {(EPS_FY2026E*26/CURRENT_PRICE-1)*100:+.0f}% vs current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest EPS growth, Crinetics integration costs weigh)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (~9%/yr off FY2026E, below the bull case)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (a modest compression from the current ~25.4×)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (no dividend; VRTX reinvests in pipeline/M&A)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: the conservative case is muted, not because Journavx/Casgevy aren't real —")
print(f"  their Q2 data is genuinely encouraging — but because the stock already prices meaningful")
print(f"  optionality, and the Crinetics deal adds integration risk on top of that before it's proven out.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.26
beta        = 0.65
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Note: stock is up {STOCK_MOVE_FROM_JUNE_LOW_PCT:.1f}% since the last refresh (Jun 10) on Journavx/Casgevy momentum")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (no dividend; cash reinvested into pipeline R&D and M&A)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; binary pipeline catalysts and launch-data-driven swings)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (moderate; large-cap biotech with diversified franchise vs single-asset peers)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (plausible on CF-plateau + Crinetics-integration-shock scenario)")
print(f"  → Crinetics deal close (Q3 2026) and integration signals are THE KEY near-term catalyst.")
print(f"  → Journavx/Casgevy ramp durability and povetacicept's Nov 2026 PDUFA are the KEY ongoing drivers.")
print(f"  → {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $410  |  Trim above $520")

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
print(f"  {valuation_label.lower()} by model standards. In plain terms: Journavx and Casgevy both showed real")
print(f"  acceleration in Q2, but the Crinetics acquisition introduces fresh integration risk right as")
print(f"  the market was starting to reward the post-CF growth story.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Crinetics acquisition close ({CRINETICS_CLOSE_TARGET}) and early integration signals")
print(f"  (2) Journavx — payer access expansion beyond 260M covered lives, label expansion into chronic pain")
print(f"  (3) Casgevy — confirming the +75% sequential acceleration continues, not a one-quarter blip")
print(f"  (4) Povetacicept — IgA nephropathy PDUFA decision ({POVETACICEPT_PDUFA})")
print(f"  (5) VX-407 (ADPKD) — Phase 2 data following enrollment completion")
print(f"  (6) CF franchise — Alyftrek switch dynamics, international reimbursement, penetration ceiling")
print(f"  {signal_short} at ${CURRENT_PRICE:.2f}  |  Add below $410  |  Trim above $520")
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
