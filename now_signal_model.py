"""
ServiceNow, Inc. (NOW) — Bottom-Up Risk/Reward Signal Model
============================================================
Analysis date : 2026-05-22
Fiscal year   : Calendar year (Jan 1 – Dec 31)
Split note    : 5-for-1 stock split effective Dec 18 2025; all prices / EPS split-adjusted
Price source  : Yahoo Finance / CNBC, 2026-05-22; intraday $98.11–$100.80;
                52-wk range $81.24–$211.48 (ATH area); down 52% from peak
"""

# ── 0. DEPENDENCIES ──────────────────────────────────────────────────────────
import math

# ── 1. CORE INPUTS ───────────────────────────────────────────────────────────
TICKER        = "NOW"
COMPANY       = "ServiceNow, Inc."
ANALYSIS_DATE = "2026-05-22"

CURRENT_PRICE = 100.58   # NOW — fetched Yahoo Finance / CNBC, 2026-05-22
                          # intraday $98.11–$100.80; post 5-for-1 split (Dec 18 2025)
                          # 52-wk low $81.24 — 52-wk high $211.48; down 52% from ATH

# Non-GAAP EPS (diluted, split-adjusted; excludes SBC + amortisation)
# Note: GAAP EPS ~$1.80E (FY2026) vs non-GAAP $4.00E; SBC ~$2.20/sh is real dilution
# Split-adjusted history:
#   FY2023 : ~$2.46  (pre-split $12.30 ÷ 5)
#   FY2024 : ~$3.41  (pre-split $17.05 ÷ 5)
#   FY2025 : $3.51   (Q4 2025 $0.92; full year confirmed; stock -40% despite beat)
#   FY2026 : ~$4.00E (Q1 actual $0.97; Q2 guided ~$0.85 Armis drag; H2 recovery)
#   FY2027E: $5.04   (consensus, 49 analysts; 26% YoY; revenue $19.16B)
#   FY2028E: ~$6.15  (22% YoY CAGR on FY2024–FY2027 pace; ~$5.04 × 1.22)
EPS_TROUGH        = 3.51   # FY2025 (last completed FY; trough relative to ATH)
EPS_TROUGH_PRICE  = 81.24  # 52-wk low (recent correction bottom; observed 23.1x trough PE)
EPP_MIN_PE        = 22     # structural floor; just below observed 23.1x trough;
                            # mission-critical workflow moat justifies 22x minimum
EPS_NOW           = 4.00   # FY2026E (Q1 actual $0.97 + 3Q avg ~$1.01; mgmt 31.5% margin)
EPS_FWD_CONSENSUS = 5.04   # FY2027 consensus (49 analysts; ~$19B revenue; 18–20% growth)
CONS_EPS_2YR      = 6.15   # FY2028E (~30 months out; 22% YoY from $5.04; cloud scale)
CONS_EXIT_PE      = 35     # 2-yr exit; historically 50–100x; 35x = conservative re-rating
                            # from current 25x to a still-below-historical-average multiple

BETA  = 1.35   # high-growth SaaS; elevated beta; macro + AI sentiment swings
IDIO  = 0.65   # idiosyncratic: agentic AI thesis, RPO backlog, mission-critical moat
MACRO = 0.35   # macro: enterprise IT spending cycle, rate sensitivity

# ── 2. SCENARIO MATRIX ───────────────────────────────────────────────────────
# BEAR  : Agentic AI (OpenAI/Anthropic toolkits) commoditises workflow automation;
#         enterprise IT freeze; FY2028 non-GAAP EPS $3.20 at 22x panic PE = $70
# BASE  : Consensus path — Agentic AI BOOSTS ServiceNow (Now Assist ARR ramps);
#         FY2028 $6.15 EPS at 35x partial re-rating = $215
# BULL  : ServiceNow = Enterprise AI OS; all IT/HR/Legal/Finance workflows agentified;
#         $8.50 FY2028 EPS at 44x premium = $374
# XBULL : ServiceNow captures enterprise AI orchestration layer (Agent Studio);
#         $12.00 FY2028 EPS at 52x peak = $624

SCENARIOS = {
    "BEAR":  {"eps": 3.20,  "pe": 22,   "price": round(3.20 *22,   0)},
    "BASE":  {"eps": 6.15,  "pe": 35,   "price": round(6.15 *35,   0)},
    "BULL":  {"eps": 8.50,  "pe": 44,   "price": round(8.50 *44,   0)},
    "XBULL": {"eps": 12.00, "pe": 52,   "price": round(12.00*52,   0)},
}

