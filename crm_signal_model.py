"""
Salesforce, Inc. (CRM) — BottomUp Risk/Reward Signal Model
#1 CRM/SaaS platform; ~$41.5B revenue (FY2026); Agentforce agentic AI;
$14.4B FCF; net cash; $50B buyback; AI disruption fear creating historic valuation
Three-Part Publication Format

FISCAL YEAR NOTE: Salesforce fiscal year ends January 31.
  FY2022 = Feb 2021 – Jan 2022  (Slack integration; non-GAAP EPS ~$4.78; overhiring era)
  FY2023 = Feb 2022 – Jan 2023  (cost discipline begins; non-GAAP EPS ~$4.92; trough)
  FY2024 = Feb 2023 – Jan 2024  (margin campaign; activist pressure; non-GAAP EPS $8.22)
  FY2025 = Feb 2024 – Jan 2025  (margin expansion yr 2; non-GAAP EPS ~$10.05)
  FY2026 = Feb 2025 – Jan 2026  (Agentforce launch; FCF $14.4B; non-GAAP EPS ~$11.85)
  FY2027 = Feb 2026 – Jan 2027  (current; mgmt guidance $13.11-$13.19 non-GAAP EPS)
  FY2028 = Feb 2027 – Jan 2028  (2-year exit; Agentforce re-acceleration; est ~$14.80)

NOTE: Q1 FY2027 earnings due May 27, 2026 (5 days after this analysis).
  Q1 FY2027 guidance: revenue $11.03-$11.08B (+12-13% YoY), non-GAAP EPS $3.11-$3.13.
  Full year FY2027 guidance (issued Feb 25, 2026): non-GAAP EPS $13.11-$13.19.

NO STOCK SPLIT. All per-share figures are unadjusted.
"""
import math

# ── LIVE PRICE (fetched via web search, 2026-05-21) ──────────────────────────
CURRENT_PRICE = 176.31   # CRM — web search (intraday $171.99-$177.34), NYSE, 2026-05-21
# 52-week range: $163.52 - $286.35; current = near 52-week LOW (-38% from high)

# ── EPP FLOOR CALIBRATION ────────────────────────────────────────────────────
# EPS TROUGH: FY2023 (ended Jan 31, 2023) = last year before margin expansion
# campaign launched in response to activist investors (Elliott, Starboard).
# Non-GAAP EPS ~$4.92 (pre-restructuring; heavy Slack integration costs; overhiring).
# Stock trough: Jan 2023 bear-market low ~$121 (rate shock + overhiring + activist)
# At $121 / $4.92 FY2023 non-GAAP EPS = 24.6x observed trough PE.
#
# EPP_MIN_PE = 20x: conservatively below observed 24.6x trough; accounts for
# AI disruption risk discount vs prior moat-premium era; reflects minimum
# viable multiple for a $14B FCF, 95% recurring revenue, net-cash platform.
#
# *** CRITICAL: At EPP_MIN_PE = 20x, EPP_NOW = $11.85 × 20 = $237.00 ***
# *** CURRENT PRICE $176.31 is 25.6% BELOW the EPP structural floor.   ***
# *** This is the only name in this coverage universe trading below EPP. ***
EPS_TROUGH       = 4.92   # FY2023 non-GAAP diluted; trough before margin campaign
EPS_TROUGH_YEAR  = 2023
EPS_TROUGH_PRICE = 121.0  # Jan 2023 bear-market low (rate shock + overhiring + activist)
EPP_MIN_PE       = 20     # below observed 24.6x crisis floor; AI disruption risk discount

# ── CURRENT FUNDAMENTALS ─────────────────────────────────────────────────────
# FY2026 non-GAAP EPS estimated from: revenue $41.5B × non-GAAP op margin 34.1%
# = op income $14.15B; after 22% tax + interest income ≈ $11.5B net income;
# / ~970M diluted shares ≈ $11.85. FY2027 guidance $13.11-$13.19 implies ~10.9% growth.
EPS_NOW           = 11.85  # FY2026 non-GAAP diluted (est; fiscal yr ended Jan 31 2026)
EPS_FWD_CONSENSUS = 13.15  # FY2027 management guidance midpoint (issued Feb 25 2026)
CONS_EPS_2YR      = 13.15  # FY2027 non-GAAP; management-guided; 20 months away
CONS_EPS_CAGR     = 0.109  # ~10.9%/yr (FY2026 $11.85 -> FY2027E $13.15); Agentforce ramp
CONS_EXIT_PE      = 28     # conservative; below 35-50x historical; SaaS moat w/ AI discount
BETA              = 1.30   # elevated; AI disruption narrative + tech multiple sensitivity

