"""
Warner Bros. Discovery, Inc. (NASDAQ: WBD)
Bottom-Up Risk/Reward Signal Model
Analysis Date: 2026-06-03

SIGNAL: ◌ WATCHLIST  |  Ratio B: 1.48×  |  EPP Gap: +352.3%

DEAL ARB + MEDIA RENAISSANCE — BUT MOST UPSIDE ALREADY PRICED IN
Stock tripled from $9.11 (52W low) to $27.14 on two transformative events:
  (1) June 9, 2025: WBD announces split into two companies
      - "Warner Bros." (Streaming+Studios): HBO, Max, DC, WB Pictures, Games → Netflix deal
      - "Discovery Global" (Linear Networks): CNN, TNT/TBS, HGTV, Discovery, Food Network → spins off Q3 2026
  (2) December 5, 2025: Netflix announces $82.7B acquisition of Warner Bros. entity
      - $27.75/share (equity value $72B); includes $5.8B breakup fee
      - $2-3B annual synergies projected by Netflix
      - Close expected: late 2026 / early 2027

At $27.14 vs Netflix deal $27.75/share: spread is ONLY 2.2% on the Netflix consideration.
WBD shareholders also receive Discovery Global shares — but Discovery Global gets the
debt-laden linear TV assets and most of the structural decline. Equity value uncertain.

WATCHLIST because:
- Underlying Warner Bros. business is genuinely excellent (Studios record year; Max profitable)
- MULTIPLE STRATEGIC BIDDERS: Paramount Skydance offered $30 all-cash (rejected as "inferior");
  Amazon and Apple also circled. Strategic floor exists.
- If Netflix deal faces antitrust scrutiny, stock falls to $14-20 range (standalone value)
- NOT A BUY at $27 — wait for pullback to $20-22 on regulatory news for better entry

THE UNDERLYING BUSINESS (what Netflix bought):
- Studios: $4B+ worldwide box office in 2025 (first studio ever, best since 2019)
  Minecraft Movie ($961M), F1 ($600M+), Superman ($619M), Sinners ($200M+)
- Max/Streaming: 131.6M global subscribers; DTC EBITDA doubled to $1.37B in FY2025
- Debt: $54B (merger peak 2022) → $33.5B (FY2025) → $30.1B net (Q1 2026) = $20B+ paydown
- But also: linear TV (-21% EBITDA FY2025), NBA rights lost ($1.1B/yr hit), cord-cutting 9%/yr
"""

import math

# ── IDENTITY ────────────────────────────────────────────────────────────────
TICKER          = "WBD"
COMPANY         = "Warner Bros. Discovery, Inc."
SECTOR          = "Streaming (Max) · Studios · Linear TV (CNN, TNT, TBS) · Netflix Deal · NASDAQ: WBD"
SECTOR_GROUP    = "Telecoms/Media"
ANALYSIS_DATE   = "2026-06-03"

# ── MARKET DATA ─────────────────────────────────────────────────────────────
CURRENT_PRICE   = 27.14    # June 3, 2026 (~$27.14; tripled from $9 52W low)
ANNUAL_DIV      = 0.00     # Dividend suspended 2023; priority is debt paydown
SHARES_OUT_M    = 2507.0   # Diluted shares outstanding
MARKET_CAP_B    = 68.0     # $68B market cap
FW52_HIGH       = 30.00    # 52-week high
FW52_LOW        = 9.11     # 52-week low (pre-Netflix deal announcement)

# ── FY2025 FULL-YEAR FINANCIALS ──────────────────────────────────────────────
REVENUE_FY2025_B       = 37.3    # Down ~5% YoY from $39.3B; linear TV drag
EBITDA_FY2025_B        = 8.7     # Adj EBITDA; down ~3% ex-FX
FCF_FY2025_B           = 3.1     # Burdened by ~$1.35B separation/transaction items
FCF_UNDERLYING_FY2025  = 4.45    # Underlying FCF ex-separation costs
FCF_FY2024_B           = 4.427   # Prior year FCF for comparison
GAAP_NET_INCOME_FY2025 = 0.727   # $727M — FIRST PROFITABLE YEAR (vs -$11.3B FY2024)
GAAP_EPS_FY2025        = 0.29    # $0.29/share on 2507M diluted shares
INTEREST_EXPENSE_FY2025= 2.085   # Billion; annual interest on $33.5B debt

# ── Q1 2026 RESULTS ──────────────────────────────────────────────────────────
REVENUE_Q1_2026_B      = 8.89    # Down 1% YoY
EBITDA_Q1_2026_B       = 2.2     # Up 5% YoY — underlying improvement
GAAP_NET_LOSS_Q1_2026  = 2.9     # $2.9B loss — $2.8B Netflix termination fee (ONE-TIME)
FCF_Q1_2026_B          = -0.476  # Negative due to Netflix termination fee payment

