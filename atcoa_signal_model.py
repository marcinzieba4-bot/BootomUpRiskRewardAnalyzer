"""
Atlas Copco AB (Nasdaq Stockholm: ATCO A) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.91×  |  EPP Gap: +50.0%
=======================================================================
THE COMPRESSOR KING WITH A SEMICONDUCTOR SECRET: Atlas Copco is the
world's #1 compressor manufacturer — and at 65%+ of revenue from
aftermarket service, it is less an equipment company than a recurring-
revenue industrial services franchise that happens to sell machines
first. The installed base of 5M+ compressor units in the field creates
a perpetual annuity: every Atlas Copco air compressor sold today adds
a decade of filter, lubricant, and service revenue at 35-40% margins.
The semiconductor secret is the Vacuum Technique division (Edwards,
Brooks Automation) — the world's leading vacuum pump and abatement
supplier to TSMC, Samsung, ASML, and the global wafer fab ecosystem —
which means Atlas Copco has a structural position inside every leading-
edge chip factory on earth, with exposure to AI infrastructure capex
that most industrial investors have not yet fully priced.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "ATCOA"
COMPANY        = "Atlas Copco AB"
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Industrials · Compressors & Vacuum Technology / Industrial Tools & Assembly / Power Technique · Nasdaq Stockholm: ATCO A"
SECTOR_GROUP   = "Industrials"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 165.00          # SEK — Nasdaq Stockholm mid-2026
ANNUAL_DIV     = 4.00            # SEK/yr (~2.4% yield); consistent grower
SHARES_OUT_B   = 4.10            # billions (A + B shares combined)

FW52_HIGH      = 196.00
FW52_LOW       = 132.00

# ── Scenario prices (SEK) ──────────────────────────────────────────────────
# BEAR  — semiconductor downturn cycle 2: TSMC/Samsung capex cuts hit Vacuum
#         Technique 20-25%; compressor demand falls in China industrial
#         slowdown; EUR/USD FX headwind on SEK reporting; 22× trough multiple
# BASE  — cycle normalizes: semiconductor recovery progresses, compressor
#         aftermarket holds, Industrial Technique benefits from EV assembly
#         and aerospace fastening; adj EPS 7.0 SEK × 24× + div = ~172 SEK
# BULL  — vacuum re-rates on AI infrastructure: TSMC advanced packaging,
#         HBM memory, and leading-edge logic capex drives Vacuum Technique
#         to double-digit growth 3-4 years; compressor pricing power confirmed;
#         adj EPS 9+ SEK; multiple re-rates to 27-28×
# XBULL — semiconductor supercycle: Atlas Copco becomes the de facto
#         infrastructure layer for the AI chip ecosystem; vacuum abatement
#         becomes regulatory-mandated globally; US onshoring adds a second
#         geography of greenfield fab construction
BEAR           = 115.0
BASE           = 165.0
BULL           = 220.0
XBULL          = 275.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: severe industrial + semiconductor downturn simultaneously;
# still earns 5.0 SEK on the compressor aftermarket and service base alone
# PE_TROUGH: 22× reflects the quality of the recurring revenue floor —
# this is not a cyclical at 10×, it is a franchise at trough
EPS_TROUGH     = 5.00
PE_TROUGH      = 22.0
EPP            = EPS_TROUGH * PE_TROUGH    # 110.0 SEK

# ── Conservative 2-year price estimate (SEK) ──────────────────────────────
# FY2026E adj EPS ~7.0 SEK × 24× conservative multiple + 4.0 div
PE_CONSERVATIVE  = 24.0
EPS_FY2026E      = 7.00
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV  # 172.0 SEK

# ── Signal computation ─────────────────────────────────────────────────────
DOWNSIDE_PCT   = (CURRENT_PRICE - BEAR) / CURRENT_PRICE
UPSIDE_PCT     = (BULL - CURRENT_PRICE) / CURRENT_PRICE
RATIO_B        = DOWNSIDE_PCT / UPSIDE_PCT

EPP_GAP_PCT    = (CURRENT_PRICE - EPP) / EPP * 100
CONS_RETURN    = (CONSERVATIVE_PRICE - CURRENT_PRICE) / CURRENT_PRICE * 100

if   RATIO_B < 0.75:  SIGNAL = "◉ BUY";        SIGNAL_COLOR = "#4ade80"
elif RATIO_B < 1.10:  SIGNAL = "◎ ACCUMULATE"; SIGNAL_COLOR = "#f0b429"
elif RATIO_B < 1.75:  SIGNAL = "◌ WATCHLIST";  SIGNAL_COLOR = "#60a5fa"
else:                 SIGNAL = "✕ AVOID";       SIGNAL_COLOR = "#f87171"

# ── Bottom-up signal factors ────────────────────────────────────────────────
SIGNALS = [
    ("global_compressor_leadership_and_installed_base_aftermarket_annuity",       4.0, 0.22),
    ("vacuum_technique_semiconductor_fab_infrastructure_and_ai_capex_exposure",   3.5, 0.20),
    ("decentralized_model_high_roic_capital_allocation_and_innovation_culture",   3.5, 0.18),
    ("industrial_tools_ev_assembly_aerospace_fastening_electrification_tailwind", 3.0, 0.17),
    ("pricing_power_service_contract_revenue_visibility_and_margin_resilience",   3.5, 0.13),
    ("china_industrial_slowdown_and_semiconductor_cycle_timing_risk",             2.5, 0.10),
]

# ── Structural Competitive Advantage (SCA) factors ─────────────────────────
SCA_FACTORS = {
    "number_one_global_compressor_share_with_5m_plus_installed_base_annuity":         +0.18,
    "65_pct_plus_aftermarket_service_revenue_recurring_35_to_40_pct_margins":         +0.16,
    "vacuum_technique_edwards_brooks_embedded_in_every_leading_edge_fab":             +0.12,
    "decentralized_180_brand_model_and_atlas_copco_way_operational_discipline":       +0.10,
    "semiconductor_vacuum_cycle_dependency_capex_cuts_hit_20_to_25_pct_volume":       -0.10,
    "premium_26_to_30x_pe_compresses_sharply_on_any_organic_growth_disappointment":   -0.08,
    "china_industrial_exposure_30_pct_asia_revenue_structural_slowdown_risk":         -0.06,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.32

# ── Weighted conviction score ──────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────
SUMMARY = (
    f"ATCOA ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor {EPP:.0f} SEK vs. price {CURRENT_PRICE:.0f} SEK "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE COMPRESSOR KING WITH A SEMICONDUCTOR SECRET: Atlas Copco is the world's #1 compressor "
    "manufacturer — but at 65%+ aftermarket/service revenue it is a recurring-revenue industrial "
    "franchise that happens to sell machines first. Every Atlas Copco compressor sold today adds "
    "a decade of filter, lubricant, and service revenue at 35-40% margins on a 5M+ installed base. "
    "THE VACUUM TECHNIQUE DIVISION IS THE AI INFRASTRUCTURE PLAY: Edwards and Brooks Automation "
    "are the leading vacuum pump and abatement suppliers to TSMC, Samsung, and ASML — every "
    "leading-edge wafer fab on earth runs Atlas Copco vacuum equipment; as AI drives semiconductor "
    "capex toward advanced packaging, HBM memory, and logic node scaling, Vacuum Technique grows "
    "with the AI buildout as essential fab infrastructure. "
    "THE COMPRESSOR AFTERMARKET IS THE PERMANENT FLOOR: compressed air is industrial oxygen — "
    "every factory, hospital, semiconductor fab, and food processor runs on it; the installed base "
    "creates a filter/lubricant/service annuity that is recession-resistant (maintenance, not capex) "
    "and priced at 35-40% EBITA margins. "
    "THE DECENTRALIZED MODEL IS THE CULTURE MOAT: 180 brands, full P&L accountability at brand "
    "level, and the Atlas Copco Way operational system have compounded ROIC above 25% for decades; "
    "this is not a conglomerate — it is a precision-engineered portfolio company. "
    "THE HONEST RISK: 26-30× PE leaves almost no earnings-basis margin of safety — a semiconductor "
    "capex cut cycle (as in 2022-2023) compresses Vacuum Technique 20-25% and the stock de-rates "
    "quickly; China is ~30% of Asia revenue and structural slowdown is real; Industrial Technique "
    "EV assembly exposure benefits from electrification but battery plant capex has been lumpy. "
    f"Conservative 2yr: adj EPS {EPS_FY2026E:.2f} SEK × {PE_CONSERVATIVE:.0f}× + "
    f"{ANNUAL_DIV:.2f} SEK div = {CONSERVATIVE_PRICE:.2f} SEK → {CONS_RETURN:.1f}% — "
    "modest upside on the base case; BULL/XBULL require semiconductor re-rating and AI capex "
    "tailwind confirmation. Accumulate on semiconductor-fear or China-fear pullbacks toward "
    f"138-148 SEK where Ratio B approaches ◉ BUY. "
    f"Bear {BEAR:.0f} · Base {BASE:.0f} · Bull {BULL:.0f} · XBull {XBULL:.0f} (SEK)."
)

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{'='*72}")
    print(f"  {TICKER}  |  {COMPANY}")
    print(f"  {SECTOR}")
    print(f"{'='*72}")
    print(f"  Current Price:                                   {CURRENT_PRICE:>10.2f} SEK")
    print(f"  Annual Dividend:                                 {ANNUAL_DIV:>10.2f} SEK")
    print(f"  52-Week Range:                        {FW52_LOW:.2f} – {FW52_HIGH:.2f} SEK")
    print()
    print(f"  Scenario Prices (SEK):")
    print(f"    Bear:                                          {BEAR:>10.2f}")
    print(f"    Base:                                          {BASE:>10.2f}")
    print(f"    Bull:                                          {BULL:>10.2f}")
    print(f"    XBull:                                         {XBULL:>10.2f}")
    print()
    print(f"  Downside (current → bear):                    {DOWNSIDE_PCT*100:>7.1f}%")
    print(f"  Upside   (current → bull):                    {UPSIDE_PCT*100:>7.1f}%")
    print(f"  Ratio B = {RATIO_B:.4f} → {SIGNAL}")
    print()
    print(f"  EPS Trough:                                    {EPS_TROUGH:>10.2f} SEK")
    print(f"  PE Trough:                                       {PE_TROUGH:>8.1f}×")
    print(f"  EPP (Earnings Power Price):                    {EPP:>10.2f} SEK")
    print(f"  EPP Gap (current vs. EPP floor):              {EPP_GAP_PCT:>+8.1f}%")
    print()
    print(f"  Conservative Price ({EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}×):       {CONSERVATIVE_PRICE:>10.2f} SEK  ({CONS_RETURN:>+.1f}%)")
    print()
    print(f"  Weighted Conviction Score:                         {WCS:>8.2f} / 5.0")
    print(f"  SCA Net:                                           {SCA_NET:>+8.2f}")
    print(f"  EV(model): {EV_MODEL:>8.2f} SEK   Upside: {(EV_MODEL-CURRENT_PRICE)/CURRENT_PRICE*100:>+.1f}%   Downside: -{DOWNSIDE_PCT*100:.1f}%")
    print()
    print(f"  SIGNAL:  {SIGNAL}   Ratio B: {RATIO_B:.2f}×   EPP Gap: {EPP_GAP_PCT:>+.1f}%")
    print(f"{'='*72}")
    print()

    print("  BOTTOM-UP SIGNAL FACTORS")
    print(f"  {'Factor':<64} {'Conv':>4}  {'Wt':>5}")
    print(f"  {'-'*72}")
    for name, conv, wt in SIGNALS:
        print(f"  {name:<64} {conv:>4.1f}  {wt:>5.0%}")
    print()

    print("  STRUCTURAL COMPETITIVE ADVANTAGE FACTORS")
    for k, v in SCA_FACTORS.items():
        print(f"  {k:<68} {v:>+.2f}")
    print(f"  {'SCA NET':<68} {SCA_NET:>+.2f}")
    print()

    print(f"{'='*72}")
    print()
    print("  WHY THIS IS AN ◎ ACCUMULATE, NOT A ◌ WATCHLIST OR ◉ BUY")
    print()
    print("  NOT ◉ BUY because:")
    print("  • 26-30× PE leaves no margin of safety on an earnings basis:")
    print("    Atlas Copco at 165 SEK is priced for continued compounding,")
    print("    not for a margin of safety — if semiconductor capex cuts repeat")
    print("    (as in 2022-2023) or China industrial deteriorates further, the")
    print("    stock can de-rate to 22-24× trough EPS in 6-12 months rapidly")
    print("  • Semiconductor cycle exposure is real and has duration: Vacuum")
    print("    Technique (Edwards/Brooks) saw 20-25% revenue declines in the")
    print("    2022-2023 memory inventory correction; another capex pause from")
    print("    TSMC, Samsung, or SK Hynix would compress near-term earnings")
    print("    and trigger a multiple de-rating simultaneously (double hit)")
    print("  • China structural slowdown: ~30% of Asia revenue with Chinese")
    print("    industrial customers facing genuine demand deterioration; some")
    print("    compressor market share gains by domestic Chinese competitors")
    print("    (Kaishan, Fusheng) in mid-tier price segments are structural")
    print("  • Conservative 2yr floor (+4.2%) is modest — not a screaming buy")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The aftermarket annuity is genuinely extraordinary: 65%+ of")
    print("    revenue from service/aftermarket means Atlas Copco's earnings")
    print("    floor in any industrial recession is far higher than peers —")
    print("    the 5M+ installed compressor base generates filter, lubricant,")
    print("    and service revenue whether or not new orders are strong")
    print("  • Vacuum Technique is structurally early in the AI cycle: every")
    print("    advanced logic, HBM memory, and advanced packaging node requires")
    print("    more vacuum chambers, more abatement systems, and more process")
    print("    steps — the semiconductor content per dollar of AI compute is")
    print("    rising, and Atlas Copco is inside every leading-edge fab")
    print("  • The decentralized model compounds ROIC: 25%+ ROIC sustained for")
    print("    decades is not luck — it is the Atlas Copco Way operational")
    print("    system, 180 brand-level P&L accountability, and a culture that")
    print("    treats acquisitions as businesses to improve, not to integrate")
    print("    into a monolith; this is one of the best-managed industrials on")
    print("    earth and that premium is partially, not fully, priced in")
    print("  • Ratio B 0.91× — 30.3% downside / 33.3% upside — modestly")
    print("    asymmetric to the upside; add on semiconductor or China fear")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Atlas Copco is the rare industrial that earns premium multiples")
    print("  on genuine quality: #1 compressor globally, 65%+ recurring")
    print("  aftermarket revenue, 25%+ ROIC sustained for decades, and a")
    print("  vacuum technology division that is infrastructure for every")
    print("  leading-edge semiconductor fab on earth. At 165 SEK — 30.3%")
    print("  from bear, 33.3% from bull — you are buying a premium franchise")
    print("  at a premium price. The semiconductor secret (Edwards/Brooks)")
    print("  means AI infrastructure capex flows directly into Atlas Copco")
    print("  earnings; the compressor aftermarket means the floor is real.")
    print("  Accumulate steadily. Add aggressively on semiconductor-cycle")
    print("  fear selloffs toward 138-148 SEK. This is a forever holding.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
