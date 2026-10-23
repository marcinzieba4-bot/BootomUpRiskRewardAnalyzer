# ACN retrospective findings (hindsight)

Patterns seen in `outcome.json` across the archive. They are **labels and hypotheses**: never feed them back into
the method or the fact sheet. Testing one means other tickers or periods, then a new method version and a full re-run.
Regenerate the numbers from `outcome.json` before quoting them; they cover the dates built so far.

Sample: 366 weekly dates, 2008-01-04 to 2014-12-31 (2-year outcomes). One stock, so every pattern is a hypothesis.

| Group | Dates | Median 2-yr total return | Cleared 15%/yr hurdle | Beat SPY |
|---|---|---|---|---|
| class CHEAP | 231 | +45% | 73% | 71% |
| class FAIR | 9 | +36% | 56% | 44% |
| class RICH | 126 | +44% | 75% | 84% |
| legacy tier BUY | 285 | +46% | 76% | 75% |
| legacy tier ACCUMULATE | 55 | +44% | 71% | 78% |
| legacy tier WATCHLIST | 25 | +26% | 36% | 64% |
| CHEAP, gap >= 1.0 | 131 | +45% | 66% | 78% |
| CHEAP, gap < 0.5 | 40 | +43% | 72% | 55% |
| price below the EPP floor | 36 | +72% | 100% | 89% |
| price 15%+ above the floor | 269 | +43% | 72% | 68% |

What these suggest (to test on other tickers, not to apply here):

1. **RICH has not worked for ACN.** Its multiple re-rated from about 13x to 18x over 2009-2014, and a valuation
   anchored on the stock's own 10-year P/E range kept calling RICH while it compounded. Candidate fix for a new
   method version: value against the market's multiple or growth-adjusted multiples as well as own history.
2. **RICH at turning points is a lag artefact:** in late 2009 the signals compare the worst quarter with the
   pre-crisis year. 'Valuation at a discount + bear dashboard' should probably read 'no call', not RICH.
3. **CHEAP is an absolute-return call more than a relative one:** in 2008 and 2012-13 CHEAP dates made money but
   lagged a strongly rising S&P 500.
4. **Small-gap CHEAP is close to fair value**, as the 2023 series also showed.
5. **Below the EPP floor was the strongest single signal** (all dates there cleared the hurdle), but every case
   comes from one crash in one stock.
6. **The legacy tier ranks outcomes better than the class:** WATCHLIST dates were clearly the weakest.