# ── 3. STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────
STRUCTURAL_FACTORS = [
    {
        "name":   "Agentic AI platform (Now Assist + Agent Studio)",
        "detail": "ServiceNow is building Agentic AI natively INTO the workflow platform — "
                  "not competing with it; Now Assist on platform integrates LLMs for "
                  "autonomous IT/HR/CSM ticket resolution; Agent Studio for custom agents; "
                  "first movers deploying 100s of simultaneous AI agents in enterprise",
        "rating": +1.1, "weight": 0.25,
    },
    {
        "name":   "$27.7B RPO backlog + 21% cRPO growth",
        "detail": "Remaining Performance Obligations $27.7B (+23.5% CC YoY); "
                  "current RPO $12.64B (+21% CC) = 3+ quarters locked revenue; "
                  "multi-year enterprise contracts; 99%+ Fortune 500 penetration",
        "rating": +0.9, "weight": 0.20,
    },
    {
        "name":   "ITSM/HRSD/CSM mission-critical moat",
        "detail": "ServiceNow runs the IT operations of 85%+ of the Global 2000; "
                  "platform is the system of record for incident/change/problem mgmt; "
                  "switching cost is enormous — full enterprise re-implementation required; "
                  "NRR consistently >120%; net new ACV accelerating with AI upsell",
        "rating": +0.7, "weight": 0.20,
    },
    {
        "name":   "Agentic AI disruption risk (OpenAI / Anthropic toolkits)",
        "detail": "Fear that LLM providers build workflow orchestration directly, "
                  "bypassing the ServiceNow platform layer; Microsoft Copilot Studio "
                  "competes in the same space; if agentic AI becomes a commodity API, "
                  "SaaS platforms lose pricing power on automation features",
        "rating": -0.9, "weight": 0.20,
    },
    {
        "name":   "Armis acquisition margin headwind + integration risk",
        "detail": "Armis (IoT/OT security) acquisition closed Q1 2026; adding 125 bps "
                  "to revenue but dragging Q2 2026 operating margin to 26.5% (-500 bps); "
                  "integration complexity; ~$0.15/sh FY2026 EPS headwind from amortisation",
        "rating": -0.4, "weight": 0.15,
    },
]

# ── 4. ENGINE — do not modify below this line ────────────────────────────────
def compute_sca(factors):
    raw = sum(f["rating"] * f["weight"] for f in factors)
    adj = raw / 2.0
    return raw, adj

def softmax_prob(scenarios, composite, T=0.60):
    keys    = list(scenarios.keys())
    centres = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    logits  = {k: -((composite - centres[k])**2) / T for k in keys}
    max_l   = max(logits.values())
    exp_    = {k: math.exp(logits[k] - max_l) for k in keys}
    total   = sum(exp_.values())
    return {k: exp_[k] / total for k in keys}

def infer_composite(scenarios, target_price, T=0.60):
    keys = list(scenarios.keys())
    lo, hi = 1.0, 4.0
    for _ in range(60):
        mid   = (lo + hi) / 2
        probs = softmax_prob(scenarios, mid, T)
        ev    = sum(probs[k] * scenarios[k]["price"] for k in keys)
        if ev < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

def signal_from_ratio(r):
    if r is None:
        return "✕ AVOID",      "AVOID",      "#f87171"
    if r < 0.75:
        return "◉ BUY",        "BUY",        "#22c55e"
    if r < 1.10:
        return "◎ ACCUMULATE", "ACCUMULATE", "#f0b429"
    if r < 1.75:
        return "◐ WATCHLIST",  "WATCHLIST",  "#60a5fa"
    if r < 2.50:
        return "▷ HOLD/TRIM",  "HOLD",       "#a78bfa"
    return "✕ AVOID",          "AVOID",      "#f87171"

# ── 5. CALCULATIONS ──────────────────────────────────────────────────────────
epp         = EPS_NOW * EPP_MIN_PE
epp_gap_pct = (CURRENT_PRICE - epp) / epp * 100

price_b = CONS_EPS_2YR * CONS_EXIT_PE
if price_b > CURRENT_PRICE:
    ratio_b   = (CURRENT_PRICE - epp) / (price_b - CURRENT_PRICE)
    ratio_str = f"{ratio_b:.2f}x"
