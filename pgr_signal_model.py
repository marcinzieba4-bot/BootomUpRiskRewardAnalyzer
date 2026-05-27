"""
The Progressive Corporation  (PGR)
BottomUp Risk/Reward Analyzer — Signal Model
"""
import math

# ── Core inputs ──────────────────────────────────────────────────────────────
TICKER        = "PGR"
COMPANY       = "The Progressive Corporation"
SECTOR        = "Personal Auto Insurance · Commercial Lines · Property · Snapshot Telematics"

CURRENT_PRICE  = 199.51   # PGR — fetched via web search, 2026-05-22 (near current as of 2026-05-26)
                            # Stock near 52-wk low; mkt cap ~$116.9B at $199.51 × 585.91M shares
PRICE_52W_LOW  = 192.02   # May 2026 low — stock is only 3.9% above its 52-wk floor
PRICE_52W_HIGH = 289.82   # Nov/Dec 2025 high; PGR is 31.2% below ATH (significant drawdown)
SHARES_M       = 585.91   # Shares outstanding (confirmed); mkt cap $116.9B / $199.51
DIVIDEND_FIXED =   0.40   # Fixed quarterly dividend: $0.10/qtr × 4 = $0.40/yr (stable component)
DIVIDEND_VAR_LAST = 13.50 # Variable annual dividend paid Jan 8 2026 (for FY2025 performance)
                            # Total received in FY2025: $13.50 + $0.40 = $13.90/share = 6.97% yield
                            # IMPORTANT: variable dividend is discretionary; future amounts depend
                            # on FY2026 underwriting results. Model uses fixed $0.40 for forward yield.

# ── EPS history (GAAP diluted) ────────────────────────────────────────────────
# Progressive's earnings are highly sensitive to combined ratio (CR). When CR < 96%
# (the 4% underwriting margin target), Progressive earns exceptional profits. When
# CR > 97%, underwriting losses compress EPS dramatically; investment income provides
# the only floor. This creates enormous year-to-year EPS volatility.
EPS_HISTORY = {
    "FY2022": 1.18,    # TROUGH: CR 95.8%; auto repair inflation spike (supply chains) +
                        # Hurricane Ian cat losses on Property segment. Near-breakeven underwriting.
                        # Investment income (lower rate environment) provided minimal cushion.
    "FY2023": 6.58,    # Recovery: rates rising aggressively (+20-30% rate increases);
                        # CR improving toward 96%; market share temporarily sacrificed for profit
    "FY2024": 14.40,   # Inflection: CR ~87-88%; rate increases fully earned; NPW +21%;
                        # +118.8% EPS YoY — the "pricing power" year. Market share reaccelerating.
    "FY2025": 19.23,   # Record: CR ~85-87%; 4%+ margin vs 13%+ actual; NPW growing ~15%;
                        # policies in force +9%; $13.50 annual dividend declared (profit-sharing)
}
EPS_NOW = 16.36   # FY2026E adj EPS analyst consensus; Q1 2026 actual $4.96 (+2.9% beat vs $4.82)
                   # Consensus implies CR normalization to ~90-92% in H2 2026 vs Q1's exceptional 86.4%
                   # NOTE: if CR stays near Q1 2026 levels all year, EPS could be $18-20

# ── EPP (Earnings Power Price) — structural floor ────────────────────────────
EPS_TROUGH  = 4.50    # Severe combined ratio deterioration: CR ~101% (underwriting loses $900M at
                        # $90B NPW); investment income on ~$70B invested assets provides floor (~$4B
                        # pre-tax investment income → ~$2.5B after-tax → $4.27/share). $4.50 = CR
                        # ~101% + full investment income offset. Historical reference: FY2022 CR 95.8%
                        # → EPS $1.18 (brutal; but included inflation surge + cat losses simultaneously).
                        # $4.50 = near-recession scenario; not the 2008-level perfect storm scenario.
