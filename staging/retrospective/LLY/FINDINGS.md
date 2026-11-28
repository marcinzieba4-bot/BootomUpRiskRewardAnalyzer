# LLY retrospective findings (hindsight)

Patterns seen in `outcome.json` for the LLY weekly dates: 987, 105 from 2008-01-04 to 2009-12-31, 209 from 2010-01-08 to 2013-12-31, 209
from 2014-01-03 to 2017-12-29, 209 from 2018-01-05 to 2021-12-31 and 255 from 2022-01-07 to 2026-11-20, all Eli Lilly and Company (NYSE: LLY). They are **labels and
hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its point-in-time build was
committed and pushed (8d1f450, the empty-slot correction the firewall found 96e4c9f, firewall result 73b08d1); the outcomes were
computed on 2026-11-21. The 2010-2013 batch was scored only after its build, checks, README section and firewall result were committed
and pushed (5a27368, f8db0dc, 5446ffc), on 2026-11-21. The 2014-2017 batch was built in a new session and scored only after its build,
checks, README section and firewall result were committed and pushed (c64c37a, 3e0e6d0, b3185fb), on 2026-11-22; this file was first
opened in that session after those pushes. The 2018-2021 batch was decided in the session that scored 2014-2017 (disclosed in
retro/README.md, "LLY 2018-2021") and scored only after its build, checks, README section and firewall result were committed and pushed
(3d43bb4, c09f6e0, 0dff694, a7c7fc1), on 2026-11-22. The 2022-2026 batch was built in a new session that had not opened this file or
any outcome (retro/README.md, "LLY 2022-2026"), and scored only after its build, validation, README section and firewall result were
committed and pushed (1355375, 4d1c23e, 6d96cd3, 8b33071), on 2026-11-23. Every date to 2021 has its 6-month, 1-, 2- and 3-year horizons (the last ends 2012-12-31
for 2008-2009, 2016-12-30 for 2010-2013, 2020-12-29 for 2014-2017 and 2024-12-30 for 2018-2021). Total returns include the quarterly
dividends ($0.425 to the ex-date of 2008-02-13, $0.47 from it, $0.49 from 2009-02-11, $0.50 from 2015-02-11, $0.51 from 2016-02-10,
$0.52 from 2017-02-13, $0.5625 from 2018-02-14, $0.645 from 2019-02-14, $0.74 from 2020-02-13, $0.85 from 2021-02-11, $0.98 from
2022-02-14, $1.13 from 2023-02-14, $1.30 from 2024-02-14, $1.50 from 2025-02-14 and $1.73 from 2026-02-13). Not every 2022-2026 date has
every horizon yet: 150 have the 2-year one (to 2024-11-15), 202 the 1-year (to 2025-11-14), 228 the 6-month (to 2026-05-15), and
2026-11-20 has none; the 3-year horizon reaches 2023-11-14 (98 dates). No split falls in any horizon, so every price is as traded. Medians of an
even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over three.
"Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY), RICH should miss the hurdle and lag it, FAIR
should land within 15pp of it either way. Every date of 2008-2013 was CHEAP and BUY, so their tables test that one call against the
calendar; 2014-2017 has 4 CHEAP and BUY dates and 205 RICH and AVOID; 2018-2021 has 168 RICH, 39 FAIR and 2 CHEAP dates; 2022-2026 has 166 RICH (all 156 dates to 2025-01-31
among them), 87 CHEAP (from the Q4 2024 print) and 2 FAIR.

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

## 2018 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 27 | +46.0% | +27.4% to +70.8% | 22 | 22 | +31.1% | 3 |
| class RICH, legacy tier WATCHLIST | 24 | +87.4% | +65.9% to +107.0% | 24 | 24 | +51.2% | 0 |
| class RICH, legacy tier ACCUMULATE | 1 | +101.9% | +101.9% to +101.9% | 1 | 1 | +57.1% | 0 |
| FY17E $1.61 (2018-01-05 to 2018-01-26) | 4 | +65.3% | +57.8% to +68.9% | 4 | 4 | +35.5% | 0 |
| FY18E $4.44 (2018-02-01 to 2018-04-20) | 12 | +85.0% | +65.9% to +105.9% | 12 | 12 | +53.8% | 0 |
| FY18E $4.57 (2018-04-25 to 2018-07-20) | 13 | +94.7% | +68.9% to +107.0% | 13 | 13 | +49.5% | 0 |
| FY18E $3.24 (2018-07-25 to 2018-11-02) | 15 | +45.9% | +28.3% to +70.8% | 13 | 15 | +30.6% | 0 |
| FY18E $3.065 (2018-11-07 to 2018-12-14) | 6 | +34.7% | +27.4% to +46.0% | 3 | 2 | +28.8% | 3 |
| FY18E $2.825 (2018-12-21 to 2018-12-28) | 2 | +59.3% | +50.6% to +59.3% | 2 | 1 | +35.2% | 0 |
| latest print Q3 2017 (2018-01-05 to 2018-01-26) | 4 | +65.3% | +57.8% to +68.9% | 4 | 4 | +35.5% | 0 |
| latest print Q4 2017 (2018-02-01 to 2018-04-20) | 12 | +85.0% | +65.9% to +105.9% | 12 | 12 | +53.8% | 0 |
| latest print Q1 2018 (2018-04-25 to 2018-07-20) | 13 | +94.7% | +68.9% to +107.0% | 13 | 13 | +49.5% | 0 |
| latest print Q2 2018 (2018-07-25 to 2018-11-02) | 15 | +45.9% | +28.3% to +70.8% | 13 | 15 | +30.6% | 0 |
| latest print Q3 2018 (2018-11-07 to 2018-12-28) | 8 | +35.0% | +27.4% to +59.3% | 5 | 3 | +30.0% | 3 |

