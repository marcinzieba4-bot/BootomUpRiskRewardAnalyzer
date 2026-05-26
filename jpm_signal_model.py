"""
JPMorgan Chase & Co. (NYSE: JPM) — BottomUp Risk/Reward Signal Model

SIGNAL:  ▷ HOLD/TRIM
RATIO B: 2.27x  (Method B $26 × 15× = $390; ratio 187.40/82.60 = 2.27×)
DATE:    2026-05-26

NOTE: EPS figures are GAAP diluted with one-time items flagged.
"Normalized" EPS excludes significant one-time items (FBR gain FY2023,
Visa gain FY2024). Banks are valued on P/TBV vs ROTCE and P/E vs
through-cycle earning power — both frameworks shown below.
"""

import math

TICKER  = "JPM"
COMPANY = "JPMorgan Chase & Co."
SECTOR  = "Global Banking · Investment Banking · Commercial Banking · Asset & Wealth Management · Markets"

# ── current price (Yahoo Finance range, 2026-05-26) ──────────────────────
CURRENT_PRICE  = 307.40   # JPM — fetched from Yahoo Finance, 2026-05-26
PRICE_52W_LOW  = 256.00
PRICE_52W_HIGH = 337.25
SHARES_M       = 2680.0   # diluted shares outstanding (B-equivalents; ~2.68B)
DIVIDEND_ANN   = 6.00     # $1.50/quarter; raised from $1.25 in 2024

# ── EPS history — GAAP diluted; one-time items noted ─────────────────────
EPS_FY2022 = 12.09   # GAAP; depressed by ~$6B credit reserve builds (pre-recession preparation)
EPS_FY2023 = 16.23   # GAAP; includes ~$2.77B after-tax First Republic bargain purchase gain
EPS_FY2024 = 19.75   # GAAP; includes ~$7.9B Visa Class B share exchange gain (~$2.24/share boost)
EPS_FY2025 = 20.02   # GAAP; relatively clean; FY2025 Q4 had some normalization items
EPS_NOW    = 22.00   # FY2026E consensus ~$22.43; Q1 2026 actual $5.94 (+17% YoY) → annualised ~$23.76

# Normalized EPS (excluding major one-time items):
#   FY2022 norm: ~$14.00 (add back $6B reserve build net-of-tax → +$1.67/sh)
#   FY2023 norm: ~$15.30 (ex $2.77B FBR bargain gain)
#   FY2024 norm: ~$17.50 (ex $7.9B Visa gain; ~$2.24/share adjustment)
#   FY2025 norm: ~$20.02 (no material exclusions)

# ── special bank metrics ──────────────────────────────────────────────────
TBV_PER_SHARE     = 108.87   # tangible book value per share (Q1 2026; +8% YoY)
BOOK_PER_SHARE    = 128.38   # book value per share (Q1 2026; +8% YoY)
ROTCE             = 23.0     # return on tangible common equity (Q1 2026 annualised)
CET1_RATIO        = 14.3     # standardised CET1 capital ratio (Q1 2026; req. ~11.5%)
NII_GUIDANCE_FY26 = 103.0    # FY2026 NII guidance in $B (trimmed from $104.5B at Q1 2026)
IB_FEES_Q1_26     = 2.9      # Q1 2026 investment banking fees $B (+28% YoY)
MARKETS_REV_Q1_26 = 13.4     # Q1 2026 markets revenue $B (IB + FICC + equities; +20% YoY)

# ── EPP — earnings power price (structural floor) ─────────────────────────
EPS_TROUGH = 12.00   # severe US recession: NII -20% ($103B→$82B), credit costs 3× normal
                     # (~$24B provisions vs ~$8B normal), markets revenue -25%.
                     # Net income impact: ~-$28B → EPS ~$12.
                     # Calibration: JPM COVID FY2020 GAAP EPS ~$8.88 (included ~$15B
                     # reserve builds); FY2022 reserve-build year: $12.09.
                     # $12 = GFC-severity with today's fortress balance sheet.
EPP_MIN_PE =   10    # Bank-level trough P/E with premium for fortress balance sheet.
                     # Standard big bank trough P/E: 8-9×. JPM +1pt premium because:
                     # (1) 14.3% CET1 = 250bps above requirement = fortress buffer;
                     # (2) $291B excess capital; (3) ROTCE 23% > peers by 5-10pts.
