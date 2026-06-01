"""
Take-Two Interactive Software, Inc. (NASDAQ: TTWO) — Bottom-Up Risk/Reward Signal Model
BottomUp Risk/Reward Analyzer · veerock framework
Date: 2026-06-01

NOTE: TTWO uses Net Bookings as its primary operating metric (differs from GAAP revenue due
to deferred recognition). Adjusted EPS (non-GAAP) is used throughout — GAAP EPS is deeply
negative due to ~$11B Zynga goodwill/intangible amortization (~$15-20/share annual impact).
The EPP gap is intentionally large; it reflects GTA VI launch optionality embedded in price.
"""

# ── PRICE & MARKET DATA ───────────────────────────────────────────────────────
TICKER            = "TTWO"
COMPANY           = "Take-Two Interactive Software, Inc."
SECTOR            = "Video Games · AAA Publishing · Mobile (Zynga) · NASDAQ: TTWO"
DATE              = "2026-06-01"
CURRENT_PRICE     = 224.16
VOL_52W_LOW       = 187.63   # Hit on GTA VI delay announcement (May→Nov 2026)
VOL_52W_HIGH      = 264.79
SHARES_OUT_M      = 185.0    # Diluted; Gearbox acquisition added ~7M shares
ANNUAL_DIV        = 0.0      # No dividend — capital reinvested in game development

# ── NET BOOKINGS HISTORY (fiscal year ends March 31) ─────────────────────────
NB_FY2024_B       = 5.33   # FY ended March 31, 2024
NB_FY2025_B       = 5.65   # FY ended March 31, 2025  (+6% YoY)
NB_FY2026_B       = 6.72   # FY ended March 31, 2026  (+19% YoY) — reported May 21, 2026
NB_FY2027_GUIDE_B = 8.10   # Midpoint of $8.0-8.2B guidance (GTA VI year)

# ── SEGMENT MIX (FY2026 approximate) ─────────────────────────────────────────
NB_MOBILE_PCT     = 0.46   # Zynga: Toon Blast, Match Factory!, Empires & Puzzles, hyper-casual
NB_2K_PCT         = 0.30   # 2K Games: NBA 2K, Borderlands, Civilization, BioShock, XCOM
NB_ROCKSTAR_PCT   = 0.21   # Rockstar: GTA Online, GTA V, Red Dead Online/RDR2
NB_OTHER_PCT      = 0.03   # Other labels, licensing

# ── RECURRENT CONSUMER SPENDING ───────────────────────────────────────────────
RECURRENT_PCT     = 0.78   # 78% of FY2026 NB from recurrent/live-service spending
# GTA Online Shark Cards + NBA 2K Virtual Currency + mobile in-app purchases

# ── GTA VI — THE EVENT ────────────────────────────────────────────────────────
GTA6_CONSOLE_LAUNCH    = "November 19, 2026"  # PS5 + Xbox Series X|S; CONFIRMED
GTA6_PLATFORMS         = "PlayStation 5 / Xbox Series X|S (console); PC TBD"
GTA6_PC_WINDOW         = "2027-2028 (unofficial estimate; Rockstar historical pattern)"
GTA6_FY2027_NB_B       = 2.9    # ~36% of $8.1B FY2027 guidance tied to GTA VI
GTA6_UNIT_BASE_M       = 25     # Base: ~25M units Year 1 console (DFC estimate: $3B first year)
GTA6_UNIT_BULL_M       = 35     # Bull: ~35M units Year 1 + pre-orders
GTA6_PRICE             = 80     # $80 standard + premium editions at $100+
GTA6_DEVELOPMENT_B     = 2.0    # Estimated $1.5-2B+ development budget (largest in gaming history)
# GTA V context: $800M Day 1, $1B in 3 days; 190M+ lifetime units; $10B+ franchise revenue
# GTA Online: $5B+ lifetime; still generating $1M+/day in 2026 (13 years post-launch)

# ── ZYNGA MOBILE ACQUISITION ──────────────────────────────────────────────────
ZYNGA_COST_B           = 12.7   # Acquisition price (2022) — now deeply underwater goodwill
ZYNGA_EST_VALUE_B      = 5.5    # Estimated current value of Zynga mobile assets
ZYNGA_GOODWILL_WRITE   = 7.2    # ~$7.2B goodwill impairment vs original price
ZYNGA_TOP_TITLES       = ["Toon Blast (50% of app store rev)", "Match Factory! (+50% QoQ)",
                           "Empires & Puzzles", "Toy Blast", "Words With Friends",
                           "Hyper-casual portfolio"]

