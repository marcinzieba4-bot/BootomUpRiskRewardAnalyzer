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

## TRGP 2014-2017 (HINDSIGHT: labels, never inputs)

Written on 2026-11-28 after the 209 models of 2014-01-03 to 2017-12-29 were built, validated, firewalled and committed
(retro/README.md, "TRGP 2014-2017"). Nothing here entered a model; no rule was changed because of it. Tables from
`python3 retro/generators/trgp/findings_tables.py 2014,2015,2016,2017`.

**By class, 2-year total return:** RICH 61 dates, median -15.8% (8 cleared the 15%/yr hurdle, 5 beat SPY, the call held on 53);
CHEAP 107, median -28.9% (21 cleared, 21 beat SPY, held on 21); FAIR 41, median +3.3% (10 cleared, 5 beat SPY, held on 18).
Scenario landing at two years: BEAR 83, BASE 115, BULL 11.

What the labels suggest (hypotheses only):
- **The CHEAP calls of 2014-2015 failed on the commodity collapse.** Every 2014 date lost 35-77% over two years whatever its class,
  and the CHEAP and BUY run of 2015 (53 of 53) lost a median 29%; the class rested on a P/E far below a window median of 44-51x built
  on 2011-2014 earnings (FY14's $2.43 against a close falling from $107 to $16), and on BASE's revenue growth, which measured 2014's
  NGL prices, not the cash flows that later fell. The CHEAP dates that worked were the last ones: from the Q3 2015 print (late 2015)
  to 2016-04-15, +61% to +245% over two years.
- **The RICH calls of late 2016 and 2017 held** (2017: median -15.6%, held on all 18 RICH and AVOID dates), and FAIR's 2017 dates were
  flat; the 2016 RICH and WATCHLIST dates still returned +27% to +46% from the 2016 low.
- **FY2015 kept at GAAP $1.09** is what made 2016-2017 RICH or FAIR (75 classes move if it is excluded, nearly all to CHEAP): with
  hindsight the CHEAP alternative would have been right for 2016 and wrong for 2017. This is the call to review first, not to change.
- The frozen 2012 signal thresholds read the 2015 collapse as BEAR on most signals, yet the class stayed CHEAP on valuation alone:
  the valuation factor dominated the signals throughout.


## 2014 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2014-01-03 to 2014-10-03) | 14 | -63.5% | -73.8% to -59.7% | 0 | 0 | -71.1% | 14 |
| class CHEAP, legacy tier BUY (2014-02-14 to 2014-12-26) | 25 | -58.5% | -76.5% to -34.7% | 0 | 0 | -51.8% | 0 |
| class FAIR, legacy tier ACCUMULATE (2014-06-20 to 2014-07-18) | 5 | -64.8% | -66.9% to -64.0% | 0 | 0 | -68.3% | 0 |
| class FAIR, legacy tier BUY (2014-07-25 to 2014-11-21) | 2 | -51.0% | -66.4% to -51.0% | 0 | 0 | -68.2% | 0 |
| class RICH, legacy tier WATCHLIST (2014-08-01 to 2014-10-31) | 4 | -59.7% | -66.2% to -57.5% | 0 | 0 | -69.2% | 4 |
| class RICH, legacy tier ACCUMULATE (2014-10-10 to 2014-10-17) | 2 | -53.5% | -56.6% to -53.5% | 0 | 0 | -69.2% | 2 |
| FY13E $0.91 (FY12's) (2014-01-03 to 2014-02-07) | 6 | -68.1% | -73.8% to -61.8% | 0 | 0 | -16.1% | 6 |
| FY14E $1.55 (FY13's) (2014-02-14 to 2014-12-26) | 46 | -61.1% | -76.5% to -34.7% | 0 | 0 | -66.1% | 14 |
| latest print Q3 2013 (2014-01-03 to 2014-02-07) | 6 | -68.1% | -73.8% to -61.8% | 0 | 0 | -16.1% | 6 |
| latest print Q4 2013 (2014-02-14 to 2014-04-25) | 11 | -64.7% | -76.5% to -59.0% | 0 | 0 | -37.2% | 0 |
| latest print Q1 2014 (2014-05-02 to 2014-07-25) | 13 | -61.1% | -66.9% to -55.5% | 0 | 0 | -60.0% | 0 |
| latest print Q2 2014 (2014-08-01 to 2014-10-31) | 14 | -60.8% | -66.2% to -53.5% | 0 | 0 | -71.4% | 14 |
| latest print Q3 2014 (2014-11-05 to 2014-12-26) | 8 | -44.2% | -56.3% to -34.7% | 0 | 0 | -65.4% | 0 |
3y (52 dates with one): 0 of 52 cleared, 0 beat SPY; range -62.6% to -21.4%
1y range -71.7 26.7 excess 2y -83.3 -50.0
drawdown -89.8 -82.9

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2015-01-02 to 2015-12-31) | 53 | -29.3% | -44.8% to +111.0% | 5 | 5 | -42.4% | 5 |
| FY14E $1.55 (FY13's) (2015-01-02 to 2015-02-06) | 6 | -27.4% | -41.1% to -25.9% | 0 | 0 | -54.5% | 0 |
| FY15E $2.43 (FY14's) (2015-02-13 to 2015-12-31) | 47 | -29.4% | -44.8% to +111.0% | 5 | 5 | -42.2% | 5 |
| latest print Q3 2014 (2015-01-02 to 2015-02-06) | 6 | -27.4% | -41.1% to -25.9% | 0 | 0 | -54.5% | 0 |
| latest print Q4 2014 (2015-02-13 to 2015-05-01) | 12 | -32.6% | -40.7% to -28.5% | 0 | 0 | -52.7% | 0 |
| latest print Q1 2015 (2015-05-06 to 2015-07-31) | 13 | -41.1% | -44.8% to -38.0% | 0 | 0 | -43.5% | 0 |
| latest print Q2 2015 (2015-08-05 to 2015-10-30) | 13 | -14.7% | -32.5% to +3.0% | 0 | 0 | -17.6% | 0 |
| latest print Q3 2015 (2015-11-04 to 2015-12-31) | 9 | +72.3% | +2.1% to +111.0% | 5 | 5 | +66.3% | 5 |
3y (53 dates with one): 5 of 53 cleared, 8 beat SPY; range -46.6% to +94.2%
1y range -78.9 127.5 excess 2y -65.0 72.2
drawdown -85.6 -43.0

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2016-01-08 to 2016-04-15) | 15 | +113.2% | +61.3% to +244.6% | 15 | 15 | +88.3% | 15 |
| class FAIR, legacy tier ACCUMULATE (2016-04-22 to 2016-07-22) | 5 | +38.3% | +32.8% to +46.1% | 5 | 3 | +15.0% | 5 |
| class FAIR, legacy tier WATCHLIST (2016-05-13 to 2016-07-15) | 9 | +33.1% | +26.1% to +41.1% | 5 | 2 | +9.6% | 9 |
| class CHEAP, legacy tier ACCUMULATE (2016-07-29 to 2016-07-29) | 1 | +54.6% | +54.6% to +54.6% | 1 | 1 | +25.5% | 1 |
| class RICH, legacy tier WATCHLIST (2016-08-04 to 2016-11-03) | 10 | +39.3% | +26.5% to +45.6% | 7 | 5 | +7.6% | 3 |
| class RICH, legacy tier AVOID (2016-09-30 to 2016-12-30) | 12 | +8.6% | -25.1% to +34.8% | 1 | 0 | -1.7% | 11 |
| FY15E $2.43 (FY14's) (2016-01-08 to 2016-02-19) | 7 | +158.1% | +132.8% to +244.6% | 7 | 7 | +125.8% | 7 |
| FY16E $1.09 (FY15's) (2016-02-26 to 2016-12-30) | 45 | +33.4% | -25.1% to +113.2% | 27 | 19 | +8.6% | 37 |
| latest print Q3 2015 (2016-01-08 to 2016-02-19) | 7 | +158.1% | +132.8% to +244.6% | 7 | 7 | +125.8% | 7 |
| latest print Q4 2015 (2016-02-26 to 2016-04-22) | 9 | +81.5% | +38.3% to +113.2% | 9 | 9 | +62.4% | 9 |
| latest print Q1 2016 (2016-04-29 to 2016-07-29) | 14 | +34.9% | +26.1% to +54.6% | 10 | 5 | +12.1% | 14 |
| latest print Q2 2016 (2016-08-04 to 2016-10-28) | 13 | +33.4% | +28.5% to +45.6% | 8 | 5 | +2.8% | 5 |
| latest print Q3 2016 (2016-11-03 to 2016-12-30) | 9 | -1.3% | -25.1% to +26.5% | 0 | 0 | -5.6% | 9 |
3y (52 dates with one): 15 of 52 cleared, 15 beat SPY; range -11.8% to +235.1%
1y range -12.4 286.9 excess 2y -39.8 191.6
drawdown -44.4 -34.2

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2017-01-06 to 2017-12-29) | 18 | -15.6% | -21.4% to -1.1% | 0 | 0 | -16.9% | 18 |
| class CHEAP, legacy tier ACCUMULATE (2017-05-05 to 2017-07-28) | 11 | +0.6% | -6.4% to +9.0% | 0 | 0 | -1.0% | 0 |
| class CHEAP, legacy tier BUY (2017-06-16 to 2017-06-23) | 2 | +8.0% | +0.9% to +8.0% | 0 | 0 | +8.2% | 0 |
| class FAIR, legacy tier WATCHLIST (2017-08-04 to 2017-12-22) | 20 | -0.6% | -8.8% to +14.5% | 0 | 0 | -7.7% | 4 |
| class RICH, legacy tier WATCHLIST (2017-10-06 to 2017-10-06) | 1 | -0.4% | -0.4% to -0.4% | 0 | 0 | -13.3% | 1 |
| FY16E $1.09 (FY15's) (2017-01-06 to 2017-02-10) | 6 | -15.4% | -21.4% to -14.8% | 0 | 0 | -17.4% | 6 |
| FY17E $1.09 (FY15's) (2017-02-16 to 2017-12-29) | 46 | -1.0% | -19.0% to +14.5% | 0 | 0 | -7.7% | 17 |
| latest print Q3 2016 (2017-01-06 to 2017-02-10) | 6 | -15.4% | -21.4% to -14.8% | 0 | 0 | -17.4% | 6 |
| latest print Q4 2016 (2017-02-16 to 2017-04-28) | 11 | -15.9% | -19.0% to -9.8% | 0 | 0 | -15.4% | 11 |
| latest print Q1 2017 (2017-05-05 to 2017-07-28) | 13 | +0.8% | -6.4% to +9.0% | 0 | 0 | -0.5% | 0 |
| latest print Q2 2017 (2017-08-04 to 2017-10-27) | 13 | -1.0% | -8.8% to +14.5% | 0 | 0 | -5.0% | 3 |
| latest print Q3 2017 (2017-11-03 to 2017-12-29) | 9 | -0.4% | -5.0% to +10.7% | 0 | 0 | -9.9% | 3 |
3y (52 dates with one): 0 of 52 cleared, 0 beat SPY; range -71.0% to -11.2%
1y range -20.5 37.5 excess 2y -48.0 -6.6
drawdown -44.5 -41.7


## TRGP 2018-2021 (HINDSIGHT: labels, never inputs)

Computed on 2026-11-28 after the 2018-2021 build, its validation outputs, README section ("TRGP 2018-2021") and firewall result were
committed and pushed (`retro_tool.py outcome` on the 209 dates, then `findings_tables.py 2018,2019,2020,2021`). Every date has its 2-year
and 3-year horizons. Nothing here may feed a fact sheet, a builder or a rule; a pattern below is a hypothesis for a later method version
with its own full re-run, never a correction of these dates. This section was written without reading the 2012-2017 sections above.

**Across the batch (2-year total return; hurdle 15%/yr; "held" is `retro_tool`'s 2-year call check):**

| Class | Dates | Median 2-yr total return | Cleared hurdle | Beat SPY | Call held |
|---|---|---|---|---|---|
| CHEAP | 112 | +95.5% | 94 | 89 | 94 |
| FAIR | 57 | +9.4% | 18 | 8 | 9 |
| RICH | 40 | -13.4% | 8 | 8 | 32 |

The calls held on 135 of 209 dates. By year: 2018 (CHEAP 7, FAIR 24, RICH 21) median -51.7%, held 21 of 52; 2019 (18, 23, 11) +18.2%,
held 24; 2020 (46, 4, 3) +262.6%, held 49 of 53; 2021 (41, 6, 5) +94.4%, held 41.
### 2018 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2018-01-05 to 2018-11-02) | 21 | -57.0% | -63.9% to +0.2% | 0 | 0 | -50.1% | 21 |
| class FAIR, legacy tier WATCHLIST (2018-02-02 to 2018-11-16) | 19 | -51.7% | -68.9% to -1.2% | 0 | 0 | -21.3% | 0 |
| class CHEAP, legacy tier WATCHLIST (2018-03-29 to 2018-03-29) | 1 | -67.6% | -67.6% to -67.6% | 0 | 0 | -16.2% | 0 |
| class FAIR, legacy tier AVOID (2018-06-01 to 2018-07-06) | 5 | -48.7% | -49.3% to -33.8% | 0 | 0 | -37.5% | 0 |
| class CHEAP, legacy tier ACCUMULATE (2018-11-23 to 2018-12-14) | 4 | -31.4% | -36.5% to -23.5% | 0 | 0 | -50.5% | 0 |
| class CHEAP, legacy tier BUY (2018-12-21 to 2018-12-28) | 2 | -11.8% | -12.7% to -11.8% | 0 | 0 | -40.2% | 0 |
| FY17E $1.09 (FY15's) (2018-01-05 to 2018-02-09) | 6 | -4.3% | -8.8% to +0.2% | 0 | 0 | -18.1% | 4 |
| FY18E $1.09 (FY15's) (2018-02-16 to 2018-12-28) | 46 | -52.6% | -68.9% to -1.2% | 0 | 0 | -41.5% | 17 |
| latest print Q3 2017 (2018-01-05 to 2018-02-09) | 6 | -4.3% | -8.8% to +0.2% | 0 | 0 | -18.1% | 4 |
| latest print Q4 2017 (2018-02-16 to 2018-04-27) | 11 | -64.2% | -68.9% to -1.2% | 0 | 0 | -19.0% | 0 |
| latest print Q1 2018 (2018-05-04 to 2018-08-03) | 14 | -49.3% | -60.0% to -33.8% | 0 | 0 | -36.0% | 4 |
| latest print Q2 2018 (2018-08-10 to 2018-11-02) | 13 | -59.2% | -63.9% to -51.6% | 0 | 0 | -53.1% | 13 |
| latest print Q3 2018 (2018-11-09 to 2018-12-28) | 8 | -31.4% | -51.7% to -11.8% | 0 | 0 | -50.5% | 0 |
3y (52 dates with one): 2 of 52 cleared, 0 beat SPY; range -27.8% to +64.5%
1y range -34.3 26.4 excess 2y -91.2 -21.7
drawdown -91.9 -44.5

### 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE (2019-01-04 to 2019-12-13) | 15 | +25.7% | -26.5% to +52.1% | 5 | 2 | -21.5% | 5 |
| class CHEAP, legacy tier WATCHLIST (2019-02-15 to 2019-02-15) | 1 | -23.6% | -23.6% to -23.6% | 0 | 0 | -56.9% | 0 |
| class RICH, legacy tier WATCHLIST (2019-02-21 to 2019-02-21) | 1 | -19.1% | -19.1% to -19.1% | 0 | 0 | -53.6% | 1 |
| class RICH, legacy tier ACCUMULATE (2019-03-01 to 2019-05-03) | 10 | -5.9% | -14.1% to -2.6% | 0 | 0 | -47.6% | 10 |
| class FAIR, legacy tier ACCUMULATE (2019-05-08 to 2019-12-20) | 17 | +26.4% | +3.5% to +49.3% | 5 | 0 | -28.1% | 5 |
| class FAIR, legacy tier WATCHLIST (2019-05-17 to 2019-12-27) | 6 | +33.3% | +0.3% to +44.9% | 3 | 0 | -16.1% | 1 |
| class CHEAP, legacy tier BUY (2019-08-16 to 2019-08-23) | 2 | +38.2% | +33.3% to +38.2% | 2 | 0 | -7.2% | 2 |
| FY18E $1.09 (FY15's) (2019-01-04 to 2019-02-15) | 7 | -21.3% | -26.5% to -17.3% | 0 | 0 | -53.5% | 0 |
| FY19E $1.09 (FY15's) (2019-02-21 to 2019-12-27) | 45 | +20.4% | -19.1% to +52.1% | 15 | 2 | -28.1% | 24 |
| latest print Q3 2018 (2019-01-04 to 2019-02-15) | 7 | -21.3% | -26.5% to -17.3% | 0 | 0 | -53.5% | 0 |
| latest print Q4 2018 (2019-02-21 to 2019-05-03) | 11 | -11.5% | -19.1% to -2.6% | 0 | 0 | -49.7% | 11 |
| latest print Q1 2019 (2019-05-08 to 2019-08-02) | 13 | +17.2% | +0.3% to +37.5% | 1 | 0 | -32.4% | 1 |
| latest print Q2 2019 (2019-08-09 to 2019-11-01) | 13 | +33.3% | +12.3% to +49.3% | 7 | 0 | -14.0% | 6 |
| latest print Q3 2019 (2019-11-08 to 2019-12-27) | 8 | +47.7% | +27.4% to +52.1% | 7 | 2 | +4.4% | 6 |
3y (52 dates with one): 45 of 52 cleared, 44 beat SPY; range +44.1% to +122.6%
1y range -75.6 13.9 excess 2y -71.9 1.0
drawdown -90.1 -88.7

### 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier WATCHLIST (2020-01-03 to 2020-01-17) | 2 | +43.9% | +33.0% to +43.9% | 2 | 1 | +4.1% | 1 |
| class FAIR, legacy tier ACCUMULATE (2020-01-10 to 2020-01-24) | 2 | +47.8% | +41.7% to +47.8% | 2 | 1 | +12.4% | 2 |
| class CHEAP, legacy tier ACCUMULATE (2020-01-31 to 2020-05-01) | 5 | +72.4% | +61.6% to +532.6% | 5 | 5 | +22.8% | 5 |
| class RICH, legacy tier AVOID (2020-02-21 to 2020-03-06) | 3 | +105.0% | +61.3% to +153.3% | 3 | 3 | +43.3% | 0 |
| class CHEAP, legacy tier BUY (2020-03-20 to 2020-12-31) | 41 | +289.5% | +149.3% to +1138.4% | 41 | 41 | +226.8% | 41 |
| FY19E $1.09 (FY15's) (2020-01-03 to 2020-02-14) | 7 | +47.8% | +33.0% to +72.4% | 7 | 5 | +12.4% | 6 |
| FY20E $0.329 (the earnings guide) (2020-02-21 to 2020-05-01) | 11 | +694.4% | +61.3% to +1138.4% | 11 | 11 | +440.9% | 8 |
| FY20E $1.09 (FY15's) (2020-05-08 to 2020-12-31) | 35 | +275.6% | +149.3% to +456.3% | 35 | 35 | +216.8% | 35 |
| latest print Q3 2019 (2020-01-03 to 2020-02-14) | 7 | +47.8% | +33.0% to +72.4% | 7 | 5 | +12.4% | 6 |
| latest print Q4 2019 (2020-02-21 to 2020-05-01) | 11 | +694.4% | +61.3% to +1138.4% | 11 | 11 | +440.9% | 8 |
| latest print Q1 2020 (2020-05-08 to 2020-07-31) | 13 | +241.7% | +200.6% to +456.3% | 13 | 13 | +214.6% | 13 |
| latest print Q2 2020 (2020-08-07 to 2020-10-30) | 13 | +305.3% | +232.8% to +399.0% | 13 | 13 | +280.5% | 13 |
| latest print Q3 2020 (2020-11-06 to 2020-12-31) | 9 | +190.3% | +149.3% to +325.8% | 9 | 9 | +156.0% | 9 |
3y (53 dates with one): 53 of 53 cleared, 53 beat SPY; range +78.6% to +1130.0%
1y range -33.1 413.4 excess 2y -18.7 1051.3
drawdown -88.7 -30.2

### 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2021-01-08 to 2021-12-31) | 41 | +84.1% | +56.1% to +181.5% | 41 | 41 | +58.4% | 41 |
| class FAIR, legacy tier WATCHLIST (2021-02-19 to 2021-04-09) | 3 | +151.6% | +148.0% to +153.6% | 3 | 3 | +126.2% | 0 |
| class RICH, legacy tier AVOID (2021-03-05 to 2021-04-30) | 5 | +128.8% | +117.4% to +139.5% | 5 | 5 | +103.0% | 0 |
| class FAIR, legacy tier AVOID (2021-03-19 to 2021-04-01) | 3 | +114.4% | +114.2% to +133.6% | 3 | 3 | +116.8% | 0 |
| FY20E $1.09 (FY15's) (2021-01-08 to 2021-02-12) | 6 | +157.1% | +149.6% to +181.5% | 6 | 6 | +132.6% | 6 |
| FY21E $0.699 (the earnings guide) (2021-02-19 to 2021-04-30) | 11 | +133.6% | +114.2% to +153.6% | 11 | 11 | +116.6% | 0 |
| FY21E $1.522 (the earnings guide) (2021-05-07 to 2021-07-30) | 13 | +84.4% | +56.1% to +98.2% | 13 | 13 | +68.1% | 13 |
| FY21E $1.74 (the earnings guide) (2021-08-06 to 2021-10-29) | 13 | +93.4% | +59.3% to +109.3% | 13 | 13 | +61.6% | 13 |
| FY21E $2.045 (the earnings guide) (2021-11-05 to 2021-12-31) | 9 | +72.0% | +61.2% to +82.3% | 9 | 9 | +49.4% | 9 |
| latest print Q3 2020 (2021-01-08 to 2021-02-12) | 6 | +157.1% | +149.6% to +181.5% | 6 | 6 | +132.6% | 6 |
| latest print Q4 2020 (2021-02-19 to 2021-04-30) | 11 | +133.6% | +114.2% to +153.6% | 11 | 11 | +116.6% | 0 |
| latest print Q1 2021 (2021-05-07 to 2021-07-30) | 13 | +84.4% | +56.1% to +98.2% | 13 | 13 | +68.1% | 13 |
| latest print Q2 2021 (2021-08-06 to 2021-10-29) | 13 | +93.4% | +59.3% to +109.3% | 13 | 13 | +61.6% | 13 |
| latest print Q3 2021 (2021-11-05 to 2021-12-31) | 9 | +72.0% | +61.2% to +82.3% | 9 | 9 | +49.4% | 9 |
3y (52 dates with one): 52 of 52 cleared, 52 beat SPY; range +162.5% to +296.4%
1y range 18.7 151.0 excess 2y 51.9 168.6
drawdown -30.2 -30.2

**Hypotheses (for a later method version, each needing its own full re-run; none applied here):**
- The 2018 dates, mostly FAIR and RICH on FY15's $1.09 (then three years old), all but one lost (2-year returns -68.9% to +0.2%; the
  March 2020 collapse inside every horizon); the RICH calls held, the FAIR calls did not, as FAIR is not a call to lose. A stale anchor read against a window of its
  own 2011-2015 multiples says little about a business whose GAAP earnings were lost to impairments.
- The CHEAP calls of 2020 (46: on the FY2020E $0.329 to 2020-05-01, then on FY15's $1.09 with the estimated net losses read as no guide)
  and of 2021 (41: on FY15's $1.09 to 2021-02-12, then on the earnings guide from 2021-05-07) held on every date; the FAIR and RICH dates of 2021-02-19 to 2021-04-30, on the first FY2021E estimate ($0.699, after
  $137.6M of preferred dividends with the deemed part annualized), returned +114% to +154% and missed. The sensitivity's display-only
  reading (FY15's $1.09) and the cash-dividends-only reading would have made all 11 of those dates CHEAP: a hypothesis on the deemed
  dividend's annualization, not a rule.
- The three RICH dates of 2020-02-21 to 2020-03-06 (the FY2020E $0.329) returned +61% to +153% from the COVID-19 trough that followed;
  outcome luck of the window, read as such.
- The signals at BEAR (80 classes in the sensitivity) and the loss years kept without impairments (106) would have turned many of these
  CHEAP dates RICH; the outcomes favour the encoding as built for 2020-2021 and are mixed for 2018-2019.