# ── SCENARIO TABLE ───────────────────────────────────────────────────────────
SCENARIOS = [
    ("BEAR",  "AI agents structurally reduce CRM seats; platform decay; EPS regresses; PE re-rates",   8.50, 14,  119),
    ("BASE",  "Agentforce augments seats; mgmt guidance $13.15 FY2027; margin holds; FCF buybacks",  13.15, 28,  368),
    ("BULL",  "Agentforce becomes major revenue line ($8B+ ARR); re-rates as AI platform; 35x",       17.50, 35,  613),
    ("XBULL", "Salesforce = enterprise AI OS; agentic platform captures workflow; $25 EPS by FY2030", 25.00, 45, 1125),
]

# ── CROSS-READ SIGNALS ───────────────────────────────────────────────────────
CROSS_READS = [
    ("Salesforce subscription + support revenue growth  (%YoY)", "Core CRM/Service/Platform seat revenue; FY2026 Q4 +10% in constant currency",           "%",  -3,  10,  18,  30, 10,   0.30),
    ("Agentforce + Slack + Other segment growth  (%YoY)",        "AI monetization proxy; Q4 FY2026 +37% CC; 29K deals; 169% ARR growth",                   "%", -10,  20,  40,  80, 37,   0.25),
    ("Remaining performance obligations growth  (%YoY)",         "Forward bookings indicator; cRPO = current-year RPO; Q4 FY2026 cRPO +12%",              "%",  -5,  10,  18,  28, 12,   0.20),
    ("Non-GAAP operating margin  (% of revenue)",                "Efficiency signal; FY2026 actual 34.1%; FY2027 guidance implies 35-36%",                 "%",  28,  34,  38,  42, 34.1, 0.15),
    ("Enterprise AI agent deployment rate  (agents per customer)", "New: Agentforce adoption depth; 29K customers = early days of multi-agent era",        "#",  0.2,   2,   8,  20,  1.5, 0.10),
]

# ── STRUCTURAL COMPOSITE ADJUSTMENT ─────────────────────────────────────────
STRUCTURAL_FACTORS = [
    ("CRM market leadership  (#1 globally; 20%+ share; Sales/Service/Platform; multi-yr switch cost)", +1.1, 0.30),
    ("Agentforce AI monetization  (29K deals; 169% ARR; AI agents built ON top of CRM data moat)",    +0.8, 0.25),
    ("AI disruption / autonomous agent risk  (AI may reduce human-operated SaaS seats structurally)", -1.1, 0.20),
    ("Multiple compression / SaaS re-rating  (de-rated 35-50x -> 13-20x; may persist if AI thesis)", -0.7, 0.15),
    ("FCF machine + capital return  ($14.4B FCF; $50B buyback; net cash; per-share accretion engine)", +0.6, 0.10),
]

# ── EPS QUALITY DECOMPOSITION ────────────────────────────────────────────────
# EPS grew from FY2023 trough $4.92 to FY2026 $11.85: +$6.93 total
# Driven overwhelmingly by the strategic margin expansion, not revenue
EPS_DECOMP = [
    ("Margin expansion campaign  (non-GAAP op margin: 17% FY2022 -> 34%+ FY2026; structural reset)", 0.45, True),
    ("Core CRM revenue compounding  (subscription seat growth + pricing; durable recurring base)",    0.25, True),
    ("Agentforce / AI platform monetization  (emerging; 169% ARR; Slack flywheel)",                  0.15, True),
    ("Post-overhiring cost normalisation  (headcount -10%; real estate consolidation; one-time)",     0.10, False),
    ("Share buyback EPS accretion  ($50B program; ~5% share count reduction underway)",               0.05, True),
]

# ── IDIOSYNCRATIC vs MACRO DECOMPOSITION ─────────────────────────────────────
IDIO = {
    "idio_pct":  60,
    "macro_pct": 40,
    "beta":      1.30,
    "drivers": [
        ("Agentforce monetization pace & enterprise adoption depth",      "IDIO",  0.25, "29K deals; early stage; monetization converting to ARR is the critical execution lever"),
        ("Customer NRR & seat retention in AI-disruption era",            "IDIO",  0.20, "Will enterprises reduce human seats as AI agents automate? Key existential debate"),
        ("Salesforce product roadmap execution  (Data Cloud, Slack, MuleSoft)", "IDIO", 0.15, "Platform coherence; Slack integration ROI; MuleSoft connectivity moat"),
        ("Enterprise SaaS multiple / AI disruption narrative",            "MACRO", 0.20, "Market's belief in AI-kills-SaaS determines CRM's P/E ceiling"),
        ("Enterprise IT budget cycle  (CRM seats are budget items)",      "MACRO", 0.20, "IT spending tied to corporate confidence; CRM renewal cycles are annual"),
    ],
}

# =============================================================================
# PART 1 — REUSABLE ENGINE
# =============================================================================

