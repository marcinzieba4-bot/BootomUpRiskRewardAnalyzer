# JPM retrospective findings (hindsight)

Patterns seen in `outcome.json` for the JPM weekly dates (JPMorgan Chase & Co., NYSE: JPM): 731 in all, 105 from 2008-01-04 to 2009-12-31,
209 from 2010-01-08 to 2013-12-31, 208 from 2014-01-10 to 2017-12-29 and 209 from 2018-01-05 to 2021-12-31 (the later sections below). They are
**labels and hypotheses**: never feed them back into the method or the fact sheet. The outcomes were computed on 2026-11-19, after the
point-in-time build and its one text correction were committed (735d7d4, ed681b3) and the firewall had passed at 16 cutoffs; the build
was not yet pushed when they were computed. Every date has its 6-month, 1-, 2- and 3-year horizons. Total returns include dividends
($0.38 a quarter to February 2009, $0.05 after). Medians of an even count are the mean of the two middle values. The 15%/yr hurdle is
+32.2% over two years. "Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY); FAIR should land
within 15 points of the benchmark; RICH should miss the hurdle and lag the benchmark.

## 2008-2009 (105 dates)

| Group | Dates | Mean 2-yr total return | Median | Mean vs SPY | Beat SPY | Cleared hurdle | Mean m12-24 avg price | Mean max drawdown | Call held |
|---|---|---|---|---|---|---|---|---|---|
| all | 105 | +14.6% | +4.0% | -6.4pp | 50 | 22 | +12.8% | -49.0% | 75 |
| 2008 | 53 | +6.2% | +1.4% | +4.7pp | 38 | 5 | +3.1% | -65.2% | 39 |
| 2008, CHEAP | 25 | +16.7% | +13.4% | +6.0pp | 16 | 5 | +16.4% | -62.7% | 20 |
| 2008, FAIR | 18 | +0.1% | -0.4% | +12.8pp | 18 | 0 | -8.6% | -68.1% | 13 |
| 2008, RICH | 10 | -9.3% | -9.6% | -13.2pp | 4 | 0 | -9.1% | -66.1% | 6 |
| 2009 | 52 | +23.1% | +16.8% | -17.7pp | 12 | 17 | +22.7% | -32.4% | 36 |
| 2009, CHEAP (2009-01-09) | 1 | +69.6% | +69.6% | +21.9pp | 1 | 1 | +55.4% | -42.5% | 1 |
| 2009, RICH | 51 | +22.2% | +16.4% | -18.5pp | 11 | 16 | +22.0% | -32.2% | 35 |
| tier BUY | 17 | +26.7% | +20.8% | +4.4pp | 9 | 6 | +25.6% | -59.2% | 13 |
| tier ACCUMULATE | 29 | -2.1% | -2.1% | +0.1pp | 21 | 0 | -2.3% | -63.4% | 25 |
| tier WATCHLIST | 20 | -12.3% | -13.3% | -13.5pp | 9 | 0 | -10.8% | -56.9% | 14 |
| tier AVOID | 39 | +35.4% | +25.3% | -12.3pp | 11 | 16 | +30.5% | -29.7% | 23 |

What the labels say, as hypotheses only:

- **2008: the class ordered the outcomes.** CHEAP dates returned a mean +16.7% over two years, FAIR +0.1%, RICH -9.3%; against SPY,
  +6.0, +12.8 and -13.2 points. Every 2008 date still had a drawdown of 50% to 68% inside its two years: the classes ranked entries, they
  did not avoid the fall. One stock over one year mostly tests "buy lower" (retro/README.md, "Scoring a single stock").
- **2009: the RICH call missed the recovery in absolute terms and held against the index.** All 51 dates from the Q4 2008 print are
  RICH, because the price is measured against FY08's $0.92. They returned a mean +22.2% over two years, 16 cleared the hurdle, and the 39
  AVOID dates returned +35.4%; the series low, 2009-03-06 at $15.93, is RICH and AVOID and returned +188% (+90 points against SPY). Yet
  40 of the 51 lagged SPY over two years, which is why "call held" reads 35 of 51: by the scoring rule a RICH call holds when the stock
  lags the benchmark or misses the hurdle.
