"""
ZAB  ·  Żabka Group S.A.  ·  WSE: ZAB
Bottom-up signal model  ·  MERGER ARBITRAGE SPECIAL SITUATION — Convenience Retail / Couche-Tard Tender Offer
Currency: PLN (Polish złoty) — this model is denominated natively in PLN, not USD
Date: 2026-08-03

⚠ IMPORTANT FRAMING NOTE: On 2026-07-31, Alimentation Couche-Tard (Circle K) announced a
  voluntary tender offer to acquire Żabka at 32.00 zł/share in cash, with ~57% of shares
  already committed via hard irrevocable tender agreements. This is no longer a standard
  growth-stock valuation exercise — it is a merger-arbitrage situation where the deal price
  is the dominant near-term price anchor. The usual ratio_b / EPP framework, built for
  open-ended growth distributions, is a structurally poor fit for a capped cash tender offer,
  and this model says so explicitly rather than letting a mechanical signal mislead.
"""

import math

# ── COMPANY CONSTANTS ─────────────────────────────────────────────────────────
TICKER        = "ZAB"
COMPANY       = "Żabka Group S.A."
SECTOR        = "Convenience Retail · Merger Arbitrage (Couche-Tard Tender Offer) · GPW: ZAB (PLN)"
CURRENT_PRICE = 31.64       # PLN; close 2026-07-31, the day the Couche-Tard tender offer was announced
VOL_52W_LOW   = 19.77       # PLN
VOL_52W_HIGH  = 33.88       # PLN
SHARES_OUT_M  = 997.42      # millions
ANNUAL_DIV    = 0.0         # PLN/share; no dividend — irrelevant in any case given the pending cash tender

# ── STANDALONE REVENUE BRIDGE (FY2026E, PLN billions) — for EPP/walk-away context only ──
# H1 2026 actual (standalone): revenue 14,666M zł (+14.7% YoY). Q2 2026: sales to end customers
# 9.2B zł (+13.2% YoY), adj EBITDA 1,228M zł (+16.2% YoY, margin 13.3% +30bps), adj net profit 366M zł
# (+66% YoY), free cash flow 1,214M zł (136.8% conversion), net debt/adj EBITDA improved to 0.7x
# (from 1.2x). Store network: 13,063 locations as of June 30, 2026 (+1,368 gross openings TTM).
# This bridge exists to establish what Żabka is worth AS A STANDALONE BUSINESS if the deal breaks —
# it is explicitly NOT the primary driver of the SCENARIOS table below, which is deal-outcome-driven.
SEG_DATA = [
    # (segment, curr_rev_B, description)
    ("Core Żabka convenience network (Poland)", 27.0, "13,063 stores; +14.7% H1 revenue growth, EBITDA margin expanding to 13.3%"),
    ("New formats & digital ventures (Jush!, delivery, nano-stores)", 3.0, "Smaller, earlier-stage growth initiatives layered on top of the core network"),
]
NET_MARGIN_STANDALONE = 0.0473  # FY2026E; reconciles to the bottom-up standalone EPS estimate below

# ── MERGER ARBITRAGE CALCULATOR (the ZAB-specific angle — read this section first) ──
DEAL_PRICE_PLN              = 32.00  # zł/share; Couche-Tard voluntary cash tender offer price
DEAL_VALUE_PLN_B            = 32.62  # PLN billions; total equity value of the offer
DEAL_VALUE_USD_B            = 8.6    # $ billions; approximate USD equivalent
SHAREHOLDER_LOCKUP_PCT      = 57     # % of shares committed via hard irrevocable tender agreements (CVC Capital Partners, Partners Group, management)
ARB_SPREAD_PCT              = round((DEAL_PRICE_PLN - CURRENT_PRICE) / CURRENT_PRICE * 100, 2)  # current spread to deal price
EXPECTED_MONTHS_TO_CLOSE    = 4      # rough estimate: subscription opens ~Aug 26 2026 pending KNF review; typical friendly-deal timeline
ARB_ANNUALIZED_RETURN_PCT   = round(ARB_SPREAD_PCT * (12 / EXPECTED_MONTHS_TO_CLOSE), 1)
PRE_ANNOUNCEMENT_CLOSE_PLN  = 29.26  # zł; prior close, the day before the deal was announced