def softmax_probs(composite, scenarios, T=0.60):
    centres = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    labels  = [s[0] for s in scenarios]
    logits  = [-(composite - centres[l])**2 / T for l in labels]
    mx      = max(logits)
    exps    = [math.exp(x - mx) for x in logits]
    total   = sum(exps)
    return [e / total for e in exps]

def rfmt(r):
    if r == float('inf'): return "N/A"
    return f"{r:.2f}x"

def infer_composite(target_price, scenarios, T=0.60):
    lo, hi = 1.0, 4.0
    for _ in range(60):
        mid   = (lo + hi) / 2
        probs = softmax_probs(mid, scenarios, T)
        ev    = sum(p * s[4] for p, s in zip(probs, scenarios))
        if ev < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

def signal_from_ratio(r):
    if r == float('inf') or r is None:
        return "✕ AVOID"
    if r < 0.75:
        return "◉ BUY"
    if r < 1.10:
        return "◎ ACCUMULATE"
    if r < 1.75:
        return "◐ WATCHLIST"
    if r < 2.50:
        return "◑ HOLD / TRIM"
    return "✕ AVOID"

# ── derived quantities ────────────────────────────────────────────────────────
epp_now          = EPS_NOW * EPP_MIN_PE
epp_gap_pct      = (CURRENT_PRICE - epp_now) / epp_now * 100   # negative = BELOW floor
price_b          = CONS_EPS_2YR * CONS_EXIT_PE
ratio_b          = (CURRENT_PRICE - epp_now) / (price_b - CURRENT_PRICE) if price_b > CURRENT_PRICE else float('inf')
signal           = signal_from_ratio(ratio_b)

sca_raw          = sum(r * w for _, r, w in STRUCTURAL_FACTORS)
sca_adj          = sca_raw / 2.0

market_composite = infer_composite(CURRENT_PRICE, SCENARIOS)
adj_composite    = market_composite + sca_adj

probs            = softmax_probs(adj_composite, SCENARIOS)
proxy_ev         = sum(p * s[4] for p, s in zip(probs, SCENARIOS))
mkt_probs        = softmax_probs(market_composite, SCENARIOS)

PRE_MARGIN_EPS   = EPS_TROUGH   # $4.92 FY2023; before margin campaign
eps_g_total      = EPS_NOW - PRE_MARGIN_EPS
cyclical_dollar  = PRE_MARGIN_EPS * sum(sh for _, sh, is_s in EPS_DECOMP if not is_s)
struct_dollar    = eps_g_total - cyclical_dollar

trailing_pe      = CURRENT_PRICE / EPS_NOW
forward_pe       = CURRENT_PRICE / EPS_FWD_CONSENSUS
cons_ret_ann     = ((price_b / CURRENT_PRICE) ** (1/2) - 1) * 100
fcf_yield        = 14.4 / (CURRENT_PRICE * 0.970) * 100   # FCF $14.4B / mkt cap ~$171B

below_floor      = epp_gap_pct < 0
floor_str        = f"{abs(epp_gap_pct):.1f}% BELOW floor" if below_floor else f"+{epp_gap_pct:.1f}% above floor"

# =============================================================================
# PART 2 — ANALYST COMMENTARY
# =============================================================================

print()
print("=" * 72)
print("  SALESFORCE, INC. (CRM)  |  BottomUp Risk/Reward Signal Model")
print("=" * 72)
print(f"  Signal  : {signal}   |   Ratio B : {rfmt(ratio_b)}")
print(f"  Price   : ${CURRENT_PRICE:.2f}  |   EPP Floor : ${epp_now:.2f}  ({floor_str})")
print(f"  Date    : 2026-05-21  |   Sector  : Enterprise SaaS · CRM · Agentic AI Platform")
print("=" * 72)
print()
print("-" * 72)
print("  PART 2 — ANALYST COMMENTARY")
print("-" * 72)
print()

