# The three lowest Ratio B stocks with a tactical S&P 500 hedge (hindsight), 2008-2026

**The long book:** RANK3's long leg from `RATIO_B_BASKET.md`. Each month, buy the three of the eleven tickers with the
lowest point-in-time Ratio B, in equal weight.

**The hedge:**
- **Open:** when the S&P 500 index closes below its 100-day moving average, short SPY equal to 100% of the portfolio.
- **Close:** once it closes back above the average.
- **Execution:** each trade happens at the next trading day's close after the signal. The short pays SPY's dividends.
  Interest on the short proceeds, borrow fees and commissions are not modelled.

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number is printed by `python3 staging/retrospective/ratio_b_hedge.py` (one section: `... ratio_b_hedge.py summary`),
from daily total-return data, 2008-01-07 to 2026-11-06 (18.8 years). The rules, the comparisons and the sensitivity runs
were fixed in the script's docstring before the first run. The "worst" section was added afterwards.

## 1. The result

| Strategy | Annual return | Volatility | Sharpe | Worst drawdown | Return / drawdown | Beta to SPY | Days hedged | Hedge entries a year |
|---|---|---|---|---|---|---|---|---|
| SPY | +11.2% | 19.7% | 0.64 | -51% | 0.22 | +1.00 | | |
| EQUAL (all eleven) | +17.9% | 19.1% | 0.96 | -37% | 0.49 | +0.89 | | |
| LONG3, unhedged | **+31.1%** | 23.1% | 1.29 | -35% | 0.89 | +0.88 | | |
| LONG3, always short SPY | +17.4% | 15.3% | 1.12 | -31% | 0.56 | -0.12 | 100% | |
| **LONG3 + tactical hedge (100-day)** | **+27.0%** | **18.0%** | **1.41** | **-28%** | **0.97** | +0.21 | 26% | 5.6 |
| The hedge leg alone | -5.4% | 16.2% | -0.26 | -79% | | -0.68 | 26% | 5.6 |
| EQUAL + tactical hedge | +14.3% | 12.4% | 1.14 | -16% | 0.87 | +0.21 | 26% | 5.6 |

- **The hedge traded about 4 points of return for a smoother ride.**
  - Return fell from 31.1% to 27.0% a year.
  - Volatility fell from 23.1% to 18.0%, the worst drawdown from -35% to -28%, and beta from 0.88 to 0.21.
  - Sharpe rose from 1.29 to 1.41.
- **Tactical beat always-hedged on every measure:** +27.0% against +17.4%, Sharpe 1.41 against 1.12, drawdown -28%
  against -31%.
- **The hedge on its own lost money: -5.4% a year, and 16 of 19 calendar years.** It is insurance. Its median spell
  lasted only **2 trading days**, with 5.6 entries a year: most signals were whipsaws around the average.
- **Robust to the long book's members:** with each ticker left out in turn, the hedged strategy returned +20.6% (no AVGO)
  to +27.6% (no NKE), with worst drawdowns of -22% to -30%.

## 2. Crashes: it paid; rebounds: it gave some back

Every SPY drawdown of 15% or more, peak to trough, then the six months after the trough:

| SPY peak - trough | SPY | LONG3 | **LONG3 hedged** | Days hedged | 6 months after: SPY | LONG3 | **LONG3 hedged** |
|---|---|---|---|---|---|---|---|
| 2008-05-19 - 2009-03-09 | -51.5% | -22.2% | **+45.8%** | 93% | +51.8% | +42.2% | +9.2% |
| 2011-04-29 - 2011-10-03 | -18.6% | -2.6% | **+13.7%** | 65% | +29.9% | +43.4% | +16.0% |
| 2018-09-20 - 2018-12-24 | -19.3% | -19.7% | **-7.2%** | 77% | +25.1% | +28.3% | +8.7% |
| 2020-02-19 - 2020-03-23 | -33.7% | -34.2% | **-8.0%** | 78% | +47.9% | +84.6% | +36.3% |
| 2022-01-03 - 2022-10-12 | -24.5% | +3.9% | **+11.9%** | 80% | +16.7% | +31.3% | +14.1% |
| 2025-02-19 - 2025-04-08 | -18.8% | -17.2% | **-2.5%** | 76% | +36.4% | +26.6% | +6.8% |

- **In every crash the hedged book lost far less, or gained.** It was on for 65-93% of each fall.
- **In every rebound it lagged,** because the short stays on until the index is back above its 100-day average, after
  the low. In the six months after the 2020 trough it made +36.3% against the unhedged book's +84.6%.
- **Its worst drawdown was not a crash.** It was the choppy 2015 market: -28% from 2015-05-29 to 2015-12-18, recovered
  only on 2017-02-13. That year the hedge leg lost 13.7% while the long book made +1.3%. The unhedged book's worst was
  COVID: -35% from 2020-02-14 to 2020-03-18, recovered by 2020-05-20.

## 3. Calendar years