# ── SEGMENT BREAKDOWN (FY2025) ───────────────────────────────────────────────
# Streaming (Max / DTC)
STREAMING_REVENUE_FY2025     = None   # Part of total $37.3B (not fully broken out)
STREAMING_EBITDA_FY2025      = 1.37   # Doubled YoY — streaming is WORKING
STREAMING_SUBS_GLOBAL_FY2025 = 131.6  # Million global subscribers (end FY2025)
STREAMING_SUB_TARGET_2026    = 150.0  # Management target: 150M by end 2026
STREAMING_SUB_ADD_Q1_2025    = 5.0    # Added 5M+ in Q1 2025 alone

# Studios
STUDIOS_EBITDA_FY2025        = 2.55   # Up from FY2024; strong theatrical
STUDIOS_BO_WORLDWIDE_2025    = 4.0    # $4B+ worldwide box office in 2025 (first studio ever)
STUDIOS_FILMS_NO1_2025       = 9      # 9 films debuted #1 at domestic box office
STUDIOS_CONSEC_OVER_40M_2025 = 7      # 7 consecutive films opened >$40M (industry first)
STUDIOS_EBITDA_TARGET_2026   = 3.0    # Management target: at least $3B Studios EBITDA

# Key 2025 Box Office
MINECRAFT_MOVIE_BO_M   = 961.0   # A Minecraft Movie worldwide ($424M domestic)
F1_MOVIE_BO_M          = 600.0   # F1: The Movie worldwide (highest-grossing original of 2025)
SUPERMAN_2025_BO_M     = 619.0   # Superman (DC Studios 2025; $125M opening weekend)
SINNERS_BO_DOMESTIC_M  = 200.0   # Sinners domestic (highest-grossing original since Coco)

# Global Linear Networks — Structural Decline
NETWORKS_EBITDA_CHG_FY2025     = -21    # Networks EBITDA -21% in FY2025
NETWORKS_REV_Q3_2025_PCT       = -22    # Q3 2025 linear network revenue -22% YoY (worst quarter)
LINEAR_CORD_CUTTING_PCT_2025   = -9     # Domestic linear pay-TV subscribers -9%/yr
NBA_RIGHTS_COST_ANN            = 1.2    # WBD was paying $1.2B/yr for NBA rights
NBA_FINANCIAL_IMPACT           = 1.1    # $1.1B annual financial hit from losing NBA to Amazon
NETWORKS_IMPAIRMENT_2024       = 9.1    # $9.1B goodwill impairment on TV Networks Q2 2024

# ── BALANCE SHEET & DEBT ─────────────────────────────────────────────────────
GROSS_DEBT_FY2025     = 33.5    # Billion (end FY2025; down from $54B merger peak in 2022)
NET_DEBT_FY2025       = 29.0    # Billion
CASH_FY2025           = 4.6     # Billion
NET_DEBT_Q1_2026      = 30.1    # Q1 2026 net debt (post Netflix termination fee)
LEVERAGE_FY2025       = 3.3     # Net Debt / Adj EBITDA (FY2025)
LEVERAGE_Q1_2026      = 3.4     # Q1 2026
DEBT_COST_AVG         = 4.7     # % weighted average cost
DEBT_MATURITY_AVG_YRS = 13.9    # Years weighted average maturity (from agent 1)
                                 # Note: Other source cites 5.9yr weighted avg — discrepancy;
                                 # $17B bridge loan (Dec 30, 2026) partially addressed by Q2 2025 tender
DEBT_PEAK_MERGER      = 54.0    # At merger close (April 2022)
DEBT_PAYDOWN_TOTAL    = 20.5    # Total paydown from peak → FY2025 ($54B → $33.5B)
DEBT_SYNERGY_TENDER_Q2_2025 = 14.6  # $14.6B debt tender offer in Q2 2025 (resolved bridge risk)
INVESTMENT_GRADE_TARGET_YEAR = 2027  # Target investment-grade (<3.0x leverage) by end 2027

# ── MERGER SYNERGIES ─────────────────────────────────────────────────────────
SYNERGY_TARGET_ANN    = 4.0     # $4B+ annual run-rate savings achieved (vs $3B initial target)
SYNERGY_RAISED_TO     = 4.3     # Final raised target

# ── NETFLIX DEAL ─────────────────────────────────────────────────────────────
NETFLIX_DEAL_ANNOUNCED      = "December 5, 2025"
NETFLIX_DEAL_EV             = 82.7   # Total enterprise value ($B)
NETFLIX_DEAL_EQUITY         = 72.0   # Equity value ($B)
NETFLIX_DEAL_PER_SHARE      = 27.75  # Per WBD share (cash + Netflix stock)
NETFLIX_DEAL_SPREAD         = NETFLIX_DEAL_PER_SHARE - CURRENT_PRICE  # $0.61 = +2.2%
NETFLIX_BREAKUP_FEE         = 5.8    # Netflix pays WBD if Netflix walks ($5.8B)
NETFLIX_SYNERGIES_ANN       = 2.5    # Netflix projects $2-3B annual cost savings
NETFLIX_DEAL_CLOSE_TARGET   = "Late 2026 / Early 2027"
NETFLIX_ENTITY_ACQUIRED     = "Warner Bros. (Streaming + Studios)"  # NOT Discovery Global

