#!/usr/bin/env python3
"""
MU Signal Model  v3
───────────────────
Micron Technology, Inc. (NASDAQ: MU)  ·  Memory Semiconductors · DRAM/NAND/HBM

Format: segment revenue bridge → signal dashboard → bear anatomy → CXMT threat
        check → updated EPP → conservative growth → volatility → probability
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 935.39    # USD (NASDAQ: MU, 2026-08-24)
PREV_CLOSE      = 897.77    # 2026-08-21 close
PRICE_1WK_AGO   = 897.77   # 2026-08-17 close (near the stock's all-time high, pre-Samsung-selloff)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

SCENARIOS = {
    #           EPS     mult  price   narrative
    "BEAR":  ( 14.36,    8,    115,  "CXMT-driven DRAM oversupply; GM collapses to 35%"),
    "BASE":  ( 90.00,   11,    990,  "AI/HBM demand and CXMT competition roughly offset"),
    "BULL":  (117.10,   13,   1523,  "HBM supercycle outruns CXMT's ramp; pricing power holds"),
    "XBULL": (137.50,   16,   2200,  "HBM TAM hits $100B+ on schedule; Micron holds share"),
}

# ── SEGMENT REVENUE BRIDGE (Micron-specific structural feature) ───────────
FY2026E_DRAM_B, BEAR_DRAM_B, BULL_DRAM_B = 99.0, 55.0, 145.0
FY2026E_NAND_B, BEAR_NAND_B, BULL_NAND_B = 30.0, 20.0, 42.0
Q1_REV_B, Q2_REV_B, Q3_REV_B_ACTUAL      = 13.64, 23.86, 41.5
Q4_GUIDE_B, Q4_GUIDE_BEAT_B              = 50.0, 6.55

FY2026E_EPS      = 73.00   # Q1 $4.78 + Q2 $12.20 + Q3 $25.11 (actual) + Q4E $31.00 (guide midpoint)
FY2026E_SHARES_B = 1.150
FY2026E_GM_PCT   = 0.816

def segment_bridge():
    total_now  = FY2026E_DRAM_B + FY2026E_NAND_B
    total_bear = BEAR_DRAM_B + BEAR_NAND_B
    total_bull = BULL_DRAM_B + BULL_NAND_B
    eps_check_now  = (total_now * FY2026E_GM_PCT - 6.5) * (1 - 0.15) / FY2026E_SHARES_B
    eps_check_bull = (total_bull * 0.860) / FY2026E_SHARES_B * 0.60   # post-buyback approximation retained from prior model
    eps_check_bear = (75.0 * 0.35 - 6.5) / FY2026E_SHARES_B
    return total_now, total_bear, total_bull, eps_check_now

# ── CXMT COMPETITIVE THREAT CHECK (the Micron-specific risk) ──────────────
CXMT_WSPM_2026E       = 350_000
MU_WSPM_APPROX        = 375_000
CXMT_IPO_RAISE_B      = 8.6
CXMT_IPO_POP_PCT      = 466
MU_MCAP_ERASED_B      = 45.0
HBM_TAM_2025_B        = 35
HBM_TAM_2028E_B       = 100
CXMT_Q1_DRAM_SHARE_PCT = 8.0
MU_Q1_DRAM_SHARE_PCT   = 22.0
CXMT_2ND_FAB_NOTE = ("Aug 24 reports that Washington may let Apple source China-market memory from CXMT/YMTC reignited the "
                      "competitive-threat narrative (analysts note the practical impact is limited to China-only Apple SKUs), "
                      "compounding a Samsung shareholder-return disappointment that hit the whole memory sector")

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
# (name, unit, bear_value, base_floor, bull_floor, xbull_floor,
#  current_value, higher_is_better, bear_narrative)
SIGNALS = [
    ("Revenue YoY growth",              "%",
      50.0,  100, 200, 300,  346.0, True,
     "CXMT floods the commodity DRAM market; pricing power evaporates"),

    ("Gross margin trajectory",         "%",
      50.0,   65,  78,  85,   85.5, True,
     "Classic memory down-cycle; oversupply crushes margins"),

    ("HBM TAM capture",                 "/4 scale",
       1.0,    2,   3,   4,    3.0, True,
     "Alternative memory architectures or a slower AI buildout stalls HBM TAM growth"),

    ("CXMT / Chinese DRAM threat",      "/4 scale",
       3.0,    2,   1,   0,    2.0, False,
     "CXMT's second Beijing fab comes online faster than expected"),

    ("Forward P/E (inverted)",          "x",
      25.0,   18,  13,   9,   12.3, False,
     "Ironically, P/E can re-rate higher even as the stock falls, if EPS falls faster"),

    ("Q4 guidance vs Street consensus", "/4 scale",
       1.0,    2,   3,   4,    4.0, True,
     "A single quarter's beat proves to be peak-cycle, not trend"),
]
WEIGHTS = [0.20, 0.20, 0.10, 0.25, 0.10, 0.15]

# Display labels for qualitative /4-scale signals (bear, base, bull, xbull, current)
QUAL_LABELS = {
    "HBM TAM capture":            ("shrinking", "flat", "growing", "tripling", "$35B→$100B by 2028"),
    "CXMT / Chinese DRAM threat": ("share loss now", "parity risk", "manageable", "non-factor", "parity risk"),
    "Q4 guidance vs Street consensus": ("well below", "below", "in-line", "above", "well above"),
}

STRUCTURAL_FACTORS = [
    ("HBM demand is structurally durable through the 2028 AI buildout",         0.6, 0.20),
    ("CXMT and Chinese DRAM capacity are the single biggest 2-yr risk",        -0.6, 0.25),
    ("Memory is a historically brutal boom-bust cycle; 85%+ GM is cyclical",   -0.5, 0.20),
    ("At ~12x forward earnings the stock is still priced for skepticism",      0.4, 0.15),
    ("HBM customer base spans essentially every AI accelerator maker",         0.3, 0.10),
    ("Capex intensity rising sharply to chase capacity, pressuring FCF",      -0.3, 0.10),
]

# ── UPDATED EPP ─────────────────────────────────────────────────────────────
EPP_TODAY_EPS      = FY2026E_EPS   # $73.00 FY2026E non-GAAP EPS
EPP_MIN_PE         = 8.0           # Micron's own multi-cycle memory-trough average P/E
EPP_HISTORICAL     = 584.0         # = EPP_TODAY_EPS * EPP_MIN_PE
EPP_REGIME_NOTE    = "(Micron's own multi-cycle memory-trough average P/E)"

# ── CONSERVATIVE GROWTH (2-yr, base-minus assumptions) ───────────────────────
CONS_EPS_2028      = 85.00  # below FY2026E — assumes the cycle has partially rolled over
CONS_EXIT_PE       = 10.0   # ~12x → 10x; a modest further de-rating
CONS_DIVIDEND_2YR  = 0.92   # $0.46/yr, cumulative 2yr

# ── VOLATILITY ───────────────────────────────────────────────────────────────
VOL_52W_LOW      = 114.25
VOL_52W_HIGH     = 1255.00
VOL_ANNUAL_PCT   = 0.55    # very high vol; cyclical semiconductor at a cycle extreme
VOL_BETA         = 1.75
VOL_DIVIDEND     = 0.46
VOL_1DAY_PCT     = (CURRENT_PRICE - PREV_CLOSE) / PREV_CLOSE * 100
VOL_1WK_PCT      = (CURRENT_PRICE - PRICE_1WK_AGO) / PRICE_1WK_AGO * 100

# ── ANALYST TARGETS (consensus context) ──────────────────────────────────
ANALYST_AVG_TARGET   = 1502.0   # ~46 analysts, Strong Buy consensus
ANALYST_LOW_TARGET   = 361.0
ANALYST_HIGH_TARGET  = 2200.0
ANALYST_NOTE = "New Street's Ferragu upgraded to Buy (from Neutral) with a $1,250 target on Aug 20, arguing AI demand is breaking the old memory boom-bust framework; Goldman Sachs remains the bearish outlier at Neutral/$900, flagging a possible FY2027 cyclical peak — sentiment still net-bullish despite the Apple/CXMT-sourcing and Samsung-payout headlines"

# ── SCORING ───────────────────────────────────────────────────────────────
def score_signal(val, base_f, bull_f, xbull_f, hib):
    if hib:
        if val >= xbull_f: return 4
        if val >= bull_f:  return 3
        if val >= base_f:  return 2
        return 1
    else:
        if val <= xbull_f: return 4
        if val <= bull_f:  return 3
        if val <= base_f:  return 2
        return 1

ICONS = {4: "★ XBULL", 3: "▲ BULL", 2: "◦ BASE", 1: "⚠ BEAR"}

def softmax_probs(composite, T=0.60):
    centres = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    raw = {k: math.exp(-abs(composite - c) / T) for k, c in centres.items()}
    tot = sum(raw.values())
    return {k: v / tot for k, v in raw.items()}

def expected_price(probs):
    return sum(probs[k] * SCENARIOS[k][2] for k in probs)

def market_implied_composite(target_ev):
    best = None
    for x in range(100, 401):
        c = x / 100
        ev = expected_price(softmax_probs(c))
        if best is None or abs(ev - target_ev) < abs(best[1] - target_ev):
            best = (c, ev)
    return best

# ── COMPUTE ───────────────────────────────────────────────────────────────────
W = 72

scored = [
    (name, unit, bv, bf, blf, xf, cv, hib, narr,
     score_signal(cv, bf, blf, xf, hib), w)
    for (name, unit, bv, bf, blf, xf, cv, hib, narr), w
    in zip(SIGNALS, WEIGHTS)
]
proxy_composite  = sum(s * w for *_, s, w in scored)
sca              = sum(s * w for _, s, w in STRUCTURAL_FACTORS)
adj_composite    = proxy_composite + sca
proxy_probs      = softmax_probs(proxy_composite)
adj_probs        = softmax_probs(adj_composite)
proxy_ev         = expected_price(proxy_probs)
adj_ev           = expected_price(adj_probs)

market_target_ev = CURRENT_PRICE * ((1 + REQUIRED_RETURN) ** HORIZON_YEARS)
mkt_composite, mkt_ev = market_implied_composite(market_target_ev)
mkt_probs = softmax_probs(mkt_composite)

# Updated EPP
epp_updated     = EPP_TODAY_EPS * EPP_MIN_PE
epp_gap_pct     = (CURRENT_PRICE - epp_updated) / epp_updated * 100
bear_vs_epp_pct = (SCENARIOS["BEAR"][2] - epp_updated) / epp_updated * 100

# Conservative growth
cons_price_2yr  = CONS_EPS_2028 * CONS_EXIT_PE
cons_total_ret  = (cons_price_2yr - CURRENT_PRICE + CONS_DIVIDEND_2YR) / CURRENT_PRICE * 100
cons_annual_ret = cons_total_ret / 2

# Volatility
sigma_1yr         = CURRENT_PRICE * VOL_ANNUAL_PCT
vol_low_1yr       = CURRENT_PRICE - sigma_1yr
vol_high_1yr      = CURRENT_PRICE + sigma_1yr
sigma_needed_bear = (CURRENT_PRICE - SCENARIOS["BEAR"][2]) / sigma_1yr
pct_of_52w_range  = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW) * 100

# Downside / upside / ratio B
downside_pct = (CURRENT_PRICE - SCENARIOS["BEAR"][2]) / CURRENT_PRICE * 100
upside_pct   = (SCENARIOS["BULL"][2] - CURRENT_PRICE) / CURRENT_PRICE * 100
ratio_b      = downside_pct / upside_pct

fwd_pe = CURRENT_PRICE / FY2026E_EPS


# ── EPP-DISTANCE ADJUSTMENT (methodology v2) ─────────────────────────────────
# Distance above the panic floor = drawdown room. LOWER IS BETTER; below floor
# is the deep-value zone. Far above the floor penalizes the composite.
if   epp_gap_pct <=   0: epp_adj =  0.20   # below panic floor — deep value
elif epp_gap_pct <=  40: epp_adj =  0.00   # moderate distance — neutral
elif epp_gap_pct <= 100: epp_adj = -0.10
elif epp_gap_pct <= 200: epp_adj = -0.20
else:                    epp_adj = -0.30   # far above floor — large drawdown room
adj_composite = adj_composite + epp_adj
epp_label = ("\u2713 BELOW panic floor \u2014 deep-value zone" if epp_gap_pct <= 0
             else "moderate distance to floor" if epp_gap_pct <= 40
             else "\u26a0 far above floor \u2014 large drawdown room")

adj_gap = adj_composite - mkt_composite
if   adj_gap >  0.50: _verdict = "UNDERVALUED"
elif adj_gap >  0.20: _verdict = "MODESTLY UNDERVALUED"
elif adj_gap > -0.20: _verdict = "FAIRLY VALUED"
elif adj_gap > -0.50: _verdict = "MODESTLY OVERVALUED"
else:                 _verdict = "OVERVALUED"

if   ratio_b >= 1.5:                    _signal = "✕ AVOID"
elif adj_gap > 0.20 and ratio_b < 1.35: _signal = "◎ ACCUMULATE"
elif adj_gap > -0.20:                   _signal = "◐ WATCHLIST"
else:                                   _signal = "✕ AVOID"

total_now_b, total_bear_b, total_bull_b, eps_check_now = segment_bridge()

# ── OUTPUT ────────────────────────────────────────────────────────────────────
print()
print("═" * W)
print(f"  MU  ·  Micron Technology, Inc.  ·  ${CURRENT_PRICE:.2f}  ·  DRAM / NAND / HBM AI Supercycle")
print(f"  Signal: {_signal}   Ratio B: {ratio_b:.2f}x   Adj gap: {adj_gap:+.2f}  [{_verdict}]")
print("═" * W)

# ── SEGMENT REVENUE BRIDGE ───────────────────────────────────────────────────
print(f"\n  SEGMENT REVENUE BRIDGE  (FY2026E  →  BEAR / BULL scenarios)")
print("  " + "─" * (W-2))
print(f"  {'Segment':<24}  {'FY2026E ($B)':>13}  {'Bear ($B)':>10}  {'Bull ($B)':>10}    Δ Bear    Δ Bull")
print("  " + "─" * (W-2))
print(f"  DRAM                    $  {FY2026E_DRAM_B:>9.1f}  $  {BEAR_DRAM_B:>7.1f}  $  {BULL_DRAM_B:>7.1f}    "
      f"{BEAR_DRAM_B-FY2026E_DRAM_B:+.1f}    {BULL_DRAM_B-FY2026E_DRAM_B:+.1f}")
print(f"    Record pricing on AI/HBM demand; CXMT's ramp is the swing factor for the 2-yr bear case")
print(f"  NAND                    $  {FY2026E_NAND_B:>9.1f}  $  {BEAR_NAND_B:>7.1f}  $  {BULL_NAND_B:>7.1f}    "
      f"{BEAR_NAND_B-FY2026E_NAND_B:+.1f}    {BULL_NAND_B-FY2026E_NAND_B:+.1f}")
print(f"    Smaller, steadier segment; less exposed to the DRAM-specific CXMT competitive threat")
print("  " + "─" * (W-2))
print(f"  TOTAL                   $  {total_now_b:>9.1f}  $  {total_bear_b:>7.1f}  $  {total_bull_b:>7.1f}    "
      f"{total_bear_b-total_now_b:+.1f}    {total_bull_b-total_now_b:+.1f}")
print(f"  Q1 ${Q1_REV_B:.2f}B → Q2 ${Q2_REV_B:.2f}B → Q3 ${Q3_REV_B_ACTUAL:.1f}B (actual) → "
      f"Q4 ${Q4_GUIDE_B:.1f}B±$1.0B (guide, beat Street by ${Q4_GUIDE_BEAT_B:.2f}B)")
print(f"\n  FY2026E EPS check:  ${total_now_b:.1f}B rev × {FY2026E_GM_PCT*100:.1f}% GM − $6.5B opex")
print(f"  − 15.0% tax  ÷ {FY2026E_SHARES_B:.3f}B shares  =  ${eps_check_now:.2f}/share  (model estimate ${FY2026E_EPS:.2f})")

# ── ① SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print(f"\n  ① SIGNAL DASHBOARD")
print(f"  {'Signal':<30}  {'BEAR':>7}  {'BASE≥':>7}  {'BULL≥':>7}  {'XBULL≥':>7}  {'NOW':>7}  Score")
print("  " + "─" * (W-2))
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    bar = "█" * s + "░" * (4 - s)
    if name in QUAL_LABELS:
        lb, lba, lbu, lx, lc = QUAL_LABELS[name]
        print(f"  {name:<30}  {lb:>13}  {lba:>9}  {lbu:>9}  {lx:>9}  {lc:>18}  {ICONS[s]}  {bar}")
    else:
        print(f"  {name:<30}  {bv:>6.1f}{unit[:1]}  {bf:>6.0f}{unit[:1]}  {blf:>6.0f}{unit[:1]}  "
              f"{xf:>6.0f}{unit[:1]}  {cv:>6.1f}{unit[:1]}  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:    {proxy_composite:.2f} / 4.00")
print(f"  Market composite:   {mkt_composite:.2f} / 4.00  "
      f"(back-solved from ${CURRENT_PRICE:.2f} + {REQUIRED_RETURN*100:.0f}%/yr hurdle)")
print(f"  SCA adjustment:    {sca:+.3f}  →  Adj composite {adj_composite:.3f}  "
      f"→  Gap {adj_gap:+.2f}  [{_verdict}]")

print(f"\n  Structural factors:")
for desc, score, wt in STRUCTURAL_FACTORS:
    arrow = "  +" if score > 0 else "  -"
    print(f"  {arrow}  {desc}  ({score:+.1f} × {wt*100:.0f}%  =  {score*wt:+.3f})")

# ── ② BEAR CASE ANATOMY ──────────────────────────────────────────────────────
print(f"\n  ② BEAR CASE ANATOMY  (variables needed to reach BEAR ${SCENARIOS['BEAR'][2]})")
print("  " + "─" * (W-2))
print(f"  {'Signal':<30}  {'Current':>10}  {'Bear val':>10}  Trigger")
for name, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    trigger = narr[:42] if len(narr) <= 42 else narr[:39] + "…"
    if name in QUAL_LABELS:
        lb, lba, lbu, lx, lc = QUAL_LABELS[name]
        print(f"  {name:<30}  {lc:>9}  {lb:>9}  {trigger}")
    else:
        print(f"  {name:<30}  {cv:>9.1f}{unit[:1]}  {bv:>9.1f}{unit[:1]}  {trigger}")

print(f"\n  Bear probability (proxy model):  {proxy_probs['BEAR']*100:.1f}%")
print(f"\n  KEY TRIGGER: memory is the most cyclical major semiconductor category, and Micron's own")
print(f"  history includes multiple 50-80% peak-to-trough drawdowns. CXMT is the specific, funded,")
print(f"  fast-moving catalyst that could turn this AI-driven supercycle into a conventional memory")
print(f"  down-cycle faster than the HBM TAM buildout can offset it. {CXMT_2ND_FAB_NOTE}.")

# ── CXMT COMPETITIVE THREAT CHECK ────────────────────────────────────────────
print(f"\n  CXMT COMPETITIVE THREAT CHECK  (the Micron-specific risk)")
print("  " + "─" * (W-2))
print(f"  CXMT wafer starts/month (2026E):     {CXMT_WSPM_2026E:,}  vs Micron's ~{MU_WSPM_APPROX:,}  "
      f"(within ~{(MU_WSPM_APPROX-CXMT_WSPM_2026E)/1000:.0f}K of parity)")
print(f"  CXMT Shanghai IPO:                    ${CXMT_IPO_RAISE_B:.1f}B raised, +{CXMT_IPO_POP_PCT}% first-day pop")
print(f"  Micron market cap erased on the news:  ${MU_MCAP_ERASED_B:.1f}B")
print(f"  CXMT Q1 2026 global DRAM revenue share: {CXMT_Q1_DRAM_SHARE_PCT:.0f}%  vs Micron {MU_Q1_DRAM_SHARE_PCT:.0f}%")
print(f"  HBM TAM (structural counterweight):    ${HBM_TAM_2025_B}B (2025) → ${HBM_TAM_2028E_B}B+ (2027-28E)")
print(f"  New this week: {CXMT_2ND_FAB_NOTE}.")

# ── ③ UPDATED EPP ────────────────────────────────────────────────────────────
print(f"\n  ③ EPP  (Earnings Power Price: pessimistic P/E × forward EPS)")
print("  " + "─" * (W-2))
print(f"  FY2026E EPS estimate:       ${EPP_TODAY_EPS:.2f}  (Q1 $4.78 + Q2 $12.20 + Q3 $25.11 + Q4E $31.00 non-GAAP)")
print(f"  Pessimistic P/E at trough:   {EPP_MIN_PE:.0f}x  {EPP_REGIME_NOTE}")
print(f"  {'─'*60}")
print(f"  EPP floor:    ${epp_updated:.0f}/share")
print(f"  Current ${CURRENT_PRICE:.2f} vs EPP ${epp_updated:.0f}:  {epp_gap_pct:+.1f}%")
print(f"  At a 15x reversion (a normalized cyclical multiple): ${EPP_TODAY_EPS:.2f} × 15 = "
      f"${EPP_TODAY_EPS*15:.0f}  ({(EPP_TODAY_EPS*15/CURRENT_PRICE-1)*100:+.0f}% from spot)")

# ── ④ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print(f"\n  ④ CONSERVATIVE GROWTH  (2-yr: modest growth off the FY2026E base, cycle risk discounted)")
print("  " + "─" * (W-2))
print(f"  Conservative FY2028E EPS:  ${CONS_EPS_2028:.2f}  (below FY2026E — assumes the cycle has partially rolled over)")
print(f"  Conservative exit P/E:      {CONS_EXIT_PE:.0f}x  (~{fwd_pe:.0f}x → {CONS_EXIT_PE:.0f}x; a further de-rating)")
print(f"  Conservative equity value:   ${cons_price_2yr:.2f}/share")
print(f"  + Cumulative dividends (2yr): +${CONS_DIVIDEND_2YR:.2f}/share  (${VOL_DIVIDEND:.2f}/yr, "
      f"{VOL_DIVIDEND/CURRENT_PRICE*100:.2f}% yield)")
print(f"  {'─'*60}")
print(f"  Conservative 2yr total:      ${cons_price_2yr + CONS_DIVIDEND_2YR:.2f}  "
      f"({'▲' if cons_total_ret >= 0 else '▼'}{abs(cons_price_2yr + CONS_DIVIDEND_2YR - CURRENT_PRICE):.2f} from ${CURRENT_PRICE:.2f})")
print(f"  Conservative total return:   {cons_total_ret:+.1f}% over 2yr  =  {cons_annual_ret:+.1f}%/yr")
print(f"\n  THE HONEST READ: at ${PRICE_1WK_AGO:.0f} a week ago — near the stock's all-time high — the conservative")
print(f"  case was solidly negative; this week's pullback to ${CURRENT_PRICE:.2f} has narrowed that gap but the")
print(f"  case still doesn't clear its cost of capital. The real risk isn't a modest EPS decline — it's")
print(f"  the full-cycle-reversal BEAR case, where CXMT-driven oversupply pushes margins toward the 30s.")

# ── ⑤ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        ${VOL_52W_LOW:.2f}  –  ${VOL_52W_HIGH:.2f}  "
      f"(stock at {pct_of_52w_range:.0f}th pct of 52W range)")
print(f"  Recent moves:          {VOL_1DAY_PCT:+.1f}% (1-day) / {VOL_1WK_PCT:+.1f}% (1-week, pulling back from last week's "
      f"near-all-time-high run on the Samsung-payout and Apple/CXMT-sourcing headlines)")
print(f"  Annual dividend:      ${VOL_DIVIDEND:.2f}/share  (yield {VOL_DIVIDEND/CURRENT_PRICE*100:.2f}%; "
      f"a small, recently reinstated payout)")
print(f"  Realized vol (1yr):   {VOL_ANNUAL_PCT*100:.0f}%  (high — typical for cyclical memory semis, "
      f"especially at a cycle extreme)")
print(f"  Beta vs S&P 500:      {VOL_BETA:.2f}  (well above market; among the most volatile large-cap semis)")
print(f"  1-sigma range (1yr):  ${vol_low_1yr:.0f}  –  ${vol_high_1yr:.0f}  (${CURRENT_PRICE:.2f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  {'─'*60}")
print(f"  Bear ${SCENARIOS['BEAR'][2]} requires:  ~{sigma_needed_bear:.1f}σ drawdown  "
      f"(large but well within Micron's own historical cycle-crash range)")
print(f"  Analyst consensus: avg target ${ANALYST_AVG_TARGET:.0f} (Strong Buy, ~46 analysts), "
      f"range ${ANALYST_LOW_TARGET:.0f}-${ANALYST_HIGH_TARGET:.0f}. {ANALYST_NOTE}.")
print(f"  → Q4 FY2026 print (Sept 29, after the close) is the next test of whether pricing power holds through the CXMT headlines.")
print(f"  → CXMT capacity ramp and Chinese DRAM ASPs are the leading indicators to watch between prints.")

# ── ⑥ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print(f"\n  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
print("  " + "─" * (W-2))
print(f"  {'Scenario':<8}  {'Price':>6}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>7}  Description")
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    eps, mult, price, narr = SCENARIOS[k]
    pp, mp = proxy_probs[k], mkt_probs[k]
    print(f"  {k:<8}  ${price:>5}  {pp*100:>6.1f}%  {mp*100:>7.1f}%  {(pp-mp)*100:>+6.1f}pp  {narr}")

print(f"\n  Adj EV (2yr): ${adj_ev:.0f}  /  Proxy EV: ${proxy_ev:.0f}  /  Market EV: ${mkt_ev:.0f}  "
      f"/  Current: ${CURRENT_PRICE:.0f}")
print(f"  Downside  (→ Bear ${SCENARIOS['BEAR'][2]}):  {downside_pct:.1f}%")
print(f"  Upside    (→ Bull ${SCENARIOS['BULL'][2]}):  {upside_pct:.1f}%")
print(f"  Ratio B   :  {ratio_b:.2f}x")
print(f"  Signal    :  {_signal}")
print(f"\n  MARKET PRICING: at ${CURRENT_PRICE:.2f} the market composite is {mkt_composite:.2f}/4.0. The model's")
print(f"  adjusted composite is {adj_composite:.2f}/4.0, for a gap of {adj_gap:+.2f} — {_verdict.lower()}.")
print(f"  Micron is delivering the strongest growth and margin expansion in its history, and the market")
print(f"  is still pricing it at a cyclical discount ({fwd_pe:.1f}x forward) rather than a growth-stock multiple.")
print(f"  CXMT is a real, quantified risk to the 2-year horizon, but the HBM TAM buildout is the larger force.")

print()
print("═" * W)
print()
