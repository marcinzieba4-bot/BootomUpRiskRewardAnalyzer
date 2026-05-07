#!/usr/bin/env python3
"""
Oracle Signal Model
────────────────────
Same framework applied to Oracle Corporation (NYSE: ORCL).

Key structural difference from AVGO, COIN, and SAP:
  $553B RPO (+325% YoY) — the largest contracted backlog in enterprise software
  54% of RPO is ONE customer (OpenAI ~$300B) — extreme concentration risk
  $90B FY2027 revenue target requires 36% growth — the most aggressive guide of all 4
  OCI growing at 84% YoY but starting from smaller base than AWS/Azure

The interesting question: proxy signals are XBULL-grade across the board, yet
the market prices Oracle at 22x forward earnings. The gap is the largest of
any stock in this framework — and entirely explained by delivery uncertainty.

Run: python orcl_signal_model.py
"""
import math

# ── CONFIG ────────────────────────────────────────────────────────────────
CURRENT_PRICE   = 175.0     # USD (NYSE: ORCL, ~May 2026)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

# Scenario 2-year price targets (non-GAAP EPS × exit multiple)
# Oracle's multiple is capped by: net debt ~$95.5B, execution history,
# and the fact that OCI is still 3-4x smaller than AWS/Azure.
# FY2028E non-GAAP EPS range: $8 (bear) to $18 (xbull)
SCENARIOS = {
    #           EPS    mult  price   narrative
    "BEAR":  ( 8.0,   18,   144,  "OCI growth stalls; OpenAI diversifies; $90B miss"),
    "BASE":  (11.0,   22,   242,  "OCI 50%+ to FY2027; $90B achieved; stable debt service"),
    "BULL":  (14.0,   25,   350,  "OCI 70%+; multicloud DB expands; 4th hyperscaler status"),
    "XBULL": (18.0,   28,   504,  "OCI = primary AI cloud; RPO converts; $100B+ run-rate"),
}

# ── RPO CONCENTRATION CALCULATOR (Oracle-specific structural feature) ────
TOTAL_RPO_B         = 553.0     # total remaining performance obligations ($B, Q3 FY2026)
OPENAI_RPO_B        = 300.0     # OpenAI multi-year contract ($B, est.)
OTHER_AI_RPO_B      =  83.0     # other AI customers in RPO ($B, est.)
TRADITIONAL_RPO_B   = 170.0     # legacy cloud + apps + support ($B)
FY2026E_REVENUE_B   =  66.0     # FY2026 estimated revenue ($B)
FY2027_TARGET_B     =  90.0     # Oracle's own FY2027 target ($B)
ANNUAL_RPO_BURN_PCT =  0.12     # % of RPO that converts to revenue per year (est.)

def rpo_analysis():
    openai_pct      = OPENAI_RPO_B / TOTAL_RPO_B
    ai_total_pct    = (OPENAI_RPO_B + OTHER_AI_RPO_B) / TOTAL_RPO_B
    annual_burn     = TOTAL_RPO_B * ANNUAL_RPO_BURN_PCT
    fy2027_gap      = FY2027_TARGET_B - FY2026E_REVENUE_B
    fy2027_growth   = (FY2027_TARGET_B / FY2026E_REVENUE_B - 1) * 100
    # What % of RPO must convert in FY2027 to hit target (incremental only)
    incremental_conv_needed = fy2027_gap / TOTAL_RPO_B
    return openai_pct, ai_total_pct, annual_burn, fy2027_gap, fy2027_growth, incremental_conv_needed

