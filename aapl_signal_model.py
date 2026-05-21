#!/usr/bin/env python3
"""
AAPL  ·  Apple Inc.
BottomUp Risk/Reward Analyzer  —  three-part publication format

Part 1  FRAMEWORK LOGIC     what each concept means (reusable)
Part 2  AAPL CASE           narrative per section, only what matters
Part 3  NUMBERS & SIGNALS   pure data, no prose

Price: $302.25  (Yahoo Finance / WebSearch, 2026-05-21)
"""
import math

# ══════════════════════════════════════════════════════════════════════════════
# INPUTS
# ══════════════════════════════════════════════════════════════════════════════
TICKER        = "AAPL"
COMPANY       = "Apple Inc."
SECTOR        = "Consumer Technology · Hardware & Software Ecosystem"
DATE          = "2026-05-21"
CURRENT_PRICE = 302.25     # Yahoo Finance / WebSearch 2026-05-21

EPS_TROUGH_YEAR  = 2022
EPS_TROUGH       = 6.11     # FY2022 GAAP diluted EPS (ended Sep 24, 2022)
EPS_TROUGH_PRICE = 124.17   # Jan 3, 2023 closing low; $6.11 × 20x = $122.20 ≈ $124 ✓
EPS_NOW          = 7.47     # FY2025 GAAP diluted EPS (ended Sep 27, 2025)
EPS_FWD_CONSENSUS = 8.55    # FY2026E (~14.3% growth; consensus from Wall Street analysts)

EPP_MIN_PE      = 20.0      # iOS ecosystem floor: $6.11 × 20 = $122.20 ≈ $124.17 actual low ✓
CONS_EPS_CAGR   = 0.10      # 10%/yr conservative (consensus ~9-10%/yr medium term)
CONS_EXIT_PE    = 25.0      # removes AI premium; quality consumer-tech ex-intelligence option
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

SCENARIOS = [
    # lbl, narrative, eps, pe, price
    ("BEAR",  "China collapses; App Store forced open; EPS contracts",  7.20, 18,  130),
    ("BASE",  "Consensus execution; steady services; no AI premium",    9.30, 24,  223),
    ("BULL",  "AI Intelligence upgrade cycle; Services re-accelerate", 11.50, 30,  345),
    ("XBULL", "Platform dominance; AI agents; new device categories",  14.00, 38,  532),
]

CROSS_READS = [
    # name, what_it_tells_us, unit, bear_ceil, base_lo, bull_lo, xbull_lo, current, weight
    ("iPhone global shipments YoY",       "Demand signal; upgrade cycle health",   "% YoY",  -3, -3,  3, 10,   5, 0.30),
    ("App Store + Services revenue YoY",  "High-margin flywheel acceleration",     "% YoY",   5,  5, 12, 20,  16, 0.25),
    ("China iPhone market share",         "Geopolitical + competitive exposure",   "%",       12, 12, 17, 22,  15, 0.20),
    ("Apple blended gross margin",        "Services mix shift + cost efficiency",  "%",       43, 43, 46, 48,  47, 0.15),
    ("US consumer electronics spend YoY", "Macro demand for premium hardware",     "% YoY",  -5, -5,  3, 10,   7, 0.05),
    ("Services gross margin",             "App Store / iCloud monetisation depth", "%",       70, 70, 73, 76, 76.7, 0.05),
]

STRUCTURAL_FACTORS = [
    ("iOS ecosystem switching costs  (App library; iMessage; iCloud lock-in)",  +1.5, 0.25),
    ("Services margin flywheel  (App Store monopoly; ~75% gross margin)",        +1.0, 0.20),
    ("China revenue concentration risk  (Huawei resurgence; tariff exposure)",  -1.2, 0.20),
    ("AI competitive gap  (Siri vs ChatGPT; monetisation path unclear)",         -0.5, 0.20),
    ("Regulatory headwinds  (EU DMA App Store; DOJ antitrust)",                  -0.8, 0.15),
]

EPS_DECOMP = [
    ("Services mix shift  (App Store → iCloud → subscription revenue)",  0.35, True),
    ("Share buybacks  (massive capital return ~$85-90B/yr)",             0.25, True),
    ("Gross margin expansion  (product mix + cost efficiency)",          0.20, True),
    ("Operating leverage  (R&D / SG&A fixed vs revenue growth)",        0.10, True),
    ("iPhone ASP & hardware pricing power  (brand premium; Pro mix)",   0.08, True),
    ("Foreign exchange  (net multi-year headwind; cyclical drag)",       0.02, False),
]