- **RICH failed on 49 of 52 dates of 2018 and held on 3 (2018-11-16 to 2018-11-30).** From $74.76-118.64, 16.8-54.1x the reported guide
  (FY17E $1.61 in January, then FY18E $4.44 to $2.825 as the reported range fell from $4.39-4.49 to $2.80-2.85 with acquired in-process
  research and development and other listed charges, the ARMO BioSciences acquisition among them, while the non-GAAP range rose from
  $4.81-4.91 to $5.55-5.60) against a 12.0-12.7x window median, the 45 entries from 2018-01-05 to 2018-11-07 returned +28.3% to +107.0%
  over two years, 2.8-96.2pp ahead of SPY, and 43 cleared the hurdle. The call held only on the 3 entries of 2018-11-16 to 2018-11-30
  ($112.87-118.64, 36.8-38.7x): +27.4% to +31.9%, under the hurdle and 8.0-8.2pp behind SPY's +35.4% to +40.0%. The call missed again on
  the 4 December entries, which cleared the hurdle. Over three years the 2018 entries returned +101.1% to +179.0% (median +150.2%),
  every one ahead of SPY and over the +52.1% hurdle.
- **The cheapest entries by the stock's own reads did best.** The 24 WATCHLIST dates and the one ACCUMULATE date (2018-02-01 to
  2018-07-20, 16.8-19.6x against the 12.0-12.4x median) returned +65.9% to +107.0%; the 27 AVOID dates, mostly after the guide cuts,
  +27.4% to +70.8%. The two-year price ($119.05-168.78) landed nearest XBULL on 36 dates and BULL on 16; the floor ($26-50) was never
  touched (the worst drawdown within two years was -18.5% to -22.9%).

## 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +107.0% | +48.0% to +150.2% | 52 | 51 | +57.3% | 0 |
| FY18E $2.825 (2019-01-04 to 2019-02-01) | 5 | +68.4% | +49.2% to +89.5% | 5 | 4 | +29.1% | 0 |
| FY19E $4.62 (2019-02-07 to 2019-04-26) | 12 | +64.7% | +48.0% to +76.4% | 12 | 12 | +28.7% | 0 |
| FY19E $4.69 (2019-05-01 to 2019-12-27) | 15 | +103.8% | +59.5% to +130.1% | 15 | 15 | +53.7% | 0 |
| FY19E $4.7 (2019-07-31 to 2019-10-18) | 12 | +129.0% | +104.7% to +150.2% | 12 | 12 | +71.8% | 0 |
| FY19E $4.71 (2019-10-24 to 2019-12-13) | 8 | +129.6% | +109.7% to +134.9% | 8 | 8 | +83.9% | 0 |
| latest print Q3 2018 (2019-01-04 to 2019-02-01) | 5 | +68.4% | +49.2% to +89.5% | 5 | 4 | +29.1% | 0 |
| latest print Q4 2018 (2019-02-07 to 2019-04-26) | 12 | +64.7% | +48.0% to +76.4% | 12 | 12 | +28.7% | 0 |
| latest print Q1 2019 (2019-05-01 to 2019-07-26) | 13 | +98.0% | +59.5% to +130.1% | 13 | 13 | +49.8% | 0 |
| latest print Q2 2019 (2019-07-31 to 2019-10-18) | 12 | +129.0% | +104.7% to +150.2% | 12 | 12 | +71.8% | 0 |
| latest print Q3 2019 (2019-10-24 to 2019-12-27) | 10 | +127.1% | +103.8% to +134.9% | 10 | 10 | +83.6% | 0 |

