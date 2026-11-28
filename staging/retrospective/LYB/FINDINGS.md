# LYB retrospective findings (hindsight)

Patterns seen in `outcome.json` for the 100 LYB weekly dates of 2012-02-10 to 2013-12-31: LyondellBasell Industries N.V. (NYSE: LYB),
from the first date after its first full year of GAAP EPS (FY2011). No 2008-2009 date exists (no LYB share before 2010-04-30;
retro/README.md, "LYB"). These are **labels and hypotheses**: never feed them back into the method or the fact sheet. The series was
scored only after its point-in-time build, validation outputs, README section and firewall result were committed and pushed
(05e46deac, f126013ec, 4ce63a65e, 614690649). Outcomes were computed on 2026-11-27: every date has its 6-month, 1-, 2- and 3-year
outcomes and the return to the average price over months 12-24. Total returns include the interim dividends and the $2.75 special dividend of
December 2012. Medians of an even count take the upper middle value
(`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years. "Call held" is `call_check_2y`: RICH should miss the hurdle and
lag the benchmark (SPY). Tables from `retro/generators/lyb/findings_tables.py 2012,2013`.

**Hindsight the model could not see:** the stock rose from $44.75 (2012-02-10) to $80.28 (2013-12-31) and to a 2014 high above $110
before the oil-price fall of late 2014; EPS rose from FY11's $4.32 (restated) and FY12's $4.96 to more than $6 in 2013 (the Q4 2013 release, 2014-01-31, after the range),
on U.S. ethane-based olefin margins and the share repurchases begun in May 2013. None of the later EPS, buybacks or prices is an input.

## 2012 (47 dates)
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2012-02-10 to 2012-12-28) | 47 | +123.4% | +40.0% to +185.6% | 47 | 46 | +75.9% | 0 |
| FY12E $3.74 (FY11's) (2012-02-10 to 2012-07-20) | 24 | +132.5% | +94.8% to +185.6% | 24 | 24 | +77.4% | 0 |
| FY12E $4.32 (FY11's) (2012-07-27 to 2012-12-28) | 23 | +100.9% | +40.0% to +156.9% | 23 | 22 | +75.9% | 0 |
| latest print Q4 2011 (2012-02-10 to 2012-04-27) | 12 | +117.5% | +94.8% to +131.3% | 12 | 12 | +68.3% | 0 |
| latest print Q1 2012 (2012-05-01 to 2012-07-20) | 12 | +166.7% | +132.5% to +185.6% | 12 | 12 | +101.9% | 0 |
| latest print Q2 2012 (2012-07-27 to 2012-10-19) | 13 | +138.5% | +78.1% to +156.9% | 13 | 13 | +78.9% | 0 |
| latest print Q3 2012 (2012-10-26 to 2012-12-28) | 10 | +85.2% | +40.0% to +97.2% | 10 | 9 | +75.0% | 0 |
## 2013 (53 dates)
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2013-01-04 to 2013-12-31) | 53 | +38.6% | +15.5% to +79.7% | 35 | 46 | +40.4% | 2 |
| FY12E $4.32 (FY11's) (2013-01-04 to 2013-01-25) | 4 | +37.4% | +35.1% to +45.1% | 4 | 0 | +53.8% | 0 |
| FY13E $4.96 (FY12's) (2013-02-01 to 2013-12-31) | 49 | +40.4% | +15.5% to +79.7% | 31 | 46 | +38.9% | 2 |
| latest print Q3 2012 (2013-01-04 to 2013-01-25) | 4 | +37.4% | +35.1% to +45.1% | 4 | 0 | +53.8% | 0 |
| latest print Q4 2012 (2013-02-01 to 2013-04-19) | 12 | +52.3% | +36.5% to +74.0% | 12 | 11 | +55.4% | 0 |
| latest print Q1 2013 (2013-04-26 to 2013-07-19) | 13 | +62.5% | +47.0% to +79.7% | 13 | 13 | +42.1% | 0 |
| latest print Q2 2013 (2013-07-26 to 2013-10-25) | 14 | +28.3% | +21.6% to +42.6% | 4 | 13 | +30.9% | 1 |
| latest print Q3 2013 (2013-10-30 to 2013-12-31) | 10 | +23.9% | +15.5% to +33.9% | 2 | 9 | +17.2% | 1 |

## Across the series

| Group | Dates | Mean 1-yr total return | Mean 2-yr total return | Mean 2-yr excess vs SPY | Mean 3-yr total return | Call held |
|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 100 | +49.5% | +80.4% | +43.5pp | +74.4% | 2 of 100 |

- **The RICH calls failed on 98 of 100 dates.** All 47 RICH dates of 2012 cleared the hurdle (median +123.4% over two years, 46 beat
  SPY) and 35 of the 53 of 2013 did (median +38.6%, 46 beat SPY). The two that held are 2013-08-23 and 2013-12-31, whose two years end in
  the late-2014 to 2015 oil-price fall. The median drawdown within two years was -38.4%; the two-year landing was XBULL on 84 dates,
  BULL on 3 and BEAR on 13 (outcome.json's `scenario_landing_2y`).
- **What drove RICH:** the P/E window holds only 2011-2013 days (2010 is two periods and excluded), on the last full year's EPS with no
  guide, so its median (8.8-10.3x) is the price of a company just out of bankruptcy; the stock re-rated and earnings grew, and the model
  read both as an expensive multiple. BASE took the latest quarter's revenue growth (negative for most of 2012-2013 as feedstock and
  product prices fell), which says little about a margin business; BULL took BASE's rate until a second year of EPS existed.
- **No tested encoding moved a class** (the sensitivity in retro/README.md, "LYB"), so the failure is the method's on a short history,
  not one call's. Hypothesis (to test on other new listings and post-reorganization stocks, never folded into this archive): a P/E window
  of one to three years after an emergence or listing, with no EPS guide, biases the class to RICH when earnings are rising. Any change
  is a new method version, decided before scoring and tested out of sample.
- **One stock, one recovery.** The dates span the years after the emergence from bankruptcy, the special dividends, the S&P 500
  inclusion and the start of the buybacks; the result tests the short-window and no-guide rules, not stock selection.

# LYB 2014-2017 (hindsight)

Patterns seen in `outcome.json` for the 209 LYB weekly dates of 2014-01-03 to 2017-12-29. Labels and hypotheses, never inputs. The
batch was scored only after its build, validation outputs, README section and firewall result were committed and pushed (3684b3b45,
b40f06552, ec8f640cf, d4b39433e); the 2012-2013 outcomes and findings above were not opened before then. Outcomes computed on
2026-11-27; every date has its 2-year horizon. Total returns include the interim dividends. Same conventions as above ("Call held" is
`call_check_2y`: RICH should miss the hurdle and lag SPY, CHEAP should clear it). Tables from
`retro/generators/lyb/findings_tables.py 2014,2015,2016,2017`.

**Hindsight the model could not see:** the share price peaked above $110 in mid-2014, fell with crude oil from late 2014 into 2016
(the LCM charges, revenue down by a third), recovered to about $110 by the end of 2017, and fell again in 2018-2019 as polyethylene
margins compressed with the new U.S. capacity; FY2017 EPS rose to about $12 on the U.S. tax reform benefit (released 2018-02-02, after
the range). None of it is an input.

## 2014 (52 dates)
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2014-01-03 to 2014-10-10) | 36 | -12.9% | -27.7% to +16.7% | 0 | 1 | -11.3% | 35 |
| class RICH, legacy tier ACCUMULATE (2014-01-31 to 2014-11-14) | 3 | -0.6% | -3.3% to +5.3% | 0 | 0 | -6.6% | 3 |
| class RICH, legacy tier WATCHLIST (2014-02-07 to 2014-11-21) | 8 | -3.0% | -6.4% to +4.8% | 0 | 0 | +3.8% | 8 |
| class RICH, legacy tier BUY (2014-11-28 to 2014-12-26) | 4 | +15.6% | +14.3% to +16.6% | 0 | 4 | +0.3% | 0 |
| class FAIR, legacy tier BUY (2014-12-12 to 2014-12-12) | 1 | +34.8% | +34.8% to +34.8% | 1 | 1 | +14.7% | 0 |
| FY13E $4.96 (FY12's) (2014-01-03 to 2014-01-24) | 4 | +9.9% | -1.8% to +16.7% | 0 | 1 | +16.3% | 3 |
| FY14E $6.76 (FY13's) (2014-01-31 to 2014-12-26) | 48 | -5.8% | -27.7% to +34.8% | 1 | 5 | -8.0% | 43 |
| latest print Q3 2013 (2014-01-03 to 2014-01-24) | 4 | +9.9% | -1.8% to +16.7% | 0 | 1 | +16.3% | 3 |
| latest print Q4 2013 (2014-01-31 to 2014-04-25) | 13 | +1.4% | -3.6% to +5.3% | 0 | 0 | +2.5% | 13 |
| latest print Q1 2014 (2014-04-30 to 2014-07-18) | 12 | -13.6% | -20.9% to -5.8% | 0 | 0 | -11.3% | 12 |
| latest print Q2 2014 (2014-07-25 to 2014-10-17) | 13 | -25.2% | -27.7% to -5.2% | 0 | 0 | -24.3% | 13 |
| latest print Q3 2014 (2014-10-24 to 2014-12-26) | 10 | +14.3% | -6.4% to +34.8% | 1 | 5 | -1.2% | 5 |
## 2015 (53 dates)
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier BUY (2015-01-02 to 2015-12-31) | 32 | +17.5% | +3.1% to +34.9% | 4 | 6 | -0.3% | 22 |
| class RICH, legacy tier ACCUMULATE (2015-04-17 to 2015-12-04) | 11 | +10.8% | -14.2% to +17.7% | 0 | 0 | -8.4% | 11 |
| class RICH, legacy tier WATCHLIST (2015-04-24 to 2015-07-02) | 10 | -15.2% | -16.7% to -8.5% | 0 | 0 | -19.5% | 10 |
| FY14E $6.76 (FY13's) (2015-01-02 to 2015-01-30) | 5 | +19.4% | +14.1% to +26.3% | 0 | 5 | +1.8% | 0 |
| FY15E $8.00 (FY14's) (2015-02-04 to 2015-12-31) | 48 | +10.9% | -16.7% to +34.9% | 4 | 1 | -5.2% | 43 |
| latest print Q3 2014 (2015-01-02 to 2015-01-30) | 5 | +19.4% | +14.1% to +26.3% | 0 | 5 | +1.8% | 0 |
| latest print Q4 2014 (2015-02-04 to 2015-04-17) | 11 | +10.2% | -4.8% to +17.5% | 0 | 1 | -4.6% | 10 |
| latest print Q1 2015 (2015-04-24 to 2015-07-24) | 14 | -14.5% | -16.7% to +3.9% | 0 | 0 | -17.5% | 14 |
| latest print Q2 2015 (2015-07-29 to 2015-10-16) | 12 | +17.1% | +3.0% to +23.9% | 0 | 0 | +0.1% | 12 |
| latest print Q3 2015 (2015-10-23 to 2015-12-31) | 11 | +20.9% | +11.9% to +34.9% | 4 | 0 | -3.6% | 7 |
## 2016 (52 dates)
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier BUY (2016-01-08 to 2016-12-30) | 46 | +39.4% | -1.3% to +66.1% | 28 | 24 | +24.3% | 18 |
| class CHEAP, legacy tier BUY (2016-02-03 to 2016-02-12) | 2 | +57.7% | +52.5% to +57.7% | 2 | 2 | +25.0% | 2 |
| class FAIR, legacy tier BUY (2016-02-19 to 2016-07-08) | 4 | +56.8% | +47.8% to +57.9% | 4 | 4 | +37.8% | 1 |
| FY15E $8.00 (FY14's) (2016-01-08 to 2016-01-29) | 4 | +63.9% | +52.0% to +66.1% | 4 | 4 | +20.5% | 0 |
| FY16E $9.60 (FY15's) (2016-02-03 to 2016-12-30) | 48 | +45.5% | -1.3% to +60.3% | 30 | 26 | +26.9% | 21 |
| latest print Q3 2015 (2016-01-08 to 2016-01-29) | 4 | +63.9% | +52.0% to +66.1% | 4 | 4 | +20.5% | 0 |
| latest print Q4 2015 (2016-02-03 to 2016-04-15) | 11 | +36.5% | +24.9% to +57.7% | 6 | 4 | +16.0% | 8 |
| latest print Q1 2016 (2016-04-22 to 2016-07-22) | 14 | +49.7% | +27.3% to +57.9% | 13 | 13 | +26.9% | 1 |
| latest print Q2 2016 (2016-07-29 to 2016-10-28) | 14 | +49.5% | +20.4% to +60.3% | 11 | 9 | +36.7% | 3 |
| latest print Q3 2016 (2016-11-02 to 2016-12-30) | 9 | +12.0% | -1.3% to +29.9% | 0 | 0 | +23.2% | 9 |
## 2017 (52 dates)
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier BUY (2017-01-06 to 2017-09-15) | 16 | +3.7% | -14.8% to +11.2% | 0 | 0 | +9.9% | 16 |
| class RICH, legacy tier ACCUMULATE (2017-02-03 to 2017-12-01) | 12 | -0.6% | -5.8% to +2.5% | 0 | 0 | -13.3% | 12 |
| class CHEAP, legacy tier BUY (2017-03-24 to 2017-08-18) | 19 | +9.4% | -6.0% to +17.8% | 0 | 0 | +15.7% | 0 |
| class RICH, legacy tier WATCHLIST (2017-11-03 to 2017-12-29) | 5 | -5.7% | -7.6% to -3.8% | 0 | 0 | -20.2% | 5 |
| FY16E $9.60 (FY15's) (2017-01-06 to 2017-01-27) | 4 | +5.0% | -1.6% to +6.9% | 0 | 0 | +16.6% | 4 |
| FY17E $9.15 (FY16's) (2017-02-03 to 2017-12-29) | 48 | +1.1% | -14.8% to +17.8% | 0 | 0 | +7.6% | 29 |
| latest print Q3 2016 (2017-01-06 to 2017-01-27) | 4 | +5.0% | -1.6% to +6.9% | 0 | 0 | +16.6% | 4 |
| latest print Q4 2016 (2017-02-03 to 2017-04-21) | 12 | +5.1% | +0.3% to +17.8% | 0 | 0 | +11.4% | 9 |
| latest print Q1 2017 (2017-04-28 to 2017-07-21) | 13 | +11.4% | +1.3% to +17.6% | 0 | 0 | +16.4% | 0 |
| latest print Q2 2017 (2017-07-28 to 2017-10-20) | 13 | -4.9% | -14.8% to +3.7% | 0 | 0 | -4.8% | 10 |
| latest print Q3 2017 (2017-10-27 to 2017-12-29) | 10 | -2.9% | -7.6% to +1.1% | 0 | 0 | -18.1% | 10 |

## Across 2014-2017

| Group | Dates | Mean 1-yr total return | Mean 2-yr total return | Mean 2-yr excess vs SPY | Mean 3-yr total return | Call held |
|---|---|---|---|---|---|---|
| class RICH | 183 | +4.6% | +9.9% | -13.1pp | +13.5% | 140 of 183 |
| class FAIR | 5 | +18.1% | +49.6% | +15.3pp | +36.4% | (no direction) |
| class CHEAP | 21 | +35.2% | +12.9% | -13.9pp | -7.1% | 2 of 21 |
| all | 209 | +8.0% | +11.2% | -12.5pp | +12.0% | 143 of 209 |

- **The RICH calls held on 140 of 183 dates,** after failing on 98 of 100 in 2012-2013. They held in 2014 on 46 of 51 RICH dates (the
  price peaked that summer and two years later sat lower, -12.9% median for the AVOID dates), in 2015 on 43 of 53 and in 2017 on all
  33; they failed in 2016 (18 of 46 held), whose two years caught the 2016-2018 recovery (median +39.4%).
- **The CHEAP calls failed on 19 of 21.** The two of February 2016 (P/E 7.9x, the 10th percentile, at the trough) cleared the hurdle
  (+52.5%, +57.7%); the 19 of March-August 2017 (P/E near the window median, BASE +14.6% to +30.0%/yr on the year-on-year revenue
  rebound) returned a median +9.4% and none beat SPY, as their two years ended in the 2018-2019 margin downturn. A revenue rebound read as
  EPS growth (BASE takes the latest quarter's revenue growth as reported, with no guide) is the cycle's peak signal for a margin
  business, not its trough signal: the mirror of 2015, when falling revenue made BASE -22% to -29%/yr and the class RICH near a bottom.
- **The two-year landing** was BEAR on 116 dates, BASE on 64 and BULL on 29 (none XBULL); the median drawdown within two years -32.8%.
- **What carried the classes** (from the sensitivity, a point-in-time result): the frozen rule-T signals (129 classes move at XBULL)
  and BASE's revenue rule. Hypothesis (to test on other cyclical tickers, never folded into this archive): for a commodity-margin
  business with no guide, BASE from the latest quarter's revenue growth is pro-cyclical, so RICH tends to hold after peaks and fail
  after troughs, and CHEAP appears late in recoveries. Any change is a new method version, decided before scoring and tested out of
  sample.
- **One stock, one oil cycle.** The dates span one crude-oil fall and recovery, the buyback that cut the diluted share count by more than a quarter (555M to 395M) and
  the 2017 peak; they test the no-guide and short-window rules on a cyclical, not stock selection.

# LYB 2018-2021 (hindsight)

Patterns seen in `outcome.json` for the 209 LYB weekly dates of 2018-01-05 to 2021-12-31. Labels and hypotheses, never inputs. The
batch was scored only after its build, validation outputs, README section and firewall result were committed and pushed (4e6e5fc48,
d6b18ea82, b3a08e3a6, 7361d9585); the 2012-2017 outcomes and findings above were not opened before then. Outcomes computed on
2026-11-27; every date has its 2-year horizon. Total returns include the interim dividends. Same conventions as above ("Call held" is
`call_check_2y`: RICH should miss the hurdle and lag SPY, CHEAP should clear it). Tables from
`retro/generators/lyb/findings_tables.py 2018,2019,2020,2021`.

**Hindsight the model could not see:** polyethylene and olefin margins compressed through 2018-2019 as new U.S. capacity started, and
the close fell from about $110 to about $70 by mid-2019; the pandemic took the close to $42 in March 2020, after which it more than doubled within
a year; 2021 brought record earnings (released 2022-01-28, after the range), and the price fell back in 2022. None of it is an input.

## 2018 (52 dates)
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2018-01-05 to 2018-01-26) | 4 | -16.5% | -23.4% to -12.8% | 0 | 0 | -26.6% | 4 |
| class CHEAP, legacy tier BUY (2018-02-02 to 2018-12-28) | 48 | -28.7% | -59.8% to +25.0% | 0 | 0 | -24.9% | 0 |
| FY17E $9.15 (FY16's) (2018-01-05 to 2018-01-26) | 4 | -16.5% | -23.4% to -12.8% | 0 | 0 | -26.6% | 4 |
| FY18E $12.28 (FY17's) (2018-02-02 to 2018-12-28) | 48 | -28.7% | -59.8% to +25.0% | 0 | 0 | -24.9% | 0 |
| latest print Q3 2017 (2018-01-05 to 2018-01-26) | 4 | -16.5% | -23.4% to -12.8% | 0 | 0 | -26.6% | 4 |
| latest print Q4 2017 (2018-02-02 to 2018-04-20) | 12 | -35.7% | -59.8% to -15.6% | 0 | 0 | -20.6% | 0 |
| latest print Q1 2018 (2018-04-27 to 2018-07-27) | 14 | -33.4% | -43.2% to -28.3% | 0 | 0 | -30.2% | 0 |
| latest print Q2 2018 (2018-08-03 to 2018-10-26) | 13 | -22.4% | -37.2% to -6.2% | 0 | 0 | -29.7% | 0 |
| latest print Q3 2018 (2018-10-31 to 2018-12-28) | 9 | +2.9% | -14.0% to +25.0% | 0 | 0 | -18.8% | 0 |
## 2019 (52 dates)
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2019-01-04 to 2019-09-06) | 24 | +34.5% | +7.0% to +63.0% | 16 | 4 | -8.8% | 16 |
| class FAIR, legacy tier BUY (2019-04-05 to 2019-07-26) | 3 | +25.4% | +23.7% to +26.3% | 0 | 0 | -13.3% | 0 |
| class RICH, legacy tier BUY (2019-04-12 to 2019-12-27) | 25 | +18.0% | +1.7% to +35.3% | 2 | 0 | +6.0% | 23 |
| FY18E $12.28 (FY17's) (2019-01-04 to 2019-01-25) | 4 | +17.5% | +12.6% to +22.5% | 0 | 0 | -17.5% | 0 |
| FY19E $12.01 (FY18's) (2019-02-01 to 2019-02-15) | 3 | +19.2% | +7.0% to +22.8% | 0 | 0 | -18.4% | 0 |
| FY19E $12.03 (FY18's) (2019-02-22 to 2019-12-27) | 45 | +27.9% | +1.7% to +63.0% | 18 | 4 | +6.0% | 39 |
| latest print Q3 2018 (2019-01-04 to 2019-01-25) | 4 | +17.5% | +12.6% to +22.5% | 0 | 0 | -17.5% | 0 |
| latest print Q4 2018 (2019-02-01 to 2019-04-18) | 12 | +26.3% | +7.0% to +34.5% | 5 | 0 | -14.7% | 6 |
| latest print Q1 2019 (2019-04-26 to 2019-07-26) | 14 | +33.6% | +17.3% to +63.0% | 7 | 4 | +4.9% | 11 |
| latest print Q2 2019 (2019-08-02 to 2019-10-25) | 13 | +24.2% | +11.5% to +57.2% | 6 | 0 | +13.8% | 13 |
| latest print Q3 2019 (2019-11-01 to 2019-12-27) | 9 | +5.7% | +1.7% to +9.9% | 0 | 0 | +6.1% | 9 |
## 2020 (53 dates)
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier BUY (2020-01-03 to 2020-11-06) | 25 | +47.2% | +11.2% to +97.3% | 18 | 19 | +40.7% | 4 |
| class RICH, legacy tier ACCUMULATE (2020-01-31 to 2020-11-13) | 7 | +25.3% | +15.6% to +34.7% | 3 | 5 | +22.4% | 1 |
| class RICH, legacy tier WATCHLIST (2020-02-07 to 2020-12-11) | 6 | +30.8% | +8.2% to +31.7% | 0 | 2 | +20.9% | 4 |
| class CHEAP, legacy tier BUY (2020-03-13 to 2020-05-15) | 10 | +130.5% | +87.1% to +164.6% | 10 | 10 | +99.1% | 10 |
| class FAIR, legacy tier BUY (2020-05-22 to 2020-05-22) | 1 | +93.0% | +93.0% to +93.0% | 1 | 1 | +64.7% | 0 |
| class RICH, legacy tier AVOID (2020-12-04 to 2020-12-31) | 4 | +7.6% | +4.4% to +11.2% | 0 | 2 | +2.2% | 2 |
| FY19E $12.03 (FY18's) (2020-01-03 to 2020-01-24) | 4 | +20.1% | +11.2% to +21.1% | 0 | 0 | +11.4% | 4 |
| FY20E $9.58 (FY19's) (2020-01-31 to 2020-02-14) | 3 | +31.7% | +31.7% to +34.5% | 1 | 0 | +21.9% | 2 |
| FY20E $9.60 (FY19's) (2020-02-21 to 2020-12-31) | 46 | +48.3% | +4.4% to +164.6% | 31 | 39 | +41.8% | 15 |
| latest print Q3 2019 (2020-01-03 to 2020-01-24) | 4 | +20.1% | +11.2% to +21.1% | 0 | 0 | +11.4% | 4 |
| latest print Q4 2019 (2020-01-31 to 2020-04-24) | 13 | +87.1% | +30.8% to +164.6% | 10 | 7 | +69.0% | 10 |
| latest print Q1 2020 (2020-05-01 to 2020-07-24) | 13 | +63.0% | +44.2% to +115.4% | 13 | 13 | +51.2% | 3 |
| latest print Q2 2020 (2020-07-31 to 2020-10-23) | 13 | +31.8% | +15.6% to +65.0% | 6 | 12 | +33.7% | 1 |
| latest print Q3 2020 (2020-10-30 to 2020-12-31) | 10 | +15.1% | +4.4% to +34.7% | 3 | 7 | +5.9% | 3 |
## 2021 (52 dates)
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2021-01-08 to 2021-07-23) | 29 | +3.5% | -10.1% to +28.1% | 0 | 14 | -13.8% | 15 |
| class FAIR, legacy tier ACCUMULATE (2021-07-30 to 2021-12-17) | 9 | +10.9% | +7.5% to +26.3% | 0 | 9 | -9.8% | 7 |
| class FAIR, legacy tier BUY (2021-09-03 to 2021-10-22) | 6 | +20.9% | +9.6% to +24.5% | 0 | 6 | -3.8% | 2 |
| class RICH, legacy tier ACCUMULATE (2021-10-29 to 2021-12-31) | 8 | +19.5% | +13.3% to +25.2% | 0 | 8 | +3.1% | 0 |
| FY20E $9.60 (FY19's) (2021-01-08 to 2021-01-22) | 3 | +13.9% | +7.9% to +16.6% | 0 | 3 | -2.9% | 0 |
| FY21E $4.24 (FY20's) (2021-01-29 to 2021-02-19) | 4 | +20.6% | +11.4% to +28.1% | 0 | 4 | -1.4% | 0 |
| FY21E $4.25 (FY20's) (2021-02-26 to 2021-12-31) | 45 | +8.3% | -10.1% to +26.3% | 0 | 30 | -11.2% | 24 |
| latest print Q3 2020 (2021-01-08 to 2021-01-22) | 3 | +13.9% | +7.9% to +16.6% | 0 | 3 | -2.9% | 0 |
| latest print Q4 2020 (2021-01-29 to 2021-04-23) | 13 | +3.7% | -7.1% to +28.1% | 0 | 8 | -13.6% | 5 |
| latest print Q1 2021 (2021-04-30 to 2021-07-23) | 13 | +1.0% | -10.1% to +10.1% | 0 | 3 | -15.4% | 10 |
| latest print Q2 2021 (2021-07-30 to 2021-10-22) | 13 | +13.7% | +7.5% to +24.5% | 0 | 13 | -7.2% | 9 |
| latest print Q3 2021 (2021-10-29 to 2021-12-31) | 10 | +21.8% | +13.3% to +26.3% | 0 | 10 | +3.2% | 0 |

## Across 2018-2021

| Group | Dates | Mean 1-yr total return | Mean 2-yr total return | Mean 2-yr excess vs SPY | Mean 3-yr total return | Call held |
|---|---|---|---|---|---|---|
| class RICH | 108 | +10.7% | +19.7% | -3.8pp | +27.5% | 53 of 108 |
| class FAIR | 19 | -3.6% | +21.1% | +10.1pp | +22.1% | (no direction) |
| class CHEAP | 82 | +4.7% | +11.5% | -23.4pp | +30.7% | 26 of 82 |
| all | 209 | +7.1% | +16.6% | -10.2pp | +28.2% | 88 of 209 |

- **The CHEAP calls failed on all 48 dates of 2018 and held on 26 of 34 after.** The 2018 dates rested on FY17's $12.28, a year lifted
  by the U.S. tax reform benefit and near the margin peak, with BASE at +21% to +27%/yr on revenue growth; their two years caught the
  2018-2019 margin downturn and the 2020 crash (median -28.7%, none beat SPY, drawdowns to -70.6%). The CHEAP dates of 2019 (P/E 5.7-7.4x)
  cleared the hurdle on 16 of 24 and the ten of March-May 2020 (P/E 4.4-6.1x, at the trough) on all ten (median +130.5%).
- **The RICH calls held on 53 of 108.** They held in early 2018 (4 of 4) and through late 2019 (23 of 25), and failed through most of
  2020 (11 of 42 held): the RICH class there came from BASE's negative revenue growth while the P/E sat below the window median, and the
  two years ran into the 2020-2021 recovery (median +47.2% for the BUY-tier RICH dates). In 2021, on FY20's $4.25 anchor (20-27x), 15 of
  the 37 RICH dates held; the median 2-yr return was +3.5% for the AVOID dates, and none cleared the hurdle.
- **The two-year landing** was BASE on 86 dates, BEAR on 68, BULL on 40 and XBULL on 15; the median drawdown within two years -49.7%.
- **What carried the classes** (from the sensitivity, a point-in-time result): the frozen rule-T signals (71 classes at XBULL), the GAAP
  anchor of an unusual year (FY2017 with the tax reform benefit: 45 classes at a derived $10.23; FY2020 with the impairment: 8 at
  $5.61) and BASE's revenue rule. Hypothesis (to test on other cyclical tickers, never folded into this archive): the last full year's
  GAAP EPS of a one-off-heavy or trough year, used as the current year's with no guide, carries that year's distortion into the class in
  both directions; together with the pro-cyclical BASE seen in 2014-2017, it makes CHEAP late at peaks (2018) and RICH late at troughs
  (2020). Any change is a new method version, decided before scoring and tested out of sample.
- **One stock, one cycle and one shock.** The dates span one margin downturn, one pandemic crash and its recovery, a large acquisition
  (A. Schulman) and continued buybacks (395M to 334M diluted shares); they test the no-guide and GAAP-anchor rules on a cyclical, not
  stock selection.


# LYB 2022-2026 (hindsight)

Patterns seen in `outcome.json` for the 255 LYB weekly dates of 2022-01-07 to 2026-11-20. Labels and hypotheses, never inputs. The
batch was scored only after its build, validation outputs, README section and firewall result were committed and pushed (ce5441085,
85e10305d); the 2012-2021 outcomes and findings above were not opened before then. Outcomes computed on 2026-11-28: 151 dates (to
2024-11-22) have their 2-year horizon, 203 a 1-year one and 99 a 3-year one; the 2025-2026 dates have no 2-year outcome yet. Total
returns include the interim and special dividends. Same conventions as above ("Call held" is `call_check_2y`: RICH should miss the
hurdle and lag SPY, CHEAP should clear it). Tables from `retro/generators/lyb/findings_tables.py 2022,2023,2024,2025,2026`.

**Hindsight the model could not see:** FY2021's record earnings were a peak; polyolefin margins fell through 2022-2025 as demand
weakened and capacity grew, with impairments, the refinery exit and the European asset sale along the way, and the close fell from about
$100 in early 2022 to the $40s-$50s by 2025, with the dividend halved in February 2026; the S&P 500 rose strongly over the same years.
None of it is an input.

## 2022 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier ACCUMULATE (2022-01-07 to 2022-01-21) | 2 | +15.0% | +14.4% to +15.0% | 0 | 2 | -0.4% | 0 |
| class RICH, legacy tier WATCHLIST (2022-01-14 to 2022-01-14) | 1 | +6.3% | +6.3% to +6.3% | 0 | 1 | -8.8% | 0 |
| class CHEAP, legacy tier BUY (2022-01-28 to 2022-12-30) | 49 | +13.3% | -3.1% to +41.8% | 6 | 1 | +8.4% | 7 |
| FY21E $4.25 (FY20's) (2022-01-07 to 2022-01-21) | 3 | +14.4% | +6.3% to +15.0% | 0 | 3 | -4.0% | 0 |
| FY22E $16.75 (FY21's) (2022-01-28 to 2022-02-18) | 4 | +12.7% | +7.5% to +14.8% | 0 | 1 | -6.3% | 1 |
| FY22E $16.77 (FY21's) (2022-02-25 to 2022-12-30) | 45 | +14.4% | -3.1% to +41.8% | 6 | 0 | +10.1% | 6 |
| latest print Q3 2021 (2022-01-07 to 2022-01-21) | 3 | +14.4% | +6.3% to +15.0% | 0 | 3 | -4.0% | 0 |
| latest print Q4 2021 (2022-01-28 to 2022-04-22) | 13 | +12.1% | +7.2% to +20.1% | 0 | 1 | -8.0% | 1 |
| latest print Q1 2022 (2022-04-29 to 2022-07-22) | 13 | +10.0% | -3.1% to +24.6% | 0 | 0 | -6.2% | 0 |
| latest print Q2 2022 (2022-07-29 to 2022-10-21) | 13 | +24.6% | +14.4% to +41.8% | 6 | 0 | +17.5% | 6 |
| latest print Q3 2022 (2022-10-28 to 2022-12-30) | 10 | +7.4% | +0.4% to +25.4% | 0 | 0 | +15.2% | 0 |

Three years (52 dates with one): 0 of 52 cleared, 0 beat SPY; range -33.9% to +3.9%

## 2023 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2023-01-06 to 2023-01-27) | 4 | -6.7% | -8.9% to -5.2% | 0 | 0 | +0.9% | 0 |
| class RICH, legacy tier AVOID (2023-02-03 to 2023-12-29) | 37 | -34.4% | -44.3% to -9.5% | 0 | 0 | -25.0% | 37 |
| class FAIR, legacy tier WATCHLIST (2023-03-10 to 2023-03-24) | 3 | -2.3% | -4.9% to +1.0% | 0 | 0 | +3.2% | 0 |
| class RICH, legacy tier WATCHLIST (2023-05-12 to 2023-07-14) | 8 | -22.5% | -27.8% to -19.2% | 0 | 0 | -9.4% | 8 |
| FY22E $16.77 (FY21's) (2023-01-06 to 2023-01-27) | 4 | -6.7% | -8.9% to -5.2% | 0 | 0 | +0.9% | 0 |
| FY23E $11.81 (FY22's) (2023-02-03 to 2023-02-17) | 3 | -11.9% | -13.5% to -10.7% | 0 | 0 | -5.8% | 3 |
| FY23E $11.83 (FY22's) (2023-02-24 to 2023-12-29) | 45 | -29.9% | -44.3% to +1.0% | 0 | 0 | -21.3% | 42 |
| latest print Q3 2022 (2023-01-06 to 2023-01-27) | 4 | -6.7% | -8.9% to -5.2% | 0 | 0 | +0.9% | 0 |
| latest print Q4 2022 (2023-02-03 to 2023-04-21) | 12 | -11.9% | -30.0% to +1.0% | 0 | 0 | -5.7% | 9 |
| latest print Q1 2023 (2023-04-28 to 2023-07-28) | 14 | -23.2% | -28.0% to -19.2% | 0 | 0 | -9.7% | 14 |
| latest print Q2 2023 (2023-08-04 to 2023-10-20) | 12 | -35.0% | -40.7% to -29.9% | 0 | 0 | -26.7% | 12 |
| latest print Q3 2023 (2023-10-27 to 2023-12-29) | 10 | -42.8% | -44.3% to -34.0% | 0 | 0 | -34.6% | 10 |

Three years (47 dates with one): 0 of 52 cleared, 0 beat SPY; range -31.4% to +5.3%

## 2024 (47 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2024-01-05 to 2024-11-22) | 47 | -24.1% | -41.9% to -10.5% | 0 | 0 | -40.3% | 47 |
| FY23E $11.83 (FY22's) (2024-01-05 to 2024-01-26) | 4 | -35.5% | -41.9% to -34.0% | 0 | 0 | -38.7% | 4 |
| FY24E $6.46 (FY23's) (2024-02-02 to 2024-02-16) | 3 | -30.6% | -34.3% to -30.1% | 0 | 0 | -41.4% | 3 |
| FY24E $6.48 (FY23's) (2024-02-23 to 2024-11-22) | 40 | -22.6% | -32.8% to -10.5% | 0 | 0 | -40.8% | 40 |
| latest print Q3 2023 (2024-01-05 to 2024-01-26) | 4 | -35.5% | -41.9% to -34.0% | 0 | 0 | -38.7% | 4 |
| latest print Q4 2023 (2024-02-02 to 2024-04-19) | 12 | -21.9% | -34.3% to -11.4% | 0 | 0 | -44.9% | 12 |
| latest print Q1 2024 (2024-04-26 to 2024-07-26) | 14 | -22.7% | -32.8% to -14.1% | 0 | 0 | -41.2% | 14 |
| latest print Q2 2024 (2024-08-02 to 2024-10-25) | 13 | -24.5% | -30.5% to -13.9% | 0 | 0 | -39.3% | 13 |
| latest print Q3 2024 (2024-11-01 to 2024-11-22) | 4 | -11.3% | -22.9% to -10.5% | 0 | 0 | -27.1% | 4 |

Three years:: none yet

## Across 2022-2026 (dates with each horizon)

| Group | Dates | Mean 1-yr total return | Mean 2-yr total return | Mean 2-yr excess vs SPY | Mean 3-yr total return | Call held |
|---|---|---|---|---|---|---|
| class RICH | 193 (147 with 1 yr, 95 with 2, 43 with 3) | -5.0% | -25.8% | -67.6pp | -15.7% | 92 of 95 |
| class FAIR | 7 (3, 3, 3) | +21.1% | -2.1% | -50.7pp | -0.6% | (no direction) |
| class CHEAP | 55 (53, 53, 53) | +10.4% | +13.8% | -26.3pp | -19.7% | 7 of 53 |
| all | 255 (203, 151, 99) | -0.6% | -11.4% | -52.8pp | -17.4% | 99 of 151 |

- **The CHEAP calls of 2022 mostly failed the hurdle.** All 53 rested on FY21's record $16.75-$16.77 (4.4-7.0x against a 9x median):
  the median 2-yr total return was +13.3% for the 49 of 2022 with special and interim dividends (2-yr hurdle +32.2%), 6 cleared it (all
  in the weeks after the Q2 2022 print, when the close was lowest; `call_check_2y` counts 7 as held) and 1 beat SPY; the 4 CHEAP
  dates of January 2023 lost 5.2% to 8.9%; the 3-yr returns turned negative (-33.9% to +3.9%).
  The anchor was a peak year: a P/E on the last full year's GAAP EPS at a cyclical peak read as cheap, as with FY2017 in 2018.
- **The RICH calls held on 92 of 95.** From the Q4 2022 print on, with BASE negative on falling revenues (2023) and then a P/E of 11-19x
  on FY23's $6.48 and FY24's $4.14 (2024), the two years ran into the downturn: median 2-yr -34.4% for the AVOID dates of 2023, -24.1% for
  those of 2024, none cleared the hurdle or beat SPY. The 3 that did not hold were January 2022 (FY20's $4.25 anchor, RICH just before
  the record year printed; +6.3% to +15.0%, all beating SPY in a falling market).
- **The two-year landing** was BASE on 78 dates, BEAR on 67, BULL on 6; the median drawdown within two years -49.7%.
- **What carried the classes** (from the sensitivity, a point-in-time result): the last full year's GAAP EPS (the adjusted EPS moves 26
  classes, mostly RICH to FAIR in 2023-2026), the frozen rule-T signals (26 at XBULL) and BASE's revenue rule. The hypothesis from 2018-2021
  (the last full year's GAAP EPS, used as the current year's with no guide, makes CHEAP late at peaks and RICH late at troughs) is
  consistent with 2022's CHEAP calls; the RICH calls of 2023-2024 held because the downturn continued, so they do not test the trough side.
  Any change is a new method version, decided before scoring and tested out of sample.
- **One stock, one cycle.** The dates span one peak and one long downturn, a refinery exit, a dividend cut and continued but smaller
  buybacks (334M to 322M diluted shares); they test the no-guide and GAAP-anchor rules on a cyclical, not stock selection.