# ── PROXY SIGNALS ─────────────────────────────────────────────────────────
# Chosen to cover: AI infra spend (OCI's #1 customer type), Oracle's own
# backlog momentum, cloud platform growth, enterprise multi-cloud adoption,
# and frontier AI CapEx direction (drives the $300B OpenAI RPO).
#
# (name, value, unit, base_floor, bull_floor, xbull_floor, higher_is_better,
#  what_it_drives_for_ORCL)
SIGNALS = [
    # OCI IaaS revenue YoY: +84% in Q3 FY2026.
    # Oracle's own hyperscale cloud. Primary driver of the $90B FY2027 target.
    # At $4.9B/quarter run-rate growing 84%, OCI is ~$20B annualised.
    # This is Oracle's own reported data but is the most directional single metric.
    ("OCI / IaaS revenue YoY",           84.0, "% YoY",    20,  50,  75, True,
     "core cloud revenue driver; $20B annualised; must sustain 50%+ for $90B target"),

    # Oracle RPO sequential change: +$30B QoQ in Q3 FY2026 (to $553B from $523B).
    # Contracted-not-yet-recognised. The rate of new signings is the best
    # leading indicator of revenue 2-6 quarters out. Each $10B/Q = ~$1.2B/yr revenue.
    ("Oracle RPO — sequential change",   30.0, "$B/Q",      5,  15,  25, True,
     "contracted future revenue; sequential $30B adds → revenue 2-6Q out"),

    # NVIDIA data center revenue quarterly: $35.6B in Q4 FY2026 (+69% YoY).
    # OCI is NVIDIA's largest hyperscale customer by GPU cluster size.
    # NVIDIA data center growth = OCI capacity expansion approval signal.
    ("NVIDIA data center rev (qtly)",    35.6, "$B/Q",      8,  20,  35, True,
     "OCI GPU capacity signal; ORCL is top NVIDIA hyperscale GPU customer"),

    # Hyperscaler CapEx YoY: +77% in aggregate (AWS + Azure + Google + Meta).
    # Oracle competes for the same AI workloads. High hyperscaler CapEx = AI
    # demand is real and sustained, directly flows into OCI capacity expansion.
    ("Hyperscaler CapEx YoY",            77.0, "% YoY",    10,  30,  60, True,
     "AI demand validation; Oracle wins AI workloads when CapEx cycle is hot"),

    # Oracle multi-cloud DB YoY: +531% in Q3 FY2026.
    # Oracle Database@Azure, @AWS, @Google. The 'Switzerland' strategy — running
    # Oracle DB inside competing clouds. Each connection = stickier customer.
    # Growth at 531% is from tiny base but validates the multi-cloud go-to-market.
    ("Oracle multi-cloud DB YoY",       531.0, "% YoY",    50, 150, 400, True,
     "cross-cloud stickiness; each multi-cloud DB = higher retention + upsell"),

    # Frontier AI CapEx signal (qualitative 1-4):
    # 1=AI investment pause, 2=flat, 3=continued growth, 4=acceleration
    # Current: OpenAI, Anthropic, Google Gemini all increasing spend → score 3.
    # Scored below 4 specifically because OpenAI = 54% of Oracle RPO —
    # concentration risk means this signal cuts both ways.
    ("Frontier AI CapEx signal",          3.0, "/4 scale",  1,   2,   4, True,
     "OpenAI/$300B RPO conversion; frontier model training requires OCI GPU clusters"),
]
WEIGHTS = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]

# ── STRUCTURAL RISK OVERLAY ──────────────────────────────────────────────
STRUCTURAL_FACTORS = [
    ("Oracle DB ecosystem switching cost moat",       1.0, 0.25),
    ("OpenAI 54% RPO concentration risk",            -1.8, 0.30),
    ("~$95B net debt — financial flexibility",        -0.8, 0.20),
    ("$90B FY2027 target credibility risk",           -0.8, 0.15),
    ("10GW power delivery timeline risk",             -0.5, 0.10),
]

# ── SCORING ───────────────────────────────────────────────────────────────
def score_signal(val, base_f, bull_f, xbull_f, hib):
    if hib:
        if val >= xbull_f: return 4
        if val >= bull_f:  return 3
        if val >= base_f:  return 2
        return 1
    else:
        if val <= base_f:  return 4
        if val <= bull_f:  return 3
        if val <= xbull_f: return 2
        return 1