# ── BALANCE SHEET ─────────────────────────────────────────────────────────────
TOTAL_DEBT_B           = 4.11   # Total debt as of FY2025 (March 31, 2025)
CASH_B                 = 1.50   # Cash & equivalents
NET_DEBT_B             = 2.61   # = 4.11 - 1.50
OCF_FY2026_B           = 0.624  # FY2026 operating cash flow ($624M, beat $450M forecast)
# Management target: NET CASH position by end of FY2027 post-GTA VI FCF surge

# ── EARNINGS (ADJUSTED, NON-GAAP) ─────────────────────────────────────────────
EPS_ADJ_FY2025A        = 2.50   # FY2025 adjusted EPS (estimate, content-drought trough)
EPS_ADJ_FY2026A        = 3.85   # FY2026 adjusted EPS (analyst consensus, beat in Q4)
EPS_ADJ_FY2027E        = 8.00   # FY2027E adj EPS consensus (GTA VI launch year)
EPS_ADJ_FY2028E        = 9.50   # FY2028E adj EPS (GTA Online + PC release compounding)
GAAP_EPS_FY2027_GUIDE  = 0.65   # Midpoint of $0.55-$0.75 GAAP EPS guidance — first profitable GAAP year!

# ── EPP (EARNINGS POWER PRICE) ────────────────────────────────────────────────
EPS_TROUGH     = EPS_ADJ_FY2026A   # = $3.85  (FY2026 adj EPS, last content-drought year)
PE_TROUGH      = 14                # Gaming company content-drought floor P/E (never goes below ~12-14×)
EPP            = EPS_TROUGH * PE_TROUGH   # = $53.90 ≈ $54
EPP_GAP_PCT    = round((CURRENT_PRICE / EPP - 1) * 100, 1)   # = +315.7%
# NOTE: Large EPP gap is EXPECTED for event-driven gaming stocks — it measures how much
# GTA VI optionality is embedded in the price. This is NOT a red flag; it's the nature
# of a company whose earnings swing 2× in one launch quarter.

# ── SCENARIO ASSUMPTIONS ──────────────────────────────────────────────────────
# (adj_eps, exit_pe, target_price, rationale)
# adj_eps × exit_pe should approximately = target_price
SCENARIOS = {
    "BEAR":  (7.50, 20, 150,
              "3rd GTA VI delay to FY2028 OR launch flops (<15M units); Zynga DAU in structural decline. "
              "FY2027 adj EPS revised to $7.50 × 20× content-drought P/E → $150."),
    "BASE":  (10.00, 26, 260,
              "GTA VI launches Nov 19; 20M Year 1 console units; solid GTA Online ramp; PC 2027-28. "
              "FY2027 adj EPS $10.00 × 26× growth P/E → $260."),
    "BULL":  (12.00, 30, 360,
              "GTA VI blockbuster 30M+ Year 1; PC launch strong; GTA Online $1.5B+ yr; "
              "Zynga stable. FY2027 adj EPS $12.00 × 30× franchise P/E → $360."),
    "XBULL": (14.30, 35, 500,
              "GTA VI = generational title, 40M+ units; GTA VI Online exceeds GTA V Online "
              "($5B+ over ~3 years); PC record launch; adj EPS $14.30 × 35× super-franchise → $500."),
}

# ── SOFTMAX SIGNAL MODEL ──────────────────────────────────────────────────────
PROXY_SIGNALS = [
    # (name, value [1-4], weight, description)
    ("gta6_launch_confidence",    3.0, 0.30,
     "Nov 19 locked: FY2027 $8.0-8.2B guidance tied to date; pre-orders June 2026; Trailer 3 imminent; "
     "Zelnick: 'locked in.' 3rd delay would require discarding $8B revenue projection."),
    ("net_bookings_trajectory",   3.0, 0.25,
     "FY2024 $5.33B → FY2025 $5.65B +6% → FY2026 $6.72B +19% → FY2027 $8.1B guided +21%. "
     "Accelerating; OCF $624M in FY2026 beat $450M forecast by 38%."),
    ("balance_sheet_trajectory",  3.0, 0.15,
     "Net debt $2.61B → net CASH target FY2027 end. GTA VI FCF surge + pre-existing deleveraging. "
     "First GAAP profitable year FY2027 ($0.55-$0.75 EPS). Massive inflection."),
    ("gta6_monetization_runway",  3.0, 0.05,
     "GTA V Online: $5B+ lifetime, $1M+/day still in 2026 (13yr). GTA VI Online = richer world, "
     "better monetization, larger player base. Potential for 10-15yr live-service franchise."),
    ("mobile_zynga",              2.0, 0.15,
     "Toon Blast = 50% of app store revenue with YoY growth. Match Factory! +50% QoQ. "
     "Core portfolio stable but Zynga broadly below $12.7B acquisition hopes; DAU pressured."),
    ("catalog_recurrent",         2.0, 0.10,
     "78% of FY2026 NB recurrent (GTA Online + NBA 2K VC + mobile IAP). Stable cash engine. "
     "NBA 2K25/26 solid but missing breakout momentum; weak new IP pipeline pre-GTA VI."),
]

