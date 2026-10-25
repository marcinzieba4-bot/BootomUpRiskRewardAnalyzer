# UNP retrospective findings (hindsight)

Patterns seen in `outcome.json` for the 366 weekly dates from 2008-01-04 to 2014-12-31. They are **labels and
hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored only after its
point-in-time build was committed: January-March 2008 in 68cbbb6, April-December 2008 in 0019904, 2009 in 4f3f27e,
2010 in 3198278, 2011-2012 in 9e129f3, 2013-2014 in ee9a0c1.

## 2008 (53 dates) Medians of an even count
take the upper middle value (`statistics.median_high`). Prices are on each date's share basis (2-for-1 split
effective 2008-05-29).

| Group | Dates | Median 2-yr total return | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price |
|---|---|---|---|---|---|
| class CHEAP | 13 | +85% | 13 | 13 | +48% |
| class FAIR | 8 | +22% | 1 | 8 | -5% |
| class RICH | 32 | +2% | 0 | 32 | -12% |
| legacy tier BUY | 7 | +100% | 7 | 7 | +60% |
| legacy tier ACCUMULATE | 5 | +53% | 5 | 5 | +22% |
| legacy tier WATCHLIST | 9 | +22% | 2 | 9 | -5% |
| legacy tier AVOID | 32 | +2% | 0 | 32 | -12% |
| price below the EPP floor | 6 | +102% | 6 | 6 | +62% |
| CHEAP, above the floor | 7 | +53% | 7 | 7 | +22% |

- **The calls ranked the outcomes in order.** CHEAP did better than FAIR, which did better than RICH, and the tier
  order was the same: BUY > ACCUMULATE > WATCHLIST > AVOID. All 13 CHEAP dates (2008-10-03 to 2008-12-31, except
  FAIR on 2008-10-31) cleared the hurdle. None of the 32 RICH dates did.
- **RICH was right on price, wrong against the market.** RICH dates lost money on the m12-24 average price (-12%) and
  were flat over two years. Every one still beat SPY, because the market fell further. So every RICH call "missed" its
  own test, which expects RICH to lag the benchmark. On this stock in 2008, RICH read "don't buy here", not "will
  underperform".
- **The turn came with the price, not the numbers.** The class moved from RICH (late September, 18-19x) to CHEAP
  (2008-10-03, 15.5x) as the stock fell. The latest print was still Q2 (carloads -3%, revenue per car +16%). The Q3
  print (2008-10-23: carloads -5%, revenue per car +22%, operating ratio better) kept it CHEAP. The six dates below the EPP floor (2008-11-21 and 2008-12-05 to 2008-12-31, at 10.7-11.9x) returned +98% to
  +122%.
- **The BEAR case never came.** All 53 two-year outcomes landed in BASE or BULL. The worst point (2009-03-09) was
  still above every date's BEAR price. The BEAR rule (the decade's worst EPS year, 2004 at -29%, repeated for two
  years) set Ratio B high on most RICH dates. Test it on other cyclicals before any method change.
- **One stock, one crash.** Nearly all the spread between classes comes from buying before or after the
  October-December 2008 decline. This mostly tests "buy lower". Testing selection needs many tickers on the same
  dates.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price |
|---|---|---|---|---|---|---|
| class CHEAP (2009-01-09 to 2009-07-10) | 23 | +119% | +96% to +180% | 23 | 23 | +81% |
| class FAIR | 3 | +93% | +93% to +98% | 3 | 3 | +68% |
| class RICH (from 2009-07-17) | 26 | +62% | +41% to +90% | 26 | 26 | +52% |
| legacy tier BUY | 33 | +112% | +47% to +180% | 33 | 33 | +77% |
| legacy tier ACCUMULATE | 17 | +55% | +41% to +71% | 17 | 17 | +52% |
| price below the EPP floor | 26 | +119% | +88% to +180% | 26 | 26 | +81% |

- **Every 2009 date made money.** Over two years the worst return was +41%, all 52 cleared the hurdle and beat SPY,
  and every outcome landed in BULL.
- **CHEAP and the low-P/E dates were the best**, as in 2008. The four dates from 2009-02-27 to 2009-03-20 (7.7-8.5x on FY08
  EPS) returned +152% to +180%, the best being 2009-03-06.
- **RICH from July was a wrong call in absolute terms.** The ranking held (CHEAP +119% vs RICH +62%), but RICH
  expects a miss, and all 26 RICH dates more than doubled the hurdle's pace. The cause is the no-revenue-guide
  fallback. From the Q1 2009 print it carries the trough quarter's freight revenue (-20%, then -28% and -25%)
  forward for two years. The BASE price falls below the market, and the adjusted gap reads "overvalued".
  The legacy tier, driven by Ratio B, stayed at BUY or ACCUMULATE and ranked those dates better.
- **The no-guide fallbacks are the open question for cyclicals.** Two are doing the work here. EPS stays at the
  last full year (FY08 $4.54), and growth follows the latest quarter. At a turn they anchor on the wrong point:
  growth on the trough, EPS on the peak. Test alternatives (the decade median revenue growth, a
  multi-quarter average) on other companies without guidance before any method change. Never fit them to UNP's
  outcomes.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price |
