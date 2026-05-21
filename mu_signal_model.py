#!/usr/bin/env python3
"""
MU  ·  Micron Technology
BottomUp Risk/Reward Analyzer  —  three-part publication format

Part 1  FRAMEWORK LOGIC     what each concept means (reusable)
Part 2  MU CASE             narrative per section, only what matters
Part 3  NUMBERS & SIGNALS   pure data, no prose

Price: $728.90  (Yahoo Finance / WebSearch, 2026-05-21)
"""
import math

# ══════════════════════════════════════════════════════════════════════════════
# INPUTS
# ══════════════════════════════════════════════════════════════════════════════
TICKER        = "MU"
COMPANY       = "Micron Technology"
SECTOR        = "Memory Semiconductors · HBM / DRAM / NAND"
DATE          = "2026-05-21"
CURRENT_PRICE = 728.90    # Yahoo Finance / WebSearch 2026-05-21

EPS_TROUGH_YEAR  = 2022
EPS_TROUGH       = 9.14     # FY2022 non-GAAP (last conventional cycle peak; used as floor reference)
EPS_TROUGH_PRICE = 52.0     # Oct 2022 cycle low  ($9.14 × 6x = $54.8 ≈ actual $52 ✓)
EPS_NOW          = 21.18    # TTM non-GAAP (HBM supercycle peak)
EPS_Q2_FY2026    = 12.20    # quarterly — massive beat vs $8.60 consensus (+684% YoY)
EPS_Q3_FY2026_E  = 19.01    # quarterly estimate, due Jun 24 2026
EPS_FWD_CONSENSUS = 14.00   # FY2026E consensus full-year (stale vs quarterly run-rate)

EPP_MIN_PE      = 6.0       # cyclical memory floor: 6x validated ($9.14×6=$54.8≈$52 actual low ✓)
CONS_EPS_CAGR   = 0.30      # 30%/yr over 2 years (HBM-driven; conservative vs run-rate)
CONS_EXIT_PE    = 25.0      # conservative exit (HBM mid-cycle; memory never sustains 30x+)
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2

SCENARIOS = [
    # lbl, narrative, eps, pe, price
    ("BEAR",  "DRAM crash; HBM ramp miss; Samsung floods market",  6.00,  6,   36),
    ("BASE",  "HBM scales; DRAM mid-cycle; Samsung share stable",  22.00, 13,  286),
    ("BULL",  "HBM #2 leader; DRAM tight; AI CapEx unabated",      42.00, 17,  714),
    ("XBULL", "Memory super-cycle; HBM pricing power; EPS $65+",   65.00, 20, 1300),
]

CROSS_READS = [
    # name, what_it_tells_us, unit, bear_ceil, base_lo, bull_lo, xbull_lo, current, weight
    ("HBM revenue (annualised)",    "Core thesis: is HBM still growing?",    "$B ann.", 2,  4,  7, 10,  10, 0.30),
    ("DRAM ASP YoY",                "Memory pricing cycle position",         "% YoY",  0,  0, 30, 55,  54, 0.20),
    ("AI GPU shipments (qtly)",     "Demand signal for HBM pull-through",    "M units", 2,  4,  7, 10,   9, 0.20),
    ("Data centre CapEx YoY",       "Hyperscaler commitment to AI infra",    "% YoY",  5,  5, 20, 35,  40, 0.15),
    ("DRAM utilisation rate",       "Supply discipline vs demand health",    "%",      65, 65, 80, 90,  92, 0.10),
    ("NAND ASP YoY",                "NAND cycle — supplementary signal",     "% YoY", -5, -5, 10, 25,  18, 0.05),
]

STRUCTURAL_FACTORS = [
    ("HBM oligopoly — 3 suppliers globally (MU #3 gaining share)",  +1.5, 0.25),
    ("NVIDIA B200/B300 qualification locked in",                    +1.0, 0.20),
    ("Samsung HBM re-entry risk (pivoting to HBM4)",               -1.5, 0.25),
    ("Commodity cycle risk — DRAM/NAND still cyclical",            -1.0, 0.15),
    ("Customer concentration — NVIDIA ~40% of HBM revenue",        -0.8, 0.15),
]

