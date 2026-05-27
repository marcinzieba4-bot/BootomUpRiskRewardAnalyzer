"""
kkr_signal_model.py — KKR & Co. Inc. (NYSE: KKR)
Pioneer of the leveraged buyout. Global alt asset manager: PE, credit, infrastructure, insurance.
Signal framework: EPP floor + Method B + SCA softmax engine.
"""

import math

# ── LIVE PRICE (fetched before model construction) ──────────────────────────
CURRENT_PRICE = 94.19    # KKR — fetched from Yahoo Finance / stockanalysis.com, 2026-05-27
# 52-wk range: $82.67 (Apr 2026 tariff-shock low) – $153.87 (Nov 2025 high)
# Market cap ~$85.3B; shares ~905M; dividend yield ~0.83%

TICKER        = "KKR"
COMPANY       = "KKR & Co. Inc."
SHARES_M      = 905          # million diluted shares
DIVIDEND_ANN  = 0.78         # USD/yr; raised from $0.74 for Q1 2026;
                              # 7th consecutive annual increase post C-Corp conversion (2018)

# ── EPS CONVENTION ───────────────────────────────────────────────────────────
# After-Tax Distributable Earnings (ATDE) per adjusted share — KKR's primary metric.
# Similar to BX's Distributable Earnings. Includes:
#   Fee-Related Earnings (FRE):   management fees + fee income – operating expenses (RECURRING)
#   Realized Performance Income:  carried interest on actual exits and realizations (LUMPY)
#   Realized Investment Income:   returns from KKR's own balance sheet investments
# Excludes: mark-to-market of unrealized investments, GAAP intangible amortization.
# GAAP EPS is far noisier (unrealized marks on $15B+ balance sheet can swing $2-3/share/quarter).

EPS_HISTORY = {
    "FY2022": 3.90,   # deal market active; PE exits strong; hard asset valuations high
    "FY2023": 3.65,   # -7% YoY; deal market freeze (rates spike kills PE exits); FRE growing but carry dry
    "FY2024": 4.70,   # recovery; AUM scaling; Global Atlantic insurance channel ramping
    "FY2025": 4.87,   # record $129B fundraising; but realizations still muted (deal market sluggish);
                       #   FRE record at $4.13/sh (+13% YoY); AUM $744B; dry powder $118B
}

# Q1 2026: ATDE = $1.39/share (+20% YoY); FRE = $1.13/share (+23% YoY); AUM $758B (+14% YoY)
# Management targets "$7+" ATDE for FY2026; deal market beginning to thaw

EPS_NOW       = 5.50     # NTM; Q1 2026 $1.39 × 4 = $5.56 annualized; H2 2026 realizations
                          # expected to accelerate; conservative mid-point of FY2025 actual ($4.87)
                          # and FY2026E consensus ($6.77)
EPS_TROUGH    = 3.50     # structural floor based on FRE: in severe bear market (2008 style),
                          # realizations = $0 but locked-up capital fees continue; FY2025 FRE = $4.13/sh
                          # in distress, FRE could compress slightly (AUM growth stops; fee resets)
EPP_MIN_PE    = 18        # same as BX: locked-up capital (10-yr funds), no redemption risk, moat
                          # Alt asset manager with locked institutional capital cannot be "run";
                          # 18× of FRE floor = appropriate premium for durability of earnings base
EPP           = EPP_MIN_PE * EPS_TROUGH   # = $63.00

CONS_EPS_2YR  = 8.13     # FY2027E analyst consensus (range $7.23–$8.82); KKR guides $7+ for FY2026
CONS_EXIT_PE  = 22        # normalized alt asset manager multiple; historical 20-30× in growth cycle;
                          # 22× = conservative mid-range (same as BX); reflects deal market recovery
price_b       = CONS_EPS_2YR * CONS_EXIT_PE   # = $178.86

ratio_b       = (CURRENT_PRICE - EPP) / (price_b - CURRENT_PRICE)
epp_gap_pct   = (CURRENT_PRICE - EPP) / EPP * 100