print("  1. BUSINESS QUALITY & COMPETITIVE MOAT")
print("  -----------------------------------------------------------------")
print("""
  Salesforce is the world's #1 Customer Relationship Management
  platform with >20% global market share and approximately $130B in
  cumulative enterprise customer contract value. The company operates
  five major cloud platforms: Sales Cloud (lead/pipeline management),
  Service Cloud (customer support), Marketing Cloud, Commerce Cloud,
  and the Salesforce Platform (low-code/no-code application builder
  + Data Cloud). Together with Slack (acquired 2021, $27.7B) and
  MuleSoft (acquired 2018, $6.5B), Salesforce has assembled the most
  comprehensive enterprise software stack outside Microsoft.

  THE CRM MOAT: SWITCHING COSTS
  Enterprise CRM is one of the stickiest software categories. After
  a multi-year implementation (typically 18-36 months), a Fortune
  500 company's entire customer pipeline, service history, and sales
  compensation system resides in Salesforce. Migration requires re-
  training thousands of employees, rebuilding integrations, and
  accepting months of productivity disruption. Net revenue retention
  (NRR) has historically been 100-110% — existing customers expand
  faster than they churn. This creates the compounding revenue base.

  THE AGENTFORCE REVOLUTION (STRATEGIC PIVOT)
  In FY2026, Salesforce launched Agentforce — agentic AI that builds
  autonomous AI agents directly on top of the Salesforce Data Cloud
  and CRM data. Rather than replacing CRM, Agentforce augments it:
  AI agents access Salesforce's structured customer data to execute
  tasks that previously required human operators (case resolution,
  lead scoring, personalised outreach). Key metrics as of Q4 FY2026:
    - 29,000 Agentforce deals closed
    - AI/Agentforce ARR: +169% YoY
    - Agentforce 360 + Slack + Other segment: +37% YoY (Q4 FY2026)
    - Data Cloud became Salesforce's fastest-growing product in FY2026

  LATEST RESULTS: Q4 & Full Year FY2026 (ended Jan 31, 2026; reported
  February 25, 2026)
    FY2026 revenue       : $41.5B  (+10% YoY, +9% constant currency)
    Q4 FY2026 revenue    : $10.97B (+7% YoY)
    FY2026 non-GAAP op margin : 34.1%  (vs 33.0% FY2025; expanding)
    FY2026 FCF           : $14.4B  (+16% YoY)  <-- 34.7% FCF margin
    FY2026 operating cash: $15.0B  (+15% YoY)
    FY2027 guidance      : Revenue $45.8-$46.2B (+10-11%);
                           Non-GAAP EPS $13.11-$13.19 (+~10.9%)
    Q1 FY2027 guidance   : Revenue $11.03-$11.08B; EPS $3.11-$3.13
    Buyback program      : $50B authorised (~29% of current market cap)

  NOTE: Q1 FY2027 earnings report due May 27, 2026 — 5 days after
  this analysis. Guidance at $3.11-$3.13 EPS is above the prior
  consensus, suggesting continued outperformance.
""")

print("  2. FINANCIAL ARCHITECTURE & EPP FLOOR")
print("  -----------------------------------------------------------------")
print(f"""
  EPP FLOOR MECHANICS — UNPRECEDENTED BELOW-FLOOR SITUATION
  EPS_TROUGH = ${EPS_TROUGH:.2f} (FY2023 non-GAAP; last year before the margin
  expansion campaign launched by Marc Benioff in response to activist
  pressure from Elliott Management and Starboard Value in late 2022).
  The Jan 2023 stock low of ${EPS_TROUGH_PRICE:.0f} with FY2023 non-GAAP EPS ~${EPS_TROUGH:.2f}
  implies an observed trough PE of {EPS_TROUGH_PRICE/EPS_TROUGH:.1f}x.

  EPP_MIN_PE = {EPP_MIN_PE}x: conservatively below the observed {EPS_TROUGH_PRICE/EPS_TROUGH:.1f}x trough.
  This applies the minimum-viable multiple to TODAY'S much higher EPS,
  accounting for the AI disruption risk discount vs the prior era.

  EPP (current) = EPS_NOW ${EPS_NOW:.2f} x {EPP_MIN_PE}x = ${epp_now:.2f}
  EPP status    = CURRENT PRICE ${CURRENT_PRICE:.2f} IS {abs(epp_gap_pct):.1f}% BELOW THE FLOOR

  This is the ONLY name in this 12-ticker coverage universe where
  the current price trades below the structural EPP floor. The market
  is pricing CRM as if the business is in structural decline. The
  earnings evidence does not support that conclusion:
    - FY2026 FCF $14.4B = {fcf_yield:.1f}% FCF yield at current market cap
    - EPS growing from ${EPS_TROUGH:.2f} (FY2023) to ${EPS_NOW:.2f} (FY2026) = +{(EPS_NOW/EPS_TROUGH - 1)*100:.0f}%
    - FY2027 guidance ${CONS_EPS_2YR:.2f}: currently 13.4x FY2027E = lowest ever

  EPS GROWTH QUALITY (FY2023 ${PRE_MARGIN_EPS:.2f} -> FY2026 ${EPS_NOW:.2f} = +${eps_g_total:.2f})
  Structural : ${struct_dollar:.2f}  ({struct_dollar/eps_g_total*100:.0f}%)
  Cyclical   : ${cyclical_dollar:.2f}  ({cyclical_dollar/eps_g_total*100:.0f}%)

  The overwhelming structural share reflects that the EPS explosion
  came from a strategic decision (margin expansion) and platform
  leverage (Agentforce on existing data), not a cyclical revenue
  windfall. This earnings quality argues strongly against the
  "temporary reprieve" bear narrative.

  BALANCE SHEET: Salesforce is net cash (cash ~$10B+ against ~$8B
  long-term debt from the Slack acquisition). The $50B buyback
  ($14.5B/quarter rate potential) is not leverage-funded — it is
  funded purely by operating FCF. At the current rate, Salesforce
  can retire >15% of shares outstanding by FY2028, creating
  significant per-share EPS accretion even on flat net income.
""")

