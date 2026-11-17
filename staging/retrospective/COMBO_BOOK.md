# Growth picks and value picks in one book, tilted by the 10-year yield (hindsight)

**The question:** hold the growth-basket selection and the value-basket selection together, then apply the yield filter.
Does that beat switching all the way (`TILT_SWITCH.md`), or holding the whole baskets?

**The book:**
- **Growth sleeve:** the 2 growth-basket members trading highest against their own P/E history.
- **Value sleeve:** the 2 value-basket members whose floor EPS fell most over 26 weeks.
- **Yield filter (Y6):** when the 10-year yield is above its level 6 months earlier, 75% goes to the value sleeve and
  25% to growth. Otherwise the reverse.

**Both selections are post-hoc:** they came from `BASKET_SELECTION.md`'s near-misses and were then swept in
`TILT_SWITCH.md`. This test adds no new selection rule.

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number is printed by `python3 staging/retrospective/combo_book.py`, from daily total-return data, 2008-01-07 to
2026-11-17. The books, settings and the main configuration were fixed in its docstring before the first run.
- **Main configuration:** a 1-month hold with a 15% trailing stop, after 0.10% costs.
- **The other settings:** 1-month and 3-month holds, each with and without a stop.

## 1. Main configuration

Annual return / Sharpe / worst drawdown, after costs:

| Book | 2008-2026 | 2008-2016 | 2017-2026 | Beta |
|---|---|---|---|---|
| Growth picks alone | +26.9% / 0.98 / -53% | +27.0% / 0.98 / -53% | +26.8% / 0.98 / -44% | 0.95 |
| Value picks alone | +20.1% / 0.89 / -38% | +15.0% / 0.68 / -36% | +24.8% / 1.10 / -38% | 0.75 |
| Combined 50/50 (no filter) | +25.0% / 1.13 / -42% | +21.9% / 0.96 / -42% | +27.8% / 1.31 / -29% | 0.85 |
| **Combined + yield tilt 75/25** | **+27.5% / 1.19 / -39%** | +23.7% / 1.00 / -39% | +31.0% / 1.39 / -30% | 0.83 |
| Yield switch 100/0 | +29.3% / 1.14 / -37% | +25.0% / 0.97 / -37% | +33.3% / 1.31 / -35% | 0.80 |
| Whole baskets 50/50 | +14.9% / 0.87 / -45% | +13.5% / 0.76 / -45% | +16.2% / 1.00 / -27% | 0.79 |
| Whole baskets + yield tilt | +16.5% / 0.94 / -40% | +14.8% / 0.80 / -40% | +18.1% / 1.10 / -25% | 0.78 |
| Whole-basket switch | +17.9% / 0.95 / -37% | +16.0% / 0.82 / -37% | +19.7% / 1.11 / -24% | 0.76 |
| SPY | +11.1% / 0.63 / -51% | +7.5% / 0.45 / -51% | +14.6% / 0.84 / -34% | 1.00 |

**Picking beat holding the baskets.**
- **Combined:** +25.0% a year held 50/50, against +14.9% for the whole baskets.
- **Each sleeve beat its own basket in both halves:**

  | Sleeve | 2008-2016 | 2017-2026 |
  |---|---|---|
  | Growth picks | +27.0% (basket +14.2%) | +26.8% (basket +19.6%) |
  | Value picks | +15.0% (basket +12.0%) | +24.8% (basket +11.7%) |

  At 6-month holds with no stop, picking had added only 1-2 points (`BASKET_SELECTION.md`).

**The yield tilt added about 2.5 points a year** over 50/50, with the best Sharpe of any book here (1.19) and a Sortino
of 1.78.
- **Going all in (the switch) made more:** +29.3% a year.
- **But it swung harder:** volatility 25.4% against 22.6%, and a Sharpe of 1.14.
- **The tilt with the half hedge:** +24.2% / 1.21 / -29%.

## 2. Why the filter works: each sleeve inside the yield regimes

1-month hold, no stop, before costs, annualised. Y6 favoured VALUE on 50% of days.

| Held | Yields rising (VALUE) | Yields falling (GROWTH) |
|---|---|---|
| Growth picks | +14.2% | **+44.7%** |
| Value picks | **+18.9%** | +25.6% |
| Whole growth basket | +10.1% | +30.2% |
| Whole value basket | +14.2% | +16.9% |
| SPY | +7.5% | +14.9% |

- **The filter ranked the sleeves right in both regimes.** Value picks led by about 5 points while yields rose; growth
  picks led by about 19 points while yields fell.
- **The value picks did better in falling-yield spells too.** So the filter's gain comes mostly from holding less growth
  when yields rise, and more growth when they fall.

## 3. Detailed statistics (main configuration, after costs)

