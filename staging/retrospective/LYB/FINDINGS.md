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