# ── IDIOSYNCRATIC ASSESSMENT ──────────────────────────────────────────────────
IDIO = {
    "idio_pct": 50,
    "macro_pct": 50,
    "beta": 1.20,
    "drivers": [
        ("iOS ecosystem execution",           "IDIO",  0.20, "App Store; services bundle; lock-in"),
        ("Apple Intelligence / AI adoption",  "IDIO",  0.15, "Feature adoption; monetisation path"),
        ("China revenue management",          "IDIO",  0.15, "Huawei defense; India diversification"),
        ("Consumer confidence & spend cycle", "MACRO", 0.20, "Premium hardware demand; GDP-linked"),
        ("Tech sentiment + rate environment", "MACRO", 0.15, "Nasdaq beta 1.20; multiple sensitivity"),
        ("Tariff / geopolitical exposure",    "MACRO", 0.15, "US-China trade; supply chain tariffs"),
    ],
    "note": (
        "Apple sits at the intersection of idiosyncratic and macro. The iOS ecosystem — "
        "2.2B active devices, App Store, iMessage, iCloud — is among the deepest switching-"
        "cost moats in equity markets. The Services flywheel is genuinely idiosyncratic: "
        "no macro event switches 1B users off their iPhone overnight. But Apple also carries "
        "1.20x beta to the Nasdaq, derives ~17% of revenue from China (with Huawei resurgent "
        "and tariff risk elevated), and sells a premium consumer device that cycles with "
        "disposable income. The EPP floor ($149) is almost entirely idiosyncratic — Services "
        "recurring revenue survives a recession. But the $153 premium above floor (102%) "
        "requires both AI Intelligence to drive an upgrade supercycle (idio) AND consumers "
        "to keep buying $1,200 phones through a potential slowdown (macro)."
    ),
}

# ══════════════════════════════════════════════════════════════════════════════
# ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def score_cr(val, base_lo, bull_lo, xbull_lo):
    if val >= xbull_lo: return 4
    if val >= bull_lo:  return 3
    if val >= base_lo:  return 2
    return 1

SLABEL = {4: "XBULL ★★", 3: "BULL  ▲ ", 2: "BASE  ◦ ", 1: "BEAR  ⚠ "}
SBAR   = {4: "████", 3: "███░", 2: "██░░", 1: "█░░░"}

scored = [(name, desc, unit, bc, blo, bulo, xlo, cur, w, score_cr(cur, blo, bulo, xlo))
          for (name, desc, unit, bc, blo, bulo, xlo, cur, w) in CROSS_READS]

proxy_composite = sum(sc * w for *_, sc, w in scored)
sca             = sum(s * w for _, s, w in STRUCTURAL_FACTORS)
adj_composite   = proxy_composite + sca

sc_map = {lbl: (narr, eps, pe, price) for lbl, narr, eps, pe, price in SCENARIOS}

def softmax(c, T=0.60):
    centres = {"BEAR": 1.25, "BASE": 2.0, "BULL": 2.75, "XBULL": 3.75}
    raw = {k: math.exp(-abs(c - v) / T) for k, v in centres.items()}
    tot = sum(raw.values())
    return {k: v / tot for k, v in raw.items()}

def ev(probs): return sum(probs[k] * sc_map[k][3] for k in probs)

proxy_probs = softmax(proxy_composite)
mkt_target  = CURRENT_PRICE * (1 + REQUIRED_RETURN) ** HORIZON_YEARS

def solve_market(target, tol=5.0):
    for c in [x/100 for x in range(100, 401)]:
        if abs(ev(softmax(c)) - target) < tol:
            return round(c, 2), softmax(c)
    return None, {}

mkt_comp, mkt_probs = solve_market(mkt_target)
mkt_ev = ev(mkt_probs) if mkt_probs else mkt_target
proxy_ev = ev(proxy_probs)

epp_now        = EPS_NOW * EPP_MIN_PE
epp_trough_val = EPS_TROUGH * EPP_MIN_PE
epp_gap_pct    = (CURRENT_PRICE - epp_now) / epp_now * 100
bear_vs_epp    = (sc_map["BEAR"][3] - epp_now) / epp_now * 100

trailing_pe = CURRENT_PRICE / EPS_NOW
forward_pe  = CURRENT_PRICE / EPS_FWD_CONSENSUS

cons_eps_2yr   = EPS_NOW * (1 + CONS_EPS_CAGR) ** 2
cons_price_2yr = cons_eps_2yr * CONS_EXIT_PE
cons_ret_ann   = (cons_price_2yr - CURRENT_PRICE) / CURRENT_PRICE / 2 * 100

dist_epp  = CURRENT_PRICE - epp_now
price_A   = CURRENT_PRICE * (cons_eps_2yr / EPS_NOW)
price_B   = cons_eps_2yr * CONS_EXIT_PE
price_C   = sc_map["BASE"][3]

upside_A  = price_A - CURRENT_PRICE
upside_B  = price_B - CURRENT_PRICE
upside_C  = price_C - CURRENT_PRICE

ratio_A = dist_epp / upside_A if upside_A > 0 else float('inf')
ratio_B = dist_epp / upside_B if upside_B > 0 else float('inf')
ratio_C = dist_epp / upside_C if upside_C > 0 else float('inf')

def rlabel(r):
    if r == float('inf') or r < 0: return "✕ AVOID"
    if r < 0.75:  return "◉ BUY"
    if r < 1.10:  return "◎ ACCUMULATE"
    if r < 1.75:  return "◐ WATCHLIST"
    if r < 2.50:  return "○ HOLD / TRIM"
    return              "✕ AVOID"

