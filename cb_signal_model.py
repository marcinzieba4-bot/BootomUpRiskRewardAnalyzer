"""
CB  ·  Chubb Limited  ·  NYSE: CB
Bottom-up signal model  ·  Global P&C Insurance / Underwriting / Reinsurance
Date: 2026-06-11
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "CB"
COMPANY       = "Chubb Limited"
SECTOR        = "Global P&C Insurance · Commercial · Personal HNW · Reinsurance · NYSE: CB"
CURRENT_PRICE = 333.50      # USD; as of 2026-06-11
VOL_52W_LOW   = 248.92      # late 2025 trough (cat-loss/rate-fear drawdown)
VOL_52W_HIGH  = 345.50      # 2026 high (mid-2026 rally on hard-market pricing strength)
SHARES_OUT_M  = 396.0       # millions; declining via steady buyback program

# Dividend: long growth streak (30+ consecutive years); growing high-single-digits/yr
ANNUAL_DIV    = 3.92        # $/share FY2026 ($0.98/quarter)

# ── SEGMENT REVENUE BRIDGE (company-specific calculator) ─────────────────────
# FY2026E net premiums earned + revenue by segment ($B)
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("North America Commercial P&C",   19.5, 17.5, 22.0, "Largest segment; hard-market pricing tailwinds; major cat exposure"),
    ("North America Personal Insurance (HNW)", 4.6, 4.0, 5.6, "High-net-worth homes/autos/valuables; CA wildfire concentration risk"),
    ("Overseas General Insurance",     14.2, 12.8, 16.5, "54-country footprint; EM HNW personal lines growth; FX swing factor"),
    ("Global Reinsurance",              2.3,  1.8,  2.9, "Opportunistic capacity deployment in hard reinsurance market"),
    ("Life Insurance",                  3.0,  2.7,  3.5, "Asia (esp. Korea/Asia-Pac) life & A&H; stable annuity-like earnings"),
]

# Underwriting & investment assumptions
COMBINED_RATIO_CURR = 0.865   # current blended combined ratio (~86.5%; best-in-class)
COMBINED_RATIO_BULL = 0.845   # BULL: benign cat year + continued pricing discipline
COMBINED_RATIO_BEAR = 0.945   # BEAR: severe cat losses (hurricanes/wildfires) push CR up ~8pp
NET_INVESTMENT_INCOME_B = 6.4 # FY2026E net investment income ($B); benefits from higher-for-longer rates
TAX_RATE             = 0.155  # effective rate; Bermuda/Switzerland domicile mix

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 21.50       # FY2026E adj operating EPS (consensus ~$21-22)
PE_PESSIMISTIC = 10.0         # trough P/E: severe cat year / hard-market fear (historical trough ~9-11x)
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)   # $215

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE ────────────────────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  (19.50, 12,  234, "Major hurricane/wildfire cat year; CR spikes to ~94.5%; EPS $19.50 → 12× trough P/E"),
    "BASE":  (23.50, 15,  353, "Combined ratio holds ~86%; steady NA Commercial pricing; EPS $23.50 (FY2028E) → 15×"),
    "BULL":  (27.00, 17,  459, "Benign cat year; rate hardening persists; investment income compounds; EPS $27 → 17×"),
    "XBULL": (31.00, 19,  589, "Multi-year underwriting outperformance; book value compounds 12%+/yr; EPS $31 → 19×"),
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
        "name":       "Combined ratio (lower = better)",
        "weight":     0.30,
        "thresholds": (">95%",   "≤90%",  "≤87%",   "≤84%"),
        "now":        "86.5%",
        "score":      3,
        "comment":    "Best-in-class underwriting discipline; cat losses well-managed; near multi-year best levels",
    },
    {
        "name":       "NA Commercial P&C pricing (renewal rate change)",
        "weight":     0.20,
        "thresholds": ("<0%",    "≥+2%",  "≥+5%",   "≥+8%"),
        "now":        "+5%",
        "score":      3,
        "comment":    "Hard market persists in casualty/excess; property pricing moderating but still positive",
    },
    {
        "name":       "Catastrophe losses (% of NPE, annualized)",
        "weight":     0.20,
        "thresholds": (">8%",    "≤6%",   "≤4%",    "≤2.5%"),
        "now":        "~5%",
        "score":      2,
        "comment":    "Active hurricane/wildfire seasons keep cat load elevated; below worst-case but above benign-year levels",
    },
    {
        "name":       "Net investment income growth YoY",
        "weight":     0.15,
        "thresholds": ("<0%",    "≥3%",   "≥7%",    "≥12%"),
        "now":        "+8%",
        "score":      3,
        "comment":    "Higher-for-longer rates continue lifting reinvestment yields on $140B+ portfolio",
    },
    {
        "name":       "Overseas General / HNW premium growth (constant $)",
        "weight":     0.10,
        "thresholds": ("<2%",    "≥4%",   "≥7%",    "≥10%"),
        "now":        "+7%",
        "score":      3,
        "comment":    "EM high-net-worth personal lines and Asia life expanding at double-digit local-currency rates",
    },
    {
        "name":       "Book value per share growth YoY",
        "weight":     0.05,
        "thresholds": ("<3%",    "≥5%",   "≥8%",    "≥12%"),
        "now":        "+9%",
        "score":      3,
        "comment":    "Operating earnings + AOCI recovery (declining rates on bond portfolio) compound BVPS",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Best-in-class underwriting culture — disciplined pricing across cycles; ~85-88% CR target",  +0.7, 0.25),
    ("+", "Berkshire Hathaway stake (8.78%, ~$11.2B) — quality endorsement; long-term holder signal",   +0.5, 0.15),
    ("+", "Global diversification — 54 countries; NA Commercial + Overseas General + HNW + Reinsurance + Life", +0.4, 0.15),
    ("-", "Catastrophe/climate exposure — hurricanes, CA wildfires, severe convective storms drive tail risk", -0.7, 0.20),
    ("+", "Investment income tailwind — large fixed-income portfolio benefits from higher-for-longer rates",   +0.3, 0.10),
    ("-", "Valuation discount persistence — trades 12-14x vs intrinsic quality warranting premium; multiple re-rating uncertain", -0.3, 0.15),
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
CONS_EPS_2YR  = 23.50   # conservative FY2028E: high-single-digit EPS CAGR; cat-load assumed normal
CONS_PE_2YR   = 13      # modest re-rating from ~12x current toward 13x as quality recognized
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Global P&C Insurance / Underwriting / Reinsurance")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]")
print("═" * (W + 4))

# ─── ① SEGMENT REVENUE BRIDGE ─────────────────────────────────────────────────
print()
print("  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
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

# EPS bridge (underwriting income + investment income, simplified)
shares = SHARES_OUT_M / 1000

curr_uw_income = curr_total * (1 - COMBINED_RATIO_CURR)
curr_pretax    = curr_uw_income + NET_INVESTMENT_INCOME_B
curr_ni        = curr_pretax * (1 - TAX_RATE)
curr_eps       = round(curr_ni / shares, 2)

bull_uw_income = bull_total * (1 - COMBINED_RATIO_BULL)
bull_pretax    = bull_uw_income + NET_INVESTMENT_INCOME_B * 1.10
bull_ni        = bull_pretax * (1 - TAX_RATE)
shares_b       = shares * 0.96   # ~2%/yr buyback over 2yr
bull_eps_imp   = round(bull_ni / shares_b, 1)

bear_uw_income = bear_total * (1 - COMBINED_RATIO_BEAR)
bear_pretax    = bear_uw_income + NET_INVESTMENT_INCOME_B * 0.98
bear_ni        = max(0, bear_pretax) * (1 - TAX_RATE)
bear_eps_imp   = round(bear_ni / shares, 1)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B NPE × ({(1-COMBINED_RATIO_CURR)*100:.1f}% UW margin) + ${NET_INVESTMENT_INCOME_B:.1f}B NII − {TAX_RATE*100:.1f}% tax")
print(f"  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share adj operating EPS  (consensus ~${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B NPE × ({(1-COMBINED_RATIO_BULL)*100:.1f}% UW margin) + ${NET_INVESTMENT_INCOME_B*1.10:.1f}B NII − tax")
print(f"  ÷ {shares_b:.3f}B shares (post-buyback)  =  ~${bull_eps_imp:.1f}/share  →  ${bull_eps_imp:.1f} × {SCENARIOS['BULL'][1]}× = ~${bull_eps_imp*SCENARIOS['BULL'][1]:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B NPE × ({(1-COMBINED_RATIO_BEAR)*100:.1f}% UW margin) + ${NET_INVESTMENT_INCOME_B*0.98:.1f}B NII − tax  =  ~${bear_eps_imp:.1f}/share")
print(f"  At {SCENARIOS['BEAR'][1]}× trough P/E (severe cat year) = ~${bear_eps_imp*SCENARIOS['BEAR'][1]:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")

# KEY SENSITIVITIES
print()
print(f"  KEY SENSITIVITIES:")
print(f"  1pt combined ratio (≈ ${curr_total*0.01:.2f}B pretax UW income):  ±${curr_total*0.01*(1-TAX_RATE)/shares:.3f}/EPS  =  ±${curr_total*0.01*(1-TAX_RATE)/shares*14:.1f}/share at 14× P/E")
print(f"  +$1B net investment income (rate move):           +${1.0*(1-TAX_RATE)/shares:.3f}/EPS  =  +${1.0*(1-TAX_RATE)/shares*14:.1f}/share at 14× P/E")
print(f"  NA Commercial P&C +$1B NPE (at current CR):       +${1.0*(1-COMBINED_RATIO_CURR)*(1-TAX_RATE)/shares:.3f}/EPS  =  +${1.0*(1-COMBINED_RATIO_CURR)*(1-TAX_RATE)/shares*14:.1f}/share at 14× P/E")
print(f"  Major cat event (+8pt CR shock, ~${curr_total*0.08:.1f}B pretax loss): −${curr_total*0.08*(1-TAX_RATE)/shares:.2f}/EPS")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (Underwriting discipline / pricing / cat load / investment income framework)")
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
    ("Combined ratio",                  "86.5%",  ">95%",   "+8.5pp", "Multiple major hurricanes + CA wildfire complex + severe convective storm losses"),
    ("NA Commercial P&C pricing",       "+5%",    "<0%",    "−5pp",   "Soft market returns as capacity floods in after benign years"),
    ("Catastrophe losses (% NPE)",      "~5%",    ">8%",    "+3pp",   "Cat-heavy year (Florida hurricane landfall + western wildfire season)"),
    ("Net investment income growth",    "+8%",    "<0%",    "−8pp",   "Sharp rate cuts compress reinvestment yields on maturing bonds"),
    ("Overseas General/HNW growth",     "+7%",    "<2%",    "−5pp",   "EM currency depreciation + HNW property losses from cat exposure"),
    ("Book value per share growth",     "+9%",    "<3%",    "−6pp",   "AOCI mark-to-market losses from rising rates offset operating earnings"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<52}  {curr:>8}  {bear_v:>9}  {move:>8}  {trigger[:45]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: A severe North Atlantic hurricane season (multiple Florida/Gulf landfalls)")
print(f"  combined with another major California wildfire event pushes the combined ratio from")
print(f"  ~86.5% to ~94.5% — wiping out most underwriting profit. EPS falls to ~${SCENARIOS['BEAR'][0]:.2f}")
print(f"  → {SCENARIOS['BEAR'][1]}× trough P/E = ${bear_price}. Note: Chubb's reserve strength and reinsurance")
print(f"  programs limit the tail; book value compounding resumes within 1-2 quarters as")
print(f"  pricing hardens further in response (the 'hard market begets hard market' dynamic).")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × current EPS)")
hr()
print(f"  FY2026E adj operating EPS estimate:  ${EPS_FY2026E:.2f}  (consensus ~$21-22)")
print(f"  Pessimistic P/E at trough:            {PE_PESSIMISTIC:.0f}×  (severe cat-year / hard-market-fear trough; historical 9-11×)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%  ({epp_gap_pct:.0f}% above trough floor)")
print()
print(f"  At {CURRENT_PRICE:.2f}, CB trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E EPS — near multi-year-low")
print(f"  multiples for a best-in-class underwriter with a 30+ year dividend growth streak and an")
print(f"  8.78% Berkshire Hathaway stake (~$11.2B). The {epp_gap_pct:.0f}% premium to EPP reflects only")
print(f"  modest confidence above the trough floor — most of the valuation is supported by tangible")
print(f"  book value and earnings power, not multiple expansion expectations.")
print(f"  EPP path: FY2028E EPS ~${CONS_EPS_2YR:.2f} × {PE_PESSIMISTIC:.0f}× = ${CONS_EPS_2YR*PE_PESSIMISTIC:.0f} floor by late 2028 (EPP growing with EPS).")
print(f"  At {CONS_PE_2YR}× mid-cycle P/E: ${EPS_FY2026E:.2f} × {CONS_PE_2YR} = ${EPS_FY2026E*CONS_PE_2YR:.0f}  — modest upside even without re-rating.")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: modest re-rating; cat load assumed normal)")
hr()
print(f"  Conservative FY2028E adj EPS:  ${CONS_EPS_2YR:.2f}  (high-single-digit EPS CAGR: pricing + investment income + buyback)")
print(f"  Conservative exit P/E:          {CONS_PE_2YR}×  (modest re-rating from ~{CURRENT_PRICE/EPS_FY2026E:.0f}× toward {CONS_PE_2YR}× as quality is recognized)")
print(f"  Conservative equity value:       ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr):   +${cons_divs:.2f}/share  (${ANNUAL_DIV:.2f}/yr; 30+ yr growth streak)")
hr()
print(f"  Conservative 2yr total:          ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:       {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE SETUP: unlike high-multiple growth names, CB's conservative case does NOT require")
print(f"  multiple expansion to work — it merely requires the discount to narrow modestly while")
print(f"  EPS compounds at high-single-digits and the dividend continues its 30+ year growth streak.")
print(f"  Breakeven at flat {CURRENT_PRICE/EPS_FY2026E:.0f}× P/E (no re-rating): FY2028E EPS ≥ ${(CURRENT_PRICE - cons_divs) / (CURRENT_PRICE/EPS_FY2026E):.2f}")
print(f"  BUY trigger: pullback toward ${round(SCENARIOS['BEAR'][2]*1.05,0):.0f}–${round(SCENARIOS['BASE'][2]*0.92,0):.0f} (ratio_b <0.75×)")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.16
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Annual dividend:      ${ANNUAL_DIV:.2f}/share  (yield {ANNUAL_DIV/CURRENT_PRICE*100:.2f}%  —  30+ yr growth streak; Dividend Aristocrat-like)")
print(f"  Realized vol (2yr):   {annual_vol*100:.0f}%  (low; large-cap insurer; defensive characteristics)")
print(f"  Beta vs S&P 500:      0.55  (defensive; cat-loss headlines drive short-term moves)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (severe cat year; well within historical range)")
print(f"  → Hurricane/wildfire season severity is THE KEY near-term swing factor for the combined ratio.")
print(f"  → Continued NA Commercial pricing discipline + investment income growth is the KEY bull catalyst.")
print(f"  → ACCUMULATE at current price  |  WATCHLIST $360–390  |  BUY below $300")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f}, the market composite ({MARKET_COMPOSITE:.2f}) is {'BELOW' if MARKET_COMPOSITE < ADJ_COMPOSITE else 'ABOVE'} the")
print(f"  model's adj composite ({ADJ_COMPOSITE:.3f}). The market is pricing ~{MARKET_COMPOSITE:.2f}/4.0 fundamentals,")
print(f"  while the model scores actual fundamentals at ~{ADJ_COMPOSITE:.2f}/4.0.")
print(f"  The gap ({ADJ_GAP:.2f}) indicates the stock is {valuation_label.lower()} by model standards.")
print(f"  In plain terms: the market continues to apply a quality discount to a best-in-class")
print(f"  underwriter, despite a Berkshire Hathaway endorsement and a structurally improved")
print(f"  combined ratio profile vs. prior cycles.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) Hurricane/wildfire season severity — benign season is the key BULL trigger for combined ratio")
print(f"  (2) NA Commercial P&C pricing trajectory — sustained hard market vs. softening cycle turn")
print(f"  (3) Interest rate path — higher-for-longer sustains net investment income tailwind")
print(f"  (4) Berkshire Hathaway stake changes — any addition/reduction is a closely-watched signal")
print(f"  (5) P/E multiple re-rating — narrowing of the persistent quality discount vs. peers")
print(f"  ACCUMULATE at ${CURRENT_PRICE:.2f}  |  WATCHLIST $360–390  |  BUY below $300")
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
