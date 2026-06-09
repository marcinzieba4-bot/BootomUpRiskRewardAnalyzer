"""
Boeing Company (NYSE: BA) — Bottom-Up Risk/Reward Signal Model
SIGNAL: ◎ ACCUMULATE  |  Ratio B: 0.93×  |  EPP Gap: +108.6%
=======================================================================
THE LAST GREAT AEROSPACE TURNAROUND: either the trade of the decade —
737 MAX + 787 production normalization unlocking $10-15 EPS by 2028-2030
on a $500B backlog in a two-player global duopoly that cannot be disrupted —
or a value trap where extreme leverage, quality culture, and regulatory risk
compound into a prolonged cash-burn cycle diluting equity further. At $195
the asymmetry slightly favors the bull; margin of safety is thin.
"""

# ── Model identity ──────────────────────────────────────────────────────────
TICKER         = "BA"
COMPANY        = "The Boeing Company"
ANALYSIS_DATE  = "2026-06-09"
SECTOR         = "Aerospace & Defense · Commercial Aircraft / Defense Systems / Global Services · NYSE: BA"
SECTOR_GROUP   = "Industrials"

# ── Price & share data ──────────────────────────────────────────────────────
CURRENT_PRICE  = 195.00          # USD — mid-2026, well off 52-wk high, recovering from strikes + quality crisis
ANNUAL_DIV     = 0.00            # dividend suspended Oct 2022, not reinstated
SHARES_OUT_B   = 0.800           # billions — post-$19B equity raise (Oct 2024) + subsequent dilution

FW52_HIGH      = 230.00
FW52_LOW       = 140.00

# ── Scenario prices ─────────────────────────────────────────────────────────
# BEAR  — production ramp stalls again (MAX stays capped, 787 issues resurface),
#         FAA tightens further, defense losses continue, $45B net debt untenable → equity dilution
# BASE  — gradual ramp: MAX to 38/month by end-2026, 787 to 7/month, BDS stabilizes,
#         FCF breakeven by late 2026, $195 fair value on 2027 EPS visibility
# BULL  — accelerated normalization: MAX 42-45/month, 787 10/month by 2027,
#         BDS fixed-price contract losses contained, $10+ EPS visible 2028
# XBULL — full recovery to pre-crisis cadence: MAX 50/month, 787 12/month,
#          defense margin recovery, $13-15 EPS 2029 → multiple re-rate
BEAR           = 130.0
BASE           = 195.0
BULL           = 265.0
XBULL          = 320.0

# ── Earnings Power Price (EPP) floor ────────────────────────────────────────
# EPS_TROUGH: mid-cycle setback scenario — MAX ramp partially reverses,
# Boeing earns ~$5.50/sh on still-depressed but recovering margins (2027-28)
# PE_TROUGH: 17× reflects franchise floor even in adversity (backlog, services)
EPS_TROUGH     = 5.50
PE_TROUGH      = 17.0
EPP            = EPS_TROUGH * PE_TROUGH     # $93.50 — floor price at genuine trough earnings

# ── Conservative 2-year price estimate ──────────────────────────────────────
# 2027E normalized EPS $7.50 × 22× conservative aerospace multiple + $0 div
# Shows genuine near-term risk: even in recovery, stock could lag from current levels
PE_CONSERVATIVE  = 22.0
EPS_FY2026E      = 7.50            # 2027E normalized EPS — 2026 still near breakeven
CONSERVATIVE_PRICE = PE_CONSERVATIVE * EPS_FY2026E + ANNUAL_DIV   # $165.00

# ── Signal computation ───────────────────────────────────────────────────────
import math

DOWNSIDE_PCT   = (CURRENT_PRICE - BEAR) / CURRENT_PRICE
UPSIDE_PCT     = (BULL - CURRENT_PRICE) / CURRENT_PRICE
RATIO_B        = DOWNSIDE_PCT / UPSIDE_PCT

EPP_GAP_PCT    = (CURRENT_PRICE - EPP) / EPP * 100
CONS_RETURN    = (CONSERVATIVE_PRICE - CURRENT_PRICE) / CURRENT_PRICE * 100

if   RATIO_B < 0.75:  SIGNAL = "◉ BUY";        SIGNAL_COLOR = "#4ade80"
elif RATIO_B < 1.10:  SIGNAL = "◎ ACCUMULATE"; SIGNAL_COLOR = "#f0b429"
elif RATIO_B < 1.75:  SIGNAL = "◌ WATCHLIST";  SIGNAL_COLOR = "#60a5fa"
else:                 SIGNAL = "✕ AVOID";       SIGNAL_COLOR = "#f87171"