| Year | SPY | LONG3 | **LONG3 hedged** | Hedge leg | Days hedged | | Year | SPY | LONG3 | **LONG3 hedged** | Hedge leg | Days hedged |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2008 | -34.6% | +18.3% | **+65.7%** | +21.9% | 86% | | 2018 | -4.6% | +10.1% | +9.5% | -2.4% | 36% |
| 2009 | +26.4% | +43.8% | +45.3% | -2.1% | 26% | | 2019 | +31.2% | +41.7% | +20.9% | -15.2% | 18% |
| 2010 | +15.1% | +31.9% | +17.7% | -12.0% | 37% | | 2020 | +18.4% | +37.1% | +37.5% | -9.3% | 26% |
| 2011 | +1.9% | +19.8% | +12.7% | -8.7% | 38% | | 2021 | +28.7% | +63.0% | +59.1% | -2.4% | 2% |
| 2012 | +16.0% | +21.0% | +5.4% | -13.5% | 25% | | 2022 | -18.2% | +28.9% | +24.6% | -7.3% | 75% |
| 2013 | +32.3% | +32.7% | +23.0% | -7.4% | 4% | | 2023 | +26.2% | +32.2% | +25.0% | -5.8% | 20% |
| 2014 | +13.5% | +39.2% | +29.1% | -7.5% | 8% | | 2024 | +24.9% | +48.4% | +45.4% | -2.1% | 1% |
| 2015 | +1.3% | +1.3% | **-11.3%** | -13.7% | 31% | | 2025 | +17.7% | +13.4% | +11.0% | -4.3% | 20% |
| 2016 | +12.0% | +26.9% | +21.3% | -5.2% | 26% | | 2026 | +8.7% | +34.6% | +36.9% | +1.3% | 13% |
| 2017 | +21.7% | +56.0% | +56.0% | +0.0% | 0% | | | | | | | |

- **Positive years:** LONG3 19 of 19; hedged 18 of 19; SPY 16 of 19.
- **Years beating SPY:** LONG3 18 of 19; hedged 13 of 19; always hedged 8 of 19.
- **2022 is a surprise:** the hedge was on 75% of the year, the long book rose 28.9%, and the hedge still lost 7.3%.
  SPY rose 2.8% over the 187 days the short was on and fell 20.4% over the 64 days it was off. Most of the fall came
  in sharp drops just after a rally had lifted the index back above its average and closed the short (computed
  separately, not printed by the script).

Sub-periods (annual return / worst drawdown):

| Strategy | 2008-2012 | 2013-2017 | 2018-2022 | 2023-2026 |
|---|---|---|---|---|
| SPY | +2.4% / -51% | +15.7% / -13% | +9.3% / -34% | +20.1% / -19% |
| LONG3 | +26.7% / -34% | +30.0% / -24% | +35.1% / -35% | +33.1% / -20% |
| LONG3 hedged | +27.6% / -20% | +21.7% / -28% | +29.3% / -16% | +30.3% / -20% |

## 4. Sensitivity (fixed before the first run)

| Variant | Annual return | Volatility | Sharpe | Worst drawdown | Return / drawdown | Days hedged | Entries a year | Median spell |
|---|---|---|---|---|---|---|---|---|
| 100-day, 100% hedge, next-day close (main) | +27.0% | 18.0% | 1.41 | -28% | 0.97 | 26% | 5.6 | 2 days |
| **100-day, 50% hedge** | **+29.4%** | 19.1% | **1.45** | **-26%** | **1.15** | 26% | 5.6 | 2 |
| 100-day, traded at the signal day's own close | +26.8% | 18.0% | 1.41 | -28% | 0.96 | 26% | 5.6 | 2 |
| 50-day average | +24.0% | 18.0% | 1.29 | -24% | 0.99 | 31% | 8.9 | 3 |
| 200-day average | +27.9% | 18.3% | 1.44 | -29% | 0.95 | 23% | 2.9 | 4 |

- **A half hedge did better on every risk-adjusted measure.** The long book's beta to SPY is about 0.9, but most of the
  hedge's cost is whipsaw, and a half hedge pays half of it.
- **The 200-day average traded half as often** (2.9 entries a year) and slightly beat the 100-day. The 50-day traded
  most and returned least.
- **Trading at the signal day's own close changed almost nothing.**

## Hypotheses (test before use)

1. **Size the hedge at about half the book,** or test a beta-matched size. A full hedge paid too much in whipsaws.
2. **Filter whipsaws.** The median spell was 2 days. A confirmation (several closes below, or a band around the
   average) is the obvious next test, but it is a new parameter and must be fixed before it is run.
3. **Add the cash rate on the short proceeds.** It is not counted here and would add a little to every hedged variant.

## Where it sits now

On 2026-11-06 the S&P 500 closed at 7,376.86, 3.2% below its 100-day average of 7,618.70, so the rule's hedge is **on**.
The long book held since the last monthly entry is ACN, LOW and AVGO. ACN is the open disruption case
(`RATIO_EPP_FINDINGS.md` section 4). This is the rule applied to point-in-time data, not advice.

## Limits

- **Survivorship.** The long book picks from eleven companies chosen in 2026; the unhedged +31.1% a year is mostly that.
  The hedge results (what it saved in crashes, what it cost in whipsaws) depend much less on the stocks.
- **Costs.** 5.6 hedge entries a year means about 11 SPY trades a year at full notional, roughly 0.2 points a year at
  0.02% a trade. The long book's monthly turnover is in `RATIO_B_BASKET.md`.
- **Six market drawdowns** are the whole crash record. The 100-day rule happened to catch long falls (2008, 2022) and
  fast ones (2020, 2025) alike; a faster crash could beat its lag.