ICONS = {4: "★ XBULL", 3: "▲ BULL", 2: "◦ BASE", 1: "⚠ BEAR"}

def softmax_probs(composite, T=0.60):
    centres = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    raw = {k: math.exp(-abs(composite - c) / T) for k, c in centres.items()}
    tot = sum(raw.values())
    return {k: v / tot for k, v in raw.items()}

def expected_price(probs):
    return sum(probs[k] * SCENARIOS[k][2] for k in probs)

def market_implied_composite(target_ev, tolerance=1.0):
    for c in [x / 100 for x in range(100, 401)]:
        if abs(expected_price(softmax_probs(c)) - target_ev) < tolerance:
            return round(c, 2), softmax_probs(c)
    return None, None

# ── MAIN ──────────────────────────────────────────────────────────────────
W = 72

scored = [(name, val, unit, score_signal(val, bf, bull_f, xf, hib), w, rt)
          for (name, val, unit, bf, bull_f, xf, hib, rt), w in zip(SIGNALS, WEIGHTS)]
proxy_composite = sum(s * w for *_, s, w, _ in scored)
sca           = sum(s * w for _, s, w in STRUCTURAL_FACTORS)
adj_composite = proxy_composite + sca
proxy_probs     = softmax_probs(proxy_composite)
proxy_ev        = expected_price(proxy_probs)

market_target_ev  = CURRENT_PRICE * ((1 + REQUIRED_RETURN) ** HORIZON_YEARS)
mkt_composite, mkt_probs = market_implied_composite(market_target_ev)
mkt_ev = expected_price(mkt_probs) if mkt_probs else market_target_ev

openai_pct, ai_total_pct, annual_burn, fy2027_gap, fy2027_growth, incr_conv = rpo_analysis()

print()
print("═" * W)
print("  ORACLE SIGNAL MODEL  —  proxy vs. market-implied probability")
print("═" * W)

# RPO concentration analysis
print(f"\n  RPO CONCENTRATION ANALYSIS  (the structural risk and opportunity)")
print("  " + "─" * (W-2))
print(f"  Total RPO (Q3 FY2026):                      ${TOTAL_RPO_B:>7.0f}B")
print(f"  ├─ OpenAI (est.):          ${OPENAI_RPO_B:.0f}B  ({openai_pct*100:.0f}% of total) ← concentration risk")
print(f"  ├─ Other AI customers:      ${OTHER_AI_RPO_B:.0f}B  ({OTHER_AI_RPO_B/TOTAL_RPO_B*100:.0f}% of total)")
print(f"  └─ Traditional cloud/apps: ${TRADITIONAL_RPO_B:.0f}B  ({TRADITIONAL_RPO_B/TOTAL_RPO_B*100:.0f}% of total)")
print(f"  AI as % of total RPO:                       {ai_total_pct*100:.0f}%")
print()
print(f"  FY2027 revenue target:                      ${FY2027_TARGET_B:.0f}B  (+{fy2027_growth:.0f}% vs FY2026E)")
print(f"  FY2026E revenue:                            ${FY2026E_REVENUE_B:.0f}B")
print(f"  Incremental revenue needed in FY2027:       ${fy2027_gap:.0f}B")
print(f"  % of total RPO that must convert (incr.):  {incr_conv*100:.1f}%  of $553B")
print(f"  Estimated annual RPO burn rate (~{ANNUAL_RPO_BURN_PCT*100:.0f}%):      ${annual_burn:.0f}B / yr")
print(f"  → ${FY2027_TARGET_B:.0f}B target is achievable IF OCI sustains 50%+ growth AND")
print(f"    OpenAI does not diversify to AWS/Azure/Google before contracts convert.")

