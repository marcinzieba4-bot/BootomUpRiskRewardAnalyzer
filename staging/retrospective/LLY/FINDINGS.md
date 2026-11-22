# LLY retrospective findings (hindsight)

Patterns seen in `outcome.json` for the LLY weekly dates: 523, 105 from 2008-01-04 to 2009-12-31, 209 from 2010-01-08 to 2013-12-31
and 209 from 2014-01-03 to 2017-12-29, all Eli Lilly and Company (NYSE: LLY).
They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its
point-in-time build was committed and pushed (8d1f450, the empty-slot correction the firewall found 96e4c9f, firewall result 73b08d1);
the outcomes were computed on 2026-11-21. The 2010-2013 batch was scored only after its build, checks, README section and firewall
result were committed and pushed (5a27368, f8db0dc, 5446ffc), on 2026-11-21. The 2014-2017 batch was built in a new session and scored
only after its build, checks, README section and firewall result were committed and pushed (c64c37a, 3e0e6d0, b3185fb), on 2026-11-22;
this file was first opened in that session after those pushes. Every date has its 6-month, 1-, 2- and 3-year horizons
(the last ends 2012-12-31 for 2008-2009, 2016-12-30 for 2010-2013 and 2020-12-29 for 2014-2017). Total returns
include the quarterly dividends ($0.425 to the ex-date of 2008-02-13, $0.47 from it, $0.49 from 2009-02-11, $0.50 from 2015-02-11, $0.51
from 2016-02-10, $0.52 from 2017-02-13, $0.5625 from 2018-02-14, $0.645 from 2019-02-14 and $0.74 from 2020-02-13). No
split falls in any horizon, so every price is as traded. Medians of an even count take the upper middle value
(`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over three. "Call held" is `call_check_2y`: CHEAP should
clear the hurdle or beat the benchmark (SPY), RICH should miss the hurdle and lag it. Every date of 2008-2013 was CHEAP and BUY, so their
tables test that one call against the calendar; 2014-2017 has 4 CHEAP and BUY dates and 205 RICH and AVOID.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 53 | -18.8% | -30.8% to +30.6% | 0 | 0 | -27.4% | 0 |
| FY07E $2.785 (2008-01-04 to 2008-01-25) | 4 | -23.4% | -30.8% to -22.0% | 0 | 0 | -33.8% | 0 |
| FY08E $3.875 (2008-01-30 to 2008-03-07) | 6 | -23.6% | -25.6% to -21.6% | 0 | 0 | -32.2% | 0 |
| FY08E $3.815 (2008-03-14 to 2008-04-18) | 6 | -21.6% | -23.5% to -16.8% | 0 | 0 | -31.5% | 0 |
| FY08E $3.975 (2008-04-22 to 2008-07-18) | 13 | -20.2% | -25.1% to -17.1% | 0 | 0 | -27.9% | 0 |
| FY08E $3.865 (2008-07-25 to 2008-10-17) | 13 | -15.6% | -20.7% to +30.6% | 0 | 0 | -25.1% | 0 |
| FY08E $2.465 (2008-10-24 to 2008-12-05) | 7 | +15.8% | +8.9% to +26.3% | 0 | 0 | +4.5% | 0 |
| FY08E $2.71 (2008-12-12 to 2008-12-31) | 4 | +3.1% | -3.3% to +6.8% | 0 | 0 | -7.4% | 0 |
| latest print Q3 2007 (2008-01-04 to 2008-01-25) | 4 | -23.4% | -30.8% to -22.0% | 0 | 0 | -33.8% | 0 |
| latest print Q4 2007 (2008-01-30 to 2008-04-18) | 12 | -22.4% | -25.6% to -16.8% | 0 | 0 | -32.2% | 0 |
| latest print Q1 2008 (2008-04-22 to 2008-07-18) | 13 | -20.2% | -25.1% to -17.1% | 0 | 0 | -27.9% | 0 |
| latest print Q2 2008 (2008-07-25 to 2008-10-17) | 13 | -15.6% | -20.7% to +30.6% | 0 | 0 | -25.1% | 0 |
| latest print Q3 2008 (2008-10-24 to 2008-12-31) | 11 | +11.2% | -3.3% to +26.3% | 0 | 0 | +3.3% | 0 |

- **CHEAP failed on all 53 dates of 2008.** From $30.43-56.81 the 2008 entries returned -30.8% to +30.6% over two years, dividends
  included, while SPY returned -18.7% to +56.9%: every one lagged it, by 1.7-47.5pp, and none cleared the hurdle. Over three years (to
  the end of 2011) they returned -28.3% to +41.2% (median -9.2%) and none beat SPY. Every 2008 date sat through a 32-52% drawdown (the
  low close $27.47 on 2009-03-05); two years on the price was $32.37-37.76.
- **The earnings were real; the multiple was not.** FY2009 came in at the guides the models used: reported $3.94 (the Q4 2009 release,
  2010-01-28, outside the series) against the $3.95-4.19 of 2009's guides. Two years on, the
  2008-2009 entries' prices ($32.37-41.64) were 8.2-10.6x that FY2009 figure, while every rule that reads the stock's own decade (the
  median P/E of 26.7-29.7x, the EPP floor of 20-22x from the 1998-2007 calendar-year lows of 17.6-31.1x) put the floor alone at
  1.08-3.10 times the entry price. The EPP floor
  ($54-88) was never reached within two years on any of the 105 dates, and the two-year price landed nearest the BEAR scenario on every
  date. Hypothesis, not a rule: a decade of a company's own multiples can sit far above what the market will pay once the company's own
  10-Ks name a wave of patent expirations a few years out ("several major products will lose intellectual property protection
  beginning in 2011", FY2007 10-K); method r2 reads those words only into the durability "why". Test it on other tickers and periods
  with a dated patent cliff, never fit it to LLY.
- **The best 2008 entries were the cheapest.** The Q3 2008 print's dates (2008-10-24 to 2008-12-31, $30.43-40.27) returned -3.3% to +26.3%,
  the January 2008 dates ($50.74-56.81) -30.8% to -22.0%.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +21.3% | +0.9% to +37.7% | 1 | 13 | +4.7% | 14 |
| FY08E $2.71 (2009-01-09 to 2009-01-23) | 3 | +1.8% | +0.9% to +3.4% | 0 | 0 | -7.9% | 0 |
| FY09E $4.125 (2009-01-30 to 2009-07-17) | 25 | +20.5% | +3.3% to +37.7% | 1 | 0 | +4.5% | 1 |
| FY09E $4.19 (2009-07-23 to 2009-10-16) | 13 | +22.3% | +15.1% to +27.0% | 0 | 8 | +7.4% | 8 |
| FY09E $3.95 (2009-10-22 to 2009-12-31) | 11 | +23.1% | +7.0% to +27.4% | 0 | 5 | +2.6% | 5 |
| latest print Q3 2008 (2009-01-09 to 2009-01-23) | 3 | +1.8% | +0.9% to +3.4% | 0 | 0 | -7.9% | 0 |
| latest print Q4 2008 (2009-01-30 to 2009-04-17) | 12 | +18.0% | +3.3% to +37.7% | 1 | 0 | +6.1% | 1 |
| latest print Q1 2009 (2009-04-21 to 2009-07-17) | 13 | +22.2% | +15.3% to +26.0% | 0 | 0 | +3.6% | 0 |
| latest print Q2 2009 (2009-07-23 to 2009-10-16) | 13 | +22.3% | +15.1% to +27.0% | 0 | 8 | +7.4% | 8 |
| latest print Q3 2009 (2009-10-22 to 2009-12-31) | 11 | +23.1% | +7.0% to +27.4% | 0 | 5 | +2.6% | 5 |

- **CHEAP held on 14 of 52 dates of 2009, mostly late in the year.** The 2009 entries ($27.98-38.48) returned +0.9% to +37.7% over two years
  against SPY's +10.4% to +98.7%: the dates from the March 2009 low to the summer lagged SPY's rebound by up to 63.6pp, and only
  2009-03-06, the low of the series ($27.98, 6.8x), cleared the hurdle (+37.7%). From 2009-08-21 the entries beat SPY on 13 dates (by
  up to 11.6pp). Over three years the 2009 entries returned +18.7% to +72.9% (median +45.0%); 20 beat SPY and 16 cleared the three-year
  hurdle.
- **Ratio B below zero was not a margin of safety.** The BEAR price exceeded the price on 44 dates (2008-10-10, 2008-10-17 and 2009-01-30
  to 2009-11-13: the price under even the BEAR case). Those dates returned +3.3% to +37.7% over two years, yet 35 of the 44 lagged SPY
  and the call held on only 10 (2008-10-10 and 2008-10-17, at +30.6% and +29.4%, missed SPY by 6.1 and 1.7pp); the BEAR case, at the
  window's 10th-percentile P/E (9.5-21.1x), was itself a multiple the market did not grant.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +34.9% | +18.5% to +58.8% | 31 | 38 | +12.1% | 39 |
| FY09E $3.95 (2010-01-08 to 2010-01-22) | 3 | +23.1% | +22.4% to +25.1% | 0 | 2 | +4.5% | 2 |
| FY10E $4.75 (2010-01-29 to 2010-04-16) | 12 | +22.7% | +18.5% to +26.1% | 0 | 1 | +7.2% | 1 |
| FY10E $4.425 (2010-04-20 to 2010-07-16) | 13 | +33.7% | +20.0% to +39.3% | 9 | 13 | +13.5% | 13 |
| FY10E $4.515 (2010-07-23 to 2010-10-15) | 13 | +40.9% | +29.2% to +49.5% | 11 | 11 | +11.9% | 12 |
| FY10E $4.6 (2010-10-22 to 2010-12-31) | 11 | +51.8% | +47.5% to +58.8% | 11 | 11 | +23.2% | 11 |
| latest print Q3 2009 (2010-01-08 to 2010-01-22) | 3 | +23.1% | +22.4% to +25.1% | 0 | 2 | +4.5% | 2 |
| latest print Q4 2009 (2010-01-29 to 2010-04-16) | 12 | +22.7% | +18.5% to +26.1% | 0 | 1 | +7.2% | 1 |
| latest print Q1 2010 (2010-04-20 to 2010-07-16) | 13 | +33.7% | +20.0% to +39.3% | 9 | 13 | +13.5% | 13 |
| latest print Q2 2010 (2010-07-23 to 2010-10-15) | 13 | +40.9% | +29.2% to +49.5% | 11 | 11 | +11.9% | 12 |
| latest print Q3 2010 (2010-10-22 to 2010-12-31) | 11 | +51.8% | +47.5% to +58.8% | 11 | 11 | +23.2% | 11 |

- **CHEAP held on 39 of 52 dates of 2010.** From $32.37-37.76 (7.1-9.1x the reported guide) the 2010 entries returned +18.5% to
  +58.8% over two years, dividends included, against SPY's +15.7% to +38.6%; 31 cleared the hurdle and 38 beat SPY. The misses are
  2010-01-22 and the 11 dates from the Q4 2009 print to 2010-04-09 (FY10E $4.75: +18.5% to +26.1%, under the +32.2% hurdle and 1.0-4.9pp
  behind SPY), and 2010-08-13 (+30.9%). From the Q1 2010 print the call held on 36 of 37 dates. Over three years the entries returned
  +44.8% to +84.3%; 48 beat SPY and 50 cleared the hurdle.
- **The floor was not the target.** The EPP floor ($79.00-99.75, 20-21x, the median of the window's calendar-year lows) was never reached
  within two years, and the two-year price ($39.05-52.53) landed nearest the BEAR case on all 52 dates. The return came from a low
  entry multiple, a dividend of about 5-6% a year and a partial re-rating: two years on the stock traded at 10.1-13.9x the reported
  guide of that date (from 7.1-9.1x), not at the 20x of the old decade.

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +53.4% | +30.8% to +73.0% | 50 | 39 | +34.3% | 50 |
| FY10E $4.6 (2011-01-07 to 2011-01-21) | 3 | +62.5% | +58.8% to +66.0% | 3 | 3 | +26.0% | 3 |
| FY11E $3.995 (2011-01-28 to 2011-04-15) | 12 | +69.2% | +61.8% to +73.0% | 12 | 12 | +32.6% | 12 |
| FY11E $3.935 (2011-04-19 to 2011-07-15) | 13 | +52.7% | +43.6% to +71.8% | 13 | 13 | +34.0% | 13 |
| FY11E $3.9 (2011-07-22 to 2011-10-14) | 13 | +52.2% | +36.0% to +64.9% | 13 | 10 | +42.0% | 13 |
| FY11E $3.915 (2011-10-21 to 2011-12-30) | 11 | +41.9% | +30.8% to +55.3% | 9 | 1 | +37.6% | 9 |
| latest print Q3 2010 (2011-01-07 to 2011-01-21) | 3 | +62.5% | +58.8% to +66.0% | 3 | 3 | +26.0% | 3 |
| latest print Q4 2010 (2011-01-28 to 2011-04-15) | 12 | +69.2% | +61.8% to +73.0% | 12 | 12 | +32.6% | 12 |
| latest print Q1 2011 (2011-04-19 to 2011-07-15) | 13 | +52.7% | +43.6% to +71.8% | 13 | 13 | +34.0% | 13 |
| latest print Q2 2011 (2011-07-22 to 2011-10-14) | 13 | +52.2% | +36.0% to +64.9% | 13 | 10 | +42.0% | 13 |
| latest print Q3 2011 (2011-10-21 to 2011-12-30) | 11 | +41.9% | +30.8% to +55.3% | 9 | 1 | +37.6% | 9 |

- **CHEAP held on 50 of 52 dates of 2011.** From $34.09-41.64 (7.6-10.6x) the entries returned +30.8% to +73.0% over two years (median
  +53.4%) against SPY's +16.9% to +60.6%; 39 beat SPY. The two misses, 2011-12-16 and 2011-12-23 (+31.0% and +30.8%), fell just under
  the hurdle and 18.7-20.9pp behind SPY. Zyprexa lost U.S. exclusivity in October 2011, inside these horizons. Over three years
  +63.5% to +104.4%, and every date beat SPY and cleared the hurdle.
- As in 2010, the floor ($74.10-87.40) was never reached within two years and the two-year price landed nearest BEAR on all 52 dates;
  two years on the stock traded at 11.0-14.4x the then-current reported guide.

## 2012 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +52.6% | +25.8% to +61.2% | 51 | 42 | +28.7% | 51 |
| FY11E $3.865 (2012-01-06 to 2012-01-27) | 4 | +48.1% | +39.0% to +48.4% | 4 | 2 | +32.4% | 4 |
| FY12E $3.15 (2012-02-01 to 2012-04-20) | 12 | +56.2% | +45.6% to +61.2% | 12 | 12 | +33.8% | 12 |
| FY12E $3.215 (2012-04-26 to 2012-07-20) | 13 | +54.0% | +49.6% to +58.8% | 13 | 13 | +29.2% | 13 |
| FY12E $3.34 (2012-07-26 to 2012-08-03) | 2 | +55.2% | +46.3% to +55.2% | 2 | 2 | +26.8% | 2 |
| FY12E $3.77 (2012-08-10 to 2012-10-19) | 11 | +48.1% | +25.8% to +52.7% | 10 | 9 | +20.8% | 10 |
| FY12E $3.73 (2012-10-25 to 2012-12-28) | 10 | +52.7% | +37.0% to +55.2% | 10 | 4 | +24.2% | 10 |
| latest print Q3 2011 (2012-01-06 to 2012-01-27) | 4 | +48.1% | +39.0% to +48.4% | 4 | 2 | +32.4% | 4 |
| latest print Q4 2011 (2012-02-01 to 2012-04-20) | 12 | +56.2% | +45.6% to +61.2% | 12 | 12 | +33.8% | 12 |
| latest print Q1 2012 (2012-04-26 to 2012-07-20) | 13 | +54.0% | +49.6% to +58.8% | 13 | 13 | +29.2% | 13 |
| latest print Q2 2012 (2012-07-26 to 2012-10-19) | 13 | +48.1% | +25.8% to +55.2% | 12 | 11 | +21.2% | 12 |
| latest print Q3 2012 (2012-10-25 to 2012-12-28) | 10 | +52.7% | +37.0% to +55.2% | 10 | 4 | +24.2% | 10 |

- **CHEAP held on 51 of 52 dates of 2012.** From $39.05-52.86 (10.1-14.0x) the entries returned +25.8% to +61.2% (median +52.6%)
  against SPY's +35.8% to +55.5%; 51 cleared the hurdle and 42 beat SPY. The miss is 2012-10-19 ($52.86, the high of the year: +25.8%,
  10.6pp behind SPY). Over three years +63.0% to +119.0%, every date ahead of SPY.
- **A negative BASE did not mark a bad entry.** From the Q4 2011 print the FY2012 dollar revenue guide put BASE at -8.4%/yr; those
  entries did as well as 2011's. The floor ($56.70-71.63) was reached within two years on 31 of the 52 dates, and the two-year price
  landed nearest BASE on 49 and BEAR on 3.

## 2013 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 53 | +62.7% | +31.1% to +89.1% | 52 | 40 | +35.3% | 52 |
| FY12E $3.73 (2013-01-04 to 2013-01-25) | 4 | +42.9% | +38.7% to +43.5% | 4 | 1 | +17.9% | 4 |
| FY13E $4.175 (2013-01-30 to 2013-07-19) | 25 | +40.1% | +31.1% to +82.8% | 24 | 15 | +19.0% | 24 |
| FY13E $4.33 (2013-07-25 to 2013-10-18) | 13 | +68.6% | +59.1% to +89.1% | 13 | 13 | +38.8% | 13 |
| FY13E $4.355 (2013-10-24 to 2013-12-31) | 11 | +74.5% | +62.7% to +78.9% | 11 | 11 | +53.3% | 11 |
| latest print Q3 2012 (2013-01-04 to 2013-01-25) | 4 | +42.9% | +38.7% to +43.5% | 4 | 1 | +17.9% | 4 |
| latest print Q4 2012 (2013-01-30 to 2013-04-19) | 12 | +36.5% | +31.1% to +44.1% | 11 | 3 | +16.9% | 11 |
| latest print Q1 2013 (2013-04-25 to 2013-07-19) | 13 | +56.3% | +33.8% to +82.8% | 13 | 12 | +29.5% | 13 |
| latest print Q2 2013 (2013-07-25 to 2013-10-18) | 13 | +68.6% | +59.1% to +89.1% | 13 | 13 | +38.8% | 13 |
| latest print Q3 2013 (2013-10-24 to 2013-12-31) | 11 | +74.5% | +62.7% to +78.9% | 11 | 11 | +53.3% | 11 |

- **CHEAP held on 52 of 53 dates of 2013.** From $48.38-57.51 (11.2-14.4x) the entries returned +31.1% to +89.1% (median +62.7%)
  against SPY's +14.6% to +45.3%; 40 beat SPY. The miss is 2013-03-08 (+31.1%, 7.0pp behind SPY). The floor was reached within two years
  on all 53 dates, and the two-year price landed nearest BASE on 47 and BULL on 6. Over three years (to 2016-12-30) +34.8% to +80.0%: 52
  beat SPY but only 34 cleared the +52.1% hurdle.
- **The late entries did best, not the cheapest.** The dates after the Q2 and Q3 2013 prints (FY13E $4.33-4.355, 11.2-12.5x) returned
  +59.1% to +89.1%; those after the Q4 2012 print (FY13E $4.175, up to 13.8x) +31.1% to +44.1%. Cymbalta lost U.S. exclusivity in
  December 2013, at the start of these horizons.

## 2014 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 4 | +64.1% | +54.5% to +72.6% | 4 | 4 | +52.3% | 4 |
| class RICH, legacy tier AVOID | 48 | +31.6% | -0.8% to +53.8% | 19 | 43 | +28.8% | 5 |
| FY13E $4.355 (2014-01-03 to 2014-01-24) | 4 | +64.1% | +54.5% to +72.6% | 4 | 4 | +52.3% | 4 |
| FY14E $2.81 (2014-01-31 to 2014-04-17) | 12 | +32.1% | +28.5% to +53.8% | 5 | 12 | +37.7% | 0 |
| FY14E $2.74 (2014-04-25 to 2014-07-18) | 13 | +32.2% | +24.6% to +41.1% | 8 | 13 | +34.3% | 0 |
| FY14E $2.71 (2014-07-25 to 2014-10-17) | 13 | +31.9% | +25.0% to +43.7% | 6 | 13 | +24.1% | 0 |
| FY14E $2.38 (2014-10-24 to 2014-12-26) | 10 | +17.0% | -0.8% to +23.5% | 0 | 5 | +15.8% | 5 |
| latest print Q3 2013 (2014-01-03 to 2014-01-24) | 4 | +64.1% | +54.5% to +72.6% | 4 | 4 | +52.3% | 4 |
| latest print Q4 2013 (2014-01-31 to 2014-04-17) | 12 | +32.1% | +28.5% to +53.8% | 5 | 12 | +37.7% | 0 |
| latest print Q1 2014 (2014-04-25 to 2014-07-18) | 13 | +32.2% | +24.6% to +41.1% | 8 | 13 | +34.3% | 0 |
| latest print Q2 2014 (2014-07-25 to 2014-10-17) | 13 | +31.9% | +25.0% to +43.7% | 6 | 13 | +24.1% | 0 |
| latest print Q3 2014 (2014-10-24 to 2014-12-26) | 10 | +17.0% | -0.8% to +23.5% | 0 | 5 | +15.8% | 5 |

- **CHEAP held on all 4 dates of January 2014; RICH held on 5 of 48.** The January entries ($51.10-55.16, 11.7-12.7x the FY2013 guide)
  returned +54.5% to +72.6% over two years, 47.8-56.8pp ahead of SPY. From the Q4 2013 print the models called RICH (18.9-32.9x the
  falling FY2014 guide, against the window's 12.7x median), and the entries of 2014-01-31 to 2014-10-17 still returned +24.6% to +53.8%,
  beating SPY's +5.8% to +17.9% on every one (by 12.2-40.6pp) and clearing the hurdle on 19. The call held only on the 5 dates from
  2014-11-28 to 2014-12-26 ($68.12-72.40, 28.6-30.4x): -0.8% to +10.6%, under the hurdle and 1.9-13.9pp behind SPY. Over three years the 2014
  entries returned +28.2% to +58.4% (median +43.8%) and 46 beat SPY.
- **The two-year price landed nearest BULL on 49 of 52 dates** ($67.20-84.26), BASE on 3; the floor ($31-48) was never touched (the
  worst drawdown within two years was -26.7%). FY2014's reported EPS came in at $2.23 against FY2013's $4.32, at the top of the last
  guide ($2.15-2.23); the market paid more for the smaller earnings, not less.

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 53 | +6.8% | -3.6% to +28.5% | 0 | 11 | -1.3% | 41 |
| FY14E $2.38 (2015-01-02 to 2015-01-02) | 1 | +10.7% | +10.7% to +10.7% | 0 | 0 | +9.0% | 1 |
| FY14E $2.19 (2015-01-09 to 2015-01-23) | 3 | +14.8% | +11.4% to +15.2% | 0 | 0 | +7.7% | 3 |
| FY15E $2.45 (2015-01-30 to 2015-04-17) | 12 | +20.0% | +9.4% to +28.5% | 0 | 10 | +7.8% | 2 |
| FY15E $2.26 (2015-04-24 to 2015-07-17) | 13 | +4.6% | -2.2% to +22.2% | 0 | 1 | -0.6% | 11 |
| FY15E $2.25 (2015-07-24 to 2015-10-16) | 13 | +4.7% | -3.6% to +10.5% | 0 | 0 | -5.5% | 13 |
| FY15E $2.425 (2015-10-23 to 2015-12-31) | 11 | +6.4% | +3.4% to +16.6% | 0 | 0 | -2.4% | 11 |
| latest print Q3 2014 (2015-01-02 to 2015-01-23) | 4 | +14.8% | +10.7% to +15.2% | 0 | 0 | +9.0% | 4 |
| latest print Q4 2014 (2015-01-30 to 2015-04-17) | 12 | +20.0% | +9.4% to +28.5% | 0 | 10 | +7.8% | 2 |
| latest print Q1 2015 (2015-04-24 to 2015-07-17) | 13 | +4.6% | -2.2% to +22.2% | 0 | 1 | -0.6% | 11 |
| latest print Q2 2015 (2015-07-24 to 2015-10-16) | 13 | +4.7% | -3.6% to +10.5% | 0 | 0 | -5.5% | 13 |
| latest print Q3 2015 (2015-10-23 to 2015-12-31) | 11 | +6.4% | +3.4% to +16.6% | 0 | 0 | -2.4% | 11 |

- **RICH held on 41 of 53 dates of 2015.** From $68.41-88.49 (27.9-39.3x the reported guide) the entries returned -3.6% to +28.5% over
  two years against SPY's +13.1% to +38.8%: none cleared the hurdle and only 11 beat SPY, all from 2015-02-06 to 2015-04-24 (by 0.7-9.7pp;
  the call missed on those 11 and on 2015-05-01, level with SPY). From 2015-05-08 it held on all 35 dates ($72.90-88.49, 32.3-39.3x:
  -3.6% to +16.6%, 1.5-34.6pp behind SPY). Over three years
  +6.4% to +49.0% (median +25.5%), none clearing the +52.1% hurdle and 10 beating SPY.
- The two-year price ($73.55-87.18) landed nearest XBULL on 43 dates and BULL on 10: the scenarios' prices sit far apart (BEAR $5-13,
  XBULL $96-106), and a flat price two years on is closest to the top case. The worst drawdown within two years was -21.7% to -26.7%.

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +20.9% | +6.9% to +81.6% | 20 | 18 | +10.4% | 32 |
| FY15E $2.305 (2016-01-08 to 2016-01-22) | 3 | +11.1% | +8.6% to +12.1% | 0 | 0 | +1.4% | 3 |
| FY16E $2.88 (2016-01-29 to 2016-04-22) | 13 | +11.1% | +6.9% to +19.3% | 0 | 0 | +12.1% | 13 |
| FY16E $2.73 (2016-04-27 to 2016-10-21) | 26 | +23.3% | +10.7% to +48.5% | 10 | 8 | +8.3% | 16 |
| FY16E $2.71 (2016-10-26 to 2016-12-09) | 7 | +54.1% | +44.2% to +81.6% | 7 | 7 | +23.4% | 0 |
| FY16E $2.62 (2016-12-16 to 2016-12-30) | 3 | +58.6% | +54.2% to +61.2% | 3 | 3 | +26.4% | 0 |
| latest print Q3 2015 (2016-01-08 to 2016-01-22) | 3 | +11.1% | +8.6% to +12.1% | 0 | 0 | +1.4% | 3 |
| latest print Q4 2015 (2016-01-29 to 2016-04-22) | 13 | +11.1% | +6.9% to +19.3% | 0 | 0 | +12.1% | 13 |
| latest print Q1 2016 (2016-04-27 to 2016-07-22) | 13 | +15.4% | +10.7% to +23.3% | 0 | 0 | +9.3% | 13 |
| latest print Q2 2016 (2016-07-27 to 2016-10-21) | 13 | +39.7% | +20.9% to +48.5% | 10 | 8 | +8.3% | 3 |
| latest print Q3 2016 (2016-10-26 to 2016-12-30) | 10 | +58.6% | +44.2% to +81.6% | 10 | 10 | +26.4% | 0 |

- **RICH held on 32 of 52 dates of 2016.** The 32 entries to 2016-08-12 ($70.95-83.40, 24.6-35.8x) returned +6.9% to +32.1% over two
  years, under the hurdle and 1.9-44.7pp behind SPY, and the call held on every one; the 20 from 2016-08-19 ($67.71-82.09, 25.0-30.1x)
  returned +36.3% to +81.6%, cleared the hurdle on all 20 and beat SPY on 18, and it held on none. Over three years +37.8% to +89.5% (median +62.5%): 46 beat SPY and 33 cleared the hurdle.
- The two-year price ($74.76-118.64) landed nearest BULL on 28 dates and XBULL on 24; the floor ($29-40) was never touched.

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +46.9% | +29.7% to +61.4% | 48 | 52 | +35.1% | 0 |
| FY16E $2.62 (2017-01-06 to 2017-01-27) | 4 | +57.4% | +55.7% to +58.3% | 4 | 4 | +24.2% | 0 |
| FY17E $2.74 (2017-02-01 to 2017-04-21) | 12 | +57.7% | +46.1% to +61.4% | 12 | 12 | +22.6% | 0 |
| FY17E $2.65 (2017-04-26 to 2017-07-21) | 13 | +47.1% | +31.6% to +55.5% | 12 | 13 | +36.3% | 0 |
| FY17E $2.56 (2017-07-26 to 2017-10-20) | 13 | +42.1% | +29.7% to +49.5% | 10 | 13 | +39.0% | 0 |
| FY17E $1.78 (2017-10-25 to 2017-12-08) | 7 | +42.4% | +35.4% to +44.0% | 7 | 7 | +37.5% | 0 |
| FY17E $1.61 (2017-12-15 to 2017-12-29) | 3 | +61.4% | +46.0% to +61.4% | 3 | 3 | +36.5% | 0 |
| latest print Q3 2016 (2017-01-06 to 2017-01-27) | 4 | +57.4% | +55.7% to +58.3% | 4 | 4 | +24.2% | 0 |
| latest print Q4 2016 (2017-02-01 to 2017-04-21) | 12 | +57.7% | +46.1% to +61.4% | 12 | 12 | +22.6% | 0 |
| latest print Q1 2017 (2017-04-26 to 2017-07-21) | 13 | +47.1% | +31.6% to +55.5% | 12 | 13 | +36.3% | 0 |
| latest print Q2 2017 (2017-07-26 to 2017-10-20) | 13 | +42.1% | +29.7% to +49.5% | 10 | 13 | +39.0% | 0 |
| latest print Q3 2017 (2017-10-25 to 2017-12-29) | 10 | +44.0% | +35.4% to +61.4% | 10 | 10 | +37.5% | 0 |

- **RICH failed on all 52 dates of 2017.** From $75.38-87.23 (28.3-34.1x the reported guide to the Q3 2017 print, then 46.6-53.8x the
  $1.78 and $1.61 guides after the streamlining charges) the entries returned +29.7% to +61.4% over two years, 7.0-41.8pp ahead of SPY,
  and 48 cleared the hurdle. Over three years (to 2020-12-29) +54.5% to +111.6% (median +91.2%), every date ahead of SPY and over the
  hurdle. The two-year price ($106.79-132.43) landed nearest XBULL on all 52 dates.
- **The GAAP guide was not what failed.** The non-GAAP guides ($4.05-4.25 for FY2017) keep every 2017 date RICH (the build's
  sensitivity: the tier moves from AVOID to WATCHLIST on 33 dates, no class moves); the call rests on the window's 12.7x median, which
  the market never returned to, while the 2017 charges put the GAAP multiple at 47-54x without changing the class.

## Across 2008-2009

- **The ranks run through the price.** Across the 105 dates the entry price ranks the two-year return at Spearman -0.91 and the return to
  the m12-24 average price at -0.99; the P/E at -0.72 and -0.75 and the EPP gap at -0.73 and -0.76 (the right signs: the lower the
  multiple and the further under the floor, the better the return); Ratio B at -0.50 and -0.58 (right); the adjusted gap at -0.30 and
  -0.39 and the proxy composite at -0.29 and -0.41 (the wrong sign: a higher read went with lower returns); the P/E percentile at +0.50
  and +0.37 (wrong, as the 2009 window without FY2008's days had a lower median). One stock over two years mostly tests "buy lower"
  (retro/README.md, "Scoring a single stock").
- **The class carried no information here.** Every date was CHEAP and BUY with robustness 8 of 8, and no encoding the build tested moved a
  class (retro/README.md, "LLY"): the call rested entirely on the stock's own 1998-2007 P/E history, which the following years did not
  repeat. A series where a call never varies cannot separate good entries from bad ones; only the price did.

## Across 2010-2013

- **CHEAP held on 192 of 209 dates** (184 cleared the hurdle, 159 beat SPY), against 14 of 105 in 2008-2009. The models' call never
  changed (CHEAP and BUY, robustness 7-8 of 8); what changed was the starting point: entries at 7-14x the reported guide after the
  2008-2009 de-rating, instead of 7-20x into it.
- **The ranks ran the wrong way.** Over the 209 dates the entry price ranks the two-year return at Spearman +0.18 and the return to the
  m12-24 average price at +0.23; the P/E at +0.16 and +0.19, the P/E percentile at +0.27 and +0.31, the EPP gap at +0.33 and +0.38 and
  Ratio B at +0.29 and +0.33 (all the wrong sign: the dearer and less discounted entries did better); the adjusted gap at -0.36 and
  -0.39 and the proxy composite at -0.16 and -0.23 (wrong as well). The later entries had more of the 2013-2015 re-rating ahead of them.
- **The 2008-2009 hypothesis, tested on the next four years (hindsight, not a rule):** that a decade of the company's own multiples
  misreads a dated patent cliff. As a target it did: for the 2010-2011 entries the own-history floor (20-21x) was never reached within
  two years and the price landed nearest BEAR, at 10-14x. As a direction it did not: entries at single-digit multiples of the reported
  guide, with a 5-6% dividend yield, cleared the hurdle through Zyprexa's and Cymbalta's U.S. expiries. So the 2008-2009 failure reads as
  an entry multiple still too high for the cliff, not as a wrong call to buy at 7-9x. Test on other tickers with dated patent cliffs
  (the PFE and BMY series in staging have their own), never fit to LLY.

## Across 2008-2013

- **206 of 314 dates held** (0 in 2008, 14 in 2009, 192 in 2010-2013), every one CHEAP and BUY. Over the 314 dates the P/E percentile
  ranks the two-year return at Spearman +0.70 (m12-24 +0.69), Ratio B at +0.65 and +0.65, the EPP gap at +0.27 and +0.29, the entry
  price at +0.14 and +0.13, the P/E at -0.03 and -0.02, the adjusted gap at -0.65 and -0.69 and the proxy composite at -0.52 and -0.58:
  the window-based reads ranked the wrong way across the six years, because they read deepest cheapness in 2008-2009, when the
  1998-2007 window was least like the market that followed. Hypothesis: for one stock across a re-rating cycle the method's cheapness
  measures describe the window's composition more than the entry; the class, which never varied, could not separate the years.

## Across 2014-2017

- **The call held on 82 of 209 dates:** CHEAP on all 4, RICH on 78 of 205 (5 in 2014, 41 in 2015, 32 in 2016, 0 in 2017). The RICH
  entries' median two-year return was +29.5%; 87 cleared the hurdle and 124 beat SPY. The class rested on one fact of the window: its
  median stayed at 12.7x on every date, the multiple of the 2009-2013 patent-cliff years, which held most of its days, while the stock
  traded at 19-54x a reported guide that had halved.
- **The ranks ran the right way inside the four years.** Over the 209 dates the P/E percentile ranks the two-year return at Spearman
  -0.54 and the return to the m12-24 average price at -0.60, Ratio B at -0.58 and -0.67, the P/E at -0.28 and -0.41, the EPP gap at -0.27
  and -0.41 and the entry price at -0.13 and -0.34 (the dearer the entry by each read, the lower the return), and the adjusted gap at
  +0.41 and +0.32 and the proxy composite at +0.26 and +0.03 (the higher the read, the better). The measures ordered the dates; the
  level they were judged against, a window anchored on the cliff years, did not fit the market that followed.
- **The 2008-2009 hypothesis, seen from the other side (hindsight, not a rule):** in 2008-2009 a window anchored on the 1998-2007
  multiples (18-30x) called a stock entering a patent cliff cheap at 7-15x, and it kept falling; in 2014-2017 a window anchored on the
  cliff years' 7-11x called the stock dear at 19-54x as the market priced the new launches (Trulicity, Taltz, Basaglar, Jardiance and the
  rest, named in the releases from 2014), and it kept rising. Both are the same reading: a ten-year own-history window describes the last
  regime, and LLY changed regime twice. Test it on other tickers whose earnings regime turned within the window (the PFE and BMY series in
  staging have their own cliffs), never fit it to LLY.

## Across 2008-2017

- **288 of 523 dates held** (CHEAP on 210 of 318, RICH on 78 of 205). Over the 523 dates every cheapness measure ranks the two-year
  return near zero (Spearman: the P/E percentile +0.06, Ratio B +0.03, the EPP gap -0.08, the P/E -0.20, the entry price -0.11, the
  adjusted gap -0.05, the proxy composite -0.15; m12-24 within -0.33 to +0.19): across two re-ratings the window-based reads describe the
  window's composition more than the entry, as the 2008-2013 section found, and inside each regime they rank correctly.
- **Profile drift:** the point-in-time profile (DURABLE, risk 2) against today's (DURABLE, risk 1, reviewed 2026-09-22) is a label only.