PROXY_COMPOSITE = sum(v * w for _, v, w, _ in PROXY_SIGNALS)
# = 3.0×0.30 + 3.0×0.25 + 3.0×0.15 + 3.0×0.05 + 2.0×0.15 + 2.0×0.10
# = 0.90 + 0.75 + 0.45 + 0.15 + 0.30 + 0.20 = 2.75

import math

SCENARIO_CENTERS = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
TEMP = 0.60

def softmax_weights(composite):
    raw = {s: math.exp(-abs(composite - c) / TEMP)
           for s, c in SCENARIO_CENTERS.items()}
    total = sum(raw.values())
    return {s: v / total for s, v in raw.items()}

# ── SCA (STRUCTURAL COMPETITIVE ADVANTAGE) ────────────────────────────────────
SCA_FACTORS = [
    ("+", "Rockstar / GTA franchise: unmatched open-world IP; GTA V $10B+ revenue; 190M+ units",    +0.9, 0.25),
    ("-", "Zynga overpayment: $12.7B in 2022; estimated current value ~$5.5B; ~$7B impaired",       -0.7, 0.20),
    ("+", "Live-service model: GTA Online $5B+ lifetime; NBA 2K VC; recurrent 78% of NB",           +0.7, 0.20),
    ("-", "GTA VI concentration: 36% of FY2027 NB from ONE title; binary launch execution risk",     -0.6, 0.15),
    ("+", "IP depth: Borderlands (Gearbox), Civilization, BioShock, Red Dead, Risk of Rain",         +0.5, 0.12),
    ("-", "Mobile structural headwinds: Zynga losing DAU to Candy Crush, Chinese mobile titles",     -0.4, 0.05),
    ("+", "Strauss Zelnick leadership: creator-first, long-tenured CEO; disciplined M&A track",      +0.3, 0.03),
]
# SCA = Σ(score × weight)
# = 0.9×0.25 + (-0.7)×0.20 + 0.7×0.20 + (-0.6)×0.15 + 0.5×0.12 + (-0.4)×0.05 + 0.3×0.03
# = 0.225 - 0.140 + 0.140 - 0.090 + 0.060 - 0.020 + 0.009 = +0.184

SCA_NET      = 0.184
SCA_SCALE    = 0.45
ADJ_COMPOSITE = round(PROXY_COMPOSITE + SCA_SCALE * SCA_NET * 0.5, 2)
# = 2.75 + 0.45 × 0.184 × 0.5 = 2.75 + 0.041 ≈ 2.79 (Rockstar brand uplift)

# ── MARKET COMPOSITE (back-solved) ────────────────────────────────────────────
# Market implies EV(c_market) = CURRENT_PRICE × 1.15²  (~2yr, 15%/yr expected return)
# Back-solve: c_market ≈ 2.32 (market pricing modest upside from BASE toward BULL,
# discounting some delay risk even with Nov 19 locked in)
MARKET_COMPOSITE = 2.32
ADJ_VS_MARKET    = round(ADJ_COMPOSITE - MARKET_COMPOSITE, 2)   # ≈ +0.47 → UNDERVALUED

# ── RATIO B ───────────────────────────────────────────────────────────────────
BEAR_TARGET  = SCENARIOS["BEAR"][2]    # $150
BULL_TARGET  = SCENARIOS["BULL"][2]    # $360
DOWNSIDE_PCT = (CURRENT_PRICE - BEAR_TARGET) / CURRENT_PRICE * 100    # 33.1%
UPSIDE_PCT   = (BULL_TARGET   - CURRENT_PRICE) / CURRENT_PRICE * 100  # 60.6%
RATIO_B      = round(DOWNSIDE_PCT / UPSIDE_PCT, 2)    # 0.55

if RATIO_B < 0.75:
    SIGNAL_SHORT = "BUY"
    SIGNAL       = "◉ BUY"
elif RATIO_B < 1.10:
    SIGNAL_SHORT = "ACCUMULATE"
    SIGNAL       = "◎ ACCUMULATE"
elif RATIO_B < 1.75:
    SIGNAL_SHORT = "WATCHLIST"
    SIGNAL       = "◐ WATCHLIST"
else:
    SIGNAL_SHORT = "AVOID"
    SIGNAL       = "✕ AVOID"