def rfmt(r):
    return f"{r:.2f}x" if r != float('inf') else "N/A"

SIGNAL  = rlabel(ratio_B)
adj_gap = adj_composite - mkt_comp if mkt_comp else 0

vol_pct = 0.26
sigma   = CURRENT_PRICE * vol_pct

# EPS decomp (real/structural engine)
eps_g_total     = EPS_NOW - EPS_TROUGH
cyclical_dollar = sum(EPS_TROUGH * sh for _, sh, is_s in EPS_DECOMP if not is_s)
struct_dollar   = eps_g_total - cyclical_dollar


# ══════════════════════════════════════════════════════════════════════════════
# OUTPUT  —  three-part publication format
# ══════════════════════════════════════════════════════════════════════════════
W  = 74
HL = "=" * W
ML = "-" * W
SL = "  " + "-" * 62

def section(title, subtitle=""):
    print()
    print(HL)
    print(f"  {title}")
    if subtitle:
        print(f"  {subtitle}")
    print(HL)

def sub(title):
    print()
    print(f"  {title.upper()}")
    print("  " + "-" * len(title))

def p(text):
    for line in text.strip().split("\n"):
        print(f"  {line.strip()}" if line.strip() else "")
    print()

# ─────────────────────────────────────────────────────────────────────────────
# PART 1  —  HOW THIS SIGNAL WORKS
# ─────────────────────────────────────────────────────────────────────────────
section("PART 1  ·  HOW THIS SIGNAL WORKS",
        "A guide to reading every analysis published here")

sub("The central question")
p("""
Every analysis starts with the same question: at the current price,
is the upside from earnings growth worth the risk of being wrong?
We answer it with three building blocks — the floor, the growth check,
and the cross-read — then combine them into a single ratio and signal.
""")

sub("EPP — the floor")
p(f"""
EPP (Earnings Power Price) is the lowest price rational capital will
accept for a business based on what it earns today.

    EPP  =  current normalized EPS  ×  min-viable trough P/E

The trough P/E is not a forecast — it is the floor multiple the market
has actually assigned this business at its worst moments in history.
It captures franchise quality: a monopoly with captive recurring revenue
never trades at the same trough multiple as a cyclical manufacturer.

When price = EPP, you are buying at the floor.
When price > EPP, you are paying a premium that EPS growth must earn back.
The floor itself migrates upward as EPS compounds — it does not move
with sentiment or rate cycles.
""")

sub("EPS quality check")
p("""
Not all EPS growth is equal. A business inflating earnings through
aggressive pricing or one-time items is not compounding. We decompose
EPS growth into real drivers (volume, operating leverage, mix shift)
versus inflation pass-through (ASP hikes, CPI). A healthy business
should show at least 65-70% real growth. Below 50% and the floor is
softer than it looks.
""")

sub("Cross-read model")
p("""
We track 5-6 external signals that are observable before the company
reports, each mapped to a specific business driver. iPhone shipment
data from Counterpoint tells us about demand and upgrade cycles. App
Store revenue trackers tell us about Services growth momentum. China
smartphone market share tells us how Huawei competition is evolving.

Each signal is scored 1-4 against pre-set thresholds:
  1 = BEAR    conditions consistent with the bear scenario
  2 = BASE    normal growth; thesis intact
  3 = BULL    outperforming; upside scenarios become more likely
  4 = XBULL   exceptional; multiple expansion possible

The weighted composite is compared to the market composite — the score
the current price needs to deliver a 15% hurdle rate. A higher proxy
composite than market composite means the model sees more than the
market is pricing. That gap is where conviction lives.
""")

sub("Structural factors (SCA)")
p("""
Qualitative overlay on top of the numbers. Moats, competitive risks,
and long-run dynamics that do not show up in quarterly data points.
Scored -2 to +2, weighted by importance, added to the composite.
A business with a deep switching-cost moat earns a positive SCA.
A business with a dominant but exposed customer or geography earns
a negative one.
""")

sub("Scenarios")
p("""
Four named outcomes — BEAR / BASE / BULL / XBULL — each with an EPS
assumption, exit multiple, and 2-year price target. Scenario
probabilities are assigned via a softmax distribution centred on the
proxy composite. The market's implied probabilities are back-solved
from the current price. When the model assigns higher probability to
BULL than the market does, the stock is likely mispriced.
""")

sub("Attractiveness ratio")
p("""
The single number that summarises risk/reward.

    Ratio  =  (current price − EPP)  /  (2yr reflated price − current)
           =  downside to floor  /  upside from EPS compounding

  Ratio below 0.75  →  ◉  BUY          Upside dominates the floor gap
  Ratio 0.75 – 1.1  →  ◎  ACCUMULATE   Balanced; edge to upside
  Ratio 1.1 – 1.75  →  ◐  WATCHLIST    Floor gap exceeds EPS upside
  Ratio above 1.75  →  ✕  AVOID        Growth fully priced

We run three methods: A holds the current multiple constant, B applies
a conservative exit multiple (honest stress-test), and C uses the BASE
scenario price. Method B is the primary signal.
""")