# ── EPP (Earnings Power Price) — standalone, walk-away basis ─────────────────
EPS_FY2026E    = 1.42        # PLN/share FY2026E; bottom-up standalone estimate (H1 actual + realistic H2 continuation)
PE_PESSIMISTIC = 16.0        # trough P/E: a genuine convenience-retail-trough multiple, absent any deal premium
EPP            = round(PE_PESSIMISTIC * EPS_FY2026E, 0)

vol_pct     = (CURRENT_PRICE - VOL_52W_LOW) / (VOL_52W_HIGH - VOL_52W_LOW)
epp_gap_pct = round((CURRENT_PRICE - EPP) / EPP * 100, 1)

# ── SCENARIO TABLE (deal-outcome-driven, NOT a standard 2-yr fundamental distribution) ──
# EPS is held roughly flat across scenarios deliberately: over the deal's short expected timeline,
# standalone earnings power barely moves — what moves is whether a cash buyer is paying 32.00 zł/share
# for it. The "P/E" column below is a display convenience (price ÷ EPS), not a genuine valuation lever.
SCENARIOS = {
    "BEAR":  (1.42, 16.2,  23, "The deal breaks (regulatory rejection, financing failure, or withdrawal); the stock reverts below its pre-announcement level on disappointment and process-risk overhang"),
    "BASE":  (1.42, 22.5,  32, "The tender offer closes essentially as announced at 32.00 zł/share — the modal outcome given the 57% shareholder lock-up"),
    "BULL":  (1.42, 23.2,  33, "The deal closes at 32.00 zł with a small bump, or minor deal-sweetening emerges during the KNF review process"),
    "XBULL": (1.42, 28.2,  40, "A rival bidder emerges with a topping bid — real but low-probability once a majority of shares are already locked up"),
}

# ── SOFTMAX PROBABILITY FUNCTION ─────────────────────────────────────────────
CENTERS = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}
T = 0.60

def softmax_probs(c):
    raw = {s: math.exp(-abs(c - CENTERS[s]) / T) for s in CENTERS}
    tot = sum(raw.values())
    return {s: raw[s] / tot for s in raw}

def expected_value(c):
    p = softmax_probs(c)
    return sum(p[s] * SCENARIOS[s][2] for s in SCENARIOS)

def back_solve_market_composite(price, tol=0.001):
    target = price * (1.15 ** 2)
    lo, hi = 1.0, 4.0
    for _ in range(80):
        m = (lo + hi) / 2
        if expected_value(m) < target:
            lo = m
        else:
            hi = m
    return round((lo + hi) / 2, 2)

