# Selection inside the growth and value baskets (hindsight)

**The question:** inside `STYLE_SWITCH.md`'s monthly GROWTH and VALUE baskets (about seven names each, out of
twenty-four), does any point-in-time reading pick the better members? And does picking them improve the yield-switched
book?

**21 readings tested** (`basket_selection.py`):
- **EPS trend:**
  - quarterly growth and its acceleration;
  - the last fiscal year's growth;
  - the 6-month change in the floor's EPS (guidance or last year);
  - the number of falls among the last ten EPS years.
- **House model:** Ratio B, the EPP gap and its 6-month change, the BASE upside, the adjusted gap, the conservative
  two-year return, the dashboard, DURABLE or not.
- **Valuation and yield:** own P/E percentile, PEG, dividend yield and dividend growth.
- **Price:** 1-month reversal, 12-1 momentum, distance below the 52-week high, volatility.

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number is printed by `python3 staging/retrospective/basket_selection.py`.
- **Fixed in advance:** the readings, the replication rule (same sign in 2008-2016 and 2017-2026, |t| >= 2 over the
  full period) and the books, in its docstring.
- **Added after the first run:** the `posthoc` section, labelled so.

## 1. Almost nothing replicates: 2 of 42 tests, about what chance gives

Rank correlation between a reading and the members' next six months, inside each basket:

| Basket | Reading | 2008-2016 | 2017-2026 | Full | t | Replicates? |
|---|---|---|---|---|---|---|
| VALUE | peg (higher did better; 81 months with data) | +0.068 | +0.192 | +0.145 | +2.02 | yes |
| VALUE | e2_rev (an EPS cut did better) | -0.079 | -0.109 | -0.094 | -1.97 | just missed |
| VALUE | eps_downyears (more down-years did better) | +0.133 | +0.086 | +0.109 | +1.90 | just missed |
| VALUE | rb (Ratio B) | -0.098 | +0.114 | +0.011 | +0.21 | no |
| VALUE | epp_gap | +0.017 | +0.076 | +0.047 | +1.10 | no |
| VALUE | eps_q_g (quarterly EPS growth) | -0.114 | -0.007 | -0.060 | -1.44 | no |
| GROWTH | pe_pctl (dearer vs own history did better) | +0.149 | +0.077 | +0.112 | +2.33 | yes |
| GROWTH | epp_gap (further above the floor did better) | +0.081 | +0.122 | +0.102 | +1.75 | no |
| GROWTH | eps_downyears | -0.029 | +0.226 | +0.112 | +1.95 | no (the halves disagree) |
| GROWTH | rb (Ratio B) | -0.002 | -0.006 | -0.004 | -0.08 | no |
| GROWTH | eps_q_g | -0.046 | +0.089 | +0.023 | +0.53 | no |

The script prints all 21 readings for both baskets.
- **Two passes in 42 tests is about chance.** At |t| >= 2 with the sign held in both halves, one or two were expected
  anyway.
- **Ratio B, the EPP distance and the quarterly EPS trend picked nothing inside either basket.**
- **The near-misses tell one story:**
  - Inside **value**, the worse fundamentals did better: an EPS cut, more down-years, a higher PEG. That is the value
    bounce from the trough (`RATIO_B_EPS_24.md` found the same for falling-EPS shorts).
  - Inside **growth**, the dearer stocks did better: own P/E percentile, EPP gap. That is momentum in growth.
- **Over one month the signals barely register:** next-month correlations of +0.019 to +0.092.

## 2. As books: picking did not beat holding the whole basket

Rebalanced monthly, as fixed in advance (annual return / Sharpe / worst drawdown, 2008-2026):

| Book | Result |
|---|---|
| VALUE, whole basket | +15.5% / 0.83 / -39% |
| VALUE, best 3 by PEG | +12.6% / 0.70 / -47% |
| GROWTH, whole basket | +19.8% / 0.90 / -57% |
| GROWTH, best 3 by own P/E percentile | +19.1% / 0.77 / -56% |
| **Y6 switch, whole baskets** (`STYLE_SWITCH.md`) | **+22.0% / 1.11 / -37%** |
| Y6 switch, picked baskets (PEG in value, P/E percentile in growth) | +21.3% / 0.93 / -50% |
| SPY | +11.1% / 0.69 / -51% |

**Post-hoc: six-month holds and a contrarian-value / strong-growth switch.** Chosen after the table above; leads, not
findings.

| Book (6-month cohorts) | 2008-2026 | 2008-2016 | 2017-2026 |
|---|---|---|---|
| VALUE, whole basket | +13.5% / 0.77 / -41% | +14.8% / 0.82 | +12.2% / 0.72 |
| VALUE, 3 whose floor EPS was just cut | +15.2% / 0.76 / -48% | +16.5% / 0.78 | +14.0% / 0.74 |
| VALUE, best 3 by PEG | +11.6% / 0.67 / -50% | +9.5% / 0.55 | +13.6% / 0.80 |
| GROWTH, whole basket | +20.7% / 0.94 / -53% | +17.4% / 0.79 | +23.9% / 1.09 |
| GROWTH, best 3 by own P/E percentile | +22.4% / 0.91 / -51% | +21.2% / 0.86 | +23.6% / 0.97 |
| **Y6 switch, whole baskets** | **+21.3% / 1.08 / -33%** | +20.3% / 0.96 / -33% | +22.1% / 1.23 / -22% |
| Y6 switch, value EPS-cut 3 / growth P/E-percentile 3 | +22.1% / 1.02 / -42% | +18.9% / 0.83 / -42% | +25.1% / 1.26 / -18% |

**Picking three names added about 1-2 points a year at best,** with the same or lower Sharpe and deeper drawdowns.
Holding the whole basket was as good on a risk-adjusted basis.

## Summary

1. **No reliable selection signal inside the baskets.** EPS trend, Ratio B and the EPP distance all failed the
   replication test. The two passes are within chance.
2. **The consistent hint:** inside value, buy the ones whose earnings just fell (a bounce from the trough); inside
   growth, the ones already being re-rated (dearest against their own history). It is worth a fresh test, but not
   proven.
3. **The best book stays the simplest:** hold the whole basket the 10-year yield trend points to. That was +22.0% a
   year, Sharpe 1.11, worst drawdown -37%, rebalanced monthly. Diversification across about seven names beat picking
   three.

## The newest month (October 2026); the Y6 rule says VALUE

| Basket | Members | Best 3 by the passing reading |
|---|---|---|
| VALUE | CMCSA, NKE, LOW, PEP, LMT, PFE, BMY | by PEG: PFE, PEP, LOW |
| GROWTH | NVDA, AVGO, AAPL, CAT, MAR, MSFT, WMT | by own P/E percentile: AAPL, CAT, AVGO |

These are hindsight hypotheses applied to point-in-time data, not advice.

## Limits

- **Small baskets:** about seven names a month, so each monthly correlation is noisy.
- **Many tests:** 42 in the first run, plus the post-hoc rows.
- **Survivorship:** the twenty-four were picked in 2026.
- **Not modelled:** costs and taxes.