- **RICH failed on all 52 dates of 2019.** From $106.79-132.43, 22.8-42.8x the reported guide (FY18E $2.825 in January, then FY19E
  $4.62-4.71, from continuing operations once Elanco was discontinued), the entries returned +48.0% to +150.2% over two years, every one
  over the hurdle and 51 ahead of SPY (2019-01-04 trailed by 1.4pp; the margin elsewhere was 3.9-91.2pp). Over three years +100.3% to
  +231.8% (median +177.7%), every date ahead of SPY. The two-year price ($165.50-278.41) landed nearest XBULL on all 52; the floor
  ($45-75) was never touched.
- **The window turned in one week and the class held.** As the 2009-2013 days fell below half of the window, its median crossed the gap
  between the two regimes, from 14.7x on 2019-06-28 to 22.9x on 2019-07-05 (24.6x by December). The class stayed RICH because Ratio B
  stayed at 2.2-9.3 (unbounded on 5 dates), with BEAR at the history's worst year (FY2014's -48.4%, and -53.5% from the recast's seam of
  2019-10-24).
- **Hindsight on the build's largest EPS call** (a label, not a reason to change it): the FY2019 guides with the Elanco gain
  ($8.57-8.69, discontinued operations in) would have made 33 dates of 2019-05-01 to 2019-12-13 CHEAP, and every one of them would have
  held (+59.5% to +150.2%). The encoding read from continuing operations follows the written rule (EPS from continuing operations
  wherever reported) and stays.

## 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 19 | +104.2% | +75.1% to +157.4% | 19 | 19 | +64.3% | 0 |
| class FAIR, legacy tier WATCHLIST | 26 | +119.0% | +71.0% to +179.5% | 26 | 26 | +83.1% | 0 |
| class FAIR, legacy tier AVOID | 6 | +102.2% | +70.7% to +116.0% | 6 | 6 | +67.8% | 0 |
| class CHEAP, legacy tier WATCHLIST | 1 | +103.4% | +103.4% to +103.4% | 1 | 1 | +84.2% | 1 |
| class CHEAP, legacy tier ACCUMULATE | 1 | +140.4% | +140.4% to +140.4% | 1 | 1 | +93.0% | 1 |
| FY19E $4.69 (2020-01-03 to 2020-01-24) | 4 | +93.1% | +77.5% to +111.0% | 4 | 4 | +64.4% | 0 |
| FY20E $6.23 (2020-01-31 to 2020-04-17) | 12 | +96.1% | +70.7% to +140.4% | 12 | 12 | +66.3% | 2 |
| FY20E $6.3 (2020-04-24 to 2020-12-11) | 21 | +106.7% | +75.1% to +179.5% | 21 | 21 | +68.4% | 0 |
| FY20E $6.58 (2020-07-31 to 2020-10-23) | 13 | +119.0% | +101.5% to +144.3% | 13 | 13 | +83.8% | 0 |
| FY20E $6.38 (2020-12-18 to 2020-12-31) | 3 | +121.0% | +114.2% to +125.1% | 3 | 3 | +82.0% | 0 |
| latest print Q3 2019 (2020-01-03 to 2020-01-24) | 4 | +93.1% | +77.5% to +111.0% | 4 | 4 | +64.4% | 0 |
| latest print Q4 2019 (2020-01-31 to 2020-04-17) | 12 | +96.1% | +70.7% to +140.4% | 12 | 12 | +66.3% | 2 |
| latest print Q1 2020 (2020-04-24 to 2020-07-24) | 14 | +103.9% | +75.1% to +116.0% | 14 | 14 | +63.3% | 0 |
| latest print Q2 2020 (2020-07-31 to 2020-10-23) | 13 | +119.0% | +101.5% to +144.3% | 13 | 13 | +83.8% | 0 |
| latest print Q3 2020 (2020-10-28 to 2020-12-31) | 10 | +152.7% | +114.2% to +179.5% | 10 | 10 | +101.9% | 0 |

- **The call held on 2 of 53 dates, both CHEAP.** The entries of 2020-02-28 ($126.13, 20.2x the $6.23 guide) and 2020-03-20 ($122.40,
  19.6x, in the March sell-off) returned +103.4% and +140.4% over two years, 52.2 and 41.1pp ahead of SPY. FAIR, on 32 dates
  ($131.31-154.17, 20.8-24.4x against a 23.3-24.3x median), failed on every one: the call expects a return within 15pp of SPY's, and the
  entries returned +70.7% to +179.5%, 27.2-156.8pp ahead. RICH, on 19 dates ($131.77-171.40, 23.6-29.8x), failed on every one: +75.1% to
  +157.4%, 20.5-144.2pp ahead.
