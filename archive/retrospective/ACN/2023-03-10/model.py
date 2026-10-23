#!/usr/bin/env python3
"""
ACN Signal Model  ·  RETROSPECTIVE as of 2023-03-10  (pre-Q2 print)  (methodology v2)
──────────────────────────────────────────────────────────────────────
Accenture plc (NYSE: ACN)  ·  IT Services & Consulting — Strategy & Consulting, Technology, Operations
Point-in-time: every input was public on AS_OF (see SOURCES); retro/retro_tool.py enforces it.
Trough year: none — FY2023 is a deceleration year, not an earnings trough (EPP on the FY2023E guide)

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness

Valuation anchors are mechanical, not hand-picked: scenario P/Es are percentiles of
ACN's own P/E on current-fiscal-year EPS over the 10 years to AS_OF, and the EPP P/E is
the median of the five panic troughs in that window.
"""
import math

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "ACN"
COMPANY     = "Accenture plc"
AS_OF       = "2023-03-10"
PRICE_DATE  = "2023-03-10"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; scenario P/E = percentiles of "
               "ACN's own 10-yr P/E on current-FY EPS; EPP P/E = median panic trough")

SOURCES = [
    {"id": "S1", "published": "2022-09-22", "title": "Accenture Q4/FY22 results (8-K ex.99)",
     "url": "https://www.sec.gov/Archives/edgar/data/1467373/000146737322000283/fy22q4plc8-kexhibit.htm",
     "supports": "FY22 revenue by industry group, record $71.7B bookings, Q4 consulting +22% LC, FY21 adjusted EPS $8.80, dividend $1.12 (+15%)"},
    {"id": "S2", "published": "2022-10-12", "title": "SEC XBRL company facts, 10-K filings 2010-10-26 .. 2022-10-12",
     "url": "https://data.sec.gov/api/xbrl/companyfacts/CIK0001467373.json",
     "supports": "GAAP diluted EPS FY2012-FY2022 for the P/E history; only facts filed on or before 2022-10-12 used"},
    {"id": "S3", "published": "2022-12-16", "title": "Accenture Q1 FY23 results (8-K ex.99)",
     "url": "https://www.sec.gov/Archives/edgar/data/1467373/000146737322000369/fy23q1earnings8-kexhibit.htm",
     "supports": "Q1 revenue $15.7B (+15% LC), consulting +10% LC, managed services +20% LC, bookings $16.2B (+6% LC), industry groups, cash $5.9B, FY23 and Q2 guidance"},
    {"id": "S9", "published": "2023-02-10", "title": "Reuters via Business Standard: ChatGPT, other AI models to disrupt Indian IT firms (J.P.Morgan)",
     "url": "https://www.business-standard.com/article/companies/chatgpt-other-ai-models-to-disrupt-indian-it-firms-jp-morgan-analyst-123021000976_1.html",
     "supports": "GenAI a near-term deflation driver for legacy IT services; Accenture/Deloitte gain share"},
    {"id": "S12", "published": "2023-03-10", "title": "Yahoo Finance daily prices, ACN and S&P 500, truncated at AS_OF",
     "url": "https://finance.yahoo.com/quote/ACN/history",
     "supports": "close $252.95, 52-week range, realized vol, beta, the 10-yr P/E distribution"},
]

# Durability as it should have been judged ON AS_OF — not today's AI_EXPOSED profile.
PIT_PROFILE = {
    "kind": "DURABLE",
    "risk": 2,
    "why": ("Accenture: #1-scale IT-services and consulting franchise that took share through the cloud "
            "cycle; discretionary consulting demand is cyclical, the franchise is not"),
    "theme_watch": [{
        "theme": "GENAI",
        "status": "live, priced as a tailwind",
        "reason": ("Live since 2022-11-30, but the "
                   "sell-side read for ACN was share gain (J.P.Morgan, 2023-02-10) and the stock trades at "
                   "22.3x FY23E — near its own median, not an AI discount. Re-file under AI_EXPOSED only when the "
                   "multiple starts discounting deflation or GenAI shows up as shrinking billable hours."),
    }],
    "evidence": ["S9"],
}

# ── CONFIG ────────────────────────────────────────────────────────────────────
CURRENT_PRICE    = 252.95   # USD, NYSE close 2023-03-10
REQUIRED_RETURN  = 0.15
HORIZON_YEARS    = 2
SHARES_DIL_B     = 0.6388   # Q1 FY23 diluted weighted average (638.8M)

# ACN P/E on current-fiscal-year EPS, the 10 years to 2023-03-10 (S2, S12).
# EPS normalized for one-offs: FY13 = mean(FY12, FY14), FY16/FY17 averaged, FY21 = $8.80 adjusted,
# FY23 = guide midpoint. Panic troughs on the same basis:
PE_PCTL = {"p5": 16.9, "p10": 17.5, "p25": 19.0, "median": 21.9, "p75": 26.0, "p90": 30.2, "max": 38.8}
PANIC_TROUGHS = [("2014-10-15", 15.9), ("2016-02-09", 15.7), ("2018-12-24", 18.2),
                 ("2020-03-23", 18.2), ("2022-10-12", 22.0)]