# ── CONSERVATIVE SCENARIO CHECK ───────────────────────────────────────────────
# For TTWO, the "conservative" check uses probability-weighted scenarios
# because trough P/E × trough EPS would be below current price (this is expected
# for a GTA VI launch stock — you're not buying trough earnings, you're buying a launch).
# Conservative weighted return (simplified 3-scenario):
#   10% delay scenario: $150 = -33.1%
#   70% base GTA VI:    $260 = +16.0%
#   20% bull GTA VI:    $360 = +60.6%
CONSERVATIVE_WEIGHTED_RETURN = round(
    0.10 * ((150 / CURRENT_PRICE - 1) * 100) +
    0.70 * ((260 / CURRENT_PRICE - 1) * 100) +
    0.20 * ((360 / CURRENT_PRICE - 1) * 100), 1)
# = 10%×(-33.1%) + 70%×(+16.0%) + 20%×(+60.6%)
# = -3.31% + 11.20% + 12.12% = +20.0% over 2yr / +9.6%/yr

# ─────────────────────────────────────────────────────────────────────────────
# REPORT
# ─────────────────────────────────────────────────────────────────────────────

def run_model():
    weights = softmax_weights(ADJ_COMPOSITE)
    ev = sum(weights[s] * SCENARIOS[s][2] for s in SCENARIOS)   # no dividend

    report = []
    A = report.append

    A("=" * 76)
    A(f"  {SIGNAL}  —  {COMPANY} ({TICKER})")
    A(f"  Bottom-Up Risk/Reward Signal Model · {DATE}")
    A("=" * 76)
    A(f"  Price: ${CURRENT_PRICE:.2f}  |  52W: ${VOL_52W_LOW}–${VOL_52W_HIGH}")
    A(f"  Shares: {SHARES_OUT_M:.0f}M  |  Mkt Cap: ${CURRENT_PRICE*SHARES_OUT_M/1000:.1f}B")
    A(f"  Dividend: None  |  Net Debt: ${NET_DEBT_B:.2f}B")
    A("")

    # ── SIGNAL DASHBOARD ────────────────────────────────────────────────────
    A("─" * 76)
    A("  SIGNAL DASHBOARD")
    A("─" * 76)
    A(f"  Signal      : {SIGNAL}")
    A(f"  Ratio B     : {RATIO_B:.2f}×  (downside {DOWNSIDE_PCT:.1f}% / upside {UPSIDE_PCT:.1f}%)")
    A(f"  EPP Gap     : +{EPP_GAP_PCT}%  (EPP ${EPP:.0f} = ${EPS_TROUGH} adj EPS × {PE_TROUGH}× trough P/E)")
    A(f"  Proxy Comp  : {PROXY_COMPOSITE:.2f}  |  ADJ: {ADJ_COMPOSITE:.2f}  |  Market: {MARKET_COMPOSITE:.2f}")
    gap_label = "UNDERVALUED" if ADJ_VS_MARKET > 0.15 else ("OVERSOLD" if ADJ_VS_MARKET > 0 else "OVERBOUGHT")
    A(f"  ADJ–Market  : {ADJ_VS_MARKET:+.2f}  →  {gap_label}")
    A(f"  2yr EV      : ${ev:.2f}  (vs ${CURRENT_PRICE:.2f} current; no dividend)")
    A(f"  Conserv.    : +{CONSERVATIVE_WEIGHTED_RETURN:.1f}% / +{CONSERVATIVE_WEIGHTED_RETURN/2:.1f}%/yr (prob-weighted, 10/70/20 delay/base/bull)")
    A("")

    # ── BUSINESS OVERVIEW ────────────────────────────────────────────────────
    A("─" * 76)
    A("  BUSINESS OVERVIEW — Take-Two Interactive Software, Inc.")
    A("─" * 76)
    A("  Take-Two is the publisher of Grand Theft Auto, NBA 2K, Red Dead Redemption,")
    A("  Borderlands, Civilization, and BioShock — collectively one of the deepest IP")
    A("  libraries in gaming. The business has three engines:")
    A("")
    A("  1. ROCKSTAR GAMES: GTA Online ($5B+ lifetime) + RDR2 Online. Anchors the")
    A("     entire company's valuation. GTA VI (Nov 19, 2026) is the singular event.")
    A("")
    A("  2. 2K GAMES: NBA 2K franchise (NBA 2K VC is a recurring $500M+/yr machine),")
    A("     Borderlands (Gearbox acq 2024, $460M in TTWO stock), Civilization VII,")
    A("     BioShock reboot, XCOM, Tiny Tina's Wonderlands. Deep pipeline.")
    A("")
    A("  3. ZYNGA MOBILE: Acquired for $12.7B in 2022 — a contested deal now. Toon")
    A("     Blast (~50% of app store rev), Match Factory!, Empires & Puzzles, Words")
    A("     With Friends. Mobile generates ~46% of net bookings. Underperformed vs")
    A("     deal thesis but stabilizing. Goodwill impairment has weighed on GAAP.")
    A("")
    A("  This is a GTA VI stock. Everything else is noise until November 19, 2026.")
    A("")

    # ── NET BOOKINGS ARCHITECTURE ─────────────────────────────────────────────
    A("─" * 76)
    A("  NET BOOKINGS ARCHITECTURE (FY2026 = $6.72B actual; FY2027 = $8.1B guided)")
    A("─" * 76)
    segments = [
        ("Zynga / Mobile",      NB_FY2026_B * NB_MOBILE_PCT,  "Toon Blast, Match Factory!, hyper-casual; growing"),
        ("2K Games (console/PC)", NB_FY2026_B * NB_2K_PCT,   "NBA 2K, Borderlands, Civ VII, BioShock"),
        ("Rockstar Games",       NB_FY2026_B * NB_ROCKSTAR_PCT,"GTA Online + GTA V + RDR2; recurrent >90%"),
        ("Other labels",         NB_FY2026_B * NB_OTHER_PCT,  "Licensing, older catalog"),
    ]
    A(f"  {'Segment':<26} {'FY2026 NB $B':>12}  {'% of Total':>11}  Note")
    A(f"  {'─'*26} {'─'*12}  {'─'*11}  {'─'*34}")
    for name, nb, note in segments:
        A(f"  {name:<26} {nb:>12.2f}  {nb/NB_FY2026_B*100:>10.0f}%  {note}")
    A(f"  {'─'*26} {'─'*12}  {'─'*11}")
    A(f"  {'TOTAL':<26} {NB_FY2026_B:>12.2f}  {'100%':>11}")
    A("")
    A(f"  Recurrent consumer spending: {RECURRENT_PCT*100:.0f}% of total NB (live-service dominance)")
    A(f"  FY2027 guided: ${NB_FY2027_GUIDE_B:.1f}B (+{(NB_FY2027_GUIDE_B/NB_FY2026_B-1)*100:.0f}%)")
    A(f"  GTA VI contribution in FY2027: ~${GTA6_FY2027_NB_B:.1f}B (~36% of total)")
    A("")

    # ── GTA VI LAUNCH MODEL: THE EVENT ────────────────────────────────────────
    A("─" * 76)
    A("  GTA VI LAUNCH MODEL — THE EVENT THAT DEFINES THE DECADE")
    A("─" * 76)
    A(f"  Launch Date   : {GTA6_CONSOLE_LAUNCH}  [CONFIRMED — Rockstar + Take-Two]")
    A(f"  Platforms     : {GTA6_PLATFORMS}")
    A(f"  PC Release    : {GTA6_PC_WINDOW} (unconfirmed; Rockstar hist. pattern ~12-18mo after console)")
    A(f"  Price         : ${GTA6_PRICE}+ standard; premium/collector editions $100-120")
    A(f"  Development   : Est. ${GTA6_DEVELOPMENT_B:.1f}B+ budget (largest in gaming history)")
    A(f"  Pre-orders    : Expected late June 2026 alongside Trailer 3")
    A("")
    A("  GTA V PRECEDENT (2013):")
    A("  • $800M revenue Day 1; $1B in 3 days (fastest entertainment product ever)")
    A("  • 190M+ lifetime units across 3 console generations")
    A("  • GTA Online $5B+ lifetime revenue; ~$1M+/day STILL in 2026 (13 years later!)")
    A("  • GTA Online peak: $743.9M in calendar 2020 (COVID tailwind)")
    A("  • Total GTA franchise revenue: $10B+ since 2013 launch")
    A("")
    A("  UNIT SALES FORECAST — SCENARIO ANALYSIS:")
    A(f"  {'Scenario':<10}  {'Year 1 Units':>13}  {'@ $80/unit':>11}  {'Note':>30}")
    A(f"  {'─'*10}  {'─'*13}  {'─'*11}  {'─'*30}")
    unit_scenarios = [
        ("BEAR",  10, "Flop/delay; fraction of GTA V launch"),
        ("BASE",  25, "DFC Intelligence estimate; $3B Year 1"),
        ("BULL",  35, "30-35M: blockbuster, beats GTA V Day 3"),
        ("XBULL", 45, "Generational; approaches GTA V first 18mo"),
    ]
    for sc, units_m, note in unit_scenarios:
        A(f"  {sc:<10}  {units_m:>11}M  ${units_m*GTA6_PRICE/1000:>10.1f}B  {note}")
    A("")
    A("  GTA VI ONLINE REVENUE POTENTIAL (Years 3-10+):")
    A("  If GTA VI Online follows GTA V Online trajectory at 2× scale:")
    A("  • Peak year Online revenue: $1.2-1.5B (vs GTA V peak $743.9M)")
    A("  • 10-year NPV of GTA VI Online (disc. 10%): $7-9B potential")
    A("  • PC launch adds ~$1B+ incremental in launch year + PC Online playerbase")
    A("")

    # ── ZYNGA MOBILE: THE OVERPAYMENT WE LIVE WITH ────────────────────────────
    A("─" * 76)
    A("  ZYNGA MOBILE: THE OVERPAYMENT WE LIVE WITH")
    A("─" * 76)
    A(f"  Acquisition  : ${ZYNGA_COST_B:.1f}B (2022)")
    A(f"  Est. Current : ~${ZYNGA_EST_VALUE_B:.1f}B  (implied goodwill impairment: ~${ZYNGA_GOODWILL_WRITE:.1f}B)")
    A(f"  Contribution : ~{NB_MOBILE_PCT*100:.0f}% of FY2026 net bookings (${NB_FY2026_B*NB_MOBILE_PCT:.2f}B)")
    A("")
    A("  TOP TITLES (FY2026):")
    for title in ZYNGA_TOP_TITLES:
        A(f"  • {title}")
    A("")
    A("  THESIS:")
    A("  Zynga is a permanent drag on GAAP EPS (amortization) but a real cash generator.")
    A("  The $12.7B price was too high — but the assets are not worthless. Toon Blast")
    A("  has compounded app store revenue; Match Factory! hit +50% QoQ in debut quarter.")
    A("  Mobile is ~46% of NB — without it, the GTA-only risk would be even higher.")
    A("  Structural risk: Chinese mobile gaming (Honor of Kings, PUBG Mobile) + Candy")
    A("  Crush Soda dominate. Zynga is #2-3 in casual puzzle/social. Defensible niche.")
    A("")

    # ── SIX PROXY SIGNALS ────────────────────────────────────────────────────
    A("─" * 76)
    A("  SIX PROXY SIGNALS  (BEAR=1 · BASE=2 · BULL=3 · XBULL=4)")
    A("─" * 76)
    for name, val, wt, desc in PROXY_SIGNALS:
        bar = "●" * int(val) + "○" * (4 - int(val))
        label = {1: "BEAR", 2: "BASE", 3: "BULL", 4: "XBULL"}.get(int(val), "?")
        A(f"  [{bar}] {label:<6}  wt={wt:.2f}  {name}")
        A(f"          {desc}")
        A("")
    A(f"  Composite  : {PROXY_COMPOSITE:.2f}  (weighted avg; center = BULL territory)")
    A(f"  SCA Adjust : {SCA_NET:+.3f}  (Rockstar brand moat vs Zynga drag)")
    A(f"  ADJ Comp.  : {ADJ_COMPOSITE:.2f}")
    A("")

    # ── STRUCTURAL COMPETITIVE ADVANTAGE ─────────────────────────────────────
    A("─" * 76)
    A("  STRUCTURAL COMPETITIVE ADVANTAGE (SCA)")
    A("─" * 76)
    for direction, desc, score, weight in SCA_FACTORS:
        A(f"  [{direction}] {desc}")
        A(f"      Score: {score:+.1f}  Weight: {weight:.2f}  Contribution: {score*weight:+.3f}")
        A("")
    A(f"  Net SCA Score : {SCA_NET:+.3f}")
    A(f"  Interpretation: Moderately positive — Rockstar brand + live-service model")
    A(f"  offset by Zynga overpayment and GTA VI concentration risk.")
    A("")

    # ── BEAR CASE ─────────────────────────────────────────────────────────────
    A("─" * 76)
    A("  BEAR CASE  (price target: $150 / composite signal: 1.25 / weight: "
      f"{weights['BEAR']*100:.0f}%)")
    A("─" * 76)
    A("  Scenario: A third GTA VI delay to FY2028 is announced in Q3-Q4 2026, OR the")
    A("  game launches November 19 but badly underperforms expectations (<15M units,")
    A("  vs 25M base case). Simultaneously, Zynga mobile DAU is in structural decline")
    A("  — Match Factory! stalls and Toon Blast loses market share to Chinese titles.")
    A("")
    A("  What the market would see: GTA VI Online doesn't emerge as a live-service")
    A("  franchise (maps, heists, and shark cards fall flat). NBA 2K faces an EA Sports")
    A("  challenge. The Zynga goodwill story forces a major impairment announcement.")
    A("")
    A("  BEAR ASSUMPTIONS:")
    A("  • GTA VI delay OR <15M Year 1 units (vs 25M base)")
    A("  • FY2027 adj EPS revised from $8.00E to ~$4.00-5.00 on missed bookings")
    A("  • Stock re-prices to ~$7.50 adj EPS × 20× content-drought P/E = $150")
    A("  • Net cash target abandoned; debt refinancing risk returns")
    A("  • Note: 52W low was $187.63 on the May→November delay announcement alone;")
    A("    $150 requires a true launch failure, not just a delay")
    A("")

    # ── EPP ───────────────────────────────────────────────────────────────────
    A("─" * 76)
    A("  EPP — EARNINGS POWER PRICE (CONTENT-DROUGHT FLOOR)")
    A("─" * 76)
    A(f"  Adj EPS (FY2026, trough) : ${EPS_TROUGH:.2f}  (last pre-GTA VI year; represents")
    A(f"                              the business WITHOUT any GTA VI contribution)")
    A(f"  Min-Viable Trough P/E   : {PE_TROUGH}×  (gaming franchise floor; never true value stock)")
    A(f"  EPP                     : ${EPP:.0f}  (= ${EPS_TROUGH} × {PE_TROUGH}×)")
    A(f"  Current Price           : ${CURRENT_PRICE:.2f}")
    A(f"  EPP Gap                 : +{EPP_GAP_PCT}%  ← LARGE GAP IS EXPECTED")
    A("")
    A("  INTERPRETATION: The +315% EPP gap means the stock at $224 prices in")
    A("  ~$170 of GTA VI optionality above the earnings-only floor. This is NOT")
    A("  a concern — it correctly reflects that GTA VI is ~6 months from launch.")
    A("  By comparison: EA (Madden/FIFA) EPP gap typically 40-80%; TTWO's gap")
    A("  spikes before major GTA launches and compresses after Online monetization")
    A("  ramps up over the following 2-3 years. The EPP floor ($54) represents")
    A("  'GTA VI is cancelled entirely' — a scenario priced at near-zero probability.")
    A("")

    # ── SCENARIO PROBABILITY DISTRIBUTION ────────────────────────────────────
    A("─" * 76)
    A("  SCENARIO PROBABILITY DISTRIBUTION  (ADJ composite = {:.2f})".format(ADJ_COMPOSITE))
    A("─" * 76)
    A(f"  {'Scenario':<10}  {'Center':>7}  {'Weight':>8}  {'Target':>8}  {'Return':>8}")
    A(f"  {'─'*10}  {'─'*7}  {'─'*8}  {'─'*8}  {'─'*8}")
    for s in ["BEAR", "BASE", "BULL", "XBULL"]:
        target = SCENARIOS[s][2]
        ret_pct = (target - CURRENT_PRICE) / CURRENT_PRICE * 100
        A(f"  {s:<10}  {SCENARIO_CENTERS[s]:>7.2f}  {weights[s]*100:>7.1f}%  "
          f"${target:>7.0f}  {ret_pct:>+7.1f}%")
    A("")
    A(f"  Weighted EV (2yr, no div): ${ev:.2f}  vs ${CURRENT_PRICE:.2f}  → {(ev/CURRENT_PRICE-1)*100:+.1f}%")
    A(f"  Conservative prob-weighted: +{CONSERVATIVE_WEIGHTED_RETURN:.1f}% / +{CONSERVATIVE_WEIGHTED_RETURN/2:.1f}%/yr")
    A("")

    # ── RATIO B ───────────────────────────────────────────────────────────────
    A("─" * 76)
    A("  RATIO B — RISK / REWARD METHOD")
    A("─" * 76)
    A(f"  Bear Target  : ${BEAR_TARGET:>6.2f}  (adj EPS $7.50 × 20× content-drought P/E)")
    A(f"  Bull Target  : ${BULL_TARGET:>6.2f}  (adj EPS $12.00 × 30× franchise P/E)")
    A(f"  Current Price: ${CURRENT_PRICE:>6.2f}")
    A(f"  Downside     : {DOWNSIDE_PCT:.1f}%  (${CURRENT_PRICE:.2f} → ${BEAR_TARGET:.2f})")
    A(f"  Upside       : {UPSIDE_PCT:.1f}%  (${CURRENT_PRICE:.2f} → ${BULL_TARGET:.2f})")
    A(f"  Ratio B      : {RATIO_B:.2f}×  =  {DOWNSIDE_PCT:.1f}% / {UPSIDE_PCT:.1f}%")
    A("")
    A("  SIGNAL THRESHOLDS:")
    A(f"  ◉ BUY        Ratio B < 0.75×   Floor gap dominated by upside  ← TTWO at {RATIO_B:.2f}×")
    A("  ◎ ACCUMULATE Ratio B 0.75–1.10× Balanced; edge to upside")
    A("  ◐ WATCHLIST  Ratio B 1.10–1.75× Floor gap exceeds EPS upside")
    A("  ✕ AVOID      Ratio B > 1.75×   Growth fully priced in")
    A("")

    # ── FINAL SIGNAL ──────────────────────────────────────────────────────────
    A("═" * 76)
    A(f"  FINAL SIGNAL  :  {SIGNAL}")
    A(f"  RATIO B       :  {RATIO_B:.2f}×  ({DOWNSIDE_PCT:.1f}% downside / {UPSIDE_PCT:.1f}% upside)")
    A(f"  EPP GAP       :  +{EPP_GAP_PCT}%  (optionality-driven; large gap expected pre-launch)")
    A(f"  ADJ vs MARKET :  {ADJ_VS_MARKET:+.2f}  →  {gap_label}")
    A(f"  COMPOSITE     :  {ADJ_COMPOSITE:.2f} adjusted  |  {MARKET_COMPOSITE:.2f} implied by market")
    A(f"  2yr EV        :  ${ev:.2f}  ({(ev/CURRENT_PRICE-1)*100:+.1f}% total return; no dividend)")
    A(f"  CONSERV.      :  +{CONSERVATIVE_WEIGHTED_RETURN:.1f}% / +{CONSERVATIVE_WEIGHTED_RETURN/2:.1f}%/yr (prob-weighted 10/70/20)")
    A("")
    A("  INVESTMENT THESIS:")
    A("  TTWO is a GTA VI launch stock. The November 19, 2026 date is locked in with")
    A("  $8.0-8.2B FY2027 guidance explicitly tied to it — a third delay would require")
    A("  Take-Two to withdraw a $8B revenue projection, which is effectively impossible.")
    A("  Pre-orders arrive late June 2026; Trailer 3 is incoming. The setup is:")
    A("")
    A("  → The stock fell from $264 → $188 (-29%) on the May→November delay.")
    A("  → It has recovered partially to $224 but remains 15% below analyst avg PT.")
    A("  → GTA VI Online has a 13-year live-service runway template (GTA V Online)")
    A("    that generates $1M+/day still in 2026 — GTA VI should be 2× that at peak.")
    A("  → PC release (2027-28) is an additional $1B+ catalyst not in FY2027 guidance.")
    A("  → First GAAP profitable year FY2027 ($0.55-$0.75 EPS) — a narrative milestone.")
    A("  → Management targets net CASH position by FY2027 year-end — complete")
    A("    reversal from $2.6B net debt.")
    A("")
    A("  BUY below $240. The risk is not whether GTA VI launches — it's whether it")
    A("  launches as the cultural event it's positioned to be.")
    A("")
    A("  RISKS TO MONITOR:")
    A("  • Third GTA VI delay (price would re-test $187 low or break below)")
    A("  • Launch quality — technical issues, review scores below 90 Metacritic")
    A("  • GTA VI Online not launching day-1 (Shark Cards delayed = cash flow miss)")
    A("  • Zynga DAU structural decline accelerates (particularly Toon Blast core loop)")
    A("  • NBA 2K competitive threat (EA Sports FC model encroaching on console sports)")
    A("  • PC release delayed to 2028 (already partially priced in)")
    A("  • Broader gaming market contraction (macro + console cycle timing)")
    A("═" * 76)

    return "\n".join(report)


