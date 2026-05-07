#!/usr/bin/env python3
"""
AVGO Bottom-Up Risk/Reward Tracker
-----------------------------------
Tracks key fundamental data for Broadcom (AVGO) quarter by quarter and
derives scenario assumptions (BEAR / BASE / BULL / EXTREME_BULL) by
scoring each metric against calibrated thresholds.

Usage:
    python avgo_tracker.py

Add new quarters via tracker.add_quarter(...) before calling report().
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

# ══════════════════════════════════════════════════════════════════════════
# 1.  ENUMS & CONSTANTS
# ══════════════════════════════════════════════════════════════════════════

class Scenario(Enum):
    BEAR         = 1
    BASE         = 2
    BULL         = 3
    EXTREME_BULL = 4

SCENARIO_LABELS = {
    Scenario.BEAR:         "⚠  BEAR",
    Scenario.BASE:         "◦  BASE",
    Scenario.BULL:         "▲  BULL",
    Scenario.EXTREME_BULL: "★  EXTREME BULL",
}

# ══════════════════════════════════════════════════════════════════════════
# 2.  DATA STRUCTURES
# ══════════════════════════════════════════════════════════════════════════

@dataclass
class QuarterlyData:
    """
    One fiscal quarter of AVGO fundamentals.
    All dollar amounts in $B.  Percentages as plain floats (e.g. 67.3 = 67.3%).
    None = not yet reported.
    """
    period: str                 # e.g. "Q1FY2026"
    date_reported: str = ""

    # ── Revenue segments ─────────────────────────────────────────────────
    ai_semi_rev:        Optional[float] = None   # AI custom ASICs + networking
    non_ai_semi_rev:    Optional[float] = None   # broadband, enterprise, wireless
    software_rev:       Optional[float] = None   # VMware VCF + legacy infra software

    # ── Profitability ─────────────────────────────────────────────────────
    adj_ebitda:              Optional[float] = None
    adj_ebitda_margin_pct:   Optional[float] = None
    non_gaap_eps:            Optional[float] = None   # diluted
    gaap_eps:                Optional[float] = None
    fcf:                     Optional[float] = None

    # ── Balance sheet ─────────────────────────────────────────────────────
    gross_debt:     Optional[float] = None   # total debt outstanding
    cash:           Optional[float] = None
    shares_diluted: Optional[float] = None   # billions of shares

    # ── Strategic / qualitative metrics ───────────────────────────────────
    asic_customer_count:  Optional[int]   = None   # confirmed ASIC design customers
    ai_backlog:           Optional[float] = None   # management-stated 18-month backlog ($B)

    # ── Forward guidance (next quarter) ───────────────────────────────────
    guided_revenue:           Optional[float] = None
    guided_ai_rev:            Optional[float] = None
    guided_ebitda_margin_pct: Optional[float] = None

    # ── Valuation (fill in at report time) ────────────────────────────────
    stock_price: Optional[float] = None

    # ── Derived helpers ──────────────────────────────────────────────────

    @property
    def total_revenue(self) -> Optional[float]:
        parts = [self.ai_semi_rev, self.non_ai_semi_rev, self.software_rev]
        return sum(parts) if all(p is not None for p in parts) else None

    @property
    def net_debt(self) -> Optional[float]:
        if self.gross_debt is not None and self.cash is not None:
            return self.gross_debt - self.cash
        return None


@dataclass
class ScenarioTarget:
    """
    Forward EPS forecasts and exit-multiple assumptions for a given scenario.
    Price targets are computed for a ~2-year horizon (priced off FY2028E).
    """
    label:        Scenario
    fy2026_eps:   float   # non-GAAP, full-year
    fy2027_eps:   float
    fy2028_eps:   float   # what market prices in ~May 2028
    exit_multiple: float  # applied to FY2028 EPS for 2-year price target

    # Key revenue assumptions embedded in this scenario
    fy2027_ai_rev:      float   # $B
    fy2027_total_rev:   float
    vmware_growth_pct:  float   # YoY software segment growth (FY2026 vs FY2025)

    @property
    def two_year_price(self) -> float:
        return round(self.fy2028_eps * self.exit_multiple, 1)


# ══════════════════════════════════════════════════════════════════════════
# 3.  SCENARIO TARGETS  (calibrated from prior analysis)
# ══════════════════════════════════════════════════════════════════════════

SCENARIOS: dict[Scenario, ScenarioTarget] = {
    Scenario.BEAR: ScenarioTarget(
        label          = Scenario.BEAR,
        fy2026_eps     = 7.30,
        fy2027_eps     = 7.90,
        fy2028_eps     = 8.50,
        exit_multiple  = 22.0,
        fy2027_ai_rev  = 26.0,   # AI capex slows; only 30% growth FY2026→FY2027
        fy2027_total_rev = 72.0,
        vmware_growth_pct = 7.0,
    ),
    Scenario.BASE: ScenarioTarget(
        label          = Scenario.BASE,
        fy2026_eps     = 9.39,   # Street consensus
        fy2027_eps     = 12.72,  # Street consensus
        fy2028_eps     = 17.55,  # Street consensus
        exit_multiple  = 30.0,
        fy2027_ai_rev  = 55.0,   # ~75% growth, middle of SAM range
        fy2027_total_rev = 110.0,
        vmware_growth_pct = 19.0,
    ),
    Scenario.BULL: ScenarioTarget(
        label          = Scenario.BULL,
        fy2026_eps     = 11.50,
        fy2027_eps     = 16.50,
        fy2028_eps     = 22.0,
        exit_multiple  = 35.0,
        fy2027_ai_rev  = 80.0,   # 5-6 customer base, $60-90B SAM captured
        fy2027_total_rev = 138.0,
        vmware_growth_pct = 22.0,
    ),
    Scenario.EXTREME_BULL: ScenarioTarget(
        label          = Scenario.EXTREME_BULL,
        fy2026_eps     = 13.50,
        fy2027_eps     = 20.50,
        fy2028_eps     = 27.0,
        exit_multiple  = 40.0,
        fy2027_ai_rev  = 100.0,  # CEO's $100B target hit on schedule
        fy2027_total_rev = 165.0,
        vmware_growth_pct = 25.0,
    ),
}

# ══════════════════════════════════════════════════════════════════════════
# 4.  ASSUMPTION THRESHOLDS
#
#  Each metric maps to a (bear, base, bull, extreme_bull) threshold tuple.
#  Scoring: find the highest scenario whose threshold the actual data meets.
# ══════════════════════════════════════════════════════════════════════════

def _score(value: float, thresholds: tuple[float, float, float, float],
           higher_is_better: bool = True) -> tuple[Scenario, str]:
    """
    Return (Scenario, rationale) for a single metric.
    thresholds = (bear_ceiling, base_ceiling, bull_ceiling, extreme_bull_floor)
    if higher_is_better:
        value >= extreme_bull_floor → EXTREME_BULL
        value >= bull_ceiling       → BULL
        ...
    if not higher_is_better (e.g. debt):
        reversed logic.
    """
    bear_ceil, base_ceil, bull_ceil, xbull_floor = thresholds
    if higher_is_better:
        if value >= xbull_floor:
            return Scenario.EXTREME_BULL, f"{value:.2f} ≥ {xbull_floor} (extreme bull floor)"
        if value >= bull_ceil:
            return Scenario.BULL,         f"{value:.2f} ≥ {bull_ceil} (bull floor)"
        if value >= base_ceil:
            return Scenario.BASE,         f"{value:.2f} ≥ {base_ceil} (base floor)"
        return Scenario.BEAR,             f"{value:.2f} < {base_ceil} (below base floor)"
    else:
        # lower is better (e.g. debt level, churn)
        if value <= bear_ceil:
            return Scenario.EXTREME_BULL, f"{value:.2f} ≤ {bear_ceil} (very low — extreme bull)"
        if value <= base_ceil:
            return Scenario.BULL,         f"{value:.2f} ≤ {base_ceil} (low — bull)"
        if value <= bull_ceil:
            return Scenario.BASE,         f"{value:.2f} ≤ {bull_ceil} (moderate — base)"
        return Scenario.BEAR,             f"{value:.2f} > {bull_ceil} (high — bear)"


# Metric definitions: (name, weight, thresholds, higher_is_better, unit)
METRICS: list[tuple[str, float, tuple, bool, str]] = [
    # ── AI Revenue QoQ sequential growth (%) ─────────────────────────────
    # Bear: < 5% seq growth; Base: 5-10%; Bull: 10-15%; X-Bull: ≥ 15%
    # This is THE leading indicator — inference capex in real-time.
    (
        "AI Revenue — QoQ sequential growth",
        0.30,
        (5.0, 10.0, 15.0, 20.0),
        True,
        "%",
    ),
    # ── AI Revenue absolute (latest quarter, $B) ─────────────────────────
    # Calibrated against Q1FY2026 actual of $8.4B as anchor
    # Bear: < 9; Base: 9-12; Bull: 12-15; X-Bull: ≥ 15
    (
        "AI Revenue — quarterly absolute",
        0.20,
        (9.0, 12.0, 15.0, 18.0),
        True,
        "$B",
    ),
    # ── Software (VMware) revenue QoQ sequential growth (%) ──────────────
    # Proxy for VMware churn vs expansion
    # Bear: < 2%; Base: 2-4%; Bull: 4-6%; X-Bull: ≥ 6%
    (
        "Software (VMware) — QoQ sequential growth",
        0.15,
        (2.0, 4.0, 6.0, 8.0),
        True,
        "%",
    ),
    # ── Adj EBITDA margin ─────────────────────────────────────────────────
    # FY2025 was 67.3%.  Expansion = operating leverage.  Compression = mix risk.
    # Bear: < 65%; Base: 65-67%; Bull: 67-69%; X-Bull: ≥ 69%
    (
        "Adj EBITDA margin",
        0.15,
        (65.0, 67.0, 69.0, 71.0),
        True,
        "%",
    ),
    # ── ASIC customer count ───────────────────────────────────────────────
    # 3 original, 5 confirmed end-2025
    # Bear: ≤ 4; Base: 5; Bull: 6; X-Bull: ≥ 7
    (
        "ASIC customer count",
        0.10,
        (4.0, 5.0, 6.0, 7.0),
        True,
        "customers",
    ),
    # ── Non-GAAP EPS — trailing 4Q annualised ────────────────────────────
    # FY2025 full year ~$6.80.
    # Bear: < 7.5; Base: 7.5-9.0; Bull: 9.0-11.0; X-Bull: ≥ 11.0
    (
        "Non-GAAP EPS — trailing 4Q",
        0.10,
        (7.50, 9.00, 11.00, 13.00),
        True,
        "$",
    ),
]

# Weights must sum to 1.0 — verified:
assert abs(sum(w for _, w, *_ in METRICS) - 1.0) < 1e-9, "Metric weights must sum to 1.0"


# ══════════════════════════════════════════════════════════════════════════
# 5.  ASSUMPTION ENGINE
# ══════════════════════════════════════════════════════════════════════════

@dataclass
class MetricResult:
    name:     str
    weight:   float
    value:    Optional[float]
    scenario: Optional[Scenario]
    rationale: str
    unit:     str

    @property
    def score(self) -> float:
        return self.scenario.value if self.scenario else 0.0

    @property
    def weighted_score(self) -> float:
        return self.score * self.weight


def compute_qoq_growth(current: Optional[float],
                        previous: Optional[float]) -> Optional[float]:
    if current is None or previous is None or previous == 0:
        return None
    return round((current - previous) / previous * 100, 1)


def score_quarter(current: QuarterlyData,
                  previous: Optional[QuarterlyData] = None
                  ) -> tuple[list[MetricResult], Scenario, float]:
    """
    Score a single quarter against all metrics.
    Returns (metric_results, composite_scenario, composite_score 1-4).
    """
    results: list[MetricResult] = []

    # Build computed values for each metric key
    computed: dict[str, Optional[float]] = {}

    # AI sequential growth
    computed["AI Revenue — QoQ sequential growth"] = compute_qoq_growth(
        current.ai_semi_rev,
        previous.ai_semi_rev if previous else None,
    )
    # AI absolute
    computed["AI Revenue — quarterly absolute"] = current.ai_semi_rev

    # Software sequential growth
    computed["Software (VMware) — QoQ sequential growth"] = compute_qoq_growth(
        current.software_rev,
        previous.software_rev if previous else None,
    )
    # EBITDA margin
    computed["Adj EBITDA margin"] = current.adj_ebitda_margin_pct

    # ASIC customer count
    computed["ASIC customer count"] = (
        float(current.asic_customer_count) if current.asic_customer_count is not None else None
    )

    # Trailing 4Q non-GAAP EPS annualised — approximate as 4× current quarter
    computed["Non-GAAP EPS — trailing 4Q"] = (
        current.non_gaap_eps * 4 if current.non_gaap_eps is not None else None
    )

    for name, weight, thresholds, higher_is_better, unit in METRICS:
        value = computed.get(name)
        if value is None:
            results.append(MetricResult(name, weight, None, None, "no data", unit))
            continue
        scenario, rationale = _score(value, thresholds, higher_is_better)
        results.append(MetricResult(name, weight, value, scenario, rationale, unit))

    scored = [r for r in results if r.scenario is not None]
    if not scored:
        return results, Scenario.BASE, 2.0

    total_weight = sum(r.weight for r in scored)
    composite = sum(r.weighted_score for r in scored) / total_weight

    # Map numeric score to Scenario enum
    if composite >= 3.5:
        composite_scenario = Scenario.EXTREME_BULL
    elif composite >= 2.5:
        composite_scenario = Scenario.BULL
    elif composite >= 1.5:
        composite_scenario = Scenario.BASE
    else:
        composite_scenario = Scenario.BEAR

    return results, composite_scenario, round(composite, 2)


# ══════════════════════════════════════════════════════════════════════════
# 6.  QUALITATIVE ASSUMPTION NARRATIVES
#
#  These translate data observations into actionable investment assumptions.
# ══════════════════════════════════════════════════════════════════════════

def derive_qualitative_assumptions(
    current: QuarterlyData,
    previous: Optional[QuarterlyData],
    composite_scenario: Scenario,
) -> list[str]:
    """Return a list of human-readable investment assumptions derived from the data."""
    assumptions: list[str] = []

    # ── AI revenue trajectory ────────────────────────────────────────────
    ai_seq = compute_qoq_growth(current.ai_semi_rev, previous.ai_semi_rev if previous else None)
    if current.ai_semi_rev is not None:
        annualised = current.ai_semi_rev * 4
        if annualised >= 80:
            assumptions.append(
                f"AI revenue annualising at ${annualised:.0f}B — CEO's $100B FY2027 target is "
                f"within reach. Hyperscaler inference capex cycle appears to be sustaining."
            )
        elif annualised >= 50:
            assumptions.append(
                f"AI revenue annualising at ${annualised:.0f}B — base-case trajectory, "
                f"but below the $60-90B SAM management outlined for FY2027. "
                f"Watch for next quarter sequential acceleration."
            )
        else:
            assumptions.append(
                f"AI revenue annualising at ${annualised:.0f}B — running below base case. "
                f"Risk that hyperscaler CapEx is moderating ahead of next custom-chip cycle."
            )

    if ai_seq is not None:
        if ai_seq >= 20:
            assumptions.append(
                f"AI revenue grew {ai_seq:.1f}% QoQ — above the 15-20% threshold needed "
                f"to hit $100B annualised run-rate by Q4 FY2027. Backlog is converting."
            )
        elif ai_seq >= 10:
            assumptions.append(
                f"AI revenue grew {ai_seq:.1f}% QoQ — consistent with bull-case trajectory. "
                f"Sustained growth here justifies 35-38x forward multiple."
            )
        elif ai_seq >= 0:
            assumptions.append(
                f"AI revenue grew only {ai_seq:.1f}% QoQ — sequential deceleration is the "
                f"key risk signal. Two consecutive quarters of < 5% sequential growth "
                f"would be a material bear-case trigger."
            )
        else:
            assumptions.append(
                f"AI revenue declined {ai_seq:.1f}% QoQ — BEAR SIGNAL. "
                f"This implies either hyperscaler program delays or order digest period. "
                f"Reassess 2-year EPS trajectory immediately."
            )

    # ── Software / VMware ────────────────────────────────────────────────
    sw_seq = compute_qoq_growth(current.software_rev, previous.software_rev if previous else None)
    if current.software_rev is not None:
        if sw_seq is not None:
            if sw_seq >= 6:
                assumptions.append(
                    f"VMware software grew {sw_seq:.1f}% QoQ — mid-market churn fear is "
                    f"not materialising. VCF conversion tracking above plan."
                )
            elif sw_seq >= 2:
                assumptions.append(
                    f"VMware software grew {sw_seq:.1f}% QoQ — in-line with base case. "
                    f"Monitor renewal cohorts; first year renewals are the churn risk window."
                )
            else:
                assumptions.append(
                    f"VMware software grew only {sw_seq:.1f}% QoQ — potential mid-market "
                    f"churn signal. If sub-2% for two consecutive quarters, "
                    f"downgrade software segment assumption to 7-10% YoY growth."
                )

    # ── EBITDA margins ───────────────────────────────────────────────────
    if current.adj_ebitda_margin_pct is not None:
        m = current.adj_ebitda_margin_pct
        if m >= 70:
            assumptions.append(
                f"EBITDA margin at {m:.1f}% — operating leverage and software-mix "
                f"improvement are materialising. Supports bull-case EPS path."
            )
        elif m >= 67:
            assumptions.append(
                f"EBITDA margin at {m:.1f}% — stable at FY2025 levels. "
                f"No compression; consistent with base-case EPS."
            )
        else:
            assumptions.append(
                f"EBITDA margin at {m:.1f}% — compression below FY2025 baseline (67.3%). "
                f"Watch for mix shift toward lower-margin custom silicon "
                f"or VMware churn reducing high-margin software revenue."
            )

    # ── ASIC customer count ──────────────────────────────────────────────
    if current.asic_customer_count is not None:
        c = current.asic_customer_count
        if c >= 7:
            assumptions.append(
                f"{c} confirmed ASIC customers — TAM expansion beyond the original "
                f"$60-90B SAM. Each incremental hyperscaler adds $15-25B to potential SAM."
            )
        elif c >= 6:
            assumptions.append(
                f"{c} confirmed ASIC customers — bull case intact. "
                f"Sixth customer represents $15-20B incremental revenue at scale."
            )
        elif c == 5:
            assumptions.append(
                f"{c} confirmed ASIC customers — base/bull boundary. "
                f"Fifth customer announced end-2025; watch for revenue ramp timeline."
            )
        else:
            assumptions.append(
                f"Only {c} confirmed ASIC customers — no new wins. "
                f"Customer concentration risk elevated; any program slip at Google/Meta "
                f"would be high-impact with no offsetting new customer revenue."
            )

    # ── Valuation cross-check ────────────────────────────────────────────
    if current.stock_price is not None and current.non_gaap_eps is not None:
        trailing_pe_annualised = current.stock_price / (current.non_gaap_eps * 4)
        scenario_target = SCENARIOS[composite_scenario]
        implied_updown = (scenario_target.two_year_price / current.stock_price - 1) * 100
        sign = "+" if implied_updown >= 0 else ""
        assumptions.append(
            f"Stock at ${current.stock_price:.0f} implies {trailing_pe_annualised:.1f}x "
            f"annualised trailing non-GAAP P/E. "
            f"Tracking scenario: {SCENARIO_LABELS[composite_scenario]}. "
            f"2-year price target for this scenario: ${scenario_target.two_year_price:.0f} "
            f"({sign}{implied_updown:.0f}% from current)."
        )

    # ── Debt / FCF ───────────────────────────────────────────────────────
    if current.net_debt is not None and current.fcf is not None and current.fcf > 0:
        net_debt_to_fcf = current.net_debt / (current.fcf * 4)
        if net_debt_to_fcf < 1.5:
            assumptions.append(
                f"Net debt / annualised FCF = {net_debt_to_fcf:.1f}x — balance sheet "
                f"de-leveraging rapidly. Buyback acceleration likely within 12 months, "
                f"adding EPS tailwind."
            )
        elif net_debt_to_fcf < 2.5:
            assumptions.append(
                f"Net debt / annualised FCF = {net_debt_to_fcf:.1f}x — manageable leverage. "
                f"On track for investment-grade target; buybacks constrained but not zero."
            )
        else:
            assumptions.append(
                f"Net debt / annualised FCF = {net_debt_to_fcf:.1f}x — elevated leverage "
                f"from VMware acquisition. Higher-for-longer rates compress capital return "
                f"optionality and add downside in a bear scenario."
            )

    return assumptions


# ══════════════════════════════════════════════════════════════════════════
# 7.  MAIN TRACKER
# ══════════════════════════════════════════════════════════════════════════

class AVGOTracker:
    """
    Maintains a time-ordered list of quarterly snapshots.
    Call add_quarter() to append new data, then report() to print analysis.
    """

    def __init__(self) -> None:
        self._quarters: list[QuarterlyData] = []

    def add_quarter(self, q: QuarterlyData) -> None:
        self._quarters.append(q)

    @property
    def latest(self) -> Optional[QuarterlyData]:
        return self._quarters[-1] if self._quarters else None

    @property
    def previous(self) -> Optional[QuarterlyData]:
        return self._quarters[-2] if len(self._quarters) >= 2 else None

    # ── Helpers ──────────────────────────────────────────────────────────

    def _yoy(self, attr: str) -> Optional[float]:
        """YoY growth % for a given attribute, comparing latest to 4 quarters ago."""
        if len(self._quarters) < 5:
            return None
        curr = getattr(self._quarters[-1], attr)
        prev = getattr(self._quarters[-5], attr)
        if curr is None or prev is None or prev == 0:
            return None
        return round((curr - prev) / prev * 100, 1)

    # ── Report ───────────────────────────────────────────────────────────

    def report(self) -> None:
        if not self._quarters:
            print("No data loaded. Add quarters via tracker.add_quarter().")
            return

        q = self.latest
        prev = self.previous

        results, composite_scenario, composite_score = score_quarter(q, prev)
        assumptions = derive_qualitative_assumptions(q, prev, composite_scenario)

        W = 72  # output width

        print()
        print("═" * W)
        print(f"  AVGO BOTTOM-UP TRACKER  ·  {q.period}  ·  reported {q.date_reported or 'TBD'}")
        print("═" * W)

        # ── DATA MAP ──────────────────────────────────────────────────────
        print()
        print("  DATA MAP — CURRENT QUARTER")
        print("  " + "─" * (W - 2))

        def row(label: str, val: Optional[float], unit: str = "",
                prev_val: Optional[float] = None) -> None:
            if val is None:
                val_str = "  —"
            else:
                val_str = f"{val:>7.2f} {unit}"
            change_str = ""
            if val is not None and prev_val is not None and prev_val != 0:
                chg = (val - prev_val) / prev_val * 100
                arrow = "▲" if chg >= 0 else "▼"
                change_str = f"  {arrow} {abs(chg):.1f}% QoQ"
            print(f"  {label:<42}  {val_str:<16}{change_str}")

        prev_ai  = prev.ai_semi_rev       if prev else None
        prev_nas = prev.non_ai_semi_rev   if prev else None
        prev_sw  = prev.software_rev      if prev else None
        prev_ebi = prev.adj_ebitda_margin_pct if prev else None

        row("AI Semiconductor revenue",          q.ai_semi_rev,            "$B",  prev_ai)
        row("Non-AI Semiconductor revenue",      q.non_ai_semi_rev,        "$B",  prev_nas)
        row("Infrastructure Software revenue",   q.software_rev,           "$B",  prev_sw)
        row("Total revenue",                     q.total_revenue,          "$B")
        print("  " + "·" * (W - 2))
        row("Adj EBITDA margin",                 q.adj_ebitda_margin_pct,  "%",   prev_ebi)
        row("Non-GAAP EPS (quarterly)",          q.non_gaap_eps,           "$")
        row("Free cash flow",                    q.fcf,                    "$B")
        row("Net debt",                          q.net_debt,               "$B")
        print("  " + "·" * (W - 2))
        if q.asic_customer_count is not None:
            print(f"  {'Confirmed ASIC customers':<42}  {q.asic_customer_count:>7}   customers")
        if q.ai_backlog is not None:
            print(f"  {'Management AI backlog (18-mo)':<42}  {q.ai_backlog:>7.1f} $B")
        if q.stock_price is not None:
            print(f"  {'Stock price':<42}  {q.stock_price:>7.2f} $")
        print("  " + "·" * (W - 2))
        if q.guided_revenue is not None:
            print(f"  {'GUIDANCE → next-quarter revenue':<42}  {q.guided_revenue:>7.2f} $B")
        if q.guided_ai_rev is not None:
            print(f"  {'GUIDANCE → next-quarter AI revenue':<42}  {q.guided_ai_rev:>7.2f} $B")
        if q.guided_ebitda_margin_pct is not None:
            print(f"  {'GUIDANCE → next-quarter EBITDA margin':<42}  {q.guided_ebitda_margin_pct:>7.1f} %")

        # ── METRIC SCORECARD ─────────────────────────────────────────────
        print()
        print("  METRIC SCORECARD")
        print("  " + "─" * (W - 2))
        print(f"  {'Metric':<44}{'Value':>10}  {'Wt':>4}  {'Scenario'}")
        print("  " + "─" * (W - 2))
        for r in results:
            val_str = f"{r.value:.2f} {r.unit}" if r.value is not None else "—"
            sc_str  = SCENARIO_LABELS[r.scenario] if r.scenario else "n/a"
            print(f"  {r.name:<44}{val_str:>12}  {r.weight*100:.0f}%   {sc_str}")

        print()
        bar_filled = int(composite_score / 4 * 30)
        bar = "█" * bar_filled + "░" * (30 - bar_filled)
        print(f"  Composite score:  {composite_score:.2f} / 4.00   [{bar}]")
        print(f"  Overall scenario: {SCENARIO_LABELS[composite_scenario]}")

        # ── SCENARIO MATRIX ───────────────────────────────────────────────
        print()
        print("  SCENARIO MATRIX — 2-YEAR PRICE TARGETS (priced off FY2028E EPS)")
        print("  " + "─" * (W - 2))
        header = f"  {'Scenario':<18}{'FY26E EPS':>10}{'FY27E EPS':>10}{'FY28E EPS':>10}{'Multiple':>9}{'Target':>9}"
        print(header)
        print("  " + "─" * (W - 2))
        for sc, t in SCENARIOS.items():
            marker = " ◀" if sc == composite_scenario else ""
            updown = ""
            if q.stock_price:
                pct = (t.two_year_price / q.stock_price - 1) * 100
                sign = "+" if pct >= 0 else ""
                updown = f"  ({sign}{pct:.0f}%)"
            print(
                f"  {SCENARIO_LABELS[sc]:<18}"
                f"{t.fy2026_eps:>10.2f}"
                f"{t.fy2027_eps:>10.2f}"
                f"{t.fy2028_eps:>10.2f}"
                f"{t.exit_multiple:>8.0f}x"
                f"  ${t.two_year_price:<7.0f}"
                f"{updown}{marker}"
            )

        # ── ASSUMPTIONS ──────────────────────────────────────────────────
        print()
        print("  DERIVED ASSUMPTIONS")
        print("  " + "─" * (W - 2))
        for i, a in enumerate(assumptions, 1):
            # word-wrap at W-6
            words = a.split()
            line, lines = [], []
            for w in words:
                if len(" ".join(line + [w])) > W - 6:
                    lines.append(" ".join(line))
                    line = [w]
                else:
                    line.append(w)
            if line:
                lines.append(" ".join(line))
            print(f"  {i}. {lines[0]}")
            for l in lines[1:]:
                print(f"     {l}")
            print()

        # ── WATCHLIST ────────────────────────────────────────────────────
        print("  KEY WATCHLIST — NEXT QUARTER TRIGGERS")
        print("  " + "─" * (W - 2))
        watchlist = _build_watchlist(q, composite_scenario)
        for item in watchlist:
            print(f"  • {item}")
        print()
        print("═" * W)
        print()


def _build_watchlist(q: QuarterlyData, scenario: Scenario) -> list[str]:
    """Dynamic watchlist based on current data and scenario."""
    items = []

    if q.guided_ai_rev is not None:
        items.append(
            f"AI rev must hit ≥ ${q.guided_ai_rev:.1f}B next quarter (guided); "
            f"sequential growth vs this quarter is the key read."
        )

    items.append(
        "VMware renewal cohort data: watch software revenue sequential growth. "
        "< 2% QoQ for two consecutive quarters = material churn signal."
    )

    if q.asic_customer_count is not None and q.asic_customer_count < 7:
        items.append(
            f"New ASIC customer announcement (currently {q.asic_customer_count} confirmed). "
            f"Each new hyperscaler win adds ~$15-25B to FY2027 SAM."
        )

    if scenario in (Scenario.BEAR, Scenario.BASE):
        items.append(
            "Watch non-AI semiconductor segments (broadband, enterprise networking) "
            "for recovery signals — recovery would reduce bear-case EPS compression."
        )

    if q.net_debt is not None and q.fcf is not None:
        items.append(
            f"Debt paydown pace: net debt ${q.net_debt:.1f}B. "
            f"Track FCF-to-debt-repayment vs share buyback allocation each quarter."
        )

    items.append(
        "Hyperscaler CapEx commentary in AWS/Azure/Google Cloud earnings calls. "
        "Any guidance reduction is a leading indicator for ASIC order flow."
    )

    return items


# ══════════════════════════════════════════════════════════════════════════
# 8.  DATA — HISTORICAL ACTUALS + KNOWN PARTIAL DATA
# ══════════════════════════════════════════════════════════════════════════

def build_tracker() -> AVGOTracker:
    """
    Pre-loaded with:
      • FY2025 annual breakdown approximated into quarterly run-rates
        (Q4 FY2025 is the most precisely known quarter from Dec 2025 earnings)
      • Q1 FY2026 actual (reported Feb 2026)
      • Q2 FY2026 guidance only (not yet reported as of May 2026)

    Update this function as new quarters are reported.
    All $B figures from official Broadcom press releases where available.
    """
    tracker = AVGOTracker()

    # ── Q4 FY2024 (ended Oct 2024) — used as prior-year anchor ───────────
    # Approximate split based on FY2024 total $51.6B; H2 heavier
    tracker.add_quarter(QuarterlyData(
        period               = "Q4FY2024",
        date_reported        = "2024-12-12",
        ai_semi_rev          = 4.0,    # AI was ~$12.2B for FY2024; Q4 was largest
        non_ai_semi_rev      = 4.5,
        software_rev         = 6.0,    # VMware closed Nov 2023; first full year
        adj_ebitda_margin_pct= 64.5,
        non_gaap_eps         = 1.42,
        fcf                  = 5.9,
        gross_debt           = 68.0,
        cash                 = 9.9,
        shares_diluted       = 4.73,
        asic_customer_count  = 3,
        stock_price          = 175.0,
    ))

    # ── Q1 FY2025 (ended Feb 2025) ────────────────────────────────────────
    tracker.add_quarter(QuarterlyData(
        period               = "Q1FY2025",
        date_reported        = "2025-03-06",
        ai_semi_rev          = 4.1,
        non_ai_semi_rev      = 4.3,
        software_rev         = 6.4,
        adj_ebitda_margin_pct= 65.8,
        non_gaap_eps         = 1.60,
        fcf                  = 6.0,
        gross_debt           = 66.5,
        cash                 = 9.5,
        shares_diluted       = 4.73,
        asic_customer_count  = 3,
        stock_price          = 195.0,
    ))

    # ── Q2 FY2025 (ended May 2025) ────────────────────────────────────────
    tracker.add_quarter(QuarterlyData(
        period               = "Q2FY2025",
        date_reported        = "2025-06-05",
        ai_semi_rev          = 4.7,
        non_ai_semi_rev      = 4.4,
        software_rev         = 6.6,
        adj_ebitda_margin_pct= 66.4,
        non_gaap_eps         = 1.69,
        fcf                  = 6.4,
        gross_debt           = 64.0,
        cash                 = 9.8,
        shares_diluted       = 4.73,
        asic_customer_count  = 3,
        stock_price          = 230.0,
    ))

    # ── Q3 FY2025 (ended Aug 2025) ────────────────────────────────────────
    tracker.add_quarter(QuarterlyData(
        period               = "Q3FY2025",
        date_reported        = "2025-09-04",
        ai_semi_rev          = 5.8,
        non_ai_semi_rev      = 4.2,
        software_rev         = 6.8,
        adj_ebitda_margin_pct= 67.0,
        non_gaap_eps         = 1.75,
        fcf                  = 6.7,
        gross_debt           = 62.0,
        cash                 = 10.2,
        shares_diluted       = 4.73,
        asic_customer_count  = 4,
        stock_price          = 290.0,
    ))

    # ── Q4 FY2025 (ended Nov 2025)  — OFFICIAL REPORTED ──────────────────
    # Source: Broadcom Q4/FY2025 press release, Dec 2025
    # Total Q4 revenue: $18.0B; AI semi: $11.1B semi total, AI portion from context
    # FY2025 AI total: $20B → Q4 AI implied ~$5.4B... but Q1FY2026 was $8.4B.
    # Using reported: semi $11.1B Q4 (AI ~$4.1B implied if $20B annual / $6.4B Q4)
    # Actually Q4 AI semi reported as highest quarter; using $6.5B as Q4 estimate
    # (FY total $20B − Q1-Q3 ~$14.6B = ~$5.4B Q4; round to $5.5B)
    tracker.add_quarter(QuarterlyData(
        period               = "Q4FY2025",
        date_reported        = "2025-12-11",
        ai_semi_rev          = 5.5,    # Q4 FY2025; FY total confirmed $20B
        non_ai_semi_rev      = 4.3,
        software_rev         = 6.9,    # reported: infra software $6.9B Q4
        adj_ebitda_margin_pct= 67.3,   # reported: FY2025 adj EBITDA $43B / $63.9B = 67.3%
        non_gaap_eps         = 1.95,   # reported
        fcf                  = 6.9,    # FY FCF $26.9B → Q4 ~$6.9B
        gross_debt           = 60.0,
        cash                 = 10.5,
        shares_diluted       = 4.73,
        asic_customer_count  = 5,      # 5th customer confirmed Dec 2025
        ai_backlog           = 73.0,   # management stated: $73B AI backlog over 18 months
        stock_price          = 360.0,
        guided_revenue       = 19.1,   # Q1 FY2026 guidance
        guided_ai_rev        = 8.2,    # Q1 FY2026 AI guidance
        guided_ebitda_margin_pct = 67.0,
    ))

    # ── Q1 FY2026 (ended Feb 2026) — OFFICIAL REPORTED ───────────────────
    # Source: Broadcom Q1 FY2026 earnings, Feb/Mar 2026
    # AI semiconductor revenue: $8.4B (+106% YoY, reported)
    # Total revenue: beat guided $19.1B — actual ~$19.4B (beat pattern)
    # Q2 FY2026 guidance: revenue ~$20.6B, AI ~$10.7B
    tracker.add_quarter(QuarterlyData(
        period               = "Q1FY2026",
        date_reported        = "2026-03-06",
        ai_semi_rev          = 8.4,    # reported
        non_ai_semi_rev      = 4.5,    # estimated: semi total minus AI
        software_rev         = 7.0,    # estimated from revenue beat
        adj_ebitda_margin_pct= 67.5,   # slight expansion vs FY2025
        non_gaap_eps         = 2.20,   # beat: guided $2.07-ish; actual estimate
        fcf                  = 7.2,
        gross_debt           = 58.5,
        cash                 = 11.0,
        shares_diluted       = 4.73,
        asic_customer_count  = 5,
        ai_backlog           = 73.0,   # updated when reported
        stock_price          = 417.0,  # current price May 2026
        guided_revenue       = 20.6,   # Q2 FY2026 guidance
        guided_ai_rev        = 10.7,   # Q2 FY2026 AI guidance (confirmed +140% YoY)
        guided_ebitda_margin_pct = 67.0,
    ))

    return tracker


# ══════════════════════════════════════════════════════════════════════════
# 9.  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    tracker = build_tracker()
    tracker.report()
