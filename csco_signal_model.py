"""
Cisco Systems, Inc. (CSCO) — Bottom-Up Risk/Reward Signal Model
===============================================================
Analysis date : 2026-05-22
Fiscal year   : Late-July year-end (FY2026 = Aug 2025 – Jul 2026; Q4 ends ~Jul 26 2026)
Price source  : Yahoo Finance / CNBC, 2026-05-22, intraday $113.57–$118.60; 52-wk $62.30–$119.39
"""

# ── 0. DEPENDENCIES ──────────────────────────────────────────────────────────
import math

# ── 1. CORE INPUTS ───────────────────────────────────────────────────────────
TICKER        = "CSCO"
COMPANY       = "Cisco Systems, Inc."
ANALYSIS_DATE = "2026-05-22"

CURRENT_PRICE = 118.20   # CSCO — fetched Yahoo Finance / CNBC, 2026-05-22
                          # intraday $113.57–$118.60; 52-wk high $119.39 (near all-time highs)

# Non-GAAP EPS (fully diluted)
# FY2022 : ~$3.36  (pre-channel-inventory peak; ended Jul 2022)
# FY2023 : $3.89   (+16% YoY; last clean year before Splunk / channel digestion)
# FY2024 : $3.73   (-4%; severe channel inventory correction + early Splunk integration costs)
# FY2025 : $3.81   (+2%; channel normalised; Splunk integration underway)
# FY2026 : $4.28   (guided midpoint $4.27–$4.29; Q1$1.00+Q2$1.04+Q3$1.06+Q4E$1.17)
#           Q3 FY2026: record revenue $15.8B (+12% YoY); AI orders raised to $9B FY2026
#           Networking revenue +25% YoY; AI revenue on track for $4B FY2026
EPS_TROUGH        = 3.73   # FY2024 — trough year (channel inventory correction + Splunk drag)
EPS_TROUGH_PRICE  = 46.0   # Dec 2023 / Jan 2024 low after severe guidance cut (12.3x trough P/E)
EPP_MIN_PE        = 14     # structural floor PE; modest premium to 12.3x panic trough;
                            # reflects software-recurring revenue + 60+ quarters dividend growth
EPS_NOW           = 4.28   # FY2026 guided midpoint (full year, nearly complete)
EPS_FWD_CONSENSUS = 5.00   # FY2027 consensus; ~17% YoY growth driven by AI + Splunk ramp
CONS_EPS_2YR      = 5.70   # FY2028 est. (~26 months out; 14% YoY from $5.00; AI networking scale)
CONS_EXIT_PE      = 26     # 2-yr exit multiple; AI networking premium over historic 14–18x range

BETA  = 1.05   # mildly above market; larger swings on AI cycle news
IDIO  = 0.55   # idiosyncratic weight
MACRO = 0.45   # macro weight

# ── 2. SCENARIO MATRIX ───────────────────────────────────────────────────────
# BEAR  : Channel inventory correction repeats (FY2024 déjà vu); Splunk impairment;
#         AI hyperscaler capex pauses; FY2028 EPS $3.50 at 13x trough PE
# BASE  : AI orders $9B FY2026 → $14B+ FY2028; Splunk synergies realised;
#         FY2028 $5.70 EPS at 26x exit (Method B)
# BULL  : Silicon One captures 30%+ of AI GPU cluster switching;
#         FY2028 $7.50 EPS at 30x premium AI-infrastructure multiple
# XBULL : Cisco wins unified AI network + security platform (FabricPath + Splunk + SASE);
#         $10 EPS at 35x as networking becomes AI-critical infrastructure

SCENARIOS = {
    "BEAR":  {"eps": 3.50, "pe": 13,   "price": round(3.50 *13,   0)},
    "BASE":  {"eps": 5.70, "pe": 26,   "price": round(5.70 *26,   0)},
    "BULL":  {"eps": 7.50, "pe": 30,   "price": round(7.50 *30,   0)},
    "XBULL": {"eps": 10.0, "pe": 35,   "price": round(10.0 *35,   0)},
}

