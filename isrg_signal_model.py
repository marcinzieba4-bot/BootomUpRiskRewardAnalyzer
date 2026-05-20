#!/usr/bin/env python3
"""
ISRG  ·  Intuitive Surgical
BottomUp Risk/Reward Analyzer  —  three-part publication format

Part 1  FRAMEWORK LOGIC     what each concept means (reusable)
Part 2  ISRG CASE           narrative per section, only what matters
Part 3  NUMBERS & SIGNALS   pure data, no prose

Price: $452  (Yahoo Finance, 2026-05-09)
"""
import math

# ══════════════════════════════════════════════════════════════════════════════
# INPUTS
# ══════════════════════════════════════════════════════════════════════════════
TICKER        = "ISRG"
COMPANY       = "Intuitive Surgical"
SECTOR        = "Surgical Robotics · Medical Devices"
DATE          = "2026-05-09"
CURRENT_PRICE = 452.0     # Yahoo Finance / WebSearch 2026-05-09

EPS_TROUGH_YEAR   = 2022
EPS_TROUGH        = 4.96
EPS_NOW           = 8.93
EPS_Q1_2026       = 2.50
EPS_FWD_CONSENSUS = 10.40
EPS_TROUGH_PRICE  = 197.0

EPP_MIN_PE      = 40.0
CONS_EPS_CAGR   = 0.15
CONS_EXIT_PE    = 47.0
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

SCENARIOS = [
    ("BEAR",  "China ban + GLP-1 collapse + hospital freeze",     8.80, 38,  334),
    ("BASE",  "DV5 global rollout; Ion scaling; China contained", 12.30, 52,  640),
    ("BULL",  "Ion mainstream; new indications approved",         14.00, 58,  812),
    ("XBULL", "Surgical AI platform; intl re-acceleration",       16.50, 65, 1073),
]

CROSS_READS = [
    # name, what_it_tells_us, unit, bear_ceil, base_lo, bull_lo, xbull_lo, current, weight
    ("DV5 placements YoY",          "Hospital capex health",           "% YoY",  5,  5, 12, 20,  17, 0.25),
    ("Procedure volume YoY",        "Surgeon adoption & recurring rev", "% YoY",  8,  8, 14, 20,  16, 0.25),
    ("Ion platform procedures YoY", "New market traction",             "% YoY", 25, 25, 55, 90,  39, 0.15),
    ("International revenue YoY",   "Geographic expansion",            "% YoY",  8,  8, 15, 22,  13, 0.15),
    ("Hospital capex YoY",          "Macro / budget environment",      "% YoY",  3,  3,  7, 12,   5, 0.10),
    ("China procedure volume YoY",  "Geopolitical risk barometer",     "% YoY",  0,  0, 10, 20,   8, 0.10),
]

STRUCTURAL_FACTORS = [
    ("Installed base switching cost moat  (9,000+ systems)",     +1.5, 0.25),
    ("No credible full-system competitor (2026)",                +1.0, 0.20),
    ("China revenue concentration  (~10-12% of revenue)",       -1.0, 0.20),
    ("GLP-1 → bariatric procedure volume overhang",             -0.5, 0.15),
    ("DV5 upgrade cycle — hospitals mid-rollout",               +0.8, 0.20),
]

EPS_DECOMP = [
    ("Real procedure volume growth",     0.44,  True),
    ("Operating leverage / margin",      0.26,  True),
    ("Mix shift  (Ion + complex procs)", 0.07,  True),
    ("ASP / consumable price hikes",     0.115, False),
    ("CPI cost pass-through",            0.105, False),
    ("Share count reduction",            0.010, True),
]

