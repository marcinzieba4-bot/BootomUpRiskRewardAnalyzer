"""
SAP SE (SAP) — Bottom-Up Risk/Reward Signal Model
==================================================
Analysis date : 2026-05-22
Fiscal year   : Calendar year (Jan 1 – Dec 31); reports in EUR (€)
ADR note      : NYSE ADR = 1 ordinary SAP SE share; EPS converted EUR→USD
FX assumption : EUR/USD 1.17  (implied from Q1 2026: €1.72 non-IFRS EPS = $2.01 USD)
Price source  : Yahoo Finance / CNBC, 2026-05-22, ~$167.27 (52-wk range $158.58–$313.28)
"""

# ── 0. DEPENDENCIES ──────────────────────────────────────────────────────────
import math

# ── 1. CORE INPUTS ───────────────────────────────────────────────────────────
TICKER        = "SAP"
COMPANY       = "SAP SE"
ANALYSIS_DATE = "2026-05-22"

CURRENT_PRICE = 167.27   # SAP — NYSE ADR, fetched Yahoo Finance / CNBC, 2026-05-22
                          # 52-wk low $158.58 — 52-wk high $313.28 (all-time high Jul 9 2025)
                          # Stock down 47% from ATH; currently 5% above 52-wk low

EUR_USD       = 1.17      # FX rate used for EUR→USD EPS conversion
                          # Q1 2026 implied: €1.72 non-IFRS EPS = $2.01 USD

# Non-IFRS EPS (EUR → USD converted at EUR_USD = 1.17)
# EUR-basis history:
#   FY2022 : ~€3.50    (pre-cloud-acceleration)
#   FY2023 : €5.01     (post-restructuring acceleration; +43% YoY)
#   FY2024 : ~€4.52    (down; Qualtrics disposal, restructuring charges, integration costs)
#   FY2025 : €6.15     (+36% YoY; restructuring complete; cloud margin expansion)
#   FY2026E: €6.84     (consensus; Q1 actual €1.72; full-year guidance confirmed)
#   FY2027E: €7.41     (consensus; 8% YoY; cloud scale + Joule AI premium)
# USD-basis at 1.17:
#   FY2025 : $7.20  |  FY2026E : $8.00  |  FY2027E : $8.67  |  FY2028E : $9.71
EPS_TROUGH        = 7.20   # FY2025 USD (€6.15 × 1.17); most recent completed FY
EPS_TROUGH_PRICE  = 158.58 # 52-wk low (May 2025; trough of the ATH-to-trough correction)
EPP_MIN_PE        = 20     # structural floor; observed trough PE was $158.58/$7.20 = 22x;
                            # 20x is conservative floor for ERP monopolist with 90%+ retention
EPS_NOW           = 8.00   # FY2026E USD (€6.84 × 1.17; Q1 actual €1.72; guidance confirmed)
EPS_FWD_CONSENSUS = 8.67   # FY2027E USD (€7.41 × 1.17; 49 analyst consensus)
CONS_EPS_2YR      = 9.71   # FY2028E USD (€8.30E × 1.17; ~24 months; 12% YoY from FY2027)
CONS_EXIT_PE      = 26     # 2-yr exit; conservative vs SAP's historical 25–45x range;
                            # just a partial re-rating from current 20.9x forward PE

BETA  = 1.10   # European large-cap; moderate; EUR/USD adds volatility for USD investors
IDIO  = 0.60   # idiosyncratic: ERP monopoly + AI execution
MACRO = 0.40   # macro: trade/tariff + EUR/USD + enterprise IT spending

# ── 2. SCENARIO MATRIX ───────────────────────────────────────────────────────
# BEAR  : Cloud growth decelerates to 10%, EUR/USD to 1.00; FX headwind bites hard;
#         FY2028 EUR EPS €7.00 × 1.00 USD = $7.00; re-rated at 18x = $126
# BASE  : Consensus path: cloud 20%+ CAGR; Joule AI adoption; FY2028 $9.71 at 26x
# BULL  : S/4HANA 300M+ users fully migrated; Joule AI commands premium pricing;
#         €9.50 FY2028 EPS × 1.17 × 32x = $355
# XBULL : SAP = Enterprise OS for AI; Joule + Business AI + data fabric + CX;
#         €13.00 FY2028 × 1.17 × 40x = $608

