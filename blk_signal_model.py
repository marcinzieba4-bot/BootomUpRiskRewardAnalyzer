"""
BlackRock, Inc.  (BLK)
BottomUp Risk/Reward Analyzer — Signal Model
"""
import math

# ── Core inputs ──────────────────────────────────────────────────────────────
TICKER        = "BLK"
COMPANY       = "BlackRock, Inc."
SECTOR        = "Asset Management · Passive Investing (iShares) · Alternatives (GIP + HPS) · Aladdin Technology"

CURRENT_PRICE  = 1073.15   # BLK — fetched via web search, 2026-05-26
                             # Intraday range $1,071.11–$1,083.96; mkt cap $175.09B
PRICE_52W_LOW  =  917.39   # April 2026 tariff-panic low (-14.5% from current)
PRICE_52W_HIGH = 1219.94   # All-time high (Nov 2025); BLK now 12.0% below ATH
SHARES_M       =  162.84   # Shares outstanding (confirmed); mkt cap $175.09B / $1,073.15
DIVIDEND_ANN   =   22.92   # $5.73/quarter (raised 13 consecutive years; yield 2.13% at current price)

# ── EPS history (adjusted / non-GAAP diluted) ─────────────────────────────────
# NOTE: BlackRock reports both GAAP and adjusted EPS. The adjusted (non-GAAP) metric
# is the primary analyst/management lens. BLK's adj EPS is typically LOWER than GAAP
# because adjustments remove mark-to-market gains on seed investments and certain
# deferred-comp offsets while adding back acquisition amortization — net effect is
# adj < GAAP in periods of strong equity markets.  All EPS below are ADJUSTED.
EPS_HISTORY = {
    "FY2022": 37.70,   # Market down -20%; equity AUM fell ~$2T; base fee growth slowed;
                        # GIP/HPS not yet acquired; pure public-markets asset manager
    "FY2023": 38.20,   # Modest recovery; markets +20% but AUM base slower; rates high
                        # (bond fund outflows offset equity inflows); +1.3% adj EPS growth
    "FY2024": 43.70,   # +14.4% YoY; GIP transaction closed Oct 1 2024 ($170B infra AUM);
                        # 15% increase in diluted EPS (per press release); record organic growth
    "FY2025": 48.09,   # +10.1% YoY; HPS closed July 1 2025 ($190B private credit);
                        # Preqin (alternatives data intelligence) integration begins;
                        # AUM $11.6T → $13.9T (Q1 2026 entry); Q4 adj EPS $13.16
}
EPS_NOW = 54.29   # FY2026E adj EPS consensus (analyst estimate post-Q1 2026 beat);
                   # Q1 2026 adj actual $12.53 (+10.9% vs Q1 2025 $11.30);
                   # Full year guided higher by HPS/GIP fee ramp + organic base fee growth

# ── EPP (Earnings Power Price) — structural floor ────────────────────────────
EPS_TROUGH  = 28.00   # Severe recession: global equity markets -35%, significant AUM redemptions.
                        # History: FY2022 adj EPS $37.70 at market -20%. A full recession with -35%
                        # market drawdown + net outflows would compress AUM from $14T to ~$9T:
                        # base fee revenue ∝ AUM × avg fee rate → ~35-40% revenue decline.
                        # Alternatives (GIP infra fees, HPS private credit) provide partial cushion —
                        # infrastructure and private credit fees are NOT mark-to-market sensitive.
                        # $28 = revenue fall of ~35% minus cost flexibility. Equals FY2022 adj × 0.74×.
                        # Far-tail scenario; normal recession might see adj EPS $35-40.
EPP_MIN_PE  = 17      # BLK franchise floor: capital-light, fee-based, no credit risk, $1T+
                        # recurring base fees. Even at April 2026 tariff-panic low ($917.39),
                        # market assigned $917 / $54.29 FY2026E = 16.9× forward — confirming the
                        # floor is ~17×. Premium vs commercial banks (9×) and IBs (11-12×) reflects
                        # the secular growth of passive AUM and the absence of balance-sheet risk.
EPP         = EPS_TROUGH * EPP_MIN_PE   # = $476.00