# ── DISCOVERY GLOBAL (Spin-off) ───────────────────────────────────────────────
DISCOVERY_GLOBAL_SPIN_TARGET = "Q3 2026"
DISCOVERY_GLOBAL_CEO         = "Gunnar Wiedenfels (current WBD CFO)"
DISCOVERY_GLOBAL_ASSETS      = "CNN, TNT Sports, TBS, HGTV, Discovery Channel, Food Network, Cartoon Network, Adult Swim, Discovery+, Bleacher Report, international factual"
DISCOVERY_GLOBAL_EBITDA_EST  = 4.8   # Estimated 2025 EBITDA ($B) = WBD total $8.7B - streaming $1.37B - studios $2.55B ≈ $4.78B
DISCOVERY_GLOBAL_DEBT_ALLOC  = "TBD — significant portion of WBD's $33.5B gross debt allocated here"
# Equity value of Discovery Global is UNCERTAIN — depends on debt allocation ratio
# Bear case: heavily debt-laden linear TV → near-zero or negative equity value
# Bull case: 3-4× EBITDA at moderate debt → $5-8/share for WBD shareholders

# ── COMPETING OFFER ──────────────────────────────────────────────────────────
PSKY_COMPETING_OFFER_PER_SHARE = 30.00  # Paramount Skydance all-cash tender for ALL of WBD
PSKY_OFFER_STATUS              = "Rejected by WBD Board as 'inferior' to Netflix deal"
PSKY_OFFER_DATE                = "December 2025"
OTHER_INTERESTED_PARTIES       = ["Amazon", "Apple", "Comcast"]

# ── ANALYST CONSENSUS ─────────────────────────────────────────────────────────
CONSENSUS_PT                 = 29.75   # Median (33 analysts; post-deal revision)
PT_LOW                       = 22.00
PT_HIGH                      = 35.00
FY2026_EBITDA_CONSENSUS      = 8.6     # $8.6B (pre-separation; 23 analysts)
FY2026_EPS_CONSENSUS         = -0.90   # Negative due to deal/transaction charges
FY2027_EPS_CONSENSUS         = 0.05    # First slightly-positive year post-restructuring

# ── SCENARIOS ─────────────────────────────────────────────────────────────────
# BEAR  $14: Netflix deal blocked by DOJ/FCC antitrust (streaming concentration risk);
#            PSKY deal also fails/renegotiates lower; Discovery Global spin still happens
#            but linear TV entity is debt-laden → distressed; Warner Bros. standalone
#            at streaming startup valuation: $3.92B EBITDA × 8× = $31.4B EV, $10B debt → $21.4B equity
#            → $8.53/share standalone... but debt stays consolidated during deal limbo = $14.
#            (Strategic bidders Amazon/Apple still circling = floor above true standalone)
#
# BASE  $29: Netflix deal closes (late 2026/early 2027) at $27.75/share + Discovery Global
#            spins with minimal equity value ($1-2/share — debt-laden linear TV); total $29.
#
# BULL  $36: Netflix deal closes + Discovery Global has real value ($6-8/share after debt
#            allocation — CNN streaming launch, HGTV/Food Network cash flows, international).
#            Total: $27.75 + $7.50 Discovery Global = $35.25 → $36.
#
# XBULL $46: Netflix sweetens deal (regulatory concessions require higher premium);
#            OR competing bid from Amazon/Apple at $35+; Discovery Global trades at 4× EBITDA.
#            Total value per WBD share exceeds $45.
BEAR    = 14.0
BASE    = 29.0
BULL    = 36.0
XBULL   = 46.0

# ── EPP (EARNINGS POWER PRICE) ────────────────────────────────────────────────
# EPP is less meaningful in deal-arb context but calculated for framework consistency.
# Streaming+Studios entity in trough: normalized streaming EBITDA ~$1.5B × 8× = $12B
# Less debt allocation to Warner Bros. entity (~$8B): equity $4B / 2.507B shares = $1.60
# More conservative: use EPS_TROUGH approach
EPS_TROUGH  = 0.50    # Normalized breakeven EPS (ex-impairments, ex-deal costs)
PE_TROUGH   = 12.0    # Streaming company trough multiple
EPP         = EPS_TROUGH * PE_TROUGH   # = $6.00

# ── SCA: STRUCTURAL COMPETITIVE ADVANTAGE ────────────────────────────────────
# Warner Bros. has EXCEPTIONAL content IP moats but is being acquired BY Netflix precisely
# because it can't efficiently monetize them at scale alone. The SCA benefits Netflix.

