# NEM retrospective findings (hindsight)

Patterns seen in `outcome.json` for the NEM weekly dates: 105 from 2008-01-04 to 2009-12-31, all Newmont Mining Corporation (NYSE: NEM).
They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its point-in-time
build, validation outputs, README section and firewall result were committed and pushed (24fcadece, 1e9dff356, c4a387d70), on 2026-11-27.
The one-line 2026 profile that `retro_tool outcome` copies into each `outcome.json` (`profile_drift`: today CYCLICAL, "gold miner; gold
price, rising AISC") was first seen there, after every model had been built, validated and committed. Every date has its 6-month, 1-, 2- and
3-year horizons. Total returns include the $0.10 quarterly dividends. The 15%/yr hurdle is +32.2% over two years. "Call held" is
`call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY).

## 2008 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2008-01-04 to 2008-12-26) | 52 | +21.6% | -15.6% to +157.5% | 21 | 51 | +2.1% | 51 |
| FY07E $1.18 (FY06's) (2008-01-04 to 2008-02-15) | 7 | -8.5% | -15.6% to -1.2% | 0 | 6 | -17.0% | 6 |
| FY08E $1.25 (FY06's) (2008-02-22 to 2008-12-26) | 45 | +26.8% | -5.2% to +157.5% | 21 | 45 | +4.4% | 45 |
| latest print Q3 2007 (2008-01-04 to 2008-02-15) | 7 | -8.5% | -15.6% to -1.2% | 0 | 6 | -17.0% | 6 |
| latest print Q4 2007 (2008-02-22 to 2008-04-18) | 9 | +7.8% | -5.2% to +19.7% | 0 | 9 | -2.9% | 9 |
| latest print Q1 2008 (2008-04-25 to 2008-07-18) | 13 | +19.6% | +9.0% to +27.8% | 0 | 13 | -1.9% | 13 |
| latest print Q2 2008 (2008-07-25 to 2008-10-24) | 14 | +53.4% | +19.9% to +152.8% | 12 | 14 | +28.7% | 14 |
| latest print Q3 2008 (2008-10-30 to 2008-12-26) | 9 | +112.5% | +57.0% to +157.5% | 9 | 9 | +87.1% | 9 |
3y (52 dates with one): 17 of 52 cleared, 48 beat SPY; range +0.1% to +193.6%

## 2009 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2009-01-02 to 2009-12-31) | 53 | +39.0% | +17.0% to +60.5% | 35 | 26 | +36.3% | 41 |
| FY08E $1.25 (FY06's) (2009-01-02 to 2009-02-13) | 7 | +40.5% | +27.7% to +56.0% | 6 | 2 | +39.3% | 6 |
| FY09E $1.82 (FY08's) (2009-02-20 to 2009-09-11) | 30 | +37.0% | +17.0% to +53.9% | 19 | 8 | +38.7% | 19 |
| FY09E $1.80 (FY08's) (2009-09-18 to 2009-12-31) | 16 | +40.7% | +21.9% to +60.5% | 10 | 16 | +24.2% | 16 |
| latest print Q3 2008 (2009-01-02 to 2009-02-13) | 7 | +40.5% | +27.7% to +56.0% | 6 | 2 | +39.3% | 6 |
| latest print Q4 2008 (2009-02-20 to 2009-04-24) | 10 | +37.7% | +17.3% to +53.9% | 7 | 0 | +38.8% | 7 |
| latest print Q1 2009 (2009-05-01 to 2009-07-17) | 12 | +25.7% | +17.0% to +53.8% | 4 | 0 | +36.6% | 4 |
| latest print Q2 2009 (2009-07-24 to 2009-10-23) | 14 | +44.0% | +33.5% to +52.6% | 14 | 14 | +37.4% | 14 |
| latest print Q3 2009 (2009-10-30 to 2009-12-31) | 10 | +32.1% | +21.9% to +60.5% | 4 | 10 | +18.8% | 10 |
3y (53 dates with one): 5 of 53 cleared, 3 beat SPY; range -7.8% to +72.6%

## What the labels suggest (hypotheses only)

- **Every date was CHEAP and BUY, and the call held on 92 of 105** (51 of 52 in 2008, 41 of 53 in 2009). The 2-year median was +21.6% for
  the 2008 entries and +39.0% for 2009's; 56 of 105 cleared the 15%/yr hurdle.
- **The 2008 calls held mostly by beating a falling market** (51 of 52 beat SPY, 21 cleared the hurdle): the January-February 2008
  entries on FY06's $1.18 lost 1-16% over two years, and only the entries from the Q2 2008 print on (late July to December 2008, the price
  mostly under the EPP floor) cleared the hurdle: 21 of those 23 dates, medians +53.4% and +112.5%. The m12-24 average price was +2.1% (median) for 2008 entries: a stock that went nowhere for a
  year and a half after entry, then rose.
- **The 2009 calls cleared the hurdle more often (35 of 53) but lagged a rebounding market** (26 of 53 beat SPY; none of the 22 dates from
  the Q4 2008 print to mid-July 2009 did). 11 of the 12 misses are there.
- **The class did not discriminate:** with one class on every date, the series tests only "buy Newmont on its own 2002-2009 multiple".
  The window's median (42-47x on the low 2002-2006 earnings) made every anchor read cheap; whether that is information or an artefact of a
  loss-heavy decade cannot be told from one stock. Worth testing on other miners and other loss-heavy windows before any rule changes.
- **The kind drifted:** DURABLE then (no 10-K said "cyclical"), CYCLICAL in today's profile. Label only; it changes no price state.
- The worst within-2-year drawdowns (-62% from the January 2008 entries) came with CHEAP calls: CHEAP here never meant safe.

# NEM 2010-2013 (hindsight)

Patterns seen in `outcome.json` for the 209 weekly dates from 2010-01-08 to 2013-12-31. **Labels and hypotheses**: never feed them back into
the method or the fact sheet. Scored only after the point-in-time build, validation outputs, README section and firewall result were
committed and pushed (bd147f46d, 550100550, 31bedf244, 55ac54199), on 2026-11-27; the 2008-2009 findings above were first opened then.
Every date has its 6-month, 1-, 2- and 3-year horizons. Total returns include the dividends paid. "Call held" is `call_check_2y`: CHEAP
should clear the 15%/yr hurdle or beat SPY.

## 2010 (52 dates)
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2010-01-08 to 2010-12-31) | 52 | -9.4% | -23.2% to +47.0% | 4 | 7 | -0.1% | 7 |
| FY09E $1.80 (FY08's) (2010-01-08 to 2010-02-19) | 7 | +35.2% | +25.6% to +47.0% | 4 | 6 | +27.7% | 6 |
| FY10E $2.68 (FY09's) (2010-02-26 to 2010-12-31) | 45 | -11.7% | -23.2% to +29.9% | 0 | 1 | -2.7% | 1 |
| latest print Q3 2009 (2010-01-08 to 2010-02-19) | 7 | +35.2% | +25.6% to +47.0% | 4 | 6 | +27.7% | 6 |
| latest print Q4 2009 (2010-02-26 to 2010-04-23) | 9 | +8.9% | -9.5% to +29.9% | 0 | 1 | +15.7% | 1 |
| latest print Q1 2010 (2010-04-28 to 2010-07-23) | 13 | -13.7% | -21.3% to -0.8% | 0 | 0 | +1.7% | 0 |
| latest print Q2 2010 (2010-07-29 to 2010-10-29) | 14 | -9.4% | -16.5% to -2.8% | 0 | 0 | -7.9% | 0 |
| latest print Q3 2010 (2010-11-03 to 2010-12-31) | 9 | -20.8% | -23.2% to -13.8% | 0 | 0 | -12.7% | 0 |
3y (52 dates with one): 0 of 52 cleared, 0 beat SPY; range -56.8% to +9.1%

## 2011 (52 dates)
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2011-01-07 to 2011-12-30) | 52 | -39.8% | -60.8% to -14.4% | 0 | 0 | -21.1% | 0 |
| FY10E $2.68 (FY09's) (2011-01-07 to 2011-02-18) | 7 | -17.6% | -21.9% to -14.4% | 0 | 0 | -10.3% | 0 |
| FY11E $4.61 (FY10's) (2011-02-25 to 2011-12-30) | 45 | -41.9% | -60.8% to -16.1% | 0 | 0 | -25.4% | 0 |
| latest print Q3 2010 (2011-01-07 to 2011-02-18) | 7 | -17.6% | -21.9% to -14.4% | 0 | 0 | -10.3% | 0 |
| latest print Q4 2010 (2011-02-25 to 2011-04-15) | 8 | -20.3% | -36.6% to -16.1% | 0 | 0 | -10.9% | 0 |
| latest print Q1 2011 (2011-04-21 to 2011-07-22) | 14 | -37.5% | -47.0% to -29.1% | 0 | 0 | -17.9% | 0 |
| latest print Q2 2011 (2011-07-29 to 2011-10-21) | 13 | -49.2% | -57.4% to -40.8% | 0 | 0 | -37.7% | 0 |
| latest print Q3 2011 (2011-10-28 to 2011-12-30) | 10 | -56.9% | -60.8% to -54.5% | 0 | 0 | -46.4% | 0 |
3y (52 dates with one): 0 of 52 cleared, 0 beat SPY; range -69.0% to -43.2%

## 2012 (52 dates)
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2012-01-06 to 2012-12-28) | 52 | -49.9% | -61.2% to -38.5% | 0 | 0 | -47.6% | 0 |
| FY11E $4.61 (FY10's) (2012-01-06 to 2012-02-17) | 7 | -56.9% | -61.2% to -54.2% | 0 | 0 | -49.1% | 0 |
| FY12E $4.61 (FY10's) (2012-02-24 to 2012-12-28) | 45 | -49.3% | -57.9% to -38.5% | 0 | 0 | -47.3% | 0 |
| latest print Q3 2011 (2012-01-06 to 2012-02-17) | 7 | -56.9% | -61.2% to -54.2% | 0 | 0 | -49.1% | 0 |
| latest print Q4 2011 (2012-02-24 to 2012-04-20) | 9 | -48.6% | -57.9% to -44.4% | 0 | 0 | -46.3% | 0 |
| latest print Q1 2012 (2012-04-27 to 2012-07-20) | 13 | -43.0% | -49.9% to -39.0% | 0 | 0 | -45.4% | 0 |
| latest print Q2 2012 (2012-07-27 to 2012-10-26) | 14 | -46.4% | -56.3% to -38.5% | 0 | 0 | -51.5% | 0 |
| latest print Q3 2012 (2012-11-02 to 2012-12-28) | 9 | -54.9% | -57.9% to -53.7% | 0 | 0 | -48.0% | 0 |
3y (52 dates with one): 0 of 52 cleared, 0 beat SPY; range -68.9% to -34.0%

## 2013 (53 dates)
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2013-01-04 to 2013-12-31) | 53 | -33.8% | -54.7% to -6.2% | 0 | 0 | -27.0% | 0 |
| FY12E $4.61 (FY10's) (2013-01-04 to 2013-02-15) | 7 | -43.2% | -54.7% to -39.1% | 0 | 0 | -48.1% | 0 |
| FY13E $3.78 (FY12's) (2013-02-22 to 2013-12-31) | 46 | -28.0% | -46.8% to -6.2% | 0 | 0 | -23.5% | 0 |
| latest print Q3 2012 (2013-01-04 to 2013-02-15) | 7 | -43.2% | -54.7% to -39.1% | 0 | 0 | -48.1% | 0 |
| latest print Q4 2012 (2013-02-22 to 2013-04-26) | 10 | -35.7% | -44.4% to -22.2% | 0 | 0 | -40.9% | 0 |
| latest print Q1 2013 (2013-05-01 to 2013-07-19) | 12 | -15.6% | -26.9% to -6.2% | 0 | 0 | -24.0% | 0 |
| latest print Q2 2013 (2013-07-26 to 2013-10-25) | 14 | -38.9% | -46.8% to -24.2% | 0 | 0 | -22.5% | 0 |
| latest print Q3 2013 (2013-11-01 to 2013-12-31) | 10 | -21.4% | -35.2% to -9.8% | 0 | 0 | -10.4% | 0 |
3y (53 dates with one): 2 of 53 cleared, 23 beat SPY; range -59.4% to +62.2%

## What the 2010-2013 labels suggest (hypotheses only)

- **Every date was CHEAP and BUY again, and the call held on only 7 of 209**, all seven in January-February 2010 (on FY08's $1.80, with
  the Q3 2009 print), which rose 26-47% in two years. From 2010-02-26 no date held: 4 of 209 cleared the hurdle, 7 beat SPY, and the
  2-year medians were -9.4% (2010), -39.8% (2011), -49.9% (2012) and -33.8% (2013). Every date's 2-year scenario landing is BEAR.
- **The anchors rose as the price peaked and then failed to fall with it.** FY09's $2.68 and FY10's $4.61 entered the history at record
  gold prices; FY10's $4.61 then stood for two years (FY2011 excluded), so the multiple read 9-15x against a 28-40x window median while
  the price fell from $70 to $43, and FY12's $3.78 kept the stock at the 0th-4th percentile through 2013's halving. A miner's trailing
  GAAP EPS at a metal-price peak looks like the classic cyclical value trap; the method's own-history multiple had no way to see it.
- **The window carried the 2002-2006 regime of 26-100x into every date** (and a five-year window, tested point in time, moved nothing,
  as 2005-2009 multiples were high too). Together with 2008-2009 (92 of 105 held), the series says only that "Newmont at its own past
  multiple" worked from the 2008 trough and failed from the 2010-2011 peak: one stock, one metal cycle, not evidence for any rule.
- **The signals did not warn either** (every data signal at BEAR moved no class point in time): unit costs rose 11-32% a year from
  Q1 2010 to Q2 2013 and ounces produced fell from Q3 2010, mostly inside rule T's BASE band set on 1997-2006 (costs per ounce
  beyond its +28% only in Q3 2011 and Q2 2013). Hypothesis to test on other miners
  and cyclicals: thresholds from a calmer decade are too wide for a cost squeeze.
- **The kind drifted** as in 2008-2009: DURABLE then (no 10-K said "cyclical"), CYCLICAL in today's profile. Label only; it changes no
  price state, but a CYCLICAL reading would at least have named the trap.
- Within-2-year drawdowns ran from -22% (early 2010) to -67% (2012 entries): CHEAP here meant neither safe nor cheap.

# NEM 2014-2017 (hindsight)

Patterns seen in `outcome.json` for the 209 weekly dates from 2014-01-03 to 2017-12-29. **Labels and hypotheses**: never feed them back into
the method or the fact sheet. Scored only after the point-in-time build, validation outputs, README section and firewall result were
committed and pushed (5f919e4a7, c5c57da35, 63603c600, 4e2f43ec8), on 2026-11-27; the 2008-2013 findings above were first opened then.
Every date has its 6-month, 1-, 2- and 3-year horizons. Total returns include the dividends paid. "Call held" is `call_check_2y`: CHEAP
should clear the 15%/yr hurdle or beat SPY; RICH should not.

Overall: CHEAP 105 dates, median 2-year total return +59.1%, 83 cleared the hurdle, 94 beat SPY, 94 calls held; FAIR 6, +45.6%; RICH 98,
+5.9%, 10 cleared, 9 beat SPY, 88 calls held. Scenario landings at 2 years: BULL 145, BASE 46, BEAR 18.

## 2014 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2014-01-03 to 2014-12-26) | 52 | +54.2% | -31.7% to +91.2% | 35 | 41 | -3.6% | 41 |
| FY13E $3.78 (FY12's) (2014-01-03 to 2014-02-14) | 7 | -23.0% | -31.7% to +14.9% | 0 | 2 | -11.7% | 2 |
| FY14E $3.78 (FY12's) (2014-02-21 to 2014-06-06) | 16 | +25.6% | +0.6% to +54.2% | 6 | 10 | -11.2% | 10 |
| FY14E $3.76 (FY12's) (2014-06-13 to 2014-12-26) | 29 | +64.9% | +42.9% to +91.2% | 29 | 29 | +16.9% | 29 |
| latest print Q3 2013 (2014-01-03 to 2014-02-14) | 7 | -23.0% | -31.7% to +14.9% | 0 | 2 | -11.7% | 2 |
| latest print Q4 2013 (2014-02-21 to 2014-04-17) | 9 | +9.9% | +0.6% to +29.2% | 0 | 3 | -12.4% | 3 |
| latest print Q1 2014 (2014-04-25 to 2014-07-25) | 14 | +50.4% | +18.4% to +64.6% | 13 | 14 | -7.9% | 14 |
| latest print Q2 2014 (2014-07-31 to 2014-10-24) | 13 | +64.2% | +51.8% to +77.4% | 13 | 13 | +10.7% | 13 |
| latest print Q3 2014 (2014-10-31 to 2014-12-26) | 9 | +73.4% | +67.4% to +91.2% | 9 | 9 | +68.5% | 9 |
3y (52 dates with one): 21 of 52 cleared, 48 beat SPY; range +25.1% to +104.2%
1y range -39.2 19.4 excess 2y -42.6 82.2
drawdown -43.8 -43.8

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2015-01-02 to 2015-12-31) | 40 | +92.8% | +39.9% to +148.0% | 40 | 40 | +84.0% | 40 |
| class FAIR, legacy tier BUY (2015-02-20 to 2015-04-17) | 3 | +45.6% | +29.9% to +47.8% | 2 | 3 | +37.2% | 1 |
| class CHEAP, legacy tier ACCUMULATE (2015-04-24 to 2015-07-02) | 7 | +34.5% | +24.3% to +42.9% | 4 | 7 | +45.1% | 7 |
| class FAIR, legacy tier WATCHLIST (2015-05-15 to 2015-05-15) | 1 | +23.2% | +23.2% to +23.2% | 0 | 1 | +30.9% | 1 |
| class CHEAP, legacy tier WATCHLIST (2015-05-22 to 2015-05-29) | 2 | +26.1% | +25.6% to +26.1% | 0 | 2 | +34.1% | 2 |
| FY14E $3.76 (FY12's) (2015-01-02 to 2015-02-13) | 7 | +55.9% | +39.9% to +77.3% | 7 | 7 | +44.1% | 7 |
| FY15E $1.10 (FY14's) (2015-02-20 to 2015-12-31) | 46 | +83.2% | +23.2% to +148.0% | 39 | 46 | +78.8% | 44 |
| latest print Q3 2014 (2015-01-02 to 2015-02-13) | 7 | +55.9% | +39.9% to +77.3% | 7 | 7 | +44.1% | 7 |
| latest print Q4 2014 (2015-02-20 to 2015-04-17) | 9 | +47.8% | +29.9% to +56.1% | 8 | 9 | +55.6% | 7 |
| latest print Q1 2015 (2015-04-24 to 2015-07-17) | 13 | +34.5% | +23.2% to +64.4% | 7 | 13 | +45.1% | 13 |
| latest print Q2 2015 (2015-07-24 to 2015-10-23) | 14 | +123.8% | +92.0% to +148.0% | 14 | 14 | +103.8% | 14 |
| latest print Q3 2015 (2015-10-30 to 2015-12-31) | 10 | +107.3% | +81.6% to +115.2% | 10 | 10 | +98.0% | 10 |
3y (53 dates with one): 45 of 53 cleared, 53 beat SPY; range +44.8% to +127.9%
1y range -30.5 175.9 excess 2y 5.9 114.6
drawdown -43.8 -32.6

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2016-01-08 to 2016-01-29) | 4 | +126.9% | +102.7% to +140.0% | 4 | 4 | +100.8% | 4 |
| class FAIR, legacy tier ACCUMULATE (2016-02-05 to 2016-02-05) | 1 | +56.4% | +56.4% to +56.4% | 1 | 1 | +46.7% | 1 |
| class FAIR, legacy tier WATCHLIST (2016-02-12 to 2016-02-12) | 1 | +44.6% | +44.6% to +44.6% | 1 | 0 | +38.9% | 1 |
| class RICH, legacy tier AVOID (2016-02-19 to 2016-12-30) | 46 | +3.9% | -26.0% to +59.0% | 10 | 9 | +7.6% | 36 |
| FY15E $1.10 (FY14's) (2016-01-08 to 2016-02-12) | 6 | +115.1% | +44.6% to +140.0% | 6 | 5 | +97.0% | 6 |
| FY16E $1.10 (FY14's) (2016-02-19 to 2016-12-30) | 46 | +3.9% | -26.0% to +59.0% | 10 | 9 | +7.6% | 36 |
| latest print Q3 2015 (2016-01-08 to 2016-02-12) | 6 | +115.1% | +44.6% to +140.0% | 6 | 5 | +97.0% | 6 |
| latest print Q4 2015 (2016-02-19 to 2016-04-15) | 9 | +46.7% | +36.3% to +59.0% | 9 | 8 | +36.5% | 0 |
| latest print Q1 2016 (2016-04-22 to 2016-07-15) | 13 | +10.5% | -9.4% to +34.0% | 1 | 1 | +5.4% | 12 |
| latest print Q2 2016 (2016-07-22 to 2016-10-21) | 14 | -18.3% | -26.0% to -4.3% | 0 | 0 | -5.5% | 14 |
| latest print Q3 2016 (2016-10-28 to 2016-12-30) | 10 | +3.9% | -13.2% to +7.8% | 0 | 0 | +11.2% | 10 |
3y (52 dates with one): 4 of 52 cleared, 4 beat SPY; range -11.2% to +98.1%
1y range -21.7 110.8 excess 2y -61.1 86.7
drawdown -32.6 -26.6

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2017-01-06 to 2017-12-29) | 52 | +7.5% | -8.0% to +25.8% | 0 | 0 | -1.2% | 52 |
| FY16E $1.10 (FY14's) (2017-01-06 to 2017-02-17) | 7 | -5.7% | -8.0% to +3.4% | 0 | 0 | +1.6% | 7 |
| FY17E $1.30 (FY14's) (2017-02-23 to 2017-12-29) | 45 | +8.5% | -5.4% to +25.8% | 0 | 0 | -1.4% | 45 |
| latest print Q3 2016 (2017-01-06 to 2017-02-17) | 7 | -5.7% | -8.0% to +3.4% | 0 | 0 | +1.6% | 7 |
| latest print Q4 2016 (2017-02-23 to 2017-04-21) | 9 | +5.1% | +1.6% to +11.3% | 0 | 0 | +3.3% | 9 |
| latest print Q1 2017 (2017-04-26 to 2017-07-21) | 13 | +9.4% | -5.4% to +25.8% | 0 | 0 | +0.8% | 13 |
| latest print Q2 2017 (2017-07-26 to 2017-10-20) | 13 | +7.3% | +2.5% to +12.9% | 0 | 0 | -8.3% | 13 |
| latest print Q3 2017 (2017-10-27 to 2017-12-29) | 10 | +15.3% | +8.5% to +20.7% | 0 | 0 | -1.5% | 10 |
3y (52 dates with one): 41 of 52 cleared, 44 beat SPY; range +24.0% to +107.3%
1y range -22.3 24.7 excess 2y -30.2 -0.9
drawdown -29.4 -29.4

## What the 2014-2017 labels suggest (hypotheses only)

- The class followed the anchor more than the business. FY12's $3.78 against a $19-27 stock made every 2014 date CHEAP at 5-7x; the
  calls held from the Q1 2014 print on (gold's low and the 2015-2016 rally), but the seven January-February 2014 dates lost 23% (median)
  and only 2 of 7 held: an anchor two years stale and from a year of $1,660 gold.
- The fragile 2015 CHEAP calls (FY14's $1.10 against a ~20x median) were the best entries of the batch: median +83% at 2 years, 46 of 46
  beat SPY. The sensitivity table shows the method only narrowly called them CHEAP (the adjusted-EPS reading, a five-year window or the
  signals at BEAR each turn most of them FAIR or RICH); hindsight favours the narrow call, not a rule.
- RICH from 2016-02-19 on (FY15 excluded, the stock tripling off its low on the same $1.10, then $1.30) held on 88 of 98 dates: the
  2016-2017 entries returned +3.9% and +7.5% median at 2 years and none of 2017's cleared the hurdle or beat SPY. The misses are the
  Q4 2015-print dates of February-April 2016 (+47% median, 0 of 9 held): the exclusion of FY2015 flipped the class just as the rally ran.
- At 3 years the 2017 RICH dates mostly cleared (41 of 52) on the 2019-2020 gold run: a 2-year RICH call on a gold miner is a
  timing call against the metal, not a valuation one.
- Profile drift again: DURABLE then (no 10-K says "cyclical"), CYCLICAL in today's profile. Label only.
- Hypothesis for a later method version (never this one): for a miner whose GAAP years swing between write-down losses and thin profits,
  the rollover anchor goes stale for years at a time (FY12 to February 2015, FY14 to the end of 2017); an anchor rule that tracks the
  metal price or production economics would be a new rule, decided before scoring, with a full re-run.

# NEM 2018-2021 (hindsight)

Patterns seen in `outcome.json` for the 209 weekly dates from 2018-01-05 to 2021-12-31. **Labels and hypotheses**: never feed them back into
the method or the fact sheet. Scored only after the point-in-time build, validation outputs, README section and firewall result were
committed and pushed (bb7663c31, dac282ed2, 6d75c5b82, e5e08862e), on 2026-11-28; the 2008-2017 findings above were first opened then.
Every date has its 6-month, 1-, 2- and 3-year horizons. Total returns include the dividends paid. "Call held" is `call_check_2y`: CHEAP
should clear the 15%/yr hurdle or beat SPY; RICH should not.

Overall: RICH 183 dates, median 2-year total return +46.3%, 97 cleared the hurdle, 89 beat SPY, 80 calls held; FAIR 11, +51.3%, 11
cleared; CHEAP 15, -24.7%, 0 cleared, 0 beat SPY, 0 calls held. Scenario landings at 2 years: XBULL 91, BULL 59, BEAR 46, BASE 13.

## 2018 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2018-01-05 to 2018-12-28) | 52 | +67.3% | +11.3% to +129.1% | 40 | 46 | +21.1% | 6 |
| FY17E $1.30 (FY14's) (2018-01-05 to 2018-02-16) | 7 | +16.7% | +11.3% to +25.2% | 0 | 1 | -4.9% | 6 |
| FY18E $1.30 (FY14's) (2018-02-23 to 2018-04-20) | 9 | +32.0% | +12.6% to +48.8% | 4 | 9 | +0.3% | 0 |
| FY18E $1.28 (FY14's) (2018-04-27 to 2018-12-28) | 36 | +90.2% | +50.2% to +129.1% | 36 | 36 | +61.2% | 0 |
| latest print Q3 2017 (2018-01-05 to 2018-02-16) | 7 | +16.7% | +11.3% to +25.2% | 0 | 1 | -4.9% | 6 |
| latest print Q4 2017 (2018-02-23 to 2018-04-20) | 9 | +32.0% | +12.6% to +48.8% | 4 | 9 | +0.3% | 0 |
| latest print Q1 2018 (2018-04-27 to 2018-07-20) | 13 | +63.3% | +50.2% to +79.1% | 13 | 13 | +15.2% | 0 |
| latest print Q2 2018 (2018-07-27 to 2018-10-19) | 13 | +110.1% | +92.7% to +129.1% | 13 | 13 | +63.5% | 0 |
| latest print Q3 2018 (2018-10-26 to 2018-12-28) | 10 | +90.2% | +80.2% to +113.1% | 10 | 10 | +71.4% | 0 |
3y (52 dates with one): 52 of 52 cleared, 46 beat SPY; range +54.8% to +106.6%
1y range -21.8 35.4 excess 2y -9.8 108.9
drawdown -29.4 -24.5

## 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2019-01-04 to 2019-11-01) | 44 | +75.6% | +42.7% to +145.8% | 44 | 39 | +70.1% | 0 |
| class FAIR, legacy tier ACCUMULATE (2019-11-06 to 2019-11-29) | 4 | +57.2% | +51.6% to +64.3% | 4 | 3 | +62.1% | 4 |
| class RICH, legacy tier ACCUMULATE (2019-12-06 to 2019-12-20) | 2 | +51.4% | +47.0% to +51.4% | 2 | 1 | +52.6% | 0 |
| class RICH, legacy tier WATCHLIST (2019-12-13 to 2019-12-27) | 2 | +48.5% | +46.3% to +48.5% | 2 | 0 | +46.9% | 0 |
| FY18E $1.28 (FY14's) (2019-01-04 to 2019-02-15) | 7 | +85.9% | +84.3% to +102.5% | 7 | 7 | +76.4% | 0 |
| FY19E $1.28 (FY14's) (2019-02-22 to 2019-12-27) | 45 | +64.4% | +42.7% to +145.8% | 45 | 36 | +63.9% | 4 |
| latest print Q3 2018 (2019-01-04 to 2019-02-15) | 7 | +85.9% | +84.3% to +102.5% | 7 | 7 | +76.4% | 0 |
| latest print Q4 2018 (2019-02-22 to 2019-04-18) | 9 | +79.1% | +64.4% to +104.1% | 9 | 9 | +77.1% | 0 |
| latest print Q1 2019 (2019-04-26 to 2019-07-19) | 13 | +107.3% | +60.6% to +145.8% | 13 | 13 | +76.3% | 0 |
| latest print Q2 2019 (2019-07-26 to 2019-11-01) | 15 | +54.0% | +42.7% to +74.5% | 15 | 10 | +61.4% | 0 |
| latest print Q3 2019 (2019-11-06 to 2019-12-27) | 8 | +51.6% | +46.3% to +64.3% | 8 | 4 | +58.4% | 4 |
3y (52 dates with one): 28 of 52 cleared, 34 beat SPY; range +17.4% to +171.3%
1y range 21.7 121.4 excess 2y -9.7 96.5
drawdown -28.4 -24.5

## 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier ACCUMULATE (2020-01-03 to 2020-02-14) | 7 | +49.9% | +40.0% to +53.4% | 7 | 5 | +37.7% | 6 |
| class RICH, legacy tier AVOID (2020-02-21 to 2020-12-31) | 46 | -11.0% | -33.6% to +103.9% | 9 | 3 | -1.4% | 37 |
| FY19E $1.28 (FY14's) (2020-01-03 to 2020-02-14) | 7 | +49.9% | +40.0% to +53.4% | 7 | 5 | +37.7% | 6 |
| FY20E $1.28 (FY14's) (2020-02-21 to 2020-12-31) | 46 | -11.0% | -33.6% to +103.9% | 9 | 3 | -1.4% | 37 |
| latest print Q3 2019 (2020-01-03 to 2020-02-14) | 7 | +49.9% | +40.0% to +53.4% | 7 | 5 | +37.7% | 6 |
| latest print Q4 2019 (2020-02-21 to 2020-05-01) | 11 | +49.7% | +23.9% to +103.9% | 9 | 3 | +23.0% | 2 |
| latest print Q1 2020 (2020-05-06 to 2020-07-24) | 12 | +14.8% | -17.1% to +31.1% | 0 | 0 | +4.0% | 12 |
| latest print Q2 2020 (2020-07-31 to 2020-10-23) | 13 | -27.6% | -30.2% to -20.9% | 0 | 0 | -5.6% | 13 |
| latest print Q3 2020 (2020-10-30 to 2020-12-31) | 10 | -14.3% | -33.6% to -11.0% | 0 | 0 | -4.5% | 10 |
3y (53 dates with one): 0 of 53 cleared, 4 beat SPY; range -38.8% to +38.6%
1y range -14.3 56.3 excess 2y -58.6 43.7
drawdown -55.8 -28.4

## 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2021-01-08 to 2021-12-31) | 29 | -23.6% | -38.9% to -3.2% | 0 | 0 | -24.7% | 29 |
| class RICH, legacy tier ACCUMULATE (2021-02-19 to 2021-03-05) | 2 | -12.1% | -14.4% to -12.1% | 0 | 0 | -1.5% | 2 |
| class CHEAP, legacy tier BUY (2021-02-26 to 2021-10-22) | 15 | -24.7% | -27.2% to -11.8% | 0 | 0 | -21.9% | 0 |
| class RICH, legacy tier WATCHLIST (2021-03-12 to 2021-10-29) | 6 | -14.1% | -21.3% to -8.5% | 0 | 0 | -13.7% | 6 |
| FY20E $1.28 (FY14's) (2021-01-08 to 2021-02-12) | 6 | -6.5% | -11.1% to -3.2% | 0 | 0 | -4.9% | 6 |
| FY21E $3.31 (FY20's) (2021-02-19 to 2021-12-31) | 46 | -23.6% | -38.9% to -8.5% | 0 | 0 | -22.3% | 31 |
| latest print Q3 2020 (2021-01-08 to 2021-02-12) | 6 | -6.5% | -11.1% to -3.2% | 0 | 0 | -4.9% | 6 |
| latest print Q4 2020 (2021-02-19 to 2021-04-23) | 10 | -14.1% | -21.3% to -8.5% | 0 | 0 | -13.3% | 9 |
| latest print Q1 2021 (2021-04-30 to 2021-07-16) | 12 | -27.1% | -38.9% to -17.2% | 0 | 0 | -27.0% | 12 |
| latest print Q2 2021 (2021-07-23 to 2021-10-22) | 14 | -24.7% | -27.2% to -17.0% | 0 | 0 | -21.9% | 0 |
| latest print Q3 2021 (2021-10-29 to 2021-12-31) | 10 | -23.8% | -35.0% to -16.7% | 0 | 0 | -22.2% | 10 |
3y (52 dates with one): 0 of 52 cleared, 0 beat SPY; range -36.6% to +13.1%
1y range -26.5 37.5 excess 2y -41.8 -10.9
drawdown -60.3 -55.8

## What the 2018-2021 labels suggest (hypotheses only)

- The batch is the mirror image of 2014-2017's: the class followed a stale anchor and the gold price ran the other way. FY14's $1.28
  stood for three years while FY2015-FY2019 were all gaps, so 2018-2019 were RICH at 23-35x on every date, and the stock returned a
  median +67% (2018) and +76% (2019) at two years on the 2019-2020 gold run and the Goldcorp and Nevada Gold Mines years: 6 of 96 such
  calls held.
- The same RICH call held on 37 of 46 dates of 2020 (from the Q4 2019 print, after the March 2020 low): entries at $55-69 in mid-2020
  lost 20-30% by mid-2022. A RICH call that is right in 2020 and wrong in 2018-2019 on the same $1.28 is a timing call against the
  metal, as the 2014-2017 findings already say, not a valuation one.
- The only CHEAP dates (15, on FY20's $3.31 at 16-18x) were the batch's worst entries (median -24.7%, 0 of 15 held): FY2020, the
  best gold-price year in the history, became the anchor just as the price peaked. The sensitivity table shows the CHEAP calls sit on
  the signals (BEAR moves 6 of them) and on FY2020 being kept.
- The FAIR dates around the Q3 2019 print (BASE lifted by the Goldcorp quarters' +57% and +45% revenue growth) did well (+51%, 10 of 11
  held); BASE at 0% on those quarters would have made them RICH and wrong. A hindsight-friendly coincidence, not a rule.
- Profile drift: DURABLE then to the FY2018 10-K, CYCLICAL from it (the 10-K's "The metals markets are cyclical"), CYCLICAL in today's
  profile. Label only.
- Hypothesis for a later method version (never this one), the 2014-2017 one again with more weight: for a miner whose GAAP years swing
  between write-downs, tax charges and one-off gains, the rollover anchor goes stale for years (FY14 to February 2021), and the one year
  that passes both tests can be the peak; an anchor that tracks the metal price or production economics, or a cap on an anchor's age,
  would be a new rule, decided before scoring, with a full re-run.