# ── 6 PROXY SIGNALS ───────────────────────────────────────────────────────────
# Scores: 1=BEAR  2=BASE  3=BULL  4=XBULL
SIGNALS = [
    {
        "name":       "Shareholder lock-up commitment",
        "weight":     0.25,
        "thresholds": ("<30%",   "≥40%",   "≥50%",   "≥60%"),
        "now":        "57%",
        "score":      3,
        "comment":    "CVC Capital Partners and Partners Group have entered hard irrevocable agreements to tender — unusually strong commitment this early",
    },
    {
        "name":       "Regulatory approval status",
        "weight":     0.15,
        "thresholds": ("blocked", "under review","on track","cleared"),
        "now":        "on track",
        "score":      3,
        "comment":    "KNF (Polish Financial Supervision Authority) reviewing the tender document; subscription expected to open ~Aug 26",
    },
    {
        "name":       "Standalone H1 2026 revenue growth",
        "weight":     0.15,
        "thresholds": ("<5%",    "≥9%",    "≥12%",   "≥15%"),
        "now":        "+14.7%",
        "score":      3,
        "comment":    "The underlying business would likely hold up reasonably well even if the deal broke",
    },
    {
        "name":       "Standalone adj. EBITDA margin trend",
        "weight":     0.15,
        "thresholds": ("declining","flat",   "improving","expanding fast"),
        "now":        "improving (+30bps)",
        "score":      3,
        "comment":    "Genuine operational momentum independent of the deal — a real walk-away value floor",
    },
    {
        "name":       "Arb spread (annualized)",
        "weight":     0.15,
        "thresholds": ("<0%",    "≥2%",    "≥4%",    "≥7%"),
        "now":        f"~{ARB_ANNUALIZED_RETURN_PCT:.1f}%",
        "score":      3,
        "comment":    "A modest but reasonable annualized spread for a deal with this much shareholder commitment already locked in",
    },
    {
        "name":       "Standalone forward P/E (walk-away risk)",
        "weight":     0.15,
        "thresholds": (">28x",   "≤25x",   "≤22x",   "≤18x"),
        "now":        "~22.3x",
        "score":      2,
        "comment":    "The standalone multiple is already close to the deal price — limited premium is being paid for the walk-away scenario specifically",
    },
]

assert abs(sum(s["weight"] for s in SIGNALS) - 1.0) < 0.001

PROXY_COMPOSITE = sum(s["score"] * s["weight"] for s in SIGNALS)

# ── STRUCTURAL COMPOSITE ADJUSTMENT (SCA) ─────────────────────────────────────
SCA_FACTORS = [
    ("+", "~57% of shares already committed via hard irrevocable tender agreements from sophisticated holders is unusually strong deal certainty this early in the process", +0.5, 0.25),
    ("+", "Couche-Tard is a large, well-capitalized strategic acquirer with no direct Polish convenience-retail overlap, minimizing antitrust risk", +0.3, 0.15),
    ("-", "KNF regulatory review is still pending and subscription hasn't formally opened — real, if modest, process risk remains", -0.3, 0.15),
    ("+", "Standalone Q2 2026 results (revenue +13.2%, adj EBITDA +16.2%, adj net profit +66%) show the business would likely hold up reasonably well even if the deal broke", +0.3, 0.15),
    ("-", "The capped, cash-tender structure means there is essentially no upside beyond ~32 zł barring a rival bid — this is a return-of-capital-plus-modest-spread trade, not a growth investment", -0.4, 0.15),
    ("-", "A rival bidder emerging is a real but low-probability scenario given the majority-shareholder lock-up already in place", -0.2, 0.15),
]
SCA = sum(score * weight for _, _, score, weight in SCA_FACTORS)
ADJ_COMPOSITE = round(PROXY_COMPOSITE + SCA, 3)

MARKET_COMPOSITE = back_solve_market_composite(CURRENT_PRICE)
ADJ_GAP = round(ADJ_COMPOSITE - MARKET_COMPOSITE, 2)

if ADJ_GAP > 0.20:
    valuation_label = "UNDERVALUED"
elif ADJ_GAP > -0.20:
    valuation_label = "FAIRLY VALUED"
else:
    valuation_label = "OVERVALUED"

# ── RATIO B ───────────────────────────────────────────────────────────────────
bear_price   = SCENARIOS["BEAR"][2]
bull_price   = SCENARIOS["BULL"][2]
downside_pct = (CURRENT_PRICE - bear_price) / CURRENT_PRICE
upside_pct   = (bull_price - CURRENT_PRICE) / CURRENT_PRICE
ratio_b      = round(downside_pct / upside_pct, 2) if upside_pct > 0 else float("inf")

if ratio_b != float("inf") and ratio_b < 0.75:
    signal_short, signal_full = "BUY",       "◉ BUY"