else:
    ratio_b   = None
    ratio_str = "N/A"

signal_label, signal_short, signal_color = signal_from_ratio(ratio_b)

sca_raw, sca_adj = compute_sca(STRUCTURAL_FACTORS)

market_composite = infer_composite(SCENARIOS, CURRENT_PRICE)
adj_composite    = market_composite + sca_adj
signal_probs     = softmax_prob(SCENARIOS, adj_composite)
proxy_ev         = sum(signal_probs[k] * SCENARIOS[k]["price"] for k in SCENARIOS)
proxy_gap_pct    = (proxy_ev - CURRENT_PRICE) / CURRENT_PRICE * 100

trailing_pe = CURRENT_PRICE / EPS_NOW
forward_pe  = CURRENT_PRICE / EPS_FWD_CONSENSUS
trough_pe   = EPS_TROUGH_PRICE / EPS_TROUGH

# Q1 FY2026 actual beat: $0.97 vs $0.55 estimate
Q1_ACTUAL    = 0.97
Q1_ESTIMATE  = 0.55
Q1_REV_B     = 3.77
Q1_RPO_B     = 27.7
Q1_CRPO_B    = 12.64

# EPS decomp: FY2025 $3.51 → FY2026E $4.00 = +$0.49
PRE_AI_EPS   = EPS_TROUGH   # FY2025 anchor (pre-Agentic-AI-monetisation)
eps_g_total  = EPS_NOW - PRE_AI_EPS

EPS_COMPONENTS = [
    {"label": "Subscription ACV expansion (new logos + upsell)",
     "detail": "Pro Plus → Enterprise tiers; net new ACV accelerating; "
               "20%+ subscription growth sustaining on large installed base",
     "share": 0.40, "type": "Structural"},
    {"label": "Now Assist AI premium uplift",
     "detail": "Generative AI SKUs (Now Assist) added ~$0.50B ARR in 2025; "
               "enterprise AI agents = premium pricing layer on base platform",
     "share": 0.25, "type": "Structural"},
    {"label": "Operating leverage on 31.5% non-GAAP margin",
     "detail": "Revenue outgrowing cost base; headcount efficiency from internal AI; "
               "G&A leverage; target 32–33% margin by FY2027",
     "share": 0.20, "type": "Structural"},
    {"label": "Share buyback / dilution management",
     "detail": "NOW approx 1B shares outstanding post-split; buybacks partially "
               "offsetting SBC dilution; modest EPS accretion",
     "share": 0.10, "type": "Structural"},
    {"label": "Armis acquisition EPS drag (partially temporal)",
     "detail": "Armis adds ~125bps revenue contribution but ~500bps margin drag "
               "in Q2 2026; integration costs + amortisation reduce FY2026 EPS ~$0.15",
     "share": 0.05, "type": "Temporal"},
]
structural_pct = sum(c["share"] for c in EPS_COMPONENTS if c["type"] == "Structural") * 100
cyclical_pct   = 100 - structural_pct

idio_drivers = [
    ("Now Assist AI agents ARR growth rate", "IDIO", "25%",
     "AI agent SKU ARR growth YoY is the key leading indicator for platform premium"),
    ("Net new ACV and large-deal momentum (>$1M TCV)", "IDIO", "20%",
     "Large-deal pipeline is a leading indicator; Middle East delays in Q1 watched"),
    ("Armis integration & IoT/OT security cross-sell", "IDIO", "20%",
     "Must prove Armis security data enriches the platform; cross-sell to base"),
    ("Enterprise IT spending cycle / budget freeze", "MACRO", "20%",
     "ServiceNow is IT budget line item; CFO pressure slows expansions/new logos"),
    ("AI disruption narrative / sentiment on SaaS multiples", "MACRO", "15%",
     "Fear of OpenAI/Anthropic tool-kit bypass is the PRIMARY multiple depressor"),
]

# ── 6. REPORT OUTPUT ─────────────────────────────────────────────────────────
W = 72
def hdr(title): return f"\n{'='*W}\n  {title}\n{'='*W}"
def sub(title): return f"\n  {title}\n  {'-'*(W-2)}"