EPP_MIN_PE  = 22      # Progressive franchise floor: tech moat (Snapshot telematics) + market share
                        # momentum means the market never truly abandons PGR even in bad years.
                        # In FY2022 (EPS $1.18), PGR stock stayed $90-140 (75-120× EPS!) because
                        # the market priced in rate cycle recovery. For normalised $4.50 trough,
                        # 22× reflects the market assigning franchise/recovery value even in down cycle.
                        # Calibration: 52-wk low $192 / FY2026E $16.36 = 11.7× forward — market
                        # confirmed 11-12× as forward floor when conditions are uncertain.
EPP         = EPS_TROUGH * EPP_MIN_PE   # = $99.00

# ── Method B (2-year normalised upside ceiling) ───────────────────────────────
CONS_EPS_2YR  = 17.00   # FY2027E adj EPS: slightly above analyst consensus $16.36 to account for
                          # market share gains continuing (policies in force +9% Q1 2026 = embedded
                          # premium growth). At CR 90-91% on NPW ~$100B, EPS $17 is achievable.
                          # Conservative relative to FY2025 actual $19.23 — builds in partial CR
                          # normalization while acknowledging PGR keeps taking market share.
CONS_EXIT_PE  = 22        # PGR has historically traded 20-28× in normal/good environments.
                          # At 22×, BUY thesis requires PGR to re-rate from current depressed
                          # 12× forward P/E back toward historical norms. Catalyst: sustained
                          # proof that CR can stay in 88-92% range (vs market's 96% fear).
price_b = CONS_EPS_2YR * CONS_EXIT_PE   # = $374.00

# ── Primary signal: Ratio B ───────────────────────────────────────────────────
ratio_b = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
# = (199.51 - 99.00) / (374.00 - 199.51) = 100.51 / 174.49 = 0.576×
# Signal: ◉ BUY (< 0.75×) — stock near 52-wk low with record earnings; 87.5% upside to Method B

# ── Softmax composite engine ──────────────────────────────────────────────────
T = 0.60
SCENARIOS = {
    "BEAR":  {"price":  99.00, "label": "BEAR"},   # EPP floor; CR 101%+ sustained; cat loss year
    "BASE":  {"price": 231.00, "label": "BASE"},   # Analyst consensus PT; CR ~90%; FY2026E × 14×
    "BULL":  {"price": 374.00, "label": "BULL"},   # Method B; FY2027E $17 × 22×; CR 90-91%
    "XBULL": {"price": 480.00, "label": "XBULL"},  # CR stays 88%; FY2027E $19 × 25× re-rating
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
    {"label": "Snapshot telematics moat — unmatched pricing data",
     "rating": +0.40, "weight": 0.25,
     "note": "Progressive's Snapshot program collects real-time driving data from 30M+ vehicles."
             " This telematics data allows PGR to price individual risk with far greater precision"
             " than competitors relying on demographics alone. Result: PGR systematically attracts"
             " the best-risk drivers (those willing to be monitored) and avoids bad-risk drivers."
             " No competitor has replicated this data moat after 15+ years of Snapshot. Flo brand"
             " + telematics + AI underwriting = structural pricing advantage compounding annually."},
    {"label": "31% drawdown from ATH — near 52-wk low with record earnings",
     "rating": +0.30, "weight": 0.20,
     "note": "PGR at $199.51 is 31.2% below its 52-wk high of $289.82 and only 3.9% above its"
             " 52-wk low of $192.02. The selloff occurred DESPITE record FY2025 EPS ($19.23) and"
             " strong Q1 2026 ($4.96 beat). Market is pricing CR normalization as certainty."
             " Trading at 12.2× FY2026E consensus — historically cheap; PGR typically 20-28×."
             " Price dislocation: record earnings + 31% drawdown = unusual asymmetry."},
    {"label": "Market share acceleration — policies in force +9%",
     "rating": +0.25, "weight": 0.15,
     "note": "Q1 2026: policies in force +9% YoY. Progressive is taking market share FROM State"
             " Farm (which faced capital constraints and reduced new business) and GEICO (which"
             " has struggled with tech/pricing upgrades). Each new policy = multiyear premium"
             " stream; PGR's superior loss ratios mean it earns MORE per policy than peers."
             " The market share gains embed 9%+ premium growth regardless of rate level."},
    # Headwinds
    {"label": "Combined ratio normalization — EPS could halve",
     "rating": -0.30, "weight": 0.25,
     "note": "Q1 2026 CR 86.4% (underwriting margin 13.6%) vs PGR's own 96% target. History:"
             " FY2022 CR 95.8% → EPS $1.18. FY2025 CR ~86% → EPS $19.23. A single 10-point CR"
             " deterioration collapses EPS dramatically. Normalization catalysts: (1) weather"
             " events (cat losses); (2) social inflation (nuclear verdicts increasing jury awards);"
             " (3) medical cost inflation; (4) used-car price declines lower subrogation recovery."
             " At 96% CR, FY2027E EPS = ~$8-10. Market is partly pricing this scenario."},
    {"label": "Tariff-driven auto parts inflation = higher claims",
     "rating": -0.25, "weight": 0.20,
     "note": "US tariffs on imported auto parts (Chinese components, Canadian steel) raise the"
             " cost of vehicle repair. Auto parts/repair = largest component of auto claims."
             " If parts costs rise 10-15% and PGR can't immediately pass through in rates,"
             " the CR deteriorates. PGR has strong pricing power to respond over 12-18 months,"
             " but there is a lag. This is the near-term risk to the exceptional Q1 2026 CR."},
    {"label": "Rate cycle saturation / customer shopping risk",
     "rating": -0.15, "weight": 0.15,
     "note": "Progressive raised rates 20-30% from 2022-2024. At current elevated premium levels,"
             " customers are shopping more aggressively for cheaper alternatives. Customer retention"
             " rates are under pressure. As competitors (State Farm, GEICO) complete their own"
             " rate increases, competitive pricing intensifies. Renewal premium growth slows."},
]