# 2-year horizon: EPS = FY2025E, P/E = the percentile band each scenario stands for
# FY23E guide midpoint grown 2 years: BEAR ~1%/yr (flat revenue, margin -40bp, buyback); BASE ~6.4%/yr
# (mid-single-digit LC growth by H2, as +8-11% FY after +15% in Q1 implies, 10-20bp margin, buyback); BULL ~11%/yr
# (the FY12-FY22 EPS CAGR, 10.8%); XBULL ~15%/yr (near the FY20-FY22 pace, 16.5%)
SCENARIO_CAGR = {"BEAR": 0.010, "BASE": 0.064, "BULL": 0.112, "XBULL": 0.153}
SCENARIO_EPS  = {k: round(11.36 * (1 + g) ** 2, 2) for k, g in SCENARIO_CAGR.items()}
SCENARIO_PE  = {"BEAR": PE_PCTL["p10"], "BASE": PE_PCTL["median"], "BULL": PE_PCTL["p75"], "XBULL": PE_PCTL["p90"]}
SCENARIO_TXT = {
    "BEAR":  "Consulting recession spreads to managed services; pricing concessions; P/E to its 10th pct",
    "BASE":  "Mid-single-digit LC growth, 10-20bp/yr margin, buyback; P/E reverts to its 10-yr median",
    "BULL":  "GenAI becomes a cloud-sized services cycle; growth back to 8-10% LC; P/E holds 75th pct",
    "XBULL": "Re-run of the FY21-22 boom: double-digit growth and a 30x multiple",
}

# ── SEGMENT REVENUE BRIDGE (FY2023E → FY2025E bear / bull, USD bn) ─────────────
# FY2023E = FY22 $61.59B x (1 + 9.5% LC - 5% FX), the December guide midpoints (S1, S3); split by
# industry group pro rata to Q1 actuals (S3); bear/bull carry the same per-group 2-yr factors.
SEGMENTS = [
    ("Products",                "Consumer/industrial/retail/auto; largest, +15% LC in Q1",    19.0, 18.8, 22.3),
    ("Health & Public Service", "Public service + health; +15% LC in Q1",                     12.3, 12.8, 14.4),
    ("Financial Services",      "Banking/insurance/capital markets; +13% LC in Q1",           12.1, 11.9, 13.9),
    ("Comms, Media & Tech",     "Tech/telco clients; slowing to +11% LC in Q1 (FY22 +28%)",   12.2, 11.5, 14.3),
    ("Resources",               "Energy/utilities/chemicals; +21% LC in Q1",                   8.7,  8.8, 10.3),
]
OP_MARGIN = {"FY23E": 0.154, "BEAR": 0.150, "BULL": 0.160}   # FY23 operating-margin guide 15.3-15.5% (S3)
TAX_RATE  = 0.245                                             # adjusted ETR guide 23.5-24.5% + minority
SHARES_FY25_B = 0.632                                         # net buyback ~0.5%/yr (FY18-FY22 trend)

# ── SIGNALS ───────────────────────────────────────────────────────────────────
SIGNALS = [
    ("New bookings growth (LC)", "% YoY",
      -5.0, 0.0, 8.0, 15.0, 6.0, True,
     "Clients defer transformation programs; bookings fall below revenue"),

    ("Consulting revenue growth (LC)", "% YoY",
      -6.0, 2.0, 7.0, 12.0, 10.0, True,
     "Discretionary consulting turns negative"),

    ("Managed services growth (LC)", "% YoY",
      3.0, 5.0, 10.0, 15.0, 20.0, True,
     "Outsourcing renewals repriced lower by automation"),

    ("Total revenue growth (LC)", "% YoY",
      0.0, 3.0, 7.0, 11.0, 15.0, True,
     "Q2 lands at the bottom of the 6-10% guide and keeps slowing"),

    ("Adj. operating margin change", "bp YoY",
      -40.0, 0.0, 20.0, 50.0, 20.0, True,
     "Pricing concessions + bench costs reverse the expansion"),

    ("GenAI: demand vs deflation", "/4",
      1.0, 2.0, 3.0, 4.0, 2.0, True,
     "Coding/testing hours shrink faster than advisory grows"),
]
WEIGHTS = [0.20, 0.20, 0.15, 0.15, 0.15, 0.15]