elif ratio_b != float("inf") and ratio_b < 1.10:
    signal_short, signal_full = "ACCUMULATE","◎ ACCUMULATE"
elif ratio_b != float("inf") and ratio_b < 1.75:
    signal_short, signal_full = "WATCHLIST", "◐ WATCHLIST"
else:
    signal_short, signal_full = "AVOID",     "✕ AVOID"

ratio_b_str = f"{ratio_b:.2f}x" if ratio_b != float("inf") else "N/A"

# ── CONSERVATIVE GROWTH (2-yr) ────────────────────────────────────────────────
# Note: for a merger-arb situation, "conservative growth" is a less meaningful frame than the
# arb spread itself — shown here for template consistency, using the standalone walk-away basis.
CONS_EPS_2YR  = 1.60    # PLN; conservative standalone FY2028E if the deal breaks and no re-rating occurs
CONS_PE_2YR   = 18      # a modest standalone multiple, no deal premium
cons_equity   = CONS_EPS_2YR * CONS_PE_2YR
cons_divs     = ANNUAL_DIV * 2
cons_total    = cons_equity + cons_divs
cons_return   = round((cons_total - CURRENT_PRICE) / CURRENT_PRICE * 100, 1)
cons_annual   = round(cons_return / 2, 1)

# ─────────────────────────────────────────────────────────────────────────────
#  OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
W = 72

def hr(): print("  " + "─" * W)
def bar(score):
    return "█" * score + "░" * (4 - score)

print()
print("═" * (W + 4))
print(f"  {TICKER}  ·  {COMPANY}  ·  {CURRENT_PRICE:.2f} zł  ·  MERGER ARBITRAGE (Couche-Tard tender @ {DEAL_PRICE_PLN:.2f} zł)")
print(f"  Signal: {signal_full}   Ratio B: {ratio_b_str}   Adj gap: {ADJ_GAP:+.2f}  [{valuation_label}]  (all figures in PLN)")
print("═" * (W + 4))
print(f"  ⚠  This is a merger-arbitrage special situation, not a standard growth-stock valuation.")
print(f"     The signal/ratio_b below is mechanically computed but is a POOR fit for a capped cash")
print(f"     tender — see the MERGER ARBITRAGE CALCULATOR section for the decision-relevant framing.")

# ─── ① MERGER ARBITRAGE CALCULATOR (read this first) ──────────────────────────
print()
print("  MERGER ARBITRAGE CALCULATOR  (the ZAB-specific angle — read this section first)")
hr()
print(f"  Deal price (Couche-Tard cash tender):    {DEAL_PRICE_PLN:.2f} zł/share")
print(f"  Total deal value:                         {DEAL_VALUE_PLN_B:.2f}B zł  (~${DEAL_VALUE_USD_B:.1f}B USD)")
print(f"  Shareholder lock-up (hard irrevocables):  {SHAREHOLDER_LOCKUP_PCT}%  (CVC Capital Partners, Partners Group, management)")
print(f"  Current price vs deal price:              {CURRENT_PRICE:.2f} zł  →  {DEAL_PRICE_PLN:.2f} zł")
print(f"  Arb spread:                               {ARB_SPREAD_PCT:.2f}%")
print(f"  Expected months to close (estimate):      ~{EXPECTED_MONTHS_TO_CLOSE}  (subscription opens ~Aug 26, pending KNF review)")
print(f"  Annualized arb return (estimate):         ~{ARB_ANNUALIZED_RETURN_PCT:.1f}%/yr")
print(f"  Pre-announcement close (2026-07-30):       {PRE_ANNOUNCEMENT_CLOSE_PLN:.2f} zł")
hr()
print(f"  THIS is the number that matters: a ~{ARB_SPREAD_PCT:.1f}% spread to close, annualizing to roughly")
print(f"  {ARB_ANNUALIZED_RETURN_PCT:.1f}%/yr if the deal closes on a normal friendly-merger timeline. That's a modest,")
print(f"  relatively low-risk return for a deal with {SHAREHOLDER_LOCKUP_PCT}% of shares already irrevocably committed —")
print(f"  not a growth investment, and not what the mechanical BEAR/BULL scenario table below is really about.")

