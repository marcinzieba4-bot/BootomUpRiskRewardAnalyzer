# Long the three highest own P/E percentiles, with a tactical S&P 500 hedge (hindsight)

**The book:**
- **Long:** the three of the twenty-four tickers trading highest against their own 10-year P/E history (PE_NOW_PCTL),
  the most balanced pattern in `PATTERN_SEARCH_24.md`. Each monthly cohort is held six months.
- **Hedge:** short SPY while the S&P 500 closes below its 100-day average (`RATIO_B_HEDGE.md`'s rule), at full or half
  size.

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number is printed by `python3 staging/retrospective/pe_pctl_hedge.py`.
- **Data:** daily total-return data, 2008-01-07 to 2026-11-17, all twenty-four tickers (`RETRO_UNIVERSE=all`).
- **Execution:** entry and hedge trades at the next day's close; no cash interest or borrow fees.
- **Fixed in advance:** the rules and every variant, in the script's docstring.

**Ties.** In 71 of 226 months (31%) more than three tickers stood at or above the third-place percentile, often at 99
or 100. The main book splits a tied place equally among the tied names. The pattern search's alphabetical tie-break is
shown beside it; it gives about the same result (+21.0% unhedged against +21.5%).

## 1. The result, all twenty-four

Annual return / Sharpe / worst drawdown:

| Book | Hedge | Full period | 2008-2016 | 2017-2026 | Beta | Days hedged |
|---|---|---|---|---|---|---|
| SPY | - | +11.1% / 0.63 / -51% | +7.5% / 0.45 / -51% | +14.6% / 0.84 / -34% | 1.00 | - |
| EQUAL (all 24) | none | +17.1% / 0.89 / -47% | +15.5% / 0.78 | +18.7% / 1.03 | 0.96 | - |
| EQUAL (all 24) | S&P 100-day, 50% | +15.8% / 1.09 / -27% | +14.3% / 0.96 | +17.1% / 1.21 | 0.62 | 26% |
| EQUAL (all 24) | S&P 100-day, 100% | +13.7% / 1.10 / -16% | +12.2% / 0.98 | +15.1% / 1.22 | 0.28 | 26% |
| **Top 3 own P/E percentile** | none | **+21.5% / 0.97 / -49%** | +21.1% / 0.95 | +21.9% / 1.00 | 0.97 | - |
| **Top 3** | **S&P 100-day, 50%** | **+20.1% / 1.09 / -33%** | +19.6% / 1.07 / -29% | +20.5% / 1.10 / -33% | 0.63 | 26% |
| Top 3 | S&P 200-day, 50% | +20.4% / 1.09 / -32% | +20.9% / 1.12 | +20.1% / 1.06 | 0.64 | 23% |
| Top 3 | S&P 100-day, 100% | +17.9% / 1.04 / -35% | +17.2% / 0.99 | +18.5% / 1.10 | 0.29 | 26% |
| Top 3 | static 50% SPY short | +15.8% / 1.03 / -27% | +17.2% / 1.10 | +14.5% / 0.96 | 0.47 | 100% |
| Top 3, rebalanced monthly | S&P 100-day, 50% | +17.7% / 0.92 / -40% | +20.0% / 1.03 | +15.7% / 0.83 | 0.60 | 26% |

- **A half-size hedge was the best balance.** It cost 1.4 points a year against the unhedged book, raised the Sharpe
  from 0.97 to 1.09, and cut the worst drawdown from -49% to -33%. The 200-day average did the same with fewer trades.
- **The pick added return, not risk-adjusted return.** With the same half hedge, the top three made +20.1% against
  EQUAL's +15.8%, at the same Sharpe (1.09). EQUAL's drawdown was shallower (-27%).
- **Held six months beat rebalancing monthly** (+20.1% against +17.7% hedged).
- **Within the twenty-four, the pick beat chance.** Against 200 runs of three random tickers a month, with the same
  cohorts:

  | | Random 5th-95th percentile | Random median | Top 3 | Random runs at or above |
  |---|---|---|---|---|
  | Unhedged | +14.1% to +19.4% | +16.6% | +21.5% | 1 of 200 |
  | Half hedge | +12.8% to +18.0% | +15.2% | +20.1% | 1 of 200 |

  But this signal was chosen from sixteen in the pattern search on the same twenty-four tickers, so the random test
  cannot remove that selection.

## 2. By universe (top 3 with the half hedge)

| Universe | EQUAL + half hedge | **Top 3 + half hedge** | Top 3 unhedged |
|---|---|---|---|
| ALL twenty-four | +15.8% / 1.09 / -27% | **+20.1% / 1.09 / -33%** | +21.5% / 0.97 / -49% |
| ORIGINAL eleven | +16.5% / 1.17 / -20% | +19.5% / 1.10 / -31% | +21.0% / 0.97 / -49% |
| NEW thirteen | +14.6% / 0.88 / -38% | +15.6% / 0.80 / -39% | +17.0% / 0.76 / -54% |
| ALL without tech | +12.5% / 0.89 / -30% | +13.6% / 0.88 / -30% | +15.2% / 0.80 / -40% |

On the new thirteen and without tech, the pick added only about one point a year over the hedged equal-weight basket,
at a slightly lower Sharpe. Most of the edge on all twenty-four comes from the tech names. Tech made up 38% of the
book's weight (AVGO 11%, MSFT 10%, AAPL 8%, NVDA 6%, ACN the rest), but supplied 60% of its summed monthly returns.
NVDA alone supplied 27%; MSFT 15%, AVGO 11%. These figures were computed after the run and are not printed by the
script.

## 3. Crashes, and the year it failed

| SPY peak - trough | SPY | Top 3 | Top 3 + full hedge | Top 3 + half hedge |
|---|---|---|---|---|
| 2008-05 - 2009-03 | -51.5% | -46.7% | -0.9% | -25.7% |
| 2011-04 - 2011-10 | -18.6% | -10.7% | +4.5% | -3.1% |
| 2018-09 - 2018-12 | -19.3% | -24.5% | -12.6% | -18.6% |
| 2020-02 - 2020-03 | -33.7% | -29.1% | -1.4% | -15.8% |
| **2022-01 - 2022-10** | -24.5% | **-32.3%** | **-26.3%** | **-29.0%** |
| 2025-02 - 2025-04 | -18.8% | -22.9% | -9.0% | -16.1% |

- **The hedge did its job in the fast crashes** (2008, 2020, 2011).
- **2022 is the failure.** The dear-against-history stocks fell 28.7% that year while EQUAL lost 5.2%. The hedge barely
  helped, as in `RATIO_B_HEDGE.md`: the S&P 500 rose on the days the hedge was on.
- **Over calendar years:** positive in 16 of 19 unhedged, 16-17 hedged. The worst year is 2022 (-29% hedged); 2026 is
  -2% to date.

## 4. Costs

- **Trading:** the book turns over about 217% a year; the 100-day hedge opens or closes 11.2 times a year.
- **At 0.10% a trade:** the half-hedged book makes +19.2% (Sharpe 1.04, worst drawdown -34%). The 200-day version makes
  +19.8% (Sharpe 1.06).

## Summary

1. **Long the three highest own P/E percentiles, held six months, with a half-size S&P 100-day hedge:**
   - before costs: +20.1% a year, Sharpe 1.09, worst drawdown -33%;
   - after 0.10% costs: about +19%.
   - For comparison: SPY +11.1% / -51%, EQUAL +17.1% / -47%.
2. **The hedge does the risk work; the pick adds return.** With the same hedge, the pick beat EQUAL by about 4 points a
   year at the same Sharpe. That rests mostly on the tech names; without tech it added about one point.
3. **It is a growth-style bet,** and it lost 29% in 2022 when that style turned. The hedge did not save it that year.

## Now

**Newest readings (highest own P/E percentile first):** AAPL 100, UNP 98, WMT 97, RCL 92, CAT 90, AVGO 87, XOM 87.

**The last monthly cohort (October 2026):** AAPL 33%, CAT 33%, UNP 17%, AVGO 17%. UNP and AVGO share the third place
at 87.

**The hedge is ON:** the S&P 500 closed at 7,334.31 on 2026-11-17, 3.8% below its 100-day average.

These are hindsight hypotheses applied to point-in-time data, not advice.

## Limits

- **Survivorship:** the twenty-four were chosen in 2026, and EQUAL alone beat SPY by 6 points a year.
- **Selection:** this signal was the pick of a sixteen-signal search on the same tickers.
- **Concentration:** three names.
- **Period:** the result covers a growth-led era.
