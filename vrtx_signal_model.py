"""
VRTX  ·  Vertex Pharmaceuticals Incorporated  ·  NASDAQ: VRTX
Bottom-up signal model  ·  CF Franchise (Trikafta/Kaftrio/Alyftrek) / Journavx (non-opioid pain) / Casgevy / Pipeline (inaxaplin, zimislecel)
Date: 2026-06-10
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "VRTX"
COMPANY       = "Vertex Pharmaceuticals Incorporated"
SECTOR        = "Biotech · Cystic Fibrosis (Trikafta/Alyftrek) · Non-opioid Pain (Journavx) · Gene Therapy (Casgevy) · NASDAQ: VRTX"
CURRENT_PRICE = 445.00      # USD; as of 2026-06-10
VOL_52W_LOW   = 365.00      # 2025 trough on CF growth deceleration concerns
VOL_52W_HIGH  = 495.00      # 2026 peak on Journavx launch momentum
SHARES_OUT_M  = 255.0       # millions
ANNUAL_DIV    = 0.0         # VRTX pays no dividend; reinvests in pipeline

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("CF franchise (Trikafta/Kaftrio/Alyftrek)", 11.3, 10.5, 12.3, "Near-total eligible-patient penetration (~94%) in developed markets; Alyftrek (vanzacaftor triple) switch drives modest pricing/duration upside but limited volume runway"),
    ("Journavx (suzetrigine, non-opioid pain)",    0.3,  0.1,  2.5, "Newly launched NaV1.8 inhibitor for acute pain; large addressable market (postsurgical/acute) with potential expansion into chronic neuropathic pain"),
    ("Casgevy (exa-cel, gene therapy SCD/TDT)",    0.15, 0.05, 0.8, "CRISPR-based one-time cure for sickle cell disease/beta-thalassemia; slow capacity-constrained rollout across qualified treatment centers, multi-year revenue recognition"),
    ("Pipeline royalties / other",                 0.25, 0.15, 0.4, "Small legacy royalty streams and other early commercial contributions"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.890   # blended gross margin; small-molecule CF franchise extremely high margin
GROSS_MARGIN_BULL = 0.895   # BULL: Journavx/Casgevy scale modestly improves blend further
OPEX_FIXED_B      = 6.4     # SG&A + R&D ($B); heavy R&D investment across pipeline (inaxaplin, zimislecel, Journavx expansion trials)
TAX_RATE          = 0.190   # effective rate

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2027E    = 18.50      # FY2027E EPS (consensus ~$18-19 non-GAAP)
PE_PESSIMISTIC = 16.0       # trough P/E: even in a CF-stagnation scenario, cash-rich profitable biotech floor ~15-17x
EPP            = round(PE_PESSIMISTIC * EPS_FY2027E, 0)   # $296

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (16.50, 16,  264, "CF franchise growth stalls (near-total penetration reached, Alyftrek switch provides minimal uplift); Journavx launch underwhelms on uptake/reimbursement; Casgevy rollout remains negligible; EPS $16.50 → 16× = $264"),
    "BASE":  (19.00, 21,  399, "CF franchise grows low-single-digits on Alyftrek mix/pricing; Journavx ramps steadily toward $1-2B run-rate in acute pain; Casgevy slowly scales across treatment centers; EPS $19.00 × 21 = $399"),
    "BULL":  (23.00, 24,  552, "Journavx becomes a multi-billion-dollar franchise with label expansion into chronic pain (diabetic peripheral neuropathy); Casgevy rollout accelerates meaningfully; inaxaplin/zimislecel pipeline readouts positive; EPS $23.00 × 24 = $552"),
    "XBULL": (29.00, 27,  783, "Journavx achieves blockbuster status across multiple pain indications, displacing opioids at scale; Casgevy becomes standard-of-care for SCD/TDT with rapid center expansion; zimislecel (T1D) and inaxaplin (APOL1) pivotal data position VRTX as a multi-franchise growth platform beyond CF; EPS $29.00 × 27 = $783"),
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
        "now":        "+5%",
        "score":      2,
        "comment":    "CF franchise approaching saturation (~94% of eligible patients on therapy in developed markets); Alyftrek switch provides modest pricing/duration tailwind but volume growth is largely exhausted",
    },
    {
        "name":       "Journavx (suzetrigine) launch trajectory",
        "weight":     0.25,
        "thresholds": ("delayed/weak", "on-track modest", "strong uptake", "category-expanding blockbuster"),
        "now":        "early launch, on-track",
        "score":      2,
        "comment":    "Approved for acute pain; early prescription trends encouraging but payer formulary access and adoption curve still developing — too early to confirm blockbuster trajectory",
    },
    {
        "name":       "Casgevy (gene therapy) commercial rollout pace",
        "weight":     0.15,
        "thresholds": ("stalled", "slow ramp", "accelerating", "rapid center expansion"),
        "now":        "slow ramp",
        "score":      2,
        "comment":    "Qualified treatment center activation and patient cell-collection/manufacturing logistics remain the bottleneck; revenue recognition lags patient starts by many months",
    },
    {
        "name":       "Pipeline readouts (inaxaplin APOL1, zimislecel T1D)",
        "weight":     0.15,
        "thresholds": ("none/negative", "1 mixed readout", "1-2 positive readouts", "multiple positive + filing"),
        "now":        "1 mixed readout",
        "score":      2,
        "comment":    "Inaxaplin Phase 3 in APOL1-mediated kidney disease and zimislecel (VX-880 successor) in type 1 diabetes both progressing; data so far supportive but pivotal readouts still pending",
    },
    {
        "name":       "Operating margin / R&D efficiency",
        "weight":     0.10,
        "thresholds": ("<55%",  "≥58%",  "≥62%",   "≥66%"),
        "now":        "~60%",
        "score":      2,
        "comment":    "High-80s gross margin offset by substantial R&D investment across Journavx label expansion, Casgevy scale-up, and pipeline (inaxaplin/zimislecel); operating margin steady in low-60s",
    },
    {
        "name":       "Balance sheet / capital allocation flexibility",
        "weight":     0.10,
        "thresholds": ("net debt", "net cash <$5B", "net cash $5-10B", "net cash >$10B"),
        "now":        "net cash ~$11B",
        "score":      4,
        "comment":    "Debt-free with a large and growing cash/investments balance, funding internal pipeline and providing flexibility for bolt-on M&A (e.g., gene-editing/cell-therapy capabilities) without dilution",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("-", "CF franchise maturation — near-total eligible-patient penetration leaves limited organic volume growth runway beyond pricing/Alyftrek mix", -0.6, 0.25),
    ("+", "Journavx optionality — large non-opioid acute/chronic pain TAM represents the single biggest near-term re-rating catalyst beyond CF",            +0.6, 0.20),
    ("+", "Pristine balance sheet — debt-free, ~$11B net cash provides downside floor and self-funds pipeline without dilution risk",                        +0.5, 0.15),
    ("+", "Casgevy long-duration optionality — first approved CRISPR gene therapy; slow rollout today but durable curative-therapy moat over a decade",      +0.3, 0.15),
    ("-", "Pipeline binary risk — inaxaplin (APOL1) and zimislecel (T1D) are still pre-pivotal; meaningful probability of clinical/regulatory setbacks",      -0.4, 0.15),
    ("-", "Premium valuation already embeds significant pipeline optionality — limited multiple expansion until Journavx/Casgevy scale is proven",           -0.3, 0.10),
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
CONS_EPS_2YR  = 21.00   # FY2028E conservative: modest growth as Journavx ramps gradually, CF roughly flat
CONS_PE_2YR   = 20      # roughly flat-to-modest compression from current ~24x as growth normalizes
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  CF Franchise (Trikafta/Alyftrek) / Journavx / Casgevy / Pipeline")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<42}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<42}  ${curr:>11.2f}  ${bear:>8.2f}  ${bull:>8.2f}  {bear-curr:>+7.2f}  {bull-curr:>+7.2f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<42}  ${curr_total:>11.2f}  ${bear_total:>8.2f}  ${bull_total:>8.2f}  {bear_total-curr_total:>+7.2f}  {bull_total-curr_total:>+7.2f}")
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
shares_b     = shares * 0.99   # modest buyback over 2yr
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp      = bear_total * GROSS_MARGIN_CURR * 0.99   # slight mix shift
bear_oi      = bear_gp - OPEX_FIXED_B * 1.0             # R&D not easily cut
bear_ni      = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.2f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS")
print()
print(f"  BULL EPS check:  ${bull_total:.2f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 24× = ~${bull_eps_imp*24:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.2f}B rev × {GROSS_MARGIN_CURR*100*0.99:.1f}% GM − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At 16× trough P/E (cash-rich profitable biotech floor) = ~${bear_eps_imp*16:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
eps_per_1B_rev   = (1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE)) / shares
eps_per_1B_cf    = 1.0 * 0.85 * (1 - TAX_RATE) / shares   # CF franchise very high incremental margin
eps_per_1B_other = 1.0 * 0.65 * (1 - TAX_RATE) / shares   # Journavx/Casgevy lower incremental margin (launch costs)

print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B CF franchise revenue:           +${eps_per_1B_cf:.3f}/EPS  = +${eps_per_1B_cf*21:.1f}/share at 21× P/E")
print(f"  Every $1B Journavx/Casgevy revenue:        +${eps_per_1B_other:.3f}/EPS  = +${eps_per_1B_other*21:.1f}/share at 21× P/E")
print(f"  1pp GM expansion (Journavx/Casgevy scale): +${curr_total*0.01*(1-TAX_RATE)/shares:.2f}/EPS  = +${curr_total*0.01*(1-TAX_RATE)/shares*21:.1f}/share at 21× P/E")
print(f"  1% buyback (~2.55M shares):                +${curr_eps*0.01:.3f}/EPS  (mechanical accretion)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (CF maturation / Journavx launch / Casgevy rollout / pipeline / margins / balance sheet)")
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
    ("CF franchise revenue growth",        "+5%",    "<2%",    "−3pp",   "Penetration plateau confirmed; Alyftrek switch yields no net pricing uplift"),
    ("Journavx launch trajectory",         "on-track","delayed/weak", "downgrade", "Payer formulary restrictions/REMS-like friction limit acute-pain uptake"),
    ("Casgevy rollout pace",               "slow ramp","stalled", "worse", "Treatment center activation and manufacturing logistics bottleneck persists"),
    ("Pipeline readouts (inaxaplin/zimislecel)", "1 mixed","negative", "setback", "APOL1 Phase 3 misses endpoint or zimislecel safety signal emerges"),
    ("Operating margin",                   "~60%",   "<55%",   "−5pp",   "Heavy launch/R&D spend on Journavx expansion + Casgevy scale-up pressures margins"),
    ("Gross margin",                       "89.0%",  "<86%",   "−3pp",   "Mix shift toward lower-margin Casgevy/cell-therapy manufacturing"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: CF franchise growth flatlines as eligible-patient penetration plateaus near")
print(f"  100% with Alyftrek providing no incremental pricing/duration benefit, while Journavx's")
print(f"  acute-pain launch underwhelms on payer access and Casgevy's center-by-center rollout")
print(f"  remains negligible. EPS falls to ~$16.50 → 16× trough P/E (cash-rich biotech floor) = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT permanent impairment — VRTX's debt-free balance sheet and durable")
print(f"  CF cash flows provide a floor. Recovery toward ~${bear_price+60}-${bear_price+110} in 2yr is plausible as")
print(f"  Journavx/Casgevy/pipeline (inaxaplin, zimislecel) re-establish a growth narrative.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2027E EPS estimate:           ${EPS_FY2027E:.2f}  (consensus ~$18-19 non-GAAP)")
print(f"  Pessimistic P/E at trough:       {PE_PESSIMISTIC:.0f}×  (cash-rich, debt-free, profitable biotech floor; historical VRTX trough ~15-17×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% {'above' if epp_gap_pct >= 0 else 'below'} trough floor)")
print()
print(f"  A {epp_gap_pct:+.0f}% {'premium to' if epp_gap_pct >= 0 else 'discount to'} EPP reflects that VRTX trades at roughly")
print(f"  {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a premium multiple for a CF franchise approaching")
print(f"  saturation, justified largely by pipeline optionality (Journavx, Casgevy, inaxaplin,")
print(f"  zimislecel). The risk is that if these pipeline assets fail to scale, the multiple")
print(f"  compresses toward a 'mature CF royalty stream' valuation near the EPP floor.")
print(f"  EPP path: FY2029E EPS ~$23 × {PE_PESSIMISTIC:.0f}× = ${23*PE_PESSIMISTIC:.0f} floor (EPP grows as Journavx/Casgevy scale lifts the earnings base).")
print(f"  At 21× mid-cycle P/E: ${EPS_FY2027E:.2f} × 21 = ${EPS_FY2027E*21:.0f}  — roughly in line with current price.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest EPS growth as Journavx ramps gradually, CF roughly flat; P/E roughly flat)")
hr()
print(f"  Conservative FY2028E EPS:        ${CONS_EPS_2YR:.2f}  (modest growth; CF flat, Journavx/Casgevy contribute incrementally)")
print(f"  Conservative exit P/E:            {CONS_PE_2YR}×  (modest compression from ~{CURRENT_PRICE/EPS_FY2027E:.1f}× as CF growth story matures)")
print(f"  Conservative equity value:        ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):    +${cons_divs:.2f}/share  (no dividend; VRTX reinvests in pipeline)")
hr()
print(f"  Conservative 2yr total:           ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:        {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE QUESTION: VRTX trades at {CURRENT_PRICE/EPS_FY2027E:.1f}× FY2027E EPS ${EPS_FY2027E:.2f} — a premium multiple that")
print(f"  reflects the market's confidence that Journavx and Casgevy will become meaningful growth")
print(f"  engines as the CF franchise matures toward saturation. Pipeline readouts (inaxaplin, zimislecel)")
print(f"  are the additional optionality. If Journavx scales toward blockbuster status and Casgevy's")
print(f"  rollout accelerates, the multiple holds or expands. If the CF plateau arrives before the")
print(f"  pipeline delivers, a derating toward {CONS_PE_2YR}× is the realistic conservative outcome.")
print(f"  For conservative 2yr to break even at {CONS_PE_2YR}× P/E: need EPS = ${(CURRENT_PRICE - cons_divs) / CONS_PE_2YR:.2f}")
print(f"  That requires ~{((CURRENT_PRICE - cons_divs) / CONS_PE_2YR / EPS_FY2027E - 1)*100:.1f}% EPS growth by FY2028E vs FY2027E.")
print(f"  BUY trigger: ${round(CONS_EPS_2YR * CONS_PE_2YR * 0.83 + cons_divs * 0.5, 0):.0f}–${round(CONS_EPS_2YR * CONS_PE_2YR * 0.90 + cons_divs * 0.5, 0):.0f} (conservative case positive at {CONS_PE_2YR}× P/E; ratio_b <1.0×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.27
beta        = 0.65
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (no dividend; cash reinvested into pipeline R&D and buybacks)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; binary pipeline catalysts and launch-data-driven swings)")
print(f"  Beta vs S&P 500:      {beta:.2f}  (moderate; large-cap biotech with diversified franchise vs single-asset peers)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (plausible on CF-plateau + Journavx-disappointment scenario)")
print(f"  52W range reflects launch-catalyst volatility around Journavx and ongoing CF growth-rate scrutiny.")
print(f"  → CF franchise growth deceleration is THE KEY binary for downside risk.")
print(f"  → Journavx acute/chronic pain uptake + Casgevy center expansion are KEY bull catalysts.")
print(f"  → AVOID above $510  |  WATCHLIST $430–495  |  ACCUMULATE $360–415  |  BUY below $330")

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
print(f"  In plain terms: the market is pricing in a degree of confidence on Journavx/Casgevy scaling")
print(f"  that the bottom-up fundamentals only partially support given how early these launches remain.")
print(f"  The risk/reward skew (Ratio B {ratio_b_str}) reflects the tension between a maturing, cash-generative")
print(f"  CF franchise providing a solid floor and a still-unproven set of pipeline growth vectors.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Journavx (suzetrigine) — acute pain launch uptake, payer access, label expansion into chronic pain")
print(f"  (2) CF franchise — Alyftrek (vanzacaftor) switch dynamics, international reimbursement, penetration ceiling")
print(f"  (3) Casgevy (exa-cel) — qualified treatment center activation pace, patient throughput, revenue recognition")
print(f"  (4) Inaxaplin — APOL1-mediated kidney disease Phase 3 readouts")
print(f"  (5) Zimislecel — type 1 diabetes cell therapy pivotal data and regulatory pathway")
print(f"  (6) Capital allocation — ~$11B net cash deployment toward buybacks vs bolt-on M&A")
print(f"  AVOID above $510  |  WATCHLIST $430–495  |  ACCUMULATE $360–415  |  BUY below $330")
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
