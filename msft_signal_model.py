#!/usr/bin/env python3
"""
MSFT  ·  Microsoft Corporation
BottomUp Risk/Reward Analyzer  —  three-part publication format

Part 1  FRAMEWORK LOGIC     what each concept means (reusable)
Part 2  MSFT CASE           narrative per section, only what matters
Part 3  NUMBERS & SIGNALS   pure data, no prose

Price: $417.42  (Yahoo Finance / WebSearch, 2026-05-20)
"""
import math

# ══════════════════════════════════════════════════════════════════════════════
# INPUTS
# ══════════════════════════════════════════════════════════════════════════════
TICKER        = "MSFT"
COMPANY       = "Microsoft Corporation"
SECTOR        = "Technology · Cloud / Enterprise Software"
DATE          = "2026-05-20"
CURRENT_PRICE = 417.42    # Yahoo Finance / WebSearch 2026-05-20

EPS_TROUGH_YEAR   = "FY2022"
EPS_TROUGH        = 9.65    # FY2022 non-GAAP (year ended June 2022)
EPS_TROUGH_PRICE  = 213.0   # Jan 2023 52-week low
EPS_NOW           = 13.16   # FY2025 non-GAAP (year ended June 2025)
EPS_Q3_FY2026     = 3.46    # Q3 FY2026 (ended Mar 2026), +13% YoY
EPS_FWD_CONSENSUS = 14.00   # FY2026E consensus non-GAAP

EPP_MIN_PE      = 22.0
CONS_EPS_CAGR   = 0.15
CONS_EXIT_PE    = 30.0
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

SCENARIOS = [
    # label, narrative, eps, pe, price
    ("BEAR",  "Azure <10%; CapEx kills margins; Copilot fails",    11.00, 20,  220),
    ("BASE",  "Azure 25-30%; Copilot 80M seats; steady execution", 17.00, 28,  476),
    ("BULL",  "Azure 30%+; Copilot mainstream; GitHub at scale",   20.00, 33,  660),
    ("XBULL", "Azure #1; Copilot standard; AGI adjacency re-rate", 25.00, 38,  950),
]

CROSS_READS = [
    # name, what_it_tells_us, unit, bear_ceil, base_lo, bull_lo, xbull_lo, current, weight
    ("Azure cloud revenue YoY",       "Cloud market share & AI demand",  "% YoY",    8, 15, 25, 35,   35, 0.25),
    ("M365 Copilot paid seats",       "AI monetization pace",            "M seats",  1,  5, 15, 30,   30, 0.20),
    ("Hyperscaler CapEx YoY",         "AI infrastructure investment",    "% YoY",    5, 10, 30, 60,   77, 0.15),
    ("LinkedIn revenue YoY",          "Enterprise hiring & ad market",   "% YoY",   -2,  5, 12, 20,    8, 0.15),
    ("GitHub Copilot paid subs",      "Developer AI tool adoption",      "M subs", 0.2, 0.5, 1,  2,  1.8, 0.15),
    ("Enterprise software spend YoY", "Broad IT budget health",          "% YoY",    0,  5, 10, 15, 14.7, 0.10),
]

STRUCTURAL_FACTORS = [
    ("Azure enterprise switching cost moat  (M365+Azure bundle)", +1.5, 0.25),
    ("OpenAI co-opetition / API dependency risk",                 -0.8, 0.20),
    ("$65B AI CapEx cycle — margin risk before monetization",     -0.8, 0.20),
    ("Copilot seat ceiling  (enterprise ROI not yet proven)",      -0.6, 0.15),
    ("Regulatory / antitrust pressure  (EU + US)",                -0.5, 0.20),
]

EPS_DECOMP = [
    # (driver, share_of_EPS_TROUGH, is_real)
    ("Azure cloud volume growth",          0.400, True),
    ("M365 commercial seat + ARPU growth", 0.250, True),
    ("Operating leverage / margin",         0.200, True),
    ("Share buyback effect",                0.095, True),
    ("M365 & Azure price increases",        0.035, False),
    ("Cost pass-through / FX tailwind",     0.020, False),
]

