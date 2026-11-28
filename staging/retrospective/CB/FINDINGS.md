# CB retrospective findings (hindsight)

**Everything below is hindsight.** It is computed from `outcome.json` (prices and dividends after each as-of date, Yahoo's CB series and
SPY), which no model reads. These are hypotheses for the live model, to be tested on other tickers and periods; none may be folded into
the CB archive or any other ticker's models (retro/README.md, "The one rule"). The point-in-time build, its decisions and its judgement
calls are in retro/README.md, "CB"; they were committed and fire-walled before any outcome was computed.

The series is ACE Limited (NYSE: ACE), the company behind today's CB, on 986 weekly dates: 105 from 2008-01-04 to 2009-12-31 (the table
below), 209 from 2010-01-08 to 2013-12-31, 208 from 2014-01-10 to 2017-12-29 (Chubb Limited, NYSE: CB, from 2016-01-15) and 209 from
2018-01-05 to 2021-12-31, and 255 from 2022-01-07 to 2026-11-20 (986 in all), each batch in its own section, scored after its build was
committed, pushed and fire-walled. The
call check is the tool's: CHEAP should clear the 15%/yr hurdle or beat SPY over two years, FAIR should land within ±15pp of SPY, RICH should miss the
hurdle and lag SPY. Judge the series by the return to the average price of months 12-24 and treat the call check as a rough tick
(retro/README.md, "Scoring a single stock").

| | dates | 2-yr total return | vs SPY (mean / median) | to the m12-24 average | call check |
|---|---|---|---|---|---|
| 2008, all | 53 | +4.2% | +2.7 / +4.8pp | -7.3% | 43 of 53 |
| 2008, CHEAP | 47 | +6.5% | +3.0 / +5.1pp | -5.6% | 37 of 47 |
| 2008, FAIR | 6 | -13.4% | +0.8 / +1.1pp | -21.1% | 6 of 6 |
| 2009, all | 52 | +46.5% | +5.6 / +7.0pp | +30.4% | 2 of 52 |
| 2009, CHEAP (January) | 4 | +35.9% | -20.2 / -18.4pp | +17.6% | 2 of 4 |
| 2009, RICH (from the Q4 2008 print) | 48 | +47.4% | +7.8 / +7.1pp | +31.4% | 0 of 48 |
| all | 105 | +25.2% | +4.2 / +5.8pp | +11.4% | 45 of 105 |

## 2008 (53 dates)

- **CHEAP or FAIR on every date, and the stock roughly kept pace with SPY.** Over two years ACE returned +4.2% on average against a falling
  market (+2.7pp over SPY, +4.8pp at the median); over three years +12.8pp. Every 2008 date landed in the BASE scenario. The call check
  hits 43 of 53: the six FAIR dates all land within ±15pp, and 37 of the 47 CHEAP dates beat SPY or clear the hurdle.
