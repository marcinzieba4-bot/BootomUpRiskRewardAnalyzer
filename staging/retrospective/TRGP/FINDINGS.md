# TRGP retrospective findings (hindsight)

Patterns seen in `outcome.json` for the 98 TRGP weekly dates of 2012-02-24 to 2013-12-31: Targa Resources Corp. (NYSE: TRGP), from the
first date after its first full year of GAAP EPS (FY2011). No 2008-2009 date exists (no TRGP share before the 2010-12-07 listing, no EPS
to common shareholders in 2008-2009; retro/README.md, "TRGP 2008-2009"), and none from the listing to 2012-02-17 (2010 a loss per share).
These are **labels and hypotheses**: never feed them back into the method or the fact sheet, and never into another ticker's models.
The series was scored only after its point-in-time build, validation outputs, README section and firewall result were committed and
pushed (f98b785c3, 3b25b1d13, eac635e42, ab4967640, ab02af9ac). Outcomes were computed on 2026-11-28: every date has its 6-month, 1-, 2-
and 3-year outcomes and the return to the average price over months 12-24. Total returns include the quarterly dividends. Medians of an
even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years. "Call held" is
`call_check_2y`: RICH should miss the hurdle and lag the benchmark (SPY), CHEAP clear it. Tables from
`retro/generators/trgp/findings_tables.py 2012,2013`.

**Hindsight the model could not see:** the stock rose from $45.95 (2012-02-24) to $88.17 (2013-12-31) and to a close of $150.62 on 2014-06-19,
then fell with the oil and NGL prices of late 2014 to $15.43 on 2016-02-11 (the two-year windows of the late-2013 dates end in that fall).
TRC's dividends paid rose from $2.06 in 2013 to $2.68 in 2014 and $3.39 in 2015 as the Partnership's incentive distribution rights paid out. None of the later prices,
dividends or events is an input.
## 2012 (45 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier WATCHLIST (2012-02-24 to 2012-03-23) | 5 | +127.0% | +117.7% to +128.1% | 5 | 5 | +67.5% | 0 |
| class FAIR, legacy tier ACCUMULATE (2012-03-30 to 2012-04-27) | 4 | +134.6% | +122.9% to +138.6% | 4 | 4 | +68.9% | 0 |
| class CHEAP, legacy tier ACCUMULATE (2012-04-13 to 2012-04-13) | 1 | +140.8% | +140.8% to +140.8% | 1 | 1 | +73.6% | 1 |
| class RICH, legacy tier AVOID (2012-05-04 to 2012-12-28) | 35 | +180.7% | +100.7% to +245.5% | 35 | 35 | +115.4% | 0 |
| FY12E $0.74 (FY11's) (2012-02-24 to 2012-12-28) | 45 | +161.5% | +100.7% to +245.5% | 45 | 45 | +110.1% | 1 |
| latest print Q4 2011 (2012-02-24 to 2012-04-27) | 10 | +128.1% | +117.7% to +140.8% | 10 | 10 | +68.5% | 1 |
| latest print Q1 2012 (2012-05-04 to 2012-08-03) | 14 | +204.2% | +128.8% to +245.5% | 14 | 14 | +103.1% | 0 |
| latest print Q2 2012 (2012-08-07 to 2012-10-26) | 12 | +192.6% | +152.0% to +221.8% | 12 | 12 | +116.6% | 0 |
| latest print Q3 2012 (2012-11-02 to 2012-12-28) | 9 | +137.3% | +100.7% to +167.9% | 9 | 9 | +128.0% | 0 |

## 2013 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2013-01-04 to 2013-12-31) | 52 | +38.6% | -63.6% to +102.0% | 30 | 30 | +65.3% | 22 |
| class RICH, legacy tier WATCHLIST (2013-06-21 to 2013-06-21) | 1 | +53.7% | +53.7% to +53.7% | 1 | 1 | +82.5% | 0 |
| FY12E $0.74 (FY11's) (2013-01-04 to 2013-02-08) | 6 | +63.3% | +51.5% to +102.0% | 6 | 6 | +95.9% | 0 |
| FY13E $0.91 (FY12's) (2013-02-15 to 2013-12-31) | 47 | +35.8% | -63.6% to +71.4% | 25 | 25 | +57.8% | 22 |
| latest print Q3 2012 (2013-01-04 to 2013-02-08) | 6 | +63.3% | +51.5% to +102.0% | 6 | 6 | +95.9% | 0 |
| latest print Q4 2012 (2013-02-15 to 2013-04-26) | 11 | +57.7% | +46.3% to +71.4% | 11 | 11 | +77.0% | 0 |
| latest print Q1 2013 (2013-05-03 to 2013-07-26) | 13 | +50.1% | +33.0% to +64.1% | 13 | 13 | +70.9% | 0 |
| latest print Q2 2013 (2013-08-02 to 2013-11-01) | 14 | -5.1% | -18.8% to +36.3% | 1 | 1 | +40.2% | 13 |
| latest print Q3 2013 (2013-11-06 to 2013-12-31) | 9 | -54.6% | -63.6% to -28.8% | 0 | 0 | +2.5% | 9 |

## Across the series

| Group | Dates | Mean 1-yr total return | Mean 2-yr total return | Mean 2-yr excess vs SPY | Mean 3-yr total return | Call held |
|---|---|---|---|---|---|---|
| class RICH | 88 | +65.9% | +84.4% | +47.6pp | +6.8% | 22 of 88 |
| class FAIR | 9 | +44.7% | +128.0% | +89.4pp | +128.3% | (no direction) |
| class CHEAP | 1 | +54.9% | +140.8% | +103.6pp | +135.9% | 1 of 1 |

- **The RICH calls failed on the two-year horizon for 2012 and early 2013.** All 35 RICH dates of 2012 cleared the hurdle (median
  +180.7% over two years, all beat SPY), and so did the 30 of 2013 to the Q1 2013 print's dates. The 22 that held are 2013-08-09 to
  2013-12-31 (the Q2 and Q3 2013 prints' dates), whose two years end in the 2015 oil and NGL price fall; on three years none of the 53
  dates of 2013 cleared the hurdle (range -60.4% to -17.0%), and the median drawdown within two years of a RICH date was -43.3%.
- **The FAIR and CHEAP dates (the Q4 2011 print's, 2012-02-24 to 2012-04-27) did best** (+117.7% to +140.8% over two years): the one
  date where BASE read the strong Q4 2011 revenue growth. That is one quarter's reading, not a tested edge.
- **What drove RICH:** the window holds only 2011-2013 days on two GAAP anchors ($0.74, $0.91), and the GAAP EPS of a general partner's
  holding company is small against the cash it pays (the Partnership's other unitholders take most consolidated earnings; the dividend
  was 1.8-2.5 times EPS). Price, multiple and dividends rose with the incentive distribution rights, which a P/E on GAAP EPS reads as an
  expensive multiple; BASE took revenue growth, negative through most of 2012-2013 as NGL prices fell while segment margins grew.
- **The sensitivity** (retro/README.md, "TRGP") moved at most 10 classes per call; the RICH calls rest on the window, not one encoding.
  Hypothesis (to test on other general partner holding companies and on later TRGP dates, never folded into this archive): for a company
  whose earnings are mostly the noncontrolling interests', a GAAP P/E on a short window says more about the payout structure than about
  value; a dividend-based or distribution-based yardstick would be a new method version, decided before scoring and tested out of sample.
- **One stock, one cycle.** The dates span TRGP's first two listed years, the NGL price fall of 2012 and the build-up to the 2014 peak;
  the result tests the short-window and no-guide rules, not stock selection.