SCA_FACTORS = {
    # Factor                    : (score,  weight)
    "pricing_power_hbo_brand"   : (+0.20,  0.12),  # HBO commands premium; Max priced well
    "switching_costs_content"   : (+0.15,  0.15),  # GOT/Last of Us/White Lotus create stickiness
    "streaming_network_effects" : (+0.05,  0.10),  # Nascent — Max subscriber base growing
    "content_ip_library"        : (+0.45,  0.20),  # DC/Batman/Superman; Harry Potter; GOT; 100yr WB library
    "studio_production_scale"   : (+0.15,  0.15),  # WB Pictures; HBO; DC Studios; New Line
    "regulatory_moat"           : ( 0.00,  0.13),  # Neutral — deal brings regulatory scrutiny
    "franchise_irreplaceability": (+0.30,  0.15),  # DC Universe, Harry Potter, LotR, GOT — cannot be replicated
}

SCA_NET   = sum(score * weight for score, weight in SCA_FACTORS.values())
SCA_SCALE = 0.45

# ── 6 PROXY SIGNALS ───────────────────────────────────────────────────────────
# Signal   (score 1–4, weight)
# 1=BEAR, 1.5=BEAR+, 2=BASE, 2.5=BASE+, 3=BULL, 3.5=BULL+, 4=XBULL

SIGNALS = {
    # The Netflix deal spread is 2.2% ($27.14 → $27.75). At this tiny spread, new buyers
    # are taking deal risk (regulatory failure → stock falls to $14-20) for minimal arb return.
    # Score 2.0 (BASE) because: PSKY $30 competing bid + Amazon/Apple interest create a floor;
    # Netflix breakup fee $5.8B protects against Netflix walking; deal likely to close.
    # But it's not BUY-level because the spread gives almost no margin of safety.
    "netflix_deal_arb_spread":        (2.0, 0.30),

    # Max DTC EBITDA DOUBLED to $1.37B in FY2025. 131.6M subscribers (vs 116.9M FY2024).
    # Q1 2025 added 5M+ subs in one quarter. Targeting 150M by end 2026.
    # The Last of Us, White Lotus, HBO prestige content driving engagement.
    # Streaming is NOW profitable — this is what Netflix is paying $82.7B for.
    "streaming_max_profitability":    (3.5, 0.20),

    # WBD became the first studio to hit $4B worldwide box office in 2025.
    # 9 of 9 films debuted #1; 7 consecutive films opened >$40M (industry first).
    # Minecraft ($961M), F1 ($600M+), Superman ($619M), Sinners ($200M+).
    # Studios EBITDA $2.55B; management targeting $3B in 2026.
    "studios_theatrical_renaissance": (4.0, 0.20),

    # Linear Networks EBITDA -21% FY2025; Q3 revenue -22% (worst quarter ever).
    # NBA rights lost to Amazon ($1.1B/yr financial hit). Cable cord-cutting -9%/yr.
    # $9.1B goodwill impairment in Q2 2024 confirmed structural decline.
    # Discovery Global will be a heavily debt-laden declining business post-spin.
    "linear_tv_secular_decline":      (1.0, 0.15),

    # Gross debt: $54B (2022 merger) → $33.5B (FY2025) → $30.1B net (Q1 2026).
    # $20B+ paid down in 3.5 years. $14.6B debt tender in Q2 2025 resolved 2026 bridge risk.
    # Avg debt maturity 13.9yr; cost 4.7%; investment-grade target by end 2027.
    # FY2025 was FIRST GAAP-profitable year ($727M). FCF underlying ~$4.45B.
    "debt_paydown_trajectory":        (3.0, 0.10),

    # Competing offers: PSKY $30/share all-cash (HIGHER than Netflix deal!), rejected as "inferior."
    # Amazon and Apple both expressed acquisition interest pre-Netflix deal.
    # Netflix $5.8B breakup fee = meaningful deterrent to Netflix walking away.
    # Multiple bidders create a strategic floor well above standalone fundamentals.
    "strategic_optionality_floor":    (3.5, 0.05),
}

# ── COMPOSITE CALCULATION ─────────────────────────────────────────────────────
def softmax_weights(composite, scenarios, T=0.60):
    centers = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
    raw = {s: math.exp(-abs(composite - centers[s]) / T) for s in scenarios}
    total = sum(raw.values())
    return {s: raw[s] / total for s in scenarios}

PROXY_COMPOSITE = sum(score * weight for score, weight in SIGNALS.values())
ADJ_COMPOSITE   = PROXY_COMPOSITE + SCA_SCALE * SCA_NET * 0.5

scenarios = {"BEAR": BEAR, "BASE": BASE, "BULL": BULL, "XBULL": XBULL}
weights   = softmax_weights(ADJ_COMPOSITE, scenarios)

EV = sum(weights[s] * (scenarios[s] + ANNUAL_DIV) for s in scenarios)

DOWNSIDE_PCT = (CURRENT_PRICE - BEAR) / CURRENT_PRICE * 100
UPSIDE_PCT   = (BULL - CURRENT_PRICE) / CURRENT_PRICE * 100
RATIO_B      = DOWNSIDE_PCT / UPSIDE_PCT