- **The floor was reached for the first time in the batch:** the 8 entries of 2020-01-31 to 2020-03-20 saw $119.05 within two years,
  under their $124.60-130.83 floor (the March 2020 low). The two-year price ($234.69-374.76) landed nearest XBULL on 49 dates and BULL
  on 4. Over three years +133.0% to +337.9% (median +194.4%), every date ahead of SPY.

## 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 45 | +116.3% | +55.0% to +159.5% | 45 | 45 | +63.2% | 0 |
| class FAIR, legacy tier WATCHLIST | 5 | +89.5% | +82.7% to +108.2% | 5 | 5 | +76.6% | 0 |
| class FAIR, legacy tier AVOID | 2 | +123.5% | +102.0% to +123.5% | 2 | 2 | +84.5% | 0 |
| FY20E $6.38 (2021-01-08 to 2021-01-22) | 3 | +93.4% | +71.4% to +122.5% | 3 | 3 | +63.2% | 0 |
| FY21E $7.425 (2021-01-29 to 2021-04-23) | 13 | +71.7% | +55.0% to +108.2% | 13 | 13 | +59.7% | 0 |
| FY21E $7.13 (2021-04-28 to 2021-07-30) | 14 | +108.5% | +91.5% to +125.4% | 14 | 14 | +60.9% | 0 |
| FY21E $6.83 (2021-08-04 to 2021-10-22) | 12 | +141.2% | +74.3% to +159.5% | 12 | 12 | +72.6% | 0 |
| FY21E $6.43 (2021-10-27 to 2021-12-10) | 7 | +133.0% | +117.3% to +148.4% | 7 | 7 | +70.3% | 0 |
| FY21E $6.205 (2021-12-17 to 2021-12-31) | 3 | +114.1% | +111.9% to +117.1% | 3 | 3 | +68.9% | 0 |
| latest print Q3 2020 (2021-01-08 to 2021-01-22) | 3 | +93.4% | +71.4% to +122.5% | 3 | 3 | +63.2% | 0 |
| latest print Q4 2020 (2021-01-29 to 2021-04-23) | 13 | +71.7% | +55.0% to +108.2% | 13 | 13 | +59.7% | 0 |
| latest print Q1 2021 (2021-04-28 to 2021-07-30) | 14 | +108.5% | +91.5% to +125.4% | 14 | 14 | +60.9% | 0 |
| latest print Q2 2021 (2021-08-04 to 2021-10-22) | 12 | +141.2% | +74.3% to +159.5% | 12 | 12 | +72.6% | 0 |
| latest print Q3 2021 (2021-10-27 to 2021-12-31) | 10 | +130.2% | +111.9% to +148.4% | 10 | 10 | +70.3% | 0 |

- **No call held in 2021.** RICH on 45 dates ($166.41-276.22, 26.1-44.5x the reported guide: FY20E $6.38 in January, then FY21E falling
  from $7.425 to $6.205 with acquired in-process research and development and other listed charges, while the non-GAAP range rose from
  $7.75-8.40 to $8.15-8.20) and FAIR on 7 (2021-03-19 to 2021-04-28, $180.55-189.25, 24.8-25.5x against a 24.3-24.8x median). The
  entries returned +55.0% to +159.5% over two years against SPY's -6.7% to +12.9%, every one over the hurdle and 49.1-159.9pp ahead.
  Over three years (to 2024-12-30) +185.1% to +326.0% (median +282.7%).
- The two-year price ($315.02-609.20) landed nearest XBULL on 38 dates and BULL on 14; the floor ($137-157) was never touched (the worst
  drawdown within two years was -17.1% to -18.7%).

## 2022 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +168.2% | +103.8% to +229.1% | 52 | 52 | +110.8% | 0 |
| FY21E $6.205 (2022-01-07 to 2022-01-28) | 4 | +164.3% | +141.6% to +166.8% | 4 | 4 | +96.9% | 0 |
| FY22E $8.075 (2022-02-04 to 2022-04-22) | 12 | +179.1% | +151.9% to +229.1% | 12 | 12 | +100.0% | 0 |
| FY22E $7.375 (2022-04-29 to 2022-07-29) | 14 | +176.1% | +147.8% to +207.4% | 14 | 14 | +103.2% | 0 |
| FY22E $7.035 (2022-08-05 to 2022-10-28) | 13 | +188.5% | +151.5% to +221.7% | 13 | 13 | +130.1% | 0 |
| FY22E $6.575 (2022-11-02 to 2022-12-30) | 9 | +119.1% | +103.8% to +139.0% | 9 | 9 | +119.8% | 0 |
| latest print Q3 2021 (2022-01-07 to 2022-01-28) | 4 | +164.3% | +141.6% to +166.8% | 4 | 4 | +96.9% | 0 |
| latest print Q4 2021 (2022-02-04 to 2022-04-22) | 12 | +179.1% | +151.9% to +229.1% | 12 | 12 | +100.0% | 0 |
| latest print Q1 2022 (2022-04-29 to 2022-07-29) | 14 | +176.1% | +147.8% to +207.4% | 14 | 14 | +103.2% | 0 |
| latest print Q2 2022 (2022-08-05 to 2022-10-28) | 13 | +188.5% | +151.5% to +221.7% | 13 | 13 | +130.1% | 0 |
| latest print Q3 2022 (2022-11-02 to 2022-12-30) | 9 | +119.1% | +103.8% to +139.0% | 9 | 9 | +119.8% | 0 |