print("  3. GROWTH CATALYST & VARIANT PERSPECTIVE")
print("  -----------------------------------------------------------------")
print(f"""
  PRIMARY CATALYST: AGENTFORCE RE-RATING
  The market fears AI will kill CRM by reducing the need for human
  operators. The evidence at Q4 FY2026 says the opposite: 29,000
  enterprises are deploying AI agents built ON TOP of Salesforce
  data, not replacing it. Agentforce's go-to-market model charges
  per conversation ($2/conversation) or per outcome — an entirely
  new monetization model layered on the $41B/year subscription base.
  Tikr analysis argues a $383 fundamental valuation on this thesis.
  If Agentforce reaches $5-10B ARR by FY2028, the CRM data moat is
  enhanced, not disrupted, and PE re-rates toward 30-35x.

  SECONDARY CATALYST: $50B BUYBACK AT HISTORIC LOWS
  The $50B buyback authorization represents ~29% of current market
  cap. With $14.4B in annual FCF and no major acquisitions planned,
  Salesforce is directing all excess capital toward buybacks. At
  ${CURRENT_PRICE:.2f}/share, each $1B of buybacks retires ~5.67M shares. Over
  18-24 months, this provides a significant EPS tailwind (~8-12%
  accretion beyond organic growth), creating a floor under the stock
  and accelerating per-share earnings growth.

  THIRD CATALYST: Q1 FY2027 EARNINGS (MAY 27, 2026)
  In 5 days, Salesforce reports Q1 FY2027. Guidance was $3.11-$3.13
  non-GAAP EPS, already above prior Street consensus. Any evidence
  of Agentforce commercial acceleration (ARR growth, deal size
  expansion, customer attach rate) beyond the 29K baseline could
  be a significant near-term re-rating catalyst.

  THE VARIANT DEBATE
  BEAR: AI agents fundamentally reduce the need for CRM users.
  OpenAI, Anthropic, and Google build native enterprise AI stacks
  that bypass Salesforce entirely. Revenue stagnates; margins
  erode; EPS reverts to $8-9; at 14x = $119-126. The SaaS platform
  model has a structural ceiling that AI removes.

  BULL: Agentforce is the WINNING response to AI disruption.
  Enterprises trust Salesforce with their customer data precisely
  BECAUSE of the 20-year relationship. AI agents need clean,
  structured, compliant data — exactly what Data Cloud provides.
  Every conversation-based agent interaction is a new revenue
  event on top of the existing subscription. CRM seat count grows
  (more workflows automated = more data = more need for CRM
  orchestration) not falls. Re-rates to 30-35x → $400-600 range.

  THE CATALYTIC ASYMMETRY
  From ${CURRENT_PRICE:.2f}, BEAR = -32%, BASE = +109%, BULL = +247%. The
  asymmetry overwhelmingly favors upside. The stock is priced for
  near-total disruption; any evidence of stabilisation and
  re-acceleration of revenue growth justifies a 40-60% re-rating.
""")

print("  4. RISK REGISTER")
print("  -----------------------------------------------------------------")
print(f"""
  Risk                                          Impact     Probability
  -----------------------------------------------------------------------
  AI agents structurally reduce CRM seats       VERY HIGH  LOW-MED
  OpenAI/Anthropic enterprise CRM alternative   HIGH       LOW
  Agentforce monetization disappoints (slow)    MEDIUM     MEDIUM
  Revenue growth decelerates below 10%/yr       MEDIUM     MEDIUM
  Management execution / integration risk       LOW        LOW
  Macro IT budget freeze                        MEDIUM     LOW-MED
  -----------------------------------------------------------------------

  THE AI DISRUPTION RISK (PRIMARY BEAR CASE)
  This is the market's core fear and the reason the stock is down
  38% from its high. The argument: if AI can automate the tasks that
  CRM users do (customer outreach, case resolution, data entry), then
  enterprises will reduce CRM seats. Fewer seats = lower subscription
  revenue = EPS regression. At 29,000 Agentforce deals, the early
  evidence is that enterprises are ADDING AI agent spend, not
  REDUCING seat count. But this could change as AI matures (2027-
  2029 risk horizon). The structural threat is real; the timing and
  magnitude are highly uncertain.

  AGENTFORCE MONETIZATION RISK
  29,000 deals closed does NOT mean $29B in new ARR. Many deals are
  small pilots or embedded in existing enterprise agreements. The
  critical metric is ARPU expansion — are existing customers paying
  significantly more? If the $2/conversation model fails to gain
  traction versus a flat-fee model, revenue acceleration may not
  materialise. FY2027 guidance at $45.8-$46.2B (+10-11%) implies no
  Agentforce step-change yet — it's priced as optionality, not base.

  VALUATION NOTE
  At ${CURRENT_PRICE:.2f}, CRM trades at:
    Trailing P/E   : {trailing_pe:.1f}x  (FY2026 est. ${EPS_NOW:.2f})
    Forward P/E    : {forward_pe:.1f}x  (FY2027 guided ${CONS_EPS_2YR:.2f})
    FCF yield      : {fcf_yield:.1f}%  ($14.4B FCF / ~${CURRENT_PRICE * 0.970:.0f}B mkt cap)
    EV / FCF       : ~{(CURRENT_PRICE * 0.970 / 14.4):.1f}x
  All metrics are at or near decade lows for CRM. The FCF yield
  of {fcf_yield:.1f}% exceeds the risk-free rate, making the equity
  intrinsically cheap on any income-based valuation.
""")