# ── Bottom-up signal factors ─────────────────────────────────────────────────
# (name, conviction 1-5, weight)
SIGNALS = [
    ("production_ramp_and_737_max_normalization_execution",            2.5, 0.22),
    ("installed_base_and_commercial_aviation_duopoly_backlog",         3.5, 0.20),
    ("global_services_bgs_recurring_revenue_annuity",                  3.5, 0.17),
    ("balance_sheet_leverage_and_cash_burn_duration_risk",             1.5, 0.17),
    ("defense_bds_fixed_price_contract_stabilization",                 2.0, 0.13),
    ("quality_culture_regulatory_faa_and_execution_risk",              1.5, 0.11),
]

# ── Structural Competitive Advantage (SCA) factors ───────────────────────────
SCA_FACTORS = {
    "commercial_aviation_duopoly_and_irreplaceable_500b_backlog":           +0.20,
    "global_services_high_margin_annuity_insulated_from_production_cycle":  +0.14,
    "commercial_air_travel_structural_growth_and_fleet_replacement_demand": +0.12,
    "kelly_ortberg_credible_turnaround_execution_and_culture_reset":        +0.10,
    "extreme_net_debt_45b_and_ongoing_cash_burn_through_2026":              -0.18,
    "production_quality_regulatory_faa_oversight_and_execution_risk":       -0.14,
    "fixed_price_defense_contract_losses_and_bds_segment_drag":             -0.10,
}
SCA_NET = sum(SCA_FACTORS.values())   # +0.14

# ── Weighted conviction score ────────────────────────────────────────────────
WCS = sum(s * w for (_, s, w) in SIGNALS) / sum(w for (_, _, w) in SIGNALS)

# ── EV (model) ───────────────────────────────────────────────────────────────
EV_MODEL = EPP * (1 + SCA_NET) * (1 + UPSIDE_PCT * WCS / 5)

# ── Summary string (used in lambda SUMMARY dict) ────────────────────────────
SUMMARY = (
    f"BA ◎ ACCUMULATE — Ratio B {RATIO_B:.2f}× ({DOWNSIDE_PCT*100:.1f}% downside / "
    f"{UPSIDE_PCT*100:.1f}% upside) | EPP floor ${EPP:.0f} vs. price ${CURRENT_PRICE:.0f} "
    f"(+{EPP_GAP_PCT:.1f}% gap) | "
    "THE LAST GREAT AEROSPACE TURNAROUND: Boeing is either the trade of the decade — "
    "737 MAX + 787 production normalization unlocking $10-15 EPS by 2028-2030 on a $500B+ "
    "backlog in a two-player global duopoly that cannot be disrupted — or a value trap where "
    "extreme leverage (~$45B net debt), quality culture, and regulatory risk compound into a "
    "prolonged cash-burn cycle diluting equity further. "
    "THE FRANCHISE IS UNAMBIGUOUS: ~10,000 Boeing commercial aircraft in service, ~5,500 on "
    "order across 100+ airlines; Global Services (BGS) generating ~$20B revenue at 15%+ EBIT "
    "margins regardless of production — a recurring parts/MRO/data annuity that floors intrinsic "
    "value meaningfully above the bear case; duopoly with Airbus means every customer MUST "
    "place Boeing orders — there is no third commercial-aircraft OEM. "
    "THE HONEST RISK: ~$45B net debt on a company with near-zero FCF through 2026; 737 MAX FAA "
    "cap at 38/month with every production step under regulatory scrutiny; BDS (defense) has "
    "recorded $8B+ in cumulative fixed-price program charges (KC-46, T-7A, MQ-25, 777X); 2026E "
    "EPS still barely positive; equity was diluted ~11% by the Oct 2024 $19B raise. "
    "Conservative 2yr (recovery-path floor): 2027E EPS $7.50 × 22× + $0 div = $165 → -15.4% — "
    "BULL/XBULL require production normalization and $10+ EPS visible by 2028. "
    "KELLY ORTBERG MATTERS: new CEO (Aug 2024) from Rockwell Collins/Collins Aerospace — an "
    "operator, not a financier; early actions (settled machinists strike, cut executive pay, "
    "halted loss-leading defense bids, walked 737 factory floor) signal the culture reset is real. "
    f"Bear ${BEAR:.0f} · Base ${BASE:.0f} · Bull ${BULL:.0f} · XBull ${XBULL:.0f}."
)