sub("Idiosyncratic score")
p("""
How much of the outcome does your stock-picking actually control?
We estimate what fraction of the return profile is driven by
company-specific factors (idiosyncratic) versus macro sentiment,
rate cycles, and broad market moves (macro).

High idiosyncratic means the thesis is right or wrong on its own
merits — fundamental work creates edge. High macro means you also
need to be right on the environment, which is harder to predict.

One rule always holds: the EPP floor is more idiosyncratic than the
premium above it. A stressed macro environment can compress the
multiple — it very rarely destroys a genuine earnings floor.
""")

# ─────────────────────────────────────────────────────────────────────────────
# PART 2  —  AAPL ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
section(f"PART 2  ·  {TICKER}  —  ANALYST COMMENTARY",
        f"{COMPANY}  ·  {SECTOR}  ·  {DATE}  ·  ${CURRENT_PRICE:.2f}")

print(f"""
  ┌{"─"*62}┐
  │  SIGNAL:  {SIGNAL:<20}  (primary: Ratio B {rfmt(ratio_B):<10})         │
  │  EPP floor ${epp_now:.0f}  ·  Gap {epp_gap_pct:+.0f}%  ·  Conservative return {cons_ret_ann:+.0f}%/yr  │
  └{"─"*62}┘""")

sub("1.  The worst EPP — when the floor was touched")
p(f"""
The EPP floor was last touched on January 3, 2023, when AAPL closed
at ${EPS_TROUGH_PRICE:.2f} — the lowest print of the 2022-2023 bear market cycle.
At that point the trailing EPS was ${EPS_TROUGH:.2f} (FY2022, ended Sep 2022).
The implied P/E at the low: ${EPS_TROUGH_PRICE:.2f} / ${EPS_TROUGH:.2f} = {EPS_TROUGH_PRICE/EPS_TROUGH:.1f}x.

The floor multiple for Apple's franchise is 20x. This is not a target —
it is what rational capital has actually paid at Apple's worst moment.
The 20x sits in a specific place in the quality spectrum:
  Regulated software platform:   28-35x trough  (near-guaranteed recurring)
  Apple (iOS ecosystem):         20x trough      (captive + recurring + hardware)
  Premium consumer hardware:     12-15x trough   (hardware cyclicality, no lock-in)
  Mass-market consumer devices:  8-12x trough    (fully commoditised)

Apple earns a 20x floor — not 30x, not 12x — because the business is
genuinely two companies in one: (1) a hardware company that would trade
at 12-15x on its own, and (2) a platform/services company earning $100B+
at 75% gross margins that would command 30x+. The blend of the two, plus
the lock-in the hardware creates for the services, gives 20x.

The validation: ${EPS_TROUGH:.2f} × 20x = ${epp_trough_val:.0f},
closely matching the ${EPS_TROUGH_PRICE:.2f} actual trough. EPP is confirmed.

Compare to ISRG's 40x floor: Apple's 20x is half because (a) 45-50%
of revenue is hardware (more cyclical than surgical robots), (b) Apple
has consumer-spending exposure (phones are premium discretionary),
and (c) China concentrates roughly 17% of revenue. But 20x is still
well above commodity consumer electronics (8-12x) — the Services flywheel
earns the premium over pure hardware peers.
""")

sub("2.  What changed since 2022 — and is it structural?")
p(f"""
EPS has compounded from ${EPS_TROUGH:.2f} to ${EPS_NOW:.2f} — a {(EPS_NOW/EPS_TROUGH-1)*100:.1f}% gain, or
{((EPS_NOW/EPS_TROUGH)**(1/3)-1)*100:.1f}%/yr over three years. FY2025 produced record revenue
of ~$416B, record net income of ~$112B, and gross margin of 46.9%.
The EPP floor migrated from ${epp_trough_val:.0f} to ${epp_now:.0f}. Multiple unchanged at 20x.
Floor moved entirely because earnings compounded.

We decompose the ${eps_g_total:.2f} EPS gain into real versus inflation:

  {struct_dollar/eps_g_total*100:.0f}% real (${struct_dollar:.2f}/shr) — Services mix shift is the
    dominant driver. Services revenue crossed $100B annual run rate in
    FY2025 (from ~$78B in FY2022), with ~75% gross margin versus
    hardware's ~37%. Each dollar of revenue that shifts from hardware
    to services adds ~38 cents of incremental margin. Share buybacks
    contributed materially: Apple returned ~$85-90B/year, reducing
    diluted shares by ~5% over 3 years. Gross margin expansion from
    ~43% to ~47% reflects this mix shift. R&D and SG&A grew slowly
    relative to revenue — classic operating leverage.

  {cyclical_dollar/eps_g_total*100:.0f}% inflation/FX (${cyclical_dollar:.2f}/shr) — foreign exchange
    headwinds. Apple earns ~60% of revenue outside the US; dollar
    strength since 2022 has been a consistent drag. This component
    partially reversed as the dollar softened in 2025.

Verdict: overwhelmingly structural. The Services flywheel is not
reversible — once users are paying for iCloud, Apple Music, Apple TV+,
and App Store ecosystem, churn is very low and ARPUs grow annually.
Buybacks are contractually ongoing ($90B+ annual authorization).

What has changed beyond EPS — and what drives the 40x valuation today:
Apple Intelligence (announced June 2024, shipping with iPhone 16) gave
Apple an AI narrative for the first time. The market is paying for:
(1) a potential AI-driven iPhone upgrade supercycle — 1.4B iPhone users
  upgrading to AI-capable devices over 2-3 years, vs. the normal
  cycle of 3-4 years;
(2) eventual AI monetisation — an "AI Pro" subscription, higher-tier
  iCloud tiers with AI features, or B2B enterprise licensing.
Neither has appeared materially in EPS yet. The gap between trailing
P/E (40x) and EPP floor (20x) is almost entirely this option premium.
""")