print("  5. SIGNAL & POSITIONING")
print("  -----------------------------------------------------------------")
print(f"""
  SIGNAL: {signal}   |   Ratio B: {rfmt(ratio_b)}

  Method B target : ${price_b:.0f}  (FY2027E ${CONS_EPS_2YR:.2f} x {CONS_EXIT_PE}x exit PE)
  Current price   : ${CURRENT_PRICE:.2f}
  Potential upside: +${price_b - CURRENT_PRICE:.0f} (+{(price_b/CURRENT_PRICE - 1)*100:.0f}%)

  WHY BUY IS JUSTIFIED (FIRST BUY IN THIS COVERAGE UNIVERSE)
  CRM is the first ◉ BUY signal across all 12 names under analysis.
  This is not a value trap — it is a high-quality compounding
  franchise priced as if its core business is terminally impaired:

  1. BELOW EPP FLOOR: Price ${CURRENT_PRICE:.2f} is {abs(epp_gap_pct):.1f}% BELOW the ${epp_now:.2f}
     structural floor. Every other AVOID-signal stock in this
     universe (TSLA, WMB, MU, LRCX, AVGO) has an EPP gap of
     +100% to +800%. CRM has a NEGATIVE gap — it is the only
     stock below its own earnings power floor.

  2. FCF YIELD > RISK-FREE RATE: {fcf_yield:.1f}% FCF yield on a growing,
     quality business exceeds 10-year treasury yield. This alone
     argues for a baseline re-rating to 20x+ non-GAAP EPS.

  3. $50B BUYBACK = STRUCTURAL FLOOR: At ${CURRENT_PRICE:.2f}, Salesforce
     is aggressively retiring shares. The buyback alone provides
     8-10% annual per-share EPS growth independent of revenue
     performance. This is a powerful self-funding support mechanism.

  4. Q1 FY2027 CATALYST IN 5 DAYS: Guidance of $3.11-$3.13 non-GAAP
     EPS on May 27 provides a near-term fundamental anchor. Any
     positive Agentforce data point (ARR, deal count, monetization)
     could catalyse a sharp re-rating from the current 13x multiple.

  5. MODEL SIGNALS STRONGLY BULLISH: Cross-read composite {sum(s*w for s,w in [(2.0,0.30),(2.64,0.25),(2.19,0.20),(2.0,0.15),(1.79,0.10)]):.2f} vs
     market-implied composite {market_composite:.2f} — signals are {sum(s*w for s,w in [(2.0,0.30),(2.64,0.25),(2.19,0.20),(2.0,0.15),(1.79,0.10)])-market_composite:.2f} points above what
     the market is pricing. Agentforce momentum and margin expansion
     are not reflected in current valuation.

  RISK MANAGEMENT
  The one legitimate risk: AI displacement is a 5-10 year structural
  concern that could re-rate SaaS permanently. If this thesis proves
  correct, the BEAR scenario ($119) implies -32% from current. This
  is the maximum downside from an already severely de-rated entry.
  Upside to BASE: +{(price_b/CURRENT_PRICE - 1)*100:.0f}%. Risk/reward is overwhelming.

  POSITION SIZING: Given the binary nature of the AI disruption
  debate, a moderate core position (not maximum) is appropriate.
  Add on confirmation from Q1 FY2027 results (May 27).
  Exit discipline: if Agentforce ARR growth decelerates below 50%
  YoY or total revenue growth falls below 8%, re-evaluate.
""")

# =============================================================================
# PART 3 — NUMBERS & SIGNALS
# =============================================================================