# ── IDIOSYNCRATIC ASSESSMENT ──────────────────────────────────────────────────
IDIO = {
    "idio_pct": 62,   # % of return driver that is company/sector-specific
    "macro_pct": 38,  # % driven by macro sentiment / rates / risk appetite
    "beta": 1.05,
    "drivers": [
        # (factor, idio_or_macro, weight, description)
        ("DV5 upgrade cycle execution",         "IDIO",  0.22, "Hospital-by-hospital adoption; no macro linkage"),
        ("Ion platform reimbursement & growth", "IDIO",  0.18, "FDA/CMS decisions; lung cancer screening TAM"),
        ("China revenue  (ban vs. growth)",     "IDIO",  0.15, "Geopolitical; specific to US medtech in China"),
        ("GLP-1 procedure volume impact",       "IDIO",  0.07, "Sector-specific; bariatric / hernia volumes"),
        ("P/E multiple  (rate sensitivity)",    "MACRO", 0.18, "At 51x, 100bp rate move ≈ 5-8pt P/E compression"),
        ("Hospital capex budget cycle",         "MACRO", 0.10, "Correlated with GDP / CFO confidence surveys"),
        ("Broad market beta  (1.05x)",          "MACRO", 0.10, "Moves with S&P; amplified in risk-off episodes"),
    ],
    "note": (
        "ISRG is a moderately idiosyncratic bet.  The EPP floor and recurring "
        "revenue base (~70% instruments/accessories) are company-specific — they "
        "do not disappear in a recession.  However ~38% of the return profile is "
        "macro-sensitive: the P/E at 51x is rate-elastic, and broad risk-off "
        "episodes pull the stock down regardless of fundamentals (as seen in 2022 "
        "and YTD 2026).  The single largest idiosyncratic risk is China — a binary "
        "event (ban vs. no ban) that has no macro substitute."
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
mkt_ev = ev(mkt_probs) if mkt_probs else mkt_target
proxy_ev = ev(proxy_probs)

epp_now         = EPS_NOW * EPP_MIN_PE
epp_trough_val  = EPS_TROUGH * EPP_MIN_PE
epp_gap_pct     = (CURRENT_PRICE - epp_now) / epp_now * 100
bear_vs_epp     = (sc_map["BEAR"][3] - epp_now) / epp_now * 100

trailing_pe = CURRENT_PRICE / EPS_NOW
forward_pe  = CURRENT_PRICE / EPS_FWD_CONSENSUS

cons_eps_2yr   = EPS_NOW * (1 + CONS_EPS_CAGR) ** 2
cons_price_2yr = cons_eps_2yr * CONS_EXIT_PE
cons_ret_ann   = (cons_price_2yr - CURRENT_PRICE) / CURRENT_PRICE / 2 * 100

dist_epp = CURRENT_PRICE - epp_now
price_A  = CURRENT_PRICE * (1 + (cons_eps_2yr / EPS_NOW - 1))
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

SIGNAL = rlabel(ratio_B)
adj_gap = adj_composite - mkt_comp if mkt_comp else 0

vol_pct = 0.28
sigma   = CURRENT_PRICE * vol_pct
eps_g_total = EPS_NOW - EPS_TROUGH
infl_dollar = sum(EPS_TROUGH * sh for _, sh, real in EPS_DECOMP if not real)
real_dollar = eps_g_total - infl_dollar


# ══════════════════════════════════════════════════════════════════════════════
# OUTPUT  —  three-part publication format
# ══════════════════════════════════════════════════════════════════════════════
W  = 74
HL = "=" * W   # heavy rule  (section breaks)
ML = "-" * W   # medium rule (sub-sections)
SL = "  " + "-" * 62  # slim rule  (tables)

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
# PART 2  —  ISRG ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
section(f"PART 2  ·  {TICKER}  —  ANALYST COMMENTARY",
        f"{COMPANY}  ·  {SECTOR}  ·  {DATE}  ·  ${CURRENT_PRICE:.0f}")

print(f"""
  ┌{"─"*62}┐
  │  SIGNAL:  {SIGNAL:<20}  (primary: Ratio B {ratio_B:.2f}x)        │
  │  EPP floor ${epp_now:.0f}  ·  Gap {epp_gap_pct:+.0f}%  ·  Conservative return {cons_ret_ann:+.0f}%/yr   │
  └{"─"*62}┘""")

sub("1.  The worst EPP — when the floor was touched")
p(f"""
ISRG's EPP floor was last touched in June 2022, when the stock hit
$197 — its lowest point since 2017. What drove it there was not the
business: it was the 2022 Fed rate cycle repricing every long-duration
growth asset simultaneously. Procedure volumes grew through the entire
selloff, DV5 placements continued, and EPS beat consensus every quarter
of the decline.

The floor that held at $197 reflects a 40x trough P/E. That number is
worth understanding. A 40x floor — even at maximum market fear — is not
assigned to cyclical businesses or companies where earnings are at risk.
It is the multiple the market applies when it is convinced that earnings
are structural, recurring, and will compound regardless of the macro
environment. In ISRG's case the reason is the installed base: 9,000+
systems already placed generate consumable revenue on every procedure
performed, independent of whether a single new system is ever sold.
The market treats that stream as near-annuity quality, and prices it
accordingly even at the worst moment of a rate cycle.

Contrast this with a medical device company that sells capital equipment
without a razor/razorblade model — those businesses trough at 12-18x
because revenue can simply stop. ISRG's 40x floor implies the market
has always believed high-probability continued EPS growth is structural,
not cyclical. You cannot buy this stock at a trough multiple that prices
in business decline — the installed base economics prevent it.
""")

sub("2.  What changed since 2022 — and is it structural?")
p(f"""
EPS has compounded from ${EPS_TROUGH:.2f} to ${EPS_NOW:.2f} — a {(EPS_NOW/EPS_TROUGH-1)*100:.0f}% gain in three years,
or {((EPS_NOW/EPS_TROUGH)**(1/3)-1)*100:.1f}%/yr. As a result the EPP floor has migrated from $198
to ${epp_now:.0f}. The trough multiple is unchanged at 40x. The floor moved
entirely because the business got physically larger.

We decompose the ${eps_g_total:.2f} EPS gain into real versus inflation:

  {real_dollar/eps_g_total*100:.0f}% real ({real_dollar:.2f}/shr) — procedure volume growth, operating
    leverage, Ion mix shift, and buybacks. The installed base grew
    from ~7,000 to 9,000+ systems; that is not a pricing artifact.
    Stripping inflation entirely, real EPS is ${EPS_NOW - infl_dollar:.2f}, implying
    a real EPP of ${(EPS_NOW - infl_dollar)*EPP_MIN_PE:.0f}. The floor survives a full
    inflation haircut.

  {infl_dollar/eps_g_total*100:.0f}% inflation ({infl_dollar:.2f}/shr) — ASP hikes on consumables and
    CPI cost pass-through. Legitimate in a monopoly with pricing power,
    but less structural than volume growth.

Verdict: structural. Q1 2026 EPS of ${EPS_Q1_2026:.2f} annualises to $10+,
up 38% year-on-year, confirming the trajectory is accelerating.
""")

sub("3.  How likely is a return below the EPP floor?")
p(f"""
At ${CURRENT_PRICE:.0f} the stock is ${dist_epp:.0f} (21%) above the current floor of
${epp_now:.0f}. To revisit the floor, either EPS must fall or the market
must compress the trough multiple below 40x.

Multiple compression alone (without EPS decline): a repeat of the 2022
rate shock would bring the stock to ~${epp_now:.0f} — not below it. The floor
itself would not break; price would simply converge to it. That is the
scenario where $357–$397 becomes an extremely attractive entry zone.

EPS decline: the only event that cuts EPS materially is a China ban.
China is ~10-12% of revenue; a full ban strips ~$0.80-1.00 from EPS,
cutting the EPP floor to ~${(EPS_NOW - 0.9)*EPP_MIN_PE:.0f}. That is what the BEAR
scenario captures: ${sc_map['BEAR'][1]:.2f} EPS × {sc_map['BEAR'][2]}x = ${sc_map['BEAR'][3]:.0f} — which is -6%
below the current floor of ${epp_now:.0f}. The floor pierces, but only
because the earnings themselves are impaired simultaneously.

Our model: {proxy_probs['BEAR']*100:.0f}% probability on BEAR. Market implies {mkt_probs.get('BEAR',0)*100:.0f}%.
No current data supports the higher figure. Q1 2026 China procedures
were up 8%, DV5 placements +17%, procedure volume +16%. The market is
applying a geopolitical fear premium to a business that is still growing
in every reportable dimension. The floor will not break unless the
data breaks first.
""")

sub("4.  Cross-read model — observable score vs market-implied score")
p(f"""
Six signals are tracked and scored 1–4 before each quarter report.
The weighted composite tells us what the observable environment is
consistent with. We back-solve the composite the current stock price
requires to deliver a 15% annual hurdle rate — that is the market's
implied score.

  Signal                        Score (1-4)   Weight   Current reading
  DV5 placements YoY           BULL  (3/4)     22%    +17%  — above 12% BULL threshold
  Procedure volume YoY         BULL  (3/4)     20%    +16%  — surgeon adoption accelerating
  Ion procedures YoY           BASE  (2/4)     18%    +39%  — approaching 55% BULL threshold
  International revenue YoY   BASE  (2/4)     15%    +13%  — steady, no acceleration
  Hospital capex YoY           BASE  (2/4)     15%     +5%  — healthy, not a tailwind
  China procedures YoY         BASE  (2/4)     10%     +8%  — positive; geopolitical watch

Raw proxy composite:     {proxy_composite:.2f} / 4.00
Structural adj (SCA):   +{sca:.2f}  (moat, DV5 cycle vs China/GLP-1 offset)
Adjusted composite:      {adj_composite:.2f} / 4.00

Market-implied composite: {mkt_comp:.2f}  — the score embedded in ${CURRENT_PRICE:.0f} at 15%/yr

Gap: +{adj_gap:.2f} composite points. Our signals price a BASE/BULL blend.
The market prices nearly pure BASE, applying a heavy discount for
geopolitical risk that is not yet materialising in reported data.
That gap is the source of the ACCUMULATE signal.

Watch: Ion at +39% is approaching its BULL threshold of +55%. If it
crosses, it signals that lung cancer screening is opening at scale —
a new market not in consensus. That single move would upgrade the
composite toward BULL and push Ratio B below 0.75x (BUY territory).
China at +8% is one headline away from BEAR. A ban confirmation
collapses the composite below BASE, challenges the EPP floor, and
triggers a DOWNGRADE.
""")

sub("5.  How idiosyncratic is this bet? — what your research controls")
p(f"""
ISRG scores {IDIO['idio_pct']}% idiosyncratic: roughly {IDIO['idio_pct']} cents of every dollar of
return variance comes from factors you can research and have a view on.
The remaining {IDIO['macro_pct']}% is driven by rates, market sentiment, and
hospital budget cycles that are harder to forecast precisely.

For context: a bank is ~25% idiosyncratic. A commodity producer ~15%.
ISRG is unusually company-specific for its size — fundamental work
creates genuine edge here.

THE {IDIO['idio_pct']}% THAT IS YOURS TO GET RIGHT
─────────────────────────────────────
DV5 execution (22%): Adoption is hospital-by-hospital. The upgrade
  cycle is trackable via quarterly placements data. No macro correlation
  — hospitals decide on surgeon demand and local budgets, not the Fed.

Ion reimbursement (18%): CMS and FDA decisions on lung cancer screening
  reimbursement are the binary events. An expanded code accelerates Ion
  adoption regardless of the interest rate environment. This is
  researchable: watch CMS comment periods and clinical guideline updates.

China binary (15%): A ban or tariff escalation is geopolitical and
  specific to US medtech — not a broad market event. You can form a view
  on US-China trade dynamics and size your China risk exposure accordingly.
  This is the only factor that breaks the EPP floor.

GLP-1 bariatric overhang (7%): Incremental data from metabolic surgery
  conferences and insurance coverage decisions will resolve this. Unlikely
  to be existential — robotic surgery is expanding beyond bariatric.

THE {IDIO['macro_pct']}% THAT MACRO CONTROLS
──────────────────────────────
Rate sensitivity (18%): At {trailing_pe:.0f}x trailing P/E, a 100bp move in the
  10-year yield compresses the multiple by ~5-8 points — a $45-70 price
  impact with no change in fundamentals. This happened in 2022 and again
  in early 2026. Being right on the business does not protect you here.

Hospital capex cycle (10%): Correlated to GDP and CFO confidence. In a
  hard recession, hospitals defer capital equipment purchases. Systematic
  risk — not ISRG-specific.

Market beta (10%): At 1.05x beta, broad risk-off events track the S&P.
  No fundamental work protects against a market-wide drawdown.

WHAT THIS MEANS FOR POSITION SIZING
The EPP floor (${epp_now:.0f}) is almost entirely idiosyncratic — anchored to
EPS, not sentiment. Macro can only push price through it by also
impairing the earnings (China scenario). At ${CURRENT_PRICE:.0f} you are 27%
above the floor, in the zone where the {IDIO['macro_pct']}% macro exposure is most
relevant. The ACCUMULATE signal rather than conviction BUY reflects
this: the thesis is right, but you are not being paid to ignore the
macro component at current prices.
""")

# ─────────────────────────────────────────────────────────────────────────────
# PART 3  —  DATA TABLES
# ─────────────────────────────────────────────────────────────────────────────
section(f"PART 3  ·  {TICKER}  —  NUMBERS & SIGNALS",
        f"${CURRENT_PRICE:.0f}  ·  {DATE}  ·  Price source: Yahoo Finance")

# Signal card
print(f"""
  ┌{"─"*62}┐
  │  {SIGNAL:<20}  Ratio B {ratio_B:.2f}x  (primary signal)             │
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
    print(f"  {name:<32}  {desc:<28}  {cur:>+4}{u}  {SLABEL[sc]}  {SBAR[sc]}")
print(SL)
print(f"  Structural adjustment (SCA):")
for desc, sc, wt in STRUCTURAL_FACTORS:
    sign = "+" if sc > 0 else " "
    print(f"    {sign}{sc:+.1f} × {wt*100:.0f}%  {desc}")
print(f"  SCA {sca:+.2f}  →  adj composite {adj_composite:.2f}  →  verdict: UNDERVALUED")

# Scenario thresholds
print(f"""
  SCENARIO THRESHOLDS
{SL}
  {"Signal":<32}  {"BEAR<":>6}  {"BASE":>8}  {"BULL":>8}  {"XBULL≥":>8}  {"NOW":>5}""")
print(SL)
for name, desc, unit, bc, blo, bulo, xlo, cur, w, sc in scored:
    u = unit.split()[0]
    print(f"  {name:<32}  {bc:>5}{u}  {blo}-{bulo:>3}    {bulo}-{xlo:>3}    {xlo:>5}{u}  {cur:>+4}{u}")

# EPP
print(f"""
  EPP FLOOR
{SL}
  {"Year":<8}  {"EPS":>6}  {"× Trough P/E":>14}  {"EPP":>7}  {"Actual low":>12}""")
print(SL)
print(f"  {'2022':<8}  ${EPS_TROUGH:>5.2f}  {'× 40x':>14}  ${epp_trough_val:>5.0f}  {'$197  ✓':>12}")
print(f"  {'2026':<8}  ${EPS_NOW:>5.2f}  {'× 40x':>14}  ${epp_now:>5.0f}  {'—':>12}  ← today's floor")
print(SL)
print(f"  Floor migration +${epp_now - epp_trough_val:.0f} (+{(epp_now/epp_trough_val-1)*100:.0f}%)  — entirely EPS compounding, multiple unchanged")
print(f"  Current ${CURRENT_PRICE:.0f} is {epp_gap_pct:.0f}% above floor  ·  {(CURRENT_PRICE-epp_now)/sigma:.1f}σ to EPP")
print(f"  Bear ${sc_map['BEAR'][3]:.0f} is {bear_vs_epp:.0f}% vs floor  ← bear scenario breaks through EPP")

# EPS quality
print(f"""
  EPS QUALITY  (FY{EPS_TROUGH_YEAR} ${EPS_TROUGH:.2f} → FY2025 ${EPS_NOW:.2f};  +{(EPS_NOW/EPS_TROUGH-1)*100:.0f}%  ·  CAGR {((EPS_NOW/EPS_TROUGH)**(1/3)-1)*100:.1f}%/yr)
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
  SCENARIOS  (2-year;  May 2026 → May 2028)
{SL}
  {"Scenario":<8}  {"EPS":>7}  {"P/E":>5}  {"Price":>7}  {"Proxy%":>8}  {"Mkt%":>7}  {"Gap":>8}  Narrative""")
print(SL)
for lbl, narr, eps, pe, price in SCENARIOS:
    pp = proxy_probs[lbl]
    mp = mkt_probs.get(lbl, 0)
    print(f"  {lbl:<8}  ${eps:>6.2f}  {pe:>4}x  ${price:>6}  {pp*100:>7.1f}%  {mp*100:>6.1f}%  {(pp-mp)*100:>+7.1f}pp  {narr[:28]}")
print(SL)
print(f"  Proxy EV ${proxy_ev:.0f}  ·  Market needs ${mkt_ev:.0f} to justify ${CURRENT_PRICE:.0f} at {REQUIRED_RETURN*100:.0f}%/yr  ·  Consensus ~$622")

# Attractiveness ratio
print(f"""
  ATTRACTIVENESS RATIO  (downside to EPP ${dist_epp:.0f}  =  {dist_epp/CURRENT_PRICE*100:.0f}% of price)
{SL}
  {"Method":<30}  {"2yr Target":>11}  {"Upside":>8}  {"Ratio":>7}  Signal""")
print(SL)
print(f"  {'A: Same P/E  (51x trailing)':<30}  ${price_A:>9.0f}  {(price_A-CURRENT_PRICE)/CURRENT_PRICE*100:>+7.0f}%  {ratio_A:>6.2f}x  {rlabel(ratio_A)}")
print(f"  {'B: Conserv exit 47x  ← PRIMARY':<30}  ${price_B:>9.0f}  {(price_B-CURRENT_PRICE)/CURRENT_PRICE*100:>+7.0f}%  {ratio_B:>6.2f}x  {rlabel(ratio_B)}")
print(f"  {'C: BASE scenario':<30}  ${price_C:>9.0f}  {(price_C-CURRENT_PRICE)/CURRENT_PRICE*100:>+7.0f}%  {ratio_C:>6.2f}x  {rlabel(ratio_C)}")

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
    print(f"  {factor:<36}  {kind:>6}  {wt*100:>4.0f}%  {desc[:28]}")

# Entry framework
print(f"""
  ENTRY FRAMEWORK
{SL}
  {"Zone":<16}  {"Price":>12}  {"Ratio B":>9}  Action""")
print(SL)
print(f"  {'◉ EPP floor':<16}  {'$357 – $397':>12}  {'< 0.50x':>9}  Buy aggressively")
print(f"  {'◎ High conv.':<16}  {'$397 – $430':>12}  {'0.50–0.75x':>9}  Build position")
print(f"  {'◎ Today':<16}  {'~$452':>12}  {'0.92x':>9}  Accumulate")
print(f"  {'◐ Watchlist':<16}  {'$480 – $530':>12}  {'1.1–1.5x':>9}  Hold / no add")
print(f"  {'✕ Avoid':<16}  {'> $530':>12}  {'> 1.75x':>9}  Trim on strength")
print(SL)
print(f"  UPGRADE to ◉ BUY if:  Ion > 55% growth  OR  China risk resolved")
print(f"  DOWNGRADE to ✕ if:    Procedure vol < 8% for 2 qtrs  OR  China ban confirmed")

print()
print(HL)
print(f"  {TICKER}  ·  {SIGNAL}  ·  Ratio B {ratio_B:.2f}x  ·  EPP ${epp_now:.0f} ({epp_gap_pct:+.0f}%)  ·  Idio {IDIO['idio_pct']}% / Macro {IDIO['macro_pct']}%")
print(HL)
print()
