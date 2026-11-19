# JPM retrospective findings (hindsight)

Patterns seen in `outcome.json` for the JPM weekly dates (JPMorgan Chase & Co., NYSE: JPM): 314 in all, 105 from 2008-01-04 to 2009-12-31
and 209 from 2010-01-08 to 2013-12-31 (the second section below). They are
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