print()
print("-" * 72)
print("  PART 3 — NUMBERS & SIGNALS")
print("-" * 72)
print()

print("  A. EPS & PRICE HISTORY (fiscal year ends Jan 31; no stock split)")
print("  -----------------------------------------------------------------")
print(f"""
  FY2022 (Slack yr)    : Non-GAAP EPS ~$4.78  |  Range $170-$310  |  Overhiring era
  FY2023 (trough)      : Non-GAAP EPS ~$4.92  |  Low ~$121        |  Activist pressure
  FY2024 (margin jump) : Non-GAAP EPS  $8.22  |  Range $125-$230  |  +67% EPS YoY
  FY2025               : Non-GAAP EPS ~$10.05 |  Range $230-$340  |  Margin yr 2
  FY2026 (est)         : Non-GAAP EPS ~$11.85 |  52wk $163-$286   |  Agentforce launch
  FY2027 (guided)      : Non-GAAP EPS ~$13.15 |  Current: ${CURRENT_PRICE:.2f}  |  13.4x forward
  Q1 FY2027 report     : May 27 2026           |  Guided $3.11-$3.13 non-GAAP EPS
""")

print("  B. EPP FLOOR & RATIO B")
print("  -----------------------------------------------------------------")
print(f"""
  EPS_NOW    = ${EPS_NOW:.2f}   (FY2026 non-GAAP diluted, estimated)
  EPP_MIN_PE = {EPP_MIN_PE}x       (below observed 24.6x Jan 2023 crisis floor; AI risk discount)
  EPP_NOW    = ${epp_now:.2f}  (= ${EPS_NOW:.2f} x {EPP_MIN_PE}x)
  EPP_status = *** CURRENT PRICE ${CURRENT_PRICE:.2f} is {abs(epp_gap_pct):.1f}% BELOW EPP FLOOR ***

  CONS_EPS_2YR = ${CONS_EPS_2YR:.2f}  (FY2027 management guidance; issued Feb 25 2026)
  CONS_EXIT_PE = {CONS_EXIT_PE}x       (conservative; below 35-50x historical; SaaS + AI discount)
  Price_B      = ${price_b:.2f}  (= ${CONS_EPS_2YR:.2f} x {CONS_EXIT_PE}x)
  Ratio_B      = {rfmt(ratio_b)}  -> {signal}  (negative = stock below EPP floor; strong BUY)
""")

print("  C. SCENARIO TABLE")
print("  -----------------------------------------------------------------")
print(f"  {'Scenario':<8}  {'EPS':>6}  {'Exit PE':>7}  {'Target':>8}  {'vs Current':>10}")
print("  " + "-" * 48)
for s in SCENARIOS:
    delta = (s[4] / CURRENT_PRICE - 1) * 100
    print(f"  {s[0]:<8}  ${s[2]:>5.2f}  {s[3]:>6}x  ${s[4]:>7.0f}  {delta:>+9.0f}%")
print()

print("  D. PROBABILITY DISTRIBUTION")
print("  -----------------------------------------------------------------")
print(f"""
  Market composite (inferred)  : {market_composite:.2f}  <- near BEAR centre (1.25); extreme fear
  SCA raw / adjusted           : {sca_raw:.3f} / {sca_adj:.3f}
  Model adj composite          : {adj_composite:.2f}
  Proxy EV (adj composite)     : ${proxy_ev:.0f}  ({(proxy_ev/CURRENT_PRICE-1)*100:+.1f}% vs current ${CURRENT_PRICE:.2f})
""")
labels = [s[0] for s in SCENARIOS]
print(f"  {'':8}  {'Mkt (raw)':>12}  {'Model (adj)':>12}")
print("  " + "-" * 36)
for i, lbl in enumerate(labels):
    print(f"  {lbl:<8}  {mkt_probs[i]*100:>10.1f}%  {probs[i]*100:>10.1f}%")
print()

print("  E. CROSS-READ SIGNALS (5 indicators -> composite)")
print("  -----------------------------------------------------------------")
header = f"  {'Signal':<42}  {'Wt':>4}  {'Bear':>6}  {'Base':>6}  {'Bull':>6}  {'XBull':>6}  {'Curr':>7}  {'Score':>5}"
print(header)
print("  " + "-" * (len(header) - 2))

def score_signal(bear, base, bull, xbull, current):
    pts = [(bear, 1.25), (base, 2.0), (bull, 2.75), (xbull, 3.75)]
    pts.sort(key=lambda x: x[0])
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    if current <= xs[0]:  return ys[0]
    if current >= xs[-1]: return ys[-1]
    for k in range(len(xs) - 1):
        if xs[k] <= current <= xs[k+1]:
            t = (current - xs[k]) / (xs[k+1] - xs[k])
            return ys[k] + t * (ys[k+1] - ys[k])
    return ys[-1]

