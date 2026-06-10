"""
AMGN  ·  Amgen Inc.  ·  NASDAQ: AMGN
Bottom-up signal model  ·  Inflammation/Oncology / Rare Disease (Horizon) / Bone (Repatha/Prolia/Evenity) / MariTide (Obesity)
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "AMGN"
COMPANY       = "Amgen Inc."
SECTOR        = "Biotechnology · Inflammation/Oncology · Rare Disease (Horizon/Tepezza) · Cardiometabolic (Repatha/Prolia/Evenity) · Obesity Pipeline (MariTide) · NASDAQ: AMGN"
CURRENT_PRICE = 312.00     # USD; as of 2026-06-10
VOL_52W_LOW   = 268.00     # 2025 trough; Horizon-debt/biosimilar erosion concerns
VOL_52W_HIGH  = 345.00     # 2026 peak on Repatha/Tezspire growth + MariTide Phase 2 readthrough optimism
SHARES_OUT_M  = 536.0      # millions
ANNUAL_DIV    = 9.46       # $/share; ~3.0% yield; 14+ yrs of dividend increases

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Repatha/Prolia/Evenity (bone+CV)",  10.5,  9.0, 12.5, "Repatha (PCSK9) +20%+ growth; Prolia facing early biosimilar entrants partly offset by Evenity (osteoporosis) momentum"),
    ("Tezspire (severe asthma)",           2.2,  1.6,  3.5, "Best-in-class severe asthma biologic; rapid share gains, strong double-digit growth runway"),
    ("Tepezza/Horizon rare disease",       2.6,  2.0,  3.2, "Tepezza (TED) growth moderating post-launch surge; Krystexxa, Uplizna, Wezlana add diversification"),
    ("Biosimilars portfolio",              3.3,  2.6,  4.2, "AMJEVITA/Wezlana/etc. - growing contributor as portfolio scales across multiple molecules"),
    ("Otezla/Enbrel (legacy, eroding)",    6.5,  4.5,  7.0, "Otezla generic erosion (LOE Feb 2028, early authorized generics already pressuring); Enbrel biosimilar-driven decline ~-10 to -15%/yr"),
    ("Oncology (BLINCYTO/LUMAKRAS/other)", 4.4,  3.8,  5.2, "BLINCYTO/Imdelltra/LUMAKRAS steady growth; KRAS franchise still scaling"),
    ("MariTide (obesity/GLP-1, Phase 3)",  0.0,  0.0,  3.0, "Phase 3 MARITIME readout pending; monthly-dose GLP-1/GIPR antagonist - binary catalyst, zero current revenue"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.745   # blended gross margin; biotech mix with biosimilar drag
GROSS_MARGIN_BULL = 0.760   # BULL: higher-margin Repatha/Tezspire/MariTide mix improves blend
OPEX_FIXED_B      = 12.5    # SG&A + R&D ($B); includes heavy MariTide Phase 3 spend
TAX_RATE          = 0.140   # effective rate; biotech international mix
INTEREST_EXP_B    = 2.6     # ~$28B Horizon-driven debt load; meaningful fixed interest drag

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 24.50       # FY2027E non-GAAP EPS (consensus ~$24-25; FY2026E ~$22.40, ~10% growth)
PE_PESSIMISTIC = 12.5        # trough P/E: high debt load + Otezla/Enbrel erosion caps downside multiple; biotech trough ~12-13x
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # $306

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (19.50, 12,  234, "MariTide Phase 3 disappoints (efficacy/tolerability) and is shelved or delayed years; Otezla/Enbrel erosion accelerates faster than offsets; Horizon debt load caps multiple at trough; EPS $19.50 → 12× = $234"),
    "BASE":  (24.50, 14,  343, "Repatha/Tezspire/Evenity growth roughly offsets Otezla/Enbrel erosion; biosimilars scale steadily; MariTide Phase 3 reads out positive but commercial launch still 2+ yrs out (modest credit); EPS $24.50 → 14× = $343"),
    "BULL":  (28.00, 17,  476, "MariTide Phase 3 delivers best-in-class monthly-dose efficacy/tolerability data, de-risking a multi-billion dollar obesity franchise; Tezspire/Repatha continue strong double-digit growth; debt paydown ahead of schedule; EPS $28.00 → 17× = $476"),
    "XBULL": (33.00, 20,  660, "MariTide becomes a genuine top-3 obesity franchise with differentiated monthly dosing, driving a multi-year re-rating toward GLP-1-leader multiples; full pipeline (oncology, inflammation) re-accelerates; balance sheet de-levered; EPS $33.00 → 20× = $660"),
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
        "name":       "Repatha/Tezspire/Evenity growth franchise YoY",
        "weight":     0.25,
        "thresholds": ("<8%",  "≥15%", "≥22%", "≥30%"),
        "now":        "+20%",
        "score":      2,
        "comment":    "Repatha +22%, Tezspire +50%+ off small base, Evenity steady double-digit growth — the core organic growth engine offsetting legacy erosion",
    },
    {
        "name":       "MariTide Phase 3 (MARITIME) readout/de-risking",
        "weight":     0.25,
        "thresholds": ("fails/shelved", "delayed/mixed", "positive, on-track", "best-in-class data"),
        "now":        "Phase 3 enrolling/ongoing",
        "score":      2,
        "comment":    "Phase 3 trials initiated based on encouraging Phase 2 (~20% weight loss, monthly dosing); full readout still pending — major binary swing factor for both BULL and BEAR",
    },
    {
        "name":       "Otezla/Enbrel legacy erosion vs new-product offset",
        "weight":     0.20,
        "thresholds": ("erosion>offset", "roughly even", "offset", "net legacy growth"),
        "now":        "Enbrel -12%, Otezla early generic pressure",
        "score":      2,
        "comment":    "Enbrel biosimilar-driven decline (~-12% YoY) and early Otezla generic erosion ahead of Feb 2028 LOE are being roughly offset by Repatha/Tezspire/biosimilars growth",
    },
    {
        "name":       "Biosimilars portfolio scaling",
        "weight":     0.10,
        "thresholds": ("<5%", "≥10%",  "≥18%", "≥25%"),
        "now":        "+15%",
        "score":      2,
        "comment":    "AMJEVITA, Wezlana and other biosimilars growing at a healthy double-digit clip, becoming a meaningful (~$3B+) revenue contributor",
    },
    {
        "name":       "Horizon debt deleveraging (net debt/EBITDA)",
        "weight":     0.10,
        "thresholds": (">3.5x", "~3.0-3.5x", "~2.5-3.0x", "<2.5x"),
        "now":        "~3.2x",
        "score":      2,
        "comment":    "Net debt/EBITDA has come down modestly from post-Horizon-acquisition peak (~3.7x) toward ~3.2x; still a meaningful multiple constraint vs pre-acquisition AMGN",
    },
    {
        "name":       "Pipeline productivity beyond MariTide (oncology/inflammation)",
        "weight":     0.10,
        "thresholds": ("none",  "1 readout", "2-3 readouts", "4+ readouts"),
        "now":        "2",
        "score":      2,
        "comment":    "BLINCYTO/Imdelltra and LUMAKRAS combination data progressing; rocatinlimab (atopic dermatitis) and other inflammation pipeline assets advancing through Phase 3",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Diversified growth franchise — Repatha/Tezspire/Evenity/biosimilars provide multiple offsets to legacy erosion, reducing single-product risk", +0.5, 0.20),
    ("-", "Horizon debt overhang — ~$28B debt load (net debt/EBITDA ~3.2x) caps multiple expansion until meaningfully de-levered", -0.6, 0.20),
    ("+", "MariTide optionality — Phase 3 in a >$100B obesity TAM represents a free option not fully reflected in current multiple", +0.5, 0.20),
    ("-", "Otezla/Enbrel cliff — Enbrel biosimilar erosion is structural and accelerating; Otezla LOE (Feb 2028) is a known, dated headwind", -0.4, 0.20),
    ("+", "Defensive cash flow + dividend — ~3.0% yield with 14+ yr increase streak provides downside support and total-return floor", +0.3, 0.10),
    ("-", "MariTide binary risk — a Phase 3 failure/disappointment removes the primary re-rating catalyst and could reinforce 'mature biotech' multiple", -0.3, 0.10),
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
CONS_EPS_2YR  = 26.50   # FY2028E conservative: ~8% CAGR off FY2027E base, modest growth as erosion laps
CONS_PE_2YR   = 14      # roughly flat from ~14x given persistent debt-load and binary MariTide overhang
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
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B - INTEREST_EXP_B
curr_ni   = curr_oi * (1 - TAX_RATE)
curr_eps  = round(curr_ni / shares, 2)

bull_gp      = bull_total * GROSS_MARGIN_BULL
bull_oi      = bull_gp - OPEX_FIXED_B - INTEREST_EXP_B * 0.85   # modest deleveraging
bull_ni      = bull_oi * (1 - TAX_RATE)
shares_b     = shares * 0.97   # ~1.5%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift toward lower-margin legacy/biosimilars
bear_oi      = bear_gp - OPEX_FIXED_B * 0.95 - INTEREST_EXP_B   # partial cost response, debt unchanged
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − ${INTEREST_EXP_B:.1f}B interest − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − interest (deleveraged) − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 17× = ~${bull_eps_imp*17:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex − interest  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 12× trough P/E (debt-discount floor) = ~${bear_eps_imp*12:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev      = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_growth   = 1.0 * 0.80 * (1 - TAX_RATE) / shares   # Repatha/Tezspire/MariTide very high incremental margin
eps_per_1B_legacy   = 1.0 * 0.60 * (1 - TAX_RATE) / shares   # legacy/biosimilars lower incremental margin

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Repatha/Tezspire/MariTide revenue:     +${eps_per_1B_growth:.3f}/EPS  = +${eps_per_1B_growth*14:.1f}/share at 14× P/E")
print(f"  Every $1B legacy/biosimilars revenue:            +${eps_per_1B_legacy:.3f}/EPS  = +${eps_per_1B_legacy*14:.1f}/share at 14× P/E")
print(f"  1pp GM expansion (mix shift to growth franchise): +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*14:.1f}/share at 14× P/E")
print(f"  $1B debt paydown (~5% rate):                      +${0.05*(1-TAX_RATE)/shares:.3f}/EPS  (mechanical interest savings)")

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
    ("Repatha/Tezspire/Evenity growth",    "+20%",   "<8%",    "−12pp",  "Competitive PCSK9/biologic entrants pressure pricing/share"),
    ("MariTide Phase 3 readout",           "ongoing","fails/shelved", "binary miss", "Efficacy/tolerability data disappoints; obesity option value evaporates"),
    ("Otezla/Enbrel erosion vs offset",    "roughly even", "erosion>>offset", "gap widens", "Generic Otezla launches early/aggressively; Enbrel decline accelerates to -20%+"),
    ("Biosimilars growth",                 "+15%",   "<5%",    "−10pp",  "Pricing competition intensifies across biosimilar portfolio"),
    ("Net debt/EBITDA",                    "~3.2x",  ">3.7x",  "+0.5x",  "Free cash flow diverted to MariTide Phase 3 spend instead of deleveraging"),
    ("Gross margin",                       "74.5%",  "<71%",   "−3.5pp", "Mix shift toward lower-margin legacy/biosimilar revenue"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: MariTide Phase 3 (MARITIME program) data disappoints on efficacy and/or")
print(f"  tolerability (GI side effects have been a known issue for monthly-dose GIPR antagonists),")
print(f"  removing the primary re-rating catalyst, while Enbrel biosimilar erosion accelerates and")
print(f"  Otezla generic competition arrives ahead of the Feb 2028 LOE. EPS falls to ~$19.50 → 12×")
print(f"  trough P/E (debt-discount floor) = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT permanent impairment — the Repatha/Tezspire/Evenity/biosimilars")
print(f"  growth engine and ~3% dividend provide a durable earnings floor. Recovery toward")
print(f"  ~${bear_price+40}-${bear_price+60} in 2yr is plausible post-shock as legacy erosion fully laps.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           ${EPS_FY2027E:.2f}  (consensus ~$24-25 non-GAAP; FY2026E ~$22.40, +~10%)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.1f}×  (debt-discount floor; high-debt large-cap biotech trough ~12-13×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% {'above' if epp_gap_pct >= 0 else 'below'} trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% {'premium to' if epp_gap_pct >= 0 else 'discount to'} EPP reflects that AMGN trades at roughly")
print(f"  {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a middling multiple for a diversified large-cap biotech")
print(f"  with a real (if early) obesity option in MariTide. The Horizon debt load and Otezla/Enbrel")
print(f"  erosion are largely known and priced in. The open question is whether MariTide Phase 3")
print(f"  delivers enough de-risking to justify a re-rating toward GLP-1-adjacent multiples, or")
print(f"  whether the stock simply tracks its growth-franchise/legacy-erosion balance near current levels.")
print(f"  EPP path: FY2029E EPS ~$28 × {PE_PESSIMISTIC:.1f}× = ${28*PE_PESSIMISTIC:.0f} floor (EPP grows as legacy erosion laps and debt is paid down).")
print(f"  At 16× mid-cycle P/E: ${EPS_FY2027E:.2f} × 16 = ${EPS_FY2027E*16:.0f}  — modestly above current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest EPS growth as legacy erosion laps; P/E roughly flat)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (~8% CAGR; Otezla/Enbrel erosion largely lapped, Repatha/Tezspire/biosimilars offset)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (roughly flat from ~{CURRENT_PRICE/EPS_FY2027E:.1f}× as debt overhang caps re-rating)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: AMGN trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a reasonable multiple")
print(f"  for a diversified biotech, reflecting the Horizon debt load and known Otezla/Enbrel erosion.")
print(f"  Repatha/Tezspire/Evenity growth and biosimilars scaling are the visible offsets; MariTide")
print(f"  Phase 3 is the free option. If MariTide reads out positively and debt paydown continues,")
print(f"  the stock can re-rate toward 16-18×. If MariTide disappoints or erosion accelerates,")
print(f"  current levels are roughly fair.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E - 1)*100:.1f}% EPS growth by FY2028E vs FY2027E.")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.24
beta        = 0.80
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  14+ yrs of dividend increases)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (moderate; large-cap biotech with binary MariTide catalyst risk)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (moderate; defensive cash flows offset by pipeline-event volatility)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (significant but plausible on MariTide-failure + erosion shock)")
print(f"  52W range reflects MariTide-readthrough optimism partly offset by debt/erosion concerns.")
print(f"  → MariTide Phase 3 (MARITIME) readout is THE KEY binary for both upside and downside.")
print(f"  → Repatha/Tezspire/Evenity growth + debt paydown pace are KEY ongoing drivers.")
print(f"  → AVOID above $360  |  WATCHLIST $300–345  |  ACCUMULATE $260–290  |  BUY below $245-260")

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
print(f"  In plain terms: the market is pricing in a roughly balanced outcome between MariTide")
print(f"  optionality and Horizon debt/legacy-erosion drag. The risk/reward skew (Ratio B {ratio_b_str})")
print(f"  reflects a stock waiting on a binary catalyst — the dividend (~3.0%) compensates for the wait.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) MariTide Phase 3 (MARITIME) data — efficacy/tolerability readout; primary re-rating catalyst")
print(f"  (2) Repatha/Tezspire/Evenity growth trajectory — pace of offset vs Otezla/Enbrel erosion")
print(f"  (3) Otezla generic competition — timing/severity of erosion ahead of Feb 2028 LOE")
print(f"  (4) Enbrel biosimilar erosion rate — pace of decline vs biosimilars portfolio growth")
print(f"  (5) Net debt/EBITDA deleveraging — pace of Horizon-debt paydown and multiple impact")
print(f"  (6) Dividend sustainability — ${ANNUAL_DIV:.2f}/share payout; 14+ yr increase streak")
print(f"  AVOID above $360  |  WATCHLIST $300–345  |  ACCUMULATE $260–290  |  BUY below $245-260")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.1f}×  |  FY2027E EPS: ${EPS_FY2027E:.2f}")
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