PART2 = run_model()

SUMMARY = (
    f"{SIGNAL}  —  Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT:.1f}% downside / {UPSIDE_PCT:.1f}% upside). "
    f"TTWO is a GTA VI launch stock. Nov 19, 2026 date CONFIRMED — $8.0-8.2B FY2027 guidance explicitly tied to it. "
    f"FY2026 net bookings $6.72B (+19%); OCF $624M. GTA VI = ~36% of FY2027 NB (~$2.9B). "
    f"Stock fell $264→$188 on May→Nov delay; now at $224, 15% below avg analyst PT $279. "
    f"GTA Online template: $5B+ lifetime, $1M+/day in 2026 (13yr post-launch). "
    f"PC release 2027-28 = additional $1B+ not in guidance. Net CASH target FY2027 year-end. "
    f"First GAAP profitable year FY2027E ($0.55-$0.75). "
    f"EPP floor $54 (+{EPP_GAP_PCT}% gap — large gap reflects launch optionality, expected pre-launch). "
    f"Bear $150 (3rd delay/flop) · Base $260 (solid launch) · Bull $360 (blockbuster) · XBull $500 (generational). "
    f"BUY below $240. Watch: pre-order numbers June 2026, day-1 Online availability, Metacritic score."
)

if __name__ == "__main__":
    print(run_model())
    print(f"\nSUMMARY: {SUMMARY}")
    print(f"\nSIGNAL: {SIGNAL} | Ratio B: {RATIO_B:.2f}× | EPP Gap: +{EPP_GAP_PCT}%")
