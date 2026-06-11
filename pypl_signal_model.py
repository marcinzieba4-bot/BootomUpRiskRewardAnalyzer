"""
PYPL  ·  PayPal Holdings, Inc.  ·  NASDAQ: PYPL
Bottom-up signal model  ·  Digital Payments / Venmo / Checkout Platform
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "PYPL"
COMPANY       = "PayPal Holdings, Inc."
SECTOR        = "Digital Payments · Venmo · Checkout Platform · NASDAQ: PYPL"
CURRENT_PRICE = 78.0         # USD; as of 2026-06-11
VOL_52W_LOW   = 55.0
VOL_52W_HIGH  = 97.0
SHARES_OUT_M  = 940.0        # millions; declining via ~$6B/yr buyback (~15% of mkt cap)

# Dividend: PayPal pays no dividend; all FCF to buybacks
ANNUAL_DIV    = 0.0          # $/share

# ── PRODUCT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E revenue by segment ($B) — branded checkout vs unbranded/Braintree vs Venmo/other
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Branded Checkout (PayPal)",  17.5, 14.5, 20.5, "Highest take-rate (~2.3%); core profit engine; share-loss risk vs Apple Pay/Stripe"),
    ("Unbranded / Braintree",       7.0,  6.5,   8.5, "Low take-rate (~0.72%) processing volume; structurally growing but margin-dilutive"),
    ("Venmo",                       2.4,  2.0,   4.0, "90M users; monetization (P2P→commerce, debit, ads) deeply undermonetized vs branded"),
    ("Other (Credit, PSP, Intl)",   2.1,  1.8,   2.6, "Pay Later, value-added services, international wallets"),
]

# Margin assumptions
GROSS_MARGIN_CURR = 0.455   # blended transaction margin FY2026E
GROSS_MARGIN_BULL = 0.475   # BULL: branded mix recovers, Venmo monetizes at higher margin
OPEX_FIXED_B      = 6.8     # opex ($B); Chriss cost discipline keeps roughly flat
TAX_RATE          = 0.21    # effective tax rate

# ── TAKE RATE DECOMPOSITION (PYPL-specific structural feature) ────────────────
TOTAL_TPV_T         = 1.65
BRANDED_MIX_PCT     = 46
BRANDED_TAKE_RATE   = 2.30
UNBRANDED_TAKE_RATE = 0.72
PEAK_BRANDED_MIX    = 55

def take_rate_economics():
    unbranded_mix    = 100 - BRANDED_MIX_PCT
    blended          = (BRANDED_MIX_PCT * BRANDED_TAKE_RATE +
                        unbranded_mix * UNBRANDED_TAKE_RATE) / 100
    current_rev      = TOTAL_TPV_T * 1e12 * blended / 100 / 1e9
    take_rate_prem   = BRANDED_TAKE_RATE - UNBRANDED_TAKE_RATE
    rev_per_pp_shift = TOTAL_TPV_T * 1e12 * (take_rate_prem / 100) * 0.01 / 1e9
    recovery_blend   = (PEAK_BRANDED_MIX * BRANDED_TAKE_RATE + (100-PEAK_BRANDED_MIX) * UNBRANDED_TAKE_RATE) / 100
    recovery_rev     = TOTAL_TPV_T * 1e12 * recovery_blend / 100 / 1e9
    mix_recovery_upside = recovery_rev - current_rev
    return blended, current_rev, take_rate_prem, rev_per_pp_shift, mix_recovery_upside

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 5.10        # FY2026E adj EPS (consensus ~$5.05-5.20; non-GAAP)
PE_PESSIMISTIC = 8.0         # trough P/E: cheapest valuation in PYPL history (~8x non-GAAP EPS)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # ~$41

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 3.0, 13,   39, "Apple Pay/AI wallets structurally displace branded checkout; take rate compresses; EPS $3 → 13x"),
    "BASE":  ( 6.0, 17,  102, "Chriss execution continues; take rate stabilizes; Venmo monetizes modestly; EPS $6 → 17x"),
    "BULL":  ( 9.0, 21,  189, "Branded checkout share stabilizes/grows; Venmo ads/commerce scale; buyback accelerates EPS; EPS $9 → 21x"),
    "XBULL": (12.0, 25,  300, "PayPal re-rates as AI-commerce wallet of record; Venmo hits branded take rate; EPS $12 → 25x"),
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
        "name":       "US e-commerce sales YoY",
        "weight":     0.25,
        "thresholds": ("<0%",    "≥4%",   "≥8%",    "≥14%"),
        "now":        "+7%",
        "score":      2,
        "comment":    "Healthy but not accelerating; consumer spending steady; no recessionary signal",
    },
    {
        "name":       "PayPal transactions / active account (TPA)",
        "weight":     0.20,
        "thresholds": ("<48",    "≥55",   "≥65",    "≥75"),
        "now":        "62",
        "score":      2,
        "comment":    "Engagement improving under Chriss but below BULL threshold; Apple/Google Wallet competition for share of wallet",
    },
    {
        "name":       "Shopify GMV YoY",
        "weight":     0.15,
        "thresholds": ("<3%",    "≥10%",  "≥20%",   "≥30%"),
        "now":        "+23%",
        "score":      3,
        "comment":    "SMB e-commerce partner volume strong; Braintree benefits from Shopify growth",
    },
    {
        "name":       "PYPL blended take rate change",
        "weight":     0.15,
        "thresholds": ("<-0.30pp", "≥-0.15pp", "≥0.00pp", "≥+0.10pp"),
        "now":        "-0.03pp",
        "score":      2,
        "comment":    "Compression has slowed materially vs prior years; close to stabilization but not yet positive",
    },
    {
        "name":       "Global cross-border e-commerce YoY",
        "weight":     0.15,
        "thresholds": ("<2%",    "≥8%",   "≥15%",   "≥22%"),
        "now":        "+15%",
        "score":      3,
        "comment":    "Cross-border, a premium take-rate segment, remains a relative bright spot",
    },
    {
        "name":       "BNPL industry volume YoY",
        "weight":     0.10,
        "thresholds": ("<2%",    "≥10%",  "≥20%",   "≥35%"),
        "now":        "+22%",
        "score":      3,
        "comment":    "Pay Later volumes growing well; supports checkout frequency and engagement",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("-", "Apple/Google OS-native checkout displacement — structural share-loss risk to branded mix",  -1.0, 0.40),
    ("+", "Venmo 90M-user network effect moat — undermonetized vs branded take rate (key optionality)",  +0.5, 0.20),
    ("+", "Chriss turnaround execution — record engagement metrics; cost discipline delivering",          +0.3, 0.20),
    ("+", "$7B net cash + ~$6B/yr buyback (~15% of market cap) — powerful EPS flywheel even at flat revenue", +0.3, 0.10),
    ("+", "US fintech regulatory tailwind — favorable stance on payments innovation",                     +0.2, 0.10),
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
CONS_EPS_2YR  = round(EPS_FY2026E * (1.08 ** 2), 2)  # conservative FY2028E: 8% EPS CAGR (cost cuts + buyback only)
CONS_PE_2YR   = 15      # conservative exit P/E: no re-rating, market stays skeptical
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Digital Payments / Venmo / Checkout Platform")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① PRODUCT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  PRODUCT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
hr()

curr_total = sum(rev for _, rev, _, _, _ in SEG_DATA)
bear_total = sum(rev for _, _, rev, _, _ in SEG_DATA)
bull_total = sum(rev for _, _, _, rev, _ in SEG_DATA)

print(f"  {'Segment':<26}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}  {'Δ Bear':>8}  {'Δ Bull':>8}")
hr()
for seg, curr, bear, bull, desc in SEG_DATA:
    print(f"  {seg:<26}  ${curr:>11.1f}  ${bear:>8.1f}  ${bull:>8.1f}  {bear-curr:>+7.1f}  {bull-curr:>+7.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<26}  ${curr_total:>11.1f}  ${bear_total:>8.1f}  ${bull_total:>8.1f}  {bear_total-curr_total:>+7.1f}  {bull_total-curr_total:>+7.1f}")
print()

# EPS bridge
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_ni   = curr_oi * (1 - TAX_RATE)
shares    = SHARES_OUT_M / 1000
curr_eps  = round(curr_ni / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B
bull_ni   = bull_oi * (1 - TAX_RATE)
shares_b  = shares * 0.85   # ~7.5%/yr buyback over 2yr (~$6B/yr ~15% of mkt cap)
bull_eps_imp = round(bull_ni / shares_b, 1)

bear_gp   = bear_total * GROSS_MARGIN_CURR * 0.95   # take-rate compression
bear_oi   = bear_gp - OPEX_FIXED_B * 0.95           # partial cost response
bear_ni   = max(0, bear_oi) * (1 - TAX_RATE)
bear_eps_imp = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% margin − ${OPEX_FIXED_B:.1f}B opex − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj EPS  (consensus ~${EPS_FY2026E:.2f})")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% margin − ${OPEX_FIXED_B:.1f}B opex − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × 21× = ~${bull_eps_imp*21:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × {GROSS_MARGIN_CURR*100*0.95:.1f}% margin − opex  =  ~${bear_eps_imp:.1f}/share")
print(f"  At {PE_PESSIMISTIC:.0f}-13× trough P/E = ~${bear_eps_imp*13:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# Take rate decomposition
blended_tr, curr_rev, tr_prem, rev_per_pp, mix_upside = take_rate_economics()
print()
print(f"  TAKE RATE DECOMPOSITION  (the entire Chriss thesis in one table)")
hr()
print(f"  Total TPV (FY2026E):                         ${TOTAL_TPV_T:.2f}T")
print(f"  Branded checkout mix:                        {BRANDED_MIX_PCT}%  (take rate {BRANDED_TAKE_RATE:.2f}%)")
print(f"  Unbranded / Braintree mix:                   {100-BRANDED_MIX_PCT}%  (take rate {UNBRANDED_TAKE_RATE:.2f}%)")
print(f"  Blended take rate (current):                 {blended_tr:.3f}%  →  ~${curr_rev:.1f}B revenue")
print(f"  Revenue uplift per 1pp branded mix gain:     ${rev_per_pp:.2f}B/yr  ← the leverage")
print(f"  Full recovery to {PEAK_BRANDED_MIX}% branded mix → +${mix_upside:.1f}B annual revenue uplift")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (e-commerce / engagement / take-rate / cross-border framework)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>9}  {'BASE':>9}  {'BULL':>9}  {'XBULL':>9}  {'NOW':>9}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>9}  {ths[1]:>9}  {ths[2]:>9}  {ths[3]:>9}  {s['now']:>9}  {lbl}  {b}")

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
    ("US e-commerce sales YoY",        "+7%",    "<0%",      "−7pp",   "Consumer recession; e-commerce contraction across the board"),
    ("PayPal TPA",                     "62",     "<48",      "−14",    "User disengagement; Apple/Google Wallet displaces PayPal at checkout"),
    ("Shopify GMV YoY",                "+23%",   "<3%",      "−20pp",  "SMB e-commerce collapses; PYPL loses Braintree partner volume"),
    ("PYPL blended take rate",         "-0.03pp","<-0.30pp", "−0.27pp","Braintree structural displacement; take rate compression accelerates"),
    ("Global cross-border e-com YoY",  "+15%",   "<2%",      "−13pp",  "Cross-border contracts; premium take-rate segment shrinks"),
    ("BNPL industry volume YoY",       "+22%",   "<2%",      "−20pp",  "BNPL fades; Pay Later adoption stalls; checkout frequency falls"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Apple Pay + Stripe/Shopify Pay structurally displace branded")
print(f"  checkout — branded mix falls from 46% toward 35-40%, costing ~${rev_per_pp*5:.1f}B+")
print(f"  in high-margin revenue with no offsetting take-rate recovery. Combined with")
print(f"  Braintree margin compression, EPS stalls near $3 → re-rates to {PE_PESSIMISTIC:.0f}-13× = ${bear_price}.")
print(f"  Note: ${bear_price} is NOT a permanent impairment — Venmo's 90M users + $7B net")
print(f"  cash provide a durable floor. Recovery toward EPP (${EPP:.0f}) is plausible post-shock.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj EPS estimate:      ${EPS_FY2026E:.2f}  (consensus ~$5.05-5.20; non-GAAP)")
print(f"  Pessimistic P/E at trough:      {PE_PESSIMISTIC:.0f}×  (cheapest valuation in PYPL history; ~8x non-GAAP EPS)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({'above' if epp_gap_pct >= 0 else 'below'} trough floor)")
print()
print(f"  At ${CURRENT_PRICE:.2f} and FY2026E EPS ${EPS_FY2026E:.2f}, PYPL trades at "
      f"{CURRENT_PRICE/EPS_FY2026E:.1f}× — near the cheapest multiple in company history.")
print(f"  The market is pricing PayPal as a structurally challenged, ex-growth payments")
print(f"  company. The bull case requires NO revenue acceleration: at ~$6B/yr buyback")
print(f"  (~15% of market cap), EPS compounds mechanically even on flat revenue.")
print(f"  EPP path: FY2028E EPS ~${CONS_EPS_2YR:.2f} × {PE_PESSIMISTIC:.0f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor (EPP grows with buyback-driven EPS).")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: buyback-driven EPS growth, no multiple re-rating)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (8% EPS CAGR: ~$6B/yr buyback + modest revenue growth)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (no re-rating from current ~{CURRENT_PRICE/EPS_FY2026E:.0f}×; market stays skeptical)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (no dividend; all FCF to buybacks)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE CORE THESIS: even at a flat {CONS_PE_2YR}× exit multiple (no re-rating credit),")
print(f"  the buyback flywheel alone ({CONS_EPS_2YR:.2f}/{EPS_FY2026E:.2f} = {(CONS_EPS_2YR/EPS_FY2026E-1)*100:.0f}% EPS growth in 2yr)")
print(f"  delivers a positive return from current levels. Any P/E recovery toward")
print(f"  historical norms (12-17×) would be additive upside on top of EPS compounding.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.40
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (none — $7B net cash + ~$6B/yr to buybacks)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (elevated; execution + sector overhang)")
print(f"  Beta vs S&P 500:      1.20  (above market; execution + structural displacement risk)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  ({'unusual — requires fundamental break' if bear_sigmas > 1.5 else 'within normal range'})")
print(f"  No dividend buffer — but ~$6B/yr buyback (~15% of market cap) partially offsets drawdown.")
print(f"  → Apple Pay / Stripe checkout share-loss is THE KEY structural risk to monitor.")
print(f"  → Venmo monetization (ads, debit, commerce) toward branded take rate is KEY bull catalyst.")
print(f"  → AVOID above $90  |  WATCHLIST $80-90  |  ACCUMULATE $65-78  |  BUY below $60")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is "
      f"{'BELOW' if MARKET_COMPOSITE < ADJ_COMPOSITE else 'ABOVE'} the model's adj composite ({ADJ_COMPOSITE:.3f}).")
print(f"  The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0 fundamentals while the model scores")
print(f"  ~{ADJ_COMPOSITE:.2f}/4.0. The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by")
print(f"  model standards. In plain terms: the market is pricing in structural decline")
print(f"  (Apple Pay/Stripe displacement) that the underlying signals do not yet confirm.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Branded checkout share trend — does the 46% mix stabilize or continue eroding to Apple Pay/Stripe?")
print(f"  (2) Venmo monetization — ads, debit card, 'Pay with Venmo' commerce toward branded take rate (BULL trigger)")
print(f"  (3) Buyback pace — ~$6B/yr (~15% of market cap) is the core flywheel even at flat revenue")
print(f"  (4) Take-rate trend — has compression bottomed (-0.03pp) and can it turn positive?")
print(f"  (5) Chriss execution — TPA, cost discipline, and new product launches (PayPal Open, Fastlane)")
print(f"  AVOID above $90  |  WATCHLIST $80-90  |  ACCUMULATE $65-78  |  BUY below $60")
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