sub("3.  How likely is a return below the EPP floor?")
p(f"""
At ${CURRENT_PRICE:.2f}, the stock is ${dist_epp:.0f} ({epp_gap_pct:.0f}%) above the EPP floor of
${epp_now:.0f}. That is the widest EPP gap in this portfolio. For context:
ISRG is 27% above floor, MSFT 44%, WMB 133%, AAPL {epp_gap_pct:.0f}%. The gap
is almost entirely the AI Intelligence option premium.

For the floor to break: EPS would need to decline below ~${EPS_TROUGH:.2f} AND
the market would need to assign less than 20x. That requires all three
of: China revenue collapsing (-30%+), regulatory bodies forcing App
Store fee structures to change materially, and consumer spending
contracting sharply. Our BEAR scenario (EPS ${sc_map['BEAR'][1]:.2f} × 18x = ${sc_map['BEAR'][3]:.0f})
actually does break below the EPP floor of ${epp_now:.0f} by
${abs(sc_map['BEAR'][3] - epp_now):.0f} ({abs(bear_vs_epp):.0f}%). This is the only stock in the
portfolio where the BEAR scenario breaches the floor — and it requires
both earnings contraction AND multiple compression simultaneously.

The floor-breach risk is low precisely because the Services revenue is
not EPS-volatile in the way hardware or commodities are. App Store
revenue does not drop 30% in a recession; iCloud subscribers do not
cancel en masse. The real risk is not the floor breaking — it is the
{epp_gap_pct:.0f}% premium above the floor eroding as:
(1) Apple Intelligence fails to drive meaningful upgrade volumes — the
  AI feature set is currently free and has no obvious monetisation path;
(2) China market share continues declining to 12-13% as Huawei's
  Mate-series phones erode Apple's premium positioning in its second-
  largest market;
(3) macro slowdown compresses premium consumer spending, slowing both
  iPhone volumes and Services ARPU growth.

Our model: {proxy_probs['BEAR']*100:.0f}% BEAR probability.
Market implies {mkt_probs.get('BEAR', 0)*100:.0f}%. The floor-break risk
is genuinely low. The AVOID signal is not about the floor — it is about
the {epp_gap_pct:.0f}% of current price that sits above the floor needing
the AI supercycle to materialise just to break even on a conservative
25x exit. At ${CURRENT_PRICE:.2f} and {trailing_pe:.0f}x trailing EPS, there is
essentially no margin of safety.
""")

sub("4.  Cross-read model — observable score vs market-implied score")
p(f"""
Six signals are tracked and scored 1–4 before each quarter report.
The weighted composite tells us what the observable environment is
consistent with. We back-solve the score embedded in the current price.

  Signal                               Score (1-4)  Weight  Current reading
  iPhone global shipments YoY          BULL  (3/4)    30%   +5%   — above +3% BULL threshold
  App Store + Services revenue YoY     BULL  (3/4)    25%   +16%  — in BULL 12-20% range
  China iPhone market share            BASE  (2/4)    20%   15%   — in BASE 12-17% range
  Apple blended gross margin           BULL  (3/4)    15%   47%   — in BULL 46-48% range
  US consumer electronics spend YoY   BULL  (3/4)     5%   +7%   — above +3% BULL threshold
  Services gross margin                XBULL (4/4)     5%   76.7% — above 76% XBULL threshold

Raw proxy composite:     {proxy_composite:.2f} / 4.00
Structural adj (SCA):   {sca:+.2f}  (ecosystem moats offset by China + regulatory risks)
Adjusted composite:      {adj_composite:.2f} / 4.00

Market-implied composite: {mkt_comp:.2f}  — the score embedded in ${CURRENT_PRICE:.2f} at 15%/yr

Gap: {adj_gap:+.2f} composite points.

Unlike WMB (where all six signals were BULL), AAPL has a split picture:
Services is performing exceptionally (BULL/XBULL), hardware demand is
healthy (BULL), but China remains the drag — BASE at 15% market share
with 20% weight holds the composite below what the market needs.

The market composite of {mkt_comp:.2f} requires most signals to stay at BULL
for two years AND Apple Intelligence to begin showing upgrade cycle
evidence. Our composite of {adj_composite:.2f} reflects the current picture: strong
Services, decent iPhone demand, but China stubbornly in BASE territory.

The adj_gap of {adj_gap:+.2f} pp means our model prices in {abs(adj_gap):.2f} less
composite strength than the market requires. This is not a huge gap
(unlike MU where the bear case was obvious), but it means there is no
model-based edge to justify initiating at $302.

Watch: China smartphone market share is the swing variable. A recovery
to 17%+ (BULL threshold) driven by India/China manufacturing diplomacy
or new iPhone design iterations would push the composite to 3.0, still
below the market composite of {mkt_comp:.2f}. Apple Intelligence monetisation
(a paid AI tier or B2B licensing deal) would be the catalyst to push
the market composite higher — but until that appears in guidance, it
is not in this model's composite.
""")

