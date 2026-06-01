"""
NFLX  ·  Netflix, Inc.  ·  NASDAQ: NFLX
Bottom-up signal model  ·  Streaming / Advertising / Live Events / Gaming
Date: 2026-05-31
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "NFLX"
COMPANY       = "Netflix, Inc."
SECTOR        = "Streaming · Ad-Supported Tier · Live Events · Gaming · NASDAQ: NFLX"
CURRENT_PRICE = 850.00       # USD; as of 2026-05-31
VOL_52W_LOW   = 660.40       # April 2026 tariff/sentiment trough
VOL_52W_HIGH  = 1_008.50     # January 2026 — first close above $1,000
SHARES_OUT_M  = 428.0        # millions; aggressive buyback program

ANNUAL_DIV    = 0.00         # no dividend; all capital return via buyback

# ── AD TIER FLYWHEEL CONSTANTS (company-specific calculator) ──────────────────
AD_MAU_CURR_M  =  70.0   # ad-supported monthly active users (millions) FY2026E
AD_ARPU_CURR   =  42.0   # ad revenue per MAU per year ($) — $3.50/month blended
AD_OP_MARGIN   =  0.75   # incremental OI margin on ad revenue (content sunk; ops ~25%)
TOTAL_SUBS_M   = 270.0   # total global paid subscribers FY2026E (millions)
CONTENT_COST_B =  17.5   # annual content spend ($B/yr FY2026E)
TAX_RATE       =  0.21   # effective rate (US + international blend)

# Ad tier scale scenarios: (MAU_M, arpu_$/yr, label)
AD_SCENARIOS = [
    ( 70.0,  42.0, "Current  (FY2026E)"),
    (100.0,  55.0, "BASE     (FY2027E)"),
    (160.0,  80.0, "BULL     (FY2028E)"),
    (220.0, 120.0, "XBULL    (2029+)  "),
]

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPP_EPS   = 30.00   # FY2026E adj EPS (consensus ~$29–$31)
PE_TROUGH = 22      # min viable P/E at crisis (confirmed streaming profitability floor)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # $660

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (18.00, 20,  360, "Subscriber stall + Disney bundling wins; margin reversal; EPS $18 → 20× distress"),
    "BASE":  (30.00, 30,  900, "Ad tier 100M MAU; ARM +10%; streaming consolidates; EPS $30 → 30× mid-cycle"),
    "BULL":  (40.00, 35, 1400, "Ad flywheel; live sports audience; ARM +15%; EPS $40 → 35× premium multiple"),
    "XBULL": (60.00, 35, 2100, "Global entertainment OS + gaming; AI content efficiency; EPS $60 → 35× peak"),
}

# ── SOFTMAX ───────────────────────────────────────────────────────────────────
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
SIGNALS = [
    {
        "name":       "Global paid net adds — quarterly (millions)",
        "weight":     0.25,
        "thresholds": ("<2M",    "≥5M",   "≥8M",    "≥12M"),
        "now":        "~6.5M",
        "score":      2,
        "comment":    "~6.5M/qtr; paid sharing normalised; growth from ad-tier converts + LATAM/APAC",
    },
    {
        "name":       "Average Revenue per Member (ARM) — blended global, YoY growth",
        "weight":     0.25,
        "thresholds": ("<3%",    "≥5%",   "≥9%",    "≥15%"),
        "now":        "+10%",
        "score":      3,
        "comment":    "+10% YoY; price increases (US $17→$18/mo standard) + ad tier ad revenue uplift",
    },
    {
        "name":       "Ad-supported tier MAU — monthly active users (millions)",
        "weight":     0.20,
        "thresholds": ("<30M",   "≥50M",  "≥90M",   "≥140M"),
        "now":        "~70M",
        "score":      2,
        "comment":    "~70M MAU; 26% of subs; growing ~5M/qtr; Netflix Ads Manager direct-sold scaling",
    },
    {
        "name":       "Adjusted operating margin (trailing 12 months)",
        "weight":     0.15,
        "thresholds": ("<20%",   "≥25%",  "≥30%",   "≥36%"),
        "now":        "~29.5%",
        "score":      2,
        "comment":    "~29.5%; FY2026 guidance ~29-30%; below BULL threshold; ad rev not yet accretive at scale",
    },
    {
        "name":       "Live events + sports rights — annualised revenue ($B/yr)",
        "weight":     0.10,
        "thresholds": ("<$0.5B", "≥$1B",  "≥$2.5B", "≥$5B"),
        "now":        "~$1.5B",
        "score":      2,
        "comment":    "NFL Christmas games + WWE Raw + boxing; ~$1.5B/yr; above BASE, below BULL threshold",
    },
    {
        "name":       "Netflix Games — monthly active players (MAU, millions)",
        "weight":     0.05,
        "thresholds": ("<3M",    "≥8M",   "≥20M",   "≥45M"),
        "now":        "~12M",
        "score":      2,
        "comment":    "~12M MAU; mobile-first; GTA trilogy + indie titles; optionality not yet priced",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Content moat — #1 global streaming; 7yr original IP runway; Emmy/Oscar wins compounding",       +0.7, 0.25),
    ("+", "Ad tier flywheel — 70M MAU growing; premium CPM $30-40; high incremental margin (75%)",         +0.6, 0.20),
    ("-", "Content cost inflation — $17.5B/yr base; live sports add $2-3B; FCF volatility rising",         -0.5, 0.20),
    ("-", "Competition intensity — Disney+/Hulu/ESPN bundle; Apple TV+ loss-leader; Amazon Prime video",    -0.4, 0.20),
    ("+", "Operating leverage — each $1B incremental revenue → ~$0.35B OI at current marginal margin",     +0.6, 0.10),
    ("-", "International FX drag — 60%+ members non-USD; ARM volatility from currency; emerging market FX", -0.3, 0.05),
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
    valuation_label = "MODESTLY OVERVALUED"

# ── RATIO B ───────────────────────────────────────────────────────────────────
bear_price   = SCENARIOS["BEAR"][2]
bull_price   = SCENARIOS["BULL"][2]
downside_pct = (CURRENT_PRICE - bear_price) / CURRENT_PRICE
upside_pct   = (bull_price - CURRENT_PRICE) / CURRENT_PRICE
ratio_b      = round(downside_pct / upside_pct, 2)

if ratio_b < 0.75:
    signal_short, signal_full = "BUY",       "◉ BUY"
elif ratio_b < 1.10:
    signal_short, signal_full = "ACCUMULATE","◎ ACCUMULATE"
elif ratio_b < 1.75:
    signal_short, signal_full = "WATCHLIST", "◐ WATCHLIST"
else:
    signal_short, signal_full = "AVOID",     "✕ AVOID"

# ── CONSERVATIVE GROWTH (2-yr) ────────────────────────────────────────────────
CONS_EPS_2YR = 33.00   # conservative FY2028E: ad tier disappoints; ARM growth slows to 5%
CONS_PE_2YR  = 24      # floor multiple (proven streaming platform; no existential threat)
cons_equity  = CONS_EPS_2YR * CONS_PE_2YR
cons_divs    = 0.00    # no dividend; assume buyback adds ~2%/yr (not captured here)
cons_total   = cons_equity + cons_divs
cons_return  = round((cons_total - CURRENT_PRICE) / CURRENT_PRICE * 100, 1)
cons_annual  = round(cons_return / 2, 1)

# ─────────────────────────────────────────────────────────────────────────────
#  OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
W = 72

def hr(): print("  " + "─" * W)
def bar(score):
    return "█" * score + "░" * (4 - score)

print()
print("═" * (W + 4))
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Streaming / Ad Tier / Live Events / Technology")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① AD-SUPPORTED TIER MONETISATION FLYWHEEL ──────────────────────────────
print()
print("  AD-SUPPORTED TIER MONETISATION FLYWHEEL  (the transformative earnings driver)")
hr()
print(f"  Ad tier architecture (FY2026E):")
print(f"  Ad-supported MAU: {AD_MAU_CURR_M:.0f}M  ({AD_MAU_CURR_M/TOTAL_SUBS_M*100:.0f}% of {TOTAL_SUBS_M:.0f}M total paid subscribers)")
print(f"  Ad revenue per MAU per year: ${AD_ARPU_CURR:.0f}  (${AD_ARPU_CURR/12:.2f}/month blended; room to triple vs linear TV)")
print(f"  Ad load: 4 min/hr  (vs 16 min/hr linear TV; Netflix preserving quality to protect subs)")
print(f"  CPM: $30–40  (premium brand-safe; above linear TV ~$15; growing with programmatic)")
print(f"  Incremental OI margin: ~{AD_OP_MARGIN*100:.0f}%  (content already sunk; ad ops ~25% of rev)")
print(f"  Fill rate: ~65% and rising — Netflix Ads Manager direct-sold platform launched 2025")
print()

shares_b = SHARES_OUT_M / 1000
print(f"  AD REVENUE SCALE SCENARIOS:")
print(f"  {'Scenario':<22}  {'Ad MAU':>7}  {'ARPU/yr':>8}  {'Ad Revenue':>11}  {'EPS (ads)':>10}  {'vs Current':>11}")
hr()
base_eps_ads = None
for mau, arpu, label in AD_SCENARIOS:
    rev_b   = mau * arpu / 1000
    oi_b    = rev_b * AD_OP_MARGIN
    ni_b    = oi_b * (1 - TAX_RATE)
    eps_ads = ni_b / shares_b
    if base_eps_ads is None:
        base_eps_ads = eps_ads
        delta_str = "—"
    else:
        delta_str = f"+${eps_ads - base_eps_ads:.2f}/EPS"
    print(f"  {label:<22}  {mau:>6.0f}M   ${arpu:>5.0f}/yr   ${rev_b:>6.2f}B       ${eps_ads:>5.2f}/EPS   {delta_str:>11}")

print()
bull_mau, bull_arpu, _ = AD_SCENARIOS[2]
bull_ad_eps = bull_mau * bull_arpu / 1000 * AD_OP_MARGIN * (1 - TAX_RATE) / shares_b
sub_eps_at_bull = SCENARIOS["BULL"][0] - bull_ad_eps
print(f"  At BULL: subscription EPS ~${sub_eps_at_bull:.1f} + ad-tier EPS ~${bull_ad_eps:.1f} ≈ ${SCENARIOS['BULL'][0]:.0f}/EPS total  ✓")
print()

# Sensitivities
eps_per_10_arpu   = AD_MAU_CURR_M * 10 / 1000 * AD_OP_MARGIN * (1 - TAX_RATE) / shares_b
eps_per_10m_mau   = 10 * AD_ARPU_CURR / 1000 * AD_OP_MARGIN * (1 - TAX_RATE) / shares_b
eps_per_10pp_fill = AD_MAU_CURR_M * AD_ARPU_CURR / 1000 * 0.10 * AD_OP_MARGIN * (1 - TAX_RATE) / shares_b

print(f"  KEY SENSITIVITIES  (at current {AD_MAU_CURR_M:.0f}M MAU base):")
print(f"  Every $10/yr increase in ad ARPU  (${AD_ARPU_CURR:.0f} → ${AD_ARPU_CURR+10:.0f}): +${AD_MAU_CURR_M*10/1000:.2f}B rev  =  +${eps_per_10_arpu:.2f}/EPS  =  +${eps_per_10_arpu*30:.0f}/share at 30×")
print(f"  Every 10M new ad MAU (at ${AD_ARPU_CURR:.0f}/yr ARPU): +${10*AD_ARPU_CURR/1000:.2f}B rev  =  +${eps_per_10m_mau:.2f}/EPS  =  +${eps_per_10m_mau*30:.0f}/share at 30×")
print(f"  Fill rate +10pp (~65%→75%): +${AD_MAU_CURR_M*AD_ARPU_CURR/1000*0.10:.2f}B rev  =  +${eps_per_10pp_fill:.2f}/EPS  =  +${eps_per_10pp_fill*30:.0f}/share at 30×")
print(f"  Content cost: ${CONTENT_COST_B:.1f}B/yr — every $1B more content raises breakeven ARM by ~${1000/TOTAL_SUBS_M*12:.1f}/yr")

# ─── ② SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (subscribers + ARM + ad tier + margin + live events + gaming)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>6}  {'BASE':>5}  {'BULL':>6}  {'XBULL':>7}  {'NOW':>7}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>6}  {ths[1]:>5}  {ths[2]:>6}  {ths[3]:>7}  {s['now']:>7}  {lbl}  {b}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15% hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    c = score * weight
    print(f"    {sign}  {desc[:72]:<72}  ({score:+.1f} × {weight*100:.0f}%  =  {c:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>7}  Trigger")
hr()
bear_triggers = [
    ("Global paid net adds (quarterly)",                     "~6.5M",  "<2M",    "−4.5M",  "US market saturation + Disney bundle switchi…"),
    ("ARM growth YoY",                                       "+10%",   "<3%",    "−7pp",   "Pricing power exhausted; competition forces …"),
    ("Ad-supported MAU",                                     "~70M",   "<30M",   "−40M",   "Ad boycott; GDPR ruling kills targeting; CPM…"),
    ("Adjusted operating margin",                            "~29.5%", "<20%",   "−9.5pp", "Content cost spiral; live sports rights cost…"),
    ("Live events revenue ($B/yr)",                          "~$1.5B", "<$0.5B", "−$1B",   "NFL contract not renewed; boxing flops; live…"),
    ("Gaming MAU (millions)",                                "~12M",   "<3M",    "−9M",    "Gaming pivot abandoned; studios closed; GTA …"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Disney+/Hulu/ESPN+/ABC bundle wins cord-cutter households at $15-18/mo.")
print(f"  Netflix subscriber count stalls at 270-280M globally. ARM growth slows as pricing power")
print(f"  exhausted — can't raise prices without accelerating churn. Ad tier MAU growth stalls as")
print(f"  targeting capability restricted by EU privacy ruling. OI margin reverts to 20%.")
print(f"  EPS falls to $18; multiple compresses to 20× → ${bear_price} (−{downside_pct*100:.0f}% from current).")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS × min viable trough P/E)")
hr()
print(f"  FY2026E adj EPS estimate:     ${EPP_EPS:.2f}  (consensus $29–$31)")
print(f"  Min viable P/E at trough:      {PE_TROUGH}×  (2022 trough ~18–20×; confirmed streaming floor)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  (market {epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  +{epp_gap_pct:.0f}% premium to EPP is justified by ad tier optionality not in current EPS.")
print(f"  Bear ${bear_price} is BELOW EPP ${EPP:.0f} — requires both EPS collapse AND multiple compression.")
print(f"  EPP rising path: FY2027E EPS ~${EPP_EPS+5:.0f} × {PE_TROUGH}× = ${(EPP_EPS+5)*PE_TROUGH:.0f} EPP — gap closes with earnings growth.")
print(f"  FCF EPP: ~$8B FCF ÷ {SHARES_OUT_M:.0f}M shares = ${8000/SHARES_OUT_M:.1f} FCF/shr × 24× = ${8000/SHARES_OUT_M*24:.0f} (higher floor)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: ad tier disappoints; ARM growth slows)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (ARM growth 5%/yr; ad MAU 90M; no new verticals)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (below current 28×; moderate growth discount)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Buyback yield:               ~+${CURRENT_PRICE*0.02:.0f}/share  (2%/yr; ~$400M/qtr; offsetting dilution)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f}; excl. buyback)")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr  (excl. buyback ~+2%/yr)")
print()
print(f"  Conservative case is MODESTLY NEGATIVE — NFLX at ${CURRENT_PRICE:.0f} requires BASE execution.")
print(f"  Breakeven: FY2028E EPS ≥${CURRENT_PRICE/CONS_PE_2YR:.1f} at {CONS_PE_2YR}× = ~$35-36 (ARM +8%/yr + ad tier 100M MAU).")
print(f"  Buyback yield ~2%/yr closes most of the conservative-case gap.")
print(f"  BUY trigger: ad MAU ≥90M (BULL) or ARM growth re-accelerates to ≥12%.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.38
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      none  (all return via buyback; ~$1.5-2B/yr repurchased)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (high; earnings-day moves ±10-15% common; sub data binary)")
print(f"  Beta vs S&P 500:      1.30  (high beta growth; subscriber number drives violent moves)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ move  (NFLX fell −76% in 2022; history shows severity)")
print(f"  52W low ${VOL_52W_LOW:.2f} = tariff/sentiment trough; ad tier derisked that level.")
print(f"  → EARNINGS DATE IS THE KEY EVENT: each quarterly report is ±8-15% on subscriber + ARM.")
print(f"  → Ad MAU disclosure (starting Q1 2026) is the NEW KEY METRIC — watch CPM trajectory.")
print(f"  → ACCUMULATE ${VOL_52W_LOW:.0f}–${round(CURRENT_PRICE*1.05,0):.0f}  |  BUY below $750  |  TRIM above ${round(VOL_52W_HIGH*1.05,0):.0f}")

# ─── ⑦ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print()
print("  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
hr()
probs_mkt = softmax_probs(MARKET_COMPOSITE)
print(f"  {'Scenario':<10}  {'Price':>6}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>7}  Description")
hr()
for s in ["BEAR","BASE","BULL","XBULL"]:
    pp   = probs_proxy[s] * 100
    pm   = probs_mkt[s]   * 100
    gap  = pp - pm
    pr   = SCENARIOS[s][2]
    desc = SCENARIOS[s][3][:45]
    print(f"  {s:<10}  ${pr:>5}  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): ${ev_adj:.0f}  /  Proxy EV: ${ev_prx:.0f}  /  Market EV: ${ev_mkt:.0f}  /  Current: ${CURRENT_PRICE:.0f}")
hr()
print(f"  Downside  (→ Bear ${bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull ${bull_price}):   {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b:.2f}x")
print(f"  Signal    :  {signal_full}")
print()
print(f"  Model and market are in close agreement (gap {ADJ_GAP:+.2f}). ACCUMULATE driven by asymmetry:")
print(f"  BULL ($1,400) adds +${bull_price-CURRENT_PRICE:.0f}/share upside; BEAR ($360) only −${CURRENT_PRICE-bear_price:.0f}/share downside.")
print(f"  The ad flywheel at BULL scale (~$18/EPS from ads alone) justifies the premium multiple.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) Ad MAU → ≥90M = BULL upgrade; watch quarterly disclosure closely")
print(f"  (2) ARM growth re-acceleration → ≥12%/yr; price increase + ad ARPU compounding")
print(f"  (3) Operating margin → ≥30% = BULL; confirms content cost discipline at live-events scale")
print(f"  (4) Netflix Ads Manager programmatic fill rate → ≥80% = structural CPM floor at $35+")
print(f"  ACCUMULATE ${VOL_52W_LOW:.0f}–${round(CURRENT_PRICE,0):.0f}  |  BUY below $750 (conservative case turns positive)  |  AVOID above $1,100")
print("═" * (W + 4))
print()

# ── EXPORT ────────────────────────────────────────────────────────────────────
RESULT = {
    "ticker":           TICKER,
    "signal":           signal_full,
    "signal_short":     signal_short,
    "price":            CURRENT_PRICE,
    "epp_gap_pct":      epp_gap_pct,
    "ratio_b":          ratio_b,
    "ratio_b_fmt":      f"{ratio_b:.2f}x",
    "adj_composite":    ADJ_COMPOSITE,
    "market_composite": MARKET_COMPOSITE,
    "adj_gap":          ADJ_GAP,
    "valuation":        valuation_label,
    "cons_return_2yr":  cons_return,
}

if __name__ == "__main__":
    pass