# ─── ② STANDALONE WALK-AWAY VALUE (EPP basis) ─────────────────────────────────
print()
print("  STANDALONE WALK-AWAY VALUE  (what Żabka is worth if the deal breaks — informational only)")
hr()
curr_total = sum(rev for _, rev, _ in SEG_DATA)
print(f"  {'Segment':<48}  {'FY26E (B zł)':>13}")
hr()
for seg, curr, desc in SEG_DATA:
    print(f"  {seg:<48}  {curr:>11.1f}")
    print(f"    {desc}")
hr()
print(f"  {'TOTAL':<48}  {curr_total:>11.1f}")
print(f"  H1 2026 actual: 14,666M zł revenue (+14.7% YoY); Q2 adj EBITDA margin 13.3% (+30bps)")
print()

shares    = SHARES_OUT_M / 1000
curr_net  = curr_total * NET_MARGIN_STANDALONE
curr_eps  = round(curr_net / shares, 2)
print(f"  Standalone FY2026E EPS check:  {curr_total:.1f}B zł rev × {NET_MARGIN_STANDALONE*100:.2f}% net margin")
print(f"  ÷ {shares:.5f}B shares  =  {curr_eps:.2f} zł/share  (model estimate {EPS_FY2026E:.2f} zł  ✓)")
print()
print(f"  EPP floor (pessimistic {PE_PESSIMISTIC:.0f}× × standalone EPS):  {EPP:.0f} zł/share  ({epp_gap_pct:+.1f}% vs current price)")
print(f"  This is the genuine walk-away floor — notably, it sits meaningfully below both the current")
print(f"  price and the deal price, which is exactly why the tender offer is attractive to shareholders")
print(f"  and why the 57% lock-up came together as quickly as it did.")

# KEY SENSITIVITIES
print()
print(f"  KEY SENSITIVITIES (deal-outcome, not fundamental):")
print(f"  Every 1pp change in deal-completion probability:  ~{(DEAL_PRICE_PLN-EPP)/100*997.42:.0f}M zł of aggregate shareholder value")
print(f"  Every 1-month change in expected time-to-close:    ~{ARB_ANNUALIZED_RETURN_PCT/EXPECTED_MONTHS_TO_CLOSE:.1f}pp of annualized arb return")

# ─── ③ SIGNAL DASHBOARD ───────────────────────────────────────────────────────
print()
print("  ① SIGNAL DASHBOARD  (lock-up / regulatory / standalone growth / margin / arb spread / walk-away P/E)")
hr()
score_labels = {1: "⚠ BEAR", 2: "◦ BASE", 3: "▲ BULL", 4: "★ XBULL"}
print(f"  {'Signal':<38}  {'BEAR':>7}  {'BASE':>7}  {'BULL':>7}  {'XBULL':>7}  {'NOW':>19}  Score")
hr()
for s in SIGNALS:
    ths = s["thresholds"]
    lbl = score_labels[s["score"]]
    b   = bar(s["score"])
    print(f"  {s['name']:<38}  {ths[0]:>7}  {ths[1]:>7}  {ths[2]:>7}  {ths[3]:>7}  {s['now']:>19}  {lbl}  {b}")
    print(f"    {s['comment']}")

