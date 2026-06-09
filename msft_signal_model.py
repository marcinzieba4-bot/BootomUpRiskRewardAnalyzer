"""
Microsoft Corporation (NASDAQ: MSFT) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 1.00×  |  EPP Gap: +161.4%
=======================================================================
THE ENTERPRISE OPERATING SYSTEM FOR THE AI ERA: Microsoft has achieved
something almost without precedent in the history of technology — it
became the dominant platform of one era (personal computing, Windows/
Office), was nearly killed by the internet transition (mid-2000s), and
then became the dominant platform of the next era (enterprise cloud,
Azure/Microsoft 365) under Satya Nadella. Now it is positioned to be
the dominant platform of the third era: AI infrastructure and enterprise
AI deployment. The OpenAI partnership — $13B+ invested, exclusive Azure
deployment rights, 49% economic interest before a certain return threshold
— gives Microsoft a structural position inside the most capable AI model
development organization on earth, with the commercial distribution
engine of Azure and Microsoft 365 to monetize it. The Copilot layer
($30/seat/month on top of M365 E3/E5) across 400M+ paid enterprise seats
is the most credible enterprise AI monetization story in existence. Azure
at 22%+ cloud market share growing 30%+ is compounding share on AWS and
building AI-specific infrastructure (Azure OpenAI Service, AI Foundry)
that creates migration friction and switching costs exceeding even the
already-high costs of moving workloads between cloud providers.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "MSFT"
COMPANY        = "Microsoft Corporation"
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Technology · Cloud Infrastructure / Enterprise Software / AI Platforms · NASDAQ: MSFT"
SECTOR_GROUP   = "Technology"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 460.00          # USD — mid-2026
ANNUAL_DIV     = 3.32            # USD/yr (~0.7% yield); 20+ consecutive years of growth
SHARES_OUT_B   = 7.44            # billions; consistent buybacks

FW52_HIGH      = 510.00
FW52_LOW       = 385.00

# ── Scenario prices ───────────────────────────────────────────────────────────
# BEAR  — AI monetization disappoints at enterprise scale: Copilot adoption
#         stalls as productivity gains prove hard to demonstrate in ROI terms;
#         Azure growth decelerates to mid-teens as hyperscaler capex cycle peaks
#         and enterprise cloud spending moderates; OpenAI relationship fractures
#         or open-source models (Llama, Mistral) commoditize AI inference;
#         multiple compresses from 33× to 22× on growth deceleration; adj EPS
#         $8-9 × 22× → ~$195-200; but Berkshire-class balance sheet prevents worse
# BASE  — steady AI compounding: Azure grows 25-28%, M365 Copilot reaches
#         15-20% enterprise penetration (60-80M seats at $30/month), adj EPS
#         $15.50 × 30× + div → ~$468; Microsoft sustains premium multiple on
#         durability of enterprise revenue and AI platform leadership
# BULL  — AI monetization inflects: Copilot reaches 30%+ enterprise penetration;
#         Azure AI workloads (inference, fine-tuning, RAG architectures) become
#         the primary growth driver replacing traditional cloud lift-and-shift;
#         adj EPS $20+ × 32×; GitHub Copilot enterprise expands; Dynamics 365
#         wins ERP share from SAP/Oracle on AI differentiation
# XBULL — Microsoft as AI operating system: Copilot becomes the default
#         interface for enterprise work globally; Azure AI infrastructure
#         earns toll-road economics on every enterprise AI deployment;
#         adj EPS $26+ by FY2029; P/FCF re-rates as AI margins confirmed
BEAR           = 295.0
BASE           = 460.0
BULL           = 625.0
XBULL          = 800.0

# ── Earnings Power Price (EPP) floor ─────────────────────────────────────────
# EPS_TROUGH: AI monetization fails + cloud deceleration + macro enterprise
# spending cuts; still earns ~$8 on the Windows/Office/Azure installed base
# PE_TROUGH: 22× reflects Microsoft at genuine trough — the enterprise
# software franchise retains premium multiple even under stress; not a
# commodity business at trough, a temporarily slowed compounder
EPS_TROUGH     = 8.00
PE_TROUGH      = 22.0
EPP            = EPS_TROUGH * PE_TROUGH    # $176.00

# ── Conservative 2-year price estimate ────────────────────────────────────────
# FY2026E adj EPS ~$15.50 × 30× conservative multiple + $3.32 div
PE_CONSERVATIVE  = 30.0
EPS_FY2026E      = 15.50
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV  # $468.32

# ── Signal computation ─────────────────────────────────────────────────────────
DOWNSIDE_PCT   = (CURRENT_PRICE - BEAR) / CURRENT_PRICE
UPSIDE_PCT     = (BULL - CURRENT_PRICE) / CURRENT_PRICE
RATIO_B        = DOWNSIDE_PCT / UPSIDE_PCT

EPP_GAP_PCT    = (CURRENT_PRICE - EPP) / EPP * 100
CONS_RETURN    = (CONSERVATIVE_PRICE - CURRENT_PRICE) / CURRENT_PRICE * 100

if   RATIO_B < 0.75:  SIGNAL = "◉ BUY";        SIGNAL_COLOR = "#4ade80"
elif RATIO_B < 1.10:  SIGNAL = "◎ ACCUMULATE"; SIGNAL_COLOR = "#f0b429"
elif RATIO_B < 1.75:  SIGNAL = "◌ WATCHLIST";  SIGNAL_COLOR = "#60a5fa"
else:                 SIGNAL = "✕ AVOID";       SIGNAL_COLOR = "#f87171"

# ── Bottom-up signal factors ────────────────────────────────────────────────────
SIGNALS = [
    ("azure_22pct_cloud_share_30pct_growth_and_ai_workload_infrastructure_leadership",  4.5, 0.22),
    ("microsoft_365_enterprise_lock_in_400m_seats_and_copilot_30_per_seat_monetization",4.5, 0.22),
    ("openai_partnership_exclusive_azure_deployment_and_ai_platform_first_mover",       4.0, 0.20),
    ("github_100m_developer_network_and_linkedin_1b_professional_data_moat",            3.5, 0.18),
    ("valuation_33_to_36x_forward_earnings_requires_sustained_15pct_plus_eps_growth",  3.0, 0.18),
]

# ── Structural Competitive Advantage (SCA) factors ─────────────────────────────
SCA_FACTORS = {
    "azure_ai_infrastructure_openai_service_and_ai_foundry_switching_cost_compounding": +0.20,
    "microsoft_365_400m_enterprise_seats_and_copilot_monetization_layer_locked_in":     +0.18,
    "openai_13b_plus_investment_exclusive_azure_deployment_and_ai_model_access":        +0.16,
    "github_100m_developers_and_linkedin_1b_professional_network_data_flywheel":        +0.10,
    "windows_70pct_desktop_os_and_enterprise_identity_active_directory_foundation":     +0.08,
    "33_to_36x_forward_pe_leaves_no_margin_of_safety_growth_miss_punishes_harshly":    -0.12,
    "amazon_aws_first_mover_and_google_gemini_compete_for_ai_workloads_intensifying":  -0.08,
    "regulatory_antitrust_scrutiny_on_openai_concentration_and_bundling_practices":    -0.06,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.46

# ── Weighted conviction score ──────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ─────────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string ─────────────────────────────────────────────────────────────
SUMMARY = (
    f"MSFT ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE ENTERPRISE OPERATING SYSTEM FOR THE AI ERA: Microsoft achieved something unprecedented — "
    "dominant platform of personal computing (Windows/Office), nearly killed by internet "
    "transition, became dominant platform of enterprise cloud (Azure/M365) under Nadella, now "
    "positioned as dominant platform of AI deployment. The OpenAI partnership ($13B+, exclusive "
    "Azure deployment, 49% economic interest) gives Microsoft the most capable AI model "
    "organization inside the most powerful enterprise distribution engine. "
    "THE COPILOT MONETIZATION IS THE BIGGEST NEAR-TERM CATALYST: $30/seat/month on top of "
    "M365 E3/E5 across 400M+ paid enterprise seats is the most credible enterprise AI "
    "monetization in existence — even 20% penetration at $30/month adds $28B+ in high-margin "
    "annual recurring revenue. AZURE AI IS THE INFRASTRUCTURE MOAT: Azure OpenAI Service, "
    "AI Foundry, and inference endpoints create switching costs on top of already-high cloud "
    "migration costs; every enterprise that trains or deploys on Azure becomes progressively "
    "harder to move. GITHUB COPILOT AND LINKEDIN ADD NETWORK EFFECTS: 100M+ developers "
    "default to GitHub for code; every Copilot-assisted line of code reinforces Azure/MSFT "
    "toolchain stickiness. "
    "THE HONEST RISK: 33-36× forward PE leaves essentially zero margin of safety — any "
    "quarter where Azure growth decelerates below 25% or Copilot seat adoption misses "
    "expectations triggers a meaningful de-rating; open-source AI models (Llama 4, Mistral) "
    "commoditizing inference is the structural bear case; AWS and Google Cloud are formidable "
    "AI infrastructure competitors with comparable model capabilities. "
    f"Conservative 2yr: adj EPS ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}× + "
    f"${ANNUAL_DIV:.2f} div = ${CONSERVATIVE_PRICE:.2f} → {CONS_RETURN:.1f}% — "
    "thin at current price; BULL requires Copilot penetration inflecting and Azure AI "
    "workloads becoming the primary growth driver. Accumulate steadily; add on AI-fear "
    f"or macro-fear selloffs toward $395-415. "
    f"Bear ${BEAR:.0f} · Base ${BASE:.0f} · Bull ${BULL:.0f} · XBull ${XBULL:.0f}."
)

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{'='*72}")
    print(f"  {TICKER}  |  {COMPANY}")
    print(f"  {SECTOR}")
    print(f"{'='*72}")
    print(f"  Current Price:                                     ${CURRENT_PRICE:>8.2f}")
    print(f"  Annual Dividend:                                   ${ANNUAL_DIV:>8.2f}")
    print(f"  52-Week Range:                          ${FW52_LOW:.2f} – ${FW52_HIGH:.2f}")
    print()
    print(f"  Scenario Prices:")
    print(f"    Bear:                                            ${BEAR:>8.2f}")
    print(f"    Base:                                            ${BASE:>8.2f}")
    print(f"    Bull:                                            ${BULL:>8.2f}")
    print(f"    XBull:                                           ${XBULL:>8.2f}")
    print()
    print(f"  Downside (current → bear):                    {DOWNSIDE_PCT*100:>7.1f}%")
    print(f"  Upside   (current → bull):                    {UPSIDE_PCT*100:>7.1f}%")
    print(f"  Ratio B = {RATIO_B:.4f} → {SIGNAL}")
    print()
    print(f"  EPS Trough:                                        ${EPS_TROUGH:>8.2f}")
    print(f"  PE Trough:                                         {PE_TROUGH:>8.1f}×")
    print(f"  EPP (Earnings Power Price):                        ${EPP:>8.2f}")
    print(f"  EPP Gap (current vs. EPP floor):              {EPP_GAP_PCT:>+8.1f}%")
    print()
    print(f"  Conservative Price ({EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}×):         ${CONSERVATIVE_PRICE:>8.2f}  ({CONS_RETURN:>+.1f}%)")
    print()
    print(f"  Weighted Conviction Score:                         {WCS:>8.2f} / 5.0")
    print(f"  SCA Net:                                           {SCA_NET:>+8.2f}")
    print(f"  EV(model): ${EV_MODEL:>8.2f}   Upside: {(EV_MODEL-CURRENT_PRICE)/CURRENT_PRICE*100:>+.1f}%   Downside: -{DOWNSIDE_PCT*100:.1f}%")
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
    print("  • 33-36× forward PE at $460 leaves no margin of safety: the")
    print("    entire bull case — Copilot at 30%+ penetration, Azure AI")
    print("    acceleration, OpenAI relationship sustaining — must materialize")
    print("    to justify the current multiple; if any one of these disappoints")
    print("    the stock reprices quickly to 25-28× on revised estimates")
    print("  • Conservative 2yr return (+1.8%) is the thinnest in the Technology")
    print("    universe: at $460 you are paying for the bull case, not the base")
    print("    case; the 0.7% dividend yield does nothing to compensate for")
    print("    the valuation risk carried")
    print("  • Open-source AI model commoditization is the real bear: Llama 4,")
    print("    Mistral, and DeepSeek-class models running on commodity hardware")
    print("    could commoditize the inference layer that Azure AI monetizes;")
    print("    if foundation model capability becomes a utility, Azure's AI")
    print("    premium pricing erodes — not the infrastructure, but the AI")
    print("    value-add that justifies the premium over AWS")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • SCA_NET = +0.46 is among the highest in the entire model")
    print("    universe: Azure + M365 + OpenAI + GitHub + LinkedIn represents")
    print("    a concentration of durable competitive advantages that is")
    print("    genuinely exceptional — each moat reinforces the others through")
    print("    data flywheels, switching costs, and network effects")
    print("  • The Copilot monetization math is enormous: 400M M365 seats ×")
    print("    20% Copilot penetration × $30/month × 12 = $28.8B incremental")
    print("    ARR at ~70%+ gross margin — this is not a speculative scenario,")
    print("    it is a mathematical outcome of enterprise adoption reaching a")
    print("    fraction of the installed base")
    print("  • Nadella's track record of platform transitions removes execution")
    print("    risk discount: Azure from zero to #2 in cloud in a decade,")
    print("    Teams from zero to 320M+ DAU in 4 years, GitHub Copilot from")
    print("    zero to the default developer AI tool in 2 years — this")
    print("    management team has demonstrated AI platform execution")
    print("  • Ratio B 1.00× — perfectly balanced downside/upside — sits at")
    print("    the center of ACCUMULATE; the quality of the business earns")
    print("    the premium, the valuation prevents the BUY rating")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Microsoft is the only company that has successfully navigated two")
    print("  platform transitions (PC → Cloud → AI) from a position of")
    print("  dominance. At $460 — 35.9% from bear, 35.9% from bull — you are")
    print("  paying a full price for the best-positioned enterprise AI platform")
    print("  on earth. SCA_NET +0.46, WCS 3.95 — the highest conviction scores")
    print("  in the technology sector in this model. The conservative case is")
    print("  thin (+1.8%); the bull and xbull cases require Copilot monetization")
    print("  inflecting and Azure AI compounding. Accumulate steadily; add hard")
    print("  on any AI-disappointment or macro selloffs toward $395-415 where")
    print("  the risk/reward improves meaningfully.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
