#!/usr/bin/env python3
"""
WMB  ·  The Williams Companies
BottomUp Risk/Reward Analyzer  —  three-part publication format

Part 1  FRAMEWORK LOGIC     what each concept means (reusable)
Part 2  WMB CASE            narrative per section, only what matters
Part 3  NUMBERS & SIGNALS   pure data, no prose

Price: $78.41  (Yahoo Finance / WebSearch, 2026-05-20)
"""
import math

# ══════════════════════════════════════════════════════════════════════════════
# INPUTS
# ══════════════════════════════════════════════════════════════════════════════
TICKER        = "WMB"
COMPANY       = "The Williams Companies"
SECTOR        = "Midstream Energy Infrastructure · Natural Gas Pipelines"
DATE          = "2026-05-21"
CURRENT_PRICE = 78.41     # Yahoo Finance / WebSearch 2026-05-20

EPS_TROUGH_YEAR  = 2022
EPS_TROUGH       = 1.67     # FY2022 adjusted EPS (post-restructuring baseline; 5yr CAGR anchor)
EPS_TROUGH_PRICE = 27.0     # 2021-22 pre-AI-rerating low; $1.67 × 16x = $26.7 ≈ $27 ✓
EPS_NOW          = 2.10     # FY2025 adjusted EPS (record year; 9% YoY)
EPS_FWD_CONSENSUS = 2.35    # FY2026E (guidance $2.20-$2.38; consensus $2.42; midpoint $2.35)

EPP_MIN_PE      = 16.0      # fee-based midstream floor: $1.67 × 16 = $26.7 ≈ $27 ✓
CONS_EPS_CAGR   = 0.12      # 12%/yr (conservative; company guiding ~9-10% EBITDA growth)
CONS_EXIT_PE    = 25.0      # removes AI premium; quality midstream fair value ex-data center
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

SCENARIOS = [
    # lbl, narrative, eps, pe, price
    ("BEAR",  "AI CapEx stalls; BTM frozen; Transco growth flat",       1.90, 14,   27),
    ("BASE",  "Transco executes; BTM adds revenue; steady gas demand",   2.60, 22,   57),
    ("BULL",  "BTM scales; Transco zone 3; LNG export boost",            3.20, 28,   90),
    ("XBULL", "WMB = US AI infrastructure backbone; BTM mainstream",     4.00, 32,  128),
]

CROSS_READS = [
    # name, what_it_tells_us, unit, bear_ceil, base_lo, bull_lo, xbull_lo, current, weight
    ("Transco throughput growth YoY",  "Core pipeline volume health",          "% YoY",   1,  1,  3,  6,   5, 0.25),
    ("BTM data center backlog",        "AI infrastructure contract wins",       "$B",      0.5,0.5,2,  5, 3.1, 0.25),
    ("Power gen gas demand YoY",       "Structural gas demand driver",          "% YoY",   3,  3,  7, 12,   8, 0.20),
    ("Henry Hub  ($/MMBtu)",           "Gas price → upstream incentive",        "$/MMBtu", 2,  2,  3,  5, 3.6, 0.15),
    ("LNG export utilisation",         "LNG pull-through on Transco system",    "%",       70, 70, 85, 92,  91, 0.10),
    ("WMB expansion projects in-svc",  "Contracted backlog delivery",           "$B",      0.5,0.5,1.5,3,  2.0, 0.05),
]

STRUCTURAL_FACTORS = [
    ("Transco east coast corridor monopoly  (no bypass possible)",   +1.5, 0.25),
    ("Fee-based revenues ~96%  (take-or-pay; long-term contracts)",  +1.0, 0.20),
    ("High leverage  (Net Debt/EBITDA ~4x; rate-sensitive)",         -1.0, 0.20),
    ("AI/BTM data center optionality  (transformational if scales)", +0.8, 0.15),
    ("Gas demand regulatory/political risk  (LNG policy; EPA)",      -0.6, 0.20),
]

EPS_DECOMP = [
    ("Transco organic volume growth  (throughput + pricing)",  0.35, True),
    ("Transco expansion projects  (new capacity in-service)",  0.25, True),
    ("Operating leverage  (scale + cost efficiency)",          0.15, True),
    ("BTM data center revenue  (nascent platform)",            0.10, True),
    ("Natural gas price benefit  (upstream / marketing)",      0.10, False),
    ("Share buybacks  (count reduction)",                      0.05, True),
]

