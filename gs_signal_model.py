"""
The Goldman Sachs Group, Inc.  (GS)
BottomUp Risk/Reward Analyzer — Signal Model
"""
import math

# ── Core inputs ──────────────────────────────────────────────────────────────
TICKER        = "GS"
COMPANY       = "The Goldman Sachs Group, Inc."
SECTOR        = "Investment Banking · Global Markets (Trading) · Asset & Wealth Management"

CURRENT_PRICE = 1000.00   # GS — fetched Yahoo Finance / web search, 2026-05-26
                            # Intraday range $991.01–$1,005.18; 52-wk ATH $1,005.36 (set TODAY)
                            # Stock surged 4.9% on SpaceX IPO lead mandate announcement
PRICE_52W_LOW  = 582.50   # April 2025 tariff panic low (+71.7% off that low to current)
PRICE_52W_HIGH = 1005.36  # May 26, 2026 — essentially ALL-TIME HIGH
SHARES_M       = 313.0    # Estimated ~$313B market cap; GS aggressive buybacks ongoing
DIVIDEND_ANN   = 16.00    # $4.00/quarter (yield 1.6% at $1,000)

# ── EPS history (GAAP diluted) ────────────────────────────────────────────────
# GS reports GAAP; no separate "adjusted" metric unlike commercial banks
EPS_HISTORY = {
    "FY2022": 30.06,   # IB revenues halved (equity/debt UW collapse); Marcus losses begin
    "FY2023": 22.87,   # TROUGH: GreenSky write-down ($2.24B → sold <$500M); Marcus exit;
                        # Apple Card credit losses; consumer strategy failure; ROE ~7%
    "FY2024": 40.54,   # +77.3%: Consumer fully exited; IB recovery; trading resilient; ROE ~12%
    "FY2025": 51.32,   # +26.6%: IB super-cycle begins; ROTCE ~15%; "return to roots" working
}
EPS_NOW = 55.00   # FY2026E consensus (~$55; forward P/E 18.2× implied by market);
                   # Q1 2026 actual $17.55 (ROTE 21.3%); H2 conservatively modelled lower

# ── EPP (Earnings Power Price) — structural floor ────────────────────────────
EPS_TROUGH  = 25.00   # Stress recession scenario: IB revenues -50%, trading -30%, credit
                       # provisions elevated. $25 is ABOVE FY2023 actual $22.87 (which had
                       # specific GreenSky/Marcus write-downs on top of weak markets — not
                       # a recurring risk). A pure macro recession (no self-inflicted write-downs):
                       # IB advisory -40% (~$4.5B→$2.7B), UW halved, trading -30% → net ~$7B
                       # earnings → ~$23-27 EPS. $25 = midpoint of this range.
                       # Calibration: 52-wk low $582.50 ÷ $25 = 23.3× stress EPS (credible).
                       # GS March 2020 COVID low: ~$153 (momentary panic), not representative.
EPP_MIN_PE  = 11      # IB/trading firm premium vs commercial bank floor (9×): even in FY2023
                       # trough ($22.87 EPS), GS stock traded $350-400 = 15-17× — market prices
                       # franchise optionality / recovery even at trough. 11× reflects this premium
                       # but is conservative (below the actual FY2023 trough multiple).
EPP         = EPS_TROUGH * EPP_MIN_PE   # = $275.00

# ── Method B (2-year normalised upside ceiling) ───────────────────────────────
CONS_EPS_2YR  = 62.00   # FY2027E analyst consensus ~$62.9; assumes sustained IB recovery +
                          # SpaceX IPO + AM fee growth + buybacks reducing share count
CONS_EXIT_PE  = 18       # Current forward P/E on FY2026E; consistent with ~17% sustainable
                          # ROTE (between FY2025 ROE 15% and Q1 2026 ROTE 21.3%);
                          # already generous — GS historically 12-17× through the cycle
price_b = CONS_EPS_2YR * CONS_EXIT_PE   # = $1,116.00

# ── Primary signal ────────────────────────────────────────────────────────────
ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
# = (1000 − 275) / (1116 − 1000) = 725 / 116 = 6.25×  → ✕ AVOID
# Note: Even using CONS_EXIT_PE = 22× → price_b $1,364; ratio_b = 725/364 = 1.99× (HOLD/TRIM)
# The generous Method B ceiling offers only +11.6% upside vs -72.5% downside to EPP.