# ────────────────────────────────────────────────────────────────────────────
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
    print(f"  Conservative Price (2027E ${EPS_FY2026E:.2f} × {PE_CONSERVATIVE:.0f}×): ${CONSERVATIVE_PRICE:>8.2f}  ({CONS_RETURN:>+.1f}%)")
    print()
    print(f"  Weighted Conviction Score:                         {WCS:>8.2f} / 5.0")
    print(f"  SCA Net:                                           {SCA_NET:>+8.2f}")
    print(f"  EV(model):                               ${EV_MODEL:>8.2f}   Upside: {(EV_MODEL-CURRENT_PRICE)/CURRENT_PRICE*100:>+.1f}%   Downside: {DOWNSIDE_PCT*100:>-.1f}%")
    print()
    print(f"  SIGNAL:  {SIGNAL}   Ratio B: {RATIO_B:.2f}×   EPP Gap: {EPP_GAP_PCT:>+.1f}%")
    print(f"{'='*72}")
    print()

    print("  BOTTOM-UP SIGNAL FACTORS")
    print(f"  {'Factor':<60} {'Conv':>4}  {'Wt':>5}")
    print(f"  {'-'*72}")
    for name, conv, wt in SIGNALS:
        print(f"  {name:<60} {conv:>4.1f}  {wt:>5.0%}")
    print()

    print("  STRUCTURAL COMPETITIVE ADVANTAGE FACTORS")
    for k, v in SCA_FACTORS.items():
        print(f"  {k:<65} {v:>+.2f}")
    print(f"  {'SCA NET':<65} {SCA_NET:>+.2f}")
    print()

    print(f"{'='*72}")
    print()
    print("  WHY THIS IS AN ◎ ACCUMULATE, NOT A ◌ WATCHLIST OR ◉ BUY")
    print()
    print("  NOT ◉ BUY because:")
    print("  • ~$45B net debt on a company generating near-zero or negative FCF —")
    print("    interest expense alone ~$2.2B/yr consuming earnings before they compound")
    print("  • Production ramp is entirely at FAA discretion: a single quality escape")
    print("    can restart the clock on the 38/month cap, as Jan 2024 proved")
    print("  • BDS defense segment has been a serial value destroyer: $8B+ in cumulative")
    print("    fixed-price charges with KC-46, T-7A, MQ-25, 777X still unresolved")
    print("  • Conservative 2yr EPS × multiple floor ($165) is BELOW current price —")
    print("    the stock is priced on 2028 recovery, not near-term fundamentals")
    print("  • Any further FAA action, quality event, or recession hitting air travel")
    print("    demand could compress the timeline and require additional dilutive equity")
    print()
    print("  NOT ◌ WATCHLIST because:")
    print("  • The duopoly moat is structurally unassailable: Airbus and Boeing are the")
    print("    only suppliers of large commercial aircraft on the planet — every airline")
    print("    MUST place orders; there is no substitute and no new entrant in 20+ years")
    print("  • $500B+ backlog = 7 years of revenue visibility; airlines are extending")
    print("    leases and paying premiums for used 737s precisely BECAUSE they cannot")
    print("    get new ones — this is the most valuable order book in manufacturing")
    print("  • Global Services (BGS, ~$20B revenue, ~15%+ EBIT) earns regardless of")
    print("    production rate — parts, MRO, modifications, data analytics on a")
    print("    10,000-aircraft installed base are annuity-like cash flows")
    print("  • Kelly Ortberg is the right CEO at the right time: 10 years as Rockwell/")
    print("    Collins CEO, built the culture that made Collins the gold standard;")
    print("    early actions (settled strike, cut exec pay, halted loss-leading defense")
    print("    bids, walked the factory floor) signal this is a real reset, not PR")
    print("  • Ratio B 0.93× means the risk/reward is asymmetric in favor of the bull:")
    print("    33.3% downside vs. 35.9% upside — not deep value, but tilted right")
    print()
    print("  THE THESIS IN ONE PARAGRAPH:")
    print("  Boeing is the rarest kind of investment: a franchise whose moat is so deep")
    print("  (irreplaceable duopoly, $500B backlog, 10,000-aircraft services annuity)")
    print("  that even serial self-inflicted wounds — MAX crashes, 787 halts, machinists")
    print("  strike, door-plug blowout, $8B+ defense losses — could not destroy the")
    print("  underlying business. The question is not whether Boeing recovers; the")
    print("  question is WHEN and at WHAT dilution cost. At $195, with Ortberg credibly")
    print("  executing, MAX production finally climbing, and 787 rate recovering, the")
    print("  timing risk is beginning to compress. Initiate at ◎ ACCUMULATE; size")
    print("  conservatively given the leverage; add aggressively on any pullback toward")
    print("  $155-170 where Ratio B would approach ◉ BUY territory.")
    print()
    print(f"{'='*72}")
    print()
    print("  SUMMARY (for API / website display):")
    print()
    # Word-wrap the summary for readability
    import textwrap
    for line in textwrap.wrap(SUMMARY, width=70):
        print(f"  {line}")
    print()
