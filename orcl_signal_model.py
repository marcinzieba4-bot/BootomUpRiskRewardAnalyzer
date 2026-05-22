"""
Oracle Corporation (ORCL) — Bottom-Up Risk/Reward Signal Model
==============================================================
Analysis date : 2026-05-22
Fiscal year   : June 1 – May 31 (FY2026 = Jun 2025 – May 2026; Q4 ends May 31 2026)
Price source  : Yahoo Finance / CNN Markets, 2026-05-22, intraday $187.20–$192.00
"""

# ── 0. DEPENDENCIES ──────────────────────────────────────────────────────────
import math

# ── 1. CORE INPUTS ───────────────────────────────────────────────────────────
TICKER        = "ORCL"
COMPANY       = "Oracle Corporation"
ANALYSIS_DATE = "2026-05-22"

CURRENT_PRICE = 189.50   # ORCL — fetched from Yahoo Finance / CNN Markets, 2026-05-22
                          # intraday range $187.20–$192.00; 52-wk range $134.57–$345.72

# Non-GAAP EPS (fully diluted, normalised)
# FY2022 (ended May 2022) — last pre-cloud-inflection baseline
# FY2025 (ended May 2025) — $6.03 (Q1$1.39+Q2$1.47+Q3$1.47+Q4$1.70)
# FY2026 normalised excl. Q2 Ampere Computing one-time gain (~$0.77/sh):
#   Reported: Q1$1.47+Q2$2.26+Q3$1.79+Q4E$1.98 = $7.50
#   Normalised: $1.47+$1.49+$1.79+$1.98 = $6.73
EPS_TROUGH        = 4.90   # FY2022 non-GAAP, pre-cloud-inflection anchor
EPS_TROUGH_PRICE  = 63.0   # Sept 2022 tech bear-market trough (~12.9x trough P/E)
EPP_MIN_PE        = 16     # structural floor PE; between 2022 shock-low 13x and 2025
                            # correction trough 22x; cloud recurring-revenue moat premium
EPS_NOW           = 6.73   # normalised FY2026 (excl. non-recurring Ampere sale $0.77/sh)
EPS_FWD_CONSENSUS = 8.16   # FY2027 consensus, 49 analysts, avg target $248-$260
CONS_EPS_2YR      = 10.00  # FY2028 est. (~24 months; 23% YoY growth from $8.16 FY2027)
CONS_EXIT_PE      = 28     # 2-yr exit multiple; conservative for 20%+ grower

BETA  = 1.15   # high-beta cloud infrastructure; moderating as OCI revenues scale
IDIO  = 0.55   # idiosyncratic weight
MACRO = 0.45   # macro weight

# ── 2. SCENARIO MATRIX ───────────────────────────────────────────────────────
# BEAR  : Cloud growth stalls; AWS/Azure pricing war; OCI ramp disappoints;
#         FY2028 EPS $5.50 on $60B revenue; market re-rates to 14x trough
# BASE  : Management FY2027 $80B revenue path; FY2028 $10 EPS at 28x exit
# BULL  : FY2027 $90B revenue (management target) + margin expansion;
#         FY2028 $14 EPS at 35x premium AI-infrastructure multiple
# XBULL : AI supercluster dominance + multi-cloud adoption surge;
#         FY2028 $20 EPS (30%+ margins on $100B+ revenue) at 42.5x

SCENARIOS = {
    "BEAR":  {"eps": 5.50,  "pe": 14,   "price": round(5.50 *14,   0)},
    "BASE":  {"eps": 10.00, "pe": 28,   "price": round(10.00*28,   0)},
    "BULL":  {"eps": 14.00, "pe": 35,   "price": round(14.00*35,   0)},
    "XBULL": {"eps": 20.00, "pe": 42.5, "price": round(20.00*42.5, 0)},
}