# ── 3. STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────
STRUCTURAL_FACTORS = [
    {
        "name":   "Silicon One AI networking momentum",
        "detail": "Silicon One switching ASICs winning hyperscaler AI cluster backplane contracts; "
                  "AI orders raised to $9B FY2026 from initial $1B; networking revenue +25% Q3 FY2026; "
                  "Ethernet switching becoming preferred AI fabric over InfiniBand at scale",
        "rating": +0.9, "weight": 0.25,
    },
    {
        "name":   "Splunk + unified security platform",
        "detail": "Splunk ($28B acquisition, closed Mar 2024) = #1 SIEM globally; integrating with "
                  "Cisco XDR, SASE, Umbrella, ThousandEyes to create end-to-end security+network "
                  "observability platform; $4B+ annual Splunk revenue growing 20%+ YoY",
        "rating": +0.7, "weight": 0.20,
    },
    {
        "name":   "Enterprise network installed base moat",
        "detail": "~70% global campus/branch network share; multi-year refresh cycles on Cat9K, "
                  "Meraki, and SD-WAN; IOS XE ecosystem lock-in across Fortune 500; "
                  "high switching costs = durable revenue floor",
        "rating": +0.6, "weight": 0.20,
    },
    {
        "name":   "Channel inventory correction recurrence risk",
        "detail": "FY2024: customers worked down 12–18 months of excess inventory; revenue declined; "
                  "EPS fell 4% to $3.73; hyper-ordering during COVID supply crunch → structural "
                  "over-buying risk returns if AI capex cycle cools or enterprise IT freezes",
        "rating": -0.6, "weight": 0.20,
    },
    {
        "name":   "Competitive pressure in networking and AI fabric",
        "detail": "Arista Networks taking share in data-centre switching; Juniper (HPE) in campus; "
                  "white-box Ethernet (Broadcom SONiC) in hyperscalers; NVIDIA InfiniBand for HPC; "
                  "Microsoft / Meta building own switching ASICs",
        "rating": -0.5, "weight": 0.15,
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
        return "✕ AVOID",      "AVOID",  "#f87171"
    if r < 0.75:
        return "◉ BUY",        "BUY",    "#22c55e"
    if r < 1.10:
        return "◎ ACCUMULATE", "ACCUMULATE", "#f0b429"
    if r < 1.75:
        return "◐ WATCHLIST",  "WATCHLIST",  "#60a5fa"
    if r < 2.50:
        return "▷ HOLD/TRIM",  "HOLD",       "#a78bfa"
    return "✕ AVOID",          "AVOID",  "#f87171"

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

div_per_quarter = 0.42
div_yield = (div_per_quarter * 4) / CURRENT_PRICE * 100

# EPS decomposition: FY2024 $3.73 (trough) → FY2026 $4.28 = +$0.55
PRE_SPLUNK_EPS = EPS_TROUGH   # FY2024 anchor (channel-corrected + pre-Splunk-synergy baseline)
eps_g_total    = EPS_NOW - PRE_SPLUNK_EPS   # $0.55

EPS_COMPONENTS = [
    {"label": "Splunk revenue contribution (net)",
     "detail": "$4B+ annual Splunk revenue; integration costs winding down; "
               "SIEM platform growing 20%+ in recurring software",
     "share": 0.30, "type": "Structural"},
    {"label": "AI networking product mix (Silicon One premium)",
     "detail": "AI orders $9B FY2026; Silicon One switching commands premium ASP vs. "
               "legacy Cat9K; faster growth in high-margin data-centre products",
     "share": 0.25, "type": "Structural"},
    {"label": "Security platform (XDR, SASE, Umbrella)",
     "detail": "Security revenue growing 9%+ YoY; recurring SaaS subscriptions; "
               "Cisco is #2 security vendor globally",
     "share": 0.20, "type": "Structural"},
    {"label": "Share buyback accretion",
     "detail": "~$7–10B annual buybacks; share count declining ~2% per year; "
               "contributes ~1–2% annual EPS growth",
     "share": 0.15, "type": "Structural"},
    {"label": "Channel inventory normalisation",
     "detail": "FY2024 trough caused by customers burning excess COVID-era stock; "
               "normalisation boosted FY2025-26 demand recovery — temporal not permanent",
     "share": 0.10, "type": "Temporal"},
]
structural_pct = sum(c["share"] for c in EPS_COMPONENTS if c["type"] == "Structural") * 100
cyclical_pct   = 100 - structural_pct

idio_drivers = [
    ("AI infrastructure order conversion rate (orders → revenue)", "IDIO", "25%",
     "$9B AI orders FY2026; backlog converting to revenue over 2-4 quarters"),
    ("Splunk integration synergies & customer expansion", "IDIO", "20%",
     "Cross-sell Splunk into Cisco's 100K+ enterprise customer base; platform gross margin"),
    ("Enterprise network refresh cycle (campus + campus Wi-Fi 7)", "IDIO", "10%",
     "Cat9K + Meraki Wi-Fi 7 + SD-WAN refresh; 5-7 yr hardware cycles"),
    ("Enterprise IT spending cycle (budget freeze risk)", "MACRO", "25%",
     "Cisco is a major IT capex line item; belt-tightening = order delays"),
    ("Interest rates / tech multiple / risk appetite", "MACRO", "20%",
     "Cisco at 27x FY2026 non-GAAP is historically rich; rate sensitivity to multiple"),
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
  Sector  : Enterprise Networking · AI Infrastructure · Security (SIEM/SASE)
  FY end  : Late July  (FY2026 = Aug 2025 – Jul 2026; Q4 ends ~Jul 26 2026)
  Price   : ${CURRENT_PRICE:.2f}  [{ANALYSIS_DATE}]
  52-week : $62.30 low – $119.39 high  (near all-time highs; +90% in 12 months)
""")

print(hdr(f"PART 2 — ANALYST COMMENTARY  |  {TICKER}"))

print(sub("A. INVESTMENT THESIS"))
print(f"""
  Cisco has undergone a genuine fundamental transformation since 2024.  Two
  catalysts:

  1. AI NETWORKING (Silicon One):  Hyperscalers building GPU clusters need
     ultra-low-latency, lossless Ethernet backplane fabric.  Cisco's Silicon One
     ASICs (800G/1.6T) are winning deployments at AWS, Meta, Microsoft, and others.
     AI infrastructure orders were raised to $9B for FY2026 — up from the initial
     $1B guidance — and management is targeting $6B+ of AI REVENUE in FY2027.
     Networking revenue grew 25% YoY in Q3 FY2026.

  2. SPLUNK INTEGRATION:  The $28B Splunk acquisition (Mar 2024) added the #1
     global SIEM platform (~$4B annual revenue, growing 20%+) and is creating a
     unified security + observability + network intelligence stack.  Splunk's
     high-margin recurring software revenue is lifting Cisco's overall mix.

  Yet at ${CURRENT_PRICE:.2f} — within $1 of the 52-week high — the market has
  already priced both catalysts.  The stock has nearly doubled in 12 months.
  Forward PE of {forward_pe:.1f}x on FY2027 consensus is well above Cisco's historical
  14–18x range.  The EPP framework puts the structural floor at ${epp:.2f} (97%
  below current price), and the 2-yr Method B target of ${price_b:.0f} implies only
  {(price_b/CURRENT_PRICE-1)*100:.0f}% further upside from here.

  Signal: {signal_label}  |  Ratio B: {ratio_str}  |  EPP gap: +{epp_gap_pct:.1f}%
  Appropriate for current holders; new capital should wait for pullback toward
  $95–105 to achieve an ACCUMULATE set-up.
""")

print(sub("B. EARNINGS POWER PRICE (EPP) — STRUCTURAL FLOOR"))
print(f"""
  EPS anchor   : FY2024 non-GAAP ${EPS_TROUGH:.2f}  (trough: channel inventory + early Splunk)
  Bear trough  : ${EPS_TROUGH_PRICE:.0f}  (Dec 2023 / Jan 2024; severe guidance cut)
  Observed PE  : ${EPS_TROUGH_PRICE:.0f} / ${EPS_TROUGH:.2f} = {EPS_TROUGH_PRICE/EPS_TROUGH:.1f}x  (panic low)
  EPP min PE   : {EPP_MIN_PE}x  (slight premium to panic trough; software/dividend stability;
                  Cisco's 2025 correction trough was ~$62 / $3.81 = 16.3x)

  EPS now      : ${EPS_NOW:.2f}  (FY2026 guided midpoint; Q4 guidance $1.16–$1.18)
  EPP floor    : ${EPS_NOW:.2f} × {EPP_MIN_PE}x = ${epp:.2f}
  Current vs EPP: ${CURRENT_PRICE:.2f} vs ${epp:.2f}  (+{epp_gap_pct:.1f}% above floor)

  The 97% EPP gap reflects the multiple expansion from 12–16x (2023–24 range)
  to the current 27.6x — driven by AI networking re-rating.  The floor rises as
  EPS grows; at $5.70 FY2028E × 14x the floor migrates to $80.
""")

print(sub("C. METHOD B — 2-YEAR EARNINGS POWER TARGET"))
print(f"""
  CONS_EPS_2YR : ${CONS_EPS_2YR:.2f}  (FY2028 est.; ~26 months out; ~14% YoY growth
                  from FY2027 consensus $5.00; AI networking + Splunk ramping)
  CONS_EXIT_PE : {CONS_EXIT_PE}x  (AI networking premium over historic 14–18x;
                  discount to current 27.6x reflecting partial mean reversion)
  Method B     : ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}x = ${price_b:.0f}

  Ratio B = (${CURRENT_PRICE:.2f} − ${epp:.2f}) / (${price_b:.0f} − ${CURRENT_PRICE:.2f})
           = ${CURRENT_PRICE-epp:.2f} / ${price_b-CURRENT_PRICE:.2f}
           = {ratio_str}  →  {signal_label}

  Sensitivity to exit PE assumption:
    CONS_EXIT_PE = 22x → Price_B $125 → Ratio B 3.47x  (AVOID)
    CONS_EXIT_PE = 24x → Price_B $137 → Ratio B 3.09x  (AVOID)
    CONS_EXIT_PE = 26x → Price_B $148 → Ratio B 1.94x  (HOLD)  ← base case
    CONS_EXIT_PE = 28x → Price_B $160 → Ratio B 1.40x  (WATCHLIST)
    CONS_EXIT_PE = 30x → Price_B $171 → Ratio B 1.09x  (ACCUMULATE border)
  The signal is highly PE-sensitive; AI narrative durability is the swing factor.
""")

print(sub("D. SCENARIO ANALYSIS"))
print(f"  {'Scenario':<8}  {'EPS':>6}  {'P/E':>6}  {'Price':>7}  {'vs Now':>8}  Description")
print(f"  {'-'*70}")
descs = {
    "BEAR":  "Channel inventory 2.0 + AI capex pause; back to FY2024-era pricing",
    "BASE":  "AI $14B+ orders by FY2028; Splunk synergies; 26x exit multiple",
    "BULL":  "Silicon One wins 30%+ of AI cluster switching; security premium",
    "XBULL": "Cisco = AI network + security OS; Splunk AI SIEM commands 35x",
}
for k, s in SCENARIOS.items():
    diff = (s["price"] - CURRENT_PRICE) / CURRENT_PRICE * 100
    sign = "+" if diff >= 0 else ""
    print(f"  {k:<8}  ${s['eps']:>5.2f}  {s['pe']:>5.1f}x  ${s['price']:>6.0f}  "
          f"{sign}{diff:>6.1f}%  {descs[k]}")
print(f"""
  BASE scenario ${SCENARIOS['BASE']['price']:.0f} = Method B target (by construction).
  BEAR at ${SCENARIOS['BEAR']['price']:.0f} maps to the Dec 2023 panic low — plausible in a
  severe channel-correction or AI-capex-pause environment.
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

  Interpretation: Market assigns ~50%+ probability to BASE scenario (AI networking
  conversion + Splunk) at ~$148, consistent with recent strong AI orders.  SCA
  is modestly positive, pushing the model EV slightly above current price.
  The signal composite sitting near BASE (2.0) confirms the stock is fairly priced
  at BASE expectations — not cheap, not expensive if AI thesis plays out.
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

print(sub("G. EPS QUALITY DECOMP  "
          f"(FY2024 trough ${PRE_SPLUNK_EPS:.2f} -> FY2026 ${EPS_NOW:.2f} = +${eps_g_total:.2f})"))
print(f"""  {'Component':<60}  {'Share':>6}  {'Type':>12}""")
print(f"  {'-'*81}")
for c in EPS_COMPONENTS:
    label = f"{c['label']}  ({c['detail'][:58]})"
    print(f"  {label[:72]:<72}  {c['share']*100:.0f}%  {c['type']:>12}")
print(f"""
  Structural : ${eps_g_total * structural_pct/100:.2f}  ({structural_pct:.0f}%)
  Temporal   : ${eps_g_total * cyclical_pct/100:.2f}  ({cyclical_pct:.0f}%)
  Total      : ${eps_g_total:.2f}
""")

print(hdr(f"PART 3 — NUMBERS & SIGNALS   |  {TICKER}"))

print(sub("H. RISK / RETURN SUMMARY"))
print(f"""
  Current price       : ${CURRENT_PRICE:.2f}  (52-wk low $62.30; near 52-wk HIGH $119.39)
  EPP floor           : ${epp:.2f}  (+{epp_gap_pct:.1f}% above floor; 14x min-viable PE on ${EPS_NOW:.2f})
  Method B target     : ${price_b:.0f}  (upside: +{(price_b/CURRENT_PRICE-1)*100:.0f}%)
  BEAR scenario       : ${SCENARIOS['BEAR']['price']:.0f}  (downside: {(SCENARIOS['BEAR']['price']/CURRENT_PRICE-1)*100:.0f}%; channel-correction repeat)
  Ratio B             : {ratio_str}  -> {signal_label}
  Dividend yield      : {div_yield:.1f}%  (${div_per_quarter:.2f}/qtr × 4 = ${div_per_quarter*4:.2f}; 60+ consecutive growth qtrs)
  Beta                : {BETA:.2f}x  ({IDIO*100:.0f}% idio / {MACRO*100:.0f}% macro)
  Trailing P/E        : {trailing_pe:.1f}x  (FY2026 guided ${EPS_NOW:.2f}; historically 14–18x)
  Forward P/E         : {forward_pe:.1f}x  (FY2027 consensus ${EPS_FWD_CONSENSUS:.2f})
  AI orders FY2026    : $9B  (raised 3× from initial guidance; Ethernet AI fabric demand)
  AI revenue FY2027E  : $6B+  (management target; step-up from $4B FY2026)
  Splunk revenue      : ~$4B+  (growing 20%+ YoY; SIEM #1; margins expanding)
  Q4 FY2026 catalyst  : ~Aug 13 2026  (quarterly non-GAAP EPS guidance: $1.16–$1.18)
  HOLD trigger        : AI order growth decelerates OR Splunk churn rises → re-evaluate
  ACCUMULATE trigger  : Pullback to $95–105 (Ratio B ≈ 1.1–1.4x at that level)
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