# ── Method B (2-year normalised upside ceiling) ───────────────────────────────
CONS_EPS_2YR  = 62.00   # FY2027E adj EPS estimate: FY2026E $54.29 × ~14% organic growth.
                          # Growth drivers: GIP+HPS fee ramp (full two-year contribution), iShares
                          # passive AUM compounding, organic base fee growth 5-7%, performance fees
                          # normalising upward. 14% CAGR is below the 2024-2026 acceleration
                          # rate (46% GAAP EPS Q1 YoY) but reflects a more normalised step-up.
CONS_EXIT_PE  = 22        # Post-transformation BLK multiple: pure passive asset managers trade
                          # 15-20×; alternatives platforms (Blackstone, Apollo) trade 20-30×.
                          # At 22×, BLK is valued as a hybrid: premium to pure passive (iShares)
                          # but discount to pure-alternatives (BX, APO). Historical BLK P/E range:
                          # 20-28× in bull markets (FY2019-FY2022). Conservative bull-case.
price_b = CONS_EPS_2YR * CONS_EXIT_PE   # = $1,364.00

# ── Primary signal: Ratio B ───────────────────────────────────────────────────
ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
# = (1073.15 - 476.00) / (1364.00 - 1073.15) = 597.15 / 290.85 = 2.052×
# Signal: ▷ HOLD/TRIM (1.75–2.50×)

# ── Softmax composite engine ──────────────────────────────────────────────────
T = 0.60
SCENARIOS = {
    "BEAR":  {"price":  476.00, "label": "BEAR"},   # EPP floor; markets -35%; large redemptions
    "BASE":  {"price": 1086.00, "label": "BASE"},   # FY2026E $54.29 × 20× = $1,086; ≈ current
    "BULL":  {"price": 1364.00, "label": "BULL"},   # Method B; FY2027E $62 × 22×
    "XBULL": {"price": 1750.00, "label": "XBULL"},  # Alt-manager re-rating; $62 × 28×
}

SIGNAL_CENTRES = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}

def softmax_weights(composite):
    logits = {s: -(composite - c)**2 / T for s, c in SIGNAL_CENTRES.items()}
    max_l  = max(logits.values())
    raw    = {s: math.exp(v - max_l) for s, v in logits.items()}
    total  = sum(raw.values())
    return {s: v / total for s, v in raw.items()}

def expected_price(composite):
    w = softmax_weights(composite)
    return sum(w[s] * SCENARIOS[s]["price"] for s in SCENARIOS)

def infer_composite(target_price, lo=1.0, hi=4.0, iterations=60):
    for _ in range(iterations):
        mid = (lo + hi) / 2
        if expected_price(mid) < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

market_composite = infer_composite(CURRENT_PRICE)

# ── SCA (Signal Catalyst Adjustments) ────────────────────────────────────────
SCA_FACTORS = [
    # Tailwinds
    {"label": "GIP + HPS alternatives transformation",
     "rating": +0.30, "weight": 0.20,
     "note": "BlackRock completed two landmark acquisitions in 18 months: GIP (Global Infrastructure"
             " Partners; $170B AUM; closed Oct 2024) + HPS Investment Partners ($190B private credit;"
             " closed July 2025). Combined: $360B+ alternatives AUM added. Alternatives generate"
             " 2-3× higher fee rates than passive (GIP infrastructure funds charge 1.5-2%+ vs iShares"
             " ETFs at 0.05-0.20%). BLK is now a top-5 alternatives platform, competing with"
             " Blackstone and Apollo for institutional mandates. Full fee ramp flows into 2026-2027."},
    {"label": "Aladdin platform / technology revenue",
     "rating": +0.25, "weight": 0.15,
     "note": "Aladdin (risk management OS) serves 55,000+ investment professionals; $130T+ in assets"
             " managed on the platform by clients. Technology service revenue growing double-digits."
             " Preqin (alternatives data) acquisition adds private market data to Aladdin's public-"
             " market dominance. The Aladdin platform creates switching costs and provides a"
             " revenue stream entirely uncorrelated with AUM market fluctuations."},
    {"label": "$13.9T AUM compounding + 13% organic growth",
     "rating": +0.20, "weight": 0.15,
     "note": "Q1 2026: long-term net inflows $135.9B; organic growth rate 13% (vs 3% in Q1 2024)."
             " $13.9T AUM at 0.25% blended avg fee = $34.75B annual base fees (run-rate)."
             " Each 1% market appreciation = ~$139B AUM → ~$347M incremental annual base fees."
             " iShares ETF platform is #1 globally; passive AUM structurally grows as active underperforms."},
    # Headwinds
    {"label": "Simultaneous integration of three acquisitions",
     "rating": -0.25, "weight": 0.25,
     "note": "GIP, HPS, and Preqin are all integrating simultaneously. Each is large and culturally"
             " distinct: GIP (infrastructure PE culture), HPS (private credit culture), Preqin (data"
             " company culture) vs BLK's public-markets ethos. Revenue dis-synergies (clients who"
             " cross-reference competing managers), talent retention, technology integration are all"
             " real risks. M&A integration failures at this scale are common. GIP and HPS combined"
             " cost BLK $30B+ in stock/cash — a significant capital allocation bet."},
    {"label": "AUM market sensitivity / passive fee compression",
     "rating": -0.20, "weight": 0.25,
     "note": "Base fee revenue directly tracks AUM × fee rate. A 25% market decline = $3.5T AUM"
             " reduction → ~$875M annual base fee revenue headwind. iShares fee rates are in secular"
             " decline (Vanguard/Fidelity fee war): blended avg fell from 0.27% (2015) to 0.17%"
             " (2024). Each 1bps fee rate compression on $14T = $1.4B annual revenue reduction."
             " These structural headwinds partially offset AUM scale growth."},
    {"label": "12% below ATH / multiple still recovering",
     "rating": -0.15, "weight": 0.20,
     "note": "52-wk high $1,219.94 (Nov 2025); current $1,073.15 = -12.0%. The stock went from"
             " $917 (ACCUMULATE) to $1,220 (AVOID) and back to $1,073 (HOLD). Multiple contracted"
             " from 22.5× at ATH to 19.8× FW at current — still on recovery trajectory."
             " Rate environment (higher-for-longer) compresses equity AUM multiples."
             " Passive ETF competition from Vanguard/Fidelity intensifying."},
]