# ── Bank-specific metrics (Q1 2026 / FY2025) ─────────────────────────────────
TBV_PER_SHARE  = 340.00   # Estimated Q1 2026; GS TBV ≈ book (minimal goodwill/intangibles);
                            # Q4 2025 book ~$335; grew ~$5 in Q1 via retained earnings
BOOK_PER_SHARE = 344.00   # Slightly above TBV (small intangibles)
ROTCE          = 21.3     # Q1 2026 ROTE (annualised); FY2025 ROE was 15.0%; Q1 was exceptional
ROTCE_FY2025   = 15.0     # FY2025 full-year ROE — the more realistic sustainable baseline
CET1_RATIO     = 12.5     # Start of Q2 2026; 110bps above required minimum; well-capitalised

# ── Scenario anchors ─────────────────────────────────────────────────────────
scenarios = {
    "BEAR":  275.0,    # EPP floor. IB collapse + market recession. EPS $25 × 11×.
    "BASE":  900.0,    # IB normalises (advisory -20% from Q1 peak); ROTE holds 16-17%;
                        # FY2027E $62 × 14.5× = $899. Analyst avg PT = $901-918 IS this scenario.
    "BULL":  1116.0,   # = price_b. IB super-cycle extends; SpaceX IPO; ROTE 18%+.
    "XBULL": 1500.0,   # Full decade-long IB + AM re-rating. ROTE 22%+; SpaceX lock-in;
                        # AI capital markets dominance; FY2028E EPS $78+ × 19×.
}

# ── SCA (Stock-specific Composite Adjustment) ─────────────────────────────────
sca_factors = [
    # (description,                                                       score,  weight)
    ("SpaceX IPO lead mandate: potentially largest IPO in history "
     "(>$400B val); prestige + multi-$B fees; 4.9% surge already baked",   +0.30,  0.20),
    ("IB super-cycle: advisory +89% YoY Q1 2026; UW +45%; record "
     "Global Banking & Markets $12.7B — pipeline continues building",      +0.25,  0.20),
    ("ROTCE trajectory: 15% (FY2025) → 21.3% (Q1 2026); Marcus exit "
     "complete; 'return to roots' compounding; AWM AUM growing",           +0.20,  0.15),
    ("Valuation at ATH: ratio_b 6.25×; analyst avg PT $901 BELOW "
     "current $1,000; 52-wk return +71.7%; no margin of safety at $1,000", -0.40,  0.25),
    ("IB cyclicality: FY2023 EPS $22.87 (-47% from FY2022) shows "
     "depth of IB cycle; Q1 2026 revenue is second-highest ever — peak",   -0.35,  0.25),
    ("Tariff/geopolitical: trade war + macro uncertainty can pause "
     "deal-making; FY2022 IB collapse was tariff/rate-driven event",       -0.15,  0.15),
]

sca_raw = sum(score * weight for _, score, weight in sca_factors)
sca_adj = sca_raw / 2.0

# ── Softmax composite engine ─────────────────────────────────────────────────
def infer_composite(current_price: float, scens: dict[str, float],
                    lo: float = 1.0, hi: float = 4.0, iters: int = 60) -> float:
    bear, base, bull, xbull = scens["BEAR"], scens["BASE"], scens["BULL"], scens["XBULL"]
    centres = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
    T = 0.60
    prices = {"BEAR": bear, "BASE": base, "BULL": bull, "XBULL": xbull}
    for _ in range(iters):
        mid = (lo + hi) / 2
        logits  = {k: -(mid - centres[k])**2 / T for k in centres}
        max_l   = max(logits.values())
        exp_l   = {k: math.exp(logits[k] - max_l) for k in logits}
        denom   = sum(exp_l.values())
        weights = {k: exp_l[k] / denom for k in exp_l}
        ev = sum(weights[k] * prices[k] for k in weights)
        if ev < current_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

market_composite = infer_composite(CURRENT_PRICE, scenarios)
adj_composite    = market_composite + sca_adj

def softmax_weights(composite: float) -> dict[str, float]:
    centres = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
    T = 0.60
    logits  = {k: -(composite - centres[k])**2 / T for k in centres}
    max_l   = max(logits.values())
    exp_l   = {k: math.exp(logits[k] - max_l) for k in logits}
    denom   = sum(exp_l.values())
    return {k: exp_l[k] / denom for k in exp_l}

