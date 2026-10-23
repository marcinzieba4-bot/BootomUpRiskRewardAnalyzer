# UNP retrospective findings (hindsight)

Patterns seen in `outcome.json` for the 13 weekly dates from 2008-01-04 to 2008-03-28. They are **labels and
hypotheses**: never feed them back into the method or the fact sheet. Each was computed after the point-in-time
build was committed (68cbbb6). Medians of an even count take the upper middle value (`statistics.median_high`).
Prices are on the as-of share basis (before the 2008 2:1 split).

| Group | Dates | Median 2-yr total return | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price |
|---|---|---|---|---|---|
| class RICH (tier AVOID) | 7 | +9.9% | 0 | 7 | -11.2% |
| class FAIR (tier WATCHLIST) | 6 | +22.4% | 0 | 6 | -4.6% |

- **Every call "missed" by its own test**, because UNP beat a falling market by 17-37pp over two years. RICH expects
  the stock to lag SPY, and FAIR expects it to stay within 15pp of SPY. None of the 13 cleared the hurdle.
- **The ranking held.** FAIR dates did better than RICH dates: +22% against +10% over two years, -5% against -11% on
  the m12-24 average price. Over a few months of one stock that mostly says "lower P/E did better", which is a
  "buy lower" test, not a selection test.
- **The bear came, but it was the multiple.** From the August 2008 high ($167.80) the stock fell 60% to $67.24
  (2009-03-09), below every date's EPP floor ($89-104). It stayed above the BEAR scenario ($43-51). All 13 two-year
  outcomes landed in BASE.
- **The no-guide fallback mattered.** The five RICH dates from 2008-01-25 to 2008-02-22 use FY07's $6.91, because
  no numeric 2008 guide had been filed yet. From 2008-02-29 the 10-K's $7.75-8.25 guide turns the same price into
  FAIR. Whether the trailing-EPS fallback makes these dates read too rich is a question for other tickers with
  gaps in their guidance, not something to tune here.
- **The BEAR rule on a cyclical.** UNP's worst EPS year (2004, -29%) repeated for two years makes BEAR the biggest
  driver of Ratio B (above 2 on most dates). Test the rule on other cyclicals before any method change.