- **No call held in 2022.** RICH and AVOID on all 52 dates ($235.74-374.76, 29.2-57.0x the reported guide: FY21E $6.205 in January, then
  FY22E falling from $8.075 to $6.575 on the acquired IPR&D and milestone charges, while the non-GAAP range fell less, $8.50-8.65 to
  $7.70-7.85), the 57th-100th percentile of a 27.4-29.7x median. The entries returned +103.8% to +229.1% over two years against SPY's
  +3.2% to +67.2%, every one over the hurdle and 51.9-211.1pp ahead; over three years +112.0% to +272.7% (median +165.8%), every one ahead.
- The two-year price landed nearest XBULL on all 52 dates; the floor ($149-177) was never touched (the worst drawdown within two years
  -17.1% to -24.3%).

## 2023 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +78.5% | +20.9% to +195.1% | 47 | 39 | +84.1% | 5 |
| FY22E $6.575 (2023-01-06 to 2023-01-27) | 4 | +123.2% | +112.5% to +139.1% | 4 | 4 | +136.6% | 0 |
| FY23E $8 (2023-02-03 to 2023-04-21) | 12 | +154.6% | +103.2% to +195.1% | 12 | 12 | +149.7% | 0 |
| FY23E $8.28 (2023-04-28 to 2023-08-04) | 15 | +73.4% | +67.2% to +124.2% | 15 | 15 | +87.3% | 0 |
| FY23E $9.3 (2023-08-09 to 2023-10-27) | 12 | +36.3% | +20.9% to +51.4% | 7 | 0 | +45.1% | 5 |
| FY23E $6.05 (2023-11-03 to 2023-12-29) | 9 | +79.9% | +59.8% to +90.7% | 9 | 8 | +38.1% | 0 |
| latest print Q3 2022 (2023-01-06 to 2023-01-27) | 4 | +123.2% | +112.5% to +139.1% | 4 | 4 | +136.6% | 0 |
| latest print Q4 2022 (2023-02-03 to 2023-04-21) | 12 | +154.6% | +103.2% to +195.1% | 12 | 12 | +149.7% | 0 |
| latest print Q1 2023 (2023-04-28 to 2023-08-04) | 15 | +73.4% | +67.2% to +124.2% | 15 | 15 | +87.3% | 0 |
| latest print Q2 2023 (2023-08-09 to 2023-10-27) | 12 | +36.3% | +20.9% to +51.4% | 7 | 0 | +45.1% | 5 |
| latest print Q3 2023 (2023-11-03 to 2023-12-29) | 9 | +79.9% | +59.8% to +90.7% | 9 | 8 | +38.1% | 0 |

- **The call held on 5 of 52 dates, all in the block after the Q2 2023 print** (FY23E $9.30, 2023-08-09 to 2023-10-27, $526.23-609.20 at
  57-66x): those 12 entries returned +20.9% to +51.4% over two years and lagged SPY's +46.1% to +70.3% on all 12, so the RICH call held
  where they also missed the hurdle. The other 40 RICH dates ($315.02-601.10, 39.4-99.4x) returned +59.8% to +195.1%, 39 of them ahead of
  SPY. Over three years +94.4% to +229.1% (median +152.0%) on the 46 dates that have it, every one ahead of SPY.
- **The dearest reading was among the better entries:** after the Q3 2023 print the acquired IPR&D charges cut FY23E to $6.05, and
  $567.81-601.10 read 94-99x, the 100th percentile; those 9 entries returned +59.8% to +90.7%, 8 ahead of SPY. The two-year price landed
  nearest XBULL on 50 dates and BULL on 2; the floor was never touched (drawdowns -24.3% to -34.8%).