if RATIO_B < 0.75:
    SIGNAL_TEXT  = "◉ BUY"
    SIGNAL_SHORT = "BUY"
    SIGNAL_COLOR = "#4ade80"
elif RATIO_B < 1.10:
    SIGNAL_TEXT  = "◎ ACCUMULATE"
    SIGNAL_SHORT = "ACCUMULATE"
    SIGNAL_COLOR = "#f0b429"
elif RATIO_B < 1.75:
    SIGNAL_TEXT  = "◌ WATCHLIST"
    SIGNAL_SHORT = "WATCHLIST"
    SIGNAL_COLOR = "#60a5fa"
else:
    SIGNAL_TEXT  = "✕ AVOID"
    SIGNAL_SHORT = "AVOID"
    SIGNAL_COLOR = "#f87171"

EPP_GAP_PCT = (CURRENT_PRICE - EPP) / EPP * 100

TARGET_MARKET = CURRENT_PRICE * (1.15 ** 2)
def ev_at_c(c):
    w = softmax_weights(c, scenarios)
    return sum(w[s] * (scenarios[s] + ANNUAL_DIV) for s in scenarios)

lo, hi = 1.0, 4.0
for _ in range(60):
    mid = (lo + hi) / 2
    if ev_at_c(mid) > TARGET_MARKET:
        hi = mid
    else:
        lo = mid
MARKET_COMPOSITE = (lo + hi) / 2
ADJ_VS_MARKET    = ADJ_COMPOSITE - MARKET_COMPOSITE

# Conservative 2yr return: assumes Netflix deal closes and Discovery Global at minimal value
# Max EPS recovery to $0.30 (post-restructuring charges) × 25× streaming PE + dividends
# More practically: Netflix deal closes → $27.75 + Discovery Global $3 = $30.75 total
PRICE_2YR_BASE   = NETFLIX_DEAL_PER_SHARE + 3.0   # Netflix consideration + Discovery Global
RETURN_2YR       = (PRICE_2YR_BASE - CURRENT_PRICE) / CURRENT_PRICE * 100
RETURN_ANN       = (((PRICE_2YR_BASE / CURRENT_PRICE) ** 0.5) - 1) * 100