- **Buying lower did not help inside the year.** The dates to mid-September (37, at 6.3-8.3x FY2007E $7.325 and then FY07's $7.66) beat
  SPY by +9.0pp on average over two years; the 20 dates from mid-September 2008 to January 2009, with the cheapest multiples of the series
  (5.3-8.6x, mostly 6-7x, under the EPP floor on four dates), lagged it by 13.4pp, because SPY's own rebound from its 2009 low lifted the benchmark more than ACE. The worst two-year excess
  of the series is a CHEAP date in that stretch (2009-01-16, -30.1pp). One stock over a few months mostly tests "buy lower", and here the
  benchmark's path dominates.
- **The FAIR dates were the expensive ones in absolute terms** (-13.4% over two years, -21.1% to the m12-24 average), but they kept pace with
  SPY, so the call holds; the absolute losses came from the 2008-2009 drawdown (-51.8% peak to trough from the 2008-01-04 date).

## 2009 (52 dates)

- **RICH on all 48 dates from the Q4 2008 print, and wrong on all 48.** From 2009-02-05 the model's multiple rests on FY08's GAAP $3.53,
  which carries $1,633M of pre-tax realized losses; at 9.2-15.5x that EPS the stock read RICH against a window median of 9.8-10.7x. ACE then returned
  +47.4% over two years on average (+7.8pp over SPY) and landed in the BULL scenario on every one of these dates. The low of the series,
  2009-03-06 at $32.50 (RICH, AVOID), doubled over two years (+100.5%, +1.9pp over SPY).
- **The four CHEAP dates of January 2009** (still on FY07's $7.66) returned +35.9% but lagged SPY's rebound by 20.2pp: two of four hits.
- **What the point-in-time tests already flagged.** The README's sensitivity test of the EPS basis (the company's operating figure, which
  removes realized gains and losses) moves 44 of the 48 RICH dates to CHEAP. The build chose GAAP by the existing rule (the company's figure
  removes recurring items), before any outcome; on these dates that choice is what made every 2009 call wrong.

## 2008-2009 together (105 dates)

- **The robustness block separated nothing useful.** The 95 dates whose class survives 7 or 8 of the 8 robustness variants hit 35 times;
  the 10 fragile ones (5 FAIR and 5 CHEAP, all from January to June 2008) hit all 10.
- **Legacy tiers:** BUY (41 dates) +0.5pp over SPY on average (+6.0pp median), ACCUMULATE (15) +3.0pp, WATCHLIST (1) -3.0pp, AVOID (48) +7.8pp:
  the AVOID tier, every 2009 date, beat the others.

## 2010-2013 (209 dates)

Scored on 2026-11-21, after the point-in-time build was committed and pushed (e1d3e3d) and the firewall had passed at 25 cutoffs
(e02dc5d). Every date has its 6-month, 1-, 2- and 3-year horizons; the 15%/yr hurdle is +32.2% over two years.

| | dates | 2-yr total return | vs SPY (mean / median) | to the m12-24 average | call check |
|---|---|---|---|---|---|
| 2010, all | 52 | +43.7% | +17.9 / +17.6pp | +28.8% | 40 of 52 |
| 2010, CHEAP | 30 | +46.6% | +19.5 / +20.8pp | +31.5% | 30 of 30 |
| 2010, FAIR | 18 | +37.1% | +12.5 / +14.2pp | +22.6% | 10 of 18 |
| 2010, RICH (January, on FY08's $3.53) | 4 | +51.8% | +30.3 / +32.6pp | +35.6% | 0 of 4 |
| 2011, all | 52 | +46.1% | +11.3 / +10.4pp | +26.8% | 37 of 52 |
| 2011, CHEAP | 18 | +50.2% | +12.4 / +9.4pp | +32.5% | 18 of 18 |
| 2011, FAIR | 34 | +44.0% | +10.7 / +11.2pp | +23.8% | 19 of 34 |
| 2012, all | 52 | +44.7% | -0.1 / -0.5pp | +30.5% | 4 of 52 |
| 2012, FAIR (January) | 4 | +43.5% | -1.0 / -0.7pp | +30.5% | 4 of 4 |
| 2012, RICH (from the Q4 2011 print) | 48 | +44.8% | -0.0 / -0.5pp | +30.5% | 0 of 48 |
| 2013, all | 53 | +25.3% | -4.8 / -4.3pp | +18.2% | 35 of 53 |
| 2013, FAIR | 12 | +20.0% | -3.8 / -3.8pp | +19.2% | 12 of 12 |
| 2013, RICH | 41 | +26.8% | -5.1 / -5.9pp | +17.9% | 23 of 41 |
| class CHEAP | 48 | +47.9% | +16.8 / +20.2pp | +31.9% | 48 of 48 |
| class FAIR | 68 | +37.9% | +8.0 / +8.2pp | +23.1% | 45 of 68 |
| class RICH | 93 | +37.2% | -1.0 / -1.1pp | +25.1% | 23 of 93 |
| all | 209 | +39.9% | +6.0 / +2.9pp | +26.0% | 116 of 209 |

- **The classes and the tiers ordered the relative outcomes.** Against SPY over two years: CHEAP +16.8pp, FAIR +8.0pp, RICH -1.0pp; over
  three years +21.9pp, +10.9pp and +4.5pp; over one year +7.4pp, +5.8pp and +0.5pp. The legacy tiers fall in order too: BUY (19 dates)
  +24.1pp, ACCUMULATE (56) +12.0pp, WATCHLIST (41) +5.4pp, AVOID (93) -1.0pp, unlike 2008-2009, when the AVOID tier beat the others. Every
  CHEAP date (48 of 48) beat SPY.
- **In absolute terms everything rose,** so the call check fails most RICH dates: the RICH dates returned +37.2% over two years and cleared
  the hurdle on 62 of 93. ACE's two-year return is positive on every date (+10.5% to +64.3%, under +20% only on 15 dates of the second
  half of 2013); its largest drawdown within two years averages -13%.
- **2010-2011: CHEAP and FAIR on the anchors FY09's $7.55 and FY10's $9.11 (6.4-8.2x),** and the stock beat SPY by +17.3pp (dates on
  FY09) and +9.5pp (on FY10) on average; the 25 CHEAP dates of February to July 2010, under or near the EPP floor, beat it by +21.5pp. The
  FAIR misses (8 of 18 in 2010, 15 of 34 in 2011) are all dates that beat SPY by more than 15 points (+15.3 to +24.2pp).
- **2012: RICH on all 48 dates from the Q4 2011 print, on FY11's $4.65 (15-18x).** ACE then returned +44.8% over two years, exactly SPY's
  +44.8%: in relative terms the call was neither right nor wrong, but the stock cleared the hurdle on every date, so the check scores 0 of
  48. FY2011's GAAP EPS carries $791M of realized losses after tax and the year's $859M of pre-tax catastrophe losses; the multiple on it
  was a trough multiple, as in 2009.
- **2013: RICH on 41 dates and FAIR on 12, on FY12's $7.89 (10.8-13.1x),** the 63rd-73rd percentile. The RICH dates of January to July
  lagged SPY by 8.3pp (19 of 25 hits); those of October to December kept pace (+0.5pp, 4 of 12). The 12 FAIR dates from the Q2 2013 print
  landed within 9 points of SPY (-8.6 to +0.7pp).
- **The trough-anchored RICH call was again the biggest miss:** the lowest price of the batch, 2010-01-08 at $47.50 (RICH, AVOID, on
  FY08's $3.53), is its best two-year excess (+36.6pp, +52.3%), as 2009-03-06 was in the first batch.
- **Robustness again separated nothing.** The 159 dates whose class survives 7 or 8 of the 8 robustness variants hit 77 times (48%); the
  50 fragile ones (45 of them FAIR) hit 39 (78%).
- **Scenario landing:** RICH dates landed in BULL on 92 of 93; CHEAP dates in BASE on all 48; FAIR in BASE on 53 and BULL on 15. Never near
  BEAR ($4.95-11.14) or XBULL.

## 2014-2017 (208 dates)

Scored on 2026-11-21, after the point-in-time build was committed and pushed (10e94201) and the firewall had passed at 27 cutoffs
(58f0f57b), in a session that had not opened this file or any CB outcome before. Every date has its 6-month, 1-, 2- and 3-year horizons;
the 15%/yr hurdle is +32.2% over two years. The text-only correction to 2010-2012 in the same build changed no class, tier or outcome above.

| | dates | 2-yr total return | vs SPY (mean / median) | to the m12-24 average | call check |
|---|---|---|---|---|---|
| 2014, all | 51 | +24.1% | +11.5 / +12.5pp | +10.9% | 30 of 51 |
| 2014, FAIR | 39 | +25.6% | +12.5 / +13.1pp | +11.3% | 30 of 39 |
| 2014, RICH (January, and October-December) | 12 | +19.2% | +8.4 / +7.6pp | +9.4% | 0 of 12 |
| 2015, RICH (every date) | 53 | +35.1% | +11.9 / +11.7pp | +21.3% | 2 of 53 |
| 2016, all | 52 | +14.8% | -20.9 / -20.9pp | +15.3% | 12 of 52 |
| 2016, RICH (to the Q1 2016 print) | 17 | +27.5% | -14.3 / -14.5pp | +24.2% | 12 of 17 |
| 2016, CHEAP (from the Q1 2016 print) | 35 | +8.7% | -24.2 / -24.9pp | +11.0% | 0 of 35 |
| 2017, all | 52 | +7.1% | -16.0 / -17.1pp | -3.5% | 36 of 52 |
| 2017, CHEAP (to the Q1 2017 print) | 16 | +3.8% | -18.7 / -19.0pp | -1.2% | 0 of 16 |
| 2017, RICH (from the Q1 2017 print) | 36 | +8.6% | -14.8 / -15.8pp | -4.6% | 36 of 36 |
| class CHEAP | 51 | +7.1% | -22.5 / -22.7pp | +7.2% | 0 of 51 |
| class FAIR | 39 | +25.6% | +12.5 / +13.1pp | +11.3% | 30 of 39 |
| class RICH | 118 | +24.3% | -0.4 / +4.6pp | +12.6% | 50 of 118 |
| all | 208 | +20.3% | -3.4 / -5.4pp | +11.0% | 80 of 208 |

- **The merger quarters' CHEAP calls were all wrong.** From the Q1 2016 print to the Q1 2017 print (51 dates) the model read CHEAP, BUY on
  42, only because BASE took the quarter's reported revenue growth with The Chubb Corporation in against a year-ago ACE alone (+56-75%),
  while the multiple sat at the 81st-94th percentile of its window. The stock then returned +7.1% over two years and lagged SPY by 22.5pp
  on average (0 of 51 hits; over three years -21.3pp); its two-year price ($123.44-140.08) never came near the BASE case ($197-306). The
  worst two-year excess of the batch is one of them (2016-06-24, $123.94: +6.3%, -33.6pp). The README's sensitivity test (BASE on the
  quarter's revenue growth per diluted share) turns all 51 to RICH, which would have hit on all 51: 131 hits for the batch instead of 80.
- **2014: FAIR on FY13's $10.92 (8.7-10.6x) beat SPY by 12.5pp.** The 39 FAIR dates hit 30 times; the misses beat SPY by more than 15
  points. The 12 RICH dates (the three of January on FY12's $7.89, the nine of October-December as the price passed $109) also beat SPY
  (+8.4pp) and missed on all 12.
- **2015: RICH on every date, on FY14's $8.42 (11.9-14.0x against a window median of 9.0x), and the stock beat SPY by 11.9pp** (+35.1%
  over two years, cleared the hurdle on 32 of 53; 2 hits). FY2014's GAAP EPS carries $467M of realized losses after tax, but the
  company's operating $9.79 reads RICH as well: the window's median, which holds the low multiples of 2008-2011, was the anchor that
  missed, as the stock re-rated from 8.7-10.6x in 2014 to 12-17x in 2015-2017.
- **2017: RICH from the Q1 2017 print and right on all 36:** at 15.4-17.4x FY16's $8.87 (the 91st-99th percentile) the stock returned
  +8.6% over two years against SPY's +23.4% (-44.6pp over three years on average). The highest price of the batch,
  2017-10-20 at $154.00, lagged SPY by 17.0pp.
- **The classes did not order the relative outcomes this time:** against SPY over two years CHEAP -22.5pp, FAIR +12.5pp, RICH -0.4pp (over
  three years -21.3pp, +13.4pp and -20.0pp); the legacy tiers BUY (42 dates) -21.6pp, ACCUMULATE (27) -0.6pp, WATCHLIST (34) +10.3pp,
  AVOID (105) -1.2pp. The disorder is the merger quarters: every CHEAP and BUY date is one of them, and without them the order holds
  (FAIR +12.5pp over RICH -0.4pp; ACCUMULATE's 18 dates of 2014 +12.4pp).
- **In absolute terms the stock rose from every date** but one (2016-12-23, -1.4%; up to +50.1% over two years; the largest drawdown within two years
  averages -16.5%). The lowest price of the batch, 2014-01-24 at $92.19 (RICH, on FY12's $7.89), beat SPY by 14.0pp; the best two-year
  excess is a 2015 RICH date (2015-07-17, $104.14: +45.0%, +25.2pp).
- **Robustness again separated nothing:** the 195 dates whose class survives 7 or 8 of the 8 robustness variants hit 71 times (36%); the 13
  fragile ones, all FAIR, hit 9 (69%).
- **Scenario landing:** RICH dates landed in BULL on 105 of 118 (BASE on 13); FAIR in BASE on all 39; the CHEAP dates' two-year price sat
  far under BASE, nearer BASE on 25 and nearer BEAR ($10-11) on 26.

## 2018-2021 (209 dates)

Scored on 2026-11-21, after the point-in-time build was committed and pushed (8decfb02) and the firewall had passed at 26 cutoffs
(a8fc6d3a). This batch was decided in the session that scored 2014-2017 (retro/README.md, "CB 2018-2021"); no rule was changed. Every
date has its 6-month, 1-, 2- and 3-year horizons; the 15%/yr hurdle is +32.2% over two years.

| | dates | 2-yr total return | vs SPY (mean / median) | to the m12-24 average | call check |
|---|---|---|---|---|---|
| 2018, RICH (every date) | 52 | +1.4% | -19.8 / -19.5pp | +4.3% | 52 of 52 |
| 2019, RICH (every date) | 52 | +21.7% | -28.3 / -27.5pp | +1.3% | 49 of 52 |
| 2020, all | 53 | +60.5% | +27.7 / +30.7pp | +46.8% | 12 of 53 |
| 2020, CHEAP (March-May) | 6 | +112.1% | +44.1 / +44.7pp | +80.2% | 6 of 6 |
| 2020, FAIR (March-April) | 3 | +78.4% | +17.8 / +17.0pp | +51.5% | 1 of 3 |
| 2020, RICH | 44 | +52.3% | +26.2 / +32.5pp | +41.9% | 5 of 44 |
| 2021, RICH (every date) | 52 | +23.8% | +20.5 / +19.0pp | +18.2% | 0 of 52 |
| class CHEAP | 6 | +112.1% | +44.1 / +44.7pp | +80.2% | 6 of 6 |
| class FAIR | 3 | +78.4% | +17.8 / +17.0pp | +51.5% | 1 of 3 |
| class RICH | 200 | +23.7% | -1.4 / -10.7pp | +15.4% | 106 of 200 |
| all | 209 | +27.0% | +0.2 / -7.5pp | +17.8% | 113 of 209 |

- **2018-2019: RICH on every date, and right on 101 of 104.** At 15-19x FY17's $8.19 and FY18's $8.49 (the 79th-100th percentile) the stock
  lagged SPY by 19.8pp (2018 dates) and 28.3pp (2019 dates) over two years; the 2018 dates' two years end in the 2020 drawdown (+1.4% on
  average). The worst two-year excess of the batch is one of them (2019-08-09, $159.62: +14.0%, -41.5pp). Unlike 2015, the high
  percentile was right here.
- **March-May 2020: the crash dates were the right calls.** The six CHEAP dates (10.2-11.2x FY19's $9.71, under the EPP floor on five)
  returned +112.1% over two years and beat SPY by 44.1pp (6 of 6); the lowest price of the batch, 2020-05-15 at $99.49 (CHEAP), is its best
  two-year excess (+114.0%, +69.7pp). The three FAIR dates beat SPY by 17.8pp (1 of 3 within the band). 2020-04-23, RICH at $104.08 under
  the floor because the Q1 2020 print's realized losses cut BASE, beat SPY by 47.4pp.
- **From late May 2020 and through 2021: RICH and wrong on all 85 dates.** From 2020-05-22 (on FY19's $9.71) and from the Q4 2020 print (on
  FY20's $7.79, a year carrying the $1,193M after-tax COVID-19 charge, at 20-25x, the 95th-100th percentile) the stock beat SPY by 36.1pp
  and 18.5pp over two years (0 hits on 33 and 48 dates; the four January 2021 dates, on FY19, beat it by 44.4pp). The README's test of
  FY2020 without its COVID-19 charge ($10.42, derived) moves 13 of the 2021 dates to FAIR, of which 4 would land within the ±15pp band:
  117 hits for the batch instead of 113.
- **The classes ordered the relative outcomes:** CHEAP +44.1pp, FAIR +17.8pp, RICH -1.4pp against SPY over two years (over three years
  +39.6pp, +18.4pp and +5.1pp). The legacy tiers: ACCUMULATE (2 dates) +22.4pp, WATCHLIST (7) +39.0pp, AVOID (200) -1.4pp.
- **The RICH class was right in one half and wrong in the other:** 101 hits on the 104 dates of 2018-2019, 5 on the 96 of 2020-2021 (the
  10 RICH dates of January-March 2020 hit 5 times). Two-year returns range from -25.1% to +116.8%; the largest drawdown within two years
  averages -31.1% (the 2020 crash sits in most windows).
- **Robustness again separated little:** the 203 dates whose class survives 7 or 8 of the 8 robustness variants hit 110 times (54%); the 6
  fragile ones (3 FAIR, 2 CHEAP, 1 RICH) hit 3.
- **Scenario landing:** RICH dates landed in BULL on 183 of 200 (BASE on 17); the CHEAP and FAIR dates all in BULL.

## 2022-2026 (255 dates)

Scored on 2026-11-21, after the point-in-time build was committed and pushed (ee7523b7) and the firewall had passed at 32 cutoffs
(949117da). The batch was built in a new session that had not opened this file or any outcome (retro/README.md, "CB 2022-2026"); no rule
was changed. Not every date has every horizon yet: 150 have the 2-year horizon (to 2024-11-15), 202 the 1-year (to 2025-11-14), 228 the
6-month (to 2026-05-15), and 2026-11-20 has none. The 15%/yr hurdle is +32.2% over two years. The table counts dates with a 2-year
outcome ("15 of 21" means 15 of the year's 21 RICH dates).

| | dates | 2-yr total return | vs SPY (mean / median) | to the m12-24 average | call check |
|---|---|---|---|---|---|
| 2022, CHEAP (from the Q4 2021 print) | 48 | +36.5% | -3.1 / -2.0pp | +16.6% | 40 of 48 |
| 2022, RICH (January) | 4 | +22.2% | +13.5 / +13.7pp | +5.3% | 0 of 4 |
| 2023, CHEAP | 1 | +25.4% | -29.0 / -29.0pp | +21.4% | 0 of 1 |
| 2023, FAIR (January) | 3 | +21.0% | -31.5 / -31.0pp | +17.2% | 0 of 3 |
| 2023, RICH (from the Q4 2022 print) | 48 | +42.3% | -5.3 / -6.7pp | +36.0% | 7 of 48 |
| 2024, CHEAP | 9 | +34.7% | -5.9 / -7.2pp | +18.6% | 7 of 9 |
| 2024, FAIR | 22 | +29.2% | -9.3 / -11.1pp | +14.5% | 15 of 22 |
| 2024, RICH | 15 of 21 | +26.0% | -12.8 / -15.9pp | +14.7% | 11 of 15 |
| class CHEAP | 58 of 82 | +36.1% | -4.0 / -2.2pp | +17.0% | 47 of 58 |
| class FAIR | 25 of 94 | +28.2% | -12.0 / -11.9pp | +14.8% | 15 of 25 |
| class RICH | 67 of 79 | +37.5% | -5.8 / -8.0pp | +29.4% | 18 of 67 |
| all | 150 of 255 | +35.4% | -6.2 / -6.3pp | +22.2% | 80 of 150 |

- **2022: CHEAP on FY21's $19.27, and right by the hurdle on 40 of 48.** FY21 carried $3,023M of after-tax realized gains (the company's
  $12.56). At 9.4-11.9x it read CHEAP, under the EPP floor on 46 dates. The stock returned +36.5% over two years, clearing the hurdle on
  most dates, but lagged SPY by 3.1pp. The year's best two-year excess is in this block (2022-08-05, $185.32: +49.0%, +20.7pp). The four
  RICH dates of January, at 25x FY20's COVID-year $7.79, beat SPY by 13.5pp (0 of 4).
- **2023: RICH on FY22's $12.55 (then $12.39 as adjusted), and wrong by the call check on 41 of 48.** FY22 carried $1,087M of after-tax
  realized losses (the company's $15.24). At 15-19.5x, the 54th-98th percentile, the stock returned +42.3% over two years: it cleared
  the hurdle, though it lagged SPY by 5.3pp. Hypothesis 4's case: a RICH call that lags SPY still misses when the stock clears 15%/yr.
  The three FAIR dates of January 2023 (on FY21's $19.27, at $227-229) are the worst of the batch:
  -31.5pp, with 2023-01-06 at -37.1pp.
- **2024: on FY23's $19.06 from the Q4 2023 print (the four January dates, RICH, still on FY22's $12.39), the classes ordered the
  relative returns.** CHEAP -5.9pp, FAIR -9.3pp and RICH -12.8pp against SPY over two
  years, with 33 of 46 hits. The company's figure excluding the Bermuda benefit was the better anchor here: FY23 at GAAP $21.80 (the
  README's variant) reads 29 more dates CHEAP and 4 RICH dates FAIR, and would have hit 22 of 46 instead of 33.
- **2025 (1-year horizon only so far):** CHEAP +8.4pp (13 dates), FAIR -3.8pp (32), RICH -1.8pp (1) against SPY over one year.
- **Over the batch the classes did not order the 2-year excess:** CHEAP -4.0pp, FAIR -12.0pp, RICH -5.8pp. SPY's two years from 2022-2024
  were strong, and every class lagged it on average (all dates -6.2pp) while clearing the hurdle on average (+35.4%). The legacy tiers:
  BUY -1.0pp (40 dates), ACCUMULATE -18.8pp (13), WATCHLIST -8.3pp (30), AVOID -5.8pp (67). Two-year returns range from +15.9% to +65.9%;
  the largest drawdown within two years averages -16.5%.
- **Robustness did not predict hits again:** the 101 dates whose class survives 7 or 8 of the 8 variants hit 48 times (48%), the 49
  fragile ones 32 times (65%).
- **Scenario landing:** CHEAP and FAIR dates landed in BASE on all 83; RICH dates in BULL on 59 of 67 (BASE on 8).

## 2008-2024: the EPS basis, tested on later dates

The 2008-2009 findings proposed that the company's operating EPS (which removes realized gains and losses) would have served an insurer
better than GAAP. The 2010-2013 dates were not scored when that was written, so they test it. Each of the 314 dates was rebuilt on the
operating basis (every year at the company's figure, every operating range as the guide: the README's sensitivity variant) and scored
by the same call check against the same outcomes (hindsight, this file only):

| | dates | GAAP hits | operating hits | classes moved | mean 2-yr excess of the moved dates |
|---|---|---|---|---|---|
| 2008 | 53 | 43 | 42 | 5 | +1.6pp |
| 2009 | 52 | 2 | 49 | 47 | +7.9pp |
| 2010 | 52 | 40 | 38 | 15 | +14.3pp |
| 2011 | 52 | 37 | 0 | 48 | +10.4pp |
| 2012 | 52 | 4 | 0 | 4 | -1.0pp |
| 2013 | 53 | 35 | 34 | 12 | -3.8pp |
| 2014 | 51 | 30 | 0 | 39 | +12.5pp |
| 2015 | 53 | 2 | 2 | 0 | |
| 2016 | 52 | 12 | 12 | 0 | |
| 2017 | 52 | 36 | 36 | 0 | |
| 2018 | 52 | 52 | 52 | 0 | |
| 2019 | 52 | 49 | 49 | 0 | |
| 2020 | 53 | 12 | 9 | 3 | +65.4pp |
| 2021 | 52 | 0 | 0 | 0 | |
| 2022 | 52 | 40 | 8 | 48 | -3.1pp |
| 2023 | 52 | 7 | 30 | 36 | -4.6pp |
| 2024 | 46 | 33 | 28 | 13 | -9.9pp |
| all | 881 | 434 | 389 | 270 | |

- **The operating basis wins 2009 by 47 calls and loses 2011 by 37: over six years the two tie (161 against 163).** In 2011 the operating
  guides ($5.40-6.75) sat well under GAAP FY10's $9.11 (a year with $451M of realized gains), so the operating basis read RICH on 48
  dates that then beat SPY by 10.4pp. In 2012, the year after the catastrophe year, both bases read RICH.
- **2014-2017 (scored after their build, the same variant): the operating basis loses 30 calls in 2014 and moves nothing after it.** In
  2014 the company's FY13 $9.35 (GAAP $10.92 with $541M of realized gains after tax) reads RICH on 39 dates that then beat SPY by 12.5pp;
  from 2015 both bases read the same class. Over 522 dates GAAP now leads, 241 hits against 213.
- **2018-2021: the bases agree on all but 3 dates** (the operating basis reads three CHEAP dates of the 2020 crash RICH, and they beat SPY
  by 65.4pp); both read 2021 RICH on a COVID year (operating FY20 $7.31). Over 731 dates GAAP leads, 354 hits against 323.
- **2022-2024 (scored after their build; the variant is the README's core basis, FY23 and FY24 at the company's core figures excluding the
  tax benefits): the bases split again, 80 hits against 66.** The core basis reads 2022's 48 CHEAP dates RICH (FY21 $12.56 against GAAP
  $19.27) and loses 32 calls, because the stock cleared the hurdle. It reads 32 of 2023's RICH dates FAIR or CHEAP (FY22 $15.24 against
  $12.55) and wins 23. Over 881 scored dates GAAP leads, 434 hits against 389. In 2022-2023 both bases ordered nothing: the two years'
  absolute returns were alike (+36.5% and +42.3%) while the GAAP class flipped from CHEAP to RICH with the anchor.
- **Both bases order the relative returns in 2010-2013** (GAAP: CHEAP +16.8pp, FAIR +8.0pp, RICH -1.0pp; operating: CHEAP +22.7pp on 29
  dates, FAIR +15.0pp on 21, RICH +1.8pp on 159). Over 2008-2013 GAAP gives +8.8, +7.4 and +2.0pp, operating +8.3, +13.3 and +1.8pp.

## Hypotheses (for other tickers and periods, never for this archive)

1. **A GAAP trough year built on realized investment losses makes an insurer look expensive exactly when it is cheap.** The rule that
   rejects the company's operating figure (it removes recurring items) is sound for recurring amortization, but for an insurer in a market
   crash the realized losses are recurring in kind yet reversing in fact: 2009's RICH calls on GAAP were wrong 48 times in 48. JPM's 2009
   (GAAP FY08 after the markdowns) is the same pattern on a bank; a test across financials, on dates not yet scored, would say whether this
   is a rule worth a new method version (it would need one, and a full re-run, with the reason recorded).
   **2010-2013 weakens it** (above): the operating basis would have fixed 2009 and broken 2011, and the two tie over 314 dates. What
   the misses share is narrower: the multiple is set on the single year after a trough (FY08 in 2009 and January 2010, FY11 in 2012),
   whichever basis is used. A hypothesis to test elsewhere: an insurer's anchor needs more than one year (an average of several years'
   EPS, or book value) rather than a different one-year figure. **2014-2017 weakens the operating basis again** (30 calls lost in 2014,
   none gained), and its RICH misses of 2015 are a different failure: not a trough year but a window median set by low past multiples
   while the stock re-rated (hypothesis 7). **2018-2021 adds another trough-year anchor:** FY2020, cut by the COVID-19 charge, set
   every 2021 multiple at 20-25x, and all 48 RICH calls on it missed (the stock beat SPY by 18.5pp). FY2008 (2009), FY2011 (2012) and
   FY2020 (2021), each a year of market or catastrophe losses, anchor the series' largest blocks of RICH misses, on either basis.
   **2022-2023 shows the mirror:** FY2021, lifted by $3,023M of after-tax realized gains, read 2022 CHEAP, and FY2022, cut by $1,087M of
   realized losses, read 2023 RICH. The stock returned +36.5% and +42.3% over the two blocks' two years: the class followed a one-year
   anchor swinging on realized items in both directions, and the outcome did not swing with it. The multi-year anchor hypothesis is the one
   this supports; the operating basis alone would have traded 2022's calls for 2023's.
2. **On a financial, book value may be the better anchor in a crisis.** ACE's book value per share fell 11.4% in 2008 while its GAAP EPS fell 54%; a
   price-to-book cross-check was not part of method r2 and was not computed here.
3. **A rebounding benchmark punishes the cheapest dates.** The late-2008 CHEAP dates lagged SPY by 13pp despite a positive absolute return;
   the relative call check penalises defensive names bought at the market's trough.
4. **In a rising market the RICH call check is unwinnable.** 2012's 48 RICH dates matched SPY exactly (+44.8%) and still scored 0 of 48,
   because the stock cleared the 15%/yr hurdle. The relative ordering (CHEAP > FAIR > RICH against SPY, and BUY > ACCUMULATE >
   WATCHLIST > AVOID in 2010-2013) is the better test of the classes than the hit count. 2023's 48 RICH dates lagged SPY by 5.3pp and
   scored 7 of 48, because the stock cleared the hurdle.
5. **Robustness agreement did not predict hits in any batch** (2008-2009: 35 of 95 robust, 10 of 10 fragile; 2010-2013: 77 of 159
   robust, 39 of 50 fragile; 2014-2017: 71 of 195 robust, 9 of 13 fragile; 2022-2024: 48 of 101 robust, 32 of 49 fragile). On this series the fragile dates are mostly FAIR, and FAIR's
   ±15pp band is the easiest to hit.
6. **An acquisition "as published" inflates BASE for four quarters and buys the wrong class.** Method r2 takes the latest quarter's reported
   revenue growth; when that quarter holds an acquired company against a year-ago quarter without it, BASE carries the deal (here +56-75%,
   paid for with 137 million new shares and $14.3 billion of cash), and every one of CB's 51 such dates read CHEAP and lagged SPY by 22.5pp.
   Revenue growth per diluted share would have read RICH on all 51 and hit on all 51. Other series in staging have acquisition quarters
   in BASE as published (the README records the rule's earlier uses); a test there, on dates scored without this result, would say
   whether a per-share or organic reading deserves a new method version (it would need one, and a full re-run, with the reason recorded).
7. **A window median set by past low multiples reads a re-rated stock as RICH for years.** CB traded at 5-9x its anchor EPS on most dates
   of 2008-2011 (the trough years' multiples aside) and at 12-17x from 2015; the ten-year median rose only from 9.0x (2015) to 11.8-12.4x
   (2017), so 2015's 53 RICH dates beat SPY by 11.9pp while 2017's, at the 91st-99th percentile, lagged it by 14.8pp. Whether the
   percentile of a multiple says more once the window no longer holds the crisis years (the CB window leaves 2008-2009 only from
   2018-2019) is a test for later dates of this series and for others. **2018-2019 answers it for this series in part:** with the median
   at 12.4-13.4x, the 79th-100th percentile read RICH and was right on 101 of 104 dates.
8. **A company figure excluding only a one-off tax benefit may be the better anchor** (one test, one ticker). The README's rule took FY2023
   at the company's $19.06 rather than GAAP $21.80, which carried Bermuda's one-time $1.14 billion deferred tax benefit; on the 46 scored
   dates of 2024 it hit 33 times against the GAAP reading's 22. The rule was decided before the outcomes and is unchanged; a test on other
   tickers' tax-law years (the 2017 Tax Act's benefits in particular, read at GAAP where no figure excludes only them) would say more.