|---|---|---|---|---|---|---|
| class FAIR (2010-07-02 to 2010-10-01, with RICH weeks between) | 13 | +65% | +51% to +79% | 13 | 13 | +40% |
| class RICH | 39 | +54% | +33% to +95% | 39 | 39 | +37% |
| RICH, January-July | 26 | +62% | +45% to +95% | 26 | 26 | +43% |
| RICH, October-December | 13 | +40% | +33% to +49% | 13 | 13 | +27% |
| legacy tier WATCHLIST | 10 | +70% | +59% to +73% | 10 | 10 | +43% |
| legacy tier AVOID | 42 | +54% | +33% to +95% | 42 | 42 | +37% |

- **No CHEAP date, and every date doubled the hurdle's pace or close to it.** All 52 cleared the hurdle, all beat SPY
  (median +32pp), and every outcome landed in BULL.
- **RICH was wrong all year in absolute terms; the ordering still held.** FAIR beat RICH, WATCHLIST beat AVOID, and
  the October-December RICH dates (22.6-25.3x on FY09 EPS) returned least. So the class ranked the dates but set its line far
  too low.
- **Why the model read RICH.** With no 2010 guide, the P/E ran on trailing FY09 EPS ($3.75, then $3.74). The trough
  year's earnings put the stock at the top of its own ten-year range while earnings were recovering fast.
  2010's quarterly EPS ($1.01, $1.40, $1.56) ran well above 2009's. This is the 2009 lesson from the other side:
  the no-guide fallback anchors EPS on the last full year, the peak in 2009 and the trough in 2010.
- **The BEAR rule kept Ratio B high** (BEAR near $24, the 2004 year applied twice), so the legacy tier read AVOID on
  42 dates. Every one of them returned at least +33%.

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY (median excess) | Median m12-24 avg price |
|---|---|---|---|---|---|---|
| class CHEAP (2011-08-19 to 2011-10-07) | 7 | +88% | +78% to +98% | 7 | 7 (+37pp) | +61% |
| class FAIR | 19 | +50% | +39% to +80% | 19 | 19 (+27pp) | +27% |
| class RICH | 26 | +58% | +38% to +67% | 26 | 26 (+26pp) | +31% |
| legacy tier ACCUMULATE | 4 | +97% | +88% to +98% | 4 | 4 (+43pp) | +70% |
| legacy tier WATCHLIST | 21 | +52% | +43% to +80% | 21 | 21 (+28pp) | +28% |
| legacy tier AVOID | 27 | +58% | +38% to +67% | 27 | 27 (+25pp) | +31% |

- **Every 2011 date made money and beat the market.** All 52 cleared the hurdle and beat SPY (median +27pp), and
  every outcome landed in BULL. The worst was 2011-01-14 (+38%), the last date priced on trailing FY09 EPS.
- **CHEAP was best again, and the August-October sell-off was the entry.** The seven CHEAP dates ($82-90, 14.8-16.2x
  FY10 EPS) returned +78% to +98%. The four ACCUMULATE dates among them returned +88% to +98%, the best being
  2011-09-23.
- **On total return FAIR trailed RICH; on excess return the order held.** FAIR's median is +50% and RICH's +58%.
  But 13 of the 19 FAIR dates are January-April (16.9-17.9x on FY10 EPS, +39% to +52%). Their two-year windows end
  in early 2013, the RICH ones of April-July (17.4-19.3x, +47% to +64%) in mid-2013. Against SPY over the same
  windows the class order holds, if narrowly between FAIR and RICH: CHEAP +37pp, FAIR +27pp, RICH +26pp. The tiers
  too: ACCUMULATE +43pp, WATCHLIST +28pp, AVOID +25pp. The October-December RICH dates beat SPY by least (median
  +12pp).
- **RICH was wrong in absolute terms for the third year running.** All 26 RICH dates cleared the hurdle, 23 of them
  by more than half again.

## 2012 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY (median excess) | Median m12-24 avg price |
|---|---|---|---|---|---|---|
| class CHEAP (2012-03-09, 2012-03-30) | 2 | +80% | +77% to +80% | 2 | 2 (+41pp) | +50% |
| class FAIR (2012-01-20 to 2012-07-06) | 22 | +74% | +53% to +89% | 22 | 22 (+31pp) | +47% |
| class RICH | 29 | +82% | +58% to +111% | 29 | 29 (+40pp) | +52% |
| RICH from 2012-07-13 | 26 | +87% | +62% to +111% | 26 | 26 (+44pp) | +53% |
| legacy tier WATCHLIST | 20 | +74% | +53% to +89% | 20 | 20 (+33pp) | +47% |
| legacy tier AVOID | 33 | +79% | +58% to +111% | 33 | 33 (+35pp) | +48% |

- **Every 2012 date made money and beat the market** (median +33pp). 37 outcomes landed in BULL. 16 of the 18
  dates from 2012-09-07 on landed in XBULL.