adj_weights = softmax_weights(adj_composite)
adj_ev      = sum(adj_weights[k] * scenarios[k] for k in adj_weights)

# ── Derived display values ────────────────────────────────────────────────────
epp_gap_pct  = (CURRENT_PRICE / EPP - 1) * 100
upside_b_pct = (price_b / CURRENT_PRICE - 1) * 100
dn_epp_pct   = (EPP / CURRENT_PRICE - 1) * 100
ptbv_current = CURRENT_PRICE / TBV_PER_SHARE
ke, g = 0.09, 0.04
warranted_ptbv_q1   = (ROTCE/100 - g) / (ke - g)
warranted_price_q1  = warranted_ptbv_q1 * TBV_PER_SHARE
warranted_ptbv_fy25 = (ROTCE_FY2025/100 - g) / (ke - g)
warranted_price_fy25 = warranted_ptbv_fy25 * TBV_PER_SHARE
rotce_stress         = 10.0
warranted_ptbv_stress = (rotce_stress/100 - g) / (ke - g)
warranted_price_stress = warranted_ptbv_stress * TBV_PER_SHARE
mkt_cap_b = CURRENT_PRICE * SHARES_M / 1000

# ── Signal label ──────────────────────────────────────────────────────────────
def signal_label(r: float) -> str:
    if r < 0:      return "◉ BUY"
    if r < 0.75:   return "◉ BUY"
    if r < 1.10:   return "◎ ACCUMULATE"
    if r < 1.75:   return "◐ WATCHLIST"
    if r < 2.50:   return "▷ HOLD/TRIM"
    return "✕ AVOID"

signal = signal_label(ratio_b)