| Statistic | Combined + yield tilt | Combined 50/50 | Yield switch | Whole-basket switch | SPY |
|---|---|---|---|---|---|
| Annual return | +27.5% | +25.0% | +29.3% | +17.9% | +11.1% |
| $1 became | $96.6 | $66.4 | $126.4 | $22.3 | $7.3 |
| Volatility | 22.6% | 21.9% | 25.4% | 19.2% | 19.7% |
| Sharpe / Sortino | 1.19 / 1.78 | 1.13 / 1.67 | 1.14 / 1.73 | 0.95 / 1.38 | 0.63 / 0.90 |
| Worst drawdown | -38.7% (Sep 2008 to Mar 2009) | -41.9% | -36.9% | -37.0% | -51.5% |
| Recovered | Apr 2009 | Aug 2009 | Apr 2009 | Nov 2009 | Apr 2011 |
| Longest under water | 1.8 yrs (from Jan 2018) | 1.3 yrs | 2.1 yrs | 1.3 yrs | 2.9 yrs |
| Calmar | 0.71 | 0.60 | 0.79 | 0.48 | 0.22 |
| Beta / correlation to SPY | 0.83 / 0.72 | 0.85 / 0.77 | 0.80 / 0.62 | 0.76 / 0.78 | 1.00 / 1.00 |
| Months positive / beating SPY | 65% / 59% | 67% / 62% | 65% / 56% | 65% / 57% | 66% / - |
| Worst month | -13.8% (Jan 2009) | -14.8% | -14.0% | -14.8% | -16.5% |
| Best / worst year | +88.6% (2020) / -21.2% (2018) | +74.6% / -18.3% | +101.1% / -24.2% | +43.2% / -14.7% | +32.3% / -34.6% |
| Years positive | 18 of 19 | 16 of 19 | 18 of 19 | 17 of 19 | 16 of 19 |

**Calendar years for the combined book with the tilt:**

| Year | Return | Year | Return | Year | Return | Year | Return |
|---|---|---|---|---|---|---|---|
| 2008 | +1.0% | 2013 | +30.3% | 2018 | **-21.2%** | 2023 | +29.7% |
| 2009 | +55.4% | 2014 | +26.5% | 2019 | +48.7% | 2024 | +56.1% |
| 2010 | +15.2% | 2015 | +17.9% | 2020 | +88.6% | 2025 | +7.8% |
| 2011 | +16.7% | 2016 | +36.5% | 2021 | +62.3% | 2026 to Nov 17 | +25.6% |
| 2012 | +20.5% | 2017 | +33.0% | 2022 | +9.6% | | |

**The weak years:**
- **2018:** yields rose all year (the filter was in value 94% of months), and the value picks fell.
- **2025:** +7.8% while SPY made +17.7%.

## 4. Robustness: other holds, stops and sleeve sizes

The script prints the full grid. After costs:

- **Three picks a sleeve in place of two cut the combined books by 4-9 points a year.** The combined + tilt book drops
  from +27.5% to +19.7% at 1 month with the stop, and from +23.9% to +19.6% at 3 months with re-entry. Most of the drop
  is in the growth sleeve (5-9 points) rather than the value sleeve (2-4). Much of the edge sits in very few names.
- **The 3-month hold with the stop and re-entry:** combined + tilt +23.9% / 1.21 / -34%, against 50/50 +22.2% / 1.16 /
  -38% and the switch +25.2% / 1.18 / -31%.
- **The tilt kept its edge over 50/50 in every setting tested (2 picks a sleeve):**

  | Setting | Gain over 50/50 |
  |---|---|
  | 1 month, no stop | +2.5 points |
  | 1 month, trailing stop | +2.5 points |
  | 3 months, no stop | +1.7 points |
  | 3 months, stop with re-entry | +1.7 points |

**Concentration:** a monthly attribution before stops, computed after the run.
- NVDA, AVGO, MSFT and AAPL were 30% of the combined book's weight but supplied 52% of its summed monthly returns. NVDA
  alone supplied 23%.
- Inside the growth sleeve they supplied 80%.

## Summary

1. **Combining the sleeves works better than holding whole baskets.** On this data the four picks beat the two whole
   baskets by about 10 points a year, in both halves.
2. **The yield filter is best used as a tilt (75/25), not a switch.** It gave the best risk-adjusted book: +27.5% a year,
   Sharpe 1.19, worst drawdown -39%, 18 of 19 years positive. The all-in switch earns about 2 points more with more
   swing.
3. **It is still a hindsight result.** The selections were found on this data, sit in 2 names a sleeve and lean on the
   tech winners. Expect far less live, and size it as a satellite.

## The newest month (October 2026, bought 2026-10-05): Y6 favours VALUE

| Stock | Sleeve | Weight | Why |
|---|---|---|---|
| NKE | value | 37.5% | floor EPS -42% in 26 weeks |
| LOW | value | 37.5% | floor EPS -2% |
| AAPL | growth | 12.5% | P/E at the 100th percentile of its own 10 years |
| CAT | growth | 12.5% | 97th percentile |

These are hindsight hypotheses applied to point-in-time data, not advice.