sca_raw = sum(f["rating"] * f["weight"] for f in SCA_FACTORS)
sca_adj = sca_raw / 2.0

adj_composite = market_composite + sca_adj

# ── Asset manager specific metrics ────────────────────────────────────────────
AUM_TOTAL_T      = 13.9    # Total AUM Q1 2026 ($T; up from $11.6T a year ago = +20%)
NNA_Q1_2026      = 135.9   # Long-term net new assets Q1 2026 ($B)
ORGANIC_GROWTH   = 13.0    # Organic AUM growth rate (last-12-months basis; Q1 2026)
ADJ_OP_MARGIN    = 44.5    # Q1 2026 adjusted operating margin (%)
GIP_AUM_B        = 170.0   # GIP AUM added ($B); closed Oct 2024
HPS_AUM_B        = 190.0   # HPS private credit AUM added ($B); closed July 2025

# ── Output ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    w = softmax_weights(adj_composite)
    exp_p = expected_price(adj_composite)

    # ── PART 1: Framework ─────────────────────────────────────────────────────
    part1 = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  BottomUp Risk/Reward Analyzer — Analytical Framework                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
This tool applies a structured bottom-up framework to estimate the risk/reward
profile of individual equities over a 2-year investment horizon.  It is NOT a
trading signal or a price prediction — it is a disciplined lens for sizing
positions relative to the gap between structural downside (EPP) and consensus
upside (Method B).

KEY METRICS DEFINED
  EPP  (Earnings Power Price)   = EPS_trough × min-viable trough P/E
       The structural floor: the price the market should not sustainably
       breach even in a severe downturn, because earnings power remains.

  Method B price                = Consensus 2-yr EPS × exit P/E assumption
       The ceiling under the base/bull scenario — what the stock is worth
       if consensus plays out and the market re-rates to a reasonable multiple.

  Ratio B (PRIMARY SIGNAL)      = (Current − EPP) / (Method B − Current)
       How much downside risk are you taking per unit of upside potential?
       < 0.75 = BUY · 0.75–1.10 = ACCUMULATE · 1.10–1.75 = WATCHLIST
       1.75–2.50 = HOLD/TRIM · > 2.50 = AVOID

  Composite score               = market-implied scenario blend (1.0–4.0 scale)
       Inferred by back-solving the softmax price engine against today's price.
       1.0 = deep BEAR | 2.0 = BASE | 3.0 = BULL | 4.0 = XBULL
       SCA adjustments shift the composite to reflect non-price catalysts.