# ── IDIOSYNCRATIC ASSESSMENT ──────────────────────────────────────────────────
IDIO = {
    "idio_pct": 55,
    "macro_pct": 45,
    "beta": 0.90,
    "drivers": [
        ("Transco expansion execution",          "IDIO",  0.20, "Project timing; FERC; cost-to-complete"),
        ("BTM data center contract wins",         "IDIO",  0.20, "Hyperscaler deals; WMB commercial pipeline"),
        ("Leverage / balance sheet management",  "IDIO",  0.15, "Credit metrics; refinancing; debt reduction"),
        ("Natural gas demand cycle",             "MACRO", 0.20, "GDP + power demand + LNG; not WMB-specific"),
        ("Interest rate sensitivity",            "MACRO", 0.15, "High leverage; ~4x EBITDA; 100bp = ~$0.15 EPS"),
        ("Broad market beta  (0.90x)",           "MACRO", 0.10, "Energy sector + market-wide risk-off moves"),
    ],
    "note": (
        "WMB is a moderately idiosyncratic bet — similar to MSFT but from an infrastructure "
        "angle. The Transco monopoly corridor and fee-based contracts anchor the EPP floor "
        "as a company-specific asset: no macro event removes the physical pipeline or voids "
        "long-term take-or-pay agreements. The BTM data center strategy is purely "
        "idiosyncratic — either WMB wins hyperscaler contracts at scale or it does not. "
        "But 45% of return variance is macro: the stock is rate-sensitive (high leverage), "
        "gas demand is GDP-linked, and energy sector sentiment moves with oil and policy. "
        "The AVOID signal is macro-driven — the AI premium embedded in the 37x P/E requires "
        "a benign rate environment and sustained AI CapEx to justify."
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
price_A   = CURRENT_PRICE * (1 + (cons_eps_2yr / EPS_NOW - 1))
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

vol_pct = 0.28
sigma   = CURRENT_PRICE * vol_pct

# EPS decomp (real/structural engine — same as ISRG/MSFT)
eps_g_total    = EPS_NOW - EPS_TROUGH
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
reports, each mapped to a specific business driver. Pipeline throughput
data tells us about gas demand and contract utilisation. Data centre
CapEx tells us about BTM contract wins. Power generation gas demand
tells us about the structural shift away from coal.

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
# PART 2  —  WMB ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
section(f"PART 2  ·  {TICKER}  —  ANALYST COMMENTARY",
        f"{COMPANY}  ·  {SECTOR}  ·  {DATE}  ·  ${CURRENT_PRICE:.2f}")

print(f"""
  ┌{"─"*62}┐
  │  SIGNAL:  {SIGNAL:<20}  (primary: Ratio B {rfmt(ratio_B):<10})         │
  │  EPP floor ${epp_now:.0f}  ·  Gap {epp_gap_pct:+.0f}%  ·  Conservative return {cons_ret_ann:+.0f}%/yr    │
  └{"─"*62}┘""")

sub("1.  The worst EPP — when the floor was touched")
p(f"""
WMB's EPP floor was last touched in the 2021-2022 period, when the
stock traded in the $26-28 range before the energy infrastructure
re-rating that followed the shale consolidation cycle. At that point
the business had just completed its restructuring — Williams Partners
fully absorbed, leverage declining, fee-based model locked in.

The floor multiple for fee-based midstream infrastructure is 16x. This
is not arbitrary — it sits between a regulated utility (18-20x trough,
near-guaranteed returns) and a capital-intensive pipeline with meaningful
leverage (12-14x trough). At 16x, the market is saying: we believe
the contracted revenues will continue; we acknowledge the leverage risk;
we are not paying for growth or AI optionality.

The validation: ${EPS_TROUGH:.2f} (FY2022 adjusted EPS) × 16x = ${epp_trough_val:.0f},
essentially matching the ${EPS_TROUGH_PRICE:.0f} pre-rerating low. The floor is
anchored by two things: (1) the Transco corridor physical monopoly —
there is no alternative pipeline serving the Northeast gas market from
the Gulf, and this cannot be replicated — and (2) the ~96% fee-based
revenue structure, where shippers pay capacity reservation charges
regardless of whether they actually flow gas. You cannot buy WMB at
a multiple that prices in business disruption, because the contracts
and the physical geography prevent it.

Compare this to ISRG's 40x floor: WMB's 16x is 60% lower because it
carries debt (~4x Net Debt/EBITDA), competes for capital in a yield-
driven sector, and lacks the software-like margin profile. But 16x is
still well above a commodity producer's 6-8x trough — the fee-based
model earns a durable structural premium.
""")

sub("2.  What changed since 2022 — and is it structural?")
p(f"""
EPS has compounded from ${EPS_TROUGH:.2f} to ${EPS_NOW:.2f} — a {(EPS_NOW/EPS_TROUGH-1)*100:.0f}% gain, or
{((EPS_NOW/EPS_TROUGH)**(1/3)-1)*100:.1f}%/yr over three years. Adjusted EBITDA hit a record
$7.75B in 2025, up from ~$5.9B in 2022. The EPP floor has migrated
from ${epp_trough_val:.0f} to ${epp_now:.0f}. Multiple unchanged at 16x. Floor moved
entirely because earnings grew.

We decompose the ${eps_g_total:.2f} EPS gain into real versus inflation:

  {struct_dollar/eps_g_total*100:.0f}% structural (${struct_dollar:.2f}/shr) — Transco organic volume
    growth (power generation demand + LNG exports feeding the system),
    three major expansion projects going in-service (Southeast Supply
    Enhancement, Regional Energy Access, Gulf Coast Storage), operating
    leverage as fixed-cost infrastructure scales, and nascent BTM data
    centre revenue. These are genuine earnings — new volumes flowing
    through irreplaceable pipes under long-term contracts.

  {cyclical_dollar/eps_g_total*100:.0f}% cyclical (${cyclical_dollar:.2f}/shr) — natural gas price
    benefit flowing through Williams' upstream gas marketing and
    storage positioning. Henry Hub moved from ~$2.50 to ~$3.60/MMBtu.
    This component reverts if gas prices normalise.

Verdict: structural, with one important caveat. The FY2025 EPS of
${EPS_NOW:.2f} includes ~${EPS_NOW - EPS_TROUGH:.2f} of compounded growth, most of which is
physical (more gas through more pipes under more contracts). What has
also changed — and what drives the stock price far more than the EPS —
is the AI data center thesis. WMB committed $3.1B to power projects
for data centres, building behind-the-meter (BTM) infrastructure that
bypasses traditional utilities to deliver gas directly to hyperscaler
campuses. This is potentially transformational. It is also what
pushed the P/E from 16-18x to 37x. None of that $3.1B BTM investment
is yet in the EPS. The market is paying for an option.
""")

sub("3.  How likely is a return below the EPP floor?")
p(f"""
At ${CURRENT_PRICE:.2f} the stock is ${dist_epp:.0f} ({epp_gap_pct:.0f}%) above the current EPP
floor of ${epp_now:.0f}. That is the widest EPP gap of any stock in this
portfolio. For context: ISRG is 27% above floor, MSFT 44% above.
WMB at {epp_gap_pct:.0f}% above is in a different category entirely — the gap
is almost entirely the AI data center option premium.

For the floor to break, EPS must fall back toward ${EPS_TROUGH:.2f}. That
would require: Transco volume to stall (which would need the Northeast
US to stop using natural gas — deeply unlikely), AND the gas price
benefit to reverse, AND new expansion revenues to disappoint. Our BEAR
scenario does not even require that extreme: EPS falls to ${sc_map['BEAR'][1]:.2f} (still
above any historical trough), × 14x = ${sc_map['BEAR'][3]:.0f}. That is ${abs(sc_map['BEAR'][3] - epp_now):.0f}
({abs(bear_vs_epp):.0f}%) below the current floor of ${epp_now:.0f}. The floor breaks because
the multiple contracts AND the AI premium evaporates simultaneously
— not because the underlying contracted revenue disappears.

The real risk is not the floor breaking. It is the 133% of price that
sits above the floor being slowly eroded as: (1) the BTM data centre
business takes longer to scale than the market expects, (2) interest
rates stay elevated, compressing the multiple on a levered balance
sheet, and (3) gas demand growth moderates.

Our model: {proxy_probs['BEAR']*100:.0f}% BEAR probability.
Market implies {mkt_probs.get('BEAR',0)*100:.0f}%. The floor is not the risk —
the premium is. At ${CURRENT_PRICE:.2f} and 37x trailing P/E for a business
growing EPS at 9-12%/yr, the margin of safety is essentially zero.
The conservative 2-year return (Method B: 25x exit multiple) is
negative. That is the AVOID signal.
""")

sub("4.  Cross-read model — observable score vs market-implied score")
p(f"""
Six signals are tracked and scored 1–4 before each quarter report.
The weighted composite tells us what the observable environment is
consistent with. We back-solve the score embedded in the current price.

  Signal                          Score (1-4)   Weight   Current reading
  Transco throughput growth YoY   BULL  (3/4)    25%    +5%   — above 3% BULL threshold
  BTM data center backlog         BULL  (3/4)    25%    $3.1B — in BULL ($2-5B) range
  Power gen gas demand YoY        BULL  (3/4)    20%    +8%   — above 7% BULL threshold
  Henry Hub  ($/MMBtu)            BULL  (3/4)    15%    $3.60 — in BULL ($3-5) range
  LNG export utilisation          BULL  (3/4)    10%    91%   — just below 92% XBULL threshold
  WMB expansion projects in-svc   BULL  (3/4)     5%    $2.0B — in BULL ($1.5-3B) range

Raw proxy composite:     {proxy_composite:.2f} / 4.00  (all BULL — strong operating environment)
Structural adj (SCA):   {sca:+.2f}  (Transco monopoly + fee-based offset by leverage + gas policy)
Adjusted composite:      {adj_composite:.2f} / 4.00

Market-implied composite: {mkt_comp:.2f}  — the score embedded in ${CURRENT_PRICE:.2f} at 15%/yr

Gap: {adj_gap:+.2f} composite points.

Every observable signal is at BULL. The business is performing exactly
as bulls would want: throughput growing, BTM backlog building, power
gen demand rising, gas prices supportive, LNG running near full. The
adj composite of {adj_composite:.2f} barely trails the market composite of {mkt_comp:.2f}.

This is the valuation paradox: observable signals confirm the bull
case, but the stock already prices it in at 37x trailing P/E. The
market composite of {mkt_comp:.2f} requires a sustained BULL/XBULL environment
for 2+ years just to deliver a 15%/yr return. One BULL-to-BASE step-
down — BTM timeline extends by a year, gas prices soften, interest
rates stay high — and the multiple derates from 37x toward 22-25x.
That repricing alone accounts for a 30-40% price decline with no
change in the underlying contracted business.

Watch: BTM backlog is the single variable that justifies the current
premium. A confirmed $5B+ backlog (XBULL threshold) with major
hyperscaler names attached would push the composite toward 3.5 and
begin to validate the 37x multiple. Anything below $2B would be a
material disappointment and trigger a rerating toward BASE multiples.
""")

sub("5.  How idiosyncratic is this bet? — what your research controls")
p(f"""
WMB scores {IDIO['idio_pct']}% idiosyncratic — similar to MSFT, and significantly
higher than MU (35%). The Transco monopoly and fee-based contracts
are company-specific anchors that do not disappear in a macro downturn.
The BTM data centre strategy is purely company-specific — no other
midstream operator has executed it at scale.

THE {IDIO['idio_pct']}% THAT IS YOURS TO GET RIGHT
─────────────────────────────────────
Transco expansion execution (20%): Three major projects — Southeast
  Supply Enhancement, Regional Energy Access, Gulf Coast Storage —
  are in execution. Cost overruns, FERC delays, or permitting
  setbacks are trackable through quarterly construction updates and
  FERC docket filings. This is researchable.

BTM data centre contract wins (20%): Hyperscaler identities and
  contract sizes are disclosed (or leaked) progressively. A $5B+
  committed backlog changes the investment thesis materially. Watch
  earnings call commentary on "power innovation" project count and
  MW capacity committed. This is the most important unknown.

Leverage management (15%): WMB targets Net Debt/EBITDA of 3.85-4x.
  With EBITDA growing 9%/yr, leverage should naturally decline. A
  credit downgrade or covenant stress would be idiosyncratic and
  researchable through quarterly balance sheet monitoring.

THE {IDIO['macro_pct']}% THAT MACRO CONTROLS
──────────────────────────────
Natural gas demand cycle (20%): The power generation shift from coal
  to gas is structural, but the rate of demand growth is
  macro-linked — industrial activity, heating degree-days, LNG
  export policy. These are not WMB-specific. A warm winter or
  weak industrial cycle dents throughput growth regardless of
  execution quality.

Interest rate sensitivity (15%): WMB carries ~$25B of long-term
  debt. With EBITDA of $7.75B, interest expense is material.
  A sustained higher-for-longer rate environment raises refinancing
  costs and compresses the EPS multiple that capital-intensive
  infrastructure companies command. Being right on BTM does not
  protect you from a 150bp rate rise.

Market beta (10%): At 0.90x beta, WMB tracks the market in risk-off
  episodes. Energy sector sentiment — particularly gas vs. oil — adds
  a further layer of non-fundamental price movement.

WHAT THIS MEANS FOR POSITION SIZING
The EPP floor (${epp_now:.0f}) is almost entirely idiosyncratic — Transco
and its contracts survive any reasonable macro scenario. But the
${dist_epp:.0f} premium above floor ({epp_gap_pct:.0f}% of price) is largely the AI
data centre option value, which requires both BTM execution AND a
macro environment that keeps gas-fired power attractive AND interest
rates that allow a 35x+ multiple to persist. The AVOID signal means:
the idiosyncratic upside does not compensate for the macro exposure
at current prices.
""")

# ─────────────────────────────────────────────────────────────────────────────
# PART 3  —  DATA TABLES
# ─────────────────────────────────────────────────────────────────────────────
section(f"PART 3  ·  {TICKER}  —  NUMBERS & SIGNALS",
        f"${CURRENT_PRICE:.2f}  ·  {DATE}  ·  Price source: Yahoo Finance")

print(f"""
  ┌{"─"*62}┐
  │  {SIGNAL:<20}  Ratio B {rfmt(ratio_B):<10}  (primary signal)        │
  │  EPP ${epp_now:.0f}  ({epp_gap_pct:+.0f}% gap)  ·  Fwd P/E {forward_pe:.0f}x  ·  Cons. {cons_ret_ann:+.0f}%/yr    │
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
  {"Signal":<32}  {"BEAR<":>6}  {"BASE":>8}  {"BULL":>8}  {"XBULL≥":>8}  {"NOW":>5}""")
print(SL)
for name, desc, unit, bc, blo, bulo, xlo, cur, w, sc in scored:
    u = unit.split()[0]
    def fmt(v): return f"${v}{u[1:]}" if u.startswith('$') else f"{v}{u}"
    print(f"  {name:<32}  {fmt(bc):>6}  {fmt(blo)}-{fmt(bulo):>4}  {fmt(bulo)}-{fmt(xlo):>4}  {fmt(xlo):>6}  {fmt(cur):>5}")

# EPP
print(f"""
  EPP FLOOR  (fee-based midstream — 16x trough multiple)
{SL}
  {"Year":<8}  {"EPS":>6}  {"× Trough P/E":>14}  {"EPP":>7}  {"Actual low":>12}""")
print(SL)
print(f"  {'FY2022':<8}  ${EPS_TROUGH:>5.2f}  {'× 16x':>14}  ${epp_trough_val:>5.0f}  {'$27  ✓':>12}")
print(f"  {'FY2025':<8}  ${EPS_NOW:>5.2f}  {'× 16x':>14}  ${epp_now:>5.0f}  {'—':>12}  ← today's floor")
print(SL)
print(f"  Floor migration +${epp_now - epp_trough_val:.0f} (+{(epp_now/epp_trough_val-1)*100:.0f}%)  — entirely EPS compounding, multiple unchanged")
print(f"  Current ${CURRENT_PRICE:.2f} is {epp_gap_pct:.0f}% above floor  ·  {(CURRENT_PRICE-epp_now)/sigma:.1f}σ to EPP")
print(f"  Bear ${sc_map['BEAR'][3]:.0f} is {bear_vs_epp:.0f}% vs floor  ← bear scenario breaks floor (EPS ${sc_map['BEAR'][1]:.2f})")

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
  {"Zone":<18}  {"Price":>14}  {"Ratio B":>9}  Action""")
print(SL)
print(f"  {'◉ EPP floor':<18}  {'$34 – $38':>14}  {'< 0.20x':>9}  Buy aggressively")
print(f"  {'◉ High conv.':<18}  {'$38 – $47':>14}  {'0.20–0.75x':>9}  Build position")
print(f"  {'◐ Watchlist':<18}  {'$47 – $55':>14}  {'0.75–1.1x':>9}  Monitor only")
print(f"  {'✕ Today':<18}  {f'~${CURRENT_PRICE:.0f}':>14}  {'N/A':>9}  Avoid / no initiation")
print(f"  {'✕ Fully priced':<18}  {'> $66':>14}  {'N/A':>9}  Trim if held")
print(SL)
print(f"  UPGRADE to ◐ WATCHLIST if:   BTM backlog confirmed >$5B  AND  forward P/E < 28x")
print(f"  UPGRADE to ◎ ACCUMULATE if:  Price retreats to $50-55 range (Ratio B ~0.75x)")
print(f"  MAINTAIN AVOID while:        BASE scenario (${sc_map['BASE'][3]:.0f}) is below current price")

print()
print(HL)
print(f"  {TICKER}  ·  {SIGNAL}  ·  Ratio B {rfmt(ratio_B)}  ·  EPP ${epp_now:.0f} ({epp_gap_pct:+.0f}%)  ·  Idio {IDIO['idio_pct']}% / Macro {IDIO['macro_pct']}%")
print(HL)
print()