# ── 3. STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────
STRUCTURAL_FACTORS = [
    {
        "name":   "OCI AI hyperscaler momentum",
        "detail": "Q3 FY2026: OCI revenue +84% YoY to $4.9B; GPU clusters booked by Nvidia/Meta/Uber; "
                  "AI training + inference workloads; remaining performance obligations +438% to $523B",
        "rating": +1.0, "weight": 0.25,
    },
    {
        "name":   "$523B RPO backlog",
        "detail": "Remaining performance obligations equal ~1x market cap — unprecedented revenue "
                  "visibility; multi-year hyperscaler contracts; customer lock-in via multi-cloud "
                  "Exadata, Autonomous DB, and sovereign cloud deployments",
        "rating": +0.9, "weight": 0.20,
    },
    {
        "name":   "Legacy Oracle DB + middleware ecosystem moat",
        "detail": "$20B+ annual license/support base; Oracle Database migration to OCI Autonomous DB "
                  "is sticky and drives OCI adoption; Java/middleware licensing creates enterprise "
                  "switching costs — largest enterprise software installed base globally",
        "rating": +0.7, "weight": 0.20,
    },
    {
        "name":   "Massive $50B capex / near-term FCF compression",
        "detail": "FY2026 capex guidance $50B (vs. $8B in FY2024); OCI data-centre buildout funded "
                  "by debt; free cash flow compressed 40–60% near term; debt/EBITDA elevated at ~3x; "
                  "execution risk on simultaneous multi-geography hyperscale buildout",
        "rating": -0.8, "weight": 0.20,
    },
    {
        "name":   "Cloud market share gap vs AWS / Azure / GCP",
        "detail": "OCI ~5% global cloud IaaS share vs. AWS 31%, Azure 24%, GCP 12%; late-mover "
                  "disadvantage; hyperscalers deploying own custom silicon (Graviton, Trainium, TPU); "
                  "customers may limit OCI concentration; price-war risk in commodity compute",
        "rating": -0.5, "weight": 0.15,
    },
]

# ── 4. ENGINE — do not modify below this line ────────────────────────────────
def compute_sca(factors):
    raw = sum(f["rating"] * f["weight"] for f in factors)
    adj = raw / 2.0
    return raw, adj

def softmax_prob(scenarios, composite, T=0.60):
    keys   = list(scenarios.keys())
    centres = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    logits = {k: -((composite - centres[k])**2) / T for k in keys}
    max_l  = max(logits.values())
    exp_   = {k: math.exp(logits[k] - max_l) for k in keys}
    total  = sum(exp_.values())
    return {k: exp_[k] / total for k in keys}

def infer_composite(scenarios, target_price, T=0.60):
    """Binary-search market composite that matches target_price via EV."""
    keys    = list(scenarios.keys())
    prices  = [scenarios[k]["price"] for k in keys]
    lo, hi  = 1.0, 4.0
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
        return "✕ AVOID", "AVOID", "#f87171"
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
epp        = EPS_NOW * EPP_MIN_PE
epp_gap_pct = (CURRENT_PRICE - epp) / epp * 100

price_b    = CONS_EPS_2YR * CONS_EXIT_PE
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

div_per_share = 0.40 * 4        # quarterly $0.40 (annualised)
div_yield     = div_per_share / CURRENT_PRICE * 100

# EPS decomposition: FY2022 $4.90 → FY2026 normalised $6.73 = +$1.83
PRE_CLOUD_EPS   = EPS_TROUGH   # FY2022 anchor (pre-OCI-inflection)
eps_g_total     = EPS_NOW - PRE_CLOUD_EPS   # $1.83

EPS_COMPONENTS = [
    {"label": "OCI / cloud revenue acceleration",
     "detail": "OCI IaaS/PaaS revenue $0→$20B+ run-rate; GPU clusters; AI training; "
               "multi-cloud enterprise agreements",
     "share": 0.40, "type": "Structural"},
    {"label": "Legacy DB + apps migration to OCI",
     "detail": "Oracle Autonomous DB, Fusion ERP, NetSuite SaaS — pulling licence base "
               "onto OCI; margin-accretive SaaS transition",
     "share": 0.25, "type": "Structural"},
    {"label": "Share buyback EPS accretion",
     "detail": "~$10B/yr buybacks (~3-4% share reduction/yr over 4 years); "
               "diluted share count from ~2.95B FY2022 to ~2.76B FY2026",
     "share": 0.20, "type": "Structural"},
    {"label": "FX normalisation",
     "detail": "2022 record-strong USD was a ~3-4% revenue/EPS headwind; "
               "normalisation contributed to reported USD EPS recovery 2023-2026",
     "share": 0.10, "type": "Temporal"},
    {"label": "Cerner integration overhead normalisation",
     "detail": "Acquired Jun 2022 for $28B; one-time integration costs wound down "
               "2023-2025; margin expansion as synergies realised",
     "share": 0.05, "type": "Temporal"},
]
structural_pct  = sum(c["share"] for c in EPS_COMPONENTS if c["type"] == "Structural") * 100
cyclical_pct    = 100 - structural_pct