- **The 2009 miss is the trough-year anchor.** With no EPS guide the last full year stands, so a year whose earnings fell 79% makes the
  multiple look high at the bottom of the price. A hypothesis
  for the live model: a P/E rule on last-year EPS reads a bank's credit trough as expensive.
- **Scenario landing:** the price two years on sat in the BASE band on 69 dates and the BULL band on 36, and never near BEAR, whose
  price was $8-9 in 2008 and $0.41 in 2009.
- **Three-year horizon:** a mean +13.1% for the 105 dates, 20.8 points behind SPY: over three years the stock lagged the index from
  most entries of both years.

Not tested here: whether any of this holds for other banks or other periods. One bank through one crisis is one observation.

## 2010-2013 (209 dates)

Scored on 2026-11-19, after the point-in-time build was committed (808e6a7) and the firewall had passed at 25 cutoffs; the build was
not yet pushed when the outcomes were computed. Every date has its 6-month, 1-, 2- and 3-year horizons. Dividends are $0.05 a quarter
to March 2011, then $0.25, $0.30 (2012) and $0.38 (from mid-2013).

| Group | Dates | Mean 2-yr total return | Median | Mean vs SPY | Beat SPY | Cleared hurdle | Mean m12-24 avg price | Mean max drawdown | Call held |
|---|---|---|---|---|---|---|---|---|---|
| all | 209 | +32.0% | +30.0% | -1.8pp | 104 | 97 | +17.9% | -27.4% | 166 |
| 2010 | 52 | +0.9% | +2.5% | -24.8pp | 0 | 0 | -6.8% | -40.9% | 36 |
| 2010, CHEAP | 13 | -1.1% | -1.4% | -26.2pp | 0 | 0 | -8.6% | -40.9% | 0 |
| 2010, FAIR | 3 | -6.2% | -10.0% | -35.4pp | 0 | 0 | -0.8% | -40.9% | 0 |
| 2010, RICH | 36 | +2.2% | +5.7% | -23.4pp | 0 | 0 | -6.6% | -40.9% | 36 |
| 2011 | 52 | +42.1% | +38.8% | +7.3pp | 32 | 30 | +18.8% | -35.5% | 35 |
| 2011, CHEAP | 49 | +44.2% | +40.1% | +8.4pp | 32 | 30 | +20.7% | -35.2% | 32 |
| 2011, FAIR | 2 | +7.5% | +7.5% | -12.2pp | 0 | 0 | -13.6% | -40.1% | 2 |
| 2011, RICH (2011-01-07) | 1 | +9.1% | +9.1% | -10.2pp | 0 | 0 | -9.8% | -40.9% | 1 |
| 2012 | 52 | +56.3% | +56.5% | +11.6pp | 44 | 52 | +42.5% | -19.4% | 52 |
| 2012, CHEAP | 44 | +58.2% | +58.5% | +12.5pp | 38 | 44 | +45.0% | -18.8% | 44 |
| 2012, FAIR | 8 | +45.7% | +46.1% | +6.6pp | 6 | 8 | +28.9% | -22.6% | 8 |
| 2013 | 53 | +28.7% | +28.3% | -1.3pp | 28 | 15 | +17.0% | -14.1% | 43 |
| 2013, CHEAP | 27 | +29.8% | +28.4% | -3.9pp | 12 | 10 | +20.0% | -14.0% | 17 |
| 2013, FAIR | 26 | +27.6% | +27.5% | +1.4pp | 16 | 5 | +14.0% | -14.2% | 26 |
| class CHEAP | 133 | +41.5% | +39.7% | +3.9pp | 82 | 84 | +25.7% | -26.0% | 93 |
| class FAIR | 39 | +27.7% | +28.5% | -1.0pp | 22 | 13 | +14.5% | -19.3% | 36 |
| class RICH | 37 | +2.4% | +6.1% | -23.1pp | 0 | 0 | -6.7% | -40.9% | 37 |
| tier BUY | 43 | +64.1% | +68.0% | +18.3pp | 39 | 39 | +48.7% | -26.7% | 39 |
| tier ACCUMULATE | 68 | +35.3% | +37.0% | -1.2pp | 38 | 46 | +19.4% | -25.4% | 48 |
| tier WATCHLIST | 62 | +23.0% | +24.6% | -4.2pp | 27 | 12 | +9.1% | -22.2% | 43 |
| tier AVOID | 36 | +2.9% | +6.2% | -22.8pp | 0 | 0 | -6.5% | -40.9% | 36 |