SCENARIOS = {
    "BEAR":  {"eps": 7.00,  "pe": 18,   "price": round(7.00 *18,   0)},
    "BASE":  {"eps": 9.71,  "pe": 26,   "price": round(9.71 *26,   0)},
    "BULL":  {"eps": 11.50, "pe": 31,   "price": round(11.50*31,   0)},
    "XBULL": {"eps": 16.00, "pe": 38,   "price": round(16.00*38,   0)},
}

# ── 3. STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────
STRUCTURAL_FACTORS = [
    {
        "name":   "S/4HANA cloud migration monopoly",
        "detail": "300M+ licensed users facing mandatory S/4HANA migration deadline 2027; "
                  "no realistic ERP alternative at enterprise scale; RISE with SAP captures "
                  "full stack; cloud ERP revenue +30% YoY Q1 2026; backlog €63B+",
        "rating": +1.2, "weight": 0.25,
    },
    {
        "name":   "Joule AI copilot + Business AI platform",
        "detail": "Joule embedded across S/4HANA, SuccessFactors, Ariba, CX; "
                  "1B+ Joule interactions in 2025; AI-native ERP commands 15-25% price "
                  "premium; SAP Business AI = largest enterprise AI use-case surface area",
        "rating": +0.9, "weight": 0.20,
    },
    {
        "name":   "Cloud backlog visibility (€63B+)",
        "detail": "Current cloud backlog growing 25%+ YoY in constant currency; "
                  "long-term multi-year contracts; 92%+ cloud renewal rates; "
                  "contracted future revenue ≈ 3× annual cloud revenue",
        "rating": +0.8, "weight": 0.20,
    },
    {
        "name":   "Microsoft Dynamics 365 + Copilot disruption risk",
        "detail": "Microsoft integrating Copilot AI into Dynamics 365 ERP; Azure-native "
                  "deployment; D365 winning SMB and mid-market displacement; "
                  "Teams + Office + Dynamics bundling pressure; long-term threat to SAP "
                  "mid-market and potential upper mid-market accounts",
        "rating": -0.8, "weight": 0.20,
    },
    {
        "name":   "EUR/USD FX headwind (for USD investors)",
        "detail": "SAP reports in EUR; ~35% North American revenue but USD-denominated costs "
                  "and EUR reporting creates translation risk; EUR weakness → lower USD EPS; "
                  "trade-war tariff risk adds macro uncertainty to European tech",
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

trailing_pe      = CURRENT_PRICE / EPS_NOW
forward_pe       = CURRENT_PRICE / EPS_FWD_CONSENSUS
trough_pe_obs    = EPS_TROUGH_PRICE / EPS_TROUGH

# EPS decomp: FY2024 ~$4.93 (€4.52 × 1.09) → FY2026E $8.00 = +$3.07
PRE_CLOUD_EPS   = 4.93     # FY2024 USD (€4.52 × 1.09 avg EUR/USD 2024; restructuring trough)
eps_g_total     = EPS_NOW - PRE_CLOUD_EPS

EPS_COMPONENTS = [
    {"label": "S/4HANA cloud subscription margin expansion",
     "detail": "Licence-to-cloud shift increases gross margin ~10pts; "
               "cloud ERP revenue +30% YoY; RISE with SAP full-stack capture",
     "share": 0.35, "type": "Structural"},
    {"label": "Restructuring cost reset (8K headcount FY2024)",
     "detail": "FY2024 restructuring removed €3B+ of annual cost; "
               "AI + automation reducing headcount needed per €1 revenue",
     "share": 0.20, "type": "Structural"},
    {"label": "Joule AI + Business AI platform premium",
     "detail": "AI-native ERP commands 15-25% price premium; "
               "Joule embedded in all modules; new AI SKUs launching",
     "share": 0.15, "type": "Structural"},
    {"label": "Share buyback accretion (€10B programme)",
     "detail": "€10B buyback announced 2025; ~8% of float; ~2%/yr EPS accretion",
     "share": 0.15, "type": "Structural"},
    {"label": "EUR/USD FX tailwind (2024→2026 appreciation)",
     "detail": "EUR/USD ~1.09 in 2024 → ~1.17 in Q1 2026; +7% USD translation benefit",
     "share": 0.15, "type": "Temporal"},
]
structural_pct = sum(c["share"] for c in EPS_COMPONENTS if c["type"] == "Structural") * 100
cyclical_pct   = 100 - structural_pct

idio_drivers = [
    ("S/4HANA migration pace (2027 end-of-maintenance deadline)", "IDIO", "25%",
     "Each SAP ECC customer that migrates = multi-year cloud contract secured"),
    ("Joule AI adoption + premium pricing realisation", "IDIO", "20%",
     "1B+ interactions in 2025; monetisation ramp in 2026-27 is the key upside"),
    ("Qualtrics/Signavio/WalkMe integration execution", "IDIO", "15%",
     "Multiple acquisitions integrating into the Business Suite; execution risk"),
    ("Enterprise IT spending cycle + tariff risk", "MACRO", "20%",
     "ERP deals can be delayed in macro freeze; US-EU trade war affects SAP customers"),
    ("EUR/USD exchange rate", "MACRO", "20%",
     "Every 0.05 move in EUR/USD = ~4% impact on USD EPS; highly material for USD investors"),
]

# ── 6. REPORT OUTPUT ─────────────────────────────────────────────────────────
W = 72
def hdr(title): return f"\n{'='*W}\n  {title}\n{'='*W}"
def sub(title): return f"\n  {title}\n  {'-'*(W-2)}"

print(hdr(f"PART 1 — FRAMEWORK OVERVIEW  |  {TICKER}  |  {COMPANY}"))
print(f"""
  Bottom-Up Risk/Reward (EPP / Ratio-B / Softmax) applied to {COMPANY} ({TICKER}).

  Three pillars:
  1. EPP Floor     — structural downside anchor  (EPS × min-viable trough P/E)
  2. Method B      — 2-yr consensus earnings power target (EPS × exit P/E)
  3. Ratio B       — primary signal: (price − EPP) / (Method B − price)
                     <0.75 BUY | 0.75–1.1 ACCUMULATE | 1.1–1.75 WATCHLIST
                     1.75–2.5 HOLD | >2.5 AVOID

  Company : {COMPANY}
  Sector  : Enterprise ERP Cloud · Business AI Platform · HR/Finance/SCM SaaS
  FY end  : December 31  (calendar year; reports in EUR; ADR 1:1 ordinary share)
  FX      : EUR/USD {EUR_USD:.2f}  (Q1 2026 implied: €1.72 non-IFRS = $2.01 USD)
  Price   : ${CURRENT_PRICE:.2f}  [{ANALYSIS_DATE}]
  52-week : ${EPS_TROUGH_PRICE:.2f} low – $313.28 high  (ATH Jul 2025; down 47% from peak)
""")

print(hdr(f"PART 2 — ANALYST COMMENTARY  |  {TICKER}"))

print(sub("A. INVESTMENT THESIS"))
print(f"""
  SAP is the world's #1 enterprise ERP vendor with an estimated 300 million+
  licensed users facing a hard migration deadline to S/4HANA Cloud (mainstream
  maintenance for SAP ECC ends 2027).  This is not a choice — it is a mandatory,
  time-limited upgrade cycle.  Every customer that migrates converts from a
  one-time licence fee to a recurring cloud subscription, permanently improving
  SAP's revenue quality and gross margins.

  Q1 2026: Cloud revenue +27% YoY (constant currency); Cloud ERP Suite +30%.
  Current Cloud Backlog (CCB): ~$25.6B (+25% CC YoY) — three years of forward
  cloud revenue secured under contract.  Non-IFRS EPS €1.72 (+20%).

  Yet the stock trades at ${CURRENT_PRICE:.2f} — just ${CURRENT_PRICE - EPS_TROUGH_PRICE:.2f} above its 52-week low
  and 47% below the July 2025 ATH of $313.28.  The sell-off was driven by:
  (1) Multiple compression from 40–50x (ATH) to the current {trailing_pe:.1f}x (20-year low);
  (2) Q4 2025 cloud backlog growth deceleration concern (CCB growth slowed);
  (3) Trade-war / EUR headwinds on US-listed ADR valuation;
  (4) Middle East geopolitical caveats in Q1 2026 guidance language.

  The fundamentals have NOT deteriorated.  Cloud revenue is growing 23–27%.
  The business is structurally stronger than at the ATH.  The market has simply
  re-rated from "bubble premium" (40–50x) to "trough discount" (21x forward).

  At ${CURRENT_PRICE:.2f}, SAP trades at {trailing_pe:.1f}x FY2026E and {forward_pe:.1f}x FY2027E —
  near the lowest forward multiple since the company began its cloud transition.
  The EPP floor at ${epp:.2f} (20x × ${EPS_NOW:.2f}) is only ${CURRENT_PRICE - epp:.2f} below current price.
  This is the largest asymmetry in the coverage universe outside of CRM.

  Signal: {signal_label}  |  Ratio B: {ratio_str}  |  EPP gap: +{epp_gap_pct:.1f}%
""")

print(sub("B. EARNINGS POWER PRICE (EPP) — STRUCTURAL FLOOR"))
print(f"""
  EPS anchor   : FY2025 USD ${EPS_TROUGH:.2f}  (€6.15 × {EUR_USD:.2f}; last completed FY)
  Bear trough  : ${EPS_TROUGH_PRICE:.2f}  (52-wk low; trough of 47% ATH correction)
  Observed PE  : ${EPS_TROUGH_PRICE:.2f} / ${EPS_TROUGH:.2f} = {trough_pe_obs:.1f}x  (recent trough multiple)
  EPP min PE   : {EPP_MIN_PE}x  (below observed {trough_pe_obs:.1f}x trough; conservative floor;
                  SAP's ERP monopoly + recurring revenue justifies 20x minimum)

  EPS now      : ${EPS_NOW:.2f}  (FY2026E USD; €6.84 × {EUR_USD:.2f}; full-year guidance confirmed)
  EPP floor    : ${EPS_NOW:.2f} × {EPP_MIN_PE}x = ${epp:.2f}
  Current vs EPP: ${CURRENT_PRICE:.2f} vs ${epp:.2f}  ({epp_gap_pct:+.1f}% — essentially AT the structural floor)

  FX sensitivity: If EUR/USD = 1.10 → EPS_NOW $7.52 → EPP $150.40 (-10% floor)
                  If EUR/USD = 1.25 → EPS_NOW $8.55 → EPP $171.00 (+7% floor)
  The current price is within the FX-sensitivity band of the EPP floor.
""")

print(sub("C. METHOD B — 2-YEAR EARNINGS POWER TARGET"))
print(f"""
  CONS_EPS_2YR : ${CONS_EPS_2YR:.2f}  (FY2028E USD; €8.30E × {EUR_USD:.2f}; ~24 months out;
                  12% YoY growth from FY2027 consensus €7.41; cloud scale + Joule)
  CONS_EXIT_PE : {CONS_EXIT_PE}x  (conservative re-rating; SAP historical range 25–45x;
                  26x is below the 10-year average; just partial recovery from 21x trough)
  Method B     : ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x = ${price_b:.0f}

  Ratio B = (${CURRENT_PRICE:.2f} − ${epp:.2f}) / (${price_b:.0f} − ${CURRENT_PRICE:.2f})
           = ${CURRENT_PRICE-epp:.2f} / ${price_b-CURRENT_PRICE:.2f}
           = {ratio_str}  →  {signal_label}

  Sensitivity:
    CONS_EXIT_PE = 22x → Price_B $214 → Ratio B 0.15x  (BUY)
    CONS_EXIT_PE = 26x → Price_B $252 → Ratio B 0.09x  (BUY)  ← base case
    CONS_EXIT_PE = 30x → Price_B $291 → Ratio B 0.06x  (BUY)
  Signal is robustly BUY across a wide range of exit PE assumptions given the
  very low EPP gap (+4.5%).  Even a 20x exit PE gives Price_B $194 — still BUY.
""")

print(sub("D. SCENARIO ANALYSIS"))
print(f"  {'Scenario':<8}  {'EPS':>6}  {'P/E':>6}  {'Price':>7}  {'vs Now':>8}  Description")
print(f"  {'-'*70}")
descs = {
    "BEAR":  "Cloud decel + EUR/USD 1.00; FX headwind erodes USD EPS; 18x floor",
    "BASE":  "Consensus FY2028 $9.71; cloud 20%+ CAGR; Joule AI uplift; 26x",
    "BULL":  "S/4HANA migration complete; Joule AI premium pricing; 31x",
    "XBULL": "SAP = Enterprise AI OS; monopoly + AI + data fabric; 38x peak",
}
for k, s in SCENARIOS.items():
    diff = (s["price"] - CURRENT_PRICE) / CURRENT_PRICE * 100
    sign = "+" if diff >= 0 else ""
    print(f"  {k:<8}  ${s['eps']:>5.2f}  {s['pe']:>5.1f}x  ${s['price']:>6.0f}  "
          f"{sign}{diff:>6.1f}%  {descs[k]}")
print(f"""
  BEAR at ${SCENARIOS['BEAR']['price']:.0f} represents a EUR/USD-adjusted EPS scenario;
  even this pessimistic case only implies -24% from current.
  BULL and XBULL reflect SAP's cloud monopoly re-rated by AI platform monetisation.
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

  Interpretation: Market is heavily pricing BEAR/base-adjacent scenarios — the
  47% ATH drawdown reflects maximum fear around cloud deceleration + FX + trade
  war.  The model (SCA-adjusted) sees high BASE and BULL probability given the
  S/4HANA migration monopoly and cloud backlog visibility.  At ${proxy_ev:.0f} model EV,
  the implied {proxy_gap_pct:+.0f}% upside is the largest in the universe for a non-CRM name.
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
          f"(FY2024 USD ${PRE_CLOUD_EPS:.2f} → FY2026E ${EPS_NOW:.2f} = +${eps_g_total:.2f})"))
print(f"""  {'Component':<60}  {'Share':>6}  {'Type':>12}""")
print(f"  {'-'*81}")
for c in EPS_COMPONENTS:
    label = f"{c['label']}  ({c['detail'][:58]})"
    print(f"  {label[:72]:<72}  {c['share']*100:.0f}%  {c['type']:>12}")
print(f"""
  Structural : ${eps_g_total * structural_pct/100:.2f}  ({structural_pct:.0f}%)
  Temporal   : ${eps_g_total * cyclical_pct/100:.2f}  ({cyclical_pct:.0f}%)
  Total      : ${eps_g_total:.2f}

  Note: FY2024 was the restructuring trough (€4.52 EUR; SAP cut 8,000+ jobs).
  FY2025 recovered to €6.15 (+36%) as restructuring benefits flowed through.
  The FX component reflects EUR appreciation vs USD 2024→2026; at a flat rate it
  would be zero — USD investors should model FX sensitivity independently.
""")

print(hdr(f"PART 3 — NUMBERS & SIGNALS   |  {TICKER}"))

print(sub("H. RISK / RETURN SUMMARY"))
print(f"""
  Current price       : ${CURRENT_PRICE:.2f}  (52-wk low ${EPS_TROUGH_PRICE:.2f}; –47% from $313.28 ATH)
  EPP floor           : ${epp:.2f}  ({epp_gap_pct:+.1f}% — stock at structural floor; 20x × ${EPS_NOW:.2f})
  Method B target     : ${price_b:.0f}  (upside: +{(price_b/CURRENT_PRICE-1)*100:.0f}%)
  BEAR scenario       : ${SCENARIOS['BEAR']['price']:.0f}  (downside: {(SCENARIOS['BEAR']['price']/CURRENT_PRICE-1)*100:.0f}%; EUR/USD shock + cloud decel)
  Ratio B             : {ratio_str}  -> {signal_label}
  Forward P/E         : {forward_pe:.1f}x  (FY2027 $8.67; SAP's 20-year low multiple)
  Trailing P/E        : {trailing_pe:.1f}x  (FY2026E $8.00; near-trough valuation)
  EUR/USD sensitivity : ±$0.05 FX move ≈ ±4% impact on USD EPS and EPP floor
  Cloud revenue FY2026: $29.7B guided (€25.4B × 1.17; +25% CC growth)
  Cloud backlog       : $29.9B (€25.6B × 1.17; 25% CC growth; 3× annual cloud revenue)
  S/4HANA deadline    : 2027 ECC maintenance end → 300M users must migrate by 2027
  Joule AI            : 1B+ interactions in 2025; premium AI SKU pricing launching
  Buyback programme   : €10B (~8% of float; announced 2025; structural EPS uplift)
  Q2 2026 catalyst    : ~Jul 2026 (Q2 results; cloud backlog growth rate is key)
  BUY thesis breaks if: cloud backlog CCB growth < 15% for 2 consecutive quarters,
                        OR EUR/USD falls below 1.00 and stays there, OR Microsoft
                        wins a large-enterprise ERP displacement campaign.
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
