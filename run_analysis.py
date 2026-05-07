#!/usr/bin/env python3
"""
AVGO Combined Analysis Runner
─────────────────────────────
Runs the fundamental tracker and proxy/alt-data model together,
producing a single blended scenario probability output.

    python run_analysis.py
"""

from avgo_tracker   import build_tracker, score_quarter
from avgo_proxy_model import (
    build_proxy_history, proxy_report, score_proxies,
    scenario_probabilities, blended_score, W,
    Scenario, SCENARIO_LABELS,
)

def main() -> None:
    # ── Fundamental model ────────────────────────────────────────────────
    tracker = build_tracker()
    _, _fundamental_scenario, fundamental_composite = score_quarter(tracker.latest, tracker.previous)

    # ── Proxy model ──────────────────────────────────────────────────────
    proxy_history = build_proxy_history()
    # Align: use proxy snapshot whose period matches the latest AVGO quarter
    latest_proxy = next(
        (p for p in reversed(proxy_history) if p.period == tracker.latest.period),
        proxy_history[-1],  # fallback to most recent
    )
    _, proxy_composite = score_proxies(latest_proxy)

    # ── Print fundamental report first ───────────────────────────────────
    tracker.report()

    # ── Print proxy report with fundamental context ──────────────────────
    proxy_report(latest_proxy, fundamental_composite=fundamental_composite)

    # ── Final blended summary ─────────────────────────────────────────────
    blended, probs = blended_score(proxy_composite, fundamental_composite)
    top_sc = max(probs, key=lambda sc: probs[sc])

    price_map = {
        Scenario.BEAR:         187.0,
        Scenario.BASE:         526.0,
        Scenario.BULL:         770.0,
        Scenario.EXTREME_BULL: 1080.0,
    }
    ev = sum(probs[sc] * price_map[sc] for sc in Scenario)
    current = tracker.latest.stock_price or 417.0
    updown  = (ev / current - 1) * 100

    print()
    print("═" * W)
    print("  FINAL BLENDED VERDICT")
    print("═" * W)
    print()
    print(f"  Fundamental score (AVGO own data)  : {fundamental_composite:.2f} / 4.00")
    print(f"  Proxy score (leading indicators)   : {proxy_composite:.2f} / 4.00")
    print(f"  Blended score (60/40)              : {blended:.2f} / 4.00")
    print()
    print(f"  Most likely scenario  : {SCENARIO_LABELS[top_sc]}  ({probs[top_sc]*100:.0f}%)")
    print()
    print(f"  {'Scenario':<22}{'Probability':>12}  {'2-yr Target':>12}")
    print("  " + "─" * 48)
    for sc in Scenario:
        marker = " ◀" if sc == top_sc else ""
        print(f"  {SCENARIO_LABELS[sc]:<22}{probs[sc]*100:>11.1f}%  ${price_map[sc]:<10.0f}{marker}")
    print("  " + "─" * 48)
    print(f"  {'Probability-weighted EV':<22}{ev:>13.0f}$")
    sign = "+" if updown >= 0 else ""
    print(f"  {'vs current (~$417)':<22}{sign}{updown:.0f}%  expected return (2yr)")
    print()
    print("  KEY TENSION IN THE DATA:")
    print("  ─────────────────────────────────────────────────────")
    print(f"  Proxy signals ({proxy_composite:.2f}) are significantly more bullish than")
    print(f"  AVGO's own reported fundamentals ({fundamental_composite:.2f}). This is the")
    print(f"  classic 'ramp gap' — the leading data sees the AI capex wave;")
    print(f"  AVGO's P&L hasn't fully absorbed it yet. The bet is on convergence:")
    print(f"  either fundamentals catch up to proxies (bull case) or proxies")
    print(f"  mean-revert to fundamentals (bear case for the multiple).")
    print()
    print("═" * W)
    print()


if __name__ == "__main__":
    main()