PE_NOW_PCTL     = 52    # share of the window's daily P/Es at or below today's (S2, S12)
VALUATION_SCORE = round(max(-0.5, min(0.5, -(PE_NOW_PCTL - 50) / 60)), 2)   # >=80th pct -0.5, median 0, <=20th +0.5
STRUCTURAL_FACTORS = [
    ("Share-gainer at scale: FY22 revenue +26% LC, record $71.7B bookings; Q1 revenue +15% LC", 0.4, 0.20),
    ("Multiple: 22.3x FY23E vs a 21.9x 10-yr median (52nd percentile of its own range)", VALUATION_SCORE, 0.25),
    ("Deceleration already guided: Q2 +6-10% LC after +15% in Q1; consulting +10% LC (from +22% in Q4 FY22)", -0.3, 0.20),
    ("Cash $5.9B, FCF guide $7.7-8.2B, >=$7.1B returned to shareholders",                               0.3, 0.15),
    ("GenAI as a services opportunity: J.P.Morgan expects global consultancies to gain share first",  0.2, 0.10),
    ("GenAI as a deflation driver for legacy delivery hours (J.P.Morgan) — not yet in the numbers",  -0.2, 0.10),
]

# ── UPDATED EPP ───────────────────────────────────────────────────────────────
EPP_TODAY_EPS = 11.36    # FY2023E EPS, December guide $11.20-11.52 (S3); FY ends Aug-31
EPP_MIN_PE    = 18.0     # median panic trough 18.2x (2014-2023), rounded down per house style

# ── CONSERVATIVE GROWTH (2-yr, base-minus) ───────────────────────────────────
# (signal_index, conservative_value, rationale)
CONS_SIGNALS = [
    (0, 0.0,  "Bookings flat (vs +6% LC)"),
    (1, 0.0,  "Consulting flat (vs +10% LC)"),
    (2, 7.0,  "Managed services +7% (vs +20%)"),
    (3, 3.0,  "Revenue +3% LC (bottom of base)"),
    (4, 0.0,  "Margin flat (vs +20bp)"),
    (5, 2.0,  "Score 2/4 (debate unresolved)"),
]
CONS_EPS_CAGR = 0.05
CONS_EXIT_PE  = 22.0     # just under the 21.9x 10-yr median: the premium is not assumed to persist
CONS_DIVIDEND = 4.48     # $1.12/quarter (S1)

# ── VOLATILITY ────────────────────────────────────────────────────────────────
VOL_ANNUAL_PCT = 0.318   # 1-yr realized, daily log returns to AS_OF (S12)
VOL_BETA       = 1.21    # 1-yr beta vs S&P 500 (S12)
VOL_52W_LOW    = 242.95
VOL_52W_HIGH   = 345.30
VOL_DIVIDEND   = 4.48
REF_LOW        = 250.07  # 2022-10-12 close, the latest bear-market low (S12)

# ── SCORING ───────────────────────────────────────────────────────────────────
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

def expected_price(probs, scenarios):
    return sum(probs[k] * scenarios[k][2] for k in probs)

def market_implied_composite(target_ev, scenarios):
    best_c, best_probs, best_diff = None, None, None
    for c in [x / 100 for x in range(100, 401)]:
        probs = softmax_probs(c)
        diff = abs(expected_price(probs, scenarios) - target_ev)
        if best_diff is None or diff < best_diff:
            best_c, best_probs, best_diff = c, probs, diff
    return best_c, best_probs

def build_scenarios(eps_mult=1.0, pe=None):
    pe = pe or SCENARIO_PE
    return {k: (round(SCENARIO_EPS[k] * eps_mult, 2), pe[k], int(round(SCENARIO_EPS[k] * eps_mult * pe[k])), SCENARIO_TXT[k])
            for k in SCENARIO_EPS}

def legacy_tier(rb):
    if rb < 0.75: return "BUY", "◉ BUY"
    if rb < 1.10: return "ACCUMULATE", "◎ ACCUMULATE"
    if rb < 1.75: return "WATCHLIST", "◐ WATCHLIST"
    return "AVOID", "✕ AVOID"

def verdict_of(gap):
    if   gap >  0.50: return "UNDERVALUED"
    elif gap >  0.20: return "MODESTLY UNDERVALUED"
    elif gap > -0.20: return "FAIRLY VALUED"
    elif gap > -0.50: return "MODESTLY OVERVALUED"
    return "OVERVALUED"

def epp_adjustment(gap_pct):
    # ── EPP-DISTANCE ADJUSTMENT (methodology v2) ──────────────────────────────
    # Distance above the panic floor = drawdown room. LOWER IS BETTER; below floor
    # is the deep-value zone. Far above the floor penalizes the composite.
    if   gap_pct <=   0: return  0.20   # below panic floor — deep value
    elif gap_pct <=  40: return  0.00   # moderate distance — neutral
    elif gap_pct <= 100: return -0.10
    elif gap_pct <= 200: return -0.20
    return -0.30                        # far above floor — large drawdown room

