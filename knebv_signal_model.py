"""
KNEBV  ·  KONE Corporation  ·  HEL: KNEBV
Bottom-up signal model  ·  Elevators & Escalators / Service / Modernisation
Date: 2026-05-31
NOTE: All prices in EUR (Helsinki Stock Exchange listing)
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "KNEBV"
COMPANY       = "KONE Corporation"
SECTOR        = "Elevators & Escalators · Service & Modernisation · Building Technology · HEL: KNEBV · Prices in EUR"
CURRENT_PRICE = 46.00        # EUR; as of 2026-05-31
VOL_52W_LOW   = 38.20        # January 2026 trough (China property market fears)
VOL_52W_HIGH  = 57.40        # July 2025 high (service growth re-rating)
SHARES_OUT_M  = 541.0        # millions (A + B shares; B shares listed/traded)

# Progressive dividend policy; KONE has paid increasing dividends since 2008
ANNUAL_DIV    = 1.78         # €/share FY2026 (paid in two instalments)

# ── CHINA vs SERVICE CONSTANTS (company-specific calculator) ──────────────────
# Revenue architecture FY2026E (€B)
MAINTENANCE_REV_B  = 5.0    # maintenance contracts (~90% renewal; locked-in 7yr avg)
MAINTENANCE_MARGIN = 0.22   # EBIT margin: best in class for recurring industrial service
MODERN_REV_B       = 1.4    # modernisation projects (aging installed base secular tailwind)
MODERN_MARGIN      = 0.13   # EBIT margin
EMEA_NE_REV_B      = 3.8    # new equipment EMEA + Americas + Asia ex-China
EMEA_NE_MARGIN     = 0.08   # EBIT margin
CHINA_NE_REV_B     = 1.8    # new equipment China (deeply depressed; −57% from 2019 peak)
CHINA_NE_MARGIN    = 0.05   # thin margin under volume + competition pressure
CHINA_NE_PEAK_B    = 4.2    # China NE peak revenue ~FY2019 (€B)
TAX_RATE           = 0.23   # effective (Finnish statutory + international)

# ── EPP (Earnings Power Price) ─────────────────────────────────────────────────
EPP_EPS   = 2.10    # FY2026E adj EPS (€); consensus €2.05–€2.20
PE_TROUGH = 20      # trough P/E (KONE quality compounder; 2022-23 trough ~18-20×)
EPP       = round(EPP_EPS * PE_TROUGH, 0)   # €42

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (all EUR) ──────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (1.40, 16,  22, "China NE collapse + global recession; margins 10%; EPS €1.40 → 16× distress"),
    "BASE":  (2.10, 22,  46, "China stabilises; service +5%/yr; margins 12.5%; EPS €2.10 → 22× P/E"),
    "BULL":  (2.80, 26,  73, "Modernisation inflects; margins 14%; China floor; EPS €2.80 → 26× premium"),
    "XBULL": (3.60, 28, 101, "China revival + service 10%/yr + digital re-rating; EPS €3.60 → 28× peak"),
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
        "name":       "China new equipment order intake — YoY growth",
        "weight":     0.25,
        "thresholds": ("<−20%",  "≥−15%", "≥+5%",  "≥+20%"),
        "now":        "−12%",
        "score":      2,
        "comment":    "−12% YoY; improving from −28% in 2023; property starts still −20%/yr; floor forming",
    },
    {
        "name":       "Service + modernisation revenue — YoY organic growth",
        "weight":     0.25,
        "thresholds": ("<2%",    "≥4%",   "≥6%",   "≥9%"),
        "now":        "+6%",
        "score":      3,
        "comment":    "+6% YoY; 1.4M units under maintenance; modernisation backlog growing; pricing +3%",
    },
    {
        "name":       "Adjusted EBIT margin (reported, trailing 12m)",
        "weight":     0.20,
        "thresholds": ("<10%",   "≥11%",  "≥13%",  "≥15%"),
        "now":        "12.5%",
        "score":      2,
        "comment":    "12.5%; service mix rising; India + Americas pricing improving; below 13% BULL",
    },
    {
        "name":       "EMEA + Americas new equipment orders — YoY growth",
        "weight":     0.15,
        "thresholds": ("<−5%",   "≥+3%",  "≥+8%",  "≥+15%"),
        "now":        "+5%",
        "score":      2,
        "comment":    "+5% YoY; infrastructure projects offsetting residential weakness in EU; US stable",
    },
    {
        "name":       "Modernisation order backlog — YoY growth",
        "weight":     0.10,
        "thresholds": ("<0%",    "≥3%",   "≥8%",   "≥14%"),
        "now":        "+7%",
        "score":      2,
        "comment":    "+7% YoY; EU safety regulation tightening; 50% of world's 20M elevators >20yr old",
    },
    {
        "name":       "KONE Connect — connected units in maintenance base (M cumulative)",
        "weight":     0.05,
        "thresholds": ("<0.4M",  "≥0.7M", "≥1.0M", "≥1.8M"),
        "now":        "1.2M",
        "score":      3,
        "comment":    "1.2M units; predictive maintenance reducing call-outs; digital margin premium emerging",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Service moat — 1.4M units under contract; ~90% renewal rate; 7yr avg; pricing power",          +0.8, 0.25),
    ("-", "China structural headwind — NE peak €4.2B → €1.8B; property crisis structural not cyclical",    -0.8, 0.25),
    ("+", "Modernisation wave — 50% of 20M global elevators >20yr old; EU safety regulation tightening",   +0.6, 0.20),
    ("+", "Sustainability moat — KONE EcoSpace, hoistway-free tech; energy efficiency regulation tailwind", +0.4, 0.15),
    ("-", "Competition intensity — Otis, Schindler, ThyssenKrupp; Chinese OEMs (Canny, SJEC) in EM",       -0.4, 0.10),
    ("-", "EUR/HEL listing — lower liquidity vs NYSE; FX drag on non-EUR revenues; KONE family control",    -0.2, 0.05),
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
CONS_EPS_2YR = 2.20    # conservative FY2028E (€): service offset China; margins flat at 12%
CONS_PE_2YR  = 20      # floor multiple (quality compounder; service visibility)
cons_equity  = CONS_EPS_2YR * CONS_PE_2YR
cons_divs    = ANNUAL_DIV * 2
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

shares_b = SHARES_OUT_M / 1000
total_rev_b   = MAINTENANCE_REV_B + MODERN_REV_B + EMEA_NE_REV_B + CHINA_NE_REV_B
service_rev_b = MAINTENANCE_REV_B + MODERN_REV_B
svc_blend_mgn = (MAINTENANCE_REV_B * MAINTENANCE_MARGIN + MODERN_REV_B * MODERN_MARGIN) / service_rev_b

print()
print("═" * (W + 4))
print(f"  {TICKER}  ·  {COMPANY}  ·  €{CURRENT_PRICE:.2f}  ·  Elevators & Escalators / Service  [PRICES IN EUR]")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① CHINA vs SERVICE: THE EARNINGS DRIVER COMPARISON ──────────────────────
print()
print("  CHINA vs SERVICE: THE EARNINGS DRIVER COMPARISON  (the counterintuitive KONE thesis)")
hr()

total_ebit = (MAINTENANCE_REV_B * MAINTENANCE_MARGIN + MODERN_REV_B * MODERN_MARGIN +
              EMEA_NE_REV_B * EMEA_NE_MARGIN + CHINA_NE_REV_B * CHINA_NE_MARGIN)
total_ni   = total_ebit * (1 - TAX_RATE)
total_eps  = total_ni / shares_b

print(f"  KONE Revenue Architecture FY2026E:")
print(f"  {'Segment':<28}  {'Revenue':>8}  {'EBIT%':>7}  {'EBIT (€M)':>10}  {'of total rev'}")
hr()
segs = [
    ("Maintenance contracts", MAINTENANCE_REV_B, MAINTENANCE_MARGIN, "90% renewal; 7yr avg; pricing power"),
    ("Modernisation",         MODERN_REV_B,       MODERN_MARGIN,       "fastest-growing; aging installed base"),
    ("NE — EMEA/Americas",   EMEA_NE_REV_B,      EMEA_NE_MARGIN,      "recovering; infrastructure + resi"),
    ("NE — China",           CHINA_NE_REV_B,     CHINA_NE_MARGIN,     "−57% from €4.2B 2019 peak ◄ THE RISK"),
]
for name, rev, mgn, note in segs:
    ebit_m = rev * mgn * 1000
    print(f"  {name:<28}  €{rev:>5.1f}B    {mgn*100:>5.1f}%    €{ebit_m:>7.0f}M    {rev/total_rev_b*100:.0f}% ({note})")
hr()
print(f"  {'TOTAL':<28}  €{total_rev_b:>5.1f}B    {total_ebit/total_rev_b*100:>5.1f}%    €{total_ebit*1000:>7.0f}M    100%")
print(f"  After {TAX_RATE*100:.0f}% tax: €{total_ni:.3f}B net income  ÷  {SHARES_OUT_M:.0f}M shares = €{total_eps:.2f}/EPS (FY2026E)")
print()

# China sensitivity per €1B NE revenue recovered
eps_per_1b_china = 1.0 * CHINA_NE_MARGIN * (1 - TAX_RATE) / shares_b
china_full_recovery_eps = (CHINA_NE_PEAK_B - CHINA_NE_REV_B) * CHINA_NE_MARGIN * (1 - TAX_RATE) / shares_b

# Service sensitivity per 1% growth per year
eps_per_1pct_service = service_rev_b * 0.01 * svc_blend_mgn * (1 - TAX_RATE) / shares_b

print(f"  CHINA NE RECOVERY SENSITIVITY  (vs current depressed €{CHINA_NE_REV_B:.1f}B; 2019 peak was €{CHINA_NE_PEAK_B:.1f}B):")
print(f"  {'China NE revenue':<26}  {'vs current':>10}  {'EBIT impact':>12}  {'EPS impact':>11}  Notes")
hr()
for china_rev in [2.5, 3.0, 3.5, CHINA_NE_PEAK_B]:
    delta_rev  = china_rev - CHINA_NE_REV_B
    delta_ebit = delta_rev * CHINA_NE_MARGIN
    delta_eps  = delta_ebit * (1 - TAX_RATE) / shares_b
    pct_vs_peak = china_rev / CHINA_NE_PEAK_B * 100
    label = " ← PEAK" if china_rev == CHINA_NE_PEAK_B else ""
    print(f"  €{china_rev:.1f}B  ({pct_vs_peak:.0f}% of peak)          +€{delta_rev:.1f}B       +€{delta_ebit*1000:.0f}M EBIT     +€{delta_eps:.2f}/EPS{label}")

print()
print(f"  FULL China recovery (€{CHINA_NE_REV_B:.1f}B → €{CHINA_NE_PEAK_B:.1f}B peak): +€{china_full_recovery_eps:.2f}/EPS permanent benefit")
print(f"  KEY: Thin {CHINA_NE_MARGIN*100:.0f}% NE margins mean China recovery is LESS VALUABLE than feared.")
print()

print(f"  SERVICE COMPOUNDING SENSITIVITY  (maintenance + modernisation; {svc_blend_mgn*100:.0f}% blended margin):")
print(f"  {'Growth rate':<16}  {'1yr EPS add':>12}  {'3yr cumulative':>15}  {'5yr cumulative':>15}")
hr()
for g in [0.04, 0.06, 0.08, 0.10]:
    eps_yr1 = eps_per_1pct_service * g * 100
    # Cumulative: each year adds on growing base
    cum3 = sum(service_rev_b * ((1+g)**y - (1+g)**(y-1)) * svc_blend_mgn * (1-TAX_RATE) / shares_b for y in range(1,4))
    cum5 = sum(service_rev_b * ((1+g)**y - (1+g)**(y-1)) * svc_blend_mgn * (1-TAX_RATE) / shares_b for y in range(1,6))
    print(f"  {g*100:.0f}%/yr service growth  +€{eps_yr1:.3f}/EPS yr1    +€{cum3:.2f}/EPS 3yr      +€{cum5:.2f}/EPS 5yr")

print()
print(f"  VERDICT: 5yr of 7% service growth (+€{sum(service_rev_b * ((1.07)**y - (1.07)**(y-1)) * svc_blend_mgn * (1-TAX_RATE) / shares_b for y in range(1,6)):.2f}/EPS cumulative)")
print(f"  is {sum(service_rev_b * ((1.07)**y - (1.07)**(y-1)) * svc_blend_mgn * (1-TAX_RATE) / shares_b for y in range(1,6)) / china_full_recovery_eps:.1f}× more valuable than a full China NE recovery (+€{china_full_recovery_eps:.2f}/EPS).")
print(f"  The market fears China. The model says SERVICE is the bull case — and it's already happening.")

# ─── ② SIGNAL DASHBOARD ──────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (China NE + service engine + margins + EMEA + modernisation + digital)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<52}  {'BEAR':>6}  {'BASE':>5}  {'BULL':>5}  {'XBULL':>6}  {'NOW':>6}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<52}  {ths[0]:>6}  {ths[1]:>5}  {ths[2]:>5}  {ths[3]:>6}  {s['now']:>6}  {lbl}  {b}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from €{CURRENT_PRICE} + 15% hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    c = score * weight
    print(f"    {sign}  {desc[:72]:<72}  ({score:+.1f} × {weight*100:.0f}%  =  {c:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR €{bear_price})")
hr()
print(f"  {'Signal':<52}  {'Current':>8}  {'Bear val':>9}  {'Move':>7}  Trigger")
hr()
bear_triggers = [
    ("China new equipment orders YoY",                       "−12%",   "<−20%",  "−8pp",   "China developers default; new starts −40%; g…"),
    ("Service + modernisation growth YoY",                   "+6%",    "<2%",    "−4pp",   "Global recession; maintenance deferrals; pri…"),
    ("Adjusted EBIT margin",                                 "12.5%",  "<10%",   "−2.5pp", "Volume deleverage + wage inflation + content…"),
    ("EMEA + Americas NE orders YoY",                        "+5%",    "<−5%",   "−10pp",  "EU construction recession; rates stay high; …"),
    ("Modernisation backlog growth",                         "+7%",    "<0%",    "−7pp",   "Budget constraints; property owners defer; …"),
    ("KONE Connect connected units (M)",                     "1.2M",   "<0.4M",  "−0.8M",  "Cyber incident; data regulation kills IoT; …"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>7}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: Global construction recession (US rates stay at 5%+; EU sovereign stress)")
print(f"  collapses both new equipment demand and modernisation budgets simultaneously. China property")
print(f"  market enters a second leg down. KONE loses pricing power in maintenance as competitors cut.")
print(f"  EBIT margin falls to 10%; EPS collapses to €1.40; at 16× distress P/E = €{bear_price} (−{downside_pct*100:.0f}%).")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: FY2026E adj EPS × min viable trough P/E)  [EUR]")
hr()
print(f"  FY2026E adj EPS estimate:     €{EPP_EPS:.2f}  (consensus €2.05–€2.20)")
print(f"  Min viable P/E at trough:      {PE_TROUGH}×  (2022-23 trough ~18-20×; service floor prevents deeper)")
print(f"  ─────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    €{EPP:.0f}/share")
print(f"  Current €{CURRENT_PRICE:.2f} vs EPP €{EPP:.0f}:  {epp_gap_pct:+.1f}%  (market only {epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  Modest +{epp_gap_pct:.0f}% premium to EPP — limited downside from fundamental earnings floor.")
print(f"  Bear €{bear_price} is BELOW EPP €{EPP:.0f} — requires EPS collapse AND multiple compression together.")
print(f"  Service recurring revenue (€{service_rev_b:.1f}B; {service_rev_b/total_rev_b*100:.0f}% of total) provides hard earnings floor.")
print(f"  EPP rising path: FY2027E EPS ~€{EPP_EPS+0.15:.2f} × {PE_TROUGH}× = €{(EPP_EPS+0.15)*PE_TROUGH:.0f} EPP — strong fundamental support.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: China stays depressed; service offsets; margins flat)")
hr()
print(f"  Conservative FY2028E adj EPS:  €{CONS_EPS_2YR:.2f}  (service +4%/yr; China no recovery; margins 12%)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (quality floor; service visibility + dividend)")
print(f"  Conservative equity value:       €{cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +€{cons_divs:.2f}/share  (€{ANNUAL_DIV:.2f} × 2; progressive policy intact)")
hr()
print(f"  Conservative 2yr total:          €{cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from €{CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  Conservative case is MARGINALLY POSITIVE — dividend covers the multiple risk.")
print(f"  Even with China permanently depressed, service compounding sustains earnings growth.")
print(f"  Dividend yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}% is well-covered (payout ~70%; FCF conversion >90%).")
print(f"  BUY trigger: <€{VOL_52W_LOW+2:.0f} where conservative 2yr total return >10%.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT  [EUR]")
hr()
annual_vol  = 0.25
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 1),
               round(CURRENT_PRICE * (1 + annual_vol), 1))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        €{VOL_52W_LOW:.2f}  –  €{VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      €{ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.1f}%  —  progressive; 17yr growth streak)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (moderate; large-cap quality compounder; China binary events)")
print(f"  Beta vs EuroStoxx:    0.85  (defensive; service recurring revenue mutes cyclicality)")
print(f"  1-sigma range (1yr):  €{sigma_range[0]:.1f}  –  €{sigma_range[1]:.1f}  (€{CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear €{bear_price} requires:  ~{bear_sigmas:.1f}σ move  (China headline risk drives sudden −15-20% dips)")
print(f"  → China property data (monthly) is the primary volatility trigger for KONE stock.")
print(f"  → At {vol_pct*100:.0f}th pct of 52W range — near the 52W low; China fears already embedded in price.")
print(f"  → ACCUMULATE €{VOL_52W_LOW:.0f}–€{round(CURRENT_PRICE*1.08,0):.0f}  |  BUY below €42 (EPP zone)  |  TRIM above €{VOL_52W_HIGH:.0f}")

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
    print(f"  {s:<10}  €{pr:>5}  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV (2yr): €{ev_adj:.0f}  /  Proxy EV: €{ev_prx:.0f}  /  Market EV: €{ev_mkt:.0f}  /  Current: €{CURRENT_PRICE:.0f}")
hr()
print(f"  Downside  (→ Bear €{bear_price}):  {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull €{bull_price}):    {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b:.2f}x")
print(f"  Signal    :  {signal_full}")
print()
print(f"  Market and model broadly agree (gap {ADJ_GAP:+.2f}). The China service trade-off is the crux:")
print(f"  market prices China recovery as the re-rating catalyst; model says service is already there.")
print(f"  KONE is a HIGH-QUALITY COMPOUNDER mispriced by China overhang — not a recovery bet.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts: (1) China property new starts stabilisation (monthly NBS data; watch Q3 2026)")
print(f"  (2) Service organic growth → ≥7% = proof of pricing power + KONE Connect premium")
print(f"  (3) EBIT margin → ≥13% = BULL upgrade; confirms service mix shift and cost leverage")
print(f"  (4) Modernisation backlog → ≥€2.5B; EU elevator safety directive enforcement starts 2027")
print(f"  ACCUMULATE €38–€{CURRENT_PRICE:.0f}  |  BUY below €42 (EPP zone)  |  TRIM above €{VOL_52W_HIGH:.0f}  [ALL IN EUR]")
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