EPP = EPS_TROUGH * EPP_MIN_PE   # $120.00

# ── Method B — 2-year normalised upside ceiling ───────────────────────────
CONS_EPS_2YR = 26.00   # FY2027E: FY2026E $22.43 × 1.10 organic + buyback boost ($12-15B/yr
                       # → ~4-5% share count reduction) + IB upcycle = ~$26/share.
                       # Street FY2027E varies $24-26; using upper end of range assuming
                       # M&A pipeline conversion and continued markets strength.
CONS_EXIT_PE =    15   # Peak-cycle P/E for JPM. Historical range: 9-16×. JPM has
                       # briefly touched 15-16× at market peaks (2019, late-2024).
                       # Requires continued ROTCE leadership + NII resilience.
                       # At 15×: implied P/TBV = 15 × $26 / ($108.87 × 1.10) = 3.26×
                       # (aggressive; needs sustained ROTCE >20%).
price_b = CONS_EPS_2YR * CONS_EXIT_PE   # $390.00

ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
# = (307.40 - 120.00) / (390.00 - 307.40) = 187.40 / 82.60 = 2.27×
# → ▷ HOLD/TRIM

epp_gap_pct = (CURRENT_PRICE - EPP) / EPP * 100
# = (307.40 - 120) / 120 × 100 = 156.2%

# P/TBV metrics
ptbv_current = CURRENT_PRICE / TBV_PER_SHARE          # 2.83× (expensive for a bank)
ptbv_bull    = price_b / (TBV_PER_SHARE * 1.10)       # ~3.26× (requires multiple expansion)
ptbv_floor   = EPP / TBV_PER_SHARE                    # 1.10× (near-book floor in severe stress)

# ── price scenarios ───────────────────────────────────────────────────────
PRICE_BEAR  = 120    # = EPP. GFC-level repeat: NII collapse, credit cycle, ROTCE <10%.
                     # P/TBV: 1.10× (JPM COVID low was ~1.0× TBV in March 2020: ~$93).
PRICE_BASE  = 320    # FY2027E $23.50 × 13.5× = $317; rounded $320.
                     # Multiple holds flat; NII stays ~$100-103B; IB normalises.
                     # +4% from current — a grinding compounder via buybacks, not price.
PRICE_BULL  = 390    # = price_b. FY2027E $26 × 15×. IB fee upcycle ($14B+); buybacks
                     # drive EPS above consensus; multiple expands to 15× on sustained ROTCE.
                     # P/TBV: ~3.26×. Requires continued top-of-cycle conditions.
PRICE_XBULL = 480    # FY2028-29E $30+ × 16×. Dimon/successor deploys $50B+ excess capital
                     # into transformative deal OR Fed cuts drive NII recovery +$8B.
                     # ROTCE holds 20%+; re-rated to 16× P/E. P/TBV: ~3.8×.
                     # Requires 2+ years of continued outperformance + favourable rate cycle.

# ── SCA (stock-specific composite adjustment) ────────────────────────────
SCA_FACTORS = [
    # (description, score, weight)
    ("IB upcycle / $3.5T M&A pipeline: IB fees +28% Q1; M&A backlog at record; IPO window reopening; advisory + DCM + ECM all accelerating", +0.35, 0.25),
    ("ROTCE leadership + $12-15B buybacks: 23% ROTCE = best big US bank; buybacks shrink float ~5%/yr; EPS mechanical boost", +0.25, 0.20),
    ("NII headwind — Fed cuts: FY2026 NII trimmed to $103B; each 25bps cut = ~$1.5-2B NII drag; 2 more cuts priced = $3-4B headwind (~$0.85/share)", -0.30, 0.25),
    ("Valuation premium (P/TBV 2.83×): highest since pre-GFC era; historical avg ~1.7-2.0×; re-rating to 1.8× TBV = ~$196 in a risk-off cycle", -0.25, 0.20),
    ("Dimon succession overhang: no named successor; Dimon flagged retirement 'in a few years'; institutional premium for Dimon may compress 5-8%", -0.15, 0.10),
]

sca_raw = sum(s * w for _, s, w in SCA_FACTORS)   # -0.0025
sca_adj = sca_raw / 2.0                             # -0.001 (≈ 0)