IDIO = {
    "idio_pct": 45,
    "macro_pct": 55,
    "beta": 0.90,
    "drivers": [
        ("Azure vs AWS/GCP execution",        "IDIO",  0.20, "Cloud share; pricing; feature velocity"),
        ("Copilot enterprise monetization",    "IDIO",  0.15, "Seat attach rate; enterprise ROI proof"),
        ("OpenAI relationship outcome",        "IDIO",  0.10, "Strategic moat vs competitive liability"),
        ("Enterprise IT spending cycle",       "MACRO", 0.20, "GDP-correlated; CFO budget decisions"),
        ("AI CapEx cycle duration",           "MACRO", 0.15, "Hyperscaler spend; AI winter scenario"),
        ("P/E rate sensitivity  (31x)",       "MACRO", 0.15, "100bp move ≈ 5-7pt P/E = $50-65 price"),
        ("Broad market beta  (0.90x)",        "MACRO", 0.05, "Bellwether; S&P correlated in risk-off"),
    ],
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
bear_composite  = sum(score_cr(bc, blo, bulo, xlo) * w
                      for (_, __, ___, bc, blo, bulo, xlo, cur, w) in CROSS_READS)
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
mkt_ev    = ev(mkt_probs) if mkt_probs else mkt_target
proxy_ev  = ev(proxy_probs)

epp_now        = EPS_NOW * EPP_MIN_PE
epp_trough_val = EPS_TROUGH * EPP_MIN_PE
epp_gap_pct    = (CURRENT_PRICE - epp_now) / epp_now * 100
bear_vs_epp    = (sc_map["BEAR"][3] - epp_now) / epp_now * 100

trailing_pe = CURRENT_PRICE / EPS_NOW
forward_pe  = CURRENT_PRICE / EPS_FWD_CONSENSUS

cons_eps_2yr   = EPS_NOW * (1 + CONS_EPS_CAGR) ** 2
cons_price_2yr = cons_eps_2yr * CONS_EXIT_PE
cons_ret_ann   = (cons_price_2yr - CURRENT_PRICE) / CURRENT_PRICE / 2 * 100

dist_epp = CURRENT_PRICE - epp_now
price_A  = CURRENT_PRICE * (cons_eps_2yr / EPS_NOW)
price_B  = cons_eps_2yr * CONS_EXIT_PE
price_C  = sc_map["BASE"][3]

ratio_A = dist_epp / (price_A - CURRENT_PRICE)
ratio_B = dist_epp / (price_B - CURRENT_PRICE)
ratio_C = dist_epp / (price_C - CURRENT_PRICE)

def rlabel(r):
    if r < 0.75:  return "◉ BUY"
    if r < 1.10:  return "◎ ACCUMULATE"
    if r < 1.75:  return "◐ WATCHLIST"
    if r < 2.50:  return "○ HOLD / TRIM"
    return              "✕ AVOID"

SIGNAL  = rlabel(ratio_B)
adj_gap = adj_composite - mkt_comp if mkt_comp else 0

vol_pct     = 0.25
sigma       = CURRENT_PRICE * vol_pct
eps_g_total = EPS_NOW - EPS_TROUGH
infl_dollar = sum(EPS_TROUGH * sh for _, sh, real in EPS_DECOMP if not real)
real_dollar = eps_g_total - infl_dollar

# ══════════════════════════════════════════════════════════════════════════════
# OUTPUT  —  three-part publication format
# ══════════════════════════════════════════════════════════════════════════════
W  = 74
HL = "=" * W
SL = "  " + "-" * 62

def section(title, subtitle=""):
    print(); print(HL); print(f"  {title}")
    if subtitle: print(f"  {subtitle}")
    print(HL)

def sub(title):
    print(); print(f"  {title.upper()}")
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
p("""
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
reports, each mapped to a specific business driver. Hospital capex data
tells us about equipment demand. Procedure volumes tell us about the
recurring revenue base. A competitor's bookings tell us about market share.

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
# PART 2  —  MSFT ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
section(f"PART 2  ·  {TICKER}  —  ANALYST COMMENTARY",
        f"{COMPANY}  ·  {SECTOR}  ·  {DATE}  ·  ${CURRENT_PRICE:.2f}")

print(f"""
  {chr(9484)}{chr(8212)*62}{chr(9488)}
  {chr(9474)}  SIGNAL:  {SIGNAL:<20}  (primary: Ratio B {ratio_B:.2f}x)        {chr(9474)}
  {chr(9474)}  EPP floor ${epp_now:.0f}  {chr(183)}  Gap {epp_gap_pct:+.0f}%  {chr(183)}  Conservative return {cons_ret_ann:+.0f}%/yr          {chr(9474)}
  {chr(9492)}{chr(8212)*62}{chr(9496)}""")

sub("1.  The worst EPP — when the floor was touched")
p(f"""
MSFT's EPP floor was touched in January 2023, when the stock hit
${EPS_TROUGH_PRICE:.0f} — its lowest in two years. The 2022 Fed rate cycle repriced
every long-duration growth asset simultaneously. Azure grew 27% through
the entire selloff. M365 seats kept growing. EPS beat consensus every
quarter of the decline. The floor was set by valuation compression, not
by any deterioration in the business.

The floor that held at ${EPS_TROUGH_PRICE:.0f} reflects a {EPP_MIN_PE:.0f}x trough P/E. That is
the minimum multiple the market has ever assigned Microsoft's earnings —
and it is worth understanding why it is {EPP_MIN_PE:.0f}x, not 10x, not 40x.

At {EPP_MIN_PE:.0f}x, the market is saying: even at maximum fear, it believes
M365 subscriptions will keep renewing. Office and Teams are embedded in
the daily workflows of 400M+ commercial users. Enterprise agreements run
3-5 years. In a recession, companies lay off people before they cancel
Office. That stickiness — not the growth story, not Azure, not Copilot
— is what the {EPP_MIN_PE:.0f}x trough reflects.

Compare this to ISRG's 40x trough: ISRG is a genuine monopoly in
robotic surgery with no viable competitor. MSFT competes directly with
AWS in cloud and Google in productivity. The lower floor multiple (22x vs
40x) is not a weakness — it is an honest assessment of competitive
position. But 22x is still 2-3x higher than a cyclical manufacturer's
trough, because even an imperfect moat is worth a premium at panic lows.
The market has always believed M365 revenue is structural. At $213 in
January 2023, it was proving that belief even under maximum pressure.
""")

sub("2.  What changed since FY2022 — and is it structural?")
p(f"""
EPS has compounded from ${EPS_TROUGH:.2f} to ${EPS_NOW:.2f} — a {(EPS_NOW/EPS_TROUGH-1)*100:.0f}% gain in three years,
or {((EPS_NOW/EPS_TROUGH)**(1/3)-1)*100:.1f}%/yr. The EPP floor has migrated from ${epp_trough_val:.0f} to ${epp_now:.0f}.
The multiple is unchanged at {EPP_MIN_PE:.0f}x. The floor moved because earnings grew.

This is a slower compounding rate than ISRG's 80% gain over the same
period. The reason is structural: Azure started the period with much
greater scale and could not sustain 50%+ growth indefinitely; the $65B
annual CapEx commitment has been dilutive to near-term EPS growth; and
M365 ARPU growth faces real pressure from Google Workspace. These are
not bugs — they are honest constraints on a mature platform.

We decompose the ${eps_g_total:.2f} EPS gain into real versus inflation:

  {real_dollar/eps_g_total*100:.0f}% real ({real_dollar:.2f}/shr) — Azure volume growth, M365 seat
    expansion and ARPU improvement, operating leverage, and buybacks.
    The installed user base grew; Azure workloads grew; the business
    is physically larger. Stripping inflation entirely, real EPS is
    ${EPS_NOW - infl_dollar:.2f}, implying a real EPP of ${(EPS_NOW - infl_dollar)*EPP_MIN_PE:.0f}.

  {infl_dollar/eps_g_total*100:.0f}% inflation ({infl_dollar:.2f}/shr) — M365 price increases (Microsoft
    raised Commercial plan prices 20% in 2023) and cost pass-through.
    Legitimate in a franchise with pricing power, but less durable
    than volume growth if enterprise budgets tighten.

Verdict: structural, with caveats. The Q3 FY2026 result removed the
biggest caveat: Azure grew +35%, beating consensus of +31% by 4 points.
EPS of ${EPS_Q3_FY2026:.2f} (+13% YoY) confirmed that the CapEx cycle is starting
to monetize — AI workloads are flowing through to revenue.
""")

sub("3.  How likely is a return below the EPP floor?")
p(f"""
At ${CURRENT_PRICE:.2f} the stock is ${dist_epp:.0f} ({epp_gap_pct:.0f}%) above the EPP floor of
${epp_now:.0f}. This is a materially wider gap than ISRG (27%) — MSFT has
priced in significantly more AI premium above its structural floor.

Multiple compression alone (without EPS decline): a full rate-cycle
repeat would bring the stock to ~${epp_now:.0f}, a decline of {epp_gap_pct:.0f}% from
today. The floor would not break; price would converge to it. Unlike
ISRG, where 27% compression gets you to an attractive buy zone, MSFT's
44% compression would be a severe drawdown. This is the cost of buying
a quality business at a wide premium to floor.

EPS decline: the only scenario that breaks the floor is the bear case.
MSFT's bear requires Azure revenue growth to stall below 10% while the
$65B annual CapEx commitment stays in place — crushing operating margins
from today's ~45% toward ~35%. That gives approximately ${sc_map['BEAR'][1]:.0f} EPS,
an EPP floor of ~${sc_map['BEAR'][1]*EPP_MIN_PE:.0f}, and a bear price of
${sc_map['BEAR'][3]:.0f} — which is {bear_vs_epp:.0f}% below the current floor.

This is different from ISRG's floor dynamic. ISRG's bear required a
specific binary event (China ban). MSFT's bear is more of a grinding
scenario: Azure deceleration is gradual, and the CapEx commitment cannot
be easily reversed. Our model assigns {proxy_probs['BEAR']*100:.0f}% probability to BEAR.
The market implies {mkt_probs.get('BEAR',0)*100:.0f}%. The gap is narrow — MSFT's bear
risks (AWS competition, AI ROI uncertainty, CapEx trap) are legitimate,
not just geopolitical fear premiums. The market is appropriately cautious.
""")

sub("4.  Cross-read model — observable score vs market-implied score")
p(f"""
Six signals are tracked and scored 1–4 before each quarter report.
The weighted composite tells us what the observable environment is
consistent with. We back-solve the score embedded in the current price.

  Signal                         Score (1-4)   Weight   Current reading
  Azure cloud revenue YoY        XBULL 4/4      25%    +35%  — at XBULL threshold; AI workloads
  M365 Copilot paid seats        XBULL 4/4      20%    30M   — 7.5% attach on 400M seat base
  Hyperscaler CapEx YoY          XBULL 4/4      15%    +77%  — AI build-out still accelerating
  LinkedIn revenue YoY           BASE  2/4      15%     +8%  — hiring recovery below trend
  GitHub Copilot paid subs       BULL  3/4      15%    1.8M  — approaching 2M XBULL threshold
  Enterprise software spend      BULL  3/4      10%   +14.7% — near top of BASE band

Raw proxy composite:     {proxy_composite:.2f} / 4.00
Structural adj (SCA):   {sca:+.2f}  (switching cost moat; offset by OpenAI risk, CapEx
                  cycle, Copilot ceiling uncertainty, and regulatory pressure)
Adjusted composite:      {adj_composite:.2f} / 4.00

Market-implied composite: {mkt_comp:.2f}  — the score embedded in ${CURRENT_PRICE:.2f} at 15%/yr

Gap: {adj_gap:+.2f} composite points. Our signals price a strong BULL/XBULL
environment. The market prices a cautious BASE/BULL mix. The gap
represents the thesis gap — observable data is significantly stronger
than what the market's required return implies.

There is an important tension here that Part 2 alone cannot resolve:
the cross-read signals are genuinely strong (three XBULL readings), but
the attractiveness ratio (Method B, {ratio_B:.2f}x) says the stock has already
re-rated to price in much of this strength. The signals confirm the
business is firing on all cylinders. The ratio says you are paying for
that fact at current prices.

Watch: GitHub Copilot at 1.8M subs is approaching the 2M XBULL
threshold. If it crosses, it signals that the developer AI monetization
flywheel is opening at scale. Azure sustaining above 30% for two
consecutive quarters would move the BASE scenario significantly closer
to BULL. Either of those would push the composite above 3.5 and make
the thesis more compelling at current prices.
""")

sub("5.  How idiosyncratic is this bet? — what your research controls")
p(f"""
MSFT scores {IDIO['idio_pct']}% idiosyncratic — meaning only {IDIO['idio_pct']} cents of every
dollar of return variance comes from factors you can research and take
a view on. The remaining {IDIO['macro_pct']}% is driven by rates, enterprise IT
budget cycles, and AI sentiment — harder to forecast and less
responsive to fundamental research.

This is a strikingly different profile from ISRG (62% idio / 38% macro).
MSFT is one of the most widely held, most analysed stocks in the world.
At $3.1T market cap and 0.90 beta, it behaves partly like a market
proxy. Fundamental work still creates edge — but the macro backdrop
matters more here than in a pure-play surgical robotics compounder.

THE {IDIO['idio_pct']}% THAT IS YOURS TO GET RIGHT
─────────────────────────────────────
Azure vs AWS/GCP execution (20%): Cloud market share is measurable
  every quarter via Azure revenue growth relative to AWS and GCP.
  The Q3 FY2026 reading (+35% vs AWS +17%) shows MSFT gaining share
  in AI workloads. This is researchable via cloud usage surveys,
  hyperscaler capex commentary, and enterprise CIO surveys.

Copilot monetization pace (15%): The seat attach rate (currently
  7.5% on 400M commercial seats) is the key number. Each additional
  percentage point of attach = ~$1.4B additional ARR. At 15% attach
  (BULL scenario), Copilot alone adds ~$10B ARR. Enterprise surveys
  and channel checks can track ROI perception ahead of reported numbers.

OpenAI relationship outcome (10%): Microsoft's $13B investment in
  OpenAI is either the most valuable strategic asset in tech (if OpenAI
  models remain the best and MSFT has exclusive commercial rights) or
  a liability (if OpenAI builds competing products). This is binary
  and researchable via OpenAI product announcements and API pricing.

THE {IDIO['macro_pct']}% THAT MACRO CONTROLS
──────────────────────────────
Enterprise IT spending cycle (20%): MSFT's renewal cycles are
  3-5 years, which smooths short-term volatility — but in a genuine
  recession, enterprises defer upgrades and renegotiate contracts.
  This is GDP-correlated. Being right on Azure and Copilot does not
  protect you if enterprise IT budgets freeze.

AI CapEx cycle duration (15%): The $77% hyperscaler CapEx growth
  is a macro sentiment driver as much as an MSFT-specific one. If
  the market decides AI infrastructure spend is not monetizing fast
  enough, CapEx could reverse industry-wide. MSFT's $65B commitment
  would then look like a liability, not an asset.

Rate/multiple sensitivity (15%): At {trailing_pe:.0f}x trailing P/E, a 100bp
  move in the 10-year yield compresses the multiple by ~5-7 points —
  a $50-65 price impact with zero change in fundamentals. This is
  pure macro exposure that no fundamental work eliminates.

Market beta (5%): At 0.90 beta, MSFT tracks the S&P in risk-off
  episodes. Slightly below market — the recurring revenue base
  provides modest defensiveness — but not enough to matter.

WHAT THIS MEANS FOR POSITION SIZING
The EPP floor (${epp_now:.0f}) is mostly idiosyncratic — anchored to M365
recurring earnings, not sentiment. But the ${dist_epp:.0f} premium above that
floor is almost entirely macro-sensitive. At {epp_gap_pct:.0f}% above floor, you
need both the AI thesis to work AND a benign macro environment. This is
why the primary signal is WATCHLIST, not ACCUMULATE. The business is
exceptional. The price is full. The 55% macro component is doing the
heavy lifting at current levels, and that is not a bet fundamental
research can hedge.
""")

# ─────────────────────────────────────────────────────────────────────────────
# PART 3  —  DATA TABLES
# ─────────────────────────────────────────────────────────────────────────────
section(f"PART 3  ·  {TICKER}  —  NUMBERS & SIGNALS",
        f"${CURRENT_PRICE:.2f}  ·  {DATE}  ·  Price source: Yahoo Finance")

print(f"""
  {chr(9484)}{chr(8212)*62}{chr(9488)}
  {chr(9474)}  {SIGNAL:<20}  Ratio B {ratio_B:.2f}x  (primary signal)             {chr(9474)}
  {chr(9474)}  EPP ${epp_now:.0f}  ({epp_gap_pct:+.0f}% gap)  {chr(183)}  Fwd P/E {forward_pe:.0f}x  {chr(183)}  Cons. {cons_ret_ann:+.0f}%/yr          {chr(9474)}
  {chr(9474)}  Idiosyncratic {IDIO['idio_pct']}% / Macro {IDIO['macro_pct']}%  {chr(183)}  Beta {IDIO['beta']:.2f}                        {chr(9474)}
  {chr(9492)}{chr(8212)*62}{chr(9496)}""")

# Cross-reads
print(f"""
  CROSS-READ MODEL  (proxy {proxy_composite:.2f} / 4.00  {chr(183)}  market {mkt_comp:.2f}  {chr(183)}  gap {adj_gap:+.2f})
{SL}
  {"Signal":<32}  {"Tracks":<26}  {"Now":>6}  Score    Bar""")
print(SL)
for name, desc, unit, bc, blo, bulo, xlo, cur, w, sc in scored:
    u = unit.split()[0]
    print(f"  {name:<32}  {desc:<26}  {cur:>+5}{u}  {SLABEL[sc]}  {SBAR[sc]}")
print(SL)
print(f"  Structural adjustment (SCA):")
for desc, sc, wt in STRUCTURAL_FACTORS:
    sign = "+" if sc > 0 else " "
    print(f"    {sign}{sc:+.1f} {chr(215)} {wt*100:.0f}%  {desc}")
print(f"  SCA {sca:+.2f}  {chr(8594)}  adj composite {adj_composite:.2f}  {chr(8594)}  verdict: {'UNDERVALUED' if adj_gap > 0.5 else 'FAIRLY VALUED'}")

# Scenario thresholds
print(f"""
  SCENARIO THRESHOLDS
{SL}
  {"Signal":<32}  {"BEAR<":>6}  {"BASE":>8}  {"BULL":>8}  {"XBULL≥":>8}  {"NOW":>6}""")
print(SL)
for name, desc, unit, bc, blo, bulo, xlo, cur, w, sc in scored:
    u = unit.split()[0]
    print(f"  {name:<32}  {bc:>5}{u}  {blo}-{bulo:<3}    {bulo}-{xlo:<3}    {xlo:>5}{u}  {cur:>+5}{u}")

# EPP floor
print(f"""
  EPP FLOOR
{SL}
  {"Year":<8}  {"EPS":>6}  {chr(215)} {"Trough P/E":>10}  {"EPP":>7}  {"Actual low":>12}""")
print(SL)
print(f"  {'FY2022':<8}  ${EPS_TROUGH:>5.2f}  {'× 22x':>12}  ${epp_trough_val:>5.0f}  {'$213  ✓':>12}")
print(f"  {'FY2025':<8}  ${EPS_NOW:>5.2f}  {'× 22x':>12}  ${epp_now:>5.0f}  {'—':>12}  {chr(8592)} today's floor")
print(SL)
print(f"  Floor migration +${epp_now - epp_trough_val:.0f} (+{(epp_now/epp_trough_val-1)*100:.0f}%)  — entirely EPS compounding, multiple unchanged")
print(f"  Current ${CURRENT_PRICE:.2f} is {epp_gap_pct:.0f}% above floor  {chr(183)}  {(CURRENT_PRICE-epp_now)/sigma:.1f}{chr(963)} to EPP")
print(f"  Bear ${sc_map['BEAR'][3]:.0f} is {bear_vs_epp:.0f}% vs floor  {chr(8592)} bear scenario breaks through EPP")

# EPS quality
print(f"""
  EPS QUALITY  ({EPS_TROUGH_YEAR} ${EPS_TROUGH:.2f} {chr(8594)} FY2025 ${EPS_NOW:.2f};  +{(EPS_NOW/EPS_TROUGH-1)*100:.0f}%  {chr(183)}  CAGR {((EPS_NOW/EPS_TROUGH)**(1/3)-1)*100:.1f}%/yr)
{SL}
  {"Driver":<38}  {"Share":>7}  {"$EPS":>6}  Type""")
print(SL)
for driver, share, is_real in EPS_DECOMP:
    dollar = EPS_TROUGH * share
    tag = "REAL  ✓" if is_real else "INFL. ~"
    print(f"  {driver:<38}  {share*100:>6.1f}%  ${dollar:>4.2f}  {tag}")
print(SL)
print(f"  Real {real_dollar/eps_g_total*100:.0f}%  (${real_dollar:.2f})     Inflation {infl_dollar/eps_g_total*100:.0f}%  (${infl_dollar:.2f})")

# Scenarios
print(f"""
  SCENARIOS  (2-year;  May 2026 {chr(8594)} May 2028)
{SL}
  {"Scenario":<8}  {"EPS":>7}  {"P/E":>5}  {"Price":>7}  {"Proxy%":>8}  {"Mkt%":>7}  {"Gap":>8}  Narrative""")
print(SL)
for lbl, narr, eps, pe, price in SCENARIOS:
    pp = proxy_probs[lbl]
    mp = mkt_probs.get(lbl, 0)
    print(f"  {lbl:<8}  ${eps:>6.2f}  {pe:>4}x  ${price:>6}  {pp*100:>7.1f}%  {mp*100:>6.1f}%  {(pp-mp)*100:>+7.1f}pp  {narr[:28]}")
print(SL)
print(f"  Proxy EV ${proxy_ev:.0f}  {chr(183)}  Market needs ${mkt_ev:.0f} to justify ${CURRENT_PRICE:.2f} at {REQUIRED_RETURN*100:.0f}%/yr  {chr(183)}  Consensus ~$560")

# Attractiveness ratio
print(f"""
  ATTRACTIVENESS RATIO  (downside to EPP ${dist_epp:.0f}  =  {dist_epp/CURRENT_PRICE*100:.0f}% of price)
{SL}
  {"Method":<32}  {"2yr Target":>11}  {"Upside":>8}  {"Ratio":>7}  Signal""")
print(SL)
print(f"  {'A: Same P/E  (' + f'{trailing_pe:.0f}x trailing)':<32}  ${price_A:>9.0f}  {(price_A-CURRENT_PRICE)/CURRENT_PRICE*100:>+7.0f}%  {ratio_A:>6.2f}x  {rlabel(ratio_A)}")
print(f"  {'B: Conserv exit 30x  ← PRIMARY':<32}  ${price_B:>9.0f}  {(price_B-CURRENT_PRICE)/CURRENT_PRICE*100:>+7.0f}%  {ratio_B:>6.2f}x  {rlabel(ratio_B)}")
print(f"  {'C: BASE scenario':<32}  ${price_C:>9.0f}  {(price_C-CURRENT_PRICE)/CURRENT_PRICE*100:>+7.0f}%  {ratio_C:>6.2f}x  {rlabel(ratio_C)}")

# Idiosyncratic
print(f"""
  IDIOSYNCRATIC SCORE
{SL}
  Idiosyncratic   {IDIO['idio_pct']}%  {"█" * (IDIO['idio_pct'] // 3)}{"░" * (33 - IDIO['idio_pct'] // 3)}
  Macro/sentiment {IDIO['macro_pct']}%  {"█" * (IDIO['macro_pct'] // 3)}{"░" * (33 - IDIO['macro_pct'] // 3)}
  Beta {IDIO['beta']:.2f}
{SL}
  {"Factor":<36}  {"Type":>6}  {"Wt":>5}  Note""")
print(SL)
for factor, kind, wt, desc in IDIO["drivers"]:
    print(f"  {factor:<36}  {kind:>6}  {wt*100:>4.0f}%  {desc[:30]}")

# Entry framework
epp_buy_hi = epp_now * 1.10
epp_acc_hi = epp_now * 1.20
watch_lo   = CURRENT_PRICE * 1.05
watch_hi   = CURRENT_PRICE * 1.15
avoid_lo   = watch_hi
print(f"""
  ENTRY FRAMEWORK
{SL}
  {"Zone":<18}  {"Price":>16}  {"Ratio B":>9}  Action""")
print(SL)
print(f"  {'◉ EPP floor':<18}  {'$' + f'{epp_now:.0f}' + ' – $' + f'{epp_buy_hi:.0f}':>16}  {'< 0.50x':>9}  Buy aggressively")
print(f"  {'◎ High conv.':<18}  {'$' + f'{epp_buy_hi:.0f}' + ' – $' + f'{epp_acc_hi:.0f}':>16}  {'0.50–0.75x':>9}  Build position")
print(f"  {'◐ Today':<18}  {'~$' + f'{CURRENT_PRICE:.0f}':>16}  {f'{ratio_B:.2f}x':>9}  Hold; no add")
print(f"  {'○ Trim zone':<18}  {'$' + f'{watch_lo:.0f}' + ' – $' + f'{watch_hi:.0f}':>16}  {'1.75–2.5x':>9}  Reduce on strength")
print(f"  {'✕ Avoid':<18}  {'> $' + f'{avoid_lo:.0f}':>16}  {'> 2.50x':>9}  Exit / avoid new")
print(SL)
print(f"  UPGRADE to ◎ ACCUMULATE if:  Azure sustains >30% for 2 qtrs  OR  Copilot >15M seats")
print(f"  DOWNGRADE to ✕ if:           Azure falls <15%  OR  CapEx guidance raised again without rev upside")

print()
print(HL)
print(f"  {TICKER}  {chr(183)}  {SIGNAL}  {chr(183)}  Ratio B {ratio_B:.2f}x  {chr(183)}  EPP ${epp_now:.0f} ({epp_gap_pct:+.0f}%)  {chr(183)}  Idio {IDIO['idio_pct']}% / Macro {IDIO['macro_pct']}%")
print(HL)
print()
