# ACN retrospective findings (hindsight)

Patterns seen in `outcome.json` across the archive. They are **labels and hypotheses**: never feed them back into
the method or the fact sheet. Testing one means other tickers or periods, then a new method version and a full re-run.
Regenerate the numbers from `outcome.json` before quoting them; they cover the dates built so far. Medians of an
even count take the upper middle value (`statistics.median_high`).

Sample: 679 weekly dates, 2008-01-04 to 2020-12-31 (2-year outcomes). One stock, so every pattern is a hypothesis.

| Group | Dates | Median 2-yr total return | Cleared 15%/yr hurdle | Beat SPY |
|---|---|---|---|---|
| class CHEAP | 232 | +45% | 73% | 72% |
| class FAIR | 18 | +58% | 78% | 72% |
| class RICH | 429 | +44% | 79% | 94% |
| legacy tier BUY | 285 | +46% | 76% | 75% |
| legacy tier ACCUMULATE | 59 | +44% | 73% | 80% |
| legacy tier WATCHLIST | 44 | +37% | 64% | 80% |
| legacy tier AVOID | 291 | +43% | 79% | 99% |
| CHEAP, gap >= 1.0 | 131 | +45% | 66% | 78% |
| CHEAP, gap < 0.5 | 41 | +43% | 73% | 56% |
| price below the EPP floor | 36 | +72% | 100% | 89% |
| price 15%+ above the floor | 582 | +43% | 77% | 84% |

2015-2016 alone (104 dates): 98 RICH and 6 FAIR, no CHEAP; 89 AVOID. Median 2-year return +40%, 82% cleared the
hurdle, all 104 beat SPY, and every 2-year outcome landed in the BULL (52) or XBULL (52) scenario. On the as-of
dates the price sat at the BASE target (median price/BASE 0.99). Two years later it was 1.35x BASE.

2017-2018 alone (105 dates): 103 RICH and 2 FAIR, no CHEAP; 102 AVOID. Median 2-year return +41%, 80% cleared the
hurdle, all 105 beat SPY; 2-year outcomes landed in XBULL 83 times, BULL 21, BASE once. The price started above the
BASE target (median 1.09x) and two years later stood at 1.53x it. On 14 dates in 2018 the price was above even the
BULL case (Ratio B infinite): those returned a median +34% and all 14 beat SPY. Endpoints from February-June 2018
fall in the March 2020 crash (median 2-year return +24% for those 20 dates); the m12-24 average (+21%) is the
steadier read there.

2019-2020 alone (104 dates): 102 RICH, one CHEAP (2020-03-20, at the COVID low: +121% over two years) and one FAIR
(2020-04-03: +128%); 99 AVOID. Median 2-year return +64%, 81% cleared the hurdle, 100 of 104 beat SPY, and 103 of
104 two-year outcomes landed in XBULL. The price started at 1.19x the BASE target and two years later stood at 1.86x it.
Ratio B was infinite on 59 dates (price above the BULL case): median +50%, 55 beat SPY. The only dates where RICH came
close to working are the 27 from July 2020, whose endpoints fall in the 2022 drawdown: median +23%, 7 cleared the
hurdle, 23 still beat SPY.

What these suggest (to test on other tickers, not to apply here):

1. **RICH has not worked for ACN.** Its multiple re-rated from about 13x to 18x over 2009-2014 and kept rising to
   2018, and a valuation anchored on the stock's own 10-year P/E range kept calling RICH while it compounded.
   2015-2020 is the clearest case: RICH on 303 of 313 dates, and 299 of them beat SPY over two years. Candidate fix for
   a new method version: value against the market's multiple or growth-adjusted multiples as well as own history.
2. **RICH at turning points is a lag artefact:** in late 2009 the signals compare the worst quarter with the
   pre-crisis year. 'Valuation at a discount + bear dashboard' should probably read 'no call', not RICH.
3. **CHEAP is an absolute-return call more than a relative one:** in 2008 and 2012-13 CHEAP dates made money but
   lagged a strongly rising S&P 500.
4. **Small-gap CHEAP is close to fair value**, as the 2023 series also showed.
5. **Below the EPP floor was the strongest single signal** (all dates there cleared the hurdle), but every case
   comes from one crash in one stock. 2015-2020 adds one CHEAP date (the March 2020 low, which paid +121%) and no
   below-floor dates, so items 3-5 still rest almost entirely on 2008-2014.
6. **The legacy tier ranked outcomes better than the class in 2008-2014** (WATCHLIST dates were clearly the weakest).
   From 2015 it did not: WATCHLIST and AVOID dates all beat SPY, so the tier order is no longer monotone.
7. **The scenario band itself sat too low from 2015.** Two-year outcomes landed in BULL or XBULL on 312 of 313 dates
   in 2015-2020. BULL uses the decade EPS CAGR and the 75th-percentile P/E. When the multiple trends up for years,
   the own-history percentiles trail it. Same root cause as item 1.