# ── softmax scenario engine ───────────────────────────────────────────────
SCENARIOS = {
    "BEAR":  {"price": PRICE_BEAR,  "centre": 1.25},
    "BASE":  {"price": PRICE_BASE,  "centre": 2.00},
    "BULL":  {"price": PRICE_BULL,  "centre": 2.75},
    "XBULL": {"price": PRICE_XBULL, "centre": 3.75},
}
T = 0.60

def softmax_weights(composite):
    logits = {k: -((composite - v["centre"]) ** 2) / T for k, v in SCENARIOS.items()}
    m = max(logits.values())
    exps = {k: math.exp(v - m) for k, v in logits.items()}
    s = sum(exps.values())
    return {k: exps[k] / s for k in exps}

def expected_price(composite):
    w = softmax_weights(composite)
    return sum(w[k] * SCENARIOS[k]["price"] for k in SCENARIOS)

def infer_composite(target_price, lo=1.0, hi=4.0, iterations=60):
    for _ in range(iterations):
        mid = (lo + hi) / 2
        if expected_price(mid) < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

market_composite = infer_composite(CURRENT_PRICE)
adj_composite    = market_composite + sca_adj

# ── signal classification ─────────────────────────────────────────────────
def classify(rb):
    if   rb < 0.75: return "◉ BUY"
    elif rb < 1.10: return "◎ ACCUMULATE"
    elif rb < 1.75: return "◐ WATCHLIST"
    elif rb < 2.50: return "▷ HOLD/TRIM"
    else:           return "✕ AVOID"

signal = classify(ratio_b)   # ▷ HOLD/TRIM

