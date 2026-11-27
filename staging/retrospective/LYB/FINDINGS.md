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