idio_drivers = [
    ("OCI AI workload adoption pace (GPU utilisation → revenue)", "IDIO", "25%",
     "Measured by OCI quarterly revenue growth rate; $523B RPO must convert"),
    ("Autonomous DB penetration + Oracle DB cloud migration", "IDIO", "20%",
     "Customer migration of on-prem Oracle DB to OCI; sticky but slow-moving"),
    ("Cerner healthcare cloud monetisation", "IDIO", "10%",
     "Oracle Health (Cerner); government/hospital digital health; long-cycle deals"),
    ("Enterprise IT capex cycle / cloud spend", "MACRO", "25%",
     "Enterprises curtailing spend = OCI new logo slowdown; key cyclical lever"),
    ("Interest rates / WACC / tech valuation multiple", "MACRO", "20%",
     "Oracle ~$85B debt from Cerner + capex; higher rates = FCF pressure + multiple compression"),
]

# ── 6. REPORT OUTPUT ─────────────────────────────────────────────────────────
W = 72
def hdr(title): return f"\n{'='*W}\n  {title}\n{'='*W}"
def sub(title): return f"\n  {title}\n  {'-'*(W-2)}"

print(hdr(f"PART 1 — FRAMEWORK OVERVIEW  |  {TICKER}  |  {COMPANY}"))
print(f"""
  This model applies the Bottom-Up Risk/Reward (EPP / Ratio-B / Softmax)
  framework to {COMPANY} ({TICKER}).

  Three pillars:
  1. EPP Floor     — structural downside anchor  (EPS × min-viable trough P/E)
  2. Method B      — 2-yr consensus earnings power target (EPS × exit P/E)
  3. Ratio B       — primary signal: (price − EPP) / (Method B − price)
                     <0.75 BUY | 0.75–1.1 ACCUMULATE | 1.1–1.75 WATCHLIST
                     1.75–2.5 HOLD | >2.5 AVOID

  Company : {COMPANY}
  Sector  : Enterprise Cloud Infrastructure · Database · AI Compute Platform
  FY end  : May 31  (FY2026 = Jun 2025 – May 2026; Q4 ends May 31 2026)
  Price   : ${CURRENT_PRICE:.2f}  [{ANALYSIS_DATE}]
  52-week : $134.57 low – $345.72 high  (currently –45% off all-time highs)
""")

print(hdr(f"PART 2 — ANALYST COMMENTARY  |  {TICKER}"))

print(sub("A. INVESTMENT THESIS"))
print(f"""
  Oracle is executing the most dramatic cloud transition among legacy enterprise
  software vendors.  OCI (Oracle Cloud Infrastructure) grew +84% YoY in Q3
  FY2026, driven by AI GPU cluster deployments from Nvidia, Meta, and large
  enterprises.  The company's remaining performance obligations (RPO) surged
  438% to $523 billion — a figure roughly equal to Oracle's entire market cap
  — providing unprecedented multi-year revenue visibility.

  Yet the stock trades at ${CURRENT_PRICE:.2f}, down 45% from its $345 peak
  (Sep 2024), primarily because:
  (1) $50B capex commitment for FY2026 compresses near-term free cash flow,
  (2) the market questions whether OCI can close the share gap on AWS / Azure,
  (3) AI hyperscaler capex could slow if model-efficiency gains (Deepseek-style)
      reduce compute requirements, and
  (4) legacy business revenues are growing slowly as cloud cannibalises licences.

  The bull case rests on the RPO backlog converting to recognised revenue at
  20%+ annual growth, with margins expanding as the capex cycle peaks around
  FY2027-28 and OCI reaches scale.  Management's own FY2027 revenue target of
  $90B implies ~34% growth from FY2026 — extraordinarily aggressive for a $540B-
  market-cap company.

  Signal: {signal_label}  |  Ratio B: {ratio_str}  |  EPP gap: +{epp_gap_pct:.1f}%
  The current price offers an attractive entry point relative to the 2-yr
  earnings power target.  But the margin-of-safety is not extreme — a pullback
  toward $160 would offer a stronger ACCUMULATE set-up.
""")