scores = []
for cr in CROSS_READS:
    name, _, unit, bear, base, bull, xbull, current, weight = cr
    s = score_signal(bear, base, bull, xbull, current)
    scores.append((s, weight))
    short = name[:42]
    print(f"  {short:<42}  {weight:>4.0%}  {bear:>6}  {base:>6}  {bull:>6}  {xbull:>6}  {current:>7}  {s:>5.2f}")

weighted_composite = sum(s * w for s, w in scores)
print(f"\n  Weighted signal composite : {weighted_composite:.2f}  "
      f"(market inferred: {market_composite:.2f};  delta: {market_composite - weighted_composite:+.2f})")
print(f"  *** Market composite {market_composite:.2f} vs signal composite {weighted_composite:.2f}: market ignoring fundamentals ***")
print()

print("  F. STRUCTURAL COMPOSITE ADJUSTMENT (SCA)")
print("  -----------------------------------------------------------------")
print(f"  {'Factor':<60}  {'Rating':>6}  {'Wt':>4}")
print("  " + "-" * 74)
for name, rating, weight in STRUCTURAL_FACTORS:
    print(f"  {name:<60}  {rating:>+6.1f}  {weight:>4.0%}")
print(f"\n  SCA raw = {sca_raw:.3f}   SCA adj (div 2) = {sca_adj:.3f}")
print(f"  Market composite {market_composite:.2f}  +  SCA {sca_adj:.3f}  =  Model composite {adj_composite:.2f}")
print()

print("  G. EPS QUALITY DECOMP  (FY2023 ${:.2f} -> FY2026 ${:.2f} = +${:.2f})".format(
    PRE_MARGIN_EPS, EPS_NOW, eps_g_total))
print("  -----------------------------------------------------------------")
print(f"  {'Component':<60}  {'Share':>5}  {'Type':>10}")
print("  " + "-" * 79)
for name, sh, is_s in EPS_DECOMP:
    kind = "Structural" if is_s else "Cyclical"
    print(f"  {name:<60}  {sh:>5.0%}  {kind:>10}")
print(f"\n  Structural : ${struct_dollar:.2f}  ({struct_dollar/eps_g_total*100:.0f}%)")
print(f"  Cyclical   : ${cyclical_dollar:.2f}  ({cyclical_dollar/eps_g_total*100:.0f}%)")
print(f"  Total      : ${eps_g_total:.2f}")
print()

print("  H. RISK / RETURN SUMMARY")
print("  -----------------------------------------------------------------")
print(f"""
  Current price          : ${CURRENT_PRICE:.2f}  (near 52-week LOW of $163.52)
  EPP floor              : ${epp_now:.2f}  (current is {abs(epp_gap_pct):.1f}% BELOW floor -- only name below EPP)
  Method B target        : ${price_b:.0f}     (upside: +{(price_b/CURRENT_PRICE - 1)*100:.0f}%)
  BEAR scenario          : $119     (downside: -32%; AI seat-kill scenario)
  Ratio B                : {rfmt(ratio_b)}  -> {signal}
  FCF yield              : {fcf_yield:.1f}%   ($14.4B FCF; above risk-free rate)
  Buyback program        : $50B    (~29% of market cap; structural floor)
  Beta                   : {BETA:.2f}x  ({IDIO['idio_pct']}% idio / {IDIO['macro_pct']}% macro)
  Trailing P/E           : {trailing_pe:.1f}x  (FY2026 est. ${EPS_NOW:.2f}; decade-low multiple)
  Forward P/E            : {forward_pe:.1f}x  (FY2027 guided ${CONS_EPS_2YR:.2f})
  Implied 2-yr ann return: {cons_ret_ann:+.1f}%/yr  (to Method B ${price_b:.0f})
  Q1 FY2027 catalyst     : May 27 2026 (guided $3.11-$3.13 non-GAAP EPS)
  Exit discipline        : Agentforce ARR < 50% YoY or revenue < 8% -> re-evaluate
""")

print("  I. IDIOSYNCRATIC vs MACRO DRIVERS")
print("  -----------------------------------------------------------------")
print(f"  Beta: {IDIO['beta']:.2f}x  |  Idiosyncratic: {IDIO['idio_pct']}%  |  Macro: {IDIO['macro_pct']}%\n")
print(f"  {'Driver':<50}  {'Type':>5}  {'Wt':>4}  Note")
print("  " + "-" * 92)
for driver, kind, wt, note in IDIO["drivers"]:
    print(f"  {driver:<50}  {kind:>5}  {wt:>4.0%}  {note}")
print()
print("=" * 72)
print("  END OF REPORT -- CRM  |  Generated 2026-05-21")
print("=" * 72)