def evaluate(scenarios, sca_shift=0.0, epp_pe=EPP_MIN_PE, hurdle=REQUIRED_RETURN):
    """Ratio B, adj gap and verdict for one set of assumptions (main case + robustness)."""
    proxy = sum(score_signal(cv, bf, blf, xf, hib) * w
                for (_, _, _, bf, blf, xf, cv, hib, _), w in zip(SIGNALS, WEIGHTS))
    sca = sum(s * w for _, s, w in STRUCTURAL_FACTORS) + sca_shift
    epp = EPP_TODAY_EPS * epp_pe
    gap_pct = (CURRENT_PRICE - epp) / epp * 100
    e_adj = epp_adjustment(gap_pct)
    adj = proxy + sca + e_adj
    mkt, _ = market_implied_composite(CURRENT_PRICE * (1 + hurdle) ** HORIZON_YEARS, scenarios)
    bear, bull = scenarios["BEAR"][2], scenarios["BULL"][2]
    down, up = (CURRENT_PRICE - bear) / CURRENT_PRICE, (bull - CURRENT_PRICE) / CURRENT_PRICE
    rb = round(down / up, 2) if up > 0 else float("inf")
    return {"proxy": proxy, "sca": sca, "epp": epp, "epp_gap_pct": gap_pct, "epp_adj": e_adj,
            "adj": adj, "mkt": mkt, "gap": round(adj - mkt, 2), "verdict": verdict_of(adj - mkt),
            "rb": rb, "down": down, "up": up}

# ── COMPUTE ───────────────────────────────────────────────────────────────────
W = 72
CUR = "$"

SCENARIOS = build_scenarios()
scored = [
    (name, unit, bv, bf, blf, xf, cv, hib, narr,
     score_signal(cv, bf, blf, xf, hib), w)
    for (name, unit, bv, bf, blf, xf, cv, hib, narr), w
    in zip(SIGNALS, WEIGHTS)
]
ev = evaluate(SCENARIOS)
proxy_composite  = ev["proxy"]
bear_composite   = sum(score_signal(bv, bf, blf, xf, hib) * w
                       for (_, __, bv, bf, blf, xf, ___, hib, ____), w
                       in zip(SIGNALS, WEIGHTS))
sca              = ev["sca"]
proxy_probs      = softmax_probs(proxy_composite)
bear_probs       = softmax_probs(bear_composite)
proxy_ev         = expected_price(proxy_probs, SCENARIOS)

market_target_ev = CURRENT_PRICE * ((1 + REQUIRED_RETURN) ** HORIZON_YEARS)
mkt_composite, mkt_probs = market_implied_composite(market_target_ev, SCENARIOS)
mkt_ev = expected_price(mkt_probs, SCENARIOS)

epp_updated     = ev["epp"]
epp_gap_pct     = ev["epp_gap_pct"]
bear_vs_epp_pct = (SCENARIOS["BEAR"][2] - epp_updated) / epp_updated * 100

cons_eps_2yr    = EPP_TODAY_EPS * ((1 + CONS_EPS_CAGR) ** 2)
cons_price_2yr  = cons_eps_2yr * CONS_EXIT_PE
cons_div_2yr    = CONS_DIVIDEND * 2.06
cons_total_ret  = (cons_price_2yr - CURRENT_PRICE + cons_div_2yr) / CURRENT_PRICE * 100
cons_annual_ret = cons_total_ret / 2

sigma_1yr         = CURRENT_PRICE * VOL_ANNUAL_PCT
sigma_needed_bear = (CURRENT_PRICE - SCENARIOS["BEAR"][2]) / sigma_1yr

epp_adj = ev["epp_adj"]
adj_composite = ev["adj"]
epp_label = ("✓ BELOW panic floor — deep-value zone" if epp_gap_pct <= 0
             else "moderate distance to floor" if epp_gap_pct <= 40
             else "⚠ far above floor — large drawdown room")

adj_gap  = ev["gap"]
_verdict = ev["verdict"]
ratio_b  = ev["rb"]
signal_short, signal_full = legacy_tier(ratio_b)

# ── OUTPUT ────────────────────────────────────────────────────────────────────
print()
print("═" * W)
print(f"  ACN  ·  Accenture plc  ·  {CUR}{CURRENT_PRICE:,.2f}  ·  RETROSPECTIVE as of {AS_OF}")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b:.2f}x   Adj gap: {adj_gap:+.2f}  [{_verdict}]")
print(f"  Point-in-time: {len(SOURCES)} sources, latest published {max(s['published'] for s in SOURCES)}")
print("═" * W)