print()
print(f"  Proxy composite:    {PROXY_COMPOSITE:.2f} / 4.00")
print(f"  Market composite:   {MARKET_COMPOSITE:.2f} / 4.00  (back-solved from {CURRENT_PRICE} zł + 15%/yr hurdle — structurally unreachable for a capped tender, see note below)")
print(f"  SCA adjustment:    {SCA:+.3f}  →  Adj composite {ADJ_COMPOSITE:.3f}  →  Gap {ADJ_GAP:+.2f}  [{valuation_label}]")
print()
print("  Structural factors:")
for sign, desc, score, weight in SCA_FACTORS:
    contribution = score * weight
    print(f"    {sign}  {desc[:88]:<88}  ({score:+.1f} × {weight*100:.0f}%  =  {contribution:+.3f})")
print()
print(f"  NOTE ON THE MARKET COMPOSITE: the back-solve target requires a 2yr, 15%/yr-squared return (~32%")
print(f"  cumulative) from the current price. A capped cash tender at {DEAL_PRICE_PLN:.2f} zł structurally CANNOT deliver")
print(f"  that from {CURRENT_PRICE:.2f} zł even in the XBULL scenario unless a real bidding war breaks out — this is a")
print(f"  correct, not degenerate, reflection of the situation, and the resulting '{valuation_label}' read should be")
print(f"  interpreted as 'this isn't a growth stock,' not as a genuine mispricing signal.")

# ─── ④ BEAR CASE ANATOMY ─────────────────────────────────────────────────────
print()
print(f"  ② BEAR CASE ANATOMY  (variables needed to reach BEAR {bear_price} zł — i.e., the deal breaking)")
hr()
print(f"  {'Signal':<32}  {'Current':>18}  {'Bear val':>18}  Trigger")
hr()
bear_triggers = [
    ("Shareholder lock-up",         "57% committed",     "irrevocables challenged","A legal challenge to the irrevocable agreements themselves — historically rare"),
    ("Regulatory approval",         "on track",          "blocked/delayed",  "KNF raises unexpected objections, or an antitrust issue emerges despite limited overlap"),
    ("Standalone revenue growth",   "+14.7%",            "<5%",               "A genuine standalone slowdown that also makes the walk-away scenario less attractive"),
    ("Standalone EBITDA margin",    "improving",         "declining",         "Cost inflation or competitive pressure erodes the margin gains achieved so far"),
    ("Minority tender participation","expected high",    "low",               "Retail/minority shareholders don't tender in sufficient numbers to reach the offer threshold"),
    ("Financing/MAC conditions",    "none disclosed",    "financing gap",     "An unexpected material-adverse-change or financing condition emerges (Couche-Tard is well-capitalized, making this unlikely)"),
]
for name, curr, bear_v, trigger in bear_triggers:
    print(f"  {name:<32}  {curr:>18}  {bear_v:>18}  {trigger[:40]}")

probs_proxy = softmax_probs(PROXY_COMPOSITE)
print()
print(f"  Bear probability (proxy model):  {probs_proxy['BEAR']*100:.1f}%")
print()
print(f"  KEY TRIGGER: with {SHAREHOLDER_LOCKUP_PCT}% of shares already irrevocably committed and a well-capitalized,")
print(f"  strategically-motivated acquirer with limited Polish market overlap, the realistic bear case is")
print(f"  narrower than a typical M&A situation — it concentrates almost entirely on the KNF regulatory")
print(f"  review, which has not yet concluded as of this model's date.")

# ─── ⑤ EPP ────────────────────────────────────────────────────────────────────
print()
print("  ③ EPP  (Earnings Power Price: pessimistic P/E × standalone forward EPS)")
hr()
print(f"  Standalone FY2026E EPS:      {EPS_FY2026E:.2f} zł  (bottom-up, H1 actual + realistic H2 continuation)")
print(f"  Pessimistic P/E at trough:   {PE_PESSIMISTIC:.0f}×  (a genuine convenience-retail-trough multiple, no deal premium)")
print(f"  ─────────────────────────────────────────────────────────────────────")
print(f"  EPP floor:    {EPP:.0f} zł/share")
print(f"  Current {CURRENT_PRICE:.2f} zł vs EPP {EPP:.0f} zł:  {epp_gap_pct:+.1f}%")
print()
print(f"  The deal price ({DEAL_PRICE_PLN:.2f} zł) sits {(DEAL_PRICE_PLN/EPP-1)*100:+.0f}% above this standalone EPP floor — a genuine, if")
print(f"  not enormous, premium for certainty and immediate liquidity versus continuing to hold a standalone")
print(f"  growth story that would otherwise need several more years to compound toward a similar value.")

