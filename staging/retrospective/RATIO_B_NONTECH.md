# The Ratio B book without tech, hedged with the Dow or a Russell index (hindsight), 2008-2026

This is the strategy of `RATIO_B_HEDGE.md` with two changes:
- **No tech stocks.** The GICS Information Technology names (AAPL, AVGO, MSFT and ACN, IT services) are removed, leaving
  UNP, LOW, NKE, PEP, SHW, WMT and XOM.
- **Other hedge indices.** Each month the long book buys the three of those seven with the lowest point-in-time Ratio B.
  Its hedge shorts an ETF while that ETF's index closes below its 100-day average, entering and exiting at the next
  day's close. The pairs:
  - DIA on the Dow;
  - IWM on the Russell 2000;
  - IWB on the Russell 1000;
  - IWD on the Russell 1000 Value;
  - SPY on the S&P 500, for reference.

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number is printed by `python3 staging/retrospective/ratio_b_nontech.py`, from daily total-return data, 2008-01-07 to
2026-11-06. The rules and every variant were fixed in its docstring before the first run. Its S&P 500 hedge signal is
identical, day for day, to `ratio_b_hedge.py`'s.

## 1. The result

| Strategy | Annual return | Volatility | Sharpe | Worst drawdown | Days hedged | Hedge entries a year |
|---|---|---|---|---|---|---|
| SPY (S&P 500) | +11.2% | 19.7% | 0.64 | -51% | | |
| DIA (Dow) | +10.0% | 18.8% | 0.60 | -49% | | |
| IWM (Russell 2000) | +8.8% | 24.7% | 0.47 | -54% | | |
| Equal weight of the seven | +13.6% | 18.6% | 0.78 | -35% | | |
| **Ratio B book, unhedged** | **+16.9%** | 21.1% | 0.84 | -35% | | |
| + S&P 500 hedge, 100% / 50% | +13.1% / **+15.4%** | 16.4% / 17.1% | 0.83 / **0.92** | -28% / -28% | 26% | 5.6 |
| + Dow hedge, 100% / 50% | +12.0% / +14.8% | 15.8% / 17.0% | 0.79 / 0.90 | -29% / -28% | 29% | 6.5 |
| + Russell 2000 hedge, 100% / 50% | +11.0% / +14.5% | 17.9% / 17.0% | 0.67 / 0.88 | -30% / -29% | 34% | 6.9 |
| + Russell 1000 hedge, 100% / 50% | +13.6% / **+15.6%** | 16.4% / 17.1% | 0.86 / **0.93** | -28% / -28% | 26% | 5.3 |
| + Russell 1000 Value hedge, 100% / 50% | +11.5% / +14.6% | 16.4% / 17.0% | 0.75 / 0.89 | -30% / -29% | 30% | 6.4 |

- **Without tech, the strategy is a market-like return with a smaller worst fall.** Unhedged it made +16.9% a year
  (SPY +11.2%). Hedged it made +11.0% to +15.6%, with worst drawdowns of -28% to -30% against SPY's -51%.
- **A full hedge no longer improves the Sharpe ratio** (0.67-0.86 against 0.84 unhedged). **A half hedge does**, with
  every index (0.88-0.93).
- **The Russell 1000 was the best hedge, by a hair over the S&P 500.** It switched least (5.3 entries a year).
- **The Dow fits the book best but hedged worse.** The book's daily beta to the Dow is 0.87 and its correlation 0.77, the
  highest of the five. But the Dow's signal fired more often (29% of days), so it lost more to whipsaws.
- **The Russell 2000 was the best crash insurance and the worst overall.** The book's beta to it is only 0.60, so a full
  hedge over-hedges, and its signal was on 34% of the days.
- **Keeping ACN (eight tickers):** +19.7% unhedged, +13.7% to +16.4% fully hedged, +17.3% to +18.4% half hedged.

## 2. Crashes (every SPY drawdown of 15% or more, 100% hedges)