print(f"\n  SEGMENT REVENUE BRIDGE  (FY2023E revenue, USD bn  →  FY2025E BEAR / BULL)")
print("  " + "─" * (W-2))
print(f"  {'Industry group':<24}  {'FY2023E':>10}  {'Bear':>8}  {'Bull':>8}    Δ Bear    Δ Bull")
print("  " + "─" * (W-2))
tot_now = tot_bear = tot_bull = 0.0
for seg_name, seg_desc, s_now, s_bear, s_bull in SEGMENTS:
    tot_now += s_now; tot_bear += s_bear; tot_bull += s_bull
    print(f"  {seg_name:<24}  {CUR}{s_now:>8.1f}  {CUR}{s_bear:>6.1f}  {CUR}{s_bull:>6.1f}    "
          f"{s_bear-s_now:>+6.1f}    {s_bull-s_now:>+6.1f}")
    print(f"    {seg_desc}")
print("  " + "─" * (W-2))
print(f"  {'TOTAL':<24}  {CUR}{tot_now:>8.1f}  {CUR}{tot_bear:>6.1f}  {CUR}{tot_bull:>6.1f}    "
      f"{tot_bear-tot_now:>+6.1f}    {tot_bull-tot_now:>+6.1f}")
print(f"  Q1 FY23 (Dec 16): revenue $15.7B +15% LC; consulting +10% LC, managed services +20% LC; bookings $16.2B +6% LC;")
print(f"  op margin 16.5% (+20bp); FY23 guide +8-11% LC, EPS $11.20-11.52 (raised from $11.09-11.41); Q2 guide $15.20-15.75B, +6-10% LC")

eps_23 = tot_now * OP_MARGIN["FY23E"] * (1 - TAX_RATE) / SHARES_DIL_B
eps_bear = tot_bear * OP_MARGIN["BEAR"] * (1 - TAX_RATE) / SHARES_FY25_B
eps_bull = tot_bull * OP_MARGIN["BULL"] * (1 - TAX_RATE) / SHARES_FY25_B
print(f"\n  FY2023E EPS check:  {CUR}{tot_now:.1f}B × {OP_MARGIN['FY23E']*100:.1f}% × (1−{TAX_RATE*100:.1f}%) ÷ {SHARES_DIL_B:.3f}B"
      f"  =  {CUR}{eps_23:.2f}  (guide midpoint {CUR}{EPP_TODAY_EPS:.2f})")
print(f"  FY2025E BEAR check: {CUR}{tot_bear:.1f}B × {OP_MARGIN['BEAR']*100:.1f}% ÷ {SHARES_FY25_B:.3f}B  =  {CUR}{eps_bear:.2f}"
      f"  (scenario {CUR}{SCENARIOS['BEAR'][0]:.2f})")
print(f"  FY2025E BULL check: {CUR}{tot_bull:.1f}B × {OP_MARGIN['BULL']*100:.1f}% ÷ {SHARES_FY25_B:.3f}B  =  {CUR}{eps_bull:.2f}"
      f"  (scenario {CUR}{SCENARIOS['BULL'][0]:.2f})")
print(f"  Every 1pp of operating margin ≈ {CUR}{tot_now*0.01*(1-TAX_RATE)/SHARES_DIL_B:.2f} EPS ≈ {CUR}{tot_now*0.01*(1-TAX_RATE)/SHARES_DIL_B*PE_PCTL['median']:.0f}/share at the median P/E")

print(f"\n  ① SIGNAL DASHBOARD")
print(f"  {'Signal':<32}  {'BEAR':>7}  {'BASE≥':>7}  {'BULL≥':>7}  {'XBULL≥':>7}  {'NOW':>8}  Score")
print("  " + "─" * (W-2))
for name_, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u = unit.split()[0] if unit else ""
    bv_s  = f"{bv:+.1f}{u}" if hib else f">{bv:.1f}{u}"
    bar   = "█" * s + "░" * (4 - s)
    print(f"  {name_:<32}  {bv_s:>7}  {f'{bf:.1f}{u}':>7}  {f'{blf:.1f}{u}':>7}  {f'{xf:.1f}{u}':>7}  {f'{cv:+.1f}{u}':>8}  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:    {proxy_composite:.2f} / 4.00")
print(f"  Market composite:   {mkt_composite:.2f} / 4.00  (back-solved from {CUR}{CURRENT_PRICE:,.0f} + {REQUIRED_RETURN*100:.0f}% hurdle)")
print(f"  SCA adjustment:    {sca:+.2f}  ·  EPP-distance adj {epp_adj:+.2f}  →  Adj composite {adj_composite:.2f}  →  Gap {adj_gap:+.2f}  [{_verdict}]")

print(f"\n  Structural factors:")
for desc, score, wt in STRUCTURAL_FACTORS:
    arrow = "  +" if score > 0 else "  -"
    print(f"  {arrow}  {desc}  ({score:+.1f} × {wt*100:.0f}%  =  {score*wt:+.2f})")