# ════════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    sep  = "=" * 72
    line = "─" * 72
    thin = "━" * 72

    print(sep)
    print(f"  {TICKER}  —  {COMPANY}")
    print(f"  {SECTOR}")
    print(sep)

    print()
    print("PART 1 — FRAMEWORK OVERVIEW")
    print(thin)
    print(f"""Special context: GS is the world's premier investment bank and is valued
using the IB-adapted lens: P/E vs through-cycle earning power + P/TBV vs ROTE.
Unlike commercial banks (JPM/BAC/WFC), GS earnings are HIGHLY cyclical — IB
revenues can fall 40-50% in a single year (FY2023: EPS -47% from FY2022).

  GS P/TBV (current)   : {ptbv_current:.2f}×   (at ATH $1,000; 52-wk low was $582.50)
  GS ROTE (Q1 2026)    : {ROTCE:.1f}%  (exceptional quarter; FY2025 full-year ROE: {ROTCE_FY2025:.1f}%)
  GS ratio_b           : {ratio_b:.2f}×    → AVOID; even generous Method B = +{upside_b_pct:.0f}%
  GS CET1 ratio        : {CET1_RATIO:.1f}%   (110bps above required minimum; Q1 2026)
  KEY EVENT             : SpaceX IPO lead mandate — stock hit $1,000 ATH on this news

Gordon Growth (P/TBV vs ROTE) dual-lens:
  Q1 2026 ROTE {ROTCE:.1f}% (peak):  warranted P/TBV {warranted_ptbv_q1:.2f}× → ${warranted_price_q1:.0f}  ← ABOVE current
  FY2025 ROE  {ROTCE_FY2025:.1f}% (annual): warranted P/TBV {warranted_ptbv_fy25:.2f}× → ${warranted_price_fy25:.0f}  ← BELOW current
  Recession ROTE {rotce_stress:.0f}%:         warranted P/TBV {warranted_ptbv_stress:.2f}× → ${warranted_price_stress:.0f}  ← catastrophic
  VERDICT: GS looks cheap only if Q1 2026 ROTE {ROTCE:.1f}% is SUSTAINABLE (it is not —
  Q1 was the firm's second-highest revenue quarter ever; H2 will be much lower).
  At sustainable ROTE {ROTCE_FY2025:.1f}% (FY2025 actual), warranted = ${warranted_price_fy25:.0f} — 12% BELOW current.

Key metrics (Q1 2026, Jan–Mar 2026):
  Net revenues        : $17.23B  (+14% YoY; +28% QoQ; 2nd-highest quarterly ever)
  Net earnings        : $5.63B   (+26% YoY)
  EPS (diluted)       : $17.55   (vs $14.12 Q1 2025; +24% YoY)
  ROE (annualised)    : 19.8%
  ROTE (annualised)   : {ROTCE:.1f}%
  Advisory revenue    : $1.5B    (+89% YoY; strongest in years)
  Equity UW           : $535M    (+45% YoY)
  GB&M total          : $12.7B   (RECORD segment revenue)
  TBV per share       : ~${TBV_PER_SHARE:.0f}    (P/TBV: {ptbv_current:.2f}×)
  CET1                : {CET1_RATIO:.1f}%    (110bps cushion above regulatory minimum)

EPP (Earnings Power Price) — structural floor
  = EPS_TROUGH × EPP_MIN_PE
  Stress EPS (${EPS_TROUGH:.2f}) × {EPP_MIN_PE}× floor.
  ${EPS_TROUGH:.2f}: IB advisory revenues -50% (from $5.9B FY2025 pace → $3B),
  equity/debt UW -45%, trading -30%. No repeat of specific GreenSky/Marcus
  write-downs (those were one-time, strategy-exit charges, not business risk).
  Pre-shock: ~$7B net earnings / ~280M shares (post-buyback) ≈ $25 EPS.
  Calibration: FY2023 actual EPS $22.87 = self-inflicted write-downs + weak IB.
  A pure macro recession (no write-downs) would produce ~$25 EPS at GS scale.
  Calibration 2: 52-wk low $582.50 ÷ $25 = 23.3× stress EPS (market never
  fully priced the catastrophe; even at the 52-wk low GS was 23× stress EPS).
  IB franchise resilience is real — GS never went to zero in any downturn.
  EPP_MIN_PE {EPP_MIN_PE}× reflects this premium vs commercial bank floor (9×).
  EPP = ${EPP:.2f}.

Method B — 2-year normalised upside ceiling
  = CONS_EPS_2YR × CONS_EXIT_PE
  FY2027E ~${CONS_EPS_2YR:.2f} (analyst consensus ~$62.9; IB recovery sustained + SpaceX +
  AM fee growth + ~$2B+ in buybacks annually reducing share count)
  × {CONS_EXIT_PE}× exit P/E (current {CURRENT_PRICE/EPS_NOW:.1f}×; {CONS_EXIT_PE}× is already generous vs GS cycle-average
  13-17×; justified only if ROTE sustains 17%+ long-term)
  = ${price_b:.2f}.
  Ratio B = (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f}) = ${CURRENT_PRICE-EPP:.2f} / ${price_b-CURRENT_PRICE:.2f} = {ratio_b:.2f}×
  → {signal}. Method B upside: +{upside_b_pct:.1f}% to ${price_b:.2f}.
  Downside to EPP: {dn_epp_pct:.1f}%.
  NOTE: Analyst avg PT $901-918 is BELOW current price — consensus models the
  BASE scenario, not the BULL, as fair value. The market is pricing BULL today.
  Even the GENEROUS Method B target of $1,116 implies only +11.6% upside.
  The risk/reward is one of the worst in our entire coverage universe.
{thin}
""")

    print()
    print("PART 2 — ANALYST COMMENTARY & CONTEXT")
    print(thin)
    print(f"""
GOLDMAN SACHS: THE GREATEST COMEBACK IN WALL STREET — BUT AT WHAT PRICE?
=========================================================================

Goldman Sachs is THE premier global investment bank — the firm that Buffett
called "a great business" and that has produced more Treasury Secretaries,
Fed chairs, and CEOs than any other firm. Its Global Banking & Markets
franchise (equities, FICC, M&A advisory, underwriting) is genuinely world-class.

The problem is not the business. The problem is the price.

AT $1,000/SHARE AND AN ALL-TIME HIGH:
  - 17.7× FY2026E EPS on ELEVATED cyclical earnings
  - Analyst avg PT $901 (10% BELOW current — consensus says SELL)
  - Method B upside of just +11.6% vs EPP downside of -72.5%
  - The SpaceX IPO narrative is fully priced in on the day it was announced
  - FY2023 showed EPS can fall -47% in a single year when IB dries up

ACT I: THE MARCUS DISASTER (2019-2023)
=======================================
Under CEO David Solomon (from 2018), Goldman attempted to build a consumer bank:
  - Marcus personal loans: millions of consumer accounts; defaults soared
  - GreenSky: acquired for $2.24B (2022); sold to investors for <$500M (2023)
    → ~$1.7B+ write-down on a single transaction
  - Apple Card: $0 origination fee credit card; Apple's credit losses became GS's
  - GM Card: launched 2023; exit announced 2024
  - Total consumer segment losses (2020-2023): estimated $3-4B+ pre-tax

The human cost:
  - Thousands of layoffs (Jan 2023: 3,200+ jobs, largest since 2008)
  - Partner compensation slashed; morale collapsed
  - CEO Solomon survived only because the board had no viable successor
  - FY2023 EPS: $22.87 — near a DECADE low for a firm with this franchise

Why this matters for today's analysis:
  The Marcus disaster is OVER. GS exited all consumer activities by FY2024.
  But it reveals a structural truth: GS earnings are VIOLENTLY cyclical. When
  things go wrong — whether macro (FY2022) or strategic (FY2023) — EPS can
  fall 47% in one year. The $25 stress EPS in our EPP model may be optimistic.

ACT II: THE RETURN TO ROOTS (2024-2026)
=========================================
Solomon's strategic pivot back to GS's core strengths is working emphatically:

  FY2024: Consumer exit complete. IB recovering. Advisory +23%. EPS $40.54.
  FY2025: IB super-cycle emerging. ROTCE reaches 15%. EPS $51.32.
  Q1 2026: Second-highest quarterly revenue ever ($17.23B). ROTE 21.3%.
    Advisory revenues: $1.5B (+89% YoY) — M&A pipeline at post-COVID highs
    Equity underwriting: $535M (+45% YoY) — IPO market reopened
    FICC trading: strong (market volatility from tariff/macro uncertainty)
    Global Banking & Markets: $12.7B RECORD segment revenue

The "return to roots" story is compelling. But here is the critical question:

  IS Q1 2026 THE BEGINNING OF A SUSTAINED SUPER-CYCLE, OR IS IT THE PEAK?

Q1 is seasonally GS's strongest quarter (bonus comp, deal closings, capital
markets activity). ROTE 21.3% in Q1 is NOT the full-year run-rate:
  Q1 2025 ROTE: ~16.9% (ROE). Full year 2025 ROE: 15.0%.
  Historically Q1 is 25-30% of full-year earnings at GS.
  If Q1 2026 ($17.55) = 27% of FY2026, then FY2026 = $65.
  Analysts are projecting $55-57 for FY2026 (more conservative H2 assumed).

The honest assessment: Q1 2026 was an exceptional quarter (tariff volatility
drove record equities trading; IB advisory surged as deals rushed to close
before trade war impact). Q2-Q4 2026 will likely be notably weaker.

THE SPACEX IPO — NARRATIVE CATALYST, ALREADY PRICED
=====================================================
Goldman Sachs winning the lead-manager role for SpaceX's IPO is genuinely
significant for the firm's prestige and fee income. Context:

  SpaceX valuation: ~$400B+ (would be among largest IPOs in history)
  Typical lead manager fee: 2-4% of deal size → $8-16B deal raises $160-640M fee
  More likely: SpaceX IPO raises $10-20B → GS gets $200-400M in fees (1-2%)

$200-400M in fees = roughly $0.65-1.30 per share after tax — meaningful but not
transformative on a $55 EPS base. The stock surged 4.9% ($47/share = $14.7B
market cap increase) on the SpaceX announcement. The market added ~35-75×
the actual fee value to GS's market cap in ONE DAY.

This is the classic "great news, already priced" scenario.

The SpaceX IPO prestige effect (future deal flow, talent retention, attracting
sovereign wealth fund clients) is real. But it is incremental, not transformational.
At $1,000 GS, you are paying 75× the SpaceX fee just in the day's price increase.

GS vs PEERS — THE INVESTMENT BANK PREMIUM
==========================================
GS is uniquely positioned as a pure-play IB + trading + AWM firm, unlike JPM/BAC
which have large commercial banking buffers:

                GS          JPM         BAC         WFC
  ROTE (Q1)    {ROTCE:.1f}%      23.0%       16.0%       14.5%
  P/TBV        {ptbv_current:.2f}×       2.83×       1.78×       1.77×
  CET1         {CET1_RATIO:.1f}%        14.3%       12.0%       10.3%
  P/E fwd      {CURRENT_PRICE/EPS_NOW:.1f}×       13.7×       12.9×       11.6×
  EPS cyclicality  EXTREME   Moderate    Moderate    Moderate

GS trades at a substantial premium on P/E (17.7× vs JPM 13.7×) primarily because:
  1. ROTE is higher in IB super-cycles (21.3% now; vs JPM 23% — nearly equal)
  2. The GS franchise carries a genuine "Goldman premium" (deal advisory moat)
  3. AWM is a growing, recurring-revenue business ($3T+ AUM)

But GS's ROTE is far MORE VOLATILE than JPM's:
  GS ROTE range: 7% (FY2023 trough) → 21.3% (Q1 2026 peak)
  JPM ROTE range: 15% (trough) → 23% (Q1 2026 peak)
  → GS swings 14 percentage points vs JPM's 8pp

At 17.7× P/E on PEAK earnings + near-zero dividend yield relative to book:
  GS at $1,000 = you are betting the IB super-cycle lasts AND EXPANDS.
  If it moderates (BASE scenario), GS returns to $850-900 = -10-15% from today.

GORDON GROWTH — THE FULL PICTURE
==================================
  Current P/TBV: {ptbv_current:.2f}×  at  TBV ${TBV_PER_SHARE:.0f}/share

  At Q1 2026 ROTE {ROTCE:.1f}% (one exceptional quarter — NOT sustained):
    Warranted P/TBV = {warranted_ptbv_q1:.2f}× → ${warranted_price_q1:.0f}  (ABOVE current — looks cheap)
  At FY2025 ROE {ROTCE_FY2025:.1f}% (full year — more realistic):
    Warranted P/TBV = {warranted_ptbv_fy25:.2f}× → ${warranted_price_fy25:.0f}  (BELOW current — expensive)
  At recession ROTE {rotce_stress:.0f}%:
    Warranted P/TBV = {warranted_ptbv_stress:.2f}× → ${warranted_price_stress:.0f}  (catastrophic)

The market is using Q1 ROTE 21.3% as the valuation anchor. That is wrong.
The right anchor is through-cycle ROTE of 15-17% (between FY2025 and a moderate
improvement). At 17% through-cycle ROTE: warranted P/TBV 2.60× = $884.

ENTRY/EXIT FRAMEWORK
====================
  ◉ BUY        : $350-450  (1.3-1.6× EPP; IB collapse + multiple compression; FY2022-style entry)
  ◎ ACCUMULATE : $500-650  (1.8-2.4× EPP; 52-wk low territory; normalised multiple)
  ◐ WATCHLIST  : $650-800  (2.4-2.9× EPP; recovery priced, not super-cycle)
  ▷ HOLD/TRIM  : $800-950  (near analyst consensus; IB cycle priced; take profits)
  ✕ AVOID      : >$950     (current $1,000; ATH; SpaceX priced; IB peak; AVOID)

The 52-wk low of $582.50 (April 2025) was the ACCUMULATE entry at ratio_b ~0.93×.
GS has returned +71.7% from that low in 13 months. At $1,000 — the ALL-TIME HIGH —
the easy money is made. The trade is over. AVOID; revisit below $800.
""")
    print(thin)

    print()
    print("PART 3 — NUMBERS & SIGNALS")
    print(thin)

    print(f"""
  I. PRICE & VALUATION SNAPSHOT
  {line}
  Current price   : ${CURRENT_PRICE:.2f}  (52-wk range: ${PRICE_52W_LOW:.2f}–${PRICE_52W_HIGH:.2f})
  vs 52-wk low    : +{(CURRENT_PRICE/PRICE_52W_LOW-1)*100:.1f}%   |   vs 52-wk high: {(CURRENT_PRICE/PRICE_52W_HIGH-1)*100:.1f}%  ← ESSENTIALLY AT ATH
  Market cap      : ~${mkt_cap_b:.0f}B   |   Shares: ~{SHARES_M/1000:.2f}B
  Dividend (ann)  : ${DIVIDEND_ANN:.2f}   |   Yield: {DIVIDEND_ANN/CURRENT_PRICE*100:.2f}%  (paltry at $1,000)
  TBV per share   : ${TBV_PER_SHARE:.0f}   |   P/TBV: {ptbv_current:.2f}×
  ROTE (Q1 2026)  : {ROTCE:.1f}%    |   CET1 ratio: {CET1_RATIO:.1f}%
  Forward P/E     : {CURRENT_PRICE/EPS_NOW:.1f}×  (on FY2026E ${EPS_NOW:.2f}; ELEVATED cyclical earnings)
  Analyst avg PT  : $901-918  — BELOW current price (consensus = BASE, not BULL)
  SpaceX IPO      : Lead mandate announced; stock surged 4.9% (+$47/share) on this news

  Gordon Growth:
    Q1 ROTE {ROTCE:.1f}% → warranted {warranted_ptbv_q1:.2f}× P/TBV = ${warranted_price_q1:.0f}  (one quarter; not sustained)
    FY2025 ROE {ROTCE_FY2025:.1f}% → warranted {warranted_ptbv_fy25:.2f}× P/TBV = ${warranted_price_fy25:.0f}  (realistic; BELOW current)
    Recession ROTE {rotce_stress:.0f}% → warranted {warranted_ptbv_stress:.2f}× P/TBV = ${warranted_price_stress:.0f}  (catastrophic)

  II. EPS HISTORY (GAAP diluted)
  {line}
  FY2022  : ${EPS_HISTORY['FY2022']:.2f}  (IB revenues halved; equity UW collapse; Marcus losses begin)
  FY2023  : ${EPS_HISTORY['FY2023']:.2f}  (TROUGH: GreenSky $1.7B+ write-down; Marcus exit; ROE 7%)
  FY2024  : ${EPS_HISTORY['FY2024']:.2f}  (+{(EPS_HISTORY['FY2024']/EPS_HISTORY['FY2023']-1)*100:.0f}%; consumer fully exited; IB recovering; ROE ~12%)
  FY2025  : ${EPS_HISTORY['FY2025']:.2f}  (+{(EPS_HISTORY['FY2025']/EPS_HISTORY['FY2024']-1)*100:.0f}%; IB super-cycle; ROTCE ~15%; "return to roots" vindicated)
  FY2026E : ${EPS_NOW:.2f}   (Q1 actual $17.55; H2 conservatively lower; fwd P/E {CURRENT_PRICE/EPS_NOW:.1f}×)
  FY2027E : ${CONS_EPS_2YR:.2f}   (used for Method B; consensus ~$62.9; assumes sustained recovery)
  Q1 2026 : $17.55  (+24% YoY; 2nd-highest quarterly EPS ever; ROTE 21.3%)

  Note: FY2023 EPS ($22.87) ÷ FY2022 EPS ($30.06) = -47% in one year. This is
  the EPS CYCLICALITY that justifies EPP_MIN_PE premium + large EPP/price gap.

  III. EPP & METHOD B
  {line}
  EPS_TROUGH  : ${EPS_TROUGH:.2f}/share  (IB -50% + trading -30%; above FY2023 $22.87 adj for write-downs)
  EPP_MIN_PE  : {EPP_MIN_PE}×           (IB franchise premium; even in FY2023 GS traded 15-17× trough EPS)
  EPP (floor) : ${EPP:.2f}        (= ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×)
  EPP gap     : +{epp_gap_pct:.1f}%    (current price is {CURRENT_PRICE/EPP:.1f}× above EPP floor — extreme)

  CONS_EPS_2YR: ${CONS_EPS_2YR:.2f}/share  (FY2027E; ~$62.9 analyst consensus)
  CONS_EXIT_PE: {CONS_EXIT_PE}×           (current P/E; generous — GS cycle-average is 13-17×)
  Method B    : ${price_b:.2f}       (= ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×; only +{upside_b_pct:.1f}% from current)
  Upside to B : +{upside_b_pct:.1f}%   ← MINIMAL upside even to the generous Method B
  Downside EPP: {dn_epp_pct:.1f}%  ← SEVERE downside

  ┌─────────────────────────────────────────────────────────────────────┐
  │  RATIO B = ({CURRENT_PRICE:.2f} − {EPP:.2f}) / ({price_b:.2f} − {CURRENT_PRICE:.2f})              │
  │           = {CURRENT_PRICE-EPP:.2f} / {price_b-CURRENT_PRICE:.2f} = {ratio_b:.2f}×                              │
  │  SIGNAL   = {signal}                                          │
  └─────────────────────────────────────────────────────────────────────┘

  IV. STOCK-SPECIFIC COMPOSITE ADJUSTMENT (SCA)
  {line}
  Factor                                                 Score      Wt  Contrib
  ────────────────────────────────────────────────────  ──────  ──────  ───────""")

    for desc, score, wt in sca_factors:
        short = desc[:51].ljust(51)
        print(f"  {short}  {score:+.2f}    {wt:.2f}   {score*wt:+.3f}")

    print(f"""  ────────────────────────────────────────────────────  ──────  ──────  ───────
  SCA raw                                                                {sca_raw:+.3f}
  SCA adj (÷2.0)                                                         {sca_adj:+.3f}

  V. COMPOSITE INFERENCE
  {line}
  Market composite  : {market_composite:.3f}  ({"BASE" if 1.625<=market_composite<2.375 else "BEAR" if market_composite<1.625 else "BULL" if market_composite < 3.125 else "XBULL"})
  Adj composite     : {adj_composite:.3f}  ({"BASE" if 1.625<=adj_composite<2.375 else "BEAR" if adj_composite<1.625 else "BULL" if adj_composite < 3.125 else "XBULL"})
  Softmax weights at adj composite ({adj_composite:.3f}):""")

    scen_prices = {"BEAR": scenarios["BEAR"], "BASE": scenarios["BASE"],
                   "BULL": scenarios["BULL"], "XBULL": scenarios["XBULL"]}
    for k, w in adj_weights.items():
        print(f"    {k:<6}: {w*100:.1f}%  (${scen_prices[k]:.0f})")

    print(f"""  Expected price (adj): ${adj_ev:.0f}  vs current ${CURRENT_PRICE:.2f}  (Δ {(adj_ev/CURRENT_PRICE-1)*100:+.1f}%)
  Note: Market is pricing in BULL scenario to justify $1,000. BASE scenario
  (analyst consensus fair value) = $900 — 10% BELOW current price.

  VI. SCENARIOS SUMMARY
  {line}
  BEAR  (${scenarios['BEAR']:.0f}) : IB recession. Advisory revenues halved ($5.9B→$3B); equity UW
               -45%; FICC trading -30% (low volatility, low volume). ROTCE falls to 9-10%.
               EPS $25 × 11× = $275. Calibration: FY2023 actual low was $22.87 EPS
               (with write-downs); GS stock then was $350-400 = 15-17× that trough.
               {(scenarios['BEAR']/CURRENT_PRICE-1)*100:.0f}% from current.

  BASE  (${scenarios['BASE']:.0f}) : IB normalises from Q1 peak. Advisory -20% in H2 2026; UW stable;
               trading returns to average. ROTE holds 15-17%; FY2027E $62 × 14.5×.
               THIS IS WHERE ANALYST CONSENSUS SITS ($901-918 avg PT = this scenario).
               {(scenarios['BASE']/CURRENT_PRICE-1)*100:+.0f}% from current — i.e., SELL at current price per analyst consensus.

  BULL  (${scenarios['BULL']:.0f}) : = price_b. IB super-cycle extends through 2026-2027; SpaceX IPO
               closes ($15-20B raise, $200-400M GS fee); M&A pipeline realises; ROTE
               sustains 18%+. FY2027E ${CONS_EPS_2YR:.0f} × {CONS_EXIT_PE}×. This is needed just to reach
               Method B — only +{upside_b_pct:.0f}% from current. Not worth the risk.
               {(scenarios['BULL']/CURRENT_PRICE-1)*100:+.0f}% from current.

  XBULL (${scenarios['XBULL']:.0f}) : GS becomes the dominant AI capital markets bank. SpaceX IPO
               leads a wave of mega-tech IPOs (Stripe, Discord, Databricks, Starlink).
               ROTE sustains 20%+; AWM reaches $4T AUM; P/TBV re-rates to 4×.
               FY2028E EPS $78+ × 19× = $1,482. Solomon vindicated; Solomon-era
               dismissals prove premature. Landmark decade for GS.
               {(scenarios['XBULL']/CURRENT_PRICE-1)*100:+.0f}% from current.

{"=" * 72}
  END OF REPORT -- {TICKER}  |  Generated 2026-05-26
{"=" * 72}""")