sub("5.  How idiosyncratic is this bet? — what your research controls")
p(f"""
AAPL scores {IDIO['idio_pct']}% idiosyncratic — the lowest in this portfolio.
This is not a knock on business quality; it reflects that Apple trades
like a macro instrument. With 1.20x beta, $4.4T market cap, and heavy
institutional ownership, AAPL moves on risk sentiment as much as on
fundamentals. The {IDIO['macro_pct']}% macro exposure is structurally elevated.

THE {IDIO['idio_pct']}% THAT IS YOURS TO GET RIGHT
─────────────────────────────────────
iOS ecosystem execution (20%): Whether Services ARPU continues growing
  (~$25/user/year currently), whether App Store regulations force
  meaningful fee cuts, and whether Apple Intelligence adoption rate
  reaches the levels required for an upgrade supercycle. These are
  researchable through quarterly Services revenue disclosures,
  regulatory docket filings, and App Store analytics providers
  (Sensor Tower, data.ai). This is the core research edge.

Apple Intelligence / AI adoption (15%): Apple Intelligence shipped with
  iPhone 16 (Oct 2024). Tracking: (a) eligible device penetration rate
  (disclosed by Apple), (b) new AI feature release cadence, (c) evidence
  of ARPU lift from AI-adjacent services. A confirmed AI Pro subscription
  announcement at any price point would be the single biggest positive
  catalyst the model does not currently price. This is observable.

China revenue management (15%): Counterpoint Research publishes monthly
  China smartphone market share data. Apple's Mainland China revenue is
  disclosed quarterly. Huawei Mate series sales data is tracked by IDC.
  A sustained recovery toward 18%+ share would change the thesis
  materially. This is the most important idiosyncratic risk factor.

THE {IDIO['macro_pct']}% THAT MACRO CONTROLS
──────────────────────────────
Consumer confidence & spend cycle (20%): The iPhone is a $1,000+
  discretionary purchase despite feeling like a necessity. In a
  genuine consumer recession, upgrade cycles extend from 3-4 years
  to 4-5 years. Consumer sentiment indices and disposable income data
  are not Apple-specific. Being right on iOS does not protect you
  from a 12-month consumer slowdown.

Tech sentiment + rate environment (15%): At 1.20x beta and ~$4.4T
  market cap, AAPL is moved by Nasdaq sentiment and risk-on/off
  cycles as much as by fundamentals. Apple has net cash of ~$50B+
  (after aggressive buybacks), so it is less rate-sensitive than WMB.
  But the P/E multiple it commands (35-40x) is sensitive to the
  discount rate used to value long-duration earnings.

Tariff / geopolitical exposure (15%): ~90% of iPhone assembly is in
  China; Apple has begun diversifying to India and Vietnam. A sudden
  tariff escalation or export restriction affecting Apple's supply
  chain is not forecastable from fundamental research. This is pure
  macro/political risk.

WHAT THIS MEANS FOR POSITION SIZING
The EPP floor (${epp_now:.0f}) is mostly idiosyncratic — Services recurring
revenue and the iOS ecosystem survive any plausible macro scenario.
But ${dist_epp:.0f} (or {epp_gap_pct:.0f}% of the current price) is the AI
Intelligence option premium. That premium requires both the AI upgrade
cycle to materialise (idio, your research can track it) AND the macro
environment to support consumers paying for a new iPhone (not within
your control). The AVOID signal holds until the observable idio
evidence — adoption rates, monetisation announcements, China recovery
— materially improves the cross-read composite.
""")

# ─────────────────────────────────────────────────────────────────────────────
# PART 3  —  DATA TABLES
# ─────────────────────────────────────────────────────────────────────────────
section(f"PART 3  ·  {TICKER}  —  NUMBERS & SIGNALS",
        f"${CURRENT_PRICE:.2f}  ·  {DATE}  ·  Price source: Yahoo Finance")