print(f"\n  ② BEAR CASE ANATOMY  (what variables need to do for BEAR to materialise)")
print("  " + "─" * (W-2))
print(f"  {'Signal':<32}  {'Current':>8}  {'Bear val':>8}  Move    Trigger")
for name_, unit, bv, bf, blf, xf, cv, hib, narr, s, w in scored:
    u = unit.split()[0] if unit else ""
    trigger = narr[:40] if len(narr) <= 40 else narr[:37] + "…"
    print(f"  {name_:<32}  {f'{cv:+.1f}{u}':>8}  {f'{bv:+.1f}{u}':>8}  {f'{bv-cv:+.1f}{u}':>6}  {trigger}")

print(f"\n  Bear composite:  {bear_composite:.2f}  →  Bear scenario price: ~{CUR}{expected_price(bear_probs, SCENARIOS):,.0f}  (model)  /  {CUR}{SCENARIOS['BEAR'][2]:,} (defined)")
print(f"  Bear probability (proxy model):  {proxy_probs['BEAR']*100:.1f}%")
print("""
  KEY TRIGGER: consulting slowed from +22% to +10% LC in one quarter; the
  bear case needs that slowdown to reach managed services (+20% LC) through
  repriced renewals. A JOINT event: a demand recession alone hits consulting,
  GenAI deflation alone hits run/maintain work — the bear needs both at once.""")

print(f"\n  ③ UPDATED EPP  (floor anchored on TODAY's fundamentals × trough multiple)")
print("  " + "─" * (W-2))
print(f"  Today's normalized EPS:          {CUR}{EPP_TODAY_EPS:.2f}  (FY2023E, guide midpoint)")
print(f"  Min viable P/E at panic:          {EPP_MIN_PE:.0f}x  [median of panic troughs: " +
      ", ".join(f"{d[:7]} {pe:.1f}x" for d, pe in PANIC_TROUGHS) + "]")
print(f"  {'─'*60}")
print(f"  UPDATED EPP:                     {CUR}{epp_updated:,.0f}/share")
print(f"  Current {CUR}{CURRENT_PRICE:,.0f} vs Updated EPP {CUR}{epp_updated:,.0f}:  {epp_gap_pct:+.0f}%  {epp_label}")
print(f"  Bear {CUR}{SCENARIOS['BEAR'][2]:,} vs Updated EPP {CUR}{epp_updated:,.0f}:  {bear_vs_epp_pct:+.0f}%  {'← BEAR requires earnings impairment' if bear_vs_epp_pct < 0 else '✓ bear is cyclical repricing'}")
print(f"  EPP-distance adjustment (v2):    {epp_adj:+.2f} on the composite")

print(f"\n  ④ CONSERVATIVE GROWTH  (2-yr, signals at BASE lower bound — no tailwinds)")
print("  " + "─" * (W-2))
print(f"  {'Signal':<32}  {'Conservative':>14}  vs Current  Rationale")
for idx, sval, srat in CONS_SIGNALS:
    sig = SIGNALS[idx]
    print(f"  {sig[0]:<32}  {sval:>14.1f}  {sval-sig[6]:>+9.1f}   {srat[:34]}")

print(f"\n  Conservative 2yr EPS:   {CUR}{EPP_TODAY_EPS:.2f} × (1+{CONS_EPS_CAGR*100:.0f}%)² = {CUR}{cons_eps_2yr:.2f}")
print(f"  At {CONS_EXIT_PE:.0f}x P/E (conservative):  {CUR}{cons_price_2yr:,.0f}/share")
print(f"  + Cumul. dividends (2yr):  +{CUR}{cons_div_2yr:.2f}/share")
print(f"  {'─'*60}")
print(f"  Conservative 2yr price:     {CUR}{cons_price_2yr:,.0f}  ({'▲' if cons_price_2yr > CURRENT_PRICE else '▼'}{abs(cons_price_2yr - CURRENT_PRICE):,.0f} from {CUR}{CURRENT_PRICE:,.0f})")
print(f"  Conservative total return:  {cons_total_ret:+.0f}% over 2yr  = {cons_annual_ret:+.0f}%/yr")
_pe_now = CURRENT_PRICE / EPP_TODAY_EPS
_be_eps = (CURRENT_PRICE - cons_div_2yr) / CONS_EXIT_PE
_be_g   = ((_be_eps / EPP_TODAY_EPS) ** 0.5 - 1) * 100
if _pe_now > CONS_EXIT_PE * 1.10:
    print(f"""
  5% EPS growth is not a bad business — it is simply what is left once the
  premium multiple ({_pe_now:.1f}x) mean-reverts to ~22x. Breakeven at {CONS_EXIT_PE:.0f}x needs
  FY2025E EPS of {CUR}{_be_eps:.2f}, i.e. {_be_g:.1f}%/yr — the multiple, not the business, is the risk.""")
else:
    print(f"""
  At {_pe_now:.1f}x the multiple is already near its ~22x median, so the conservative
  case is a growth question: breakeven at {CONS_EXIT_PE:.0f}x needs FY2025E EPS of {CUR}{_be_eps:.2f},
  i.e. {_be_g:.1f}%/yr — the business, not the multiple, carries the risk.""")