# Scenario prices
scenarios = {
    "BEAR":  63,     # EPP; $3.50 × 18; deal market collapses; realizations = $0; FRE-only earnings
    "BASE":  130,    # FY2026E $6.77 × 19×; partial multiple recovery; consensus analyst zone
    "BULL":  179,    # Method B; FY2027E $8.13 × 22×; normalized multiple
    "XBULL": 240,    # FY2027E $8.13 × 30×; deal boom; peak cycle; full re-rate to growth premium
}

# ── SOFTMAX ENGINE ───────────────────────────────────────────────────────────
T = 0.60
CENTRES = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}

def softmax_weights(composite):
    logits = {k: -((composite - c) ** 2) / T for k, c in CENTRES.items()}
    max_l  = max(logits.values())
    exps   = {k: math.exp(v - max_l) for k, v in logits.items()}
    total  = sum(exps.values())
    return {k: v / total for k, v in exps.items()}

def expected_price(composite):
    w = softmax_weights(composite)
    return sum(w[k] * scenarios[k] for k in scenarios)

def infer_composite(target_price, lo=1.0, hi=4.0, iterations=60):
    for _ in range(iterations):
        mid = (lo + hi) / 2
        if expected_price(mid) < target_price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

market_composite = infer_composite(CURRENT_PRICE)

# ── SCA — SIGNAL CATALYST ADJUSTMENTS ───────────────────────────────────────
sca_items = [
    # (description, score, weight)
    ("Record AUM $758B (+14% YoY); FPAUM $615B (+17%); $129B raised FY2025; "
     "$120B dry powder — all-time highs across every growth metric despite price collapse",
     +0.30, 0.25),
    ("Global Atlantic $219B insurance AUM: perpetual capital + stable investment spread; "
     "non-cyclical FRE contributor growing 15%+ YoY; insulates earnings from PE cycle",
     +0.30, 0.25),
    ("39% below $153.87 52-wk high; 11.6× FY2027E EPS; market extrapolating deal-market freeze "
     "into perpetuity despite $120B dry powder being deployed as macro settles",
     +0.25, 0.20),
    ("PE deal market uncertainty: tariffs + elevated rates = muted M&A/IPO windows; "
     "carry realizations may disappoint vs. $6.77-8.13 consensus estimates in near term",
     -0.35, 0.25),
    ("Alt asset manager sector de-rating: BX/APO/CG/ARES all down 30-40% from highs; "
     "multiple compression may persist as long as macro uncertainty remains elevated",
     -0.20, 0.20),
    ("KKR PE concentration ~40% of AUM: most sensitive to deal cycle; FRE grows steadily "
     "but carry timing uncertainty is highest here vs. credit/infrastructure peers",
     -0.15, 0.05),
]

sca_raw = sum(score * weight for _, score, weight in sca_items)
sca_adj = sca_raw / 2.0
adj_composite = market_composite + sca_adj

adj_weights    = softmax_weights(adj_composite)
expected_px    = expected_price(adj_composite)

# ── SIGNAL ───────────────────────────────────────────────────────────────────
if   ratio_b < 0.75:  signal = "◉ BUY"
elif ratio_b < 1.10:  signal = "◎ ACCUMULATE"
elif ratio_b < 1.75:  signal = "◐ WATCHLIST"
elif ratio_b < 2.50:  signal = "▷ HOLD/TRIM"
else:                  signal = "✕ AVOID"