print(sub("B. EARNINGS POWER PRICE (EPP) — STRUCTURAL FLOOR"))
print(f"""
  EPS anchor   : FY2022 non-GAAP ${EPS_TROUGH:.2f}  (pre-cloud-inflection baseline)
  Bear trough  : ${EPS_TROUGH_PRICE:.0f}  (Sep 2022 tech selloff)
  Observed PE  : ${EPS_TROUGH_PRICE:.0f} / ${EPS_TROUGH:.2f} = {EPS_TROUGH_PRICE/EPS_TROUGH:.1f}x  (panic trough)
  EPP min PE   : {EPP_MIN_PE}x  (structural floor; cloud recurring-revenue premium
                  over 2022 shock low of 13x; recent 2025 correction trough was 22x)

  EPS now      : ${EPS_NOW:.2f}  (normalised FY2026; excl. $0.77/sh Ampere one-time gain)
  EPP floor    : ${EPS_NOW:.2f} × {EPP_MIN_PE}x = ${epp:.2f}
  Current vs EPP: ${CURRENT_PRICE:.2f} vs ${epp:.2f}  (+{epp_gap_pct:.1f}% above floor)

  Note on Ampere gain: Q2 FY2026 non-GAAP EPS was $2.26 (+54%) vs. $1.49 normalised,
  boosted by a $2.7B pre-tax gain on sale of Oracle's stake in Ampere Computing.
  Reported FY2026 EPS would be ~$7.50; normalised EPS used here is $6.73.
""")

print(sub("C. METHOD B — 2-YEAR EARNINGS POWER TARGET"))
print(f"""
  CONS_EPS_2YR : ${CONS_EPS_2YR:.2f}  (FY2028 est.; 49 analysts; 23% YoY growth from
                  FY2027 consensus $8.16; oracle management targeting $90B FY2027 revenue)
  CONS_EXIT_PE : {CONS_EXIT_PE}x  (conservative for 20%+ revenue grower with AI tailwinds;
                  peak 50x+ in 2024, trough 13x in 2022)
  Method B     : ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x = ${price_b:.0f}

  Ratio B = (${CURRENT_PRICE:.2f} − ${epp:.2f}) / (${price_b:.0f} − ${CURRENT_PRICE:.2f})
           = ${CURRENT_PRICE-epp:.2f} / ${price_b-CURRENT_PRICE:.2f}
           = {ratio_str}  →  {signal_label}
""")

print(sub("D. SCENARIO ANALYSIS"))
print(f"  {'Scenario':<8}  {'EPS':>6}  {'P/E':>6}  {'Price':>7}  {'vs Now':>8}  Description")
print(f"  {'-'*70}")
descs = {
    "BEAR":  "Cloud ramp stalls; OCI loses GPU bookings; FY2028 miss",
    "BASE":  "Mgmt $80B FY2027 path; $10 EPS FY2028 at 28x exit PE",
    "BULL":  "$90B revenue (mgmt target) + margin expansion; 35x peak",
    "XBULL": "AI cloud dominance + multi-cloud + enterprise AI agents",
}
for k, s in SCENARIOS.items():
    diff = (s["price"] - CURRENT_PRICE) / CURRENT_PRICE * 100
    sign = "+" if diff >= 0 else ""
    print(f"  {k:<8}  ${s['eps']:>5.2f}  {s['pe']:>5.1f}x  ${s['price']:>6.0f}  "
          f"{sign}{diff:>6.1f}%  {descs[k]}")