| SPY peak - trough | SPY | Book | + S&P 500 | + Dow | + Russell 2000 | + Russell 1000 | + Russell 1000 Value |
|---|---|---|---|---|---|---|---|
| 2008-05 - 2009-03 | -51.5% | -14.5% | +59.9% | +54.7% | +55.4% | +61.2% | +74.5% |
| 2011-04 - 2011-10 | -18.6% | -14.4% | -0.8% | -6.8% | +0.3% | -0.7% | +0.2% |
| 2018-09 - 2018-12 | -19.3% | -23.6% | -11.9% | -16.0% | **-0.9%** | -11.7% | -13.7% |
| 2020-02 - 2020-03 | -33.7% | -34.2% | -8.0% | -4.3% | **+2.2%** | -7.0% | +0.2% |
| 2022-01 - 2022-10 | -24.5% | -0.8% | +6.2% | +4.7% | **+17.1%** | +11.6% | +2.4% |
| 2025-02 - 2025-04 | -18.8% | -15.5% | -0.7% | -4.7% | **+7.6%** | +0.6% | -3.2% |

**Every hedge turned the falls into small losses or gains.** Small caps fall harder than these large caps, so shorting
the Russell 2000 paid most in a crash. Between crashes, the same mismatch cost it most.

Calendar years:
- **Positive years:** the unhedged book 16 of 19; the hedged versions 14-16 of 19.
- **Years beating SPY:** the unhedged book 11 of 19; the hedged versions 5-7.
- **Worst year:** 2015, when the unhedged book lost 13.9% and the S&P 500-hedged book 24.7%.
- **2026 to date:** the book is down (-3.5% unhedged).

## 3. Does Ratio B still add anything without tech?

Three random non-tech tickers a month, 300 runs, against the Ratio B book:

| Hedge | Random median | Random 95th percentile | **Ratio B book** | Runs at or above the book |
|---|---|---|---|---|
| none | +13.2% | +17.5% | **+16.9%** | 18 of 300 |
| S&P 500 | +9.5% | +13.5% | **+13.1%** | 17 of 300 |
| Dow | +8.3% | +12.4% | **+12.0%** | 17 of 300 |
| Russell 2000 | +7.4% | +11.4% | **+11.0%** | 17 of 300 |
| Russell 1000 | +10.0% | +14.1% | **+13.6%** | 17 of 300 |

**Yes, but modestly:** about 3.5 points a year over random picks, beaten by about 6% of the random runs. With tech in the
list it was 13 points, and no random run came close (`RATIO_B_HEDGE.md`, "Is the 27% real?").

## 4. After costs

At 0.10% on every dollar traded (the long book turns over about 325% a year, plus each hedge open and close):

| Strategy | Annual return | Worst drawdown |
|---|---|---|
| Unhedged | +16.5% | -35% |
| + S&P 500 / Dow / Russell 2000 / Russell 1000 / Russell 1000 Value (100%) | +11.5% / +10.2% / +9.2% / +12.0% / +9.8% | -30% to -31% |

The hedges trade 11-14 times a year at full size, so costs hit the hedged versions much harder than the long book.

## 5. Where it sits now

- **Long book:** LOW, SHW and UNP, held since the last monthly entry on 2026-10-05. They are also the three lowest
  non-tech Ratio B readings on the newest dates.
- **Hedge signals on 2026-11-06:**
  - below the 100-day average, so the hedge is **on**: S&P 500 (-3.2%), Dow (-2.1%), Russell 2000 (-5.5%), Russell 1000
    (-3.1%);
  - above it, so **off**: Russell 1000 Value (+1.8%).

This is the rule applied to point-in-time data, not advice.

## Limits

- **Survivorship remains, but smaller.** These seven are still companies chosen in 2026, but without the biggest
  compounders. Their equal weight beat SPY by 2.4 points a year, against 6.7 points with tech.
- **The hedge results rest on six market drawdowns.** The choice between indices turns on small differences (Sharpe
  0.88 to 0.93 for the half hedges).
- **Not modelled:** interest on the short proceeds, which would help the hedged versions a little; taxes on frequent
  trading.