print(f"\n  ⑤ VOLATILITY CONTEXT")
print("  " + "─" * (W-2))
print(f"  52-week range:        {CUR}{VOL_52W_LOW:,.2f}  –  {CUR}{VOL_52W_HIGH:,.2f}  (at {(CURRENT_PRICE-VOL_52W_LOW)/(VOL_52W_HIGH-VOL_52W_LOW)*100:.0f}th pct of range)")
print(f"  Annual dividend:      {CUR}{VOL_DIVIDEND:.2f}/share  (yield {VOL_DIVIDEND/CURRENT_PRICE*100:.1f}%)")
print(f"  Realized vol (1yr):   {VOL_ANNUAL_PCT*100:.0f}% annualized")
print(f"  Beta vs broad market: {VOL_BETA:.2f}")
print(f"  1-sigma range (1yr):  {CUR}{CURRENT_PRICE - sigma_1yr:,.0f}  –  {CUR}{CURRENT_PRICE + sigma_1yr:,.0f}  ({CUR}{CURRENT_PRICE:,.0f} ± {VOL_ANNUAL_PCT*100:.0f}%)")
print(f"  2-sigma range (1yr):  {CUR}{CURRENT_PRICE - 2*sigma_1yr:,.0f}  –  {CUR}{CURRENT_PRICE + 2*sigma_1yr:,.0f}")
print(f"  {'─'*60}")
print(f"  Bear {CUR}{SCENARIOS['BEAR'][2]:,} requires:  ~{sigma_needed_bear:.1f}σ price move  {'(unusual — requires fundamental break)' if sigma_needed_bear > 1.5 else '(within normal vol range)'}")
print(f"""  A consulting compounder with a {VOL_BETA:.1f} beta: the stock is {(CURRENT_PRICE/REF_LOW-1)*100:+.0f}% off its October
  low while consulting growth went from +22% (Q4 FY22) to +10% LC (Q1).
  {'The rally is in the multiple, not the numbers.' if CURRENT_PRICE / REF_LOW > 1.10 else 'Near the low: the multiple has de-rated alongside the numbers.'}""")

