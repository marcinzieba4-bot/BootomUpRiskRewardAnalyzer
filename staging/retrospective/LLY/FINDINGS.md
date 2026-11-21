# LLY retrospective findings (hindsight)

Patterns seen in `outcome.json` for the LLY weekly dates: 314, 105 from 2008-01-04 to 2009-12-31 and 209 from 2010-01-08 to
2013-12-31, all Eli Lilly and Company (NYSE: LLY).
They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its
point-in-time build was committed and pushed (8d1f450, the empty-slot correction the firewall found 96e4c9f, firewall result 73b08d1);
the outcomes were computed on 2026-11-21. The 2010-2013 batch was scored only after its build, checks, README section and firewall
result were committed and pushed (5a27368, f8db0dc, 5446ffc), on 2026-11-21. Every date has its 6-month, 1-, 2- and 3-year horizons
(the last ends 2012-12-31 for 2008-2009 and 2016-12-30 for 2010-2013). Total returns
include the quarterly dividends ($0.425 to the ex-date of 2008-02-13, $0.47 from it, $0.49 from 2009-02-11, $0.50 from 2015-02-11 and $0.51 from 2016-02-10). No
split falls in any horizon, so every price is as traded. Medians of an even count take the upper middle value
(`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over three. "Call held" is `call_check_2y`: CHEAP should
clear the hurdle or beat the benchmark (SPY). Every date was CHEAP and BUY, so the tables test that one call against the calendar.

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
- **Profile drift:** the point-in-time profile (DURABLE, risk 2) against today's (DURABLE, risk 1, reviewed 2026-09-22) is a label only.