# ─── ⑥ CONSERVATIVE GROWTH ────────────────────────────────────────────────────
print()
print("  ④ CONSERVATIVE GROWTH  (2-yr standalone basis — less relevant here than the arb spread itself)")
hr()
print(f"  Conservative standalone FY2028E EPS:  {CONS_EPS_2YR:.2f} zł")
print(f"  Conservative standalone exit P/E:      {CONS_PE_2YR}×  (no deal premium assumed)")
print(f"  Conservative standalone equity value:   {cons_equity:.2f} zł/share")
hr()
print(f"  Conservative 2yr total:      {cons_total:.2f} zł  ({'▼' if cons_total < CURRENT_PRICE else '▲'}{abs(cons_total-CURRENT_PRICE):.2f} from {CURRENT_PRICE:.2f} zł)")
print(f"  Conservative total return:   {cons_return:.1f}% over 2yr  =  {cons_annual:.1f}%/yr")
print()
print(f"  THE HONEST READ: this 2-year standalone framing is the WRONG lens for this situation — nobody")
print(f"  should be underwriting a 2-year standalone hold here. The actual decision is about the {EXPECTED_MONTHS_TO_CLOSE}-month")
print(f"  arb spread (~{ARB_ANNUALIZED_RETURN_PCT:.1f}%/yr annualized) versus the {SHAREHOLDER_LOCKUP_PCT}%-locked-up deal-completion odds.")

# ─── ⑦ VOLATILITY CONTEXT ─────────────────────────────────────────────────────
print()
print("  ⑤ VOLATILITY CONTEXT")
hr()
annual_vol  = 0.10  # deliberately low — merger-arb positions trade tightly around the deal price once announced
sigma_range = (round(CURRENT_PRICE * (1 - annual_vol), 2),
               round(CURRENT_PRICE * (1 + annual_vol), 2))
print(f"  52-week range:        {VOL_52W_LOW:.2f} – {VOL_52W_HIGH:.2f} zł  (stock at {vol_pct*100:.0f}th pct of 52W range)")
print(f"  Pre-deal vs post-deal: {PRE_ANNOUNCEMENT_CLOSE_PLN:.2f} zł (pre-announcement) → {CURRENT_PRICE:.2f} zł (current) → {DEAL_PRICE_PLN:.2f} zł (deal price)")
print(f"  Annual dividend:      0.00 zł/share  (irrelevant — cash tender supersedes any dividend consideration)")
print(f"  Expected volatility:  low (~{annual_vol*100:.0f}%) while the deal is pending — arb positions trade tightly around the deal price")
print(f"  A genuine deal-break would be a discontinuous, not gradual, repricing event — not well captured by a smooth vol assumption")
hr()
print(f"  → Subscription period expected to open ~Aug 26, 2026, pending KNF review of the tender document.")
print(f"  → KNF review progress and any competing-bid rumors are the leading indicators to watch.")
print(f"  → This is a merger-arb HOLD/accumulate-toward-deal-price situation, not a conventional {signal_short} call.")