sca_raw = sum(f["rating"] * f["weight"] for f in SCA_FACTORS)
sca_adj = sca_raw / 2.0

adj_composite = market_composite + sca_adj

# ── Insurance-specific metrics ────────────────────────────────────────────────
COMBINED_RATIO_Q1_2026   = 86.4    # Q1 2026 companywide CR (underwriting margin 13.6%)
COMBINED_RATIO_TARGET    = 96.0    # PGR's own 4% underwriting margin goal
COMBINED_RATIO_FY2022    = 95.8    # FY2022 "trough" year (barely profitable)
POLICIES_IN_FORCE_GROWTH = 9.0     # Q1 2026 policies in force YoY growth (%)
NPW_Q1_2026              = 23.6    # Net premiums written Q1 2026 ($B; +6% YoY from $22.2B)
UNDERWRITING_MARGIN_Q1   = 13.6    # Q1 2026 underwriting margin (vs 4% target = 3.4× target)
NET_PROFIT_Q1_2026       = 2.8     # Q1 2026 net income ($B)

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
"""

    # ── PART 2: Analyst commentary ────────────────────────────────────────────
    part2 = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PGR  |  The Progressive Corporation  |  ◉ BUY                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

SNAPSHOT  (as of 2026-05-22)
  Price         ${CURRENT_PRICE:.2f}   52-wk range  ${PRICE_52W_LOW:.2f} – ${PRICE_52W_HIGH:.2f}
  Shares        {SHARES_M:.2f}M       Mkt cap      ~$116.9B
  Div (fixed)   ${DIVIDEND_FIXED:.2f}/yr        Div (variable) ${DIVIDEND_VAR_LAST:.2f} paid Jan 2026
  FY2026E EPS   ${EPS_NOW:.2f}          FW P/E       {CURRENT_PRICE/EPS_NOW:.1f}×   (historically 20-28×)
  Q1 2026 CR    {COMBINED_RATIO_Q1_2026:.1f}%           CR target    {COMBINED_RATIO_TARGET:.1f}% (4% margin goal)
  EPP floor     ${EPP:.2f}        Ratio B      {ratio_b:.3f}×  →  ◉ BUY

THE BUSINESS: AMERICA'S MOST PRECISE AUTO INSURER
Progressive is the #1 or #2 personal auto insurer in the US (competing with State Farm
for the top spot) and the clear technology leader in risk pricing.  The business is
deceptively simple: collect premiums, invest the float, pay claims.  The edge is in
HOW you price risk — and Progressive's Snapshot telematics program is a decade+ ahead.

THE SNAPSHOT MOAT (why PGR keeps winning)
Snapshot collects real-time driving data: how hard you brake, when you drive, how far.
30M+ vehicles enrolled.  This telematics dataset allows Progressive to price risk at
the individual driver level with far greater precision than competitors relying on:
  - Age, gender, zip code, credit score (traditional actuarial inputs)
  - Progressive: + actual braking patterns, night driving, mileage, acceleration

The consequence: PGR systematically attracts the safest drivers (those WILLING to be
monitored = demonstrating confidence they drive well) and avoids the riskiest.  Its
loss ratios are structurally lower than peers at the same premium level.

No competitor has replicated this after 15+ years.  Flo (world's most recognisable
insurance mascot) + Snapshot + sophisticated AI underwriting = durable moat.

THE COMBINED RATIO PARADOX
Progressive targets a 96% combined ratio (4% underwriting margin) intentionally.
Unlike most insurers that maximise profit per policy, PGR uses the 4% target to
GROW market share — it deliberately underprices vs peers willing to accept 5-8%
margins.  In doing so, it captures the best risks at scale.

When PGR's CR drops below 96%, it is earning excess profit above its target:
  FY2022: CR 95.8%  → EPS $1.18    (barely above target; cat losses + inflation)
  FY2023: CR ~95%   → EPS $6.58    (rates catching up)
  FY2024: CR ~87%   → EPS $14.40   (rates fully adjusted; excess profit)
  FY2025: CR ~86%   → EPS $19.23   (exceptional; 13%+ margin vs 4% target)
  Q1 2026: CR 86.4% → EPS $4.96 (annualised ~$19.84)

The market has CORRECTLY identified that 86.4% CR is not the new normal.  The question
is: what is the "new normal" CR for Progressive?
  - PGR's own target: 96%  (4% margin)
  - Pre-2022 era (2018-2021): ~95-97% CR
  - Post-rate-cycle: possibly 90-93% (higher rates + telematics = sustainably better)

At 90% CR on $95B NPW: underwriting margin $9.5B → after-tax income ~$10.5B → EPS $17.90
At 93% CR on $95B NPW: underwriting margin $6.65B → after-tax income ~$8.6B → EPS $14.68
Analyst consensus $16.36 implies CR ~91-92%.  The BEAR case is 96% CR → EPS ~$10.

WHY BUY AT CURRENT PRICE NEAR 52-WK LOW
The PARADOX: record earnings + stock near 52-wk lows.

  FY2025 EPS: $19.23 (record)          Stock: $199.51 = 10.4× trailing EPS
  Q1 2026 EPS: $4.96 (strong beat)     FW P/E: 12.2× consensus FY2026E
  Analyst avg PT: $231                  Analyst consensus: "Hold"

The market is pricing PGR at 12× forward EPS — the BEAR case multiple — because it
believes the exceptional CR will mean-revert.  This creates the asymmetry:

  IF CR stays at 90-92% (analyst base case):
    EPS $16-17, re-rate to 18-20× = $288-340 = +44-70% upside
  IF CR reverts to 95% (bear case):
    EPS ~$12, at 15× = $180 = -10% downside
  IF CR stays at 86-88% (continuation of current):
    EPS $19, at 20× = $380 = +90% upside

At $199, the BEAR case is roughly priced in already.  If CR mean-reverts to 95%, the
stock is fairly valued at $180 (only -10% downside).  But any scenario above the pure
BEAR case = significant upside.  The risk/reward is asymmetric: limited downside to
~$180, upside to $288-380+.

DIVIDEND STRUCTURE (unique to Progressive)
Progressive pays:
  Fixed quarterly:  $0.10/share × 4 = $0.40/yr  (stable; 0.20% yield)
  Variable annual:  Based on FY profitability formula; January payment each year
                    FY2025 → $13.50/share paid Jan 2026 (6.77% yield!)
                    FY2024 → ~$8.00/share estimated
                    FY2023 → $0 (below profitability threshold)
                    FY2022 → $0 (CR too close to target; no variable declared)

At $199, the guaranteed yield is 0.20% — but the POTENTIAL annual dividend if FY2026
is a good year could add $8-15/share more.  Variable dividend = profit sharing with shareholders.

RISK FACTORS
  CR normalization:  The dominant risk.  If auto frequency increases (miles driven rising
  post-COVID) or severity surges (tariff-driven parts costs), CR rises and EPS falls sharply.
  Social inflation:  "Nuclear verdicts" in auto liability cases are structurally increasing
  jury awards; PGR's personal injury liability reserves could be inadequate.
  Competition:  State Farm + GEICO both completed aggressive rate increases in 2024-2025.
  Now pricing competitively again — PGR may lose some rate advantage it temporarily held.
  Hurricane / cat:  Property segment (homeowners) is growing; cat exposure increasing.
"""

    # ── PART 3: Numbers & signals ─────────────────────────────────────────────
    part3 = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PGR — Numbers & Signals                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