SIGNAL TABLE
  ◉ BUY        Ratio B < 0.75   — asymmetric upside; margin of safety present
  ◎ ACCUMULATE Ratio B 0.75–1.10 — favourable risk/reward; build position
  ◐ WATCHLIST  Ratio B 1.10–1.75 — balanced; monitor for entry improvement
  ▷ HOLD/TRIM  Ratio B 1.75–2.50 — upside limited vs downside; reduce on strength
  ✕ AVOID      Ratio B > 2.50   — risk/reward deeply unfavourable at current price

DATA QUALITY NOTE
  All EPS figures use ADJUSTED (non-GAAP) earnings per BlackRock's reporting
  convention.  BLK's adjusted EPS is typically LOWER than GAAP because the
  adjustment removes mark-to-market gains on seed capital investments and
  certain deferred-compensation offsets.  Street models universally use
  adjusted EPS for BLK comparisons.
"""

    # ── PART 2: Analyst commentary ────────────────────────────────────────────
    part2 = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  BLK  |  BlackRock, Inc.  |  ▷ HOLD/TRIM                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

SNAPSHOT  (as of 2026-05-26)
  Price         ${CURRENT_PRICE:,.2f}   52-wk range  ${PRICE_52W_LOW:.2f} – ${PRICE_52W_HIGH:.2f}
  Shares        {SHARES_M:.2f}M          Mkt cap      ~$175.1B
  Dividend      ${DIVIDEND_ANN:.2f}/yr      Yield        ~{DIVIDEND_ANN/CURRENT_PRICE*100:.2f}%
  FY2026E EPS   ${EPS_NOW:.2f} (adj)   FW P/E       {CURRENT_PRICE/EPS_NOW:.1f}×
  AUM           ~${AUM_TOTAL_T:.1f}T          Organic NNA  ${ORGANIC_GROWTH:.0f}% (Q1 2026)
  EPP floor     ${EPP:.2f}       Ratio B      {ratio_b:.2f}×  →  ▷ HOLD/TRIM

THE BUSINESS: THE WORLD'S LARGEST ASSET MANAGER, NOW GOING ALTERNATIVES
BlackRock manages $13.9 trillion in client assets — more than any entity in human
history.  It is the backbone of global passive investing: iShares is the world's
largest ETF provider by AUM.  But the defining story of 2024-2025 was BLK's
deliberate pivot into private markets through two landmark acquisitions:

PLATFORM TRANSFORMATION (the GIP + HPS + Preqin trilogy):

  GIP — Global Infrastructure Partners  (closed Oct 1, 2024)
  ~$170B AUM in infrastructure: airports (Gatwick, Edinburgh, Sydney), toll roads,
  data centers, energy transition assets.  Infrastructure funds charge 1.5-2%+ fees
  (vs iShares ETFs at 0.05-0.20%) and offer 10-15 year locked capital.  GIP transforms
  BLK from a price-taker in fee competition to a category leader in an asset class
  with structural tailwinds (AI infrastructure, energy transition, deglobalisation).

  HPS Investment Partners  (closed July 1, 2025)
  ~$190B in private credit assets — direct lending, mezzanine, asset-backed.
  Private credit has displaced traditional bank lending in leveraged buyouts and
  corporate finance since 2022.  HPS adds a recurring fee stream at 1-2% rates that
  is largely immune to public equity/bond market volatility.

  Preqin  (alternative investment data)
  Brings private markets data intelligence alongside Aladdin (public markets OS).
  BLK now owns the data AND the investment platform for both public and private assets.

Combined result: BLK has added $360B+ in alternatives AUM at 3-5× higher fee rates.
With ~$1.5T in alternatives, BLK is now a top-5 global alternatives manager alongside
Blackstone, Apollo, KKR, and Carlyle — while ALSO remaining the world's #1 passive manager.

Q1 2026: RECORD FLOWS, RECORD REVENUE
  Revenue: $6.7B (+27% YoY)  ·  Adj EPS: $12.53 (+10.9%)  ·  GAAP EPS: $14.06 (+46%)
  Long-term net inflows: $135.9B  ·  Organic growth: 13% (vs 3% in Q1 2024)
  Adj operating margin: 44.5%  ·  AUM: $13.9T (from $11.6T a year ago = +$2.3T)
  Performance fees: more than tripled to $272M

The organic growth rate of 13% is the key metric: it shows that BLK is not just growing
because markets went up — it's genuinely winning client mandates across all categories.

WHY HOLD/TRIM, NOT BUY OR ACCUMULATE
The business is excellent.  The question is price:

  1. Current $1,073 is essentially the BASE scenario price:
     BASE = FY2026E $54.29 × 20× = $1,086 ≈ current price.
     The market is already pricing the normal/good scenario.
     To generate meaningful upside from here, you need the BULL to materialise.

  2. Method B ($1,364) offers only +27.1% from current — modest for the risk taken.
     Against a BEAR at $476 (-55.7% downside), the risk/reward is 2.05× unfavourable.

  3. 52-wk low $917.39 was the entry:
     At $917 with EPP=$476 and price_b=$1,364:
     ratio_b = (917.39-476)/(1364-917.39) = 441.39/446.61 = 0.99× → ◎ ACCUMULATE
     That was 6-8 weeks ago. The stock recovered +17% from its panic low — the easy
     money from the ACCUMULATE entry zone is already made.

  4. Analyst avg PT $1,251-1,254 → +16-17% above current.
     Unlike GS (+11.6% upside on AT) or MS (-5% downside), BLK's analyst community
     is genuinely bullish with PTs above current price.  This is the best signal in the
     Finance coverage universe — but it still implies only 16-17% upside in 12 months.

  5. Alternatives integration is the key uncertainty:
     GIP, HPS, Preqin integrating simultaneously is operationally complex.  If ANY of the
     three underperforms (talent departure, fund performance issues, cross-selling friction),
     the $360B alternatives AUM premium evaporates.

COMPARISON TO OTHER FINANCE NAMES IN COVERAGE
  GS:   $1,000  Ratio B 6.25×  ✕ AVOID   — pure IB at ATH; analyst PTs 10% below
  MS:   $200.92 Ratio B 3.64×  ✕ AVOID   — WM+IB at ATH; analyst PTs below current
  AXP:  $311.01 Ratio B 1.60×  ◐ WATCHLIST — closed-loop moat; Buffett holds
  BLK:  $1,073  Ratio B 2.05×  ▷ HOLD/TRIM — world's best asset manager; fairly priced
  SPGI: $417.95 Ratio B 1.51×  ◐ WATCHLIST — Mobility spin catalyst imminent

BLK has the BEST fundamentals of the Finance group and the most credible long-term
thesis (passive AUM secular growth + alternatives transformation).  But at current
price, it's fairly valued — a HOLD for existing holders; wait for a pullback to
ACCUMULATE ($860-920) or BUY (below $740) for new positions.
"""

    # ── PART 3: Numbers & signals ─────────────────────────────────────────────
    part3 = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  BLK — Numbers & Signals                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