# ── OUTPUT ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    SEP  = "=" * 70
    DASH = "─" * 70

    print(SEP)
    print("KKR & CO. INC. (KKR) — SIGNAL MODEL")
    print("Founder of modern private equity. Alt asset manager: PE, Credit, Infra, Insurance.")
    print(SEP)

    print("""
SIGNAL FRAMEWORK — METHOD B + SCA ENGINE
─────────────────────────────────────────
EPP  = EPS_TROUGH × EPP_MIN_PE          (structural floor; ATDE per share basis)
Ratio B = (Price − EPP) / (price_b − Price)

KKR EPS convention: After-Tax Distributable Earnings (ATDE) per adjusted share.
Includes Fee-Related Earnings (FRE, recurring management fees) + Realized Performance
Income (carried interest on exits) + Realized Investment Income (own balance sheet).
Excludes mark-to-market of unrealized investments. GAAP EPS is meaningless for
alt asset managers — unrealized marks on a $15B+ balance sheet create $2-3/share
quarterly swings completely unrelated to economic earnings.

SIGNAL THRESHOLDS
  Ratio B < 0.75   →  ◉ BUY
  0.75 – 1.10      →  ◎ ACCUMULATE
  1.10 – 1.75      →  ◐ WATCHLIST
  1.75 – 2.50      →  ▷ HOLD/TRIM
  > 2.50           →  ✕ AVOID

EPP_MIN_PE = 18×  rationale:
  KKR manages $615B in fee-paying AUM locked in 10-year closed-end funds. Unlike
  mutual funds or hedge funds, investors CANNOT redeem. When markets crash, KKR's
  management fees on committed capital continue — there is no run risk. The FRE
  component ($4.13/share in FY2025, growing 23% YoY) is structurally defensive.
  In 2009 (worst financial crisis in 80 years), KKR's management fees did NOT
  collapse because funds were locked up. 18× of the trough FRE base is the floor.
  Same multiple as BX (alt manager peer); appropriately higher than banks/brokers
  that face real capital flight risk.
""")

    print("KKR & CO. INC. (KKR) — THE PIONEER OF PRIVATE EQUITY, PRICED FOR DISTRESS")
    print("=" * 70)

    print("""
BUSINESS OVERVIEW
─────────────────
KKR & Co. Inc. was founded in 1976 by Henry Kravis, Jerome Kohlberg, and George
Roberts — the three men who invented the modern leveraged buyout (LBO). The 1989
RJR Nabisco takeover ($31.4B — still one of history's largest LBOs) made KKR
legendary. Today KKR has evolved far beyond PE into a diversified multi-strategy
alternative asset manager with $758B AUM (as of Q1 2026). CEO since 2021: Scott
Nuttall. Co-chairmen: Henry Kravis and George Roberts (both still active advisors).
C-Corp conversion in 2018 opened KKR to institutional and index investors.

KKR THREE-ENGINE ARCHITECTURE ($758B AUM TOTAL)
──────────────────────────────────────────────
  PRIVATE EQUITY        ~$140B AUM   (the founding business; flagship PE funds)
  ─────────────────────────────────
  Buyout funds targeting industrial, healthcare, tech, consumer, financial. Classic
  LBO model: acquire, improve operations, sell 5-7 years later. Carry = 20% of
  profits above hurdle. Currently: KKR Americas Fund XIII, KKR European Fund VI,
  KKR Asian Fund V all in market. $129B raised in FY2025.

  CREDIT & INSURANCE    ~$400B AUM   (fastest-growing; the new growth engine)
  ─────────────────────────────────
  Leveraged Credit:      $144B  (CLOs, leveraged loans, high yield bonds)
  Asset-Based Finance:    $92B  (mortgages, consumer loans, equipment finance)
  Corporate Private Credit: $49B  (direct lending, unitranche)

  Global Atlantic ($219B): KKR acquired Global Atlantic (life/annuity insurer) in
  2021. GA provides perpetual capital — insurance policyholder liabilities that
  never "redeem." KKR manages GA's $219B investment portfolio, earning management
  fees on every dollar. As GA grows by writing new annuity policies (and it is
  growing ~15%/yr), KKR's FRE base grows with it. This is the structural moat
  that distinguishes KKR from pure PE peers.

  REAL ASSETS           ~$210B AUM   (infrastructure + real estate)
  ─────────────────────────────────
  Infrastructure: $100B+ — KKR Global Infrastructure funds; energy transition,
  digital infrastructure, transportation, utilities. 20-30-year concession assets.
  Real Estate: $50B — opportunistic and core real estate globally.
  Energy: $30B — midstream, renewable power generation.
  Arctos (newly acquired): sports franchise ownership + solutions platform;
  building toward $100B AUM vertical in sports/entertainment.

WHY FRE IS THE CROWN JEWEL: THE LOCKED-UP CAPITAL ENGINE
──────────────────────────────────────────────────────────
Management fees (FRE) are calculated on committed capital in closed-end funds.
A PE fund with $20B committed capital earns ~1.5% management fees annually =
$300M/year for the life of the fund (~10 years), regardless of market conditions.
Investors CANNOT redeem. In 2008-2009, KKR's management fees continued flowing.

FY2025 FRE: $4.13/share (+13% YoY) → growing annually as AUM scales
Q1 2026 FRE: $1.13/share (+23% YoY) → growth accelerating

At $94 (current price), the market is paying just $94 - $63 (EPP) = $31/share for
ALL realizations over the next 10+ years — essentially for free. Given $120B dry
powder that will be deployed and eventually realized at 2× or more returns, the
embedded value of future carry is substantial.

THE $120B DRY POWDER: THE COMPRESSED SPRING
─────────────────────────────────────────────
KKR has $120B of dry powder (capital committed by LPs, not yet deployed). This
represents 10-12 months of typical deployment pace. Once macro uncertainty
clears (tariffs resolved, rate direction clearer), KKR DEPLOYS this capital
into deals → investments appreciate → exits happen → carry realizations spike.

The cycle timeline:
  Deploy → Hold 5-7 years → Exit → Carry realization
KKR deployed $95B in FY2025. At typical 2-2.5× return multiples, these
investments will generate $95-142B of exits in 5-7 years → massive carry.

FY2026 REALIZATION CYCLE: THE TRIGGER
───────────────────────────────────────
FY2022-2024: PE deal market was frozen (rising rates → compressed buyout multiples →
sellers wouldn't accept lower prices → deal volumes fell 40-50%). Carry dried up.
FY2025: Slow improvement; FRE grew to $4.13 but realizations muted → ANI only $4.87
FY2026E: Deal market beginning to thaw. Rate stability + maturing portfolio vintages
from 2018-2021 are ready for exit → analysts model $6.77 ATDE (+39% from $4.87).
Management targets "$7+" — the realization cycle is turning.

GLOBAL ATLANTIC: THE INSURANCE MOAT
──────────────────────────────────────
The $219B insurance AUM through Global Atlantic is KKR's most underappreciated asset:
  1. PERMANENT CAPITAL: Insurance liabilities don't redeem. GA's policyholder base
     grows as people buy annuities — $30B+ in new policy premiums annually.
  2. FRE GROWTH DRIVER: As GA grows from $219B toward $300B+ AUM, KKR earns
     perpetual management fees on every dollar. This is pure FRE — no carry risk.
  3. INVESTMENT SPREAD: KKR manages GA's assets (structured credit, CLOs, ABF)
     at higher yields than vanilla insurers → GA earns above-average spreads.
  4. INSURANCE INDUSTRY TRANSFORMATION: Industry-wide shift to private credit for
     insurance investment portfolios. KKR is at the forefront → industry tailwind.

RECORD FUNDRAISING: THE FOUNDATION IS GETTING STRONGER
────────────────────────────────────────────────────────
  FY2025 capital raised:   $129B   (record; nearly 2× vs. two years prior)
  FY2025 capital deployed:  $95B   (deals made at attractive entry prices)
  80%+ of $300B 2024-2026 fundraising target achieved in just FY2024-2025
  FPAUM: $615B (+17% YoY) — every dollar of new FPAUM = ~$9-10/yr of management fees

  New KKR flagship PE fund raising in 2026 — targeting $20B+ for Americas Fund XIV.
  Every billion raised at 1.5% fee = $15M/yr more FRE for 10 years.

Q1 2026 RESULTS — STRONG BUT STORY IS ABOUT WHAT'S COMING
───────────────────────────────────────────────────────────
  ATDE per share:    $1.39  (+20% YoY; $1.39 × 4 = $5.56 annualized run rate)
  FRE per share:     $1.13  (+23% YoY; record; continuing momentum)
  TOE per share:     $1.47  (+18% YoY)
  AUM:               $758B  (+14% YoY; RECORD)
  FPAUM:             $615B  (+17% YoY; RECORD)
  New capital raised: $28B  (fundraising momentum intact)

  Management maintains "$7+" ATDE guidance for FY2026. H2 2026 realizations
  from the thawing deal market are the key variable.

VALUATION DISLOCATION: 39% BELOW 52-WEEK HIGH
───────────────────────────────────────────────
At $94.19:
  FW P/E on FY2026E $6.77:    13.9×  (vs. historical 20-30× for growing alt managers)
  FW P/E on FY2027E $8.13:    11.6×  (extraordinarily cheap on 2-yr view)
  Dividend yield:               0.83% ($0.78 / $94.19; 7th consecutive annual increase)
  Market cap / AUM:             11.2% ($85B market cap / $758B AUM — "almost free" AUM)

For context: at the 52-week high of $153.87 (Nov 2025), KKR traded at ~22× FY2026E.
At $94.19 today = 13.9×. The business is materially stronger than 6 months ago
(AUM up 14%, FPAUM up 17%), yet the stock is 39% cheaper.

PEER COMPARISON (alt asset managers, all sold off significantly)
──────────────────────────────────────────────────────────────
  Blackstone (BX):    ~$119; 15× FY2026E; ◎ ACCUMULATE in our model
  KKR:                ~$94;  13.9× FY2026E; ◉ BUY (more compelling entry)
  Apollo Global (APO):  ~similar to KKR; also deeply discounted
  Ares Management (ARES): credit-focused; more defensive; less discounted

  KKR's deeper discount vs. BX is partly explained by KKR's higher PE exposure
  (more realization-sensitive) vs. BX's larger credit/real estate base. But at
  13.9× vs. BX at 15×, the gap is too wide — KKR's Global Atlantic provides
  comparable non-cyclical FRE support.

KEY RISKS
──────────
  1. DEAL MARKET FREEZE: If tariffs/trade war escalates, PE deal activity could
     remain depressed → carry realizations disappoint → ATDE stays near $5-6 rather
     than consensus $7-8. FRE still grows but stock re-rates lower.
  2. MULTIPLE CONTRACTION: Alt manager multiples compressed 40-50% from 2024 peaks.
     If macro deteriorates further, multiples could compress more before recovering.
  3. CREDIT CYCLE RISK: $285B+ in credit/private credit AUM is subject to defaults
     in a recession. GA's insurance spread could compress if credit losses spike.
  4. KEY-MAN RISK: Kravis/Roberts co-chairmen but age 80+. Scott Nuttall (CEO since
     2021) capable successor, but cultural transitions create uncertainty.
  5. LEVERAGE: KKR's portfolio companies use LBO leverage. Rate shock could stress
     portfolio, delay exits, compress valuations.

SUMMARY VERDICT
───────────────
KKR is trading at 11.6× FY2027E consensus ATDE — the multiple applied to a company
WHEN IT'S IN DISTRESS — while every business metric is at ALL-TIME HIGHS ($758B AUM,
$615B FPAUM, $129B raised, $120B dry powder). This is the classic alt-asset-manager
setup: the deal market cycle creates near-term realization uncertainty, and the market
extrapolates the trough into perpetuity. The FRE floor ($4.13/share growing 23% YoY)
is secured by locked-up capital. Global Atlantic's $219B insurance AUM is perpetual.
At $94.19, the market is essentially giving away all future carry for free above the
FRE floor. Deep BUY. Target: $130-179 over 2 years.
""")

    print("KEY METRICS")
    print(f"  Current price (fetched)          = $  {CURRENT_PRICE:.2f}")
    print(f"  52-week range                    = $82.67 – $153.87")
    print(f"  Market cap                       = ~$85.3B")
    print(f"  FW P/E on FY2026E ${EPS_NOW:.2f}        = {CURRENT_PRICE/EPS_NOW:.1f}×  (vs historical 20-30×; distressed pricing)")
    print(f"  FW P/E on FY2027E ${CONS_EPS_2YR:.2f}        = {CURRENT_PRICE/CONS_EPS_2YR:.1f}×  (extraordinary 2-yr view)")
    print(f"  Dividend (annual)                = ${DIVIDEND_ANN:.2f}  (yield {DIVIDEND_ANN/CURRENT_PRICE*100:.2f}%; 7th consecutive annual increase)")
    print(f"  AUM (Q1 2026, record)            = $758B  (+14% YoY; all-time high)")
    print(f"  Fee-paying AUM (FPAUM)           = $615B  (+17% YoY; locked-up; recurring fees)")
    print(f"  Dry powder                       = $120B  (committed, undeployed; carry compressed spring)")
    print(f"  FRE per share FY2025             = $4.13  (+13% YoY; growing 23% in Q1 2026)")
    print(f"  Global Atlantic AUM              = $219B  (insurance perpetual capital)")
    print(f"  Capital raised FY2025            = $129B  (record; ~2× vs. 2 years prior)")
    print(f"  Analyst avg price target         = ~$141-148  (+50-57% from current)")
    print()

    print("AFTER-TAX DISTRIBUTABLE EARNINGS (ATDE) HISTORY")
    for yr, val in EPS_HISTORY.items():
        print(f"  {yr}  ${val:.2f}")
    print(f"  FY2026E ${EPS_NOW:.2f}  (NTM run rate; Q1 annualized; H2 realizations to add)")
    print(f"  FY2026E ${6.77:.2f}  (analyst consensus; management guides $7+)")
    print(f"  FY2022–FY2025 CAGR: {((EPS_HISTORY['FY2025']/EPS_HISTORY['FY2022'])**(1/3)-1)*100:.1f}%/yr  (muted by FY2023 deal-market freeze; FRE growing 20%+)")
    print()

    print("EPP CALCULATION")
    print(f"  EPS_TROUGH × EPP_MIN_PE  =  ${EPS_TROUGH:.2f} × {EPP_MIN_PE}×  =  ${EPP:.2f}")
    print(f"  (FRE floor on locked-up capital; severe bear; realizations = $0; 18× same as BX)")
    print()

    print("METHOD B  (2-year forward)")
    print(f"  CONS_EPS_2YR × CONS_EXIT_PE  =  ${CONS_EPS_2YR:.2f} × {CONS_EXIT_PE}×  =  ${price_b:.2f}")
    print()

    print("RATIO B  (PRIMARY SIGNAL)")
    print(f"  (${CURRENT_PRICE:.2f} − ${EPP:.2f}) / (${price_b:.2f} − ${CURRENT_PRICE:.2f})")
    print(f"  = ${CURRENT_PRICE - EPP:.2f} / ${price_b - CURRENT_PRICE:.2f}")
    print(f"  = {ratio_b:.3f}×   →   {signal}")
    print(f"  EPP gap: +{epp_gap_pct:.1f}% above structural floor")
    print()

    print("SCENARIO PRICES")
    for name, price in scenarios.items():
        print(f"  {name:<8} ${price:>7.2f}   ", end="")
        if name == "BEAR":
            print("EPP floor; deal market collapses; realizations = $0; FRE-only earnings")
        elif name == "BASE":
            print("FY2026E $6.77 × 19×; deal market thaw; partial re-rating; consensus PT zone")
        elif name == "BULL":
            print("Method B; FY2027E $8.13 × 22×; normalized multiple recovery")
        else:
            print("FY2027E $8.13 × 30×; deal boom; peak cycle; full growth premium re-rate")
    print()

    print("SOFTMAX COMPOSITE ENGINE")
    print(f"  Market composite (inferred)  =  {market_composite:.3f}")
    print(f"  (Market near pure BEAR zone — pricing deal-market distress, ignoring $120B dry powder)")
    print()

    print("SCA — SIGNAL CATALYST ADJUSTMENTS")
    for desc, score, weight in sca_items:
        trunc = desc[:55]
        sign  = "+" if score >= 0 else ""
        print(f"  {trunc:<55}  {sign}{score:.2f} × {weight:.2f}  =  {'+' if score*weight>=0 else ''}{score*weight:.4f}")
    print()
    print(f"  sca_raw     =  {'+' if sca_raw>=0 else ''}{sca_raw:.4f}")
    print(f"  sca_adj     =  {'+' if sca_adj>=0 else ''}{sca_adj:.4f}  (= sca_raw / 2.0)")
    print(f"  adj_composite  =  {market_composite:.3f}  +  {sca_adj:.4f}  =  {adj_composite:.3f}")
    print()

    print("SOFTMAX SCENARIO WEIGHTS  (at adj_composite = {:.3f})".format(adj_composite))
    for name, w in adj_weights.items():
        print(f"  {name:<8}  {w*100:5.1f}%   ${scenarios[name]:.2f}")
    print()
    print(f"  Expected price (probability-weighted)  =  ${expected_px:.2f}")
    print()

    print("BUSINESS METRICS")
    print(f"  AUM total (Q1 2026)            = $758B  (RECORD; +14% YoY; all strategy highs)")
    print(f"  Fee-paying AUM                 = $615B  (+17% YoY; locked up; cannot redeem)")
    print(f"  Dry powder                     = $120B  (committed capital awaiting deployment)")
    print(f"  FY2025 capital raised          = $129B  (RECORD; 80%+ of $300B 2024-26 target)")
    print(f"  FY2025 capital deployed        = $95B   (deployed at attractive post-rate-reset prices)")
    print(f"  Global Atlantic AUM            = $219B  (perpetual insurance capital; growing ~15%/yr)")
    print(f"  Q1 2026 FRE per share          = $1.13  (+23% YoY; recurring floor)")
    print(f"  Q1 2026 ATDE per share         = $1.39  (+20% YoY; annualized $5.56)")
    print(f"  Market cap / AUM               = 11.2%  ($85B / $758B — extraordinarily low ratio)")
    print()

    print("SIGNAL ENTRY GUIDE")
    def threshold_price(rb):
        return (EPP + rb * price_b) / (1 + rb)
    p_buy   = threshold_price(0.75)
    p_watch = threshold_price(1.10)
    p_hold  = threshold_price(1.75)
    p_avoid = threshold_price(2.50)
    print(f"  ✕ AVOID      above  ${p_avoid:.0f}  (ratio_b > 2.50×; 52-wk high $153.87 = deep AVOID at 3.62×)")
    print(f"  ▷ HOLD/TRIM  ${p_hold:.0f} – ${p_avoid:.0f}  (ratio_b 1.75–2.50×)")
    print(f"  ◐ WATCHLIST  ${p_watch:.0f} – ${p_hold:.0f}  (ratio_b 1.10–1.75×; analyst avg PT $141-148 = HOLD/WATCHLIST)")
    print(f"  ◎ ACCUMULATE ${p_buy:.0f} – ${p_watch:.0f}  (ratio_b 0.75–1.10×)")
    print(f"  ◉ BUY        below  ${p_buy:.0f}  (ratio_b < 0.75×)  ← current ${CURRENT_PRICE:.2f}  BUY")
    print()
    print(f"  52-wk low $82.67 = deep BUY (ratio_b 0.20×); tariff panic low.")
    print(f"  52-wk high $153.87 = deep AVOID (ratio_b 3.62×) — stock peaked at ~22× FY2026E.")
    print(f"  Analyst avg PT $141-148 = HOLD/TRIM zone — conservative; doesn't model peak cycle.")
    print(f"  BUY to BULL ($179) = +90%; BUY to BASE ($130) = +38%.")
    print(f"  Key watch: H2 2026 PE realizations (exits/IPOs); Global Atlantic AUM growth;")
    print(f"  FRE per share Q2 2026 (23% trend); new Americas Fund XIV fundraise close.")
    print(f"  Market cap/AUM 11.2% is historically anomalous — BX at trough was 12-15%; KKR cheaper.")