EPS HISTORY (GAAP diluted)
  FY2022   ${EPS_HISTORY['FY2022']:>6.2f}   TROUGH: CR 95.8%; auto inflation + Hurricane Ian; near-breakeven UW
  FY2023   ${EPS_HISTORY['FY2023']:>6.2f}   Recovery: rates rising; CR ~95%; market share sacrifice for profit
  FY2024   ${EPS_HISTORY['FY2024']:>6.2f}   Inflection: CR ~87%; rates fully earned; NPW +21%; +119% EPS YoY
  FY2025   ${EPS_HISTORY['FY2025']:>6.2f}   Record: CR ~86%; 3.4× above 4% target; PIF +9%; $13.50 var div
  FY2026E  ${EPS_NOW:>6.2f}   Consensus: CR ~91% H2 normalization; Q1 actual $4.96 (+2.9% beat)
  FY2027E  ${CONS_EPS_2YR:>6.2f}   Estimate: CR ~90-91%; policies in force +7-8%; continued share gains

EPP — STRUCTURAL FLOOR
  EPS_trough  = ${EPS_TROUGH:.2f}   (CR ~101%; investment income $4B/yr after-tax offset; rare scenario)
  EPP_min_PE  = {EPP_MIN_PE}×       (franchise floor; PGR never truly abandoned even in FY2022 at $1.18 EPS)
  EPP         = ${EPP:.2f}   (= ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×)
  Gap to EPP  = {(CURRENT_PRICE/EPP - 1)*100:.1f}% above floor  (current ${CURRENT_PRICE:.0f} is {CURRENT_PRICE/EPP:.2f}× EPP)