What the labels say, as hypotheses only:

- **Over the four years the classes and the tiers both ordered the outcomes.** CHEAP +41.5% over two years (+3.9 points against SPY),
  FAIR +27.7% (-1.0), RICH +2.4% (-23.1); BUY +64.1%, ACCUMULATE +35.3%, WATCHLIST +23.0%, AVOID +2.9%. None of the 37 RICH dates and
  none of the 36 AVOID dates beat SPY or cleared the hurdle.
- **Most of that ordering is the calendar year.** The class is set mainly by which year's EPS anchors the multiple: RICH is 2010 (36
  of its 37 dates), CHEAP is mostly 2011-2012 (93 of 133). Inside a year the split is thin or reversed: in 2010 the 13 CHEAP dates
  (the Q4 2009 print, January to April) did no better than the 36 RICH ones (-1.1% against +2.2%), and all 16 CHEAP and FAIR calls of
  2010 failed; in 2013 CHEAP and FAIR are level (+29.8% and +27.6%), and CHEAP lagged SPY by 3.9 points.
- **2010 is the mirror of 2009.** In 2009 the trough year made the stock read RICH at the low and the calls missed a recovery; in 2010
  the anchor moved up to FY09's $2.32, the reading stayed RICH on 36 dates, and this time every one of them lagged SPY (-23.4 points
  on average) through the 2011 fall. The same mechanism was wrong at the bottom and right a year later: one stock cannot tell a rule
  from a coincidence.
- **2011-2012 CHEAP on 7-12x was followed by strong returns,** +44.2% and +58.2% over two years, with every 2012 date clearing the
  hurdle. The 2011 entries still fell a further 35% on average before that (the low of October 2011).
- **Scenario landing:** BASE on 173 dates and BULL on 36; never near BEAR ($0.91-1.66) or XBULL (about $700). The two outer scenarios,
  both products of the 2008 trough year, described nothing that happened.
- **Three-year horizon:** a mean +52.4%, 1.6 points ahead of SPY; RICH entries still lag by 13.5 points and CHEAP lead by 5.3.

Across both batches (314 dates): the series' misses are concentrated where the anchor year is a trough (2009 RICH at the low) and in
early 2010 (CHEAP on the first post-trough print). A hypothesis for the live model, to test on other banks before any use: a
last-year-EPS anchor needs a rule for the year after a collapse. Not tested here: any other bank, any other cycle.

## 2014-2017 (208 dates)

Scored on 2026-11-19, after the point-in-time build was committed (0441b24) and the firewall had passed at 27 cutoffs, and after the
decisions, checks and sensitivities of retro/README.md ("JPM 2014-2017") were written; the build was not yet pushed when the outcomes were
computed. Every date has its 6-month, 1-, 2- and 3-year horizons. Dividends are $0.38 a quarter to mid-2014, then $0.40, $0.44, $0.48,
$0.50 and $0.56 (from late 2017). The P/E percentile rows group the dates by `PE_NOW_PCTL`, the multiple's place in its own ten-year range
on the as-of date (a point-in-time number the method already prints; the grouping is hindsight).

