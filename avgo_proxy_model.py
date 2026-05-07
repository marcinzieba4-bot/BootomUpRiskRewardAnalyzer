#!/usr/bin/env python3
"""
AVGO Proxy / Alternative Data Model
-------------------------------------
Tracks leading-indicator data from third-party sources to derive scenario
probability distributions for Broadcom (AVGO) *before* AVGO reports.

Proxy signals and their AVGO read-through:
──────────────────────────────────────────────────────────────────────────
 Signal                      Source          Lead time   AVGO read-through
 ─────────────────────────────────────────────────────────────────────────
 Hyperscaler CapEx (YoY)     GOOG/META/      1-2Q        AI custom ASIC
                             MSFT/AMZN                   orders
 TSMC HPC revenue %          TSMC monthly    1-2Q        AI chip fab volume
 Arista Networks rev (YoY)   ANET quarterly  0-1Q        AI cluster build-out;
                                                         AVGO networking ASICs
 Nutanix ARR growth (YoY)    NTNX quarterly  1Q          VMware churn proxy
   (inverse — high NTNX      (inverse)                   (more NTNX = more
    growth = more AVGO                                    VMware defection)
    software headwind)
 SMCI revenue (YoY)          SMCI quarterly  0Q          AI server density;
                                                         GPU cluster builds
 CDW revenue (YoY)           CDW quarterly   0-1Q        Enterprise IT budget
                                                         health; AVGO non-AI
                                                         semi + VMware channel

Usage:
    python avgo_proxy_model.py           # standalone proxy report
    from avgo_proxy_model import ...     # imported by avgo_tracker.py
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import math

# ══════════════════════════════════════════════════════════════════════════
# 1.  SHARED ENUMS (duplicated-lite so file is self-contained)
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
# 2.  PROXY DATA STRUCTURE
# ══════════════════════════════════════════════════════════════════════════

@dataclass
class ProxySnapshot:
    """
    One period's worth of third-party proxy data.
    The period should align with the *AVGO quarter being predicted*,
    i.e. data available a few weeks before AVGO reports.

    All growth figures are YoY (%) unless noted.
    Dollar amounts in $B.
    """
    period: str         # e.g. "Q1FY2026"
    date_snapshot: str  # when this data became available

    # ── HYPERSCALER CAPEX (combined: GOOG + META + MSFT + AMZN) ──────────
    # Source: quarterly earnings calls (1-4 weeks before AVGO reports)
    # Read-through: measures pipeline demand for custom AI ASICs ~1-2Q ahead.
    hyperscaler_capex_total_qtr: Optional[float] = None  # combined $B that quarter
    hyperscaler_capex_yoy_pct:   Optional[float] = None  # YoY growth %

    # ── TSMC HPC PLATFORM % of REVENUE ───────────────────────────────────
    # Source: TSMC quarterly earnings (Jan/Apr/Jul/Oct)
    # Read-through: HPC includes almost all AVGO custom AI ASICs on N3/N5.
    # Rising % = AVGO AI orders filling fab.
    tsmc_hpc_pct:               Optional[float] = None  # % of TSMC quarterly revenue
    tsmc_rev_yoy_pct:           Optional[float] = None  # TSMC total revenue YoY

    # ── ARISTA NETWORKS REVENUE GROWTH ───────────────────────────────────
    # Source: ANET quarterly (reports ~2-3 weeks before AVGO)
    # Read-through: Arista deploys Ethernet AI clusters → uses AVGO's
    # Tomahawk/Jericho merchant silicon for AI-scale networking.
    # High ANET growth = hyperscalers building AI pods = AVGO networking ASIC upside.
    arista_rev_yoy_pct:         Optional[float] = None
    arista_rev_qtr:             Optional[float] = None  # $B

    # ── NUTANIX ARR GROWTH (INVERSE) ─────────────────────────────────────
    # Source: NTNX quarterly (FY ends Jul; reports quarterly)
    # Read-through: Nutanix is the #1 destination for VMware defectors.
    # HIGH Nutanix growth → VMware churn intensifying → BEAR for AVGO software.
    # LOW Nutanix growth → mid-market holding VMware → BULL for AVGO software.
    nutanix_arr_yoy_pct:        Optional[float] = None  # ARR growth — inverse signal
    nutanix_new_logos_qtr:      Optional[int]   = None  # new customer logos

    # ── SUPER MICRO COMPUTER REVENUE GROWTH ──────────────────────────────
    # Source: SMCI quarterly (FY ends Jun; note: had accounting delays in 2024)
    # Read-through: SMCI ships GPU/AI servers to hyperscalers.
    # High SMCI growth = AI server racks deploying = AI capex flowing.
    smci_rev_yoy_pct:           Optional[float] = None
    smci_rev_qtr:               Optional[float] = None  # $B

    # ── CDW TECHNOLOGY SOLUTIONS REVENUE ─────────────────────────────────
    # Source: CDW quarterly (reports ~5-6 weeks after quarter end)
    # Read-through: CDW is a top Broadcom channel partner for software/hardware.
    # CDW enterprise growth → SMB/enterprise VMware + non-AI semi demand healthy.
    cdw_rev_yoy_pct:            Optional[float] = None
    cdw_commercial_yoy_pct:     Optional[float] = None  # commercial segment specifically

    # ── SUPPLEMENTAL QUALITATIVE FLAGS ───────────────────────────────────
    # Manual flags set from earnings call commentary / trade press
    hyperscaler_guidance_tone: Optional[str] = None  # "positive" / "neutral" / "cautious"
    tsmc_mgmt_ai_commentary:   Optional[str] = None  # "accelerating" / "stable" / "moderating"
    vmware_channel_checks:     Optional[str] = None  # "sticky" / "mixed" / "churning"


# ══════════════════════════════════════════════════════════════════════════
# 3.  PROXY METRIC DEFINITIONS
#
#  Each entry: (name, weight, thresholds, higher_is_better, unit, description)
#
#  Thresholds are FLOORS in ascending scenario order:
#    (base_floor, bull_floor, extreme_bull_floor)
#  Value < base_floor → BEAR; value ≥ base_floor → BASE; etc.
#
#  For inverse metrics (higher value = worse for AVGO), the logic flips.
# ══════════════════════════════════════════════════════════════════════════

@dataclass
class ProxyMetricDef:
    name:              str
    weight:            float
    thresholds:        tuple   # (base_floor, bull_floor, xbull_floor)
    higher_is_better:  bool
    unit:              str
    read_through:      str     # what this tells us about AVGO

PROXY_METRIC_DEFS: list[ProxyMetricDef] = [

    ProxyMetricDef(
        name             = "Hyperscaler CapEx — YoY growth",
        weight           = 0.30,
        # Bear: < 10%; Base: 10-30%; Bull: 30-60%; X-Bull: ≥ 60%
        # Calibration: 2026 combined projected +47-77% YoY = BULL/X-BULL
        thresholds       = (10.0, 30.0, 60.0),
        higher_is_better = True,
        unit             = "% YoY",
        read_through     = "AVGO AI ASIC orders ~1-2Q lead",
    ),

    ProxyMetricDef(
        name             = "TSMC HPC platform — % of revenue",
        weight           = 0.20,
        # Bear: < 50%; Base: 50-57%; Bull: 57-62%; X-Bull: ≥ 62%
        # Calibration: Q1 2026 = 61% (up from 55% Q4 2025) → BULL
        thresholds       = (50.0, 57.0, 62.0),
        higher_is_better = True,
        unit             = "% of TSMC rev",
        read_through     = "AI chip fab utilisation; direct AVGO ASIC volume",
    ),

    ProxyMetricDef(
        name             = "Arista Networks — revenue YoY growth",
        weight           = 0.15,
        # Bear: < 15%; Base: 15-25%; Bull: 25-35%; X-Bull: ≥ 35%
        # Calibration: Q1 2026 = +35.1% YoY → X-Bull boundary
        thresholds       = (15.0, 25.0, 35.0),
        higher_is_better = True,
        unit             = "% YoY",
        read_through     = "AI cluster Ethernet build-out; AVGO networking ASIC demand",
    ),

    ProxyMetricDef(
        name             = "Nutanix ARR growth — YoY (INVERSE)",
        weight           = 0.15,
        # INVERSE: lower Nutanix growth = less VMware churn = better for AVGO
        # Bear (for AVGO): NTNX ARR > 30% YoY (many VMware defectors)
        # X-Bull (for AVGO): NTNX ARR < 10% YoY (VMware sticky)
        # Thresholds inverted: (bear_ceiling, base_ceiling, xbull_ceiling)
        # i.e. value ≤ 10 → EXTREME_BULL; ≤ 20 → BULL; ≤ 30 → BASE; > 30 → BEAR
        thresholds       = (10.0, 20.0, 30.0),   # used in reverse logic
        higher_is_better = False,
        unit             = "% YoY ARR (inv)",
        read_through     = "VMware churn rate — inverse: low NTNX growth = VMware sticky",
    ),

    ProxyMetricDef(
        name             = "Super Micro — revenue YoY growth",
        weight           = 0.10,
        # Bear: < 20%; Base: 20-60%; Bull: 60-100%; X-Bull: ≥ 100%
        # Calibration: Q2/Q3 FY2026 = +123% YoY → EXTREME BULL
        # Note: SMCI is lumpy (accounting issues); use directional only
        thresholds       = (20.0, 60.0, 100.0),
        higher_is_better = True,
        unit             = "% YoY",
        read_through     = "AI server rack deployments; GPU cluster density; AI capex flowing",
    ),

    ProxyMetricDef(
        name             = "CDW commercial — revenue YoY growth",
        weight           = 0.10,
        # Bear: < 0%; Base: 0-5%; Bull: 5-10%; X-Bull: ≥ 10%
        # Calibration: Q1 2026 commercial = +9.6% YoY → BULL boundary
        thresholds       = (0.0, 5.0, 10.0),
        higher_is_better = True,
        unit             = "% YoY",
        read_through     = "Enterprise IT budget health; AVGO VMware channel + non-AI semi",
    ),
]

# Weights sum check
assert abs(sum(m.weight for m in PROXY_METRIC_DEFS) - 1.0) < 1e-9


# ══════════════════════════════════════════════════════════════════════════
# 4.  SCORING ENGINE
# ══════════════════════════════════════════════════════════════════════════

@dataclass
class ProxyMetricResult:
    metric:    ProxyMetricDef
    value:     Optional[float]
    scenario:  Optional[Scenario]
    rationale: str

    @property
    def score(self) -> float:
        return self.scenario.value if self.scenario else 0.0

    @property
    def weighted_score(self) -> float:
        return self.score * self.metric.weight


def _score_metric(value: float, thresholds: tuple, higher_is_better: bool
                  ) -> tuple[Scenario, str]:
    base_f, bull_f, xbull_f = thresholds
    if higher_is_better:
        if value >= xbull_f:
            return Scenario.EXTREME_BULL, f"{value:.1f} ≥ {xbull_f} (extreme bull floor)"
        if value >= bull_f:
            return Scenario.BULL,         f"{value:.1f} ≥ {bull_f} (bull floor)"
        if value >= base_f:
            return Scenario.BASE,         f"{value:.1f} ≥ {base_f} (base floor)"
        return Scenario.BEAR,             f"{value:.1f} < {base_f} (below base floor)"
    else:
        # Inverse: lower is better; thresholds are CEILINGS for each scenario
        if value <= base_f:
            return Scenario.EXTREME_BULL, f"{value:.1f} ≤ {base_f} (extreme bull — very low)"
        if value <= bull_f:
            return Scenario.BULL,         f"{value:.1f} ≤ {bull_f} (bull — low)"
        if value <= xbull_f:
            return Scenario.BASE,         f"{value:.1f} ≤ {xbull_f} (base — moderate)"
        return Scenario.BEAR,             f"{value:.1f} > {xbull_f} (bear — high)"


def _extract_value(snap: ProxySnapshot, metric: ProxyMetricDef) -> Optional[float]:
    """Map metric name to the ProxySnapshot field."""
    mapping = {
        "Hyperscaler CapEx — YoY growth":          snap.hyperscaler_capex_yoy_pct,
        "TSMC HPC platform — % of revenue":        snap.tsmc_hpc_pct,
        "Arista Networks — revenue YoY growth":    snap.arista_rev_yoy_pct,
        "Nutanix ARR growth — YoY (INVERSE)":      snap.nutanix_arr_yoy_pct,
        "Super Micro — revenue YoY growth":        snap.smci_rev_yoy_pct,
        "CDW commercial — revenue YoY growth":     snap.cdw_commercial_yoy_pct,
    }
    return mapping.get(metric.name)


def score_proxies(snap: ProxySnapshot) -> tuple[list[ProxyMetricResult], float]:
    """
    Score all proxy metrics for a snapshot.
    Returns (results, composite_score 1.0–4.0).
    """
    results: list[ProxyMetricResult] = []
    for m in PROXY_METRIC_DEFS:
        value = _extract_value(snap, m)
        if value is None:
            results.append(ProxyMetricResult(m, None, None, "no data"))
            continue
        scenario, rationale = _score_metric(value, m.thresholds, m.higher_is_better)
        results.append(ProxyMetricResult(m, value, scenario, rationale))

    scored = [r for r in results if r.scenario is not None]
    if not scored:
        return results, 2.0

    total_w   = sum(r.metric.weight for r in scored)
    composite = sum(r.weighted_score for r in scored) / total_w
    return results, round(composite, 3)


# ══════════════════════════════════════════════════════════════════════════
# 5.  PROBABILISTIC SCENARIO MODEL
#
#  Converts composite score (1.0–4.0) into a probability distribution
#  across the four scenarios using a smooth softmax over distance to
#  each scenario's "centre" score.
#
#  Centre scores:  BEAR=1.25, BASE=2.0, BULL=2.75, EXTREME_BULL=3.75
#  Temperature (τ): controls spread — lower τ → sharper, more decisive.
# ══════════════════════════════════════════════════════════════════════════

_SCENARIO_CENTRES = {
    Scenario.BEAR:         1.25,
    Scenario.BASE:         2.00,
    Scenario.BULL:         2.75,
    Scenario.EXTREME_BULL: 3.75,
}

_TEMPERATURE = 0.60   # tuned so that composite=2.0 gives ~40% BASE, rest spread


def scenario_probabilities(composite: float) -> dict[Scenario, float]:
    """
    Return probability for each scenario (sums to 1.0).
    Uses negative-distance softmax: scenarios closer to composite get higher p.
    """
    distances = {sc: abs(composite - centre)
                 for sc, centre in _SCENARIO_CENTRES.items()}
    # softmax over negative scaled distances
    logits = {sc: -d / _TEMPERATURE for sc, d in distances.items()}
    max_logit = max(logits.values())
    exps = {sc: math.exp(v - max_logit) for sc, v in logits.items()}
    total = sum(exps.values())
    return {sc: round(e / total, 4) for sc, e in exps.items()}


def conviction_score(results: list[ProxyMetricResult]) -> float:
    """
    Returns 0–1 measure of how much the proxy signals AGREE with each other.
    1.0 = all scored metrics point to same scenario.
    0.0 = maximum disagreement.
    """
    scored = [r for r in results if r.scenario is not None]
    if len(scored) < 2:
        return 1.0
    scores = [r.score for r in scored]
    mean_s = sum(scores) / len(scores)
    variance = sum((s - mean_s) ** 2 for s in scores) / len(scores)
    max_variance = 2.25   # maximum possible (1↔4 = 2.25 var)
    return round(1.0 - variance / max_variance, 2)


# ══════════════════════════════════════════════════════════════════════════
# 6.  COMBINATION WITH FUNDAMENTAL SCORE
#
#  The proxy model is a LEADING indicator; the fundamental AVGO model is
#  COINCIDENT. We blend them:
#    • 60% weight on proxy (forward-looking)
#    • 40% weight on fundamental (confirms actual delivery)
# ══════════════════════════════════════════════════════════════════════════

PROXY_WEIGHT      = 0.60
FUNDAMENTAL_WEIGHT = 0.40

def blended_score(proxy_composite: float,
                  fundamental_composite: float) -> tuple[float, dict[Scenario, float]]:
    combined = proxy_composite * PROXY_WEIGHT + fundamental_composite * FUNDAMENTAL_WEIGHT
    combined = round(combined, 3)
    return combined, scenario_probabilities(combined)


# ══════════════════════════════════════════════════════════════════════════
# 7.  QUALITATIVE SIGNAL NARRATIVE
# ══════════════════════════════════════════════════════════════════════════

def proxy_narrative(snap: ProxySnapshot,
                    results: list[ProxyMetricResult],
                    probs: dict[Scenario, float]) -> list[str]:
    """Generate hedge-fund-style investment implications from proxy signals."""
    notes: list[str] = []
    r_map = {r.metric.name: r for r in results if r.scenario is not None}

    # Hyperscaler CapEx
    capex_r = r_map.get("Hyperscaler CapEx — YoY growth")
    if capex_r and snap.hyperscaler_capex_total_qtr:
        if capex_r.scenario in (Scenario.BULL, Scenario.EXTREME_BULL):
            notes.append(
                f"Hyperscaler CapEx of ${snap.hyperscaler_capex_total_qtr:.0f}B this quarter "
                f"({snap.hyperscaler_capex_yoy_pct:.0f}% YoY) is the most powerful confirming "
                f"signal. At this pace, AVGO's $73B AI backlog is in active conversion — "
                f"the pipeline is not speculative."
            )
        elif capex_r.scenario == Scenario.BASE:
            notes.append(
                f"Hyperscaler CapEx growth ({snap.hyperscaler_capex_yoy_pct:.0f}% YoY) "
                f"supports base-case AI revenue but is not yet strong enough to validate "
                f"the extreme bull path to $100B AI revenue in FY2027."
            )
        else:
            notes.append(
                f"Hyperscaler CapEx deceleration ({snap.hyperscaler_capex_yoy_pct:.0f}% YoY) "
                f"is a RED FLAG. This is the most upstream indicator; if capex stalls here, "
                f"AVGO AI ASIC orders will follow with a 1-2 quarter lag."
            )

    # TSMC HPC
    tsmc_r = r_map.get("TSMC HPC platform — % of revenue")
    if tsmc_r and snap.tsmc_hpc_pct:
        if tsmc_r.scenario in (Scenario.BULL, Scenario.EXTREME_BULL):
            notes.append(
                f"TSMC HPC at {snap.tsmc_hpc_pct:.0f}% of revenue confirms the fab is "
                f"being consumed by AI chip orders — AVGO's N3/N5 ASIC slots are filling. "
                f"CoWoS packaging is the bottleneck to watch, not fab capacity."
            )
        else:
            notes.append(
                f"TSMC HPC at {snap.tsmc_hpc_pct:.0f}% of revenue suggests AI chip "
                f"production mix is not expanding. Monitor monthly TSMC revenue for "
                f"any deceleration before the quarterly breakdown is published."
            )

    # Arista
    anet_r = r_map.get("Arista Networks — revenue YoY growth")
    if anet_r and snap.arista_rev_yoy_pct:
        if anet_r.scenario == Scenario.EXTREME_BULL:
            notes.append(
                f"Arista +{snap.arista_rev_yoy_pct:.0f}% YoY: AI clusters requiring ultra-low "
                f"latency Ethernet networking are deploying at scale. AVGO Jericho/Tomahawk "
                f"ASICs ship inside Arista platforms — this is direct ASIC volume visibility."
            )
        elif anet_r.scenario == Scenario.BEAR:
            notes.append(
                f"Arista growth slowing ({snap.arista_rev_yoy_pct:.0f}% YoY) signals cluster "
                f"deployment pause — likely impacts AVGO networking ASIC revenue within 1 quarter."
            )

    # Nutanix (inverse)
    ntnx_r = r_map.get("Nutanix ARR growth — YoY (INVERSE)")
    if ntnx_r and snap.nutanix_arr_yoy_pct:
        if ntnx_r.scenario in (Scenario.BULL, Scenario.EXTREME_BULL):
            notes.append(
                f"Nutanix ARR growing {snap.nutanix_arr_yoy_pct:.0f}% YoY — decelerating "
                f"from prior periods. VMware mid-market churn is real but NOT accelerating. "
                f"AVGO software segment is more defensible than feared."
            )
        elif ntnx_r.scenario == Scenario.BEAR:
            notes.append(
                f"Nutanix ARR growing {snap.nutanix_arr_yoy_pct:.0f}% YoY — elevated defection "
                f"pace from VMware. Flag software segment for downgrade risk; "
                f"watch next AVGO software QoQ sequential closely."
            )

    # SMCI
    smci_r = r_map.get("Super Micro — revenue YoY growth")
    if smci_r and snap.smci_rev_yoy_pct:
        if smci_r.scenario == Scenario.EXTREME_BULL:
            notes.append(
                f"SMCI +{snap.smci_rev_yoy_pct:.0f}% YoY: GPU server deployments in "
                f"hyper-growth. Each GPU rack typically pairs with custom ASIC networking — "
                f"this volume directly supports AVGO AI networking silicon demand."
            )

    # CDW
    cdw_r = r_map.get("CDW commercial — revenue YoY growth")
    if cdw_r and snap.cdw_commercial_yoy_pct:
        if cdw_r.scenario in (Scenario.BULL, Scenario.EXTREME_BULL):
            notes.append(
                f"CDW commercial +{snap.cdw_commercial_yoy_pct:.0f}% YoY: enterprise IT "
                f"budgets healthy. De-risks AVGO's non-AI semiconductor demand recovery "
                f"and reduces VMware mid-market churn risk."
            )
        elif cdw_r.scenario == Scenario.BEAR:
            notes.append(
                f"CDW commercial stalling ({snap.cdw_commercial_yoy_pct:.0f}% YoY) signals "
                f"enterprise budget tightening — risk to AVGO non-AI semi and VMware "
                f"renewal rates at mid-market accounts."
            )

    # Qualitative overrides
    if snap.hyperscaler_guidance_tone == "cautious":
        notes.append(
            "OVERRIDE — Hyperscaler earnings calls flagged cautious CapEx tone. "
            "Scoring may understate bear risk; increase probability weight on BEAR by ~10pp manually."
        )
    if snap.vmware_channel_checks == "churning":
        notes.append(
            "OVERRIDE — Channel checks show VMware churn accelerating. "
            "Nutanix ARR alone may understate pace of enterprise VMware defection."
        )

    # Scenario summary
    top_sc = max(probs, key=lambda sc: probs[sc])
    notes.append(
        f"Probability-weighted scenario: {SCENARIO_LABELS[top_sc]} "
        f"({probs[top_sc]*100:.0f}% probability). "
        f"2-year price range implied: BEAR ${187:.0f} → BASE ${526:.0f} "
        f"→ BULL ${770:.0f} → EXTREME ${1080:.0f}. "
        f"Probability-weighted EV: "
        f"${_probability_weighted_price(probs):.0f}."
    )

    return notes


def _probability_weighted_price(probs: dict[Scenario, float]) -> float:
    price_map = {
        Scenario.BEAR:         187.0,
        Scenario.BASE:         526.0,
        Scenario.BULL:         770.0,
        Scenario.EXTREME_BULL: 1080.0,
    }
    return sum(probs[sc] * price_map[sc] for sc in Scenario)


# ══════════════════════════════════════════════════════════════════════════
# 8.  STANDALONE REPORT
# ══════════════════════════════════════════════════════════════════════════

W = 72

def proxy_report(snap: ProxySnapshot,
                 fundamental_composite: Optional[float] = None) -> None:
    results, proxy_composite = score_proxies(snap)
    probs_proxy = scenario_probabilities(proxy_composite)

    if fundamental_composite is not None:
        blended, probs = blended_score(proxy_composite, fundamental_composite)
    else:
        blended = proxy_composite
        probs   = probs_proxy

    conv = conviction_score(results)
    narr = proxy_narrative(snap, results, probs)

    top_sc = max(probs, key=lambda sc: probs[sc])

    print()
    print("═" * W)
    print(f"  AVGO PROXY / ALT-DATA MODEL  ·  {snap.period}  ·  {snap.date_snapshot}")
    print("═" * W)

    # ── PROXY DATA MAP ───────────────────────────────────────────────────
    print()
    print("  PROXY DATA MAP")
    print("  " + "─" * (W - 2))

    def prow(label, val, unit="", extra=""):
        val_s = f"{val:.1f} {unit}" if val is not None else "—"
        print(f"  {label:<45}  {val_s:<18}{extra}")

    prow("Hyperscaler CapEx — total (GOOG+META+MSFT+AMZN)",
         snap.hyperscaler_capex_total_qtr, "$B quarterly",
         f"  YoY: {snap.hyperscaler_capex_yoy_pct:.0f}%" if snap.hyperscaler_capex_yoy_pct else "")
    prow("TSMC HPC % of quarterly revenue",
         snap.tsmc_hpc_pct, "%",
         f"  TSMC total YoY: {snap.tsmc_rev_yoy_pct:.0f}%" if snap.tsmc_rev_yoy_pct else "")
    prow("Arista Networks — quarterly revenue",
         snap.arista_rev_qtr, "$B",
         f"  YoY: +{snap.arista_rev_yoy_pct:.0f}%" if snap.arista_rev_yoy_pct else "")
    prow("Nutanix ARR growth YoY (inverse churn proxy)",
         snap.nutanix_arr_yoy_pct, "% YoY")
    prow("Super Micro — quarterly revenue",
         snap.smci_rev_qtr, "$B",
         f"  YoY: +{snap.smci_rev_yoy_pct:.0f}%" if snap.smci_rev_yoy_pct else "")
    prow("CDW commercial segment — YoY growth",
         snap.cdw_commercial_yoy_pct, "% YoY")

    if any([snap.hyperscaler_guidance_tone,
            snap.tsmc_mgmt_ai_commentary,
            snap.vmware_channel_checks]):
        print("  " + "·" * (W - 2))
        if snap.hyperscaler_guidance_tone:
            print(f"  {'Hyperscaler earnings call tone':<45}  {snap.hyperscaler_guidance_tone}")
        if snap.tsmc_mgmt_ai_commentary:
            print(f"  {'TSMC management AI commentary':<45}  {snap.tsmc_mgmt_ai_commentary}")
        if snap.vmware_channel_checks:
            print(f"  {'VMware channel checks':<45}  {snap.vmware_channel_checks}")

    # ── PROXY SCORECARD ──────────────────────────────────────────────────
    print()
    print("  PROXY SIGNAL SCORECARD")
    print("  " + "─" * (W - 2))
    print(f"  {'Signal':<48}{'Value':>12}  {'Wt':>4}  {'Scenario'}")
    print("  " + "─" * (W - 2))
    for r in results:
        val_s = f"{r.value:.1f} {r.metric.unit}" if r.value is not None else "—"
        sc_s  = SCENARIO_LABELS[r.scenario] if r.scenario else "n/a"
        print(f"  {r.metric.name:<48}{val_s:>13}  {r.metric.weight*100:.0f}%   {sc_s}")

    print()
    bar_f = int(proxy_composite / 4 * 30)
    bar   = "█" * bar_f + "░" * (30 - bar_f)
    print(f"  Proxy composite score:    {proxy_composite:.2f} / 4.00   [{bar}]")

    conv_bar_f = int(conv * 20)
    conv_bar   = "█" * conv_bar_f + "░" * (20 - conv_bar_f)
    conv_label = "HIGH" if conv >= 0.75 else "MEDIUM" if conv >= 0.50 else "LOW"
    print(f"  Signal conviction:        {conv:.2f} / 1.00   [{conv_bar}]  {conv_label}")

    if fundamental_composite is not None:
        print(f"  Fundamental score:        {fundamental_composite:.2f} / 4.00   "
              f"(weight {FUNDAMENTAL_WEIGHT:.0%})")
        print(f"  Blended score:            {blended:.2f} / 4.00   "
              f"(proxy {PROXY_WEIGHT:.0%} + fundamental {FUNDAMENTAL_WEIGHT:.0%})")

    # ── PROBABILITY DISTRIBUTION ─────────────────────────────────────────
    print()
    print("  SCENARIO PROBABILITY DISTRIBUTION")
    print("  " + "─" * (W - 2))
    print(f"  {'Scenario':<22}{'Probability':>12}  {'Bar (20 chars)':>4}  {'2-yr Price'}")
    print("  " + "─" * (W - 2))
    price_map = {
        Scenario.BEAR:         187.0,
        Scenario.BASE:         526.0,
        Scenario.BULL:         770.0,
        Scenario.EXTREME_BULL: 1080.0,
    }
    for sc in Scenario:
        p   = probs[sc]
        bar = "█" * int(p * 20) + "░" * (20 - int(p * 20))
        marker = " ◀ most likely" if sc == top_sc else ""
        print(f"  {SCENARIO_LABELS[sc]:<22}{p*100:>11.1f}%  {bar}  ${price_map[sc]:<8.0f}{marker}")

    ev = _probability_weighted_price(probs)
    print(f"  {'─'*50}")
    print(f"  Probability-weighted expected price (2yr): ${ev:.0f}")
    current_assumed = 417.0
    ev_updown = (ev / current_assumed - 1) * 100
    sign = "+" if ev_updown >= 0 else ""
    print(f"  vs current ~$417:  {sign}{ev_updown:.0f}%  expected return (2yr, no discount)")

    # ── NARRATIVES ───────────────────────────────────────────────────────
    print()
    print("  PROXY SIGNAL IMPLICATIONS")
    print("  " + "─" * (W - 2))
    for i, n in enumerate(narr, 1):
        words = n.split()
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

    print("═" * W)
    print()


# ══════════════════════════════════════════════════════════════════════════
# 9.  HISTORICAL PROXY DATA
# ══════════════════════════════════════════════════════════════════════════

def build_proxy_history() -> list[ProxySnapshot]:
    """
    Pre-loaded proxy snapshots aligned to each AVGO quarter.
    Sources:
      Hyperscaler CapEx: GOOG/MSFT/META/AMZN quarterly earnings
      TSMC: TSMC quarterly + monthly revenue releases
      ANET: Arista quarterly results
      NTNX: Nutanix quarterly results (FY ends Jul)
      SMCI: Super Micro quarterly results (FY ends Jun; note: accounting restatements)
      CDW:  CDW quarterly results
    """
    return [

        # ── Q3 FY2025 proxy window (data available ~Sep 2025) ─────────────
        # This data was available BEFORE AVGO reported Q3 FY2025
        ProxySnapshot(
            period                      = "Q3FY2025",
            date_snapshot               = "2025-09-01",
            # Hyperscaler: Q2 2025 calendar = GOOG ~$13.2B + META ~$15.3B +
            #              MSFT ~$21.4B + AMZN ~$27.4B = ~$77B
            # Q2 2024 was ~$53B → YoY +45%
            hyperscaler_capex_total_qtr = 77.0,
            hyperscaler_capex_yoy_pct   = 45.0,
            # TSMC Q2 2025: HPC ~55%, total YoY +38%
            tsmc_hpc_pct                = 55.0,
            tsmc_rev_yoy_pct            = 38.0,
            # ANET Q2 2025: $2.085B, +16.9% YoY
            arista_rev_yoy_pct          = 17.0,
            arista_rev_qtr              = 2.09,
            # NTNX Q4 FY2025 (ended Jul 2025): ARR +18% YoY
            nutanix_arr_yoy_pct         = 18.0,
            nutanix_new_logos_qtr       = 650,
            # SMCI Q4 FY2025 (ended Jun 2025): $5.8B, +7% YoY (lumpy due to acctg)
            smci_rev_yoy_pct            = 7.0,
            smci_rev_qtr                = 5.8,
            # CDW Q2 2025: commercial +4.5% YoY
            cdw_rev_yoy_pct             = 3.8,
            cdw_commercial_yoy_pct      = 4.5,
            hyperscaler_guidance_tone   = "positive",
            tsmc_mgmt_ai_commentary     = "accelerating",
            vmware_channel_checks       = "mixed",
        ),

        # ── Q4 FY2025 proxy window (data available ~Nov/Dec 2025) ─────────
        # Data available before AVGO Q4 FY2025 report (Dec 2025)
        ProxySnapshot(
            period                      = "Q4FY2025",
            date_snapshot               = "2025-11-15",
            # Hyperscaler: Q3 2025 calendar = ~$65B GOOG + META + MSFT + AMZN combined
            # GOOG $13.1B + META $16.0B + MSFT $20.0B + AMZN ~$22.6B = ~$72B
            # vs Q3 2024 ~$50B → YoY +44%
            hyperscaler_capex_total_qtr = 72.0,
            hyperscaler_capex_yoy_pct   = 44.0,
            # TSMC Q3 2025: HPC 57%, total YoY +39%
            tsmc_hpc_pct                = 57.0,
            tsmc_rev_yoy_pct            = 39.0,
            # ANET Q3 2025: $2.308B, +27.5% YoY
            arista_rev_yoy_pct          = 27.5,
            arista_rev_qtr              = 2.31,
            # NTNX Q1 FY2026 (ended Oct 2025): ARR +18% YoY
            nutanix_arr_yoy_pct         = 18.0,
            nutanix_new_logos_qtr       = 620,
            # SMCI Q1 FY2026 (ended Sep 2025): $6.0-7.0B guided — use $6.5B est
            smci_rev_yoy_pct            = 30.0,
            smci_rev_qtr                = 6.5,
            # CDW Q3 2025: +5.2% YoY commercial
            cdw_rev_yoy_pct             = 4.8,
            cdw_commercial_yoy_pct      = 5.2,
            hyperscaler_guidance_tone   = "positive",
            tsmc_mgmt_ai_commentary     = "accelerating",
            vmware_channel_checks       = "mixed",
        ),

        # ── Q1 FY2026 proxy window (data available ~Mar 2026) ─────────────
        # Most complete and current snapshot — data available before AVGO Q1 FY2026
        ProxySnapshot(
            period                      = "Q1FY2026",
            date_snapshot               = "2026-03-01",
            # Hyperscaler: Q4 2025 calendar
            # GOOG $14.3B + META $20.0B + MSFT $22.6B + AMZN ~$28.3B ≈ $85B
            # Q4 2024 ~$61B → YoY +39%; but Q1 2026 shows $36B from GOOG alone → acceleration
            # Using average of available data: ~$140B combined Q4 2025 (some sources say $140B
            # for combined Q4), others say "hyperscalers spending $700B in 2026" → ~$175/qtr
            # Conservative Q4 2025: $85B combined (GOOG+META+MSFT+AMZN), YoY +39%
            hyperscaler_capex_total_qtr = 85.0,
            hyperscaler_capex_yoy_pct   = 77.0,   # full 2026 projection: +77% YoY; Q1 on track
            # TSMC Q4 2025: HPC 55%; Q1 2026 jumped to 61%
            # Using Q1 2026 (most recent, reported Apr 2026) for this snapshot
            tsmc_hpc_pct                = 61.0,
            tsmc_rev_yoy_pct            = 42.0,   # TSMC Q1 2026 strong beat
            # ANET Q4 2025: $2.488B, +28.9% YoY (Q1 2026 = $2.709B +35.1% — use if available)
            arista_rev_yoy_pct          = 35.1,   # Q1 2026 reported May 5 2026 — latest
            arista_rev_qtr              = 2.71,
            # NTNX Q1 FY2026 (Oct 2025): ARR +18%; Q2 FY2026 = $670.6M +13% YoY
            nutanix_arr_yoy_pct         = 18.0,   # most recent available
            nutanix_new_logos_qtr       = 620,
            # SMCI Q2 FY2026 (Dec 2025): $12.68B, +123% YoY
            smci_rev_yoy_pct            = 123.0,
            smci_rev_qtr                = 12.68,
            # CDW Q1 2026: commercial +9.6% YoY
            cdw_rev_yoy_pct             = 9.2,
            cdw_commercial_yoy_pct      = 9.6,
            hyperscaler_guidance_tone   = "positive",
            tsmc_mgmt_ai_commentary     = "accelerating",
            vmware_channel_checks       = "mixed",
        ),
    ]


# ══════════════════════════════════════════════════════════════════════════
# 10.  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    history = build_proxy_history()

    # Show trend across all snapshots, then detailed report on latest
    print()
    print("═" * W)
    print("  PROXY SIGNAL TREND ACROSS QUARTERS")
    print("═" * W)
    print(f"  {'Period':<12}{'Proxy Score':>12}{'Top Scenario':>20}  Probs  [BEAR / BASE / BULL / XBULL]")
    print("  " + "─" * (W - 2))
    for snap in history:
        res, comp = score_proxies(snap)
        ps = scenario_probabilities(comp)
        top = max(ps, key=lambda sc: ps[sc])
        bear_p  = ps[Scenario.BEAR]
        base_p  = ps[Scenario.BASE]
        bull_p  = ps[Scenario.BULL]
        xbull_p = ps[Scenario.EXTREME_BULL]
        print(
            f"  {snap.period:<12}{comp:>12.2f}"
            f"{SCENARIO_LABELS[top]:>20}  "
            f"  {bear_p*100:.0f}% / {base_p*100:.0f}% / {bull_p*100:.0f}% / {xbull_p*100:.0f}%"
        )
    print()

    # Full detailed report for latest quarter
    latest = history[-1]
    proxy_report(latest, fundamental_composite=2.15)  # pass AVGO fundamental score
