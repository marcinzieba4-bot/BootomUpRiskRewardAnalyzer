# Is a small, shrinking EPP gap a structural loser? Short it against the S&P 500 (hindsight)

**Hypothesis tested:** a small EPP gap that keeps shrinking marks a structural loser, so short the stock and buy SPY.
This is the reverse of `EPP_DOWNSIDE.md`.

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number is printed by `python3 staging/retrospective/epp_short.py`, from point-in-time EPP gaps on 10,728 weekly
dates and Yahoo total-return data to 2026-11-06. The signals and the basket rules were fixed in its docstring before the
first run.

**The trade:** short the stock and buy the same amount of SPY, from the close after the as-of date. Its result is SPY's
total return minus the stock's. A positive number means the trade won.

**Survivorship cuts against this test.** The eleven are 2026's survivors, so the companies that kept falling, the best
shorts, are missing. Shorting any of these stocks lost money on average: over all dates the trade won only 42% of the
time at 12 months (median -4.0%).

## 1. The pair trade

**All eleven:**

| Signal | Dates | Episodes | 3m: median / won | 12m: median / won | 24m: median / won |
|---|---|---|---|---|---|
| **MAIN: gap <= 40% and lower than 26 weeks ago** | 2,365 | 183 | -1.2% / 46% | **-1.2% / 48%** | **-3.5% / 48%** |
| gap <= 40%, down 20+ points in 26 weeks | 1,024 | 134 | -1.4% / 46% | -3.1% / 44% | -14.1% / 41% |
| gap <= 40%, lower than 52 weeks ago | 2,333 | 160 | -0.5% / 48% | -1.2% / 48% | +2.6% / 52% |
| MAIN and the price down over 12 months | 1,137 | 122 | +0.4% / 51% | +2.8% / 55% | +4.7% / 56% |
| gap <= 0% (below the floor) and lower than 26 weeks ago | 727 | 67 | -1.2% / 46% | +4.8% / 58% | +8.9% / 64% |
| every date (baseline) | 10,158 | 11 | -0.9% / 46% | -4.0% / 42% | -9.8% / 40% |

**Without tech:**

| Signal | Dates | 12m: median / won | 24m: median / won |
|---|---|---|---|
| MAIN | 1,768 | +1.9% / 53% | +5.2% / 54% |
| MAIN and the price down over 12 months | 892 | +5.4% / 61% | +12.9% / 63% |
| **gap <= 0% and lower than 26 weeks ago** | 553 | **+7.5% / 64%** | **+14.1% / 70%** |
| every date (baseline) | 6,517 | -0.3% / 49% | -1.1% / 49% |

- **The main signal fails.** Shorting stocks with a small, shrinking gap lost to SPY slightly, at every horizon.
- **The signal does find relatively weaker stocks.** Its trade did better than the baseline of shorting any date (-1.2%
  against -4.0% at 12 months). It just does not find stocks weak enough to lag the market.
- **Below the floor and still shrinking is where the idea starts to show,** especially without tech: the trade won 64% of
  the time at 12 months and 70% at 24. Requiring the price to be down over 12 months helps too.
- **Over 1-3 months every variant lost** (medians -0.4% to -1.4%): fallen stocks tended to bounce first.

## 2. Why: the signal cannot tell a loser from a compounder on sale

Per ticker, main signal, short the stock and long SPY:

| Ticker | Dates | 12m: median / won | 24m: median / won | Read |
|---|---|---|---|---|
| NKE | 254 | **+14.2% / 65%** | +65.0% / 57% | a real laggard: the short worked |
| PEP | 312 | **+9.0% / 71%** | +15.7% / 74% | a real laggard |
| XOM | 393 | **+7.1% / 62%** | +23.1% / 83% | a real laggard |
| WMT | 222 | -0.8% / 47% | -11.0% / 46% | neither |
| ACN | 272 | -2.2% / 44% | -7.9% / 38% | |
| MSFT | 128 | -2.8% / 42% | +4.2% / 64% | 2008-2013, before the cloud re-rating |
| LOW | 356 | -3.2% / 43% | -16.1% / 29% | a compounder on sale: the short lost |
| UNP | 210 | -4.2% / 44% | -21.1% / 36% | a compounder on sale |
| SHW | 141 | -10.0% / 16% | -22.7% / 19% | a compounder on sale |
| AAPL | 175 | **-25.5% / 20%** | -59.4% / 15% | a compounder on sale |
| AVGO | 98 | **-61.2% / 7%** | **-182.2% / 0%** | a compounder on sale (2022) |

A shrinking gap near the floor happens both to businesses in slow decline (PEP, XOM, NKE) and to compounders in a
temporary slump (AAPL 2013 and 2016, AVGO 2022, SHW 2018, LOW 2022). The EPP gap alone cannot tell them apart. A short
loses at most about 100% on a loser, but can lose 180% on a compounder that keeps running.

## 3. As a monthly basket

Each month, short every signalled stock in equal weight against 100% SPY.

| Universe | Signal | Hold | Annual return | Sharpe | Worst drawdown |
|---|---|---|---|---|---|
| all eleven | **MAIN** | 1m / 6m / 12m | **-7.5% / -4.9% / -3.8%** | -0.36 / -0.26 / -0.21 | -81% / -75% / -65% |
| all eleven | below the floor and shrinking | 1m / 6m / 12m | -6.3% / -1.8% / -1.1% | -0.32 / -0.06 / -0.02 | -78% / -49% / -40% |
| all eleven | MAIN and the price down over 12 months | 1m / 6m / 12m | -1.8% / -0.9% / -0.6% | -0.03 / +0.01 / +0.03 | -56% / -56% / -41% |
| without tech | MAIN | 1m / 6m / 12m | -5.9% / -3.3% / -0.4% | -0.25 / -0.15 / +0.04 | -81% / -70% / -50% |
| without tech | **below the floor and shrinking** | 12m | **+1.0%** | +0.15 | -27% |
| without tech | **MAIN and the price down over 12 months** | 12m | **+2.0%** | +0.22 | -33% |

- **No version of the basket was worth running.** The best made 1-2% a year, with drawdowns of -27% to -33%.
- **The main basket lost money in 15 of 19 calendar years.** It made money in 2015, 2019 and 2024 (2024 +23%).
- **2008 is the telling year.** With SPY down 37%, the main basket still lost 23%: the "losers" fell even more than the
  market.

## Summary

1. **"Small and shrinking EPP gap = structural loser" does not hold as a rule.** Short it against SPY and the trade lost
   slightly at every horizon, and as a monthly basket 4-8% a year.
2. **It works only for real laggards** (PEP, XOM, NKE, where the short won 62-71% of the time over 12 months). It loses
   heavily on compounders in a slump (AVGO -61%, AAPL -26% over 12 months).
3. **The narrowest version is the only promising one, and it is still weak:** below the floor, still shrinking, the price
   down over 12 months, without tech. It made at most 1-2% a year as a basket.
4. **To make it work, it needs a filter that recognises a business in decline,** which the EPP gap alone does not
   provide. Candidates for a new method version: falling EPS or revenue, a live disruption theme, a falling own P/E. Test
   them only on tickers not yet built.

## The newest signals (2026-11-06)

**The main signal fires on LOW** (gap +8%, down 14 points in 26 weeks, price -18% over 12 months) **and PEP** (gap +9%,
down 10 points, price -6%).
- Both also pass "the price down over 12 months".
- LOW was a compounder that this short lost on (-3.2% median at 12 months). PEP was one of the laggards where it worked
  (+9.0%).

This is point-in-time data read through hindsight labels, not advice.
