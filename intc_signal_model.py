"""
INTC  ·  Intel Corporation  ·  NASDAQ: INTC
Bottom-up signal model  ·  Semiconductors / Foundry Turnaround / AI PC / Data Center
Date: 2026-08-03
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "INTC"
COMPANY       = "Intel Corporation"
SECTOR        = "Semiconductors · Foundry Turnaround · AI PC · Data Center · NASDAQ: INTC"
CURRENT_PRICE = 90.20        # USD; close 2026-07-31 (verified live)
VOL_52W_LOW   = 18.97        # 2025 pre-turnaround, pre-strategic-capital trough
VOL_52W_HIGH  = 142.35       # 2026 turnaround-momentum peak
SHARES_OUT_M  = 5_043.0      # millions; $455.0B mkt cap / $90.20; diluted by the 2025 government/Nvidia/SoftBank raises
ANNUAL_DIV    = 0.0          # $/share; dividend remains suspended, capital preserved for capex

# ── SEGMENT REVENUE BRIDGE (FY2026E, $B) ──────────────────────────────────────
# Q1 actual $13.6B (+7%); Q2 actual $16.1B (+25%, fastest growth since 2011), DCAI $6.3B (+59%),
# Foundry $5.8B (+6% qoq, external only $293M ≈5% of segment). Q3 guide: $15.8-16.8B, EPS $0.38.
SEG_DATA = [
    # (segment, curr_rev_B, bear_rev_B, bull_rev_B, description)
    ("Client Computing (Core Ultra/AI PC)", 34.0, 27.0, 40.0, "Panther Lake (18A) ramps H2 2026 — the swing factor for both share and margin"),
    ("Data Center & AI",                    24.0, 17.0, 32.0, "+59% YoY in Q2; hyperscaler server demand the clearest bright spot in the print"),
    ("Foundry (external) + Network/Edge",    4.0,  2.5,  7.0, "External foundry still only ~5% of Foundry segment revenue — the turnaround's real proof point"),
]

# Margin assumptions (non-GAAP)
GROSS_MARGIN_CURR = 0.400   # FY2026E blended non-GAAP gross margin; Q3 guided to 42%, still depressed by node-transition + foundry costs
GROSS_MARGIN_BULL = 0.480   # BULL: 18A/14A yields keep improving, external foundry volume adds high-margin revenue
OPEX_FIXED_B      = 16.2    # R&D + SG&A ($B); Intel is not cutting its way to the turnaround, it's spending through it
TAX_RATE          = 0.150   # low effective rate reflecting large accumulated NOLs

# ── STRATEGIC CAPITAL / FOUNDRY TURNAROUND CALCULATOR (the Intel-specific angle) ─
GOV_STAKE_PCT       = 10.0   # % of Intel now owned by the US government (~$8.9B)
NVIDIA_INVEST_B     =  5.0   # $B Nvidia invested in Intel common stock, Sept 2025
SOFTBANK_INVEST_B   =  2.0   # $B SoftBank invested in Intel common stock, 2025
FOUNDRY_EXT_REV_M   =  293   # $M external Foundry revenue, Q2 2026 (~5% of the $5.8B Foundry segment)
CAPEX_GUIDE_2026_B  = 20.0   # $B+ FY2026 capex guidance, raised at Q2
GUIDANCE_BEAT_STREAK =  7    # consecutive quarters of beating Intel's own guidance through Q2 2026

# ── EPP (Earnings Power Price) ────────────────────────────────────────────────
EPS_FY2026E    = 1.45        # $/share non-GAAP FY2026E; Q1 $0.29 + Q2 $0.42 + Q3E guide $0.38 + Q4E ~$0.36
PE_PESSIMISTIC = 65.0        # trough P/E: with EPS this early in a turnaround, a conventional multiple
                              # isn't meaningful — this credits real strategic-asset value beyond trailing earnings
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (2-year horizon → FY2028E) ────────────────────────────────
SCENARIOS = {
    "BEAR":  ( 0.31, 81,   25, "18A/14A yields disappoint; external foundry customers don't materialize; turnaround stalls near breakeven"),
    "BASE":  ( 2.70, 34,   92, "Panther Lake ramps as planned; DCAI keeps compounding; foundry external revenue grows off a tiny base"),
    "BULL":  ( 3.39, 35,  119, "14A wins real external customers; DCAI scales further; margin recovers toward the high-40s"),
    "XBULL": ( 5.00, 42,  210, "Intel re-establishes itself as a credible #2 foundry and a real AI-infrastructure compute player"),
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
        "weight":     0.20,
        "thresholds": ("<5%",    "≥12%",   "≥20%",   "≥30%"),
        "now":        "+25%",
        "score":      3,
        "comment":    "Q2 $16.1B (+25%), the fastest growth since 2011, beating the guidance midpoint by $1.8B",
    },
    {
        "name":       "Data Center & AI revenue YoY growth",
        "weight":     0.20,
        "thresholds": ("<15%",   "≥30%",   "≥45%",   "≥60%"),
        "now":        "+59%",
        "score":      4,
        "comment":    "Record server growth on hyperscaler demand — the clearest evidence the turnaround has commercial traction",
    },
    {
        "name":       "External foundry revenue (% of segment)",
        "weight":     0.20,
        "thresholds": ("<2%",    "≥5%",    "≥12%",   "≥25%"),
        "now":        "~5%",
        "score":      2,
        "comment":    "$293M of the $5.8B Foundry segment — this is the number that decides if IFS is a real business or a subsidized cost center",
    },
    {
        "name":       "Non-GAAP gross margin",
        "weight":     0.15,
        "thresholds": ("<35%",   "≥40%",   "≥45%",   "≥50%"),
        "now":        "~42%",
        "score":      2,
        "comment":    "Q3 guided to 42% — recovering, but still well below Intel's historical 55-60%+ margin structure",
    },
    {
        "name":       "Guidance beat streak",
        "weight":     0.10,
        "thresholds": ("miss",   "1-3 qtrs","4-6 qtrs","7+ qtrs"),
        "now":        "7 qtrs",
        "score":      4,
        "comment":    "Seven consecutive quarters beating Intel's own guidance — the most consistent execution signal in years",
    },
    {
        "name":       "Forward P/E (non-GAAP)",
        "weight":     0.15,
        "thresholds": (">80x",   "≤60x",   "≤45x",   "≤30x"),
        "now":        "~62x",
        "score":      1,
        "comment":    "62× FY2026E — rich for a company still GAAP-unprofitable; a lot of turnaround success is already priced in",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "Strategic capital floor — $8.9B US government, $5B Nvidia, $2B SoftBank; none of these backers want a failure", +0.7, 0.20),
    ("+", "DCAI momentum is real — +59% YoY, record hyperscaler server demand, not a one-quarter fluke",                  +0.6, 0.15),
    ("-", "External foundry is still tiny — ~5% of the segment; IFS remains subsidized by Intel Products, not yet a standalone business", -0.7, 0.20),
    ("-", "Valuation has already run hard — up ~375% from the 2025 trough; a lot of the turnaround optimism is in the price", -0.7, 0.20),
    ("+", "Execution consistency — 7 straight guidance beats is the best evidence yet that this management team can deliver", +0.4, 0.15),
    ("-", "Still GAAP-unprofitable — TTM GAAP EPS -$2.30; non-GAAP profitability is real but the full P&L isn't there yet", -0.4, 0.10),
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
CONS_EPS_2YR  = 2.10    # conservative FY2028E: turnaround continues but slower than the BASE case
CONS_PE_2YR   = 28      # multiple compresses from ~62× today toward a still-generous turnaround-story level
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
print(f"  {TICKER}  ·  {COMPANY}  ·  ${CURRENT_PRICE:.2f}  ·  Semiconductors / Foundry Turnaround / AI PC / Data Center")
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
print(f"  Q1 actual $13.6B (+7%), Q2 actual $16.1B (+25%). Q3 guide: $15.8-16.8B, EPS $0.38")
print()

# EPS bridge
shares    = SHARES_OUT_M / 1000
curr_gp   = curr_total * GROSS_MARGIN_CURR
curr_oi   = curr_gp - OPEX_FIXED_B
curr_eps  = round(curr_oi * (1 - TAX_RATE) / shares, 2)

bull_gp   = bull_total * GROSS_MARGIN_BULL
bull_oi   = bull_gp - OPEX_FIXED_B * 1.10
shares_b  = shares * 1.00
bull_eps_imp = round(bull_oi * (1 - TAX_RATE) / shares_b, 2)

bear_gp   = bear_total * 0.360     # margin compression if the node transition and foundry losses both persist
bear_oi   = bear_gp - OPEX_FIXED_B * 0.92
bear_eps_imp = round(max(0, bear_oi) * (1 - TAX_RATE) / shares, 2)

print(f"  FY2026E EPS check:  ${curr_total:.1f}B rev × {GROSS_MARGIN_CURR*100:.1f}% GM − ${OPEX_FIXED_B:.1f}B opex")
print(f"  − {TAX_RATE*100:.1f}% tax  ÷ {shares:.3f}B shares  =  ${curr_eps:.2f}/share  (model estimate ${EPS_FY2026E:.2f}  ✓)")
print()
print(f"  BULL EPS check:  ${bull_total:.1f}B rev × {GROSS_MARGIN_BULL*100:.1f}% GM − opex")
print(f"  =  ~${bull_eps_imp:.2f}/share  →  × 35× = ~${bull_eps_imp*35:.0f}  ✓ BULL ${SCENARIOS['BULL'][2]}")
print()
print(f"  BEAR EPS check:  ${bear_total:.1f}B rev × 36.0% GM (node transition + foundry losses persist) − opex")
print(f"  =  ~${bear_eps_imp:.2f}/share  →  × 81× trough = ~${bear_eps_imp*81:.0f}  ✓ BEAR ${SCENARIOS['BEAR'][2]}")
print()
print(f"  ⚠ NOTE THE SHARE COUNT: {SHARES_OUT_M/1000:.1f}B shares outstanding — nearly 6× a typical large-cap semi at this")
print(f"  market cap — means even large dollar swings in operating income translate into modest")
print(f"  per-share moves. The 2025 capital raises fixed the balance sheet; they also mean every")
print(f"  dollar of future profit is split more ways than it used to be.")

# STRATEGIC CAPITAL / TURNAROUND CHECK
print()
print(f"  STRATEGIC CAPITAL & TURNAROUND CHECK  (the Intel-specific angle):")
print(f"  US government stake:          {GOV_STAKE_PCT:.0f}%  (~$8.9B, 2025)")
print(f"  Nvidia investment:             ${NVIDIA_INVEST_B:.0f}B  (common stock, Sept 2025; joint product development)")
print(f"  SoftBank investment:           ${SOFTBANK_INVEST_B:.0f}B  (common stock, 2025)")
print(f"  External Foundry revenue:      ${FOUNDRY_EXT_REV_M}M  (~5% of the ${SEG_DATA[2][1]:.1f}B Foundry+ segment)")
print(f"  FY2026 capex guidance:         ${CAPEX_GUIDE_2026_B:.0f}B+  (raised at Q2 on growing 18A/14A customer confidence)")
print(f"  Guidance beat streak:          {GUIDANCE_BEAT_STREAK} consecutive quarters through Q2 2026")
print()
print(f"  Roughly $16B of strategic capital from the US government, Nvidia, and SoftBank is a")
print(f"  genuine downside backstop — none of these parties benefit from an Intel failure, and")
print(f"  that changes the shape of the bear case versus a normal cyclical semiconductor company.")
print(f"  But it is not a substitute for the actual proof point: external Foundry customers paying")
print(f"  Intel to make their chips. At ~5% of segment revenue, that proof point is still early.")

# KEY SENSITIVITIES
print()
eps_per_1B_rev  = 1.0 * GROSS_MARGIN_CURR * (1 - TAX_RATE) / shares
eps_per_1pp_gm  = curr_total * 0.01 * (1 - TAX_RATE) / shares
print(f"  KEY SENSITIVITIES:")
print(f"  Every $1B revenue (at 40% GM):        +${eps_per_1B_rev:.3f}/EPS  = +${eps_per_1B_rev*34:.2f}/share at 34× P/E")
print(f"  Every 1pp of gross margin:             +${eps_per_1pp_gm:.3f}/EPS  = +${eps_per_1pp_gm*34:.2f}/share at 34× P/E")
print(f"  Every 1 turn of P/E:                   ±${EPS_FY2026E:.2f}/share  ({EPS_FY2026E/CURRENT_PRICE*100:.1f}% of the stock)")

# ─── ② SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (revenue growth / DCAI / external foundry / margin / execution / valuation)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<40}  {'BEAR':>7}  {'BASE':>8}  {'BULL':>8}  {'XBULL':>7}  {'NOW':>8}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<40}  {ths[0]:>7}  {ths[1]:>8}  {ths[2]:>8}  {ths[3]:>7}  {s['now']:>8}  {lbl}  {b}")
    print(f"    {s['comment']}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from ${CURRENT_PRICE} + 15%/yr hurdle)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:88]:<88}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")

# ─── ③ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${bear_price})")
hr()
print(f"  {'Signal':<32}  {'Current':>10}  {'Bear val':>10}  {'Move':>8}  Trigger")
hr()
bear_triggers = [
    ("Total revenue YoY",           "+25%",   "<5%",     "-20pp",  "AI PC and DCAI demand both normalize sharply"),
    ("DCAI revenue YoY",            "+59%",   "<15%",    "-44pp",  "Hyperscalers dual-source away from Intel Xeon toward custom silicon/Nvidia"),
    ("External foundry revenue",    "~5%",    "<2%",     "-3pp",   "18A/14A fail to win meaningful external customers despite the roadmap progress"),
    ("Non-GAAP gross margin",       "~42%",   "<35%",    "-7pp",   "Node-transition costs and foundry losses both persist longer than guided"),
    ("Guidance beat streak",        "7 qtrs", "miss",    "break",  "The most bullish execution signal in the model reverses"),
    ("Forward P/E",                 "~62x",   "≤30x",    "-32x",   "Market decides the turnaround story doesn't yet justify the premium"),
]
for name, curr, bear_v, move, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>10}  {bear_v:>10}  {move:>8}  {trigger[:44]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: the single number that resolves this entire debate is external Foundry")
print(f"  revenue as a share of the segment. Everything else in this dashboard — DCAI growth,")
print(f"  the guidance beat streak, Client Computing share — can be genuinely excellent and Intel")
print(f"  still fails the turnaround thesis if IFS never becomes a real, third-party business.")
print(f"  At ~5% today, the bear case isn't a prediction of failure — it's a statement that the")
print(f"  proof point the market is paying 62× forward earnings for hasn't arrived yet.")

# ─── ④ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
hr()
print(f"  FY2026E non-GAAP EPS:       ${EPS_FY2026E:.2f}  (Q1 $0.29 + Q2 $0.42 + Q3 guide $0.38 + Q4E ~$0.36)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (a conventional multiple isn't meaningful this early in a turnaround;")
print(f"  this credits real strategic-asset value beyond trailing earnings)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    ${EPP:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${EPP:.0f}:  {epp_gap_pct:+.1f}%")
print()
print(f"  At ${CURRENT_PRICE:.2f} the stock trades at {CURRENT_PRICE/EPS_FY2026E:.1f}× FY2026E non-GAAP EPS — {epp_gap_pct:.0f}% BELOW even")
print(f"  this model's own 65× 'pessimistic' floor multiple on CURRENT earnings power. That is a")
print(f"  narrower reading than ratio B, and the two metrics are answering different questions:")
print(f"  EPP asks whether today's earnings power alone justifies the price at a harsh multiple —")
print(f"  and on that test, INTC screens fine. Ratio B asks what happens if earnings power itself")
print(f"  deteriorates over two years, which is the scenario the AVOID signal is actually flagging.")
print(f"  At a 45× reversion (still a rich multiple for a semiconductor turnaround): ${EPS_FY2026E:.2f} × 45 = ${EPS_FY2026E*45:.0f}")
print(f"  ({(EPS_FY2026E*45/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ─── ⑤ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr: turnaround continues but slower, multiple compresses)")
hr()
print(f"  Conservative FY2028E EPS:  ${CONS_EPS_2YR:.2f}  (steady but unspectacular progress from the ${EPS_FY2026E:.2f} FY2026E base)")
print(f"  Conservative exit P/E:      {CONS_PE_2YR}×  (~62× → 28×; a real de-rating as the story matures)")
print(f"  Conservative equity value:   ${cons_equity:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${cons_divs:.2f}/share  (dividend remains suspended)")
hr()
print(f"  Conservative 2yr total:      ${cons_total:.2f}  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: even continued (if unspectacular) EPS growth, paired with a real")
print(f"  multiple compression toward a level still generous for a company this early in a")
print(f"  turnaround, produces a {'negative' if cons_return < 0 else 'modest'} conservative return. The stock has already re-rated a great deal")
print(f"  on strategic backing and execution momentum; the model's read is that you are now paying")
print(f"  for the turnaround to succeed, not being paid to wait and see.")
print(f"  Breakeven at 28× requires FY2028E EPS ≥ ${CURRENT_PRICE / CONS_PE_2YR:.2f} — {'above' if CURRENT_PRICE / CONS_PE_2YR > CONS_EPS_2YR else 'below'} this conservative estimate.")

# ─── ⑥ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.55
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 0),
               round(CURRENT_PRICE * (1 + annual_vol), 0))
bear_sigmas = (CURRENT_PRICE - bear_price) / (CURRENT_PRICE * annual_vol)
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Move off the low:      +{(CURRENT_PRICE/VOL_52W_LOW-1)*100:.0f}%  in roughly a year — the turnaround re-rating in one number")
print(f"  Annual dividend:      none — suspended, capital preserved for the ${CAPEX_GUIDE_2026_B:.0f}B+ FY2026 capex program")
print(f"  Realized vol (1yr):   {annual_vol*100:.0f}%  (still a high-beta turnaround story despite the strategic capital)")
print(f"  Beta vs S&P 500:      1.60  (semiconductor cyclicality plus turnaround-specific execution risk)")
print(f"  1-sigma range (1yr):  ${sigma_range[0]:.0f}  –  ${sigma_range[1]:.0f}  (${CURRENT_PRICE:.2f} ± {annual_vol*100:.0f}%)")
hr()
print(f"  Bear ${bear_price} requires:  ~{bear_sigmas:.1f}σ drawdown  (would retest territory well below the current 52W low)")
print(f"  → External Foundry revenue disclosure each quarter is the single highest-signal number to track.")
print(f"  → Panther Lake's H2 2026 launch and reception is the next major Client Computing catalyst.")
print(f"  → AVOID at current price  |  WATCHLIST $70–85  |  ACCUMULATE $55–65  |  BUY below $40")

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
print(f"  MARKET PRICING: at ${CURRENT_PRICE:.2f} the market composite is {MARKET_COMPOSITE:.2f}/4.0. The model's")
print(f"  adjusted composite is {ADJ_COMPOSITE:.2f}/4.0, for a gap of {ADJ_GAP:+.2f} — {valuation_label.lower()}.")
print(f"  Intel's turnaround is genuinely further along than it was a year ago — DCAI growth,")
print(f"  the guidance beat streak, and the strategic capital are all real. But the stock has")
print(f"  already re-rated ~375% off its low pricing in a great deal of that progress, while the")
print(f"  one metric that would fully validate the foundry thesis — external customer revenue — remains small.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) External Foundry revenue disclosure each quarter — the single number that validates or breaks the thesis")
print(f"  (2) Panther Lake (18A) H2 2026 launch reception — Client Computing share and margin implications")
print(f"  (3) 14A PDK 0.9 (targeted October) and any named external 14A customer commitments")
print(f"  (4) DCAI growth durability — needs to hold well above 30% to keep validating the AI-server narrative")
print(f"  (5) Capex discipline vs the $20B+ guide — funding the turnaround without over-extending the balance sheet")
print(f"  AVOID at ${CURRENT_PRICE:.2f}  |  WATCHLIST $70–85  |  ACCUMULATE $55–65  |  BUY below $40")
print(f"  EPP floor: ${EPP:.0f}  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  FY2026E EPS: ${EPS_FY2026E:.2f}  |  External foundry: ~5% of segment")
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