print(f"""
  ┌{"─"*62}┐
  │  {SIGNAL:<20}  Ratio B {rfmt(ratio_B):<10}  (primary signal)        │
  │  EPP ${epp_now:.0f}  ({epp_gap_pct:+.0f}% gap)  ·  Fwd P/E {forward_pe:.0f}x  ·  Cons. {cons_ret_ann:+.0f}%/yr   │
  │  Idiosyncratic {IDIO['idio_pct']}% / Macro {IDIO['macro_pct']}%  ·  Beta {IDIO['beta']:.2f}                      │
  └{"─"*62}┘""")

# Cross-reads
print(f"""
  CROSS-READ MODEL  (proxy {proxy_composite:.2f} / 4.00  ·  market {mkt_comp:.2f}  ·  gap {adj_gap:+.2f})
{SL}
  {"Signal":<32}  {"Tracks":<28}  {"Now":>5}  Score    Bar""")
print(SL)
for name, desc, unit, bc, blo, bulo, xlo, cur, w, sc in scored:
    u = unit.split()[0]
    val = f"${cur}{u[1:]}" if u.startswith('$') else f"{cur:>4}{u}"
    print(f"  {name:<32}  {desc:<28}  {val:>6}  {SLABEL[sc]}  {SBAR[sc]}")
print(SL)
print(f"  Structural adjustment (SCA):")
for desc, sc, wt in STRUCTURAL_FACTORS:
    print(f"    {sc:+.1f} × {wt*100:.0f}%  {desc}")
print(f"  SCA {sca:+.2f}  →  adj composite {adj_composite:.2f}  →  verdict: AI PREMIUM FULLY PRICED")

# Scenario thresholds
print(f"""
  SCENARIO THRESHOLDS
{SL}
  {"Signal":<32}  {"BEAR<":>6}  {"BASE":>8}  {"BULL":>8}  {"XBULL≥":>8}  {"NOW":>6}""")
print(SL)
for name, desc, unit, bc, blo, bulo, xlo, cur, w, sc in scored:
    u = unit.split()[0]
    def fmt(v): return f"${v}{u[1:]}" if u.startswith('$') else f"{v}{u}"
    print(f"  {name:<32}  {fmt(bc):>6}  {fmt(blo)}-{fmt(bulo):>4}  {fmt(bulo)}-{fmt(xlo):>4}  {fmt(xlo):>6}  {fmt(cur):>6}")

# EPP
print(f"""
  EPP FLOOR  (iOS ecosystem — {EPP_MIN_PE:.0f}x trough multiple)
{SL}
  {"Year":<8}  {"EPS":>6}  {"× Trough P/E":>14}  {"EPP":>7}  {"Actual low":>12}""")
print(SL)
print(f"  {'FY2022':<8}  ${EPS_TROUGH:>5.2f}  {'× 20x':>14}  ${epp_trough_val:>5.0f}  {'$124  ✓':>12}")
print(f"  {'FY2025':<8}  ${EPS_NOW:>5.2f}  {'× 20x':>14}  ${epp_now:>5.0f}  {'—':>12}  ← today's floor")
print(SL)
print(f"  Floor migration +${epp_now - epp_trough_val:.0f} (+{(epp_now/epp_trough_val-1)*100:.0f}%)  — entirely EPS compounding, multiple unchanged")
print(f"  Current ${CURRENT_PRICE:.2f} is {epp_gap_pct:.0f}% above floor  ·  {(CURRENT_PRICE-epp_now)/sigma:.1f}σ to EPP")
print(f"  Bear ${sc_map['BEAR'][3]:.0f} is {bear_vs_epp:.0f}% vs floor  ← BEAR breaks below floor (EPS ${sc_map['BEAR'][1]:.2f})")

# EPS quality
print(f"""
  EPS QUALITY  (FY{EPS_TROUGH_YEAR} ${EPS_TROUGH:.2f} → FY2025 ${EPS_NOW:.2f};  +{(EPS_NOW/EPS_TROUGH-1)*100:.0f}%  ·  CAGR {((EPS_NOW/EPS_TROUGH)**(1/3)-1)*100:.1f}%/yr)
{SL}
  {"Driver":<44}  {"Share":>6}  {"$EPS":>6}  Type""")
print(SL)
for driver, share, is_real in EPS_DECOMP:
    dollar = EPS_TROUGH * share
    tag = "REAL  ✓" if is_real else "INFL. ~"
    print(f"  {driver:<44}  {share*100:>5.0f}%  ${dollar:>4.2f}  {tag}")
print(SL)
print(f"  Real {struct_dollar/eps_g_total*100:.0f}%  (${struct_dollar:.2f})     Inflation {cyclical_dollar/eps_g_total*100:.0f}%  (${cyclical_dollar:.2f})")

# Scenarios
print(f"""
  SCENARIOS  (2-year;  May 2026 → May 2028)
{SL}
  {"Scenario":<8}  {"EPS":>7}  {"P/E":>5}  {"Price":>7}  {"Proxy%":>8}  {"Mkt%":>7}  {"Gap":>8}  Narrative""")