## 2024 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 43 | +33.4% | +14.4% to +95.2% | 23 | 14 | +12.9% | 19 |
| class RICH, legacy tier WATCHLIST | 3 | +36.2% | +30.2% to +44.1% | 2 | 1 | +18.4% | 1 |
| FY23E $6.05 (2024-01-05 to 2024-02-02) | 5 | +68.0% | +58.1% to +70.2% | 5 | 5 | +32.4% | 0 |
| FY24E $12.05 (2024-02-07 to 2024-04-26) | 12 | +31.5% | +14.4% to +47.4% | 4 | 2 | +13.5% | 7 |
| FY24E $13.3 (2024-05-01 to 2024-08-02) | 14 | +34.0% | +25.5% to +50.1% | 8 | 3 | +11.1% | 6 |
| FY24E $15.35 (2024-08-09 to 2024-10-25) | 12 | +30.2% | +22.1% to +44.1% | 5 | 2 | +12.6% | 7 |
| FY24E $12.3 (2024-10-31 to 2024-12-27) | 3 | +72.3% | +64.3% to +95.2% | 3 | 3 | +31.1% | 0 |
| latest print Q3 2023 (2024-01-05 to 2024-02-02) | 5 | +68.0% | +58.1% to +70.2% | 5 | 5 | +32.4% | 0 |
| latest print Q4 2023 (2024-02-07 to 2024-04-26) | 12 | +31.5% | +14.4% to +47.4% | 4 | 2 | +13.5% | 7 |
| latest print Q1 2024 (2024-05-01 to 2024-08-02) | 14 | +34.0% | +25.5% to +50.1% | 8 | 3 | +11.1% | 6 |
| latest print Q2 2024 (2024-08-09 to 2024-10-25) | 12 | +30.2% | +22.1% to +44.1% | 5 | 2 | +12.6% | 7 |
| latest print Q3 2024 (2024-10-31 to 2024-12-27) | 3 | +72.3% | +64.3% to +95.2% | 3 | 3 | +31.1% | 0 |

1-year horizon (the 6 dates without a 2-year one):

| Group | Dates | Median 1-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median SPY |
|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 6 | +38.4% | +22.9% to +42.5% | 6 | 6 | +14.6% |
| FY24E $12.3 (2024-11-22 to 2024-12-27) | 6 | +38.4% | +22.9% to +42.5% | 6 | 6 | +14.6% |
| latest print Q3 2024 (2024-11-22 to 2024-12-27) | 6 | +38.4% | +22.9% to +42.5% | 6 | 6 | +14.6% |

- **The RICH call held on 20 of the 46 dates with a two-year outcome,** all from the Q4 2023 print to the Q3 2024 print (FY24E $12.05,
  $13.30, $15.35; $725.38-960.02 at 57-71x, the 80th-93rd percentile): those 38 entries returned +14.4% to +50.1% over two years, over the
  hurdle on 17 and ahead of SPY on 7. The January entries on FY23E $6.05 and the November ones on FY24E $12.30 returned +58.1% to +95.2%,
  every one ahead. The 6 December dates with a one-year outcome only returned +22.9% to +42.5%, every one ahead of SPY.
- The two-year price landed nearest BULL on 41 dates and XBULL on 5; the floor ($313-359) was never touched, the drawdowns within two
  years -32.7% to -34.8%.

## 2025 (52 dates; 1-year horizon only)

| Group | Dates | Median 1-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median SPY |
|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 41 | +47.2% | +0.6% to +90.5% | 35 | 32 | +19.8% |
| class RICH, legacy tier AVOID | 4 | +36.3% | +28.6% to +38.9% | 4 | 4 | +16.6% |
| class RICH, legacy tier WATCHLIST | 1 | +43.9% | +43.9% to +43.9% | 1 | 1 | +17.0% |
| FY24E $12.3 (2025-01-03 to 2025-01-31) | 5 | +36.3% | +28.6% to +43.9% | 5 | 5 | +16.6% |
| FY25E $22.8 (2025-02-07 to 2025-04-25) | 12 | +16.3% | +0.6% to +29.1% | 6 | 5 | +18.0% |
| FY25E $20.92 (2025-05-02 to 2025-08-01) | 14 | +50.1% | +17.7% to +56.6% | 14 | 12 | +25.5% |
| FY25E $21.475 (2025-08-08 to 2025-10-24) | 12 | +59.0% | +36.9% to +90.5% | 12 | 12 | +19.8% |
| FY25E $22.15 (2025-10-31 to 2025-12-26) | 3 | +47.2% | +41.5% to +65.1% | 3 | 3 | +11.9% |
| latest print Q3 2024 (2025-01-03 to 2025-01-31) | 5 | +36.3% | +28.6% to +43.9% | 5 | 5 | +16.6% |
| latest print Q4 2024 (2025-02-07 to 2025-04-25) | 12 | +16.3% | +0.6% to +29.1% | 6 | 5 | +18.0% |
| latest print Q1 2025 (2025-05-02 to 2025-08-01) | 14 | +50.1% | +17.7% to +56.6% | 14 | 12 | +25.5% |
| latest print Q2 2025 (2025-08-08 to 2025-10-24) | 12 | +59.0% | +36.9% to +90.5% | 12 | 12 | +19.8% |
| latest print Q3 2025 (2025-10-31 to 2025-12-26) | 3 | +47.2% | +41.5% to +65.1% | 3 | 3 | +11.9% |