| Group | Dates | Mean 2-yr total return | Median | Mean vs SPY | Beat SPY | Cleared hurdle | Mean m12-24 avg price | Mean max drawdown | Call held |
|---|---|---|---|---|---|---|---|---|---|
| all | 208 | +43.9% | +37.8% | +20.2pp | 187 | 125 | +27.8% | -20.7% | 22 |
| 2014 | 51 | +18.4% | +18.1% | +5.8pp | 37 | 7 | +9.2% | -23.8% | 15 |
| 2014, FAIR | 2 | +14.2% | +14.2% | +2.7pp | 1 | 0 | +14.1% | -20.1% | 2 |
| 2014, RICH | 49 | +18.6% | +18.1% | +6.0pp | 36 | 7 | +9.0% | -24.0% | 13 |
| 2015 | 53 | +50.6% | +51.6% | +27.3pp | 53 | 51 | +24.2% | -23.3% | 0 |
| 2015, FAIR | 6 | +58.3% | +56.5% | +42.0pp | 6 | 6 | +18.8% | -24.3% | 0 |
| 2015, RICH | 47 | +49.6% | +50.4% | +25.5pp | 47 | 45 | +24.9% | -23.2% | 0 |
| 2016 | 52 | +76.6% | +80.4% | +40.9pp | 52 | 48 | +58.4% | -13.2% | 0 |
| 2016, FAIR | 5 | +102.8% | +104.5% | +53.6pp | 5 | 5 | +64.2% | -12.5% | 0 |
| 2016, RICH | 47 | +73.8% | +79.6% | +39.6pp | 47 | 43 | +57.8% | -13.2% | 0 |
| 2017 | 52 | +29.6% | +30.9% | +6.4pp | 45 | 19 | +19.0% | -22.4% | 7 |
| 2017, RICH | 52 | +29.6% | +30.9% | +6.4pp | 45 | 19 | +19.0% | -22.4% | 7 |
| class FAIR | 13 | +68.6% | +64.2% | +40.4pp | 12 | 11 | +35.5% | -19.1% | 2 |
| class RICH | 195 | +42.3% | +36.7% | +18.9pp | 175 | 114 | +27.3% | -20.8% | 20 |
| tier WATCHLIST | 8 | +47.3% | +55.0% | +32.2pp | 7 | 6 | +17.7% | -23.2% | 2 |
| tier AVOID | 200 | +43.8% | +37.4% | +19.8pp | 180 | 119 | +28.2% | -20.6% | 20 |
| Q4-print intervals | 24 | +48.7% | +42.3% | +24.2pp | 19 | 12 | +30.6% | -20.2% | 5 |
| other dates | 184 | +43.3% | +37.8% | +19.7pp | 168 | 113 | +27.4% | -20.7% | 17 |
| RICH, Ratio B infinite | 48 | +27.8% | +27.1% | +5.4pp | 41 | 12 | +18.6% | -22.0% | 7 |
| RICH, Ratio B finite | 147 | +47.0% | +43.7% | +23.3pp | 134 | 102 | +30.1% | -20.4% | 13 |
| P/E percentile 0-39 | 23 | +89.5% | +92.8% | +52.0pp | 23 | 23 | +59.0% | -14.1% | 0 |
| P/E percentile 40-59 | 29 | +66.1% | +75.4% | +37.1pp | 28 | 26 | +44.3% | -17.2% | 2 |
| P/E percentile 60-79 | 101 | +35.2% | +36.0% | +15.7pp | 88 | 58 | +19.9% | -22.8% | 13 |
| P/E percentile 80-100 | 55 | +29.4% | +28.9% | +6.4pp | 48 | 18 | +20.5% | -21.4% | 7 |

What the labels say, as hypotheses only:

- **The class was wrong on almost every date.** 195 of the 208 dates are RICH and returned a mean +42.3% over two years, 18.9 points
  ahead of SPY; 175 of them beat SPY and 114 cleared the 15%/yr hurdle, so the RICH call held on 20. The 13 FAIR dates did better still
  (+68.6%, +40.4 points) and held on 2. All 200 AVOID dates together returned +43.8%. "Call held" reads 22 of 208, the series' worst.
- **The class here measures the 2008 trough, not the price.** BEAR is FY07 to FY08, -80.1%/yr, on every date, a BEAR price of $1.34 to
  $1.98, so the downside in Ratio B is about 97% whatever the price. Ratio B then rests on the upside to BULL, and BULL's growth falls as
  the low early years (FY04 $1.45, FY05 $2.45) leave the ten years: +13.0%/yr in 2014 to +3.8% in 2017. The class turned RICH and stayed
  there while earnings rose from $4.35 to $6.19; the price rose with them. Most FAIR dates are the Q4-print intervals, when the history
  briefly holds an eleventh, older year.
- **The multiple's own percentile ordered the outcomes where the class did not.** Entries at the 0-39th percentile of the ten-year range
  (23 dates: three in January 2015 and twenty from January to July 2016, at 9.5-10.7x) returned +89.5% over two years; the 40-59th +66.1%; the 60-79th +35.2%; the 80th
  and above +29.4%, still 6.4 points ahead of SPY. The method already scores this percentile (the valuation factor), but with a weight
  that the Ratio B rule overrides in the class. A hypothesis for the live model, to test on other banks and periods before any use: when
  BEAR is a single trough year outside the current cycle, the percentile, not Ratio B, carries the information.
