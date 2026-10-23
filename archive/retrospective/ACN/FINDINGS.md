# ACN retrospective findings (hindsight)

Patterns seen in `outcome.json` across the archive. They are **labels and hypotheses**: never feed them back into
the method or the fact sheet. Testing one means other tickers or periods, then a new method version and a full re-run.
Regenerate the numbers from `outcome.json` before quoting them; they cover the dates built so far. Medians of an
even count take the upper middle value (`statistics.median_high`).

Sample: 809 weekly dates, 2008-01-04 to 2023-06-30 (2-year outcomes). One stock, so every pattern is a hypothesis.
The 2023 dates are the pilot series re-encoded with the chain's rules (retro/README.md, "The 2023 pilot, harmonized").

| Group | Dates | Median 2-yr total return | Cleared 15%/yr hurdle | Beat SPY |
|---|---|---|---|---|
| class CHEAP | 278 | +41% | 66% | 60% |
| class FAIR | 39 | +28% | 46% | 38% |
| class RICH | 492 | +40% | 68% | 85% |
| legacy tier BUY | 310 | +45% | 75% | 69% |
| legacy tier ACCUMULATE | 85 | +36% | 54% | 55% |
| legacy tier WATCHLIST | 61 | +27% | 48% | 61% |
| legacy tier AVOID | 353 | +38% | 65% | 85% |
| CHEAP, gap >= 1.0 | 146 | +43% | 64% | 70% |
| CHEAP, gap < 0.5 | 53 | +38% | 66% | 43% |
| price below the EPP floor | 36 | +72% | 100% | 89% |
| price 15%+ above the floor | 712 | +39% | 65% | 71% |

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
- **2022: the class turned with the drawdown.** It was RICH on 7 dates (+3%), FAIR on 10 (+18%) and CHEAP on 35 (+21%, 10
  cleared the hurdle). None of the 2022 CHEAP dates beat SPY.
- **Scenario landings re-centred.** 2-year outcomes landed in BASE 55 times, BULL 38 and XBULL 11.

2023 alone (26 dates, January to June): 11 CHEAP (+20%, 4 cleared the hurdle), 11 FAIR (+27%, 4) and 4 RICH (+2%,
none). None of the 26 beat SPY. Outcomes landed in BASE 16 times and BULL 10; the price sat just under the BASE target
(median 0.94x). The m12-24 average price gave +20%.
- **The harmonization moved four dates from FAIR to CHEAP.** Two are in late 2022 (+25%, +24%) and two in April 2023
  (+8% each), so the 2023 CHEAP median fell from the pilot's +32% (9 dates) to +20%. The rules were applied before
  these outcomes were looked at. The point is that a FAIR/CHEAP boundary this close to the price moves with
  encoding details.

What these suggest (to test on other tickers, not to apply here):

1. **RICH did not work for ACN until the multiple peaked.** Its multiple re-rated from about 13x to 18x over 2009-2014
   and kept rising to 2021, and a valuation anchored on the stock's own 10-year P/E range kept calling RICH while it
   compounded. 2015-2020 is the clearest case: RICH on 303 of 313 dates, and 299 of them beat SPY over two years.
   RICH was finally right in the second half of 2021, but a signal that says RICH almost every week for seven years
   being right once is not evidence of timing skill. Candidate fix for a new method version: value against the
   market's multiple or growth-adjusted multiples as well as own history.
2. **RICH at turning points is a lag artefact:** in late 2009 the signals compare the worst quarter with the
   pre-crisis year. 'Valuation at a discount + bear dashboard' should probably read 'no call', not RICH.
3. **CHEAP is an absolute-return call more than a relative one:** in 2008, 2012-13 and 2022-23 CHEAP dates made money
   but lagged a strongly rising S&P 500 (2022-2023: 46 CHEAP dates, median +21%, none beat SPY).
4. **Small-gap CHEAP is close to fair value.** Against SPY, CHEAP with a gap under 0.5 won 43% of the time (53 dates).
   FAIR won 38% and CHEAP with a gap of 1.0 or more won 70%. In 2023, FAIR dates (+27%) did better than CHEAP (+20%).
5. **Below the EPP floor was the strongest single signal** (all dates there cleared the hurdle), but all 36 cases
   come from one crash in one stock (2008-2009). 2015-2020 adds one CHEAP date (the March 2020 low, which paid +121%)
   and 2022-2023 adds 46 CHEAP dates, none below the floor. Items 3 and 4 now have a second episode; item 5 still
   rests on 2008-2009 alone.
6. **The legacy tier ranked outcomes better than the class in 2008-2014** (WATCHLIST dates were clearly the weakest).
   In 2015-2020 it did not: WATCHLIST and AVOID dates all beat SPY. In 2021-2022 the order came back in absolute terms
   (BUY +34%, ACCUMULATE +16%, WATCHLIST +18%, AVOID 0%), and it held in 2023 (BUY +34%, ACCUMULATE +20%,
   WATCHLIST +6%, AVOID +4%), so it works when the multiple moves both ways.
7. **The scenario band itself sat too low from 2015.** Two-year outcomes landed in BULL or XBULL on 312 of 313 dates
   in 2015-2020. BULL uses the decade EPS CAGR and the 75th-percentile P/E. When the multiple trends up for years,
   the own-history percentiles trail it. Same root cause as item 1. When the multiple fell back (2021-2023 dates),
   outcomes landed mostly in BASE and BULL.