if __name__ == "__main__":
    SEP = "═" * 76
    sep = "─" * 76

    print(SEP)
    print(f"  {TICKER} — {COMPANY}")
    print(f"  {SECTOR}")
    print(f"  Analysis: {ANALYSIS_DATE}  |  Price: ${CURRENT_PRICE:.2f}  |  52W: ${FW52_LOW:.2f}–${FW52_HIGH:.2f}")
    print(SEP)

    print(f"\n  SIGNAL:  {SIGNAL_TEXT}   Ratio B: {RATIO_B:.2f}×   EPP Gap: {EPP_GAP_PCT:+.1f}%")
    print(f"  EV(model): ${EV:.2f}   Upside: +{UPSIDE_PCT:.1f}%   Downside: -{DOWNSIDE_PCT:.1f}%\n")

    print(sep)
    print("  NETFLIX DEAL STRUCTURE")
    print(sep)
    print(f"  Announced:         {NETFLIX_DEAL_ANNOUNCED}")
    print(f"  What Netflix buys: Warner Bros. (Streaming + Studios entity, post-spin)")
    print(f"  Deal price:        ${NETFLIX_DEAL_PER_SHARE:.2f}/WBD share  (equity value ${NETFLIX_DEAL_EQUITY:.0f}B; EV ${NETFLIX_DEAL_EV:.1f}B)")
    print(f"  Current spread:    ${NETFLIX_DEAL_SPREAD:.2f}/share = {NETFLIX_DEAL_SPREAD/CURRENT_PRICE*100:.1f}% to deal close — TINY")
    print(f"  Breakup fee:       ${NETFLIX_BREAKUP_FEE:.1f}B (Netflix pays WBD if Netflix walks)")
    print(f"  Netflix synergies: ${NETFLIX_SYNERGIES_ANN:.1f}B/yr projected")
    print(f"  Expected close:    {NETFLIX_DEAL_CLOSE_TARGET}")
    print(f"\n  Discovery Global spin-off: {DISCOVERY_GLOBAL_SPIN_TARGET} (pre-conditions Netflix deal)")
    print(f"  Discovery Global gets: {DISCOVERY_GLOBAL_ASSETS[:80]}...")
    print(f"  Discovery Global EBITDA est.: ~${DISCOVERY_GLOBAL_EBITDA_EST:.1f}B BUT heavily debt-laden — equity value TBD")
    print(f"\n  Competing offer: PSKY ${PSKY_COMPETING_OFFER_PER_SHARE:.2f}/share all-cash — {PSKY_OFFER_STATUS}")
    print(f"  Also interested: {', '.join(OTHER_INTERESTED_PARTIES)}")

    print(f"\n{sep}")
    print("  FY2025 FINANCIALS (Consolidated)")
    print(sep)
    print(f"  Revenue:         ${REVENUE_FY2025_B:.1f}B  (YoY: -5%; linear TV drag)")
    print(f"  Adj. EBITDA:     ${EBITDA_FY2025_B:.1f}B  (YoY: -3% ex-FX)")
    print(f"  FCF:             ${FCF_FY2025_B:.1f}B  (underlying ex-separation: ~${FCF_UNDERLYING_FY2025:.2f}B)")
    print(f"  GAAP Net Income: +${GAAP_NET_INCOME_FY2025:.3f}B  ← FIRST PROFITABLE YEAR (vs -$11.3B FY2024)")
    print(f"  Interest:        ${INTEREST_EXPENSE_FY2025:.3f}B/yr")
    print(f"\n  Q1 2026:")
    print(f"    Revenue: ${REVENUE_Q1_2026_B:.2f}B  |  EBITDA: ${EBITDA_Q1_2026_B:.1f}B (+5% YoY)")
    print(f"    Net loss: -${abs(GAAP_NET_LOSS_Q1_2026):.1f}B (dominated by $2.8B Netflix termination fee — ONE-TIME)")
    print(f"    FCF: ${FCF_Q1_2026_B:.3f}B (negative due to same termination fee)")

    print(f"\n{sep}")
    print("  SEGMENT PERFORMANCE")
    print(sep)
    print(f"  ── MAX / DTC STREAMING ──")
    print(f"  Global subscribers: {STREAMING_SUBS_GLOBAL_FY2025:.1f}M  (vs 116.9M FY2024; target {STREAMING_SUB_TARGET_2026:.0f}M by end 2026)")
    print(f"  DTC Adj. EBITDA:   ${STREAMING_EBITDA_FY2025:.2f}B  (DOUBLED YoY — streaming is profitable!)")
    print(f"  Q1 2026 EBITDA:    $438M (+17% ex-FX YoY)")
    print(f"  Content:           The Last of Us, White Lotus, House of the Dragon; HBO brand = premium")
    print(f"\n  ── STUDIOS ──")
    print(f"  Adj. EBITDA FY2025: ${STUDIOS_EBITDA_FY2025:.2f}B  (target: >${STUDIOS_EBITDA_TARGET_2026:.0f}B in 2026)")
    print(f"  Box office 2025:   ${STUDIOS_BO_WORLDWIDE_2025:.0f}B+ worldwide — FIRST STUDIO EVER; best since 2019")
    print(f"    A Minecraft Movie:     ${MINECRAFT_MOVIE_BO_M:.0f}M global")
    print(f"    F1: The Movie:         ${F1_MOVIE_BO_M:.0f}M+ global (highest-grossing original of 2025)")
    print(f"    Superman (DC Studios): ${SUPERMAN_2025_BO_M:.0f}M global")
    print(f"    Sinners:               ${SINNERS_BO_DOMESTIC_M:.0f}M+ domestic (best original since Coco)")
    print(f"  {STUDIOS_FILMS_NO1_2025} films debuted #1; {STUDIOS_CONSEC_OVER_40M_2025} consecutive opens >$40M")
    print(f"  Q1 2026: Studios revenue +31% ex-FX; EBITDA +156% ex-FX to $775M")
    print(f"\n  ── GLOBAL LINEAR NETWORKS — STRUCTURAL DECLINE ──")
    print(f"  FY2025 Networks EBITDA: {NETWORKS_EBITDA_CHG_FY2025}%  (cord-cutting + NBA rights lost)")
    print(f"  Q3 2025 Networks revenue: {NETWORKS_REV_Q3_2025_PCT}% YoY (worst quarter ever)")
    print(f"  NBA rights lost: Amazon won at $1.8B/yr; WBD paying ${NBA_RIGHTS_COST_ANN:.1f}B/yr → $0")
    print(f"  Financial hit from NBA loss: ~${NBA_FINANCIAL_IMPACT:.1f}B/yr in revenue+affiliate leverage")
    print(f"  Pay-TV cord-cutting: {LINEAR_CORD_CUTTING_PCT_2025}% domestic subscriber decline annually")
    print(f"  Replaced NBA with: Big 12 College Football + Basketball; retained NHL + MLB + March Madness")
    print(f"  Goodwill impairment: ${NETWORKS_IMPAIRMENT_2024:.1f}B (Q2 2024) — confirming secular decline")

    print(f"\n{sep}")
    print("  DEBT TRAJECTORY — $20B+ PAID DOWN SINCE MERGER")
    print(sep)
    print(f"  Merger peak (2022): ${DEBT_PEAK_MERGER:.0f}B gross debt")
    print(f"  FY2025 gross debt:  ${GROSS_DEBT_FY2025:.1f}B  |  Net debt: ${NET_DEBT_FY2025:.0f}B  |  Cash: ${CASH_FY2025:.1f}B")
    print(f"  Q1 2026 net debt:   ${NET_DEBT_Q1_2026:.1f}B  |  Leverage: {LEVERAGE_Q1_2026:.1f}× EBITDA")
    print(f"  Total paydown:      ~${DEBT_PAYDOWN_TOTAL:.0f}B in 3.5 years")
    print(f"  Q2 2025 tender:     ${DEBT_SYNERGY_TENDER_Q2_2025:.1f}B single-largest debt action (resolved Dec 2026 bridge)")
    print(f"  Avg debt cost:      {DEBT_COST_AVG:.1f}%  |  Target: investment-grade by end {INVESTMENT_GRADE_TARGET_YEAR}")
    print(f"  Synergies achieved: ${SYNERGY_TARGET_ANN:.1f}B+ annualized (vs ${SYNERGY_TARGET_ANN}B target; initial was $3B)")

    print(f"\n{sep}")
    print("  6 PROXY SIGNALS")
    print(sep)
    labels = {
        "netflix_deal_arb_spread":        "Netflix deal arb spread",
        "streaming_max_profitability":    "Max/DTC streaming profitability",
        "studios_theatrical_renaissance": "Studios theatrical renaissance",
        "linear_tv_secular_decline":      "Linear TV secular decline",
        "debt_paydown_trajectory":        "Debt paydown trajectory",
        "strategic_optionality_floor":    "Strategic optionality / bidder floor",
    }
    for k, (score, weight) in SIGNALS.items():
        bar = "█" * int(score * 5)
        print(f"  {labels[k]:<38}  {score:.1f}  wt={weight:.2f}  {bar}")
    print(f"  {'PROXY COMPOSITE':<38}  {PROXY_COMPOSITE:.4f}")

    print(f"\n{sep}")
    print("  SCA — STRUCTURAL COMPETITIVE ADVANTAGE")
    print(sep)
    sca_labels = {
        "pricing_power_hbo_brand":    "Pricing power (HBO brand premium)",
        "switching_costs_content":    "Switching costs (content stickiness)",
        "streaming_network_effects":  "Network effects (nascent)",
        "content_ip_library":         "Content IP (DC, HP, GOT, 100yr WB library)",
        "studio_production_scale":    "Studio production scale",
        "regulatory_moat":            "Regulatory moat",
        "franchise_irreplaceability": "Franchise irreplaceability (DC, HP, GOT, LotR)",
    }
    for k, (score, weight) in SCA_FACTORS.items():
        print(f"  {sca_labels[k]:<42}  {score:+.2f} × {weight:.2f} = {score*weight:+.4f}")
    print(f"  {'SCA_NET':<42}  {SCA_NET:+.4f}")
    print(f"  ADJ contribution (+0.45 × SCA_NET × 0.5): {SCA_SCALE * SCA_NET * 0.5:+.4f}")

    print(f"\n{sep}")
    print("  COMPOSITE SCORES")
    print(sep)
    print(f"  PROXY_COMPOSITE:   {PROXY_COMPOSITE:.4f}")
    print(f"  ADJ_COMPOSITE:     {ADJ_COMPOSITE:.4f}")
    print(f"  MARKET_COMPOSITE:  {MARKET_COMPOSITE:.4f}  (back-solved from ${CURRENT_PRICE}×1.15²=${TARGET_MARKET:.2f})")
    print(f"  ADJ_VS_MARKET:     {ADJ_VS_MARKET:+.4f}  → {'OVERVALUED' if ADJ_VS_MARKET < -0.3 else 'SLIGHTLY OVERVALUED' if ADJ_VS_MARKET < 0 else 'FAIRLY VALUED' if ADJ_VS_MARKET < 0.2 else 'UNDERVALUED'}")

    print(f"\n{sep}")
    print("  SCENARIO WEIGHTS (softmax at ADJ_COMPOSITE)")
    print(sep)
    for s, price in scenarios.items():
        print(f"  {s:<6}: ${price:>5.0f}  |  P={weights[s]:.4f}  |  contribution: ${weights[s]*price:.2f}")
    print(f"  EV(model) = ${EV:.2f}  vs  current ${CURRENT_PRICE:.2f}  (model premium: {(EV/CURRENT_PRICE-1)*100:+.1f}%)")

    print(f"\n{sep}")
    print("  SIGNAL DETERMINATION")
    print(sep)
    print(f"  Downside to BEAR (${BEAR:.0f}):  -{DOWNSIDE_PCT:.1f}%")
    print(f"  Upside to BULL (${BULL:.0f}):    +{UPSIDE_PCT:.1f}%")
    print(f"  Ratio B = {RATIO_B:.4f} → {SIGNAL_TEXT}")
    print(f"  EPP floor: EPS_T ${EPS_TROUGH:.2f} × PE_T {PE_TROUGH:.1f}× = ${EPP:.2f}  (gap: {EPP_GAP_PCT:+.1f}%; high in deal-arb context)")

    print(f"\n{sep}")
    print("  CONSERVATIVE 2-YEAR RETURN ESTIMATE")
    print(sep)
    print(f"  Base case: Netflix deal closes → ${NETFLIX_DEAL_PER_SHARE:.2f}/share")
    print(f"  + Discovery Global value:      +$3.00/share (conservative; post-debt allocation)")
    print(f"  Total 2yr target:              ${PRICE_2YR_BASE:.2f}")
    print(f"  2-year return:                 {RETURN_2YR:+.1f}%  ({RETURN_ANN:+.1f}%/yr)")
    print(f"  (Includes NO Discovery Global upside beyond $3 — very conservative)")
    print(f"  If Discovery Global worth $7/share: ${NETFLIX_DEAL_PER_SHARE + 7:.2f} total → +{((NETFLIX_DEAL_PER_SHARE+7)/CURRENT_PRICE-1)*100:.1f}%")

    print(f"\n{sep}")
    print("  WHY WATCHLIST — NOT BUY AND NOT AVOID")
    print(sep)
    print("""
  WHY NOT ◉ BUY (at $27.14):
  • Netflix deal spread = 2.2% ($27.14 → $27.75). Essentially zero arb for new buyers.
  • Most of the tripling from $9 → $27 has already happened.
  • Discovery Global equity value is deeply uncertain — debt-heavy linear TV.
  • Antitrust risk: Netflix + Warner Bros. = streaming giant; DOJ may scrutinize.
  • At $27, you're paying for near-certainty of Netflix deal close AND a value
    Discovery Global = near zero. Even small regulatory delay hurts.

  WHY NOT ✕ AVOID (at $27.14):
  • PSKY offered $30/share all-cash — HIGHER than Netflix deal price. That's the floor.
    If Netflix fails, PSKY (or Amazon or Apple) can renew their interest above $20.
  • Netflix deal has a $5.8B BREAKUP FEE if Netflix walks — significant deterrent.
  • Underlying Warner Bros. business is exceptional: Studios record $4B+ box office;
    Max profitable ($1.37B DTC EBITDA, doubling YoY); debt down $20B+ from peak.
  • Deal probability is high (75%+): DOJ antitrust is manageable given Netflix's
    modest US market share in certain segments (WB is studio+streaming, not ISP).

  WATCHLIST RATIONALE:
  The right entry is $20-22 if Netflix deal faces regulatory delay/complication.
  At $22: spread to Netflix deal = 26%, discovery global is still "free", Ratio B drops below 0.75.
  At current $27.14: you're buying 2.2% spread with 48% downside. Wait for a pullback.
  HOLD for existing shareholders — the PSKY $30 offer (all-cash, HIGHER) means you have
  a floor that existing holders should respect. Don't sell $27 paper below $28.

  IDEAL ENTRY POINTS:
  • Below $22: Ratio B drops below 1.0 → ◉ BUY (Netflix deal provides 26% upside)
  • Below $20: Discovery Global becomes a "free" asymmetric option
  • Below $16: Priced as if deal has already failed → ◉ BUY on standalone alone
    (Studios EBITDA $2.55B + Streaming EBITDA $1.37B = $3.92B × 8× EV = $31.4B;
    minus WB entity net debt ~$8B → equity $23.4B / 2.507B = $9.33/share...
    Actually at $16 you're buying a growing streaming studio at ~4× EV/EBITDA)
""")

    print(SEP)
    print(f"""
SUMMARY: WBD ◌ WATCHLIST — Ratio B 1.48× (48.4% downside / 32.7% upside). DEAL ARB + MEDIA \
RENAISSANCE: stock tripled from $9.11 (52W low) to $27.14 on Netflix's $82.7B acquisition of Warner \
Bros. streaming+studios entity ($27.75/share equity; Dec 2025). Spread = 2.2% — most upside already \
priced in. Discovery Global (linear TV spin-off Q3 2026) equity uncertain. UNDERLYING BUSINESS \
EXCEPTIONAL: Studios $4B+ global box office (Minecraft $961M, F1 $600M+, Superman $619M — first \
studio ever to hit $4B); Max 131.6M subs, DTC EBITDA doubled to $1.37B; debt paid down $20B+ to \
$33.5B (3.3× EBITDA). But linear TV structural drag: Networks EBITDA -21%, NBA rights lost ($1.1B \
hit), cord-cutting -9%/yr. FLOOR: PSKY competing offer $30 all-cash (rejected as "inferior"), Amazon \
and Apple also interested; Netflix $5.8B breakup fee. WATCHLIST — BUY on pullback below $22 (Netflix \
deal = 26% upside from there). HOLD existing shares. Bear $14 · Base $29 · Bull $36 · XBull $46.
""")

    print(f"SIGNAL: {SIGNAL_TEXT} | Ratio B: {RATIO_B:.2f}× | EPP Gap: {EPP_GAP_PCT:+.1f}%")