EPS HISTORY (adjusted / non-GAAP)
  FY2022   ${EPS_HISTORY['FY2022']:>7.2f}   Markets -20%; pure public-markets manager; AUM ~$8-9T
  FY2023   ${EPS_HISTORY['FY2023']:>7.2f}   Modest recovery; rates high; bond fund outflows; +1.3% adj EPS
  FY2024   ${EPS_HISTORY['FY2024']:>7.2f}   +14.4% YoY; GIP closed Oct 1 (adds $170B infra AUM + fees)
  FY2025   ${EPS_HISTORY['FY2025']:>7.2f}   +10.1% YoY; HPS closed July 1 ($190B private credit);
                      Q4 adj EPS $13.16; AUM reaches $13.9T by year-end
  FY2026E  ${EPS_NOW:>7.2f}   Consensus adj EPS; Q1 actual $12.53 (+10.9% YoY); full fee ramp
  FY2027E  ${CONS_EPS_2YR:>7.2f}   Estimate: +14% from FY2026E; GIP+HPS full contribution + organic

EPP — STRUCTURAL FLOOR
  EPS_trough  = ${EPS_TROUGH:.2f}   (severe recession: markets -35%; AUM ~$9T; infra+credit cushion)
  EPP_min_PE  = {EPP_MIN_PE}×       (52-wk low $917.39 ÷ FY2026E $54.29 = 16.9× = market floor confirmed)
  EPP         = ${EPP:.2f}   (= ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×)
  Gap to EPP  = {(CURRENT_PRICE/EPP - 1)*100:.1f}% above floor  (current ${CURRENT_PRICE:.0f} is {CURRENT_PRICE/EPP:.2f}× EPP)