# ─── ⑧ SCENARIO PROBABILITIES ─────────────────────────────────────────────────
print()
print("  ⑥ SCENARIO PROBABILITIES  (proxy model vs market-implied)")
hr()
probs_mkt = softmax_probs(MARKET_COMPOSITE)
print(f"  {'Scenario':<10}  {'Price':>7}  {'Proxy%':>7}  {'Market%':>8}  {'Gap':>7}  Description")
hr()
for s in ["BEAR","BASE","BULL","XBULL"]:
    pp  = probs_proxy[s] * 100
    pm  = probs_mkt[s]   * 100
    gap = pp - pm
    pr  = SCENARIOS[s][2]
    desc = SCENARIOS[s][3][:44]
    print(f"  {s:<10}  {pr:>6} zł  {pp:>6.1f}%  {pm:>7.1f}%  {gap:>+6.1f}pp  {desc}")

ev_adj = expected_value(ADJ_COMPOSITE)
ev_prx = expected_value(PROXY_COMPOSITE)
ev_mkt = expected_value(MARKET_COMPOSITE)
print()
print(f"  Adj EV: {ev_adj:.0f} zł  /  Proxy EV: {ev_prx:.0f} zł  /  Market EV: {ev_mkt:.0f} zł  /  Current: {CURRENT_PRICE:.0f} zł")
hr()
print(f"  Downside  (→ Bear {bear_price} zł):  {downside_pct*100:.1f}%")
print(f"  Upside    (→ Bull {bull_price} zł):  {upside_pct*100:.1f}%")
print(f"  Ratio B   :  {ratio_b_str}  (see framing note above — not the primary decision metric here)")
print(f"  Signal    :  {signal_full}  (mechanical; the REAL call is: hold/accumulate toward the {DEAL_PRICE_PLN:.2f} zł deal price)")
print()
print(f"  MARKET PRICING: at {CURRENT_PRICE:.2f} zł the stock trades {ARB_SPREAD_PCT:.2f}% below the announced deal price, with")
print(f"  {SHAREHOLDER_LOCKUP_PCT}% of shares already irrevocably committed to tender. The market is pricing high but not")
print(f"  certain deal-completion odds — appropriately, given the KNF review has not yet concluded.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
print()
print("═" * (W + 4))
print(f"  Key catalysts to watch:")
print(f"  (1) KNF (Polish Financial Supervision Authority) review conclusion and subscription opening (~Aug 26)")
print(f"  (2) Minority shareholder tender participation once the subscription period opens")
print(f"  (3) Any competing bid or regulatory objection — both currently low-probability but the real tail risks")
print(f"  (4) Deal closing timeline confirmation — the key input to the annualized arb-return calculation")
print(f"  (5) Standalone Q3 2026 results, relevant only if the deal breaks and the walk-away value matters")
print(f"  Merger arb: {ARB_SPREAD_PCT:.2f}% spread to {DEAL_PRICE_PLN:.2f} zł  (~{ARB_ANNUALIZED_RETURN_PCT:.1f}%/yr annualized, ~{EXPECTED_MONTHS_TO_CLOSE}mo estimated close)")
print(f"  Standalone EPP floor: {EPP:.0f} zł  |  Pessimistic P/E: {PE_PESSIMISTIC:.0f}×  |  Shareholder lock-up: {SHAREHOLDER_LOCKUP_PCT}%")
print("═" * (W + 4))
print()

# ── EXPORT ────────────────────────────────────────────────────────────────────
RESULT = {
    "ticker":            TICKER,
    "signal":            signal_full,
    "signal_short":      signal_short,
    "price":             CURRENT_PRICE,
    "epp_gap_pct":       epp_gap_pct,
    "ratio_b":           ratio_b if ratio_b != float("inf") else None,
    "ratio_b_fmt":       ratio_b_str,
    "adj_composite":     ADJ_COMPOSITE,
    "market_composite":  MARKET_COMPOSITE,
    "adj_gap":           ADJ_GAP,
    "valuation":         valuation_label,
    "cons_return_2yr":   cons_return,
    "deal_price":        DEAL_PRICE_PLN,
    "arb_spread_pct":    ARB_SPREAD_PCT,
}

if __name__ == "__main__":
    pass