# EPS_DECOMP uses structural/cyclical split (not real/inflation — appropriate for memory)
# Share = fraction of (EPS_NOW − EPS_TROUGH) attributed to each driver
# is_structural=True → structural compounding; False → cyclical/temporary
EPS_DECOMP = [
    ("HBM mix shift  (near-zero→$8B+ revenue)",  0.40,  True),
    ("Operating leverage  (scale + fab util.)",  0.30,  True),
    ("HBM capacity expansion  (1γ node ramp)",   0.10,  True),
    ("DRAM ASP recovery  (cycle pricing)",        0.20,  False),
    ("NAND recovery  (partial)",                  0.05,  False),
    ("Share buybacks  (count reduction)",         0.05,  True),
]
# Note: shares sum to >1 (1.10) — deliberate; reflects some driver overlap at peak cycle.
# We use these only for directional decomp, not strict accounting arithmetic.

# ── IDIOSYNCRATIC ASSESSMENT ──────────────────────────────────────────────────
IDIO = {
    "idio_pct": 35,    # % of return driver that is company/sector-specific
    "macro_pct": 65,   # % driven by macro sentiment / cycle / rates
    "beta": 1.35,
    "drivers": [
        # (factor, idio_or_macro, weight, description)
        ("HBM execution & yield ramp",       "IDIO",  0.20, "1γ node yields; NVIDIA qual retention"),
        ("Samsung HBM re-entry timing",      "IDIO",  0.15, "Competitive share shift; MU-specific risk"),
        ("NVIDIA customer concentration",    "IDIO",  0.10, "Binary: NVIDIA reallocates or diversifies"),
        ("DRAM memory cycle position",       "MACRO", 0.25, "Global supply/demand cycle; no control"),
        ("AI CapEx cycle (hyperscaler)",     "MACRO", 0.15, "Macro commitment to GPU infra"),
        ("Broad market beta  (1.35x)",       "MACRO", 0.15, "High-beta; amplifies risk-off moves"),
    ],
    "note": (
        "MU is primarily a macro/cycle bet. 65 cents of every dollar of return variance "
        "is driven by factors outside any analyst's fundamental control: memory pricing "
        "cycles, AI infrastructure CapEx commitments, and broad risk-off sentiment at "
        "a 1.35x beta. The HBM thesis is real and structural, but it is already embedded "
        "in both the EPS run-rate and the current P/E multiple. What your research can "
        "control is the Samsung risk (timing, yield), NVIDIA allocation visibility, and "
        "1γ node execution. These are meaningful — but they are 35%, not 65%."
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

dist_epp = CURRENT_PRICE - epp_now
price_A  = CURRENT_PRICE * (1 + (cons_eps_2yr / EPS_NOW - 1))
price_B  = cons_eps_2yr * CONS_EXIT_PE
price_C  = sc_map["BASE"][3]

ratio_A = dist_epp / (price_A - CURRENT_PRICE)
ratio_B = dist_epp / (price_B - CURRENT_PRICE)
# ratio_C: BASE scenario is below current price — negative ratio (AVOID by definition)
ratio_C_raw = (price_C - CURRENT_PRICE)
ratio_C = dist_epp / ratio_C_raw if ratio_C_raw > 0 else float('inf')

def rlabel(r):
    if r == float('inf') or r < 0: return "✕ AVOID"
    if r < 0.75:  return "◉ BUY"
    if r < 1.10:  return "◎ ACCUMULATE"
    if r < 1.75:  return "◐ WATCHLIST"
    if r < 2.50:  return "○ HOLD / TRIM"
    return              "✕ AVOID"

SIGNAL = rlabel(ratio_B)
adj_gap = adj_composite - mkt_comp if mkt_comp else 0

vol_pct = 0.45     # MU: historically volatile semiconductor; HBM beta
sigma   = CURRENT_PRICE * vol_pct

# EPS decomp: structural vs cyclical
eps_g_total     = EPS_NOW - EPS_TROUGH
structural_share = sum(sh for _, sh, is_s in EPS_DECOMP if is_s)
cyclical_share   = sum(sh for _, sh, is_s in EPS_DECOMP if not is_s)
# dollar approximation (normalised to 1.0 weight)
total_share = structural_share + cyclical_share
struct_dollar = eps_g_total * (structural_share / total_share)
cyclical_dollar = eps_g_total * (cyclical_share / total_share)


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

For cyclical businesses like memory semiconductors, we adapt the split
to structural versus cyclical: structural growth (HBM mix shift, fab
utilisation improvements) is durable; cyclical growth (DRAM/NAND ASP
recovery from a trough) reverses when the cycle turns. A floor built on
cyclical earnings is much less reliable than one built on structural ones.
""")

sub("Cross-read model")
p("""
We track 5-6 external signals that are observable before the company
reports, each mapped to a specific business driver. HBM revenue data
tells us whether the AI memory thesis is holding. DRAM ASP trends tell
us where we are in the memory cycle. AI GPU shipments tell us about
demand pull-through.

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
# PART 2  —  MU ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
section(f"PART 2  ·  {TICKER}  —  ANALYST COMMENTARY",
        f"{COMPANY}  ·  {SECTOR}  ·  {DATE}  ·  ${CURRENT_PRICE:.2f}")

print(f"""
  ┌{"─"*62}┐
  │  SIGNAL:  {SIGNAL:<20}  (primary: Ratio B {ratio_B:.2f}x)        │
  │  EPP floor ${epp_now:.0f}  ·  Gap {epp_gap_pct:+.0f}%  ·  Conservative return {cons_ret_ann:+.0f}%/yr  │
  └{"─"*62}┘""")

sub("1.  The worst EPP — when the floor was touched")
p(f"""
MU's EPP floor was tested in October 2022, when the stock hit $52 —
the bottom of the most severe memory down-cycle in a decade. At that
moment the company's FY2023 EPS was heading negative as DRAM oversupply
crushed pricing. The prior year (FY2022) had printed ${EPS_TROUGH:.2f} in
non-GAAP EPS, the last positive peak before the collapse.

The floor multiple for commodity memory is 6x. This is not a discount
— it is the empirical result of every memory down-cycle since 2000. A
6x trough P/E reflects what the market assigns when it believes the
cycle will eventually recover, but cannot say when. At 6x you are
paying for one year of normalised earnings with almost no optimism
embedded. The market applied exactly that logic in late 2022:
${EPS_TROUGH:.2f} × 6x = ${epp_trough_val:.0f}; the actual low was ${EPS_TROUGH_PRICE:.0f}. A 5% gap at
the point of maximum fear.

Why 6x and not 2x or 10x? Because even in the worst oversupply
episode, the market knows: (1) memory is a permanently growing TAM,
(2) the industry has consolidated to 3-4 players, and (3) the specific
company has survived every prior cycle. That survival optionality and
the structural TAM growth are what prevent the multiple from going
to zero — and what set the verified floor at 6x. The market implies
that once the cycle turns, earnings recovery is highly probable.
""")

sub("2.  What changed since 2022 — and is it structural?")
p(f"""
EPS has rebounded from the FY2022 baseline of ${EPS_TROUGH:.2f} to a TTM of
${EPS_NOW:.2f}. Q2 FY2026 alone printed ${EPS_Q2_FY2026:.2f} quarterly — a single quarter
worth 134% of the entire FY2022 annual EPS. Q3 FY2026 is estimated at
${EPS_Q3_FY2026_E:.2f}. This is not a pricing cycle recovery. It is a structural mix
shift driven by HBM (High Bandwidth Memory).

We decompose the gain into structural versus cyclical:

  ~{int(structural_share/total_share*100)}% structural (${struct_dollar:.2f}/shr):
    HBM mix shift — HBM revenue went from essentially zero to an $8B+
    annualised run-rate. HBM earns 3-4x the ASP of standard DRAM per bit
    and commands structurally higher gross margins (~55-60% vs ~35% DRAM).
    This is not pricing — it is product architecture. Once an AI GPU is
    designed around HBM, the memory supplier is locked in for that
    platform generation. Operating leverage and 1γ node cost reductions
    amplify EPS further.

  ~{int(cyclical_share/total_share*100)}% cyclical (${cyclical_dollar:.2f}/shr):
    DRAM ASP recovery (+54% YoY) and partial NAND recovery. These are
    real but cycle-dependent. DRAM pricing will mean-revert if supply
    discipline breaks. NAND has shown less structural improvement —
    it remains a more commoditised, oversupplied market.

Verdict: the EPS floor has structurally risen — but only the HBM
component is durable at a higher floor multiple. The current EPP of
${epp_now:.0f} (${EPS_NOW:.2f} × 6x) is conservative precisely because it uses the
6x cyclical multiple against peak-cycle TTM EPS. In reality, the HBM
portion of earnings deserves a higher multiple and the DRAM/NAND
portion deserves a lower one. The blended 6x is deliberately cautious.
""")

sub("3.  How likely is a return below the EPP floor?")
p(f"""
At ${CURRENT_PRICE:.2f} the stock is ${dist_epp:.0f} ({epp_gap_pct:.0f}%) above the current floor
of ${epp_now:.0f}. The floor itself is the least likely breach — the concern
is the 83% of price sitting above it.

For the floor to break, EPS must fall below the FY2022 trough of
${EPS_TROUGH:.2f}. That requires a down-cycle worse than 2022-2023, when EPS
went negative. Possible — memory cycles are severe — but the HBM
structural floor limits how far EPS can fall now. Even in a severe
DRAM/NAND crash, HBM revenue continues as long as AI CapEx holds.
The BEAR scenario captures this: EPS falls to ${sc_map['BEAR'][1]:.2f} (positive,
not negative), × 6x = ${sc_map['BEAR'][3]:.0f}. The bear scenario breaks the floor by ${abs(sc_map['BEAR'][3] - epp_now):.0f} (
{abs(bear_vs_epp):.0f}% below current EPP), which would require HBM revenue to
simultaneously collapse at the same time DRAM oversupply hits.

The paradox is not the floor — it is the premium. ${dist_epp:.0f} of the
current ${CURRENT_PRICE:.2f} price (83%) sits above the EPP. That premium is
entirely the market pricing in continued HBM supercycle execution,
ongoing DRAM tightness, and sustained AI CapEx. All three of those are
macro or semi-macro cycle calls, not fundamental company analysis.

Our model: {proxy_probs['BEAR']*100:.0f}% BEAR probability. Market implies {mkt_probs.get('BEAR',0)*100:.0f}%.
The AVOID signal is not because the bear scenario is likely — it is
because even the BASE scenario (EPS ${sc_map['BASE'][1]:.2f} × {sc_map['BASE'][2]}x = ${sc_map['BASE'][3]:.0f}) is
-${CURRENT_PRICE - sc_map['BASE'][3]:.0f} below today's price. To make money from here you need
the BULL or XBULL scenario to materialise. Both are possible. Neither
is worth the premium at current price when there is no margin of safety.
""")

sub("4.  Cross-read model — observable score vs market-implied score")
p(f"""
Six signals are tracked and scored 1-4 before each quarter report.
The weighted composite tells us what the observable environment is
consistent with. We back-solve the composite the current stock price
requires to deliver a 15% annual hurdle rate — that is the market's
implied score.

  Signal                          Score (1-4)   Weight   Current reading
  HBM revenue (annualised)        XBULL (4/4)    30%    $10B ann. — above $7B BULL threshold
  DRAM ASP YoY                    BULL  (3/4)    20%    +54% — just below 55% XBULL threshold
  AI GPU shipments (qtly)         BULL  (3/4)    20%    ~9M units — just below 10M XBULL threshold
  Data centre CapEx YoY           XBULL (4/4)    15%    +40% — above 35% XBULL threshold
  DRAM utilisation rate           XBULL (4/4)    10%    92% — above 90% XBULL threshold
  NAND ASP YoY                    BULL  (3/4)     5%    +18% — between 10% BULL / 25% XBULL

Raw proxy composite:     {proxy_composite:.2f} / 4.00  (BULL/XBULL blend; strong across all signals)
Structural adj (SCA):   {sca:+.2f}  (HBM moat + NVIDIA qual vs Samsung re-entry + concentration)
Adjusted composite:      {adj_composite:.2f} / 4.00

Market-implied composite: {mkt_comp:.2f}  — the score embedded in ${CURRENT_PRICE:.2f} at 15%/yr

Gap: {adj_gap:+.2f} composite points.

This is the cycle peak paradox. Every observable signal is at or near
XBULL. The cross-read model returns a composite of {proxy_composite:.2f}/4.00 —
maximum excitement, all cylinders firing. And the stock is priced for
exactly that: at {trailing_pe:.1f}x TTM earnings, the market is not discounting
the current quarter — it is pricing in continued HBM dominance, AI
demand, and DRAM tightness for the next 2 years.

The gap of only {adj_gap:+.2f} means: our model agrees with the market's
optimism. There is no mispricing. There is no margin of safety. The
stock is fair value to slightly expensive relative to the BULL/XBULL
scenario that is already embedded in the price. When all signals are
XBULL and the stock already prices it in, the signal is not BUY —
it is AVOID.

Watch: Samsung HBM4 yield progress is the single most important signal
to monitor. An SK Hynix or Samsung recapture of HBM share would hit MU
disproportionately — market share loss in a product commanding 3x
standard ASP compresses earnings faster than the headline implies.
""")

sub("5.  How idiosyncratic is this bet? — what your research controls")
p(f"""
MU scores {IDIO['idio_pct']}% idiosyncratic: only {IDIO['idio_pct']} cents of every dollar of
return variance comes from factors you can research and have a view on.
The remaining {IDIO['macro_pct']}% is driven by the memory cycle, AI infrastructure
CapEx commitments, and broad market sentiment — macro forces that
outweigh company execution in determining the stock price.

For context: ISRG (62% idio) is a company where fundamental research
creates most of the edge. MU (35% idio) is a company where being right
on the cycle and the macro matters more than knowing the company well.

THE {IDIO['idio_pct']}% THAT IS YOURS TO GET RIGHT
─────────────────────────────────────
HBM execution (20%): 1γ node HBM3E and HBM4 ramp yields are
  trackable through quarterly gross margin data and management guidance.
  NVIDIA qualification retention is knowable — watch NVIDIA's supply
  chain calls for mention of second-source HBM vs MU allocation.

Samsung re-entry timing (15%): Samsung's pivot from HBM3E to HBM4
  is public information. Their yield progress on HBM4 is the most
  consequential company-specific risk. If Samsung ships HBM4 at scale
  in H2 2026, MU's HBM share erodes from 24% toward 15-18%. That cuts
  $2-4 from EPS directly — before any cycle effects.

NVIDIA concentration (10%): ~40% of MU's HBM revenue flows through
  one customer. An architectural shift (e.g. NVIDIA moving to in-house
  HBM or shifting allocation to SK Hynix) is binary and researchable.
  Watch NVIDIA's HBM supply disclosures on earnings calls.

THE {IDIO['macro_pct']}% THAT MACRO CONTROLS
──────────────────────────────
Memory cycle (25%): DRAM pricing is set by global supply/demand
  dynamics across Samsung, SK Hynix, and MU collectively. No amount of
  MU-specific research predicts when Samsung decides to expand capacity
  or when enterprise DRAM demand weakens. This is the biggest source of
  uncontrollable variance.

AI CapEx cycle (15%): Microsoft, Google, Amazon, and Meta collectively
  determine whether AI infrastructure spend continues at 35-40% YoY
  growth. A CFO-level pullback or CapEx rationalisation quarter collapses
  HBM demand without any change in MU's execution.

Market beta (15%): At 1.35x beta, MU amplifies S&P moves by 35%.
  In a risk-off episode, MU sells off faster than the index — even if
  HBM revenue is hitting records. The 2022 parallel: EPS was fine through
  Q1 2022; the stock fell 60% because macro repriced all semis.

WHAT THIS MEANS FOR POSITION SIZING
The EPP floor (${epp_now:.0f}) represents only {epp_now/CURRENT_PRICE*100:.0f}% of today's price.
The other {epp_gap_pct:.0f}% is premium that requires both the HBM thesis to
hold AND the macro cycle to cooperate. With 65% of return variance
macro-driven and the stock priced for maximum optimism, position
sizing should reflect that this is primarily a cycle bet with a
company-specific HBM option embedded. The AVOID signal means:
do not initiate. If held, the question is whether the BULL scenario
is more than 40% probable — and at current price, you need it to be.
""")

# ─────────────────────────────────────────────────────────────────────────────
# PART 3  —  DATA TABLES
# ─────────────────────────────────────────────────────────────────────────────
section(f"PART 3  ·  {TICKER}  —  NUMBERS & SIGNALS",
        f"${CURRENT_PRICE:.2f}  ·  {DATE}  ·  Price source: Yahoo Finance")

# Signal card
print(f"""
  ┌{"─"*62}┐
  │  {SIGNAL:<20}  Ratio B {ratio_B:.2f}x  (primary signal)             │
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
print(f"  SCA {sca:+.2f}  →  adj composite {adj_composite:.2f}  →  verdict: CYCLE PEAK / FAIRLY PRICED")

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
  EPP FLOOR  (cyclical memory — 6x trough multiple)
{SL}
  {"Year":<8}  {"EPS":>6}  {"× Trough P/E":>14}  {"EPP":>7}  {"Actual low":>12}""")
print(SL)
print(f"  {'FY2022':<8}  ${EPS_TROUGH:>5.2f}  {'× 6x':>14}  ${epp_trough_val:>5.0f}  {'$52  ✓':>12}")
print(f"  {'TTM2026':<8}  ${EPS_NOW:>5.2f}  {'× 6x':>14}  ${epp_now:>5.0f}  {'—':>12}  ← today's floor")
print(SL)
print(f"  Floor migration +${epp_now - epp_trough_val:.0f} (+{(epp_now/epp_trough_val-1)*100:.0f}%)  — EPS compounding + HBM structural shift")
print(f"  Current ${CURRENT_PRICE:.2f} is {epp_gap_pct:.0f}% above floor  ·  {(CURRENT_PRICE-epp_now)/sigma:.1f}σ to EPP")
print(f"  Bear ${sc_map['BEAR'][3]:.0f} is {bear_vs_epp:.0f}% vs floor  ← bear scenario breaks floor (EPS ${sc_map['BEAR'][1]:.2f})")

# EPS quality / structural decomp
print(f"""
  EPS DECOMP  (FY{EPS_TROUGH_YEAR} ${EPS_TROUGH:.2f} → TTM ${EPS_NOW:.2f};  +{(EPS_NOW/EPS_TROUGH-1)*100:.0f}%;
               structural/cyclical split for memory — not real/inflation)
{SL}
  {"Driver":<42}  {"Share":>7}  Type""")
print(SL)
for driver, share, is_struct in EPS_DECOMP:
    tag = "STRUCTURAL ✓" if is_struct else "CYCLICAL  ~"
    print(f"  {driver:<42}  {share*100:>6.0f}%  {tag}")
print(SL)
print(f"  Structural ~{int(structural_share/total_share*100)}%  (${struct_dollar:.2f}/shr)     Cyclical ~{int(cyclical_share/total_share*100)}%  (${cyclical_dollar:.2f}/shr)")
print(f"  NOTE: shares sum >100% due to driver overlap at peak cycle — directional only")

# Scenarios
print(f"""
  SCENARIOS  (2-year;  May 2026 → May 2028)
{SL}
  {"Scenario":<8}  {"EPS":>7}  {"P/E":>5}  {"Price":>7}  {"vs now":>7}  {"Proxy%":>7}  {"Mkt%":>6}  Narrative""")
print(SL)
for lbl, narr, eps, pe, price in SCENARIOS:
    pp = proxy_probs[lbl]
    mp = mkt_probs.get(lbl, 0)
    vs_now = (price - CURRENT_PRICE) / CURRENT_PRICE * 100
    print(f"  {lbl:<8}  ${eps:>6.2f}  {pe:>4}x  ${price:>6}  {vs_now:>+6.0f}%  {pp*100:>6.1f}%  {mp*100:>5.1f}%  {narr[:30]}")
print(SL)
print(f"  Proxy EV ${proxy_ev:.0f}  ·  Market needs ${mkt_ev:.0f} to justify ${CURRENT_PRICE:.2f} at {REQUIRED_RETURN*100:.0f}%/yr")
print(f"  BASE (${sc_map['BASE'][3]:.0f}) is -{CURRENT_PRICE - sc_map['BASE'][3]:.0f} below today  ←  even base case implies loss from current price")

# Attractiveness ratio
print(f"""
  ATTRACTIVENESS RATIO  (downside to EPP ${dist_epp:.0f}  =  {dist_epp/CURRENT_PRICE*100:.0f}% of price)
{SL}
  {"Method":<34}  {"2yr Target":>11}  {"Upside":>8}  {"Ratio":>7}  Signal""")
print(SL)
print(f"  {'A: Same P/E  ({:.1f}x trailing)'.format(trailing_pe):<34}  ${price_A:>9.0f}  {(price_A-CURRENT_PRICE)/CURRENT_PRICE*100:>+7.0f}%  {ratio_A:>6.2f}x  {rlabel(ratio_A)}")
print(f"  {'B: Conserv exit 25x  ← PRIMARY':<34}  ${price_B:>9.0f}  {(price_B-CURRENT_PRICE)/CURRENT_PRICE*100:>+7.0f}%  {ratio_B:>6.2f}x  {rlabel(ratio_B)}")
_c_str = f"${price_C:.0f}  (BASE below price)" if ratio_C_raw <= 0 else f"${price_C:.0f}"
print(f"  {'C: BASE scenario':<34}  {_c_str:>11}  {(price_C-CURRENT_PRICE)/CURRENT_PRICE*100:>+7.0f}%  {'N/A':>7}  {rlabel(ratio_C)}")

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
epp_plus_10 = epp_now * 1.10
epp_plus_20 = epp_now * 1.20
epp_plus_40 = epp_now * 1.40
print(f"""
  ENTRY FRAMEWORK
{SL}
  {"Zone":<18}  {"Price":>14}  {"Ratio B (approx)":>18}  Action""")
print(SL)
print(f"  {'◉ EPP floor':<18}  {'$127 – $140':>14}  {'< 0.10x':>18}  Buy aggressively")
print(f"  {'◉ Deep value':<18}  {'$140 – $250':>14}  {'0.10–0.50x':>18}  Build position")
print(f"  {'◐ Watchlist':<18}  {'$450 – $580':>14}  {'1.1–1.75x':>18}  Monitor only")
print(f"  {'✕ Today':<18}  {f'~${CURRENT_PRICE:.0f}':>14}  {f'{ratio_B:.2f}x':>18}  Avoid / no initiation")
print(f"  {'✕ Fully priced':<18}  {'> $700':>14}  {'> 3.5x':>18}  Trim if held")
print(SL)
print(f"  UPGRADE to ◎ ACCUMULATE if:  Samsung HBM4 yields disappoint AND DRAM stays tight")
print(f"  UPGRADE to ◉ BUY if:         DRAM down-cycle hits; price falls to $200-$300 range")
print(f"  MAINTAIN AVOID while:        BASE scenario (${sc_map['BASE'][3]:.0f}) is below current price")

print()
print(HL)
print(f"  {TICKER}  ·  {SIGNAL}  ·  Ratio B {ratio_B:.2f}x  ·  EPP ${epp_now:.0f} ({epp_gap_pct:+.0f}%)  ·  Idio {IDIO['idio_pct']}% / Macro {IDIO['macro_pct']}%")
print(HL)
print()