# Signal scorecard
print(f"\n  PROXY SIGNAL SCORECARD")
print(f"  {'Signal':<38}{'Value':>9}  Wt   Score")
print("  " + "─" * (W-2))
for name, val, unit, s, w, rt in scored:
    bar = "█" * s + "░" * (4 - s)
    if unit in ("/4 scale",):
        fmt = f"{val:>+7.1f}"
    elif unit == "$B/Q":
        fmt = f"${val:>6.1f}"
    else:
        fmt = f"{val:>+7.1f}"
    print(f"  {name:<38}{fmt}{unit[0]}  {w*100:.0f}%  {ICONS[s]}  {bar}")

print(f"\n  Proxy composite:   {proxy_composite:.2f} / 4.00")
if mkt_composite:
    print(f"  Market composite:  {mkt_composite:.2f} / 4.00  "
          f"(back-solved from ${CURRENT_PRICE:.0f} + {REQUIRED_RETURN*100:.0f}% reqd return)")
    gap = proxy_composite - mkt_composite
    print(f"  Gap (proxy − mkt): {gap:+.2f}  ← the largest gap in this framework")

# Valuation context
print(f"\n  VALUATION CONTEXT")
print("  " + "─" * (W-2))
print(f"  Current price:           ${CURRENT_PRICE:.0f}")
print(f"  FY2026E non-GAAP EPS:    ~$7.95  (consensus)")
print(f"  Forward P/E:             ~22x  (vs 30-35x for hyperscalers)")
print(f"  Net debt:                ~$95.5B  ($134.6B gross - $39.1B cash)")
print(f"  FY2026E CapEx:           ~$50B  (cloud infra buildout)")
print(f"  Analyst avg target:      ~$200-305  (+{(252/CURRENT_PRICE-1)*100:.0f}% vs current, midpoint)")
print(f"  → Cheap on PE, expensive on FCF once you net out $50B CapEx cycle")

# Probability table
print(f"\n  STRUCTURAL RISK OVERLAY  (analyst-assessed; beyond proxy signals)")
print("  " + "─" * (W-2))
print(f"  {'Factor':<44}  {'Score':>5}  {'Wt':>3}   {'Adj':>5}")
for desc, score, wt in STRUCTURAL_FACTORS:
    adj_c = score * wt
    arrow = "▲" if score > 0 else "▼"
    print(f"  {desc:<44}  {score:>+5.1f}  {wt*100:>3.0f}%  {adj_c:>+5.2f}  {arrow}")
print(f"  {'─'*68}")
print(f"  Structural adj. (SCA):     {sca:>+6.2f}")
print(f"  Adjusted composite:         {adj_composite:.2f}  "
      f"(proxy {proxy_composite:.2f} {'+' if sca >= 0 else ''}{sca:.2f})")
if mkt_composite:
    adj_gap = adj_composite - mkt_composite
    if   adj_gap >  0.50: _verdict = "UNDERVALUED"
    elif adj_gap >  0.20: _verdict = "MODESTLY UNDERVALUED"
    elif adj_gap > -0.20: _verdict = "FAIRLY VALUED"
    elif adj_gap > -0.50: _verdict = "MODESTLY OVERVALUED"
    else:                 _verdict = "OVERVALUED"
    print(f"  Market composite:          {mkt_composite:.2f}")
    print(f"  ADJUSTED GAP:             {adj_gap:>+6.2f}  ← {_verdict}")

print(f"\n  {'Scenario':<10}  {'Proxy':>8}  {'Market':>8}  {'Gap':>8}  "
      f"{'EPS':>6}  {'Mult':>5}  {'Price':>7}  Narrative")
print("  " + "─" * (W-2))
for k in ["BEAR", "BASE", "BULL", "XBULL"]:
    eps, mult, price, narr = SCENARIOS[k]
    pp  = proxy_probs[k]
    mp  = mkt_probs[k] if mkt_probs else 0
    gap_pp = pp - mp
    sign = "+" if gap_pp >= 0 else ""
    print(f"  {k:<10}  {pp*100:>7.1f}%  {mp*100:>7.1f}%  "
          f"{sign}{gap_pp*100:>6.1f}pp  ${eps:>5}  {mult:>4}x  ${price:<6}  {narr[:28]}…")