- **CHEAP and BUY on the 47 dates from the Q4 2024 print; on the 41 with a one-year outcome the call held on 35** (the CHEAP test applied
  to one year: over the 15% hurdle or ahead of SPY). The entries returned +0.6% to +90.5% (median +47.2% against SPY's +19.8%). The class
  turned on BASE, not on the window: the FY2025 revenue guide of +28.8% to +41.0% put the BASE case at $1,310-1,565 against prices of
  $625.65-1,080.36 (29.1-48.8x the guide, the 33rd-76th percentile of a 34.2-35.2x median).
- **The first CHEAP block was the weakest:** FY25E $22.80 (2025-02-07 to 2025-04-25, $732.41-920.63) returned +0.6% to +29.1%, ahead of SPY
  on 5 of 12; the block after the Q2 2025 print, which held the series low ($625.65 on 2025-08-08, 29.1x), the strongest (+36.9% to
  +90.5%, all ahead). Inside the 41 CHEAP dates Ratio B ranks the one-year return at Spearman -0.49, the EPP gap at -0.39 and the adjusted
  gap at +0.30 (all the right sign), the entry price at -0.61.
- The 5 RICH dates of January 2025 (FY24E $12.30, $725.72-811.08, 59-66x) returned +28.6% to +43.9% over one year, all ahead of SPY. The 6
  CHEAP dates of 2025-11-21 to 2025-12-26 have a six-month horizon only: -1.4% to +12.4%.

## 2026 (46 dates; 6-month horizon only)

- 20 dates have a six-month outcome, all CHEAP (2026-01-02 to 2026-05-15, $878.24-1,080.36; BUY or ACCUMULATE, FY25's $22.95 standing for
  FY26E from 2026-02-05): +11.7% to +47.5%. The RICH and FAIR dates from 2026-08-21 and the rest have no horizon yet; score them when they do.

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

## Across 2018-2021

- **The call held on 5 of 209 dates:** CHEAP on 2 of 2, RICH on 3 of 168, FAIR on 0 of 39. The RICH entries' median two-year return was
  +94.7%; 163 cleared the hurdle and 162 beat SPY. A CHEAP call would have held on 206 of the 209 dates (the entries cleared the hurdle
  on 204 and beat SPY on 203): RICH could hold only on the 3 dates where CHEAP would not.
- **The ranks ran the right way inside the four years, as in 2014-2017.** Over the 209 dates the EPP gap ranks the two-year return at
  Spearman -0.50 and the return to the m12-24 average price at -0.73, the P/E percentile at -0.45 and -0.66, Ratio B at -0.29 and -0.47
  and the P/E at -0.24 and -0.36 (the dearer the entry by each read, the lower the return), and the adjusted gap at +0.40 and +0.53 (the
  higher, the better); the proxy composite at -0.07 and -0.10 and the entry price at +0.37 and +0.38 ran the wrong way (the later
  entries had more of the rise ahead of them).
- **The window caught up with the regime five years late.** Its median stayed at 12.0-12.7x through 2018, the multiple of the 2009-2013
  patent-cliff years, and rose to 23.3-27.1x in 2020-2021 once those years left; the class followed only as far as FAIR, as the market
  paid 20-45x the reported guide. The build's own sensitivity shows what the call rested on: a five-year window moves 72 classes (63 to
  CHEAP), and with it 68 of the 209 calls would have held instead of 5; every other tested encoding leaves at most 38 holding (the
  FY2019 total EPS) and most 3-13.
- **The 2014-2017 hypothesis, tested on the next four years (hindsight, not a rule):** that a ten-year own-history window describes the
  last regime. It held in its strongest form: the window read the stock RICH or FAIR on 207 of 209 dates while the entries returned
  +27.4% to +179.5% over two years and +100.3% to +337.9% over three, and the only CHEAP calls came when a market-wide sell-off took the
  price to the risen floor. Test it on other tickers whose earnings regime turned within the window (the PFE and BMY series in staging
  have their own), never fit it to LLY.

## Across 2014-2021