print(SL)
for lbl, narr, eps, pe, price in SCENARIOS:
    pp = proxy_probs[lbl]
    mp = mkt_probs.get(lbl, 0)
    print(f"  {lbl:<8}  ${eps:>6.2f}  {pe:>4}x  ${price:>6}  {pp*100:>7.1f}%  {mp*100:>6.1f}%  {(pp-mp)*100:>+7.1f}pp  {narr[:28]}")
print(SL)
print(f"  Proxy EV ${proxy_ev:.0f}  ·  Market needs ${mkt_ev:.0f} to justify ${CURRENT_PRICE:.2f} at {REQUIRED_RETURN*100:.0f}%/yr")
print(f"  BASE (${sc_map['BASE'][3]:.0f}) is {(sc_map['BASE'][3]-CURRENT_PRICE)/CURRENT_PRICE*100:+.0f}% vs today  ←  base case implies loss from current price")

# Attractiveness ratio
print(f"""
  ATTRACTIVENESS RATIO  (downside to EPP ${dist_epp:.0f}  =  {dist_epp/CURRENT_PRICE*100:.0f}% of price)
{SL}
  {"Method":<32}  {"2yr Target":>11}  {"Upside":>8}  {"Ratio":>7}  Signal""")
print(SL)
print(f"  {'A: Same P/E  ({:.1f}x trailing)'.format(trailing_pe):<32}  ${price_A:>9.0f}  {(price_A-CURRENT_PRICE)/CURRENT_PRICE*100:>+7.0f}%  {rfmt(ratio_A):>7}  {rlabel(ratio_A)}")
if upside_B > 0:
    print(f"  {'B: Conserv exit 25x  ← PRIMARY':<32}  ${price_B:>9.0f}  {upside_B/CURRENT_PRICE*100:>+7.0f}%  {rfmt(ratio_B):>7}  {rlabel(ratio_B)}")
else:
    print(f"  {'B: Conserv exit 25x  ← PRIMARY':<32}  ${price_B:>9.0f}  {upside_B/CURRENT_PRICE*100:>+7.0f}%  {'N/A':>7}  ✕ AVOID  (target below current price)")
if upside_C > 0:
    print(f"  {'C: BASE scenario':<32}  ${price_C:>9.0f}  {upside_C/CURRENT_PRICE*100:>+7.0f}%  {rfmt(ratio_C):>7}  {rlabel(ratio_C)}")
else:
    print(f"  {'C: BASE scenario':<32}  ${price_C:>9.0f}  {upside_C/CURRENT_PRICE*100:>+7.0f}%  {'N/A':>7}  ✕ AVOID  (BASE below current price)")

# Idiosyncratic
print(f"""
  IDIOSYNCRATIC SCORE
{SL}
  Idiosyncratic   {IDIO['idio_pct']}%  {"█" * (IDIO['idio_pct'] // 3)}{"░" * (33 - IDIO['idio_pct'] // 3)}
  Macro/sentiment {IDIO['macro_pct']}%  {"█" * (IDIO['macro_pct'] // 3)}{"░" * (33 - IDIO['macro_pct'] // 3)}
  Beta {IDIO['beta']:.2f}
{SL}
  {"Factor":<38}  {"Type":>6}  {"Wt":>5}  Note""")
print(SL)
for factor, kind, wt, desc in IDIO["drivers"]:
    print(f"  {factor:<38}  {kind:>6}  {wt*100:>4.0f}%  {desc[:28]}")

# Entry framework
print(f"""
  ENTRY FRAMEWORK
{SL}
  {"Zone":<20}  {"Price":>14}  {"Ratio B":>9}  Action""")
print(SL)
print(f"  {'◉ EPP floor':<20}  {'$149 – $162':>14}  {'< 0.20x':>9}  Buy aggressively")
print(f"  {'◉ High conv.':<20}  {'$162 – $182':>14}  {'0.20–0.75x':>9}  Build position")
print(f"  {'◎ Accumulate':<20}  {'$182 – $190':>14}  {'0.75–1.1x':>9}  Scale in")
print(f"  {'◐ Watchlist':<20}  {'$190 – $215':>14}  {'1.1–1.75x':>9}  Monitor only")
print(f"  {'✕ Today':<20}  {f'~${CURRENT_PRICE:.0f}':>14}  {'N/A':>9}  Avoid / no initiation")
print(SL)
print(f"  UPGRADE to ◐ WATCHLIST if:   AI Intelligence monetisation announced (paid tier)")
print(f"                               AND price retreats below $215")
print(f"  UPGRADE to ◎ ACCUMULATE if:  China share recovers to 17%+  AND  price < $190")
print(f"  MAINTAIN AVOID while:        BASE scenario (${sc_map['BASE'][3]:.0f}) is below current price")

print()
print(HL)
print(f"  {TICKER}  ·  {SIGNAL}  ·  Ratio B {rfmt(ratio_B)}  ·  EPP ${epp_now:.0f} ({epp_gap_pct:+.0f}%)  ·  Idio {IDIO['idio_pct']}% / Macro {IDIO['macro_pct']}%")
print(HL)
print()