# ════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    W = softmax_weights(adj_composite)
    exp_p = expected_price(adj_composite)

    print("=" * 72)
    print(f"  {TICKER}  —  {COMPANY}")
    print(f"  {SECTOR}")
    print("=" * 72)

    print("""
PART 1 — FRAMEWORK OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Special context: JPMorgan Chase is valued using two complementary lenses:
  (1) P/E vs through-cycle earnings power — standard EPP/Method B framework
  (2) P/TBV vs ROTCE — the bank-specific valuation anchor (Gordon Growth model)
Both lenses currently signal HOLD/TRIM.

  P/TBV (current)  : 2.83×  (TBV/share $108.87; expensive for a bank)
  P/TBV (EPP floor): 1.10×  (EPP $120 / TBV $108.87)
  P/TBV (Method B) : ~3.26×  (price_b $390 / 2027E TBV ~$120)
  ROTCE (Q1 2026)  : 23.0%  (best-in-class US big bank; BAC ~14%, WFC ~15%)
  CET1 ratio       : 14.3%  (fortress; 250bps above ~11.5% requirement)
  Dividend yield   : 1.95%  ($6.00 annual / $307.40)""")

    print(f"""
EPP (Earnings Power Price) — structural floor
  = EPS_TROUGH × EPP_MIN_PE
  Stress EPS ($12.00) × 10× trough P/E = ${EPP:.2f}.
  $12/share represents a severe recession: NII -20% (~$103B→$82B),
  credit provisions 3× normal (~$24B vs $8B), markets revenue -25%.
  This is GFC-severity with today's fortress balance sheet (CET1 14.3%,
  $291B in excess capital). COVID FY2020 GAAP EPS was ~$8.88 including
  $15B reserve builds — stress scenario $12 is realistic for modern JPM.
  The 10× trough P/E reflects a 1pt premium over generic bank trough (8-9×)
  for the fortress capital position and best-in-class ROTCE.
  EPP = ${EPP:.2f}.  P/TBV at EPP = {ptbv_floor:.2f}× (near book value; extreme scenario).
  Calibration: 52-wk low $256 ÷ $12 = 21.3× stress EPS — JPM's correction
  low was 21× stressed EPS, confirming the $120 EPP floor is a true catastrophe
  scenario, not a near-term trading floor.

Method B — 2-year normalised upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E ~$26.00 (FY2026E $22.43 + 10% organic + buyback-driven share
  reduction ~5%/yr; IB upcycle contribution) × 15× exit P/E (peak-cycle
  for JPM; historically touched 15-16× briefly in 2019 and late-2024)
  = ${price_b:.2f}.
  Ratio B = (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f}) = ${CURRENT_PRICE-EPP:.2f} / ${price_b-CURRENT_PRICE:.2f} = {ratio_b:.2f}×
  → {signal}. JPM is an exceptional franchise fairly/fully priced.
  Method B upside: +{(price_b/CURRENT_PRICE-1)*100:.1f}% to ${price_b:.0f}. Downside to EPP: -{(1-EPP/CURRENT_PRICE)*100:.1f}%.
  Risk/reward: asymmetric on the downside. Hold existing; don't add.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

    print("""
PART 2 — ANALYST COMMENTARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

JPMORGAN CHASE: THE WORLD'S PREMIER BANK — BUT HOW MUCH PREMIUM IS ENOUGH?
============================================================================

JPMorgan Chase is, by virtually every measure, the finest large bank on
earth. It has the highest ROTCE among major US banks (23% vs BAC ~14%,
WFC ~15%, C ~12%), the largest and most profitable investment banking
franchise (#1 global wallet share for 5 consecutive years), a retail
banking network of 5,000+ branches serving 82M US households, and a
balance sheet so fortified (CET1 14.3%, $291B excess capital) that it
was the only major US bank that never needed government capital during
the GFC.

The analytical question in May 2026 is not "is JPM a great bank?" — it
clearly is. The question is: "At $307.40, 2.83× TBV, and 13.7× FY2026E
EPS, has the greatness already been priced in?"

The answer, per this model, is: largely yes. HOLD/TRIM.

Q1 2026 — RECORD PROFITS; DIMON WARNS OF TREACHEROUS GEOPOLITICS
=================================================================
  Net income:          $16.5B (+13% YoY; record Q1)
  Diluted EPS:         $5.94 (+17% YoY; beat est $5.46 by 8.8%)
  Revenue (managed):   $50.5B (+8% YoY; beat est $49.2B)
  NII:                 $25.5B (+9% YoY; beat est $25.3B)
  IB fees:             $2.9B (+28% YoY; advisory/ECM/DCM all surging)
  Markets revenue:     $13.4B (+20% YoY; FICC +21%, Equities strong)
  ROTCE:               23% (annualised; best-in-class)
  CET1 ratio:          14.3% (fortress; 250bps above requirement)

The quarter was a genuine beat across the board. However, JPM trimmed
its FY2026 NII guidance to $103B (from $104.5B) — acknowledging that
the interest rate environment is incrementally less favourable. This
single guidance trim drove the stock -4% on earnings day despite the
EPS beat, illustrating how rate-sensitive JPM's valuation has become.

Jamie Dimon's commentary in the annual shareholder letter (Apr 2026)
continued his pattern of macro caution: "The world may be entering one
of the most treacherous geopolitical eras since World War II." This is
not Dimon being dramatic — he has been more right than wrong on macro
calls over 15 years. His caution explains JPM's elevated capital buffers
(14.3% CET1 vs ~11.5% required) and selective deployment posture.

THE NII EQUATION: RATE SENSITIVITY IS THE KEY VARIABLE
======================================================
Net Interest Income is JPM's single largest revenue line (~$103B
guided for FY2026, or ~51% of total revenue). Rate sensitivity:
  - Each 25bps Fed rate cut  →  ~$1.5-2.0B annual NII reduction
  - Market currently pricing 2 more Fed cuts in H2 2026
  - Potential NII impact: -$3-4B (reduces EPS ~$0.80-1.00/share)
  - This is manageable but not immaterial

Against this NII headwind, JPM has structural offsets:
  - Loan growth: commercial + consumer loan demand recovering
  - Deposit repricing: as rates fall, funding costs decline faster
    than asset yields in some scenarios (positive repricing gap)
  - Buybacks: $12-15B/yr reduces float ~5% → partly offsets EPS hit
  - Fee income: IB + markets + AWM provide NII diversification

JPM is NOT a pure interest rate bet. Even if NII declines modestly,
IB fees, markets, AWM, and card services provide diversification that
BAC and WFC lack at the same scale.

THE INVESTMENT BANKING MACHINE: M&A SUPERCYCLE LOADING
======================================================
JPMorgan's Corporate & Investment Bank (CIB) is in the early stages of
what could be a multi-year IB fee upcycle:

  Q1 2026 IB fees:  $2.9B (+28% YoY) — strongest IB quarter in years
  M&A advisory:     +35% — $3.5T pending M&A pipeline reported by Reuters
  DCM/ECM:          Both surging as companies refinance and issue equity
  Global IB wallet: JPM #1 for 5th consecutive year

The $3.5T M&A backlog is the key variable. If half of this converts to
closed transactions in 2026-2027, JPM's advisory fees alone could add
$3-4B annually above recent trough levels. Combined with ECM/DCM
revival, total IB revenues could reach $12-14B/yr vs $8-9B in 2022-23.
At JPM's ~30% incremental margin, that's $1.2-1.4B after-tax = ~$0.50/
share additional EPS. Not transformative, but meaningful.

The risk: M&A pipelines can freeze. A recession, tariff escalation, or
regulatory crackdown on mega-deals could stall the upcycle in weeks.
This is why the IB contribution is a positive SCA factor but not a
core thesis.

THE VALUATION TENSION: P/TBV vs ROTCE
=====================================
The Gordon Growth model for bank valuation:
  Warranted P/TBV = (ROTCE - g) / (Ke - g)
  Where: ROTCE=23%, g=4% (sustainable growth), Ke=9% (cost of equity)
  Warranted P/TBV = (23% - 4%) / (9% - 4%) = 19% / 5% = 3.8×

At 3.8× warranted P/TBV, current 2.83× looks CHEAP by this math!
However, the model assumptions are aggressive:
  - Ke=9% assumes risk-free rate stays low (Fed eventually cuts to ~3-3.5%)
  - g=4% assumes JPM grows its tangible book at 4%/yr (achievable via retained earnings)
  - The dangerous assumption: ROTCE=23% is a PEAK metric

If ROTCE mean-reverts to 16% in a recession (conservative for JPM):
  Warranted P/TBV = (16% - 4%) / (9% - 4%) = 12% / 5% = 2.4×
  Implied price: 2.4× × $108.87 TBV = $261 — 15% below current

If ROTCE = 12% (moderate stress):
  Warranted P/TBV = (12%-4%)/(9%-4%) = 1.6× → $174 implied price

This analysis confirms the asymmetric risk profile:
  - UPSIDE (if ROTCE stays 20%+): 3.5-4× TBV = $380-435 → modest additional upside
  - DOWNSIDE (ROTCE to 16% recession): 2.4× TBV = $261 → -15%
  - SEVERE DOWNSIDE (ROTCE to 12%): 1.6× TBV = $174 → -43%

At current prices, you're buying peak-cycle ROTCE at peak-cycle P/TBV.
The margin of safety is thin. This is what the ratio_b of 2.27× is
quantifying.

THE DIMON QUESTION
==================
Warren Buffett at Berkshire. Tim Cook at Apple. Jamie Dimon at JPM.
There are a handful of leaders who command a visible premium in their
stock price. Dimon has been at JPM since 2005 and has navigated: the
GFC (JPM bought Bear Stearns and WaMu at crisis prices), the Whale
trading scandal ($6B loss, Dimon called it a "tempest in a teapot"),
Dodd-Frank regulatory overhaul, COVID, and the FBR acquisition in 48
hours. His strategic instincts have been consistently superior.

In his April 2026 shareholder letter, Dimon signalled a retirement
timeline of "a few years." The named internal candidates (Marianne
Lake, Daniel Pinto, Mary Erdoes) are capable executives. But a CEO
transition at JPM, whenever it occurs, will temporarily compress the
institutional premium that Dimon commands. We estimate 5-8% of JPM's
current P/TBV premium reflects the "Dimon factor." This is a modest
risk but non-trivial.

ENTRY/EXIT FRAMEWORK
====================
  ◉ BUY            : $195-220  (1.8-2.0× TBV; ROTCE implies 2.0× warranted)
  ◎ ACCUMULATE     : $240-270  (2.2-2.5× TBV; near 52-wk lows; dividend 2.2-2.5%)
  ◐ WATCHLIST      : $270-295  (2.5-2.7× TBV; awaiting catalyst)
  ▷ HOLD/TRIM (now): $295-325  (2.7-3.0× TBV; approaching full value)
  ✕ TRIM HARD      : >$325     (above 52-wk high territory; Method B ceiling $390)

The 52-wk low of $256 in late 2025 (during broader market selloff)
was a strong ACCUMULATE entry (2.35× TBV, 11.7× FY2026E). That
opportunity has largely passed. Current $307 = HOLD existing position.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

    print("PART 3 — NUMBERS & SIGNALS")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    print("""
  I. PRICE & VALUATION SNAPSHOT
  ----------------------------------------------------------------------""")
    pct_from_low  = (CURRENT_PRICE - PRICE_52W_LOW) / PRICE_52W_LOW * 100
    pct_from_high = (CURRENT_PRICE - PRICE_52W_HIGH) / PRICE_52W_HIGH * 100
    mktcap_b      = CURRENT_PRICE * SHARES_M / 1000
    print(f"  Current price   : ${CURRENT_PRICE:.2f}  (52-wk range: ${PRICE_52W_LOW:.2f}–${PRICE_52W_HIGH:.2f})")
    print(f"  vs 52-wk low    : +{pct_from_low:.1f}%   |   vs 52-wk high: {pct_from_high:.1f}%")
    print(f"  Market cap      : ~${mktcap_b:.0f}B   |   Shares (B-eq): {SHARES_M/1000:.2f}B")
    print(f"  Dividend (ann)  : ${DIVIDEND_ANN:.2f}   |   Yield: {DIVIDEND_ANN/CURRENT_PRICE*100:.2f}%")
    print(f"  TBV per share   : ${TBV_PER_SHARE:.2f}  |   P/TBV: {ptbv_current:.2f}×")
    print(f"  Book per share  : ${BOOK_PER_SHARE:.2f}  |   P/Book: {CURRENT_PRICE/BOOK_PER_SHARE:.2f}×")
    print(f"  ROTCE (Q1 2026) : {ROTCE:.1f}%     |   CET1 ratio: {CET1_RATIO:.1f}%")
    print(f"  NII guidance    : ${NII_GUIDANCE_FY26:.0f}B (FY2026)  |  IB fees Q1: ${IB_FEES_Q1_26:.1f}B (+28% YoY)")
    fwd_pe = CURRENT_PRICE / EPS_NOW
    print(f"  Forward P/E     : {fwd_pe:.1f}×  (on FY2026E ${EPS_NOW:.2f})")

    print(f"""
  II. EPS HISTORY (GAAP diluted; one-time items noted)
  ----------------------------------------------------------------------
  FY2022  : ${EPS_FY2022:.2f}  (reserve builds ~$6B; normalized ~$14.00)
  FY2023  : ${EPS_FY2023:.2f}  (First Republic bargain gain ~$2.77B AT; norm ~$15.30)
  FY2024  : ${EPS_FY2024:.2f}  (Visa Class B gain ~$7.9B pre-tax; norm ~$17.50)
  FY2025  : ${EPS_FY2025:.2f}  (relatively clean; through-cycle run rate)
  FY2026E : ${EPS_NOW:.2f}  (consensus ~$22.43; Q1 actual $5.94 × 4 = $23.76 annualised)
  FY2027E : ${CONS_EPS_2YR:.2f}  (used for Method B; ~+16% from FY2026E)
  Q1 2026 : $5.94  (beat est $5.46; +17% YoY; ROTCE 23%)

  III. EPP & METHOD B
  ----------------------------------------------------------------------
  EPS_TROUGH  : ${EPS_TROUGH:.2f}/share  (severe recession; GFC-severity with fortress balance sheet)
  EPP_MIN_PE  : {EPP_MIN_PE}×          (bank trough P/E + fortress premium)
  EPP (floor) : ${EPP:.2f}       (= ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×)
  EPP gap     : +{epp_gap_pct:.1f}%    (current price is {epp_gap_pct/100:.1f}× above EPP floor)

  CONS_EPS_2YR: ${CONS_EPS_2YR:.2f}/share  (FY2027E; organic + buyback-boosted)
  CONS_EXIT_PE: {CONS_EXIT_PE}×          (peak-cycle P/E for best-in-class bank)
  Method B    : ${price_b:.2f}       (= ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×)
  Upside to B : +{(price_b/CURRENT_PRICE-1)*100:.1f}%
  Downside EPP: -{(1-EPP/CURRENT_PRICE)*100:.1f}%

  ┌─────────────────────────────────────────────────────────────────────┐
  │  RATIO B = ({CURRENT_PRICE:.2f} − {EPP:.2f}) / ({price_b:.2f} − {CURRENT_PRICE:.2f})               │
  │           = {CURRENT_PRICE-EPP:.2f} / {price_b-CURRENT_PRICE:.2f} = {ratio_b:.2f}×                               │
  │  SIGNAL   = {signal:<35}              │
  └─────────────────────────────────────────────────────────────────────┘""")

    print(f"""
  IV. STOCK-SPECIFIC COMPOSITE ADJUSTMENT (SCA)
  ----------------------------------------------------------------------
  {'Factor':<52}  {'Score':>6}  {'Wt':>6}  {'Contrib':>7}""")
    print(f"  {'─'*52}  {'──────'}  {'──────'}  {'───────'}")
    for desc, score, weight in SCA_FACTORS:
        contrib = score * weight
        print(f"  {desc[:52]:<52}  {score:>+6.2f}  {weight:>6.2f}  {contrib:>+7.3f}")
    print(f"  {'─'*52}  {'──────'}  {'──────'}  {'───────'}")
    print(f"  {'SCA raw':<52}  {'':>6}  {'':>6}  {sca_raw:>+7.3f}")
    print(f"  {'SCA adj (÷2.0)':<52}  {'':>6}  {'':>6}  {sca_adj:>+7.3f}")

    print(f"""
  V. COMPOSITE INFERENCE
  ----------------------------------------------------------------------
  Market composite  : {market_composite:.3f}  (BASE)
  Adj composite     : {adj_composite:.3f}  (BASE)
  Softmax weights at adj composite ({adj_composite:.3f}):
    BEAR  : {W['BEAR']*100:.1f}%  (${PRICE_BEAR})
    BASE  : {W['BASE']*100:.1f}%  (${PRICE_BASE})
    BULL  : {W['BULL']*100:.1f}%  (${PRICE_BULL})
    XBULL : {W['XBULL']*100:.1f}%  (${PRICE_XBULL})
  Expected price (adj): ${exp_p:.1f}  vs current ${CURRENT_PRICE:.2f}  (Δ {(exp_p/CURRENT_PRICE-1)*100:+.1f}%)

  VI. SCENARIOS SUMMARY
  ----------------------------------------------------------------------
  BEAR  (${PRICE_BEAR}) : GFC-level repeat. NII collapses -20% ($103B→$82B); credit
               provisions triple to ~$24B (vs $8B normal); markets revenue -25%;
               ROTCE drops to 8-10%. Warranted P/TBV at 10% ROTCE = ~1.0-1.1×.
               CET1 14.3% means JPM SURVIVES but EPS craters to ~$12.
               EPP = $12 × 10× = $120. -{(1-PRICE_BEAR/CURRENT_PRICE)*100:.0f}%.

  BASE  (${PRICE_BASE}) : Soft landing. NII holds ~$100-103B as rate cuts offset by loan
               growth; IB fees normalise to $10-11B/yr; credit costs stay benign
               ~$8-10B; ROTCE 18-20%; buybacks reduce float 5%/yr.
               FY2027E $23.50 × 13.5× = $317 → $320. +{(PRICE_BASE/CURRENT_PRICE-1)*100:.0f}%.
               JPM grinds higher via buybacks, not price multiple expansion.

  BULL  (${PRICE_BULL}) : M&A supercycle + NII resilience. IB fees surge to $14-16B/yr
               (M&A pipeline $3.5T converts 50%+); loan growth accelerates as
               Fed cuts stimulate refinancing wave; credit stays clean; ROTCE
               sustained above 22%. FY2027E $26 × 15× = $390. +{(PRICE_BULL/CURRENT_PRICE-1)*100:.0f}%.
               Requires: continued M&A momentum + no NII cliff.

  XBULL (${PRICE_XBULL}) : Generational deployment. Dimon or successor announces transformative
               capital deployment (major acquisition: global bank, fintech platform,
               $50-100B deal); Fed cuts to 2.5-3.0% restore NII; AI/fintech
               moat widens; ROTCE sustains 25%+. FY2028E $30+ × 16× = $480.
               +{(PRICE_XBULL/CURRENT_PRICE-1)*100:.0f}%. Requires: 2+ years of perfect execution.
""")

    print("=" * 72)
    print(f"  END OF REPORT -- {TICKER}  |  Generated 2026-05-26")
    print("=" * 72)