- **87 of 418 dates held** (CHEAP on 6 of 6, RICH on 81 of 373, FAIR on 0 of 39). Over the 418 dates the adjusted gap ranks the two-year
  return at Spearman +0.78 (m12-24 +0.78), the EPP gap at -0.65 and -0.74, Ratio B at -0.65 and -0.73, the P/E percentile at -0.60 and
  -0.67, the P/E at -0.32 and -0.42 and the proxy composite at +0.51 and +0.42 (all the right sign), and the entry price at +0.69 and
  +0.62 (wrong). Inside the regime that began with the 2014 launches the method's measures ordered the entries well; the level it judged
  them against was the previous regime's.

## Across 2008-2021

- **293 of 732 dates held** (CHEAP on 212 of 320, FAIR on 0 of 39, RICH on 81 of 373), where a CHEAP call on every date would have held
  on 542. Over the 732 dates the cheapness measures rank the two-year return weakly and mostly with the wrong sign (Spearman: the P/E
  percentile +0.14, Ratio B +0.12, the P/E +0.12, the EPP gap +0.06, the adjusted gap -0.05; the proxy composite +0.14, the only right
  sign; m12-24 within -0.16 to +0.21) and the entry price at +0.50 (+0.54): across three regimes the window-based reads describe the
  window's composition, while inside 2008-2009 (the P/E, the EPP gap and Ratio B), 2014-2017 and 2018-2021 most of them ranked the right
  way (2010-2013 is the exception, the re-rating running through it).
- **Profile drift:** the point-in-time profile (DURABLE, risk 2) against today's (DURABLE, risk 1, reviewed 2026-09-22) is a label only.

## Across 2022-2026

- **The call held on 25 of the 150 dates with a two-year outcome, all RICH** (2022: 0 of 52; 2023: 5 of 52; 2024: 20 of 46), where a
  CHEAP call on every date would have held on 124. The RICH entries' median two-year return was +83.1%; 124 cleared the hurdle and 106
  beat SPY. Over one year the call held on 70 of 202 (RICH 35 of 161, CHEAP 35 of 41). The robust dates (7 or 8 of 8) held 23 times in
  144, the fragile ones 2 in 6. Every tested encoding of the README leaves the two-year count at 25 or 26 and the one-year at 65-70: the
  calls rest on the same thing whatever the encoding.
- **Inside the three RICH years the dearness of the entry ranked the outcome, the window did not.** Over the 150 two-year dates the entry
  P/E ranks the two-year return at Spearman -0.80 (the m12-24 return -0.75), the entry price at -0.90 (-0.84) and the EPP gap at -0.72
  (-0.64), the right sign; the P/E percentile at -0.05 (+0.10) and Ratio B at -0.18 (-0.01) carry almost nothing, as the window read every
  date at the 57th-100th percentile; the adjusted gap at -0.59 (-0.70) and the proxy composite at -0.76 (-0.75) ran the wrong way (the
  strongest prints came at the dearest prices).
- **The earlier hypotheses, tested on the next five years (hindsight, not rules):** the 2014-2017 one, that a ten-year own-history window
  describes the last regime, held again in 2022-2023: a 27-31x median against 40-110x paid for the reported guide, RICH on all 104
  dates while the entries returned +20.9% to +229.1% over two years. In 2024 it weakened: the multiple paid stayed 57-71x while the stock
  slowed, and the RICH call held on 20 of 46. What turned the class to CHEAP in 2025 was the growth input, the company's own revenue guide
  of +29-41% in BASE, at a window median that had risen only to 34-35x; on one year that call held on 35 of 41.
- **A new one, for other tickers:** a GAAP guide that carries acquired IPR&D reads a buyer of pipeline dearest exactly when it buys most
  (FY23E $6.05 at 94-99x after the Q3 2023 charges; those entries returned +59.8% to +90.7%). The README's non-GAAP variant moves only 8
  classes here, because the window itself is GAAP; test the reading on the other pharmaceutical series (PFE, BMY), never fit it to LLY.

## Across 2008-2026

- **318 of 882 dates with a two-year outcome held** (CHEAP on 212 of 320, FAIR on 0 of 39, RICH on 106 of 523), where a CHEAP call on every
  date would have held on 666. Over the 882 dates the cheapness measures rank the two-year return with the wrong sign (Spearman: the P/E
  percentile +0.24, the P/E +0.24, Ratio B +0.26, the EPP gap +0.08, the adjusted gap -0.13; the proxy composite +0.05) and the entry
  price at +0.49: across four regimes the window-based reads describe the window's composition, while inside 2008-2009, 2014-2017,
  2018-2021 and 2022-2024 most of them ranked the right way.
- **Profile drift:** the point-in-time profile (DURABLE, risk 2) against today's (DURABLE, risk 1, "GLP-1 leader; priced for it", reviewed
  2026-09-22) is a label only.