- **The ordering broke, on total and excess return alike.** RICH beat FAIR and matched the two CHEAP dates, and
  AVOID beat WATCHLIST. The last 26 dates, RICH at 17.5-19.1x on FY11 EPS, returned the most: +62% to +111%, the best
  being 2012-11-16.
- **Why the model read RICH.** With no 2012 guide, the P/E ran all year on FY11's $6.72. Meanwhile each 2012
  quarter was published as it came: EPS of $1.79, $2.10 and $2.19 (against $1.29, $1.59 and $1.85), and operating
  ratios 4.2, 4.3 and 2.5 points better. The method has no margin step without a numeric guide, and BASE growth took
  the slowing freight revenue (+14%, then +7% and +4%). So the model saw 17-19x on last year's earnings and slowing
  revenue, while earnings grew through the operating ratio.
- **The BEAR case never came close.** BEAR prices were $24-44. The lowest price within any 2011-2012 date's two
  years was $79.83 (2011-10-03). Every date's two-year low was at least 2.28 times its BEAR price.

## 2013 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY (median excess) | Median m12-24 avg price |
|---|---|---|---|---|---|---|
| class RICH (every date) | 52 | +30% | -3% to +88% | 25 | 27 (+2pp) | +40% |
| legacy tier WATCHLIST (2013-01-25 to 2013-04-12) | 12 | +80% | +57% to +88% | 12 | 12 (+38pp) | +55% |
| legacy tier AVOID | 40 | +24% | -3% to +81% | 13 | 15 (-4pp) | +38% |
| AVOID, 2013-06-28 to 2013-12-31 | 28 | +18% | -3% to +32% | 1 | 4 (-6pp) | +37% |

- **Every date read RICH; the tier did the ranking.** The Q4 2012 print put FY12's $8.27 into the P/E, and the next
  12 dates read WATCHLIST at 16.1-17.2x. They returned +57% to +88%, and all cleared the hurdle and beat SPY (median
  +38pp). The 40 AVOID dates (17.6-20.3x, apart from the two January dates on trailing FY11 EPS) returned a median
  +24%.
- **RICH turned right during the year.** Returns fell date by date as the two-year windows ran into late 2015. The
  April-June dates returned +33% to +54%. From 2013-06-28 the median was +18%: 1 of 28 dates cleared the hurdle and 4
  beat SPY. These are the first RICH calls in the series to hit (miss the hurdle and lag SPY): none of the 152 RICH
  dates of 2008-2012 did, 24 of 2013's did.

## 2014 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY (median excess) | Median m12-24 avg price |
|---|---|---|---|---|---|---|
| class FAIR = legacy tier WATCHLIST (2014-02-14 to 2014-03-28, 2014-04-11) | 8 | -8% | -10% to -6% | 0 | 0 (-20pp) | -1% |
| class RICH = legacy tier AVOID | 44 | -9% | -20% to +0% | 0 | 0 (-21pp) | -16% |

- **Every 2014 date lost money over two years** (-20% to 0%). None cleared the hurdle or beat SPY (median -20pp), and
  every outcome landed in BASE. The deepest fall within two years was -44% (from 2014-01-31). All 44 RICH calls hit.
- **The prints were the best of the series, and the stock was at the top of its range.** 2014's quarters had
  carloads +5% to +8%, operating ratios 2.0-2.5 points better and EPS up 17-23%. The model still read RICH: 18.2-25.9x
  trailing EPS, the 80th-100th percentile of its ten-year range (90th-100th from the Q1 print on).
- **FAIR did not rank above RICH within the year** (-8% against -9%). Both trailed SPY by about 20pp.
- **The BEAR case never came.** Even through the 2015-2016 fall, every date's two-year low stayed at least 1.64 times
  its BEAR price.

## Across 2008-2014: the no-guide fallbacks are the open question

UNP gave no numeric full-year guide from 2009 on, so three fallbacks did the work: the last full year's EPS stands,
BASE growth takes the latest quarter's revenue growth, and there is no margin step. They anchored on the peak in
2009, the trough in 2010, and last year's earnings while margins expanded in 2012. Price level still ranked the dates
in most years: the CHEAP stretches of late 2008, early 2009 and autumn 2011 were the best entries. RICH set its line
too low from 2009 to 2012, then was right from mid-2013 through 2014.

**A high P/E percentile did not separate 2010 from 2014.** Both read RICH at the top of the stock's own range: in 2010
at the 99th-100th percentile on trailing FY09 EPS, with a median two-year return of +54%; in 2014 at the 90th-100th
percentile on trailing FY13 EPS, with -9%. What was visible at the time: 2010's P/E ran on a trough year (FY09 EPS
-17%), 2014's on a record year after four years of growth.

Candidates to test on other companies without guidance, never fitted to UNP's outcomes:
- trailing-four-quarter EPS, which is published by AS_OF and so carries no hindsight;
- a margin step from the latest quarters' published operating-ratio change;
- a cyclical BEAR from the worst two-year run rather than the worst year applied twice;
- a P/E on normalized earnings (the ten-year median or trend EPS), which would read a trough year and a record year
  differently.