print(hdr(f"PART 1 — FRAMEWORK OVERVIEW  |  {TICKER}  |  {COMPANY}"))
print(f"""
  Bottom-Up Risk/Reward (EPP / Ratio-B / Softmax) applied to {COMPANY}.

  Three pillars:
  1. EPP Floor     — structural downside anchor  (EPS × min-viable trough P/E)
  2. Method B      — 2-yr consensus earnings power target (EPS × exit P/E)
  3. Ratio B       — primary signal: (price − EPP) / (Method B − price)
                     <0.75 BUY | 0.75–1.1 ACCUMULATE | 1.1–1.75 WATCHLIST
                     1.75–2.5 HOLD | >2.5 AVOID

  Company : {COMPANY}
  Sector  : Enterprise SaaS · Workflow Automation · Agentic AI Platform
  FY end  : December 31  (calendar year)
  Split   : 5-for-1 effective Dec 18 2025; all prices / EPS split-adjusted
  Price   : ${CURRENT_PRICE:.2f}  [{ANALYSIS_DATE}]
  52-week : ${EPS_TROUGH_PRICE:.2f} low – $211.48 high  (ATH area; down 52% from peak)
""")

print(hdr(f"PART 2 — ANALYST COMMENTARY  |  {TICKER}"))

print(sub("A. INVESTMENT THESIS"))
print(f"""
  ServiceNow is the operating system for enterprise workflows — running the IT
  operations, HR processes, customer service, and legal workflows of 85%+ of the
  Global 2000.  The platform's moat is structural: replacing ServiceNow requires
  re-implementing the entire workflow layer of a Fortune 500 enterprise, a
  multi-year, $50–200M+ undertaking.  Net revenue retention consistently >120%.

  Q1 2026: Revenue $3.77B (+22% YoY); non-GAAP EPS $0.97 (vs $0.55 estimated —
  a 76% beat).  RPO $27.7B (+23.5% CC).  FY2026 subscription guidance raised.

  Yet the stock sits at ${CURRENT_PRICE:.2f} — 52% below the ATH of $211.48 — as the
  market prices a dystopian scenario where OpenAI/Anthropic toolkits commoditise
  workflow automation, rendering the ServiceNow platform redundant.

  This thesis is largely inverted.  Agentic AI REQUIRES a workflow orchestration
  layer — exactly what ServiceNow provides.  Now Assist and Agent Studio position
  NOW as the enterprise agentic AI deployment platform, not its victim.  The
  same dynamics played out with the cloud transition: fear that SaaS would be
  disrupted by cloud actually made SaaS more valuable.

  At ${CURRENT_PRICE:.2f}, NOW trades at {trailing_pe:.1f}x FY2026E non-GAAP EPS and {forward_pe:.1f}x
  FY2027E — the lowest forward multiple since 2018 for this platform.  37 of 45
  analysts rate it Strong Buy with an average price target of $142.77.

  Signal: {signal_label}  |  Ratio B: {ratio_str}  |  EPP gap: +{epp_gap_pct:.1f}%
""")

print(sub("B. EARNINGS POWER PRICE (EPP) — STRUCTURAL FLOOR"))
print(f"""
  EPS anchor   : FY2025 non-GAAP ${EPS_TROUGH:.2f}  (split-adj.; last completed FY;
                  Q4 2025: $0.92; stock fell 16% in April despite beats)
  Bear trough  : ${EPS_TROUGH_PRICE:.2f}  (52-wk low; trough of 52% ATH correction)
  Observed PE  : ${EPS_TROUGH_PRICE:.2f} / ${EPS_TROUGH:.2f} = {trough_pe:.1f}x  (recent trough multiple)
  EPP min PE   : {EPP_MIN_PE}x  (below observed {trough_pe:.1f}x trough; mission-critical SaaS
                  platform with 99%+ Fortune 500 penetration warrants 22x floor)

  EPS now      : ${EPS_NOW:.2f}  (FY2026E; Q1 actual $0.97; Q2–Q4 avg ~$1.01; mgmt guidance)
  EPP floor    : ${EPS_NOW:.2f} × {EPP_MIN_PE}x = ${epp:.2f}
  Current vs EPP: ${CURRENT_PRICE:.2f} vs ${epp:.2f}  (+{epp_gap_pct:.1f}% above floor)

  GAAP note: FY2026E GAAP EPS ~$1.80 (vs non-GAAP $4.00); SBC is ~$2.20/sh —
  real economic dilution.  Non-GAAP used for cross-coverage consistency.
  EPP at {EPP_MIN_PE}x × $1.80 GAAP = $39.60; current price is well above GAAP floor.
""")