- **Scenario landing:** BULL on 192 dates and BASE on 16; never near BEAR. Over 2014-2017 the scenario that came true is the one the
  method gave the least room (BULL at +3.8% to +13.8%/yr against EPS that rose 42% from FY13 to FY16).
- **By year:** 2014 +18.4% (+5.8 points against SPY), 2015 +50.6% (+27.3), 2016 +76.6% (+40.9), 2017 +29.6% (+6.4). The 2016 entries,
  the cheapest by percentile, returned the most; one stock in one period is one observation.
- **Three-year horizon:** a mean +65.6%, 26.3 points ahead of SPY (166 of 208 ahead); the 2017 entries, whose third year ends in 2020,
  lag SPY by 11.7 points on average.

Across the three batches (522 dates): the classes ordered the outcomes in 2008 and over 2010-2013 and failed in 2009, early 2010 and all
of 2014-2017. Each failure traces to the history's trough year: as the anchor at the 2009 low, and as BEAR from the Q4 2008 print on. A hypothesis for
the live model, as in 2010-2013 and still untested elsewhere: a last-year-EPS method needs a rule for a single collapse year, here for
BEAR as well as for the anchor. Not tested here: any other bank, any other cycle.

## 2018-2021 (209 dates)

Scored on 2026-11-19, after the point-in-time build was committed (ab268ad), the firewall had passed at 25 cutoffs, and the decisions,
checks and sensitivities of retro/README.md ("JPM 2018-2021") were written; the build was not yet pushed when the outcomes were computed.
Every date has its 6-month, 1-, 2- and 3-year horizons (the 2021 entries' third year ends in 2024). Dividends are $0.56 a quarter to
October 2018, then $0.80, $0.90 (from October 2019) and $1.00 (from October 2021). This section was written by the session that wrote the
2014-2017 one, so the P/E percentile rows test that section's hypothesis on four years it was not drawn from.

| Group | Dates | Mean 2-yr total return | Median | Mean vs SPY | Beat SPY | Cleared hurdle | Mean m12-24 avg price | Mean max drawdown | Call held |
|---|---|---|---|---|---|---|---|---|---|
| all | 209 | +18.2% | +17.5% | -8.7pp | 58 | 61 | +10.0% | -40.1% | 147 |
| 2018 | 52 | +2.9% | -2.8% | -18.4pp | 5 | 3 | +3.1% | -39.9% | 42 |
| 2018, FAIR | 5 | +25.8% | +24.8% | -20.8pp | 0 | 2 | +8.0% | -44.0% | 0 |
| 2018, RICH | 47 | +0.4% | -3.7% | -18.2pp | 5 | 1 | +2.5% | -39.5% | 42 |
| 2019 | 52 | +43.3% | +44.1% | -6.8pp | 14 | 44 | +12.0% | -44.0% | 30 |
| 2019, CHEAP | 6 | +40.5% | +41.3% | -5.8pp | 1 | 5 | +2.6% | -44.0% | 5 |
| 2019, FAIR | 20 | +51.8% | +52.6% | +1.7pp | 12 | 19 | +11.6% | -44.0% | 19 |
| 2019, RICH | 26 | +37.4% | +38.8% | -13.6pp | 1 | 20 | +14.5% | -44.0% | 6 |
| 2020 | 53 | +28.4% | +25.4% | -4.5pp | 26 | 14 | +39.6% | -36.1% | 36 |
| 2020, CHEAP | 32 | +33.7% | +29.9% | -2.0pp | 17 | 14 | +52.7% | -34.0% | 25 |
| 2020, FAIR | 8 | +23.7% | +24.4% | -9.0pp | 3 | 0 | +31.5% | -36.8% | 4 |
| 2020, RICH | 13 | +18.2% | +17.0% | -7.8pp | 6 | 0 | +12.2% | -40.9% | 7 |
| 2021 | 52 | -2.0% | -2.2% | -5.3pp | 13 | 0 | -15.2% | -40.4% | 39 |
| 2021, RICH | 52 | -2.0% | -2.2% | -5.3pp | 13 | 0 | -15.2% | -40.4% | 39 |
| class CHEAP | 38 | +34.8% | +33.0% | -2.6pp | 18 | 19 | +44.8% | -35.6% | 30 |
| class FAIR | 33 | +41.0% | +46.6% | -4.3pp | 15 | 21 | +15.9% | -42.3% | 23 |
| class RICH | 138 | +8.1% | +2.0% | -11.5pp | 25 | 21 | -1.0% | -40.8% | 94 |
| tier BUY | 36 | +34.1% | +30.9% | -2.5pp | 17 | 17 | +47.9% | -35.1% | 29 |
| tier ACCUMULATE | 9 | +41.4% | +40.5% | -0.2pp | 5 | 5 | +21.0% | -38.3% | 7 |
| tier WATCHLIST | 35 | +38.4% | +43.9% | -4.8pp | 15 | 22 | +12.4% | -43.1% | 18 |
| tier AVOID | 129 | +6.6% | +1.1% | -12.1pp | 21 | 17 | -2.0% | -40.8% | 93 |
| P/E percentile 0-39 | 35 | +33.2% | +29.7% | -2.5pp | 18 | 14 | +52.5% | -33.7% | 27 |
| P/E percentile 40-59 | 8 | +34.7% | +26.9% | +2.6pp | 5 | 3 | +16.9% | -40.1% | 6 |
| P/E percentile 60-79 | 31 | +42.9% | +48.0% | -0.8pp | 16 | 25 | +9.8% | -43.5% | 20 |
| P/E percentile 80-100 | 135 | +7.6% | +1.5% | -12.8pp | 19 | 19 | -1.4% | -41.0% | 94 |
| RICH, Ratio B infinite | 58 | +1.6% | -0.4% | -4.4pp | 17 | 1 | -12.9% | -37.9% | 41 |

What the labels say, as hypotheses only:

- **The class ordered the outcomes again, mostly through RICH.** CHEAP +34.8% over two years (-2.6 points against SPY), FAIR +41.0%
  (-4.3), RICH +8.1% (-11.5); AVOID +6.6% against +34-41% for the other tiers. "Call held" reads 147 of 209, against 22 of 208 in
  2014-2017: with FY2008 gone from BEAR (from 2018-03-02) Ratio B measured the price again. Every class and tier lagged SPY on average
  (ACCUMULATE by only 0.2 points); FAIR in 2019 (+1.7) and the 40-59th percentile (+2.6) are the groups that led.
- **The RICH years were the weak ones.** 2018 (RICH on 47 of 52) returned +2.9% and lagged SPY by 18.4 points; 2021 (RICH on all 52, on
  FY20's reserve-build EPS) returned -2.0%, 5.3 points behind. The 2020 entries, CHEAP on 32 dates through the COVID fall, returned
  +33.7% (the CHEAP ones), and their m12-24 average price was 52.7% above entry.
- **The percentile hypothesis of 2014-2017, out of period: half held.** Entries at the 80th percentile of the ten-year range or above
  (135 dates, mostly 2018 and 2021) returned +7.6% and lagged SPY by 12.8 points, again the worst group. Below the 80th the order did not
  hold: the 0-39th returned +33.2%, the 40-59th +34.7%, the 60-79th +42.9% (25 of its 31 dates are 2019 entries, whose two years end in
  2021). So "expensive against its own range lags" survived one more period; "cheaper is better all the way down" did not.
- **Scenario landing:** BULL on 107 dates, BASE on 100 and BEAR on 2 (2020-10-02 and 2020-10-09, CHEAP entries whose two years ended at
  the 2022 low): the first JPM dates near BEAR, now that BEAR is a -16% to -17% year rather than 2008's -80%.
- **Drawdowns:** a mean -40.1% inside the two years, every entry year through the COVID fall or the 2022 decline.
- **Three-year horizon:** a mean +40.6%, 4.5 points behind SPY; CHEAP entries +59.9% (+11.0), FAIR +40.1% (-16.4), RICH +35.4% (-5.8).

Across the four batches (731 dates): the class ordered JPM's outcomes in 2008, 2010-2013 and 2018-2021 and failed in 2009 (the trough
year as the anchor) and 2014-2017 (the trough year as BEAR, -80%/yr, while the price rose away from a shrinking BULL). In 2010-2013 BEAR
was the trough too, but the price sat far enough under BULL for Ratio B to separate the dates. The hypothesis for the live model, still
untested on any other bank: with a single collapse year as BEAR, Ratio B depends on the BULL upside alone and stops measuring the price
once the price nears BULL; the class became informative again when that year left BEAR.