print(f"\n  Prob-weighted 2yr:  proxy ${proxy_ev:.0f}  /  market ${mkt_ev:.0f}")
print(f"  Current price: ${CURRENT_PRICE:.0f}")

# Verdict
print(f"\n  WHAT THE GAP MEANS")
print("  " + "─" * (W-2))
gap = (proxy_composite - mkt_composite) if mkt_composite else 0
print(f"""  Proxy composite {proxy_composite:.2f}  vs  market-implied {mkt_composite:.2f}.
  Gap = {gap:+.2f}

  Cross-stock gap comparison:
    AVGO gap = +1.41  (proxies bullish; market applies 4-part skepticism discount)
    SAP  gap = +0.91  (proxies constructive; market in 'show me' mode on Joule)
    COIN gap = +0.29  (fairly priced; 6 signals collapse into 1 BTC driver)
    ORCL gap = {gap:+.2f}  (proxies near-XBULL; market applies the LARGEST discount)

  WHY THE MARKET PRICES ORACLE WELL BELOW PROXY SIGNALS:

    1. OpenAI concentration (54% of RPO): $300B from ONE customer.
       If OpenAI diversifies to AWS/Azure or raises its own capital to build
       in-house infra, Oracle loses its entire bull case. Market assigns
       ~40% probability to partial OpenAI diversification within 3 years.

    2. $90B FY2027 target is the most aggressive guide in enterprise software.
       Requires 36% revenue growth. Oracle has missed aggressive multi-year
       targets before (the 'cloud 2.0' era). Market discounts by ~30%.

    3. Delivery uncertainty on 10GW power capacity:
       Oracle has pre-committed to data center builds requiring ~10GW of
       new power. Permitting, grid connection, and construction timelines
       routinely slip 12-24 months. CapEx is sunk; revenue is not.

    4. Net debt of ~$95.5B limits financial flexibility:
       At 15% required return, $95.5B of debt consumes ~$14B/yr of equity
       value. Refinancing risk rises if rates stay elevated. Oracle cannot
       easily pivot if OCI growth slows — CapEx is already committed.

    5. OCI is still structurally #4:
       AWS, Azure, and Google each have 3-5x OCI's scale. Network effects
       in cloud compound. Oracle wins on price and GPU availability for AI
       training, but enterprise migration from AWS/Azure is slow.

  THE BULL CASE REQUIRES TWO NON-HEROIC ASSUMPTIONS:
    (a) OpenAI contract holds: even 50% RPO conversion = $150B over 3 years,
        sufficient to sustain OCI at 50%+ growth through FY2027.
    (b) Multi-cloud DB adoption continues: each Oracle DB@Azure/AWS contract
        locks in 5-7 yr retention and creates natural OCI upsell path.
    Combined: $90B FY2027 at 22x multiple = $242 (BASE, +38% from $175).

  THE NON-CONSENSUS CATALYST (not yet priced):
    Oracle becoming the de-facto AI training cloud for frontier models
    outside of OpenAI. Each new frontier AI lab (xAI, Mistral, Cohere,
    Databricks) that signs a multi-year OCI GPU contract de-risks the
    concentration problem AND adds to RPO. One Grok-scale contract
    (~$5-10B/yr) would move the stock 15-20% on announcement.

  THE BEAR CASE IS ALSO REAL:
    OpenAI closes its own data centers (Project Stargate alternative route),
    reducing Oracle OCI demand by 30-40% annually. OCI growth drops to 20%.
    $90B target is missed by 20%. EPS stays ~$8. Multiple compresses to 18x
    on debt burden. Stock returns to ~$144 (-18% from current).""")
print()
print("═" * W)
