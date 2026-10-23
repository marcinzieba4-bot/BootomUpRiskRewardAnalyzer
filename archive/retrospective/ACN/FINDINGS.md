# ACN retrospective findings (hindsight)

Patterns seen in `outcome.json` across the archive. They are **labels and hypotheses**: never feed them back into
the method or the fact sheet. Testing one means other tickers or periods, then a new method version and a full re-run.
Regenerate the numbers from `outcome.json` before quoting them; they cover the dates built so far. Medians of an
even count take the upper middle value (`statistics.median_high`).

Sample: 575 weekly dates, 2008-01-04 to 2018-12-31 (2-year outcomes). One stock, so every pattern is a hypothesis.

| Group | Dates | Median 2-yr total return | Cleared 15%/yr hurdle | Beat SPY |
|---|---|---|---|---|
| class CHEAP | 231 | +45% | 73% | 71% |
| class FAIR | 17 | +58% | 76% | 71% |
| class RICH | 327 | +41% | 78% | 94% |
| legacy tier BUY | 285 | +46% | 76% | 75% |
| legacy tier ACCUMULATE | 57 | +44% | 72% | 79% |
| legacy tier WATCHLIST | 41 | +36% | 61% | 78% |
| legacy tier AVOID | 192 | +40% | 79% | 100% |
| CHEAP, gap >= 1.0 | 131 | +45% | 66% | 78% |
| CHEAP, gap < 0.5 | 40 | +43% | 72% | 55% |
| price below the EPP floor | 36 | +72% | 100% | 89% |
| price 15%+ above the floor | 478 | +41% | 76% | 82% |

2015-2016 alone (104 dates): 98 RICH and 6 FAIR, no CHEAP; 89 AVOID. Median 2-year return +40%, 82% cleared the
hurdle, all 104 beat SPY, and every 2-year outcome landed in the BULL (52) or XBULL (52) scenario. On the as-of
dates the price sat at the BASE target (median price/BASE 0.99). Two years later it was 1.35x BASE.

2017-2018 alone (105 dates): 103 RICH and 2 FAIR, no CHEAP; 102 AVOID. Median 2-year return +41%, 80% cleared the
hurdle, all 105 beat SPY; 2-year outcomes landed in XBULL 83 times, BULL 21, BASE once. The price started above the
BASE target (median 1.09x) and two years later stood at 1.53x it. On 14 dates in 2018 the price was above even the
BULL case (Ratio B infinite): those returned a median +34% and all 14 beat SPY. Endpoints from February-June 2018
fall in the March 2020 crash (median 2-year return +24% for those 20 dates); the m12-24 average (+21%) is the
steadier read there.

What these suggest (to test on other tickers, not to apply here):

1. **RICH has not worked for ACN.** Its multiple re-rated from about 13x to 18x over 2009-2014 and kept rising to
   2018, and a valuation anchored on the stock's own 10-year P/E range kept calling RICH while it compounded.
   2015-2018 is the clearest case: RICH on 201 of 209 dates, and every one beat SPY over two years. Candidate fix for
   a new method version: value against the market's multiple or growth-adjusted multiples as well as own history.
2. **RICH at turning points is a lag artefact:** in late 2009 the signals compare the worst quarter with the
   pre-crisis year. 'Valuation at a discount + bear dashboard' should probably read 'no call', not RICH.
3. **CHEAP is an absolute-return call more than a relative one:** in 2008 and 2012-13 CHEAP dates made money but
   lagged a strongly rising S&P 500.
4. **Small-gap CHEAP is close to fair value**, as the 2023 series also showed.
5. **Below the EPP floor was the strongest single signal** (all dates there cleared the hurdle), but every case
   comes from one crash in one stock. 2015-2018 adds no CHEAP or below-floor dates, so items 3-5 rest on 2008-2014.
6. **The legacy tier ranked outcomes better than the class in 2008-2014** (WATCHLIST dates were clearly the weakest).
   From 2015 it did not: WATCHLIST and AVOID dates all beat SPY, so the tier order is no longer monotone.
7. **The scenario band itself sat too low from 2015.** Two-year outcomes landed in BULL or XBULL on 208 of 209 dates
   in 2015-2018. BULL uses the decade EPS CAGR and the 75th-percentile P/E. When the multiple trends up for years,
   the own-history percentiles trail it. Same root cause as item 1.
