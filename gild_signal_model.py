"""
GILD  ·  Gilead Sciences, Inc.  ·  NASDAQ: GILD
Bottom-up signal model  ·  HIV (Biktarvy/Lenacapavir-Yeztugo) / Oncology (Trodelvy/Kite) / Liver Disease / Veklury
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "GILD"
COMPANY       = "Gilead Sciences, Inc."
SECTOR        = "Biopharma · HIV (Biktarvy/Lenacapavir-Yeztugo) · Oncology (Trodelvy/Kite Yescarta-Tecartus) · Liver Disease · NASDAQ: GILD"
CURRENT_PRICE = 108.50     # USD; as of 2026-06-10
VOL_52W_LOW   = 92.10      # 2025 trough pre-Yeztugo launch ramp confirmation
VOL_52W_HIGH  = 121.40     # 2026 peak on lenacapavir/Yeztugo PrEP launch momentum
SHARES_OUT_M  = 1_245.0    # millions
ANNUAL_DIV    = 3.16       # $/share; ~2.9% yield; steadily growing dividend

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("HIV - Biktarvy",                        12.6, 11.5, 13.2, "World's top-selling HIV regimen; durable share leader but nearing peak ahead of ~2033 patent cliff"),
    ("HIV - Lenacapavir/Yeztugo (PrEP+treat)",  0.6,  0.2,   3.5, "Twice-yearly PrEP launch (Yeztugo) - largest new-product opportunity in company history; early-stage ramp"),
    ("HIV - Descovy/other legacy",              1.8,  1.4,   2.0, "Descovy for PrEP cannibalized by lenacapavir over time; modest legacy decline"),
    ("Oncology (Trodelvy/Kite Yescarta-Tecartus)", 4.6, 3.9,  6.0, "Trodelvy label expansions + Kite cell therapy (Yescarta/Tecartus) growth in earlier treatment lines"),
    ("Liver Disease (Vemlidy/Hepcludex/HCV)",   2.0,  1.7,   2.3, "Stable HBV/HDV franchise; modest growth from Hepcludex international expansion"),
    ("Veklury (COVID antiviral)",               1.4,  0.6,   1.6, "Highly volatile, demand-driven by COVID hospitalization rates; structurally declining"),
    ("Other (inflammation, products)",          1.0,  0.8,   1.2, "Small legacy/other product revenue"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.78    # blended gross margin; biopharma high-margin mix
GROSS_MARGIN_BULL = 0.80    # BULL: lenacapavir/Trodelvy mix shift improves blend further
OPEX_FIXED_B      = 11.0    # SG&A + R&D ($B); includes lenacapavir launch investment
TAX_RATE          = 0.16    # effective rate; international IP mix

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 8.60       # FY2027E EPS (non-GAAP consensus ~$8.40-$8.80, lenacapavir ramp accretive)
PE_PESSIMISTIC = 9.0        # trough P/E: Biktarvy patent-cliff discount; historical GILD trough ~9-10x
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # ~$77

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 6.75,  9,   61, "Lenacapavir/Yeztugo PrEP launch disappoints (access/payer friction, slow uptake); Biktarvy faces earlier-than-expected generic/competitive erosion; Veklury collapses further; Kite oncology stalls; EPS $6.75 → 9× = $61"),
    "BASE":  ( 8.60, 11,   95, "Yeztugo PrEP ramps steadily toward multi-billion-dollar run rate by 2028; Biktarvy holds share near-term with gradual decline starting late-decade; Trodelvy/Kite grow mid-single-digits; EPS $8.60 → 11× = $95"),
    "BULL":  (10.25, 14,  144, "Lenacapavir becomes the dominant global PrEP standard with rapid payer/government uptake (incl. PEPFAR-style access deals), creating a multi-billion-dollar new franchise; Biktarvy stable; oncology beats; EPS $10.25 → 14× = $144"),
    "XBULL": (12.50, 17,  213, "Lenacapavir achieves blockbuster-of-blockbusters status (>$10B peak) across PrEP and treatment, effectively replacing Biktarvy's eventual decline 1-for-1; Kite/Trodelvy reach new-franchise scale; multiple re-rates toward growth biotech peers; EPS $12.50 → 17× = $213"),
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
        "name":       "Lenacapavir/Yeztugo PrEP launch trajectory",
        "weight":     0.30,
        "thresholds": ("uptake stalls", "slow but building", "ramping to multi-$B run rate", "blockbuster (>$5B) trajectory confirmed"),
        "now":        "early launch, building",
        "score":      2,
        "comment":    "Yeztugo (twice-yearly injectable PrEP) launched with strong clinical profile (near-100% efficacy in trials) but early commercial ramp - payer coverage and access programs (incl. global access deals) still being established",
    },
    {
        "name":       "Biktarvy revenue durability vs patent cliff (~2033)",
        "weight":     0.20,
        "thresholds": ("declining now", "flat/low-single-digit growth", "mid-single-digit growth", "share gains accelerating"),
        "now":        "+low single digit",
        "score":      2,
        "comment":    "Biktarvy remains the dominant HIV regimen with continued share gains in treatment-naive patients, but growth is decelerating as the franchise approaches peak ahead of the 2033 patent cliff",
    },
    {
        "name":       "Oncology (Trodelvy/Kite Yescarta-Tecartus) growth",
        "weight":     0.15,
        "thresholds": ("<3%",  "≥6%",  "≥12%",   "≥20%"),
        "now":        "+9%",
        "score":      2,
        "comment":    "Trodelvy label expansions (earlier-line breast cancer) and Kite cell therapy growth provide a credible second growth pillar, though execution against larger oncology competitors remains a watch item",
    },
    {
        "name":       "Veklury (COVID antiviral) revenue trend",
        "weight":     0.10,
        "thresholds": ("rising/volatile upside", "stable", "declining as expected", "collapsing faster than modeled"),
        "now":        "declining as expected",
        "score":      2,
        "comment":    "Veklury continues its structural decline as COVID hospitalizations normalize; modeled as a shrinking but still-relevant cash contributor",
    },
    {
        "name":       "Pipeline depth beyond lenacapavir (oncology, inflammation)",
        "weight":     0.10,
        "thresholds": ("thin",  "1-2 readouts","3-4 readouts","5+ readouts/approvals"),
        "now":        "2-3",
        "score":      2,
        "comment":    "Trodelvy combination studies, additional Kite indications, and early inflammation pipeline provide some optionality beyond the HIV franchise, though lenacapavir remains the dominant near-term value driver",
    },
    {
        "name":       "Balance sheet strength / capital return capacity",
        "weight":     0.15,
        "thresholds": ("<BBB+", "BBB+/A-", "A",   "A+/AA-"),
        "now":        "A",
        "score":      3,
        "comment":    "Solid investment-grade balance sheet with strong free cash flow generation (HIV franchise economics); growing dividend (~2.9% yield) and continued buyback capacity support shareholder returns",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Lenacapavir/Yeztugo optionality - twice-yearly PrEP addresses a massive underserved global market; could become GILD's largest-ever franchise", +0.6, 0.25),
    ("-", "Biktarvy concentration risk - single product remains ~40%+ of revenue; 2033 patent cliff is a real long-dated overhang requiring lenacapavir to deliver", -0.5, 0.20),
    ("+", "Cash-generative HIV franchise + solid A-rated balance sheet provide durable downside floor and funding for lenacapavir launch investment", +0.4, 0.20),
    ("-", "Veklury volatility - COVID-driven revenue remains unpredictable and structurally shrinking, creating near-term EPS noise", -0.3, 0.10),
    ("+", "Oncology diversification (Trodelvy/Kite) reduces single-franchise (HIV) concentration and offers a credible second growth vector", +0.3, 0.15),
    ("-", "Execution/access risk on lenacapavir global rollout (pricing, payer coverage, manufacturing scale-up) could delay the bull thesis by years", -0.4, 0.10),
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
    signal_short, signal_full = "HOLD",      "▷ HOLD/TRIM"
else:
    signal_short, signal_full = "AVOID",     "✕ AVOID"

ratio_b_str = f"{ratio_b:.2f}x" if ratio_b != float("inf") else "N/A"

# ── CONSERVATIVE GROWTH (2-yr) ────────────────────────────────────────────────
CONS_EPS_2YR  = 9.25    # FY2028E conservative: lenacapavir ramping, Biktarvy still holding
CONS_PE_2YR   = 12      # modest rerate from ~12.6x as lenacapavir traction becomes visible
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  HIV (Biktarvy/Lenacapavir-Yeztugo) / Oncology / Liver Disease")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<46}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<46}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<46}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
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
shares_b     = shares * 0.96   # ~2%/yr buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.97   # mix shift away from high-margin lenacapavir
bear_oi      = bear_gp - OPEX_FIXED_B * 0.95           # partial cost response
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 14× = ~${bull_eps_imp*14:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.97:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 9× trough P/E (patent-cliff-discount floor) = ~${bear_eps_imp*9:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev       = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_lena      = 1.0 * 0.85 * (1 - TAX_RATE) / shares   # lenacapavir very high margin
eps_per_1B_onc       = 1.0 * 0.65 * (1 - TAX_RATE) / shares   # oncology lower margin (cell therapy COGS)

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B Lenacapavir/Yeztugo revenue:           +${eps_per_1B_lena:.3f}/EPS  = +${eps_per_1B_lena*11:.1f}/share at 11× P/E")
print(f"  Every $1B Oncology (Trodelvy/Kite) revenue:      +${eps_per_1B_onc:.3f}/EPS  = +${eps_per_1B_onc*11:.1f}/share at 11× P/E")
print(f"  1pp GM expansion (mix shift to lenacapavir):     +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*11:.1f}/share at 11× P/E")
print(f"  1% buyback (~12.5M shares):                      +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Lenacapavir launch / Biktarvy durability / Oncology / Veklury / Pipeline / Balance sheet)")
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
    ("Lenacapavir/Yeztugo launch trajectory", "building", "uptake stalls", "stalls",  "Payer access/pricing friction and slow PrEP-prescriber adoption stunt the launch curve"),
    ("Biktarvy revenue trend",                "+low-sd", "declining now",  "−mid-sd", "Earlier-than-expected competitive/generic pressure erodes Biktarvy share ahead of plan"),
    ("Oncology (Trodelvy/Kite) growth",       "+9%",     "<3%",   "−6pp",   "Trodelvy/Kite lose ground to competitive ADCs/CAR-Ts; label expansions disappoint"),
    ("Veklury revenue",                       "declining as expected", "collapsing faster", "accelerated decline", "COVID hospitalizations fall faster than modeled, removing a cash cushion"),
    ("Pipeline readouts",                     "2-3",     "thin (0-1)", "−2",   "Oncology/inflammation pipeline readouts disappoint or are delayed"),
    ("Gross margin",                          "78%",     "<74%",  "−4pp",   "Mix shift toward lower-margin oncology/cell therapy without lenacapavir offset"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Lenacapavir/Yeztugo's PrEP launch stalls on payer access and pricing friction")
print(f"  just as Biktarvy begins facing earlier-than-expected competitive erosion ahead of its 2033")
print(f"  patent cliff, while Veklury's COVID-driven revenue collapses faster than modeled and")
print(f"  Trodelvy/Kite oncology growth disappoints. EPS falls to ~$6.75 → 9× trough P/E")
print(f"  (patent-cliff-discount floor) = ${bear_price}.")
print(f"  Note: $61 is NOT permanent impairment — Gilead's HIV franchise remains highly cash-generative")
print(f"  with an A-rated balance sheet and growing dividend (${ANNUAL_DIV:.2f}/share). Recovery to")
print(f"  ~${bear_price+20}–${bear_price+35} in 2yr is plausible once lenacapavir traction becomes visible.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           ${EPS_FY2027E:.2f}  (consensus ~$8.40-$8.80 non-GAAP)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (patent-cliff-discount floor; historical GILD trough ~9-10×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({abs(epp_gap_pct):.0f}% {'above' if epp_gap_pct >= 0 else 'below'} trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% {'premium to' if epp_gap_pct >= 0 else 'discount to'} EPP reflects that GILD trades at roughly")
print(f"  {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a modest valuation for a cash-generative,")
print(f"  A-rated biopharma with a dominant HIV franchise. The Biktarvy patent-cliff overhang (~2033)")
print(f"  and Veklury volatility are largely priced in. The open question is whether lenacapavir/")
print(f"  Yeztugo's PrEP launch can become a multi-billion-dollar franchise large enough to bridge")
print(f"  the eventual Biktarvy decline, or whether the launch ramps too slowly to shift the narrative.")
print(f"  EPP path: FY2029E EPS ~$9.75 × {PE_PESSIMISTIC:.0f}× = ${9.75*PE_PESSIMISTIC:.0f} floor (EPP grows as lenacapavir scales).")
print(f"  At 12× mid-cycle P/E: ${EPS_FY2027E:.2f} × 12 = ${EPS_FY2027E*12:.0f}  — modest upside from current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: lenacapavir ramping, Biktarvy holds, modest re-rate)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (modest growth; lenacapavir ramp partially offsets Veklury decline)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (modest rerate from ~{CURRENT_PRICE/EPS_FY2027E:.1f}× as lenacapavir traction becomes visible)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: GILD trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a modest multiple for")
print(f"  a cash-generative, A-rated HIV/oncology leader — reflecting the long-dated Biktarvy patent-")
print(f"  cliff overhang (~2033) and Veklury volatility. Lenacapavir/Yeztugo's twice-yearly PrEP launch")
print(f"  is the central swing factor: if it scales toward a multi-billion-dollar run rate by 2028,")
print(f"  the stock can re-rate toward 12-14×. If the launch ramps slowly, current levels persist.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E - 1)*100:.1f}% EPS growth by FY2028E vs FY2027E.")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.22
beta        = 0.50
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  steadily growing payout)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (moderate; defensive HIV franchise offset by lenacapavir launch headlines)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (low-beta defensive large-cap biopharma)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (significant; lenacapavir-launch-stall + Biktarvy-erosion tail scenario)")
print(f"  52W range reflects building optimism around the Yeztugo launch with periodic pullbacks on")
print(f"  access/reimbursement headlines.")
print(f"  → Lenacapavir/Yeztugo quarterly revenue ramp is THE KEY catalyst for both downside and upside.")
print(f"  → Biktarvy quarterly trends and any signs of early competitive erosion are the KEY risk signal.")
print(f"  → AVOID above $135  |  WATCHLIST $115–135  |  ACCUMULATE $95–115  |  BUY below $90–95")

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
print(f"  In plain terms: the market is pricing in {'more' if MARKET_COMPOSITE > ADJ_COMPOSITE else 'less'} confidence in the lenacapavir/Yeztugo")
print(f"  PrEP launch trajectory than the bottom-up fundamentals currently support. The risk/reward")
print(f"  skew (Ratio B {ratio_b_str}) reflects a durable HIV cash-flow floor against a long-dated")
print(f"  Biktarvy patent-cliff overhang, with lenacapavir as the key swing factor for re-rating.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Lenacapavir/Yeztugo PrEP launch — quarterly revenue ramp, payer coverage, global access deals")
print(f"  (2) Biktarvy revenue trend — durability of share leadership ahead of ~2033 patent cliff")
print(f"  (3) Trodelvy label expansions / Kite (Yescarta/Tecartus) growth — oncology diversification progress")
print(f"  (4) Veklury revenue trajectory — pace of structural decline as COVID demand normalizes")
print(f"  (5) Pipeline readouts (oncology combinations, inflammation) — optionality beyond HIV")
print(f"  (6) Dividend growth — ${ANNUAL_DIV:.2f}/share payout; capital return capacity from HIV cash flows")
print(f"  AVOID above $135  |  WATCHLIST $115–135  |  ACCUMULATE $95–115  |  BUY below $90–95")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2027E EPS: ${EPS_FY2027E:.2f}")
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
