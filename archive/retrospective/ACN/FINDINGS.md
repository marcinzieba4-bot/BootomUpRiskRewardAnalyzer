# ACN retrospective findings (hindsight)

Patterns seen in `outcome.json` across the archive. They are **labels and hypotheses**: never feed them back into
the method or the fact sheet. Testing one means other tickers or periods, then a new method version and a full re-run.
Regenerate the numbers from `outcome.json` before quoting them; they cover the dates built so far. Medians of an
even count take the upper middle value (`statistics.median_high`).

Sample: 783 weekly dates, 2008-01-04 to 2022-12-30 (2-year outcomes). One stock, so every pattern is a hypothesis.
The 2023 pilot series is left out: it was built from its own FY22 vintage with different conventions
(retro/README.md, "Seam with the 2023 pilot").

| Group | Dates | Median 2-yr total return | Cleared 15%/yr hurdle | Beat SPY |
|---|---|---|---|---|
| class CHEAP | 265 | +43% | 68% | 63% |
| class FAIR | 30 | +28% | 47% | 50% |
| class RICH | 488 | +41% | 69% | 86% |
| legacy tier BUY | 303 | +45% | 75% | 71% |
| legacy tier ACCUMULATE | 73 | +37% | 59% | 64% |
| legacy tier WATCHLIST | 56 | +33% | 50% | 66% |
| legacy tier AVOID | 351 | +39% | 66% | 86% |
| CHEAP, gap >= 1.0 | 146 | +43% | 64% | 70% |
| CHEAP, gap < 0.5 | 44 | +41% | 75% | 52% |
| price below the EPP floor | 36 | +72% | 100% | 89% |
| price 15%+ above the floor | 686 | +40% | 67% | 74% |

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

2021-2022 alone (104 dates): the first stretch where the calls moved with the price.
- **2021: all 52 dates RICH.** Median 2-year return about 0%, none cleared the hurdle and 14 beat SPY. The 27 dates
  from July to December 2021 (the multiple's peak) lost money on 22 and never beat SPY.
- **2022: the class turned with the drawdown.** It was RICH on 7 dates (+3%), FAIR on 12 (+18%) and CHEAP on 33 (+21%, 10
  cleared the hurdle). None of the 2022 CHEAP dates beat SPY.
- **Scenario landings re-centred.** 2-year outcomes landed in BASE 54 times, BULL 39 and XBULL 11.

What these suggest (to test on other tickers, not to apply here):

1. **RICH did not work for ACN until the multiple peaked.** Its multiple re-rated from about 13x to 18x over 2009-2014
   and kept rising to 2021, and a valuation anchored on the stock's own 10-year P/E range kept calling RICH while it
   compounded. 2015-2020 is the clearest case: RICH on 303 of 313 dates, and 299 of them beat SPY over two years.
   RICH was finally right in the second half of 2021, but a signal that says RICH almost every week for seven years
   being right once is not evidence of timing skill. Candidate fix for a new method version: value against the
   market's multiple or growth-adjusted multiples as well as own history.
2. **RICH at turning points is a lag artefact:** in late 2009 the signals compare the worst quarter with the
   pre-crisis year. 'Valuation at a discount + bear dashboard' should probably read 'no call', not RICH.
3. **CHEAP is an absolute-return call more than a relative one:** in 2008, 2012-13 and 2022 CHEAP dates made money but
   lagged a strongly rising S&P 500 (2022: 33 CHEAP dates, median +21%, none beat SPY).
4. **Small-gap CHEAP is close to fair value**, as the 2023 series also showed.
5. **Below the EPP floor was the strongest single signal** (all dates there cleared the hurdle), but every case
   comes from one crash in one stock. 2015-2020 adds one CHEAP date (the March 2020 low, which paid +121%) and no
   below-floor dates, so items 3-5 still rest almost entirely on 2008-2014.
6. **The legacy tier ranked outcomes better than the class in 2008-2014** (WATCHLIST dates were clearly the weakest).
   In 2015-2020 it did not: WATCHLIST and AVOID dates all beat SPY. In 2021-2022 the order came back in absolute terms
   (BUY +34%, ACCUMULATE +16%, WATCHLIST +18%, AVOID 0%), so it works when the multiple moves both ways.
7. **The scenario band itself sat too low from 2015.** Two-year outcomes landed in BULL or XBULL on 312 of 313 dates
   in 2015-2020. BULL uses the decade EPS CAGR and the 75th-percentile P/E. When the multiple trends up for years,
   the own-history percentiles trail it. Same root cause as item 1. When the multiple fell back (2021-2022 dates),
   outcomes landed mostly in BASE and BULL.