print(sub("C. METHOD B — 2-YEAR EARNINGS POWER TARGET"))
print(f"""
  CONS_EPS_2YR : ${CONS_EPS_2YR:.2f}  (FY2028E; ~30 months out; 22% YoY from FY2027 $5.04;
                  consensus revenue $19.16B FY2027 → ~$23B FY2028; margin expansion)
  CONS_EXIT_PE : {CONS_EXIT_PE}x  (historically 50–100x; 35x = deeply conservative;
                  just a partial re-rating from current {trailing_pe:.1f}x to below historical avg)
  Method B     : ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x = ${price_b:.0f}

  Ratio B = (${CURRENT_PRICE:.2f} − ${epp:.2f}) / (${price_b:.0f} − ${CURRENT_PRICE:.2f})
           = ${CURRENT_PRICE-epp:.2f} / ${price_b-CURRENT_PRICE:.2f}
           = {ratio_str}  →  {signal_label}

  Sensitivity to exit PE (at CONS_EPS_2YR ${CONS_EPS_2YR:.2f}):
    CONS_EXIT_PE = 28x → Price_B $172 → Ratio B 0.18x  (BUY)
    CONS_EXIT_PE = 35x → Price_B $215 → Ratio B 0.11x  (BUY)  ← base case
    CONS_EXIT_PE = 45x → Price_B $277 → Ratio B 0.07x  (BUY)
    CONS_EXIT_PE = 55x → Price_B $338 → Ratio B 0.05x  (BUY)
  Signal is robustly BUY across all plausible exit multiples.  Even 20x exit
  gives Price_B $123 — still +22% upside with a BUY signal.
""")

print(sub("D. SCENARIO ANALYSIS"))
print(f"  {'Scenario':<8}  {'EPS':>6}  {'P/E':>6}  {'Price':>7}  {'vs Now':>8}  Description")
print(f"  {'-'*70}")
descs = {
    "BEAR":  "Agentic AI toolkits commoditise workflow; IT freeze; 22x panic",
    "BASE":  "Consensus FY2028 $6.15; Now Assist ramps; 35x conservative exit",
    "BULL":  "NOW = Enterprise AI OS; all workflows agentified; 44x re-rate",
    "XBULL": "NOW captures enterprise agentic orchestration market; 52x peak",
}
for k, s in SCENARIOS.items():
    diff = (s["price"] - CURRENT_PRICE) / CURRENT_PRICE * 100
    sign = "+" if diff >= 0 else ""
    print(f"  {k:<8}  ${s['eps']:>5.2f}  {s['pe']:>5.1f}x  ${s['price']:>6.0f}  "
          f"{sign}{diff:>6.1f}%  {descs[k]}")
print(f"""
  BASE scenario ${SCENARIOS['BASE']['price']:.0f} = Method B target (by construction).
  BEAR at ${SCENARIOS['BEAR']['price']:.0f} is below the 52-week low — requires both EPS decline AND
  multiple compression from current levels; unlikely without severe recession + AI disruption.
""")

print(sub("E. SOFTMAX MARKET COMPOSITE"))
print(f"""
  Market composite  (inferred from ${CURRENT_PRICE:.2f}): {market_composite:.3f}
  SCA adjustment                                : +{sca_adj:.3f}
  Model composite                               : {adj_composite:.3f}

  Scenario probabilities (model):""")
for k, p in signal_probs.items():
    bar = "█" * int(p * 40)
    print(f"    {k:<6}  {p*100:5.1f}%  {bar}")
print(f"""
  Model EV (proxy) : ${proxy_ev:.0f}  ({proxy_gap_pct:+.1f}% vs current ${CURRENT_PRICE:.2f})

  Interpretation: Market is pricing maximum BEAR fear — agentic AI disruption
  narrative dominates despite Q1 2026 beating estimates by 76%.  The SCA-adjusted
  model composite re-weights toward BASE/BULL, generating a large positive EV gap.
  The {proxy_gap_pct:+.0f}% model EV implies this is the most mispriced name in the
  high-growth segment of the coverage universe.
""")

print(sub("F. STRUCTURAL COMPOSITE ADJUSTMENT (SCA)"))
print(f"""  {'Factor':<60}  {'Rating':>6}  {'Wt':>4}""")
print(f"  {'-'*74}")
for f in STRUCTURAL_FACTORS:
    full = f"{f['name']}  ({f['detail'][:78]})"
    print(f"  {full[:72]:<72}  {f['rating']:>+5.1f}  {f['weight']*100:.0f}%")