print(f"""
  BASE scenario ${SCENARIOS['BASE']['price']:.0f} = Method B target  (by construction).
  BULL path requires Oracle to execute $90B FY2027 revenue and sustain 20%+ margins.
  BEAR assumes AI capex efficiency (Deepseek-style) kills demand for OCI GPU clusters.
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

  Interpretation: Market is pricing Oracle between BEAR and BASE — reflecting
  FCF compression concerns from $50B capex, cloud share-gap vs. AWS/Azure,
  and AI compute efficiency risk.  Model (SCA-adjusted) sees upside to BASE/BULL
  given $523B RPO and 84% OCI growth.  The +{proxy_gap_pct:.0f}% model EV gap warrants
  an ACCUMULATE on further weakness.
""")

print(sub("F. STRUCTURAL COMPOSITE ADJUSTMENT (SCA)"))
print(f"""  {'Factor':<60}  {'Rating':>6}  {'Wt':>4}""")
print(f"  {'-'*74}")
for f in STRUCTURAL_FACTORS:
    full = f"{f['name']}  ({f['detail'][:80]}...)" if len(f['detail'])>80 else f"{f['name']}  ({f['detail']})"
    print(f"  {full[:72]:<72}  {f['rating']:>+5.1f}  {f['weight']*100:.0f}%")
print(f"""
  SCA raw = {sca_raw:.3f}   SCA adj (div 2) = {sca_adj:.3f}
  Market composite {market_composite:.2f}  +  SCA {sca_adj:.3f}  =  Model composite {adj_composite:.2f}
""")

print(sub("G. EPS QUALITY DECOMP  "
          f"(FY2022 ${PRE_CLOUD_EPS:.2f} -> FY2026 normalised ${EPS_NOW:.2f} = +${eps_g_total:.2f})"))
print(f"""  {'Component':<60}  {'Share':>6}  {'Type':>12}""")
print(f"  {'-'*81}")
for c in EPS_COMPONENTS:
    dol = eps_g_total * c["share"]
    label = f"{c['label']}  ({c['detail'][:60]})"
    print(f"  {label[:72]:<72}  {c['share']*100:.0f}%  {c['type']:>12}")
print(f"""
  Structural : ${eps_g_total * structural_pct/100:.2f}  ({structural_pct:.0f}%)
  Temporal   : ${eps_g_total * cyclical_pct/100:.2f}  ({cyclical_pct:.0f}%)
  Total      : ${eps_g_total:.2f}
""")

print(hdr(f"PART 3 — NUMBERS & SIGNALS   |  {TICKER}"))

print(sub("H. RISK / RETURN SUMMARY"))
print(f"""
  Current price       : ${CURRENT_PRICE:.2f}  (52-wk low $134.57; –45% from $345 peak)
  EPP floor           : ${epp:.2f}  (+{epp_gap_pct:.1f}% above floor; cloud moat floor at 16x)
  Method B target     : ${price_b:.0f}  (upside: +{(price_b/CURRENT_PRICE-1)*100:.0f}%)
  BEAR scenario       : ${SCENARIOS['BEAR']['price']:.0f}  (downside: {(SCENARIOS['BEAR']['price']/CURRENT_PRICE-1)*100:.0f}%; AI capex freeze scenario)
  Ratio B             : {ratio_str}  -> {signal_label}
  Dividend yield      : {div_yield:.1f}%  ($0.40 × 4 = ${div_per_share:.2f} annualised; 7% CAGR dividend growth)
  Beta                : {BETA:.2f}x  ({IDIO*100:.0f}% idio / {MACRO*100:.0f}% macro)
  Trailing P/E        : {trailing_pe:.1f}x  (FY2026 normalised ${EPS_NOW:.2f})
  Forward P/E         : {forward_pe:.1f}x  (FY2027 consensus ${EPS_FWD_CONSENSUS:.2f})
  RPO backlog         : $523B  (+438% YoY; equals ~1x market cap — revenue runway secured)
  OCI growth          : +84% YoY (Q3 FY2026); $4.9B quarterly run-rate → $20B annualised
  Capex FY2026        : ~$50B  (data-centre buildout; FCF compressed near term)
  FY2027 mgmt target  : $90B revenue  (+34% YoY; extraordinarily aggressive)
  Q4 FY2026 catalyst  : ~Jun 20 2026  (Q4 ends May 31; report expected ~3-4 wks later)
  Exit discipline     : OCI quarterly growth <30% YoY for 2 consecutive quarters → re-evaluate
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