METHOD B — 2-YEAR UPSIDE CEILING
  Consensus EPS (FY2027E)  = ${CONS_EPS_2YR:.2f}   (CR ~90-91%; market share gains embedded)
  Exit P/E assumption      = {CONS_EXIT_PE}×   (PGR historical 20-28×; 22× assumes partial re-rating from 12× trough)
  Method B price           = ${price_b:.2f}   (+{(price_b/CURRENT_PRICE-1)*100:.1f}% from current)

RATIO B (PRIMARY SIGNAL)
  Ratio B = (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})
          = {CURRENT_PRICE-EPP:.2f} / {price_b-CURRENT_PRICE:.2f}
          = {ratio_b:.3f}×   →   ◉ BUY  (threshold: < 0.75×)

  Interpretation: for every $1 of downside to EPP floor, there is ${1/ratio_b:.2f} of upside to Method B.
  Asymmetry is decisively favourable.

SCENARIO ANALYSIS
  BEAR   ${SCENARIOS['BEAR']['price']:>7.2f}   EPP floor; CR 101%+; sustained underwriting loss + cat losses
  BASE   ${SCENARIOS['BASE']['price']:>7.2f}   Analyst consensus PT; CR ~90%; FY2026E $16.36 × 14×
  BULL   ${SCENARIOS['BULL']['price']:>7.2f}   Method B; FY2027E $17 × 22×; re-rating from 12× to 22×
  XBULL  ${SCENARIOS['XBULL']['price']:>7.2f}   CR stays 88%; FY2027E $19-20; market re-rates to 25×