print(f"""
  SCA raw = {sca_raw:.3f}   SCA adj (div 2) = {sca_adj:.3f}
  Market composite {market_composite:.2f}  +  SCA {sca_adj:.3f}  =  Model composite {adj_composite:.2f}
""")

print(sub(f"G. EPS QUALITY DECOMP  "
          f"(FY2025 ${PRE_AI_EPS:.2f} → FY2026E ${EPS_NOW:.2f} = +${eps_g_total:.2f})"))
print(f"""  {'Component':<60}  {'Share':>6}  {'Type':>12}""")
print(f"  {'-'*81}")
for c in EPS_COMPONENTS:
    label = f"{c['label']}  ({c['detail'][:58]})"
    print(f"  {label[:72]:<72}  {c['share']*100:.0f}%  {c['type']:>12}")
print(f"""
  Structural : ${eps_g_total * structural_pct/100:.2f}  ({structural_pct:.0f}%)
  Temporal   : ${eps_g_total * cyclical_pct/100:.2f}   ({cyclical_pct:.0f}%)
  Total      : ${eps_g_total:.2f}

  Note: $0.49 is the FY2025→FY2026 step.  The FULL earnings thesis is the
  FY2026→FY2028 compounding: $4.00 → $6.15 = +54%.  The platform's operating
  leverage is the structural driver; Armis is a temporary drag in 2026.
""")

print(hdr(f"PART 3 — NUMBERS & SIGNALS   |  {TICKER}"))

print(sub("H. RISK / RETURN SUMMARY"))
print(f"""
  Current price       : ${CURRENT_PRICE:.2f}  (52-wk low ${EPS_TROUGH_PRICE:.2f}; –52% from $211.48 ATH)
  EPP floor           : ${epp:.2f}  (+{epp_gap_pct:.1f}% above floor; 22x × ${EPS_NOW:.2f} FY2026E)
  Method B target     : ${price_b:.0f}  (upside: +{(price_b/CURRENT_PRICE-1)*100:.0f}%)
  BEAR scenario       : ${SCENARIOS['BEAR']['price']:.0f}  (downside: {(SCENARIOS['BEAR']['price']/CURRENT_PRICE-1)*100:.0f}%; AI disruption + freeze)
  Ratio B             : {ratio_str}  -> {signal_label}
  Trailing P/E        : {trailing_pe:.1f}x non-GAAP / ~55x GAAP  (FY2026E)
  Forward P/E         : {forward_pe:.1f}x non-GAAP  (FY2027 consensus ${EPS_FWD_CONSENSUS:.2f})
  5-for-1 split date  : Dec 18 2025  (all prices / EPS above are split-adjusted)
  Q1 2026 beat        : Non-GAAP EPS $0.97 vs $0.55 estimate (+76%); revenue $3.77B vs $3.74B
  RPO                 : $27.7B  (+23.5% CC); cRPO $12.64B (+21% CC; 1 bp above guidance)
  Now Assist AI       : 1B+ daily AI interactions; Agent Studio for custom enterprise agents
  FY2026 sub revenue  : $15.735–$15.775B guidance (+20.5–21% CC; raised Q1)
  Armis headwind      : ~125 bps to revenue; ~500 bps margin drag Q2 2026; recovers H2
  Analyst consensus   : 37/45 Strong Buy; avg price target $142.77 (+42% from current)
  Q2 2026 catalyst    : ~Jul 22 2026 (cRPO growth and operating margin are key metrics)
  BUY thesis breaks if: RPO growth decelerates below 15% CC, OR Now Assist fails to
                        monetise (zero incremental ARR from AI SKUs by Q3 2026), OR
                        Microsoft Copilot wins >5% of ITSM seats from ServiceNow base.
""")

print(sub("I. IDIOSYNCRATIC vs MACRO DRIVERS"))
print(f"""  Beta: {BETA:.2f}x  |  Idiosyncratic: {IDIO*100:.0f}%  |  Macro: {MACRO*100:.0f}%
""")
print(f"  {'Driver':<52}  {'Type':>5}  {'Wt':>4}  Note")
print(f"  {'─'*92}")
for d, typ, wt, note in idio_drivers:
    print(f"  {d:<52}  {typ:>5}  {wt:>4}  {note[:60]}")

print(f"""
{'='*W}
  END OF REPORT -- {TICKER}  |  Generated {ANALYSIS_DATE}
{'='*W}
""")