print(f"\n  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
print("  " + "─" * (W-2))
print(f"  {'Scenario':<8}  {'EPS':>6}  {'P/E':>5}  {'Price':>8}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>6}  Description")
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    sc = SCENARIOS[k]
    pp, mp = proxy_probs[k], mkt_probs[k]
    print(f"  {k:<8}  {sc[0]:>6.2f}  {sc[1]:>4.1f}x  {CUR}{sc[2]:>7,}  {pp*100:>6.1f}%  {mp*100:>7.1f}%  {(pp-mp)*100:>+6.1f}pp  {sc[3]}")

_band = ("above the BULL case" if market_target_ev > SCENARIOS["BULL"][2] else
         "between the BASE and BULL cases" if market_target_ev > SCENARIOS["BASE"][2] else "at or below the BASE case")
_read = ("the price asks for more than the numbers support" if adj_gap < -0.20 else
         "price and numbers roughly agree" if adj_gap <= 0.20 else "the numbers support more than the price asks")
print(f"\n  Proxy EV (2yr): {CUR}{proxy_ev:,.0f}  /  Market EV: {CUR}{mkt_ev:,.0f}  /  Current: {CUR}{CURRENT_PRICE:,.0f}")
print(f"  Conservative EV (2yr, ④): {CUR}{cons_price_2yr:,.0f} + {CUR}{cons_div_2yr:.2f} divs = {CUR}{cons_price_2yr + cons_div_2yr:,.0f} total value")
print(f"  Downside (→ Bear {CUR}{SCENARIOS['BEAR'][2]}): {ev['down']*100:.1f}%   Upside (→ Bull {CUR}{SCENARIOS['BULL'][2]}): {ev['up']*100:.1f}%   Ratio B {ratio_b:.2f}x  →  {signal_full}")
print(f"""
  To earn the {REQUIRED_RETURN*100:.0f}%/yr hurdle from {CUR}{CURRENT_PRICE:,.0f} the market needs {CUR}{market_target_ev:,.0f} in two years —
  {_band}. That is a market composite of {mkt_composite:.2f} against a model
  read of {adj_composite:.2f}: {_read}.""")

# ── ⑦ ROBUSTNESS (retrospective-only: is the verdict an artefact of one input?) ──
P = PE_PCTL
VARIANTS = [
    ("Main case",                                  dict()),
    ("Multiples one band richer (p25/p75/p90/max)", dict(scenarios=build_scenarios(pe={"BEAR": P["p25"], "BASE": P["p75"], "BULL": P["p90"], "XBULL": P["max"]}))),
    ("Multiples one band cheaper (p5/p25/med/p75)", dict(scenarios=build_scenarios(pe={"BEAR": P["p5"], "BASE": P["p25"], "BULL": P["median"], "XBULL": P["p75"]}))),
    ("Scenario EPS +1.5pp/yr",                     dict(scenarios=build_scenarios(eps_mult=1.015 ** 2))),
    ("Scenario EPS -1.5pp/yr",                     dict(scenarios=build_scenarios(eps_mult=0.985 ** 2))),
    ("Structural read +0.30 (bullish SCA)",        dict(sca_shift=0.30)),
    ("EPP at 21x (near the 2022-23 trough, no v2 penalty)", dict(epp_pe=21.0)),
    ("Hurdle 10%/yr instead of 15%",               dict(hurdle=0.10)),
]
print(f"\n  ⑦ ROBUSTNESS  (each line changes one input; classification uses the same rules)")
print("  " + "─" * (W-2))
print(f"  {'Variant':<44}  {'Ratio B':>7}  {'EPP gap':>7}  {'Adj gap':>7}  Verdict")
robustness = []
for name_, kw in VARIANTS:
    sc = kw.pop("scenarios", SCENARIOS)
    r = evaluate(sc, **kw)
    tier = legacy_tier(r["rb"])[0]
    robustness.append({"variant": name_, "ratio_b": r["rb"], "epp_gap_pct": round(r["epp_gap_pct"], 1),
                       "adj_gap": r["gap"], "verdict": r["verdict"], "legacy_tier": tier,
                       "cons_return_2yr": round(cons_total_ret, 1)})
    print(f"  {name_:<44}  {r['rb']:>6.2f}x  {r['epp_gap_pct']:>+6.0f}%  {r['gap']:>+7.2f}  {r['verdict']} / {tier}")

print()
print("═" * W)
print("  Key catalysts to watch (from the as-of date):")
print("  (1) Q2 FY23 print (late March) — does consulting hold high single digits, and does the 8-11% FY range hold?")
print("  (2) Consulting bookings vs revenue — book-to-bill 0.96x in Q1")
print("  (3) First disclosed GenAI bookings — tailwind in numbers, or only in narrative?")
print("  (4) Managed-services renewal pricing — where GenAI deflation would show first")
print(f"  (5) Buyback pace at {CURRENT_PRICE/EPP_TODAY_EPS:.0f}x — management's own read of the multiple")
print(f"  {signal_full}  |  EPP floor {CUR}{epp_updated:,.0f}  |  ADD below ~{CUR}{SCENARIOS['BASE'][2]*0.85:,.0f}  |  TRIM above {CUR}{SCENARIOS['BULL'][2]:,}")
print("═" * W)
print()

# ── EXPORT ────────────────────────────────────────────────────────────────────
summary = (
    f"ACN (retrospective, {AS_OF}) {signal_full} — Ratio B {ratio_b:.2f}x ({ev['down']*100:.1f}% downside to Bear "
    f"${SCENARIOS['BEAR'][2]} / +{ev['up']*100:.1f}% upside to Bull ${SCENARIOS['BULL'][2]}) | "
    f"Adj composite {adj_composite:.2f} vs market {mkt_composite:.2f}: gap {adj_gap:+.2f} [{_verdict}] | "
    f"{epp_gap_pct:+.0f}% above the EPP floor ${epp_updated:,.0f} ({EPP_MIN_PE:.0f}x FY23E ${EPP_TODAY_EPS:.2f}) | "
    f"Conservative 2-yr case: {cons_total_ret:+.1f}% total ({cons_annual_ret:+.1f}%/yr) | "
    f"At {CURRENT_PRICE/EPP_TODAY_EPS:.1f}x FY23E the 15% hurdle price ${market_target_ev:,.0f} sits {_band} while "
    f"consulting has slowed to +10% LC (from +22%) and Q2 is guided to +6-10% LC; GenAI is a live theme but priced as a tailwind, not a threat."
)
RESULT = {
    "ticker":           TICKER,
    "company":          COMPANY,
    "date":             AS_OF,
    "price":            CURRENT_PRICE,
    "signal":           signal_full,
    "signal_short":     signal_short,
    "epp":              round(epp_updated, 2),
    "epp_gap_pct":      round(epp_gap_pct, 1),
    "epp_adj":          epp_adj,
    "ratio_b":          ratio_b,
    "ratio_b_fmt":      f"{ratio_b:.2f}x",
    "proxy_composite":  round(proxy_composite, 3),
    "sca":              round(sca, 3),
    "adj_composite":    round(adj_composite, 3),
    "market_composite": mkt_composite,
    "adj_gap":          adj_gap,
    "valuation":        _verdict,
    "cons_return_2yr":  round(cons_total_ret, 1),
    "scenarios":        {k: {"eps": v[0], "pe": v[1], "price": v[2], "desc": v[3]} for k, v in SCENARIOS.items()},
    "robustness":       robustness,
    "summary":          summary,
}