COMBINED RATIO SENSITIVITY
  CR 86% (Q1 2026 pace)   → EPS ~$19   at 20× = $380  (+90% from current)
  CR 90% (bull case)      → EPS ~$17   at 22× = $374  (+87% from current = Method B)
  CR 92% (base case)      → EPS ~$15   at 18× = $270  (+35% from current)
  CR 95% (normalization)  → EPS ~$11   at 15× = $165  (-17% from current)
  CR 99% (bad year)       → EPS ~$ 6   at 18× = $108  (-46% from current; near EPP)

  The market at $199 is pricing CR ~95%+ (the bear case). If PGR achieves analyst consensus
  CR 91-92%, the stock re-rates +35-87% from current. Downside (to bear case) is ~17%.

SOFTMAX COMPOSITE ENGINE
  Market composite (inferred)  =  {market_composite:.3f}
  (Market pricing PGR between BEAR and BASE — deeply discounted vs fundamentals)

SCA — SIGNAL CATALYST ADJUSTMENTS
{"".join(f"  {f['label'][:50]:<50}  {f['rating']:+.2f} × {f['weight']:.2f}  =  {f['rating']*f['weight']:+.4f}" + chr(10) for f in SCA_FACTORS)}
  sca_raw     =  {sca_raw:+.4f}
  sca_adj     =  {sca_adj:+.4f}  (= sca_raw / 2.0)
  adj_composite  =  {market_composite:.3f}  +  {sca_adj:+.4f}  =  {adj_composite:.3f}

SOFTMAX SCENARIO WEIGHTS  (at adj_composite = {adj_composite:.3f})
{"".join(f"  {s:<6}  {w[s]*100:5.1f}%   ${SCENARIOS[s]['price']:,.2f}" + chr(10) for s in ['BEAR','BASE','BULL','XBULL'])}
  Expected price (probability-weighted)  =  ${exp_p:,.2f}

INSURANCE METRICS
  Q1 2026 combined ratio          =  {COMBINED_RATIO_Q1_2026:.1f}%   (companywide; vs {COMBINED_RATIO_TARGET:.0f}% 4% margin target)
  Q1 2026 underwriting margin     =  {UNDERWRITING_MARGIN_Q1:.1f}%   (Personal Lines 14.0%; Commercial 11.0%)
  Q1 2026 net premiums written    =  ${NPW_Q1_2026:.1f}B   (+{(NPW_Q1_2026/22.2-1)*100:.0f}% YoY from $22.2B)
  Q1 2026 net profit              =  ${NET_PROFIT_Q1_2026:.1f}B
  Policies in force growth (Q1)   =  {POLICIES_IN_FORCE_GROWTH:.0f}% YoY
  FY2022 combined ratio (trough)  =  {COMBINED_RATIO_FY2022:.1f}%   → EPS $1.18 (the true floor reference)
  Analyst avg PT                  =  $231  (+{(231/CURRENT_PRICE-1)*100:.1f}% from current)
  Analyst consensus               =  "Hold" (25 analysts; PT range $190-$295)

SIGNAL ENTRY GUIDE
  ✕ AVOID      above  $296  (ratio_b > 2.50×)
  ▷ HOLD/TRIM  $274 – $296  (ratio_b 1.75–2.50×; 52-wk high $289.82 was HOLD at 2.27×)
  ◐ WATCHLIST  $244 – $274  (ratio_b 1.10–1.75×)
  ◎ ACCUMULATE $217 – $244  (ratio_b 0.75–1.10×)
  ◉ BUY        below  $217  (ratio_b < 0.75×)  ← HERE at $199.51

  52-wk low $192.02 = ratio_b {(PRICE_52W_LOW-EPP)/(price_b-PRICE_52W_LOW):.3f}× → deep BUY (current best entry in Finance coverage)
  52-wk high $289.82 = ratio_b {(PRICE_52W_HIGH-EPP)/(price_b-PRICE_52W_HIGH):.2f}× → HOLD/TRIM territory
  Variable dividend upside: if FY2026 CR stays 90%, expect $10-12 variable div payout Jan 2027.
"""

    print(part1)
    print(part2)
    print(part3)