METHOD B — 2-YEAR UPSIDE CEILING
  Consensus EPS (FY2027E)  = ${CONS_EPS_2YR:.2f}
  Exit P/E assumption      = {CONS_EXIT_PE}×   (hybrid passive+alternatives; 15-20× passive + 20-30× alternatives blend)
  Method B price           = ${price_b:.2f}   (+{(price_b/CURRENT_PRICE-1)*100:.1f}% from current)

RATIO B (PRIMARY SIGNAL)
  Ratio B = (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})
          = {CURRENT_PRICE-EPP:.2f} / {price_b-CURRENT_PRICE:.2f}
          = {ratio_b:.2f}×   →   ▷ HOLD/TRIM  (range: 1.75–2.50×)

SCENARIO ANALYSIS
  BEAR   ${SCENARIOS['BEAR']['price']:>8.2f}   EPP floor; markets -35%; large AUM outflows; infra/credit slowdown
  BASE   ${SCENARIOS['BASE']['price']:>8.2f}   FY2026E $54.29 × 20× = $1,086; organic growth steady; ~current
  BULL   ${SCENARIOS['BULL']['price']:>8.2f}   Method B; FY2027E $62 × 22×; alt fees fully ramped
  XBULL  ${SCENARIOS['XBULL']['price']:>8.2f}   Alternatives re-rating (28×); $62 EPS; BX/APO-like premium

SOFTMAX COMPOSITE ENGINE
  Market composite (inferred)  =  {market_composite:.3f}
  (Market pricing BLK at BASE — current price ≈ FY2026E consensus × 20×)

SCA — SIGNAL CATALYST ADJUSTMENTS
{"".join(f"  {f['label'][:50]:<50}  {f['rating']:+.2f} × {f['weight']:.2f}  =  {f['rating']*f['weight']:+.4f}" + chr(10) for f in SCA_FACTORS)}
  sca_raw     =  {sca_raw:+.4f}
  sca_adj     =  {sca_adj:+.4f}  (= sca_raw / 2.0)
  adj_composite  =  {market_composite:.3f}  +  {sca_adj:+.4f}  =  {adj_composite:.3f}

SOFTMAX SCENARIO WEIGHTS  (at adj_composite = {adj_composite:.3f})
{"".join(f"  {s:<6}  {w[s]*100:5.1f}%   ${SCENARIOS[s]['price']:,.2f}" + chr(10) for s in ['BEAR','BASE','BULL','XBULL'])}
  Expected price (probability-weighted)  =  ${exp_p:,.2f}

ASSET MANAGER METRICS
  Total AUM (Q1 2026)         =  ${AUM_TOTAL_T:.1f}T  (from $11.6T a year ago; +$2.3T)
  Long-term NNA Q1 2026       =  ${NNA_Q1_2026:.1f}B
  Organic growth rate         =  {ORGANIC_GROWTH:.0f}%  (last 12 months; vs 3% in Q1 2024)
  Adj operating margin        =  {ADJ_OP_MARGIN:.1f}%  (Q1 2026; expanded from 43.2% prior year)
  GIP alternatives AUM        =  ${GIP_AUM_B:.0f}B  (closed Oct 1, 2024; infrastructure)
  HPS private credit AUM      =  ${HPS_AUM_B:.0f}B  (closed July 1, 2025; direct lending)
  Analyst avg PT              =  $1,251–$1,254  (+{(1253/CURRENT_PRICE-1)*100:.0f}% from current)
  Dividend                    =  ${DIVIDEND_ANN:.2f}/yr  ({DIVIDEND_ANN/CURRENT_PRICE*100:.2f}% yield); 13 consecutive annual increases

SIGNAL ENTRY GUIDE
  ✕ AVOID      above  $1,200  (ratio_b > 2.5×; ATH territory)
  ▷ HOLD/TRIM  $1,000 – $1,200  (current; ratio_b 1.75–2.50×)  ← HERE
  ◐ WATCHLIST  $  920 – $1,000  (ratio_b 1.10–1.75×)
  ◎ ACCUMULATE $  860 – $  920  (ratio_b 0.75–1.10×; near April 2026 low)
  ◉ BUY        below  $  740  (ratio_b < 0.75×; severe dislocation)

  52-wk low $917.39 was ACCUMULATE at ratio_b 0.99× — +17% recovery to current HOLD.
  Best re-entry: ACCUMULATE $860-920 on next macro scare or market drawdown.
  Analyst avg PT $1,254 (+16.9%); strong buy consensus with $1,393 high estimate.
"""

    print(part1)
    print(part2)
    print(part3)
